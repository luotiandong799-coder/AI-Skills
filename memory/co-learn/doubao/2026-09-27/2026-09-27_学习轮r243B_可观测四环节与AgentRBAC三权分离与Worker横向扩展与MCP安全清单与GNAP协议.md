# r243-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（可观测性/审计面） | ✓ | 内置 analytics dashboard（performance/cost/engagement）；conversation/run logs 保留+可下载归档+Run History+Variable Inspector 中间值+每 node 类型化错误元数据；Traces 流到 7 个外部栈（Langfuse/LangSmith/Opik/W&B Weave/Arize/Phoenix/Alibaba ARMS over OpenTelemetry）；审计四环节（应用层/API 网关/向量数据库/模型调用结构化日志+敏感操作标记+实时告警+合规导出，部署阶段即对齐策略）；插件治理 "Trust Is a Feature"（marketplace 发布验证行为检查）；plugin-daemon 隔离环境执行插件 |
| 2 | n8n（认证/权限/治理面） | ✓ | Agent RBAC 三权分离（谁能编辑/谁能执行/每次执行可达哪些凭证；Editor 不自动有 execute 权，execute 权不授予凭证访问）；Credentials 加密不暴露给 AI agent；Custom Project Roles（per-resource 细粒度权限 workflows/credentials/data tables/variables/folders/source）；OAuth 2.0 Token Exchange RFC 8693（seamless iframe embedding 无单独登录屏/delegated API access 全审计归因）；SSO 用户生命周期同步（加入/换角色/离开自动更新）；环境分离 dev/staging/prod 各自 credentials；Token exchange role claim（IdP 成为用户全局角色真相源每次覆盖 UI 角色，省略则 member） |
| 3 | LangFlow（组件开发面） | ✓ | Custom component API 三端点（POST /v1/custom_component 从代码建组件返回 node；/update 更新 build config 和 outputs；/validate/code 验证 Python 片段）；Extension bundle（pip 可安装包发布或 lfx extension dev 加载；lfx extension init 脚手架 canonical layout）；组件基础（Python 类继承 Component，class-level 属性标识描述，input/output lists 决定数据流）；LANGFLOW_ALLOW_CUSTOM_COMPONENTS 禁自定义 Python 组件执行+COMPONENTS_PATH allow-list；langflow-builder-mcp（MCP server 让 AI 编程式建/改 flows）；Native MCP server（每 project 可暴露为 MCP server，MCP client 消费外部 server 作为组件） |
| 4 | Activepieces（部署/扩展面） | ✓ | Worker 横向扩展（add replicas 任意 orchestrator Docker Compose/K8s/Nomad；推荐 one flow per worker concurrency 1 从单数规模 fleet）；AP_WORKER_CONCURRENCY=1 按 replicas 扩展（concurrency-1 worker 跑单 flow 小尺寸；slots=containers×concurrency 保持总槽位）；算术扩展（workers=peak concurrent flows，apps=ceil(workers/10)，1:10 app-to-worker）；吞吐实测（80 workers/8 apps 484 req/s warm→160 workers 777 req/s）；小 Redis 足够（千级 jobs/s 很少瓶颈）；单容器自托管（docker run MIT license） |
| 5 | Make（触发器/调度面） | ✓ | 两种主要触发器（Polling scheduled 定时检查外部服务拉变化 Gmail Watch/Sheets Watch 大多数 app 触发器 vs Instant webhook 外部服务推变化）；Webhook 是 instant trigger（request 到达即触发零轮询调用，实时事件支付/表单/Git）；webhook 批处理调度（默认收数据立即执行，可改 scenario 或 webhook 模块设置周期性处理所有请求）；On-demand 调度（等 API 调用或 Run once，无 schedule 不自动跑）；激活时选处理旧数据或只新数据 |
| 6 | Pipedream（HTTP/工作流面） | ✓ | HTTP Request Action（Postman-like 界面配置 headers/body/连接 account，连 Slack 自动配置 Bearer authorization headers）；Actions 抽象（处理连接逻辑/错误处理，只需指定参数，可创建共享自定义 actions）；HTTP API 调用 workflow（OAuth client ID/secret+Project ID+workflow HTTP endpoint）；Workflow 分享（share link 唯一 key 代表 triggers/steps/settings；不包含私有资源 connected accounts/sources/data stores 需手填）；Create workflow endpoint（单 API 请求编程式分配 connected accounts/props/deploy）；HTTP interface（$.interface.http+customResponse+respond()）；Destinations（$.send.http 发数据到外部 endpoint） |
| 7 | Anthropic（MCP 面） | ✓ | MCP 2026-07-28 大改（stateless core 双向有状态→request/response，服务器可 serverless/edge，breaking initialize/session 移除 per-request metadata）；标准化扩展（MCP Apps/Tasks versioned extensions framework）；安全最佳实践（默认 read-only 按 server 按 project 开写；least-privilege tokens fine-grained PAT 特定 repo/DB role 限 schema/OAuth scope 只读；secrets env/secrets manager 不提交不 inline；fetched content 当 untrusted）；生产安全清单（隔离 server connections sandbox 显示完整 launch command；review tool descriptions 隐藏指令；validate every request sign requestState/check token audience/validate Origin/reject header-body mismatches；SDKs patched）；Transport（stdio 本地，streamable HTTP formerly SSE 远程，capability negotiation initialize） |
| 8 | skills.sh（CLI/安装面） | ✓ | skills CLI（npx skills add <owner>/<skill-name>；find [query] [--owner]；update 更新所有已装；init 创建 SKILL.md 或新 skill 子目录）；npx 直接运行无需安装；npx-skills PyPI 包（Python 项目内用无需全局 Node/npm，vendored Node runtime，uv add npx-skills，项目级版本约束）；skills.json 版本化配置（committed to Git 可 review diffable 记录激活 skills；air-gapped 自包含二进制）；--skill 精确安装单技能（npx skills add nvidia/skills --skill cuopt-... 用 SKILL.md name 字段） |
| 9 | docs.openclaw.ai（插件/网关面） | ✓ | Gateway 是会话/路由/通道连接单一真相源（多通道 Discord/iMessage/Signal/Slack/Telegram/WhatsApp/WebChat 单 Gateway 进程；plugin channels 加 Matrix/Nostr/Twitch/Zalo；多 agent 路由隔离 session per agent/workspace/sender）；插件两种格式（channel plugin 连接消息平台/普通 plugin；defineChannelPluginEntry 或 definePluginEntry；imports 用 plugin-sdk/<subpath>）；npm-first 分发模型（git 直接安装 ref checkouts+metadata tracking；openclaw plugins list 依赖透明）；Gateway relay 反转 voice 认证（浏览器只连 OpenClaw 实例，Gateway 管理所有上游 provider 连接，API keys/OAuth tokens 不进 client 不暴露 DevTools）；SDK source-provider contract（外部插件代码完全在核心 npm 包外但深度集成） |
| 10 | GitHub（生态面） | ✓ | Hindsight 32,217★（Agent Memory That Learns）；GNAP 2.0K★（Git-Native Agent Protocol：git repo 4 JSON 文件协调 AI agents 无 server 无 DB）；CrewAI 58,770★（多 agent 编排最易接入，PyPI 9.52M 月下载）；MetaGPT/AgentScope/AG2（multi-agent 编排框架）；Microsoft AutoGen 24k★（Python/.NET/Java 灵活编排插件集成） |

