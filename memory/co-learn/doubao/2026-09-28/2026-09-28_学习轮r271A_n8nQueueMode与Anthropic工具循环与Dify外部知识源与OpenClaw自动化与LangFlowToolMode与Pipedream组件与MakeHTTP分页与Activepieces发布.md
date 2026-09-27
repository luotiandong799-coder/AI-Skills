# r271A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r266-r270 全表 150 词错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（外部知识源/API 面） | ✓ | **External Knowledge API**（自定义知识库——Endpoint URL+API Key；Dify 自动追加 /retrieval；response records[] metadata/score/title/content）；**InfraNodus GraphRAG 接入**（外部知识库 API 连接复用）；**LlamaCloud 插件**（Index 部署为端点）；**Knowledge Pipeline**（新起点——RAG 工作流编排，组件可插拔 upload/parse/chunk/embed）；**v1.6.0 双向 MCP**（workflow 内编排 MCP 工具；Agent 节点动态路径——Linear 案例三 agent 分流）；**API 扩展点**（app.external_data_tool.query 基于输入/变量取外部数据）；**Tavily 数据源插件**（实时 web knowledge pipeline）；**Unstructured 插件**（MCP 转换） |
| 2 | n8n（队列模式/扩展面） | ✓ | **Queue mode 架构**（主实例处理 timer/webhook 生成但不执行；execution ID 传 Redis 队列；worker 拉取执行）；**扩展**（加/减 worker；Redis 6+；BullMQ 队列；PostgreSQL 共享持久层）；**并发控制**（N8N_CONCURRENCY_PRODUCTION_LIMIT 默认 10 全局封顶；worker --concurrency 默认 10 推荐 ≥5；每并发执行 +256MB 内存）；**陷阱**（worker 数×并发——太多 worker+低并发耗尽 DB 连接池；Oracle 原生节点并发 DB session）；**autoscaling v2.0**（queue+webhooks 自动加 worker——数百并发） |
| 3 | LangFlow（agent 工具面） | ✓ | **Tool Mode**（组件头菜单开启——组件变工具，输入动态改变；Toolset port 连 Agent Tools port）；**工具注册**（Tool 对象通用接口；description 驱动 agent 选择）；**Simple Agent 模板**（Tool-calling agent+URL tool+Calculator+Chat）；**多工具**（一 agent 多工具，每工具多 action）；**Composio**（Gmail 单服务→Toolset 连 Agent；CUGA Agent 企业案例+MCP Tools）；**Code Agents**（max_iterations 默认 5 范围 1-50；code_execution_mode stepwise/full）；**LangChain bundle**（return_intermediate_steps/max_execution_time/early_stopping） |
| 4 | Activepieces（发布/市场面） | ✓ | **发布 CLI**（npm run publish-piece-to-api——打包上传 API endpoint；API Key Admin 生成；三问题）；**打包**（build-piece → .tgz）；**三种分享**（Contribute Back 主仓库/Community npm 直接分享/Private 私有）；**私有分发**（build --name；上传 tarball Platform Admin→Pieces）；**Piece 同步三类型**（Official cloud registry 自动同步/Custom npm 平台级/Private .tgz）；**两级管理**（Platform Admin 全平台/Project Admin 项目级 show/hide）；**生态**（pieces=npm 包 TypeScript typed framework；60% 社区贡献；280+ 全开源全部可作 MCP） |
| 5 | Make（HTTP/分页面） | ✓ | **HTTP v4**（简化设置+更安全 keychain+原生分页；legacy v3）；**分页模式**（Repeater 或递归场景 fetch 全页；cursor-based：响应 < page size 即末页；Stripe/Shopify/Slack next_cursor/has_more——提取传下请求直到 null）；**指数退避重试**（Tools>Sleep 动态公式 {{2^(bundle.attempt-1)}}——2s/4s/8s 后通知；重试 5xx backoff；4xx 通知）；**SDK pagination 指令**（mergeWithParent/repeat 条件重发带 delay+limit） |
| 6 | Pipedream（组件库面） | ✓ | **组件结构**（.app.mjs 逻辑——axios 封装 API URL+token；common.mjs 共享逻辑）；**Actions vs Sources**（actions 作 workflow step 不能独立运行——props 捕获输入返回 JSON（return/$.export 给后续）；sources 有 lifecycle hooks/dedupe/emit——actions 无）；**迁移**（legacy→component：params→props）；**Registry**（PipedreamHQ/pipedream components 目录——每集成一目录 actions+sources）；**Connect components**（triggers+actions=自包含可执行单元；backend SDK 自建前端 或 connect-react 预建）；**预建 actions**（最快集成——props 配置已连接账号） |
| 7 | Anthropic（工具循环面） | ✓ | **tool call loop**（tool runner 迭代器 yield Claude 消息；每迭代检查 tool use——调用发回结果自动继续；任意迭代 break）；**while 循环**（Ring 1 假设只调一次——真实多次调用；直到 stop_reason 不再 tool_use；历史累积 messages）；**硬迭代上限**（防 runaway 烧 token——交互 10 次/批 25 次；per-tool timeouts 防慢工具阻塞；监控平均迭代/session——creep upward 提示 schema regression/下游 API 变化）；**缓存工具定义**（tool definitions 每请求发送——缓存降成本）；**子代理策略**（subagent 全新对话无父历史但加载自己 system prompt+CLAUDE.md；仅最终响应回父作 tool result——父上下文只长 summary）；**loop 四型**（Turn-based 检查/Goal-based 停止/Time-based 触发/Proactive 提示） |
| 8 | deeplearning.ai（agentic 课程面） | ✓ | **Agentic AI 课程**（设计模式 reflection/tool use/planning/multi-agent workflows；集成外部工具 databases/API/web search/code execution；评估优化 metrics/error analysis/production；五节每节 <1h 免费）；**Building Coding Agents with Tool Execution**（写执行代码 agent——沙箱保护 untrusted code 1h21m）；**smolagents 课程**（research multi-agent；code agents 优势 over tool-calling；安全部署+结构化评估）；**memory 课程**（LangGraph 长期记忆模式——偏好/上下文/交互；respond/ignore/notify 决策）；**o1 课程**（复杂推理 1h44m）；**crewAI 课程**（2h49m 协作）；**agentic workflow**（分解为独立阶段——LLM 或外部工具；essay 例 outline→research→write→loop revise/check/redraft） |
| 9 | GitHub（编排框架面） | ✓ | **Omnigent（Databricks）**（Apache-2.0 meta-harness——组合/治理/沙箱/共享 Claude Code+Codex+Cursor+custom agents 会话）；**HydraFusion（GitHub Copilot）**（多模型编排——新模型评估并入池，优势给最合适任务）；**Vibe Kanban 22.4k**（看板编排 AI 编码 agent——issues 规划/spawn isolated workspaces/inline diff review 10+ agents）；**Superset 4.9k**（AI agents IDE——10+ 并行 git worktree 隔离+persistent daemon 跨崩溃保活）；**MetaGPT 68.8k**（multi-agent 编排）；**CrewAI v1.14.5**（A2A protocol 支持——Google 开放标准 agent-to-agent inter-crew；roles/goals/backstories）；**OpenAI 收购 Ona**（编排战略信号）；**langchain 146k/dify 143k** |
| 10 | OpenClaw（自动化面） | ✓ | **CLI cron**（openclaw cron add/create 别名——schedule 前 prompt 后；--name/--tz/--session/--system-event/--wake now）；**三调度类型**（at 一次性 ISO 8601；every 固定间隔 ms；cron 5 字段（或 6 带秒）+IANA 时区）；**触发器脚本**（--trigger-script ./watch-pr-ci.js——文件脚本创建 supervisor；--message；--session isolated）；**Gateway scheduler**（持久化任务，精确时刻唤醒，可选投递任意消息通道；无外部服务无 crontab）；**字段**（label/schedule/prompt/channel）；**报告自动化案例**（weekly-report：读 CSV→模板→周环比→flag 超 15% 指标→保存）；**变更操作**（add/edit/remove 注意生效时机） |

