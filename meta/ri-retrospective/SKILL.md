---
name: ri-retrospective
description: 经验复盘与持续改进（Reflection Intelligence）。当任务完成或失败后需要沉淀经验、比较预期与实际、做根因分析、总结可复用规则时调用。提供 verification-discipline / handoff-protocol / engineering-economy 等方法论、无责复盘仪式、复盘准入触发器、行动项可验收动词门与三类关闭态、决策质量与结果质量分栏评分、决策时间线与结果偏差/归因偏差三列门，产出复盘报告。RI 可提议修改 Skills/提示词/规则/工作流，但未经授权不得直接改系统核心配置、复盘标签体系与跨事故模式聚合（severity 与 taxonomy 分工、受控枚举、已知/潜在与原文锚点）。
module: RI
modules: RI,EI
version: "1.6.0"
---

# RI · 经验复盘与持续改进（Reflection Intelligence）

> 本技能是 Personal AI OS 13 模块中 **RI（复盘智能）** 的载体之一（与 `wb-debug-loop` 调试复盘、`agent-guild` learnings 互补）。
> 方法论实拉（2026-11-07 实拉）：`github.com/poloplay0114/hard-won-claude-skills`（8 个从真实生产事故提炼的工程复盘技能，MIT）。

## 一、触发

- 任务完成或失败，需把经验变成下次更好的能力。
- 出现"看起来对其实不对"的偏差、误报绿、交接错位。

## 二、核心方法论（每条规则背后有事故）

1. **verification-discipline（证明对，而非看着对）**
   - 独立 oracle：用与生成者无关的渠道验证（如真实 Excel 打开而非库容忍）。
   - 绝不轻信自报结果：工具说自己成功 ≠ 真的成功。
   - 精确对账：数值/状态逐项比对，不留"差不多"。
   - 比较锚点：用已知正确样本作基准。

2. **handoff-protocol（与实现者协作不失控）**
   - 一句话结论：先给结论再给过程。
   -  phantom stall vs 真实失败：区分"卡住"与"已挂"。
   - 双向对账：双方状态互认，不假设。
   - 自曝假绿：曾报绿但实际未完成的，主动标注。

3. **engineering-economy（最小改动）**
   - 最小改动、最短测试、最佳特性。
   - 动手前先看外部世界（依赖/环境/契约）。
   - 先冻结契约（接口/§条款）再改实现。
   - 性能由基线断言守住。

4. **spec-citation（条款即公共 API）**
   - 编辑前 grep 活引用；语义锚点优于行号。

## 三、复盘报告模板

```
## 复盘：<任务>
- 预期 vs 实际：
- 根因（逐层追问到可改）：
- 应保留（做对的）：
- 应停止（踩的坑）：
- 可复用规则（写入 MI 的条例）：
- 改进建议（含是否需调 EI Guard / 提示词 / 工作流）：
- 证据（日志/产物/截图）：
```

## 四、护栏

- RI **可提议**改 Skills/提示词/规则/工作流，但**不得未经授权直接改系统核心配置**（模型路由、权限、Hook、MCP）。
- 改进项须经验证（在独立集测过）才升级为系统规则；未经验证不得自动生效。

## 五、无责复盘方法论（2026-11-07 第二轮实拉深化）

> 上轮 coverage 偏"工程纪律"（verification-discipline/handoff 等）；本轮补"仪式 + 方法 + 闭环"——复盘开成批斗会百次无用，须让人错也不会出大事的系统视角。

### 5.1 无责复盘（Blameless Postmortem）标准骨架
摘要 → 影响范围（量化：用户数/金额/时长）→ 时间线（从真实开始而非发现）→ 检测与响应 → 根因分析 RCA → 促成因素 → 经验教训 → 行动项。语言中性："什么条件允许了事件发生"而非"谁弄坏"。

### 5.2 根因分析三法
- **5 Whys**：连问五层到机制层（"人不仔细"不是根因，"流程允许 100% 直上"才是）。
- **故障树 FTA**：自顶向下拆解故障为与/或组合，定位关键路径。
- **排障树（LLM 适配）**：节点只问是非题，每步先看视图（span 树 / 三本账 / 版本标签）再动手，叶子全是止损动作；口诀"慢看段占比、错看责任层、坏看版本对齐、贵看三本账"，"当天有变更吗"是最高杠杆问题。

### 5.3 无责五问（Google SRE 落到 LLM 应用）
1. 什么坏了（现象+影响面，数字来自三支柱，非形容词）；
2. 为什么没能更早发现（哪信号该亮没亮）；
3. 为什么会发生（根因链到机制层）；
4. 怎么更快恢复（告警到止损实际用时）；
5. 怎么防止再发（行动项带责任人+验收，下次复盘开场先查上次闭环）。

### 5.4 行动项闭环（反模式预警）
- 必须有 **owner + 到期日 + 验证测试**（证明生产不再复现才算闭环）；无 owner=愿望，无日期=永不排期。
- 反模式：开成追责会（下次没人留真时间线）；行动项写"加强意识"（不可验收=不会发生）。
- 时效：事件后 24–72h 启动；MTTA/MTTR 按严重度分别跟踪趋势，而非混算均值。

### 5.5 与本章关系
上轮纪律 + 本节仪式方法 = 完整复盘；复用 §三 模板时按 5.1 骨架填、5.3 五问挖、5.4 闭环。

## 六、与 OS 协作

- 复盘产出 → **MI** 沉淀为"已验证经验"；可复用规则进长期记忆。
- 改进项（经验证）→ **AI** 调优 EI Guard / 提示词 / 工具顺序。
- 反复失败模式 → 回 **TI/DI** 重审方案。

## 七、复盘准入与行动项存活率（2026-11-08 r706C 实拉）

> 与 §五 分工：§五 给「无责仪式 + 根因三法 + 五问」；本节给**开不开复盘、复盘中写什么才算数、行动项为什么大批死掉**。§5.4 已定「owner + 到期日 + 验证测试」，本节不重复这三项，只补它没覆盖的准入、动词、存放位置与关闭态。

### 7.1 ★触发条件必须在事故之前定义

- Google SRE 逐字："It is important to define postmortem criteria before an incident occurs so that everyone knows when a postmortem is necessary. In addition to these objective triggers, any stakeholder may request a postmortem for an event."
- 客观触发器清单（照搬其结构，个人场景映射）：用户可见降级超阈值 · 任何数据丢失 · 需人工介入回滚/改道 · 解决时长超阈值 · 监控失效（意味着靠人发现）。
- 判据：**「要不要复盘」不应该由当事人事后凭感觉决定**——事后判断会被「这次好像不严重」「已经修好了」系统性稀释；事先写死阈值 + 允许任何干系人提名，才不会漏掉最有价值的失败。
- 另有一层：**复盘文档与复盘会议是两个东西**——postmortem 是 artifact，incident review 是同步会议；文档应在会议开始前就存在，不是在会上现写（incident.io 指南）。

### 7.2 贡献因素 / 缓解因素 / 风险三分，拒绝单一根因

