

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


## r340B 下沉：Capability 5 / 6（Refresh last_seen · Where to persist shared data）2026-10-01
## Capability 5 — Refresh last_seen

Once per session, update your entry's `last_seen` (prefer `ag last-seen`, fallback Edit). Never overwrite the whole registry — patch only your entry.

## Capability 6 — Where to persist shared data

New skill / MCP / plugin / tool / persistent data you install → **MUST** go under `~/.agent-guild/{skills,skills_data,mcp,plugins,tools}/<name>/`, not a private path (唯一豁免见 M3). The user backs up the whole `~/.agent-guild/` with one command.


## §r344A 下沉｜Capability 17 — 记忆晋升的三门 + 污点门控 + 压缩前静默 flush + 注入截断可观测（来源：OpenClaw 官方 `docs.openclaw.ai/concepts/memory`，2026-09-27 r205-C 实拉）
- 后台巩固（dreaming）晋升带三门：候选同时过 score / recall-frequency / query-diversity 才进长期记忆；taint gated——不可信来源与系统派生候选永不进入巩固提示词，也不走持久晋升通道。判据：晋升是带门槛的筛选，不是时间到了搬家。
- 人工复核面与机器排序面分开：`DREAMS.md` 是人看的复核面（rewrite counts / highlights、可 grounded backfill 回放旧日志并 `--rollback`）；短期 SQLite 是机器排序面；`MEMORY.md` 只由深度晋升写入。
- 压缩前静默 flush 用对话的私有副本，housekeeping 消息不出现在后续用户轮（即使被中断）；只读/无 workspace 沙箱跳过；可单独指定小模型降本。
- 超预算只截断注入副本、磁盘原文保留；`/context list` 看 raw vs injected 与截断状态——截断是"该把细料迁去 memory/*.md"的信号，不是"该删内容"。

## 学习轮沉淀 r347A（来源 Qoder r360-Q-A · 2026-10-01 · 入站/出站分面）
- **跨会话/跨 agent 入站须显式 accept，与出站分面各自默认关**：如 `"crossSessionInbound":"accept"` 才受理入站；共享后撤销另有纪律（revocable session sharing），入站默认极性此前未管。判据：入站默认拒；身份声明≠授权。来源：claude-delegation / openclaw bindings。

## 学习轮沉淀 r347B（来源 Qoder r361-Q-B · 2026-10-01 · 派发身份伪造）
- **派发身份可被伪造劫持授权（跨编排器实证）**：TrustFork（arXiv 2609.32635，1890 任务/27,826 轨迹/16 系统/8 orchestrator 含 OpenCode/Opus 等）实证跨编排器派发身份可伪造。判据：跨编排器派发须验真身份，身份声明≠授权。来源：arXiv 2609.32635。


# §r349C 下沉

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

## §r395-ag 下沉（原文零删减，自 SKILL.md 移入）

<!-- src: SKILL.md L189-L202 -->
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


<!-- src: SKILL.md L218-L226 -->
## Agent 自主权分三档：只读免审，gated 需审，Auto≠沙箱（来源：LangChain Deep Agents Code approval-modes，2026-09-23 r150-B 独立实拉首读，清单外新信源）

- **把动作分成"只读"和"gated"两类**：`ls/read/glob/grep` 等只读工具永远免审直接跑；写/删文件、跑 shell、发 web 请求、委派子代理属 gated，需审批。判据：给 agent 自主权先分清楚"看"和"改/外发"，不要一锅烩。
- **三档模式**：Manual（每次 gated 都问）、Auto（常规动作自动过、不确定的交给模型审、反复拒绝/分类失败再退回人）、YOLO（完全不审，需一次性风险确认）。
- **Auto 是授权启发式，不是沙箱**：文档明说 Auto 不提供 OS 边界、不保证生成动作安全。把"自动批准"当成"安全"是误区。
- **Auto 的判定流**：常规动作直过 → 不确定的由活动模型按用户请求审效果 → 高风险的（如把本地内容发往未配置目的地）仍要显式授权；反复拒绝/分类失败就停、转回人审。
- **越权前先复核状态**：决策绑定线程/模式/批次/具体调用；切到 Manual 或状态竞态/重放时，回退到人审，不让旧 Auto 决定静默执行。
- 与 §记忆与技能分层 / §目标驱动 的分工：那条管身份与上下文；本条管"agent 能自己做到哪一步、何时必须问人"。

## §r395-ag2 下沉（原文零删减，自 SKILL.md 移入）

<!-- src: SKILL.md L244-L245 -->
## Capability 13 — 留痕的范围由"显式输出"决定，不由"算过什么"决定（来源：Pipedream 官方 docs《Security Best Practices》，2026-09-27 r200-A 实拉 6,456B）


<!-- src: SKILL.md L246-L252 -->
## Capability 14 — 多 Agent 编排：文件化 handoff + 评估器闭环 + 迭代上限（来源：GitHub Copilot agent mode / custom agents 实战文，2026-09-27 r252-C 实拉）

- **★文件化 handoff 替代共享上下文**：多 agent 协作时各 agent 不共享上下文，只通过**共享文件**传递（plan 写进 `docs/plans/*.md` 作为后续 agent 的共享记忆；subagent 的 5 万 token 探索随其消亡，只回传一份 synthesis 报告）。判据：协调靠"写盘的文件"不靠"都在同一上下文"——文件是跨 agent 的契约。
- **★evaluator-optimizer 闭环**：生成器产出解 → 评估器（编译器 / 测试套件）给客观真值反馈 → 反复修正直到通过所有判据。判据：LLM 会犯错，但工具（编译/测试）给客观真值，让 agent 基于工具输出自修比靠自评更准。
- **★迭代上限 5–10 次**：agent mode 循环设上限，防测试失败时陷入死循环。判据：任何自循环必须带退出上限，否则不可控。
- **★最小工具权限 + Plan Mode 质量门**：设计类 agent 不给 terminal；>3 文件 / 改 schema / 改公开接口 → 强制先出计划（计划 = definition of done），批准后再写码。判据：权限按角色最小化；计划文件是验收契约。


<!-- src: SKILL.md L253-L267 -->
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

## Capability 1-4（2026-10-03 r396B 自 SKILL.md 下沉）

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

## §Capability 4-10 下沉（2026-10-03 r408A 自 SKILL.md 下沉）
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

## Capability 10 — 记忆分仓与路标式索引：私有仓 vs 组织共享仓

> 原文已下沉 `references/knowledge-base.md §r395-ag`（保持原文零删减）。


## 学习轮下沉 r413A（ag SKILL.md 行数治理 · 原 Cap38 / Cap39 整节下沉）
### Cap38 待办先落盘再到期执行；维护类任务停了也不报错（来源：docs.n8n.io durable-scheduler.md + system-tasks.md，r354A 实拉）
- 计划先持久化再执行：in-memory 定时器随进程停止而丢，且停机期间过期的运行被跳过而非补跑。
- 静默失败是维护类任务的默认失效模式：无调用方、无报错、不在编辑器出现，唯一症状是"该变小的一直变大 / 该变新的越来越旧" ⇒ 必须配独立存活信号。
- 观测面须覆盖两种模式且指标名能区分（in_memory vs durable），否则"该模式下从没跑过"被显示成"没有数据"。
- 配套看板每面板给一条建议动作，交付物是"看到这个数该做什么"而非图表。
- 提升层：工具 / 工作流 / 可复用 Skill。

