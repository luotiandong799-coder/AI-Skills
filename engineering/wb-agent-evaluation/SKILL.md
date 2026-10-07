---
name: wb-agent-evaluation
description: >-
  Agent 评估能力：让 Agent 不仅完成任务，还能判断自己完成得好不好。覆盖 Agent Trace（执行轨迹）、Observability（可观测性）、过程评估、结果评估、LLM-as-a-Judge、指标设计。核心产出：对真实 WB 任务复盘，区分「结果问题」与「执行过程问题」，并证明优化有效。当用户要求复盘一次 Agent 执行、评估某个技能/工具选择是否正确、检查是否存在无效步骤或未验证结论、设计评估指标时使用。触发词：复盘、评估这次执行、做得好不好、过程评估、结果评估、执行轨迹、LLM 评委、LLM-as-a-Judge、指标设计、trace 分析、无效步骤、未验证结论、优化有效吗、评测口径。不适用：单次任务的排障（走 wb-debug-loop）、生成物验证（走 wb-artifact-verification）。
version: 1.3.0
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

## 「按规程走完了」与「结果做对了」必须分列计量：单一总分会把「合规但无效」掩盖成「有效」（来源：arxiv.org/abs/2610.05161 44,911B，2026-10-08 一手 curl 逐串命中 `Protocol Completion Rate (PCR)` / `decouple it from the final Task Outcome` / `99.27%` / `82.95%`）
- **实证**：官方摘要原文「we introduce the **Protocol Completion Rate (PCR)**, defined as reaching accepted termination through all required phases, and **decouple it from the final Task Outcome**」；「Qwen3.5-4B achieves Protocol Completion Rates of **99.27%** on Math and **99.96%** on Search, while slightly outperforming original baselines in Task Outcome (**82.95%** and **46.61%**, respectively)」。
- **判据**：① **两轴必须分列**：PCR 99.96% 配 Task Outcome 46.61% 是同一模型的同一次评测——规程遵循近乎满分、成效不足五成；合成一个总分后，这条最关键的诊断信号（技能/规程本身合规但内容或能力不足）会被抹平成一个"还行"的分数。② **「合规但成效低」是独立的失败类型，修法不同**：PCR 低是规程/装载问题（没走完、缺终止态），Outcome 低是内容或能力问题（走了但方向不对）；混报会导致把内容缺陷按流程缺陷去修。③ **判据要能回答"终止态是否被显式声明"**：PCR 的定义依赖"到达 accepted termination"，技能若没声明合法终止态，这一轴根本无法计算 ⇒ 写技能时就要留退出判定。
- 提升层：工作流（评测计量）/ 可复用 Skill（指标设计）。触发词：PCR、Protocol Completion Rate、规程依从与成效解耦、99.27 vs 82.95、合规但无效、accepted termination。

