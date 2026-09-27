# r265A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站，查询词与 r263 三轮+r264 三轮全错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（Creator Center 发布面） | ✓ | **Creator Center 提交管理**（上传导出文件提交模板/Customize profile 管公开档案/Organization settings 邀请成员控权限）；**发布审核流**（提交→Pending 审核→批准发布；Pending 可撤回回 Draft 再编辑重提交；Publish Update 生效）；**模板变现**（PartnerStack 联属链接，订阅佣金）；**插件发布 CI 管线**（pre-check-plugin.yaml 风险标签/pre-check-plugin-sandbox.yaml 沙箱验证/upload-merged-plugin.yaml 合并后上传；CI 阻塞错误 vs 警告分离；merge main 自动上 marketplace.dify.ai）；**发布形态**（hosted 体验/API 端点/embeds/MCP-compatible 工具） |
| 2 | n8n（企业身份治理面） | ✓ | **SSO 四通道**（SAML/LDAP/OIDC 并存；IdP groups→instance/project roles 自动映射同步生命周期）；**Custom Project Roles+环境组合**（生产安全迭代）；**Token Exchange (RFC 8693)**（iframe 嵌入免登录/delegated API 带审计归因；IdP role claim=全局角色真相源覆盖 UI 角色；未识别/owner 角色拒绝）；**AI Agent 身份管理**（SSO/OIDC 把 agent 会话绑定认证用户→继承作用域权限而非共享 service account；HTTP 集成集中 OAuth 凭证管理，refresh/scopes/grant 出 workflow） |
| 3 | LangFlow（生产部署面） | ✓ | **两形态部署**（IDE=开发可视化编辑器 vs runtime=生产无头服务仅 API，只跑服务 flow 所需进程）；**资源下限**（backend 1Gi RAM/0.5CPU×1；runtime 2Gi RAM/1CPU×3）；**外部 PostgreSQL 强推**（默认 SQLite 不推荐生产）；**Active-Active HA**（多实例+负载均衡+共享 HA PostgreSQL；主写副本读流复制）；**Helm 两 chart**（langflow-ide 开发/langflow-runtime 生产）；**多 worker**（LANGFLOW_JOB_QUEUE_TYPE=redis/REDIS_QUEUE_URL/GUNICORN_PRELOAD）；**容器化**（langflowai/langflow:latest 基镜像打包 flows+依赖可复现）；Caddy 反代 |
| 4 | Activepieces（轮询触发器面） | ✓ | **Polling Trigger 三钩子**（onEnable 初始化状态如 lastId→run 每 5 分钟拉取→onDisable 清理）；**两轮询策略**（Polling by ID vs Polling by timestamp——Drupal/Snowflake 实例按 id 或 updated_at 检测新增）；**Worker PollingJob**（Cron 默认 5 分钟：Load config→call onEnable→fetch new items）；**数据同步**（webhook/event/cron triggers 启动同步；Tables 存 cursor+last-seen timestamps；HTTP/code/built-in 加工 normalize+merge 保持 identifier 一致）；**Redis 队列**（失败 job 重执行；spike 延迟不丢） |
| 5 | Make（错误处理高级面） | ✓ | **Retry error handler**（暂停失败 bundle、存 error message+mappings+remaining flow、自动/手动重试——vs 默认跳过/回滚）；**Break 指令重试**（attempt limit 1-10+间隔分钟；固定间隔非指数退避；rate limit 设 5-15 分钟）；**指数退避**（connectionerror/moduletimeouterror 自动；延迟取决于 incomplete executions 开关）；**Incomplete executions 管理**（勾选批量 Retry selected→Scheduled→In Progress）；**Throw 替代**（JSON parse bundlevalidationerror 条件抛错）；**429 绕行**（Sleep+Ignore directive） |
| 6 | Pipedream（触发器/event source 面） | ✓ | **两类触发器**（App-based event sources 第三方事件/native triggers）；**Sources 能力**（props 部署时收输入；HTTP/timer/cron/manual 触发；emit 事件→触发 workflow→SSE 实时消费/API 消费；内置 kv store；内置 deduping strategies）；**pd.triggers.deploy API**（部署 triggers 给 end user，webhookUrl 回调）；**Connect workflow HTTP 触发**（x-pd-environment/x-pd-external-user-id 头）；**test event**（选历史事件或发新） |
| 7 | Anthropic（MCP 开发面） | ✓ | **工具数量上限**（agent 质量在 30-40 tools/context 后骤降——Anthropic 内部评测；scope=每 server 一个 coherent 产品域，别做 80 工具 platform-server）；**Tool Search Tool**（2025-11 advanced tool use：注册数千工具+defer_loading: true，agent 按需搜索）；**细粒度工具**（create/update/delete 三分比 action 参数好推理+安全）；**安全清单**（server-side strict schema 验证+fail closed；sensitive 数据 redact/truncate；audit trails 记录谁调了啥/sessionId/toolName）；**传输**（stdio 本地/streamable HTTP 远程，initialize 能力协商）；**MCP Directory 提交**（safety annotations 要求）；Python SDK v2 2026-07-27 |
| 8 | 腾讯 SkillHub（演进面） | ✓ | **定位**（ClawHub 本土化高速镜像平台：中文搜索+国内节点分发+安全审核）；**规模演进**（2026-03-11 上线 1.3 万→6 月 8 万+→8 月 10.8 万+；下载 6000 万+）；**TRACE 评测体系**（识别高质量 Skill）；**三线并行安全审核**；**SkillPay**（2026-07-16：Skill 分发+Agent 调用+支付同链路，微信支付底层；商家上架 Pay Skill 收费）；**生态**（WorkBuddy/QClaw/ima 兼容）；**安装**（skillhub.cn/install/skillhub.md） |
| 9 | deeplearning.ai（课程面） | ✓ | **RAG 课程模块**（keyword/semantic/hybrid search、chunking、query parsing；ANN/向量库/Weaviate；cross-encoders/ColBERT/reranking；agentic RAG；RAG vs fine-tuning；生产部署）；**Agentic AI**（reflection/tool use/planning/multi-agent 四模式）；**Document AI**（LandingAI ADE 框架：文档当视觉对象，custom models 解析复杂元素+字段 grounded 到页面精确位置，集成 RAG+部署 AWS 管线）；**课程路线**（Prompt Engineering→LangChain→Agentic RAG with LlamaIndex→Multi Agent CrewAI） |
| 10 | GitHub（agent 生态面） | ✓ | **Trending 新仓库**（earendil-works/pi=Unified LLM API+agent loop+TUI+coding agent CLI 一体；tinyhumansai/openhuman=开源 agent harness 本地优先记忆+编排+工作流；akitaonrails/ai-memory=跨 agent 供应商编码 CLI 长期记忆+handoff）；**Top100**（herdr=编码 agent 运行时 Rust 40.8k★；TiDB=agentic 负载 ACID+事务+分析+向量搜索；BrowserOS=开源 agentic 浏览器；GNAP=git repo 4 JSON 文件协调 agent 无 server 无 DB）；browser-use 116k★ 领先榜 |