### Cap39 数据外迁时清理责任一并外迁；不做配置 = 默认永久保留（来源：docs.n8n.io use-external-storage.md，r354C 实拉）
- 存储位置变更连带改变清理责任归属：搬到外部存储后主系统剪枝逻辑不再覆盖它。
- 未配置的默认态是"无限期保留"而非"继承原策略" ⇒ 外迁动作必须配"谁负责删 / 多久删 / 按什么条件删"。
- groom 规则必须显式覆盖外迁位置并声明周期，清理清单把"外迁出去的部分"列为独立条目。
- 提升层：工作流 / 可复用 Skill。


## 学习轮下沉 r413C（ag SKILL.md 行数治理 · 原 Cap40 / Cap41 整节下沉）
## Cap40 授权评审的对象是「权限组合」而非单项；授予的是可事后改写的角色定义，不是权限快照（来源：docs.n8n.io `administer/.../create-custom-instance-roles.md` 8,015B + `create-custom-project-roles.md` 11,109B + `see-available-roles.md` 4,301B，2026-10-03 r388A 独立 curl 取 .md 原文实拉）
- **原文**：「A user with **Roles: Manage all roles** can edit their own custom role to add permissions they weren't originally granted.」「A user with **Members: Manage** can invite a user they control, then grant that user Admin-level access.」「Changes to a custom instance role take effect for **all users with that role** across the entire instance.」「If users have this role, reassign them to a different role before deleting it.」
- **判据**：① **单项权限都合法，组合起来才是提权路径**——「能改角色」+「自己持有该角色」= 自提权；「能邀请人」+「能给人授权」= 借壳提权。逐项审批看不到这两条，只有把已授出的权限当**一个集合**做组合评审才能发现。② **授予动作指向的是角色定义（活引用），不是权限快照**——改一次角色定义，所有持有者的权限面当场漂移；因此「当初批了什么」不能作为当前权限的证据，撤销/复核必须回查角色定义的当前内容。③ **角色不可留空指向即删**——删除前必须先改派；guild 的交接与授权回收同理：先把成员/agent 迁到新角色，再回收旧角色，顺序颠倒会产生无归属窗口。
- 提升层：工作流 / 可复用 Skill。触发词：权限组合提权、自提权、角色活引用、改角色即批量改权限、删除前改派、授权回收顺序。

## Cap41 审批回执要落稳定终态码，「不可用」类不等于「拒绝」类；留痕开关只向前生效（来源：docs.openclaw.ai/gateway/audit.md 37,793B，2026-10-03 r388B 独立实拉）
- **原文**：审批结果映射稳定 reason code：`operator_approval_allowed_once/always`、`_denied_by_reviewer`、`operator_approval_expired`、`_cancelled_run_aborted`、`_cancelled_gateway_restart`、`_denied_no_route`、`_denied_malformed_verdict`、`_denied_storage_corrupt`、`operator_approval_record_corrupt`、`_execution_link_missing/_malformed/_mismatch`；「An unreadable row is `unknown`, never reconstructed.」「Enabling collection does not backfill earlier activity or add identity to an already admitted run.」「Its outcome is `not-applicable` ... This is an explanation of admission evidence, not an enforcement claim.」
- **判据**：① **审批终态是一张码表不是布尔值**——除了允许/驳回，还必须有 过期 / 被中止（运行 abort、网关重启）/ 无投递路由 / 判定畸形 / 存储损坏 / 记录损坏 / 绑定缺失·畸形·不匹配；把后几类归并成「驳回」会把**基础设施故障误记成人的决定**，问责时会追错对象。② **「不可用」类是独立一类，不是拒绝**——读不出来的回执判 unknown 并给出补救，绝不重建一条。③ **留痕/审计开关只向前生效**——开启不回溯历史活动，也不给已准入的运行补身份；「我们开了审计」不能作为追溯既往的证据。④ **回执存在 ≠ 判定发生过**——`not-applicable` 是显式终态，含义是「没有任何身份相关策略被证明执行过」；guild 的审批留痕要能表达这一态，否则空回执会被读成「已审批通过」。
- 提升层：工作流 / 可复用 Skill。触发词：审批终态码表、expired、no-route、malformed_verdict、storage_corrupt、link_mismatch、不可用≠拒绝、留痕不回溯、not-applicable 回执。
<!-- sunk from SKILL.md 2026-10-04 r415 原文零删减 -->

## §r415-ag（2026-10-04 r415 下沉，原文零删减）
## Cap35 多人共改同一轮：改向与中止是两个意图、身份可共享而权限不可共享、可见不等于已被消费（来源：docs.openclaw.ai/concepts/queue-steering 12,366B + concepts/retry 10,184B，2026-10-01 r344A 独立 curl 实拉逐串命中；与 §说过≠记着 互补——那条管"消息进没进队列"，本条管"消息有没有被消费、以谁的名义执行"）
- **原文**："**A visible message or send acknowledgment does not mean the active runtime has consumed it.**"；"**Stopping already-running work is a different intent from redirecting future work.**"；并行批次 "one atomic launch checkpoint… a steer arriving after it does not recall any of them"；被跳过的调用 "receives **paired** tool start/end events and a synthetic result"；turn "**keeps its original owner's authority, tool bindings, and approval destination**"；个人上下文重分配 "takes effect on the **next new turn**; it does not replace the running turn's personal instructions"；权限不同的消息 "**queue the message as a followup**"；撤回 `chat.abort` 仅"before delivery starts"，"once delivery starts, cancellation cannot guarantee withdrawal or undo completed work"。
- **判据**：① **改向（redirect）与中止（abort）必须做成两个动作**——改向只影响"尚未启动的工作"，已跨过发射检查点的调用不召回；拿中止去表达改向，代价是丢掉已完成的工作；② **被跳过的工作也必须配一条结果**（配对 start/end + 合成结果），留痕保持结构配对，否则下游看到"请求了却没有结果"会误判成执行失败；③ **多人共轮时身份可共享、权限不可共享**——谁能插话是一回事，以谁的名义执行、审批发到谁是另一回事；权限不同的输入降级到下一轮，不在运行中改权限；④ **送达回执不是消费证据**，撤回只在投递开始前可保证，已开始的取消必须明示"不保证撤销已完成工作"。
- 提升层：工作流/安全边界。触发词：改向、中止、跳过调用的配对结果、发射检查点、多人共轮、身份可共享权限不可共享、送达不等于消费、撤回了但仍执行。

