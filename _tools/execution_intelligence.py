#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""execution_intelligence.py — Agent Execution Intelligence (EDG / GDR / CCS) · P0

把 HarnessMM 的 EDG / GDR / CCS 思想落成可运行、可验证、可回滚的外层调度工具。
不微调模型，不接管宿主工具调用，只做「已确定动作的保存、校验、复用与记账」。

设计单源：本文件 docstring + skills/_tools/README.md
复用而非新建：状态语义与原子写对齐 dag_scheduler.py；安全判定对齐 guardian_precheck.py。

子命令：
  compile <spec.json> <edg.json>      结构校验 + 权限校验 + 参数校验 -> 可执行决策图
  guard   <edg.json> <facts.json> <step_id>   单条 Guard 求值（true/false/unknown）
  plan    <edg.json> <facts.json>      GDR：reuse / already_done / needs_llm / confirm_required / blocked
  certify <edg.json> <facts.json> --ledger L.jsonl [--step ID ...]   签发执行证书（需真实证据）
  run     <edg.json> <facts.json> [--apply]   保守执行器：默认 dry-run，仅低风险幂等命令
  stats   <ledger.jsonl>              证书账本聚合（回调节省 / 证据覆盖率 / 原因分布）
  selftest                            内置 6 组可重复用例，全绿才退出 0
  schema                              打印 spec 结构约定

诚实边界（不得宣称已解决）：
  1. 本工具不调用、也无法跳过宿主的模型回调；它只判定「该步是否需要模型重新判断」，
     真正的跳过由宿主按 plan 输出执行。
  2. tokens_saved_estimate 是估算值（默认 1200 输入 + 300 输出/次），非实测计数。
  3. 未实现 RSI（自动改提示/改 Guard/改配置）：缺独立验证集与回滚通道，按规范 P2 暂缓。
  4. Guard 表达式只支持比较与布尔组合，不支持函数调用；未知字段返回 unknown 而非 false。

仅标准库。零第三方依赖。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional, Tuple

SCHEMA = "execution_intelligence/v1"
CERT_SCHEMA = "ccs_certificate/v1"
RISKS = ("low", "medium", "high")

# 允许的动作 + 必填参数。新增动作必须同时更新 guardian 检查，禁止裸扩展。
ACTIONS: Dict[str, List[str]] = {
    "noop": [],
    "read_file": ["path"],
    "write_file": ["path", "content"],
    "run_command": ["command"],
    "analyze_results": [],
}

# 语义字段：Guard 一旦引用，或步骤标记 semantic，即视为必须由 LLM 重新判断。
SEMANTIC_FIELDS = {"semantic", "judgement", "judgment", "is_correct",
                   "matches_intent", "quality", "relevance", "intent"}

# run --apply 的保守白名单：只放行只读或幂等的命令前缀。
CMD_ALLOWLIST = ("python", "python3", "pytest", "py.test", "echo", "dir", "ls",
                 "git status", "git diff", "git log", "type", "cat")

DEFAULT_IN_TOK = 1200
DEFAULT_OUT_TOK = 300
DEFAULT_TTL = 86400


class CompileError(Exception):
    def __init__(self, errors: List[str]):
        super().__init__("; ".join(errors))
        self.errors = errors


class GuardError(Exception):
    pass


# ------------------------------------------------------------------ helpers ---
def iso(ts: Optional[float] = None) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(time.time() if ts is None else ts))


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def atomic_write_json(path: str, obj: Any) -> None:
    d = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".ei_", suffix=".tmp")
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


def sha(obj: Any) -> str:
    body = json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(body).hexdigest()[:16]


# --------------------------------------------------------- guard 表达式求值 ---
class _Unknown:
    __slots__ = ()

    def __repr__(self) -> str:
        return "UNKNOWN"

    def __bool__(self) -> bool:
        raise GuardError("UNKNOWN 不可直接转布尔")


UNKNOWN = _Unknown()

_TOKEN_RE = re.compile(
    r"\s*(?:"
    r"(?P<num>-?\d+(?:\.\d+)?)"
    r"|(?P<str>'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")"
    r"|(?P<op>==|!=|>=|<=|>|<)"
    r"|(?P<lp>\()"
    r"|(?P<rp>\))"
    r"|(?P<id>[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)"
    r")"
)


def tokenize(expr: str) -> List[Tuple[str, str]]:
    pos, out = 0, []
    while pos < len(expr):
        m = _TOKEN_RE.match(expr, pos)
        if not m:
            if expr[pos:].strip() == "":
                break
            raise GuardError("无法解析位置 %d: %r" % (pos, expr[pos:pos + 20]))
        pos = m.end()
        for kind in ("num", "str", "op", "lp", "rp", "id"):
            val = m.group(kind)
            if val is not None:
                out.append((kind, val))
                break
    if not out:
        raise GuardError("空表达式")
    return out


