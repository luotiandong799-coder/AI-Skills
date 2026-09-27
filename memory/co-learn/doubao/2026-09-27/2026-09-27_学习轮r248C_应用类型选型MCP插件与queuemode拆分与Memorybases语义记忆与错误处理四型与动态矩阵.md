# r248-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（应用类型/API 编排面） | ✓ | 应用类型（Workflow/Chatflow 主要；Chatbot/Agent/Text Generator 基础型同引擎下层 legacy 界面）；选型判据（Agent=任务需 AI 推理选择下一步用工具；Text Generator=结构化内容输出 Cold Email Writer/Meeting Minutes）；Agent 节点（经典 Agent 给 LLM 工具自主控制迭代决定用哪个工具；Agent Strategies 定义思考行动方式 Function Calling 等）；Chatflow Invoker 插件（把 Chatflow 转成节点；universal streaming interface 调用工具——模型/Agent/Workflow/Chatflow 只要有流式输出接口都能集成保留流式能力）；MCP 集成（MCP SSE 插件 HTTP+SSE 与多 MCP server 通信动态发现调用外部工具；MCP Agent Strategy 插件把 MCP 直接嵌进 Workflow Agent 节点自主决定调用）；工具集成（Apify Run Actor wait for finish 选项；Brave Search LLM1 query refinement 链） |
| 2 | n8n（队列模式/生产面） | ✓ | Queue mode 拆分调度与执行（main 实例处理 timers/webhooks 生成不运行；execution ID 传 Redis 队列；worker 拉取执行）；水平扩展（加/减 workers 应对负载）；EXECUTIONS_MODE=queue；共享 Redis+Postgres+N8N_ENCRYPTION_KEY；好处（保护 main 实例；workers 并行处理提高性能可靠性；bounded pool 防 webhook 洪峰压垮 Postgres——解耦 Postgres 写入速度与实际工作耗时）；生产最佳实践 15 条（架构可扩展性 queue mode+workers；多 workflow 并行）；部署形态（Docker Compose PostgreSQL+Redis；Cloud Run enable_queue_mode；Render PostgreSQL+Redis 缓冲突发流量）；workers stateless 从队列拉任务并行执行长任务不影响 UI 响应 |
| 3 | LangFlow（记忆/存储面） | ✓ | Message History 组件（默认 Langflow storage；可附第三方 chat memory Mem0/Redis；可无 LM/agent 独立用——聊天外取记忆）；Agent 内置 chat memory 默认启用用 Langflow storage（大多数用例够）；Memory bases（1.10 新：per-flow 向量存储自动摄入对话消息；语义检索过去会话跨 session 持久——对比 Message History 时间顺序 vs memory base 语义相似度返回最相关上下文；对比知识库手动填充）；Vector store 配置（namespace/embedding/metric cosine/euclidean/dot_product/setup_mode Sync Async Off/pre_delete_collection；cache_vector_store 缓存向量存储加速读）；Memory 数据类型（Memory ports 接 Message History 与外部存储；Message 扩展 JSON 加文本字段）；存储后端（Zep/Cassandra/IBM Db2/DataStax Astra） |
| 4 | Activepieces（人工审批/协作面） | ✓ | Human-in-the-Loop Approvals（workflow 暂停发通知 email/Slack 请求审批→批准/拒绝后继续；高风险任务合同审批/内容审核/财务交易复核/退款确认；Zapier 无原生审批/Make 需外部服务）；Waitpoints 架构（paused step durable row；flow run row 只带状态 PAUSED/RUNNING；resume signal resume URL HTTP call 或 scheduled job 触发 都带 body/headers）；Flow Control（ctx.run 里 Stop Flow 提前停/send intermediate HTTP response/pause 等外部信号恢复）；Tables（内置轻量数据库：结构化记录 lookup/workflow state case status/owner/timestamps；避免重复处理；LLM workflows 复用 history 跨 runs）；审批后 resume 带决策/评论/编辑继续下游 CRM/helpdesk/notification 更新不丢上下文 |
| 5 | Make（错误处理/恢复面） | ✓ | Incomplete executions（保存失败 run 的 data+blueprint 可 rerun 防信息丢失；模块设置/输入/输出数据到失败模块；可调查）；Error handlers 四型（Break 只停出错 bundle 存 incomplete execution 其他 bundle 继续=生产最有用；Ignore 忽略错误移除 bundle 继续下一个；Resume 用替代输出替换模块输出 其余正常用替代输出；Rollback 撤销先前模块；Commit 保存部分进度）；Retry error handler（暂停失败 bundle 存错误消息/mappings/剩余 flow；自动或手动重试 incomplete）；场景设置 Process data in order（每条完成才下一条；incomplete executions 未解决不开始新 run）；Scenario recovery/version history（自动保存 blueprint 恢复未保存更改；版本历史 60 天恢复） |
| 6 | Pipedream（env vars/连接面） | ✓ | Env vars（分离 secrets 和静态配置；process.env.API_KEY 引用；不把 API key 写进代码）；Connect（managed auth 3,000+ APIs 处理授权或接受 API keys；Client SDK/Connect Link 几分钟接入；MCP server 给 agent 10,000+ tools）；环境变量集（PIPEDREAM_CLIENT_ID/SECRET/PROJECT_ID/PROJECT_ENVIRONMENT development|production）；.env 不提交版本控制；Accounts 通过 MCP 连接存储在 project；OAuth client |
| 7 | Anthropic（MCP connector 面） | ✓ | MCP connector allowlist（enabled: false 默认，显式启用特定工具；configs 工具级配置>default_config 集级>系统默认 优先级）；claude mcp add 作用域（--scope global/project；memory/filesystem/postgres）；配置位置（.mcp.json 项目级 repo 特定；~/.claude.json 用户级跨工具；Windows 反斜杠转义）；远程 server URL（sse URL+Authorization Bearer header）；managed-settings.json allowedMcpServers/deniedMcpServers（管理员控制用户可配置哪些） |
| 8 | OpenClaw（automations/cron 面） | ✓ | 三种调度类型（at 一次性 ISO8601；every 固定间隔 ms；cron 5 或 6 字段可选 IANA 时区）；时区（无时区时间戳=UTC；--tz America/New_York 本地时间）；--exact 禁用 staggering/--stagger 设置窗口；isolated sessions 默认（fresh context）或 main session；Heartbeats（cron expression+message+channel 三部分；assistant 收 heartbeat 消息执行指令送结果）；避免 task pileups/时区处理/重试 |
| 9 | GitHub Actions（expressions/matrix 面） | ✓ | Matrix strategy（单 job 定义多变量组合自动创建多 job run——多语言版本/多 OS 测试）；jobs.<id>.strategy.matrix；动态矩阵（fromJSON(needs.job1.outputs.matrix) 上游产出矩阵）；needs 上下文（依赖 job 的 outputs）；表达式数据类型（boolean/null/number/string）；contexts（secrets/strategy/matrix/needs/vars）；上下文矩阵（repository_dispatch 事件 payload 建矩阵） |
| 10 | Hugging Face（smolagents 面） | ✓ | CodeAgent 核心（Actions 是 Python 代码片段；工具调用以 Python 函数调用执行——一个 action 里多次搜索；生成 Python 代码块 parse_code_blobs 提取 LocalPythonExecutor 执行）；安全执行（默认受限安全函数集；禁止 imports 除非显式授权）；模型后端（HfApiModel/InferenceClientModel/TransformersModel 本地 Qwen2.5-Coder-32B/Ollama nemotron-3-nano）；工具（DuckDuckGoSearchTool/WebSearchTool；typed inputs dict 带描述生成 LLM schema；forward() 方法）；Hub agents 配置（model/endpointUrl/servers MCP stdio/可选 PROMPT.md）；stream_outputs=True 流式输出 |

