# r244-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（知识库/检索面） | ✓ | 检索双层过滤（knowledge base 层定初始结果池+knowledge retrieval node 层 rerank 收窄/重排——两个连续过滤器）；三种检索（Semantic 向量语义/Full-Text BM25 关键词精确匹配产品码 ID 快速可预测/Hybrid 语义+全文+reranker 最准但慢需 rerank 模型）；Weighted Score（semantic priority=1 vs keyword priority=1 vs custom weights）；Top K/Score Threshold 调参（初始 topK 3-4 threshold 0.5）；Metadata filtering 三级（Disabled/Manual 显式条件对象/Automatic LLM 从自然语言查询提取过滤条件）；Multimodal retrieval（VISION badge 多模态 embedding+rerank；图片 chunk 级管理：多模态模型图片向量化参与检索，文本模型图片仅附件随 chunk 返回） |
| 2 | n8n（数据转换/Code node 面） | ✓ | Code Node 契约（输入 [{json:{...}}] 输出必须同格式 return [{json:{...}}]；默认 JavaScript 不支持 require 除内置库不能装 npm 包）；$json.messages.toJsonString()（数组转合法 JSON 字符串内联）或 Raw/Custom body JSON.stringify；Code node 作安全网（parser 后校验 route 白名单不在 throw 阻塞下游）；n8n-nodes-json-parser 社区节点（从 AI 输出提取 JSON：Smart Detection/First-Last/All/Between Markers/Custom Regex）——AI 输出常在对话/代码块内嵌 JSON；Set(Edit Fields) JSON 模式（直接写完整输出 JSON 对象深结构快） |
| 3 | LangFlow（记忆/存储面） | ✓ | Memory bases（per-flow vector stores 自动摄取会话消息；跨 sessions 持久会话上下文区别于 session-scoped memory；agent 连 Memory Base 组件从向量库取上下文）；DB Providers（Settings→DB Providers 配置 Chroma 默认本地/Chroma Cloud/OpenSearch/Postgres pgvector；选定的 provider 应用于所有新建，已有的继续用创建时的 provider）；默认存储 SQLite（路径按系统）；Local DB 组件（Chroma DB 增强版 Ingest/Retrieve 两模式自动 collection 管理持久化 cache 目录） |
| 4 | Activepieces（部署/自托管面） | ✓ | 单容器部署（docker run -p 8080:80 -v ~/.activepieces；PGLITE/MEMORY 零配置；Kubernetes/Helm/Docker Compose）；生产形态（SANDBOX_CODE_ONLY+AP_REUSE_SANDBOX=true；one flow per worker 0.5vCPU/1GB）；规模公式（concurrency-1 worker busy 全程至 10min→按并发 flow 数定规模 workers=peak concurrent flows；apps=ceil(workers/10)；50 并发=50 workers 25vCPU/50GB+5 apps）；算术扩展（每 10 worker 加 1 app 1:10；80 workers/8 apps 484req/s→160 workers 777req/s）；worker/app 容器分离（AP_CONTAINER_TYPE=WORKER/APP 默认 WORKER_AND_APP） |
| 5 | Make（模板/场景市场面） | ✓ | Template Gallery（官方 make.com/en/templates 1000+ 预建场景；filter by app/category Sales/Marketing/Operations/AI；另一口径 7000+）；模板即完整场景（可用即用/编辑扩展/分享/复用）；Make Community（用户共享场景+讨论；Scenario of the Month 挑战赢 credits）；Make AI Playbook（88 use cases 按 team+AI maturity 组织，每个含问题/受众/影响/可部署场景） |
| 6 | Pipedream（触发器/调度面） | ✓ | 触发器四类（HTTP triggers/cron schedule triggers/email triggers/event sources 从 app 实时流事件）；组件部署（cron object：intervalSeconds 或 cron+timezone；$.interface.timer 声明）；10000+ prebuilt triggers and actions（public registry；deploy triggers 把 webhook 事件送到 app）；Schedule app（每分钟到每年；serverless 环境） |
| 7 | Anthropic（上下文工程面） | ✓ | Prompt caching 两种启用（Automatic caching 单 cache_control 顶层字段系统自动把 breakpoint 放最后 cacheable block 随对话推进 vs Explicit cache breakpoints 手动标最多 4 个）；成本（cached reads 10% base input price；5-min TTL 默认/1h extended；write multipliers 1.25x 5min/2x 1h；min 1024 tokens 内容在 breakpoint 前 512 for Fable 5 direct Bedrock 仍 1024）；KV+hash 不存 raw text（ZDR 合规）；breakpoint 位置（稳定内容边界，RAG 文档可更新而不失效工具/指令缓存）；Message Batches API（免 latency premium 异步批量处理）；Token counting（发送前测量请求 prompt bloat 构建时发现） |
| 8 | skills.sh（CLI/工具面） | ✓ | CLI 命令（npx skills find [query] [--owner]/add <package>/update/check/list ls）；@agentskill.sh/cli ags（search 100,000+ skills/install slug/install @owner/skill-name/list/update/remove/feedback 1-5 评分）；agent 路径映射（同 skill 自动落各 agent 目录：Cursor .agents/skills/ Claude .claude/skills/ 等） |
| 9 | OpenClaw（网关/部署面） | ✓ | Gateway 单一事实来源（会话/路由/渠道连接；单进程连 WhatsApp/Telegram/Discord/iMessage；扩展包加 Mattermost）；渠道三分类（Built-in：Discord/Google Chat/iMessage/IRC/Signal/Slack/Telegram/WebChat/WhatsApp；Bundled plugin：Feishu/LINE/Matrix/Mattermost/MS Teams/Nextcloud Talk/Nostr/QQ Bot/Synology Chat/Tlon/Twitch/Zalo/Zalo Personal；Optional：Voice Call/WeChat）；消息归一化（Maton Gateway 处理各平台认证 WhatsApp pairing/Telegram bot tokens/Slack OAuth→标准格式给 agent）；每代理/工作区/发送者隔离会话；发送接收图像/音频/文档；安装（macOS/Linux/WSL2 curl 脚本/Windows iwr） |
| 10 | GitHub（生态面） | ✓ | Agentic tooling 主导（builder 从 prompt wrappers 进 full agent infrastructure；BuilderIO/agent-native TS 框架 +607）；claude-code 146,377★（1,620 stars this week）；codex-chatgpt-web（ChatGPT Pro 作 Codex 原生模型 context/compaction/streaming/images/MCP tools）；Jev 决策插件（Claude Code plugin 替换 compaction summary——每个 tool call/result 一次快请求评分过时 drop/truncate 决策化 compaction）；OpenViking 38,699★（Self-evolving Context Database for AI Agents 统一 Agent Memory/Knowledge RAG/Skills）；vLLM Fast Start（GPU weight cache 跳过磁盘重启加载）；UI-TARS-desktop 39,113★（多模态 AI agent stack） |

