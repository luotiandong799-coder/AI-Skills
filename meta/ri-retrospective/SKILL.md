---
name: ri-retrospective
description: 经验复盘与持续改进（Reflection Intelligence）。当任务完成或失败后需要沉淀经验、比较预期与实际、做根因分析、总结可复用规则时调用。提供 verification-discipline / handoff-protocol / engineering-economy 等方法论、无责复盘仪式、复盘准入触发器、行动项可验收动词门与三类关闭态、决策质量与结果质量分栏评分、决策时间线与结果偏差/归因偏差三列门，产出复盘报告。RI 可提议修改 Skills/提示词/规则/工作流，但未经授权不得直接改系统核心配置、复盘标签体系与跨事故模式聚合（severity 与 taxonomy 分工、受控枚举、已知/潜在与原文锚点）。关闭≠修复（implemented→verified 两阶段/原始 trigger 验证/三态结论与事前成功条件）。复盘会第二道门（准入/主持·记录·事故负责人三分离/发言权/时间盒议程与会前准备）；FRAM 功能共振分析（成功失败同源/近似调整·涌现·四原则·六方面六角·四步·两表现型 timing/precision·耦合聚合放大阻尼·管理可变性而非消除·WAD vs WAI·与 STAMP 分工）。AAR 事后回顾薄门（四问四步·follow-up 才产生改进·引导者只问开放题不下判·正式/非正式双轨·每次行动都过的薄门与事故深挖门并存）。单/双/三环学习深度分级（改动作/改假设策略/改学习机制本身·防御惯例与熟练无能阻断双环·反思-重构循环·学习与有效行为不等价须分层验收）。正常事故理论NAT与HRO对照（交互复杂×紧耦合·安全记录好≠高可靠·降耦合与提前预案）。 故障树FTA与事件树ETA（演绎找致祸组合vs归纳看触发后果·定性最小割集/单点失效/共因·量化=触发频率×条件概率乘积）。 FMEA/FMECA与RPN排序陷阱（模式清单≠优先级·RPN序数相乘伪精度与并列·AP表严重度主导·先分档后档内排序） HFACS人为因素分类（四层主动性失败vs潜伏条件·组织/监督/前提/不安全行为·19类·外部影响非层级·归因停在操作员=把症状当因）蝴蝶结bowtie（屏障有效/独立/可审计三门）。仍未证明栏（四块结构附没证明什么·可照做≠可审计·修正覆盖三分类）·三门有效/独立/可审计·近失改屏障状态·变更分析IS/IS-NOT）
module: RI
modules: RI,EI
version: "2.12.0"
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

## 十四、关闭 ≠ 修复：行动项有效性验证的两阶段、原始 trigger 与三态结论（RI · r751C 2026-11-15 实拉，四独立域交叉）

> 与 §7.4「三态关闭（已完成／显式降优先级／升级）」分工：那条管**动作状态**是否合法关闭，本条管**关闭之前有没有证明措施挡住了原失效**；与 §八 r717C「复发率是结果指标」、§十一 r738C「完成率是过程指标」分工：那两条定验收指标，本条定**单次行动项的关闭准入**。

### r751C-1 ★ 「关闭」是工作量声明，「已验证」是结果声明，两者必须是两条独立字段
qatronic《Postmortem Action Item Verification: Closed ≠ Fixed》逐字 "**a closed ticket is a claim about effort, and a verified fix is a claim about outcome**"；"All of this machinery answers one question well: **was the work done?** None of it, by itself, answers a different and more important question: **does the fix actually stop the specific failure that caused the incident from happening again?**"；四句对照表逐字 "The ticket is closed." ⇒ "**A change was made, reviewed, and deployed that is plausibly related to the action item's description**"，而 "It's been in production for months with no recurrence." 只确认 "**The exact triggering conditions have not recurred yet, or have recurred but did not reach the same severity by coincidence**"。devopsaitoolkit 逐字 "**'The ticket is closed' and 'the failure can no longer happen' are two entirely different claims**" / "**A remediation is a hypothesis** — 'this change will prevent the failure' — and a hypothesis that is never tested is just **an assumption wearing a completed checkbox**"。
- **判据**：① 行动项生命周期固定 **implemented → verified** 两段，禁止一步到 closed；关闭条件是「复现原始失效 → 观察到措施确实改变结果」，而非「代码合并／上线数月无复发／QA 签字／加了条测试」——后者各自只证明别的事。② 复盘模板增两栏：**工作量状态**（已实施/未实施）与**有效性状态**（已验证/未验证/不可验证带残留风险），任一空即不完整。③ 「无复发」是弱证据：可能是触发条件未再出现，也可能是复发了但没到同一严重度被巧合掩盖；观察窗须含足够多的**相关机会**（见 C-3）。

### r751C-2 ★ 验证必须打原始 trigger 而非症状；四类措施各有不同验证法，验证者≠实施者
devopsaitoolkit 逐字 "**Symptom cleared != trigger neutralized. Test the trigger.**" / "**Verification must exercise the ORIGINAL trigger**: reproduce the failure condition (fault injection / game day / staging replay) … **for alerts** -> deliberately create the condition; confirm it fires / **for runbooks** -> have someone unfamiliar execute it end to end / **for retries/failover** -> inject the fault; watch it actually recover"；"**assign verification to someone other than the implementer**, and require evidence … before the action item is allowed to close"；"**'Should' language** … with no test, game day, or observation cited to turn 'should' into 'does'" 是可机检的未验证信号。qatronic 分类表逐字：告警须 "**replayed against the original incident's metric time series** … at the right time, with enough lead time to matter"（阈值按当前基线校准会失效）；断路器须 "**exercised under the original failure's concurrency and latency profile, across every call site** that implements the same underlying retry or request pattern"；输入校验须重放 "**the exact payload (or a faithful equivalent, with sensitive data removed)**" 且验证相邻合法输入不被破坏。
- **判据**：① 症状消失 ≠ 触发中和；验收动作固定为「注入/重放**当时**的失效条件，看措施是否激活并挡住影响」，不是「看现在一切正常」。② 措施类型决定验证法（告警回放时序／断路器跨所有同构调用点注入原始并发延迟／校验重放原始 payload＋相邻合法输入／runbook 由不熟悉者端到端跑），不可用单一「加个测试」通吃。③ 验证者与实施者分离，证据（game-day 记录／测试结果／告警触发截图）须随关闭附档；「should prevent…」措辞命中即判未验证。④ 无法安全复现时**显式登记残留风险**，不得藏在绿勾后面。

