# r245-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（嵌入/模型提供面） | ✓ | 模型供应商配置（LLM OpenAI/Anthropic/Google/Cohere/Ollama 本地 + Embedding OpenAI/Cohere/Azure/本地 + Specialized 图像生成/语音/Moderation）；自带 API key vs AI credits 共存（Usage Priority 控制先用哪个再 fallback 哪个）；Dify 检查 key（Setup 填 API key 后先验证再让 provider 可用）；VISION badge（多模态 embedding/rerank 模型标记 VISION AWS Bedrock/Google Vertex/Jina/Tongyi 图片向量化参与检索）；向量库可插拔（VECTOR_STORE 环境变量 tablestore/opensearch/腾讯云 换库不换应用）；Voyage AI plugin（Atlas vector search 工具 embed 单文本） |
| 2 | n8n（模板/集成生态面） | ✓ | 模板生态（471 CRM workflows 按类浏览；RAG 客服/工单 triage/多平台发布）；execution_id 关联（webhook 收工单生成唯一 execution_id 关联 run 每个事件）；Query-to-action（AI Classifier 解释意图映射到工具 Bright Data MCP+OpenAI 聊天转自动化）；社区节点（Lusha 社区节点 enrich 线索）；工单 triage（AI Agent 读工单+知识库+置信度草稿响应 数据表工具记 EVENT）；自定义 AI Agent URL（每 distinct job description 一个 URL） |
| 3 | LangFlow（API/部署面） | ✓ | lfx serve（FastAPI 服务器把 flows 暴露为 HTTP API POST /flows/{flow_id}/run 需 LANGFLOW_API_KEY public server）；部署双形态（IDE 可视化编辑器开发 + Runtime headless backend 只服务 API 生产 2Gi RAM/1000m CPU per instance 3 replicas）；多 worker（LANGFLOW_WORKERS 增并发 每个进程自己的内存 build queue 除非加 Redis-backed job queue 共享 build events）；1.8 v2/workflow API（更简单 response+异步后台 jobs）；OSS 无 Admin Page（/admin 移除 用户管理走 Users API /login/admin 仍是 admin sign-in）；Docker 部署（LANGFLOW_AUTO_LOGIN）；watsonx Orchestrate 部署（publish flow as tool 不 hosting 完整 server） |
| 4 | Activepieces（自托管/安全/权限面） | ✓ | RBAC（团队 admin 分配角色控制项目/文件夹/资源访问 四标准角色）；SSO（SAML 2.0+Google SCIM Provisioning 自动同步用户组）；AP_SSRF_ALLOW_LIST（flow 需访问内部 API/数据库时加白名单 地址或整个子网 10.10.0.0/24）；数据掩码（敏感细节不出现日志）；凭证加密（credentials stay in own vault encrypted at rest）；敏感连接需审批（restrict sensitive connections require approval before use 防私下连私有数据库）；Helm 部署（外部 PostgreSQL/Redis 支持 secrets 引用） |
| 5 | Make（模板/用例面） | ✓ | 模板生态（7 AI 自动化示例各配 scenario template 可 clone 模块链 不只概念描述）；模板选型判据（≤5 节点低复杂度用模板 内部用可接受偶发失败 生产关键自定义）；部署用 duplication 不 copy-paste（duplication 保留参数结构和版本引用 copy-paste 产生孤儿实例漂移）；staging 测试三场景（happy path/缺失输入/迟到触发器 模板失败多在这里暴露）；Text parser 截断（LinkedIn 700 字符/Twitter 250）；category filter 门控分发 |
| 6 | Pipedream（连接账号/认证面） | ✓ | Managed Auth（托管认证 3,000+ APIs hosted OAuth clients+secure token storage+automatic refresh 用户秒级连接开发者不碰凭证）；external_user_id（端用户标识）；自带 OAuth client（OAuth 应用 Google Drive/Slack/Notion 必须用自己 custom OAuth clients oauthAppId 关联）；API Proxy（Pipedream OAuth client+Connect environment production/development+external user ID+account ID）；this.appName.$auth（code step 里 app auth 信息 oauth_access_token）；SDK 自动刷新 token |
| 7 | Anthropic（提示工程/上下文管理面） | ✓ | 五层上下文工程栈（minimal system prompts+progressive disclosure+tool design+auto-memory+richer references）；system prompt 是内核不是知识库（稳定行为进 prompt 任务特定知识进检索 操作指导进工具 持久偏好进记忆）；@ 引用文件（references 让 Claude 引用深信息 specs/mockups/codebases HTML mockup 比描述/截图更好）；Progressive Disclosure（不 dump 全部 context 进第一条消息 最小指令起步让模型按需问）；上下文意识（Opus 4.6/4.5 跟踪剩余 context 窗口 token 预算）；先宽后窄（短宽查询起步再逐渐收窄）；验收标准 upfront（说清 done 长什么样 测试过/风格匹配/无新依赖）；一条会话一个任务 /clear 隔离；绝不臆测未打开代码 |
| 8 | skills.sh（优秀技能榜单/评测面） | ✓ | Official Skills 生态（56 dev teams/9 categories/660 official skills microsoft/testmu-ai 等）；榜单信号（install count 是价值信号 leaderboard ranked by installs 每 skill 映射 GitHub repo npx skills add owner/repo）；Superpowers 147.7K+ installs（obra/superpowers brainstorming plan-before-code workflow+TDD+systematic debugging）；元技能（find-skills vercel-labs 常年霸榜 以技能管技能；skill-creator/writing-great-skills 写规范技能）；Skill Vetter 273.9K（security-first skill vetting 装任何 skill 前检查 red flags/permission scope/suspicious patterns）；web-artifacts-builder 97.2K（收集计算器/仪表盘/网页表单） |
| 9 | OpenClaw（安全/事件/权限面） | ✓ | CVE-2026-25253（WebSocket origin validation gap CSWSH 跨站 WebSocket 劫持 CVSS 8.8 偷 gateway auth token 可禁用确认提示/逃容器/执行任意命令 gatewayUrl query parameter 设计缺陷）；最小权限（专用服务账号运行不 root Docker 只挂 agent 需要的目录 drop 不必要的 Linux capabilities）；Exec Approvals 增强 2026.6.6+（Cwd-Bound Reusable Approvals 绑定工作目录的复用批准 + Scoped Cron Grants 作用域 cron 授权 + Revocable MCP App Access 可撤销 MCP 应用访问）；每日安全审计 cron（firewall/fail2ban/SSH 配置/openclaw.json .env 文件权限/开放端口/Docker 状态/是否 root 运行 报昨日差异）；OPENCLAW_STATE_DIR（2026.6.6 前默认 ~/.openclaw） |
| 10 | GitHub（RAG/记忆/编排面） | ✓ | MemOS 11,594★（Self-evolving memory OS ultra-persistent memory+hybrid-retrieval+cross-task skill reuse 35.24% token savings DeepSeek Harness 支持）；all-in-rag 11,388★（RAG 技术全栈指南 Datawhale）；RAGFlow 70-89K★（RAG 引擎 document ingestion/vector indexing/citation tracking/multi-step reasoning/agent integration）；LangGraph 60K（图状编排）；code-graph-rag（Tree-sitter 解析多语言代码库进 Memgraph 知识图谱 自然语言查询/编辑/优化）；Mem0 62-63K（universal memory layer 简单 API）；Cognee 30K（knowledge-graph memory for agents）；MemGraphRAG（agent-memory/graph-construction/multi-agent/ontology KDD 2026）；pocketflow 10K（local LLM orchestration） |

