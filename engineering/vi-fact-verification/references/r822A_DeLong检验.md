# r822A · DeLong 检验：两个 ROC AUC 的统计比较（VI · 2026-11-28）

> 主题：DeLong test / 相关 ROC 曲线下面积比较。与 §r810A Youden 指数（选阈值）、§r788B Bland-Altman（一致性）异命题——本章管「两个方法的 AUC 谁更高，差异是否超出抽样波动」。
> 实拉：MedCalc 官方书页 + PubMed 原论文摘要 + MedCalc 官方手册（三页 WebFetch 200 全文逐字），每轮 ≥2 独立域一手。

## 一、为什么必须做统计比较（MedCalc 官方书页逐字）

> "A new biomarker rarely enters clinical practice in isolation. It is almost always evaluated against an established test ... The question is not merely whether the new test is good in absolute terms; it is whether it is better than what already exists."
> "Visual inspection is not sufficient. Two ROC curves may cross, or one may appear to dominate only over a limited range of the false positive rate. Even when one AUC is numerically larger than the other, the difference could easily arise from sampling variability if the study is small."

两种设计（决定能否忽略相关性）：
- **Paired (dependent)**：两检验在同一批患者上做（如 120 例脓毒症患者同时测 CRP 与 PCT）。难分类患者两检验都会得分模糊 → **两 AUC 正相关**。
- **Independent**：两检验在非重叠的两组患者上评估，效率低、较少见（历史数据对比或伦理约束时出现）。

> "The distinction is critical because it determines whether the correlation between the two AUC estimates must be accounted for ... a correlation that, if ignored, leads to an inflated standard error of the difference, reduced power, and a conservative test. Handling the two designs with the same formula is a methodological error."

## 二、DeLong 方法原理（DeLong, DeLong & Clarke-Pearson 1988）

PubMed 原论文摘要逐字（PMID 3203132，Biometrics 1988 Sep）：
> "When two or more empirical curves are constructed based on tests performed on the same individuals, statistical analysis on differences between curves must take into account the correlated nature of the data. This paper presents a nonparametric approach to the analysis of areas under correlated ROC curves, by using the theory on generalized U-statistics to generate an estimated covariance matrix."

MedCalc 书页展开：
- 完全非参数："it makes no assumption about the distribution of test values in the diseased or healthy population."
- 起点：**AUC ≡ Wilcoxon rank-sum statistic**。n1 病例、n0 对照时：
  `θ̂ = 1/(n1·n0) · Σᵢ Σⱼ ψ(X1ᵢ, X0ⱼ)`
  核函数 ψ = 1（病例值 > 对照值）/ 0.5（并列）/ 0（对照值 > 病例值）。即「随机病例得分高于随机对照的概率」。
- 方差：**structural components**（jackknife 的推广）给出 θ̂ 方差的闭式估计，同时用于单 AUC 置信区间与两 AUC 协方差。

配对比较公式（书页逐字转写）：
`z = (θ̂₁ − θ̂₂) / √(Var(θ̂₁) + Var(θ̂₂) − 2·Cov(θ̂₁, θ̂₂))`
- Cov 由同一批病例/对照上两检验的结构分量直接估计，无需枚举重采样。
- H0: θ1 = θ2 下 z ~ N(0,1)；双侧 p = 2×Φ(−|z|)。
- 95% CI for θ1−θ2: `(θ̂₁−θ̂₂) ± 1.96·√(Var(θ̂₁)+Var(θ̂₂)−2Cov(θ̂₁,θ̂₂))`

独立比较：Cov = 0 by definition，`z = (θ̂₁−θ̂₂)/√(Var(θ̂₁)+Var(θ̂₂))`，方差各自用 DeLong 估计。

协方差为何重要（书页算例）：100 例心梗、AUC 0.82 vs 0.78 差 0.04。若两标志物高度相关（troponin 模糊者 BNP 也模糊），Cov 大而正 → 差的标准误小 → 有效能检出适度真实差异；若错当独立，标准误被高估、z 被压低，可能漏检真实优势。

