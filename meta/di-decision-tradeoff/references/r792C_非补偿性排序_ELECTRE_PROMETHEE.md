# r792C 非补偿性排序（ELECTRE / PROMETHEE outranking）正文下沉

> 所属技能：`meta/di-decision-tradeoff`（DI 决策模块）。SKILL.md §二十六 留摘要，本文件存完整独点、逐字证据、判非与来源。
> 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点。

## 本章定位
§六 MCDA 加权、§r733B 补偿性/非补偿性结构、§r788C 多属性效用加性形式管「权重怎么定、效用值从哪来、能不能用加权和」；本章管一个被加权和掩盖的前置问题：**当某准则差到不可接受时，其他准则的优异能不能把它「补回来」**。价值测量法（SAW/MAVT/MAUT）默认能补偿；out ranking 法（法国学派 ELECTRE/PROMETHEE）默认不能。选方法 = 选补偿逻辑。

## 独点 1：out ranking 的默认假设是「决策者不愿/不能给准则间权衡」，用一个准则的极差不能被另一个的极好补偿
- 一手逐字（SINTEF 博士论文，WebSearch 全文片段）："In outranking methods, it is assumed that the DM is not able to/willing to define trade-offs between criteria. Accordingly, in these methods it cannot be assumed that a poor performance value in one criterion can be compensated by a sufficiently good performance values in another criterion, as in the value-measurement methods."
- 对比 SAW：Bradford 论文逐字 "SAW adopts a compensatory approach ... whilst PROMETHEE and ELECTRE adopt a no-compensation between criteria performance approach"；SAW 是 "linear additive method ... summing normalized criteria values within the decision matrix per alternative to generate an index value in the range 0 to 1"。
- 关键警告（SINTEF 逐字）："Choosing an MCDA method means choosing a **compensation logic**." 且多项实验显示 "choice of method might have a significant influence on the decision outcome ... might even matter as much or more than which person that are using the methods" ⇒ 报告「用加权和排出来了」必须声明采用补偿逻辑的理由，否则方法选择在悄悄替决策者表态。
- out排名 relation 的四态（Politecnico di Torino 论文逐字）：A S B 且非 B S A ⇒ A P B（严格偏好）；B S A 且非 A S B ⇒ 逆偏好；双向成立 ⇒ A I B（无差异）；双向都不成立 ⇒ A R B（**不可比 incomparable**）。不可比是一等输出，不强行拉成全序。

## 独点 2：ELECTRE 走 concordance + 非 discordance 双门槛、可能排不出唯一最优；PROMETHEE II 用净流给全序
- ELECTRE（法文 ELimination Et Choix Traduisant la REalité）：四态关系建模为「at least as good as」，成立需两条件（UPM 论文逐字）："Concordance states that … a sufficient majority of criteria have to be in favor of this assertion. Non-discordance states that in the cases when the concordance condition holds, none of the criteria should be strongly opposed." 且 "both concordance and non-discordance conditions have to hold true"；veto threshold 让某准则能否决「a outranks b」。ELECTRE III 用 indifference/strict preference/veto 阈值算 concordance/discordance/credibility 三指数，经 downward/upward distillation 合成中位 preorder。
- 关键差异（SINTEF 逐字）："The ELECTRE III method … is sometimes not able to find the 'best alternative'. However, it is often useful to apply … in the beginning of the decision process to produce a shortlist of the best alternatives." ⇒ ELECTRE 优先做**淘汰/短名单**，不承诺给唯一赢家。
- PROMETHEE（Brans）：每准则定 preference function `P_i(a,b)=F_i[d_i(a,b)] ∈ [0,1]`，`d_i(a,b)=g_i(a)−g_i(b)`，权重 Σw_i=1，聚合偏好指数 `π(a,b)=Σ P_i(a,b) w_i`（UPM 逐字）。正流 Φ⁺（a outranks  others 的程度，越高越好）、负流 Φ⁻（被 others outrank，越低越好）；PROMETHEE I 给偏序图、**PROMETHEE II 用净流 Φ=Φ⁺−Φ⁻ ∈ [−1,+1] 给完全排序**（Bradford 逐字）。文献给六种偏好函数类型（Usual/U-shape/V-shape/level/linear/Gaussian）。
- ⇒ 选型判据：要「短名单+允许不可比+ veto 保护」用 ELECTRE；要「一张从好到坏的全序表」用 PROMETHEE II；两者都不该与 SAW 混报而不声明补偿逻辑。