## Agent 复用生命周期与显式交接契约：邀请 vs 一次性副本 vs 晋升，沙箱不互串（来源：Dify 新版 Agent 节点文档 2026-09-28 r207-B 独立实拉首读；docs.dify.ai/en/use-dify/nodes/agent）
- **三种复用形态，选错就产生分叉**：① 邀请已发布 agent（集中管理，能力改一处 → 所有引用它的工作流同步生效）；② Make a copy 一次性副本（节点内独立，从此不跟随原版）；③ 从零建。判据：**想让改动全局生效就用邀请，想做局部实验就用副本**；副本若"证明有价值"应**晋升**回共享资产供别处复用，而不是永远当私货。
- **同一 agent 被多处引用 ≠ 共享运行状态**：两个节点邀请同一个 agent 仍各自起独立沙箱，一个节点写的文件/装的工具不会带到另一个。判据：**能力可共享，状态不可共享**——跨节点传结果必须显式声明为 output 并由下游引用，不能指望"它刚才已经写过了"。
- **交接用声明式具名类型化输出，不是一大块 text**：默认只返回一个 `text`；下游若需要某个具体值或某个文件，要在任务文本里**声明具名 output 并指定类型**（如 `{{vendor_name}}`、`{{quote_file}}`），下游按名引用。判据：**交接边界上的东西必须有名字和类型**，否则下游只能靠解析自然语言。
- **任务变量按文本传会被截断（Dify 实测 2000 字符），长内容必须走文件**：单文件上限 50 MB。判据：**"传文本"和"传内容"是两件事**——超过阈值的正文、大表格、长日志一律走文件句柄，不要拼进提示词变量。
- 与 §Agent 自主权三档 / §记忆与技能频谱 的分工：那两条管"能自己做到哪一步""知识常驻还是按需"；本条管"**agent 被复用时，能力/状态/产物这三样各怎么过边界**"。

## 下沉存档 §r417-ag（2026-10-04，零删减自 SKILL.md）

## Capability 13 — 留痕的范围由"显式输出"决定，不由"算过什么"决定

> 原文已下沉 `references/knowledge-base.md §r395-ag2`（保持原文零删减）。
## Capability 14 — 多 Agent 编排：文件化 handoff + 评估器闭环 + 迭代上限

> 原文已下沉 `references/knowledge-base.md §r395-ag2`（保持原文零删减）。
## Capability 15 — 群组式多 Agent：角色分工 + 人工打断特权 + 共享工作区

> 原文已下沉 `references/knowledge-base.md §r395-ag2`（保持原文零删减）。
## r205-C 净新两点（2026-09-27 独立实拉）


## 入站准入双门与会话隔离粒度（来源：docs.openclaw.ai 首页与配置段 2026-09-28 r207-B 独立实拉；与 §r205-C Cap16 凭据分离互补——那条管凭据不落执行体，本条管会话边界与谁能进来）
- **会话隔离有三条轴可选**：per-agent / per-workspace / per-sender，按部署形态选，不要默认全共享。默认策略是**私聊共享 agent 主 session，每个群聊各自独立 session**。判据：**隔离粒度是配置项不是默认值**，先想清楚"谁的历史该被谁看见"。
- **入站准入是两道门，缺一道就会被外部消息驱动**：`allowFrom` 白名单（谁能发）+ `requireMention`（群里是否必须 @）。判据：**能发消息进来 = 能驱动 agent 干活**；只配白名单不配 mention 规则，等于把 agent 交给群里所有人。
- **架构上把"受信任网关"与"不可信执行"分开，策略用确定性规则表达**：网关是会话/路由/连接的唯一真身，执行侧当不可信；`~/.openclaw/openclaw.json` 是唯一配置面。判据：**信任边界画在网关上，不要画在 prompt 里**。
- 提升层：工作流 / 工具。触发词：邀请 agent、一次性副本、晋升共享、沙箱不互串、具名输出、声明式输出、变量截断、走文件传、会话隔离、per-sender、allowFrom、requireMention、入站准入。


## r418A 下沉（Cap23/24/25 沙箱边界三角，自 SKILL.md 迁入以腾 500 行预算）
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




## §r420-ag 存档（2026-10-05 r420A 下沉，零删减）

### Capability 16 — 凭据与执行体容器级物理分离 + 输出四级管线（来源：GitHub Agentic Workflows 官方安全架构，经 agentpatterns.ai / aidevme 2026-09-27 r205-C 实拉）
- **★三种凭据分装三个容器，agent 容器零密钥**：LLM 凭据在 **API proxy 容器**（agent 经代理调用，看不到 key）；MCP 凭据在 **MCP gateway 容器**（按仓库策略路由，HTTP 转发）；**agent 容器**只带防火墙出网白名单 + 只读 /host 挂载 + tmpfs 覆盖 + chroot jail。判据：**密钥不该和会读不可信输入的那个进程共处一个故障域**——agent 被提示注入打穿时，手上是没有任何凭据的。
- **★四个信任边界分层，token 绑在配置层不在 agent 内**：Substrate（VM 隔离 + 内核强制通信边界）/ Configuration（声明式权限分派 + token 绑定）/ Planning（分阶段工作流 + 显式数据交换）。判据：**权限是声明出来的，不是运行时协商出来的**。
- **★写操作走 safe-outputs 四级管线，没有临时写权限**：Operation filtering（限可调 API）→ **Volume limiting**（封顶次数，如"最多 3 个 PR"）→ Content sanitization（剥掉 URL 与 secrets）→ Moderation（确定性分析后才允许下游投递）。判据：**"能不能写"之外必须还有"写多少 / 写什么内容 / 谁复核"三道闸**——只管能不能写，一次失控就是无限 blast radius。
- **★默认只读 + agent 产的 PR 永不自动合并**：先把流程跑成只读/只评论、证明低噪音后再开放 label / 建 PR。判据：**放权按观测到的行为渐进，不按预期行为一次性给**。
- 与 §Capability 12 留痕通道独立于被测对象、§Capability 13 留痕范围由显式输出决定 的分工：那两条管"记录怎么写、写哪些字段"；本条管"**执行体手里有什么、能往外做什么**"——一个定留痕，一个定权限。
- 提升层：工作流 / 安全边界。

## 评审类协作的质量由「给评审者什么上下文」决定，且评审必须尽早（来源：deeplearning.ai《AI Code Review》（Qodo，1h4m，Intermediate）2026-09-28 r208-C 独立实拉）
- **评审无效的常见根因不是评审规则写得不好，是评审者拿到的上下文不对**：课程核心断言 `context is what makes a review reliable`，做法是把 `giving the reviewer the right context` 当作设计评审流程的第一件事。判据：**改评审提示词前先改评审输入；上下文错了，规则越细越自信地错。**
- **评审要尽早运行，而不是等产物完整后一次评审**：课程明确"尽早运行评审"。判据：**评审推迟的代价是返工面变大，不是评审变准**；早评审发现的是方向问题，晚评审只能发现细节问题。
- **做评审 agent 时，先定义"它需要看见什么"，再定义"它该说什么"**：课程路径是先给对上下文 → 再构建自己的 review agent。判据：**顺序反了会得到一台语气很好但看不见关键面的评审机器。**
- 判重：与 wb-artifact-verification §独立证据源（验证要看独立证据）相邻——那条管「验证的独立性」，本条管「评审输入的完整性」。
- 提升层：工作流 / 可复用 Skill。触发词：评审上下文、评审不可靠、评审 agent、尽早评审、评审质量、review context、给评审者什么。


## §r420-ag-C 存档（2026-10-05 r420C 下沉，零删减）

