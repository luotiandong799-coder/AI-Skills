# r265C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站，查询词与 r265A/B 及历批全错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（多 agent 编排面） | ✓ | **嵌套 agent 节点**（v1.3+：一个 agent 把另一个当 tool 调用→跨专业角色涌现行为）；**Agent Node workflows 的 Agentic RAG**（迭代分析意图→选工具/源→重写 query→评估证据，非一次性 retrieve-then-generate）；**New Agent 对话构建**（2026-08-27：聊天自动生成可复用 skills+保留上下文，就绪后加进 workflow 更大流程）；**YAML 串行调用链**（researcher→summarizer→validator，edges 定义 source/target 依赖）；**协调者模式**（coordinator 收请求→分给 research/data/writer 专家） |
| 2 | n8n（模板/可复用面） | ✓ | **模板质量判据四件**（清晰节点命名非"HTTP Request1"/显式错误处理/注释或 sticky notes 说明意图/近期版本——缺一宁可重建）；**生产化追加**（每失败点错误处理/指数退避重试/输入校验/idempotency 防重复 webhook/监控 dashboard）；**模板 vs 从零决策**（验证想法/学新 node/复制错误处理批量模式→模板；客户数据安全合规/Agent+Vector Store 复杂面→从零）；**pattern library**（"manager" 模式有状态处理+overlap protection/function+utility workflow 复用/错误日志；模板最终约 70% 重写）；**Pattern 1**（event-driven intake→normalize→route：收→canonical schema→IF/Switch 路由→写目标系统→structured audit） |
| 3 | LangFlow（自定义组件面） | ✓ | **自定义组件基类**（继承 Component；class 级属性标识描述；inputs/outputs 列表定义数据流；methods 定义行为；内部变量错误处理+logging）；**Extension 脚手架**（lfx extension init my-extension→extension.json v0 manifest+pyproject.toml pip 可装+src/lfx_my_extension 布局）；**Flow DevOps Toolkit SDK**（1.9：lfx init 建部署脚手架，environments.yaml 控制 dev/prod）；**组件包贡献**（bundle=相关组件分组）；**安全**（LANGFLOW_COMPONENTS_PATH 类别覆盖/allow-list 绕过 LANGFLOW_ALLOW_COMPONENTS_PATHS_OVERRIDE=false/组件类别 allow-list）；**ALTK**（Post-tool JSON 处理：大 JSON 工具响应现场生成 Python 代码提取相关数据减少上下文）；**langflow-builder-mcp**（MCP 调 add_custom_component 传 code 建组件） |
| 4 | Activepieces（自定义 piece 面） | ✓ | **Piece=标准 TS 模块**（createPiece({name, displayName, actions, triggers})；action=createAction({name, displayName, run})，inputs(props)→执行→outputs）；**CLI 脚手架**（npm run cli actions create/triggers create 三问）；**三触发器技术**（Polling 周期查/Webhook 单 URL 监听/App Webhooks Subscriptions——OAuth2 dev app 单 URL 收全部授权用户事件）；**Auth**（Add Piece Authentication）；**400+ MCP servers**（piece 经 MCP 暴露）；**MCP tools**（ap_search_actions/ap_search_triggers 自然语言搜索） |
| 5 | Make（模板/蓝图面） | ✓ | **Blueprint=可复用场景版本**（含 modules/settings/mapped values；导出备份/共享组织内外/重用于新账号）；**Use Template 流程**（画廊→复制 blueprint 进账号→OAuth/API key 连账号→调 filters/mappings/schedules→test mode→激活，15-30 分钟）；**API 克隆**（POST /scenarios/{source_id}/clone json{teamId,name}）；**生产级 blueprint**（subscenarios 稳定积木 upsert/create/send 归一化输出；可靠性默认：幂等键/error handlers 接 incomplete executions/重试/限流；instrumentation：correlation_id/结构化日志/告警路由/runbook replay-backfill；激活前导出→受控 clone+激活清单）；**粘贴重建**（Ctrl+V 粘贴后逐模块核对连接/webhook/API key） |
| 6 | Pipedream（Connect SDK 面） | ✓ | **Managed Auth**（OAuth 全程托管：hosted OAuth clients/加密存储/自动 refresh——用户秒连账号，你永不碰凭证；3,000+ APIs；自有或 approved OAuth clients）；**SDK**（PipedreamClient({clientId, clientSecret, projectId, projectEnvironment dev/prod})→tokens.create({externalUserId}) 每用户 connect token）；**Connect Link**（drop-in 或自建 UI；oauthAppId 必带）；**MCP server**（给 AI agent 10,000+ tools）；**REST API 取凭证**（client_credentials 换 token；检索 end-user OAuth tokens 免费至 1,000 connected accounts） |
| 7 | skills.sh（目录生态面） | ✓ | **定位**（Vercel 开源目录+leaderboard：SKILL.md 指令包任意 GitHub repo 发布，20+ coding agent 一键 npx skills add owner/repo）；**规模**（2026-06 ~669,670 skills；top=vercel-labs find-skills）；**API**（totalOwners/totalSkills/featuredRepo/featuredSkill）；**排行榜**（find-skills 1.3M+ 安装/vercel-react-best-practices 371K+/frontend-design anthropics 368K+）；**officialskills.sh**（56 dev teams/9 categories/660 official skills）；agentskill.sh（110,000+） |
| 8 | SkillsMP（目录生态面） | ✓ | **定位**（独立社区平台聚合 GitHub 开源 SKILL.md；规模 425,000+）；**特性**（AI semantic search/职业分类/类别浏览/公开 API/安装指南；支持 Claude Code/Codex CLI/ChatGPT；npx/bunx/pnpm 安装）；**skill-creator 官方**（anthropics/skills 2026-09-03：创建/修改/评估技能、run evals、variance analysis、优化 description 提升触发）；**ui-ux-pro-max**（nextlevelbuilder：79 searchable styles/192 product palettes 本地数据） |
| 9 | deepseek-plugin.org / DeepSeek Harness | ✓ | **DeepSeek Harness**（developer preview："Everything is a plugin"——models/tools/skills/sessions/sandboxes/storage/loops/scheduling/UI 全插件化可换可重组；npx @deepseek-ai/dsh web）；**dsh 插件市场**（deepseek-plugin.org：8,000+ dsh 插件，AI 生成 wiki+GitHub star 排行+安装命令；deepseek-plugin npm 包 agent 内搜索安装）；**Copilot 集成**（DeepSeek V4 Pro/Flash 进 Copilot Chat 模型选择器，保留 agent mode/tool calling/skills/MCP）；**dsh-tui**（Claude Code 风格界面公共 beta MIT）；**dsh.do**（插件画廊：深链分享/README 自动封面/标签反查） |
| 10 | Hugging Face（smolagents 面） | ✓ | **CodeAgent vs ToolCallingAgent**（code agent 写 Python 代码作为行动 vs JSON/Text tool call——单次生成可调 3 工具+循环+算术+中间变量一步完成；HF/DeepMind 基准 ~30% 更少步骤同等准确率）；**轻量**（~1000 行）；**模型无关**（transformers/Ollama/HF providers/OpenAI/Anthropic/Bedrock/Azure via LiteLLM）；**工具无关**（MCP/LangChain/HF Hub Space）；**沙箱执行**（Blaxel/E2B/Modal/Docker；LocalPythonExecutor AST）；**Hub 共享**（tools+agents 经 Hub 加载）；**agents-course unit2** |

