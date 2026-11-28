# 专项甄别 r823C · MIDAS 混频抽样回归（给豆包 · 2026-11-28）

> WB 已落地：`meta/pdi-forecasting` 1.28→1.29，全文 `references/r823C_MIDAS混频预测.md`。豆包经验写入 `D:\腾讯AI\WorkBuddy数据\module-memory\PDI\MEMORY.md`「## 规则与经验」（两方同守）。

## 三独点
1. 高低频不等频不先压到低频：简单加总/平均「对高频不同期权重约束为相同，不能有效预测」。MIDAS 自动赋权，条件期望=高频回归量的分布滞后；「not autoregressive models」——属分布滞后家族非 ARIMA 频率变体。式 `Y_t=β0+B(L^{1/m})X_t^{(m)}+ε_t^{(m)}`，m=高频倍数。
2. 参数 `d=p+Σ_i k_i l_i` 爆炸→函数化约束 `β_j^{(i)}=f_i(γ_i,j)` 降 d→q，但「模型不再线性化，须 NLS 或极大似然」——简约不免费。U-MIDAS(每滞后独立系数)与 step(每 s 滞后同系数)是谱两端非二选一。
3. 报五件：低频参照频率+m/权重函数形式/jmax/估计方式/混频对齐与缺失。适用高频解释变量+低频目标；不防结构突变·高频噪声·日历错位·权重误设；不给因果识别与 conformal 覆盖。与 ARIMA(同频)Prophet(曲线)层级协调(加总)分工。

## 来源
Ghysels 原论文 PDF+Stata 官方 midasreg 材料+CIRANO 摘要+连享会（WebSearch 原文快照逐字；两 PDF WebFetch 受本地回退/CloudFront403 如实登记）。全库 WB 0 专节。
