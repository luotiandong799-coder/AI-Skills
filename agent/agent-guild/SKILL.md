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
version: "1.66.0"
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
### Capability 16 — 凭据与执行体容器级物理分离 + 输出四级管线（来源：GitHub Agentic Workflows 官方安全架构，经 agentpatterns.ai / aidevme 2026-09-27 r205-C 实拉）
- **★三种凭据分装三个容器，agent 容器零密钥**：LLM 凭据在 **API proxy 容器**（agent 经代理调用，看不到 key）；MCP 凭据在 **MCP gateway 容器**（按仓库策略路由，HTTP 转发）；**agent 容器**只带防火墙出网白名单 + 只读 /host 挂载 + tmpfs 覆盖 + chroot jail。判据：**密钥不该和会读不可信输入的那个进程共处一个故障域**——agent 被提示注入打穿时，手上是没有任何凭据的。
- **★四个信任边界分层，token 绑在配置层不在 agent 内**：Substrate（VM 隔离 + 内核强制通信边界）/ Configuration（声明式权限分派 + token 绑定）/ Planning（分阶段工作流 + 显式数据交换）。判据：**权限是声明出来的，不是运行时协商出来的**。
- **★写操作走 safe-outputs 四级管线，没有临时写权限**：Operation filtering（限可调 API）→ **Volume limiting**（封顶次数，如"最多 3 个 PR"）→ Content sanitization（剥掉 URL 与 secrets）→ Moderation（确定性分析后才允许下游投递）。判据：**"能不能写"之外必须还有"写多少 / 写什么内容 / 谁复核"三道闸**——只管能不能写，一次失控就是无限 blast radius。
- **★默认只读 + agent 产的 PR 永不自动合并**：先把流程跑成只读/只评论、证明低噪音后再开放 label / 建 PR。判据：**放权按观测到的行为渐进，不按预期行为一次性给**。
- 与 §Capability 12 留痕通道独立于被测对象、§Capability 13 留痕范围由显式输出决定 的分工：那两条管"记录怎么写、写哪些字段"；本条管"**执行体手里有什么、能往外做什么**"——一个定留痕，一个定权限。
- 提升层：工作流 / 安全边界。

#<!-- 2026-10-01 r344A 下沉：Capability 17 记忆晋升三门整段 → references/knowledge-base.md §r344A -->

#<!-- 2026-10-04 r415 下沉：Cap35 + Cap36 → references/knowledge-base.md §r415-ag -->
> 入站准入双门与会话隔离粒度一节已零删减下沉至 references/knowledge-base.md 的 r417-ag 存档节。
## 评审类协作的质量由「给评审者什么上下文」决定，且评审必须尽早（来源：deeplearning.ai《AI Code Review》（Qodo，1h4m，Intermediate）2026-09-28 r208-C 独立实拉）
- **评审无效的常见根因不是评审规则写得不好，是评审者拿到的上下文不对**：课程核心断言 `context is what makes a review reliable`，做法是把 `giving the reviewer the right context` 当作设计评审流程的第一件事。判据：**改评审提示词前先改评审输入；上下文错了，规则越细越自信地错。**
- **评审要尽早运行，而不是等产物完整后一次评审**：课程明确"尽早运行评审"。判据：**评审推迟的代价是返工面变大，不是评审变准**；早评审发现的是方向问题，晚评审只能发现细节问题。
- **做评审 agent 时，先定义"它需要看见什么"，再定义"它该说什么"**：课程路径是先给对上下文 → 再构建自己的 review agent。判据：**顺序反了会得到一台语气很好但看不见关键面的评审机器。**
- 判重：与 wb-artifact-verification §独立证据源（验证要看独立证据）相邻——那条管「验证的独立性」，本条管「评审输入的完整性」。
- 提升层：工作流 / 可复用 Skill。触发词：评审上下文、评审不可靠、评审 agent、尽早评审、评审质量、review context、给评审者什么。

## 治理处置增「申诉期冻结态」：被质疑不下架，转只读冻结（来源：help.openai.com/en/articles/8798878-sharing-and-publishing-gpts 2026-09-28 r313-Q-C 浏览器实拉 + r279-C 复核）
- **实证**：OpenAI GPT 发布申诉期政策——"While an appeal is under review: You can continue using the GPT privately; You cannot edit or update it; You cannot share it with others until the appeal is resolved or you cancel it." 即**私人可用、禁编辑/更新/对外分享**的冻结态。
- **判据**：治理处置增一档「只读冻结」——被质疑/审核中的技能不下架、不删，转成"可私有使用、禁编辑/更新/对外分享"，申诉解决后自动解冻；另一硬前置：任何对外暴露动作/工具**必须自带隐私与出处声明字段**。
- 提升层：工作流。触发词：申诉期冻结、只读冻结、隐私出处声明、治理处置档、appeal under review。

## 说过 ≠ 记着：发消息本身不入队，任务必须由具名 owner 显式登记（来源：github.com/mvschwarz/openrig README 2026-09-28 r283-B 独立 WebFetch 取正文核验）
- **实证**：官方原文「**Sending a message does not itself create a queue item; the owner records the task.**」；配套命令 `rig send dev-owner@first-project '... Track the task in the queue and return its ID ...'` + `rig queue list --destination dev-owner@first-project`。拓扑另以 **YAML RigSpec 声明**（pods / members / edges / continuity policies / culture file）。同文佐证：YOLO **off by default**，`rig down --snapshot` / `rig up <name>` 快照恢复并逐节点报告 resumed/fresh/failed。
- **判据**：**通信内容与任务队列是两个东西**——消息被收到不等于任务被接下。跨 agent 交接时，必须由具名 owner 显式登记任务并给出 ID，否则「我们讨论过」会被当成「有人在做」，形成无人认领的假成功。
- **落地动作**：交接消息里凡含请求，结尾必须要求对方回一个**任务 ID**；收到请求的一方，登记动作先于回复动作。无 ID 的交接，发起方不得标记为"已派发"。
- 提升层：工作流。触发词：发消息不入队、said vs recorded、任务 ID、具名 owner、交接登记、假成功、RigSpec。

## 晋升收益门：只把「期望收益为正」的经验结晶成技能（来源：arXiv 2607.16621 MSCE 2026-09-28 r283-B 经 Qoder r316-Q-A 实拉取证；续 r205 §记忆晋升三门）
- **实证**：原文机制是**只把"正期望收益的 L2 策略"结晶为可调用技能**，并用 **reflection-weighted value backfilling** 把稀疏的终局反馈回传给中间步骤（基准 EvoAgentBench + LoCoMo）。
- **判据**：r205 已落的晋升三门是**频次口径**（score / recall-frequency / query-diversity）——回答"它常被用到吗"；本门是**收益口径**——回答"留住它划算吗"。**收益为负或不确定的策略不晋升**：一条被高频调用但每次都把事情带偏的经验，频次门全过、收益门不过，结晶成技能只会把错误固化。稀疏反馈还要有回传机制，否则只有终局成败可观测、中间步骤分不到功劳。
- **落地动作**：晋升候选同时过四门（频次三门 + 收益一门）；收益无法估计时**默认不晋升**，只留在日志里继续观察。
- 提升层：可复用 Skill / 工作流。触发词：晋升收益门、期望收益为正、结晶为技能、value backfilling、频次口径 vs 收益口径、不确定即不晋升。

