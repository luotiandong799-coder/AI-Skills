# r264C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站，查询词与 r263 三轮+r264A+r264B 全错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（插件生态面） | ✓ | **Marketplace 治理度量**（928 列插件/263 Official 标签/99 活跃维护基线）；插件页**安全评级 S+Last checked 时间戳**；**资源上限声明**（Maximum memory 256MB/Maximum storage 1MB/Access domain 白名单）；**安装三式**（Marketplace 一键/GitHub repo/Release 本地文件）；**Creator Center+Template Marketplace**（发布 workflow 模板+PartnerStack 联属佣金）；提交审核=官方签名/certified 徽章/自动更新；OpenAI-API-compatible 插件（LLM/reranking/embedding/STT/TTS 统一配置） |
| 2 | n8n（agent 记忆面） | ✓ | **内存即画布节点**（AI Agent 节点连 memory sub-node，全可视可改）；**Window Buffer Memory=滑动窗口最后 N 条**（K 可配；窗口外完全遗忘，适合 5-10 轮会话）；**截断陷阱**（窗口切掉 assistant tool_calls 但留 tool response→OpenAI payload 非法——K 要够大/偶数）；**session key 纪律**（key=Teams conversation ID 非静态值，否则用户互看上下文）；**长期记忆管线**（定期 flow：Pull→aggregate/summarize→embed→pgvector→RAG）；dual-layer（Postgres 15 条+pgvector 长期） |
| 3 | LangFlow（记忆分层面） | ✓ | **Agent 组件内建 chat memory 默认开启**（Langflow storage，Number of Chat History Messages 可配）；**Message History 组件**（存储/检索/排序/过滤；可挂第三方 Mem0/Redis；无需 LLM/agent 单独用）；**memory base=向量化长期记忆**（semantic retrieval 跨会话，按相似度非时间——区别于时序检索）；**session_id 分组**（custom ID 隔离用户；flow 多 session；不同 flow 可共享 session）；默认 100 条；monitor/messages 端点 |
| 4 | Activepieces（webhook 安全面） | ✓ | **handshake 策略**（handshakeConfiguration+onHandshake 返回 status/body/headers）；**HMAC 验签流程**（code step 计算比较共享密钥，不匹配早拒；log 签名+时间戳；nonce 防重放）；**schema version 字段路由**（payload 版本字段→按版本转换→旧 route 保留到迁移完）；**webhook 安全清单**（secret tokens/TLS/验签/结构校验/限速/日志/端点不公开/轮换）；**waitpoints**（flow 暂停到 callback URL 恢复，URL 每 run 唯一，async/sync 两模式）；AP_APP_WEBHOOK_SECRETS（Slack/Square 单 webhook/应用） |
| 5 | Make（调度队列面） | ✓ | **调度四类型**（indefinitely 每 N 秒/on-demand 仅 API 触发/once 指定时间/immediately 尽快）；**on-demand+webhook 队列**（事件确认+存队列→Run Once 拉取）；**限速队列**（最大 30 runs/min 超额排队；webhook 超限→调用方 429）；**轮询成本**（每分钟≈43,200 credits/月 vs 15 分钟=2,880——间隔即成本平衡点）；**延迟去重模式**（长 delay 前写 Data Store pending→delay 后读状态，已被改→跳过）；Cron 表记（0 9 * * MON-FRI） |
| 6 | Pipedream（版本部署面） | ✓ | **deploy/draft 模型**（每 workflow 一个 live deployed 版本+一个 editable draft；discard draft 回滚到上次 deployed；**deploy 后无法自动回滚**——完整历史只在 GitHub Sync）；**Connect 两环境**（development/production，credentials 分离，dev 全功能免费）；**pd publish --connect-environment**；**GitHub Sync changelog**（merge→production→deploy）；**Edit with AI**（workflow/code step 级自然语言编辑+Debug with AI）；数据驻留（AWS us-east-1/VPC 专属网络+静态出口 IP） |
| 7 | Claude Code（任务管理面） | ✓ | **todo 生命周期四态**（Created pending→Activated in_progress→Completed→Removed；2026-01 从 Todos 升级到 Tasks）；**TodoWrite/TodoRead 系统提示硬要求**（非常频繁使用：tracking+visibility+拆解大任务）；**CLAUDE_CODE_TASK_LIST_ID 环境变量**（任务列表分组，子任务依赖声明）；SDK 结构化 todo 渲染进度；Todoist MCP 集成（写操作需人审） |
| 8 | GitHub Actions（复用面） | ✓ | **reusable workflow vs composite action 选型**（可复用=整 workflow 多 job；composite=多 step 合成单 action 单 job step）；**on.workflow_call** 定义 inputs/outputs/secrets 映射；**$/ 自仓库语法**（2026-07-30 新：uses: $/... 指向运行中精确 commit，无需 checkout）；**YAML anchors 复用 job 配置**；composite runs.using: 'composite'；安全 roadmap（scoped secrets & reusable workflow inheritance） |
| 9 | OpenClaw（gateway/webhook 面） | ✓ | **gateway=单进程多渠道**（Discord/Google Chat/iMessage/Matrix/Teams/Signal/Slack/Telegram/WhatsApp/Zalo）；**hooks 配置**（POST /webhook/{path}，hooks.enabled/endpoint/token）；**wake hook**（POST /hooks/wake {text, mode: now\|next-heartbeat}）；**channel=gateway 级适配器**（翻译外部平台↔内部消息格式，进程内 18789）；**webhooks 默认关闭**；ingress 安全（untrusted wake-hook owner downgrade/CLI authority/parsing 加固/webhook-auth throttling/限速）；**cron vs heartbeat vs webhook 分工**（webhook=外部系统安全交活） |
| 10 | Hugging Face（smolagents 面） | ✓ | **CodeAgent=写 Python 代码执行动作**（parse_code_blobs→LocalPythonExecutor 执行→结果存 memory steps→ReAct 循环）；**ToolCallingAgent=JSON tool calls**；max_steps 上限；任意 LLM（Hub/transformers/推理 API/OpenAI/Anthropic）；@tool 装饰器；verbosity_level；smolagents-colony（output_type object 免 JSON 序列化/typed inputs dict 供 LLM schema 生成） |

