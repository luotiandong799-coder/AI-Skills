# r284B 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r284A + 更早全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（RAG 检索优化） | OK | **多路径检索（Multi-path Retrieval）：关键词&语义加权评分 + Rerank 模型选择（Cohere/Jina）**；**Summary Index（1.12.0）=轻量替代 GraphRAG：每个 chunk 附加 summary 字段，summary 匹配时同/语义相关 chunks 一起检索（碎片检索→全文上下文）**；检索模式三分：向量（语义相似）/全文（精确匹配：产品码/ID）/混合（精度与召回平衡）；**metadata 过滤（product: billing、type: FAQ 标签）**；**清洗源文档（页眉/页脚/页码/导航噪声）**；**用固定代表性问题集测试分块（对比各设置）**；rerank 模型选型：多模态知识库选 Vision 标记模型否则图片被排除 rerank；Top K 自动调整；索引方法两档：High-Quality（向量）/ Economical（关键词） |
| 2 | n8n（错误处理/重试） | OK | **三层错误处理：node-level Retry on Fail（瞬时错误最便宜的可靠性收益；Max Tries 上限 5、Wait Between Tries 上限 5s）+ Error Workflow（全局集中错误处理+通知）+ workflow-level retry loops（Code/Wait/IF，指数退避 waitSeconds=min(maxDelay, baseDelay×2^(attempt-1))）**；**默认可重试状态码 408/409/425/429/500/502/503/504；不可重试 400/401/403/404/422**；EXECUTIONS_DATA_SAVE_ON_ERROR=all（保存失败数据以便 UI 重试）；**AI 分诊+重试计数（每事件最多 3 次、指数退避、n8n API 重试失败执行、OpenTelemetry 遥测）**；continueOnFail 谨慎（仅非关键步骤）；重试间隔≥1-5 秒；最终 fallback=紧急通知节点 |
| 3 | LangFlow（多 Agent 编排） | OK | **五 agent 深度研究流水线：Research Planner 拆 3-7 子问题 → Source Finder（web 搜索取高信号链接）→ Summarization（工具调用提取关键事实）→ Reviewer（找缺口提后续问题）→ Professional Writer（综合成报告）——每个 agent 单一职责+明确交接**；**agent 作为 tool 递归编排（agents calling agents，1.1 起 tool mode）**；**Supervisor 模式：User query → Supervisor → Research/Code/Writer agents**；CUGA 企业工作流（Planner 更新计划 + Plan Controller 管理子任务序列/状态）；CrewAI hierarchical crew（Roles/Goals/Backstories + Manager 角色）；Sequential agents（链式推理：每个 agent 接独特 tool + Prompt 控制行为） |
| 4 | Activepieces（触发器） | OK | **Trigger Technique 二选一：polling（周期查端点）或 webhook（单 URL 监听事件）**；**Webhook 触发器机制：On Enable 用 context.webhookUrl 注册第三方 webhook + store webhook Id；On Handshake 有些服务需成功握手**；App Webhooks（订阅式，OAuth2 开发者 app 单 URL 收所有授权事件，当前 Not Supported）；Catch Webhook（GET/POST/PUT/DELETE 任意方法）+ Return Response action；**MCP ap_search_triggers（自然语言搜触发器："when a new row is added to a Google Sheet"）**；触发器=启动 flow，actions=触发后执行任务；预建触发器跨数十流行 app |
| 5 | Make（HTTP/Router） | OK | **HTTP v4=新版本（简化 setup、更安全 keychain 存储、原生 pagination）；旧版 v3 HTTP legacy 可切换**；Headers（User-Agent/Cache-Control）+ Query parameters 配置；**Router=分支多条 chain：每条 route 首连线 Filter 设条件（less than/greater than 等运算符）+ fallback route 处理不匹配其他 route 的数据**；Router 两分支场景：数据找到/没找到 + Filter 前置；**错误处理模式：router 后两 routes（数据正常 + 错误处理路径 Sleep+重试）**；Throw 模拟（JSON parse 配 bundlevalidationerror 可选抛错）；Resolve URL（跟随所有重定向返回最终 URL） |
| 6 | Pipedream（状态/重放） | OK | **pd.flow.rerun / $.flow.rerun=单步多次运行（外部 API 轮询完成或服务回调处理）**；**$.flow.suspend()/resume=显式暂停点；真 checkpoint/resume 只存在于显式暂停点**；**Event History 批量操作：Replay（选中事件重放：修复 bug 后重跑失败事件）+ Delete（清除/scrub 事件）**；重放=从原始入站事件数据重新执行（不是从失败步骤恢复 mid-run）；v2 builder：test/save 不 deploy、事件菜单 Replay Event；trigger.context（deadline/JIT/run 元数据）；批量 unpause/restart 不支持（只能代码内 rerun/suspend）；部署模型：Deploy 按钮 Draft→Active、GitHub Sync 做完整历史/回滚 |
| 7 | Anthropic（SKILL.md 规范） | OK | **SKILL.md 命名必须精确（case-sensitive，SKILL.MD/skill.md 不接受）**；**文件夹 kebab-case（notion-project-setup ✓/Notion Project Setup ✗）且与 name 匹配**；**frontmatter 硬约束：name≤64 字符（仅小写字母/数字/连字符、不能含 XML 标签、不能含保留词 "anthropic"/"claude"）；description 非空≤1024 字符、不能含 XML 标签**；上传总量<30MB（未压缩）；**自定义 skill=目录（SKILL.md+附属文件）zip 或单文件上传，创建返回 skill_* ID**；**版本格式：Anthropic Skills=日期型（20251013/latest）；Custom Skills=epoch 时间戳（1759178010641129/latest）**；预建技能 pptx/xlsx/docx/pdf；**启动时 agent 预加载 name+description** |
| 8 | GitHub（agent 生态） | OK | **n8n 187.8K stars（AI agent top100 #1）；langflow 153K（visual builder）；OpenClaw 382K（harnesses.sh #1，9-axis capability schema、75 harnesses 档案）**；**herdr 40.9K Rust（the runtime your coding agents live on）；agency-agents 149K（300+ agent personas 一个命令装）；awesome-harness-engineering（memory/evals/verification/orchestration 纪律清单）**；RAG_Techniques 29.6K（高级 RAG 技术 notebook 教程）；freellmapi 29.1K（34 free LLM providers/635 free endpoints/smart routing/failover/加密 keys）；**TiDB 为 agentic workloads 构建（ACID+事务+分析+向量搜索）**；ZeroClaw（Rust 重写、secure by default）；NanoClaw（每对话独立容器 OS 级隔离）；TrustClaw（云服务 OAuth 托管凭据+远程沙箱） |
| 9 | OpenClaw（插件系统） | OK | **defineToolPlugin=构建仅加 agent 可调用工具的插件（无 channel/model provider/hook/service/setup backend，生成 manifest 元数据供发现不加载运行时）**；**插件可注册：Gateway RPC methods / Gateway HTTP handlers / Agent tools / CLI commands / Background services / Optional config validation / Skills（manifest 列 skills 目录）/ Auto-reply commands**；api.registerCommand（name/description/acceptsArgs/requireAuth/handler）；CLI 命令（api.registerCli、program.command）；**安装：openclaw plugins install ./custom-plugin（--link 链接模式）、marketplace：openclaw skills search/install、openclaw plugins marketplace list/install plugin@marketplace**；**类型化边界：可 discover/validate/test/disable/upgrade** |
| 10 | WaytoAGI（知识库/提示工程） | OK | **WaytoAGI=中文多模态 AI 知识库（文章精选 articles.waytoagi.com + Chat with Wiki 问答 + AI 学习路径：李宏毅课程等）**；"通往 AGI 之路"学习六步：记忆→理解→应用→分析→评价→创造；**Meta-Prompting：用模型生成/完善/批评 prompts（"Rewrite this prompt to be more specific"/"What's missing?"）**；**Directional Stimulus Prompting：小刺激槽引导 tone/证据规则/简洁性而不改主 prompt**；提示设计六要素：Task objective/context/role/audience/examples/output format；系统提示设计原则（System vs user prompts、role setting、constraints、output specifications）；prompt chaining/negative prompting/parameter tweaking（temperature/top-p）；提示工程八阶段路线（基础→各平台→进阶技术→项目实践） |

