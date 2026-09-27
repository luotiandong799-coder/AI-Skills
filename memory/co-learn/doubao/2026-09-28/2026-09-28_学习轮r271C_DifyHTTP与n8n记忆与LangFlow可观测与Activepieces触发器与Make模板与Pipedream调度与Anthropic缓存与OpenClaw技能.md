# r271C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表 170 词错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（HTTP 请求面） | ✓ | **HTTP Request 节点**（连接外部 API/web services——fetch data/send webhooks/upload files；全 HTTP 方法 GET/HEAD/POST/PUT/PATCH/DELETE；配置 auth/headers/query params/timeouts/body 用 workflow variables）；**安全**（请求全经 SSRF proxy service；敏感 API key 存环境变量不硬编码节点配置）；**模板变量插值**（{{ $vars.datasetId }} URL 构造）；**响应**（JSON/Text/raw 供后续节点） |
| 2 | n8n（AI agent 记忆面） | ✓ | **Memory sub-nodes 只挂 AI Agent root node**（n8n chain nodes 不支持 memory——要会话记忆必须用 agent 不用 chain）；**Tools Agent**（外部工具和 API 执行动作；理解工具能力决定用哪个；Langchain tool calling interface 描述工具和 schema；改进输出解析）；**记忆类型**（Simple Memory Window Buffer 最常见——存最近 N 条；database-backed：Postgres Chat Memory/Redis Chat Memory/MongoDB Chat Memory）；**上下文权衡**（太多 token 浪费+慢+混淆；太少决策缺信息）；**Manager Agent 案例**（Memory BufferWindow 连 ai_memory input）；**n8n vs LangGraph**（visual-first+Code node JS/Python+LangChain Code node 自定义 agentic） |
| 3 | LangFlow（可观测面） | ✓ | **Traces**（记录 flow/components 详细执行 trace——debug/latency/token usage 无需外部服务；trace+span 表存 Langflow DB；Flow Activity+Trace Details UI）；**Arize 集成**（OpenTelemetry+OpenInference；AX 托管云/enterprise；Phoenix 开源本地——UUID trace 是 Langflow components）；**Openlayer**（自动捕获：component hierarchy 父子/LangChain callbacks 嵌套 LLM 调用/timing/inputs outputs/user context/error tracking）；**Langfuse**（自动收集发送 trace——LLM observability 开源）；**flow 可作 MCP server 暴露**（Claude Code/Cursor/Desktop 把 flow 当工具） |
| 4 | Activepieces（触发器面） | ✓ | **触发器类型对比**（Polling：延迟 5-15 分钟/API calls 定期/简单/用户 setup 无；Webhook：即时/on event/setup 中等/用户注册；App Webhook：即时/on event/简单/平台处理）；**Polling 机制**（run 每 5 分钟——timestamp 范围或直到 last item id；返回新 items 数组；store 存 timestamp；默认 AP_TRIGGER_DEFAULT_POLL_INTERVAL=5）；**Worker 架构**（PollingJob——cron 默认每 5 分钟；load config→onEnable hook→fetch new items）；**超时**（AP_FLOW_TIMEOUT_SECONDS=600；AP_TRIGGER_TIMEOUT_SECONDS）；**Catch Webhook**（任意 HTTP method） |
| 5 | Make（模板/用例面） | ✓ | **AI 自动化示例**（新员工入职：Airtable watch→Slack welcome 触发 onboarding stage；7 个可复制 2026）；**模板场景**（废弃购物车恢复：Shopify Watch Events→Sleep 1h→检查订单→Klaviyo 恢复邮件带购物车物品；30 分钟 setup）；**Word 模板+OpenAI**（个性化客户提案：OpenAI 分析数据→填充 Word 模板；动态报告 AI 总结→格式化 Word；会议摘要转写；自动合同生成填充变量条款） |
| 6 | Pipedream（调度面） | ✓ | **schedule 定义**（intervalSeconds 秒频率/cron 自定义+timezone）；**Cron Scheduler 属性**（interval_seconds/cron string/timestamp/timezone_configured/timezone_utc）；**timer interface**（$.interface.timer default intervalSeconds——默认 15 分钟）；**Schedule source**（内置 Schedule app——每分钟到 1 年；cron 控制具体星期 '0 8 * * 1-5'；min 1-minute；2026-04 起所有 plans 含 free）；**执行限制**（HTTP/email-triggered 默认 30s；cron-triggered 默认 60s；paid 750s max） |
| 7 | Anthropic（缓存面） | ✓ | **Prompt caching**（cache_control 标记前缀——automatic caching 或 explicit breakpoints 5-min/1-hour TTL）；**定价**（base $5/MTok Opus 4.5；5m write $6.25 1.25x；1h write $10 2x；hits $0.50 0.1x；output $25）；**成本模型**（40-turn 任务首轮发 40 次——成本≈turn 平方增长；缓存不停止重发但每重发约 1/10 成本+更快：prefix 按 cache-read 率计费，每 turn 只为新内容付 1.25x write）；**实际节省**（最多 90% input 成本；latency 2x+ 改善；例 $720→$72）；**breakpoints 上限**（最多 4） |
| 8 | deeplearning.ai（RAG 课程面） | ✓ | **RAG 课程（Intermediate 26h3m Coursera）**（M1 RAG Overview——Andrew Ng 对话/架构；M2 检索技术：keyword/semantic/hybrid search、chunking、query parsing、ANN、vector databases、Weaviate API；M3 重排：cross-encoders/ColBERT/reranking；M4 LLMs：transformer/sampling/选 LLM/prompt engineering/hallucination 处理/评估/agentic RAG/RAG vs fine-tuning；M5 Production）；**组件化构建**（component-by-component 生产系统——非单一 demo；5 模块） |
| 9 | GitHub（RAG/知识图谱面） | ✓ | **框架对比**（Cognee：统一 graph+vector memory ECL pipeline——Neo4j/NetworkX/FalkorDB/Kuzu/Memgraph+多 vector adapters，Apache-2.0，native persistent agent memory；Letta：stateful agent memory in-context+external——archival vector search，long-running agents）；**RAGFlow 79.6k**（可视化 RAG+Agent 多模态）；**AnythingLLM 35k**（轻量 UI 上传即聊天）；**GraphRAG 34k**（Microsoft graph-based 复杂推理；nano-graphrag 简单 hackable 文件存储）；**LightRAG 36k**（HKU EMNLP 2025——知识图谱+vector 检索；incremental updates/multiple query modes/PostgreSQL/Neo4j/Milvus/Qdrant/ChromaDB/MongoDB/Faiss；dual-level keyword）；**AWS unified**（auto 策略 LLM router 每查询选） |
| 10 | OpenClaw（技能开发面） | ✓ | **技能创建**（SKILL.md bundle——YAML frontmatter 定义能力；~/.openclaw/workspace/skills/ 最高优先级；可问 agent 创建"创建技能检查 Todoist"——agent 生成文件；My skills 插件→个人 profile；无需 host shell 访问）；**结构**（SKILL.md 必需+tools/ 可选+skill.json/main.js 传统插件）；**技术栈**（skills 开发只需 Markdown/YAML/清晰技术写作——无需传统编程；plugin 需 JS/TS+Node；集成需 API literacy+脚本）；**分发**（ClawHub；Hub 激活即扩展无 coding）；**agent 定义**（system prompt 个性+skills+model preferences+behavior settings compaction/memory/limits；capabilities.agent.skills）；**指令质量**（instructions 必须 explicit/sequential/unambiguous——歧义导致不可预测行为） |

