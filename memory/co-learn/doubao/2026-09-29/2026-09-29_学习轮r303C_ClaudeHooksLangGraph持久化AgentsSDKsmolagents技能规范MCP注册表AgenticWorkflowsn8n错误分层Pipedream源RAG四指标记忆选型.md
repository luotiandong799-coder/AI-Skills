# 学习轮 r303C（2026-09-29）— AI 技能库学习

批次：r303C（每轮 10 次信源实拉，本批 30 次全量逐站完成；查询词与 r302、r303A/B 全错开）
判重基线：当日全部留痕（r284A~r303B）+ WorkBuddy 留痕 + SKILL.md 最新章节（双键检索：来源标识+概念词）
信源健康度：30 次实拉全部成功返回；无站点连续失败；本批无删/加信源动作。
垃圾清理：本轮未产生临时文件（无 _tmp/_log/__pycache__）。

## 十独点（增量判定通过，纯重复不落）

### 1. Claude Code hooks 事件模型与权限决策四值（工具/可复用 Skill 层）
来源：code.claude.com/docs/en/agent-sdk/hooks + /docs/en/hooks + anthropics/claude-plugins-official hook-development SKILL，2026-09-29 实拉。
- PreToolUse 在工具调用前触发，可 **block 或修改** 工具调用（如拦截危险 shell 命令）；PostToolUse 在工具执行后触发，用于记录文件变更审计轨迹；PermissionRequest 在权限弹窗出现时触发；PermissionDenied 在自动模式拒绝工具调用时触发——其 JSON 输出 `hookSpecificOutput.retry: true` 可指示模型**重试被拒的工具调用**，但分类器未产出 verdict 时 Claude Code 忽略 retry。
- PreToolUse 的 `permissionDecision` 有四值：`allow` / `deny` / `ask` / `defer`——hook 不只能拦，还能把决定权交回（defer）。
- **subagents 与主 agent 共享同一套 hooks**；插件内 hooks 定义在 `hooks/hooks.json`，SKILL frontmatter 也可内嵌 hooks。
- 判据：与"工具结果断言层"（调用后打标）互补——hooks 是**调用前**的结构化拦截+权限决策机制，且决策粒度是四值不是二值。

### 2. LangGraph 双持久层 + DeltaChannel 修复 O(N²) 快照成本（工具层）
来源：docs.langchain.com/oss/python/langgraph/persistence + langchain.com/blog/delta-channels + aws.amazon.com DynamoDBSaver + learn.microsoft.com MongoDBSaver，2026-09-29 实拉。
- 持久化双系统：**checkpointers=线程级短期记忆**（每个 super-step 把图状态存为 checkpoint 到 thread，图执行后仍可访问→支持时间旅行/中断恢复），**stores=跨线程长期记忆**。
- 默认 full-snapshot 模型下 checkpoint 存储按 O(N²) 增长（长消息历史+文件系统上下文时是真实运维成本）；**DeltaChannel 每步只存 delta、每 K 步写一次全量快照**——恢复延迟有界、存储成本随会话变长保持平坦，且现有 thread 透明升级。
- 生产级 connector：AWS 官方维护 DynamoDBSaver（按 payload 大小智能处理）、Azure DocumentDB 走官方 MongoDBSaver；TTL 支持 `delete`（连 run+checkpoint 全删）与 `keep_latest`（留最新 checkpoint 删旧）。
- 判据：选持久引擎先定"要不要时间旅行/中断恢复"，再选 checkpointer 实现；长会话必须上 delta 通道，否则存储成本不可控。

### 3. OpenAI Agents SDK 原语：handoff 是专用工具调用、guardrail 异步跑输出流（工具/工作流层）
来源：pypi.org openai-agents 0.6.7 + larsderidder/framework-analysis tier-1/openai-agents-sdk.md + openai.com running-codex-safely + openai.github.io openai-agents-js，2026-09-29 实拉。
- SDK 由 Swarm 实验演化而来，核心原语=agents/handoffs/guardrails/sessions/tracing，支持 100+ 模型 provider。
- **handoffs 是专门化的工具调用**，用于 agent 间转移控制权；sessions 自动管理会话历史；tracing 内建、对接主流可观测平台。
- **guardrails 对 agent 响应输出流异步运行**：文本会话检查 output text deltas，音频会话检查 transcript deltas（前提是 transcript 可用而非独立文本模态）；违规立即切断响应。GuardrailAgent 是 Agents SDK `Agent` 类的 drop-in 替换，自动从配置装载 guardrails。
- Codex 生产安全四件套=managed configuration（受管配置）+ constrained execution（约束执行）+ network policies（网络策略）+ agent-native logs（agent 原生日志审计）。
- 判据：多 agent 系统"换人"用 handoff（工具调用语义可观测），"防违规"用 guardrail（异步流上检查，不阻塞生成）；日志用 agent 原生格式而非事后拼装。

