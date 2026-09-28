# r280B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r280A 十词 + r279 全表 30 词 + r278 全表 30 词错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（model providers） | OK | Settings→Model Providers 添加供应商（OpenAI/Anthropic/Google/Cohere/通义/DeepSeek）；API key 输入+校验后可用；Usage Priority（自有 key 与 AI credits 共存时控制先用哪个+回退）；每模型负载均衡（多 key round-robin/auto-switching，DeepSeek R1 三策略保持在线）；marketplace 插件装 provider（DeerAPI base URL 可配）；自定义 model provider plugin（supported_model_types/help/icon）；OpenAI-API-compatible 插件 |
| 2 | n8n（templates） | OK | 官方社区模板库（6500+ AI/1350 sales/2949 marketing/AI chatbot 1269 等，任何人可贡献质量参差）；模板导入需填 credentials 并按需调配置；creator program+marketplace 进行中；第三方 n8n-library.com（2348 免费模板）与 n8ntemplates.me（12000+ 带 AI 生成）；engineering 类含"把 workflow 变 MCP server"模板（designing agent tools for outcome） |
| 3 | LangFlow（env/secrets） | OK | 全局变量（DB 存储+secret key 加密、可复用 credentials、可从 env var 源）vs 环境变量（LANGFLOW_PORT/LOG_LEVEL 部署级设置）；LANGFLOW_SECRET_KEY（Fernet 加密 + JWT HS256 签名；不设自动生成但生产必须显式设）；K8s 生产=Kubernetes secrets + secretKeyRef（values.yaml env valueFrom）或外部 secrets manager（HashiCorp Vault）；JWT 算法（HS256/RS256/RS512、PRIVATE_KEY/PUBLIC_KEY）；Langfuse 集成 .env 配三键 |
| 4 | Activepieces（AI actions） | OK | AI piece（Summarize Text/Run Agent 复杂多步任务 reasoning+tools+iterate）；OpenAI piece（Ask ChatGPT 9 fields/Ask Assistant）；Text AI piece（Ask AI 选 provider+model+prompt，例 RSS 聚合 gpt-4o）；Contextual AI（Grounded LM Generate Text）；Straico（Ask AI/RAG Prompt Completion/Create Agent）；AI MCP 6 tools（Ask AI/Summarize/Generate Image 链式调用同 run） |
| 5 | Make（scheduler/timezone，通用调度器实拉） | OK | 本站命中通用调度器判据（非 Make 特有，如实标注）：EventBridge Scheduler 按时区调整调度；Recurrence trigger date+time+timezone；Prefect cron day_or 默认 True（日/周 OR——与本库 §cron 判据同构）；Oracle UTC only 平台 DST 不自动调；UnifyApps timezone-aware（按业务时区不按服务器）；Logic Apps 未选时区 DST 会漂移 1 小时 |
| 6 | Pipedream（components） | OK | 组件=triggers+actions 自包含可执行单元；Sources 可本地开发经 CLI 部署或发布后 UI 实例化；Actions 只能发布；pd dev source.js 本地热重载（保存即自动更新部署组件）；组件代码维护在自己 GitHub repo；Registry 贡献（fork PipedreamHQ/pipedream→PR 审核）；TypeScript 组件（pnpm install）；/sources + /actions 子文件夹结构；props 捕获用户输入；REST API 建 source 先建 component（id/code/configurable_props） |
| 7 | Anthropic（Claude Code hooks） | OK | hook 事件全集：Setup/UserPromptSubmit/UserPromptExpansion/PreToolUse/PostToolUse/PostToolUseFailure/PostToolBatch/Notification/MessageDisplay/SubagentStart/SubagentStop/Stop/SessionStart/SessionEnd/ConfigChange/PermissionRequest/PreCompact/TaskCreated；PreToolUse=可 block/modify 工具调用（工作马，可审批/拒绝/改输入/升级用户）；PostToolUse=成功后不可 block 但提供上下文；PreCompact=压缩前备份 transcript（matcher auto）；用例：audit trail、lint 触发、通知、压缩前保数据 |
| 8 | GitHub（code search CLI/API） | OK | gh search code CLI；REST /search/code（q+qualifiers、text-match JSON、page/per_page/sort/order）；gh api 子命令发 REST 请求；注意 legacy code search engine（regex 新特性 API 没有、结果可能与 github.com 不一致）；code_search_url 端点模板 |
| 9 | deeplearning（prompt engineering，首查无返回补查成功） | OK | ChatGPT Prompt Engineering for Developers（Andrew Ng+Isa Fulford/OpenAI 联授、1h40m、9 视频课 7 代码示例、免费+证书）；两大原则（清晰具体指令 + 给模型思考时间）；Iterative 迭代开发（写 prompt→跑→分析失败→改进）；Inferring/Transforming/Summarizing/Expanding/Chatbot（系统消息+消息序列）；表达技巧（模型听不懂弦外之音） |
| 10 | OpenClaw（hooks） | OK | hooks=agent 事件触发时 Gateway 内运行的小脚本（目录自动发现+CLI 管理，类似 skills）；事件：command:new/reset/stop/command、session:compact:before/after、session:patch、agent:bootstrap；内置 hooks：session-memory（/new /reset 存会话到 /memory/）、bootstrap-extra-files（glob 注入）、command-logger（记 commands.log）、compaction-notifier（压缩前后可见通知）；plugin hooks=进程内扩展点（inspect/change agent runs/tool calls/message flow/subagent routing/installs/Gateway startup）；HOOK.md 脚本 vs plugin hooks 分工 |