## Capability 18 — 白名单字段的「空值语义」必须显式声明，且配置要能锁死为只读（来源：docs.langflow.org `mcp-client` 与 Lock 机制，2026-09-29 经 Qoder r320-Q-B 实拉取证；**WB 未独立复核，按引文落地并标注待复核**）
- LangFlow `mcp-client` 的 `tool` 字段**留空即放行该 server 全部工具**——"可选白名单"的缺省方向若是 allow-all，漏配＝全开。
- 判据：本文库凡 allowlist 字段统一约定**空＝拒绝全部**；且配置面应可"锁死为只读"（LangFlow Lock 可锁住 MCP server management 防运行时被改）。
- 与 AV §审计三维（2.46.0）不同面：那条讲证据留存，本条讲缺省权限方向与运行时可改性；与 §空数组语义（SA 3.45.0）同族。

## Capability 19 — 共享记忆里「多条条目」不等于「多份独立证据」：采纳判定要按来源族门控（来源：arXiv 2609.30813 CPB，2026-09-29 经 Qoder r321-Q-C 实拉取证；**WB 未独立复核，按引文落地并标注待复核**）
- 实测：相互相关的记忆条目被下游当作彼此佐证；**按来源门控后误采纳 0.06–0.09，未门控 0.22–0.47（约 4–5 倍）**；错误信念一旦未被质疑，下游 **0.97–0.99 直接复述**（一次污染、全程背书）。
- 判据：写入共享记忆时带**来源族 ID**，读取时把同族条目**折叠为一条证据**再参与判定——这正是 AV「三条独立证据源」里"独立"的定义。
- 与豆包 r172C（外部内容信任标签，ctx 自留地）、WB r155B（跳过沿依赖链传染，ed 自留地）分工：那两条管入口与传染，本条管记忆库内部的统计独立性。

## Capability 20 — 记忆检索范围就是权限范围，且扩大范围不保证更准（来源：arXiv 2609.29144，2026-09-29 经 Qoder r321-Q-C 实拉取证；**WB 未独立复核，按引文落地并标注待复核**）
- 实测反例：**接入全局记忆准确率 0.713，反而低于只用静态记忆的 0.775**；按来源族取回 0.816（增益 +0.063，95% CI [0.037, 0.094]）。
- 判据：扩记忆可见面后必须跑同一套题回归（与 AV「先固定模型」并成一条验收动作）；**可见面本身按权限对待**，跨用户/跨项目记忆不并入默认检索集。
- 与 §记忆晋升三门（r205-C）、晋升收益门（r283-B）不同对象：那两条管条目去留，本条管可见面与权限。


## Cap23 可选能力缺失时把入口藏掉，不回退到更宽的路径（fail-closed 而不是 fail-open）（来源：docs.openclaw.ai《What gets sandboxed》2026-09-29 r288-A 独立 curl 实拉原文核验）
- 原文：目录发现 "uses `ls` without granting shell execution"；自定义后端可选实现 `SandboxFsBridge.readDirectory({ filePath, cwd, signal })`，而 "`ls` is hidden when it is absent, and OpenClaw does **not** fall back to reading the host filesystem."
- 判据：**降级默认 fail-closed**——可选能力缺失时隐藏入口，而不是用次优实现顶上；因为"回退"多数时候等于放宽边界（此处回退就是拿宿主机文件系统给模型看）。对照 AV 已有的"静默降级是失败模式"，本条给的是正向设计写法：**没有就是不提供**。
- 提升层：工具。触发词：不回退、能力缺失、隐藏工具、fail-closed、SandboxFsBridge、ls 隐藏。


## Cap24 挂载是把沙箱戳穿的口子：默认读写、双层路径校验、shared 作用域忽略单 agent 配置（来源：docs.openclaw.ai《Sandbox vs tool policy vs elevated》2026-09-29 r288-B 独立 curl 实拉原文核验）
- 原文："`docker.binds` **pierces** the sandbox filesystem: whatever you mount is visible inside the container with the mode you set (`:ro` or `:rw`). **Default is read-write if you omit the mode**"——漏写模式即最宽权限，源码/密钥类必须显式 `:ro`。
- 校验做两遍：先对**归一化源路径**校验，再**沿最深存在祖先解析后校验一次**；原文 "Symlink-parent escapes do not bypass blocked-path or allowed-root checks"，且不存在的叶子路径同样安全校验（`/workspace/alias-out/new-file` 经符号链接父目录解析到被封路径则拒绝挂载）。
- 两个易漏点：`scope: "shared"` **忽略 per-agent binds，只认全局 binds**；挂 `/var/run/docker.sock` "effectively hands host control to the sandbox"，只能刻意为之。工作区访问（`workspaceAccess`）与 bind 模式互相独立。
- 判据：凡"把宿主机目录给执行体看"的配置，默认给只读、明确作用域优先级（共享作用域会吃掉个体配置）、并对路径做**解析后复检**而不是只查字面。与 Cap22（分界线与逃生口）互补：那条管进程边界，本条管**边界上被主动开的洞**。
- 提升层：工具。触发词：bind mounts、默认读写、:ro、符号链接逃逸、shared 忽略单 agent、docker.sock、挂载穿透。


