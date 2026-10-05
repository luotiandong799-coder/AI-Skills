---
name: agent-guild
description: |
  智能体协会（agent-guild）— cross-agent shared memory. 本机多个 AI agent 共享
  同一份身份、规则、记忆与交接消息 — 纯本地 Markdown/JSON，无服务器。

  触发（任何自然等价表达都算）：
  · 身份/习惯："我是谁" "我的身份/习惯/偏好" "who am I" "my routine"
  · 回忆/历史："你记得吗" "之前聊过" "上次我们" "what did we discuss"
  · 写记忆："帮我记住" "记一下" "沉淀一下" "remember this" "记到日志"
  · 跨 agent："告诉其他 agent" "交接给" "让 XX 也知道" "hand off to"
  · 当前状态："现在在做什么" "当前任务/焦点/进度" "current focus"
  · 数据卫生："整理一下协会" "清理过期数据" "协会瘦身/归档" "防止数据劣化"
    "groom" "cleanup" "archive old data"
  · 加入："加入协会" "初始化协会" "join agent guild" "install this skill"

  能力：读/写共享身份、规则、焦点；收件箱交接；每日日志；跨 agent 学习台账
  （错误/纠正/特性请求 → 复发追踪 → 晋升规则或萃取共享 skill）；数据卫生
  （bootstrap 后自动 groom：过期日志/焦点/台账归档、审计轮转，防数据劣化）；
  `ag init/adopt/bootstrap/doctor/groom/upgrade/learn/review/resolve`
  （upgrade **只查新版并提示，绝不自动更新**——更新须用户授权，见 §升级纪律）。
  未加入？先跑 docs/ONBOARDING.md。、审批模式、分层授权、只读免审、gated actions、Manual/Auto/YOLO、Auto≠沙箱、授权启发式、越权复核、目标驱动、goal、rubric、验收标准、定义完成、粘滞质量门、amend/pause/resume、逐轮评分、记忆与技能、AGENTS.md、按需加载、always-loaded、on-demand、全局vs项目
slug: agent-guild
displayName: 智能体协会 Agent Guild
protocol_version: "3.2"
version: "1.81.0"
license: MIT
homepage: https://github.com/dqsjqian/agent-guild
repository: https://github.com/dqsjqian/agent-guild
agent_created: true
display_name: "智能体协会 Agent Guild"
display_name_en: "Agent Guild"
description_zh: "跨 agent 共享记忆协议：本机多个 AI agent 共享身份、规则、记忆与交接消息，纯本地 Markdown/JSON，无服务器"
description_en: "Cross-agent shared memory protocol: agents on one machine share identity, rules, memory and handoff messages. Local-only Markdown/JSON, no server."
---

# Agent Guild — Runtime Skill

> Local-first cross-agent shared memory. Join once, share identity/rules/focus
> across every agent on this machine. Data lives at `~/.agent-guild/`
> (plaintext, yours, never uploaded).

`SKILL_DIR` below means the directory containing this file. CLI entry point:
`python3 <SKILL_DIR>/scripts/ag.py` (referred to as `ag`). Requires Python 3.9+
(stdlib only, no third-party packages). On Windows use `python` instead of
`python3` if that is what your PATH exposes.

## Mandatory Session Contract (once per session, MUST)（原文已下沉 agent-guild/references/knowledge-base.md §r349C 下沉）
## Self-check (each session, before real work)

```bash
# 1. registered?
grep -q '"<your-agent-name>"' ~/.agent-guild/registry.json && echo registered || echo not_registered
# 2. protocol version compatible?
grep -E '"protocol_version"' ~/.agent-guild/skills/agent-guild/manifest.json | head -1
```
Not registered → run onboarding first. Central major version > yours → re-run
onboarding from the top.

## The `ag` CLI — use it for all writes

Writes to shared files are atomic + audited when done through the CLI
(zero-dependency Python, stdlib only). Reads stay plain file reads.

```bash
AG="python3 <SKILL_DIR>/scripts/ag.py"

$AG init <agent>                    # bootstrap the guild (idempotent)
$AG bootstrap <agent>               # read ALL shared context in one shot
$AG adopt <agent>                   # dry-run: what of mine belongs in the guild?
$AG adopt <agent> --apply           # move it in + symlink back
$AG doctor                          # dangling links / stale paths / drift
$AG status                          # who is registered
$AG register <agent> <home> <tier>  # join (tier: symlink|copy|readonly)
$AG last-seen <agent>               # refresh presence
echo "<body>" | $AG send <dst> <topic>        # handoff message
echo "<body>" | $AG log <agent> "<title>"     # daily log
echo "<body>" | $AG focus <agent> "<title>"   # update current-focus
echo "<body>" | $AG learn <agent> <kind> "<summary>"  # learning ledger entry
                                             #   kind: learning|error|featreq
                                             #   opts: --area X --priority Y --pattern-key K
$AG review                          # pending stats + promotion candidates
$AG resolve <ID> ["note"]           # mark entry resolved (+ note)
$AG groom [--dry-run]               # data hygiene: archive expired data
                                    #   (auto-runs after bootstrap, 1/day)
$AG audit                           # audit trail of shared writes
$AG prune 30                        # list idle agents
```

If the CLI is unavailable (no Python, sandboxed runtime), fall back to the
manual file operations below — Edit in place, never Write-overwrite a shared
file. Every capability in this skill is reachable by plain file reads/writes;
the CLI only adds atomicity and an audit trail.

## 升级纪律（禁止自动升级）

外部组件（Skill / MCP / 插件 / 外部脚本 / 权限相关组件）一律：

```
检查更新 → 发现新版 → 告知变化与风险 → 用户明确授权 → 更新 → 验证
```

- **禁止**：发现新版就自动升级。`ag upgrade` 只做「查询 + 提示」，不落地替换。
- 更新前必须能说明：改了什么、是否影响现有配置/数据、如何回滚。
- 更新后必须验证（doctor / 冒烟），失败则回滚到上一版本。

<!-- 2026-10-03 r396B 下沉：Capability 1–4（读共享上下文/更新焦点/收件箱/每日日志）→ references/knowledge-base.md §Capability 1-4 -->
## Capability 1–4 — 读共享用户上下文 / 更新当前焦点 / 检查收件箱与发消息 / 每日日志（原文已下沉 references/knowledge-base.md §Capability 1-4，2026-10-03 r396B；触发词：共享用户上下文、USER.md、current-focus、inbox、handoff、daily log、跨 agent 交接）
## Capability 4 — Daily log（原文已下沉 references/knowledge-base.md §Capability 4-10 下沉，2026-10-03 r408A）
## Failure modes

- Some files missing → read what exists, note the rest, don't block.
- `registry.json` not writable → log the issue, proceed read-only.
- Inbox file in an unexpected format → read anyway, reply with a structured request for clarity.

## Spec

- Manifest: `manifest.json`
- Onboarding (one-time): `docs/ONBOARDING.md`
- Conventions: `docs/CONVENTIONS.md`
- Learning ledger (self-improvement): `docs/LEARNINGS.md`
- Repository: https://github.com/dqsjqian/agent-guild
- License: MIT

## Agent 自主权分三档：只读免审，gated 需审，Auto≠沙箱

> 原文已下沉 `references/knowledge-base.md §r395-ag`（保持原文零删减）。
## HITL 安全锁插在「执行通道层」而非「对话层」（来源：阿里云 Agent Skills 门户 skills.aliyun.com HITL 插件，2026-09-28 r213-A 独立实拉）
- **实证**：阿里云 Skills 门户内置 HITL 插件，在 **Agent 与 Aliyun CLI 之间**插入检查点——高风险命令（删除/计费/对外暴露）在执行前被识别并**暂停等待人工确认**；风险评级由**云端风险评级服务**做（非本地规则库）。
- **判据**：① 安全锁的**拦截点应落在工具调用执行通道（CLI wrapper / 工具层），不是对话层**——对话层的"请确认"可被模型自说自话绕过，通道层拦截才是物理阻断；② 风险分级可**外包给独立远端服务**（云端评级）而非写死在 agent 规则里，分级随服务演进、不污染本地规则面。与 §三档审批 分工：三档是"agent 自身审批模式"，本条是"在 agent 之外的执行通道上架一道物理检查点 + 评级外包"。
- 提升层：工作流 / 安全边界。触发词：HITL、执行通道拦截、CLI wrapper 检查点、云端风险评级、高风险暂停、物理阻断。

## 目标驱动：让 agent 自己起草验收标准并逐轮评分（来源：LangChain Deep Agents Code goals-and-rubrics，2026-09-23 r150-B 独立实拉首读，清单外新信源）

- **goal：给目标，让 agent 起草验收标准再开工**：目标有生命周期，被接受后跨轮保持活跃，直到完成/阻塞/暂停/清除；每轮后续都按验收标准评分。适合开放任务——把"要做成什么样"显式化成定义完成。
- **rubric：已知标准就当质量门**：可粘滞跨轮（每轮都卡）或只卡下一轮。`/rubric set` 设持久标准，`/rubric next` 只卡当次。非交互模式用 `--rubric` 直接给。
- **amend/pause/resume 不重放**：改目标不必取消当前任务重来——`/goal amend` 协调改目标与标准、`/goal pause` 暂存、`/goal resume` 从现有对话续上。判据：调整方向不该付出"重跑一遍"的代价。
- **与"先立规约"的互补**：spec-driven 是人在动手前写验收；这里是 agent 在拿到目标后自己起草、人审后执行。两者都要求"完成"先于"动手"，差异在谁起草。
- 与 §三档审批 的分工：那条管"能不能自己改"；本条管"改完怎么算改好、怎么逐轮验收"。

## 记忆与技能是频谱：常驻上下文 vs 按需加载（来源：LangChain Deep Agents Code memory-and-skills，2026-09-23 r150-B 独立实拉首读，清单外新信源）

- **记忆=总是加载的常驻上下文**：`AGENTS.md`（全局 `~/.deepagents/<agent>/AGENTS.md` + 项目 `.deepagents/AGENTS.md`）在会话开始就拼进 system prompt，放人格/通用偏好/跨项目约定/架构。自动记忆按主题存 `.deepagents/<agent>/memories/*.md`，任务前检索、不确定时查、新信息自动存。
- **技能=按需发现、相关才读**：agent 启动时只读每个 `SKILL.md` 的 name+description，任务匹配描述才读全文。放任务专属的工作流/最佳实践/参考文档。全局与项目技能重名时，后加载的覆盖先加载的。
- **判据：常驻 vs 按需**：通用且每次都要的放记忆（always-loaded）；任务专属、只在特定场景才用的放技能（on-demand）。不要为了"全加载"把所有知识塞进 AGENTS.md——那会撑爆上下文且稀释重点。
- **额外记忆文件要被 AGENTS.md 引用才生效**：放在 `.deepagents/` 的附加文件，启动时并不自动读，必须在 AGENTS.md 里指名，agent 需要时再去读取。
- 与 §三档审批 / §目标驱动 的分工：那两条管行为边界与验收；本条管"知识该常驻还是按需"，决定 context 装什么。

## Skill Evaluation（技能评估/淘汰/优化 · 学习闭环的一部分）

用户要求「Skill Evaluation 的 skill 学习必须做」。本学习技能除从外部信源学习外，也承担**内部技能库的健康审计**：

- **审计脚本**：`D:\腾讯AI\yt\scripts\skill_eval.py`（托管 python 运行），扫描 `D:\腾讯AI\skills` 全部 SKILL.md，产出 `D:\腾讯AI\yt\outputs\skill-eval\<日期>_eval.md`（技能总数、机检异常、重叠候选 Jaccard≥0.3）。
- **机检**：CRLF / STRAY_CR / FFFD / description≤1024，异常即 LF 化修复（repo 与 live 同步），修后重跑 sha256。
- **重叠处置**：运行时治理 vs 编写期 ≠ 重复保留；同功能层 Jaccard>0.6 才列合并/淘汰候选。**淘汰/合并属 L2，须用户确认才执行，不擅自强删。**
- **调度**：不另建自动化；作为本学习技能的职责，随现有学习循环（agent-guild 上下文）每次运行附带或周期性触发。
- 参考方法：wb-skill-authoring（评估/去重合并）、meta/knowledge-governance（重叠/归档）、agent-evolution（生命周期治理）。

<!-- 2026-09-30 r336B 下沉：r186 审计落地（Qoder r189-Q-C #5 · 0 净新）整段 → references/knowledge-base.md §r336B -->

<!-- 2026-09-29 r290 下沉：Capability 12 诊断日志与审计留痕分仓 → references/knowledge-base.md §r199-B 批 -->
> 早期两节（Capability 13 留痕范围 / Capability 14 多 Agent 编排 / Capability 15 群组式多 Agent）已零删减下沉至 references/knowledge-base.md 的 r417-ag 存档节。
<!-- 2026-10-05 r420A 下沉：Capability 16 凭据与执行体容器级物理分离 → references/knowledge-base.md §r420-ag -->

#<!-- 2026-10-01 r344A 下沉：Capability 17 记忆晋升三门整段 → references/knowledge-base.md §r344A -->

#<!-- 2026-10-04 r415 下沉：Cap35 + Cap36 → references/knowledge-base.md §r415-ag -->
> 入站准入双门与会话隔离粒度一节已零删减下沉至 references/knowledge-base.md 的 r417-ag 存档节。
<!-- 2026-10-05 r420A 下沉：评审类协作上下文一节 → references/knowledge-base.md §r420-ag -->

<!-- 2026-10-05 r420C 下沉：治理处置申诉期冻结态一节 → references/knowledge-base.md §r420-ag-C -->

<!-- 2026-10-05 r420C 下沉：说过 ≠ 记着（发消息不入队）一节 → references/knowledge-base.md §r420-ag-C -->

## 晋升收益门：只把「期望收益为正」的经验结晶成技能（来源：arXiv 2607.16621 MSCE 2026-09-28 r283-B 经 Qoder r316-Q-A 实拉取证；续 r205 §记忆晋升三门）
- **实证**：原文机制是**只把"正期望收益的 L2 策略"结晶为可调用技能**，并用 **reflection-weighted value backfilling** 把稀疏的终局反馈回传给中间步骤（基准 EvoAgentBench + LoCoMo）。
- **判据**：r205 已落的晋升三门是**频次口径**（score / recall-frequency / query-diversity）——回答"它常被用到吗"；本门是**收益口径**——回答"留住它划算吗"。**收益为负或不确定的策略不晋升**：一条被高频调用但每次都把事情带偏的经验，频次门全过、收益门不过，结晶成技能只会把错误固化。稀疏反馈还要有回传机制，否则只有终局成败可观测、中间步骤分不到功劳。
- **落地动作**：晋升候选同时过四门（频次三门 + 收益一门）；收益无法估计时**默认不晋升**，只留在日志里继续观察。
- 提升层：可复用 Skill / 工作流。触发词：晋升收益门、期望收益为正、结晶为技能、value backfilling、频次口径 vs 收益口径、不确定即不晋升。

## Capability 18 — 白名单字段的「空值语义」必须显式声明，且配置要能锁死为只读（原文已下沉 references/knowledge-base.md §r426A-ag 下沉 Cap18–Cap20；触发词：allowlist 空值语义、空等于拒绝全部、配置锁死只读）
## Capability 19 — 共享记忆里「多条条目」不等于「多份独立证据」：采纳判定要按来源族门控（原文已下沉 references/knowledge-base.md §r426A-ag 下沉 Cap18–Cap20；触发词：来源族门控、相关条目折叠为一条证据、误采纳率、错误信念复述）
## Capability 20 — 记忆检索范围就是权限范围，且扩大范围不保证更准（原文已下沉 references/knowledge-base.md §r426A-ag 下沉 Cap18–Cap20；触发词：可见面即权限、扩记忆回归、全局记忆反降）
## Cap23 / Cap24 / Cap25 沙箱边界三角（原文已下沉 references/knowledge-base.md §r418A 下沉；触发词：fail-closed 缺能力藏入口、挂载戳穿沙箱、shared 作用域、沙箱网络边界、私网不可达）

## Cap26 机器人入站是独立于人、独立于 API 的第三条通道："看得见"与"会触发"是两个开关，互聊护栏是滑动窗口不是硬阻断（来源：docs.openclaw.ai/channels/bot-loop-protection 2026-09-29 r290-B 独立 curl 实拉 5,889B；与 Cap18 入站准入双门 allowFrom+requireMention 互补——那条管人类入站，本条管 bot 入站）
- 原文：Discord/Slack 在支持 `allowBots` 的频道默认接受 bot 消息（走正常 mention 与访问规则），显式 `allowBots: false` 才关；"**Bot messages can remain visible as conversation context independently of turn admission.**"；"Pair loop protection bounds rapid exchanges between two bot identities. It is a **sliding-window rate guard**, so **slower exchanges below the budget can continue**."
- 判据：① 入站治理要回答两个**独立**问题——这条消息**能否进入上下文**（可见性）与**能否驱动一次回合**（准入）；多 agent 群里只读旁听是一等配置，不是靠拉黑；② 两个 bot 互相激发的死循环不能用"禁止 bot 触发"一刀切——代价是砍掉所有合法的 bot 协作；正确形态是**速率护栏**（窗口内超预算才停），低于预算的正常慢速对话照常跑。
- 提升层：工具。触发词：bot 入站、allowBots、可见不等于触发、滑动窗口、互聊死循环、旁听模式。

