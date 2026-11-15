---
name: meta/pdi-forecasting
description: 预测与概率判断（Predictive Intelligence）。当需要估计"某事件会不会发生/何时发生/量级多大"、给结论配概率、做情景推演、或要求"押个概率/预测一下/评估可能性"时调用。提供超预测五步法（精化问题→参考类基率→内部视角微调→贝叶斯小步更新→Brier 记分闭环）、费米拆解、范围敏感性、预测版 Pre-Mortem、0.1–0.9 校准带。输出带概率与依据的可结算判断，绝不把它当行动决策或专业建议、预测题面可结算性与解析条件（什么算/何时算/谁裁定、三类规格缺陷、回退源）；多步预测策略（Recursive/Direct/DirRec/MIMO/DIRMO 五策略、误差累积与随机依赖两轴、windows_identical 跨视界可比与逐视界最准互斥）。；加权评分规则与预报员困境（w(y)S 破坏适当性/threshold-weighted 与 outcome-weighted 两类/条件分不进事件概率）。
module: PDI
modules: PDI,TI,DI
version: "1.10.0"
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

## 十二、聚合多个概率时"取平均"本身会系统性压扁信心（PDI · r742A 2026-11-14 实拉，四独立域交叉）

§七管"用哪把尺评分"、§八管"校准指标自己有什么缺陷"、§十管"预测对象形态决定尺"、§十一管"区间/集合预测保证什么"。本节管更前置的一层：**多个独立预测合成一个数时，简单平均这个动作本身就是一个有偏估计量**。§三 那句"多源平均 + 适度极端化"只是技法口号，本轮补上它为什么成立、什么时候反而不该极端化、以及怎么验收。

### r742A-1 ★两个彼此独立的压扁机制，只有一个能靠换统计量躲开
Baron / Mellers / Tetlock / Stone / Ungar（Decision Analysis 2014, 11(2):133-145）官方摘要逐字：把多人概率估计合成共识时通常用简单加权平均，而"Such aggregated probabilities correspond more closely to the real world if they are transformed by **pushing them closer to 0 or 1**"。两个 distorting factors：
- **因素一＝概率尺度两端被压缩**：逐字 "The first factor is the **compression of the probability scale at the two ends**, so that random error tends to push the average probability toward 0.5. This effect **does not occur for the median forecast, or, arguably, for the mean of the log odds** of individual forecasts." ⇒ 这是**算术平均这种统计量自带的**偏差，换中位数或对数几率均值即可绕开，不是"人太保守"。
- **因素二＝每个人都把自己只见部分信息这件事算进了谨慎里**：逐字 "the result of forecasters taking into account their **individual ignorance of the total body of information** available. Individual confidence in the direction of a probability judgment (high/low) thus fails to take into account the **wisdom of crowds** that results from combining different evidence available to different judges." ⇒ 群体合并后掌握的信息多于任何个人，但平均把每个人的谨慎原样保留了；这一条**对 mean / median / mean of log odds 三者都生效**。
- 官方结论逐字："We show that the same transformation function can approximately eliminate both distorting effects **with different parameters for the mean and the median**. And we show how, in principle, **use of the median can help distinguish the two effects**." ⇒ 判据：① 报聚合数必须写明用的是 mean 还是 median、有没有做 log-odds 变换；② 两种成因的修正强度参数不同，不能拿一个 extremize 系数一套用到底；③ 想判断"偏保守到底来自哪一个"，用中位数与均值之差做诊断，而不是凭直觉调系数。与 §7.2「一个 BS 同时测三件事」分工：那条讲单个分数不能证明校准，本条讲**聚合这个动作**本身带偏。

### r742A-2 ★极端化强度是"信息重叠度"的函数，不是可调超参
Satopää / Pemantle / Ungar《Modeling Probability Forecasts via Information Diversity》（arXiv:1406.2148，v1 2014-06-09 / v5 2015-09-10）官方摘要逐字：主观概率估计的异质性"is often more important than **measurement noise**"，论文建模"experts that use **partially overlapping information sources**"，并"shows how the **optimal amount of extremizing of the average probability forecast** (shifting it closer to its nearest extreme) **varies as a function of the experts' information overlap**. Our model thus gives a more principled understanding of the **historically ad hoc practice** of extremizing average forecasts."。UQAM 学位论文（GJP/ACE 综述）逐字佐证："An ideal opinion pool maximizes both calibration and sharpness (Ranjan & Gneiting, 2010)"、"linear opinion pools are **necessarily uncalibrated and lacking in sharpness**… too close to the marginal event frequency… leading to **underconfidence**"。
- 判据：① 信息完全重叠 → 最优聚合退化为平均；完全不重叠 → 趋向投票；**同一个模型在同一批新闻上跑 5 次不是 5 个独立信息源**，对它做极端化等于凭空造信心；② 极端化系数 a 必须**从已结算的同类问题上学出来**（在 log-odds 上取均值再乘 a 映射回概率，a=1 即赔率几何平均，a>1 才产生极端化），不许在事后挑让 Brier 好看的 a；③ 登记每个来源的信息集（看了什么、与谁重叠），否则"多源"只是重复计数。与 §8.3「重校准不是无损操作」分工：那条改的是概率值到下游阈值的映射，本条改的是**多个概率如何合成一个**。

### r742A-3 ★聚合器可以比"平均 + 极端化"更省，且同时做偏差校正与极端化
Satopää / Baron / Foster / Mellers / Tetlock / Ungar《Combining multiple probability predictions using a simple logit model》（International Journal of Forecasting 2014, 30(2):344-356）官方著录摘要逐字："construct a **likelihood-based aggregation formula**… The resulting aggregator has a simple analytical form that depends on a **single, easily-interpretable parameter**. This makes it computationally simple, attractive for further development, and **robust against overfitting**. Based on a large-scale dataset in which **over 1300 experts tried to predict 69 geopolitical events**, our aggregator is found to be **superior to several widely-used aggregation algorithms**."；UQAM 综述逐字："Satopää et al. (2014) used a recalibration technique based on the logit function which was able to **out-perform both the unweighted mean and the Beta-transformed linear opinion pool** algorithm suggested by Ranjan and Gneiting (2010)"。DataField《Further Reading》独立第三方逐字："Introduces the logistic recalibration approach to finding the optimal extremizing factor. Shows that this approach outperforms simple extremizing and provides **both bias correction and extremization simultaneously**."；同页另立"**Forecast Combination Puzzle**"（Stock & Watson 2004 / Smith & Wallis 2009）："simple combination methods frequently outperform more sophisticated approaches"、"the **estimation error in optimal weights** is often large enough to offset the theoretical advantage of optimization"。
- 判据：① 聚合方案升级前先问"多了几个待估参数"——单参数 logit 聚合器优于多参数的复杂加权，是因为后者在有限已结算题上把权重估歪；② 结算台账把「偏差校正」与「极端化」分两栏记，别用一次 Brier 改善同时给两者发奖；③ 简单平均是强基线（forecast combination puzzle），声称"新聚合更好"要在**同类题的样本外**比，不能只在拟合集上比。与 §7.1「严格适当规则」分工：那条约束评分尺，本条约束聚合器选型。

