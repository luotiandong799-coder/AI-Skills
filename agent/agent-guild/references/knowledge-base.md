

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
