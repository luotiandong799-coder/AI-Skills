---
name: wb-debug-loop
description: >-
  有纪律的排障循环（诊断 bug / 报错 / 性能回归的根因）。当出现报错、崩溃、白屏、500、超时、测试失败、行为与预期不符、构建/部署跑不起来、性能变慢、内存泄漏、复现不了的怪问题时应用：重现 → 最小化 → 假设 → 验证 → 修复 → 回归测试。禁止"先改再猜"、禁止一次改多处、禁止靠重启/清缓存糊过去。另含「修复验证」：补丁是待验证假设，不从 diff 大小/作者/上游一致/原 PoC 失效推成功，须测同根因变体与兄弟路径。触发词：报错、错误、异常、崩溃、闪退、白屏、跑不起来、不生效、没反应、失败、失败原因、找不到原因、查不出、定位、排查、排障、根因、复现、回归、性能变慢、卡顿、内存泄漏、超时、内存溢出、debug、troubleshooting、root cause、stack trace、崩溃日志、模型行为、幻觉、选型、补丁、修复验证、patch、变体、这算 bug 吗、加固算修复吗、兜底不是修复、重试掩盖、静默降级、缓解不是修复、改指令算修了吗、装了不生效、静默失败、幻影字段、声明但未写入。不适用：只是"该不该写这段代码"的取舍（走 wb-ponytail）、多步实现任务的规划与交付（走 wb-spec-driven）、任务级"点名目标全量覆盖 / 失败换路攻坚"纪律（走 wb-execute-discipline）。、一直在重复、转圈、卡死检测、迭代上限定多少、并行单元重名、工具结果用错、喂给判定的字段要人话、验证证据要让外行能下结论、先找仓库既有规程、失败声明、failure cause、只报原因不报对策、分类不出就原样抛、等待提示、错误负载缺省字段、OOM 恢复、中断恢复、取消不等于丢弃、半成品保留、完成标记游标、重试准入、重试不生效、参数冲突、单次超时与总时长、重试留痕、兜底范围、提前终止原因、结束原因可见、主动退出留痕、诊断只读、修复须批准、diagnose不执行repair、读写分离、终态退出码、超时携带诊断、失败不二次变更、幂等护栏、轮询分批、卡住运行恢复
version: "1.150.0"
agent_created: true
---

# wb-debug-loop（排障：按纪律走，不靠猜）

来源：mattpocock/skills 的 `diagnose` 技能（重现 → 最小化 → 假设 → 工具 → 修复 → 回归测试）+ 通用调试纪律。提纯为本地循环。

**核心判断：改不动的 bug，几乎都是"还没复现就先改了"。** 定位是证据工作，不是灵感工作。

## 二、六步循环（原文已下沉 references/knowledge-base.md §六步循环下沉，2026-10-03 r408A）
## 二·五、修复验证：补丁是待验证假设（细则已下沉 KB）
- 完整论证见 [references/knowledge-base.md](references/knowledge-base.md) §二·五、修复验证：补丁是待验证假设。
> 本节（二·五·五、修在调用方收敛处：只修被报告的路径 = 修…）原文已整段下沉至 `references/knowledge-base.md`，需要时按标题检索。
<!-- 2026-09-29 r290 下沉：容错装置/失败经验记忆/日志即线索 3 节 → references/knowledge-base.md §r111 批 -->
## 二·七、失败永不阻塞主回复：回复路径上每一步都要 等 6 节（细则已下沉 KB）
- 完整论证见 [references/knowledge-base.md](references/knowledge-base.md) §二·七、失败永不阻塞主回复：回复路径上每一步都要 等 6 节。
## 复现不了就先把发生率抬高：1% 追不到，50% 就能二分（来源：topaiskills.com「diagnosing-bugs-skill-faq」（Matt Pocock `diagnosing-bugs`，mattpocock/skills 工程族）2026-09-21 实拉，与 §六步循环「没有稳定复现之前不改产品代码」互补——那条管"没有复现不许动手"，本条管"**复现率低到不可用时该往哪个方向使劲**"）；原文已下沉 references/knowledge-base.md §复现率低时的发力方向下沉，2026-10-03 r408C
## 探针要能一次撤干净，seam 太浅本身就是结论（同来源 `diagnosing-bugs` 技能正文，与 §诊断装置自身的可信度、§接线腐烂 互补——那两条管"检查器有没有遭遇"与"装了为什不生效"，本条管"**临时探针的回收**"与"**回归测试挂点选错时该怎么报告**"）

- **原文事实**：调试日志只允许打在**能区分假设的边界**上，绝不"log everything and grep"；每条调试日志带**唯一前缀**（如 `[DEBUG-a4f2]`），收尾一条 grep 全清；原文判词 "**one breakpoint beats ten log statements**"。性能回归不用日志查——**先建基线测量，再二分**。回归测试**在修复之前写，但前提是存在正确的 seam**（该测试在真实调用点上复现该 bug 形态）；**seam 太浅的测试给的是虚假信心**；**若根本不存在正确 seam，那本身就是发现**——代码库架构在阻止这个 bug 被锁定，要作为结论报出来。收尾六条清单：原 repro 不再复现（重跑第一轮循环）、回归测试通过、按前缀 grep 清掉全部 `[DEBUG-...]`、一次性原型删除或移到标记位置、**把被证实正确的那条假设写进 commit / PR 说明**。
- **判据**：
  1. **每条临时探针都要有可回收的标识**。判据：**写第一行调试代码前先定前缀，收尾时用同一个前缀 grep 并确认命中 0**；没有回收手段的探针不该落地（与 §观测是被动旁路 分工：那条管测量挂在哪条时间线，本条管临时测量怎么撤）。
  2. **"测不到"要分两种并分别报告**：seam 太浅 → **给的是假信心，必须标注**；没有 seam → **是架构结论，不是失败**。判据：**写回归测试前先回答"这个测试能不能在真实调用链上复现该形态"，答不出就别写，把答案当发现报**。
  3. **把"哪条假设是对的"写进提交信息**。判据：**下一次排障的人应该能从 commit 里读到这次的因果，而不是从代码里反推**。
- 提升层级：工作流（探针生命周期）+ 可复用 Skill（结论的写法）。
- 触发词：唯一前缀、[DEBUG-a4f2]、一次 grep 清理、一个断点胜十行日志、基线再二分、seam 太浅、没有 seam 是发现、假设写进 commit。


---

## 等待/轮询/卡住运行处置（来源：OpenClaw `ci/watching-runs.md`，2026-09-30 实拉）；原文已下沉 references/knowledge-base.md §等待轮询下沉，2026-10-04 r411A


## Harness 自改进与 trace 复用簇（细则已下沉 KB）
- 技能级记忆、Harness 工程与三阶段自改进、后台 review fork、视觉双扩展、trace 失败模式清单、trace→evaluator、harness 演进三问——**七条同源，完整论证见** [references/knowledge-base.md](references/knowledge-base.md) §Harness 与 trace 自改进簇。


## 数据钉定（input pinning）与局部执行（partial execution）：钉输入 + 只跑待测节点 = 最小可复现调试闭包（来源：docs.n8n.io types-of-executions 6,643B，2026-09-30 r327B 独立实拉）；原文已下沉 references/knowledge-base.md §数据钉定与局部执行下沉，2026-10-04 r409A
- **滑窗规避反模式**（arXiv 2609.30217 EvasionBench）：重试循环会把"相关上下文"推出监控/评审窗口，让同一操作在第 N 次重试"看不见地"通过——监控须锚定**操作序列**而非近期窗口，跨轮拆分动作计入同一意图链。
- **执行回放一等位**（Activepieces）：每次执行的完整动作序列留独立可读回放记录，排障不依赖 trace 后端。

## 读侧先行的灰度升级律（来源：docs.n8n.io/hosting/scaling/queue-mode/，2026-09-28 r210-B 独立实拉）；原文已下沉 references/knowledge-base.md §读侧先行下沉，2026-10-04 r411A
## 「之前照做的规则现在不照做了」先查修剪，再怀疑模型（来源：agentskills.io《How to add skills support to your agent》客户端规范 2026-09-28 r284-A 独立实拉 + arXiv 2606.22528《Governance Decay》独立核验；与 §上下文随循环增长要修剪 互补——那条是主动写减法，本条是被动排障归因）
- **实证**：客户端规范明文要求 **exempt skill content from pruning**，理由是技能指令中途被裁掉后"模型继续运行但没有专业指令，**没有任何可见报错**"；Governance Decay 给出量化——约束被摘要保住时违规 **0%**、被丢弃时 **38%**，失效呈**二值**（不是渐渐变差）。
- **判据**：长会话 / 多轮任务里出现"某条规则/约束/格式要求突然不被遵守"时，排障第一步是**取证该条指令此刻是否还在上下文窗口内**（检索原文字符串是否存在），再决定是否改写规则或换模型。**顺序不能反**：先改规则 = 在指令已经不在场的前提下做无效功；先怀疑模型 = 把上下文管理问题错记成能力问题。
- **判据延伸**：这也解释了为什么"规则写了但没生效"的高频根因是**被挤出去**而不是**没写清**——修法是把硬约束做原文透传（Constraint Pinning）而不是把规则写得更长。
- 提升层：工作流（排障归因顺序）。触发词：规则突然不生效、指令失效、行为漂移、被挤出去、上下文还在不在、先查修剪。


工具被拒先分三类再归因：在哪跑 / 是否存在 / 有没有逃生口，且必须看「生效值 + 它来自哪一层」工具被拒先分三类再归因：在哪跑 / 是否存在 / 有没有逃生口，且必须看「生效值 + 它来自哪一层」（来源：docs.openclaw.ai《Sandbox vs tool policy vs elevated》2026-09-29 r288-B 独立 curl 实拉原文核验）（原文已下沉 references/knowledge-base.md §r325B）
## 诊断输出要分「给人看的粗桶」与「给机器读的稳定原因码」两层；先分清「根本没发出调用」还是「发了但失败」（来源：docs.openclaw.ai/auth-credential-semantics 2026-09-29 r290-B 独立 curl 实拉 24,733B 原文核验）
- 原文："Probe results carry a `status` bucket (`ok`, `auth`, `rate_limit`, `billing`, `timeout`, `format`, `unknown`, `no_model`) plus a **stable `reasonCode` when the probe never reached a model call**"；七个稳定码 = `excluded_by_auth_order` / `missing_credential` / `expired` / `invalid_expires` / `unresolved_ref` / `ineligible_profile` / `no_model`；"Eligibility checks report `ok` as the reason code for usable credentials."
- 原文（对齐要求）："These semantics keep **selection-time and runtime auth behavior aligned**. They are shared by `resolveAuthProfileOrder` / `resolveApiKeyForProfile` / `openclaw models status --probe` / `openclaw doctor` auth checks."
- 判据：① 故障分两族——**没跑起来**（配置/凭据/选型，有稳定原因码）与**跑了但失败**（服务端结果）；绝大多数被误判成"模型不行"的故障其实在第一族，先取原因码再动手；② 原因码是**对外契约不是日志文案**——要稳定、可枚举、可用完了还准，改动要走版本；③ **选择期与运行期必须共用同一套判定**（探针说可用、真跑却失败 = 两处语义漂移，属设计缺陷不是偶发）；④ `ok` 也要占一个码位，别用空值表示成功——空值无法区分"没检查"与"检查通过"（与 AV 2.44.0「未检查是独立结论值」同向）。
- 提升层：工具/工作流。触发词：reasonCode、status bucket、稳定原因码、选择期运行期对齐、没发出调用、凭据不可用。

局部调试未必比整体便宜：部分执行要满足入口契约，且数据一大反而只能整跑局部调试未必比整体便宜：部分执行要满足入口契约，且数据一大反而只能整跑（来源：docs.n8n.io《Types of executions》2026-09-29 r290-C 独立 curl 实拉 .md 原文核验）（原文已下沉 references/knowledge-base.md §r325A）
多分支执行顺序不是逻辑决定的，是「创建时期版本 + 画布空间位置」决定的：结果顺序不对先查这两样多分支执行顺序不是逻辑决定的，是「创建时期版本 + 画布空间位置」决定的：结果顺序不对先查这两样（来源：docs.n8n.io《Understand execution order》2026-09-29 r296-A 独立 curl 取 .md 原文 1,835B 核验）（原文已下沉 references/knowledge-base.md §r325A）
## 超时不是一个数：默认值随触发类型分档、可调上限随套餐分档（来源：pipedream.com/docs/workflows/limits 2026-09-29 r296-C 实拉）；原文已下沉 references/knowledge-base.md §超时分档下沉，2026-10-04 r411A
> 下沉索引：〇、先分型：模型行为问题 vs 代码问题 等 2 节原文已移至 `references/knowledge-base.md`（按最旧批次下沉，正文只留指针）

## 已处理的失败是「独立可见状态」（Warning 态），不是消失了；重试有固定序列且超限会熔断关停调度（来源：help.make.com《Introduction to errors and warnings》+《Exponential backoff》2026-09-29 r337-Q-A 实拉核验；与 §重试掩盖 互补——那条管"别用重试糊过去"，本条管"重试本身有几条纪律"）
- 原文：Make 把错误与警告分开——错误=未被处理的意外事件，警告=「错误被成功处理后场景呈 Warning 态」；**12 种具名错误类型**（Bundle Validation/Data/Duplicate Data/Incomplete Data/Max File Size/Operations Limit/Data Size/Account Validation/Module Timeout/Connection/Rate Limit/Runtime）；handler 语义 Skip/Retry/Resume/Commit/Rollback，可挂 module/route/scenario 三级；**场景级内置指数退避自动重试 8 次（1、2、5、10、30 分钟、1、3、12、24 小时），第 8 次失败则 disables scheduling of the scenario（熔断关停调度）**。
- 判据：① **「已处理」≠「已消失」**——一个被 handler 兜住的失败要留下 Warning 痕迹，让它能被事后审计，而不是在日志里无影无踪（和 §静默降级 同源：凡静默掉的失败都要有可查的记录）；② **重试是有序列的、有上限的**——指数退避的时点固定（不是无限退避），到第 8 次仍失败就**主动熔断关停调度**，而不是一直重试把资源耗死或把下游打爆；③ handler 分三级挂载（模块/路由/场景）意味着**兜底粒度要选对层**——局部可恢复的挂模块级，要整体放弃的挂场景级；④ 把"重试多少次、超限怎么办"写成明确策略，而不是"失败就重试"的模糊指令。
- 提升层：工作流/诊断。触发词：警告态、12 类错误、重试 8 次序列、第 8 次熔断关停、handler 三级挂载、已处理失败留痕。

## 判死前先回查真实执行状态，别把「无信号」直接当「已失败」（来源：n8n 2.41.0 release note「Recheck the execution status before failing a stalled queue job」github.com/n8n-io/n8n/releases 2026-09-29 r334-Q-A 实拉核验；与 §心跳误杀 分工——那条管"心跳为什么发不出去"，本条管"判死这个结论本身要先验证"）
- 原文：n8n 在把「卡住的队列任务」标记为失败之前，先**回查该执行的真实运行状态**（数据库/执行引擎里的实际状态），确认它真的死了、不是「还在跑但信号没传回来」才下失败语义。
- 判据：① 「判死」是一个**结论**，不是「超时/无响应」这个信号的同义词——信号只是疑点，真实状态才是判决依据；看到 stalled/timeout/无心跳，先去查权威状态源（执行表/运行时），不要直接等价于"任务已失败"；② 误判的代价是**重复执行**：把一个还在跑的任务判死并触发重试/补偿，会和原执行并发抢同一份状态，制造更难查的竞态；③ 这条是「先验证再下结论」在排障里的具体实例化——和 §修复验证 同源：补丁是待验证假设，判死也是待验证假设。
- 提升层：工作流/诊断。触发词：判死前回查、stalled 先查真实状态、误判导致重复执行、队列任务判活、先验证再判失败。

## 超时不是回滚授权：判死与回滚是两个门；只有「已验证回滚」才交回前一代，且与分诊互不自动触发（来源：docs.openclaw.ai cli/update repair-and-recovery，2026-09-30 r320A 实拉）（细则见 KB，2026-09-30 r320C 下沉）


## 重试钉在单请求而非复合流、已完成步不重放；「已发出无应答」是歧义态须先对账；内层重试独立计数且外层可掐断；鉴权/计费/拒答不进重试预算直接走降级（来源：docs.openclaw.ai/concepts/retry，2026-09-30 r321B 独立实拉 9,854B；细则见 references/knowledge-base.md §r321B）
## 「恰好一次」的成立前提是在途时间有上界：只靠验证/对账在 late commit 下永远达不到，重尾时等待无效、须给每个写发幂等键；崩溃-恢复要查执行痕迹计数而非看结果（来源：arXiv 2609.29095，2026-09-30 r322C 独立实拉 44,254B，重复率 56%/74%、契约解释 81%；细则见 references/knowledge-base.md §r322C）


## 自述成功不构成幂等证据：重复执行中九成 agent 仍自报成功；引量化结论前先确认分子分母（来源：arxiv.org/abs/2609.29095，2026-09-30 r323B 独立实拉 44,254B）
- 原文：「the same frontier models duplicate in **56% and 74%** of episodes」（在途未返回 / 传输重复两种情形）；「lowers the duplicate rate from **28% to 4%**」（契约化后）；「agents **reported success in 90% of the episodes in which they had duplicated an effect**」；「the contract explains **81%**」= 契约能解释的**方差占比**，不是重复率（**口径纠偏**：不得把 81% 引成“81% 的请求会重复”）。
- 判据：① **“恢复后重跑成功”与“只执行过一次”是两件事**：重复执行里九成自带成功自述，因此验收幂等只能靠外部痕迹（执行痕迹计数、副作用唯一键、服务端去重日志），**不能靠 agent 汇报**——自述成功是“我觉得成了”，不是“只发生了一次”；② **引量化结论前先确认分子分母**：同一篇里 56/74%（重复率）、28%→4%（干预前后）、81%（方差解释度）属于三个不同量，混引会造出不存在的事实；③ 把“待补”复核成“已核”时，条目里要**写下核到的原句**（不是只写“已复核”），否则下一个人仍无法判断。
- 提升层：工具/工作流。触发词：自述成功、幂等证据、重复率、方差解释度、口径纠偏、痕迹计数。

## 兜底链路可能与故障链路同源：错误工作流默认指向自身、同一兜底可被多条主链路共用，且手动运行不触发——兜底能否工作无法用演练路径验证（来源：docs.n8n.io errortrigger 节点页 822,401B + flow-logic/error-handling 596,446B，2026-09-30 r324C 独立复拉命中「uses itself as the error workflow」×2、「can't test error workflows」×1、「same error workflow for multiple workflows」；与 §超时不是回滚授权 互补——那条管“判死与回滚分两门”，本条管“兜底自己会不会一起死”；细则见 references/knowledge-base.md §r324C）


