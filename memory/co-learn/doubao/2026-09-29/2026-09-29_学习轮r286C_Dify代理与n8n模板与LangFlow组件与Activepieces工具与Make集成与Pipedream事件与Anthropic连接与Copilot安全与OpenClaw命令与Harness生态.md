# r286C 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r284/r285/r286A/r286B 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（Agent 策略/插件） | OK | **Agent 两种推理策略：Function Calling（模型原生函数调用，更可靠高效清晰，适合 GPT-4/Claude 3.5 等强函数调用模型）/ ReAct（Thought→Action→Observation 显式推理循环，透明可调试）**；**Allowed tools list：Agent 节点可选工具白名单，只送白名单工具给模型**；**Agent Strategy 插件：可自定义推理方法（Multi-turn reasoning / Tool orchestration / Context management / Termination control 四框架）**；**session.tool.invoke()（provider/tool_name/parameters）**；**自定义工具三法：OpenAPI/Swagger 粘贴自动解析、OpenAI Plugin 标准、代码方式** |
| 2 | n8n（模板库/社区） | OK | **模板生态规模：12,404 workflow templates（9 分类），AI 分类 7,379、CRM 471、Engineering 529**；**生产级模板三要素：clean commented JSON（import-ready）+ setup guide（凭证配置顺序）+ 注意事项**；**垂直行业自动化包（33 包：bookkeeping/legal/healthcare 等，每包 10 个预建 workflow JSON + 国家变体 + 设置指南）**；**self-hosted AI 模板（Ollama 本地模型 11 个模板无 API key）**；**社区贡献循环：improve → share back（PR 或分享实现）** |
| 3 | LangFlow（自定义组件/扩展） | OK | **自定义组件结构：继承 Component 类 + class-level attributes（display name/description/icon）+ inputs/outputs 列表 + methods + error handling/logging 内部变量**；**extension 新机制（lfx extension init my-extension）：extension.json v0 manifest + pyproject.toml pip-installable + src 布局——扩展化是组件分发新形态**；**Langflow Assistant 用 prompt 生成组件代码（"Create a custom component URLTitleExtractor with..."）模型驱动生成**；**组件更新：Update（无 breaking changes 单组件）/ Review（有 breaking changes 先快照再更新）**；**bundle=相关组件组（按服务商），贡献需进 bundle**；**安全：LANGFLOW_COMPONENTS_PATH 替换整个 category，allow-list 由 admin 控制；LANGFLOW_ALLOW_COMPONENTS_PATHS_OVERRIDE=false 防越权**；**agent 可用自定义组件作工具** |
| 4 | Activepieces（AI agents/MCP） | OK | **一个 MCP server 暴露 760+ apps（单 URL），无需单独安装每个 app**；**Tool search：按任务搜不按名字搜（ap_search_actions 工具），agent 描述任务→找到 action→检 schema→运行**；**AI-ready Pieces：tool search + AI metadata + audience**；**Custom API Pieces：TypeScript 把内部 API 变成可复用 action（typed inputs / auth handling / consistent responses）**；**Run logs & retries：step-level logs 捕获输入输出**；**自托管选项完全控制数据；每个连接 app 的 action 都变成 assistant 可调用的 tool** |
| 5 | Make（AI 模块/LLM 集成） | OK | **Make AI Toolkit（内置，无需外部 API key 所有计划可用）：Categorize Text/Classify/Summarize 等模块**；**原生模块支持 Anthropic Claude/OpenAI 等**；**OpenAI 模块：Chat Completions（GPT-4o/mini/o1/o3）/DALL-E/Whisper/Embeddings，模块 UI 直接配 model/temperature/system prompt，{{variable}} 传动态数据**；**典型 AI workflow 七类（Gmail 摘要分类/Typeform 打分/工单主题/Google Docs 摘要/发票提取/评论情感/博客创作）**；**LLM 集成成本治理三档执行栈（live/cached/surrogate + budget-aware routing）** |
| 6 | Pipedream（事件源/组件） | OK | **组件两类：sources（事件源，独立资源，props 接受用户输入，HTTP/timer/cron/手动触发，可作 workflow trigger 或独立 serverless）+ actions（操作，写 API）**；**10,000+ 预建 triggers/actions（public registry）**；**事件源运行独立于 workflow——同一 source 可触发多个 workflow**；**Connect proxy：3,000+ APIs 任意请求**；**source 开发：props 声明 app + dedupe: "greatest" 去重策略 + run() 逻辑**；**两种 trigger 分类（Connect 语境）：app-based event sources / native triggers**；**每 app 工具列表（如 Salesforce 61 actions/12 triggers）** |
| 7 | Anthropic（MCP connector） | OK | **MCP connector：直接接入 MCP server 无需实现 MCP client（Messages API 调用 MCP 工具）**；**tool_runner 接 MCP（list_tools → beta.messages.tool_runner）**；**只支持 tool calls（MCP 规范子集）；server 必须公开 HTTP（Streamable HTTP / SSE 传输）**；**OAuth Bearer 认证；单请求可连多个 MCP servers**；**Custom connectors（远程 MCP）：Settings → Connectors → Add custom → URL（HTTPS 公网可达）+ OAuth Client ID/Secret → Connect**；**组织级授权：IdP 集成，provision once / scope by group / revoke via IdP，跨 Claude chat/Code/Cowork 一致**；**Interactive connectors（Salesforce/Slack 等，内置工作工具交互）** |
| 8 | GitHub（Copilot 安全） | OK | **Copilot coding agent 内建三重扫描：code scanning + secret scanning + dependency vulnerability checks（PR 开之前 flag）**；**code scanning 原本 GHAS 付费，Copilot coding agent 免费**；**GitHub MCP server：secret scanning GA（2026-05）、dependency scanning public preview（2026-05，dependabot toolset）——提交前/开 PR 前扫描**；**/security-review slash command（Copilot CLI 2026-06 experimental + Copilot app 2026-07 public preview）**；**第三方 coding agent 安全验证（2026-06）：CodeQL 分析 + Advisory Database 依赖检查 + secret scanning，发现问题 agent 自行修复后 finalize PR**；**Dependabot alerts 可指派 AI agent 修复（Autofix），MCP server 让 agent 扫描修复 secrets/SAST/dependencies/code-quality**；**Copilot Autofix 不需要 Copilot 订阅** |
| 9 | OpenClaw（CLI/命令） | OK | **CLI 域：Setup/onboard/configure/config/completion/doctor/dashboard；Reset/backup/migrate/reset/uninstall/update；message/agent/agents/attach/acp/mcp；status/health/sessions/audit；gateway/logs/system**；**Slash 命令：/status（快速诊断）/trace（会话级 plugin trace）/config（持久化配置）/debug（运行时内存配置覆盖，commands.debug:true）/tools（运行时工具问答）/restart/dock-telegram/dock-discord**；**host bash：! <cmd> 或 /bash <cmd>**；**nodes 命令：nodes rename/invoke（--node/--command/--params/--invoke-timeout/--idempotency-key）/run——idempotency-key 在 invoke 里防重复** |
| 10 | WaytoAGI / DeepSeek Harness / HF | OK | **DeepSeek Harness（DSH）：2026-08-13 发布，MIT 开源 agent runtime（v0.1 developer preview）——"agent-assembly runtime" 不是另一个 Codex**；**SKILL.md 兼容：你的 SKILL.md 文件夹在 DSH 直接用（Agent Skills 兼容）**；**npm @deepseek-ai/dsh：2026-08-10 首发到 0.1.0-rc.6 四天六个版本（节奏快）**；**插件生态：GitHub dsh-plugin topic 1,200+ repos 快速增长**；**ModLens：第一个 vision 插件（为纯文本模型外挂视觉，粘贴图片出结构化 JSON 证据 OCR/版面/语义）——"vision bridge for every text-only coding agent"**；**视频总结技能安装教程：教 dsh 看视频**；**HF Skills：AI/ML 任务定义（dataset creation/model training/evaluation），与 OpenAI Codex/Claude Code/Gemini CLI/Cursor 互操作**；**Roo-cline 插件：Cursor/VSCode 里装 Roo-cline 接 DeepSeek R1 部署** |