## 治理处置增「申诉期冻结态」：被质疑不下架，转只读冻结（来源：help.openai.com/en/articles/8798878-sharing-and-publishing-gpts 2026-09-28 r313-Q-C 浏览器实拉 + r279-C 复核）
- **实证**：OpenAI GPT 发布申诉期政策——"While an appeal is under review: You can continue using the GPT privately; You cannot edit or update it; You cannot share it with others until the appeal is resolved or you cancel it." 即**私人可用、禁编辑/更新/对外分享**的冻结态。
- **判据**：治理处置增一档「只读冻结」——被质疑/审核中的技能不下架、不删，转成"可私有使用、禁编辑/更新/对外分享"，申诉解决后自动解冻；另一硬前置：任何对外暴露动作/工具**必须自带隐私与出处声明字段**。
- 提升层：工作流。触发词：申诉期冻结、只读冻结、隐私出处声明、治理处置档、appeal under review。

## 说过 ≠ 记着：发消息本身不入队，任务必须由具名 owner 显式登记（来源：github.com/mvschwarz/openrig README 2026-09-28 r283-B 独立 WebFetch 取正文核验）
- **实证**：官方原文「**Sending a message does not itself create a queue item; the owner records the task.**」；配套命令 `rig send dev-owner@first-project '... Track the task in the queue and return its ID ...'` + `rig queue list --destination dev-owner@first-project`。拓扑另以 **YAML RigSpec 声明**（pods / members / edges / continuity policies / culture file）。同文佐证：YOLO **off by default**，`rig down --snapshot` / `rig up <name>` 快照恢复并逐节点报告 resumed/fresh/failed。
- **判据**：**通信内容与任务队列是两个东西**——消息被收到不等于任务被接下。跨 agent 交接时，必须由具名 owner 显式登记任务并给出 ID，否则「我们讨论过」会被当成「有人在做」，形成无人认领的假成功。
- **落地动作**：交接消息里凡含请求，结尾必须要求对方回一个**任务 ID**；收到请求的一方，登记动作先于回复动作。无 ID 的交接，发起方不得标记为"已派发"。
- 提升层：工作流。触发词：发消息不入队、said vs recorded、任务 ID、具名 owner、交接登记、假成功、RigSpec。

## Cap74 多 agent 编播编排：预算计的是「尝试」不是「产出」，续轮的输入是合成摘要不是原始事件（来源：docs.openclaw.ai/channels/broadcast-groups.md 20,936B + channels/channel-routing.md 9,997B + channels/access-groups.md 7,329B + channels/ambient-room-events.md 9,078B + channels/bot-loop-protection.md 5,889B，2026-10-05 r418A 独立 curl 取 `.md` 原文实拉逐串命中；与 Cap71 有界队列 / Cap26 互聊滑动窗口 互补——那两条管单通道积压与双 bot 互激，本条管一次入站扇出给多个 agent 时的预算、续轮与隔离面）
- 原文："`maxTurns` counts **agent runs started by the coordinator**, including runs that pass or fail. **Slots are reserved synchronously before parallel launch**… If the budget is smaller than the eligible participant count, configured order determines which turns start."；"Each receives an **attributed, size-bounded digest of sibling finals**… **it is not a replay of the physical inbound message**"；"All participants passing ends the thread."；"Budget state is in memory… **It is not restart-resumable**: a Gateway restart loses the active round and budget state."；"`maxTurns` does not count, buffer, or cap physical messages."；"Agents fail independently… does not block the others."；隔离清单 "Session keys / Conversation history / Workspace / Tool access / Memory/context" 五面全隔，而 WhatsApp "group context buffer… is shared on purpose… **cleared once after the fan-out completes**"；路由侧 "Even when direct-message conversation history is shared with main, **sandbox and tool policy use a derived per-account direct-chat runtime key**"；访问组 "**A group grants nothing by itself.** It only matters where an allowlist field references it."
- 判据：① **预算的计数对象必须先声明**——计「启动过的运行」（含失败与弃权）还是「成功产出」，两者在部分失败时会给出完全不同的剩余额度，混用会让「还剩多少次」变成一个不可信的数字；② **槽位同步预留 + 配置顺序决定取舍**：额度小于合格参与者数时不是随机丢弃，而是按声明顺序取前 N，取舍必须是确定性的、可复现的；③ **续轮拿到的不是原事件**：后续轮的输入是「带归属、有长度上限的兄弟结论摘要」，它有自己的内部身份，**不是物理入站消息的重放** ⇒ 凡「让下一步重看原始输入」的设计，必须显式把原始输入单独传下去，不能指望继承；④ **收敛靠显式弃权信号**：全员弃权才结束线程，「没说话」不能等同于「同意结束」；⑤ **编排中间态是易失的**——轮次与预算状态在内存、范围到根消息、宿主重启即丢且不续 ⇒ 需要跨重启续跑的编排必须自己持久化进度，不能指望调度器；⑥ **隔离要逐面列清单，并把「刻意没隔的那一个」单独点名**（本例是共享群上下文缓冲）且说明它的生命周期（扇出完成后清一次）——只写「已隔离」的声明无法验收；⑦ **上下文可以合并而策略不可以**：私信历史并入主会话时，沙箱与工具策略仍走派生运行时键 ⇒ 「共享了上下文」不得被解读为「拿到了同等执行面」；⑧ **命名集合本身不授权**：访问组定义了也不生效，只有在白名单字段引用它的那个点上才生效 ⇒ 判断「某主体有没有权限」要找引用点，不是找定义点。
- 提升层：工作流 / 可复用 Skill。触发词：多 agent 编播、扇出预算、maxTurns、槽位预留、续轮摘要、派生输入不是重放、全员弃权结束、编排状态易失、隔离面清单、共享上下文不共享策略、命名组不授权。

## Cap75 持久自主程序 = 四字段定义（Scope/Triggers/Approval gates/Escalation）+ 显式「不该做」护栏；Standing Order 定「什么」、Automation 定「何时」（来源：docs.openclaw.ai/automation/standing-orders.md 9,726B，2026-10-05 r418C 独立 curl 取 `.md` 原文实拉逐串命中；与 Cap26 互聊护栏 / Cap73 三道门 / §三档审批 互补——那几条管单条入站与授权面，本条管「常驻自主程序」这一整类对象的定义结构与护栏沉淀）

