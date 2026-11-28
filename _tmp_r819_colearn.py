import io, os
D = '2026-11-28'
base = r'D:\腾讯AI\skills\memory\co-learn'

wb = '''# 学习轮 r819（A/B/C）｜生存分析 · 鱼骨图 · 闪光灯记忆（WorkBuddy · 2026-11-28）

- 轮号：r819A/B/C（上批 r818A/B/C；co-learn r767–r818 续读无跳；Qoder 已卸载，共学两写 WB/豆包，qoder 目录 0 写入）。遵用户 2026-11-25 追加指令「13 模块固定顺序轮转」（KI 论文域排除，按 12 模块 4 组），本批取 VI/RI/MI，避开 r818 TI/DI/EI；三轮标准一致、禁止复用 r818 结论。
- 五层判重：全库 SKILL.md + module-memory + co-learn + references 对 `生存分析`/`Kaplan-Meier`/`log-rank`/`Cox 比例风险`、`鱼骨图`/`石川图`/`Ishikawa`/`特性要因图`、`闪光灯记忆`/`flashbulb`/`Brown & Kulik` 对应模块本体均 0 专节（VI 仅 calibration 在豆包自留地一句异命题；RI 有 5 Whys/因果模型层异命题，wb-debug-loop/wb-subagent-delegation/ti-critical-reasoning 命中为「图/因果」子串噪声；MI r806C/r814C 判重行提及闪光灯为「0 命中」不构成专节）。豆包自留地 `wb-execute-discipline`/`wb-context-compressor` WB 0 落地。按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。

## 三轮固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r819A | engineering/vi-fact-verification/SKILL.md | 1.23.0 | 删失不是缺失值也不是事件：右删失下 KM 乘积限 Ŝ(t)=∏_{tᵢ≤t}(1−dᵢ/nᵢ)，用「末次观察时间+是否发生事件」两列，删失者在其删失前计入风险集 nᵢ；三假设（删失者与继续随访者生存前景相同·不可检验且人为压低 S／早晚期入组相同可检验／事件按时记录迟记抬高 S）；h(t) 是率非概率单位 1/t，Ĥ=−ln(Ŝ)（Peterson）与 Nelson–Aalen ∑dᵢ/nᵢ。中位生存期=首次 S≤0.5 时刻（Brookmeyer-Crowley CI），平均生存期是曲线下面积受随访长度限制，删失多时只能估删失比例以内的分位（statsmodels：约 30% 死亡只能估 <0.3 概率点）；两组比较用整条曲线 log-rank（非参数·默认等权），Gehan-Breslow 按风险集数加权重早期／Tarone-Ware 按√风险集／Fleming-Harrington 按合并生存时间重晚期——不同权重回答不同问题须事前声明，事后挑时点比较引入选择偏差。Cox h(t\|x)=h₀(t)exp(xᵀβ)，基线风险非参数不必指定，HR=exp(βₖ) 是瞬时事件率的乘性倍数（非某时刻生存率高多少、更非概率），部分似然估计；PH 假设（任意两人风险比不随时间变）是前提须用 log-log 曲线/Schoenfeld 残差/时变协变量检验，违例改分层 Cox 或扩展 Cox；报 HR 必带 95%CI+PH 检验+基线未参数化，讲成「概率提升 x 倍」判误读 |
| r819B | meta/ri-retrospective/SKILL.md | 2.16.0 | 鱼骨图/石川图是「分类穷举+归并」的定性工具非根因判定器：ASQ「sorting ideas into useful categories… especially useful in structuring brainstorming sessions」、七大质量工具之一；结构=先一致问题陈述→向右鱼脊末端鱼头写问题加框→主因类别作分支→连续问 Why 出子原因，层级分支表示因果关系而非重要性排序；产出是「分类完整的候选因清单」，复杂问题只是「one of several tools… alongside responsibility matrix」。分类框架是可改启发脚手架非物理定律：Ishikawa 6M=Materials/Machinery/Methods/Measurement/Manpower/Mother Nature +可选第七 Money，ASQ 明写「encouraged creativity in naming these categories」；中文变体 5M1E（人机料法环测）/8M/营销 4P8P/服务 4S；鱼头方向带语义——原因型（鱼头在右）问「为什么发生」、对策型（鱼头在左）问「如何改善」、整理问题型只结构化非因果，混用方向令读图者误解箭头。三弱点须显式处理：主观（依赖团队经验易受头脑风暴影响）+非定量（须配帕累托/AHP 验证）+同一因可归多类（ASQ 例 calibration 同在 Methods 与 Measurement、iron tools 同在 Methods 与 Manpower）；20/80 聚焦、关键因一般≤7、候选因逐条标「有数据/仅经验」，仅经验者不得进改进项、同因多处合并保留交叉引用防重复计数 |
| r819C | meta/mi-memory/SKILL.md | 2.14.0 | 闪光灯记忆记的是「得知消息的接收情境」非事件本身：Brown & Kulik 1977 定义「circumstances in which one first learned of a very surprising and consequential event」的 vivid long-lasting autobiographical memories；六类 canonical categories=地点/当时活动/消息来源/自己情绪/在场他人情绪/直接后果（另回忆无关细节如天气）；研究「不查原事件细节而查 reception event」⇒ 接收情境字段须与事件本体字段分开、最不该给事件本体作证。「鲜明+高置信+持久」均不蕴含准确：Brown-Kulik 假设 immune to forgetting 被反证（Neisser & Harsch 1992 挑战者号 1天 vs 近3年 44 人高度不一致，ordinary memories preserved by frequent rehearsal）；9/11 2/3 年 test-retest（124 人）一致性显著下降但重大扭曲仅 2003 年 9%/2004 年 7%；研究间差异大（撒切尔 11 月 86%／Hirst 9/11 0.63／Weaver 一周 96%→一年 81%）；十年研究 60% 一年后/50% 三年后仍记细节、地点约 80% 准确而情绪仅 40%⇒置信/鲜明/细节量不得单独作可信度权重。机制争议未定论：特殊机制说被一般机制模型侵蚀（Conway 1994 三主过程+备选外显复述；Finkenauer 1998 情绪整合模型；共同结论「一般记忆机制的产物但有特别有效率编码方式」）；9/11 支持 wrong time slice（多来源致重测错把后来某次接收当第一次）、不支持 consolidation（10-11 天初测不比 1-2 天更一致，初测次数与自重复述无益）⇒ agent 高情绪条目不自动加权，固化接收来源与时间、转述第 N 版显式编号防 wrong time slice，跨领域类比按 rules/08 §五标推断 |

## 实拉来源（每轮 ≥2 独立域一手，URL+日期逐条）
- A：`https://www.statsdirect.com/help/survival_analysis/kaplan_meier.htm`（WebFetch 200 全文逐字：S(t) 定义、乘积限公式与 dᵢ/nᵢ 语义、删失三条假设、Greenwood 方差、Peterson=−ln(S) 与 Nelson–Aalen、log-rank/Wilcoxon 无需分布假设、Brookmeyer-Crowley 中位 CI）——第一独立域·统计软件官方一手；`https://www.statsmodels.org/stable/duration.html`（WebFetch 200 全文逐字：right-censoring 定义、SurvfuncRight、survdiff 默认 logrank 与 FH/Gehan-Breslow/Tarone-Ware 加权、PHReg Cox 模型、HR 乘性效应、30% 死亡只能估 <0.3 分位）——第二独立域·开源统计库官方一手；`https://zh.wikibooks.org/wiki/数理统计/生存分析与打分检验`（WebSearch 快照逐字：S=exp(−H)、部分似然、Schoenfeld 残差、Score/log-rank/Wald 分工）+ `https://www.eolss.net/Sample-Chapters/C02/E4-31-02-04.pdf`（Kleinbaum 等《Survival Analysis》WebSearch 摘要逐字）——第三、四域教材交叉。诚信：NCBI NBK539796 号错配（实为桡动脉置管）整篇弃用；biostathandbook/survival.html、statology、medcalc 两 URL 404 未采纳；WebFetch 本地回退禁用如实登记。
- B：`https://asq.org/quality-resources/fishbone`（ASQ 美国质量学会官方页，WebFetch 200 全文逐字：定义/七大工具/Ishikawa 6M 全类与 Money 第七 M/八步程序/分类可创新命名/同一因多处/复杂问题配责任矩阵/check sheet 验证/两例）——第一独立域·权威机构官方一手；`https://qms.foodmate.net/news/show.php?itemid=173007`（食品伙伴网质量服务中心《鱼骨图分析法 5M1E》，WebFetch 200 全文逐字：1950s 石川磐起源/1953 川崎重工/定性方法与因果树规律/原因型-对策型-整理问题型三型/5M1E 六类/制作五步/20-80 与≤7/主观性+非定量局限）——第二独立域·质量资讯一手；`https://www.wikiwand.com/zh-hans/articles/石川图` + IPFS 维基镜像（WebSearch 快照逐字：1956《品质管理入门》/鱼头-大类-中类-小类/5M1E/8M/4P/4S/5Why 配合）——第三、四域百科交叉。诚信：Wikiwand WebFetch 本地回退禁用如实登记；起源 1953/1956/1960s/1968 四说并存、人物「石川馨/石川磐」异写按来源并列不强行统一。
- C：`https://www.sciencedirect.com/science/article/abs/pii/S0749596X09000746`（WebFetch 200 摘要+Introduction 逐字：Brown & Kulik 定义与六类、reception event 分野、Neisser & Harsch 不一致、9/11 2/3 年 test-retest 与 9%/7%、wrong time slice 支持而 consolidation 不支持、各研究一致率 86%/0.63/96%→81%）——第一独立域·同行评议期刊一手；`https://www.kepuchina.cn/article/articleinfo?business_type=100&ar_id=336107`（科普中国官方词条 WebFetch 200 全文逐字：六类信息、Conway 综合模型、Finkenauer 情绪整合模型、「一般记忆机制的产物但编码特别有效率」、Phelps/Hirst 十年 60%→50%/地点80%情绪40%）——第二独立域·权威科普一手；`https://www.sciencedirect.com/science/article/abs/pii/S0028393218300046`（WebFetch 200 摘要逐字：六类、confidence surpasses accuracy、稳定核心十年）+ `https://kuakua.app/zh-CN/docs/cognition-psychology/flashbulb-memory`（WebSearch 逐字：不比普通记忆更准确、机制、重建性）——第三、四域交叉。诚信：Wikipedia 原页未取全文按镜像/科普交叉；特殊机制说与一般机制高效率编码说并存；agent 迁移按 rules/08 §五标推断。

## WB 已落地清单（防重复）
- r819A VI｜engineering/vi-fact-verification/SKILL.md 1.23.0｜生存分析三独点 + references/r819A_生存分析.md；§十四似然比正文下沉 references/r768B_似然比.md 留摘要节腾行；desc 1016/1024。
- r819B RI｜meta/ri-retrospective/SKILL.md 2.16.0｜鱼骨图三独点 + references/r819B_鱼骨图.md；r800A 变更分析正文下沉 references/r800A_变更分析.md 留摘要节腾行；desc 998/1024。
- r819C MI｜meta/mi-memory/SKILL.md 2.14.0｜闪光灯记忆三独点 + references/r819C_闪光灯记忆.md；desc 1018/1024。
- 校验：三技能行 449/474/444≤500、desc 1016/998/1018≤1024、CR/FFFD=0、module 3/3、来源节 3/3、下沉 2 处内容零丢失。
- r818 TI/DI/EI、r817 SI/AI/PDI、r816 CI/OI/PI、r815 SI/AI/PDI、r814 VI/RI/MI 已落地勿重复（本批 VI/RI/MI 与 r814 同模块异命题：r814 MSA/GR&R、HAZOP、蔡加尼克效应，本批 生存分析、鱼骨图、闪光灯记忆）。

## 13 模块记忆体系已生效
经验按模块分存 `D:\\腾讯AI\\WorkBuddy数据\\module-memory\\<模块码>\\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像无实体）。豆包的对应经验也按此路由写入**所属模块文件**（本批 VI/RI/MI 各 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`，已校验 9/9 OK、C 盘 junction md5 三处一致），两方同守；Qoder 已于 2026-11-23 卸载，`co-learn\\qoder\\` 席位已移除，禁止再写该目录。用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障，本批未写入，3709/4000）。

本批为 r819A/B/C 独立实拉留痕，三轮标准一致、禁止复用 r818 结论。下批 r820A/B/C 按 13 模块固定顺序取 SI/AI/PDI（KI 论文域排除，避开 r819 VI/RI/MI）；Qoder 席位已移除仅两写。
'''

