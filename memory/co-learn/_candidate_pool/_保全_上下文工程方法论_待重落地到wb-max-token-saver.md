version: 3.890.0
## context=finite attention budget：硬限制+effective-capacity+U 形注意力（lost-in-the-middle）· 组件典型范围表（tools 500-3000/few-shot 500-2000/query 50-500 按优先度）（来源：muratcankoylan/Agent-Skills-for-Context-Engineering（**Treat context as a finite attention budget, not a storage bin——每个 token 竞争注意力、耗尽预算无法中途补充；三约束：硬 token 限制、较软 effective-capacity 上限、U 形注意力曲线（中间信息受 penalize，lost-in-the-middle）**）+ yennanliu/ai-engineering-from-scratch（**组件典型范围：Tool definitions 500-3000 tokens 动态中优先按 query intent 剪枝；Few-shot 500-2000 tokens 动态高优先按任务相似度选；User query 50-500 tokens 固定最高优先**）2026 实拉；与 §上下文预算管理（既有）分工——那边管"用多少开始压"，本条管"context 本质约束+各组件占多少合理"）
Context 先当注意力预算：三约束（硬限/有效容量/U 形曲线），组件按范围+优先度配。
- **三约束**：**硬 token 限制 / effective-capacity 软上限 / U 形注意力（中间信息被 penalize）**（muratcankoylan 原文）→ 判据：**中间信息要少放**；有效容量<标称。
- **组件范围表**：**tools 500-3000（按 intent 剪枝）/ few-shot 500-2000（按相似度选）/ query 50-500（最高优先）**（yennanliu 原文）→ 判据：**组件有基准**；超基准即裁。
- **预算即注意力**：**context 是预算不是存储**（muratcankoylan 原文）→ 判据：**放进去=花注意力**；能省则省。
- **提升层**：工具/可复用 Skill（上下文认知）。

## 两层记忆 token 效率与 memory-aware 模型选择：LoCoMo 91.6%@6,956 vs 72.9%@26,000（+18.7 点 4x）· 大窗模型深分析/小模型快速调用 · memory 有每消息 token 成本（来源：Rohit Raj（**LoCoMo benchmark：两层记忆 91.6% @ ~6,956 tokens/query vs 全上下文 72.9% @ ~26,000 tokens——+18.7 点、约 4x token 效率；context window 是 RAM 不是 storage**）+ PipeLLM（**model selection becomes memory-aware：大上下文模型（Gemini 2.5 Pro 1M）做深度分析，小便宜模型做快速工具调用，unified gateway 让切换无缝；cost optimization follows memory optimization**）+ Maia（**每个 memory 增加每消息 tokens，删不需要的 memory 减 token**）2026 实拉；与 §记忆提取四策略（既有）分工——那边管"记忆怎么提"，本条管"记忆的 token 成本与模型分工"）
记忆先算账：两层记忆 4x token 效率，memory-aware 选模型，记忆条目本身有成本。
- **两层量化**：**LoCoMo：91.6%@6,956 vs 72.9%@26,000——+18.7 点、约 4x 效率**（Rohit 原文）→ 判据：**先量化再选**；两层优于全塞。
- **模型分工**：**大窗模型做深度分析、小模型做快速工具调用**（PipeLLM 原文）→ 判据：**按任务选窗**；不一律大窗。
- **记忆成本**：**每条 memory 增加每消息 tokens，删除减本**（Maia 原文）→ 判据：**记忆有价**；冗余记忆删。
- **提升层**：工作流/工具（记忆成本治理）。

## stuff vs retrieve 决策与 compaction 缓存：S<<Weff stuff / S>>Weff retrieve / 中间 hybrid · system prompt 末尾 cache_control 断点独立缓存 · 80-90% 成本削减（来源：LLM Stack（**S << Weff（工作集远小于有效容量）→stuff；S >> Weff 或单 query 只触小片→retrieve（2M 行代码库/文档集/历史对话）；中间→hybrid stuff 小核心+retrieve**）+ Anthropic Compaction（**system prompt 末尾加 cache_control breakpoint——system prompt 独立缓存，compaction 后仍从缓存读，只需写新 summary 缓存条目**）+ AI Agents Kit（**Token Budgeting 从定性指令到定量预算+prompt caching=80-90% 成本削减**）2026 实拉；与 §压缩后规则重声明（既有）分工——那边管"压缩后规则怎么复活"，本条管"压缩前先决策 stuff/retrieve+缓存布局"）
先决策 stuff/retrieve：工作集小就塞、大就检索、中间 hybrid；system prompt 缓存断点独立保活。
- **stuff/retrieve 阈值**：**S<<Weff stuff；S>>Weff 或单 query 触小片 retrieve；中间 hybrid**（LLM Stack 原文）→ 判据：**先估工作集**；大库必检索。
- **缓存断点**：**system prompt 末尾 cache_control——独立缓存，compaction 后仍从缓存读**（Anthropic 原文）→ 判据：**system 单独缓存**；压缩不动它。
- **量化收益**：**定量预算+prompt caching=80-90% 成本削减**（AI Agents Kit 原文）→ 判据：**预算化=省钱**；定性指令不够。
- **提升层**：工作流/可复用 Skill（检索-塞入决策）。
## MELD 五结果记忆准入：insert/merge/relate/conflict/reject+三信号（claim-key identity+embedding similarity+NLI verdict）+context/freshness gates · 单一可审计 Patch（来源：MELD（**self-managing coherence mechanism for federation of agent memories——运行时模型即知识图；每个 brain 用五结果流程准入每条 incoming claim：insert/merge/relate/conflict/reject；三信号：scoped claim-key identity、embedding similarity、natural-language-inference verdict；context 与 freshness gates 下进行；经唯一可审计、认证的 Patch 对象**）2026 实拉；与 §记忆提取四策略（既有）分工——那边管"记忆怎么从对话提"，本条管"多条 agent 记忆合流时每条 claim 按五结果准入"）
记忆准入先五分类：每条 claim 经五结果流程+三信号+双 gates，动作只有可审计 Patch。
- **五结果**：**insert/merge/relate/conflict/reject 之一**（MELD 原文）→ 判据：**每条必有归宿**；不默认 insert。
- **三信号**：**claim-key 身份+embedding 相似度+NLI 裁决**（MELD 原文）→ 判据：**多信号决策**；不单靠相似度。
- **可审计动作**：**唯一认证 Patch 对象，无旁路写入**（MELD 原文）→ 判据：**写有审计**；不绕过 Patch。
- **提升层**：工具/工作流（记忆准入）。

## 共享记忆双刃剑与 Session 策略：single brain compound vs over-share noisy log · session ID 共享=跨委派连续/隔离=防泄漏 · project-level memory 事实传播（来源：Vectorize（**single brain：研究 agent 发现→写作 agent 上下文→审查 agent 参考——系统 compound；或 over-share 互相矛盾→共享库变 noisy log 无人可靠检索**）+ n8n（**共享 session ID：orchestrator 与 specialist 共享会话历史，specialist 可见用户对 orchestrator 说的（跨委派连续性）；隔离 session ID：各 agent 只见自己历史（防上下文跨域泄漏）**）+ Claude Code Projects（**project-level memory store：每个 thread 添加并从它读取；线程学到 billing 需某人 sign-off→事实传播到未来线程；context 有机积累，减少复杂 prompt engineering；记忆跨天跨周**）2026 实拉；与 §MELD 五结果准入（同轮 ④）分工——那边管"单条 claim 怎么准入"，本条管"共享层整体形态+会话隔离策略"）
共享先分账：single brain 可 compound 可 noisy，session 按连续性/泄漏权衡，project memory 让事实传播。
- **双刃剑**：**compound（研究→写作→审查串联）或 over-share 变 noisy log**（Vectorize 原文）→ 判据：**共享有代价**；overshare 即污染。
- **session 决策**：**共享=跨委派连续；隔离=防上下文泄漏**（n8n 原文）→ 判据：**按连续性需求选**；专注场景必隔离。
- **project memory**：**thread 学到的持久事实传播到未来 thread；context 有机积累**（Claude Code 原文）→ 判据：**共享事实入库**；新 thread 先读。
- **提升层**：工作流/可复用 Skill（共享形态）。

## 失效信号与异步缓冲：coordinator 发 ~12 token invalidation 替代重播 · Muffin orchestrator 路由→team 并发→缓冲交换→summarizer · flat-file 冲突文件人工仲裁（来源：agent-coherence（**每个 shared artifact 本地缓存 per agent，fresh 时读本地；写提交 coordinator，发轻量 invalidation signals（~12 tokens）给 peers——下次读抓新版本而非重播整个 artifact；single-writer-multiple-reader per artifact+bounded staleness**）+ Muffin（**orchestrator 按推理需求路由到 single/multi-agent；multi-agent 配置 team，agents 并发推理、通过 shared memory buffer 交换中间发现，私有推理保持本地；最后 summarizer**）+ mech.app（**两 agent 同时写同文件→Syncthing 创建 conflict file；写协议要求先查 .sync-conflict 文件，存在则停下人工解决**）2026 实拉；与 §共享记忆双刃剑（同轮 ⑤）分工——那边管"共享层形态"，本条管"变更怎么传播+异步协作结构"）
变更先传播：失效信号替代全量重播，异步缓冲交换中间发现，文件冲突走人工。
- **失效信号**：**coordinator 发 ~12 token invalidation，peers 下次读抓新版本**（agent-coherence 原文）→ 判据：**改后发信号**；不重播全文。
- **Muffin 结构**：**orchestrator 路由→team 并发→共享缓冲交换→summarizer 收尾**（Muffin 原文）→ 判据：**异步交换**；私有推理本地。
- **文件冲突**：**写前查 .sync-conflict，存在即停+人工解决**（mech.app 原文）→ 判据：**冲突文件即停**；人工仲裁。
- **提升层**：工具/工作流（变更传播）。
## 确定性结构回归优先：结构执行 DAG（tool sequence/retry loops/wasted token deltas）sub-5ms Exit 0/1 替代 15-60s LLM judge · 五规则评分器（禁工具/权限检查/必填参数/敏感字段/调用次数）（来源：AgentDiff（**LLM judges 打分语义细微（15-60s 昂贵非确定）；AgentDiff 评估 structural execution DAG（tool sequence order、retry loops、wasted token deltas）sub-5ms 纯图算法——instant deterministic Exit Code 0/1 for CI/CD**）+ 掘金（**先写最硬的 5 规则评分器：禁止工具不能调用；权限检查必须出现；必填参数不能缺；敏感字段不能输出；工具调用次数不超过阈值；再加轨迹评分：对关键链路定义期望轨迹（read-only query: auth_check -> ...）**）2026 实拉；与 §统计回归判定（同轮 ③）分工——那边管"结果用统计判"，本条管"能确定性的先确定性（结构层）再上语义层"）
结构先回归：执行 DAG 纯图算法毫秒级确定性判定，规则评分器先于语义。
- **结构优先**：**tool sequence/retry loops/wasted token deltas 用图算法 sub-5ms 出 Exit 0/1**（AgentDiff 原文）→ 判据：**能确定性先确定性**；LLM judge 最后上。
- **五规则**：**禁工具/权限检查/必填参数/敏感字段/调用次数超阈值**（掘金 原文）→ 判据：**规则先硬**；语义后软。
- **轨迹评分**：**关键链路定义期望轨迹（auth_check -> ...）**（掘金 原文）→ 判据：**轨迹可比**；偏航即错。
- **提升层**：工具/工作流（结构回归）。

## 成本与效率指标：cost_per_attempt/cost_per_success=cost/成功率 · mean tool calls per task · P95 latency · cost per task 看趋势非绝对值 · TrajectoryScore 聚合 step 分数（来源：Kunal Ganglani（**cost_per_attempt = LLM token cost + tool call costs + infra costs；success_rate = successful/total；cost_per_success = cost_per_attempt / success_rate**）+ Agentic Engineering Guide（**metrics：hallucination rate/mean tool calls per task/P95 latency/cost per task（track trend, not absolute）/human override rate**）+ FutureAGI（**TrajectoryScore 聚合 step-level scores 为单一轨迹评分——部分学分决策+趋势 dashboard 的正确信号；ToolSelectionAccuracy 按 tool name+call depth 切片最快定位**）2026 实拉；与 §确定性结构回归（同轮 ④）分工——那边管"对错判定"，本条管"成本与效率度量"）
效率先定指标：成本摊到成功，工具调用/延迟/轨迹分可切片。
- **成本指标**：**cost_per_success = (token+tool+infra)/success_rate**（Kunal 原文）→ 判据：**成本摊成功**；只算 attempt 会骗人。
- **效率指标**：**mean tool calls per task、P95 latency、cost per task 看趋势非绝对值**（Agentic Guide 原文）→ 判据：**趋势优先**；单值无意义。
- **轨迹度量**：**TrajectoryScore 聚合 step 分数；ToolSelectionAccuracy 按 tool/depth 切片定位**（FutureAGI 原文）→ 判据：**可切片**；问题定位到工具层。
- **提升层**：工作流（效率度量）。

## prompt 优化与回归闭环：regression suite gates every change（optimizer 提候选 suite 决定 promote）· 复现测试（fail→pass）+回归测试（pass→fail）双验证 · 组件级评估（code-based vs LLM-judge 选择）（来源：FutureAGI（**agent-opt 六优化器（RandomSearch/BayesianSearch+Optuna+MetaPrompt/ProTeGi/GEPA/PromptWizard）run eval-driven optimization；2026 pattern：regression suite gates every change——optimizer 对 regression set 提候选，suite 决定 promote；EarlyStoppingConfig 改进停止即砍搜索预算**）+ ISSCEC（**补丁验证：复现测试（fail→pass）+回归测试（pass→fail）；原始仓库通常只有回归测试没有复现测试——LLM 自动生成复现测试**）+ deeplearning.ai（**Evaluating AI Agents：component-level evaluations——testing examples+code-based 或 LLM-as-Judge 选择+right metrics；结构化为 experiments 迭代 output quality+path taken**）2026 实拉；与 §成本效率指标（同轮 ⑤）分工——那边管"度量什么"，本条管"优化/补丁怎么闭环验证"）
优化先闭环：候选由 regression suite 裁决，补丁过双验证，组件级选对 judge。
- **suite 裁决**：**regression suite gates every change，optimizer 提候选 suite 决定 promote；EarlyStopping 止损**（FutureAGI 原文）→ 判据：**优化被门禁**；不是无限搜。
- **双验证**：**复现（fail→pass）+回归（pass→fail）都跑；缺复现测试用 LLM 生成**（ISSCEC 原文）→ 判据：**双向验证**；单测一边不够。
- **组件级评估**：**按组件选 code-based 或 LLM-judge+对指标；结构化为 experiments**（deeplearning.ai 原文）→ 判据：**组件分测**；judge 选型按组件。
- **提升层**：工作流/可复用 Skill（优化闭环）。
## 工具管道开销实测：工具结果 JSON ~34% 输入 token · input:output 1.9:1 · OpenAI 框架显示 vs 官方账单 ~1.6x 膨胀——记账按官方 API 口径（来源：n8n Community《Each tool you attach to an AI Agent node is re-billed every turn》2026-07-24（**4 tools wired into one Agent node added ~3x+ per-turn cost；Tool results (the JSON an executed tool hands back) were ~34% of total input tokens over a multi-step run——often bigger than the user message and the tool schemas combined；input:output ratio landed around 1.9:1——most of that input was tool plumbing, not conversation**）+ n8n Community《Retrieve LLM Token Usage》（**for OpenAI models there's a ~1.6x increase in token usage in n8n in relation to the number displayed at the official OpenAI API data (and it's actually what's used for billing)**）2026-10-06 实拉；与 §每步成本累积（同轮 ③）分工——那边管"每步怎么算"，本条管"工具管道是隐藏大头+框架计数不可信"）
工具先记账：管道是隐藏大头，计数按官方 API 口径。
- **管道大头**：**工具结果 JSON ~34% 输入 token（比用户消息+tool schemas 还大）；每加一个工具每轮重计费**（n8n 原文）→ 判据：**工具结果先瘦身**；schema 精简+结果截断优先。
- **输入输出比**：**1.9:1——大部分输入是工具管道不是对话**（n8n 原文）→ 判据：**优化工具管道**；省输入比省输出划算。
- **口径差异**：**框架显示 vs 官方账单 ~1.6x 膨胀（账单按官方 API 数据）**（n8n 原文）→ 判据：**记账用官方 API**；框架数字只作相对比较。
- **提升层**：工作流（管道记账）。

## token 模块性价比验证：固定推理预算下 vanilla actor 匹配 skill/memory 模块——上线前先测模块值不值其 token 成本（来源：arXiv《Are Online Skill and Memory Modules Always Worth Their Tokens? A Budget-Constrained Study of Web Agents》2606.15017（**under a fixed total inference budget, a token-matched vanilla actor matches or surpasses AWM（agentic workflow module）、ASI（agentic skill module）and memory modules across three WebArena domains and three models**）2026 实拉；与 §工具管道开销（同轮 ④）分工——那边管"已知管道的账怎么记"，本条管"新增模块前先验证性价比"）
模块先验证：固定预算下 vanilla 基线可能平手，上线前先做 token 等价对照。
- **基线对照**：**token 等价的 vanilla actor 匹配或超越 skill/memory 模块**（arXiv 原文）→ 判据：**先跑 vanilla 基线**；模块要赢过同预算裸 actor 才上线。
- **预算约束**：**在固定总推理预算下比较**（arXiv 原文）→ 判据：**预算固定再比**；不拿无限预算比性价比。
- **提升层**：工作流/可复用 Skill（性价比验证）。

## 压缩点经验数据：LangWatch 873 次中位数 pre 574,875/post 65,588/summary 4,382（~58% 窗口触发、压后 ~6.5%）；Claude Code effective window = modelWindow - min(maxOutput,20000)（来源：LangWatch《Finding the Optimal Context Window》2026-08（**873 compactions 中位数：post-compaction context 65,588 / compaction summary 4,382 / pre-compaction window 574,875**）+ JavaGuide《Claude Code 上下文管理详解》2026-07（**getEffectiveContextWindowSize(modelWindowSize, maxOutputTokens) = modelWindowSize - min(maxOutputTokens, 20000)——预留 summary 空间，返回值用于警告/自动压缩/阻塞判断**）2026 实拉；与 §实测预算设定（同轮 ①）分工——那边管"预算总量"，本条管"压缩动作的经验触发点与压后形态"）
压缩先定锚：触发点用实测分位，压后形态有基准，预留 summary 空间。
- **触发与压后**：**pre 574,875（~58% 窗口）触发、post 65,588（~6.5%）+summary 4,382**（LangWatch 原文）→ 判据：**58% 不是 80%**；压后留 ~6.5% 是常见形态。
- **有效窗口公式**：**modelWindow - min(maxOutput, 20000)**（JavaGuide 原文）→ 判据：**预留输出/summary 空间**；窗口满打满算必翻车。
- **提升层**：工具/可复用 Skill（压缩锚点）。
## fallback 链与降级路径：fallback_tools per-agent 有序降级 · search rate-limit→cached index · DB 不可达→stale 数据+新鲜度警告 · 快端点超时→慢可靠端点 · 确定性后备层（rule-based/人工审查队列）防级联（来源：GenAI Club《Keep an AI Agent Reliable When Its Tool Calls Fail》（**web search rate-limits → fall back to cached index；database unreachable → return stale data with a freshness warning；CrewAI v0.9（2026-03）引入 fallback_tools 参数——per-agent degradation chains，fallbacks 定义在 agent 层**）+ ToolWithFallbacks（**主工具包有序 fallback 备选：primary stock API down→try different provider；fast endpoint times out→fall back to the slower but more reliable one**）+ DeepUseCase（**many guides skip the fallback layer：AI 返回 nonsense 或 rate limit 时工作流应有确定性 backup（rule-based reply 或 manual review queue），否则单个坏响应级联成 angry customers**）2026 实拉；与 §断路器三态（同轮 ③）分工——那边管"故障时快速失败"，本条管"失败后降级到哪/怎么降级"）
降级先有序：fallback 链定义在 agent 层，缓存/陈旧+警告是合法降级，确定性后备防级联。
- **有序链**：**fallback_tools per-agent；主 API 挂→换 provider；快端点超时→慢可靠端点**（CrewAI+ToolWithFallbacks 原文）→ 判据：**降级有序**；不是随机换。
- **陈旧+警告**：**DB 不可达→返回 stale data+新鲜度警告；search rate-limit→cached index**（GenAI 原文）→ 判据：**陈旧数据可接受但要标注**；静默陈旧是骗人。
- **确定性后备**：**AI 返回 nonsense 或 rate limit→rule-based reply/人工审查队列；防单个坏响应级联**（DeepUseCase 原文）→ 判据：**有兜底层**；无兜底=级联风险。
- **提升层**：工作流/可复用 Skill（降级路径）。

## 静默失败检测与三层诊断：post-tool 评审（ACCOMPLISHED/PARTIALLY/NOT）· 失败先诊断层（decision/schema/execution）再修 · 重试带错误反馈（错误喂回模型再试一次，模型常能自我纠正）（来源：arXiv《ALTK: Reusable Middleware Components for Robust AI Agents》2603.15473（**Silent Error Review 组件在 post-tool 阶段用提示式方法评审工具响应为 ACCOMPLISHED / PARTIALLY ACCOMPLISHED / NOT ACCOMPLISHED——识别静默失败**）+ Neural Base《Function Calling Theory Advanced》（**function-calling 失败发生在 decision layer / schema layer / execution layer——必须先诊断哪层再修**）+ The Tool Call Problem（**工具调用校验失败时，把错误喂回模型重试一次值得做——models often self-correct when told specifically what went wrong；graceful degradation instead of raising（Google ADK：返回 ToolFailureResponse 告诉模型停用该工具换方法）**）2026 实拉；与 §handler 分工（同轮 ②）分工——那边管"错误怎么传"，本条管"静默失败怎么发现+修哪层"）
静默先评审：工具结果过三态评审，失败先定层，重试带反馈。
- **三态评审**：**post-tool 评审工具响应：ACCOMPLISHED/PARTIALLY/NOT**（ALTK 原文）→ 判据：**结果过评审**；无评审=静默失败漏网。
- **三层诊断**：**decision/schema/execution 先定层再修**（Neural Base 原文）→ 判据：**先诊断层**；修错层白修。
- **反馈重试**：**校验失败把错误喂回模型再试一次（模型被告知具体错哪常自我纠正）；重试超限 graceful degradation（停用该工具换方法）而非 re-raise**（The Tool Call Problem+ADK 原文）→ 判据：**带反馈重试**；裸重试重复同错。
- **提升层**：工具/可复用 Skill（静默失败治理）。

## 最小韧性栈与无限重试防护：retry+backoff→jitter→显式 timeout→DLQ 顺序加 · 重试持续失败→停止该记录+送 DLQ（防无限重试冻结管线）· retry policy 放编排层非各工具内部 · 实测：可靠性模式成功翻倍/人工升级 66%→23%（来源：Supergood《When Agents Fail: Retry Logic, Circuit Breakers, and Dead Letter Queues》（**最小韧性栈按 impact-to-effort 排序：先 retry+backoff（最高杠杆，可一个下午加完，每个外部 API 调用包括 LLM provider 都配）→加 jitter→显式 timeout→加 DLQ（哪怕简单实现）**）+ NanoGPT《Fault Tolerance in AI Pipelines》（**模型重试持续失败→停止处理该记录，否则无限重试循环冻结管线阻塞下游；送 DLQ 或二级存储供后续审查——一个畸形事件不拖垮整条管线**）+ softwareengineer.vn《Tool Calling Reliability》（**retry policy 应在 orchestration layer 而非各工具内部；timeout budget/idempotency key/approval gate/human handoff 实战**）+ Effloow（**实测：naive（无模式）成功 34%/100、加 retry backoff+loop detection+timeout budgets 后接近翻倍；human escalations 66%→23%（减少三分之二）**）2026 实拉；与 §fallback 链（同轮 ④）分工——那边管"降级到哪"，本条管"韧性栈的顺序与重试终点"）
韧性先排序：retry+backoff→jitter→timeout→DLQ，重试有终点，policy 在编排层。
- **栈顺序**：**retry+backoff 最高杠杆→jitter→显式 timeout→DLQ**（Supergood 原文）→ 判据：**按顺序加**；先 retry 后 DLQ。
- **重试终点**：**持续失败→停止该记录+送 DLQ；防无限重试冻结管线**（NanoGPT 原文）→ 判据：**有终点**；无限重试=冻结。
- **policy 位置**：**编排层统一配 retry（非各工具内部）；timeout budget/idempotency key/approval gate/human handoff**（softwareengineer.vn 原文）→ 判据：**集中编排**；散在工具里不可治理。
- **实测**：**可靠性模式成功近翻倍、人工升级减三分之二**（Effloow 原文）→ 判据：**投资有据**；不是玄学。
- **提升层**：工作流/可复用 Skill（韧性栈）。
## 缓存读成本治理：cache read 价降 60%、read rate 从 1/10 降到 1/20 输入价——缓存读越来越便宜是成本重点 · cachedInputPer1M 缓存感知成本估计 · 缓存策略三层（provider-native/exact-match/semantic cache）+cache ROI 建模（来源：Anthropic《What a task costs on Opus 5.5》（**Opus 5.5：input/output tokens 比 Opus 5 便宜 20%；cache reads 便宜 60%；read rate 从输入价 1/10 降到 1/20**）+ model-router CHANGELOG（**model catalog 增加 cachedInputPer1M 字段做 cache-aware cost estimation**）+ LLM Cost Engineering《Chapter 5 Caching Strategies》（**provider-native cache / exact-match cache / semantic cache 三层；cache hit-rate optimization；cache ROI modeling**）2026 实拉；与 r629A 既有 §工具管道开销实测 分工——那边管"记账口径"，本条管"缓存读这个成本项怎么算怎么省"）
缓存先算价：cache read 越来越便宜（1/20 输入价），选型/记账要 cache-aware。
- **read 降价**：**cache reads 降 60%、read rate 从 1/10 降到 1/20 输入价——缓存读成本占比持续下降，是成本治理重点**（Anthropic 原文）→ 判据：**缓存读按新 rate 记账**；沿用旧率高估成本。
- **cache-aware 估计**：**model catalog 加 cachedInputPer1M；大缓存上下文偏好便宜输入模型**（model-router+pi-auto-model 原文）→ 判据：**选型/记账认缓存**；忽略缓存=误判贵贱。
- **三层缓存**：**provider-native/exact-match/semantic cache 三层；cache hit-rate 优化+cache ROI 建模**（LLM Cost Engineering 原文）→ 判据：**分层用缓存**；ROI 不划算的缓存不上。
- **提升层**：工作流/可复用 Skill（缓存成本治理）。

## 路由与验证体系：升级标准数据驱动（每档先调 output_config.effort 再上大模型）· parity 是生产问题（每池内模型 per-task eval set+mirrored production traffic 小比例真实请求新旧对比）· 路由延迟成本（rule-based <1ms/classifier 20-80ms，延迟敏感用规则或异步）（来源：Claude Architect Certification《Model Selection and Cost Routing》（**升级标准 data-driven 非 vibes；output_config.effort 每档先调再上更大模型；Haiku 4.5 便宜分类/路由、Sonnet 5 默认主力、Opus 4.8 明确 hard/high-stakes 任务**）+ DevOpsNess《Multi-Provider LLM Gateway Patterns》（**parity 是生产问题不是 eval 问题：Claude 调优的 prompt 在 GPT 上行为异常；池内每模型需要 per-task eval set（池变化重跑）+mirrored production traffic（新模型成 fallback 前把一小比例真实请求同时发给新旧打分对比）**）+ llm-academy《LLM Model Routing》（**rule-based 路由 <1ms；classifier-based 20-80ms——延迟敏感用规则或异步跑分类器**）2026 实拉；与 §分级路由（同轮 ①）分工——那边管"分档标准"，本条管"路由上线的验证与运行开销"）
验证先到位：升级有数据标准，换模型过 parity 验证，路由延迟按形态选。
- **数据驱动升级**：**升级标准 data-driven；每档先调 output_config.effort 再上更大模型**（Claude Architect 原文）→ 判据：**先调 effort**；调完不够再升级。
- **parity 验证**：**prompt 在 A 模型调优在 B 上行为异常；每池内模型 per-task eval set+mirrored traffic（新模型成 fallback 前小比例真实请求新旧对比打分）**（DevOpsNess 原文）→ 判据：**上线前镜像对比**；直接换=生产事故。
- **路由延迟**：**rule-based <1ms vs classifier 20-80ms；延迟敏感用规则或异步分类**（llm-academy 原文）→ 判据：**按延迟选路由形态**；实时场景别用同步分类。
- **提升层**：工作流/可复用 Skill（路由验证体系）。

## 升级/回退与按步骤选模型：confidence scoring 升级（低成本模型先答→置信度评估器不够好自动升级）· 默认 V3 只在答错花真钱的步骤引入 R1（按步骤选模型）· 混合比例基线（70% Haiku/20% Sonnet/8% Opus/2% Fable——其他是 routing bug）· validation in code not in another model call（校验用代码不用模型）（来源：n8n workflow《Route AI queries cost-efficiently with GPT-4o-mini, GPT-4o and confidence scoring》（**先由便宜模型处理→confidence-scoring AI agent 评估响应质量→不足则自动升级到高质量模型**）+ Activepieces《DeepSeek R1 vs V3 for Business》（**默认 V3，只在答错会花真钱/漏风险的步骤引入 R1——按步骤选模型**）+ ai-portal《Claude Code Model Routing》（**正确答案是混合：70% Haiku/20% Sonnet 5/8% Opus 4.8/2% Fable 5——其他都是 routing bug；跨文件/系统/数小时的任务才升级 Opus**）+ Ramon《Model routing with OpenRouter and DeepSeek》（**validation 放代码里不放在另一个模型调用里**）2026 实拉；与 §分级路由（同轮 ①）分工——那边管"任务类型→档"，本条管"动态升级/回退与步骤级选型"）
升级先设计：置信度评估决定升级，默认档+按步骤引入强档，校验放代码。
- **confidence 升级**：**便宜模型先答→置信度评估→不足自动升级强模型**（n8n 原文）→ 判据：**先便宜后升级**；评估器把关。
- **按步骤选型**：**默认 V3/R1 只用于答错花真钱的步骤；跨文件/系统/数小时的任务才升级 Opus**（Activepieces+ai-portal 原文）→ 判据：**步骤级选型**；全链强模型=浪费。
- **混合基线**：**70/20/8/2（Haiku/Sonnet/Opus/Fable）是合理默认；其他比例是 routing bug**（ai-portal 原文）→ 判据：**先按基线**；异常比例=审计。
- **校验在代码**：**validation in code not in another model call；便宜模型可能静默劣化（定期抽查真实样本，不只信 JSON 能解析）**（Ramon 原文）→ 判据：**校验不调模型**；静默劣化靠抽查。
- **提升层**：工具/工作流（升级回退设计）。
## 吞吐与显存优化参数：Ollama OLLAMA_NUM_PARALLEL=4+OLLAMA_MAX_LOADED_MODELS=2 饱和 GPU 批容量 · vLLM --max-num-batched-tokens 8192 --max-num-seqs 256 --gpu-memory-utilization 0.9 · llama-server -fa flash attention（需 Hopper/Ada/Apple Silicon）· 多卡张量并行 --tensor-parallel-size 4 跑 32B（来源：Markaicode《Quantized Serving with Ollama》（**OLLAMA_NUM_PARALLEL=4 与 OLLAMA_MAX_LOADED_MODELS=2 饱和 GPU 批容量；用 ollama ps 监控延迟**）+ DEV《Ollama, llama.cpp, vLLM Comparison》（**llama-server -fa flash attention 需 Hopper/Ada/Apple Silicon；vLLM --max-num-batched-tokens 8192 --max-num-seqs 256；AWQ/GPTQ 量化+--gpu-memory-utilization 0.9**）+ 王玉祥《本地化部署》（**vLLM 单卡 DeepSeek-R1-Distill-Qwen-7B --port 8000；多卡张量并行 --tensor-parallel-size 4 跑 32B**）2026 实拉；与 §量化决策树（同轮 ③）分工——那边管"怎么压模型"，本条管"压完怎么跑满"）
吞吐先给参数：引擎级并发/批/显存参数直接决定跑多快。
- **Ollama 并发**：**OLLAMA_NUM_PARALLEL=4 + OLLAMA_MAX_LOADED_MODELS=2 饱和 GPU 批容量**（Markaicode 原文）→ 判据：**本地并发改环境变量**；不够再加。
- **vLLM 批量**：**--max-num-batched-tokens 8192 --max-num-seqs 256；量化模型配 --gpu-memory-utilization 0.9**（DEV 原文）→ 判据：**生产调批容量**；显存利用 90% 封顶。
- **多卡扩展**：**--tensor-parallel-size 4 跑 32B；单卡 7B 直接 --port 8000**（王玉祥原文）→ 判据：**模型超单卡显存上张量并行**；7B 单卡即可。
- **提升层**：工具/工作流（吞吐优化）。

