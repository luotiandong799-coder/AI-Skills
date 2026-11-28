import re, io, os
p = r'D:\腾讯AI\skills\engineering\vi-fact-verification\SKILL.md'
t = io.open(p, encoding='utf-8').read()
lines_before = t.count('\n') + 1

# 1) extract section 14 full text into references
m = re.search(r'(## 十四、似然比[^\n]*\n)(.*?)(?=\n## 十五、Conformal)', t, re.S)
assert m, 'section14 not found'
sec14 = m.group(1) + m.group(2)
ref = r'D:\腾讯AI\skills\engineering\vi-fact-verification\references\r768B_似然比.md'
io.open(ref, 'w', encoding='utf-8', newline='\n').write('# r768B 似然比（全文下沉 · 2026-11-19 原节）\n\n' + sec14.strip() + '\n')

summary = '''## 十四、似然比（r768B · 全文下沉 references/r768B_似然比.md）

> 本节三独点（LR 定义与 portable 性 / 验前 odds×LR=验后 odds 与 Fagan / LR+≥3 与 DOR 与自然频率沟通）与四域一手来源逐字全文已下沉 `references/r768B_似然比.md`，结论仍有效：验前概率不同时预测值不能照搬，用 LR 迁移；与 §13 谱偏倚、§26 生存分析分工不复用。

'''
t = t[:m.start()] + summary + t[m.end():]

# 2) desc lossless tighten + add triggers
old_desc_frag = [
 ('涉及事实声称/来源引用/数据计算核对/改动验收/判断是否真正完成时调用。', '事实声称/来源引用/数据核对/改动验收/完成判定。'),
 ('落实独立性与来源分级，给出"真/误导/夸大/缺证据/假"评级。', '独立性+来源分级+真/误导/夸大/缺证据/假评级。'),
 ('注意：EI 的 CCS 验"执行过"，VI 验"对不对"，互补不重复。', 'EI验执行过/VI验对不对，互补。'),
 ('变异算子·存活/等价变异体·等价不可判定·耦合效应·human oracle problem', '变异算子·存活/等价变异体·耦合效应'),
]
for a, b in old_desc_frag:
    assert a in t, 'desc frag missing: ' + a
    t = t.replace(a, b, 1)
add = '、生存分析（Kaplan-Meier乘积限·删失·log-rank·Cox比例风险·风险比HR·PH假设检验）'
dm = re.search(r'^(description: .+)$', t, re.M)
assert dm
desc = dm.group(1)
t = t[:dm.start(1)] + desc + add + t[dm.end(1):]

# 3) bump version
t = t.replace('version: "1.22.0"', 'version: "1.23.0"', 1)

