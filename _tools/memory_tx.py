#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memory_tx.py — 记忆事务 / 版本 / 回滚引擎
=========================================
填补 rules/07 §十「任务级记忆执行纪律」的工程缺口：
  - 原体系只有 Markdown 文件 + 纪律文字，无事务 / 版本 / 回滚 / 同步状态。
  - 本工具提供真实可运行的原子写、版本快照、回滚、跨副本同步状态标记。

设计原则（不重复建设）：
  - 纯标准库，零外部依赖，放在 skills 仓 _tools/ 复用。
  - 版本目录 <file>.versions/ 与源文件同目录，不污染其他路径。
  - 原子写用「临时文件 + os.replace」，进程中断也不会写出半截文件。
  - 回滚前自动快照当前版，绝不丢失有效业务状态。

用法：
  python memory_tx.py write   <path> <content> [--actor X] [--note Y]
  python memory_tx.py list    <path>
  python memory_tx.py rollback <path> [--vid V]
  python memory_tx.py sync    <path> <replica> <status>
"""
import os
import sys
import json
import shutil
import datetime
import argparse

VERSIONS_SUFFIX = ".versions"
SYNC_FILE = ".sync_status.json"


def _versions_dir(path: str) -> str:
    return path + VERSIONS_SUFFIX


def _snapshot(path: str, actor: str, note: str) -> str:
    """把当前文件快照进版本目录，返回 version_id。"""
    vd = _versions_dir(path)
    os.makedirs(vd, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    with open(path, "rb") as f:
        h = hashlib_sha256(f.read())
    vid = f"{ts}_{h[:10]}"
    shutil.copy2(path, os.path.join(vd, vid + ".bak"))
    idx = os.path.join(vd, "index.json")
    arr = json.load(open(idx, encoding="utf-8")) if os.path.exists(idx) else []
    arr.append({"version_id": vid, "time": ts, "hash": h[:10], "actor": actor, "note": note})
    json.dump(arr, open(idx, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return vid


def hashlib_sha256(b: bytes) -> str:
    import hashlib
    return hashlib.sha256(b).hexdigest()


def atomic_write(path: str, content: str, make_version: bool = True,
                 actor: str = "agent", note: str = "") -> dict:
    """原子写：先落临时文件再 os.replace；可选保留旧版。
    返回: {version_id|None, status, path}"""
    d = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(d, exist_ok=True)
    version_id = None
    if make_version and os.path.exists(path):
        version_id = _snapshot(path, actor, note)
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
    _snapshot(path, "rollback", f"rollback-to-{version_id}")  # 先保当前有效版
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


def main():
    ap = argparse.ArgumentParser(description="记忆事务/版本/回滚引擎")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("write"); p.add_argument("path"); p.add_argument("content")
    p.add_argument("--actor", default="agent"); p.add_argument("--note", default="")
    p = sub.add_parser("list"); p.add_argument("path")
    p = sub.add_parser("rollback"); p.add_argument("path"); p.add_argument("--vid", default=None)
    p = sub.add_parser("sync"); p.add_argument("path"); p.add_argument("replica"); p.add_argument("status")
    args = ap.parse_args()

    if args.cmd == "write":
        print(json.dumps(atomic_write(args.path, args.content, actor=args.actor, note=args.note), ensure_ascii=False))
    elif args.cmd == "list":
        print(json.dumps(list_versions(args.path), ensure_ascii=False, indent=2))
    elif args.cmd == "rollback":
        print(json.dumps(rollback(args.path, args.vid), ensure_ascii=False))
    elif args.cmd == "sync":
        print(json.dumps(mark_sync(args.path, args.replica, args.status), ensure_ascii=False))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
