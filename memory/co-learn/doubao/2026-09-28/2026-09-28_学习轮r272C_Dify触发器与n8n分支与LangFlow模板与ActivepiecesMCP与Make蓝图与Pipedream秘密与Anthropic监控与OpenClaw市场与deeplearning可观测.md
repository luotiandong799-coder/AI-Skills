# r272C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（触发器面） | ✓ | **三种 Trigger**（Schedule 预设时间/间隔周期可预测任务；Plugin 插件事件——Slack/GitHub 集成；Webhook 收 HTTP 请求通用接口）；**Start 节点互斥**（User Input 直接交互/API 调用；Trigger 自动运行——同画布互斥 right-click Change Node）；**发布限制**（仅 User Input workflows 可发布 web apps/MCP servers/backend API/复用工具）；**Schedule 配置**（hourly/daily/weekly/monthly/cron；提供 timestamps 变量）；**Webhook 细节**（回调 URL；自定义 query 参数+请求头；事件订阅式）；**Plugin 事件**（Zendesk ticket_created 等）；**配额**（20,000 Trigger Events/月） |
| 2 | n8n（分支/合并面） | ✓ | **IF 节点**（二元决策 true/false；10 操作符 equals/not/greater/less/contains/not contains/is empty 等；Combine AND/OR；Always Output Data 若后接 merge 要开）；**Switch**（多条件 Case n/Default；Rules 直接比较/Expression JS 逻辑；多分支比链 IF 高效）；**Merge**（重组分支；Append 堆叠/Combine 按标识符配对；Split>Process>Merge 关键模式；Merge+IF 会触发 IF 两输出都执行）；**Filter**（筛 item 不建分支）；**多 IF 链** |
| 3 | LangFlow（模板/市场面） | ✓ | **Templates**（预建 flow 起点——Basic Prompting 到 Vector Store RAG 双 sub-flow）；**模板提交规范**（name ≤3 词首字母大写；description 展示编辑器）；**Store API**（GET /v1/starter-projects/；POST /v1/store/components/ 分享组件；PATCH 更新）；**导出三方式**（Projects 页/共享/API /flows/download）；**Share 菜单**（API access 自动生成 Python/JS/curl；Export JSON；MCP Server 暴露工具；Embed HTML/React/Angular；Shareable Playground）；**Shareable Playground**（/public_flow/$FLOW_ID 公开 URL——交互聊天无需安装/API key） |
| 4 | Activepieces（MCP 面） | ✓ | **内置 MCP server**（AI 助手自然语言建 flows/管理 tables/测试自动化；OAuth 浏览器认证首次）；**MCP Tool piece**（创建工具 MCP 客户端可调用执行 flow——4 字段）；**最大开源 MCP server**（连接 Claude/Cursor/Codex 驱动全平台；763 apps；免费所有 plan）；**AI Agent Builder**（Max steps 20 per run；own model OpenAI/Anthropic/Gemini/Azure/Bedrock；External MCP 让 agent 用自有 MCP servers；Human Approvals 运行等人批准）；**Embeddable MCP**（用户点 Authorize 后端拿 token 运行自动化——OAuth）；**跨应用桥**（安排会议/更新日历/触发邮件） |
| 5 | Make（蓝图/克隆面） | ✓ | **Scenario blueprints**（保存/复制成蓝图含模块/设置/映射值；备份场景——丢权限/换账号；分享蓝图他人导入）；**Scenario sharing**（公共场景页链接/社媒分享；链接查看或登录复制副本编辑；链接总显示最新保存版本——不用导出导入）；**克隆**（同团队/跨团队——模块设置+连接都带；只需设 webhooks；跨团队设目标连接）；**模板**（预配置蓝图模块序列/连接/映射；make.com/en/templates 浏览；Use Template 复制进工作区；所有 plan 含免费；落 inactive 先审再激活）；**API clone**（POST /scenarios/{source_id}/clone json teamId/name） |
| 6 | Pipedream（属性/秘密面） | ✓ | **env vars 限制**（sources/actions 不直接访问——组件可被任何人用无法保证变量存在；sources 用 secret props；actions object explorer 选变量）；**私有组件**（无直接 workspace/project 变量访问——加 prop 专门要；API keys 配 secret prop set value {{process.env.YOUR_ENV_VAR}}）；**secret props 规范**（敏感数据一律 secret props；Shared Secrets GUID 存 $.service.db 验证入站事件）；**connected accounts vs env**（Pipedream 集成 app 用 connected accounts；不支持 app/任意配置用 env vars；别硬编码 code steps）；**configure 端点**（POST /v1/connect/{project_id}/components/configure 取 prop 候选值）；**app prop 错误引用**（google_sheets vs googleSheets） |
| 7 | Anthropic（用量/监控面） | ✓ | **Usage & Cost Admin API**（程序化访问历史用量成本；精确 token counts；Cost Reconciliation 财务对账；Admin key/OAuth org:admin/非 workspace 限制个人 key；workspace keys 不行）；**端点**（GET /v1/organizations/cost_report 服务级美元拆分；user_cost_report 每用户；get-messages-usage-report uncached input tokens/workspace_id/has_more/next_page）；**监控内容**（uncached input/output/cache creation/reads；跨 models/workspaces/keys；cache efficiency/server tool usage）；**用途**（Usage Monitoring/Cost Attribution/finance chargeback）；**spend cap**（Start/Build/Scale 月上限）；**API 头**（Authorization Bearer 或 x-api-key；anthropic-workspace-id 多 workspace 必填）；**Agent SDK cost tracking**（每交互 token 用量——并行工具+多步对话） |
| 8 | deeplearning.ai（LLMOps 可观测面） | ✓ | **Evaluating AI Agents（Arize 2h36m）**（Tracing agents/Monitoring agents——observability 洞察步骤调试；component evals code-based vs LLM-as-a-Judge；experiments 迭代质量+路径）；**LLMOps（Google Cloud 1h31m）**（Fundamentals/Data Preparation/Automation and Orchestration Pipelines）；**LLM 可观测专门课程**（LangSmith+Langfuse 生产级 observability+incident response——prompt chains/token costs/hallucination/silent quality degradation）；**LangSmith current_trace().invoke**（每 chain 捕获 requests/responses/latency）；**MLflow 替代**（实验+模型+traces 单平台；10-100 req/day overhead 不可测）；**Observability Pillars**（logs/metrics/traces 适配 LLM token usage+output quality；Feedback loops 用户反馈回 eval/fine-tuning）；**DSPy**（MLflow 追踪调试） |
| 9 | GitHub（AI agent 框架面） | ✓ | **Trending 09-18**（vercel/eve 开源 agent 构建 +173；strands-agents/harness-sdk 生产 harness Python/TS +41；alphaXiv/OpenResearch coding→research agents +939；NVIDIA/OpenShell 安全私有自主运行时）；**Trending 09-21**（BuilderIO/agent-native +98；AutoGPT +27；smolvm 可嵌入可分支 VM +45；webcodex 云 AI agents 真实开发环境 +99）；**榜单**（langflow 155k★/langchain 146.9k★/awesome-llm-apps 139k★/cc-switch 133.8k★；LibreChat 45k★ MCP/Skills 增强；siyuan 46.5k★）；**框架比较**（最小框架覆盖真实需求几乎总胜最流行——语言→license→能力；18 tracked）；**agentscope 26.9k/ag2 4.2k/genai_agents 20k**；**pathway 62.2k ETL 流处理/LLM pipelines/RAG**；**llm-app 58.9k 云模板** |
| 10 | OpenClaw（ClawHub 面） | ✓ | **ClawHub**（官方技能市场；skill=含 SKILL.md 文件夹+可选文件）；**publish**（clawhub skill publish <path> --slug --name --changelog；跳过未变化内容；新技能 1.0.0 起；认证）；**install 两法**（openclaw skills install <slug> 装活动 workspace；clawhub install <slug> 装 ./skills；@owner/<slug>；--version --global）；**search**（clawhub search <keyword> 返回 description/version/install count）；**update/verify**（skills update @owner/ --global；verify --card 打印 Skill Card；clawhub sync --all）；**发布流程**（自动化扫描后公开；社区评分反馈；开放提交比 SkillHub 多）；**source metadata**（记录 install source 更新解析同一 registry 包）；**包类型**（clawhub package publish；plugins install clawhub:<package>）；**前置**（npm i -g clawhub；无 openclawcli 不工作） |

