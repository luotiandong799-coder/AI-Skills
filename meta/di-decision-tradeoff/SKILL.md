---
name: di-decision-tradeoff
description: 决策权衡分析（Decision Intelligence）。当用户面临 ≥2 个可行方案、需要在成本/收益/风险/可行性之间权衡、或要求"帮我选/对比/排优先级"时调用。提供加权决策矩阵、Pros&Cons 加权、Pre-Mortem、机会成本、ICE、RICE、Eisenhower、单向/双向门等框架，以及期望效用(EU)/信息价值(EVPI) 量化决策与"该不该再调研"停手线，输出结构化方案对比与推荐，绝不替用户做需授权的重大决定。
module: DI
modules: DI,TI
version: "1.7.0"
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