## 异步入口的丢失窗 =「回执与落库之间」那一段：已应答的请求不会有人重试；有重建路径的子系统，陈旧备份严格劣于空库（来源：www.activepieces.com/docs/install/guarantees/disaster-recovery.md，2026-09-30 r325A 独立 curl 实拉 7,611B 逐串命中；经 Qoder r357-Q-A 提名）
- 原文：①「Activepieces returns `200` with an `x-webhook-id` header after the job is enqueued to Redis, **before** any Postgres record exists. If Redis loses its dataset in that window, those requests vanish without a trace, and the sender — having received a `200` — **will not retry**. Your async-webhook RPO **is** your Redis persistence window」；同步路径「the run is recorded in Postgres **before** execution」不受此窗影响；②「A **stale** Redis backup is **strictly worse** than an empty Redis plus the refill on restart」；③ runbook「Restore or replace Redis (an **empty** Redis is fine) → Restart the app containers. The refill machinery rebuilds schedules, renewals, and paused-run timers from Postgres → filter runs still in `QUEUED`/`RUNNING` … resumes from the last checkpoint and **never re-runs completed steps**」；④ 三 store 分册：Postgres=flows/runs/schedules/waitpoints/connections（System of record）、S3=执行历史（SOR）、Redis=除队列本身外全部可由 Postgres 重建；⑤「Recovery targets are stated as **formulas**…they are properties of *your* Postgres/Redis/S3 setup, not of Activepieces」；⑥ 队列重试「starts at 8 minutes — **longer than a typical failover**」；⑦「Database connection pools are **not guaranteed to re-establish cleanly** through a failover's DNS flip; a restart is cheap and **always correct**」。
- 判据：① **「已返回 200」不等于「已持久化」**——凡回执时点与落库时点不一致的入口（先入队、后异步落库），其暴露窗等于队列的持久化窗，且这扇窗内的丢失**不可自愈**，因为发送方拿到成功确认后不会重试；设计异步接收链路必须先回答「回执那一刻数据落在哪一层」，并把这个窗**单独**计量成 RPO，不能用整体可用性数字代替；② **RPO/RTO 是推导量不是产品属性**——官方把恢复目标写成公式，理由是自托管下它取决于你自己的存储档位；引用任何一个 RPO 数字前先问「它背后是哪个 store 的哪档持久化」；③ **有权威源 + 自动重建器的子系统不该备份**：陈旧副本会把已完成进度倒退回过去，比空副本更糟——空 + 回填是幂等收敛，旧副本是状态回退；判断「要不要备份」的标准是**有没有回填通道**，不是「数据重不重要」；④ **恢复程序必须自带人工收尾动作**：清空 → 回填 → 按最后检查点批量重试滞留态，且明确不重跑已完成步 ⇒ 恢复脚本自身必须幂等并能按检查点续；⑤ **恢复后重启优于「优雅重连」**——连接池不保证跨 DNS 切换自愈，宁可付一次便宜且永远正确的重启；⑥ **重试首延要大于典型故障切换时长**，否则所有重试都落在故障窗内，白烧预算还放大下游压力。
- 提升层：工作流/工具。触发词：异步暴露窗、回执先于落库、x-webhook-id、RPO=队列持久化窗、陈旧备份劣于空库、重建优先于备份、批量重试滞留态、DNS flip 后重启。


## 慢的外部依赖不得阻塞冷启动：连接与刷新各给一个独立上界，超时只降级不阻塞；启动期对未就绪依赖 fail-closed，刷新期旧值继续供给（来源：docs.n8n.io `/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/external-secrets.md` 4,588B，2026-09-30 r325B 独立 curl 实拉逐串命中，**通道更正**：Qoder 给的 `docs.n8n.io/use-environment-variables/external-secrets.md` 实际返回「Page Not Found」壳，真实前缀须经 `docs.n8n.io/llms.txt`(286,271B) 定位；经 Qoder r358-Q-B 提名）
- 原文：「`N8N_EXTERNAL_SECRETS_CONNECT_TIMEOUT`…`20`…If the vault doesn't answer in time, n8n **marks it as errored**, retries the connection in the background with **increasing delays**, and **startup continues without its secrets**.」「`N8N_EXTERNAL_SECRETS_REFRESH_TIMEOUT`…`20`…If the fetch takes longer, n8n **stops waiting** and the fetch **keeps running in the background**. When it completes, n8n stores the secrets. **At startup, workflows that use secrets from that vault fail until the first fetch completes. On an update interval, the previously fetched secrets stay available.**」「For HashiCorp Vault and Infisical, n8n also **cancels each single HTTP request after the larger of the two timeouts**.」（均 Available from n8n 2.41.0）
- 判据：① **冷启动不能被最慢的那个依赖绑架**——对不可达/慢的外部凭据源设**两个独立上界**（connect / refresh），到点即标记 errored 或停止等待，主流程继续；「配了但拉不到」不应等于「系统起不来」；② **降级方向按阶段分叉，不是一刀切**：启动期没有旧值可用 ⇒ **fail-closed 直到首次拉取成功**（依赖它的执行直接失败，不拿空值蒙混）；周期性刷新已有旧值 ⇒ **旧值继续供给不中断**（"取新的别把已有的掐了"）；同一个超时在两个阶段给出相反动作，是设计不是矛盾；③ **后台续跑 + 递增延时重试**是让"慢依赖"与"主流程"解耦的标准形态：等待被截断，但工作不丢弃，成功即入库；④ **单个 HTTP 请求的上界要由两个超时中的较大者兜底**，否则会出现"整体超时已过、单次请求还在挂着"的悬挂连接。
- 提升层：工具/架构。触发词：冷启动不阻塞、connect/refresh 双超时、启动期 fail-closed、刷新期旧值继续、后台续跑、递增延时重连、单次请求上界。

## 并发闸门有作用域：「已开限流」≠「全链路受控」，且队列项不可重试（来源：n8n control-concurrency 本机实拉，r326B）
- **原文**：①「Concurrency control applies **only to production executions**: those started from a webhook or trigger node. It doesn't apply to any other kinds, such as **manual executions, sub-workflow executions, error executions, or started from CLI**」；②「**You can't retry queued executions.** Cancelling or deleting a queued execution also removes it from the queue」；③「On instance startup, n8n **resumes queued executions up to the concurrency limit** and re-enqueues the rest」。
- **判据**：① **设限后必须逐执行形态验证是否真被管住**——守压力的闸门恰恰不管「兜底用的错误工作流」与「被复用的子工作流」这两条最容易失控的路径；「我开了限流」只证明主路径被管。② 排队 ≠ 可重试：入队即失去重试权 ⇒ 队列不是「稍后重试的备份」，重试责任在调用方。③ 重启策略=「按上限恢复 + 其余重新排队」⇒ 重启后的在途量由闸门决定，不是全量洪峰。
- **提升层**：工作流/工具。触发词：限流作用域、only production executions、manual/子流程/错误流程绕过、队列不可重试、重启按上限恢复。

- **按「调用方身份」计数的闸门必须自证生效：反向代理会让它整体失效（来源：Flowise rate-limit 本机实拉，r326B）**：本章已下沉 `references/knowledge-base.md`（r326B）。
## 诊断技能严格只读、修复须经批准：diagnose 与 repair 是分离的两动作（来源：docs.openclaw.ai/tools/custodian-skills.md 5,298B，2026-09-30 r336A 独立实拉）
- 原文：「Repair diagnoses with `openclaw doctor --lint`. Only an explicitly approved repair uses `openclaw doctor --fix --non-interactive`. The read-only `diagnose-gateway` skill recommends that separate step but never runs it.」
- 判据：① **诊断（只读）与修复（写操作）必须是两个被分离的动作**：只读诊断技能只负责发现 + 推荐修复步骤，**永不自己执行修复**；修复动作须单独、显式批准、并以非交互（`--non-interactive`）方式运行。② 让「会改东西」的技能同时拥有诊断与修复，等于把扳手与螺丝刀焊在一起——误触发诊断即触发写，且审计里无法区分「只是看了」与「已经改了」。③ repair 的「批准 + 非交互」双约束 = 可审计点：谁批准、何时、跑的是哪条命令，事后能查；交互式修复把决定权推给运行时的 stdout，无法留痕。④ 与 §超时不是回滚授权 同源——判死/回滚分两门，本条把「看」与「改」也分两门。
- 提升层：工作流/安全边界。触发词：诊断只读、修复须批准、diagnose 不执行 repair、doctor --lint、doctor --fix --non-interactive、读写分离。

