# 学习轮 r198-A：LangFlow组件版本分叉与Make计费白泡与SKILL官方标准与技能索引总量与spec前置层（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/application-orchestrate | 死链 |
| 2 | docs.langflow.org/components-processing | OK 全文（components overview） |
| 3 | activepieces.com/docs/activepieces/overview | 死链 |
| 4 | docs.n8n.io/courses/level-one | OK |
| 5 | make.com/en/help/scenarios/scenario-editor | OK 全文 |
| 6 | pipedream.com/docs/workflows/build | 死链 |
| 7 | docs.anthropic.com agent-skills/upload | region 不可用 |
| 8 | agentskills.io | OK 官方标准 |
| 9 | skillsmp.com/skills/page/2 | OK |
| 10 | GitHub AI 生态（robots 禁走搜索） | OK |

## 独点（5 个）
### A1：LangFlow 组件版本分叉与更新门——workspace 副本不自动同步（来源：docs.langflow.org components overview）
- 组件放进 flow 时创建 **detached 副本**，保留添加时的版本与状态，**不随 Langflow 升级自动同步**；通知分两档：Update ready（无 breaking）/ Update available（可能 breaking，改输入输出会断连）；更新前可开 **Create backup flow**（同目录 `(backup)` 后缀）；Freeze 冻结组件**及全部上游**不再重跑。
- 判据：**组件实例是快照不是引用**——升级平台后旧 flow 里组件版本不变是设计而非故障；动 breaking 更新先备份。
- **提升层**：工作流。

### A2：Make 场景编辑器——操作计费白泡 + Explain flow + Auto-align 不可逆 + Blueprint 导入导出（来源：make.com scenario-editor）
- 每个模块右上白泡显示**该模块执行的操作数**（按总操作数计费）；Explain flow（飞机图标）跑前可视化数据流；**Auto-align 不可逆**（除非先保存）；Export/Import Blueprint 为 JSON；Previous Versions 可恢复旧版；路由连线可设 filter/unlink/add router。
- 判据：**可视化平台也有"对齐布局不可逆 + 版本恢复"的纪律**——大改前保存/导出 blueprint。
- **提升层**：工作流。

### A3：Agent Skills 官方标准——SKILL.md 最小元数据 + progressive disclosure 三阶段（来源：agentskills.io）
- 官方标准文档形态：skill=文件夹含 SKILL.md（最小 name+description）+ scripts/references/assets 可选；加载走 **progressive disclosure 三阶段**：Discovery（只读 name+description）→ Activation（任务匹配才读全文进上下文）→ Execution；客户端 Showcase 列支持产品。
- 判据：**"渐进披露"是 skill 标准的第一设计原则**——SKILL.md 的 description 决定激活，正文只在激活时花 token。
- **提升层**：可复用 Skill（标准）。

### A4：skillsmp 索引总量 3,229,343 cataloged skills + 高分新技能信号（来源：skillsmp.com/skills/page/2）
- 索引 102 页、当前展示 10,122 条、**cataloged 总量 3,229,343**；新信号：archify 68,705★（架构/序列/数据流图→可探索 HTML+SVG）、deslop（diff-scoped AI-slop 清理）、MoneyPrinterTurbo 125,001★、notion 390,183★、markitdown 45,497★、gan-style-harness（GAN 生成器-评估器框架，基于 Anthropic 2026-03 框架论文）。
- 判据：**技能市场已是百万级索引**——选技能用排行榜+厂商源双重校验。
- **提升层**：生态观察。

### A5：GitHub 生态——OpenSpec spec 前置层 + orca 并行 agent 舰队 + 754 网络安全技能（来源：GitHub 生态走搜索）
- OpenSpec：AI coding 开始前加 proposal→spec→design→task 结构化层，让人与 agent 先对齐"建什么"；stablyai/orca：ADE 并行 agent 舰队（用自己的订阅跑任意 coding agent，desktop/mobile/remote）；browser-use 生态 9M★/22M 安装；754 结构化网络安全 skills（映射五大行业框架）。
- 判据：**"先对齐再编码"已工具化（spec 前置层）；并行 agent 管理走"自带订阅的 ADE"**。
- **提升层**：生态观察/工作流。

## 判重说明
- A1 → r196-C 已记 Tool Mode/双输出/双成本；组件版本分叉+Freeze 上游+备份 flow 全新增量。
- A2 → r196-B 已记 Make 标题壳；scenario-editor 首次真拉，计费白泡/Explain flow/Auto-align/Blueprint 全新。
- A3 → r195-C 已记 SKILL.md de facto 标准 50+ 客户端；agentskills.io 官方三阶段表述 + 文件夹结构首次真拉，取增量。
- A4 → r196-B 已记 skillsmp SOC 867；page/2 首次真拉，总量 322 万 + archify/deslop/MoneyPrinter 增量。
- A5 → r196-A/C 已记 GitHub 生态；OpenSpec/orca/754 网络安全技能增量。
