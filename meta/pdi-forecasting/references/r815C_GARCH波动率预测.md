# r815C GARCH 波动率预测（全文 · 2026-11-27 实拉）

## 一手来源与逐字要点
1. AI-PM《波动率建模：ARCH 与 GARCH》 — https://aipm.ac/business/14-financial-econometrics/04-volatility-modeling-arch-and-garch （WebFetch 200 全文逐字）
   - 波动率聚集：大波动后跟大波动；条件同方差下残差方差为常数无法刻画，需条件异方差。ARCH 对 ε_t² 拟合 AR、GARCH 拟合 ARMA，GARCH 抓相关所需阶数小。
   - GARCH(1,1)：`σ_t²=α₀+α₁ε_{t−1}²+β₁σ_{t−1}²`；α₀>0、α₁,β₁≥0 保正；α₁+β₁<1 弱平稳；无条件方差 α₀/(1−α₁−β₁)；α₁+β₁ 是持续性，近 1 衰减极慢。
   - 四类检验不可混：ε̂_t 序列相关判均值方程充分；ε̂_t² 的 Q 检验判 ARCH 效应（IBM Q(12)=726.34/p≈0）；标准化残差 v̂_t 的 Q 判均值方程；v̂_t² 的 Q 判波动率方程。Engle LM 辅助回归 `ε̂_t²=α₀+Σαᵢε̂_{t−i}²`，`LM=T·R² ~ χ²(q)`，IBM q=6 → LM=385.48；q 按 ε̂² 的 PACF 定。
   - QMLE：`y_t=φ₀+φ₁y_{t−1}+ε_t, ε_t=σ_t v_t, v_t~iid N(0,1)`，条件对数似然 `L=−(T−1)/2·log(2π) −½Σ log σ_t² −½Σ(y_t−φ₀−φ₁y_{t−1})²/σ_t²`；v_t 非正态时大样本仍一致但不有效（QMLE，截面 OLS 即特例）；VaR/置信区间需标准化残差非参数密度估分位。
   - 诊断：v̂_t=ε̂_t/σ̂_t 应白噪声、v̂_t² 无序列相关；峰度>3 改 Student-t（IBM 峰度 7.98 → df≈5.8，AIC −5.542→−5.628）；定阶试 (2,1)/(1,2)，负系数或不显著高阶退回 (1,1)，EViews 不自动施正性约束。
   - 预测：一步 σ_{t+1}² 在 F_t 已知；多步 `E_t(σ_{t+j}²)=α₀+(α₁+β₁)E_t(σ_{t+j−1}²)` 收敛无条件方差；区间 `ŷ_{t+1}±1.96σ̂_{t+1}`（t 分布按 df 取分位）；两步误差方差 `c₁²σ_{T+1}²+c₂²σ_{T+2}²` vs 同方差 `(c₁²+c₂²)σ²`。
   - 扩展：GARCH 对冲击符号不敏感，EGARCH 与 GJR/Threshold 引入符号；还有 GARCH-M / IGARCH / GARCH-MIDAS。
2. 玻尔科学百科《GARCH 模型：原理、估计与应用》 — https://scipedia.bohrium.com/sciencepedia/feynman/keyword/garch_model_estimation （WebFetch 200 全文逐字）
   - 三成分：ω 恒定基准方差 + αε² 昨日冲击新信息 + βσ² 昨日方差记忆（「祖母讲故事」）；β 一参数创造对所有过去冲击的无限递减记忆，简约性使 GARCH(1,1) 常优于高阶 ARCH。
   - 持久性 α+β 近 1 → 崩盘动荡很久才消散；稳定条件 α+β<1；长期方差 `σ²=ω/(1−α−β)`，可反推 β。
   - EGARCH 方程：`ln(σ_t²)=ω+α(|z_{t−1}|−E|z_{t−1}|)+γ z_{t−1}+β ln(σ_{t−1}²)`；γ<0 时负冲击 z<0 对 log 方差贡献为正 → 推高未来波动（杠杆效应）。
   - 验证：标准化残差 ẑ_t=ε_t/σ̂_t 应 iid 零均值单位方差无自相关、ẑ_t² 也无自相关；Shapiro-Wilk 检正态，失败可用更厚尾 t 分布。
   - 跨域：GARCHX 加指示变量测事件影响；DDoS 使标准化平方新息系统性超阈值 → 异常检测；GARCH-EVT 组合测黑天鹅；期权路径模拟。
3. 交叉 WebSearch：百度百科（Engle 1982 ARCH / Bollerslev 1986 GARCH / IGARCH / GARCH-M）· MBA 智库（GJR 1989 / EGARCH 1991 / GARCH 不能解释负相关与非对称 / 正性约束致估计震荡）。

## 诚信与判非
- 判重：全库 SKILL.md 对 `GARCH` / `条件异方差` / `波动率聚集` / `ARCH 效应` 0 专节；wb-context-compressor「volatility 混合策略」是上下文注入时机异命题，vi-fact-verification Bland-Altman「异方差」一句异命题。
- 豆包自留地 WB 0 落地。按 rules/07「优＝加厚现有」：加厚 `meta/pdi-forecasting`，0 新建。
- 波动率建模产出的是区间宽度/风险测度，不是均值方向预测；不与 Prophet/ETS/CUSUM 混为一谈。
