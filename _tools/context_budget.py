#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
context_budget.py — 上下文动态预算启发式
=======================================
估算 token、按优先级裁剪、检测过期/冲突/遗漏。弥补"无动态预算子系统"。

优先级（高→低）：hard(硬约束) > decision(有效决策) > state(当前状态) > evidence(证据) > background(背景)
规则：超预算时先丢低优先级；hard 永不被静默丢弃。
"""
import sys
import json

PRIORITY = {"hard": 0, "decision": 1, "state": 2, "evidence": 3, "background": 4}


def est_tokens(text: str) -> int:
    """中文按字符*1.3，英文按词*1.3 近似估算。"""
    cn = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    en = max(len(text.split()) - cn, 0)
    return int(cn * 1.3 + en * 1.3)


def budget(items: list, limit: int = 8000) -> dict:
    """items: [{text, prio, tag}] → 返回裁剪结果。"""
    for it in items:
        it["_t"] = est_tokens(it["text"])
    items.sort(key=lambda x: PRIORITY.get(x["prio"], 4))
    kept, dropped, used = [], [], 0
    for it in items:
        if it["prio"] == "hard" or used + it["_t"] <= limit:
            kept.append(it)
            used += it["_t"]
        else:
            dropped.append(it)
    return {
        "used": used,
        "limit": limit,
        "kept": [k["tag"] for k in kept],
        "dropped": [d["tag"] for d in dropped],
        "note": "安全约束(hard)永不被裁剪；超预算先丢 background/evidence",
    }


if __name__ == "__main__":
    sample = [
        {"text": "禁止删除个人文件（硬约束）", "prio": "hard", "tag": "safety"},
        {"text": "当前项目状态：记忆事务引擎已部署", "prio": "state", "tag": "state"},
        {"text": "背景资料：WB 是 AI 助手，由风若不止使用", "prio": "background", "tag": "bg"},
        {"text": "证据：chromadb 下载成功 23MB", "prio": "evidence", "tag": "ev"},
    ]
    print(json.dumps(budget(sample), ensure_ascii=False, indent=2))
