# r268C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r268A/r268B 及 r266/r267 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（自托管/部署面） | ✓ | **Docker Compose 部署**（需 Compose 2.24.0+；7 core services+8 dependent components+一次性 init_permissions 退出属正常）；**资源规格**（Min 2 CPU/4GB RAM；生产推荐 4+ cores/16GB；同机跑本地模型 +8GB per 7B）；**企业生产**（K8s 6 worker nodes 各 8CPU/32GB——支撑 3000 DAU；Container Registry AWS ECR AK/SK 或 IRSA）；**HTTPS**（Nginx 支持 Certbot Let's Encrypt 自动化——生产不长期纯 HTTP）；**SECRET_KEY**（openssl rand -base64 42）；**升级纪律**（git clone --branch latest release tag；用 release 文档、不删不认识的容器；docker compose ps 核对 Up/healthy） |
| 2 | n8n（调度触发器面） | ✓ | **Schedule Trigger 六字段 cron**（秒/分/时/日/月/周——`*/10 * * * * *` 每 10 秒）；**crontab guru 校验法**（去掉秒列后在 crontab guru 验证）；**高级 cron 字符**（- range// step/? day fields only/L last day of month——`0 9 L * *` 每月最后一天 9AM）；**时区回退**（Schedule Trigger 用 workflow timezone 若设置否则 n8n 实例时区）；**self-heal**（Schedule Node 用 elapsed-time check 自愈 missed triggers——strict equality 永久阻塞 bug 修复） |
| 3 | LangFlow（MCP 面） | ✓ | **MCP server**（flow 暴露为工具给 MCP clients；streamable HTTP 默认+SSE fallback；project MCP server URL path）；**MCP client**（消费外部 MCP servers 作为组件）；**双原生唯一**（Langflow 是唯一原生同时 MCP client+server 的系统）；**1.9 MCP for IDEs/coding agents**（IBM Bob/Claude Code 通过标准化 MCP 协议构建执行 flows）；**Git MCP server 例**（mcpServers config command uvx args mcp-server-git——project path 控制文件访问权限）；**watsonx Orchestrate 部署**（flow 发布为工具给 Orchestrate agent 调用——只部署 flow 非全 server） |
| 4 | Activepieces（自托管面） | ✓ | **单容器快速**（docker run -p 8080:80 -v ~/.activepieces；AP_DB_TYPE=PGLITE/AP_REDIS_TYPE=MEMORY 全内存跑）；**生产**（Docker Compose+PostgreSQL+Redis；Helm chart）；**app/worker 分离**（同镜像两角色 AP_CONTAINER_TYPE——APP 停止拉 flows 只服务 API/UI 重跑不再拖慢界面；WORKER 三 env vars 即可）；**MIT 许可**（非 source-available 非 fair-code 商用自由）；**升级**（release tag 0.79.2；multi-platform amd64+arm64 push Docker Hub+GHCR）；**安全**（生产改默认 DB 密码；≥6GB RAM 推荐） |
| 5 | Make（新特性面） | ✓ | **Make AI Apps 按钮**（Scenario Builder toolbar 查看最新 AI apps 直接加 canvas）；**移动场景到文件夹**（builder 内直移不必先保存离开）；**Make AI Sub-Agents 2026-07 发布**（coordinator concierge 服务/预订更新/维护告警）；**monday.com AI 模块**（Run Platform Agent beta——context id 会话记忆；Generate Chat Completion beta——平台 AI gateway 结构化 JSON）；**MCP Client 更新**（Execute an Action with AI 模块可选 AI provider——Make AI provider 访问 OpenAI 和 Claude 模型）；**新模型**（Claude Opus 5 大输入推理/Gemini 3.6 Flash/OpenAI 降 credit 成本）；**API endpoint 更新**（credential requests 新版本/scenario usage tracking/connection filtering）；**SAP Data Extractor/Darkmode** |
| 6 | Pipedream（运行时/部署面） | ✓ | **cloud-only 无自托管**（runtime 是 theirs；components source-available GitHub 但非可部署平台）；**Source Available License（2022-01-03）proprietary 非开源**；**数据主权影响**（严格数据驻留需求选 n8n 等自托管替代）；**Workday 收购（2025 末）**产品仍活；**受管 serverless AWS**（primarily US AWS；EU-only residency 非标准自助需 sales）；**无 white-label 隐形品牌化**；**迁移 playbook**（迁代码到标准栈 Vercel Functions/Supabase Edge Functions/Upstash QStash 重建 workflow execution） |
| 7 | Anthropic（prompt caching 面） | ✓ | **两种启用**（Automatic caching 顶层 cache_control 自动应用 breakpoint 到最后可缓存块并随对话前移——多轮最佳；Explicit block-level breakpoints 手动按频率分段）；**TTL 2026 经济**（5-min ephemeral 默认/1-hour extended 略高写成本；写 1.25x 5-min/2x 1-hour；读约 0.1x；最小可缓存块 1024 tokens Opus 4.7/Sonnet）；**最佳实践**（cache stable：system/background/large contexts/tool definitions；cached 内容放 prompt 开头；breakpoint 放最后稳定块；语义边界）；**三个 cache-buster**（改 tool definitions/切模型/变量数据注入 prefix——变量放 dynamic tail 永不 prefix）；**一致性**（cached sections identical+cache_control 同位置；tool_choice/image 一致；5 分钟生命周期内调用）；**压缩验证**（compaction 后 prefix 字节级保留验证）；**自动检查**（cache hits 到 breakpoint 前 ~20 blocks）；**价值排序**（system prompt 2,000-token 第一、工具定义第二大） |
| 8 | deeplearning.ai（prompt engineering 面） | ✓ | **ChatGPT Prompt Engineering for Developers**（1h40m 六任务模式——Guidelines 17m/Iterative 13m/Summarizing 7m/Inferring 11m/Transforming 12m/Expanding 6m/Chatbot 12m）；**AI Prompting for Everyone**（7h4m——Module1 Finding Info：novice vs power user/pretrained knowledge/web search/deep research；Module2 Writing：sycophancy/AI critique；Module3 Multimedia & Code）；**Prompt Engineering with Llama 2&3**（多轮对话/技巧/模型对比/Llama Guard 安全）；**GenAI with LLMs（AWS）**（13h18m）；**CharonHub 基础提示技术**（deep research 模式/给足上下文更多文档图像/重要决定让 AI 多想几分钟/生成图像分析数据） |
| 9 | GitHub（AI 技能仓库面） | ✓ | **gh skill（2026-04-16 发布）**（GitHub CLI 新命令 discover/install/manage/publish agent skills——遵循开放 Agent Skills 规范跨工具）；**VoltAgent awesome-agent-skills**（1500 官方技能聚合）；**mattpocock/skills 256.9k stars +13,419/周**（工程 agent skills）；**tt-a1i/archify 54.7k**（diagram skill）；**DietrichGebert/ponytail 132.1k +12,598/周**（coding thinking skill）；**addyosmani/agent-skills 85K**；**anthropics/skills 金标准**（Claude.ai/Claude Code/API 跨平台；web-artifacts-builder 例 npx skills add）；**awesome-harness-engineering**；**OpenClaw 385K stars**（TypeScript local-first）；**Hermes Agent 223K**（self-improving Nous）；**AutoGPT 186K**；**medy-gribkov/arcana**（universal skill manager 60+ skills marketplace——Claude Code/Cursor/Codex） |
| 10 | OpenClaw（模型路由面） | ✓ | **Gateway 架构**（port 18789 默认——消息平台与 AI agent 间核心路由层；管理会话；路由 WhatsApp/Telegram/Discord 消息）；**routing strategies 三种**（manual switching/primary-thinking tiering/multi-tier complexity-based——优化 cost-quality；典型省 50-90% API 成本）；**provider 前缀模型引用**（openrouter/fusion 多模型评估融合、vercel-ai-gateway/anthropic/claude-opus-4.6 路由到上游）；**routing config**（strategy fallback/chain ["anthropic","ollama"]；rateLimiting global tokensPerDay）；**condition 配额感知**（provider 级 condition：quota.models.X.remaining > 0 and error_count < 3） |