def _refs(expr: str) -> List[str]:
    """表达式里引用到的字段名（排除布尔/逻辑关键字）。"""
    kw = {"and", "or", "not", "true", "false", "null", "none"}
    return [v for k, v in tokenize(expr) if k == "id" and v.lower() not in kw]


def _and(a: Any, b: Any) -> Any:
    if a is False or b is False:
        return False
    if a is UNKNOWN or b is UNKNOWN:
        return UNKNOWN
    return bool(a) and bool(b)


def _or(a: Any, b: Any) -> Any:
    if a is True or b is True:
        return True
    if a is UNKNOWN or b is UNKNOWN:
        return UNKNOWN
    return bool(a) or bool(b)


def _not(a: Any) -> Any:
    return UNKNOWN if a is UNKNOWN else (not bool(a))


class _Parser:
    def __init__(self, toks: List[Tuple[str, str]], facts: Dict[str, Any]):
        self.t = toks
        self.i = 0
        self.facts = facts

    def peek(self) -> Tuple[Optional[str], Optional[str]]:
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def eat(self, kind: Optional[str] = None, val: Optional[str] = None) -> Tuple[str, str]:
        k, v = self.peek()
        if k is None:
            raise GuardError("表达式意外结束")
        if kind and k != kind:
            raise GuardError("期望 %s，得到 %s:%s" % (kind, k, v))
        if val is not None and (v or "").lower() != val:
            raise GuardError("期望 %s，得到 %s" % (val, v))
        self.i += 1
        return k, v  # type: ignore[return-value]

    def parse(self) -> Any:
        r = self.or_expr()
        if self.i != len(self.t):
            raise GuardError("多余 token: %r" % (self.peek()[1],))
        return r

    def or_expr(self) -> Any:
        v = self.and_expr()
        while self.peek()[0] == "id" and (self.peek()[1] or "").lower() == "or":
            self.i += 1
            v = _or(v, self.and_expr())
        return v

    def and_expr(self) -> Any:
        v = self.not_expr()
        while self.peek()[0] == "id" and (self.peek()[1] or "").lower() == "and":
            self.i += 1
            v = _and(v, self.not_expr())
        return v

    def not_expr(self) -> Any:
        k, v = self.peek()
        if k == "id" and (v or "").lower() == "not":
            self.i += 1
            return _not(self.not_expr())
        return self.comparison()

    def comparison(self) -> Any:
        left = self.primary()
        k, v = self.peek()
        if k == "op":
            self.i += 1
            right = self.primary()
            return self._cmp(left, v, right)
        return left

    def primary(self) -> Any:
        k, v = self.peek()
        if k == "lp":
            self.i += 1
            r = self.or_expr()
            self.eat("rp")
            return r
        if k == "num":
            self.i += 1
            return float(v) if "." in (v or "") else int(v)
        if k == "str":
            self.i += 1
            return (v or "")[1:-1].encode("utf-8").decode("unicode_escape")
        if k == "id":
            self.i += 1
            low = (v or "").lower()
            if low == "true":
                return True
            if low == "false":
                return False
            if low in ("null", "none"):
                return None
            return self.resolve(v or "")
        raise GuardError("非法 token: %s:%s" % (k, v))

    def resolve(self, name: str) -> Any:
        parts = name.split(".")
        root, rest = parts[0], parts[1:]
        steps = self.facts.get("steps") or {}
        if root in steps and isinstance(steps[root], dict):
            cur: Any = steps[root]
        elif root in self.facts:
            cur = self.facts[root]
        else:
            return UNKNOWN
        for p in rest:
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            else:
                return UNKNOWN
        return cur

    @staticmethod
    def _cmp(a: Any, op: Optional[str], b: Any) -> Any:
        if a is UNKNOWN or b is UNKNOWN:
            return UNKNOWN
        try:
            if op == "==":
                return a == b
            if op == "!=":
                return a != b
            if op == ">":
                return a > b
            if op == "<":
                return a < b
            if op == ">=":
                return a >= b
            if op == "<=":
                return a <= b
        except TypeError:
            return UNKNOWN
        raise GuardError("未知运算符 %s" % op)


