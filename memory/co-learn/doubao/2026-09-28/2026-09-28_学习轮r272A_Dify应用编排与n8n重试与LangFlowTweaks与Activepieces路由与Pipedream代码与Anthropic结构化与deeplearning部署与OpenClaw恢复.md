# r272A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表 200 词错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（应用编排面） | ✓ | **Workflow vs Chatflow**（Workflow 单轮批处理——webapp+API 批访问；Chatflow 每轮对话触发——会话变量存储更新/LLM 节点 memory/流式文本图像文件）；**App 类型选型**（Agent：自主推理+工具；Text Generator：结构化内容——Cold Email Writer/会议纪要）；**Agent 节点**（可返回文件 50MB 上限；Instructions 描述任务）；**对话式建 agent**（"Introducing New Agent"——聊天建 agent 自动生成可复用 skills 保持上下文；建好加 workflow 更大流程）；**Workflow Studio**（可视化画布——模型/检索/工具/代码/分支/触发器/人工审核） |
| 2 | n8n（错误/重试面） | ✓ | **Retry On Fail 节点级**（Settings 开关；Max Tries 上限 5；Wait Between Tries 上限 5000ms；常见基线 3 tries 2000-3000ms）；**默认不重试状态码**（400/401/403/404/422）；**指数退避公式**（waitSeconds = min(maxDelaySeconds, baseDelaySeconds * 2^(attempt-1))；finalWait = waitSeconds ± random(jitterPercent)）；**工作流级重试循环**（Code+Wait+IF；REST API retry /api/v1/executions/{id}/retry）；**三层错误处理**（node-level 有界瞬时失败；最终失败路由 Error Workflow；保留 failed executions 重试；副作用需幂等键）；**超时分类**（一种 timeout 不应直接进重试循环——Code 节点超时重试无意义） |
| 3 | LangFlow（API/tweaks 面） | ✓ | **Tweaks**（请求携带临时修改 flow 参数——单次运行覆盖组件设置不修改底层配置不持久；/run payload；TS client { model_name: "gpt-4o-mini" }；flow.tweak 创建新 flow 对象）；**session_id**（分离对话——同 session 继续）；**API 端点**（POST /v1/flows 创建；POST /v1/run/$FLOW_ID；/process /predict 已废弃改 /run）；**LFX run**（接受 .py 脚本程序化定义 flows）；**Workflow API beta**（mode: "background" 返回 job_id 排队）；**env-file**（uv run langflow run --env-file .env；x-api-key） |
| 4 | Activepieces（分支/路由面） | ✓ | **Router step**（条件分支基于表达式——contains 'urgent'/Greater Than > 100/Exists 操作符；caseSensitive 文本）；**ROUTER 类型**（executionType EXECUTE_FIRST_MATCH；conditions 数组）；**分支数据**（router.output.branches[] branchIndex/branchName/evaluation）；**流程操作 API**（stepLocationRelativeToNewParent AFTER/INSIDE_LOOP/INSIDE_BRANCH；LOCK_FLOW）；**MCP 工具**（ap_update_branch 更新分支条件不触碰步骤）；**AI 路由**（spam filter contains true → log → END）；**分支隔离风险步骤** |
| 5 | Make（webhook 面） | ✓ | **Webhook 机制**（URL 外部调用触发——instant trigger 区别于 scheduled；每 webhook 独用不能多场景共用）；**响应超时**（40 秒——Webhook Response 必须 40s 内到达否则 200 Accepted；错误场景 500；HTML/JSON/XML 默认响应）；**Webhook Response 放场景末尾**（Google Calendar 案例；前面错误则不 fire）；**webhook URL 是秘密**（当 API key 对待） |
| 6 | Pipedream（代码面） | ✓ | **npm 导入**（workflow 默认无包——import axios from "axios"；400k+ 包）；**@pipedream/platform axios**（import { axios } from "@pipedream/platform"——app props managed auth；axios($, {method/url/headers/data})）；**defineComponent**（props type app；run({steps, $}) 访问 steps.trigger.body；返回传下游）；**http_request prop 类型**（default method/url）；**v1→v2 迁移**（require→import） |
| 7 | Anthropic（结构化输出面） | ✓ | **messages.parse output_format**（Pydantic BaseModel——output_format=APIResponse；response.parsed）；**strict tool use**（strict: true 保证工具输入匹配 JSON Schema——grammar-constrained sampling 约束 token 采样）；**Agent SDK structured_output**（JSON Schema → outputFormat；structured_output 字段验证数据）；**json_schema 格式**（output_config.format type；Zod z.toJSONSchema()/Pydantic model_json_schema 生成）；**input_examples**（示例数组帮 Claude 理解工具）；**JSON Schema 限制**（enum 仅字符串/数字/布尔/null；const/anyOf/allOf/$ref/$defs 有限制） |
| 8 | deeplearning.ai（部署面） | ✓ | **Fine-tuning & RL for LLMs（Sharon Zhou AMD）**（post-training——SFT/RLHF 改善 instruction following/reasoning/safety；评估引导改进；生产就绪 cost-aware——promotion/serving 规划/monitor/compute budget）；**RAG Systems in Production（M5）**（production 挑战/评估策略/logging monitoring observability/tracing/customized evaluation/quantization/cost vs quality）；**LLMOps**（自动化测试 CI pipeline——每次变更评估）；**Serverless LLM Bedrock**（serverless 部署） |
| 9 | GitHub（工具榜面） | ✓ | **Trending 2026-09**（Ponytail——AI coding agent middleware 最小代码/减依赖/避免无价值 refactor；colibri——C 纯 MoE 引擎 26.5k★）；**GitHub Next**（Repo Mind Light 仓库整体理解/Project Copernicus LLM 导航/Discovery Agent）；**OpenMontage**（开源视频生产系统 12 流程 52 工具 500+ agent 技能）；**weekly**（stop-slop 去 AI 味/taste-skill 好品味/markitdown 文件转 MD/codegraph TS）；**ai-dev-tasks 7785★**；**multica**（人类+AI 一个团队自托管）；**rocketride-server**（C++ 核 50+ Python 节点 pipeline 引擎） |
| 10 | OpenClaw（会话恢复面） | ✓ | **Restart recovery**（gateway 启动几秒自动重派标记会话——合成系统消息告诉 agent 前轮被打断从 transcript 继续；最终回复未交付则包含文本直接交付不重做；重启不取消任务；重放保护只允许只读核心工具+明确安全插件）；**Session 重放**（保留已记录 tool calls 结果含嵌套；完成回复关闭重放；恢复等待消息 pending 不必重发）；**tombstoned sessions**（独立恢复路径）；**快照**（sess load <name> 恢复——live transcript 自动备份 pre-load~ts；session.snapshot("pre-analysis-checkpoint")）；**NemoClaw snapshot restore**（exact version/name/timestamp）；**checkpoint-restore**（--latest/--force/--workspace-only） |

