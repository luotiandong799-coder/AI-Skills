---
name: di-decision-tradeoff
description: 决策权衡分析（Decision Intelligence）。当用户面临 ≥2 个可行方案、需要在成本/收益/风险/可行性之间权衡、或要求"帮我选/对比/排优先级"时调用。提供加权决策矩阵、Pros&Cons 加权、Pre-Mortem、机会成本、ICE、RICE、Eisenhower、单向/双向门等框架，以及期望效用(EU)/信息价值(EVPI) 量化决策与"该不该再调研"停手线，输出结构化方案对比与推荐，绝不替用户做需授权的重大决定。、偏好反转、程序不变性、尺度兼容、诱导方式、选择与定价、权变加权、AHP一致性检验、CR/CI/RI、判断矩阵、逻辑传递性、阈值分档、标度粒度、层次总排序、影响图、信息弧、决策节点、价值节点、决策基三要素、前景理论、参照点依赖、损失厌恶、框架效应、确定性效应、反射效应、禀赋效应、编辑与评价两阶段、全局敏感性分析、Morris筛选、Sobol指数、一阶效应、总效应、交互效应、因子排序、因子固定、实物期权、real options、管理灵活性、延迟扩张放弃转换期权、ROV、不可逆投资、参考类预测、reference class forecasting、外部视角、inside view、规划谬误、planning fallacy、乐观偏差、optimism bias、reference class tennis、成本超支、uplift、Flyvbjerg、博弈论决策、game theory、占优策略、最佳回应、纳什均衡、混合策略、逆向归纳、子博弈精炼、不可信威胁、可信承诺、连锁店悖论、策略互动、效用函数 elicitation、标准赌局、standard gamble、确定等价、certainty equivalent、风险容忍常数、Arrow-Pratt、凹性风险规避、vNM公理、多属性效用、加性独立性、概率轮、权衡法、ELECTRE、PROMETHEE、outranking、非补偿性排序、concordance、discordance、净流、不可比、veto阈值、心理账户、mental accounting、交易效用、获得效用、银边原则、多收益分离、多损失合并、fungibility可替代性、沉没成本剧院票
module: DI
modules: DI,TI
version: "1.23.0"
---

# DI · 决策权衡分析（Decision Intelligence）

> 本技能是 Personal AI OS 13 模块中 **DI（决策智能）** 的唯一载体。TI 负责"想明白"，DI 负责"在多方案中作合理选择"。
> 方法论实拉自社区技能（2026-11-07 实拉）：`skillmd.ai/skills/decision-matrix-1`、`ruleskill.com/skills/iflytek/decision-matrix`、`hub.decision.ai/skills/nickcrew/decision-maker`、`github.com/alivirgo/Major-AI-Skills`（pros-and-cons-table）。

## 一、何时用

- 存在 ≥2 个可行选项，需要权衡（技术选型 / 架构 / 供应商 / 路线）。
- 需要对一批事项排优先级（功能 / 想法 / 实验）。
- 用户明确说"帮我选 / 对比 / 排优先级 / 该不该做"。
- **不适用**：低风险可逆的日常小事、需要执业资质的结论（医疗/法律/金融重大）、危机即时处置、数据完全不可得。

## 二、框架库（按场景选）

| 框架 | 适用 | 输出 |
|---|---|---|
| **加权决策矩阵（Pugh）** | 多选项 × 多标准 | 加权总分表 + 推荐 |
| **加权 Pros&Cons** | 快速二元抉择 | 两栏带权重评分 |
| **Pre-Mortem** | 高风险、需风险压力测试 | 失败模式清单 + 缓解 |
| **机会成本框架** | 两个都好、二选一 | 得/失/后悔测试 |
| **ICE** | 多事项快速排序 | Impact×Confidence×Ease |
| **RICE** |  backlog/功能优先级 | Reach×Impact×Confidence÷Effort |
| **Eisenhower** | 任务分诊 | 紧迫×重要 2×2 |
| **单向/双向门（贝索斯）** | 判断可逆性 | Type1 不可逆 / Type2 可逆 |

## 三、标准流程

1. **澄清决策**：一句话陈述决策 + 成功标准 + 截止时间。
2. **枚举选项**：列全所有现实选项，含"什么都不做 / 延后"。2–6 个为宜。
3. **选框架**：二元→Pros&Cons；多标准→加权矩阵；排序→ICE/RICE；风险→Pre-Mortem；分诊→Eisenhower。
4. **定标准（加权矩阵）**：列 3–5 条最关键标准（帕累托，>5 条增噪）；**权重由用户定**（防 AI 偏见）；含"切换成本/锁定风险"。
5. **打分**：每选项每标准 1–10 整数；总分 = Σ(分×权重)。
6. **检验假设**：看最强项、不确定性、不可谈判项、可逆性。
7. **输出**：推荐 + 依据 + 可能推翻结论的新信息。

## 四、硬护栏（实拉共识）

- **权重必须由用户确认**后才能打分（防 AI 操纵权重保其偏好）。
- **绝不编造**缺失的成本/概率/约束/偏好；标"估计/未知"。
- 高利害决策：框架只用于"组织问题与权衡"，**不当专业建议或最终结论**；引导用户核实事实并咨询有资质方。
- 分数非客观真理，是"用户已声明偏好的透明表达"——明确标注。
- 决策边界：DI 不替代 TI 分析，不擅自替用户作需授权的重大决定。

## 五、与 OS 协作

- 输出结构化方案对比 → 交给 **EI** 生成执行计划。
- 多 Agent 协作决策 → 委托 `agent-guild` 做收件箱交接。
- 决策记录 → **MI** 沉淀为"已验证经验"。

## 六、MCDA 形式化（加权 / AHP / TOPSIS + 敏感性）

> 加权决策矩阵的严谨版：把"拍分"升级为可审计的多准则决策分析（MCDA）。2026-11-07 实拉。
**① 加权和与归一化**
- 综合值 `V(a)=Σ wᵢ·sᵢ(a)`，权重归一 `Σwᵢ=1, wᵢ≥0`。
- 效益型归一 `s=(x−min)/(max−min)`；成本型反向 `s=(max−x)/(max−min)`——方向反了结论必错。

**② AHP 定权重（防"拍脑袋定权"）**
- 成对比较矩阵 A：`aᵢⱼ=1/aⱼᵢ, aᵢᵢ=1`；取主特征向量为权重。
- **一致性比率 CR** 必须算：常规阈值 CR<0.1；选项多、矩阵大时可放宽（实拉案例用到 0.2）。CR 超标=判断自相矛盾，须重填。

**③ 聚合方式（按需）**
- 加权和（补偿型，最常用）/ TOPSIS（正负理想解距离，`Pᵢ=Sᵢ⁻/(Sᵢ⁺+Sᵢ⁻)`，越近 1 越优）/ 超排序 outranking（PROMETHEE/VIKOR 概念：允许"不可补偿"）。
- 超排序可用一致性指数 `C(a,b)=Σ_{i:sᵢ(a)≥sᵢ(b)} wᵢ` 表达"a 在多大权重上不劣于 b"。

**④ 敏感性分析（必做，否则结论不稳）**
- **OAT（一次一因素）**：目标权重 0%→100%，其余等比缩放保和=1，观察排名反转点 → 画 tornado 图看哪条标准最撼动结论。
- **阈值分析**：找出使 top 选项发生 rank reversal 的权重临界值（安全边界）。
- **全局敏感性**：蒙特卡洛/狄利克雷 bootstrap 抽样上千组权重向量，算**排名稳定性** `RS(a)=P(a 排第一)`；高 RS=稳健，低 RS=靠权重假设撑着。
- **情景分析**：预设若干权重方案（"成本优先" vs "质量优先"），看结论是否随立场翻转。
- **判读铁律**：MCDA 排名是**条件性**的——依赖标准/权重/归一化/聚合规则/不确定性假设。输出须分开"稳健 top"与"边缘候选"，并声明在什么权重变化下结论会变。

## 七、决策日志与校准训练（来源：brierscore.com / digitaladvisory.com，2026-11-07 实拉）

**核心原则：决策 ≠ 结果**。好决策（当时信息下合理）可能结果差，坏决策可能侥幸赢——只评过程，因为过程是唯一可控的。

**决策日志七字段（结果出来前写，防事后偏差）**：
1. 决策内容与备选方案 2. 最强证据 3. 概率估计（必须给数字，"大概"不可结算）4. 最大不确定性/最大假设 5. 预期结果+置信度 6. **改主意触发器**（什么证据出现我会改变判断）7. 评审日期（何时对账现实，过期不评=日志退化为档案）

**日志腐坏四征兆（digitaladvisory）**：事后补写（=给未来写的新闻稿）、预期写得太模糊（怎么都不算错）、只记舒服的决策、写给未来读者看的体面话。有任一征兆，日志已失效。

**按桶校准复盘（brierscore.com 预测日志法）**：定期按概率桶（0.5-0.6/0.6-0.7…）汇总——说 70% 的事是否约 70% 发生？哪类问题主导错误？一次只修一个重复错误（如基率忽视/过度自信），下 5 个决策强制应用（如">500 元支出前必须找一个反证来源"）。

**与 MCDA 的分工**：本节管"决策后学习闭环"（时间维度）；§六 MCDA 管"单次多方案结构化对比"（空间维度）。

## 八、期望价值/期望效用 + 信息价值（EVPI）（2026-11-08 实拉）

把"拍分/加权"升级为**概率化期望决策**：当选项结果含不确定状态（各状态有概率 pⱼ）时，用期望而非单点估值，并能量化"是否值得再调研"。

**① 期望货币值 EMV / 期望效用 EU**
- EMV(i)=Σⱼ pⱼ·Rᵢⱼ（Rᵢⱼ=选 i 时状态 j 的收益）；选 argmaxᵢ EMV。
- 期望效用 EU=Σ pᵢ·u(结果ᵢ)；u(·) 为效用函数（风险厌恶者 u 为 concave，如 u(W)=√W 或 log W）。**EU 与 EMV 排序可能不同**——EMV 只看钱，EU 看"钱的效用"；大额/高风险下 EU 更稳（圣彼得堡悖论即因线性期望失真，D. Bernoulli 1738 用对数效用解）。
- 适用：结果有概率、金额大、风险态度显著时（保险/投资/赌注），优先 EU 而非 EMV。

**② 信息价值 EVPI（决定"该不该再调研/买情报"）**
- EV|PI = Σⱼ pⱼ·(maxᵢ Rᵢⱼ)（若事先已知状态 j，每状态选最优 i 的期望）；
- EVPI = EV|PI − EMV。即"消除不确定性"最多值多少钱。
- **判读**：报价 > EVPI → 拒买情报（不值）；报价 ≪ EVPI → 可买；EVPI≈0 → 当前不确定性不影响最优选择，无需再调研（直接定）。这是"调研/等待/买数据"决策的硬上限。
- 偏信息价值 EVPPI：只对少数关键参数求完美信息，比全模型 EVPI 更常用于研究优先级（PCORI）。

**③ 风险 vs 不确定性（Knight 1921）**
- 风险=结果集与概率可知（保险/频率）；不确定性=概率本身未知、无参照类（Knightian）。EVPI/EU 仅适用于"风险"；纯不确定性须降级为情景分析+专家判断，不可硬套概率。

**④ 行为边界（防过度迷信期望）**
- Allais(1953)/Ellsberg(1961) 悖论：真实人在同批选择中会违反独立性/确凿性原则且偏好稳定不改——EU 是**规范基准**非描述模型；选项含"确定性组件"或"模糊概率"时，结论须标注"与 EU 偏离风险"。
- EU 计算对输入敏感：u(·) 形态、概率估计、结果取值任一错 → 排序翻转；须做 §六④ 敏感性。

## 九、来源（2026-11-07 + 2026-11-08 实拉）

### 2026-11-08 新增（期望效用/EVPI，WebSearch 交叉核验）
- EVPI 定义与公式 EVPI=EV|PI−EMV、投资三选项例：en.wikipedia.org/wiki/Expected_value_of_perfect_information（2026-11-08）
- EVPI=WS−RP、报童问题例：lancaster.ac.uk STOR-I 讲义 Rebekah Fearnhead (2025)
- EVPI=E_Θ maxⱼ NB − maxⱼ E_Θ NB、EVPPI 公式：pcori.org Value of Information and Research Prioritization（2026-11-08）
- 自适应管理 EVPI=E_s[max_a U(a,s)]−max_a E_s[U(a,s)]：Springer 10.1007/978-3-031-99739-6_23（2026-11-08）
- 期望效用 EU=Σ pᵢ·u(结果ᵢ)、风险态度、圣彼得堡悖论：biz.libretexts.org Risk Management 3.4 Choice under Uncertainty（2026-11-08）
- vNM 四公理(完备/传递/连续/独立)、Allais/Ellsberg 悖论、Knight 风险vs不确定性：pressbooks.calstate.edu criticalthinking ch12（2026-11-08）

### 2026-11-07 原来源

- Weighted Decision Matrix / Pugh：skillmd.ai/skills/decision-matrix-1；ruleskill.com/skills/iflytek/decision-matrix
- Pre-Mortem / Opportunity Cost / ICE / RICE / Eisenhower / 10-10-10：hub.decision.ai/skills/nickcrew/decision-maker；skilld.dev/gh/iflytek/skillhub/decision-matrix
- 加权 Pros&Cons + Type1/Type2 门（贝索斯）：github.com/alivirgo/Major-AI-Skills/blob/master/skills/pros-and-cons-table/SKILL.md
- MCDA 敏感性分析（OAT/阈值/蒙特卡洛/情景）+ AHP 加权求和：ecologysci.com/posts/multicriteria-decision-analysis-for-ecosystem-services-a-comprehensive-framework-for-assessment-optimization-and-validation
- AHP 成对比较/一致性比率 CR/±25% 敏感性：mdpi.com/2071-1050/13/23/13483
- 加权和 V(a)/归一化/超排序一致性指数/排名稳定性 RS：sustainablecatalyst.com/?p=2841
- TOPSIS 正负理想解 + AHP/TOPSIS 敏感性：tandfonline.com/doi/full/10.1080/14786451.2023.2167999

## r708A 下沉：深不确定下不预测、改压力测试（RDM / DMDU，2026-11-08 实拉）

> 与上文 EU/EVPI 分工：EU/EVPI **假定概率分布已知或可估**，回答"再调研值不值"；RDM 处理**多方连概率分布与模型都无法达成一致**的深不确定，回答"不预测未来也能选什么"。两者是互补的两条决策轴，不互相替代。

- **XLRM 是决策框架，不是分析产物**：`X` 外部不确定因素 / `L` 可控杠杆（策略）/ `R` 二者到结果的关系（模型）/ `M` 绩效度量。**先定 XLRM 再跑模型**；缺 M 就无法定义"策略失败"，缺 X 的杠杆清单会把假设藏进模型里。判据：说不出这四格，就别开始算。
- **目标从"最优"换成"跨未来够用"（satisficing）**：深不确定下不找单个最可能未来去优化，而是让策略在**大量似然未来**里都达到阈值；用"牺牲峰值表现换低敏感性 / 保留未来选项"作为鲁棒定义。判据：报结论时给**达标比例与阈值**，不给"最优方案"四个字。
- **核心动作是压力测试而非概率加权**：RDM 在成百上千组假设上跑模型、把每组当**同等可能**来试探，不赋似然权重；与蒙特卡洛（按分布抽样估期望）方向相反。经典提问是"**要我们相信哪些假设成立，才会弃 A 选 B**"，把分歧从"谁预测得准"转成"结论依赖哪条假设"。
- **场景发现（scenario discovery）找的是失败箱，不是叙事场景**：用 PRIM / CART 在参数空间里圈出"策略未达阈值"的输入组合；箱体三指标同时权衡 **coverage**（覆盖多少政策相关案例）/ **density**（箱内尽量少决策无关输入）/ **interpretability**（能用少数关键参数说清）；用 **resampling test** 验可复现、**quasi-p-value** 估"这个约束是否偶然"。判据：输出的是可机检的**参数边界**，不是三五个故事线。
- **鲁棒性判据的选择本身会改变排序**：domain criterion / regret（`Max_i(u_ij) − u_ij`）/ satisficing 三档没有"所有情形下最好"的一档，**不同判据常给出不同策略排序** ⇒ 判据必须在问题框架阶段选定并写明，不允许跑完再挑一个支持既定结论的。
- 判据：**深不确定下的产出是"策略 + 它在哪些假设下失效 + 补救触发条件"，不是单点最优解**；自适应策略（随新信息演化）通常比静态策略更鲁棒，代价是复杂度与近/远期投资拆分。

**来源（2026-11-08 实拉，逐串核验）**：
- `uncertainfutures.github.io/theory/scenario-discovery/` — HTTP 200 / 19,687B，命中 coverage·density·interpretability·PRIM·CART·quasi-p-value·resampling·threshold。
- `www.rand.org/content/dam/rand/pubs/research_reports/RR1900/RR1932/RAND_RR1932.pdf` — **HTTP 403（正文未取到，如实登记不冒充命中）**；其 XLRM / satisficing / 与蒙特卡洛的分工由下列 4 个独立域交叉补足：
- `tile.loc.gov/.../2024739970.pdf`（RAND 科罗拉多河报告，WebSearch 摘要正文命中 XLRM / satisficing / scenario discovery）；`www.edgechat.ai/robust-decision-making`（XLRM 四要素 / regret / PRIM-CART 细节）；`sciencedirect.com/science/article/abs/pii/S2215016126003183`（OSeMOSYS-RDM：LHS 抽样 + PRIM 场景发现）；`onlinelibrary.wiley.com/wol1/doi/10.1111/j.1539-6924.2007.00940.x/references`（Lempert & Collins 2007：三种鲁棒判据与预防原则对照）。

