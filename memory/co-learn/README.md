# 共同学习区 / Co-Learn

豆包 与 WorkBuddy 共享的学习地址。两边产出并排存放、一起同步到 GitHub，互不覆盖。

## 地址（同一物理目录，两处可见）
- 本地实时：`D:\腾讯AI\skills\memory\co-learn\`（NTFS junction → 仓库 `memory/co-learn\`）
- GitHub：`AI技能仓库/memory/co-learn/`

## 目录
- `doubao/` —— 豆包产出。用户粘贴或豆包自写，命名 `YYYY-MM-DD_主题.md`。
- `workbuddy/` —— WorkBuddy 每日学习落点，命名 `YYYY-MM-DD_主题.md`。

## 同步模式（GitHub 整理模式）
- WorkBuddy 每次收尾 `git commit` + SSH over 443 `push` 一次（不重试、不启 VPN、禁止强推）。
- 豆包的 `.md` 由用户放进 `doubao/`，下一次 WorkBuddy 同步即进 GitHub。
- 两边笔记**按 `日期_主题.md` 落盘，绝不共写同一文件**，避免互相覆盖。
- 引用对方结论时注明来源：`来源：doubao/2026-09-18_xxx.md` 或 `来源：workbuddy/2026-09-18_xxx.md`，便于追溯与去重。
- 去重：落地前先 grep 对方目录，重叠 >60% 不重复写，只补对方没有的独有点。

## 仓库整体整理模式
- 技能按职能分 8 类：`engineering/ defaults/ writing/ media/ research/ agent/ system/`（根 README 有索引）。
- `memory/` 存学习记录（含本共同学习区）；`meta/` 存仓库元信息（SkillHub 迁移记录、plugins）。
- `AGENTS.md` / `README.md` 留在根：规则入口 + GitHub 展示。
- 本地技能实时目录 `D:\腾讯AI\skills`（junction → `C:\Users\26719\.workbuddy\skills`）保持**平铺**（WorkBuddy 加载所需）；仓库为**分类归档**，同步时按职能落到对应类别目录。
