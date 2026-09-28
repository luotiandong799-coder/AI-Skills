# r283A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站；查询词与 r282 三十词 + r281 三十词 + r280 三十词 + r279 三十词 + r278 三十词 + 更早全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（错误处理/重试） | OK | **节点级错误处理三策略：重试（最多 10 次、间隔最大 5000ms）/ 返回类型化默认值 / 失败分支路由（fail branch）**；同时开启错误重试+异常处理时**优先重试、重试仍失败才走异常处理**；LLM/HTTP/Code/Tool 四类节点支持；DeepWiki 建议：指数退避+回退模型提供商+Continue on Error+If-Else 错误分支；HTTP 节点失败重试 3 次示例 |
| 2 | n8n（日志流/可观测） | OK | **可观测三层：内置执行痕迹（节点输入输出可查）→ OpenTelemetry 追踪（N8N_OTEL_ENABLED，agent 追踪 N8N_AGENTS_TRACING_ENABLED）→ log streaming 外送（Enterprise：Datadog Logs/Grafana Loki/云存储，支持匿名化脱敏）**；N8N_LOG_LEVEL=debug 细节；Grafana n8n Workflow Traces dashboard（n8n 2.19+，Tempo datasource）；**Error Trigger + Data Tables 中心化审计日志模式（AuditLog/ErrorLog 两张表跨 workflow 复用）**；execution data redaction（Enterprise）；Insights dashboard（Pro+） |
| 3 | LangFlow（数据库配置） | OK | **默认 SQLite（sqlite:///./langflow.db）→ 生产推荐 PostgreSQL 15+**；LANGFLOW_DATABASE_URL 环境变量；SQLite 路径须绝对；**多 worker 部署需要外部 PG + Redis job queue + LANGFLOW_GUNICORN_PRELOAD=true**；pgvector 作 vector provider（需 CREATE 权限+可选依赖）；K8s 最佳实践：4Gi RAM/2 CPU/多副本、work_mem 调优；LANGFLOW_CONFIG_DIR 存日志/文件存储/监控/密钥 |
| 4 | Activepieces（piece 开发） | OK | **TypeScript 构建 pieces；本地开发 AP_PIECES_SYNC_MODE 从 dist 加载**；**贡献流水线：离线开发→package.json 版本递增→PR→合并后 CLI/GitHub Action 触发同步**；发布 CLI（npm run publish-piece-to-api，API Key 从 Admin Settings 生成）；trigger 创建（npm run cli triggers create）；piece 分类 custom（自用）/community（社区共享）；社区流程：测试→贡献→审查（质量/安全/可用性）→市场分发；贡献奖励 +1,400 tasks/月云额度 |
| 5 | Make（场景克隆/蓝图） | OK | **克隆时可保持轮询触发器状态：Yes=从原场景最后处理项继续，No=从头开始**；**蓝图（blueprint）=可复用版本（含模块设置+映射值），备份/跨账号/分享导入**；克隆现在复制 notes（设置提示+交接细节）；**replay=用历史触发数据重跑当前版本场景（调试/恢复/受控回填，消耗 credits、非批量）**；蓝图上线战术：克隆生产→staging→改→replay 代表历史 run→临时禁用通知路由防重复；模板库 1000+ 预置流；module migrator 自动更新 legacy 模块 |
| 6 | Pipedream（版本/回滚） | OK | **deploys 不可变（immutable），只能部署新版本**；v2 无自动回滚；**Versions 标签页可手动 Deploy 旧版本恢复为 active**；**GitHub Sync=完整 git 版本历史（行级），未部署变更进 undeployed-changes 前缀分支**；changelog 追踪 git 活动（合并出错排查）；无内建 per-step 版本历史（GitHub sync 补足）；Inspector events log 可重放生产事件 |
| 7 | Claude Code（后台/动态工作流） | OK | **dynamic workflows=JS 编排脚本后台运行大量 subagent，会话保持响应**；适用：全代码库 bug 扫查/500 文件迁移/多角度研究交叉核验；**/workflows 列出运行中/已完成 workflow，进度视图显示每阶段 agent 数**；claude -p 等后台 subagent/workflow 完成（默认 10 分钟连续 idle 上限）；**routines=保存的配置（prompt+repos+connectors）打包自动跑（Anthropic 云端或自托管，定时 hourly/nightly/weekly 触发）**；scheduled tasks 错过时间不补（fires once 当 idle 时）；Dispatch（Cowork）=long-running 后台 agent |
| 8 | GitHub（AGENTS.md 规范） | OK | **2500+ 仓库经验：代码示例优于解释（一个真实代码片段胜过三段描述）、设明确边界（never touch：secrets/vendor/production config）、具体技术栈（"React 18 with TypeScript, Vite, Tailwind"）**；必填 Commands/Testing/Code Structure，推荐 Code Style/Git Workflow；**150 行以内（每 token 每次请求都加载，长文件拖慢 agent）**；**随代码变更同步更新（stale 指令比没有更糟，主动误导）**；负面指令最有用（"Never commit secrets"最常见）；链接不重复；start simple→iterate often；Addy Osmani：Layer 1 概览/Layer 2 构建与验证命令按序 |
| 9 | OpenClaw（agents 管理/团队） | OK | **openclaw agents 管理隔离 agent（workspace+auth+routing）；角色模板四件套：coordinator（Chief of staff 协调专家作单点）/researcher（收集证据返回引用简报）/writer（简报+素材→草稿）/reviewer（对照需求检查产物返回可操作发现）**；**team CLI：add-agent/remove-agent/scale --agents [count]**；agents.list 数组（identity/workspace/model/capabilities）；MEMORY.md 每 agent 一份自动维护；**AGENTS.md=agent registry（Triage Agent 读它决定何时部署哪个专家）**；sandbox per-agent（off/all，scope agent=每 agent 一容器）；Dashboard 卡片（绿 active/黄 idle/红 disconnected、restart/改 skill 配置/切换平台/归档） |
| 10 | deeplearning.ai（红队课程） | OK | **Red Teaming LLM Applications（Giskard 合作，1h29m Beginner）**：课程四步=Overview of LLM Vulnerabilities（18m 视频+代码）→ Red Teaming LLMs（13m）→ Red Teaming at Scale（17m）→ Red Teaming LLMs with LLMs（10m）→ Conclusion+**Graded Quiz 通过获 Accomplishment**；主题：AI Safety/Chatbots/Generative Models/LLMOps/Prompt Engineering |

