# r271B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表 160 词错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（文件处理/分块面） | ✓ | **Knowledge Pipeline 编排**（Chunker 类型：Q&A Processor 处理电子表格问答对/General Chunker 基础文档；文本预处理规则：替换连续空格/换行/tab、删除 URL/邮箱）；**提取器**（Document extractors 解析各格式为下游可处理格式——文件类型检测/内容提取/可选图像提取）；**工作流文件上传**（文档 TXT/PDF/HTML 用 Doc Extractor 节点提取为字符串；音视频需 audio-to-text/keyframe 工具；gpt-4o-audio-preview 直接处理音频）；**分段策略**（自动检测自然边界/自定义——技术文档 800-token chunks+150-token overlap；FixedRecursive/EnhanceRecursiveCharacterTextSplitter；段落/章节/句 separators；自动推荐最优化分隔符） |
| 2 | n8n（数据转换面） | ✓ | **表达式**（{{ }} JS 风格动态设参数：previous nodes/workflow metadata/env vars；$json.body.city；$input.item.json；$node["Name"].json.id 访问其他节点；方法调用 $json.name.toLowerCase()；JMESPath $jmespath(obj, expression) 查询复杂嵌套——无效返回 undefined）；**表达式 vs 数据节点**（能用表达式就用——即时预览计算值；复杂转换用 Code 节点）；**数据结构**（array of objects 每对象包 json key——Code node [{json:{...}}]）；**Set 节点指南**（={{ $json.score * 2 }}）；**拖拽 data mapping** |
| 3 | LangFlow（记忆面） | ✓ | **Memory Base**（向量化格式存长期 chat history——跨会话语义检索最相关上下文；vs Message History 按时间序；vs Knowledge Base 手动填充——memory base 自动嵌入向量按语义相似检索）；**Chat memory vs vector store memory**（chat memory 专为存/取聊天消息数据库构建——Agent 和 Message History 组件内置访问数据库作 memory；vector stores 设计为语义搜索文本 chunks）；**Message History 组件**（组合聊天历史+消息存储；Langflow storage 或专用 chat memory 数据库 Mem0/Redis；Agent 内置 chat memory 默认启用 Langflow storage 多数够用；{memory} 代码创建 memory input port）；**Astra DB Chat Memory**（AstraDBChatMessageHistory LangChain 类）；**Store Message/Message History helper**（Data objects 存/取）；**1.12 变更**（默认安装不含多数 vector store bundles——Chroma 本地默认仍用） |
| 4 | Activepieces（代码步骤面） | ✓ | **Code step TypeScript**（export async function code(inputs)；data 转换 map/toUpperCase；packages {} 加 npm 包——导入外部库执行专门函数）；**执行引擎**（Piece Executor 动态加载 pieces at runtime；CODE 类型设置 sourceCode+packages+input）；**沙箱隔离**（flow code 永远跑在 sandbox 包裹 engine 进程；AP_EXECUTION_MODE 是自托管最重要安全选择——恶意 flow 被限制单 worker pod 还是触内核；SANDBOX_CODE_ONLY：V8 沙箱快轻量/不支持 NPM/多租户安全/reusable workers）；**MCP tools 参考**（PIECE: pieceName/actionName/input/auth/continueOnFailure/retryOnFailure） |
| 5 | Make（调度面） | ✓ | **Schedule settings**（默认每 15 分钟；选项：At regular intervals/Once/Every day/Days of week/Days of month/Specified dates/On demand）；**调度用途**（特定时间跑——每日中午/每隔周二/每 15 分钟备份）；**Webhook+cron 外部调度**（Crontap 集成——webhook URL 触发任意间隔） |
| 6 | Pipedream（数据存储面） | ✓ | **Data Stores**（key-value store——持久状态跨 workflow 共享；CRUD；set/get/'' 删除值保留 key；TTL 记录过期自动删除——留空不失效）；**DB service prop**（$.service.db——component-specific key-value store 跨执行保持状态；set 值必须 JSON-serializable）；**Data Stores API**（add/update multiple/append/check existence/delete）；**用途**（save API 结果/用户输入/interim data；read/update/enrich；tracking status/aggregating metrics）；**File store**（项目级 filesystem 所有 workflow 共享）；**Project secret**（加密不可从 UI 读） |
| 7 | Anthropic（MCP 面） | ✓ | **MCP connector**（Messages API 直接连远程 MCP server 无需独立 MCP client——mcp-client-2025-04-04 已弃用）；**MCP 架构**（Client/Transport/Server——stdio 本地进程/streamable HTTP 远程（前 SSE）；Server 暴露 resources/tools/prompts；capability negotiation 初始化期间）；**起源**（Anthropic David Sorria Para+Justin Spahr-Summers——LSP 启发；2024-11 open source；M×N 问题）；**SDK 实现**（各 SDK 含 client+server，支持 stdio+streamable HTTP；server-exposed primitives+client-exposed sampling/roots/elicitation）；**企业集成**（前 MCP：连接 CRM 需 custom code+auth 手动+context 自己管——每新系统重建） |
| 8 | deeplearning.ai（评估课程面） | ✓ | **Evaluating AI Agents（Beginner 2h36m Arize AI）**（Evaluation in the time of LLMs/Decomposing agents/Lab1 building agent/Lab5 adding structure）；**Improving Accuracy of LLM Applications**（Sharon Zhou Lamini+Amit Sangani Meta——SQL agent+评估指标+prompt engineering+self-reflection）；**Fine-tuning & RL（6h10m 43 视频 11 作业）**（SFT/RLHF 改善 instruction following/reasoning/safety；evaluation 引导改进——build evals reveal problems/choose data+rewards/iterate）；**评估指标**（LLM-as-Judge/Perplexity/Safety refusal rate/Over-refusal 良性提示拒绝率应低/Hallucination）；**Agent 评估子类**（Planning：Plan Quality/Node F1/Step Success Rate；Reasoning：Next-tool Prediction Accuracy）；**指标绑定业务风险**（generic metrics 几乎总是错——pick metrics tied to cost of being wrong） |
| 9 | GitHub（CLI/终端 agent 面） | ✓ | **Copilot CLI GA**（2026-02-25 GA 所有 Copilot 订阅者——terminal-native coding agent；2025-09 preview 数百改进）；**能力**（引用 issues/浏览 PR/管理 repos/MCP tools；默认 Claude Sonnet 4.5 可切 GPT-5；free tier 50 请求/月）；**custom agents**（.agent.md 自带 tools/instructions/MCP servers——interactive wizard 创建）；**hf-agents**（HF CLI 扩展——自动检测硬件选最佳 GGUF 模型 llmfit——hf agents run pi 单命令本地 agent）；**Terminal-Bench 2.1**（Codex CLI 83.4% 领先/Claude Code 78.9%/Gemini CLI 1000 free req/day）；**开源 CLI**（DeepSeek Harness ~203k 全插拔/OpenCode ~202k 默认 provider-agnostic/Codex CLI ~119k Apache-2.0 sandboxed/Pi ~98k 精简/OpenHands ~85k 自主）；**Grok Build**（Plan Mode 默认——计划审批后改文件；8 并行 sub-agents isolated git worktrees） |
| 10 | OpenClaw（MCP 面） | ✓ | **MCP 服务器配置**（~/.openclaw/openclaw.json mcp.servers；url/transport streamable-http|sse/command+args npx stdio/enabled/connectionTimeoutMs/requestTimeoutMs/toolFilter include 白名单/auth oauth（openclaw mcp login）/sslVerify 仅信任私有 HTTPS false/clientCert-clientKey mTLS/headers Authorization）；**CLI 命令**（openclaw mcp list/show/set/unset；openclaw mcp serve --url wss://gateway --token-file）；**暴露为 MCP**（openclaw.direct /mcp endpoint——从任意 AI 工具管理 fleet）；**dashboard 可视化 MCP 管理器**（按类别 Development/Research/Communication/Database/Finance/DevOps/Design；Connect 填凭据 Save 即用——无需 JSON/终端/重启） |

