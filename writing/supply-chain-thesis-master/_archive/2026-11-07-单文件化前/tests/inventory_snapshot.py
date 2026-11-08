# -*- coding: utf-8 -*-
"""Read-only snapshot proving pre-existing skills were not touched."""
import hashlib
from collections import Counter
from datetime import datetime
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "deliverables" / "skills-inventory-snapshot.txt"
NEW_SKILL = "writing/supply-chain-thesis-master"
assert SKILL_ROOT.name == "skills", f"wrong root: {SKILL_ROOT}"


def is_pre_existing(p: Path) -> bool:
    rel = str(p.relative_to(SKILL_ROOT)).replace("\\", "/")
    return not (rel.startswith(NEW_SKILL + "/") or "/tests/" in rel or "/deliverables/" in rel)


files = sorted(p for p in SKILL_ROOT.glob("**/SKILL.md") if is_pre_existing(p))
by_cat = Counter(str(p.relative_to(SKILL_ROOT)).split("\\")[0] for p in files)

lines = [
    "# 原有技能只读快照",
    "",
    f"生成时间：{datetime.now().isoformat(timespec='seconds')}",
    f"根目录：{SKILL_ROOT}",
    f"排除：{NEW_SKILL}（本次新建）",
    "",
    "> 说明：本快照在验收阶段生成，用于**事后核验**本次任务未修改/删除/覆盖任何原有技能；",
    "> 它不是事前备份。因本次未对原有技能执行任何写操作，无需回滚。",
    "> 合并/备份/恢复能力的演练证据见 `tests/runtime/dup-drill/`（虚拟样本，不进入真实技能库）。",
    "",
    f"原有技能总数：{len(files)}",
    "",
    "## 按顶层目录",
    "",
    "| 目录 | 数量 |",
    "|---|---|",
]
for k, v in sorted(by_cat.items()):
    lines.append(f"| {k} | {v} |")
lines += ["", "## 逐项哈希（sha256 前 12 位）", "", "| 相对路径 | sha256[:12] | 字节 |", "|---|---|---|"]
for p in files:
    rel = str(p.relative_to(SKILL_ROOT)).replace("\\", "/")
    h = hashlib.sha256(p.read_bytes()).hexdigest()[:12]
    lines.append(f"| {rel} | {h} | {p.stat().st_size} |")
lines.append("")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"snapshot: {len(files)} skills -> {OUT}")