### r742A 来源与判非（逐字核验，2026-11-14）
- `pubsonline.informs.org/doi/10.1287/deca.2014.0293`（INFORMS 官方期刊页，Published Online 19 Mar 2014，WebFetch 200 摘要全文逐字）— 一手
- `econpapers.repec.org/article/inmordeca/v_3a11_3ay_3a2014_3ai_3a2_3ap_3a133-145.htm`（RePEc/EconPapers 著录，Decision Analysis 2014 vol.11 iss.2 pp.133-145，WebFetch 200 摘要逐字，双域交叉）— 一手著录
- `arxiv.org/abs/1406.2148`（arXiv 官方 abs 页，WebFetch 200 摘要逐字 + v1/v5 提交史）— 一手
- `www.econbiz.de/Record/.../10011051471`（IJF 30(2):344-356 官方著录，1300 experts / 69 events / single parameter / robust against overfitting 摘要逐字）— 一手著录
- `archipel.uqam.ca/20294/1/D5145.pdf`（UQAM 机构库学位论文，GJP 聚合算法综述，WebSearch 快照逐字：linear opinion pool / necessarily uncalibrated / logit 优于 unweighted mean 与 beta-transformed linear pool）— 学术一手交叉
- `datafield.dev/learning-prediction-markets/part-04/chapter-25/further-reading.html`（独立教材书目页，WebFetch 200 全文逐字：Clemen 1989 / Ranjan & Gneiting 2010 / forecast combination puzzle / Satopää 2014 同时做 bias correction + extremization）— 独立域交叉
- `olivlaw.com/en/us/cugetari/prognoza-20-extremizarea`（第三方课程笔记，含 log-odds 幂次 a 的算例与"a 从已结算题上学"的操作口径；**商业/教学立场，仅作算例交叉，不作结论唯一来源**）
- **判非**：`extremiz` 全库 SKILL.md 仅 1 命中＝本技能 §三「多源平均 + 适度极端化」的一句技法口号（无机制、无适用边界、无验收）；本轮把它展开为两个独立成因、信息重叠度函数与聚合器选型，**不重复口号本身**。`Ranjan` 命中在 `engineering/wb-execute-discipline/SKILL.md`（Ranjan Kumar，人名巧合，非 Ranjan & Gneiting 2010），不同命题。`log odds` / `logit aggregat` / `information overlap` / `wisdom of crowds` / `opinion pool` / `linear pool` / `under-confident` / `1300 experts` / `calibrated forecasts` 全库 SKILL.md **0 命中**；`extremiz` co-learn 台账 1 命中经查为 r710A 之外的历史建议引用，非本命题。豆包自留地 WB 0 落地。
- **未采纳**：具体极端化系数 a 的拟合值、GJP 各年 Brier 数字、beta-transformed linear pool 与 QRA/conformal 等建模方法族（沿用 §十 r734A 判非不搬）。B/C 两轮结论一律不复用。


## 十三、先判「这题能不能结算」：题面规范是评分规则之前的门槛（PDI · r746A 2026-11-14 实拉，四独立域交叉）

> 本轮取的是**题面（question specification / resolution criteria）**这一层：§7 管选哪把评分尺、§10 管预测对象形态、§11 管覆盖保证、§12 管多人聚合，但都默认「题目已经能被无争议地结算」。本轮补的是这个默认前提本身。

### r746A-1 ★ 结算三要素：什么算、何时算、谁裁定；「我看见就知道」不是阈值
Good Judgment《What's a month?》（Superforecaster Ryan Adler，事件 2025-08-04）逐字："**Ambiguity Kills Forecasts**"、"If a term or clause could be interpreted reasonably in different ways, we define that term and include examples as needed"、"everybody must be contemplating the same elements of an event they are asked to forecast"。实例：CNBC 两位评论员争 Tesla 股价"过去一个月"涨跌，一个用 7/3 收盘价约 $315（8/4 往前一个月是 7/4 休市），另一个用 7/7 开盘价约 $300——**两人都没算错，错在 "month" 没有共享定义**。原文引 Potter Stewart 在 *Jacobellis v. Ohio* 的 "I know it when I see it"，判词逐字："may work when deciding that a movie is not obscene, but it is **no way to set a threshold for a forecasting question**. Otherwise, we would invite **static from the crowd instead of signal**." 结论逐字："**Define upfront what counts, when it counts, and who decides**, and leave as little as possible to interpretation. Good forecasting starts with good question writing."
- **判据**：写概率前先填三格——① 什么算发生（判定对象与阈值）② 何时算（截止时刻/时区/数据源发布日）③ 谁裁定（数据源还是仲裁人）。三格任一留白 ⇒ 该概率**不可结算**，禁止进入 Brier 台账；"等结果出来再看"就是把噪声当信号。与 §7.1「先选尺」分工：那条约束评分尺，本条约束**被评分的题面**。Good Judgment 另页登记：随机抽样研究中约 **5%** 预测市场题目存在严重缺陷可能作废、2025-03 Polymarket 美乌矿产协议在未签署情况下结算 Yes（**厂商立场，仅作交叉，不作结论来源**）。

