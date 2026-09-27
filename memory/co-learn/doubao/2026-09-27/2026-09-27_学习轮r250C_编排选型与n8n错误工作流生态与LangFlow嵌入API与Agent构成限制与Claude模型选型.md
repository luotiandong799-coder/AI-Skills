# r250-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（编排策略面） | ✓ | Agent 两核心策略（Function Calling：LLM 原生 tools 参数直传模型内置机制决定何时何法调用；ReAct：结构化提示 Thought→Action→Observation 显式推理步骤）；选型判据（FC 适合 GPT-4/Claude 3.5/GLM-4 等原生函数调用；ReAct 适合 Llama/Qwen/Mistral 7B 等开源无 FC——想看清完整推理也用 ReAct）；Nested agent nodes（v1.3+ 一个 agent 调用另一个为 tool——跨专业角色 emerging behavior）；Agentic RAG（Agent Node 决策引擎：intent analysis/tool orchestration/source selection/retry logic 封装全部 agent 行为）；固定流程用 Chatflow/Workflow（模型决定调哪个工具 vs workflow 固定顺序防随机变化）；混合检索+每数据集 score 阈值 |
| 2 | n8n（错误工作流面） | ✓ | Error Trigger 全局错误处理（workflow settings 指定 error workflow 任何执行失败触发；同一 error workflow 可服务多 workflow；以 Error Trigger 为第一节点）；捕获字段（workflow name/execution URL/last node executed/error message）；AI 诊断（LangChain Agent 深度分析 root cause/potential solutions/impact/urgency；Severity Level+Quick Resolution）；错误分类 7 型（Auth Error/Rate Limit/Network/Data Config/Not Found/Server Error/Permission；severity Critical/High/Medium；每类 suggested fix 如 "Re-authenticate credential for: [node name]"）；去重（LLM 分类→UNKNOWN fallback→dedup hash 分组相似错误→Jira 已开 issue append recurrence comment 否则新开 bug）；重试分级（retryable 408/409/425/429/500/502/503/504；not retried 400/401/403/404/422；backoff waitSeconds=min(maxDelay, baseDelay*…) +jitter）；ErrorLog/AuditLog Data Tables 中央日志 |
| 3 | LangFlow（嵌入/API 面） | ✓ | Embedded chat widget（最少输入 host_url HTTPS+flow_id；Share→Embed into site 复制 snippet 插 body；React/Angular/HTML 三形态）；API 触发（POST /api/v1/…；x-api-key header；input_value body）；OpenAI Responses API 兼容端点（POST /api/v1/responses；现有 OpenAI client 库只改 model 名即用）；react-native-langflow-chat（iOS/Android/Expo）；安全（Email Calendar 集成避免完整邮件 payload/机密数据只给摘要） |
| 4 | Activepieces（AI agent builder 面） | ✓ | Agent 构成（instruction+允许的 tools+knowledge；tools=任何集成/你的 automation/你的 MCP servers；knowledge=上传文件或保持更新 tables）；**两限制**（run 之间不记忆任何东西；无 SharePoint/Drive/Notion 实时同步）；New Agent 流程（name+description purpose/context→详细 instructions 做什么数据如何响应→Add Tool piece 500+ 集成或 flow 现有 workflow 成 tool）；Run Agent piece（复杂多步任务推理+准确用工具+迭代至完成）；测试 builder 内 plain language 输入/动作/结果 |
| 5 | Make（webhook 面） | ✓ | Custom webhook module（第三方服务调 unique webhook URL 触发 scenario；每 scenario 自己的 webhook 不能多 scenario 共用）；Webhook-triggered AI agent（数据发 webhook→agent 处理→回 webhook）；Mailhook（email webhook 新邮件即时触发非 schedule）；Webhook response 自定义响应 |
| 6 | Pipedream（Data Store 面） | ✓ | Data Stores=key-value store（跨 workflow run 管理状态；Node.js this.dataStore.set/get；Python pd.inputs["data_store"] 字典式）；TTL 可选（秒数到期自动删除；留空不过期）；容量（JSON-serializable strings/objects/arrays/dates/ints/floats；不能序列化 functions/classes；单 query 检索 10,000 keys/存 10,000）；用例（幂等键/滚动聚合/last-synced 时间戳——不立真数据库）；重型状态自备数据库（Postgres/MySQL/Supabase/MongoDB connectors）；$.service.db 组件专用 key-value 跨执行保状态 getters/setters 防 typo |
| 7 | Claude（模型对比面） | ✓ | Claude Opus 5（2026-07-24：Zapier automation bench 榜首不花更多 token；端到端 churn-prevention 序列）；Claude Sonnet 5（2026-06-30：agentic-coding 强模型 top-tier accuracy 可比 opus 级；比 Sonnet 4.6 step-function 提升）；模型矩阵（Opus 5.5 大多数负载起步/Fable 5.1 复杂推理长 agent 工作/Opus 4.6 1M context beta $5/$25 深度推理/Sonnet 4.6 1M $3/$15 最佳价值日常编码/Haiku 4.5 200K $1/$5 速度成本）；Claude Code 默认 Sonnet-4.6（研究：OPUS 4.8 高产量更好）；BenchLM 2026-07 Mythos 5 84.71 编码第二 |
| 8 | OpenClaw（安全/MCP 面） | ✓ | 最小权限（审查批准 MCP server 具体 actions；只请求 automation 需要的权限；可随时改）；MCP bridge permissions（permissions_list_open 列出 pending exec/Plugin approval；permissions_respond allow-once/allow-always/deny 三态）；Gateway 认证（bridge 认证用与远程 Gateway 客户端相同 token/password 控制；approval 状态 live/in-memory 仅当前 bridge session；messages_send 只能经已存 route）；cron/single-query contexts 默认拒绝需批准命令；非交互上下文可 auto-approve；Trust boundary（Gateway-owned authority；sandbox/node/cloud-worker execution；**sandboxing off by default**）；MCP server 安全（pre-audited configs/automated scanning/continuous monitoring） |
| 9 | GitHub MCP（tools 面） | ✓ | Projects tools（projects_list/projects_get/projects_write 统一项目管理）；OAuth scope filtering（2026-01-28 changelog）；Remote GitHub MCP server（GitHub 托管最易起步；不支持 remote 用本地 binary）；覆盖面（repo browsing/issue PR/code search/Actions inspection/security-alert triage；agentic PR review/issue triage/CI failure 调查）；生态（github-mcp-server 90k stars 2026-09；2026 最常装 MCP server；modelcontextprotocol/servers 87.3k stars；n8n-mcp 21.8k stars；Glama/LobeHub 多实现） |
| 10 | deeplearning.ai（community/课程面） | ✓ | 2026 新课程（Building Adaptive AI Agents 8-26/Evaluating AI Agents 6-1/Build Interactive Agents with Generative UI/Agent Skills with Anthropic Elie Schoppik：skills=instructions 文件夹扩展 agent 能力一次构建跨 skills-compatible agent 部署/Spec-Driven Development with Coding Agents/Agent Memory: Building Memory-Aware Agents/Multi-vector Image Retrieval）；Agentic AI 完整课 9h55m（Degrees of autonomy/Task decomposition）；RAG 完整课 26h3m（生产级从架构到部署评估）；学习方法（Pomodoro 25+5；参与社区论坛；主动学习记笔记总结教别人应用） |

