# r802B 逐字全文与判非｜序贯检验与 peeking｜2026-11-23 实拉

## 独点
1. 固定样本 p<0.05 只对"看一次"成立；重复看假阳性累积 1/5/10/20 次≈5%/19%/30%/54%；机制=零假设下运行 z 是随机游走、看够多次必穿越阈值。
2. 解法一 alpha spending：总 α 分摊各 interim，每次更严；OBF 早期极保守（首次 |z|>3.438 p<0.0006，末次 p<0.0471）把大部分留给终点，Pocock 均分（两次各 p<0.015 双侧）；Lan-DeMets flexible 允许不固定次数。
3. 解法二 e-value/always-valid：e_t=e_{t-1}×LR_t，e_t≥1/α 即停，任意停止策略（含自主决定）有效；代价=区间更宽/无早停更慢+最短运行时护栏；只管统计错误不管短期≠稳态。

## 一手逐字（第一独立域）
- 来源：https://gravityfield.ai/glossary/sequential-testing （WebFetch 200 全文）
- "A classical frequentist A/B test requires the sample size to be fixed in advance... Watching interim results and stopping once it looks significant is peeking."
- "At a threshold of p < 0.05 the false positive rate is fixed at 5% — for one check. Repeated checks accumulate: 1 check → false positives ~5% / 5 checks → ~19% / 10 checks → ~30% / 20 checks → ~54%"
- "The total type I error budget of 0.05 is spent according to a defined function across the interim checks. Each check uses a stricter threshold... total spend never exceeds 0.05."
- "An e-value is an accumulating measure of evidence: e_t = e_{t-1} × LR_t (the product of likelihood ratios at each step). The test can stop when e_t ≥ 1/alpha. The key property is that validity holds under any stopping strategy — including a discretionary one."
- 商业立场已登记（Gravity Field 自身卖贝叶斯连续监控）；数字仅取其统计口径，不采其产品结论。

## 一手逐字（第二独立域 · 医学教材原文）
- 来源：https://www.sciencedirect.com/topics/medicine-and-dentistry/interim-analysis （WebFetch 200 全文，Elsevier 教材章节汇编）
- "Testing twice with a 5% risk of error each time leads to an approximately 10% overall risk of error. To maintain the overall 5%, α is split for the repeated testing times, effectively exacting a penalty for interim testing. The choice of critical p-values is often likened to a spending function, where the available amount in the budget to spend is α."
- "Pocock proposed that α be split equally among the k analyses."；"Pocock method assumes an equal number of patients... between tests"
- "O'Brien and Fleming proposed to reserve most of the type I error for the final analysis."；"sets a very stringent standard for the first interim test"；"On the first interim analysis, the absolute value of the test statistic must exceed 3.438 to be considered significant (p<0.0006)... second, it must exceed 2.431 (p=0.0151). Finally... must exceed 1.985 (p=0.0471)"
- "More flexible approaches, called flexible group sequential (alpha-spending) methods, allow investigators to determine how often and when to peek... Examples ... Lan and DeMets, Wang and Tsiatis, Hwang, Shih, and De Cani."
- 伦理："If a new regimen is convincingly demonstrated to be superior to the active control, there is an ethical obligation to stop the randomization..."

## 一手逐字（第三/四/五域 · WebSearch 快照交叉）
- https://www.growthstack.dev/glossary/peeking-problem："daily checking over a 30-day experiment can inflate the false positive rate to 25% or higher"；"random walks"；"the maximum over multiple looks has a larger expected absolute value"；mSPRT / always-valid confidence sequences（Howard, Ramdas）
- https://www.calibreos.com/decoder/sequential-testing："an always-valid interval is wider than a fixed-sample one at the same sample size"；"Enforce a minimum runtime of at least one full weekly cycle regardless of what the sequential test says"；"sequential validity ... controls the statistical error, not the mismatch between a short measurement window and a long-run question"
- https://markusloecher.github.io/pValue-Hacking-Solutions：recommend 顺序 group-sequential（gsDesign/rpact）→ mSPRT/Beta-Binomial → e-values/always-valid p-values/online FDR

## 判非（去重五层）
- VI 技能对 `序贯`/`sequential`/`alpha spending`/`peeking`/`always-valid`/`e-value`/`O'Brien-Fleming`/`Lan-DeMets` 0 专节（description 词条本轮新增，非既有）。
- §十一多重检验校正=横向 family（一次内 m 条结论），本条=纵向同一检验反复看，正交不复用。
- 全库命中：`meta/agent-evolution` mSPRT 早停语境（异命题，仅对比提及）；豆包自留地 wb-execute-discipline/wb-context-compressor；co-learn 与配置文档——WB 0 落地。
- 数字均挂可复拉 URL；未冒充 RCT 原始论文（医学为教材章节汇编、三 glossary 为工具/教学站，一手数字口径可复拉，立场已登记）。
- 未采纳：Lan-DeMets 具体 spending 函数公式、confidence sequence 的 Ville 不等式证明（超出验收口径）。