### r746A-2 ★ 规格缺陷是三类正交故障，不是一种「没写清楚」
Rethink Priorities《Types of specification problems in forecasting》（Juan Gil，2021-07-20）逐字三分类：**Ambiguous**（"not tight enough for it to be clear how it should resolve"）／**Misaligned**（"the **letter of the question diverges from the spirit of the question**"）／**Uncompelling**（"not interesting or important enough to incentivize forecasters to think about it"，在兴趣驱动型平台尤甚）。Misaligned 实例：朝鲜导弹确已发射，但解析条件要求美国国防部确认，DoD 以涉国家情报为由拒发声明 ⇒ 结算为否；逐字 "**a confirmation source is, by definition and necessity, an integral part of the proposition**"。原文明确三类 "not 'crisp'"、一题可同时中多类，且代理量与目标量在长视界上会脱钩（"what if that organization changes methodology, leadership, focus"）。
- **判据**：题面复核按**三行分别打勾**，不能只查歧义：① 无歧义（同一事实只解出一种结算）② 对齐（结算条件就是决策者真正关心的量；用代理量必须写明代理与目标的关联假设及失效条件）③ 有投入价值（有人愿意为它花时间，否则收不到有效预测）。歧义的两种收场各有代价，原文逐字：作废 "resolves neither positively or negatively"（预测者投入沉没）或交仲裁人 "some arbiter has final say"——此时 "**The forecaster would need to predict how they might decide (rather than the object-level question)**"，即预测对象被悄悄替换成"仲裁人会怎么判"，还额外引入仲裁人腐败空间。⇒ 仲裁兜底不得当作题面合格证明。

### r746A-3 ★ 解析条件七条硬清单 + 时间跨度放大 + 标题与条件必须同向
经 Metaculus《Guidelines for resolution conditions》在 Rethink Priorities 文内逐字转录的七条：**Aim for tight resolution conditions**（"limit the scope for ex-post quarrels"）／**Define your terms**（"Don't worry about being a little pedantic here!"）／**Be concrete**／**Use authoritative sources**（"be sure that the sources will be available at the time of resolution"）／**Consider and account for edge-cases**／**Consider fall-back criteria**（数据源停刊怎么办）／**Try to account for unknown unknowns**。原文："This problem becomes harder on **longer time scales** since there's more time for the world to change in a way that makes your question no longer make sense." Forecasting Wiki《How to Write Forecasting Questions》独立逐字补三条："**Questions do not resolve against "reality" they resolve against whatever source is stated**"；"**Compare the resolution criteria to the title question**. Is there any possibility where the criteria will go one way but the title question the other? ... It is unsatisfying when questions resolve on a **technicality**"；"The further into the future the more you want clarity as to what happens if the **resolution criteria disappears**." 同页 checklist 逐字要求 "written clearly enough as to leave no room for **ex post facto quarrels** over what really happened—and who was right"，并设"假想一位千里眼能否不问'原本是什么意思'就结算"的自检。
- **判据**：题面模板固定七格（紧／定义／具体步骤／权威源+存续性／边缘案例／回退源／未知未知），**视界越长格数不减反增**；另加「标题↔解析条件同向检查」与「结算所依据的数据源是否仍在发布」两项。题目对象是所写数据源而不是"现实"⇒ 数据源停刊时若无回退条款，此题必须判为作废而非按印象结算。与 §11「结算栏写保证类型」互补：那条写统计保证，本条写**结算可执行性**。

### r746A 来源与判非（逐字核验，2026-11-14）
- `goodjudgment.com/whats-a-month/`（Good Judgment，Ryan Adler；WebFetch 200 全文逐字；事件日 2025-08-04）— **第一独立域（从业者一手）**
- `rethinkpriorities.org/research-area/types-of-specification-problems-in-forecasting/`（Rethink Priorities，Juan Gil，2021-07-20；WebFetch 200 全文逐字，含 Metaculus 七条指南转录）— **第二独立域（研究机构一手）**
- `forecasting.wiki/wiki/How_to_Write_Forecasting_Questions`（Forecasting Wiki；WebFetch 200 全文逐字；外链 Metaculus question-writing guidelines / checklist、Foretold、AI Forecasting Dictionary）— **第三独立域（社区规范一手）**
- `goodjudgment.com`（《What the ForecastBench "Rematch" Still Won't Measure》，WebSearch 快照逐字：约 5% 题目有严重缺陷／2025-03 Polymarket 案例／GJ question team 题目失败率近零）— **厂商立场，仅交叉不作结论唯一来源**
- `joyful-slides-532925.framer.app/threshold-2030/part-3-forecasting`（Threshold 2030，WebSearch 快照逐字：五要素 specificity/reliable sources/edge cases/fallback/unknowns 及严格适当评分+多重比较的示例解析条件）— **第四独立域交叉（会议教程）**
- **判非**：三轮窄串全库 SKILL.md 精确扫描——`resolution criteria` / `question failure` / `ambiguity kills` / `fall-back criteria` / `unknown unknowns` / `misaligned question` / `letter of the question` / `operationalization` / `voided` / `Potter Stewart` **全 0 命中**；`arbiter` 唯一命中在 `defaults/wb-context-compressor/SKILL.md` §r608C 的 `StackArbiter` 产品名（子串噪声，非仲裁人命题）。`10-90 rule` / `clairvoyant` 等未纳入。B/C 两轮结论一律不复用；豆包自留地 `wb-execute-discipline` / `wb-context-compressor` **WB 0 落地**。
- **未采纳**：评分系统激励失配、"Dead people can't get paid"、预测市场平台对齐整篇论文、arbiter 腐败的经济学讨论、题目类型（binary/category/range/conditional）分类学——属平台机制研究，与可迁移判据无关。

## 十四、层次预测的一致性（coherence）与对账：分解预测不会自动加总（PDI · r750C 2026-11-15 实拉，3 独点）

> 与 §十（预测对象形态决定评分规则）、§十一（边际/条件覆盖）、§十二（概率聚合）、§十三（题面可结算性）分工：那四族管**单个概率怎么报、怎么结算**；本节管**把一件事拆成多个层级分别预测后，这些数还加不加得起来**——是预测台账的结构性验收，不是又一把评分尺。四独立域交叉：Hyndman《FPP2》§10 /《FPP3》§11 官方教材全文逐字 + Hyndman et al. `dow_hts.pdf` 作者论文 + CRAN `hts` 官方 refman + Monash 与斯里兰卡央行 staff study 综述。

