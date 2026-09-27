# r270A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r266-r269 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（工具调用/函数节点面） | ✓ | **Agent 节点**（给 LLM 工具自主控制——迭代决定用什么/何时用；动态推理 vs 预规划；适合 GPT-4 等强模型）；**ParameterExtractorNode**（function calling 结构化提取——_generate_function_call_prompt 构造 system prompt 注入用户查询模板）；**QuestionClassifier**（LLM 路由）；**reverse invocation**（插件可反向调用 ParameterExtractor/QuestionClassifier——封装复杂 prompt+code 逻辑用 LLM 处理硬编码规则难解任务）；**节点全表**（Iteration/Variable Aggregator/HTTP Request/Template Transform Jinja2/Tool/Parameter Extractor）；**Workflow vs Chatflow**（同节点库同执行模型——触发方式与交互形式不同；Workflow 一次运行端到端）；**Workflow DSL**（Edges 条件路由/状态 conversation 管理）；**异步外部服务**（ComfyUI POST 提交→prompt_id→轮询） |
| 2 | n8n（循环/数据面） | ✓ | **隐式循环黄金规则**（每节点默认对每 Item 执行一次——上游 N Items 下游执行 N 次——零循环代码）；**Loop Over Items（SplitInBatches）**（显式循环：保存原始输入/每迭代返回预定量/done 输出合并；Batch Size；API 限流/顺序处理）；**跨批表达式**（$input.all().map(i => i.json.email).join(', ')；reduce/removeDuplicates）；**Code Node 适用判据**（多 item 归并单 item/复杂数组重构/依赖多步/带 break 循环/新建 items/表达式过长）；**嵌套循环**（forEach 嵌套；reset 选项清输入用第二三组数据） |
| 3 | LangFlow（API 端点面） | ✓ | **health_check**（GET /health_check）；**/api/v1/responses**（OpenAI Responses API 兼容——model=FLOW_ID+input+x-api-key）；**Build endpoints**（POST /build/$FLOW_ID/flow 返回 job ID 流事件）；**Workflow API**（/api/v2/workflows mode=stream+stream_protocol=agui；mode=background 轮询）；**run 端点**（POST /api/v1/run/FLOW_ID input_type/output_type/**tweaks**——tweaks 按 component_id+parameter_name 覆写组件参数）；**custom_component API**（POST 代码构建组件/update/validate/code 验证 Python 片段）；**JS client**（fetch/axios/官方 JS client） |
| 4 | Activepieces（代码步骤面） | ✓ | **CODE 步骤**（自定义 TypeScript/JavaScript 数据转换——export const code = async (inputs) => {...} 返回对象；npm 包解析数据/格式化/领域规则）；**Code Action JSON**（name/type CODE/settings.sourceCode.code+packageJson/input 映射）；**MCP tools**（ap_flow_structure 截断 300 字符 vs code 读取完整源码 packageJson+input mappings 不截断）；**触发数据键控**（Google Sheets 列字母 A/B/C——Use Column Names 键控 header）；**表达式**（{{ output }}/模板字符串动态 URL/条件字段） |
| 5 | Make（AI 提示工程面） | ✓ | OpenAI best practices（具体描述 context/outcome/length/format/style；指令开头用 ### 或 """ 分隔）；**prompt 类型表**（zero-shot/one-shot/few-shot/chain-of-thought——各适用与注意）；**Dotprompt**（prompts as code——prompt+model+参数与应用代码分离，UI 快速迭代）；**消息结构**（system/user/assistant 角色——assistant 历史维持多轮）；**reasoning 模型**（描述期望结果而非逐步指令）；**eval 驱动**（测试数据衡量性能） |
| 6 | Pipedream（环境变量/秘密面） | ✓ | **env vars 分离秘密与配置**（process.env.API_KEY 而非密钥本身）；**两类存储**（集成→connected accounts；不支持的 app/任意配置→env vars）；**Python 访问**（os.environ["VAR"]）；**组件内 env vars 不可直接访问**（sources 用 secret props；actions 对象浏览器选 env var 传步骤）；**secret props**（secret:true 密码式隐藏+加密存储+运行时解密——仅 string props）；**MCP env**（PIPEDREAM_CLIENT_ID/SECRET/PROJECT_ID/ENVIRONMENT+x-pd-environment/x-pd-external-user-id 头）；**REST auth**（OAuth client credentials 换 token——服务端安全存） |
| 7 | Anthropic（长上下文/Claude Code 面） | ✓ | **长上下文提示**（20k+ tokens：长文档放顶部在 query/instructions/examples 之上；query 放末尾——复杂多文档输入响应质量提升至 30%）；**context awareness**（Opus 4.6/4.5 跟踪剩余 token 预算高效管理）；**Claude Code 大代码库导航**（像工程师遍历文件系统/读文件/grep——本地运行无需索引上传；vs RAG 嵌入全库检索）；**harness 长运行 agent 两折**（initializer agent 首次建环境+coding agent 每次会话增量进展留清晰 artifacts；一次一个 feature）；**compaction cache-safe forking**（压缩用与父完全相同的 system prompt/context/tool definitions——缓存前缀复用）；**结构化笔记**（agent 定期写笔记到窗口外——to-do list/NOTES.md） |
| 8 | deeplearning.ai（Agent 评估课程面） | ✓ | **Agentic AI 课程**（Module 4：evals/error analysis/组件级评估——被评最有价值）；**Evaluating AI Agents（Arize AI，2h36m）**（可观测性洞察+调试；组件级评估：测试例子/选评估器 code-based vs LLM-as-a-Judge/指标；结构化实验迭代质量+路径）；**smolagents（Hugging Face，54m）**（写并执行代码完成任务）；**视频 agent 评估三方法**（SigLIP 图像-文本相似度评分——可编程数字分；LLM-based judges 自定义标准捕捉定性不匹配；structured rubric）；**patterns not frameworks**（reflection/tool use/planning/multi-agent 跨库） |
| 9 | GitHub（本地 LLM 推理面 2026） | ✓ | **llama.cpp（~124.7k★ MIT）**（CPU-only 8GB 可行；CUDA/ROCm/Metal/Vulkan/SYCL/CANN/OpenCL；本地推理约 $0.002/M tokens vs 云 API $2.50-15.00——1000 倍成本差）；**Ollama（166k★）**（GGUF；OpenAI+Anthropic 兼容）；**MLX（27.5k★）**（Apple Silicon；2026 加 CUDA）；**vLLM vs SGLang vs TRT-LLM**（vLLM 最灵活默认/SGLang prefix-heavy+结构化输出/TRT 最大单模型吞吐；TGI 已退休）；**Exo（42.7k★）**（分布式）；**Jan.ai（41.1k★）**（隐私桌面）；**LocalAI（49k★）**（多模态+P2P federated+prefix-cache-aware v3）；**Copilot CLI 本地化**（2026-04 对 Ollama/vLLM/Foundry Local——auth 可选免订阅；COPILOT_OFFLINE 停遥测）；**NobodyWho**（Rust 引擎 6 框架绑定日榜） |
| 10 | OpenClaw（模型供应商面） | ✓ | **密钥配置层级**（OPENCLAW_LIVE_<PROVIDER>_KEY 单实时覆盖最优先；<PROVIDER>_API_KEYS 逗号分隔多 key）；**供应商表**（BytePlus ARK 国际火山 BYTEPLUS_API_KEY；Vercel AI Gateway AI_GATEWAY_API_KEY 例 vercel-ai-gateway/anthropic/claude-opus-4.6；OpenAI openai/gpt-5.1-codex；Fireworks OpenAI-compatible 默认 glm-5p2-fast；Arcee 直接或 OpenRouter）；**Ollama 本地**（ollama pull+OLLAMA_API_KEY 任意值不验证）；**JSON 配置**（models.providers.<id>.apiKey 引 env var 或硬编码；defaults.provider+model；minimax baseUrl+api anthropic-messages）；**CLI 入职**（openclaw onboard --auth-choice）；**gateway order**（anthropic: ["anthropic:api"]） |

## 判重（双键检索结果）
- Dify 工具调用：库内已落 §Agent 策略（r267A）+插件面——Agent 节点自主控制+ParameterExtractor function calling+reverse invocation+Workflow vs Chatflow 为独有增量 ≥40% → 落地
- n8n 循环：库内已落 §数据转换（r269A）——隐式循环黄金规则+SplitInBatches 显式循环+跨批表达式+表达式 vs Code crossover 为独有增量 ≥40% → 落地
- LangFlow API：库内已落 §部署 API（r269A background 轮询）——health_check+Responses 兼容+tweaks 覆写+custom_component API 为独有增量 ≥40% → 落地（合并增量）
- Activepieces 代码步骤：库内已落 §Tables data code——CODE 步骤 JSON+完整读取 MCP+触发键控为独有增量 ≥40% → 落地
- Make 提示工程：并入记录（方法已在库内）
- Pipedream 环境变量：库内已落 §Secrets 面（OpenClaw Secrets 而非 Pipedream）——env vars 分离+组件限制+secret props 加密为独有增量 ≥40% → 落地
- Anthropic 长上下文：库内已落 §上下文工程/§Compaction——长文档置顶+query 末尾 30%+context awareness+Claude Code 导航+harness 两折+cache-safe forking 为独有增量 ≥50% → 落地
- deeplearning.ai agent 评估：库内已落 §评估驱动——组件级 eval+Evaluating AI Agents+三评估方法为独有增量 ≥40% → 落地
- GitHub 本地推理：并入记录（生态情报）
- OpenClaw 模型供应商：库内已落 §模型路由（r268C gateway）——密钥层级+供应商表+Ollama 本地+CLI onboard 为独有增量 ≥40% → 落地

## 独点落地（7 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r270A-1 | wb-execute-discipline | 3.26.0+ | Anthropic 长上下文提示与 Claude Code 导航（增量合并 §上下文工程） | 工具 |
| r270A-2 | wb-execute-discipline | 3.26.0+ | Dify Agent 节点与函数调用节点（增量合并 §Agent 策略） | 工作流 |
| r270A-3 | wb-execute-discipline | 3.26.0+ | n8n 隐式循环与显式循环（增量合并 §数据转换） | 工作流 |
| r270A-4 | wb-execute-discipline | 3.26.0+ | deeplearning.ai agent 评估方法论（增量合并 §评估驱动） | 可复用 Skill |
| r270A-5 | wb-execute-discipline | 3.26.0+ | OpenClaw 模型供应商配置（增量合并 §模型路由） | 可复用 Skill |
| r270A-6 | wb-execute-discipline | 3.26.0+ | Pipedream 环境变量与秘密管理 | 工具 |
| r270A-7 | wb-execute-discipline | 3.26.0+ | LangFlow API 端点与 tweaks（增量合并 §部署 API） | 工作流 |

## 复核
七独点均有当日实拉来源；均为增量合并或新面落地；并入记录：Make 提示工程/GitHub 本地推理生态。垃圾：本轮未产生临时文件。
