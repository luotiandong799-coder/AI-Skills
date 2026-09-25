# 学习轮 r208-C：Anthropic MCP管理与skillsmp p30与腾讯SkillHub技能生态（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/30（#2901-2953） | OK（paper2skill/code-to-prd/smart-explore 等 50+） |
| 2 | make.com/en/help | OK（帮助中心目录，产品事实低增量） |
| 3 | docs.pipedream.com/workflows/build/ | 死链 |
| 4 | blog.n8n.io/error-handling-llm-tool-calling（URL 猜测） | 死链 |
| 5 | skillsmp.com/skills/page/30 续读（#2954-3000） | OK（litreview/mathmodel-figure/bizard） |
| 6 | blog.n8n.io 错误处理文章 | 死链 |
| 7 | docs.anthropic.com MCP 页（0-3996） | OK（传输选项/scope/重连/插件捆绑） |
| 8 | general_search 腾讯 SkillHub | OK（1.3 万技能镜像/鲁班/技能锻造炉） |
| 9 | docs.anthropic.com MCP 页续读（3996-9995） | OK（OAuth scope pin/Tool Search/输出上限） |
| 10 | agentskills.io/specification/ | OK（官方 spec 完整版，与 r205-B 重叠确认） |

## 独点（3 个）
### C1：Anthropic MCP 管理：OAuth scope pin 与 Tool Search 延迟加载与输出上限治理（来源：docs.anthropic.com MCP 页 2026-09-25，hooks 之外的工具面管理增量）
- **OAuth scope pin（最小授权）**：`oauth.scopes` 把授权范围钉死在安全团队批准的子集（RFC 6749 §3.3 空格分隔串），优先于 authServerMetadataUrl 与服务器 .well-known 广告的 scope；授权服务器支持 offline_access 时自动附加（免重新登录刷新 token）；工具调用遇 403 insufficient_scope 用同一 pin 重认证，需要更宽 scope 时显式放宽——**连接期一次授权，scope 可事后收紧**。
- **认证发现链与覆盖**：默认先 RFC 9728 Protected Resource Metadata（/.well-known/oauth-protected-resource）→ 回退 RFC 8414 authorization server metadata；`authServerMetadataUrl` 可显式覆盖（内部代理/标准端点报错时）；401/403 或 WWW-Authenticate 头自动标记需认证。
- **Tool Search 延迟加载**：默认启用——MCP 工具定义**只在需要时进上下文**，启动只载入工具名，加 MCP server 对上下文窗口影响最小；`ENABLE_TOOL_SEARCH=auto:N` 阈值模式（工具集 ≤ 窗口 N% 就全部预载，溢出才延迟）；需要 tool_reference 能力（Sonnet 4+/Opus 4+，Haiku 不支持）；**工具描述与 server instructions 各 2KB 截断**——关键细节放开头；server instructions 明确"何时搜索我的工具"让模型知道该调 ToolSearch。
- **输出上限治理**：默认 10,000 token 警告/25,000 上限；`MAX_MCP_OUTPUT_TOKENS` 调整；**单工具级 `_meta["anthropic/maxResultSizeChars"]` 注解**把该工具阈值提到注解值（硬上限 500,000 字符），超过默认阈值的大输出**落盘替换为文件引用**不爆上下文——数据库 schema/文件树这类天然大输出用注解免全局调限。
- **认证与重连机制**：OAuth token 安全存储自动刷新；--callback-port 固定回调端口（预注册 redirect URI）；--client-id/--client-secret（keychain，不进配置）；**headersHelper** 处理非 OAuth 认证（Kerberos/短时 token/内部 SSO）——连接时跑命令生成 JSON 头，10s 超时，每次连接重跑无缓存，CLAUDE_CODE_MCP_SERVER_NAME/URL 环境变量让一个脚本服务多 server；HTTP/SSE 断线指数退避重连最多 5 次（1s 起倍增），初始连接瞬时错误重试 3 次（认证/404 不重试）。
- **MCP scope 与优先级**：Local（~/.claude.json 单项目个人）> Project（.mcp.json 版本控制共享）> User（跨项目）> Plugin-provided > claude.ai connectors；三 scope 按名去重、插件/connectors 按端点去重；`.mcp.json` 支持 `${VAR}`/`${VAR:-default}` 展开（command/args/env/url/headers），缺必要变量无默认=解析失败；插件可捆绑 MCP server（CLAUDE_PLUGIN_ROOT/CLAUDE_PLUGIN_DATA 持久状态）；`claude mcp serve` 把 Claude Code 自身暴露为 stdio MCP server 给其他应用用。
- 判据：**远程 MCP 一律 pin scope**；MCP 多则开 Tool Search（auto 阈值按窗口比例）；大输出用单工具注解免全局调限；非 OAuth 认证走 headersHelper。
- **提升层**：工具。

