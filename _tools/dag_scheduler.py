#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DAG Scheduler —— 多 Agent 团队任务编排的状态机底座（skills/_tools）

设计单源：rules/07 §十 10.5/10.7（原子性与版本）+ wb-subagent-delegation（拓扑选型/门禁）+ r485C
不变式：给定相同状态 + 相同事件，产出相同下一状态。LLM 在提示层（不确定），状态机在文件层（确定）。
本脚本【不自己起 Agent】，只产出「谁该跑、谁可并行、跑完能不能解锁」；执行交给 WB Agent 工具。

子命令：
  init  <dag.json>                     从 spec 建 DAG 状态文件
  plan  <state.json>                   输出就绪队列 + 并行分组 + 每任务的 model 档位建议
  claim <state.json> <task_id>         pending/ready -> running，重试计数 +1
  done  <state.json> <task_id> <evidence>  记录执行证据；证据为空则拒收（门禁）
  fail  <state.json> <task_id> <reason>    记录失败原因；超过上限 -> needs_human（转人工）
  status <state.json>                  全局视图（counts / ready / running / blocked）
  verify <state.json> <task_id> <cmd...>  恢复前核对真实执行状态，防重复副作用
  reset-running <state.json>            把 running 且无证据的任务退回 ready（未确认则不动）

状态文件与 DAG 存放在同一提交边界内：状态 + 证据一次原子写（tmp + os.replace），
避免 r346C 说的「必须一致的状态对分开落盘即失步窗口」。
「放弃」的语义是状态不推进：reset-running 不留失败痕迹，下一轮天然重做。

仅标准库。零第三方依赖。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from typing import Any, Dict, List

# ---------- 状态机定义 ----------
PENDING, READY, RUNNING, DONE, FAILED, NEEDS_HUMAN = (
    "pending", "ready", "running", "done", "failed", "needs_human",
)
TERMINAL = {DONE, NEEDS_HUMAN}
OPEN_STATES = {PENDING, READY, RUNNING, FAILED}

SCHEMA = "dag_scheduler/v1"


# ---------- 原子读写（状态 + 证据同一次提交） ----------
def _atomic_write_json(path: str, obj: Any) -> None:
    d = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".dag_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.unlink(tmp)
            except OSError:
                pass