- incident.io 逐字：Contributors "not as 'root causes' but as a set of conditions that allowed the incident to happen, or made it as bad as it was"；并单列 **Mitigators**（哪些控制奏效、减小了影响，值得强化与共享）与 **Risks and learnings**（如「只有一人懂该系统」的 key person risk）。
- 判据：**只找「那个根因」会漏掉两半信息**——让事故变严重的条件（contributors）和让事故没更糟的条件（mitigators）。后者是「应保留」的证据来源，不写就等于下次可能把它删掉。
- 与 §5.2 的 5 Whys/FTA 不冲突：那两法用于向机制层下钻；本条管**下钻前先把面铺开**，避免一开始就锁死在一条因果链上。

### 7.3 ★行动项动词门：过程动词不算行动项

- incident.io 逐字："'Review', 'explore', 'investigate' describe activity, not change. They are easy to start and impossible to finish in any meaningful sense. Prefer verbs that create a visible result: add, remove, change, update, test, deploy."；"If an action starts with 'review', it's worth asking what decision that review leads to - and making that the actual action."
- 对照表（写进复盘模板的硬门）：

| 过程动词（禁作最终行动项） | 结果动词（可验收） |
|---|---|
| Review / Explore / Investigate / Discuss / Consider / Evaluate | Add / Remove / Change / Update / Test / Deploy |

- 判据：**「复查监控」永远没有完成态**；把它改写成「这条 review 要导向什么决定」，把决定本身写成行动项。接 §5.4「加强意识不可验收」，本条给可机检的动词白名单。

### 7.4 行动项的四种死法 + 第五种（系统性）

incident.io 逐字归纳（"How actions die"）：

1. **Nobody owns it** —— "the team should improve monitoring" 是共同意向不是行动；名字才是意向与承诺的分界。
2. **It lives in the wrong place** —— 只写在复盘文档或临时表格里，不进日常真正打开的工具（tracker），等于借来的时间。
3. **It's a direction, not a task** —— "Improve alerting" 是罗盘方向不是目的地，没有「yes, done」的那一刻。
4. **Nobody checks** —— 没有人在既有的站会/交接里问一句「还有未闭环的复盘行动吗」。
5. **系统性问题是 leadership problem** —— 「理清组件归属」「改激励结构」不该伪装成工程任务塞进 sprint；正解是具名缺口 + 量化后果 + 具体方案 + 给对层级的人 + 期限（例："Component X has no clear owner, which meant it took 40 minutes to find someone…Can we assign ownership to Team Y by end of month?"）。

**反近因偏差（soak time）**：incident.io 指南逐字 "with the influence of recency bias … there's a temptation to prioritize tasks that may not be worth the effort"，故建议给负责团队一段沉淀时间再决定是否承诺，并「we'd encourage you to avoid committing to actions until the owning team has had time to … weigh up the relative importance」；行动项应与事故严重度成比例，讨论时还要看二阶效应（新行动可能引入新风险）。⇒ **复盘会上当场拍出的长清单不是成果，是偏差产物**。

### 7.5 ★无责 ≠ 无人负责：blame 向后，accountability 向前

- incident.io 逐字："Blame is backward-looking. Accountability is forward-looking."；"we're assigning ownership of the fix, not responsibility for the incident"。
- 与 §五 张力互补：§5.1 要求语言中性「什么条件允许了事件」，本条补上**为什么仍需具名 owner**——两者不矛盾，因为归属的是「未来的修复」而非「过去的过错」。缺这句，团队会误把无责读成「行动项不用写名字」，正好触发 7.4 第 1 种死法。
- 复盘会上主动把这句话说出来，能显著降低认领阻力。

### 7.6 关闭是显式动作（三类终态）

- incident.io 逐字："closing a post-mortem should be a deliberate act. Either the actions are done, or they've been explicitly deprioritised with a reason… 'We decided not to do this because the risk is low and the effort is high' is a completely valid outcome. What tends to go wrong is the action quietly rotting in a backlog until it gets archived and forgotten."
- 三类合法终态：**已完成（有验证）** / **显式降优先级（写明理由）** / **升级为系统性问题（交对应层级）**；第四类「静默腐烂到归档」是唯一非法态。
- 节律：不新开会，在已有仪式里加一句常设问题 "any open incident actions?"（两分钟），加两星期一次轻提醒；长期挂起的同类行动是信号——要么真不重要（显式关），要么有结构性阻塞（上报）。
- **闭环要可见**：下次复盘时点名「上次那条告警真的拦住了一次故障」，让「行动项 → 被预防的事故」这条因果被看见，否则没人愿意认领下一条。

### 7.7 写作质量与时效（SRE workbook 好复盘五特征）

- **Promptness**：事故结束后一周内写完并传阅；原文 "The longer you wait, the more they will fill the gap with the products of their imagination"。
- **可量化 + 数据驱动**：影响给出数字（用户数/时长/命中率），结论所依据的原始数据要能从文档点开；长日志/聊天记录做摘要、原文留链接。
- **面向超出直接团队的读者**：Background / Glossary 不能空，术语先解释（接 §三 模板，补其缺项）。
- **行动项五要素**：owner + tracking number + priority + verifiable end state + 按主题分组并区分 **Prevent / Mitigate**（本条只作为 SRE 原文归档，不与 §5.4 的三要素重复主张）。
- **深度**：不止查故障邻近区域，跨团队看影响与系统缺陷。

## 八、复盘有效性用复发率验收 + 反事实语言门 + 替换测试（2026-11-08 r717C 实拉）

> 与 §七 分工：§7.1 准入触发器、§7.3/7.4 管**单条行动项**的动词与四种死法、§7.6 关闭三态；本节管**组织级有没有真的学到**（验收指标与季度仪式）、**复盘文档怎么写才不污染归因**（语言门 / 局域理性 / 主持中立），以及**无责与问责的可操作分界**。

### 8.1 ★验收指标是复发率，不是文档数或行动项完成率
- zakhassan 逐字："The most direct signal is incident recurrence rate — the fraction of incidents that represent a failure mode you've seen before. A genuine learning culture drives this number down over time."；前提是给事故打 `failure_mode` / `is_recurrence` 标签并按 90d 窗口查询（原文给出 PromQL 分子分母）。
- 配套三个量："action item closure velocity — the ratio of action items completed per quarter to action items opened. If this ratio is below 1.0, your backlog is growing and systemic debt is accumulating faster than you're paying it down"；"items older than 90 days without progress are a signal of organizational prioritization failure, not engineering failure"；心理安全用季度 1–5 脉冲 + 独立发言人数 / 出席人数衡量参与分布。
- 收口："The goal was never to have better postmortem documents."；"If your system design looks the same a year from now despite a year of postmortems, the learning culture is aspirational rather than real."；stackademic 交叉："repeat incident rate ... above 30%, your postmortems are producing documentation, not learning"，且"时间线凭记忆重建、根因停在症状"是典型坏味道。
- ⇒ **「行动项全关了但复发率不降」仍判复盘无效**；与 §7.4 分层：那条管单条存活，本条管组织级成效。落地：复盘台账必须带失效模式标签，季度算复发率 + 闭环速度比 + 90 天存量；写「本轮产出 N 篇复盘」不算成效证据。
- ★**单次复盘与季度学习复盘是两层**：zakhassan "A postmortem is incident-specific ... Individual incidents are noisy ... Treating each incident in isolation also makes it easy to miss patterns — the same class of failure appearing in different subsystems, the same type of action item that never gets implemented"；Learning review 每季度跑，把复盘语料当 "evidence about the state of the sociotechnical system, not just a collection of individual events"，议程五段（事故清单 / 模式分析含 "same root class appearing ≥2x" / 行动项审计含「上季被降优先级的项是否牵涉本季事故」/ 心理安全脉冲 / 前瞻风险）。反事实换框：不问 "what caused this?"，改问 "what would have had to be true for this incident not to happen?"，列**联合充分**的多个条件，按 generalizability 与 cost 挑干预组合 ⇒ "portfolio of interventions that would reduce the probability of this class of incident"。

