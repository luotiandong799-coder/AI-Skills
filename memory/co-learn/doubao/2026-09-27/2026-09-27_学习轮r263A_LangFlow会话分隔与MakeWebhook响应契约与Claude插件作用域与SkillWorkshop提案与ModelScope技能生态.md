# r263A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（多 agent 编排面） | ✓ | nested agent nodes（agent 可作 tool 被另一 agent 调用）；coordinator agent 模式；sub-workflow 可复用组件从父 workflow 调用；整条多 agent workflow 可暴露 REST API；multi-agent 支持"存在但基础"（对比 CrewAI/AutoGen 缺高级协调）；物流实例子代理编排 |
| 2 | n8n（模板市场面） | ✓ | 官方库 11,741 community workflows（2026-08）六类（AI 8,002 占 70%）AI/Sales/IT Ops/Marketing/Document Ops/Support；模板按类别组织+版本/评价/文档；付费市场 Gumroad $9-200+ 垂直包；第三方 n8nresources 5,600+/n8nmarkets 850+ |
| 3 | LangFlow（chat memory 面） | ✓ | 默认 session_id=flow ID（所有消息一个大 session 多用户易串）；custom session ID 分隔（user ID 作 session ID 隔离上下文）；Agent 组件内置 chat memory 默认启用（滚动上下文窗口按 session ID）；Message History 组件（chronological messages 表）vs Memory Bases（vectorized 语义检索跨会话）；monitor API 按 flow_id/session_id/sender/sender_name 过滤排序 |
| 4 | Activepieces（触发类型面） | ✓ | 三技术：Polling（轮询查变化）/Webhooks（单 URL 监听）/App Webhooks（OAuth2 订阅未支持）；TriggerStrategy.POLLING/WEBHOOK；webhook trigger 生命周期 On Enable（context.webhookUrl 注册+store 存 webhook Id）/On Handshake；Catch Webhook 任意 HTTP method（GET/POST/PUT/DELETE）；Return Response 动作；Event Streaming 审计事件转发（flow lifecycle/run status/folder/connection/user activity/platform admin actions）+Audit Log Events catalog |
| 5 | Make（webhook 响应面） | ✓ | 响应模块四字段 type（json/urlencoded/text 默认 json）/status/headers/body；content-type 头指定 application/json；redirect 用 status 3xx+location 头；JSON Pass-through YES 默认 No（原始 body 透传）；webhook 日志保留：enterprise 30 天/其他 3 天；Get webhook logs API /hooks/{hookId}/logs；原始 JSON 存 data store 防丢 |
| 6 | Pipedream（组件系统面） | ✓ | 两种类型：sources（需实例化独立资源=workflow 触发器也可独立 serverless）+actions（仅能作 workflow 步骤不能独立运行）；Registry 公开 GitHub repo 10,000+ 预建 triggers/actions；props 捕获用户输入；managed auth；contributing guidelines（action 需 type:action+description 含文档链接格式）；Edit with AI 自然语言改 workflow 代码步骤 |
| 7 | Claude Code（插件市场面） | ✓ | /plugin marketplace add <owner/repo>（#ref pin branch/tag）；marketplace 源四类（GitHub repo/git repo 任意 host/本地目录文件/hosted marketplace.json）；plugin install @ --scope local（gitignored 个人）/project（提交共享团队）/user（跨项目个人）三作用域；plugin uninstall @；官方 Anthropic marketplace 或 org 内部 marketplace（settings.json 链接自动加）；plugin skill 下载时机=change applied 或 restart；skill 命令来自目录名+frontmatter name |
| 8 | Copilot（组织级指令面） | ✓ | VS Code 三存储：workspace AGENTS.md（多 agent 自动应用全 workspace 或子文件夹 experimental）/repo .github/copilot-instructions.md（自动识别全 workspace）/path-specific .github/instructions/**/*.instructions.md；org-level 定义于 GitHub organization 跨多个 workspace/repos；Agent Host 格式分派 Copilot .github/instructions vs Claude .claude/rules；user 级 ~/.copilot/instructions；设置开关 includeApplyingInstructions/includeReferencedInstructions/codeGeneration.useInstructionFiles 默认 true；.prompt.md 可复用 prompt 文件 |
| 9 | OpenClaw（Skill Workshop 面） | ✓ | propose-create（name/description/proposal 文件）→ inspect → apply 生命周期；proposal-only frontmatter（status: proposal/version/date）；apply 时写 active SKILL.md；agent-drafted skills 或 operator review 场景用提案而非直接写；ClawHub 发布前检查 SKILL.md 完整（name/description/availability 控制字段） |
| 10 | ModelScope（Skills 生态面） | ✓ | Skills Central 83,099 个技能（社区）+MS-Agent × Skills 解锁；Awesome Skills 合集安装三式（npx skills add collection URL / pip modelscope + download --collection / curl install.sh）；技能格式=Markdown+YAML 头（name 字段调用名/description 判断何时自动调用），复杂技能带脚本文件；Ultron=群体智能基础设施（智能体共享经验/技能/画像解决换会话失忆）；AIPC Skills 本地 OCR+RAG（localhost 不离开本机）；Agent 大本营勾选内置 tool 发布需 API key；ModelScopeGPT LLM controller 连接多领域模型 |

## 判重基准
双键检索：LangFlow session_id 分隔（无前置章节新面）；Make webhook 响应契约（§6236 Make Webhook 安全管认证验签——响应四字段/日志保留/JSON Pass-through 为独有增量合并）；Claude Code 插件源与作用域（无前置章节新面）；OpenClaw Skill Workshop 提案生命周期（无前置章节新面，与既有 ClawHub/技能开发互补）；ModelScope Skills 生态（§r252C ModelScope 微调为模型面——Skills 83,099/安装三式/Ultron 为独有增量新面）。备选并入记录：n8n 模板市场数据（11,741 六分类/付费包）、Dify 嵌套 agent、Copilot 组织级指令体系（AGENTS.md 分派）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 |
|---|---|---|
| ① LangFlow session_id 分隔纪律 | 默认 flow ID 串扰/custom 分隔/三存储面 | 工作流 |
| ② Make webhook 响应契约 | 四字段/JSON Pass-through/日志保留/API | 工作流 |
| ③ Claude Code 插件源与作用域 | marketplace 四源/三 scope/org 内部市场 | 工具 |
| ④ OpenClaw Skill Workshop 提案 | 提案生命周期/frontmatter/operator review | 可复用 Skill |
| ⑤ ModelScope Skills 生态 | 83,099 技能/安装三式/Ultron 群体智能 | 工具 |

## 复核
五独点均有当日实拉来源；②按增量判定并入保留增量；①③④⑤为新面；备选并入记录。垃圾：本轮未产生临时文件。
