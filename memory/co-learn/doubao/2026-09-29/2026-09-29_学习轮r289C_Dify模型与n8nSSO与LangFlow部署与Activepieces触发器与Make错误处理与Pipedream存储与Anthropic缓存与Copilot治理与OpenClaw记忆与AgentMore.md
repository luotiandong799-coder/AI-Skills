# r289C 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r289A/r289B 及 r284-r288 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（模型配置） | OK | **模型供应商在 设置 > 模型供应商 配置；系统默认推理模型（System Reasoning Model）：创建应用使用的默认推理模型，对话名称生成、下一步问题建议等功能也用该默认模型**；**模型插件市场安装（Dify Marketplace）：predefined-model + customizable-model + fetch-from-remote 三种配置方式可共存（统一凭据可用预定义+远程模型，新模型可额外自定义）**；**OpenAI-API-compatible 插件可接任意兼容 OpenAI 的端点（如阿里百炼 compatible-mode/v1）**；**插件类别含 LLM/rerank/embedding 模型（如 Bedrock 插件预定义 llm+rerank+embedding 且支持自定义模型配置）** |
| 2 | n8n（SSO/用户管理） | OK | **OIDC/SAML SSO + User provisioning：IdP（Okta/Azure AD/Google Workspace）登录时自动分配每个用户的 instance role 和 project roles——权限生命周期跟随组织（入职/角色变更/离职自动同步，免手工管理）**；**JIT provisioning：管理员在 n8n 内定义 group-to-role 映射表达式（$claims 对象访问 OIDC claims，表达式返回 true 即分配所选角色，规则从上到下评估，每次登录重新评估）——IdP 只需发标准 group 数据，n8n 处理映射**；**三内置 instance role：Owner/Admin/Member + 可创建自定义角色（granular permissions）**；**SSO 环境变量：N8N_SSO_MANAGED_BY_ENV / N8N_SSO_USER_ROLE_PROVISIONING=instance_role / N8N_SSO_OIDC_LOGIN_ENABLED 等；2FA enforcement** |
| 3 | LangFlow（生产部署） | OK | **生产用 Runtime（headless 后端）部署：只服务 Langflow API、无可视化编辑器；最小资源 2Gi RAM + 1000m（1 CPU）/实例 × 3 副本**；**v1.9.0→v1.10.0 内存优化：依赖裁剪 + worker 生命周期管理 + Linux Copy-on-Write，内存消耗 ~89% 减少**；**多 worker 配置：LANGFLOW_WORKERS/LANGFLOW_WORKER_TIMEOUT/LANGFLOW_GUNICORN_PRELOAD/GUNICORN_CMD_ARGS（--max-requests --max-requests-jitter）——worker 太多本地库 OOM，先少后调**；**LANGFLOW_DEPLOYMENT_PROFILE=prod 生产预检（默认 dev 跳过）**；**MCP server export：任何 Langflow flow 可编译成 MCP 兼容服务器——Cursor/Claude Desktop/LangGraph 可当标准工具调用（tool factory 定位）**；**安全：LANGFLOW_CORS_ORIGINS 指定来源（禁通配）、不直接暴露 7860 端口（Nginx/Caddy 反代）、HTTPS、API key 轮换、RBAC；性能：缓存 LLM 调用/批处理节点/异步工作流/连接池/Prometheus+Grafana 监控；PostgreSQL HA（流复制主写副本读+故障转移）** |
| 4 | Activepieces（Webhook/触发器） | OK | **三种触发器技术：Polling（周期调用端点查变化）/ Webhooks（单 URL 监听用户事件）/ App Webhooks Subscriptions（OAuth2 developer app 收所有授权用户事件，Not Supported）**；**Webhook Trigger 生命周期：On Enable 用 context.webhookUrl 向第三方注册 webhook 并存储 webhook Id 到 store；On Handshake 某些服务要求 challenge 握手**；**Catch Webhook 触发器接受任意 HTTP 方法（GET/POST/PUT/DELETE）**；**Webhook 双角色：触发器（收数据起流）或动作（流末发通知）**；**Event Streaming：把平台审计事件转发到 webhook（常见模式：指向流内 flow → 路由到 Slack/Gmail/Teams/custom HTTP）——反应 flow run 失败/新登录/项目发布**；**API 自动化：配置 retries with backoff、circuit breakers** |
| 5 | Make（监控/错误处理） | OK | **错误处理器四型 + 选择表：Resume（造假输出保持流——邮件发送失败时继续处理失败日志）/ Commit（事务处理确认——DB 多模块部分成功时确认）/ Rollback（事务取消——DB 部分失败整体回滚）/ Break（保存 incomplete execution + 重试——停止会误事的一般运营场景）**；**Break handler：从流程移除错误 bundle，Make 存错误消息+映射+剩余流程为 incomplete execution，可按设置自动完成或存到人工解决**；**Notifications：场景设置 Notifications 标签页启用错误邮件通知；更精细做法=专门监控场景**；**Slack 告警：Error Handler 连 Slack Send a Message，含场景名/错误类型/错误消息/发生时间 + 失败执行深链；Email digest 模式：data store 收集全天错误，每天发一封摘要（别为每次瞬态错误 ping 团队）**；**错误类型：AccountValidationError（HTTP 401/403）等；Make API Get incomplete executions 做每日健康报告（6AM cron）** |
| 6 | Pipedream（Data Store/调度） | OK | **Data Stores=内建 KV 存储：Brotli 压缩、JSON 可序列化，项目内任意 workflow 可读写——跨 run 追踪状态（幂等键/滚动聚合/最后同步时间戳）无需真数据库；scope=workspace，可 dashboard 编辑，有计划限制**；**set 方法第三参数 TTL（秒）——记录自动过期（临时值/会话历史清理）**；**较重状态用自带 DB connectors（Postgres/MySQL/Supabase/MongoDB）**；**调度触发器（2026-04 起所有套餐含免费）：预设间隔（15/30 分钟、每小时、每天、每周、每月）+ 自定义 cron 表达式**；**组件级 KV：$.service.db（component-specific，跨执行保持状态）**；**工作流日志/执行数据按账号保留规则存储；x-pd-nostore header 或 retention 控制可关闭日志** |
| 7 | Anthropic（Prompt Caching） | OK | **自动缓存：请求顶层加单个 cache_control 字段，系统自动管理 cache breakpoint（移到对话增长时最后一个可缓存块并前移）——多轮会话推荐起点**；**显式块级 breakpoints：需按不同变化频率缓存不同段时用（system instructions/背景信息/大上下文/频繁工具定义；放提示开头效果最佳；breakpoint 放语义边界）**；**最小缓存块：1024 tokens（Opus 4.7/Sonnet 4.6）、2048（Haiku 4.5）；最多 4 个 cache_control breakpoints/请求；缓存前缀创建顺序：tools → system → messages**；**TTL 两档：5 分钟（默认：写成本 1.25× 输入、命中成本 10% 输入——高频端点/会话/批处理/紧耦合 agent 最佳）与 1 小时（extended cache：写成本 2×、命中成本 10%）**；**成本最多降 90%**；对比：Gemini 显式 CachedContent API 最小 32768 tokens（Pro）/4096（Flash），TTL 默认 1 小时 |
| 8 | GitHub Copilot（企业治理） | OK | **Enterprise managed settings 覆盖 Copilot app 和 cloud agent（managed-settings.json：企业所有者定义 guardrails——哪些插件/市场可用、能否绕过审批提示；Copilot 客户端自动强制）**；**Copilot app 独立 policy（不再依赖 Copilot CLI policy 开关）**；**MCP allowlists（2026-08）：allowedMcpServers/deniedMcpServers 集中控制客户端可运行的 MCP servers——批准依赖的、阻止不可信/不合规的**；**Enterprise teams model policy targeting（2026-07 公测）：user-based model policy——AI 管理员设企业基线模型集，再给特定 team 授额外模型（按角色/前沿团队实验）**；**Enterprise team specialization（2026-08）：按 team 定制 managed settings（分项配置文件）**；**cost centers + premium request allowance 管理支出；模型访问强制：显式选择允许模型并定期评审 allowlist（GA 新模型评审后启用、deprecated 退役前确保替代已启用）；Enterprise-Managed Authorization（EMA）IdP 驱动 MCP auth 流** |
| 9 | OpenClaw（会话/记忆） | OK | **记忆三层：短期（当前会话——刚提的偏好）/ 长期（永久 MEMORY.md——用户画像/事实）/ 情景（永久——重要交互事件）**；**会话存储结构：sessions.json（session store：键值映射 sessionKey→SessionEntry，Gateway 管理可变运行时状态：当前会话 ID/最近活动/开关/令牌计数器）+ transcript（仅追加树形 JSONL：id+条目）**；**每日日志循环：memory/YYYY-MM-DD.md + MEMORY.md 永久参考卡；新会话加载今天+昨天日志（更早掉出直接视野）；会话结束 agent 写短命上下文到每日日志 + 更新 MEMORY.md 持久事实（旧/更正条目更新或移除）**；**v2026.4.9 "Dreaming"：长期记忆整合配置（schedule: after-session、sessionWindow: 30、dayWindow: 7、relevanceThreshold: 0.6、decayRate: 0.05、outputPath: .openclaw/memory/consolidated.json）**；**v2026.7.1：记忆提供商不可用时系统明确提示失败而非看似完整答案；会话/对话/压缩/目标/路由在重启/重置/延迟跟进后更一致保留**；**记忆丢失原因：任务状态只在会话期间模型上下文窗口里，显式写入 MEMORY.md/每日记忆才跨重启存活（临时推理/未保存中间变量随会话消失）** |
| 10 | 智谱 AgentMore | OK | **智谱清言推出的 AI 智能体协作与 Skills 扩展平台（2026-05-25 发布）：多 Agent 协作、技能市场扩展、任务执行与工作流编排；基于大模型 Agent 框架，支持多角色并行与工具调用**；**Skills 技能广场三模块：内置推荐 + SkillHub + 开源社区，免费开放超 7.4 万个专业技能包（微信读书/美团优惠券等第三方生活与工作服务），一键安装且不消耗额外 Token**；**共享工作区：公共+私密共享文件空间，群组实时共享资料协同文档**；**多平台一键接入：微信/飞书等无缝接入；流程自动化：重复操作沉淀为可复用流程；协作扩展：团队把常用任务封装成能力模块持续调用迭代**；**智谱智能体开发平台：零代码拖拉拽画布构建任务流 + 批量调试 + 页面嵌入/API 输出；GLM-5.3-Flash 多模态；ZCode/Claude Code/Codex 接入 + 4 类开发场景 MCP（视觉理解/联网搜索/网页读取/开源仓库分析）** |