## 判重基准
双键检索：n8n 记忆（§6183 向量记忆管"检索管线质量"——窗口截断陷阱+session key 纪律为增量合并）；LangFlow 记忆（§6153 memory bases+§6354 会话分隔已覆盖大部分——Message History 组件/第三方 Mem0 为弱增量并入记录）；Activepieces webhook（§6302 签名验证同源全覆盖——纯重复不落）；Make 调度（§6093 并发治理引过 schedule-a-scenario——调度四类型+轮询成本量化+延迟去重为增量合并）；Pipedream draft（无 deploy/draft 章节——新面）；Claude Tasks（§6405 memory/§6462 Plan mode 不同面——任务生命周期新面）；GitHub Actions 复用（§6309 Agentic/r264B 缓存不同面——选型新面）；OpenClaw gateway（§6282 权限模式提过 gateway 信任边界——gateway 架构分层+webhook 分工增量并入记录）；Dify 市场治理（§3596 插件安全评级卡已落——治理度量+Creator Center 增量并入记录）；smolagents（无章节——新面，价值低于前五并入记录）。

## 独点落地（5 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r264C-1 | wb-execute-discipline | 3.20.0+ | n8n agent 窗口记忆截断陷阱与 session key 纪律 | 工作流 |
| r264C-2 | wb-execute-discipline | 3.20.0+ | Make 调度四类型与轮询成本量化+延迟去重 | 工作流 |
| r264C-3 | wb-execute-discipline | 3.20.0+ | Pipedream deploy/draft 模型与环境分离 | 工具 |
| r264C-4 | wb-execute-discipline | 3.20.0+ | Claude Code Tasks 生命周期与任务分组 | 工作流 |
| r264C-5 | wb-execute-discipline | 3.20.0+ | GitHub Actions 复用选型：reusable vs composite + $/ 语法 | 工作流 |

## 复核
五独点均有当日实拉来源（逐站 URL 见各站摘要）；r264C-1/2 按增量判定合并保留增量；r264C-3/4/5 新面；备选并入记录不单独落地（LangFlow 记忆/Activepieces webhook 纯重复不落）。垃圾：本轮未产生临时文件。
