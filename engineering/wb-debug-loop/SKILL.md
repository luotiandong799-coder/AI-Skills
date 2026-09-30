---
name: wb-debug-loop
description: >-
  有纪律的排障循环（诊断 bug / 报错 / 性能回归的根因）。当出现报错、崩溃、白屏、500、超时、测试失败、行为与预期不符、构建/部署跑不起来、性能变慢、内存泄漏、复现不了的怪问题时应用：重现 → 最小化 → 假设 → 验证 → 修复 → 回归测试。禁止"先改再猜"、禁止一次改多处、禁止靠重启/清缓存糊过去。另含「修复验证」：补丁是待验证假设，不从 diff 大小/作者/上游一致/原 PoC 失效推成功，须测同根因变体与兄弟路径。触发词：报错、错误、异常、崩溃、闪退、白屏、跑不起来、不生效、没反应、失败、失败原因、找不到原因、查不出、定位、排查、排障、根因、复现、回归、性能变慢、卡顿、内存泄漏、超时、内存溢出、debug、troubleshooting、root cause、stack trace、崩溃日志、模型行为、幻觉、选型、补丁、修复验证、patch、变体、这算 bug 吗、加固算修复吗、兜底不是修复、重试掩盖、静默降级、缓解不是修复、改指令算修了吗、装了不生效、静默失败、幻影字段、声明但未写入。不适用：只是"该不该写这段代码"的取舍（走 wb-ponytail）、多步实现任务的规划与交付（走 wb-spec-driven）、任务级"点名目标全量覆盖 / 失败换路攻坚"纪律（走 wb-execute-discipline）。、一直在重复、转圈、卡死检测、迭代上限定多少、并行单元重名、工具结果用错、喂给判定的字段要人话、验证证据要让外行能下结论、先找仓库既有规程、失败声明、failure cause、只报原因不报对策、分类不出就原样抛、等待提示、错误负载缺省字段、OOM 恢复、中断恢复、取消不等于丢弃、半成品保留、完成标记游标、重试准入、重试不生效、参数冲突、单次超时与总时长、重试留痕、兜底范围、提前终止原因、结束原因可见、主动退出留痕
version: 1.84.1
agent_created: true
---

# wb-debug-loop（排障：按纪律走，不靠猜）

来源：mattpocock/skills 的 `diagnose` 技能（重现 → 最小化 → 假设 → 工具 → 修复 → 回归测试）+ 通用调试纪律。提纯为本地循环。

**核心判断：改不动的 bug，几乎都是"还没复现就先改了"。** 定位是证据工作，不是灵感工作。

## 二、六步循环

| 步 | 做什么 | 判据（做到什么算这步结束） |
|---|---|---|
| 1 重现 | 用固定的输入/环境/命令拿到**确定性**的失败；记录命令与输出**原文**（不转述） | 我能重复触发它三次 |
| 2 最小化 | 剥掉无关输入、依赖、代码路径，直到最小失败用例 | 能把失败压成一小段片段或一条命令 |
| 3 假设 | 写 1–3 条**可证伪**的假设，按"验证代价"排序（先排最便宜的） | 每条假设都能说出"什么观察结果会否掉它" |
| 4 验证 | 用日志 / 断点 / 单测 / 二分 / 版本回退**直接观测** | 拿到一手证据（打印的值、返回码、trace），不是"读代码觉得应该是" |
| 5 修复 | 改最小必要处，说明**根因**（不是症状） | 能一句话说清"为什么之前会错" |
| 6 回归 | 跑最小复现（现在通过）+ 相关既有测试/路径（没挂） | 两边都跑过，输出留着 |

1–4 步才是排障，5–6 步是顺手完成的事。**卡住 90% 是跳过了 2 或 4。**

## 二·五、修复验证：补丁是待验证假设（细则已下沉 KB）
- 完整论证见 [references/knowledge-base.md](references/knowledge-base.md) §二·五、修复验证：补丁是待验证假设。
> 本节（二·五·五、修在调用方收敛处：只修被报告的路径 = 修…）原文已整段下沉至 `references/knowledge-base.md`，需要时按标题检索。
<!-- 2026-09-29 r290 下沉：容错装置/失败经验记忆/日志即线索 3 节 → references/knowledge-base.md §r111 批 -->
## 二·七、失败永不阻塞主回复：回复路径上每一步都要 等 6 节（细则已下沉 KB）
- 完整论证见 [references/knowledge-base.md](references/knowledge-base.md) §二·七、失败永不阻塞主回复：回复路径上每一步都要 等 6 节。
## 复现不了就先把发生率抬高：1% 追不到，50% 就能二分（来源：topaiskills.com「diagnosing-bugs-skill-faq」（Matt Pocock `diagnosing-bugs`，mattpocock/skills 工程族）2026-09-21 实拉，与 §六步循环「没有稳定复现之前不改产品代码」互补——那条管"没有复现不许动手"，本条管"**复现率低到不可用时该往哪个方向使劲**"）