## 判重（双键检索，增量判定）
- Dify 模型配置（r284-r289B 无模型配置主题）→ 系统默认推理模型/三配置共存/OpenAI-compatible 插件 → **新面**
- n8n SSO（r284-r289B 无 SSO/用户主题）→ OIDC/SAML provisioning/JIT group-to-role/$claims/自定义角色 → **新面**
- LangFlow 生产部署（r289B 知识库不覆盖）→ Runtime headless/内存 89% 降/多 worker/prod 预检/MCP export → **新面**
- Activepieces 触发器（r289A agent、r289B piece 构建不覆盖）→ 三触发器技术/Webhook 生命周期/Event Streaming → **新面**
- Make 错误处理（r289B 版本/恢复不覆盖）→ 错误处理器四型/Break handler/Notifications/Slack 告警/Email digest → **新面**
- Pipedream Data Store（r289A 凭证、r289B 超时不覆盖）→ KV 存储/TTL/调度触发器/$.service.db → **新面**
- Anthropic Prompt Caching（wb-max-token-saver 有缓存治理比例原则）→ 重叠约 50%，增量=TTL 双档成本（5 分钟 1.25×/1 小时 2×、命中 10%）/最小缓存块 1024-2048/4 breakpoint/自动缓存机制 → **合并保留增量**
- GitHub Copilot 治理（r289A 自定义 agent 文件契约不覆盖）→ managed-settings.json/MCP allowlists/model policy targeting/EMA → **新面**
- OpenClaw 会话/记忆（wb-context-compressor 有记忆分层/流水线方法论）→ 重叠约 60%，增量=sessions.json/transcript 存储结构/每日+昨日加载窗口/Dreaming 参数/记忆丢失原因 → **合并保留增量**
- 智谱 AgentMore（r289A 技能市场治理、r289B 腾讯 SkillHub）→ 重叠约 60%，增量=三模块广场/不消耗 Token 安装/共享工作区/多角色并行 → **合并保留增量**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 模型配置与供应商插件（新面） | 工具 |
| 2 | n8n SSO 与用户供给（新面） | 工具 |
| 3 | LangFlow 生产部署与内存优化（新面） | 工具 |
| 4 | Activepieces 触发器与 Event Streaming（新面） | 工作流 |
| 5 | Make 错误处理器四型与告警（新面） | 工作流 |
| 6 | Pipedream Data Store 与调度（新面） | 工具 |
| 7 | Anthropic Prompt Caching 机制（合并增量） | 工具 |
| 8 | GitHub Copilot 企业治理（新面） | 工具 |
| 9 | OpenClaw 会话存储与记忆整合（合并增量） | 工具 |
| 10 | 智谱 AgentMore 平台（合并增量） | 工作流 |

## 复核
十独点均有当日实拉来源；7 新面 + 3 合并保留增量（增量均≥40%），零纯重复。