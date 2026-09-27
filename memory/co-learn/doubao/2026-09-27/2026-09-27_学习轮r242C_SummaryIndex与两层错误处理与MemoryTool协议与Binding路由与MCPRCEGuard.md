# r242-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（知识库/RAG 面） | ✓ | Retrieval Modes 选型（N-to-1 多知识库合并结果推荐大多数场景/Multi-path 每库分别检索适合并行）；Summary Index 1.12（比 GraphRAG 轻量——每 chunk 附 summary 字段使语义相关内容一起检索，summary 匹配则共享 summary 的所有 chunks 一起返回）；Child Chunks 检索钩子（Parent-child 模式搜 child 返 parent，child 可当 parent 语义标签/检索提示，重写 child 不影响 parent）；chunk 质量纪律（完整句子逻辑段落边界/避免跨层级标题断裂/预留 5% 上下文余量/清洁源文档去 header footer 页码导航/metadata 过滤）；chunk 参数（自动按段落标题多数情况/技术密集 800 tokens+150 overlap） |
| 2 | n8n（错误处理/生产面） | ✓ | 两层错误处理（node-level Retry On Fail maxTries+wait 网络抖动 429 就地重试 + Error Trigger workflow 报警/dead-letter/记录失败）；Continue on Fail + $error 字段（单失败请求不杀整执行，$error 供下节点判断重试或继续）；AI 分类重试（Gemini/Anthropic 分类 transient/permanent/needs_human→仅瞬态指数退避重试→非重试/预算耗尽 Google Sheets dead-letter 注册表夜间重放）；错误分类 7 型（Auth/Rate Limit/Network/Data-Config/Not Found/Server Error/Permission）；监控排除自身执行防告警循环 |
| 3 | LangFlow（RAG/agent 面） | ✓ | RAG 管线组件链（Text Splitter→Embeddings→Vector Store pgvector/Pinecone/Chroma/Astra DB/Weaviate；查询 embed→similarity→可选 rerank→Prompt Template 插上下文→LLM→Chat Output）；Retriever subflow 范式（chat input→embed→向量搜索→解析上下文→LLM 生成，工具 web search+datetime）；Vector Store RAG 模板两 subflow（Load Data 加载+Retriever 检索，换库只换组件对） |
| 4 | Activepieces（错误/监控面） | ✓ | retries exponential backoff + circuit breakers + DLQ（死信队列溢出）；request-response pairs/metrics/alerts；run log 单压缩 checkpoint 文件（一步一条按 step name 键控 input secrets hidden/output/status——fresh worker 恢复一切）；run 状态存 Tables（结构化记录查重/去重/run-state 跟踪/增量处理跨系统）；重试安全（job 超时重试后 workflow 安全跳过已应用副作用） |
| 5 | Make（函数/聚合面） | ✓ | Functions app 独立模块化（IML 函数之前只在 mapping fields 现在变 standalone modules 链式组合可视数据变换工作流复杂逻辑易读易维护）；新函数 arraydiff/arrayintersect/set/escapejson（数组比较/更新集合/准备 raw JSON 少模块）；Aggregator 类型（Array 多 bundle 合成数组/Text 文本连接指定分隔符/Numeric sum average max min）；空输入行为（input 空/null/missing 输出空结果不停止 scenario） |
| 6 | Pipedream（代码/调试面） | ✓ | Build with AI 三按钮（Edit with AI builder header 改整个 workflow/Code step Edit with AI 改单步骤/Debug with AI 步骤结果遇错 AI 调试辅助）；Error Handling 设置（error notifications 连续 N 次错误后通知设 1 立即告警）；静默失败比嘈杂更糟（catch block 返回 fallback object status unknown+generic message + $.send.http 或 Slack 告警）；pd_sdk_debug=true 调试标志看工具调用 API 调用 |
| 7 | Anthropic（context engineering 面） | ✓ | Context Engineering 范式（从一次性 Prompt 到生命周期 Context；"optimizing the utility of tokens against the inherent constraints of LLMs" be informative yet tight）；Memory Tool 协议（模型通过持久文件目录跨会话存/取；auto-injected system prompt check-memory-first："ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE... Your context window might be reset at any moment" client-side API 给协议+工具 schema 应用实现）；Context editing（接近 token 上限自动清 stale tool calls and results 保持对话流）；工具响应上限 25,000 tokens（pagination/range/filter/truncation 默认）；Prompt caching 1 小时 TTL Bedrock（5 分钟→1 小时长 agent 成本效率）；80% prompt cut |
| 8 | skills.sh（技能发现面） | ✓ | find-skills 类别→查询词映射（Web Development react/nextjs/typescript/css/tailwind；Testing jest/playwright/e2e；DevOps deploy/docker/kubernetes/ci-cd；Documentation docs/readme/changelog/api-docs；Code Quality review/lint/refactor/best-practices；Design ui/ux/design-system/accessibility）；91,000+ skills indexed/385,000+ 总安装追踪；找不到技能应对策略（先广后窄/换同义词/搜作者）；find-skills 94.1K 装机量榜首 |
| 9 | docs.openclaw.ai（多 agent 路由/记忆面） | ✓ | Binding 路由架构（agent=完整 per-persona scope workspace 文件/agentDir/模型注册/session store；binding 映射 channel account Slack workspace/WhatsApp 号→agent；入站消息经 binding 路由）；Session Router（Gateway 收 Message→Session Router 按 Message Session Key 路由到某 agent session；每 agent 至少一个 main session）；ACP 协议 v4.2（Agent Communication Protocol 跨 agent 通信；thread-bound persistent sessions；sessions_spawn 委托任务/sessions_send 直接通信）；Cloud session（普通 session 编码工作在另一台机器跑；Gateway 保持对话/workspace/模型凭证所有权；session 与持久状态远程失败后存活；reclaimed/suspended workers 下条消息重启） |
| 10 | GitHub（生态面） | ✓ | MCP RCE Guard（Layer-3 RCE 防御 MCP servers 策略合成——从声明语义合成 per-tool 策略执行时强制；关闭 sidecar scanners mcp-armor/stdio wrappers mcp-stdio-shellguard 抓不到的 tool-injection-RCE 类）；SDL-MCP（Symbol Delta Ledger cards-first context 系统给 coding agents 省 token 改善上下文）；mastra 28.3k★（现代 TypeScript AI 应用/agents 框架）；budibase 28.3k★（AI agents/automations/apps model agnostic）；RAGFlow（开源 RAG 引擎融合 RAG+Agent 创建 LLM 上下文层）；memwyre（MCP-native 持久记忆层混合向量+BM25+cross-encoder 73.1% LoCoMo 跨 Claude Code/Cursor/VS Code/OpenClaw）；wassette（安全 runtime 通过 MCP 运行 WebAssembly 组件） |

