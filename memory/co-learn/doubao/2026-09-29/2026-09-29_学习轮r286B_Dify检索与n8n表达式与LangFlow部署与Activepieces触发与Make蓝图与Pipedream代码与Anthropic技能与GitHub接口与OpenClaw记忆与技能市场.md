# r286B 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r284/r285/r286A 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（RAG/知识库） | OK | **RAG 是"检索→生成"两段式，知识作为补充 truth source 减少幻觉**；**Dify 内置评估套件：Answer relevance（答案是否回答问题）/ Context precision（chunk 相关性）/ Faithfulness（答案是否忠于 context）/ Citation accuracy（引用正确性）——RAGAS 式框架**；**Summary Index（1.12.0）：每 chunk 附 summary 字段，语义相关内容一起检索——GraphRAG 轻量替代，解决"只返回最相关单片段缺上下文"**；**多模态检索：Embedding（首轮向量粗匹配）+ Reranking（二次精排视觉/文本证据）两阶段**；**向量库选择：Built-in（默认，中小知识库）/ pgvector / Qdrant / Weaviate**；**优化实测（CSDN）：自定义 chunk 策略+混合检索+per-dataset score threshold，响应 P95 1240→380ms、NDCG@3 0.217→0.912（+4.2×）、误召回率 18.6%→4.3%** |
| 2 | n8n（表达式/数据转换） | OK | **表达式 `{{ }}` 在节点参数里做轻转换（$json.body.city / $json.score*2），不加节点保持逻辑就近**；**Code 节点复杂转换（JS/Python），返回 [{json:data}] 格式**；**AI Transform 节点（LLM 转换）**；**转换三选：表达式（轻）/ Code 节点（复杂）/ AI Transform（语义）**；**AI 代码帮助：Code 节点写自然语言 prompt 让 AI 生成 JS**；**JS 技巧：Object.keys/values、合并 {...defaults,...overrides}、解构删除字段 {password,...safeData}、Object.fromEntries 重命名**；**API key 用 proper credentials 不用环境变量** |
| 3 | LangFlow（部署/性能） | OK | **内存优化：依赖裁剪+worker 生命周期管理+Linux CoW，~89% 内存下降（v1.9→v1.10）**；**生产部署：headless runtime（backend only）跑 API；K8s 最小资源：frontend 512Mi/0.3 CPU、backend 1Gi/0.5 CPU**；**多 worker：LANGFLOW_WORKERS 从少开始防 OOM + GUNICORN_PRELOAD + max-requests+jitter**；**性能优化：缓存 LLM 调用/batch 节点/异步 I/O/连接池/Prometheus+Grafana 监控**；**Redis-backed job queue（1.10+）跨 worker 共享 build events**；**安全：.env 不入库** |
| 4 | Activepieces（触发器/调度） | OK | **触发器三技术：Polling（定时轮询端点查变更）/ Webhooks（单 URL 监听用户事件）/ App Webhooks Subscriptions（OAuth2 开发者 app 单 URL 收所有授权事件）**；**内置控制：Branching/retries/waitpoints/subflows/error handling/human approvals**；**数据脱敏：敏感细节不出现在日志（data masking）**；**430+ 连接器（CRM/billing/support/data/dev tools），凭证加密**；**Chat 起草流程（AI-first 工作台）**；**cron-like 调度：时区感知** |
| 5 | Make（蓝图/模板） | OK | **Blueprint=可复用场景版本（含模块/设置/映射值），可导出 JSON、备份、分享导入**；**模板两类：Public（Make+社区，7,500+ use cases）/ Team（团队内共享可公链分享）**；**参数命名规范：snake_case、必需字段标 Required（坏 payload 快速失败）、每个参数加 description、有限值用 Select 防业务逻辑漂移、数组定义嵌套 item 类型、集合稳定时定义 specification、可选字段默认值**；**设计围绕 canonical payload（路由和映射在 app 变更时存活）；分离 orchestration 与可复用 utilities 用 subscenarios**；**备份纪律：导出 scenario blueprint JSON 是唯一完整恢复机制** |
| 6 | Pipedream（AI/代码步） | OK | **代码步 defineComponent({async run({steps,$})})，$.export 导出数据**；**AI 代码生成：Code 节点写 prompt 让 AI 生成 JS 流式进编辑器**；**MCP connect：Pipedream MCP 接 Vercel AI SDK（clientId/clientSecret 鉴权）**；**预处理模式：Slack 消息去 @botname 提取纯问题文本再送 GPT；过滤短消息/机器人消息防误触发**；**$.respond()/$.flow.exit() 控制响应**；**props 自动刷新显示连接账号与输入字段** |
| 7 | Anthropic（Skills API/最佳实践） | OK | **Skills API + Files API：skill 是"instructions+scripts+templates 文件夹"，任务需要时才加载；Skills API 上传/版本化自己的 skill 并 attach 到请求，跑在 Claude 代码执行沙箱——不需要自己 host**；**trigger 调优：undertriggering（该加载没加载/用户手动启用）→ 加细节与关键词；overtriggering（无关查询也加载/用户禁用）→ 加 negative triggers 更具体；execution issues（结果不一致/API 失败）**；**SKILL.md 结构：name+description（max 1024 字符，唯一 metadata）+ Instructions + Examples；body 建议 <500 行，详细 checklists/templates/examples 放 references**；**Skills vs prompts/Projects/MCP/subagents：Skills=任何 Claude 实例可加载的能力；subagents=独立完整 agent 自管上下文工具权限；配合用：code-review subagent 用语言特定 skill**；**可移植性是核心：一个 SKILL.md 文件夹无修改跑 Claude Code/Codex CLI/Cursor/Antigravity + 9 更多 agent——警惕厂商锁定**；**Unix-style 路径跨平台，Windows-style 报错** |
| 8 | GitHub（Search API/Actions） | OK | **REST Search 端点（/search/code 等），X-GitHub-Api-Version 头**；**rate limit：code_search limit 10 每分钟（低）**；**gh search code：legacy code search 引擎，regex 搜索 API 还不可用**；**Actions API：/repos/{owner}/{repo}/actions/workflows 列出/管理 workflow 文件与 runs；workflow runs 查询返回"less precise but more accurate"记录数（2026-09 变更）**；**GitHub Actions permissions：pull-requests/security-events 等按权限粒度写（read/write），Dependabot/secret scanning alerts 不能用此权限读，需要 GitHub App 或 PAT**；**gh api 在 workflow 里跑 API（GH_TOKEN secrets）**；**GraphQL+Actions 自动化 Project（PR ready for review 时加 task 设 Status）** |
| 9 | OpenClaw（记忆/工作流） | OK | **四记忆文件：USER.md（稳定偏好/沟通风格/关系/活动项目上下文，指令式，会话开始小预算加载）/ MEMORY.md（长期记忆，持久非 profile 事实与决定）/ daily logs（memory/YYYY-MM-DD.md append-only，会话开始读今天+昨天）/ memory-wiki**；**重要信息写入 daily；定期 review daily 更新 MEMORY.md；"remember" 指令直接写记忆文件**；**为什么用文件：token 无限制、上下文不溢出、不会忘、定期维护修剪**；**Memory-Wiki（v2026.4.7）：结构化知识系统，分类+链接 vs 向量语义搜索——不是更长上下文而是跨会话 agent 可读可写的 Wiki**；**三态存储：Short-term Context（RAM）/ Long-term Structured Storage（SQLite/JSON）/ Semantic Memory（向量库 RAG，Pinecone/Milvus）**；**MEMORY.md 适合：API 配置位置（不是 key 本身）/项目结构约定/重要决定与理由/反复问题解决方案** |
| 10 | AI 技能市场（skills.sh/SkillsMP 等） | OK | **skills.sh = "the npm for agent skills"（Vercel 目录+排行榜，57k+ 公开技能，npx skills add <owner/repo> 一键安装，按安装数排名）**；**SkillsMP = "Google for agent skills"（聚合器，自动索引 GitHub，2,154,976 收集 SKILL.md，无策展）**；**agentskill.sh = CLI 商店（search/info/install 单技能或整套）**；**LobeHub（~170k，分类浏览）**；**生态分层：skills.sh 排行榜（安装数排名）/ SkillsMP 聚合（raw index）/ ClawHub 注册表（registry 版本化 agent-native CLI）/ anthropics/skills 官方（Git 历史版本）/ localskills.sh 替代（私有技能+版本回滚+团队角色+一次安装多工具）**；**claudemarketplaces.com ~6,700 条（广覆盖少策展）**；**技能市场选型判据：curation 质量/版本化/安装方式/团队功能** |