### r751C-3 ★ 三态结论 + 事前成功条件 + 无机会窗口判 inconclusive
ones.com 逐字 "Keep three outcomes separate: **implemented** means the change was put into practice; **effective** means the evidence meets the agreed condition; **inconclusive** means the evidence is too limited or mixed for a fair decision."；"Define the **measure, target, counting method, baseline, and review window before work begins**"；"**A review window with no releases cannot tell you whether a release-handoff change worked**"；"**A convenient metric can improve while the postmortem problem remains**"（如交付变快不证明要求的评审发生了）；"**Record meaningful changes in team size, scope, workload, or tools that may affect interpretation**"；反模式逐字 "**Starting observation before agreeing on criteria** … makes it easier to **shift the success standard after results appear**" 与 "**Forcing a binary decision**"。
- **判据**：① 成功条件（度量／目标／计数法／基线／观察窗）必须**在实施前**写明，看结果后再改阈值即无效；证据须直接对应原失效而非「附近但无关」的指标改善。② 结论固定三态，**inconclusive 是一等合法终态**：证据不足或观察窗内没有相关机会时延期或改措施，不默认关闭；上下文变化（人员／范围／工作量／工具）须记录并说明对归因的影响。③ 关闭记录含「成功条件＋基线＋观察窗＋所审证据＋复发检查＋结论＋理由＋剩余工作 owner/复审点」，交给未参与该措施的人也能复述（与 §十三 r746C-3 标签原文锚点同构，但落到**结论粒度**）。④ 与 §7.2 过程动词门分工：那条管行动项写成「可完成的任务」，本条管「完成后按什么条件判它有效」。
**提升层**：复盘 / 验收协议。触发词：closed ≠ fixed、implemented → verified 两阶段、工作量声明 vs 结果声明、复现原始 trigger、symptom cleared != trigger neutralized、should 措辞门、验证者≠实施者、game day / fault injection / staging replay、implemented/effective/inconclusive 三态、事前成功条件、无机会窗口判 inconclusive、残留风险显式登记。

### r751C 来源与判非（逐字核验，2026-11-15）
- `https://qatronic.com/blog/postmortem-action-item-verification-closed-fixed`（QAtronic《Postmortem Action Item Verification: Why Closing the Ticket Is Not the Same as Fixing the Failure》，**2026-10-15**；**WebFetch 200，AI 摘要 60s 超时取前 15,000／64,446 字原文逐字**，如实登记：工作量 vs 结果两问、四句对照表、四类措施分类表、"a closed ticket is a claim about effort, and a verified fix is a claim about outcome"、独立复核与残留风险；其引 Google SRE Workbook／PagerDuty／Atlassian 均为**二手转述**，如实登记未冒充一手）— **第一独立域（厂商测试服务博客，商业立场登记）**。
- `https://devopsaitoolkit.com/blog/postmortem-remediation-without-verification`（DevOps AI Toolkit，James Joyner IV，2026-07-09，Last reviewed Jul 2026；**WebFetch 200 全文逐字**：两个不同声明／假设穿复选框／8 症状／7 根因／Diagnostic Workflow 代码块／IdP 变慢 game day 反例／7 条 Prevention Best Practices／Quick Reference）— **第二独立域（教学/工具站一手，商业立场登记）**。
- `https://ones.com/blog/best-practices-for-verifying-and-closing-corrective-actions-from-software-project-postmortems/`（ONES，**2026-10-31**，11 min；**WebFetch 200 全文逐字**：三态／事前成功条件五要素／实施与有效分离／无发布的观察窗／证据匹配原失败／6 反模式／验证质量 5 信号）与 `https://ones.com/blog/how-to-verify-whether-corrective-actions-from-a-project-postmortem-were-effective/`（同站姊妹篇，**WebSearch 快照逐字**：完成测试交给非 owner 复述／复发案例须重开决策／不可事后调阈值）— **第三独立域（产品方指南，立场登记）**。
- `https://risksight.com.au/blog/workplace-incident-management`（RiskSight；**WebSearch 快照逐字**：「An action is closed when the task is complete. **An investigation is closed when the risk has demonstrably changed**」／verification of effectiveness／控制层级）＋ `https://www.kepuchina.cn/...`（本轮 A 域，不作 C 结论来源）— **第四独立域交叉（行业安全实践，不作唯一结论来源）**。
- **判重**：全库 SKILL.md 精确扫描 `effectiveness verification` / `verification of effectiveness` / `reproduce the original` / `inconclusive` / `closed ticket` / `game day` / `fault injection` / `实施与有效` / `验证有效性` **全 0 命中**；`remediation` 3 命中逐条核归属——`meta/ri-retrospective` §十三 r746C「remediation backlog health」（跨季度聚合字段，异命题）、`engineering/wb-execute-discipline` 与 `engineering/wb-release-maintain`（**豆包自留地**，异命题）、`writing/wb-doc-writing`；`success condition` 1 命中为 `wb-artifact-verification` 定义完成口径、`复现` 27 命中为调试/验证通用词、`残留风险` 1 命中为发布门禁，均异命题登记不复用。`reproduction` 1 命中属实验可复现性。与本技能 §7.4／§八／§十一／§十二／§十三 结论不复用；豆包自留地 WB **0 落地**。
- **未采纳**：PagerDuty 15/30 天、Atlassian 4–8 周 SLO 等具体时限数字（各站二手转述且随组织变化）、QAtronic 的托管测试服务导流、ONES 产品字段配置、IdP 案例的 2 秒超时与线程池数值、游戏日排期与故障注入平台选型——属产品绑定与运维实现细节。

## 十五、复盘会是独立于文档的第二道门：准入、角色分离与发言权、时间盒议程（RI · r755C 2026-11-15 实拉，四独立域交叉）

> 与 §7.1 / §十一 r738C-1（**文档**准入触发器事前定义）、§八 r717C（**文档**反事实措辞 lint）、§十三（跨事故标签）、§十四（行动项有效性验证）分工：本条管**那一次同步会议本身**——要不要开、谁主持谁记录、谁有发言权、这一小时怎么分配。厂商与教学站立场逐条登记；两来源对「是否设专门行动项时段」结论相反，按 rules/08 §二保留冲突、不强行统一。

### r755C-1 ★ 文档写完不自动等于要开会；会议准入须单独定义且保留提请旁路
DevOps AI Toolkit《Running a Postmortem Review Meeting: Agenda and Facilitation》（James Joyner IV，**2026-07-13**）逐字「**Not every incident earns a synchronous review. A small, well-understood SEV-3 with an obvious fix can be handled in the doc and a quick async review. Reserve the meeting for incidents that were severe, surprising, or crossed team boundaries — the ones where people genuinely disagree about what happened or what to do. Meeting for every trivial incident trains people to tune out.**」；并逐字「**The document is the artifact; the review meeting is the learning.**」。incident.io 官方《A guide to post-mortem meetings》（**2023-10-11**）给自家做法：「we run a debrief meeting … **for every major or critical incident** … We also **occasionally run them for lower-severity incidents too, at the discretion of the incident lead or by request from anyone involved**」。incident.io guide《Incident reviews》补时点：「**often within a few days, and ideally while the incident is still fresh enough in people's minds**」；同站博客逐字「**Don't wait too long to have the debrief. It's better to have a scrappier post-mortem and to hold the debrief sooner than it is to polish the doc for ages and have forgotten what happened by the time you run it**」。
- **判据**：① 复盘制度要**两道独立门**——文档门（§7.1 事前触发清单）与会议门（严重度 / 意外度 / 跨团队边界 / 是否存在真实分歧）；「已产出复盘文档」不构成开会理由，反之「不写长文档」也不构成跳过会议的理由（scrappier doc + sooner debrief 是官方明确许可的形态）。② 会议门须留**任何干系人可提请**旁路（与 §7.1 同源），否则「要不要开」变成事后裁量、边界事故被静默降级。③ 每起小事都开会是**失效模式不是勤快**：官方明说会训练参与者把会议当噪声屏蔽；报「复盘覆盖率 100%」不得当作健康指标（与 §十一 r738C-3「越低越好的计数器奖励沉默」同向，本条给会议层的抗博弈口径）。④ 与 §十四 r751C 分工：那条管单次行动项关闭准入，本条管会议这一仪式本身的准入。