## 判重基准
双键检索（相对 r244 三批+r245-A/B 已落章节）：Dify（r244-C 落检索/r245-B 落意图路由——"Usage Priority+VECTOR_STORE 插拔"独有增量新面）；n8n（r244-B 落 webhook/r245-B 落错误处理——"execution_id 关联全 run 事件"独有增量新面）；LangFlow（r244-A 落 Extension/r245-A 落 Agentics——"IDE/Runtime 分离+lfx serve"独有增量深化）；Activepieces（r245-B 落触发器/r244-C 落部署——"SSRF 白名单+敏感连接审批+掩码"独有增量新面，本轮未选）；Make（r245-A 落模板/r245-B 落场景调度——"模板选型判据+duplication vs copy-paste"独有增量新面，本轮未选）；Pipedream（r245-A 落 props/r245-B 落 sources/actions——"Managed Auth+API Proxy+env 区分"独有增量深化，本轮未选）；Anthropic（r244-C 落 caching/r244-A 落 hooks——"五层栈+内核 vs 知识库分层"独有增量新面）；skills.sh（r245-A 落 Skill Workshop/r245-B 落发布路径——"official skills+install signal+vetter"独有增量新面，本轮未选）；OpenClaw（r243 落 RBAC/r245-B 落会话双层——"Exec Approvals 生命周期+安全审计 cron"独有增量新面）；GitHub（r245-A 落 hindsight/r245-B 落 agent-browser——"MemOS+code-graph-rag"独有增量深化，本轮未选）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify Usage Priority+向量库插拔 | 自带 key vs credits 并存优先级控制；VECTOR_STORE env 换库 | 工具/工作流 | wb-execute-discipline |
| ② n8n execution_id 关联 | webhook 收单生成唯一 id 关联 run 每事件 | 工作流 | wb-execute-discipline |
| ③ LangFlow IDE vs Runtime+lfx serve | 开发可视化/生产 headless；lfx serve 需 API key | 工具/工作流 | wb-execute-discipline |
| ④ Anthropic 五层上下文栈 | minimal prompt+progressive disclosure+tool design+auto-memory+richer references；内核 vs 知识库 | 模型/工作流 | wb-execute-discipline |
| ⑤ OpenClaw Exec Approvals 生命周期 | cwd-bound 复用批准+scoped cron+revocable MCP；每日安全审计 | 工具/工作流 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