## 十、排序反转与权重—量表对齐（2026-11-08 实拉，r715C）

> 与 §六④ 敏感性分析的**分工声明（判重结论）**：§六④ 处理「**权重变了**排名会不会翻转」（OAT / 阈值 / 蒙特卡洛 / 情景，输出 RS）；本节处理「**选项集变了**（增删或复制一个备选）排名会不会翻转」——成因是相对归一化而非权重假设，属另一条轴，互补不覆盖。来源：`sciencedirect.com/science/article/pii/S0895-7177(11)00785-0`《On rank reversal in decision analysis》+ `sciencedirect.com/science/article/abs/pii/S0377221799000405`《On the relativity of relative measures》+ 墨尔本大学 CEBRA《Uses and Misuses of MCDA in Environmental Decision-Making》PDF + USP 收录 Dyer《Remarks on the Analytic Hierarchy Process》PDF，4 独立域交叉；`rank reversal` 全库仅 1 处泛用、`秩反转` / `IIA` / `Distributive` / `Ideal mode` / `absolute scale` 全 0 命中。

- **r715C-1 排序反转（rank reversal）与无关方案独立性 IIA**：增删（甚至复制）一个备选会改变既有 A/B 的排序，极端情形 **total rank reversal**（最优直接变最差）；ScienceDirect 逐字 `the alternatives' order of preference changes when an alternative is added to or removed from the decision problem`、`Such rank reversals violate the invariance principle of utility theory`。IIA 公理源流：Luce & Raiffa 1957 axiom 7 `If an act is non-optimal ... it cannot be made optimal by adding new acts`；Belton & Gear 1983 发现「加入新副本」即可翻转；Dyer 1990 据此判定 AHP 不可接受；Harker & Vargas 反驳为理论误用。TOPSIS 同样有此现象。⇒ 判据：**决策结论必须声明「在哪个选项集下成立」**；增删候选后重跑，不沿用旧排序；与 §六④ 并列两条必检轴（权重扫描 + 选项集扰动），只做前者不算稳健。
- **r715C-2 Distributive / Ideal 两种合成模式须先选，且「保序」不总是对的**：EJOR 逐字 AHP `now supports two types of synthesis procedures – one that preserves rank and one that does not`；`Distributive` 把每准则下备选得分归一到和为 1 ⇒ 得分依赖**其他备选表现**，是排序反转的机制根源；`Ideal` 只除以该准则最优得分 ⇒ 保序。但**不能为了「不反转」盲目换法**：Luce & Raiffa 自己承认全保序 `yields unreasonable results`，Tversky 等给出一批「反转本应发生」的实证（context-dependent preference），Vargas 1997 反例证明乘法合成虽保序却在已知真值下给出无效答案；保序方法有无穷多种。⇒ 判据：先判本次决策**该不该受无关备选影响**，再选模式并写明理由；选项集是封闭固定的用 Ideal，允许「参照系随候选变化」的用 Distributive 并对扰动做复核。禁止把 rank reversal 一律当 bug 修掉。
- **r715C-3 权重脱离量表无意义；swing 式诱导与多利益相关方聚合前提**：墨尔本 CEBRA 逐字 `criteria weights, taken on their own, are meaningless`、`weights and performance scales must be aligned`；权重反映的是**该准则上备选的实际取值范围**（Edwards & Barron 1994 逐字 `weights reflect the range of the attribute (criterion) being weighted, as well as its importance`），改量表必须同步改权重，否则只重标定评分尺度就能翻盘（`the final ranking of options can be sensitive to changes in the performance scoring scales`）。Dyer 1990 p.256 诱导法：先告知决策者各准则**实际变动区间**，再问「从最差到最好这一整段变化」相对另一准则同等变化的重要度（SMART/swing 思路），而非抽象问「哪个更重要」。多利益相关方在未定义指标尺度时各按心中不同量表给权重，`any aggregation of these individual weights into group weights rather meaningless`。改用**绝对标度**（高/中/低，Saaty 1987 absolute scale）可使排名不随选项集变化。⇒ 判据：与 §四硬护栏「权重必须由用户确认」互补——那条管**谁来定**，本条管**定之前必须先固定 0/1 端点含义**；报加权结论时附「量表端点定义」，跨方比较先统一量表。

**提升层**：可复用 Skill（多方案权衡）/ 工作流（结论稳健性声明）。触发词：rank reversal、秩反转、total rank reversal、IIA、Luce-Raiffa axiom 7、Belton & Gear、Dyer 1990、Distributive/Ideal 合成模式、absolute scale、权重与量表对齐、swing weighting、量表端点、组权重不可聚合、选项集扰动复核。

## 十一、来源（2026-11-08 r715C 实拉，逐串核验）

- `www.sciencedirect.com/science/article/pii/S0895-7177(11)00785-0` —《On rank reversal in decision analysis》：定义、total rank reversal、IIA 公理源流、AHP/TOPSIS 双方法、Belton&Gear/Dyer/Harker&Vargas/Saaty 论争。
- `www.sciencedirect.com/science/article/abs/pii/S0377221799000405` —《On the relativity of relative measures》：Distributive vs Ideal 两模式逐字、Saaty 1994 要求显式选择、Tversky 等「反转本应发生」、Vargas 1997 乘法合成反例。
- `cebra.unimelb.edu.au/__data/assets/pdf_file/0011/2220887/0607_0610.pdf` —《Uses and Misuses of MCDA》：权重脱离量表无意义、Edwards&Barron 原句、Dyer p.252/p.256 诱导法、多方聚合前提、绝对标度。
- `edisciplinas.usp.br/pluginfile.php/8024038/mod_resource/content/2/Paper%202.Remarks-on-the-analytic-hierarchy-process.pdf` — Dyer《Remarks on the AHP》：A4 稀释 8/18→9/12 的数值例、hierarchic composition 失效、supermatrix 175 次比较的成本量级。

## r733B · 非补偿性决策、优超关系与输出类型（来源：2026-11-11 r733B 本轮独立实拉，≥2 独立域一手交叉）

> 模块：DI｜二轮深化第 4 批｜本轮定位：DI 3886B/6 条（次薄、主技能数仅 1）

### r733B-1 ★加权求和是补偿型，会把致命短板被高分抹平；有硬约束准则时必须换非补偿结构

ELECTE 逐字："A weighted-sum model is compensatory. Give each criterion a weight, score every alternative, multiply, and add. The mathematics permits a high score on one criterion to offset a low score on another"；给的实例是供应商 A 价格 9 / 交付可靠性 1、供应商 B 两项均 4，价格权重足够高时 A 在加权平均中胜出，而 "a missed delivery would stop production"。逐字结论 "a strong result on one criterion shouldn't automatically cancel out a failure that matters more than the average suggests"；"Weighted scoring asks which alternative has the highest total; ELECTRE asks whether one alternative is sufficiently supported and free from unacceptable failure"。Stockholm 学术综述逐字把两类方法对立起来："A central distinction within MCDA methodology lies between compensatory and non-compensatory approaches"、"ÉLECTRE employs veto thresholds that can block an alternative from being selected despite high performance in most other respects"，并指出非补偿准则常对应 "hard constraints or categorical imperatives"。判据：① 出加权矩阵之前先问「本决策有没有不可补偿准则」（安全 / 不可逆 / 合规 / 合同硬门槛）；有则该矩阵不是合适的聚合规则，须显式列 veto 条件并允许方案被一票阻断；② 异量纲（欧元 / 天数 / 检验分 / 定性风险）合并成单一数字是 "false precision"，逐字 "Combining them into one number can create false precision"；③ 与既有 §一/§四加权矩阵、ICE/RICE 等互补不覆盖——它们仍是纯补偿型决策的正确工具，本条只界定其适用边界。与 r715C-3「权重脱离量表无意义」分工：那条在补偿型内部修权重口径，本条判定补偿型本身不适用。

### r733B-2 ★权重语义随方法而变（汇率 vs 投票权），且阈值是外生输入不是方法从数据里找出来的

DecisionMind 逐字："Here, weights are not an 'exchange rate' as in TOPSIS but a 'voting weight' the criterion brings to the decision"；优超断言须两条件同时成立——"The first is concordance: a sufficiently large share of the criteria must support this claim. The second is the absence of discordance: even a single criterion on which the other side is clearly superior can refute the claim"，后者 "works like a kind of veto"。TU Delft 论文逐字给出阻断机制："A discordance index of 1 for any criterion ... means that no improvement in one alternative's performance or deterioration in the others' performance can offset this veto effect (Figueira et al., 2013)"，并给出阈值不等式 `v_j >= p_j >= q_j >= 0`（否决 / 偏好 / 无差异）。DecisionMind 逐字："ELECTRE III and TRI require the decision-maker to set, separately for each criterion, preference, indifference and veto thresholds; these thresholds come from outside and are not estimated from the data"；"A third error is presenting ELECTRE III's or TRI's thresholds or boundary profiles as 'an objective line the method finds by itself'"；灌溉合作社案例中收紧成本否决线会让最贵标书滑落 ⇒ "This makes the choice of the veto threshold a critical decision"。判据：① 报结论必须声明用的是哪种聚合语义，禁止把 §四/R715C 的「权重=边际替代率」直接搬到优超法；② 阈值须来源于运营容忍度 / 合同 / 法规 / 明确记录的管理判断，且在报告中标注为决策人输入；③ 必须做阈值敏感性测试——"Treat sensitivity testing as part of the decision, not as an optional presentation exercise"，禁止挑一组刚好支持既定结论的阈值。与 r715C-3 同源不同义：那条管权重端点定义，本条管阈值外生性与权重语义随方法漂移。

### r733B-3 ★先定输出类型再选方法族成员；不可比与不完整排序是合法结果，不是需要修掉的缺陷

DecisionMind 逐字："Members built on the same core logic produce a choice, a ranking or a sorting, depending on the purpose"——ELECTRE I 出 core set（"those that cannot be separated with these thresholds", not "the best ones"）、II/III 出全序或偏序、TRI 与预定义边界剖面比较后分类（accept/conditional/reject）；"An order (ELECTRE II, III) is not a distance score in the manner of TOPSIS"；"A category assignment (TRI) states not the alternative's absolute quality but where it falls relative to predefined boundary profiles. If the boundary profiles change, the assignment changes with them"。ELECTE 逐字承认局限："ELECTRE can produce incomplete rankings, incomparabilities, or intransitive relations"、"No automatic objectivity: The method structures judgement, but it doesn't eliminate judgement"；Stockholm 学术综述逐字 "These methods admit intransitivities and incomparabilities by design"，并警告 "Substituting a since-long well-established and sound axiomatic computational core for homemade calculi only leads to questionable results and opaqueness"。判据：① 开工先答「本次要的是选择集 / 全排序 / 归类」，再选成员；把 core set 读成排行榜、把 TRI 类别读成绝对质量分都是范畴错误；② 如实输出「两者不可比」或「本组无法区分」，禁止为了给一个完整排名硬调阈值；③ 不同成员结果不可直接横比（"different members produce different types of output under different assumptions"）；④ 换聚合核心必须建立在既有公理化方法上，不得自造混合算式。与 r715C-2「保序 vs 允许反转」互补：那条在补偿型内部讨论该不该受无关备选影响，本条给出「不接受全序」这一合法输出形态。

**提升层**：可复用 Skill（DI 模块方法论）/ 工作流（决策或编排的验收链）。

### r733B 来源与判非

- ELECTE《ELECTRE Method Explained: A Practical Decision Guide》Fabio Lauria，2026-09-04 → https://www.electe.net/post/electre-method-explained（WebFetch 200 全文逐字；厂商站，商业立场如实登记）
- DecisionMind Academy《ELECTRE》→ https://decisionmind.app/academy/methods/electre（WebFetch 200 全文逐字，独立域）
- Stockholm University DSV《Widely Used Multi-Criteria Decision Analysis Methods》→ https://people.dsv.su.se/~mad/Popular_MCDA_Methods.pdf（WebFetch 403 Forbidden，正文经 WebSearch 结果快照逐串核验，如实登记）
- TU Delft JSCMS《Dry port location selection ... Northern Vietnam》ELECTRE III 案例 → https://journals.open.tudelft.nl/jscms/article/download/7743/6067/28572（WebFetch 返回 application/pdf 二进制被丢弃，正文经 WebSearch 结果快照逐串核验，如实登记）
- 同厂商中文版交叉（不计独立域）：https://www.electe.net/zh/文章/electre-method-explained
- 判非：`outranking` 唯一命中在本技能 L71 概念列举，无机制内容；豆包自留地 WB 0 落地。

- 窄串 `veto threshold` / `concordance` / `discordance` / `non-compensatory` / `incomparab` 全库 SKILL.md **0 命中**；`outranking` 仅 1 命中，为 `meta/di-decision-tradeoff` L71 的一句概念列举「超排序 outranking（PROMETHEE/VIKOR 概念：允许"不可补偿"）」，无 veto / 阈值 / 输出类型 / 不可比性任何机制 ⇒ 按 rules/07 取「优＝加厚现有」并写明与 L71 的互补关系，不新建、不并存两套口径。
- 既有 §十 r715C 三条（排序反转 / Distributive-Ideal / 权重-量表对齐）全在**补偿型内部**讨论；r708A 的 RDM/XLRM 处理**深不确定下的概率不可知**；本轮三点是**补偿 vs 非补偿的聚合规则选择**，三条轴正交，结论不复用。
- `wb-execute-discipline` / `wb-context-compressor` 为豆包自留地，WB 0 落地；A 轮 OI 结论一律不复用；r731/r717/r715 各轮结论不复用。
- 换道：ELECTE 厂商站的产品导流（ELECTE ≠ ELECTRE 的辨析、SaaS 风险页）不落地；`people.dsv.su.se` PDF WebFetch 403、TU Delft PDF 二进制被丢弃，均如实登记为搜索快照逐串核验，未冒充一手全文直读；阈值具体数值属易漂移参数，只取不等式与外生性判据。

## 十二、多主体偏好聚合：循环、不可能与议程（2026-11-11 r736B 独立实拉 · DI）

> 与 §十 r715C 的**分工声明（判重结论）**：§十处理「**一个决策者**在补偿型方法里，增删/复制备选会不会翻转排序」（成因是相对归一化，rank reversal）；本节处理「**多个决策者 / 评审者**的偏好能不能合成一个不循环的排序」（成因是偏好聚合），属另一条轴，互补不覆盖。与 §十一 r733B（非补偿 ELECTRE 的输出类型）分区：那边管成员族产生 choice/ranking/sorting，本节管聚合前的可行性。与 §九 r708A（深不确定 RDM/XLRM）分区：那边是概率不可知，本节是偏好冲突。

### r736B-1 ★两两多数可以直接没有「综合排序」，加权给分不等于存在社会偏好

- SEP《Arrow's Theorem》(Winter 2022 Edition, First published 2014-10-13 / substantive revision 2019-11-26) §1 逐字：三人偏好 ABC / BCA / CAB，逐对投票得 A 胜 B、B 胜 C，却「it is just the other way around, since there are two voters who prefer C to A. **We do not have a social ordering of the alternatives at all. We have a cycle.**」；「Pairwise majority decision doesn't result in a social maximum, though… because they cycle, the social preferences do not.」
- 判据：① 多评审打分 / 多干系人排序 / 多 agent 投票汇总前，**先检验是否成环**（逐对矩阵算一遍）；② 成环时合法输出是「本组无稳定序 + 环的具体路径」，不是硬挑一个第一名；③ 加权求和总能算出一个数，但**数字存在 ≠ 排序合法**——它只是选定了一种聚合规则；④ 与 r733B「不可比、不完整排序是合法结果」同向，那里来自方法族设计，这里来自偏好结构本身。

### r736B-2 ★五条看似温和的条件不可兼得；任何「综合意见」都必须声明放弃了哪条

- SEP 逐字五条件：`Unrestricted Domain (U)`（能处理任何偏好组合）、`Social Ordering (SO)`（结果必须是传递且连通的排序，不许循环）、`Weak Pareto (WP)`（全员严格偏好 x>y 则社会也如此）、`Nondictatorship (D)`（不存在一个人的严格偏好永远成为社会偏好）、`Independence of Irrelevant Alternatives (I)`（x 与 y 的社会比较只取决于各人对 x/y 的偏好）。定理原文：「**Suppose there are more than two alternatives. Then no social welfare function f satisfies U, SO, WP, D, and I.**」
- 合法逃生口只有三类，且**每一类都在显式放弃一条**：① 域限制——SEP §5.1 单峰偏好 + 奇数投票者 ⇒ Black (1948) 证明两两多数必出排序，且赢家是**中位选民的 bliss point**（偶数投票者单峰也不保证传递性，需 Moulin 1980 的 phantom voter）；② 放宽 IIA —— Borda / 评分制（§5.2/5.3）；③ 引入基数效用或分数/等级（§5.3/5.4）。SEP《Social Choice》(First published 2013-12-18, substantive revision 2022-10-14) 逐字：「To avoid it, **we must relax at least one of the five conditions** or give up the restriction of the aggregation rule's inputs to orderings」。
- 判据：① 输出「综合大家意见后的推荐」时，必须写明**用了哪种聚合规则、放弃了哪条公理、候选项集是否固定**；② 禁止宣称「客观地综合了所有人的意见」——不存在同时满足五条件的客观综合；③ 若方案能沿**单一维度**（成本/工期/风险预算）排开、且各干系人偏好单峰，可改用中位规则并说明那一维是什么；④ 单峰不是默认成立的前提，须先问「大家是否在同一个评价轴上」，答不出就退回 §一的多方案对比矩阵而不是强行投票。

