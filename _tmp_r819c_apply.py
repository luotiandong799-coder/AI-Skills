import re, io
p = r'D:\腾讯AI\skills\meta\mi-memory\SKILL.md'
t = io.open(p, encoding='utf-8').read()

# 1) desc add triggers (has room: 976 + ~90 = under 1024)
add = '·闪光灯记忆flashbulb（Brown-Kulik1977·六类接收情境·鲜明自信≠准确·一致性随时间降·wrong-time-slice非巩固·情绪唤醒与复述非特殊机制·agent高置信条目须验来源）'
dm = re.search(r'^(description: .+)$', t, re.M)
t = t[:dm.start(1)] + dm.group(1) + add + t[dm.end(1):]

# 2) bump version
t = t.replace('version: "2.13.0"', 'version: "2.14.0"', 1)

# 3) append section
sec = '''

## r819C · 闪光灯记忆（flashbulb memory）：鲜明与高置信不是准确性证据，接收情境也会随重述漂移（MI · 2026-11-28 实拉，≥3 独立域一手）

**独点 1｜闪光灯记忆记的是「得知消息的接收情境」，不是事件本身；六类 canonical categories 是核对清单。** Brown & Kulik (1977) 定义逐字：对「the *circumstances* in which one first learned of a very surprising and consequential (or emotionally arousing) event」的「particularly vivid and long lasting (autobiographical) memories」（p.73）。关键分野——研究「不查对原事件细节的记忆，而查所谓的 reception event——一个人第一次听到消息时的个人处境」（ScienceDirect 逐字）。Brown & Kulik 报告人们至少能回忆起六类 canonical categories 之一：**地点 / 当时活动 / 消息来源(informant) / 自己情绪 / 在场他人情绪 / 直接后果**，许多人还回忆无关细节（「the weather was cloudy and grey」）。⇒ 记忆核验里，「我在哪/谁告诉我/我当时在做什么」这类**接收情境**字段与「事件本体」字段必须分开存放：前者恰恰是最易被重述污染、最不该拿来给事件本体作证的部分。

**独点 2｜「鲜明 + 高置信 + 持久」三项都不蕴含准确；一致性随时间下降，且不同研究的下降幅度差异极大。** 早期 Brown & Kulik 假设闪光灯记忆「unusually long-lasting and accurate, as well as immune to forgetting」，后续研究反证：Neisser & Harsch (1992) 在挑战者号爆炸后 1 天与近 3 年两次访谈 44 名本科生，前后报告「a high degree of inconsistency」，结论是它们「not necessarily consistent, and are ordinary memories that have been preserved by frequent rehearsal rather than by the operation of some special encoding mechanism」。ScienceDirect 的 9/11 研究（test–retest 2、3 年，124 人）：「Despite a reliable drop in consistency over the long delay periods, mean consistency scores were fairly high and the number of memories classed as 'major distortions' was remarkably low in both 2003 (9%) and 2004 (7%)」；但不同事件口径差异极大——撒切尔辞职 11 个月后 86% 一致、9/11 相似延迟 Hirst 2009 只有 0.63、Weaver & Krug 一周内 96% 一致而一年后降至 81%。科普中国引 Phelps/Hirst 十年研究：约 60% 一年后仍记得很多细节、三年降至 50%，「说明闪光灯记忆并不比其他类型的记忆更准确」；地点记忆准确度约 80% 而当时情绪只有 40% 准确。⇒ 判据：置信度、鲜明度、细节量三者都**不得**单独作为条目可信度权重，必须回到「来源锚点 + 编码时记录 + 延迟后复测」；这与 §r775A 错误记忆「高置信≠真实」、§十一「即时命中≠延迟保持」同向，但对象 specialize 在「情绪震撼事件的接收情境」。

**独点 3｜机制争议未有定论：特殊编码假说被一般机制模型侵蚀，wrong-time-slice 解释扭曲来源。** Brown & Kulik 原主张「special brain mechanism that switches on automatically whenever the levels of surprise and importance or consequentiality exceed a certain 'threshold'」。Conway 等 (1994) 综合模型给出三主过程 + 一备选：已有知识（把当前事件挂到已有记忆结构）/ 个人重要性 / 惊讶与激动的情绪状态 / 外显复述（备选，部分撒切尔记忆者并未复述）；Finkenauer 等 (1998) 情绪整合模型加事件新颖度与对核心人物的情感态度。两模型共同结论逐字：「闪光灯记忆是一般记忆机制的产物。但是，闪光灯记忆有许多具体细节构成，有良好的清晰度和保持度。这些事实说明它有一个特别有效率的编码方式」。9/11 研究进一步：结果符合 **wrong time slice hypothesis**（一天内从多个来源听到消息，重测时错把后来某次真实接收场合当第一次），**不支持 consolidation hypothesis**（10–11 天后初测者并不比 1–2 天者更一致；初测次数与自重复述均无益）；结论「flashbulb memories may be formed automatically and consolidated fairly soon after an emotional event」。⇒ 落地口径：写入侧对「高情绪/高冲击」条目**不自动加权**，反而要立刻固化接收来源与时间、并把「他人转述的第 N 次版本」显式编号（防 wrong time slice）；agent 不能因为「这条记得特别清楚」就跳过溯源——这是人类结论跨领域类比，按 rules/08 §五标推断不作既定实证。

**判据（MI 落地）**：高情绪/高冲击来源的条目验三件事——① 事件本体与接收情境是否分字段；② 置信/鲜明/细节量是否被误当准确性；③ 是否有编码时来源锚点与延迟复测，转述链是否编号。缺一判「高置信未验证」，不得升格为事实条目。与 §r775A 错误记忆（语义要点自发长出高置信错误）、§r787A 近因态（延迟+干扰后仍可取回才算落地）、§r759A 前瞻记忆（意图三元组）、§r791A 干扰正交分工，均异命题。

**判重**：全库 SKILL.md / module-memory / co-learn 对 `闪光灯记忆` / `flashbulb` / `Brown & Kulik` 0 专节（MI r806C/r814C 判重行仅提及该词为「0 命中」，不构成专节）；豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地。

**来源与诚信**：`https://www.sciencedirect.com/science/article/abs/pii/S0749596X09000746`（WebFetch 200 摘要+Introduction 逐字：Brown & Kulik 定义与六类、reception event 分野、Neisser & Harsch 不一致、9/11 2/3 年 test-retest 与 9%/7% 重大扭曲、wrong time slice 支持而 consolidation 不支持、各研究一致率 86%/0.63/96%→81%）——第一独立域·同行评议期刊一手；`https://www.kepuchina.cn/article/articleinfo?business_type=100&ar_id=336107`（科普中国官方词条 WebFetch 200 全文逐字：Brown-Kulik 六类信息、Conway 综合模型三主+备选、Finkenauer 情绪整合模型、「一般记忆机制的产物但编码特别有效率」结论、Phelps/Hirst 十年 60%→50%/地点80%情绪40%）——第二独立域·权威科普一手；`https://www.sciencedirect.com/science/article/abs/pii/S0028393218300046`（WebFetch 200 摘要逐字：六类 canonical categories、confidence surpasses actual accuracy、FM 并非免疫遗忘、9/11 稳定核心与十年稳定）与 `https://kuakua.app/zh-CN/docs/cognition-psychology/flashbulb-memory`（WebSearch 快照逐字：Talarico & Rubin 2003 不比普通记忆更准确、情绪唤起/杏仁核/意外检测/复述机制、重建性）——第三、四独立域交叉。诚信：Wikipedia 原页未取全文按镜像/科普交叉；「特殊神经机制」与「一般机制高效率编码」两说并存不强行统一；agent 迁移按 rules/08 §五标推断。逐字全文与判非见 `references/r819C_闪光灯记忆.md`。
'''
t = t.rstrip('\n') + '\n' + sec
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

