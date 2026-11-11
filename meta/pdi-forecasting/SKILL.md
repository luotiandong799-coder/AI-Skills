---
name: meta/pdi-forecasting
description: 预测与概率判断（Predictive Intelligence）。当需要估计"某事件会不会发生/何时发生/量级多大"、给结论配概率、做情景推演、或要求"押个概率/预测一下/评估可能性"时调用。提供超预测五步法（精化问题→参考类基率→内部视角微调→贝叶斯小步更新→Brier 记分闭环）、费米拆解、范围敏感性、预测版 Pre-Mortem、0.1–0.9 校准带。输出带概率与依据的可结算判断，绝不把它当行动决策或专业建议。
module: PDI
modules: PDI,TI,DI
version: "1.5.0"
---

# PDI · 预测与概率判断（Predictive Intelligence）

> 本技能是 Personal AI OS 13 模块中 **PDI（预测智能）** 的唯一载体。TI 想明白因果、DI 在多方案中选择、PDI 负责"给未来事件配一个可结算的概率并持续校准"。
> 方法论实拉自 2026-11-07 WebSearch（真实可核验）：judgmentcallpodcast.com（Tetlock/IARPA ACE、超预测 Brier≈0.14）、duelduck.com（五步框架、基率先行、单因素调整上限 10–15pp）、predictionmarketsindex.com（超预测者 Brier 0.166 vs 普通 0.259）、soul-atlas.github.io/souls/superforecaster（Tetlock 序列/似然比/参考类/Pre-Mortem）、xueqiu.com（费米化/双视角/贝叶斯更新/Brier 闭环）。

## 一、何时用

- 用户要"评估可能性 / 押个概率 / 会不会发生 / 何时发生 / 量级多大"。
- 需要把"云状问题"（战略、市场、项目风险）拆成可结算的判断。
- 情景推演、风险预判、对某结论标注置信度。
- **不适用**：需要执业资质的高风险结论（医疗/法律/重大投资）→ 只做概率整理，交有资质方；纯事实查询；已确定的历史事实。

## 二、超预测五步法（核心流程）

| 步 | 动作 | 要点 |
|---|---|---|
| 1 精化问题 | 改写成可判定的二元/分档问题 + 明确结算来源与日期 | "会不会涨"→"BTC 于 2026-12-31 收盘价是否 > $X（来源 CoinGecko）"。两个陌生人能否对结果达成一致=前提 |
| 2 参考类基率 | 先找最可辩护的参考类，写下 base rate（外部视角） | 问"这类事历史上发生过多频繁"。忽略基率=最有把握地犯错 |
| 3 内部视角微调 | 当前案特异性只作**小额调整**，锚定基率 | 单因素调整上限 **10–15pp**；大幅偏离必须给明确因果机制（非"感觉"） |
| 4 贝叶斯小步更新 | 新证据按**似然比**小幅更新，记录每次修订 | "若为真/若为假，这条新闻概率各多少"；似然比≈1 的新闻再响也无信息 |
| 5 Brier 记分闭环 | 记录每个概率，结算后算 Brier，诊断过度/不足自信 | Brier=概率与结果(1/0)差的平方均值；0 完美、0.25=永远猜 50%、1 全错。超预测者≈0.14–0.17，普通≈0.26 |

## 三、关键技法

- **费米拆解**：大问题拆成若干可独立估的小量，加权合成；每小量各自给概率+依据。
- **范围敏感性**：概率必须随"时间窗/量级"变化——"6 个月内"须低于"5 年内"；不随范围变=在讲叙事不是建模。
- **预测版 Pre-Mortem（Gary Klein）**：假想该预测以意外方式结算，解释"怎么会这样"，暴露中枢估计忽略的尾部路径。
- **0.1–0.9 校准带**：未训练判断天然过度自信（把薄证据当近乎确定）；公开概率先压在 0.1–0.9，只有在具名因果机制支撑时才越界。
- **多源平均 + 适度极端化**：多个独立估计（自拆解/模型/他人/市场）取平均后，向 0/1 方向适度 extremize，回收分歧掩盖的信号。
- **越更新越准的前提**：快、重复、被记分的反馈；无记录时记忆会抹掉失误只留命中。

## 四、硬护栏（实拉共识）

- **绝不编造概率依据**：缺数据/缺基率时明确标"基率未知，仅给区间"，不硬造精确数字。
- **区分「预测」与「决策」**：PDI 只给可结算概率；采不采纳、投多少仓是 DI/EI 的事，PDI 不替用户下注。
- **区分「事实 / 推断 / 猜测」**：基率有来源=事实级；内部视角调整=推断；纯直觉=猜测，必须标注。
- **概率非真理**：是"当前证据下的最佳可校准判断"，随新证据变；Brier 需长期批量评估，不以单次命中/失误论英雄。
- 高利害场景引导用户核实事实、咨询有资质方，不把概率当专业建议。