## 三、k≥3 条曲线与 Hanley–McNeil 对照

- 先全局检验 H0: θ1=θ2=⋯=θk，取 k−1 个独立对比向量 c，`χ² = cᵀV⁻¹c`（V 为对比协方差矩阵），df=k−1；显著后再逐对 z 检验。书页算例：NGAL/KIM-1/cystatin C 在 200 例上 AUC 0.84/0.79/0.76，全局 χ²(df=2) 显著才报三对两两比较。
- Hanley & McNeil (1983) 旧法：用平均 AUC 与原始分数 Pearson r 查表得 r′，`SE(θ̂₁−θ̂₂)=√(SE²(θ̂₁)+SE²(θ̂₂)−2r′SE(θ̂₁)SE(θ̂₂))`。DeLong 更优因**直接从数据估协方差**，不经 r′ 近似；H&M 仅用于复现旧文献。

## 四、Verdict ≠ clinical relevance（书页逐字要点）

- 大样本下 AUC 差 0.01 也能 p<0.05；0.03（0.85 vs 0.82）多数场景可忽略，≥0.10 才通常算实质重要。
- 曲线交叉时整体 AUC 比较会掩盖「高敏区 A 优、高特区 B 优」，必须看图。
- AUC 统计无显著差异时，临床选便宜/快/低侵入者——AUC 无法捕捉。
- 报告规范：各检验 AUC + 95%CI、AUC 差 + 95%CI、p 值；差的 CI 比单独 p 更有信息（含方向与合理区间）。

## 五、MedCalc 手册算例（第二独立页逐字，WebFetch 200）

`Comparison of ROC curves`（2–6 条**同源**曲线，DeLong 推荐）：n=100，阳性 55/阴性 45。
- TEST1 AUC 0.947 SE 0.0241 CI 0.883–0.982；TEST2 0.679 SE 0.0537 CI 0.578–0.769；TEST3 0.915 SE 0.0275 CI 0.843–0.962。
- 逐对：TEST1~TEST2 差 0.268 SE 0.0577 CI 0.155–0.381 z=4.642 P<0.0001；TEST1~TEST3 差 0.0313 SE 0.0218 CI −0.0113–0.0740 z=1.439 P=0.1501（**不显著**）；TEST2~TEST3 差 0.237 SE 0.0430 CI 0.152–0.321 z=5.497 P<0.0001。
- AUC 的 95%CI 默认 **binomial exact**（推荐），非 AUC±1.96SE；此 exact 选项**不适用于两 AUC 之差**。
- `Comparison of independent ROC curves`：按性别分组分别算 AUC 再两两比，例 Female 0.971(SE 0.0217) vs Male 0.924(SE 0.0432)，差 0.0473 SE 0.0484 CI −0.0475–0.142 z=0.978 P=0.3283。

## 六、诚信与判非

- 候选第二独立域 arXiv:1402.9224、arXiv:1701.06359 经 WebFetch 均非 DeLong/AUC 主题（一为 not found、一为双曲算子分解），**已弃用不冒充来源**。
- 本主题全库 SKILL.md + module-memory + co-learn + references 判重：DeLong 0 命中、0 专节；Bland-Altman（§r788B 一致性）、Youden（§r810A 阈值）异命题。豆包自留地 WB 0 落地。
- 来源：
  - `https://www.medcalc.org/en/book/roc-comparison.php`（WebFetch 200 全文逐字，第一独立域）
  - `https://pubmed.ncbi.nlm.nih.gov/3203132/`（WebFetch 200 原论文摘要，第二独立域）
  - `https://www.medcalc.org/en/manual/comparison-of-roc-curves.php`（WebFetch 200 手册算例，第三页）
  - `https://www.medcalc.org/en/manual/comparison-of-independent-roc-curves.php`（WebFetch 200 独立样本对照）
