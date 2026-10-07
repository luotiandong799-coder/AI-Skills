---
name: wb-agent-evaluation
description: >-
  Agent 评估能力：让 Agent 不仅完成任务，还能判断自己完成得好不好。覆盖 Agent Trace（执行轨迹）、Observability（可观测性）、过程评估、结果评估、LLM-as-a-Judge、指标设计。核心产出：对真实 WB 任务复盘，区分「结果问题」与「执行过程问题」，并证明优化有效。当用户要求复盘一次 Agent 执行、评估某个技能/工具选择是否正确、检查是否存在无效步骤或未验证结论、设计评估指标时使用。触发词：复盘、评估这次执行、做得好不好、过程评估、结果评估、执行轨迹、LLM 评委、LLM-as-a-Judge、指标设计、trace 分析、无效步骤、未验证结论、优化有效吗、评测口径。不适用：单次任务的排障（走 wb-debug-loop）、生成物验证（走 wb-artifact-verification）。
version: 1.1.0
---

# wb-agent-evaluation（Agent 评估与复盘）

定位：优化提升层。让 Agent 具备自评能力，源自 DeepLearning.AI「Agent Evaluation」模块。与 wb-artifact-verification 分工：那条管「生成物对不对」，本条管「执行过程与整体完成质量」。

## 一、评估对象二分

- **结果问题**：目标是否达成、产出是否正确可用。
- **执行过程问题**：Skill/Tool 选得对不对、有无无效步骤、有无未验证结论、是否绕路。

复盘时先定类是「结果」还是「过程」，再下结论；把两类混为一谈会修错地方。

## 二、复盘清单（对真实 WB 任务）

1. 目标是否完成？（对照用户原始意图，不是对照自己的计划）
2. Skill / Tool 选择是否正确？（该触发的是否触发、有无错触发/漏触发）
3. 是否存在无效步骤？（重试掩盖、重复调用、为表演而做的动作）
4. 是否出现未验证结论？（把推测当事实、缺证据链）
5. 如何证明优化有效？（要有 before/after 对照或可复跑的判据，不能「感觉变好了」）

## 三、核心能力

- **Agent Trace**：把一次执行的「调用了什么、顺序、输入输出、耗时、成败」抽成可检视的轨迹；没有 trace 就无法评估过程。
- **Observability**：在关键节点留结构化标记（开始/决策/调用/结果/结束原因），让复盘可依而非凭记忆。
- **LLM-as-a-Judge**：用模型做评委时，评委提示词须给出评分维度与锚点样例，且判分与「人审抽样」对比校准；禁止把评委分数当绝对真理。
- **指标设计**：区分结果指标（正确率、完成率）与过程指标（无效步骤数、重试次数、未验证结论数、工具错选率）；指标一经发布即锁定定义（见 wb-artifact-verification §指标锁定）。

## 四、结论格式

复盘输出必须含：① 结果/过程分类 ② 具体问题点（带 trace 证据）③ 改进项 ④ 验证方法（如何证明改后更好）。缺④等于没评估。

