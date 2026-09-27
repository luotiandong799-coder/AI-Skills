# r239-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（知识库/RAG 检索面） | ✓ | 检索三模式（向量检索自然语言复杂主题/全文检索精确术语产品码名称 ID 快且可预测/混合检索语义+全文+reranker 最佳准确率但慢需 rerank 模型）；Weighted Score（语义权重/关键词权重 0-1 自定义比例；semantic=1 纯向量 keyword=1 纯关键词）；Rerank 模型（第三方重排 Cohere rerank-multilingual-v3.0/Jina AI；多模态知识库需 Vision 标记 rerank 否则图像被排除）；Multi-path Retrieval（同时查 Context 所有知识库→collect 全部对齐内容→Rerank 选出最合适）；K 值调优（保守开始再升/阈值不高不低/必要 rerank 上澄み；K 太大噪声混入太小漏召回）；High Quality 索引模式才可用 Weighted Score |
| 2 | n8n（Agent 记忆/工具细节面） | ✓ | 记忆作为画布可配置部分（AI Agent 节点连接 memory sub-nodes 定义对话历史存储/持久时长/何时检索清除；每个记忆节点设置可见于画布）；Multi-Agent AI Agent Tool（orchestrator 有几个工具其中一个或多个是配置为工具的第二个 agent）；Manager+Sub-agent 模板（Memory BufferWindow 节点连 ai_memory input）；ReAct 演进（现代 LLM GPT-5/Claude/Gemini 原生 tool calling 处理推理行动循环显式 ReAct prompting 大多不再需要；n8n Tools Agent 在此基础上加持久记忆/可配置 max iterations/全执行可追溯）；Data Table memory（multi-session chat agent 用 session ID 持久到 Data Table；滑窗 10 轮+按 name/email 查历史+身份验证流） |
| 3 | LangFlow（API/部署面） | ✓ | 生产部署最佳实践（runtime headless backend only 服务 Langflow API 无可视化编辑器；最低 2Gi RAM+1000m CPU per instance 3 replicas；外置 PostgreSQL 替代默认 SQLite）；Docker 容器化（langflowai/langflow:latest；自定义组件适配）；API 访问（/api 端点；LANGFLOW_PORT env；webhook 触发 flows）；Flow DevOps Toolkit SDK（终端工作流 version/test/deploy 替代手动 JSON 导出分享导入；环境变量/测试/部署；production url+api_key_env）；多 worker（LANGFLOW_WORKERS/GUNICORN_PRELOAD/max-requests jitter；从少 worker 开始防 OOM） |
| 4 | Activepieces（piece 开发面） | ✓ | Piece 标准 TypeScript 模块（createPiece name/displayName/actions/triggers；action=createAction name/displayName/run async context；trigger 监听外部事件）；PieceAuth（None()/SecretText with async validate hook 调 provider API）；开发流程（ap create-piece→cd pieces→npm install→npm run build）；piece-builder 五步（RESEARCH 找 REST API 文档/识别 auth API key OAuth2 Basic Auth/列端点查 webhooks/记 base URL pagination rate limits→PLAN→BUILD→TEST）；动态属性（Property.Dropdown options async 拉用户仓库 auth 上下文）；createPiece 元数据（displayName/logoUrl/authors/minimumSupportedRelease） |
| 5 | Make（监控/团队/可靠性面） | ✓ | 团队级场景 Playbook（请求转价值可行性风险评分 backlog/场景设计为小可测阶段+显式决策点+安全默认/幂等键+轻量 ledger 防重复不安全重放/标准化错误路由重试限流使失败可观测可恢复/RBAC+凭据治理+变更控制式发布——teams are the unit）；系统监控自动化（轮询系统健康/阈值触发告警/路由 on-call/记录每个事件）；操作监控（按计划监控项目管理和工单；AI 捕获优先级负责人耗时；标记逾期结构化告警路由 owner——act on prioritized escalations not raw data）；Make Grid（数百 automation/agent 一个 live view 总览）；可视化优先（Scenario Builder 画布可视化整个决策树；每模块接收产出 fallback 分叉可见；他人可读逻辑）；执行日志（详细步骤日志；retry/skip problematic records/route failures to notification flows；scheduling and throttling） |
| 6 | Pipedream（MCP 工具/agent 使用面） | ✓ | 单 MCP 端点 10000+ 工具（3000+ APIs；远程 server 工具发现+per-user auth；任何 MCP client 兼容；工具跑每用户已连接账户）；用户侧场景（帮草拟产品更新基于 Linear tickets/为明天会议准备参会人信息 Google Calendar/探索 PostgreSQL 最近 10 客户/Stripe 昨日营收发 Slack 摘要）；调试场景（拉最后 5 事件查 JSON 结构/描述工作流逻辑步骤查配置错/列活跃订阅看外部 API 喂到哪）；Vercel AI SDK 集成（StreamableHTTPClientTransport 示例） |
| 7 | Anthropic（模型定价/规格面） | ✓ | 模型价目矩阵（Sonnet 5 $2/$10 introductory→9/1 起 $3/$15；Opus 5.5 $4/$20 比 Opus 5 $5/$25 便宜；Fable 5.1 $10/$50 旗舰；Haiku 4.5 $1/$5；Batch API 50% 折扣）；Opus 5.5（1M context window/128K max output/Fast mode 可用）；定价三档（Standard/Standard US-only inference/Batch 半价）；缓存价格分层（cache reads $0.20-0.50 vs 普通输入 $4-5——差 20 倍；5m cache writes/1h cache writes）；rate limits 提升（为更高 effort level 提高） |
| 8 | skills.sh（ClawHub/安装生态面） | ✓ | ClawHub 双 CLI 分工（openclaw 命令 search/install/update skills+plugins vs 独立 clawhub CLI registry auth/publishing/delete-undelete）；安装源五形态（@owner/slug ClawHub、skills-sh:owner/repo/slug、git:owner/repo@main、./path/to/skill --as custom-name、--force 重装）；记录 install source metadata 更新解析同一 registry 包；ClawHub 5400+ 技能社区贡献；免费为主 vast majority free open-source 少量 premium verified publishers 一次性/订阅费；安全元数据（minimum Gateway version/target hosts/environment requirements/cryptographic summaries of artifacts） |
| 9 | 阿里虾小宝（龙虾生态面） | ✓ | JVS Claw（阿里云手机版 OpenClaw"龙虾"：三步操作；自进化"万能 skill"——"如果没有这个技能，请搜索并创建"，小龙虾找最合适 skill 完成任务；免费内测 8000 Credits 14 天；iOS/Android/网页/Pad 多端）；Cloud Agents CN 更新日志（Skills 上传 zip 自动归一化 Windows 反斜杠路径 Mac/Windows 跨平台一致；并发加资源 FOR UPDATE 锁杜绝相互覆盖；卡死会话自动恢复）；支付宝"阿宝"（万余项服务 AI 化；AHA 协议多智能体跨端互联；Agentar 200+ 技能包+数字专家智能体+模板定制开发）；天猫"龙虾版"生意管家（虚拟 Agent 团队全天候经营） |
| 10 | GitHub（AI 标签仓库生态面） | ✓ | 技能生态分发格局（obra/superpowers 69.6k★ 20+ dev workflow skills plugin marketplace 安装/alirezarezvani/claude-skills 2.3k★ 86 production-ready/anthropics/skills 82.8k★ 16 official example）；agent-skills addyosmani 99,160★ Production-grade engineering skills for AI coding agents 已验证 production 技能集；design-taste-frontend 432.3k 安装 83.4k★ 修复颜色字体间距构图具体修正建议（habr TOP-50 报告 9 百万星/22 百万安装）；gemini-cli 107,164★ 开源终端 agent；LangGraph 33k★ 生产标准有状态 agent 框架（Klarna/Cisco/Vizient 用） |

