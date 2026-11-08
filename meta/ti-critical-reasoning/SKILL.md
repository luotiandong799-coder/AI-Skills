---
name: ti-critical-reasoning
description: 因果推理与批判性思考（Thinking Intelligence）。当任务需要区分"相关"与"因果"、评估方案真实贡献、做反事实推演（"若当初换方案会怎样"）、识别 LLM 关联机误判因果时调用。基于 Pearl 因果阶梯、do-calculus、结构因果模型（SCM/DAG）、后门/前门调整。本技能是 TI 载体，补齐关联式推理的因果盲区。
version: 1.2.0
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