## 评测设计三事：配对评测是地基、自生成技能实测为负、技能装配个数存在拐点（来源：arxiv.org/html/2602.12670v4（SkillsBench）738,092B → 去标签全文 124,551B，2026-10-08 一手 curl 逐串命中 `87 tasks across 8 domains` / `18 model–harness configurations` / `from 33.9% to 50.5% (+16.6 percentage points)` / `13 of 87 tasks show negative Skills deltas` / `-8.1 pp` / `2–3 Skills gain +19.0 pp`；与 §技能增益只能用配对差归因 互补——那条给归因原则与分维报数，本条给基准层一手量级与两条新增必测维度）
- **实证**：官方摘要原文「**87 tasks across 8 domains** paired with curated Skills and deterministic verifiers … under **matched no-Skills and curated-Skills conditions for 18 model–harness configurations**」；「Curated Skills raise the average pass rate **from 33.9% to 50.5% (+16.6 percentage points**; 25.5% normalized gain), with configuration-level gains ranging **from +4.1 to +25.7 pp**」；失败面「**13 of 87 tasks show negative Skills deltas**」；装配个数消融「tasks paired with **one Skill gain +18.0 pp, 2–3 Skills gain +19.0 pp, and ≥4 Skills give only +10.1 pp**」；自生成条件「**Self-generated Skills land below the no-Skills baseline on all three configurations (−8.1 pp** on Claude Code + Opus 4.7, **−11.3 pp** on Codex + GPT-5.5, **−11.5 pp** on Gemini CLI + Gemini 3.1 Pro), while curated Skills add **+18.2 to +24.8 pp** on the same configurations」；轨迹审计归因于「generated packs the solver never discovers」。
- **判据**：① **配对（matched with/without）是技能评测的地基不是加分项**：18 组配置的增益跨 +4.1 到 +25.7 pp，同一基准在不同 harness 上差 6 倍 ⇒ 只报"装了技能后 50.5%"毫无意义，可比的只有配对差；正常化增益（25.5%）须与绝对差（+16.6pp）并列，因为基线高低决定同一个绝对差的分量。② **「让 agent 自己写技能」是必测维度且实测为负**：三个配置全部低于无技能基线（−8.1/−11.3/−11.5 pp），而人工策展在同样配置下 +18.2~+24.8 pp ⇒ 差距不在"写得好不好"而在"会不会被发现"；技能若不进可发现面，写得再对也是死代码。③ **装配个数有拐点，不是越多越好**：1 个 +18.0 / 2–3 个 +19.0 / ≥4 个仅 +10.1 pp ⇒ 评估"该给几个技能"必须做上界实验，堆满技能包会把增益压回三分之一。④ **负增益是常态不是异常**：13/87 任务为负 ⇒ 报"平均提升"必须同列负例占比，只报均值等于把约 15% 的失败藏进均值。
- **与既有能力分工**：§技能增益只能用配对差归因（NVIDIA SkillEvaluator）给的是**单技能归因原则与分维报数**；本条给的是**基准层量级 + 两条新增必测维度（自生成 vs 策展、装配个数）**。
- 提升层：工作流（评测设计）/ 可复用 Skill（技能库准入）。触发词：paired evaluation、33.9 到 50.5、+16.6pp、13 of 87 负增益、自生成技能 −8.1、2–3 技能最优、≥4 只有 +10.1、技能个数拐点、curated vs self-generated。

## 组合级联是独立于「单件扫描」的失效模式：逐件全绿、组合发作，且一并绕过运行时监控（来源：arxiv.org/abs/2609.30383（SkillCascade-Bench）43,037B，2026-10-08 一手 curl 逐串命中 `213 validated cascading test cases` / `evading existing per-skill scanners and runtime monitors`；与 §评测设计三事 互补——那条管"单技能有没有增益"，本条管"多个都过审的技能放一起会不会出事"）
- **实证**：官方摘要原文「we develop **SkillCascade**, an automated multi-agent red-teaming framework, and release **SkillCascade-Bench**, a benchmark of **213 validated cascading test cases** across multiple agent systems and domains. Across representative agents (e.g., OpenClaw, Claude Code, Codex) and LLM backbones, **cascaded interactions reliably induce harmful behaviors while evading existing per-skill scanners and runtime monitors**」；摘要给的具体链条是三件各自合规的技能级联后，把一条严重告警的优先级压低、再在最终摘要里抑制掉，「so that a severe … warning **silently disappears** before reaching the physician」。
- **判据**：① **「每件都过审」不是装配安全的前提**：失效不在单个技能里，而在它们的交互上 ⇒ 引入多技能装配时，评测单元必须从「单件」扩到「组合」（技能对、三元组），只做单件审等于没审装配。② **绕过面同时覆盖静态扫描与运行时监控**：原文并列 per-skill scanners 与 runtime monitors ⇒ 加一道运行时监控不能替代组合级审查，两者是同一盲区下的两道同向失效。③ **级联的破坏形态是"静默降级"不是"报错"**：实例里没有任何环节失败——每件都按自己写的方式工作，结果是关键告警在汇总阶段消失 ⇒ 评测指标若只看"有没有报错/有没有拒绝"，抓不到这一类；要看**末端产物里关键信息是否还在**。④ **与既有条目串成链**：完整性（哈希/签名）→ 单件扫描（已知噪声率高）→ 上下文复核（裁决）→ **组合级联回归（本条）**，四道各自独立，任何一道通过都不代表下一道通过。
- **与既有能力分工**：wb-artifact-verification §恶意第二档零恶意件组合（r436A）管**验证侧要开组合档**；本条给**评测侧的基准与量级**（213 例、三实例链条、运行时监控一并失效）。
- 提升层：工作流（评测设计）/ 可复用 Skill（装配审查）。触发词：SkillCascade、213 cascading test cases、逐件全绿组合发作、evading per-skill scanners and runtime monitors、组合级回归、静默降级。
