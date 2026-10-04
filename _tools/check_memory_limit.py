#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEMORY.md 4000 字硬上限 · 实时卡点工具
========================================
用途（配合 rules/07 §八「写入即校验」）：
  - A 写入即校验：agent 改完 MEMORY.md 后跑一次，超限立即处理。
  - B 兜底：自动化定时跑 `--fix`，修掉豆包/Qoder 等外部写入造成的溢出。

【安全铁律 · 不伤 agent 性能】
  只做「无损压缩」：删的是行内已声明"细节在单源文件"的冗余内联副本
  （rules/0X / AGENTS.md § / 00_*.md）。agent 本来就会重读那些单源文件，删了零损失。
  绝不删独立纪律/指针条目（那些是 agent 行为本身）。
  无损压缩后仍 >4000 → 退出码 2，列出候选独立长行交人工裁决，绝不猜删。

字符计数与 `wc -m` 对齐：len(open(path).read()) 含换行，同 wc -m。
"""
import sys, re, os

DEFAULT = r"C:\Users\26719\.workbuddy\user-4a04b9c5-3426-4ded-bbf7-39090973ec66-personal\MEMORY.md"
LIMIT = 4000

# 单源指针短语：行内出现即表示"此后/此前细节在别处"，内联副本可无损删
SRC_REF = re.compile(r"(全见 rules/|见 rules/|详见 AGENTS|见 AGENTS|见 `AGENTS)")

def count_chars(path):
    with open(path, encoding="utf-8") as f:
        return len(f.read())

def compress_line(line):
    """返回压缩后的行（无损）；不可压或无需压返回 None。"""
    m = SRC_REF.search(line)
    if not m:
        return None  # 无单源引用 -> 不碰（可能是独立纪律）
    stripped = line.rstrip("\n")
    if len(stripped) <= 50:
        return None  # 已够短 -> 不动
    # 取引用前的主题首节（第一个 "、" 之前），丢掉冗余 specifics
    prefix = stripped[: m.start()].lstrip("- ").strip()
    topic = prefix.split("、")[0].strip() if prefix else ""
    ref = m.group(0).rstrip("`")
    new = f"- {topic}：**见 {ref}**（单源）。\n" if topic else f"- **见 {ref}**（单源）。\n"
    return new if new != line else None

def fix(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    out, changed = [], 0
    for ln in lines:
        c = compress_line(ln)
        if c is not None:
            out.append(c); changed += 1
        else:
            out.append(ln)
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(out)
    return changed

def main():
    args = sys.argv[1:]
    path = DEFAULT
    do_fix = False
    for a in args:
        if a == "--fix":
            do_fix = True
        elif not a.startswith("--"):
            path = a
    if not os.path.isfile(path):
        print(f"文件不存在: {path}"); return 3
    n = count_chars(path)
    print(f"MEMORY.md 字符数: {n} / 上限 {LIMIT}")
    if n <= LIMIT:
        print("OK · 未超限，无需处理")
        return 0
    print(f"超限 {n - LIMIT} 字")
    if not do_fix:
        print("（仅检查；请按 rules/07 §八 无损压缩或删等量旧内容压回）")
        return 1
    ch = fix(path)
    n2 = count_chars(path)
    print(f"--fix 无损压缩 {ch} 行 -> 现 {n2} 字（仅删 rules/XX/AGENTS.md§ 的冗余内联副本）")
    if n2 <= LIMIT:
        print("OK · 已压回上限内，独立纪律/指针条目未动")
        return 0
    print(f"仍超限 {n2 - LIMIT} 字：剩余均为独立纪律/指针条目，禁止自动删 -> 需人工裁决")
    for i, ln in enumerate(open(path, encoding="utf-8"), 1):
        s = ln.rstrip("\n")
        if len(s) > 40 and not SRC_REF.search(s):
            print(f"  候选 L{i}: {s[:64]}")
    return 2

if __name__ == "__main__":
    sys.exit(main())