### r736B-3 ★IIA 违反是议程操纵的入口，候选清单本身就是决策变量

- SEP《Social Choice》Table 3/4 逐字实证：两个 profile 只在 Individual 1 的排序上有差别，且**x 与 z 的相对顺序都没变**，Borda 分却从 z(52)>x(51) 翻成 x(52)>z(51)——「Despite identical individual preferences between x and z in Tables 3 and 4, **the social preference between x and z is reversed, a violation of independence of irrelevant alternatives**.」紧接原文：「Such violations are common in real-world voting rules, and they make preference aggregation potentially vulnerable to **strategic voting and/or strategic agenda setting**.」另给 plurality 反例：34%/33%/33% 分布下「an alternative that is **majority-dispreferred to every other alternative** may win under plurality rule」，且「Plurality rule… also violates the weak Pareto principle」。
- Gibbard–Satterthwaite（SEP 逐字）：「There exists no social choice rule satisfying universal domain, non-dictatorship, the range constraint, resoluteness, and strategy-proofness.」唯一平凡满足的是独裁。Moulin (1980) 逐字：限制到单峰域时，中位投票类方案可满足其余条件。SEP 还区分 sincere / insincere manipulation（2000 年 Nader→Gore 妥协投票属前者），并登记「计算复杂性可阻碍操纵」（Bartholdi/Tovey/Trick 1989、Harrison & McDaniel 2008 Kemeny 行为激励兼容）。
- 判据：① **候选项清单与呈现顺序必须事先冻结并留痕**——加一个陪跑选项就可能改变既有两选项胜负，与 §十 r715C 的 rank reversal 同现象不同成因（那里是归一化，这里是计分依赖全体排序）；② 多人评审要收**完整排序或成对比较**，只收「第一名」等于偷偷换成 plurality 规则并引入多数不偏好者胜出；③ 「请如实打分」不是防操纵措施——策略免疫在通用域下定理级不可能，只能靠收窄域（单峰/二元）或降低可操纵收益；④ 与 `agent/grill-me` r735C 决策卫生四步互补：那条防锚定与信息顺序污染（**流程**），本条防候选集与聚合规则污染（**结构**），两条要一起用。

**提升层**：可复用 Skill（群体决策）/ 工作流（多评审汇总验收）。触发词：Condorcet 循环、投票悖论、Arrow 不可能定理、U/SO/WP/D/I 五条件、IIA 违反、Borda 计分翻转、单峰偏好、Black 中位选民、phantom voter、策略性投票、strategic agenda setting、Gibbard-Satterthwaite、候选集冻结、plurality 多数不偏好者胜出。

### r736B 来源与判非（独立实拉，2026-11-11）

- Stanford Encyclopedia of Philosophy《Arrow's Theorem》Winter 2022 Edition 一手 WebFetch 200 全文逐字 → https://plato.stanford.edu/archives/win2022/entries/arrows-theorem/
- Stanford Encyclopedia of Philosophy《Social Choice Theory》一手 WebFetch 200 逐字（First published Wed Dec 18, 2013; substantive revision Fri Oct 14, 2022）→ https://plato.stanford.edu/entries/social-choice/
- SEP《Normative Economics and Economic Justice》spr2026（Black 1958 单峰一致性、Condorcet 悖论）→ https://plato.stanford.edu/archives/spr2026/entries/economic-justice
- SEP 镜像交叉（不计独立域）→ https://plato.sydney.edu.au//entries///arrows-theorem/index.html · https://seop.illc.uva.nl/archives/spr2019/entries///arrows-theorem/
- 判重：`Condorcet` / `single peaked` / `median voter` / `irrelevant alternatives` / `agenda` / `spoiler` 全库 SKILL.md **0 命中**；`IIA` 命中集中在 `meta/di-decision-tradeoff` §十 r715C（AHP rank reversal 语境，Luce-Raiffa axiom 7 / Belton&Gear / Dyer 1990），本轮为社会选择公理化语境（Arrow 1951 / SEP），已在节首写明分工，不并存两套口径；`Arrow` 5 命中经查为箭头符号与地名子串噪声。⇒ 净新，取「优＝加厚现有」不新建（DI 唯一载体）。
- 未采纳：SEP 的政治哲学引申（Riker 对民主的解读）、Gibbard-Satterthwaite 的证明细节、phantom voter 的形式化构造、计算复杂性阻碍操纵的实证结论（仅登记不转为行动条款）。r715C 的 Distributive/Ideal、r733B 的 ELECTRE 输出类型、r708A 的 RDM 结论一律不复用。`wb-execute-discipline` / `wb-context-compressor` 为豆包自留地，WB 0 落地。

## 十三、先分类决策门，再定流程权重（r740C 实拉，2026-11-14）

> 本技能 description 已声明「单向/双向门 + EVPI 停手线」但正文此前无对应章节，本轮补齐结构性缺口。与 §八 EVPI 的分工：EVPI **算**「再调研值不值」，门型 **定**「该用多重的流程、谁拍板、多快拍」，两者互不替代；与 §七 决策日志（Brier 校准）互补：那条管「预测准不准」，本条管「选错能不能退」。
> 来源：rework.com《One-Way vs Two-Way Door Decisions: Bezos's Decision Framework》（Tara Minh，更新 2026-10-12）WebFetch 200 全文逐字（内含 2015/2016 股东信原文引述与对照表）；rufuspollock.org 转录的 2016 / 2017 股东信英文原文；澎湃新闻中文一手（贝索斯高速决策四条）；fasterthannormal.co / Dialogue Review（Colin Powell 40/70 与 70% 阈值）交叉。厂商/媒体二手立场一律登记，不作结论来源。

### 13.1 ★ 可逆性决定流程权重，与金额/风险/重要性不是同一问
官方逐字："A decision can be large and still reversible. A decision can be small and still locked in."（带退出罚则的三年合同、公开承诺日期、裁员公告 = 小但锁死；区域试点 = 大但可退）、"the framework is about the process, not the topic"、"Reversibility asks something sharper: what does being wrong cost, and how long does that cost last?"。Bezos 点名的失败模式是 "the heavy-weight Type 1 decision-making process on most decisions"。
- 判据：**跑 §六 MCDA 打分之前先出「门型」一行**；门型定的是流程重量、谁拍板、谁被咨询、要不要书面异议。把双向门送进重型流程，或把单向门当快决策，都是流程错配而非打分误差。与豆包自留地「按不可逆性选 HITL 审批模式」分工：那条是**动作执行层的确认门**，本条是**方案选择层的流程门**。

### 13.2 ★ 70% 是双向门专用启发式，不是研究阈值
官方逐字："The 70% rule belongs to the second column, not the first. Using it on a one-way door is a misreading, and it's the most common one."；"Both letters are Bezos's own statements of a management practice. Neither is a controlled study, so treat the framework as a judgment tool, not a measured result."；"It's a nudge to stop waiting, not a formula"。
- 判据：引用 70% 必须同时写「门型 = 双向」+「启发式、非实测」两个标签；**单向门上不能用它砍调研预算**（对照表信息门槛：单向门 "High, with time spent closing gaps"，双向门 "Around 70%"）。Colin Powell 40/70（40% 下限防赌博、70% 上限防拖延）是另一独立口径，别与 Bezos 70% 混成一个数。

### 13.3 ★ 双向门成立要靠「可设计的退出 + 回看日期」，不是口头可撤销
官方逐字："Often you can turn a one-way door into a two-way door by piloting, phasing, or adding an exit clause"、"Many 'irreversible' decisions are only irreversible because nobody tried to design the exit"、"A two-way door is only two-way if somebody looks back. Put a date on it"、"A reversible choice nobody revisits is effectively permanent"、"Confusing reversible with free. A reversible decision can still cost money, time, and credibility. The point is that the cost is bounded."
- 判据：决策日志固定三栏 **owner / 反转触发条件 / review date**；缺 review date 的「可逆」判定为事实单向门。可逆性是**可设计属性**（试点、分期、退出条款），不是固有属性；且可逆 ≠ 零代价，只是代价有界。输出推荐时先问五问：能否撤销 / 撤销代价（钱·时间·信任·士气）/ 谁被一起锁住 / 窗口多久关闭 / 能否缩小。

**提升层**：可复用 Skill（决策门分类前置门）/ 工作流（决策日志三栏）。触发词：one-way door、two-way door、Type 1 / Type 2 decision、可逆性、door classification、70% rule、nudge to stop waiting、exit clause、review date、disagree and commit、process not the topic。
**来源**：rework 2026-10-12 更新页 WebFetch 200 全文逐字 + 2016/2017 股东信原文转录 + 澎湃中文一手 + 两处二手交叉（2026-11-14 实拉）；`process, not the topic` / `nudge to stop waiting` / `exit clause` / `look back` 全库 0 命中，`单向门` 仅见于 `engineering/wb-artifact-verification` 的「上传是单向门」产物可达性隐喻（登记不复用）⇒ 净新。`wb-execute-discipline` / `wb-context-compressor` 为豆包自留地，WB 0 落地。

## 十四、决策质量 DQ：打分之前的六要素准入与最弱环（r744C 实拉，2026-11-14）

> 与 §十三（门型定流程权重）分工：门型答「这轮流程该多重」，本节答「这轮流程本身哪一段不合格」。与 `meta/ri-retrospective` §r742C（**复盘层**「决策质量与结果质量分栏」）分工：那条的落点在事后评价对象分离，本节的落点在**决策时刻、结果未知时**的准入清单；两轮结论不复用。≥3 独立域一手交叉。

### 14.1 ★决策质量 = 决策时刻的六要素过程判定，整体等于最弱一环
Spetzler / Howard / SDG 谱系（*Decision Quality*, Wiley 2016）定义六要素：**appropriate frame**（在解正确的问题、范围与人对）、**creative doable alternatives**（真选择集，「A decision with one option is not a decision」）、**meaningful reliable information**（证据及不确定性诚实陈述，非 advocacy）、**clear values and trade-offs**（事前声明要什么、愿意放弃什么）、**sound reasoning**（把证据连到选择的逻辑）、**commitment to action**（「A decision nobody executes was a conversation」）。链式规则逐字：「**overall quality equals the weakest element**」「**100% on five elements with a broken frame is a low-quality decision**」；「**Improvement effort goes to the weakest link, and stops when more effort isn't worth it**」。
- 判据：跑 §六 MCDA 打分**之前**先出六要素逐项评分（每项问「距 100% 差多少」，100% = 再投入不值得改善），整体取最小值；改进资源只投最弱项且边际收益转负即停。**禁把加权矩阵总分当决策质量**——那是方案排序，不是过程质量；五项满分而 frame 错仍是低质量决策。

### 14.2 ★按结果评分是学习机制污染，且无结构化记录时记忆会按结果重写决策
按结果给决策打分叫 **resulting**（Annie Duke, *Thinking in Bets* 2018）：逐字「**systematically promotes lucky recklessness and punishes sound judgment**」；学术一手 Vlek 1984 引文「**A decision is, therefore, a bet, and evaluating it as good or not must depend on the stakes and the odds, not on the outcome**」——理由是决策时刻 unchosen alternative 的结果永远不可观测，评价天然含不确定分量。Argumentree 逐字：「**A structured record makes the measurement honest; without one, post-hoc memory grades the decision the outcome deserved rather than the one that was made**」；可复核性判据是「could a **skeptic** inspect the frame, the alternatives considered, the evidence and its uncertainty, the stated trade-offs, the reasoning chain, and the execution plan — and find them adequate?」。
- 判据：决策日志必须在**结果未知时**写六要素评分并冻结留痕（含证据与不确定性、权衡、推理链、执行计划），事后补写一律标注为重构而非原始记录；DQ「**tests one decision**」，而「**enterprise decision excellence is the system that makes good decisions repeatable**」（治理 / 文化 / 有效性 / 组织记忆）是另一层 ⇒ 别把「同类决策反复出问题」当单次 DQ 打分去修。

### 14.3 ★诊断顺序由最弱项决定；更多数据 / 更强推演只补 information 一项
Grafium 官方逐字诊断例：「**A decision rich in alternatives but built on a poor frame should not have more alternatives generated; the frame should be reworked**」；「A decision with a clear frame, alternatives, information and values but **no commitment to action is a decision in name only**」；「The framework keeps both visible **without establishing in advance which element will be weakest**」。规范性边界逐字：「decision quality is **normative**」而 bounded rationality「is a **descriptive** theory of how humans actually decide」——混用会把「人常这么决策」当成「这样决策合格」。工具边界逐字：数字孪生输出「may contribute **conditional, modelled evidence** to the useful-information element … **They do not supply decision quality or sound reasoning by themselves**」；Argumentree 并列「**Sound reasoning — the element that turns those inputs into a defensible choice — is the one no framework supplies**」「**Better data inside a wrong frame is still a low-quality decision — the chain rule spares no element**」。
- 判据：拿到更强工具 / 更多数据 / 更多备选时，验收动作是**重跑六要素评分看最弱项是否已转移**，而不是继续往已达标项加料；六要素里只有 information 能被情报与模型抬高，frame / alternatives / values / reasoning / commitment 不随数据自动改善。

**提升层**：可复用 Skill（决策准入清单）/ 工作流（决策日志冻结留痕）/ RI 复盘（分层边界）。触发词：decision quality、six elements、appropriate frame、commitment to action、chain rule、weakest link、resulting、Annie Duke、Spetzler、100% 边际停手、normative vs descriptive、enterprise decision excellence、conditional modelled evidence。

**来源**：`https://www.argumentree.com/what-is/decision-quality?hl=en`（Last updated 2026-08-24，WebFetch **200 全文逐字**，含中英双页 `https://www.argumentree.com/zh/what-is/decision-quality`）+ `https://grafium.io/glossary/decision-quality-framework`（官方 glossary，WebFetch **200 全文逐字**）+ `https://symposium.org/wp-content/uploads/2021/12/global_perspectives_barometer_2016_final.pdf`（St. Gallen Symposium《Global Perspectives Barometer 2016》Info Box 3-1 六要素逐条与「linked as a chain … the weakest link will define the overall quality」，WebSearch 快照逐字）+ `https://dx.doi.org/10.1080/01446193.2019.1577559`（*Construction Management and Economics* 2019 论文，Howard 1988 / Spetzler 2016 六要素与 Vlek 1984 赌局引文，WebSearch 快照逐字）。四域交叉；Argumentree 自述为 argument-tree 产品方、其「第五要素无工具供给」属产品立场，仅取可迁移判据并登记；Bain *Decide & Deliver* 与 McKinsey 相关性证据按其自身口径标为 correlation，不作因果结论。
**判非**：`chain rule` / `weakest link` / `appropriate frame` / `commitment to action` / `Spetzler` / `six elements` / `Annie Duke` / `normative` 全库 `SKILL.md` **0 命中**；`decision quality` 1 命中与 `outcome bias` 1 命中均在 `meta/ri-retrospective` §r742C（复盘层评价对象分离，本轮取决策时刻准入层，互补不重述）；`resulting` 5 命中经查为 `resulting in` 类英文子串噪声。按 rules/07 去重铁律拍板「优＝加厚现有」，不新建、不覆盖复盘层结论。豆包自留地 **WB 0 落地**。A/B 两轮结论一律不复用。
## 十五、信息价值的四把尺与「必要 ≠ 充分」门槛阶梯（r748B 实拉 · 2026-11-15，3 独点）

> 适用：「要不要再查一轮 / 买数据 / 做一次调研 / 起一个验证实验」这类**为决策追加信息**的请求。
> 与 §八分工：§八已给 EVPI=EV|PI−EMV 与「报价 > EVPI 就拒买」的硬上限；本节不重述定义，补的是**四量测各回答什么**、**门槛的充分性方向**、**研究设计怎么择优**。与 §十四 DQ 分工：那条管决策时刻的六要素过程质量，本节管「这个决策值不值得再买信息」。

### 15.1（r748B-1）★EVPI / EVPPI / EVSI / ENBS 是四个不同问题的四把尺，不是同一个数的四种算法
- ISPOR 官方 2020-03-31 公告逐字：Report 2「details methods for computing **4 specific VOI measures**: (1) the expected value of perfect information, (2) expected value of partial perfect information, (3) expected value of sample information, and (4) expected net benefit of sampling」；Report 1 面向「decisions about the adoption of healthcare or the funding of healthcare research」，Report 2 面向 methodologists/analysts——**读者不同、问题不同**。
- 四个量各自回答：EVPI＝消除**全部**参数不确定性值多少；EVPPI＝只消除**一组**参数值多少（用来排研究优先级）；EVSI＝**某个具体研究设计**带来的部分信息值多少（Report 2 逐字 `EVSI = E_X[max_d E_θ|X {U(d,θ)}] − max_d E_θ{U(d,θ)}`）；ENBS＝population EVSI − 该研究总成本。EVPPI 是「任何以该组参数为对象的研究」的**上界**。
- 判据：决策记录第一行先写「本轮问的是哪一把尺」。**禁止把 EVPI 上限当作「这项研究值多少」**——EVPI 假设全知，实际有限样本只能买到部分信息；按 §八「报价 > EVPI 拒买」只能得出否结论，正结论必须落到具体设计的 EVSI/ENBS。

