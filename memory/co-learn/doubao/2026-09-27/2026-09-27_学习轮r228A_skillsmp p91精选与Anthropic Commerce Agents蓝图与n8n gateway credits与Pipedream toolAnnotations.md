# 学习轮 r228A：skillsmp p91精选与Anthropic Commerce Agents蓝图与n8n gateway credits与Pipedream toolAnnotations（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/91（total_length=9540 读满 9000，#9001-9093） | OK |
| 2 | Dify（blog/Human Input Node v1.13.0/Marketplace） | OK |
| 3 | n8n（Introducing Agents/gateway credits/70 MCP OAuth/2.40 release notes） | OK |
| 4 | LangFlow（Agentics bundle/Assistant 1.13/Code Agents） | OK |
| 5 | Activepieces（changelog 0.90.4/0.91.0/AI Agent Builder） | OK |
| 6 | Make（AI Toolkit/2026-09-25 release/AI Agent New app） | OK |
| 7 | Pipedream（MCP v2/toolAnnotations/Connect） | OK |
| 8 | Anthropic（Commerce Agents/Subagents vs Skills arXiv/Extension Layer Decision Guide） | OK |
| 9 | GitHub 生态与趋势（Github-Ranking-AI 2026-09-24 各榜） | OK |
| 10 | WaytoAGI（Skills 蓝皮书/飞书 AI Agent 节点/多维表格智能体/Lark CLI） | OK |

## 独点（4 个）
### A1：skillsmp p91 精选：持续教练模式 / 四角色 PRD 评审 / 软著四件套确定性校验（来源：skillsmp.com/skills/page/91，2026-09-27 实拉）
- **claude-coach 持续教练模式（alirezarezvani/claude-skills ★26,225）**：**首次触发"教用 Claude"后，每一后续轮次都检测遗漏的优化机会（模糊提示/被忽略的能力/可自动化的手工活），给出一条 power-user tip**——coaching 不是一次会话，是每次对话都检查"这次又错过了什么"（持续教练面）。
- **requirement-review 四角色 PRD 评审模拟器**：**模拟真实互联网公司需求评审会，从开发/设计/测试/业务四个角色视角对 PRD 全方位质疑和挑战**——在正式评审前发现盲区、补齐边界、强化论据（评审模拟面：与已有"拷问"类能力互补，区别是固定四角色视角）。
- **chinese-copyright-application 软著四件套（okooo5km/Skills4U ★185）**：**申请表 Markdown 输出+源程序/用户手册/设计说明书三份 LaTeX 编译 PDF；并做三项一致性校验——版本号一致性、模块覆盖双向核验、字数限制信息一致性**（合规生成面：确定性校验防返工）。
- **提升层**：工作流 / 可复用 Skill。

### A2：Anthropic Commerce Agents 蓝图与 Claude Code 扩展层决策图（来源：marktechpost 2026-09-03 + hidekazu-konishi.com 2026-09-25，实拉）
- **Commerce Agents 蓝图（Apache-2.0）**：**购物/商户 agent 的官方蓝图——四要素定义：prompts、skills、tool contracts、gates；commerce-builder 插件提供双命令：/scaffold-commerce-agent 脚手架新 agent、/review-… 审查现有 agent**（agent 蓝图面：先定义工具契约与门控再写 prompt）。
- **Claude Code 扩展层决策流程图（7 层）**：**扩展面含 CLAUDE.md/skills/subagents/hooks/MCP servers/plugins/settings；核心问题是"新自动化或知识该放哪层"——给出可复用决策流程图；错误放置的真实失败模式：被忽略指令/技能永不触发/上下文膨胀**（分层决策面：r227-B Steering 七方法管"怎么控制"，本条管"新东西放哪层"，互补）。
- **Subagents vs Agent Skills（arXiv 2609.09233）**：**subagents 能把单上下文最大信息量降下来，但现有 harness 的 subagents 普遍利用率低——多数场景下可复用技能比开 subagent 更省**（分工面：先试技能再开 subagent）。
- **提升层**：工作流 / 可复用 Skill。