- **脱敏的正确形态是「保留可观测骨架、替换载荷」，且错误详情必须在脱敏清单内（来源：docs.n8n.io/deploy/host-n8n/configure-n8n/security/redact-execution-data.md 17,934B，2026-09-30 r338C 独立实拉）**：本章已下沉 `references/knowledge-base.md`（r338C）。
- **定时器恢复的默认动作是「重排未来时点」而不是「补跑历史欠账」：合并错过的滴答，且用运行身份而非起始时间认领（来源：docs.openclaw.ai/automation/cron-jobs/how-it-works.md 9,877B，2026-10-01 r339A 独立 curl 实拉逐串命中）**：本章已下沉 `references/knowledge-base.md`（r339A）。
## 并发互斥的锁键必须是「执行身份」而不是调用通道或运行时形态；队列满有三档背压语义；旁路维护失败不得替换已完成的回复（来源：docs.openclaw.ai/concepts/queue.md 17,920B + concepts/compaction.md 17,978B，2026-10-01 r340A 独立 curl 实拉逐串命中）
- **原文**：①「CLI, embedded, and Codex runs share the same **session-key lane** (`session:<key>`). Each turn waits there before acquiring the session's execution claim, so **changing runtimes cannot start a competing turn**」；②「`drop: \summarize\` ... **drop the oldest queued entries as needed, keep compact summaries, and inject them as a synthetic followup prompt**」/「`drop: \old\` ... drop the oldest ... **without preserving summaries**」/「`drop: 
ew\`: **reject the newest message when the queue is already full**」；③「**Optional maintenance failures are logged without replacing an already completed reply**」；④「A running stage is **not preempted**」+「asynchronous stage work **can still overlap and does not count toward that time budget**; this **does not lower the run concurrency limit** or change session serialization」。
- **判据**：① **互斥的键要绑在谁在执行上，不是从哪条路进来**：CLI / 嵌入式 / 别的运行时共享同一把会话锁，于是**换一个入口并不能绕过互斥**。⇒ 排查为什么两个回合打起来了时，先问锁的键是什么——按进程名、按调用方式、按客户端类型加锁，都会在换一种入口时被绕过；只有按会话身份加锁才成立。② **队列满不是一种行为，是三档语义，选错档就是选错丢谁的信息**：`summarize` 丢最旧但把摘要合成一条后续提示（信息降级保留）/ `old` 丢最旧且不保摘要（信息丢失）/ `new` 拒最新（保护历史、让新调用显式失败）。⇒ 设计背压时必须显式选档并写清满了之后谁被丢；默认档往往最温柔也最容易被误当成没丢。③ **旁路维护的失败只能进日志，不能回写主结果**：压缩、落盘、刷新这类顺手做的工作失败时，已完成的回复仍然是已完成的——不得用一个后来的失败把已交付的成功改成失败态。⇒ 判成败要分清主链路与旁路：旁路的健康度单独计量，不并进主结果的状态机。④ **让出 CPU 的预算与并发上限是两个旋钮**：切片让出（16 个阶段或 8ms）只保证入口不被饿死，既不抢占运行中的阶段，也不改变并发上限与会话串行化。⇒ 调响应变慢时不要把让出阈值当成并发限制去改。
- **提升层**：工具/工作流/可观测性。触发词：锁键=执行身份、session-key lane、换运行时不绕过互斥、队列满三档、drop summarize/old/new、背压语义、旁路维护失败不降级、让出预算≠并发上限。


## 改向/取消的生效边界是「原子发射检查点」；落盘不等于已被消费；「调用被跳过」不能反推「有用户输入在等」；能力缺失应降级为等待而非失败（来源：docs.openclaw.ai/concepts/queue-steering.md 12,366B + concepts/memory.md 15,623B，2026-10-01 r340B 独立 curl 实拉逐串命中）
- **原文**：①「OpenClaw **distinguishes started work from requested work**」+「A parallel batch has **one atomic launch checkpoint**. A steer present before it suppresses all prepared calls; a steer arriving after it **does not recall any of them**」+「Validation or policy outcomes finalized before the parallel checkpoint **remain truthful**. Only executable calls that did not start receive the steering skip result」；②「A **later answer does not replace a completed answer to an earlier input**, even when steering skipped its pending tools」；③「A transcript commit **confirms persistence, not that a later model request has read the input**」；④「Internal updates, including subagent completion reports, also use this steering boundary ... A skipped tool **does not necessarily mean a user message is waiting**」；⑤「When a runtime **cannot accept steering** in `steer` mode, OpenClaw **waits for the active run to finish** before starting the prompt」。
- **判据**：① **已启动与已请求是两类工作，取消只能作用于后者**：并行批有一个原子发射检查点——检查点之前到达的改向抑制全部已准备的调用，之后到达的**一个也召不回**。⇒ 排查我明明取消了怎么还跑了时，别去看取消信号送达没有，去看它相对发射检查点的先后；另外**检查点前已定稿的校验/策略结论不因后续改向而失效**，别把已定稿的前置判断一起回滚掉。② **后到的回复不覆盖先到的已完成回复**：多输入场景下每个输入各有其答案，即使后来的转向跳过了前一个输入的待办工具，前一个的答案仍是已交付事实。⇒ 判这次到底答了没要按输入逐条对账，不能只看最后一条输出。③ **持久化与消费是两件事**：transcript 提交只证明写进去了，不证明后面的请求读到了。⇒ 排障数据链路时，把落盘成功当成下游已见是最常见的一类误判；要查消费侧（谁读了、读到哪一条）。④ **同一个边界可能承载多种来源，因此现象不能反推原因**：内部更新（子 agent 完成报告）走的是同一条转向边界，却可以隐藏于 transcript 且不进用户队列。⇒ 看到某次调用被跳过不能直接推出有用户消息在等——先枚举这个通道上还有哪些非用户来源。⑤ **能力不支持时的正确行为是显式降级而不是报错**：运行时不接受同回合转向时，系统选择等当前回合跑完再起新回合。⇒ 设计可选能力时，把不支持的路径写成一条可预期的降级链路（等待/排队/换通道），不要让它变成一次莫名失败。
- **提升层**：工具/工作流/可观测性。触发词：原子发射检查点、started vs requested work、改向不召回、后答不覆盖先答、落盘不等于已消费、transcript commit、跳过不反推用户输入、能力缺失降级等待。

- **入队四态语义；显式命令覆盖持久设置；降级会剥离语义标签（来源：docs.openclaw.ai/tools/steer.md 3,228B，2026-10-01 r342A 独立 curl 实拉逐串命中）**：本章已下沉 `references/knowledge-base.md`（r342A）。
- **续期只认真实执行；环境变量常常只是初值（来源：docs.openclaw.ai/concepts/session.md 22,390B + www.activepieces.com/docs/install/configure-operate/telemetry.md 2,830B，2026-10-01 r342B 独立 curl 实拉逐串命中）**：本章已下沉 `references/knowledge-base.md`（r342B）。
## 降级是回合局部的；受理后台维护不等于清理完成（来源：docs.openclaw.ai/concepts/context-engine.md 26,167B，2026-10-01 r343A 独立 curl 实拉逐串命中）

- **原文**：①「OpenClaw uses the legacy context path **for the whole logical turn, including retries**. The configured context-engine slot is **not changed**, and OpenClaw **tries the configured engine again on the next logical turn**.」；②「When queued budget compaction **accepts** background maintenance, it keeps the prepared runtime alive through maintenance, coalesced reruns, and engine disposal. **Acceptance does not mean cleanup has finished.** **Return asynchronous work** from engine methods and `dispose()` so the host can join it before releasing their resources.」；③「A stalled cleanup **logs a warning and lets the completed reply return**; it does not cancel the plugin's pending disposal. Cleanup failures and timeouts ... **do not certify resource closure**.」
- **判据**：① **降级的作用域要说清三件事：作用于哪一段、改不改配置、会不会自动恢复**：本例是"整个逻辑回合（含该回合内的重试）走降级路径、槽位配置不被改写、下一回合自动再试原实现"。⇒ 排障时看到"走了降级实现"不能直接判定配置被改或能力不可用——它是**回合局部**的临时态；反过来，若降级改写了配置，就会变成需要人工回退的持久态。② **"受理"只代表接下了任务，不代表活干完了**：后台维护被接受后，运行时必须**跨维护、合并重跑与 dispose 全程保活**，且要把异步句柄**交回宿主 join**，宿主才能在释放资源前等到它落地。⇒ 受理方不能一返回就拆资源；返回异步句柄是让"我可以等"这件事成为可能的唯一机制。③ **清理卡住不影响回复返回，但这不是"资源已关闭"的证据**：清理超时只记警告、让已完成回复先走，同时不取消待处理的释放动作；超时与失败都不认证关闭。⇒ 收尾判定要分两条线——"用户拿到回复了"和"资源释放完了"是独立事件，不能拿前者当后者的证据；要证明关闭，得有关闭侧自己的回执。
- **提升层**：工作流/工具。触发词：turn-local 降级、降级不改配置、下回合自动重试、accepted 不等于 cleanup finished、异步句柄交回宿主、清理超时不认证关闭、回复返回不等于资源释放。


## 配置写入分运行时覆盖与持久两档；异步写失败不回滚已生效的会话选择（来源：docs.openclaw.ai/tools/slash-commands.md 38,378B，2026-10-01 r343B 独立 curl 实拉逐串命中）

- **原文**：①（`/debug`）「**Overrides apply immediately to new config reads but do `not` write to disk.**」（`/config`）「`/config` updates **persist across restarts**.」；②「**Asynchronous write errors do not revert the session selection.**」「Immutable configuration stays unchanged.」
- **判据**：① **"改配置"要分清两档：运行时覆盖（立即生效、不落盘、重启即失）与持久写入（跨重启）**：两者命令不同、可见性不同。⇒ 排障"我明明改了怎么重启就没了"的标准答案是先确认走的是哪一档；反过来"改了没生效"也要确认是不是只写了运行时而读的是落盘值（或反之）。**同一份配置存在两个真源（内存覆盖 / 磁盘）时，必须能自报当前读数来自哪一档**，否则任何"改了没生效"都无从判断。② **内存态已生效、持久态写入失败时，系统保留已生效状态而不自动回滚**：会话选择已经切过去了，配置落盘却是异步失败——结果就是"实际在用的"和"重启后会读到的"不一致，且没有自动纠正。⇒ 遇到"跑着是对的、重启就变了"，不要假设是缓存或时序，先查**上一次持久化有没有真的成功**；设计这类两段写入时必须给出显式对账手段（状态可查 + 失败可见），不能依赖"反正下次会重试"。
- **提升层**：工具/工作流。触发词：运行时覆盖不落盘、/debug vs /config 两档、持久跨重启、异步写失败不回滚、内存态与持久态不一致、配置两个真源。


## 配置意图要三参数分立：设置值 / 显式置空 / 清除覆盖；吊销不因重新启用而回溯（来源：docs.openclaw.ai/automation/cron-jobs/payloads.md 27,960B，2026-10-01 r343C 独立 curl 实拉逐串命中）

- **原文**：①「Pass `--fallbacks ""` for a **strict run with no fallbacks**.」「Pass `--tools ""` for an **empty allowlist that disables all agent tools**, including tools used by a condition trigger.」「`--clear-fallbacks` ... **removes the per-job fallback override so the job follows configured fallback precedence**. Cannot combine with `--fallbacks`.」「`--clear-model` ... removes the per-job model override so the job follows normal ... precedence.」；②「Disabling or removing a job, withdrawing its `message` capability, or revoking its caller or plugin authority **stops further affected reads**」「**Re-enabling the job does not restore an occurrence's revoked access.**」
- **判据**：① **"置空"和"清除覆盖"是两种完全不同的意图，不能用同一个空值表达**：`--fallbacks ""` 是**显式声明"我不要任何回退"**（严格模式，失败即失败），`--clear-fallbacks` 是**撤销本次覆盖、回到继承的配置优先级**；同理 `--tools ""` 是"显式禁用全部"，`--clear-tools` 才是"恢复继承"。⇒ 排障"为什么还在回退 / 为什么工具全没了"先分清用户当时下的是哪一种意图；设计配置接口时，这三者（设具体值 / 显式置空 / 清除覆盖）**必须是三个不同的参数且互斥**，否则"传空串"这一个动作会同时承担两种相反语义。② **吊销是单次不可撤销事件，重新启用只恢复未来**：吊销一旦发生，该次调用后续的读取立即停止；之后把作业重新启用，也不会把这次已吊销的访问还回来。⇒ 排查"重新打开了怎么还是读不到"时，答案不在配置里而在事件里——**吊销作用于发生时的那一次，重新启用作用于之后的每一次**，两者不互补。
- **提升层**：工具/工作流。触发词：配置意图三参数、显式置空 vs 清除覆盖、--fallbacks 空串严格模式、--tools 空串全禁、--clear-* 恢复继承、吊销不回溯、重新启用只恢复未来。

- **远端执行的 canonical 唯一且随模式改变 + 自动修复不得顺带放宽安全面 + break-glass 显式命名 + attested 工作区消失拒绝重播种**：本章已下沉 references/knowledge-base.md §r346B。

- **「没生效」三分支（未发现/不合格/未执行）+ 静态资格报告只覆盖它检查过的项 + 发现不递归且拒绝后不放宽**：本章已下沉 references/knowledge-base.md §r346C。

## 失败恢复有两条硬边界：回滚资格按「是否事务模块」封闭枚举，且重试耗尽可级联改变自动化生命周期（来源：help.make.com/rollback-error-handler.md 8,865B + exponential-backoff.md 2,779B + docs.n8n.io/.../executions.md，2026-10-01 r348A 独立 curl 实拉）
- 原文：①「Modules that support transactions are labeled with the 'ACID' label.」②「Auto-commit enabled — Only the module that produced the error can revert its changes.」③「Auto-commit disabled — All changes made during the bundle's execution across every transaction-supported module can be reverted.」④「If the 8th attempt fails, Make disables scheduling of the scenario.」⑤第二证 `N8N_WORKFLOW_AUTODEACTIVATION_MAX_LAST_EXECUTIONS=3`。
- 判据：① **回滚范围不是「尽量回滚」，而是按模块是否事务（ACID 标签）封闭枚举** —— 非事务模块的改动失败后仍然留着。⇒ 任何「出错就回滚」的承诺都必须先回答哪些改动真的可回滚；把不可回滚的算进去，验收时会得到「回滚成功了但状态还是脏的」。② **提交模式反转回滚粒度**：Auto-commit 开=只有出错模块回滚；关=整个 bundle 跨全部事务模块回滚。粒度更粗的那一档不是更好，而是失败时影响面更大，要与业务的原子性需求对表。③ **重试耗尽不止是这次失败**：它可以直接改自动化本身（停用调度）。⇒ 排障「这条自动化怎么不跑了」时，先看是不是先前的重试耗尽把它关掉了，而不是查触发器与权限。
- 提升层：工作流。触发词：ACID 标签回滚资格、Auto-commit 反转回滚粒度、只有出错模块可回滚、重试耗尽停用调度、AUTODEACTIVATION。

## 同一个错误的默认处置会随调度形态分岔；重试资格要按错误类别封闭列举，不靠「看起来可重试」（来源：help.make.com/fix-rate-limit-errors.md 9,275B + docs.dify.ai/en/api-reference/guides/errors.md 3,157B，2026-10-01 r348A 独立 curl 实拉）
- 原文：①同一 `RateLimitError`（429）无 handler 时：定时触发=「pauses the next scenario run for 20 minutes」；即时触发=「reruns the incomplete execution from its start with exponential backoff」。②Dify：「Retry with backoff: `too_many_requests`, `500`, and network failures」vs「Don't retry as-is: validation errors (fix the request first), authorization failures, or quota errors (they won't clear until the quota does)」；`code` 是稳定分支键，`status` 只镜像 HTTP。
- 判据：① **跨调度形态的默认值不可假设一致**：同一个 429 在定时/即时两条路径上的默认动作完全不同（暂停 20 分钟 vs 从头指数退避）。⇒ 写重试/兜底策略时先问这条路径的调度形态是什么，否则同一种错误会得到两种完全不同的用户体验。② **重试资格要写成两张封闭清单**（可重试 vs 不可原样重试），而不是一个「是否重试」布尔：配额类错误在配额刷新前重试纯属浪费，鉴权/校验类不改请求重试必然重复失败。③ **分支键取稳定字段**：用业务 `code` 分支，不要用镜像 HTTP 的 `status` —— 后者会随传输层重映射漂移。
- 提升层：工具/工作流。触发词：429 定时暂停 20 分钟、即时指数退避、同错误分岔、重试白名单黑名单、配额错误不重试、code 稳定分支键、status 只镜像 HTTP。

## 背压要先分「丢弃式 / 阻塞式」两档并显式写出；限流的作用面按触发类型分轨（来源：pipedream.com/docs/concurrency-and-throttling.md + docs.n8n.io `/scaling/control-concurrency.md`，2026-10-01 r348A 独立实拉）
- 原文：①「fixed window throttling」、`limit=0` 即关队列、「exceeds the queue size, events will be lost」。②队列仅对 event-driven 生效，「excluding native HTTP or cron types」。③第二证：n8n 并发上限「applies only to production executions」，显式不含 manual / sub-workflow / error / CLI。
- 判据：① **背压有两档且代价相反**：丢弃式（队列满即丢事件，吞吐让位于内存）与阻塞式（反压上游，延迟换不丢）。⇒ 选型时先声明是哪一档；混着用会出现「既延迟又丢事件」的最坏组合，而日志上两者都只是「慢」。② **`limit=0` 这种取值要显式识别** —— 它不是队列无限，而是队列不存在，溢出直接丢。③ **限流/并发上限必须点名覆盖哪些触发类型**：只覆盖事件驱动、不覆盖 HTTP/cron/子工作流/手动/错误工作流是默认形态。⇒ 排「限流没生效」时先核对触发类型在不在作用域内；恰好漏掉兜底错误工作流与被复用子工作流，是最常见的失效面。
- 提升层：工作流。触发词：丢弃式背压、阻塞式背压、events will be lost、limit=0 关队列、限流按触发类型分轨、生产执行才限流、子工作流不在并发上限内。

## 「我在改的东西会不会被在途同步覆盖」要按锁的覆盖范围判，不按我的操作意图判（来源：docs.openclaw.ai/gateway/openshell.md 25,346B，2026-10-01 r348A 独立 curl 实拉）
- 原文：①「External editors and other Gateway processes do not participate in that lock」—— mirror 模式的锁只覆盖同一 Gateway 进程内的 upload→command→download。②「symlinks, FIFOs, or Unix sockets, into either workspace」永不复制。③清理失败须保留 runtime registry 条目供 recreate/prune 重试，明令勿靠删 registry 或切 workspace 隐藏失败。④`timeoutSeconds:120` 但 sandbox 创建保底 ≥300s。
- 判据：① **锁的作用域不等于「所有会碰这个文件的人」**：进程外的编辑器与宿主进程不参与锁，因此运行中的镜像命令在 download 阶段可以覆盖外部编辑。⇒ 「我刚改的怎么没了」这类问题的判据是谁参与这把锁，不是我改的时候有没有人看着。② **清理失败要留下可重试的把柄**：删沙箱失败时保留 registry 条目，是为了让 recreate/prune 还能找到它；靠删记录或切工作区让错误消失，等于把可重试故障变成不可见孤儿。③ **超时分档要按阶段看**：执行超时与创建保底是两个数值，用执行超时去估创建等待会误判卡死。
- 提升层：工作流。触发词：锁不覆盖外部编辑器、download 覆盖外部编辑、清理失败保留 registry、勿隐藏失败、symlink 不跨同步、创建保底超时。

## 分叉结构的「并行性」与「可合并性」都不对称，不能按图形外观推断（来源：help.make.com/router.md 6,347B + if-else-and-merge.md 19,001B，2026-10-01 r348B 独立 curl 实拉）
- 原文：①「modules connected to a router run **sequentially, not in parallel**」；②同页对照表：`can be merged back together with a Merge module` vs `Routes can't be merged back together`。
- 判据：① **看到扇出就假设并行，是「跑得挺快但结果对不上」类 bug 的误判源头**：同一种图形，在一种节点类型下是顺序执行。⇒ 排障前先确认分叉节点类型，再谈并行；性能预期与正确性预期都要按节点语义而非连线形状来定。② **两种分叉的合并能力不对称是结构事实**：router 分支不可在下游合并，if-else 分支可以。⇒ 不能把一种分叉的收束手法迁移到另一种；「聚合」这个词在同一系统里至少三种语义（顺序聚合 / 按到达顺序收带上限 / 任一分支为空即不产出），引用时必须点名是哪一种。
- 提升层：工作流。触发词：router 顺序非并行、扇出不等于并行、Routes 不可 merge、if-else 可 merge、聚合三种语义。

## 观测面可损、重放面必精：「看不见」不等于「没存」（来源：docs.n8n.io `/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions.md` 13,422B，2026-10-01 r348C 独立 curl 实拉）
- 原文：「For larger executions, n8n omits the data (shown as **too large to display**)」+「**Doesn't affect retrying or resuming executions, which always load the full data**」；`EXECUTION_DATA_MAX_DISPLAY_SIZE` 默认 104857600。
- 判据：① **展示截断与存储完整是两个不同的面**：观测面为了不把低资源实例拖垮而省略大数据，但重试/恢复永远加载全量。⇒ 「界面上看不到数据」不能推出「数据没存」；排障时把「取不到数据」至少分成三支 —— **没存 / 没到（写入未成功）/ 该面故意不可访问**，逐支验证而不是直接判丢。② **阈值是配置项而非固定行为**：`MAX_DISPLAY_SIZE` 可调，同一个现象在不同实例上成因不同。⇒ 报「这里显示 too large」时先读当前配置值，再判是不是容量问题。
- 提升层：工作流/可观测性。触发词：观测可损重放必精、too large to display、看不见不等于没存、取不到数据三分支、MAX_DISPLAY_SIZE。

## 运行期组件健康位与宿主健康态分离：被调组件降级只让「该执行面」失败，宿主整体继续跑（来源：help.make.com/on-premise-agent.md 17,056B，2026-10-01 r349A 独立 curl 实拉，`every four minutes` / `associated scenarios still run` / `500 error` 逐串命中；经 Qoder r366-Q-A 提名）
- 原文：①「Make checks its activity **every four minutes**」；②「When in **Not responding** status, **associated scenarios still run**, but the module using the On-prem agent shows a **500 error**」。
- 判据：① **宿主健康 ≠ 被调组件健康**：组件失联时场景整体照跑，只有用到它的那个模块报错 ⇒ 排障要问「报错落在哪一层」，而不是看整体是否在跑；把「整体在跑」当作依赖健康的证据会漏掉单点降级。② **降级要落到具体执行面**：健康位是每组件独立的，一个组件 Not responding 不应升级为全局停 ⇒ 先定「哪些执行面会因该组件失败」，再定告警粒度。③ 与既有「慢依赖不阻塞冷启动」（启动期）互补：本条是**运行期**。④ 心跳周期（4 分钟）决定失联判定延迟，别把它当实时信号。
- 提升层：工作流。触发词：组件独立健康位、Not responding、降级只失败该执行面、宿主照跑、心跳 4 分钟、运行期降级。

## 「查不到状态变化」先核默认作用域键是不是资源 ID：同一资源的所有调用共用一个会话/状态桶（来源：docs.langflow.org/memory 56,213B，2026-10-01 r349B 独立 curl 实拉，`default session ID is the flow ID` 逐串命中；经 Qoder r367-Q-B 提名）
- 原文：「The **default session ID is the flow ID**, which means that all chat messages for a flow are stored under the same session ID as one large chat session」。
- 判据：① **默认归属键是资源 ID 而不是使用者 ID**，是一个静默的共享面：不同用户在同一流程上的对话会互相污染记忆、串数据、并把审计归因错到「同一个主体」。② **症状 → 成因要分三档**：串数据（记忆污染）/ 审计归因错（主体不可分）/ 状态莫名被重置（作用域比预期宽）⇒ 排障第一步是问「这个状态的默认键是谁」，而不是先改 prompt。③ 与既有「解析基准 ≠ 隔离边界」互补：那条管路径解析，本条管**状态/会话的默认归属键**。
- 提升层：工作流。触发词：默认 session ID 是 flow ID、作用域键是资源 ID、记忆污染、串数据、审计归因错、共享会话桶。

## 挂起态是双字段：状态位只回答「态」，原因与恢复入口在独立实体；恢复去重的正确原语是存储唯一约束（来源：www.activepieces.com/docs/install/architecture/waitpoints.md 7,102B，2026-10-01 r349B 独立 curl 实拉，`only carries status` / `the *why* lives on the waitpoint` / `never processes a resume twice` / `10 000 is also the ceiling` 逐串命中；经 Qoder r367-Q-B 提名）
- 原文：①「The flow run row **only carries status** (`PAUSED`, `RUNNING`, …); the ***why*** lives on the waitpoint」；②「Duplicate callbacks are absorbed by the **uniqueness constraint**; the engine never processes a resume twice」；③「**10 000 is also the ceiling**: the env var cannot raise it higher」。
- 判据：① **状态位不是原因位**：把「为什么等」压进状态枚举，会在复挂/多因等待时信息不够 ⇒ 等待必须有独立持久实体承载原因与恢复入口。② **去重要落在存储的唯一约束上，不是应用层判重**：应用层判重有并发窗口，唯一约束没有；「重复回调被唯一约束吸收」给出的是**键位实现**，比「记得判重」可靠。③ **要区分可调上限与已封死上限**：10 000 是 env 也抬不上去的硬顶 ⇒ 已封死上限应写进容量规划，别把 env 当逃生口。
- 提升层：工具/工作流。触发词：挂起态双字段、waitpoint 承载原因、唯一约束去重、重复回调吸收、已封死上限、10 000 ceiling。

## 重放默认跑在「最新代码」上：可复现取证必须显式钉住原运行版本（来源：pipedream.com/docs/workflows/building-workflows/inspect.md 2,607B，2026-10-01 r349C 独立 curl 实拉，`replays** the event against the newest version of your workflow` 逐串命中；经 Qoder r368-Q-C 提名）
- 原文：replay「**replays the event against the newest version of your workflow**」（保序）。
- 判据：① **默认把事件与代码版本解耦**：重放通过只能证明「用现在这份代码能跑通这个事件」，**不能证明当时那次执行是正确的** ⇒ 取证/复盘类重放必须显式钉原运行版本，否则「重放通过」会被误当成历史结论。② 与既有「观测可损、重放必精」同族：那条讲**数据完整性**，本条讲**代码版本绑定**。③ 自愈/续跑也有预算（openclaw `concepts/session.md` 22,390B，`budget` 命中，耗尽后换新会话身份而非无限救旧）⇒ 「救回来」不是无成本的默认选项。
- 提升层：工作流。触发词：重放跑最新代码、事件与代码版本解耦、钉原运行版本、取证重放、自愈预算耗尽换新会话。

## 调度面「防惊群」与「漏扫记账」是两件相反极性的事：默认抖峰，漏扫按已完成记账不补跑（来源：docs.openclaw.ai/automation/cron-jobs/schedules.md 15,917B，2026-10-01 r349C 独立 curl 实拉，`stagger` ×5 / `catch-up` / `fire: true` ×3 逐串命中；经 Qoder r371-Q-C 提名）
- 原文：①密集周期默认 **stagger**（随机抖动）防惊群、可显式关闭；②漏扫走 **catch-up** 路径，补录计数为已完成、异常不自滚而交退避队列；③gate 脚本仅当输出 `fire: true` 才触发执行。
- 判据：① **防惊群是默认开启的性能保护**（stagger），但它同时意味着「周期不再精确」——需要精确时刻时必须显式关闭抖动，而不是假设周期严格。② **漏扫不补跑、只记账为已完成**：与既有「misfire 重放」是**相反极性**的两条（一个重放、一个记账），引用时必须点名当前系统的选择，否则「漏了会不会补」两种预期都会错。③ **评估默认静默、触发须显式放行**（`fire: true`）：gate 脚本输出非 true 一律不触发 ⇒ 「脚本跑了但没执行」的正确怀疑方向是 gate 输出，不是调度未触发。
- 提升层：工作流。触发词：stagger 防惊群、漏扫 catch-up 记账、fire:true 才触发、gate 默认静默、周期不精确。

## r350A · 关闭序钩子的超时语义：限时的是调用方等待，不会取消 handler（来源：docs.openclaw.ai/automation/hooks/event-types，2026-10-02 r350A 实拉 224,709B）

