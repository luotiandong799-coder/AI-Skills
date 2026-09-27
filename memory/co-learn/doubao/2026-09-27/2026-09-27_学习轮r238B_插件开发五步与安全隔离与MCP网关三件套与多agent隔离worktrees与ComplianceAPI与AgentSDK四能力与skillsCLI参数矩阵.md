# r238-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（插件开发面） | ✓ | 插件开发五步（Setup CLI→Define manifest/schema→Develop hot reload→Test remote debugging→Publish Marketplace/GitHub）；安全隔离三机制（沙箱+权限模型显式能力授予+资源限制 CPU/内存/网络）；Data Source 插件 .difypkg 打包；SchemaRAG 插件（数据库结构自动分析建知识库+NL2SQL 多库自动适配 MySQL/PostgreSQL/MSSQL/Oracle/DM）；RAG 扩展（自定义解析器 CAD/医疗报告+自定义 chunking） |
| 2 | n8n（MCP Server/网关面） | ✓ | n8n MCP Server（first-party 原生内建 Cloud/Enterprise/Community 免费自托管）；Intelligent MCP Gateway 模板（REST API→结构化 AI 可访问；Claude 意图验证+参数校验；Google Sheets 工具注册表+rate limit 跟踪+审计日志；SMTP 违规告警；webhook URL 给 MCP client）；Enterprise MCP 编排（RBAC 策略表+session registry+审计+JWT+tenant 隔离）；gateway credits 云预付余额跑 AI 模型 |
| 3 | GitHub（生态/排行榜面） | ✓ | dify 152K/langchain 144K；CrewAI 44K+（角色目标 agent 组队委托独立 LangChain）；OpenClacky（prompt caching+16 核心工具+skill extensions）；Orca（桌面 agent IDE 同跑 30+ coding agents 隔离 git worktrees+terminal splits+embedded Chromium+SSH remotes）；agno 42K/langgraph 42K；ReviewCerberus（AI code review git branch 差异安全/性能/质量）；Awesome LLM Apps 100+ 端到端测试 |
| 4 | Anthropic（Claude Code 权限/合规面） | ✓ | Enterprise 治理（SOC 2 Type II+SSO+RBAC+组织级策略；SCIM 自动供应+audit trails+seat allocation；session/token/成本跟踪；BYOK）；Compliance API（本地 session endpoints 返回 transcripts 含 Chrome sessions）；Agent SDK 四能力（内置工具 read/write/edit/run/search web+hooks 生命周期+subagents+MCP）；managed-settings.json disableWorkflows 组织级禁用；auto mode 对 token/成本/延迟有小影响 |
| 5 | Pipedream（AI 编辑工作流面） | ✓ | Edit with AI（workflow builder 内 AI 编辑既有工作流：Workflow-level 修改整流程+Code step 单代码步+Debug with AI 报错帮助+Seamless 在 String.com 编辑部署回 Pipedream）；AI Agent Builder（prompt→run/edit/deploy 秒级）；AI Code Generation（任何 API 生成代码）；目的地 $send.s3()/$send.http()（S3/HTTP/email/SSE 抽象连接/批处理/交付）；10,000+ 预置组件 3,000+ APIs |
| 6 | Make（场景模板/LLM 集成面） | ✓ | LLM 集成五步（Make AI Toolkit Categorize Text 分类入站邮件→验证→路由；无需外部 API key 全计划）；AI 自动化例（Typeform→Claude 分类意图紧急性→HubSpot enriched 联系人→Slack 正确 rep；Salesforce deal→OpenAI 草稿→Gmail 送审）；SEO 聚类（GSC 查询→去重→OpenAI 按搜索意图分组→JSON 簇→Iterator 展开→Filter ≥3 查询且均位<20）；MCP client 场景（日历+AI 调 CRM MCP 工具+邮件简报）；Sales outreach agent（Gmail 盯 leads→分析→web 研究→qualify→查日历→草稿→Slack 送审）；Gartner 40% 企业 app 嵌入任务型 agent |
| 7 | skills.sh/LobeHub（安装 CLI 面） | ✓ | npx skills 命令族（find 交互/关键词搜；add --skill 单技能；--all -y 全装；--agent claude-code/cursor；--global 全局；check/update）；LobeHub Skills Marketplace 334,137 Skills agent-first 开放；market-cli（npx -y @lobehub/market-cli skills install --agent cursor）；ClawHub CLI npm（search/install --dir/list/update/info；hash-based 本地文件匹配升级）；install_skill MCP tool 支持 skills.sh URL/GitHub URL/owner/repo@skill 格式 |
| 8 | OpenClaw（Plugins 开发/发布面） | ✓ | 插件可加消息渠道/model provider/本地 CLI backend/agent tool/hook；发布流程（clawhub package publish --dry-run→正式；ClawHub 验证 owner scope/包名/版本/文件限制/source metadata；新版本隐藏到 review 完成）；安装 openclaw plugins install clawhub:<package> 裸包名 npm；发布前要求 package metadata+plugin manifest+setup docs+维护 owner；ClawHub 36,000+ 社区技能（2026-03）版本化存储+搜索/标签/使用信号；技能销售 80% revenue share |
| 9 | deeplearning.ai（新课程面） | ✓ | Agent Memory: Building Memory-Aware Agents（Oracle 合作：记忆工程=一等基础设施外部于模型/持久/结构化；Oracle AI Database+LangChain+LLM pipelines）；A2A: The Agent2Agent Protocol；Agent Skills with Anthropic（Elie Schoppik：skills=文件夹指令扩展；开放标准一次构建任意兼容 agent 部署；Skills vs Tools/MCP/Subagents；预构建+自定义+Claude API+Agent SDK）；Build Interactive Agents with Generative UI（生成自定义 UI 图表/表单/白板）；Agentic AI Module 2 reflection 评估影响 |
| 10 | 腾讯 SkillHub（安装/生态面） | ✓ | WorkBuddy/QClaw/ima 生态（WorkBuddy SkillHub CLI 装技能直接调用；QClaw 对接 ClawHub 兼容开源 Skills+MCP Server；ima 知识号发布/发现 Skill）；WorkBuddy 装法（方式 1 内置技能市场一键装单次≤10 个优先核心款避免冲突；方式 2 SkillHub/ClawHub 命令行复制官方命令切 GLM-5.0-Turbo 粘贴自动装）；五种导入（对话安装/网页搜索/ZIP 上传/CLI/官方安装脚本提示词 `根据 https://skillhub.cn/install/skillhub.md 安装 Skillhub商店`）；ClawPro（对话式/ZIP 上传/预置 SkillHub 社区官方精选 50 个高速下载） |