## air-gapped/隐私部署路径：install.sh --local ollama.tgz+本地 GGUF+ollama create -f Modelfile（离线完整栈）· Llama 容器无需 call home 许可证验证 · MLX 原生 Anthropic 兼容 API drop-in（Gemma 4 31B/Qwen 3.5 122B）· 本地-云端路由信号（sensitivity/task type/volume/complexity——敏感走本地、高复杂度走云端）（来源：Markaicode《Air-Gapped AI Stack》（**install.sh --local ollama.tgz 离线装；本地 GGUF 转移后 ollama create llama3-8b-q4 -f Modelfile 加载——无网络完整栈**）+ Activepieces airlines blog（**Llama 3 容器无需 call home 许可证验证——可在 air-gapped/受限网络运行；非生产 PII 数据流先测试**）+ LobeHub claude-code-local-mlx（**MLX 原生推理服务器实现 Anthropic 兼容 API，Claude Code 客户端 drop-in 指向 localhost:8000；支持 Gemma 4 31B/Qwen 3.5 122B ~65 tok/s**）+ n8n blog《Self-Hosted vs Cloud Routing》（**用 sensitivity flag/task type/request volume/complexity score 做路由信号**）+ Activepieces self-hosting（**OLLAMA_ORIGINS 环境变量配 web 访问；openai-custom 连自托管端点**）2026 实拉；与 §本地引擎选型（同轮 ①）分工——那边管"正常联网怎么搭"，本条管"离线/隐私怎么搭+怎么分流"）
隐私先设计：air-gapped 有完整栈，敏感流量走本地、复杂任务走云端。
- **离线完整栈**：**install.sh --local + 本地 GGUF + ollama create -f Modelfile——无网络可跑**（Markaicode 原文）→ 判据：**离线环境照常部署**；不用联网验证。
- **无 call home**：**Llama 容器无需许可证验证——受限网络可运行**（Activepieces 原文）→ 判据：**选无电话回家依赖的开源容器**；企业内网可用。
- **MLX drop-in**：**Apple Silicon 原生 Anthropic 兼容 API，Claude Code 客户端直接指向 localhost**（LobeHub 原文）→ 判据：**Mac 用户本地跑 Claude Code 客户端**；零代理层。
- **本地-云端分流**：**sensitivity flag/task type/volume/complexity 做路由信号——敏感走本地、高复杂度走云端**（n8n 原文）→ 判据：**按数据敏感度分流**；不是全本地也不是全云端。
- **提升层**：工作流/可复用 Skill（隐私部署）。

## 本地部署监控与成本账：自托管规模省成本（vs API 定价）· 监控正确指标（latency p95 非平均）· 模型体积选择（qwen2.5 4.7GB 多数机器 vs Llama 405b 243GB——按硬件选 7B 起步）· 微调工具调用路径（JSONL 20% 负样本→LoRA 7B 30-45min→Ollama→50 条真消息测试再切生产）（来源：Zero to AI《05 LLM Server And API》（**自托管在规模上相对 API 定价显著省钱；监控 latency p95 而非平均**）+ Langflow《Local AI Using Ollama with Agents》（**qwen2.5 4.7GB 多数机器可跑 vs Llama 3.1 405b 243GB；按机器选模型大小**）+ Dify DeepSeek 部署（**7B 起步；参数越多质量越高但内存要求越高**）+ Ertas AI《Fine-Tuned Tool Calling》（**JSONL 正确 tool-call 结构+20% 负样本→LoRA 微调 7B 30-45 分钟→Ollama 部署→50 条真实消息测试再切生产流量**）2026 实拉；与 §air-gapped（同轮 ⑤）分工——那边管"哪里能跑"，本条管"值不值得跑+跑起来怎么验"）
本地先算账：规模省钱、监控 p95、模型按硬件选、微调先测再切。
- **成本账**：**自托管规模相对 API 定价显著省钱**（Zero to AI 原文）→ 判据：**量大才自托管**；量小省不回运维成本。
- **监控指标**：**监控 latency p95 而非平均**（Zero to AI 原文）→ 判据：**看尾延迟**；平均会掩盖长尾卡顿。
- **体积选择**：**qwen2.5 4.7GB 多数机器可跑 vs 405b 243GB；7B 起步，参数越多质量越高内存要求越高**（Langflow+Dify 原文）→ 判据：**按硬件选体积**；小机器 7B 起步。
- **微调路径**：**JSONL 工具调用结构+20% 负样本→LoRA 微调 7B（30-45min）→Ollama→50 条真实消息测试再切生产**（Ertas AI 原文）→ 判据：**小模型微调做工具调用**；测满 50 条再切。
- **提升层**：工具/工作流（成本与验证）。
## 编排模式升级路径与终止条件：sequential pipeline 起（定义/可重复）→ supervisor/worker（动态分解）→ HITL/kanban（真实世界后果或 EU AI Act 人类监督）· 终止条件（TextMentionTermination("APPROVED")+max_turns=10；Swarm 生产环境硬性轮数上限）· AG2 adapter 形态（consulting 自动关闭/conversation 显式 close/TTL/discussion round-robin）（来源：Knowlee《Orchestration Guide 2026》（**Start with Pattern 1 sequential pipeline for defined repeatable workflows；Upgrade to Pattern 2 supervisor/worker when tasks require dynamic decomposition；Add Pattern 5/6 HITL or kanban when outputs trigger consequential real-world actions or EU AI Act human-oversight requirements apply**）+ Qantcore（**RoundRobinGroupChat：termination=TextMentionTermination("APPROVED")；participants=[critic, optimizer, arbiter]；max_turns=10——Group Chat 每 agent 说一轮，靠终止条件停**）+ AG2 Action-Driven Network（**Adapter 形态：consulting 1↔1 单轮 ask→answer 自动关闭；conversation 1↔1 自由形式显式 close() 或 TTL；discussion N 参与 round-robin 显式 close() 或 TTL**）+ MESHLAUNCH（**Swarm 生产环境慎用须设硬性轮数上限**）2026 实拉；与 §多 agent 三规则（r630B ①）分工——那边管"选哪种形状"，本条管"从哪开始+怎么停"）
编排先定路径与终止：从 pipeline 起、升级按需、终止条件必须显式。
- **升级路径**：**sequential pipeline 起（定义/可重复）→ supervisor/worker（动态分解）→ HITL/kanban（真实世界后果或 EU AI Act 人类监督）**（Knowlee 原文）→ 判据：**从简单起**；输出影响现实才上 HITL。
- **终止条件**：**TextMentionTermination("APPROVED")+max_turns=10；Swarm 生产须硬性轮数上限**（Qantcore+MESHLAUNCH 原文）→ 判据：**对话有终止词+轮数上限**；否则无限循环。
- **通信形态**：**consulting 单轮自动关闭；conversation 显式 close/TTL；discussion round-robin 显式 close/TTL**（AG2 原文）→ 判据：**按协作形态选 adapter**；对话型必须有关闭机制。
- **提升层**：工作流（编排路径与终止）。

## Sub-agents 嵌套与上下文隔离：Dify 嵌套 agent 节点（agent 把 agent 当 tool）· n8n AI Agent Tool（orchestrator 把 sub-agent 配成 tool）· Make Sub-Agents（一个收任务选专家返回结果无硬编码 handoff）· 子工作流封装专业 Agent（参数接口通信·上下文彻底隔离·可复用·并行）· 首尾相连否则线性工作流·agent 名称与适用场景明确设定（来源：DEV《5 Hidden Uses of Dify》（**Dify v1.3+ 支持嵌套 agent 节点——一个 agent 把另一个当 tool 调用，跨专业 LLM 角色的 emergent behavior**）+ 华为云《Dify 多智能体协同编排实战》（**方式二子工作流封装专业 Agent（推荐）：Agent 间通过参数接口通信、上下文彻底隔离、单个 Agent 可复用、支持并行调用；适合 3 个以上 Agent、需复用并行的生产级场景；方式三 HTTP 节点对接外部 Agent 服务**）+ n8n Production AI Playbook（**AI Agent Tool：把第二个 agent 配置成第一个 agent 可调用的 tool——orchestrator 收输入决定做什么**）+ Make Sub-Agents（**把 AI Agents 作为 tools 加进其他 AI Agents——一个 agent 收任务选合适专家返回最终结果，无需硬编码 handoffs**）+ WaytoAGI 扣子（**智能体编排中首尾相连，不然成为线性工作流；单个 Agent 的名称与适用场景明确设定好以让节点跳转模型更好识别触发**）+ n8n @mentions（**@mentions 触发特定 agent 或全响应**）2026 实拉；与 §多 agent 协作纪律（r627 前）分工——那边管"共享知识层/接口契约"，本条管"具体嵌套形态与上下文隔离做法"）
嵌套先做隔离：agent 当 tool 嵌套、子工作流参数接口通信、名称场景明确。
- **嵌套形态**：**agent 把 agent 当 tool（Dify 嵌套节点/n8n AI Agent Tool/Make Sub-Agents）——一个收任务选专家返回结果无硬编码 handoff**（DEV+n8n+Make 原文）→ 判据：**agent-as-tool 是通用嵌套法**；orchestrator 选专家。
- **子工作流封装**：**参数接口通信+上下文彻底隔离+可复用+并行——适合 3+ agent 生产级**（华为云原文）→ 判据：**3+ agent 用子工作流**；隔离上下文。
- **编排连通**：**首尾相连否则线性工作流；agent 名称与适用场景明确设定**（WaytoAGI 原文）→ 判据：**节点要连成环**；命名带场景。
- **提升层**：工具/工作流/可复用 Skill（嵌套与隔离）。

## 框架选型与 2026 生态坐标：LangGraph=显式控制流状态图生产耐用（34.5M 月下载）· CrewAI=角色团队最大社区 56.9k · AutoGen/AG2=对话式+GroupChat · OpenAI Agents SDK=最轻量内置 handoffs/guardrails/tracing 100+ LLM · ADK=Google Cloud · PydanticAI=简单 agents 代码通信（Radar Adopt 比 LangGraph 精简可调试）· 80% agentic 实施时间花在数据工程与治理非框架配置（来源：Developers Digest《How to Coordinate Multiple AI Agents》（**显式控制流+可调试状态机→LangGraph；角色团队+共享内存→CrewAI；对话式协调→AutoGen/AG2；面向客户 handoff 流→OpenAI Agents SDK；Google Cloud 部署→ADK；开发工作流→Claude Code 原生 sub-agents**）+ Firecrawl（**LangGraph 企业采用领先 34.5M 月下载；Dify GitHub stars 领先 144k；Smolagents 单 agent loop 最快路径**）+ nstdata（**CrewAI 56.9k stars 最大社区；OpenAI Agents SDK 最轻量 provider-agnostic 内置 handoffs/guardrails/tracing 100+ LLM**）+ Atlan（**80% agentic AI 实施时间消耗在数据工程与治理——不是框架配置；每个框架管 agents 怎么跑，没一个管 agents 读什么**）+ agentic-ai.readthedocs（**PydanticAI Thoughtworks Radar Vol.34 Adopt：简单 agents 通过代码执行通信优于刚性图+巨大共享状态，比 LangGraph 更精简可调试**）2026 实拉；与 §多 agent 三规则（r630B ①）分工——那边管"模式>框架"，本条管"真要选框架时的坐标"）
选框架先看坐标：按协作形态选，80% 时间在数据工程不在框架。
- **形态→框架**：**显式控制流→LangGraph；角色团队→CrewAI；对话式→AutoGen/AG2；客户 handoff→OpenAI Agents SDK；Google Cloud→ADK；开发工作流→Claude Code sub-agents**（Developers Digest 原文）→ 判据：**按协作形态选**；不按名气选。
- **生态坐标**：**LangGraph 34.5M 月下载生产耐用；CrewAI 56.9k stars 最大社区；OpenAI Agents SDK 最轻量内置 handoffs/guardrails/tracing**（Firecrawl+nstdata 原文）→ 判据：**生产用 LangGraph、角色团队用 CrewAI、轻量用 SDK**。
- **真耗时**：**80% agentic 实施时间花在数据工程与治理非框架配置；框架管"agents 怎么跑"没一个管"agents 读什么"**（Atlan 原文）→ 判据：**数据工程优先投入**；别在框架选型上耗。
- **提升层**：工具/工作流（框架坐标）。
## 防 eval 说谎与过拟合：跑 N 次看 verdicts 翻转（agent-variance→修 agent；judge-flake→修 eval）· train 改善 test 平→怀疑过拟合 revert · consistency guards（tdd_green_ran=NO 强制 tdd_green_pass=NO 防 LLM 幻觉）· judge 与专家标签校验 ≥90% 一致+高风险人工抽检（evaluator 共享偏差相关失败）（来源：ciagent（**告诉你 agent 的 evals 是否在骗你：跑套件 N 次看哪些 verdicts 翻转带责任——agent-variance→修 agent；judge-flake→修 eval；审计 LLM judge**）+ Claude 自动化 eval hillclimbing（**train set 改善但 test set 平→怀疑 overfitting revert；回归→revert；train+test 都改善→keep patch**）+ claude-sdlc-harness（**consistency guards：enforce_tdd_consistency——tdd_green_ran=NO 则强制 tdd_green_pass=NO，防 LLM 幻觉**）+ aitutorialmaker（**judge 与专家标签校验：200 例评审集目标 ≥90% 一致，consequential 决策要求更高；高风险结果人工抽检——evaluator 模型共享偏差可能相关失败**）+ Anthropic Demystifying evals（**专项 evals 团队拥有核心基础设施+领域专家与产品团队贡献多数 eval 任务并自己跑；拥有迭代 evals 应像维护单元测试一样例行**）2026 实拉；与 §三层 evaluator（同轮 ⑤）分工——那边管"用哪几类 evaluator"，本条管"eval 结果可不可信+怎么迭代"）
防 eval 说谎：跑 N 次看翻转、train/test 双查、consistency guard、judge 过专家校验。
- **翻转归因**：**跑 N 次看 verdicts 翻转——agent-variance→修 agent；judge-flake→修 eval**（ciagent 原文）→ 判据：**翻转分责**；别把 judge 不稳定当 agent 失败。
- **防过拟合**：**train 改善 test 平→怀疑过拟合 revert；train+test 都改善才 keep**（Claude 原文）→ 判据：**双集判 keep**；只 train 好=过拟合。
- **防幻觉**：**consistency guards——tdd_green_ran=NO 强制 tdd_green_pass=NO**（claude-sdlc 原文）→ 判据：**未跑=未过**；防 LLM 编造通过。
- **judge 校验**：**judge 与专家标签 ≥90% 一致；高风险人工抽检（evaluator 共享偏差相关失败）**（aitutorialmaker 原文）→ 判据：**judge 先标定**；高风险人工兜底。
- **提升层**：工作流/可复用 Skill（eval 可信度）。

## 三层 evaluator 与工具调用验证：确定性检查（exact/contains/regex/numeric 免费评大部分）· LLM judge 只评自由形式 1-5 · 语义 diffing 三层叠 · record calls+assert（预期工具跑/参数精确匹配/禁止工具未调）+独立断言终态 · tool call accuracy 最可靠规划质量代理 · 版本化每个可改行为组件（prompts/model/temp/tool descriptions/retrieval indexes/rubrics）（来源：CallSphere《Semantic Diffing 三层 evaluator》（**①确定性检查便宜快精确跑每行——调了必须工具吗/延迟预算内吗/避开禁用短语；②LLM-as-judge 开放语义；③代码/custom 业务逻辑；三层叠抓长尾，任一单独都漏**）+ Qodex《AI Agent Testing》（**record calls during run 并断言：预期工具跑了、参数精确匹配、禁止工具从未调用；然后独立断言结果状态——参数好的调用仍可能留错终态**）+ AgentMarketCap（**tool call accuracy 最可靠规划质量代理，比生成指标更快抓 prompt 回归；latency/token cost 抓效率回归**）+ aitutorialmaker（**版本化每个能改变行为的组件：prompts/model identifiers/temperature/tool descriptions/retrieval indexes/policies/evaluator rubrics**）+ n8n（**确定性检查 exact/contains/regex/numeric 免费评大部分；LLM judge 只评标 llm-judge 的自由形式 1-5**）2026 实拉；与 §防 eval 说谎（同轮 ④）分工——那边管"结果可信度"，本条管"具体哪几类 evaluator 怎么组合"）
评估先分三层：确定性免费、judge 补自由形式、调用断言+终态双查。
- **三层叠**：**确定性检查跑每行（必须工具/延迟预算/禁用短语）+LLM-judge 开放语义+custom 逻辑——三层叠抓长尾**（CallSphere 原文）→ 判据：**三层都上**；单一层必漏。
- **调用断言**：**record calls 并断言（预期工具/参数精确/禁止工具）+独立断言终态**（Qodex 原文）→ 判据：**调用与终态双查**；参数好仍可能错终态。
- **版本化**：**版本化每个可改行为组件（prompts/model/temp/tool descriptions/retrieval indexes/rubrics）**（aitutorialmaker 原文）→ 判据：**行为组件入版本**；改任何一项可追溯。
- **提升层**：工具/工作流/可复用 Skill（evaluator 组合）。

## 组件级 eval 与 observability→evaluation 分工：observability 显示 run 发生什么（trace 每 model call/tool/step）· evaluation 判定结果好坏（LLM-as-judge 或 code-based 对照已知答案）· 组件级 eval（组件单独测 code-based 或 judge）→experiments 迭代 · 应用层决策≠模型决策（LLM 对但 agent 发错——回归测试抓应用决策）· Tuned evaluators 专用模型成本降 82%（来源：DeepLearning.AI《Evaluating AI Agents》（**observability 加进 agent 得步骤洞察→debug；组件级 evals：preparing testing examples+选 evaluator code-based 或 LLM-as-Judge+identify 正确指标；结构化成 experiments 迭代改进输出质量与路径**）+ Make《Agent observability 2026》（**observability 显示 run 发生什么；evaluation 判定结果好不好——LLM-as-judge 或 code-based checks 对照已知正确答案**）+ Dify（**Arize Phoenix 自动 trace 每个 model call/tool invocation/chain step；三级可观测 Single Runs→长期监控**）+ DEV《LLM 对但 agent 发错》（**recorded model decision P0 vs application decision P1——应用层决策与模型决策不一致；escalation False→True；regression test Failed→Passed；回归测试抓应用决策**）+ LangSmith Tuned Evaluators（**后训练专用模型超所有 frontier+评估成本降 82%**）2026 实拉；与 §三层 evaluator（同轮 ⑤）分工——那边管"评什么怎么评"，本条管"评测的层次结构与观测分工"）
评测先分层：observability 管"看到什么"、evaluation 管"好不好"、组件级先于整体。
- **分工**：**observability 显示 run 发生什么；evaluation 判定结果好坏（judge 或 code-based 对照已知答案）**（Make+DeepLearning.AI 原文）→ 判据：**观测与评估分开**；先看到再评判。
- **组件级**：**组件单独测（code-based 或 judge）→结构化成 experiments 迭代**（DeepLearning.AI 原文）→ 判据：**组件先于整体**；先修零件再整机。
- **应用层≠模型层**：**LLM 对但 agent 发错——应用决策与模型决策不一致，回归测试抓应用决策**（DEV 原文）→ 判据：**测应用层决策**；不只测模型输出。
- **tuned evaluator**：**后训练专用模型超 frontier+成本降 82%**（LangSmith 原文）→ 判据：**专用评测模型更省**；批量评测用 tuned。
- **提升层**：工具/工作流（评测分层）。
## 后置非 LLM 校验与三步验证：Pydantic/Zod 做最终业务验证（强制 agent 可能忽略的业务逻辑）· 三步验证（类别非空且匹配列表/规范化大小写 trim/置信度>0.7 阈值）· 验证成本 vs 错误成本（错分类 bundle 路由到错误系统清理更贵）· 写前验证+检索事实+citation 字段+高影响写 review gate · schema 字段 .describe() 帮 LLM 理解 + enum 加 'Use other if unsure' 降级说明（来源：Activepieces《Building a Reliable Harness for Multi-Agent AI Systems》（**非 LLM 层（Pydantic model）是最终验证必需——强制 agent 可能忽略的业务逻辑；类型提示强制 agent 不返回 string 当系统要 integer**）+ Activepieces《Reduce hallucinations》（**enforce structured outputs 并写前验证；用 curated Tables/API 检索事实；输出带 citations/source 字段；高影响更新加 review gate**）+ Make《Integrating LLMs into Enterprise Workflows》（**三步验证：Filter 类别非空且匹配定义值列表→Set Variable 规范化大小写 trim→Filter 置信度>0.7 阈值；验证模块消耗 credit，但错分类 bundle 路由到错误系统清理成本更高**）+ LangChain 前端结构化输出最佳实践（**schema 字段 .describe() 帮 LLM 理解每字段内容**）+ Schema 引导（**enum 加 'Use other if unsure' 降级说明**）2026 实拉；与 §结构化输出五步 recipe（execute 同轮 ①）分工——那边管"生成端分层"，本条管"输出后校验与业务规则"）
输出后必校验：非 LLM 层验证业务规则；三步验证定档；高影响写加 review gate。
- **非 LLM 层**：**Pydantic/Zod 做最终验证——强制 agent 可能忽略的业务逻辑**（Activepieces 原文）→ 判据：**验证不靠 LLM**；类型提示兜底。
- **三步验证**：**类别非空且匹配列表→规范化大小写 trim→置信度>0.7 阈值**（Make 原文）→ 判据：**结构化三查**；漏一步错一路。
- **成本权衡**：**验证模块消耗 credit，但错分类 bundle 路由到错误系统清理更贵**（Make 原文）→ 判据：**验证成本<错误成本**；别省校验。
- **写前门**：**写前验证+检索事实+citation 字段+高影响写 review gate**（Activepieces 原文）→ 判据：**高影响写人工审**；citation 可追溯。
- **提升层**：工具/工作流（输出后校验）。

## 自我纠正循环与验证失败回馈：编号验证错误喂回下一次提取直到通过或 maxAttempts · 无 parser 兜底（Switch 路由回 AI Agent 更新 prompt 重试最多 4 次防死循环）· 每平台独立 schema（不同平台字段不同）· sample data 驱动 Response structure 自动生成 · Anthropic 工具 schema 命名约束（属性名无特殊字符/≤64 字符）（来源：n8n workflow 15995（**解析模型输出验证每 action item 必填字段/截止格式/允许优先级/上下文长度；验证失败且尝试未耗尽→编号验证错误喂回下一次提取，重试到通过或 maxAttempts；返回成功或失败细节**）+ n8n workflow 4316（**无 Structured Output Parser 兜底：Switch 节点输出不匹配 schema 时路由回 AI Agent 更新 prompt 要求返回正确格式，最多 4 次防死循环；匹配则继续**）+ DEV workflowguides（**每平台独立 schema——不同平台字段不同，单独 request/schema**）+ Make Academy（**sample data 显示想要结构→Make 自动开发 Response structure 字段**）+ Make 社区（**Anthropic 工具 schema 校验：Notion 工具属性名含特殊字符或超 64 字符→400 错误**）2026 实拉；与 §后置非 LLM 校验（同轮 ④）分工——那边管"静态规则校验"，本条管"失败后怎么自动修"）
自纠先设上限：编号错误喂回重试、无 parser 用路由兜底、每平台独立 schema。
- **喂回重试**：**编号验证错误喂回下一次提取，重试到通过或 maxAttempts**（n8n 原文）→ 判据：**错误要编号**；给模型可消化的反馈。
- **路由兜底**：**无 parser 时 Switch 路由回 AI Agent 更新 prompt，最多 4 次防死循环**（n8n 原文）→ 判据：**设重试上限**；防死循环。
- **每平台独立**：**不同平台字段不同→单独 request/schema**（DEV 原文）→ 判据：**平台级 schema**；不共用错位字段。
- **命名约束**：**工具属性名无特殊字符/≤64 字符（Anthropic schema 校验 400）**（Make 社区原文）→ 判据：**schema 命名守规**；特殊字符即 400。
- **提升层**：工作流/可复用 Skill（自纠与重试）。

## 输出 schema 契约与下游免清洗：结构化输出消除 30-60% 生产 agent bug · 响应格式设置确保有效 JSON（下游免手工清洗——Google Sheets 收干净字符串+boolean）· OpenAPI 导入自动解析端点参数描述为工具 · 渲染前验证必填字段（流式可能部分数据）· 通用提取函数参数化（type+required fields 跨 schema 复用）· 渐进渲染（来源：Agentmelt《Structured Output for AI Agents》（**结构化输出消除导致 30-60% 生产 agent bug 的解析失败；用 OpenAI Structured Outputs/function calling、Anthropic tool use、Gemini JSON mode；每响应用 Pydantic/Zod 验证**）+ Activepieces（**响应格式设置确保输出有效 JSON，允许无限 flow 解析免手工清洗——Google Sheets connector 收干净 Category 字符串+Urgent boolean**）+ Dify-hosting（**OpenAPI Schema 导入自动解析全部端点/参数/描述为可用工具**）+ LangChain 前端结构化输出最佳实践（**渲染前验证必填字段存在（流式可能部分数据）；通用提取函数用 type+required fields 参数化跨 schema 复用；渐进渲染字段到达即显示**）2026 实拉；与 §Schema 设计四律（execute 同轮 ②）分工——那边管"schema 写法"，本条管"契约价值与消费端"）
输出契约先定价值：schema 消除解析失败、下游免清洗、消费端先验证后渲染。
- **价值量化**：**结构化输出消除 30-60% 生产 agent bug（解析失败）**（Agentmelt 原文）→ 判据：**解析失败是最大 bug 源**；schema 消掉。
- **下游免清洗**：**响应格式确保有效 JSON——下游收干净字段免手工清洗**（Activepieces 原文）→ 判据：**上游保结构**；下游不洗数据。
- **OpenAPI 导入**：**OpenAPI Schema 自动解析端点/参数/描述为工具**（Dify 原文）→ 判据：**契约即工具**；不手写 schema。
- **消费端**：**渲染前验证必填字段（流式部分数据）+通用提取参数化+渐进渲染**（LangChain 原文）→ 判据：**先验证后渲染**；流式按到达显示。
- **提升层**：工作流/可复用 Skill（输出契约消费）。
## agent 自我审查与代码评审基准：开 PR 前用 code review 审自己 patch（agent 抓到自己字符串拼接复杂并在 PR 前修复）· ReviewBench 219 PR 六指标（grounded precision/recall/F1+augmented；按 severity 配 evals）——测"抓真 bug"不是评论频率 · Copilot grounded recall 26%/Cursor 9.6%/最佳 44.2% · 87.8% 评论是真缺陷但只找到 26% 已知 · 多源 golden set+资深工程师 96.6% 同意验证（来源：GitHub《What's new with Copilot coding agent》（**Copilot coding agent 开 PR 前用 Copilot code review 审查自己改动、反馈迭代改进 patch——你被 tag 前已有人过一遍；实例：agent 抓到自己字符串拼接过度复杂在 PR 落地前修好**）+ GitHub《ReviewBench: An open benchmark for AI code review》（**219 PR/187 仓库/19 语言，分布对标 1.039 亿真实 PR；多源 golden set+一致 rubric+资深工程师独立验证 96.6% 同意；六指标 grounded precision/recall/F1+augmented 版本；按 severity 配置 evals；数据集/judge prompt/runner MIT 开源**）+ AICoder 报道（**grounded recall：Copilot(Balanced) 26.0%/Devin 23.8%/Qodo 22.1%/Cursor 9.6%；Claude Sonnet 5 当 judge**）+ Devlery（**Copilot 87.8% 评论是真实缺陷但只找到 26% 已知缺陷；critical defects Codex 81 vs Copilot 63**）+ CodeReviewBench（**最佳模型找到 44.2% bug（DeepSeek V4 Pro recall 44.2% precision 43.6% $0.30/PR）**）2026 实拉；与 §多 agent 协作纪律（r629 前）分工——那边管"编排协作"，本条管"评审自身的质量度量"）
评审先定度量：grounded recall 测抓真 bug 非评论频率；agent 开 PR 前自我审查。
- **自我审查**：**开 PR 前 code review 审自己 patch——被 tag 前已有人过一遍**（GitHub 原文）→ 判据：**PR 前自审**；把自纠放进工作流。
- **基准**：**219 PR/19 语言/分布对标 1.039 亿 PR；六指标 grounded precision/recall/F1+augmented；按 severity 配 evals；MIT 开源**（ReviewBench 原文）→ 判据：**测抓真 bug**；不是评论频率。
- **现实水位**：**Copilot grounded recall 26%/Cursor 9.6%/最佳 44.2%；87.8% 评论是真缺陷但只找 26% 已知**（各报道原文）→ 判据：**评审 agent 是助手非替代**；人审仍必需。
- **提升层**：工具/可复用 Skill（评审度量与自审）。