- **★关闭类钩子的等待是有界的，超时不取消 handler**：`gateway:shutdown` 默认等 5 秒、`gateway:pre-restart` 另加 10 秒预算；文档原话 **"These bound the caller's wait, not the handler's work: timeout does not cancel promises"**。判据：**超时 ≠ 取消**，一个永不 settle 的 handler 会让进程内关闭永远完不成；排查"关不掉/关得很慢"时查的是 handler 是否 settle，不是把超时调大。
- **★关闭前 Gateway 会 join 真实钩子完成情况**：关闭共享状态前要等 handler；期间通道还没拆，但**排队的 agent 工作与消息投递都不保证在关闭前跑完**。判据：**"通道还活着"不等于"任务会跑完"**，收尾不能把未决工作算作已完成。
- **★持久化出站队列的结算可以推迟观测，但不让钩子本身变持久**。判据：**投递结算 ≠ 钩子持久化**，别因为"队列会补发"就认为关闭钩子里做的事是可靠的。
- 排查顺序：进程退不出 → 先看是否有未 settle 的关闭钩子 → 再看 handler 内部是否在等一个永远不会返回的 promise → 最后才看超时配置。

## r350A · 并发容量要选一个"货币"并按占用时长计量，耗尽按触发类型三路分叉（来源：help.make.com/parallel-capacity.md，2026-10-02 r350A 实拉 9,462B）

- **★并发上限必须用统一货币计量，且按"运行期间持续占用"计**：Make 用 PU（Processing Units），每次运行期间占住、结束即释放；处理大数据的运行全程占多个 PU。判据：**并发配额是"占用时长 × 单份重量"的积分，不是"次数"**——同样跑 N 次的两个场景，占的容量可以差很多。
- **★容量耗尽的处理按触发类型分叉**：即时触发（无 webhook 响应模块）→ 排队，容量可用再处理；定时触发 → 延迟下一次定时运行（**不排队补跑**）。判据：**"延迟"与"丢弃/排队"是三种不同后果**，设计背压前必须明确本次走哪条。
- **★监控要能同时看"余量"和"形状"**：堆叠条按场景上色（每根柱一个时点、每色一个场景），Y 轴有 Full capacity（看剩余余量、触顶线=该时刻被延迟或拒绝）与 Fit to usage 两种刻度；拉长到数天才能看出周期性峰值（夜间同步/周报）。判据：**只看峰值不看按场景堆叠，定位不到是谁打满的；只看短期看不出周期峰**。
- 提升层：工作流 / 工具。

## r350B · 恢复路径由"失败分类"路由，重试不是第一招（来源：docs.openclaw.ai/concepts/model-failover，2026-10-02 r350B 实拉 319,996B）

- **★先判失败类别，再选恢复手段**：临时性限流/供应商故障 → 有界同模型恢复（重试，重试状态带 wait 与 attempt 计数）；供应商在 failover-worthy 错误下耗尽 → 轮换 auth profile / 冷却规则 → 才推进到候选链上的下一个模型。判据：**重试是"同一配置下再试一次"，轮换与降级是另一档动作**，混用会让"换了模型才碰巧成功"被记成"重试有效"。
- **★有些失败必须保留原分类、不得改参数重试**：模型/账户限制、以及"与该请求无关的 unsupported option"，保持原始失败分类并按 fallback 策略走；文档明确 **不会用关闭 thinking 的方式对这类错误重试**。判据：**为了跑通而悄悄降级请求参数 = 把失败伪装成成功**，归因时必须留原分类。
- **★候选链由"选择来源"决定**：配置默认值、cron 主模型、自动选中的 fallback 各自可用不同的 fallback 策略。判据：**同一模型在不同选择来源下，可用降级路径不同**——排查"为什么这个任务没有降级"先看它从哪条路径选中的模型。
- 提升层：工具 / 工作流。

## r350B · 执行序的隐性来源：几何位置与版本分叉（来源：docs.n8n.io/build/flow-logic/understand-execution-order，2026-10-02 r350B 实拉 515,463B）

- **★分支执行序随版本语义分裂**：n8n 1.0 之前 = 逐层推进（所有分支的第 1 个节点 → 再所有分支的第 2 个节点）；1.0 起 = 逐分支跑完（一个分支到底再下一个）。判据：**"多分支谁先跑"不是规范保证的常量**，升级运行时可能静默改写业务时序。
- **★分支顺序取画布几何**：自上到下，同高度则左优先；可在工作流设置里改。判据：**画布布局是执行序的一部分**——拖动节点会改变运行语义，代码评审看不出来。
- 排查顺序：出现"偶发时序错乱" → 先确认运行时版本与执行序模式 → 再看画布几何 → 最后才看业务代码。
- 提升层：工具 / 工作流。

> 早期三节（r350B 保序与并发 / r350C 限流多组预算 / r350C 重试粒度与失败类别预算）已零删减下沉至 references/knowledge-base.md 的 r417-dl 存档节。
## r351B · 扩展点是"观察者"不是"拦截器"：写入成功 ≠ 投递成功（来源：docs.openclaw.ai `automation/hooks/writing-hooks.md` 10,721B，2026-10-02 r351B 独立 curl 实拉逐串命中）

- **★返回值三不：不阻塞、不取消、不改写**：原文 "Returned values **do not block, cancel, or rewrite** the operation."。判据：排障时别把事件钩子当成熔断/拦截点——想在钩子里"返回 false 掐掉这次操作"是无效设计；真要拦截必须走宿主提供的专用否决通道。**这条决定了"为什么我的钩子没生效"的第一类答案：生效了，但它本来就没有阻断权。**
- **★context 是观测快照，唯一可写例外要显式点名**：原文 "Treat context as an **observation, not a live state-editing API**... **patch events carry cloned snapshots**. The **explicit mutable exception** is `agent:bootstrap`'s `context.bootstrapFiles`."。判据：**往 context 里改字段默认不产生任何效果**（且 patch 类事件给的是克隆副本），只有被点名的那一个例外可写。排查"改了没反应"时，先确认写的是不是那个唯一例外。
- **★同一个写入点，投递语义按生产者分档**：`event.messages` 原文 "is **not a general send-message API**"——表列四档：chat 命令会 await 并尝试回复；Gateway 会话 reset/create 的 RPC "messages are **not routed as chat replies**"；压缩事件交给调用方的回调投递；**其余核心事件（含 `/stop`、自动 reset、bootstrap、patch、Gateway 生命周期）"Ignored as replies"**。判据：**推送成功不等于送达**；且"缺失收件人/不支持的路由/发送策略/投递失败"任一都能让回复静默消失。
- **★时序早于 settle 才算数**：原文 "Append messages **before the handler's promise settles**; detached work that pushes later can **miss the producer's delivery step**."。判据：异步尾巴里补写的消息会静默丢失——这类丢失无任何报错，是典型的"偶发不发"根因。
- **★禁用 ≠ 移除，放置 ≠ 生效**：原文 "**Disabling leaves the files in place**"；放 workspace 目录的钩子须显式启用，且 "Workspace placement is **not an agent sandbox or a guarantee that the Gateway will load** that workspace's hooks"。判据：排查残留行为时，被禁用的钩子文件仍在磁盘上（可能被别的机制重新发现）；排查"没加载"时，先查放置位置是否被宿主承认，而不是查代码逻辑。
- 排障顺序：① 该扩展点是否有阻断权 → ② 写的是否为唯一可写例外 → ③ 该生产者是否把这次写入计入投递 → ④ 写入发生在 settle 前还是后 → ⑤ 文件是否被宿主发现（放置位）与被启用（禁用留文件）。
- 提升层：工具 / 工作流。触发词：返回值不阻塞、观察式契约、唯一可写例外、克隆快照、写入不等于投递、settle 前写入、禁用留文件、放置不保证加载。

## r352B · 重放的两副面孔：它跑的是「旧输入 + 当前版本」，且变量取当下值不是当时值（来源：help.make.com `scenario-run-replay.md` 9,556B，2026-10-02 r352B 独立 curl 实拉逐串命中；与 §数据钉定 / §局部执行 互补——那两条管"把输入钉住、把范围收窄"，本条管"拿历史真实输入重跑时到底复现了什么"）

- **★重放 = 旧触发数据 × 当前版本代码，且流经全部模块**：原文 "a **current version** of a scenario runs using the **trigger data of a previous run**… That data **passes through all modules, even those that ran successfully**."。判据：**重放验证的是"修好的新版本能不能吃下旧输入"，不是"复现当时那次失败"**；而全模块重跑意味着**原本成功的副作用（发信、写库、计费）会被再执行一次**——回填型重放必须按副作用清单过一遍，调试型重放则应收窄到待测段（走 §局部执行）。与 §已完成步不重放 不矛盾：那条禁止的是"整流重试"把成功步重跑，本条说的是回填场景**故意**全跑，代价要显式认。
- **★重放不是时光机：可变量取"最新值"而非当时值**：原文存三样 = trigger output data / scenario inputs / "**the most up-to-date** variable value (**values from previous runs are not preserved** if updated during or since these runs)"。判据：**输入被快照了、环境没被快照**——凡依赖全局变量/配置/外部状态的流程，"同样输入跑出不同结果"不要先怀疑代码，先确认这些可变量在这期间变过没有。想要真正可复现，必须把可变量一起钉进快照，光留触发数据不够。
- **★重放能力要附「不可重放清单」与分场景入口**：原文 "**Run cannot be replayed**" 因两类 run 不入库——**Check run**（轮询触发器无新数据的检查运行）与 **Single module run**。入口分两个：Builder 内 *Run with existing data* 用于边建边测，History / Run details 里 *Replay run* 用于错误恢复与数据回填（不需要进 Builder）。判据：**声明"哪些运行没有存"与"从哪进"是重放功能的一部分**；排查"为什么这条不能重放"时，第一件事是核它是不是那两类不入库的运行，而不是查权限。
- 排障顺序（重放相关）：① 这次重放跑的是当前版本还是当时版本 → ② 变量取的是当下值还是当时值 → ③ 全模块重跑的副作用是否已清点 → ④ 该运行是否属于不入库类型。
- 提升层：工具 / 工作流。触发词：重放、replay、旧输入新版本、回填、变量取最新值、不可重放清单、Check run、Run with existing data、Replay run。


## r353A · 确认不是一个动作：ack ≠ transcript commit ≠ 被模型读到（来源：docs.openclaw.ai `plugins/codex-harness-runtime/queue-and-feedback` 4,065B，2026-10-02 r353A 实拉）

- **★三段确认语义互不蕴含**：`turn/steer` 的 acknowledgment **不代表 transcript commitment**；"A message sent to Codex without a confirmed transcript commit is **not replayed automatically**"；而 commit 只证明输入**进入了历史**，"does not prove that a subsequent model request has read it"。判据：**收到 ack 只能说"送达了"，说不了"存下了"，更说不了"生效了"**——排查"我明明发了但没执行"要按这三段分别取证，不能停在 ack。
- **★观测面降级只投运维通道，不回落给用户**：Codex 保存诊断日志失败时，只在 **Gateway logs 记 warning**；每条 native notice **收到即记一次**，不按共享该 app-server 的每个会话重复广播；operator-only，**不回落 chat**；"a logging failure never interrupts the native connection"，且该告警**既不修复原生日志故障，也不代表会话状态丢失**。判据：**日志系统自身的故障是"静默降级"而非"抛错"**——看不到日志 ≠ 没有故障；同时它保证不影响主链路，所以不能靠"业务还在跑"反推日志健康。
- 排障顺序（确认相关）：① 有没有 ack → ② 有没有 transcript commit（无 commit 则不会自动 replay）→ ③ 是否有后续模型请求真的读了它 → ④ 若怀疑日志缺失，先去运维通道查 warning，不要以 chat 无提示为证据。
- 提升层：工具 / 工作流。触发词：确认语义、ack、transcript commit、自动重放、诊断日志失败、operator-only。


## r353B · 日志落点会回退、低级别日志结构性降质、"跳过"不等于有人在等（来源：docs.openclaw.ai `gateway/logging` 23,470B + `concepts/queue-steering` 12,731B，2026-10-02 r353B 实拉）

- **★日志路径不保证稳定**：默认滚动日志在 `/tmp/openclaw/`（每天一个、按网关主机本地时区命名，命名 profile 另加前缀）；**若该目录不安全或不可写（属主错误 / world-writable / 是 symlink）则回退到用户级 `os.tmpdir()` 路径**，且"On Windows it **always** uses that OS-tmpdir fallback"。判据：**取证不能硬编码日志路径**——先解析实际落点；Windows 上默认就在 tmpdir，清理临时目录会直接清掉日志。
- **★低级别日志为省开销主动降质**：`trace` / `debug` / `info` / `warn` 记录**省略调用点元数据 `_meta.path`**（避免每条常规消息都抓取并解析栈），只有 `error` / `fatal` 保留；开启 diagnostics 且有内部消费者订阅时**所有级别都保留**。判据：**warn 级记录天然缺少定位信息，这是设计而非缺陷**——要靠 warn 定位必须临时开 diagnostics，不能指望常规日志自带调用点。
- **★"工具被跳过"不等于"有用户消息在等"**：被跳过的调用仍会收到配对的 start/end 事件与合成结果（`Skipped to process an incoming message.`），但**内部更新（如子 agent 完成报告）走同一个转向边界**，它们"can be hidden from the chat transcript and do not appear in the user message queue"。判据：**看到 Skipped 只能推出"有内部更新进来"，推不出"用户在催"**；把它当作用户行为信号会误判排队原因。
- 排障顺序（日志/信号相关）：① 日志实际落点（是否回退到 tmpdir）→ ② 该条记录的级别是否自带调用点（warn 以下没有）→ ③ Skipped 事件先按内部更新解释，再按用户消息解释。
- 提升层：工具 / 工作流。触发词：日志回退、tmpdir、_meta.path、warn 降质、Skipped 合成结果、内部更新走同一边界。


## r354B · 重试解决瞬时故障、熔断解决持续故障：两者必须成对配置，且熔断默认关（来源：docs.n8n.io `use-environment-variables/executions.md` 独立 curl 取 `.md` 原文，2026-10-02 r354B 实拉）

- **★"反复崩溃自动停用"是一个有默认关闭的熔断开关**：`N8N_WORKFLOW_AUTODEACTIVATION_ENABLED` 默认 `false`，`N8N_WORKFLOW_AUTODEACTIVATION_MAX_LAST_EXECUTIONS` 默认 `3`（"Number of crashed executions before unpublishing a workflow"）。判据：**重试与熔断方向相反且必须成对**——重试把失败再试一次（适合瞬时抖动），熔断在连续失败 N 次后停止投喂（适合持续故障）；只配重试，持续故障会被变成"持续压力 + 持续产生垃圾执行"。
- **★熔断的判据是"最近 N 次"而非"累计 N 次"**：变量名 `MAX_LAST_EXECUTIONS` 指向最近窗口。判据：**连续性与累计性是两种不同的触发语义**——累计计数会让"偶发失败的老工作流"在时间拉长后必然被熔断；连续/最近窗口才对应当下的健康度。
- **★熔断动作是"下线（unpublish）"不是"删除"**：触发后工作流被取消发布而非移除。判据：**自动处置的默认动作应是可逆的停用**；让自动化拥有删除权，等于把误判的代价从"暂停"抬到"数据丢失"。
- **★阈值可配说明熔断强度是策略不是常量**：3 次是默认值而非固定值。判据：**把熔断阈值写死在代码里，等于让运维在"太敏感"和"太迟钝"之间没有调节余地**；阈值、开关、动作三者都应该是配置项。
- 提升层：工作流 / 可复用 Skill。触发词：重试与熔断成对、autodeactivation、最近 N 次、连续 vs 累计、熔断即下线、熔断阈值可配。

## r383A · 额度归属借用四元组与部分可用启动语义（来源：help.make.com worker group + docs.n8n.io external-secrets.md，2026-10-02 r374-Q-B 实拉；经 Qoder 提名）
- 额度模型必须写成「档位 + 借用公式 + 迁移连带 + 互斥组合」四元组：floor（预留）/ ceiling（软上限），未指派默认 `min(plan limit, group slots)` 可借用但被 clamp；换组会把等待中的运行一起搬走，预留与隔离互斥（code-only mode 对 grouped workers 被拒）。
- 依赖源不可用时把「启动是否放行」与「谁因此失败」分开定义：外部密钥源超时标 errored、后台递增延迟重连、startup continues without its secrets，而启动期用到该 secret 的 workflow 在首次拉取完成前失败；更新周期超时旧值继续可用——三者任一未写即为未定义行为。

## r383B · 审批第四终态：`withdrawn` 与 `rejected` 主体相反（来源：activepieces.com 审计事件枚举，2026-10-02 r379-Q-A 实拉；经 Qoder 提名）
- 撤回不得触发驳回分支、不得留授权副作用；合并会污染拒绝率与再触发谓词，须作为独立终态分列。

## r383C · 采样的异常保留例外（来源：activepieces setup-opentelemetry.md + docs.openclaw.ai diagnostics/flags.md，2026-10-02 r381-Q-C 实拉；经 Qoder 提名）
- 按比例丢弃的通道必须显式声明保留谓词：`AP_LOG_SAMPLE_RATE_INFO` + `AP_LOG_KEEP_SLOW_MS`（慢必留、error 免采样）；对偶 = OpenClaw diagnostics flags「单子系统开额外日志而不全局抬 level」。

