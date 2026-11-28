# r820C · ARIMA / Box-Jenkins：用自相关结构建模，与 ETS 是互补而非包含（全文）

> 来源：Rob J Hyndman & George Athanasopoulos《Forecasting: Principles and Practice》3rd ed. §9 ARIMA（otexts.com/fpp3/arima.html，WebFetch 200 全文逐字）+ §2.8/2.9 ACF（otexts.com/fpp3/acf.html，WebFetch 200，页面未含 PACF/Ljung-Box 如实登记）+ Minitab 官方《拟合 ARIMA 模型》中文支持页 + 玻尔科学百科《博克斯-詹金斯方法论》+ StatisticsEasily《Box-Jenkins》+ GitHub apachecn 译《Box-Jenkins 方法简介》（WebSearch 逐字，第二独立域）。落点 `meta/pdi-forecasting/SKILL.md` §三十四 → 1.28.0。PDI 模块 · 2026-11-28 实拉。

## 独点1 ARIMA(p,d,q) 定义、差分与后移算子

**定位**（与 §r803C ETS 互补）：FPP3 逐字「Exponential smoothing and ARIMA models are the two most widely used approaches to time series forecasting, and provide complementary approaches to the problem. While exponential smoothing models are based on a description of the trend and seasonality in the data, ARIMA models aim to describe the autocorrelations in the data.」ETS 描述趋势/季节/误差类型，ARIMA 描述观测值与过去值、过去误差的相关结构。

**平稳性与 d**：平稳=「statistical properties do not depend on the time at which the series is observed」，形式化 `(y_t,…,y_{t+s})` 分布不随 t 变；趋势/季节非平稳，白噪声平稳；有周期但无固定周期长度的循环行为反而平稳。差分 `y'_t=y_t−y_{t−1}` 稳定均值（对数变换稳定方差）；二阶差分 `y_t−2y_{t−1}+y_{t−2}`，「almost never necessary to go beyond second-order differences」；季节差分 `y_t−y_{t−m}`（月 m=12，季 m=4）。**过度差分警告**：「applying more differences than required will induce false dynamics or autocorrelations that do not really exist...do as few differences as necessary」，Minitab 补信号=第一个自相关接近 −0.5 且其他位置小值即过度差分。用 KPSS 检验（原假设平稳，p<0.05 建议差分）定 d、`unitroot_ndiffs`/`unitroot_nsdiffs`（季节 F_S<0.64 不差分）。

**模型式**（式9.1）：`y'_t = c + φ₁y'_{t−1}+…+φ_p y'_{t−p} + θ₁ε_{t−1}+…+θ_q ε_{t−q} + ε_t`；后移算子 `(1−φ₁B−…−φ_pB^p)(1−B)^d y_t = c + (1+θ₁B+…+θ_qB^q)ε_t`，即 `φ(B)(1−B)^d y_t = c + θ(B)ε_t`。p=AR 阶、d=一阶差分次数、q=MA 阶。特例：white noise=ARIMA(0,0,0)、random walk=ARIMA(0,1,0)、带漂移 random walk=ARIMA(0,1,0)+常数、AR(p)=ARIMA(p,0,0)、MA(q)=ARIMA(0,0,q)。AR(1) `-1<φ₁<1`（=1 变随机游走）；MA(1) 可逆性 `-1<θ₁<1`（|θ|>1 远观测权重反更大不合意义）。平稳 AR(p) 可写 MA(∞)，可逆 MA(q) 可写 AR(∞)。

**常数 c 决定长期预测**：c=0,d=0→趋 0；c=0,d=1→趋非零常数；c=0,d=2→沿直线；c≠0,d=0→趋均值；c≠0,d=1→沿直线；c≠0,d=2→二次趋势「not recommended，fable 不允许」。d 越大预测区间增长越快；d=0 长期区间收敛到历史标准差、d≥1 持续增长。

## 独点2 ACF/PACF 定阶的适用范围、Box-Jenkins 流程与诊断

**ACF/PACF 识别（有前提！）**：FPP3 逐字「If the data are from an ARIMA(p,d,0) or ARIMA(0,d,q) model, then the ACF and PACF plots can be helpful...If p and q are both positive, then the plots do not help in finding suitable values of p and q」。纯 AR(p,d,0)：ACF 指数衰减或正弦、PACF 在 lag p 显著尖峰且之后无；纯 MA(0,d,q)：PACF 指数衰减或正弦、ACF 在 lag q 显著尖峰且之后无；ARMA 混合两者都拖尾，须 AICc 网格。季节部分看季节滞后：ARIMA(0,0,0)(0,0,1)₁₂ 在 lag12 ACF 尖峰 + PACF 季节滞后指数衰减；ARIMA(0,0,0)(1,0,0)₁₂ 反之。PACF 是「去除 lag1..k−1 影响后 y_t 与 y_{t−k} 的关系」，第 k 个偏自相关=AR(k) 中 φ_k 的估计。ACF 显著性带 `±1.96/√T`（T=50 时 ±0.28），超过 5% 尖峰越界或一个大尖峰越界即非白噪声（FPP3 §2.9）。

