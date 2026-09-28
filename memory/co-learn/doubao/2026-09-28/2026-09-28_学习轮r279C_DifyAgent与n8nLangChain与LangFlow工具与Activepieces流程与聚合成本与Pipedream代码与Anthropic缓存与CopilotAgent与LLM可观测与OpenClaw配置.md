# r279C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r279A/r279B/r278/r277/r276 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（Agent 节点） | OK | Agent node 给 LLM 自主工具控制（迭代决定用哪个工具）；Agent Strategy=可扩展模板定义标准化输入/输出（CoT/ToT/GoT/BoT）；Function Calling（GPT-4o/Claude）vs ReAct（无原生函数调用模型）；Allowed tools list（只发送/运行列出工具、空=全列表）；嵌套 agent 节点（v1.3+ 一个 agent 调另一个作 tool）；MCP 集成（SSE 插件动态发现外部工具、MCP Agent Strategy 嵌入 Agent 节点）；v1.6.0 双向 MCP（agent 运行时选工具、分诊三个专业化 agent） |
| 2 | n8n（LangChain 集成） | OK | AI nodes 实现 LangChain JS 框架（可选 agent/LLM/memory 组件）；LangChain Code node（自托管 only、粒度控制 prompts、省 token）；Conversation Agent 内建；SQL Agent type（SQLite）；MCP Trigger/toolWorkflow/agent 节点；Langfuse tracing（自定义 LLM 配 callbacks）；vs LangGraph（1000+ connectors、per-node execution history/OpenTelemetry、encrypted credentials 不给 agent 访问） |
| 3 | LangFlow（agent 工具） | OK | Agent 组件可用任何组件作 tool（含其他 agent 和 MCP servers）——启用 Tool Mode 挂到 Tools 端口；自定义组件 Python（langflow.custom Component/io MessageTextInput/Output/schema Data）；Code Agents（max_iterations 默认 10 范围 1-100）；MCP filesystem server（AI coding agent）；CUGA（browser automation Playwright+structured output）；LangChain bundle（LLM Math/NL2SQL/Retrieval QA/Self Query/JSON Agent/VectorStoreRouterAgent）；Agentics bundle（aMap/aReduce/aGenerate 表格变换）；Langflow Assistant（自然语言构建 flow/组件、内置 flow 运行） |
| 4 | Activepieces（流程控制） | OK | 逻辑块直接放主 flow（Branches/loops/delay 可视）；Router Executor（表达式条件分支 router-executor.ts）；Branch Action（if/else conditions firstValue）；ap_add_branch MCP 工具（加条件分支、插 fallback 前）；loopActions 循环；内建 assistant（英文描述→建议步骤/写自定义块代码）；Test 按钮；分支 flow vs 条件逻辑（条件=底层规则、分支=结构结果）；版本系统（lock/publish 草稿） |
| 5 | Make（data store 聚合） | OK | 本站搜索命中 Google Datastore/Firestore/Doris/MongoDB 聚合（非 Make 特有）；可内化=write-time vs read-time 聚合成本权衡（文档少 read-time 便宜、量大 write-time 便宜）；Datastore 聚合查询 count/sum/avg（省取实体成本）；Doris 聚合模型预聚合（导入/合并阶段预聚合、只存聚合结果）；Firebase 事务内维护 numRatings/avgRating |
| 6 | Pipedream（code steps） | OK | Node.js（defineComponent async run({steps,$})、$.export 导出、props 传参——仅 Node 支持 props）；Python（def handler(pd)、pd.steps["trigger"]、返回 dict）；Golang/Bash；连接账号到 code step（Node/Python 用 connected accounts 做 HTTP、catch errors/retries/多 API 请求单步）；$.service.db（source 开发存状态）；npm 包直接导入 |
| 7 | Anthropic（提示缓存） | OK | 两法：automatic（顶层 cache_control）+ 手动 breakpoints（cache_control: {"type":"ephemeral"}）；定价：写缓存比基础输入价贵 25%、用缓存内容仅 10% 基础输入价（如 Opus 4.8 input $5/MTok、cache write $6.25、cache read $0.50）；大幅降重复上下文延迟成本；成本优化组合（缓存+Batch API+监控 token 用量）；rate limits 按 tier |
| 8 | GitHub Copilot（agent mode） | OK | agent 模式=自主实时同步协作者（自然语言多步编码任务）；能力：分析 codebase 全上下文、计划并执行多步方案、运行命令/测试、调外部工具、迭代到完成；与 coding agent 区别（coding agent=后台异步、agent mode=编辑器内实时流式、watch steps/intervene/keep local）；Tools→Manage 开关能力；terminal 命令需确认 |
| 9 | LLM 可观测工具 | OK | MLflow（端到端 GenAI 生命周期、OpenTelemetry-compatible、30M+ 月下载）；LangSmith（LangChain 团队、agent debugging/observability/evals、专家标注 traces）；Arize Phoenix（RAG 调试、OpenInference=OpenTelemetry 标准、开源自托管、trace-style+evals、CI dual-mode）；Langfuse（自托管、observability+prompt mgmt、ClickHouse-native）；Opik（Apache-2.0 开源、20k+ stars、LLM-as-a-judge、production monitoring）；Helicone（低延迟代理+观测/缓存）；AgentOps（自主 agent 监控）；选型（LangSmith 全面/Langfuse 自托管/Helicone 低延迟） |
| 10 | OpenClaw（配置/agent/channels） | OK | 单主配置文件 config.yaml（gateway、channels WhatsApp/Telegram/Discord/Slack+15+、providers Anthropic/OpenAI/Gemini/DeepSeek/Ollama、agents、memory、advanced）；agent 字段（model/system_prompt/channels [terminal] 默认/memory.backend sqlite/redis）；多 agent 路由（agents.list+bindings 匹配 channel/account/peer→agent；agentToAgent 默认关+allow 白名单）；channel 配置（telegram dmPolicy pairing/allowlist/open/disabled、whatsapp allowFrom/groups requireMention、discord mediaMaxMb 8/allowBots false/actions 门）；broadcast groups（strategy parallel、群/号码→agents）；subagents（allowAgents/delegationMode prefer/requireAgentId、tools profile minimal） |

