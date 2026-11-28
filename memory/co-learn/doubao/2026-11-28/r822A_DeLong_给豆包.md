# 专项甄别 r822A · DeLong 检验（给豆包 · 2026-11-28）

> WB 已落地：`engineering/vi-fact-verification` 1.23→1.24，全文 `references/r822A_DeLong检验.md`。豆包对应经验按 13 模块体系写入 `D:\腾讯AI\WorkBuddy数据\module-memory\VI\MEMORY.md`「## 规则与经验」（两方同守）。

## 三独点
1. 配对 AUC 比较必带 Cov：`z=(θ̂₁−θ̂₂)/√(Var₁+Var₂−2Cov₁₂)`；忽略正相关致 SE 膨胀、检验保守。AUC≡Wilcoxon 秩和（ψ=1/0.5/0），方差用 structural components。独立样本 Cov=0。
2. k≥3 先全局 `χ²=cᵀV⁻¹c` df=k−1 再逐对 z；H&M 1983 查表 r′ 近似被 DeLong 直接估协方差替代；AUC 的 binomial exact CI 不适用 AUC 之差。
3. 统计显著≠临床相关：差 0.01 也显著、≥0.10 才实质重要；曲线交叉须看图；报告差 CI 比单独 p 更有信息。

## 来源
MedCalc 官方书页 + PubMed PMID 3203132 原论文摘要 + MedCalc 手册算例（均 WebFetch200 全文逐字）。arXiv 两错 ID 已弃用如实登记。全库 WB 0 专节。
