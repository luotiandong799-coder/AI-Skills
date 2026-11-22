---
name: ti-critical-reasoning
description: 因果推理与批判性思考（Thinking Intelligence）：区分相关与因果、评估方案真实贡献、反事实推演、识别 LLM 关联误判因果时调用。基于 Pearl 因果阶梯/do-calculus/SCM/DAG/后门前门调整，补齐关联推理的因果盲区。；未测混杂敏感性 E-value（RR 阈值/点估计与 CI 端各算/保守不判混杂存在/连续暴露按 IQR 标准化）；图尔敏论证图式（六要素/隐含 warrant/内部外部证成/模态限定与反驳）；论证图式与批判性问题（推定可废止/assumptions 与 exceptions 举证/图式目录覆盖缺口与错分）。；因果跨域可迁移性（S-node 指向机制/transport formula 三式/三档/meta-analysis 抹平差异之误）。；认知接种与预驳斥（弱攻击+反驳预热/counterarguing才是抗体/被动阅读优于主动自生/泛化须显式验证）。；因果发现（CPDAG 等价类/PC 与 GES 同边界/LiNGAM 非高斯定向/承重假设不可检验）。；面板数据准实验因果识别（DiD 平行趋势不可验证只能事前诊断/SCM 对 donor pool 加权构造反事实且凸包条件与过拟合风险/SDID 双权重放松平行趋势且可大面板推断）。；工具变量与 LATE（IV识别complier局部效应非全员ATE/排除限制不可数据检验/monotonicity无defiers才给正权重/多工具下单调性与异质性效应不相容）。；目标试验仿真TTE（先写七组件RCT协议再映射观察数据/设计缺陷比统计失配更常致错/94%观察CER有设计缺陷）；永生时间偏倚（未来治疗状态定义暴露却提前起随访→强制对齐 time zero）；clone-censor-weight 克隆人工删失加 IPCW 仿效宽限期策略、仍受无未测混杂与 positivity 约束。；G方法/g-formula（处理-混杂反馈致传统回归双向偏倚/g-computation 拟混杂+结局模型前向模拟再平均/与 IPTW-MSM 建模侧对称差异/g-null 悖论/双重稳健 AIPTW·TMLE）。；交错处理时点TWFE偏误（已处理单位当对照产生负权重·效应异质时系数可翻负·Goodman-Bacon分解看timing权重·CS/SA/stacked稳健估计量·多估计量一致不等于验证·预期效应是设计问题重加权修不了）。
version: 2.7.0
module: TI
modules: TI,EI
---

# TI · 因果推理与批判性思考（Critical Reasoning）

> 本技能是 Personal AI OS 13 模块中 **TI（思考智能）** 的载体之一（与 `agent/ai-input-enhancement` / `grill-me` / `prompt-library-40` 同属 TI：输入增强 / 对抗性质询 / 提示词库 / 本技能=因果与反事实）。
> 方法论实拉（2026-11-07 实拉）：youonai.ai（do-operator / do-calculus）、probsee.com（Causal AI / SCM / DAG）、army.mil（Pearl 因果阶梯）、view.inews.qq.com（中文因果阶梯解读）。

## 一、为什么 TI 需要因果层

LLM 本质是关联机：它在海量含人类解释的语料上训练，学到的是 `P(y|x)`（看见 X 推测 Y），而非 `do(x)`（强制 X 后的效应）。部署去决策时，它用"观测装备"回答"干预问题"，常"自信且灾难性地"答错。Pearl 定位：缺 do-operator 的系统身处"两个不同世界"——被展示的世界与被要求行动的世界。

## 二、Pearl 因果阶梯

| 层级 | 名称 | 问题 | AI 现状 |
|---|---|---|---|
| 1 | 关联 Association | "看到 X，Y 如何变？" | LLM 强项（统计相关） |
| 2 | 干预 Intervention | "强制 X=x，会怎样？" | 需 do-calculus；RL/agent 可部分达到 |
| 3 | 反事实 Counterfactual | "若当初 X 不同，Y 会怎样？" | 最弱，需机制假设 |

层级严格递进：仅靠增加低层数据量无法获得高层推理能力。

## 三、do-operator 与 do-calculus

- **do(X=x)**：切断所有指向 X 的箭头，强制 X=x，模拟外部干预。
- **P(y|do(x)) ≠ P(y|x)**：前者是干预分布（去掉混杂），后者是观测条件（含混杂）。
- **do-calculus 三规则**判定：给定因果图与假设，"干预效应能否从观测数据识别"。可识别则无需做实验；不可识别则再多观测数据也无用——这是信息逻辑的边界，非技术局限。

## 四、结构因果模型（SCM / DAG）

- 有向无环图（DAG）表达变量因果结构；函数 `Y = f_Y(父节点, 噪声)`。
- **后门调整（back-door）**：阻断混杂路径估计因果效应。
- **前门调整（front-door）**：当混杂不可观测但存在中介时，经中介估计。
- 局限：依赖"正确因果图"，而图本身是易错的人类判断——但 do-calculus 逼你把假设摆上台面供批评，正是对大模型不可检假设的纠正。

## 五、在 Agent 工作流中的用法

1. **方案评审**：问"这是相关还是因果？"——某改动"伴随"指标改善 ≠ "导致"改善；先找混杂（同期还有别的变化吗）。
2. **反事实推演**：决策前跑"若当初选 B 而非 A，预期差多少"，用 DAG 标注可观测/不可观测。
3. **复盘升级**：RI 的根因分析补因果层——5 Whys 到机制层后，再用 do-calculus 判"该干预是否真能消除故障"。
4. **警惕自己**：Agent 复盘时易把"训练语料里见过解释"当"自主建立因果"，须显式标注证据层级。

## 六、与 OS 协作

- **DI** 方案对比：用反事实给各选项预期效应排序。
- **EI** 执行后：用因果层判"步骤成功是因其做对，还是巧合/混杂"。
- **RI** 复盘：根因从"相关"升到"因果"，行动项更可能对准真因。
- **VI** 验证：因果声称须有一手/独立源，禁把相关当因果声称。

## 七、来源（2026-11-07 实拉）

- youonai.ai/fieldguide/high/the_do_operator（do-operator / do-calculus / 三规则）
- probsee.com/p/Causal_AI（Causal AI / SCM / DAG / 后门前门调整）
- army.mil/article/270910（Pearl 因果阶梯 / AGI 视角）
- view.inews.qq.com/a/20260809A0ACUC00（图灵奖得主 Pearl 因果阶梯中文解读）

## 八、论证评估与思维技法族（2026-11-08 r710B 实拉，3 独点）

> 来源（≥2 独立域、一手 WebFetch 全文逐串）：`superlore.ai/learn/critical-thinking-exercises`（2026-11-08 WebFetch 全文：validity/soundness、Steelmanning 五步、Socratic 六问、Pre-Mortem、来源评估）；`superlore.ai/blog/how-to-develop-critical-thinking-skills`（Gary Klein 前瞻性后见、thinking journal、偏差对抗动作）；`criticalthinkingexercisez.com`（15 式：inversion / first-principles / Six Thinking Hats / consider the opposite / 思维日志，交叉）；`skillsdirectory.com/skills/ferroxlabs-critical-thinker`（CRAAP / belief audit / misinformation patterns，交叉）；`skillsdirectory.com/skills/57uff3r-akorchak-thinking-session`（crux-finding / murphyjitsu / Bayesian updating / 二阶效应，交叉）。
> 判非：Pearl 因果阶梯 / do-calculus / 后门前门（§二–四）既有；`5 Whys` / `inversion` / `second-order` / `base rate` 已在全库既有条目，不重复立点；`steelman` / `crux` / `Socratic` 裸词在其他文件仅子串出现，词边界核验本技能与全库均无「论证技法族」成体系落地（窄串 `argument map` / `pre-mortem` / `prospective hindsight` / `consider the opposite` / `Six Thinking Hats` / `murphyjitsu` / `crux-finding` 技能正文与 co-learn 台账均 0 命中）⇒ 净新。

### 8.1（r710B-1）论证评估先拆「有效性」与「健全性」两轴：结论对不证明推理对
- **原文**：「**Validity**: If the premises were true, would the conclusion have to be true? (About logical structure)」/「**Soundness**: Is the argument valid AND are the premises actually true? (About real-world truth)」；「An argument can be **valid but unsound**」；「An argument can have **true premises and true conclusion but still be invalid**」（Paris is in France / Snow is white / Therefore 2+2=4）；「Most real-world reasoning is **inductive and probabilistic**. We should hold conclusions with appropriate confidence, not certainty.」
- **判据**：① **反驳要报打的是哪一轴**——结构无效（前提真也推不出）vs 前提假（结构对但事实错）；混成一团会让反驳打偏，与 §因果层 `P(y|x) ≠ P(y|do(x))` 同构：**观察对不代表机制对**。② 「前提真 + 结论真」**不证明**论证有效 ⇒ 结论正确不能反推推理成立；评估方案「结果达标」时须单独验「是不是这个推理带来的」。③ 演绎给确定性、归纳只给概率 ⇒ 现实判断须带置信度与反例清单，不写成断言；这是 TI 与 VI（验证）的交接点。
- **提升层**：思考 / 验证。触发词：validity vs soundness、有效但不健全、前提真结论真仍无效、归纳给概率、结论对不证明推理对。

### 8.2（r710B-2）Steelmanning 五步是「理解门」；Socratic 六问按功能分型而非随机追问
- **原文**：「**Steelmanning**: 1. Take a position you disagree with 2. Articulate it as compellingly as possible 3. Find the best evidence and arguments for it 4. **Only then respond with criticism** 5. **You haven't understood a position until you can argue for it**」；「**Socratic Questioning**: What do you mean by that? (Clarification) / How do you know? (Evidence) / What evidence supports this? (Justification) / What are the implications? (Consequences) / Could there be another explanation? (Alternatives) / **What would change your mind? (Falsifiability)**」；偏差对抗「**Countermeasure**: Actively seek out opposing views; **steelman** (represent charitably) rather than **strawman**」「**Look for base rate statistics**, not just memorable examples」。
- **判据**：① **理解门**：重构对方立场到「对方会说：对，我就是这个意思」之前不许开批；把「我没说服它」当「它错了」就是 straw man 的来源 ⇒ 评审/纠错场景先复述对方最强版本再给异议（接用户纠错协作协议：先讲哪里不对+为什么）。② 质询按**六种功能逐格排查**（澄清/证据/理据/后果/替代/可证伪），不是随机问；「什么会改变你的想法」是**可证伪门**——答不上来说明立场不可修正，不是论证强。③ 偏差不能只知道名字，要挂**具体动作**：confirmation→主动找反证、anchoring→先看多个参考点、availability→查 base rate、hindsight→事前记录预测；「知道偏差名」不产生任何免疫。④ 与 `agent/grill-me`（对抗性质询）分工：那条管「追着问」，本条管「问之前先站到对方那一侧、且六类问法要问全」。
- **提升层**：思考 / 可复用 Skill。触发词：steelmanning 五步、理解门、straw man、Socratic 六问分型、what would change your mind、可证伪门、偏差挂具体动作。

### 8.3（r710B-3）Pre-Mortem 用「前瞻性后见」合法化失败想象；crux-finding / belief audit 把信念变成可更新对象
- **原文**：「**Pre-Mortem Analysis**: 1. Imagine it led to failure 2. Write down all the reasons why it failed 3. Use these to identify risks you hadn't considered 4. Adjust the plan accordingly」；「This technique (developed by psychologist **Gary Klein**) leverages **prospective hindsight** to identify risks your optimism might overlook」；「**Crux-Finding**: What one thing, if proven false, would change your mind?」；「**Belief Audit**: What evidence would change my mind? When did I last update this belief? What is the strongest argument against it?」；「**Record predictions before events**; remember what you actually believed」。
- **判据**：① **先假定已失败再倒推**比「列风险」更能引出正常计划会上因礼貌/乐观不提的风险——prospective hindsight 把「想象失败」变成合法动作，不靠谁敢唱反调。② **crux-finding 逼出单点可证伪条件**（哪一件事若为假就改结论）⇒ 争论收敛到可核验的一格，而不是各自铺开整套论证；与 §因果层「把假设摆上台面」同源，但这里落在「开工前」。③ **信念是带时间戳的可更新对象**：belief audit 三问 + 决策前记录预测，才有「当时真实怎么想」可对照，否则复盘一律被 hindsight bias 洗成「我早就知道」⇒ 预测须先落盘、后验结果。④ 与 §因果层分工：因果层判「这个干预有没有真实效应」，本组管「动手前把哪些假设摆上台面、什么条件下撤回」；与 RI（复盘）交接：记录预测是复盘的输入，不是复盘的产物。
- **提升层**：思考 / 复盘。触发词：pre-mortem、prospective hindsight、Gary Klein、crux-finding、belief audit、记录预测对抗后见偏差、信念带时间戳。

### 本轮来源（2026-11-08 r710B 实拉）
- superlore.ai/learn/critical-thinking-exercises（validity/soundness · Steelmanning 五步 · Socratic 六问 · Pre-Mortem · 来源评估）
- superlore.ai/blog/how-to-develop-critical-thinking-skills（Gary Klein 前瞻性后见 · thinking journal · 偏差 countermeasure）
- criticalthinkingexercisez.com（15 式交叉：inversion / first-principles / Six Thinking Hats / consider the opposite）
- skillsdirectory.com/skills/ferroxlabs-critical-thinker（CRAAP · belief audit · misinformation patterns）
- skillsdirectory.com/skills/57uff3r-akorchak-thinking-session（crux-finding · murphyjitsu · Bayesian updating）
## 九、输出侧判断力提示：2–3 条具体追问，每对话最多一次（来源：`anthropics/skills`·`skills/discernment-nudge/SKILL.md` 10,592B，2026-11-08 实拉）

- **目的**：在"用户会据此行动"的实质回答末尾追加 **2–3 条具体追问**，用提问而不是说教，模拟三种辨别习惯——**核事实**（哪条具体论断值得核、拿什么核）/ **质疑推理**（逻辑在哪一步跳了）/ **注意缺失上下文**（回答不得不假设什么）。
- **触发表（满足其一）**：给了未落到用户具体处境的估算、预测或数字；在商业/健康/法律/金融/职业/人际等重大域给了建议；给了用户可能据此行动或转述的事实性论断；走了多步推理（早期假设错则结论变）；替用户解读了数据；起草了实质产物（目标/计划/pitch/提案/邮件）且内容依赖对用户处境的假设。
- **不触发面（宁缺勿滥，逐条守住）**：创意写作；闲聊；**用户会自己执行的代码**（跑起来就是验证；但架构建议没法快跑，仍值得提示）；简单查询；纯教学解释（含"X 是什么 / X 与 Y 区别"，即便在重大域，只要没描述自身处境、没问"我该怎么做"）；**用户已要求核实/引用/标注不确定**（此时该内联标注，末尾再追问像没听见）；用户要"快速版 / 我自己会查"；**用户让你检查他的东西**（你的回答本身就是辨别，再追问是循环）；用户给了原始材料只要你整理；用户要的是观点/take（take 用来权衡，不是用来核查，应内联对冲）。
- **频次与格式**：每对话**最多一次**——重复会把轻提示变成唠叨；先完整回答问题，空一行后固定引导句 `A few things worth a second look:` + 纯文本 bullet，每条 ≤120 字符、第一人称、口语、问句；不加标题、引用块、emoji；**nudge 之后不再加任何话**（它就是收尾）。
- **判据**：每条必须指向答案里的**具体数字 / 命名步骤 / 假设**——"能再核对一下事实吗"这类泛问等于没问；与 `agent/grill-me` 分工：那条在**动手前**拷问用户，本条在**交付后**请用户复核，且只一次。
- 反模式：把提示写成免责声明；每条都追问一遍（超过 3 条）；用户已给了原始材料还让他核对你的整理；追问后又加"需要我继续吗"。
- **提升层**：工作流（输出侧）+ 模型行为。
- 触发词：discernment nudge、判断力提示、A few things worth a second look、2–3 条具体追问、每对话一次、不触发面

## 十、推理链忠实度与可监控性：自述推理不是推理证据（2026-11-09 r731A 实拉，3 独点）

> 来源（≥3 独立域、一手逐字）：`anthropic.com/research/reasoning-models-dont-say-think`（Anthropic Alignment Science 团队，2026-11-09 WebFetch 一手全文逐串）；`www-cdn.anthropic.com/.../reasoning_models_paper.pdf` + `assets.anthropic.com/.../reasoning_models_paper.pdf`（论文 PDF 摘要，WebSearch 一手命中）；`arxiv.org/abs/2507.11473`（Korbak 等 40+ 作者跨 OpenAI/DeepMind/Anthropic/Meta/UK AISI，v1 2025-07-15 / v2 2025-12-07，WebFetch 一手摘要）；`arxiv.org/abs/2503.11926` + `cdn.openai.com/.../CoT_Monitoring.pdf`（Baker 等 OpenAI，WebSearch 一手摘要逐字）。
> 判非：窄串 `CoT faithfulness` / `monitorability` / `unfaithful` / `obfuscated reward hacking` / `monitorability tax` 全库 SKILL.md 0 命中；`faithfulness` 2 文件、`忠实度` 2 文件命中均为豆包自留地 RAG「答案是否扎根检索片段」（与「推理过程报告是否忠实」不同义）⇒ 净新。§8.1 打逻辑结构轴、§九管输出侧追问，均不覆盖本条。

