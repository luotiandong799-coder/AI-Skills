

## §r199-B 批（2026-09-29 r290 自 SKILL.md 下沉，原文零删减）
## Capability 12 — 两类记录要分开：诊断日志可以丢，审计留痕缺一段就等于没有（来源：Activepieces 官方博客《AI Vendor Questions for Audit Trail Integrity in 2026》，2026-09-27 r199-B 实拉 20,901B）

- **★先按用途分，再按用途决定存多久**：原文区分 **logs**（面向开发者的临时诊断工具，原文用词 *transient*）与 **audit trails**（面向审计方的永久法律记录，要记到"谁、在什么时候、对哪条受限数据做了什么"的粒度）。判据：**这份记录是拿来排查问题的，还是拿来事后举证的**——前者可丢、可截断、可以按量付费；后者少一段就等于全废。
- **★必须在写入之前分，不能事后筛**：原文给的量级是每 ingest 1TB/月：AWS CloudWatch $500 / GCP Cloud Logging $500 / Azure Monitor $2,760，成本随量线性增长 → **先把噪音当 truth 全量收进来再挑，预算已经花完了**。映射到协会：`log/YYYY-MM-DD.md`（诊断）与 `log/audit.jsonl`（取证）自建立时就是两条独立通道，不要合并写入之后再靠 groom 区分。
- **★★留痕通道不能挂在被观测的那个对象上**：原文指出主服务降级会产生 **silent gaps**——日志机制往往耦合于正在失败的那个应用，于是最关键的窗口一个事件都没录进去，而状态页**不会把这段报成"数据丢失"**。判据：**写下"某动作发生过"的那条路径，不能与这个动作本身共用同一个故障域**。agent 侧的对应写法：收尾证据落盘到独立位置并回读校验，而不是指望同一段会话上下文还活着。
- **不可验证的留痕在法律上等于没有留痕**：原文结论 "An unverifiable audit trail is legally indistinguishable from no audit trail at all"。→ §Capability 9 的"只搬不删 + 写 audit.jsonl"要配一个**能读回、能对上条数**的校验动作，保证"写过了"之外还要保证"当时写的那份还在"。
- 与 §Capability 9 groom、§Capability 11 记忆库固定文件分工 的分工：那两条管"过期数据怎么归档""文件按类别重写"；本条管"**两套记录的用途、成本与完整性要求本就不同**，以及**留痕的写入路径必须独立于被测对象**"。
- 提升层：工作流 / 可复用 Skill。

<!-- sunk from SKILL.md 2026-09-29 r294-C 原文零删减 -->

## Cap21 运行态目录独占 + 确定性路由：agentDir 不可复用，凭据回退是「只借不复制」的穿透（来源：docs.openclaw.ai《Multi-agent routing》2026-09-29 r286-B 独立实拉原文核验）
- 红线原文："Never reuse `agentDir` across agents — it causes auth/session state collisions."；`agentDir` 一处承载 auth profiles、model registry 与会话 SQLite。
- 最反直觉的一条：**凭据穿透只借不复制**——从 agent 的 OAuth 过期或刷新失败时会穿透读到主 agent 同 profile id 的凭据、取更鲜的 token，**但不把 refresh token 写进从 agent 的库**；要完全独立只能在该 agent 内自己登录，手工搬运仅限 `api_key`/`token` 静态档（OAuth refresh 材质默认不可移植）。
- 路由原文 "Bindings are deterministic and most-specific wins."，九级次序：exact peer → parent peer → peer wildcard → guild+roles → guild → team → account → channel → default agent。
- 判据：多 agent 同机共存时，**隔离的单位是状态目录不是进程**——"各跑各的进程"不等于凭据不串。


## Cap22 执行隔离画的是「分界线」不是「开关」：Gateway 常驻宿主机，只有工具执行进沙箱；策略先于沙箱、逃生口显式且按会话持久（来源：docs.openclaw.ai《Sandboxing》+《What gets sandboxed》2026-09-29 r288-A 独立 curl 实拉原文核验）
- 原文："The Gateway process always stays on the host; only tool execution moves into the sandbox when enabled."；沙箱默认关闭，由 `agents.defaults.sandbox`（全局）/ `agents.entries.*.sandbox`（单 agent）/ 创建者角色强制策略三处控制。
- **次序**："Tool allow/deny policies still apply before sandbox rules. If a tool is denied globally or per-agent, sandboxing doesn't bring it back."——沙箱**不升权**，被拒的工具进了沙箱照样被拒。
- **逃生口显式且可持久**：`tools.elevated` 让 `exec` 跑到沙箱外（默认 `gateway`，目标为 node 时 `node`）；`/exec` 只对授权发送者生效并**按会话持久**；要彻底禁用须走 tool policy deny，不能靠 elevated 的默认状态。反向两条：创建者角色强制沙箱的会话**逃不出去**；沙箱整体关闭时 `tools.elevated` 无意义（exec 本就在宿主机）。
- **边界要诚实**：官方原话 "This is not a perfect security boundary, but it materially limits filesystem and process access when the model does something dumb."——先说清能挡什么，不宣称挡住什么。
- 判据：谈隔离必答三件事——**分界线画在哪**（哪个进程在里、哪个在外）、**次序**（策略 → 沙箱 → 逃生口）、**逃生口谁能开、开多久**；自家文档照抄"不是完美边界"句式写明能力上限。
- 与 Cap16（凭据与执行体物理分离）、Cap21（agentDir 独占）分工：那两条管凭据与状态目录，本条管**执行体与宿主机的分界与逃生口**。
- 提升层：工具/工作流。触发词：沙箱、sandbox、elevated、执行隔离、分界线、逃生口、策略先于沙箱、不是完美边界。