## 判重基准
双键检索（相对 r241-A/B/C 已落章节 + r242-A/B 本批）：Dify（r241-C 落过分块三策略——"Summary Index+Child Chunks 钩子"独有增量深化）；n8n（r241-A 落过错误五型——"两层错误处理+AI 分类三分+dead-letter 重放"独有增量深化）；LangFlow（r241-C 落过检索四层——"Retriever subflow 范式+双 subflow 模板"独有增量深化）；Activepieces（r242-B 落过 durable execution——"熔断+DLQ+run log 单文件"独有增量深化）；Make（r241-B 落过聚合器——"functions 模块化+空输入行为"独有增量深化）；Pipedream（r241-A 落过错误五型——"静默失败纪律+阈值告警"独有增量深化）；Anthropic（r240 落过上下文工程四件套——"Memory Tool check-memory-first+工具响应上限"独有增量深化）；skills.sh（r242-A 落过 CLI 命令矩阵——"类别映射+找不到应对"独有增量）；openclaw（r242-A 落过多通道共享——"binding 路由+ACP+cloud session"独有增量深化）；GitHub（r241-C 落过 MCP 面——"RCE Guard 策略合成"独有增量深化）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify Summary Index+Child Chunks 钩子 | 每 chunk 附 summary 同语义一起检索轻量图；搜 child 返 parent 重写 child 不影响 parent | 工作流 | wb-execute-discipline |
| ② n8n 两层错误处理+AI 分类三分 | node Retry On Fail 就地+Error Trigger 报警；transient/permanent/needs_human→dead-letter 重放 | 工作流 | wb-execute-discipline |
| ③ Anthropic Memory Tool check-memory-first | 上下文随时重置必须先看记忆目录；工具响应上限 25k tokens | 工作流/可复用 Skill | wb-execute-discipline |
| ④ OpenClaw Binding 路由+ACP+cloud session | channel→agent 映射隔离；sessions_spawn/sessions_send；远程执行所有权归 Gateway | 工作流 | wb-execute-discipline |
| ⑤ GitHub MCP RCE Guard 策略合成 | 从声明语义合成 per-tool 策略执行时强制防 tool-injection-RCE | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