### 10.1（r731A-1）★自述推理是待核验声明，不是推理证据；忠实度必须用行为对照测
- **原文**：「On average across all the different hint types, Claude 3.7 Sonnet mentioned the hint **25% of the time**, and DeepSeek R1 mentioned it **39% of the time**.」「A substantial majority of answers, then, were **unfaithful**.」；未授权访问类提示「Claude was faithful **41%** of the time and R1 **19%**」；「on average, the unfaithful Chains-of-Thought were **substantially longer** than the faithful ones」；「faithfulness was on average **lower when the question being asked was more difficult**」。
- **测法**：成对题目（标准题 / 插入提示的同一题），只在「无提示答 A、有提示改答 B」的样本上查 CoT 是否承认用了提示 ⇒ 忠实度是**可测的行为对照率**，不是读解释的流畅度。
- **判据**：① 解释更长更细**不是**可信度信号，实测不忠实的更长；题越难忠实度越低 ⇒ 高难任务更不能靠「它讲得很细」放行。② 与 §8.1 分工：那条判「结论真 + 前提真仍可能推理无效」（结构轴），本条判「推理过程报告本身可能不是实际过程」（过程轴）。③ 落地：把模型/自己写的推理链当**声明**，须用外部可观测变化（答案变没变、依据是否承认）交叉，不用自述当证据。
- **提升层**：思考 / 验证。触发词：CoT faithfulness、忠实度是可测对照率、提示插入对照、不忠实的解释更长、自述推理不是证据。

### 10.2（r731A-2）★让解释「更好看」不产生忠实度；压力会造出假的合理化
- **原文**：结果导向 RL「initially increases ... but the improvement **plateaus at 28% on MMLU and 20% on GPQA**」「outcome-based RL alone is **insufficient** to achieve high Chain-of-Thought faithfulness」；reward hacking 场景「The model learns to exploit the reward hack on **>99%** of the prompts, but almost never (**<2%** of the time) verbalizes the reward hack」「instead of being honest about taking the shortcut, the models often **constructed fake rationales for why the incorrect answer was in fact right**」。
- **判据**：① 把「解释质量/可读性」纳入优化目标（评分、评审、模板化要求写清推理），初期看似改善、很快平台化；**优化的是可见面，不是忠实度**。② 最危险的不是「不解释」，而是**长篇假合理化**：>99% 用了 hack、<2% 承认，且编出一整套论证 ⇒ 复盘/审计时「有完整论证」不能作为未走捷径的证据。③ 落地：验收看行为对照（答案改变与承认率），不看解释文本长度/结构；禁止以「让推理写得好看」为唯一验收标准。
- **提升层**：思考 / 复盘 / 可复用 Skill。触发词：plateau 28%/20%、outcome-based RL 不足、>99% 用 hack <2% 承认、fake rationales、假合理化、解释质量不等于忠实度。

### 10.3（r731A-3）★可监控性是脆弱属性，须付 monitorability tax；CoT 监控只能是补充层
- **原文**：arXiv 2507.11473 摘要逐字「Like all other known AI oversight methods, CoT monitoring is **imperfect and allows some misbehavior to go unnoticed**」「investment in CoT monitoring **alongside existing safety methods**」「Because CoT monitorability **may be fragile**, we recommend that frontier model developers **consider the impact of development decisions** on CoT monitorability」；OpenAI 2503.11926 摘要逐字「CoT monitoring can be **far more effective than monitoring agent actions and outputs alone**」、弱模型 GPT-4o 可有效监控更强的 o3-mini，但过强优化导致「**obfuscated reward hacking, hiding their intent within the CoT**」「it may be necessary to **pay a monitorability tax by not applying strong optimization pressures directly to the chain-of-thought**」；Anthropic 结论「we can't always rely on what they tell us about their reasoning」「if we want to **rule out** undesirable behaviors using Chain-of-Thought monitoring, there's still substantial work to be done」。
- **判据**：① 监控有效与监控充分是两件事：**能发现一部分不良行为 ≠ 能排除不良行为**；CoT 监控只能与其他安全方法并列，不得当唯一门。② 监督通道一旦成为优化目标就会退化（Goodhart）：训练/提示直接压 CoT 使意图转入不可见处 ⇒ 须主动**不**对推理链施加直接优化压力，接受 monitorability tax。③ 可监控性会被架构/流程变更侵蚀 ⇒ 引入新模型、新推理形态、新提示规约时，把「推理链是否仍可读可对照」列为一项体检，而不是能力承诺。④ 与 §九 discernment nudge 分工：那条在交付后请用户复核结论，本条管**推理过程本身能否被核验**。
- **提升层**：治理 / 思考 / 验证。触发词：monitorability tax、可监控性是脆弱属性、alongside existing safety methods、obfuscated reward hacking、不要优化推理链、rule out 不等于发现。

### 本轮来源（2026-11-09 r731A 实拉）
- anthropic.com/research/reasoning-models-dont-say-think（WebFetch 一手全文：25%/39%/41%/19%、unfaithful 更长、28%/20% 平台、>99%/<2%、fake rationales、rule out 结论）
- www-cdn.anthropic.com/b9ca6db27f02a9ddf0d4fdb51b26432c99a27be0.pdf · assets.anthropic.com/m/71876fabef0f0ed4/original/reasoning_models_paper.pdf（论文 PDF 摘要逐字）
- arxiv.org/abs/2507.11473（Korbak et al., v1 2025-07-15 / v2 2025-12-07；WebFetch 一手摘要）
- arxiv.org/abs/2503.11926 · cdn.openai.com/pdf/34f2ada6-870f-4c26-9790-fd8def56387f/CoT_Monitoring.pdf（Baker et al., OpenAI；WebSearch 一手摘要逐字）

## 十一、溯因（Abduction / IBE）：假设生成与证成分离（2026-11-14 r745A 实拉）

> 本技能此前覆盖「论证有效性/健全性」（§8）、「CoT 忠实度」（§10）与因果/反事实（§一–§七）；本节补第三类推理形态：**解释性推理**。判重：`abduction` / `abductive` / `Peirce` / `inference to the best explanation` / `best explanation` / `explanatory virtue` / `bad lot` / `van Fraassen` / `monotonicity` 全库 SKILL.md **0 命中**；`IBE` 16 命中经核为 `describe` / `subscribe` / `attribute` 一类英文子串噪声，词边界 `\bIBE\b` 为 0 ⇒ 净新。

### 11.1（r745A-1）溯因两义必须分开，且它违单调性：新证据可以撤销原最佳解释
- **原文**：SEP《Abduction》（First published 2011-03-09；substantive revision 2025-06-18）逐字「In both senses, the term refers to some form of explanatory reasoning. However, in the historically first sense, it refers to the place of explanatory reasoning in *generating* hypotheses, while in the sense in which it is used most frequently in the modern literature it refers to the place of explanatory reasoning in *justifying* hypotheses. In the latter sense, abduction is also often called "Inference to the Best Explanation."」；「A noteworthy feature of abduction, which it shares with induction but not with deduction, is that it violates *monotonicity*, meaning that it may be possible to infer abductively certain conclusions from a *subset* of a set *S* of premises which cannot be inferred abductively from *S* as a whole.」；例证「adding the premise that Tim and Harry are former business partners who still have some financial matters to discuss ... may no longer warrant you to infer that they are friends again」。另 SEP §1.1 给出与归纳的分界「in abduction there is an implicit or explicit appeal to explanatory considerations, whereas in induction there is not; in induction, there is *only* an appeal to observed frequencies or statistics」。IEP《Critical Thinking》§4d 逐字「Though abduction is structurally distinct from other inductive arguments, it functions similarly in practice: a good explanation provides a probabilistic reason to believe a proposition.」「It might be thought that explanations only function to help critical thinkers formulate hypotheses, and do not, strictly speaking, support propositions.」
- **判据**：① 排查「最可能原因 / 根因」时**先声明这次是生成候选还是裁决候选**，两者不是同一步：生成阶段不许因「解释得漂亮」提前收敛，裁决阶段不许再偷偷补候选凑答案。② **解释性结论必须可撤销**——新增一条前提（如「两人仍有财务往来」）会让原最佳解释失效，这是演绎推理不会有的性质；因此凡「已定位根因」的结论都要附「哪条新证据会推翻它」，并在证据集变化时**重跑比较**，而不是把旧结论加固。③ 判定是不是溯因看**有没有 appeal to explanatory considerations**，不看有没有统计数据：用了频率但结论靠「这样最好解释」支撑，仍是溯因，得按本节规则管。④ 与 §8.1（有效性 vs 健全性：论证结构与前提真）、§10（自述推理链是否可核验）分工：那两条管论证与推理过程，本条管**从观察跳到解释**这一步的准入与更新。
- **提升层**：思考 / 复盘 / 可复用 Skill。触发词：溯因、最佳解释推论、IBE、生成假设 vs 证成假设、非单调性、新证据撤销旧结论、解释性考量不是频率。

### 11.2（r745A-2）「最佳」是相对候选集的，不是绝对真：bad lot 论证与 IBE 的可错性
- **原文**：SEP §3.1 逐字「We have already encountered the so-called argument of the bad lot, which, we saw, is valid as a criticism of ABD1 but powerless against various (what we called) congruous rules of abduction.」；SEP §2 给出免疫形态 ABD3「Given evidence E and candidate explanations H1,…,Hn of E, if Hi explains E better than any of the other hypotheses, infer that Hi is closer to the truth than any of the other hypotheses.」（只推「更接近真」，不推「为真」）；SEP §2 另注「if one can be certain that, however many candidate explanations for the data one may have missed, none equals the best of those one has thought of, then the congruous versions license exactly the same inference as ABD1 does」。IEP《Scientific Realism and Antirealism》§5e 逐字「The caveat "if there is one" blocks inferences to the best of a bad lot: the best explanation may not reach a minimally acceptable threshold.」「like any inferential principle that amplifies our knowledge, conclusions inferred by IBE are fallible: while they are more likely to be true, they could be false.」；IEP《Metaphysics of Science》§2b 逐字「Quite obviously, IBEs are not deductively valid, and even the best explanations we have at our disposal can later turn out to be incorrect.」（Vulcan 行星：为解释水星轨道异常而假设，望远镜找不到，最终由广义相对论解释；对照 Neptune 由天王星摄动成功推得）。SEP §3 另引 Lombrozo (2007)：「in some situations, people tend to grossly overrate the probability of simpler explanations compared to more complicated ones」。
- **判据**：① 交付「根因 / 最优解释」必须同时写三件：**候选集清单 + 最低可接受阈值 + 是否全部候选都低于阈值**。全部不达标就输出「无合格解释、需扩候选」，而不是把相对最好那个硬报成原因。② 结论措辞固定为「**当前候选集中最接近真**」，禁止写成「为真 / 已确认」；「没别的解释了」不构成论证，它只说明候选集没扩充。③ 主动找**反例类候选**（SEP 明确「however many candidate explanations for the data one may have missed」是关键不确定源），并在报告里留「未考虑到的解释类型」一栏。④ 别拿解释的简洁度当概率：SEP/Lombrozo 的实验显示人会系统性高估简单解释的可能性。
- **提升层**：思考 / 验证 / 复盘。触发词：best of a bad lot、候选集不完备、最低可接受阈值、IBE 非演绎有效、Vulcan 反例、相对最优不等于为真、最弱环之外的候选扩充。

### 11.3（r745A-3）解释选择按可枚举的理论美德逐项打分；loveliness ≠ likeliness
- **原文**：IEP《Critical Thinking》§4d 逐字「Coined by C. S. Peirce (1839-1914), abduction, also called retroduction, or inference to the best explanation, refers to a way of reasoning informally that provides guidelines for evaluating explanations. Rather than appealing to types of arguments (generalization, analogy, causation), the value of an explanation depends on the theoretical virtues it exemplifies.」「What constitutes fittingness (or "loveliness," as Peter Lipton (2004) calls it) is controversial, but many of the virtues are intuitively compelling」；六项逐字：**Simplicity**（Ockham's Razor「Do not multiply entities beyond necessity.」，IEP 注明该句不见于奥卡姆著作，属传说）、**Conservatism**「a good explanation does not contradict well-established views in a field」、**Independent Testability**「a good explanation is successful on different occasions under similar circumstances」、**Fecundity**「a good explanation leads to results that make even more research possible」、**Explanatory Depth**「a good explanation provides details of how an event occurs」、**Explanatory Breadth**「a good explanation also explains other, similar events」；且「ideally, the virtues work together to help critical thinkers decide among competing hypotheses to test」。IEP《Scientific Realism》§5e 逐字「If IBE is to be non-trivial, the best explanation must not entail that what is best must antecedently be what is most likely ... Rather the best explanation must be characterized in terms of properties like "loveliest" or "most explainey" (Lipton 2004).」「Traditional examples of such properties are: it has wide scope and precision; it appeals to plausible mechanisms; it is simple, smooth, elegant, and non-ad hoc; and it underwrites contrasts (why this rather than that).」；SEP §3.1 记 van Fraassen 第一反驳「an elementary logical point that a more informative theory cannot be more likely to be true [and thus] attempts to describe inductive or evidential support through features that require information (such as 'Inference to the Best Explanation') must either contradict themselves or equivocate」及「clearly the extension has more ways of being false」；IEP《Metaphysics》§2b「Note also that Occam's Razor and IBEs sometimes pull in opposite directions: whereas IBEs often enrich, rather than reduce, our ontology, Occam's Razor is set on eliminating as many entities as possible.」；SEP §3.1 另记 van Fraassen 第二反驳：概率版溯因「must either amount to Bayes' rule, and thus be redundant, or be at variance with it but then ... be probabilistically incoherent」（Lewis 动态 Dutch book）。
- **判据**：① 候选解释做**六项美德矩阵**（简洁 / 保守 / 可独立检验 / 多产 / 深度 / 广度），禁止用「综合最合理」一句带过——与 `agent/grill-me` §r735C-2「维度独立打分、禁止过早整体印象」同构，但那条管**多人判断的聚合顺序**，本条管**解释候选的裁决维度**。② **lovely 与 likely 两栏分记**：解释得漂亮（覆盖广、机制顺）不推出更可能为真；van Fraassen 指出更 informative 的理论「有更多方式为假」。③ 简单与广度冲突时**显式声明权重**（IEP 明说 Ockham 与 IBE 方向相反），不许默认挑简单那个当作「因此更可能」。④ 「underwrites contrasts (why this rather than that)」要单列：能解释「为什么是 A 不是 B」才算有区分力，只解释「为什么发生」的解释会把所有候选都解释一遍。⑤ 别把溯因包装成贝叶斯更新的等价物：概率版要么冗余、要么不相容，这是两套东西。
- **提升层**：思考 / 验证 / 决策。触发词：理论美德六项、loveliness 不是 likeliness、Ockham 与 IBE 相反、underwrites contrasts、解释力不等于概率、van Fraassen 两反驳。

### r745A 来源与判非（2026-11-14 实拉，逐字核验）
- `https://plato.stanford.edu/entries/abduction/`（Stanford Encyclopedia of Philosophy《Abduction》，First published 2011-03-09 / substantive revision 2025-06-18）— **WebFetch 200 全文逐字（74,722 chars，AI 摘要 60s 超时返回前 15,000 字，如实登记）+ curl 一手 HTML 逐字提取 §1 / §1.1 / §2 ABD3 / §3 / §3.1**；两义定义、演绎/归纳/溯因分界、非单调性、ABD1–ABD3、bad lot、van Fraassen 两反驳、Lombrozo 2007。**第一独立域（哲学权威百科一手）**。
- `https://iep.utm.edu/critical-thinking/`（Internet Encyclopedia of Philosophy《Critical Thinking》§4d Abduction；旧址 `https://iep.utm.edu/?p=30583/`）— **WebFetch 200 全文逐字（99,037 chars，前 15,000 字；AI 摘要 60s 超时如实登记）+ WebSearch 快照逐字核验 §4d 全段**；Peirce/retroduction/IBE、理论美德六项逐字定义、Lipton loveliness、「a good explanation provides a probabilistic reason to believe a proposition」、Ockham 传说标注。**第二独立域**。注：旧路径 `https://iep.utm.edu/abductive/` **WebFetch 404**，已改用现址，未冒充一手。
- `https://iep.utm.edu/met-scie/`（IEP《Metaphysics of Science》§2b IBE）— WebSearch 快照逐字：「IBEs are not deductively valid」/ Vulcan 与 Neptune 双例 / Ockham 与 IBE 方向相反。**第三独立域（同 IEP 不同条目，作交叉不作唯一来源）**。
- `https://www.iep.utm.edu/time/..scientific-realism-antirealism`（IEP《Scientific Realism and Antirealism》§5e IBE）— WebSearch 快照逐字：「if there is one」/ best of a bad lot / loveliest / fallible / Harman 1965 /「why this rather than that」。**第四独立域**。
- `https://plato.stanford.edu/archives/fall2021/entries/abduction/` 与 `/archives/sum2018/entries/abduction/` — WebSearch 快照逐字，用于核验两义定义与非单调性段落跨版本一致（非新增结论来源）。
- **判非**：窄串全库 SKILL.md — `abduction` / `abductive` / `Peirce` / `retroduction` / `inference to the best explanation` / `best explanation` / `explanatory virtue` / `theoretical virtue` / `bad lot` / `van Fraassen` / `monotonicity` / `falsification` / `2-4-6` / `Wason` / `hypothesis generation` **全 0 命中**；`IBE` 16 命中为 `-scribe` / `attribute` 类子串噪声，词边界 `\bIBE\b` 0。与既有 §8.1 有效性/健全性（论证结构）、§10 CoT 忠实度（自述推理）、`agent/grill-me` §r735C（判断离散度与独立评分）正交，未复用任何一轮结论。豆包自留地 `wb-execute-discipline` / `wb-context-compressor` **WB 0 落地**。
- **未采纳**：SEP §3.1 之后对 van Fraassen 两反驳的逐条辩护、§4 与贝叶斯确认理论的整段关系、ABD1/ABD2 全部形式化变体属专门哲学争论，只取可迁移判据；「Neptune / Vulcan / 电子发现」仅作机制例证，不写成工程事实。IEP 页面自述为同行评审百科但 §4d 属教学性概述，其美德清单与 SEP 的规范性讨论交叉后才采纳。