## r385B · 诊断/修复工具要分清「检查面」与「修复面」，并把「跳过」做成一等结果（来源：docs.openclaw.ai `gateway/doctor/running` 242,314B 独立 curl 实拉，2026-10-02；经 Qoder r388-Q-C 提名并纠错）
- **★检查项出现 ≠ 修复项存在，两个面是不同集合**：原文「Some lint findings are **intentionally diagnostic only**, so **a check appearing in `--lint --all` does not mean `--fix` will mutate that area**. The contract separates `detect()` (reports findings) from `repair()` (reports changes/diffs/side effects), which keeps a path open for a future `doctor --fix --dry-run` **without turning lint checks into mutation planners**」。判据：**把检查器顺手升级成修复器，会让"报出来"隐含"能修好"**——自愈类工具必须分别声明检查面与修复面，且允许只报不修；与 §r336A「诊断只读 / 修复须批准」分工：那条管**读写权限分离**，本条管**两个面的集合关系**。
- **★"跳过"是一等结果，必须与"运行"分列计数，否则 0 结论不可信**：机读信封给出 `checksRun` / `checksSkipped`：「counts (**skipped by profile, `--only`, or `--skip`**)」，且 `ok` 只表示「whether any finding met the selected severity threshold」。判据：**`findings` 为空有两种完全不同的含义——真的干净 / 全被跳过**；不报 `checksSkipped`，"0 问题"就是不可判的。与 §r354C「采集结论三态 命中/缺位/未达」同族：那条管**采集面**，本条管**执行面**。
- **★无人值守档只做 safe 动作，需人确认的动作是"显式跳过"而不是"静默降级为已修"**：`--non-interactive`「applying only **safe migrations** (config normalization + on-disk state moves). **Skips restart/service/sandbox actions that need human confirmation**. Legacy state migrations still run automatically when detected」；`--fix` 才含「workspace setup, session stores, exec approvals, and audit schema migrations」，`--fix --force` 才是激进档。判据：**非交互执行必须列出"这一档不做什么"**，否则运维会以为跑过一遍就修全了——被跳过的动作要留在报告里，不要从结果中消失。
- **★取消不能留下半截修复**：「Once started, Doctor finishes and releases its resources **before a cancelled caller settles**, so **cancellation cannot abandon an in-progress repair**」。判据：**可中断的修复工具必须先声明中断语义**——要么跑完再响应取消，要么整体回滚；把取消当成"尽力而为"会在修复类操作上留下半写状态。
- 判非（纠正 Qoder 转述）：本页**未检索到** `repaired/skipped/failed` 三态枚举与 `HealthFinding[]` 类型名（grep 0 命中），故该表述不作为判据引入；仅落上列可实证的四点。
- 提升层：工具 / 工作流 / 可观测性。触发词：检查面与修复面、检查项不等于可修复项、checksSkipped、0 findings 不可判、non-interactive 只做 safe migrations、显式跳过、取消不半截修复。

## r385C · 断点恢复必须写读双侧对称：存不存的判据是「能不能回校验」，且只修写侧救不了存量病灶（来源：api.github.com/repos/langflow-ai/langflow/pulls/15241 26,494B JSON 独立 curl 实拉，merged=true，标题「fix(checkpoint): drop model state that cannot be validated back on resume」，2026-10-02 实拉；经 Qoder r389-Q-A 提名）
- **★「序列化没报错」不是「能恢复」的证明**：原文根因段「`serialize_value` treats "`model_dump(mode="json")` did not raise" as **proof that a model round-trips**」——上游 langchain-core 1.6.1 让 `BaseTool` 的 dump 从抛异常变成成功，但 pydantic 把 `func` 与 `coroutine` 两个字段**静默降级成 `repr`**，于是「**the dump *succeeds* — and pydantic **silently degrades** the two fields it still cannot represent ... **with no warning**」；落库后 `_restore_model` 在恢复时 `model_validate` 永久抛 `callable_type`，「The pause is durable, so **the run is stuck for good**」。判据：**写盘的通过判据必须是往返校验（dump → re-validate → 同一 model），不是"没抛异常"**；上游一个版本升级就能把"抛"变成"静默降级"，让原本正确的判据失效。
- **★写侧丢弃与读侧恢复要对称，且读侧必须能降级**：修复是双侧——写侧「only encode a model when its dump **validates back into the same model**. This makes the drop **symmetric with `_restore_model`** — anything that would raise on resume is **dropped at write time** instead, and the rebuilt component re-derives it」；读侧「a stored payload that no longer restores **degrades to `None` instead of raising**, and its vertex joins `checkpoint_opaque_dropped_ids` so the existing fixpoint re-runs it」。判据：**只改写侧，库里已经毒化的数据不会自愈**——原文点明「Without this, **runs already paused on an affected install stay stuck after upgrading**, because the poisoned checkpoint is already in the database」。恢复路径的改造必须**新数据（写侧）+ 存量（读侧）**成对出场，否则升级本身成为新的失败源。
- **★丢弃不是丢数据，是让可重建物回到重建路径**：被丢弃的顶点进入 `opaque-dropped: ['chat_input']`、`resume layer: ['chat_output']`，恢复后由重建重新派生。判据：**对"可由重建重新得到"的状态，丢弃严格优于带着坏值继续**——与 §r325A「有重建器的子系统不该备份，陈旧副本严格劣于空库」同族：那条管**备份**，本条管**检查点里的单个状态项**。
- **★回归测试要能对"所有上游版本"都失败，才算覆盖了这一类 bug**：三个回归测试中关键的一条「**Fails on the CI-pinned 1.5.1 without the fix**, so CI now covers this class of bug **regardless of which langchain-core resolves**」；并注明该 bug 之所以没被 CI 抓到，是因为「This repo and CI are **pinned to 1.5.1** ... a clean install today resolves 1.6.3」。判据：**CI 绿可能只是因为锁到了旧版本**——验证一个与上游解析相关的修复时，要证明测试在旧版本与新版本上都能复现失败。
- 提升层：工作流 / 工具。触发词：序列化成功不等于可恢复、往返校验、写侧丢弃与读侧降级对称、checkpoint_opaque_dropped_ids、存量毒化不自愈、CI 绿只是锁了旧版本。

## 相关量不能替代身份：证据缺失时返回 unknown，禁止从元数据反推绑定（来源：docs.openclaw.ai/gateway/audit.md 37,793B，2026-10-03 r388B 独立实拉）
- **原文**：「Because `runId` is correlation rather than execution identity, it never substitutes for the owner-local binding.」「The inspector never infers a binding from session metadata, timestamps, or retained context counts.」「An unreadable row is `unknown`, never reconstructed.」「the retry never manufactures replacement evidence.」
- **判据**：① **区分「相关量」与「身份量」**——runId / 会话 key / 时间戳 / 上下文条数 都是路由与恢复用的相关量，可以缩小候选但**不能证明归属**；排障时把它们当身份证据会得出「就是这个执行」的假结论。② **不可用 ≠ 反面结论**：读不出来的行（corrupt / missing / malformed / mismatched）一律判 `unknown` 并给出补救动作，不许从相邻记录补齐、不许用「只保留了一条上下文所以必然是它」这种计数推理。③ **重试不制造替代证据**——恢复路径若原证据丢失，就明确「精确核查不可用」，而不是拿新进程的身份补上；补上的那一刻证据就变成了伪造。
- 提升层：工作流 / 可复用 Skill。触发词：相关量≠身份、runId 不是执行身份、不推断绑定、unknown 不重建、重试不补证据、证据补救动作。

## 「能解析」不等于「干净」：优先级漂移与残留是两类独立故障；门禁退出码要分「有发现」与「不可用」（来源：docs.openclaw.ai/cli/secrets.md 16,115B，2026-10-03 r388C 独立实拉）
- **原文**：审计发现码 `PLAINTEXT_FOUND` / `REF_UNRESOLVED` / `REF_SHADOWED` / `STORE_PLAINTEXT_RESIDUE` / `LEGACY_RESIDUE`；「precedence drift (auth profile store credentials shadowing `openclaw.json` refs)」「store residue (a team store value duplicated by plaintext in `openclaw.json`)」；「`audit --check` returns `1` on findings. Unresolved refs return `2` (regardless of `--check`). Store validation and disclosure-policy failures return `2`.」
- **判据**：① **配置「能取到值」不代表取的是你以为的那份**——同名值存在于多个存储时，命中哪个由优先级决定而不是由你刚改了哪个决定（auth profile 会遮蔽配置里的 ref）；排查"改了没生效"必须把"该名字在几个地方存在、谁优先"当成第一问。② **残留与遮蔽是不同的故障，处置动作不同**——残留是"同一份值既在安全存储又在明文里"（要删明文），遮蔽是"高优先级处有一份旧值"（要清理或对齐）；混为一谈会只清一半。③ **门禁退出码必须把"有发现"与"不可用"分开**——`1`=有发现（可处置）、`2`=未解决/校验失败（结论不可用）、目标不存在另给码；CI 里把所有非零当同一种失败，会让"这次审计本身没跑成"被当成"这次审计没发现问题"。
- 提升层：工作流 / 可复用 Skill。触发词：能解析≠干净、优先级漂移、REF_SHADOWED、残留 vs 遮蔽、退出码 1 vs 2、审计没跑成≠没发现问题。


## 联邦身份撤销不同步 + 全局命名空间先到先得 + 迁移通道的丢失面（来源：docs.n8n.io `verify-user-identity/use-saml/manage-users-with-saml.md` 1,830B + `follow-best-practices.md` 2,455B，2026-10-03 r390A 独立 curl 取 `.md` 原文实拉）
- **原文**：「If you **remove a user from your IdP, they remain logged in to n8n**. You need to manually remove them from n8n as well.」；「Webhook paths must be unique across the entire instance... **The path works for the first workflow that's run or published. Other workflows will error** if they try to run with the same path.」；「To move workflows between accounts, export the workflow as JSON, then import it to the new account. **Note that this action loses the workflow history.**」；另：「n8n recommends that owners create a member-level account for themselves. Owners can see all workflows, but **there is no way to see who created a particular workflow**」。
- **判据**：① **身份联邦的撤销不会级联到本地会话**——上游（IdP）删人，本地已登录会话照旧；撤销动作必须在两端各执行一次，只做上游等于没撤。排障"人已离职却还能操作"先查本地会话与本地账号，不要只看 IdP。② **全局命名空间的冲突表现是"先到先得 + 后来者报错"**，不是"后者覆盖前者"：第一个跑/发布的占住路径，其余同路径工作流报错 ⇒ 遇到"路径莫名不可用"先查是否已被别处占用，而不是查本条配置。③ **迁移通道必须显式声明丢失面**：导出 JSON 再导入会丢掉工作流历史；凡"导出—导入"式迁移，输出里要写明丢了什么，否则使用者会把"迁移完成"当成"完整搬过去了"。④ **高权限账号做日常编辑会切断归因链**：owner 能看全部工作流但无法追溯创建者，也就无法判断正在改的是谁的成果 ⇒ 排障与评审都要回退到"用成员级账号改、用高权限账号管"。
- 提升层：工具 / 工作流。触发词：IdP 删人本地仍在、联邦撤销不同步、webhook path 全局唯一、先到先得、导出丢历史、owner 归因链断裂。


## 会话新鲜度锚定「起点」不是「最近写入」；只差大小写的 ID 会分裂会话与记忆；隐私会话过期即删不归档（来源：docs.openclaw.ai/concepts/session 22,767B，2026-10-03 r390B 独立 curl 取 `.md` 原文实拉）
- **原文**：「Daily reset (`mode: "daily"`) - opt into a new session at a configured local hour… **Daily freshness is based on when the current `sessionId` started, not on later metadata writes.**」；「IDs that differ only by case identify different conversations.」；incognito「The thread expires 24 hours after creation or when the Gateway restarts, whichever comes first. **Activity does not extend its lifetime.** Expiry **stops active work and deletes the session and transcript without an archive**.」；另：「Channel docking and manual cross-channel reply focus have been removed. The `/dock-*` commands no longer move a session's reply destination… neither restores manual cross-channel docking.」
- **判据**：① **"这个会话是不是新的"要看会话起点，不看最后一次活动**——日常重置基于 `sessionId` 起始时刻，后续元数据写入不算；把"刚活跃过"当成"刚创建"会把续跑的会话误判成新会话，进而复跑冷启动流程。② **身份标识的大小写与规范化要在入口定死**：只差大小写的 ID 被当成不同会话 ⇒ 表现为"记忆/上下文莫名少一半"。排查这类问题先比对 ID 的字面归一化，不要先怀疑存储或召回。③ **临时/隐私类会话的过期是硬过期且不归档**：活动不延长寿命、到期停止在跑的工作并删除 transcript 无存档 ⇒ 凡"用完即焚"的运行面，设计时必须声明"活动不续期"与"无归档"，否则使用者会以为"还在用就不会丢"。④ **已退役能力不会因习惯而复活**：通道停靠已移除，命令不再移动回复目标，也没有替代开关 ⇒ 排障"命令怎么没反应"要先查该能力是否已在当前版本退役，而不是查参数写没写对。
- 提升层：工具 / 工作流。触发词：会话新鲜度、sessionId 起点、大小写分裂、硬过期不续期、无归档、能力已退役、dock 命令失效。


## 「有错误」不等于「有可重试记录」：四类错误不产生实体；自动重试是白名单不是黑名单，并发上限保护的是下游（来源：help.make.com `errors-that-dont-create-incomplete-executions.md` 1,401B + `automatic-retry-of-incomplete-executions.md` 5,663B，2026-10-03 r390C 独立 curl 取 `.md` 原文实拉；与 §重试与熔断成对 互补——那条管熔断何时介入，本条管哪些错误根本没进重试体系）
- **原文**：不产生 incomplete execution 的四类——「When the error happens on **the first module** in the scenario. However, you can add the **Retry** error handler to the first module… Make stores the incomplete execution even when the first module outputs an error.」；「When your **incomplete executions storage is full**… If the data loss is disabled, Make **disables the scenario**. If the data loss is enabled, Make keeps scheduling scenario runs and **discards the incomplete execution**」；「When the scenario runs longer than the scenario run **duration limit**」；「When an error happens during the **initialization or rollback scenario phase**… there is no incomplete scenario run.」；自动重试只对 `RateLimitError` / `ConnectionError` / `ModuleTimeoutError`「**Other error type usually require changes in the incomplete execution and manual resolving. Make doesn't retry these error types automatically by default.**」；退避阶梯 1m→10m→10m→30m→30m→30m→3h→3h（约 7h51m 收尾）；「the retry **doesn't start when the original scenario is running already**」；「there is a limit of **3 incomplete execution retries running in parallel**… This limitation is to prevent your scenarios from getting **follow-up rate limit errors**」。
- **判据**：① **错误留痕有一份"不覆盖清单"，且它决定补偿机制的真实覆盖率**：首模块错、存储满、超长运行、初始化/回滚阶段错——这四类错发生了但**没有可重试实体**。设计任何"失败会自动重试"的承诺时，必须先公布不覆盖清单，否则"我们会自动重试"在四类场景下直接落空。② **可观测面的缺口可以用配置补**：首模块默认不存，挂上 Retry handler 才存 ⇒ 可观测性是配置项不是默认值，想要覆盖就得显式打开。③ **自动重试按错误类型白名单**，只对"外部暂时性"三类（限流/连接/超时）自动，其余交人工 ⇒ 把"会自动重试"说成通用能力是错的表述。④ **重试的并发上限动机是保护下游不是保护自己**：原文明确限 3 是为避免重试本身触发下游限流；且**重试不与本场景自身的运行并发**（避免自相干扰）。⇒ 调重试并发时先问"下游扛得住吗"，不是"我们并发还能再高吗"。
- 提升层：工作流 / 工具。触发词：不产生 incomplete execution、首模块错误、存储满丢记录、初始化回滚阶段无记录、重试白名单、退避阶梯、重试并发上限保护下游、不与自身运行并发。

## 审计分层视图会收窄可见面：团队视图看不见组织级事件，因此窄视图无法自证「上层没动过我」（来源：help.make.com `audit-logs.md` 8,460B，2026-10-03 r390C 独立 curl 取 `.md` 原文实拉）
- **原文**：「Organization Audit logs are visible only to organization owners and admins.」；「Team audit logs are available to team admins.」；「**Some of the events are not visible in the team audit logs.** For example, you won't see events about organization variables, but you will see events connected to this specific team」；「you can see what was changed, who made the change, when it was made, and for which scenario」；「Audit logs are stored for 12 months.」
- **判据**：做分层审计（组织级 / 团队级 / 项目级）时，**下层视图天然缺少影响它的上层事件**（组织变量变更在团队视图里不存在）。⇒ 结论不能从单一层级的日志得出：**"本团队日志里没有变更"不能证明"没有任何影响本团队的变更"**，跨层比对才是完整的；排查"谁改了我的配置"必须带上层视图。
- 提升层：可观测性 / 治理。


## 「为什么这条没被脱敏」先要分清是哪一面：用户规则是替换、内置规则始终生效、工具负载是合并——三面语义各不相同（来源：docs.openclaw.ai `gateway/config-observability.md` 10,454B，2026-10-03 r391A 独立 curl 取 `.md` 原文实拉；与 §脱敏保留可观测骨架 互补——那条管脱敏后还能不能排查，本条管脱敏规则之间的覆盖关系）
- **原文**：「`redactPatterns`: regexes for best-effort masking of console output, file logs, OTLP log records, and persisted session transcript text. Setting this **replaces** only the default string regex list for log and transcript output. **Built-in form-body, structured auth-header, and bare AWS key protections always apply.** Tool payload redaction is **separate and always merges your patterns with the default string list.**」；「Redaction is always on and is **no longer configurable** … **UI, tool, and diagnostic safety surfaces redact secrets independently of this policy.**」
- **判据**：① **脱敏不是一个开关而是三个面，覆盖语义还不一样**：日志/转录面用户正则是**替换**默认列表（配了就只认你的）；内置的表单体、结构化 auth 头、裸 AWS key 保护**永远生效**（配置改不掉）；工具负载面是**合并**（你的 + 默认的）。⇒ 排查"这条密钥怎么出现在日志里"时，先定位属于哪一面：替换面漏了是自己配置的锅，合并面漏了才是系统缺口。② **"脱敏可配置"这个前提本身可能是过时的**：原文明确脱敏已常开且不可关，UI/工具/诊断三个安全面**各自独立**脱敏，与用户策略无关。⇒ 把"我关掉了脱敏"当成某处泄露的解释前，先确认它还是不是可关的。③ **观测开关同时是敏感度开关**：OTel 的 `captureContent` 默认关，打开才会把消息、工具与工具定义内容写进 span 属性（provider 内部 thinking 仍排除）。⇒ 为了排障临时打开观测内容捕获，等于临时把数据敏感度提高一档，收工时要有复位动作。
- 提升层：可观测性 / 工具。触发词：redactPatterns 替换、内置保护始终生效、工具负载合并、脱敏三面、captureContent 默认关、观测即敏感度。

