# r273A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（Variable Aggregator 面） | ✓ | **Variable Aggregator**（原 Variable Assigner）——聚合互斥分支到单一输出；If/Else/Question Classifier 创建互斥分支（每 run 只一路执行）避免下游重复节点；**array 模式**收集所有分支输出为列表再 Code 处理；并行分支（两 LLM 同时调用）合并；DSL 结构（groups/group_name/output_type/variables/value_selector）；Workflow Major Update：Iteration/Parameter Extractor/Publish Workflow as a Tool |
| 2 | n8n（HTTP Request/Code/Sub-workflow 面） | ✓ | **HTTP Request 节点**（REST API 查询；参数配置或 **Import curl**——解析 method/URL/headers/query/body；Import 全变 string 的坑；附 AI agent 当工具）；**Execute Sub-workflow**（host 跑另一工作流；From list/Workflow ID——URL /workflow/ 含 ID）；**Code 节点两 Mode**（Run Once for All Items——$input.all() 一次处理整包 vs Run Once for Each Item）；n8n 配置（workflow concurrency max/http maxSockets） |
| 3 | LangFlow（子流程/向量库面） | ✓ | **Vector Store RAG 模板双 subflow**（Load Data 加载嵌入内容入向量库/Retriever 按查询向量搜索；Load Data 与 Retriever 分离因为不需每次跑）；Chat Input 收 Playground 用户输入；**Knowledge Base**（向量数据库存 embeddings；默认 Chroma 本地，可配 Chroma Cloud/OpenSearch/Postgres pgvector；不每次 flow run 重新 ingest——更高效；与 memory bases 共享 DB Providers） |
| 4 | Activepieces（pieces 开发面） | ✓ | **Trigger 三技术**（Polling 周期调用端点查变化/Webhooks 单 URL 听用户事件/App Webhooks Subscriptions 用 developer app）；**CLI 脚手架**（npm run cli pieces create 三问——Piece Name/package name/type community；actions create；triggers create——folder/display/description/technique）；**Piece 定义**（createPiece({name/displayName/actions/triggers})；createAction({name/displayName/run})）；**CI/CD**（AP_API_KEY；离线开发；package.json 升版本；PR 合并后 CLI 或 GitHub Action 同步）；**MCP 工具**（ap_run_action 单次执行 piece action 不建 flow——one-shot；ap_research_pieces 发现） |
| 5 | Make（Router/过滤器面） | ✓ | **Router**（原生工具分场景到多模块链；每条 route 按条件处理数据不同；Filters 定条件——less than/greater than 等；路由排序+**fallback route** 处理不适合其他 route 的数据——fallback 也能设 filter；应用例：咨询按类型路由不同团队 Slack）；添加 Router 默认两条路径 + 按钮加更多；**Router 之后部分模块不执行的坑**（conditional true 仍不执行——需 blueprint 排查）；Blueprint 导出不含连接私钥；AI agent 创建（plan→build→configure job/tools/knowledge→test） |
| 6 | Pipedream（Connect SDK/HTTP 面） | ✓ | **Connect SDK**（@pipedream/sdk；PipedreamClient({clientId/clientSecret/projectId/projectEnvironment})；tokens.create({externalUserId}) 创建 connect token；用于任何 Node.js 框架 Express/Next.js/Fastify/Hono；浏览器用法）；**SDK 自动刷新 access tokens+invoke workflows**；**远程 MCP**（client.connect({url remote.mcp.pipedream.net, headers x-pd-external-user-id})——agent 选工具 auth 已处理；callTool slack-send-message）；**HTTP/Webhook trigger**（唯一 URL 每请求运行）；**HTTP Request Action**（Postman 式；连接 account 自动配置 authorization headers——Slack Bearer）；**HTTP Destinations**（发数据到外部 endpoint）；**Python pd.respond()**（返回响应——至少 body）；**Connect API**（TS/Python/Java SDK+REST；api.pipedream.com/v1/connect/{project_id}） |
| 7 | Anthropic（Agent SDK/工具循环面） | ✓ | **Agent SDK**（Claude Code as library——Python/TS；同样 agent loop/context management/tools/permissions/sessions/hooks；query() 主入口创建 agentic loop 返回 async iterator 流消息）；**Tool Runner**（定义每工具为函数传 tool_runner()；内建错误封装/结果格式化/会话管理；每 iteration 查 Claude 是否要 tool use 自动跑送回；break 随时结束；循环到无 tool use 或 max_iterations）；**Client SDK vs Agent SDK**（Client 自己实现 tool loop；Agent SDK Claude 处理）；**server-side tools**（web_search/web_fetch/code_execution/tool_search——Claude 决定何时搜索；一次请求多次搜索；最终响应带 cited sources；你从不构造 tool_result）；**tool-runner takeover**（接管 iteration 时 runner 不 append assistant message/tool results——自己负责 conversation 合法性；max_iterations 绑定） |
| 8 | deeplearning.ai（课程清单面） | ✓ | **新课程**（Evaluating AI Agents Arize 2h16m/2h36m——15 视频/6 code/1 graded；Building and Evaluating Data Agents Snowflake 1h59m——Data Agent/Multi-Agent Workflow/Expand Capabilities/Observe Performance/Measure GPA；AI Code Review 2026-09-14 新）；**Agentic AI 结构**（Module 2 Reflection Design Pattern——improving outputs；Module 4 Practical Tips——evals/error analysis/component-level evals；9h55m）；**课程生态**（Voice for AI Agents/AI Coding Workflows/RFT GRPO/Fast LLM Inference/On-Device AI/Prompt Engineering Llama2/Generative UI/AutoGen/LLMOPs Automated Testing/Pydantic/DSPy/Spec-Driven/Multi-vector IR） |
| 9 | GitHub（awesome-agent-skills 面） | ✓ | **awesome-agent-skills（VoltAgent）**（1,400+/1,500+ agent skills 精选目录；聚合官方定义——Anthropic/Google/Stripe/Cloudflare+社区；跨 Claude Code/Cursor/Copilot/Gemini CLI；31.8k★/3.4k forks）；**Copilot agent skills**（官方支持创建/共享——anthropics/skills+github/awesome-copilot；gh skill CLI 发现）；**awesome_ai_agents（jim-schwoebel）**（1,500+ agents）；**awesome-agents（kyrolabs）**；**ComposioHQ/awesome-claude-skills**（最大 Claude skills 列表）；**生态链接**（skills.sh/agentskills.io/skillrepo.dev/skillmd/mdskills）；**Addy Osmani agent-skills**（20 production-grade 工作流——Define/Plan/Build/Verify/Review/Ship）；**korchasa awesome-ai-agents**（React Doctor/flow 21k★/AgentGPT 36k★）；**agency-agents 140k★**（每 agent 专家各有性格/流程/deliverables）；**MetaGPT**（multi-agent orchestration） |
| 10 | OpenClaw（CLI/配置/桌面面） | ✓ | **CLI onboarding**（macOS/Linux/WSL2/原生 Windows；openclaw setup 同一流程；Quick start 检测 AI 可用性/选连接/真实 completion 验证/开 web dashboard）；**后台服务**（macOS LaunchAgent 需登录会话，headless 用 LaunchDaemon；Linux/WSL2 systemd user unit——loginctl enable-linger 注销后继续；原生 Windows Scheduled Task 优先拒绝则 fallback）；**macOS 权限**（Desktop/Documents/Downloads 文件权限——挂起需授权同一进程上下文；Computer Control 分别查 Accessibility/Event Posting/Screen Recording——TCC 独立桶；Exec approvals system.run 存 ~/.openclaw/exec-approvals.json——Security/ask/allowlist）；**Full Disk Access**（运行进程需全盘访问——Terminal/VS Code/iTerm；授权后重启 gateway）；**approvals CLI**（openclaw approvals set --node --stdin JSON——defaultAction deny+rules 白名单） |