### 14.1 数据按结构加总，预测不会自动加总；「一致性」是独立验收门
- FPP3 逐字：「**Forecasts are often required for all disaggregate and aggregate series, and it is natural to want the forecasts to add up in the same way as the data**」；「**we require forecasts that are coherent across the entire aggregation structure**」。FPP2 给矩阵式 `y_t = S b_t`，S 是 **summing matrix**，其下 m 行是单位阵、上方各行编码聚合约束；同一组数据若属性是**交叉**而非嵌套（grouped time series），存在多条合法聚合路径，S 的行数 n > m。
- Hyndman 论文逐字：「**while time series data naturally aggregate according to a hierarchical structure, forecasts usually do not**」。传统三法各有结构性代价：**bottom-up** 只预报底层再求和（丢掉聚合层自身的信息，聚合层精度常不如直接预报）；**top-down** 先报总量再按历史比例分摊，「**will always produce biased forecasts even if the original forecasts are unbiased**」（Monash 综述补：历史比例会随时间变化、低层精度差、middle-out 集两者之短）。
- 判据：任何「总体 + 分项」预测必须先声明 ① 聚合结构 S（嵌套 / 交叉 / 时间聚合） ② 一致性是不是硬要求 ③ 各层是独立预报还是由其他层导出。**分项加总 ≠ 总量**若未显式处理，是台账缺陷不是四舍五入误差；禁止用「分别预测完再手工凑齐总量」当作已做对账。

### 14.2 MinT 是带前提的最优化：W_h 的四种近似决定它能不能用
- FPP2 §10.7 逐字：使协调预测误差协方差迹最小且满足 `S G S = S` 的 `G = (S' W_h⁻¹ S)⁻¹ S' W_h⁻¹`，最优协调预测 `ỹ_h = S(S'W_h⁻¹S)⁻¹S'W_h⁻¹ ŷ_h`（式 10.8），称 **MinT (Minimum Trace)**；CRAN `hts` 逐字著录 Wickramasuriya, Athanasopoulos & Hyndman《Forecasting hierarchical and grouped time series through trace minimization》(JASA)，`MinT()` 参数含 `covariance = c("shr","sam")`、`nonnegative`、`algorithms = c("lu","cg","chol")`。Hyndman 论文逐字：MinT「**guaranteeing minimum variance unbiased forecasts**」——**无偏**是前提不是附赠。
- W_h 四种近似各有适用面（FPP2 逐字）：① `W_h = k_h I`（OLS，`G` 与数据无关、最省算力，但**忽略层间尺度差与序列相关**）；② `W_h = k_h diag(Ŵ_1)`（WLS 方差缩放，用一步残差方差）；③ `W_h = k_h Λ, Λ=diag(S1)`（**structural scaling**，只依赖结构、**残差不可得时唯一可用**，如判断性预测 / 无残差模型）；④ `W_h = k_h W_1` 样本协方差，但 m 相对 T 很大时估计差，须**收缩到对角阵**（`covariance="shr"`）。FPP2 结论逐字：「**optimal reconciliation forecasts are generated using all the information available within a hierarchical or a grouped structure**」。
- 判据：报协调结果必写「用了哪种 W_h + 是否有残差 + 基预测是否有偏」。Monash 实证反例逐字：「**MinT becomes infeasible for datasets with many repeated values or zeros**」（间断需求 / 多零值序列协方差奇异），此时退 WLS。把 MinT 当默认开关而不查前提 = 把带条件的无偏性当成无条件保证。

### 14.3 「加总对得上」与「预测更准」是两本账
- Hyndman 论文逐字引 Panagiotelis et al. (2021)：「**the predictive accuracy of reconciled forecasts cannot be worse than unreconciled forecasts in the mean squared error sense**」——这是**准确性收益**，但成立在基预测无偏、协方差可估、结构 S 正确之上；coherence 本身只保证**加总一致**，既不保证更准，也不保证概率校准 / 适当评分规则下的分数变好（与 §七「严格适当规则」分工）。
- 时间维度是另一条轴：斯里兰卡央行 staff study 逐字记 Athanasopoulos et al. (2017) **THieF**（时间聚合层面对账）与 Kourentzes & Athanasopoulos (2019) **cross-temporal**（截面 × 时间两维同时对齐）；并明确 Spiliotis et al. (2020) 的**顺序**执行「**does not guarantee coherent forecast across all dimensions**」。⇒ 分层与分时间尺度各做一遍对账，不等于全维一致。
- 判据：预测台账把「一致性验收（S 约束是否满足、哪些维度未对齐）」与「精度 / 校准验收（§七~§十三 的尺）」分成两栏分别报；对账只修加总，不拿它当「模型变好了」的证据。与 §十三 分工：那条管题面能不能结算，本条管多个可结算题之间的数是否自洽。