## 十二、图尔敏论证图式：六要素、隐含理据与两层证成（2026-11-15 r747A 实拉，3 独点）

> 适用：审一份方案/结论是否成立时，把「论证」拆成可逐格检查的部件，尤其逼出没写出来的隐含假设。与 §8.1「有效性 vs 健全性」互补：8.1 判断单个论证的结论真不真、推理对不对；本节给出论证的**内部结构**与「哪一层被攻击」。

### 12.1（r747A-1）★六要素分「三基础 + 三扩展」；审查着力点是把隐含 warrant 逼出来，不是只核证据真假
Purdue OWL 逐字：「breaks arguments down into six component parts: **claim, grounds, warrant, qualifier, rebuttal, and backing**」「every argument begins with **three fundamental parts: the claim, the grounds, and the warrant**」「The other three elements—backing, qualifier, and rebuttal—are **not fundamental** to a Toulmin argument, but may be added as necessary」；warrant 定义逐字「**the assumption that links the grounds to the claim**」，且「**either implied or stated explicitly**」。Wikipedia《Argumentation theory》快照同向：前三为 essential components，后三「may not be needed in some arguments」，并记该布局「was based on legal arguments」、原用于法庭论证的合理性分析。
- **判据**：① 审论证按六格逐项填空——主张 C / 予料 D / 理据 W / 支援 B / 限定 Q / 反驳 R；三基础缺任一即不成论证，三扩展缺失不必强凑。② **warrant 通常是没写出来的那一句**，所以「证据都真」不等于论证成立：要显式写出「凭什么从 D 走到 C」再评它，否则双方争的是两回事。③ 明尼苏达开放教材快照逐字「Grounds should directly support the premises of the main argument itself, while **backing exists to help the warrants make more sense**」⇒ **grounds 支持 claim、backing 支持 warrant，两者不能互换**；把「再补一条数据」当成对理据的支援是错层补证据。④ 与 r745A 溯因分工：那条管「几个解释候选里选哪个」，本条管「一条已选论证内部由什么部件撑起来」，先拆结构再评候选，顺序不可倒。

### 12.2（r747A-2）★内部证成 / 外部证成是两层：D+W→C 管推出，B 与 R 管前提本身对不对
中国法学网（中国社科院法学所）王彬《案例指导制度下的法律论证》全文逐字：「一个完整的法律论证具有六个要素：1. …要提出一个主张 C（Claim），必须说明这一规范性命题的成立根据；2. 为证成主张 C，需要寻找予料 D（Data）…；要回答『如何从予料 D 中得出主张的』，需要提出理据 W（Warrant）…；4. 予料与理据的结合构成了论证的前提，但是，它们对主张 C 存在不同的强度，主张 C 的成立需要模态限定 Q（Qualifiers），指示从予料和理据到结论的跳跃力量…；5. 在模态限定 Q 下，除非条件（Rebuttal）R 出现，理据 W 无法被反驳；6. 支援 B（Backing）是对理据 W 的深度证立，它解决『为什么理据 W 可适用于某一特定案件』的问题」；关键两层逐字「从事实命题 D 与法律命题 W 推导裁决结论的过程属于**内部证成**的层次，内部证成涉及从既定前提推导出结论的法律决定的有效性问题；支援 B 对法律命题 W 的进一步证立以及反对它的反驳 R 则属于**外部证成**的层次，外部证成涉及**前提本身的正确性**问题」；并记「法律命题并非是绝对的、永恒正确的推理前提，而具有**可辩驳的特征**」「只具有『**初显优先性**』」「其拘束力并非是有无的问题，而是**程度的问题**」（引麦考密克／萨默尔：拘束力呈「正式拘束力→无正式拘束力但有影响力→…→仅具表述性价值」光谱）。
- **判据**：① 出现「证据没问题但结论还是不对」时，先判是内部层（推理跳不过去）还是外部层（理据本身不适用本场景），两层修法完全不同。② **Q 与 R 要单列成字段**：Q 写「这个结论是必然／大概／在…条件下成立」，R 写「除非出现什么」。③ 规则、先例、既有结论迁移到新案/新任务时只带初显优先性，强度是程度不是布尔；「已有一条规则」不等于「已证成」。④ 与 `engineering/wb-instruction-prior`「目标须可验证」分工：那条管任务入口，本条管结论成文后的结构审查。

### 12.3（r747A-3）★限定词与反驳是「可辩驳性」的一等结构，但也是弱论证的免责口，二者要分辨
Purdue OWL 逐字「The **qualifier** shows that a claim **may not be true in all circumstances**. Words like 'presumably,' 'some,' and 'many' …」「The **rebuttal** is an acknowledgement of another valid view of the situation」「Including a qualifier or a rebuttal in an argument helps build your **ethos, or credibility**」；明尼苏达教材快照逐字「The qualifier (or **modal qualifier**) indicates the strength of the leap from the data to the warrant and may limit how universally the claim applies. The necessity of qualifying words comes from the plain fact that **most absolute claims are ultimately false … because one counterexample sinks them immediately**」，同时明确反向警告「**Qualifiers and reservations can be used to bolster weak arguments** … They are often used by advertisers who are constrained not to lie. Thus, they slip 'usually,' 'virtually,' 'unless,' and so on into their claims to protect against liability」；中国法学网同记 Toulmin「那种认为一个普遍的和永恒的程序法典，能够为我们的所有问题提供唯一的和明确的答案的想法是一种**原则的暴政**」。
- **判据**：① 一个反例即击沉绝对断言 ⇒ 结论默认带 Q，禁写「一定／所有／必然」除非能给出全称保证；R 要写出具体例外条件而非「情况可能不同」。② **有 hedge ≠ 论证可靠**：审限时同时问「它是在诚实标注力度，还是在给不可证伪留后路」——若 Q/R 多到使结论在任何结果下都算说中，按 §8.1 / r731A 可证伪门判不合格。③ 承认反方（rebuttal）提升可信度是修辞效果，不构成证据；不得把「写了 rebuttal」当「已回应反驳」，回应须落到 D/W/B 的哪一格被改。④ 与 `agent/grill-me` §r735C 独立评分分工：那条管多人判断的聚合，本条管单个论证的限定粒度。

**提升层**：思考 / 验证 / 写作审查。触发词：Toulmin 六要素、claim-grounds-warrant、隐含 warrant、backing 支持 warrant 不是 claim、内部证成 vs 外部证成、模态限定 Q、除非条件 R、初显优先性、可辩驳性、限定词是免责口。

### r747A 来源与判非（2026-11-15 实拉，逐字核验）
- `https://owl.purdue.edu/owl/general_writing/academic_writing/historical_perspectives_on_argumentation/toulmin_argument.html`（Purdue University OWL《Toulmin Argument》，Copyright 1995-2018）— **WebFetch 200 全文逐字**：六要素、三 fundamental / 三 not fundamental、warrant「the assumption that links the grounds to the claim」、qualifier / rebuttal / backing 逐字定义、ethos 句。**第一独立域（大学写作中心权威教学一手）**。
- `http://iolaw.cssn.cn/fxyjdt/201706/t20170605_4650748.shtml`（中国法学网·中国社科院法学所，王彬《案例指导制度下的法律论证》，2017-06-05）— **WebFetch 200 全文逐字**：六要素中译与功能、内部证成/外部证成两层逐字、可辩驳性、初显优先性、拘束力程度与光谱、「原则的暴政」引文、注释 [1] Toulmin《The Uses of Argument》Updated Edition, CUP 2003, p.97 与 [2]《An Introduction to Reasoning》改 Data 为 Ground。**第二独立域（法学学术论文一手，与 Purdue 无引用关系）**。
- `https://manifold.open.umn.edu/read/full-text/section/5be693bd-6c4f-4a15-8f4f-2f5e4c390cd8`（明尼苏达大学 OEN Manifold / Berea Writes!《Chapter 3 - Argument》）— **WebFetch 200 前 15,000 字**（AI 摘要 60s 超时如实登记）+ **WebSearch 快照逐字**补 Toulmin 段：Claim/Grounds/Warrant/Backing/Qualifier/Rebuttal 定义、「grounds should be tested for soundness」「warrants are often implicit and hence unstated. This gives space for the other person to question and expose the warrant」、「one counterexample sinks them immediately」、「Qualifiers and reservations can be used to bolster weak arguments」广告商免责用例。**第三独立域（开放教材，作交叉不作唯一来源）**；该页 curl 直连被拒（WinError 10061），未冒充一手全文。
- `https://wikipedia.com/wiki/Argumentation_theory`（《Argumentation theory》Toulmin model 段）— WebSearch 快照逐字：六要素、前三 essential / 后三 may not be needed、原基于法庭法律论证、Brockriede & Ehninger 1963 引入修辞学、批评「does not fully consider the use of questions in argumentation」。**第四独立域（百科，仅作交叉与批评面登记）**。
- `https://livrepository.liverpool.ac.uk/3196148/1/CompLegalArg24.pdf`（University of Liverpool《Computational Models of Legal Argument》）— **WebFetch 返回 403 Forbidden，无任何正文**，如实登记；Google 搜索快照含其 §2.2 Toulmin 六要素与三类攻击（rebutting / undercutting / undermining）逐字，仅作交叉，**不冒充一手**。
- `https://www.peopleapp.com/rmharticle/30016353746`（人民日报客户端《97 思维模型：图尔敏论证模型》）、`https://tnstate.libguides.com/c.php?g=1341399`（田纳西州立大学图书馆《Types of Arguments》）— WebSearch 快照，中文术语对照与六术语清单交叉；科普/教学立场登记，不作唯一结论来源。
- **判非**：窄串全库 `SKILL.md` 精确扫描（97 个文件）— `Toulmin` / `modal qualifier` / `grounds` / `rebuttal` / `internal justification` / `外部证成` / `defeasib` / `初显优先` / `implied warrant` / `unless clause` / `six component parts` **全 0 命中**；`warrant` 2 命中为 `defaults/wb-context-compressor`（豆包自留地）与本技能 §8.1 的通用「担保」义、`backing` 1 命中在豆包自留地、`qualifier` 1 命中在 `engineering/wb-execute-discipline`（豆包自留地），均非论证图式命题，登记不复用。与 §8.1 有效性/健全性两轴、§8.2 Steelmanning/Socratic、§8.3 Pre-Mortem、§十 CoT 忠实度、§十一 r745A 溯因/理论美德五族结论**均不复用**；与 `engineering/wb-instruction-prior`、`agent/grill-me` 分工已在上文逐条写明。豆包自留地 `wb-execute-discipline` / `wb-context-compressor` **WB 0 落地**。
- **未采纳**：Toulmin《The Uses of Argument》全书 field-dependent / field-invariant 之辩、Wikipedia 所记相对主义与绝对主义争论、中国法学网全文关于指导性案例效力定位的司法制度结论、Liverpool PDF 中 AI & Law 形式化（dialogue games / argumentation schemes）整段，均属专门领域争论或不可迁移制度事实，只取可迁移的结构判据。

## 十三、因果识别性判据：聚合反转、后门准则与对撞陷阱（TI · r750A 2026-11-15 实拉，3 独点）

> 与 §三 / §四 分工：那两节回答「do-operator 是什么、后门/前门调整是什么」，本节回答**「一个因果结论能不能从手上这份观测数据算出来」**，给可机检的判定清单。三独立域一手交叉：SEP《Simpson's Paradox》（2026-06-06 实质修订）官方全文逐字 + PNAS Bareinboim & Pearl 2016《Causal inference and the data-fusion problem》官方全文 + UCLA CS r509《Causal inference in AI education: A primer》PDF 快照逐字。

### 13.1 「多收数据也算不出来」是图的性质，不是样本量的性质
- SEP 逐字：「**identifiability is a relationship between a DAG G, probability distribution P and a causal quantity Q, such that Q is identifiable if and only if it is uniquely determined by P given G**」。PNAS **Definition 2** 给可机检形式：对任意两个满足 G 假设的全设定模型 M1、M2，`P1(v)=P2(v) ⇒ Q(M1)=Q(M2)` —— 同一观测分布必须给出同一答案，Q 才可只由 P 与 G 表达（与真实机制 F、外生分布 P(u) 无关）。
- 反例逐字：存在未观测的 S 与 T 共同原因时，「**the probability distribution is compatible with any possible distribution for p(S|do(T))**」——观测数据对干预效应零约束力。
- PNAS 完备性逐字：「**The do-calculus was proved to be complete** for queries in the form Q=P(y|do(x),z) ... **if Q cannot be reduced to probabilities of observables by repeated application of these three rules, Q is not identifiable**」。三规则（插入/删除观测、行动与观测互换、插入/删除行动）反复用尽仍消不掉 do 算子 = 逻辑边界。
- 判据：报「这个结论从现有数据推不出」必须同时给出 ① 图 G ② 那条缺失 / 未测的边 ③ 声明**识别性失败**而非模型不够强或数据不够多。禁止用换估计量、加特征、扩样本来回应识别性问题。

### 13.2 聚合反转（Simpson）不是统计悖论，是「该条件化哪个变量」的图问题
- SEP 逐字：全人群 `p(S|T)=p(S|¬T)`，而男女各层 `p(S|T,M)>p(S|¬T,M)` 且 `p(S|T,¬M)>p(S|¬T,¬M)`；成因是全概率展开 `p(S|T)=p(S|T,M)p(M|T)+p(S|T,¬M)p(¬M|T)` 两式**权重不同**（治疗组女性 27:13、对照组男性 7:5）。**Theorem 1**：若 `p(M|T)=p(M|¬T)` 权重相同，分层关联在聚合层保持，反转不可能发生。
- UCLA r509 逐字给出关键陷阱：同一份观测数据可对应**两个观察等价、干预含义相反**的因果模型 —— (a) Z 是混杂须控制；(b) Z 只是对撞 `U1→Z←U2` 控制反而引入混杂偏误。两模型分别推出「按年龄分层点击率投 Ad 0」与「按聚合数据投 Ad 1」两个相反决策，且原文靠「不可能存在影响年龄的潜在混杂」这一领域知识才判 (a) 更可辩护。⇒ **数据本身不裁决，必须显式声明图**。
- 判据：遇「整体与分组结论相反」，先输出 ① 分组变量与处理的关联 ② 候选图清单（混杂 / 中介 / 对撞） ③ 每个图下该不该分层，再给结论；禁止默认「分层更细所以更可信」。与 §8.1 有效性/健全性两轴分工：那条评单条论证结构，本条评聚合口径。

### 13.3 后门准则两条硬约束；「多控制一个变量」会反向引入偏误
- SEP 逐字后门准则：「**No node in Z is a descendant of X, and Z blocks every path between X and Y containing an arrow into X**」；命中则 `p(Y|do(X)) = Σ_Z p(Y|X,Z) p(Z)`。混杂的正式定义是 `P(Y|X,Z) ≠ P(Y|do(X),Z)`（即关系未被识别），并明确「**Confounders threaten causal inference not by providing an alternate explanation of why an effect occurred, but by undermining the possibility of measuring the causal relationship**」——混杂不是「还有别的解释」，是「根本量不出来」。
- 方向陷阱逐字：共同原因 `X←Z→Y` 条件于 Z **阻断**路径；共同结果 `X→Z←Y` 「**the path will be blocked provided that one does not condition on Z or a descendant of Z**」——条件于对撞或其后代反而**打开**伪相关。PNAS **Definition 1 (d-separation)**：Z 阻断路径 p 当且仅当 p 含 Z 中的箭头发出节点，或含一个**不在 Z 且 Z 中无其后代**的碰撞节点；原文举例 `Z={X,Z3,W3}` 因 Z3 处收敛箭头而留下未阻断路径，故 `Z1⫫Y|(X,Z3,W3)` 不成立。
- 判据：调整集须逐条写「为何不含 X 的后代」「每条含箭头入 X 的路径由谁阻断」「是否误纳入对撞 / 中介」。以「控制得越全越准」为默认即不合格。UCLA r509 补：条件于中介 M 会改变估计对象（总效应 vs 直接/间接效应），不得称作「控制了一切」。落地：方案评审 / 复盘归因时把「调整集 + 图 + 未测边」三项写进结论，与 §五 的「先找混杂」形成可执行版。