### 15.2（r748B-2）★门槛是阶梯，且「必要」与「充分」方向相反；研究成本含三项不只是调研费
- Report 2 官方逐字：「A population EV(P)PI that is **less than** the estimated costs of any research study is a **sufficient condition** for establishing that research is **not of value**. A population EV(P)PI that is **greater than** the estimated cost … is a **necessary, but not sufficient** condition」；ENBS≥0 才是「conducting the study」的充分条件（「A positive ENBS … provides a sufficient condition regarding the worth of a specific research study」）。
- 成本结构（Report 1 逐字，GPR/正文）：① 固定成本（setup、salaries）；② 每受试者/样本的可变成本；③ **机会成本**——「some participants will receive a non-optimal intervention **during the study**」，即研究期间相关方持续承受次优方案的损失。只算调研费会系统性高估「值得做」。
- 判据：**判定表按结论强度排四行**：`EV(P)PI < 成本` ⇒ 直接否、停（充分）；`EV(P)PI > 成本` ⇒ 仅进入下一门（必要非充分）；`EVSI > 成本` ⇒ 仍只是必要；`ENBS = EVSI − 成本 ≥ 0` ⇒ 才够判「这个设计值得做」。写「EVPI 很大所以该做这项研究」是把必要条件当充分条件，按 §14.2 同族的学习机制污染处理。

### 15.3（r748B-3）★研究优先级按「会不会改决策」排，不按「哪个最不确定」排；最优设计 = ENBS 最大
- Report 1 GPR6 逐字：「**EVPPI should be undertaken for groups of parameters** where it is likely that a new study … would be informative for the whole group, rather than for individual parameters」；同页反直觉事实：「**the parameters with the highest EVPPI will not necessarily correspond to the parameters that are most uncertain** … Eliminating uncertainty in a very uncertain but unimportant parameter … will have **no value**」。
- GPR9 逐字：「**Identify the most efficient study design as that with the greatest expected net benefit of sampling (ENBS)**」；EVSI/ENBS 须对**一组设计**（样本量、分配、随访长度、终点）分别算并取最大；「**When no design has a positive ENBS, the current available evidence should be considered sufficient for decision making**」。
- 判据：调研清单按 **decision relevance**（该参数不确定性是否会翻转最优选项）排序，不按方差/置信区间宽度排；输出物是「最有效设计 + 其余设计的 ENBS 对照」，不是「最大样本量」或「最全的调研」。全设计 ENBS≤0 时正确动作是**按现有证据拍板**（接 §13 门型：双向门不必等），而不是继续找更好看的设计。
- 结构不确定性补充（Report 2 逐字）：VOI 结果「always **conditional on the characterization of the decision problem**」；忽略结构不确定性「is equivalent to assuming that the model is perfect」，应参数化/情景/模型平均/差异分析显式纳入。⇒ 报告须写明「模型结构里哪些假设没被 VOI 定价」。

**提升层**：可复用 Skill（调研准入清单）/ 工作流（研究设计择优）/ DI 决策（信息采购）。触发词：EVPI、EVPPI、EVSI、ENBS、necessary but not sufficient、sufficient condition、opportunity cost、groups of parameters、most efficient study design、decision relevance、structural uncertainty、ISPOR VOI Task Force。

**来源（r748B 独立实拉 2026-11-15，≥2 独立域交叉）**：
- `https://www.ispor.org/heor-resources/news-top/news/view/2020/03/31/ispor-value-of-information-task-force-publishes-two-new-good-practices-reports`（ISPOR 官方公告，**Published Mar 31, 2020**，WebFetch **200 全文逐字**：四量测清单、Report 1/2 受众分工、Value in Health 2020 年 2 月/3 月两期）——**第一独立域（学会官方一手）**。
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC7373630/`（ISPOR VOI Task Force **Report 2** 全文，PMC 官方 HTML，WebFetch **200**；**AI 摘要 60s 超时 → 返回前 15,000/95,031 字原文逐字，如实登记**：四量测摘要、参数/结构不确定性、GPR1–4、EVPI/EVPPI 定义与公式、risk-neutral 前提）——**第二独立域（PubMed Central 官方全文）**。
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC7373630/pdf/nihms-1604682.pdf`（Report 2 PDF，WebSearch 快照逐字：`EVSI` 公式 (10)、`ENBS` 定义、**necessary, but not sufficient**、population EV(P)PI 的 sufficient condition、研究成本含机会成本）——**第三独立域（同一报告的 PDF 版逐串核对）**。
- `https://eprints.whiterose.ac.uk/id/eprint/158024/1/ISPOR_TF_Report_1_-_final_submitted.pdf`（Report 1 作者定稿，WebSearch 快照逐字：GPR6/7/8/9、ENBS 正负判据、三项成本、EVPPI 高≠最不确定、模型假设须声明）+ `https://ris.utwente.nl/ws/files/179932151/PIIS1098301520300279.pdf`（Report 1 另一机构仓储，WebSearch 快照逐字：informativeness、研究设计各要素、报告须按阈值范围图形化）+ `https://www.valueinhealthjournal.com/servlet/linkout?...doi=10.1016/j.jval.2020.01.004`（期刊页，WebSearch 快照逐字：EVPI/EVPPI/EVSI 公式 (4)(7)(10)、EVPI＝expected cost of uncertainty）——**第四、五独立域（学术仓储与期刊，交叉核验）**。
- **实拉诚信登记**：`eprints.whiterose.ac.uk` 与 `ris.utwente.nl` 两份 PDF 经 Bash `curl -sL` 直取均返回 **000 / 0B（TLS 连接被拒）**，`WebFetch` 对 PDF 返回 `application/pdf` 字节丢弃；故上述两条按**搜索快照逐字**引用，**未冒充一手 PDF 直取**。按 r731/r745 先例如实登记，结论仅采可与 PMC 官方 HTML + ISPOR 官方公告互相印证的部分。ISPOR 为专业学会、报告为 Task Force 专家共识（非随机对照实测），价值观前提（risk-neutral、社会视角成本）已登记，不作普适事实。
- **判非**：`expected value of perfect` / `decision curve` / `threshold probability` / `net benefit` / `reference point` / `loss aversion` 全库 **0 命中**；`value of information` / `EVPPI` 命中在**本文件 §八**（基础定义与本轮互补，不重述、不覆盖）；`EVSI` 1 命中在豆包自留地 `engineering/wb-execute-discipline` r687A（EVSI 与延迟成本比较，只读判非，**WB 0 落地**）。本轮净新在「四尺分工 + 必要/充分阶梯 + GPR6/9 设计择优 + 三项成本 + 结构不确定性」。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。

## 十六、程序不变性：偏好是诱导方式构造出来的（2026-11-15 r752B 实拉，3 独点）

> 与 §十（r715C rank reversal）分工：那条是**选项集增删**导致排序反转（AHP 归一化、IIA）；本节是**同一批选项换提问方式**导致偏好反转，两条轴不并存。与 §十五 VOI 分工：那条管「该不该再研究」，本节管「权重/排序从哪来」。

### 16.1（r752B-1）选择与定价给出相反偏好序，偏好不是稳定待测量
- **原文**：经典范式——「Lottery A provides a **9/12 chance of winning $110** and a 3/12 chance of losing $10（**P bet**）；Lottery B provides a **3/12 chance of winning $920** and a 9/12 chance of losing $200（**$ bet**）」；「When individuals are asked to **choose** between these two lotteries, they tend to choose **Lottery A**… When asked to select a **cash equivalent price** for each lottery separately they tend to place a **higher selling price on Lottery B**」。首报 Lichtenstein & Slovic 1971 / Lindman 1971，Tversky, Slovic & Kahneman 1990 系统复核。
- **判据**：决策矩阵中的「权重 / 排序 / 打分」必须声明是哪种诱导得来（选择 / 定价 / 匹配 / 评级 / 吸引力判断），**禁止把不同诱导方式产出的权重混进同一个加权矩阵**；用户说「我更看重 X」与「我给 X 打更高分」冲突时先记为诱导方式差异，不急着判用户前后矛盾。

### 16.2（r752B-2）主流解释是程序不变性违反 + 尺度兼容，不是传递性崩坏
- **原文**：三类解释「(a) violations of **transitivity**… (b) violations of the **independence axiom**… (c) violations of **procedure invariance**」；「According to Tversky et al. (1990), however, the violations of transitivity and independence axiom can account for **only a small fraction** of observed preference reversals. Therefore, violations of procedure invariance (usually considered as arising from effects of **scale compatibility**) are **nowadays the most widely accepted explanation: Due to the identical scale, the payoffs of a lottery are weighted more heavily in pricing than in choice**」（ResearchGate 快照另给出该小比例约 **10%**）。机制族：contingent weighting「The exponential weight of the probabilities is **low under the pricing condition and high under the choice**… while **monetary outcomes are assumed to be weighted more heavily in pricing than in choice**」；change-of-process「The **bids are a multiplicative function** of probability and amount, whereas **ratings are an additive function**」；expression theory 把成因放在「changes in the mapping from a gamble's components to the response」。Columbia 综述逐字「the weight of a stimulus attribute is **enhanced by its compatibility with the response scale**」「**the answer to how much you like a decision option can depend greatly on how you ask the question**」。
- **判据**：打分前先问「输出量纲与哪个属性同量纲」——同量纲属性会被系统性放大（收益与货币出价同量纲 ⇒ 定价时收益权重被抬高，选择时概率维度更突出）；改打分方式（金额 / 1–5 分 / 排序 / 两两匹配）等于改权重，须重跑而非沿用旧权重。

### 16.3（r752B-3）反转可被参数设计制造或消掉，且「出价」是否等于「偏好」本身存疑
- **原文**：Li 1994 / 该文三组赌局，原始参数下「**only 29%** of participants put a higher price on `$ bet` and, at the same time, actually choose the `$ bet`」；把最坏结果拉近（Problem 2：120/−10 vs 395/−15）后「**68%**」一致；反转最坏结果关系（Problem 3：270/−56 vs 930/−23）后「**66%**」。Columbia 综述「the preference-reversal phenomenon may be so robust because there are **multiple underlying causes, each of which may be operative in some situations but not others**」。作者质疑前提：「**The key issue is whether or not giving a price is the same as giving a preference**」；并指出同为货币的 bidding 与 subsidizing 两任务之间也出现排序反转，「make the existing explanations irrelevant」（expression theory / contingent weighting / change-of-process 三模型都不预测定价-补贴差异）。
- **判据**：出现「选了 A、却给 B 更高分」时，排查顺序 = 属性参数设计（最坏结果/概率/金额的相对差）→ 输出量纲兼容 → 诱导方式一致性；**不要归因为「用户非理性」或「权重没调好」，也不要靠再问一次求一致来修**。反转本身是设计信号：它告诉你哪个属性维度在被输出量表放大。

### 本轮来源（2026-11-15 r752B 实拉）
- `https://www.thefreelibrary.com/Preference+reversal%3a+a+new+look+at+an+old+problem.-a0149975067`（《Preference reversal: a new look at an old problem》）— **WebFetch 200，AI 摘要 60s 超时 → 返回前 15,000/51,331 字原文逐字**：P bet/$ bet 具体概率金额、三类解释、Tversky 1990「only a small fraction」、程序不变性为最广泛接受解释、expression / contingent weighting / change-of-process 三模型、29%/68%/66% 三组参数、「giving a price is the same as giving a preference」、bidding-subsidizing 反例。**第一独立域（期刊论文全文）**。
- `https://business.columbia.edu/sites/default/files-efs/pubfiles/1134/annual_review_constructive.pdf`（《Behavioral Decision Research: A Constructive Processing Perspective》Annual Review 综述）— **curl 200 / 4,394,813B，但 PDF 为扫描件，pypdf 46 页仅提取 45 字符 ⇒ 按 WebSearch 搜索快照逐字登记，未冒充一手 PDF 直取**：标准范式「two bets of comparable expected values… When asked to choose… most people prefer the bet with the higher probability of winning. When asked to bid… most people assign a higher value to the low-probability, high-payoff bet」、scale compatibility 定义、strategy compatibility、Schkade & Johnson 过程追踪、「multiple underlying causes」、「how you ask the question」。**第二独立域（学术综述，快照口径如实标注）**。
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC11652196/`（《Preference reversal in intertemporal decision making》2024）— WebFetch 仅返回 HHS 页眉、Bash `curl` **000/0B（TLS 拒连）** ⇒ 按 WebSearch 快照逐字：choice「qualitative reasoning / ordering strategy」、bidding「measuring an independent object with a caliper」、compatibility effect、loss 域同样反转、DFT/DDM 证据累积。**第三独立域（PubMed Central，快照口径）**。
- `https://www.researchgate.net/publication/379803705_Preference_reversals_in_judgment_and_choice`（快照逐字：intransitivity + independence「only account for a small proportion of the reversals (**10%**)」、overpricing 归因 scale compatibility、Expression Theory / Change-of-Process 细节）+ `https://baike.baidu.com/item/偏好反转现象`（中文快照：Karni & Safra 1986 / Holt 1986、兼容性假设、权变加权、齐当别模型、为自己/为他人决策诱发反转）。**第四、五独立域（学术仓储与中文百科，立场已登记，不作唯一结论来源）**。
- 判非：`preference reversal` / `程序不变` / `scale compatibility` / `尺度兼容` / `Lichtenstein` / `Slovic` / `权变加权` / `突出假说` 全库 SKILL.md **0 命中**；`elicitation` 3 命中全部属 MCP 客户端「向用户索取信息」（form/URL 两模式）与豆包自留地评测取样，异命题；`兼容性假设` / `procedure invariance` 在 DI 现有条目无覆盖。与 r715C（选项集增删）、r733B（ELECTRE 权重语义）、r736B（Arrow 偏好聚合）、r744C（决策质量六要素）、r748B（VOI 四尺）逐条分工，均不并存。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。

## 十七、AHP 一致性检验的能力边界与规模陷阱（r756A 实拉 · 2026-11-15，3 独点）

> 与 §十 r715C（选项集增删导致排序反转）、§十六 r752B（诱导方式构造偏好）分工：那两条管**结论依赖什么外部条件**，本条管**输入自身那道自洽门到底证明了什么**。§「加权决策矩阵」Step 的一致性比率 CR 是口号级要求，本节给出它的能力边界，按 rules/07「优＝加厚现有」不新建。

### 17.1 一致性比率是「逻辑自洽门」，不是「结论正确性门」
- 官方科普中国（中国科学院大学数学科学学院张三国教授认证词条，2026-02-21）逐字：「**一致性检验是AHP内置的质量控制机制，也是其区别于其他简单加权方法的核心特征**」；「AHP通过成对比较构建了一个相互关联的判断网络。例如，对A与B、B与C的判断，逻辑上蕴含了对A与C的特定判断。最大特征值的数学特性，使其能够**精确度量实际判断与这种逻辑传递性之间的偏差**」；CR 过高时「它向决策者发出明确信号：『您的判断存在矛盾，请重新审视您的偏好。』」，「这种『修正判断-重新计算CR』的迭代循环，极大地提升了**输入数据的质量**」。
- 判据：**CR 绿灯只证明这组成对判断不互相矛盾，不证明权重反映真实偏好、更不证明排序正确**——一个完全一致的矩阵可以整体系统性偏离（每个判断都同样错且不违反传递性）。报告分两栏写「输入自洽性（CR）」与「结论有效性（外部证据/敏感性/选项集）」，禁把 `CR<0.1` 写成「权重可靠」「决策已验证」。与 §十四 DQ 六要素分工：DQ 评的是决策过程，CR 只评其中 information 的一个子面。
- 文献立场（意大利巴勒莫大学学位论文，Saaty 1990 / Ishizaka & Lusti 2004 引述）：「**consistency is not necessary, and certainly not perfectly achievable by human subjects, but it is definitely desirable for the reliability of the results**」⇒ 一致性是**可取**不是**必要**，不得以「人做不到完全一致」为由跳过检验，也不得以「CR 达标」为由宣称结果可靠。

### 17.2 阈值随矩阵阶数分档，RI 是随机基线不是「允许错误量」；整数标度自带不可消除的不一致
- **定义链**（三域交叉逐字）：`CI = (λmax − n)/(n − 1)`；`RI` 是「对大量随机生成的正互反矩阵计算CI的平均值」（科普中国），Sabanci 论文「the average of C.I. values of these randomly generated matrices is defined as a reference point, Random Index (R.I.)」；`CR = CI/RI`（Roszkowska 综述写 `CR = CI/RI · 100%`，`CR≤10%`）。⇒ RI 是**随机判断的参照分母**，不是「可容忍的错误百分比」；引用必须写清用的是哪张 RI 表、n 是多少。
- **阈值分档**（巴勒莫大学学位论文逐字）：「**the upper bound for CR to consider a respondent "sufficiently" consistent is 0.1 for n-dimensional matrices, with n bigger than 5. Only for n=3 the CR upper bound is equal to 0.05 and for n=4 the upper bound is 0.08**」；中文科普/百科统一写「当CR<0.10时可以接受」是**简化口径**。⇒ 小矩阵（n=3/4）照抄 0.1 会放过按分档应判超标的不一致；判定表固定写「n / CI / RI / CR / 该 n 的阈值档 / 阈值出处」六栏。
- **整数标度是结构性不一致源**（Sabanci 大学《Modeling the Supplier Selection Process》逐字）：「**Varying levels of inconsistency are not rare cases in AHP. In fact, inconsistency might be observed due to several reasons even if the decision-maker is very consistent**」；具体反例「if Criterion A is strongly more important than Criterion C, and Criterion C is weakly more important than Criterion B, then it is not possible to make a consistent comparison between Criteria A and C, since the associated ratio is **5/3 which does not exist in the scale**」；「a consistent judgment … would be **15, which is beyond the upper limit of the scale**」；结论「**the inconsistency term is inherent in AHP**」。
- 判据：**CR 超标的第一排查项不是逼决策者反复改判断**，而是 ①矩阵阶数与该档阈值 ②1–9 标度是否无法表达所需比值 ③是否把本该分组的准则塞进同一矩阵。「修正判断-重算 CR」的迭代循环若收敛不了，说明是**标度粒度/结构**问题，继续追问只会把用户的真实偏好磨成能填进标度的数。

