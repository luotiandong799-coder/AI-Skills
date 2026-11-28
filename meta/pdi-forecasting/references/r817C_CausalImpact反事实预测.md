# r817C · CausalImpact 反事实预测：用预处理期拟合结构时间序列，推断干预后「如果没发生」的响应

> PDI · 2026-11-28 独立实拉 · ≥2 独立域一手交叉（Google Research 官方出版页 WebSearch 逐字摘要 + Project Euclid《Annals of Applied Statistics》9(1):247-274 官方摘要 WebSearch 逐字 + Google CausalImpact 官方 README/R vignette raw GitHub WebFetch 200 全文逐字）· 3 独点。

## 判重与定位
- 全库 `SKILL.md`+`module-memory`+`co-learn` 对 `CausalImpact`/`贝叶斯结构时间序列`/`BSTS`/`反事实预测`/`合成控制` 0 命中（TI 因果森林/CATE 是异命题：那管从横截面估计异质性处理效应，这里管**单条时间序列**在干预后的反事实路径）。豆包自留地 WB 0 落地 ⇒ 按 rules/07「增＝加厚现有」0 新建。
- 分工：§r812C Prophet 管趋势/季节/节假日分解拟合、§r815C GARCH 管条件方差与区间、§r754C 管多步策略、§r762C 管回测防泄漏；本章管**没有随机实验时，如何用对照序列预测「干预未发生」的同期响应并把差值结算为因果效应**。
- 边界先行：这是观察数据的因果归因，结论依赖强假设；不替代随机实验（论文原话 those settings where a randomised experiment is unavailable）。

## 独点1 · 模型形态与三类优于经典 DiD 的能力（论文摘要逐字）
- 论文：Brodersen KH, Gallusser F, Koehler J, Remy N, Scott SL. *Inferring causal impact using Bayesian structural time-series models*. Annals of Applied Statistics, 2015, 9(1):247-274（版权 IMS 2015；Google Research 出版页 pub41854）。
- 原文逐字：提出基于 **diffusion-regression state-space model** 推断因果影响，「predicts the counterfactual market response in a synthetic control that would have occurred had no intervention taken place」；用 MCMC 做 posterior inference。
- 相对经典 difference-in-differences 的三项增量（摘要逐字）：(i) infer the temporal evolution of attributable impact（能给出影响随时间的演化，而非单一前后差）；(ii) incorporate empirical priors on the parameters in a fully Bayesian treatment；(iii) flexibly accommodate multiple sources of variation，包括 local trends、seasonality、time-varying influence of contemporaneous covariates（即**合成控制**：用未受干预的对照时间序列线性组合重建反事实）。
- 实测场景：在线广告活动对 search-related site visits 的影响；R 包 `CausalImpact` 为参考实现。

## 独点2 · 结构分量、反事实构造与结算口径（R 官方 vignette 逐字）
- 输入 = 响应序列（如 clicks）+ 一组**自身未受干预影响**的对照序列（如未受影响市场的 clicks/其他站点 clicks）；`CausalImpact(data, pre.period, post.period)` 装配 BSTS 模型、做 posterior inference、算因果效应估计。pre 期训练，post 期把观测响应置 `NA` 后预测反事实（自定义模型时逐字：「the counterfactual response is unobserved after the intervention」），再用真实观测减预测得 pointwise 效应。
- 结构分量（官方参数说明逐字）：local level = 高斯随机游走，`prior.level.sd` 默认 0.01（低残差波动的稳定数据），拿不准用 0.1（合成数据验证过，但区间可能过宽）；季节 `nseasons`（日粒度用 7 表 day-of-week；当前接口**只支持一个季节分量**，多个要用 `bsts` 自构后传 `bsts.model`）、`season.duration`（小时粒度 day-of-week 用 `nseasons=7, season.duration=24`）；回归系数默认静态，`dynamic.regression=TRUE` 可放松时变假设，但与时变 local level/trend 同用常 **overspecification**，静态更安全。
- 变量选择：用 posterior inclusion probabilities 看哪些对照序列进模型（`plot(impact$model$bsts.model, "coefficients")`，条长=纳入概率，着色=系数非零时为正/负的条件概率，灰=正负同概率）。`standardize.data=TRUE` 用**预处理期**矩标准化，等价于经验贝叶斯设先验、保证对线性变换不变；`niter` 默认 1000 次 MCMC。
- 三幅图逐字：第一幅数据与 post 期反事实预测；第二幅观测−反事实=**pointwise** 因果效应；第三幅把 pointwise 累加=**cumulative** 效应。数值摘要 `summary(impact)`：**Average** 列是 post 期时间平均、**Cumulative** 列是逐点求和——只有流量型变量（queries/clicks/visits/installs/sales/revenue）适合累计；存量型（current subscribers/stock price）不能跨时间有意义地相加，画图应只取 `c("original","pointwise")`。示例真值注入 10、 recovered 平均 99 vs 预期 89 = 效果 11、95% posterior interval [9.8, 11] 不含 0 即判有因果效应；`summary(impact, "report")` 给文字版，`impact$summary` 给全精度数值。