def eval_guard(expr: str, facts: Dict[str, Any]) -> Tuple[bool, Any, Dict[str, Any]]:
    """-> (resolved, value, detail)。resolved=False 表示存在未解析字段（应重新判断）。"""
    try:
        val = _Parser(tokenize(expr), facts).parse()
    except GuardError as e:
        return False, None, {"result": "unknown", "expr": expr, "error": str(e)}
    if val is UNKNOWN:
        missing = [r for r in _refs(expr) if _Parser(tokenize(expr), facts).resolve(r) is UNKNOWN]
        return False, None, {"result": "unknown", "expr": expr, "unresolved": missing}
    if isinstance(val, bool):
        return True, val, {"result": "true" if val else "false", "expr": expr}
    return True, bool(val), {"result": "true" if val else "false", "expr": expr,
                            "note": "非布尔值按真值处理"}


# ------------------------------------------------------------------- compile ---
def _topo(steps: Dict[str, Any]) -> List[str]:
    indeg = {k: 0 for k in steps}
    for k, s in steps.items():
        for d in s.get("depends_on", []):
            if d in indeg:
                indeg[k] += 1
    ready = sorted(k for k, v in indeg.items() if v == 0)
    out: List[str] = []
    while ready:
        n = ready.pop(0)
        out.append(n)
        for k, s in steps.items():
            if n in s.get("depends_on", []):
                indeg[k] -= 1
                if indeg[k] == 0:
                    ready.append(k)
        ready.sort()
    return out


def _cycles(steps: Dict[str, Any]) -> List[List[str]]:
    color = {k: 0 for k in steps}
    stack: List[str] = []
    found: List[List[str]] = []

    def dfs(n: str) -> None:
        color[n] = 1
        stack.append(n)
        for d in steps.get(n, {}).get("depends_on", []):
            if d not in steps:
                continue
            if color[d] == 1:
                found.append(stack[stack.index(d):] + [d])
            elif color[d] == 0:
                dfs(d)
        stack.pop()
        color[n] = 2

    for n in sorted(steps):
        if color[n] == 0:
            dfs(n)
    return found


def compile_spec(spec: Dict[str, Any], now: Optional[float] = None) -> Dict[str, Any]:
    now = time.time() if now is None else now
    errs: List[str] = []
    raw = spec.get("steps")
    if not isinstance(raw, list) or not raw:
        raise CompileError(["spec.steps 必须是非空数组"])
    allow = set(spec.get("allow_actions") or list(ACTIONS.keys()))
    bad_allow = allow - set(ACTIONS.keys())
    if bad_allow:
        errs.append("[未知动作] allow_actions 含未注册动作 %s" % sorted(bad_allow))

    ids: List[str] = []
    for i, s in enumerate(raw):
        if not isinstance(s, dict):
            errs.append("steps[%d] 不是对象" % i)
            continue
        sid = s.get("id")
        if not isinstance(sid, str) or not sid.strip():
            errs.append("steps[%d].id 缺失或非字符串" % i)
            continue
        if sid in ids:
            errs.append("[重复 id] %s" % sid)
        ids.append(sid)
    idset = set(ids)

    steps: Dict[str, Any] = {}
    for s in raw:
        if not isinstance(s, dict) or not isinstance(s.get("id"), str):
            continue
        sid = s["id"]
        action = s.get("action")
        params = s.get("params") or {}
        guard = s.get("guard", "true")
        deps = s.get("depends_on") or []
        risk = s.get("risk", "low")
        idem = s.get("idempotent")

        if action not in ACTIONS:
            errs.append("[未知动作] %s.action=%r 不在注册表" % (sid, action))
        elif action not in allow:
            errs.append("[权限拒绝] %s.action=%s 未被 allow_actions 授权" % (sid, action))
        if not isinstance(params, dict):
            errs.append("[参数非法] %s.params 必须是对象" % sid)
            params = {}
        if action in ACTIONS:
            for req in ACTIONS[action]:
                if req not in params:
                    errs.append("[参数缺失] %s.action=%s 缺 %r" % (sid, action, req))
        if action == "run_command" and "command" in params:
            cmd = params.get("command")
            if not isinstance(cmd, str) or not cmd.strip():
                errs.append("[参数非法] %s.command 必须是非空字符串" % sid)
            elif len(cmd) > 4000:
                errs.append("[参数非法] %s.command 过长" % sid)
        if action == "write_file" and isinstance(params.get("path"), str):
            if ".." in params["path"].replace("\\", "/"):
                errs.append("[参数非法] %s.path 含上级目录跳转" % sid)
        if not isinstance(guard, str) or not guard.strip():
            errs.append("[Guard 非法] %s.guard 必须是非空字符串" % sid)
        else:
            try:
                tokenize(guard)
                _Parser(tokenize(guard), {}).parse()
            except GuardError as e:
                errs.append("[Guard 语法] %s: %s" % (sid, e))
        if not isinstance(deps, list):
            errs.append("[依赖非法] %s.depends_on 必须是数组" % sid)
            deps = []
        for d in deps:
            if d not in idset:
                errs.append("[未知依赖] %s -> %s" % (sid, d))
            if d == sid:
                errs.append("[自环] %s" % sid)
        if risk not in RISKS:
            errs.append("[风险等级非法] %s.risk=%r" % (sid, risk))
        if not isinstance(idem, bool):
            errs.append("[幂等性未声明] %s.idempotent 必须显式 bool" % sid)

        steps[sid] = {
            "id": sid,
            "action": action,
            "params": params,
            "params_hash": sha(params),
            "guard": guard if isinstance(guard, str) else "false",
            "depends_on": [d for d in deps if d in idset],
            "risk": risk if risk in RISKS else "high",
            "idempotent": bool(idem),
            "semantic": bool(s.get("semantic", False)),
            "requires_confirmation": (risk == "high"),
            "ttl_seconds": int(s.get("ttl_seconds", spec.get("default_ttl_seconds", DEFAULT_TTL)) or 0),
            "max_attempts": int(s.get("max_attempts", 2) or 2),
            "gate": list(s.get("gate") or []),
            "state": "pending",
        }

    for c in _cycles(steps):
        errs.append("[循环依赖] " + " -> ".join(c))
    if errs:
        raise CompileError(errs)

    return {
        "schema": SCHEMA,
        "task": spec.get("task", "unnamed"),
        "goal": spec.get("goal", ""),
        "compiled_at": now,
        "compiled_at_iso": iso(now),
        "spec_hash": sha({"task": spec.get("task"), "steps": steps}),
        "allow_actions": sorted(allow),
        "steps": steps,
        "order": _topo(steps),
    }