### 17.3 一致性检验有层级与规模边界：各层合格 ≠ 总排序合格
- 科普中国逐字：「在完成所有层次的权重计算和一致性检验后……同样，**也可以对整个层次结构进行总的一致性检验，以确保各层次累积的不一致性仍在可接受范围内**」⇒ 每个局部矩阵 CR 全绿时，累积到总排序仍可能超限；报表须同时给「每层 CR」与「总排序 CR」两个数，只列前者判不合格。
- 规模边界（Roszkowska 综述逐字）：「**it is not sensible to use the method for a large set of criteria**」，因成对比较数 `n(n−1)/2` 随准则数平方增长；Sabanci 论文亦点名特征向量法「obligation of a complete comparison matrix and **combinatorial growth of the number of comparisons**」。⇒ 备选/准则规模大时先分组、剪枝或换非两两比较方法，而不是硬填一张大矩阵再靠 CR 兜底。
- 输出模板：决策记录的一致性栏固定六项 —— ①每层矩阵 n 与 CR ②总排序 CR ③各 n 所用阈值档与出处 ④RI 表来源 ⑤标度（1–9 或自定义）与是否出现不可表达比值 ⑥若迭代修正过，记录修正了哪几个判断与修正理由。缺任一项，不得写「已通过一致性检验」。

### 本轮来源（2026-11-15 r756A 实拉）
- `https://www.kepuchina.cn/article/articleinfo?ar_id=675994&business_type=100`（科普中国《层次分析法（运筹学理论）》，上传时间 **2026-02-21**，认证专家中国科学院大学张三国教授）— **WebFetch 200 全文逐字**：一致性检验定义、逻辑传递性偏差、CR 作为反馈工具、RI 表 n=1..11（0/0/0.52/0.89/1.12/1.26/1.36/1.41/1.46/1.49/1.52）、CR<0.10、层次总排序一致性、λmax≈5.073→CI=0.01825→CR≈0.016 实例、1–9 标度表、几何平均法权重。**第一独立域（中文权威科普一手，认证立场已登记）**。
- `https://iris.unipa.it/bitstream/10447/105641/1/Anna_Errore_tesi.pdf`（意大利巴勒莫大学学位论文《ADVANCED STATISTICAL TOOLS FOR SIX SIGMA AND OTHER INDUSTRIAL APPLICATIONS》）— **WebSearch 快照逐字**：`CI=(λmax−n)/(n−1)`、Saaty 随机矩阵生成 RI、`CR=CI/RI`、阈值 **n=3→0.05 / n=4→0.08 / n>5→0.1**、`n(n−1)/2`、Ishizaka & Lusti「consistency is not necessary…but definitely desirable」、Belton&Gear/Dyer 批评线索。**Bash curl 403 / 5,549B 拦截页 ⇒ 如实按快照登记，未冒充一手全文**（**第二独立域，学术一手但取证口径降级**）。
- `https://research.sabanciuniv.edu/id/eprint/48891/1/10384999.pdf`（Sabanci 大学《MODELING THE SUPPLIER SELECTION PROCESS FOR MECHANICAL PARTS》）— **WebSearch 快照逐字**：「inherent in AHP」、5/3 不在标度、15 超上限、Saaty 1977 CI 与 1980 CR、RI 为随机矩阵 CI 平均、「acceptably consistent if … ≤ 10 percent of the C.I. of the random index」、1–9 标度五方案比较、特征向量法完整矩阵与组合增长两缺陷。**第三独立域（学术一手，快照口径）**。
- `https://repozytorium.uwb.edu.pl/jspui/bitstream/11320/2189/1/02_Ewa%20ROszkowska.pdf`（《RANK ORDERING CRITERIA WEIGHTING METHODS – A COMPARATIVE OVERVIEW》）— **WebSearch 快照逐字**：`CI=(λmax−n)/(n−1)`、`CR=CI/RI ·100%`、`CR≤10%` 接受、「The calculated priorities are plausible only if the comparison matrices are consistent or near consistent」、「not sensible to use the method for a large set of criteria」、ROC/RR/RS 与 AHP 权重对照表。**第四独立域（学术综述，交叉核验）**。
- `https://baike.baidu.com/item/层次分析法`（中文百科快照，与科普中国**同源表述**，仅作口径一致性交叉，不单列为独立结论来源）+ `https://www.mdpi.com/2071-1050/13/23/13483`（本技能 §十已引，CR/±25% 敏感性，按「合」登记不重述）。
- **判非**：`Random Index` / `RI 值` / `1-9 标度` / `整数标度` / `一致性不等于` / `逻辑传递性` / `一致性检验的能力边界` 全库 SKILL.md **0 命中**；`CI/RI` 1 命中为本技能 §「加权决策矩阵」既有 CR 口径（口号级），`AIP` 3 命中全为 `AIPromptsHub` 子串（异命题）；`Saaty` 命中在 §十 rank reversal 论争（异命题）。与 §十（选项集增删）、§十二（非补偿/veto）、§十三（门型）、§十四（DQ 六要素）、§十五（VOI 四尺）、§十六（诱导方式）逐条分工，均不并存。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除；豆包自留地 **WB 0 落地**。

## 十八、影响图：把决策基（备选/信息/偏好）画成一张可校验依赖的有向无环图（r760C 独立实拉 2026-11-17，≥2 独立域一手交叉，3 独点）

> 定位：本节管「**决策结构的显式建模**」——把「哪些量我能选、哪些量我不知道、哪些弧表示我决策前已知、偏好挂在哪个节点」画出来，让信息/依赖假设可审计。与 §十五 VOI 四把尺分工：VOI 回答「该不该再调研、值多少」，本节回答「这条信息在决策时到底可不可得、依赖结构长什么样」——影响图是 VOI 的**结构前置**（信息弧画错，EVPI 算得再准也是错的前提）。与 §十四 DQ 六要素分工：那是决策质量的检查清单，本节是检查清单里「information / alternatives」两项的结构化表达。与决策树：树随变量数**指数增长分支**，影响图用共享节点紧凑表达同一决策问题。

### 18.1（r760C-1）影响图是贝叶斯网络 + 决策节点 + 价值节点；三类节点 + 三类弧各自对应决策基三要素
- **原文**（BayesFusion GeNIe 官方文档《Influence diagrams》WebFetch 200 一手全文逐字）：「Influence diagrams (Howard & Matheson 1984) … are **acyclic directed graphs** representing decision problems. The goal … is to choose a decision alternative that has the **highest expected gain (expected utility)**」；「influence diagram can be also viewed as **Bayesian network extended by decision and value nodes**」。四类节点：Chance（circle/oval，随机变量，用条件概率分布量化）、Decision（rectangle，「under full control of the decision maker … specifying the probability distributions over their outcomes is **pointless** — we just specify their possible states」）、Deterministic（double oval）、Value（diamond，「represent utility … always **continuous** … quantified by the utility of each of the possible combinations of outcomes of the parent nodes」）。三类弧（Wikipedia/HandWiki《Influence diagram》WebFetch 一手逐字）：「**Functional arcs** (ending in value node) … a component of additively separable utility function is a function of all nodes at their tails；**Conditional arcs** (ending in uncertainty node) … probabilistically conditioned on tails；**Informational arcs** (ending in decision node) … the decision … is made with the outcome of all nodes at tails **known beforehand**」；「Decision nodes and incoming information arcs collectively state the **alternatives**; Uncertainty/deterministic nodes and incoming conditional arcs … model the **information**; Value nodes and incoming functional arcs … quantify the **preference** … termed **decision basis**」（alternatives / information / preference 三要素）。
- **判据**：① 决策基三要素（备选/信息/偏好）各有明确的图元承载——**决策节点+信息弧=能做什么、机会节点+条件弧=知道什么与概率关系、价值节点+功能弧=偏好怎么算**；画图时缺任一类节点/弧，等于决策基缺一项，与 §十四 DQ 最弱项诊断同向。② 决策节点**不写概率**（完全可控，只列可能状态），价值节点**是连续的**且按父节点组合打分——把决策节点当随机变量赋概率、或把价值节点当离散标签，都是建模错误。③ 影响图 = BN 扩展，所以「只保留机会节点」的子图就是一个贝叶斯网络，可复用 d-分离读条件独立：缺一条弧意味着存在一组节点使两变量条件独立，不是「忘了画」。④ 用途边界：目标是**最大期望效用**，因此与 §十五 VOI 同族（都属 EU 框架）；深不确定下 EU/EVPI 失效时（§一 RDM/DMDU）影响图的「期望效用最大化」前提也不成立，此时只借用其**结构可视化**，不借用其求解结果。

### 18.2（r760C-2）信息弧表示「决策时已知」的时间/信息先后，不是因果；多决策节点必须用信息弧串成序列
- **原文**（BayesFusion 一手逐字）：「Normally, an arc in an influence diagram denotes an influence … Some arcs … have clearly a **causal** meaning. In particular, a directed path **from a decision node to a chance node** means that the decision (an intervention … imposing a value) will **impact** that chance node … changing the probability distribution over its outcomes. **Arcs coming into decision nodes are called informational arcs and have a different meaning.** As decision nodes are under the decision maker's control, these arcs **do not denote influences but rather temporal precedence (in the sense of the flow of information)**. The outcomes of all nodes at the tail of informational arcs will be **known before the decision is made**. In particular, if there are multiple decision nodes, they **all need to be connected by informational arcs**. This reflects … decisions are made in a sequence and the outcome of each decision is known before the next」。Terek《Decision Trees and Influence Diagrams in Decision Analysis》PDF 一手逐字：虚线弧指向决策「the decision is made **knowing the outcome** of the predecessor node … the specific information available to the decision maker」，决策→决策弧「the first decision is made **before** the second」，正确构造的影响图「have **no cycles**」。
- **判据**：① **信息弧 ≠ 因果弧**是本节的头号易错点：指向机会/价值节点的弧是「影响/条件」，指向决策节点的弧只是「这条信息在做决定前已知」，画反方向会把「我决策时知道天气」误读成「我的决策改变天气」。② 多决策必须显式排时序：每个后续决策都要有从前序决策来的信息弧，否则图在说「第二个决策不知道第一个选了什么」，求解结果无效。③ 图必须无环：出现环说明「A 决策前要知道 B，B 决策前又要知道 A」的时间悖论，先修结构再谈计算。④ 与 §十五 VOI 直接接口——Wikipedia  vacation 例：决策「度假活动」、机会「天气」与「天气预报」、价值「满意度」，仅「预报→决策」有信息弧；三场景（决策时已知真实天气 / 只知道预报 / 二者皆不知）对应加/留/删信息弧，第一最好、第三最差 ⇒ **EVPI 就是「加一条天气→决策信息弧」带来的效用差**（把 §十五抽象的「消除不确定性值多少」落成图上的一条弧）。⑤ 报告要求：决策记录须附「信息弧清单」——每条写明「哪个量、在做哪个决定前、是否真的已知」，缺此清单不得声称做过 VOI 分析。

### 18.3（r760C-3）影响图相对决策树的紧凑性是「共享节点」，但准确性受限于输入值质量；团队决策可显式表达信息不共享
- **原文**（Wikipedia/HandWiki 一手逐字）：「now adopted widely and becoming **an alternative to the decision tree which typically suffers from exponential growth in number of branches** with each variable modeled. ID is **directly applicable in team decision analysis**, since it allows **incomplete sharing of information among team members to be modeled and solved explicitly**；Extensions … in game theory as an alternative representation of the game tree」。NAP《Persistent Forecasting of Disruptive Technologies》一手逐字（Howard & Matheson 1981）：影响图「generalizations of Bayesian networks … improved variants of decision trees or game trees」，「its ability to accurately predict an outcome is **dependent on the quality of values** that are assigned to uncertainty, utility, and other parameters」，「error bars … depend on the quality of the values that capture the underlying interrelationships」。BayesFusion 一手：「goal … highest expected gain」+ VentureID 投资例（Investment decision 两状态 Invest/DoNotInvest，Expert forecast / Success of venture 机会节点，Financial gain 价值节点）。
- **判据**：① 选影响图而非决策树的判据是**变量多、分支组合爆炸**：树每个变量都复制整棵子树，影响图用共享节点表达同一结构；变量少、时序简单时树更直观，别为画而画。② 结构正确 ≠ 结论正确：图把依赖画清楚了，但输出精度受限于机会节点的概率值与价值节点的效用值质量；「图画得漂亮」不能替代 §十五 VOI 对参数不确定性的量化，须报参数来源与误差棒。③ 团队/多方决策的独特价值：信息弧能表达「谁在做决定时知道什么」，因此**信息不对称可被显式建模**——这正好补 §十五 VOI 的「给谁的信息值多少」（EVPPI 按参数组、团队按成员分工），须与 `agent-guild` 的跨 agent 信息共享规则分开（那条管机制，本条管建模）。④ 与 §一 RDM/DMDU 的边界重申：影响图求解依赖概率与效用赋值，深不确定下这些值本身无共识 ⇒ 只用于呈现结构与讨论「哪些信息值得获取」，不输出「最优方案」假精确。⑤ 落地触发：当决策涉及 ≥3 个变量且存在「先知道 X 再定 Y」的时序、或多人信息不对称时，先用影响图把结构画出来再套 §十五 VOI/§十 AHP 等方法计算。

**来源（r760C 独立实拉 2026-11-17，≥2 独立域一手交叉）**：
- `https://support.bayesfusion.com/docs/GeNIe/da_ids.html`（BayesFusion GeNIe 官方《Influence diagrams》文档，WebFetch 200 一手全文逐字）— Howard & Matheson 1984、DAG 定义与最大期望效用目标、BN+决策/价值节点、四节点两类弧、决策节点不赋概率只列状态、价值节点连续且按父组合量化、因果路径（决策→机会）vs 信息弧（指向决策=时序/信息流）、多决策须信息弧串联、VentureID 投资例。**第一独立域·厂商工具官方文档一手**。
- `https://wikiwand.com/en/Decision_node` + `https://handwiki.org/wiki/Influence_diagram`（Wikipedia 镜像《Influence diagram》，WebFetch 200 一手全文逐字）— 三类节点三类弧逐定义、decision basis 三要素（alternatives/information/preference）、d-分离与缺弧含义、vacation 三场景 VOI 例、相对决策树指数分支的紧凑性、团队决策信息不共享建模、博弈论 game tree 扩展。**第二独立域·百科一手**。
- `https://jamsi.fpv.ucm.sk/docs/v01n01_04_2005/v01n01_09_Terek.pdf`（M. Terek《Decision Trees and Influence Diagrams in Decision Analysis》，WebFetch 摘要逐字）— 实线/虚线弧语义、虚线指决策=已知前驱结果、决策→决策=先后、正确构造无环、投资决策图例。**第三独立域·学术一手（摘要口径）**。
- `https://www.nap.edu/read/12557/chapter/4`（美国国家科学院出版社《Persistent Forecasting of Disruptive Technologies》ch4，WebFetch 200 一手全文逐字）— Howard & Matheson 1981、ID 是 BN 推广与决策树改进变体、四类弧定义、决策基三要素、精度依赖参数值质量与误差棒、技术预警用途。**第四独立域·国家级学术机构一手**。
- **判非**：`influence diagram` / `影响图` / `informational arc` / `信息弧` / `decision node` / `价值节点` / `决策基三要素` 全库 SKILL.md **0 命中**；`regret` 命中本技能 §十（决策后悔/resulting，异命题）。与 §一（RDM/DMDU 深不确定）、§十（选项集）、§十二（非补偿/veto）、§十三（门型）、§十四（DQ 六要素）、§十五（VOI 四尺：EVPI/EVPPI/EVSI/ENBS）、§十六（诱导方式）、§十七（AHP 一致性）逐条分工，均不并存——本节是**结构建模层**，那八节是**方法/评价层**，本节为 §十五 VOI 提供信息弧结构前置。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除；豆包自留地 **WB 0 落地**。
- **未采纳**：影响图的求解算法（variable elimination / junction tree 具体推导）、效用函数公理体系（vN-M 完整证明）、价值节点加性可分的数学前提详述、game theory 扩展形式博弈建模、具体工具（GeNIe/Netica）操作步骤、连续节点离散化细节。

## 十九、前景理论：同一个决策换个说法就翻转，权重不是稳定偏好（r764C 独立实拉 2026-11-18，≥2 独立域一手交叉，3 独点）

> DI 前面各章假设「权重/排序能被稳定诱导出来」——§十六证明诱导方式会构造偏好，本章再进一步：**参照点本身可被措辞移动**，同一客观选项在「收益框」与「损失框」下被归到价值函数不同侧，风险偏好直接翻转。这解释了为什么用户「刚才稳健、现在激进」未必是前后矛盾，而可能是你换了表述。

- **r764C-1 ★评价的是相对参照点的变化量，不是绝对量；编辑阶段 situation-dependent，评价阶段才稳定**：前景理论（Kahneman & Tversky 1979）把决策分两阶段——「an editing phase, in which the problem is recognized and the decision framework is determined, and an evaluation phase, in which the alternatives are evaluated according to the problem recognition」；一手逐字「The former phase is situation-dependent and can be altered by slight differences in linguistic expression, whereas in the latter phase, once the problem is identified, situation-independent evaluations and decisions are made」。参照点是价值函数的原点、「is determined at the editing stage」，且「can easily be shifted depending on how the decision problem is edited」。⇒ 决策矩阵先固定「参照点写死是什么」（现状？预期？目标？——三参照点理论分底线/现状/目标），再 elicitation；同一批选项改了措辞（「保住 400」vs「损失 200」）后若权重变了，先归因于参照点被移动，不要直接改原始权重表或判用户非理性。