## hooks 验证门与批准门 + 科学辩论破锚定：PostToolUse hooks 作验证门（exit code 2 把发现喂回模型）· PreToolUse 批准门（allow/deny/ask 人工；hooks 在 agent 行动处运行→规则处处成立）· 重复工作转 subagents（.claude/agents/*.md name/何时用/可触碰工具；simplifier/verifier/researcher）· Agent teams 科学辩论破锚定（5 agent 互相证伪，幸存理论更可能真根因——顺序调查有锚定偏差）· Kairos 26 条结构规则校验→违规送 Claude 纠正 3 次→strip 服务端字段（来源：Anthropic《Claude Code Advanced Patterns》（**修 bug 前先写失败测试复现；describe/it 块不用 test；除非测外部 API 避免 mock；改动后总跑相关测试文件；agent 团队评审按严重度评 inline comments**）+ Codex 案例（**PostToolUse hooks 验证门 exit code 2 喂回**）+ Claude Code hooks 文档（**PreToolUse 每次工具调用前 allow/deny/ask 人工；hooks 在 Claude 行动处运行→规则在终端处处成立**）+ Anthropic agent teams 文档（**5 agent teammate 调查不同假设互相反驳如科学辩论；辩论结构是关键机制——顺序调查有锚定偏差，多独立调查者互相证伪幸存理论更可能真根因**）+ Kairos SDK（**workflow 26 条结构规则校验（node IDs/types/versions/names/positions/connections/forbidden fields/trigger presence/AI connection direction/cycle detection/webhook pairing/required parameters）→失败具体违规送回 Claude 纠正最多 3 次（末轮温度更紧）→strip 服务端字段**）2026 实拉；与 §定时任务记账（r629 前）分工——那边管"排期语义"，本条管"执行生命周期闸门"）
执行闸门先双设：PostToolUse 验证门喂回失败、PreToolUse 批准门人工把关。
- **双门**：**PostToolUse 验证门（exit code 2 喂回发现）+PreToolUse 批准门（allow/deny/ask）**（Codex+Claude Code 原文）→ 判据：**门设在行动处**；规则处处成立。
- **subagents 分工**：**simplifier（主 agent 完成后去复杂度）/verifier（跑应用查行为）/researcher（探索 codebase 不 flooding 主上下文）**（Anthropic 原文）→ 判据：**按职责拆**；防上下文淹没。
- **辩论破锚定**：**5 agent 独立调查互相证伪——顺序调查有锚定偏差，幸存理论更可能真根因**（Anthropic 原文）→ 判据：**多独立证伪**；别顺序钻一个方向。
- **结构校验**：**26 条规则校验→违规送模型纠正 3 次→strip 服务端字段**（Kairos 原文）→ 判据：**规则可数**；纠正设上限。
- **提升层**：工具/工作流/可复用 Skill（执行闸门）。

## 代码沙箱与人工门控 + 审查与任务粒度：Code Execution 沙箱 daemon 隔离执行（防代码执行危及主 API 服务）· 直接编辑文件=需要权限系统+git 分支可 revert · Tools Agent 人工审批门控工具（AI 想用门控工具时 workflow 暂停发审批请求）· 以维护者身份审查（读最终 diff；正常用户流+至少一种错误情况+测试覆盖要求行为）· 小任务（一次一个函数/组件；大而模糊请求产出难维护代码）· 安全清单（secrets hardcoded/input validate sanitize/SQL injection/auth 所有端点）（来源：Dify Code Execution Node（**沙箱服务独立 daemon 端口 5003 隔离执行环境——防止代码节点执行危及主 API 服务**）+ code.live（**直接编辑文件？只有有权限系统+git 分支可 revert 才允许**）+ n8n Tools Agent（**Human review for tool calls：AI 想用门控工具时 workflow 暂停发审批请求，接收人 approve 工具执行/deny 取消——approval channel Chat/Slack/Telegram**）+ Kimi AI 编程工作流（**以维护者身份审查 AI 代码：读最终 diff；正确性=满足验收标准+正常用户流+至少一种错误情况+测试覆盖要求行为**）+ Akousa（**一次一个函数/组件/query/示例；大而模糊请求产出难维护代码；行为测试覆盖正常/边界/空/无效/失败路径；美化代码仍可错**）+ Developer Awam 安全清单（**secrets hardcoded？input validate sanitize？SQL injection？auth 所有端点？**）2026 实拉；与 §约束解码（r631A 同轮 ③）分工——那边管"输出结构约束"，本条管"执行环境与人工把关"）
代码执行先隔离：沙箱独立 daemon、门控工具人工审批、任务拆小。
- **沙箱隔离**：**Code Execution 沙箱独立 daemon 端口隔离——防代码节点危及主 API 服务**（Dify 原文）→ 判据：**执行与主服务隔离**；代码节点不碰主进程。
- **人工门控**：**门控工具调用时 workflow 暂停发审批请求，approve 才执行**（n8n 原文）→ 判据：**高影响工具门控**；暂停等待人。
- **维护者审查**：**读最终 diff；正确性=满足验收+正常流+至少一错误情况+测试覆盖**（Kimi 原文）→ 判据：**以维护者身份看**；不替 AI 打钩。
- **任务粒度**：**一次一个函数/组件；大而模糊请求产出难维护代码；美化≠正确**（Akousa 原文）→ 判据：**小步拆**；漂亮也要测。
- **安全清单**：**secrets hardcoded/input validate sanitize/SQL injection/auth 所有端点**（Developer Awam 原文）→ 判据：**安全四查**；AI 代码同样过。
- **提升层**：工具/工作流（执行环境与把关）。
## RAG 数据工程三纪律：600-1000 tokens 递归 chunking 起步（语义 chunking 复杂度你可能还不需要）· 混合检索 vector+BM25（纯向量漏精确词：错误码/产品名/API 端点）· 分开测检索质量与生成质量（坏检索不能用更好 LLM 修）· 从第一天建增量 ingestion（全量重索引难扩）· 生产阈值 faithfulness>0.85/answer relevancy>0.8/context precision>0.75/context recall>0.8（来源：aiwisdom《Designing RAG Systems That Actually Scale》（**600-1000 tokens 递归 chunking 起步——语义 chunking 增加复杂度可能不需要；总是混合检索 vector+BM25——纯向量漏精确词错误码/产品名/API 端点；分开测检索质量和生成质量——坏检索不能用更好 LLM 修；从第一天建增量 ingestion——全量重索引难扩**）+ metafiedlab（**生产阈值 faithfulness>0.85/answer relevancy>0.8/context precision>0.75/context recall>0.8**）2026 实拉；与 §知识库工程（r629 前）分工——那边管"向量+关键词双路召回/分块"，本条管"工程化阈值与增量"）
RAG 先立纪律：chunk 起步递归 600-1000、检索必须混合、质量分测、增量先行。
- **chunk 起步**：**600-1000 tokens 递归切——语义 chunking 复杂度可能不需要**（aiwisdom 原文）→ 判据：**递归起步**；语义切按需上。
- **混合检索**：**vector+BM25——纯向量漏精确词（错误码/产品名/API 端点）**（aiwisdom 原文）→ 判据：**双路召回**；精确词靠 BM25。
- **分测质量**：**检索质量与生成质量分开测——坏检索不能用更好 LLM 修**（aiwisdom 原文）→ 判据：**先修检索**；LLM 不背检索锅。
- **增量先行**：**从第一天建增量 ingestion；全量重索引难扩**（aiwisdom 原文）→ 判据：**增量架构**；别等全量爆炸。
- **阈值**：**faithfulness>0.85/answer relevancy>0.8/context precision>0.75/context recall>0.8**（metafiedlab 原文）→ 判据：**阈值量化**；上线前对齐。
- **提升层**：工具/工作流/可复用 Skill（RAG 工程）。

## 语义切片与元数据：按语义边界切片（标题层级自然分段+段落内句子边界；最小 200 最大 1000 超上限按句二切）· 切片携带来源元数据（文件名/章节标题/页码/修改日期）· chunk 级去重精确+近重复（重复膨胀检索分数）· 剥离 boilerplate+contextual retrieval 每 chunk 加 context prefix · 什么时候不用 RAG（小静态语料塞 system prompt/实时数据调工具 API/会话状态存 session store/结构化查询用 Text-to-SQL）（来源：袋鼠云《AI Agent RAG 企业知识库构建实战》（**按语义边界切片：标题层级自然分段+段落内句子边界，最小 200 字符最大 1000 字符，超上限按句子边界二次分割；切片携带来源信息——文件名/章节标题/页码/修改日期**）+ Future AGI《RAG Architecture 2026》（**索引前三检查：chunk 级去重精确+近重复——重复膨胀检索分数；剥离 boilerplate（footers/navigation）使 chunk 含真实内容；Anthropic-style contextual retrieval 每 chunk 加 context prefix**；**什么时候不用 RAG：小静态语料塞进 system prompt/实时数据（股价/传感器/天气）调工具 API——索引实时数据保证陈旧/会话状态存 session store 不存向量索引/结构化查询用 Text-to-SQL agent**）+ 匠人学院（**RAG 管道：clean+normalize→chunk by structure→add metadata（source/owner/time/ACL/version）→create embeddings→vector/hybrid index→retrieval+rerank**）2026 实拉；与 §RAG 三纪律（同轮 ④）分工——那边管"全局纪律"，本条管"切片细节与适用边界"）
切片先定界：语义边界切、元数据随身、索引前去重剥壳、知道何时不 RAG。
- **语义切片**：**标题层级分段+句边界切；最小 200 最大 1000，超上限按句二切**（袋鼠云原文）→ 判据：**语义单元完整**；上下限硬性。
- **元数据**：**每切片带文件名/章节标题/页码/修改日期**（袋鼠云原文）→ 判据：**来源可溯**；cite 有据。
- **索引前检查**：**chunk 级去重（精确+近重复——重复膨胀检索分数）+剥离 boilerplate+contextual prefix**（Future AGI 原文）→ 判据：**先净再索引**；重复会作弊。
- **不用 RAG 清单**：**小静态语料塞 prompt/实时数据调 API/会话状态存 session store/结构化查询 Text-to-SQL**（Future AGI 原文）→ 判据：**按数据形态选路**；不硬上 RAG。
- **提升层**：工作流/可复用 Skill（切片与边界）。

## prompt 缓存工程与客户端-服务端对齐：缓存边界先于语义逻辑组织 prompt（结构静态内容早、波动内容晚；系统提示词结构首先由缓存边界决定，其次才是语义逻辑）· 一 breakpoint 稳定前缀+尾部工具结果 breakpoint 每轮清除重放 · cache-aware rolling buffer keep_n=3 interval=25 旧截图占位符替换 · 服务端 150k compaction+客户端截断对齐（否则为服务器已不需要的 token 付费+破坏缓存稳定前缀）· 缓存 1.25x base 写价（来源：Bojie Li《从 Claude Code 看 Harness Engineering》（**系统提示词组织结构首先由缓存边界决定，其次才是语义逻辑——大部分人按语义分段写 prompt，但生产系统里按缓存边界分段更重要；全局稳定内容-跨用户可共享 vs 会话特定内容-不缓存；DYNAMIC BOUNDARY 警告不删不改**）+ Anthropic《Best practices for computer and browser use with Claude》（**一个 cache breakpoint 在稳定前缀，三个在尾部工具结果，每轮清除重放；cache-aware rolling buffer keep_n=3 interval=25，旧截图用占位符批量替换；服务端 150k input tokens 触发 compaction+custom prompt，客户端截断保持两视图对齐；否则为服务器已不需要的 token 付费+rolling-buffer pruner 操作不同消息切片破坏缓存稳定前缀**）+ IntuitionLabs（**Anthropic 1.25x base input price 写 5 分钟缓存**）2026 实拉；与 §上下文预算管理（r629 前）分工——那边管"何时压"，本条管"缓存怎么排与两端怎么对齐"）
缓存先排结构：缓存边界定组织、静态早波动晚、客户端服务端对齐。
- **边界定序**：**系统提示词结构首先由缓存边界决定，其次语义；静态内容早波动内容晚**（Bojie Li+PDF 原文）→ 判据：**按缓存边界分段**；不按语义习惯。
- **breakpoint 布局**：**稳定前缀一 breakpoint+尾部工具结果 breakpoint 每轮清除重放**（Anthropic 原文）→ 判据：**前缀稳定、尾部逐轮重放**；缓存收益最大。
- **rolling buffer**：**keep_n=3 interval=25 旧截图占位符替换**（Anthropic 原文）→ 判据：**截图有界**；批量占位。
- **两端对齐**：**服务端 compaction 后客户端必须同步截断——否则为服务器已不需要的 token 付费+破坏缓存稳定前缀**（Anthropic 原文）→ 判据：**两视图对齐**；不同步=双输。
- **提升层**：工具/工作流（缓存工程）。
## MCP 与 A2A 分层 + 统一治理：MCP 管 agent-tool 集成（单 agent 内工具与上下文），A2A 管 agent-agent 通信协调（跨 agent 边界委派）——"MCP inside agents, A2A between agents" 互补非替代 · 2026-08-17 A2A 加入 AAIF（Linux Foundation 主导，已管 MCP/goose/OpenAI AGENTS.md）两大标准同一治理伞 · IETF AGTP 定义消息跨网络传输（AGMP=MCP/A2A/ACP 定义说什么，AGTP 定义怎么传）· MCP 97M 月 SDK 下载（来源：A2A v1.0 blog（**A2A 正式发布 v1.0 production-ready；MCP 与 A2A 解决不同层：MCP 管工具/上下文集成在单个 agent 层，A2A 管 agent 之间通信协调；实际系统两者都用：MCP inside agents, A2A between agents**）+ AAIF 整合分析（**2026-08-17 Google A2A 正式加入 Agentic AI Foundation（AAIF）——Linux Foundation 主导已治理 Anthropic MCP、Block goose、OpenAI AGENTS.md；两大 agent 标准同一治理伞**）+ IETF draft（**AGMP（MCP/A2A/ACP）定义 agent 互相说什么，AGTP（Agent Transfer Protocol）定义消息怎么跨网络移动，AGTP 作 AGMP 消息传输基板**）+ Alice Labs（**MCP 97M 月 SDK 下载；A2A GA 支持 Copilot Studio/Azure AI Foundry/Amazon Bedrock AgentCore/Vertex AI Agent Builder**）2026 实拉；与 §MCP 选型五标准（r629 前）分工——那边管"MCP 怎么选"，本条管"MCP 与 A2A 分层与治理归属"）
互操作先分层：MCP 管工具、A2A 管 agent；协议说的与传的分开。
- **分层判据**：**MCP inside agents（工具/上下文，单 agent 层）；A2A between agents（通信/协调，跨 agent 层）；互补非替代**（v1.0 blog 原文）→ 判据：**先分层面**；别用一个协议硬扛两层。
- **治理伞**：**A2A 加入 AAIF（Linux Foundation 已管 MCP/goose/AGENTS.md）——两大标准同一治理**（整合分析原文）→ 判据：**标准看治理归属**；进基金会=可持续。
- **说/传分离**：**AGMP 定义说什么（MCP/A2A/ACP），AGTP 定义怎么跨网传**（IETF 原文）→ 判据：**协议分语义层与传输层**；互操作排障先定位层。
- **提升层**：工具/工作流（互操作分层）。

## Agent 记忆选型三档与语义记忆：Mem0 纯 RAG 长对话召回成本最优 / Letta 状态化长期 agent 自带 runtime / Zep 时间准确事实追踪 · memory base（语义相似度检索最相关上下文）vs Message History（时间序取最近）vs Knowledge（静态知识）三态分工 · LangChain 显式记住指令（"That approach worked well. Update your instructions to always use that going forward."——agent 像队友记笔记更新长期指令）· 长期记忆纪律 descriptive paths/document structure/prune old data/按环境选存储（来源：Mem0 vs Letta vs Zep 2026（**Mem0 纯 RAG-like 长对话召回成本最优；Letta 状态化长期 agent 自带 runtime；Zep 时间准确事实追踪；都集成 LangGraph/CrewAI/OpenAI/Anthropic SDK，只有 Letta 自带 agent runtime**）+ Langflow memory bases（**memory base 存长期聊天历史向量化格式，按语义相似度返回最相关上下文；不同于 Message History 按时间序从 messages 表取最近消息；不同于 Knowledge 静态知识**）+ LangChain Deep Agents 记忆（**descriptive paths/document the memory structure/prune old data/开发 InMemoryStore 生产 PostgresStore 多租户 namespace factory**）+ LangChain Agent Builder（**告诉 agent 记住："That approach worked really well. Update your instructions to always use that going forward."——agent 更新长期指令像队友记笔记**）2026 实拉；与 §记忆提取四策略（r629 前）分工——那边管"提取策略与两级沉淀"，本条管"存储形态选型与三态分工"）
记忆先选型：按形态选存储（召回/状态/事实）、三态分工、显式记住指令。
- **三档选型**：**Mem0 纯 RAG 召回成本最优 / Letta 状态化自带 runtime / Zep 时间事实追踪**（对比原文）→ 判据：**按形态选**：召回/状态/时间事实。
- **三态分工**：**memory base 语义相似检索 vs Message History 时间序 vs Knowledge 静态知识**（Langflow 原文）→ 判据：**语义会话/最近会话/静态知识分开存**；一库通吃是混乱源。
- **显式记住**：**让 agent 自己更新长期指令（"That approach worked well. Update your instructions to always use that going forward."）**（LangChain 原文）→ 判据：**运行时指令演进**；像队友记笔记。
- **存储纪律**：**descriptive paths/document structure/prune old data/开发内存生产持久化多租户 namespace**（LangChain 原文）→ 判据：**命名+剪枝+环境匹配**；记忆文件是接口。
- **提升层**：工具/工作流（记忆存储）。

## 框架 State 设计纪律：state 从第一天 typed（TypedDict/Pydantic never raw dict）· node 纯函数（state→updates，副作用归 tool node 不归路由逻辑）· prebuilt ReAct agent 用到不能再用为止 · state=agent 的 notebook 设计时逐问每块数据归属 · durable execution checkpointing 每步持久化让失败 run 从已做决策恢复不重头（来源：LangGraph Thinking in LangGraph（**state 是所有节点共享的内存——agent 记录学习与决策的 notebook；设计 state 问每块数据该不该进**）+ Precision AI Academy（**state 从第一天 typed——TypedDict 或 Pydantic，never raw dict；node 尽量纯——拿 state 返回 updates，副作用归 tool node 不在路由逻辑；prebuilt ReAct agent 用到不能再用为止**）+ LangChain blog（**durable execution：模型驱动步骤不确定，checkpointing 每步持久化，失败 run 从已做决策恢复**）2026 实拉；与 §共享知识层先建（r629 前）分工——那边管"多 agent 共享层架构"，本条管"单个图/流程的 state 与 node 纪律"）
State 先设计：typed 从第一天、node 纯函数、副作用归工具层、失败可恢复。
- **typed state**：**TypedDict/Pydantic never raw dict；设计时逐问每块数据归属**（Precision+LangGraph 原文）→ 判据：**schema 先行**；raw dict 是债。
- **纯 node**：**node 拿 state 返回 updates，副作用归 tool node 不归路由逻辑**（Precision 原文）→ 判据：**路由无副作用**；可测可重放。
- **渐进用框架**：**prebuilt ReAct 用到不能再用为止**（Precision 原文）→ 判据：**默认组件先用**；不够再定制。
- **durable execution**：**模型步骤不确定，checkpointing 每步持久化，失败从已做决策恢复**（LangChain 原文）→ 判据：**恢复不重头**；持久化每步。
- **提升层**：工具/可复用 Skill（状态图工程）。
## OTel GenAI 语义约定与零代码可观测：gen_ai.* / agent.* 标准属性（模型/输入输出 token/opt-in 时完整 prompt/completions/tool calls/tool results），TTFT=gen_ai.client.operation.time_to_first_chunk · OTLP 进 Collector 采样/脱敏/导出，vendor-neutral 社区治理不绑模型不绑后端 · OBI（eBPF 内核拦截解析网络流量零 code/SDK/restart，源自 Grafana Beyla）· TraceAI 20+ 框架 drop-in instrumentors（OpenAI/Anthropic/LangChain/CrewAI/AutoGen/DSPy/Guardrails/Haystack/Vercel AI SDK）· 微软 Agent Framework OTel middleware 自动 trace agent invocations（来源：OTel GenAI 语义约定官方（**gen_ai.*/agent.* 属性已移到独立仓库 semantic-conventions-genai；gen_ai.operation.name invoke_agent/create_agent、gen_ai.agent.name、agent.description；标准记录模型/输入输出 token/opt-in 完整 prompt/completions/tool calls/tool results；vendor-neutral 社区治理，应用产生 trace/metric/可选 event 经 OTLP 进 Collector 采样/脱敏/导出到现有观测平台**）+ OBI（**eBPF-based zero-code 可观测 agent：Linux eBPF 拦截解析 app 网络流量，标准 OTel Traces/Metrics，ZERO code/SDK/restart**）+ TraceAI（**OTel-native tracing layer Apache 2.0，drop-in instrumentors 20+ 框架**）+ 微软（**Go Agent Framework OTel middleware 自动 trace agent invocations**）2026 实拉；与 §MCP/A2A 分层（r632A）分工——那边管"互操作协议"，本条管"观测标准与零代码埋点"）
观测先标准化：OTel 约定统一命名、零代码埋点、遥测独立于模型。
- **标准属性**：**gen_ai.*/agent.* 统一命名模型/token/opt-in 内容；TTFT=time_to_first_chunk**（OTel 原文）→ 判据：**按标准命名**；换后端不换埋点。
- **管道**：**OTLP 进 Collector 采样/脱敏/导出——vendor-neutral**（OTel 原文）→ 判据：**Collector 做治理**；采样脱敏在管道层。
- **零代码**：**eBPF 内核拦截零 code/SDK/restart（OBI）**（原文）→ 判据：**埋点无侵入**；改不动代码时用。
- **drop-in**：**TraceAI 20+ 框架 instrumentors；微软 middleware 自动 trace**（原文）→ 判据：**框架级一键埋点**；别手写 instrumentor。
- **提升层**：工具/工作流（观测标准化）。

## 评估按 metric 级设阈值+分品类跟踪+推理分歧监控：聚合精度太粗——faithfulness<0.88 或 answer relevance 掉 3 分即 block deploy；分品类跟踪性能——全局分数掩盖单类崩塌 · RAG 每响应 faithfulness 打分<0.7 告警 · LLM-as-judge 采样 5-10% production traces，幻觉风险分统计显著上升告警 · 监控 agent 推理分歧——cosine similarity 区分 consensus vs errors，两 agent 对同上下文不同解释=值得捕获审查的信号（来源：Logic《LLM Testing in Production: Catch Regressions》（**aggregate accuracy 太粗；阈值设在 metric 级——faithfulness<0.88 或 answer relevance 掉 3 点 block deploy；per-category 跟踪，一个区域改进不能掩盖另一区域崩塌**）+ valuestreamai（**RAG 每响应对检索上下文打分 faithfulness<0.7 告警；LLM-as-judge 采样 5-10% 生产 traces 幻觉风险分统计显著上升告警**）+ MLflow（**监控 agent 推理 traces 分歧：cosine similarity 区分 consensus 与 errors；两 agent 对同一上下文不同解释=值得捕获的信号**）2026 实拉；与 §合成数据评测三维（r631C）分工——那边管"数据质量评测"，本条管"生产响应质量门禁"）
评估先分粒度：metric 级阈值、分品类跟踪、分歧即信号。
- **metric 级**：**faithfulness<0.88 或 relevance 掉 3 分 block deploy；聚合精度太粗**（Logic 原文）→ 判据：**指标级设门**；均值会骗人。
- **分品类**：**per-category 跟踪——单类改进不能掩盖他类崩塌**（Logic 原文）→ 判据：**按类分账**；全局分掩盖局部崩。
- **采样评测**：**LLM-as-judge 采样 5-10% traces+统计显著上升告警**（valuestreamai 原文）→ 判据：**采样可持续**；全量评测烧钱。
- **分歧监控**：**cosine similarity 区分 consensus vs errors——分歧=捕获信号**（MLflow 原文）→ 判据：**分歧当信号**；一致性不等于正确。
- **提升层**：工具/工作流（评估门禁）。

## 日志-追踪关联与脱敏先行：trace_id 贯穿（logging_context 带 trace_id+start_as_current_span("agent.run")+所有后续操作带同一 trace_id）· JSONL 日志带 traceId/spanId/parentSpanId 顶层键，外部处理器与 OTEL spans/traceparent 关联（OpenClaw/LangFlow OTel trace correlation 自动拾取）· 存储前脱敏——local-first 默认 scrub PII/敏感 prompt，云托管先配 data masking 再上线，共享日志系统存 raw prompts 是合规雷（来源：腾讯云《Agent 调试实战：从黑盒到透明》（**logging_context={"trace_id"}；with tracer.start_as_current_span("agent.run")；span.set_attribute("trace_id");所有后续操作带同一 trace_id**）+ OpenClaw logging（**日志带 traceId/spanId/parentSpanId/traceFlags 顶层 JSON 键，外部处理器可与 OTEL spans 和 traceparent 传播关联；JSONL 循环日志文件**）+ LangFlow logging（**安装 opentelemetry-api 且有 active span 时每日志记录自动拾取 trace_id/span_id；OTel 非硬依赖未装则 no-op**）+ MLflow（**存储前 scrub 敏感数据：local-first 平台默认 scrub PII/敏感 prompt 内容；云托管先配 data masking 再上线；共享日志系统捕获 raw prompts 是合规雷**）2026 实拉；与 §工具输出沙箱化（r629 前）分工——那边管"工具输出隔离"，本条管"日志与追踪关联+存储脱敏"）
日志先关联：trace_id 贯穿全链、日志自动拾取 span、存储前脱敏。
- **trace 贯穿**：**logging_context 带 trace_id+start_as_current_span——所有后续操作同 ID**（腾讯云原文）→ 判据：**单 ID 贯穿**；断链=黑盒。
- **自动拾取**：**JSONL 日志顶层 traceId/spanId/parentSpanId 供外部关联；OTel active span 时自动拾取**（OpenClaw+LangFlow 原文）→ 判据：**日志自动带上下文**；不手动拼。
- **脱敏先行**：**存储前 scrub PII/敏感 prompt；云托管先配 data masking；raw prompts 进共享日志是合规雷**（MLflow 原文）→ 判据：**脱敏在存储前**；raw 内容别进共享系统。
- **提升层**：工具/工作流/可复用 Skill（日志关联与脱敏）。
## 上下文六步序列与三策略匹配：token budget 写 prompt 前先立 → static/dynamic context 分离 → 按 agent type 选技术 → static 层 prompt caching → context routing layer 动态注入 → governance+observability（跳过 budget 直接选技术=在未测量系统上盖楼）· 三策略：Offload（长期笔记/工具日志/TODO 写 AgentFS 指针引用）/ Reduce Compaction（对话太长总结旧轮+剪无关工具结果）/ Retrieve（按需 RAG 只取相关 chunks）（来源：Atlan《AI Agent Context Window Management: Implementation Guide 2026》（**六步序列：define token budget 在写任何 prompt 前→separate static/dynamic→select technique matched to agent type→enable prompt caching on static layer→add context routing layer for dynamic injection→governance and observability；每步建在上一步；跳过 budget 直接选技术=在未测量系统上盖楼**）+ agentic-ai KB（**三策略匹配：Offload 长期笔记/工具日志/TODO 写 AgentFS 指针引用；Reduce 对话太长总结旧轮剪工具结果；Retrieve 按需外部知识 RAG 只取相关 chunks**）2026 实拉；与 §上下文预算管理（r629 前）分工——那边管"何时开始规划压"，本条管"从预算到注入的完整序列与三策略匹配"）
上下文先立序列：budget 先行、static/dynamic 分离、三策略按需匹配。
- **六步序列**：**token budget 先立（写 prompt 前）→分离 static/dynamic→按 agent type 选技术→static 层缓存→context routing 动态注入→治理可观测**（Atlan 原文）→ 判据：**budget 先行**；跳过=未测量盖楼。
- **三策略**：**Offload（AgentFS 指针）/Reduce（总结剪枝）/Retrieve（按需 RAG）**（KB 原文）→ 判据：**按内容类型选策略**；别一把抓。
- **routing 层**：**IF/Switch 动态上下文选择——按 intent/user type 路由检索路径**（n8n 原文）→ 判据：**路由先分类**；动态注入有闸门。
- **提升层**：工作流/可复用 Skill（上下文序列）。

## Context bloat 削减与工具结果瘦身：别把 raw tool output 塞回下个 prompt——chat history 当 storage layer 是错；工具大 payload 先总结再进循环（模型只需要改变下一步的切片）· ACM（Agentic Context Management）：agent 自主决定何时压缩+offload 丢弃内容到外部记忆按需查询+后训练构造高质量上下文管理演示提升模型性能 · 短期窗口保持紧（active prompt+当前对话+立即工具结果），长期记忆跨会话易查询（来源：DEV《I finally cut AI context bloat by 80%》（**chat history 被当 storage layer 用；停止把 raw tool output 塞回下个 prompt，agent 更快更便宜更少困惑**）+ Mallary《Context Engineering for Agents 2026》（**短期窗口=active prompt+当前对话+立即工具结果保持紧；工具大 payload 先总结再进循环——模型只需要改变下一步的切片；长期记忆=持久用户事实/偏好/任务历史跨会话易查询**）+ arXiv 2607.23809（**ACM：agent 自主决定何时压缩上下文，offload 丢弃内容到外部记忆系统按需查询；后训练管线构造高质量上下文管理演示提升模型性能**）2026 实拉；与 §上下文预算管理（r629 前）分工——那边管"预算与时机"，本条管"内容瘦身与自主压缩"）
瘦身先截流：raw 输出不进下轮、大 payload 先总结、agent 自主压缩。
- **raw 截流**：**别把 raw tool output 塞回下个 prompt——chat history 不是 storage layer**（DEV 原文）→ 判据：**工具输出消化后进**；raw 直塞=bloat 80%。
- **payload 总结**：**大 payload 先总结再进循环——模型只需要改变下一步的切片**（Mallary 原文）→ 判据：**只进增量**；全量塞=浪费。
- **自主压缩**：**ACM：agent 自主决定何时压缩+offload 到外部记忆按需查询**（arXiv 原文）→ 判据：**压缩是 agent 技能**；不靠固定规则。
- **提升层**：工作流/工具（上下文瘦身）。

## Prompt 自动优化：OPRO-style Optimizer LLM 分析历史性能分+reasoning 数学推导更好 prompt；DSPy 分离 Logic（workflow）与 Parameters（prompts）自纠到 Ground Truth · GEPA 遗传-Pareto：LLM-based reflection+Pareto-efficient evolutionary search 优化 prompts/code/agent 架构/任何文本参数（MIT）· PromptForge 七维评分 LLM prompts 本地重写弱 prompt 清晰保意图（Python API/CLI/Gradio）· 腾讯 PromptEnhancer：CoT 提示重写+专用奖励模型 AlignEvaluator 无需修改 T2I 权重即插即用，精准度提升 300%（来源：n8n OPRO&DSPy workflow（**Optimizer LLM 分析过去性能分+reasoning 数学推导更好 prompt；DSPy 分离 Logic 与 Parameters 自纠直到匹配 Ground Truth**）+ GEPA（**Genetic-Pareto：LLM-based reflection+Pareto 进化搜索优化 prompts/code/agent architectures/文本参数，MIT**）+ tuneprompt（**PromptForge：七维评分 prompt 质量+重写弱 prompt 清晰保意图，local-first Python API/CLI/Gradio**）+ 腾讯混元 PromptEnhancer（**CoT 提示重写+奖励模型 AlignEvaluator，无需改 T2I 权重即插即用，中文 T2I 精准度 +300%**）2026 实拉；与 §评测信封（r629 前）分工——那边管"怎么评"，本条管"prompt 自动改"）
优化先自动化：性能分驱动重写、逻辑/参数分离、进化搜索。
- **OPRO**：**Optimizer LLM 分析历史性能分+reasoning 推导更好 prompt**（n8n 原文）→ 判据：**性能分驱动**；别手调碰运气。
- **DSPy 分离**：**Logic（workflow）与 Parameters（prompts）分离自纠到 Ground Truth**（原文）→ 判据：**逻辑/参数解耦**；prompt 变参数。
- **进化搜索**：**GEPA LLM reflection+Pareto 进化搜索（prompts/code/架构/文本参数）**（原文）→ 判据：**多目标搜索**；单目标会偏。
- **评分重写**：**七维评分+本地重写（PromptForge）；CoT 重写+奖励模型（PromptEnhancer 无权重改）**（原文）→ 判据：**评分先行**；改前先测。
- **提升层**：工具/工作流/可复用 Skill（提示词自动优化）。