### r755C-2 ★ 主持 / 记录 / 事故负责人三者分离；参会规模是发言权变量不是信息量变量
incident.io 博客 ground rules 逐字「**Take notes**: … **Pro tip: the person running the meeting should not be the person taking notes. Their focus should be as a facilitator.**」；DevOps AI Toolkit 逐字「**Pick a neutral facilitator. Not the person who led the incident. They're too close; they'll re-litigate their own decisions. The facilitator runs the process; they don't need the answers.**」；incident.io guide 给三类候选并各自代价（文档作者「has the most context」/ 事故 lead「ability to replay what happened as they saw it」/ 完全中立的主持人池「It's important to ensure they have **time to prepare**」），统一要求「**comfortable walking through the incident, guiding the conversation, and helping to avoid the conversation getting stuck or too deep**」。**来源冲突如实登记**：guide 把事故 lead 列为合格候选，DevOps AI Toolkit 明确排除；incident.io 自家做法按严重度分档消解——「**For less severe incidents, it's common for the lead to write the postmortem and run the debrief. For bigger incidents, someone else, like a tech lead, will run the debrief. This frees up other key players to contribute to the conversation.**」⇒ 不强行统一，按「低严重度可兼任、大事故必须换人」采用。规模侧逐字「**The larger the "audience," the harder it is for participants to speak openly.** Reviewing what went wrong is challenging enough without feeling like you're **presenting to half the engineering team**」「**Recording the session and sharing is a great way to allow outside "read-only" participation**」「**Don't invite too many people … If it's valuable for people to "sit in," record it instead**」「if you invite all senior leaders, the environment will feel more like '**all the leaders are watching you explain yourself**'」。现场四个引导动作逐字：**Protect the quiet responder**（「The person who made the change under scrutiny will **go quiet or defensive**. Draw them out gently — **they hold the most context**」）、**Manage the loud room**（「Senior voices and executives can steamroll a retro … 'Let's hear from the on-call before we go to solutions'」）、**Redirect blame in real time**（「if Sam had just checked the dashboard」→「So the dashboard existed but **wasn't part of the on-call's normal flow — why not?**」）、**Timebox the rabbit holes**（「park it … keep moving」，incident.io 同向「we'll create a **follow-up** for someone to keep the session focused on learning」）。
- **判据**：① 会议检查表至少查**三分离**（主持 ≠ 记录 ≠ 事故负责人），大事故由中立者主持并把关键当事人释放为**发言者**；② 「只读旁听」走**录播 + 分享**，不靠扩邀请名单；参会人数上限按「能否坦率发言」定而非按「谁该知情」定；③ 沉默当事人**须被专门引出**——掌握最多上下文的人恰是最可能不说话的人，缺这一动作即会议取证不完整；④ 现场 blame 重定向是**口语动作**，与 §八 r717C 文档措辞 lint 同一原则的两个执行面，不可互相顶替；⑤ 离题讨论转 follow-up 而不是当场判完，且须具名。与 §十三 r746C「标签不 tag 人」分工：那条管跨事故数据结构，本条管会场发言权。

### r755C-3 ★ 会前准备决定会议是不是用来重建时间线；60 分钟按分歧密度分配，亮点刻意放末尾
DevOps AI Toolkit 逐字 prep 四条「**Assemble the timeline in advance.** Pull the incident channel, deploy log, and alerts into a chronological narrative **before the meeting. The review examines the timeline; it doesn't reconstruct it live.**」「**Circulate the draft 24 hours ahead.** Participants read the timeline and draft analysis *before* walking in. **The meeting is for discussion, not reading aloud.**」「**Invite the right people, not everyone** … Not a spectator gallery」「**Pick a neutral facilitator**」。定时议程逐分钟：`00:00 (2m)` 引导者定无责/学习框架 · `00:02 (8m)` 作者讲摘要与影响「**Clarifying questions only**」· `00:10 (15m)` 走时间线「Fill gaps, correct times, note surprises」· `00:25 (15m)` 根因/贡献因素 · `00:40 (10m)` 打磨行动项「owner, type, due date each」· `00:50 (5m)`「**What went well + where we got lucky**」· `00:55 (5m)`「Confirm owners, next steps, **who finalizes the doc**」。两条设计注记逐字：「**"what went well" comes near the end on purpose — by then the room has processed the failures and is ready to be honest about what saved them, rather than rushing past it**」「**the largest blocks are timeline and root cause, because that's where disagreement lives and where the learning happens**」。incident.io guide 独立交叉：「**The timeline should be updated with new information, comments and corrections as you go**」、走时间线时向**具体人发问**（「Sara – **how did you know that would work?**」→「We had an incident the week before ...」）、且「**there's no "root cause" section here, which is very intentional**」（与 §7.2 三分、§十 CAST 同源）；同页反向约束「**in reality a great incident review can bounce around between sections … We encourage leaning into the flow of the conversation rather than dogmatically following this structure**」。Common mistakes 逐字含「**No prep, so the hour is spent rebuilding the timeline**」「**Skipping the finalize step. Decide in the room who updates the doc and by when, or it stays a draft forever**」「**Ending with no named owners**」。incident.io 七步框架（WebSearch 快照）交叉：「**Step 2: Map it out** … Stick strictly to facts」「**Step 3: Focus on real-world impact**」「**Step 5: Extract actionable lessons** … the "**so what?**" test」「**Step 7: Finish strong … Celebrate what went well**」；nextretro 快照给 45–60 分钟、时间线会前 15 分钟异步写、detection/decision/recovery 三列。
- **判据**：① 没提前 24h 发 draft、没预装时间线 ⇒ 会议降级为集体回忆，判**不合格**（与 §八 r717C「时间线严格按当时每人所知重建」互补：那条定内容口径，本条定它必须在会前就存在）；② 时间按**分歧密度**分配（时间线 15m + 贡献因素 15m = 半小时 / 60 分钟），「where we got lucky」放末尾而非开场暖场——顺序是设计，不是礼节；③ 议程是引导工具不是硬脚本，允许回跳但要有人负责 timebox（与 incident.io 的「leaning into the flow」一致）；④ 结尾必须**点名谁定稿、何时定稿**，否则文档永远停在草稿（与 §7.4 三态关闭、§十四验证分工：那两条管行动项状态与有效性，本条管会议产出物的归属）；⑤ 走时间线时向具名人发问「你当时怎么知道这样做有效」，把局域理性挖出来，而不是只念一遍自动生成的事件表。
- **来源冲突登记**：incident.io guide 主张「**Let improvements surface naturally** … rather than setting aside time specifically for 'action items'」，DevOps AI Toolkit 的 60 分钟议程给了专门 10 分钟打磨行动项。两者立场不同，按 rules/08 §二**不强行统一**：只取可机检共识（owner / due date / 谁定稿必须在场确认），时段分配不作为定律。两站均强调 recency bias / soak time（本技能 §131 已落 r706C），**本轮不复用该结论**。
**提升层**：复盘仪式 / 会议设计 / 组织学习。触发词：会议是第二道门、Not every incident earns a synchronous review、severity/surprising/跨团队/真实分歧、任何干系人可提请、文档是 artifact 会议是 learning、主持≠记录≠事故负责人、neutral facilitator、re-litigate their own decisions、read-only participation 走录播、观众越大越不敢说、protect the quiet responder、redirect blame in real time、timebox rabbit holes、timeline 会前组装、draft 24 hours ahead、60 分钟定时议程、what went well 放末尾、who finalizes the doc、议程可回跳但要 timebox。