## 判重（双键检索结果）
- Dify 自托管：库内仅 §生产部署秘密键纪律——资源规格/K8s 拓扑/升级纪律为独有增量 ≥40% → 落地
- n8n 调度：库内已落 §定时任务错拍三策略/§触发器编排与幂等——秒级六字段 cron+self-heal 增量约 40% 边缘 → 并入记录
- LangFlow MCP：库内已落 §MCP 规格/§A2A 发布——双原生+IDE/coding agent 集成增量约 40% → 并入记录
- Activepieces 自托管：库内已落企业治理/Agent Builder——app/worker 分离部署+单容器为独有增量 ≥40% → 落地
- Make 新特性：并入记录（AI Apps 按钮/MCP Client 选 provider/monday AI 模块）
- Pipedream 运行时：库内 Pipedream 章节均为组件/开发面——cloud-only 平台边界事实（选型判据）为独有增量 ≥40% → 落地
- Anthropic prompt caching：库内仅 §上下文预算/pin 契约——TTL 经济数字/三 cache-buster/自动模式为独有增量 ≥40% → 落地
- deeplearning.ai prompt engineering：并入记录（六任务模式方法论已在库）
- GitHub gh skill：库内已落 §skills CLI 生态——并入记录
- OpenClaw 模型路由：库内仅 §Gateway 路由纪律（原则）——具体 routing 策略+condition 配额表达式（机制）为独有增量 ≥40% → 落地

## 独点落地（4 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r268C-1 | wb-execute-discipline | 3.22.0+ | Anthropic prompt caching TTL 经济与三 cache-buster（增量合并 §上下文预算） | 工具 |
| r268C-2 | wb-execute-discipline | 3.22.0+ | OpenClaw 模型路由三策略与配额感知 condition（增量合并 §Gateway 路由纪律） | 工作流 |
| r268C-3 | wb-execute-discipline | 3.22.0+ | Dify 自托管部署资源规格与升级纪律（增量合并 §生产部署秘密键纪律） | 工作流 |
| r268C-4 | wb-execute-discipline | 3.22.0+ | Pipedream cloud-only 平台边界事实与迁移 playbook（选型判据） | 工具 |

## 复核
四独点均有当日实拉来源；均为增量合并或新事实面落地；并入记录：n8n 秒级 cron/self-heal、LangFlow MCP 双原生、Make 新特性、deeplearning.ai 六任务模式、GitHub gh skill/生态情报。垃圾：本轮未产生临时文件。