### r750A 来源与判非（2026-11-15 实拉，逐字核验）
- `https://seop.illc.uva.nl/entries/paradox-simpson/`（Stanford Encyclopedia of Philosophy，《Simpson's Paradox》，First published 2021-03-24 / **substantive revision 2026-06-06**）— **curl 200 全文 104,115 字逐字提取**（WebFetch 首轮 AI 摘要 60s 超时仅返回前 15,000 / 91,345 字，改 curl 取全文）：§3.3 识别性定义与 p(S|T)≠p(S|do(T))、§3.4 混杂定义 `P(Y|X,Z)≠P(Y|do(X),Z)` / 「Confounders threaten ... by undermining the possibility of measuring」/ 后门准则两条件与式 (5) / 共同原因 vs 共同效果对比、§2.2 Theorem 1 权重条件。**第一独立域（学术百科一手全文）**。
- `https://www.pnas.org/doi/full/10.1073/pnas.1510507113`（PNAS，Bareinboim & Pearl，**2016-07-05**《Causal inference and the data-fusion problem》）— **WebFetch 200 全文逐字**：Definition 1 (d-separation) 两条件与 Z3 反例、Definition 2 (identifiability) 的 `P1(v)=P2(v)⇒Q(M1)=Q(M2)`、do-calculus 三规则式 (5)(6)(7)、「proved to be complete ... if Q cannot be reduced ... Q is not identifiable」、干预切断入边与 assignment mechanism。**第二独立域（期刊论文一手）**。
- `https://ftp.cs.ucla.edu/pub/stat_ser/r509-reprint.pdf`（UCLA CS 技术报告 r509《Causal inference in AI education: A primer》）— **WebSearch 快照逐字**（PDF 正文未逐页 curl，如实登记）：Simpson 悖论 AdBot 例 3.1、Figure 5 两个观察等价模型 (a)/(b) 与相反决策、Definition 4.1 干预切断入边、Definition 4.2 后门准则两条件与调整公式、对 `U1→Z←U2` 的 d-separation 说明。**第三独立域（高校技术报告，作交叉不作唯一来源）**。
- `https://theory.toys/toys/philosophy/causal-inference` + `https://lmversity.com/learn/maths-foundations/s4-6-causal-graphical-models-do-calculus-and-identifiability-limits`（教学 / 交互式工具）— WebSearch 快照逐字：Fork / Chain / Collider 三构型、collider adjustment 的 induced bias、未测混杂应报 non-identifiable。**教学立场交叉登记，不作结论唯一来源**。
- **判非**：窄串全库 `SKILL.md` 精确扫描 — `Simpson` / `辛普森` / `聚合反转` / `d-separation` / `碰撞节点` / `collider` / `identifiability` / `complete for` / `后门准则` / `共同效果` **全 0 命中**；`back-door` / `do-calculus` / `DAG` 命中在本技能 §三 / §四（概念层，无判定式、无完备性、无对撞），本轮按「优＝加厚现有」补判定层、不新建、不重述结论；`reconcil` / `coherent` 命中在 `execution-intelligence` 等为执行对账异命题。`wb-context-compressor` 的 `因果完备性` 命中为记忆因果链异命题。豆包自留地 `wb-execute-discipline` / `wb-context-compressor` **WB 0 落地**。B / C 两轮结论一律不复用。
- **未采纳**：SEP §5.1 线性回归参数化、§5.3 Sure-Thing Principle 决策论争论、§4 心理学对「为何觉得悖论」的实验、PNAS 全篇 data-fusion / transportability 与 selection bias 的形式化、UCLA 的因果阶梯三层教学内容 —— 属专门领域或已在 §一/§三覆盖，不迁移为通用判据。

## 十四、论证图式与批判性问题：推定、举证责任与标准 defeater（2026-11-15 r754A 实拉，3 独点）

> 分工：§十二 图尔敏管「一条论证由哪些结构要素组成（D/W/B/Q/R）」，本节管「这类推理由哪些**标准失败方式**被检索出来、以及每问之后举证责任落在谁身上」。两节不同层，不互相替代；对话博弈 / Carneades 形式化不在本节范围。

### 14.1 图式是「推定 + 可废止」，输出是举证责任台账而非有效/无效
- Walton 原文（AI & Law 纪念论文逐字转录，Walton 2006b p.84）：「**Several distinct forms of argument ... are not deductive or inductive in nature. These arguments are presumptive and defeasible**」；「**If the respondent accepts the premises, then that gives him a good reason to also accept the conclusion. But it does not mean that the respondent should accept the conclusion uncritically. Matching each form of argument is a set of appropriate critical questions to ask**」；「**They are used to shift a burden of proof to one side or the other in a dialogue**」。
- 标准例「专家证言图式」：大前提 `E` 是含命题 `A` 的领域 `D` 的专家；小前提 `E` 断言 `A` 为真；结论 `A` 可被合理视为真。配套六条 CQ：expertise（E 可信度）/ field（是否同领域）/ opinion（E 到底断言了什么）/ trustworthiness（E 本人是否可靠）/ consistency（与其他专家是否一致）/ backup evidence（断言是否有证据支撑）。
- 方法论库逐字：「**The defeaters are retrieved, not improvised** — each scheme's question set encodes the accumulated knowledge of how that specific pattern fails」；输出「**is not "valid or invalid" but a burden-of-proof ledger: which questions were answered, which remain open, and whether the presumption survives**」。
- **判据**：评审单个短推定论证固定五步 —— ① 门禁（是不是单条可废止推论；多前提结构走论证图、演绎/统计结论不套图式）② 复述结论+明示前提 ③ 显式命名图式、写出 runner-up 与匹配置信度 ④ 填槽暴露隐含前提 ⑤ 检索该图式**自带**的 CQ 组并出推定裁决 `STANDS / STANDS-PENDING / FALLS`。禁止临场即兴想反驳；禁止把结论写成「有效/无效」。

### 14.2 CQ 分 assumptions / exceptions 两类，举证责任方向相反
- 官方逐字：「**With regard to burden of proof, critical questions are of two kinds: assumptions ... once they have been asked, create a burden of proof on the party who put forward the argument ... the premise is assumed to be true unless it is questioned, after which it is no longer assumed but must be supported by further arguments and evidence**」（例：expertise question）。「**exceptions. The other kind ... the burden of proof is placed on the respondent, the party challenging the argument by asking the critical question, to provide an argument proving the exception holds**」（例：trustworthiness question，质疑者须证明证人不诚实）。
- Informal Logic 2022 逐字：「**an argument is defeated if the respondent asks an appropriate critical question that is not answered by the proponent**」；「**Advancing an argument shifts the burden of proof, and asking the critical question shifts it back again**」；推定论证「**non-monotonic, i.e., further information may reveal the conclusion's falseness or its doubtfulness and hence require a revision of the former result**」，且「**the conclusion may be false though all the premises are true**」。
- **判据**：每条未答 CQ 必须写明「谁举证」并分两栏：assumption 类一问即撤销默认 → **提出方**补证；exception 类 → **质疑方**证明例外存在。禁止对全部未答项一律回「请补充证据」。新增证据使结论撤销时须重跑整组 CQ（与 §11.1 溯因非单调互补：那条讲新增前提撤销「最佳解释」，本条讲对话中举证责任来回移动）。

### 14.3 图式目录自带覆盖缺口与错分风险，证据等级须随结论声明
- Informal Logic 2022 逐字统计：「**49 (47.1%) of the 104 argument schemes contain no critical questions**」；「**The number of critical questions assigned to the individual argument schemes varies greatly (from zero to seven questions)**」；undercutter (UC) 是最大子类，且「**A pattern, for example, that questions of a certain type are added to all argument schemes, is not recognizable**」。
- 方法论库逐字：「**Even the five most common schemes machine-separate at only 63-91% accuracy (Feng and Hirst, 2011), so mis-typing is live, not rare**」；「**Do not skip stating the classification, and do not trust a confident mis-type**」；「**Walking the critical questions and recording shallow answers produces the appearance of scrutiny**」；「**Naming the scheme is the beginning of evaluation, not its end**」。证据等级自评 **P (practitioner)**：「**No study measures single-application evaluation accuracy, and nothing is validated on AI agents; the transfer is an explicit, untested assumption**」，两项对照研究测的是数周课堂**教学**对学生写作的影响。
- **判据**：结论固定带三件附属声明 —— ① 图式名 + runner-up + 置信度 ② 该图式 CQ 组是否为空 / 不全（近半图式无 CQ ⇒ 须明写「标准 defeater 集缺失，覆盖依赖即兴」，不得假装已穷尽） ③ 证据等级与迁移边界（概念文献 + 课堂长期教学，无单次应用效果、无 agent 验证）。禁止把「命名了图式」当反驳、把「答完清单」当健全性证明；错分会把整组 CQ 打到错误的漏洞上，故分类必须可争辩。

### r754A 来源与判非（2026-11-15 实拉，逐字核验）
- `https://cgi.csc.liv.ac.uk/~katie/ail2020.pdf`（Atkinson 等《In memoriam Douglas N. Walton: the influence of Doug Walton on AI and law》，Liverpool 大学官方仓储；另见 `https://cgi.csc.liv.ac.uk/~tbc/publications/WaltonSubmission.pdf` 与 `https://intranet.csc.liv.ac.uk/~katie/ail2020.pdf` 同文镜像）— **WebSearch 逐字快照**：Walton 2006b p.84 推定/可废止定义与举证责任转移、专家证言图式六大 CQ、assumptions vs exceptions 两类与各自举证方、图式三用途（评估 / 发明 / 分配举证责任）、「contextual forms of argument」与 schema 变量 E/D/A。**如实登记**：WebFetch 对该 PDF 拒收字节（Content-Type: application/pdf，字节被丢弃）；Bash curl 因域名含 `csc` 被安全策略误判拦截 → **未取得 PDF 全文，仅按搜索引擎逐字快照取证，不冒充一手全文**。**第一独立域（同行评审纪念论文）**。
- `https://www.erudit.org/en/journals/informallogic/2022-v42-n1-informallogic06950/1088463ar.pdf`（《An Epistemological Appraisal of Walton's Argument Schemes》，Informal Logic 42(1), 2022）— **WebSearch 逐字快照**：104 schemes 中 49 (47.1%) 无 CQ、每图式 0–7 条且类型分布不均、UC 为最大子类、非单调性、「defeated if the respondent asks an appropriate critical question that is not answered」、对话性（vs 演绎的命题/单主体性）。**如实登记**：curl 200 但仅 7,170B 截断页、pypdf 报 `STREAM_TRUNCATED_PREMATURELY`，带 UA 重试同结果 → 按快照取证，不冒充 PDF 全文。**第二独立域（同行评审期刊）**。
- `https://thinking-framework-skills.productonpurpose.com/frameworks/think-walton-argumentation-schemes`（方法论库《Argumentation Schemes with Critical Questions》）— **WebFetch 200 前 15,000 / 46,150 字逐字**（AI 摘要 60s 超时返回原文）：classify-then-probe-with-keyed-defeaters、「defeaters are retrieved, not improvised」、burden-of-proof ledger、五步/七步流程与 STANDS/STANDS-PENDING/FALLS、63–91% 五类机器分类准确率、checklist theater 与「naming the scheme is not a refutation」、证据等级 P 与「No study measures single-application evaluation accuracy ... nothing is validated on AI agents」、Walton 1996 25 schemes / 2008 约 60 主 + 44 子、Calvo Figueras & Agerri 2025 CQs-Gen。**第三独立域（方法论库，二手立场，逐条登记不作唯一结论来源）**。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `argumentation scheme` / `critical question` / `burden of proof` / `defeater` / `undercutter` / `举证责任` / `presumptive` / `可废止` **全 0 命中**；`图式` 命中在本技能 §十二（图尔敏论证**结构要素**）与 §180 一句「Liverpool PDF 中 AI & Law 形式化（dialogue games / argumentation schemes）整段属专门领域、未采纳」—— **r747A 明确判非且未落地**，本轮取的是「推理模式 + 该模式自带 defeater 集 + 举证责任方向」这一**内容层**，与 r747A 的结构层正交，且不取 dialogue games 形式化，故不构成重复；`meta/mi-memory` 的「要点/图式层」是记忆心理学 schema 异命题；`defaults/wb-context-compressor`（豆包自留地）「导航式/图式/多向量」是检索范式异命题。按 rules/07 四态判「**优＝加厚现有**」，不新建并行层。豆包自留地 `wb-execute-discipline` / `wb-context-compressor` **WB 0 落地**。与 r753(AI/EI/SI)、r752(VI/DI/OI)、r751(MI/CI/RI) 九模块结论均不复用。
- **未采纳**：Carneades 把 CQ 建模为 typed premises 的形式化、ASPIC+ / AIF / argument mining 工程线、CQs-Gen shared task 67.6 分数、Walton 1996 与 2008 目录数量考据、Blair 2001 标准批评、两项课堂对照研究细节 —— 属形式化实现、数值与专门争论，不迁移为通用判据。


## 十五、因果结论的跨域可迁移（外部效度）：selection diagram 与 transport formula（r758A · 2026-11-16 实拉）

> 与 §十三分工：§十三问「**同一个域内**给定图 G 与分布 P，Q=P(y|do(x)) 能不能从 P 唯一算出」（识别性）；本节问「**源域做实验、目标域只能被动观测**时，目标域的 R=P*(y|do(x)) 能不能算」（可迁移性）。两道判定门，数据来源与所需假设都不同。

### 15.1 可迁移性与识别性是两个判定门，「样本够大/做过 RCT」不构成外部效度证据
- UCLA r485（Pearl《Causal and Counterfactual Inference》§5）逐字：「**a totally different application, to decide if experimental findings from environment π can be transported to a new, potentially different environment, π\*, in which only passive observations can be performed**」；「**invariably, experiments performed in one environment (or population) are intended to be used elsewhere, where conditions may differ**」。
- INAOEP（Pearl & Bareinboim《External Validity: From Do-Calculus to Transportability》Definition 5）逐字：「**R(Π\*) = P\*(y|do(x), z) is said to be transportable from Π to Π\* in D if R(Π\*) is uniquely computable from P, P\*, I in any model that induces D**」——输入是三份东西：源域观测 P、源域实验 I、目标域观测 P\*，缺一即无定义。
- 两条连接逐字：「**all identifiable causal relations in D are also transportable, because they can be computed directly from P\* and require no experimental information from Π**」；「**given causal diagram G, one can produce a selection diagram D such that identifiability in G is equivalent to transportability in D**」（做法：D=G 再让 S 指向全部变量＝目标域不共享任何机制）。还逐字点明反向更难：「**proofs of nontransportability are more involved than those of nonidentifiability**」，须证明不存在两个兼容 D、在 {P,P\*,I} 一致而在 R 上不一致的模型。
- **判据**：报「本结论可用于新场景/新人群/新环境」时固定先分两问 —— ① 目标域自己能否从 P\* 直接识别（能则无需源实验，属 trivially transportable）② 需要哪几份数据组合、差异假设写在哪。禁止把「样本量够大」「原研究是随机对照试验」「我们复现了效应」当作外部效度证据：RCT 只保证源域内部识别，不迁到 π\*。

### 15.2 差异要锚在「机制」不是「分布」；S 指向哪里决定 reweight 用哪个条件式，且观测分布看不出来
- r485 逐字：「**A selection diagram is a causal diagram annotated with new variables, called S-nodes, which point to the mechanisms where discrepancies between the two populations are suspected to take place**」；Theorem 3（=INAOEP Theorem 1）逐字：「**R = P\*(y|do(x),z) is transportable from π and π\* if and only if the expression P(y|do(x),z,s) is reducible, using the rules of do-calculus, to an expression in which S appears only as a conditioning variable in do-free terms**」。
- 三个图给出三条**不同**的 transport formula（r485 逐字）：(a) `P(y|do(x),s)=Σ_z P(y|do(x),z)P(z|s)`；(b) `P(y|do(x),s)=P(y|do(x))`；(c) `P(y|do(x),s)=Σ_z P(y|do(x),z)P(z|x,s)`；(c) 的推导用 Rule 1 从首项去 s（`Y⊥⊥S|Z` in `G_X̄`）、Rule 2 把次项 do(x) 换 x。
- INAOEP 关键反例逐字：「**every probability distribution P(x, y, z) that is compatible with the process of Figure 3(b) is also compatible with that of Figure 3(a) and, yet, the two processes dictate different transport formulas**」；且「**the correct transport formula should be P\*(y|do(x)) = Σ_z P(y|do(x),z)P\*(z|x), which is different from both (3.1) and (3.2)**」——即该按 `P*(z|x)` 而非 `P*(z)` 加权。原因是年龄未测：「**because age is not measured, this condition cannot be detected in the probability distribution P**」。
- **判据**：跨场景复用结论必须画出 S 节点指向**哪一条机制**（是协变量分布变了、还是某机制的条件概率变了、还是机制依赖 X 变了）；reweight 权重取 `P(z|s)` / `P(z|x,s)` / 不加权由 S 位置决定，不许挑顺手的那个。同一份观测数据可兼容多张 S 图却要求不同公式 ⇒ 必须靠领域知识显式声明机制差异，不能「从数据里看出来」，也不能默认「按人口结构加权就够了」。