## 判重基准
双键检索：Dify（多轮已落，独有增量=开发五步 hot reload+remote debug+SchemaRAG 实例）；n8n（多轮已落，独有增量=MCP 网关三件套工具注册表 Google Sheets+意图验证+审计）；GitHub（多轮已落，独有增量=Orca 30+ agents 隔离 worktrees+OpenClacky prompt caching）；Anthropic（r238-A 已落，本轮合规面独有增量=Compliance API+Agent SDK 四能力+managed-settings 禁用）；Pipedream（r238-A 已落，本轮 Edit with AI 与既有重叠并入不单列）；Make（多轮已落，AI Toolkit 免 key 分类与既有重叠并入不单列）；skills.sh（多轮已落，独有增量=CLI 参数矩阵+market-cli 指定 agent）；OpenClaw（多轮已落，独有增量=发布验证流程+80% 分成+36K 规模）；deeplearning（多轮已落，独有增量=Agent Memory 记忆工程三特性+A2A 课程）；腾讯 SkillHub（r237-A 已落，独有增量=安装方法论 ≤10 限制+对话提示词+五方式）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 插件开发五步+安全隔离 | Setup→Define→Develop(hot reload)→Test(remote debug)→Publish；沙箱+权限显式授予+资源限制；SchemaRAG NL2SQL 实例 | 工具 | wb-execute-discipline |
| ② n8n MCP 网关三件套 | REST→结构化 AI 可访问；Claude 意图验证+Google Sheets 工具注册表+SMTP 违规告警；企业 RBAC+JWT+tenant | 工作流 | wb-execute-discipline |
| ③ 多 agent 隔离 worktrees+prompt caching | Orca 同跑 30+ coding agents 隔离 git worktrees；OpenClacky prompt caching+16 工具+skill extensions | 工具 | wb-execute-discipline |
| ④ Compliance API+Agent SDK 四能力 | 本地会话端点 transcripts；hooks/subagents/MCP 能力；managed-settings 组织禁用；日志+身份治理双轨 | 工具 | wb-execute-discipline |
| ⑤ skills CLI 参数矩阵 | skills add --skill/--agent/--global；market-cli 指定 agent；SkillHub 单次≤10 防冲突+对话安装提示词 | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：wb-context-compressor 长度控制合并评估继续挂账（多批未决）；本轮 skills CLI --global/--agent 参数与技能管理直接相关，可作批末功能套件评估输入；wb-ponytail/wb-max-token-saver 无变化需求。
- 垃圾：本轮未产生临时文件。