## 判重（双键检索结果）
- Dify 文件处理：库内已落 §RAG chunking 策略/§混合检索——Q&A Processor+工作流 Doc Extractor 节点+自动/自定义分段（800/150）为独有增量 ≥40% → 落地
- n8n 数据转换：无专门章节——表达式语法+数据结构 json key+表达式 vs 数据节点为独有 → 落地
- LangFlow 记忆：库内已落 §语义记忆/§记忆——Memory Base 向量化语义检索 vs Message History 时间序 vs Knowledge Base 为独有增量 ≥40% → 落地
- Activepieces 代码步骤：库内已落 §认证——Code step TS+packages+沙箱 AP_EXECUTION_MODE+动态加载为独有增量 ≥40% → 落地
- Make 调度：库内已落 §场景蓝图——Schedule 选项表+外部 webhook cron 为独有增量 ≥40% → 落地
- Pipedream 数据存储：库内已落 §并发/运行时——Data Stores CRUD+TTL+$.service.db+File store 为独有增量 ≥40% → 落地
- Anthropic MCP：库内已落 §MCP 规范——connector 直接 API 集成+传输类型+SDK 双实现为独有增量 ≥40% → 落地
- deeplearning.ai 评估：库内已落 §agent 评估方法论——评估课程体系+指标子类（Plan Quality/Node F1/Step Success）为独有增量 ≥40% → 落地
- GitHub CLI：并入记录（Copilot CLI GA/开源 CLI 生态情报）
- OpenClaw MCP：并入记录（与 §OpenClaw 插件 相邻面，配置表留待后续）

## 独点落地（8 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r271B-1 | wb-execute-discipline | 3.30.0+ | n8n 表达式与数据结构 | 工作流 |
| r271B-2 | wb-execute-discipline | 3.30.0+ | Dify 文件处理与分段策略 | 工作流 |
| r271B-3 | wb-execute-discipline | 3.30.0+ | LangFlow Memory Base 三类记忆 | 工具 |
| r271B-4 | wb-execute-discipline | 3.30.0+ | Activepieces Code Step 与沙箱 | 可复用 Skill |
| r271B-5 | wb-execute-discipline | 3.30.0+ | Make 调度选项与外部 cron | 工作流 |
| r271B-6 | wb-execute-discipline | 3.30.0+ | Pipedream Data Stores 状态持久化 | 工具 |
| r271B-7 | wb-execute-discipline | 3.30.0+ | Anthropic MCP Connector 直接集成 | 可复用 Skill |
| r271B-8 | wb-execute-discipline | 3.30.0+ | deeplearning.ai 评估指标子类 | 可复用 Skill |

## 复核
八独点均有当日实拉来源；均为增量合并或新面落地；并入记录：GitHub CLI 生态、OpenClaw MCP 配置。垃圾：本轮未产生临时文件。
