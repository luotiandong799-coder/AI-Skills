# r818C 下沉全文｜RPO / RTO / MTTR：把「多久能恢复、丢多少数据」写成可验收目标（EI · 2026-11-28）

> 正文摘要见 SKILL.md §二十八。本文件存逐字一手摘录与判非。3 独点：①RPO/RTO/MTTR 三指标正交（目标 vs 事实）、RPO 是数据丢失时间窗不是备份频率、RTO 是业务可容忍停机的倒推；②RTO 四步计算（BIA 量化→最大可容忍停机→评估现有能力→设计架构）+ 分层 Tier；③四档恢复策略按 RTO 阶梯（backup/restore 小时~天→pilot light 小时→warm standby 分钟~小时→multi-site active-active 秒~分钟）与资源成本递增，RPO 越短备份压力越大。

## 一手来源（≥2 独立域）
- `https://aws.amazon.com/what-is/recovery-time-objective`（AWS 官方《What Is Recovery Time Objective (RTO)?》WebFetch 200 全文逐字：RTO/RPO/MTTR 定义与差异/如何计算 RTO 四步/四档灾难恢复策略 RTO 区间/AWS 服务映射）——第一独立域·厂商官方一手。
- `https://aws.amazon.com/what-is/data-recovery`（AWS 官方《什么是数据恢复?》WebFetch 200 全文逐字：RPO=备份最低保留期限/RTO=恢复过程最短时间/3-2-1 规则/灾难恢复手册步骤）——第二独立域·厂商官方一手（同厂不同条目，按来源族折叠为 AWS 族，独点靠逐字原文支撑）。
- `https://aws.amazon.com/what-is/disaster-recovery`（AWS 官方《什么是灾难恢复?》WebSearch 逐字：RTO=完成 DR 前经过的最长时间/RPO=可接受最长数据丢失时间/备份/每年测试 1–2 次）——第三独立域·厂商官方另一条目。
- `https://www.ibm.com/think/topics/recovery-time-objective`（IBM 官方 RTO 词条 WebSearch 检索作为跨厂商口径交叉，未取为全文一手，如实登记）。
- 诚信降级：`https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/disaster-recovery` WebFetch 返回 404 未采纳，未冒充一手；AWS 中文页（cn/tw）与英文页同族折叠按英文页逐字为准。

## 独点 1：RPO / RTO / MTTR 三指标正交——目标 vs 事实，数据丢失窗口 vs 停机时长
- RTO（AWS 逐字）：「Recovery time objective (RTO) is the maximum allowable time to restore a system after a disruption to make sure the least impact on business operations.」——中断后恢复系统的**最长允许时间**，是按「多久开始产生不可接受损失」倒推的目标，不是实测。
- RPO（AWS 逐字）：「The recovery point objective is the maximum amount of data loss you can tolerate, explained in a time period. ... if you define your RPO as one hour, then your organization is able to tolerate one hour of lost data changes in the event of a disaster.」——可容忍的**最大数据丢失量，以时间表示**，不是备份频率本身（虽然它约束备份频率）。
- MTTR（AWS 逐字）：「The mean time to recover is the actual total amount of time that it takes your business to recover from a system outage. ... Unlike RPO and RTO, MTTR is a factual time based on data, rather than a desired estimate or goal.」——MTTR 是**基于数据的事实时间**，RPO/RTO 是期望目标；「The mean time to recovery metric is often compared to the recovery time objective, as a discrepancy could represent work to be done」⇒ MTTR≫RTO 就是改进空间。
- 分层：RTO/RPO 按系统关键度不同——「A critical workload might have an extremely low RPO that approaches zero. A less important system that logs or archives non-audited information ... can safely have an RPO of days or more.」；「tiered system levels can be set for RTOs, depending on system criticality.」
- 权衡（AWS 逐字）：「While a zero-time RPO is ideal, the lower the RPO, the more organizational strain in the process of creating and updating backups. Determining RPOs is a balancing act between backup frequency and resource drain.」——零 RPO 理想但成本陡增，是把备份频率和资源消耗拉满。
- 与 EI 既有节分工：§10 超时取值/§12 deadline 传播管「请求级时间预算」、§20 错误预算管「成功率预算」；本章管**灾难级中断后的恢复目标与策略选择**——量级与决策对象不同，不互相替代。