## 判重（双键检索，增量判定）
- Dify 检索策略（r284A DSL 版本控制）→ Summary Index+加权/rerank+metadata 过滤为新面 → **新面**
- n8n 错误处理（r284A 表达式）→ 状态码分层+三层重试+AI 分诊为新面 → **新面**
- LangFlow 多 Agent（r284A 记忆）→ 五 agent 流水线+agent-as-tool+Supervisor 为新面 → **新面**
- Activepieces 触发器（r284A 分支循环）→ polling/webhook 机制+ap_search_triggers 为新面 → **新面**
- Make Router（r284A Data Store）→ fallback route+filter 条件+错误处理路由为新面 → **新面**
- Pipedream 重放（r284A components）→ Event History replay+suspend/resume+GitHub Sync 为新面 → **新面**
- Anthropic SKILL.md 规范（r284A Claude MCP 配置）→ 64/1024 字符硬约束+30MB+kebab-case+版本格式为新面 → **新面**
- GitHub 生态（r284A Agentic Workflows）→ harnesses.sh/herdr/agency-agents/TiDB agentic 为新面 → **新面**
- OpenClaw 插件（r284A 记忆架构）→ defineToolPlugin+marketplace+类型化边界为新面 → **新面**
- 提示工程进阶（r284A Agent Skills 生态）→ Meta-prompting+DSP+六要素为新面 → **新面**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 多路径检索与 Summary Index | 工作流 |
| 2 | n8n 三层错误处理与状态码分层 | 工作流 |
| 3 | LangFlow 多 Agent 流水线编排 | 工作流 |
| 4 | Activepieces 触发器类型与机制 | 工具 |
| 5 | Make Router 分支与 fallback | 工具 |
| 6 | Pipedream 事件重放与显式暂停 | 工作流 |
| 7 | Anthropic SKILL.md 规范硬约束 | 可复用 Skill |
| 8 | GitHub agent 生态新锐信号 | 工作流 |
| 9 | OpenClaw 插件系统与类型化边界 | 工具 |
| 10 | 提示工程进阶（Meta/DSP/六要素） | 模型 |

## 复核
十独点均有当日实拉来源；全部新面（零增量合并、零纯重复）。版本建议 3.68.0。