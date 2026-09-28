# r287B 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r287A/r284-r286 错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（Knowledge Base/RAG） | OK | **Summary Index（1.12.0）：给每个 chunk 附 summary 字段，语义相关内容一起检索——GraphRAG 的轻量替代（不用建实体关系图）**；**Knowledge Retrieval 节点两级过滤：KB 设置定初始池 + 节点设置 rerank/缩小池（两个连续过滤器）**；**Rerank 设置：Weighted Score（semantic vs keyword 相对权重，仅 High Quality 模式可用）+ Rerank Model**；**多模态检索：Embedding 一轮快速相似匹配 + Reranking 评估 query/text/image 具体相关性**；**RAG 精度配置：test chunking against source structure、clean source（去重复页眉页脚页码导航）、metadata filtering（tag 文档 "product: billing"）**；**chunk size：200-500 tokens 事实问答 / 500-1000 摘要；chunk overlap 10-20% 最优**；**多 KB 应用必须配置 retrieval mode（Rerank Setting）**；模型避坑：腾讯混元/部分 DeepSeek 无可用 Rerank、OpenAI 只有 Embedding 无 Rerank |
| 2 | n8n（Expressions/AI 功能） | OK | **$fromAI(key, description?, type?, defaultValue?)：LLM 提供节点参数值——key 只含字母数字下划线连字符，提供 description 结果更好**；**表达式五模式：Basic {{ $json.field }} / Nested {{ $json.user.email }} / Array {{ $json.items[0] }} / Node reference {{ $node["Name"].json.id }}（节点名要引号、大小写敏感、精确匹配）/ Method call {{ $json.name.toLowerCase() }}**；**AI coding help：引用 incoming node data 用 dot notation 帮 AI 理解（personal_info.first_name）**；**$jmespath 旧语法升级：$jmespath($json.body.meta_data, "[?key == 'xxx'].value")[0] 改用 .find()** |
| 3 | LangFlow（部署/生产） | OK | **Runtime（production）：headless（backend only）服务只服务 Langflow API——生产 flows 程序化执行不需要 visual editor**；**最小要求 2Gi RAM + 1000m CPU/实例、3 replicas；HPA 按 CPU 动态扩缩**；**v1.9-v1.10 内存优化 ~89% 减少（dependency pruning + worker lifecycle management + Linux CoW）**；**Langflow 1.9 Flow DevOps Toolkit SDK：lfx init 创建 scaffold、environments.yaml 控制部署——版本化/测试/部署 flows 从终端**；**NextPlaid（1.11.0）：ColBERT retrieval 作为 Rust service（PLAID index server，REST API over Axum + MmapIndex + SQLite metadata）——多向量检索**；**生产特性：LangSmith/LangFuse observability、API key RBAC 认证**；部署形态：Desktop/Docker/K8s/Cloud/API Export |
| 4 | Activepieces（Webhook/Triggers） | OK | **触发器三形态：Polling（定期轮询）/ Webhooks（单 URL 监听）/ App Webhooks (Subscriptions)（OAuth2 developer app 单 URL 收授权事件）**；**Webhook Trigger 生命周期：On Enable 用 context.webhookUrl 注册第三方 webhook 并存 webhook ID 到 context.store；On Handshake 处理 challenge；Disable 用 store 取 ID 删除**；**Webhook 同时是 trigger 和 action**；**App Webhooks 局限：Slack/Square 每个 OAuth2 app 只支持一个 webhook，需 developer portal 手动配置**；**Event Streaming：平台 audit events 转发到 webhook URL（flow run failures/新登录/项目发布）→ flow 路由到 Slack/Gmail/Teams** |
| 5 | Make（Data Store/迭代/聚合） | OK | **Reliable fan-out then fan-in 四步：Iterate（拆 per-item bundles）→ Validate early（迭代后立即丢弃/隔离无效项避免浪费）→ Transform（归一化：currency/SKU/category mapping）→ Aggregate（构建单一下游 payload 一次 API 调用）**；**操作注意：iteration 成倍放大下游模块运行——文档化期望数组大小、应用 limits**；**经典模式：HTTP Webhook 收数组 → Iterator → Router（按 total 路由 premium/standard 表）→ Aggregator → HTTP Response 返回 summary JSON**；语义缓存路由：embedding + Redis，相似阈值内命中缓存、miss 路由到最便宜达标模型（40-60% 减少） |
| 6 | Pipedream（Code Step/Components） | OK | **组件两类型：sources（必须实例化、独立资源运行、常用作 workflow trigger、也可独立 serverless 函数）/ actions（workflow 步骤，不能独立运行）**；**组件生命周期 hooks：activate()/deactivate()——update 时先 invoke deactivate → 更新代码 props → 再 activate，组件 ID 不变**；**actions 是预建 code steps（连接管理/错误处理封装，只需指定参数）**；**components 源码在公共 GitHub repo，社区维护**；**AI code generation：prompt → 流式生成 → connected accounts/props 自动刷新**；Node.js defineComponent({ async run({steps, $}) }) / Python def handler(pd) |
| 7 | Anthropic（Managed Agents/API） | OK | **Claude Managed Agents（2026-04 推出）：创建 Agent 配置（模型、system prompt、工具、MCP servers、Skills）→ 通过 API 启动 Session → Anthropic 托管沙箱——"Agent 作为服务"（接口之上最大产品化跃迁）**；**version 字段 optional：更新 Managed Agents 提供=optimistic concurrency（mismatch 返回 409），省略=无条件应用**；**session thread event streams 支持 event deltas（GET /v1/sessions/{session_id}/threads/{thread_id}/stream）**；**Python SDK v1.0：移除 Text Completions API legacy 与 temperature/top_p、要求 Python 3.10+**；**Opus 5：1M-token context window（Anthropic API 与 Max/Team/Enterprise；Bedrock/GCP 选 1M variant）**；improve_prompt/templatize_prompt 端点 2026-08-17 停用 |
| 8 | GitHub（Copilot Code Review） | OK | **gh pr create --reviewer @copilot 创建 PR 时请求 Copilot 审查；已有 PR 用 gh pr edit**；**Copilot code review 支持 agent skills 和 MCP servers（2026-06 public preview → 2026-07-29 GA，全订阅）：SKILL.md 带进 review 让 Copilot 调团队内部工具和 coding standards**；**effort levels（Lite/Balanced GA 2026-08-07）：按 PR 复杂度风险匹配审查深度——文档更新/小修复用 Lite，复杂逻辑/安全敏感/跨服务变更用 Balanced（medium analysis tier 复杂 PR 路由高推理模型）**；**auto-resolution（2026-09-11）**；**计费：2026-06-01 起消耗 GitHub Actions minutes** |
| 9 | OpenClaw（Memory/Tasks） | OK | **memory 非信任内容只作证据，等 trusted reviewer 确认前不存为 durable memory**；**action-sensitive boundaries：失去 timing/authority/expiry/safe-to-act 上下文会导致 agent 以后做错事时用这些边界**；**用 scheduled tasks 做精确提醒/定时检查/周期工作，memory 只总结持久上下文**；**session-memory hook：会话结束时自动触发 → 总结要点 → 追加当日日志 → 打时间戳和话题标签（openclaw.json 配置）**；**三文件：MEMORY.md（长期，每次会话开始加载）+ memory/YYYY-MM-DD.md（日志）+ archives/（旧日志）**；**ontology Skill：结构化持久记忆（people/projects/tasks 跨会话）——知识图谱化；regular context memory vs ontology（记什么和怎么查询的区别）** |
| 10 | WaytoAGI / DeepSeek 生态 | OK | **Deepseek 推理模型 vs 通用模型：推理型无需用户提供详细步骤指令，理解真实需求直接给答案；更懂"人话"；深度思考**；**DeepSeek V4 for Copilot Chat：VS Code 插件把 V4 Pro/Flash 加进 Copilot 模型选择器，仍可用 Copilot Agent 模式/工具调用/Skills/MCP**；**DeepSeek TUI：/skills 列出 /skill <name> 激活 /skill new scaffold /skill install github:<owner>/<repo> /skill update——TUI 也有技能系统**；**DeepSeek Harness（dsh）：2026-08-13 发布 MIT 协议 Agent 框架，"一切皆插件"；colleague-skill 把同事聊天记录蒸馏为 AI Skill；OpenBiliClaw 反算法推荐** |