## Cap27 定时任务"没跑"有五个独立原因，其中两个是静默开关；创建者权限与投递目标是两个字段（来源：docs.openclaw.ai/automation/cron-jobs/troubleshooting 2026-09-29 r290-B 独立 curl 实拉 4,407B）
- 原文："Check the `cron.enabled` config setting and `OPENCLAW_SKIP_CRON` in the Gateway's launch environment. **Either can disable automatic runs**; clear both disable settings and restart the Gateway to enable scheduling."；"`reason: not-due` in run output means the manual run was checked with `--due` and the job was not due yet."；"`handler-unavailable` means the heartbeat service was not registered or stopped during the wait. The attempt is recorded as skipped."；"If a capped job's **stored named creator account** is unavailable, the run fails **before model/tool execution**… **changing the delivery `--account` does not change creator authority**."
- 判据：① 排查顺序 = **双静默开关（配置位 + 环境变量位，任一即全停）→ 宿主时区 vs `--tz` → 是否真的到期（`not-due` 是正常结果不是故障）→ 心跳/执行器是否注册（`handler-unavailable`）→ 创建者账号是否还在**；② 排障命令梯由粗到细（status → gateway status → automations status → list → runs → heartbeat last → logs --follow → doctor），**先确认系统级再确认作业级**，倒着查会把正常状态误判成故障；③ **投递目标 ≠ 权限主体**——改收件人不改权限，任何"换个账号重发就好了"的修复都是假修复，必须回到创建者身份。
- 提升层：工具/工作流。触发词：定时任务没跑、cron.enabled、SKIP_CRON、not-due、handler-unavailable、创建者账号、投递目标不等于权限。

## Cap28 评审权与写权同源：能看差异的人就是能推送的人，diff 面板的上下位固定为「将被更新的那一方」（来源：docs.n8n.io《Compare versions》2026-09-29 r294-A 独立 curl 取 `.md` 原文 4,906B 核验；与 Cap11 评审质量取决于给评审者什么上下文 互补——那条管"给什么"，本条管"谁有资格拿到"）
- 原文：diff 视图"displays two workflows stacked vertically"，push 时 **top=远端分支（将被写入的一方）**、pull 时 **top=本地（将被覆盖的一方）**，"In both cases, the top panel always displays the workflow that will update with changes."；"Only users who can push or pull commits for an instance can access workflow diffs: instance owners, instance admins, project admins."；变更计数 = 节点 + 连接 + 工作流一般设置三者合计。
- 判据：① **差异视图的方位必须自解释**——上下两栏的含义随方向翻转，靠记忆一定读反；正确做法是让界面（或自己的输出）明写"上面板 = 会被改的那一侧"，否则评审者会把 diff 方向读反，做出的合并决策正好相反；② **评审入口绑定写权限意味着没有"只读评审"这一档**——想让某人 review 就必须给他 push/pull 权，等于同时给了他绕过 review 直接改的能力；需要只读评审时必须另开通道（导出快照/生成补丁），不能指望平台的 diff 视图；③ 变更计数把**结构性改动与配置改动混成一个数**，评审时不要拿这个总数当改动量级（改一个全局设置和加一个节点都记 1），要展开看类型分布（新增 N / 修改 M / 删除 D）。
- 提升层：工作流/工具。触发词：workflow diff、上下面板、diff 方向读反、只读评审、评审权等于写权、变更计数。
## Cap29 同步通道的「推」与「拉」是两个独立权限，单向授权是被支持的形态；能力还受套餐与特性开关双重前置（来源：docs.n8n.io《Understand source control》2026-09-29 r294-C 独立 curl 取 `.md` 原文 1,929B 核验；与 Cap28 评审权等于写权 互补——那条说"能看 diff 就能写"，本条说"写"本身还要再拆方向）
- 原文："Instance owners and instance admins can push changes to and pull changes from the connected repository. **Project admins can push changes to the connected repository. They can't pull changes from the repository.**"；另见同页特性可用性：Business/Enterprise 套餐 + "You must be an n8n instance owner or instance admin to **enable and configure** source control"。
- 判据：① **把 Git 权限当成四格矩阵而不是一个开关**——启用配置 / 推 / 拉 / 看差异各自独立，官方就实现了"能推不能拉"这一格；设计多 agent 或多成员协作时，按方向授权比按角色授权更贴合真实风险（能推 = 能污染上游，能拉 = 能被上游污染，两者危害不同）；② **"有这个功能"不等于"这个功能开着"**：套餐位（Business/Enterprise）与实例特性开关是两层前置，排障"为什么没有 Git 菜单"要先分清是没买还是没开；③ 单向授权要有配套——只能推不能拉的人无法自证与上游一致，给他推权就要另给一条只读的比对/快照通道，否则他把上游改坏了自己也不知道。
- 提升层：工作流/工具。触发词：project admin 能推不能拉、推拉分离、单向授权、source control 权限、套餐加开关双前置。

## Cap30 告警可以分层静音，但「系统把你停掉了」那一类不可静音；跳过与失败是两个独立计数器（来源：docs.openclaw.ai《Automation delivery》2026-09-29 r294-C 独立 curl 取 `.md` 原文 16,578B 核验；与 Cap27 定时任务没跑的五个原因 互补——那条管"为什么不跑"，本条管"跑了之后谁被告知"）
- 原文：`job.failureAlert: false` 关掉该任务的执行与投递失败告警，"The **auto-disable safety notification remains active**"；全局 `cron.failureAlert.enabled:false` 关继承，而 per-job 的 `failureAlert` 对象"**activates and tunes the policy even when the job had no existing route**"；`delivery.bestEffort:true` 抑制继承/默认告警，"An explicit per-job `failureAlert` remains **authoritative**"；"`failureAlert.includeSkipped:true` opts … into repeated skipped-run alerts. **Skipped runs keep a separate consecutive-skip counter, so they do not affect execution-error backoff.**"；`delivery.failureDestination` "is only supported on `sessionTarget="isolated"` jobs unless the primary delivery mode is `webhook`."
- 判据：① **静音是分层的（全局继承 → 投递模式 → 单任务显式），且显式永远赢**——所以"我明明关了告警怎么还发"的答案通常是某个 job 上有显式对象；反过来要静音必须指名到那一层，不能假设关全局就全关；② **安全类告警要设计成不可静音**——用户可以选择不听"这次失败了"，但不能选择不听"因为这个任务一直失败，我把它停了"；凡是会自动改变系统行为的动作（自动禁用、自动降级、自动回收），其通知必须与普通失败告警分通道且不可被同一开关关掉；③ **跳过 ≠ 失败，必须两个计数器**——把 skipped 计入 failure backoff 会让"正常跳过"被放大成"连续失败"并触发退避甚至停用；④ 失败投递目的地带**前置条件**（隔离会话或 webhook 主投递），配了不生效时先查前置而不是查地址。
- 提升层：工具/工作流。触发词：failureAlert、bestEffort、安全通知不可静音、auto-disable、skipped 独立计数器、failureDestination 前置条件、显式覆盖继承。

## Cap31 审计账本要声明「它证明不了什么」：只存元数据不存内容、不构成授权证据、缺授权绝不事后补造（来源：docs.openclaw.ai《Audit history》2026-09-29 r296-B 独立 curl 取 .md 原文 36,899B 核验；与 §Capability 13「留痕范围由显式输出决定」互补——那条管单次记录装哪些字段，本条管整本账本的能力边界）
- 原文："The ledger stores identity, ordering, provenance, action, status, and normalized outcome codes. It **never stores** prompts, message bodies, tool arguments, tool results, attachments, filenames, URLs, command output, or raw error text."；"it does not make the activity ledger lossless and **does not turn audit records into authorization evidence**."；"Auto-review, full-access policy, native hook decisions, and requests rejected before operator routing have no operator-owned row and remain unsupported as operator-approval evidence; **later tool events never manufacture one**."
- 判据：① **审计系统必须写明"证明不了什么"，否则用户会拿它当它承担不了的东西用**——这本账本能回答"谁在什么时候跑了、怎么结束的"，但**不能当授权凭据**；设计任何审计/留痕设施都要同时输出能力边界清单（不存什么、不算什么证据），边界声明与留存内容同等重要；② **缺失的授权记录不许由后续行为反推补造**——一次执行如果没有人工审批行，后面发生了多少工具事件都不能"凑出"一条审批证据；事后再造一条等于把"未审批"洗成"已审批"，这是审计系统最危险的造假方式；③ **多来源合并只 join 不复制**：审批、外发投递、定时任务各自是 owner-native 源，"Run inspection merges both sources directly; **neither is copied into the generic decision-fact table**"——复制一份进通用表会产生第二份可能过期的真相；④ **关联键不足时如实报 unknown**："`runId` alone never joins one of these rows to an execution. Legacy, missing, deleted, corrupt, or mismatched bindings **remain unknown or absent; they never change task behavior**"——绑定坏了不改变任务行为，也**绝不猜一个绑定填上**。
- 提升层：可观测性/治理。触发词：审计边界声明、审计不算授权证据、不补造审批行、只 join 不复制、runId 不足以关联、绑定缺失报 unknown。

## Cap32 凭据分「只写不可读」与「可读」两类，空凭据必须被拒；出网白名单没配就 fail-closed；迁移不写含明文的回滚备份（来源：docs.openclaw.ai《Secrets》2026-09-29 r296-B 独立 curl 取 .md 原文 15,672B 核验；与 §Cap16 容器级凭据分离 互补——那条管"密钥不在执行体里"，本条管"密钥存进来之后怎么被读写"）
- 原文："Secret values **never appear** in human, `--json`, or `--plain` output. `store get` refuses a `secret` entry as **write-only by design** and exits `2`. It exits `3` when the name does not exist. Environment-kind values are readable."；"A `secret` entry **may not be empty**, because an empty credential cannot be diagnosed later."；"Secret egress substitution **fails closed** until each secret has at least one exact allowed host."；"`secrets apply` **intentionally does not write rollback backups containing old plaintext values**."
- 判据：① **"读不出来"要当成设计确认而不是故障**——秘密类条目从设计上不可回读（读命令显式拒绝并用**不同退出码区分"拒绝读"与"不存在"**）；排障"取不到值"时先分清是这一类设计还是真的没配；② **空凭据必须在写入侧就拒掉**——理由不是"空值没用"而是"空凭据事后无法诊断"：一个空值和"配错了"在现象上一样，却没有任何线索可查；凡凭据类字段，**空值应视为配置错误而非缺省**；③ **出口白名单缺省方向必须是拒绝**：出网替换在"至少一个精确主机"配好之前一律不生效——与 §Cap18（白名单空=拒绝全部）同向，本条给的是**可外发凭据**这一最高风险面的官方写法；④ **回滚备份本身也是泄漏面**：迁移工具"故意不写含旧明文的备份"，靠严格预检 + 原子应用 + 失败时内存态尽力恢复来兜底——**备份策略要连"备份了什么内容"一起设计**，否则为可用性做的备份会成为最大的一份明文副本。
- 提升层：安全边界/工具。触发词：只写不可读、write-only by design、exit 2 拒绝读、空凭据被拒、egress fail-closed、allowed host、迁移不写明文备份。

