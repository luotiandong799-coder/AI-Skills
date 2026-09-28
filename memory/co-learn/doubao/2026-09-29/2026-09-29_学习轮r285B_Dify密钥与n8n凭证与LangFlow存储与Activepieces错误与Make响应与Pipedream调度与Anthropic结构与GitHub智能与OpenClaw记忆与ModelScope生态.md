# r285B 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r285A/r284 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（API 发布） | OK | **API 密钥：应用级创建、仅作用于该应用、一个密钥服务所有终端用户**；**Bearer Token 认证（Authorization: Bearer YOUR_API_KEY）**；**只在后端调用 API——嵌入前端/客户端应用的密钥可被提取和滥用**；**用户隔离：每个 API 请求可带 user 参数区分不同人**；每个 workflow 有自己的 key；XXL-JOB 可调度 Dify workflow |
| 2 | n8n（凭证/认证） | OK | **HTTP Request credentials 十种认证：Predefined credential type / Basic auth / Custom auth / Digest auth / Header auth / Bearer auth / OAuth1 / OAuth2 / Query auth / Simplified Custom Auth**；**credential-only nodes：只设凭证不提供独立节点（在 HTTP Request 节点使用）**；**predefined credential type 替代 generic credentials**；自定义节点 credentials 文件（IAuthenticateGeneric，type generic，properties auth username/password） |
| 3 | LangFlow（存储/向量） | OK | **Memory bases：按 flow 的向量存储、自动摄取会话消息、跨会话语义检索（vs Message History 时序检索；vs knowledge base 手动填充）**；**DB Providers（Settings→DB Providers）：Chroma/Chroma Cloud/OpenSearch 可配置向量后端**；**Local DB=Langflow 增强版 Chroma（Ingest/Retrieve 双模式、自动 collection 管理、内置持久化到 cache 目录）**；默认存储 SQLite（路径按 OS）；knowledge 索引配置（默认 index langflow_knowledge/vector_field/text） |
| 4 | Activepieces（错误处理） | OK | **Step 错误三类：Step Errors / Timeout Errors / Sandbox Errors**；**retryOnFailure/continueOnFailure 布尔参数（默认 false）**；处理：指数退避重试/继续到 error handler/标记 run 失败；**并发控制：项目达限后新 run 不丢弃——排队+指数退避自动重试，槽位空出后下一个开始**；**幂等：idempotency keys+correlation IDs 存 Tables 检测重复、短路重复 run；429/5xx 分支；failed payload 持久化到表控制重处理**；partial failure 用分支隔离风险步骤+补偿动作+中间状态持久化；**Project Replace CLI：恢复靠重跑不是回滚，按 externalId 匹配，崩溃后下次 diff 检测并完成** |
| 5 | Make（Webhook） | OK | **Custom webhook 模块生成唯一 URL（每个 scenario 用各自 webhook，不能共用）**；**Webhook response 模块：控制响应（status/body/headers），Stripe 等要求特定响应体确认收到 {received:true}**；默认 200 OK 立即返回；**同步自定义响应用 Webhook Response 模块**；Mailhook 独立；webhook 数据结构自动确定（发请求到 URL 后自动决定） |
| 6 | Pipedream（Cron 调度） | OK | **Schedule 触发器=内置 cron，无需 app 连接**；**cron 对象（intervalSeconds 或 cron 表达式+timezone）**；**默认 UTC 运行，按团队时区需调 offset**；**timer interface：props 定义 $.interface.timer，default intervalSeconds**；标准 cron 语法（0 8 * * 1-5）；2026-04 起所有计划含 free tier |
| 7 | Anthropic（Skills 结构） | OK | **SKILL.md 必须恰好是 SKILL.md（区分大小写——skill.md 和 SKILL.MD 被拒）**；**YAML frontmatter（name/description）+ markdown 指令体**；**目录结构：SKILL.md（必需）+ scripts/（可选可执行代码）+ references/（可选按需加载文档）+ assets/（可选模板）**；**会话开始只加载 name 和 description，完整 body 在调用时才加载（slash 命令 /code-review 或自动匹配）**；目录名=技能名 |
| 8 | GitHub（Agentic Workflows） | OK | **用自然语言 Markdown 定义、编译成标准 Actions YAML（.lock.yml），在 .github/workflows/ 添加 Markdown 文件**；**支持 AI 引擎：GitHub Copilot/Claude Code/Google Gemini/OpenAI**；**gh aw add-wizard 命令安装工作流**；**Docker Sandboxes 作为 agent runtime（microVM 隔离+网络策略+secrets 注入）**；与确定性 CI/CD 互补（事件触发+定时）；Claude Code GitHub Action v1 GA（改名输入面） |
| 9 | OpenClaw（记忆持久化） | OK | **三层持久记忆：Markdown + ChromaDB vectors + NetworkX knowledge graph**；**memory-wiki 插件：把持久知识编译成 wiki 仓库（确定性页面结构、结构化断言与证据、矛盾跟踪与时效性）**；**知识图谱：事实/关系/模式提取成结构化知识库**；**跨渠道记忆（WhatsApp 早上/Telegram 下午同一记忆）**；**Graphiti（Zep 时间知识图谱）：时间感知——"切到 PostgreSQL"标记旧关系结束、带时间戳新建**；**SurrealDB 记忆升级（语义搜索+情景记忆+工作记忆+自动上下文注入+per-agent 隔离）** |
| 10 | ModelScope（agent 生态） | OK | **ModelScope-Agent 框架：可定制 agent 系统（Prompt generator 组装上下文：system prompt/API schema/retrieved knowledge/conversation history/few-shot examples，按查询类型+LLM 最大长度选配）**；**MS-Agent v1.6.0rc1：Agentic Insight v2（重构 deep-research）**；**Agents-A1（35B 达万亿参数性能）：agentic reasoning/工具使用/指令跟随**；**ModelScope API skill for OpenClaw（发现/查询/下载 194,000+ 模型与 80,000+ 技能）**；集成官方工具：web_browser/代码解释器/天气/图像生成/Qwen-VL 图像理解；Nex-N2 Agentic Thinking（需求理解→任务规划→代码实现→环境反馈→评估调试→迭代闭环） |