## 判重基准
双键检索：Dify 多 agent（§6175 并行分支/§6322 DSL 迁移管"并行与版本"——嵌套 agent+Agentic RAG+New Agent 构建为新增量≥40%，合并保留增量落）；n8n 模板（§6295 子工作流工程管"拆分边界"——模板四件判据+生产化清单+70% 重写预期新面落）；LangFlow 组件（§6191 多 Agent 编排/§6229 RAG 评测——Component 基类+Extension+DevOps Toolkit+allow-list 新面落）；Activepieces piece（§6198 版本/§6260 重试/§6302 验签——piece 开发+三触发器新面落）；Make blueprint（§6093 场景并发——blueprint 生产化+API clone 新面落）；DeepSeek Harness（§6366 Claude 插件源/§6379 ModelScope 生态——全插件化架构新面落）；smolagents（**§6349 已落 CodeAgent 代码即行动/~30% 少步骤——纯重复不落**）；Pipedream Connect（r265B 触发器已落——Connect SDK 托管 OAuth 并入记录）；skills.sh/SkillsMP（历批目录面——规模数字增量并入记录）。

## 独点落地（6 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r265C-1 | wb-execute-discipline | 3.20.0+ | Dify 多 agent 编排：嵌套 agent+Agentic RAG+New Agent 构建（增量） | 工作流 |
| r265C-2 | wb-execute-discipline | 3.20.0+ | n8n 模板质量判据与生产化清单 | 可复用 Skill |
| r265C-3 | wb-execute-discipline | 3.20.0+ | LangFlow 自定义组件与 Extension 脚手架 | 可复用 Skill |
| r265C-4 | wb-execute-discipline | 3.20.0+ | Activepieces 自定义 piece 与三触发器技术 | 工具 |
| r265C-5 | wb-execute-discipline | 3.20.0+ | Make blueprint 生产化框架 | 工作流 |
| r265C-6 | wb-execute-discipline | 3.20.0+ | DeepSeek Harness 全插件化架构 | 可复用 Skill |

## 复核
六独点均有当日实拉来源（逐站 URL 见各站摘要）；r265C-1 增量合并落地，r265C-2/3/4/5/6 新面；smolagents §6349 已覆盖纯重复不落；备选并入记录不单独落地（Pipedream Connect/skills.sh/SkillsMP）。垃圾：本轮未产生临时文件。