## 判重（双键检索，增量判定）
- Dify Summary Index/RAG（r286B 已落"RAG 评估四指标 + Summary Index"）→ 重叠约 65%，增量=两级过滤（KB 定池+节点 rerank）/Weighted Score/多模态检索/chunk 参数（200-500/500-1000、overlap 10-20%）/metadata 标签（≥40%） → **合并保留增量**
- n8n 表达式（r286B 已落"表达式三选与 AI 代码生成"）→ 重叠约 60%，增量=$fromAI 参数契约/表达式五模式/node 名引号与大小写/$jmespath 旧语法迁移（≥40%） → **合并保留增量**
- LangFlow 部署（r286B 已落"headless runtime/worker/Redis 队列"）→ 重叠约 70%，增量=lfx init/environments.yaml/内存优化 89%（dependency pruning+CoW）/NextPlaid ColBERT Rust/生产 observability（≥40%） → **合并保留增量**
- Activepieces 触发器（r286B 已落"触发器三技术 + 数据脱敏"）→ Webhook 生命周期（On Enable 注册+store 存 ID/Handshake challenge/Disable 删除）/Event Streaming 审计事件 → **新面**
- Make 迭代聚合（r285A 场景蓝图/Data Store、r286B 蓝图参数契约）→ 重叠约 60%，增量=fan-out then fan-in 四步（Validate early/Transform/Aggregate）/文档化数组大小/经典 Router 分桶模式（≥40%） → **合并保留增量**
- Pipedream 组件（r286B 已落"代码步 defineComponent"、r287A trace_id）→ 重叠约 60%，增量=sources vs actions/activate-deactivate 生命周期/actions 预建 code steps/AI code gen props 自动刷新（≥40%） → **合并保留增量**
- Anthropic Managed Agents（r286B 已落"API 版本化"）→ Managed Agents"Agent 作为服务"（配置/session/托管沙箱）/version 乐观并发 409/event deltas → **新面**
- GitHub Copilot Review（r286C 已落"Copilot 安全扫描三重"）→ 重叠约 65%，增量=gh pr create --reviewer @copilot/effort levels Lite-Balanced/agent skills+MCP 进 review（SKILL.md 带进）/计费 Actions minutes（≥40%） → **合并保留增量**
- OpenClaw memory（r285C 记忆持久化、r286B 四记忆文件）→ 重叠约 65%，增量=非信任内容只作证据待确认/action-sensitive boundaries/session-memory hook 自动总结打标签/ontology Skill 结构化图谱（≥40%） → **合并保留增量**
- DeepSeek 生态（r286C 已落"Harness 生态 + ModLens"）→ 重叠约 70%，增量=DeepSeek V4 for Copilot Chat 插件（模型选择器加 V4、保留 Agent/Skills/MCP）/DeepSeek TUI /skills 命令族/colleague-skill 蒸馏聊天（≥40%） → **合并保留增量**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify RAG 两级过滤与 chunk 参数（合并增量） | 工作流 |
| 2 | n8n $fromAI 与表达式五模式（合并增量） | 工具 |
| 3 | LangFlow DevOps Toolkit 与内存优化（合并增量） | 工具 |
| 4 | Activepieces Webhook 生命周期与 Event Streaming | 工具 |
| 5 | Make fan-out then fan-in 四步（合并增量） | 工作流 |
| 6 | Pipedream 组件两类型与生命周期（合并增量） | 工具 |
| 7 | Anthropic Managed Agents 服务化 | 工作流 |
| 8 | Copilot Code Review 技能化与 effort levels（合并增量） | 工作流 |
| 9 | OpenClaw 记忆信任边界与 session hook（合并增量） | 工具 |
| 10 | DeepSeek Copilot 插件与 TUI 技能系统（合并增量） | 工具 |

## 复核
十独点均有当日实拉来源；2 新面 + 8 合并保留增量（增量均≥40%），零纯重复。版本建议 3.73.0。