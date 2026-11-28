import io
base = r'D:\腾讯AI\WorkBuddy数据\module-memory'
entries = {
'VI': [
 '- ｜2026-11-28｜engineering/vi-fact-verification（r819A）｜生存分析先辨删失：右删失者既非「已发生」也非缺失，KM 乘积限 Ŝ(t)=∏_{tᵢ≤t}(1−dᵢ/nᵢ) 用「末次观察时间+是否发生事件」两列，删失者在删失前计入风险集 nᵢ；三条假设（删失者生存前景与继续随访者相同·不可检验且人为压低 S／早晚期入组相同可检验／事件按时记录迟记抬高 S）。｜r819A；statsdirect.com/help/survival_analysis/kaplan_meier.htm WebFetch200 全文逐字（公式·三假设·Greenwood·Peterson=−lnS vs Nelson–Aalen·log-rank/Wilcoxon 无需分布假设）；落 SKILL.md §二十六 独点1 →1.23.0',
 '- ｜2026-11-28｜engineering/vi-fact-verification（r819A）｜中位生存期=首次 S≤0.5 时刻（Brookmeyer-Crowley CI），平均生存期是曲线下面积受随访长度限制，删失多时只能估删失比例以内的分位（约30%死亡只能估<0.3 分位）；两组比较用整条曲线的 log-rank（非参数·默认等权），Gehan-Breslow 按风险集数加权重早期／Tarone-Ware 按√风险集／Fleming-Harrington 按合并生存时间重晚期——不同权重回答不同问题须事前声明，事后挑时点比较引入选择偏差。｜r819A；statsmodels.org/stable/duration.html WebFetch200 全文逐字（survdiff 默认 logrank 与三种加权·30%死亡只能估<0.3 分位）；落 §二十六 独点2',
 '- ｜2026-11-28｜engineering/vi-fact-verification（r819A）｜Cox 比例风险 h(t|x)=h₀(t)exp(xᵀβ)，基线风险非参数不必指定，HR=exp(βₖ) 是瞬时事件率的乘性倍数（不是某时刻生存率高多少、更不是概率），部分似然估计；PH 假设（任意两人风险比不随时间变）是前提须用 log-log 曲线/Schoenfeld 残差/时变协变量检验，违例改分层 Cox 或扩展 Cox；报 HR 必带 95%CI+PH 检验+基线未参数化，讲成「概率提升 x 倍」判误读。｜r819A；zh.wikibooks 生存分析与打分检验 WebSearch 逐字（部分似然·Schoenfeld 残差）+ EOLSS Kleinbaum PDF 摘要（PH 假设 log-log 曲线·分层/扩展 Cox）；落 §二十六 独点3 + references/r819A_生存分析.md；判重全库 0 专节',
],
'RI': [
 '- ｜2026-11-28｜meta/ri-retrospective（r819B）｜鱼骨图/石川图是「分类穷举+归并」的定性工具非根因判定器：ASQ 逐字「sorting ideas into useful categories… especially useful in structuring brainstorming sessions」、七大质量工具之一；结构=先一致问题陈述→向右鱼脊末端鱼头写问题加框→主因类别作分支→连续问 Why 出子原因，层级分支表示因果关系而非重要性排序；产出是「分类完整的候选因清单」，复杂问题上它只是「one of several tools… alongside responsibility matrix/action-planning matrix」。｜r819B；asq.org/quality-resources/fishbone WebFetch200 全文逐字；落 SKILL.md r819B 节 独点1 →2.16.0',
 '- ｜2026-11-28｜meta/ri-retrospective（r819B）｜分类框架是可改的启发脚手架非物理定律：Ishikawa 的 6M=Materials/Machinery/Methods/Measurement/Manpower/Mother Nature +可选第七 Money，ASQ 明写「encouraged creativity in naming these categories」；中文变体 5M1E（人机料法环测）/8M/营销 4P8P/服务 4S；鱼头方向带语义——原因型（鱼头在右）问「为什么发生」、对策型（鱼头在左）问「如何改善」、整理问题型只结构化非因果，混用两种方向令读图者误解箭头；跨团队比图前先对齐分类口径。｜r819B；ASQ 官方全文逐字＋qms.foodmate.net 鱼骨图分析法 WebFetch200 全文＋wikiwand 石川图 WebSearch 交叉；落 r819B 独点2',
 '- ｜2026-11-28｜meta/ri-retrospective（r819B）｜鱼骨图三弱点须显式处理：主观（依赖团队经验易受头脑风暴影响）+非定量（须配帕累托/AHP 等数据工具验证关键因素）+同一因可归多类（ASQ 例中 calibration 同在 Methods 与 Measurement、iron tools 同在 Methods 与 Manpower）；用 20/80 聚焦、关键因一般≤7、逐条检查语法；后续用 check sheet 收数据验证，候选因逐条标「有数据/仅经验」，仅经验者不得进改进项、同因多处合并保留交叉引用防重复计数；与 r800A 变更分析（有基线只在差异找因）/r804A Tripod Beta/r814B HAZOP 分工。｜r819B；foodmate 局限段逐字＋ASQ 复杂例逐字；落 r819B 独点3 + references/r819B_鱼骨图.md；起源 1953/1956/1960s/1968 四说并列不强行统一',
],
'MI': [
 '- ｜2026-11-28｜meta/mi-memory（r819C）｜闪光灯记忆记的是「得知消息的接收情境」非事件本身：Brown & Kulik 1977 定义「circumstances in which one first learned of a very surprising and consequential event」的 vivid long-lasting autobiographical memories；六类 canonical categories=地点/当时活动/消息来源/自己情绪/在场他人情绪/直接后果（另回忆无关细节如天气）；研究「不查原事件细节而查 reception event」⇒ 记忆核验中「我在哪/谁告诉我」这类接收情境字段须与事件本体字段分开，前者最易被重述污染、最不该给事件本体作证。｜r819C；ScienceDirect S0749596X09000746 WebFetch200 摘要+Intro 逐字＋科普中国闪光灯效应词条 WebFetch200 全文；落 SKILL.md r819C 节 独点1 →2.14.0',
 '- ｜2026-11-28｜meta/mi-memory（r819C）｜「鲜明+高置信+持久」均不蕴含准确：早期 Brown-Kulik 假设 immune to forgetting 被反证（Neisser & Harsch 1992 挑战者号 1天 vs 近3年 44 人高度不一致，结论 ordinary memories preserved by frequent rehearsal）；9/11 2/3 年 test-retest（124 人）一致性显著下降但重大扭曲仅 2003 年 9%/2004 年 7%；研究间差异大（撒切尔 11 月 86% 一致 / Hirst 9/11 相似延迟仅 0.63 / Weaver 一周 96%→一年 81%）；十年研究约 60% 一年后/50% 三年后仍记细节，地点约 80% 准确而情绪仅 40%⇒置信/鲜明/细节量不得单独作可信度权重，须回来源锚点+编码时记录+延迟复测。｜r819C；ScienceDirect 摘要逐字＋科普中国 Phelps/Hirst 十年段逐字；落 r819C 独点2；与 §r775A 高置信≠真实同向但 specialize 情绪震撼事件',
 '- ｜2026-11-28｜meta/mi-memory（r819C）｜机制争议未定论：Brown-Kulik 特殊机制「switches on automatically when surprise/importance exceed threshold」被一般机制模型侵蚀——Conway 1994 综合模型三主过程（已有知识/个人重要性/惊讶激动情绪）+备选（外显复述，部分撒切尔记忆者未复述）、Finkenauer 1998 情绪整合模型加新颖度与对核心人物情感态度，两模型共同结论「是一般记忆机制的产物…但有特别有效率的编码方式」；9/11 研究支持 wrong time slice（一天多来源听到，重测错把后来某次真实接收场合当第一次）、不支持 consolidation（10-11 天初测者不比 1-2 天者更一致，初测次数与自重复述无益）⇒ agent 对高情绪条目不自动加权，立刻固化接收来源与时间、把转述第 N 版显式编号防 wrong time slice，跨领域类比按 rules/08 §五标推断。｜r819C；ScienceDirect 摘要逐字＋科普中国模型段逐字；落 r819C 独点3 + references/r819C_闪光灯记忆.md；判重全库 0 专节',
],
}

for mod, lines in entries.items():
    p = base + '\\' + mod + '\\MEMORY.md'
    t = io.open(p, encoding='utf-8').read()
    assert '## 规则与经验' in t, mod + ' no section'
    add = '\n'.join(lines) + '\n'
    t = t.rstrip('\n') + '\n' + add
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print(mod, 'wrote', len(lines), 'entries')
