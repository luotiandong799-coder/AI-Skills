---
name: ri-retrospective
description: 经验复盘与持续改进（Reflection Intelligence）。当任务完成或失败后需要沉淀经验、比较预期与实际、做根因分析、总结可复用规则时调用。提供 verification-discipline / handoff-protocol / engineering-economy 等方法论、无责复盘仪式、复盘准入触发器、行动项可验收动词门与三类关闭态，产出复盘报告。RI 可提议修改 Skills/提示词/规则/工作流，但未经授权不得直接改系统核心配置。
module: RI
modules: RI,EI
version: "1.1.0"
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

## 八、来源（2026-11-07 首拉 / 2026-11-08 r706C 增补）

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
