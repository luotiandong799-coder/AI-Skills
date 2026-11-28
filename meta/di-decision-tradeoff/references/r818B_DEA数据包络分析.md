# r818B 下沉全文｜DEA 数据包络分析：多投入多产出的相对效率评价（DI · 2026-11-28）

> 正文摘要见 SKILL.md §三十四。本文件存逐字一手摘录与判非。3 独点：①相对效率而非绝对产出、DMU 同质集+无预设生产函数+效率值 0–1+前沿标杆；②CCR(CRS)/BCC(VRS) 分工与 TE=PTE×SE 分解、规模报酬系数 Σλ 判方向；③松弛变量/有效性双条件、数据正数与 DMU≥3×(投入+产出) 经验法则、有效单元过多用超效率模型、局限（对异常值敏感/相对排名无置信区间）。

## 一手来源（≥2 独立域）
- `https://superr.online/docs/mcdm/dea.html`（SuperR Online《DEA数据包络法》WebFetch 200 全文逐字：方法概述/计算步骤 7 步/银行分行案例/常见问题 Q1–Q6/使用建议/参考文献 Charnes1978·Banker1984）——第一独立域·方法平台一手。
- `https://www.sciencedirect.com/science/article/pii/S0925527398002527`（Elsevier《The efficiency of conventional fuel power plants in South Korea》WebSearch 逐字：DEA 源起 Debreu–Farrell、CCR 效率分式规划定义与线性化、CRS 假设、Farrell 效率=规模效率×技术效率、BCC 由 Banker et al. 引入）——第二独立域·期刊论文一手摘要。
- `https://www.sciencedirect.com/science/article/abs/pii/S037722172030792X`（Elsevier《A strong efficiency measure for CCR/BCC models》WebSearch 逐字：CCR1978 CRS/BCC1984 VRS、Farrell 技术效率=最大比例缩减投入、径向模型非零松弛缺陷、Pareto-Koopmans 有效、有效需 z0=1 且松弛全零）——第三独立域·期刊论文一手摘要。
- `https://qks.sufe.edu.cn/j/PDFFull/A160824004971.pdf`（上海财大期刊 PDF WebSearch 逐字：BCC 线性规划式、规模效率=TE/PTE 分离规模无效率与纯技术无效率）——第四独立域·中文学术一手。
- 诚信：`https://en.wikipedia.org/wiki/Data_envelopment_analysis` WebFetch 本地回退禁用（CODEBUDDY_WEBFETCH_DISABLE_LOCAL_FALLBACK=1）未采纳，未冒充一手。

## 独点 1：相对效率，不是绝对产出——DMU 同质集、无预设生产函数、效率值 0–1、前沿标杆
- superr.online 逐字：「数据包络分析（Data Envelopment Analysis, DEA）是一种基于线性规划的非参数效率评价方法，由 Charnes、Cooper 和 Rhodes 于 1978 年提出。该方法通过构建生产前沿面，将每个决策单元（Decision Making Unit, DMU）的投入产出数据投影到前沿面上，通过比较 DMU 偏离前沿面的程度来评估其相对效率。」
- 核心思想逐字：「每个 DMU 使用若干输入（资源）生产若干输出（成果）。不需要预设生产函数形式，完全由数据驱动。通过线性规划求解每个 DMU 的效率值（0~1），效率值为 1 的 DMU 位于前沿面上，称为有效 DMU（标杆）。」
- 关键判据：效率是**相对于同一批 DMU 的前沿**算出来的，换一批 DMU 或换指标集即换标杆——不是绝对产出高低，不是「产出大就效率高」。DMU 须同质（「要求同质，即使用相同的投入产出指标」），否则前沿无意义。
- 应用域：企业效率评价、银行分行绩效、医院效率、教育机构比较、供应链管理。
- 与既有 §六 MCDA（加权/AHP/TOPSIS）、§r813B 成本效果分析（ICER=ΔC/ΔE 单一健康产出）分工：DEA 管**多投入多产出、不设权重不设生产函数的相对效率**，靠数据内生把每个 DMU 与前沿比；MCDA 是先定权重再排序、ICER 是单产出效率比阈值——三者不同命题，不互替。