## 判重基准
双键检索（相对 r224-r250B 已落章节）：Dify（r224-r250B 已落知识库/变量/检索/编排——FC vs ReAct 选型判据+nested agent v1.3+ 互调+Agentic RAG 决策引擎为独有增量）；n8n（r226 错误处理四型——Error Trigger 全局工作流生态+7 型分类+dedup hash+重试状态码分级为独有增量）；LangFlow（r250-B 模板复用——chat widget 嵌入 host_url/flow_id+OpenAI Responses API 兼容端点为独有新面）；Activepieces（r250-B webhook 契约——agent 构成 instruction/tools/knowledge+run 间无记忆+无 Notion 实时同步限制为独有增量）；Claude（r249-A hooks/r250-A 安全/r250-B headless——2026 模型矩阵 Opus 5.5/Fable 5.1/Sonnet 5 为独有新面）。未选素材：OpenClaw security（r244 defineToolPlugin 契约已落，permissions 三态与 Claude Code 安全互补但增量弱）；GitHub MCP（r249-C 已落 51 tools/OAuth scope filtering；projects 新工具集增量弱）；Pipedream Data Store（r248 DataStore 持久化已落，TTL 增量弱）；Make webhook（r226 webhook 响应选型已落）；deeplearning.ai（课程列表与用户学习偏好重叠，独有知识增量弱）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 编排选型 | FC vs ReAct 判据+nested agent+Agentic RAG | 工具/工作流 | wb-execute-discipline |
| ② n8n 错误工作流生态 | 全局 Error Trigger+分类去重+重试分级 | 工作流/可复用 Skill | wb-execute-discipline |
| ③ LangFlow 嵌入与 API 触发 | chat widget+Responses 兼容端点 | 工作流 | wb-execute-discipline |
| ④ Agent 构成与限制 | instruction+knowledge+run 间无记忆 | 工具 | wb-execute-discipline |
| ⑤ Claude 模型选型纪律 | 2026 模型矩阵+负载匹配 | 模型 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
