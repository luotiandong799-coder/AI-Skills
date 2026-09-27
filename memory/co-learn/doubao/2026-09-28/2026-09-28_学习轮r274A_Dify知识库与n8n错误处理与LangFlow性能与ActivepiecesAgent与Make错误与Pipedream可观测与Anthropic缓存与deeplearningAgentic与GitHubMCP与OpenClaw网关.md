# r274A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（知识库管理面） | ✓ | **RAG 三步骤**（Retrieval——先检索知识库相关内容；Augmented——检索结果+用户 query 合成增强上下文；Generation——LLM 生成）；**知识库创建**（Knowledge→Create Knowledge；PDF/Word .docx/TXT/Markdown .md/HTML/CSV 多文件；自动 chunking/embedding/indexing）；**索引方法**（High quality；三种分段策略——paragraph/parent-child/QA）；**检索设置**（vector retrieval/rerank gte-rerank/Top K 3/Score Threshold）；**Multimodal retrieval**（Embedding 第一轮相似匹配+Reranking 评估 query-text-image 相关性）；**Summary Index（1.12.0）**（碎片检索问题——只返最相关单片段上下文不足；GraphRAG 重但实现复杂；每 chunk 附 summary 字段使语义相关内容一起检索——轻量替代）；**Knowledge Pipeline（1.16.0）**（Data Source→Data Processing（Extractor+Chunker）→KB Node（Chunk Structure+Retrieval Setting）→User Input→Test & Publish）；外部知识源 Notion/web pages |
| 2 | n8n（错误处理面） | ✓ | **两层错误处理**（node-level Retry On Fail（maxTries+wait）处理瞬时——网络抖动/429 多数就地；Error Trigger workflow 处理剩余——alerting/dead-letter/记录）；**Retry On Fail**（Max Tries 3+Wait 5000ms 静默重试全耗尽才失败）；**可复用 retry 模式**（Execute Workflow 调用——运行瞬时操作→分类→指数退避+抖动重试→最大次数停止→Slack/email alerts）；**LLM tool calling 错误处理**（可视化执行 trace——哪个 LLM tool call 失败/为何/尝试传什么参数——无重 DevOps 生产级可靠性）；**错误路由**（瞬时→retry 路径；其余→alert；Wait 2 分钟+HTTP POST REST API retry endpoint）；**错误工作流**（Error Trigger+Slack 每 workflow 设置；Set min(maxDelay, baseDelay×2^(attempt-1))）；**7 模式**（Continue on Fail 所有节点可开/Retry On Fail/Error Trigger） |
| 3 | LangFlow（Agent 组件/性能面） | ✓ | **Tool Mode**（组件头菜单启用——修改组件 inputs 变工具；Toolset 端口连 Agent Tools 端口；无按钮组件加 tool_mode=True input）；**Run Flow 组件作工具**（选 flow 启用 Tool Mode——flow 变 action）；**CUGA bundle**（lite_mode true 默认加速小工具集；lite_mode_tool_threshold 25 自动开 CugaLite；shortlisting_tool_threshold 35——超阈值启用 find_tools 过滤子集再决策——省 token）；**Code Agents**（input_value/llm 必填/tools 可选/max_iterations 默认 10 范围 1-100）；**Agentics**（aMap 随行数扩/aReduce 一次全发/aGenerate 随实例扩——小批或采样降本；batch 默认 10 max 25）；**多 agent 系统**（每节点混选模型——planning 小/检索工具友好/合成大）；**Scaling**（Uvicorn workers fork 继承预构建状态——只读内存页跨 30+ workers 共享；gc.freeze()）；**ALTK**（SPARC tool validation+JSON 智能后处理） |
| 4 | Activepieces（AI Agent 面） | ✓ | **Agent 构成**（instruction+允许的工具+知识；工具=任意集成/其他自动化/自己 MCP servers；知识=上传文件或保持更新的 tables）；**两限制**（run 间不记忆；无 SharePoint/Drive/Notion 实时同步）；**接入 workflow**（触发器+Agent step——填 input 告诉 agent 用触发数据做什么）；**触发**（webhooks/schedules/system events/manual runs）；**记忆三类型**（短时近期步骤/长时文档历史结果/用户记忆偏好）；**构建**（Agents→New Agent→name+description→instructions→Add Tool——From Piece 320+ 或 From Flow 转工具）；**构建块**（Agents/Flows/Tables/Apps 760+——agent 调 flow/flow 跑 agent/读写同一 tables）；**Human Review**（approval/manual-input 暂停 run 捕获编辑/确认）；**Tables**（prior prompts/entity IDs/validation flags——跨 run 复用历史避免重复） |
| 5 | Make（错误处理面） | ✓ | **Rollback handler**（停场景+回滚事务支持模块——mysql/data store；不能撤销非事务——gmail 发送/dropbox 删除；失败 bundle 不继续；history 标 error 但场景不禁用）；**Rollback 默认**（无 handler 或 incomplete executions 启用时——ACID 模块自动回滚）；**Break 指令**（生产最有用——失败送 Incomplete Executions 队列可自动重试而非丢弃；配重试次数）；**Commit**（错误保留之前工作只停本次——部分成功）；**Incomplete executions**（保存失败 blueprint+日志详情——settings/input/output 到失败模块——可调查可重跑；ConnectionError/RateLimitError 可 retry 同 settings）；**Throw**（条件抛错——JSON parse 可选抛 BundleValidationError 模拟）；**Rollback 适用**（多系统建单失败不想半建记录） |
| 6 | Pipedream（错误处理/可观测面） | ✓ | **maxRetries**（默认 10；超限进下一步；需异常处理 raise Exception）；**$errors channel**（subscription 订阅 workflow 全部错误不必逐个处理）；**$.flow.rerun**（try...catch 内重试失败 API 请求）；**执行日志**（每步 input/output/error state；失败事件单键 replay——API down 2h 50 webhook 失败全 replay 无数据丢失）；**Runs tab**（每 run 显示 payload/output/response；失败红标+错误消息；Settings>Notifications 错误邮件）；**SDK 自动重试**（指数退避默认 2 次；retryStatusCodes legacy）；**try/catch**（catch 块 $.send.http 或 fallback 告警）；**Python raise**（提前退出异常进 logs） |
| 7 | Anthropic（缓存/上下文工程面） | ✓ | **两种启用**（Automatic caching——顶层 cache_control 系统自动 breakpoint 到最后 cacheable block 随对话前移；Explicit breakpoints 手动）；**缓存内容**（稳定可复用——system instructions/背景/大上下文/频繁工具定义；放 prompt 开头最佳；breakpoint 分隔 prefix 段；**会话末尾+可编辑内容前设 breakpoint 最大化命中**）；**收益**（延迟降 80%/成本降 90%；默认 lifetime 5 分钟）；**Claude Code 经验**（用 messages 不用 system prompt 改动——plan mode/日期插 messages；**别中途换工具/模型**——用工具建模状态转换；延迟加载工具；**监控 cache hit rate 像监控 uptime**）；**滚动缓冲坑**（逐条剪除破坏缓存——**分批修剪**保持 prefix 字节相同几轮再一次性失效）；**immutable prefix pattern**（stable prefix system→tools→project instructions+growing tail conversation）；**缓存候选**（>2k tokens 每调用必发/RAG 稳定文档/多轮对话/批量文档分析/agent loops） |
| 8 | deeplearning（Agentic AI 面） | ✓ | **Agentic AI 四模式**（Reflection 自评迭代/ Tool Use 连数据库 API/ Planning 拆可执行步骤可适应/ Multi-Agent 多专用协调——Python 实践）；**AI Agents in LangGraph**（1h42m——LangGraph+Tavily agentic search 可控 agents）；**Long-Term Agentic Memory**（LangMem 记忆管理）；**crewAI**（3h2m——自然语言设计 agent 团队超单 LLM 提示）；**Agentic AI with LangChain/LangGraph**（memory/iteration/conditional logic；Reflection/Reflexion/ReAct；agent orchestration；agentic RAG 路由）；**高级模式**（conditional routing 按输出分支/critique loops Writer→Reviewer→Writer 带迭代计数/scatter-gather 扇出+reducer 合并）；**RAG 进阶**（Self-RAG/Corrective RAG/Adaptive RAG 超标准 RAG） |
| 9 | GitHub（MCP 生态面） | ✓ | **MCP 2026-07-28 规范**（stateless core——部署易扩展；Multi Round-Trip Requests；header-based routing；cacheable list results；authorization hardening；formal extensions framework；Tier 1 SDKs——最大版本）；**GitHub MCP Server**（2026-07-23 提前支持最新 spec；新工具管理 GitHub Projects）；**MCP Registry**（2026-07-27 preview——开放目录+API 提升可发现性；community-driven Anthropic-maintained app store；API freeze v0.1；支持 GitHub OAuth/OIDC/DNS/HTTP ownership verification）；**Copilot MCP**（扩展 Copilot 连数据源/工具） |
| 10 | OpenClaw（网关架构面） | ✓ | **Gateway 单源真相**（sessions/routing/channel connections；多通道单进程——Discord/iMessage/Signal/Slack/Telegram/WhatsApp/WebChat；插件通道 Matrix/Nostr/Twitch/Zalo）；**hub-and-spoke**（WebSocket 控制面 pub-sub——单控制点/统一 session 管理/无核心修改可扩展）；**协议**（text frames JSON payloads；首 frame connect；req/res/event 结构）；**消息路由**（channel adapter 归一化；pairing 新发送者配对码批准除非 open DM；session router 按 scope——main/per-peer/per-channel-peer/per-account-channel-peer；队列进 session lane）；**路由决策**（platform identity——Telegram vs Slack 不同处理；user/chat ID——work/personal 分离；映射 platform chat ID→session ID）；**节点**（macOS/iOS/Android/headless role: node+caps；每 host 一个 Gateway）；**MEMORY.md 跨 session 持久**；canvas host /__openclaw__/canvas/ |