## 判重（双键检索结果）
- Dify 外部知识源：库内已落 §Dify RAG 检索/§混合检索——External Knowledge API 协议（/retrieval+records 格式）+Knowledge Pipeline+双向 MCP Agent 节点动态工具为独有增量 ≥40% → 落地
- n8n queue mode：库内已落 §错误工作流/§可观测性——Queue 架构（主不执行→Redis→worker）+并发控制（LIMIT/--concurrency/256MB slot）+DB 连接池陷阱为独有增量 ≥40% → 落地
- LangFlow agent 工具：库内已落 §组件构建/§多agent——Tool Mode 机制+工具注册 description 驱动+Composio/MCP+CUGA+Code Agents 参数为独有增量 ≥40% → 落地
- Activepieces 发布：库内已落 §生命周期/§认证——发布 CLI+三分享方式+两级管理+60% 社区+280+ 全 MCP 为独有增量 ≥40% → 落地
- Make HTTP：库内已落 §Webhook/§聚合——HTTP v4 原生分页+分页模式+指数退避公式为独有增量 ≥40% → 落地
- Pipedream 组件：库内已落 §components/§秘密——.app.mjs/common.mjs 结构+Actions vs Sources+Registry+Connect 两实现为独有增量 ≥40% → 落地
- Anthropic 工具循环：库内已落 §工具循环终止条件/§tool_choice——while 直到 stop_reason+硬迭代上限（10/25）+per-tool timeout+子代理 summary 回父+缓存工具定义为独有增量 ≥40% → 落地
- OpenClaw 自动化：库内已落 §定时任务记账判据——三调度类型+CLI 语法（trigger-script/system-event/wake）+Gateway scheduler+报告模板为独有增量 ≥40% → 落地
- deeplearning.ai agentic：并入记录（课程情报与方法论已在库内 agent 评估锚点）
- GitHub 编排：并入记录（Omnigent/HydraFusion/Vibe Kanban/Superset 生态情报）

## 独点落地（8 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r271A-1 | wb-execute-discipline | 3.29.0+ | n8n Queue Mode 与并发控制 | 工作流 |
| r271A-2 | wb-execute-discipline | 3.29.0+ | Anthropic 工具循环与迭代上限（增量合并 §工具循环终止条件） | 可复用 Skill |
| r271A-3 | wb-execute-discipline | 3.29.0+ | Dify 外部知识源与双向 MCP | 工作流 |
| r271A-4 | wb-execute-discipline | 3.29.0+ | OpenClaw 自动化三调度与 CLI（增量合并 §定时任务记账判据） | 工具 |
| r271A-5 | wb-execute-discipline | 3.29.0+ | LangFlow Tool Mode 工具化 | 可复用 Skill |
| r271A-6 | wb-execute-discipline | 3.29.0+ | Pipedream 组件结构 Actions/Sources | 工具 |
| r271A-7 | wb-execute-discipline | 3.29.0+ | Make HTTP 分页与退避重试 | 工作流 |
| r271A-8 | wb-execute-discipline | 3.29.0+ | Activepieces 发布与市场 | 可复用 Skill |

## 复核
八独点均有当日实拉来源；均为增量合并或新面落地；并入记录：deeplearning.ai agentic 课程、GitHub agent 编排生态。垃圾：本轮未产生临时文件。