## 判重基准
双键检索：Dify（r238-B SchemaRAG/r239-B 已落，检索三模式+Multi-path 独有增量）；n8n（r239-A/B 已落，记忆画布化+ReAct 演进独有增量）；LangFlow（r236-C 已落 Flow DevOps 工具链，DevOps SDK 终端工作流重叠>60% 增量约 40% 可合并但不单列）；Activepieces（r239-A/B 已落，piece 五步构建+动态属性独有但本批不单列）；Make（r239-A 已落，团队化 Playbook+Grid 独有但本批不单列）；Pipedream（r239-A/B 已落，单端点 10k 工具独有但本批不单列）；Anthropic（r238/r239-A/B 已落，价目矩阵+缓存 Batch 成本独有）；ClawHub（r238-C 已落 OpenClaw hooks，安装源五形态+安全元数据独有）；虾小宝（r238-A 已落"龙虾"生态入门，万能 skill 自创建+zip 归一化独有）；GitHub（r238-C/r239-B 已落，技能集仓库星标格局独有但本批不单列）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 检索三模式+双权重+Multi-path | 向量/全文/混合选型；语义关键词 0-1 双权重；多知识库并发+rerank 上澄；K 值保守起 | 工作流 | wb-execute-discipline |
| ② n8n 记忆画布化+ReAct 演进 | 记忆 sub-node 存储/持久/检索清除可见；原生 tool calling 替代显式 ReAct prompting | 工作流 | wb-execute-discipline |
| ③ Anthropic 价目矩阵+成本结构 | Sonnet5/Opus5.5/Fable 价目；cache read 比输入便宜 20 倍；Batch 半价 | 模型 | wb-execute-discipline |
| ④ ClawHub 安装源五形态+安全元数据 | @owner/skills-sh/git/path/force 五源；最小 Gateway 版本+工件加密摘要 | 工具 | wb-execute-discipline |
| ⑤ 万能 skill 自创建+zip 路径归一化 | "没有这技能请搜索并创建"；zip 反斜杠归一化跨平台一致 | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：wb-ponytail/wb-max-token-saver/wb-context-compressor 无新可优化项。
- 垃圾：本轮未产生临时文件。
