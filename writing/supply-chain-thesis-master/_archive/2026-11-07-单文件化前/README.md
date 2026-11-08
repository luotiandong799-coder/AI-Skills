# 1.0.0 分散形态只读快照（2026-11-07 单文件化前）

- 唯一入口已上移为 `../../SKILL.md`（1.1.0 单文件一条）。本目录不作技能入口、不被路由调用。
- 回退方法：把本目录内 `modules/ references/ workflows/ checklists/ templates/ tests/ deliverables/ sources/` 拷回技能根目录，并把 `SKILL_1.0.0_原版快照.md.bak` 改名 `SKILL.md` 覆盖即可。
- `tests/verify_acceptance.py` 是 1.0.0 形态的验收脚本，依赖本目录内分散文件；复跑需先执行上述回退。
