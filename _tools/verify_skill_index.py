#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
技能仓库索引对账 / 自动同步工具
监听 00_总目录_所有AI入口.md §7「入库与合规纪律」。

用法（在唯一物理真身目录下运行）：
    python _tools/verify_skill_index.py          # 只体检，不改动；有不合规则 exit 1
    python _tools/verify_skill_index.py --fix    # 体检并按磁盘真相自动重写三张表

背景：本仓库存在并发写入（豆包学习轮会自行 bump 版本号并 commit），
静态版本表必然漂移 —— 所以提交 / 发布前务必跑一次本脚本。

覆盖检查：
  ① 集合一致：§3 / §4 / 附录C 三张表与磁盘实际技能集合完全一致（不多不少）
  ② 版本准确：三表版本号与各 SKILL.md frontmatter 完全一致
  ③ 三表互账：§3 = §4 = 附录C
  ④ 8 类归档：根目录无平铺 SKILL.md、无游离在 8 类之外的技能
  ⑤ 触发门禁：每个 SKILL.md 必须有非空 description
  ⑥ 旧路径：不得出现 D:\\AI技能仓库 等已删路径（规则自述句除外）
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = ["agent", "defaults", "engineering", "meta",
        "media", "research", "system", "writing"]
OLD_PATHS = ("D:\\AI技能仓库", "D:/AI技能仓库")
# 规则自述句（在这类句子里出现旧路径是为了「禁止」它，不算违规）
PROHIBIT_CTX = ("不得出现", "禁止", "无 `D:", "等已删路径", "等旧路径")

MAIN = os.path.join(ROOT, "00_总目录_所有AI入口.md")
PRE = os.path.join(ROOT, "00_做前预读_共学三方纪律.md")
SEP = "=" * 70

DO_FIX = "--fix" in sys.argv


def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def frontmatter(t):
    m = re.search(r"\A﻿?---\s*\n(.*?)\n---", t, re.S)
    return m.group(1) if m else ""


def fm_field(fm, key):
    m = re.search(r"^%s:[ \t]*(.*)$" % re.escape(key), fm, re.M)
    if not m:
        return None
    val = m.group(1).strip()
    if val and val not in ("|", ">", "|-", ">-", "|+"):
        return val.strip("'\"")
    lines = []
    for ln in fm[m.end():].splitlines():
        if not ln.strip():
            if lines:
                break
            continue
        if ln[:1] in (" ", "\t"):
            lines.append(ln.strip())
        else:
            break
    return " ".join(lines).strip()


def section(t, start, end):
    m = re.search(start + r".*?\n(.*?)\n" + end, t, re.S)
    return m.group(1) if m else ""


def parse_row_table(block):
    out = {}
    for line in block.splitlines():
        m = re.match(r"\|\s*([^|]*?)\s*\|\s*`([a-z]+/[^`/]+/SKILL\.md)`", line)
        if m:
            out[m.group(2)] = m.group(1).strip()
    return out


def parse_inline_table(block):
    out = {}
    for line in block.splitlines():
        if not line.startswith("| `"):
            continue
        for m in re.finditer(r"`([a-z]+)/([^`/]+)`\s+([^\s·|]+)", line):
            k = "%s/%s/SKILL.md" % (m.group(1), m.group(2))
            out[k] = m.group(3)
    return out


def build_rows(actual):
    rows = []
    for cat in CATS:
        for k in sorted(k for k in actual if k.startswith(cat + "/")):
            rows.append("| %s | `%s` |" % (actual[k][0], k))
    return "\n".join(["| 版本 | 路径 |", "| ------ | --- |"] + rows)


def apply_fix(main_txt, pre_txt, actual):
    """按磁盘真相重写 §3 内联版本号 + 重建 §4 / 附录C 两张行表。"""
    changed = []

    def patch_inline(block):
        for k, (ver, _sf) in actual.items():
            cat, name = k[:-len("/SKILL.md")].split("/", 1)
            block = re.sub(
                r"`%s/%s`\s+[^\s·|]+" % (re.escape(cat), re.escape(name)),
                "`%s/%s` %s" % (cat, name, ver), block)
        return block

    new_main, n1 = re.subn(
        r"(## 3\.[^\n]*\n)(.*?)(\n### )",
        lambda m: m.group(1) + patch_inline(m.group(2)) + m.group(3),
        main_txt, flags=re.S)
    rows = build_rows(actual)
    new_main, n2 = re.subn(
        r"(## 4\.[^\n]*\n)(.*?)(\n（`—`)",
        lambda m: m.group(1) + rows + m.group(3),
        new_main, flags=re.S)
    new_pre, n3 = re.subn(
        r"(## 附 C[^\n]*\n)(.*?)(\n（`—`)",
        lambda m: m.group(1) + rows + m.group(3),
        pre_txt, flags=re.S)

    if new_main != main_txt:
        write(MAIN, new_main)
        changed.append("00_总目录_所有AI入口.md")
    if new_pre != pre_txt:
        write(PRE, new_pre)
        changed.append("00_做前预读_共学三方纪律.md")
    return changed, (n1, n2, n3)


# ------------------------- 收集磁盘真相 -------------------------
actual = {}
for cat in CATS:
    base = os.path.join(ROOT, cat)
    if not os.path.isdir(base):
        continue
    for d in sorted(os.listdir(base)):
        sf = os.path.join(base, d, "SKILL.md")
        if os.path.isfile(sf):
            ver = fm_field(frontmatter(read(sf)), "version")
            actual["%s/%s/SKILL.md" % (cat, d)] = (ver if ver else "—", sf)