- **原文**："Each program specifies: 1. **Scope** - what the agent is authorized to do; 2. **Triggers** - when to execute (schedule, event, or condition); 3. **Approval gates** - what requires human sign-off before acting; 4. **Escalation rules** - when to stop and ask for help."；"### What NOT to do: Do not send reports to external parties / Do not modify source data / Do not skip delivery if metrics look bad - report accurately."；"Standing orders define **what** the agent is authorized to do. Automations define **when** it happens."
- **判据**：① **常驻自主程序必须四字段齐备**：Scope（授权边界）/ Triggers（触发：定时·事件·条件）/ Approval gates（哪些动作前须人审）/ Escalation（何时停手求助）——缺任一字段=该程序定义不完整，验收时无法判断「它到底被允许到哪」。② **正向 Scope 不够，必须显式写「不该做」**：只列「能做什么」会漏掉「绝不能做」的负向约束；负向护栏（不发外域、不改源数据、指标异常也要如实报）要作为程序定义的一节 bake in，不能靠运行时临场判断。③ **What 与 When 分离**：Standing Order 定「授权与护栏」（what），Automation/cron 定「何时执行」（when），两者引用而非复制——把触发逻辑写进程序定义会让「改频率」变成「改程序」，把程序逻辑写进 cron 会让「改行为」变成「改调度」。④ **自主程序是边界对象不是一次性提示**：它常驻于 `AGENTS.md`/`standing-orders.md` 每会话自动注入，与 one-shot 脚本入口（跳过 workspace bootstrap）是两回事 ⇒ 凡「长期自主运行」的需求，先问「它的四字段定义与负向护栏写好了吗」，没写就是裸奔。
- 提升层：工作流 / 可复用 Skill。触发词：持久自主程序、四字段定义、Scope/Triggers/Approval/Escalation、显式不该做护栏、What 与 When 分离、常驻注入非一次性。

<!-- r422A 自 SKILL.md 下沉 -->

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

<!-- r424A 自 SKILL.md 下沉 -->

## Cap60 中断不是错误、也不产生错误事件；等待态只接受"回应"不接受新指令，且中断会取消整组等待（来源：docs.bigmodel.cn `cn/managed-agents/faq.md` 7,447B + `events.md` 15,944B，2026-10-04 r409C 独立 curl 取 `.md` 原文实拉；与 §Cap35 改向与中止是两个意图 / §Cap55 权威源是服务端记录 互补——那两条管"改向≠中止"与"以谁的记录为准"，本条管"中断在事件面上长什么样"与"等待态接受什么输入"）
- **原文**：`发送 user.interrupt 后，平台会主动停止当前模型响应，并向运行中的命令发出停止信号；命令在宽限期内（当前约 3 秒）没有结束会被强制终止，本轮必然停下`；`中断不会产生 session.error`；`interrupt 之前尚未处理的消息会被跳过，之后提交的 user.message 会在下一轮执行`；`若停在 requires_action，interrupt 会取消整组等待中的工具调用和审批`；`停在 requires_action：在等你处理 event_ids 里列出的调用……此时发 user.message 会被拒绝（400）`；`更新 Agent 返回 409……服务器上当前版本已经变了——通常是别人（或另一次请求）刚更新过。先 GET 最新 Agent，用返回的 version 再更新；CI 这类声明式同步可以省略 version，后写覆盖`。
- **判据**：① **主动中断与失败是两条通道**：中断不产生 `session.error` ⇒ 监控不要用"有没有错误事件"判断"是不是出了问题"，被中断的轮次在错误面上完全干净，要另设中断计数。② **中断有宽限期且必然停**：命令先收到停止信号、宽限期内不退出才强杀 ⇒ "发了 interrupt 却还在跑"看的是宽限期，不是中断失效。③ **等待态的输入类型是受限的**：`requires_action` 下只能回 `user.custom_tool_result` / `user.tool_confirmation`，发新 `user.message` 直接 400 ⇒ 等待态不是"可以顺便追加要求"的时机，想把新指令带进去必须等本轮结束或先取消。④ **中断是整组取消**：对等待中的一整组工具调用与审批一次性取消 ⇒ 部分响应没有意义，恢复后要按"整批重来"处理，不能假设其中某几条已经生效。⑤ **中断会吞掉未处理的排队消息**：中断前入队但还没处理的消息被跳过 ⇒ 重要指令不要在 interrupt 前后脚发送，否则静默丢失。⑥ **版本冲突的两种正确解法按场景分**：交互式先 GET 再带 version；CI 声明式同步**省略 version 让后写覆盖**——把交互式做法搬进 CI 会造成无谓的冲突失败，反之则会互相覆盖。
- 提升层：工作流 / 安全边界。触发词：中断不产生 error、宽限期强杀、等待态拒绝新指令、中断取消整组、中断吞掉排队消息、声明式同步省略 version、409 版本冲突先 GET。

## Cap68 写同一条记录不等于推进它的生命周期：维护类写入必须声明自己算不算「交互」（来源：docs.openclaw.ai `automation/cron-jobs/troubleshooting.md` 4,654B，2026-10-04 r413C 独立 curl 取 `.md` 原文实拉；与 §Cap57 定时任务三态 / §Cap60 中断不是错误 互补——那两条管"暂停恢复归档各自改变什么""中断在事件面上长什么样"，本条管"哪些写入有资格推进新鲜度"）
- **原文**：「Daily and idle reset freshness is **not based on `updatedAt`**」「Automation wakeups, heartbeat runs, exec notifications, and gateway bookkeeping **may update the session row for routing/status, but they do not extend `sessionStartedAt` or `lastInteractionAt`**」「For legacy rows created before those fields existed, OpenClaw can recover `sessionStartedAt` from the transcript JSONL session header when the file is still available. Legacy idle rows without `lastInteractionAt` use that recovered start time as their idle baseline.」
- **判据**：① **"行被写过"与"生命周期被推进"是两件事**——心跳、唤醒、通知、系统记账都会改同一行（路由/状态），但刻意不延长新鲜度字段；若把新鲜度定义成 `updatedAt`，一个后台心跳就能让会话永不过期。⇒ 任何"多久没动就归档/重置"的规则，必须显式列出**哪些写入算交互、哪些不算**；用"最后修改时间"当新鲜度等于把续命权交给噪音。② **同一个对象上要有两套时间语义并各自命名**：路由态的时间（什么时候被系统碰过）与交互态的时间（什么时候人/主体真的说了话）。混用后排查"为什么没过期"只能靠猜。③ **字段缺失时的回退基准要写清楚且优先从原始记录恢复**——旧行没有这两个字段时从 transcript 头恢复 `sessionStartedAt`，无 `lastInteractionAt` 的旧行用它当 idle 基线；⇒ 补字段的迁移不能默认"缺失 = 现在"或"缺失 = 永不过期"，两者都会成批改变既有对象的命运，必须给出可核验的恢复来源。④ 对 guild 的落点：共享记忆/交接/收件箱的 groom 与归档规则同理——后台 groom 自己写的时间戳不能算"这条还有人在用"；存活判定要挂在明确的交互字段上。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：写入不推进生命周期、updatedAt 不是新鲜度、sessionStartedAt、lastInteractionAt、心跳不算交互、groom 存活判定字段。

<!-- r424A 二次下沉 -->