## 五、与 OS 协作

- 概率结果 → **DI**：把概率喂进决策矩阵/期望值权衡。
- 情景与尾部风险 → **EI**：生成预案与回滚触发条件。
- 预测台账与 Brier → **RI**：复盘时用记分诊断校准度。
- 因果结构（该不该调、调多少）→ 委派 **TI**（`meta/ti-critical-reasoning`）。

## 六、Brier 分解三病灶诊断（BS = 可靠性 − 分辨率 + 不确定性；来源：brierscore.com / inferensys.com，2026-11-07 实拉）

Brier 分数只是一个数，分解才知道**错在哪**，避免修错方向：

| 病灶 | 症状 | 修法 |
|---|---|---|
| **可靠性差**（校准错误） | 说 70% 的事不是约 70% 发生；校准曲线偏离对角线；系统性过/欠自信 | 修概率映射（按桶收缩/拉伸）；从基率出发、有证据才偏离；不混不同类别/周期的校准视图 |
| **分辨率低**（区分度差） | 预测全挤在 0.5 附近——校准好了但没信息量；或大胆但错（sharp 无 resolution） | 只在真有信号的类别下注；建立一致的更新规则让概率随证据移动；监控预测分布别钉死在 0.5 |
| **不确定性高**（题目本身难） | 基率接近 50/50 时 BS 下限高（=0.25） | 不可行动项；跨数据集比较 BS 无意义，用 Brier Skill Score 对基准 |

**周度复盘流水线（brightlearn.ai）**：结构化日志（预测概率/结果0-1/时间戳/问题引用）→ 按桶算三分量 → 可靠性主导→修校准；分辨率主导→改信号；样本小时分解不稳定，勿过度解读。

**诚实边界**：BS 混合了你的行为与数据集难度；miscalibrated 时"更敢押"反而更差——先修可靠性再追分辨率。

## 七、评分规则的选择与「同一个分数不能同时当三把尺」（2026-11-08 r706B 实拉）

> 与 §六 分工：§六 用 Brier 分解诊断**病灶**（修校准还是修信号）；本节管**该用哪把尺、这把尺能不能证明结论**，以及校准曲线本身的测量误差。避免「算了个 BS 就宣布校准变好」这类越界。

### 7.1 评分规则是激励设计，不是中性计分器

- **严格适当（strictly proper）** 的定义：期望分在「报出真实信念」时唯一取最优（JMLR 23-0106 原文 "It is strictly proper if inequality (1) is strict unless p = q"；另有定义式 `E_{Y~q}[s(q,Y)] > E_{Y~q}[s(p,Y)]`，"A prediction of p = q is truthful, as the agent simply reports her belief q"）。⇒ **用适当评分规则记账，才使「不装、不迎合、不硬造概率」成为最优策略**；换成命中率/准确率就会奖励把 0.4 说成 1。
- **Brier 与 log score 惩罚尾部的行为不同**：两者都严格适当，但 Brier 有界（二元 0–1）、log score 在 `p→0` 而事件发生时**发散到 ∞**；metricgate 逐字 "log loss diverges, Brier remains bounded"、"When the cost of overconfidence dominates, log loss is the more discriminating choice"。⇒ **0/1 极端断言的代价用 Brier 会被大幅低估**；本技能 §三 的 0.1–0.9 校准带在高风险题上应配 log score 复核，不能只报 BS。
- 判据：**选尺先于下注**。结算后再挑对自己好看的分数 = 把评分规则变成可博弈对象；台账必须事先写明本题用哪个规则、为什么。

### 7.2 ★一个分数同时测三件事 ⇒ 不能用它单独证明校准

- scikit-learn 原文逐字："Strictly proper scoring rules … assess calibration (reliability) and discriminative power (resolution) of a model, as well as the randomness of the data (uncertainty) at the same time. **As it is not clear which term dominates, the score is of limited use for assessing calibration alone** (unless one computes each term of the decomposition). **A lower Brier loss, for instance, does not necessarily mean a better calibrated model, it could also mean a worse calibrated model with much more discriminatory power**."
- ⇒ **BS 变好 ≠ 校准变好**：可能是分辨率涨了压过可靠性恶化。要宣称「校准改善」，必须同时给出分解后的 CAL/REL 分量或可靠性图；单报 BS 的趋势不构成证据（接 §六 三病灶，但结论方向相反：§六 用分解诊断，本条禁止用未分解的分数做结论）。
- **UNC 由题目难度决定，不是预测者水平**：ScienceDirect 原文 "It is inappropriate to compare forecasts for systems with significantly different UNC values"；BSS = 1 − BS/BS_ref 才把基率难度归一。⇒ 跨题目集/跨周期比原始 BS 排名无意义；要给出同参考基线的 BSS。