### 8.2 ★反事实语言门 + 局域理性 + 主持中立（可机检）
- tinycto 逐字："Counterfactual reasoning—speculating about what people 'could have, should have, or failed to do'—is the most pervasive anti-pattern in incident postmortems. It is fueled by hindsight bias: knowing the outcome makes the failure seem obvious in retrospect."；"True blameless postmortems ban counterfactual language."
- 四条硬规则："Ban counterfactual words: Scrub words like 'could have', 'should have', 'failed to', 'carelessly', and 'inadvertently'"；"Reconstruct the local rationality: Map out the exact UI screens, alert notifications, and architectural assumptions present during the action"；改为问 "Given the information, dashboard signals, time pressure, and organizational tools available to the engineer at that exact second, why did their action make complete sense to them at the time?"；行动项要技术护栏（automated schema validation / read-only DB replays / CI-CD gating / IAM scoping）而非 "remind developers to be more careful"。
- **可机检**：tinycto "establish automated linting rules on postmortem markdown templates to flag words like 'should have' or 'human error'" + "Appoint trained postmortem facilitators outside the impacted team"；sph.sh "Hindsight bias in the timeline. Build it strictly from what each responder knew at the time, not from what the reviewers know now"；pmmilestone "Reconstruct the timeline first using logs, chat transcripts and pager data. Only then discuss what to do about it"、"Cap action items at five. A postmortem with 27 actions produces zero completed actions"、"Someone not directly involved in the incident" 主持。
- sph.sh 的复发实例：第一次复盘停在「谁 merge 的 + 测试覆盖率 should have caught it」，同类 bug 两个发布周期后由**另一个人、另一条代码路径**复发；第二次深入到「无幂等保证 / 无 dry-run / 两服务无共享锁」并加幂等键、dry-run、重复写告警，该类才不再出现。⇒ **措辞不是文风问题，是会不会找到真因的因果开关**。

### 8.3 ★替换测试：无责与问责的可操作分界
- sph.sh 逐字："The substitution test is the hinge. It comes from James Reason's work and was popularized in Dekker's Just Culture. Would another competent person, with the same information and the same pressures, likely have made the same choice? If yes, the problem is the situation, not the person, and you stay in blameless analysis. If a reasonable peer clearly would not have, you have moved toward genuine recklessness, and the accountability path applies."；且 "Even then, the system learning still happens; an accountability case does not excuse the organization from fixing the conditions."
- PagerDuty 的诚实修正："perfect blamelessness is unrealistic, because human bias toward attribution does not vanish on command. They prefer 'blame awareness'"，模板**刻意不设「谁造成事故」字段**，响应者只以角色出现（"the on-call engineer" / "an unspecified responder"），名字不作为归责载体。
- 其余可复用动作：pmmilestone "Highlight near misses as well as full incidents. A caught-in-canary bug carries the same lessons at a fraction of the cost"、"Read old reports before writing a new one. Half the time the current incident is a variant of a past one, and the past report has the fix"、"Repeat incidents are review failures, not incident failures"。
- ⇒ 与 §7.5「无责 ≠ 无人负责」互补：那条是原则声明，本条给**判定测试**。落地：复盘模板 + 禁用词 lint + 当事者视角时间线 + 局域理性栏 + 场外主持人；是否转问责由替换测试裁定，不靠主持人直觉。
- 判非：§7.2 三分、§7.3 动词门、§7.4 四死法、§7.6 三类关闭态均不重复；全库 `替换测试` / `局域理性` / `local rationality` / `facilitator` / `repeat incident` / `near miss` 词边界 0 命中；`复发率` 仅 `wb-debug-loop` KB「按症状分诊导致复发率统计不出来」（不同命题）。

## 九、来源（2026-11-07 首拉 / 2026-11-08 r706C、r717C 增补）

- github.com/poloplay0114/hard-won-claude-skills（verification-discipline / handoff-protocol / engineering-economy / spec-citation / cache-discipline / ui-station-delivery，MIT，2026-08）
- 互补：本仓 `engineering/wb-debug-loop`（调试复盘）、`agent/agent-guild`（learnings 台账）

### 本轮深化来源（2026-11-07 实拉，无责复盘）
- blameless.com/blog/incident-retrospective-postmortem-template（无责复盘标准模板）
- itoc360.com（MTTA/MTTR 指标 + blameless 模板骨架）
- aiknowledge.cn/article/75075（排障树 / 无责五问 / LLM 适配）
- renrendaima.com/wap/article/2354.html（无指责 Postmortem / 5 Whys / FTA）
- yisu.com/zixun/1107281.html（运维事后分析结构）

### 2026-11-08 r706C 增补来源（逐字核验，双独立域交叉）

- sre.google/sre-book/postmortem-culture/（Ch.15：postmortem 定义、三个主要目标、客观触发清单、「define postmortem criteria before an incident occurs」、any stakeholder may request、blameless 假定人人善意且按当时信息做了正确的事、「You can't 'fix' people, but you can fix systems and processes」）
- sre.google/workbook/postmortem-culture/（好复盘五特征：Ownership/Prioritization/Measurability/Preventative action/Blamelessness；"A postmortem with no action items is ineffective"；Promptness 一周内传阅、长日志摘要+原文链接；Missing context / Key details omitted 反面案例）
- sre.google/static/pdf/Anatomy_Of_An_Incident.pdf（AI 需 owner 与 deadline、时间线六时点、live document 事中记录、"Events should be analyzed in order to draw conclusions, not simply recounted"、最大范围共享）
- incident.io/blog/why-post-mortem-action-items-die（2026-04-16，WebFetch 全文：四种死法 + 第五种系统性问题、结果动词 vs 过程动词、"Blame is backward-looking. Accountability is forward-looking."、follow-up ritual 常设问题、closing 是 deliberate act、显式降优先级、让闭环可见）
- incident.io/guide/learn-and-improve/incident-reviews（Contributors / Mitigators / Risks and learnings 三分、recency bias 与 soak time、二阶效应、行动项与严重度成比例）
- incident.io/blog/sre-incident-postmortem-best-practices（postmortem=artifact vs incident review=会议、文档应会前存在；blameless 不是无后果；语言对照表；psychological safety）
- incident.io/blog/why-do-post-mortem-action-items-fail-how-to-make-incident-follow-ups-actually-get-done（动词对照表全量、系统性升级五步公式、"we're assigning ownership of the fix, not responsibility for the incident"）
- 判非：§5.4 已有的 owner+到期日+验证测试、§5.2 的 5 Whys/FTA/排障树、§5.1 无责骨架与量化影响均不重复落地；`wb-agent-evaluation` 的评测有效性、`wb-debug-loop` 的调试六道门亦不在此重落。

