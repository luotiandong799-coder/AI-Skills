# r249-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（可观测性面） | ✓ | 日志审计 2026 重构（OpenTelemetry 标准、结构化 JSON、分布式追踪 TraceID 关联、实时审计告警；覆盖用户操作/LLM 调用/RAG 检索/工作流执行全生命周期）；OpsTraceManager（异步可扩展派发 rich trace 到多第三方平台；凭证加密/动态 provider 实例化/重试机制）；外部可观测集成（Langfuse/LangSmith/Arize Phoenix/Opik/W&B Weave；全节点分布式追踪；token 用量成本追踪；每节点延迟分析；错误追踪含全上下文与堆栈；A/B 实验跟踪）；集成层异步后台 workers 不影响应用运行时性能——外部平台故障不影响用户应用；Trace 视图检查中间值定位出错节点 |
| 2 | n8n（表达式/数据映射面） | ✓ | Expressions（JS-like 直接放节点参数 {{ }} 语法；$json 取数/工作流元数据/env 变量；轻转换就地做）；Edit Fields (Set) 节点做数据转换（添加字段/修改值/删除重命名；分离数据转换与业务逻辑）——最佳实践：以转换为目标用 Set 节点而非表达式堆砌；安全表达式（可选链 user?.profile?.email ?? ''；数组 ?.[0]?.name ?? 'No items' 避免嵌套 null 崩溃）；API keys/tokens 用 credentials 而非 env vars；转换四类（添加字段/修改字段/映射/清洗） |
| 3 | LangFlow（部署/认证面） | ✓ | 安全基线（LANGFLOW_AUTO_LOGIN=False；非默认 LANGFLOW_SECRET_KEY；反代+认证）；JWT（HS256 单服务器/开发；RS256 生产公私钥对）；外部认证（LANGFLOW_EXTERNAL_AUTH_ENABLED=true；Keycloak JWKS/OIDC；内置 JWT 先试外部兜底）；API 密钥（x-api-key 认证；只返回一次立即存储；密钥权限 Read/Execute 配置）；CORS 具体 origins；CVE-2026-5027/33017 未认证 RCE（不直接暴露公网、反代/VPN 边界、出站过滤限制 exfil 通道） |
| 4 | Activepieces（Copilot/agent builder 面） | ✓ | AI Agent Builder（配置 agent 用 tools/memory/human-approval checkpoints 非 prompt wrapper；设目标选 apps/flows/files 让 agent 决定步骤执行；要审的等审批）；Chat to Automation（自然语言描述→生成起始 flow 再精修）；MCP 原生（400+ MCP servers 最大开源 MCP 工具集；MCP 作 server+client 双角色；integrations 兼作 MCP servers 供 Claude Desktop/Cursor 调用）；内置 AI agents/Todos HITL 审批系统；模型 provider 管理员配置一次（your model your key）；per-active-flow 定价 |
| 5 | Make（性能优化面） | ✓ | 操作成本（每模块=1 operation；filter 前置省 40% op；bulk/聚合器省 70-98% op）；性能（Router 并行化省 50% 时间；聚合器批量 API 调用）；智能分页（Iterator+Sleep 批处理 100 行避免 timeout）；计划（off-peak 批量；webhook 优先于 polling）；批量写+断点续传（datastore 缓冲受控块写；checkpoint last page/cursor/timestamp 重放安全）；大文件可恢复（chunked upload <3MB）；重试抖动（delay 加 random(0;30) 分散负载）；AI agent 最佳实践（工具命名与描述决定 agent 选工具） |
| 6 | Pipedream（triggers/schedule 面） | ✓ | Trigger 四型（HTTP/Webhook 唯一 URL；Cron 时间表；Email 入站；Event sources 应用事件）；Schedule 触发（intervalSeconds 或 cron 表达式+timezone；Schedule API custom interval/daily/monthly/weekly 时区支持）；Timer interface（$.interface.timer prop；interval 或 cron）；部署 workflow 后每次请求都触发；cron 表达式完全控制时间（简单 interval picker 不能指定一天内具体时间） |
| 7 | Anthropic（Claude Code hooks 面） | ✓ | Hook 事件清单（UserPromptSubmit/PreToolUse/PostToolUse/PostToolUseFailure/PostToolBatch/Notification/MessageDisplay/SubagentStart/SubagentStop/TaskCreated/Stop/ConfigChange/PreCompact/SessionStart/TeammateIdle/TaskCompleted）；阻断模式（top-level decision: block+reason；exit code 2 blocks；continue:false）；注册位置（settings.json/managed policy/skill-agent frontmatter）；Hook 类型（command/HTTP/mcp_tool 确定性触发；prompt/agent 用 Claude 判断）；exec form vs shell form（command+args 无 shell 直接 spawn）；async 后台不阻塞；matcher 匹配（Bash(git *)）+if 条件；用途（PreToolUse 拦截危险命令/验证路径/自动批准安全操作；PostToolUse 格式化/lint/日志；PreCompact 备份 transcript 保留重要决定；SessionStart 注入 git status/TODO/环境）；低上下文成本 |
| 8 | OpenClaw（memory 面） | ✓ | 三文件记忆（MEMORY.md 长期持久事实偏好决策会话开始加载；memory/YYYY-MM-DD.md 每日笔记）；MEMORY.md 放什么（API 配置位置——不是密钥本身；项目结构约定；重要决策+理由；反复问题与解法）；分层记忆（原始对话日志层→实体图谱层：人/项目/公司/偏好提取连接）；Honcho 记忆（跨会话持久化到专门服务；用户建模 profile 偏好事实沟通风格；agent 建模）；语义搜索跨所有记忆；文件支撑（记住保存的 workspace 内容，不是所有聊天出现过的）；Memori（创建自动、召回 agent 控制；多维排名算法） |
| 9 | GitHub（trending 生态面） | ✓ | Trending 2026-09-21（AI agents 主导 dev tools：diffusion studio/editor 开源视频编辑器 edits as code）；Top100 AI agents（herdr 40805 stars Rust 编码 agent 运行时；TiDB agentic workloads vector search）；digest 09-01（deepseek-harness Everything is a Plugin 208k stars）；jev-chat-jarvis（手机对话副驾 6591 stars Kotlin QQ/X/飞书读屏候选回复）；new-api（统一模型网关 48.9k Go OpenAI/Claude/Gemini 兼容格式转换）；JeecgBoot（低代码 v2.0 AI Skills 一句话画流程/表单/报表/大屏 47.9k Java）；OpenClaw 363k stars 多通道个人助手；Hermes Agent 113k 自改进学习循环；ZeroClaw 30.5k 精简 Rust；NanoClaw 27.8k 容器隔离；Evolver 6.7k 可审计自进化；n8n 205.8k；Brave Search MCP 90.6k |
| 10 | skills.sh（registry 面） | ✓ | skills.sh（Agent Skills Directory 66 万+ skills 2026-06；npx skills add owner/repo 一键安装 GitHub 托管 SKILL.md；匿名遥测自动上 leaderboard；API V1Skill 统一形状；官方技能 660+/dev teams 56/categories 9）；分发模型（GitHub repo+SKILL.md+README）；localskills.sh（package-manager 式 registry：SKILL.md 根+docs/scripts/templates 文件夹包 100MB/500 文件每版本；版本化 rollback；visibility public/private/unlisted；下载分析）；skillshub（GitHub URL 直装无需 registry；taps 组织；~/.skillshub/skills 一次安装多 agent；skillshub link 同步；版本追踪 commit） |