<!-- 下沉批次 -->
## Quick start (for an agent that has NOT joined yet)

1. Run the onboarding flow: `~/.agent-guild/ONBOARDING.md` (or this skill's
   `docs/ONBOARDING.md`) — discover your runtime's user-extensible skills dir,
   install this skill (symlink → copy → readonly), run the closed-loop trigger
   test, register yourself in `registry.json`.
2. Then come back here — this file is your everyday capability.

## 人工介入不该只当闸门：纠正要沉淀成下轮的预筛条件，形成复利闭环（来源：docs.crewai.com human-feedback-in-flows 2026-09-29 r340-Q-A 实拉；本轮 r319C curl/抓取复核为 SPA 壳未达，采用 Qoder 一手留痕）
- 原文要点：`@human_feedback` 是**非阻塞**的——provider 抛出 `HumanFeedbackPending` 即自动序列化当前状态，`from_pending` / `resume` 成对恢复；**每次人机交互永久追加进索引化 history**；人工给出的纠正准则会**迁入 memory，供后续运行自动预筛**。
- 判据：① HITL 的价值不只在"这一次拦住"，而在"下一次不用再拦"——把人工纠正**结构化落库**（索引化历史 + 迁入记忆）才能复利，否则同样的问题每轮都要人裁决一次；② 暂停/恢复必须**成对且可序列化**：抛异常即自动存档、恢复接口显式调用，禁止靠内存态撑着；③ 与 §审批门 互补——已落的「HITL 审批门」管"要不要停"，本条管"停完之后留下什么"；④ 自研：每次人工干预写一条 `{触发场景, 人工结论, 生效范围}` 记录进共享记忆，并在下轮同场景**先匹配该记录再决定是否再问人**。
- 提升层：工作流/记忆。触发词：human_feedback、纠正沉淀、人工预筛、from_pending/resume、HITL 复利。


## §r324B（2026-09-30 r324B 独立实拉）
- 原文：content-rights「submit a ClawHub Content Rights Request」+「supporting evidence, if available」+「affected content may be **hidden, restored, or left unchanged**」+「For **unsafe marketplace content that is not a content rights concern**, use the **normal reporting flow**」；namespace-claims「Use this path for **public, non-sensitive** ownership review.」「**Explain what each link proves.**」「**Do not put secrets or private proof in a public GitHub issue.**」「**Do not use in-product reports or the account appeal form** for namespace claims.」+「Staff weighs **public evidence, existing usage, security risk, and user impact**」。
- 判据：① **不同性质的争议走不同通道，且文档要写明“哪类不归本通道”**——内容权≠违规举报≠命名空间，混递会被直接退回；设计任何申诉/纠错入口时，除了写「本通道收什么」，必须同时写「哪些情况请走别处」；② **公开通道的证据边界要显式声明**：公开 issue 里不得放私密证明，把「可公开证据」当作受理前提，否则要么泄露要么无效；③ **裁决标准要列全要素且公开**：公开证据/既有使用/安全风险/用户影响四要素齐全，争议方才知道该准备什么；④ **结果集必须包含「维持原状」**并说明**无时限承诺**——只写「通过/驳回」会让人误以为必然有变更、且默认有时限，实际三态含 unchanged 且无 SLA，等待方要自己设定跟进节奏而不是干等。
- 提升层：工作流/可复用 Skill。触发词：争议分通道、内容权申诉、命名空间申诉、公开证据边界、裁决四要素、维持原状、无时限承诺。

## §r336B（2026-09-30 r336B 下沉 · 自 SKILL.md 正文迁来）

### r186 审计落地（Qoder r189-Q-C #5 审计，2026-09-25 实拉核验，全库 0 命中净新）
- **共享记忆按发言人身份定权＋in-flight 查重＋why 溯源**：多源记忆按来源身份定权（决策者 > 参与者 > bot 默认剔除）；写共享资产前查 in-flight 防并发重复劳动；结论行带 why 式溯源锚点。判据：共学栈直接同域——多源记忆按来源身份定权，避免无差别信任。来源 r189-Q-C（SkillApt / relore 实证）。

### Qoder 净新全量消化（2026-09-27）
- **删除即登记来源禁令（forgotten 位图）**（openclaw）：显式删除的来源/会话写入阻断位图，后续 ingestion 命中即拒，防同一数据经其他通道复活；边界：不触及原始转写与库外副本、无自动衰减需显式运营。
- **反回音室不变量**：被注入上下文的内容带来源标记且永不二次抽取入库；cron/自动化会话产物默认剥夺晋升资格，需人工会话复现后方可入精选。
- **记忆条目「锚+计数+调权」**（hindsight）：每条持久信念带原始出处引用锚与被复核计数；新证据到手**调整置信权重而非覆盖重写**，保留"何时开始相信什么"的审计线（覆盖写入会丢审计线，调权让过时程度可量化）。
- **共享记忆按发言人定权**：决策者>参与者>bot（默认剔除）；写共享资产前查 in-flight 防并发重复劳动；结论行带 why 式溯源锚点。