### 2026-11-08 r717C 增补来源（逐字核验，四独立域交叉）

- zakhassan.com/blog/building-a-learning-culture-from-incidents-beyond-blameless-postmortems（2026-05-07，Staff SRE；incident recurrence rate 定义 + PromQL 90d 查询、closure velocity <1.0、>90 天无进展是优先级失败、季度 Learning Review 五段议程与模板、反事实分析「what would have had to be true」、供应商故障专门节、"The goal was never to have better postmortem documents"；WebFetch 全文逐字）
- tinycto.tv/learn/blameless-postmortem-counterfactual-bias（counterfactual 是最普遍反模式、hindsight bias、禁用词表 could/should have/failed to/carelessly/inadvertently、局域理性重构原问句、latent traps、技术护栏型行动项、markdown 模板 lint、场外 facilitator、Dekker Safety Differently；WebFetch 全文逐字）
- sph.sh/en/posts/blameless-culture-postmortem-thinking（2026-06-21；Dekker Old/New View、Allspaw second story、替换测试 James Reason / Just Culture、PagerDuty blame awareness 与 unspecified responder、无「谁造成事故」字段的模板、时间线 hindsight bias、双收费 bug 两次复盘实例、行动项只改系统；WebFetch 全文逐字）
- pmmilestone.com/encyclopedia/post-incident-review（时间线先用 logs/chat/pager 重建再讨论、行动项上限 5 vs 27、owner+due date 进日常 tracker、near miss 同等价值、场外主持、5 工作日内、"Repeat incidents are review failures"、读旧报告；WebFetch 全文逐字）
- blog.stackademic.com/your-incident-postmortem-process-is-probably-making-your-team-worse-heres-the-data-3092c9005ad2（交叉佐证：repeat incident rate >30% = 产出文档非学习、行业 35–50%、凭记忆重建时间线 / 根因停在症状 / 行动项无人认领四坏味道；WebSearch 结果全文）
- 判非：r706C 的 SRE/incident.io 七源（准入触发器 / 三分 / 动词门 / 四死法 / 三态关闭 / soak time）不重复；本节只补「组织级有效性度量 + 语言门 + 替换测试」三维。豆包自留地 WB 0 落地。


## 十、控制结构视角的复盘：CAST 把「事件链」换成「约束为何没被执行」（2026-11-11 r734B 实拉，五独立域交叉）

> 与 §七（准入触发器／贡献三分／动词门／四死法／三态关闭）、§八（复发率验收／反事实语言门／替换测试）分工：那两节是**流程与语言层**；本节是**因果模型层**——用什么结构解释事故，决定复盘能问出哪些问题。CAST/STAMP 在 §七「拒绝单一根因」之上给出可操作的结构载体。

- **r734B-1 ★复盘单位是控制结构，不是失效事件；安全是控制问题不是可靠性问题**：ScienceDirect《Learning from non-failure of Onagawa nuclear power station》(2020-12) 逐字 "STAMP consists of three principles: **safety constraints, hierarchical safety control structures, and process models**"；"accidents are viewed as **violations of system safety constraints and inadequate or ineffective control in enforcing safety constraints**"；"**There is no single root cause for accidents, and safety becomes a control problem where the goal of control is to enforce safety constraints**"；MIT Munekata 论文逐字 "STAMP **models safety as a control problem rather than the traditional view of safety as a reliability problem**"、"STAMP asks **why certain safety constraints were not enforced in the system**"、"It is much easier to blame the operators than to look at the confounding factors that may lead to human behaviors"。判据：① 复盘问题从「哪个组件／谁失效」改成「哪条约束、由谁负责执行、为何没执行」；② 停在找到 failure event 就写行动项，等于把症状当原因；③ 与 §7.2「贡献／缓解／风险三分」互补——三分是分类词汇，控制结构是因果骨架，两者要同时用。

- **r734B-2 ★CAST 九步里第 6 步是核心，且必须逐层上溯；它是分析方法不是调查技术**：MIT smadnick《Cyber Safety》(2014-07) 表 2.3 逐字 "Moving up the levels of the hierarchical safety control structure, establish how and why each successive higher level control **allowed or contributed to** the inadequate control at the current level"；引用 Leveson 原文 "**fully understanding the behavior at any level of the sociotechnical safety control structure requires understanding how and why the control at the next higher level allowed or contributed to the inadequate control at the current level**"，并明写 "This step is the core of CAST analysis ... **This is in contrast to Chain of Events Model where the focus is on a failure event and analysis stops once a failure event is identified**"；MIT dspace 118131 逐字给出第 6 步的二选一归因 "either the responsibility for enforcing it **was never assigned** to a component ... or a component ... **did not exercise adequate control**"，以及人的决策须按四类解释（当时可得信息／缺失信息、behavior-shaping mechanisms、value structures、process models 缺陷及其成因）；同篇 "**CAST is not designed to be a linear process**"（MIT smadnick 亦写 "these steps can be carried out in **any order**"）；Munekata 原文 "CAST is an **analysis method, not an investigation technique** ... used to help identify what questions should be asked and what system design recommendations can be implemented"。判据：① 复盘模板须列出控制结构各层的角色／职责／控制动作／反馈通道，缺反馈通道就没法解释「为何上层没发现」；② 行动项若只落在物理层（修那个坏部件），等于跳过了第 6 步；③ 九步可按任意顺序迭代，做成线性 checklist 会丢掉「上层允许」这个主要结论；④ 与 §8.2「反事实语言门」互补：语言门管措辞（防后见之明），第 6 步管归因方向（防停在人）。

- **r734B-3 ★时间维度独立成一步：控制结构随时间向高风险态迁移**：MIT smadnick 表 2.3 第 8 步逐字 "Determine the dynamics and changes in the system and the safety control structure ... and any **weakening of the safety control structure over time**"；"**Most accidents/incidents occur when a system migrates towards a higher risk state over time.** Understanding the dynamics of this migration towards less safe and secure environment will help with implementing appropriate countermeasures"；MIT dspace 122433 逐字 "CAST ... provides the ability to examine the entire sociotechnical system design to identify the weakness in the existing safety control structure and to identify changes that will not simply **eliminate symptoms but potentially all the causal factors, including the systemic ones**"；MIT Soma 矿难论文逐字 "the interactions in the system components and their changing nature during the course of the accident"、且在数据高度不确定／缺失时仍可给出预防建议。判据：① 复盘模板加一问「事故前 6–12 个月，哪些变更／降本／角色调整削弱了这条控制与反馈」，只重建事发当天时间线不算完成第 8 步；② 与 §8.1「复发率按 90d 窗口」互补——那条是组织级结果指标，本条是单次复盘必须重建的结构演化；③ 数据不全不等于不能复盘：约束执行链可从职责与反馈缺口推出（Soma 案例），但须显式标注证据强度，不得把推断写成事实。