## 判重（双键检索，增量判定）
- Dify Agent（r279A 分块/r279B 环境变量/r278A 混合检索）→ 新面（Agent 节点/策略）
- n8n LangChain（r279A 错误/r279B 秘密/r278B 数据转换）→ 新面（AI 节点/LangChain Code）
- LangFlow agent（r279A 记忆/r279B API/r278B 向量存储）→ 新面（Tool Mode/Code Agents）
- Activepieces 流程（r279A 触发器/r279B AI/r278C 嵌入）→ 新面（router/branch/loop）
- 聚合成本（r279A webhook/r279B 调试/r278B 数据存储）→ 新面（write-time vs read-time）
- Pipedream code（r279A 调度/r279B 安全/r278C CLI）→ 新面（code steps 运行时）
- Anthropic 缓存（r279A 结构化/r279B 思考/r278A 缓存已落但本面=定价机制）→ 增量合并（缓存定价/自动缓存）
- Copilot agent（r279A 技能市场/r279B Models/r278B Copilot 已落但本面=agent mode）→ 增量合并（agent mode）
- LLM 可观测（r279A 评估/r279B 多代理）→ 新面（工具全景/选型）
- OpenClaw 配置（r279A 会话/r279B 开发/r278C 多代理已落但本面=配置路由）→ 增量合并（config.yaml/bindings）

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify Agent 节点与策略 | 工具 |
| 2 | n8n LangChain 集成 | 工具 |
| 3 | LangFlow agent 工具 | 工具 |
| 4 | Activepieces 流程控制 | 工具 |
| 5 | 聚合查询成本权衡 | 工作流 |
| 6 | Pipedream code steps | 工具 |
| 7 | Anthropic 提示缓存定价 | 工具 |
| 8 | Copilot agent mode | 工具 |
| 9 | LLM 可观测工具全景 | 可复用 Skill |
| 10 | OpenClaw 配置与多 agent 路由 | 可复用 Skill |

## 复核
十独点均有当日实拉来源；均新面或增量合并；无纯重复。版本建议 3.55.0+。