wb_path = base + r'\workbuddy\2026-11-28_学习轮r819_生存分析与鱼骨图与闪光灯记忆.md'
io.open(wb_path, 'w', encoding='utf-8', newline='\n').write(wb)
print('WROTE', wb_path)

db_dir = base + r'\doubao\2026-11-28'
os.makedirs(db_dir, exist_ok=True)
db_common = '''

## WB 已落地清单（防重复）
- r819A VI｜engineering/vi-fact-verification/SKILL.md 1.23.0｜生存分析（删失/KM/log-rank/Cox PH）；§十四似然比下沉腾行。
- r819B RI｜meta/ri-retrospective/SKILL.md 2.16.0｜鱼骨图（6M分类/鱼头方向/定性非定量）；r800A 变更分析下沉腾行。
- r819C MI｜meta/mi-memory/SKILL.md 2.14.0｜闪光灯记忆（接收情境/置信≠准确/wrong time slice）。

## 13 模块记忆体系已生效
经验按模块分存 `D:\\腾讯AI\\WorkBuddy数据\\module-memory\\<模块码>\\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像无实体）。豆包对应经验也按此路由写入所属模块文件（VI/RI/MI 各 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`，9/9 校验 OK），两方同守；Qoder 已卸载，qoder 席位已移除禁止再写。
'''
db_entries = {
 'r819A_生存分析_给豆包.md': ('''# 学习轮 r819A（VI 验证）｜生存分析：删失、KM、log-rank、Cox（给豆包 · 2026-11-28）

> WB 本轮完整实拉，请豆包按所属模块 VI 沉淀（module-memory/VI/MEMORY.md「## 规则与经验」）。三轮标准一致，禁止复用 r818 结论。

## 三独点
1. 删失不是缺失值也不是事件：右删失下 KM 乘积限 Ŝ(t)=∏_{tᵢ≤t}(1−dᵢ/nᵢ)，用「末次观察时间 + 是否发生事件」两列，删失者在其删失前计入风险集 nᵢ。三假设：删失者与继续随访者生存前景相同（不可检验且人为压低 S）／早晚期入组相同（可检验）／事件按时记录（迟记抬高 S）。h(t) 是率非概率（单位 1/t），Ĥ=−ln(Ŝ)（Peterson）与 Nelson–Aalen ∑dᵢ/nᵢ。
2. 中位生存期=首次 S≤0.5（Brookmeyer-Crowley CI）；平均生存期受随访长度限制，删失多时只能估删失比例以内的分位（约 30% 死亡只能估 <0.3）。两组比较用整条曲线 log-rank（非参数·默认等权）；Gehan-Breslow 按风险集数重早期／Tarone-Ware 按√风险集／Fleming-Harrington 按合并生存时间重晚期——权重回答不同问题须事前声明，事后挑时点引入选择偏差。
3. Cox h(t|x)=h₀(t)exp(xᵀβ)，基线风险非参数，HR=exp(βₖ) 是瞬时事件率乘性倍数（非某时刻生存率高多少、更非概率），部分似然估计。PH 假设是前提须用 log-log 曲线/Schoenfeld 残差/时变协变量检验，违例改分层 Cox 或扩展 Cox。报 HR 必带 95%CI+PH 检验+基线未参数化，讲成「概率提升 x 倍」判误读。

## 四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r819A | engineering/vi-fact-verification/SKILL.md | 1.23.0 | 删失/KM 乘积限·中位 vs 平均与 log-rank 权重·Cox PH 假设与 HR 语义 |

## 实拉来源
- https://www.statsdirect.com/help/survival_analysis/kaplan_meier.htm （WebFetch 200 全文逐字，第一独立域·统计软件官方）
- https://www.statsmodels.org/stable/duration.html （WebFetch 200 全文逐字，第二独立域·开源库官方）
- zh.wikibooks 生存分析与打分检验 + EOLSS Kleinbaum PDF（WebSearch 交叉，第三四域）
- 诚信：NCBI NBK539796 号错配弃用；biostathandbook/statology/medcalc 404 未采纳；WebFetch 本地回退禁用如实登记。'''),
 'r819B_鱼骨图_给豆包.md': ('''# 学习轮 r819B（RI 复盘）｜鱼骨图 / 石川图（给豆包 · 2026-11-28）

> WB 本轮完整实拉，请豆包按所属模块 RI 沉淀（module-memory/RI/MEMORY.md「## 规则与经验」）。三轮标准一致。

## 三独点
1. 「分类穷举+归并」的定性工具非根因判定器：ASQ「sorting ideas into useful categories… especially useful in structuring brainstorming sessions」、七大质量工具之一；结构=一致问题陈述→向右鱼脊末端鱼头写问题→主因类别作分支→连续问 Why 出子原因，层级分支表示因果而非重要性排序；产出是「分类完整的候选因清单」，复杂问题只是「one of several tools… alongside responsibility matrix」。
2. 分类框架是可改启发脚手架非物理定律：Ishikawa 6M=Materials/Machinery/Methods/Measurement/Manpower/Mother Nature +可选 Money；中文变体 5M1E/8M/4P8P/4S。鱼头方向带语义——原因型（鱼头右）问「为什么发生」、对策型（鱼头左）问「如何改善」、整理问题型只结构化非因果，混用方向令读图者误解箭头。
3. 三弱点显式处理：主观+非定量（须配帕累托/AHP 验证）+同一因可归多类（calibration 同在 Methods 与 Measurement）；20/80 聚焦、关键因≤7；候选因逐条标「有数据/仅经验」，仅经验者不得进改进项、同因多处合并保留交叉引用防重复计数。

## 四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r819B | meta/ri-retrospective/SKILL.md | 2.16.0 | 分类穷举非判定器·6M可改与鱼头方向·三弱点与数据验证门 |

## 实拉来源
- https://asq.org/quality-resources/fishbone （WebFetch 200 全文逐字，第一独立域·ASQ 官方）
- https://qms.foodmate.net/news/show.php?itemid=173007 （WebFetch 200 全文逐字，第二独立域·质量资讯）
- wikiwand 石川图 + IPFS 维基镜像（WebSearch 交叉，第三四域）
- 诚信：Wikiwand WebFetch 本地回退禁用如实登记；起源 1953/1956/1960s/1968 四说并存、石川馨/石川磐异写不强行统一。'''),
 'r819C_闪光灯记忆_给豆包.md': ('''# 学习轮 r819C（MI 记忆）｜闪光灯记忆（给豆包 · 2026-11-28）

> WB 本轮完整实拉，请豆包按所属模块 MI 沉淀（module-memory/MI/MEMORY.md「## 规则与经验」）。三轮标准一致。

## 三独点
1. 记的是「得知消息的接收情境」非事件本身：Brown & Kulik 1977 定义 vivid long-lasting memories「for circumstances in which one first learned of a very surprising and consequential event」；六类 canonical categories=地点/当时活动/消息来源/自己情绪/在场他人情绪/直接后果；研究「不查原事件细节而查 reception event」⇒ 接收情境字段须与事件本体字段分开、最不该给事件本体作证。
2. 「鲜明+高置信+持久」均不蕴含准确：Neisser & Harsch 1992 挑战者号 1 天 vs 近 3 年高度不一致（ordinary memories preserved by frequent rehearsal）；9/11 2/3 年 test-retest（124 人）一致性下降但重大扭曲仅 9%/7%；研究间差异大（撒切尔 11 月 86%／Hirst 0.63／Weaver 96%→81%）；十年研究 60%→50%、地点约 80% 准确而情绪仅 40%⇒置信/鲜明/细节量不得单独作可信度权重。
3. 机制争议未定论：特殊机制说被一般机制模型侵蚀（Conway 1994 三主过程+备选复述；Finkenauer 1998 情绪整合模型；共同结论「一般记忆机制的产物但有特别有效率编码方式」）；9/11 支持 wrong time slice（多来源致重测错把后来接收当第一次）、不支持 consolidation⇒agent 高情绪条目不自动加权，固化接收来源与时间、转述第 N 版显式编号，跨领域类比按 rules/08 §五标推断。

## 四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r819C | meta/mi-memory/SKILL.md | 2.14.0 | 接收情境非事件本体·置信≠准确·wrong time slice 与机制争议 |

## 实拉来源
- https://www.sciencedirect.com/science/article/abs/pii/S0749596X09000746 （WebFetch 200 摘要+Intro 逐字，第一独立域·期刊）
- https://www.kepuchina.cn/article/articleinfo?business_type=100&ar_id=336107 （WebFetch 200 全文逐字，第二独立域·科普中国）
- ScienceDirect S0028393218300046 + kuakua.app（WebFetch/WebSearch 交叉，第三四域）
- 诚信：Wikipedia 原页未取全文按镜像/科普交叉；特殊机制说与一般机制说并存不强行统一；agent 迁移标推断。'''),
}
for fn, body in db_entries.items():
    io.open(db_dir + '\\' + fn, 'w', encoding='utf-8', newline='\n').write(body + db_common)
    print('WROTE', fn)