## 排查要取「生效面」而不是「配置面」：诊断命令是权威来源，拒绝事件有专属审计条目，日志路径会随平台漂移并被轮转清掉（来源：docs.openclaw.ai `gateway/sandbox-vs-tool-policy-vs-elevated.md` 9,792B + `gateway/sandboxing.md` 8,613B + `gateway/config-observability.md` 10,454B，2026-10-03 r391A 独立 curl 取 `.md` 原文实拉；与 §相关量≠身份量 互补——那条管别拿相关量当归属证据，本条管别拿配置值当生效值）
- **原文**：「`openclaw sandbox explain …` inspects **effective sandbox mode, host workspace, runtime workdir, Docker mounts, tool policy**, and fix-it config keys. Its `workspaceRoot` field remains the **configured** sandbox root; `effectiveHostWorkspaceRoot` shows **where the active workspace actually lives**.」；拒绝留痕「Gateway logs include **`agents/tool-policy` audit entries** when a tool policy step removes tools or a sandbox tool policy blocks a call. Use `openclaw logs` to see the **rule label, config key, and affected tool names**.」；日志路径「Default log file: `/tmp/openclaw/openclaw-YYYY-MM-DD.log` … When `/tmp/openclaw` is unsafe or unavailable (**and always on Windows**), OpenClaw uses a directory under the OS temp dir instead: `openclaw-<uid>` … **Dated log files are pruned after 24 hours.**」；轮转「`maxFileBytes` … default: `104857600` = 100 MB … keeps up to **five numbered archives**」；信号隔离「Protocol validation is **isolated per signal**, so an unsupported resolved value **disables that signal's OTLP exporter without blocking supported sibling signals**.」；「`openclaw sandbox recreate … --force` removes containers/environments so they get recreated with **current config on next use**.」
- **判据**：① **配置值与生效值要分成两个字段输出**：`sandbox explain` 同时给 `workspaceRoot`（配置的）与 `effectiveHostWorkspaceRoot`（实际生效的），还标出每条工具策略**来自 agent / global / default 哪一层**。⇒ 排查"为什么不在我配的位置/为什么这条规则生效"，读配置永远不如读 explain；复现问题时的第一条命令应是诊断命令而不是 `cat` 配置。② **拒绝类事件有专属审计条目，且条目里带定位三件套**：`agents/tool-policy` 会记下**规则标签 + 配置键 + 受影响工具名**。⇒ 遇到"工具被拦"不要猜，直接查该条目；日志里没有它就说明拦你的不是策略层（可能是沙箱层或权限层）。③ **日志会漂移也会消失**：默认路径在 `/tmp/openclaw`，Windows 与不可写时落到系统临时目录的 `openclaw` / `openclaw-<uid>`；按日文件 **24 小时后被清**，活跃文件 100MB 轮转留 5 份。⇒ 取证第一步是确认"当时写到了哪个路径、现在还在不在"，晚一天就什么都没有。④ **部分失效不该拖垮整体，但要能看出是哪一部分坏了**：OTel 协议校验按信号隔离，一个信号协议不支持只禁用它自己的导出器，兄弟信号照常。⇒ 排查"为什么没有 trace"时， metrics 还在不等于 trace 通道健康。⑤ **改了配置不等于生效**：容器/环境要 `sandbox recreate` 才会按当前配置重建。⇒ "我改了但没变化"这类工单，第一问是"重建了吗"。
- 提升层：可观测性 / 工作流。触发词：explain 生效值、配置值 vs 生效值、规则来源层级、agents/tool-policy 条目、日志路径平台漂移、24h 清理、100MB 五份归档、信号隔离、改配置要 recreate。


## 限流排查先看作用域再看数值；限额可以随令牌走；同一错误的「去重」是通道属性不是错误属性（来源：pipedream.com/docs `connect/api-reference/rate-limits.md` 2,732B + `workflows/limits.md` 9,083B + `workflows/building-workflows/errors.md` 9,150B，2026-10-03 r391B 独立 curl 取 `.md` 原文实拉；与 §重试与熔断成对 / §自动重试是白名单 互补——那两条管被限之后怎么退，本条管"限的是谁"与"告警为什么没响"）
- **原文**：限流表三列「Name | Endpoint | Request Limit | **Scope**」，如 `POST /token` 100/min **Per external user**、`GET|DELETE /accounts/*` 2,000/5min **Per project**、`GET /components/*` 3,000/5min **Per project**；自定义限额「Create a rate limit by specifying a time window and maximum requests allowed within that window. The API returns a **`rate_limit_token`** that you include in subsequent Connect API requests」→ 用法「Include the `rate_limit_token` in the **`x-pd-rate-limit` header**」；QPS「You can send an **average of 10 requests per second** … We'll also accept **short bursts** of traffic, as long as you remain close to an average of 10 QPS (e.g. sending a batch of 50 requests every 30 seconds should not trigger rate limiting) … you should retry the request with **exponential backoff**」；去重双语义「Pipedream only sends at most **one email, per error, per workflow, per 24 hour period** … If a different workflow throws a `TypeError`, you **will** receive an email about that.」但「Unlike the default system emails, **duplicate errors are sent to any workflow listeners**」；测试态「When you're editing and testing your workflow, any unhandled errors will **not** raise errors as emails, nor are they forwarded to error listeners. Error notifications are only sent when a **deployed workflow** encounters an error on a live event.」
- **判据**：① **限流描述必须带作用域，否则不可用于排查**：同一平台里 100/min 是 per external user、2,000/5min 是 per project——**同一个"被限"现象，在 per-user 作用域下是某个用户打爆，在 per-project 作用域下是全局配额耗尽**，处置完全不同。⇒ 记限流信息时固定三列：数值、端点、作用域；只抄数值等于没记。② **限额可以是"随令牌走"的运行时参数**：自定义限额返回一个 token，调用方把它放进 header 才生效 ⇒ **同一身份的两次调用可能适用不同限额**。排查"为什么这次被限、上次没有"时，除了看调用者，还要看这次带没带限额令牌、带的是哪一个。③ **限流是"平均值 + 突发容忍"，不是瞬时硬顶**：10 QPS 是平均值，50 条/30 秒的突发不算超限。⇒ 用瞬时峰值判断"有没有被限"会误判；压测与告警阈值要按窗口均值设计，被限后客户端承担指数退避责任。④ **告警静默不等于事件没有发生**：默认邮件按 (错误 × 工作流 × 24h) 去重，而自定义错误流**完全不去重**——同一次故障在两条通道上的可见性天差地别。⇒ 建告警体系时必须为每条通道单独声明去重语义；用"我没收到邮件"推断"没有新错误"是典型的错误推理。⑤ **测试态与生产态的错误通道是分开的**：编辑测试中的错误既不发邮件也不进错误流。⇒ 排查"为什么这个错误没人管"时，先确认错误发生在部署版本还是调试版本。
- 提升层：工作流 / 可观测性。触发词：限流三要素、per user vs per project、rate_limit_token、限额随令牌走、QPS 均值与突发、429 指数退避、每错误每工作流 24h、错误流不去重、测试态不告警。

## 限流要补问「副本语义」与「成功计不计入」；超时时钟只走活跃段；同步调用要分清「答错了」与「没回答」（来源：pipedream.com/docs/conduit/deploy/hardening.md 7,011B + www.activepieces.com/docs/install/reference/limits.md 6,779B，2026-10-03 r393A 独立 curl 取 `.md` 原文实拉；与 §限流排查先看作用域再看数值 互补——那条管"限的是谁"，本条管"多副本会不会放大"与"什么才写进计数器"）

- 限流器要问第四件事：计数器是共享还是 per-replica。认证失败类（登录、OAuth、MCP、SCIM）在 PostgreSQL tier **跨副本共享** ⇒ 跑 N 副本不会让凭据猜测者拿到 N 倍速率；其余限流器**故意 per-replica**（集群总速率≈N×单实例）⇒ 扩容前必须确认目标限流器属于哪一类，否则横向扩容等于放大攻击面。
- 只有失败写计数器，成功登录不写 ⇒ 护栏不该给正常行为制造状态，也不该让攻击者用成功请求探测计数；被限的认证失败会以 `rate_limited` 出现在指标里，是观测信号不是普通错误。
- 超时只计活跃执行时间：被 Wait for Approval / Delay 暂停的时段**不计入** run timeout ⇒ 人类审批挂在流程里不会烧掉执行预算；但"暂停生命周期"另有独立上限，是另一条时钟，两条都要声明。
- 同步 webhook 的状态码语义：流程跑失败**立刻** 500；只有超时窗口内从未产生任何响应才 408（仍在运行，或流程没有 Return Response 步骤）⇒ 500 是"答了但错了"，408 是"根本没答"，排障方向不同。

## 指标与审计是两条通道：会重置的那条不能承载必须精确的数；拒绝不产生耗时样本；认证失败要按 reason 分族（来源：pipedream.com/docs `conduit/deploy/monitoring.md` 9,842B + docs.openclaw.ai `gateway/config-gateway.md` 36,884B，2026-10-03 r393B 独立 curl 取 `.md` 原文实拉；与 §限流要补问副本语义 互补——那条管"限的是谁、会不会被扩容放大"，本条管"看到异常后该改哪里"）

- 指标在内存聚合、进程重启归零，是**设计如此不是缺陷**：原文明确"必须精确计量的东西（用量看板、审计日志）另行存在数据库里，与这些指标无关" ⇒ 验收计量类能力要先问"这个数会不会因为重启而丢"，答案是会就必须另有持久通道。
- 每个副本报自己的计数，聚合在查询侧做；histogram 跨副本必须 `sum by (le)` 才正确，直接取分位数会错。
- outcome 三态 `ok` / `error` / `denied`：**被策略拒绝的调用根本没跑，所以不产生任何耗时样本** ⇒ 延迟分布里看不到拒绝，算错误率时分母是"已执行的"而不是"被请求的"。
- 认证失败的 reason 要分三族，族不同改的地方完全不同：①凭据类（`missing_token`/`invalid_token`/`session_expired`/`org_ambiguous`）= 客户端凭据坏了或有人在猜；②客户端被拒类（`client_revoked`/`client_not_allowed`）= 工作区拒绝**有效令牌**的客户端（撤销了，或禁止动态注册客户端）；③登录策略类（`sign_in_*`）= 工作区的登录策略拒绝（provider 被禁用/删除、密码登录被关）。
- 拒绝率有正常基线："少量持续拒绝是正常的（客户端会探测看不见的工具）"，**策略编辑之后出现阶跃才是信号** ⇒ 与变更时间对齐看趋势，不要对绝对值告警。
- 限流器热更新时**已有状态延续**：失败记录、已赚到的锁定截止期都保留；同一 `{scope, clientIp}` 的失败尝试会先串行化再写，所以并发错误尝试的第二个就会触发限流 ⇒ 不要以为"并发能冲过去"。
- 本地回环豁免（`exemptLoopback`）必须显式声明：不声明时调试请求会进同一套失败计数，把调试噪声和攻击面混在一起。

## 同一个超时状态码下有两种命运；「提交成功」不等于「会单独跑一次」；404 与 204 指向两处不同配置（来源：docs.openclaw.ai `gateway/config-hooks.md` 36,853B，2026-10-03 r393C 独立 curl 取 `.md` 原文实拉；经 llms.txt/索引页定位；与 §有错误不等于有可重试记录 互补——那条管哪些错误根本没进重试体系，本条管已经拿到回执之后怎么解读）

- 503 不能一概读作"没跑成"：单跑模式下 15 秒内未准入，**那段排队工作被取消**；fan-out 模式下待处理工作**继续在后台执行**；网关暂停/重启也会返回 `503 gateway_unavailable` ⇒ 同一个码、三种后果，先分清提交模式再决定要不要重提。
- wake 回执的 `eventOutcome` 有两个值：`queued`（队列接受了这次唤醒）与 `coalesced`（同样的唤醒已经是队列里最近的待处理事件，被合并了）⇒ **"我提交成功了"不等于"它会单独执行一次"**，重复提交被合并是设计行为，验收时要读这个字段而不是只看 200。
- 404 与 204 是两种"什么都没发生"：404 = 没有任何 mapping 匹配到这个 hook；204 = 匹配到了但没产生任何动作 ⇒ 前者去查匹配条件，后者去查动作定义，方向完全不同。
- 重试前先分类：400 是 JSON/载荷/路由或投递选择不合法，**原文要求先读 `error` 字段再重试**；401 是 hook 鉴权失败；429 必须遵守 `Retry-After`；500 是 mapping/transform 抛异常（查网关日志）；502 是准入前的 agent 准备失败。


## 观测的陈旧窗口要写明秒数，且「负面结果不缓存」是独立设计；凭据状态要报「配置不可用」而非回落到正常态（来源：docs.openclaw.ai `gateway/config-secrets-env.md` 10,309B + `gateway/config-tools.md` 7,517B 索引页 + `gateway/config-tools/github-identity.md` 17,020B，2026-10-03 r395A 独立 curl 取 `.md` 原文实拉）

- **缓存窗口要给出具体秒数，并说明哪些面受影响**：成功的 `gh auth token` 读取会复用最多 **60 秒**（与凭据校验缓存对齐），因此 `gh auth login/logout/switch` 的变更**最多 60 秒后**才在这些读面可见；并发读共享一次原生查找 ⇒ 排查「改了没生效」时先算有没有落在缓存窗口内，别急着判定配置没写进去。
- **失败与「缺席证明」不缓存**：失败的 token 读取、以及「匿名访问不存在」这类否定结论**不进缓存**；环境 token、托管 profile 凭据、调用方权限、会话访问仍实时检查 ⇒ 若把否定结果也缓存，「暂时拿不到」会被固化成「确实没有」，这是两类完全不同的故障。
- **状态错误码不得降级**：托管 profile 缺失/无 token/损坏报 `configured_unavailable` 而不是改报原生账号；不可用的托管身份产生可操作错误而不是偷偷换凭据 ⇒ 排查时看到「还在正常工作」要先确认是不是已经静默切换到了另一套身份。
- **换身份不是即时吊销**：改选身份后，已准入的运行保留原 profile 选择，已启动的本地进程保留启动 token 直到退出、重启或 token 过期，而**新运行立即用新身份**；本地改动也**不撤销 GitHub 侧的授权**，要撤销得去 OAuth 应用设置单独做 ⇒ 撤销动作与生效动作是两个地方，声明里要分开写。


## 文档示例值不是内建默认值；单次超时与含重试的总等待是两个数；「0」可能是关闭也可能是无限制（来源：docs.openclaw.ai `gateway/config-tools/sessions-and-subagents.md` 9,632B + `gateway/config-tools/custom-providers.md` 13,129B，2026-10-03 r395B 独立 curl 取 `.md` 原文实拉）

- **示例值 ≠ 内建默认**：`runTimeoutSeconds` 内建默认 `0`（无超时），文档代码块里写的 `900` 是「常见的 opt-in 取值」而非默认值 ⇒ 排查超时相关问题时，先分清「文档里出现的数」与「不配时的默认值」，把示例抄进生产等于凭空加了一条超时。
- **单次超时 ≠ 含重试的总等待**：`announceTimeoutMs` 默认 120000 是**每次投递尝试**的超时，瞬时重试会让**总等待超过一次配置的超时** ⇒ 看到「超时设了 2 分钟却等了 6 分钟」不是配置没生效，而是重试次数没算进去。
- **同一个 `0` 在不同字段含义相反**：`runTimeoutSeconds: 0` 是**无超时**（放开），`archiveAfterMinutes: 0` 是**关闭自动归档**（收紧）⇒ 数值型开关的零值语义必须逐字段声明，不能靠一类字段的习惯去推另一类。


## 「改不了」先查字段归属方；两侧视图不一致时以记录持有方为准（来源：docs.n8n.io `security/enable-ssrf-protection.md` 3,822B + `security/block-specific-nodes.md` 2,425B + `basic-configuration/use-environment-variables/ssrf-protection.md` 7,039B + pipedream.com/docs `conduit/configure/access-control.md` 13,330B + `conduit/configure/scim.md` 9,789B，2026-10-03 r395C 独立 curl 取 `.md` 原文实拉；n8n 与 Pipedream 均经各自 `llms.txt`（287,049B / 34,240B）定位）

- **改不动某个字段，先查这个字段归谁**：被 SCIM 供给的人，其姓名**归目录所有**，本人改不了；工作区管理员只有在「工作区拥有该账号」时才可改名，条件三条同时成立——通过该工作区自己的 IdP 登录、未被 SCIM 供给、且不高于该管理员；而**后续 SSO 登录永不覆盖本人或管理员设定的姓名** ⇒ 排查「为什么改不了」的正确起点是「这个字段的归属方是谁」，不是「我的权限够不够」。
- **两侧视图不一致时，以持有记录的那一侧为准**：IdP 侧删掉 SCIM 资源后，IdP 读这个地址是 `404`，但平台侧记录仍然占着地址、仍然拒绝新的人 ⇒ 同步类故障要**两边各查一次**，只信其中一侧会得到完全相反的结论。
- **同步错误与审计都写明是人工介入场景**：官方把回收地址标注为「唯一需要人工介入的情形」，同步错误与审计记录都会提示 ⇒ 自动化同步要显式列出「哪些情况转人工」，否则会一直重试一个永远成功不了的动作。


## 诊断输出带执行环境前提；机器可读日志是独立开关；「拒绝执行」要显式声明成没跑（来源：docs.n8n.io `.../use-environment-variables/logs.md` 12,684B + docs.openclaw.ai `tools/exec-approvals.md` 39,387B，2026-10-03 r396B 独立 curl 取 `.md` 原文实拉）

- **诊断输出有环境前提，看不到不等于没执行**：`CODE_ENABLE_STDOUT` 默认 `false`，且置真后**只对 production executions 生效** ⇒ 同一段代码在手动执行与生产执行下可观测性不同；排查「为什么没有输出」的正确起点是**这个开关在哪种执行形态下生效**，而不是代码没跑到。
- **日志能不能被机器消费是独立开关**：`N8N_LOG_FORMAT` 默认 `text`，要一行一 JSON（含 message/level/timestamp/metadata）需显式设 `json` ⇒ 「有日志」不等于「可机读」，把日志接进监控/比对前先确认格式开关，否则下游只能解析人读文本。
- **拒绝类结果必须写成「没有执行」**：`SYSTEM_RUN_DENIED` 的语义是节点**拒绝执行**，官方特别说明它**不是「命令可能已运行」** ⇒ 凡返回拒绝，声明里要明确写出「未执行」，不能让调用方按「结果未知」去猜；配套地，迟到的批准无法重启已取消的那一轮 ⇒ 撤销的生效点在启动边界，批准不复活已终止的执行。


## 日志级别枚举里存在「静音」档；保留窗口是「单份大小 × 份数」的乘积（来源：docs.n8n.io `deploy/host-n8n/keep-n8n-running/set-up-logging.md` 7,738B + `.../use-environment-variables/logs.md` 12,684B，2026-10-03 r396C 独立 curl 取 `.md` 原文实拉）

- **最低档是「什么都不输出」，不是「只报严重错误」**：n8n 的级别枚举含 `silent`（outputs nothing at all），位于 `error` 之下 ⇒ 「一条日志都没有」可能是**合法配置**而未必是进程没起来或日志管道断了；排查零输出时先把级别档位读出来，再怀疑链路。
- **日志能留多久由两个上限相乘决定**：`N8N_LOG_FILE_SIZE_MAX`（单份 MB）与 `N8N_LOG_FILE_COUNT_MAX`（保留份数）共同构成保留窗口，且官方提示**使用 workers 时份数值必须设** ⇒ 「日志还在不在」算的是容量×份数的乘积，只调其中一个算不出保留时长；多进程形态下不设份数会互相覆盖。

