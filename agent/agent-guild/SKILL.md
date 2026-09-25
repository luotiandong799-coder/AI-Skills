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
  `ag init/adopt/bootstrap/doctor/groom/upgrade/learn/review/resolve`（upgrade
  自动从 skillhub/github/clawhub 查最新版并更新）。
  未加入？先跑 docs/ONBOARDING.md。、审批模式、分层授权、只读免审、gated actions、Manual/Auto/YOLO、Auto≠沙箱、授权启发式、越权复核、目标驱动、goal、rubric、验收标准、定义完成、粘滞质量门、amend/pause/resume、逐轮评分、记忆与技能、AGENTS.md、按需加载、always-loaded、on-demand、全局vs项目
slug: agent-guild
displayName: 智能体协会 Agent Guild
protocol_version: "3.2"
version: 1.3.1
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

一次读全：用户画像 → 日程 → 最高优先级戒律 → 在做的项目 → 各 agent 当前焦点 → 你的未读收件箱。

| 文件 | 内容 |
|---|---|
| `identity/profile.md` | 用户是谁 |
| `identity/ROUTINE.md` | 日程 / 习惯 |
| `rules/universal.md` | 最高优先级戒律 |
| `projects/active.md` | 用户当前在做什么 |
| `handoff/shared-state/current-focus.md` | 各 agent 当前焦点 |

读到什么就按什么做。**没读就动手 = 违反协议。** 之后按需再读 `toolchain/*.md`、其他 `rules/*.md`。

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

- **审计脚本**：`D:\腾讯AI\yt\scripts\skill_eval.py`（托管 python 运行），扫描 `D:\AI技能仓库` 全部 SKILL.md，产出 `D:\腾讯AI\yt\outputs\skill-eval\<日期>_eval.md`（技能总数、机检异常、重叠候选 Jaccard≥0.3）。
- **机检**：CRLF / STRAY_CR / FFFD / description≤1024，异常即 LF 化修复（repo 与 live 同步），修后重跑 sha256。
- **重叠处置**：运行时治理 vs 编写期 ≠ 重复保留；同功能层 Jaccard>0.6 才列合并/淘汰候选。**淘汰/合并属 L2，须用户确认才执行，不擅自强删。**
- **调度**：不另建自动化；作为本学习技能的职责，随现有学习循环（agent-guild 上下文）每次运行附带或周期性触发。
- 参考方法：wb-skill-authoring（评估/去重合并）、knowledge-governance（重叠/归档）、agent-evolution（生命周期治理）。