### 7.3 可靠性图（校准曲线）自带估计误差，别把图当真相

- **分箱是偏差-方差权衡**：scikit-learn 原文 "a higher number of bins provides a more granular view (less bias), it also requires more data to ensure that each bin has a sufficient number of samples to produce a stable estimate of the fraction of positives (variance)"；`n_bins="cube_root"` 自动取 ⌈n^(1/3)⌉，"For a small number of samples, say 100, it might return slightly too low number of bins"。⇒ **个人预测台账样本少时，校准曲线的每个点都不稳**；必须同时报每箱样本数，箱数少就别下细粒度结论。
- **空箱与分箱策略**：`calibration_curve` 文档 "Bins with no samples … will not be returned, thus the returned arrays may have less than n_bins values"；`strategy` 有 `uniform`（等宽）/`quantile`（等样本）。⇒ 曲线点数少于箱数不是 bug；混用两种策略画的图不可直接比。
- **★校准器必须独立于生成预测用的数据**：scikit-learn 原文 "Ideally, the calibrator is fit on a dataset independent of the training data used to fit the classifier … Using the classifier output of training data to fit the calibrator would thus result in a **biased calibrator that maps to probabilities closer to 0 and 1 than it should**"；`CalibratedClassifierCV` 用交叉验证保证无偏。⇒ **用自己那批已结算预测去拟合自己的校准映射，会把概率系统性推向极端**；留一份独立校准集，或至少交叉验证。

### 7.4 落地清单

1. 登记预测时同时写死：本题评分规则（Brier / log）、结算来源与日期、参考基线 BS_ref。
2. 报告改善前先算三分量；只报 BS 一律标注「未证明校准改善」。
3. 高风险题（0.1–0.9 带边缘）加算 log score，检查极端自信是否被 Brier 掩盖。
4. 画可靠性图必带每箱样本数；样本 <100 只作定性参考。
5. 校准映射用独立集或 CV 拟合，禁止在同一批结算样本上自校准。

## 八、校准指标自身也是一把尺：ECE 的三个结构性缺陷与重校准的连锁代价（2026-11-08 r717B 实拉）

> 与 §七 分工：§七管「评分规则与 Brier 三量分解」，§7.3 管「可靠性图这个估计量自带偏差-方差误差」；本节管 **ECE 作为单一数字的可比性 / 抵消盲点 / 忽略 sharpness**，以及**把概率重新映射之后下游阈值会怎样**。

### 8.1 ★ECE 只测校准，不测 sharpness（信息量）
- mbrenndoerfer 逐字："ECE also only measures calibration, not sharpness. Sharpness is the property that the model's confidence scores are informative: a model that always predicts the marginal class probability (for example, predicting 0.7 confidence for a class with 70% base rate) is perfectly calibrated but useless"；mlmentorship 逐字："Doesn't measure sharpness: a model that predicts 0.5 for everything has ECE = 0 if base rate is 0.5, but is useless."
- ⇒ **「ECE 降到 0」不等于「判断变得有用」**：恒定报基率即可拿到完美校准分。PDI 台账里报校准必须与适当评分规则（Brier / log，见 §7.1–7.2）及分辨率同时报；校准与 sharpness 是两个独立目标，理想是「既准又有区分」。全库 `sharpness` 唯一命中是豆包自留地 KB 的「continuity vs sharpness」（上下文卫生），不同维度；`MCE` / `debiased` 词边界 0 命中。

### 8.2 ★ECE 是分箱协议的函数，且两个盲点会互相掩护
- mbrenndoerfer 逐字："Different researchers use different bin counts (typically between 10 and 20), making it difficult to compare ECE values across papers without knowing the exact evaluation protocol. A model with ECE of 0.03 reported with 15 bins may not be directly comparable to one with ECE of 0.04 reported with 10 bins."；"Equal-width binning can produce misleading ECE estimates if the confidence distribution is imbalanced"；Adaptive binning "complicates comparison across models and implementations"。
- thelion 逐字："ECE has two blind spots. Overconfidence in one bin and underconfidence in another partly cancel. And if almost all predictions fall in the top bin, ECE mostly measures that bin."（实例：ECE 0.031 / 1,200 题 / 990 题挤在 0.9–1.0 箱，低箱每箱仅 handful）；lifeofresearch 预印本补：「等宽箱 plugin 估计量有偏且小样本偏差大」（Roelofs 2022 等质量箱/去偏、Kumar 2019、Nixon 2019「重校准方法排名随校准度量选择而变」、Blasiok 2023「ECE 甚至不是预测器的连续函数」）。
- mlmentorship 变体清单：MCE=最坏箱（安全关键视角）、Adaptive ECE=等频箱、Class-wise ECE、Top-label ECE（多类只用 top-class 概率 ⇒ "ignoring whether the full distribution is well-calibrated"）。
- ⇒ **报 ECE 必须附「箱数 + 分箱策略 + 每箱样本数 + 是否 MCE」四件套**，否则跨轮 / 跨台账的 ECE 数字不可比；单看一个下降的 ECE 不能证明校准改善（可能被抵消、可能只测了顶箱）。与 §7.3 的分层：那条是「校准曲线的估计误差」，本条是「把曲线压成一个数之后丢掉的信息」。

