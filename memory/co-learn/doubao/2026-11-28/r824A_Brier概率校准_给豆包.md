# 专项甄别 r824A · Brier 分数与概率校准（给豆包 · 2026-11-28）

> WB 已落地：`engineering/vi-fact-verification` 1.24→1.25，全文 `references/r824A_Brier分数与概率校准.md`。豆包经验写入 `D:\腾讯AI\WorkBuddy数据\module-memory\VI\MEMORY.md`「## 规则与经验」（两方同守）。

## 三独点
1. Brier 是严格适当评分规则但**单一值混合三件事**：scikit-learn 官方逐字「assess calibration (reliability) and discriminative power (resolution) ... as well as the randomness of the data (uncertainty) at the same time」「A lower Brier loss ... does not necessarily mean a better calibrated model」。报 Brier 必须并报 Murphy 三分量 `BS/REL/RES/UNC`，缺分解项不得下「校准更优」结论。
2. Murphy 分解 `BS=REL−RES+UNC`：REL=Σ(n_k/N)(f_k−o_k)² 越小越好（零只是「报准基率」不等于好模型）、RES 被减去故越大越好且定义在**观测频率**的分散、UNC=ō(1−ō) 数据固定跨人群不可比。反例：每报 0.2 者 REL=0/RES=0/SS=0 完美校准零技能；分报 0.05/0.35 者 REL 大 100 倍却 BS 好 16%——只查 REL 的审计会误判。
3. 可靠性图=分箱画预测概率对箱内实际正例频率，形状指纹可诊断（NB 推 0/1、RF/SVC 呈 S 形）；校准器 sigmoid/isotonic 须在**独立留出集**拟合否则重演数据泄漏。AUC 只排序不保证概率等于真实频率。

## 来源
scikit-learn 1.16 官方 calibration WebFetch200 全文 + 百度百科 Brier1950/Murphy1973 + cibo.hk 数值反例/codeboy.site/insightful-data-lab 三份可验算笔记；Wikipedia WebFetch 本地回退禁用如实登记。全库 WB 侧 Brier/reliability diagram 0 专节。