# 4) append section 26
section26 = '''

## 二十六、生存分析（time-to-event）：还没发生的样本不是「成功」，也不是缺失值（VI · 2026-11-28 实拉，≥2 独立域一手交叉，3 独点）

**独点 1｜删失不是缺失值、也不是事件：KM 乘积限把「最后一次观察时间」和「是否发生事件」两列同时用起来。** 生存分析的结局是「从起点到某事件发生的时间」（故障/死亡/流失/漂移），研究结束时未发生事件者是被**右删失**（right censoring：只知事件在 t 之后、不知确切时刻），既不能当「已发生」也不能整条丢弃。Kaplan–Meier 乘积限估计 `Ŝ(t)=∏_{tᵢ≤t}(1−dᵢ/nᵢ)`：在每个事件时刻 tᵢ，dᵢ 为该时刻事件数、nᵢ 为恰在 tᵢ 前的风险集人数，删失者在其删失时刻之前计入 nᵢ、之后退出；S(t) 是「到 t 仍未发生事件」的概率，S(0)=1 随 t 递减。StatsDirect 明列三条假设：① 删失者与继续随访者生存前景相同——**无法检验且会人为压低 S**；② 早晚期入组者生存前景相同（可检验）；③ 事件在规定时刻被记录，迟记会人为抬高 S。⇒ 凡「跑一段时间才知道结论」的验证（功能多久后出错、用户多久流失、设备多久失效），验收表必须同时有「末次观察时间」与「事件是否发生」两列，只统计已发生者或把未发生当作成功都判违规。

**独点 2｜中位生存期是首次 S≤0.5 的时刻，曲线比较用 log-rank 而非某一时点的率。** 中位生存期 = S 首次降到 0.5 或以下的时刻（Brookmeyer–Crowley 给 95% CI）；平均生存期是 S 曲线下面积，受最长随访时间限制，删失多时只能估到删失比例以内的分位（statsmodels：约 30% 受试者死亡时，只能估 0.3 概率点以下的分位数，如 0.25 分位），拿平均生存期冒充典型值会掩盖重尾。比较两组不能挑某个时点的生存率比大小（选点即引入选择偏差）；`survdiff` 默认 **log-rank** 是非参数、对整条曲线做检验，另有 Gehan–Breslow（按风险集人数加权，更重早期差异）、Tarone–Ware（按 √风险集加权）、Fleming–Harrington（按合并生存时间加权，p=1 更重晚期）——**不同加权回答不同问题，须事前声明**，不能看完哪条显著再挑。⇒ 验证报告写「A 组更可靠」须给出曲线、log-rank p 值与所用权重，缺一不算。

**独点 3｜Cox 比例风险模型估的是乘性效应，比例风险假设是前提而非可选项。** Cox 模型 `h(t|x)=h₀(t)·exp(xᵀβ)`：基线风险 h₀(t) 非参数、不必指定形状，协变量效应以**风险比 HR=exp(βₖ)** 表达——「瞬时事件率被乘以某个倍数」，不是「某时刻生存率高多少」，也不是概率。估计用**部分似然**（只用到事件时刻的风险集）。核心前提 **PH 假设**：任意两人的风险比不随时间变化；违例时 HR 是随时间变化的平均值、不可照搬。检验用 log-log 生存曲线是否平行、Schoenfeld 残差是否随时间有趋势、或引入时变协变量；违例改用**分层 Cox**（对违背 PH 的变量分层、对其余变量估系数）或**扩展 Cox**（含时变变量）。⇒ 凡报 HR 必同时报 95% CI、PH 假设检验结果与基线风险未参数化这一事实；把 HR 讲成「概率提升 x 倍」或跳过 PH 检验，判为误读。

**判据（VI 落地）**：以「经过一段时间才见分晓」的指标做验证时，先问三件事——① 删失样本是否被显式记录而不是被删/被当成功；② 曲线比较是事前声明的 log-rank 与权重，还是事后挑时点；③ 若用 Cox 报效应，是否带 CI 且验过 PH 假设。三者缺一，结论只算「在有偏观测上的描述」，不得升级为事实。与 §九统计功效（多少样本）、§二十二序贯检验（何时看）、§二十四 Youden（阈值怎么选）、§二十五 MSA（量尺是否可信）分工：本节点在「时间到事件且结局尚未全部揭晓时怎么验证」，均异命题。

**判重**：全库 SKILL.md / module-memory / co-learn 对 `生存分析` / `Kaplan-Meier` / `log-rank` / `Cox 比例风险` 0 专节（仅豆包自留地 `wb-context-compressor` 有 `calibration` 语境一句，异命题且 WB 0 落地）；与 PDI 预测（预测值校准）、VI §十四似然比（验前验后迁移）、§十三谱偏倚（人群依赖）分工不复用。

**来源与诚信**：`https://www.statsdirect.com/help/survival_analysis/kaplan_meier.htm`（WebFetch 200 全文逐字：S(t) 定义、乘积限公式与 dᵢ/nᵢ 语义、删失三条假设、Greenwood 方差、Peterson=−ln(S) 与 Nelson–Aalen、log-rank/Wilcoxon 无需分布假设、Brookmeyer–Crowley 中位 CI）——第一独立域·统计软件官方文档；`https://www.statsmodels.org/stable/duration.html`（WebFetch 200 全文逐字：right-censoring 定义、SurvfuncRight、survdiff 默认 logrank 与 FH/Gehan-Breslow/Tarone-Ware 加权、PHReg Cox 模型、HR 乘性效应、30% 死亡只能估 <0.3 分位）——第二独立域·开源统计库官方文档；`https://zh.wikibooks.org/wiki/数理统计/生存分析与打分检验`（WebSearch 快照逐字：S=exp(−H)、KM 公式、Nelson–Aalen、Cox 部分似然 L(β)、Schoenfeld 残差、Score/log-rank/Wald 三者分工）与 `https://www.eolss.net/Sample-Chapters/C02/E4-31-02-04.pdf`（Kleinbaum 等《Survival Analysis》章节 WebSearch 摘要逐字：censored 定义、PH 假设 log-log 曲线、分层/扩展 Cox）——第三、四独立域教材交叉，WebFetch 本地回退禁用（`CODEBUDDY_WEBFETCH_DISABLE_LOCAL_FALLBACK=1`）如实登记不冒充全文。诚信：`https://www.ncbi.nlm.nih.gov/books/NBK539796/` 号错配（实为桡动脉置管）整篇弃用；`biostathandbook.com/survival.html`/`statology.org/kaplan-meier-curve`/`medcalc.org/manual/cox-*` 均 404 未采纳；维基教科书与 wipedia 同族按来源族折叠。逐字全文与判非见 `references/r819A_生存分析.md`。
'''
t = t.rstrip('\n') + '\n' + section26