### r755C 来源与判非（2026-11-15 实拉，逐字核验）
- `https://devopsaitoolkit.com/blog/running-a-postmortem-review-meeting-agenda-and-facilitation`（DevOps AI Toolkit，James Joyner IV，**2026-07-13**，9 min；**WebFetch 200 全文逐字**：会议准入、prep 四条、60 分钟逐分钟议程、两条设计注记、六个 facilitation moves、Common mistakes 五条、文档 artifact vs 会议 learning）— **第一独立域（教学/工具站一手，商业立场登记）**。
- `https://www.incident.io/blog/a-guide-to-post-mortem-meetings`（incident.io 官方，**2023-10-11**，9 min；**WebFetch 200 全文逐字**：definition、blameless accountability note、三条 ground rules 含主持人不做记录、right people / agenda / 端到端 review / contributing factors / lessons / align on follow-ups、recency bias 与避免当场 commit、自家 debrief 频率与按严重度换主持人、Google Meet 录播、不过度纠正、行动项与严重度成比例、四条 responder tips、尽早开 debrief）— **第二独立域（厂商官方一手）**。
- `https://incident.io/guide/learn-and-improve/incident-reviews`（incident.io 官方指南；**WebFetch 200 全文逐字**：会后数日内趁新鲜、参会限于直接相关者、larger audience 抑制坦率、read-only participation 走录播、三类主持人候选与代价、facilitator 避免卡住或过深、summary level-set、走时间线向具名人发问并边走边更新、无 root cause 环节是刻意的、contributors/mitigators/risks 三分、行动项自然浮现与二阶效应、soak time）— **第三独立域（厂商官方指南，与博客同厂商不同文档，按独立信源计并登记同源）**。
- `https://www.incident.io/blog/a-seven-step-framework-for-running-incident-debriefs`（七步框架：ditch blame / map timeline 严格事实 / user-first impact / evaluate response / "so what?" test / owners+due dates 但 sleep on it / finish strong）+ `https://www.nextretro.io/blog/what-is-a-blameless-retrospective`（45–60 分钟、时间线会前 15 分钟异步写、detection/decision/recovery 三列、Prime Directive、语言纠正表）— **WebSearch 快照逐字，第四、五独立域交叉（教学/社区立场，不作结论唯一来源）**。
- **判重**：全库 SKILL.md 精确扫描 `24 hours ahead` / `circulate the draft` / `neutral facilitator` / `timed agenda` / `what went well` / `rabbit hole` / `quiet responder` / `read-only participation` / `会议引导` / `时间盒议程` **全 0 命中**；`soak time` 1 命中在本技能 §131（r706C 行动项沉淀时间，**异命题**，本轮明确不复用）；`root cause` / `contributing factors` 命中在 §7.2 / §十 CAST（三分与九步，按「合」登记不重述）。与本技能 §十三（标签体系）、§十四（关闭≠修复）、§八（反事实措辞）、§十一（完成率与计数器）分工明确、结论不复用；与 r755A(MI) / r755B(CI) 信源域与结论不复用；与 r754/r753/r752 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：60 分钟各段分钟数当通用定律（来源自陈是可粘贴到邀请的样例，且明确允许回跳）、Google Meet / 具体录播工具、SEV-3 等厂商分级编号、「sleep on it overnight」等具体时限、nextretro 的 sprint retro 与匿名卡片流程（团队复盘而非事故复盘）。
## r759C · FRAM 功能共振：复盘对象从「失效事件」换成「日常绩效可变性的耦合」（来源：Hollnagel《FRAM Handbook》2012，functionalresonance.com 官方四步全文 + MDPI Safety 2022《FRAM in an overtaking situation》全文 + ScienceDirect 系统综述/ScienceDirect 医疗 FRAM 交叉，2026-11-16 实拉）

> 与 §十三（标签体系）·§十四（关闭≠修复）·§八（反事实措辞）·§十一（完成率与计数器）·既有 r734B STAMP/CAST 分工：那些管「事故后怎么验收、怎么防偏差、控制结构如何失效」，本节管「为什么成功与失败同源、日常正常工作的可变性怎样耦合放大成事故」——**复盘本体论换视角**，不是根因分析的另一种画法。
- **成功与失败同源，是同一枚硬币的两面**：functionalresonance 官方逐字「the recognition, strongly supported by resilience engineering, that failures and successes have the same source, and that they metaphorically speaking are two sides of the same coin」；三阶段演进逐字「In the classical view, humans were seen as error prone or as fallible machines ... find the "human error" that either was the primary (or even "root") cause」→「1990s ... performance shaping factors ... could "force" people to fail」→「failures and successes have the same source」。FRAM 定义逐字「provides a way to describe outcomes using the idea of resonance arising from the variability of everyday performance」。**判据：复盘不能只分析出事的当天**——要分析日常正常工作（work-as-done）里那些也支持成功的调整； opponent 与既有 r706C「贡献/缓解/风险三分」呼应但不同：那是在一次事故内分因素，本条是本体论层「成功路径与失败路径共用同一套功能」，故 FRAM 强调 Safety-II（MDPI 摘要逐字 "the assumption [human error is main cause] is too simplistic ... potential side effects and adaptations in the socio-technical system"）。
- **六方面六角 + 四原则 + 四步的可执行骨架**：functionalresonance 官方四步逐字「① Identify and describe essential system functions, and characterise each function using the six basic characteristics (aspects) ... ② Check the completeness / consistency of the model ③ Characterise the potential variability of the functions ... as well as the possible actual variability ... in one or more instances ④ Define the functional resonance based on dependencies / couplings among functions ... ⑤ Identify ways to monitor the development of resonance either to dampen variability that may lead to unwanted outcomes or to amplify variability that may lead to wanted outcomes」（首步内含建模块、检查，合称通行四步：建模→变异性→耦合聚合→监控管理）。六方面逐字「input, output, control, resource, precondition, and time」，六角图「represented graphically by hexagons / snowflake」。MDPI Safety 2022 逐字四原则「equivalence of success and failures, approximate adjustments, emergence, and functional resonance」、两表现型「timing（too early/on time/too late/not at all）与 precision（precise/acceptable/imprecise）」、foreground vs background functions（前者分析中可大变的焦点功能，后者稳定作系统边界）。**判据：复盘记录若只写「谁没做什么」＝停在第一代错误观；FRAM 要求逐功能列六方面、标变异性表现型、再画耦合**。
- **聚合是放大/阻尼/维持三态，目标是管理可变性到可接受边界而非消灭它**：ScienceDirect 系统综述逐字「FRAM gets its name from the propagation of variability through a system which can result in ... functional resonance – or the point at which an expected level of 'noise' oscillates and becomes a 'signal' representing a non-specific accident cause」，第四步「identify solutions to maintain work operations within an acceptable boundary of safety and performance ... propose new ways of monitoring and/or dampening unwanted performance variability」。MDPI 逐字「upstream-downstream couplings ... an increase in variability (amplifying effect), a decrease in variability (damping effect) and to maintain variability (no effect)」「the last and fourth step ... manage or dampen variability to a level where no unwanted outcomes arise, **rather than eliminating variability since this is inevitable for things going well**」。Praetorius 论文逐字「it is neither possible nor meaningful to completely eliminate any type of variability」、用 11 个 CPC（Common Performance Conditions）按「stable or variable but adequate / inadequate / unpredictable」判变异性。**判据：FRAM 的改进项写「监测+阻尼」而非「消除差异」；把「规范化、统一做法」当万能解在这里是反模式**（与 §十一 复盘有效性看行动项完成率分工：那是验收，这是改什么）。
**提升层**：复盘方法论 / 系统事故模型 / 弹性工程。触发词：FRAM、functional resonance、Hollnagel、resilience engineering、Safety-I vs Safety-II、work-as-done vs work-as-imagined、failures and successes same source、four principles（equivalence/approximate adjustments/emergence/resonance）、six aspects（input/output/precondition/resource/control/time）、hexagon snowflake、four steps、variability phenotypes（timing/precision）、amplifying/damping/no-effect couplings、monitor and dampen not eliminate、CPC、foreground/background functions、与 STAMP 分工。