## 判重（双键检索结果）
- Dify 触发器：库内已落 §Workflow vs Chatflow（r272A）——触发器三类型+Start 互斥+发布限制为独有增量 ≥40% → 落地
- n8n 分支/合并：库内已落 §循环与分支——IF/Switch/Merge 三节点分工+Split>Process>Merge 为独有增量 ≥40% → 落地（增量合并）
- LangFlow 模板/市场：库内已落 §模板——模板提交规范+Store API+Shareable Playground 为独有增量 ≥40% → 落地（增量合并）
- Activepieces MCP：库内已落 §MCP 规范——MCP server 平台能力+Embeddable MCP+Agent Builder 限制为独有增量 ≥40% → 落地
- Make 蓝图/克隆：库内已落 §场景蓝图——scenario sharing 链接版+克隆带连接+API clone 为独有增量 ≥40% → 落地（增量合并）
- Pipedream 秘密：库内无 Pipedream secret props 章节——secret props+GUID shared secrets 为独有增量 ≥40% → 落地
- Anthropic 用量监控：库内已落 §缓存定价——Usage & Cost API+监控指标+spend cap 为独有增量 ≥40% → 落地（增量合并）
- deeplearning LLMOps 可观测：库内已落 §评估——Evaluating AI Agents 课程+可观测支柱+feedback loops 为独有增量 ≥40% → 落地（增量合并）
- GitHub agent 框架：并入记录（vercel/eve/harness-sdk/OpenResearch/smolvm/webcodex 等新框架情报）
- OpenClaw ClawHub：库内已落 §技能创建分发——marketplace 细节（publish/install/search/verify/source metadata）为独有增量 ≥40% → 落地（增量合并）

