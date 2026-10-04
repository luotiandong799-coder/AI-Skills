

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