## Query 扩展的规范码维度与多模态统一语义空间：同义词不够还补标准代号；图文进同一坐标空间双向检索（来源：CSDN Dify 实测《召回率提升 4.2 倍》2026-09 + dify.ai Multimodal Retrieval 2026-01 + Langflow 1.11.0 NextPlaid 2026-07 实拉，r633A 落地，与 §query transformation 三招分工——那边管"查询变换策略（Multi-Query/Step-Back）"，本条管"领域术语扩展与多模态检索空间"）
- **query expansion 含标准代号**：**自动补全同义词与标准代号——输入"变频器"扩展为"VFD, 变频驱动器, GB/T 12668"**（CSDN 实测，召回率 +4.2 倍/延迟 380ms）→ 判据：**领域词表补全**——同义词管口语、标准代号管检索命中；工业/法规域缺代号扩展=精确匹配永远打不中。
- **统一语义空间多模态检索**：**Dify v1.11.0 把图与文放进共享坐标系统——Image-to-Text / Text-to-Image / Image-to-Image 双向检索；自动提取 Markdown 链接引用的图片**（dify.ai 原文）→ 判据：**图文同空间互查**——"只嵌文本"=图问不到文、文问不到图；"统一语义空间"=双向都通。
- **视觉文档检索 ColPali**：**Langflow 1.11.0 lfx-nextplaid 扩展包提供 ColBERT 晚期交互 + ColPali 视觉文档检索**（langflow 原文）→ 判据：**扫描件/图文混排走视觉检索**——纯文本嵌入读不了版面；ColPali 直接向量化页面。
- **提升层**：工具/工作流（查询扩展 + 多模态检索）。

## RAG 评估分阶段定位与三类指标：ragbisect 告诉你哪一段丢质量、RAGPerf 拆三层测、EncouRAGe 本地化三类 metrics（来源：PyPI ragbisect 2026-09 + arXiv 2603.10765 RAGPerf + arXiv 2511.04696 EncouRAGe + EvalScope RAGAS 实拉，r633A 落地，与 §RAGAS 四指标分工——那边管"整体四指标跟踪"，本条管"定位到具体阶段/分三层测"）
- **分阶段定位**：**ragbisect 对 retrieval/ranking/generation 分开评分，从你自己的语料构建 eval set，指出哪个阶段丢质量最多+哪个内置替代能恢复**（PyPI 原文：tells you which stage is losing the most quality, and which built-in alternative would recover it）→ 判据：**别只看总分**——"端到端说坏"=不知道修哪；"分阶段定位"=直接换该阶段的替代方案。
- **三层指标**：**Context Recall（检索 chunk 中相关占比）/ Factual Consistency（回答中声明被检索上下文明确支持的比例）/ Query Accuracy（回答与 ground-truth 语义对齐）**（RAGPerf）→ 判据：**检索层/生成层分开量**——Context Recall 管召回、Factual Consistency 管接地、Query Accuracy 管答对。
- **本地快速评估**：**EncouRAGe 把指标分三类（generator/retrieval/LLM-based）本地跑；rag-scorecard 零成本确定性 token-overlap 启发式+LLM-as-judge 深评双速，结构差异/缺参/限流优雅降级不崩**（EncouRAGe/rag-scorecard）→ 判据：**评估也要成本分层**——启发式先筛、judge 深评；跑评不过期、能扛限流。
- **提升层**：工具/可复用 Skill（RAG 评估定位）。

## OpenClaw 上下文注入与混合记忆检索实现：MEMORY.md 条件注入+大文件截断附标记、memory_search 关键词精确匹配 ID、非对称嵌入 input_type（来源：docs.openclaw.ai 多语言页 concepts/agent + concepts/memory + reference/memory-config 2026-09~10 实拉，r633A 落地，与 §记忆检索后处理管线分工——那边管"取出来怎么排（加权合并/时间衰减/MMR）"，本条管"文件怎么进上下文、检索用哪种匹配"）
- **注入三条件**：**新会话首个轮次注入工作区文件到系统提示词项目上下文；MEMORY.md 仅当存在于工作区根目录才注入；空文件跳过；大文件裁剪截断并附加标记保持提示词精简（标记提示"请读取文件查看完整内容"）**（原文）→ 判据：**注入按存在性与体积决策**——"常驻全注入"=大文件撑爆窗口；"裁剪+附标记"=精简不失入口。
- **memory_search 混合检索实现**：**向量相似度（语义）+关键词匹配（精确术语如 ID 和代码符号）双路**（原文）→ 判据：**精确标识符走关键词**——纯向量对 ID/函数名相似度不可靠；"向量+关键词"=语义与精确各司其职。
- **非对称嵌入 input_type**：**兼容 OpenAI 的嵌入端点可用 input_type 请求字段区分查询嵌入与文档嵌入——非对称嵌入模型要求两者用不同标签**（memory-config 原文）→ 判据：**非对称模型按角色打标**——查询/文档向量方向不同；不区分=查询与文档错配。
- **提升层**：工具/工作流（上下文注入 + 记忆检索实现）。

## 多模态上下文注入三要求与块级限制：图文链路成立要三条件齐备，chunk 有 10 图上限（来源：DeepWiki Dify docs 8.7 Knowledge Retrieval Node Integration + 8.5 Multimodal Knowledge Bases + Dify 文档 Upload Local Files 2026-03~10 实拉，r633B 落地，与 §统一语义空间多模态检索分工——那边管"嵌入空间怎么建"，本条管"检索节点/模型/rerank 三环怎么配、块容量边界"）
- **三要求缺一断链**：**多模态上下文注入要求 ①知识库用多模态 embedding 模型 ②LLM 节点支持视觉能力 ③rerank 模型（若用）必须多模态——三环任一不满足图文链路断**（原文）→ 判据：**配置三环齐查**——"只配了多模态知识库"=下游不支持视觉照样断；"rerank 用纯文本"=多模态结果被文本排序毁掉。
- **跨模态检索数据流**：**Query → 多模态知识库 → 跨模态检索 → result 变量 → Vision-Enabled LLM；文本查询可检索到相关图像、图像查询可检索到相关文本**（原文）→ 判据：**双向都要通**——"只做文→图"=图→文场景漏；"双向跨模态"=query 与 result 类型解耦。
- **块级容量边界**：**每个 chunk 最多 10 张图片附件，超限不提取；上传文件的图片 URL 可安全移除不影响提取图片（选多模态 embedding 后提取图也会被嵌入索引）**（Dify 文档）→ 判据：**块容量有上限**——"图多到爆块"=超过 10 张静默丢；"URL 可删"=文本干净与图片索引两不误。
- **提升层**：工作流（多模态检索链路配置）。

## 文档解析模型工程选型：长序列 KV 常量、轻量 SOTA、结构输出三档（来源：A2A Protocol Unlimited-OCR 2026-07 + 中国电信 TeleOCR 2026-09 + 智谱 GLM-OCR docs + AI2 OlmOCR 2026-01 + 阿里 PaddleOCR-VL-1.6 2026-06 实拉，r633B 落地，与 §RAGFlow 版面分析先切分分工——那边管"管线先懂版式"，本条管"具体解析模型怎么选（按尺寸/精度/输出格式）"）
- **长序列常量 KV**：**Unlimited-OCR（百度 2026-06 开源）用 R-SWA（Reference Sliding Window Attention）解码器在长序列生成期间保持 KV cache 常量——OmniDocBench v1.5 93.23%，"one-shot long-horizon parsing"时代；5 周近 19,700★**（原文）→ 判据：**长文档看 KV 增长**——"序列越长 KV 越涨"=超长文档不可行；"R-SWA 常量 KV"=任意长输入可解析。
- **轻量小模型 SOTA**：**GLM-OCR 0.9B（CogViT 视觉编码器+轻量跨模态连接器+GLM-0.5 解码，层次化视觉注意力，可转 LaTeX/Markdown）；TeleOCR 1.2B 96.87/100 登全球文档解析榜首（ICDAR 2026 sci-image-miner 第一）；PaddleOCR-VL-1.6 96.33% 且与 1.5 结构一致零成本适配**（原文）→ 判据：**尺寸与精度可兼得**——"大模型才准"=部署贵；"0.9B-1.6B SOTA"=小模型够用；换版本结构一致=即换即用。
- **结构化输出形态**：**OlmOCR（AI2 开源 GPU 文档重建工具包）把 PDF/PNG/JPG 页转自然排序 Markdown 或文本（含表格与公式）**（原文）→ 判据：**按下游格式选**——"要 Markdown 带表格公式"=OlmOCR 形态；"要 LaTeX"=GLM-OCR 形态；输出形态是选型第一筛。
- **提升层**：工具/模型（文档解析选型）。

## OpenClaw 媒体理解规则：原生视觉直传原图、音频空文件占位跳过、模型 input 字段声明视觉、保留图像计入成本（来源：docs.openclaw.ai nodes/media-understanding 多语言页 2026-09~10 + clawdocs voice-multimodal 2026-10 实拉，r633B 落地，与 §OpenClaw 上下文注入分工——那边管"文件怎么进上下文"，本条管"入站媒体怎么处理、成本怎么控"）
- **原生视觉直传**：**主图像模型原生支持视觉时跳过 [Image] 摘要块、原始图像直接传模型；MiniMax 是例外（仍需描述 pass）**（原文）→ 判据：**能直传就别摘要**——"有视觉能力还打 [Image] 块"=多花一次描述调用；"直传原图"=零额外成本；例外单独配。
- **空文件占位**：**音频文件 <1024 字节视为空或损坏，转录前跳过；agent 收到确定性的占位转录文本**（原文）→ 判据：**空文件确定性处理**——"空音频进管线"=转录乱返回；"确定性占位文本"=agent 知道这是空文件。
- **视觉能力声明**：**OpenClaw 通过模型定义 input 字段判断是否支持视觉——配置 `"input": ["text","image"]` 才被当作视觉模型**（阿里云 Model Studio 帮助）→ 判据：**能力靠配置声明**——"模型会看图但不声明"=OpenClaw 不传图；"input 字段声明"=能力显式化。
- **成本与清理**：**保留在后续请求中的图像会贡献输入成本（依 provider 与运行时上下文处理而定）；session pruning 负责清理；识别/提取任务无需持续像素访问时用工具（tools.media.image maxBytes/maxChars/models 可配）**（原文）→ 判据：**图像按需保留**——"每轮都带图"=输入成本累积；"识别完即弃"=只留文本结论。
- **提升层**：工具/工作流（媒体理解与成本）。

## 提示缓存断点工程：system prompt 独立缓存、压缩前先缓存、workspace 级隔离（来源：Anthropic 官方 Prompt Caching + Compaction docs + IT之家 Claude Code 省钱技巧 2026-08 + 智谱上下文缓存 docs 实拉，r633C 落地，与 §前缀缓存共享 system prompt 工程分工——那边管"引擎侧 RadixAttention"，本条管"API 侧 cache_control 怎么放、何时放"）
- **system prompt 末尾断点**：**在 system prompt 末尾加 cache_control 断点，使 system prompt 与对话分开缓存——压缩发生时 system prompt 缓存保持有效并从缓存读取，只有压缩摘要需要写新缓存项**（Anthropic 官方）→ 判据：**断点放在最长静态块末尾**——"断点放中间"=缓存块被截短；"末尾断点"=整个静态前缀一次缓存；压缩不碰它。
- **缓存有效期内压缩**：**Claude Code 省钱：/compact 在休息前做——对话还在缓存里时压缩成本只有正常十分之一，等缓存过期再压按全价重新读一遍**（IT之家）→ 判据：**压缩时机挂靠缓存 TTL**——"缓存过期后压缩"=全价重读；"缓存有效时压缩"=1/10 成本；与 §压缩时机按任务状态分工：那边管"能不能压"，本条管"什么时候压最便宜"。
- **缓存计费与隔离**：**缓存读取 0.1× 输入价（写略贵）；2026-02-05 起 Claude API/Azure 按 workspace 级隔离（Bedrock/Vertex 保持组织级）；智谱上下文缓存命中通常为标准价 50%**（官方）→ 判据：**缓存是共享状态要知边界**——"跨 workspace 复用缓存"=2026-02 后失效；"命中率设计"=把静态内容前置；各家折扣不同（Claude 90%/智谱 50%）。
- **提升层**：工具/工作流（提示缓存工程）。

## 量化部署决策框架：位宽按硬件与负载选、验证跑生产负载、GGUF 起点与升级路径（来源：腾讯云 FP8 分析 2026-07 + Spheron 2026-10 + Kunal Ganglani GGUF/GPTQ/EXL2 对比 2026-07 + OpenClaw 本地配置 docs 实拉，r633C 落地，与 §MoE 激活参数选型分工——那边管"模型本身怎么选"，本条管"同一模型压到几位、用哪个量化格式"）
- **位宽按硬件代际选**：**FP8 相比 FP16 显存减 50%、推理速度 +30-33%、困惑度仅 +0.1-0.3%，是 2026 年 H100+ 生产环境默认；Blackwell 试 FP4（RTN+激活校准的 nvidia/ 预校准模型）；INT4 面向端侧（Ling-3.0-tiny 115 tok/s）**（原文）→ 判据：**位宽挂硬件代际**——"H100 以下硬上 FP8"=无 tensor core 收益；"消费卡"=GGUF INT4/Q4 优先；"数据中心"=FP8/FP4。
- **GGUF 起点与升级路径**：**多数开发者从 GGUF Q4_K_M 起步（Mac/Linux/Windows/CPU/GPU 全跑，Ollama/llama.cpp）；特定任务质量不达标升 Q5_K_M/Q8_0 再换格式；RTX 4090/5090 追最大吞吐试 EXL2**（Kunal）→ 判据：**先兼容再精调**——"直接上最大位宽"=内存不够；"Q4_K_M 起步按需升级"=最小可行配置；格式切换放最后。
- **部署形态三选**：**OpenClaw 本地模式三选（云端+本地混合/仅云端 ollama.com 无守护进程/仅本地）；OLLAMA_API_KEY=ollama-local（本地主机任意值）；3B 8GB RAM、7B+ 16GB+、14-27B 32GB RAM/16-24GB VRAM**（docs）→ 判据：**先定部署形态再选位宽**——"全本地"=隐私与成本优先，内存决定位宽；"混合"=常规本地+峰值云端；"云端"=无本地硬件负担。
- **提升层**：工具/模型（量化部署）。

## 模型路由与混合部署：分层路由、关键词规则路由、Batch 降本（来源：CSDN Claude 成本优化三板斧 2026-04 + n8n Self-Hosted vs Cloud 2026-10 + n8n DGX Spark 2026-10 + OpenClaw 模型路由配置 2026-10 实拉，r633C 落地，与 §上下文预算管理分工——那边管"窗口怎么省"，本条管"请求派给哪个模型、云端还是本地"）
- **分层路由**：**简单任务走 Haiku、复杂走 Sonnet、深度推理才 Opus；Batch API 5 小时内处理、成本降 50%**（CSDN）→ 判据：**任务难度→模型档位**——"全用旗舰"=简单任务多付 10-20 倍；"分层路由+批处理"=成本随任务形态下降。
- **本地/云端路由**：**n8n 官方指南：按"硬件能跑什么+怎么在本地与云之间路由"设计；DGX Spark 上"按带宽选模型不是按参数量"；OpenClaw primary/fallback 双模型+rules 关键词路由（如 本地 llama3.2:3b 默认+anthropic/claude-sonnet 备份，rules match 摘要/翻译/提醒 走指定模型）**（原文）→ 判据：**路由规则先于调用**——"单一模型硬扛"=要么贵要么慢；"primary+fallback+rules"=成本与质量按任务分流；带宽（而非参数量）是本地选型主指标。
- **提升层**：工作流/工具（模型路由）。

## 模型路由的版本与成本语义：路由版本钉定、智能模式四档、agent 成本栈（来源：阿里百炼智能路由官方文档 + 新版智能体应用 + DEV Opus Plans Haiku Executes 2026-10-10 实拉，r634A 落地，与 §模型路由与混合部署分工——那边管"请求派给哪个模型、云端还是本地"，本条管"路由配置本身怎么管理、成本怎么算"）
- **路由版本钉定**：**阿里百炼智能路由：切换路由版本时备选模型集随之变更，修改后几分钟内生效且不影响线上请求；选定版本后线上路由行为长期稳定；路由版本默认不自动更新，升级版本前必须全面评估**（阿里）→ 判据：**路由配置要版本化**——"路由规则随时变"=线上行为不可复现；"版本钉定+显式升级"=行为稳定、升级可评估；与 §技能评测闭合邻域分工：那边管"技能评测"，本条管"路由版本切换要评估"。
- **智能模式四档**：**百炼新版智能体应用智能模式含 AUTO/性能/均衡/经济四档（手动选定），AUTO 与其他三档区别在于动态调整；推荐多步规划用强工具调用模型（千问-Max 系列）**（阿里）→ 判据：**成本档位显式声明**——"全默认"=档位不可控；"四档手动/动态"=按业务对成本-质量取舍显式选择；多步规划任务先看工具调用能力再看档位。
- **agent 成本栈**：**全 opus 的代价：从扫描目录到格式化字符串都烧 frontier-model token（$5/$25 per million）——"every model was opus"是 agent 成本危机；正确做法是规划用旗舰、执行用廉价**（DEV）→ 判据：**按步骤角色分配模型档位**——"一个模型通吃所有步骤"=成本爆炸；"规划/执行分模型"=成本栈分层；成本核算按步骤类型统计而非按总调用数。
- **提升层**：工作流/工具（路由版本与成本）。

## 统一 API 网关与多 provider 归一化：单端点多模型、四层回退、MCP 单连接暴露全工具（来源：腾讯 TokenHub 官方 + CSDN GitHub 开源月报 2026-08 + Activepieces MCP 官方 2026 实拉，r634A 落地，与 §工具集成与发现分工——那边管"工具怎么找/怎么加载"，本条管"模型与工具的入口怎么收敛"）
- **单端点多模型**：**腾讯 TokenHub：一个 OpenAI 兼容端点路由到 Kimi K3/GLM-5.2/DeepSeek-V4/Qwen 3.6/Hunyuan 等——免去切换厂商账号/SDK/计费关系；新加坡节点保国际低延迟**（腾讯）→ 判据：**网关收敛接入面**——"每厂商一套 SDK/计费"=接入成本线性增长；"单 OpenAI 兼容端点"=路由与计费统一；网关选型先看兼容面与地域节点。
- **四层自动回退**：**OmniRoute 用一个端点统一接入 350+ AI 提供商并支持四层自动回退（GitHub 8 月万星榜）；Claude Code Router 本地网关连接 Claude Code/Codex/Grok CLI 到任意 provider 带路由/failover/可观测**（CSDN + EveryDev）→ 判据：**网关自带 failover 语义**——"应用层自己写重试"=每个调用方重复实现；"网关四层回退"=故障转移集中化；网关回退层数要与提供商可用性 SLA 匹配。
- **MCP 单连接暴露全工具**：**Activepieces HTTP MCP server：连一次 HTTP，其全部动作变工具，同一 server URL 覆盖该平台 770+ 应用；所有已连接 piece 可经一个 MCP server 暴露给 Claude/Cursor/Windsurf 调用**（Activepieces）→ 判据：**MCP 是统一工具入口**——"每应用一个集成"=工具面爆炸；"单 MCP server 暴露全部动作"=agent 一条连接调全平台；与 §per-tool 最小权限分工：那边管"每个工具给多少权"，本条管"多少工具走一个入口"。
- **提升层**：工具/工作流（统一网关）。

## 工具集成与发现：code-as-action、知识图谱 API 发现、Hub 工具分享（来源：smolagents 官方 docs + deeplearning.ai 新课程 + ModelScope Agents-A1 实拉，r634A 落地，与 §统一 API 网关分工——那边管"入口收敛"，本条管"工具从哪来、怎么被发现"）
- **code-as-action 形态**：**smolagents（~1000 行核心 Apache-2.0）让模型写可执行 Python 作为动作格式（而非 JSON tool calls），模型无关（transformers/Ollama/LiteLLM），可选沙箱执行（E2B/Docker/WebAssembly）、托管 sub-agents、Hub 分享**（HF）→ 判据：**动作格式按场景选**——"复杂多步操作"=code-as-action 表达力强于 JSON 调用；"简单固定调用"=JSON 更可审计；沙箱是 code-as-action 的前置安全条件。
- **知识图谱 API 发现**：**deeplearning.ai 新课程《Knowledge Graphs for AI Agent API Discovery》：构建知识图谱让 agent 找到并按正确顺序调用正确的 API（而非靠提示词碰运气）**（deeplearning.ai）→ 判据：**API 发现结构化**——"提示词里列 API"=超出上下文就找不到；"知识图谱存 API 关系+调用顺序"=发现与排序可推理；发现层先于执行层建。
- **Hub 工具分享与原生工具模型**：**smolagents Tool.from_hub()/push_to_hub() 社区共享工具；Tool.from_langchain() 包装 LangChain 工具；InternScience Agents-A1 原生 function calling+工具集成（分解可执行子步骤/规划/基于中间结果自适应）**（HF + ModelScope）→ 判据：**工具可复用可分享**——"工具写死在代码里"=换项目重写；"Hub 分享+包装已有工具"=跨项目复用；模型选型看原生工具调用能力（多步规划任务）。
- **提升层**：模型/工具/可复用 Skill（工具集成）。

## 生成期护栏：intrinsic guardrail、自停生成、LogitsProcessor 局部约束（来源：arXiv SingProbe 2608.30703 + styxx.guardrail + Neosophie LogitsProcessor + Zep 幻觉降低 2026 实拉，r634B 落地，与 §生成后验证分工——那边管"生成完再查"，本条管"生成过程中就拦"）
- **intrinsic guardrail**：**SingProbe：复用 base model 自回归解码时已产生的 hidden states 做生成期监控，而非独立模型反复处理生成文本——跨模型 guard 适配/统一训练/服务集成/评估资源开放栈**（arXiv）→ 判据：**护栏复用生成侧算力**——"独立模型盯生成"=双倍推理成本；"hidden states 复用"=监控几乎零额外推理；generation-time 监控与后处理校验互补。
- **自停生成**：**styxx.generate_safe：单函数实时自停生成——在 token 边界处干预，防止捏造到达用户前；styxx.guardrail 多信号幻觉检测 AUC 0.90（HaluEval-QA），29-probe 跨供应商探测图集**（Zenodo）→ 判据：**护栏要在边界拦**——"生成完再检测"=幻觉已送达；"token 边界自停"=捏造在到达前被截；生成期干预与后校验分层。
- **局部 logits 约束**：**Neosophie 自定义 LogitsProcessor：只在 JSON 输出的 Content 字段内应用 no-repeat-ngram 控制，其余生成不动——幻觉循环在要害处抑制、附带损伤最小；Zep：答案有已知形态（schema/enum/有效 ID 集）时约束模型使其无法发明不存在的值——structured outputs+constrained decoding 按构造移除整类幻觉**（Neosophie + Zep）→ 判据：**约束范围精准**——"全生成无差别约束"=误伤正常输出；"只约束问题字段"=对症下药；"合法值集合约束"=整类幻觉按构造消失。
- **提升层**：模型/工具（生成期护栏）。

## 护栏分层与证据化：Layered Defense、verity receipt、TEE attestation、形式逻辑预检（来源：Wasil Zafar Anthropic SDK Part 20 + logi-cmd agent-guardrails + Proof-of-Guardrail arXiv 2603.05786 + ICME Pre-flight 2026 实拉，r634B 落地，与 §Agent 工具面安全分工——那边管"注入怎么防"，本条管"护栏怎么分层、执行怎么留证"）
- **护栏四层叠放**：**生产系统用多层重叠护栏而非单一技术，每层抓不同失败模式：prompt engineering（grounding 指令+"I don't know" 许可）/structured output（tool_use schemas nullable+enum 约束）/post-processing validation（程序化检查必填字段/合法范围/引用存在）/human**（Wasil）→ 判据：**护栏按失败模式分层**——"单层护栏"=一种失败模式漏网全漏；"四层叠放"=每层专抓一类；护栏不是选一层是叠多层。
- **执行证据化**：**logi-cmd agent-guardrails：验证通过记录结构化 verificationEvidence（verity receipt 证明本地运行时验证）；Proof-of-Guardrail：TEE 平台 attestation 文档——每次用户输入生成新 attestation，用户用开源 f 的期望测量+输入/响应/验证密钥验证护栏执行**（GitHub + arXiv）→ 判据：**护栏执行要可举证**——"护栏跑了但无记录"=无法审计无法证明；"receipt/attestation 留证"=可独立验证；证明粒度到每次输入。
- **形式逻辑预检**：**ICME Pre-flight：明文规则→编译成形式逻辑→执行前检查每个 agent 动作（<1 秒）；SAT=允许 UNSAT=阻止，无模型判断/无人工瓶颈/无信任；返回加密 ZK receipt 防篡改**（ICME）→ 判据：**规则要可判定**——"自然语言规则跑在模型判断上"=解释空间大；"形式逻辑预检 SAT/UNSAT"=确定性拦截；与 §Guard 化工具分工：那边管"工具层护栏"，本条管"动作层预检+证据"。
- **提升层**：工作流/工具（护栏分层与证据）。

## 结构约束的边界与陷阱：structure snowballing、provider 能力结构校验不能证、bounded evidence 评估一次（来源：arXiv 2604.06066 + OpenClaw decision-models + Plugin SDK capabilities 2026 实拉，r634B 落地，与 §结构化输出工程分工——那边管"怎么约束"，本条管"约束的副作用与边界"）
- **structure snowballing**：**纯 Outlines 受约束解码不强加结构约束不提升自纠错——Qwen3-8B 上结构约束触发新失败模式"structure snowballing"：满足严格格式规则的认知负担把模型推进格式陷阱；这是受约束解码的对齐税**（arXiv）→ 判据：**结构约束有代价**——"以为约束=免费质量提升"=格式负担拖垮推理；"约束+自纠错分离"=结构约束与反思质量分开评估；用约束前先测它是否伤推理。
- **结构校验 ≠ 能力证明**：**OpenClaw Plugin SDK：结构校验（validateDecisionBatchV2/validateDecisionResultV2）强制 bounded data contract，但结构校验不能证明 provider 支持某操作/输入模态/推理模式——决策模型 evaluate(batch, context) 返回 validated typed answers**（OpenClaw）→ 判据：**校验形状不校验能力**——"schema 通过=provider 能用"=误判；"结构校验+能力声明分开"=形状合规与操作支持是两个断言。
- **bounded evidence 评估一次**：**OpenClaw decision-models：消费者构建 bounded useful evidence、评估一次、provider 返回 unsupported-input 时保持正常行为（含上下文溢出）；运行时不确定模型 token、不截断 evidence、不重试、不换 provider——输入拒绝不打开 provider circuit，取消与关闭 authority 保持终态**（OpenClaw）→ 判据：**评估输入有界且只评估一次**——"无限重试换 provider"=circuit 失控；"bounded evidence+一次评估+拒绝即终态"=决策确定性；上下文溢出当作 unsupported-input 处理而非无限膨胀。
- **提升层**：模型/工作流（结构约束边界）。

## MCP 访问控制与授权边界：Tool 级 ACL、Meta MCP 司令官、Relay 权限（来源：腾讯云 MCP 网关 Tool 级黑白名单 + 腾讯云 MCP 开发指南 Meta MCP + OpenClaw MCP Relay + StackSwap Dify MCP 双模式 2026 实拉，r634C 落地，与 §MCP 选型五标准分工——那边管"选哪个 MCP"，本条管"MCP 的访问控制与编排怎么配"）
- **Tool 级黑白名单**：**腾讯云 MCP 网关：Server 访问模式"全部开放"时可用 Tool 访问控制自定义权限——按 Consumer 配置"谁能调整个服务"与"谁能调具体 Tool"（Tool 级 ACL）**（腾讯云）→ 判据：**授权粒度到工具**——"只控 server 级"=装一个 server 全工具开放；"Tool 级 ACL+按 Consumer"=最小暴露；与 §per-tool 最小权限分工：那边管"agent 侧每个工具给多少权"，本条管"网关侧按调用者配黑白名单"。
- **Meta MCP 司令官**：**腾讯云 MCP 开发指南（功能搬运→能力合成）：原子套件前加"司令官"层——所有调用先过它，由它按意图做索引/路由/组合判断；轻档·索引路由型只暴露两个 meta-tool：search(intent)（自然语言检索相关原子）+invoke(tool,params)**（腾讯云）→ 判据：**工具面加路由层**——"agent 面对一堆原子工具"=选择负担+上下文占用；"两 meta-tool 收敛入口"=检索+调用分离；与 §Agent 模型路由形态学分工：那边管"模型路由"，本条管"工具路由"。
- **Relay 授权边界**：**OpenClaw MCP Relay：MCP 会话操作不暴露任意 Gateway 方法；请求以 grant 的 principal 身份运行（在其 selected access limit+当前权限内）；发送消息可让 agent 在其自身策略下采取真实行动——连接 server 不自动启用其 UI 代码/不绕过 session 工具权限**（OpenClaw）→ 判据：**权限随身份走**——"连接即全权"=越权；"grant principal 身份+access limit"=调用者权限即执行权限；MCP 的 UI/工具能力默认不激活。
- **提升层**：工具/工作流（MCP 访问控制）。