### 4. smolagents：CodeAgent vs ToolCallingAgent + AST 白名单执行 + 生产显式 sandbox（工具层）
来源：pypi.org smolagents 1.26.0 + deepwiki.com huggingface/smolagents + folarin.dev code-agent-vs-tool-calling-agent + theneuralbase.com，2026-09-29 实拉。
- **CodeAgent 写 Python 代码编排工具**（step=一次完整代码执行，无法拦截程序内单次工具调用），**ToolCallingAgent 发 JSON 工具调用**（无第二解释器）。
- 默认 LocalPythonExecutor 基于 **AST 执行**防止危险内建、import 白名单（`additional_authorized_imports` 显式扩权）；生产应显式 `sandbox='e2b'`（云沙箱，需 E2B_API_KEY、约 25s/次执行延迟）或 `sandbox='local'`。
- ReAct 循环：生成代码→执行→执行日志作为 chat messages 回记忆→直到调用 `final_answer` 工具才终止。
- 判据：已把计算放进沙箱的用 ToolCallingAgent（更轻），需要编排复杂工具链的用 CodeAgent；**默认本地执行只适合实验**，生产必须显式选 sandbox。

### 5. Agent Skills frontmatter 硬约束 + 两级加载成本模型（可复用 Skill 层）
来源：agentskills.zhcn.dev/specification + vercel.com/blog/agent-skills-explained + freecodecamp.org 规范表 + arXiv 2608.08453（138K SKILL.md 实证）+ arXiv 2607.25032，2026-09-29 实拉。
- frontmatter 仅 `name`/`description` 必填：name≤64 字符、小写字母数字单连字符、**必须匹配目录名**与 `^[a-z0-9]+(-[a-z0-9]+)*$`；description≤1024 字符、"做什么+何时用"；license/compatibility/metadata 可选；**规范兼容运行时忽略未识别 key**→技能跨 agent 可移植。
- 两级加载：会话开始时仅注入每个已装技能的 name+description（约 **100 tokens/技能**），模型据此决定是否加载 body——这是"库能装很多技能却不付全部内容成本"的机制。
- arXiv 138K 实证：技能可复用性依赖 frontmatter 质量——模型只凭 name+description 判断是否加载，描述写得差=技能永远不被发现。
- 判据：写技能先过 frontmatter 校验（名称匹配目录、描述含触发场景）；description 是技能的唯一"售卖窗口"，花最多功夫。

### 6. GitHub Agentic Workflows：Markdown 定义 + safe-outputs 白名单 + gh aw compile（工作流/工具层）
来源：github.blog 2026-02-13 tech preview + 2026-06-11 public preview + docs.github.com creating agentic workflows，2026-09-29 实拉。
- `.github/workflows/*.md` 用 **YAML frontmatter（on/permissions/safe-outputs/tools）+ Markdown 自然语言指令**定义自动化（issue triage/CI 失败分析/文档更新）。
- `gh aw compile` 把 md 编译为 `.lock.yml` **标准 Actions**——因此复用现有 runner groups 与策略约束。
- 安全优先设计：**safe-outputs 白名单限制模型能做的副作用动作**（如 `create-issue: title-prefix/labels/allowed` 限定标签取值）、permissions 最小化、tools+toolset 限定模型可用的工具子集。
- 判据：把"让模型干活"编译成"标准 CI 可审计动作"——模型负责决策，safe-outputs 负责圈定决策范围；发布=合并到 main 即自动生效。

### 7. n8n 错误处理三层分层：节点 Retry / 错误工作流 / API 重放（工作流层）
来源：n8n.io/workflows/16744 + docs.n8n.io/flow-logic/error-handling + n8nlogic.com + community.n8n.io 300785，2026-09-29 实拉。
- **Layer 1 节点级 Retry On Fail** 管瞬时错误；**Layer 2 工作流级 Error Workflow**（Error Trigger 首节点）捕获未处理失败；**Layer 3 API 级** `POST /api/v1/executions/{id}/retry` body `{"loadWorkflowExecution": true}` 重放失败执行。
- 永久错误（401/畸形 payload）要告警**不要**五次重试；可预测错误（期望数据处空数组）要 fail loudly；Continue on Fail 让单节点失败不杀死整个执行，输出带 `$error` 字段供下一节点决策。
- 死信模式：retryCount 上限（≤3 次）后转 Jira/Slack 告警；LLM tool calling 失败用单次可视化执行轨迹显示**哪个工具调用失败/为什么/模型传了什么参数**。
- 判据：错误按"瞬时/永久/可预测"三分类，每类一个处理路径；重试预算与退避是硬编码不是模型自觉。

