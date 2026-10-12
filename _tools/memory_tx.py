#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memory_tx.py — 记忆事务 / 版本 / 生命周期 / 删除传播引擎
=====================================================
填补 rules/07 §十 工程缺口，并落地 M1-M22 终版中真正缺失的微观项：

  - M7 / M8 / M15 : 原子写 / 版本快照 / 回滚 / 同步状态（基础能力）
  - M17 来源追溯  : version index 记录 source_type（user/tool/外部/推断）+ verified 状态
  - M16 生命周期  : lifecycle 状态机（candidate/verified/active/deprecated/archived/revoked）
  - M22 删除传播  : 删除主记录 + 级联标记派生/索引/副本传播状态，诚实标注外部副本不可验证
  - M13 依赖关系  : 轻量记录记忆/规则/Skill 间依赖

不重复建设：纯标准库、零依赖、与 agent-guild / personal-ai-os 协同，不新造平行架构。

用法：
  python memory_tx.py write   <path> <content> [--actor X] [--note Y]
                            [--source-type user|tool|external|inferred] [--verified]
  python memory_tx.py list    <path>
  python memory_tx.py rollback <path> [--vid V]
  python memory_tx.py sync    <path> <replica> <status>
  python memory_tx.py status  <path> [--set STATE] [--reason R]
  python memory_tx.py delete  <path> --actor X --reason R [--cascade id1,id2]
  python memory_tx.py dep     <path> add <target> | list
