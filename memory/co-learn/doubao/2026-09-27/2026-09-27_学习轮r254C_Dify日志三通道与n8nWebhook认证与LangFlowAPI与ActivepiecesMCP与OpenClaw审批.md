# r254-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（日志/监控面） | ✓ | 六类日志数据：Message Log（用户输入与模型输出原文）/Tool Usage Log（调用参数/函数/返回值/耗时）/Retrieval Trace（检索到的文档段落与向量信息）/Feedback（满意/不满意按钮）/Token 使用计数（token/花费/模型分布）/调试信息（中间提示词拼接）；三类通道协同：应用级（调试→日志页，时间倒序完整 trace ID 链路）+组件级（点节点查看输入输出元数据）+后端服务（dify-api worker.log/api.log/orchestrator.trace）；失败节点红色标识+错误堆栈；日志级别开发 DEBUG/生产 INFO/WARN；企业版：防篡改审计日志实时 SIEM+单次调用级别全追踪+Prompt 历史 PII 脱敏；集中化 Filebeat→ES→Kibana/SLS 插件 |
| 2 | n8n（webhook 认证面） | ✓ | 内置认证：Basic/Header/JWT/None；建议 Header Auth 几乎一切，JWT 当 caller 讲 JWT（密码学验证非手动轮换），Basic 最弱仅调用系统不支持别的才用；内置认证不原生验证 payload 完整性/防重放→HMAC-SHA256+raw body capture+timing-safe comparison+IP allowlisting 补层；HMAC 重放保护模板：认证+完整性（raw body byte-for-byte 签名）+重放保护（拒绝过期时间戳默认 5 分钟）+payload 白名单过滤；GET webhook：secret query 参数+IF node 校验（弱，仅 IoT 无更好方法）；OpenID Connect（Authorization Code+PKCE）；多租户：每租户唯一 secret key+时间戳防重放+rate limit+凭据加密+按租户隔离执行 |
| 3 | LangFlow（API/lfx 面） | ✓ | Workflow API v2：POST /api/v2/workflows，sync/stream/background 三模式，body flow_id 必须；v1：POST /v1/run/{flow_id_or_name}；advanced：/v1/run/advanced/{flow_id}（显式 inputs/outputs/tweaks）；/build/{flow_id}/flow 返回 job ID 流式事件；API access pane 自动生成 Python/JS/curl snippets；LFX：lfx run（fetch 远端 flow 运行，stdin；jq 改 model 再跑="modify flow before running"）；lfx serve（FastAPI 把 flows 暴露为 POST /flows/{flow_id}/run；需 LANGFLOW_API_KEY 因公开访问）；RAG 数据加载 /v2/files/ 上传→/v1/run/$FLOW_ID |
| 4 | Activepieces（MCP server 面） | ✓ | 内置 MCP server：AI 助手通过 MCP 用自然语言 build flows/manage tables/test automations；官方文档更正（verified 2026-09-24）：每 project 一个内置 MCP server（非每 piece）；Settings→MCP Server 开启；client 指向 https://<instance>/mcp；OAuth 认证（首次浏览器）；暴露 ap_* tools；280+（后 400+）open source pieces 作 MCP（自托管/cloud）；3 steps：Connect Tools in UI→Add Server URL to Claude/Cursor/Windsurf→Ask AI；AI agent 模式：看输入数据/推理条件/决定下一步工具，知道何时暂停（draft→check rules→wait for review before sending）；450+ connectors+内置 AI SDK |
| 5 | Make（AI agent 面） | ✓ | Make AI Agents 原生：sales outreach agent（watch gmail leads→分析内容判商机→web scraping 研究→qualify→查日历→起草个性化邮件→发草稿审批）；email sorting agent（watch inbox→classify→apply labels→draft replies routine→escalate priority to Slack）；实现模式：Revenue ops（parse 非结构化 lead data→extract→pre-populate CRM）/Customer success（分离 generic how-to vs churn risk）/Internal service desks（classify requests）；Router+Filter：AI 模块输出→分路由，条件用 Equal to case insensitive（AI 可能大小写不同）；Make MCP client：AI Agent 连 MCP servers+Make scenarios（Calendar MCP+Google Maps via scenario）；Maia：Scenario Builder 里自然语言描述→生成完整 scenario（"从 I build 到 I describe"） |
| 6 | Pipedream（schedule 面） | ✓ | Schedule trigger 两种：Every（每 N days/hours/minutes）/Cron Expression（cron 可绑任意时区）；组件 triggers cron object：intervalSeconds/cron+timezone；实用建议：简单 interval 无法指定星期几→用 Cron Expression（0 8 * * 1-5）；Pipedream 默认 UTC 运行 schedule，要调 UTC offset 匹配团队时区；触发源选核心 Schedule source（非 app-specific trigger）；Schedule app 从每 1 分钟到每年 |
| 7 | Anthropic（MCP 生产面） | ✓ | MCP 2026-07-28 规范：stateless core（双向有状态→请求/响应模型），servers 可部署 serverless+edge；Streamable HTTP canonical HTTP transport（spec 2025-11-25）；生产清单：工具数 20-30 上限（method/tag filters，LLM 选择过多工具掉精度）/显式 HTTP timeout（30s 默认）/结构化错误 isError:true+上游 status code/绝不无确认暴露 destructive tools（DELETE/DROP/rm）/环境变量管凭据不硬编码/transport 层 rate limiting（1 req/100ms 起步）/记录 tools/call（timestamp+tool name+input hash+execution time）/状态无状态化外部存储/内部 Streamable HTTP behind reverse proxy（nginx/Caddy）+OAuth 2.1+mTLS/公开服务器 rate limiting+audit+签名工具描述；Cloudflare Workers 托管；部署 AWS 模式 Lambda 快速原型/ECS 生产 |
| 8 | GitHub（当日榜面） | ✓ | 2026-09-27 热门：paperclipai/paperclip（open-source 管理 agents at work，TS ai）、vectorize-io/hindsight、dream-num/univer；当日 trending 另含：rohitg00/ai-engineering-from-scratch、openbao/openbao、microsoft/vscode、zhaoxuya520/reverse-skill、obra/super、anthropics/skills；生态参考：transitions.dev（12 CSS transitions+agent skill）、andrej-karpathy-skills（CLAUDE.md drop-in）、SkillKit（package manager 46 agents 31 sources）；weekly gain：colibri 7.8k/ECC 6.2k/ponytail |
| 9 | OpenClaw（permissions 面） | ✓ | Exec Approvals：沙箱 agent 在真实主机跑命令的防护；policy+allowlist+（可选）user approval 三同意才运行；三模式 deny（全锁）/allowlist（仅白名单）/full（全允许=提升模式）；sandbox vs tool policy vs elevated 三控制分离决策：sandbox 决定在哪运行/tool policy 决定哪些工具存在/deny always wins；无审批 UI 可达时 deny by default；strict 情况（inline eval/heredocs）任何 fallback 都不能软化；2026.5.20 更新：移除旧 cat SKILL.md 兼容 allowlist 绕过路径/trusted /approve 路由（手工审批走可信审批运行时）/doctor 诊断 sandbox tool policy 隐藏 MCP server tools；node pairing（2026.3.31 起 node commands 需 pairing 审批）；openclaw security audit+doctor --fix 脚手架 |
| 10 | Full Stack Skills（生态面） | ✓ | agenticskills.io：6 AI agent skills+4 MCP servers 集成单管线（前端代码到活部署）；40 skills-compatible products（OpenAI Codex/GitHub Copilot/Cursor/Gemini CLI/VS Code）；SkillsMP 约 1.9M skills；Skill=Expertise Injection（skill 专化通用 agent 领域专长）；生态五判断：registry 生态数万 public skills 跨数千 repos；Agent-Ready rubric 分级评估；React 技能包含非确定性响应设计；MCP 作为集成标准（产品以 MCP server 暴露能力） |