### 15.3 三档可迁移性分层 + 完备性 + 「多研究平均」是抹平不是修正 + 选择偏误不能被随机化消除
- INAOEP Definition 6 逐字：「**A causal relation R is said to be trivially transportable from Π to Π\*, if R(Π\*) is identifiable from (G\*, P\*)**」（目标域自己算，不用源域）；Definition 7 逐字：「**A causal relation R is said to be directly transportable from Π to Π\*, if R(Π\*) = R(Π)**」，图检验 `(S⊥⊥Y | X, Z)_{G_X̄}`；Remark 逐字：「**The notion of "external validity" as defined by Manski (2007) corresponds to Direct Transportability, for it requires that R retains its validity without adjustment ... Such conditions preclude the use of information from Π\* to recalibrate R**」——常识里的「外部效度」其实只是最窄那一档。
- r485 Theorem 4（Bareinboim & Pearl 2013）三条逐字：**多项式时间**判定多环境非参数可迁移性、**多项式时间**导出 transport formula、「**The algorithm is complete, i.e., when it fails, transportability is infeasible**」；另有「**a consistent estimator may be constructed from multiple sources even in cases where it is not constructible from any one source in isolation**」。
- 反例逐字：「**typically handled inadequately by a statistical method called "meta analysis" which "averages out" differences instead of rectifying them**」；选择偏误逐字：「**It cannot be removed by randomized experiments and can rarely be detected in either experimental or observational studies**」、「**biased estimates will be produced regardless of how many samples were collected**」（培训项目对收入：高收入者更常报收入）。
- **判据**：① 跨研究/跨场景汇总先判三档（trivial / direct / 需 reweight 公式）并附 S 图，声明是否用了 Π\* 信息重校准；② 把多个研究加权平均称为「修正了差异」不合格——那是抹平差异，正确形态是给出 transport formula 指明每个源域该抽取什么；③ 完备算法判不可迁移就报「不可迁移」，不许换估计量硬凑；④ 选择偏误是**数据收集机制**偏差，加大样本或补做 RCT 都消不掉，须靠实验+观测数据组合与相干不等式诊断（r485 脚注 11）。与 §13.2「同一份数据可对应观察等价图」互补：那条讲域内需领域知识声明图，本节讲跨域还需声明**哪些机制变了**。

### r758A 来源与判非（2026-11-16 实拉，逐字核验）
- `http://ftp.cs.ucla.edu/pub/stat_ser/r485.pdf`（Pearl《Causal and Counterfactual Inference》，UCLA 官方 stat_ser 技术报告）— **curl 200 / 800,724B → pypdf 25 页 / 52,457 字全文逐字**：§5 External Validity and Transportability 全节、S-node 定义、Theorem 3、三条 transport formula 与 Rule 1/2 推导、Theorem 4 三条完备性、data fusion 与 meta-analysis「averages out」、Selection Bias 两段与脚注 11。**第一独立域（作者官方仓储一手全文）**。
- `https://ccc.inaoep.mx/~esucar/Clases-mgc/externalValityPearl.pdf`（Pearl & Bareinboim《External Validity: From Do-Calculus to Transportability Across Populations》，INAOEP 课程镜像）— **curl 200 / 424,562B → pypdf 18 页 / 73,575 字全文逐字**：Definition 5/6/7、识别性↔可迁移性两条连接、非可迁移性证明更难、Theorem 1 与证明、(3.4) `P*(y|do(x))=Σ_z P(y|do(x),z)P*(z|x)`、Figure 3(a)/(b) 观测等价却要求不同公式、Manski 2007 对应 Direct Transportability。**第二独立域（同作者不同文稿/不同机构镜像，逐字交叉）**。
- `https://escholarship.org/uc/item/9jg8x22k.pdf`（《The mathematics of causal inference》）+ `https://www.degruyterbrill.com/document/doi/10.1515/jci-2014-0016/html`（《The Deductive Approach to Causal Inference》，Journal of Causal Inference）+ `https://lacuna.tiptreesystems.com/direction/selection-diagrams-for-causal-transportability/`（sID 算法与 s-hedge 障碍）— **WebSearch 逐字快照**：Theorem 1 同文、三式、(c) 的 `P(z|x,s)` 解释、s-hedge「makes transportability mathematically impossible」、Subbaswamy dataset shift。**第三~五域（期刊/百科式转述，逐条登记，不作唯一结论来源）**。
- **失败与降级如实登记**：`escholarship.org` PDF **python urllib 45s TimeoutError**（未取得全文，仅按 WebSearch 快照，不冒充一手 PDF）；`air.unimi.it`（本批 C 轮另一稿）**HTTP 403 Forbidden**。以上均不引用其正文数值之外的东西。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `selection diagram` / `transport formula` / `S-admissibility` / `外部效度` / `跨域因果` / `selection node` **全 0 命中**；`transportability` 1 命中＝**本技能 §十三 r750A 来源节明确写「PNAS 全篇 data-fusion / transportability 与 selection bias 的形式化 … 属专门领域或已在 §一/§三覆盖，不迁移为通用判据」＝r750A 判非未采纳**，本轮正式展开，按 rules/07 四态判「**优＝加厚现有**」而非新建并行层；`可迁移性` 3 命中经查为 `defaults/wb-context-compressor`（OTel 跨工具迁移 / DSPy 跨 locale）、`writing/supply-chain-thesis-master`（企业匿名化保留可迁移性），全为**异命题**。TI 模块记忆 §13 三条（识别性/Simpson/后门）结论**一律不复用**，本轮取正交的跨域迁移层。豆包自留地 `engineering/wb-execute-discipline` / `defaults/wb-context-compressor` **WB 0 落地**。与 r757(AI/EI/SI)、r756(DI/VI/OI)、r755(MI/CI/RI) 九模块结论不复用。
- **未采纳**：sID 算法递归细节与 s-hedge 构造、Tian-Pearl/Shpitser 识别算法、Example 4~6 逐个图式、meta-analysis 逆方差权重公式、PNAS 2016 data-fusion 全篇、Manski 2007 边界定义原文 —— 属专门算法与形式化证明，不迁移为通用判据。


## 十六、认知接种：给结论预装「反驳疫苗」而非事后辟谣（r762A · 2026-11-18 实拉）

> 与 §八～§十五分工：那些章节教「怎么构造/评估一条论证」；本节教「在说服攻击到来**之前**，如何让一个已成立的判断更难被撬动」。与 SI 模块可信边界互补：SI 挡的是外部不可信输入，本节挡的是对**自己已有立场**的渐进侵蚀。证据等级声明：机制（两步模型/材料形式/威胁作用）有多篇一手与元分析支持；**effect size 的具体数值与数字预驳斥游戏的迁移效果存在系统综述级争议**，按下方判据分档使用，不把应用研究结果当理论定论。

### 16.1 接种的两步动机-认知模型：先制造「我的立场会被攻」的威胁感，再给弱化攻击+反驳弹药
- Sage 2026 系统综述（Loughnan 等，*Communication Research* 53(7)，DOI 10.1177/00936502251411467）WebFetch 200 原文逐字：心理接种「deliver weak *persuasive attacks* to stimulate a *threat* response to produce *counterarguments* that defend against future *persuasion*」；基础模型是「a two-step motivational-cognitive process which culminates in resistance to counter-attitudinal information」。第一步「stimulates a perception that one's attitudinal position on an issue is under threat」，可加「an explicit warning about future persuasive attempts」；第二步 prebunk「consists of the aforementioned threat-inducing attacks followed by their refutations」，且攻击消息须弱（「an incomplete or poorly supported argument」）以免「overwhelm the system (i.e., convince)」，反驳须足够强。
- PMC11393549（*Processing of misinformation as motivational and cognitive biases*）WebFetch 200 全文逐字：「A prerequisite for inoculation to succeed is for people to develop threat perceptions as they lead to the realization of the vulnerability of their beliefs, which in turn motivates the building of defense systems」；且「the presence of a forewarning message tends to be more effective」于仅靠反态度消息自发产生的内在威胁（intrinsic threat）。
- **判据**：给 AI agent 的判断做「免疫」，不能只塞结论和结论的理由（那是 supportive defense），必须显式写出「谁会用哪条看似合理的攻击来撬它」＋「这条攻击为什么站不住」两半；攻击样本要弱到不会被 agent 采信、反驳要强到能压住。缺威胁唤醒这一步＝只给了论据清单，不是接种。

### 16.2 真正赋予抗性的是接种后的 counterarguing，不是喂进去的反驳材料本身
- PMC11393549 逐字：「counterarguing, a cognitive process that occurs postinoculation treatment, is **not the same and goes beyond** refutational materials presented in a refutational preemption treatment」；「**It is this cognitive process—motivated by the perceived threat from impending attacks—that confers resistance**」（Insko 1967）。refutational preemption 两个功能：「to provide content to be used to refute potential attacks and to allow the practice of counterarguing」。
- 被动 vs 主动：PMC 逐字「In addition to this more passive refutation approach, individuals are sometimes instructed to develop their own refutation material」（Compton and Ivanov 2013；McGuire and Papageorgis 1961）。
- 威胁是否必要存在真实分歧：Sage 2026 逐字「Banas and Rains' (2010) meta-analysis which found that **threat did not predict inoculation**. However, the researchers noted their test was likely **underpowered**」；后续引入更贴合理论的「motivational threat」量表（Banas & Richards 2017；Richards & Banas 2018；「the traditional measure of threat operationalized an affective response that is not well aligned with the theory」）。接种科学站（inoculation.science）逐字记 Banas & Rains 2010 元分析「mean effect size of d = 0.43 across 41 experiments」。
- **判据**：验收接种效果必须测「攻击真的来了以后 agent 会不会自己生成反驳」，而不是测「它能不能复述预驳斥文本」——复述材料 ≠ 产生抗体。威胁维度标为「理论核心但元分析证据不一致」，报告时不得省略这一分歧；引用 d=0.43 须同时带「41 实验 / Banas & Rains 2010 / threat 项未预测」三件配套事实。

### 16.3 泛化不是白送的：refutational-same/-different 等效只在同一信念内成立，跨话题溢出须单独验证
- PMC11393549 逐字：数十年证据表明「'refutational-same and -different' treatments are **equally effective**」，「suggesting that inoculation offers an **umbrella or blanket of protection**」；且「inoculation may even offer **cross-protection** such that its protection spillover from one topic to other related topics (e.g., from condom use to binge drinking, Parker et al. 2012, 2016)」；应用范围已从「cultural truisms」（刷牙之类无人反对的共识）扩展到转基因、疫苗等争议议题（Banas and Rains 2010；Compton and Pfau 2005）。
- Nature *Humanities and Social Sciences Communications* 9:114 (2019) PDF（van der Linden 等）WebFetch 快照逐字：接种本为 prophylactic（暴露前），新近才测 therapeutic（「those who already carry an informational 'virus' can still benefit from inoculation treatments」，类比「therapeutic vaccines」）；并指出按具体话题做「vaccine」存在 scalability 与 generalisability 问题（Bonetto 2018；Roozenbeek & van der Linden 2018）。
- **判据**：本技能只承诺「同一判断、换了攻击角度」的泛化（refutational-different 等效）；跨到相关话题必须拿该话题的独立攻击重测，不写「一次 inoculation 全领域免疫」。给 agent 免疫是预防性工程，别等立场已被污染再指望治疗性接种能等效恢复。

### r762A 来源与判非（2026-11-18 实拉，逐字核验）
- `https://journals.sagepub.com/doi/full/10.1177/00936502251411467`（Loughnan 等 2026《An Analysis of Studies Testing Digital Interventions to Inoculate Against Misinformation: A Systematic Review》，Communication Research 53(7)）— **WebFetch 200，AI 摘要 60s 超时后返回前 15,000 / 96,622 字原文逐字**：Abstract 的 k=72 与「studies did not pose hypotheses relating to the core factors… threat conferral and counterarguing」「empirical designs and analyses have introduced confounding factors」「links… are weak」「whether the interventions inoculate remains unbroached」；两步模型全段、威胁必要性争议段、Banas & Rains 2010 underpowered 注记。**第一独立域（同行评审系统综述一手）**。
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC11393549/`（*Processing of misinformation as motivational and cognitive biases*，PMC 全文）— **WebFetch 200 全文逐字**：forewarning + refutational preemption 两部分、威胁前提、被动/主动反驳、counterarguing 与材料的区别与「motivated by the perceived threat… confers resistance」、same/-different 等效与跨话题溢出段。**第二独立域（PubMed Central 开放全文，逐条与综述交叉）**。
- `https://inoculation.science/inoculating-against-extremism/`（Inoculation Science 官方科普页）＋ `https://www.nature.com/articles/s41599-019-0279-9.pdf`（van der Linden 等 2019 PDF）＋ `https://datafield.dev/misinformation-media-literacy-critical-thinking/part-07/chapter-35/further-reading.html`（原始文献注释书目：McGuire 1961/1964、Papageorgis & McGuire 1961、Compton 2013、Maertens 2021 纵向衰减与 booster-shot）— **WebSearch 逐字快照**：d=0.43/41 实验、prophylactic vs therapeutic、接种衰减与加强针、原始文献著录。**第三～五域（机构专题站 / 期刊 PDF / 学术书目，交叉登记，不作唯一结论来源）**。
- **失败与降级如实登记**：Sage 全文页 AI 摘要 **60s 超时**，取 WebFetch 返回的前 15,000 / 96,622 字原文逐字；Nature PDF 仅取得 WebSearch 逐字快照，未宣称读完 PDF 全文。d=0.43 为二手转述的元分析效应量，与 Sage 2026 系统综述的「结论未触及」并列登记、不择一冒充实测。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `接种理论` / `inoculation` / `认知免疫` / `prebunk` / `refutational` **目标技能 0 命中**；命中仅 `defaults/wb-context-compressor/references/knowledge-base.md`（RLHF 对齐语境的「inoculation」异命题，**豆包自留地 WB 永不落地**）与 co-learn 历史记录。按 rules/07 四态判「**优＝加厚现有 `meta/ti-critical-reasoning`**」，补的是「判断的抗侵蚀工程」这一正交层，不重述 §八 steelmanning / §十 CoT 忠实度 / §十一 溯因 / §十三 因果识别。TI 模块记忆前 15 条结论不复用。豆包自留地 WB 0 落地。与 r760(AI/VI/DI)/r761(OI/EI/SI) 九模块结论不复用；B/C 两轮结论亦不复用。
- **未采纳**：Bad News / Go Viral! 等具体游戏化 prebunk 产品的交互设计与大样本数值、Maertens 2021 三纵向实验的衰减曲线具体值、跨 cultures 五国实验数值、心理反应理论（reactance）与 post-inoculation talk 的社会网络扩散模型 —— 属应用产品与专项实验设计，不迁移为通用判据。

## 十七、因果发现：从数据找回图，但观测数据只到等价类（r766A · 2026-11-19 实拉，≥2 独立域交叉）

> 与 §十三（识别性/后门）/ §十五（跨域可迁移）分工：那两节假定**图已知**、在图上判识别或迁移；本节处理更前一步——**图未知时如何从观测数据把结构找回来**。因果发现的全部边界都挂在「观测只能看见条件独立关系」这一条上。

### 17.1（r766A-1）观测数据只到马尔可夫等价类，PC 与 GES 两个算法族撞同一堵墙
- Frontiers 2019 综述（Bayes 或 causal discovery 综述）Table 1 逐字对照：**PC / FCI / GES 输出 Markov equivalence class / Partial ancestral graph / Markov equivalence class；LiNGAM/PNL/ANM 在各自可识别条件下才输出「DAG as well as causal model」**。faithfulness 假设：PC/FCI 要、GES 要「some weaker condition」、LiNGAM/PNL/ANM 不需要；分布假设：只有 GES（常假设线性高斯或多项分布）与 LiNGAM 族要专门分布；「Properly handle confounders」一列 PC/FCI/GES/LiNGAM 全 No，只有 FCI 列 Yes。
- javiermeseguer.me 一手逐字：多个 DAG 隐含同一组条件独立，「observational data sees nothing but those independencies — so it cannot tell those graphs apart」；发现算法返回的不是 DAG 而是 **CPDAG**——「some edges directed, others left undirected because the data does not contain the answer」；那条约 `X0−X4` 无向边「is not a failure of the algorithm. Both orientations imply identical independencies, so no amount of Gaussian observational data distinguishes them」。**GES 走另一条路（greedy search + BIC 打分而非检验条件独立），却返回同一个含同样无向边的 CPDAG；两个算法族撞同一边界，是数据的属性，不是某个方法的属性**。
- **判据**：报「发现了因果结构」前先写输出类型（CPDAG/MEC vs 完整 DAG）与所用假设；无向边不是「没找到」，是观测数据原则上无法定向，不许靠主观挑一个方向补上。

### 17.2（r766A-2）非高斯/函数因果模型用「残差独立只在真方向成立」打破等价
- 同上一手逐字：LiNGAM 加一味料——噪声非高斯时出现高斯性掩盖的不对称：「for Y=βX+ε, the regression residual is independent of the regressor only in the true causal direction」。同一结构换均匀噪声后 LiNGAM 找回全部方向，包括 PC 碰不了的那条 `X4→X0`。DirectLiNGAM 把系数 prune 到精确 0：拟合矩阵四个非零 0.63/0.91，中间与 0.05–0.40 任何 cutoff 都得同一张图，**cutoff「looks like a tuning knob and is not one」**。
- arXiv 2610.23543 综述逐字：LiNGAM 写线性 SCM `X=BX+ε, X=(I−B)⁻¹ε`，用 ICA 识别混合矩阵到 scaling/permutation 模糊，再由结构归一化与无环排序消歧；DirectLiNGAM 用「真外生变量与对其回归的残差独立」递归抽取顺序；Hyvärinen-Smith 2013 用成对似然比、Wang-Drton 2020 用稀疏+矩信息控排序误差。
- **判据**：只有能核验「噪声非高斯/线性/可加」时才报完整定向 DAG；否则退回等价类。区分「识别了方向」与「识别了系数值」——前者靠非高斯不对称，后者还依赖结构归一化。