### r750C 来源与判非（2026-11-15 实拉，逐字核验）
- `https://otexts.robjhyndman.com/fpp2/hierarchical-forecasting.html`（Hyndman & Athanasopoulos《Forecasting: Principles and Practice》2nd ed. §10）— **curl 200 全文 42,387 字逐字提取**（WebFetch 首轮 AI 摘要 60s 超时仅返回前 15,000 / 48,944 字，改 curl 取全文）：coherent 定义、`y_t=S b_t` summing matrix 与展开、§10.3 bottom-up、§10.4 top-down 三种比例、§10.7 MinT 式 (10.8) `G=(S'W_h⁻¹S)⁻¹S'W_h⁻¹`、四种 W_h 近似（OLS / WLS variance scaling / structural scaling `weights="nseries"` / sample covariance + `covariance="shr"`）、「optimal reconciliation forecasts are generated using all the information available」。**第一独立域（教材作者官方全文）**。
- `https://otexts.com/fpp3/hierarchical-forecasting.html`（FPP3 §11）— **WebFetch 200 前 15,000 / 66,039 字全文逐字**（AI 摘要 60s 超时，如实登记）：「forecasts to add up in the same way as the data」、coherent 定义、hierarchical vs grouped（嵌套 vs 交叉、`parent/child` 与 `attribute1*attribute2` 语法）、多聚合路径式 (11.3)(11.4)、澳大利亚旅游 / 监狱人口例。**第二独立域（同作者新版教材）**。
- `https://robjhyndman.com/papers/dow_hts.pdf`（Hyndman et al.《Improving out-of-sample forecasts of stock price indexes with forecast reconciliation and clustering》）— **WebSearch 快照逐字**：「while time series data naturally aggregate ... forecasts usually do not」、top-down「will always produce biased forecasts even if the original forecasts are unbiased」、MinT「guaranteeing minimum variance unbiased forecasts」、Panagiotelis et al. (2021)「cannot be worse than unreconciled forecasts in the mean squared error sense」、reconciliation 两优势（coherence + 类似 forecast combination 的精度增益）。**第三独立域（作者论文，作交叉）**。
- `https://cran.stat.unipd.it/web/packages/hts/refman/hts.html`（CRAN `hts` 6.0.3，**Date/Publication 2024-07-30**）— **WebSearch 快照逐字**：包功能含 bottom-up / top-down / optimal combination / **trace minimization (Wickramasuriya et al. 2018 JASA)**，`MinT()` 的 `covariance=c("shr","sam")` / `nonnegative` / `algorithms=c("lu","cg","chol")` 参数与著录。**第四独立域（官方包文档）**。
- `https://www.cbsl.gov.lk/sites/default/files/cbslweb_documents/statistics/otherpub/staff_studies_Vol_51_2021.pdf`（斯里兰卡央行 Staff Studies Vol.51 §2.2）+ `https://researchmgt.monash.edu/ws/portalfiles/portal/637762132/517222219-oa.pdf`（Monash《Forecasting system's accuracy》）— **WebSearch 快照逐字**：Hyndman 2011 OLS 权重「completely independent of the data」、Wickramasuriya 2019 MinT 最小化迹、THieF 时间维度、cross-temporal 两步法、Spiliotis 2020 顺序法「does not guarantee coherent forecast across all dimensions」、Monash「**MinT becomes infeasible for datasets with many repeated values or zeros**」与退 WLS、top-down 三比例法偏差。**第五 / 六独立域（机构综述与同行评审实证，作交叉）**。
- **判非**：窄串全库 `SKILL.md` 精确扫描 — `coherence` / `summing matrix` / `MinT` / `trace minimization` / `top-down` / `bottom-up` / `base forecast` / `加总一致` / `层次预测` / `THieF` / `P.1204` **全 0 命中**（本技能 §十~§十三 全无分层加总命题）；`reconcil` 命中在 `engineering/execution-intelligence`（执行结果对账 / effect reconciliation）、`engineering/wb-debug-loop`（owner reconciliation）、`system/wb-spec-driven`（配置 reconcile）与 `system/skills-security-check`（策略合成），均为**执行态/配置态异命题**；`coherent` 命中在 `defaults/wb-context-compressor`（豆包自留地，coherent prompt）与 `engineering/wb-skill-authoring`（skillset 输出互洽），均非预测数值加总。按 rules/07 四态判「优＝加厚现有 `meta/pdi-forecasting`」，不新建并行层。豆包自留地 **WB 0 落地**。A / B 两轮结论一律不复用。
- **未采纳**：MinT 的 shrink 协方差估计量具体形式、cross-temporal 一步法的维数灾难推导、各法在 M5 / 旅游数据上的数值对比、股票指数聚类实证结论 —— 属数值与专门领域，不迁移为通用判据。

## 十五、多步预测策略与视界台账：误差累积、随机依赖与训练窗口（2026-11-15 r754C 实拉，3 独点）

> 分工：§十 管「用哪把尺结算一个概率/区间」，§十三 管「题面能不能结算」，§十四 管「多个题之间加总自洽」；本节管「这串 H 步预测是**用哪种策略生产出来的**、训练窗口被谁约束」。四层不同，不复用结论。

### 15.1 生产 H 步的策略是设计决策，不是超参；五策略与三大并发症
- NN5 原论文逐字：「**Multi-step ahead forecasting is still an open challenge**」；相比一步预测「**they have to deal with various additional complications, like accumulation of errors, reduced accuracy, and increased uncertainty**」。五策略逐字定义：**Recursive**「iterates, H times, a one-step ahead forecasting model ... After estimating the future series value, it is fed back as an input for the following forecast」；**Direct**「estimates a set of H forecasting models, each returning a forecast for the ith value」；**DirRec**「a different model is used at each step but the approximations from previous steps are introduced into the input set」；**MIMO**「In order to preserve, between the predicted values, the stochastic dependency characterizing the time series ... returns a vector of future values in a single step」；**DIRMO**「aims to find a trade-off between the property of preserving the stochastic dependency between the forecasted values and the flexibility of the modeling procedure」。
- 官方自陈结论逐字：「**the collective outcome of these studies regarding forecasting performance has been inconclusive. So the modeler is still left with little guidance as to which strategy to use**」——原文并列了支持 Recursive、支持 Direct、支持 DirRec、认为 MIMO 更差、以及支持 MIMO/DIRMO 的互相冲突文献；结论「**the larger the forecast horizon, the higher is the uncertainty**」。2025 河流盐度实证（二手快照）在 4h/24h/48h 三视界上「**Direct, MIMO, and DirMO strategies consistently outperformed others**」，但同一段明写「**Strategy choice depends on the accuracy vs. computational efficiency trade-off**」。
- **判据**：任何多步预报台账必写 ① 策略名 ② 视界 H ③ 是否把预测值回灌为输入；只写模型名（LSTM / ARIMA / Transformer）不足以复现，也不足以解释误差形状。「哪个策略更好」不得跨数据集/配置照搬论文结论（一手原文自陈 inconclusive），须报本域本视界的对照结果。

### 15.2 误差累积与随机依赖是两根独立轴，单看误差率会漏掉断裂轨迹
- 天大 Seq2Seq 论文页逐字：「**the Direct strategy does not accumulate errors. However, since H models are learned independently, which prevents this approach from considering the complex dependencies between the predicted values**」；「**Although the DirRec strategy avoids the disadvantage of the Direct strategy, it still has the disadvantage of the Recursive strategy, i.e., error accumulation**」；「**The MIMO strategy can avoid error accumulation and overcome the problem caused by using independently single-step predictor at different steps in the Direct strategy. However, The MIMO strategy imposes a constraint that all horizons being predicted must use the same model structure and the same set of input training data**」。
- NN5 逐字把 MIMO 的动机写成保留预测值之间的 stochastic dependency；2025 实证逐字「**the Recursive and DirREC strategies exhibited error accumulation, particularly in long-term forecasts**」。
- **判据**：验收固定两栏 —— **逐视界误差曲线（累积面）** 与 **轨迹连贯性 / 相邻步依赖（依赖面）**。Direct 逐点误差可能更优但曲线不连贯；MIMO 两头兼顾却要求所有视界共用同一模型结构与同一输入集，不能对每个 H 单独调参；DirRec 补齐依赖却把误差累积带回来。单报 MAPE/SMAPE 会把「分数不错 + 轨迹断裂」判成合格。