# ---------------------------------------------------------------------- plan ---
def plan(edg: Dict[str, Any], facts: Dict[str, Any], now: Optional[float] = None) -> Dict[str, Any]:
    now = time.time() if now is None else now
    steps = edg["steps"]
    order = edg.get("order") or _topo(steps)
    out: Dict[str, Any] = {}
    for sid in order:
        st = steps[sid]
        rec: Dict[str, Any] = {"step": sid, "action": st["action"], "risk": st["risk"]}
        bad = [d for d in st["depends_on"]
               if out.get(d, {}).get("decision") not in ("reuse", "already_done")]
        if bad:
            rec.update(decision="blocked", reason="deps_not_satisfied", blocked_by=bad)
            out[sid] = rec
            continue
        ttl = st.get("ttl_seconds") or 0
        if ttl and (now - float(edg.get("compiled_at") or 0)) > ttl:
            rec.update(decision="needs_llm", reason="decision_expired")
            out[sid] = rec
            continue
        fh = facts.get("edg_hash")
        if fh and fh != edg.get("spec_hash"):
            rec.update(decision="needs_llm", reason="edg_drift")
            out[sid] = rec
            continue
        if st.get("semantic") or (set(_refs(st["guard"])) & SEMANTIC_FIELDS):
            rec.update(decision="needs_llm", reason="semantic_requires_rejudgement")
            out[sid] = rec
            continue
        resolved, val, detail = eval_guard(st["guard"], facts)
        rec["guard_detail"] = detail
        if not resolved:
            rec.update(decision="needs_llm", reason="guard_unresolved")
            out[sid] = rec
            continue
        if val is not True:
            rec.update(decision="needs_llm", reason="guard_false")
            out[sid] = rec
            continue
        if st["risk"] == "high" and not (facts.get("confirmations") or {}).get(sid):
            rec.update(decision="confirm_required", reason="high_risk_needs_confirmation")
            out[sid] = rec
            continue
        fstep = (facts.get("steps") or {}).get(sid) or {}
        if not st["idempotent"] and fstep.get("completed") is True:
            rec.update(decision="already_done", reason="non_idempotent_already_completed")
            out[sid] = rec
            continue
        rec.update(decision="reuse", reason="stored_decision_reused")
        out[sid] = rec

    counts: Dict[str, int] = {}
    for r in out.values():
        counts[r["decision"]] = counts.get(r["decision"], 0) + 1
    skipped = counts.get("reuse", 0) + counts.get("already_done", 0)
    return {
        "task": edg.get("task"),
        "edg_hash": edg.get("spec_hash"),
        "counts": counts,
        "model_callbacks_avoided": skipped,
        "model_callbacks_total": len(out),
        "steps": out,
    }