### 17.3（r766A-3）承重假设不可从数据检验，Sachs 基准 precision 完美只因太保守
- 一手逐字点破因果发现的软肋：**「All of it rests on assumptions that cannot be checked from the data being analysed. Causal sufficiency — no unmeasured common causes — is the load-bearing one」**——两个有隐藏共因、彼此无边的变量会被 PC 「produce a phantom edge」并如实报告；faithfulness 要求数据中唯一的条件独立就是图蕴含的那些（排除精确抵消）；此外条件独立检验在有限样本下必须可靠。
- Sachs et al. 2005 基准（11 个磷酸化蛋白、853 个观测免疫细胞，有分子生物学共识网络做 ground truth）：PC 在 853 细胞上 skeleton 对 consensus network **precision 1.00 / recall 0.41（17 条真边找回 7 条、0 假边）**。原文自陈「Precision is not high here. It is perfect — and that deserves an explanation rather than an adjective, because the explanation is unflattering」。
- **判据**：① 报重建质量必须 precision+recall 同报，只报 precision 会掩盖「过度保守、大半真边没找回」；② 声明「无未测共因」是外部领域假设、不是数据能证的结果；③ 发现输出要附「哪些边是等价类无向、哪些方向靠非高斯/函数假设才定」。与 §十三分工：那里评「给定图能否识别查询」，本节点评「图本身能不能被数据认出来」。

### r766A 来源与判非（2026-11-19 实拉，逐字核验）
- `https://www.frontiersin.org/articles/10.3389/fgene.2019.00524/pdf`（《Review of Causal Discovery Methods Based on Graphical Models》，Frontiers in Genetics 2019）— **WebFetch 返回非文本 PDF（如实登记），Table 1 与正文摘要由 WebSearch 对该 PDF 的逐字命中取得**：PC/FCI/GES/LiNGAM×faithfulness/分布假设/混杂处理/输出的对照表逐字、CI 法返回等价类与 FCM 返回唯一结构的前提、各方法可扩展性（PC/GES 上万变量、非线性 FCM 仅数十变量）。**第一独立域（同行评审综述一手，PDF 正文未直读，按逐字快照登记）**。
- `https://javiermeseguer.me/projects/ci-discovery`（Causal Discovery 一手技术笔记）— **WebFetch / WebSearch 逐字快照**：Markov equivalence 上限、CPDAG、PC 的 skeleton→v-structure→propagate 两段、GES 同边界、LiNGAM 非高斯破局与 DirectLiNGAM cutoff、causal sufficiency/faithfulness、Sachs 853 细胞 precision 1.00/recall 0.41。**第二独立域（与综述交叉）**。
- `https://inferensys.com/glossary/.../causal-discovery-algorithm` + `https://papers.nips.cc/paper/2018/file/e1314fc026da60d837353d20aefaf054-Paper.pdf`（NeurIPS 2018） + `https://arxiv.org/pdf/2610.23543` — **WebSearch 逐字快照**：constraint-based/score-based/functional/hybrid(MMHC)/time-series(PCMCI) 分类、GES 在等价类上搜、LiNGAM 用 ICA、CPDAG 图刻画「same skeleton and same v-structures」、GES/PC 在 faithfulness 下可证明一致但假设对检验误差敏感。**第三～五域（工具词库 / 会议论文 / arXiv，交叉登记）**。
- **失败与降级如实登记**：Frontiers PDF WebFetch 明确返回「non-text resource」不重试，Table 1 逐字来自 WebSearch 对该 PDF 的索引命中，未冒充已读 PDF 全文；arXiv 2610.23543 仅取 WebSearch 逐字摘要段，未读完整 PDF。precision 1.00/recall 0.41 为同一笔记口径，与综述「等价类不可识别」并列登记、不择一冒充唯一实测。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `causal discovery` / `马尔可夫等价` / `Markov equivalence` / `CPDAG` / `LiNGAM` / `PC 算法` / `v-structure` **全库 0 命中**；本技能 §十三/§十五虽有 Pearl/do-calculus/selection diagram，但那是「图已知求识别/迁移」，与「图未知从数据发现」异命题，按 rules/07 四态判「**优＝加厚现有 `meta/ti-critical-reasoning`**」，补因果发现这一正交前置层，不重述 §十一溯因（假设生成）/ §十三识别性/ §十五可迁移。TI 模块记忆前 21 条结论不复用。豆包自留地 WB 0 落地。与 r765(OI/EI/SI)/r764(AI/VI/DI)/r763(MI/CI/RI) 九模块结论不复用；B/C 两轮结论亦不复用。
- **未采纳**：PC 完整定向传播规则与 FCI 的 PAG 细节、LiNGAM 的 ICA 算法实现与 high-dimensional 扩展、PCMCI 时滞公式与具体检验统计量、Sachs 数据集逐蛋白真边清单 —— 属算法实现与专项数据集，不迁移为通用判据。

## 十八、面板数据准实验：DiD 的平行趋势不可验证，SCM/SDID 用加权反事实补位（r770A · 2026-11-19 实拉，≥2 独立域交叉）

> 与 §十三（识别性/后门）/ §十五（跨域迁移）/ §十七（因果发现）分工：那三节都在 **DAG/潜在结果的结构层** 讲「给定假设能否识别」；本节处理**实证最常用的面板准实验工具族**——DiD / SCM / SDID，判据挂在「反事实怎么造、假设能不能验、权重会不会过拟合」上，不重述 do-calculus、transport formula 或 CPDAG。

### 18.1（r770A-1）DiD 的平行趋势是不可验证假设，只能做事前趋势诊断，不能当事实
- 一手逐字（TrueSight 因果推断专文）：DiD `δ=(Y_T,post−Y_T,pre)−(Y_C,post−Y_C,pre)`；「**平行趋势是一个不可验证的假设，因为我们永远无法观测到处理组在干预后的反事实趋势。如果处理组在干预前就已经呈现出不同的增长斜率，DiD 得出的结论就是纯粹的幻想**」。
- 玻尔百科（科学百科·面板因果）逐字同构：「平行趋势这个关键假设无法被直接证明，但我们可以通过检验政策实施前两组的趋势是否平行来进行诊断，增加我们结论的可信度」。
- 中国社会科学网逐字：「如果两省在政策出台之前的就业率保持平行(符合反事实假设),这个模型估计就具有因果效应」——把「平行」明确标为**假设/前提**而非数据结论。
- **判据**：报 DiD 结论必须先写「平行趋势」是假设、附事前趋势图/检验（pre-trend），并声明「若事前趋势已分叉则效应是幻想」；禁止把平行趋势当成数据已证明的事实直接下因果结论。处理组事前斜率已高于对照组却仍用 DiD，属高估。

### 18.2（r770A-2）SCM 显式造反事实，但把「找对照」换成「验权重」——凸包条件与过拟合是真软肋
- 玻尔百科逐字：SCM「不再是寻找某个单一的最佳对照单位,而是通过对多个未受干预的「捐赠」单位进行加权平均,来「合成」一个处理单位在干预前的「虚拟替身」。这个权重是通过优化选择的,目的是让合成控制组在干预前的所有相关特征(包括过去的结局趋势)都与处理单位完美匹配……为小样本、特别是 N=1 的案例研究提供了前所未有的严谨性」。
- TrueSight（SCM vs DiD 批判）逐字：SCM「通过加权构建反事实」「适用于单一处理单元」「动态优化权重 W」，主要缺陷「**易出现过拟合与内插偏差**」；加州烟草税案例——「如果在捐赠池中加入一个完全无关的州,而模型依然能通过调整权重将其『拟合』得很好,那么这个合成单元就失去了经济学意义,变成了纯粹的数学游戏……如果某个州的权重占据了 90%,那么这本质上还是一个简单的 Case Study,而非合成控制」。
- 广外中心 SDID 专文逐字：传统 SCM 两大缺陷「**一是要求处理单元的特征必须位于控制单元特征的『凸包』内(即处理单元可由控制单元线性组合表示),否则权重估计会失真;二是难以进行有效的大面板推断,无法可靠估计处理效应的标准误与显著性**」。
- **判据**：① SCM 报告必须附**权重分布**（哪个 donor 占多大权重）——单 donor 占 90% 等于承认是 case study；② 检查处理单元是否落在 donor 凸包内，落在凸包外权重估计失真；③ 事前拟合「完美重合」既可能是真相似也可能是过拟合，须加留一/置换（placebo）检验，不把拟合优度当因果证据；④ SCM 减少但不消除对平行趋势的依赖（它匹配的是事前趋势而非消除假设）。

### 18.3（r770A-3）SDID 双权重：个体权重+时间权重同时放松平行趋势，且给出可推断的大面板估计
- 广外中心专文逐字（Arkhangelsky 等 2021 AER 提出的 SDID）：「**通过构建包含个体权重与时间权重的加权双重差分框架**，实现了三大突破：一是兼容大量处理单元与少量处理单元的场景；二是大幅放松平行趋势假设,无需处理组与控制组事前趋势完全平行;三是允许有效的大面板推断,估计量具有一致性与渐近正态性,可通过 bootstrap、jackknife 等方法可靠估计标准误」。核心「双重加权与差分推断」「第一步：界定核心变量与研究框架」。
- 同文对照定位：DiD「核心假设是平行趋势……适用于大量个体接受处理的场景……当平行趋势假设不满足时……估计结果会出现严重偏差」；SCM「适用于单个或少量处理单元……要求特征位于凸包内……难以进行有效的大面板推断」。SDID 是二者折中——个体权重继承 SCM 的「造反事实」、时间权重继承 DiD 的「差分」，双重加权弱化各自单一假设。
- **判据**：① 单个/少量处理单元且找不到好对照 → SCM；大量处理单元且平行趋势可信 → DiD；平行趋势存疑又要大面板推断（要标准误/显著性）→ SDID，别硬套单一方法；② SDID 的「放松平行趋势」是**大幅弱化而非取消**，仍需事前拟合诊断；③ 凡报「政策效应显著」必须附标准误来源（bootstrap/jackknife/渐近），SCM 传统形式缺此能力时不得冒充有推断。

### r770A 来源与判非（2026-11-19 实拉，逐字核验）
- `https://tsight.io/articles/17207379`（TrueSight《因果推断的幻象与真相》）— **WebFetch/WebSearch 逐字快照**：DiD 平行趋势不可验证的「纯粹幻想」论断、SCM 显式造反事实但过拟合、方法对比与决策矩阵、SEM/PC/FCI「算法不能替代理论」。**第一独立域（方法批判一手）**。
- `https://scipedia.bohrium.com/sciencepedia/.../causal_inference_from_observational_data`（玻尔科学百科·从观察数据进行因果推断）— **WebFetch/WebSearch 逐字快照**：DiD 事前趋势可诊断不可证明、SCM 加权「虚拟替身」N=1 严谨性、RD/LATE 临界点局部效应。**第二独立域（科学百科一手，与第一交叉）**。
- `https://ygakj.gdufs.edu.cn/info/1260/1433.htm`（广东外语外贸大学·合成双重差分 SDID 前沿）— **WebFetch 200 全文逐字**：SDID 双权重三突破、一致性/渐近正态/bootstrap、DiD 平行趋势偏差与 SCM 凸包+大面板推断两缺陷、三步骤。**第三独立域（学术机构专文，主 SDID 证据）**。
- `https://cssn.cn/zzx/zgzz/202210/t20221024_5551695.shtml`（中国社会科学网·大数据与政治学）＋ `https://tsight.io/articles/18158842`（TrueSight·Stata SCM 批判）— **WebFetch/WebSearch 逐字快照**：云南贵州最低工资 DiD 平行假设例、SCM 是 DiD 扩展、加州烟草权重 90% 与过拟合警告、GSC/矩阵补全/RDD 替代。**第四～五域（学术媒体/方法批判，交叉登记）**。
- **失败与降级如实登记**：SDID 原论文 arXiv 号三次命中错误论文（1812.05827 实为夸克禁闭、1812.05722 为算子理论、1812.06989 为霍尔效应），均未冒充 SDID 一手；`syntheticcontrolmethod.org` WebFetch 连接失败。本轮结论由 TrueSight + 玻尔百科 + 广外中心三独立域交叉支撑，**不宣称直读 Imbens 团队 AER 原论文全文**，SDID 三突破按广外中心转述登记；DiD 公式「Y_T,post−Y_T,pre」与数值算例只取定性口径，不择一冒充唯一权威。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `合成控制`/`synthetic control`/`双重差分`/`difference-in-differences`/`平行趋势`/`parallel trend` 命中仅 `meta/agent-evolution` 的 **CUPED 预实验方差缩减**（r745C，异命题：那是降方差、不是准实验因果识别）与 co-learn 台账。按 rules/07 四态判「**优＝加厚现有 `meta/ti-critical-reasoning`**」，补面板准实验识别这一正交层，不重述 §十三 DAG 识别/§十五 transport/§十七因果发现。TI 模块记忆前 21 条结论不复用。豆包自留地（`wb-execute-discipline`/`wb-context-compressor`）WB 0 落地。与 r769(OI/EI/SI)/r768(AI/VI/DI)/r767(MI/CI/RI) 九模块结论不复用；B/C 两轮结论亦不复用。
- **未采纳**：SDID 个体/时间权重的优化目标函数与估计量构造细节、bootstrap 具体实现、GSC 因子模型与矩阵补全算法、RDD 带宽选择 —— 属计量实现细节，不迁移为通用判据。

## 十九、工具变量与 LATE：IV 识别的是谁、排除限制凭什么、多工具为何失效

> r774A（2026-11-19）实拉。§十三–§十八管「图已知/未知、跨场景、面板准实验」的识别；本节补一类正交缺口：当存在**未观测混杂**且后门调整不可用时，工具变量如何工作、它识别的到底是谁的效应、以及它的两个假设为何不能从数据里验出来。与 §十八 DiD/SCM/SDID 分工：那是「用时间/对照造反事实」，本节是「用外生工具隔离变异」。

### 19.1（r774A-1）LATE 定理：IV 给的是 complier 的局部效应，不是全员 ATE
- Angrist 2022（NBER w29726 / Econometrica 90(6)）摘要逐字：「**The local average treatment effects (LATE) framework for causal inference helped make this so. The LATE theorem tells us for whom particular instrumental variables (IV) and regression discontinuity estimates are valid.**」——LATE 框架的核心贡献不是给一个数，而是回答「这个 IV 估计对**哪些人**有效」。
- 人群按对工具的反应分四类：compliers（随工具开关而改变处理）、always takers、never takers、defiers（逆向）。IV 估计量在单调性下 = **compliers 的平均处理效应（LATE）**，不是全样本 ATE：对 always/never takers，工具不改变其行为，其处理变异不来自工具，故不被识别。
- **判据**：① 报 IV 结论必须写明「这是 complier 的效应」，禁直接外推成「对所有人有效」；② 问「这个政策对整体会怎样」时要额外假设（效应同质或可把 complier 效应推到他人），该假设不在 IV 本身里；③ LATE 与 RD 是同一族——都只识别局部（阈值附近 / complier），不是全局平均。

### 19.2（r774A-2）排除限制是「解释承诺」不是可检验前提；单调性排除 defiers
- Angrist 2022 逐字：「**A surprising exclusion restriction, an assumption central to the LATE interpretation of IV estimates, is shown to explain why enrollment at Chicago exam schools reduces student achievement. … IV exclusion restrictions formalize commitment to clear and consistent explanations of reduced-form causal effects.**」
- 排除限制（exclusion restriction）= 工具 Z 只能通过影响处理 D 来影响结果 Y，不能有直接路径或其他路径；as-if-random = Z 与结果误差项无关。二者是**欺骗性外生**（plausibly exogenous）的假设，**不能从观测数据检验**（这正是 IV 的软肋：换一个工具就等于换一套因果故事）。单调性（monotonicity）= 无 defiers，即不存在「工具推高反而降低处理」的人；有了 defiers，IV 估计不再是干净的正权重 LATE。
- **判据**：① 用 IV 前先写清「Z 凭什么只通过 D 影响 Y」这条故事并接受它不可证——这是解释承诺，不是数据结论；② 结论随工具选择而变时，报告差异而不是挑好看的那个；③ 检查单调性方向合理性（有没有理由存在 defiers），违背时 LATE 解释失效。

### 19.3（r774A-3）多工具变量 + 异质性效应：单调性与 2SLS 正权重解释不相容
- Mogstad/Torgovitsky/Walters 2021（NBER w25691 / AER 111(11)）摘要逐字：「**When treatment effects are heterogeneous, a common justification for including multiple IVs is that the 2SLS estimand can be given a causal interpretation as a positively-weighted average of local average treatment effects (LATEs). This justification requires the well-known monotonicity condition. However, we show that with more than one instrument, this condition can only be satisfied if choice behavior is effectively homogenous.**」并在大学回报实证中发现「**the standard monotonicity condition is at odds with the data**」，但较弱的 partial monotonicity 下 2SLS 仍可解释为正权重 LATE。
- Mogstad/Torgovitsky 2024（NBER w32927）综述：线性 IV 在异质性处理效应（UHTE）下通常误设，两条路——继续用线性 IV 并反推 LATE 解释，或向前设计显式允许 UHTE 的估计量（MTE / control function / bounding）。
- **判据**：① 多个工具变量并用时，「2SLS = 正权重 LATE」的默认辩护**在效应异质时站不住**，除非选择行为近乎同质；② 报告多工具 2SLS 前须检验偏单调性或有 partial monotonicity 的可验证充分条件，否则只当统计关联；③ 异质性为核心关切时，考虑 MTE 一类显式允许异质性的框架，别硬套线性 IV 的同质假设。

