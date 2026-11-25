# r808C · CUSUM 累积和变点预警（PDI · 2026-11-26 实拉）全文与判非

> PDI 模块；≥2 独立域一手（NIST/SEMATECH e-Handbook 两页 WebFetch 200 全文 + Minitab 官方方法/数据前提页 WebFetch/WebSearch 逐字）。
> 主线：单点阈值只看当前值，CUSUM 累积「相对目标的偏差」，把持续的小偏移攒成大信号；报警时刻 ≠ 变点时刻，必须用 ARL 双指标定 h/k。

## 独点1 · 累积偏差为何对小偏移更敏感

- NIST 逐字：「CUSUM charts, while not as intuitive and simple to operate as Shewhart charts, have been shown to be more efficient in detecting small shifts in the mean of a process. In particular, analyzing ARL's for CUSUM control charts shows that they are better than Shewhart control charts when it is desired to detect shifts in the mean that are 2 sigma or less.」
- 构造：`S_m = Σ_{i=1}^m (x̄_i − μ̂_0)` 或标准化 `S'_m = (1/σ_x̄) Σ (x̄_i − μ̂_0)`；「as long as the process remains in control centered at μ̂_0, the CUSUM plot will show variation in a random pattern centered about zero. If the process mean shifts upward, the charted CUSUM points will eventually drift upwards, and vice versa」。
- ARL（NIST 表，k=0.5，h 为标准化决策区间）关键值：受控 0 偏移时 CUSUM h=4→336、h=5→930、Shewhart→371；1σ 偏移时 CUSUM h=4→8.38、h=5→10.4、Shewhart→44.0；2σ 偏移 CUSUM 3.34/4.01 vs Shewhart 6.30；3σ 偏移 CUSUM 2.19/2.57 vs Shewhart 2.00。结论逐字：「the Shewhart chart is superior for detecting large shifts and the CUSUM scheme is faster for small shifts. The break-even point is a function of h.」
- 口径：1σ 偏移要查表中第一列 0.5（因为 k=0.5 要加回去），直接查 1.00 行会得到 8.38 对应 1.5σ 偏移——表中 shifted mean = 第一列 + k，读表常见错。

## 独点2 · 双侧表格式递推与两个设计参数

- NIST 表格式（初值 `S_hi(0)=S_lo(0)=0`）：`S_hi(i) = max(0, S_hi(i−1) + x_i − μ̂_0 − k)`；`S_lo(i) = max(0, S_lo(i−1) + μ̂_0 − k − x_i)`；「When either S_hi(i) and S_lo(i) exceeds h, the process is out of control.」
- k = reference value / allowable slack，「k specifies the size of the shift you want to detect」，实务可设 `k=(μ̂_0+μ_1)/2`（μ_0 可接受质量水平、μ_1 拒收质量水平）；h = decision limit，超过即报警；单侧图需 n、k、h 三参数，控制正负两向时「two one-sided charts are used」。
- Minitab 官方默认：tabular CUSUM 中心线为 0，「The default value for h is 4」「The default value for k is 0.5」；h/k 常从 ARL 表选；另有 FIR（fast initial response）——「Normally, tabular CUSUMs are initialized at 0, but if the process is out of control at startup, the CUSUMs will not detect the situation for several subgroups」，FIR 解决这段启动盲区。
- V-mask 是同一机制的图形形态（Barnard 1959），设计参数 k（臂斜率）与 h（rise/decision interval）；NIST 经验法则「choose k to be half the δ shift ... and h to be around 4 or 5」；手工构建复杂，表格形式更实用。
- 设计流程：先定 μ_0、μ_1 与期望 ARL（`L0` 受控要高、`L1` 失控要低），再反查标准化 `k_s=(μ−k)√n/σ`、`h_s=h√n/σ`；ARL 精确计算涉及积分方程，NIST 用程序/诺模图给出，不可手算糊弄。

## 独点3 · 失效面与验收

- 数据前提（Minitab Data considerations 逐字）：数据须连续（计数型用属性控制图）；「Small shifts in the data are important」才用 CUSUM，否则 Xbar-R / I-MR 即可；「The observations within each subgroup should not be correlated with each other」——子组内相关会让控制限过窄、把受控点误报为失控；「The data should be in time order」且等时间间隔采集，整子组缺失不出图。
- 报警语义：超限点是**检出时刻**，不是变点时刻；NIST V-mask 做法是「sliding the V-Mask backwards ... determine the first point that signaled an out-of-control situation」，表格 CUSUM 可回溯到最后一次归零处估偏移起点；报预警必须同时给「检出时刻 + 估计起点 + 方向（hi/lo）」。
- 不防什么：非平稳趋势/季节性未建模时累积项会把正常漂移当变点；方差漂移、分布变换后阈值不迁移；自相关序列须先对残差做监控；h/k 从别处硬抄会让误报率与检出延迟同时失真；单次超限只是信号不是根因结论。
- 与 §十八事件型预警分工：那章管「异常是区间不是点、point-adjustment 会让随机探测器拿高分」的评测协议；本章管在线监控统计量本身。与 §十五多步策略/§十七回测协议正交；与 §r803C ETS 分工：ETS 给点预测与区间，CUSUM 监控过程均值是否漂移。

## 来源与诚信

- `https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm`（NIST/SEMATECH e-Handbook 6.3.2.3，WebFetch 200 全文逐字：CUSUM 定义/累积式/V-mask k 与 h/αβδ 关系/经验法则/表格式 hi-lo 递推与超限判据/20 点算例）——第一独立域·官方一手。
- `https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc3231.htm`（NIST 6.3.2.3.1 Cusum ARL，WebFetch 200 全文逐字：ARL 定义/L0 高 L1 低/k=(μ0+μ1)/2/标准化 ks·hs/完整 ARL 对照表/Shewhart 1σ=44 的推导/小偏移 CUSUM 快大偏移 Shewhart 快）——同域第二页，数值来源。
- `https://support.minitab.com/en-us/minitab/help-and-how-to/quality-and-process-improvement/control-charts/how-to/time-weighted-charts/cusum-chart/methods-and-formulas/methods-and-formulas/`（Minitab 官方方法页 WebFetch 200 逐字：h=4/k=0.5 默认、FIR、tabular vs V-mask、中心线 0、k 是 allowable slack）——第二独立域·厂商官方一手；`.../before-you-start/data-considerations/`（WebSearch 逐字：连续性/小偏移重要性/子组内不相关/时间顺序/等间隔）。
- 诚信登记：`https://itl.nist.gov/div898/handbook/pmc/section3/pmc35.htm` 重定向到 NIST ITL 主页未取到内容，未采纳；`kevos.com/tools/cusum-chart-check` WebFetch 被重定向到 bizomat.ai 主页，未采纳。
- 判非：全库 SKILL.md + module-memory + co-learn 对 `CUSUM`/`change-point`/`变点检测` 在 PDI 本体 0 专节（wb-context-compressor references 里有词命中属豆包自留地，WB 0 落地；co-learn 里 CUSUM 仅为模型路由/文档处理语境的单词命中）。按 rules/07 判「增＝加厚现有」，0 新建。
