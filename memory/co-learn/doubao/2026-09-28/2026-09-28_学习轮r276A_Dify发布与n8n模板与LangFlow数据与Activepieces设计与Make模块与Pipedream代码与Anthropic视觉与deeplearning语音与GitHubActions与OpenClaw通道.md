# r276A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（发布嵌入面） | ✓ | **发布 7 种方式**（hosted WebApp/API endpoints/embeds/MCP-compatible tools/工具引用/MCP 服务端/Chrome 扩展/iframe+script 嵌入）；**iframe 嵌入**（<iframe src="https://udify.app/chatbot/YOUR_APP_TOKEN" width="100%" height="600" frameborder="0">——始终可见/全功能/可定制）；**script 嵌入**（脚本标签——浮动 widget 按钮/自定义 UI）；**Pre-Fill Hidden Fields**（发布面板 Web App 区 Embedded > Pre-Fill Hidden Fields——填入值烘焙进 iframe URL 和 script snippet 的 inputs 对象——每位访问者自己的值：登录用户 ID/所在页面）；**三种嵌入**（iframe/浮动 widget 按钮/custom UI）；**API 自动**（每 app 自动 REST API——API Reference 拿 key——n8n/Zapier 调用） |
| 2 | n8n（模板社区面） | ✓ | **模板库规模**（Support 888 workflows/AI RAG 712/AI Chatbot 1269——分类浏览）；**RAG Starter Template**（Simple Vector Stores+Form trigger+OpenAI——PDF 自定义知识——给 Agent 知识）；**模板实践**（lead follow-up: Webhook→normalize→validate email→append Sheets→Gmail→Slack→log failures；Stripe Payment→Fulfillment→Receipt；Form→Sheets+Slack——clean commented JSON import-ready）；**自托管 AI 模板无 API key**（AI Blog Writer 4 阶段 research/outline/draft/edit；Social Media Generator；YouTube-to-Newsletter；Competitor Intelligence Monitor；Email Auto-Responder）；**WhatsApp AI 销售助手**（结构化 system prompt：一次一个问题/不编价格/不编链接；外部文本文件动态定价查询） |
| 3 | LangFlow（数据组件面） | ✓ | **SQL Database 组件**（SQLAlchemy 兼容数据库执行 SQL——PostgreSQL/MySQL/SQLite——CQL 走 DataStax bundle）；**自然语言查数据库**（SQL Database+Agent 组件改造支持 NL 查询）；**BigQuery 组件**（Google bundle——参数化 SQL 查询公开数据集——结果流入 DataFrame Operations/Parser 转文本/结构化供 LLM）；**SQL Agent（LangChain bundle）**（基于 Agent core——参数 llm/database/top_k——SELECT 返回行数）；**DataStax Astra DB CQL**（CQL 表查询——输出 JSON 对象列表——projection fields——number_of_results）；**IBM Db2 Vector Store**（DB2VS 实例读写——远程 enterprise-grade）；**RFM 客户分层模板**（agent 详细指令 RFM Recency/Frequency/Monetary+人口统计——完整数据库 schema——执行 SQL 返回结构化分析建议） |
| 4 | Activepieces（工作流设计面） | ✓ | **最佳实践清单**（描述性命名 flows/steps；发布前测试；用文件夹组织；error handling 分支+失败通知；复杂步骤加 notes；定期检查执行日志）；**构建原则**（先简单——增量构建每步测过再加下一步——真实数据测试再发布）；**Router 条件**（+ 添加条件分支——过滤发送者/主题/文件类型/前序数据——每分支独立 actions——避免一开始建不必要分支）；**AI-powered inbound lead 流**（Netlify 表单→Perplexity 研究→Claude 评分优先级→Claude 标记 spam→Gmail 自动回复→Sheets 日志→Slack 通知）；**跨系统流**（emails/chats/documents/forms/events/webhooks 触发——AI steps 摘要/提取/分类——凭据加密+data masking）；**MCP flows 模板**（Airtable MCP 合同追踪/CRM 去重/自动发邮件回填） |
| 5 | Make（模块类型面） | ✓ | **Actions 类型**（处理服务检索数据——最常见——Get/Create/Update/Delete——Delete 注意有些服务不支持）；**If–Else 与 Merge 模块**（2026 早全 plan——原生复杂条件逻辑分支——Merge 合并场景）；**模板四阶段形态**（Trigger webhook/schedule/app event→Modules fetch+map→Filter/router 条件分支→Action 写 CRM/Slack/Sheets——20 模板都是这一个形状变体）；**AI-assisted workflow building**（coming soon） |
| 6 | Pipedream（代码步骤面） | ✓ | **语言支持**（Node.js v20+npm 400,000+ 包/Python 用 Pipedream SDK+PyPI/Go/Bash edge cases——每步可代码）；**Python 限制**（只能作 code step 语言——Components 系统只支持 Node.js——Python 不能发布为可复用 action/trigger）；**步骤模型**（code 拿 incoming event+所有前序 steps 输出作输入——return 或 assign 到 step output 流到下一步）；**内置能力**（Flow control/Concurrency and throttling/Key-value stores/Error handling/VPCs）；**连接账户**（OAuth tokens 运行时注入——this.slack.$auth.oauth_access_token——axios 调 Slack chat.postMessage） |
| 7 | Anthropic（视觉面） | ✓ | **三种图像来源**（base64 内嵌 request body/URL 引用/file_id Files API 上传一次引用多次）；**入口**（claude.ai 上传/拖拽；Playground 加到 User 消息块；API image content blocks）；**限制**（people identification 不能识别（命名）图中人物——拒绝）；**媒体类型**（jpeg/png/gif/webp）；**Files API 上传**（client.beta.files.upload file=(file name, f, media type)）；**坐标工作流**（coordinate-based workflows 指引） |
| 8 | deeplearning（语音面） | ✓ | **Whisper 架构**（encoder-decoder transformer——mel spectrograms→text autoregressive——680,000 小时多语言多任务监督音频——单模型多语言转写/英译/语言识别/时间戳预测）；**API**（$0.006/分钟 hosted whisper-large-v2——不用本地 GPU）；**本地 vs 云**（CPU/GPU 灵活/无 API 限制/成本可预测/延迟控制 sub-100ms/开源权重/社区扩展）；**性能**（99 语言/自动语言检测/口音背景噪声鲁棒） |
| 9 | GitHub（Actions 生态面） | ✓ | **Marketplace 规模**（2026 超 30,000 actions（2024 10,000+）——最大可复用 CI/CD 组件生态）；**主要维护者**（actions/* 官方 checkout/setup-node/cache/upload-artifact；docker/* Docker-Build/Buildx/Login docker/build-push-action@v6）；**高频 actions**（actions/checkout@v4 几乎每个 workflow——先找 marketplace 再写自定义 shell）；**研究事实**（arXiv 2103.12224：3190 repos 708 unique actions 20 类——最常用 CI/utilities/deployment——median action 添加两次；Apps vs Actions：Actions 免费自定义单任务自动化，Apps 可免费/付费带 paywall）；**供应链风险**（2026 LiteLLM/Telnyx/elementary-data/lightning/mistralai 恶意 wheel——Trivy chain PyPI token/cache poison+OIDC token theft） |
| 10 | OpenClaw（通道面） | ✓ | **50+ 通道**（Telegram/WhatsApp/Discord/Slack/Signal/iMessage/Microsoft Teams/Matrix/LINE/Lark/Google Chat/WebChat widget——单 Gateway 一个 agent 多 app）；**通道实现**（Telegram 内置核心 grammY Bot API 支持群组；Discord Bot API+Gateway；SMS Twilio webhook 官方插件；Synology Chat；Tlon Urbit；Twitch IRC；语音通话；BlueBubbles iMessage REST API 编辑/撤回/特效/回应/群组管理）；**管理命令**（openclaw channels add——交互式设置——配置或 Web UI——platform-specific credentials bot token/API keys）；**多通道**（同时跑多平台——自动按 chat 路由——dispatcher 归一化入站消息到同 agent runtime——context 跨平台）；**自定义通道**（channel adapters 50+——构建自有——发布社区）；**Discord 配置步骤**（OAuth2 scopes bot/Send Messages/Read Message History/View Channels→授权→paste token→Channel ID） |

## 判重（双键检索结果）
- Dify 发布嵌入：库内 §Dify 类锚点——发布 7 方式/iframe+script 嵌入/Pre-Fill Hidden Fields/widget 为独有增量 ≥40% → 落地
- n8n 模板社区：库内 §n8n 类锚点——模板库分类规模/RAG starter/自托管无 key 模板/WhatsApp 销售助手 prompt 约束为独有增量 ≥40% → 落地
- LangFlow 数据组件：库内 §LangFlow 类锚点——SQL Database 组件/NL 查询/SQL Agent/BigQuery 参数化/Astra CQL/Db2 VS 为独有增量 ≥40% → 落地
- Activepieces 工作流设计：库内 §Activepieces 类锚点——最佳实践清单/Router 条件/增量构建/AI inbound lead 流为独有增量 ≥40% → 落地
- Make 模块类型：库内 §Make 类锚点——Actions Get/Create/Update/Delete/If-Else+Merge/模板四阶段形态为独有增量 ≥40% → 落地
- Pipedream 代码步骤：库内 §Pipedream 类锚点——Node.js v20+npm/Python 仅 code step/步骤模型/内置能力为独有增量 ≥40% → 落地
- Anthropic 视觉：库内 §Anthropic 类锚点——三图像来源/people identification 拒绝/Files API/坐标工作流为独有增量 ≥40% → 落地
- deeplearning 语音：库内 §deeplearning 类锚点——Whisper 架构/680k 小时/API 定价/本地 vs 云为独有增量 ≥40% → 落地
- GitHub Actions 生态：库内 §GitHub 类锚点——Marketplace 规模/主要维护者/供应链攻击案例为独有增量 ≥40% → 落地
- OpenClaw 通道：库内 §OpenClaw 类锚点——50+ 通道/channels add/多通道路由/custom channels为独有增量 ≥40% → 落地

## 独点落地（10 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r276A-1 | wb-execute-discipline | 3.44.0+ | Dify 应用发布与嵌入 | 工具 |
| r276A-2 | wb-execute-discipline | 3.44.0+ | n8n 模板与社区生态 | 可复用 Skill |
| r276A-3 | wb-execute-discipline | 3.44.0+ | LangFlow 数据组件与数据库集成 | 工具 |
| r276A-4 | wb-execute-discipline | 3.44.0+ | Activepieces 工作流设计与最佳实践 | 可复用 Skill |
| r276A-5 | wb-execute-discipline | 3.44.0+ | Make 模块类型与核心概念 | 工具 |
| r276A-6 | wb-execute-discipline | 3.44.0+ | Pipedream 代码步骤与多语言 | 工具 |
| r276A-7 | wb-execute-discipline | 3.44.0+ | Anthropic 视觉与图像理解 | 工具 |
| r276A-8 | wb-execute-discipline | 3.44.0+ | deeplearning 语音与音频 AI | 可复用 Skill |
| r276A-9 | wb-execute-discipline | 3.44.0+ | GitHub Actions 生态与 Marketplace | 工具 |
| r276A-10 | wb-execute-discipline | 3.44.0+ | OpenClaw 通道与聊天集成 | 工具 |

## 复核
十独点均有当日实拉来源；均增量合并或新面；无并入未落地项。垃圾：本轮未产生临时文件。