## 判重基准
双键检索（相对 r244-r248 已落章节）：Dify（r248-B 落执行引擎——可观测性 OpsTraceManager/第三方集成/异步隔离为独有新面）；n8n（r247-B 落 Code 节点契约——表达式安全写法/Set 节点职责分离为独有增量）；LangFlow（r248-B 落 lfx 验证链——部署安全 AUTO_LOGIN/JWT/OIDC/CVE 教训为独有新面）；Anthropic（r247-B 落 OpenClaw Hook 生命周期四步——Claude Code hooks 事件清单/阻断模式/matcher/注册位置为独有增量深化）；GitHub（r224/r226 落旧热度榜——本批最新榜+生态分层观察为增量更新）。未选素材：Activepieces AI Agent Builder（tools/memory/approval checkpoints 非 prompt wrapper+Chat to Automation+MCP 双角色）；Make 性能优化（filter 前置省 40%/聚合省 98%/Router 并行省 50%/重试抖动/断点续传）；Pipedream triggers 四型（HTTP/cron/email/event sources+timer interface）；OpenClaw memory 三文件（MEMORY.md 长期+每日笔记+Honcho 用户建模）；skills.sh registry（npx skills add+匿名遥测 leaderboard+localskills 版本化 rollback）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 可观测性 | OpsTraceManager 异步派发+第三方集成+异步隔离 | 工具/工作流 | wb-execute-discipline |
| ② n8n 表达式安全写法 | 可选链+fallback+Set 节点职责分离 | 工具/工作流 | wb-execute-discipline |
| ③ LangFlow 部署安全 | AUTO_LOGIN/JWT 分级/OIDC/API 密钥权限 | 工具/工作流 | wb-execute-discipline |
| ④ Claude Code hooks | 事件清单+阻断模式+exec form+matcher | 工具/可复用 Skill | wb-execute-discipline |
| ⑤ trending 生态观察 | agent-first 工具主导+生态分层 | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