## 判重（双键检索结果）
- Dify 知识库：库内 §RAG 检索（r268A）——Summary Index/Multimodal/Pipeline/三分段策略为独有增量 ≥40% → 落地（增量合并）
- n8n 错误处理：库内 §错误三模式（r270C）——两层架构/retry workflow/LLM trace/7 模式为独有增量 ≥40% → 落地（增量合并）
- LangFlow 性能：库内 §Tool Mode（r271A）——CUGA/Code Agents/Agentics/ALTK/Scaling 为独有增量 ≥40% → 落地
- Activepieces Agent：库内 §AgentBuilder（r267C）——构成三件套/两限制/记忆三类型/Human Review 为独有增量 ≥40% → 落地（增量合并）
- Make 错误处理：库内 §错误恢复（r269C）——Rollback 语义/Break 队列/Commit/Incomplete 重跑为独有增量 ≥40% → 落地（增量合并）
- Pipedream 错误处理：库内 §平台边界（r268C）——maxRetries/$errors/rerun/replay/SDK 退避为独有增量 ≥40% → 落地（增量合并）
- Anthropic 缓存：库内 §缓存经济（r268C）——automatic/explicit/Claude Code 经验/分批修剪/immutable prefix 为独有增量 ≥40% → 落地（增量合并）
- deeplearning Agentic：库内 §课程生态（r273A）——四模式/高级模式/RAG 进阶为独有增量 ≥40% → 落地
- GitHub MCP：库内 §GitHub MCP 生态（r272B）——2026-07-28 规范/Registry/Projects 工具为独有增量 ≥40% → 落地（增量合并）
- OpenClaw 网关：库内无 Gateway 路由专题——架构/路由/协议/配对为独有增量 → 落地