## 观测沉降窗与「首读物化」：按物化时点而非开关翻转时点切存量；日志落盘有沉降延迟（来源：Qoder r399-Q/r400-Q 审计净新，2026-10-03；与 §诊断输出带执行环境前提 互补——那条管"看不看到"，本条管"看到的是哪个时点的"）

- **首读物化时点 ≠ 开关翻转时点**：配置/开关从"翻转"到"真正物化进存储/生效"之间有延迟，存量数据要按**物化时点**切，不能按开关翻转时点切——否则会把"已翻转但未生效"的数据算进新状态，或把"已生效但时点在翻转前"的算漏。
- **观测有沉降窗**：日志/指标从产生到可被查询存在延迟窗口，排障时"现在查不到"可能是还没沉降而非没发生；验收覆盖面要标清观测沉降窗，避免把延迟当成缺失。
- 提升层：诊断/观测。触发词：首读物化时点、物化时点切存量、观测沉降窗、开关翻转≠生效。

## 先落盘后转发的事件缓冲层：多写者会把缓冲变损坏源，恢复解析必须有上界；下游熔断按滑动窗口计数（来源：docs.n8n.io `administer/observe-and-log/stream-logs-to-external-systems.md` 23,919B，2026-10-03 r408A 独立 curl 取 `.md` 原文实拉）
- **原文**：① n8n 先把每个事件**持久化到本地 `n8nEventLog.log`** 再转发，文件**跨重启存活**，用于**重放尚未投递的事件**；默认按进程类型加 `-worker` / `-webhook-processor` 后缀。② 共享可写卷（queue mode workers 挂 NFS/EFS）下**多进程并发追加会交错或损坏文件，导致恢复失败与丢事件** ⇒ 必须给每个进程配 `N8N_EVENTBUS_LOGWRITER_LOGFULLPATH` 唯一绝对路径，且**一旦设置就不再自动加后缀，唯一性责任归编排方**；已存在的旧 `n8nEventLog-worker.log` 需**人工隔离**，系统不自动删。③ `N8N_EVENTBUS_LOGWRITER_MAXTOTALMESSAGESPERFILE` 限制**恢复时从单个文件解析的行数**，使损坏文件**不会耗尽进程内存**。④ 每个目的地带 `circuitBreaker`：`maxFailures`（默认 5）与 `failureWindow`（默认 60000ms，下限 100ms）**滑动窗口**，**旧失败会过期**。
- **判据**：① **「先落盘再转发」的可靠性前提是单写者**——一旦多个进程共享同一个缓冲文件，容错机制本身就成了数据损坏源，表现为「恢复失败 + 丢事件」而不是「投递变慢」；排查投递异常时先问「这个缓冲有几个写者」。② **手工接管命名就要接管唯一性**：打开自定义路径开关的同时，自动后缀消失，唯一性从系统保障变成编排方的责任——这类开关要在变更说明里写清「你接手了什么」，否则「我配了路径」反而制造冲突。③ **重放通道必须有解析上界**：恢复时逐行读取损坏文件会演变成 OOM，越强调「不丢事件」越要限制单次恢复的规模。④ **熔断与退避是两种不同保护**：退避限制的是**重试节奏**，熔断按**窗口内失败计数**切断投递、保护的是已经吃不消的下游；窗口滑动意味着「之前失败过」不代表「现在还是坏的」，用固定印象判断当前可用性会误判。⑤ 「失败计数达阈」与「失败序列达阈」（Make 第 8 次关停调度）不可互换——前者看密度、后者看累计，选错会让系统要么过于敏感要么迟迟不断。
- **提升层**：工作流 / 诊断。触发词：事件缓冲多写者、logwriter 唯一路径、恢复解析上界、滑动窗口熔断、maxFailures、旧失败过期、退避与熔断区别。

## 降级值要满足输出类型契约；同叫「循环」，Loop 恒停而 Iteration 可继续，继续方式又分「留位 null」与「剔除」（来源：docs.dify.ai `en/cloud/use-dify/build/predefined-error-handling-logic.md` 3,768B，2026-10-03 r408B 独立 curl 取 `.md` 原文实拉）
- **原文**：① 节点失败可选三行为：**None**（默认，整个工作流停止，拿到原始错误）/ **Default Value**（用备用值继续）/ **Fail Branch**（走独立错误处理分支）。Default Value **必须与节点输出类型一致**（输出 string 则默认值得是 string）。② **Loop 节点在任一子节点失败时立即终止整个循环**并返回错误，不再继续后续迭代；**Iteration 节点**可选 `terminated`（默认，任一失败即停）/ `continue-on-error`（跳过失败项继续，**失败项在输出数组里返回 `null`**）/ `remove-abnormal-output`（继续处理但**从最终输出中过滤掉失败项**）。
- **判据**：① **降级不是「填个值」而是「填一个符合契约的值」**——默认值类型不匹配时，失败被换成了类型错误，故障从「上游不可用」变成「下游解析失败」，排查方向被彻底带偏；验收降级路径时要在**失败态**下检查输出类型，而不是只看成功态。② **Fail Branch 与 Default Value 是两种不同承诺**：前者把错误当事件交给另一条流程（可通知、可换服务、可记录），后者把错误当缺席、用占位顶上；选错的表现是「用户完全不知道出过问题」或「整个流程为一个非关键节点停摆」。③ **同为循环体，失败语义必须逐类确认**：Loop 没有继续选项，Iteration 有——把 Iteration 的容错写法套到 Loop 上会得到「配了但没用」。④ **两种继续模式的差别在输出形状**：`continue-on-error` 保**位置**（数组长度不变、失败项为 `null`），`remove-abnormal-output` 保**内容**（只留成功的、长度变短）；下游按索引取值和按内容遍历的结果会完全不同，出了「结果少了几条」先判断用的是哪一种。⑤ 失败项返回 `null` 时，**「有值但为空」与「该项不存在」在后续节点里是两件事**，聚合前要先决定空值语义。
- **提升层**：工作流 / 诊断。触发词：Default Value 类型匹配、Fail Branch、Loop 恒停、Iteration 三模式、continue-on-error null、remove-abnormal-output、失败项空值语义。

## 需人工确认的工具不能用进无人值守通道；审批是「逐事件回执」协议，回一半不算恢复（来源：docs.bigmodel.cn `cn/managed-agents/permission-policies.md` 6,620B（经 `llms.txt` 49,320B 定位），2026-10-03 r408C 独立 curl 取 `.md` 原文实拉）
- **原文**：① 权限策略两档 `always_allow` / `always_ask`，**默认两档都是 `always_allow`**，且**平台不提供「记住本次决定」「只询问一次」这类中间形态**。② 调用 `always_ask` 工具时会话发 `agent.tool_use` 事件 → 暂停 → 发 `session.status_idle`，`stop_reason.type = requires_action`，**待审批的事件 ID 列在 `stop_reason.event_ids` 数组里**；**会话无限期等待响应**。③ 要为每个待审批事件发一条 `user.tool_confirmation`（`tool_use_id` + `result` = allow/deny，拒绝可带 `deny_message`），**一次 events 请求可携带多条确认**；**所有待审批事件都被处理后会话才回到 running**。④ 官方提示：**定时部署可以绑定带 `always_ask` 的 Agent，但触发后会停在 `requires_action`**，**无人值守的 cron 请用 `always_allow`**。⑤ 另有：权限策略管的是「已启用工具何时执行」，**要把工具彻底移除得用 `enabled: false`** —— 两个旋钮正交。
- **判据**：① **「需要人点头」的能力与「没有人」的通道是组合禁忌，不是配置建议**——同一个 Agent 定义挂到交互式会话没问题、挂到定时/队列触发就会永久停在 `requires_action`；上线前要按**触发方式**逐个检查被挂载的能力里是否有 `always_ask`，而不是按 Agent 定义看起来对不对。② **暂停原因是被显式列出来的**（`stop_reason.event_ids`），不是"整会话暂停"——读状态要先读这个数组，逐个消解；只回一部分的话会话**继续挂起**，表现为「我批了啊怎么还没动」。③ **批量回执要按组而非按条看待**：多条确认可一次发送，但恢复条件是「该批全部处理完」，这是个**全或无**语义，不是逐条放行。④ **没有中间形态是有意的**：平台不提供「本次允许/仅一次」，说明凡是「一会变 mature 长期有效」的便利形态都会把一次性批准演变成事实上的长期授权；缺这个选项不应被当成功能缺口去绕过。⑤ **审批开关不能充当撤销**：想让工具彻底消失要改启用位，只把策略调严，工具仍在能力面里（随时能被改回）；两者要分开声明。
- **提升层**：工作流 / 安全边界。触发词：always_ask 与 cron 冲突、requires_action、event_ids 待审批列表、tool_confirmation 批量回执、全或无恢复、策略不等于启用。

## 依赖失败不阻断会话启动，只降级为带三态重试标的事件；会话外可主动探测且探测结论含「不可判定」一态（来源：docs.bigmodel.cn `cn/managed-agents/{mcp,vaults}.md` 6,511B / 7,423B，2026-10-04 r409A 独立 curl 取 `.md` 原文实拉；与 §长命周期任务故障计数分型 / §判死前先回查真实执行状态 互补——那两条管"怎么判死"与"计数怎么分型"，本条管"依赖不可用时平台选择继续跑"与"探测结论本身可能不可判定"）
- **原文**：`创建会话时不校验 MCP 的连通性或凭据。如果某个 MCP 服务器不可达或拒绝了凭据，会话仍会正常启动、正常交互。平台会发出 session.error 事件，其中包含出错服务器的 mcp_server_name 和重试状态 retry_status（取值 retrying / exhausted / terminal）`；`没有匹配凭据时，连接将以未认证方式尝试`；`mcp_oauth_validate 会对目标服务器发起 MCP initialize 探测，返回 valid / invalid / unknown 结论`；响应含 `refresh（刷新尝试结果：succeeded / failed / connect_error / no_refresh_token）`；`mcp_probe（initialize 探测的 HTTP 摘要，敏感值已脱敏）`。
- **判据**：① **启动成功不等于依赖可用**——依赖失败被降级成一条事件而非启动失败码，验收/监控必须去读事件流，不能只看"创建会话返回 200"。② **失败不是二值而是三态机**：`retrying` 还有机会、`exhausted` 已耗尽、`terminal` 已判定不可恢复——同一条错误事件在不同态下处置相反（继续等 vs 换凭据 vs 摘除该依赖）。③ 主动探测的结论**保留 unknown 一态**，`unknown` 既不是成功也不是失败，把 unknown 当"已通过"或"已失败"都会给出错误结论。④ 刷新结果四态里 `no_refresh_token` 是**配置缺失不是故障**，`connect_error` 是**网络面问题不是凭据失效**——四态分属三个责任面，排障先归面再动手。⑤ 探测摘要已脱敏，**拿探测输出当凭据校验依据会读到假值**。⑥ 无匹配凭据时以未认证方式尝试 = 显式 fail-open，"连上了"不等于"以预期身份连上了"。
- 提升层：工具/工作流。触发词：依赖失败不阻断启动、retry_status 三态、exhausted/terminal、探测结论 unknown、no_refresh_token、脱敏探测摘要、fail-open 未认证连接。

## 跨轮持久性是分层的：产物目录恒久、工作区要开 checkpoint、进程与内存从不保；快照只在成功轮更新，故恢复点会滞后于失败尝试（来源：docs.bigmodel.cn `cn/managed-agents/create-session.md` 9,481B，2026-10-04 r409C 独立 curl 取 `.md` 原文实拉；与 §重放不是时光机（可变量取最新值）/ §观测快照唯一可写例外 互补——那两条管"重放语义"与"快照可写性"，本条管"哪些东西跨轮还在"与"快照什么时候才会推进"）
- **原文**：`/mnt/session/outputs 始终跨轮保留……并编目为可下载的 Session File`；`/workspace、/tmp、运行期安装的软件包 默认不保留。加 x-checkpoint: true 后随系统盘快照跨轮保留`；`x-checkpoint：仅创建会话时可用。精确小写 true / false，缺省 false`；`平台会在成功执行结束时尝试保存快照，下一轮优先从最近一次成功快照恢复；失败轮不更新快照`；`快照的创建或恢复受账号配额和底层服务可用性影响，失败时会回退到新的沙箱，因此不应作为唯一的持久存储`；`Checkpoint 只保留磁盘，不保留正在运行的进程和内存状态`；`响应中的 budget 字段当前恒为 null：平台暂不支持会话级消费上限`；`创建时加 x-events-encrypted: true……开关创建后不能改`；`覆盖语义：可覆盖 model、system、tools、mcp_servers、skills；每个字段都是整体替换（非深合并）`；`只要 initial_events 非空，会话创建成功后会自动开始执行……重复发送同一任务会执行两次`。
- **判据**：① **持久性分三层，各层默认值不同**：产物目录恒久保留（设计上就是交付面）、工作区/临时目录默认丢（要保留得开 checkpoint）、进程与内存永不保 ⇒ "上一轮还在"这个问题必须先问它在哪一层，把中间产物写进工作区却指望跨轮可见是最常见的错。② **快照只在成功轮更新**：失败轮不推进快照 ⇒ 连续失败后恢复点可能停在很久以前，"从快照恢复"得到的环境比你以为的旧；评估恢复成本要按"最后一次成功的时刻"算。③ **快照失败会静默回退新沙箱**：配额/可用性导致快照不可用时不会报错而是起一个新沙箱 ⇒ 快照是**尽力而为**，不能当唯一持久存储，可靠交付仍要落产物目录。④ **一次性开关必须创建时决定**：`x-checkpoint` 与 `x-events-encrypted` 都只在创建会话时可用、之后不可改 ⇒ 加密与保留策略属于"设计期决策"，运行中发现没开会无法补救，只能重建。⑤ **布尔头是严格字面量**：`x-checkpoint` 只接受精确小写 `true`/`false`，写 `True`/`1` 等于没开 ⇒ 静默失效型配置，验收要读实际生效值。⑥ **"字段存在"不等于"能力存在"**：`budget` 恒为 null 意味着平台根本没有会话级预算能力，把"配置里有个 budget 字段"当成"可以设预算"会得到永远不生效的策略——与 §文档示例值≠内建默认 同族（那条是值不同，这条是能力缺失）。⑦ **整体替换非深合并**：会话级覆盖是整块替换，只传一个子字段会抹掉其余配置。⑧ initial_events 非空即自动开跑且**不会去重** ⇒ 重试创建 + 重发同一任务会造成双跑。
- 提升层：工具 / 工作流。触发词：持久性分层、产物目录恒久、checkpoint 仅创建时、快照只在成功轮更新、失败轮不推进快照、快照回退新沙箱、一次性开关、布尔头严格字面量、budget 恒 null、整体替换非深合并、initial_events 双跑。

## 循环上限的计数单位被「自我复制」重置就等于没有上限；修完 bug 要把它的状态签名固化成断言；监控缺「增长率 / 同类重复」两个维度就只能等客户上报（来源：www.activepieces.com/docs `handbook/engineering/postmortems/2026-03-19-redis-and-delay-overload.md` 3,797B，2026-10-04 r411A 独立 curl 实拉；与 §长命周期任务故障计数分型 / §熔断按滑动窗口计数 互补——那两条管"达到阈值后怎么停用"，本条管"阈值挂错计量对象时根本达不到"）
- **原文**：Delay 步骤的 job 带着 `executionType: BEGIN` 而非 `RESUME` 被 `moveToDelayed()` 挂起，到期后 worker 从第一步重跑、再遇 Delay 再挂起，无限循环淹没 Redis。官方明确："The platform does enforce per-execution time limits, but because the job was marked as `BEGIN` instead of `RESUME`, each loop iteration was treated as a brand-new execution rather than a continuation."；检测面："**Detected by customers, not automated alerting.** There was no monitoring on repeated execution patterns or runaway job creation for a single flow."；纵深修复两条："Worker validates that RESUME operations have non-empty execution state. An empty state with RESUME is the exact signature of the original bug and is rejected with a `VALIDATION` error" / "Engine asserts that BEGIN operations have empty execution state."
- **判据**：① **上限的计数单位必须与失控的放大单位一致**——自我复制 / 重入型循环的每一轮都会开一个新的"配额桶"（新执行、新会话、新请求），于是"每次执行最多多久"这类预算**每轮重置、永远不触发**；要拦住它必须按**同一 run / 同一对象**累计（同一 run 的重复执行次数、同一 flow 短窗内的重触次数）。⇒ 看到一个循环"明明有上限却跑飞了"，先问这个上限是按"每次"算还是按"累计"算。② **修完 bug 要把 bug 的状态签名固化成断言，而不只是改掉触发路径**：RESUME 带空状态 = 原 bug 的签名、BEGIN 带非空状态 = 回归签名，两者都做成了显式校验 ⇒ 回归时现象从"又出错了（要重新定位）"变成"被断言挡住且指名原因"。③ **监控维度的缺口不是灵敏度而是维度本身**：只测"在不在 / 有多少"测不出"在自我放大"，必须补**增长率**（队列深度增速、调度量突增）与**同类重复模式**（同一对象短窗 N 次重触）——本次事故由客户上报发现，两个"To do"恰好都是这两类告警。⇒ 评估可观测面时按"绝对量 / 变化率 / 同类重复"三类分别清点，缺哪类就是哪类事故只能靠用户发现。
- 提升层：工作流 / 可观测性。触发词：自我复制循环、每次预算被重置、上限计数单位、resume 空态签名、状态签名断言、增长率告警、同类重复模式、客户先于告警发现。