## 判重（双键检索，增量判定）
- Dify 错误处理（r267C n8n 工具失败/r269A n8n 错误工作流）→ Dify 侧节点三策略+重试优先规则为独有增量 → **新面/增量合并**
- n8n 可观测（r270C Dify 可观测/r274A Pipedream 可观测/r278C LangFlow 可观测）→ n8n OTel+日志流+中心化审计表为新面 → **新面**
- LangFlow 数据库（r268C Dify 自托管/r275A LangFlow 部署 API）→ 生产数据库迁移+多 worker 依赖为新面 → **新面**
- Activepieces 开发（r269A Dify 插件开发/r274C LangFlow 模板）→ TypeScript 本地开发+CI/CD 发布流水线为新面 → **新面**
- Make 克隆（r281B Make 回滚/r275C 版本）→ 克隆状态保持+蓝图+replay 战术为新面 → **新面**
- Pipedream 版本（r271A 组件/r282C sources）→ 部署不可变+Versions/GitHub Sync 为新面 → **新面**
- Claude 动态工作流（r282C subagents）→ JS 编排脚本+后台执行+routines 为独有增量 → **增量合并**
- AGENTS.md（此前未实拉过该主题）→ 全新方向 → **新面**
- OpenClaw 团队（r278C OpenClaw 多代理）→ 角色模板+team CLI+registry 路由为独有增量 → **增量合并**
- deeplearning 红队（r275A 安全/r280C 微调）→ 红队四步方法论为独有增量 → **增量合并**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 节点级错误处理三策略 | 工具 |
| 2 | n8n 可观测三层与中心化审计 | 工具 |
| 3 | LangFlow 生产数据库迁移 | 工具 |
| 4 | Activepieces piece 开发流水线 | 可复用 Skill |
| 5 | Make 场景克隆与蓝图回放 | 工作流 |
| 6 | Pipedream 部署不可变与版本治理 | 工具 |
| 7 | Claude 动态工作流与后台执行 | 工作流 |
| 8 | AGENTS.md 写作规范 | 可复用 Skill |
| 9 | OpenClaw 多 agent 团队编排 | 工作流 |
| 10 | LLM 红队方法论 | 工作流 |

## 复核
十独点均有当日实拉来源；四点增量合并（均含≥40% 独有增量）、六点新面；无纯重复。版本建议 3.65.0。