## 判重基准
双键检索：MCP 开发（§r263A MCP 安全四机制/§r239B MCP 安全清单——30-40 tools 上限+defer_loading+scope 一产品域为独有增量，新面落）；n8n 身份（grep 未见 SSO/RBAC/Token Exchange 章节——新面）；LangFlow 部署（§6392 LFX 无头执行管"无头怎么跑"——IDE/runtime 架构+资源+HA+Postgres 增量并入记录）；Activepieces 轮询（§6302 webhook 验签管"webhook 安全"——轮询三钩子+两策略新面落）；Make 错误（r231C 错误五指令+§261C 已覆盖错误处理面——retry error handler 暂停 bundle+Break 重试配置增量并入记录）；Pipedream 触发器（r264A GitHub Sync/r264C draft 模型——event source/triggers API 新面落）；SkillHub（r246B 本土镜像——规模数字+SkillPay+TRACE 增量并入记录）；deeplearning（r264A Agentic AI——ADE/文档视觉对象新面并入记录）；GitHub 生态（r226C jev-chat/§2172 archify——herdr/pi/ai-memory/openhuman 新面落）。

## 独点落地（5 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r265A-1 | wb-execute-discipline | 3.20.0+ | MCP 工具数量上限与 defer_loading + server 安全纪律 | 可复用 Skill |
| r265A-2 | wb-execute-discipline | 3.20.0+ | n8n 企业身份治理：SSO 四通道与 agent 身份继承 | 工具 |
| r265A-3 | wb-execute-discipline | 3.20.0+ | Activepieces 轮询触发器三钩子与 ID/timestamp 两策略 | 工作流 |
| r265A-4 | wb-execute-discipline | 3.20.0+ | Pipedream event source 与触发器部署 API | 工具 |
| r265A-5 | wb-execute-discipline | 3.20.0+ | GitHub agent 生态新仓库：herdr/pi/ai-memory/openhuman | 可复用 Skill |

## 复核
五独点均有当日实拉来源（逐站 URL 见各站摘要）；r265A-1/3/4/5 新面，r265A-2 新面；备选并入记录不单独落地（LangFlow 部署/Activepieces 未落、Make 错误/SkillHub/deeplearning 增量并入）。垃圾：本轮未产生临时文件。