## Cap25 沙箱的网络边界要单独声明：跑在云上 = 私网不可达（来源：docs.dify.ai `llms-full.txt`《New Agent》2026-09-29 r288-C 独立 curl 实拉原文核验；与 Cap22/24 构成跨厂沙箱边界三角）
- 原文："The agent's sandbox runs in the cloud, so **hosts on your private network aren't reachable**. Public URLs work; for internal material, add it to the agent's Files instead."
- 判据：沙箱边界不止文件系统与进程，**网络可达域**同样被切——把执行体搬进沙箱或云端，等于同时切断它对内网资源的访问；需要内网材料时走"上传进工作区"，不要去打通网络。
- **跨厂对照（闭合 r212 遗留「沙箱边界声明是否跨平台通则」）**：三家都显式且保守地写下能力上限——openclaw 明说 "not a perfect security boundary"、Dify 明说"私有网络不可达"，两家都把隔离默认态与逃生口分开管理。**通则成立**：凡提供隔离执行的产品，官方文档都会写明"能挡什么"；照抄这种句式写自家边界，**写不出"能挡什么"的隔离就是没想清楚的隔离**。
- 提升层：工具。触发词：沙箱网络边界、私网不可达、云上沙箱、边界声明、跨厂对照。


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
- **原文**：「End-user credentials let workflows run with the credentials of the person who **triggers** them, rather than a fixed credential.」；「Each connection belongs to the user who made it: **only they can use it, and only they can see the data it returns**.」；「**Sharing shares the template, not a connection.**」；admin 侧「An admin can see that an end-user credential template exists and that it has connections attached... **That count is all they see.** They can't: View anything about individual connections / View a connection's secrets / Use anyone's connected account in their own workflows / See the redacted output of executions that ran on another user's connection」；「**Deleting the credential template deletes the whole credential, including every user's connection**, not just your own.」；触发器「let you require that the triggering user has permission to execute the trigger... A user without that role **can't connect their account**.」
- **判据**：① **执行身份决定数据归属，不是权限表决定**——同一条工作流、同一份凭据定义，触发者不同则读到的数据与可见面完全不同；设计共享能力时必须先回答"这次以谁的身份执行"。② **"共享能力"与"共享授权"必须拆开**：跨项目/跨人传递的是模板（能力定义），接收方必须自己完成连接；拿到模板不等于拿到别人已建立的授权。③ **管理权不含使用权**——管理员能看到"有这个模板、挂了几条连接"，且仅此一个计数；不能查看连接、不能读密钥、不能拿别人的连接跑自己的流程、也看不到别人执行里的原文（只看到 redacted）。写治理规则时把"看得见存在"与"用得了实体"列为两个权限位。④ **删除模板是级联动作且毁的是别人建立的授权**：删模板连带删除全部用户连接，依赖它的工作流在重建前停止解析 ⇒ 凡"父对象被删会带走子对象已建立的授权"的操作，删前必须给连接计数 + 显式告警 + 影响面清单。⑤ **连接动作本身也要过权限门**——没有执行角色的用户连账号都连不上，不是"能连上就能用"。
- 提升层：安全边界 / 工作流。触发词：终端用户凭据、执行身份、模板 vs 连接、管理权不含使用权、admin 只见 redacted、删模板级联删连接、触发权限第二道门。


## Cap43 会话键相同不等于会话合并：取消半径是 agent 不是 key；隔离与归并是两个方向的配置；隐私模式必须声明「防谁」（来源：docs.openclaw.ai/concepts/session 22,767B，2026-10-03 r390B 独立 curl 取 `.md` 原文实拉；与 §入站准入双门 / §Cap35 改向与中止 互补——那两条管谁能进来、怎么改向，本条管进来之后上下文归谁、取消动作波及多远）
- **原文**：「With `session.scope: "global"`, the selected agent still owns its session. The shared key `global` **does not merge different agents' conversations**… Session lists, model filters, previews, and sharing controls also retain the stored conversation's agent」；「Stopping with `/stop`, deleting, resetting, or archiving a session **cancels only that agent's work** for the selected conversation. Another agent's active turn and queued messages are preserved even when the agents use the same session key.」；「If multiple people can message your agent, enable DM isolation. Without it, all users share the same conversation context, so **Alice's private messages would be visible to Bob**.」；`dmScope` 四档 `main`（默认）/ `per-peer` / `per-channel-peer`（推荐）/ `per-account-channel-peer`；「Native catalog source IDs, Matrix room and thread IDs, and Signal group IDs are **case-sensitive**: IDs that differ only by case identify different conversations.」；incognito「keeps its session entry, transcript, and compaction state **in process memory instead of on disk**… expires 24 hours after creation or when the Gateway restarts… **Activity does not extend its lifetime.** Expiry stops active work and **deletes the session and transcript without an archive**」；「Incognito **does not restrict the agent's normal tools**. An explicit request to save information, or any tool-driven file write, can still persist data outside the incognito session store.」；「OpenClaw still records operational diagnostics and **content-free audit metadata such as HMAC references**」；「This protects them from storage and other gateway-mediated users, **not from the gateway owner or process operator**, who can always observe live sessions.」
- **判据**：① **会话键是路由标签不是合并指令**——同一个 key 下不同 agent 各自持有独立会话与排队消息；"共用一个会话"这类描述必须落到"某 agent 的这条会话"。② **取消/重置/删除的作用半径要写明是哪一个 agent**：一个停止动作只取消该 agent 的工作，同 key 下别人的回合照跑；没写半径的取消操作，用户会以为停掉了全部。③ **默认共享隐含单人假设**：DM 默认全部共享一条会话，多人场景不显式开隔离就等于把 Alice 的上下文给 Bob；隔离粒度给四档（发送者 / 渠道+发送者 / 账号+渠道+发送者），且配了**反向的归并且**（`identityLinks` 把同一人的多身份映射成一个 peer）——**隔离与归并是两个方向的两套配置，不是同一旋钮的两端**。④ **身份标识的大小写敏感性必须显式声明**：只差大小写的 ID 会分裂成两条会话与两份记忆，这在排查"记忆怎么少了一半"时是最难想到的一类。⑤ **隐私模式的边界声明要回答三个问题**：防谁（防存储与其他网关用户，**不防宿主/运维**）· 仍然落到哪里（工具写盘照旧、模型提供方仍处理消息、operational diagnostics 与 HMAC 类无内容元数据仍记）· 何时消失（24h 或重启，活动不延长，过期即删不归档）。缺任何一问，"开了隐私模式"都是错觉。
- 提升层：安全边界 / 工作流。触发词：会话键不合并、取消半径、DM 隔离四档、identityLinks、大小写敏感 ID、incognito 防谁、活动不延长、过期不归档、隐私模式不限制工具。

## Cap44 队列溢出是策略不是故障：三种丢弃语义与默认合成补偿；排队不借权限，撤回对已接受的运行仍生效；并发是分车道的两级预算（来源：docs.openclaw.ai/concepts/queue 17,971B，2026-10-03 r390B 独立 curl 取 `.md` 原文实拉；与 §Cap35 改向/中止/配对合成结果 互补——那条管运行中的改向语义，本条管队列满与并发预算）
- **原文**：`drop` 三档——「`summarize`（默认）：drop the oldest queued entries as needed, **keep compact summaries, and inject them as a synthetic followup prompt**」；「`old`：drop the oldest… without preserving summaries」；「`new`：reject the newest message when the queue is already full」；`cap` 默认 20，「Values below `1` are ignored.」；权限面「Gateway input **retains its authenticated operator and original scope ceiling** while queued or delegated to a child… other input waits in FIFO order **instead of borrowing the active or newest sender's permissions**」；「An accepted turn can continue after its request returns or its client disconnects. **That does not extend revoked device authority or permissions removed by a current operator role.** Subsequent actions still check the original source, including work held by an accepted child.」；并发「A lane-aware FIFO queue drains each lane with a configurable concurrency cap… CLI, embedded, and Codex runs **share the same session-key lane** (`session:<key>`). Each turn waits there before acquiring the session's execution claim, **so changing runtimes cannot start a competing turn**.」
- **判据**：① **队列溢出必须先选语义再谈容量**：三档分别是"丢旧的但留下摘要并注入合成追问"（默认，等于**内容被改写后再送达**）·"丢旧的无补偿"·"拒绝最新的"。默认档会改变消息内容，所以"收到过"与"原样收到过"不是一回事；验收队列行为时必须确认用了哪一档。② **排队与合并都不借权限**：输入在排队或被委派到子执行体期间始终携带自己的 operator 与 scope ceiling，不合资格的只能在 FIFO 里等，不会"搭便车"借到当前运行者或最新发送者的权限。③ **权限检查不只在准入时做一次**：已接受的运行在请求返回或客户端断连后仍可继续，但**被撤销的设备权限与被移除的角色当场生效**，后续动作仍回查原始来源——包括已经被子执行体接走的工作。⇒ 撤销必须作用于"在飞的"，只拦新请求等于没撤。④ **并发是两级预算而非一个数**：先抢**会话 claim**（同 session key 的 lane，换运行时也绕不过），再抢**全局/父级预算**（main lane 受 `maxConcurrent`，子 agent 用其 spawning session 的预算，swarm 用 group 预算）。⇒ 调"并发"前要先分清是卡在会话串行还是卡在全局预算，改错一层永远看不到效果。
- 提升层：工作流 / 安全边界。触发词：队列溢出策略、drop summarize/old/new、合成补偿、cap 20、排队不借权限、撤销作用于在飞、会话 lane、两级并发预算、换运行时绕不过。