## Cap66 昂贵召回路径必须由「意图匹配 + 廉价通道无强命中」双条件共同放行；检索方式的能力边界要写死（来源：docs.openclaw.ai `concepts/active-memory.md` 7,276B + `concepts/active-memory/how-it-works.md` 6,173B，2026-10-04 r412B 独立 curl 取 `.md` 原文实拉；与 §Cap64 会重置的通道 / §Cap32 只写不可读 互补——那两条管"数放哪条通道"与"存储形态"，本条管"什么时候值得为一次召回付出阻塞代价"）
- **原文**："The default `escalate` mode runs its blocking recall sub-agent **only when the message asks about the past and the deterministic memory lane found no strong trusted trigger match**"；表格 `escalate` | "Default. Run only for recall intent when lane 1 has no strong hit." / `always` | "Preserve the previous behavior and run on every eligible targeted turn."；"Flat retrieval is strongest for **direct fact matches** and **weaker on temporal and multi-session questions**."
- **判据**：① **升级条件要两条同时成立**：意图匹配（这轮确实在问过去）**且**廉价确定性通道没有强命中 ⇒ 只拿"廉价失败"当条件，会把冷启动、无关问题、以及本来就不该深挖的轮次全部拖进阻塞式子调用，成本由所有轮次平摊而收益只落在少数轮次上。② **检索层必须声明自己的能力边界**：扁平/向量检索强于直接事实匹配、弱于时序与跨会话问题（有 LongMemEval / PrefEval 这类基准量化该差距）⇒ 不写边界的检索层，用户感知到的"想不起来"会被误判成"根本没存过"，于是重复沉淀已有信息。③ **改默认不许删掉旧行为**：`escalate` 作默认、`always` 保留旧路径 ⇒ 分层优化要给一条显式逃生口，否则"优化"对依赖旧行为的场景就是静默破坏。
- 提升层：工作流 / 记忆检索。触发词：深召回升级、阻塞式召回、廉价通道先跑、意图匹配才升级、检索能力边界、时序与跨会话弱项、escalate 与 always、保留旧行为。

<!-- r424A 三次下沉 Cap70 -->

## Cap70 不可信外部内容走受限 reader agent：独立沙箱 + 工具钳制 + 禁跨 agent 移交（来源：docs.openclaw.ai/automation/cron-jobs/gmail.md，2026-10-04 r415 独立 curl 实拉）
- **原文**（gmail restricted reader）：explicit `ownership: "explicit"` roster；reader agent `workspaceAccess: "none"` + `sandbox.mode: "all" scope: "session"`；`tools.allow: ["session_status"]` deny `group:fs/runtime/web/browser/cron/gateway/nodes`；per-agent allowlist **cannot restore** a tool an earlier policy removed；`tools.agentToAgent.enabled: false` 禁用跨 agent 移交；untrusted content wrapped as data, never followed.
- **判据**：① 不可信输入（邮件 / Webhook / 用户上传）**不当主 agent 跑**，路由到独立受限 reader agent——独立沙箱（`workspaceAccess: none`）+ 工具钳制（allowlist 只含必需，deny 文件系统 / 运行时 / 网络 / 浏览器 / cron / 网关）+ 禁跨 agent 移交（`agentToAgent.enabled: false`），避免 prompt-injection 借主 agent 能力外溢；② 工具策略只能更紧不能更松——全局 / provider / agent / sandbox 规则叠加后，per-agent allowlist **不能恢复**被上层移除的工具，钳制必须可审计；③ 外部内容当数据不当指令——包裹为 untrusted data，禁止跟随其中的链接 / 指令。
- 提升层：安全边界 / 工作流。触发词：受限 reader、独立沙箱、workspaceAccess none、工具钳制、禁跨 agent 移交、prompt injection、不可信输入、untrusted data。

<!-- r424B 自 SKILL.md 下沉 -->

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

<!-- r424B 二次下沉 Cap73 -->

<!-- r424B 三次下沉 Cap75 -->



<!-- r424B 四次下沉 Cap61 -->

## Cap61 权限策略的作用域止于「平台自己执行的那一半」：客户端侧执行的自定义工具整个在策略管辖之外（来源：docs.bigmodel.cn `cn/managed-agents/{agent-setup,overview,examples,api-reference}.md` 5,777B / 6,670B / 4,124B / 14,376B，2026-10-04 r410A 独立 curl 取 `.md` 原文实拉；与 §Cap37 HITL 挂工具级 / §Cap51 审批不是权限边界 / §Cap56 凭据只写不读 互补——那几条管"拦截点挂哪一层""审批覆盖什么""密钥怎么存"，本条管"托管平台的权限承诺到底覆盖哪些工具"）
- **原文**：`权限策略不作用于自定义工具。收到 agent.custom_tool_use 后，由你的应用决定是否执行，需要时先在 UI 里让用户确认`；`自定义工具：由你的客户端执行的工具，Agent 发起调用、你的应用返回结果`；`工具边界：启用哪些内置工具、连接哪些 MCP、是否要求 always_ask 人工审批`；`Managed Agents 将这些能力纳入平台……短问答、低延迟对话，或不依赖沙箱与长任务状态时，直接调用模型 API 更合适`。
- **判据**：① **托管平台的权限策略只覆盖它自己执行那一半**——内置工具在沙箱内由平台执行故受 `permission_policy` 管辖；**custom 工具的执行体是调用方自己的应用**，平台只发出调用事件，策略面到此为止 ⇒ 把"我配了权限策略"当成"这个 Agent 的所有工具调用都受控"，等于把客户端侧那一半漏在外面。② **"工具边界"这条配置面的作用域要显式写清它不覆盖什么**：文档把工具边界列为调用方自决项，同时明说策略不作用于自定义工具 ⇒ 声明能力边界时，光列"管什么"会让人默认"剩下的也管了"。③ **客户端执行的工具，人工确认必须在客户端实现**——平台给的落点是"收到事件后由你的应用决定、需要时在 UI 里确认" ⇒ 这是 HITL 落点的分派：平台侧执行 → 平台侧批；客户端侧执行 → 客户端侧批，两端都要有，不能互相替代。④ **能力托管的边界同时是选型边界**：平台明确"不依赖沙箱与长任务状态时应直接调模型 API" ⇒ 托管带来的是循环/上下文/沙箱/密钥/落库/跨会话状态/用量七项，代价是把执行位置交给平台；只有托管方与自管方的**责任分界线**清楚了，这七项才是收益而不是黑箱。
- 提升层：安全边界 / 工作流。触发词：权限策略不作用于自定义工具、custom_tool_use、客户端执行、工具边界作用域、平台侧批 vs 客户端侧批、能力托管七项。

## §r425A-ag 下沉 Cap42–Cap45（r425-A 行数治理，原文+判据移至 KB，SKILL.md 留指针）

### Cap42（原文+判据）
- **原文**：「End-user credentials let workflows run with the credentials of the person who **triggers** them, rather than a fixed credential.」；「Each connection belongs to the user who made it: **only they can use it, and only they can see the data it returns**.」；「**Sharing shares the template, not a connection.**」；admin 侧「An admin can see that an end-user credential template exists and that it has connections attached... **That count is all they see.** They can't: View anything about individual connections / View a connection's secrets / Use anyone's connected account in their own workflows / See the redacted output of executions that ran on another user's connection」；「**Deleting the credential template deletes the whole credential, including every user's connection**, not just your own.」；触发器「let you require that the triggering user has permission to execute the trigger... A user without that role **can't connect their account**.」
- **判据**：① **执行身份决定数据归属，不是权限表决定**——同一条工作流、同一份凭据定义，触发者不同则读到的数据与可见面完全不同；设计共享能力时必须先回答"这次以谁的身份执行"。② **"共享能力"与"共享授权"必须拆开**：跨项目/跨人传递的是模板（能力定义），接收方必须自己完成连接；拿到模板不等于拿到别人已建立的授权。③ **管理权不含使用权**——管理员能看到"有这个模板、挂了几条连接"，且仅此一个计数；不能查看连接、不能读密钥、不能拿别人的连接跑自己的流程、也看不到别人执行里的原文（只看到 redacted）。写治理规则时把"看得见存在"与"用得了实体"列为两个权限位。④ **删除模板是级联动作且毁的是别人建立的授权**：删模板连带删除全部用户连接，依赖它的工作流在重建前停止解析 ⇒ 凡"父对象被删会带走子对象已建立的授权"的操作，删前必须给连接计数 + 显式告警 + 影响面清单。⑤ **连接动作本身也要过权限门**——没有执行角色的用户连账号都连不上，不是"能连上就能用"。