## 质量断言必须收敛为数值：先确定性规则、再资源数值、模型判分永远末位；「是否调了该调的工具」是 0/1 断言（来源：docs.n8n.io/build/integrate-ai/test-and-improve-ai-workflows/use-metrics-to-measure-quality.md 8,289B，经 llms.txt 287,049B 定位真路径后 2026-10-08 一手 curl 取 `.md` 原文逐串命中 `In n8n, metrics are always numbers` / `**Tools Used**: Whether the execution used tools or not. Returns a score between 0 and 1`；与 §评估对象二分 互补——那条管评什么，本条管断言用什么形态表达）
- **实证**：官方原文「**In n8n, metrics are always numbers.** You need to add the logic to calculate the metrics for your workflow, at a point after it has produced the outputs」；指标表含 **Tools Used**（「Whether the execution used tools or not. Returns a score between 0 and 1」）与 Correctness（对照参考答案，匹配返 1 否则 0）。评测执行与生产同路径开支（`Check If Evaluating` 分支隔离评测开销）。
- **判据**：① **不可聚合的判定进不了回归**：一切断言收敛为数字，散文式"看起来还行"无法跨轮比较、无法设阈值、无法画趋势 ⇒ 评测体系从"把判定写成数字"开始，不是从"多写几条检查"开始。② **工具调用断言是最便宜的行为回归**：`Tools Used` 只回答"有没有调该调的工具"，成本极低却能抓住"换了条路走"这一类退化；能力回归先加这一条，再谈质量分。③ **判分层级有固定顺序：确定性规则 → 资源数值 → 模型判分**：规则（包含/前缀及取反）零成本零方差、数值（token/延迟/输出长度）可阈值、模型判分（幻觉/Correctness 1–5）最贵且方差最大 ⇒ 能用规则判的不要交给模型，模型判分永远是末位选项。④ **评测流量要能从生产路径里被识别并隔离开销**：评测跑在生产路径上却不计成本，就是假账——省下的不是钱，是"这次评测花了多少"这个可回答的问题。
- **与既有能力分工**：§一「结果问题 vs 过程问题」管**评什么**；本条管**断言长什么样、按什么顺序选判定手段**。
- 提升层：工具（评测契约）/ 工作流（回归设计）。触发词：metrics are always numbers、Tools Used 0/1 断言、确定性规则优先、模型判分末位、token/延迟数值断言、Check If Evaluating、评测开销隔离。

## 技能增益只能用「配对差」归因并按维分列；必须保留净负案例，官方库里也有装了更差的技能（来源：developer.nvidia.com/blog/evaluating-ai-agent-skill-performance-with-nvidia-skillevaluator/ 257,328B，2026-10-08 一手实拉逐串命中 `Skill Lift of 41 points for Correctness and 39 points for Effectiveness` / `39 to 78` / `cuopt-install` increased tokens from 25,227 to 55,582 (120.3%)；与 §LLM-as-a-Judge 互补——那条管怎么打分，本条管"装了技能有没有变好"这个因果怎么证）
- **实证**：官方原文「Skill Lift of **41 points for Correctness** and **39 points for Effectiveness**」（基线 39 → 78）；分维结论「Discoverability, Effectiveness, and Efficiency, indicating substantial room for improvement. **Security was the exception**, with an average baseline score of 97」；跨 harness「per-product variation ranged from **+2 to +46 points**」；净负案例「`cuopt-install` increased tokens from **25,227 to 55,582 (120.3%)** and execution time from **34.0 to 41.1 seconds (20.8%)**」。
- **判据**：① **增益只能用配对差定义**（同一任务带技能分 − 不带技能分）：单跑一次的绝对分无法归因，"78 分"本身说明不了任何事——基线 39 的 78 是巨大提升，基线 97 的 78 是倒退。② **不许压成一个总分**：Discoverability / Effectiveness / Efficiency 三档各自有落差，而 Security 基线 97 几乎不动 ⇒ 一个总分会把"安全维没救了"这条最关键的信息抹平；分维报数也是优先级依据（先补哪一维）。③ **必须保留并公开净负案例**：官方认证库里仍有让 token +120.3%、耗时 +20.8% 的技能 ⇒ 任何"加装即增益"的汇报都是红旗；只报平均提升是把负例藏进均值里。④ **跨 harness 的方差大于 harness 之间的差异**（+2 到 +46）⇒ 结论要绑到具体产品与评测设计，不能说"某个 harness 更强"。
- **与既有能力分工**：§一「过程 vs 结果」管**一次执行怎么评**；本条管**加入某个能力后的因果增益怎么证**。
- 提升层：工作流（归因设计）/ 可复用 Skill（评测口径）。触发词：Skill Lift、配对差归因、分维报数、Security 基线 97、cuopt-install +120.3%、净负技能、+2 到 +46 方差、别把负例藏进均值。
