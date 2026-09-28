# r284A 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r283 三十词 + 更早全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（版本控制） | OK | **每个工作流可导出为 DSL YAML → Git 版本控制、diff 部署差异、CI/CD 管道发布**；代码修复尝试每次创建新版本（Version 1/2…下拉选择）；应用生命周期五阶段：Build & Configure / Debug & Test / Publish / Monitor / Update（版本控制+回滚）；DSL 可导入其他 Dify 实例；**坑：Admin API 总是创建新 app 不能覆盖现有（publish 两次=两个 app）；completed-with-warnings 通常=DSL version 比目标旧**；2026 更新：条件分支复杂逻辑运算符 AND/OR/NOT、循环并行、错误重试策略、批量处理（多输入同时跑+进度跟踪） |
| 2 | n8n（表达式/数据映射） | OK | **{{ }} 双花括号动态引用；$json（当前 item）/ $node["Name"]（具名节点）/ $input.item/all()/first()/last() / $binary（二进制数据）**；**JMESPath（$jmespath()）查复杂嵌套 JSON**；访问记号三分：点记号（已知结构）/ 括号记号（特殊字符字段）/ 可选链（$json.user?.address?.city ?? 默认）；Luxon 处理日期；表达式运行时求值；数据映射=拖放或手写表达式 |
| 3 | LangFlow（记忆组件） | OK | **chat memory 与 vector store memory 是两类：chat memory 专为存/取聊天消息设计（agent 回忆上下文）；vector store 面向文本块语义搜索**；**Memory bases（1.10）：per-flow vector stores 自动摄入对话消息、跨 session 持久（区别于 session-scoped memory）**；Redis/Valkey vector store 组件（连接串/index 名/自定义 code）；Redis Chat Memory + Message History 组件（Store 模式 + Controls→External Memory）；DB Providers 配置后端（Chroma/Chroma Cloud/OpenSearch/pgvector）；**坑：Redis 缓存 DB 0 与 job queue DB 1 不能混用（LANGFLOW_REDIS_QUEUE_DB）** |
| 4 | Activepieces（映射/分支/循环） | OK | **Router/Branch 输出结构：router.output.branches 数组（branchIndex/branchName/evaluation 条件结果）**；LOOP 动作（items+loopActions）；BRANCH 动作（conditions 数组 firstValue 等）；**loop 与 branch 可互相嵌套（loop 内 router、router 内 loop）**；Router/loop executor（顺序或并行迭代）；MCP tools（ap_add_branch 在 fallback Otherwise 前插分支）；**JavaScript steps 做字段清洗/类型转换/规范化/记录重塑：上游 payload 映射成一致 schema 再写 API/DB**；专家提示：第一个分支条件保持简单、先单独测两条路径再加复杂度 |
| 5 | Make（Data Store/变量） | OK | **Data Stores=Make 内建持久化存储；scenarios 默认无状态，Data Store 给跨 run 记忆（toy automation vs production infrastructure 的分界）**；key-value 结构（防重用 key=已处理 ID 存 timestamp；计数 key=counter；lookup key=查询键）；字段=name+type（Text/Number/Boolean）；场景变量（单 run 临时数据，set/get variable 工具）；自定义变量（组织/团队级 Pro+，跨场景共享）；Data Store 用例：重复处理防重、每日计数累计、AI 结果缓存；data store 在账户内多 scenario 共享 |
| 6 | Pipedream（components/代码步骤） | OK | **Actions=可复用代码步骤（封装连接逻辑/错误处理，用户只填参数）**；**components 系统只支持 Node.js；Python 只作 code step 语言（复用=复制粘贴到另一 workflow）**；components 三特性：props 接受输入、return JSON 可序列化数据、可发布到注册表；**component API：deploy()/activate() hooks + 部署生成组件 ID**；source 开发用 $.service.db（get/set 持久化）；代码/action 步骤不能在 trigger 前；action 定义（name/key/version/type/props/run） |
| 7 | Claude（MCP 配置） | OK | **claude mcp add 命令（--transport http sentry https://mcp.sentry.dev/mcp）；claude mcp list 显示认证状态（! Needs authentication）**；**Anthropic Directory（claude.ai/directory）已审查连接器，与 Claude Code 同一 MCP 基础设施，远程服务器可直接 claude mcp add**；mcp add-json 传 mcpServers 内部对象（url 无 command 的条目需先修复）；**插件 marketplace：/plugin marketplace add anthropics/claude-plugins-official + /plugin install mcp-server-dev@claude-plugins-official**；marketplace.json 目录文件（git repo 或 HTTPS 托管、pin revision）；.mcp.json 插件根配置（command/args/env，${CLAUDE_PLUGIN_ROOT} 变量） |
| 8 | GitHub（Agentic Workflows） | OK | **GitHub Agentic Workflows（2026-02 技术预览、06-11 公开预览）：Markdown 自然语言定义自动化 → 编译成标准 Actions YAML（.lock.yml）→ 在 GitHub Actions 跑 coding agent（Copilot/Claude Code/Gemini/OpenAI Codex）**；用途：issue triage/CI 失败分析/文档更新/PR review；guardrails=sandboxing+permissions+control+review；**Docker Sandboxes（2026-07）：agent 在 microVM 隔离 + 网络策略 + secrets 注入**；**safe-outputs handler 护栏模板：title 前缀 [docs]、label、draft: true（从不自动合并）、base branch 限 main/release/*、reviewer 指定**；.github/workflows/ 放 Markdown 文件、gh aw CLI 编译；Claude Code Action v1 GA（输入面改名，旧 @beta 片段已过时） |
| 9 | OpenClaw（记忆） | OK | **记忆=agent workspace 里的普通 Markdown 文件（~/.openclaw/workspace）；模型只记得保存到磁盘的内容（无隐藏状态）**；**每日日志 memory/YYYY-MM-DD.md（append-only，会话开始读今日）+ MEMORY.md（精炼长期记忆，会话开始加载）**；memory-wiki 技能维护知识库；**三态记忆：short-term context（RAM 易失）/ long-term structured（SQLite/JSON 持久可查）/ semantic memory（向量数据库语义检索）**；RAG 无限上下文（Pinecone/Milvus 摄入+检索）；**LCM Lossless Context Management：决定保全文/压缩/归档** |
| 10 | agentskills.io（生态） | OK | **skills.sh 7 个月达 100 万 skills、近 2.8 亿 installs（Vercel 2026-09-25）**；**AgentSkills.io spec=事实上的跨平台标准（Anthropic 2025-10 发起，Google/Microsoft/独立工具采纳）**；SkillsMP 索引约 190 万公共 skills（GitHub 爬取）；2026-03 跨过"严肃基础设施"门槛（87K+ stars、13,700+ 社区 skills、30+ 平台采用）；**安全是最大风险：审计 skills 26% 含漏洞、12% 恶意（跨注册中心）；Snyk ToxicSkills 13.4% 关键问题**；skills.sh 分类（Development & Engineering 288,811 / Product Management 86,948 / Marketing 74,510 / Data & Analytics 69,187 / Operations 51,007）；8 个竞争注册中心（2025-12 1 个→2026 Q2 8 个）；2,500+ Claude Code plugin marketplaces；Google Gemini API skills 官方评测 87-96% 准确率提升；安全优先目录兴起 |

## 判重（双键检索，增量判定）
- Dify DSL 版本控制（r283A 错误处理/r283B 索引）→ YAML→Git CI/CD+Admin API 坑为新面 → **新面**
- n8n 表达式（r283A 可观测/r283B Merge）→ $json/$node/$input+JMESPath+可选链为新面 → **新面**
- LangFlow 记忆（r283C 输入类型/r272B 记忆组件）→ chat vs vector memory+Memory bases+DB 隔离为新面 → **新面**
- Activepieces 分支循环（r283B waitpoint/r283C 定时）→ router 输出结构+嵌套+JS 步骤 schema 化为新面 → **新面**
- Make Data Store（r283B 目录治理/r283C webhook）→ 无状态 vs 持久化+key-value 用例为新面 → **新面**
- Pipedream components（r283A 部署不可变/r283C 并发）→ actions 三特性+deploy hooks+$.service.db 为新面 → **新面**
- Claude MCP 配置（r282C MCP 选型/r283A 动态工作流）→ add/list 命令+Directory+marketplace 为新面 → **新面**
- GitHub Agentic Workflows（r283A GitHub 事件/r283C Copilot 指令）→ Markdown→Actions+safe-outputs 护栏为新面 → **新面**
- OpenClaw 记忆（r283B 身份/r283C 渠道）→ Markdown 文件记忆+三态+LCM 为新面 → **新面**
- Agent Skills 生态安全（r283C 课程信号/r272A 生态）→ 100 万 skills+12% 恶意+8 市场为新面 → **新面**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify DSL 版本控制与 CI/CD | 工作流 |
| 2 | n8n 表达式访问体系 | 工具 |
| 3 | LangFlow 记忆分类与 Memory bases | 工具 |
| 4 | Activepieces 分支循环嵌套与 Router 输出 | 工作流 |
| 5 | Make Data Store 持久化 | 工具 |
| 6 | Pipedream components 复用系统 | 工具 |
| 7 | Claude MCP 配置命令生态 | 工具 |
| 8 | GitHub Agentic Workflows | 工作流 |
| 9 | OpenClaw Markdown 记忆架构 | 工具 |
| 10 | Agent Skills 生态与安全 | 工作流 |

## 复核
十独点均有当日实拉来源；全部新面（零增量合并、零纯重复）。版本建议 3.68.0。