### 8.3 ★重校准不是无损操作：argmax 不变 ≠ 下游决策不变
- thelion 逐字："Temperature does not change which Choice option wins, but it changes every Noul probability and every Score expectation, so every threshold tuned before the fit has to be tuned again."（实例：0.8 的退款路由阈值 + 拟合 T=2.2 → 自动批准份额 "drops by half overnight"，"Nothing was wrong with the fit"）。
- mlmentorship 逐字："Shared positive scaling preserves multiclass argmax, not every probability-threshold action."；Platt 的截距可改变 0.5 处决策、isotonic 的平台可造平局或把分数推过操作阈值、**vector / matrix scaling "can change class ordering and accuracy"**；收口 "Calibration is not generally lossless on accuracy or decision cost."
- 两个连带失效面：① **子群反向** thelion "A single temperature can also help the average and hurt a subgroup. Nimble's fit improved average calibration, while the ECE of its Score questions rose from 0.105 to 0.177"；② **分布漂移** "Laya's English checkpoint scored 0.000 accuracy on Khmer text while reporting 0.952 confidence ... No threshold on confidence can catch that"。
- ⇒ 任何「把历史预测重新映射 / 重校准」的动作，必须连带做：重验所有基于概率阈值的护栏（弃权线、0.1–0.9 带、升级线）→ 分子群报校准 → 声明「仅分布内有效」；否则「我调了校准」不等于「概率可用了」。mlmentorship 四个 common pitfalls（拟评同批、报 ECE 不配可靠性图、假设重缩放必有帮助、把校准与 accuracy 混淆）并入落地清单。
- 判非：§7.3 的 cube_root / 空箱 / 独立校准集、§7.2 的 BS 三量分解、§7.1 严格适当规则均不重复；`vi-fact-verification` L96 只讲「温度缩放用留出集、ECE 与分类质量并列报」，未覆盖阈值失效 / 子群 / 漂移三连。

## 九、来源

### 2026-11-07 首拉

- 超预测 / IARPA ACE / Brier≈0.14 超基线 30%：judgmentcallpodcast.com/2026/08/82361-forecasts-3-archetypes-why-the-hedger-wins-in-2026
- 五步框架 / 基率先行 / 单因素 10–15pp 上限 / Metaculus 0.111：duelduck.com/blog/how-to-price-a-prediction-beginners-framework
- 校准可训练 / Brier 0.166 vs 0.259 / 0.25 参考：predictionmarketsindex.com/learn/calibration-and-forecasting-skill
- Tetlock 序列 / 似然比 / 参考类 / 范围敏感性 / Pre-Mortem / extremize：soul-atlas.github.io/souls/superforecaster
- 费米化 / 双视角 / 贝叶斯更新 / Brier 闭环：xueqiu.com/9169772982/394454891

### 2026-11-08 r706B 增补（逐字核验）

- scikit-learn.org/dev/modules/calibration.html §1.16（严格适当评分规则同时测三量、「limited use for assessing calibration alone」、低 Brier ≠ 更好校准、n_bins 偏差-方差与 cube_root、校准器须独立数据）（WebFetch 全文）
- scikit-learn.org/stable/modules/generated/sklearn.calibration.calibration_curve.html（空箱不返回、uniform/quantile 策略）
- metricgate.com/docs/scoring-rules-brier（strictly proper 定义、Murphy 分解、BSS=1−BS/UNC、log loss 在尾部发散而 Brier 有界）
- handwiki.org/wiki/Brier_score（BS=REL−RES+UNC、reliability=0 才完美、BSS=1−BS/BS_ref）
- sciencedirect.com/science/article/pii/B978044318681300026X Ch.14（UNC 不同不可比、「inappropriate to compare forecasts for systems with significantly different UNC values」）
- onlinelibrary.wiley.com/doi/10.1002/2013JD020195（Murphy 分解实证：人类预报 reliability 差但 resolution 高 ⇒ 单看总分误判）
- JMLR 23-0106 / Gneiting & Raftery 2007（严格适当定义式，经 ima.qq.com 索引实拉）
- 判非：BS 三病灶表、周度复盘流水线已在 §六（brierscore.com / inferensys.com / brightlearn.ai），本轮不重复落；`wb-agent-evaluation` 的评测集有效性亦不在此重复。

