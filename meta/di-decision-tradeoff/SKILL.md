---
name: di-decision-tradeoff
description: 决策权衡分析（Decision Intelligence）。当用户面临 ≥2 个可行方案、需要在成本/收益/风险/可行性之间权衡、或要求"帮我选/对比/排优先级"时调用。提供加权决策矩阵、Pros&Cons 加权、Pre-Mortem、机会成本、ICE、RICE、Eisenhower、单向/双向门等框架，以及期望效用(EU)/信息价值(EVPI) 量化决策与"该不该再调研"停手线，输出结构化方案对比与推荐，绝不替用户做需授权的重大决定。
module: DI
modules: DI,TI
version: "1.4.0"
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