## 「fallback」有两种相反语义（解析期候选链 vs 运行期故障转移）；废弃兼容字段必须明说「不再改变运行时行为」；默认值随别的参数联动时必须给出映射表（来源：docs.openclaw.ai `concepts/active-memory/tuning.md` 4,601B，2026-10-04 r412C 独立 curl 取 `.md` 原文实拉；与 §循环上限的计数单位 / §诊断输出分粗桶与稳定原因码 互补——那两条管"失控怎么计量"与"报错怎么说清"，本条管"配了却没生效这类假象怎么定位"）
- **原文**："`config.modelFallbackPolicy` is a compatibility field kept for older configs, **deprecated in v2026.4.12; it no longer changes runtime behavior** — `modelFallback` is strictly the last resort in the chain above, **not a runtime failover that swaps in another model when the resolved one errors**"；解析链 "explicit plugin model -> current session model -> agent primary model -> optional configured fallback model"；默认联动 "message -> strict / recent -> balanced / full -> contextual"，"An explicit `config.promptStyle` always overrides the mapping."
- **判据**：① **同名不同义的配置先分语义再谈生效**：`fallback` 在解析链里是"候选顺序的最后一环"（在选定之前起作用），在故障转移里是"选定之后出错才换"（在选定之后起作用）——触发时机相反；把前者当后者配，会得到"明明配了备用却没顶上"的假故障，而且排查方向从第一步就是错的。② **废弃字段要写清"还认不认 / 还做不做"**：为了兼容老配置而继续解析（读了不报错）与仍然改变行为是两件事；只写 deprecated 不写"不再改变运行时行为"，用户就会把它当成仍有效的控制——与 §Cap65 撤销≠禁止 同族：看起来在生效、实际在空转的假控制。③ **默认值随另一个参数联动时，必须把映射表写出来**：只写"默认值是 balanced"是错的，用户改了 queryMode 就静默换了召回风格 ⇒ 联动默认不列表，任一参数的副作用就不可见、也不可预期。④ **显式覆盖必须无条件胜出**：用户明确写下的值压过一切推断，别让"更懂你"的推断盖掉显式配置。
- 提升层：工具 / 诊断。触发词：fallback 语义、解析链与故障转移、废弃字段不再生效、假控制、默认值联动映射、显式覆盖优先、配了没生效。


## 故障分类按「文本像不像」而不是状态码：跨厂商没有统一协议语义，周期用量窗口与瞬时限流同桶会让冷却时长失去意义（来源：docs.openclaw.ai `concepts/model-failover.md` 39,408B，2026-10-04 r413B 独立 curl 取 `.md` 原文实拉；与 §fallback 两种相反语义 / §循环上限计量 互补——那两条管"备用在哪个阶段顶上""上限以什么为单位"，本条管"什么叫一次限流、冷却到什么时候为止"）
- **原文**：「That rate-limit bucket is **broader than plain 429**: it also includes provider messages such as `Too many concurrent requests`, `ThrottlingException`, `concurrency limit reached`, `workers_ai ... quota limit exceeded`, `throttled`, `resource exhausted`, and **periodic usage-window limits** such as `weekly limit reached` or `monthly limit exhausted`.」「A timeout that **looks like** rate limiting counts as such a failure.」「Thrown exhaustion summaries include structured per-attempt details and the **soonest cooldown expiry** when one is known.」「A terminal credential failure cools down **the exact selected profile** before model fallback.」「Transcript, format, context, pre-provider timeout, and ambient CLI failures **without a selected profile do not change shared profile health**.」
- **判据**：① **分类规则必须写成文本枚举而非状态码匹配**——同一类处置（冷却 + 换下一个）由"消息像不像"触发；跨厂商没有统一状态语义，只认 429 会把大半真实限流漏成普通错误。⇒ 排障时"为什么它没走降级"的第一查点是**匹配表是否覆盖该厂商的措辞**，不是网络/凭据。② **瞬时与周期窗口不能共用同一个冷却值**——`429` 的恢复单位是秒，`weekly limit reached` 的恢复单位是天；两者进同一个桶 ⇒ 冷却值无论取哪个都是错的。⇒ 分类桶必须携带**恢复量级**，或者干脆把周期窗口单列；否则重试风暴（短冷却打在周限额上）与假死（长冷却打在瞬时抖动上）二选一。③ **耗尽报告的价值在"最早可重试时刻"而不是"失败原因列表"**——终态失败要给出 soonest cooldown expiry；只列每次失败原因，运维拿到的是"为什么不行"而拿不到"什么时候再试"。④ **归因必须有门槛：没有选定目标的失败不该记到任何目标头上**——发生在选定之前的失败（pre-provider timeout / 环境级 / 无 profile 的 CLI 失败）不改变共享健康度；把所有失败都用来惩罚候选，会让一次环境问题把全部凭据依次冷却掉。⑤ **归因粒度要精确到"被选中的那一个"**——终端凭据失败只冷却那个具体 profile，不是整个 provider；粗粒度惩罚会把"一个 key 坏了"放大成"一家厂商不可用"。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：限流桶文本枚举、周期用量窗口、soonest cooldown expiry、冷却量级、归因门槛、精确到被选中的凭据。


## 取消不是回滚、超时降级不得串联更多超时、失败类别决定重试资格：清理预算与操作预算必须分离，且「信号被拒」须靠进程普查证明才算清理完成（来源：docs.openclaw.ai `concepts/compaction.md` 20,148B + `ci/checkout.md` 21,314B，2026-10-04 r416A 独立 curl 取 `.md` 原文实拉；与 §fallback 两种相反语义 / §限流桶文本枚举 互补——那两条管"备用在哪个阶段顶上""什么叫一次限流"，本条管"取消/超时之后现场是什么状态、什么才配重试"）
- **原文**：「Cancellation is not rollback: a compaction that already completed remains in the transcript and is still counted, without sending a late reply.」「The built-in OpenClaw runtime does not start further recovery hooks, maintenance, transcript truncation, or retries after cancellation.」「OpenClaw commits that compaction without a summary instead of ending the turn … A timed-out summary does not move to the model fallback chain, because each extra model could add another full timeout window to the wait.」「Such a replacement must strictly reduce history; unchanged or larger results are rejected.」「Cleanup has a ten-second allowance, separate from the operation deadline.」「A denied group signal can be accepted only when that census proves there are no live members; live or unknown state still fails closed.」「Only ordinary Git failure or `FetchTimeout` permits retry after verified cleanup.」「After a failed or terminated fetch and verified process-tree extinction, the owner removes newly created locks in physical Git metadata; pre-existing locks and linked metadata remain untouched.」「Once cleanup succeeds, cancellation takes precedence over timeout or ordinary Git failure.」
- **判据**：① **取消只保证"不再向前"，不保证"回到之前"**：已完成的副作用（已写入的压缩条目）留在转录里并参与计数，只是不补发迟到的回复；取消后不再启动任何后续 recovery / 维护 / 截断 / 重试 ⇒ 把取消当回滚，会在"看起来干净"的现场上继续跑，而实际已经留下了一半的变更。② **超时降级不得串联更多超时**：摘要超时就提交一个"无摘要"的压缩让回合继续，刻意**不**转模型 fallback 链——每多一个候选模型就多一个完整超时窗口 ⇒ 用"换一个更慢的东西再试一次"来救超时，本质是把 N 倍等待塞给用户；降级路径必须显式声明它不再引入新的等待源。③ **优化类操作要有单调性校验**：压缩结果必须严格小于原历史，等于或更大则拒绝 ⇒ 没有单调性校验的"优化"可能只是复制甚至放大，而且不会报错。④ **失败类别决定重试资格，不是所有失败都该重试**：只有「普通失败 / 取数超时」在**进程树抽干经验证之后**才放行重试，取消与所有权失败是终态 ⇒ 不分类的重试会把终态失败也拖进重试风暴，还会掩盖真正的终态原因。⑤ **清理预算与操作预算必须分离**：清理有独立的固定额度（10 秒），不吃操作 deadline ⇒ 共用一份预算时，要么收尾没时间做完留下脏状态，要么主操作被清理挤掉。⑥ **"发了终止信号"不等于"它停了"**：信号被拒时须做进程普查证明无存活成员才接受，live 或 unknown 一律 fail closed ⇒ 这是清理假象的头号来源；同理"等 leader 退出"不够，要观察整个进程组消失。⑦ **清理只动自己新建的东西**：锁回收只移除本次新创建的锁，既有锁与链接元数据保持不动 ⇒ 清理必须区分所有权，否则会顺手破坏别人的状态。⑧ **取消优先于超时与普通失败**：清理成功后若同时存在取消，归类为取消 ⇒ 终态归类要有优先级，否则同一现场会被记成三种不同的失败。
- 提升层：工作流 / 诊断 / 可复用 Skill。触发词：取消不是回滚、超时降级不串联超时、单调性校验、失败类别决定重试资格、清理预算独立、进程普查 fail closed、只清理自己新建的、取消优先于超时。

## 进度标记与产出分两次落库就是失步窗口；超时放弃的语义是「当没发生过」，且放弃阈值必须小于接管租约（来源：docs.n8n.io deploy/host-n8n/configure-n8n/durable-scheduler.md 30,546B，2026-10-04 r417A 独立 curl 取 .md 原文实拉；真页经 llms.txt 287,049B 重新定位，此前 Qoder 引用的 hosting/scaling/durable-scheduler 系 1,930B 404 壳）
- 进度与产出是两个写入就存在失步窗口：轮询光标默认存 workflow static data 并与执行分开保存，崩溃落在两次保存之间时二者错位，症状是「跳过条目」或「重复处理」。修法是把光标与执行放进同一张表的同一事务，使一轮轮询要么完全发生要么完全没发生。判据：写入次数即窗口数。
- 超时放弃必须让标记原地不动：poll 超过阈值被放弃时平台什么都不记、光标不动，下一次覆盖同一段，因此不丢数据。「放弃」的正确语义是「当作没发生过」，若写成「推进到下一处」就会静默丢数据。
- 两个超时必须有偏序：放弃阈值（poll timeout）须严格小于接管租约（lease duration），否则被放弃的工作仍在跑而另一实例已接管同一 run，放弃形同虚设；平台在 timeout 达到 lease 时启动告警。
- 积压补跑是形状选择且没有任何策略逐条重放：丢弃全部 / 坍缩为最新一次 / 每条触发规则各一次，三种策略下时钟一律跨过积压；一次性触发没有「下一次」可恢复，故 catch-up 策略下仍会晚跑，skip 则永久丢弃。与部分失败三形状互补——那条管同批内失败条目的形状，本条管跨批积压的形状。
- 调度实体有所有者：owner reconciliation 周期回收所有者已消失的 schedule，否则留下无人认领的孤儿定时任务。


## 同一根因在四层症状上暴露；调试行为本身会改变资源画像（来源：docs.n8n.io `deploy/host-n8n/configure-n8n/scaling/fix-memory-issues.md` 5,626B，2026-10-05 r420-B 经 llms.txt 定位真路径后 .md 实拉）
- **实证**：官方列出 OOM 的四类表现——节点级 `Execution stopped at this node (n8n may have run out of memory)`、工作流级 `Problem running workflow`、连接级 `Connection Lost`、协议级 `503 Service Temporarily Unavailable`，另有引擎日志级 `Allocation failed - JavaScript heap out of memory`；「Manual or automatic workflow executions: manual executions increase memory consumption as n8n makes a copy of the data for the frontend」；拆分为子工作流「might seem counter-intuitive at first as it usually requires adding at least two more nodes」但「the sub-workflow only holds the data for the current batch in memory, after which the memory is free again」，前提是「returns only a small result set to its parent workflow」。
- **判据**：① **症状层与根因层要分开建表**——同一根因（资源耗尽）在节点提示 / 工作流状态 / 连接断开 / HTTP 状态码 / 引擎日志五个面各有说法；按症状分诊会把一次 OOM 记成四种不同故障，复发率永远统计不出来。② **"人看着跑"会改变资源画像**——手动执行为前端额外复制数据，因此调试态比生产态更容易触顶； reproduced-under-debug 与 reproduced-in-prod 必须分别标注。③ **降峰值靠缩短数据存活期，不靠减少步骤数**——拆成子流程反而省内存，因为每批数据用完即释放；"看起来更绕的解法更省"是可判据化的，不是玄学。④ **边界数据量决定拆分是否生效**——子流程必须只回传小结果集，回传大对象时拆分零收益；优化要看**跨界传输量**，不是内部计算量。⑤ 验收增一项：**资源类故障的症状覆盖面**（是否把连接级与协议级也归到同一根因）。
- **与既有能力分工**：1.145.0 管限流类故障的文本枚举与冷却量级；本条管**资源耗尽类故障的跨层症状映射**，以及"观测行为改变被测对象"这一自举偏差。
- 提升层：工作流 / 工具。触发词：OOM 四层症状、手动执行更耗内存、拆分降峰值、存活期决定峰值、边界数据量、调试改变资源画像。

## 修复由「再检测」证明，不由返回值证明；耗时与退出码本身不能证明原因（来源：docs.openclaw.ai `cli/doctor/health-contract.md` 3,303B + `ci/checkout.md` 21,314B，2026-10-05 r421-A 独立 curl 取 `.md` 原文实拉逐串命中；消化 Qoder r407-Q-A N3/N12 积压点，并回源钉定 r385B 曾判「转述未证实」的真页）
- **实证**：「`repair()` reports `status: "repaired" | "skipped" | "failed"` (**omitted status means `repaired`**).」；「**After a successful repair, doctor re-runs `detect()` scoped to the repaired findings; if the finding is still present, doctor reports a repair warning instead of treating the change as complete.**」；「Repair contexts can carry `dryRun`/`diff` requests; repair results can return structured `diffs` … and `effects` (service, process, package, state, or other side effects), so converted checks can grow toward `doctor --fix --dry-run` **without moving mutation planning into `detect()`**.」；归因侧「`FetchTimeout` is reported **only when present in the chain**. Earlier failures without this evidence retain an unknown cause; **elapsed time or exit 125 alone cannot establish a timeout or a particular failing API**.」；「The diagnostic reports **up to four exceptions**, following explicit causes before implicit contexts.」
- **判据**：① **修复的完成度由复检给出，不由返回值给出**——repair 成功后以被修项为范围重跑 detect，仍检出即降级为 warning ⇒ 一个函数返回 "repaired" 只说明它"做过了"，把自证当验收是修复类失败的主要来源；凡"自动修复"必须有紧随其后的复检，且复检范围等于被修范围。② **省略状态不是中性，而是取了最宽的那种解释**——omitted status 视为 repaired ⇒ 静默默认一律要挑明：默认取"修好了"会让所有没实现状态上报的修复假成功；设计契约时把"不说话"映射到最严档而不是最宽档。③ **`skipped` 与 `failed` 要跳过验收**——这两档明确不跑复检 ⇒ 把三者合并成一个布尔会把"没修"和"修了但失败"混成一类，无法区分能力缺失与执行失败。④ **计划面与检测面必须分离**——`dryRun`/`diffs`/`effects` 由 repair 上下文承载，刻意不挪进 `detect()` ⇒ detect 一旦知道"这次只是预演"，它的语义就被污染了；预演能力要靠参数传递，不能靠让检测器自己猜。⑤ **耗时不能证明时间类故障**——超时只有异常链在位才算超时，耗时或 exit 125 本身不构成证据 ⇒ 把"跑得久"直接记成 timeout 会让之后所有的重试预算与退避都建立在错误根因上；证据不足时保留 unknown cause，比编造一个更像的原因更有价值。⑥ **诊断记录的封顶是设计不是限制**——异常数、帧数、遍历深度三重上限且省略路径/env/凭据 ⇒ 诊断输出既要够用又要不能成为泄漏面；写诊断时先定"最多报几条、每条多深、哪些字段永不进日志"。
- **与既有能力分工**：1.148.0 管「失败类别决定重试资格 + 进程普查 fail closed」（什么配重试）；本条管**修复本身的验收语义**与**根因的证据资格**——修没修好要复检，因什么坏要有链。
- 提升层：工作流 / 诊断。触发词：修复由再检测证明、repair 后重跑 detect、省略状态视为已修、skipped 与 failed 不计验收、dryRun 不侵入 detect、耗时不能证明超时、异常链在位才算、unknown cause 优于编造、诊断三重封顶。

## 层级配置「取抬高不取拒绝」；放弃型超时必须严格小于租约；弃跑不留痕以保证重放等价（来源：docs.n8n.io/deploy/host-n8n/configure-n8n/durable-scheduler.md 30,546B，2026-10-05 r421-B 经 llms.txt 287,049B 定位真路径后独立 curl 实拉逐串命中；消化 Qoder r408-Q-B B5/B6 积压点）
- **实证**：「n8n **raises** a node's grace period to an instance-derived minimum (based on `N8N_SCHEDULER_EXECUTOR_INTERVAL` and `N8N_SCHEDULER_MATERIALIZATION_WINDOW`) **when set below it**, and caps it at 30 days.」；「A poll that runs longer than `N8N_SCHEDULER_POLL_TIMEOUT` (45 seconds by default) is **abandoned**. n8n **stops waiting for it and records nothing: the cursor stays put**, so the next poll covers the same ground and **no data goes missing**.」；「**Keep the timeout below `N8N_SCHEDULER_LEASE_DURATION`, so an abandoned poll can't still be running when another instance takes its run over.** n8n warns at startup when the timeout reaches the lease duration.」；「**Missed polls are always skipped.** A poll fetches everything new since it last ran, so a catch-up poll would repeat the same fetch.」
- **判据**：① **"值不可信"与"值不可用"要分开处置**——下级值低于由上级参数导出的安全下限时**自动抬到下限并给启动期告警**，而不是报错终止 ⇒ 一个偏小的宽限值通常只是估算错误，拒绝启动会把配置问题升级成可用性事故；抬高+留痕才是"纠正而不中断"。② **抬高的下限必须可推导**——下限由另外两个参数算出，不是拍一个数 ⇒ 凡"自动纠正配置"，纠正依据要能被使用者复算，否则纠正本身就是新的不确定源。③ **跨参数的时序前提是并发安全命题不是性能调优**——放弃型超时必须严格小于租约时长，否则"已弃跑的活仍在执行而他人已接手" ⇒ 两个时间参数一旦失序，就会出现同一份工作被两方同时处理；这类约束必须在启用时校验，不能等到数据错乱才发现。④ **"放弃"的正确姿势是回到未开始态**——超时放弃时停止等待且**不写任何记录、游标原地不动**，下一轮自然覆盖同一片地 ⇒ 半途写一条"部分完成"的状态最危险：既不完整又阻止重做；宁可什么都不记，也不要记一半。⑤ **补跑资格由取数语义推导而非政策选择**——增量拉取型事件的补跑等于重复同一次取数，所以结构上就不该补 ⇒ 判断"漏了要不要补"，先问这个动作的取数语义是增量还是快照，而不是问业务上想不想补。⑥ **反复超时要加大间隔而不是加压**——持续超时的轮询按加宽间隔重投，避免锤一个已经答不上来的服务 ⇒ 退避方向永远与"对方健康度"反相关。
- **与既有能力分工**：1.149.0 管「修复验收与根因证据资格」；1.148.0 管「失败类别与重试资格」；本条管**放弃与配置纠正这两个"非失败终态"**——放弃时现场该是什么样、配置越界时该纠正还是该拒绝。
- 提升层：工作流 / 工具。触发词：抬高不取拒绝、下限自动纠正、跨参数时序不变量、超时小于租约、弃跑不留痕、游标原地不动、回到未开始态、增量拉取不补跑、反复超时加间隔。
