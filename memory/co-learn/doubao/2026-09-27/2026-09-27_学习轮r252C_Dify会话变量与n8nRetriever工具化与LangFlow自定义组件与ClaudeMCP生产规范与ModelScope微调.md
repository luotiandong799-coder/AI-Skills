# r252-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（conversation variables 面） | ✓ | Conversation Variables（Chatflow only）：会话级持久，跨多轮 chatflow runs 单会话；sys.conversation_id 作用域（不同会话独立副本）；唯一可变变量类型；Variable Assigner 节点写入；类型 String/Number/Object/Array[object]；append 模式持续追加（简化 OpenAI 记忆：session variable Array[object] append 持续更新记忆，类型转换需 escape node）；用途：待办清单/token cost/用户偏好/临时存储 |
| 2 | n8n（vector retriever 面） | ✓ | Vector Store Retriever 节点与 QA Chain 配合（LangChain 风格）；Vector Store 节点 ai_vectorStore 输出接 Retriever/QA Chain；Retrieve Documents (As Tool for AI Agent) 模式：ai_tool 输出接 AI Agent Tool input，Tool Name=agent 暴露的函数名，Tool Description 指导何时用；混合检索社区节点 n8n-nodes-qdrant-hybrid：dense+sparse prefetch 结果 RRF 融合；两阶段检索：文件描述检索（metadata 相似度过滤限文件数）→文档 chunk 检索（仅在命中文件内取 chunk）；索引自身工作流做语义搜索（24h 周期+webhook 查询） |
| 3 | LangFlow（custom components 面） | ✓ | Custom component=继承 Component 的 Python 类；类级属性标识描述；input/output 列表决定数据流；方法定义行为；内部变量错误处理与日志；扩展机制：lfx extension init my-extension（extension.json v0 manifest/pyproject.toml/src 规范布局）；Langflow Assistant 生成组件代码（from lfx.custom import Component; from lfx.io import FloatInput/MessageTextInput/Output）；安全：LANGFLOW_ALLOW_CUSTOM_COMPONENTS 禁用自定义组件执行（受控部署），配合 LANGFLOW_COMPONENTS_PATH 白名单；踩坑：method 后字符串必须与自定义方法名一致，输出与方法强绑定（硬性规则）；Bundles 架构（多组件包） |
| 4 | Activepieces（triggers 面） | ✓ | 三触发技术：Polling（周期调端点查变更，延迟 5-15min，实现简单）/Webhook（单 URL 实时，注册需 handshake challenge，中等复杂度）/App Webhook subscriptions（平台级 OAuth2 单 URL 收所有授权事件，暂不支持，workaround=对 endpoint 轮询）；Webhook trigger 生命周期：On Enable 用 context.webhookUrl 注册+store webhook Id；队列架构：一切 queue-backed（webhooks/recurring jobs 落 Redis BullMQ，worker 拉取；spike 不丢工作排队 drain）；API workflow：route requests by headers/path params/payload |
| 5 | Make（filters/routers 面） | ✓ | Filter=两个模块间的条件门：下一模块仅当条件为真才运行；Router 中每分支放 filter 决定哪个分支执行；添加方式 wrench icon→Set up a filter；label 要有意义（如 "Lead source = Email"）；Filter 是 Make 条件逻辑的基础单元，Router 分支 + Filter 组合实现条件路由 |
| 6 | Pipedream（sources/triggers 面） | ✓ | Event sources=workflow 独立资源（同一 source 可触发多个 workflow；sources 与 workflow 分离）；触发类型：HTTP/webhook/Schedule/Email/RSS/App-based；两类 triggers（Connect 部署）：App-based event sources/Native triggers；Component 能力：props 部署时接受用户输入/触发 HTTP/timers/cron/manual/emit events（this.$emit）触发 workflows 可被 API 消费/内置 key-value store（this.db）/dedupe strategies；10,000+ prebuilt triggers and actions；pd.triggers.deploy({id: "gmail-new-email-received"...})；故障：polling triggers 处理太多数据时保存转圈（用 timer-based polling 定时取）；sources 无 type 属性=默认 sources |
| 7 | Claude（MCP best practices 面） | ✓ | Remote server 是 distribution 关键（唯一跨 web/mobile/cloud-hosted agents 配置）；group tools around intent 不按 endpoint（少而精的工具胜过 exhaustive API mirrors，别 1:1 包 API）；MCP 2026-07-28：Apps/Tasks versioned extensions framework；Auth 对齐生产 OAuth 2.0/OIDC（Entra/Okta）；Streamable HTTP 官方推荐 transport（SSE deprecated）；生产级 server 清单：Zod 校验 handler 边界/长运行工具返回 job ID+status resource/stderr 结构化日志每请求/MCP Inspector smoke test 进 CI/versioned server name 加性 schema 变更/HTTP transport 必须 auth（OAuth 2.1 或 signed tokens）/per-tool rate limits+timeouts/replay capture 调试；分工：Tools=外部系统访问，CLAUDE.md=项目上下文，Hooks=确定性自动化 lifecycle events；三种设置：claude_desktop_config.json 本地 server/claude mcp add per project/remote server custom connector；memory MCP server 三操作 write/query/delete-update |
| 8 | ModelScope（微调/数据集/Agent 面） | ✓ | MSAgent-Bench：598k 对话综合工具数据集（通用 API/模型 API/API 问答/API 无关指令）——训练 agent LLM（多轮对话模式）；魔搭紫皮书：跑出第一个结果（下载+环境+本地/云端 Notebook）→让模型适应任务（ms-swift 轻量微调+评估前后）→搭具体应用（客服电话质检报告/企业知识问答）；MS-Swift 微调：Qwen3.5-0.8B-Base 完整跑通行业 Agent 流水线（硬件门槛低）；创空间部署 Skill：Gradio/Streamlit/Docker/static website；创建/代码同步/部署/日志监控/明文与 secret 变量管理/自动诊断修复；MiniCPM5-1B-GGUF：多框架 cookbook+Agent Skill（TRL+PEFT/LLaMA-Factory/ms-swift/unsloth） |
| 9 | Full Stack Skills（全栈 agent 工程面） | ✓ | Agent-Ready fullstack 栈：React/Next.js+FastAPI+LangGraph backend+MCP server+eval harness（graded against 2026 Agent-Ready rubric）；编排框架选型：LangGraph（stateful graph 复杂条件流程）/CrewAI（role-based 快速 bootstrap）/AutoGen（conversational Azure 集成）；2026 agent 工程师栈：LLM APIs/OpenAI Agents SDK/LangGraph/CrewAI/LlamaIndex/tool calling/MCP/vector DBs/RAG/workflow engines/sandboxing/evals/tracing/human approvals/security identity；Pydantic 结构化输出（business area info list model）；技能栈层次：LLM 基础→RAG→agent 框架→API 工具调用→向量库→部署 MLOps |
| 10 | agentskills.io（featured 面） | ✓ | agentskills.io 展示 40+ clients（Microsoft/OpenAI/Cursor/GitHub 采用；partner skills Atlassian/Figma/Canva/Stripe/Notion/Zapier）；Claude Code skills 位置 .claude/skills/（项目）或 ~/.claude/skills/（全局）；生态统计：anthropic-cybersecurity-skills 734 skills 26 domains→754 skills（MITRE ATT&CK+NIST CSF 2.0 mapping+ATT&CK Navigator layer）；agentskillslist top 4061 skills 按 downloads+stars 排序（#01 Self Improving Agent 480.6K ClawHub downloads，capture learnings/errors/corrections）；技能例：project-planner/visualization-expert/email-drafter/meeting-notes/decision-helper；agent-introspection-debugging（capture-diagnosis-contained recovery-introspection reports，失败时可复现诊断而不是重试）；Schemathesis（API schema→negative/edge-case 测试覆盖）；claude-code-plugins-plus-skills：423 plugins 2849 skills 177 agents（ccpi CLI package manager） |

