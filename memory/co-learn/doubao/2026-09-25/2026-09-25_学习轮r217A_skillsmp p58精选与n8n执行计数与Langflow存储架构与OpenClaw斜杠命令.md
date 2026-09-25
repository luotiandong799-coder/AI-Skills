# 学习轮 r217A：skillsmp p58精选与n8n执行计数与Langflow存储架构与OpenClaw斜杠命令（2026-09-25）

## 实拉记录（12 次调用，10 成功 / 1 robots 禁 / 2 死链 / 1 越界）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/58（#5701-5752，5933/11871 取） | OK |
| 2 | dify.ai/blog 续读（100856-105386） | OK（Plugin System 设计/DeepResearch） |
| 3 | docs.n8n.io/build/understand-workflows/understand-executions.md | OK（执行计数规则/redaction） |
| 4 | docs.langflow.org/memory（4154B 全取） | OK（存储架构/凭证防入库/chat vs vector） |
| 5 | GitHub Trending 搜索（startupcorners/trendshift/yuxiaopeng） | OK（jevals/CowAgent/siyuan） |
| 6 | deeplearning.ai/charonhub | robots 禁（计数） |
| 7 | docs.openclaw.ai/slash-commands（4984/8635） | OK（三命令类型/Directives 剥离） |
| 8 | activepieces.com/docs offset 19123 | 越界（已读尽，计数） |
| 9 | skills.sh/anthropics/skills（97B） | OK（官方 18 技能安装榜） |
| 10 | agentskills.io/clients | 死链（计数，换 /clients） |
| 11 | agentskills.io/clients（4408/50186） | OK（Factory/Emdash/ZeroClaw） |
| 12 | skills.sh/agents | 死链（计数） |

## 独点（4 个）
### A1：skillsmp p58 精选：插件级配置模式 / hook 注入统计 / 知识图谱替代 Grep / 逻辑间隔压缩（来源：skillsmp.com/skills/page/58，2026-09-25 实拉）
- **configured-agent（anthropics/claude-code ★147,483）**：**`.claude/plugin-name.local.md` 模式——YAML frontmatter+markdown 内容存插件级配置，实现 per-project 可配置插件**。
- **pordee-stats（kerlos/pordee ★329）**：**真实 token 用量与节省——直接从 Claude Code session log 读取，非 AI 估算；输出由 mode-tracker hook 注入，模型本身不计算数字**（统计与展示解耦）。
- **context-engine（alirezarezvani/claude-skills ★26,225）**：**C-suite 顾问共享公司上下文——读 ~/.claude/company-context.md、检测 stale 上下文（>90 天）、对话中丰富上下文、外部 API 调用前强制隐私/匿名化规则**。
- **code-graph（handsontable/handsontable ★22,044）**：**预构建 code-review-graph 知识图谱（Tree-sitter，整个 monorepo）替代 Grep+Read 走调用链——2-6x 更便宜，捕获 grep 漏掉的动态分派；跨多文件任务都适用（修 bug/探索/重构/审 diff）**。
- **strategic-compact（ECC ★264,820）**：逻辑间隔手动上下文压缩——按任务阶段保留上下文而非任意自动压缩（与本地 context-compressor 同向）。
- **update-skills（microsoft/vscode ★192,746）**："learn!" 触发——会话中发现显著模式/陷阱时创建/更新仓库技能。
- **提升层**：工作流 / 可复用 Skill。

### A2：n8n 执行计数规则与数据 redaction（来源：docs.n8n.io understand-executions，2026-09-25 实拉）
- **配额只算 production executions**（触发器/调度/轮询自动启动的），手动跑不计。
- **按触发类型计数**：Schedule Trigger 每次触发算 1（不论结果）；Polling 节点（如 Google Drive Trigger）只在新数据时算 1；Webhook 每个入站请求算 1（含空 body `{}`），malformed 失败不计。
- **不计 quota**：manual / sub-workflow（Execute Sub-workflow 只算父级）/ error workflow / polls 无数据 / malformed 请求。
- **Execution data redaction**：隐藏输入输出数据、保留执行元数据（status/timing/node names）——敏感信息脱敏不丢审计信息。
- **提升层**：工具（自动化执行记账）。

### A3：Langflow 存储架构：数据表清单 / 凭证防入库 / chat memory vs vector 边界（来源：docs.langflow.org/memory，2026-09-25 实拉）
- **存储选项**：SQLite 默认（Desktop 与 OSS 路径不同、DB 绑定 venv 路径不共享）；外部 PostgreSQL（LANGFLOW_DATABASE_URL）；NOOP 数据库测试（LANGFLOW_USE_NOOP_DATABASE=True）；chat memory 可单独外置。
- **凭证防入库**：**`LANGFLOW_REMOVE_API_KEYS=True` 时，保存 flow 前把字段名含 api/key/token 的 password 字段置 null**——防凭证写进数据库。
- **关键表**：A2ATask/A2ACheckpoint（A2A 协议任务+human-in-the-loop 图检查点跨重启恢复）；IngestionRun（知识摄取历史）；MemoryBase*/MessageIngestionRecord（消息↔内存基 join 表防重复摄取）；Trace/Span；Variables（加密凭证）；Authz*/SSO*（授权治理）。
- **chat memory vs vector memory**：chat memory 按 session_id 分组、为对话历史优化；跨会话语义检索用 memory base（**Filter by Session 默认开**，关掉可跨会话）；**默认 session ID=flow ID（一流程一大会话），多用户应用用自定义 session ID（如 user ID）隔离上下文**。
- **缓存**：async 默认、redis 实验性（跨 worker）、disk 1.10 移除。
- **提升层**：工作流（记忆存储与隔离）。

### A4：OpenClaw 斜杠命令三类型与 Directives 剥离语义（来源：docs.openclaw.ai/slash-commands，2026-09-25 实拉）
- **三种命令类型**：①Commands（独立 `/...` 消息，必须消息唯一内容）②**Directives（/think /fast /verbose /trace /reasoning /elevated /exec /model /queue——在模型看到前从消息剥离；单独发送时持久化会话设置；/exec security/ask 只作用于当条消息）**③Inline shortcuts（/help /commands /status /whoami 立即运行+剥离）。Directives 剥离保留剩余文本缩进与行尾。
- **授权**：`commands.allowFrom` 配置时是唯一授权源；未配置走 channel allowlist+pairing；未授权 sender 的 directive 当纯文本。
- **配置默认值矩阵**：commands.text=true / native=auto（Discord/Telegram 开、Slack 关）/ bash=false（需 tools.elevated allowlist）/ config=false / mcp=false / plugins=false / debug=false / restart=true。
- **其他**：/learn [request] 从当前会话草拟可评审技能走 Skill Workshop；/btw 侧问题不改变会话上下文；/subagents list 检视子 agent 运行；/context 解释上下文如何组装。
- **提升层**：工具 / 工作流（命令面治理）。

## 判重说明
- A1 全新（p58 独有），落。
- A2 n8n 增量（执行计数按触发类型+redaction，r215 未覆盖），落。
- A3 langflow 增量（存储架构级，r216-A 只到 agents 页参数），落。
- A4 openclaw 增量（slash 命令页，r217 新增页），落。
- 未落：dify Plugin System 设计（与 r216-C Extension Plugin Endpoint 关联度高，增量并入后续）、trending jevals/CowAgent（描述有限）、skills.sh anthropics 安装榜（生态数据、辅助）、agentskills clients（产品名录为主）、activepieces（已读尽）、deeplearning charonhub robots 禁（计数）。