## 独点 3：选补偿逻辑后还要做敏感性分析——权重一变排序可能翻，方法选择的影响可能大过换决策者
- Politecnico di Torino 论文逐字："Sensitivity analysis may be performed … to assess the effects of uncertainty and subjectivity, usually associated with any decision process, by testing the consistency of MCDA results after a variation in the input parameters and/or in the decision-maker's preferences." 技术敏感性分析 "assesses which input data have a critical influence on the overall evaluation, i.e., whether a slight variation, for example, in a criterion weight can affect the MCDA results."
- 最常动的是准则权重，但也可动：方案得分、准则/方案数量、阈值（如 ELECTRE III 的 indifference/preference/veto）、其他技术参数。⇒ out ranking 的输出不是「排完就定」，须附「哪个输入微调会翻转排序」的敏感面清单。
- 代价与门槛（SINTEF 逐字）：out ranking "requires less precise input in terms of describing criteria and preferences … may correspond better to the way DMs really think. However, a major drawback is that many of the necessary inputs might feel non-intuitive for DMs, particularly the indifference and strict preference thresholds." ⇒ 用它的前置成本是向决策者 elicitation 出一套阈值（.indifference/preference/veto）， elicitation 做不到时方法再合适也落不了地。
- 与 §r788C 分工加一句：那里测「效用值本身从哪来（标准赌局/CE/权衡法）」，这里定「能不能用加权和这种补偿结构」；先把补偿逻辑定下来，再决定要不要费劲 elicitation 精确效用。

## 来源（r792C 独立实拉 2026-11-22，≥2 独立域一手交叉）
- `https://www.sintef.no/globalassets/project/seds/espen-loken_thesis.pdf`（SINTEF 博士论文《Multi-Criteria Planning of Local Energy Systems》，WebSearch 一手全文片段逐字）— out ranking 不补偿假设、ELECTRE/PROMETHEE 法国学派定位、"choosing a method means choosing a compensation logic"、方法选择影响可大过换人、ELECTRE III 短名单而非唯一最优、阈值非直觉的代价。**第一独立域·一手学位论文**。
- `https://oa.upm.es/44528/1/FILIP_RADULOVIC.pdf`（ Universidad Politécnica de Madrid 论文，WebSearch 一手全文片段逐字）— out ranking 四态关系 P/I/R/逆偏好、concordance + non-discordance 双条件、veto threshold、ELECTRE IV、PROMETHEE 偏好函数 `P_i=F_i[d_i]`、`π(a,b)=ΣP_i w_i`、Σw=1、六种偏好函数。**第二独立域·一手论文**。
- 交叉快照（WebSearch 逐字）：`https://bradscholars.brad.ac.uk/bitstream/10454/8533/4/JoCP_PAPER_unnumbered_FINAL_160616-1.pdf`（Bradford：SAW 补偿 vs PROMETHEE/ELECTRE3 不补偿、Φ⁺/Φ⁻/净流 Φ 定义、concordance/discordance/credibility 三指数、downward/upward distillation、13 种噪声屏障实证对比）· `https://iris.polito.it/retrieve/0950eb5e-d1c5-44c3-ad7d-351946acb01c/conv_phd_thesis_Vassoney_Erica_final.pdf`（Politecnico di Torino：三类方法分类、out ranking 四态 S/P/I/R、敏感性分析定义与可动参数清单）· `http://edok01.tib.uni-hannover.de/edoks/e01dh09/607614323.pdf`（Hannover：ELECTRE 不完全/PROMETHEE II 完全、concordance/discordance 矩阵构造、P+−P− 净流排序）。

## 判非 / 去重
`ELECTRE`/`PROMETHEE`/`outranking`/`非补偿性排序`/`concordance`/`discordance`/`净流` 全库 SKILL.md 本体 0（§r733B 有「补偿 vs 非补偿」的结构词但无方法体，§六 MCDA 加权是补偿法、§r788C 是效用 elicitation，均异命题）。与 §六 MCDA、§r733B 补偿结构、§r788C 效用 elicitation 逐条分工，不并存。豆包自留地 WB 0 落地。

## 未采纳
六种偏好函数的完整数学形式与选型规则、ELECTRE 各版本（I/II/III/IV/IS）的演化细节、credibility 指数的具体计算公式、promethee 软件操作——属建模细节与工具操作，留后续按需要再拉。
