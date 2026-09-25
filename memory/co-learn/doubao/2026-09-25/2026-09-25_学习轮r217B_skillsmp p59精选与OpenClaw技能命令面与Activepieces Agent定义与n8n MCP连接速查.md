# 学习轮 r217B：skillsmp p59精选与OpenClaw技能命令面与Activepieces Agent定义与n8n MCP连接速查（2026-09-25）

## 实拉记录（10 次调用，10 成功）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/59（#5801-5850，5985/11194 取） | OK |
| 2 | dify.ai/blog 续读（105386-109882） | OK（多语言翻译/多模态 R1/API 不稳三策略） |
| 3 | docs.langflow.org/manage-session-id | 死链（计数，换 n8n） |
| 4 | docs.n8n.io/connect/connect-to-n8n-mcp-server/mcp-client-examples.md（3173B 全取） | OK |
| 5 | GitHub Trending 搜索（github.hot/trendshift/llmnews） | OK（Octop/arcbox/scientific-agent-skills） |
| 6 | deeplearning.ai/the-batch（1798B） | OK（The Batch 内容流/loop engineering） |
| 7 | docs.openclaw.ai/slash-commands 续读（4984-8635 全） | OK（skill 命令/loop/btw/plugins 信任分级） |
| 8 | activepieces.com/docs/agents/overview（1326B） | OK（Agent 定义/Flow vs Agent） |
| 9 | skills.sh 续读（offset 8259） | OK（仅图片，已读尽计次） |
| 10 | agentskills.io/clients 续读（4408-8778） | OK（Qodo/Tabnine/OpenHands） |

## 独点（4 个）
### B1：skillsmp p59 精选：frontmatter 结构化检索 / markdown→HTML 演示 / AI 安全推理扫描 / 承诺式策略备忘录（来源：skillsmp.com/skills/page/59，2026-09-25 实拉）
- **memory-metadata-search（basicmachines-co/basic-memory ★4,014）**：**Basic Memory 结构化元数据搜索——按自定义 frontmatter 字段（equality/range/array/nested 过滤）查笔记而非全文**——状态/优先级/置信度类字段检索，和全文语义搜索互补。
- **md-slides（alirezarezvani/claude-skills ★26,225）**：**markdown deck → 单文件 HTML 演示**——`---` HR 或 `# H1` 分隔 slide、`<!-- notes: -->` presenter notes、键盘导航（arrow/space/PgDn/Home/End/P/Esc）、presenter mode（当前 slide+演讲者备注+时钟+下一 slide 预览）、URL-hash 深链、`@media print` 每页一 slide PDF 导出。
- **security-review（github/awesome-copilot ★39,255）**：**AI 代码库安全扫描器像安全研究员一样推理**——追踪数据流、理解组件交互、捕获 pattern-matching 工具漏掉的漏洞；覆盖注入/认证访问控制/secrets/弱加密/依赖/业务逻辑，跨 JS/TS/Python/Java/PHP/Go/Ruby/Rust。
- **strategy-memo（mohitagw15856/pm-claude-skills ★1,320）**：**策略备忘录=承诺一个 bet + 明确不做什么（explicit non-goals）**——战略问题、诊断、赌注/路径、为什么现在、non-goals、怎么知道有效、风险。
- **audio-jingle（nexu-io/open-design ★97,471）**：音频生成路由——音乐→Suno V5/Udio/Lyria、语音→MiniMax TTS/FishAudio/ElevenLabs V3、SFX→ElevenLabs SFX/AudioCraft，单 MP3/WAV 落盘。
- **提升层**：工具 / 可复用 Skill。

### B2：OpenClaw 技能命令面：确定性路由 / 自定节奏 loop / 侧问题不入历史 / 插件来源信任分级（来源：docs.openclaw.ai/slash-commands，2026-09-25 实拉）
- **skill command-dispatch: tool**：技能默认经 `/skill <name>` 路由到模型当普通请求；**技能可声明 `command-dispatch: tool` 直接路由到工具（确定性、无模型参与）**。名字净化 `a-z0-9_` 最长 32，冲突加数字后缀。
- **/tools 回答运行时问题**：这个 agent 此刻这个会话能用什么——不是静态配置目录；改 agent/channel/thread/sender 授权/模型都会改变输出。
- **/loop 自定节奏**：`/loop 5m check deploy status` 创建固定节奏 cron；无间隔时 `self-paced`——活跃时更频、安静时退避到 1h。
- **/btw 侧问题**：用当前会话做背景、不改未来会话上下文、**不写入 transcript 历史**（Codex harness 里走 ephemeral 侧线程）。
- **/plugins 来源信任分级**：ClawHub 与官方目录免 provenance 确认；任意 npm/git/archive/本地路径显示 provenance 警告并需 `--force`；需要能力同意时返回声明的能力与精确重试命令、`--accept-capabilities` 确认；第三方能力同意与来源确认是两回事。
- **提升层**：工具 / 工作流（命令面治理）。

### B3：Activepieces Agent 定义：brief 而非 configure + Flow vs Agent 判定表（来源：activepieces.com/docs/agents/overview，2026-09-25 实拉）
- **Agent = 你 brief 而不是 configure**：自然语言写下工作、给它需要的 app 访问权，活来了它自己干——每次运行读情况、决定用哪些工具、持续到完成；两个相似 case 可被不同处理（像同事）。
- **Flow vs Agent 判定表**：逻辑写一次 vs 每次现算；同输入同步骤 vs 可能不同处理；**知道流程用 Flow、工作多变用 Agent**。
- **760+ pieces 任意动作都可成为它可调的工具**；答案 grounded 在你的文档与表格；**可在一个 flow 内当一步跑并返回结构化数据**；一句话开始（agent 被自动写出来）。
- **提升层**：工作流（Agent 编排决策）。

### B4：n8n MCP 多客户端连接速查：配置文件位置矩阵 + OAuth 优先（来源：docs.n8n.io mcp-client-examples，2026-09-25 实拉）
- **9 个客户端连接配置**：Lovable（Settings>Integrations OAuth）/ Claude Desktop（claude_desktop_config.json）/ Claude Code（claude mcp add --transport http 或 claude.json）/ Codex（~/.codex/config.toml，`experimental_use_rmcp_client=true`）/ Gemini CLI（~/.gemini/settings.json）/ Cursor（~/.cursor/mcp.json 或项目）/ VS Code（.vscode/mcp.json）/ Windsurf（~/.codeium/windsurf/mcp_config.json）/ Google ADK（Python McpToolset+StreamableHTTPServerParams）。
- **OAuth 推荐 vs API key**（Bearer `<YOUR_N8N_MCP_TOKEN>` 头）；**Server URL 以 `/mcp-server/http` 结尾**（不是编辑器地址）；n8n 2.33.0 Connect a client 一键设置（Claude.ai/Cursor/VS Code）。
- **提升层**：工具（MCP 接入速查）。

## 判重说明
- B1 全新（p59 独有），落。
- B2 openclaw 增量（slash 命令技能面，r217-A 只到三类型/剥离语义），落。
- B3 activepieces 增量（agents 页新入口），落。
- B4 n8n 增量（MCP 客户端连接矩阵，r216 未覆盖），落。
- 未落：dify DeepSeek API 不稳三策略（与既有 dify 点重叠>60%）、trending arcbox/anything2explainer（描述有限）、deeplearning loop engineering（证据不足）、agentskills Qodo/OpenHands（产品名录为主）、skills.sh（已读尽）。
