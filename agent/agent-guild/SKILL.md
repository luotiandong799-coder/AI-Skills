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
version: 1.29.0
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

> 下沉索引：Capability 5（Refresh last_seen）与 Capability 6（Where to persist shared data）原文已移至 `references/knowledge-base.md` §r340B
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

<!-- 2026-09-30 r336B 下沉：r186 审计落地（Qoder r189-Q-C #5 · 0 净新）整段 → references/knowledge-base.md §r336B -->

<!-- 2026-09-29 r290 下沉：Capability 12 诊断日志与审计留痕分仓 → references/knowledge-base.md §r199-B 批 -->
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

<!-- 2026-09-30 r336B 下沉：Qoder 净新全量消化（2026-09-27）4 条 → references/knowledge-base.md §r336B -->

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