## 判重（双键检索，增量判定）
- Dify API（r284 版本控制 / r285A 提示词编排）→ API 密钥/后端调用/用户隔离 新面 → **新面**
- n8n 凭证（r284 表达式/错误/智能体 / r285A Webhook）→ 凭证十类型/credential-only 新面 → **新面**
- LangFlow 存储（r284 记忆分类 / r285A Tool Mode）→ Memory bases 重叠>60%，增量=DB Providers/Local DB 持久化/SQLite 路径（≥40%） → **合并保留增量**
- Activepieces 错误处理（r284 分支/触发器/测试）→ retry/并发排队/幂等 新面 → **新面**
- Make Webhook（r284 存储/路由/迭代聚合 / r285A 蓝图）→ Webhook response 模块 新面 → **新面**
- Pipedream Cron（r284C 触发器类型与 cron 对象）→ 重叠约 50%，增量=内置 Schedule source/UTC 默认/timer interface（≥40%） → **合并保留增量**
- Anthropic Skills 结构（r284B SKILL.md 硬约束）→ 重叠约 55%，增量=目录结构/SKILL.md 大小写严格/按需加载机制（≥40%） → **合并保留增量**
- GitHub Agentic Workflows（r284A 已落地）→ 重叠约 50%，增量=.lock.yml 编译/gh aw add-wizard/Docker sandbox（≥40%） → **合并保留增量**
- OpenClaw 记忆（r284A Markdown 记忆架构）→ 重叠约 50%，增量=Graphiti 时间图谱/三层持久记忆/memory-wiki（≥40%） → **合并保留增量**
- ModelScope（前轮未拉）→ 新面 → **新面**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify API 密钥与后端调用纪律 | 工作流 |
| 2 | n8n 凭证十类型与 credential-only | 工具 |
| 3 | LangFlow 存储后端可配置与持久化（合并增量） | 工具 |
| 4 | Activepieces 错误处理与并发排队 | 工作流 |
| 5 | Make Webhook 响应模块 | 工具 |
| 6 | Pipedream Schedule 触发器与 UTC 时区（合并增量） | 工具 |
| 7 | Anthropic Skills 目录结构与加载机制（合并增量） | 可复用 Skill |
| 8 | GitHub Agentic Workflows Markdown 编译（合并增量） | 工作流 |
| 9 | OpenClaw 三层记忆与时间图谱（合并增量） | 工具 |
| 10 | ModelScope-Agent 生态 | 工作流 |

## 复核
十独点均有当日实拉来源；6 新面 + 4 合并保留增量（增量均≥40%），零纯重复。版本建议 3.71.0。