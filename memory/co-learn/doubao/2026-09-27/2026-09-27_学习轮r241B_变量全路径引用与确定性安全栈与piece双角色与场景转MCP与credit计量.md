# r241-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（变量/编排面） | ✓ | 变量替换（{{variable_name}} 双花括号 prompt 中引用模型前替换）；特殊变量（#context# 知识检索输出/#histories# 对话记忆 TokenBufferMemory/#files# 视觉文件）；变量不保存修复（短引用 {{user_name}} 换全路径 {{node_2.user_name}}）；Variable Aggregator（汇聚互斥分支输出到一致类型；array 模式收集所有分支输出成 list 再 Code 处理）；Output 节点（无 Output 分支不返回值；多 Output 支持）；Human Input 节点（表单内联/邮件发给决策人审批敏感数据）；LLM 节点（chat 模型 roles System/User/Assistant vs completion 模型纯文本延续；temperature 0-1） |
| 2 | n8n（AI agent/模板面） | ✓ | 生产 AI agent 栈 Lite（确定性 Code nodes only 无 LLM 无凭据：PII 脱敏→fresh lead→HANDOFF APPROVED；重复→HELD AT RELIABILITY；prompt injection/信用卡号→STOPPED AT SECURITY 在 AI 前）；并发防重（FOR UPDATE SKIP LOCKED 防止并发 webhook 重复 AI 响应；错误监控 workflow 抓 DNS/连接失败 WhatsApp 告警；凭据 credential manager 不硬编码）；模板化（clean+genericize 移除业务数据保留逻辑+配置指南）；JSON 强制输出（显式 System Message Extract fields return valid JSON only null for missing+Response Format JSON Object）；RAG 入门（Simple Vector Stores+Form trigger） |
| 3 | LangFlow（prompt/agent/模型面） | ✓ | Agent Instructions（system_prompt 每对话应用；工具 Tools port 任何组件可当工具含 Agent/MCP server）；CodeAct Agent Smolagents（代码写作 agent 迭代生成+执行 Python 沙箱解释器，输出决定下一步直到最终答案）；Prompt Template（自然语言+固定值+动态变量基线上下文；定义用户查询一致结构/输出格式 JSON）；Chat Input/Output（Message 数据含 sender/session ID/timestamp/file attachments；初始输入不应是完整对话历史）；Marketing 模板（先请求用户详细 briefing：内容类型/目标平台/受众/语气/长度/主题再创作） |
| 4 | Activepieces（pieces/模板面） | ✓ | type-safe pieces 框架 TypeScript（每 piece 是集成且同时是 workflow 构件和 MCP server，400+ MCP servers AI agent 可发现调用）；createAction（name/displayName/run(context)）；Approval 门控（触碰 money/customers/production 的步骤门控，其余自动）；Chat to Automation（自然语言描述生成起始 flow 供精修）；AI Agent Builder（tools+memory+human-approval checkpoints 不只是 prompt wrapper） |
| 5 | Make（场景/模板面） | ✓ | MCP server 暴露（创建 3 场景暴露为 MCP tools：create Jira ticket+Slack 通知/搜索 tickets/详情；voice AI 平台 VoiceFlow/VAPI 连 Make MCP server 对话中调用）；MCP client（Calendar 检测会议+AI 模块连 CRM MCP server get_account/get_deals/get_contacts/get_activities/update_account 自动决定调用）；AI automation 例（WordPress 新文章→Claude 生成 LinkedIn/X/newsletter→Buffer 各渠道；Calendly 访谈→OpenAI 转写→Notion 结构化）；Meeting Intelligence Pipeline（Zoom/Meet webhook→Whisper 转写→Chat 总结 JSON title/attendees/decisions/action_items owner due_date→Notion+Calendar）；AI Playbook（70+ use case 四阶段 Build/Accelerate/Scale/Lead） |
| 6 | Pipedream（定价/限制面） | ✓ | credit 计量（1 credit=30 秒 compute@256MB；512MB 双倍 1GB 四倍——credit 成本随内存缩放）；free（100 credits/mo+3 active workflows+3 连接 apps；开发/builder 测试不耗 credits；hosted MCP servers 个人使用）；硬上限（credits 超限 workflow 中途停止 hard caps）；Basic（$29/mo 2,000 credits 10 workflows） |
| 7 | Anthropic（MCP/Claude Code 面） | ✓ | MCP v1/v2 runtime（v1 SDK 1.x + v2 SDK 2.0 MCP protocol revision 2026-07-28）；claude mcp add（本地 stdio 服务器 npx -y @package/server/远程 HTTP 服务器 --transport http）；插件形态（single mcp connector 指向远程 MCP server/plugin bundle 组合 MCP servers+skills host GitHub submit repo；插件可含 LSPs）；作用域（project MCPs .mcp.json/local MCPs ~/.claude.json） |
| 8 | skills.sh（安装流程面） | ✓ | npx skills 免安装（npx skills add owner/repo 跨 Claude Code/Cursor/Cline 等；-g 全局装到 ~/<agent>/skills/）；命令集（npx skills find [query] 交互搜索/ npx skills add <package>/ npx skills check 检查更新/ npx skills update）；find-skills 榜首 94.1K 装机量；安装粒度（整包 npx skills add vercel-labs/agent-skills vs 单技能安装命令） |
| 9 | docs.openclaw.ai（agent/session 面） | ✓ | Session keys & routing（direct messages: agent:<agentId>:<mainKey> dmScope main/dm:<peerId> per-peer/<channel>:dm:<peerId> per-channel-peer；group chats 另有形态）；Serialization（同 session 消息一次处理一个 Command Queue——两个同时消息破坏状态或冲突工具输出）；Session 存储（per-agent SQLite ~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite+Transcript JSONL）；Bindings 确定性路由（按 channel/account/peer 匹配 most-specific wins：exact peer match > parent peer match > guild+roles > guild-level）；Memory（MEMORY.md 策展洞察 agent 复习每日日志提炼更新；memory/ 目录 YYYY-MM-DD.md 每日日志；Honcho memory 跨会话持久+用户建模） |
| 10 | GitHub（生态面） | ✓ | superpowers 291.8k★ #1（agentic skills framework & software development methodology）；hermes-agent 249k★；mcp-for-beginners（microsoft：MCP 基础课程跨语言 .NET/Java/TS/JS/Rust/Python 模块化可扩展安全工作流）；llm-provider-mcp（本地 MCP server 在 Claude Code/Codex/Cursor Agent/Pi 间委派异步编码作业）；Atomic Agent 2.5k★（本地优先 CLI/TUI 编码助手 open-weight llama.cpp fork 无需账号 56 内置工具）；awesome-harness-engineering（harness engineering 纪律：memory/evals/verification/orchestration 模型外围模式）；DarkMoon 913★（自托管 pentest MCP host 80+ 攻防工具） |

