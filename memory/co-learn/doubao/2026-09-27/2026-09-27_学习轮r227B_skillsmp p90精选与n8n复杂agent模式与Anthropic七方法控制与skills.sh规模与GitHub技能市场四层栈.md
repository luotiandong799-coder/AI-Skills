# 学习轮 r227B：skillsmp p90精选与n8n复杂agent模式与Anthropic七方法控制与skills.sh规模与GitHub技能市场四层栈（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/90（#8901-8963 实拉） | OK |
| 2 | Dify 检索（Creator Center 模板市场/Agent Strategies） | OK |
| 3 | n8n 检索（Production AI Playbook/Agent Memory/Context Engineering） | OK |
| 4 | Anthropic 检索（Steering 七方法/Skills vs Commands 统一模型/checkup） | OK |
| 5 | Activepieces 检索（AI Agent Builder/企业 agent） | OK |
| 6 | skills.sh 检索（Vercel State of agent skills/SkillRegistry/私有注册表） | OK |
| 7 | Make 检索（AI Agent New app 六步流程/最佳实践/Knowledge 模块） | OK |
| 8 | deeplearning.ai 检索（新课程/AI Code Review） | OK |
| 9 | GitHub 生态（agentconn 技能市场四层栈/CLAWS 目录/Hermes 自动写 skill） | OK |
| 10 | WaytoAGI 检索（Claude Agent Skills 蓝皮书/提示词指挥→委托） | OK |

## 独点（4 个）
### B1：skillsmp p90 精选：AST 图爆炸半径审查 / SmartCrusher 压缩 / instinct 演进学习 / Postgres 写前加载（来源：skillsmp.com/skills/page/90，2026-09-27 实拉）
- **code-review-graph（vudovn/ag-kit ★8,179）**：**Tree-sitter AST 图+MCP 的 token 高效代码审查——计算变更爆炸半径（blast radius）而不是读整个代码库，SQLite 图数据库做结构分析**（token 高效审查面：爆炸半径计算砍 token，与 r227-A qt-cpp-review 并行 agent 审查互补）。
- **headroom（momori777/Artemis ★346）**：**SmartCrusher+CCR 上下文压缩——crunch 大型 JSON 数组/工具输出/搜索结果省 token**（上下文压缩面：SmartCrusher/CCR 具体技术增量）。
- **continuous-learning-v2（affaan-m/ECC ★264,820）**：**通过 hooks 观察会话，置信度评分创建原子 instinct，再演进成 skill/command/agent；v2.1 项目范围 instincts 防跨项目污染**（持续学习面：instinct→skill 演进+置信度门槛+防污染）。
- **supabase-postgres-best-practices（supabase/agent-skills ★2,643）**：**写任何 Postgres 前先加载——建表/改列/选类型/schema/迁移/RLS 策略与验证测试/索引/触发器/函数/队列/pgvector；不只性能指南，schema 安全 SQL 也要**（数据库最佳实践面：写前加载规则包）。
- **提升层**：工作流 / 可复用 Skill。

### B2：n8n 复杂 agent 模式与上下文工程四策略 / Anthropic 七方法控制与三层统一模型（来源：blog.n8n.io Production AI Playbook 2026-06-09 + AI Agent Memory/Context Engineering 2026-07-07 + claude.com Steering 2026-06-18 + jsmanifest Unified Model 2026-06-06，实拉）
- **n8n Production AI Playbook（复杂性悬崖）**：**第一个 agent 好、加三个就不可调试；sub-workflows 作为可复用 agent 组件（优于 AI Agent Tool 的理由）；多 agent 记忆三档：window buffer→数据库（Postgres/Redis/MongoDB）→会话 ID（多 agent 记忆的关键）；自纠正 agent loop（迭代推理）；prompt chaining vs agent delegation 的选择**（复杂 agent 模式面：组件化+记忆分层+自纠正循环）。
- **n8n Context Engineering 四策略**：**Write/Select/Compress/Isolate——写精炼指令/选择性检索/压缩历史/隔离无关上下文；just-in-time retrieval with MCP**（上下文工程四策略面：写/选/压/隔四动作）。
- **Anthropic Steering 七方法**：**控制 Claude 行为的七种方法（CLAUDE.md/rules/skills/subagents/hooks/output styles/追加 system prompt），每个方法控制三维：何时加载进上下文/长会话是否持久（compaction 行为）/承载多少权威**（控制方法矩阵面：加载时机+持久性+权威三维）。
- **skills/commands/tools 三层统一模型**：**Interface/Procedure/Capability——skills、slash commands、tools 是同一三层架构的表达；避免"已有 command 时重复创建 skill"**（统一模型面：Interface/Procedure/Capability 分层）。
- **提升层**：工作流 / 可复用 Skill。

