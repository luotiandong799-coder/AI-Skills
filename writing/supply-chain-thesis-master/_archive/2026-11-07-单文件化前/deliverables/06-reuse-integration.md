# 新旧能力复用与整合报告

## 一、决策原则

按 `skill-compact` 五策略判据（merge >30% 重复 / absorb 子集 / extract-shared 共用模板 / refactor >300 行 / no-op）逐项定态；按 `skill-cleaner` 纪律「先备份再改、keeper 判定、隔离区 + restore」执行。本次是**新建技能**，不改动任何原有技能，故所有合并决策都发生在「吸收进新技能内部」这一层。

## 二、5 个 GitHub 项目的四态决策

| 项目 | 许可证 | 实读文件 | 决策 | 落点 | 未采用 / 放弃 |
|---|---|---|---|---|---|
| `trleo/skill-cleaner` | MIT（已读 LICENSE 原文） | `skills/skill-cleaner/SKILL.md` | **吸收**三信号 + keeper + 隔离区/restore 流程 | `modules/09`、`workflows/content-deduplication.md`、`tests/verify_acceptance.py` 的 dup-drill | 放弃 Python CLI 本体（路径假设不适配 WB） |
| `JuanJoseGonGi/skill-compact` | MIT | `SKILL.md` | **吸收**五策略 + 先备份 + 500 行上限 + references 一层深 + manifest | 本报告决策表、`dup-drill/merged/manifest.md` | 放弃 TS/tsx 脚本链 |
| `junbolian/Academic-Humanizer` | MIT | `academic-humanizer/SKILL.md` | **吸收**编辑纪律五条、audit/compare 思路、Not reasons to change 清单 | `references/academic-writing-rules.md` §一、§七 | 放弃英文语法层（非英语母语专项） |
| `zczjyq/de-AIGC-skill` | **无 LICENSE（raw 404）** | `SKILL.md` | **只吸收方法论**：16 类中文 AI 模式 → 归纳为 C1–C10、保量 ≥92%、术语表 + 滚动段落摘要、轻微自修/严重上报分界 | `references/academic-writing-rules.md` §二–§五、`modules/10` 第三节 | **不复制任何原文段落**；不采用「以降低 AIGC 率为目标」的表述；不执行其脚本 |
| `cangtianhuang/humanizer-academic-zh` | MIT | `SKILL.md` | **吸收**「命中不等于必须替换」 | `references/academic-writing-rules.md` §六噪声预算 | 无 |

诚实边界：未执行任何第三方脚本，只阅读文本；这些项目的「降 AIGC 率」效果均未获独立验证，本技能不承诺任何检测结果。

## 三、去重合并决策（关键）

| 项 | 判定 |
|---|---|
| 三家 Humanizer 重叠度 | 约 60%（编辑纪律、套话清单、保量阈值、自检项高度重合） |
| 策略 | **merge** → 合并为 `references/academic-writing-rules.md` 一套规则 |
| 禁止 | 不叠加三份规则、不在模块里复制规则表 |
| 结构 | 编辑纪律 → 内容层 C1–C10 → 语言层 → 风格层 → 硬阈值 → 噪声预算 → 自检 → 禁止事项 |
| 本地 `humanizer-zh` | 只吸收可用部分进同一规则源，非学术场景仍可由原技能处理，不重复建规则 |

## 四、内部整合：规则单源

| 规则类别 | 唯一来源 | 其他文件如何引用 |
|---|---|---|
| 公式与指标定义 | `references/formulas-and-indicators.md`（W1–W8 / I1–I8） | 模块 03、04 及正文只写编号 + 口径易错点 |
| 润色规则与硬阈值 | `references/academic-writing-rules.md` | 模块 10 指向该文件；检查清单只写审查动作，不写阈值数字 |
| 引用格式 | `references/citation-rules.md` | 模块 11 + `checklists/citation-verification.md` |
| 方法适用条件 | `references/research-methods.md` | 模块 05 + 各方向框架 |
| 项目记忆（术语表/章节摘要） | `SKILL.md` §五 | 模块 10 第三节、`workflows/long-document-editing.md` |

## 五、与原有能力的边界划分

| 能力 | 归属 | 理由 |
|---|---|---|
| 供应链论文全流程、专业指标、开题、答辩 | 本技能 | 原有库无此能力 |
| Word 成稿与学校模板落地 | `workbuddy-docx` | 排版不是内容能力 |
| Excel 批量处理与图表 | `workbuddy-sheetagent` / `workbuddy-sheet-generation` | 本技能只定口径 |
| PDF 文献读取 | `workbuddy-pdf` | 读取通道 |
| 通用中文去 AI 味（非学术） | `writing/humanizer-zh` | 语体不同 |
| 通用长文写作方法 | `writing/wb-doc-writing` | 无供应链专业约束 |
| 技能库审计、合并、备份 | `system/skills-security-check` | 是工具不是内容 |
| 文件级重复清理 | `system/local-file-dedup` | 与论文内容去重不同层级 |

## 六、验收中发现的 4 个问题与修复（真实记录）

| # | 问题 | 证据 | 修复 | 复核 |
|---|---|---|---|---|
| 1 | 模块 03 与公式库双写 W2/W7 等 8 个公式本体 | 基线 `[FAIL] 公式单源 拣货总件数/` | 第三节整表改为「指标 / 编号 / 口径易错点」，公式本体全部降级为编号引用 | PASS |
| 2 | 模块 04 与公式库双写 7 处公式（第 6 步审计先发现） | Grep 命中 | 已改为 I1/I2/I3/I6/I7/I8/W7 编号引用 | PASS |
| 3 | `checklists/academic-style-review.md` 复写「应 ≥92%」阈值 | 基线 `[FAIL] 保量阈值 92% 单源` | 改为「按规则库第五节判定，本清单不重复写阈值」 | PASS |
| 4 | 保量阈值未定义统计粒度，套话密集段必然误判（P2 48.3%） | 基线 `[FAIL] P2 保量 ≥92%` | 规则库补 §5.1「统计单位 = 全文/全章」+ §5.2「需补料分支」，并在自检清单加一条；明确优先级「不新增 > 保量阈值」 | PASS（走需补料分支，不编造补足） |

另修正测试工具自身问题：`inventory_snapshot.py` 初版根目录少算一层，把虚拟演练样本误计入原有技能（15 个）；修正 `parents[3]` + 排除 `tests/` 后得 60 个，与人工盘点一致。

## 七、明确放弃的内容

| 放弃项 | 原因 |
|---|---|
| `skill-cleaner` / `skill-compact` 的可执行脚本 | 路径与运行时假设不适配 WB，只取方法 |
| 三家 Humanizer 的英文语法专项 | 中文本科论文不适用 |
| 「降低 AIGC 率」「通过查重」类目标表述 | 无法验证且违反用户红线 |
| 把 12 个模块注册成独立技能 | 违反单一入口要求，会造成重复与上下文浪费 |
| 复制 de-AIGC-skill 原文段落 | 无 LICENSE，版权边界不清 |
| 修改 / 删除任何原有技能 | 用户明确禁止 |