## Cap45 策略变更事件本身要入账；凭据过期应能原地重授权而不是重建（来源：help.make.com `credential-requests-reauthorization-2fa-enforcement-logs.md` 1,630B + `audit-logs.md` 8,460B，2026-10-03 r390C 独立 curl 取 `.md` 原文实拉；与 §Cap31 审计边界 / §Cap42 凭据归属 互补——那两条管账本证明不了什么、执行身份归谁，本条管"谁改了规则"与"凭据过期后怎么续"）
- **原文**：「Audit logs now record changes to **2FA enforcement** settings. Organization admins and owners can see: **Who enabled or disabled 2FA enforcement** / When they did it」；「Previously, expired OAuth connections required **creating and authorizing a new credential request each time**. Requesters can now ask recipients to **reauthorize OAuth connections directly from an existing credential request**」；可用性标注「Both features are available on the Enterprise plan」。
- **判据**：① **审计要记两类事件：违规事件与策略变更事件**——只记"谁没开 2FA"会漏掉更关键的一条：**谁把强制 2FA 关掉了**。改变规则比违反规则影响面更大，且通常只有极少数人有这个权限；凡是能被开关的安全策略，其开关动作必须进审计日志（谁 + 何时 + 从什么改成什么）。② **凭据过期应提供原地重授权通道**：过期即重建会不断产生新的凭据请求与连接，旧的连接面不会自动消失 ⇒ 累积出来的是一批无人清理的平行授权。续期（reauthorize）与新建（create）是两个动作，默认应走续期。③ **这类能力通常带套餐门槛**（Enterprise），写进共享规则时要连同前置面一起声明，避免"我们平台应该有"的误判。
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

## Cap56 凭据三约束：只写不读、注入的是代理值不是原文、身份键不可变（换目标=新建）（来源：docs.bigmodel.cn `cn/managed-agents/{vaults,mcp,cloud-environment}.md` 7,423B / 6,511B / 6,579B，2026-10-04 r409A 独立 curl 取 `.md` 原文实拉；与 §Cap49 凭据回写只存来源标记 / §Cap32 fail-closed 同族——前两条管"不把明文固化回配置"与"空凭据拒绝"，本条管"值根本不进进程"与"改址不等于改字段"）
- **原文**：`密钥只写不读——所有 token、secret 在任何响应中都不会回显，Agent 与沙箱也拿不到原始值`；`environment_variable 类型：以环境变量名提供给沙箱；进程中看到的是 omasec_ 代理值，真实密钥只在访问允许的目标主机时由平台代入请求`；`environment_variable 类型必须声明 networking 策略（unrestricted，或 limited + allowed_hosts，至多 16 项）`；`身份字段（mcp_server_url / host / secret_name，以及 refresh 的 token_endpoint / client_id / resource）不可变，更新时必须省略——要换目标就新建一条凭据`；`POST /v1/vaults/:vaultId/credentials/:credentialId 做部分更新：提供的 secret 被替换，省略的 secret 保留`。
- **判据**：① **进程内可见 ≠ 密钥可用**：注入的是代理值，真实值只在出站且目标主机命中凭据的 networking 规则时由平台代入 ⇒ 凭据的**作用域由网络策略界定，不是由"谁拿到了环境变量"界定**；评判暴露面要同时看值面与出网面。② **轮换是部分更新，但身份键必须省略**：省略=保留这条规则对 secret 成立、对身份键不成立（身份键要求省略是因为它不可改）⇒ **同一个"省略"字段在不同类型上语义相反**，写轮换脚本时不能一律"缺省即保留"。③ **换目标 = 新建凭据，不是改字段**：地址/宿主/名字是身份，改身份等于换对象；沿用旧凭据改 URL 的做法在该模型下不可行。④ **只写不读 ⇒ 凭据没有"回读校验"这一手段**：正确性只能靠外部探测（如 `mcp_oauth_validate` 的 valid/invalid/unknown）证明，不能靠读回来看对不对。⑤ 读取接口只回非敏感字段（`expires_at`、不含秘密值的 refresh 配置）⇒ **可见的元数据面与不可见的值面是两条清单**，不要把"能看到过期时间"当"能看到凭据"。
- 提升层：安全边界。触发词：只写不读、代理值、omasec_、出站代入、身份键不可变、换目标新建、部分更新省略即保留、凭据作用域由网络策略界定。

## Cap57 定时任务的暂停/恢复/归档三态各有独立语义：暂停不阻断手动、恢复以当下为锚重算且漏跑不补、归档是终态但历史可查（来源：docs.bigmodel.cn `cn/managed-agents/deployments.md` 6,382B，2026-10-04 r409B 独立 curl 取 `.md` 原文实拉；与 §Cap 自动化排障「not-due 是正常结果 / handler-unavailable」互补——那条管"为什么没触发"的诊断顺序，本条管"暂停恢复归档三个动作各自改变什么"）
- **原文**：`pause：停止后续定时触发；手动 run 仍允许`；`unpause：以当前时间为锚重算 schedule.upcoming_runs_at；暂停期间漏掉的触发不会补跑`；`archive：终态且幂等；归档后不再触发、不可手动 run（409），历史 run 仍可查询`；`Deployment 只保存引用，每次触发按环境当前配置固化进新会话；环境被归档或删除后，下一次触发失败`；`响应中的 agent.version 是创建时固定（pin）下来的真实版本号`；`session_id（该次运行创建的会话；刚返回时可能为 null，通常数秒后填上）`。
- **判据**：① **暂停 ≠ 停用**：手动触发在暂停期仍可用 ⇒ "这个任务停了"这句话要分清是定时面停了还是整个任务停了，用暂停当"关停"会留下手动入口。② **恢复的锚点是当下不是暂停时刻**：漏掉的运行不补跑 ⇒ 恢复后不要按"本该跑几次"核算，也不要靠 unpause 去追补历史窗口；需要补数必须自己按时间窗重放。③ **归档只读不删历史**：归档后 run 记录仍可查询 ⇒ 归档是"停止变化"不是"抹除证据"，审计/复盘窗口在归档后仍然成立。④ **引用式绑定的失败推迟到下一次触发**：Deployment 只存环境引用，环境被删除/归档不会立即报错，要等下一次触发才失败 ⇒ 变更 Environment 时必须反查哪些 Deployment 引用它（与 §引用完整性责任相反两套 同源）。⑤ **版本在触发时 pin**：run 记录里带的是本次实际使用的 Agent 版本 ⇒ 复盘必须绑定版本，否则"当时配的是 X"无法还原。⑥ **异步填充字段不能当缺失处理**：`session_id` 刚返回为 null 是常态，立刻判"没创建会话"会误报。
- 提升层：工作流。触发词：暂停不阻断手动、恢复以当下为锚、漏跑不补、归档终态历史可查、引用式绑定延迟失败、run 绑定 agent 版本、session_id 异步填充。