### B3：skills.sh 百万规模与私有注册表 / Dify 模板市场 / GitHub 技能市场四层栈 / Hermes 自动写 skill（来源：vercel.com State of agent skills 2026-09-25 + localskills.sh 2026-07-06 + dify.ai Creator Center 2026-03-10 + agentconn.com 2026-09-01 + local-ai-models.ai CLAWS，实拉）
- **skills.sh 生态规模**：**七个月达到 100 万个 agent skills、近 2.8 亿次安装；skills CLI 开源（github.com/vercel-labs/skills）**（生态规模面：事实数字）。
- **私有技能注册表**：**团队内部 agent skills 的私有注册表——git/自托管/托管三选一，SSO/角色/审计日志；一次发布+版本化+决定谁可见**（内部技能分发面：一次发布版本化+可见性控制）。
- **Dify Creator Center & Template Marketplace（2026-03-10）**：**创作者发布 workflow 模板、用户发现并一键采用，可选 PartnerStack 联盟分佣**（模板市场+分佣面）。
- **GitHub 技能市场四层栈+Hermes 自动写 skill**：**四层栈：AI agents/agent skills/skills marketplace/claude code agent harness；Hermes Agent 复杂任务后自动写结构化 skill 文档、FTS5 over SQLite 全文本搜索所有过往会话、Tirith 预执行扫描**（生态栈+自动 skill 沉淀面：复杂任务后自动写 skill 文档）。
- **提升层**：工具 / 工作流。

### B4：Make 六步 agent 构建流程 / Claude Agent Skills 蓝皮书 / 提示词"指挥→委托"（来源：help.make.com Create your first AI agent 2026-07-20 + waytoagi.feishu.cn 蓝皮书 2026-09-27 + CSDN 2026-09-23，实拉）
- **Make 六步 agent 构建流程**：**规划 agent（做什么/工具/知识/触发器）→构建场景→配置 agent（理解职责）→加工具→加知识（额外上下文）→测试再上线**（构建流程面：先规划后配置、测试再上线）。
- **Claude Agent Skills 蓝皮书（WaytoAGI × 黄叔）**：**2026 年最值得投入的 AI 技能是 Skill；散落教程多、系统学习路径少——技能学习要成体系**（学习路径面：系统化技能学习）。
- **提示词工程范式转移（指挥→委托）**：**新一代模型下提示词工程从"指挥 AI"转向"委托 AI"——给目标与约束、让模型自主决策执行路径**（提示工程面：指挥→委托范式）。
- **提升层**：工作流 / 可复用 Skill。

## 判重说明
- B1 code-review-graph（爆炸半径 AST 图）与 r227-A qt-cpp-review（确定性 lint+并行 agent）不同面，各自独立；headroom SmartCrusher/CCR 为 wb-context-compressor 已有压缩方法的具体技术增量（重叠>60% 但含≥40% 独有技术）；continuous-learning-v2 instinct 演进全新；supabase-postgres 写前加载全新；落。
- B2 n8n Playbook（sub-workflows/会话 ID/自纠正 loop）、Context Engineering 四策略、Steering 七方法三维矩阵、三层统一模型均新面（r226-B n8n agentic 度分级互补不重复）；落。
- B3 skills.sh 规模数字为 r224 skills.sh 面的增量事实（合并保留增量）；私有注册表/模板市场/四层栈/Hermes 自动写 skill 新面；落。
- B4 Make 六步流程（与 r227-A Make 模型面互补，结构增量）；蓝皮书/指挥→委托为新面；落。
- 未落：Activepieces Agents 实体化与 AI Agent Builder（r226-C/r227-A 已覆盖）；deeplearning.ai 新课程列表（数量面，无方法增量）；WaytoAGI ICIO 框架（r224 已落同类）；Make 工具命名描述（与 Anthropic 工具写作五原则重叠）。