### 2026-11-08 r717B 增补（逐字核验，四独立域交叉）

- mbrenndoerfer.com/writing/calibration-machine-learning-confidence-accuracy-ece/limitations-and-impact（2026-02-26；ECE 箱数 10–20 不可比、0.03@15箱 vs 0.04@10箱、equal-width 失衡误导、只测校准不测 sharpness、恒报基率 0.7 完美校准但无用、温度缩放假设跨类均匀；WebFetch 全文逐字）
- www.thelion.ai/guide-to-decision-models（Ch.7 Calibration；"Temperature ... changes calibration without changing accuracy at all"、0.8 阈值 + T=2.2 → 份额腰斩、"every threshold tuned before the fit has to be tuned again"、ECE 两盲点 0.031/1200/990、Nimble Score ECE 0.105→0.177、Laya Khmer 0.000 accuracy / 0.952 confidence；WebFetch 逐字核验）
- mlmentorship.com/concepts/expected-calibration-error（2025-08-18；ECE 加权定义、MCE/Adaptive/Class-wise/Top-label 变体、"Shared positive scaling preserves multiclass argmax, not every probability-threshold action"、Platt/isotonic/vector-matrix 对决策的影响、"Calibration is not generally lossless"、四个 common pitfalls；WebFetch 全文逐字）
- lifeofresearch.com/preprints/133/files/136/calibrated-is-not-informative.pdf（预印本；binned ECE 有偏、Roelofs 2022 等质量箱/去偏、Kumar 2019、Nixon 2019 排名随度量变、Blasiok 2023 ECE 非连续、分布漂移 Ovadia 2019；WebSearch 结果全文，逐串命中）
- metricgate.com/blogs/predictive-uncertainty-calibration-methods/（交叉佐证：ECE/MCE/Brier 三者并用、子群漂移 overall ECE 0.01 可藏 0.15、Platt/isotonic 不改 AUC、堆叠校准两次会劣化；WebSearch 结果全文）
- 判非：`ECE` 全库 46 命中经词边界复核仅 6 文件且为 `recent` 等子串噪声；`vi-fact-verification` L96、`00_AI智慧进化研究主线` 的 AUROC/ECE、`wb-agent-evaluation` KB 的 isotonic vs temperature scaling 均属不同命题；`sharpness` / `温度缩放` 命中在豆包自留地 KB（上下文卫生 / 评测阈值诊断），WB 0 落地。


## 十、预测对象形态决定评分规则：从二元事件到分位／区间／全分布／多变量（2026-11-11 r734A 实拉，四独立域交叉）

> 与 §七（Brier 三分解／可靠性图）、§八（ECE 三缺陷／重校准）分工：那两节全在处理**二元事件的点概率**；本节处理**预测对象本身是什么形状**——分位数、区间、完整分布、多变量场景各需要不同的尺，且这些尺是同一族的不同投影，不是彼此独立的指标。

- **r734A-1 ★先声明预测对象，再选评分规则；拿 Brier 评区间预测是范畴错误**：MDPI《Recent Advances in Probabilistic Electricity Price Forecasting》§6.7 逐字给出按形态的尺表——"**Quantile forecasts** should primarily be evaluated using the pinball loss or the CRPS approximated from quantiles"／"**Prediction intervals** should be assessed using both coverage and sharpness information"／"**Full marginal predictive distributions** are naturally evaluated using CRPS"／"**Multivariate scenarios** require multivariate scores, such as the energy score or variogram score"；二元事件才是 "the Brier Score is a natural evaluation metric"。且四把尺并非并列发明：arXiv 2609.37273 EC.2.2 逐字 "The CRPS is therefore the **integral of the so-called Brier scores** for the associated binary probability forecasts at all real-valued thresholds"、"S(P̂,y) = 2∫₀¹ ℓᵤ(y,Q(u))du"（CRPS = 所有分位 pinball loss 的平均）、"The interval score defined here is **the sum of the pinball losses at its two endpoint quantile levels**: Sα([L,U],y)=ℓ_{α/2}(y,L)+ℓ_{1−α/2}(y,U)"；"CRPS aggregates quantile performance across all quantile levels, whereas the interval score samples that same quantile-based scoring idea at only two levels"。判据：① 预测台账先登记「本次输出是事件概率／单点分位／区间／CDF／场景向量」，再登记用哪把尺；② 只评一个分位数（如 P90）的 pinball loss 不能用来宣称「整个分布更好」；③ 给区间或连续量套 Brier/ECE 属于把二元事件的尺误用到别的对象上，与 §8.1「ECE=0 不等于判断有用」是两类错误。