## 工具注册表与目录分野：registry vs directory、标签治理、多源聚合（来源：localskills.sh skills-sh-alternatives + 腾讯技能包标签访问控制 + find-skill MCP 多源聚合 + 科大讯飞 SkillHub CLI 2026 实拉，r634C 落地，与 §技能库检索即 RAG 分工——那边管"运行时怎么选技能"，本条管"技能/MCP 注册表怎么建、目录与注册表怎么分"）
- **registry vs directory 分野**：**skillsmp 是 marketplace-style index（directory）——广度是重点，作为发现工具的补充；要 private skills/roles/review gate/团队功能走 registry 而非 directory；目录解决"有什么"，注册表解决"谁能用+版本+评审"**（localskills）→ 判据：**按治理需求选形态**——"只要发现"=directory 够；"要私有/角色/评审门"=registry；判据：要 review gate 就是 registry 范畴。
- **标签访问治理**：**腾讯技能包：技能 tags 空=公开（谁都能用）/技能 tags 与用户 tags 有交集=受保护（匹配即访问）/交集空=受限；用户→角色→标签集合——角色本质是一组标签，按能力域划分可见性，不需单独权限体系**（腾讯云）→ 判据：**标签即权限面**——"逐技能配权限"=管理爆炸；"角色=标签组"=能力域划分；三档可见性（公开/受保护/受限）覆盖大部分场景。
- **多源聚合与可配置 registry**：**find-skill MCP：多源聚合——SkillsMP marketplace 2M+ skill（按语言/分类筛选，免鉴权可搜+可选 API_KEY）；sources/ 下加文件实现 search(query, opts)→Candidate[] 即接新源；科大讯飞 SkillHub CLI：registry 可配置（默认 https://skill.xfyun.cn，--registry 临时换源，SKILLHUB_API_KEY 环境变量）**（LobeHub + 讯飞）→ 判据：**注册表可插拔**——"写死单一 marketplace"=换源重写；"sources 接口+registry 配置"=多源聚合；发现与安装走统一接口。
- **提升层**：工具/可复用 Skill（注册表治理）。

## 工具面规模与组合策略：MCP 与 Skills 替代关系、多源工具加载、bundles 合并（来源：deeplearning.ai SDD 课程总结 + smolagents 工具四源 + OpenClaw bundles + Hivebook smolagents 2026 实拉，r634C 落地，与 §工具集成与发现分工——那边管"工具怎么找/加载"，本条管"工具面规模怎么控、Skills 与 MCP 谁替代谁"）
- **Skills+CLI 部分替换 MCP**：**deeplearning.ai SDD 课程总结：MCP servers 正在被部分替换为 Skills + CLI tools——Agent Skills 标准化格式自动化重复 prompt 流程**（deeplearning.ai）→ 判据：**连接型用 MCP、程序型用 Skills**——"本地可执行工具"=CLI/Skills 更直接；"外部系统连接"=MCP；选型先问"这工具是连系统还是跑流程"。
- **多源工具加载一行化**：**smolagents 工具四源：Tool.from_hub()（社区共享）/Tool.from_langchain()（包装 LangChain）/ToolCollection.from_mcp()（连接任意 MCP server 取工具集，stdio/SSE，一行加载 Smithery registry 或自建 server）/Tool.from_space()（HF Space 变工具）——MCP 原生集成 2000+ servers 无 wrapper；sandbox 多选+import whitelist（不让你跑 os.system）**（smolagents）→ 判据：**工具加载统一抽象**——"每来源一套代码"=集成成本线性涨；"四源统一 from_* 接口"=一行接入；代码执行沙箱是前提。
- **bundle 合并与 opt-in**：**OpenClaw bundles：Hook packs（HOOK.md+handler.ts 布局）与 MCP tools（bundle MCP config 合并进 OpenClaw settings，stdio/HTTP servers 加载）统一分发；MCP servers 可提供沙箱化交互视图但需 opt-in（MCP Apps host），连接不自动启用 UI 代码**（OpenClaw）→ 判据：**能力包打包分发**——"技能+hook+MCP 散装"=安装管理混乱；"bundle 合并配置"=一包装齐；UI/高权能力 opt-in 默认关。
- **提升层**：工具/工作流（工具面规模策略）。

## 记忆摄取与整合：离散事实优先、元数据同权重、会话后整合防降级（来源：MindStudio 持久记忆 + Redis 多轮精度 + CSDN 长期记忆 metadata + n8n 记忆节点 2026 实拉，r635A 落地，与 §记忆提取四策略分工——那边管"提取哪些类型"，本条管"摄取后怎么结构化、怎么防污染"）
- **离散事实而非原始记录**：**记忆摄取质量取决于 ingestion 时如何结构化——提取离散事实，不存原始 transcript；query expansion 回退+显式 gap 承认是生产可靠性必备**（MindStudio）→ 判据：**记的是事实不是流水账**——"整段 transcript 入库"=检索噪声+token 浪费；"离散事实条目"=每块可检索可引用；检索不到时显式承认缺口而非硬答。
- **元数据与语义同权重**：**metadata（user/recency/topic/visibility/source）过滤与语义相似同等重要；长期记忆每条带 metadata：user_id/tenant_id/memory_type/visibility/source**（MindStudio + CSDN）→ 判据：**记忆条目带身份**——"裸文本嵌入"=无法按用户/时间/主题筛；"元数据+向量"=多路过滤；visibility 管可见性、source 管溯源。
- **会话后整合**：**每次会话后记忆整合（consolidation）防 stale/重复记录随时间降级检索；多轮精度靠把交互历史存为向量、检索语义相关过去交换作新查询上下文，而非拼接不断增长的 transcript（context bloat）**（MindStudio + Redis）→ 判据：**整合是周期任务**——"每轮追加不整合"=重复与过期堆积；"会话后整合"=去重+提炼；跨轮上下文用检索不用全文拼接。
- **提升层**：工作流（记忆摄取与整合）。

## 记忆库形态与工具面：三合一虚拟 FS、auto-recall/auto-capture、术语表记忆（来源：OpenViking + OpenClaw memory-lancedb + mem0 search-knowledge + Jev Agent + WikiKB 2026 实拉，r635A 落地，与 §知识库工程分工——那边管"文档知识库"，本条管"agent 记忆库的形态与工具设计"）
- **三合一虚拟文件系统**：**OpenViking：记忆+RAG+技能统一为一个虚拟文件系统，agent 用 ls/tree/find 浏览——消除"记忆在一个库、RAG 在向量库、技能散在仓库"的碎片化**（OpenViking 33K★）→ 判据：**记忆库可浏览**——"三类资产三套接口"=agent 不会用；"统一 FS+文件命令"=发现成本低；显式策展（WikiKB）优于被动堆叠。
- **auto-recall/auto-capture 闭环**：**OpenClaw memory-lancedb：模型 turn 前 auto-recall 相关记忆、响应后 auto-capture 重要事实；memory_search 混合检索（向量语义+关键词精确术语：标识符/代码符号）**（OpenClaw）→ 判据：**记忆读写挂生命周期**——"只在被问时搜"=该记的没记；"turn 前召回+响应后捕获"=闭环；混合检索让精确符号与语义表达都能命中。
- **术语表记忆与精确工具**：**mem0 search-knowledge：同语料上随时间改进检索——corpus-aware glossary（informal→formal、品牌拼写、别名、常见 typo 映射），非用户偏好存储；Jev Agent：surgical search 工具（jevgrep 精确片段）替代标准 RAG 的 broad fuzzy 匹配**（mem0 + Activepieces）→ 判据：**检索知识独立于偏好**——"术语映射塞进偏好库"=两不相干污染；"检索专用 glossary"=查询面表达归一；精确场景用精确工具不靠模糊匹配。
- **提升层**：工具/可复用 Skill（记忆库形态）。