### 15.3 训练窗口被视界反向约束；「跨视界可比」与「逐视界最准」是互斥装配
- sktime v0.22.0 官方 `make_reduction` 逐字：`strategy`「**Must be one of "direct", "recursive" or "multioutput"**」；「**By construction, a recursive reducer always targets the first data point after the window, irrespective of the forecasting horizons requested**」；`windows_identical=True`（默认）「**Number of windows = total observations + 1 - window_length - maximum forecasting horizon**」、direct「**will create multiple models, one for each forecasting horizon ... the windows used to train the model are defined by the maximum forecasting horizon**」、「**All other forecasting horizons will also use those two (maximal) windows**」；`False` 时「**= total observations + 1 - window_length - forecasting horizon**」。官方给例：14 观测 / window_length=9 / fh=[2,4] → True 时各视界只有 2 个窗口，False 时 fh=2 可得 4 个。
- 官方取舍逐字：「**Use windows_identical = True if you want to compare the forecasting performance across different horizons, since all models trained will use the same windows. Use windows_identical = False if you want to have the highest forecasting accuracy for each forecasting horizon.**」
- 二手逐字（教学站，登记立场）：direct 目标矩阵 off-by-one 泄漏「**for model f_h predicting y_{t+h}, the most recent observation allowed in the input is y_t. Not y_{t+1}**」；「**Ordinary K-fold validation is not a safe default for forecasting**」、「**Purge rows whose label windows cross the forecast cutoff**」。
- **判据**：台账固定写四项 —— **strategy + windows_identical + 划分器（时序切分/滑窗）+ 泄漏检查**。同一套装配不能同时宣称「H=1..N 的误差可比」与「每个 H 用了最多训练样本」；recursive 训练时根本看不到视界（永远只学窗口后第一个点），故它的 H=h 与 direct 的 H=h 不是同一训练条件，横向比较须显式注明。与 §十一 conformal 覆盖保证分工：那条写统计保证的作用域，本节写训练装配与可比性口径。

### r754C 来源与判非（2026-11-15 实拉，逐字核验）
- `https://www.sciencedirect.com/science/article/abs/pii/S0957417412000528`（**Ben Taieb, Bontempi, Atiya, Sorjamaa**,《A review and comparison of strategies for multi-step ahead time series forecasting based on the NN5 forecasting competition》，**Expert Systems with Applications 39(8): 7067–7083, 2012-06-15**）— **WebFetch 200 全文逐字**：摘要三发现（Multiple-Output best / deseasonalization uniformly improves / input selection 与去季节化协同）、三并发症、五策略逐字定义与文献分歧段「inconclusive ... little guidance」、结论「the larger the forecast horizon, the higher is the uncertainty」、NN5 = 111 条序列 / 56 天视界。**第一独立域（同行评审期刊一手全文）**。
- `https://sktime-backup.readthedocs.io/en/v0.22.0/api_reference/auto_generated/sktime.forecasting.compose.make_reduction.html`（sktime v0.22.0 官方 API）— **WebFetch 200 全文逐字**：strategy 三值、windows_identical 两公式与 14 观测/9 窗口/[2,4] 图示、True/False 取舍逐字、recursive 恒定目标、`pooling` 与 `transformers` 仅支持 Recursive 的约束、Bontempi 2013 引用。另 `https://sktime-backup.readthedocs.io/en/v0.15.0/api_reference/auto_generated/sktime.forecasting.compose.make_reduction.html` 与 `https://sktime.readthedocs.io/en/stable/examples/01_forecasting.html`（SlidingWindowSplitter / ForecastingGridSearchCV 时序调参）**WebSearch 快照逐字**。**第二独立域（框架官方文档一手）**。
- `https://www.sciencedirect.com/science/article/abs/pii/S0301479725034139`（2025 河流盐度 LSTM 五策略实证，**Direct/Recursive/DirREC/MIMO/DirMO**）+ `https://cam.tju.edu.cn/en/research/downAchiev.php?id=710`（天津大学 Seq2Seq 多步负荷预测，DirRec 式 (6) 与 MIMO 约束）— **WebSearch 快照逐字**：Direct/MIMO/DirMO 优于 Recursive/DirREC、误差累积在长期尤甚、DirRec「still has the disadvantage ... error accumulation」、MIMO 同结构同输入约束、4h/24h/48h 三视界。**第三 / 四独立域（同行评审实证与高校论文，作交叉）**。
- `http://letsdatascience.com/blog/multi-step-time-series-forecasting-recursive-direct-and-hybrid-strategies` + `https://lacuna.tiptreesystems.com/work/a-review-and-comparison-of-strategies/version/art_ee0e8c0872a0babb188ec1c9058ab4b7` — **二手逐字**：direct 目标 off-by-one 泄露与最新允许 `y_t`、K-fold 不安全与 purge、38/39 配置去季节化改善、MIMO-ACFLIN SMAPE 20.28%、训练/推理成本与四种策略适用表。**教学/转述立场登记，不作唯一结论来源**。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `windows_identical` / `DirRec` / `MIMO` / `multioutput` / `recursive reducer` / `forecast horizon` **全 0 命中**；`误差累积` 命中在 `media/pi-audio` §四（Whisper 长转写 `condition_on_previous_text=False`，音频转写异命题）；`视界` 命中在 `meta/agent-evolution` §r737B-1（固定视界检验只读一次，实验设计异命题）、本技能 §十三（题面「视界越长失效面越大」，可结算性异命题）与 `engineering/vi-fact-verification` §176（`TimeSeriesSplit` 匹配预测视界，交叉验证切分异命题）。按 rules/07 四态判「**优＝加厚现有 `meta/pdi-forecasting`**」，不新建并行层。豆包自留地 **WB 0 落地**。与 r753/r752/r751 九模块结论不复用；本技能 §七~§十四 全无「多步生产策略」命题。
- **未采纳**：NN5 的 Lazy Learning / 去季节化 38/39 数值与 Friedman test、MIMO-ACFLIN SMAPE 20.28%、2025 盐度各点 SMAPE 区间、DIRMO 分块参数、Seq2Seq encoder-decoder 结构与四种策略训练成本表 —— 属 benchmark 数值、模型实现与成本工程，不迁移为通用判据。


