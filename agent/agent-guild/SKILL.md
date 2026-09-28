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
version: 1.17.0
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

## Quick start (for an agent that has NOT joined yet)

1. Run the onboarding flow: `~/.agent-guild/ONBOARDING.md` (or this skill's
   `docs/ONBOARDING.md`) — discover your runtime's user-extensible skills dir,
   install this skill (symlink → copy → readonly), run the closed-loop trigger
   test, register yourself in `registry.json`.
2. Then come back here — this file is your everyday capability.

## Mandatory Session Contract (once per session, MUST)

> ⛔ 这些是**强制动作**，不是建议。每次会话开始（或首次需要用户上下文时）执行，不要等用户点名。
> 全部通过 `ag` 一条命令完成，别手工开五个文件。
>
> **No shell / no Python?** Every step below has a plain-file equivalent — read
> the listed files directly and Edit them in place. The contract still applies;
> only the mechanism changes. On Windows, use `python` if `python3` is not on PATH.

### M0 — Ensure the guild exists (first use / every session start)

```bash
python3 <SKILL_DIR>/scripts/ag.py init <your-agent-name>
```

幂等：目录不存在则建全套骨架 + 落地本 skill；已存在则只补缺失项，**绝不覆盖已有数据**。
输出 `initialized` = 首次自举，`verified` = 已存在。

### M1 — Bootstrap: read shared context BEFORE real work

```bash
python3 <SKILL_DIR>/scripts/ag.py bootstrap <your-agent-name>
```

**轻量优先（默认不全量读）**：Session 开始只加载**最小必要上下文**——
`identity/profile.md`（用户是谁）+ `rules/universal.md`（戒律）+ 与当前任务直接相关的那一份。
其余（`ROUTINE.md` 日程 / `projects/active.md` 项目 / `current-focus.md` 各 agent 焦点 / 未读收件箱）
**按需读取**：任务提到才读，不预判全读。

**只有以下场景才执行完整 bootstrap**（一次读全）：
跨 Agent 协作任务 · 长任务 · 需要长期记忆/上下文连续 · 任务交接 · 用户明确要求读取完整上下文。

读到什么就按什么做。之后按需再读 `toolchain/*.md`、其他 `rules/*.md`。

### M2 — Write memory after substantive work

完成**实质工作**后 MUST 追加 daily log（见 Capability 4）。满足任一即"实质工作"：
产出交付物（代码/文档/报告/网站/脚本）・改了代码或配置・做了技术决策・修复错误并定位根因・学到可复用的长期事实（用户偏好/项目约定/坑）。

**跳过**：寒暄、简单查询、短问答、纯检索。

跨 agent 有价值的事实 → 也写 `memory/shared/`；只对你自己有意义的 → 留在 `memory/<你的名字>/`。

**踩坑/被纠正/发现更好做法 → 同时记学习台账**（Capability 8，`ag learn`）。
用户纠正了你・命令非预期失败・用户想要不存在的能力・发现某任务更优解 ——
这些是全 guild 的免疫素材，别只留在当天日志里。**绝不记录 secrets/原始报文**，摘录要脱敏。

### M3 — Route skills & data into the guild (default-on)

- **装新 skill**：MUST 装到 `~/.agent-guild/skills/<name>/`，再从那里软链回自己 runtime（symlink → copy → readonly 降级，见 ONBOARDING.md Step 3）。
- **写持久化数据**：MUST 写 `~/.agent-guild/skills_data/<skill>/`（敏感数据拆 `private/`）。
- **MCP / 插件 / CLI 工具**：分别进 `mcp/`、`plugins/`、`tools/`。
- **唯一豁免**：你的 runtime 强制私有路径（如 platform-managed）——在 registry 里记录原因即可，不算违反。

### M4 — Self-audit: adopt what's still scattered (first join + monthly)

```bash
python3 <SKILL_DIR>/scripts/ag.py adopt <your-agent-name>            # DRY-RUN, 只报告
python3 <SKILL_DIR>/scripts/ag.py adopt <your-agent-name> --apply    # 真的搬 + 软链回来
```