## 记忆分层与防投毒：tiers 信任级别、engine-local 排序、基准驱动选型（来源：OpenClaw memory architecture + memory-builtin + MemPalace/agentmemory 基准 + Cognee graph-native 2026 实拉，r635A 落地，与 §记忆分层分工——那边管"记忆分几层"，本条管"分层后的信任/检索/选型细则"）
- **tiers 与防投毒**：**OpenClaw Memory Core：plain files+SQLite 索引，tiers 有不同信任级别/写入规则/注入行为——内容如何"赚"进长期记忆，防御垃圾与投毒；内置索引把 MEMORY.md/USER.md/memory/*.md 分块（默认 400 token+80 overlap）**（OpenClaw）→ 判据：**记忆有准入机制**——"什么都往长期记忆写"=垃圾进检索；"分层信任+写入规则"=低层需验证才升层；分块参数影响命中粒度。
- **engine-local 排序**：**OpenClaw：检索用 engine-local text ranking，SQLite 与 PostgreSQL 分数/排序可不同；换引擎不保证同序**（OpenClaw）→ 判据：**排序是引擎实现细节**——"换库后顺序变了"=正常非故障；跨引擎对比结果要标引擎；评分不可移植。
- **基准驱动选型**：**MemPalace 54.1K★：LongMemEval 96.6% R@5 零 API 调用（全本地 MIT）；agentmemory 29K★ 基于真实基准；Cognee graph-native+30+ 源摄取+entity/relationship/provenance 追踪**（Rohit Raj + Vuncloud + Cognee）→ 判据：**记忆选型看基准**——"看 star 不看基准"=能力虚标；"LongMemEval R@5+本地性"=可复现；图记忆管关系与溯源、向量管相似。
- **提升层**：模型/工作流（记忆分层与防投毒）。

## 跨会话 web 记忆：轨迹 episodic、condenser 摘要、coach 检索指导（来源：WebCoach arXiv 2511.12997 + HEEL 状态中心记忆 + claude-mem 冷启动 2026 实拉，r635B 落地，与 §记忆摄取分工——那边管"事实怎么结构化"，本条管"浏览器/任务轨迹怎么跨会话复用"）
- **三件套**：**WebCoach：WebCondenser（原始导航日志标准化成简明摘要）+External Memory Store（完整轨迹=episodic experiences 组织）+Coach（检索相关轨迹并指导）——模型无关、自演化，免重训获得长期规划/反思/持续学习**（WebCoach）→ 判据：**轨迹是记忆对象**——"只记结果不记路径"=重跑时从头再来；"condenser 摘要+轨迹 episodic+coach 指导"=任务经验可复用；轨迹记忆独立于模型（换模型不丢经验）。
- **状态中心自传体记忆**：**HEEL：终身记忆库跨 session 持久；新会话（分身）创建时以 Character ID 为键查询 Experience 层（J=1）记忆项、按复合评分排序注入上下文——超越"会话中心本体论"**（HEEL）→ 判据：**记忆键是身份不是会话**——"以会话为界"=每次新会话冷启动；"Character ID 查 Experience 层注入"=身份延续；跨会话连续性由记忆库承担。
- **冷启动双天花板**：**static system prompt（冻结指令，无法发现"你总用 TypeScript"）+stateless session（会话结束工作知识蒸发）=永远冷启动；解法=evolving memory（记忆随使用演化，替代静态 prompt 与无状态会话）**（AgentSwarms）→ 判据：**静态系统提示+无状态会话是天花板**——"写完 prompt 不再变"=学不到偏好；"记忆演化补上"=跨会话个性化；会话是工作台、记忆是档案柜。
- **提升层**：模型/工作流（跨会话 web 记忆）。

## 会话与记忆分型：workbench vs filing cabinet、三层记忆、freshness（来源：Alex Ostrovskyy sessions vs memory + augmentable 2026 三层 + Mem0 freshness/user_id 治理 2026 实拉，r635B 落地，与 §记忆分层分工——那边管"分几层"，本条管"session 与 memory 的边界与新鲜度"）
- **session 与 memory 二分**：**session=短期"工作台"——单次对话即时、详细、瞬态的对话历史；memory=长期"档案柜"——跨多个 session 精选、整合、持久的知识，用于长期个性化**（Alex Ostrovskyy）→ 判据：**瞬态与持久分开管**——"把对话历史当长期记忆"=档案柜爆满；"session 细节不入 memory、整合后入"=各归其位；工作台可清、档案柜要精选。
- **2026 三层**：**episodic（短期 session 状态）/semantic（长期事实与偏好）/procedural（静态指令文件）；context window 是 buffer 不是 memory——每工具按形态分工：Claude 缓存工作记忆、Cursor Merkle 树索引代码、Copilot/Codex 跨会话持久、LangGraph checkpoint 图状态、Mem0 统一**（augmentable + Mastra）→ 判据：**工具按记忆形态选**——"全栈一个接口"=形态不匹配；"episodic 用缓存、semantic 用向量、procedural 用文件"=各管一段；context window 只是缓冲不是记忆本体。
- **freshness 与 user 隔离**：**Mem0：只有相关不够——底层事实过期时相关也误人（staleness）；user_id 让同 agent 多用户累积独立记忆 profile（也是治理关注）；跨会话 semantic recall 用向量检索同用户任一先线程**（Mem0 + Mastra）→ 判据：**新鲜度与相关性并列**——"只查相关不查新鲜"=过期事实照答；"召回时校验时效"=结论可信；多用户必须按 user_id 隔离，隔离即治理。
- **提升层**：工作流/可复用 Skill（会话与记忆分型）。

## 记忆引擎选型与 token 形态：latent memory、Observer/Reflect、轨迹检索参数（来源：Mem-W arXiv 2605.09317 + Mastra Observer/Reflect + Mem0 library 多轮上下文 2026 实拉，r635B 落地，与 §记忆库形态分工——那边管"记忆库怎么组织"，本条管"记忆引擎的机制参数与后台维护"）
- **latent memory 参数化**：**Mem-W（memory-native GUI agents）：潜在记忆 token K=8、working memory window L=3、chunk size W=4、检索轨迹数 M=5——记忆以隐式 token 形式进推理而非明文拼接**（Mem-W）→ 判据：**记忆有显式参数**——"隐式记忆无参"=不可调不可复现；"K/L/W/M 显式"=按任务调窗口与检索量；token 形态省显存但牺牲可解释。
- **后台压缩 agents**：**Mastra Observational memory：Observer+Reflect 两个后台压缩 agent——Observer 观察、Reflect 反思提炼，把会话沉淀进语义记忆**（Mastra）→ 判据：**记忆维护是独立角色**——"主 agent 自己顺手记"=注意力被占；"Observer/Reflect 后台专职"=提炼不打断主循环；压缩是异步后台任务。
- **多轮上下文工程**：**Mem0：relevance 之外要管 freshness、context window 预算、user_id 多用户 profile 分离；提取→校验→整合是记忆流水线（不是每轮追加）**（Mem0）→ 判据：**记忆是流水线不是追加**——"每轮对话都写长期记忆"=噪声累积；"提取→校验→整合"=只有值得长期存的入库；窗口预算、时效、身份三者在召回时一起判。
- **提升层**：工具/模型（记忆引擎选型）。

## Skill 标准与治理：中性基金会、审计元组、Skill Workshop（来源：Agentic AI Foundation 移交 + ClawHub audit tuples + Skill Workshop propose + 企业预审清单 2026 实拉，r635C 落地，与 §技能治理分工——那边管"本库技能备份/批量/质量"，本条管"行业标准与市场级治理"）
- **标准中立化**：**2026-10-22 Agent Skills 移交 Agentic AI Foundation（Linux Foundation 中性治理，与 MCP 并列），vendor-neutral，70+ 平台采用；标准定义：文件夹结构（SKILL.md+scripts/references/assets）、YAML frontmatter、三级加载、命名规范；标准不定义：发现/分发/计费/质量监控——"SKILL.md 正在变成 agent 的 package.json"**（DEV + claw0x）→ 判据：**格式中立可移植**——"技能绑死一个 agent"=平台锁定；"只依赖标准定义的部分"=换 agent 不重写；发现/计费/质量是生态层不是标准层。
- **市场治理**：**ClawHub 官方 registry：可安装版本化技能（publisher 细节/扫描信号/更新历史）；企业治理=policy conformance with audit tuples（policy/evidence/findings/result hashes）+allowlist+pin versions+stage rollouts with approvals；上传前预审清单：权限显式（fs/shell/browser/network/channel/API）/回滚路径存在/受影响自动化（cron/subagent/channel）已识别/owner 具名**（Skywork + Lobsterland）→ 判据：**技能是资产不是文件**——"装完就忘"=坏了没法回滚；"audit tuples+pin 版本+分阶段上线"=可审计可回滚；每个技能必须具名 owner。
- **评审流控**：**Skill Workshop：propose 模式后台评审可暂存一个待审提案，nothing goes live until applied（默认 auto 学习开启，off 可关后台学习只留 /learn 手动）——技能生成走提案-评审-应用，不直接生效**（ClawDocs）→ 判据：**技能变更走评审**——"后台学到就直接改"=未审内容上线；"propose 暂存+显式 apply"=有人把关；学习默认开但生效必须显式。
- **提升层**：工作流/可复用 Skill（Skill 标准与治理）。

## 技能编写与成本纪律：跨 agent 可移植、config 与逻辑分离、token 预算（来源：NiteAgent SKILL.md authoring + DEV one-SKILL.md-every-agent + Elegant config 分离 + OpenClaw creating-skills 2026 实拉，r635C 落地，与 §技能评测分工——那边管"触发与激活怎么测"，本条管"技能怎么写得省、写得不脆"）
- **token 预算**：**每个已装 skill 启动约 100 token（name+description metadata）；完整 SKILL.md body 只在激活时加载、应 <5000 token；references/assets/scripts 按需加载；SKILL.md <500 行保上下文**（NiteAgent）→ 判据：**描述级加载+内容按需**——"把全文塞 metadata"=每个技能都烧 5000 token；"三级加载"=启动只付 100 token；体量与行数上限是硬预算。
- **跨 agent 可移植三条件**：**只用 spec 的 frontmatter 字段；住在共享 .agents/skills 文件夹；复制或链接进各 agent 自己的文件夹；name 规范：max 64 字符小写字母/数字/连字符、禁止 anthropic/claude 词、不得以连字符开头/结尾、name 匹配文件夹名；description ≤1024 无 XML 字符**（DEV + Collective Brain）→ 判据：**可移植=守 spec**——"用自家扩展字段"=别家 agent 读不了；"共享文件夹+链接"=一处维护多处生效；命名规范是上传硬门槛。
- **config 与逻辑分离**：**技能配置声明式、外部化、易审阅——平台验证/加载/安装策略变化不强制改技能核心行为；把运行时假设硬编码进 skill=升级断点；Be concise（教模型做什么，不是怎么当 AI）；exec 防任意命令注入；openclaw agent --message 先本地测试再分享；先 ClawHub 找现成再自建**（Elegant + OpenClaw）→ 判据：**配置不混进指令**——"运行时假设写死进 SKILL.md"=平台一变就碎；"声明式配置分层"=升级只动配置；发布前必须本地实测。
- **提升层**：可复用 Skill（技能编写与成本纪律）。

## 群体技能结晶与自动进化：Ultron 再结晶、Replay2Skill 回放成技（来源：ModelScope Ultron 群体智能 + Replay2Skill Forge 2026 实拉，r635C 落地，与 §重复工作流固化分工——那边管"先手动跑再编码、阈值 3+ 次"，本条管"高频记忆自动结晶为技能与回放编译"）
- **自动结晶**：**Ultron：高频记忆通过语义聚类自动结晶为工作流技能；技能上线后不固化——新证据积累触发再结晶持续进化，溯源验证+结构分数门控确保只升不降；免人工整理或编写复杂 SKILL.md**（智源/ModelScope）→ 判据：**记忆结晶是自动化**——"技能全靠手写"=沉淀慢；"高频记忆语义聚类→技能+新证据再结晶"=持续演化；门控保证只升不降。
- **回放成技**：**Replay2Skill Forge：把已成功且用户验收的 Agent 任务转化为可审阅/可测试/可导出的标准 Skill 预览包（本地 AI PC 运行）——成功的任务回放编译成技能**（ModelScope）→ 判据：**验收过的任务=技能原料**——"跑完就忘"=经验流失；"验收任务回放编译"=可复现技能；转化产物可审阅可测试再导出。
- **生态打通**：**Ultron 打通 ModelScope Skill Hub 统一检索 80000+ 外部技能——既能复用团队内部沉淀经验，也能无缝接入外部生态；ms-agent>=1.4.0 create_agent_skill 一键装配**（智源 + ModelScope）→ 判据：**内部沉淀+外部生态双通道**——"只存内部"=错过外部现成；"统一检索内部+外部"=按需取用；结晶产物与外部技能同格式可互装。
- **提升层**：模型/工作流（群体技能结晶）。

## 语音评测四层与观测指标：只测 LLM 输出漏掉 80% 体验（来源：Future AGI + TestMu + LangSmith + Prodinit + Smallest.ai 2026 实拉，r636A 落地，与 §评测方法论分工——那边管"通用 agent 评测"，本条管"语音特有指标层"）
- **四层监控**：**基础设施（按组件延迟/丢包/并发）、模型性能（按口音和噪音分段的 WER、LLM 任务完成率与幻觉率、TTS MOS 与发音错误率）、UX（首次解决率/放弃率/平均处理时长/CSAT/升级率）、业务（每次解决成本/包含率/收入影响）——只测 LLM 输出漏掉用户实际体验的 80%**（Future AGI + Prodinit）→ 判据：**体验层是主体**——"只看 LLM 质量"=漏掉语音/网络/UX；"四层分测"=归因到组件；WER 按口音噪音分段才找得出真问题。
- **关键阈值**：**TTFW <800ms（响应性）；WER <5%（防 agent 对错误输入响应）；关键事实 HUN（幻觉+不安全响应）率接近 0%（已知答案测试集对 ground truth）；barge-in 误报率是最被低估的指标——因背景噪音错误停句一次，信任当通不恢复**（TestMu + Smallest.ai + Prodinit）→ 判据：**指标带阈值才算数**——"记录 WER 但不设线"=漂移看不见；"TTFW/WER/HUN 三线"=质量有界；误报率单独盯。
- **12 层测试法**：**真实电话+多样口音噪音，check 12 层：电话/音频质量/STT/轮次控制/延迟/理解/接地/语音输出/安全/负载/回归/生产监控；每个关键场景至少跑 5 次、全过才 pass**（TestMu）→ 判据：**语音要真打真听**——"模拟器测语音"=漏真实链路；"真实呼叫 5 次全过"=验收门槛；12 层含安全与负载不是纯对话质量。
- **提升层**：工作流/可复用 Skill（语音评测四层）。

## 语音 Agent 上下文与记忆：短提示与记忆的张力、会话数据跨轮、多 agent 语音编排（来源：Relinns + n8n VAPI with memory + Google ADK + LangSmith experience + 智子角色一致 2026 实拉，r636A 落地，与 §记忆分层分工——那边管"通用记忆分层"，本条管"语音场景上下文预算与跨轮状态"）
- **短提示 vs 记忆张力**：**语音延迟优先→system prompt <500 tokens；但长记忆/角色一致性要跨轮保留——用外部 session 数据传递而非塞 prompt；n8n 模式：VAPI Function Tool 把 user query+session data 发给 workflow，assistant 回调工具取上下文**（Relinns + n8n）→ 判据：**上下文外置不内置**——"全塞进语音 prompt"=延迟爆；"query+session data 外置回调"=短提示+记忆兼得；语音的 prompt 是缓存友好的稳定前缀。
- **多 agent 语音编排**：**ADK：实时语音+外部工具数据，planner/researcher/writer 多 agent 编排；生产化=guardrails+persistent memory+自动评测+Agent Engine 部署；LangSmith 体验层评估（响应性/自然度/会话摩擦）匹配评估器到信号**（deeplearning.ai ADK + LangSmith）→ 判据：**语音也能拆 agent**——"语音=单 agent 单模型"=复杂任务扛不住；"planner/researcher/writer 语音编排"=分工；体验评估器（自然度/摩擦）是语音特有信号。
- **角色一致与记忆延续**：**角色型语音 agent：人格表达+世界观知识+对话记忆深度结合，跨次对话连贯（智子 Agent 1.0 三体宇宙）——记忆是角色一致性的载体**（上观新闻）→ 判据：**语音人格=记忆+风格双持久**——"只调风格不存记忆"=每次都是陌生人；"世界观知识+对话记忆入库"=跨会话人设稳定；记忆检索在响应前注入。
- **提升层**：工作流（语音上下文与记忆）。

## 语音安全与合规：转录即文本注入面、唤醒词面、录音合规（来源：Smallest.ai compliance + TestMu security layer + OpenAI audio path + 火山引擎约束 2026 实拉，r636A 落地，与 §Agent 安全纵深分工——那边管"文本注入与工具面"，本条管"语音侧特有注入面与合规"）
- **转录即注入**：**语音管线的注入面=STT 转录文本进入 LLM 的那一刻——背景人声/恶意音频可携带指令，与文本注入同源；语音输出端也要接地检查（grounding）防模型复述恶意指令**（TestMu 12 层含理解/接地/安全）→ 判据：**语音不豁免注入**——"音频来源就安全"=谬误；"转录进 LLM 前同文本消毒"=注入面收窄；接地层防复述。
- **唤醒词与误触发面**：**wake word（"hey claw"）与 push-to-talk 是常驻监听面——macOS 需 Accessibility/Input Monitoring 权限全局检测按键；误触发=隐私/尴尬双损失**（OpenClaw Playbook）→ 判据：**监听面最小化**——"常开无唤醒词"=持续录音面；"显式按键/唤醒词+权限提示"=用户知情；权限弹窗是用户控制点。
- **录音与转录合规**：**企业语音 agent 必须遵循合规规则（不只是功能）；录音/转录含 PII 须最小化留存与访问控制；HUN 率含不安全响应项**（Smallest.ai）→ 判据：**录音是敏感数据**——"转录文本当普通日志"=PII 泄漏；"最小化留存+访问控制"=合规底线；语音测试集含不安全响应检测。
- **提升层**：模型/工具（语音安全与合规）。

## 微调数据质量与防过拟合：数据集是主驱动、holdout 纪律、记忆化诊断（来源：AI Learning Hub + nanobase + Sozee + Forgetting on Purpose + dev.to 2026 实拉，r636B 落地，与 §评测数据质量分工——那边管"评测集怎么建"，本条管"微调训练集质量与防过拟合"）
- **数据质量清单**：**数据集质量是微调成功主驱动：200 条仔细审过的例子胜过更多垃圾；清单=每条响应正确（领域专家抽样审）/格式语气一致/覆盖多样（含边界和困难例）/长度合适（不含人为过长过短）/system prompt 与推理时匹配**（AI Learning Hub）→ 判据：**先审数据再审模型**——"数据脏先怪模型"=因果倒置；"抽样专家审+一致性+多样性"=数据门槛；system prompt 一致性是隐性要求。
- **防过拟合序列**：**先 hold out 10-20% 验证集（分层代表任务多样性）→保守 LoRA rank 8-16、1-3 epochs（不默认往上调）→每 epoch/几百步跟踪验证 loss，平台或上升即停→过拟合出现才动正则；无 holdout 无停止规则=看不到过拟合；按 holdout 分数选 checkpoint 而非最后 epoch；测试集本身有标签错误（十基准平均 ≥3.3%）**（nanobase + dev.to）→ 判据：**验证集先于训练存在**——"没 holdout 就训"=过拟合隐形；"rank 8-16+1-3 epochs+验证 loss 早停"=保守起步；checkpoint 选优=holdout 说了算。
- **LoRA 记忆化五线索**：**LoRA 完美复现训练图=记忆设备非好模型；五线索诊断从学习滑向记忆：base 能力退化/概念窄化/caption 僵化/纠缠泄漏/视觉签名复现；照片写实 LoRA 最优 15-40 图，姿势/光照/表情多样防 identity drift 与塑料皮肤**（Forgetting on Purpose + Sozee）→ 判据：**泛化是质量判据**——"复现训练集"=过拟合；"五线索查记忆化"=学习 vs 记忆可诊断；小图集多样性保身份不漂移。
- **提升层**：工作流/可复用 Skill（微调数据与防过拟合）。

## 微调评估与 RL 后训练：LoRA 测试协议、GRPO 推理强化、蒸馏（来源：aiofm + deeplearning.ai GRPO/Post-training + Hyperion 2026 实拉，r636B 落地，与 §微调数据质量分工——那边管"训练集与防过拟合"，本条管"微调完怎么测、RL 后训练怎么做"）
- **LoRA 测试协议**：**光照泛化测试（untrained lighting 身份是否保持）、权重刻度测试（同 prompt 在 0.5/0.7/0.9/1.1 权重找甜点）——每测试跑 4 seeds，80%+ 输出可识别才算过；泛化测试=模型学没学会概念的直接证据**（aiofm）→ 判据：**测试要打未训练域**——"只测训练分布"=自证；"光照泛化+权重刻度+4 seeds"=稳健性证据；80% 阈值是接受线。
- **RL 后训练**：**GRPO：强化微调用奖励函数提升 LLM 推理（Predibase 1h43m）；Post-training 全谱：SFT→DPO→online RL 适配任务行为；Fine-tuning & RL 课程线：数据准备→PEFT→RL rewards/preference learning；DPO 数据集 prompt/chosen/rejected+preference accuracy 早停**（deeplearning.ai + Hyperion）→ 判据：**推理提升走奖励**——"SFT 数据堆"=推理提升有限；"GRPO 奖励函数"=显式优化推理；后训练谱系 SFT/DPO/RL 各管一段。
- **蒸馏与合成数据**：**模型蒸馏：大模型教小模型（teacher logits/偏好对）压成本提延迟；合成数据：生成 prompt 是决定成败的一环——弱 prompt 产生窄重复数据集，好 prompt 产生多样现实示例（指定任务类型+输出格式）**（Hyperion + AI/TLDR）→ 判据：**蒸馏是压缩不是复制**——"直接搬 logits"=容量浪费；"teacher 知识+偏好对蒸馏"=小模型提能力；合成数据质量上限=生成 prompt。
- **提升层**：模型/工作流（微调评估与 RL 后训练）。

## 视频生成评估体系：盲人偏好、VLM 自动评估、rubric 统一（来源：WorldJen + MemoBench + CVPR 2026 survey + VideoArgus + THEval + Sozee 2026 实拉，r636B 落地，与 §语音评测四层分工——那边管"语音特有指标"，本条管"视频生成质量评估"）
- **人类偏好基准**：**盲人偏好研究：2696 成对标注/7 标注者/50 prompt×6 模型 100% 覆盖，标注者间一致 66.9%→人类 ground-truth Bradley-Terry 三级结构；HPS v2：CLIP 微调于大规模人类选择数据（跨图像分布泛化）；MPS 多维偏好：美学/语义对齐/细节质量三维度分离**（WorldJen + CVPR survey）→ 判据：**视频质量以人类偏好为锚**——"自动指标独断"=偏离感知；"BT 三级+成对盲审"=基准可信；标注者一致 ~67% 说明多模型难分。
- **自动评估与一致性**：**VLM 自动评估对齐人类偏好（WorldJen 第二支柱）；VideoArgus：agentic rubric-grounded 统一评估——1260 视频人类对齐集上五任务（生成+编辑）相关性高于基准专用评估器，rubric 生成与评估 VLM 骨干不同但模型排名大体一致（rubric 可移植）；THEval：talking head 三维度 8 细粒度指标（quality/naturalness/synchronization）Spearman ρ=0.87**（VideoArgus + THEval）→ 判据：**评估要接地人类信号**——"单指标打天下"=维度漏；"rubric-grounded+骨干无关"=可移植；talking head 音画同步单独测。
- **世界模型与记忆一致性**：**MemoBench：动态变化环境 360 ground-truth clips（合成+真实），自动指标+VQA 四诊断支柱，disappear-and-reappear 范式测记忆一致性（人类验证 92.9% 一致 κ=0.85）——物体消失再出现是否保持一致**（MemoBench）→ 判据：**视频一致性含时序**——"单帧质量高"=时序记忆漏；"disappear-and-reappear 测记忆"=长时一致有界；物体再出现一致性是生成世界模型的短板。
- **提升层**：工作流/可复用 Skill（视频生成评估体系）。

## 引用验证与幻觉检测三层法：存在性/归因/相关性、多模型交叉（来源：Clarity + arXiv 2607.22693 + urlhealth + CheckIfExist + PromptQuorum 2026 实拉，r636C 落地，与 §事实核查分工——那边管"回答内容查证"，本条管"引用/来源层专门验证"）
- **三层验证法**：**有效引用验证=三层层层过：存在性（来源存在吗）/归因（它真说了文本声称的吗）/相关性（它真支持具体论点吗）——缺一层就漏一类幻觉**（Clarity）→ 判据：**引用检查是三层不是一层**——"只查存在"=归因/相关性幻觉漏；"存在→归因→相关"=逐层筛；任何一层不过=引用不合格。
- **多模型交叉验证**：**同一研究问题同时跑 GPT-5.6/Claude Opus 5/Gemini 3.1 Pro——独立模型极少捏造同一具体虚假声明；跨模型结果一致才采信**（PromptQuorum）→ 判据：**单模型自证不成立**——"一个模型说找到"=可能同源幻觉；"多模型交叉+零共享上下文"=异源证据；Rivalry Engine 式对抗审查暴露单模型漏网。
- **自动化工具与其边界**：**urlhealth（开源）：URL 活性检查+stale-vs-hallucinated 分类（Wayback Machine），agentic 自纠错把非解析引用 URL 降 6-79× 到 <1%（依赖模型工具使用能力）；CheckIfExist：多源级联验证（CrossRef/Semantic Scholar/OpenAlex+字符串相似度）；Scite Smart Citations 标记全文缺支持/对比证据的引用；检测工具性能受限=参考提取错误/元数据不全/数据库覆盖有限/验证结果不一致**（arXiv 2604.03173 + CheckIfExist + Scite + arXiv 2607.22693）→ 判据：**自动化是早期预警非最终裁决**——"工具说存在就过"=漏归因层；"工具预警+人核对归因"=双层；工具局限（提取/元数据/覆盖）已知则用途明确。
- **提升层**：工作流/可复用 Skill（引用验证与幻觉检测）。

## 图像生成自动评估与迭代闭环：图像接地评分、VLM 改 prompt、循环上限（来源：PRISM + BLIP 迭代精修 + Pruna DSPy + FreeAcademy 2026 实拉，r636C 落地，与 §图像生成提示词工程分工——那边管"人工迭代纪律"，本条管"自动评估与闭环"）
- **图像接地自奖励闭环**：**PRISM：Prompt Refinement via Image-grounded Self-rewarding——VLM 生成图像结构化视觉诊断+三维评分（语义一致性/美学质量/人类偏好对齐），把 prompt-image 反馈闭环；自奖励优化（hybrid ideal-point + Chebyshev）**（arXiv 2607.24353）→ 判据：**评估接地在图像上**——"只评 prompt 文本"=没看生成物；"图像视觉诊断+三维评分"=评估有锚；反馈闭环=prompt 越改越准。
- **VLM 迭代精修优于 LLM 盲改**：**VLM（BLIP）分析生成图像+提出修改建议，对齐文本与图像——传统 LLM 改 prompt 是盲改（没看图）；DSPy 自动化：生成图→VLM 对比图 vs 期望 prompt→不匹配则 VLM 建议修订→循环直到匹配（上限 5 次迭代）**（VectMag + Pruna）→ 判据：**改 prompt 前先看图**——"LLM 盲改"=不知道差在哪；"VLM 看图给修改建议"=诊断驱动；自动化循环设上限防无限迭代。
- **迭代成本纪律**：**小批量（4 张非 40 张）→选最接近目标→平实写下错→每次只改一个→5-10 遍胜过 50 次随机；第一代是诊断不是最终结果**（FreeAcademy）→ 判据：**迭代讲成本**——"大炮打鸟"=烧额度；"4 张+每次改一个+5-10 遍"=最小代价收敛；诊断心态=第一次输出是信息不是失败。
- **提升层**：模型/工作流（图像生成自动评估与迭代闭环）。

## 工作区 Agent 与知识结构化：know-how 技能化、前置上下文、治理内容（来源：Google Workspace skills + Gemini at Work + ChatGPT workspace agents + Microsoft 团队知识库 + Obsidian Agent 2026 实拉，r636C 落地，与 §项目级指令文件分工——那边管"项目内指令怎么写"，本条管"个人/团队知识资产化与 Agent 工作区形态"）
- **know-how 技能化**：**Google Workspace skills：可复用 prompts 引导 Gemini 用团队规则/模板/参考文件自动化流程——把个人 know-how 捕获成自动化资产，规模化机构知识不用长培训**（Google Workspace）→ 判据：**工作流沉淀为可复用 prompt**——"know-how 在人脑"=不可扩展；"skills 捕获规则/模板/参考文件"=自动化资产；复用胜过重教。
- **前置上下文与内联工作**：**Gemini agent 提前已知日历/团队/项目/文档关系（被 brief 再开始，不现场探索）；内联工作（email 线程/文档/聊天空间内）；ChatGPT workspace agents（Codex 驱动）云端运行你不在也继续，团队建一次共享迭代改进**（Google Cloud + OpenAI）→ 判据：**agent 先被 brief 再干活**——"现场翻找上下文"=慢且漏；"前置注入日历/团队/文档关系"=一步到位；云端持续运行=任务不随人停。
- **治理内容与知识结构化**：**Copilot/agents 在良好治理内容上表现最佳（团队知识库由 Copilot 和 agents 策展，治理是 AI 表现前提）；Obsidian+Agent：2026 AI Agent 瓶颈不再是模型能力，真正限制生产力=数据质量够不够高+数据结构够不够适合机器使用——本地 Markdown+双链知识组织恰好做好这两点**（Microsoft + 掘金）→ 判据：**知识先结构化再接 agent**——"笔记随手堆"=agent 无米下锅；"本地 Markdown+双链+数据质量"=机器可用；治理内容=agent 表现上限。
- **提升层**：工具/工作流（工作区 Agent 与知识结构化）。

## 数据质量 Agent 化与证据链：无参照清洗、规则生成、四维审计（来源：arXiv 2608.14765 + data-quality-agent-dk + AutoDCWorkflow + 阿里云证据链 + gillilab 2026 实拉，r637A 落地，与 §工具结果断言层分工——那边管"调用结果可疑打标"，本条管"数据本身的质量治理"）
- **无干净参照的 agentic 清洗十组件**：**structured context+profiling+LLM reasoning+executable checks+controlled local evidence retrieval+source ranking+citation alignment+conservative repair+reversible scripts+provenance logging——分离受控合成损坏评估与原始数据描述性评估（126 成功 run/三数据集/七配置）**（arXiv 2608.14765）→ 判据：**没有干净参照也能清洗**——"等干净数据"=卡死；"profiling+可执行检查+证据检索+保守修复+可逆脚本"=有界清洗；provenance logging=改动可追溯。
- **规则从真实证据创建+验证执行**：**data-quality-agent-dk：profile CSVs→从真实证据创建潜在 DQ 规则→每规则生成 SQL→验证→执行（带重试）→JSON 报告确认违规；LLM 非结构化数据质量自动化=采集到服务全程质量门（schema 推断/规则生成/异常检测/元数据更新/自动修复或 review 队列）**（PyPI + gillilab）→ 判据：**规则先于检查**——"凭经验猜问题"=漏真实违规；"profile→证据规则→SQL 验证执行"=闭环；全程质量门=问题在源头拦。
- **四维列审计与证据链告警**：**AutoDCWorkflow 四维：accuracy（明显错误/不一致/偏差）/relevance（对分析目标关键性）/completeness（充分性）/conciseness；AI 质量诊断从告警到证据链：异常表现/关联字段/上游加工节点/计算逻辑变更按逻辑顺序串联——'为什么出错'从推断变可核验链路+自动整改建议+影响范围评估；可行性验证阶段：评估生成规格的现实性与可执行性，必要时迭代精修再执行**（arXiv 2412.06724 + 阿里云 + arXiv 2606.13692）→ 判据：**诊断要证据链不要孤立告警**——"某表某字段异常"=不可核验；"异常+关联字段+上游节点+逻辑变更串联"=可追溯归因；规格先验可执行性=防跑一堆废验证。
- **提升层**：工作流/可复用 Skill（数据质量 Agent 化与证据链）。

## 数据 Agent 评估：轨迹级判断、计划合规、中间里程碑（来源：AD-Bench + DataClawBench + Plan-RewardBench + IBM 计划合规 + deeplearning.ai Building Data Agents 2026 实拉，r637A 落地，与 §评估器先行分工——那边管"评估器先于实现"，本条管"数据 agent 用什么基准和维度评估"）
- **轨迹与里程碑评估**：**AD-Bench：真实营销分析请求+领域专家可验证参考答案+参考工具调用轨迹，三难度级（L1-L3）评估多轮多工具协作；DataClawBench：206 万真实记录（企业/行业/政策域）保留原生噪声+492 智库咨询任务，标注中间里程碑诊断探索/推理失败（超出结果准确率）**（arXiv 2602.14257 + arXiv 2605.02503）→ 判据：**只评最终答案漏探索失败**——"只看结果对错"=路径浪费隐形；"参考轨迹+中间里程碑"=过程可诊断；原生噪声保留=评测贴近真实。
- **轨迹级偏好与硬负样本**：**Plan-RewardBench：判断器区分偏好 vs 干扰轨迹；四任务族（Safety Refusal/Tool-Irrelevance/Complex Planning/Robust Error Recovery）——验证正轨迹+易混淆硬负样本（多模型自然构建）**（arXiv 2604.08178）→ 判据：**判轨迹偏好要硬负样本**——"只看正轨迹"=判不出区别；"偏好 vs 干扰+四任务族"=覆盖面；硬负样本=区分度真实。
- **计划合规与内联评估**：**IBM 计划合规（16991 轨迹/SWE-agent 四 LLM/八计划变体）：无显式计划→agent 回退到训练内化工作流（常不完整/过拟合/不一致应用），提供标准计划提高问题解决率；deeplearning.ai Building Data Agents：design planner+plan executor+专门 sub-agents 连数据源；trace+评估（最终答案质量+目标/计划/行动对齐）；加 inline evaluations 让 agent 运行期调计划**（IBM Research + deeplearning.ai）→ 判据：**计划要显式且被追踪**——"无计划"=回退内化工作流；"planner+executor+对齐评估"=可控；inline evaluations=运行期自调。
- **提升层**：模型/工作流（数据 Agent 评估）。

## 数据分析自动化四象限与个人落地：重复工作流自动化、技能化、成本账（来源：ExcelMaster + DataPilot + QLens + sheetsmith + OpenClaw Sheets + SFAI Labs 2026 实拉，r637A 落地，与 §重复工作流固化分工——那边管"何时固化/四块结构"，本条管"数据分析场景的具体自动化路径"）
- **重复工作流自动化**：**DataPilot：上传 CSV→检查列→缺失值→EDA→训练基线→试另一模型→比较→决定下一步（把高频重复工作流交给 agent）；ExcelMaster：写公式/跑代码/建图/清理数据实时可见，45 分钟手工→2 分钟；QLens：上传 CSV/Excel+自然语言问→洞察/可视化/计算/操作**（DEV + ExcelMaster + QLens）→ 判据：**EDA 管线可脚本化**——"每次手点"=重复；"CSV→列检查→EDA→基线→比较"=固定管线 agent 化；实时可见=信任可建。
- **技能化免重写**：**sheetsmith：Pandas 驱动 CSV/Excel 管理（预览/摘要/过滤/转换/格式转换）——不用每次重写 pandas；col 级摘要/查询/表达式/导出清洗数据 CSV/TSV/XLSX；OpenClaw Google Sheets 对话控制（问预算状态/记支出/生成周报告）**（OpenClaw Skills + getopenclaw）→ 判据：**重复代码技能化**——"每文件重写 pandas"=重复劳动；"sheetsmith 免重写+col 摘要/转换/导出"=一次封装复用；对话读写=低门槛入口。
- **数据分析技能开发纪律**：**验证文件存在+有效 CSV→读前 5 行识别列名类型→数值列 min/max/mean/median/std→文本列 <20 唯一值 value counts→数值列 top3 相关性→数据质量检查——把探测步骤显式编进技能**（SFAI Labs）→ 判据：**技能步骤可枚举**——"隐式凭经验"=不可复现；"前 5 行+数值统计+文本 counts+相关性"=探测路径固定；显式步骤=新人可跑。
- **提升层**：工作流/可复用 Skill（数据分析自动化四象限）。

## CI 失败根因分析 Agent：预处理管线、语义 diff、RCA 共识（来源：LogSage + 四 agent log differencing + LangChain 失败分析器 + 42JerryKim RCA 综述 2026 实拉，r637B 落地，与 §工具结果断言层分工——那边管"单次调用可疑打标"，本条管"CI 失败日志级根因定位"）
- **预处理管线+RAG 修复**：**LogSage（首个端到端 LLM CI/CD RCA+自动修复）：token 高效日志预处理管线（过滤噪声提取关键错误）→结构化诊断 prompt 精确 RCA→RAG 生成解决方案（检索历史修复）**（arXiv 2506.03691）→ 判据：**日志先瘦身再诊断**——"500 行日志整段进"=token 爆炸+噪声淹信号；"预处理过滤噪声+提取关键错误"=诊断聚焦；RAG 历史修复=复用同型失败方案。
- **四 agent 语义 diff 管线**：**Agent1 context seeding→Agent2 语义对比（vs 传统文本 diff，LLM 深层语义 diff 隔离关键错误）→Agent3 根因总结（差异合成简洁自然语言根因）→Agent4 自动修复建议；LangChain 失败分析器：读 CI 失败日志→诊断根因→PR 上发布清晰解释+修复建议（500 行 npm install 失败/K8s 部署超时无明确原因/junior 工程师 2 小时调试）**（TDC + DevOpsBoys）→ 判据：**语义 diff 优于文本 diff**——"文本 diff"=同名同位置≠同因；"语义对比隔离关键错误"=跨层归因；修复建议回贴 PR=闭环。
- **RCA 日志方法共识**：**Microsoft/Meta/ByteDance 各自不同方式收敛同一模式：都不把日志整段给 LLM——'解析→异常检测→搜索缩小候选→LLM 推理'**（42JerryKim）→ 判据：**LLM 只吃缩小后的候选**——"整段日志"=上下文污染；"解析→异常→搜索缩小→LLM"=先机器后模型；三家收敛=模式可信。
- **提升层**：工作流/可复用 Skill（CI 失败根因分析 Agent）。

## Agent 测试金字塔与分层策略：成本分层、语义评估、影子测试（来源：CheckAgent + AWS Well-Architected Agentic Lens + Omnithium + RapidClaw + AgentMarketCap 2026 实拉，r637B 落地，与 §评测信封分工——那边管"评测覆盖范围"，本条管"agent 测试的分层结构与成本分配"）
- **成本分层比例**：**健康 agent 测试套件分布：Mock 80%（免费快速最大化覆盖）/Replay 15%（真实轨迹回归网）/Eval 4%（质量测量——merge 时跑非 commit）/Judge 1%（统计质量门——release 保留）；不是任意比例是成本-价值分层**（CheckAgent）→ 判据：**比例按成本价值分配**——"全部真模型测"=贵且慢；"Mock 为主+Replay 回归+Eval merge 时+Judge release"=成本与价值对齐；比例背后=每层触发时机不同。
- **语义评估与分层结构**：**AWS Agentic Lens：单元/集成/e2e/shadow 测试（生产环境）；自动化管线每代码和配置变更跑；覆盖指标跟踪维持阈值；语义质量评估而非精确匹配——非确定性输出不破坏套件；单元测试（tools）每 commit 验证 tool I/O/错误处理/边界**（AWS + RapidClaw）→ 判据：**非确定性输出用语义评估**——"精确匹配"=输出抖动破坏套件；"语义质量评估"=判断意图而非字面；shadow 生产=真实流量验证。
- **落地路径与场景测试**：**第一周：提取所有现有手工测试到 golden dataset+识别编排逻辑→第二周：3-5 高风险 prompt 构建约束组件 evals（temperature=0/结构化输出/客观可验证用例）+路径特定触发器集成 CI；场景行为测试=端到端但非 happy-path——对抗性多轮设计暴露 misalignment，从真实用户旅程建套件（客户争议扣款/开发者请求 review）**（AgentMarketCap + Omnithium）→ 判据：**测试金字塔可周级落地**——"一次建完"=不可行；"W1 golden 数据→W2 高风险 evals+CI 触发"=渐进；对抗场景=暴露规则破坏。
- **提升层**：工作流/可复用 Skill（Agent 测试金字塔与分层策略）。

## 测试自治分级与 QA 工程：三层自治、最高 ROI、评估文档共享（来源：QASkills + SoftwareTestPilot + qaa-agent + NobleProg 2026 实拉，r637B 落地）
- **三层自治分级**：**Tier1 完全自主（人类审周报不批单个测试）；Tier2 监督自治（新功能/关键旅程——agent 生成测试提案，QA 工程师批准/修改/拒绝后进活跃套件）；Tier3 人写（合规/安全/监管领域可选 AI 辅助）——按领域风险分配自治度**（QASkills）→ 判据：**自治度按风险分级**——"全自动全领域"=合规区失控；"完全自主/监督自治/人写"=风险匹配；监管领域人写=责任清晰。
- **最高 ROI 与 prompt 框架**：**2026 单元测试是 QA 最高 ROI 的 AI 用途：单元测试小而确定易审查+LLM 有百万开源示例可模仿；RCTF prompt 框架团队一致命中；测试生成让生成测试'像 codebase 本地的不通用'——先产评估文档（test_assessment/coverage_gaps）下游 agent 都读**（SoftwareTestPilot + qaa-agent）→ 判据：**先评估后生成**——"直接生成"=通用风格不贴代码库；"先 test_assessment+coverage_gaps 再生成"=上下文共享；RCTF 框架=一致质量。
- **技能测试纪律**：**skill 测试方法=sample inputs/expected outputs/error handling/documentation；OpenClaw 行为测试：完整行为测试+文档化评估（可靠性/外部渠道部署就绪）；系统性测试跨场景+证据为基础改进（受控变更+重测）+回归测试确保改进不破坏**（NobleProg + UandWorld）→ 判据：**技能验收=四件套**——"只测 happy path"=错误处理漏；"sample inputs/expected outputs/error handling/docs"=完整验收；改进后回归=不破坏旧行为。
- **提升层**：工作流/可复用 Skill（测试自治分级与 QA 工程）。

## 红队基准与漏洞正交性：数据集聚合、攻击类型有效性、注入与越狱分开测（来源：RedBench + Adaptive Adversaries + SAFEDIALBENCH + ACM 注入越狱 + AI Security Leaderboard + HarDBench 2026 实拉，r637C 落地，与 §数据 Agent 评估分工——那边管"数据 agent 基准维度"，本条管"红队基准与攻击类型测法"）
- **数据集聚合与标准化**：**RedBench：聚合 37 基准数据集（顶会+仓库）29362 样本（攻击+拒绝 prompts），标准化 22 风险类/19 域——一致全面评估 LLM 漏洞+现代 LLM 基线；AI Security Leaderboard：四模型（Claude Fable 5/GPT-5.6 Sol/Gemini 3.1 Pro/Grok 4.5）360 攻击目标（CBRNE+进攻性网络攻击）+三阶段筛选识别'通用越狱'**（arXiv 2601.03699 + 智源）→ 判据：**红队基线要聚合标准化**——"单数据集"=覆盖偏斜；"37 集聚合+22 风险类+标准分类"=可比基线；通用越狱筛选=跨目标可迁移。
- **攻击类型有效性与模型差异**：**SAFEDIALBENCH（多轮+多样越狱）：fallacy attack/purpose reverse/role play 成功破坏安全；topic change/reference attack 最小有效；GLM4-9B/Yi-34B 全攻击鲁棒；ChatGPT-4o 对 fallacy 有显著漏洞——攻击有效性模型特异；ACM：prompt injection 与 jailbreak 正交漏洞——0% 注入漏洞的模型可严重 jailbreak 漏洞（Llama3.2:3B：0% 注入，69.2% 越狱）**（ICLR + ACM）→ 判据：**注入与越狱分开评估**——"注入 0% 就放心"=漏 69.2% 越狱；"攻击类型×模型矩阵"=漏洞画像；正交漏洞=各自防线。
- **多轮基准方法学**：**Adaptive Adversaries：21 场景多轮自适应（攻击者观察响应 pivot；每 defender 响应作新鲜交互评估；只评第一轮 ASR 0-1% vs 15 轮显著提升）——基准必须允许多轮；HarDBench：基于草稿的共同写作越狱（1204 验证草稿：爆炸物/毒品/武器/网络攻击）——安全-效用对齐实验**（arXiv 2607.18063 + arXiv 2604.19274）→ 判据：**基准要测自适应**——"单轮 ASR"=低估；"多轮+新鲜交互评估"=真实威胁；协作写作场景=新攻击面。
- **提升层**：模型/工作流（红队基准与漏洞正交性）。

## CI/CD LLM 安全集成与工具生态：shift-left 三阶段、PR 门禁、扫描工具（来源：SecureTom + Promptfoo + garak-sdk + ModelAudit 2026 实拉，r637C 落地，与 §CI 失败根因分析分工——那边管"CI 失败日志 RCA"，本条管"CI 里主动扫描 LLM 安全"）
- **shift-left 三阶段**：**PR gate（Promptfoo 快速聚焦）→staging 行为测试（Garak 完整 probe 库——数百 probes：hallucination/data leakage/prompt injection/misinformation/toxicity/jailbreaks/encoding-based bypass）→（DeepTeam）——PR 快、staging 穷尽**（SecureTom）→ 判据：**扫描强度按阶段分**——"全量扫 PR"=慢；"PR 快速门禁+staging 穷尽扫描"=分层；probe 库覆盖多种类=不只见注入。
- **PR 门禁与代码扫描**：**Promptfoo GitHub Action：自动扫描 PR 代码变更——prompt injection/PII exposure/excessive agency 等 LLM 特定风险；findings 带严重级别+建议修复作为 PR review 评论；quality gates 强制最低性能阈值+OWASP 合规报告；ModelAudit：部署前扫描 ML 模型文件（--strict 模式 warnings/critical 即失败）**（Promptfoo + promptfoo scan-model）→ 判据：**安全扫描进 PR 流程**——"部署后才查"=泄漏已发生；"PR review 评论带严重级+修复建议"=开发者就地改；--strict=门禁严格度显式。
- **工具形态与集成**：**garak-sdk：安全扫描+多 generator（OpenAI/Anthropic/HF）+probe 类别（jailbreaks/harmful content/privacy violations）+JSON/JSONL/HTML 报告+CI 集成——自动化与连续集成为内建；Garak（NVIDIA 开源）：120+ probes 深度漏洞研究模型评估（agentic/RAG 覆盖有限）；PyRIT（Microsoft MIT）：Python 自定义多轮攻击编排（Crescendo/TAP）无固定攻击库——orchestration layer；DeepTeam：最清晰 OWASP LLM Top 10 映射+最简单 onboarding**（garak-sdk + BeyondScale + Repello）→ 判据：**工具按用途选**——"固定攻击库"=受限；"Garak 穷尽扫描/PyRIT 自定义编排/Promptfoo PR 门禁/DeepTeam OWASP 映射"=各司其职；CI 内建=扫描不靠手工。
- **提升层**：工具/工作流（CI/CD LLM 安全集成与工具生态）。

## 红队披露与合规闭环：90 天窗口、报告标准、残余风险决策（来源：2026 披露框架 + EU AI Act CoP + Cloudstreet 披露伦理 + RockB + Biosecurity Handbook 2026 实拉，r637C 落地，与 §红队框架分工——那边管"怎么攻"，本条管"发现后怎么披露收尾"）
- **披露流程与窗口**：**2026 AI 漏洞披露框架：通知受影响方（全技术细节+PoC）→90 天修复期（关键基础设施可延长）→公开披露前协调（CVE 通过 MITRE 分配）→发现团队认可（赏金/公开致谢）；ISO/IEC 29147:2026+AI Incident Database 最佳实践**（bgnews24 + RockB）→ 判据：**披露是流程不是动作**——"直接公开"=patch 窗口 forfeit；"全细节 PoC→90 天→协调 CVE"=责任闭环；赏金/致谢=激励持续发现。
- **报告标准与伦理**：**'The model said this is a bug'不是报告——'文件/行/触发输入/攻击者可做什么/演示测试用例'才是报告；诚实披露工具（若模型写的说明）；评估应标识确切模型/系统配置/访问模式/工具/评估资源/测试日期；结果是引发能力下界+时间有界快照**（Cloudstreet + Biosecurity）→ 判据：**报告要可复现**——"模型说有问题"=不可验证；"文件+行+触发输入+影响+测试用例"=可复现可修复；快照标注=结论不过期。
- **强制重测与残余风险**：**EU AI Act GPAI CoP S-04 强制重测触发：模型材料变更（重训改能力画像/微调影响五类别/架构修改/安全对齐变化）——'material change'对最后部署门能力画像评估非固定阈值；新高风险部署上下文；红队以残余风险决策结束：定义修复/重测/监控/事件响应义务**（sota + Biosecurity）→ 判据：**红队要有收尾状态**——"测完即散"=风险无主；"残余风险决策+修复/重测/监控/事件响应义务"=闭环；材料变更强制重测=评估不过期。
- **提升层**：工作流/可复用 Skill（红队披露与合规闭环）。

## 路由评估与基准：Pareto 移动、成本削减 workload 特异、成本质量旋钮（来源：LLMRouterBench + RouteLLM 基准 + LiteLLM Auto Routing + Brick + Cascade Routing 2026 实拉，r638A 落地，与 §数据 Agent 评估分工——那边管"数据 agent 基准维度"，本条管"路由器的评估方法与收益口径"）
- **路由器评估要看 Pareto 与互补性**：**LLMRouterBench：top 路由方法平均精度 +4% over Best Single +31.7% 成本削减匹配 Best Single 性能——增益不普适；强 Router 移动 Pareto 前沿（GPT-5 65.96/RouteLLM 67.67/GraphRouter 67.79/Avengers-Pro 68.58/Dataset Oracle 69.16/Instance Oracle 85.66）——Instance Oracle 远高于 Dataset Oracle=实例级模型互补性才是收益来源**（arXiv 2601.07206 + CSDN）→ 判据：**评估报告要看 Pareto 前沿与 Oracle 上界**——"单点成本/精度"=看不出收益；"+4% 精度 31.7% 成本"=互补性收益；"Instance vs Dataset Oracle"=路由潜力上界。
- **成本削减因 workload 而异**：**RouteLLM 基准：MT-Bench 85% 成本削减/95% GPT-4 质量；MMLU 45%/92%；GSM8K 35%——简单 chat 路由远多查询到便宜模型 vs 数学重活；成本削减变化按 workload（LiteLLM cost ladders：58% 节省时语义 router 46.8% win rate vs complexity_router 41.5%——同成本更保质量）**（klymentiev + LiteLLM）→ 判据：**路由收益按 workload 报**——"统一宣称 85%"=误导；"chat vs math 分档"=真实收益；同成本比质量=router 对比口径。
- **成本质量旋钮连续可调**：**Brick：cost-quality knob 暴露连续权衡——低档超 FrugalGPT 69.42% +2.20pp 同成本；中档 74.11% 4.71× 低成本仅 0.91pp 精度损失；Cascade Routing 统一框架（routing+cascading 理论最优策略——质量估计器=模型选择成功关键）**（arXiv 2606.13241 + arXiv 2410.10347）→ 判据：**路由要暴露可调旋钮**——"固定档"=无法按预算调；"连续 cost-quality 权衡"=预算/质量灵活；估计器决定范式上限。
- **提升层**：模型/工作流（路由评估与基准）。

## 网关生产陷阱与观测：钉版本、semaphore 死锁、路由四维（来源：ZonFlip + FAILUREATLAS + CNBPA + OTel GenAI + inapps 2026 实拉，r638A 落地，与 §工具结果断言层分工——那边管"调用后结果合理性"，本条管"网关层生产陷阱"）
- **钉版本是生产强制**：**每个生产 API 调用用全限定版本化模型标识符——不用 alias/latest/短名；dated/hash-pinned 版本；模型版本变更=major dependency upgrade：staging+eval suite+canary 再全量；prompt 开发像 feature branch：新版本分支+CI eval suite+merge 门**（ZonFlip + inapps）→ 判据：**生产钉死版本**——"latest"=提供商静默更新改行为；"全限定版本+eval+canary"=变更受控；prompt 分支=可回滚。
- **网关失败模式**：**FAILUREATLAS：Redis semaphore leak→rate-limit deadlock——网关 Redis-backed semaphore 跟踪 in-flight（max_parallel_requests），上游 provider timeout/5xx 错误处理路径 bypass decrement→'active' count stranded 死锁；避免 mid-stream retries（输出字节已到客户端后）；rate-limit thrashing+missing token attribution（直连多 provider 单 API key）**（arXiv 2607.17525 + dev.to）→ 判据：**错误处理路径必须走清理**——"异常路径 bypass decrement"=计数泄漏死锁；"输出已到客户端"=重试破坏流；token 归属=按请求记账。
- **路由四维与观测**：**路由模型四维：模型能力（文本/向量/代码/多模态/重排）、模型版本（稳定/候选/实验/回滚）、租户等级（生产/内部/测试/低优先级批）、资源状态（GPU 利用率/队列长度/实例健康/冷启动）；LLM 观测=为什么模型说它说的（OTel GenAI semantic conventions——比 APM 严格更大的表面）**（CNBPA + maketocreate）→ 判据：**路由决策要可解释**——"只按模型名"=漏版本/租户/资源维度；"四维路由"=完整决策面；观测记录为什么=排障归因。
- **提升层**：工作流/可复用 Skill（网关生产陷阱与观测）。

## 故障切换与优雅降级：failover 四部分、filter-rank-degrade、降级梯（来源：Continuum + TrueFoundry + Belgavi + andrew.ooo + 72Technologies 2026 实拉，r638A 落地，与 §轻量自动化三模式分工——那边管"自动化形态"，本条管"模型故障时怎么降级不断服"）
- **failover 四部分**：**①分类错误（429/500/504/529/连接失败）②指数退避+honor retry-after ③fall back 到能力等价模型——不单是更便宜的 ④agent case：已跑工具调用的 turn 不能简单重放；fallback chains 跨/内 provider（primary→secondary→tertiary 两轴）**（Continuum + TrueFoundry）→ 判据：**fallback 选能力等价**——"换便宜模型"=质量差破坏下游；"已跑工具"=重放=副作用重复；错误分类→退避→等价降级→agent 感知=完整链。
- **filter-rank-degrade 三原则**：**eligibility 是硬过滤；ranking 用实时健康；adapters 双向翻译；无 route 可 deadline 内服务时 degradation ladder 显式降级模式；response envelope：route used/degradation level/output validated against schema——产品展示降级模式不隐藏**（Belgavi）→ 判据：**降级要显式不隐藏**——"悄悄换模型"=用户不知情；"envelope 带 route+level+schema 验证"=可观测可校验；无可用 route=按梯降级。
- **降级梯与验证**：**Tier 3 减范围（跳可选增强返回核心结果）；Tier 4 优雅失败（缓存/模板响应+显式用户消息+排队重试）——跳过这步的团队 incident 时发现 fallback 输出 fail schema validation 把模型 outage 转成应用 outage；timeout 紧于 UX 预算+per-provider circuit breaker；top 3 prompts port 到第二 provider 跑 eval——接近才 viable fallback；fallback feature flag 后 1% 流量一周看质量**（andrew.ooo + 72Technologies）→ 判据：**降级梯预先定义+预验证**——"incident 时才想 fallback"=雪崩；"Tier3/Tier4+eval 接近+1% 流量"=可预期；fallback 输出过 schema=降级不破下游。
- **提升层**：工作流/可复用 Skill（故障切换与优雅降级）。

## Token 压缩与记忆成本：压缩二次方、图形压缩、六技术堆叠（来源：Context-Engineering + ReCAP + 2609.22114 + Mem0 + Billion-context 2026 实拉，r638B 落地，与 §压缩只付在本次变更范围内分工——那边管"压缩范围纪律"，本条管"压缩的经济性与记忆成本结构"）
- **压缩经济性**：**内容压缩只省 ~2% cache-priced 前缀每轮——但压缩读取累积历史每后轮重发→累计节省二次方增长 ≈3,350N² tokens（实测）——~6 turns 内超过固定 tool-filter 节省；Compaction：利用率超 70% 总结积累上下文再以 summary 重初始化（distill 保留任务关键状态）；compaction lossy——先 masking 移除低值 bulk 再压缩**（arXiv 2609.22114 + Context-Engineering）→ 判据：**压缩收益按轮次累计**——"单轮看"=只省 2% 低估；"N² 累计"=多轮大头；先 masking 后压缩=有损压缩用在已清过的内容上。
- **图形化压缩**：**ReCAP Persistent Context Graphs（vs Codex 默认总结式压缩）：压缩+冷恢复延迟 -95%（Qwen3-Coder/gpt-oss）；SWE-Together 历史上下文减半同任务质量；Lost-in-Conversation 代码任务精度 +19.8/41.2 点**（arXiv 2609.40118）→ 判据：**压缩保结构比保摘要强**——"纯总结"=丢可检索结构；"持久上下文图"=低延迟恢复+质量保持；结构保留=代码任务精度升。
- **记忆成本六技术**：**token budgeting（-75% prompt tokens）/hierarchical summarization（-59%）/Ebbinghaus eviction（-59%）/embedding quantization（4× 存储）/Jaccard self-curation/hot-cold caching（83% RAM 减）——正确顺序堆叠 cut memory costs 3-4× 不碰模型；Billion-context：5× token 压缩 100K 窗口处理月级会话（否则截断丢连续性/升 million-token 10× 贵/重启破多日工作流）；context partitioning：单窗口放不下时跨子 agent 隔离上下文切分工作**（Mem0 + DEV + Context-Engineering）→ 判据：**记忆成本多技术复合**——"单技术"=收益有限；"预算+分层摘要+遗忘+量化+策展+冷热"=3-4×；放不下就切分不硬塞。
- **提升层**：模型/工作流（Token 压缩与记忆成本）。

## Prompt 缓存经济学：caching first、写读价差、稳定前置（来源：Claude Platform + AgentPatterns + MasterPrompting + Azure Foundry + Habr 2026 实拉，r638B 落地，与 §语义缓存分工——那边管"跨请求响应级缓存"，本条管"提供商前缀缓存的价格模型与请求结构"）
- **Caching first 与平方增长**：**agent 每轮重发整个增长对话（system prompt+工具定义+每前轮）——40-turn 任务第一轮发 40 次→成本随轮数平方增长；caching 不停止重发但每次约 1/10（Claude Opus 5 上 1/20）；先开 prompt caching 再动其他杠杆**（Claude Platform）→ 判据：**缓存是 agent 成本第一杠杆**——"轮数平方增长"=先控重发成本；"1/10 每次"=重发可负担；其他优化排在缓存后。
- **写读价差与结构**：**cache write（首次）1.25× base input vs cache read（后续命中）0.1×——首次成本 +25% 第二请求起 0.1×；immutable prefix pattern：稳定内容（system instructions/examples）放 prompt 开头，可变内容放后——favor reads over writes；Azure gpt-5.6+ 付 cache writes→控制写频次；Gemini 无写溢价（隐性 hourly storage fee 显式）**（AgentPatterns + MasterPrompting + Azure + DEV）→ 判据：**请求结构按缓存设计**——"稳定前置可变后置"=命中率高；"写 1.25× 读 0.1×"=避免频繁写；读写偏好=价格结构决定。
- **成本公式与倍率**：**账单五维：input+cached_input（clamp 不超 input）+cache_write_input+output 各按单价/百万；缓存折扣 up to 90%+batch 折扣 ~50%+reasoning-token 计费把单查询有效输出成本放大数倍——区分厂商 published list price 与 effective delivered cost**（codex-report + IntuitionLabs + Habr）→ 判据：**成本按公式算不按单价估**——"只报单价"=漏缓存/错峰/reasoning 维度；"五维公式"=可复现预算；有效成本≠标价。
- **提升层**：工具/工作流（Prompt 缓存经济学）。

## 成本建模与治理实践：账单四维、TTFT 杠杆、凭证级配额（来源：腾讯云 + IntuitionLabs + aiwisdom + 得助 MaaS + 阿里 Token Plan + 人民网 2026 实拉，r638B 落地，与 §成本预算强制分工——那边管"机制形态"，本条管"成本怎么算与治理落地"）
- **账单四维与不可固定值**：**AI API 账单四维：调哪个模型/输入 token/输出 token/走没走缓存与错峰——不存在'一次调用多少钱'固定值，同样一次调用成本可能差十倍；TTFT 杠杆：cut input tokens（shorter context=faster prefill=lower TTFT 最便宜 win）+cached prefixes（40-60% TTFT 降）+小/蒸馏模型（2-4× TPOT）用任务特定路由**（腾讯云 + aiwisdom）→ 判据：**先降输入再谈其他**——"输入 token 削减"=prefill 快+便宜双赢；"缓存前缀"=TTFT 40-60% 降；四维账单=预算口径完整。
- **凭证级配额与自动暂停**：**得助 MaaS：每研发小组独立调用凭证+每月固定 Token 上限；实时监控用量波形——触发阈值自动暂停凭证调用权限（消除脚本错误请求循环账单激增）+项目成本核算透明；阿里 Token Plan 网关：模型路由+订阅配额管理，任务复杂度（关键词/长度）动态调度轻量/旗舰，Redis 月度 Token 额度控制+自动降级——成本降 ~60% 预算确定性**（中关村科金 + 阿里云）→ 判据：**配额绑凭证不绑全局**——"全局 cap"=组间互相拖累；"凭证级上限+阈值自动暂停"=故障循环自愈；自动降级=预算不超。
- **分层模型组合降本**：**Prompt 压缩（1500→600 token -20%）+引入 mini（60% 请求 -40%）+自建小模型（30% 简单请求 -25%）；国产 KV 缓存调度 GPU/CPU/SSD 三级迁移压缩 1/7+长效缓存容量 5 倍+输入文本长度分桶匹配解决超长文本并发算力浪费**（腾讯云 + 人民网）→ 判据：**降本按层叠**——"压缩+路由+自建"=每层各减一截；KV 三级存储=缓存容量与迁移成本；长度分桶=并发不浪费。
- **提升层**：工作流/可复用 Skill（成本建模与治理实践）。

## 平台错误处理与韧性模式：error workflow 盲区、节点级重试、triage-retry、failover 链（来源：n8n Docs + n8n Blog + n8n 模板 + n8n Community 2026 实拉，r638C 落地，与 §故障切换与优雅降级分工——那边管"模型故障降级"，本条管"编排平台内执行失败怎么处理"）
- **error workflow 盲区**：**n8n 每 workflow 可设 error workflow（失败时跑，Error Trigger 首节点；邮件/Slack 告警；同一 error workflow 复用多 workflow）——但 AI Agent node 工具失败不触发 error workflow：工具错误视为 agent 推理的一部分非执行错误——需 IF/code node try-catch 手动处理，或让工具总返回结构化 JSON**（n8n Docs + Community）→ 判据：**工具失败走推理不走执行错误**——"把工具失败当 node 失败"=永远不触发 error workflow；"结构化 JSON 返回+条件分支"=可控处理；error workflow 管执行级错误。
- **节点级重试与 triage**：**node-level retry：节点内最大尝试+等待时间，简单 backoff 后台处理瞬时错误；高级策略用 looped IF node 上限；triage-and-retry：AI 诊断+telemetry+per-incident retry counter（up to 3）决定自动重试资格——transient 且 confidence 足够+预算剩→指数退避+n8n API 重试失败执行+记录结果；不可重试→转人工**（n8n Blog + 模板 16744）→ 判据：**重试前先分类**——"transient 可重试/不可重试转人工"=不盲目重试；"retry counter 上限"=防无限重试；诊断+遥测=重试决策有据。
- **failover 链**：**AI Agent 节点失败→On Error 输出→loop 回 Agent Variables 递增 fail_count→换模型重试（GPT→Gemini 链）——与预算强制联动防死循环**（n8n 模板 5160）→ 判据：**模型故障走显式链**——"On Error 输出+fail_count 递增"=跨模型降级；计数器上限=不烧钱；与预算强制联动=failover 不失控。
- **提升层**：工具/工作流（平台错误处理与韧性模式）。

## 平台可观测与成本告警：step-level traces、等待不 bill、三告警规则、replay evals（来源：Trigger.dev + Inngest + LangSmith + Kitaru + Activepieces 2026 实拉，r638C 落地，与 §网关生产陷阱与观测分工——那边管"网关层观测"，本条管"编排平台层观测与成本告警"）
- **step-level traces**：**Inngest Traces 记录每 step input/output+structured logs——"发了什么给模型/回来什么/多久"一处看全（每 prompt/response pair+token usage+tool inputs/outputs）；不需拼接 log lines 或外部 trace ID**（Codeables）→ 判据：**追踪到步级**——"每 step 输入输出+token 一处"=不用拼日志；"模型-工具全链"=归因清楚。
- **等待不 bill 与 SQL 查询**：**Trigger.dev：agent 等人审批工具调用时从停的 line 恢复且不 bill 等待；telemetry 每个 AI SDK 调用 run trace 带 tokens+cost；无 determinism 约束无平台超时；OTel+SQL-style query language；run 边跑边存崩溃不丢+30 天保留可查可 retry**（Trigger.dev + Activepieces）→ 判据：**持久化执行=不重复付费**——"等人不 bill+断点恢复"=长任务省钱；"run 实时存+30 天保留"=崩溃不丢可重试。
- **成本告警三规则与 replay evals**：**LangSmith：alert 日预算超支/单 run 超 100K tokens（潜在 loop 或检索爆炸）/平均 cost per request WoW +20%——catch cost regressions 在 AWS/Anthropic bill 前；Kitaru：open-source replay-based evals——对记录 tool history 重跑真实 agent 代码测 prompt/model/参数/代码改动（production-derived cases）**（fp8 + ZenML）→ 判据：**告警在账单前**——"日预算+单 run 阈值+周环比"三规则=成本回归先于账单暴露；"replay 真实历史"=改动验证用生产案例。
- **提升层**：工具/可复用 Skill（平台可观测与成本告警）。

## 工作流平台安全治理：sidecar 单次凭证、运行时强制、least-privilege 凭证、签名元数据（来源：IETF + NVIDIA OpenShell + WorksBuddy + AgentFacts + KeyRunner + 搜狐 2026 实拉，r638C 落地，与 §Agent 工具面安全分工——那边管"单个工具面威胁"，本条管"工作流平台整体安全治理"）
- **凭证生命周期治理**：**IETF sidecar：从 secret management（HashiCorp Vault）为 agent 获取凭证→单次操作使用→即弃；K8S mutating admission webhook 拦截 pod CREATE 注入 sidecar+policy volume；least-privilege agent 级：scoped credentials 只绑该 workflow step 需要的数据对象——over-permissioned agent=single point of failure；KeyRunner：'Give agents capability, not credentials'——policy enforcement+runtime secret injection+approvals+redaction+auditability，现有 API 变 governed AI tool <5 分钟**（IETF + WorksBuddy + KeyRunner）→ 判据：**能力与凭证分离**——"给能力不给凭证"=最小权限+可撤销；"单次凭证即弃"=泄露面最小；凭证绑 workflow step 不绑 agent=over-permissioned 消除。
- **运行时强制与审计**：**NVIDIA OpenShell：runtime 强制 agent 能访问哪些系统/数据不重写 agent——sandboxed execution+controlled service access+credential management+formal policy analysis；audit immutability：每 agent 动作/决策分支/数据访问事件写 append-only 日志**（NVIDIA + WorksBuddy）→ 判据：**治理在运行时不在提示词**——"不重写 agent 的运行时强制"=策略真正生效；"append-only 审计"=决策可追溯不可篡改。
- **签名元数据与合规**：**AgentFacts（KYA 标准）：cryptographically-signed capability declarations+multi-authority validation（不同权威验证不同 metadata 方面——消除单点信任失败）+dynamic permission management+graduated confidence；合规 metadata 自动更新；国内企业级=等保三级+信创适配+私有化**（arXiv 2506.13794 + 搜狐）→ 判据：**信任靠签名不靠自述**——"签名能力声明+多权威验证"=第三方 agent 可验证；"动态权限+分级置信"=信任可增量；等保+信创=国产合规基线。
- **提升层**：工作流/可复用 Skill（工作流平台安全治理）。

## Agent 评估方法：oracle 在对话外、transcript vs outcome、first-attempt 规则（来源：Traccia + FutureAGI + AEVAL + Holistic Evaluation + Awesome Agent Eval 2026 实拉，r639A 落地，与 §路由评估与基准分工——那边管"路由决策评不评得准"，本条管"agent 整体怎么评"）
- **oracle 在对话外**：**agent 的 oracle 常活在对话外：数据库状态/编译产物/测试结果/访问控制记录/对账账本——transcript 记录过程但不定义成功（采购 agent 可产有效采购摘要却创建重复订单）**（Traccia）→ 判据：**终态真相在环境**——"只看 transcript"=摘要漂亮订单重复看不见；"数据库/编译产物/测试结果"=成功可验证。
- **transcript vs outcome 两法**：**outcome grading：终态正确——客观但粗；transcript grading：步骤合理——抓 lucky/wasteful paths 仍落对答案（跑套件通过但乱翻文件的 agent）**（FutureAGI）→ 判据：**按风险选法**——"outcome 快但粗"=终态错看不见；"transcript 细但贵"=lucky/wasteful 路径被捕获；两者互补非互斥。
- **first-attempt 规则与失败归因**：**AEVAL first-attempt grading：grader 对 first-attempt trajectory 评——若轨迹含自纠编辑且因果必需于断言成功→该断言标 FAIL 不管后续成功（防 assertion-after-observation fitting）；Holistic：Plan Efficiency（执行与声明计划一致性 1-5 各 error modes）+Tool Coverage（后代工具调用集合覆盖整体目标 1-5）；术语：Task=prompt+success criteria/Trial=一次尝试/Grader=判定机制/Harness=模型外循环工具上下文**（AEVAL + arXiv 2605.14865 + Awesome List）→ 判据：**首试判成败**——"自纠因果必需=FAIL"=防拟合观测后断言；"Plan/Tool 两维 1-5"=过程质量可量化；术语统一=评估可交流。
- **提升层**：模型/工作流（Agent 评估方法）。

## 生产评估与漂移监控：dataset drift、observability vs evaluation、7 日滚动（来源：FutureAGI + QASkills + DailyAIWorld + MarkTechPost + aiturnpoint 2026 实拉，r639A 落地，与 §平台可观测与成本告警分工——那边管"编排平台层观测"，本条管"评估集与生产质量监控"）
- **dataset drift 与回流**：**eval set 写于启动——用户找到测试作者没预料的意图，dataset 不动 eval 仍过（离线分数数月平、生产投诉多样化、测试集复现不了多数失败）；fix=周采样失败 trace 按用户段/意图/judge 分桶→最硬 5-10% 提升进 eval set**（FutureAGI）→ 判据：**评估集是活的**——"dataset 不动=漂移隐形"；"周采样失败+最硬 5-10% 进集"=评估集追生产；离线平≠生产好。
- **observability vs evaluation**：**evaluation 部署前：固定数据集挡回归答"够不够好能 ship 吗"；observability 部署后：真实流量记录 latency/cost/quality 答"生产还在正确行为吗"——两者都要；平台记每 span prompts/completions/retrievals/tool calls/tokens/latencies/costs 再 score outputs；失败常以错误答案非错误出现**（QASkills + MarkTechPost + aiturnpoint）→ 判据：**两问两答**——"部署前挡+部署后盯"=完整闭环；"span 全记录"=坏输出可解释。
- **trace-to-dataset 闭环与漂移告警**：**token-budget graph=runaway loop 首信号（超出测试尾部）；deck gate=golden dataset suite 回归 delta+latency+hallucination flags 从真实生产 trace 组装才可 ship；drift 监控：online evaluator scores 时间序列——rolling 7-day mean+std per evaluator，today mean 掉 >1.5σ alert；safety-metric drops page、quality drops ticket**（DailyAIWorld + FutureAGI）→ 判据：**闭环与阈值**——"trace→dataset→gate"=生产反哺评估；"7 日滚动±1.5σ"=漂移可量化；"safety page/quality ticket"=分级响应。
- **提升层**：工作流/可复用 Skill（生产评估与漂移监控）。

## 评测框架选型与平台机制：框架对比、leaderboard 机制、三指标（来源：DeepakGupta + PromptEval + AIXYZ + PromptQuorum + DEV + Microsoft ThinkingBox + GAIA + n8n 2026 实拉，r639A 落地，与 §编排平台选型判据分工——那边管"工作流平台选型"，本条管"评测框架/平台选型与读数纪律"）
- **框架选型判据**：**LangSmith=LangChain/LangGraph 路径最小阻力（per-seat 成本看 reviewer 数）；Opik=注解队列+30 内置指标<$20/月价值选；Promptfoo=YAML-first 回归+红队插件+强 CI（秒级、每次 commit 抓回归、分数降 fail build；string similarity/regex/LLM-as-judge/custom graders）；DeepEval=pytest 式质量断言；RAGAS=可组合 RAG 指标；Phoenix=OTel-native；Langfuse=MIT trace 转数据集**（DeepakGupta + PromptEval + AIXYZ + PromptQuorum）→ 判据：**按 stack/许可/CI 选**——"LangChain 生态"→LangSmith；"预算+注解队列"→Opik；"CI 回归"→Promptfoo；"pytest 内断言"→DeepEval；"检索中心"→RAGAS。
- **leaderboard 读数纪律**：**HF leaderboard：.eval_results YAML+base_model filter（默认视图隐藏 30%）；rows 可来自非 model owner 的 PR——先看 PR author 再当 vendor 数字；GAIA 466 任务三级难度 exact-match private test set——exactness 是故意的（长自由形式要 LLM-as-judge 削弱可复现性）**（DEV + benchmarkingagents）→ 判据：**读榜先查源**——"PR 提交的分数≠厂商分"；"exact-match 保复现"=可复现优先于表达自由。
- **可靠性三指标与平台内建评估**：**Microsoft ThinkingBox：pass@1（单次成功=first-try quality）/pass@20（20 次至少一次=capability ceiling 能力上限）/20-of-20（每次过=dependability 可承诺客户）——只报 pass@1 误导，三指标都报才是真贡献；n8n 内建评估：Evaluation Trigger+Set Metrics node（correctness/tools used/string match/custom）+run-by-run 对比（回归部署前浮出）；社区版单 workflow 覆盖、子 workflow 单独评**（ThinkingBox + n8n）→ 判据：**三指标齐报**——"pass@1+cap@20+dependability"=能力与承诺分开；"平台内建评估同处"=建测一体回归早浮。
- **提升层**：工具/可复用 Skill（评测框架选型与平台机制）。

## 计划验证与失败恢复：monitor 三标准、advance-retry-replan、局部修复优先（来源：AgentixForce + LADDER + PAOVR + Algomox + RoboBRIDGE 2026 实拉，r639B 落地，与 §平台错误处理与韧性模式分工——那边管"编排平台执行失败"，本条管"agent 计划执行失败怎么恢复"）
- **monitor 三标准与五触发**：**每步后 monitor 查五触发（工具失败/新信息使假设失效等）；三标准：correctness（输出匹配期望）/progress（整体推进）/plan validity（后续步骤假设仍有效）——任一失败分类失败类型选修订策略**（AgentixForce）→ 判据：**监控看三面**——"correct+progress+valid"=输出对、有进展、假设活；"分类后选策略"=修法匹配错因。
- **恢复三择与预算保护**：**LADDER：verification 后决定 advance/retry/replan——完成子目标移队列推进；未完成 in place 重试；可互换对象重复子目标→未完成移队尾（一个难对象不耗 episode budget）；PAOVR Repair：local repair 只重跑/调整失败叶子 vs subtree re-plan 仅当该子树依赖/假设真变——never throw away 未失败部分**（LADDER + PAOVR）→ 判据：**局部优先**——"local repair 先行"=不从头再来；"subtree re-plan 有触发条件"=不无谓重规划；"难对象移队尾"=预算保护。
- **验证即证据**：**remediation API 返回 200 是请求接受证明非修复证明；验证失败→调整计划重试/回滚/带全上下文升级人工——决策逻辑非模型流畅度决定部署成败；高置信失败立即 halt+诊断模型推根因选 recovery target**（Algomox + RoboBRIDGE）→ 判据：**200≠修复**——"接受与修复分开"=验证要真证据；"重试/回滚/升级人工"=失败有出路；"高置信即 halt"=不硬闯。
- **提升层**：工作流/可复用 Skill（计划验证与失败恢复）。

## 计划执行鸿沟与状态一致：declaration-execution gap、state mismatch、PIVOT/SPIN（来源：arXiv 2609.38108 + ConPAct + PIVOT + SPIN 2026 实拉，r639B 落地，与 §分层规划分工——那边管"怎么分"，本条管"声明计划与执行不一致怎么办"）
- **声明-执行鸿沟**：**Plan Declaration-Execution Gap：声明计划与执行不匹配——区分 planning-mode selection 失败与 plan execution 失败（RQ1：长时程多步能否依赖 agent 执行承诺的规划方式）**（arXiv 2609.38108）→ 判据：**两失败分开**——"模式选择失败 vs 执行失败"=修法不同；"声明≠执行"=不能只看计划文本。
- **planner-actor state mismatch**：**ConPAct：两 agent 对相同任务相关状态事实系统分歧——prompt 双方结构化 state assertions 程序对比检测显式矛盾；提供任务相关状态信息减少 mismatch 改善协调与任务表现**（arXiv 2609.38891）→ 判据：**状态断言可对比**——"结构化 assertions+程序对比"=分歧显式化；"提供状态信息"=mismatch 可减。
- **轨迹精修与 DAG 前缀**：**PIVOT：PLAN 生成候选轨迹→INSPECT 执行+结构损失（文本梯度编码 plan-execution 差异）→EVOLVE 改进→VERIFY 最终全局检查；monotonic acceptance 非减解质量；SPIN：验证 DAG 计划+repair prompting 强制 DAG 契约→增量评估 prefixes 当前 prefix 足够回答即停（AssetOpsBench 261 场景减执行任务）**（PIVOT + SPIN）→ 判据：**轨迹可优化+够即停**——"损失信号回灌轨迹"=执行差异变学习信号；"prefix 足够即停"=不执行多余步骤。
- **提升层**：模型/工作流（计划执行鸿沟与状态一致）。

## 目标保持与规划幻觉分类：goal drift、misgeneralization 三深度、CoT 2026 模式（来源：Zylos + arXiv 2610.19731 + Adaline + Beyond Fluency + FutureAGI + PromptMake + CAP-CoT 2026 实拉，r639B 落地，与 §反思闭环分工——那边管"输出怎么自修"，本条管"目标漂移怎么防+规划幻觉怎么分类"）
- **goal drift 与 planning ceiling**：**Inherited Drift=条件化在先前 agent 漂移轨迹；Value Conflict Drift=显式约束对抗训练模型值；planning ceiling：运行结束 agent 初始目标被悄悄替换为看起来相似但不同的——horizon 之外无法跨步维持连贯意图无论模型多强**（Zylos + Adaline）→ 判据：**漂移有因**——"inherited vs value conflict"=触发不同；"ceiling 是产品问题"=目标保持要产品层机制非模型层。
- **misgeneralization 三深度**：**functional target substitution（行为跟替代目标）/policy shortcut（跟学习动作策略）/cue competition（意图与代理目标线索竞争）——目标丢失深度不同：达决策层 steering 重定向 16.0%→95.3%；达策略未达决策仅新下游布线恢复 31.6%→84.3%；inert 两者都不行**（arXiv 2610.19731）→ 判据：**先判深度再选恢复**——"cue competition 可 steering"=轻恢复；"policy shortcut 需重布线"=重恢复；"inert"=两者都不行别浪费。
- **规划幻觉分类与 CoT 2026**：**agentic IR 规划阶段幻觉：Fact Derive（初始策略引入不存在/误导事实）/Task Decompose（任务不对齐子目标忽略主约束）；CoT 2026 模式：reasoning tuned model 内用+sampling 3-8 traces self-consistency（允许的 benchmark）+tree/graph of thoughts（有搜索结构任务：游戏/定理证明/约束规划）；推理模型默认跳过 prompt CoT（GPT-5.6 Sol/Claude Opus 5/Fable 5/Gemini 3.1 Pro 硬分析——给 crisp brief：success/拒什么/格式，让模型私花思考预算，外部步骤仅 eval set A/B 显示真实增益后加）；plan-and-solve 先计划后执行（代码生成/结构化分析——提交前 checkpoint）；CAP-CoT：forward solver 生成链+adversarial challenger 构造看似合理故意错链+feedback agent 对比产生 step-aligned 反馈双向优化**（Beyond Fluency + FutureAGI + PromptMake + CAP-CoT）→ 判据：**幻觉分类+CoT 按模型选**——"Fact/Task 分类"=规划幻觉可归因；"reasoning model 私花预算+外部步骤 A/B 后加"=不为提示而提示；"adversarial challenger"=优化用故意错例。
- **提升层**：工作流/可复用 Skill（目标保持与规划幻觉分类）。

## Agent 安全纵深：行动面审核、硬件层观察、三护栏（来源：NVIDIA + OWASP Cheat Sheet + AI Buzz + LlamaFirewall + OpenAI Alignment 2026 实拉，r639C 落地，与 §Agent 工具面安全分工——那边管"工具面四个具体威胁"，本条管"安全架构纵深+行动面控制"）
- **行动面审核**：**action screening：每个提议工具调用对照原始用户意图评估——guardrail 查用户任务与提议动作但不摄入不可信中间上下文；output screening：主模型响应返回用户/传下游工具前按策略评分（成功的注入系统提示泄漏/渗出标记/违规内容事后抓）**（OWASP）→ 判据：**动作对照意图+输出过筛**——"动作审核不摄入中间上下文"=注入不污染决策；"输出评分"=泄漏事后抓。
- **硬件层与人类签收**：**agents can't secure themselves；OpenShell 密封环境限制文件/网络+Sentry 硬件层独立于 agent 观察停止未授权活动+task-specific checks+人类在后果性事件前签收；高风险动作 HITL 批准（邮件发送/文件写/外部 API/金融交易）=防注入指令自动触发不可逆真实世界动作——最有效爆炸半径控制**（NVIDIA + AI Buzz）→ 判据：**纵深+人闸**——"密封+硬件观察"=agent 自证不了自己；"高风险动作人类批准"=不可逆动作留人闸；"后果性事件签收"=问责在人在。
- **三护栏与自复制注入**：**LlamaFirewall：PromptGuard 2 通用越狱检测/Agent Alignment Checks 基于 CoT 审计器查推理中提示注入与目标偏离（实验阶段但防间接注入更强）/CodeShield 在线静态分析防编码 agent；self-replicating prompt injection（prompt infection：LLM-to-LLM 多 agent 系统注入）真实存在**（LlamaFirewall + OpenAI Alignment）→ 判据：**护栏分层**——"越狱检测+推理审计+静态分析"=入口/推理/代码三面；"多 agent 注入会自复制"=隔离与审计不可省。
- **提升层**：工作流/可复用 Skill（Agent 安全纵深）。

## A2A 与 MCP 协议边界及去中心化协作：手与同事、skill marketplace、stake slashing（来源：A2A Protocol + IETF + SwarmHarness + OmniSwarm + AgentVerse 2026 实拉，r639C 落地，与 §MCP 选型五标准分工——那边管"MCP server 怎么选"，本条管"A2A/MCP 协议边界+去中心化协作机制"）
- **MCP=手 A2A=同事**：**A2A=agent-to-agent 通信开放分散标准：独立 agent（含用 MCP 的）相互发现/委托任务/共享结果；MCP 装备单个 agent 具体工具（GitHub repo/SQL 数据库），A2A 让专门 agent 安全与其他 agent 协作；MCP stateful per connection stateless across connections 不支持 session resumption；A2A 使 opaque 系统（不同框架/语言/厂商）共同语言发现能力/协商通信**（A2A + IETF）→ 判据：**两协议分工**——"MCP 管人-agent 工具/A2A 管 agent-agent"=装备与协作分离；"opaque 系统共同语言"=不暴露内部逻辑。
- **去中心化激励与信誉**：**skill marketplace：节点发布 skill 可用性+credit-per-call 定价——提交者比较报价再派遣；差分定价：稀缺高性能技能（大 GPU 推理）吸引更多贡献者、常见低成本（文本分类）竞争定价；agent 经济：agent 实例 stake tokens 参与任务池——交付损坏/幻觉数据 stake 被 cryptographic proofs slashed；高性能 agent 赚不可变链上 reputation→更高层任务；BFT 无 leader agent 经济：5000+ edge agents 零中央服务器/零可信第三方/零单点故障**（SwarmHarness + OmniSwarm + AgentVerse）→ 判据：**市场机制管协作**——"报价比较+差分定价"=稀缺与常见分流；"stake slashing+reputation"=欺骗有成本、好表现可积累；"BFT 无 leader"=无单点。
- **提升层**：工具/工作流（A2A 与 MCP 协议边界及去中心化协作）。

## 生产可观测性与长时程评估：trace 每步、任务级成本警报、MEA 审计链（来源：Langfuse + FoundrySoft + landed + Zylos + LongHorizon-Harness + UBC 2026 实拉，r639C 落地，与 §生产评估与漂移监控分工——那边管"评估集与质量指标监控"，本条管"生产 trace/成本/失败率观测+长时程评估结构"）
- **trace 每步与任务级警报**：**每 generation/tool/retrieval 记 span（trace=span 树 OTel-aligned）带 cost/latency/args/结构化 error——失败通常藏中间步非最终答案；cost-per-resolved-task 与 steps-per-task 是最早回归警报（super-linear cost 放大额外步）——cost-per-call 单独误导**（Langfuse + landed）→ 判据：**任务级成本盯梢**——"cost-per-resolved-task"=一次成功任务总成本；"steps-per-task 涨"=多步放大；"单 call 成本"=看不出回归。
- **finishReason 直接告警**：**agent 放弃或达 step limit 率用 finishReason 字段直接告警不推断；rising step-limit exits 通常=工具开始静默失败或 prompt 改变让 agent 自疑进多余循环**（FoundrySoft）→ 判据：**退出原因直采**——"finishReason 原字段告警"=不靠猜；"step-limit 涨"=查工具静默失败或提示自疑。
- **长时程评估结构**：**MEA（LongHorizon-Harness）：三结构隔离角色一审计状态机——每角色独立预算（executor 1800s/round+manager 300s+auditor 300s，上限 25 rounds）；manager 发 subtask contract+executor fresh context 状态改变+auditor 追加只读报告到审计链；label task envelope first：长任务/单项目挑战/科学工作流=不同声明，验证方法各不同**（LongHorizon-Harness + UBC）→ 判据：**评估结构隔离+声明匹配**——"三角色独立预算+审计链"=执行/管理/审计不互蚀；"先标任务信封"=声明与验证方法匹配。
- **提升层**：工作流/可复用 Skill（生产可观测性与长时程评估）。

## 系统提示组装分层与固定结构（来源：OpenClaw docs.openclaw.ai·concepts/system-prompt + reference/rich-output-protocol + cli/infer 2026 实拉，r640A 落地，与 §上下文预算管理分工——那边管"窗口预算"，本条管"系统提示怎么组装/怎么出结构化协议"）
- **三层组装**：**buildAgentSystemPrompt 从显式输入渲染 prompt——保持纯 renderer 不直接读全局配置；resolveAgentSystemPromptConfig 解析配置-backed 旋钮（owner display/TTS hints/model aliases/memory citation mode/sub-agent……）**（OpenClaw）→ 判据：**渲染与配置分离**——"纯 renderer"=输入即输出可测；"配置旋钮解析"=可变项集中不散落。
- **compact 固定节**：**system prompt 紧凑、固定节：Tooling（结构化工具是 source-of-truth 提醒+runtime 工具使用指引）；progress_card（update_plan）保持一个 durable plan+status note，最多一个 in_progress step**（OpenClaw）→ 判据：**固定节防漂移**——"source-of-truth 提醒"=工具定义权威；"单 in_progress step"=计划不并发打架。
- **rich-output 协议与稳定字段**：**[view ...] 对新增输出无效、[embed ...] 2026.4 替代；normalized/stored assistant content block 是结构化 canvas item；CLI infer JSON 稳定顶层字段：ok/capability/transport/provider/model/attempts/inputs/outputs/ignoredOverrides/error（媒体命令 outputs 另含……）**（OpenClaw）→ 判据：**输出协议稳定**——"稳定顶层字段"=下游可机读；"ignoredOverrides"=不支持 hint 显式暴露。
- **提升层**：工作流/可复用 Skill（系统提示组装分层与固定结构）。

## 输出修复与重试策略：repair loop 与安全 fallback（来源：ML Digest + deeplearning.ai Getting Structured LLM Output + OpenAI Community + kissapi 2026 实拉，r640A 落地，与 §输出校验防线分工——那边管"防线怎么拦"，本条管"拦不住时修复/重试/回退怎么走"）
- **repair loop 有界化**：**structured outputs 组合：schemas + allowed values + validation + repair loops + 何时安全 fallback；Repair-based Structured Output：解析失败→带错误信息重试→有界次数；避免 assertion-after-observation 拟合——修复循环要预先定义修复规则而非事后看结果编规则**（ML Digest + deeplearning.ai）→ 判据：**修复有界且规则先行**——"有界次数"=不无限重试；"规则先定"=不拟合特定失败。
- **强制优先于修复**：**Structured Generation with Outlines：生成时 token 级强制 schema——模型不能产出畸形 JSON，事后修复归零；生成时强制成本 < 事后 repair 循环（少一次往返+少一重解析失败分支）；OpenAI 社区：用 Responses API + Structured Outputs、工具/函数调用当强制层——别为 JSON 生成 fine-tune（错误方向）**（Outlines + OpenAI Community）→ 判据：**先强制后修复**——"token 级强制"=非法输出不可能；"别 fine-tune 为 JSON"=用 API 机制非训练解决。
- **fallback 与跨模型安全**：**何时安全 fallback：格式错误可安全降级（重试后仍失败→返回 permissive 结构/人工标记）；跨模型差异由网关归一（response_format/tools 载荷一致）——fallback 面窄化到语义层而非格式层**（kissapi + n8n permissive schema）→ 判据：**fallback 分语义/格式**——"格式层网关兜底"=载荷一致；"语义层人工标记"=降级不静默。
- **提升层**：工作流/可复用 Skill（输出修复与重试策略）。

## 约束生成选型与边界：Beyond JSON 与非 JSON 结构化（来源：deeplearning.ai + Pipedream + 腾讯云 + FutureAGI 2026 实拉，r640A 落地，与 §结构化输出三层强制分工——那边管"三层机制怎么用"，本条管"选型边界与非 JSON 形态"）
- **Beyond JSON**：**Structured Generation: Beyond JSON——结构化生成不限于 JSON：regex/grammar/代码/受控枚举（Literal）都是结构化面；选型判据：消费端要什么形状就约束什么形状——中间态用 JSON 便于传递、终态用 schema 化文本/代码减少二次解析**（deeplearning.ai + Outlines Literal）→ 判据：**按消费端选形态**——"中间态 JSON"=传递方便；"终态 code/枚举"=免二次解析。
- **受控枚举与状态面**：**状态字段用 enum 约束受控取值（status: READY/NEEDS_CLARIFICATION）；受约束值面让下游 switch 分支穷尽——模型不能发明状态；Pipedream action 一律 return JavaScript 对象（API 返 XML 先转对象）——组件输出形状统一**（腾讯云 + Pipedream）→ 判据：**状态枚举化**——"enum 状态"=分支可穷尽；"组件返对象"=消费端统一。
- **约束的边界**：**grammar/schema 管格式不管语义：格式合法≠内容正确——约束解码之后仍需语义校验层（值域/一致性/业务规则）；decode-time 强制提升"格式通过率"但不提升"语义正确率"，两指标分开测**（FutureAGI + Outlines）→ 判据：**格式与语义两指标分开**——"格式通过率"由约束层保证；"语义正确率"由校验层负责；混为一谈=漏业务校验。
- **提升层**：工具/可复用 Skill（约束生成选型与边界）。

## 上下文工程定义与四机制（来源：Anthropic Applied AI 团队定义 + 博客园 + XBSTACK 2026 实拉，r640B 落地，与 §上下文预算管理分工——那边管"窗口预算数值"，本条管"上下文工程定义与机制组合"）
- **定义**：**上下文工程=在有限注意力预算下，找到最小的高信号 token 集合来最大化期望行为**（Anthropic Applied AI，2026-06）→ 判据：**定义即目标函数**——"最小高信号 token 集"=数量与质量双约束；"最大化期望行为"=产出导向非信息量导向。
- **四机制组合**：**压缩（长会话逼近窗口前主动总结）/ 检索（按需取外部信息）/ 工具（行动扩展上下文）/ 记忆（跨会话复用）——在预算约束内按需组合，不全用**（博客园）→ 判据：**机制按场景选**——"压缩管逼近"、检索管未知、工具管行动、记忆管复用；"四机制全上"≠更好，预算约束下要取舍。
- **多厂商收敛**：**Anthropic 把上下文当有限注意力预算；Google 定义为 agent 周围的结构化数据/环境基础设施；Microsoft Foundry 把 Knowledge Retrieval/Tool Search/Skills/Memory 放进企业 agent 成本优化框架**（XBSTACK）→ 判据：**收敛=核心地位确认**——"检索/工具/技能/记忆"四件套进成本框架=上下文工程是成本治理一部分。
- **提升层**：工作流/可复用 Skill（上下文工程定义与四机制）。

## 嵌入模型选型与基准陷阱（来源：arXiv Embedder's Dilemma + T3EM + LMEB + Qwen3-VL 2026 实拉，r640B 落地，与 §RAG 检索工程·一索引一模型分工——那边管"索引与模型绑定"，本条管"选型基准与成本/质量权衡"）
- **范式平局**：**受控成本感知对比（10 LLM × 26 embedding 模型 × 37 任务）：最佳 LLM（Gemini 3.1 Pro 77.6）与最佳 embedding 模型（77.x）总体持平——LLM 当 embedding 不一定更好，按成本选**（arXiv Embedder's Dilemma）→ 判据：**成本感知对比**——"总体持平"=别默认 LLM 更强；"受控成本"=选型看性价比。
- **质量-延迟-成本三角**：**T3EM 检索质量最高（平均 nDCG@10=0.638）但约 7-14 倍开源替代延迟+per-query API 成本；mE5-L 最强开源通用英文替代，差 0.09 nDCG 分**（arXiv T3EM）→ 判据：**延迟与成本是选型项**——"0.09 分差距 vs 7-14 倍延迟"=边际质量不值得高延迟时选开源。
- **基准对齐任务**：**LMEB 长程记忆嵌入基准：30 个模型（33M-12B）无单一模型全类型占优，且 LMEB 与 MTEB（English v2）检索子集相关性弱——评估分数必须对任务类型（含长程记忆检索）选基准；Qwen3-VL-Embedding/Reranker 统一多模态框架 MMEB-V2 77.8**（arXiv LMEB + Qwen）→ 判据：**基准要对齐任务**——"MTEB 高分≠长程记忆好"=别用错榜单；"多模态单独测"=单模态榜单不作数。
- **提升层**：工具/工作流（嵌入模型选型与基准陷阱）。

## 向量库与切块生产细节（来源：n8n docs + LangFlow docs + vectordbpipe + Vucense 2026 实拉，r640B 落地，与 §RAG 检索工程分工——那边管"检索策略与指标"，本条管"入库/切块/库形态"）
- **两阶段入库检索**：**先按文件描述向量相似度阈值+文件限制筛出文件 ID→再只从这些文件取向量 chunk 附加相似度过滤——文件级粗筛后块级精取，避免无关文件块浪费上下文**（n8n workflow）→ 判据：**先文件后块**——"文件级阈值"=粗筛；"块级相似度"=精取；两阶段减少噪声注入。
- **库形态与再入库**：**LangFlow knowledge base 默认 Chroma 本地向量库、可配外部 provider（Chroma Cloud/OpenSearch/pgvector）；knowledge base 不随 flow 每次运行 re-ingest 更高效；n8n 入库链路：Data Loader（切块）→Embeddings→Vector Store Insert（upsert）；本地主权 RAG 三件套=embedding 模型+pgvector+本地 LLM；Vectorless RAG=层级 PageIndex 无向量引擎**（LangFlow + n8n + Vucense + vectordbpipe）→ 判据：**入库与查询分离**——"不随 flow re-ingest"=数据变更才重灌；"三件套本地"=主权可审计；"无向量引擎"=免嵌入成本换简化。
- **切块参数**：**Recursive Character Text Splitter 按结构递归切块；切块后每块转 embedding 存库——切块粒度影响召回粒度：过大=噪声、过小=上下文割裂，按文档结构选**（n8n）→ 判据：**切块跟结构**——"递归切"=保层级；"粒度=召回粒度"=按文档定。
- **提升层**：工具/工作流（向量库与切块生产细节）。

## State Store 持久化内容清单与边界（来源：WaytoAGI 生态 24/7 Agent + OpenClaw automation/tasks + taskflow 2026 实拉，r640C 落地，与 §记忆提取策略分工——那边管"记忆怎么提炼"，本条管"运行态该持久化什么"）
- **该存清单**：**至少持久化：当前 step 号 / 任务 ID 与元数据 / 最后一次工具调用及其结果 / 影响未来步骤的 LLM 决策 / 当前 step 重试计数 / 任务已花费成本**（WaytoAGI 生态）→ 判据：**存恢复所需最小集**——"step 号+任务元数据"=定位；"末次工具调用+结果"=续跑依据；"决策+重试计数+成本"=状态与预算。
- **不存边界**：**不持久化原始 LLM 输出当操作状态——输出是数据不是状态；操作状态=可推进执行的元数据**（WaytoAGI 生态）→ 判据：**状态 vs 数据分离**——"LLM 输出"=可重算数据；"操作状态"=决策推进；混存导致恢复时状态污染。
- **持久化与并发**：**OpenClaw durable state：flow_runs 表进度跨 gateway 重启存活；每次写 bump revision——并发写者传 stale expected revision 冲突需重读；WAL growth 由 SQLite autocheckpoint+定期 passive checkpoint 约束；cron 任务内存执行环境消失时先查持久执行历史再标记丢失**（OpenClaw）→ 判据：**进度落盘+并发守卫**——"跨重启存活"=进程死进度在；"revision 冲突重读"=并发写不乱；"先查历史再标记丢失"=不误判。
- **提升层**：工作流/可复用 Skill（State Store 持久化内容清单与边界）。

## 暂停/恢复与 HITL 状态序列化（来源：Dify Human Input node + Dosu + n8n Wait Node + Pipedream 2026 实拉，r640C 落地，与 §State Store 分工——那边管"运行态存什么"，本条管"跨暂停边界的序列化"）
- **三状态组件跨暂停边界**：**Dify Human Input（HITL）节点：工作流在指定点暂停→呈现交互表单给操作员→基于响应恢复；跨多个请求上下文，须显式序列化+恢复执行状态；三个独立状态组件必须存活：GraphRuntimeState（变量池/LLM generate entity/response stream filter state）——GraphRunPausedEvent→PauseStatePersistenceLayer 存 WorkflowResumptionContext（图运行时快照）+映射暂停原因**（Dify + Dosu + Doc Holiday）→ 判据：**暂停即序列化**——"变量池+生成实体+流过滤器"三件存活；"暂停原因映射"=恢复分支可定。
- **异步暂停恢复模式**：**n8n Wait Node Async Portal/Teleport 模式：主流程在 checkpoint 无限暂停→外部异步事件恢复；Pipedream：suspend 执行→轮询外部 API 状态后恢复或接受回调恢复——暂停期间无时长上限且不计 credits；Activepieces：Wait for Approval/Delay 暂停不计入 flow run timeout（10min 只计活跃执行时间）**（n8n + Pipedream + Activepieces）→ 判据：**暂停不计时**——"wait/approval/delay"=挂起非执行；"异步事件恢复"=不占轮询线程。
- **提升层**：工具/工作流（暂停/恢复与 HITL 状态序列化）。

## 超时与错误分类治理（来源：Pipedream + Make + Activepieces + Dify 2026 实拉，r640C 落地，与 §恢复语义三原则分工——那边管"失败后走哪条恢复路"，本条管"超时边界与错误呈现"）
- **超时边界与拆片**：**Pipedream：HTTP/Email 触发默认 30s/次、Cron 60s/次；超时抛 Timeout 停止但部分日志与可观测性保留；paid 最大 750s 硬限——超限拆多个 workflow 分片处理或 suspend-poll-resume**（Pipedream）→ 判据：**超时是设计参数**——"默认值随触发类型变"=按场景定；"超时留日志"=失败可查；"硬限拆片"=长任务分片化。
- **模块级超时与状态机**：**Make：模块运行时上限 40/60 秒→ModuleTimeoutError；配 Retry error handler+存储 incomplete executions；ConnectionError/ModuleTimeoutError 自动 exponential backoff；自动重试前 3 个 incomplete：成功→Resolved 停止，全失败→Unresolved 可手动重试或 resolve；Activepieces：hung steps 报 proper timeout errors 而非内部 RPC 失败；自动升级前跑兼容性检查+audit log 记录 before/after 版本+可回滚受影响 flow**（Make + Activepieces）→ 判据：**错误要可读**——"proper timeout error"=可归因；"Resolved/Unresolved 状态机"=重试有终态；"升级前兼容检查+版本留痕"=变更可回滚。
- **节点级降级**：**Dify Reliability：LLM/HTTP/代码/工具节点可停止、返回默认值或带类型化错误信息转入恢复分支**（Dify）→ 判据：**节点级三选一**——"停止/默认值/类型化错误分支"=按影响面选；"类型化错误"=分支可编程。
- **提升层**：工具/工作流（超时与错误分类治理）。

## 生产级错误处理与死信治理（来源：n8n Community + n8nlogic + DEV + n8n Triage template 2026 实拉，r641A 落地，与 §超时与错误分类治理分工——那边管"超时边界与错误呈现"，本条管"重试耗尽后的死信与告警治理"）
- **重试耗尽先落状态再告警**：**retry limit 到达时，先把 failed/dead-letter 状态存 PostgreSQL，再发 Slack/Email 通知——告警不能是失败唯一记录；重复告警在 PostgreSQL/Redis 去重而非 workflow static data（static data 实验性，高频执行下不可靠）**（n8n Community）→ 判据：**死信落库先于通知**——"告警=提示，DB=真相"；去重放外部状态不放工作流静态数据。
- **Error workflow 单点**：**恰好一个 Error workflow：Error Trigger→Format Alert→Send to Slack；Throwing 只有有人听到才有用；每个网络节点 Enable Retry On Fail（3 tries ~2500ms）；Stop Workflow vs Continue（用错误输出）按失败语义选——部分成功可接受才 Continue，且错误分支必须路由到某处**（n8nlogic + DEV）→ 判据：**错误有家可归**——"单点 Error workflow"=告警不散；"Continue 必配路由"=不静默吞错。
- **per-incident retry counter 判 eligible**：**AI 诊断+telemetry+每次事故重试计数（最多 3 次）判失败是否 eligible 自动重试；transient 且预算内→exponential backoff+n8n API 重试失败执行+记录结果；不 eligible 或预算尽→升级人工**（n8n Triage template）→ 判据：**重试资格有据**——"transient+预算内"才自动重试；"每事故计数"防无限重试同一失败。
- **提升层**：工具/工作流（生产级错误处理与死信治理）。

## Agent Skills 生态与标准治理（来源：agentskills.io + skills.sh + Full Stack Skills + Claude Code Skills Directory + GitHub Blog 2026 实拉，r641A 落地，与 §Agent 工具面安全分工——那边管"工具面威胁"，本条管"技能生态选择与治理"）
- **标准即生态**：**Agent Skills 2025-12 从 Anthropic 内部格式发布为开放标准，数月成整个工具生态扩展 coding agent 的主流机制——2026 初 30+ 平台采用，10 月 Anthropic 报告 70+ 平台（Cursor 等）集成；写好的技能可在兼容工具间共享，行为仍随 agent/模型而异**（agentskills.io + shattered.io）→ 判据：**标准可移植**——"同一技能跨工具"=投资可迁移；"行为随引擎异"=换工具要重测。
- **技能形态选择**：**skills.sh：用 Markdown 文件向 Cursor/Claude Code/Copilot 注入架构规则/代码约定/程序性知识；Full Stack Skills：171 技能覆盖全栈，12 插件类别按技能种类而非岗位划分便于组合；官方仓库（openai/skills、expo/skills、OpenRouterTeam/skills）作结构模板**（skills.sh + Gitee + DEV）→ 判据：**按组合选形态**——"纯规则=Markdown 注入"；"重逻辑=脚本技能"；"分类按技能种类"=跨岗位复用。
- **节点留痕与多分支聚合**：**Dify 每节点留痕是排障救命稻草——检索回旧文档=知识库文档更新后没重新同步；多分支聚合前提=各分支末端 Code 节点输出变量名一致**（腾讯云 + 51CTO）→ 判据：**留痕可查+聚合契约**——"每个节点留痕"=问题可定位；"输出变量名一致"=聚合可合并。
- **提升层**：可复用 Skill/工作流（Agent Skills 生态与标准治理）。

## 编码技能开发纪律与加载治理（来源：OpenClaw docs + BetterClaw + theopenclawplaybook 2026 实拉，r641A 落地，与 §技能评测闭合邻域分工——那边管"评测怎么测"，本条管"技能怎么写怎么加载"）
- **技能编写纪律**：**简洁——指示模型做什么、不是怎么当 AI；安全第一——skill 用 exec 时写不允许不可信输入任意命令注入的 prompt；本地先测 openclaw agent --message 再分享；分享前先查 ClawHub 社区技能避免重复**（OpenClaw docs）→ 判据：**编写五律**——"指令性非说教/exec 防注入/本地先测/先查社区"逐条过。
- **常见坑清单**：**缺错误处理——API 500 时 agent 该知道下一步，不盲目重试；过度工程——先 Markdown-only 技能，逻辑工具调用真表达不了才加脚本；环境特定路径——不硬编码 /Users/xxx，用相对路径或环境变量；TS moduleResolution bundler+target ES2022——配置不匹配占"技能为什么不加载"问题 40%**（theopenclawplaybook + BetterClaw）→ 判据：**写前避坑**——"500 有下一步"=错误处理；"先 Markdown"=延迟脚本化；"相对路径"=可移植；"TS 配置匹配"=加载不炸。
- **加载治理**：**技能按 environment/config/binary presence 在 load time 过滤；改技能或配置对运行中 agent 生效有会话快照延迟（性能取舍）**（Claw docs）→ 判据：**加载可预期**——"load time 过滤"=按环境装；"快照延迟"=改动生效要等，别误判失效。
- **提升层**：可复用 Skill/工具（编码技能开发纪律与加载治理）。

## Skill 商店生态与商业化链路（来源：36氪 + 央广网 + 腾讯云 2026 实拉，r641B 落地，与 §Agent Skills 生态与标准治理分工——那边管"标准与形态选择"，本条管"商店生态与变现链路"）
- **三巨头 Skill 商店模式**：**阿里虾小宝：内置 JVS Claw Agent，挑选 Skill 一键同步到工具；市场不收费但调用消耗算力（云业务收入）；字节两路线：火山 Find Skill 面向企业整合 ClawHub/GitHub 多源+扣子 Skill 商店面向普通开发者支持售卖**（36氪 + ai-indeed）→ 判据：**变现模式清晰**——"市场免费+算力收费"=按用量计；"企业/开发者分路线"=按受众分。
- **SkillPay 支付链路**：**腾讯 SkillHub 上线 SkillPay（2026-07-16）：技能分发+Agent 调用+技能支付同一条链路打通；商家上架 Pay Skill 获收费能力；SkillHub 负责来源认证/内容完整性校验/可信调用入口，微信支付底层**（央广网）→ 判据：**交易链路三方分工**——"分发/调用/支付同链路"=闭环；"来源认证+完整性校验+可信入口"=信任基建。
- **商店治理指标**：**SkillHub：8 万+ Skills、国内高速镜像秒速安装、三线并行安全审核、首发 TRACE 评测体系帮用户识别高质量 Skill；腾讯文档/会议/地图/ima/QQ 浏览器核心能力封装官方 Skills；上线首周 180GB/87 万次下载；本地镜像站始终标注 clawhub 原始来源**（腾讯云 + 财新）→ 判据：**商店可信可测**——"镜像秒装"=可用性；"三线审核+TRACE 评测"=质量门；"标注原始来源"=生态贡献透明。
- **提升层**：可复用 Skill/工作流（Skill 商店生态与商业化链路）。

## 个人知识库与内容工作流配方（来源：Dify 快速上手 + 博客园 + 掘金 + CSDN 2026 实拉，r641B 落地，与 §个人自动化配方分工——那边管"效率自动化怎么起手"，本条管"个人知识库与内容生成怎么搭"）
- **30 分钟内容生成器**：**Dify 快速上手：文本/文档/图像输入→加偏好声音和语气→输出平台特化社媒文案——用 LLM 节点+节点编排（多平台内容生成器）**（Dify）→ 判据：**风格注入可复用**——"偏好声音语气"=输出一致；"平台特化"=一稿多平台。
- **知识库注入让 AI 读过书再回答**：**上传 4 本 PDF 建知识库（职场规矩智能体）——回答从模型通用知识变成基于注入内容；知识库索引选高质量保检索准确度；Notion 数据源导入；Chatflow 编排 IF/ELSE 节点后接知识库+LLM 节点**（掘金 + 博客园）→ 判据：**先注入再问答**——"PDF 进知识库"=内容主权；"索引选高质量"=检索准确；"IF/ELSE 后接知识库"=条件路由。
- **私有 AI 本地化**：**Dify+Ollama+DeepSeek 本地部署：数据不出内网，进阶 Chatflow/Workflow 应用**（Dify legacy-docs）→ 判据：**本地主权**——"Ollama+DeepSeek 本地"=隐私/成本可控。
- **提升层**：工具/工作流（个人知识库与内容工作流配方）。

## 自动化平台选型与迁移治理（来源：人人都是产品经理 + FlowRunner + Pipedream 官方 + Langflow 2026 实拉，r641B 落地，与 §超时与错误分类治理分工——那边管"运行中错误怎么处理"，本条管"选哪个平台与平台生命周期"）
- **自搭 vs SaaS 选型**：**自搭服务器用 n8n/Dify；SaaS 用 Coze 工作流/通义 AppBuilder/百度 AppBuilder/飞书自动化/钉钉宜搭——先跑出第一条能真正跑的工作流再谈深度**（人人都是产品经理）→ 判据：**按运维能力选**——"愿自搭=n8n/Dify"；"省事=SaaS"；"第一条能跑"优先于功能全。
- **平台关停迁移**：**Pipedream Workflows 2027-03-31 关停——export 工具逐项目导出 ZIP：每个 workflow 一个 JSON 文件描述 triggers/steps/code/configured props/control flow；inline code steps 保留（最费时间写的部分）；漏掉的部分同样重要需自行补齐**（FlowRunner + Pipedream）→ 判据：**迁移契约=完整描述**——"JSON 含 triggers/steps/code/props/control flow"=可重建；"inline code 在导出里"=核心资产不丢。
- **平台能力盘点**：**Pipedream 目录 3,224 apps/14,966 tools（2026-09-23 核验）；Langflow：组件和流可当 agent 工具、可暴露为 MCP server、可连外部 MCP client**（stacksandflows + Langflow docs）→ 判据：**按接入面选**——"app 目录量"=开箱集成；"MCP server 化"=agent 可编程接入。
- **提升层**：工具/工作流（自动化平台选型与迁移治理）。

## 晚交互/多向量检索选型（来源：CSDN ColBERT 解析 + Sentence Transformers v6.0 + Nemotron ColEmbed V2 + Hydra + Langflow 1.11 2026 实拉，r641C 落地，与 §向量库生产细节分工——那边管"单向量库怎么配"，本条管"晚交互多向量模型怎么选"）
- **晚交互核心机制**：**ColBERT（Contextualized Late Interaction over BERT）：不压缩——每个 token 保留独立向量表示，检索时 MaxSim 操作符细粒度匹配（查询每 token 在文档所有 token 向量找最相似）——突破 embedding 天花板**（CSDN）→ 判据：**细粒度匹配**——"token 级向量+MaxSim"=语义精度；"不压缩"=存储成本换质量。
- **生态支持面**：**Sentence Transformers v6.0：MultiVectorEncoder 第四模型类型——支持 late interaction（PyLate/Stanford-NLP ColBERT checkpoints）+ColPali-family 视觉文档检索；Langflow 1.11.0 lfx-nextplaid 扩展包：ColBERT 晚交互+ColPali 视觉检索头等公民**（Creati.ai + Langflow）→ 判据：**工具链支持**——"ST v6.0 原生 MultiVector"=训练检索一体；"lfx-nextplaid"=低代码可用。
- **视觉文档检索与单模型双头**：**Nemotron ColEmbed V2：3B/4B/8B 晚交互 embedding 视觉文档检索 ViDoRe SOTA；Hydra：dual-head 单 VLM 同时提供 ColBERT 晚交互检索+自回归生成——单一 LoRA adapter 推理时切换：启用产多向量 embedding，禁用恢复基座生成质量（426/426 权重逐字节相同）**（arXiv）→ 判据：**单模型双能力**——"LoRA 切换"=检索生成一体免双部署；"权重逐字节相同"=切换无损。
- **提升层**：模型/工具（晚交互/多向量检索选型）。

## Graph RAG 轻量替代与统一栈（来源：Dify 1.12 Summary Index + microsoft/graphrag + AWS 统一栈 + n8n 多 KB/HybridRAG 2026 实拉，r641C 落地，与 §多跳 RAG 分工——那边管"多跳推理怎么架"，本条管"图检索怎么轻量落地"）
- **Summary Index 轻量替代**：**检索只返最相关单片段→模型缺上下文；GraphRAG 建实体关系图但实现复杂；Summary Index：每 chunk 附 summary 字段，语义相关内容一起检索——轻量替代**（Dify）→ 判据：**先轻量再上图**——"summary 字段"=零图基建；"GraphRAG 复杂"=最后手段。
- **图检索生态**：**microsoft/graphrag 36k+ stars MIT v3.1.0 基于图的 RAG 复杂文本推理（import 集成）；LightRAG+GraphRAG 统一栈（AWS 合规场景：几千合同回答"哪个义务会因里程碑延迟暴露"——答案不在任何单文档=多跳跨文档）；RAGU：多步 GraphRAG+紧凑域适配 LLM，pip install 单 GPU，发现 HippoRAG2 多跳优势大部分是响应格式 artifact**（DEV.co + AWS + ChatPaper）→ 判据：**跨文档问题=图/多跳**——"答案不在单文档"=检索面不足；"统一栈"=两类 RAG 一套部署。
- **混合编排**：**n8n HybridRAG：AI Agent 节点编排多检索工具——vector 语义+graph 关系型；两阶段检索：文件描述级过滤（metadata 匹配）→文件内 chunk 级（ID 二次查询+相似度阈值）；multi-KB agent：三向量库+Wikipedia fallback**（n8n）→ 判据：**双检索通道**——"vector+graph"=语义+关系互补；"两阶段"=先窄后深。
- **提升层**：工具/工作流（Graph RAG 轻量替代与统一栈）。

## 记忆检索与溯源审计（来源：OpenClaw memory citations + native-memory-citations 插件 + Dreaming 2026 实拉，r641C 落地，与 §Agent 工具面安全分工——那边管"工具威胁"，本条管"记忆检索的可审计性"）
- **片段强制来源**：**OpenClaw memory.citations 对所有 backend 生效：auto 默认=片段附带 "Source: ..." footer；on=Always include footer——检索结果强制带来源**（OpenClaw docs）→ 判据：**默认溯源**——"auto 附 Source footer"=零配置溯源；"on 强制"=合规场景。
- **有界可审计记忆访问**：**native-memory-citations 插件：operator 定义可搜索 workspace 文件/目录；访问前强制边界；返回前脱敏 secret 形状材料；附 citation metadata 每条答案可追溯到源——目标=operator 控制的检索+审计轨迹**（npm）→ 判据：**检索边界=权限边界**——"operator 定义可搜范围"=最小权限；"返回前脱敏"=不泄露；"citation metadata"=可审计。
- **记忆巩固三阶段**：**OpenClaw Dreaming：后台记忆整合系统三阶段（light 排序/stage 短期材料→REM 反映/surface 主题→deep 提升 durable 事实进 MEMORY.md）；Grounded backfill：重放旧笔记+检查系统认为 durable 的内容**（OpenClaw CLI）→ 判据：**记忆有巩固调度**——"light/REM/deep 三阶段"=短期→长期分步；"grounded backfill"=可检验持久化。
- **提升层**：可复用 Skill/工具（记忆检索与溯源审计）。
