### 8. Pipedream event source 与 workflow 解耦：一源多流 + 内置去重（工具/工作流层）
来源：pipedream.com/docs/sources + /docs/components + /docs/connect/components/triggers，2026-09-29 实拉。
- **event source 是独立于 workflow 的资源**：单一 source 可触发多个 workflow、也可被自有 app 通过 API 消费事件。
- triggers 分两类=**app-based event sources**（第三方服务事件）与 **native triggers**（HTTP/Webhook、Schedule、Email、RSS）；组件支持 `props` 部署时接收用户输入、内置 key-value store 存状态、**内置 deduping 策略**去重。
- Connect 面向最终用户：`pd.triggers.deploy` 部署 webhook 事件到用户 app，per-user auth 单次调用跑 action，测试用 `x-pd-environment: development` + `x-pd-external-user-id` 头。
- 判据：要"一个数据源喂多个流"就把 source 独立出来，不塞进 workflow；要消费事件就 API 拉，不重复部署。

### 9. RAG 评估四核心指标与诊断配对：检索问题 vs 生成问题（工作流/可复用 Skill 层）
来源：dev.to RAG-evaluation-2026-four-core-metrics + manning.com LLM-evaluation-and-alignment ch6 + superml.org RAGAS + langfuse.com faithfulness + atlan.com RAG-evaluation-explained，2026-09-29 实拉。
- 四指标成两对：**检索对=context precision**（检索块是否相关且排序好）+ **context recall**（标准答案要点被检索到多少）；**生成对=faithfulness/groundedness**（回答每个论断是否被检索上下文支持，0.6=约 40% 论断无依据）+ **answer relevance**（judge 模型基于回答生成反事实问题、与原问题算语义相似度）。
- 目标阈值：faithfulness>0.85 生产、>0.95 高利害域；**四指标必须同 run 计算**——否则无法判断坏答案是检索问题还是生成问题（两者需要相反的修复）。
- 范围差异：faithfulness 只对 RAG 范围（真实但上下文不支持的论断也算失败）；hallucination 是更广的失败类。盲点：标准指标假设检索索引可信，0.95 faithfulness 仍可能因陈旧/未拥有内容返回错答案。
- 判据：低分先看是哪对指标——检索对低改索引/分块，生成对低改 prompt/上下文；faithfulness 是可控上下文里最可行动的幻觉信号。

### 10. Agent 记忆选型分层：Mem0 工作记忆 + Graphiti 时间档案（工具层）
来源：llm4agents.com/blog/graphiti-mem0-agent-memory + vectorize.io mem0-vs-zep + rockb 记忆架构指南 + hindsight.vectorize.io 开源记忆系统盘点，2026-09-29 实拉。
- **Mem0**=个性化优先、向量存储+可选知识图谱；聊天历史回忆**优于朴素 RAG**（存提取事实而非原始消息块），省 80-90% token、低延迟。
- **Zep/Graphiti**=时间知识图谱，每个事实带时间戳、有效窗口保留版本历史——能答"上个季度用户说了什么预算"式时间问题；LongMemEval 63.8% vs Mem0 49.0%。
- 选型判据：需要推理事实随时间变化→Graphiti；需要便宜大规模取回正确上下文→Mem0；两者可分层=Mem0 活跃会话工作记忆 + Graphiti 长期档案。框架互相承认对方强项（Mem0 认 Zep 时间推理、Zep 认 Mem0 token 效率与生态广度）。
- 判据：记忆选型先问"要不要时间维度"——不要就用便宜的提取事实向量存储，要就上时间知识图谱。

## 功能套件检查（wb-ponytail / wb-max-token-saver / wb-context-compressor）
- 本批十独点中 hooks 权限决策（#1）、RAG 四指标（#9）、记忆选型（#10）、技能 frontmatter 规范（#5）可并入 wb-context-compressor / wb-execute-discipline 章节；本轮 SKILL 章按内容分派追加至 wb-context-compressor（见 SKILL.md 章节 commit）。
- 无功能套件增删。

## 复核与收尾
- 十独点全部带来源（本轮 30 次实拉 URL/文档标题）；每点均标注提升层；增量判定通过（与 r303A LangChain 检索优化、r303B 编排模式/评测收敛等均无纯重复）。
- 本轮留痕一次 commit；SKILL 章一次 commit；批末 SSH over 443 push 一次。