## 独点落地（9 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r272C-1 | wb-execute-discipline | 3.34.0+ | Dify 触发器三类型与发布限制 | 工作流 |
| r272C-2 | wb-execute-discipline | 3.34.0+ | n8n IF/Switch/Merge 分支与合并（增量合并 §分支） | 工作流 |
| r272C-3 | wb-execute-discipline | 3.34.0+ | LangFlow 模板规范与 Store API（增量合并 §模板） | 可复用 Skill |
| r272C-4 | wb-execute-discipline | 3.34.0+ | Activepieces MCP 平台与 Embeddable MCP | 工具 |
| r272C-5 | wb-execute-discipline | 3.34.0+ | Make 蓝图克隆与链接分享（增量合并 §场景蓝图） | 工作流 |
| r272C-6 | wb-execute-discipline | 3.34.0+ | Pipedream secret props 与秘密管理 | 可复用 Skill |
| r272C-7 | wb-execute-discipline | 3.34.0+ | Anthropic Usage & Cost API 监控（增量合并 §缓存定价） | 可复用 Skill |
| r272C-8 | wb-execute-discipline | 3.34.0+ | OpenClaw ClawHub 市场（增量合并 §技能创建分发） | 可复用 Skill |
| r272C-9 | wb-execute-discipline | 3.34.0+ | deeplearning LLMOps 可观测与反馈闭环（增量合并 §评估） | 可复用 Skill |

## 复核
九独点均有当日实拉来源；均为增量合并或新面落地；并入记录：GitHub agent 框架。垃圾：本轮未产生临时文件。
