# r285A 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r284 全表及更早错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（提示词编排） | OK | **LLM 节点双模型界面：CHAT 模型=System/User/Assistant 三消息角色；COMPLETE 模型=Context/Conversation History/Query/Variables 块自由调整**；**提示词引用工作流变量用双花括号 {{variable_name}}，变量在到达模型前替换**；**系统变量 sys.app_id/sys.workflow_id/sys.timestamp、环境变量 env.*、Chatflow 从 Redis/PostgreSQL 加载会话变量**；**Variable Aggregator：合并分支输出到单一变量（聚合变量必须同数据类型，运行时仅实际执行的分支贡献值；v0.6.10+ 一个节点多聚合组）**；Agent 动态提示词（变量=用户填写输入框→运行时注入） |
| 2 | n8n（Webhook） | OK | **Webhook 响应三种模式：Immediately（状态码+Workflow got started）/ When Last Node Finishes（最后节点输出）/ Using Respond to Webhook Node（自定义：Response Code/Headers/body JSON/Text/Binary/Redirect/No Data）**；**Streaming response：实时流式返回，需触发节点+至少一个节点配置流式**；**测试 URL /webhook-test/ 与生产 URL /webhook/ 分离**；Response Data 选项：All Incoming Items/Binary File/First Incoming Item/JSON/JWT Token；常见坑：Response Data>First Entry JSON+Property Name（默认 data） |
| 3 | LangFlow（Agent/工具） | OK | **Tool Mode：在组件头菜单启用，把组件变成工具（修改组件 inputs），连接 Toolset 端口→Agent 的 Tools 端口**；**Agent=LLM 推理引擎选择工具；100+ 内置组件八大类：Agents（ReAct/Tool Calling/CrewAI）/LLMs/Vector Stores/Retrievers/Tools/Memory**；Sequential Tasks Agent 流（Chat Input+Prompt+Agent+YFinance/Tavily 工具+Chat Output）；MCP filesystem 服务器（npx @modelcontextprotocol/server-filesystem 路径限制）；Langflow 流可导出 JSON 作为 watsonx Orchestrate 工具 |
| 4 | Activepieces（连接/变量） | OK | **Secret Managers：集成外部密钥管理系统（HashiCorp Vault 等），连接对话框点钥匙图标🔑选 secret manager+secret path——集中凭证管理**；**Project Variables：命名值、作用域到单个项目、任何 flow 任何步骤可引用（API key/webhook URL/Slack channel ID/feature flag），不在 flow 步骤里、旋转 key 只改一处**；变量类型：Step Outputs（{{ trigger.body.name }}/{{ send_http.body.results }}）/ Connections（{{ connections.my_database.host }}）/ Router 分支数据；安全清单：HTTPS/firewall/rate limiting/secrets in secret manager/rotation/加密/SSO/MFA/RBAC |
| 5 | Make（场景模板/蓝图） | OK | **模板两级：Team templates（私有/可发布链接分享）/ Public templates（公开库 7500+，提交审核后入）**；**场景蓝图八块：Intake（webhook/poll/call）→ Normalize（canonical payload/field cleanup/defaults）→ Enrich（lookups/dedupe checks/context fetch）→ Route（分支）→ Write（CRM/DB updates）→ Notify（Slack/email）→ Audit（logging/metrics/run notes）**；**四段通用形态：Trigger→Modules（fetch+map）→Filter/router（branch）→Action（write）**；设计原则：围绕 canonical payload（路由映射在 app 变化后存活）、subscenarios 分离编排与可复用工具（清晰 I/O 契约）、router/iterator/aggregator 有意使用、生产可靠性第一天（retries/idempotency/logging/alerting）、发布纪律（blueprint exports/environment separation/ownership） |
| 6 | Pipedream（HTTP action） | OK | **HTTP Request Action=Postman 式界面（headers/body/连接 account），连接 app 自动配置 authorization headers（Slack Bearer token）**；集成数千个 app；**Component API：props 定义 http_request（type: http_request，default method/url），async run() 用 this.httpRequest**；Python 步骤 import requests（内置无需 pip install）；HTTP 触发事件字段：body/client_ip/headers/method |
| 7 | Anthropic（MCP） | OK | **MCP connector：直接从 Messages API 连接远程 MCP 服务器（无需单独 MCP client），旧版 mcp-client-2025-04-04 已弃用**；远程 MCP 服务器（互联网托管）让 Claude 访问工具与数据；**Claude SDK（Anthropic Python SDK）原生 MCP helpers：mcp_tool()/async_mcp_tool()/mcp_message() 一键转换 MCP 工具到 Anthropic API 格式**；tool_runner（model claude-opus-5-5）；Claude Code mcp add server-name；工具/CLAUDE.md/Hooks/MCP 四件套分工（MCP=外部工具/数据库/API 标准协议） |
| 8 | GitHub（Copilot coding agent） | OK | **内置安全扫描：code scanning/secret scanning/dependency vulnerability 在 PR 打开前标记（依赖已知问题/疑似 commit 的 API key）**；model picker+self-review+custom agents+CLI handoff；**cloud agent（原 coding agent）：不限于 PR 流程，可在 branch 工作不建 PR**；**automations：定时或仓库事件自动运行（triage issues 自动打 bug 标签）**；/security-review 与 /rubberduck 技能（多模型族批判找新问题）；Copilot code review 支持 agent skills+MCP GA；Copilot CLI GA（plan mode Shift+Tab）；agents 可访问终端/集成浏览器（分享 tab 上下文实时验证）；dev containers on ssh/tunnel/wsl |
| 9 | OpenClaw（CLI） | OK | **命令分区：Setup（openclaw/setup/onboard/configure/config/completion/doctor/dashboard）/ Reset-backup（backup/database/migrate/reset/uninstall/update）/ Messaging（message/agent/agents/claws/attach/acp/mcp）/ Health（status/health/triage/sessions/resume/audit）/ Gateway（fleet/gateway/logs/system）/ Network（connect/directory/nodes/node/worker）/ Runtime（approvals/exec-policy/sandbox/tui/browser）/ Models（models/infer/memory/commitments/wiki）**；**slash 命令：/diagnostics（owner-only 支持报告，每次要 exec 审批）/ /tasks（当前会话后台任务）/ /context list\|detail\|map\|json（解释上下文如何组装）/ /whoami / /usage off\|tokens\|full\|reset\|cost（per-response usage footer 控制）**；openclaw-cli watch -d（守护进程自动重启） |
| 10 | DeepSeek（插件生态） | OK | **DeepSeek Harness（Cordis）开源：每个组件都是插件——模型适配器/工具注册表/会话日志/沙箱/存储后端/agent 循环/任务调度器/UI**；**dshmarket 可视化插件市场（npm 1000+ 包，浏览/搜索/一键安装）**；**dsh.so DSH Plugin Trust & Discovery Registry（L5 运行测试通过列表；L4 sandbox-install 验证）**；**Mem0 deepseek-plugin：自动召回（搜索最新人类提示加入上下文）/自动捕获（存储每轮消息）/search_memory 工具**；**graph-memory 插件（知识图谱记忆：从会话提取结构化三元组、压缩上下文 75%、跨会话经验复用）**；插件安全审查信号：不必要依赖/原生二进制/安装时脚本/废弃包/异常位置依赖/未固定版本 |

