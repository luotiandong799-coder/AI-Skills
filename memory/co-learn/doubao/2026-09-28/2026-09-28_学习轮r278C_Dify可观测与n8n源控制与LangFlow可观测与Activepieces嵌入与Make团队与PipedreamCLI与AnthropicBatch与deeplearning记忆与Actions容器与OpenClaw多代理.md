# r278C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表+r278A/B 错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（可观测性） | OK | 外部 LLMOps 平台集成（LangSmith/Langfuse/Arize Phoenix 等 7 个）；内置监控面板+执行日志；OpenTelemetry（after_request 注入 X-Trace-Id/X-Span-Id 到 HTTP 响应头）；Dify Cloud 用量/延迟/成本/错误一览+日志历史；ARMS 接入（阿里云调用链视图） |
| 2 | n8n（源控制） | OK | Settings→Source Control（Enterprise）连 Git 仓库；push=序列化 workflows/credentials metadata（凭据值加密不进 repo）/variables；dev/prod 环境=链接不同分支 push-pull；不推荐同一实例 push+pull；GitOps 模式（workflows/ 目录 JSON 文件，AI agent 可写文件创建 workflow）；--separate 每 workflow 一个文件便于 diff |
| 3 | LangFlow（可观测性） | OK | 1.12 OpenTelemetry（service health+flow runs）；内建 Traces（trace/span 表、Flow Activity 页面）；外部平台（Langfuse/LangSmith/LangWatch/Openlayer/Arize/Instana-Traceloop）；K8s 生产监控（ELK/Fluentd 日志集中、Prometheus/Grafana 指标）；环境变量一键启用 |
| 4 | Activepieces（嵌入） | OK | Embed Builder=iframe 嵌入你应用（品牌化、containerId/builder 选项 disableNavigation/hideFlowName/dashboard hideSidebar）；Provision users=token 创建用户免二次登录；Preset connections=预设连接；Embeddable MCP（authRequestId→Authorize popup→code→token 流程）；navigate 路由（/flows /runs）；自托管嵌入保持私有 |
| 5 | Make（团队/角色） | OK | Teams=组织下至少一个 team；templates/connections/webhooks/keys/devices/data stores/data structures/custom functions/credential requests 都属于 team 且不可换 team；用户可属多 team；Custom roles（Enterprise 计划、组织/团队级自定义权限，private instance 不支持） |
| 6 | Pipedream（CLI 开发） | OK | pd dev=本地文件链接已部署组件、保存自动更新；pd deploy/pd publish（action 只能 publish）；TypeScript 组件先编译到 dist 再 publish（直接部署 TS 会失败）；pd login 链接账号；GitHub sync 本地编辑（clone repo→VSCode→push dev branch→UI pull）；Connect MCP env（PIPEDREAM_CLIENT_ID/SECRET/PROJECT_ID/ENVIRONMENT=development\|production） |
| 7 | Anthropic（Batch API） | OK | Message Batches API=异步处理大批量 Messages 请求；50% 折扣；多数批次 <1 小时完成（上限 24 小时）；批量结果 29 天可用；适用=评估/翻译/反馈分析等非实时大规模；提交最多 10,000 查询/批；创建即开始处理 |
| 8 | deeplearning（Agent Memory 课程） | OK | Agent Memory: Building Memory-Aware Agents（Oracle+LangChain：多记忆类型存储检索、语义搜索扩展工具访问、write-back loops 自主更新记忆、Memory Aware Agent 启动加载上下文）；Long-Term Agentic Memory with LangGraph（semantic→+episodic→+procedural 分层记忆）；核心问题=agent 会忘，每次会话从零开始 |
| 9 | GitHub Actions（service containers） | OK | services 运行 Docker 容器与 job 并行（Postgres/Redis/RabbitMQ/MongoDB）；health check（pg_isready/health-interval/health-retries）；"Infrastructure as a Sidecar"=不 mock 基础设施、跑真实一次性容器、job 结束容器消失；Linux runner 必须；端口映射+localhost 访问 |
| 10 | OpenClaw（多代理） | OK | Multi-agent routing=一个 Gateway 多隔离 agent（各带 workspace/state dir/SQLite 会话历史、channel bindings 路由）；Sub-agents=orchestrator 拆任务→spawn 子代理并发→回报组装（subagents 工具 list/steer/kill）；sessions_spawn=父建子代理隔离上下文结果自动回推；maxSpawnDepth 默认 1、开 2 解锁 orchestrator 模式；declarative manifest（delegationMode suggest/prefer、allowAgents allowlist、model 指定）；Coordinator+Workers 模式 |

## 判重（双键检索，增量判定）
- Dify 可观测（r278A 混合检索/r278B 插件）→ 新面（LLMOps 集成）
- n8n 源控制（r278B 数据转换）→ 新面（Git 版本控制）
- LangFlow 可观测（r278B 向量存储）→ 新面（traces/外部平台）
- Activepieces 嵌入（r278B piece 开发）→ 新面（嵌入 SDK/MCP）
- Make 团队（r278B 蓝本）→ 新面（组织/角色）
- Pipedream CLI（r278B 协作权限）→ 新面（本地开发）
- Anthropic Batch（r278A 缓存/r278B Computer Use）→ 新面（批量处理）
- deeplearning 记忆（r278A agentic RAG/r278B 编码代理）→ 新面（agent 记忆课程）
- GitHub Actions 容器（r278A 安全）→ 新面（service containers 集成测试）
- OpenClaw 多代理（r278A 安装/r278B 配置）→ 新面（sub-agents 编排）

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 可观测性（LLMOps） | 工具 |
| 2 | n8n 源控制与 GitOps | 工作流 |
| 3 | LangFlow 可观测性 | 工具 |
| 4 | Activepieces 嵌入 | 工具 |
| 5 | Make 团队与角色 | 工具 |
| 6 | Pipedream CLI 开发 | 可复用 Skill |
| 7 | Anthropic Batch API | 工具 |
| 8 | deeplearning Agent Memory 课程 | 可复用 Skill |
| 9 | GitHub Actions service containers | 工具 |
| 10 | OpenClaw 多代理编排 | 可复用 Skill |

## 复核
十独点均有当日实拉来源；均增量合并或新面；无并入未落地项。版本建议 3.52.0+。