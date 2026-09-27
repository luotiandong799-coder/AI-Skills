# r273C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（API 发布面） | ✓ | **API 密钥管理**（应用密钥——app 内创建仅作用该应用、一个密钥服务所有终端用户；知识库密钥；**Bearer Token** Authorization header；**只在后端调用**——嵌入前端/客户端可被提取滥用；每请求 user 参数区分人=用户隔离）；**OpenAI Compatible Dify App**（插件暴露 OpenAI 兼容 endpoint——Endpoint Name/API Key/App/Memory Mode；API key 建议 GUID/hash）；**Extension Plugin Endpoint**（serverless 灵活性——api_key secret-input）；**HTTP Request API Key 三子类型**（Basic base64/Bearer/Custom）；阿里云 SchedulerX 集成（API key+Inputs JSON 定时跑 workflow） |
| 2 | n8n（模板/社区面） | ✓ | **模板库规模**（Miscellaneous 480/CRM 471/AI RAG 712——数千真实共享 workflows import 拆解；n8n blog 客户案例；YouTube Nate Herk AI-agent 全端）；**AI Content Summarizer Suite**（4 workflows 处理 URL/raw text/PDF）；**RAG Starter**（Simple Vector Stores+Form trigger+OpenAI）；**Ollama 自托管模板**（11 Self-Hosted AI Workflow Templates 无 API keys——AI Blog Writer 4-stage research/outline/draft/edit、Lead Scoring 1-100、Competitor Monitor、Email Auto-Responder、Support Ticket Router）；**生产级**（Lead Capture→CRM→Welcome Email zero paid nodes；Stripe Payment→Fulfillment→Receipt；Form→Sheets+Slack）；**社媒流水线**（topic→AI content→branded image→scheduled posting——并行 image+logo、Google Drive 公开 URL、日志回写 Sheet）；**AI agent 商业**（YouTube→Auto Social Repurposer 视频→3 tweets+LinkedIn+email subjects→Notion；Reddit Lead Monitor+AI Reply Drafter——AI 起草 Telegram 审批后发） |
| 3 | LangFlow（API 认证面） | ✓ | **API key 认证**（1.5+ 大多 endpoint 需 x-api-key header 或 query；用户特定——只访问创建者 flows/components；Settings→Langflow API Keys→Add New）；**LANGFLOW_API_KEY_SOURCE**（db 默认——数据库验证；env——LANGFLOW_API_KEY 环境变量——K8s/CI-CD 注入）；**JWT 认证**（HS256 对称单机/开发；RS256 非对称生产；JWT_SECRET）；**lfx serve**（FastAPI server 暴露 POST /flows/{flow_id}/run；需 API key）；**Workflow API**（x-api-key header；Content-Type/accept）；**Flow DevOps Toolkit SDK**（production url+api_key_env）；**配置**（LANGFLOW_SUPERUSER/SUPERUSER_PASSWORD；LANGFLOW_SECRET_KEY——Fernet 加密）；**CLI**（langflow api-key——superuser 才能创建） |
| 4 | Activepieces（环境变量/密钥面） | ✓ | **Project Variables**（命名值 scoped 单项目——任一步引用；API key/webhook URL/Slack channel ID/feature flag；不像 step output 不随 run 变）；**Secret Managers**（外接秘密管理——1Password Secrets Automation service account token；op://vault/item/field 引用；flow 跑时 AP 认证取密——on-demand 从不存储；更新后 cache 过期最多 1 小时或立即）；**部署 env 变量**（AP_ENCRYPTION_KEY 32 字符 hex 加密 connections——openssl rand -hex 16；AP_JWT_SECRET 32 hex；AP_FRONTEND_URL redirect/webhook；AP_EXECUTION_MODE SANDBOXED/UNSANDBOXED/SANDBOX_CODE_ONLY；AP_FLOW_WORKER_CONCURRENCY 10；AP_DB_TYPE）；**docker-compose 坑**（.env.example→.env 自动填密——openssl 缺失仍报成功留空——grep 检查三键） |
| 5 | Make（函数/数组面） | ✓ | **Make Functions app**（IML 函数从 mapping fields 独立成 standalone modules——可视化数据处理链式构建；空输入输出空结果不停场景）；**新增内置函数**（arraydiff/arrayintersect/set/escapejson——比较数组找新增/缺失、更新集合、准备 raw JSON）；**数组函数库**（first/last/count/contains/map 含过滤——map(complex array; key; [filter key]; [values])；sort(array, key, order)；keys()/length()/merge()/remove()/get(array; index)——索引从 1 开始/flatten/deduplicate/filter/reduce/parseJSON/toString）；**应用例**（Trello custom fields——map+get+first；webhook payload 动态字段提取） |
| 6 | Pipedream（触发器类型面） | ✓ | **触发器分类**（Connect 两类——App-based event sources+Native triggers（cron 自定义+timezone）；workflow 触发——App triggers/HTTP/Webhook/Schedule/Email/RSS）；**组件接口**（Timer——interval 或 cron；HTTP——请求调用；props 部署时用户输入；emit events 检查/触发 workflows/自 app 消费；内置 key-value store；**内置 deduping strategies**）；**开发**（timer prop $.interface.timer default intervalSeconds 15*60；polling triggers——timer 属性） |
| 7 | Anthropic（thinking 面） | ✓ | **Interleaved thinking**（Claude 在工具调用之间思考——单 assistant turn 内对每工具结果推理再决定下一步；链式多工具调用中间夹推理；基于中间结果更精细决策；模型支持——Claude Opus 4.6 等）；**adaptive thinking**（thinking: {type: "adaptive"}——评估每请求复杂度决定是否/多少思考；默认 effort high 几乎总想；低 effort 简单问题跳过；**自动启用 interleaved**——agentic 工作流有效）；**manual extended thinking**（type: "enabled"；budget_tokens 设内部推理最大 token——作用于完整 thinking tokens 非摘要；beta header interleaved-thinking-2025-05-14；Sonnet 4.6 支持两者）；**thinking 结构**（评估 prompt→think→distill summary into thinking block） |
| 8 | deeplearning（提示工程面） | ✓ | **ChatGPT Prompt Engineering for Developers**（Isa Fulford+Andrew Ng——两原则：写清晰指令+给模型时间思考；summarization/inferring/transforming/expanding/chatbot；90 分钟/9 视频/7 code；Jupyter 环境）；**Prompt Engineering with Llama 2 & 3**（Llama Guard 安全）；**AI Prompting for Everyone**（AI as Thought Partner——正确上下文/更有效头脑风暴/**AI 诚实反驳而非迎合**；多媒体与代码）；**advanced 技术**（CoT——"Let's think step by step" 提升 30-50%；directional stimulus；Program-of-Thought；Self-refine 迭代改进） |
| 9 | GitHub（Agentic Workflows 面） | ✓ | **GitHub Agentic Workflows**（2026-06-11 public preview——GitHub Actions 内跑 coding agents；natural language Markdown 定义自动化——编译为标准 Actions YAML（.lock.yml 加固）；复用现有 runner groups/policy constraints；引擎——Copilot/Claude Code/Gemini/OpenAI Codex；场景——issue triage/CI failure analysis/docs updates/test enhancements/scheduled jobs）；**gh aw CLI**；**Docker Sandboxes 运行时**（2026-07——agent 宽控制环境跑 Docker，隔离 microVM+网络策略+secrets injection）；**deep-agent-action**（自托管——@agent mention；plan/edit/run toolchain/land PR——runner 内进程无 SaaS 无 secrets 出境）；**演进**（2018 Actions→2021 Copilot→2025 Coding Agent→2026 Agentic Workflows） |
| 10 | OpenClaw（插件/扩展面） | ✓ | **插件定义**（小代码模块扩展命令/工具/Gateway RPC；核心未内置功能或排除可选功能）；**官方插件**（Matrix/Nextcloud Talk/Nostr/Twitch/Zalo 一条命令装；官方通道 Discord/Feishu/Google Chat/iMessage/IRC/LINE/Matrix/Mattermost/Microsoft Teams/Nextcloud Talk/Nostr/QQ Bot/Raft/Signal/Slack/SMS/Synology Chat/Tlon/Twitch/Voice Call/WhatsApp/Zalo）；**架构演进**（v2026.5.28-v2026.6.1——外部化官方插件/SQLite install index/SecretRef 契约/标准化 lifecycle hooks）；**api.registerHook**（typed hooks 运行时生命周期——middleware/policy/message rewriting/prompt shaping/tool control 首选）；**扩展面**（channels/model providers/harnesses/tools/skills/speech/transcription/voice/media/generation/web fetch/search）；**社区**（5,705+ community-built；ClawHub；Bundled/Managed/Workspace 三档）；**@1claw**（29 工具——secrets/vaults/policies/sharing/signing/transactions/env/automations/memory/approvals——EVM+Bitcoin/Solana/XRP/Cardano/Tron）；**集成**（Apple Notes/Notion/Obsidian/GitHub；Home Assistant/Philips Hue/Spotify/Sonos） |

## 判重（双键检索结果）
- Dify API 发布：库内 §发布（r272C）——密钥管理/OpenAI Compatible/Extension Endpoint/API Key 三子类型为独有增量 ≥40% → 落地（增量合并）
- n8n 模板社区：库内无模板生态专题——规模/生产级模式/Ollama 模板为独有增量 → 落地
- LangFlow API 认证：库内 §部署 API（r269A）——API key 体系/JWT/lfx serve/DevOps SDK 为独有增量 ≥40% → 落地（增量合并）
- Activepieces 环境变量：库内 §认证（r270C）——Project Variables/Secret Managers/部署 env 为独有增量 ≥40% → 落地
- Make 函数：库内 §表达式（r266B）——Functions app/新四函数/map 过滤语法为独有增量 ≥40% → 落地（增量合并）
- Pipedream 触发器：库内 §触发器（r270A）——Connect 两类/Native cron/deduping 为独有增量 ≥40% → 落地（增量合并）
- Anthropic thinking：库内 §长上下文（r269C）——Interleaved/adaptive thinking/budget_tokens 为独有增量 ≥40% → 落地（增量合并）
- deeplearning 提示工程：库内无提示工程课程专题——两原则/Thought Partner/advanced 技术为独有增量 → 落地
- GitHub Agentic Workflows：库内 §GitHub 生态（r273A/B）——Markdown→YAML/Docker Sandboxes/gh aw/多引擎为独有增量 ≥40% → 落地
- OpenClaw 插件：库内 §插件（r270A）——官方通道/架构演进/registerHook/社区扩展为独有增量 ≥40% → 落地（增量合并）

## 独点落地（10 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r273C-1 | wb-execute-discipline | 3.37.0+ | Dify API 发布与密钥管理 | 可复用 Skill |
| r273C-2 | wb-execute-discipline | 3.37.0+ | n8n 模板与社区生产级模式 | 工作流 |
| r273C-3 | wb-execute-discipline | 3.37.0+ | LangFlow API 认证体系 | 可复用 Skill |
| r273C-4 | wb-execute-discipline | 3.37.0+ | Activepieces 环境变量与密钥管理 | 可复用 Skill |
| r273C-5 | wb-execute-discipline | 3.37.0+ | Make Functions 可视化转换 | 工具 |
| r273C-6 | wb-execute-discipline | 3.37.0+ | Pipedream 触发器与组件接口 | 工作流 |
| r273C-7 | wb-execute-discipline | 3.37.0+ | Anthropic interleaved/adaptive thinking | 模型 |
| r273C-8 | wb-execute-discipline | 3.37.0+ | deeplearning 提示工程课程 | 可复用 Skill |
| r273C-9 | wb-execute-discipline | 3.37.0+ | GitHub Agentic Workflows | 工具 |
| r273C-10 | wb-execute-discipline | 3.37.0+ | OpenClaw 插件系统 | 可复用 Skill |

## 复核
十独点均有当日实拉来源；均增量合并或新面；无并入未落地项。垃圾：本轮未产生临时文件。