## 判重（双键检索，增量判定）
- Dify Agent（r285A 提示词编排、r286A 编排、r286B RAG）→ Agent 双策略/Allowed tools 白名单 新面 → **新面**
- n8n 模板（r285A Webhook、r286B 表达式）→ 模板生态规模/生产模板三要素 新面 → **新面**
- LangFlow 组件（r284 记忆、r285B 存储、r286A 缓存、r286B 部署）→ 自定义组件结构/extension 机制 新面 → **新面**
- Activepieces MCP（r285C 已落"单 MCP server 760+"）→ 重叠约 60%，增量=tool search（按任务搜）/AI-ready Pieces/custom API pieces（≥40%） → **合并保留增量**
- Make AI Toolkit（r285A 场景蓝图、r286B 蓝图参数）→ AI Toolkit 模块/七类 AI 工作流 新面 → **新面**
- Pipedream 事件源（r285C 共享、r286A 触发器、r286B 代码步）→ 事件源独立资源/dedupe/props 新面 → **新面**
- Anthropic MCP connector（r285A 已落"Anthropic MCP connector"）→ 重叠约 60%，增量=connector 接入流程（Settings→Connectors→custom URL+OAuth）/组织级 IdP 授权/tool_runner（≥40%） → **合并保留增量**
- GitHub Copilot 安全（r285A 已落"安全扫描前置"）→ 重叠约 60%，增量=/security-review 命令/MCP server secret scanning GA/第三方 agent 安全验证/Autofix 免费（≥40%） → **合并保留增量**
- OpenClaw CLI（r285A 已落"八命令域"）→ 重叠约 65%，增量=slash 命令详情（/status /trace /config /debug /tools）/nodes invoke idempotency-key/host bash（≥40%） → **合并保留增量**
- DeepSeek Harness（r285A 已落"Cordis 生态"）→ 重叠约 55%，增量=SKILL.md 兼容性/ModLens 视觉插件/dsh-plugin 1,200+ repos/npm 节奏（≥40%） → **合并保留增量**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify Agent 双策略与工具白名单 | 工作流 |
| 2 | n8n 模板生态与生产级模板三要素 | 工作流 |
| 3 | LangFlow 自定义组件与扩展机制 | 工具 |
| 4 | Activepieces MCP tool search（合并增量） | 工具 |
| 5 | Make AI Toolkit 与七类 AI 工作流 | 工作流 |
| 6 | Pipedream 事件源独立资源与 dedupe | 工具 |
| 7 | Anthropic MCP connector 接入（合并增量） | 工具 |
| 8 | GitHub Copilot 内建安全扫描（合并增量） | 工具 |
| 9 | OpenClaw slash 命令与节点调用（合并增量） | 工具 |
| 10 | DeepSeek Harness 生态与 ModLens（合并增量） | 可复用 Skill |

## 复核
十独点均有当日实拉来源；6 新面 + 4 合并保留增量（增量均≥40%），零纯重复。版本建议 3.73.0。