**提升层**：工作流（复盘模板与归因结构）+ 可复用 Skill。触发词：CAST、STAMP、safety constraints、hierarchical safety control structure、process model、control loop feedback、chain of events、migration to high-risk state、上层允许、分析而非调查、九步非线性、约束未分配。

**判非（本轮独立机检，登记不落地）**：`CAST`／`STAMP` 经 **grep -w 词边界** 全库 SKILL.md **0 命中**（初始 7／10 命中全为 `broadcast`／`timestamp` 等子串噪声，已剔除）；`safety control structure`／`hierarchical control`／`chain of events`／`migration to a high-risk`／`an analysis method, not an investigation technique` 均 0 命中；`safety constraints` 1 命中位于豆包自留地 `wb-context-compressor`（语义为「给 SKILL.md 加 Safety Constraints 节」的工程约定），与事故因果模型无关，WB 按纪律 **0 落地**该文件；`sre.google` / `incident.io` 七源（r706C）与组织级学习度量四源（r717C）不重复立论，本节只补系统论因果模型这一层。

### 2026-11-11 r734B 增补来源（逐字核验，五独立域交叉）

- `web.mit.edu/smadnick/www/wp/2014-07.pdf`（MIT Sloan《Cyber Safety: A Systems Thinking and Systems Theory Approach》，**WebFetch 返回 application/pdf 二进制被丢弃**；改用 `curl` 200 取回 4,938,180B，Python 从 PDF stream 提取 282,723 字符，逐串命中 `nine step`×2、`hierarchical`×30、`migrat`×10、`Chain of Events`×1、`safety constraints`×12；WebSearch 快照取回表 2.3 九步原文与第 6 步 Leveson 引句）
- `www.sciencedirect.com/science/article/abs/pii/S2590123020300931`（2020-12《Learning from non-failure of Onagawa nuclear power station》；WebFetch 200 全文逐字：STAMP 三原则、violations of safety constraints、no single root cause、CAST 九步、"shift away from assigning blame"）
- `sunnyday.mit.edu/theses/Munekata-thesis.pdf`（MIT 学位论文《Safety in US Air Force Tandem Seat Pilot Training Applying STAMP Processes》；WebSearch 快照逐字："STAMP models safety as a control problem rather than ... reliability problem"、"CAST is ... an analysis method, not an investigation technique"、"control structures are drawn with information flowing to and from the control authority"、CAST 五步；`curl` 该 PDF **000 超时**，如实登记为快照取证）
- `dspace.mit.edu/bitstream/handle/1721.1/118131/1051211763-MIT.pdf`（MIT《Systems Theoretic Accident Analysis of an Offshore Supply Vessel Collision》§2.5；WebSearch 快照逐字九步 + 第 6 步二选一归因 + 人的决策四要素 + "CAST is not designed to be a linear process"）
- `dspace.mit.edu/bitstream/handle/1721.1/122433/1120721284-MIT.pdf` + `dspace.mit.edu/bitstream/handle/1721.1/126555/...`（MIT 铁路／Soma 矿难 CAST 案例；WebSearch 快照："The use of CAST does not lead to identifying single causal factors"、"not simply eliminate symptoms"、数据不确定下仍可给预防建议）· `qmro.qmul.ac.uk/.../Huang_Huayi_PhD_Final_111115.pdf` + `repository.lboro.ac.uk/.../16955600.pdf`（交叉佐证九步清单与 "steps can be carried out in any order"）

## 十一、复盘文化的有效性度量：完成的行动项、事前触发条件、以及会奖励沉默的指标（RI · r738C 2026-11-11 实拉，五独立域交叉）

§八给单篇复盘的语言门与行动项可验收动词，r717C 给复发率验收。本节处理另一层：**这一整套复盘机制本身有没有在起作用**。判断依据不在文档写得多完整，而在组织是否把结论变成改动，以及度量会不会反过来抑制上报。

- **（r738C-1）触发条件必须事前定义，否则"要不要写复盘"变成事后裁量**。Google SRE 官方五类触发：用户可见停机/降级超阈、任何数据丢失、on-call 介入（回滚/切流）、解决时长超阈、监控失效（通常意味着人工发现）；并明确 "It is important to define postmortem criteria before an incident occurs so that everyone knows when a postmortem is necessary."，且 "any stakeholder may request a postmortem for an event"。判据：① 阈值写进规则、事故前生效；② 触发是客观条件匹配，不是负责人判断"这次算不算严重"；③ 存在"任何人可提请"的旁路，否则边界事件会被静默降级（与下面 days-since 计数器同族）。与 §八「行动项可验收动词门」分工：那条管单条行动项怎么写，本条管整场复盘该不该开。
- **（r738C-2）有效性看行动项完成率，不看产出篇数；复发率与完成率是两个不同的量**。官方口径下 "A postmortem with no completed actions is a story."，Ben Treynor Sloss 引句 "To our users, a postmortem without subsequent action is indistinguishable from no postmortem."；行动项须 owner / priority / 真实日期 / 可外部验证的终态、并与功能需求进**同一个 backlog**（"file every action in the same tracker as other engineering work so it competes openly for time"），"improve" / "make better" 一类动词视为未写完。按 30/90 天跟踪关闭率；社区口径给出 85% 目标、并指出低完成率比不写更糟（制造改善幻觉）——该阈值为第三方立场、登记不作硬指标。判据：① 复盘质量报告至少并报"关闭率（30/90 天）"与"重复事件数"两栏；② 复发率是**结果**指标（同一事故是否再来），完成率是**过程**指标（结论是否兑现），只报前者会漏掉"改了但没改对"；③ 与 r717C 复发率验收分工明确，本条不重复立论。
- **（r738C-3）少即是好的计数器会奖励沉默；失效早信号要在文档里查得出来**。"days since last incident" 只有"时间过去且没申报"这一种改善方式，会导致边界事件被改叫"只是告警"、延迟申报、降级严重度、近失不记录；替代指标组：首次信号到申报时长、近失上报数、有书面复盘的事故占比、复盘行动完成率，且"近失上报数上升"应读作信任上升而非安全变差。官方与二手共同列出的失效早信号：行动项永不关闭、只复盘客户可见事件、时间线含糊、无人愿当主持、只有当事组读过、发布严重滞后、重复事件。领导行为侧：不因某人复盘频繁而污名（"A team with many reviews may simply be honest. A team with none may be hiding."）、未评审的复盘等于没写过。判据：① 任何"越低越好"的安全指标先问"它能不能通过不报来变好"；② 复盘篇数不得进个人绩效；③ 每季度抽查近 N 篇看七个信号，比统计总篇数有用。