**Box-Jenkins 三阶段迭代**（Box & Jenkins 1970《Time Series Analysis: Forecasting and Control》，基于 Wold 分解，玻尔百科/StatisticsEasily/Minitab 三源交叉）：①识别 identification=平稳性+定 d（单位根检验逐轮重复）+ACF/PACF 定 p,q；②估计 estimation=MLE（fable 用 MLE，类似最小化 Σε²；不同软件估计法/优化器不同答案略异）；③诊断 diagnostic checking=残差 ACF/PACF 白噪声 + Ljung-Box portmanteau，有大尖峰即改模型，再回到识别迭代。FPP3 完整七步：绘图识别异常→Box-Cox 稳方差→差分至平稳→ACF/PACF 判纯 AR/纯 MA→AICc 搜更优→残差 ACF+portmanteau 检验→白噪声后预测。Hyndman-Khandakar 算法只管步骤 3–5，其余人工。

**残差检验自由度修正**：ARIMA 的 portmanteau 检验用 `ℓ−K` 自由度（ℓ=检验滞后数，K=p+q 为 AR+MA 参数数），否则检验不准——与 §r803C ETS 残差 Ljung-Box 直接套不同，此处须扣参数数。AICc 只在**同模型类、同差分阶数**内可比：「information criteria tend not to be good guides to selecting the appropriate order of differencing (d)...differencing changes the data on which the likelihood is computed」⇒ 先用单位根定 d，再 AICc 选 p,q；**AICc 不能跨 ETS/ARIMA 比较**（似然算法不同）。

**自动定阶**（fable ARIMA()，Hyndman-Khandakar 变体）：重复 KPSS 定 0≤d≤2 → 差分后 AICc 最小选 p,q，先拟 (0,d,0)/(2,d,2)/(1,d,0)/(0,d,1) 及 d≤1 时无常数版 → 邻域 p±1/q±1/include-exclude c 贪心搜到 AICc 不再降；`greedy=FALSE` 全邻域、`approximation=FALSE` 关近似、`stepwise=FALSE` 更大搜索空间。d>1 常数总是省略（二次以上趋势危险）。

## 独点3 预测机制、区间偏窄与不防什么

点预测三步：展开方程使 y_t 在左→t 换 T+h→未来观测换预测值、未来误差换 0、过去误差换对应残差，h=1,2,…递推。一期区间 `ŷ_{T+1|T} ± 1.96σ̂`（对所有 ARIMA 成立）；ARIMA(0,0,q) 多步 `σ̂²_h=σ̂²[1+Σ_{i=1}^{h−1}θ̂²_i]`。区间基于残差不相关且正态假设，不满足则错；残差不正态但无相关可 `bootstrap=TRUE`。**ARIMA 区间偏窄**（「tend to be too narrow」）：只算了误差变动，没算参数估计变异、模型阶数不确定性、历史模式延续假设风险——与 §r806B conformal 给有限样本覆盖保证、§r734A 区间联合约束分工不同，ARIMA 区间不给条件覆盖保证。

**ETS↔ARIMA 关系不是谁包含谁**：FPP3 逐字「It is a commonly held myth that ARIMA models are more general than exponential smoothing」——线性 ETS 都是 ARIMA 特例（ETS(A,N,N)=ARIMA(0,1,1) θ₁=α−1；ETS(A,A,N)=ARIMA(0,2,2)），但非线性 ETS 无 ARIMA 对应、很多 ARIMA 无 ETS 对应；**所有 ETS 非平稳，部分 ARIMA 平稳**。d=0 平稳 ARIMA 预测区间收敛、ETS 全非平稳故不收敛。AICc 只能同类内选模。

**落地口径与边界**：报「用了 ARIMA」写 p/d/q（+季节 P/D/Q,m）/是否含常数/定阶方式（ACF-PACF 还是自动 AICc）/残差诊断四件；d 由单位根定不由 AICc 定；样本一般≥50（Minitab/百科口径）；数据<50 或强非线性/多外生变量不适用。不防：过度差分引入伪动态、p,q 均正时 ACF/PACF 失效需网格、ARIMA 区间偏窄（不含参数与阶数不确定性）、结构突变、与 ETS 跨类比较的误用。与 §r803C ETS（趋势季节误差族+AICc 自动选模+区间解析）、§r815C GARCH（条件异方差）、§r754C 多步策略、§r762C 回测协议分工不复用。

**来源与判非**：FPP3 §9 arima.html（WebFetch 200 全文逐字：定义/平稳/差分/后移算子/AR/MA/ARIMA(p,d,q)/常数/ACF-PACF 表/Box-Jenkins 七步/portmanteau dof/AICc 局限/季节/自动定阶/预测/区间/ETS 关系等价表）+ FPP3 §2.8 acf.html（WebFetch 200：ACF 定义/显著性带/白噪声，页面未含 PACF/Ljung-Box 如实登记）；Minitab 官方中文《拟合 ARIMA 模型》+ 玻尔科学百科《博克斯-詹金斯方法论》（Wold 分解/三阶段）+ StatisticsEasily + GitHub apachecn 译（WebSearch 逐字，第二独立域）。判重：全库 SKILL.md+module-memory 对 `ARIMA`/`Box-Jenkins`/`ACF`/`PACF` 0 专节（仅 §r803C ETS 与 ARIMA 无 universal winner 一句对照、§r815C GARCH 用 PACF 定 q 一句异命题），豆包自留地 WB 0 落地，按 rules/07「增＝加厚现有」0 新建。