# ------------------------------------------------------------------ certify ---
def _certified_keys(ledger: str, task_id: str, edg_hash: Optional[str]) -> set:
    """已签发的 (task_id, edg_hash, step_id) 集合，用于证书幂等去重。"""
    keys: set = set()
    if not os.path.isfile(ledger):
        return keys
    with open(ledger, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                c = json.loads(line)
            except ValueError:
                continue
            if c.get("task_id") == task_id and c.get("edg_hash") == edg_hash:
                keys.add(str(c.get("step_id")))
    return keys


def certify(edg: Dict[str, Any], facts: Dict[str, Any], plan_out: Dict[str, Any],
            ledger: str, only: Optional[List[str]] = None,
            in_tok: int = DEFAULT_IN_TOK, out_tok: int = DEFAULT_OUT_TOK,
            allow_unverified: bool = False) -> Tuple[int, List[str]]:
    written, refused = 0, []
    task_id = facts.get("task_id") or edg.get("task") or "task_001"
    done = _certified_keys(ledger, task_id, edg.get("spec_hash"))
    for sid, rec in plan_out["steps"].items():
        if rec["decision"] not in ("reuse", "already_done"):
            continue
        if only and sid not in only:
            continue
        if sid in done:
            continue
        st = edg["steps"][sid]
        fstep = (facts.get("steps") or {}).get(sid) or {}
        evidence = fstep.get("evidence") or ""
        verified = bool(evidence)
        if not verified and not allow_unverified:
            refused.append(sid)
            continue
        cert = {
            "schema": CERT_SCHEMA,
            "task_id": task_id,
            "step_id": sid,
            "substitution": True,
            "decision": rec["decision"],
            "guard_result": (rec.get("guard_detail") or {}).get("result"),
            "guard_expr": st["guard"],
            "evidence": evidence or "(unverified)",
            "action": st["action"],
            "execution_status": "success" if fstep.get("completed", True) else "unknown",
            "timestamp": iso(),
            "reason": rec["reason"],
            "edg_hash": edg.get("spec_hash"),
            "tokens_saved_estimate": in_tok + out_tok,
            "token_estimate_basis": {"input": in_tok, "output": out_tok,
                                     "note": "估算值，非实测计数"},
            "verified": verified,
        }
        d = os.path.dirname(os.path.abspath(ledger)) or "."
        os.makedirs(d, exist_ok=True)
        with open(ledger, "a", encoding="utf-8") as f:
            f.write(json.dumps(cert, ensure_ascii=False) + "\n")
        written += 1
    return written, refused


# --------------------------------------------------------------------- stats ---
def stats(ledger: str) -> Dict[str, Any]:
    if not os.path.isfile(ledger):
        return {"error": "ledger 不存在: %s" % ledger}
    total = saved = verified = 0
    by_reason: Dict[str, int] = {}
    by_task: Dict[str, int] = {}
    with open(ledger, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                c = json.loads(line)
            except ValueError:
                continue
            total += 1
            saved += int(c.get("tokens_saved_estimate") or 0)
            verified += 1 if c.get("verified") else 0
            r = str(c.get("reason") or "?")
            by_reason[r] = by_reason.get(r, 0) + 1
            t = str(c.get("task_id") or "?")
            by_task[t] = by_task.get(t, 0) + 1
    return {
        "certificates": total,
        "verified": verified,
        "verified_ratio": round(verified / total, 4) if total else 0.0,
        "tokens_saved_estimate": saved,
        "by_reason": by_reason,
        "by_task": by_task,
        "note": "tokens 为估算口径（证书内 token_estimate_basis），不可当实测值对外引用",
    }


# ----------------------------------------------------------------------- run ---
def run_steps(edg: Dict[str, Any], facts: Dict[str, Any], plan_out: Dict[str, Any],
              apply: bool, timeout: int = 60) -> Dict[str, Any]:
    results: Dict[str, Any] = {}
    for sid, rec in plan_out["steps"].items():
        if rec["decision"] != "reuse":
            continue
        st = edg["steps"][sid]
        act, params = st["action"], st["params"]
        if act == "noop":
            results[sid] = {"completed": True, "evidence": "noop"}
        elif act == "read_file":
            p = str(params.get("path"))
            results[sid] = ({"completed": True, "evidence": "read:%s" % p}
                            if os.path.isfile(p) else
                            {"completed": False, "evidence": "missing:%s" % p})
        elif act == "write_file":
            p = str(params.get("path"))
            if not apply:
                results[sid] = {"completed": False, "evidence": "dry_run:write:%s" % p}
            else:
                try:
                    os.makedirs(os.path.dirname(os.path.abspath(p)) or ".", exist_ok=True)
                    with open(p, "w", encoding="utf-8") as f:
                        f.write(str(params.get("content", "")))
                    results[sid] = {"completed": True, "evidence": "wrote:%s" % p}
                except OSError as e:
                    results[sid] = {"completed": False, "evidence": "write_error:%s" % e}
        elif act == "analyze_results":
            results[sid] = {"completed": False, "evidence": "skipped:needs_host_analysis"}
        elif act == "run_command":
            cmd = str(params.get("command", "")).strip()
            if st["risk"] != "low" or not st["idempotent"]:
                results[sid] = {"completed": False, "evidence": "skipped:risk_or_idempotency"}
            elif not any(cmd.startswith(p) for p in CMD_ALLOWLIST):
                results[sid] = {"completed": False, "evidence": "skipped:not_allowlisted"}
            elif not apply:
                results[sid] = {"completed": False, "evidence": "dry_run:%s" % cmd}
            else:
                try:
                    p = subprocess.run(cmd, shell=True, capture_output=True,
                                       text=True, timeout=timeout)
                    out = (p.stdout or p.stderr or "").strip()[:400]
                    results[sid] = {"completed": p.returncode == 0,
                                    "exit_code": p.returncode, "evidence": out}
                except (OSError, subprocess.TimeoutExpired) as e:
                    results[sid] = {"completed": False, "evidence": "exec_error:%s" % e}
        else:
            results[sid] = {"completed": False, "evidence": "skipped:unknown_action"}
    merged = dict((facts.get("steps") or {}))
    merged.update(results)
    new_facts = dict(facts)
    new_facts["steps"] = merged
    return new_facts


# ------------------------------------------------------------------ selftest ---
def _base_spec(steps: List[Dict[str, Any]], task: str = "selftest") -> Dict[str, Any]:
    return {"task": task, "goal": "selftest", "steps": steps}


def selftest() -> int:
    rows: List[Tuple[str, bool, str]] = []

    def case(name: str, cond: bool, detail: str) -> None:
        rows.append((name, bool(cond), detail))

    # S1 确定性顺序链：全部可复用
    spec1 = _base_spec([
        {"id": "compile", "action": "run_command", "params": {"command": "python -m compileall ."},
         "guard": "true", "idempotent": True, "risk": "low"},
        {"id": "test", "action": "run_command", "params": {"command": "pytest -q"},
         "guard": "compile.exit_code == 0", "depends_on": ["compile"],
         "idempotent": True, "risk": "low"},
        {"id": "analyze", "action": "analyze_results", "params": {},
         "guard": "test.completed == true", "depends_on": ["test"],
         "idempotent": True, "risk": "low"},
    ])
    edg1 = compile_spec(spec1, now=time.time())
    f1 = {"task_id": "t1", "steps": {"compile": {"exit_code": 0, "completed": True, "evidence": "exit=0"},
                                      "test": {"completed": True, "evidence": "pytest ok"}}}
    p1 = plan(edg1, f1)
    case("S1 确定性链全部复用",
         p1["counts"] == {"reuse": 3} and p1["model_callbacks_avoided"] == 3,
         json.dumps(p1["counts"], ensure_ascii=False))

    # S2 条件分支：一条复用一条重新判断
    spec2 = _base_spec([
        {"id": "build", "action": "run_command", "params": {"command": "python build.py"},
         "guard": "true", "idempotent": True, "risk": "low"},
        {"id": "deploy", "action": "run_command", "params": {"command": "python deploy.py"},
         "guard": "build.exit_code == 0", "depends_on": ["build"],
         "idempotent": True, "risk": "medium"},
        {"id": "notify", "action": "noop", "params": {},
         "guard": "build.exit_code == 1", "depends_on": ["build"],
         "idempotent": True, "risk": "low"},
    ])
    edg2 = compile_spec(spec2)
    p2 = plan(edg2, {"steps": {"build": {"exit_code": 0, "completed": True, "evidence": "exit=0"}}})
    case("S2 条件分支：deploy 复用 / notify 重判",
         p2["steps"]["deploy"]["decision"] == "reuse"
         and p2["steps"]["notify"]["decision"] == "needs_llm"
         and p2["steps"]["notify"]["reason"] == "guard_false",
         "deploy=%s notify=%s" % (p2["steps"]["deploy"]["decision"], p2["steps"]["notify"]["reason"]))

    # S3 工具异常：Guard 不满足 -> 下游阻塞，零证书
    p3 = plan(edg1, {"steps": {"compile": {"exit_code": 1, "completed": False,
                                            "evidence": "exit=1"}}})
    case("S3 工具异常下游阻塞",
         p3["steps"]["compile"]["decision"] == "reuse"
         and p3["steps"]["test"]["decision"] == "needs_llm"
         and p3["steps"]["analyze"]["decision"] == "blocked",
         "compile=%s test=%s analyze=%s" % (p3["steps"]["compile"]["decision"],
                                            p3["steps"]["test"]["decision"],
                                            p3["steps"]["analyze"]["decision"]))

    # S4 语义任务必须重新推理（标记 semantic 与引用语义字段两种）
    spec4 = _base_spec([
        {"id": "review", "action": "analyze_results", "params": {},
         "guard": "true", "idempotent": True, "risk": "low", "semantic": True},
        {"id": "judge", "action": "analyze_results", "params": {},
         "guard": "review.quality > 0.8", "depends_on": ["review"],
         "idempotent": True, "risk": "low"},
    ])
    edg4 = compile_spec(spec4)
    p4 = plan(edg4, {"steps": {"review": {"completed": True, "evidence": "x"}}})
    case("S4 语义任务强制重判",
         p4["steps"]["review"]["reason"] == "semantic_requires_rejudgement"
         and p4["steps"]["judge"]["decision"] == "blocked"
         and p4["steps"]["judge"]["reason"] == "deps_not_satisfied",
         "review=%s judge=%s" % (p4["steps"]["review"]["reason"], p4["steps"]["judge"]["reason"]))

    # S5 高风险：无确认 -> confirm_required；有确认 -> reuse
    spec5 = _base_spec([
        {"id": "purge", "action": "run_command", "params": {"command": "python purge.py"},
         "guard": "true", "idempotent": True, "risk": "high"},
    ])
    edg5 = compile_spec(spec5)
    p5a = plan(edg5, {"steps": {}})
    p5b = plan(edg5, {"confirmations": {"purge": True}, "steps": {}})
    case("S5 高风险需确认",
         p5a["steps"]["purge"]["decision"] == "confirm_required"
         and p5b["steps"]["purge"]["decision"] == "reuse",
         "no_conf=%s with_conf=%s" % (p5a["steps"]["purge"]["decision"],
                                      p5b["steps"]["purge"]["decision"]))

    # S6 编译期拦截：循环依赖 / 未注册动作 / 缺参数 / 幂等性未声明
    bad = [
        {"id": "a", "action": "noop", "params": {}, "guard": "true",
         "depends_on": ["b"], "idempotent": True},
        {"id": "b", "action": "noop", "params": {}, "guard": "true",
         "depends_on": ["a"], "idempotent": True},
        {"id": "c", "action": "rm_rf", "params": {}, "guard": "true", "idempotent": True},
        {"id": "d", "action": "run_command", "params": {}, "guard": "true"},
    ]
    try:
        compile_spec(_base_spec(bad))
        case("S6 编译期拦截非法图", False, "未抛错")
    except CompileError as e:
        joined = " | ".join(e.errors)
        case("S6 编译期拦截非法图",
             ("循环依赖" in joined and "未知动作" in joined
              and "参数缺失" in joined and "幂等性未声明" in joined),
             "%d 项错误" % len(e.errors))

    # S7 证书门禁 + 统计 + 保守执行器
    tmp = tempfile.mkdtemp(prefix="ei_selftest_")
    ledger = os.path.join(tmp, "certs.jsonl")
    edg7 = compile_spec(_base_spec([
        {"id": "e1", "action": "noop", "params": {}, "guard": "true",
         "idempotent": True, "risk": "low"},
        {"id": "e2", "action": "noop", "params": {}, "guard": "true",
         "depends_on": ["e1"], "idempotent": True, "risk": "low"},
    ]))
    facts7 = {"task_id": "t7", "steps": {"e1": {"completed": True, "evidence": "noop"}}}
    p7 = plan(edg7, facts7)
    w, refused = certify(edg7, facts7, p7, ledger)
    st = stats(ledger)
    facts7b = run_steps(edg7, facts7, p7, apply=False)
    w2, refused2 = certify(edg7, facts7b, plan(edg7, facts7b), ledger)
    case("S7 证书门禁（无证据拒发）",
         w == 1 and refused == ["e2"], "written=%d refused=%s" % (w, refused))
    case("S7 执行后补发 + 统计",
         w2 == 1 and stats(ledger)["certificates"] == 2 and st["verified_ratio"] == 1.0,
         "total=%d" % stats(ledger)["certificates"])

    print("== execution_intelligence selftest ==")
    ok = True
    for name, passed, detail in rows:
        print("  %s  %-32s %s" % ("PASS" if passed else "FAIL", name, detail))
        ok = ok and passed
    print("-- %d/%d passed --" % (sum(1 for _, p, _ in rows if p), len(rows)))
    return 0 if ok else 1


# ---------------------------------------------------------------------- main ---
def _print(obj: Any) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    ap = argparse.ArgumentParser(prog="execution_intelligence",
                                 description="EDG / GDR / CCS 执行智能调度（P0）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("compile")
    p.add_argument("spec")
    p.add_argument("out")

    p = sub.add_parser("guard")
    p.add_argument("edg")
    p.add_argument("facts")
    p.add_argument("step_id")

    p = sub.add_parser("plan")
    p.add_argument("edg")
    p.add_argument("facts")

    p = sub.add_parser("certify")
    p.add_argument("edg")
    p.add_argument("facts")
    p.add_argument("--ledger", required=True)
    p.add_argument("--step", action="append", default=None)
    p.add_argument("--in-tokens", type=int, default=DEFAULT_IN_TOK)
    p.add_argument("--out-tokens", type=int, default=DEFAULT_OUT_TOK)
    p.add_argument("--allow-unverified", action="store_true")

    p = sub.add_parser("run")
    p.add_argument("edg")
    p.add_argument("facts")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--write-facts", default=None)
    p.add_argument("--timeout", type=int, default=60)

    p = sub.add_parser("stats")
    p.add_argument("ledger")

    sub.add_parser("selftest")
    sub.add_parser("schema")

    args = ap.parse_args()

    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "schema":
        _print({
            "spec": {"task": "str", "goal": "str", "allow_actions": ["可选，默认全部注册动作"],
                     "default_ttl_seconds": DEFAULT_TTL,
                     "steps": [{"id": "str(唯一)", "action": sorted(ACTIONS.keys()),
                                "params": {k: v for k, v in ACTIONS.items()},
                                "guard": "布尔表达式，如 compile.exit_code == 0",
                                "depends_on": ["id"], "risk": list(RISKS),
                                "idempotent": "必填 bool", "semantic": "可选 bool",
                                "ttl_seconds": "可选 int", "max_attempts": 2, "gate": ["str"]}]},
            "facts": {"task_id": "str", "edg_hash": "可选，校验图版本",
                      "confirmations": {"step_id": True},
                      "steps": {"step_id": {"completed": True, "exit_code": 0,
                                            "evidence": "真实执行证据（签发证书必需）"}}},
            "guard_language": "== != > < >= <= and or not ( ) 数字/字符串/true/false/null/step.field",
            "honest_boundary": ["不代宿主跳过模型回调", "tokens 为估算", "未实现 RSI"],
        })
        return 0

    try:
        if args.cmd == "compile":
            edg = compile_spec(load_json(args.spec))
            atomic_write_json(args.out, edg)
            _print({"ok": True, "out": args.out, "task": edg["task"],
                    "steps": len(edg["steps"]), "order": edg["order"],
                    "spec_hash": edg["spec_hash"]})
            return 0
        if args.cmd == "guard":
            edg = load_json(args.edg)
            facts = load_json(args.facts)
            st = edg["steps"].get(args.step_id)
            if st is None:
                _print({"ok": False, "error": "未知步骤 %s" % args.step_id})
                return 2
            resolved, val, detail = eval_guard(st["guard"], facts)
            _print({"ok": resolved, "value": val if resolved else None, "detail": detail})
            return 0 if resolved else 1
        if args.cmd == "plan":
            _print(plan(load_json(args.edg), load_json(args.facts)))
            return 0
        if args.cmd == "certify":
            edg = load_json(args.edg)
            facts = load_json(args.facts)
            pl = plan(edg, facts)
            written, refused = certify(edg, facts, pl, args.ledger, args.step,
                                       args.in_tokens, args.out_tokens, args.allow_unverified)
            _print({"ok": True, "written": written, "refused_no_evidence": refused,
                    "ledger": args.ledger})
            return 0
        if args.cmd == "run":
            edg = load_json(args.edg)
            facts = load_json(args.facts)
            pl = plan(edg, facts)
            new_facts = run_steps(edg, facts, pl, args.apply, args.timeout)
            if args.write_facts:
                atomic_write_json(args.write_facts, new_facts)
            _print({"ok": True, "apply": args.apply,
                    "executed": [k for k, v in (new_facts["steps"] or {}).items()
                                 if v.get("completed")],
                    "facts": new_facts["steps"]})
            return 0
        if args.cmd == "stats":
            _print(stats(args.ledger))
            return 0
    except CompileError as e:
        _print({"ok": False, "stage": "compile", "errors": e.errors})
        return 2
    except (OSError, ValueError) as e:
        _print({"ok": False, "error": str(e)})
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