print(SEP)
print("技能仓库索引对账 · 真身：%s" % ROOT)
print(SEP)
print("磁盘实际技能数：%d" % len(actual))

main_txt, pre_txt = read(MAIN), read(PRE)
sec3 = parse_inline_table(section(main_txt, r"## 3\. ", r"### "))
sec4 = parse_row_table(section(main_txt, r"## 4\. ", r"（`—`"))
appc = parse_row_table(section(pre_txt, r"## 附 C", r"（`—`"))

for nm, tb in (("§3 分类表", sec3), ("§4 技能清单", sec4), ("附录C 版本表", appc)):
    print("  %-14s 解析到 %d 条" % (nm, len(tb)))

# ------------------------- 体检 -------------------------
def audit():
    bad = []
    print()
    print("--- ① 集合一致 / ② 版本准确 ---")
    for nm, tb in (("§3 分类表", sec3), ("§4 技能清单", sec4), ("附录C 版本表", appc)):
        miss = sorted(set(actual) - set(tb))
        phan = sorted(set(tb) - set(actual))
        wrong = sorted(k for k in set(tb) & set(actual) if tb[k] != actual[k][0])
        ok = not (miss or phan or wrong)
        print("[%s] %-12s missing=%d phantom=%d 版本不符=%d"
              % ("OK  " if ok else "FAIL", nm, len(miss), len(phan), len(wrong)))
        bad += ["① %s 缺少 %s" % (nm, k) for k in miss]
        bad += ["① %s 幽灵条目 %s" % (nm, k) for k in phan]
        bad += ["② %s %s 表=%s 实际=%s" % (nm, k, tb[k], actual[k][0]) for k in wrong]

    print()
    print("--- ③ 三表互账 ---")
    for a, b, A, B in (("§3", "§4", sec3, sec4), ("§4", "附录C", sec4, appc)):
        diff = sorted(k for k in set(A) | set(B) if A.get(k) != B.get(k))
        print("[%s] %s vs %s 差异=%d" % ("OK  " if not diff else "FAIL", a, b, len(diff)))
        bad += ["③ %s/%s 不一致：%s" % (a, b, k) for k in diff]

    print()
    print("--- ④ 8 类归档（根目录禁平铺） ---")
    flat = [f for f in os.listdir(ROOT)
            if f.endswith("SKILL.md") and os.path.isfile(os.path.join(ROOT, f))]
    stray = []
    for cur, _d, files in os.walk(ROOT):
        rel = os.path.relpath(cur, ROOT).replace("\\", "/")
        if rel == "." or rel.split("/")[0] in ("memory", "_tools"):
            continue
        if "SKILL.md" in files and rel.split("/")[0] not in CATS:
            stray.append(rel)
    print("根目录平铺=%d，8 类之外游离=%d %s" % (len(flat), len(stray), (flat + stray) or ""))
    bad += ["④ 未归档技能：%s" % (flat + stray)] if (flat or stray) else []
    if not flat and not stray:
        print("[OK  ] 全部技能均落在 8 类目录内")

    print()
    print("--- ⑤ description 非空门禁 ---")
    nod = [k for k, (_v, sf) in actual.items()
           if not fm_field(frontmatter(read(sf)), "description")]
    print("缺少非空 description 的技能：%d %s" % (len(nod), nod or ""))
    bad += ["⑤ %s 无有效 description" % k for k in nod]
    if not nod:
        print("[OK  ] 全部技能均可被正确触发")

    print()
    print("--- ⑥ 旧路径扫描（规则自述句除外） ---")
    hits = []
    for cur, _d, files in os.walk(ROOT):
        rel = os.path.relpath(cur, ROOT).replace("\\", "/")
        if rel.split("/")[0] in ("memory", "_tools"):
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(cur, fn)
            for i, ln in enumerate(read(p).splitlines(), 1):
                if any(op in ln for op in OLD_PATHS) and \
                        not any(ctx in ln for ctx in PROHIBIT_CTX):
                    hits.append("%s:%d" % (os.path.relpath(p, ROOT).replace("\\", "/"), i))
    hits = sorted(set(hits))
    print("真实违规行：%d %s" % (len(hits), hits or ""))
    bad += ["⑥ 含旧路径 %s" % h for h in hits]
    if not hits:
        print("[OK  ] 未发现真实旧路径引用")
    return bad


bad = audit()

if bad and DO_FIX:
    print()
    print(">>> --fix：按磁盘真相自动重写三张表 …")
    main_txt, pre_txt = read(MAIN), read(PRE)
    changed, n = apply_fix(main_txt, pre_txt, actual)
    print("    已更新文件：%s" % (", ".join(changed) or "无"))
    main_txt, pre_txt = read(MAIN), read(PRE)
    sec3 = parse_inline_table(section(main_txt, r"## 3\. ", r"### "))
    sec4 = parse_row_table(section(main_txt, r"## 4\. ", r"（`—`"))
    appc = parse_row_table(section(pre_txt, r"## 附 C", r"（`—`"))
    bad = audit()

print()
print(SEP)
if bad:
    print("不合规 %d 条：" % len(bad))
    for b in bad:
        print("  -", b)
    print(SEP)
    sys.exit(1)
print("全部通过：三表实时同步 · 版本准确 · 8类归档 · description 非空 · 无旧路径")
print(SEP)
sys.exit(0)