- **原文事实**：技能要求先有一条 **red-capable 命令**（已跑过至少一次、走真实 bug 路径、断言用户确切症状，且确定性 / 秒级 / agent 可无人跑）；原文判词 "*if you catch yourself reading code to build a theory before a red-capable command exists, stop*"。对 flaky 的处理不是追干净复现，而是**抬高发生率**：把触发循环一百次、并行化、加压、压缩时间窗、注入 sleep。原文阈值直白 —— **"a 50%-flake bug is debuggable, a 1% bug is not"**，一直抬到可调试为止。30 秒的 flaky 回路比没有回路好不了多少；2 秒的确定性回路是超能力。
- **判据**：
  1. **flaky 的方向是"抬高发生率"，不是"等它自己再出现一次"**。判据：**先量化当前发生率，然后逐档抬高（循环次数 / 并发 / 压力 / 时序干预），每档记录命中率**；只写"偶现"两个字等于把这个 bug 判了无期。
  2. **没有回路就禁止假设，且要大声说出"我没有回路"**。判据：**假设之前必须有一条已经跑过、能在该 bug 上变红的命令**；建不出来就停下列出试过什么，并点名要三样之一——能复现的环境、脱敏的捕获产物（HAR / 日志转储 / core dump / 带时间戳录屏）、或加临时生产埋点的授权。
  3. **假设必须自带预测，且成组并列**：生成 **3–5 条可证伪假设**，每条写清"**如果 X 是原因，改 Y 会让 bug 消失或变糟**"，**先给用户看排序再动手测**（单条假设会锚定在第一个想得通的解释上）。判据：**一条没有预测语句的假设不是假设，是一个名词**。
- 提升层级：工作流（排障循环的执行顺序）+ 工具（回路与探针的构造）。
- 触发词：复现率、抬高发生率、flaky 阈值、red-capable、red-capable 命令、无回路不假设、假设带预测、3–5 条假设、锚定。

## 探针要能一次撤干净，seam 太浅本身就是结论（同来源 `diagnosing-bugs` 技能正文，与 §诊断装置自身的可信度、§接线腐烂 互补——那两条管"检查器有没有遭遇"与"装了为什不生效"，本条管"**临时探针的回收**"与"**回归测试挂点选错时该怎么报告**"）

- **原文事实**：调试日志只允许打在**能区分假设的边界**上，绝不"log everything and grep"；每条调试日志带**唯一前缀**（如 `[DEBUG-a4f2]`），收尾一条 grep 全清；原文判词 "**one breakpoint beats ten log statements**"。性能回归不用日志查——**先建基线测量，再二分**。回归测试**在修复之前写，但前提是存在正确的 seam**（该测试在真实调用点上复现该 bug 形态）；**seam 太浅的测试给的是虚假信心**；**若根本不存在正确 seam，那本身就是发现**——代码库架构在阻止这个 bug 被锁定，要作为结论报出来。收尾六条清单：原 repro 不再复现（重跑第一轮循环）、回归测试通过、按前缀 grep 清掉全部 `[DEBUG-...]`、一次性原型删除或移到标记位置、**把被证实正确的那条假设写进 commit / PR 说明**。
- **判据**：
  1. **每条临时探针都要有可回收的标识**。判据：**写第一行调试代码前先定前缀，收尾时用同一个前缀 grep 并确认命中 0**；没有回收手段的探针不该落地（与 §观测是被动旁路 分工：那条管测量挂在哪条时间线，本条管临时测量怎么撤）。
  2. **"测不到"要分两种并分别报告**：seam 太浅 → **给的是假信心，必须标注**；没有 seam → **是架构结论，不是失败**。判据：**写回归测试前先回答"这个测试能不能在真实调用链上复现该形态"，答不出就别写，把答案当发现报**。
  3. **把"哪条假设是对的"写进提交信息**。判据：**下一次排障的人应该能从 commit 里读到这次的因果，而不是从代码里反推**。
- 提升层级：工作流（探针生命周期）+ 可复用 Skill（结论的写法）。
- 触发词：唯一前缀、[DEBUG-a4f2]、一次 grep 清理、一个断点胜十行日志、基线再二分、seam 太浅、没有 seam 是发现、假设写进 commit。


---

## 学习轮沉淀区（本段）
（r历史 起的连续学习轮章节共 115 章已下沉 references/knowledge-base.md §≤200迁移，正文留此指针）

## Harness 自改进与 trace 复用簇（细则已下沉 KB）
- 技能级记忆、Harness 工程与三阶段自改进、后台 review fork、视觉双扩展、trace 失败模式清单、trace→evaluator、harness 演进三问——**七条同源，完整论证见** [references/knowledge-base.md](references/knowledge-base.md) §Harness 与 trace 自改进簇。
## 学习轮沉淀区（本段）
（r历史 起的连续学习轮章节共 236 章已下沉 references/knowledge-base.md §≤200迁移，正文留此指针）