### r759C 来源与判非（2026-11-16 实拉，逐字核验）
- `https://functionalresonance.com/introduction-to-fram/`（**FRAM 官方网站，Hollnagel 方法授权页，WebFetch 200 全文逐字**：人类角色三阶段演进、failures and successes have the same source/two sides of same coin、FRAM 定义 resonance arising from variability of everyday performance、四步全文、六方面）— **第一独立域（方法官方一手）**。
- `https://www.mdpi.com/2313-576X/8/1/3/htm`（**MDPI《Safety》2022, 8(1), 3，Grabbe et al.，DOI 10.3390/safety8010003，WebFetch 200 全文逐字**：四原则、四步、六方面六角、foreground/background functions、两表现型 timing/precision 各水平、上游下游耦合 amplifying/damping/no effect、manage/dampen variability rather than eliminate、FRAM 用于功能分配、overtaking 场景）— **第二独立域（同行评议全文，`safety8010003`）**。
- `https://www.sciencedirect.com/science/article/abs/pii/S0925753518319672`（系统综述 1990–2018，WebFetch 快照逐字：四方法 HFACS/AcciMap/STAMP-CAST/FRAM 使用计数、`functional resonance` 定义 noise→signal、第四步 acceptable boundary、monitor/dampen unwanted variability）＋ `https://www.sciencedirect.com/science/article/abs/pii/S0925753522003332`（医疗 FRAM 实践反思，WebFetch 快照逐字：Resilience Engineering 四基石 monitor/respond/anticipate/learn、Safety-II、WAD、六方面、四步、model vs instantiation、Fragile 特性）＋ `https://functionalresonance.com/wp-content/uploads/2024/08/Praetorius-Lund-Lutzhoft-2011.pdf`（逐字：snowflake 六角、11 CPC 三档判据、Herald of Free Enterprise 案例、neither possible nor meaningful to eliminate variability）— **第三、四、五域交叉（系统综述/实践论文/案例，立场逐条登记，不作唯一来源）**。
- **判重**：全库 SKILL.md 精确扫描 `functional resonance` / `功能共振` / `Hollnagel` / `resonance` / `工作即想象` **全 0 命中**；`FRAM` 1 命中为 `FRAMEWORKS` 子串误抓、`可变性`/`variability` 命中逐条核为异命题——grill-me §74《Noise》的 `unwanted variability in judgments`（判断噪声）、wb-context-compressor §1766 LLM 可变性、ei-reliability §156 hedged requests 的 latency variability、agent-evolution §356 CUPED 的 metric variability、pdi-forecasting §159 分数差抽样波动，**全异命题**。与本技能 §十三/§十四/§八/§十一 及既有 r734B STAMP/CAST 分工明确、结论不复用（STAMP 管约束与控制结构，FRAM 管可变性耦合，二者互补不互相顶替）；与 r758(TI/PI/PDI)、r757(AI/EI/SI)、r756(DI/VI/OI) 九模块结论不复用；豆包自留地 WB 0 落地。
- **未采纳**：Herald of Free Enterprise / 超车 / 医疗具体案例结论（作方法示例不作普适规则）、11 CPC 完整清单当固定模板（按场景裁剪）、FMV 工具与可视化软件绑定、FRAM 与 AcciMap/STAMP 的优劣排序（学界无定论，只记适用面差异）、具体数值化半定量评分方案。HRO 高可靠性组织正念五原则（预期三类+反应两类·collective mindfulness·reluctance to simplify vs 线性事故模型·sensitivity to operations 工作漂移·deference to expertise 分级动态切换·resilience 四能力与检测缺口）。

## r763C · 高可靠性组织（HRO）正念五原则：复盘之外，还要有「事前/事中」的组织姿态（来源：Weick & Sutcliffe《Managing the Unexpected》2001/2007/2015，ScienceDirect《Scoping review of HRO implementation》S0925753523001200 全文逐字 + FTA TRACS 16-01 官方报告 PDF 逐字 + ScienceDirect《Assessing the HRO》S0925753520304793 + NZ 政府 Iroquois 审查报告交叉，2026-11-18 实拉）