## 判重（双键检索结果）
- Dify 应用编排：库内已落 §Agent 节点/§会话变量——Workflow vs Chatflow+App 选型+对话式建 agent 为独有增量 ≥40% → 落地
- n8n 错误/重试：库内已落 §错误三模式——节点级参数+退避公式+默认不重试码为独有增量 ≥40% → 落地（增量合并）
- LangFlow API：库内已落 §API 端点与 tweaks——tweaks 单次语义+TS client+LFX run .py+background job_id 为独有增量 ≥40% → 落地（增量合并）
- Activepieces 分支/路由：无 §分支路由 → 落地
- Make webhook：库内已落 §40 秒时效——增量有限（40s 已在库）→ 并入记录
- Pipedream 代码：库内已落 §组件结构——npm import+platform axios+app props 为独有增量 ≥40% → 落地
- Anthropic 结构化输出：库内已落 §结构化输出——strict mode+grammar-constrained sampling+Agent SDK structured_output+限制为独有增量 ≥40% → 落地（增量合并）
- deeplearning.ai 部署：库内已落 §评估/§RAG chunking——LLMOps CI+生产课程体系为独有增量 → 落地
- GitHub 工具榜：并入记录（Ponytail 同名仓库/multica/rocketride）
- OpenClaw 会话恢复：库内已落 §会话持久化——restart recovery+重放安全过滤+快照恢复为独有增量 ≥40% → 落地（增量合并）

## 独点落地（8 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r272A-1 | wb-execute-discipline | 3.32.0+ | Dify Workflow vs Chatflow 与 App 类型选型 | 工作流 |
| r272A-2 | wb-execute-discipline | 3.32.0+ | n8n Retry On Fail 参数与退避公式（增量合并 §错误三模式） | 可复用 Skill |
| r272A-3 | wb-execute-discipline | 3.32.0+ | LangFlow Tweaks 单次覆盖与程序化运行（增量合并 §API 端点） | 可复用 Skill |
| r272A-4 | wb-execute-discipline | 3.32.0+ | Activepieces Router 分支路由 | 工作流 |
| r272A-5 | wb-execute-discipline | 3.32.0+ | Pipedream npm 导入与 platform axios | 可复用 Skill |
| r272A-6 | wb-execute-discipline | 3.32.0+ | Anthropic Structured Outputs strict 模式（增量合并 §结构化输出） | 可复用 Skill |
| r272A-7 | wb-execute-discipline | 3.32.0+ | deeplearning.ai LLMOps CI 与生产课程 | 可复用 Skill |
| r272A-8 | wb-execute-discipline | 3.32.0+ | OpenClaw 重启恢复与快照（增量合并 §会话持久化） | 可复用 Skill |

## 复核
八独点均有当日实拉来源；均为增量合并或新面落地；并入记录：Make webhook（40s 已在库）、GitHub 工具榜。垃圾：本轮未产生临时文件。
