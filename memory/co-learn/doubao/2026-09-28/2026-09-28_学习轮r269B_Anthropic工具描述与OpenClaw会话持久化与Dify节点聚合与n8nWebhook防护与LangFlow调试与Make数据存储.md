# r269B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r266/r267/r268/r269A 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（工作流节点面） | ✓ | **节点全表**（用户输入/定时触发/LLM/知识检索/问题分类器/条件分支/迭代/工具/代码执行/人工介入）；**If-Else**（IF/ELIF 多路径/ELSE；AND/OR 复杂条件；文本 contains/starts with/值比较 equals/greater than/空态）；**Question Classifier**（LLM 分类路由）；**Iteration/Loop**（数组顺序/最大迭代/退出条件）；**Variable Aggregator**（汇聚互斥分支单一输出——If-Else/Question Classifier 只跑一支，输出同类时避免下游重复定义）；**Human Input 节点（v1.13.0）**（执行暂停→表单发给指定人→审批/修改/转交/超时→沿分支继续）；**并行分支**（条件+并行任务搜索/爬取/总结）；**早停**（IF/ELSE 检测错误消息→直出 Output 结束省 token） |
| 2 | n8n（Webhook 安全面） | ✓ | **四种认证**（Basic/Header/JWT/None）；**IP(s) Allowlist**；**GET webhook 保护**（?secret= 查询参数+IF 验证——仅 IoT/简单 web app 有限场景）；**x-api-key header 验证**；**HMAC 深度防护模板**（HMAC-SHA256 验发送者身份+raw body 逐字节签名保完整性+replay 过期时间戳默认 5 分钟+payload whitelist 过滤+timing-safe 比较）；**community 纵深防御**（Auth profiles HMAC timestamp+nonce/JWT JWKS/API Key/Combo HMAC+IP；rate limiting per IP；Content-Type allowlist+body size caps；mTLS proxy headers） |
| 3 | LangFlow（评估/调试面） | ✓ | **Playground**（实时测不同输入/审查修改记忆/监控输出逻辑）；**Traces（1.8）**（component spans 输入输出延迟错误+LangChain spans 链工具检索 LLM 含模型名 token 用量——不需外部 observability）；**Openlayer/Langfuse/Arize 集成**（自动收集 tracing——OpenTelemetry/OpenInference）；**flaky node 调试**（step-by-step 跑节点+查输入输出+临时 Chat Output taps 可视化中间值+输出约束简单 schema lists/objects 让失败显眼）；**多 agent 调试**（关键步骤 Chat Output 验证推理；并行减延迟）；**可视化路由调试**（看每条 query 路径/任意处 logging/隔离测组件/A-B 测路由策略/query 模式覆盖规则） |
| 4 | Activepieces（Webhook 触发器面） | ✓ | **三种触发器技术**（Polling 周期轮询/Webhooks 单 URL 监听/App Webhooks Subscriptions OAuth2 开发者应用单 URL 收全部授权事件）；**Webhook Trigger 生命周期**（On Enable：context.webhookUrl 发 HTTP 注册+store 存 webhook Id；On Handshake：challenge 握手类 normal run）；**Catch Webhook**（任意 HTTP 方法）；**npm run cli triggers create**；**Event Streaming**（Audit Logs→New Destination 选事件→Generate handler flow——落地个人项目带 webhook trigger+每事件 router 分支+预置 sample data）；**Webhook MCP**（每 action 成为 agent 工具） |
| 5 | Make（Data Store/函数面） | ✓ | **Data Store 模块全表**（Delete All/Get by key/Search 过滤/Check Existence 返回 true-false 不取数据/Count/Add-or-Replace）；**Make Functions App**（IML 函数从映射字段变独立模块——链式步骤式转换避免嵌套代码；空输入=空结果不停场景）；**Iterator+Array Aggregator**（逐行处理再映射列）；**Aggregator 类型**（Array/Numeric sum-min-max/Table HTML 表格邮件报告）；**Source Module 设置**（指定哪模块后的 bundles 聚合——通常 Iterator 后）；**dataStore.aggregate**（MongoDB 风格 group/match/sum 分组聚合）；**sum() 数组求和** |
| 6 | Pipedream（HTTP/API 面） | ✓ | **HTTP Request Action**（Postman-like 界面 headers/body/连 account——连上自动配置 authorization 头）；**HTTP destination 异步**（workflow 完成后发请求；url/data/headers/params/auth basic）；**http_request prop 类型**（组件 API default method/url）；**Python requests**（pd.inputs["github"]["$auth"]["oauth_access_token"]）；**Connect SDK**（PipedreamClient projectEnvironment dev/prod+projectId/clientId/clientSecret——前端 fetchToken）；**REST API**（GET /components/{key|id} metadata） |
| 7 | Anthropic（工具使用面） | ✓ | **工具调用循环**（Ring 1 假设调一次——真实任务常多次：create→read confirmation→create another；修复=while loop 持续喂结果直到 stop_reason≠tool_use）；**tool_choice 三值**（any=必须用一工具不强制特定/tool=强制特定/none=禁用默认）；**描述纪律**（≥3-4 句/工具复杂更多；描述=性能最重要因素：做什么/何时用何时不用/每参数含义/不返回什么/名字歧义；优先描述而非示例）；**三核心原则**（保持简单/透明显式规划/精心 ACI）；**高级工具使用**（Tool Search 不占上下文/Programmatic Tool Calling 代码环境调工具/ Tool Use Examples 通用标准）；**工具写作原则**（选对工具/命名空间化/返回有意义上下文/优化 token/建 eval） |
| 8 | deeplearning.ai（新课程面） | ✓ | **Agent Skills with Anthropic（2026-01）**；**Build Interactive Agents with Generative UI（2026-05 CopilotKit）**；**Building Adaptive AI Agents**；**Agent Memory（Oracle 合作）**（memory engineering 视长期记忆一等基础设施：外部于模型/持久/结构化——Oracle AI Database+LangChain+LLM pipelines）；**Spec-Driven Development**；**SGLang**；**AI Agents in LangGraph（Harrison Chase）**（ReAct/persistence/human-in-the-loop/search-augmented；agentic search 多答案 agent 友好格式）；**crewAI**（manager/worker 模式）；**Functions Tools Agents with LangChain**（LCEL） |
| 9 | GitHub（awesome AI 清单面） | ✓ | **awesome-ai-tools（5,690★）**（按场景分类文本/代码/图像/视频/语音克隆/音乐/营销/电话 Agent）；**system-prompts-and-models-of-ai-tools（143k★）**；**LlamaIndex**（RAG-first）；**Ollama+OpenWebUI+LobeChat**（本地三件套）；**MoneyPrinter**（YouTube Shorts 自动化）；**BrowserOS（13.7k★）**（开源 Agentic browser——Atlas/Comet/Dia 替代）；**Swarms**（企业级多 agent 编排）；**Griptape**（严格类型 Pipelines/Workflows/Agents）；**Atomic Agents**（Atomic Design 启发模块化）；**awesome-ai-agents-2026**（Wan 2.1 免费 OSS 自托管/HunyuanVideo 腾讯 OSS 消费级 GPU/LTX Video） |
| 10 | OpenClaw（会话管理/记忆面） | ✓ | **Incognito 模式**（session entry/transcript/compaction state 进 process memory 不上盘——Gateway 重启消失；不跑自动 memory flush；reset/delete 不建 archive；Codex runs 也 ephemeral）；**两层持久化**（Session store sessions.json：key/value 映射 sessionKey→SessionEntry 小可变安全编辑删条目；Transcript <sessionId>.jsonl：append-only 树结构 id+parentId——真实对话+工具调用+压缩摘要，用于重建未来上下文；Telegram topic -topic-<threadId>.jsonl）；**路径**（~/.openclaw/agents/<agentId>/sessions/）；**MEMORY.md**（每新会话加载 curated 长期记忆；daily notes 按需搜索——/new /reset 后近期 re-priming）；**Honcho**（跨会话——每 AI 回合后持久化对话；用户画像 preferences/facts/style+agent 画像 personality/behaviors）；**recall 边界**（compaction/provider context/retrieval scope） |