> 下沉索引：Quick start (for an agent that has NOT j 等 1 节原文已移至 `references/knowledge-base.md`（按最旧批次下沉，正文只留指针）

## 争议处置按性质分通道：内容权 / 违规举报 / 命名空间各走独立入口；公开通道只收可公开证据并明确禁放私密证明；裁决按四要素（公开证据·既有使用·安全风险·用户影响）权衡；结果三态含「维持原状」且无时限承诺（来源：docs.openclaw.ai/clawhub/content-rights.md 1,166B + namespace-claims.md 4,167B，2026-09-30 r324B 独立实拉；与 §撤销与审核分层 互补——那条管“结论怎么撤”，本条管“争议往哪递”；细则见 references/knowledge-base.md §r324B）

## Cap33 技能级作用域可见性：技能只对解析出的特定 agent 可见，对其余 agent 完全缺席（来源：docs.openclaw.ai/tools/custodian-skills.md 5,298B，2026-09-30 r336B 独立实拉；与 §入站准入双门与会话隔离粒度 互补——那条管谁能进来，本条管某个技能对谁‘根本不存在’）
- **原文**：Custodian skills「load at the bundled-skill precedence tier, but only for the agent resolved by `agents.defaults.systemAgent.agentId`... For every other agent, Custodian skills are absent from discovery, snapshots, slash-command catalogs, sandbox sync, and the model-facing skills prompt」；「Normal skill controls still apply... agent skill allowlists can narrow the final set.」
- **判据**：① **可见性是‘默认不存在、按身份显式出现’的开关，不是‘默认全有、按名单删’**——一个技能可以只对某一个被解析出的系统 agent 加载，对其它所有 agent 从发现/快照/目录/沙箱同步/提示词里彻底消失（不是‘可见但禁用’）；② **作用域锁与 allowlist 是两件事**：作用域决定‘这个技能根本存不存在于你的世界’，allowlist 在‘存在’之上再收窄‘你能用哪几个’；先定作用域再谈收窄；③ 与跨 agent 共享纪律一致——共享记忆管‘谁读得到’，技能可见性管‘谁装得上’，两者都按身份声明而非默认广播；④ 落地到 WB：技能分发时若某技能只服务一个角色 agent，配置为‘仅该 agent 可见’，避免污染其它 agent 的技能提示词与发现面。
- 提升层：工作流/安全边界。触发词：技能级作用域可见性、role-scoped skill、仅 systemAgent 可见、discovery 缺席、作用域锁、allowlist 收窄。

## Cap34 记忆分四层各司其职；超限只在「注入侧」截断且磁盘完整，截断本身是分层迁移信号；偏好变更就地取代而非追加矛盾条目（来源：docs.openclaw.ai/concepts/memory.md 15,623B，2026-10-01 r340B 独立 curl 实拉逐串命中；与 §争议按性质分通道 互补——那条管争议往哪递，本条管记忆往哪写）
- **原文**：四文件 = `USER.md`（稳定偏好/画像，**写成指令式**，带 observed-date 与 active/superseded 元数据）/ `MEMORY.md`（**durable non-profile facts** 与长期决策，「It is **not a raw transcript, daily log, or exhaustive archive**」）/ `memory/YYYY-MM-DD.md`（工作层：细节、观察、原始上下文，**不进每次 bootstrap**）/ `DREAMS.md`（后台整合摘要，供人复核）；「When a preference changes, **supersede it in place instead of appending a contradictory active directive**」；「If `MEMORY.md` grows past the bootstrap file budget, OpenClaw **keeps the file on disk intact but truncates the copy injected into context**. **Treat that as a signal** to move detailed material into `memory/*.md`」；「The default heartbeat prompt **performs no memory maintenance on its own**」。
- **判据**：① **共享记忆必须分层，且各层的加载策略不同**：画像层（少量、每次带）/ 长期层（精选、启动时带）/ 日志层（详尽、按需检索不常驻）/ 整合层（后台产出、供人复核）。把日志层当长期层用，结果是启动时被原始流水淹没；把长期层当日志层用，结果是耐久事实被细节挤掉。② **超限的正确处置是只截注入副本、磁盘保持完整**：文件在盘上不受损，被截断的只是送进上下文的那一份。⇒  truncation 不是数据丢失，是**注入预算的告警**；收到这个信号应做的是分层迁移（把细节挪到日志层、长期层只留耐久摘要），而不是删内容或盲目上调预算。③ **偏好变更就地取代**：偏好变了就在原条目上标记 superseded 并改写，**不追加一条与之矛盾的活跃指令**。⇒ 两条互相矛盾的活跃偏好同时存在时，读取方无从裁决，实际行为取决于谁后加载——这是最难排查的一类漂移。④ **后台整合与主动记录是两条独立通道**：心跳提示本身不做记忆维护，整合由后台 sweep 负责、主动落盘由工作中的 agent 负责。⇒ 不能因为有自动整合就不写，也不能因为会写就指望自动整合来兜底分层。
- **提升层**：工作流/记忆治理。触发词：记忆四层、USER/MEMORY/日志/DREAMS、不追加矛盾偏好、supersede in place、注入侧截断、磁盘完整、截断即迁移信号、心跳不维护记忆。

## Cap36 客户端凭据在服务端按终端用户签发、短时效并绑定来源白名单；限流必须可被程序读取（来源：pipedream.com/docs `connect/api-reference/create-connect-token` 9,194B，2026-10-01 r344C 独立 curl 实拉；与 §Cap32 只写不可读 / §Cap18 白名单空=拒绝 互补——那两条管"密钥存进来之后怎么被读写""白名单缺省方向"，本条管"发给浏览器的那一枚短令牌长什么样"）
- **原文**："To securely scope connection to a specific end user, **on your server**, you retrieve a **short-lived token** for that user, and return that token to your frontend."；"When using the Connect API to make requests **from a client environment like a browser**, you **must** specify the **allowed origins** for the token. Otherwise, this field is optional."；429 响应同时给 `Retry-After`、`X-RateLimit-Limit`、`X-RateLimit-Remaining`（"always 0 when throttled"）、`X-RateLimit-Reset`。
- **判据**：① **"谁在连"必须由服务端决定**——连接/授权类令牌在服务端按终端用户单独签发并短时效，前端只拿凭证；把一枚通用长期令牌放在前端，等于把"以谁的名义"交给浏览器；② **凡会离开服务端的令牌必须带来源白名单**，且这是**必填**（原文用 must），不是"可选加固"——否则任何页面都能拿着它调；③ **限流的四个头要齐着给**（何时可重试 / 上限 / 剩余 / 重置时刻）：只回一个 `Throttled` 等于让调用方靠猜退避，猜错就是把瞬时抖动放大成雪崩。
- 提升层：安全边界/工具。触发词：短时效令牌、服务端签发、allowed_origins、来源白名单、浏览器侧令牌、限流四头、Retry-After、X-RateLimit。

## 拒绝/封禁名单必须按「能力等价集」枚举，不能按工具名点杀（来源：docs.openclaw.ai/gateway/config-tools/tool-policy.md 18,865B，2026-10-01 r349C 独立 curl 实拉，`does not deny `apply_patch`` 逐串命中；经 Qoder r368-Q-C 提名）
- 原文：「`deny: ["write"]` **does not deny `apply_patch`**」。
- 判据：① **按名字写的 deny 只覆盖同名工具，名字不同的等价能力工具整个逃逸** ⇒ 「已经禁了写操作」这类断言，只要没枚举等价能力集就站不住；审计拒绝名单要问「还有哪些工具能达成同一效果」。② 与既有「授权清单覆盖语义」不同维：那条管 **allow 的覆盖与追加**（谁的授权盖过谁），本条管 **deny 的逃逸面**（哪种写法根本没被拦住）。③ 正向表述必须可机检：给出等价能力清单并逐项验证被拒，而不是给出一条正则或名字。
- 提升层：工作流/安全边界。触发词：deny 不覆盖 apply_patch、按能力等价集枚举、拒绝名单逃逸面、按名点杀失效、同名工具才被拦。

## Cap37 审批挂在哪一级决定它拦不拦得住：流程级检查点 vs 工具级拦截；驳回是「反馈 + 有界回环」不是布尔值；外发审批链接把审批权移出账号体系（来源：docs.flowiseai.com `tutorials/human-in-the-loop.md` 15,347B + `using-flowise/monitoring.md` 7,765B，2026-10-02 r352A 独立 curl 实拉逐串命中；与 §HITL 执行通道层 互补——那条管拦截点在哪一层，本条管挂在哪一级对象上）
- **原文**：「There are 2 ways human in the loop can be used: Using **Human Input** node to halt the execution / Enable **Require Human Input** for Agent's tools」；「When Require Human Input is enabled, we place an additional checkpoint **after tool calls are detected**」；回环节点「**Max Loop Count**: 5 (prevents infinite loops)」，驳回分支「Send feedback and loop back to the agent for improvements」；轨迹分享「The execution trace is now available as a **public link**… **Users outside of Flowise can reject or approve**」；监控「`/api/v1/metrics` endpoint … **requires API key authentication**」且「only **high-level metrics** such as API requests, counts of flows/predictions are tracked. For details node by node observability, we recommend using Analytic」。
- **判据**：① **审批有两个挂载点，粒度不同效果差一个量级**——流程级检查点只拦你画好的那一条路径，agent 自主改道就可能整体绕过；工具级（`Require Human Input`）挂在工具本身，**无论 agent 怎么编排、什么时候决定调用都被拦**。⇒ 凡要求「这个动作一定经过人」的，挂工具级；只挂流程级等于把保证寄托在 agent 会走那条路上。② **驳回不是布尔值，是「拒绝 + 可执行的修改意见 + 有界回环」**（反馈回灌 agent + `Max Loop Count` 封顶）：只有布尔驳回，人只能反复手动重来；没有上限的回环则打转成死循环。与 §Cap14 迭代上限 互补——那条说自修循环要设上限，本条补上：上限之外还必须有反馈回路，否则上限只是把死循环变成「放弃」。③ **把执行轨迹做成公开链接外发审批，等于在账号体系之外开了第二条授权路径**——链接本身就是凭证（与 §Cap28「评审权=写权」正好相反：那条里能评审就必须能写，这里不能写的人也能批准）。⇒ 凡用分享链接/快照实现外部评审，必须带时效与范围，并把链接产生的批准与账号内的批准进同一本审计账，不能因「人不在系统里」就漏记。④ **观测面自身是被保护面，且内建指标只到聚合层**：指标端点要 API key（观测通道不是免费旁路），默认只有 API 请求数 / 流程数这类高层计数，逐节点可观测要显式开关或外接。⇒ 说「有监控」时必须分清聚合层与节点层，把聚合指标当成「出了问题能查到」是自欺。
- 提升层：工作流/安全边界。触发词：HITL 粒度、流程级 vs 工具级、Require Human Input、驳回带反馈、有界回环、外发审批链接、链接即凭证、评审权脱离账号、观测端点鉴权、聚合指标 vs 节点级可观测。

## Cap42 执行身份绑定：共享的是凭据模板不是授权；管理权不含使用权；删模板级联删掉别人的连接（来源：docs.n8n.io `administer/manage-credentials/end-user-credentials.md` 9,720B + `verify-user-identity/use-saml/manage-users-with-saml.md` 1,830B + `follow-best-practices.md` 2,455B，2026-10-03 r390A 独立 curl 取 `.md` 原文实拉；与 §Cap32 只写不可读 / §Cap40 权限组合 互补——那两条管"密钥怎么读写""权限怎么组合"，本条管"这次执行是以谁的身份跑的、跑出来的数据归谁看"）
- （原文+判据已下沉 references/knowledge-base.md §r425A-ag）
- 提升层：安全边界 / 工作流。触发词：终端用户凭据、执行身份、模板 vs 连接、管理权不含使用权、admin 只见 redacted、删模板级联删连接、触发权限第二道门。

## Cap43 会话键相同不等于会话合并：取消半径是 agent 不是 key；隔离与归并是两个方向的配置；隐私模式必须声明「防谁」（来源：docs.openclaw.ai/concepts/session 22,767B，2026-10-03 r390B 独立 curl 取 `.md` 原文实拉；与 §入站准入双门 / §Cap35 改向与中止 互补——那两条管谁能进来、怎么改向，本条管进来之后上下文归谁、取消动作波及多远）
- （原文+判据已下沉 references/knowledge-base.md §r425A-ag）
- 提升层：安全边界 / 工作流。触发词：会话键不合并、取消半径、DM 隔离四档、identityLinks、大小写敏感 ID、incognito 防谁、活动不延长、过期不归档、隐私模式不限制工具。

## Cap44 队列溢出是策略不是故障：三种丢弃语义与默认合成补偿；排队不借权限，撤回对已接受的运行仍生效；并发是分车道的两级预算（来源：docs.openclaw.ai/concepts/queue 17,971B，2026-10-03 r390B 独立 curl 取 `.md` 原文实拉；与 §Cap35 改向/中止/配对合成结果 互补——那条管运行中的改向语义，本条管队列满与并发预算）
- （原文+判据已下沉 references/knowledge-base.md §r425A-ag）
- 提升层：工作流 / 安全边界。触发词：队列溢出策略、drop summarize/old/new、合成补偿、cap 20、排队不借权限、撤销作用于在飞、会话 lane、两级并发预算、换运行时绕不过。

## Cap45 策略变更事件本身要入账；凭据过期应能原地重授权而不是重建（来源：help.make.com `credential-requests-reauthorization-2fa-enforcement-logs.md` 1,630B + `audit-logs.md` 8,460B，2026-10-03 r390C 独立 curl 取 `.md` 原文实拉；与 §Cap31 审计边界 / §Cap42 凭据归属 互补——那两条管账本证明不了什么、执行身份归谁，本条管"谁改了规则"与"凭据过期后怎么续"）
- （原文+判据已下沉 references/knowledge-base.md §r425A-ag）
- 提升层：治理 / 安全边界。触发词：策略变更入审计、谁关掉了 2FA 强制、reauthorize vs 重建、凭据续期、平行授权累积。

## Cap46 沙箱 / 工具策略 / 提权是三道不同的门：沙箱决定「在哪跑」，工具策略决定「能不能调用」，提权只是 exec 的逃生口；强制沙箱 fail-closed 并把 rw 压成 ro（来源：docs.openclaw.ai `gateway/sandboxing.md` 8,613B + `gateway/sandboxing/what-gets-sandboxed.md` 1,573B + `gateway/sandbox-vs-tool-policy-vs-elevated.md` 9,792B + `gateway/sandboxing/workspace-access.md` 7,119B，2026-10-03 r391A 独立 curl 取 `.md` 原文实拉；与 §Cap40 权限组合评审 / §Cap42 执行身份 互补——那两条管权限授予给谁，本条管授予之后代码在哪执行、能不能逃出去）
- **原文**：「This is **not a perfect security boundary**, but it materially limits filesystem and process access when the model does something dumb.」；三层分工「1. **Sandbox** … decides **where tools run** (sandbox backend vs host). 2. **Tool policy** … decides **which tools are available/allowed**. 3. **Elevated** … is an **exec-only escape hatch**」；「Tool allow/deny policies still apply **before** sandbox rules. If a tool is denied globally or per-agent, sandboxing doesn't bring it back.」；规则「`deny` **always wins**. If `allow` is non-empty, everything else is treated as blocked. … Tool policy is the hard stop: `/exec` cannot override a denied `exec` tool. … Tool policy filters tool availability **by name**; it does not inspect side effects inside `exec`. If `exec` is allowed, denying `write`, `edit`, or `apply_patch` **does not make shell commands read-only**.」；MCP「For sandboxed MCP servers, the sandbox tool policy is a **second allow gate** … add `bundle-mcp`, `group:plugins`, or a server-prefixed MCP tool name/glob … then **restart/reload the gateway and recapture the tool list**」；强制策略「An operator role with `sandbox: "required"` **overrides agent mode**, **cannot be escaped through elevated execution or host overrides**, and **fails closed** when its sandbox cannot be provisioned.」；「For a role-required sandbox, OpenClaw **caps configured `rw` workspace access at `ro`** and logs an `agent/sandbox` warning.」；绑定校验「OpenClaw validates bind sources **twice**: first on the normalized source path, then again after resolving through the deepest existing ancestor. Symlink-parent escapes do not bypass blocked-path or allowed-root checks.」；「Binding `/var/run/docker.sock` **effectively hands host control to the sandbox**」；「`scope: "shared"` ignores per-agent binds (only global binds apply).」
- **判据**：① **"进了沙箱"与"没有这个能力"是两件必须分开声明的事**：沙箱只决定执行位置（容器内 vs 宿主），它**不是完整安全边界**，官方原文直接说"只是模型犯傻时限制文件与进程访问"。把沙箱当成授权面，等于把一个减爆炸半径的措施当成访问控制。② **三道门的否决顺序要写明**：工具策略先于沙箱生效——全局被 deny 的工具，沙箱不会把它带回来；`deny` 恒赢且 `allow` 非空即默认全封。⇒ 排查"为什么这个工具不可用"时，先看策略再看沙箱，顺序反了会得到错误结论。③ **按名过滤意味着 exec 是策略的盲区**：允许 `exec` 时再 deny `write`/`edit`/`apply_patch` **不构成只读**，因为策略不检查 shell 命令内部干了什么。想做只读 agent 必须 deny `group:runtime`，而不是 deny 几个文件工具。④ **更强的策略会把弱配置向下压，且降级必须留痕**：creator role 的 required sandbox 覆盖 agent 自己的 mode、提权逃不出去、**供应不出来时 fail-closed**（不是退回宿主继续跑）；同时把配置里写的 `rw` 压成 `ro` 并记一条 `agent/sandbox` 警告。⇒ 任何"配置被更强的策略覆盖"的场景，沉默覆盖都是缺陷，必须留下可查的降级记录。⑤ **挂载是绕过沙箱文件面的正门，要按"交出什么"来审**：bind 会穿透沙箱文件系统（默认 rw，源码/密钥应显式 `:ro`）；路径校验做两遍（归一化后 + 解析最深存在祖先后再一次）以挡住符号链接父目录逃逸；挂 `/var/run/docker.sock` 等于把宿主机控制权交出去；`scope: shared` 会忽略 per-agent 挂载——这几条都是"看起来只是加了个目录"的操作。
- 提升层：安全边界 / 工作流。触发词：沙箱不是安全边界、where vs which、deny 恒赢、allow 非空全封、exec 是策略盲区、group:runtime、沙箱第二道门、MCP 工具消失、fail-closed、rw 压成 ro、bind 穿透、docker.sock、scope shared。

## Cap47 · 默认「自动批准」本身就是提权面；要真正关掉往往得同时动两个开关（来源：docs.openclaw.ai `gateway/config-gateway.md` 36,884B，2026-10-03 r393B 独立 curl 取 `.md` 原文实拉；与 Cap40 授权评审对象是权限组合 互补——那条管怎么审一个角色，本条管"这个门默认是开的还是关的"）

- 节点配对默认开启同主机自动批准（`autoApproveLocal` 默认 true）：同主机设备**静默配对并静默升级访问**，不需要人点确认 ⇒ 默认值就是"同主机可信"，部署前先确认这个前提成不成立。
- 关掉自动批准要**两个开关同时动**：`sshVerify=false` **并且** unset `autoApproveCidr` 列表；只关一个是无效配置——`sshVerify` 仅关闭 SSH 验证这条路，不影响 CIDR 自动批准。
- CIDR 自动批准是"可选、默认不开"的白名单，一旦配上等于把整个网段变成可信配对源；它与 SSH 验证是两条独立通道，互不影响 ⇒ 收紧一条不等于收紧了全部。
- 通则：凡是"自动批准 / 静默升级"类开关，默认态、关闭条件、以及各通道是否独立，必须在声明里写全；只写"支持手动审批"而不写"默认是自动"等于误导。

## Cap48 凭据绑定点是「进程启动」，撤销半径是「下一次启动」；profile 不可用必须 fail-closed 拒绝执行而不是回落宽路径；一次性交接用后硬删；出口白名单空数组 ≠ 放行全部（来源：docs.openclaw.ai `gateway/config-secrets-env.md` 10,309B + `gateway/config-tools.md` 7,517B 索引页 + `gateway/config-tools/github-identity.md` 17,020B，2026-10-03 r395A 独立 curl 取 `.md` 原文实拉）

- **绑定点决定撤销半径**：本地 exec 在**每次进程启动前**读取并校验所选 profile，把 access token 只放进私有子进程环境并清除同义环境变量；已启动的进程**保留启动时的 token 直到退出**，retired profile 文件要到下一次 Gateway 重启才清理 ⇒ **「改了配置」不是即时吊销**，声明里必须写清「什么时候生效、什么还在用旧凭据」。
- **profile 缺失/无 token/不安全 → 在命令开始前拒绝执行**，而不是允许回落到 native keyring（明确写 refuses the local execution before the command starts）；对**可能间接调用**该工具的命令同样适用 ⇒ 凭据不可用时的正确方向是 fail-closed，不是「先跑起来再说」。
- **状态要报「配置不可用」而不是回落到正常账号**：配置的托管 profile 缺失/无 token/损坏时状态报 `configured_unavailable`，**不**改报原生账号 ⇒ 错误码不得把「配置坏了」降级显示为「一切正常，只是换了个身份」。
- **一次性交接用后硬删**：PAT 设置路径下浏览器把粘贴的 token 放进 secret store 作为 one-use handoff，网关在拿它校验之前**硬删除该交接**；两条设置路径都只写 account-owned 私有 profile，**不改主机全局 CLI 登录与 OS keyring** ⇒ 导入凭据的第一原则是「不污染宿主已有凭据面」。
- **白名单空数组是「最小放行」不是「全部放行」**：出口代理 `allowedHosts` 存在时只放行列出的主机 + 绑定了 secret 的主机 + `bypassHosts`；**空数组表示只允许绑定或绕过的主机** ⇒ 空值语义必须逐项写清，读代码式地假设「空=不限制」会直接把策略读反。
- **盲隧道是有意的取舍**：`bypassHosts` 走认证过的 blind CONNECT，哨兵**不做替换**，因此证书固定客户端会认证失败，代价是明文不暴露 ⇒ 这类「宁可失败也不解密」的通道要在声明里点名是设计选择，而不是写成缺陷。

## Cap49 凭据回写只存「来源标记」不存解析值，且标记必须取解析前的配置快照生成（来源：docs.openclaw.ai `gateway/config-tools/sessions-and-subagents.md` 9,632B + `gateway/config-tools/custom-providers.md` 13,129B，2026-10-03 r395B 独立 curl 取 `.md` 原文实拉）

- **回写的是来源指针，不是解析结果**：被 SecretRef 管理的 provider 凭据在回写时**从 source marker 刷新**（env 引用写 `ENV_VAR_NAME`，file/exec/store 引用写 `secretref-managed`），而**不持久化解析后的密钥** ⇒ 配置里出现的是「去哪取值」，不是「值是什么」。
- **标记必须在解析前的快照上生成**：marker 持久化的来源是**生效中的 source config 快照（解析前）**，不是解析后的运行时值 ⇒ 这一顺序是关键：一旦拿解析后的值去生成标记，就等于把明文固化回了配置，脱敏在最接近落盘的那一步被破坏。
- **判重提示**：与 §Cap32「凭据只写不可读 / 空凭据必须被拒」互补——那条管能不能读回值，本条管回写时写的是值还是取值的路。

## Cap50 身份供给必须与登录同源且按提供方分隔；地址回收需要人工闸门，「看起来 404」不等于已释放；跨层身份要先从上位层撤（来源：docs.n8n.io `security/enable-ssrf-protection.md` 3,822B + `security/block-specific-nodes.md` 2,425B + `basic-configuration/use-environment-variables/ssrf-protection.md` 7,039B + pipedream.com/docs `conduit/configure/access-control.md` 13,330B + `conduit/configure/scim.md` 9,789B，2026-10-03 r395C 独立 curl 取 `.md` 原文实拉；n8n 与 Pipedream 均经各自 `llms.txt`（287,049B / 34,240B）定位）

- **供给与登录必须同源**：每个 SCIM 连接绑定**某一个** SSO provider，它推送的每个用户按该 provider 的身份 keying——这正是「供给与登录解析到同一个人」的原因，也**防止一个 provider 认领属于另一个 provider 的用户** ⇒ 打通身份同步时，先确认「这次同步用哪个登录通道」，混通道等于制造重复身份与抢号面。
- **邮箱回收是硬拒绝，且自动同步解除不了**：IdP 把某个邮箱给了另一个人时平台**拒绝**把这个账号交出去（否则等于把前任的历史与访问权交给继任）；**在 IdP 里移除前任、甚至删除其 SCIM 资源都不能解除**——记录仍占着这个地址，而 IdP 侧读起来已经是 `404` ⇒ 「看起来不存在」不等于「已被释放」，这是必须留人工闸门的场景。
- **身份标识的迁移也被拒**：试图把已供给用户的 `externalId` 移到另一个身份会被拒绝，正确做法是 remove 后重新 provision ⇒ 身份主键不可就地改，迁移路径是「删除+重建」而不是「改字段」。
- **撤销/降权要先从上位层动手**：instance admin **不能在工作区内被改名或移除**——owner 不行，SCIM 推送也不行；要下线一个运维实例的人，必须**先撤掉他的 instance 角色** ⇒ 权限是分层的，下层再高的权限也动不了上层的身份，执行顺序错了会表现为「明明执行成功却没生效」。
- **判重提示**：与 §Cap42 管理权不含使用权 / §Cap48 改配置不是即时吊销 互补——那两条管「管理权不蕴含使用权」「改配置到撤销之间有时延」，本条管「跨层身份的撤销顺序」与「自动同步解决不了的回收场景」。

## Cap51 批准绑定的是「那一刻的二进制」而非命令文本；授权是每次使用时重算的衍生关联；覆盖不全时拒绝而非假装全覆盖（来源：docs.openclaw.ai `tools/exec-approvals.md` 39,387B，2026-10-03 r396B 独立 curl 取 `.md` 原文实拉）

- **批准不是身份边界，也不是只读策略**：官方明确审批只降低误执行风险，**既不是 per-user 鉴权边界，也不是文件系统只读策略**；一旦批准，命令按所选宿主/沙箱权限改写文件 ⇒ 「走完审批」不等于「这次执行被限制了」，审批面与权限面是两个面。
- **批准绑的是可执行身份，不是命令文本**：网关侧在评审前绑定每个已解析的可执行段，**启动前再校验一次**；绑定窗口内解析结果发生变化——包括 `PATH` 上出现新的同名可执行文件——即拒绝这次运行；可写可执行文件还额外用内容 hash；受保护可执行文件只用 real-path 身份 ⇒ 被批准的是「那一刻的那个二进制」，同名的另一个文件不算数。
- **识别不了就拒绝，不假装全覆盖**：文件绑定是 best-effort，**不是对所有解释器/运行时加载路径的完整建模**；当无法唯一确定一个本地文件操作数时，官方选择**拒绝铸造这次批准运行**，而不是放行并假装覆盖 ⇒ 安全类绑定遇到「模型外」的情况，正确方向是 fail-closed 拒跑，而不是降级放行。
- **撤销在 spawn 边界生效，迟到的批准不复活**：校验在进程 spawn 前立刻执行，所以落在在飞窗口里的撤销或作业编辑**仍然赢**；而关闭或取消那一轮后，**迟到的批准无法重启它**；`SYSTEM_RUN_DENIED` 表示节点**拒绝了执行**，不是「可能已经跑过」 ⇒ 撤销的生效点是启动边界，批准的有效期到 turn 结束为止。
- **长期授权是衍生关联，每次使用都重算**：standing grant 只是「衍生相关」，每次使用都要拿**原始的批准行、自动化行、撤销态重新校验**；授权失效条件包括作业被删或**实质性定义变更**（即使后来改回原定义也不恢复）、命令/cwd/env 差一个字节、撤销、过期、原始批准记录消失 ⇒ 「改回原样」不恢复授权，而「暂停再启用」保留 ⇒ 定义变更与运行状态变更是两类事件。

## Cap52 看得见审批卡 ≠ 能批准它；批准权的来源按通道分叉，且严格通道只认显式名单（来源：docs.openclaw.ai `tools/exec-approvals-advanced.md` 27,837B，2026-10-03 r396C 独立 curl 取 `.md` 原文实拉）

- **投递位置只决定提示出现在哪，不决定谁有权批准**：官方明确 session 投递**不授权该会话里的每个参与者批准**；通用同会话 `/approve` 仍要求发送者本身已获该频道会话的命令授权 ⇒ 「他看见了」与「他能批」是两个集合，把审批投到群里不等于把决定权交给群里。
- **批准权有三条可能的来源，且各通道取哪条不同**：① 发送者本身具备命令授权；② 通道若暴露**显式 approvers**，这些人即使在该会话内没有命令授权，也能授权 `/approve`；③ 更严格的通道（Discord / Telegram / Matrix / Slack 原生审批 DM 等）**只按自己解析出的 approver 名单**判定——例如 Telegram 话题里的审批提示**所有人可见**，但只有 `channels.telegram.execApprovals.approvers` 或 `commands.ownerAllowFrom` 解析出的数字用户 ID 能批准或拒绝 ⇒ 声明审批能力时必须写清「本通道按哪条来源判定批准权」，否则可见面会被误当成授权面。

## Cap53 IM/工单类审批：响应权与可见权是两条独立的门，空列表=全放行反模式（来源：docs.n8n.io `integrations/builtin/app-nodes/n8n-nodes-base.slack/approvals.md` 8,545B，2026-10-03 r405A 独立 curl 取 `.md` 实拉；与 §Cap52 看得见审批卡≠能批准 互补——Cap52 管通道显式 approvers 的权限源分叉，本条管 IM/工单系统里"谁能看见请求"与"谁能响应"被同一列表错误耦合的反模式）

- **审批列表控制的是响应权不是可见权**：n8n Slack Approvals 的 `Restrict Who Can Approve` 决定谁能批准，列表为空时频道所有成员都能批准 ⇒ 「看得见请求」被错误等同于「能批准」，是危险反模式；审批可见性必须显式收敛到私信道/DM，不能靠"列表非空"顺带隐藏。
- **未授权者点击→私密 ephemeral 提示 + workflow 继续等待**：不推进、不泄露决策，是「识别不了就拒绝而非假装覆盖」（Cap32 同源）在 IM 的具体实现。
- **空列表语义必须显式声明**：n8n 是「空=全放行」，与授权类白名单「空=全拒」（sa 3.82.0）字面相反，混用会制造「以为要批其实谁都能批」的漏洞；配置审批面时把两种空态都写清。
- 提升层：安全边界/工作流。触发词：审批响应权≠可见权、空列表全放行反模式、IM 审批私密提示、Restrict Who Can Approve。

## Cap54 能「管理授权」的权限自身是提权面：自改角色/自邀请=提权通道，且角色编辑即时全局生效（来源：docs.n8n.io `administer/manage-users-and-access/set-permissions-and-roles-rbac/create-custom-roles/create-custom-instance-roles.md` 8,015B + `see-available-roles.md` 4,301B，2026-10-03 r406A 独立 curl 取 `.md` 实拉；与 §Cap51 批准绑定二进制 / §Cap52 可见≠授权 / §Cap53 响应权≠可见权 同族——前几条管单次授权的源与门，本条管「授权管理权」本身的提权风险）

- **拥有「管理角色/管理成员」权限 = 能给自己提权**：n8n 自定义实例角色中，`Roles: Manage all roles` 持有者可编辑自己角色、追加原本未授予的权限；`Members: Manage` 持有者可邀请自己控制的账号再赋 Admin；`Roles: Manage project roles` 持有者可改自己所在项目的角色自授权限 ⇒ 「授权管理权」与「被管理的授权」不能由同一主体掌控，否则授权管理变成自服务提权通道，须把「能改授权」与「被授权者」分离。
- **角色编辑即时全局生效，无过渡窗**：n8n 改自定义角色「对所有被分配用户在整个实例立即生效」，无 dry-run/暂存；撤销/变更边界落在「角色定义修改点」而非「下次登录/重载」——与 Cap51「撤销在 spawn 边界生效」同源，但此处是配置侧即时生效，没有进程边界兜底。
- **删除角色前须先迁移成员**：n8n 要求删角色前把用户改派其他角色，否则成员悬空 ⇒ 撤销授权有级联依赖，不能只删角色不处理成员（与 r399-B「PATCH 语义按类型分叉」的删除前置条件同源）。
- 提升层：安全边界/授权模型。触发词：授权管理权提权、自改角色、自邀请提权、角色编辑即时全局生效、删角色前迁移成员。

## Cap55 决定的权威源是服务端记录而非提交动作；敏感命令的审批提示与结果同走私密路由（来源：docs.openclaw.ai `tools/exec-approvals-advanced.md` 27,837B（Approval forwarding / Native approval delivery / Official mobile operator apps 三段），2026-10-03 r408A 独立 curl 取 `.md` 原文实拉；与 §Cap51 批准绑定二进制 / §Cap52 可见≠授权 同族——前两条管「批准什么」与「谁能批」，本条管「批了之后以谁的记录为准」与「结果发到哪」）
- **原文**：① 移动端提交决定后若**回执丢失**，应用**禁用控件并重新读取记录**；若另一个界面已先胜出，应用显示**那条已记录的决定**；**待处理提示绑定在签发它的 Gateway 上，切换活动 Gateway 不能重定向旧 approval ID**。② owner-only 的敏感组命令（`/diagnostics`、`/export-trajectory`）用**私密 owner 路由**发送审批提示**与最终结果**：先试同一 surface 的私密路由，没有则退到 `commands.ownerAllowFrom` 中第一个可用路由（因此 Discord 群命令的审批与结果可能发到 owner 的 Telegram DM），**群聊只收到一句简短确认**。③ 请求者本人不必是审批者。
- **判据**：① **「我点了批准」不等于「批准生效」**——并发界面下权威是服务端那条记录，提交方拿到的是待确认的意图；**回执丢失时正确动作是重读而非假定自己的选择成立**，否则会出现两个界面各自认为已生效。② **ID 绑定签发者**：审批 ID 只对签发它的实例有效，切换 Gateway 不能改投旧 ID——多实例/多 Gateway 环境下「换个地方批」不是可用手段，反而说明该请求已随签发者失效。③ **高风险操作的输出与输入同等敏感**：审批提示走私密路由而结果发在群聊，等于把「谁批准」保护了、把「批准换来了什么」公开了；验收要**同时确认提示与结果两条投递路径**。④ **路由降级会改投递面**：私密路由不可用时退到 ownerAllowFrom 第一个可用项，意味着结果可能出现在完全不同的通道上——「没收到结果」先查路由降级链，而不是判定执行失败。⑤ **请求者≠审批者是默认形态**，不要默认发起人具备批准权，也不要因发起人不能批就认为流程挂死。
- **提升层**：安全边界 / 工作流。触发词：回执丢失重读、决定以服务端记录为准、审批 ID 绑定签发 Gateway、敏感命令私密路由、结果跟随路由降级、请求者不必是审批者。

- **原文**：`密钥只写不读——所有 token、secret 在任何响应中都不会回显，Agent 与沙箱也拿不到原始值`；`environment_variable 类型：以环境变量名提供给沙箱；进程中看到的是 omasec_ 代理值，真实密钥只在访问允许的目标主机时由平台代入请求`；`environment_variable 类型必须声明 networking 策略（unrestricted，或 limited + allowed_hosts，至多 16 项）`；`身份字段（mcp_server_url / host / secret_name，以及 refresh 的 token_endpoint / client_id / resource）不可变，更新时必须省略——要换目标就新建一条凭据`；`POST /v1/vaults/:vaultId/credentials/:credentialId 做部分更新：提供的 secret 被替换，省略的 secret 保留`。
- **判据**：① **进程内可见 ≠ 密钥可用**：注入的是代理值，真实值只在出站且目标主机命中凭据的 networking 规则时由平台代入 ⇒ 凭据的**作用域由网络策略界定，不是由"谁拿到了环境变量"界定**；评判暴露面要同时看值面与出网面。② **轮换是部分更新，但身份键必须省略**：省略=保留这条规则对 secret 成立、对身份键不成立（身份键要求省略是因为它不可改）⇒ **同一个"省略"字段在不同类型上语义相反**，写轮换脚本时不能一律"缺省即保留"。③ **换目标 = 新建凭据，不是改字段**：地址/宿主/名字是身份，改身份等于换对象；沿用旧凭据改 URL 的做法在该模型下不可行。④ **只写不读 ⇒ 凭据没有"回读校验"这一手段**：正确性只能靠外部探测（如 `mcp_oauth_validate` 的 valid/invalid/unknown）证明，不能靠读回来看对不对。⑤ 读取接口只回非敏感字段（`expires_at`、不含秘密值的 refresh 配置）⇒ **可见的元数据面与不可见的值面是两条清单**，不要把"能看到过期时间"当"能看到凭据"。
- 提升层：安全边界。触发词：只写不读、代理值、omasec_、出站代入、身份键不可变、换目标新建、部分更新省略即保留、凭据作用域由网络策略界定。

- **原文**：`pause：停止后续定时触发；手动 run 仍允许`；`unpause：以当前时间为锚重算 schedule.upcoming_runs_at；暂停期间漏掉的触发不会补跑`；`archive：终态且幂等；归档后不再触发、不可手动 run（409），历史 run 仍可查询`；`Deployment 只保存引用，每次触发按环境当前配置固化进新会话；环境被归档或删除后，下一次触发失败`；`响应中的 agent.version 是创建时固定（pin）下来的真实版本号`；`session_id（该次运行创建的会话；刚返回时可能为 null，通常数秒后填上）`。
- **判据**：① **暂停 ≠ 停用**：手动触发在暂停期仍可用 ⇒ "这个任务停了"这句话要分清是定时面停了还是整个任务停了，用暂停当"关停"会留下手动入口。② **恢复的锚点是当下不是暂停时刻**：漏掉的运行不补跑 ⇒ 恢复后不要按"本该跑几次"核算，也不要靠 unpause 去追补历史窗口；需要补数必须自己按时间窗重放。③ **归档只读不删历史**：归档后 run 记录仍可查询 ⇒ 归档是"停止变化"不是"抹除证据"，审计/复盘窗口在归档后仍然成立。④ **引用式绑定的失败推迟到下一次触发**：Deployment 只存环境引用，环境被删除/归档不会立即报错，要等下一次触发才失败 ⇒ 变更 Environment 时必须反查哪些 Deployment 引用它（与 §引用完整性责任相反两套 同源）。⑤ **版本在触发时 pin**：run 记录里带的是本次实际使用的 Agent 版本 ⇒ 复盘必须绑定版本，否则"当时配的是 X"无法还原。⑥ **异步填充字段不能当缺失处理**：`session_id` 刚返回为 null 是常态，立刻判"没创建会话"会误报。
- 提升层：工作流。触发词：暂停不阻断手动、恢复以当下为锚、漏跑不补、归档终态历史可查、引用式绑定延迟失败、run 绑定 agent 版本、session_id 异步填充。

- **原文**：`In mode=auto, reviewer-approved unpinned execution requires the complete dispatch chain to be identity-bound. The authorization plan must succeed, every candidate must use direct transport, and every wrapper and final executable must have a recorded executable operand.`；`Shell -c wrappers, env with assignments, xcrun, BusyBox/Toybox applets, shell builtin/command/exec dispatch, and anything else whose complete chain cannot be bound skip automatic review with "Exec auto-review skipped: dispatch chain cannot be bound".`；`Node executable-identity bindings are local to one invocation. The remote human approval plan keeps its existing direct executable pinning ... it does not carry every executable identity inside a shell wrapper across the approval wait. For those inner commands, identity revalidation starts when the approved invocation reaches the node's local policy evaluation, so it does not detect substitutions made earlier in the remote approval wait.`；`If no decision arrives before the timeout, the request is treated as an approval timeout and surfaced as a terminal host-command denial.`；`OpenClaw also resumes that session with an internal followup so the agent observes that the command did not run instead of later repairing a missing result.`；`Pending exec approvals expire after 30 minutes by default.`；`Denied async approvals use the same main-session followup path for the denial status, but they do not register elevated runtime handoffs and they do not run the command.`
- **判据**：① **自动/人工的分界线是"可绑定性"不是风险高低**：能钉住整条派发链才配进自动复核，钉不住的一律转人工 ⇒ "为什么这条命令要人点"的答案常常是结构性的（包装层不可绑定），不是因为它更危险。② **钉不住 ≠ 拒绝**：不可绑定是**降级到人工**，而既存硬拒绝（`-i`/`--interactive`/`-ic`）**优先于降级**，保持拒绝而不是转成人工请求 ⇒ 同一族形态里"降级"与"拒绝"会同时存在，判定顺序必须是"先查既存拒绝，再谈降级"。③ **远程审批的等待期是校验盲区**：内层命令的身份在节点本地策略求值时才重新校验，等待期内发生的替换检测不到 ⇒ 把"批了"当作"整条链都安全"是错误的，长等待审批后的执行应重新确认。④ **绑定只在内存存续于审批生命周期，无持久化变更** ⇒ 重启/换会话后绑定不保留，不能指望"上次批过所以这次还绑着"。⑤ **超时是终态拒绝不是悬空**：无人决定时系统给出的是 denial，不是"继续等" ⇒ 监控要把 timeout 归入拒绝类而不是挂起类。⑥ **系统会主动补一条"没跑"的通知**：让 agent 立刻知道命令没执行，而不是事后再发现结果缺失 ⇒ 反过来要求：收到审批相关 followup 时必须区分"批准并执行了"与"拒绝了/超时了"，两者走同一条投递路径但语义相反。
- 提升层：安全边界 / 工作流。触发词：dispatch chain cannot be bound、auto-review 跳过转人工、既存拒绝优先于降级、远程审批等待期盲区、绑定仅内存存续、审批超时即终态拒绝、followup 告知没跑、收到了消息不等于跑了。

- **原文**：`更新 path 和/或 content。可带 precondition：内容已被改过则更新失败，避免覆盖他人刚写的内容`；`删除 Memory；可带 expected_content_sha256，当前内容已变化时拒绝删除`；`更新前先读取当前 content_sha256，再把它作为条件提交`；`每次创建、修改、删除都会产生一条不可变的版本记录，标注操作类型（created / modified / deleted）与执行主体（session_actor 会话内 Agent，含 session_id；或 user_actor API 调用者）`；`如果某个版本包含不应留存的敏感内容……用脱敏接口抹除该版本的内容与路径，保留审计轨迹`；`脱敏后该版本的 path / content / content_sha256 变为 null，redacted_at 与 redacted_by 记录操作时间与主体`；`不能对当前 head 版本脱敏，会返回 409；先改内容或删除条目，再对历史版本执行 redact`；`删除条目不会抹掉历史版本里的内容`。
- **判据**：① **共享记忆必须走乐观锁**：多 agent/多会话写同一份记忆时，"读—改—写"之间必须带内容哈希做前置条件，否则后写静默覆盖先写；正确姿势是**先读哈希、再带条件提交**，不是"写完再看对不对"。② **删除也要带条件**：`expected_content_sha256` 让"我删的是我以为的那版"成为可验证命题，防止删掉别人刚更新的内容。③ **写入主体必须二分归因**：`session_actor`（agent，带 session_id）与 `user_actor`（人，经 API）⇒ 同一份记忆里"这条是谁写的"是可查的，做记忆治理/回溯时不能把 agent 沉淀与人工修正混为一谈。④ **删除 ≠ 抹除**：删除条目只影响当前视图，历史版本里的内容仍在 ⇒ 涉密数据的回收必须落到**版本级 redact**，只删条目会留下完整副本。⑤ **脱敏受版本位置约束**：head 版本不可脱敏（409），须先改内容或删除条目、让目标版本退为非 head，再 redact ⇒ "先改后抹"是固定两步顺序，直接对最新版脱敏会失败。⑥ **脱敏保留审计轨迹**：path/content/hash 变 null 但 `redacted_at`/`redacted_by` 留存 ⇒ 抹除动作本身留证，符合"能说清谁在什么时候抹了什么"。
- 提升层：安全边界 / 工作流。触发词：记忆乐观锁、precondition、expected_content_sha256、先读哈希再提交、session_actor/user_actor 二分、删除不抹历史版本、head 版本不可脱敏、先改后抹、redact 保留审计轨迹。

- **原文**：`发送 user.interrupt 后，平台会主动停止当前模型响应，并向运行中的命令发出停止信号；命令在宽限期内（当前约 3 秒）没有结束会被强制终止，本轮必然停下`；`中断不会产生 session.error`；`interrupt 之前尚未处理的消息会被跳过，之后提交的 user.message 会在下一轮执行`；`若停在 requires_action，interrupt 会取消整组等待中的工具调用和审批`；`停在 requires_action：在等你处理 event_ids 里列出的调用……此时发 user.message 会被拒绝（400）`；`更新 Agent 返回 409……服务器上当前版本已经变了——通常是别人（或另一次请求）刚更新过。先 GET 最新 Agent，用返回的 version 再更新；CI 这类声明式同步可以省略 version，后写覆盖`。
- **判据**：① **主动中断与失败是两条通道**：中断不产生 `session.error` ⇒ 监控不要用"有没有错误事件"判断"是不是出了问题"，被中断的轮次在错误面上完全干净，要另设中断计数。② **中断有宽限期且必然停**：命令先收到停止信号、宽限期内不退出才强杀 ⇒ "发了 interrupt 却还在跑"看的是宽限期，不是中断失效。③ **等待态的输入类型是受限的**：`requires_action` 下只能回 `user.custom_tool_result` / `user.tool_confirmation`，发新 `user.message` 直接 400 ⇒ 等待态不是"可以顺便追加要求"的时机，想把新指令带进去必须等本轮结束或先取消。④ **中断是整组取消**：对等待中的一整组工具调用与审批一次性取消 ⇒ 部分响应没有意义，恢复后要按"整批重来"处理，不能假设其中某几条已经生效。⑤ **中断会吞掉未处理的排队消息**：中断前入队但还没处理的消息被跳过 ⇒ 重要指令不要在 interrupt 前后脚发送，否则静默丢失。⑥ **版本冲突的两种正确解法按场景分**：交互式先 GET 再带 version；CI 声明式同步**省略 version 让后写覆盖**——把交互式做法搬进 CI 会造成无谓的冲突失败，反之则会互相覆盖。
- 提升层：工作流 / 安全边界。触发词：中断不产生 error、宽限期强杀、等待态拒绝新指令、中断取消整组、中断吞掉排队消息、声明式同步省略 version、409 版本冲突先 GET。

## Cap62 安全加固先画责任分界表：平台只限「未认证可猜」的面，业务突发与滥用由部署方判；代理之后必须显式声明否则审计全记成代理（来源：pipedream.com/docs `conduit/deploy/hardening.md` 6,976B，2026-10-04 r410C 独立 curl 取 `.md` 原文实拉；与 §Cap36 限流四头可机读 互补——那条管"被限了怎么知道何时重试"，本条管"谁该限哪些面、限流计数放在哪一层"）
- **原文**：`Nothing in Conduit requires public reachability … so a deployment on a private network or behind a VPN is fully supported, and for an internal tool it is the right default`；`Every surface where an unauthenticated caller could guess, flood, or probe is throttled per client IP, with no configuration`；`On the PostgreSQL tier these two counters are shared across replicas, so running N replicas does not multiply the rate a credential-guesser gets`；`The other limiters are per-replica by design (≈N× the single-instance rate cluster-wide)`；`Conduit does not impose sustained throughput quotas on authenticated tool calls — a burst of legitimate agent traffic is business, not abuse, and distinguishing the two is a policy decision`；`set CONDUIT_TRUSTED_PROXIES so audit records and per-IP limits attribute requests to real clients rather than the proxy`；`A body over its cap is an error, never a truncation — a short read cannot pass for a complete one anywhere in the gateway`；`Reports that say nothing about the deployment are dropped rather than recorded: content a browser extension injected into the page … and reports naming a page outside CONDUIT_BASE_URL, which the endpoint being unauthenticated otherwise lets anyone submit`；checklist 表把每个关注点映射到 `Conduit` 或 `Your edge`。
- **判据**：① **加固方案的第一产物是一张责任分界表，不是一组配置**：官方把每个关注点（入站认证/授权/暴力破解/体量滥用/TLS/超大载荷/出站 SSRF/静态密钥/审计）逐行标注"平台内置"还是"你的边缘" ⇒ 说"我们做了安全加固"却拿不出这张表，等于说不清哪一格是空的。② **限流的适用范围按"未认证能不能猜"划界**：平台只限登录、OAuth 各端点、失败的 MCP/SCIM 认证、CSP 报告、CLI 下载；**已认证的工具调用不做持续吞吐配额**——业务突发与滥用的区分是策略判断，不该由平台替部署方拍板 ⇒ 把已认证流量也一律限流，等于把正常业务当攻击；完全不限未认证面，等于放任猜测。③ **计数器的共享范围是安全属性，不是实现细节**：会被穷举的那几个面（密码失败、MCP/SCIM 认证失败）计数跨副本共享，**否则跑 N 副本就让猜测者拿到 N 倍速率**；其余限流器故意按副本 ⇒ 判断一个限流器对不对，要问"这个计数跨实例后还成立吗"。④ **有代理时必须显式声明可信代理**：否则审计记录与 per-IP 限流全部归因到代理那一台 ⇒ 这会同时污染取证与限流，且症状是"所有请求来自同一个 IP"，排查时极易误判为单客户端攻击。⑤ **无认证的可观测端点是投毒面**：CSP 违规报告端点不认证 ⇒ 任何人可提交；官方丢弃"与本次部署无关"的两类报告（浏览器扩展注入的、指向 BASE_URL 之外页面的）⇒ 凡开放收集的可观测数据必须带"与本次部署相关"的过滤，否则观测面被噪声淹没。⑥ **超限是错误不是截断**：超上限的 body 一律报错，短读绝不能冒充完整读 ⇒ 与 §上传超限 part 静默丢弃 正好是一对正反写法。
- 提升层：安全边界 / 工具。触发词：加固责任分界表、平台限流 vs 边缘限流、只限未认证可猜面、跨副本共享计数、N 副本不等于 N 倍速率、业务突发不是滥用、CONDUIT_TRUSTED_PROXIES、审计归因到代理、CSP 报告投毒、超限是错误不是截断。

## Cap63 信任不跨层传递：令牌签发必须单点、可见与可调用是两道门、出站只带自己的凭据（来源：pipedream.com/docs `conduit/deploy/architecture.md` 5,764B，2026-10-04 r411B 独立 curl 取 `.md` 原文实拉；与 §Cap46 三道门 / §Cap42 执行身份 / §Cap62 责任分界表 互补——那三条管执行位置、数据归属、谁该加固哪一格，本条管"凭据由谁签发"与"边界之间是否互信"）
- **原文**："the surfaces enforce their own checks rather than **trusting each other**"；"It is the **only** token issuer: externally issued tokens (your identity provider's JWTs included) are **not accepted** at the MCP endpoint — the identity provider authenticates the human during sign-in, and Conduit mints what clients hold"；策略面 "computes each user's effective tool set (allow policies ∩ the user's enabled connectors) and enforces it on **every tool listing *and* every call** — **a tool hidden from the list cannot be invoked by name**"；出网 "Every HTTP request … leaves through a **single hardened client** that blocks requests to private and internal addresses, never follows redirects, and requires HTTPS"；"Upstream calls use Conduit's own credentials for each connector — **the client's bearer token is never forwarded to an upstream service**."
- **判据**：① **认证人与签发凭据是两个职责，必须分开**——上游 IdP 只证明"这个人是谁"，本系统签发"这个客户端持有什么"；直接接受外部 JWT，等于把受众、生命周期、撤销能力一并交给上游，本系统从此无法单独吊销一枚令牌。⇒ 凡接入外部身份源，落点是"用它认证、不拿它当凭据"。② **同一平面上的组件互不授信，各自独立校验**——授权服务器、管理 API、策略引擎、目录同步各自做检查，而不是"前一个验过了后面就信"；省掉一层校验的前提必须是"这一层的输入不可能来自别处"。③ **可见性与可调用是两道门，只做前一扇等于留后门**：从列表里隐藏的工具，调用侧必须同样拒绝——"看不见"是给不知道名字的人的门槛，对知道名字的人毫无作用；验收方式固定为"按名字直接调用被隐藏项，应被拒"。④ **出站只有一个口，且加固规则写在口上不在调用点上**：阻断私网/内网地址、不跟随重定向、强制 HTTPS，这三条如果散在每个调用方各自实现，漏一个就等于没有；同时**调用方的令牌绝不转发给上游**——否则上游拿到的是调用方的权限面而非服务自己的，一个服务就变成了权限放大器。
- 提升层：安全边界 / 工具。触发词：唯一签发者、外部 JWT 不接受、认证与签发分离、隐藏不等于不可调用、按名调用仍被拒、单一出网口、出站不转发客户端令牌、组件互不授信。

## Cap64 可丢的与不可丢的必须分通道；观测端点默认不监听并做到「结构上不可能公网可达」（来源：pipedream.com/docs `conduit/deploy/monitoring.md` 9,842B，2026-10-04 r411B 独立 curl 取 `.md` 原文实拉；与 §Cap62 无认证可观测端点是投毒面 / §Cap37 观测端点需鉴权 互补——那两条管"谁能往里塞"与"要不要鉴权"，本条管"哪些数能放在会丢的通道上"与"能不能被公网摸到"）
- **原文**："Metrics are aggregated **in memory and reset to zero when the process restarts** … anything Conduit must **count exactly** (usage dashboards, the audit log) is stored in its database **independently of these metrics**"；"Unset (the default), no listener starts and nothing is exposed"；"The port is deliberately **not** part of the chart's Service or Ingress: … the endpoint can **never be exposed through the public entry point by accident**"；"unauthenticated by design … It reveals operational shape (connector names, request rates, session counts) but **never payloads, secrets, or per-user data**"；指标里 `outcome` 三值 `ok` / `error`（"the call ran and failed"）/ `denied`（"blocked by access policy before running"），且 "Denied calls never run, so they record no duration"。
- **判据**：① **会重置的通道只能放可容忍丢失的量**：内存指标重启归零、`rate()` 跨重置拼接是预期行为 ⇒ 凡必须精确的数（用量、计费、审计）必须落在独立持久存储上，把它挂在会重置的通道上，会让"少算了"变成静默且不可恢复的偏差（用户看到的是"这个月好像用得少"，而不是"我们丢了数据"）。判一个数字可不可信，先看它走的是哪条通道。② **默认不监听 + 结构上不可达，优于"默认开但记得关"**：端口刻意不放进 Service/Ingress、抓取走 pod IP ⇒ 公网暴露不是靠人记得配，而是在拓扑上做不到；把"不该被公网访问"交给配置纪律，等于把它交给下一次改动。③ **不认证的观测端点必须写清它暴露的是什么**：只有操作形状（名字、速率、计数），且从不带 payload/密钥/每用户数据 ⇒ "免鉴权"能成立的前提是"内容本身不敏感"，不写这条边界的免鉴权端点只是没想清楚的端点。④ **被拒绝必须单独计一档，且不进耗时分布**：`denied` 是策略在跑之前拦下的，与 `error`（跑了并失败）混在一起会让"策略生效"显示成"故障率上升"；它也不该产生耗时样本，否则 P99 里混进一批根本没执行的调用。
- 提升层：可观测性 / 安全边界。触发词：指标会重置、必须精确计数走数据库、默认不监听、端口不进 Service、结构上不可公网、观测端点暴露面声明、denied 与 error 分档、拒绝不计耗时。

## Cap65 控制的粒度必须匹配被控对象的可伪造性：身份可自造时逐身份封禁无效，须上提到准入姿态；撤销不等于禁止（来源：pipedream.com/docs `conduit/use/mcp-authorization.md` 15,363B，2026-10-04 r412A 独立 curl 取 `.md` 原文实拉；与 §Cap63 信任不跨层传递 / §Cap64 会重置的通道 互补——那两条管"谁签发、谁能被摸到"，本条管"封禁一个可自造身份的对象到底有没有用"）
- **原文**："a block on one holds only until it registers again under another"；"To keep self-registering clients out for good, use *Verified clients only* or *Only allowed clients*, which refuse anything unproven that you have not allowed"；"A revocation makes a member re-approve a client; **to keep a client out, block it**"；"a grey question mark when it only registered itself and presented signals any client could imitate"；"A client you add is decided about on its own, even when its document sits under a vendor Conduit recognizes"；"Registration happens before anyone signs in and names no workspace, so it is the authorization server's own switch."
- **判据**：① **先问被控对象能不能自己造一个身份**：能自造（自注册、换个名字重来）⇒ 按身份逐条封禁只是把对手逼去换一个身份，投入随封禁条数线性增长而收效为零；此时控制必须上提到**准入姿态**（只许已验证身份 / 只许白名单），把默认从"允许除非被抓到"改成"拒绝除非被证明"。② **撤销与禁止是两种控制，别混用**：撤销（revoke）只强制重新授权，作用域限于本工作区，且当事人在别处重新同意即全域解除 ⇒ 它治"这次授权要不要复核"，不治"这个对象该不该进来"；要"不让进"必须用 block/准入。把撤销当禁止用，会得到一个看起来在生效、实际可自愈的假控制。③ **身份按可出示的凭证判定，不按声称的名字**：同名的未验证安装是**独立实体**，单独成行、单独决策；"它说它是 X"不构成它是 X，名牌之下的每一行各自承担自己的结论。④ **发生在归属确立之前的动作，其控制点不可下放**：注册发生在登录之前且不指明工作区 ⇒ 它只能有一个实例级开关；凡是"在身份/归属确定之前发生的动作"，控制必然是全局的，想按租户下放在结构上就做不到。
- 提升层：安全边界 / 治理。触发词：封禁无效、身份可自造、准入姿态、verified only、白名单准入、撤销不等于禁止、revoke 与 block、未验证安装单独成行、归属确立前的全局开关。

- **原文**："The default `escalate` mode runs its blocking recall sub-agent **only when the message asks about the past and the deterministic memory lane found no strong trusted trigger match**"；表格 `escalate` | "Default. Run only for recall intent when lane 1 has no strong hit." / `always` | "Preserve the previous behavior and run on every eligible targeted turn."；"Flat retrieval is strongest for **direct fact matches** and **weaker on temporal and multi-session questions**."
- **判据**：① **升级条件要两条同时成立**：意图匹配（这轮确实在问过去）**且**廉价确定性通道没有强命中 ⇒ 只拿"廉价失败"当条件，会把冷启动、无关问题、以及本来就不该深挖的轮次全部拖进阻塞式子调用，成本由所有轮次平摊而收益只落在少数轮次上。② **检索层必须声明自己的能力边界**：扁平/向量检索强于直接事实匹配、弱于时序与跨会话问题（有 LongMemEval / PrefEval 这类基准量化该差距）⇒ 不写边界的检索层，用户感知到的"想不起来"会被误判成"根本没存过"，于是重复沉淀已有信息。③ **改默认不许删掉旧行为**：`escalate` 作默认、`always` 保留旧路径 ⇒ 分层优化要给一条显式逃生口，否则"优化"对依赖旧行为的场景就是静默破坏。
- 提升层：工作流 / 记忆检索。触发词：深召回升级、阻塞式召回、廉价通道先跑、意图匹配才升级、检索能力边界、时序与跨会话弱项、escalate 与 always、保留旧行为。

## Cap67 工具清单是「限流」不是「授权」：配置里列出工具名不产生授权，授权面由父 agent 的有效工具策略决定（来源：docs.openclaw.ai `concepts/active-memory/memory-tools.md` 5,831B，2026-10-04 r413A 独立 curl 取 `.md` 原文实拉；与 §Cap63 信任不跨层传递 / §Cap66 昂贵召回双条件放行 互补——那两条管"凭据由谁签发""什么时候值得召回"，本条管"召回工具配上了到底算不算被允许用"）
- **原文**：「`toolsAllow` is a **limit, not a permission grant**. Before starting recall, Active Memory filters these names through the parent agent's **finalized tool policy**.」「`allow` and `alsoAllow` **cannot be combined** in the same scope.」「A later allowlist **cannot restore** tools excluded by a profile.」「These grants also give the **parent agent** access to the named tools; they are not recall-only permissions.」「A tool listed there is **registered**, but that output does not prove the parent agent or Active Memory is **authorized** to call it.」「wildcards, `group:*` entries, and core agent tools … are **silently filtered out**」
- **判据**：① **白名单是上限不是许可**——`toolsAllow` 只回答"最多用这几个"，不回答"可以用这几个"；真正生效的是它与父级工具策略的**交集**，交集为空时该能力静默缺席（`status=policy-disabled`），症状是"明明配了却没召回"。⇒ 凡"在某处列出能力名"的配置，都要追问它在哪一层被过滤，"列了"不等于"批了"。② **注册可信 ≠ 授权可信**——`plugins inspect` 能证明工具已注册，不能证明调用方被授权；排查"配了不生效"时这两件事必须分开取证，否则会把授权问题误修成注册问题。③ **放宽与收紧不是对称操作**——`alsoAllow` 只能在 profile 之外**加**，不能覆盖显式 deny / provider / agent / sandbox 限制，也不能救回被 profile 排除的工具；且 `allow` 与 `alsoAllow` 同域互斥。⇒ 收紧是减法、放宽只有加法这一个方向，**被减掉的东西没有对等补回路径**，配之前要想清楚哪一层在减。④ **为了子能力开的授权会同时抬高父 agent 的能力面**——给召回子 agent 开的 `alsoAllow` 同时把该工具交给父 agent，授权不是"仅这次用"，开给局部的口子是全域的。⑤ **非法条目应拒绝启动而非静默放宽**（与 sa 3.124.0 同族判据在此面复现）：只收精确工具名，通配/组/核心工具被静默过滤 ⇒ 静默过滤让"配错了"表现成"没配"。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：白名单是限流不是授权、toolsAllow、alsoAllow 与 allow 互斥、profile 排除不可恢复、注册不等于授权、policy-disabled。

- **原文**：「Daily and idle reset freshness is **not based on `updatedAt`**」「Automation wakeups, heartbeat runs, exec notifications, and gateway bookkeeping **may update the session row for routing/status, but they do not extend `sessionStartedAt` or `lastInteractionAt`**」「For legacy rows created before those fields existed, OpenClaw can recover `sessionStartedAt` from the transcript JSONL session header when the file is still available. Legacy idle rows without `lastInteractionAt` use that recovered start time as their idle baseline.」
- **判据**：① **"行被写过"与"生命周期被推进"是两件事**——心跳、唤醒、通知、系统记账都会改同一行（路由/状态），但刻意不延长新鲜度字段；若把新鲜度定义成 `updatedAt`，一个后台心跳就能让会话永不过期。⇒ 任何"多久没动就归档/重置"的规则，必须显式列出**哪些写入算交互、哪些不算**；用"最后修改时间"当新鲜度等于把续命权交给噪音。② **同一个对象上要有两套时间语义并各自命名**：路由态的时间（什么时候被系统碰过）与交互态的时间（什么时候人/主体真的说了话）。混用后排查"为什么没过期"只能靠猜。③ **字段缺失时的回退基准要写清楚且优先从原始记录恢复**——旧行没有这两个字段时从 transcript 头恢复 `sessionStartedAt`，无 `lastInteractionAt` 的旧行用它当 idle 基线；⇒ 补字段的迁移不能默认"缺失 = 现在"或"缺失 = 永不过期"，两者都会成批改变既有对象的命运，必须给出可核验的恢复来源。④ 对 guild 的落点：共享记忆/交接/收件箱的 groom 与归档规则同理——后台 groom 自己写的时间戳不能算"这条还有人在用"；存活判定要挂在明确的交互字段上。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：写入不推进生命周期、updatedAt 不是新鲜度、sessionStartedAt、lastInteractionAt、心跳不算交互、groom 存活判定字段。
## Cap69 自动化任务默认「启用+监督」，禁用等审批是更糟的失败（来源：docs.openclaw.ai/automation/cron-jobs/how-it-works.md，2026-10-04 r415 独立 curl 实拉）
- **原文**：job created **enabled, not disabled-pending-approval**；scheduler supervises enabled jobs: a failing one raises a failure notification and is **auto-disabled after repeated errors**, with the reason recorded and the owner notified；nothing supervises a disabled job；a job left disabled waiting for a confirmation that never arrives is **invisible to every guard, hidden from the default list, and will never fire or explain itself** — a silent non-outcome, which is a worse failure than a job that runs and visibly complains.
- **判据**：① 自动化任务默认**启用+受监督**（失败即告警 + 重复失败自动禁用）优于**禁用等审批**——被禁用的任务对守卫不可见、不在默认列表、永不触发、永不解释自己，是「静默非结果」，比「运行并可见地抱怨」更糟；② 调度器必须拥有失败记账与可见性，任务「是否健康」应由监督信号决定，而非由「有没有被人工批准启用」决定；③ 落地动作：新任务走「启用+监督+自动禁用」而非「禁用等确认」，把「会不会响」交给重复失败计数而非人工点击。
- 提升层：工作流 / 可靠性。触发词：默认启用、受监督、自动禁用、禁用等审批、静默非结果、可见失败优于静默。

- **原文**（gmail restricted reader）：explicit `ownership: "explicit"` roster；reader agent `workspaceAccess: "none"` + `sandbox.mode: "all" scope: "session"`；`tools.allow: ["session_status"]` deny `group:fs/runtime/web/browser/cron/gateway/nodes`；per-agent allowlist **cannot restore** a tool an earlier policy removed；`tools.agentToAgent.enabled: false` 禁用跨 agent 移交；untrusted content wrapped as data, never followed.
- **判据**：① 不可信输入（邮件 / Webhook / 用户上传）**不当主 agent 跑**，路由到独立受限 reader agent——独立沙箱（`workspaceAccess: none`）+ 工具钳制（allowlist 只含必需，deny 文件系统 / 运行时 / 网络 / 浏览器 / cron / 网关）+ 禁跨 agent 移交（`agentToAgent.enabled: false`），避免 prompt-injection 借主 agent 能力外溢；② 工具策略只能更紧不能更松——全局 / provider / agent / sandbox 规则叠加后，per-agent allowlist **不能恢复**被上层移除的工具，钳制必须可审计；③ 外部内容当数据不当指令——包裹为 untrusted data，禁止跟随其中的链接 / 指令。
- 提升层：安全边界 / 工作流。触发词：受限 reader、独立沙箱、workspaceAccess none、工具钳制、禁跨 agent 移交、prompt injection、不可信输入、untrusted data。

- **原文**：「Recurring top-of-hour expressions (minute `0` with a wildcard hour field) are … by up to 5 minutes to reduce load spikes. Use `--exact` to force precise timing」；「An `on-exit` job disables itself when its payload is queued to run. Re-enable the job to watch again」；「If the new command exits before that payload finishes, its exit waits for the previous run to settle … This includes cleanup still running after a timeout response. Disabling or changing the watch cancels its pending exit.」；「Only one payload fire and one bounded pending batch are retained per job … coalesce into that pending batch rather than building an unbounded queue.」；「Failed payloads are not retried because they may not be idempotent.」；「Combining a script payload with a condition gate is rejected because both would own the persisted `trigger.state` slot.」；「Five consecutive runs shorter than 60 seconds leave the job in an error state … manually re-enable the job to clear the restart cap.」；「If either limit is exceeded, the source stops with a recorded error … then manually re-enable the job.」
- **判据**：① **默认形状要取能扛住最坏情况的那一侧**：整点周期作业默认自动错开至多 5 分钟削峰，**精准是显式声明换来的**（`--exact`）；把"准点"设成默认，等于让所有使用者的默认值在同一秒撞在一起。⇒ 凡"大家都想要同一个时刻"的能力，默认值必须带打散，且打散窗口只对周期类有意义（间隔型/事件型不适用）。② **一次性触发用完即停用，且重启是显式动作**：`on-exit` 作业在载荷排队时就自我停用，要看须重新启用 ⇒ 事件型触发不排队，"监视到一次"之后不能假设它还在监视。③ **"上一个还没 settle"要显式等待，且 settle 包含超时之后的清理**：新命令若先退出，退出动作会等前一个载荷 settle（含超时响应后仍在跑的清理）才停用作业并起下一个 ⇒ 只看"响应已返回"会漏掉仍在跑的收尾。④ **积压必须有界，超限停源并留错**：只保留一个在跑的载荷 + 一个有界待批，其余合流；匹配预算或队列超限则**源直接停止并记录错误**，须手动重启 ⇒ 无限队列把"处理不过来"伪装成"稍后会处理"，有界 + 停源才让背压可见。⑤ **不幂等的失败不重试**：失败载荷刻意不重试（"may not be idempotent"）⇒ 重试资格由副作用性质决定，不是由"失败了该不该再试"决定。⑥ **两个特性争用同一状态槽时在准入期就拒**：script payload 与 condition gate 都要独占 `trigger.state`，组合直接被拒 ⇒ 冲突不要在运行时表现为"互相覆盖"，要在装配时拒绝。⑦ **快速失败循环要有封顶并转为人工**：连续 5 次短于 60 秒进入错误态、须手动重新启用 ⇒ 自动重启 + 无上限 = 把崩溃变成高频噪声。
- 提升层：工作流 / 工具。触发词：默认打散、削峰默认开、精准须显式、on-exit 自我停用、有界队列、超限停源、不幂等不重试、状态槽争用准入期拒绝、快速失败封顶须手动清、settle 含超时后清理。

- **原文**：「As a platform administrator, you have **full control** over which pieces are available to your users.」；层级表 `**Platform Level** | Platform Admin | Install and remove across the entire platform` / `**Project Level** | Project Admin | **Show/hide** specific pieces for specfic project`；「Project administrators can **further restrict** which pieces are available within their specific project. This is useful when different teams or projects need access to access to…」
- **判据**：① **两级作用域的动词不同决定了能力方向**：平台级是 install/remove（**改变全集**），项目级是 show/hide（**只在本项目内增减可见性**）⇒ 下级作用域的操作对象不是"能力本身"而是"上级已授予集合在自己范围内的投影"。② **继承律是 deny-only**：项目管理员只能 further restrict，**不能启用平台层未安装/未批准的东西** ⇒ 若下级能自行放大，权限的实际边界就不再由上级决定，"平台级批准"会退化成一种建议。③ **"能管理"不等于"能扩张"**：两级都叫 manage，但一个是增删全集、一个是隐藏子集 ⇒ 设计多级作用域时必须把动词写清楚，否则同一词在两层含义相反，审计时无法判定越权。④ **收窄是免费且可逆的，放大不是**：隐藏可以随时取消且不影响他人；新增能力会影响所有使用者且常常不可逆 ⇒ 不对称性本身就是该选 deny-only 的理由。⑤ **落点**：任何"平台级 vs 项目级 / 租户级"的技能注册表、工具集、凭据池，能力组合语义必须写成 deny-only 继承，并在实现上让下级的 enable 操作只能作用于上级已授予的集合内。
- 提升层：可复用 Skill / 治理。触发词：deny-only 继承、分层作用域、只收窄不放大、平台级 vs 项目级、能管理不等于能扩张、收窄免费放大不可逆、下级不得自授能力。

### Capability 73 — 能力生效要过三道各自独立的门；平台默认表是「天花板」不是「清单」（来源：docs.openclaw.ai nodes/command-policy.md 9,909B，2026-10-04 r417C 独立 curl 取 .md 原文实拉；与 Cap67「工具清单是限流不是授权、生效的是交集」互补——那条管工具清单与父策略的交集，本条管连接端自声明与配对批准的分离）
- 三道门分属三个声明方，缺任一都不生效：① 连接端在**认证后的连接元数据**里自声明（`connect.commands`）；② 该命令在该连接的**已批准命令面**上；③ 平台的「默认值 + 审批」派生允许表包含它。**平台文档里那张按操作系统列的表描述的是策略天花板，不是每个节点都实现了的清单**——命令最终可用还要求对端真的声明了它。
- **单一否决位永远压过一切允许来源**：显式拒绝清单优先于平台默认值与任何额外加入的允许条目。设计允许面时必须同步回答「有没有一个位置能否决全部」，否则每次新增默认值都在无声地扩大历史配置的权限。
- **待批扩展期间系统收缩，不是冻结也不是放开**：初次未批准的命令面没有任何有效命令；提交扩展后、批准之前，只有「先前已批准 ∧ 当前仍声明 ∧ 当前仍允许」的旧命令继续有效。三者任一变化都会让它在此期间失效——把它做成「保持旧集合不变」会放行已失效的能力。
- **配对成功不得连带授予命令**：自动批准 CIDR 只批准**设备**，命令面仍须单独批准，理由是配对本身不构成对能力的同意。**能连带批准初始命令面的通道必须记录了明确的所有权或管理员同意证据**（SSH 回读到的精确设备密钥、带管理员同意的 setup code）；仅「来自可信网络段」不是这类证据。⇒ 自动授权的资格由**证据类型**决定，不由网络位置决定。
- 危险与隐私类命令即使对端已声明也须平台侧显式一次性 opt-in ⇒ **对端自称支持不构成授权**。
- 落地口径：任何「连接端 + 中枢 + 能力清单」三层结构（设备配对、MCP 服务器注册、插件工具发布、子 agent 能力上报）都适用——先分清「谁在声明」「谁在批准」「谁在设天花板」，再决定否定项该放在哪一层。

## Cap76 控制的「误读澄清」必须与能力声明同表同级：先写清它防什么，再写清什么情况不算它失效，「未承诺」不等于「被绕过」（来源：docs.openclaw.ai/gateway/security/trust-model.md 9,980B + gateway/security.md 14,456B，2026-10-05 r419A 独立 curl 取 `.md` 原文实拉逐串命中；与 Cap67「工具清单是限流不是授权」/ Cap75「显式不该做护栏」互补——那两条管"清单不产生授权"与"程序定义要带负向约束"，本条管"每项控制声明必须自带误读澄清，且与正向声明同级存放"）
- **原文**：Trust boundary matrix 三列 `Boundary or control | What it means | **Common misread**`；"`sessionKey` (session IDs, labels) is a **routing selector, not an authorization token**."；"[Named operator roles](/gateway/operator-scopes#named-operator-roles) bound what each teammate's connections can do; they are **collaboration guardrails, not tenant isolation**."；"Prompt/content guardrails - Reduce model abuse risk | misread: *prompt injection alone proves auth bypass*"；"Browser evaluate - Intentional operator capability when enabled | misread: *any JS eval primitive is automatically a vuln*"；"Local TUI shell - Explicit operator-triggered local execution | misread: *local shell convenience command is remote injection*"；「Everyone who can message a tool-enabled agent shares that agent's delegated tool authority」。
- **判据**：① **控制项的价值有一半在「它不是什么」**——只写「我提供了 X」，消费方会把 X 当成它没承诺的东西（把选择器当令牌、把护栏当租户隔离、把运营商能力当漏洞）⇒ 每项能力/控制声明必须与「常见误读」成对出现，不能把澄清丢进 FAQ 或等出事再解释。② **澄清要与声明同表同级**：误读是同一张表的第三列，不是脚注也不是附录——同表同级才能让评审在看到能力的同一眼看到它的边界。③ **区分「未承诺」与「被攻破」**：prompt injection 得手 ≠ 认证被绕过；存在 eval 原语 ≠ 存在漏洞；本地 shell 便利命令 ≠ 远程注入 ⇒ 复盘/上报时先判「这个控制是否曾承诺挡住它」，没承诺过的归入设计范围问题，不与安全事件混账。④ **同名的两个词必须并列分家**：routing selector vs authorization token、collaboration guardrail vs tenant isolation ⇒ 名字相近而语义不同的两件事要在同一处并列定义，否则下游按其中一种语义使用时无人会发现。⑤ **共享能力 = 共享授权**：能给工具型 agent 发消息的每个人，都共享该 agent 被委托的工具权限 ⇒ 「谁能跟它说话」与「它能做什么」是一条边界的两端，只收紧一端等于没收紧。⑥ 对 guild 的落点：共享身份/规则/交接的能力声明（Cap 清单、gated actions、分层授权）一律补一列「它不是什么」；新增 Cap 时同步写明该项**不防什么**，其他 agent 判重时才不会把「未覆盖」误读成「已失效」。
- 提升层：可复用 Skill / 治理。触发词：误读澄清、它不是什么、未承诺不等于被绕过、路由选择器不是授权令牌、协作护栏不是租户隔离、同表同级、控制声明带负向列、共享发信即共享授权。

## Capability 77 — 提问是「不续命、不授权、有终态」的暂停原语；提问权不可随委派下放（来源：docs.openclaw.ai `tools/ask-user.md` 9,167B + `tools/acp-agents/controls.md` 9,158B，2026-10-05 r420-A 独立 curl 取 .md 原文实拉）
- **实证**：官方原文「Answering a question does not grant the agent additional permissions.」「A pending question does not extend an explicit run budget.」「An aborted agent run cancels its pending Gateway question.」；超时返回 `status: "no_answer"` 后「the agent then continues with its best judgment」；`ask_user` 仅主会话可用，「Subagents and other non-primary runs do not receive it」；需要凭据时走 `secrets` 工具而非提问（masked prompt，不入 chat / transcript / 模型上下文）；多问题在消息通道「degrade to readable text」。
- **判据**：① **暂停不换时间**——等待人类不延长任何显式预算，run 被中止则其待答提问一并取消；把「在等人」当成「还在跑」会让预算与超时全部失真。② **回答 ≠ 授权**——人类回应的唯一产物是答案本身，不附带任何能力授予；凡"答了就算同意了方案/放开了权限"的设计都是把确认与授权混为一谈。③ **无答必须有既定去向**——`no_answer` 是合法终态且明确要求 agent 以最佳判断继续；"等人等到卡住"不是合法状态。④ **提问权不可委派**——子 agent 拿不到提问工具，委派任务不等于把"回头问人"的能力一起转交；需要子 agent 请示时，必须由主会话代问或预置决策规则。⑤ **提问通道不是安全输入面**——凭据走独立 masked 通道，绝不进对话与上下文；在提问里收密钥等于把秘密写进转录。⑥ **同一提问跨通道形状会降级**——结构化控件在消息通道降为可读文本，语义保持但可机读性丢失；依赖结构化回执的下游必须在降级通道上改用文本解析或显式回退。⑦ 人类等待须有上下界（超时钳制 30–3600s），无界等待等价于把控制权交出去且收不回。
- **与既有能力分工**：Cap67 管「工具清单是限流不是授权、生效的是交集」（清单与父策略）；Cap73 管「配对成功不得连带授予命令」（设备/通道配对）；Cap71 管「一次性触发用完即停用」（调度形状）。本条管**人机交接这一条回路本身的语义**——等待、回应、无答各是什么。
- 提升层：工作流 / 安全边界。触发词：ask_user、提问不授权、no_answer、暂停不续命、提问权不可委派、凭据不走提问、通道降级。

## Capability 78 — 双身份分离：拥有会话的 agent 与外部执行体是两个独立身份，冲突必须可见失败（来源：docs.openclaw.ai `tools/acp-agents/controls.md` 9,158B + `tools/acp-agents/sessions.md` 7,281B，2026-10-05 r420-A 独立 curl 取 .md 原文实拉）
- **实证**：官方原文「The OpenClaw agent that owns a session is separate from the external harness selected by ACP.」——owner 携带 `agentId`，`agent` 只是 harness 名；「Bare keys such as `global` require an explicit owner when ownership is explicit.」「Conflicting owner/key pairs fail visibly.」；运行时控制须 owner identity 或 `operator.admin`，非 owner 只能用 `sessions`/`doctor`/`install`/`help`，且「For non-owner senders, `/acp sessions` lists only the current bound or requester session」；「`/acp steer` queues a follow-up; it cannot add input to the running ACP turn.」「To redirect work in progress, run `/acp cancel` first」；「`/acp cwd` … closes the previous handle before replacing it」。
- **判据**：① **归属与执行是两个身份，必须各自命名**——"谁的会话"与"哪个引擎在跑"分开记账，混成一个字段后既无法审计也无法回收。② **裸名必须有显式归属，冲突要可见失败而不是静默择优**——两个身份撞在一起时报错，比悄悄选一个更能防止越权。③ **只读也分可见面**——非 owner 的"列表"只列自己；把"能读"当成"能读全部"会在审计时漏掉别人的领地。④ **转向 ≠ 改道**——排队指令只能在当前回合结束后跑，没有插队能力；想改正在做的事必须先取消，"我发了新指令所以它应该改方向"是不成立的假设。⑤ **换上下文会销毁旧句柄**——切换工作目录先关闭上一个 handle，热替换不成立；凡是"改了就立刻生效且不中断"的预期都要显式验证。
- 提升层：工作流 / 安全边界。触发词：双身份、owner 与 harness、裸键显式归属、冲突可见失败、只读可见面、steer 不插队、换目录销毁句柄。

## Capability 79 — 短时能力凭证：撤销先于过期、URL 不放可复用凭据、缓存命中不绕过鉴权（来源：docs.openclaw.ai `web/control-ui/security-model.md` 12,843B，2026-10-05 r420-C 经 llms.txt 211,319B 定位真路径后 .md 实拉）
- **实证**：官方原文「Browser-rendered image, audio, video, and document URLs use `mediaTicket=<ticket>` instead of the active gateway token or password. The ticket expires quickly and cannot authorize a different source.」「Losing session visibility or role permissions stops new reads through existing tickets, even before they expire.」；「The revision is a cache key, not an access token; unversioned image requests retain the original image.」；「Conditional requests still require authentication before returning `304 Not Modified`.」；「keeps media rendering compatible with browser-native media elements without putting reusable gateway credentials in visible media URLs」；已加载图像在连接或元数据续期失败时仍可见但「it does not extend its media ticket or authorize fresh reads」；显式 missing / access-denied / 源、凭据或访问范围变化即清除保留图像；管理员 **Allow image**「without changing the session's permissions or allowing its parent folder」；过载时返回 `503` + `Retry-After: 1`「instead of a permanent lookup failure」。
- **判据**：① **撤销先于过期**——授权状态一变，票据立刻失效，不等 TTL；把过期当作唯一的失效机制等于给撤销留了一个 TTL 长的窗口。② **可见 URL 里只能放不可复用、不可换源的一次性凭证**——把长期凭据放进资源 URL 等于把凭据写进日志、referrer 与浏览器历史。③ **缓存命中不得绕过鉴权**——条件请求返回 304 之前仍要过认证；"命中了就不查权限"是最常见的越权捷径。④ **展示存活 ≠ 授权存活**——已渲染内容可以在凭证失效后继续显示（体验需要），但这既不延长票据也不授权新读取；缓存是展示层概念，绝不能升格成权限层概念。⑤ **失效信号必须逐条枚举**——missing / access-denied / 源变化 / 凭据变化 / 访问范围变化，任一即清缓存；靠"感觉该清了"必然留下一条没清的路径。⑥ **一次性例外不得扩面**——放行单个文件不等于放行其父目录，也不改变会话权限；例外的粒度要写到被放行的最窄对象。⑦ **过载降级要带重试语义**——503 + Retry-After 把临时状态表达为"稍后再来"，压成永久失败会让调用方误判为终态。⑧ **修订号是缓存键不是令牌**——无版本的请求仍应返回原对象，不得因为版本号不对就当成未授权。
- **与既有能力分工**：Cap56 管「令牌轮换不能借以升级角色」；Cap73 管「能力生效要过三道门」；本条管**凭证在签发之后的整段生命周期**——何时失效、失效如何传播、缓存与展示会不会让它"假活"。
- 提升层：安全边界 / 工具。触发词：短时凭证、撤销先于过期、URL 不放凭据、缓存不绕过鉴权、展示存活不等于授权存活、一次性例外不扩面、Retry-After、修订号是缓存键。

## Capability 80 — 治理是否生效取决于装配路径：经构造器接入才自动获得聚合/去重/缓存，手工组合则三者全无（来源：learn.microsoft.com/agent-framework/agents/skills 156,444B，2026-10-05 r421-A 独立 curl 实拉逐串命中；消化 Qoder r407-Q-A N10 积压点）
- **实证**：官方原文「Builder — AgentSkillsProviderBuilder assembles multiple sources into a single provider, applying **aggregation, deduplication, caching, and optional filtering**. In Python, compose source classes such as AggregatingSkillsSource, FilteringSkillsSource, and DeduplicatingSkillsSource **directly**.」；「DeduplicatingSkillsSource — removes duplicate skill names (**case-insensitive, first occurrence wins**). Duplicates are logged at warning level.」；「refresh_interval … **When None (the default), cached results never expire**.」；「Concurrent callers for the same cache key **share a single in-flight fetch**, so the inner source is queried at most once per key.」；`cache_isolation_key_selector`「**Returning None (or leaving it None) uses a single shared cache bucket**」。
- **判据**：① **"有治理"不是能力的属性，是装配方式的属性**——同一批技能源经构造器装配就自动获得聚合/去重/缓存，手工逐个组合则三者全部消失、顺序也全由调用方自控 ⇒ 迁移或换装配器时，治理能力会随装配方式一起丢失而不报错；验收要问"这批能力是谁在管"，不是"这批能力有没有"。② **去重策略必须显式择优并留痕**——大小写不敏感、首个胜出、重复项打 WARNING ⇒ 静默 last-wins 与静默 first-wins 同样危险（前者悄悄换掉，后者悄悄丢掉），唯一的区别是有没有那条警告；凡"同名冲突"必须有可观测的一条记录。③ **缓存默认永不过期是显式选择不是缺陷**——`refresh_interval` 为 None 即永不过期 ⇒ 任何"缓存多久失效"的问题必须先确认这个旋钮是否被设置；把它当"实现了缓存"就默认有失效机制，会让陈旧目录长期假活。④ **缓存分域键决定泄漏面**——不设隔离键则所有调用方共享同一个桶 ⇒ 多主体（per agent / per tenant）场景下"共享缓存"等于跨主体可见；分域是安全属性不是性能调优。⑤ **并发合流要写在契约里**——同键并发共享单次在途取数，源最多被查一次 ⇒ 合流既省调用也掩盖了"有多少人真的想要"，观测侧要单独立计数。
- **与既有能力分工**：Cap72 管「分层作用域只允许收窄不允许放大」（谁能给自己加东西）；Cap67 管「工具清单是限流不是授权」（清单与授权）；本条管**装配这一层**：同一份内容走不同装配路径时，治理是"附带获得的"还是"必须自己接的"。
- 提升层：工具 / 治理。触发词：装配路径、构造器聚合去重缓存、手工组合失治理、first occurrence wins、缓存永不过期、隔离键分域、共享缓存桶、并发合流。

## Capability 81 — 收紧型完整性规则以「默认关的 flag」灰度落地：开关为真 ≠ 行为已换（来源：www.activepieces.com/docs/install/reference/environment-variables.md 24,703B，2026-10-05 r421-A 独立 curl 取 `.md` 实拉；消化 Qoder r407-Q-A N9 + r408-Q-B B8 积压点）
- **实证**：官方环境变量表原文「`AP_ENFORCE_CONNECTION_PIECE_BINDING` | Reject a step's connection at runtime unless the connection was created for the same piece as the step. | **`false`**」——绑定收紧规则出厂即为关；同族先例 n8n `N8N_SCHEDULER_ENABLED=true` 缺配套 publication service 时**只 warning、旧行为原样继续**。
- **判据**：① **收紧型规则默认关是迁移兼容取舍，不是安全建议**——"凭据只能被创建它的那个能力用"是完整性收紧，出厂关着是为了让存量流程继续跑 ⇒ 抄默认值 = 把过渡期妥协固化成长期架构；启用这类 flag 前要问"关着时谁在受益"。② **"开关为真"与"行为已换"之间隔着前置依赖**——启用新子系统需要同族第二个开关在位，否则只 warning、旧行为继续 ⇒ 失败模式不是报错而是"看起来在跑"，是最难发现的一类假生效；启用类变更的验收动作必须是**验证行为真的换了**，不是读回配置值。③ **首次覆盖范围要单独确认**——新开关的覆盖范围常不含同类能力（须另 flag）⇒ 只开一个就以为同类全部收紧，会在同源的另一半上留出未收紧面。④ 对 guild 的落点：跨 agent 引入新纪律时，先判这条纪律是"收紧型"（会打破存量）还是"放宽型"，收紧型一律走 flag + 灰度 + 存量豁免清单，不一次性全局生效。
- 提升层：工具 / 治理。触发词：收紧型 flag 默认关、灰度而非破坏性变更、开关为真不等于行为已换、前置依赖静默降级、同类能力另需 flag、迁移兼容默认值。

## Capability 82 — 删除即持久准入政策：被遗忘项先入删除账本再清产物，排除状态跨重复清除与跨全量重建存续（来源：docs.openclaw.ai `cli/memory.md` 35,246B，2026-10-05 r421-A 独立 curl 取 `.md` 原文实拉逐串命中；消化 Qoder r407-Q-A N4 积压点）
- **实证**：官方原文「A real purge **records the selected session IDs as forgotten in the agent's SQLite database before removing artifacts**.」；「Automatic dreaming ingestion, `memory session-backfill`, and transcript indexing, **including `memory index --force`**, check those records.」；「**Repeating the purge does not remove the exclusion, and removing an admission-policy rule does not undo it.** Future sessions with new IDs are not excluded by a previous purge.」；另有「Sessions previously selected by `memory forget` also remain excluded.」
- **判据**：① **删除的顺序是"先记账、后清产物"**——先把 ID 写进持久排除账本，再删实体 ⇒ 反序会留下一个窗口：产物还没清完，重新入场的摄取流程已经把它当新材料读回来了。② **排除状态必须比任何一次重建更长寿**——跨重复清除、跨准入规则移除、跨 `--force` 全量重建都存续 ⇒ "重建索引"不能成为"被删内容复活"的通道；凡有全量重建路径的系统，删除决定必须存在重建读不到也抹不掉的地方。③ **排除的粒度是 ID 不是规则**——新会话 ID 不受既往清除影响 ⇒ 用规则表达"以后都别要这类东西"会连带误伤，用 ID 表达则精确但需持久；两者要分开存放，不能互相替代。④ **副作用的宽度要和意图核对**——按非空选择清除会连带清掉该 agent **整个**嵌入缓存 ⇒ 一次"删几个会话"的操作可能抹掉不相关内容的向量，操作前必须能回答"这次会顺带清掉什么"。
- **与既有能力分工**：Cap79 管「短时凭证撤销先于过期」（临时访问的失效）；Cap59 管「删除不抹历史版本」（版本保留）；本条管**被删除对象的"永不复活"**——删除决定本身要成为一条比重建更持久的政策。
- 提升层：工具 / 记忆治理。触发词：删除即准入政策、先记账后清产物、跨重建存续、forget 账本、排除粒度是 ID、连带清空嵌入缓存、删除防复活。

## Capability 83 — 守卫失败要按「谁不可判定」分极性：被检对象读不懂 ⇒ 阻塞；守卫自己没准备好 ⇒ 只警告继续；兼容窗口永不覆盖安全面（来源：api.github.com/repos/anthropics/claude-code/releases 96,622B，v2.1.289 changelog 一手命中，2026-10-05 r422-A 独立 curl 实拉；docs.openclaw.ai `gateway/protocol/versioning.md` 14,899B + `gateway/protocol/handshake.md` 18,434B，同轮独立 curl 取 `.md` 原文实拉逐串命中；消化 Qoder r418-Q-A 积压点）
- **实证**：Claude Code v2.1.289 原文「Fixed PreToolUse and PermissionRequest hooks **being skipped when matching them failed or the tool's input could not be serialized to JSON; the call is now blocked**.」；OpenClaw 原文「Device auth, pairing, scopes, command policy, and exec approvals are **unchanged by this compatibility window**.」；「Plugin-owned node ... because their hosted surfaces are **not part of the N-1 contract**.」；「None of these states triggers local fallback or automatic replay.」；handshake 侧「reports the negotiated role and the current socket's effective authorization scopes **even when no device token is issued**」。
- **判据**：① **守卫失败要分两种，默认极性相反**——失败原因是「被检对象无法解析/匹配不上」（输入不可序列化、载荷读不懂）⇒ 必须**阻塞**，因为"跳过"在效果上等于默认放行，守卫不存在与守卫放行是同一结果，这是安全默认极性的错置；失败原因是「守卫自身配置缺失或前置开关未开」（Cap81 那条）⇒ 可以只 warning 并让旧行为继续，因为被检对象没变、风险敞口没有扩大。**判据一句话：读不懂的是"东西"就拦，读不懂的是"规则"就降级。** ② **兼容窗口必须有"不被窗口覆盖"的显式清单**——N-1 版本协商只放宽协议版本，设备认证、配对、作用域、命令策略、exec 审批五面不随之放宽 ⇒ 任何"向后兼容/灰度共存"的设计都要同时声明窗口边界：哪些面进窗口、哪些面绝不进；只写"支持旧版本"而不写"安全面不降"的兼容承诺，等于把安全面默认划进窗口。③ **插件/第三方自有面不在兼容契约内**——托管面属于宿主协议契约，插件自有 hosted surface 不享受 N-1 ⇒ 依赖插件面的调用方不能假定它与平台同寿命，升级判定要按各自的契约分别算。④ **降级状态不触发本地兜底与自动重放**——旧版本态走显式处理，不本地兜底、不自动重放 ⇒ "兼容"不等于"自动替它跑一遍"，隐式重放会把一次失败放大成两次副作用。⑤ **协商结果回执独立于凭据发放**——即使未签发设备令牌，也要回报协商出的角色与生效作用域 ⇒ 生效权限的可见性不能绑定在"有没有拿到凭据"上，否则无凭据连接会成为观测盲区。
- **与既有能力分工**：Cap81 管「收紧型 flag 默认关、前置缺失时只 warning 旧行为继续」（守卫没准备好）；Cap76 管「控制声明要自带误读澄清」（声明怎么写）；Cap72 管「分层作用域只收窄不放大」（作用域叠加）；本条管**失败与兼容这两类"边界时刻"的默认取哪一侧**，并给出 Cap81 与本条的适用分界。
- 提升层：工具 / 治理。触发词：守卫读不懂就阻塞、跳过等于放行、兼容窗口不覆盖安全面、N-1 契约边界、插件面不在契约内、协商回执独立于令牌、不自动重放。

## Capability 84 — 循环上限要按「循环的种类」分别设置，且按对端分别计数：自递归 ≠ 跨实体往返（来源：docs.flowiseai.com/llms-full.txt 618,913B「Understanding Max Iteration parameter in Workers」段，2026-10-05 r422-B 独立 curl 实拉逐串命中；与 Cap74「预算计尝试非产出」互补——那条管计数口径，本条管上限该按什么维度切分）
- **实证**：官方原文「`Max Iterations Cap` … serves as a guardrail against excessive, potentially infinite, interactions between the Supervisor and Worker. **Unlike the Supervisor node's `Recursion Limit`, which restricts how many times the Supervisor can call itself**, the Worker node's `Max Iteration` parameter limits **how many times a Supervisor can iterate or query a specific Worker**. By capping or limiting the Max Iteration, we ensure that costs remain under control, even in cases of unexpected system behavior.」
- **判据**：① **"自己调自己"与"来回调别人"是两个正交的循环，必须两个计数器**——Recursion Limit 只约束主管自调用，Max Iteration 约束主管对某个工人的查询次数 ⇒ 只设前者时，A↔B 无限往返完全不受约束，而"我设了递归上限"会给人一种已被兜住的错觉；排查失控循环时先问"失控的是哪一种循环"。② **上限要挂在"对端"上，不是全局一个值**——限制的是"查询某个特定 worker 的次数"，每个工人各有一份 ⇒ 全局上限会被"轮流调用多个工人"摊薄绕过（每轮都换一个对端，全局计数永远不满）。③ **上限的验收问题是"成本是否可控"而不是"有没有死循环"**——原文把收益写成 costs remain under control ⇒ 失控的形式不只是卡死，也可以是长时间合法运行导致的成本失控；只看 CPU/挂起会漏掉这一类。④ **两个上限的默认值要分别核对**——不同层级、不同种类的限制常有各自默认值，改了一个不等于另一个也收紧 ⇒ 变更验收要逐个上限验证，不能因为"限制了循环"就认为所有循环都被限制。
- **与既有能力分工**：Cap74 管「预算计的是尝试次数不是产出数量」（计数口径）；Cap71 管「队列有界、超限停源留错」（积压封顶）；本条管**多实体编排中上限该按哪些维度切分**（种类 × 对端）。
- 提升层：工具 / 治理。触发词：递归上限与迭代上限是两个计数器、按对端计数、自递归不等于跨实体往返、上限挂在对端、成本失控也是失控、逐个上限验证。

## Capability 85 — 认证只定「角色」，授权在每次调用上另判；应用内权限不是隔离边界，强隔离要在 OS 用户/主机层；等待式读取在返回前重检五要素（来源：docs.openclaw.ai/gateway/operator-scopes.md 39,492B，2026-10-05 r423-A 独立 curl 取 `.md` 原文实拉逐串命中；与 Cap72 分层作用域 / Cap83 守卫极性互补——那两条管"作用域怎么叠加"与"守卫失败站哪一侧"，本条管"认证之后还有一层授权"以及"这套东西的隔离边界在哪一层"）
- **实证**：官方原文「Operator scopes gate what a Gateway client can do **after it authenticates**.」「They are a control-plane guardrail inside one trusted Gateway operator domain, **not hostile multi-tenant isolation**. For strong separation between people, teams, or machines, **run separate Gateways under separate OS users or hosts**.」；「Operator RPC methods require the `operator` role. Node-originated methods require the `node` role.」；作用域表「`operator.admin` … **Satisfies every `operator.*` scope**」「`operator.write` … Also satisfies `operator.read`」；自作用域例外段「These methods **do not expose team secrets, mutate shared configuration, or grant write/admin scopes**.」；收尾「Identity, role, access grant, connection, and session visibility are **rechecked before returning awaited reads**.」
- **判据**：① **通过认证不等于获得授权**：连接进来只确定"我是哪一类客户端（角色）"，每个方法再按 scope 单独判 ⇒ 把"已认证"当"已授权"，等于把一次身份检查当成全会话通行证。**判据一句话：认证回答"你是谁"，scope 才回答"这一下能不能做"。** ② **应用内权限模型不能冒充隔离边界**：官方明说这套 scope 只是**同一信任域内**的控制面护栏、**不是对抗性多租户隔离**，要强隔离就在 OS 用户/主机层分开 ⇒ 设计权限前先声明威胁模型是"防误操作"还是"防恶意邻居"；声称防恶意而执行边界仍在同一进程/同一账号内，就是伪隔离（纸面边界在被攻破的第一刻一起失效）。③ **角色要互斥且在入口强制**：控制面方法与能力宿主方法分属两个角色，各自只能由对应角色发起 ⇒ 角色不互斥等于默认全能，"都是可信内部调用"是最常见的越权通道。④ **判定一个"只读"令牌是否真只读，要看高阶蕴含**：`write` 满足 `read`、`admin` 满足全部 ⇒ 宣称只读的凭据如果和更高阶凭据同源或可被同一调用方替换，它的"只读"只是标签。⑤ **自作用域例外必须自带四条不越权断言**：只操作自己的账号 + 不暴露团队密钥 + 不改共享配置 + 不授予更高 scope，缺一条它就不是"例外"而是提权后门。⑥ **异步/等待式读取要在返回前重检**：身份、角色、授权授予、连接状态、会话可见性五项在 await 之后重新校验 ⇒ 入口验一次 ≠ 出口仍成立，等待窗口里权限可能已被撤销或会话已不可见。
- 提升层：工具 / 治理 + 安全边界。触发词：认证不等于授权、连接角色、认证后的第二层授权、应用内权限不是隔离、OS 用户或主机层隔离、高阶蕴含低阶、自作用域例外、等待读前重检、await 后重校验。

## Capability 86 — 凭证作用域必须下沉到「资源」这个最小单元，租户/工作区级默认值是漏洞（来源：api.github.com/repos/langgenius/dify/releases 244,162B，v1.17.1 一手命中，2026-10-05 r424-A 独立 curl 实拉 JSON 逐串命中；消化 Qoder r418-Q-A 积压点，更正其"Dify v1.17.1"为带 issue 上下文的实词）
- **实证**：官方原文「**Knowledge base service-API keys were scoped to the whole workspace**: one key could read and write **every** knowledge base in the tenant, so giving an integrator a key gave them a key to the whole tenant.」；v1.17.1 新增「**Dataset-Scoped** Knowledge Base API Keys」将作用域收敛到单个知识库。
- **判据**：① **默认作用域越大，越接近漏洞**——"一钥通tenant读改写所有知识库"是出厂默认就存在的敞口，不是配置错误 ⇒ 评价凭证方案时，先看"拿到这把钥匙最坏能摸到多大范围"，再看它默认就是多大；默认过大的系统，集成方一拿 key 就等于拿到全租户。② **blast radius 的最小单元是"资源"不是"应用/用户"**——按知识库隔离（dataset-scoped）而非按 workspace/tenant ⇒ 给第三方集成时，只能给"它该用的那一个"，不能给"它所在的那一堆"。③ **收敛动作要可独立撤销与审计**——dataset-scoped 之后，每个 key 绑一个资源，回收/轮换/审计都落到资源粒度 ⇒ 租户级 key 一旦泄露，回滚要重发全租户所有依赖。④ **同类收敛要顺势做满**——同批次 Dify 还把 RAG/conversation/workspace-credential/OAuth-client 资源"consistently bound to their owners and app scope"，说明作用域下沉不是单点补丁，而是一组资源的统一治理 ⇒ 引入任何凭据体系时，逐个资源问"它默认绑在哪一级"。
- **与既有能力分工**：Cap79 管「短时凭证撤销先于过期、一次性票据不扩面（放行单文件不放行父目录）」；本条管**长期服务凭据的默认作用域粒度**——Cap79 防的是"一次性令牌被放大"，本条防的是"长期 key 出厂就过大"，两者都是作用域最小化，按凭证寿命分两侧。
- 提升层：工具 / 治理。触发词：凭证作用域下沉到资源、租户级 key 是漏洞、dataset-scoped、blast radius 最小单元、默认作用域越大越接近漏洞、收敛可独立撤销。

## Capability 87 — 新能力不得绕过宿主既有的安全策略；自建旁路等于关掉这道墙（来源：api.github.com/repos/langgenius/dify/releases 244,162B，v1.17.0 一手命中「Agent skills bypassed the SSRF private-network policy」段，2026-10-05 r424-A 独立 curl 实拉 JSON 逐串命中；与 Cap63 信任不跨层传递 / Cap64 可丢通道结构上不可公网可达 互补——那两条管"凭据由谁签""哪些数能放会丢通道"，本条管"新能力不能悄悄拆掉宿主已有的边界"）
- **实证**：官方原文「**Agent skills bypassed the SSRF private-network policy.** Agent traffic goes through a **separate proxy that ignored `SSRF_PROXY_ALLOW`**」；同批次另有「short-lived agent authorization tokens」「token expiry (EMAIL_CODE_LOGIN_TOKEN_EXPIRY_MINUTES)」「Azure Key Vault / Pluggable KMS」。
- **判据**：① **能力一旦引入，必须复用宿主既有策略，不能另走一条不带策略的旁路**——agent 流量走了独立代理、该代理没继承 SSRF 允许列表 ⇒ 加一个能力，等于在不知情的情况下把网络边界墙开了一个洞；评价新能力时，先问"它走的通道有没有继承宿主已有的安全约束"，没有就是回归。② **"独立实现"最易漏掉的是安全默认值**——不是故意绕开，而是新模块没接旧策略 ⇒ 接入任何新代理/通道/执行体，安全策略是必接项不是可选项；审计清单里"安全策略是否透传"要和"功能是否可用"并列。③ **能力通道要可观测、可统一管控**——SSRF 策略失效是因为代理层各自为政 ⇒ 凡引入并行通道，必须能纳入同一套策略/审计面，否则它迟早成为绕过点。④ **配套：短命授权令牌 + 令牌过期 + 外部 KMS** 是"凭据生命周期"的同一组手段（Cap79 的短时凭证在此得到开源产品级佐证）⇒ 新能力的授权缺省应是短命、可过期、由专用密钥库管理，而非长命共享。
- **与既有能力分工**：Cap63 管"信任不跨层传递、令牌单点签发"；Cap64 管"可丢通道结构上不可公网可达"；本条管**新增能力对宿主既有边界的尊重**——前两条定的是"应该怎么建"，本条定的是"不能拆掉已有的"。
- 提升层：工具 / 治理。触发词：能力不绕过宿主策略、自建旁路等于拆墙、独立代理须继承安全默认、策略透传是必接项、并行通道须统一管控。

## Capability 88 — 扩展/插件机制默认是中性能力放大器，不自带安全约束；约束要靠独立的 allow/策略列表显式叠加（来源：docs.openclaw.ai `concepts/model-providers/custom-providers.md` 18,145B，2026-10-05 r424-B 独立 curl 取 `.md` 原文实拉逐串命中；与 Cap87 能力不绕过宿主策略 互补——那条讲"新增能力必须复用宿主策略"，本条讲"扩展点天然不绑策略，约束要显式加"）
- **实证**：官方原文「it neither **restricts overrides** nor **registers a new runtime model** by itself. For custom provider models, also add `models.providers.<id>.models[]` …; use `agents.defaults.modelPolicy.allow` **separately** when you want an override restriction.」；另有「Many of the bundled provider plugins … already publish a **default catalog**. Use explicit `models.providers.<id>` entries only when you want to **override** the default base URL, headers, or model list.」
- **判据**：① **扩展点开放 ≠ 受控，二者是独立的两件事**——自定义 provider 扩展点"既不限制覆盖、也不注册新运行时模型"，限制要另配 allow 列表 ⇒ 不要把"平台支持插件/自定义"误读成"已经过安全评审"，扩展点的存在只是把能力放大器装上了，约束是另一份要单独写的东西。② **默认走信任目录，覆盖才是显式动作**——bundled 插件自带默认目录，只有在你想改 base URL/headers/模型列表时才写显式 entries ⇒ 覆盖是显式、可审计、非默认的；凡是"静默合并"自定义配置的扩展点，等于把默认信任边界交给调用方随意改。③ **约束叠加是"另配"而非"内置"**——modelPolicy.allow 与扩展注册是两条独立的配置路径 ⇒ 引入任何扩展机制时，默认假设它不限制任何东西，必须主动去挂约束，漏挂就是敞口（Cap87 的"悄悄拆墙"在扩展点场景的具体形态）。④ 对 guild 的落点：引入任何"可装插件/可自定义 provider/可注册节点"的能力，发布门禁里单列一条"扩展点的约束是否显式挂上"，与"功能是否可用"并列验收。
- **与既有能力分工**：Cap87 管"新能力不得绕过宿主既有策略"（被动防拆墙）；Cap79 管"凭证作用域最小化"；本条管**扩展机制本身的约束缺省是空**，必须主动加 allow/策略（主动补墙）。
- 提升层：工具 / 治理。触发词：扩展点中性需另配策略、默认目录vs显式覆盖、allow列表显式叠加、扩展开放不等于受控、静默合并自定义配置。

## Capability 89 — 发现/索引类缓存必须在「部分刷新失败」时保留每条目的真实状态：empty（确无内容）≠ unavailable（取数失败）≠ stale（已过期未刷新）；部分失败不得把 unavailable 静默升级为可用，也不得把 empty 当成 present（来源：docs.openclaw.ai/providers/bedrock.md 21,784B，2026-10-05 r425-A 独立 curl 取 `.md` 原文实拉逐串命中 L140-151；与 Cap80「治理取决于装配路径、refresh_interval 默认永不过期、隔离键分域」互补——那条管装配时的缓存配置，本条管部分刷新时的状态完整性）
- **原文**：「Both lists, including every inference-profile page, must succeed before OpenClaw caches the result. A failed refresh reports unavailable or rejected catalog access… failures and retain successful empty provider results, as the bundled catalog…」；「Discovery is shared with the CLI backend and cached until process restart」；「failed CLI probe uses OpenClaw's maintained version floor」；「A failed refresh reports unavailable or rejected catalog access」；「retain successful empty provider results」。
- **判据**：① **部分刷新必须逐条目定状态**：成功但无内容的条目保留为 empty（不是"有内容"），取数失败的条目标记为 unavailable（不是"用旧缓存"也不是"假装成功"）；把 empty 当 present、把 unavailable 当可用，都会让后续调用产出错误结论。② **缓存新鲜度必须有界**：发现结果缓存到进程重启或显式 TTL，过期必须重取，不得无限复用陈旧目录——与 Cap80 ③「缓存默认永不过期是显式选择」同向，本条补上：有界 freshness 必须由调用方显式设置且可被观测，不能依赖"进程什么时候重启"。③ **部分失败不降级整体**：catalog 刷新中部分条目取数失败，成功的保留、失败的标记不可用，整体可用状态必须反映最弱条目，绝不因"大部分成功"就整体标绿。④ **三态可观测**：empty / unavailable / stale 必须能被诊断接口区分报告，不能只报"成功/失败"两态——否则排障时无法分清"没配"与"取不到"与"过期"。
- 提升层：治理 / 可复用 Skill。触发词：发现缓存、部分刷新、empty≠unavailable≠stale、缓存新鲜度有界、进程重启失效、部分失败不降级整体、三态可观测、陈旧目录不复用。

## Capability 90 — 「自动发现」型凭据解析是用便利换掉作用域的分维能力：同一宿主上所有自动发现通道共享一个身份与一套权限，逐路收窄在机制内做不到（来源：docs.n8n.io `administer/manage-credentials/use-external-secret-stores.md` 21,594B，2026-10-05 r426-B 独立 curl 取 `.md` 原文实拉逐串命中；与 Cap86「凭证作用域下沉到资源」互补——那条管默认作用域的粒度大小，本条管自动发现机制本身让粒度收窄在结构上不可达）
- **原文**：「n8n doesn't take any credentials input for that vault; it resolves whatever identity is available in its runtime environment. That means **every vault you configure with Auto Detect on the same n8n instance shares one IAM identity and one set of permissions**. You can't assign different IAM scopes … to separate Auto Detect vaults.」；「If you need to scope secret access per vault, per project, or per team, **use IAM User instead**: create a separate IAM user and access key per vault, and attach an ARN-scoped policy to each one.」；「Auto Detect is best suited to a single global vault, or to setups where every project sharing that vault should have the same access.」
- **判据**：① **自动发现＝把作用域的决定权交给运行时环境，代价是分维收窄能力被吃掉**——同一宿主上所有自动发现通道共用同一身份与同一套权限，"这一路只给它该碰的几个资源"在机制内做不到 ⇒ 引入自动发现型凭据（SDK 默认链 / 环境变量 / 实例角色 / 宿主 ambient 身份）前先问"这几路是否需要不同作用域"，需要就必须放弃自动发现。② **要分维就必须显式化：一路一身份、一身份一策略**——官方给的对照解是每 vault 独立身份 + 独立密钥 + ARN 级策略 ⇒ 最小权限与自动便利是**互斥选项**而非可调参数；凡是"按资源 / 按项目 / 按团队"分维的需求，显式身份是唯一出路。③ **自动发现的适用面只有"单一全局通道"**——官方明说它最适合单个 global vault 或所有共享方权限相同的场景 ⇒ 把自动发现用在多方共享宿主上，等于默认把所有方拉齐到同一权限面（多方里权限最小的那家被静默抬高）。④ **审计口径**：清点凭据来源时"自动发现"要单列一类并标注"作用域不可分维"，不能与显式身份混在同一张清单里按同一标准评估；把 ambient 身份当"已配置的凭据"记账，会得出"每路都已收窄"的假结论。
- 提升层：工具 / 治理。触发词：自动发现凭据、Auto Detect、默认凭据链、ambient 身份、便利换最小权限、作用域不可分维、一路一身份、ARN 级策略、全局 vault。

## Capability 91 — 权限/范围类配置能否下放给终端用户，判定基准是「违规后果落在谁的合规身份上」；且下放范围不沿类型继承链传递（来源：docs.n8n.io `administer/manage-credentials/credential-overwrites.md` 5,099B，2026-10-05 r426-C 独立 curl 取 `.md` 原文实拉逐串命中；与 Cap86「默认作用域过大」/ Cap77「提问权不可随委派下放」互补——那两条管"默认给多大""哪个原语不可下放"，本条管"下放的判定基准是后果归属"）
- **原文**：「Letting users set their own scopes **can break verified OAuth apps**. Many providers, such as Google, require you to define and justify every scope your app requests during app verification. If a user adds a scope you didn't declare, the provider may **suspend or ban your app**. Only enable this setting for credential types where users adding scopes won't put your app's verification at risk.」；「This setting applies **only to the credential types you list**. It **doesn't apply to credential types that extend** a listed type.」
- **判据**：① **下放的代价不在"用户多拿到多少权限"，而在"后果记在谁的账上"**——用户加一个未声明的 scope，被暂停/封禁的是平台方已验证的应用身份 ⇒ 凡后果外溢到主体**合规资格**（应用验证、封禁、牌照、信誉分）的配置，一律不可下放；判据问句是"它坏了谁遭殃"，不是"它能给谁方便"。② **每个可下放开关必须自带风险归属声明**——官方要求只在"用户加 scope 不会危及 app 验证"的类型上开启 ⇒ 开关的文档里要写明它失控时的受损害方，写不出受损害方的开关默认关闭。③ **下放的适用范围不沿继承链传递**——该设置只作用于显式列出的类型，不作用于继承它的派生类型 ⇒ 派生方会带着"看起来继承了、实际没有"的错觉运行；凡"只匹配显式列出项"的白名单/开关，必须显式声明对派生项的语义（继承 / 不继承 / 须单独列出），否则继承体系里会出现静默的配置缺口。④ 对 guild 的落点：给终端用户或子 agent 开"可自选权限范围"的口子之前，先登记这条口子失控时哪个主体的资格受损；若存在类型继承/派生关系，再核一遍派生项是否被静默排除在外。
- 提升层：治理 / 工具。触发词：下放权限配置、后果归属决定下放边界、verified app 被封、scope 不可下放、风险归属声明、显式列出项不作用于派生类型、继承链不传递配置。