- **r764C-2 ★价值函数 S 型 + 损失侧更陡 + 小概率超权：四条可检验的行为预测**：ScienceDirect 逐字——价值函数「S shaped … convex below the reference point (people are risk seeking in the domain of losses) and concave above it (people are risk averse in the domain of gains)」，且「asymmetric, steeper below the reference point than above it … loss aversion」；概率权重函数「small probabilities are overweighted, and large probabilities are underweighted」。由此四条：**确定性效应**（面对收益偏确定选项）、**反射效应**（面对损失偏冒险）、**损失厌恶**（损失痛苦 > 等量收益快乐，1992 量化版至少约 2 倍）、**禀赋效应**（拥有后估值抬高：Kahneman 1990 马克杯实验，拥有者要价高于未拥有者出价，WTA>WTP 违背新古典「估值不受所有权影响」）。⇒ 把选项摆进决策矩阵前先标注它落在 gain 还是 loss 域；报「loss aversion 系数约 2」须标来源（1992 量化版）与实际是否本地验证；2020 跨国复制研究（n=4,098 / 19 国 / 13 语言）验证大部分原始结论可复制，但不是精确系数普适。

- **r764C-3 ★框架效应是偏好翻转不是噪声；参照点可以是「期望」而非现状**：ScienceDirect 逐字「the framing effect occurs when the same decision problem is perceived differently in different linguistic expressions in the editing stage」，且「By shifting the reference point, the same decision problem becomes risk-averse when the decision maker grasps the options in the gain domain, and risk-oriented … in the loss domain. Thus the framing effect can explain the reversal of preferences」。心理所 PDF（Lu 等）引入 Köszegi & Rabin 2006：参照点可以是**期望**而非现状——「an unexpected wealth of $400 is a gain, but receiving $500 with an expectation of $600 can be viewed as a loss」；并指出决策对象是「自己」还是「他人」会移动参照点（为自己决策时期望拿到 100% 作参照点，为他人决策时以 0% 作参照点），从而同一收益分配在自/他框架下风险偏好相反。⇒ 涉及「代用户做决定/给团队提方案」时，先声明以谁的期望为参照点；用户先稳健后激进，排查顺序=表述框架→参照点归属→gain/loss 域，与 §十六「诱导方式→输出量纲→诱导一致性」串联成完整诊断链；不靠「再问一遍求一致」掩盖框架效应。

**来源（r764C 独立实拉 2026-11-18，≥2 独立域一手交叉）**：
- `https://www.sciencedirect.com/topics/economics-econometrics-and-finance/prospect-theory`（ScienceDirect《Prospect Theory》百科条目 WebFetch 200 全文逐字）— 编辑/评价两阶段与 situation-dependent、参照点为价值函数原点且可移、价值函数 concave gain/convex loss/损失侧更陡、概率权重小超权大低权、框架效应致偏好翻转、Econometrica 1979 47:263-292 著录。**第一独立域·一手百科**。
- `https://www.sciencedirect.com/topics/neuroscience/prospect-theory`（ScienceDirect neuroscience 版《Prospect Theory》WebFetch 快照逐字）— 确定性/反射/损失厌恶/禀 endowment、Kahneman 1990 马克杯 WTP/WTA、S 型价值函数与 4.1 节、Tversky-Shafir 1992 sure-thing 违反。**第二独立域·一手百科**。
- 交叉快照（不冒充一手全文）：`https://ir.psych.ac.cn/bitstream/311026/32444/1/...pdf`（中科院心理所《Risk preferences in self-other decisions》PDF WebSearch 快照逐字，Köszegi-Rabin 参照点=期望、$400/$500/$600 例、自/他分配框架参照点 100% vs 0%）· 百度百科前景理论/风险决策机制（2020 跨国复制 n=4,098/19 国/13 语言、损失痛苦≥2 倍收益快乐、三参照点理论底线/现状/目标）。原始 1979 Econometrica 论文全文 PDF 未直接取得，按百科一手转述登记不冒充原文。
- **判非 / 去重**：`前景理论` / `prospect theory` / `损失厌恶` / `参照点依赖` / `框架效应` / `禀赋效应` 全库 SKILL.md 0 落地；`loss aversion`/`reference point` 仅在本技能 §十五 r748B 的判非串（明确写「全库 0 命中」，那里主落地是 VOI 四把尺）。r748B 判非已预留本主题，本轮正式展开、不覆盖其 VOI 结论。与 §十六程序不变性（诱导方式构造偏好）、§十五 VOI（该不该再调研）、§十七 AHP（逻辑自洽门）分工，不并存。与 r762/r761/r760 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：价值函数/权重函数的具体参数拟合（α≈0.88/λ≈2.25 等）、累积前景理论的秩依赖权重公式、前景理论在金融/营销的具体应用案例（建模与场景细节，留给后续）。

## 二十、没有可信概率时的决策准则：minimax regret 与深度不确定性鲁棒性（r768C 独立实拉 2026-11-19，≥2 独立域一手交叉，3 独点）

> §十五 EVPI/EVSI 与 §十九前景理论都默认「各状态的概率（或至少能 elicitation 出主观概率）」可用。本章补一个前置缺口：**当概率根本不可信或不存在（Knightian / deep uncertainty）时，EU 与 EVPI 失去输入**，此时要换一批不依赖概率的不确定性准则。核心不是「算得更准」，而是「换决策哲学并显式声明」——四个准则常给出不同答案，报告它们的分歧本身就是产出。

- **r768C-1 ★regret = 该状态下最优行动的收益 − 所选行动的收益；minimax regret 取「最大后悔」最小的行动，不需要概率**：Savage（1951）提出的 minimax regret，一手定义（RAND RGSD340 逐字）`R(s_i,f_i) = Max[Performance(s',f_i)] − Performance(s_i,f_i)`，决策 `Min_{s_i} Max_{f_i} R(s_i,f_i)`——后悔是「若事后知道哪个状态发生，本可选的最优 vs 实际所选」的差。做法四步：列行动×状态收益矩阵→每列（状态）找最大值→每格用列最大减去它得后悔矩阵（每列至少一格为0）→每行取最大后悔、选最小那个。MetricGate 逐字「No prior distribution is required — the rule is invariant to state probabilities」，且对损失矩阵的加性平移不变（因按每状态最优归一化）。⇒ 当用户说「我根本不知道各情况概率」时，不要硬套 EU/EVPI 或逼他猜主观概率——改用后悔矩阵；这也回应 §十五「研究该不该做」在深不确定下的失效（连概率都没有，EVPI 无从算起）。

- **r768C-2 ★它处在「极端悲观 maximin」与「均匀先验 Bayes/Laplace」之间，比 maximin 保守度低；四准则并列比对才见稳健性**：一手定位（MetricGate）「canonical compromise between the pessimistic minimax loss criterion and a Bayes rule with a uniform prior」。四准则谱系：maximin（Wald，best-of-worst，最悲观）／maximax（最乐观）／**minimax regret**（后悔规避的中间派）／Laplace（无信息即等概率→算均值）。农技实例（UMN ageconsearch PDF 逐字）：扩建谷物升降机——maximax 选扩建、maximin 选不扩建、minimax regret 选扩建（最大后悔 0.484M < 不扩建 0.621M）、EMV 选扩建，四准则三比一指向扩建。Hurwicz 系数 α 线性混合最好与最坏收益（α=0→maximin、α=1→maximax），可做乐观度敏感性扫描。⇒ 报告模板固定四准则结论并列 + Hurwicz α 扫描；四者一致才判「对决策哲学稳健」，分歧则显式标记为「真实的风险偏好权衡，需人拍板」，不替用户选（与 §决策红线一致）。

- **r768C-3 ★它有一条硬伤（违背无关选项独立性），且「有概率时还用」会无谓保守；深不确定另有 RDM 框架**：一手指出主理论弱点（MetricGate/PMC8898502）「Adding or removing a state/action can change which action is chosen」——违背 independence of irrelevant alternatives，因后悔值依赖每状态的最大收益、增删行动会改动它。⇒ 用法上必须配敏感性输出：比较增删一个边际状态前后的排序是否翻转。适用边界（RAND、Annual Review of Resource Economics）：适用于「无可靠先验的新市场进入、一次性基建、novel 政策、对抗自然」等 Knightian 场景；「When reliable probabilities are available, expected utility maximization is generally more powerful」，深不确定下还用 minimax regret 会 unnecessarily conservative。更完整的深不确定框架是 RDM（Robust Decision Making，Lempert 2019 五步：decision framing→跨 future 评估→vulnerability analysis→tradeoff analysis→new futures/strategies），用 exploratory modeling + 全局敏感性分析找「在很宽情景集上都还行」的策略，而非对某个 most-likely 情景最优；max-min 常过保守、min-max regret 保守度较低（Annual Review 逐字「max-min method … often too conservative. The min-max regret method is less conservative」）。⇒ minimax regret 是 RDM 家族里的一个准则，不是全部；先判「有无可信概率」再选工具：有→EU/EVPI（§十五），无且要稳健→后悔准则/RDM，别把两者混用。

**来源（r768C 独立实拉 2026-11-19，≥2 独立域一手交叉）**：
- `https://www.rand.org/content/dam/rand/pubs/rgs_dissertations/RGSD300/RGSD340/RAND_RGSD340.pdf`（RAND《Strategies for Managing Sovereign Debt: A Robust Decision Making Approach》一手 PDF 全文逐字）— Savage 1951 min-max regret 定义与公式、Wald max-min、deep uncertainty 第四象限、Gilboa-Schmeidler max-min expected utility、Info-Gap、robust satisficing。**第一独立域·智库一手**。
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC8898502/`（PMC8898502《Multi-attribute COVID-19 policy evaluation under deep uncertainty》WebFetch 一手逐字）— RDM 五步框架、regret(Savage 1951)与 minimax regret 在 RDM 中的位置、tail risk 下的用途、MCDA/MAUT 对比。**第二独立域·论文一手**。
- 交叉快照（不冒充一手全文）：`https://metricgate.com/docs/minimax-regret-rule`（后悔=机会损失、对概率不变、纯 maximin 与 Laplace Bayes 之间的 compromise、IIA 违背、四准则并列与 Hurwicz、敏感性输出逐字）· `https://metricgate.com/docs/savage-minimax-regret`（R_ij=max_k V_kj−V_ij、每列至少一格为0、admissibility 支配剪枝、Bayes risk 对照逐字）· `https://ageconsearch.umn.edu/nanna/record/55465/files/09-17.pdf`（UMN 谷物升降机四准则实例：maximax/maximin/minimax regret/EMV 结论对照、后悔矩阵 0.484M vs 0.621M 逐字）· `https://resource.annualreviews.org/content/journals/10.1146/annurev-resource-121624-104610`（Annual Review：max-min 常过保守、min-max regret 较少保守、IAM 气候政策应用逐字）· `https://ce.arizval.com/civil/engineering-management/02-decision-making/content`（payoff matrix 准则须先声明、EV 不捕捉风险态度逐字）· `https://themba.institute/quantitative-analysis-for-managerial-applications/other-approaches-for-decision`（Hurwicz α 混合、Laplace 等概率、α 敏感性扫描交叉）· `https://www.numberanalytics.com/blog/minimax-regret-explained-game-theory-deep-dive`（与 EU 数学对照、线性规划/蒙特卡洛求解交叉）。
- **判非 / 去重**：`minimax regret` / `最小最大后悔` / `鲁棒决策` / `deep uncertainty` 全库 SKILL.md **0 命中**（初判相关串经核分散在 §十五 VOI 四把尺、§十九前景理论、PDI conformal 覆盖率，均异命题）；`regret` 在 agent-evolution §16 是 bandit online regret 最小化（异命题，WB 本章首次落地 minimax regret 作为无概率决策准则）。与 §十五 EVPI/EVSI（有概率才成立）、§十八影响图（结构可视化）、§十九前景理论（权重不稳）逐条分工，均不并存。与 r767/r766/r765 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：minimax regret 的混合策略线性规划求解、admissibility 支配剪枝的完整算法、Info-Gap 的 robustness function 数学、Gilboa-Schmeidler max-min expected utility 公理、RDM 的 exploratory modeling 具体实现（建模细节与异命题，留给后续）。

## 二十一、全局敏感性分析：在决策模型的诸多不确定输入里，谁真正驱动结果波动（r772C 独立实拉 2026-11-19，≥2 独立域一手交叉，3 独点）
> §十五 VOI 回答「该不该再收集信息」，但没有回答「先收集哪一个」；§二十 RDM 用 exploratory modeling 找稳健策略，其 vulnerability analysis 也要靠敏感性分析定位脆弱假设。本章补的是这个前置环节：**当决策模型有 k 个不确定输入时，用全局敏感性分析（GSA）把所有输入一起在其分布上变动，量化每个输入对结果波动的贡献，从而分清"该优先搞清的少数"与"可以直接固定的多数"**。
- **r772C-1 ★OAT 在非线性/有交互模型里会系统性漏判，十维一次一动留下 >99.75% 输入空间没探索**：一手逐字（healtheconomics.wiki 引 Saltelli 2019）「moving factors one at a time in ten dimensions leaves over 99.75% of the input space unexplored」，且局部导数「a valid measure only when the model is linear」——对 Xi 非线性时导数随取点变、输入间有交互时导数随其他输入值变；OAT 共享此缺陷，因为每次只动一个、其余固定，故**看不到交互**（一个输入的影响依赖于另一个输入的取值）。GSA 则让所有输入同时在其分布上变动，所以其指数能捕捉交互、并按"输入自身有多不确定"加权。更隐蔽的坑：不加权不确定性的排序会错——一个模型对某输入极敏感但该输入范围很窄时，它其实不是波动主因；GSA 的方差分解把"模型敏感度"与"输入不确定性"两者都计入。⇒ 决策模型做敏感性前先问：模型是否非线性、输入是否交互——只要有一条成立，OAT/单因素扰动就不能作为"谁重要"的结论依据。
- **r772C-2 ★Morris 筛选（便宜、定性）与 Sobol 方差分解（贵、定量）是两步，不是二选一**：两类方法按目的分工。Morris（elementary effects）：把每个输入离散成 levels，从随机点反复做 OAT 步长，得 elementary effect `E_j^i=[f(X^i+Δe_j)−f(X^i)]/Δ`，用 μ*（绝对值均值，衡量影响力）与 σ（标准差，标记非线性或交互）概括；r 次重复、d 个输入需 r(d+1) 次运行（r 常 4–10），便宜，主用于 **factor fixing**（低 μ* 与低 σ 的输入可在任意点固定）。σ/μ*>1 表示强交互/非线性（Nature 尾矿坝实例五参数全 >1 ⇒ 单因素法完全失效）。Sobol（variance-based）：无需线性/单调假设，把输出方差分解为各输入及交互项，一阶 `S_i=Var_Xi[E(Y|Xi)]/Var(Y)`（固定 Xi 可消除的方差份额），总效应 `S_Ti`（含所有涉及 i 的交互），**交互份额 = S_Ti − S_i**；Saltelli 设计两簇指数要 `N(k+2)` 次运行、N≥500（Nature 实例 N=2048、k=5 → 24,576 次），故工程上常先用 Morris 降维再对少数关键输入做 Sobol（Morris 可比 Sobol 省至多两个数量级）。S_i 高≈S_Ti 判"主效应加性"，S_i 低但 S_Ti 高判"只通过交互起作用、不能固定"。⇒ 报告固定两栏：输入 ×（μ*,σ）或（S_i,S_Ti,交互份额），并写明运行预算 r(d+1) 或 N(k+2)；结论分"factor prioritisation（优先搞清）"与"factor fixing（可固定）"两类，不要混为一谈。
- **r772C-3 ★GSA 结果条件于你给的分布，且"方差占比大"不等于"值得研究"——后者是 VOI 的判据**：三条边界逐字（healtheconomics.wiki 引 Saltelli 2010）：①「Every global result is conditional on the input distributions supplied, so an input given an arbitrarily narrow range ranks low even when the model responds strongly to it」——人为给窄范围会把强影响输入排低，排名只在所设不确定性空间内成立；②经典 Sobol 分解假设输入独立，相关参数要分组或用 Shapley effects，估计带 Monte Carlo 误差需对样本分块 bootstrap 给置信界；③最关键——「a large variance share also says nothing about research value unless resolving that uncertainty could change the decision」，Oakley & O'Hagan 证明平方误差损失下方差测度恰等于该组输入的完美信息期望值（接 §十五 EVPPI），但"一个输入即使占很大方差，若其任何合理取值都不改变最优选项，就无决策价值"。⇒ 决策落地顺序：GSA 先分清"哪些输入驱动波动"（factor prioritisation/fixing）→ 对关键输入接 §十五 VOI/EVPPI 判"搞清它值不值"→ 深不确定下再接 §二十 RDM 找稳健策略；GSA 给的是"看哪里"，VOI 给的是"值不值得看"，RDM 给的是"看不清时怎么选"，三者串联不互相替代。