## 判重（双键检索结果）
- Dify 节点面：库内已落 §迭代节点/§工作流编排/§插件面——Variable Aggregator 汇聚互斥分支+Human Input 节点+IF/ELIF 多路径+早停模式为独有增量 ≥40% → 落地
- n8n Webhook 安全：库内已落 §Webhook 端点化/§工具面安全——HMAC 深度防护（签名+replay+whitelist+timing-safe）+四认证+IP allowlist 为独有增量 ≥40% → 落地
- LangFlow 评估调试：库内已落 §版本/MCP/部署——Traces 双层 span+可观测集成+flaky node 调试纪律为独有增量 ≥40% → 落地
- Activepieces 触发器：库内已落 §触发器/时序（r268A）+企业治理——三触发器技术+On Enable/Handshake 生命周期+Event Streaming 为独有增量 ≥40% → 落地
- Make Data Store：库内已落 §DataStore（r266）+场景蓝图——Data Store 模块全表+Make Functions App+Aggregator 设置纪律为独有增量 ≥40% → 落地
- Pipedream HTTP：并入记录（http_request prop/destination 异步/Connect SDK——增量约 40%）
- Anthropic 工具使用：库内已落 §工具循环/§工具调用——tool_choice 三值语义+描述纪律（≥3-4 句/优先描述）+高级工具使用三特性为独有增量 ≥50% → 落地
- deeplearning.ai 新课程：并入记录（Agent Memory/Agent Skills/Generative UI 课程情报）
- GitHub awesome 清单：并入记录（清单生态情报）
- OpenClaw 会话管理：库内已落 §子代理 session/§记忆三层——Incognito+两层持久化结构+MEMORY.md 加载+Honcho 跨会话为独有增量 ≥50% → 落地

## 独点落地（6 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r269B-1 | wb-execute-discipline | 3.24.0+ | Anthropic tool_choice 三值与工具描述纪律（增量合并 §工具循环） | 工具 |
| r269B-2 | wb-execute-discipline | 3.24.0+ | OpenClaw 会话两层持久化与 Incognito（增量合并 §子代理 session） | 工作流 |
| r269B-3 | wb-execute-discipline | 3.24.0+ | Dify 节点聚合与人工介入（Variable Aggregator/Human Input/早停） | 工作流 |
| r269B-4 | wb-execute-discipline | 3.24.0+ | n8n Webhook HMAC 深度防护（签名/replay/whitelist/timing-safe） | 工具 |
| r269B-5 | wb-execute-discipline | 3.24.0+ | LangFlow 评估调试面（Traces 双层 span/flaky 调试纪律） | 工作流 |
| r269B-6 | wb-execute-discipline | 3.24.0+ | Make Data Store 模块与函数 App（模块全表/Aggregator 纪律） | 工作流 |

## 复核
六独点均有当日实拉来源；均为增量合并或新面落地；并入记录：Pipedream HTTP 面/deeplearning.ai 课程情报/GitHub 清单生态。垃圾：本轮未产生临时文件。
