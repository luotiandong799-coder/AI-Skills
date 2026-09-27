# r269A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r266/r267/r268 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（插件开发面） | ✓ | **四类插件**（Tool/Agent Strategy/Extensions/Bundles）；**Tool Plugin**（/tools 目录+Tool 类+dify_plugin 依赖；provider credential 验证失败抛 ToolProviderCredentialValidationError；provider 是工具归属）；**Agent Strategy Plugin**（给 LLM 推理决策逻辑——Function Calling/ReAct/CoT/ToT 可下载；CLI 快速建策略插件；自定义配置表单与可视化组件；开放策略开发标准可集成学术算法）；**Customizable Model 四步**（model provider 文件→按模型类型分层 code 文件 llm/text_embedding→开发→打包）；**Cheatsheet**（dify plugin package ./yourapp）；**Agent Node**（Workflows 内 LLM 自主决策；策略=LLM 如何用工具的框架） |
| 2 | n8n（错误处理/数据转换面） | ✓ | **Edit Fields (Set) 专门数据转换**（表达值增改/删除/重命名字段——分离数据转换与业务逻辑）；**六步排障**（locate failing node→inspect resolved values→identify contract break JSON/date/items→reproduce minimal payload→normalize at source→lock schema）；**错误表**（[object Object]→JSON.stringify；invalid JSON→JSON fixer；Split Out empty→查字段名；Merge duplicates→查 merge mode）；**Error workflow 模式**（主 workflow+Error Trigger 节点+dedicated error workflow；Continue error output 两路径分流）；**六可靠性模式**（AI 输出在 Code node 验证并 throw——空串/markdown fences/拒答/截断对象直接进写节点=静默空行；Claude 结构化分类 category/severity/root cause/transient+dedup hash）；**Code Node 分页模式**（response.data||results||items||records） |
| 3 | LangFlow（生产部署/API 面） | ✓ | **API 访问**（http://IP_OR_DNS/api；LANGFLOW_PORT env）；**/run endpoint**；**Workflow API（Beta 1.9）**（/api/v2/workflows POST——mode background 异步+轮询 status completed/failed/cancelled）；**Flow DevOps Toolkit SDK**（production url+api_key_env 环境变量注入）；**K8s 生产**（Runtime headless backend-only——只服务 API 不跑可视化编辑器；最小 2Gi RAM+1000m 1CPU per instance ×3 replicas+HPA）；**API 认证 env 组**（LANGFLOW_AUTO_LOGIN=False/SUPERUSER/SECRET_KEY/NEW_USER_IS_ACTIVE=False/ENABLE_SIGNUP=False）；**watsonx Orchestrate 部署**（deployments/runs 状态轮询） |
| 4 | Activepieces（AI 模块面） | ✓ | **Ask AI step**（选 provider OpenAI/Anthropic/Gemini/Azure/Bedrock——admin 一次配 provider，模型可选）；**Agent Builder**（你选工具：app action/自有 automation/MCP server/上传文件；**Approval before it acts——paused run 保留 30 天**）；**Embeddable MCP**（用户点 Authorize→后端拿 token 跑用户自动化——OAuth）；**数据掩码**（凭据加密/敏感细节不进日志）；**760+ 集成**（pieces 开源 TypeScript SDK 自定义） |
| 5 | Make（HTTP/API 集成面） | ✓ | **HTTP app**（Get/Post/自定义 webhook；Parse response=Yes 映射响应）；**HTTP POST 场景联动**（Scenario A POST 编码 JSON 触发 Scenario B webhook——webhook scenario 只有新数据才跑）；**OAuth2 自定义连接**（先找基本信息再配 scenario）；**LLM 集成三路径**（direct API/Make 预建模块/LangChain——Make 最快因 retries/validation/routing 原生处理）；**API docs**（/data-stores endpoint teamId query param）；**蓝图**（webhook→JSON Parse→Iterator→Text Aggregator） |
| 6 | Pipedream（计划触发面） | ✓ | **Cron triggers 属性**（interval_seconds/cron/timestamp/timezone_configured/timezone_utc）；**Schedule source 内置**（Cron Expression 全控制 vs interval 简单——interval 不能定星期几；`0 8 * * 1-5` 8AM UTC Mon-Fri；**UTC 默认——本地时区要换算 UTC offset 输入**）；**New Scheduled Tasks API 触发**（Pipedream API scheduled tasks——secret 可选） |
| 7 | Anthropic（上下文工程/文档管理面） | ✓ | **Structured note-taking（agentic memory）**（agent 定期把笔记写到 context window 外的持久化内存——Claude Code to-do list/NOTES.md 模式；跨复杂任务追踪进度）；**Memory tool**（Claude 跨会话存取的 memory file directory——create/read/update/delete；**check-memory-first 协议 auto-injected："ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE"**；client-side 工具——API 给协议与 schema，应用实现）；**Context editing**（选择性清 conversation history 特定内容——context 有限资源收益递减；fine-grained runtime 控制）；**@mention files 引用**（prefer 代码内文件——HTML mockup 优于设计描述或截图）；**Agent Skills**（30-50 tokens 渐进披露相关才加载） |
| 8 | deeplearning.ai（agentic RAG 面） | ✓ | **Agentic AI 课程（9h19m）**（四设计模式：reflection/tool use/planning/multi-agent workflows；外部工具：databases/APIs/web search/code execution；评估：performance metrics/error analysis/production deployment）；**Building Agentic RAG with LlamaIndex**（Router Query Engine/Tool Calling/Agent Reasoning Loop/Multi-Document Agent）；**RAG 课程 Module 4**（agentic RAG/RAG vs fine-tuning）；**Advanced RAG**（sentence-window/auto-merging 超基线） |
| 9 | GitHub（顶级 AI agent 框架面） | ✓ | **框架矩阵**（Dify 143k 视觉平台/LangGraph 30-33k 生产有状态 agent 工作流/CrewAI 48-51k MIT 角色团队/AutoGen 57.4k MIT 研究原型维护模式/Agno ex-Phidata 39k Apache-2.0 生产多 agent 控制平面/OpenAI Agents SDK 27.2k 轻量/smolagents 27.9k 研究代码/Pydantic AI 17k 类型安全/Microsoft Agent Framework 企业 .NET/Mastra TS 生产/Microsoft Agent Framework）；**选型判据**（LangChain 七框架：developer experience/production reliability/observability/debugging/ecosystem/pricing transparency；"rarely settle on one"）；**场景映射**（复杂多 agent→LangGraph；轻量→OpenAI Agents SDK；TS web→Vercel AI SDK；角色团队→CrewAI；企业→Microsoft Agent Framework；RAG 重→LlamaIndex Workflows） |
| 10 | OpenClaw（技能权限/安全面） | ✓ | **三权限门**（agents.list[].tools.allow/deny agent 级；tools.sandbox.tools.allow 沙箱级工具过滤；sandbox.docker.network 容器网络）；**Operator Install Policy**（security.installPolicy——可信本地命令在 stage 后安装前批准/阻止 skill+plugin 安装；targets skill/plugin；exec command timeout）；**安全默认**（default no network/default no shell 或每命令确认/prefer fileRead-only/risky skills 沙箱内）；**L1-L3 分级**（L1 read-only/L2 writes or external APIs 需 review/L3 sensitive）；**四权限审计**（fileRead/fileWrite/network/shell——无技能同时四权限；audit log）；**内置高风险组**（group:runtime exec/bash；group:fs read/write——黑名单优先）；**工具策略**（shell requireApproval+allowedCommands 白名单/blockedCommands 黑名单 rm -rf/sudo/chmod）；**secret 注入作用域**（skills.entries.*.env/apiKey 只当轮注入 host 进程不进沙箱；secrets 不进 prompts 和 logs） |