## 十六、强调特定结果时的评分规则：加权必须保适当性，否则诱发对冲（r758C · 2026-11-16 实拉）

> 与 §七分工：§七讲评分规则本身是激励设计、只有严格适当规则才使「报真实信念」唯一最优；本节讲**加权这个动作**会把适当性破坏掉，以及想强调尾部/极端事件时哪两类加权仍保适当性。与 §十 r734A-3 分工：那条讲分数差须显著性检验，本节讲加权后仍须检验且样本 100 万也可能不显著。

### 16.1 「按观测权重乘分数」或「只挑已发生的极端样本算普通分」会破坏适当性，把最优预报改成真分布的加权版
- `scoringrules` 官方库《Weighted scoring rules》逐字：「**Gneiting and Ranjan (2011) demonstrate that this is not a proper scoring rule. In particular, if Y ~ G, then the expected score E[w(Y)S(F, Y)] is minimised by a weighted version of G rather than G itself**」；该加权分布密度 `g_w(x) = w(x)g(x) / ∫ w(z)g(z) dz`；当 `w(x)=1{x∈A}` 时，`G_w` 就是 `Y|Y∈A` 的条件分布。
- 预报员困境逐字：「**If we only evaluate forecasts made for extreme outcomes, then it becomes an attractive strategy to always predict that an extreme event will occur, regardless of how likely such an event is ... Lerch et al. (2017) term this the forecaster's dilemma**」；「**such a forecast is useless in practice**」。
- CUSO/Thorarinsdottir 讲义（§6.3.3）逐字：「**a proper scoring rule S is rendered improper if the product with a nonconstant weight function w is formed, where w depends on the observed value y**」，式 (6.22) `S₀(F,y)=w(y)S(F,y)`、式 (6.23) `f(y)=w(y)g(y)/∫w(z)g(z)dz`；「**the restriction of conventional forecast evaluation to subsets of extreme observations by selecting the extreme observations after-the-fact while discarding the nonextreme ones ... will invalidate their theoretical properties and encourage hedging strategies**」。arXiv 2407.15900 逐字：「**when weighting the CRPS by an observed outcome ... propriety is lost. This makes the score unsuitable for objective evaluation and for training**」。
- **判据**：想强调极端事件，**禁止**两种动作 —— ① 事后只保留已发生极端的样本算普通 CRPS/LogS；② 直接 `w(y)×S(F,y)`。二者等价于把评估口径改成「条件于结果」，理论上鼓励永远报极端。固定先问一句：这把加权尺还是不是 proper？「事前声明权重函数」与「事后按观测筛样本」是两件事，前者可救、后者不可救。

### 16.2 保适当性的两条正交路径：threshold-weighted 改积分/变换预测，outcome-weighted 对加权后的预测分布打分
- Gneiting & Ranjan (2011)（JBES 29(3):411-422）官方摘要逐字：「**weighted versions of the continuous ranked probability score. The weighting emphasizes regions of interest, such as the tails or the center of a variable's range, while retaining propriety, as opposed to a recently developed weighted likelihood ratio test, which can be hedged**」——同一篇里「保适当性」与「可被 hedge」是**两种加权**的对比，不能读成「所有加权都安全」。
- `scoringrules` 逐字公式：**threshold-weighted** `twCRPS(F,y;w) = ∫ (F(x) − 1{y≤x})² w(x) dx = E|v(X)−v(y)| − ½E|v(X)−v(X′)|`（`v` 是 `w` 的反导数，Allen et al. 2024）；当 `w(x)=1{x>t}` 可取 `v(x)=max{x,t}`，等价于把预测与观测在阈值处**截尾后再算标准 CRPS**。Matheson & Winkler (1976) 逐字把 CRPS 写成 Brier 分数对所有阈值的积分，并注「**if certain regions of values of the variable are of particular interest, the experimenter might make [w(z)] higher in these regions than it is elsewhere**」。**outcome-weighted** `owS(F,y)=w(y)S(F_w,y)`（Holzmann & Klar 2017），「**is therefore generally proper but not strictly proper**」；`owCRPS(F,y;w)=w(y)∫(F_w(z)−1{y≤z})²dz`。
- 权重函数表（Gneiting & Ranjan 2011 经 Milano 大学讲义 Table 1 逐字转录，实轴变量）：Uniform `w(x)=1` / `v(α)=1`；Center `w(x)=φ(x)` / `v(α)=α(1−α)`；Tails `w(x)=1−φ(x)/φ(0)` / `v(α)=(2α−1)²`；Right tail `w(x)=Φ(x)` / `v(α)=α²`；Left tail `w(x)=1−Φ(x)` / `v(α)=(1−α)²`；且「**the uniform weight, w(z)=1 and v(α)=1, leads to the standard CRPS**」。
- **判据**：报任何「加权分」固定四栏 —— **哪一类加权（threshold / outcome）+ 权重函数 + 阈值或区域 + 是否仍 proper**。uniform 权重退化成标准 CRPS，等于没加权；twCRPS 与 owCRPS 量纲、含义都不同，不可混称「加权 CRPS」。权重函数与阈值必须在**看结果之前**定进台账（与 §7.1「选尺先于下注、禁止结算后挑好看的分」同构，本条把「选权重」一并纳入事前冻结）。