## 独点落地（10 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r274A-1 | wb-execute-discipline | 3.38.0+ | Dify 知识库管理进阶（Summary Index/Multimodal/Pipeline） | 可复用 Skill |
| r274A-2 | wb-execute-discipline | 3.38.0+ | n8n 错误处理两层架构与 retry 模式 | 工作流 |
| r274A-3 | wb-execute-discipline | 3.38.0+ | LangFlow Agent 性能优化（CUGA/ALTK/Scaling） | 工作流 |
| r274A-4 | wb-execute-discipline | 3.38.0+ | Activepieces AI Agent 构成与记忆 | 可复用 Skill |
| r274A-5 | wb-execute-discipline | 3.38.0+ | Make Rollback/Break/Incomplete Executions | 工作流 |
| r274A-6 | wb-execute-discipline | 3.38.0+ | Pipedream 错误处理与可观测 | 工作流 |
| r274A-7 | wb-execute-discipline | 3.38.0+ | Anthropic 缓存架构纪律 | 可复用 Skill |
| r274A-8 | wb-execute-discipline | 3.38.0+ | deeplearning Agentic AI 课程与高级模式 | 可复用 Skill |
| r274A-9 | wb-execute-discipline | 3.38.0+ | GitHub MCP 2026-07-28 规范与 Registry | 工具 |
| r274A-10 | wb-execute-discipline | 3.38.0+ | OpenClaw Gateway 架构与路由 | 工作流 |

## 复核
十独点均有当日实拉来源；均增量合并或新面；无并入未落地项。垃圾：本轮未产生临时文件。
