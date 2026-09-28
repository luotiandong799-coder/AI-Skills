# r284C 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r284A/B + 更早全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（工作流节点） | OK | **HTTP Request 节点：所有标准方法（GET 取数据/HEAD/POST/PUT/DELETE/PATCH）、模板变量替换、灵活认证、SSRF 保护、超时管理、动态请求体序列化**；**Code 节点：Python/JS 自定义代码、沙箱环境、沙箱内不能做外部网络调用——需要网络用 HTTP Request 节点**；**Iteration 节点：数组输入→对每元素跑子工作流（顺序或并行），当前 item 和 index 作为变量（批量处理）；Loop 节点：满足结束条件前重复、各周期基于上次结果**；敏感 API key 存 Dify 环境变量不硬编码节点配置 |
| 2 | n8n（AI Agent） | OK | **AI 节点实现 LangChain JS 框架；AI Agent root node=有界执行环境，子节点=LLM/记忆/工具/检索**；**三种 agent：Tools Agent（工具调用接口+标准输出格式）/ Conversational Agent（系统 prompt 描述工具+解析 JSON tool calls，chatbot，memory 不跨会话持久）/ ReAct Agent（CoT+行动计划循环，不支持 memory 子节点）**；**记忆子节点：Simple Memory（Window Buffer 存最近 N 条）/ Postgres Chat Memory / Redis Chat Memory / MongoDB Chat Memory**；Session Key 表达式（user 特定会话）；manager agent with sub-agent tools（记忆接 ai_memory 输入） |
| 3 | LangFlow（自定义组件） | OK | **自定义组件=继承 Component 类的 Python 类：类级属性（display_name/description/icon）、输入输出列表、方法定义行为逻辑、内部变量错误处理与日志**；**agent 可用自定义组件作为工具（New Custom Component）**；**bundle=相关组件分组（服务提供商相关，lfx components 文件夹）；extension：lfx extension init my-extension（extension.json manifest + pyproject.toml + src）**；**Langflow Assistant（1.10.0）：提示词生成自定义组件代码（"Create a custom component URLTitleExtractor with input/output/timeout handling/clean docstring"）** |
| 4 | Activepieces（轮询/测试） | OK | **Polling 触发器：周期调用端点查变化（推荐限制为五个），示例 Airtable New Record/Salesforce New Updated Item**；**sampleData=静态测试样本数据（title/link/pubDate/content）**；**测试纪律：每个步骤添加前必须先测试（Test me），保证能访问上一步数据（避免选错数据/发布后破坏流程）**；**触发器测试差异：polling 可 Test flow/load sample data；webhook 不能 Test Flow（用静态 sample data），须发布 flow 后执行真实事件再查 dashboard 运行**；token 放 Connections/Secret 不写进公开 Flow；webhook 本地开发须暴露到公网 |
| 5 | Make（迭代/聚合） | OK | **Iterator=特殊模块把数组拆成 series of bundles（每个数组项一个 bundle 逐个处理：5 附件逐个处理）**；**Aggregator=把多个 bundle 累加成单个 bundle（Array aggregator/Text aggregator：构建 JSON/CSV/HTML）**；**每个 iterator/list/search 模块必须配对一个 aggregator（迭代范围闭合）**；**嵌套迭代坑：row → 再 iterate images 后 aggregator 失去 row-level 边界（rowId 分组不工作）；Array aggregator 不闭合迭代范围 → 后模块每迭代跑一次而非一次**；组合：Array Aggregator 后接 Text Aggregator 产出长字符串 |
| 6 | Pipedream（触发器） | OK | **触发器类型：App triggers（Twitter/GitHub 等）/ HTTP / Webhook / Schedule / Email / RSS**；**Schedule 触发器：intervalSeconds（秒频率）或 cron 对象（自定义 cron + timezone，如 "cron": "0 8 * * 1-5"）**；**HTTP/Webhook trigger=生成唯一 URL，部署后每个请求跑一次 workflow**；**要指定星期几必须用 cron 而非 simple interval**；HTTP 请求 action=Postman 式图形界面（query string/headers/basic auth）；Source 开发（db.get/db.set 状态、this.http.respond、this.$emit） |
| 7 | skills.sh | OK | **Vercel 的 agent skills 中心目录；安装 CLI：npx skills add owner/repo（例 vercel-labs/agent-skills），免全局安装（npx）**；**CLI 自动搜索仓库已知目录（skills/、.agents/skills/、.claude/skills/）+ manifest（.claude-plugin/marketplace.json）零配置发现安装**；npx skills find（搜索）；**API：installs（去重安装数）、sourceType（github/well-known）、installUrl、isDuplicate（检测 fork/拷贝）——目录级重复检测**；VS Code 扩展；find-skills 技能（自然语言"find a skill for X"→CLI 搜索验证安装） |
| 8 | GitHub（MCP server） | OK | **官方 GitHub MCP server（远程托管 + 本地 Docker 部署两种）；remote URL https://api.githubcopilot.com/mcp/**；**工具面：context（当前用户与 GitHub 上下文，强烈推荐）/ actions（Actions workflows/CI/CD）/ code_security（Code Scanning）/ copilot / dependabot / discussions / gists**；与 Copilot SDK/Declarative Agent（Microsoft 365）/Agent Framework/AWS Bedrock 集成；Copilot coding agent 支持 MCP servers（Playwright/Sentry/Notion） |
| 9 | OpenClaw（自动化） | OK | **cron 配置：enabled/store jobs.json/maxConcurrentRuns/retry maxAttempts 3；Wakeups=一等公民（"wake now" vs "next heartbeat"）**；**webhook：hooks enabled+token（shared-secret）+path /hooks；认证 Authorization: Bearer token 或 x-openclaw-* 头；cron 每 job 支持 delivery.mode="webhook" + delivery.to="url"**；**Heartbeat（~30 分钟间隔 HEARTBEAT.md）——三种自动化：Cron（精确排期）/ Heartbeat（定期检查）/ Webhook（外部事件触发）**；cron CLI 命令（--command/--command-cwd/--command-env/--command-input/--timeout-seconds/--no-output-timeout-seconds/--output-max-bytes/--webhook）；curl webhook 示例（POST /hooks/agent + Bearer + message/name/channel/to/deliver） |
| 10 | Hugging Face（smolagents） | OK | **CodeAgent=主要 agent 类型（生成 Python 代码执行动作而非 JSON/文本）；ToolCallingAgent=JSON-based tool calls（不需要代码执行）**；**模型无关：本地 transformers/Ollama、HF inference providers、OpenAI/Anthropic/Azure/Bedrock、100+ LLMs via LiteLLM；工具无关：MCP servers/LangChain/HF Hub Space 的工具**；**@tool 装饰器定义 agent 可调用函数；Tool 基类（name/description/inputs 字典/output_type）**；**沙箱代码执行：Blaxel/E2B/Modal/Docker**；内置工具：visit_webpage（抓网页转 markdown）/wikipedia_search/transcriber（Whisper 语音转文字）/final_answer/user_input；**通过 HF Hub 分享与加载工具和 agents**；agent 逻辑~1000 行代码；webagent CLI（vision-based 浏览器控制，VLM 截图解释） |