- **r734A-2 ★coverage 与 width 必须作为联合约束，且只有 proper interval score 能把两者折成一个数**：MDPI §6.2 逐字 "A calibrated interval should have PICPα ≈ 1−α. Nevertheless, **interval coverage should not be interpreted separately from interval width. A model can achieve nominal coverage by producing excessively wide intervals**"；"PIAW and its normalized version, PINAW, **reward narrow intervals regardless of whether the empirical coverage is adequate**. Therefore, they are best interpreted jointly with PICP and, preferably, with a proper interval score"；Winkler 分数式 (6) `ISα(L,U;y) = (U−L) + (2/α)(L−y)1{y<L} + (2/α)(y−U)1{y>U}`——"This score **rewards narrow intervals but penalizes observations that fall outside the interval**, with larger penalties for more severe violations. It is therefore consistent with the calibration-sharpness principle"。temporalcv 官方文档逐字同式并标注 "Reference: **Gneiting & Raftery (2007, equation 43)**"、"Alias for compute_interval_score(). **Winkler (1972)** is the original formulation"、CRPS = `E|X−y| − 0.5·E|X−X′|`。判据：① 只报「95% 区间覆盖率 94.8%」等于允许无限宽区间刷满，必须同时报平均宽度与 IS；② PIT 直方图近似均匀只诊断**边际**校准（MDPI §6.5 "average scores may hide systematic failures during specific hours, price regimes or high-renewable periods"），不评依赖结构；③ AWD 是诊断量不是评分规则，不能拿来排名模型。

- **r734A-3 ★分数差要做显著性检验，且统计分数改进不等于决策价值**：MDPI §6.6 逐字 "Forecast comparisons should **not rely only on differences in average scores**. Since electricity prices are serially dependent ... apparent improvements may be driven by sampling variability"；给出 Diebold–Mariano（`DM = d̄ / sqrt(σ̂²_d/T)`）、Giacomini–White 条件预测能力检验（`H₀: E[g_t]=0`，`g_t=z_t·d_t`），多模型并列时 "pairwise testing can lead to multiple-testing problems. In such cases, researchers may use **model confidence set** procedures"；§6.7 又给出两条边界——"**CRPS is scale-dependent** and does not assess cross-hour or cross-market dependence. Therefore, comparisons across markets with different price levels or volatility should be interpreted carefully"、"**a statistically superior probabilistic forecast does not always imply higher decision value**"，须报完整 forecast-to-decision 链。判据：① 宣称「新版比旧版好」必须附分数差检验与所用尺，不能只比两个平均数；② 跨题目集／跨波动期比原始 CRPS 无意义（与 §7.2「跨题目集比原始 BS 无意义」同构，但那是 UNC，这是尺度与依赖）；③ 预测台账的「结算」栏须包含「尺 + 差检验 + 决策映射」三项，缺任一不许写「预测能力已提升」。

**提升层**：工作流（预测台账与结算协议）+ 可复用 Skill。触发词：评分对象形态、CRPS、pinball loss、Winkler／interval score、PICP/PINAW、energy score、variogram score、PIT、Diebold–Mariano、Giacomini–White、model confidence set、scale-dependent、forecast-to-decision。

**判非（本轮独立机检，登记不落地）**：`CRPS`／`pinball`／`Winkler`／`interval score`／`PICP`／`energy score`／`variogram`／`Diebold-Mariano`／`Giacomini-White`／`model confidence set` 全库 SKILL.md **0 命中**；`PIT` 11 命中经查为 `pit`/`pivot` 等子串与其他命题，非 PIT 直方图；§7 的 Murphy 分解、§8 的 ECE 分箱均属点概率层，本节不重立论；MDPI 综述中 QRA／conformal／normalizing flows 等**建模方法**族不属 PDI 评分规则，不搬。arXiv PDF 与 MIT 系 PDF 的 WebFetch 二进制拒绝如实登记（见下来源），未冒充一手全文直读。

### 2026-11-11 r734A 增补来源（逐字核验，四独立域交叉）