## 判重基准
双键检索（相对 r224-r252B 已落章节）：Dify（r252-A 记忆/r252-B 检索——会话变量面独有）；n8n（r252-A RAG/r252-B agent 记忆——Retriever 工具化面独有）；LangFlow（r252-B 调试 DevOps——custom components 面独有）；Activepieces（r252-A AI builder/r252-B MCP——triggers 面独有）；Make（r250 未落 filter/router 细节——条件门纪律独有但内容薄）；Pipedream（r251-A 组件 API/r252-B OAuth——sources 模式面独有）；Claude（r251-A SDK/r252-A subagents/r252-B 记忆——MCP 生产规范面独有）；ModelScope（r251-C Agent 表面——微调/数据集/部署面独有）；Full Stack Skills（未落——全栈工程栈增量中等）；agentskills.io（r251-A trending——生态规模/标准面增量合并）。未选素材：Make filters（单点细节弱）；Full Stack Skills（课程类偏泛）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify Conversation Variables | 会话级可变状态+append 记忆 | 工作流 | wb-execute-discipline |
| ② n8n Retriever 工具化 | ai_tool 输出+两阶段检索+RRF | 工具 | wb-execute-discipline |
| ③ LangFlow Custom Components | Python 组件+扩展安全开关 | 工具 | wb-execute-discipline |
| ④ Claude MCP 生产规范 | intent 分组+OAuth 2.1+job ID | 工作流 | wb-execute-discipline |
| ⑤ ModelScope 微调与数据集 | MSAgent-Bench+ms-swift+部署 Skill | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