**来源（r772C 独立实拉 2026-11-19，≥2 独立域一手交叉）**：
- `https://healtheconomics.wiki/concept/global-sensitivity-analysis`（HealthEconomics.wiki GSA 词条 WebFetch 200 全文逐字）— Saltelli 2019 定义、OAT 十维 99.75% 未探索、局部导数仅线性有效、Morris elementary effect 与 μ*/σ、Sobol S_i 公式与 S_Ti−S_i 交互、factor prioritisation vs fixing、N(k+2) 与 N≥500、输入分布条件性/相关输入/Monte Carlo 误差/Oakley-O'Hagan 研究价值。**第一独立域·一手百科**。
- `https://www.nature.com/articles/s41598-026-71253-3`（Nature Scientific Reports 尾矿坝滑动距离预测 WebFetch 摘要逐字）— Morris μ* 定主因、σ/μ*>1 判强交互非线性单因素法失效、Sobol Saltelli N=2048×2k+2=24,576 次、ΣS1=0.3596 而交互占 64.04%、S_Ti 与 S_i 分工实证。**第二独立域·期刊论文一手**。
- 交叉快照（不冒充一手全文）：`https://skillmd.com/skills/tools-only/sensitivity-analysis-guidelines`（SkillMD 方法分类表：Local OAT / Morris / Sobol 成本、μ*/σ 四象限、S_i 与 S_Ti 交互解读、Saltelli 采样数表）· `https://iris.unitn.it/retrieve/handle/11572/418690/796421/Di_Santo_PhD_thesis%20(25).pdf`（特伦托大学博士论文：Morris OAT 局限、Sobol 方差分解、Morris 作 Sobol 前置省两数量级）· `http://iris.unipa.it/retrieve/handle/10447/101163/131251/Mannina%20et%20al_iemss2014_207.pdf`（巴勒莫大学：μ* 因子固定、S_i/S_Ti 交互、相关因子分组）。
- **判非 / 去重**：`全局敏感性分析` / `Sobol` / `Morris 筛选` / `一阶效应` / `总效应` / `因子固定` 全库 SKILL.md **本体 0 命中**（初判命中串分散在 ci-context 配额、agent-guild 安全策略等异命题）。与 §十五 VOI/EVPI/EVPPI（该不该收集信息）、§二十 RDM/minimax regret（深不确定怎么选）逐条分工——那两章管"要不要查/怎么选"，本章管"先查哪个输入、哪些可直接固定"；与 §十六 AHP 权重敏感性（准则权重微调看排序翻转）不同层——那是单一方法内的稳健性检查，本章是对决策模型全部不确定输入的系统方差分解。与 r771/r770/r769 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：Shapley effects 处理相关输入的数学、Sobol 各阶指数的 Jansen/Saltelli 估计量推导、Morris 轨迹采样设计、DTAR 等 moment-independent 方法（建模细节与异命题，留给后续）。

## 二十二、实物期权：当决定不可逆且环境高波动，「等待/扩张/放弃」本身是有价的权利（r776C 独立实拉 2026-11-19，≥2 独立域一手交叉，3 独点）
> §十三「双向门」管「可逆性决定流程权重」，但只给了启发式（pilot/phasing/exit clause），没有给「灵活性值多少」；§十五 VOI 管「再调研值不值」。本章补的是：**当投资不可逆、不确定性高时，把「未来还能改主意」这件事当期权定价，它可能是 NPV 之外的正价值**。
- **r776C-1 ★传统 NPV/DCF 假设「now-or-never + 被动持有」，实物期权给「管理灵活性」定价：Project Worth = NPV + Value of Options**：LibreTexts 官方教材逐字「Traditional capital budgeting techniques such as NPV, IRR, and PI assume that investment decisions are now-or-never: the firm either accepts or rejects a project today and then passively receives future cash flows」「Real options analysis recognizes that many investment projects contain managerial flexibility—the option to delay, expand, contract, abandon, or modify a project in response to new information」「This flexibility has value, especially in uncertain environments, and is often ignored by standard NPV analysis」。Investopedia 逐字「A real option gives businesses the flexibility to adjust their investments or projects in response to changing economic or market conditions」「the right, but not the obligation」。⇒ DI 落地：对高风险/不可逆选项，决策日志在 NPV 之外单列「本案保留了哪些后续权利（延迟/扩张/放弃/转换）」，它们可能是把「拒绝」变成「接受」的那一项；例（researchlab.pk 教学例）初始 NPV −$3M，50% 概率市场增长下扩张期权加 $5.5M 期望价值 ⇒ 项目价值 +$2.5M ⇒ 接受。
- **r776C-2 ★不确定性与价值的关系在传统 DCF 和实物期权里方向相反**：传统 DCF 里风险↑→折现率↑→NPV↓；实物期权里「greater uncertainty can increase project value when flexibility exists」「Upside outcomes can be pursued aggressively. Downside outcomes can be limited through abandonment or delay. As a result, uncertainty creates opportunity, not just risk」（LibreTexts §9.6.4）。ScienceDirect 实证（《Managerial flexibility, uncertainty, and corporate investment》）逐字「irreversibility creates an option value from waiting for the arrival of new information」「increased uncertainty reduces the amount invested ... due to an options value from waiting」，且该负效应在财务约束少、规模大的企业更明显（灵活性代理）。⇒ 落地：不要一见「不确定性高」就只调高折现率；先问「本案能否通过等待/分阶段把不确定性消解后再决定」，若能，不确定性可能是正价值而非纯扣分项；但不能反过来说「不确定性总是好事」——Investopedia 明写「ROV is applicable only when ... sufficient information flow, and sufficient funds to cover potential downside risks」。
- **r776C-3 ★期权是一组具体权利不是一句口号，估值既借金融期权术语又须承认主观性**：三类（Investopedia）—①项目规模：扩张/收缩；②项目寿命：启动/延迟/放弃/排序分阶段；③运营：工艺柔性/产品组合/运营规模；LibreTexts 另列 switch（换投入/产出）。估值映射：标的价格≈项目 NPV、行权价≈不可回收成本、到期≈决策时限、波动率≈风险；方法含二叉树、Black-Scholes、Monte Carlo（Investopedia；Aberdeen 油田论文用 binomial lattice 与 Black-Scholes 对延迟/扩张/放弃定价，报「DCF values lag those of the option values for the deferral and expansion options, ... abandonment option exhibited only a marginal change」）。但必须同时报主观性：「real options analysis is still often considered to be a heuristic」「the choice of the model itself is based on judgment and often a trial-and-error approach」「objective values cannot be mathematically determined with any degree of certainty」（Investopedia）。⇒ 落地：决策记录写「期权类型（哪一类）+ 行权触发条件（看到什么信号才扩张/放弃）+ 估值方法 + 主观性声明」四栏；不确定下用情景/区间而非单一 ROV 数，并注意「放弃期权对价值改变可能很小」这种实证反例（不是每个期权都值钱）。
**来源（r776C 独立实拉 2026-11-19，≥2 独立域一手交叉）**：
- `https://www.investopedia.com/terms/r/realoption.asp`（Investopedia 词条 WebFetch 200 全文逐字，Updated 2026-04-24）— right but not obligation、三类权利、NPV≈spot/不可回收成本≈strike/决策时限≈expiration、Monte Carlo、heuristic 主观性、适用与不适用条件。**第一独立域·金融教育一手**。
- `https://biz.libretexts.org/Courses/Aurora_University/Principles_of_Financial_Management/09%3A_Capital_Budgeting/9.06%3A_Real_Options_in_Capital_Budgeting_Overview`（LibreTexts 大学教材 WebFetch 200 全文逐字）— now-or-never 假设、delay/expand/abandon/contract/switch 五类、A vs B 项目例、uncertainty↑抬高价值、NPV 的 conceptual complement not replacement。**第二独立域·教材一手**。
- 交叉快照（不冒充一手全文）：`https://www.sciencedirect.com/science/article/abs/pii/S1059056008001275`（ScienceDirect 摘要逐字，irreversibility/等待期权价值/不确定性抑制投资与灵活性代理）· `https://blog.researchlab.pk/?p=524`（Project Worth=NPV+Value of Options 教学例与三类期权整理）· `https://abdn.elsevierpure.com/en/publications/on-the-valuation-of-natural-resources-real-options-analysis-of-ma`（Aberdeen 油田 ROA 论文摘要逐字延迟/扩张/放弃期权对比）。
- **判非 / 去重**：`实物期权` / `real options` / `管理灵活性` / `ROV` 全库 SKILL.md 本体 0 命中。与 §十三 双向门（可逆性定流程权重，给的是 pilot/phasing/exit clause 启发式）、§十五 VOI/EVPI（调研信息值不值）、§二十 minimax regret（无可信概率怎么选）、§二十一 GSA（先看哪个输入）分工：那四章管「要不要查/怎么选/先看哪里」，本章管「把未来可调整的权利本身当资产定价」。与 r772C GSA、r768C minimax regret 不复用。
- 豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地。与 r775/r774/r773 九模块结论不复用。
- **未采纳**：Black-Scholes 在实物期权上的完整推导、二叉树格点定价数学、跳跃扩散与随机利率扩展（建模细节，留给后续）。

## 二十三、参考类预测：用同类历史结果的分布，替掉「我们这个项目不一样」的自估（r780C 独立实拉 2026-11-20，≥3 独立域一手交叉，3 独点）
> §十九前景理论管「参照点与框架怎么让偏好翻转」，是描述性偏差；本章管一个直接可用的去偏差程序：**当团队从本项目细节自底向上估成本/工期/收益时，强制先把同类项目的实际结果分布当基准，再允许有证据的偏离**。它落在决策前的输入校准层，不改 MCDA/VOI 的排序逻辑。
- **r780C-1 ★三步法与「先定参考类再看它指向哪里」的纪律**：三方一手一致（Wikiwand/Kahneman-Tversky、GovLoop/Flyvbjerg、becisions）：①识别一组过去的相似项目；②为要预测的参数建立这组项目的概率分布；③把当前项目放进该分布定位最可能结果。GovLoop 的 Flyvbjerg 版本补两条：样本「must be large enough to be statistically meaningful, but narrow enough so that the parameters closely match your planned project」；调整顺序是「First: Base Rate Then: Case-Specific Adjustment Not the reverse」，且必须是「Evidence-Based not Confidence-Based Adjustment」。Edinburgh Tram Line 2 实证（Wikiwand）：原估 £320M 含 25% 应急，RCF 算得 P80=£400M（57% 应急）/P50=£357M（40%），实际 2014 年开通晚三年、终值 £776M。⇒ 决策日志在自估之外固定三栏：参考类是什么/样本量多少/基准分布的中位数与 P80；没有参考类的成本工期估计按「未做外部视角校准」标注。
- **r780C-2 ★偏差有三类，RCF 只直接治第一类，后两类要靠 Governance**：一手期刊（Taylor & Francis 2025 研究议程）逐字区分：optimism bias（「a cognitive predisposition ... to judge future events in a more positive light than is warranted by actual experience」）/ uniqueness bias（「our project is different」致拒绝考虑分歧信息）/ strategic misrepresentation（「the deliberate distortion of information to steer a decision ... in the direction the advocate supports」）。Kahneman-Tversky 的原始机制是 inside view「focus is on the constituents of the specific planned action instead of on the actual outcomes of similar ventures」+ 忽略 distributional information；Flyvbjerg&Sunstein 把低估成本/时间/风险+高估收益称「planning fallacy writ large」。⇒ 报告「已用 RCF 去偏差」不能顺便宣称也防了Strategic misrepresentation——后者是激励问题，RCF 的 uplift 反而会被「故意先报低、等上调」利用（期刊原文：「project sponsors may intentionally set lower initial estimates knowing that later uplifts will increase the budget」）。
- **r780C-3 ★参考类选择本身是决策，且 RCF 的实测收益有条件、不是无条件更好**：「reference class tennis」问题（Wikiwand）：写心理学教材该取全部书/全部教材/只取心理学教材，越窄越接近 inside view、越宽样本越大但可比性越差；期刊逐字「If the reference class is too broadly constituted, it will not allow for accurate comparisons, while too narrowly selected and the resulting class would be too small to permit statistical smoothing」，且「RCF only outperforms EVM and Monte Carlo simulation when the degree of similarity ... is sufficiently high」。另有硬边界：罕见项目类型（核电站）凑不到足够样本、企业不愿披露敏感数据；批判性研究指出「clear evidence for the existence of optimism bias ... was mixed」、某丹麦大型公共项目纵向案例「the use of RCF did not improve the accuracy of cost estimates」，且「risk and uncertainty」被混同——历史分布可量化风险，unknown-unknowns 无法事后平滑。⇒ 落地：参考类须在看到它指向哪个结论之前冻结（防 reference class shopping / 幸存者偏差），先写纳入排除标准；报 RCF 结论同时报相似度、样本量、是否被操纵的可能与 uplift 依据，禁把「做了 RCF」当「成本Estimate已校准」。
**来源（C 独立实拉 2026-11-20，≥3 独立域一手交叉）**：
- `https://www.tandfonline.com/doi/full/10.1080/09537287.2025.2578708`（《Reference class forecasting: promises, problems, and a research agenda moving forward》WebFetch 200 全文逐字）— 三类偏差定义、inside/outside view、UK/Denmark 强制采用、参考类太宽/太窄、相似度门槛、罕见类型与披露问题、乐观偏差证据 mixed、丹麦纵向案例无改善、risk vs uncertainty、RCF 可被操纵。**第一独立域·期刊论文一手**。
- `https://www.wikiwand.com/en/Outside_view`（Outside view / Reference class forecasting 条目，WebFetch 失败；以 WebSearch 返回的一手全文逐字登记，不冒充 WebFetch 成功）— Kahneman-Tversky 发现、RCF 三步、reference class tennis 教科书例、Edinburgh Tram £320M/P80 £400M/P50 £357M/终值 £776M。**第二独立域·百科一手（降级登记）**。
- `https://govloop.com/have-you-fallen-victim-to-the-planning-fallacy`（GovLoop WebSearch 逐字）— 厨房改造 $18,658 预期 vs $38,769 实际、outside view 定义、Flyvbjerg 三步与样本「large enough but narrow enough」。**第三独立域·政策实践一手**。
- 交叉快照（不冒充一手全文）：`https://signalb4noise.com/en/reference-class-forecasting-strategic-decisions`（三步、P20–P90 超支分布表、Decision Sheet 十二栏、reference class shopping 幸存者偏差、均值不是决策数要用 P80/P90 配风险偏好）· `https://becisions.com/dictionary/terms/reference-class-forecasting`（outside view 替代 inside view、规划谬误与乐观偏差、选择参考类与诚实数据之难）· `https://probsee.com/p/Reference_class_forecasting`（base-rate neglect 起源、学生论文 34 天预估 vs 55 天实际、超支从 >30% 降到 <10%）。
- **判非 / 去重**：`参考类预测` / `reference class forecasting` / `planning fallacy` / `outside view` 在 DI 技能正文 0 命中；全库命中在 `meta/pdi-forecasting` §二表「参考类基率」一行（预测流程的基率步骤，异命题——本章管决策输入去偏差与参考类选择的治理）与 `meta/ti-critical-reasoning` 判非句里 base rate 一次提及。按去重铁律取「优＝加厚现有」落 DI 唯一技能，不改 PDI/TI。与 §十九前景理论（描述性偏差）、§十三双向门（可逆性定流程）、§二十 minimax regret/RDM（无可信概率怎么选）逐条分工。与 r779 三轮结论不复用。
- **未采纳**：RCF 与 EVM/Monte Carlo 的混合模型数学、uplift 货币化与风险缓解的定量权衡、超级预测者整合 base rate 的实证细节（建模细节与异命题，留后续）。