### Cap43（原文+判据）
- **原文**：「With `session.scope: "global"`, the selected agent still owns its session. The shared key `global` **does not merge different agents' conversations**… Session lists, model filters, previews, and sharing controls also retain the stored conversation's agent」；「Stopping with `/stop`, deleting, resetting, or archiving a session **cancels only that agent's work** for the selected conversation. Another agent's active turn and queued messages are preserved even when the agents use the same session key.」；「If multiple people can message your agent, enable DM isolation. Without it, all users share the same conversation context, so **Alice's private messages would be visible to Bob**.」；`dmScope` 四档 `main`（默认）/ `per-peer` / `per-channel-peer`（推荐）/ `per-account-channel-peer`；「Native catalog source IDs, Matrix room and thread IDs, and Signal group IDs are **case-sensitive**: IDs that differ only by case identify different conversations.」；incognito「keeps its session entry, transcript, and compaction state **in process memory instead of on disk**… expires 24 hours after creation or when the Gateway restarts… **Activity does not extend its lifetime.** Expiry stops active work and **deletes the session and transcript without an archive**」；「Incognito **does not restrict the agent's normal tools**. An explicit request to save information, or any tool-driven file write, can still persist data outside the incognito session store.」；「OpenClaw still records operational diagnostics and **content-free audit metadata such as HMAC references**」；「This protects them from storage and other gateway-mediated users, **not from the gateway owner or process operator**, who can always observe live sessions.」
- **判据**：① **会话键是路由标签不是合并指令**——同一个 key 下不同 agent 各自持有独立会话与排队消息；"共用一个会话"这类描述必须落到"某 agent 的这条会话"。② **取消/重置/删除的作用半径要写明是哪一个 agent**：一个停止动作只取消该 agent 的工作，同 key 下别人的回合照跑；没写半径的取消操作，用户会以为停掉了全部。③ **默认共享隐含单人假设**：DM 默认全部共享一条会话，多人场景不显式开隔离就等于把 Alice 的上下文给 Bob；隔离粒度给四档（发送者 / 渠道+发送者 / 账号+渠道+发送者），且配了**反向的归并且**（`identityLinks` 把同一人的多身份映射成一个 peer）——**隔离与归并是两个方向的两套配置，不是同一旋钮的两端**。④ **身份标识的大小写敏感性必须显式声明**：只差大小写的 ID 会分裂成两条会话与两份记忆，这在排查"记忆怎么少了一半"时是最难想到的一类。⑤ **隐私模式的边界声明要回答三个问题**：防谁（防存储与其他网关用户，**不防宿主/运维**）· 仍然落到哪里（工具写盘照旧、模型提供方仍处理消息、operational diagnostics 与 HMAC 类无内容元数据仍记）· 何时消失（24h 或重启，活动不延长，过期即删不归档）。缺任何一问，"开了隐私模式"都是错觉。

### Cap44（原文+判据）
- **原文**：`drop` 三档——「`summarize`（默认）：drop the oldest queued entries as needed, **keep compact summaries, and inject them as a synthetic followup prompt**」；「`old`：drop the oldest… without preserving summaries」；「`new`：reject the newest message when the queue is already full」；`cap` 默认 20，「Values below `1` are ignored.」；权限面「Gateway input **retains its authenticated operator and original scope ceiling** while queued or delegated to a child… other input waits in FIFO order **instead of borrowing the active or newest sender's permissions**」；「An accepted turn can continue after its request returns or its client disconnects. **That does not extend revoked device authority or permissions removed by a current operator role.** Subsequent actions still check the original source, including work held by an accepted child.」；并发「A lane-aware FIFO queue drains each lane with a configurable concurrency cap… CLI, embedded, and Codex runs **share the same session-key lane** (`session:<key>`). Each turn waits there before acquiring the session's execution claim, **so changing runtimes cannot start a competing turn**.」
- **判据**：① **队列溢出必须先选语义再谈容量**：三档分别是"丢旧的但留下摘要并注入合成追问"（默认，等于**内容被改写后再送达**）·"丢旧的无补偿"·"拒绝最新的"。默认档会改变消息内容，所以"收到过"与"原样收到过"不是一回事；验收队列行为时必须确认用了哪一档。② **排队与合并都不借权限**：输入在排队或被委派到子执行体期间始终携带自己的 operator 与 scope ceiling，不合资格的只能在 FIFO 里等，不会"搭便车"借到当前运行者或最新发送者的权限。③ **权限检查不只在准入时做一次**：已接受的运行在请求返回或客户端断连后仍可继续，但**被撤销的设备权限与被移除的角色当场生效**，后续动作仍回查原始来源——包括已经被子执行体接走的工作。⇒ 撤销必须作用于"在飞的"，只拦新请求等于没撤。④ **并发是两级预算而非一个数**：先抢**会话 claim**（同 session key 的 lane，换运行时也绕不过），再抢**全局/父级预算**（main lane 受 `maxConcurrent`，子 agent 用其 spawning session 的预算，swarm 用 group 预算）。⇒ 调"并发"前要先分清是卡在会话串行还是卡在全局预算，改错一层永远看不到效果。

### Cap45（原文+判据）
- **原文**：「Audit logs now record changes to **2FA enforcement** settings. Organization admins and owners can see: **Who enabled or disabled 2FA enforcement** / When they did it」；「Previously, expired OAuth connections required **creating and authorizing a new credential request each time**. Requesters can now ask recipients to **reauthorize OAuth connections directly from an existing credential request**」；可用性标注「Both features are available on the Enterprise plan」。
- **判据**：① **审计要记两类事件：违规事件与策略变更事件**——只记"谁没开 2FA"会漏掉更关键的一条：**谁把强制 2FA 关掉了**。改变规则比违反规则影响面更大，且通常只有极少数人有这个权限；凡是能被开关的安全策略，其开关动作必须进审计日志（谁 + 何时 + 从什么改成什么）。② **凭据过期应提供原地重授权通道**：过期即重建会不断产生新的凭据请求与连接，旧的连接面不会自动消失 ⇒ 累积出来的是一批无人清理的平行授权。续期（reauthorize）与新建（create）是两个动作，默认应走续期。③ **这类能力通常带套餐门槛**（Enterprise），写进共享规则时要连同前置面一起声明，避免"我们平台应该有"的误判。


