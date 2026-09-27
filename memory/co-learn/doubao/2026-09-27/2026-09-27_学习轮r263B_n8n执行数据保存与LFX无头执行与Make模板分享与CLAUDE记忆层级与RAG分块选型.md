# r263B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（错误处理面） | ✓ | 错误重试+异常处理同时开启时**优先重试节点，重试失败再走异常处理**；Code node Retry Settings 最多 10 次自动重试（间隔最大 5000ms）；Error Handling 定义 fallback 路径；v0.14.0 引入（2024-12）；Human Input Node（v1.13.0）三按钮 Confirm/Regenerate/Forward 各映射分支，超时 3 天自动 forward；Supervisor agent mode 协调多 sub-agents；Agent loop 改进 tool-call retry+并行工具执行；**Dify 不原生支持 scheduled 执行**——用 XXL-JOB 调度并带告警可观测 |
| 2 | n8n（执行数据面） | ✓ | EXECUTIONS_DATA_PRUNE_MAX_COUNT 默认 10,000（超量从旧到新删）；EXECUTIONS_DATA_MAX_AGE 默认 336h=14 天；new/running 状态执行不删；**高频大 payload 防 OOM 技巧**：EXECUTIONS_DATA_SAVE_ON_SUCCESS=none + SAVE_ON_ERROR=all（失败仍可调试）；分块处理（10,000 行改 200 行/execution）；避免 Code node；避免手动执行；子工作流返回有限数据；Insights 保留 365 天（N8N_INSIGHTS_MAX_AGE_DAYS）封顶 730 天；AI Agent 每节点接受一个 memory sub-node（Chat Memory Manager 查大小/清条目） |
| 3 | LangFlow（LFX 执行面） | ✓ | LFX=轻量 CLI+Python 库无头运行 flow JSON（stateless、minimal dependencies、no database、no UI）；比 --backend-only 更轻（无需装 Langflow 包+依赖）；两命令 serve/run；`lfx run my_flow.json "问句" --format json/text/message/result`；flow graph 存内存免数据库加载；Workflow API（Beta）：mode stream/background（background 立即返回 job_id 异步）+GET /api/v2/workflows?job_id 查询 |
| 4 | Activepieces（密钥管理面） | ✓ | 关键 env：AP_FRONTEND_URL（webhook/redirect 需公网可达）/AP_ENCRYPTION_KEY（32 字符 16 字节 hex 加密 connections，openssl rand -hex 16）/AP_JWT_SECRET（32 hex 签 JWT）/AP_EXECUTION_DATA_RETENTION_DAYS/AP_SCHEDULED_WORKER_CONCURRENCY 默认 10；Secret Managers 集成外部（HashiCorp Vault——连接对话框 key icon 选 Vault，secret path 格式 mount/data/path/to/secret/key）；Project Variables=project 级命名值跨任意 flow/step 引用（API key/webhook URL/Slack channel ID/feature flag，不随 run 变）；Project Replace CLI（源/目标实例迁移 project，API key flag 或 env）；managed secrets 每环境变量+RBAC |
| 5 | Make（模板分享面） | ✓ | blueprint=可复用场景版本（含模块/模块设置/mapped values）——导出备份/换账号/分享导入；Scenario sharing 链接分享（无需登录可看公开页，链接总是最新保存版比 blueprint 更灵活）；Templates 画廊（make.com/en/templates 按 app/category/use case 过滤，Use Template 一键复制，所有 plan 含 free）；API clone scenario（POST /scenarios/{source_id}/clone {teamId,name}）；Templates API（/templates/{templateId}/blueprint，templates:read scope）；生产级 blueprint 框架（导出再激活/controlled clone+activation checklist/共享逻辑移入 subscenario 内部服务契约） |
| 6 | Pipedream（secrets 面） | ✓ | env vars 分离 secrets 与代码（process.env.API_KEY）；安全最佳实践两方式：connected accounts（平台支持 app 优先）/env vars（不支持或任意配置）；外部凭证运行时获取（HashiCorp Vault/AWS Secrets Manager/DB/Nango 拉取传给步骤）；**components 内 env vars 不可直接访问**——用 secret props（true 时浏览器隐藏 password 式+数据库加密+运行时解密，仅 string props）；Python 步骤 os.environ；SDK projectEnvironment development/production |
| 7 | Claude Code（memory 层级面） | ✓ | 四层记忆：Enterprise policy（/etc/claude-code/CLAUDE.md 系统级组织 wide IT 分发）/User（~/.claude/CLAUDE.md 个人全项目）/Project（./CLAUDE.md 或 .claude/CLAUDE.md 团队共享版本控制）/CLAUDE.local.md（个人项目级 gitignore，最后读）；**根 CLAUDE.md session start 全量加载且 compaction 后重读不丢**；子目录 CLAUDE.md on-demand（读该目录文件时才加载非 session start）；AGENTS.md 独立或并行加载；目录层级上方 CLAUDE.md 全量加载 |
| 8 | GitHub Codespaces（devcontainer 面） | ✓ | Copilot CLI 含在默认 Codespaces 镜像+Dev Container Feature（npm/Homebrew/WinGet/脚本/独立可执行多方式安装，2026-02-25 GA）；VS Code 1.138 agentHost.devContainer.enabled（Agents window 在 Dev Container 里跑 agent session——用项目 toolchain 非本地环境）；Claude/Codex 作为 coding agents 在 github.com/GitHub Mobile/VS Code（Copilot Pro+/Enterprise，2026-02-04 public preview）；Microsoft Agent Framework 支持 GitHub Copilot SDK 后端；VS Code agent orchestration（子 agent 各自 context window 防溢出）；BYO model key（Business/Enterprise 用户自链 API keys OpenRouter/Foundry/Google/Anthropic/OpenAI + 本地 Ollama） |
| 9 | OpenClaw（hooks 面） | ✓ | 两类：internal hooks（Gateway 进程内小 JS/TS handler，事件型：command:new/reset/stop/session:compact:before/gateway startup/message flow/tool result——save session context/log reset/短副作用）+Plugin hooks（api.on(...) 修改 prompts/拦截 tools/控制 replies/带优先级和返回值）；Webhooks 外部 HTTP 触发（CI/CD build status/monitoring alerts/command events）；openclaw hooks 管理；不 fork 产品加行为 |
| 10 | WaytoAGI（RAG 分块面） | ✓ | 选型树：fixed（基线）/semantic（长文低 recall 时）/parent-child（recall+大 context 平衡最优）/late chunking（跨块语义：法律/科学/多节报告）/RAPTOR 层级（多跳）；结构感知分块（Markdown/HTML 按 heading 边界先切再细分超限段）；metadata 必含（source/section title/page/date 过滤引用）；embedding max length 超限静默截断；hybrid sparse+dense（BM25/SPLADE 罕见词/命名实体）；pin embed model+距离 metric+chunker 配置可复现；chunk 为原子事实+deliberate overlap；调参（dense 多主题减小 chunk/boundary misses 增 overlap）；语义分块提分 15-20% |