## Cap58 自动复核的准入是「派发链能否整体绑定」：不可绑定降级为人工而非拒绝；远程审批的等待期是身份校验盲区；超时即终态拒绝并主动通知「没跑」（来源：docs.openclaw.ai `tools/exec-approvals-advanced.md` 27,837B（Executable identity binding / auto-review / approval timeout 段），2026-10-04 r409B 独立 curl 取 `.md` 原文实拉；与 §Cap51 批准绑那一刻的二进制 / §Cap55 权威源是服务端记录 同族——那两条管"批准绑什么"与"以谁的记录为准"，本条管"什么有资格进入自动复核"与"没人批的时候结局是什么"）
- **原文**：`In mode=auto, reviewer-approved unpinned execution requires the complete dispatch chain to be identity-bound. The authorization plan must succeed, every candidate must use direct transport, and every wrapper and final executable must have a recorded executable operand.`；`Shell -c wrappers, env with assignments, xcrun, BusyBox/Toybox applets, shell builtin/command/exec dispatch, and anything else whose complete chain cannot be bound skip automatic review with "Exec auto-review skipped: dispatch chain cannot be bound".`；`Node executable-identity bindings are local to one invocation. The remote human approval plan keeps its existing direct executable pinning ... it does not carry every executable identity inside a shell wrapper across the approval wait. For those inner commands, identity revalidation starts when the approved invocation reaches the node's local policy evaluation, so it does not detect substitutions made earlier in the remote approval wait.`；`If no decision arrives before the timeout, the request is treated as an approval timeout and surfaced as a terminal host-command denial.`；`OpenClaw also resumes that session with an internal followup so the agent observes that the command did not run instead of later repairing a missing result.`；`Pending exec approvals expire after 30 minutes by default.`；`Denied async approvals use the same main-session followup path for the denial status, but they do not register elevated runtime handoffs and they do not run the command.`
- **判据**：① **自动/人工的分界线是"可绑定性"不是风险高低**：能钉住整条派发链才配进自动复核，钉不住的一律转人工 ⇒ "为什么这条命令要人点"的答案常常是结构性的（包装层不可绑定），不是因为它更危险。② **钉不住 ≠ 拒绝**：不可绑定是**降级到人工**，而既存硬拒绝（`-i`/`--interactive`/`-ic`）**优先于降级**，保持拒绝而不是转成人工请求 ⇒ 同一族形态里"降级"与"拒绝"会同时存在，判定顺序必须是"先查既存拒绝，再谈降级"。③ **远程审批的等待期是校验盲区**：内层命令的身份在节点本地策略求值时才重新校验，等待期内发生的替换检测不到 ⇒ 把"批了"当作"整条链都安全"是错误的，长等待审批后的执行应重新确认。④ **绑定只在内存存续于审批生命周期，无持久化变更** ⇒ 重启/换会话后绑定不保留，不能指望"上次批过所以这次还绑着"。⑤ **超时是终态拒绝不是悬空**：无人决定时系统给出的是 denial，不是"继续等" ⇒ 监控要把 timeout 归入拒绝类而不是挂起类。⑥ **系统会主动补一条"没跑"的通知**：让 agent 立刻知道命令没执行，而不是事后再发现结果缺失 ⇒ 反过来要求：收到审批相关 followup 时必须区分"批准并执行了"与"拒绝了/超时了"，两者走同一条投递路径但语义相反。
- 提升层：安全边界 / 工作流。触发词：dispatch chain cannot be bound、auto-review 跳过转人工、既存拒绝优先于降级、远程审批等待期盲区、绑定仅内存存续、审批超时即终态拒绝、followup 告知没跑、收到了消息不等于跑了。

## Cap59 共享记忆的写入要有乐观锁与主体归因；删除不抹历史版本，脱敏只对非 head 版本可行（来源：docs.bigmodel.cn `cn/managed-agents/memory-stores.md` 7,572B，2026-10-04 r409C 独立 curl 取 `.md` 原文实拉；与 §Cap 凭据只写不读 / §脱敏≠已删除 互补——那两条管"值不回显"与"正文脱敏不等于数据消失"，本条管"多主体写同一份记忆时怎么不互相覆盖"与"涉密内容到底怎么真正抹掉"）
- **原文**：`更新 path 和/或 content。可带 precondition：内容已被改过则更新失败，避免覆盖他人刚写的内容`；`删除 Memory；可带 expected_content_sha256，当前内容已变化时拒绝删除`；`更新前先读取当前 content_sha256，再把它作为条件提交`；`每次创建、修改、删除都会产生一条不可变的版本记录，标注操作类型（created / modified / deleted）与执行主体（session_actor 会话内 Agent，含 session_id；或 user_actor API 调用者）`；`如果某个版本包含不应留存的敏感内容……用脱敏接口抹除该版本的内容与路径，保留审计轨迹`；`脱敏后该版本的 path / content / content_sha256 变为 null，redacted_at 与 redacted_by 记录操作时间与主体`；`不能对当前 head 版本脱敏，会返回 409；先改内容或删除条目，再对历史版本执行 redact`；`删除条目不会抹掉历史版本里的内容`。
- **判据**：① **共享记忆必须走乐观锁**：多 agent/多会话写同一份记忆时，"读—改—写"之间必须带内容哈希做前置条件，否则后写静默覆盖先写；正确姿势是**先读哈希、再带条件提交**，不是"写完再看对不对"。② **删除也要带条件**：`expected_content_sha256` 让"我删的是我以为的那版"成为可验证命题，防止删掉别人刚更新的内容。③ **写入主体必须二分归因**：`session_actor`（agent，带 session_id）与 `user_actor`（人，经 API）⇒ 同一份记忆里"这条是谁写的"是可查的，做记忆治理/回溯时不能把 agent 沉淀与人工修正混为一谈。④ **删除 ≠ 抹除**：删除条目只影响当前视图，历史版本里的内容仍在 ⇒ 涉密数据的回收必须落到**版本级 redact**，只删条目会留下完整副本。⑤ **脱敏受版本位置约束**：head 版本不可脱敏（409），须先改内容或删除条目、让目标版本退为非 head，再 redact ⇒ "先改后抹"是固定两步顺序，直接对最新版脱敏会失败。⑥ **脱敏保留审计轨迹**：path/content/hash 变 null 但 `redacted_at`/`redacted_by` 留存 ⇒ 抹除动作本身留证，符合"能说清谁在什么时候抹了什么"。
- 提升层：安全边界 / 工作流。触发词：记忆乐观锁、precondition、expected_content_sha256、先读哈希再提交、session_actor/user_actor 二分、删除不抹历史版本、head 版本不可脱敏、先改后抹、redact 保留审计轨迹。

