# r273B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（Agent/工具面） | ✓ | **Agent 节点**（模型需支持 function calling 若用该策略）；**工具配置三要素**（Authorization——API keys/credentials workspace；Description——清晰说明工具做什么何时用引导 Agent 决策；Parameters——必需/可选输入带验证）；**Instructions and Context**（自然语言定义角色/目标/上下文）；**工具集成**（内置 Wikipedia/Google/Brave Search；自定义 API——OpenAPI/Swagger 与 OpenAI Plugin 标准 tweak API 匹配；MCP 工具/HTTP 请求/沙箱代码；插件市场 Firecrawl/Tavily）；**Agent Strategy Plugin 四参数**（model/tools/query/maximum_iterations——防过度计算）；工作流节点类型（推理检索/控制流/执行/人工审核） |
| 2 | n8n（AI Agent/向量库面） | ✓ | **Vector DB 选型**（Pinecone/Qdrant/Weaviate/Supabase 原生；in-memory simple starter 模板；cluster 节点架构秒换 embedding 模型）；**Upstash Vector Store**（AI Companion Node——插 AI Agent/Q&A Chain/Vector Store Tool；Server-Side Auto-Embeddings 免单独 embedding key；SQL-like metadata filters）；**AI Agent memory**（memory sub-nodes 保持/检索对话历史；Chat Memory Manager 高级——check size/clear entries；每 AI Agent 节点一个 memory sub-node）；**RAG 模板**（Supabase Storage sync→chat；PostgreSQL→Pinecone schema auto-discovery；Claude+Supabase+Postgres memory） |
| 3 | LangFlow（会话/Playground/工具面） | ✓ | **内置 chat memory**（Agent 组件默认——rolling context window per session ID；自定义 session ID 隔离用户/应用）；**Message History 组件**（组合 chat history+storage；Langflow storage 或 Mem0/Redis）；**Memory Bases**（1.10+——per-flow 向量存储自动 ingest 会话消息跨会话语义检索——"remember what we discussed last week"）；**Playground**（不同输入响应/审查修改 memories；**Agent 逻辑审查**——打印 agent 用过的 tools+每 tool 输出）；**REST API**（flows/upload POST；flows/{id}/run；/stream SSE；/info）；**工具集**（Data Loaders/ComponentToolkit——任何组件 wrap 成 LangChain Tool）；**LFX API**（/flows/upload /run /stream /info） |
| 4 | Activepieces（webhook/重试面） | ✓ | **Webhook 安全重试**（幂等键+correlation IDs 存 Tables 查重后短路重复 run；条件分支+backoff——瞬时失败重试不重复处理）；**签名验证**（payload 加 schema version 按版本路由；每版本转换步骤；旧路由保持到迁移完）；**并发管理**（project 上限——达限新 run 排队+指数退避；**不丢弃**最终执行）；**错误处理**（Continue on Failure/Retry on Failure）；**WebhookHandshakeStrategy**（NONE 默认/HEADER_PRESENT/QUERY_PRESENT/BODY_PARAM_PRESENT）；**API 自动化**（exponential backoff/circuit breakers/DLQs/按 status code 分支/throttle+幂等键）；**breaking change**（/sync webhook 失败曾 hold 30 秒才 408 空 body——现 FAILED 立即返回终态）；**Worker 架构**（defaultJobOptions attempts 3/backoff exponential delay 1000/removeOnComplete age 3600/removeOnFail 7 天；EXECUTE_VALIDATION；delayed jobs=paused/upcoming polling/retrying） |
| 5 | Make（调度面） | ✓ | **Schedule 选项**（At regular intervals/Once/Every day/Days of week/Monthly/Specified dates/On demand/**Immediately**——数据到达立即执行；每 15 分钟默认；免费最小 15 分钟，付费到 1 分钟）；**Immediately+webhook 队列**（最大 run/分钟 1-100）；**Data Processing**（Sequential 顺序/Parallel 并行——付费；Priority execution Pro+）；**Polling vs Instant**（Polling 每 X 分钟查新数据——Gmail/RSS/表格；Webhook 事件即时——表单/Stripe）；**Run once 测试**（每模块变绿） |
| 6 | Pipedream（npm/内置面） | ✓ | **npm 直接 import**（默认无包安装——import axios 部署时自动下载最新 bundle；无 package.json/npm install）；**@pipedream/browsers**（导出 puppeteer & playwright 同接口——browser(opts?)）；**platform axios 优势**（自动管理凭据/错误处理）；**managed auth**（3,000+ apps OAuth/key-based）；**async 坑**（大多 Node 包返回 Promises——axios 不加 await 不发送）；**组件**（Node.js modules 跑 serverless；无 npm install；import 在顶部） |
| 7 | Anthropic（Message Batches 面） | ✓ | **Batches API**（多条 Messages 请求异步；创建即处理；最多 24 小时但多数 1 小时内；**50% 折扣**；最多 10,000 queries/batch；免管队列/rate limits）；**状态**（EndedAt 全部 succeeded/errored/canceled/expired 才算结束；ExpiresAt=创建后 24 小时；过期未完成即失效）；**轮询**（GET /v1/messages/batches/{id} 幂等；results_url 取结果；结果可用 29 天）；**适用**（customer feedback 分析/翻译——无需实时） |
| 8 | deeplearning.ai（RAG 课程面） | ✓ | **RAG 课程**（Intermediate 26h3m 5 模块——Module 1 Overview/Andrew Ng 对话/RAG 架构；搜索技术+向量库——keyword/semantic/hybrid/chunking/query parsing；Prompt design+评估+部署；跨域 healthcare/e-commerce；Coursera 免费旁听）；**RAG Specialization**（LangChain/LlamaIndex/FAISS/Chroma DB——advanced retrieval/vector DBs/retriever 选型到接口） |
| 9 | GitHub（Copilot coding agent 面） | ✓ | **Coding agent**（自主处理低-中复杂度任务——review repo 上下文含 issues/PR discussions/custom instructions；修复 bug/增量特性/重构/测试/文档/secret scanning/技术债；**PR 需 human approval 后 CI 才跑**）；**内置安全检查**（code scanning/secret scanning/dependency vulnerability 直接 workflow 内——CVE/疑似 API key 在 PR 打开前标记）；**Copilot app**（agent-native；**每 session 独立 git worktree**——真实隔离副本并行不互扰；app 管 worktree）；**agent skills 文件**（markdown 教专门工作流；live 在 .github/skills/、~/.copilot/skills/、.agents/skills/——相关时自动加载）；**skills vs custom agents vs instructions**（agents 定义 persona+tool set；instructions 一般偏好；skills 任务特定自动发现） |
| 10 | OpenClaw（技能编写面） | ✓ | **SKILL.md 格式**（唯一硬要求；YAML frontmatter+Markdown 指令；最少 name+description——name slug 小写字母数字连字符，description 一行显示 agent/发现结果——**最重要**写清触发条件）；**可选 frontmatter**（user-invocable true 默认 slash 命令；disable-model-invocation false 默认——true 时从 system prompt 排除仍可 /skill；command-dispatch tool——slash 直连工具绕过模型；command-arg-mode raw）；**requires 块**（bins [jq, ripgrep]/env [LOG_SERVICE_PATH]/config）；**最佳实践**（Be concise——教做什么不教怎么当 AI；Clear Triggers——"当用户问 X 时用此技能"；Safety——exec/bash 防注入；Test locally——openclaw agent --message 测试；Modularity——单域专注）；**标准**（遵循 AgentSkills spec——agentskills.io） |

## 判重（双键检索结果）
- Dify Agent 工具配置：库内 §Agent 节点（r270A）——工具配置三要素/插件四参数/自定义工具标准为独有增量 ≥40% → 落地（增量合并）
- n8n AI Agent 向量库：库内 §记忆四类（r266A）——Vector DB 选型/Upstash auto-embeddings/Chat Memory Manager/RAG 模板为独有增量 ≥40% → 落地
- LangFlow 会话：库内 §记忆（r268A）——Memory Bases/Playground 打印工具使用/Message History/LFX API 为独有增量 ≥40% → 落地（增量合并）
- Activepieces webhook 重试：库内 §认证（r270C）——幂等+签名版本路由/并发队列/Worker 参数/HandshakeStrategy 为独有增量 ≥40% → 落地
- Make 调度：库内 §调度（r271B）——Immediately 队列限速/顺序-并行处理/Priority 为独有增量 ≥40% → 落地（增量合并）
- Pipedream 内置包：库内 §npm 导入（r272A）——browsers/managed auth/async 坑为独有增量 ≥40% → 落地（增量合并）
- Anthropic Message Batches：库内无批处理章节——新面 → 落地
- deeplearning RAG 课程：库内 §RAG chunking（r270C）——课程路线并入记录不落地（技术面已覆盖）
- GitHub Copilot coding agent：库内 §GitHub 生态（r273A）——coding agent/内置扫描/worktree/skills 位置为独有增量 ≥40% → 落地
- OpenClaw 技能编写：库内 §技能创建分发（r271C）——frontmatter 细节/AgentSkills spec/最佳实践为独有增量 ≥40% → 落地（增量合并）

## 独点落地（9 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r273B-1 | wb-execute-discipline | 3.36.0+ | Dify Agent 工具配置与插件参数 | 可复用 Skill |
| r273B-2 | wb-execute-discipline | 3.36.0+ | n8n AI Agent 向量库与记忆进阶 | 工作流 |
| r273B-3 | wb-execute-discipline | 3.36.0+ | LangFlow Memory Bases 与 Playground 审查 | 工作流 |
| r273B-4 | wb-execute-discipline | 3.36.0+ | Activepieces Webhook 幂等与重试策略 | 工作流 |
| r273B-5 | wb-execute-discipline | 3.36.0+ | Make 调度队列与顺序/并行处理 | 工作流 |
| r273B-6 | wb-execute-discipline | 3.36.0+ | Pipedream 内置包与浏览器自动化 | 工具 |
| r273B-7 | wb-execute-discipline | 3.36.0+ | Anthropic Message Batches 批处理 | 可复用 Skill |
| r273B-8 | wb-execute-discipline | 3.36.0+ | GitHub Copilot coding agent 工作流 | 工具 |
| r273B-9 | wb-execute-discipline | 3.36.0+ | OpenClaw SKILL.md 编写规范 | 可复用 Skill |

## 复核
九独点均有当日实拉来源；均增量合并或新面；并入记录：deeplearning RAG 课程。垃圾：本轮未产生临时文件。
