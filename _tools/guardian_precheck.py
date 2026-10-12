#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
guardian_precheck.py — 运行时安全前置检查
========================================
工具调用前权限/风险/范围检查；高风险操作授权门；不可信输入标记。
替代原"明确不建"的 Guardian：以规则+precheck 形态落地（非进程级拦截，诚实标注）。

检查项：
  1. 路径是否命中 No-Go 区（个人/系统目录，rules/01 护栏）
  2. 操作是否命中 L2 高风险清单（需显式确认，rules/01 §0.11）
  3. 不可信输入标记（外部/未验证内容）
"""
import sys
import json

NOGO = ["Desktop", "Downloads", "Documents", "AppData", "Windows",
        "ProgramData", "/", "C:\\", "D:\\OneDrive"]
L2 = ["删除", "批量", "系统", "支付", "发消息", "格式化", "重置", "覆盖",
      "强制推送", "私钥", "凭据", "对外"]


def check(op: str, path: str = None, confirmed: bool = False,
          untrusted: bool = False) -> dict:
    risk = [k for k in L2 if k in op]
    if path and any(g.lower() in path.lower() for g in NOGO):
        return {"decision": "deny",
                "reason": f"路径命中 No-Go 区 {path}（个人/系统目录，rules/01 护栏）"}
    if risk:
        if not confirmed:
            return {"decision": "confirm_required", "risk": risk,
                    "reason": "命中 L2 高风险操作，需显式确认（rules/01 §0.11）"}
        return {"decision": "allow", "risk": risk, "note": "已确认，执行"}
    if untrusted:
        return {"decision": "allow_with_caution", "note": "不可信输入，执行中需安检"}
    return {"decision": "allow", "note": "低风险"}


if __name__ == "__main__":
    op = sys.argv[1] if len(sys.argv) > 1 else "读取项目文件"
    p = sys.argv[2] if len(sys.argv) > 2 else ""
    c = sys.argv[3] == "1" if len(sys.argv) > 3 else False
    u = sys.argv[4] == "1" if len(sys.argv) > 4 else False
    print(json.dumps(check(op, p, c, u), ensure_ascii=False, indent=2))