- `www.mdpi.com/1996-1073/19/15/3552`（Energies 2026, 19(15), 3552, Dudek/Piotrowski/Kopyt/Baczyński；WebFetch 200 全文 87,081 字符，§6.1–6.7 逐字：pinball 式(1)、PICP 式(4)、PIAW 式(5)、Winkler IS 式(6)、CRPS 式(8)(9)(10)、energy/variogram 式(11)–(13)、PIT、DM 式(15)、GW 式(17)、§6.7 按形态选尺清单）
- `arxiv.org/pdf/2609.37273`《When Stress Tests Miss the Risk》EC.2.2（**WebFetch 返回 application/pdf 二进制被丢弃**；改由 WebSearch 快照 + `ar5iv.labs.arxiv.org/html/2609.37273` 交叉，逐串命中 strictly proper 定义、CRPS=阈值 Brier 积分、CRPS=全分位 pinball 平均、IS=两端点 pinball 之和；ar5iv 可见正文在 §5.2 处截断、EC.2.2 未取到，如实登记不冒充全文）
- `temporalcv.readthedocs.io/en/stable/api/metrics.html`（WebFetch 200 逐字：`L(y,q;τ)=τ·max(y−q,0)+(1−τ)·max(q−y,0)`、`CRPS=E|X−y|−0.5·E|X−X′|`、`IS=(u−l)+(2/α)(l−y)I(y<l)+(2/α)(y−u)I(y>u)`、"A well-calibrated narrow interval scores better than a wide one"、Gneiting & Raftery (2007, eq.43) / Winkler (1972) / Koenker & Bassett (1978)）
- `www.mdpi.com/1996-1073/14/6/1679/html`（Energies 2021, 14(6), 1679；WebSearch 快照：IS/QS/IGN/CRPS 分解、reliability/resolution/sharpness 三分、PIT 直方图 "cannot be considered a decisive attribute to compare different models"）
- `umatechnology.org/probabilistic-forecasting-learning-uncertainty`（WebSearch 快照：coverage 与 sharpness 定义、"Two models may both achieve 90% coverage, but one may produce intervals that are half as wide"、评分须按 horizon 与 subgroup 分报、预测与过高／过低代价对齐）


## 十一、边际覆盖与条件覆盖不可兼得（2026-11-11 r737C 实拉，≥2 独立域一手交叉）

### r737C-1 ★「90% 覆盖」默认是边际覆盖，不是「每个 x / 每个子群都 90%」

conformal 只承诺 P(Y_{n+1}∈Ĉ(X_{n+1})) ≥ 1−α（对随机测试点平均）；条件覆盖 P(Y∈Ĉ(X)|X=x)=1−α 是更强要求，且 (2)⇒(1) 反之不成立。JRSSB 逐字：无分布假设 / 有限样本有效 / 条件覆盖三者「impossible to obtain all three … simultaneously (Barber et al., 2020; Vovk, 2012)」，conformal 是主动「relaxes the third criterion to the marginal coverage guarantee」。Springer Theorem 1 明写靠 **exchangeability** 证明，连续分数下还有上界 1−α+1/(n+1)。⇒ 结算栏必须写「保证类型 = 边际」，并声明 exchangeability 前提（时序/分布漂移下保证不自动成立）；禁止把平均有效讲成人人有效。

### r737C-2 ★精确条件覆盖不可得，实务折中是「预先声明关心的有限维平移族」

JRSSB 2025 把条件覆盖改写成「一族协变量 shift 上的覆盖」：目标类有限维时可「simultaneously obtain exact finite-sample coverage over all possible shifts」（例如每个**预指定**子群都精确覆盖），无限维类只能「quantifying the coverage errors」并用超参控制误差；ASA JSM 摘要同源佐证「impossible to form non-vacuous prediction intervals that give valid conditional coverage in finite samples」。⇒ 预测区间必须随附「保证的是哪一类覆盖、覆盖哪些预声明子群、gap 上界多少」；与 §十 r734A 的 PICP≈1−α 分工：那条讲覆盖率与宽度要联合约束（防无限宽刷分），本条讲这个覆盖率数字的作用域。

### r737C-3 ★边际有效掩盖高风险子群，且往往不知道该查哪个子群

JRSSB「Marginal validity does not preclude substantial variation in coverage among relevant subpopulations」；NeurIPS 2023 ImageNet 实例：名义 90% 下整体 89.8%，water jug 类仅 **50.8%**、flamingo **99.2%**；Springer 举末期患者被 undercover、少数族裔风险被误估，并逐字「oftentimes we do not have prior knowledge that what subpopulations may be at stake, or do not have access to the sensitive attribute information」（Fairness under unawareness）。⇒ 高风险预测必须分子群报覆盖 + 显式列出「未核验的子群」；仅报一个总覆盖率等于把最脆弱的那部分藏进平均数。

**提升层**：PI 输入保真 / AI 验收协议 / PDI 结算台账（按轮）。触发词：边际覆盖、条件覆盖、exchangeability、covariate shift、coverage gap、子群覆盖、PICP 作用域。

### r737C 来源与判非（逐字核验）