## 判重（双键检索结果）
- Dify HTTP 请求：库内已落 §节点聚合/§插件市场——全方法+SSRF proxy+模板变量插值为独有增量 ≥40% → 落地
- n8n AI agent 记忆：库内已落 §多 agent 编排/§子工作流——memory sub-nodes 只挂 AI Agent+Tools Agent+记忆类型为独有增量 ≥40% → 落地
- LangFlow 可观测：库内已落 §调试/§生产部署——Traces 表+Arise/Openlayer/Langfuse+flow 作 MCP 为独有增量 ≥40% → 落地
- Activepieces 触发器：库内已落 §触发器生命周期——三类型对比表+POLL_INTERVAL+PollingJob 为独有增量 ≥40% → 落地
- Make 模板：库内已落 §场景蓝图/§团队模板——AI 自动化示例+Word 模板集成=独有增量 ≥40% → 落地
- Pipedream 调度：库内已落 §触发器部署——schedule 定义+执行限制 30s/60s/750s 为独有增量 ≥40% → 落地
- Anthropic 缓存：库内已落 §缓存定价与盈亏平衡——自动缓存模式+40-turn 平方成本模型+90% 案例为独有增量 ≥40% → 落地（增量合并）
- deeplearning.ai RAG：库内已落 §RAG chunking 策略——课程五模块体系并入记录
- GitHub RAG/知识图谱：无 GraphRAG 章节——Cognee/Letta/RAGFlow/LightRAG 生态并入记录
- OpenClaw 技能开发：库内已落 §技能三目录/frontmatter——创建分发流程（My skills/ClawHub/无需编程）为独有增量 ≥40% → 落地（增量合并）

## 独点落地（8 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r271C-1 | wb-execute-discipline | 3.31.0+ | Dify HTTP Request 节点 | 工作流 |
| r271C-2 | wb-execute-discipline | 3.31.0+ | n8n AI Agent 记忆子节点 | 可复用 Skill |
| r271C-3 | wb-execute-discipline | 3.31.0+ | LangFlow Traces 与可观测集成 | 工具 |
| r271C-4 | wb-execute-discipline | 3.31.0+ | Activepieces 触发器三类型 | 工具 |
| r271C-5 | wb-execute-discipline | 3.31.0+ | Make 模板用例 | 可复用 Skill |
| r271C-6 | wb-execute-discipline | 3.31.0+ | Pipedream Schedule 与执行限制 | 工作流 |
| r271C-7 | wb-execute-discipline | 3.31.0+ | Anthropic Prompt Caching 自动模式与成本模型（增量合并 §缓存定价） | 可复用 Skill |
| r271C-8 | wb-execute-discipline | 3.31.0+ | OpenClaw 技能创建分发（增量合并 §技能目录） | 可复用 Skill |

## 复核
八独点均有当日实拉来源；均为增量合并或新面落地；并入记录：deeplearning.ai RAG 课程、GitHub RAG 生态。垃圾：本轮未产生临时文件。
