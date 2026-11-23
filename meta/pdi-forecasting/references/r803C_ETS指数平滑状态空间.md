# r803C｜PDI｜二十九、ETS 指数平滑状态空间模型：把点预测升级为可自动选模+给区间的统一框架

访问日期：2026-11-23；本轮独立实拉禁止复用上轮。

## 一手来源（逐字 + URL + 日期）

1. Rob J Hyndman《The tourism forecasting competition》（robjhyndman.com/papers/forecompijf.pdf，PDF fetch 失败；正文取自 WebSearch 逐字快照，2026-11-23，未冒充 PDF 全文）：
   - "Ord et al. (1997), Hyndman et al. (2002) and Hyndman et al. (2005)... have developed a statistical framework for the exponential smoothing methods. The statistical framework incorporates stochastic models, likelihood calculations, forecast intervals and procedures for model selection."
   - "We select models by minimising the AIC amongst all models (both additive and multiplicative), then compute forecast intervals from the selected models using analytical formulae, or by simulation if the analytical formulae are not available."
   - "We label this method ETS in the tables that follow. The three letters are an abbreviation of 'ExponenTial Smoothing', and also specify the three components of the stochastic model: Error, Trend and Seasonality. For example, an ETS(A,A,A) is a Holt-Winters' additive method with an additive error component."

2. Hyndman R 讲义 ANU《Time series and forecasting in R》（maths-people.anu.edu.au/~johnm/courses/r/ASC2008/pdf/Rtimeseries-ohp.pdf，WebFetch 200 全文逐字，2026-11-23）：
   - 分类表（逐字）：Trend ∈ {N, A, Ad(additive damped), M, Md(multiplicative damped)}；Seasonal ∈ {N, A, M}；"General notation ETS(Error,Trend,Seasonal)"；"ETS(A,N,N): Simple exponential smoothing with additive errors. ETS(A,A,N): Holt's linear method with additive errors. ETS(A,A,A): Additive Holt-Winters' method."
   - "Ord, Koehler & Snyder (JASA, 1997) and Hyndman, Koehler, Snyder and Grose (IJF, 2002)... showed that all ES methods (including non-linear methods) are optimal forecasts from innovation state space models."
   - "Apply each of 30 methods that are appropriate to the data. Optimize parameters and initial values using MLE... Select best method using AIC: AIC=−2 log(Likelihood)+2p where p=# parameters. Produce forecasts using best method. Obtain prediction intervals using underlying state space model. Method performed very well in M3 competition."
   - ETS(M,A,M) 状态方程与约束："where 0≤α≤1, 0≤β≤α, 0≤γ≤1−α and m is the period of seasonality."

3. Forecast Studio《Exponential smoothing and ETS models: from simple smoothing to Holt-Winters》（forecaststudio.com.mx/blog/exponential-smoothing-ets，WebFetch 200 全文逐字，2026-11-23）：
   - "Simple exponential smoothing... ℓ_t=α·y_t+(1−α)·ℓ_{t−1} with 0<α<1. A high α reacts fast to recent changes (and to noise); a low α smooths harder. In practice α is fit by minimizing the sum of squared one-step errors, not chosen by hand."
   - "ETS stands for Error, Trend, Seasonal — each with none/additive/multiplicative options, giving up to 30 model variants (Hyndman, Koehler, Snyder & Grose, 2002)... Framing exponential smoothing as a state-space model gives it... a proper likelihood, which means AICc-based automatic model selection and analytically derived prediction intervals rather than only point forecasts (Hyndman & Athanasopoulos, FPP3 §8.8)."
   - "Additive — seasonal swings of roughly constant size regardless of the level. Multiplicative — seasonal swings that scale with the level (a bigger baseline means a bigger seasonal bump in absolute terms) — the common case for demand data with strong growth."
   - "Neither class is universally superior (FPP3 §9.10), and Gardner's review of five decades of empirical evidence finds exponential smoothing remarkably robust in practice... ETS... requires no stationarity pre-processing, unlike ARIMA."

4. cttir《ETS Models》（cttir.github.io/tutorials/tutorials/time-series/ets-models.html，WebFetch 200 全文逐字，2026-11-23）：
   - "The state-space framework allows proper likelihood-based estimation, AIC-based model selection, and principled prediction intervals derived from the underlying stochastic structure rather than ad-hoc heuristics."
   - "Multiplicative components require strictly positive data; the AIC-based selection avoids choosing an invalid model."；"For complex multi-seasonality (e.g. weekly + yearly), TBATS... extends ETS with multiple seasonal layers and Box-Cox transformation."
   - "checkresiduals() provides Ljung-Box and graphical diagnostics."；"ETS prediction intervals can be very wide at long horizons because the multiplicative variance compounds; for a more nuanced view, simulate many sample paths."
   - 报告句式："Always state the chosen ETS specification and the smoothing parameters."

5. CTModelling《ETS模型》（ctmodelling.cn/talk/wangjiahe_ets_r，WebFetch 200 全文逐字，2026-11-23）：
   - "核心思想是通过对过去数据赋予指数递减的权重... 简单指数平滑：适用于没有明显趋势和季节性的平稳时间序列。霍尔特线性趋势模型：...线性趋势但无季节性。霍尔特-温特斯季节性模型：...趋势和季节性。包括加法型和乘法型两种季节性模型。"
   - "通过状态空间表示，提供了一个系统化的方式来表示和选择不同的误差、趋势和季节性成分的组合。"

## 判非（不采 / 边界）

- 不把 ETS 当单一模型：它是 30 个变体的族，必须报三字母规格 + 平滑参数，不能只说"指数平滑"。
- 不手调 α/β/γ：一手原文明确"fit by minimizing the sum of squared one-step errors, not chosen by hand"，由 AIC/AICc 自动选模。
- 乘性成分要求数据严格为正（cttir），遇含零序列须改用加性或换模型；本条不替代 §二十八 Croston 的间歇需求处理。
- 长视界乘性 ETS 区间会因方差复合变得极宽，须用模拟多路径而非只报解析区间。
- 不宣称 ETS 普遍优于 ARIMA：FPP3 §9.10 明言无universally superior，Gardner 2006 只说稳健；选型须滚动起点 CV 实测（本技能 §十七/§十五分工）。
- 与 §十七回测协议（purge/embargo/CPCV）分工：那里管防泄漏，这里管模型族本身；与 §二十八 Croston 分工：那里管零膨胀间歇需求，这里管一般趋势/季节序列。
- Hyndman PDF WebFetch 失败、MDPI 类页面曾返回空 Title —— 对应正文取 WebSearch 逐字快照已如实登记，未冒充已读全文。
- 豆包自留地 WB 0 落地；全库 PDI SKILL.md `ETS/指数平滑` 无专节（仅 §十五一处把 ARIMA 当模型名举例）。
