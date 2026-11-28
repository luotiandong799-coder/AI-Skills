# r824A · Brier 分数与概率校准（VI · 2026-11-28 实拉，≥3 独立域一手交叉）

> 全文支撑 `engineering/vi-fact-verification/SKILL.md` §r824A 摘要节。本文件为完整取证与判重留痕，结论不与其正文重复堆叠。

## 主题定位

§十 ECE/温度缩放管「置信度校准」、§十五 Conformal 管「覆盖保证」、§r810A Youden 管「阈值选取」、§r822A DeLong 管「AUC 比较」。本轮补的是**概率预测本身的严格适当评分与三分量分解**：一个分数能否同时反映「准不准（校准）」与「分不分得开（分辨力）」，以及为什么只看单一 Brier 值会把「完美校准但零技能」的预报员判满分。四者互补，不复用结论。

## 三独点

### 独点 1 · Brier 是严格适当评分规则，但单一数值混合了校准与分辨力，低分不等于校准更好

scikit-learn 官方 1.16 逐字：「Strictly proper scoring rules for probabilistic predictions like `sklearn.metrics.brier_score_loss` and `sklearn.metrics.log_loss` assess calibration (reliability) and discriminative power (resolution) of a model, as well as the randomness of the data (uncertainty) at the same time. This follows from the well-known Brier score decomposition of Murphy. As it is not clear which term dominates, the score is of limited use for assessing calibration alone (unless one computes each term of the decomposition). A lower Brier loss, for instance, does not necessarily mean a better calibrated model, it could also mean a worse calibrated model with much more discriminatory power, e.g. using many more features.」

百度百科逐字：「Brier评分是由气象学家Glenn Brier于1950年提出的概率预测模型评估指标。它衡量预测概率与理想情况的偏差,最优值为0。对于二元结果,评分范围在[0,1]之间，是一种严格评分规则」「1973年,Murphy将Brier评分分解为可靠性、分辨能力和不确定项三部分」。

**判据**：报「Brier=X」不写分解项 = 无法判断「准不准」还是「分得开」。验收报告须固定四格 `Brier 总分 / REL / RES / UNC`，缺分解项不得下「校准更好/更差」的结论。

### 独点 2 · Murphy 三分量分解 BS=REL−RES+UNC，其中 REL 要小、RES 要大、UNC 固定

cibo.hk 逐字：「Murphy (1973) 的分解：BS = REL − RES + UNC」「REL = Σ (n_k/N)(f_k − o_k)² ← 校准误差，越小越好」「RES = Σ (n_k/N)(o_k − ō)² ← 分辨力，越大越好」「UNC = ō(1 − ō) ← 结果本身的不确定性，与预报无关」「技能分 SS = (RES − REL)/UNC」。

codeboy.site 逐字：「令 Y∈{0,1},报告概率为 S∈[0,1],总体正例率为 π=EY ... REL=E(S−m(S))²,RES=E(m(S)−π)²,UNC=π(1−π)。则有可靠度—分辨力分解 BS=REL−RES+UNC」「分辨力在恒等式中被减去」「常报基率的预测器可靠度项为零,分辨力也为零;能可靠地区分高低风险的模型,可以在仍然校准的同时获得更低 Brier 分数」。

insightful-data-lab 逐字：「The name 'reliability' is the trap. In ordinary speech a reliable forecaster is a good one, and here the reliability term is an error that you want to be zero.」「Resolution is defined on outcomes rather than on predictions. A model that issues wildly varying probabilities but whose bins all turn out to have the same event rate has no resolution at all — the spread has to appear in what happened, not in what was said.」

**数值反例（cibo.hk 逐字，可当场验算）**：N=1000，基准率 ō=0.2，UNC=0.16。预报员 A 每次都报 0.2 → REL=0、RES=0、BS=0.16、SS=0（完美校准，零技能）。预报员 B：500 次报 0.05（实际 4%），500 次报 0.35（实际 36%）→ REL=0.0001、RES=0.0256、BS=0.1345、SS≈0.159。B 校准误差比 A 大 100 倍，Brier 分数却好 16%。只查 REL 的审计把 A 判满分、B 判不合格。