> 与 §7.1（事前触发门槛）·§八（反事实/结果偏差）·§十一（完成率与计数器）·§十四（关闭≠修复）·§十五（复盘会）·r734B STAMP/CAST·r759C FRAM 分工：那些全是「**事故后**怎么分析/验收/防偏差」，r734B 管控制结构、r759C 管日常可变性耦合，本节管「**事故前与事故中**，组织靠什么持续避免灾难」——复盘是闭环的一半，HRO 是另一半（预测 + 反应两类姿态），不互相顶替。
- **五原则分「预期三类」与「反应两类」，由 collective mindfulness 支撑，且 HRO 按「失败必然发生」设计**：ScienceDirect scoping 逐字「The five behaviours that enhance organisational reliability are organised into two categories. Those that enable organisations to anticipate unexpected problems (i.e., preoccupation with failure, reluctance to simplify, and sensitivity to operations) and those related to capacity to react and manage unexpected problems when they arise (i.e., deference to expertise and commitment to resilience)」；「the application of these five principles together creates a culture of collective mindfulness, an organisational state precipitated by HRO behaviours where individuals share common goals to achieve reliability ... everyone focuses on the developments in the environment while attending work ... ultimately, minimises complacency」。FTA 官方逐字「An HRO is one that can repeatedly (thousands of times) operate high-risk processes without a catastrophic event despite significant hazards, time constraints, and complex technologies ... for an HRO, one major accident is too many; there is no acceptable number of catastrophic failures」；「HROs are designed around an assumption that failures will occur. In order to prevent a catastrophic failure, a system cannot be designed entirely around avoiding errors. Rather, the system must be designed around the assumption that sooner or later, errors will occur, and the system must be capable of coping with these errors and continuing to perform safely despite their occurrence」。**判据：可靠性姿态须分两栏审查——「预期」三原则看有没有把弱信号当问题查，「反应」两原则看出错时能否在最低层 contain 并把决策权交给最懂的人；只做事后复盘、没有事前姿态＝闭环缺一半**；设计前提写「失败会发生」而非「零失误」，与 §7.1「事前定义触发条件」同向但那管「何时复盘」，本条管「平时怎么运转」。
- **reluctance to simplify 直指线性事故模型；sensitivity to operations 抓 work-as-designed 与 work-as-performed 的漂移**：scoping 逐字「Linear accident theories have been criticised for simplification when applied to modern complex safety events, leading to a poor exploration of broad and deep causal factors (Leveson, 2004) ... linear models, such as Heinrich's Domino theory, can lead to a focus on human error or physical component failures as root causes, limiting the options of causality at the expense of more understated factors」；「Simplification '...obscures unwanted, unanticipated, unexplainable details and in doing so, increases the likelihood of unreliable performances'」；sensitivity 逐字「'...is about the work itself, about seeing what we are actually doing regardless of intentions, designs, plans' ... Unexpected events can eventuate during normal operations, and several weak indicators may precede events ... Equipping staff with the competence and motivation to detect these weak signals enables appropriate responses before minor problems escalate」。FTA 逐字「gathering the information necessary to understand how operations are actually functioning in practice, regardless of how they are supposed to be functioning on paper」。**判据：① 复盘若停在「人误/某部件失效」的单因线性叙事，正是 HRO 要纠的 simplification——须把组织与系统交互因素纳入因果面（与 r734B CAST「逐层上溯」同向，CAST 是事后分析法，本条是平时的认知纪律）；② 回路健康要看「实际怎么做」而非「设计怎么写」，漂移是弱信号，须有常态化渠道让一线把偏差说出来**（与 §八反事实措辞门分工：那条禁事后甩锅措辞，本条要求事前就看见 work-as-done）。
- **deference to expertise 是「平时层级、异常时下移、事后复位」的动态切换，不是一味扁平；resilience 须有检测与反弹的可验机制**：scoping 逐字「Most organisations operate a typical hierarchical structure which is appropriate for normal operating conditions. During an emergency or unexpected event, the most appropriate person for the situation will be delegated with the decision-making authority, regardless of rank or experience」；批评方逐字「'...bottom-up decentralized [decision making] can lead to major accidents in complex socio-technical systems' (Marais et al., 2004)」，而 HRO 的反驳是「under normal conditions, HROs employ a hierarchical structure with clear roles and responsibilities founded upon accountability of roles, redundancy in the event of failure, and procedural compliance ... HROs can deconstruct this hierarchy when the need arises (deference to expertise) and reform it efficiently upon return to normal operations (commitment to resilience)」；「Expertise means not only the person deferred but also the individual deferring」。**判据：权力下移要带触发条件与复位条件——只在异常态、交给当时最懂的人、事后回到常态层级；把「永远扁平/人人可改」当 HRO 是误读**（与 §十五「主持/记录/事故负责人分离」分工：那是会场角色，本条是运行态决策权）。resilience 面 scoping 逐字 Hollnagel 四能力「anticipate, respond to, learn from, and monitor unexpected events ... anticipation of the potential, responses to address the actual, learning to address the factual and monitoring to address the critical」，并如实登记缺口「methods to enhance an organisation's ability to 'detect' and 'bounce back' were not observed in the articles reviewed」⇒ **判据：「我们有韧性」不算证据，须给出可观测的检测信号与恢复时限，否则只是口号**（与 §十四「关闭≠修复、验证须打原始 trigger」同构：那条验单条修复，本条验组织反应能力）。
**提升层**：可靠性治理 / 事故预防姿态 / 复盘闭环的前半环。触发词：HRO、high reliability organization、Weick & Sutcliffe、collective mindfulness、preoccupation with failure、chronic unease、reluctance to simplify、linear accident theory、Heinrich domino、sensitivity to operations、weak signals、work-as-designed vs work-as-performed、deference to expertise、hierarchy deconstruct/reform、commitment to resilience、Hollnagel four constituents、anticipate vs react、one major accident is too many、Mindfulness Organizing Scale、与 STAMP/FRAM 分工。

### r763C 来源与判非（2026-11-18 实拉，逐字核验）
- `https://www.sciencedirect.com/science/article/pii/S0925753523001200`（**ScienceDirect《Scoping review of peer-reviewed empirical studies on implementing high reliability organisation theory》全文，WebFetch 200 逐字**：五行为两类、collective mindfulness 段、chronic unease=Reason 1997、reluctance to simplify 与 Leveson 2004 线性理论批判、sensitivity 弱信号与 work-as-done 引语、commitment to resilience 与 Hollnagel 四 constituents、deference to expertise 常态层级/异常下移/复位与 Marais 2004 批评、Mindfulness Organizing Scale 与实证应用缺口）— **第一独立域（同行评议综述全文）**。
- `https://www.transit.dot.gov/sites/fta.dot.gov/files/docs/regulations-and-guidance/safety/64011/building-toward-strong-safety-culture-tracs-16-01-final-report.pdf`（**美国联邦交通局 TRACS 16-01 官方报告，WebSearch 全文快照逐字**：HRO 定义「repeatedly thousands of times without catastrophic event」、one major accident is too many、五原则逐条、HRO 按失败必然发生设计、Weisbord 六因素）— **第二独立域（政府官方一手报告，PDF WebFetch 拒读按快照登记）**。
- `https://www.sciencedirect.com/science/article/abs/pii/S0925753520304793`（**《Assessing the HRO》WebSearch 逐字**：五实践逐条、pre-occupation/report weak signals、reluctance/sensitivity/commitment/deference 逐字、Mindfulness Audit 83 问 9 组、被误用为 checklist、三版书 6991 Google Scholar 引用）＋ `https://www.superscheme.govt.nz/...ANZAC-Day-Iroquois...PDF`（NZ 政府审查报告逐字：五原则、mindfulness 定义、Haddon Cave 七洞见含 hindsight bias 警告）— **第三、四域交叉（同行评议 + 政府审查，立场登记）**。
- **判重**：全库 SKILL.md 精确扫描 `preoccupation with failure` / `reluctance to simplify` / `deference to expertise` / `集体正念` / `collective mindfulness` / `高可靠性组织` **全 0 命中**；初筛 `高可靠`/`HRO` 的 20+ 命中经逐条核为 `reliability`（工程可靠性、`ei-reliability` 技能名、STAMP「safety as control not reliability」）等**异命题**，无一本体命中；与 §7.1/§八/§十一/§十四/§十五 及 r734B STAMP/CAST、r759C FRAM 结论不复用；与 r762(TI/PI/PDI)/r761(OI/EI/SI)/r760(AI/VI/DI) 九模块结论不复用；豆包自留地 WB 0 落地。
- **未采纳**：五原则具体问卷题项（83 问/MOS 9 问）当可直接套用模板、Heinrich/Leveson 完整理论对比、HRO vs Resilient Engineering 学派的优劣裁决（学界无定论，只记适用面）、航空/核电/医疗具体行业案例结论、Marais 2004 争端的唯一正确性裁定（只记「常态层级+异常下移」的操作含义）。

## r767C · AAR 事后回顾薄门（四问四步 · 引导者只问不判 · 正式/非正式双轨）

> 本节正文（三独点 + 四域一手来源 + 判重）已下沉 `references/r767C_AAR.md`，结论仍有效：每次行动都过的 15 分钟薄门、follow-up 才产生改进、主持人只问开放题不作评判、正式/非正式双轨并存；与 §十五事故深挖门分工不复用。

## EXT-S1 · 成绩记录必附「仍未证明」栏：改进落地≠效果验证（2026-11-22 外部共学，正文见 references/EXT-S1_仍未证明栏.md）
三独点速览：①每条改进记录四块结构末栏固定写「仍未解决的限制」，「方法已写进技能」≠「效果已验证」，缺口声明进行文结构而非收尾总声明；②证据四级分档（亲手运行/队内不可复核/推断/未验），承诺「方法可照做」不承诺「战绩可审计」，对他方状态断言须本回合实读否则标 unverified；③修正覆盖三分类：已更新／未变更（给理由）／不可核，不许沉默略过。
来源：GitHub `dabingfy-dot/solo-to-team-skills`（MIT，commit fedfd4e 2026-11-17，1091 stars）`skills/ops-case-notes` 正文直读+Orchivane Close the turn 节；全文 references/EXT-S1_仍未证明栏.md。2026-11-22 外部项目共学（EXT-S1），判重=全库「仍未证明」0 命中，判「增」。
## 事故复盘 AcciMap：六层因果映射，别把系统性因素压成一条线性根因链（r795E 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）