## §r426A-ag 下沉 Cap18–Cap20（2026-10-05 r426-A 行数治理，原文+判据移至 KB，SKILL.md 留指针）

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


## §r427A-ag 下沉 Cap83 / Cap85（2026-10-06 r427-A 行数治理，原文+判据移至 KB，SKILL.md 留指针）

## Capability 83 — 守卫失败要按「谁不可判定」分极性：被检对象读不懂 ⇒ 阻塞；守卫自己没准备好 ⇒ 只警告继续；兼容窗口永不覆盖安全面（来源：api.github.com/repos/anthropics/claude-code/releases 96,622B，v2.1.289 changelog 一手命中，2026-10-05 r422-A 独立 curl 实拉；docs.openclaw.ai `gateway/protocol/versioning.md` 14,899B + `gateway/protocol/handshake.md` 18,434B，同轮独立 curl 取 `.md` 原文实拉逐串命中；消化 Qoder r418-Q-A 积压点）
- **实证**：Claude Code v2.1.289 原文「Fixed PreToolUse and PermissionRequest hooks **being skipped when matching them failed or the tool's input could not be serialized to JSON; the call is now blocked**.」；OpenClaw 原文「Device auth, pairing, scopes, command policy, and exec approvals are **unchanged by this compatibility window**.」；「Plugin-owned node ... because their hosted surfaces are **not part of the N-1 contract**.」；「None of these states triggers local fallback or automatic replay.」；handshake 侧「reports the negotiated role and the current socket's effective authorization scopes **even when no device token is issued**」。
- **判据**：① **守卫失败要分两种，默认极性相反**——失败原因是「被检对象无法解析/匹配不上」（输入不可序列化、载荷读不懂）⇒ 必须**阻塞**，因为"跳过"在效果上等于默认放行，守卫不存在与守卫放行是同一结果，这是安全默认极性的错置；失败原因是「守卫自身配置缺失或前置开关未开」（Cap81 那条）⇒ 可以只 warning 并让旧行为继续，因为被检对象没变、风险敞口没有扩大。**判据一句话：读不懂的是"东西"就拦，读不懂的是"规则"就降级。** ② **兼容窗口必须有"不被窗口覆盖"的显式清单**——N-1 版本协商只放宽协议版本，设备认证、配对、作用域、命令策略、exec 审批五面不随之放宽 ⇒ 任何"向后兼容/灰度共存"的设计都要同时声明窗口边界：哪些面进窗口、哪些面绝不进；只写"支持旧版本"而不写"安全面不降"的兼容承诺，等于把安全面默认划进窗口。③ **插件/第三方自有面不在兼容契约内**——托管面属于宿主协议契约，插件自有 hosted surface 不享受 N-1 ⇒ 依赖插件面的调用方不能假定它与平台同寿命，升级判定要按各自的契约分别算。④ **降级状态不触发本地兜底与自动重放**——旧版本态走显式处理，不本地兜底、不自动重放 ⇒ "兼容"不等于"自动替它跑一遍"，隐式重放会把一次失败放大成两次副作用。⑤ **协商结果回执独立于凭据发放**——即使未签发设备令牌，也要回报协商出的角色与生效作用域 ⇒ 生效权限的可见性不能绑定在"有没有拿到凭据"上，否则无凭据连接会成为观测盲区。
- **与既有能力分工**：Cap81 管「收紧型 flag 默认关、前置缺失时只 warning 旧行为继续」（守卫没准备好）；Cap76 管「控制声明要自带误读澄清」（声明怎么写）；Cap72 管「分层作用域只收窄不放大」（作用域叠加）；本条管**失败与兼容这两类"边界时刻"的默认取哪一侧**，并给出 Cap81 与本条的适用分界。
- 提升层：工具 / 治理。触发词：守卫读不懂就阻塞、跳过等于放行、兼容窗口不覆盖安全面、N-1 契约边界、插件面不在契约内、协商回执独立于令牌、不自动重放。

## Capability 85 — 认证只定「角色」，授权在每次调用上另判；应用内权限不是隔离边界，强隔离要在 OS 用户/主机层；等待式读取在返回前重检五要素（来源：docs.openclaw.ai/gateway/operator-scopes.md 39,492B，2026-10-05 r423-A 独立 curl 取 `.md` 原文实拉逐串命中；与 Cap72 分层作用域 / Cap83 守卫极性互补——那两条管"作用域怎么叠加"与"守卫失败站哪一侧"，本条管"认证之后还有一层授权"以及"这套东西的隔离边界在哪一层"）
- **实证**：官方原文「Operator scopes gate what a Gateway client can do **after it authenticates**.」「They are a control-plane guardrail inside one trusted Gateway operator domain, **not hostile multi-tenant isolation**. For strong separation between people, teams, or machines, **run separate Gateways under separate OS users or hosts**.」；「Operator RPC methods require the `operator` role. Node-originated methods require the `node` role.」；作用域表「`operator.admin` … **Satisfies every `operator.*` scope**」「`operator.write` … Also satisfies `operator.read`」；自作用域例外段「These methods **do not expose team secrets, mutate shared configuration, or grant write/admin scopes**.」；收尾「Identity, role, access grant, connection, and session visibility are **rechecked before returning awaited reads**.」
- **判据**：① **通过认证不等于获得授权**：连接进来只确定"我是哪一类客户端（角色）"，每个方法再按 scope 单独判 ⇒ 把"已认证"当"已授权"，等于把一次身份检查当成全会话通行证。**判据一句话：认证回答"你是谁"，scope 才回答"这一下能不能做"。** ② **应用内权限模型不能冒充隔离边界**：官方明说这套 scope 只是**同一信任域内**的控制面护栏、**不是对抗性多租户隔离**，要强隔离就在 OS 用户/主机层分开 ⇒ 设计权限前先声明威胁模型是"防误操作"还是"防恶意邻居"；声称防恶意而执行边界仍在同一进程/同一账号内，就是伪隔离（纸面边界在被攻破的第一刻一起失效）。③ **角色要互斥且在入口强制**：控制面方法与能力宿主方法分属两个角色，各自只能由对应角色发起 ⇒ 角色不互斥等于默认全能，"都是可信内部调用"是最常见的越权通道。④ **判定一个"只读"令牌是否真只读，要看高阶蕴含**：`write` 满足 `read`、`admin` 满足全部 ⇒ 宣称只读的凭据如果和更高阶凭据同源或可被同一调用方替换，它的"只读"只是标签。⑤ **自作用域例外必须自带四条不越权断言**：只操作自己的账号 + 不暴露团队密钥 + 不改共享配置 + 不授予更高 scope，缺一条它就不是"例外"而是提权后门。⑥ **异步/等待式读取要在返回前重检**：身份、角色、授权授予、连接状态、会话可见性五项在 await 之后重新校验 ⇒ 入口验一次 ≠ 出口仍成立，等待窗口里权限可能已被撤销或会话已不可见。
- 提升层：工具 / 治理 + 安全边界。触发词：认证不等于授权、连接角色、认证后的第二层授权、应用内权限不是隔离、OS 用户或主机层隔离、高阶蕴含低阶、自作用域例外、等待读前重检、await 后重校验。
