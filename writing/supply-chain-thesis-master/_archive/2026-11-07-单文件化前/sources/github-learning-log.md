# GitHub 学习来源与许可证记录

学习日期：2026-11-07。方式：读取仓库首页、README、SKILL.md 正文与 LICENSE 原文，非仅凭 README 下结论。

## 逐项记录

| 项目 | 版本/最近提交 | 许可证 | 实际读到的文件 | 吸收内容 | 未采用 |
|---|---|---|---|---|---|
| trleo/skill-cleaner | v0.1.0，2026-10-30 | MIT（已读 LICENSE 原文，Copyright (c) 2026 trleo） | skills/skill-cleaner/SKILL.md | 五步流程、三类重复信号（同名/同内容/关键词 Jaccard≥0.30）、keeper 判定顺序、隔离区 + restore、managed 技能只报不动 | Python CLI 本体（路径假设不适配 WB） |
| JuanJoseGonGi/skill-compact | v0.1.0，2026-03-03 | MIT | SKILL.md | 五策略判据（merge >30% 重复 / absorb 子集 / extract-shared 共用模板 / refactor >300 行 / no-op）、先备份再改、500 行上限、references 一层深、manifest 记录合并决策 | TS/tsx 脚本链 |
| junbolian/Academic-Humanizer | v1.1，2026-10-21 | MIT | academic-humanizer/SKILL.md | 编辑纪律五条、Rule 1–12 框架、check_revision.py 的 audit/compare 思路、Not reasons to change 清单 | 英文语法层规则（first-language 非英语专项） |
| zczjyq/de-AIGC-skill | 活跃，2026 | **无 LICENSE 文件（raw 请求返回 404）** | SKILL.md | 仅吸收方法论：16 类中文 AI 模式分类、保量润色 ≥92%、术语表 + 滚动段落摘要、轻微自修/严重上报分界、LaTeX 保护 | **不复制任何原文段落**；不采用「以降低 AIGC 率为目标」的表述 |
| cangtianhuang/humanizer-academic-zh | 2026-05-23 | MIT | SKILL.md | 25 条精简规则、命中不等于必须替换、表达质感四要素 | 无 |

## 合并决策

三家 Humanizer（Academic-Humanizer / de-AIGC / humanizer-academic-zh）重叠约 60%，按 skill-compact 的 merge 判据合并为 `references/academic-writing-rules.md` 一套规则，禁止叠加三份。

## 诚实边界

1. de-AIGC-skill 无许可证，只吸收不受版权保护的方法与思想，未逐字搬运。
2. 这些项目的「降 AIGC 率」效果均未获独立验证，本技能不承诺任何检测结果。
3. 未执行任何第三方脚本；仅阅读文本。