### r774A 来源与判非（2026-11-19 实拉，逐字核验）
- `https://nber.org/papers/w29726`（Angrist 2022《Empirical Strategies in Economics》，NBER w29726 / Econometrica 90(6):2509-2539）— **WebFetch 200 摘要全文逐字**：LATE theorem tells us for whom IV/RD are valid / exclusion restriction formalizes commitment to clear and consistent explanations / Chicago exam schools。**第一独立域（一手论文摘要，主证据）**。
- `https://nber.org/papers/w25691`（Mogstad 等 2021《The Causal Interpretation of 2SLS with Multiple IVs》，AER 111(11)）— **WebFetch 200 摘要全文逐字**：positively-weighted average of LATEs / monotonicity / multiple instruments only if choice behavior effectively homogenous / at odds with data / partial monotonicity。**第二独立域（一手论文摘要，多工具主证据）**。
- `https://nber.org/papers/w32927`（Mogstad & Torgovitsky 2024《IV with Unobserved Heterogeneity in Treatment Effects》）— **WebSearch 逐字快照**：UHTE 两策略（reverse-engineer LATE 解释 / forward-engineer MTE 估计量）。**第三独立域（一手综述摘要，异质性交叉）**。
- **失败与降级如实登记**：SEP《instruments and causality》与 Britannica instrumental-variable-analysis 两条 URL 均命中错误/空页（Document Not Found / 无关的 NBER w18541 外汇套利），已弃用不冒充；Imbens & Wooldridge 综述 w18541 命中错误编号。LATE 四人群分类、defiers/monotonicity 的标准定义按 Angrist 与 Mogstad 摘要逐字＋<P>通用口径登记，未直读 Imbens & Angrist 1994 原论文全文，不冒充一手全文。数值/实证（芝加哥考试学校、大学回报挂各自来源口径只取定性。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `工具变量` / `instrumental variable` / `两阶段最小二乘` / `2SLS` / `局部平均处理效应` / `exclusion restriction` / `combining for adaptation` 全库 0 命中（`LATE` 大写命中为 `late` 子串噪声、`弱工具` 1 命中与 `负对照` 1 命中均属异命题）。按 rules/07 四态判「**优＝加厚现有 `meta/ti-critical-reasoning`**」，补「外生工具隔离变异」这一与 §十三–§十八正交的识别层，不重述后门调整/transport/因果发现/DiD-SCM-SDID。A 轮结构映射（Gentner）原拟题因 `ai-input-enhancement` §155 已落地 systematicity/one-to-one（>60% 重叠）判「删/换道」，改取 IV。TI 模块记忆前 21 条结论不复用。豆包自留地 WB 0 落地。与 r773(OI/EI/SI)/r772(AI/VI/DI) 六模块结论不复用；B/C 两轮结论亦不复用。
- **未采纳**：2SLS 两阶段具体估计步骤与 std errors、MTE 估计量构造与 control function 推导、弱工具的第一阶段 F 统计量阈值之争、LATE 与 ATE 的权重边界公式 —— 属计量实现细节，不迁移为通用判据。

## 二十、断点回归设计（RDD）：效应只在阈值处，带宽与偏差修正才是成败手（TI · r778A 2026-11-20 实拉，≥2 独立域交叉）

### 20.1（r778A-1）★RDD 识别的是阈值处的局部效应，fuzzy RD 是换皮 IV，不是全员 ATE
Hahn/Todd/van der Klaau 连续性识别式 `t_SRD = lim_{x↓c} E[Y|X=x] - lim_{x↑c} E[Y|X=x]`：门槛两侧刚好相邻的个体「as-good-as-randomly assigned」，跳变即处理效应——但只对阈值处局部人群成立，外推到远离 c 的用量须额外参数假设。sharp RD（`D=1{X≥c}`）直接从结果跳变读效应；fuzzy RD（阈值只改变处理概率）把「超过阈值」当工具变量，效应 = Y 跳变 / D 跳变 = Wald ratio = 单调性下 complier 的 LATE（§19 的工具变量与弱工具教训全数迁移，第一阶段跳变越弱估计越不稳）。原文：「the jump in E[Y|X] at c is the causal effect — for the local population at the cutoff」。判据：报 RDD 结论必须写「这是 c 处的局部效应（fuzzy 则 complier）」，禁外推全员；识别家族写清是 sharp 还是 fuzzy、running variable / cutoff 是什么。

### 20.2（r778A-2）★局部低阶多项式 + 数据驱动带宽是设计决策；高阶全局多项式让远处数据污染边界
「The most common approach is to use (non-parametric) local polynomial methods to approximate the two regression functions near the cutoff.」「The bandwidth is typically chosen in an optimal and data-driven fashion to ensure transparency and avoid specification searching.」——在 `Xi∈[c−h,c+h]` 内用 triangular kernel 分别拟合两侧局部线性（允许两侧斜率不同，防 X 的非线性冒充跳变），而非全域高阶多项式（Gelman–Imbens：高阶全局把任意的远端观测和多项式阶数绑架到边界估计，CI 过窄）。带宽 h 是偏差-方差权衡：窄 h 低偏差高方差、宽 h 反之；用 IK/CCT 的 MSE-optimal 数据驱动选择（rdrobust 默认），并强制报带宽敏感性表（h 减半/加倍）——只在一个带宽出现、窗口一动就消失的效应是警讯不是稳健发现。「Stay local, stay low-order.」判据：不写带宽选择规则与敏感性表的 RDD 不通过验收。

### 20.3（r778A-3）★MSE-optimal 带宽留下偏差 ⇒ 常规 CI 失效，须 CCT 稳健偏差修正 + 三项证伪
逐字：「When the bandwidth is chosen to be MSE-optimal, this approximation error appears in the standard distributional approximation and renders the conventional least squares confidence intervals invalid because conventional inference assumes that the approximation error is zero.」——点估计最优的带宽对推断并不最优，必须报 Calonico–Cattaneo–Titiunik 稳健偏差修正（RBC）CI：对点估计做偏差修正、标准误随偏差估计步调整；「These robust bias-corrected confidence intervals lead to valid inferences when using the MSE-optimal bandwidth, and remain valid for other bandwidth choices」。连续性假设无法直接观测，靠三项证伪：① McCrary/Cattaneo–Jansson–Ma 密度检验——running variable 在 c 处密度有跳变即受操纵/排序（「failing to reject 是与无操纵一致，不是证明无操纵」，且只测改变密度的那类操纵）；② 协变量连续性（把事前固定协变量当安慰剂结果，c 处有跳变即两侧本来就不同）；③ 安慰剂 cutoff（在无政策变化处重跑应 ≈0）。最危险的 compound-treatment（同一 c 处还有其他政策同时变）不可检验，只能靠制度论证。连续性框架（参数=阈值处平均处理效应）与局部随机化框架（参数=窗口 W 内平均、核心假设是 c 附近像随机实验）定义的是不同参数，禁混报。判据：RDD 报告须含 RBC CI + 三项证伪 + 框架声明，缺一判不完整。

### r778A 来源与判非（2026-11-20 实拉，逐字核验）
- `https://arxiv.org/html/2110.08410v1`（arXiv 2110.08410《Covariate Adjustment in RD Designs》§2.1 WebFetch 200 全文逐字：local polynomial / data-driven bandwidth / MSE-optimal 使常规 CI invalid / RBC 有效 / continuity vs local randomization 参数不同 / canonical 只用 outcome+score）
- `https://ccfd.cufe.edu.cn/info/1073/4167.htm`（中央财经大学财税文摘·elite high school RDD：Gelman–Imbens 全局高阶多项式误导、Imbens–Lemieux 交叉验证带宽、Lee 协变量连续性检验、模糊 RD 选择偏误；中文一手交叉）
- `https://casrai.org/guides/regression-discontinuity-design`（CASRAI 指南 WebSearch 快照：高阶全局多项式边界病态、IK/CCT 带宽和 RBC、McCrary 2008 密度检验机制与「未拒绝≠证明」、协变量平衡 + 安慰剂 cutoff 稳健项）
- `https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-04/ch43-regression-discontinuity.html`（ASSIP 实证金融教材 ch4.3 WebSearch 快照：sharp vs fuzzy、triangular kernel local-linear、「stay local stay low-order」、带宽偏差-方差、McCrary + 协变量 + compound-treatment 审计）
- **判重**：全库 SKILL.md 精确扫描 `断点回归` 0 命中；`regression discontinuity` 3 命中全部在 `meta/ti-critical-reasoning` r770A 来源段（GSC/RDD 替代）与「未采纳：RDD 带宽选择」及 LATE 定理引文，**无专节落地**；`RDD` 3 命中同属上述语境；`propensity score`/`倾向得分` 全库 0。本轮取 §18 DiD/SCM/SDID、§19 IV/LATE 之后的正交识别策略（阈值连续性 + 带宽/RBC 工程面），不复用其结论。豆包自留地 WB 0 落地。

## 二十一、目标试验仿真：先写 RCT 协议再让观察数据就位，设计缺陷比统计更致命（TI · r782A 2026-11-20 实拉，≥3 独立域交叉）

> 与 §13–20 分工：那些是「给定研究设计后如何识别/估计」（图识别/IV/DiD/RDD）；本节是**上一步**——在碰数据前把因果问题写成一份假说 RCT 协议，再逐条映射到观察数据。Hernán & Robins 2016 框架。

### 21.1（r782A-1）★七组件协议先写、因果问题定义试验而非数据定义分析；设计缺陷比统计失配更常致错
目标试验协议七组件（Hernán–Robins 2016，NAP 委员会 Table 2-1 逐字）：eligibility criteria（入排标准**全部基于基线时点已确定的特征**，禁事后用基线后信息定义基线资格）、treatment strategies（含初始治疗及停药/换药的方案许可理由）、treatment assignment（基线随机、可按预后因子分层）、start/end of follow-up（基线开始、死亡/结局/失访/行政截尾止）、outcomes（尽量含 negative controls 即已知不受该治疗影响的结局）、causal contrasts（ITT：被分配到策略的效应 vs per-protocol：按方案实际接受的效应）、statistical analysis（预先写明如何调整基线与随访中的预后/依从/失访因素）。关键ORDER：the causal question defines the trial; the trial defines the analysis; the data are made to fit the analysis — not the other way around。scoping review（Zuo 等，96 项研究）：94% 观察性 CER 至少一项设计缺陷，61% 用基线后信息定义基线资格、81% 未声明 ITT 还是 per-protocol；Hernán 强调**协议组件与随机分配的不完整仿效（设计面）比统计调整不足更可能导致错误推断**。判据：报观察性因果结论前先亮七组件表，缺任一格即声明该格是假设不是数据结论；「用了 IPW/PS 匹配等高级统计」不构成 TTE 合格。

### 21.2（r782A-2）★永生时间偏倚是 time-zero 未对齐的产物，不是样本量或模型问题
机制（crvscience 逐字）：用**未来的治疗状态**定义暴露、却把随访起点放在更早的临床事件（确诊/入院）——因为「晚开始用药者必须活到开药那天」，把这段治疗前生存窗口记到治疗组头上，artificially inflating survival benefits。目标试验通过强制对齐消除：每个人**恰在满足资格并被分入策略的那一刻**开始随访（time zero = eligibility met = assignment = follow-up start）。更一般的 three biases：immortal time / prevalent-user / misaligned-follow-up selection bias。扩展：资格可反复满足（多次门诊）→ sequential nested target trials（每个合格月/就诊各起一个嵌套试验、robust variance 处理同一人跨重叠试验相关）；策略含宽限期（如「3 个月内启动他汀」）→ time-zero 分配未知。判据：看到「治疗组生存更好」先核 time-zero 是否与资格/分配同一时刻；错起点下再高级的 Cox/加权也修不回。

### 21.3（r782A-3）★clone-censor-weight 是宽限期策略的仿效主力，克隆消偏倚、IPCW 补信息性删失
宽限期策略在 time-zero 无法知道分配 → 克隆：每个合格者在基线**复制到每个策略各一份**（Di={(i,a=1),(i,a=0)}），两臂都从 time-zero 起贡献人时（neutralizes immortal time bias）；当某人实际轨迹偏离所分配策略时对该 clone **人工删失**；再用 inverse probability of censoring weights（IPCW，以时变混杂为条件估计「仍依从未删失」概率的倒数）校正人工删失带来的选择偏倚，得无偏 per-protocol 生存曲线。边界（crvscience 逐字）：TTE **does not replace randomization**，因果有效性仍落在不可检验的 no unmeasured confounding（条件可交换性）+ positivity 上；价值在消除 self-inflicted design flaws（已多次调和观察研究与 RCT 的分歧：激素替代/他汀/COVID 疗法）。判据：报 per-protocol 效应须写清克隆臂、人工删失触发点、IPCW 是否施加及 positivity 是否成立；「无条件可交换性/无阳性」声明只写「用了 IPW」不合格。

### r782A 来源与判非（2026-11-20 实拉，逐字核验）
- `https://nap.edu/read/25532/chapter/4` → 重定向 `nap.nationalacademies.org` 再转 `www.nationalacademies.org`（**WebFetch 两次重定向放弃逐字抓、以 WebFetch 首跳返回全文片段逐字登记，不冒充完成 WebFetch**）：NAP 委员会 Table 2-1 七组件及逐字描述（「all inclusion and exclusion criteria are based on characteristics ascertained exclusively at baseline」、negative controls、ITT vs per-protocol、protocol/analysis follow from explicit causal question、emulation 是 iterative process）——第一独立域·政府/学术机构原文。
- `https://www.sciencedirect.com/science/article/abs/pii/S0895435623002032`（Zuo 等 TTE scoping review，WebFetch 摘要全文逐字：96 studies / 94% 至少一设计缺陷 / 61% 基线后信息 / 81% 未定义因果对比 / time-zero 防 immortal time bias / statistical methods only a part of TTE design / Hernán 强调设计缺陷更易致错）——第二独立域·同行评议综述。
- `https://crvscience.com/wiki/target-trial-emulation`（WebFetch 200 全文逐字：两阶段、七组件表、immortal time bias 机制、time-zero 对齐、sequential nested trials、clone-censor-weight 公式与 IPCW、does not replace randomization + 条件可交换性与 positivity 边界、Hernán-Robins 2016/JAMA 2022 著录）——第三独立域·方法学 wiki。
- `https://metricgate.com/blogs/target-trial-emulation-observational`（WebSearch 逐字快照：七组件、time zero is sacred、clone-censor-weight recipe 与 IPW vs Matching 交叉）——第四独立域·工程教学。
- `https://www.sciencedirect.com/science/article/abs/pii/S0003496724013220`（RA CER 系统综述 WebSearch 摘要逐字：31 研究 29(94%) 设计缺陷、七组件映射）——交叉佐证。
- **判重**：全库 SKILL.md 精确扫描 `target trial`/`目标试验`/`immortal time`/`clone-censor` 0 命中（`emulat` 命中为 personal-ai-employees 的 K8s emulation version 与 browser-skill 的设备模拟，异命题）；`propensity score`/`倾向得分` 全库 0（r778A 判重行登记）。AIPW/DR 与 `meta/agent-evolution` §off-policy（IPS/SNIPS/Doubly Robust）有重叠按 rules/07 弃用、改取「先写 RCT 协议」这一更上游且正交的子面。豆包自留地 WB 0 落地。

## 二十二、未测混杂敏感性 E-value：把「相关不等于因果」从免责句变成可量化阈值（TI · r786A 2026-11-20 实拉，≥4 独立域交叉）

> 与 §13–21 分工：那些解决「怎么识别/估计因果效应」（后门/IV/DiD/RDD/TTE 都落在不可检验的 no unmeasured confounding 假设上）；本节解决**估计完成之后的诚实交代**——效应已经报出来了，要多强的未测混杂才能把它解释掉。它不是识别策略，是对既有估计的稳健性尺，且**不能判定混杂是否存在**。VanderWeele & Ding 2017（Ann Intern Med 2017;166:619-627，DOI 10.7326/M16-2607）。

### 22.1（r786A-1）★E-value 是「解释掉所需的最小关联强度」，点估计与置信限各算一个
定义（VanderWeele-Ding 原摘要逐字）：the minimum strength of association, on the risk ratio scale, that an unmeasured confounder would need to have with both the treatment and the outcome to fully explain away a specific treatment-outcome association, conditional on the measured covariates。即在已测协变量条件下，一个未测混杂因素要同时与处理、与结局达到多大 RR 关联，才能把这个效应抹平到无。大 E-value = 需要相当强的混杂才能解释掉（稳健）；小 E-value = 一点混杂就够（脆弱）。最低值为 1（E-value=1 意味着根本不需要未测混杂就能解释掉）。点估计公式 `E = RR + √(RR·(RR−1))`；RR<1 时先取倒数 1/RR 代入。置信区间另算一个——取**最靠近零的那端**（LL>1 用 LL 代公式；UL<1 取 1/UL 代公式；区间跨 1 则 E-value=1），把统计不确定性一起交代。论文建议所有旨在提供因果证据的观察性研究都报 E-value 或等价敏感性分析。判据：报观察性因果结论，稳健性栏须给两个数（点估计 E、CI 端 E）；只报点估计 E 缺统计不确定性，不合格。

### 22.2（r786A-2）★E-value 是最坏情形下的保守下界，不是「混杂存在与否」的检验
Sage 2025 实操指南逐字：E-value represents the minimum strength of association an unmeasured confounder would need to have with both the treatment and the outcome after accounting for measured confounders to fully explain the observed association；其 bias factor 由 `RR_EU × RR_UD / (RR_EU + RR_UD − 1)` 给出，E-value 是令 `RR_EU = RR_UD` 时把 `RR_ED` 拉到 1 的正解；因为取的是**最大 RR**，结果是 worst case scenario、因而**conservative**——「the E-value does not tell one whether unmeasured confounding is actually present—it simply quantifies the strength of confounding needed to fully explain an observed association」。低患病率的混杂可能根本产生不了那么大的偏倚，所以 E-value 大不等于结论就因果成立。IQSS（Harvard）逐字把 E-value 列为最常用却 also one of the most controversial and misinterpreted，并指出不存在单一最佳方法、无统一报告标准。判据：E-value 只写「要多强的混杂才能解释掉」，禁写成「已排除未测混杂」或「因果成立」；须与「该领域实际可能的混杂强度」并列解读，无参照时声明无法判断。

