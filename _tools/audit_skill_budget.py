#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
技能预算与标题完整性机检（五轴 + 标题缺陷）

用途：在唯一物理真身目录（D:\\腾讯AI\\skills）下运行，检查全部 SKILL.md 是否越预算。

    python _tools/audit_skill_budget.py            # 只体检；有违规 exit 1
    python _tools/audit_skill_budget.py --near     # 额外列出预算临界项（>480 行 / >950 字符）

五轴口径：
  ① 行数     ≤500（豆包自留地 wb-execute-discipline / wb-context-compressor 另有 ≤200 红线）
  ② description ≤1024  —— **必须走 PyYAML 解析**。正则抓折行标量（`>-`）会把标量头与
     换行/缩进算进去，虚增 3~5 字符（曾把 1022 误报成 1027）。
  ③ FFFD（U+FFFD 乱码替换符）=0
  ④ CRLF =0
  ⑤ frontmatter 可被 yaml.safe_load 解析，且 name/description 非空

标题缺陷（次要轴，只扫 SKILL.md，跳过代码围栏）：
  · 全角/半角括号不配对
  · 「（来源：…（原文已下沉 …）」——下沉工具按字符截断生成的索引行，会同时造成
    **括号不闭合** 与 **URL 被切半**（静默断链）。修法：从同技能 KB 取回完整标题。
  · 标题以「（ / ，/ ：/ 《 」等未闭合符号结尾

退出码：0 = 全通过；1 = 有违规。
"""
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELF_GOVERNED = {"engineering/wb-execute-discipline", "engineering/wb-context-compressor"}
NEAR_LINES = 480
NEAR_DESC = 950
SEP = "=" * 70
SHOW_NEAR = "--near" in sys.argv


def skill_files():
    for dp, dn, fns in os.walk(ROOT):
        if ".git" in dp.replace("\\", "/").split("/"):
            continue
        if "SKILL.md" in fns:
            yield os.path.join(dp, "SKILL.md")


def heading_defects(lines):
    """只扫非代码围栏内的 ##/### 标题"""
    out = []
    fence = False
    for i, ln in enumerate(lines, 1):
        if ln.strip().startswith("```"):
            fence = not fence
            continue
        if fence or not re.match(r'^#{2,3} \S', ln):
            continue
        why = []
        if ln.count("（") != ln.count("）"):
            why.append("全角括号不配对")
        if ln.count("(") != ln.count(")"):
            why.append("半角括号不配对")
        if re.search(r'（来源：.+（原文已下沉', ln):
            why.append("来源被下沉注记截断")
        if ln.count("原文已下沉") > 1:
            why.append("下沉注记重复")
        if ln.rstrip().endswith(("（", "(", "，", "：", ":", "、")):
            why.append("标题结尾截断")
        if re.search(r'《[^》]*$', ln):
            why.append("书名号未闭合")
        if why:
            out.append((i, why, ln))
    return out


def main():
    rows, bad, near, headbad = [], [], [], []
    for p in skill_files():
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        raw = open(p, "rb").read()
        text = raw.decode("utf-8", errors="replace")
        lines = text.rstrip("\n").split("\n")
        nlines = len(lines)
        fffd = raw.count(b"\xef\xbf\xbd")
        crlf = raw.count(b"\r\n")

        desc_len, err = None, ""
        if text.startswith("---\n"):
            end = text.find("\n---", 4)
            if end < 0:
                err = "frontmatter 未闭合"
            else:
                try:
                    fm = yaml.safe_load(text[4:end]) or {}
                    d = fm.get("description")
                    desc_len = len(str(d)) if d else 0
                    if not fm.get("name"):
                        err = "缺 name"
                    elif not d:
                        err = "description 为空"
                except Exception as e:
                    err = f"YAML 解析失败: {e}"
        else:
            err = "无 frontmatter"

        why = []
        if nlines > 500:
            why.append(f"行数 {nlines} > 500")
        if desc_len is not None and desc_len > 1024:
            why.append(f"description {desc_len} > 1024")
        if fffd:
            why.append(f"FFFD={fffd}")
        if crlf:
            why.append(f"CRLF={crlf}")
        if err:
            why.append(err)
        rows.append((rel, nlines, desc_len, why))
        if why:
            bad.append((rel, why))
        elif SHOW_NEAR and (nlines >= NEAR_LINES or (desc_len or 0) >= NEAR_DESC):
            near.append((rel, nlines, desc_len))

        hd = heading_defects(lines)
        if hd:
            headbad.append((rel, hd))

    print(SEP)
    print(f"技能预算机检 · 真身：{ROOT}")
    print(f"扫描 SKILL.md：{len(rows)} 个")
    print(SEP)

    print("\n--- ① 预算五轴 ---")
    if bad:
        for rel, why in bad:
            print(f"[FAIL] {rel}\n         " + " / ".join(why))
    else:
        print("[OK  ] 行数 ≤500 · description ≤1024 · FFFD=0 · CRLF=0 · frontmatter 可解析 —— 0 违规")

    print("\n--- ② 标题完整性 ---")
    if headbad:
        for rel, hd in headbad:
            print(f"[FAIL] {rel} —— {len(hd)} 处")
            for i, why, ln in hd[:6]:
                print(f"        L{i}: {'/'.join(why)}  {ln[:110]}")
    else:
        print("[OK  ] 无括号不配对 / 无下沉注记截断 / 无未闭合结尾 —— 0 缺陷")

    if SHOW_NEAR:
        print(f"\n--- ③ 预算临界（≥{NEAR_LINES} 行 或 ≥{NEAR_DESC} 字符，合规但下轮需盯）---")
        for rel, n, d in sorted(near, key=lambda x: -x[1]):
            print(f"        {n:>4d}/500  {(d if d is not None else -1):>5d}/1024  {rel}")

    print("\n" + SEP)
    ok = not bad and not headbad
    print("全部通过：预算五轴 0 违规 · 标题完整性 0 缺陷" if ok else "存在不合规项，见上")
    print(SEP)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
