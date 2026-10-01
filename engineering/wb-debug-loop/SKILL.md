---
name: wb-debug-loop
description: >-
  有纪律的排障循环（诊断 bug / 报错 / 性能回归的根因）。当出现报错、崩溃、白屏、500、超时、测试失败、行为与预期不符、构建/部署跑不起来、性能变慢、内存泄漏、复现不了的怪问题时应用：重现 → 最小化 → 假设 → 验证 → 修复 → 回归测试。禁止"先改再猜"、禁止一次改多处、禁止靠重启/清缓存糊过去。另含「修复验证」：补丁是待验证假设，不从 diff 大小/作者/上游一致/原 PoC 失效推成功，须测同根因变体与兄弟路径。触发词：报错、错误、异常、崩溃、闪退、白屏、跑不起来、不生效、没反应、失败、失败原因、找不到原因、查不出、定位、排查、排障、根因、复现、回归、性能变慢、卡顿、内存泄漏、超时、内存溢出、debug、troubleshooting、root cause、stack trace、崩溃日志、模型行为、幻觉、选型、补丁、修复验证、patch、变体、这算 bug 吗、加固算修复吗、兜底不是修复、重试掩盖、静默降级、缓解不是修复、改指令算修了吗、装了不生效、静默失败、幻影字段、声明但未写入。不适用：只是"该不该写这段代码"的取舍（走 wb-ponytail）、多步实现任务的规划与交付（走 wb-spec-driven）、任务级"点名目标全量覆盖 / 失败换路攻坚"纪律（走 wb-execute-discipline）。、一直在重复、转圈、卡死检测、迭代上限定多少、并行单元重名、工具结果用错、喂给判定的字段要人话、验证证据要让外行能下结论、先找仓库既有规程、失败声明、failure cause、只报原因不报对策、分类不出就原样抛、等待提示、错误负载缺省字段、OOM 恢复、中断恢复、取消不等于丢弃、半成品保留、完成标记游标、重试准入、重试不生效、参数冲突、单次超时与总时长、重试留痕、兜底范围、提前终止原因、结束原因可见、主动退出留痕、诊断只读、修复须批准、diagnose不执行repair、读写分离、终态退出码、超时携带诊断、失败不二次变更、幂等护栏、轮询分批、卡住运行恢复
version: 1.105.0
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

## 等待/轮询/卡住运行处置（来源：OpenClaw `ci/watching-runs.md`，2026-09-30 实拉）

1. **终态用不同退出码区分，超时携带诊断载荷**：GREEN=0 / FAILING=15 / TIMEOUT=16 —— 成功、失败、超时是可区分信号而非笼统「未完成」；TIMEOUT 须附带最后聚合 + 待处理计数诊断载荷。判据：有等待/轮询的环节，失败与超时必须分码返回、超时码带诊断上下文。
2. **失败/不确定状态绝不自动触发二次变更（幂等护栏）**：不确定态禁止自动重试/二次写入，否则放大副作用；恢复须是显式人工/批准动作。判据：不确定态默认不自愈，恢复动作显式且可审计。
3. **轮询分批拉取 + 超额缓存续拉**：每轮最多读 32 条缺失记录，超额保持 pending 从缓存 resume，不一次性拉全量压垮下游。判据：长列表轮询设每轮上限，超出走增量续拉。

## 长命周期任务须有"故障计数分型 + 达阈自动停用 + 停用原因写回状态对象"：运行失败与计算错误阈值不同，运维面才能区分"没人用"与"用坏了"（来源：docs.openclaw.ai/automation/cron-jobs/delivery、help.make.com/llms.txt、docs.n8n.io/.../durable-scheduler.md，2026-10-01 r362-Q-C 实拉；回答 WB r288 ③）
- 判据：① openclaw cron 在 **10 次执行故障** 或 **3 次调度计算错误** 后**自动禁用**，原因写入 `state.autoDisabled.reason`（两类故障阈值不同）；告警是"连续 2 次崩溃 + 60 分钟冷却"，与停用阈值分离。② 跨平台口径（回答 r288 ③）：Make=无内容性自动停用，只有 credit 触顶后管理员暂停场景；n8n durable-scheduler=用 `quarantine 86400` 隔离态代替停用，failed 保留 604800；Activepieces=本轮路径 404 未取到。⇒ 停用要有原因字段与阈值分型，否则运维面无法区分"没人用"和"用坏了"。
- 提升层：工作流。触发词：故障计数分型、达阈自动停用、autoDisabled.reason、运行失败10次/计算错误3次、quarantine 代替停用。

## 学习轮沉淀区（本段）
（r历史 起的连续学习轮章节共 115 章已下沉 references/knowledge-base.md §≤200迁移，正文留此指针）

## Harness 自改进与 trace 复用簇（细则已下沉 KB）
- 技能级记忆、Harness 工程与三阶段自改进、后台 review fork、视觉双扩展、trace 失败模式清单、trace→evaluator、harness 演进三问——**七条同源，完整论证见** [references/knowledge-base.md](references/knowledge-base.md) §Harness 与 trace 自改进簇。
## 学习轮沉淀区（本段）
（r历史 起的连续学习轮章节共 236 章已下沉 references/knowledge-base.md §≤200迁移，正文留此指针）

## Qoder 净新（2026-09-27 · 全量消化）
- **偏差点重启-替代生成法**（arXiv 2609.29154 SkillPivot）：修技能/排查失败 run 用三信号（执行有效性/目标进度/动作多样性）定位**首个偏差点**，从偏差前缀重放生成"同一历史下的成功替代段"，只把替代段与偏差前缀的差异反哺进修订——不把整条失败轨迹当废样本（与受控扰动审计互补：那管事前找缝隙，这管事后从真实失败挖最小修订）。

## 数据钉定（input pinning）隔离待测单元：dev-only 钉子、生产忽略（来源：docs.n8n.io types-of-executions 6,643B，2026-09-30 r327B 独立实拉）
- **原文**：`On future runs, instead of executing the pinned node, n8n will substitute the pinned data and continue following the flow logic... Production executions ignore all pinned data.`
- **判据**：① 迭代调试时把上游节点输出**钉死为固定样本**，下游只在这一固定输入上反复试错 → 把「单元待测」与「上游可变性/外部调用成本」解耦，避免每次改一行都要重打整条链路或重复打外部服务。② 钉子是**开发态构造物**，生产执行必须全部忽略（否则测试夹具污染真实数据 + 跳过本应执行的真实逻辑）。③ 与「局部执行」配合：钉输入 + 只跑待测节点 = 最小可复现调试闭包。提升层：工具/工作流。触发词：数据钉定、input pinning、确定性迭代、dev-only 夹具、生产忽略 pin。

## 局部执行（partial execution）：重跑范围可靶向，不整流产跑（来源：docs.n8n.io types-of-executions 6,643B，2026-09-30 r327B 独立实拉）
- **原文**：`Partial executions are manual executions that only run a subset of your workflow nodes... executes the specific node and any preceding nodes required to fill in its input data.`
- **判据**：① 重跑/复现应**只跑待测节点 + 喂它所需的最小前驱**，而非把整条工作流从头跑一遍——降低复现成本、避免重触发副作用节点。② 局部执行仍需触发拓扑（须有一条 trigger 描述「何时执行」），不是任意节点都能起跑 ⇒ 靶向重跑要在「最小前驱」与「拓扑合法性」之间取平衡。③ 与「数据钉定」是同一调试哲学的两面：一个控输入、一个控范围。提升层：工具/工作流。触发词：局部执行、partial execution、靶向重跑、只跑待测节点、最小前驱。
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