## 判重（双键检索，增量判定）
- Dify RAG 评估（r284B 已落检索优化）→ 重叠约 50%，增量=评估四指标（RAGAS 式）/Summary Index/多模态两阶段（≥40%） → **合并保留增量**
- n8n 表达式（r285B 凭证、r286A 错误恢复）→ 表达式三选/AI 代码生成 新面 → **新面**
- LangFlow 部署（r284 记忆、r285B 存储、r286A 缓存）→ 部署/多 worker/内存优化 新面 → **新面**
- Activepieces 触发器（r284 分支、r285B 错误、r285C MCP、r286A 版本）→ 三技术分类/数据脱敏 新面 → **新面**
- Make 蓝图（r285A 已落场景蓝图八块）→ 重叠约 60%，增量=参数命名规范/canonical payload/subscenarios 分离（≥40%） → **合并保留增量**
- Pipedream 代码步（r285C 共享、r286A 触发器）→ 代码步/MCP 接入 新面 → **新面**
- Anthropic Skills（r285B 已落 Skills 结构）→ 重叠约 55%，增量=Skills API 上传版本化/触发调优（undertrigger/overtrigger）/Files API（≥40%） → **合并保留增量**
- GitHub Search API（r285A Copilot、r285C MCP）→ Search API/Actions 权限粒度 新面 → **新面**
- OpenClaw 记忆（r285B 已落记忆持久化）→ 重叠约 55%，增量=四记忆文件分工/USER.md/Memory-Wiki 结构化知识/三态存储（≥40%） → **合并保留增量**
- 技能市场（r285C 已落 agentskills 生态）→ 重叠约 55%，增量=skills.sh npx 安装命令/LobeHub/生态分层表（≥40%） → **合并保留增量**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify RAG 评估四指标与 Summary Index（合并增量） | 工作流 |
| 2 | n8n 表达式三选与 AI 代码生成 | 工具 |
| 3 | LangFlow 部署性能与多 worker | 工作流 |
| 4 | Activepieces 触发器三技术与数据脱敏 | 工具 |
| 5 | Make 蓝图参数规范与备份纪律（合并增量） | 工具 |
| 6 | Pipedream 代码步与 MCP 接入 | 工具 |
| 7 | Anthropic Skills API 与触发调优（合并增量） | 可复用 Skill |
| 8 | GitHub Search/Actions API 权限粒度 | 工具 |
| 9 | OpenClaw 四记忆文件与 Memory-Wiki（合并增量） | 工作流 |
| 10 | 技能市场分层与安装命令（合并增量） | 可复用 Skill |

## 复核
十独点均有当日实拉来源；4 新面 + 6 合并保留增量（增量均≥40%），零纯重复。版本建议 3.73.0。