**判非**：`second story` / 反事实语言门 / 替换测试 / 复发率验收已由 r717C 落地 §八，CAST/STAMP 由 r734B 落地 §十，本轮 **0 复用**，只补组织级有效性度量这一层。窄串 `30 and 90 days` / `same backlog` / `postmortem of postmortems` / `time from first signal` / `unreviewed postmortem` / `days since last` / `Wheel of Misfortune` 全库 0 命中；`85%` 10 命中经查为其他语境的泛数值，不与本轮立论冲突。

### 2026-11-11 r738C 增补来源（五独立域交叉，逐字核验）

- `sre.google/sre-book/postmortem-culture/`（Google SRE 官方第 15 章，**WebFetch fetch failed 如实登记**；由 `landing.google.com/sre/book/chapters/postmortem-culture.html` 官方镜像搜索快照逐字：primary goals / contributing root cause(s) / 五触发器 / "You can't 'fix' people, but you can fix systems and processes"）
- `landing.google.com/sre/workbook/chapters/postmortem-culture/`（Google SRE Workbook 第 10 章，搜索快照逐字：坏复盘失败模式 / 案例三年后同类事件 blast radius 缩小；WebFetch 同样 fetch failed，登记）
- `www.safeguard.sh/resources/blog/blameless-postmortem-template`（2026-10-18 一手 WebFetch 200 全文逐字：八字段模板含 What went well / Where we got lucky / Review questions / "A postmortem with no completed actions is a story." / "Report the completion rate to leadership."）
- `centerconsulting.com/code-library/concepts/blameless-postmortem`（2026-06-08 校验，一手 WebFetch 200 全文逐字：first story / second story / 航空医疗起源；仅用于判非，未落地）
- `www.safeguard.sh/resources/blog/why-a-days-since-last-incident-counter-backfires`（独立一手快照逐字：计数器反向激励 / 替代指标组）+ `www.safeguard.sh/resources/blog/reinforce-blameless-postmortem-culture-leaders-guide`（早信号 / 不污名化 / 未评审等于没写）+ `busfactor.tech/blog/blameless-postmortem-template`（Treynor Sloss 引句 / same backlog / verifiable end state / 30-90 天关闭率）+ `dev.to/senthil_kr/blameless-postmortems-a-leaders-guide-to-learning-from-incidents-10c0`（七个失效信号）+ `techblueprints.in/devops/monitoring/incident-management/postmortems`（85% / 30% 阈值，社区立场登记）

## 十二、把"决策质量"与"结果质量"分成两栏：结果偏差、决策时间线与无事故样本（RI · r742C 2026-11-14 实拉，四独立域交叉）

§八 r717C 立了反事实**语言门**（禁 could/should have、局域理性、替换测试），§十一 r738C 立了**组织级有效性度量**（完成率/复发率/计数器反激励）。本节处理一个更靠前的判据：**复盘在评价一个决策时，评价对象到底是不是那个决策**。若用结果给决策打分，前两节的机制再完备，结论仍会被运气改写。

### r742C-1 ★结果偏差是独立偏差，不是后见之明的另一种说法
Identec Solutions《Incident Analysis: Understanding Biases and Improving Investigations》（2026-07-20）逐字："**Outcome bias occurs when people judge a decision primarily by its result rather than by the information and reasoning available at the time.** This bias is especially problematic because **good decisions do not always produce good outcomes, and poor decisions do not always produce bad outcomes**. Randomness, uncertainty, and external factors can influence results."；两支海上维护队同样信息、同样风险评估流程，一队平安一队设备伤人，"Because investigators focus on the negative outcome, they may conclude that the second team's decision was flawed. However… the decision-making process itself may have been entirely reasonable."；官方结论逐字："**A robust incident analysis evaluates the quality of decisions independently of their outcomes.**"。Thinking Bugs 引 Baron & Hershey（1988, *JPSP*, "Outcome Bias in Decision Evaluation"）逐字："showed that **identical decisions were rated differently once people learned good versus bad outcomes**. Participants still cared about process information when it was available, but **outcome knowledge systematically shifted evaluations** — evidence that results leak into judgments of decision quality even when they should be held constant."；同一页明确分工："Hindsight makes the past feel more predictable. **Outcome bias uses the known result to grade whether the decision was competent.**"。
- 判据：① 复盘报告模板强制两栏——「决策质量（按决策时可得信息、备选方案、风险定级、假设披露评）」与「结果质量（实际影响、含运气）」，**结果不得自动回写前一栏**；② 用"结果翻转测试"自检：若同一决策换成好结果，我的评语会不会变？会变即结果偏差在起作用；③ 两本账（Thinking Bugs 逐字 "Two ledgers: **quality of choice, and new information from the result**"）——结果只作为"关于世界的新信息"入第二本账，用于更新规则，不用于评级；④ 高风险决策在结果到达**之前**写下理由与概率，否则事后无法重建过程（与 `ti-critical-reasoning` 的 belief audit 交接）。与 §八 r717C 分工：那条管**措辞 lint**（could/should have），本条管**评分对象分离**；与 §十一 r738C 分工：那条管整套机制有没有效，本条管单次决策怎么被评。

### r742C-2 ★三种偏差各需不同纠正动作，合谋会造出一条误导叙事
Identec 逐字把三种偏差并列：**Hindsight bias**（"view an event as having been more predictable after it has occurred"，纠正 "investigators should **reconstruct events chronologically and evaluate decisions using only information available before the incident occurred**"）、**Outcome bias**（纠正＝"evaluates the quality of decisions independently of their outcomes"）、**Fundamental attribution error**（"overemphasise personal characteristics or individual mistakes while **underestimating situational and organisational influences**"，纠正清单：Excessive workload / Inadequate staffing / Poorly designed procedures / Equipment limitations / Production pressures / Organizational norms）。同页逐字给出三者合流后的产物："Together, these biases create a **misleading narrative**: The hazard was obvious. The decision was poor. The individual caused the problem."；后果逐字"**retraining an employee may have little impact if the real issue involves procedural complexity, inadequate staffing, or flawed equipment design**"。Cybermaniacs 独立交叉逐字："Hindsight bias harms incident learning **in two ways**. First, it encourages blame… Second, it creates **shallow corrective action**."。
- 判据：① 复盘模板按三列分别记录「事前可知性」「结果是否影响评级」「是否只归到个人」，任一列为空即调查不完整；② 行动项若只有"再培训 / 提醒更小心 / 纪律处理"，触发 §7.3 动词门之外的**归因门**：回到工作量、编制、流程设计、设备、生产压力、组织规范六项找系统因；③ 时间线严格按"当时每人所知"重建（§八已有此纪律），本条补的是：**它只解决 hindsight，解决不了 outcome bias 与归因错误**，三者不可互相顶替。与 §十 r734B CAST 分工：CAST 分析控制结构为何没执行，本条约束调查者自身的认知偏差。