## 判重（双键检索结果）
- Dify 插件开发：库内仅 §插件市场与发布流程（分发面）——开发面（四类结构/Agent Strategy 开放标准/自定义模型四步/dify_plugin SDK）为独有增量 ≥40% → 落地
- n8n 错误/数据转换：库内已落 §工具失败两层架构/§结构化输出解析器——错误工作流模式（Error Trigger+dedicated workflow）+六步排障法+Edit Fields 最佳实践为独有增量 ≥40% → 落地
- LangFlow 生产部署：库内已落 §版本化/§LFX 命令/§MCP——/api/v2/workflows 异步模式+Flow DevOps SDK+K8s runtime headless 部署+API 认证 env 组为独有增量 ≥40% → 落地
- Activepieces AI 模块：库内已落 §Agent Builder 工具选择——Approval paused run 30 天+Embeddable MCP+数据掩码为独有增量约 50% → 落地
- Make HTTP：库内已落 §HTTP v4 错误链——LLM 集成三路径选型+场景联动模式增量约 40% → 并入记录
- Pipedream 计划触发：库内已落 §并发/限流/重试——Schedule source 内置+UTC 默认时区换算为增量约 40% → 并入记录
- Anthropic 上下文工程：库内已落 §上下文工程/§记忆提取——Structured note-taking+Memory tool check-memory-first 协议+Context editing+@mention 引用纪律为独有增量 ≥50% → 落地
- deeplearning.ai agentic RAG：并入记录（LlamaIndex Agentic RAG 结构/Agentic AI 四模式已在库）
- GitHub 框架对比：并入记录（选型矩阵情报）
- OpenClaw 技能权限：库内已落 §安全纵深/§per-tool 最小权限——installPolicy+L1-L3 分级+四权限审计+secret 注入作用域为独有增量 ≥50% → 落地

## 独点落地（5 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r269A-1 | wb-execute-discipline | 3.23.0+ | Anthropic Memory tool 协议与 context editing（增量合并 §上下文工程） | 工具 |
| r269A-2 | wb-execute-discipline | 3.23.0+ | OpenClaw 技能权限三门与 installPolicy（增量合并 §安全纵深） | 可复用 Skill |
| r269A-3 | wb-execute-discipline | 3.23.0+ | Dify 插件开发四类与 Agent Strategy 开放标准（增量合并 §插件市场） | 工作流 |
| r269A-4 | wb-execute-discipline | 3.23.0+ | n8n 错误工作流模式与数据转换排障六步（增量合并 §工具失败处理） | 工作流 |
| r269A-5 | wb-execute-discipline | 3.23.0+ | LangFlow 生产部署 API 面（异步 workflow/DevOps SDK/headless runtime） | 工作流 |

## 复核
五独点均有当日实拉来源；均为增量合并或新面落地；并入记录：Make LLM 三路径/Pipedream UTC 时区/deeplearning.ai Agentic RAG/GitHub 框架矩阵。垃圾：本轮未产生临时文件。