## 判重（双键检索，增量判定）
- Dify 提示词编排（r284 版本控制/检索/节点）→ CHAT/COMPLETE 双界面+系统变量+Variable Aggregator 为新面 → **新面**
- n8n Webhook（r284 表达式/错误/智能体）→ 响应三模式+Streaming 为新面 → **新面**
- LangFlow Tool Mode（r284 记忆/多Agent/组件）→ Tool Mode 转工具+八大类 为新面 → **新面**
- Activepieces（r284 分支/触发器/测试）→ Secret Manager+Project Variables 为新面 → **新面**
- Make（r284 存储/路由/迭代聚合）→ 场景蓝图八块+模板两级 为新面 → **新面**
- Pipedream（r284 组件/重放/触发器）→ HTTP action 自动认证+Component API 为新面 → **新面**
- Anthropic MCP（r284 Claude MCP 配置）→ MCP connector+SDK helpers 为新面（增量>40%，合并保留） → **新面**
- GitHub Copilot（r284 GitHub 智能流程/生态）→ coding agent 安全扫描+automations 为新面 → **新面**
- OpenClaw CLI（r284 记忆/插件/自动化）→ CLI 命令分区+slash 命令 为新面 → **新面**
- DeepSeek（前轮未实拉主站）→ Cordis 全插件架构+Mem0 插件 为新面 → **新面**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 双模型提示界面与 Variable Aggregator | 工具 |
| 2 | n8n Webhook 响应三模式与 Streaming | 工具 |
| 3 | LangFlow Tool Mode 组件转工具 | 工具 |
| 4 | Activepieces Secret Manager 与 Project Variables | 工具 |
| 5 | Make 场景蓝图八块与模板治理 | 工作流 |
| 6 | Pipedream HTTP 自动认证与 Component API | 工具 |
| 7 | Anthropic MCP connector 与 SDK helpers | 工具 |
| 8 | GitHub Copilot coding agent 安全扫描与 automations | 工作流 |
| 9 | OpenClaw CLI 分区与 slash 命令 | 工具 |
| 10 | DeepSeek Harness Cordis 全插件架构 | 工作流 |

## 复核
十独点均有当日实拉来源；全部新面（零增量合并、零纯重复）。版本建议 3.70.0。