- `academic.oup.com/jrsssb/article-abstract/87/4/1100/8058684`（JRSSB 2025, 87(4) 1100–1126, Gibbs/Cherian/Candès《Conformal prediction with conditional guarantees》，WebFetch 200 摘要+引言逐字）：「Prior work has shown that it is impossible to provide exact conditional coverage universally in finite samples.」；三目标逐字「(1) make no assumptions on the underlying data-generating mechanism, (2) be valid in finite samples, and (3) satisfy the conditional coverage guarantee … Unfortunately, prior work has shown that is impossible to obtain all three of these conditions simultaneously (Barber et al., 2020; Vovk, 2012).」；「conformal prediction, which relaxes the third criterion to the marginal coverage guarantee」；「Marginal validity does not preclude substantial variation in coverage among relevant subpopulations.」；「When the target class of shifts is finite-dimensional, we show how to simultaneously obtain exact finite-sample coverage over all possible shifts. For example, given a collection of subgroups, our prediction sets guarantee coverage over each group.」；无限维类「quantifying the coverage errors」+ 可调超参。**一手期刊官方全文逐字**
- `link.springer.com/10.1007/s10994-024-06627-7`（Machine Learning《Adjusting regression models for conditional uncertainty calibration》，WebFetch 200 全文逐字）：「Conformal Prediction methods have finite-sample distributional-free marginal coverage guarantees. However, they generally do not offer conditional coverage guarantees, which can be important for high-stakes decisions.」；Theorem 1「We can prove that C(·) satisfies the marginal coverage guarantee by exchangability」，连续分数时「P(Y_{n+1}∈C(X_{n+1})) ≤ 1−α + 1/(n+1)」；「marginal coverage does not guarantee predictive sets with valid coverage for certain subgroups, especially for rare events or minorities」；「significantly undercover end-stage patients in survival year estimation, or misestimate the risk of minorities in tasks like recidivism prediction」；「oftentimes we do not have prior knowledge that what subpopulations may be at stake, or do not have access to the sensitive attribute information (Chen et al., 2019)」。**一手期刊官方全文逐字（第二独立域）**
- `papers.nips.cc/paper_files/paper/2023/file/cb931eddd563f8d473c355518ce8601c-Paper-Conference.pdf`（NeurIPS 2023《Class-Conditional Conformal Prediction with Many Classes》，WebSearch 快照逐字）：ImageNet 实例「Running STANDARD using a nominal coverage level of 90% on 50,000 examples … yields prediction sets that achieve very close to the correct marginal coverage (89.8%). However, this marginal coverage is achieved by substantially undercovering some classes and overcovering others. For example, water jug … only include it in 50.8% of the cases … flamingo … 99.2%」；形式化「class-conditional coverage: P(Y_test ∈ C(X_test) | Y_test = y) ≥ 1 − α, for all y」，且「(2) implies (1)」。**学术一手交叉（PDF 未全文直取，仅快照数值）**
- `ww2.amstat.org/meetings/jsm/2023/onlineprogram/abstract.cfm?sid=3157&tid=3157-p3`（ASA JSM 2023 摘要，WebSearch 快照逐字）：「In general, it is impossible to form non-vacuous prediction intervals that give valid conditional coverage in finite samples. Thus, popular predictive inference methods only provide marginal coverage over the covariates.」；同一组作者给出「coverage over a class of covariate shifts」的折中路径与「exact coverage over each group」。**独立学会摘要交叉**
- `econstor.eu/bitstream/10419/308058/1/1913045811.pdf`《An Introduction to Conformal Inference for Economists》：**WebFetch 返回 Anubis 反机器人验证页，正文未取到**；WebSearch 快照含 Proposition 1（Lei et al. 2018 / Foygel Barber et al. 2021）与 exchangeability 论证，但按先例**不冒充一手全文直读**，本轮仅作现象登记，结论一律由 JRSSB + Springer 两篇一手交叉支撑。**访问受阻，如实登记不采纳**

- **判非**：窄串词边界全库 SKILL.md：`marginal coverage` / `conditional coverage` / `exchangeability` / `calibration set` / `undercover` **全 0 命中**；`conformal` 唯一命中在本技能 §十 r734A 的**判非段**（明确写「QRA／conformal／normalizing flows 等**建模方法**族不属 PDI 评分规则，不搬」）。本轮不引入任何建模方法/算法流程，只取**统计保证的验收语义**（覆盖类型、三目标不可兼得、exchangeability 前提、子群 gap），与 r734A 判非不冲突且正好补齐其留下的元层；与 §十 的 PICP/PINAW/IS 分工：那节是「怎么打分」，本节是「这个分数保证不了什么」。豆包自留地 WB 0 落地。
- **换道/未采纳**：换道：clustered conformal / CLASSWISE / normalized conformal 等**生成预测集的算法族**按 r734A 判非一律不搬；econstor PDF 被 Anubis 反爬拦截，其 Proposition 1 仅作 WebSearch 快照登记、不冒充一手全文；Springer 的端到端训练改条件校准方案属建模方法，不采纳。A/B 两轮结论一律不复用。