## 二十四、博弈论决策：当结果取决于他人怎么回应，单人加权矩阵就是框架错配（r784C 独立实拉 2026-11-20，≥2 独立域一手交叉，3 独点）
> §十二管「多人偏好怎么聚合成社会序」（社会选择/Arrow），本章管「对方会根据我的选择做最优回应」的策略互动——前者聚合给定偏好，后者把回应内生化。§十八影响图"未采纳"里 game tree 一句被本轮按不同粒度取用（策略互动判据，非影响图求解细节）。
- **r784C-1 ★先分四轴再选解概念，占优≠最优回应，Nash 是"无人能单方改进"不是"大家好"**：四轴逐字（fiveable/theeconprofessor）：同时 vs 序贯、合作 vs 非合作、零和 vs 非零和、完全 vs 不完全信息。占优策略"consistently outperforms other strategies regardless of opponents' choices"（fiveable 逐字）；best response 是给定他人策略下最大化自己收益，与占优不同。Nash 均衡逐字："no player can improve their payoff by unilaterally changing their own strategy, assuming all other players keep theirs fixed. In other words, each player's strategy is a best response to the strategies of the others."（theeconprofessor）；"Nash proved that every finite game has at least one Nash equilibrium, though it may involve mixed strategies"，多均衡时协调成为问题（Battle of Sexes）。⇒ 决策日志在跑 MCDA 前先写「对手是谁/同时还是序贯/能否签约束协议」，有策略依赖却用单人加权打分=框架错配。
- **r784C-2 ★混合策略的反直觉规则与序贯博弈的不可信威胁剔除**：混合均衡里"each player's probabilities are chosen to make the opponent indifferent between their pure strategies ... my probabilities are pinned down by your payoffs, not by mine"（econtutorials WebSearch 逐字，Matching Pennies p=½ 推导），随机化用于不可预测（bluffing/deterrence）。序贯用逆向归纳从终局倒推，得子博弈精炼均衡 SPNE——"a strategy profile that constitutes a Nash equilibrium in every subgame, including subgames that are never reached in equilibrium"（Selten 1965，econtutorials 逐字）；进入威慑例（在位者容纳 5/5、价格战 −2/−3）"The threat was never credible. Nash equilibrium tolerated a threat no rational player would carry out; subgame perfection rules it out"（econtutorials 逐字）。theeconprofessor 逐字补"Sequential games ... are analyzed using backward induction ... subgame perfect equilibria, which refine Nash equilibrium by eliminating non-credible threats"⇒ 报"对手威胁/承诺"先过 SPNE 筛不可信项，不把口头威胁当既定约束。
- **r784C-3 ★承诺=主动毁掉自己选项把不可信威胁变可信；有限重复会倒推瓦解合作**：Schelling《The Strategy of Conflict》(1960)"a player can gain enormously by destroying their own options. Burn the bridge behind your army, and retreat becomes impossible ... Your loss of freedom is the source of your power"；经济例子=过剩产能/违约罚金/ sunk cost into high-output technology，"Each of these changes the payoffs in the subgame, converting a non-credible threat into a credible one"（econtutorials WebSearch 逐字）。有限重复反向归纳：round 100 无未来双背叛→round 99 同理→全背叛，"Selten's chain store paradox (1978) ... A known endpoint destroys cooperation all the way back to the beginning"（econtutorials 逐字）；重复博弈才可能靠未来惩罚维持合作。⇒ 决策记录固定写「我能否可信承诺/毁掉哪些退路/博弈是否有明确终点」，有终点就要预期合作倒推瓦解。
**来源（r784C 独立实拉 2026-11-20，≥2 独立域一手交叉）**：
- `https://library.fiveable.me/microeconomic-analysis-for-business-decisions/unit-9/basic-concepts-game-theory/study-guide/CKAIKnAZV4QFEr52`（WebFetch 200 全文逐字）— players/strategies/payoffs、占优定义、混合策略、SPNE 精炼序贯 Nash、backward induction 从尾到头、合作/非合作、Shapley/Nash bargaining/core、CKR/贝叶斯均衡。**第一独立域·一手教学页**。
- `https://theeconprofessor.com/understanding-game-theory-a-beginners-guide-to-economic-decision-making`（WebFetch 200 全文逐字）— Nash 定义与每有限博弈至少一均衡（可混合）、混合策略不可预测用于 bluffing/deterrence、序贯用逆向归纳与 SPNE 剔不可信威胁、零和/非零和、完全/不完全信息。**第二独立域·一手教学页**。
- 交叉快照（WebSearch 逐字，WebFetch 被 Cloudflare 拦如实登记）：`https://econtutorials.com/game-theory-introduction/`（混合策略"我的概率由你的收益定"、Matching Pennies p=½、SPNE Selten 1965 定义、进入威慑不可信威胁、Schelling 承诺毁退路、chain store paradox）· `https://www.pearson.com/channels/ko-kr/microeconomics/study-guides/game-theory-and-strategic-decision-making-microeconomics`（占优/SPNE/可信威胁 sunk cost）· `https://www.codartium.com/strategic-interaction-and-game-theory-in-managerial-economics`（承诺与可信性、先手后手效应、战略互补替代）。
- **判非/去重**：`纳什均衡`/`Nash equilibrium`/`逆向归纳`/`backward induction`/`占优策略`/`可信承诺`/`subgame perfect` 全库 SKILL.md 本体 0（agent-evolution §r741C 命中是 performative prediction 的 Nash/Stackelberg 反馈均衡、异命题；DI §十八来源句仅"game tree 扩展"一句、§十八未采纳仅提"game theory 扩展形式博弈建模"，均非本体）。与 §十二社会选择、§十八影响图、§二十深不确定准则分工。豆包自留地 WB 0 落地。
- **改了就删**：§十八未采纳中"game theory 扩展形式博弈建模"一句，本轮按"策略互动判据"粒度取用（非影响图求解），不删除该未采纳（它说的是影响图求解细节，仍有效）。
- **未采纳**：Shapley 值公理化推导、机制设计/拍卖最优性、重复博弈 folk theorem 完整条件、贝叶斯博弈均衡求解细节（建模细节与异命题，留后续）。
## 二十五、效用函数 elicitation：先把「风险态度」问出来，再谈期望效用最大化（r788C 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）
> §八算 EU/EVPI、§十五算信息价值四把尺——它们都**假设效用函数已知**；本章管更前置的一步：**决策者自己的效用函数怎么测出来**。跳过这步直接用金额/人数当量代效用，等于把"风险态度"偷偷设成线性（风险中性），在涉及生死/大额不可逆的决策里框架就错了。
- **r788C-1 ★三种 elicitation 问法相同点不同：标准赌局变概率、确定等价变金额、权衡法消概率权重**：标准赌局（vNM）逐字（unict MCDA 综述）："what probability p would make you indifferent between receiving x amount for certain and a lottery, where you receive 100,000 dollars (max) with probability p and nothing with probability (1−p). Then, the indifference probability p is simply u(x). Then, we repeat the exercise for a number of other x-values (typically 5–7)."；50-50 变体："What is the sure payoff x for which you would be indifferent between a lottery that gives a 50%–50% chance to 100,000 and 0 and the sure payoff x? ... u(x)=0.5×u(100,000)+0.5×u(0)"；硬约束："the branches must be chosen so that the utilities of the corresponding consequences are known"。确定等价（CE）逐字（Myerson）："U(CE)=E(U(X))"，固定赌局问"多少确定金额与它等效"；SEP 逐字：风险规避判据"CE(X)<EU(X)，风险中性 CE=EU，风险寻求 EU<CE"，50-50 中 10 utiles/0 值 5 utiles、若 3 utiles 确定即无差异则是 risk averse。权衡法（TO，FDA 评论逐字）："robust to distortions in probability perception, because the same probability p is used on both sides of the indifference, the weight of the probability cancels out"。⇒ 决策日志写效用时须注明用哪种问法、p 或 x 的无差异点、5–7 个锚点是否齐。
- **r788C-2 ★曲线凹性=风险态度，且同一个人不同健康/财富水平态度相反**：凹（log）风险规避、凸风险寻求、直线风险中性（ejsei/SEP 逐字）；Arrow-Pratt 测度逐字（SEP）："the agent's risk aversion at any point x is equal to −u″(x)/u′(x)"，且"invariant under transformations of the utility function that preserve the preference relation (multiplication by a positive constant and addition of an arbitrary constant)"——效用只到正仿射变换唯一，绝对值无意义。FDA 评论逐字："individuals tend to be risk-seeking at low levels of health or survival and risk-averse at high levels. Gravely ill patients with few options often prefer a long-shot therapy, whereas healthy patients ... prefer safe bets." ⇒ 不能给决策者贴"你就是风险规避"的固定标签，须按结果水平分段问；概率轮（probability wheel）逐字（Lippincott）用于"minimizing cognitive biases that accompany the elicitation of percentages"。与 §十九前景理论分工：前景理论描述"参照点移动导致框架翻转"的**偏差**，本节能动地**测出**基准效用曲线供 EU 使用，二者互补不并存。
- **r788C-3 ★多属性效用的加性形式要过独立性门槛，否则须换乘性**：加性逐字（unict）："U(x1,…,xn)=k1·u1(x1)+…+kn·un(xn), k_i>0, Σk_i=1"，成立需两条件"(1) the criteria are mutually preferentially independent, and (2) ... additively independent"；若只满足 mutual utility independence 则用乘性形式"U=(∏(1+k·k_i·u_i)−1)/k，k>−1 且 k≠0，1+k=∏(1+k·k_i)"（Keeney & Raiffa 1976 给出独立性检验操作）。常风险容忍简化逐字（Myerson）："U(x)=−EXP(−x/τ)，τ 是风险容忍常数；只要测一个简单赌局的 CE 就能算出 τ，之后任意复杂赌局的 EU/CE 都可估"——但这是"常数风险容忍"假设下的便利，非普适。⇒ 决策日志用加权和前先问"准则是否偏好独立/加性独立"，不满足却仍用加权和是把乘性交互硬拍平；与 §六 MCDA 加权、§r733B 补偿性决策分工：那里给"补偿 vs 非补偿"的结构，这里给"效用值本身从哪来"。
**来源（r788C 独立实拉 2026-11-22，≥2 独立域一手交叉）**：
- `https://plato.stanford.edu/entries/risk/`（WebFetch 200 全文逐字）— 期望效用定义、CE/EU 风险态度判据、凹性/凸性、Arrow-Pratt −u″/u′ 与正仿射不变性、50-50 10 utiles 例。**第一独立域·一手百科**。
- `https://home.uchicago.edu/rmyerson/teaching/util206.pdf`（WebSearch 全文片段逐字）— U(CE)=E(U(X))、vNM 1947 论证、常风险容忍 U(x)=−EXP(−x/τ)、单赌局 CE 定 τ、独立赌局 CE 可加。**第二独立域·一手教材 PDF**。
- 交叉快照（WebSearch 逐字，WebFetch 被 Cloudflare/CloudFront 拦如实登记）：`https://www.iris.unict.it/retrieve/...S0377221724005988-main.pdf`（MCDA 五十年综述：标准赌局 p=u(x)、5–7 x 值、50-50 CE 变体、分支已知效用、加性 U=Σk_i u_i 两独立条件、乘性形式与 k、Keeney&Raiffa 1976）· `https://ejsei.com/EJSE/article/download/55/54/62`（vNM 1944 必要充分公理、CE 法 U(C)=pU(A)+(1−p)U(B)、$0=0/$40000=1 与 $10000 给 50-50 得 U($10000)=0.5、凹/凸/线性风险态度）· `https://www.regulations.gov/comment/FDA-2025-D-3217-0008`（SG/CE/TO 三法逐字、低健康 risk-seeking 高健康 risk-averse）· `https://journals.lww.com/plasreconsurg/Fulltext/2014/10000/...`（标准赌局概率轮、u 值 0–1、风险偏好 u 曲线）。
- **降级如实登记**：unict PDF（Just a moment 拦截）、regulations.gov（CloudFront 403）、iris/ejsei WebFetch 均未取全文，以 WebSearch 逐字片段登记，不冒充 WebFetch 200；核心三独点由 SEP WebFetch 200 全文 + 多源逐字支撑。
- **判非/去重**：`效用函数 elicitation`/`standard gamble`/`certainty equivalent`/`Arrow-Pratt`/`多属性效用` 全库 SKILL.md 本体 0（§八 EU/EVPI、§十九前景理论、§六 MCDA 加权均异命题）。豆包自留地 WB 0 落地。
- **未采纳**：vNM 四公理（完备/传递/连续/独立）的形式化证明、多属性效用独立性检验的操作题设计、Savage 主观期望效用公理（异命题/建模细节，留后续）。

## 二十六、非补偿性排序 ELECTRE / PROMETHEE：一个准则差到不可接受，别的准则优异补不回来（r792C 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点；正文下沉 `references/r792C_非补偿性排序_ELECTRE_PROMETHEE.md`）：§六 MCDA 加权、§r788C 效用 elicitation 管「权重怎么定、效用从哪来」，本章管前置问题——**加权和默认可补偿，out ranking 默认不可**。选方法=选补偿逻辑（SINTEF 逐字），方法选择对结果影响可大过换决策者。**独点1** out ranking 假设 DM 不愿/不能给准则间 trade-off，故一准则的极差不能被另一准则极好补偿；out ranking relation 四态（A P B 严格偏好 / 逆偏好 / A I B 无差异 / **A R B 不可比**），不可比是一等输出不强行全序。**独点2** ELECTRE 走 concordance（多数准则支持）+ non-discordance（无准则强烈反对）双门槛、veto 可否决，ELECTRE III 有时排不出唯一最优（适合做短名单）；PROMETHEE 每准则定偏好函数 `P_i=F_i[d_i]∈[0,1]`、聚合 `π(a,b)=ΣP_i w_i`，PROMETHEE I 偏序图、**II 用净流 Φ=Φ⁺−Φ⁻ 给全序**，六种偏好函数可选。**独点3** 输出须附敏感性分析（权重/得分/阈值一微调排序可能翻），代价是要 elicitation 出 indifference/preference/veto 阈值（对 DM 常不直观）；与 §r788C 分工：那里测效用值本身，这里定能否用加权和的补偿结构。判重：ELECTRE/PROMETHEE/outranking/concordance/净流 全库本体 0，豆包自留地 WB 0 落地。**三独立域逐字来源 + 判非全段见下沉文件。**
## 二十七、决策滞后 hysteresis：单阈值必震荡，切换规则要有状态与滞回带（r795B 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）

§八 EVPI 管「该不该再调研」、§十五 VoI 四把尺管「买哪种信息」，本章管**执行层的切换决策**：在噪声信号下，「超过阈值就切」会因反复越线产生高切换成本，正确形态是带锁存状态的双阈值。

**独点1** 判据：实现必须含锁存状态——ON 条件 `PV≤T_low`、OFF 条件 `PV≥T_high`、带内 `state:=prev`；只有单一比较器 `PV vs T` 即判为必 chattering。CMU 讲义逐字：hysteresis 源于「internal state causes the output response to vary based on the history of the input」，双阈值使「small noise variations around a threshold level will not trigger a change」。

**独点2** 滞回带 `ΔH=T_high−T_low` 必须成对配置且 `T_high>T_low`；`ΔH` 要覆盖信号峰峰值噪声，并与最大允许切换频率联动。混合系统实现须让 flow 集 `μ≤δ` 与 jump 集 `μ≥δ` 重叠；边界无缝拼接时「噪声 ε<δ 不误切换」不成立（arXiv:1910.02026 逐字：hysteresis gap prevents chattering）。

**独点3** 决策记录须写明切换成本与滞回带取值理由；若策略切换、告警升降级、资源扩缩容只有一条阈值，判为「未计入切换成本」。与 §十五「单向/双向门」分工：门定流程与谁拍板，本条定状态机的上下界。

- **判重：`hysteresis`/`滞后阈值`/`双阈值` 本体全库 0；与 §八 EVPI、§十五 VoI、单向/双向门分工不复用。豆包自留地 WB 0 落地。**
- **来源与诚信**：https://courses.ideate.cmu.edu/16-223/f2018/text/ex/Arduino/input-hysteresis/input-hysteresis.html（CMU IDeATe 16-223，2018 秋，WebFetch 200 逐字：历史依赖定义 / light_threshold 高于 dark_threshold / 小噪声不触发）；https://arxiv.org/html/1910.02026（Casau 等，arXiv:1910.02026，2019-10-04，WebFetch 200 逐字：hysteresis gap prevents chattering / flow μ≤δ 与 jump μ≥δ 重叠）。无。`2–3×噪声` 一类具体倍数非一手来源给出，未写入。 逐字全文与判非见 `references/r795B_决策滞后.md`。
## 二十八、Cynefin 分域：先定因果可知性再选动作链（r796B · 全文下沉）

> 四域（Clear/Complicated/Complex/Chaotic）+ 第五域 Confusion + 四条动作链（sense-categorize-respond / sense-analyze-respond / probe-sense-respond / act-sense-respond）+ 域迁移条件 + Cynefin.io 与 OpenLearn 一手逐字与判非，全文见 `references/r796B_Cynefin.md`（23 行）。使用本方法时以该 references 为准，本节仅留路由，不内联正文。

## 二十九、心理账户：钱被分进不同账户，fungibility 就失效（r799A 独立实拉 2026-11-23，≥3 独立域一手交叉，3 独点）

§一前景理论管参照点与损失厌恶的**值函数形状**，本章管更前置的一层——**同一笔钱被放进哪个账户**，账户间的钱不可互换，规范上的 fungibility 在人的实际决策里失效。
**独点1** 交易效用与可替代性违反：Thaler 1985 把价格作为属性引入价值函数、价格成参照点；`TU=参照价−实付价`，总效用=获得效用+交易效用。四个经典案例（赢来的钱敢下注 vs 股票赚的钱弃牌、存 15k@10% 却贷 11k@15% 买车、自购嫌贵的羊绒衫做礼物则喜）都违反「同单位货币无差别」。判据：决策记录须分两栏写「这笔钱从哪个心理账户出」与「fungibility 下的机会成本应是多少」，二者相左即心理账户在起作用。
**独点2** 四 MAP 编码原则决定偏好方向：多收益分离 `v(x)+v(y)>v(x+y)`；多损失合并；混合收益（净收益）合并——银边原则让损失被收益吸收；混合损失看相对大小——损失远大于收益时分离、两者接近时合并。剧院票 10 美元实验：丢票 56% 不再买（该 10 计入「看戏账户」心理票价变 20），丢现金 88% 仍买（计入「丢钱账户」心理票价仍 10）。判据：同一组现金流在分离/合并两编码下翻转偏好即心理账户效应，方案必须写明编码方式，禁止把「分账户」当给定。
**独点3** 账户预算不可互替导致沉没成本误判：沉没成本本不该进决策，但账户划分阻碍识别；处置效应里 paper loss 不平仓＝账户未关闭、回避实现亏损的痛感。与 §一前景理论分工：那里管值函数形状与参照点移动，这里管钱如何分账户、账户间预算为何不能换；与 §十六诱导 / §十七 AHP 分工不复用。不防什么：描述性理论（人实际怎么错），不提供规范性分账户规则，不替代机会成本核算。
- **判重：`心理账户`/`mental accounting`/`交易效用`/`silver lining` 全库 SKILL.md 0 命中；`前景理论`/`损失厌恶` 命中本技能 §r762，分工见独点 3，不并存。豆包自留地 WB 0 落地。按 rules/07 判「增＝加厚现有」。**
- **来源与诚信**：https://dept.abcdef.wiki/wiki/Mental_Accounting（葡语维基词条，WebFetch 200 全文逐字：账户创建/剧院票 56% vs 88%/损失厌恶/文献）; https://theses.gla.ac.uk/7563/1/2016Agbatophd.pdf（格拉斯哥大学博士论文，WebSearch 逐字快照：四 MAP 公式与 silver lining/fungibility 违反）; https://erepo.uef.fi/bitstreams/c8539672-7485-4f9f-9daf-c3b0f0c73c27/download（东芬兰大学论文，WebSearch 逐字：87 学生 56 人/Thaler1999 定义/处置效应）; https://jjxdt.ajcass.com/Admin/UploadFile/20150323002/2018-04-04/Issue/2x5acvui.pdf（中国社科院引介，WebSearch 逐字：四案例/可替代性/交易效用）。格拉斯哥 PDF WebFetch 非文本、逐字取自搜索快照如实登记。 逐字全文与判非见 `references/r799A_心理账户.md`。