"""
import os
import sys
import json
import shutil
import datetime
import argparse

VERSIONS_SUFFIX = ".versions"
SYNC_FILE = ".sync_status.json"
LIFECYCLE_FILE = "lifecycle.json"
DEPS_FILE = "deps.json"
DELETED_DIR = ".deleted"
LIFECYCLE_STATES = ["candidate", "verified", "active", "deprecated", "archived", "revoked"]


def _versions_dir(path: str) -> str:
    return path + VERSIONS_SUFFIX


def _hash(b: bytes) -> str:
    import hashlib
    return hashlib.sha256(b).hexdigest()


def _snapshot(path: str, actor: str, note: str, source_type="unknown", verified=False) -> str:
    """把当前文件快照进版本目录，返回 version_id。"""
    vd = _versions_dir(path)
    os.makedirs(vd, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    with open(path, "rb") as f:
        h = _hash(f.read())
    vid = f"{ts}_{h[:10]}"
    shutil.copy2(path, os.path.join(vd, vid + ".bak"))
    idx = os.path.join(vd, "index.json")
    arr = json.load(open(idx, encoding="utf-8")) if os.path.exists(idx) else []
    arr.append({
        "version_id": vid, "time": ts, "hash": h[:10], "actor": actor,
        "note": note, "source_type": source_type, "verified": bool(verified),
    })
    json.dump(arr, open(idx, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return vid


def atomic_write(path: str, content: str, make_version: bool = True,
                 actor: str = "agent", note: str = "",
                 source_type: str = "unknown", verified: bool = False) -> dict:
    """原子写：先落临时文件再 os.replace；可选保留旧版。
    返回: {version_id|None, status, path}"""
    d = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(d, exist_ok=True)
    version_id = None
    if make_version and os.path.exists(path):
        version_id = _snapshot(path, actor, note, source_type, verified)
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)  # 原子替换，中断也安全
    return {"version_id": version_id, "status": "ok", "path": path}


def list_versions(path: str) -> list:
    idx = os.path.join(_versions_dir(path), "index.json")
    if not os.path.exists(idx):
        return []
    return json.load(open(idx, encoding="utf-8"))


def rollback(path: str, version_id: str = None) -> dict:
    """回滚到指定版本（默认最近一版）；回滚前先快照当前有效版。"""
    if not os.path.exists(path):
        return {"status": "no_target"}
    vd = _versions_dir(path)
    if version_id is None:
        vs = list_versions(path)
        if not vs:
            return {"status": "no_versions"}
        version_id = vs[-1]["version_id"]
    src = os.path.join(vd, version_id + ".bak")
    if not os.path.exists(src):
        return {"status": "not_found", "version_id": version_id}
    # 回滚只恢复有效业务状态，不恢复已撤销授权/已删除个人信息/已废安全规则
    lc = _load_lifecycle(path)
    if lc.get("state") == "revoked":
        return {"status": "blocked_revoked", "version_id": version_id,
                "reason": "目标生命周期已 revoked，禁止无条件回滚复活"}
    _snapshot(path, "rollback", f"rollback-to-{version_id}")
    shutil.copy2(src, path)
    return {"status": "ok", "rolled_to": version_id}


def mark_sync(path: str, replica: str, status: str) -> dict:
    """标记某副本同步状态。可控副本标 ok/pending；外部副本标 unreachable。
    绝不承诺无法验证的彻底清除。"""
    sf = os.path.join(_versions_dir(path), SYNC_FILE)
    data = json.load(open(sf, encoding="utf-8")) if os.path.exists(sf) else {}
    data[replica] = {"status": status, "time": datetime.datetime.now().isoformat()}
    json.dump(data, open(sf, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return data


# ---------- M16 生命周期状态机 ----------
def _load_lifecycle(path: str) -> dict:
    f = os.path.join(_versions_dir(path), LIFECYCLE_FILE)
    if os.path.exists(f):
        return json.load(open(f, encoding="utf-8"))
    return {"state": "active", "history": []}


def _save_lifecycle(path: str, state: str, reason: str, actor: str) -> dict:
    vd = _versions_dir(path)
    os.makedirs(vd, exist_ok=True)
    lc = _load_lifecycle(path)
    lc["history"].append({
        "from": lc.get("state"), "to": state,
        "time": datetime.datetime.now().isoformat(), "reason": reason, "actor": actor,
    })
    lc["state"] = state
    json.dump(lc, open(os.path.join(vd, LIFECYCLE_FILE), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return lc


def set_status(path: str, state: str, reason: str = "", actor: str = "agent") -> dict:
    if state not in LIFECYCLE_STATES:
        return {"status": "bad_state", "allowed": LIFECYCLE_STATES}
    # 状态迁移合法性：revoked 不可被普通回滚复活（由 rollback 拦截），需显式 set active
    return {"status": "ok", "lifecycle": _save_lifecycle(path, state, reason, actor)}


# ---------- M22 删除传播 ----------
def delete_with_propagation(path: str, actor: str, reason: str,
                            cascade: list = None) -> dict:
    """删除主记录 + 级联标记传播状态。
    - 主记录软删除（移入 .deleted/ 可恢复），lifecycle=revoked
    - cascade: 显式声明的派生/索引/副本 id 列表，逐一标记删除传播状态
    - 外部不可控副本必须诚实标注 unreachable，不得宣称全链路清除"""
    vd = _versions_dir(path)
    os.makedirs(os.path.join(vd, DELETED_DIR), exist_ok=True)
    # 先快照再移走，保留可恢复证据
    if os.path.exists(path):
        _snapshot(path, actor, f"delete:{reason}", verified=False)
        dest = os.path.join(vd, DELETED_DIR, os.path.basename(path) + "." +
                            datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        shutil.move(path, dest)
    _save_lifecycle(path, "revoked", f"delete:{reason}", actor)
    prop = {"primary": "revoked_soft_deleted", "cascade": {}}
    for cid in (cascade or []):
        prop["cascade"][cid] = "marked_revoked_pending_sync"
    prop["external_replicas"] = "unreachable_unverified"
    json.dump(prop, open(os.path.join(vd, ".delete_propagation.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return {"status": "ok", "propagation": prop}


# ---------- M13 依赖关系（轻量） ----------
def _dep_path(path: str) -> str:
    return os.path.join(_versions_dir(path), DEPS_FILE)


def dep_add(path: str, target: str) -> dict:
    f = _dep_path(path)
    arr = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else []
    if target not in arr:
        arr.append(target)
    json.dump(arr, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return {"deps": arr}


def dep_list(path: str) -> list:
    f = _dep_path(path)
    return json.load(open(f, encoding="utf-8")) if os.path.exists(f) else []


def main():
    ap = argparse.ArgumentParser(description="记忆事务/版本/生命周期/删除传播引擎")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("write"); p.add_argument("path"); p.add_argument("content")
    p.add_argument("--actor", default="agent"); p.add_argument("--note", default="")
    p.add_argument("--source-type", default="unknown")
    p.add_argument("--verified", action="store_true")
    p = sub.add_parser("list"); p.add_argument("path")
    p = sub.add_parser("rollback"); p.add_argument("path"); p.add_argument("--vid", default=None)
    p = sub.add_parser("sync"); p.add_argument("path"); p.add_argument("replica"); p.add_argument("status")
    p = sub.add_parser("status"); p.add_argument("path")
    p.add_argument("--set", default=None); p.add_argument("--reason", default="")
    p = sub.add_parser("delete"); p.add_argument("path")
    p.add_argument("--actor", default="agent"); p.add_argument("--reason", default="")
    p.add_argument("--cascade", default="")
    p = sub.add_parser("dep"); p.add_argument("path"); p.add_argument("op"); p.add_argument("target", nargs="?")
    args = ap.parse_args()

    if args.cmd == "write":
        print(json.dumps(atomic_write(args.path, args.content, actor=args.actor,
              note=args.note, source_type=args.source_type, verified=args.verified), ensure_ascii=False))
    elif args.cmd == "list":
        print(json.dumps(list_versions(args.path), ensure_ascii=False, indent=2))
    elif args.cmd == "rollback":
        print(json.dumps(rollback(args.path, args.vid), ensure_ascii=False))
    elif args.cmd == "sync":
        print(json.dumps(mark_sync(args.path, args.replica, args.status), ensure_ascii=False))
    elif args.cmd == "status":
        if args.set:
            print(json.dumps(set_status(args.path, args.set, args.reason), ensure_ascii=False))
        else:
            print(json.dumps(_load_lifecycle(args.path), ensure_ascii=False, indent=2))
    elif args.cmd == "delete":
        cascade = [x for x in args.cascade.split(",") if x]
        print(json.dumps(delete_with_propagation(args.path, args.actor, args.reason, cascade), ensure_ascii=False))
    elif args.cmd == "dep":
        if args.op == "add" and args.target:
            print(json.dumps(dep_add(args.path, args.target), ensure_ascii=False))
        else:
            print(json.dumps(dep_list(args.path), ensure_ascii=False))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