## 判重基准
双键检索：Dify（r254-A/B 多面——日志三通道/trace 链路面独有）；n8n（r254-A error/r254-B queue——webhook 认证分层+HMAC 补层面独有）；LangFlow（r254-A lfx 扩展/r254-B memory——Workflow API+lfx serve 面独有）；Activepieces（r254-A webhook/r254-B polling——内置 MCP server 面独有）；Make（r253 多面/r254-A data store——AI Agent 原生面增量≥40%，备选）；Pipedream（r254-A CLI/r254-B MCP——schedule 细节弱增量备选）；Anthropic（r254-A Agent SDK/r253 多面——MCP stateless 规范+生产清单增量强，备选）；GitHub（r253-A/r253-C 榜面——当日榜弱增量不落）；OpenClaw（r253-A skills/r254-B memory——Exec Approvals 权限审批面独有）；Full Stack Skills（生态规模弱增量不落）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 日志三通道与 trace 定位 | 六类日志+应用/组件/后端三通道+trace ID 链路 | 工作流 | wb-execute-discipline |
| ② n8n Webhook 认证分层与 HMAC 补层 | Basic/Header/JWT+payload 完整性/防重放补层 | 工作流 | wb-execute-discipline |
| ③ LangFlow Workflow API 与 LFX serve | v2 sync/stream/background+lfx run/serve | 工具 | wb-execute-discipline |
| ④ Activepieces MCP Server 与 AI Agent | 每 project 内置 MCP+OAuth+pieces 作 MCP+暂停审批 | 工作流 | wb-execute-discipline |
| ⑤ OpenClaw Exec Approvals 策略即代码 | policy+allowlist+approval 三同意+deny 默认 | 工作流 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 备选未落：MCP 2026-07-28 stateless+生产清单（增量强，下批判）/Make AI Agent 面/Pipedream Schedule 细节/GitHub 当日榜/Full Stack Skills 生态。
- 垃圾：本轮未产生临时文件。