## 判重（双键检索，增量判定）
- Dify 供应商（r280A 变量/r279A 分块/r279B 环境变量/r279C Agent/r278A 混合检索）→ 新面（供应商配置/Usage Priority/负载均衡）
- n8n 模板（r280A 表达式/r279A 错误/r279B 秘密/r279C LangChain/r278A queue）→ 新面（模板生态/社区库）
- LangFlow secrets（r280A widget/r279A 记忆/r279B API/r279C 工具/r278C 监控）→ 新面（全局变量 vs 环境变量/加密/JWT/Vault）
- Activepieces AI（r280A MCP/r279A 触发器/r279B AI pieces 已落但本面=AI actions 动作面）→ 增量合并（Ask AI/Run Agent/Summarize）
- 调度时区（r280A 优化/r279A webhook/r279B 调试/r278B 场景）→ 新面（通用调度器时区判据；与 §cron OR 判据同构但本面=DST/业务时区）
- Pipedream 组件（r280A 认证/r279A 调度/r279B 安全/r279C code steps）→ 新面（组件开发/Registry/pd dev）
- Claude hooks（r280A subagent/r279A 结构化/r279B 思考/r279C 缓存/r278C Batch）→ 新面（hook 事件全集/PreToolUse 拦截）
- GitHub 代码搜索（r280A reusable/r279A 技能市场/r279B Models/r279C Copilot/r278A Actions）→ 新面（gh search/REST API）
- deeplearning prompt（r280A 四模式/r279A 评估/r279B 多代理/r279C 可观测）→ 新面（两原则/迭代开发——与 §评估驱动互补）
- OpenClaw hooks（r280A 记忆/r279A 会话/r279B 开发/r279C 配置）→ 新面（hooks 事件系统/plugin hooks）

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 模型供应商配置与负载均衡 | 工具 |
| 2 | n8n 模板生态 | 工具 |
| 3 | LangFlow 环境变量与秘密管理 | 工具 |
| 4 | Activepieces AI 动作面 | 工具 |
| 5 | 调度时区纪律 | 工作流 |
| 6 | Pipedream 组件开发与 Registry | 工具 |
| 7 | Claude Code hooks 事件面 | 工作流 |
| 8 | GitHub 代码搜索 CLI/API | 工具 |
| 9 | deeplearning Prompt 工程两原则 | 工作流 |
| 10 | OpenClaw hooks 自动化 | 可复用 Skill |

## 复核
十独点均有当日实拉来源（第 9 站首查空已补查）；均新面或增量合并；无纯重复。第 5 站如实标注为通用调度器实拉（Make 特有未命中，未编造）。版本建议 3.57.0+。