## 判重基准
双键检索：Dify（r241-A 落过部署秘密键，"变量全路径引用+聚合器+HITL"独有增量）；n8n（r241-A 落过 Code node 结构，"确定性安全栈+并发锁+JSON 强制"独有增量）；LangFlow（r241-A 落过组件规范，"CodeAct+结构化工单"独有增量）；Activepieces（r241-A 落过队列分级，"piece 双角色+审批门控"独有增量）；Make（r241-A 落过错误五型，"场景转 MCP+结构化 JSON"独有增量）；Pipedream（r241-A 落过触发器选型，"credit 计量纪律"独有增量）；Anthropic（r241-A 落过流式 backpressure，"插件 bundle+双 runtime"独有增量）；skills.sh（r241-A 落过评估驱动，"命令全景+全局安装粒度"独有增量）；docs.openclaw.ai（r241-A 落过插件边界，"session 路由+序列化"独有增量）；GitHub（r241-A 落过 claude-mem，"superpowers 技能框架+跨 agent 委派"独有增量）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 变量引用纪律 | 短引用换全路径 {{node_2.user_name}}；#context#/#histories#/#files# 特殊变量；Variable Aggregator array 模式收集分支；Human Input 审批 | 工作流 | wb-execute-discipline |
| ② n8n 确定性 AI 安全栈 | Code nodes only 前置 PII 脱敏/重复检测/注入拦截；FOR UPDATE SKIP LOCKED 并发防重；JSON 强制输出 | 工作流 | wb-execute-discipline |
| ③ Activepieces piece 双角色 | piece=workflow 构件+MCP server 双角色；Approval 门控 money/customer/production | 工具/工作流 | wb-execute-discipline |
| ④ Make 场景转 MCP | 场景暴露为 MCP tools 供 AI 对话调用；结构化 JSON 输出字段化写库 | 工作流 | wb-execute-discipline |
| ⑤ Pipedream credit 计量 | 1 credit=30s@256MB 内存翻倍成本翻倍；超限中途停止；开发测试不耗 credits | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
