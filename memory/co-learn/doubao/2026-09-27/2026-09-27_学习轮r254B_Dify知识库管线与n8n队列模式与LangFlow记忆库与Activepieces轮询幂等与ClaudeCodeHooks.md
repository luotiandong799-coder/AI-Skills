# r254-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（知识库管线面） | ✓ | 五段管线：数据源（文件/在线文档/云盘/爬虫）→提取（文本/表格/图片/扫描件）→处理（分块/增强/清洗/代码）→存储（向量/全文/元数据/图片）→检索（语义/关键词/混合/重排）；每知识库独立分块/索引/检索/精炼策略；分块按文档类型匹配；自动分段+自动清洗（rules JSON）；自定义：高密度技术文档 800 tokens chunk+150 overlap；清洗去重复 header/footer/页码/导航菜单噪音；元数据过滤 tag（product: billing/type: FAQ）只检索子集；父子模式 hierarchical_model（父分段挂子分段，API 更新分段重触发索引）；TopK 召回；用固定代表性问题测试分块对比；Markdown Text Chunker 插件保留标题层级+上下文元数据 |
| 2 | n8n（queue mode 面） | ✓ | Queue mode：main 实例处理 timers+webhooks 生成（不运行）执行 → 传 execution ID 给 Redis（BullMQ job queue）→ 下一个可用 worker 拉取执行；EXECUTIONS_MODE=queue 在 main+每个 worker 设置；共享同一 Redis+同一 Postgres+同一 N8N_ENCRYPTION_KEY；worker 并发 n8n worker --concurrency=5（默认 10）；docker compose up -d --scale n8n-worker=N 横向扩展；组件典型：main 1/worker 2-10+/Redis 1/PostgreSQL 1；workers 忙时 job 在队列等待无执行丢失；OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS=true 手动执行跑 worker；所有 worker 共享加密密钥才能解密凭据 |
| 3 | LangFlow（memory bases 面） | ✓ | Memory Base：per-flow vector store 自动摄取对话消息，跨会话语义检索（嵌入向量按语义相似度返回最相关上下文）；vs Message History（chronological 取最近）；vs Knowledge Base（手动填充）；1.10：Assistant 构建整个 flow+Memory bases+DB Providers（可配置向量数据库后端）+七语言；1.8：知识库=本地向量数据库（数据不用每次 run 从远端取回重摄取）+Guardrails 组件（LLM prompt 校验 flow）+Agentics bundle（LLM 填充/折叠/生成表格数据）；1.11：Multi-Vector Retrieval lfx-nextplaid（ColBERT-style late interaction+ColPali 视觉文档检索，零胶水代码）；判据：跨会话连续性"记得上周讨论的"→Memory Base；仅会话内→标准 chat buffer |
| 4 | Activepieces（polling 面） | ✓ | Polling Trigger：On Enable 存 last state；Run 每 5 分钟按 timestamp 或 last item id 遍历，返回新 items 数组；DedupeStrategy.TIMEBASED（timestamp 检测）/LAST_ID（last item ID 之后）；run 返回数组（单 polling 多 triggers 每个 item 触发 flow）；事件幂等：Tables 存 unique event key，每 run 开始检查已处理短路；idempotency keys+correlation IDs 检测重复；条件分支+backoff 瞬时失败重试不重复处理；数据同步防重复：source record IDs+updated-at+operation type 组合确保一次应用；DLQ 处理 rate limit 溢出 |
| 5 | Make（webhook 面） | ✓ | 关键发现：Custom Webhook 不暴露 raw request body（解析 JSON 后才可访问）——HMAC 需要 raw bytes 不能原生在场景内做 → Cloudflare Worker 前置验签只转发成功；Stripe 验证算法 HMAC-SHA256(secret, timestamp+"."+raw_body)（t=+v1= 提取）；Meta webhook：场景返回 ONLY raw hub.challenge（无引号无 JSON wrapper），Webhook Response header text/plain 3 秒内响应；安全建议：X-Webhook-Token secret token 比较/优先 HMAC/只接受 POST+验证 Content-Type/按 event ID 幂等 dedupe；Custom Webhook 模块生成唯一 URL，每场景独立不能共用 |
| 6 | Pipedream（AI gateway/MCP 面） | ✓ | 集成层：managed auth+10,000+ prebuilt tools/triggers+raw proxy；MCP servers for agents：一个 MCP endpoint 给 agent 10,000+ tools（remote server tool discovery+per-user auth，任何 MCP client）；Conduit：gateway 员工安全连接 apps 到 AI agents（SSO/access policies/per-user permissions/full audit trail）；单 MCP server 暴露整个集成目录（3,000+ apps 10,000+ tools）managed OAuth；Queues+private networking 内置；每步任意 Node/Python（npm install @anthropic-ai/sdk 即"add Claude"） |
| 7 | Claude Code（hooks 面） | ✓ | Hook 事件表：PreToolUse（工具调用前，可阻塞可修改）/PostToolUse（工具结果后，审计）/PostToolUseFailure（失败处理）/PostToolBatch（整批工具调用解析后，每批一次注入约定）/PermissionRequest（需权限决策）/PermissionDenied（自动模式拒绝，含无 classifier 判定，hookSpecificOutput.retry:true 告诉模型可重试，无判定时忽略 retry）；matcher：Bash/Edit/Write/Read/Glob/Grep/Agent/WebFetch/WebSearch/MCP 工具名；settings.json 配置 hooks；permissionDecision deny+reason；SDK hooks（Python+TS 拦截控制 agent 行为） |
| 8 | GitHub（awesome agentic 列表面） | ✓ | awesome-agents（kyrolabs）+Awesome-AI-Agents（jenqyang）+awesome-agentic-ai（学习路线图/框架/工具/实例）；awesome-ai-agents-2026：340+ agents/20+ 分类；新仓库信号：ReviewCerberus（免费开源 AI code review git 分支差异）、Sugar（持久任务队列+TDD+agent 路由）、BidClub（agents 与人类平等分享研究）、Yoyo（agent 社交网络 MCP 连接）；DarkMoon（MCP host 编排 80+ 攻防工具）、Atomic Agent（本地 CLI 56 内置工具免账号）；microsoft/autogen 59K/github/awesome-copilot 35.1K/composiohq/composio 28.8K |
| 9 | OpenClaw（memory 面） | ✓ | 记忆=写普通 Markdown 文件到 agent workspace（默认 ~/.openclaw/workspace）；模型只记住存盘的内容，无隐藏状态；MEMORY.md=长期知识（持久真理/学习偏好/项目上下文/关键事实）+memory/YYYY-MM-DD.md 每日日志；memory-wiki 插件（2026.4.7）：把持久知识编译成 wiki 存档——确定性页面结构/结构化 claims+evidence/矛盾与陈旧监控/dashboard/五工具（wiki_status 等）；对比：向量嵌入 vs 结构化文档（语义搜索 vs 分类+链接；自动提取 vs 主动创建；审计弱 vs 强）；适合运维 runbook/API 文档；MIND=个人知识图谱插件（11 tools/4 skills）；ontology Skill 结构化记忆 |
| 10 | ModelScope/Qwen（agent 面） | ✓ | Agents-A1（InternScience 35B MoE）：agentic reasoning 分解任务/规划/适应中间结果；原生 function calling+工具集成（API/code interpreter/search）；长视界研究；ModelScope-Agent 框架（MSAgent-Bench 微调 LLaMA/Qwen/ChatPLUG）；Qwen-AgentWorld：语言世界模型（环境建模=训练目标 CPT→SFT→RL；七域单模型：文本 MCP/Search/Terminal/SWE+GUI Web/OS/Android）；Qwen3.7-Max：35 小时全自主 kernel 优化 1000+ tool calls；Qwen3.8-Omni-Flash 插件：omni-skill-creator（把教学视频/录屏/操作演示转成可复用 Agent Skill.md 文件）+omni-memory（长视频人物/对话/声音/事件记忆）；Qwen3.6-Plus 1M context 默认 |