扫五类资产：`skills` / `skills_data` / `mcp` / `tools` / `memory`。
**默认 dry-run**，先把清单给用户看；`--apply` 才动手（搬完自动验证软链，失败自动回滚，删除走废纸篓）。

自动排除：可重建缓存（`.venv`/`node_modules`/`__pycache__`）、凭证、runtime 内部元数据、平台托管包（`__skillhub`/`connector-*`）、connector 型 skill。

健康检查（发现悬空软链 / 旧路径残留 / registry 漂移）：

```bash
python3 <SKILL_DIR>/scripts/ag.py doctor
```

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

## Capability 1 — Read shared user context

| File | Purpose |
|---|---|
| `~/.agent-guild/identity/profile.md` | Who the user is |
| `~/.agent-guild/identity/ROUTINE.md` | Daily schedule / routines |
| `~/.agent-guild/rules/universal.md` | **Mandatory commandments** — highest priority |
| `~/.agent-guild/rules/public-repo.md` | Public-repo hard rules |
| `~/.agent-guild/rules/file-cleanup.md` | File deletion preferences |
| `~/.agent-guild/rules/safety.md` | Safety guardrails |
| `~/.agent-guild/projects/active.md` | What the user is working on |
| `~/.agent-guild/handoff/shared-state/current-focus.md` | What any agent is focused on now |
| `~/.agent-guild/toolchain/*.md` | Tool-specific config — read on demand |

Read on demand; don't slurp everything every turn.

## Capability 2 — Update current-focus

`current-focus.md` is the "what's hot right now" board. When you start or
finish a major task, prepend your block (`ag focus` or manual Edit in place).
Never rewrite history other agents wrote.

## Capability 3 — Check inbox / send messages