## 独点 2：RTO 四步计算 + BIA 量化 + 分层 Tier
- AWS《How do you calculate RTO?》逐字四步：
  1. **Conduct business impact analysis**：识别并量化灾难与停机的潜在影响——revenue loss（销售额/暂停交易数/服务中断成本）、productivity impacts（员工无法访问系统的成本）、reputation damages（尤其网络安全事件后客户信心下降）、regulatory penalties（可通报事件未按时报告的罚款）；「Assign a monetary value to each of these categories and add them to a final figure for business impact.」
  2. **Determine maximum tolerable downtime**：「a critical system might need a much faster RTO than a little-used adjunct system ... define multiple RTO tiers based on how critical the system is」「A Tier 1 system would be your highest priority, requiring the shortest possible RTO, while a Tier 3 might not need fixing for upward of 24 hours.」
  3. **Assess current recovery capabilities**：「map out existing data backup systems, your business continuity plan, and any other strategies ... An initial investigation will help reveal whether your RTO figures are realistic.」——目标必须拿现有能力基线校验，否则是空目标。
  4. **Design recovery architectures to meet RTO targets**：加 failover mechanisms、redundancy、continuous monitoring、configuration management 来降 RTO。
- 反面：直接拍一个 RTO 数字而不做 BIA 和能力基线 = 目标不可验收；MTTR 事实与 RTO 目标的差才是待改进工作量。

## 独点 3：四档恢复策略按 RTO 阶梯 + 资源成本递增 + 3-2-1 备份
- AWS《disaster recovery strategies for different RTO requirements》逐字四档（RTO 区间为原文标注）：
  - **Backup and restore（RTO: hours to days）**：「running frequent backups ... revert to the backup data」最常见易实现；「you will have to define the RPO for mission-critical applications ahead of time. A low RPO could result in many incremental backups」。
  - **Pilot light（RTO: hours）**：「a small, scaled-down version of your core infrastructure that runs at minimum capacity ... scale up into a functional state at a moment's notice」核心库/系统在外部最小集常驻。
  - **Warm standby（RTO: minutes to hours）**：「hosts a near-clone of your active running environment. Engineers regularly push updates from the primary system to this clone ... can take over at a moment's notice」；「resource-intensive, so ... typically only used with critical systems」。
  - **Multi-site active-active（RTO: seconds to minutes）**：「a complete clone of your systems that runs in parallel ... continually data stream ... instantly replace any system」；「extremely resource-intensive and only used in a system that cannot, for any reason, experience more than a few minutes of downtime.」
- 成本/能力单调：RTO 越短 ⇒ 资源越重（backup/restore→pilot light→warm standby→active-active 依次升级），RPO 越短 ⇒ 备份/复制压力越大 ⇒ 两者都要和 BIA 算出的业务损失挂钩，不是越短越好。
- 3-2-1 备份规则（AWS《什么是数据恢复?》逐字）：「at least three data copies on at least two different storage types, with at least one copy offsite」；「一些组织还会选择维护完全离线备份，以防范网络相关风险」——勒索软件场景下离线副本是关键。
- DR 手册与演练（AWS《什么是灾难恢复?》逐字）：计划须含内外部沟通与角色、恢复时间表（RTO/RPO）、数据备份、「you must test your disaster recovery plan at least once or twice a year ... record and fix any gaps found in these tests」——不演练的 RTO 是未验证目标。

## 判非（写结论时禁止的表述）
- 禁「RPO 就是每多久备份一次」——RPO 是可容忍数据丢失的时间窗目标，备份频率是为满足它而设的手段。
- 禁把 MTTR 与 RTO 当同义词——一个是实测事实时间，一个是目标上限。
- 禁「RTO 越短越好/一律上 active-active」——须先 BIA 量化损失、按 Tier 分级、与资源成本平衡；非关键系统 Tier3 24 小时可接受。
- 禁「有备份=满足 RPO/RTO」——备份要能恢复（离线副本/异地/演练），且 RTO 还取决于恢复架构（failover/冗余），不只是备份。
- 禁把 AWS 四档 RTO 区间当成普适定额——是 AWS 口径下典型区间，实际以自身 BIA 与能力基线为准。
- 与 §10/§12/§20/§26 异命题（请求级时间预算、成功率预算、过载丢弃），不互相替代。