### r742C-3 ★技术时间线回答不了"系统为何有能力这样做"；没出事的样本也要复盘
Cybermaniacs（2026-10-26）逐字："A technical timeline answers questions such as: When did the agent begin the activity? Which identity or credential did it use? What tools did it call?… **They may not explain why the system was capable of doing it. That requires a decision timeline**: Why was the use case approved? Which assumptions supported the decision? Who believed the access was necessary? Why was a safeguard reduced? What compensating controls were expected? **Who accepted the remaining risk?** What evidence was available at the time? … When did the practical use move beyond the original approval?"；"A **bare approval** tells investigators that someone clicked a button. A **concise rationale** shows what they believed they were approving."；NIST AI RMF 逐字："calls for organizations to document system objectives, application scope, expected benefits and costs, human oversight, knowledge limits, and risks or impacts across the lifecycle"。决策环境重建清单逐字十一项：information available at the time / information that was missing / uncertainty understood / assumptions that appeared reasonable / competing priorities / time and commercial pressure / role and authority / previous experience / advice received from other teams / confidence in technical controls / perceived consequences of delaying the work。
- **无事故样本**：同页逐字"Organizations need to **assess decision quality separately from outcome quality**. A good decision should be evaluated according to whether the person: used appropriate information; surfaced important assumptions; considered affected people; followed applicable decision rights; sought relevant expertise; identified material uncertainty; applied proportionate controls; documented the rationale; **defined conditions for reassessment**."；"Agentic systems can strengthen this pattern because **many unsafe decisions will initially produce useful results**. Broad access may make the agent more effective. Reduced review may increase throughput… **The absence of immediate harm becomes evidence that the decision was good. This is how weak decisions gain legitimacy.**"。Thinking Bugs 独立交叉："**unexamined wins teach luck as skill**"、"reviews that **hide the final score until the process is graded**"、"In postmortems, **label luck explicitly** before you change the playbook"。
- 判据：① 复盘准入不得只挂负面结果（§7.1 触发条件之外补一条"成功但绕过了控制"的抽样复盘），否则"没出事"会持续给弱决策发通行证；② 每个具名批准留**理由**而非 boolean，`why are you doing this` 类问题作 cognitive forcing function（同页逐字 "interrupts automatic action long enough… to articulate the objective, assumptions, boundaries, and expected consequence"）；③ 决策记录须含"什么变化会触发重新评估"，否则批准时成立的假设在用途漂移后无人复核；④ 评"某次没出事的绕行是否可接受"时**先隐藏结果**评过程，再揭结果。与 §7.1 分工：那条管"要不要开复盘"（事前阈值），本条管"复盘调查哪条时间线、哪些样本该进池"。

### r742C 来源与判非（逐字核验，2026-11-14）
- `www.identecsolutions.com/news/incident-analysis-understanding-biases-and-improving-investigations`（2026-07-20, Mark Buzinkay，WebFetch 200 全文逐字：三偏差定义/两维护队案例/A robust incident analysis evaluates…/误导叙事三句/最佳实践七项）— 一手全文
- `cybermaniacs.com/cm-blog/the-incident-started-before-the-ai-agent-took-action`（2026-10-26，WebFetch 200 全文逐字：决策时间线 12 问 / bare approval vs concise rationale / NIST AI RMF / hindsight 两危害 / outcome bias 与 weak decisions gain legitimacy / 决策质量九项清单 / cognitive forcing function / 决策环境十一项）— 独立域一手全文
- `thinkingbugs.com/outcome-bias`（WebFetch 200 全文逐字：Baron & Hershey 1988 *JPSP* 同一决策不同评分 / hindsight 与 outcome 分工 / 两本账 / hide the final score / label luck / unexamined wins teach luck as skill）— 独立域交叉（含 doi 10.1037/0022-3514.54.4.569 原始出处）
- `biascodex.com/hindsight-bias`（WebSearch 快照逐字：decision journals / 区分 'signals we missed' 与 'noise that became signal only in retrospect' / Fischhoff 1975 与 Roese & Vohs 2012 文献）＋ `sciencewalk.blog/what-is-the-i-knew-it-all-along-phenomenon`（WebSearch 快照，decision journal 与 consider-the-opposite）— 两独立域背景交叉，立场登记
- **判非**：`outcome bias` / `fundamental attribution` / `Baron and Hershey` / `Hershey` / `decision timeline` / `decision rationale` / `bare approval` / `decision quality` / `two ledgers` / `reassessment` / `cognitive forcing` / `lucky win` / `label luck` 全库 SKILL.md **0 命中**；`hindsight bias` 2 命中＝本技能 §八 r717C 的**反事实语言门**（tinycto 引句）与 `meta/ti-critical-reasoning` 的 belief audit（记录预测是复盘输入），均为**语言/前置记录层**，本轮取的是**评价对象分离与决策时间线层**，明确分工不重述；`near miss` 1 命中＝r717C「near misses 同等价值」，本轮不重复该结论，只在"无事故样本"下另立"绕过控制但成功"这一不同命题。co-learn 台账 `outcome bias` / `decision timeline` **0 命中**，`hindsight bias` 6 命中经查均属 r717C 语言门语境。豆包自留地 WB 0 落地。
- **未采纳**：Baron & Hershey 实验的具体效应量与样本数（二手转述，不冒充原始论文直读）、HRM 绩效制度设计（超出 RI 复盘技能边界）、NIST AI RMF 完整框架（只取"记录目标与理由"这一条）。A/B 两轮结论一律不复用。


## 十三、让跨事故模式可见：severity 与 taxonomy 分工、起步标签 schema、标注自带证据等级（RI · r746C 2026-11-14 实拉，四独立域交叉）

> §8 用复发率验收单次复盘有没有产生学习，§11 管计数器会不会奖励沉默，§12 管决策与结果分栏。本轮补的是**复盘产物如何变成可检索、可聚合、可核验的组织资产**——单个复盘讲一个故事，五十份打了标签的复盘才说明该往哪投。

### r746C-1 ★ severity 管响应，taxonomy 管学习；只按严重度排序看到的是紧急度不是失效生物学
Incident Index《Incident Taxonomy and Tags: Reporting Without Gaming Metrics》逐字："Severity ... answers '**how urgent and how bad right now?**' A taxonomy answers '**what kind of failure was this, where did it live, and what do we want to learn across quarters?**'"；"Teams that only sort by severity see trends in **urgency, not in failure biology**."；"**Keep severity for response policy**: paging, comms cadence, post-mortem requirement. **Keep taxonomy for learning**: which services repeat, which dependency classes burn time, where detection lagged." 同一事故可 "SEV2 for response while tags capture 'database failover' and 'vendor API throttle' as facts for analytics"。季度汇总逐字 "top three failure modes, detection gaps, customer-affected hours, and remediation backlog health"，图表须 "sourced from the same canonical tags"。
- **判据**：复盘模板把两轴拆开——severity 只驱动响应动作与是否必须复盘；taxonomy（子系统/触发因 vs 贡献因素/失败模式/检测来源/客户可见与否/地域租户范围）驱动跨季度检索与投资。两者不可互相替代，更不可用 severity 当学习分类。与 §12 r742C-3「决策时间线」分工：那条重建单次决策的理由链，本条建立**跨事故可比的事实字段**。