## 判重（双键检索结果）
- Dify Variable Aggregator：库内 §Dify 节点聚合（r269B）——array 模式/DSL/并行合并/更名史/Major Update 为独有增量 ≥40% → 落地（增量合并）
- n8n HTTP/Code/Sub-workflow：库内无 HTTP Request 三节点专题——Import cURL/两 Mode/Execute Sub-workflow 为独有增量 → 落地
- LangFlow 子流程/Knowledge Base：库内 §LangFlow 记忆（r268A）——双 subflow RAG 模式/KB 概念/外部 provider 为独有增量 ≥40% → 落地（增量合并）
- Activepieces pieces 开发：库内 §Code Step（r271B）/§MCP（r272C）——Trigger 三技术/CLI 脚手架/Piece 结构/CI-CD/ap_run_action 为独有增量 ≥40% → 落地
- Make Router：库内 §Make 蓝图（r272C）——Router+fallback/路由排序/不执行坑为独有增量 ≥40% → 落地
- Pipedream Connect SDK：库内 §组件（r271A）——Connect SDK/远程 MCP/HTTP Action 自动 auth/pd.respond 为独有增量 ≥40% → 落地
- Anthropic Agent SDK：库内 §工具循环（r271A）——Agent SDK/Tool Runner/server-side tools/takeover 为独有增量 ≥40% → 落地（增量合并）
- deeplearning 课程：库内 §评估（r271B）——Reflection 模式/GPA 测量/新课程生态为独有增量 ≥40% → 落地（增量合并）
- GitHub awesome-agent-skills：库内 §GitHub 生态（r272B 并入）——awesome-agent-skills 仓库/Copilot skills/Addy Osmani 20 工作流为独有增量 ≥40% → 落地
- OpenClaw CLI 权限：库内 §沙箱（r272B）/§信任边界（r270B）——CLI onboarding/后台服务/TCC 三桶/Full Disk Access/approvals JSON 为独有增量 ≥40% → 落地（增量合并）

## 独点落地（10 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r273A-1 | wb-execute-discipline | 3.35.0+ | Dify Variable Aggregator 聚合互斥分支 | 工作流 |
| r273A-2 | wb-execute-discipline | 3.35.0+ | n8n HTTP Request/Code/Sub-workflow 三节点 | 工具 |
| r273A-3 | wb-execute-discipline | 3.35.0+ | LangFlow 双 subflow RAG 与 Knowledge Base | 工作流 |
| r273A-4 | wb-execute-discipline | 3.35.0+ | Activepieces pieces 开发 CLI 与 Trigger 三技术 | 可复用 Skill |
| r273A-5 | wb-execute-discipline | 3.35.0+ | Make Router 分支与 fallback | 工作流 |
| r273A-6 | wb-execute-discipline | 3.35.0+ | Pipedream Connect SDK 与远程 MCP | 工具 |
| r273A-7 | wb-execute-discipline | 3.35.0+ | Anthropic Agent SDK 与 Tool Runner | 可复用 Skill |
| r273A-8 | wb-execute-discipline | 3.35.0+ | deeplearning Reflection 模式与课程生态 | 可复用 Skill |
| r273A-9 | wb-execute-discipline | 3.35.0+ | GitHub awesome-agent-skills 生态 | 可复用 Skill |
| r273A-10 | wb-execute-discipline | 3.35.0+ | OpenClaw CLI 权限与后台服务 | 可复用 Skill |

## 复核
十独点均有当日实拉来源；均为增量合并或新面落地；无并入未落地项。垃圾：本轮未产生临时文件。
