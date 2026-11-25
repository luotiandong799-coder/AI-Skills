# r809A｜Bradford Hill 准则：把「相关≠因果」拆成九个可审视的证据维度（TI · 2026-11-26）

> 正文下沉自 `meta/ti-critical-reasoning/SKILL.md` §三十五（r809A 实拉）。≥2 独立域一手交叉，URL+日期逐条。

## 一、准则原文九条 + 显著性检验（PMC4792272 TABLE 1 逐字）

标题：`Viewpoints on Disease Association or Causation: The Bradford-Hill Criteria (1965)`，作者 manuscript available in PMC 2016 Mar 15。

1. **Strength of association**：「Both strong and slight associations are relevant. Slight associations do not mitigate causation. For example, the low invasive potential of meningococcus in the colonized host does not negate the conclusion that meningococcus causes meningitis.」
2. **Consistency**：「Has the observed association been repeatedly observed by different persons, in different places, circumstances, and times?」
3. **Specificity**：「Interpretation must be cautious, as diseases may have more than one cause.」
4. **Temporality**：「Which is the cart and which is the horse? This criterion is particularly relevant with diseases of slow development.」
5. **Biological gradient**：「Defining a dose-response curve between exposure and disease outcome should be sought, although it can be difficult to secure a satisfactory quantitative measure of the associated environmental factor.」
6. **Biologically plausible**：「This criterion is dependent on the biologic knowledge of the day, and the observed association may be new to science and medicine.」
7. **Coherence**：「The cause-and-effect interpretation should not significantly conflict with known principles of science or the natural history of disease. However, the failure to replicate disease in an experimental model cannot nullify human epidemiologic observations. For example, John Snow's observations on transmission of cholera by water were not invalidated by lack of contemporaneous isolation of the inciting *Vibrio cholerae* that awaited Robert Koch's work 30 years later.」
8. **Experiment**：「Experimental evidence, when available, may provide the strongest support for disease causation.」
9. **Analogy**：「It is reasonable to consider prior examples in which an exposure was linked to disease causation in judging a new putative exposure associated with disease.」
10. **Test of significance**（Hill 单列为第十项，常被误计入「九条」）：「Formal tests of significance serve as a reminder of the effects of chance on observations but contribute nothing to the 'proof' of the hypothesis incorporating the integrated analyses (above) required for determination of disease association or causation.」

## 二、判据（三条独点）

### 独点1：这是「观点(viewpoints)」不是勾选清单；时序性是唯一不可逾越的逻辑前提
- 玻尔科学百科逐字：「并非一套用于打勾的僵硬清单，而是一套用于审视证据、在不确定性中做出明智判断的启发式思维工具」；「在九条指南中，时序性（原因必须发生在结果之前）是唯一不可逾越的逻辑前提和『铁律』」。
- 反例保护：强度条原文明确「slight associations do not mitigate causation」——小关联不能否定因果；特异性条「diseases may have more than one cause」——一因一果不是必需。
- 判据：① 报告须写「哪几条支持、哪几条缺失、缺失是否致命」，不能写「满足 X/9 条故因果成立」。② 时序性不满足直接否掉，其余八条只调整置信度、不构成充分条件。③ 部分作者加「可逆性（原因消失则结果消失）」，标为增补非 Hill 原始九条。

### 独点2：一致性与特异性不是因果证明；coherence 的缺证不等于否定
- Wikiwand 中译逐字：一致性「不同人在不同地方用不同样本观察到的一致结果增强了效果的可能性」——是增强不是证明；coherence「缺乏这种（实验室）证据并不能抵消流行病学对关联性的影响」。
- PMC 逐字 John Snow 霍乱例：未分离出霍乱弧菌（30 年后 Koch 才做到）不推翻水的传播结论。
- 判据：① 实验证据缺席不与流行病学证据相互抵消——两边是异质证据源，不能用一边空否决另一边。② 「实验室没复现」须登记为证据缺口而非结论反转。③ 类比/合理性受「当日知识」约束（原文 biologically plausible 条），随知识更新需重评。

### 独点3：与 do-calculus / E-value / 贝叶斯因子分工——证据组织层 vs 识别层 vs 量化层
- Hill 准则管「拿到一堆观察关联，怎么系统审视它像不像因果」（证据组织/启发式层）；§13–21 的 DAG/do-calculus/IV/RDD 管「图已知/准实验设置下如何识别估计」（识别层）；§22 E-value 管「未测混杂要多强才能解释掉」（稳健性量化层）；§34 贝叶斯因子管「数据对 H0/H1 各支持多少」（证据强度量化层）。
- Hill 第十条把显著性检验明确排除在「证明」之外：p 值是 chance 提醒器，不是 integrated analyses 的替代品。
- 判据：① 交付因果结论时四层各写一句：Hill 维度审视 / 识别策略与假设 / 稳健性阈值 / 证据强度，缺任一层都标缺口。② 禁把「p<0.05 + 满足 Hill 六条」当作因果成立的充分论证。③ 与 `agent/grill-me` SDT 分工：SDT 判「分辨力 vs 判定标准」，Hill 判「关联像不像因果」，两者都防「单点命中率」误读。

## 三、来源与诚信（2026-11-26 实拉）
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC4792272/table/T1/`（NIH PubMed Central，WebFetch 200 全文逐字：TABLE 1 九条+显著性检验逐字、John Snow 例、meningococcus 例）——第一独立域·官方医学文献一手。
- `https://www.mhlw.go.jp/shingi/2005/03/dl/s0331-9b2.pdf`（日本厚生劳动省官方 PDF，WebSearch 逐字：九条逐条+吸烟肺癌 9–10 倍/扫烟囱睾丸癌 200 倍/29 回顾+7 前瞻一致性判例）——第二独立域·国家级卫生机构一手。
- `http://scipedia.bohrium.com/sciencepedia/feynman/epidemiology_undergraduate-Bradford_Hill_guidelines_for_causal_inference`（玻尔科学百科，WebSearch 逐字：时序性唯一铁律、启发式非清单、与孟德尔随机化/潜在结果框架互补）——第三独立域·科学百科一手。
- `https://www.wikiwand.com/zh-hk/布拉德福德·希爾準則` + `https://wikii.one/Bradford_Hill_criteria`（中译镜像，WebSearch 逐字：九条中文口径、可逆性增补条）——第四、五独立域·译本交叉（非一手，仅作中文口径核对）。
- 诚信降级：Wikipedia 原页 WebFetch fetch failed 未采纳为全文；中译镜像仅作译本核对不当一手。
- 判重：全库 SKILL.md/module-memory/co-learn 对 `Bradford Hill`/`希尔准则`/`Hill criteria` 0 专节（r786A E-value references 仅一句旁及非专节）；与 §22 E-value（混杂阈值）、§34 贝叶斯因子（证据强度）、§13–21 识别策略异命题。豆包自留地 WB 0 落地。按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。
