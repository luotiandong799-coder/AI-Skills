# r283C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站；查询词与 r283A/B 十词 + r282 三十词 + r281 三十词 + 更早全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（实时调试） | OK | **Variable Inspect Panel（1.5.0）：画布底部全局控制中心实时显示全工作流所有变量；可直接编辑变量值测试下游节点效果，不必重跑昂贵上游操作（LLM 调用/API 请求/数据库查询）**；调试流程=执行到目标节点→打开面板→编辑缓存变量→run step 下游节点用修改值；类型不兼容（string 传错）常见；Last Run 日志定位精确原因；DEBUG=true LOG_LEVEL=DEBUG（不用于生产）；**Response Validation 模式：AI 节点后跟 Condition 节点校验输出（要 JSON 就加第二个节点验证合法性）** |
| 2 | n8n（Wait 节点/恢复） | OK | **Wait 暂停语义分界：<65 秒不落库（进程继续跑）；>=65 秒 offload 执行数据到数据库、worker 完全释放（无悬挂进程）；execution 表 status=waiting，metadata=恢复时间戳或 webhook URL**；execution.resumeUrl=调用恢复等待工作流的 webhook URL；execution.customData 自定义数据；**恢复与幂等：无状态工作流失败重启会盲目重跑/跳过——checkpointing（DB 存 last processed page/cursor，重启从该页开始）+ 写幂等（upsert/unique keys）**；HTTP 分页超时：内建分页失败重跑整节点 page 1→关内建分页手动分页（每页独立请求+Retry on Fail 每页生效）；长任务：job_id 键存阶段状态，子工作流入口查状态跳过已完成阶段 |
| 3 | LangFlow（组件输入类型） | OK | **组件输入类型体系：TextInput/IntInput/BoolInput/DropdownInput/DataInput/MessageTextInput/DataFrameInput**；JSON 端口（结构化数据对象，含 text_key 主文本字段）；Input/Output 组件参数（input_value/sender/sender_name/session_id）；Data 组件（curl/method/query_params/body/headers）；Processing（data/llm/filter_instruction/sample_size）；LangChain bundle（tools/system_prompt/memory/max_iterations）；Table 类型只连 DataFrameInput |
| 4 | Activepieces（定时触发器） | OK | **Schedule pieces：Every X Minutes/Hour/Day/Week/Month + Cron Expression 两类触发器**；cron 触发器配置（pieceName @activepieces/piece-schedule、triggerName cron_trigger、input cronExpression "0 9 * * 1-5"）；时区感知；自定义 cron（"0 12 * * SUN#2"=每第二个周日）；**后台作业最佳实践：定时触发器+条件逻辑限制只处理新/变更记录，Tables 持久化 last cursor/timestamp 只处理增量（delta）** |
| 5 | Make（webhook/认证） | OK | **webhook URL 应保密：泄露可被触发消耗 operations（嵌入网页=危险）**；测试 HTTP 调用用 Postman（最佳实践）；custom webhook 每场景独立 URL 不能复用；**Get request headers 选项访问请求头，map()+get() 提取 authorization 头做过滤（Basic Auth 验证公式）**；Make API 认证=Authorization: Token 头；OAuth 2.0 authorization code flow with refresh token（confidential clients 可安全存 Client Secret）；webhook verification directive（condition IML string 处理验证请求） |
| 6 | Pipedream（并发/节流） | OK | **concurrency=并发 workers 数；throttling=execution rate（0-10000 events/interval 秒分时）**；workers=1 串行化（一次一个事件，前一个完成才处理下一个）；超限事件进队列（queue size 可设）或丢弃；**执行时限：HTTP/Email 触发默认 30s、Cron 触发默认 60s，超时抛 Timeout error 停止（已跑成功的 cell 日志保留）**；cold start：约 5 分钟不活动后首次请求需 spin up 新执行环境（延迟） |
| 7 | Claude Code（settings/权限） | OK | **权限三态：allow（自动许可）/ask（确认）/deny（禁止）；语法 Tool(filter)：Bash(npm run lint)、Read(./.env)**；deny 排除敏感文件（WebFetch/Bash(curl:*)/Read(./.env)/Read(./secrets/**)）；**Bash patterns 是前缀匹配、可被绕过（安全边界要额外注意）**；additionalDirectories 扩展工作目录；defaultMode（acceptEdits 等）；**disableBypassPermissionsMode/disableAutoMode=disable 强制禁止绕过**；$schema 指向发布 JSON schema（IDE 自动补全+内联校验）；企业/项目/用户三层 settings |
| 8 | GitHub（Copilot 自定义指令） | OK | **两层自定义指令：仓库级 .github/copilot-instructions.md（应用于仓库内所有请求）/ 路径级 .github/instructions/NAME.instructions.md（匹配指定路径文件的请求）**；内容建议=项目概览（目的/背景）+编码标准约定（命名/格式/最佳实践）+工具/库/框架及版本号；**cloud agent 自定义 agents：description（必填）+tools 列表（含仓库设置或 agent profile 里配置的 MCP tools）**；Coding agent best practices 同样强调 build/test 信息进指令文件 |
| 9 | OpenClaw（多渠道 Gateway） | OK | **Gateway 网关=连接聊天应用与 AI agent 的桥：Discord/Google Chat/iMessage/Matrix/Teams/Signal/Slack/Telegram/WhatsApp/Zalo/WebChat 等 50+ 渠道**；**多渠道可同时跑：config.yaml 配多个 gateway，同一 agent 从所有渠道接任务、共享同一 memory/context（WhatsApp 发任务 Telegram 查进度=同一个 agent）**；媒体/表情支持因渠道而异（文本全支持）；WhatsApp 用 Baileys 需二维码配对；WebChat 基于 WebSocket；NVIDIA NemoClaw 支持 Telegram/Discord/Slack/WeChat/WhatsApp/Teams，WeChat 用 host 侧 QR 扫码采集 token |
| 10 | deeplearning.ai（2026 新课程信号） | OK | **2026 课程方向：Building Adaptive AI Agents（08-26）/ AI Coding Workflows: From Cloud to Local（09-06）/ AI Code Review（09-23）/ Fast LLM Inference with Cerebras（WSE-3 实时推理）/ Agent Memory: Building Memory-Aware Agents（Oracle AI Database+LangChain：长期记忆=外部、持久、结构化的一等基础设施）/ Document AI: From OCR to Agentic Doc Extraction（LandingAI：OCR 丢版式信息→agentic 抽取解决合并单元格表格/图表-说明关系/多栏阅读顺序）/ Agent Skills with Anthropic / Prompt Compression and Query Optimization / Semantic Caching for AI Agents / Knowledge Graphs for AI Agent API Discovery / AI Prompting for Everyone（7h4m Beginner）** |

## 判重（双键检索，增量判定）
- Dify 调试面板（r283A 错误处理/r267C 工具循环）→ 变量检查面板+响应验证为新面 → **新面**
- n8n Wait 恢复（r283B Activepieces waitpoint/r282C 响应模式）→ <65s 落库边界+checkpointing+手动分页幂等为独有增量 → **增量合并**
- LangFlow 输入类型（r281C 组件目录/r272C 模板）→ 类型体系+JSON 端口为新面 → **新面**
- Activepieces 定时触发（r270B 生命周期/r273B Webhook）→ cron+时区+增量模式为新面 → **新面**
- Make webhook 安全（r276B webhook 场景/r281A 连接）→ URL 保密+认证过滤+Postman 测试为新面 → **新面**
- Pipedream 并发节流（r278B concurrency）→ 执行时限 30s/60s+cold start 为独有增量 → **增量合并**
- Claude Code 权限（r282B hooks 权限）→ settings.json 三态权限+Tool(filter) 语法+可绕过警告为新面 → **新面**
- Copilot 指令分层（r283A AGENTS.md/r281A CLAUDE.md）→ 仓库级/路径级两层指令为新面 → **新面**
- OpenClaw 渠道网关（r270A 供应商/r283A 团队）→ 50+ 渠道+同 agent 跨渠道共享记忆为新面 → **新面**
- deeplearning 课程信号（r283B diffusion/r275A red team）→ Agent Memory/Document AI 方向为新面 → **新面**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 实时调试与变量检查面板 | 工具 |
| 2 | n8n 等待恢复与检查点幂等 | 工作流 |
| 3 | LangFlow 组件输入类型体系 | 工具 |
| 4 | Activepieces 定时触发与增量模式 | 工作流 |
| 5 | Make Webhook 认证与安全 | 工具 |
| 6 | Pipedream 并发节流与执行时限 | 工具 |
| 7 | Claude Code 权限配置语法 | 工具 |
| 8 | Copilot 指令分层体系 | 工作流 |
| 9 | OpenClaw 多渠道网关架构 | 工具 |
| 10 | 2026 课程方向信号 | 工作流 |

## 复核
十独点均有当日实拉来源；三点增量合并（均含≥40% 独有增量）、七点新面；无纯重复。版本建议 3.67.0。