**判据**：REL 是误差项（越小越好，零不等于好模型）；RES 在恒等式中被减去（越大越好，且必须体现在观测频率而非口头概率的分散）；UNC 由数据固定、跨人群不可直接比（与 §十三谱依赖呼应）。

### 独点 3 · 可靠性图（calibration curve）是分箱后画「预测概率 vs 实际正例频率」，形状诊断比单一数字更可操作

scikit-learn 逐字：「Calibration curves, also referred to as reliability diagrams (Wilks 1995), compare how well the probabilistic predictions of a binary classifier are calibrated. It plots the frequency of the positive label (to be more precise, an estimation of the conditional event probability P(Y=1|predict_proba)) on the y-axis against the predicted probability predict_proba of a model on the x-axis.」「This is accomplished by binning the predictions such that the x-axis represents the average predicted probability in each bin. The y-axis is then the fraction of positives given the predictions of that bin.」

模型偏差的形状指纹（scikit-learn 逐字）：GaussianNB 把概率推向 0/1（条件独立假设失效）、RandomForest 呈 characteristic sigmoid shape（bagging/森林平均难给到接近 0/1 的极值）、LinearSVC 比森林更 S 形（最大间隔方法聚焦边界支持向量）。校准器用 sigmoid(Platt) 或 isotonic 回归，且「Ideally, the calibrator is fit on a dataset independent of the training data used to fit the classifier in the first place ... would result in a biased calibrator that maps to probabilities closer to 0 and 1 than it should」——校准本身也须独立留出集，否则重演 §十泄漏。

**判据**：概率验证的产出是 `可靠性图 + 各箱 n_k/f_k/o_k + BS/REL/RES/UNC + 校准器是否在独立集拟合`，不是「AUC 高所以概率可信」。AUC 只排序、不管概率是否等于真实频率。

## 来源（逐域登记）

- 第一独立域（方法官方一手）：`https://scikit-learn.org/stable/modules/calibration.html`（scikit-learn 1.16 Probability calibration，WebFetch 200 全文逐字：严格适当评分同时评 reliability/resolution/uncertainty、lower Brier≠better calibrated、calibration curve=reliability diagram、分箱轴定义、各模型偏差形状、CalibratedClassifierCV 独立数据拟合）。
- 第二独立域（百科一手）：`https://baike.baidu.com/item/Brier%E8%AF%84%E5%88%86/68714300`（WebSearch 原文快照逐字：Brier 1950 气象学家 Glenn Brier、1950 原论文 Monthly Weather Review、Murphy 1973 三分量、二分类[0,1]、严格评分规则、广义 Brier）。
- 第三、四、五域（可当场验算的技术笔记，立场登记不作唯一来源）：`https://cibo.hk/zh-HK/notes/...Brier...1793812468_83faf9`（BS=REL−RES+UNC、SS=(RES−REL)/UNC、A/B 两预报员数值反例）、`https://www.codeboy.site/foundations/tcs/learning-theory/brier-score-decomposition.html`（REL/RES/UNC 定义与符号、常报基率反例）、`https://insightful-data-lab.com/2025/08/21/murphys-decomposition/`（reliability 命名陷阱、resolution 定义在结果而非预测、100 预报算例）。
- 诚信登记：`https://en.wikipedia.org/wiki/Brier_score` 的 WebFetch 触发本地回退禁用（CODEBUDDY_WEBFETCH_DISABLE_LOCAL_FALLBACK=1），未取全文，不冒充 200；上述结论全部来自已取到的官方页与可验算笔记，不依赖维基。

## 判重

全库 WB 侧 SKILL.md / module-memory / co-learn 精确扫描 `Brier` / `brier_score_loss` / `可靠性图` / `reliability diagram` / `Hosmer` / `校准曲线` / `calibration curve` **全 0 命中**；`calibration` 命中为 §一 ECE/温度缩放（分类置信度校准）、§十五 Conformal 校准集、豆包自留地 wb-context-compressor，均异命题。与 §十/§十五/§r810A/§r822A 分工明确、结论不复用。豆包自留地 WB 0 落地。