## Cap60 中断不是错误、也不产生错误事件；等待态只接受"回应"不接受新指令，且中断会取消整组等待（来源：docs.bigmodel.cn `cn/managed-agents/faq.md` 7,447B + `events.md` 15,944B，2026-10-04 r409C 独立 curl 取 `.md` 原文实拉；与 §Cap35 改向与中止是两个意图 / §Cap55 权威源是服务端记录 互补——那两条管"改向≠中止"与"以谁的记录为准"，本条管"中断在事件面上长什么样"与"等待态接受什么输入"）
- **原文**：`发送 user.interrupt 后，平台会主动停止当前模型响应，并向运行中的命令发出停止信号；命令在宽限期内（当前约 3 秒）没有结束会被强制终止，本轮必然停下`；`中断不会产生 session.error`；`interrupt 之前尚未处理的消息会被跳过，之后提交的 user.message 会在下一轮执行`；`若停在 requires_action，interrupt 会取消整组等待中的工具调用和审批`；`停在 requires_action：在等你处理 event_ids 里列出的调用……此时发 user.message 会被拒绝（400）`；`更新 Agent 返回 409……服务器上当前版本已经变了——通常是别人（或另一次请求）刚更新过。先 GET 最新 Agent，用返回的 version 再更新；CI 这类声明式同步可以省略 version，后写覆盖`。
- **判据**：① **主动中断与失败是两条通道**：中断不产生 `session.error` ⇒ 监控不要用"有没有错误事件"判断"是不是出了问题"，被中断的轮次在错误面上完全干净，要另设中断计数。② **中断有宽限期且必然停**：命令先收到停止信号、宽限期内不退出才强杀 ⇒ "发了 interrupt 却还在跑"看的是宽限期，不是中断失效。③ **等待态的输入类型是受限的**：`requires_action` 下只能回 `user.custom_tool_result` / `user.tool_confirmation`，发新 `user.message` 直接 400 ⇒ 等待态不是"可以顺便追加要求"的时机，想把新指令带进去必须等本轮结束或先取消。④ **中断是整组取消**：对等待中的一整组工具调用与审批一次性取消 ⇒ 部分响应没有意义，恢复后要按"整批重来"处理，不能假设其中某几条已经生效。⑤ **中断会吞掉未处理的排队消息**：中断前入队但还没处理的消息被跳过 ⇒ 重要指令不要在 interrupt 前后脚发送，否则静默丢失。⑥ **版本冲突的两种正确解法按场景分**：交互式先 GET 再带 version；CI 声明式同步**省略 version 让后写覆盖**——把交互式做法搬进 CI 会造成无谓的冲突失败，反之则会互相覆盖。
- 提升层：工作流 / 安全边界。触发词：中断不产生 error、宽限期强杀、等待态拒绝新指令、中断取消整组、中断吞掉排队消息、声明式同步省略 version、409 版本冲突先 GET。

## Cap61 权限策略的作用域止于「平台自己执行的那一半」：客户端侧执行的自定义工具整个在策略管辖之外（来源：docs.bigmodel.cn `cn/managed-agents/{agent-setup,overview,examples,api-reference}.md` 5,777B / 6,670B / 4,124B / 14,376B，2026-10-04 r410A 独立 curl 取 `.md` 原文实拉；与 §Cap37 HITL 挂工具级 / §Cap51 审批不是权限边界 / §Cap56 凭据只写不读 互补——那几条管"拦截点挂哪一层""审批覆盖什么""密钥怎么存"，本条管"托管平台的权限承诺到底覆盖哪些工具"）
- **原文**：`权限策略不作用于自定义工具。收到 agent.custom_tool_use 后，由你的应用决定是否执行，需要时先在 UI 里让用户确认`；`自定义工具：由你的客户端执行的工具，Agent 发起调用、你的应用返回结果`；`工具边界：启用哪些内置工具、连接哪些 MCP、是否要求 always_ask 人工审批`；`Managed Agents 将这些能力纳入平台……短问答、低延迟对话，或不依赖沙箱与长任务状态时，直接调用模型 API 更合适`。
- **判据**：① **托管平台的权限策略只覆盖它自己执行那一半**——内置工具在沙箱内由平台执行故受 `permission_policy` 管辖；**custom 工具的执行体是调用方自己的应用**，平台只发出调用事件，策略面到此为止 ⇒ 把"我配了权限策略"当成"这个 Agent 的所有工具调用都受控"，等于把客户端侧那一半漏在外面。② **"工具边界"这条配置面的作用域要显式写清它不覆盖什么**：文档把工具边界列为调用方自决项，同时明说策略不作用于自定义工具 ⇒ 声明能力边界时，光列"管什么"会让人默认"剩下的也管了"。③ **客户端执行的工具，人工确认必须在客户端实现**——平台给的落点是"收到事件后由你的应用决定、需要时在 UI 里确认" ⇒ 这是 HITL 落点的分派：平台侧执行 → 平台侧批；客户端侧执行 → 客户端侧批，两端都要有，不能互相替代。④ **能力托管的边界同时是选型边界**：平台明确"不依赖沙箱与长任务状态时应直接调模型 API" ⇒ 托管带来的是循环/上下文/沙箱/密钥/落库/跨会话状态/用量七项，代价是把执行位置交给平台；只有托管方与自管方的**责任分界线**清楚了，这七项才是收益而不是黑箱。
- 提升层：安全边界 / 工作流。触发词：权限策略不作用于自定义工具、custom_tool_use、客户端执行、工具边界作用域、平台侧批 vs 客户端侧批、能力托管七项。

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