## 判重基准
双键检索（相对 r244-r248B 已落章节）：Dify（r248-B 落执行引擎/r247-C 落异常——"应用类型选型+Agent Strategy+Chatflow Invoker 流式桥+MCP 插件"独有增量新面）；n8n（r248-B 落 Agents 复用——"queue mode main 生成 worker 执行+Redis 队列+encryption key 共享"独有增量深化）；LangFlow（r247-B 落 RAG 两段式记忆——"Memory bases per-flow 向量化语义检索跨会话 vs Message History 时间顺序"独有增量深化）；Make（r247-C 落 directives——"错误处理四型 Break/Ignore/Resume/Rollback+incomplete executions 保存 blueprint 重跑"独有增量深化）；GitHub（r248-A 落 Actions 安全——"matrix 动态 fromJSON+needs 上下文+表达式数据类型"独有增量新面）。未选素材：Activepieces 审批（r247-A 落 waitpoint——"human-in-loop 审批+决策评论 resume+Tables 状态"独有增量 未选）；Pipedream env vars/Connect（——"env 分离+Connect managed auth+10k tools"独有增量 未选）；Anthropic MCP connector（r247-B 落 MCP——"allowlist 默认禁用显式启用+优先级合并+作用域配置"独有增量 未选）；OpenClaw cron（r247 落 cron 判据——"at/every/cron 三型+isolated session 默认+heartbeat 三部分"独有增量 未选）；HF smolagents（r247-B 落 HF guardrails——"CodeAgent Python 代码动作+安全执行器+TransformersModel 本地"独有增量 未选）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① 应用类型选型+MCP 插件 | Agent 选型判据；流式桥；MCP 嵌入 Agent | 工具/工作流 | wb-execute-discipline |
| ② queue mode 拆分 | main 生成 worker 执行；Redis 队列 | 工作流/工具 | wb-execute-discipline |
| ③ Memory bases 语义记忆 | 向量化跨会话 vs 时间顺序 | 工作流/工具 | wb-execute-discipline |
| ④ 错误处理四型 | Break/Ignore/Resume/Rollback | 工作流/工具 | wb-execute-discipline |
| ⑤ 动态矩阵 | fromJSON+needs 上下文 | 工作流/工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
