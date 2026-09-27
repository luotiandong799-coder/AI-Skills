# r235-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Hugging Face smolagents 1.26（PyPI+生产教程） | ✓ | managed_agents 参数；planning_interval 规划间隔；final_answer_checks 最终答案校验（_validate_final_answer）；沙箱执行（E2B/Modal/Docker/WASM，沙箱化不支持多 agent→不可信输入隔离子 agent）；VLM 视觉支持；Hub 分享 tools/agents；多 agent 输出字符串 gotcha（结构化数据显式转 JSON 否则 repr()）+无全局 timeout 每 run 设超时 |
| 2 | n8n（Structured Output Parser+社区） | ✓ | Require Specific Output Format；Structured Output Parser（JSON Schema 字段/enum/描述，parser 自动注入格式指令省 prompt）；Auto-fixing Output Parser（首次失败喂回模型修正）；Generate from JSON Example（全字段必填）vs 手动 JSON Schema；手动 schema 校验循环 runIndex 上限 4 次防死循环 |
| 3 | Agent 评测框架（AgentCompass/Claw-Eval/GitHub Blog/ASSERT/agent-eval-forge） | ✓ | AgentCompass（Benchmark/Harness/Environment 三组件解耦+容错异步+轨迹分析诊断 reward-hacking）；Claw-Eval（300 任务 9 类+三证据通道 traces/audit logs/snapshots→2159 rubric）；GitHub Copilot（三层次等价检测视觉+LLM 语义+dominator 必经状态）；ASSERT（自然语言规范→可执行 evals）；AI Litmus Test 2.0 三支柱（trajectory/faithfulness/efficiency） |
| 4 | Dify 可观测性（阿里云 ARMS/SLS/LangSmith/Langfuse/Arize） | ✓ | ARMS OpenTelemetry trace（inputs/outputs/token/五类 operation TASK TOOL CHAIN LLM RETRIEVER）；SLS 全文本索引任意 key-value+意图节点 PV 趋势分析+数据脱敏；内建 dashboard（request logs/token/response time/error rate per app）；三方选型（LangSmith 评估强/Langfuse 开源 prompt 管理/Arize 漂移检测） |
| 5 | Pipedream（Connect/MCP changelog 2026-09） | ✓ | OAuth 静态 URL（https://mcp.pipedream.net/v2）；2600+ 集成 app 发布为 MCP servers；10,000+ tools 一个 MCP endpoint；per-user auth 工具发现内建；兼容 ChatGPT/Claude/Cursor/Windsurf；Connect SDK code-level 控制 |
| 6 | Make（LLM 集成指南+Router+nested if-else） | ✓ | Router=目的地系统不是代码分支（优先级+fallback 兜底，无 fallback bundle 静默消失无日志）；AI 结构化输出字段直接驱动路由（urgency/topic/reply_needed）；Nested if-else+Merge 多层决策单场景内 |
| 7 | 腾讯（SkillHub/SkillPay/智能体开发平台） | ✓ | SkillPay 支付体系（2026-07-16：分发+调用+支付同链路，平台来源认证/内容完整性校验/可信调用入口，微信支付底层）；Agentic RAG（Agent Loop 驱动）；企业共享 Skills（提交+审批沉淀）；内置 Skills 安全审核+自动版本更新；SkillHub 7 万+ skill（2026-06）；ADP 4.0 AgentOps |
| 8 | deeplearning.ai（Oracle Adaptive AI Agents+Agentic AI 课程） | ✓ | agent traces→可复用 human-approved skills 管道；code knowledge graph 改进大型代码库检索；何时 adapt model 本身；Agentic AI 四模式（reflection/tool use/planning/multi-agent）；LangMem 长期记忆 |
| 9 | Langflow（1.10/1.12 release+scaling） | ✓ | Memory bases（per-flow 向量存储自动摄入对话跨 session 持久化）；1.12 OpenTelemetry（service health+flow runs）；1.9-1.10 内存降 89%（依赖裁剪+worker 生命周期+Linux CoW）；知识库本地向量库免重复摄入；1.13 企业化 RBAC |
| 10 | GitHub 生态（Trending/排行榜：hermes-agent/ponytail/humanizer/OpenMAIC/AutoGPT） | ✓ | hermes-agent 247,587 stars（"agent that grows with you"）；ponytail 118,297（"best code is code you never write"最懒资深开发理念，对照 wb-ponytail 套件）；humanizer 52,064（去 AI 味开源 skill）；OpenMAIC 27,873（清华多 agent 互动教室）；AutoGPT 187,453/firecrawl 182,407/langflow 155,168 生态规模参照 |

## 判重基准
双键检索：smolagents（r234C 已落 CodeAgent vs ToolCallingAgent，本条独有增量=多 agent 输出字符串 gotcha+每 run 超时+final_answer_checks）；n8n（r235-B 已落编排，本条独有增量=结构化输出 parser auto-fix）；agent 评测（r234A 分层评估/r235-A TRACE，本条独有增量=三证据通道+必经状态骨架+框架三组件解耦）；腾讯（r235-A TRACE，本条独有增量=SkillPay 商业化链路+Agentic RAG）；Pipedream（r234B MCP 面，本条独有增量=托管 MCP 静态 URL+per-user auth）；Langflow（r235-A 1.10/1.11 面，本条独有增量=Memory bases 自动摄入+内存降 89%）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① smolagents 多 agent 输出纪律 | 字符串 gotcha 显式 JSON；每 run 超时；final_answer_checks 校验；沙箱不支持多 agent 隔离子 agent | 工作流 | wb-execute-discipline |
| ② n8n 结构化输出解析器 | schema 自动注入省 prompt；auto-fix 自愈；手动循环上限 4 次 | 工具 | wb-execute-discipline |
| ③ agent 评测三支柱 | 框架三组件解耦；三证据通道；必经状态 dominator | 可复用 Skill | wb-execute-discipline |
| ④ 技能商业化+记忆自动摄入 | SkillPay 分发/调用/支付同链路；Agentic RAG；Memory bases per-flow 自动摄入 | 工作流 | wb-execute-discipline |
| ⑤ 托管 MCP 服务器 | 静态 URL+per-user auth+工具发现内建；2600+ app 一个 endpoint | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉原文来源，无编造。
- 功能套件检查：① 与 wb-ponytail 对照（GitHub ponytail 118K stars 理念"best code is code you never write"——套件保留，无需改）；② 与 wb-max-token-saver 互补（多 agent 超时/JSON 纪律省 token）；③ 与 wb-context-compressor 互补（记忆自动摄入面）。三件套无需增删。
- 垃圾：本轮未产生临时文件。