ref = '''# r819C 闪光灯记忆逐字取证 · 2026-11-28

> 载体：meta/mi-memory SKILL.md r819C 节（version 2.14.0）。≥3 独立域一手交叉。

## 一手域 1 — ScienceDirect《Consistency of flashbulb memories of September 11 over long delays》(WebFetch 200 摘要+Introduction 逐字)
URL: https://www.sciencedirect.com/science/article/abs/pii/S0749596X09000746
- 定义："particularly vivid and long lasting (autobiographical) memories 'for circumstances in which one first learned of a very surprising and consequential (or emotionally arousing) event' (Brown & Kulik, 1977, p. 73)"
- 六类："at least one of the six so called 'canonical categories' about this reception event (the location, activity one was engaged in, source of news or informant, own emotion, others emotion and immediate aftermath)"；无关细节 "the weather was cloudy and grey"。
- reception event 分野："they do not examine one's memories for the details of the original event itself but for the so-called reception event – one's personal circumstances in which the news was first heard."
- 特殊机制原假说："encoded by a special brain mechanism that switches on automatically whenever the levels of surprise and importance or consequentiality exceed a certain 'threshold'."
- test-retest 方法："comparing participants' memory reports obtained soon after the event (preferably within the first 48 h) and then again at some later date"。
- Neisser & Harsch 1992："interviewed 44 undergraduates about their flashbulb memories of the Challenger explosion 1 day after the event and again after almost 3 years"；"a high degree of inconsistency"；结论 "not necessarily consistent, and are ordinary memories that have been preserved by frequent rehearsal rather than by the operation of some special encoding mechanism"。
- 本研究："test–retest delays of 2 and 3 years"、124 人；"Despite a reliable drop in consistency over the long delay periods, mean consistency scores were fairly high and the number of memories classed as 'major distortions' was remarkably low in both 2003 (9%) and 2004 (7%)."
- wrong time slice："explains the development of distortions by hearing the news from multiple sources on the day of the flashbulb event"；"people hear the important news from several different sources throughout the day and, at re-test, incorrectly remember some other (but real) occasion of hearing the news instead of the first occasion."
- consolidation 不支持："memories of participants who were initially tested 10–11 days after September 11 were not more consistent than memories of participants tested 1–2 days after the event"；"the number of initial tests… and self-reported rehearsal did not have any beneficial effects on consistency."
- 结论："flashbulb memories may be formed automatically and consolidated fairly soon after an emotional event."
- 各研究一致率："86% of participants had consistent flashbulb memories"（撒切尔 11 个月）/"Hirst et al. (2009), the mean consistency score after a similar delay was only .63"/"near ceiling after 1 week from the first test (96%) and dropped reliably to 81% at 1-year re-test"/>

## 一手域 2 — 科普中国官方词条（WebFetch 200 全文逐字）
URL: https://www.kepuchina.cn/article/articleinfo?business_type=100&ar_id=336107
- "闪光灯效应 (flashbulb effect)指个人对引人震撼的事件容易留下深刻的记忆，又称闪光灯记忆。"
- Brown-Kulik 六类：信息提供者 / 听到消息时位置 / 正在发生事件 / 自身情绪 / 他人情绪 / 事件后果；"其理论的核心观点是，闪光灯效应在其保持时间、准确度和所依赖的独特神经机制这些方面与其它记忆很不相同。"
- Conway 1994 综合模型：已有知识（把当前事件同已有记忆结构联系）/ 个人重要性 / 惊讶和激动的情绪状态 / 外显复述（备选，部分撒切尔记忆者未复述）。
- Finkenauer 1998 情绪整合模型：加事件新颖度与对核心人物的情感态度。
- 共同结论："闪光灯记忆是一般记忆机制的产物。但是，闪光灯记忆有许多具体细节构成，有良好的清晰度和保持度。这些事实说明它有一个特别有效率的编码方式。"
- Phelps/Hirst 十年 9/11："大约有60%的人在1年之后仍记得很多细节，3年之后，这一比例降至50%，说明闪光灯记忆并不比其他类型的记忆更准确"；"参与者地点记忆的准确性高达80%左右，但只有40%的人能够准确回想起当时的情绪。"

## 交叉域 3/4 — WebFetch/WebSearch 逐字
- https://www.sciencedirect.com/science/article/abs/pii/S0028393218300046（WebFetch 200 摘要逐字）："the reception event (Brewer, 1992)"；六类 "place, activity, informant, the person's affect, affect in others present, aftermath"；"more vivid… accompanied by an enhanced confidence in the accuracy, which tends to surpass the actual accuracy"；"not resistant to forgetting and can, moreover, be somewhat inaccurate"；9/11 "a stable core of the memory remained after a consolidation period of one year"，"remained stable even after a period of ten years"。
- https://kuakua.app/zh-CN/docs/cognition-psychology/flashbulb-memory（WebSearch 逐字）："研究表明它们并不比普通记忆更准确——它们以相同速度消退。特殊之处在于鲜明与自信，而这两者都不是准确性的指标"；"记忆是重建性的：鲜明与自信并不能保证真实。"

## 诚信登记
- Wikipedia 原页未取全文，不冒充一手；ScienceDirect 两篇同站不同条目按来源族折叠，独点靠不同原文句支撑。
- 「特殊神经机制」与「一般机制但编码特别有效率」两说并存不强行统一；consolidation/wrong-time-slice 争议如实登记。
- agent 高置信条目溯源按 rules/08 §五标推断，不作人类实证直接外推；豆包自留地 WB 0 落地。
'''
io.open(r'D:\腾讯AI\skills\meta\mi-memory\references\r819C_闪光灯记忆.md', 'w', encoding='utf-8', newline='\n').write(ref)

t = io.open(p, encoding='utf-8').read()
dm = re.search(r'^description: (.+)$', t, re.M)
print('LINES', t.count(chr(10))+1, 'DESC', len(dm.group(1)), 'VER', re.search(r'version: "([^"]+)', t).group(1), 'CR', t.count(chr(13)), 'FFFD', t.count(chr(0xFFFD)))
