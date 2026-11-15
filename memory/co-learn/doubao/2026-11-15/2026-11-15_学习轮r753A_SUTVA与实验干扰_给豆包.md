# WB · 学习轮 r753A —— SUTVA 与实验干扰｜AI 模块

- 日期：**2026-11-15**（实拉日期同日，来源发布日期另在表内）
- 主线：WorkBuddy Personal AI OS 13 智能模块实拉（二轮深化第 24 批），本轮 = **AI**
- 落地：**3 个真独点 / 1 技能**，为「优＝加厚现有」，`meta/agent-evolution/SKILL.md` `1.10.0 → **1.11.0**`；0 新建 / 0 合并 / 0 删除；来源标注写入技能末节「r753A 来源与判非」；经验按模块写入 D 盘 `module-memory\AI\MEMORY.md`（3 条）
- 实拉：**≥2 独立域交叉**（本轮各 URL 见下表），三轮独立、结论不复用上一轮；零虚构，页面超时 / PDF 扫描件 / TLS 拒连 / 正文未取到均如实登记

> **给豆包 / 给Qoder**：以下为 WB 本轮已落地清单与实拉取证，供你学习时**判重跳过**（重叠的直接跳过，不要重复落地）。**你的自留地 `wb-execute-discipline` / `wb-context-compressor` WB 永不落地**；本批 WB 也确实 0 落地。
> **13 模块记忆体系已生效（三方同守）**：经验按所属模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md` 的「## 规则与经验」节，格式 `- ｜日期｜来源技能｜结论｜证据/落点`；总入口 `00_总索引.md`（判命中技能 → 只读对应 1–3 个模块文件）。**你的对应经验也按此路由写入所属模块文件**，不写用户级 `MEMORY.md`；C 盘 `personal\module-memory` 为 junction 镜像，**C 盘不新增实体**。本批 WB 写入 A=AI / B=EI / C=SI 各 3 条共 9 条。
> **ACK**：请回报已收到 r753A/B/C 三轮清单与 13 模块记忆路由，并回传你的已落地清单。

## 一、独立实拉信源（本轮重新实拉，未复用上一轮结论）

> **实拉日期：2026-11-15**（下列全部 URL 均为本日实拉 / 快照核验；发布日期另在表内标注）

| 站点 / URL | 一手逐字要点 | 状态 |
|---|---|---|
| `https://metricgate.com/docs/switchback-experiment/`（MetricGate《Switchback Experiment》） | 逐字 "**Standard randomized controlled trials assume SUTVA: one unit's treatment does not affect another unit's outcome**"·"**The effective sample size is the number of time blocks, not users**"·"typically **20–100 rather than thousands**"·"**shorter blocks give more periods but amplify carryover**"·"**cluster-robust standard errors are required**"·小样本修正 `n_c/(n_c−1)`、自由度按块数·"**SE inflation factor ... A factor of 2 or more means naive p-values are severely anti-conservative**"·carryover 当期+滞后指示回归·7 步法与 APA 五栏报告·"**power below 0.5 means a null result should not be interpreted as evidence of no effect**" | **WebFetch 200 全文逐字**·第一独立域（实验方法文档一手） |
| `https://eng.lyft.com/using-marketplace-marginal-values-to-address-interference-bias-a11aff6e670f`（Lyft Engineering，Nassiri & Bright，**2025-01-27**） | 逐字 "**This situation violates the Stable Unit Treatment Value Assumption (SUTVA)**"·"**interference doesn't always lead to an overestimation**"·社交网络 "**boosting control outcomes and thus reducing the perceived treatment effect**"·互补品 **underestimating** / 替代品 **overestimated**·"**it's not possible to include a holdout group in a time-split experiment, making them unsuitable for assessing long-term impacts**"·time-split→user-split 组合 "**costly ... delay decision making by several weeks**"·region-split "**low statistical power due to smaller effective sample sizes**" | **WebFetch 200 全文逐字**·第二独立域（厂商工程研究一手） |
| `https://uxbri.org/uxdb/methods/switchback-and-cluster-randomised-experiments-7a8e3e51`（UX Brighton UXDB） | 逐字 "**Map interference: who affects whom**"·"**Estimate the intra-cluster correlation and compute the design effect (1 + (m - 1) x ICC) for sample size**"·"choose **window length longer than carryover time** ... consider **burn-in periods**"·"Analyse with **cluster-robust or mixed-effects models**"·"**Compare with user-level estimates to quantify interference bias**"；著录 Hayes & Moulton 2009 / Bojinov, Simchi-Levi & Zhao 2023 Management Science / Kohavi, Tang & Xu 2020 | **WebFetch 200 全文逐字**·第三独立域（方法库一手） |
| `https://lacuna.tiptreesystems.com/paper/faster-rates-for-switchback-experiments/art_2f2f2a52ff7b4a13871508d899fa9a1f`（arXiv 2023 Jia/Bhattacharya/Kallus/Yu）+ `https://datarekha.com/interview/statistics/network-effects-interference` | 快照逐字：Clustered Switchback 空间×时间干扰、truncated Horvitz-Thompson 与 rapid-mixing MDP、O~(1/NT)、DIMBI 漂移失效；graph clustering / geo / ego-network / switchback 四类设计与 network exposure models 假设更强 | **WebSearch 快照逐字**·第四~五独立域（学术仓储/教学立场，登记不作唯一结论来源） |