### A3：n8n gateway credits 免注册试用 / Make token 统一与连接过滤 / Pipedream toolAnnotations（来源：blog.n8n.io 2026-09-17 + help.make.com 2026-09-21/25 + pipedream.com docs，实拉）
- **n8n gateway credits（2026-09-17）**：**免账号设置直接试用新模型和服务——支持节点上选 gateway credits 替代 credential**；70 个 MCP server 一键 OAuth 连接（2026-08-10）（模型试用面：把"新账户注册"从实验前置条件里去掉）。
- **Make AI Toolkit（2026-09-21）+2026-09-25 release**：**API tokens 与 MCP tokens 统一不再区分；新增连接过滤（connection filtering）与场景用量追踪（scenario usage tracking）**（工具治理面：连接白名单+用量可追踪）。
- **Pipedream MCP v2 toolAnnotations**：**10,000+ tools 全部带 toolAnnotations——read / write / destructive 三分类标注，帮 MCP 客户端理解工具类型；OAuth 认证+静态 URL+免预设置**（工具安全面：给模型侧提供"这工具是读还是写还是破坏性"的元数据，让客户端可据此限制调用）。
- **提升层**：工具 / 工作流。

### A4：Activepieces 审计与审批 / 飞书工作流 AI Agent 节点与多维表格智能体 / Langflow Assistant（来源：activepieces.com changelog 2026-09-14 + feishu.cn hc 2026-06-26/08-28 + docs.langflow.org 1.13，实拉）
- **Activepieces 0.91.0（2026-09-14）**：**agent 能力升级——flow step 集成+audit logs；0.90.4（09-08）flow approvals 审批**（治理面：agent 进 flow step 可审计可审批）。
- **飞书工作流 AI Agent 节点**：**自选大模型、具有记忆能力、基于对话内容和具体指令智能规划、自主调用工具（抽签、生成随机数等）完成复杂业务场景**；**多维表格智能体**：内置助手基于知识库问答+自动完成数据录入/查询/分析/流程触发（飞书生态面：表格内智能体=知识库问答+自动操作）。
- **Langflow Assistant（1.13 Next）**：**应用内虚拟助手面板，理解 Langflow 图结构，从自然语言构建完整 flows 或单个组件；每次发消息在服务器上运行一个内置 Langflow flow——该 flow 与画布上被编辑的 flow 相互独立**（架构面：助手本身也是 flow，与被编辑 flow 隔离）。
- **提升层**：工作流 / 工具。

## 判重说明
- A1 claude-coach 持续教练（每后续轮检测遗漏优化机会→单条 tip）与 r227-A think 10 阶段推理循环不同面（推理 vs 持续教练）；requirement-review 四角色模拟与 grill-me（拷问对齐）互补增量；软著三项一致性校验新；落。
- A2 Commerce Agents 蓝图（prompts/skills/tool contracts/gates 四要素+脚手架/审查双命令）新面；扩展层决策图（放哪层）为 r227-B Steering 七方法（怎么控制）的互补增量；subagent 利用率研究（先技能后 subagent）增量；落。
- A3 gateway credits 免注册试用、Make token 统一+连接过滤+用量追踪、Pipedream toolAnnotations 三分类均新面；落。
- A4 Activepieces audit logs/flow approvals 治理增量；飞书工作流 AI Agent 节点+多维表格智能体新面；Langflow Assistant 独立 flow 架构新；落。
- 未落：Dify Human Input Node（r225 HITL 概念已覆盖，无节点级细节增量）；GitHub 排名事实（已有落地）；Karpathy skills（r226-B 已落）；Skills 蓝皮书（r227-B 已落）；Lark CLI 开源（r225 已落 lark-cli 面）。