## Cap66 昂贵召回路径必须由「意图匹配 + 廉价通道无强命中」双条件共同放行；检索方式的能力边界要写死（来源：docs.openclaw.ai `concepts/active-memory.md` 7,276B + `concepts/active-memory/how-it-works.md` 6,173B，2026-10-04 r412B 独立 curl 取 `.md` 原文实拉；与 §Cap64 会重置的通道 / §Cap32 只写不可读 互补——那两条管"数放哪条通道"与"存储形态"，本条管"什么时候值得为一次召回付出阻塞代价"）
- **原文**："The default `escalate` mode runs its blocking recall sub-agent **only when the message asks about the past and the deterministic memory lane found no strong trusted trigger match**"；表格 `escalate` | "Default. Run only for recall intent when lane 1 has no strong hit." / `always` | "Preserve the previous behavior and run on every eligible targeted turn."；"Flat retrieval is strongest for **direct fact matches** and **weaker on temporal and multi-session questions**."
- **判据**：① **升级条件要两条同时成立**：意图匹配（这轮确实在问过去）**且**廉价确定性通道没有强命中 ⇒ 只拿"廉价失败"当条件，会把冷启动、无关问题、以及本来就不该深挖的轮次全部拖进阻塞式子调用，成本由所有轮次平摊而收益只落在少数轮次上。② **检索层必须声明自己的能力边界**：扁平/向量检索强于直接事实匹配、弱于时序与跨会话问题（有 LongMemEval / PrefEval 这类基准量化该差距）⇒ 不写边界的检索层，用户感知到的"想不起来"会被误判成"根本没存过"，于是重复沉淀已有信息。③ **改默认不许删掉旧行为**：`escalate` 作默认、`always` 保留旧路径 ⇒ 分层优化要给一条显式逃生口，否则"优化"对依赖旧行为的场景就是静默破坏。
- 提升层：工作流 / 记忆检索。触发词：深召回升级、阻塞式召回、廉价通道先跑、意图匹配才升级、检索能力边界、时序与跨会话弱项、escalate 与 always、保留旧行为。


## Cap67 工具清单是「限流」不是「授权」：配置里列出工具名不产生授权，授权面由父 agent 的有效工具策略决定（来源：docs.openclaw.ai `concepts/active-memory/memory-tools.md` 5,831B，2026-10-04 r413A 独立 curl 取 `.md` 原文实拉；与 §Cap63 信任不跨层传递 / §Cap66 昂贵召回双条件放行 互补——那两条管"凭据由谁签发""什么时候值得召回"，本条管"召回工具配上了到底算不算被允许用"）
- **原文**：「`toolsAllow` is a **limit, not a permission grant**. Before starting recall, Active Memory filters these names through the parent agent's **finalized tool policy**.」「`allow` and `alsoAllow` **cannot be combined** in the same scope.」「A later allowlist **cannot restore** tools excluded by a profile.」「These grants also give the **parent agent** access to the named tools; they are not recall-only permissions.」「A tool listed there is **registered**, but that output does not prove the parent agent or Active Memory is **authorized** to call it.」「wildcards, `group:*` entries, and core agent tools … are **silently filtered out**」
- **判据**：① **白名单是上限不是许可**——`toolsAllow` 只回答"最多用这几个"，不回答"可以用这几个"；真正生效的是它与父级工具策略的**交集**，交集为空时该能力静默缺席（`status=policy-disabled`），症状是"明明配了却没召回"。⇒ 凡"在某处列出能力名"的配置，都要追问它在哪一层被过滤，"列了"不等于"批了"。② **注册可信 ≠ 授权可信**——`plugins inspect` 能证明工具已注册，不能证明调用方被授权；排查"配了不生效"时这两件事必须分开取证，否则会把授权问题误修成注册问题。③ **放宽与收紧不是对称操作**——`alsoAllow` 只能在 profile 之外**加**，不能覆盖显式 deny / provider / agent / sandbox 限制，也不能救回被 profile 排除的工具；且 `allow` 与 `alsoAllow` 同域互斥。⇒ 收紧是减法、放宽只有加法这一个方向，**被减掉的东西没有对等补回路径**，配之前要想清楚哪一层在减。④ **为了子能力开的授权会同时抬高父 agent 的能力面**——给召回子 agent 开的 `alsoAllow` 同时把该工具交给父 agent，授权不是"仅这次用"，开给局部的口子是全域的。⑤ **非法条目应拒绝启动而非静默放宽**（与 sa 3.124.0 同族判据在此面复现）：只收精确工具名，通配/组/核心工具被静默过滤 ⇒ 静默过滤让"配错了"表现成"没配"。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：白名单是限流不是授权、toolsAllow、alsoAllow 与 allow 互斥、profile 排除不可恢复、注册不等于授权、policy-disabled。


## Cap68 写同一条记录不等于推进它的生命周期：维护类写入必须声明自己算不算「交互」（来源：docs.openclaw.ai `automation/cron-jobs/troubleshooting.md` 4,654B，2026-10-04 r413C 独立 curl 取 `.md` 原文实拉；与 §Cap57 定时任务三态 / §Cap60 中断不是错误 互补——那两条管"暂停恢复归档各自改变什么""中断在事件面上长什么样"，本条管"哪些写入有资格推进新鲜度"）
- **原文**：「Daily and idle reset freshness is **not based on `updatedAt`**」「Automation wakeups, heartbeat runs, exec notifications, and gateway bookkeeping **may update the session row for routing/status, but they do not extend `sessionStartedAt` or `lastInteractionAt`**」「For legacy rows created before those fields existed, OpenClaw can recover `sessionStartedAt` from the transcript JSONL session header when the file is still available. Legacy idle rows without `lastInteractionAt` use that recovered start time as their idle baseline.」
- **判据**：① **"行被写过"与"生命周期被推进"是两件事**——心跳、唤醒、通知、系统记账都会改同一行（路由/状态），但刻意不延长新鲜度字段；若把新鲜度定义成 `updatedAt`，一个后台心跳就能让会话永不过期。⇒ 任何"多久没动就归档/重置"的规则，必须显式列出**哪些写入算交互、哪些不算**；用"最后修改时间"当新鲜度等于把续命权交给噪音。② **同一个对象上要有两套时间语义并各自命名**：路由态的时间（什么时候被系统碰过）与交互态的时间（什么时候人/主体真的说了话）。混用后排查"为什么没过期"只能靠猜。③ **字段缺失时的回退基准要写清楚且优先从原始记录恢复**——旧行没有这两个字段时从 transcript 头恢复 `sessionStartedAt`，无 `lastInteractionAt` 的旧行用它当 idle 基线；⇒ 补字段的迁移不能默认"缺失 = 现在"或"缺失 = 永不过期"，两者都会成批改变既有对象的命运，必须给出可核验的恢复来源。④ 对 guild 的落点：共享记忆/交接/收件箱的 groom 与归档规则同理——后台 groom 自己写的时间戳不能算"这条还有人在用"；存活判定要挂在明确的交互字段上。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：写入不推进生命周期、updatedAt 不是新鲜度、sessionStartedAt、lastInteractionAt、心跳不算交互、groom 存活判定字段。
## Cap69 自动化任务默认「启用+监督」，禁用等审批是更糟的失败（来源：docs.openclaw.ai/automation/cron-jobs/how-it-works.md，2026-10-04 r415 独立 curl 实拉）
- **原文**：job created **enabled, not disabled-pending-approval**；scheduler supervises enabled jobs: a failing one raises a failure notification and is **auto-disabled after repeated errors**, with the reason recorded and the owner notified；nothing supervises a disabled job；a job left disabled waiting for a confirmation that never arrives is **invisible to every guard, hidden from the default list, and will never fire or explain itself** — a silent non-outcome, which is a worse failure than a job that runs and visibly complains.
- **判据**：① 自动化任务默认**启用+受监督**（失败即告警 + 重复失败自动禁用）优于**禁用等审批**——被禁用的任务对守卫不可见、不在默认列表、永不触发、永不解释自己，是「静默非结果」，比「运行并可见地抱怨」更糟；② 调度器必须拥有失败记账与可见性，任务「是否健康」应由监督信号决定，而非由「有没有被人工批准启用」决定；③ 落地动作：新任务走「启用+监督+自动禁用」而非「禁用等确认」，把「会不会响」交给重复失败计数而非人工点击。
- 提升层：工作流 / 可靠性。触发词：默认启用、受监督、自动禁用、禁用等审批、静默非结果、可见失败优于静默。