§FRAM/§STAMP/§HFACS 各管一种系统视角，本章补**跨层因果映射**：把事件从工作台一路挂到监管与政府层，防止「根因=操作员」式收口。

**独点1** 六层完备性：图中须显式出现 ≥6 层且每层 ≥1 因子；只有 staff/work 两层有节点判「未完成系统映射」。Wong 2025 逐字：AcciMap「generically formatted into six levels」，Step 4 用 ActorMap 找每层有安全责任的人与组织，Step 8 才按因果连箭头。

**独点2** 非线性闭环：箭头须同时含「高层决策→低层实践」与「低层信息→高层反馈」两类跨层边；全图单一无分叉路径即线性根因链。Goode 2016 逐字：高层决策 reflected in lower-level practices，低层信息 informs higher-level decisions；并点名 root cause seduction 这一陷阱。

**独点3** 方法选择而非排序：跨层因果与政策杠杆用 AcciMap、控制结构与约束失效用 STAMP/CAST、预定义失效分类与航空语境用 HFACS；报告须写选择理由，出现「A 优于 B」判违规（学界无定论）。六层命名在不同来源间不一致，按原文登记，不自造统一译名。

- **判重**：`AcciMap` 本体仅在 §r759C / §r790A「未采纳」中作为「不做方法优劣排序」的相邻短语出现，无独立专节；按 rules/07 判「增」。该两处未采纳项声明的是「学界无定论、不做优劣排序」，与本轮 AcciMap 六层映射专节不冲突，按「改了就删」不删有效声明。豆包自留地 WB 0 落地。
- **来源与诚信**：https://pmc.ncbi.nlm.nih.gov/articles/PMC11905254/?report=classic（Wong & Pawlicki，J Appl Clin Med Phys，2025，WebFetch 200 逐字：六层 / ActorMap Step 4 / Step 8 / root cause seduction）；https://pmc.ncbi.nlm.nih.gov/articles/PMC5179528/?report=classic（Goode 等，Front Psychol，2016，WebFetch 200 逐字：government→regulators→company→management→staff→work / 上下双向 / 图重建因）；https://sciencedirect.com/science/article/pii/S0950423019306552（Xing 等，J Loss Prev Process Ind，2020-03，WebFetch 逐字：六层枚举 / HFACS 受限于分类与航空域 / STAMP 控制结构）。Rasmussen 1997 与 Svedung & Rasmussen 2002 原文未获取；未在任何抓取来源找到「succession of layers」字面短语，未编造。 逐字全文与判非见 `references/r795E_AcciMap.md`。
## 公正文化 Just Culture：无责≠无问责，替换测试定可责边界（r796E 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）

§无责复盘仪式管「怎么开会让敢说」，本章管**追责边界在哪**——只喊 blameless 会把故意违规也一并放过，只罚人会压掉报告量。

**独点1** 替换测试 substitution test：判据——把当事人换成「同资质、同动机、同情境」的另一个人，若也会犯同样错 → 判 blameless（human error）；GAIN/Roadmap 逐字：「could a different person (well motivated, equally competent, and comparably qualified) have made the same error under similar circumstances」。只归因「健忘/疏忽/道德弱点」的 person approach 与 system approach 二分须写进结论（Reason 2000 逐字）。

**独点2** 公正文化两半都必须写：判据——鼓励甚至奖励报告安全信息，同时清晰划定可接受/不可接受行为界线；只有前半是误读。四分类：human error 不追责但需 corrective training、negligible/reckless（「conscious disregard of an obvious risk」）/willful 才追责。

**独点3** 报告激励链：判据——反制措施有效性取决于个人是否愿意报告错误，需要信任氛围（GAIN 逐字）；若复盘后报告量下降，判「问责边界设计失败」而非「员工素质问题」。与 §blameless postmortem 边界：无责=golden error 不罚，不推出「完全取消问责」——该边界无 SRE 一手直接支撑，按推断标注。

- **判重：`Just Culture`/`公正文化`/substitution test 在本体仅 r795E/§172 相邻短语，无专节；与 §无责复盘仪式、§r795E AcciMap 分工不复用。豆包自留地 WB 0 落地。**
- **来源与诚信**：https://www.bmj.com/content/320/7237/768.full（James Reason，BMJ 320:768，2000-03-18，WebFetch 200 逐字：person approach vs system approach/unsafe acts 源于个体心理异常）; https://www.coloradofirecamp.com/just-culture/definitions-principles.htm（GAIN Working Group E《Roadmap to a Just Culture》2004-09 官方报告 HTML 转载，WebFetch 200 逐字：信任+奖励报告且划清行为界线/substitution test 原文/reckless 定义/报告意愿决定反制有效性）。traficom.fi 官方 PDF 非文本、skybrary.aero Cloudflare、sre.google postmortems fetch failed；blameless 边界仅推断已标注。 逐字全文与判非见 `references/r796E_公正文化.md`。

## r800A · 变更分析（Change Analysis）：出问题先问「这次有什么不同」，把基线当作找因的锚（RI · 2026-11-23 实拉，≥3 独立域一手交叉，3 独点）

**这一节管什么**：已有 FTA/HFACS/AcciMap/蝴蝶结都在回答「这张因果图上哪里断了」；变更分析补的是**因果图之前的一步**——原本稳定的系统突然出问题，先锁定「上一次正常」与「这一次异常」之间的**差异集合**，只在差异里找因，避免把整系统重扫一遍或把同时发生当成因果。

### 三独点
1. **「曾正常→现失效」才适用，核心是拿基线比差异而非从零分析**：TrustEd 逐字「Change analysis is a hazard analysis technique that compares a *baseline* (a known, accepted, previously analyzed or accident-free condition) with a *new or proposed* condition, identifies every difference between the two, and then evaluates each difference for its potential to create new hazards or defeat existing controls」+「if the baseline was safe and the new situation is not, the cause must lie in what is different. Rather than re-analyzing an entire system from scratch, change analysis focuses attention on the deltas」。Umbrex 逐字「if a system, process, or business activity used to perform acceptably and now does not, something changed」+「It does not ask, "What could possibly be wrong?" It asks, "What is different here, and could that difference explain the result?"」。**判据**：复盘开场先判适用性——「有没有一个可信的 as-was 基线」；无基线（首次运行/从未正常过）则本方法不适用，转 FTA/AcciMap。与 §r791C 蝴蝶结、§r779C FTA 分工：那些管已知顶事件后的屏障/组合，本条管**因从哪里找**。
2. **IS/IS-NOT 矩阵把「问题不存在的地方」当等值证据，非差异不可能是因**：GitHub KT Workflow（源自 Kepner & Tregoe《The Rational Manager》1965）逐字「The IS NOT column is equally important as IS — it defines the boundary of the problem」+ 四维度 What/Where/When/Extent 各追问「what is different between IS and IS NOT」+「Non-distinctions (things that are the same in both IS and IS NOT columns) cannot be causes」；KT 官网逐字从「新大豆油导致产量降 22%」推进到机制：「We asked, 'What about the soy oil aids in the growth of organisms?' The answer was proteins」→ 查新旧油蛋白含量、得新油低 20%+ 才把供应商变更坐实为因，并明确「Correlation is not causation… What's missing is the mechanism of the cause」+ 反证句「I've used this same appliance at the same time of day every day for over two years without causing a blackout」。**判据**：IS 与 IS-NOT 两栏同列，任一维度只写 IS 视为矩阵不完整；候选因必须同时「解释全部 IS」且「不违反任何 IS-NOT」，缺机制（只有时间相关）不得列为因。与 §r742C 决策时间线分工：那条防评价者偏差，本条防**从相关直接跳到因**。
3. **临时变更与渐进漂移最易漏，替换件须「规格相同」才算非变更**：TrustEd 逐字分类「planned vs. unplanned, permanent vs. temporary, intentional vs. unintentional and gradual (creeping) vs. sudden」+「temporary changes and gradual drift still require analysis. Many major incidents (Flixborough is the classic example) resulted from temporary modifications that were never formally evaluated」；六类变更逐字 People / Equipment and tools / Materials / Procedures and methods / Environment / Organization and management。replacement in kind 逐字「Replacing a component with an identical item that meets the original design specification is *not* a change… Anything that deviates from the design specification (different material, rating, size, manufacturer with different characteristics, a software version with changed logic) is a change and must be analyzed」+「Do not be fooled by phrases such as 'similar' or 'equivalent' – only identical-to-specification counts as in kind」。事后用法逐字「investigators ask 'what was different this time?'」并强调「Be exhaustive; small or indirect differences are frequently the significant ones」；与 MORT 配对逐字「two techniques are central to MORT investigations… change analysis and barrier analysis」。**判据**：变更清单显式含「临时/渐进」两栏，疑似「等价替换」须逐项核对规格（材料/等级/尺寸/厂商特性/软件逻辑），有一项不同即当变更进分析；事后把显著差异喂给 barrier/root-cause 而非停在差异列表。