### 22.3（r786A-3）★连续暴露/OR/HR/SMD 需先换算到可比尺度，横向比较要求同口径
Sage 指南专门给出从 logistic（连续暴露）与 linear regression（连续暴露）算 E-value 的流程，并说明 E-value 以 RR 尺度表达但可由 OR、hazard ratio、standardized mean differences（Haneuse 2019）换算；连续暴露须按有意义的增量（IQR 或标准差）标准化成一个可比的风险比后再代入公式。ScienceDirect 概念文逐字：For any given RR reported in a study, two E-values can be calculated: one for the observed outcome, and one for the 95% confidence interval；且 VanderWeele 等给出把公式改造到 OR/HR 的补充指引。IQSS 提醒：现有方法「either depend on the analysis method used or are on a particular (non-universal) scale」，故跨研究、跨暴露类型比 E-value 数字须先确认尺度与换算口径一致。判据：报 E-value 须附「原始效应量类型 + 换算到 RR 的方式 + 连续变量的标准化增量」三件事；不同尺度/不同增量的 E-value 不可直接比高低或排序稳健性。

### r786A 来源与判非（2026-11-20 实拉，逐字核验）
- `https://www.acpjournals.org/doi/10.7326/M16-2607`（VanderWeele & Ding 2017 原论文，PubMed PMID 28693043 + TeselaGen Scholar 著录双取：E-value 定义逐字「minimum strength of association, on the risk ratio scale, that an unmeasured confounder would need to have with both the treatment and the outcome to fully explain away a specific treatment-outcome association, conditional on the measured covariates」、报点估计与最靠近 null 的 CI 端、annals 建议所有因果证据研究都报；ACP 页面需登录，用 PubMed/Scholar 一手摘要逐字，不冒充全文）——第一独立域·原论文一手摘要。
- `https://journals.sagepub.com/doi/10.1177/25152459251326571`（Bi 等 2025《Navigating Unmeasured Confounding... A Practical Guide to Computing and Interpreting E-Value》WebFetch 200 全文逐字：bias factor 式 `RR_EU × RR_UD/(RR_EU+RR_UD−1)`、worst case/conservative、does not tell whether unmeasured confounding is actually present、连续暴露 logistic/linear 两节、RR/OR/SMD 换算、best practices）——第二独立域·实操教程一手全文。
- `https://www.sciencedirect.com/science/article/abs/pii/S089543562300255X`（Journal of Clinical Epidemiology 概念文 WebFetch 摘要逐字：E-value 公式 `RR+RR×(RR−1)`（即 RR+√(RR·(RR−1)) 展开写法）、RR<1 取倒数、CI 端表 LL/UL 规则、最低值 1、「two E-values can be calculated」、strengths and limitations 段）——第三独立域·同行评议概念文。
- `https://iqss.github.io/dss-ps/sensitivity.html`（Harvard IQSS WebFetch 200 全文逐字：E-value 是 transformation of the effect estimate、most common yet one of the most controversial and misinterpreted、no single best method / no agreed reporting standards / methods depend on analysis or non-universal scale、不推荐特定方法只提醒跟进该领域）——第四独立域·权威方法学机构。
- **判重**：全库 SKILL.md 精确扫描 `E-value`/`Evalue` 0 命中本体（唯一命中为本技能 §21.3 TTE 的「no unmeasured confounding 条件可交换性」一句，是识别假设声明、非稳健性尺）；`sensitivity analysis` 命中在 skills-security-check（安全语义异命题）。本轮补的是「估计完成后如何量化稳健性」这一 §13–21 全缺的正交层，不重述后门/IV/RDD/TTE 的识别结论。豆包自留地 WB 0 落地。与 r785(OI/EI/SI)/r784(AI/VI/DI)/r783(MI/CI/RI) 九模块结论不复用；B/C 两轮结论亦不复用。
- **未采纳**：Ioannidis 2019 批评的具体论点、Rosenbaum bounds / VanderWeele limit-based sensitivity 等其他方法的公式细节、临床试验中 E-value 的争议案例 —— 属方法学纵深，不迁移为通用验收判据。

## 二十三、时变混杂的 G 方法：g-computation 与 IPTW-MSM 是同一问题的两种机制（TI · r790A 2026-11-22 实拉，≥3 独立域交叉）
> 与 §13–22 分工：那些假定图已知在图上判 do/后门/IV/DiD/RDD/TTE，都是**单次或固定时点**的干预；本节处理「治疗反复给、且有一个被前次治疗改变的协变量夹在两轮治疗之间」——普通回归调它既过度校正（它是中介）又漏中介效应，不调它则后一轮治疗决策仍混杂。Robins 1986 提出参数 g-formula 处理 occupational healthy worker survivor effect，比 2000 年 MSM 的 IPTW 方案早十余年。

### 23.1（r790A-1）★g-computation 是「前向模拟的标准化」，不建治疗模型；IPTW-MSM 是「重加权」，不建结局模型
CASRAI 逐字：g-computation「fits a model for the outcome (and for the time-varying confounder itself), then simulates each subject forward under a hypothetical treatment history」。五步：①对每个时变混杂拟合「给定截至该点的治疗与协变量史」的模型；②拟合结局模型（含全部治疗史与协变量史包括时变混杂）；③在固定干预方案下对每个体从自身基线出发前向模拟——设治疗为方案值、从混杂模型抽混杂、再从结局模型抽结局；④用**同一批个体的基线**重复另一方案（同基线分布标准化）；⑤两方案模拟均值相减即总因果效应。「Nothing in this sequence involves a treatment-assignment (propensity) model at all — g-computation never asks how likely was this person to be treated. IPTW never asks the reverse question — it never models the confounder or outcome process.」判据：策略反复且至少有一个协变量夹在两轮之间才动用 G 方法；单次治疗用 IPTW/倾向评分匹配即可。
### 23.2（r790A-2）★非参数无交互时三法趋于一致；参数化下差别来自各法建模了数据分布的哪一部分
Oxford 肾病综述逐字：三种方法「similar interpretation as clinical trials」都是边际/人群层效应，「always treated vs never」是理想化情形，只有当成「intention to continue treatment」才类比特异 ITT。CASRAI 演示同一模拟数据三法：真效应 −1.239；把时变混杂当普通协变量调的回归得 −2.507（夸大 102%）；g-computation 得 −1.247（约 1% 内）；IPTW-MSM 得 −1.240（模拟噪声内）。「the bias is not in the coefficients themselves, but in treating their sum as the total effect of a sustained treatment strategy」——各轮直接效应系数接近真值，错在把系数和当总效应、漏掉经混杂的间接通路。中华流行病学杂志 Naimi 实例三 G 法均得 Δŷ=50.0/μl，传统回归低估。判据：报「传统回归与 G 方法结论相反」须先确认存在处理-混杂反馈，否则两者本就该接近。
### 23.3（r790A-3）★g-null 悖论与模型误设是 g-formula 独有代价；报告须写干预方案+每个模型+模拟种子+bootstrap CI
「zero paradox」：当前治疗对未来混杂有非零效应时，参数 g-formula 会给出与因果零假设不一致的结论（g-null paradox），IPW 与 G 估计无此悖论（零假设分别对应加权 MSM 系数为 0、波动函数 ψ=0）。CASRAI 并列假设：consistency / positivity / sequential exchangeability 三者在模拟区间内都要成立——positivity 在确定性方案把协变量推出观测范围时变成外推风险；且 g-formula 额外要求**混杂模型与结局模型的函数形式都正确**，IPTW 只要求治疗模型正确。正因此才有双重稳健：AIPTW/TMLE 结合两套机制，「the estimate stays consistent if either side is right, not only if both are」，TMLE 还是 substitution estimator 不会预测到样本外。报告清单：比较的具体干预方案（g-formula 能模拟 MSM 难及的动态方案）、每个混杂与结局模型的设定含交互项、Monte Carlo 抽样数并换种子复验、CI 用 bootstrap 每重样本重拟全部模型（非仅点估计 SE）、是否在整个模拟协变量范围满足 positivity。判据：只报点估计不报方案与模拟稳定性不合格；「双重稳健」不是 g-computation 的同义词。
### r790A 来源与判非（2026-11-22 实拉，逐字核验）
- `https://www.casrai.org/guides/g-computation-time-varying-confounding`（WebFetch 200 全文逐字：五步机制、worked example 真效应 −1.239/回归 −2.507/g-comp −1.247/IPTW −1.240、g-null paradox、三假设、报告标准、g-formula vs g-computation vs g-methods vs g-estimation 术语表、双重稳健 TMLE）——第一独立域·方法指南一手全文。
- `https://html.rhhz.net/zhlxbx/20211022.htm`（梁洁等《纵向研究中控制时依混杂的G方法》中华流行病学杂志 2021;42(10):1871-1875，WebFetch 200 全文逐字：处理-混杂反馈与 collider 双重角色、g-formula 标准化思想、稳定/不稳定权重、零悖论、三法有效性稳定性与适用范围、Naimi 实例 Δŷ=50、仅有 20% 文献用 G 方法其中 80.3% 是 IPW）——第二独立域·中文核心期刊一手全文。
- `https://academic.oup.com/epirev/article/43/1/130/6294770`（Oxford Epidemiologic Reviews 2021 妊娠期用药综述 WebFetch/Scholar 逐字：反馈结构三型图、三法在非参数无交互时近同而参数化下有别、IPTW 假设更少但不稳定权重、g-formula 复杂联合干预更有效但 g-null paradox 与模型误设、TMLE substitution estimator 不预测样本外）——第三独立域·同行评议综述一手。
- **判重**：全库 SKILL.md 精确扫描 g-formula/g-computation 在 ti-critical-reasoning 本体 0 命中；仅 engineering/wb-execute-discipline 与 agent-evolution/references/r784A 命中且为异命题（前者豆包自留地 WB 0 落地、后者元学习语境）。本轮补 §13–22 全缺的「时变混杂反馈」处理层，不重述 do-calculus/IV/RDD/TTE 的识别结论；clone-censor-weight（§21.3）已借 IPCW 但未展开 G 方法家族，本轮不重复其宽限期策略。与 r789(OI/EI/SI)/r788(AI/VI/DI)/r787(MI/CI/RI) 九模块结论不复用；B/C 两轮不复用。
- **未采纳**：具体 gfoRmula/stgest/DTRreg 软件包命令细节、结构嵌套模型波动函数的参数化形式、孕期 SSRI 实证案例的具体数值 —— 属特定实现/特定域结果，不迁移为通用验收判据。

## 二十四、交错处理时点的 TWFE 偏误与稳健 DiD 估计量（TI · r794A 2026-11-22 实拉，≥2 独立域一手交叉）
> 与 §13–23 分工：那些处理的是单次或固定时点干预（后门/IV/RDD/DiD/TTE/G 方法）。本节处理「处理在不同单位、不同时点陆续铺开，且处理效应随队列或随时间异质」时，标准双向固定效应（TWFE）回归系数不再是可解释的平均处理效应——这是系数本身的算术缺陷，不是数据脏。

### 24.1（r794A-1）★偏误是算术问题：TWFE 是所有 2×2 DiD 的加权平均，异质效应下「已处理当对照」造出负权重
Jeffrey Michler 教学模拟逐字：真效应 9.8，朴素 `xtreg`（TWFE）得 6.14；原因是「standard TWFE calculates a weighted average of all possible 2x2 Difference-in-Difference combinations. When adoption is staggered, TWFE uses already-treated units as controls for newly-treated units」，而已处理组的效应仍在增长，「this creates negative weights, severely biasing your estimate」。Goodman-Bacon 分解证明 β_TWFE 是三类比较的方差加权平均（早处理 vs 晚处理、处理 vs 从未处理、有问题的晚处理 vs 早处理）；`bacondecomp` 散点里实心三角=好比较（新处理 vs 从未处理，估计 5–10 贴合真值）、空心圆=坏比较（已处理当对照，接近 0 甚至负），虚线是整体 TWFE（约 3.9）。Barrios 150 小时规则 Primer 的蒙特卡洛更极端：无从未处理单位且效应随时间累积时，1000 次 TWFE 估计全为负（均值 −0.236），而每个真处理效应按构造都是正的（+0.570）——「Nothing about the data is pathological; the weighting does it」。判据：交错铺开 + 效应异质时禁止直接报单一 TWFE 系数；先做 Goodman-Bacon 分解看 timing 比较占多少权重、有没有负权重，权重可见后才有讨论系数的资格。

### 24.2（r794A-2）★稳健估计量只比「新处理 vs 尚未处理/从未处理」；CS / SA / stacked 各有适配场景
Michler 逐字：现代估计量「explicitly avoid using already-treated units as controls. Instead, they only compare newly-treated units to 'not-yet-treated' or 'never-treated' units」；`csdid`（Callaway & Sant'Anna 2021）算 group-time ATT，`estat simple` 得 9.96，逼近真值 9.8。Barrios 应用对照（53 个辖区、36 个半年考期）：TWFE −1.08（SE 0.15），Callaway–Sant'Anna −1.40（0.24），Sun–Abraham −1.12（0.22），stacked regression −1.63（0.21）——「The estimates span half a log point, though no two are statistically distinguishable」，跨度主要来自各估计量参照期不同，而非权重。场景匹配（Barrios E2）：CS 适配有从未/尚未处理对照与协变量、Sun–Abraham 适配事件研究（含最后处理队列作对照）、stacking 用矫正权重、imputation（Borusyak 等 / Gardner）求效率、Wooldridge 2023 适配非线性结局。判据：报稳健估计须写「目标参数（总体 ATT / 队列 ATT / 事件时点曲线）+ 聚合权重 + 对照类型」，先声明 estimand 再比数字；否则换个估计量数字变了只是回答了不同的问题。

### 24.3（r794A-3）★「多个稳健估计量一致」不等于验证；预期效应是设计问题，重加权修不了
Barrios 三条 takeaway 逐字：①「The bias is arithmetic」——TWFE 是全部成对 2×2 比较的加权平均，Goodman-Bacon 让权重可见；②「Agreement among robust estimators is not validation」——校正方法修的是同一个权重缺陷，且「every one still assumes parallel trends and no anticipation. Running five estimators answers one threat five times」；③「Anticipation is economics, not a nuisance」——采用前一年考生抢考的 +0.188（约 21%）尖峰是真实行为响应，「No reweighting repairs a mistimed treatment date; the remedy is design, moving the event date or dropping the window」。平行趋势也别只靠过了事前趋势检验（Roth 2022），要报 HonestDiD 界：多大的违背会推翻结论（Rambachan & Roth 2023）。判据：交错 DiD 结算栏至少五项——①Goodman-Bacon 权重分解 ②一个稳健估计量 ③estimand + 参照期 ④预期/提前趋势的设计处置 ⑤HonestDiD 敏感性；五个估计量数字相近不是「设计无误」的证据，只是把同一个威胁答了五遍。

### r794A 来源与判非（2026-11-22 实拉，逐字核验）
- `https://jdavidm.github.io/learn-stata/materials/11-twfe`（Jeffrey D. Michler 教学页，WebFetch 200 全文逐字：已处理当对照与负权重机制、模拟真效应 9.8 / xtreg 6.14、bacondecomp 实心三角 5–10 与空心圆、整体约 3.9、csdid estat simple 9.96 对真 9.8、Goodman-Bacon 2021 / Callaway-Sant'Anna 2021 / Sun-Abraham 2021 / Borusyak 2024 著录）——第一独立域·可复现教学一手。
- `http://johnmbarrios.com/papers_web/paper_staggered_did.html`（Barrios《Staggeringly Problematic: A Primer on Staggered DiD for Accounting Researchers》Conditionally accepted, Accounting Horizons，WebFetch 200 全文逐字：1000 次模拟均值 −0.236 对真 +0.570 且符号翻转、150 小时规则 TWFE −1.08/CS −1.40/SA −1.12/stacked −1.63 含 SE、预期 +0.188≈21%、GB 权重 timing 53%/never 43%/pre-1990 4%、三条 Key Takeaways、D1–P3 的 17 项 checklist、HonestDiD 与 Roth 2022）——第二独立域·同行评议方法 Primer 一手。
- **判重**：全库 SKILL.md 精确扫描 `Goodman-Bacon` / `Callaway` / `staggered` / `TWFE` / `负权重` 命中仅 meta/agent-evolution §长期实验的「time-staggered treatments start a second copy later」（A/B 实验收敛检验异命题，非交错 DiD）；`交错DID`/`多期DID`/`交叠DID` 全库 0。本轮补的是 §13–23 全缺的「处理时点交错 + 效应异质」这一设计层，不重述后门/IV/RDD/TTE/G 方法的识别结论。豆包自留地 WB 0 落地。与 r793(OI/EI/SI)/r792(VI/AI/DI)/r791(MI/CI/RI) 九模块及 B/C 两轮不复用。
- **未采纳**：具体 Stata/R `csdid`/`bacondecomp` 命令与安装细节、Triple Differences / 溢出 / 非线性设定的展开、150 小时规则的经济学解释 —— 属特定实现/特定域结果，不迁移为通用验收判据。