def load(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(path: str, state: Dict[str, Any]) -> None:
    _atomic_write_json(path, state)


# ---------- 拓扑校验（节点级校验，不整体重规划） ----------
def detect_cycles(tasks: Dict[str, dict]) -> List[List[str]]:
    """DFS 三色标记，返回所有发现的环（每个环一条）。"""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {k: WHITE for k in tasks}
    stack: List[str] = []
    cycles: List[List[str]] = []

    def dfs(n: str) -> None:
        color[n] = GRAY
        stack.append(n)
        for dep in tasks.get(n, {}).get("deps", []):
            if dep not in tasks:
                continue
            if color[dep] == GRAY:
                i = stack.index(dep)
                cycles.append(stack[i:] + [dep])
            elif color[dep] == WHITE:
                dfs(dep)
        stack.pop()
        color[n] = BLACK

    for n in sorted(tasks):
        if color[n] == WHITE:
            dfs(n)
    return cycles


def validate(spec: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    tasks = spec.get("tasks", {})
    if not tasks:
        errs.append("spec.tasks 为空")
    for tid, t in tasks.items():
        for dep in t.get("deps", []):
            if dep not in tasks:
                errs.append(f"[未知依赖] {tid} -> {dep}")
        if tid in t.get("deps", []):
            errs.append(f"[自环] {tid}")
        mt = t.get("max_attempts", 2)
        if not isinstance(mt, int) or mt < 1:
            errs.append(f"[重试上限非法] {tid}: max_attempts={mt}")
        for req in t.get("gate", []):
            if not isinstance(req, str) or not req.strip():
                errs.append(f"[门禁项非法] {tid}")
    for c in detect_cycles(tasks):
        errs.append("[循环依赖] " + " -> ".join(c))
    return errs


def refresh(state: Dict[str, Any]) -> None:
    """重算派生状态：只有全部前置 done 才解锁；前置 failed/needs_human 则阻塞下游。"""
    tasks = state["tasks"]
    for tid, t in tasks.items():
        if t["state"] in TERMINAL:
            continue
        deps = t.get("deps", [])
        if t["state"] == RUNNING:
            continue
        dep_states = [tasks[d]["state"] for d in deps if d in tasks]
        if any(s in (FAILED, NEEDS_HUMAN) for s in dep_states):
            t["state"] = FAILED if t.get("attempts", 0) < t.get("max_attempts", 2) else NEEDS_HUMAN
            t["blocked_by"] = [d for d in deps if tasks.get(d, {}).get("state") in (FAILED, NEEDS_HUMAN)]
        elif all(s == DONE for s in dep_states):
            t["state"] = READY
            t.pop("blocked_by", None)
        elif t["attempts"] >= t.get("max_attempts", 2) and t["state"] == FAILED:
            t["state"] = NEEDS_HUMAN
        else:
            t["state"] = PENDING


def ready_layers(state: Dict[str, Any]) -> List[List[str]]:
    """就绪队列分层：同层内无依赖关系 => 可真并行（交给 run_in_background）。"""
    tasks = state["tasks"]
    done = {k for k, v in tasks.items() if v["state"] == DONE}
    layers: List[List[str]] = []
    remaining = {k for k, v in tasks.items() if v["state"] == READY}
    while remaining:
        layer = sorted(k for k in remaining if all(d in done for d in tasks[k].get("deps", [])))
        if not layer:
            break
        layers.append(layer)
        remaining -= set(layer)
    return layers


def _model_hint(t: dict) -> str:
    if t.get("model"):
        return t["model"]
    d = t.get("difficulty", "L1")
    return {"L0": "qwen3.8-flash", "L2": "qwen3.8-max"}.get(d, "均衡模型(L1)")


# ---------- 子命令 ----------
def cmd_init(args) -> int:
    spec = load(args.spec)
    errs = validate(spec)
    if errs and not args.force:
        for e in errs:
            print("[拒绝] " + e)
        print("修好再 init，或显式 --force 忽略（不推荐）")
        return 2
    tasks = {}
    for tid, t in spec.get("tasks", {}).items():
        tasks[tid] = {
            "deps": list(t.get("deps", [])),
            "state": PENDING,
            "attempts": 0,
            "max_attempts": t.get("max_attempts", 2),
            "gate": list(t.get("gate", [])),
            "brief": t.get("brief", ""),
            "difficulty": t.get("difficulty", "L1"),
            "model": t.get("model"),
            "evidence": None,
            "reason": None,
            "history": [],
        }
    state = {
        "schema": SCHEMA,
        "team": spec.get("team", "unnamed"),
        "goal": spec.get("goal", ""),
        "tasks": tasks,
    }
    refresh(state)
    save(args.state, state)
    print(f"[init] {args.state}  tasks={len(tasks)}  ready={sum(1 for t in tasks.values() if t['state']==READY)}")
    return 0


def cmd_plan(args) -> int:
    state = load(args.state)
    refresh(state)
    save(args.state, state)
    layers = ready_layers(state)
    if not layers:
        print(json.dumps({"layers": [], "note": "无就绪任务"}, ensure_ascii=False))
        return 0
    tasks = state["tasks"]
    out = []
    for i, layer in enumerate(layers, 1):
        nodes = []
        for tid in layer:
            t = tasks[tid]
            nodes.append({
                "task": tid,
                "run_in_background": len(layer) > 1,
                "model": _model_hint(t),
                "gate": t["gate"],
                "brief": t["brief"],
            })
        out.append({"wave": i, "parallel": len(layer) > 1, "nodes": nodes})
    print(json.dumps({"layers": out}, ensure_ascii=False, indent=2))
    return 0


def cmd_claim(args) -> int:
    state = load(args.state)
    refresh(state)
    t = state["tasks"].get(args.task_id)
    if t is None:
        print(f"[错] 未知任务 {args.task_id}")
        return 2
    if t["state"] != READY:
        print(f"[拒绝] {args.task_id} 状态={t['state']}，只有 ready 可领取")
        return 2
    if t["attempts"] >= t["max_attempts"]:
        t["state"] = NEEDS_HUMAN
        save(args.state, state)
        print(f"[转人工] {args.task_id} 超出重试上限 {t['max_attempts']}")
        return 2
    t["state"] = RUNNING
    t["attempts"] += 1
    t["reason"] = None
    t["history"].append({"event": "claim", "attempt": t["attempts"]})
    save(args.state, state)
    print(f"[claim] {args.task_id} attempt={t['attempts']}/{t['max_attempts']}")
    return 0


def cmd_done(args) -> int:
    state = load(args.state)
    t = state["tasks"].get(args.task_id)
    if t is None:
        print(f"[错] 未知任务 {args.task_id}")
        return 2
    ev = (args.evidence or "").strip()
    if not ev:
        print("[门禁拒收] 未提供执行证据，不得标记成功（未取得执行证据不得标成功）")
        return 2
    t["state"] = DONE
    t["evidence"] = ev
    t["history"].append({"event": "done", "attempt": t["attempts"], "evidence": ev[:500]})
    refresh(state)
    save(args.state, state)
    newly = ready_layers(state)
    print(f"[done] {args.task_id}  新解锁={sum(len(w) for w in newly)}")
    return 0


def cmd_fail(args) -> int:
    state = load(args.state)
    t = state["tasks"].get(args.task_id)
    if t is None:
        print(f"[错] 未知任务 {args.task_id}")
        return 2
    reason = (args.reason or "").strip()
    if not reason:
        print("[门禁拒收] 失败必须记原因，否则重试链无法判断是否换路径")
        return 2
    t["reason"] = reason
    t["evidence"] = None
    t["state"] = FAILED if t["attempts"] < t["max_attempts"] else NEEDS_HUMAN
    t["history"].append({"event": "fail", "attempt": t["attempts"], "reason": reason[:500]})
    refresh(state)
    save(args.state, state)
    print(f"[fail] {args.task_id}  state={t['state']}  attempts={t['attempts']}/{t['max_attempts']}")
    return 0


def cmd_status(args) -> int:
    state = load(args.state)
    refresh(state)
    save(args.state, state)
    tasks = state["tasks"]
    counts: Dict[str, int] = {}
    for t in tasks.values():
        counts[t["state"]] = counts.get(t["state"], 0) + 1
    layers = ready_layers(state)
    print(json.dumps({
        "team": state.get("team"),
        "counts": counts,
        "ready_waves": layers,
        "needs_human": [k for k, v in tasks.items() if v["state"] == NEEDS_HUMAN],
        "tasks": {k: {"state": v["state"], "attempts": v["attempts"],
                      "reason": v["reason"], "has_evidence": bool(v["evidence"])}
                  for k, v in tasks.items()},
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_verify(args) -> int:
    """恢复前核对真实执行状态：外部命令退出码 0 视为已完成（有副作用的任务必须先跑这个）。"""
    state = load(args.state)
    t = state["tasks"].get(args.task_id)
    if t is None:
        print(f"[错] 未知任务 {args.task_id}")
        return 2
    try:
        p = subprocess.run(args.cmd, capture_output=True, text=True, timeout=args.timeout,
                           shell=False)
    except (OSError, subprocess.TimeoutExpired) as e:
        print(json.dumps({"result": "unknown", "detail": str(e)},
                         ensure_ascii=False))
        return 3
    out = (p.stdout or "").strip()
    if p.returncode == 0:
        t["state"] = DONE
        t["evidence"] = f"verify:{out[:400]}"
        t["history"].append({"event": "verify_done", "evidence": t["evidence"]})
        refresh(state)
        save(args.state, state)
        print(json.dumps({"result": "already_done", "evidence": t["evidence"]},
                         ensure_ascii=False))
        return 0
    print(json.dumps({"result": "not_done_or_unknown", "returncode": p.returncode,
                      "stdout": out[:400], "stderr": (p.stderr or "")[:400]},
                     ensure_ascii=False))
    return 1


def cmd_reset_running(args) -> int:
    """放弃语义 = 状态不推进：不记失败、不计痕迹，退回 ready 由下一轮重做。"""
    state = load(args.state)
    moved = []
    for tid, t in state["tasks"].items():
        if t["state"] == RUNNING and not t.get("evidence"):
            t["state"] = PENDING
            t["attempts"] = max(0, t["attempts"] - 1)  # 放弃不算一次失败尝试
            moved.append(tid)
    refresh(state)
    save(args.state, state)
    print(json.dumps({"reset": moved}, ensure_ascii=False))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="dag_scheduler", description="多 Agent DAG 状态机底座")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init"); p.add_argument("spec"); p.add_argument("state")
    p.add_argument("--force", action="store_true"); p.set_defaults(func=cmd_init)
    p = sub.add_parser("plan"); p.add_argument("state"); p.set_defaults(func=cmd_plan)
    p = sub.add_parser("claim"); p.add_argument("state"); p.add_argument("task_id")
    p.set_defaults(func=cmd_claim)
    p = sub.add_parser("done"); p.add_argument("state"); p.add_argument("task_id")
    p.add_argument("evidence"); p.set_defaults(func=cmd_done)
    p = sub.add_parser("fail"); p.add_argument("state"); p.add_argument("task_id")
    p.add_argument("reason"); p.set_defaults(func=cmd_fail)
    p = sub.add_parser("status"); p.add_argument("state"); p.set_defaults(func=cmd_status)
    p = sub.add_parser("verify"); p.add_argument("state"); p.add_argument("task_id")
    p.add_argument("cmd", nargs=argparse.REMAINDER); p.add_argument("--timeout", type=int, default=30)
    p.set_defaults(func=cmd_verify)
    p = sub.add_parser("reset-running"); p.add_argument("state"); p.set_defaults(func=cmd_reset_running)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())