### C2：skillsmp p30：smart-explore AST 结构化代码搜索与 litreview 免 key 检索与预算检查点（来源：skillsmp.com/skills/page/30 2026-09-25）
- **smart-explore（tree-sitter AST 结构化搜索）**：用 AST 解析做 token 优化的代码结构探索（找函数/理解结构/高效探索代码库）——**替代整文件读的省 token 方案**；与 learn-codebase（新代码库全文读 prime）分工：陌生项目先全文 prime，熟悉后探索用 AST。
- **litreview（免 key 文献检索+预算门控）**：默认免 key API（PubMed E-utilities+OpenAlex 免费检索），Consensus MCP 作可选增强通道；搜索计划用 PICO（默认）/SPIDER/Decomposition/hybrid 回退；**grill-me intake 前置**（研究问题特异性+框架提示+初步深度三问）→ 检索；**Phase 2 强制检查点**（确认框架+子领域+深度才继续消耗预算）；**深度可配置（5/10/20 queries）控制覆盖与速度**；输出"发射台"定位指南而非成品综述——让研究者自信深入。
- **figure-generation 三阶段出图**：query expansion→code generation with execution→VLM visual feedback（视觉模型看渲染结果给反馈迭代）——论文级图自动管线。
- **convert-word-to-md 多文件类型纪律**：docx→md 转换；**用户引用含多类型文件的文件夹（.pdf/.docx/.xlsx）时必须调用全部三个兄弟技能（convert-pdf-to-md+convert-word-to-md+convert-excel-to-md），不让任何文件类型被静默跳过**——多模态文件夹完整处理。
- **paper2skill / skillXiv**：arXiv/ML 论文→Claude 技能秒级转换——把论文技术提炼成可复用 agent 指令的管道，批量论文→技能库。
- **bys-personal-dashboard 数据归属判据**：个人工作台触发判定三特征（手机上用/每天打开/私人数据）；**判据=数据属于谁不是数据在哪**（个人记账 Excel 手机看=工作台；公司销售报表=不是）——工作台类任务边界。
- **code-to-prd 反向工程**：代码库→业务可读 PRD（routes/components/state/API/交互→工程师或 AI 可完整重建每一页/端点）。
- 附：mathmodel-figure（20 个 Nature 主题 matplotlib 模板，theme.json 声明配色可整体替换）+ bizard（257 可复现教程/798 真实生物医学图例，R/Python/Julia）——科研出图模板库判重时用。
- 判据：**探索用 AST 结构搜索省 token，新库全文 prime**；文献检索先 grill-me intake 再设预算检查点；多类型文件夹转换三兄弟全调防静默跳过；论文转技能是技能库扩充管道。
- **提升层**：可复用 Skill / 工作流。

### C3：腾讯 SkillHub 本土化技能生态与技能优化元技能（来源：general_search skillhub.tencent.com/腾讯云开发者社区 2026-09-25）
- **SkillHub（腾讯云轻量应用服务器团队）**：OpenClaw/ClawHub 官方生态的**本土化高速镜像+中文技能社区**；收录 **1.3 万+ 技能**持续增长；社区全量**安全扫描过滤风险/侵权内容**；官方 Plugin 支持 DeepSeek Harness（9.7 千 GitHub MIT 开源 Plugin，Plugin 广场搜索安装）。
- **腾讯生态 skill 化改造**：WorkBuddy（腾讯云个人 AI 助手，SkillHub CLI 安装管理技能）/ QClaw（AI 智能体框架，对接官方 ClawHub+兼容开源 Skills+MCP Server）/ ima（知识管理平台，知识号发布发现 Skill）；**10+ 腾讯产品完成 skill 化改造**；智能体开发平台内置 Skills 覆盖 SkillHub 社区+腾讯文档+IMA+QQ 浏览器+乐享，**自动检测新版本自动更新到技能广场**，全部经平台安全审核+质量验证。
- **安全约束（EdgeOne Skill）**：插件**严禁直接把 SecretId/SecretKey 提供给 AI**，必须浏览器 OAuth 统一授权保护凭证——云能力类技能的凭证纪律。
- **技能优化元技能**：鲁班.Skill（工业级技能优化器：10 维加权评分/自动优化/质量检查/skill review）；**技能锻造炉 Skill Forge**（创建/升级/重铸/审计技能的元技能：锻造模式=从零打造带版本反馈环/真实素材覆盖审计/外部标杆对比/自我迭代/生产签批/真机验证；审视模式=10 维加权评分尺给任意技能打分）——**技能本身的迭代闭环方法论**。
- 判据：**技能生态选有安全扫描+自动更新治理的**；云凭证一律浏览器 OAuth 不落文本；技能优化走"版本反馈环+真实素材审计+外部标杆对比+生产签批+真机验证"闭环而非单次改稿。
- **提升层**：可复用 Skill / 工作流。

## 判重说明
- C1 → r207-C Z1（PermissionRequest 六类规则）同源 MCP 管理侧增量（OAuth scope pin/Tool Search 延迟加载/输出上限治理/headersHelper/scope 优先级），落。
- C2 → 新（smart-explore AST 搜索/litreview 免 key 预算门控/paper2skill/数据归属判据），落。
- C3 → 与 r208-A A4（阿里云门户）不同平台（腾讯 SkillHub 镜像+元技能闭环），技能锻造炉与 wb-skill-authoring（caliper 评测）增量大（生产签批/真机验证/外部标杆），落。
- 未落：make.com help（产品目录低方法）、pipedream workflows/build（死链）、n8n 错误处理 URL 猜测（死链）、agentskills.io spec（与 r205-B S2 重叠>60% 确认）。