## 判重（双键检索，增量判定）
- Dify 节点（r284B 检索策略）→ HTTP/Code 沙箱分离+Iteration 数组批处理为新面 → **新面**
- n8n AI Agent（r284B 错误处理）→ 三型 agent+记忆子节点（Postgres/Redis/Mongo）为新面 → **新面**
- LangFlow 自定义组件（r284B 多 Agent）→ Component 类结构+bundle/extension+Assistant 生成代码为新面 → **新面**
- Activepieces 测试（r284B 触发器）→ 测试纪律（Test me）+sampleData+webhook 测试差异为新面 → **新面**
- Make 迭代聚合（r284B Router）→ iterator/aggregator 配对+嵌套迭代坑为新面 → **新面**
- Pipedream 触发器（r284B 重放）→ 触发器类型清单+cron 对象+HTTP trigger 为新面 → **新面**
- skills.sh（r284A Agent Skills 生态）→ 目录 API+CLI 发现机制+isDuplicate 为新面 → **新面**
- GitHub MCP（r284A Claude MCP 配置）→ 官方 server 工具面+远程 URL 为新面 → **新面**
- OpenClaw 自动化（r284B 插件）→ cron/webhook/heartbeat 三件套+delivery.mode 为新面 → **新面**
- smolagents（r284B 提示工程）→ CodeAgent 代码动作+沙箱+HF Hub 分享为新面 → **新面**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 节点沙箱分离与 Iteration 批处理 | 工具 |
| 2 | n8n AI Agent 三型与记忆子节点 | 工作流 |
| 3 | LangFlow 自定义组件与 bundle/extension | 工具 |
| 4 | Activepieces 测试纪律与 sampleData | 工作流 |
| 5 | Make Iterator/Aggregator 配对与嵌套坑 | 工具 |
| 6 | Pipedream 触发器类型与 cron 对象 | 工具 |
| 7 | skills.sh 目录与 CLI 发现机制 | 可复用 Skill |
| 8 | GitHub MCP 官方 server | 工具 |
| 9 | OpenClaw 自动化三件套 | 工作流 |
| 10 | smolagents CodeAgent 与工具生态 | 工具 |

## 复核
十独点均有当日实拉来源；全部新面（零增量合并、零纯重复）。版本建议 3.69.0。