## 独点3 · 强假设与「 placebo 自检」（不把拟合优度当因果成立）
- 官方 README 逐字：「As with all approaches to causal inference on non-experimental data, valid conclusions require strong assumptions」；两条核心假设：①存在一组**自身未受干预影响**的对照时间序列（若受影响，会低估/高估真实效应，甚至假阳性）；②预处理期建立的「协变量↔处理序列」关系在 post 期保持稳定（可用 dynamic.regression 放松，但与主题模型过配冲突）。
- 假设检查（vignette「elephant in the room」段逐字）：先逐条论证纳入的协变量为何未受干预影响、画全部协变量做视觉 sanity check；再检验 y 在**干预开始前**的可预测性——「running CausalImpact() on an imaginary intervention」，检查假干预期是否**无显著效应**（反事实与实际应接近）；显著即说明模型/对照选择不可信。
- 其他口径：先验必须显式列出并告知受众（尤其 `prior.level.sd`，在模型假设这条上不能只报效应值）；响应列可含 `NA`、**协变量列不可含 NA**（否则插补或剔除该回归元）；自定义模型要把 post 期响应置 NA 并另传真实观测供计算差值。
- 与 PDI 其他节分工：不防结构突变（pre 期关系一旦断裂，post 反事实失效）、不防干预溢出到对照序列、不等于随机实验的内部效度；本节给的是「点预测+累积/平均结算+区间+假设自检」的完整闭环，与 §r794C conformal 的**覆盖保证**互补（conformal 给边际覆盖，不给因果解释）。

## 来源（URL + 抓取日期 + 状态）
- `https://research.google/pubs/pub41854` — WebSearch 2026-11-28 命中官方出版页逐字摘要（diffusion-regression state-space / counterfactual market response / (i)(ii)(iii) / MCMC / online advertising / CausalImpact R package）。第一独立域·官方一手（直接 WebFetch 被本地回退禁用，如实登记，取 WebSearch 逐字）。
- `https://projecteuclid.org/journals/annals-of-applied-statistics/volume-9/issue-1/Inferring-causal-impact-using-Bayesian-structural-time-series-models/10.1214/14-AOAS788.full` — WebSearch 2026-11-28 命中 IMS 官方摘要逐字（2015, Vol.9 No.1 247-274 / synthetic control / local trends seasonality time-varying covariates / strengths and limitations）；WebFetch 被 Incapsula 拦截如实登记。第二独立域·期刊官方一手。
- `https://raw.githubusercontent.com/google/CausalImpact/master/README.md` + `https://raw.githubusercontent.com/google/CausalImpact/master/vignettes/CausalImpact.Rmd` — WebFetch 200 全文逐字（假设与强假设声明 / pre-post 切分 / 反事实 / 三面板图 / Average vs Cumulative / stock vs flow / 95% posterior interval / placebo imaginary intervention / 参数与先验 / NA 限制）。第三独立域·官方实现一手。

## 不防什么
- 不防对照序列被干预污染、pre-post 关系漂移、结构突变、先验误设；不替代随机实验；不提供 conformal 式有限样本覆盖保证；存量型响应不可累计；不自动给出「对照为何未受影响」的论证（须人给出并自检）。