## 独点 2：CCR(CRS) vs BCC(VRS)、TE=PTE×SE、规模报酬系数 Σλ 判扩缩方向
- 模型定义的出处（Elsevier S037722172030792X 逐字）：「Charnes, Cooper and Rhodes (1978) (hereinafter CCR), in a context of constant returns to scale (hereinafter CRS), and Banker, Charnes and Cooper (1984) (hereinafter BCC), in a context of variable returns to scale (hereinafter VRS), provided a methodology to determine Farrell's efficiency measure by using linear programming, giving rise to Data Envelopment Analysis.」
- Farrell 技术效率逐字：「the maximum proportional reduction that can be operated on all inputs of a production unit (hereinafter DMU) maintaining the output level」——在产出不变下投入能同比例压到多低。
- CCR 分式规划（Elsevier S0925527398002527 逐字）：`Max p_j0 = Σ_r u_r y_rj0 / Σ_i v_i x_ij0`，约束 `Σ_r u_r y_rj / Σ_i v_i x_ij ≤ 1`（N 个 DMU 各一条），`u_r≥0, v_i≥0`；「a fractional programming problem, which may easily be linearized」。CCR 在**规模报酬不变**强假设下「corresponding to the most productive scale size (MPSS) point」。
- BCC 只加一条凸性约束 `Σλ_i = 1`（superr.online 逐字：「BCC 模型增加约束 ∑λ_i=1，允许规模报酬可变」），从而把规模因素剥出。
- 投入导向 CCR LP（superr.online 逐字）：`min θ`，s.t. `Σλ_i x_ij ≤ θ x_0j (j=1..m)`、`Σλ_i y_ir ≥ y_0r (r=1..s)`、`λ_i≥0`；产出导向最大化 φ、效率值换算为 `1/φ`。
- 三效率分解（superr.online 逐字）：技术效率 TE=CCR 效率（综合）；纯技术效率 PTE=BCC 效率（剔除规模）；规模效率 `SE = TE / PTE`；「纯技术效率低说明技术利用不足，规模效率低说明规模不优」。
- 规模报酬系数 `Σλ`：`<1` 规模报酬递增、`≈1` 恒定、`>1` 递减（superr.online 逐字）——据此判该扩规模还是缩规模，不是只看效率值。
- 选模口径：怀疑规模效应选 BCC、所有 DMU 同规模水平选 CCR；管理者控投入选投入导向、投入固定追求产出最大化选产出导向；BCC 效率值通常不低于 CCR。

## 独点 3：有效性双条件与非零松弛、数据正数与数量经验法则、局限
- 有效性的**双条件**（Elsevier S037722172030792X 引 Charnes et al. 1978 p.433 逐字）：「no DMU can be rated as efficient unless the following conditions are both satisfied (i) z0 = 1, and (ii) the slack variables are all zero.」——θ=1 但 slack 非零只是径向有效、不是 Pareto-Koopmans 有效；径向模型「does not give value to any inefficiency resulting from the possibility of reducing some inputs and/or increasing some outputs in addition to the maximum proportional reduction」，会高估这类 DMU。
- 松弛变量（superr.online 逐字）：输入松弛=实际投入−目标投入（冗余量）、输出松弛=目标产出−实际产出（不足量）；「非零松弛说明即使效率值达到 1，仍需调整才能达到完全有效（帕累托最优）」。给出「应减少/增加的具体数量」，是改进方向而非只排名。
- 数据条件（superr.online 逐字）：全部指标为正数（「至少非负」）；零/负值需平移变换或超效率 DEA 等扩展，「平台会给出警告，但不会自动处理」；输入越小越好、输出越大越好；至少 2 个 DMU、≥1 输入+1 输出。
- 数量经验法则（superr.online Q4 逐字）：「DEA 对指标数量敏感，经验法则要求 DMU 数量至少为输入+输出指标数的 3 倍。若指标过多，可考虑使用主成分分析降维或选择代表性指标。」——DMU 太少而指标太多会把大量 DMU 判为有效（前沿过松），失去区分度。
- 有效单元过多（superr.online 使用建议 5 逐字）：「若有效 DMU 过多（>50%），可考虑调整指标或使用超效率模型」；过少则查数据质量或放宽指标；应对比不同模型/导向结果做敏感性分析。
- 标杆与参考集：效率=1 的 DMU 构成生产前沿面可作标杆；每个非有效 DMU 的参考集由 LP 中非零 λ_i 对应的有效 DMU 组成（权重 λ_i）。
- 局限登记：DEA 给的是**相对排名/效率值**，非参数故不产出统计显著性区间，不能当成「绝对效率已证明」；对异常值敏感（单个离群 DMU 可抬高前沿）；指标方向选错（把越大越好的成本当输入）会使结论反；有效单元扎堆时区分度不足。

## 判非（写结论时禁止的表述）
- 禁「产出最大就是效率最高」——DEA 是投入产出比 + 相对前沿，绝对产出大不代表有效。
- 禁「CCR 效率=规模效率」——CCR 是综合技术效率 TE，须用 BCC 拆出 PTE 后 `SE=TE/PTE`。
- 禁「效率值=1 就完全有效」——还须所有松弛变量为 0 才是 Pareto-Koopmans 有效。
- 禁「DEA 能证明统计显著优于」——它不产出置信区间/显著性；要推断需另配统计方法（如 Elsevier S0925527398002527 用 DEA 效率作外生变量进计量模型）。
- 禁跨 DMU 集合/跨指标集直接比较效率值——前沿变了，分值不可比。
- 与 §六 MCDA、§r813B ICER 异命题，不互相替代。