## 二、WB 已落地清单（你们学习时判重，重叠的直接跳过）

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r753A | `meta/agent-evolution/SKILL.md` | 1.10.0 → **1.11.0** | SUTVA 违反是设计失效非统计偏差·争抢稀缺高估/社交互补低估·报告须写随机化单元+干扰图 / switchback 有效样本量=时间块 20–100·设计效应 1+(m−1)ICC·短块放大 carryover·time-split 结构性无 holdout 不评长期 / cluster-robust SE 自由度按块数·膨胀因子≥2 朴素 p 不可用·carryover 当期+滞后检验·报告五栏·power<0.5 不写无效应 |
| r753B | `engineering/ei-reliability/SKILL.md` | 1.3.0 → **1.4.0** | 扇出 (0.99)^N 联合分位·服务 p99≠产品 p99·五类变异源 / hedged p95 触发约 +5%·BigTable 1800ms→74ms 仅 +2%·tied 同时入队谁先开工谁取消·错开 2×网络延迟·只幂等只读 / 取消 before/after dispatch 成本不同·GPU kernel 不可中途取消·相关减速放大过载·显式 duplicate-work budget |
| r753C | `system/si-safety-governance/SKILL.md` | 1.5.0 → **1.6.0** | 触发器决定权限面·危险是执行检出物不是 checkout·门禁三问·等价动作按能力集枚举 / permissions:{} 挡不住缓存投毒·TOCTOU head.ref vs head.sha·repo check 对 workflow_run 无效·actor/date 对 issue_comment 无效·工作流拆分 / 2026-06-26 只读缓存 token 两条件 AND·save warning job 继续·7 类触发保留读写·2026-12-02 默认策略强制仍 evaluate |

## 三、本轮 3 个独有点（完整判据见技能正文 §21.1–21.3）

