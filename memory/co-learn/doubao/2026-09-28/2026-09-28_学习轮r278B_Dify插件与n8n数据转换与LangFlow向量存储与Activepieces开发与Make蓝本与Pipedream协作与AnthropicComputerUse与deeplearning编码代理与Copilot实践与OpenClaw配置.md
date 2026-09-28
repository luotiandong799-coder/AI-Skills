# r278B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表+r278A 错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（插件系统） | OK | 插件类型 Tool/Model/Endpoint（Extension）；Tool Provider 凭证校验（ToolProviderCredentialValidationError）；Endpoint=在 Dify 内跑 HTTP server（serverless 灵活性、OpenAI-compatible 格式、反向工具调用 Agent 插件化）；第三方插件=JSON 文件 URL 加载；插件开发限制（不用 open()/read()/write() 直接文件操作、用 memory 变量或 KV 存储 API） |
| 2 | n8n（数据转换） | OK | Item Lists 节点 1.21.0 移除→拆成 Aggregate/Limit/Remove Duplicates/Sort/Split Out/Summarize；Aggregate=多 item→单（n→1），模式 Individual Fields/All Item Data；Code 节点 Run Once For All Items（$input.all()）做全局过滤/排序/去重/聚合；Split Out 反向；Merge Append 合并两流；聚合数组（Operation Aggregate Items/Output Format Array/Field Name） |
| 3 | LangFlow（向量存储/记忆） | OK | Memory Base=长期聊天历史向量化存储、语义检索（按相似度返回相关上下文，区别于 Message History 按时序）；Knowledge Base=向量库存 embeddings（默认 Chroma 本地，可配 Chroma Cloud/OpenSearch/PGVector）；Load Data subflow（文件→chunk→embedding→索引）与 Retriever subflow 分离（不必每次运行加载数据）；Embedding 组件连 Vector Store |
| 4 | Activepieces（自定义 piece） | OK | TypeScript SDK（定义 triggers/actions/auth）；Piece Type=custom/community；AP_DEV_PIECES 环境变量本地开发（dist 文件夹加载、7 秒内浏览器见变化）；PieceAuth.CustomAuth/SecretText；CLI（npm run cli triggers create）；多语言 WebAssembly 执行扩展方向；本地开发从 dist 加载非数据库 |
| 5 | Make（蓝本/模板） | OK | Scenario blueprint=可复用版本（模块设置映射值），导出/导入备份/分享；Team templates（含公司设置/API keys/权限）vs Public templates（社区分享）；Scenario sharing=链接分享实时最新版、观众无需登录；拖放导入；blueprint 是 Make 的版本控制原语（export/import） |
| 6 | Pipedream（协作/权限） | OK | Workspace 三角色 Owner/Admin/Member；Projects access controls（Business 计划限制到个人、项目级环境变量）；Connected accounts 访问管理（workspace 或 individual）；工作流分享不分享 connected accounts（复制后显示插槽让用户连自己的账号）；GitHub Sync 部署阻断（无法验证合并人有账号权限时 block deploy）；Publish as template |
| 7 | Anthropic（Computer Use） | OK | computer_toolset_20260801 客户端工具集（17 个成员工具：screenshot/mouse/keyboard）；工作循环=截图 PNG→视觉语言模型解释布局→坐标点击/输入/按键/滚动→执行→新截图继续；可加 bash/text editor 增强；模型范围（Sonnet 4.5/Haiku 4.5/Opus 4.1）；vision 能力（图片理解） |
| 8 | deeplearning（函数调用/编码代理） | OK | Functions Tools and Agents with LangChain（LCEL 做 tagging/extraction/tool selection/routing、函数调用结构化输出）；Building Coding Agents with Tool Execution（执行环境比较=本地/容器/sandboxed microVM、E2B 云环境内置隔离+资源控制）；Building Code Agents with smolagents（code agents 写代码执行 vs 传统 tool-calling）；关键教训=agent=LLM+tools in a loop（for 循环处理多并发 tool calls、while 循环持续到完成） |
| 9 | GitHub Copilot（编码代理） | OK | issue 范围清晰（问题描述+完整验收标准+指定文件）；copilot-setup-steps.yml 可靠 setup（build/test 自信、flaky tests 让 agent 挣扎）；.github/instructions/ 文件提供模式约定上下文；skills 给重复任务；Secure Sandboxes（2026-06-02 公测、MXC 本地沙箱限制文件系统/网络）；自定义 agents（团队约定）；SKILL.md<500 行+references/ 分离（微软规范） |
| 10 | OpenClaw（配置体系） | OK | gateway 配置（auth token UUID、port 18789、controlUi）；models providers 配置（mode merge、自定义 provider baseUrl/apiKey/api openai-completions/authHeader/headers/models 列表）；agent 配置（from/gateway/policy/providers/autoProviders/timeoutSeconds）；provider 选择（Anthropic/OpenAI/Gemini/OpenRouter/Ollama 本地）；模型厂商云端 agent（Kimi Claw 预配 K2.5 模型）；OPENCLAW_GATEWAY_URL sandbox dialback |

## 判重（双键检索，增量判定）
- Dify 插件（r278A 插件面？不，r278A 是 Dify 混合检索）→ 新面（插件系统 Tool/Endpoint）
- n8n 数据转换（r277C JSONata/r276B 并行分支）→ 新面（聚合/拆分节点）
- LangFlow 向量存储（r277C output parser）→ 新面（memory base/vector store）
- Activepieces 自定义 piece（r277A Pieces 治理）→ 增量=TypeScript SDK+AP_DEV_PIECES 开发流程
- Make 蓝本（r276A modules/r277B HTTP）→ 新面（模板/分享）
- Pipedream 协作（r277C 定价）→ 新面（角色/权限/分享）
- Anthropic Computer Use（r277C OpenClaw browser automation 不同）→ 新面（工具集 API）
- deeplearning 函数调用（r277C MCP 课程/r277A prompt 工程）→ 新面（LCEL/编码代理课程）
- GitHub Copilot（r277B Actions 复用）→ 新面（编码代理实践）
- OpenClaw 配置（r278A 安装）→ 增量=gateway/models/agent 配置细节

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 插件系统（Tool/Endpoint） | 工具 |
| 2 | n8n 数据转换与聚合 | 工具 |
| 3 | LangFlow 向量存储与记忆 | 工具 |
| 4 | Activepieces 自定义 piece 开发 | 可复用 Skill |
| 5 | Make 蓝本与模板体系 | 工具 |
| 6 | Pipedream 协作与权限 | 工具 |
| 7 | Anthropic Computer Use | 工具 |
| 8 | deeplearning 函数调用与编码代理课程 | 可复用 Skill |
| 9 | GitHub Copilot 编码代理最佳实践 | 可复用 Skill |
| 10 | OpenClaw 配置体系 | 工具 |

## 复核
十独点均有当日实拉来源；均增量合并或新面；无并入未落地项。版本建议 3.51.0+。