## Cap70 不可信外部内容走受限 reader agent：独立沙箱 + 工具钳制 + 禁跨 agent 移交（来源：docs.openclaw.ai/automation/cron-jobs/gmail.md，2026-10-04 r415 独立 curl 实拉）
- **原文**（gmail restricted reader）：explicit `ownership: "explicit"` roster；reader agent `workspaceAccess: "none"` + `sandbox.mode: "all" scope: "session"`；`tools.allow: ["session_status"]` deny `group:fs/runtime/web/browser/cron/gateway/nodes`；per-agent allowlist **cannot restore** a tool an earlier policy removed；`tools.agentToAgent.enabled: false` 禁用跨 agent 移交；untrusted content wrapped as data, never followed.
- **判据**：① 不可信输入（邮件 / Webhook / 用户上传）**不当主 agent 跑**，路由到独立受限 reader agent——独立沙箱（`workspaceAccess: none`）+ 工具钳制（allowlist 只含必需，deny 文件系统 / 运行时 / 网络 / 浏览器 / cron / 网关）+ 禁跨 agent 移交（`agentToAgent.enabled: false`），避免 prompt-injection 借主 agent 能力外溢；② 工具策略只能更紧不能更松——全局 / provider / agent / sandbox 规则叠加后，per-agent allowlist **不能恢复**被上层移除的工具，钳制必须可审计；③ 外部内容当数据不当指令——包裹为 untrusted data，禁止跟随其中的链接 / 指令。
- 提升层：安全边界 / 工作流。触发词：受限 reader、独立沙箱、workspaceAccess none、工具钳制、禁跨 agent 移交、prompt injection、不可信输入、untrusted data。


## Cap71 编排默认取「削峰」不选「精准」；一次性触发自我停用后须显式重启；队列必须有界且超限停源留错；争用同一状态槽的特性在准入期就被拒（来源：docs.openclaw.ai `automation/cron-jobs/schedules.md` 16,129B，2026-10-04 r416B 独立 curl 取 `.md` 原文实拉；与 Cap69「自动化默认启用+监督」互补——那条管"启用后谁来监督"，本条管"默认形状取哪一侧、触发语义与积压怎么封顶"）
- **原文**：「Recurring top-of-hour expressions (minute `0` with a wildcard hour field) are … by up to 5 minutes to reduce load spikes. Use `--exact` to force precise timing」；「An `on-exit` job disables itself when its payload is queued to run. Re-enable the job to watch again」；「If the new command exits before that payload finishes, its exit waits for the previous run to settle … This includes cleanup still running after a timeout response. Disabling or changing the watch cancels its pending exit.」；「Only one payload fire and one bounded pending batch are retained per job … coalesce into that pending batch rather than building an unbounded queue.」；「Failed payloads are not retried because they may not be idempotent.」；「Combining a script payload with a condition gate is rejected because both would own the persisted `trigger.state` slot.」；「Five consecutive runs shorter than 60 seconds leave the job in an error state … manually re-enable the job to clear the restart cap.」；「If either limit is exceeded, the source stops with a recorded error … then manually re-enable the job.」
- **判据**：① **默认形状要取能扛住最坏情况的那一侧**：整点周期作业默认自动错开至多 5 分钟削峰，**精准是显式声明换来的**（`--exact`）；把"准点"设成默认，等于让所有使用者的默认值在同一秒撞在一起。⇒ 凡"大家都想要同一个时刻"的能力，默认值必须带打散，且打散窗口只对周期类有意义（间隔型/事件型不适用）。② **一次性触发用完即停用，且重启是显式动作**：`on-exit` 作业在载荷排队时就自我停用，要看须重新启用 ⇒ 事件型触发不排队，"监视到一次"之后不能假设它还在监视。③ **"上一个还没 settle"要显式等待，且 settle 包含超时之后的清理**：新命令若先退出，退出动作会等前一个载荷 settle（含超时响应后仍在跑的清理）才停用作业并起下一个 ⇒ 只看"响应已返回"会漏掉仍在跑的收尾。④ **积压必须有界，超限停源并留错**：只保留一个在跑的载荷 + 一个有界待批，其余合流；匹配预算或队列超限则**源直接停止并记录错误**，须手动重启 ⇒ 无限队列把"处理不过来"伪装成"稍后会处理"，有界 + 停源才让背压可见。⑤ **不幂等的失败不重试**：失败载荷刻意不重试（"may not be idempotent"）⇒ 重试资格由副作用性质决定，不是由"失败了该不该再试"决定。⑥ **两个特性争用同一状态槽时在准入期就拒**：script payload 与 condition gate 都要独占 `trigger.state`，组合直接被拒 ⇒ 冲突不要在运行时表现为"互相覆盖"，要在装配时拒绝。⑦ **快速失败循环要有封顶并转为人工**：连续 5 次短于 60 秒进入错误态、须手动重新启用 ⇒ 自动重启 + 无上限 = 把崩溃变成高频噪声。
- 提升层：工作流 / 工具。触发词：默认打散、削峰默认开、精准须显式、on-exit 自我停用、有界队列、超限停源、不幂等不重试、状态槽争用准入期拒绝、快速失败封顶须手动清、settle 含超时后清理。


## Cap72 分层作用域只允许「收窄」不允许「放大」：下级的权限是上级授予集合的子集，把"能管理"与"能扩张"分开（来源：www.activepieces.com/docs `admin-guide/guides/manage-pieces.md` 4,552B，2026-10-04 r416C 独立 curl 取 `.md` 原文实拉；与 Cap67「工具清单是限流不是授权」/ Cap65「撤销≠禁止」互补——那两条管"清单与授权是两件事""撤销与禁止是两件事"，本条管"多级作用域叠加时，下级能不能给自己加东西"）
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
