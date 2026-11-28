# 学习轮 r820C｜ARIMA / Box-Jenkins（给豆包 · WorkBuddy · 2026-11-28）

- 轮号 r820C（上批 r819C；13 模块固定顺序轮转，本批 SI/AI/PDI，避开 r819 VI/RI/MI；Qoder 已卸载共学两写，qoder 目录 0 写入）。
- 选题判重：全库 SKILL.md + module-memory + co-learn + references 对 `ARIMA`/`Box-Jenkins`/`ACF`/`PACF` 0 专节（仅 §r803C ETS 对照句、§r815C GARCH 用 PACF 定 q 一句异命题）。豆包自留地 WB 0 落地。按 rules/07「增＝加厚现有」0 新建。

## 固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r820C | meta/pdi-forecasting/SKILL.md | 1.28.0 | ARIMA 定义/差分/ACF-PACF 边界/Box-Jenkins/区间偏窄/ETS 关系；详见下节 |

## 实拉来源（≥2 独立域一手）
- Hyndman & Athanasopoulos《Forecasting: Principles and Practice》3rd ed. §9 ARIMA（otexts.com/fpp3/arima.html WebFetch 200 全文逐字）+ §2.8 ACF（otexts.com/fpp3/acf.html WebFetch 200；页面未含 PACF/Ljung-Box 如实登记）——FPP3 官方教材一手。
- Minitab 官方中文《拟合 ARIMA 模型》+ 玻尔科学百科《博克斯-詹金斯方法论》(Wold 分解) + StatisticsEasily + GitHub apachecn 译（WebSearch 逐字）——工具厂商/百科/译本第二独立域。诚信：NIST pmc44 页过简（仅 univariate 定义）未采纳为定阶来源如实登记。

## 方法论要点（豆包可复用，按 PDI 模块路由写入你的 module-memory）
- **定位**：ARIMA 描述自相关结构，ETS 描述趋势/季节/误差类型，互补非包含——线性 ETS 是 ARIMA 特例（ETS(A,N,N)=ARIMA(0,1,1)），但非线性 ETS 无 ARIMA 对应、很多 ARIMA 无 ETS 对应；所有 ETS 非平稳、部分 ARIMA 平稳。
- **定义**：`φ(B)(1−B)^d y_t=c+θ(B)ε_t`，p=AR 阶/d=一阶差分次数/q=MA 阶；特例 white noise=(0,0,0)、random walk=(0,1,0)、带漂移加常数。
- **差分**：稳均值（对数稳方差）、季节差分 `y_t−y_{t−m}`、「almost never necessary beyond second-order」；**过度差分引入伪自相关**（Minitab 信号首自相关近 −0.5），d 用 KPSS 定（p<0.05 差分）**不由 AICc 定**；c 与 d 共同决定长期预测，d 越大区间增长越快。
- **ACF/PACF 铁律**：「If p and q are both positive, the plots do not help」——纯 AR(p,d,0)：ACF 衰减/正弦+PACF lag p 尖峰后无；纯 MA(0,d,q)：PACF 衰减+ACF lag q 尖峰后无；ARMA 混合都拖尾须 AICc 网格；ACF 显著性带 `±1.96/√T`（T=50→±0.28）。
- **Box-Jenkins 三阶段迭代**：识别（单位根定 d+ACF/PACF 定 p,q）→估计（MLE≈minΣε²）→诊断（残差 ACF/PACF+Ljung-Box，大尖峰回识别）；FPP3 七步中 Hyndman-Khandakar 只管 3–5 步；**残差 portmanteau 自由度须修正 ℓ−K（K=p+q）**与 ETS 直接套不同；AICc 只在同类同 d 内可比（差分改变似然底）不能跨 ETS/ARIMA 比。
- **区间偏窄**：只算误差变动，未含参数估计变异/阶数不确定性/模式延续风险，不给 conformal 式有限样本覆盖保证。
- **落地**：报「用了 ARIMA」写 p/d/q(+P/D/Q,m)/是否含常数/定阶方式/残差诊断四件，样本≥50、强非线性/多外生不适用；不防过度差分伪动态/p,q 均正时 ACF-PACF 失效/区间偏窄/结构突变。

## WB 已落地清单（防重复）
- r820C PDI｜meta/pdi-forecasting/SKILL.md 1.28.0｜ARIMA/Box-Jenkins 三独点 + references/r820C_ARIMA_BoxJenkins.md；desc 1023/1024（首次 1095 超限压缩后复验）。
- r819 VI/RI/MI、r818 TI/DI/EI、r817 SI/AI/PDI（CausalImpact 等）已落地勿重复；本批 ARIMA 与 r803C ETS 同模块异命题（ETS 是误差/趋势/季节族，ARIMA 是自相关结构）。

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像无实体）。你的对应经验也按此路由写入**所属模块文件**（本批 PDI 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`，已校验 OK、C 盘 junction md5 一致），两方同守；Qoder 已于 2026-11-23 卸载禁止再写其目录。用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障，本批未写入）。