## 判重基准
双键检索：Dify（r253-A 多路召回=检索面——本轮知识库管线/分块/清洗面独有）；n8n（r254-A error/r253 多面——queue mode 横向扩展面独有）；LangFlow（r253-A/B/C 部署/widget/A2A/r254-A lfx——Memory Bases 语义长期记忆+multi-vector 增量≥40%）；Activepieces（r253-C Tables 游标 delta——polling dedupe 策略+幂等键增量≥40% 可合并）；Make（r254-A data store——webhook raw body 限制+前置验签新发现）；Pipedream（r254-A CLI/r253-B REST——MCP gateway+Conduit 面）；Claude Code（r252-A 相关面——hooks 事件契约完整面，新）；OpenClaw（r253-A skills——memory-wiki 结构化记忆新面）；ModelScope（r252-C 微调/数据集——agent 模型+omni-skill-creator 新面）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 知识库管线与分块 | 五段管线+分块策略+清洗+元数据过滤+父子模式 | 工作流 | wb-execute-discipline |
| ② n8n Queue Mode 横向扩展 | main+Redis+workers+共享密钥+并发调优 | 工作流 | wb-execute-discipline |
| ③ LangFlow Memory Bases 与多向量 | per-flow 语义长期记忆+DB Providers+ColBERT/ColPali | 工作流 | wb-execute-discipline |
| ④ Activepieces Polling 与事件幂等 | DedupeStrategy+unique key 短路+幂等键+DLQ | 工作流 | wb-execute-discipline |
| ⑤ Claude Code Hooks 事件契约 | PreToolUse 可阻塞+PermissionDenied retry+matcher | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 备选未落：Make webhook raw body 前置验签/OpenClaw memory-wiki/Pipedream MCP gateway/omni-skill-creator（留痕存档后续批次再判）。
- 垃圾：本轮未产生临时文件。