## Qoder 净新（2026-09-27 · 全量消化）
- **偏差点重启-替代生成法**（arXiv 2609.29154 SkillPivot）：修技能/排查失败 run 用三信号（执行有效性/目标进度/动作多样性）定位**首个偏差点**，从偏差前缀重放生成"同一历史下的成功替代段"，只把替代段与偏差前缀的差异反哺进修订——不把整条失败轨迹当废样本（与受控扰动审计互补：那管事前找缝隙，这管事后从真实失败挖最小修订）。
- **滑窗规避反模式**（arXiv 2609.30217 EvasionBench）：重试循环会把"相关上下文"推出监控/评审窗口，让同一操作在第 N 次重试"看不见地"通过——监控须锚定**操作序列**而非近期窗口，跨轮拆分动作计入同一意图链。
- **执行回放一等位**（Activepieces）：每次执行的完整动作序列留独立可读回放记录，排障不依赖 trace 后端。

## 读侧先行的灰度升级律：旧版读侧会把引用当正文返给客户端，且不报错（来源：docs.n8n.io/hosting/scaling/queue-mode/，2026-09-28 r210-B 独立实拉）
- **实证**：n8n 2.34.0 起支持把超大的 webhook 响应体 offload 到存储、只回传引用；官方明写「只有 2.34.0 及以上版本的 main 实例才读得懂 offloaded body，旧版会把 storage reference 当响应体直接返给客户端」；给出的升级顺序是「先升全部 main 与 webhook 实例，再给 worker 打开 offload 开关」；worker 若未设该变量则全部 inline 发送，超出上限即失败。
- **判据（两种错配的代价不对称）**：**读侧旧 + 写侧新 = 静默坏数据**（客户端收到引用串当正文，没人报错，最贵）；**写侧旧 + 读侧新 = 明确报错**（便宜、易定位）。所以灰度升级固定 **读侧先行**。
- **排障动作**：遇到「升级后数据变了但没有任何报错」，**先列一张实例版本 × 开关状态的一维表**，再问「谁在读、谁在写」——不要先去 diff 业务逻辑。
- 与 §回退到已知好点 互补——那条管「回退时被回退的那段不能从日志里消失」，本条管「灰度推进时先升级哪一侧」。
- 提升层：工作流 / 可复用 Skill。触发词：灰度升级、滚动升级、读侧、功能开关、坏数据不报错、版本错配。

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
## 超时不是一个数：默认值随触发类型分档、可调上限随套餐分档，且超时后只保留「已成功步骤」的日志（来源：pipedream.com/docs/workflows/limits 2026-09-29 r296-C 独立 curl 取 .md 原文核验；与 §2.41.0 容量上限二分 互补——那条管"能不能提升"，本条管"同一平台里超时有几套默认值"）
- 原文："HTTP and Email-triggered workflows default to **30 seconds** per execution. — Cron-triggered workflows default to **60 seconds** per execution."；上限表：Free 300 秒（5 分钟）/ Paid 750 秒（12.5 分钟）；"Any partial logs and observability associated with code cells that **ran successfully before the timeout** will be attached to the event in the UI, so you can examine the state of your workflow and troubleshoot where it may have failed."；磁盘 /tmp 2GB "This limit cannot be raised."
- 判据：① **同步入口与定时入口的超时预算本就不同**——HTTP/Email 是有人（或有系统）在等响应，默认 30 秒；Cron 没人等，默认 60 秒；把定时任务的预算套到 webhook 上，或者反过来，都会拿到不该有的超时；排查超时先确认**这个工作流的触发类型决定了它拿的是哪一套默认值**；② **"默认值"与"可调上限"是两个参数**——默认值能改，但天花板由套餐决定；用户说"我已经调到最大了还是超时"，要先问是哪个套餐，因为"最大"对免费档是 5 分钟、对付费档是 12.5 分钟；③ **超时不等于日志全丢，但丢的恰好是最需要的那一块**：已成功 cell 的日志会被附到事件上，而**正在跑的那一步的中间态拿不到**——所以超时类故障能确认"跑到哪一步"，不能确认"那一步内部卡在哪"；需要后者就得自己写中间检查点（与 §每一步都落检查点 同向）。
- 提升层：工具/工作流。触发词：超时默认值、30s vs 60s、触发类型决定超时、套餐决定超时上限、超时后部分日志、/tmp 2GB 不可提升。

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

## 按「调用方身份」计数的闸门必须自证生效：反向代理会让它整体失效（来源：Flowise rate-limit 本机实拉，r326B）
- **原文**：「The rate limitation is **tracked by IP-address**. If you have deployed Flowise on cloud service, you'll have to set `NUMBER_OF_PROXIES`」；「most likely you are behind a proxy/load balancer. **Therefore, the rate limit might not be able to work.**」；官方校验闭环=逐档 +1 直到 `{{hosted_url}}/api/v1/ip` 回显的 IP 与你的实际 IP 一致。
- **判据**：① **「按身份计数」的闸门（IP / 租户 / 客户端）上线验收必须做一次身份回显比对**，否则测的是没被限流的那条路径而全绿；失效形态是**完全不工作**（不是变宽），最危险。② 平台应自带「回显我看到的客户端身份」端点——没有自证端点的限流 = 不可验证的限流。③ 修复方向是让平台认识真实拓扑（代理档数），而不是放宽阈值。
- **提升层**：工具/安全边界。触发词：限流按 IP、NUMBER_OF_PROXIES、代理后限流失效、身份回显自证、闸门可验证性。