### 来源与诚信
- `https://trustedinstitute.com/concept/bcsp-asp/safety-programs-and-concepts/change-analysis`（TrustEd Institute CSP/ASP 官方培训页，WebFetch 200 全文逐字：定义/baseline-vs-new/MORT+KT 谱系/六类变更/四组分类/七步流程/replacement in kind/Flixborough/事后 what was different this time）——第一独立域·官方培训一手。
- `https://www.kepner-tregoe.com/blog/enhanced-troubleshooting-correlation-is-not-causation/`（Kepner-Tregoe 官方博客，WebSearch 逐字：NYC blackout 反证句/新大豆油案例蛋白机制/correlation is not causation 缺机制）——第二独立域·方法创始机构一手。
- `https://github.com/DorShaer/Husk/blob/main/libs/lifeos/skills/RootCauseAnalysis/Workflows/KepnerTregoe.md`（KT Workflow 技能文档，WebSearch 逐字：IS/IS-NOT 四维度矩阵/非差异不可能是因/last known good→first observed bad 窗口/候选因解释全部 IS 不违反 IS-NOT）——第三独立域·方法实现一手。
- `https://umbrex.com/?p=342045`（Umbrex 咨询方法论页，WebSearch 逐字：曾正常现失效即 something changed/比较型证据型而非头脑风暴/五类变化维度）——第四域交叉，立场登记。
- **判非**：全库 SKILL.md 与 module-memory 对 `变更分析`/`change analysis` 0 专节；`IS/IS-NOT` 曾在 r742C 决策时间线语境相邻出现但异命题（那条防评价偏差，本条找因）。豆包自留地 WB 0 落地。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。



## r804A · Tripod Beta 事故树：不停在「人误」，沿事件—屏障—人因—组织四段重建（RI · 2026-11-25 实拉，≥3 独立域一手交叉，3 独点）

### 三独点
- **树是 AND 门串联的 Trio，不是单因链**：Trio 三要素 = 事件（状态变化及其后果）/ 对象（被改变的人或物）/ 变更代理（造成变化的驱动，如「火」作用于「人」→「被烧伤的人」）；两个事件组合成一个结果，结果又成为下一 Trio 的事件/代理，通常 2–5 个 Trio 互联成树；调查从「最后一个正常事件」逆向起手，其后发生的一切才反常。潜在事件（屏障挡住而未实现）也要建模，不能只画已发生的路径｜IEC 62740:2015 C.12 官方标准正文（融合 Reason 瑞士奶酪 + Rasmussen GEMS + Wagenaar Tripod 因果路径，树状因果网络）+ wikii.one Tripod_Beta 译本逐字（Trio 定义/AND 门/从 last normal event 起手）。
- **先问屏障存在/可用/有效/被正确使用，再追人因**：每个关键事件问「本应有哪些预防/检测/控制/减缓屏障」，屏障状态分有效/失效/缺失（IEC 标准分三态；EHS-SIL 补「被绕过」）；联锁被旁路不能停在「操作员旁路」，须再查旁路授权、报警管理、维护积压、生产计划、风险评估与监督机制——屏障失效只是直接原因，不是结论｜Icologiq 术语表（Tripod Foundation 维护、Energy Institute 出版官方用户指南，Version 6/2023，六步流程：重建事件序列→识别屏障→直接原因→绩效影响因素→组织根因→纠正措施）× IEC 62740 标准 × EHS-SIL 实战指南三域交叉。
- **三层因果 + 培训不是万能措施**：直接原因（紧邻事件的行为/状态）→ 前提条件（使直接原因更易出现的设备/任务/环境/人员条件，即绩效影响因素）→ 潜在原因（设计/维护/程序/培训/沟通/组织管理决策）；措施优先恢复强化关键屏障、消除共同失效原因，培训只能是措施之一，不能替代工程/设计/管理系统改进；与 §r791C 蝴蝶结（屏障路径图不追组织根因）、§r787C HFACS（四层人因分类）、§r734B CAST/STAMP（控制结构）、§r779C FTA/ETA（布尔路径）分工——本条补「事件—屏障—人因—组织」四段式树与屏障三态｜IEC 62740:2015 原文 + EHS-SIL《Tripod Beta 事故调查怎么做》+ Icologiq 三源逐字。

### 来源与诚信
- `https://ima.qq.com/wiki/?shareId=...mediaId=pdf_5d86d214...`（IEC 62740:2015 / BS EN 62740:2015 标准 C.12 Tripod Beta 节，WebSearch 逐字：融合 Reason/GEMS/Wagenaar 三理论 / 对象-变更代理 / 屏障三态 / 树状因果网络 / 流程 a-b-c）——第一独立域·标准原文（经标准库镜像取正文，页面为标准节选非全本，如实登记）。
- `https://www.icologiq.com/glossary/tripod-beta`（Icologiq 术语表，WebFetch 抓全文失败取 WebSearch 逐字：Version 6/2023、Tripod Foundation 维护 + Energy Institute 官方用户指南、三阶段与六步流程、基本风险因素 BRF）——第二独立域·官方方法维护链交叉（厂商词条立场登记）。
- `https://ehs-sil.com/articles/tripod-beta-incident-investigation-guide.html` + `https://wikii.one/Tripod_Beta`（EHS-SIL 实践指南与 wikii 译本，WebSearch 逐字：三层因果/屏障状态四分/联锁旁路追组织/Trio 三要素/AND 门/从最后正常事件倒推）——第三、四域交叉（wikii 为译本非独立一手，仅作定义互证）。
- **判非**：全库 SKILL.md / module-memory 对 `Tripod Beta`/`三脚架` 0 专节（`bowtie` 蝴蝶结在 §r791C 是屏障路径图不同方法；HFACS/CAST/STAMP/FTA 各管一段异命题）；与豆包自留地无关。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。