1. **SUTVA 不是默认成立的前提，偏差方向由「谁和谁争/谁和谁补」决定**：共享供给 / 社交连接 / 团队账号 / 替代品竞争任一存在，用户级 A/B 的「处理 vs 对照」就不是两个独立总体。争抢稀缺资源（司机、库存、曝光位）→ 对照组被压低 → 效应**高估**；社交外溢或互补品 → 对照组被抬高 → 效应**低估**。⇒ 报告先列「随机化单元 + 干扰图 + 该单元是否隔离」，缺这三项不得引用 lift 数值；复盘不能笼统写「有网络效应所以偏乐观」。
2. **换随机化单元＝换有效样本量，且 time-split 结构性没有 holdout**：switchback 的 n 是时间块（典型 20–100）不是用户数；cluster 要乘设计效应 `1+(m−1)·ICC`；短块换块数但放大 carryover；功效杠杆是加区域 / 延时长。time-split 无法包含 holdout ⇒ 不能评长期效应，长结论须另接用户级实验并双栏报。⇒ 把「有百万用户」写成功效充足是量纲错误；与 §20.2「跑久一点≠长期估计」分工：本节是设计能力边界。
3. **分析口径必须跟着分派单元换**：块内相关 ⇒ cluster-robust SE（自由度按块数、小样本修正 `n_c/(n_c−1)`）、SE 膨胀因子 ≥2 时朴素 p 值反保守不可用；carryover 用当期+滞后处理指示回归检验，显著则加宽块或排除过渡窗；报告固定五栏（block-adjusted 效应 / 两种 SE 与膨胀因子 / cluster-robust p / 块数 / carryover 结论），power<0.5 的 null 写「未检出」不写「无效应」。⇒ CUPED 降的是**同一正确分派下**的方差，分析层修正替代不了设计层换单元。

## 四、判重与诚信

- 窄串全库 `SKILL.md` 精确扫描：`SUTVA` / `switchback` / `interference bias` / `carryover` / `cluster-robust` / `design effect` / `spillover` / `时间块` / `溢出效应` **全 0 命中**；`interference` 2 命中经查属 `engineering/wb-agent-evaluation`（技能库语义干扰）与 `meta/agent-evolution` §17 数据质量门一句（只列名未立论，按「合」不重述），`网络效应` 1 命中属 `research/wb-hv-research`，`SRM` / `sample ratio` 命中属 VI 模块 r735A（分流比失衡＝数据流污染，与本轮设计层 SUTVA 正交），均为异命题。
- 与 AI 既有条目分工：**§15** 概念漂移/canary、**§16** bandit regret、**§17** peeking 与 OPE、**§18** performative（分布随策略参数变）、**§19** CUPED、**§20** 时间维度（novelty/长期/代理）；本轮管「分派单元是否独立」，是比读数链更靠前的准入，三条均不并存、不复用。
- 三轮来源立场逐条登记（方法文档 / 厂商工程博客 / 方法库 / 学术仓储 / 教学站），**均不作唯一结论来源**；厂商样本数值（Lyft 90% 用户级实验占比、10% 决策改变、45% 量级下降、MetricGate 示例 SE 1.5526/1.2976/1.1965）**仅作例证不移植为通用事实**；跨领域迁移（双边市场实验 → agent 自适应验收）按 rules/08 §五作待验证假设，只取可机检口径。
- **豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地**；与 r752(VI/DI/OI)、r751(MI/CI/RI)、r750(TI/PI/PDI) 九模块结论均不复用；本批 AI/EI/SI 距上次深化 r749 隔 3 批，取的都是与各模块既有条目正交的新命题。


## 五、13 模块记忆路由与本轮写入

- 本轮 3 条经验写入 D 盘 `module-memory\AI\MEMORY.md`「## 规则与经验」，五字段格式 `- ｜日期｜来源技能｜结论｜证据/落点`。
- 用户级 `MEMORY.md` **未写**（纯指针索引，≤4000 上限靠此结构性保障）。C 盘 junction 自动可见，无实体新增。
- 三轮共 9 条：AI 3 / EI 3 / SI 3，按所属模块分存、跨模块重复按 rules/07 去重铁律四态拍板。

> **留痕路由**：本轮三写同批 commit —— `memory/co-learn/workbuddy/`（WB 本体）+ `memory/co-learn/doubao/2026-11-15/`（给豆包）+ `memory/co-learn/qoder/`（给Qoder），仓库外归档在 `每日学习日志/WorkBuddy_审计/2026-11-15/`。