io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

# 5) reference detail file
ref26 = '''# r819A 生存分析（time-to-event）逐字取证 · 2026-11-28

> 载体：engineering/vi-fact-verification SKILL.md §二十六（version 1.23.0）。三轮标准一致，≥2 独立域一手交叉。

## 一手域 1 — StatsDirect 官方帮助（WebFetch 200 全文逐字）
URL: https://www.statsdirect.com/help/survival_analysis/kaplan_meier.htm
- "This function estimates survival rates and hazard from data that may be incomplete."
- "St=number of individuals surviving longer than t / total number of individuals studied"；"At t=0 S(t) = 1 and decreases toward 0 as t increases toward infinity."
- "The product limit (PL) method of Kaplan and Meier (1958) is used to estimate S: Ŝ(t)=∏_{tᵢ≤t}[1−dᵢ/nᵢ]"；"where tᵢ is duration of study at point i, dᵢ is number of deaths up to point i and nᵢ is number of individuals at risk just prior to tᵢ."
- "If a subject is last followed up at time tᵢ and then leaves the study for any reason (e.g. lost to follow up) tᵢ is counted as their censorship time."
- Assumptions 逐字：① "Censored individuals have the same prospect of survival as those who continue to be followed. This can not be tested for and can lead to a bias that artificially reduces S."；② "Survival prospects are the same for early as for late recruits to the study (can be tested for)."；③ "The event studied (e.g. death) happens at the specified time. Late recording of the event studied will cause artificial inflation of S."
- hazard: "the event rate at time t conditional on surviving up to or beyond time t. As h(t) is a rate, not a probability, it has units of 1/t."；Ĥ(t)=−ln(Ŝ(t))（Peterson 1977）；Nelson–Aalen H̃(t)=∑dᵢ/nᵢ，"A Nelson-Aalen hazard estimate will always be less than an equivalent Peterson estimate"。
- Greenwood (1926) var(Ŝ)=Ŝ²∑dᵢ/[nᵢ(nᵢ−dᵢ)]；CI 用 log 变换的渐近最大似然（Kalbfleisch & Prentice 1980），因直接用 Greenwood 会给出 <0 或 >1。
- "you would use the Log-rank and Wilcoxon tests which do not assume any particular distribution of the survivor function."；例 Brookmeyer-Crowley 95% CI for median = 192 to 235，mean=218.68。

## 一手域 2 — statsmodels 0.15.0 官方文档（WebFetch 200 全文逐字）
URL: https://www.statsmodels.org/stable/duration.html
- "implements several standard methods for working with censored data."；"Currently only right-censoring is handled. Right censoring occurs when we know that an event occurred after a given time t, but we do not know the exact event time."
- "Since only around 30% of the subjects died during this study, we can only estimate quantiles below the 0.3 probability point."
- "We can formally compare two survival distributions with survdiff, which implements several standard nonparametric procedures. The default procedure is the logrank test."；另列 Fleming-Harrington(p=1 weight by pooled survival time) / Gehan-Breslow(weight by number at risk) / Tarone-Ware(weight by sqrt number at risk)。
- "Proportional hazard regression models ('Cox models') are a regression technique for censored data."；"These models express the covariate effects in terms of 'hazard ratios', meaning the the hazard (instantaneous event rate) is multiplied by a given factor depending on the value of the covariates."
- 输出表 HR：age 1.1065 [1.1012,1.1119]、female 0.7545 [0.6875,0.8280]，"Confidence intervals are for the hazard ratios"。
- 参考：Therneau 1996 Extending the Cox model；Rodriguez 2005 Non-parametric estimation in survival models；Gillespie 2006 Checking the assumptions in the Cox proportional hazards model。

## 交叉域 3/4 — WebSearch 快照逐字（不作一手全文）
- https://zh.wikibooks.org/wiki/数理统计/生存分析与打分检验：S(t)=P(T>t)、h=f/S、S=exp(−H)、H=∫h；KM Ŝ(t)=∏(1−dᵢ/nᵢ)；Nelson–Aalen Ĥ=∑dᵢ/nᵢ；Greenwood 方差；Cox h(t|x)=h₀(t)exp(xᵀβ) 与部分似然 L(β)=∏_{i∈D}exp(xᵢᵀβ)/∑_{j∈R(tᵢ)}exp(xⱼᵀβ)；HR=exp(βₖ)；Schoenfeld 残差诊断比例假设；Score/log-rank/Wald 三者分工（log-rank 非参数删失稳健）。
- https://www.eolss.net/Sample-Chapters/C02/E4-31-02-04.pdf（Kleinbaum, Christensen, Rowe《SURVIVAL ANALYSIS》章节）：目录含 censoring / KM / log-rank / Wilcoxon / Cox PH / evaluating PH assumption（log-log survival curves, time-dependent variables, GOF）/ stratified Cox / extended Cox；Summary 逐字 "Study subjects who do not experience an event during the study period are designated as 'censored' and are included in the analysis by counting the follow-up time they contributed during the study."；"An important assumption of the Cox proportional hazards model is that the hazard for an individual is proportional to that for another individual, regardless of time."

## 诚信登记
- NCBI NBK539796 号错配（WebFetch 200 但实为 Radial Artery Cannulation）整篇弃用，未冒充生存分析一手。
- https://biostathandbook.com/survival.html 404；outline 第三版无 survival 章节；https://www.statology.org/kaplan-meier-curve/ 404；medcalc 两 URL 404；IBM SPSS beta 页无正文——均未采纳。
- wikibooks curl 直取 exit 35；EOLSS PDF / wikibooks WebFetch 触发本地回退禁用（CODEBUDDY_WEBFETCH_DISABLE_LOCAL_FALLBACK=1）——按 WebSearch 快照转述并标明，不冒充 WebFetch 全文。
- 维基教科书与 wipedia survival analysis 按来源族折叠；豆包自留地 wb-context-compressor / wb-execute-discipline WB 0 落地。
'''
io.open(r'D:\腾讯AI\skills\engineering\vi-fact-verification\references\r819A_生存分析.md', 'w', encoding='utf-8', newline='\n').write(ref26)

dm = re.search(r'^description: (.+)$', io.open(p, encoding='utf-8').read(), re.M)
print('LINES_BEFORE', lines_before, 'LINES_AFTER', io.open(p, encoding='utf-8').read().count('\n') + 1)
print('DESC_LEN', len(dm.group(1)))
print('OK')