Inbox: `~/.agent-guild/handoff/inbox/`.
- Receive: `ls ~/.agent-guild/handoff/inbox/ | grep "to-<your-agent-name>-"`, read, act, then `mv` to `handoff/archive/`.
- Send: `from-<src>-to-<dst>-<topic>.md` — write for a recipient with no context (what you did, what's left, where artifacts are).

## Capability 4 — Daily log

After **substantive work** (built/fixed/decided/learned a lasting fact), append to `~/.agent-guild/log/daily/YYYY-MM-DD-<your-agent-name>.md` — per-agent file, append-only. **Skip** greetings / lookups / short Q&A.

Good entry: `## <title>` + What / Why / Result / Cross-agent note (if others need to know).

## Capability 5 — Refresh last_seen

Once per session, update your entry's `last_seen` (prefer `ag last-seen`, fallback Edit). Never overwrite the whole registry — patch only your entry.

## Capability 6 — Where to persist shared data

New skill / MCP / plugin / tool / persistent data you install → **MUST** go under `~/.agent-guild/{skills,skills_data,mcp,plugins,tools}/<name>/`, not a private path (唯一豁免见 M3). The user backs up the whole `~/.agent-guild/` with one command.

## Capability 7 — Cross-agent memory

| Path | What goes there |
|---|---|
| `~/.agent-guild/memory/<agent>/` | 该 agent 的私有记忆文件（`ag adopt` 搬进来后软链回原位，runtime 照常读写） |
| `~/.agent-guild/memory/shared/` | 跨 agent 都该知道的事实（用户偏好、项目约定、踩过的坑） |

写之前先读：别把别人已经记过的东西重复记一遍。

## Capability 8 — Learning ledger (self-improvement loop)

三本跨 agent 台账在 `~/.agent-guild/learnings/`：`LEARNINGS.md`（纠正/知识盲区/最佳实践）·
`ERRORS.md`（命令/集成失败）· `FEATURE_REQUESTS.md`（用户想要但不存在的能力）。
完整规范（schema/触发词/晋升阈值/萃取流程）：`docs/LEARNINGS.md`（权威）。

**触发速查**：

| 情况 | 动作 |
|---|---|
| 命令失败/异常/超时 | `ag learn <agent> error "<summary>"` |
| 用户纠正你（"不对"/"其实是"/"you're wrong"） | `ag learn <agent> learning "<summary>"`（category correction） |
| 你的知识过时 / API 行为和认知不符 | 同上（knowledge_gap） |
| 发现更好做法 | 同上（best_practice） |
| 用户想要不存在的能力 | `ag learn <agent> featreq "<summary>"` |

**复发追踪**：相同 `Pattern-Key` 的条目跨 agent 计数；`ag review` 报告达到阈值的组。

**晋升**（达到阈值后 MUST，详见 docs/LEARNINGS.md）：
行为/偏好 → `rules/<topic>.md`；工具坑 → `toolchain/<tool>.md` 或 `memory/shared/`；
通用可复用解法 → 萃取为 skill 放 `skills/<name>/`（共享 skill bus，全 agent 即刻可用），
条目状态改 `promoted` / `promoted_to_skill`。

**红线**：不记 secrets/token/原始报文；条目只增不改，仅 `Status`/`Resolution` 可由任何 agent 更新。

## Capability 9 — Data hygiene (`ag groom`, protocol 3.2+)

协会用得越久，数据越容易劣化：current-focus 只增不减、daily log 无限堆积、
audit 越滚越大、resolved 台账条目永远躺在 live 文件里。groom 是自动防线：

- **自动触发**：`ag bootstrap` 尾部挂钩（速率限制默认 24h 一次），skill 正常
  触发即自动维护，无需用户点名。
- **保真原则**：只搬不删 —— 过期数据进 `log/archive/`、
  `handoff/shared-state/archive/`、`learnings/archive/` 或可恢复的 `.trash/`；
  手写的、无时间戳的 focus 块永远不动；未读收件箱永远只报告不搬。
- **策略可调**：所有阈值在 `~/.agent-guild/RETENTION.md`（用户文件，升级不覆盖）。
- **可审计**：每次 groom 写 `log/audit.jsonl` + `.groom.json` 状态。

## Capability 10 — 记忆分仓与路标式索引：私有仓 vs 组织共享仓（来源：Letta 官方 `docs.letta.com/concepts/memfs` + `/concepts/shared-memory` + `/configuration/memory` + LangChain 官方 `docs.langchain.com/oss/deepagents/code/memory-and-skills`，2026-09-23 r145-A 独立实拉首读，此前未读）

- **两个仓，别混成一个**：**私有记忆仓**（单 agent 所有，存身份/人格/自有技能/长期记忆，git 版控，随 agent 迁移）vs **组织共享仓**（多 agent 共享，存团队约定/产品知识/研究/计划/文档）。判据：**这份知识换一个 agent 还成不成立**——成立才进共享仓，只对本 agent 成立的留私有仓。官方把"给多个 agent 挂同一块 in-context 记忆块"判为 legacy，明令迁到共享仓。与 §Capability 7 分工：那条管"目录在哪"，本条管"**分几个仓、按什么判据分**"。
- **共享仓也能发技能**：共享仓根下 `skills/<name>/SKILL.md` 会被所有挂载它的 agent 读到；摘掉挂载即刻失效。判据：**想让全协会都用上的能力 → 放共享仓的技能目录**，不要给每个 agent 各拷一份（与 §M3 装新 skill 分工：那条管"装到哪个目录"，本条管"**一份供多个 agent 时放哪**"）。
- **同步是 agent 自己的事**：共享仓要 agent 自己 commit + push，其他 agent 才 pull 得到；首次挂载才 clone，之后只 fast-forward。判据：**写了不 push 等于没共享**。
- **记忆整理走 git worktree 并发**：后台记忆子代理在独立 worktree 里改记忆，不占主 agent 的检出、不阻塞主线。判据：**整理记忆这种后台活，别在主工作树上做**（与 §Capability 9 groom 分工：那条管"数据过期怎么归档"，本条管"**归档动作本身在哪个工作树里跑**"）。

## Capability 11 — 记忆库的固定文件分工：按"是不是基础事实 + 变多快"分文件，不是按时间堆（来源：Cline 官方 `docs.cline.bot/best-practices/memory-bank`，2026-09-23 r145-C 独立重拉首读，新信源首读，此前未读）

- **六文件固定分工，各管一类**：`projectbrief`（基础盘：核心需求与目标，是范围的事实源）· `productContext`（为什么存在、解决什么问题）· `activeContext`（当前焦点/最近改动/下一步，**改动最频繁**）· `systemPatterns`（架构与技术决策）· `techContext`（技术栈、约束、依赖）· `progress`（什么能用了、还剩什么、已知问题）。判据：**新事实进来先问"它属于哪一类、会不会经常变"**——高频的单独成文件，别和长期事实混在一起天天重写。与 §Capability 4 daily log 分工：日志**按时间追加**，记忆库**按类别重写**，两者不是一回事，别互相替代。
- **更新频率按文件定，不是统一**：官方写明 `activeContext` 每次会话后更新、`progress` 在里程碑时更新。判据：**给每个记忆文件定一个"什么时候必须改"的触发条件**，没有触发条件的文件会悄悄过期。
- **"全量复审"是一次独立动作**：官方要求收到"update memory bank"时 **MUST review ALL files**，不是只补新增的那条。判据：**增量补写会留下前后矛盾**——记忆库要定期整读一遍做一致性校准（与 §Capability 9 groom 分工：那条管"过期数据归档"，本条管"**还活着的文件之间是否自相矛盾**"）。
- **放在项目里才能跟着项目走**：官方建议把这套 instructions 存进项目级规则文件（`.clinerules/memory-bank.md`）而不是只放全局——**跨 agent / 跨机器共享的是这份文件，不是某次会话**。

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

## Agent 自主权分三档：只读免审，gated 需审，Auto≠沙箱（来源：LangChain Deep Agents Code approval-modes，2026-09-23 r150-B 独立实拉首读，清单外新信源）

- **把动作分成"只读"和"gated"两类**：`ls/read/glob/grep` 等只读工具永远免审直接跑；写/删文件、跑 shell、发 web 请求、委派子代理属 gated，需审批。判据：给 agent 自主权先分清楚"看"和"改/外发"，不要一锅烩。
- **三档模式**：Manual（每次 gated 都问）、Auto（常规动作自动过、不确定的交给模型审、反复拒绝/分类失败再退回人）、YOLO（完全不审，需一次性风险确认）。
- **Auto 是授权启发式，不是沙箱**：文档明说 Auto 不提供 OS 边界、不保证生成动作安全。把"自动批准"当成"安全"是误区。
- **Auto 的判定流**：常规动作直过 → 不确定的由活动模型按用户请求审效果 → 高风险的（如把本地内容发往未配置目的地）仍要显式授权；反复拒绝/分类失败就停、转回人审。
- **越权前先复核状态**：决策绑定线程/模式/批次/具体调用；切到 Manual 或状态竞态/重放时，回退到人审，不让旧 Auto 决定静默执行。
- 与 §记忆与技能分层 / §目标驱动 的分工：那条管身份与上下文；本条管"agent 能自己做到哪一步、何时必须问人"。

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

## r186 审计落地（Qoder r189-Q-C #5 审计，2026-09-25 实拉核验，全库 0 命中净新）

- **共享记忆按发言人身份定权＋in-flight 查重＋why 溯源**：多源记忆按来源身份定权（决策者 > 参与者 > bot 默认剔除）；写共享资产前查 in-flight 防并发重复劳动；结论行带 why 式溯源锚点。判据：共学栈直接同域——多源记忆按来源身份定权，避免无差别信任。来源 r189-Q-C（SkillApt / relore 实证）。


## Capability 12 — 两类记录要分开：诊断日志可以丢，审计留痕缺一段就等于没有（来源：Activepieces 官方博客《AI Vendor Questions for Audit Trail Integrity in 2026》，2026-09-27 r199-B 实拉 20,901B）

- **★先按用途分，再按用途决定存多久**：原文区分 **logs**（面向开发者的临时诊断工具，原文用词 *transient*）与 **audit trails**（面向审计方的永久法律记录，要记到"谁、在什么时候、对哪条受限数据做了什么"的粒度）。判据：**这份记录是拿来排查问题的，还是拿来事后举证的**——前者可丢、可截断、可以按量付费；后者少一段就等于全废。
- **★必须在写入之前分，不能事后筛**：原文给的量级是每 ingest 1TB/月：AWS CloudWatch $500 / GCP Cloud Logging $500 / Azure Monitor $2,760，成本随量线性增长 → **先把噪音当 truth 全量收进来再挑，预算已经花完了**。映射到协会：`log/YYYY-MM-DD.md`（诊断）与 `log/audit.jsonl`（取证）自建立时就是两条独立通道，不要合并写入之后再靠 groom 区分。
- **★★留痕通道不能挂在被观测的那个对象上**：原文指出主服务降级会产生 **silent gaps**——日志机制往往耦合于正在失败的那个应用，于是最关键的窗口一个事件都没录进去，而状态页**不会把这段报成"数据丢失"**。判据：**写下"某动作发生过"的那条路径，不能与这个动作本身共用同一个故障域**。agent 侧的对应写法：收尾证据落盘到独立位置并回读校验，而不是指望同一段会话上下文还活着。
- **不可验证的留痕在法律上等于没有留痕**：原文结论 "An unverifiable audit trail is legally indistinguishable from no audit trail at all"。→ §Capability 9 的"只搬不删 + 写 audit.jsonl"要配一个**能读回、能对上条数**的校验动作，保证"写过了"之外还要保证"当时写的那份还在"。
- 与 §Capability 9 groom、§Capability 11 记忆库固定文件分工 的分工：那两条管"过期数据怎么归档""文件按类别重写"；本条管"**两套记录的用途、成本与完整性要求本就不同**，以及**留痕的写入路径必须独立于被测对象**"。
- 提升层：工作流 / 可复用 Skill。

## Capability 13 — 留痕的范围由"显式输出"决定，不由"算过什么"决定（来源：Pipedream 官方 docs《Security Best Practices》，2026-09-27 r200-A 实拉 6,456B）

## Capability 14 — 多 Agent 编排：文件化 handoff + 评估器闭环 + 迭代上限（来源：GitHub Copilot agent mode / custom agents 实战文，2026-09-27 r252-C 实拉）

- **★文件化 handoff 替代共享上下文**：多 agent 协作时各 agent 不共享上下文，只通过**共享文件**传递（plan 写进 `docs/plans/*.md` 作为后续 agent 的共享记忆；subagent 的 5 万 token 探索随其消亡，只回传一份 synthesis 报告）。判据：协调靠"写盘的文件"不靠"都在同一上下文"——文件是跨 agent 的契约。
- **★evaluator-optimizer 闭环**：生成器产出解 → 评估器（编译器 / 测试套件）给客观真值反馈 → 反复修正直到通过所有判据。判据：LLM 会犯错，但工具（编译/测试）给客观真值，让 agent 基于工具输出自修比靠自评更准。
- **★迭代上限 5–10 次**：agent mode 循环设上限，防测试失败时陷入死循环。判据：任何自循环必须带退出上限，否则不可控。
- **★最小工具权限 + Plan Mode 质量门**：设计类 agent 不给 terminal；>3 文件 / 改 schema / 改公开接口 → 强制先出计划（计划 = definition of done），批准后再写码。判据：权限按角色最小化；计划文件是验收契约。

## Capability 15 — 群组式多 Agent：角色分工 + 人工打断特权 + 共享工作区（来源：智谱 AgentMore，2026-09-27 r252-C 实拉）

- **★群组协作两模式**：头脑风暴（多角色并行发散）vs 任务分配（各 agent 认领子任务）；单群上限 5 个 agent，超额需分群。判据：复杂任务用"多角色并行 + 任务分配"提速，但群规模有上限。
- **★人工打断特权**：群主可一键打断 agent 间无限对话。判据：自主多 agent 必须保留人类中断开关，防 runaway。
- **★共享工作区协调**：公共/私密文件空间作为 agent 间协同介质；Agent 持续自学习"日记"（越陪伴越懂你）。判据：共享工作区 = 群组内的协调层。
- **★企业短板**：AgentMore 缺 RBAC / 审计日志 / SSO、不可私有化——企业级多 agent 须补权限与审计（见 §Capability 12/13 留痕纪律）。

- **★★平台只持久化"从步骤返回或打印出来的数据"，内存里的中间变量一份都不进日志**：原文列出的保留范围 = 事件源发出的事件数据 + `console` 日志/错误 + 步骤导出（step exports）+ 错误栈里带的数据。判据：**想知道一份记录会不会留下，别看"这个东西有没有被算出来"，看"它有没有被 return / 打印 / 导出"**——同一份客户名单，在变量里过一遍不留痕，`console.log` 一行就永久留下。
- **★要收缩留痕面，动的是"输出"不是"计算"**：原文给的做法是改代码，**移除日志与步骤导出**，而不是不去做那个计算。判据：**留痕面与计算面是两层，脱敏要在出口做**；把"不敏感"寄托于"我只是临时用一下"，迟早被一次 `console.log` 或一次报错捅出去。
- **★错误栈是留痕的旁路**：平台保留一段有限的事件历史，而**错误栈会自动把字段带进留痕**——一次异常就能把本来没导出的内容永久化。判据：**设计输出时必须连异常路径一起想**：这条路径会带出什么，决定了失败时留痕面有多大。
- 与 §Capability 12 的分工：那条管"诊断日志与审计留痕是两种东西、且留痕通道不能挂在被测对象上"；本条管"**单次记录里到底装进哪些字段**"——一个定通道，一个定内容。
- 提升层：可观测性 / 工作流。

## Qoder 净新全量消化（2026-09-27）
- **删除即登记来源禁令（forgotten 位图）**（openclaw）：显式删除的来源/会话写入阻断位图，后续 ingestion 命中即拒，防同一数据经其他通道复活；边界：不触及原始转写与库外副本、无自动衰减需显式运营。
- **反回音室不变量**：被注入上下文的内容带来源标记且永不二次抽取入库；cron/自动化会话产物默认剥夺晋升资格，需人工会话复现后方可入精选。
- **记忆条目「锚+计数+调权」**（hindsight）：每条持久信念带原始出处引用锚与被复核计数；新证据到手**调整置信权重而非覆盖重写**，保留"何时开始相信什么"的审计线（覆盖写入会丢审计线，调权让过时程度可量化）。
- **共享记忆按发言人定权**：决策者>参与者>bot（默认剔除）；写共享资产前查 in-flight 防并发重复劳动；结论行带 why 式溯源锚点。

## r205-C 净新两点（2026-09-27 独立实拉）

### Capability 16 — 凭据与执行体容器级物理分离 + 输出四级管线（来源：GitHub Agentic Workflows 官方安全架构，经 agentpatterns.ai / aidevme 2026-09-27 r205-C 实拉）
- **★三种凭据分装三个容器，agent 容器零密钥**：LLM 凭据在 **API proxy 容器**（agent 经代理调用，看不到 key）；MCP 凭据在 **MCP gateway 容器**（按仓库策略路由，HTTP 转发）；**agent 容器**只带防火墙出网白名单 + 只读 /host 挂载 + tmpfs 覆盖 + chroot jail。判据：**密钥不该和会读不可信输入的那个进程共处一个故障域**——agent 被提示注入打穿时，手上是没有任何凭据的。
- **★四个信任边界分层，token 绑在配置层不在 agent 内**：Substrate（VM 隔离 + 内核强制通信边界）/ Configuration（声明式权限分派 + token 绑定）/ Planning（分阶段工作流 + 显式数据交换）。判据：**权限是声明出来的，不是运行时协商出来的**。
- **★写操作走 safe-outputs 四级管线，没有临时写权限**：Operation filtering（限可调 API）→ **Volume limiting**（封顶次数，如"最多 3 个 PR"）→ Content sanitization（剥掉 URL 与 secrets）→ Moderation（确定性分析后才允许下游投递）。判据：**"能不能写"之外必须还有"写多少 / 写什么内容 / 谁复核"三道闸**——只管能不能写，一次失控就是无限 blast radius。
- **★默认只读 + agent 产的 PR 永不自动合并**：先把流程跑成只读/只评论、证明低噪音后再开放 label / 建 PR。判据：**放权按观测到的行为渐进，不按预期行为一次性给**。
- 与 §Capability 12 留痕通道独立于被测对象、§Capability 13 留痕范围由显式输出决定 的分工：那两条管"记录怎么写、写哪些字段"；本条管"**执行体手里有什么、能往外做什么**"——一个定留痕，一个定权限。
- 提升层：工作流 / 安全边界。

### Capability 17 — 记忆晋升的三门 + 污点门控 + 压缩前静默 flush + 注入截断可观测（来源：OpenClaw 官方 `docs.openclaw.ai/concepts/memory`，2026-09-27 r205-C 实拉）
- **★后台巩固（dreaming）晋升带三门，不是"够久就升"**：候选必须同时过 **score / recall-frequency / query-diversity** 三道门槛才进长期记忆；**taint gated**——不可信来源与系统派生候选**永不进入巩固提示词，也永不走持久晋升通道**。判据：**晋升是带门槛的筛选，不是时间到了搬家**；自动化产物默认剥夺晋升资格（与 §Qoder 反回音室不变量同向）。
- **★人工复核面与机器排序面分开**：`DREAMS.md` 是人看的复核面（含 rewrite counts 与 highlights、可 grounded backfill 回放旧日志并可 `--rollback`）；短期 SQLite 存储是机器排序面；`MEMORY.md` **只由深度晋升写入**。判据：**人看的面、机器排的面、最终生效的文件，三者各一份，不要合并**。
- **★压缩前静默 flush 用私有对话副本**：compaction 前跑一个静默轮提醒 agent 存记忆，该轮用**对话的私有副本**，其 housekeeping 消息不会出现在后续用户轮（即使被中断）；只读/无 workspace 的沙箱跳过 flush；可为该轮单独指定小模型降本。判据：**"保存记忆"这个动作本身不能污染用户可见的对话**。
- **★超预算只截断注入副本、磁盘原文保留，并把截断当信号**：`MEMORY.md` 超 bootstrap 预算时磁盘文件不动，只截断注入上下文的副本；用 `/context list` 看 raw vs injected 大小与截断状态——**截断是"该把细料迁去 memory/*.md"的信号，不是"该删内容"**。判据：**先让它可观测（raw vs injected 各有数字），再决定搬还是加预算**。
- 与 §Capability 9 groom、§Qoder 记忆条目「锚+计数+调权」的分工：groom 管过期数据归档（只搬不删）；「锚+计数+调权」管单条信念的置信度更新方式；本条管"**从短期到长期的晋升这道门怎么设、人看什么、机器排什么**"。
- 提升层：可复用 Skill / 记忆治理。

## Agent 复用生命周期与显式交接契约：邀请 vs 一次性副本 vs 晋升，沙箱不互串（来源：Dify 新版 Agent 节点文档 2026-09-28 r207-B 独立实拉首读；docs.dify.ai/en/use-dify/nodes/agent）
- **三种复用形态，选错就产生分叉**：① 邀请已发布 agent（集中管理，能力改一处 → 所有引用它的工作流同步生效）；② Make a copy 一次性副本（节点内独立，从此不跟随原版）；③ 从零建。判据：**想让改动全局生效就用邀请，想做局部实验就用副本**；副本若"证明有价值"应**晋升**回共享资产供别处复用，而不是永远当私货。
- **同一 agent 被多处引用 ≠ 共享运行状态**：两个节点邀请同一个 agent 仍各自起独立沙箱，一个节点写的文件/装的工具不会带到另一个。判据：**能力可共享，状态不可共享**——跨节点传结果必须显式声明为 output 并由下游引用，不能指望"它刚才已经写过了"。
- **交接用声明式具名类型化输出，不是一大块 text**：默认只返回一个 `text`；下游若需要某个具体值或某个文件，要在任务文本里**声明具名 output 并指定类型**（如 `{{vendor_name}}`、`{{quote_file}}`），下游按名引用。判据：**交接边界上的东西必须有名字和类型**，否则下游只能靠解析自然语言。
- **任务变量按文本传会被截断（Dify 实测 2000 字符），长内容必须走文件**：单文件上限 50 MB。判据：**"传文本"和"传内容"是两件事**——超过阈值的正文、大表格、长日志一律走文件句柄，不要拼进提示词变量。
- 与 §Agent 自主权三档 / §记忆与技能频谱 的分工：那两条管"能自己做到哪一步""知识常驻还是按需"；本条管"**agent 被复用时，能力/状态/产物这三样各怎么过边界**"。

## 入站准入双门与会话隔离粒度（来源：docs.openclaw.ai 首页与配置段 2026-09-28 r207-B 独立实拉；与 §r205-C Cap16 凭据分离互补——那条管凭据不落执行体，本条管会话边界与谁能进来）
- **会话隔离有三条轴可选**：per-agent / per-workspace / per-sender，按部署形态选，不要默认全共享。默认策略是**私聊共享 agent 主 session，每个群聊各自独立 session**。判据：**隔离粒度是配置项不是默认值**，先想清楚"谁的历史该被谁看见"。
- **入站准入是两道门，缺一道就会被外部消息驱动**：`allowFrom` 白名单（谁能发）+ `requireMention`（群里是否必须 @）。判据：**能发消息进来 = 能驱动 agent 干活**；只配白名单不配 mention 规则，等于把 agent 交给群里所有人。
- **架构上把"受信任网关"与"不可信执行"分开，策略用确定性规则表达**：网关是会话/路由/连接的唯一真身，执行侧当不可信；`~/.openclaw/openclaw.json` 是唯一配置面。判据：**信任边界画在网关上，不要画在 prompt 里**。
- 提升层：工作流 / 工具。触发词：邀请 agent、一次性副本、晋升共享、沙箱不互串、具名输出、声明式输出、变量截断、走文件传、会话隔离、per-sender、allowFrom、requireMention、入站准入。

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


## Cap21 运行态目录独占 + 确定性路由：agentDir 不可复用，凭据回退是「只借不复制」的穿透（来源：docs.openclaw.ai《Multi-agent routing》2026-09-29 r286-B 独立实拉原文核验）
- 红线原文："Never reuse `agentDir` across agents — it causes auth/session state collisions."；`agentDir` 一处承载 auth profiles、model registry 与会话 SQLite。
- 最反直觉的一条：**凭据穿透只借不复制**——从 agent 的 OAuth 过期或刷新失败时会穿透读到主 agent 同 profile id 的凭据、取更鲜的 token，**但不把 refresh token 写进从 agent 的库**；要完全独立只能在该 agent 内自己登录，手工搬运仅限 `api_key`/`token` 静态档（OAuth refresh 材质默认不可移植）。
- 路由原文 "Bindings are deterministic and most-specific wins."，九级次序：exact peer → parent peer → peer wildcard → guild+roles → guild → team → account → channel → default agent。
- 判据：多 agent 同机共存时，**隔离的单位是状态目录不是进程**——"各跑各的进程"不等于凭据不串。