## 判重基准
双键检索：n8n 执行数据保存策略（§6085 是 community node 供应链——执行数据管理新面）；LangFlow LFX（SKILL.md 无 LFX 标题章节——独立包/run 命令格式/Workflow API background 为新面）；Make 模板分享（无章节——blueprint 定义/Scenario sharing 链接/API clone 为新面）；Claude Code memory 四层（SKILL.md 无 memory 层级标题——四层表/on-demand 加载/enterprise policy 为新面）；RAG 分块选型树（§6229 LangFlow RAG 评测管评测——分块策略选型为增量）。备选并入记录：Activepieces 密钥/Vault/Project Variables、Dify retry+error 叠加顺序/XXL-JOB 调度、OpenClaw internal vs plugin hooks 分工、Pipedream secret props。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 |
|---|---|---|
| ① n8n 执行数据保存策略 | SAVE_ON_SUCCESS=none 防 OOM/剪枝默认/分块 | 工作流 |
| ② LangFlow LFX 无头执行 | 独立包 stateless/serve+run/Workflow API background | 工具 |
| ③ Make 场景模板与分享 | blueprint/Scenario sharing 链接/API clone | 工作流 |
| ④ Claude Code memory 四层 | Enterprise/User/Project/local+on-demand | 工作流 |
| ⑤ RAG 分块选型树 | fixed→semantic→parent-child→late→RAPTOR | 可复用 Skill |

## 复核
五独点均有当日实拉来源；②③④⑤按增量判定合并保留增量；①为新面；备选并入记录。垃圾：本轮未产生临时文件。