### 16.3 条件/结果加权虽保适当性，却看不见「事件会不会发生」；补救要补二元分且两分量尺度不保证兼容
- `scoringrules` 逐字：「**In evaluating the conditional forecast distribution, these outcome-weighted scoring rules do not take into account the forecast probability that an outcome of interest will occur ... Two forecasts that have the same conditional distribution will therefore receive the same score**」；「**Holzmann and Klar (2017) proposed to remedy this by adding a proper scoring rule for binary outcomes, such as the Brier score ... However, there is no guarantee that the scale of the two scores are compatible, and there is often no canonical choice for the scoring rule for binary outcomes**」（补分不在 `scoringrules` 库内提供）。
- ECB 2016 研讨（Garratt 对 Lerch et al.《Forecaster's Dilemma》的讨论稿）逐字：「**using unweighted (and proper) CRPS and LogS, the perfect model is preferred when using the whole sample but mistakenly the extreme model is preferred if the CRPS and LogS are conditioned on the observed extreme outcomes**」；「**proper weighted scoring rules ... If these are applied then the perfect model is again preferred**」；「**Indicator weight functions ... do not correspond to restricting the evaluation to observed observations which are deemed extreme — instead of excluding them it assigns a zero weight, so the ranking of competing forecasts is retained**」——零权重 ≠ 删除样本，这是保适当性的关键机制差。
- CUSO 讲义逐字：「**the ranking of forecasters should not be solely based on the mean score, even if the sample size seems to be sufficiently large, but confidence intervals should be given**」；「**even for 1 million data points, differences between the forecast scores were often not significant at the 5% level**」。讲义另列 Diks et al. (2011) 的 CL / CSL 条件与删失似然分数作为保适当性的另一族。
- **判据**：极端/高影响事件评估台账分两栏 —— ① **事件是否发生**（二元 Brier 或 CL/CSL）② **事件发生条件下的量级**（条件分/加权分）。只看后者会把「永远报极端但量级准」与「正确报发生概率」判成同分；两分量量纲不保证可加，禁止硬合成一个总分。加权分差仍要做 DM / bootstrap 置信区间，样本量大也不能免（与 §十 r734A-3 互补）。与 §十一 conformal 覆盖保证分工：那条讲区间覆盖的统计保证作用域，本节讲强调尾部时的评分规则适当性。

### r758C 来源与判非（2026-11-16 实拉，逐字核验）
- `https://ideas.repec.org/a/taf/jnlbes/v29y2011i3p411-422.html`（**RePEc/IDEAS 官方著录**，Gneiting & Ranjan 2011《Comparing Density Forecasts Using Threshold- and Quantile-Weighted Scoring Rules》，**Journal of Business & Economic Statistics 29(3):411-422, 2011-07，DOI 10.1198/jbes.2010.08110**）— **WebFetch 200 全文逐字**：完整摘要「emphasizes regions of interest ... while retaining propriety, as opposed to a recently developed weighted likelihood ratio test, which can be hedged」、英格兰银行通胀密度预测与太平洋西北风资源两案例、准确卷期页码与 DOI。**第一独立域（权威著录一手）**。
- `https://scoringrules.readthedocs.io/en/latest/weighted_scores.html`（**scoringrules Python 库官方文档**）— **WebFetch 200 全文逐字**：`w(y)S(F,y)` 非 proper 与 `g_w` 式、指示器权重退化为条件分布、forecaster's dilemma 全段、Holzmann-Klar `owS(F,y)=w(y)S(F_w,y)`「generally proper but not strictly proper」、同条件分布同分、补二元分的尺度不兼容警告、Matheson-Winkler CRPS=Brier 积分、twCRPS/owCRPS/vrCRPS/owES/twES 全族公式、Allen 2024 `v(x)=max{x,t}` 变换、CL/ceLS 定义。**第二独立域（实现库官方文档一手全文，公式级交叉）**。
- `https://statistique.cuso.ch/fileadmin/statistique/user_upload/Thordis-Lectures.pdf`（CUSO 统计课程 Thorarinsdottir 讲义 §6.3.3 ASSESSING EXTREME EVENTS）+ `https://www.ecb.europa.eu/pub/conferences/shared/pdf/20160603_forecasting/Discussion_of_paper_07_by_Lerch_Garratt.pdf`（ECB Forecasting Workshop 2016，Garratt 对 Lerch et al.《Forecaster's Dilemma》讨论稿）+ `https://arxiv.org/html/2407.15900`（极端风速后处理，§3/§4）+ `https://air.unimi.it/retrieve/.../document.pdf`（Milano 大学《Proper Scoring Rules ... Asymmetric Loss Functions》Table 1）— **WebSearch 逐字快照**：式 (6.22)/(6.23)、「after-the-fact ... encourage hedging」、CL/CSL 式、三模型模拟与「perfect model is again preferred」、indicator 权重「assigns a zero weight, so the ranking ... is retained」、五类权重函数表与 uniform 退化、100 万样本仍常不显著。**第三~六域（讲义/央行研讨/同行评审预印本/大学讲义，逐条登记立场；Milano PDF 本批 curl 403 未取得全文，按快照逐字不冒充一手 PDF）**。
- **失败与降级如实登记**：`air.unimi.it` PDF **curl 200 之前一次 HTTP 403 Forbidden**（UA 后仍拒），改用 WebSearch 逐字快照取 Table 1；escholarship PDF（本批 A 轮）**45s TimeoutError**。以上均不冒充已取全文。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `threshold-weighted` / `weighted CRPS` / `tail-weighted` / `quantile-weighted` / `稀有事件` / `extreme event` / `class imbalance` / `极端事件` / `forecaster's dilemma` / `twCRPS` / `owCRPS` **全 0 命中**；`Gneiting` 1 命中在本技能 §7.1（Gneiting & Raftery 2007 **严格适当定义式**）、§十 r734A-2（eq.43 interval score）、§十二（Ranjan & Gneiting 2010 **线性意见池欠自信**）—— 全为**未加权**口径；`Ranjan` 2 命中其一为 `engineering/wb-execute-discipline`（Ranjan Kumar，人名巧合）。按 rules/07 四态判「**优＝加厚现有 `meta/pdi-forecasting`**」，补的是「加权是否保适当性」这一正交层，不重述 §7 Brier 分解/ECE、§十 四把尺、§十二 聚合结论。豆包自留地 **WB 0 落地**。与 r757/r756/r755 九模块结论不复用；A / B 两轮结论亦不复用。
- **未采纳**：vrCRPS 与 owES/twES 多元推广完整公式、de Punder 2023 删失密度解释、Allen 2024 Proposition 4.10、DM 检验拒绝率曲线与三种分布模拟参数、GraphCast/台风个案评测数值、PIT 直方图形状诊断 —— 属实现公式、benchmark 数值与个案，不迁移为通用判据。