### r746C-2 ★ 起步 schema 5–8 字段 + 四个反模式 + 季度把一条模式转成带 owner 的路线项
Safeguard《How should you tag past incidents so patterns become visible?》（Safeguard Security Team，Last reviewed 2026-10-19；转述 Google SRE Book 第 15 章「复盘完成评审后加入组织历史事故库」与 SRE Workbook「mature postmortem cultures often add **machine-readable tags** and other metadata for downstream analytics」）逐字："**One incident tells you a story. Fifty tagged incidents tell you where to invest.**" 起步八字段：detection source（自有监控/客户/合作方/研究者/审计）／cause class（访问控制/依赖/配置/构建发布/流程缺口/第三方）／affected area／severity／time to detect（分桶）／time to contain／action types（prevent/detect/mitigate）／status。设置六步：选单一可检索仓库→字段做**下拉**（"Free text produces twenty spellings of the same cause"）→回填过去一年→**标签进复盘关闭检查单**（"no postmortem is closed without them"）→每季度按 tag 计数看 top cause class 与最慢 detection source→"Turn one pattern into a roadmap item, with an owner"。四个反模式逐字：**Too many tags**（"Five to eight fields is plenty"）／**Tags as blame**（"Never tag a person. Tag the system and the control"）／**Counting incidents as a score**（"More incidents recorded can mean a healthier reporting culture, not a worse system"）／**One cause per incident**（"Allow multiple cause classes. Google's guidance speaks of contributing causes in the plural"）。近失也要打标，但用单独 severity/type 值以便与完整事故对比。Incident Index 独立补治理："**Assign owners for the taxonomy itself. When services are renamed, migrate tags or map old values explicitly**"、"Prefer **stable enums over clever synonyms**"、若领导只奖"更少事故"就会 "misclassify severity or avoid filing"。
- **判据**：① 标签字典是**受控枚举且有人负责**，服务改名必须迁移旧值或显式映射，否则跨期对比静默断裂；② 标签是复盘关闭门（缺标签不算关）而非事后补录；③ 季度聚合必须落到一个带 owner 的路线项，只出图表不算闭环；④ 禁用"事故数"当绩效（与 §11 r738C-3「奖励沉默的计数器」同向，本条给出**标签层的抗博弈设计**：tag 系统与控制、不 tag 人、允许多因）；⑤ 近失单独取值，别与完整事故混在同一桶。

### r746C-3 ★ 标注本身要带证据等级：已知 vs 潜在 + 原文锚点
AI Incident Database 官方 GMF taxonomy（Goals, Methods, Failures；maintainer Nikiforos Pittaras / contributor Sean McGregor，SafeAI 2023 workshop paper）逐字：它是 "a **failure cause analysis taxonomy** for AI systems in the real world, interrelating the goals of the system deployment, the system's methods, and likely technical causal factors"；设计动机之一是公开事故报告 "which may **lack details and technical information**"／"noisy, low-information documents"。结构为**三个互相关联本体**（AI System Goals／AI Methods and Technologies／AI failure causes），每条标注强制配三件："**Confidence modifiers (known and potential)**, corresponding to the degree of certainty of the annotator"／"**Text samples** from the incident report relevant to the assigned label, which **ground each the classification to supporting text data**"／"**Free comments**, where the annotator may provide their rationale, evidence, sources"。检索相似事故时会带出历史标注、示例文本片段与标注者理由，以弥补报告细节缺失。
- **判据**：任何标签都必须能回答"这是观察到的还是推断的"以及"报告里哪句话支撑它"。**没有原文锚点的标签不得进入跨事故统计**——否则聚合出来的是标注者的猜测分布，不是失效模式分布。三本体结构提示标签维应覆盖「目标／方法／失效因」而非只标后果。与 §10 r734B-3「数据不全须标证据强度、不得把推断写成事实」同构，本条把它落到**标签粒度并给出可机检字段**（confidence modifier + text sample）。与 §8 r717C「复发率按 failure_mode/is_recurrence 打标」分工：那条定义验收指标，本条定义**标签数据的可信度与可核验性**。

### r746C 来源与判非（逐字核验，2026-11-14）
- `safeguard.sh/resources/blog/tag-past-incidents-so-you-can-search-and-spot-patterns`（Safeguard Security Team，Last reviewed 2026-10-19；WebFetch 200 全文逐字；其引 Google SRE Book《Postmortem Culture》与 SRE Workbook《Postmortem Culture》属**二手转述**，如实登记，未冒充 Google 一手）— **第一独立域（厂商实践一手，含官方二手转录）**
- `incidentdatabase.ai/taxonomies/gmf`（Responsible AI Collaborative / AIID 官方 taxonomy 页；WebFetch 200 全文逐字；外链 SafeAI 2023 workshop paper CEUR Vol-3381/17.pdf）— **第二独立域（学术/官方分类法一手）**
- `incidentindex.com/guides/incident-taxonomy-tags-reporting`（Incident Index；WebFetch 200 全文逐字：severity vs taxonomy、useful dimensions、anti-patterns、rollups、governance）— **第三独立域（产品方指南，立场登记）**
- `hireunderstudy.ai/blog/incident-postmortem-knowledge-capture`（WebSearch 快照逐字：postmortem graveyard、tag everything、决策树提取进 runbook、双向链接、runbook 更新内建进复盘流程）＋ `incidentdatabase.ai/es/taxonomies/csetv0`（CSETv0 字段与分布快照）— **第四独立域交叉（产品博客/镜像，不作结论唯一来源）**
- **判重**：`machine-readable tags` / `detection source` / `cause class` / `tag as blame` / `five to eight` / `back fill` / `quarterly` / `confidence modifiers` / `GMF` 全库 SKILL.md **0 命中**；`taxonomy` 4 命中逐条核归属均**异命题**——`engineering/wb-agent-evaluation`（Microsoft KDD 2019 SRM 分类法）、`engineering/wb-subagent-delegation`（LLM 只能在固定 taxonomy 内选类别）、`defaults/wb-ponytail`（MCP 五层 taxonomy 触发词）、`engineering/wb-execute-discipline`（同族触发词）；`dropdown` 2 命中在 `wb-artifact-verification` / `wb-release-maintain`（界面控件与发布清单，非标签字典）⇒ 净新。A/B 两轮结论不复用；豆包自留地 WB **0 落地**。
- **未采纳**：CSETv0 具体伤害等级分布数字、GMF 各标签的 incident 计数、Incident Index 的 RCA 模板与产品导流、hireunderstudy 的自动打标产品能力——前者是时点统计，后者是工具绑定。
