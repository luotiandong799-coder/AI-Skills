# r796D｜VI｜十、等效性检验 TOST：不显著不是等效，先定等效界才有权说「一样」

访问日期：2026-11-22；每轮独立实拉禁止复用上轮。

## 一手来源逐字

- https://journals.sagepub.com/servlet/linkout?dbid=4&doi=10.1177%2F14761270251410355&key=10.1177%2F1948550617697177&site=sage&suffix=e_1_3_5_47_1（Lakens，SPPS 8(4)，2017，WebFetch 200 逐字：p>α 不能推出无效应/TOST 两单侧/90%CI 排除界/0 假设不可能被支持）

- https://journals.sagepub.com/servlet/linkout?dbid=4&doi=10.1177%2F25152459251323480&key=10.1177%2F2515245918770963&site=sage&suffix=e_1_3_5_19_1（Lakens/Scheel/Isager，AMPPS，2018-06，WebFetch 200 逐字：取较大 p/无需多重校正/不显著=数据不足/90%CI 全落界内/SESOI 决定样本量）

## 独有点

1. 先看数据前写 Δ（±Δ 须附领域/成本-收益理由）与 α，再据 Δ 算样本量；判据——事后按结果挑 Δ、把 0 当等效界均判违规。Lakens 2017 逐字：researchers often incorrectly conclude an effect is absent based a nonsignificant result；「not possible to conclude there is no effect when p > α」。

2. 做两个单侧检验 H01:Δ≤−ΔL 与 H02:Δ≥ΔU，取较大 p 与 α 比；判据——两个都显著才等效，禁止用 p>α 宣布等效，禁止对两次检验做多重比较校正（Lakens 2018 逐字：not necessary to control for multiple comparisons）。若既非显著不同也非统计等效 → 写「数据不足」，不得二选一硬判。

3. 90% CI 必须完全落入 [−ΔL,+ΔU] 才写等效；判据——以「95%CI 含 0 / 不显著」替代等效结论、把等效检验与优效性 NHST 混用均判违规。界值来自 SESOI，界越窄所需样本越大（Lakens 2018 逐字）。与 §9 分工：§9 防止误报「无效应」，本条给「有界等效」的正向证据路径。

## 判重与判非

- 判重：`TOST`/`等效性检验`/`equivalence test` 全库 SKILL.md 0；与 §9 统计功效（防误判）分工不复用。豆包自留地 WB 0 落地。

- 抓取失败：FDA 生物等效性指南限定域检索无结果，未虚构 URL；Δ 预先定的「before looking at data」原句被截断，标注为谨慎外推。