## 判重基准
双键检索（相对 r241-r244B 已落章节）：Dify（r243-C 落 memory base 语义检索/r244-A 落四形态发布——"双层过滤+LLM 元数据过滤+多模态"独有增量深化）；n8n（r243-C 落 LLM 输出规范化/r244-A 落 parser/r244-B 落 webhook——"Code Node 契约+JSON parser 多提取法"独有增量深化）；LangFlow（r243-C 落 memory base 语义检索/r244-A 落 Extension/r244-B 落 API 流式——"per-flow 自动摄取+provider 时点绑定"独有增量深化）；Activepieces（r243-B 落 worker 扩展/r244-B 落模板库——"规模公式+容器分离"独有增量深化）；Make（r244-A 落 AI Toolkit/r244-B 落 Data Store——"模板 gallery+playbook 用例库"独有增量新面）；Pipedream（r244-A 落代码面/r244-B 落 Connect——"触发器四类+组件化 timer"独有增量新面）；Anthropic（r243-C 落 caching 成本模型/r244-A 落 hooks/r244-B 落工具合并——"automatic vs explicit 双模式+批量免延迟溢价+token counting"独有增量深化）；skills.sh（r244-B 落 Skill Packs——"CLI 命令面+路径映射"独有增量深化）；openclaw（r243-B 落 Gateway/r244-A 落 cron/r244-B 落 session hooks——"消息归一化+渠道三分类"独有增量深化）；GitHub（r243 落 MemOS/agentmemory/r244-A 落多模型编排/r244-B 落 ADE——"自进化 context db+决策化 compaction"独有增量深化）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 检索双层+三级过滤+多模态 | KB 层定池+node 层 rerank；LLM 元数据过滤；VISION 图片向量化 | 工作流/工具 | wb-execute-discipline |
| ② n8n Code Node 契约+JSON parser | 输入输出同构；社区 parser 多提取法 | 工作流 | wb-execute-discipline |
| ③ LangFlow Memory bases 摄取+Provider | per-flow 自动摄取；provider 时点绑定 | 工具 | wb-execute-discipline |
| ④ Anthropic Caching 双模式+批量 | automatic vs explicit；免延迟溢价；token counting | 工作流 | wb-execute-discipline |
| ⑤ OpenViking 自进化 Context DB | 统一 Memory/RAG/Skills；Jev 决策化 compaction | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