## 判重基准
双键检索（相对 r241/r242/r243-A 已落章节）：Dify（r243-A 落 queue engine——"可观测四环节+7 trace 栈"独有增量深化）；n8n（r242 落错误处理/r243-A 落 embedding——"RBAC 三权分离+Token Exchange"独有增量深化）；LangFlow（r243-A 落 DevOps Toolkit——"组件 API+执行开关 allow-list"独有增量深化）；Activepieces（r242-B 落 durable execution——"worker 横向扩展模型"独有增量深化）；Make（r243-A 落 error router——"Polling vs Instant 触发器选型"独有增量深化）；Pipedream（r243-A 落 props 纪律——"Actions 抽象+workflow 编程式部署"独有增量深化）；Anthropic（r241-C/r242-C 落 MCP 协议/安全——"MCP 安全清单 read-only 默认/least-privilege tokens"独有增量深化）；skills.sh（r242-A 落 CLI 触发纪律——"skills.json 版本化+npx-skills Python 内嵌"独有增量深化）；openclaw（r242-C 落 Binding 路由——"Gateway relay 反转认证+npm-first 插件分发"独有增量深化）；GitHub（r243-A 落 Plugin 架构——"GNAP Git-native 4 JSON 无 server 无 DB"独有增量深化）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 可观测四环节 | 应用/网关/向量库/模型四环节结构化日志+敏感操作标记+7 trace 栈 | 工作流 | wb-execute-discipline |
| ② n8n Agent RBAC 三权分离 | 编辑/执行/凭证访问独立；credentials 加密不暴露；Token Exchange 全审计 | 工作流 | wb-execute-discipline |
| ③ Activepieces worker 横向扩展 | concurrency-1 加 replicas；slots=containers×concurrency；1:10 app 比例 | 工作流 | wb-execute-discipline |
| ④ MCP 安全最佳实践清单 | 默认只读+least-privilege tokens+secrets 不 inline+fetched 当 untrusted | 工作流/工具 | wb-execute-discipline |
| ⑤ GNAP Git-Native Agent Protocol | git repo 4 JSON 文件协调 agent 无 server 无 DB+skills.json 版本化 | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
