---
name: mi-memory
description: 长期记忆治理（Memory Intelligence）。当任务涉及"该记什么/不该记什么"的判断、用户级 MEMORY.md 与模块记忆分层、跨会话记忆的写入/检索/去重、记忆容量与检索侧治理权衡、个人文件与隐私不入记忆、记忆可靠性与可恢复性、事实失效与双时态时间戳、按来源删除级联、记忆系统评测五能力、以及判断是否要固化长期规则时使用。是 13 模块中 MI 的载体。；记忆巩固效用评级（十技法四变量/熟悉感错觉/即时与延迟双栏/desirable difficulty）。检索即改写（再巩固窗口/可及性≠保真度/重整与消退两过程/分层抗改）。矛盾解决位置（写入侧四操作 vs 检索侧 ADD-only）·遗忘双机制（decay 降权 vs eviction 真删）·架构反转迁移清单；前瞻记忆与意图兑现（事件/时间线索·双成分四阶段·回顾记忆是内容底座·线索三特性·外部审计与取消意图）。交互记忆系统 TMS（记忆分布在人+外部 aid·元记忆 who-knows-what 目录·编码存储检索三过程 transactive·专长公开宣布才提升群体绩效·turnover 破坏目录）。检索诱发遗忘 RIF（检索是抑制性选择·Rp+/Rp−/control 三态·抑制说 vs 阻断说与独立线索裁决·稳健但带范式边界·换检索程序须双用例回归）。睡眠依赖系统巩固（突触巩固vs系统巩固两机制·SO-spindle-ripple顺序耦合定时·内源重激活强度预测巩固·TMR倒U与个性化·巩固周期性分期且NREM/REM分工存争议）。错误记忆与来源监控（DRM关键诱饵·模糊痕迹verbatim/gist双 trace·激活监测与来源监控失败·误导信息效应与DRM的verbatim反向作用·高置信≠真实须逐字锚点回归）。 定向遗忘两范式分离（item 编码+提取双因/list 提取抑制·accessibility≠availability 换线索验真删·直接抑制vs替代两策略）。 编码特异性检索（线索效力来自编码时共存语境而非语义相似度·情境效应主要是回忆现象须换线索验真删·线索过载与判别竞争限制匹配）。序列位置效应（首因=LTM复述/近因=STM双分离·延迟抹近因不动首因·呈现速率反向·agent按存储层分流验收）前摄/倒摄干扰（学习阶段竞争vs检索抑制RIF正交·AB/AC延迟自发恢复推翻即时覆盖·相似性倒U最危险）
version: "2.8.0"
module: MI
modules: MI,AI
---

# MI · 长期记忆治理（Memory Intelligence）

> 本技能是 13 模块中 **MI（记忆智能）** 的载体。完整经验日志（逐条带来源）在 D 盘实体：`D:\腾讯AI\WorkBuddy数据\module-memory\MI\MEMORY.md`（C 盘同名仅 junction 镜像）。关联子技能：`meta/knowledge-governance`、`meta/personal-ai-os`。

## 一、分层与边界

- 用户级 MEMORY.md = 纯指针索引 + 最高优先铁律；模块经验存 `module-memory/<模块>/MEMORY.md`，**不**挤进 MEMORY。
- 写入端不预筛、容量治理放检索侧：memory stream 时间驱动 append-only；写入时判"重不重要"会丢掉事后才有价值的上下文且不可重算。但须连成本量级一起报（多 agent 场景 cache tax 显著），不自动迁移轻量场景。
- 派生层（reflection/plan）必须回写同一条 memory stream 并参与检索，否则高层结论只在生成那一刻可用；观察与计划冲突只重规划"受影响段"，派生结论带指回原观察的指针。

## 二、写入纪律

- 落点判定：明确要长期记住且与项目无关的 → 用户级 MEMORY.md；按所属技能 → 对应模块文件（条目标「日期｜来源技能｜结论｜证据」）。
- 个人文件 / 隐私 / 系统核心 / 私钥：**永不**进记忆，优先回收站而非永久删除。
- 全局自定义指令无写入存储：勿改 leveldb。
- 声称架构组件"必要"须给逐项消融证据，不能只列三件套清单；可行性结论须连成本量级一起报。

## 三、触发与协作

- 何时加载：要固化一条长期规则 / 纪律前；跨会话需要回忆既往决策或经验前；用户说"记住…"时；判断某信息该进哪一层记忆时。
- 与 AI（自适应）：记忆是策略优化的输入；与 KI（知识）：知识组织与记忆治理交接在"什么该沉淀为可检索知识"。

## 四、记忆架构方法论（实拉，2026-11-08）

> 来源：`meta/personal-ai-os` 经 arXiv 2304.03442 摘要一手 + CSDN 深读 + 中科院讲义；落地 `meta/personal-ai-os/references/knowledge-base.md` §r713A。

- **（A-1）写入端不预筛、容量治理放检索侧**：memory stream 是时间驱动的 append-only 日志；在写入时刻判断"这条重不重要"会丢掉那些事后才显出价值的上下文，且不可重算。代价侧须连同量级一起报（实测 25 agents / 2 天 / 数千美元 token），因此不自动把重载体迁移到轻量场景——先看成本是否真的不可承受。
- **（A-2）派生层必须回写同一 stream**：reflection / plan 这类高层结论必须存回同一条 memory stream 并参与后续检索，否则"结论只在生成那一刻可用"；当新观察与旧计划冲突时，只重规划"受影响段"，派生结论带一个指回原观察的指针，便于溯源。
- **（A-3）"必要"须消融证据**：声称某架构组件"必要"，必须给逐项消融（去掉它系统是否真的崩）；只列三件套清单不足以证明。可行性结论必须连带成本量级，否则无法判断是否值得做。

## 五、事实的时间语义、溯源与评测（实拉 r732B，2026-11-11）

> 来源：arXiv 2410.10813《LongMemEval》v2（ICLR 2025，WebFetch 200 摘要逐字 + 搜索结果回读 PDF §3.2 全文）；Zep 官方 `help.getzep.com/v3/facts.md`（WebFetch 200 全文）；Zep 官方博客《How Zep tracks provenance in agent memory》（Daniel Chalef，2026-07-14 / 更新 07-24，WebFetch 200 全文）；`getzep.com/ai-agents/temporal-knowledge-graph`（四时间戳表）；gamgee.ai / sentra.app / aimemoryworks.com（五能力与题型计数交叉）。四独立域交叉。

- **（r732B-1）记忆是五种互不替代的能力，"召回率"只是其中一维**：LongMemEval 定义 Information Extraction / Multi-Session Reasoning / Knowledge Updates / Temporal Reasoning / Abstention 五能力、七题型；**Abstention 不是独立题型**，而是从其他题型改写出 30 道 false-premise 题（ID 带 `_abs` 后缀）；KU 的官方 judge 允许答案里提到旧值，只要**给出的**是新值。⇒ 评估记忆系统必须按能力分桶报分，单报总准确率会把"会检索但不会更新 / 不会弃答"掩盖掉；ollama/向量库同时召回新旧两值即典型 KU 失败。arXiv 摘要逐字：商业助手与长上下文 LLM 在持续交互记忆上出现 **30% accuracy drop**。
- **（r732B-2）事实失效是双时态四时间戳，不是删除或覆盖**：Zep 每条事实（边）带 `created_at`（系统何时学到）/ `valid_at`（世界中何时成立）/ `invalid_at`（世界中何时失效）/ `expired_at`（系统何时学到失效）；现实时间与数据库事务时间**两条轴**，故能同时答"现在是什么"与"2024-06 时是什么"；被否证的事实**留在图里带完整历史而非删除**。官方逐字限定："The fields do not establish that the source content or the derived fact is true" ⇒ 时间字段只是系统推断的检索边界，**不是真值证书**。与 `meta/knowledge-governance` 的 `valid_until` 三分法互补：那条给"保留双条 / recency 加权 / 显式失效"三种处置，本条给四字段的可实现模型与"字段不等于真值"的边界。
- **（r732B-3）溯源是 episode 集合不是标量 source_id，删除按"剩余支撑"级联**：LLM 抽取使「一事实来自多源 / 实体合并 / 事实失效」三种变异让单个 `source_id` 失效（官方逐字 "A scalar `source_id` on the fact cannot represent any of this"）。⇒ 合并实体取两侧 episode 关联的**并集**（丢一侧会静默孤儿化事实）、事实保留每一个 parent（再确认或否证都追加而非覆盖）、失效记录是哪个 episode 何时 superseded。混合信任父集（2 verified + 1 未验证）的判定**按用例选 ANY / ALL 谓词，不能硬编码进存储**：过敏标记怕假阴性（任一 verified 即可甚至无条件放行），"已签同意书"怕假阳性（须全部 verified）——同图形状、相反策略。`remove_episode` 只在**没有任何剩余 episode 支撑**该事实时才删；两条限制：删 episode **不重生成**其他 episode 仍支撑的节点摘要、**已失效的事实保持失效**。⇒ 删除是"支撑度归零"判定，不是"删了源就删所有派生"。

## 六、应用运行规则（跨任务，2026-10-02 强制）

- 不自动开关：我打开的应用（含微信、网易云）保持运行，禁自动关闭 / 反复开关；开关只按用户明确指令。
- 浏览器默认 Edge：`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`。
- 任务结束**绝不**主动关闭我打开的浏览器 / 应用 / 窗口 / 文件，除非用户明说关。

## 七、用户与环境背景（写入记忆前先核对）

- 用户：供应链本科（西安欧亚）；Agent 名称 yt；真实 AI 应用仅 WorkBuddy + 豆包；不装全局技能。
- 学习轮不碰已删 4 类：重构 / 拆单 / 多媒体取证 / 扩展构建。
- 全局自定义指令无写入存储（勿改 leveldb）；workspace 级 AGENTS.md 不自动继承全局，发现缺失就补 workspace 级。
- 技能入库偏好：拒"太专业 / 过小众"，以实用常用能落地为准。

## 八、来源

- arXiv 2304.03442（memory stream / generative agents 一手摘要）
- CSDN 深读 + 中科院讲义（memory 容量治理 / 检索侧口径）
- 落地：`meta/personal-ai-os/references/knowledge-base.md` §r713A A-1 / A-2 / A-3
- r732B：arXiv 2410.10813（LongMemEval 五能力 / 七题型 / 30% drop）+ Zep 官方 v3 facts.md（四时间戳 / 字段不证真值）+ Zep 官方 provenance 博客（episode 集合 / AND-OR 谓词 / remove_episode 级联）+ getzep temporal-knowledge-graph + gamgee / sentra / aimemoryworks 交叉

## 九、记忆/知识库的对抗验收口径（r740B 实拉，2026-11-14）

> 与既有分工：豆包自留地已覆盖**投毒谱系 + 写时 HMAC 门控 + 隔离机制本体**，本条只取**验收口径**（报什么指标、抽检能不能抓到、防御怎么测才算过），不搬机制、不往那两个文件落地。与 §五 LongMemEval「五能力分桶报分」互补：那条测**功能正确性**，本条测**对抗下的可信性**，两条并行不合并。
> 来源：arXiv 2407.12784《AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases》（Chen/Xiang/Xiao/Song/Li，2024-07-17 提交）abs 页与 HTML v1 全文 WebFetch 200 逐字；PDF 摘要与 Figure 1 快照逐串复核；mlsanity / scholarfeed / SerialsSolutions 元数据交叉（引文数不计结论）。≥2 独立形态交叉。

### 9.1 ★ 投毒落在检索层，不落在模型权重
官方逐字："AgentPoison requires no additional model training or fine-tuning"；触发器生成是 constrained optimization，把带触发的实例映射进 "a unique region in the embedding space"（compactness / target generation / coherence 三损失联合）；"high ASR even when we inject only one instance in the knowledge base with a single-token trigger"；投毒率 <0.1%。
- 判据：验收对象是**记忆/知识库的写入面与检索簇**，不是微调记录；「我没重训模型」不构成记忆可信证明。换 embedder 也不能当清除——官方逐字 trigger "can be transferred to effectively attack other types of RAG embedders"。

### 9.2 ★ 必须 ASR / ACC 双栏并报，且抽查式抽检在结构上抓不到
官方逐字：平均 ASR ≥80%、benign 性能影响 ≤1%；Introduction 另给 "82% retrieval success rate and 63% end-to-end attack success rate"——**检索命中率 ≠ 端到端行动成功率**，是两个指标。
- 判据：只跑 ACC（正常问答准确率）的记忆评测会显示「一切正常」，ASR 与 ACC 必须同表并报且分开标注分母；<0.1% 投毒率意味着按常规比例抽检几乎必然漏检 ⇒ **「抽查几条记忆没发现异常」不可作为安全验收项**，须改成针对「异常紧凑嵌入簇 + 触发词组合」的定向扫描。

### 9.3 ★ 常规文本防御通过 ≠ 安全验收通过
官方逐字："evasive to potential defenses based on perplexity examination or rephrasing"、"resilient to diverse augmentations"。
- 判据：不能只在一个 embedder 上跑一遍困惑度/复述过滤就判安全；防御有效性须按「触发词 × 嵌入簇 × 多个 embedder」的联合面测，并把触发器可迁移写进威胁模型。与 §五 r732B 的 episode 集合溯源互补：溯源管「这条事实从哪来」，对抗验收管「检索行为有没有被改写」。

**提升层**：工作流（记忆系统上线/巡检验收表）。触发词：AgentPoison、检索层投毒、unique embedding region、compactness loss、single-token trigger、ASR-ACC 双栏、poison rate <0.1%、perplexity examination、rephrasing、embedder 迁移、对抗验收。
**来源**：arXiv 2407.12784 abs + HTML v1（2026-11-14 WebFetch 200 逐字）+ PDF/Figure 1 快照 + 三处元数据交叉；`retrieval success rate` / `compactness loss` / `single-token trigger` / `evasive to potential defenses` / `no additional model training` 全库 0 命中 ⇒ 净新（投毒机制本体命中全在豆包自留地，按 r739 先例只取元层）。

## 十、实体解析与未解矛盾的治理口径（r744B 实拉，2026-11-14）

> 与 §五 r732B（episode 溯源：事实从哪来）、§九 r740B（对抗验收：检索行为有没有被改写）分工：本节管「两次抽取指向同一实体吗」与「两条事实互相打架时系统放不放行」。≥3 独立域一手交叉。

### 10.1 ★错误合并是一次写入污染多条后续答案，故身份判定必须先于相似度、先于作用域
Supermemory 官方逐字：「a **mistaken merge can attach correct facts to the wrong entity and contaminate many later answers**」；「A display name is useful for reading but **usually insufficient as the only identity key**」；「**Do not merge across tenant or workspace boundaries** just because names and descriptions match. **Authorization scope should constrain candidate matches before semantic similarity is considered**」。ContextOS 官方并列「Entity-resolution **false positives** merge two real-world entities and corrupt downstream traversals」为已登记 failure mode。
- 判据：解析流水线顺序固定为「**作用域 / 稳定源 ID → 归一化名与别名精确匹配 → 模糊 → 语义嵌入**」，语义相似放最后而不是第一；同一名字的两人、改名项目、多别名组织、复用邮箱各写专门用例；「**Measure incorrect merges and missed matches independently; they have different consequences**」——错合（污染）与漏配（碎片）分开计数，不可合报一个 F1。

### 10.2 ★解析是三态不是二态，「不确定」必须是一等可留痕对象
Neo4j 官方 NAMS 逐字：每个新抽取实体走 **type-strict resolver cascade**——「first *exact* match on normalized names and aliases, then *fuzzy* matching (**Levenshtein, Jaro-Winkler, token-sort**), then *semantic* match on embeddings」；「**High-confidence matches are auto-merged; clear non-matches become new nodes; the ambiguous middle band is written as a SAME_AS edge marked pending and surfaced here in the review queue**」；置信度低于**可配阈值**才转人工，面板分 pending / confirmed / rejected 三计数，每行带 source、target、confidence 与 flag 出它的方法（示例「92% via fuzzy」）。Supermemory 同向：「**Keeping two unresolved candidates can be preferable to confidently combining them**」、「An **inferred** match should remain distinguishable from a **confirmed** one」并留足 provenance 供新证据到达时重访。
- 判据：二值 resolver 会把中间带强行并掉或强行拆开 ⇒ 验收必须查「第三态是否真实存在、阈值是否可调、每行是否记了 method 与置信分」；另 NAMS 写入是**异步管道**（store 立即返回，抽取/嵌入/去重/压缩在 memory:events 等 stream 上跑，`queue lag = 0` 才算图谱追上写入）⇒ 写后立刻读到的「没重」可能是**尚未解析**而非判定不重，验收要等 lag 归零或显式声明未结算。

### 10.3 ★矛盾未解即阻断提交，图只描述分歧、不授予模型裁决权
ContextOS 官方：同一 `(subject, predicate)` 上两条边断言冲突事实 ⇒ 检索 bundle **返回两条**并附 **EvidenceConflictMarker**（点名冲突 evidence refs、受影响的 decision requirements、resolved/unresolved 状态）；逐字「**An unresolved conflict is never silently ranked away**」，编译器把它带进 EvidenceGate、将 compiled view 标 **insufficient** 且保持 **`commit_allowed: false`**；resolved 状态必须「name a **resolution_ref** and the selected evidence refs so replay can reconstruct both the discarded branch and the rule or accountable review that selected the winner」；逐字「**The graph detects and describes the disagreement; it does not grant the model authority to resolve it**」——裁决只归确定性源优先级规则、新权威读、或其决定本身记为证据的具名复核人。Neutron 官方独立一手：矛盾「remains **unresolved until** an automatic, agent, or human resolution is recorded」，且「**stays within the Scopes of the claims that disagree**. A caller sees it, and can resolve it, **only when acting for every one of those Scopes**」；跨 Scope 解析须 `scopeIds` 覆盖全部；tombstone 从当前读移除但**队列 / 缓存 / 归档 / 压缩不得把它复活**。
- 判据：记忆系统验收须含两项新门——① 存在未解矛盾时下游动作是否被阻断（而非取置信度高的那条）；② 裁决证据链能否重放重建被丢弃分支；可见面与可解面都要按 claims 的 Scope 交集收窄。另 Supermemory 逐字「**A simple rename is different from a split: changing the label does not repair facts attached to the wrong subject**」「**Inspect downstream answers after correcting the identity mapping, not only the graph's visual appearance**」⇒ 错合修复单位是**拆分 + 按来源重挂关系与派生记忆**，验收看下游答案，不看图谱画面对不对。

**提升层**：工作流（记忆系统上线/巡检验收表）/ 安全边界（可见与可解按 Scope 交集）。触发词：entity resolution、type-strict resolver cascade、Jaro-Winkler、SAME_AS pending、HITL Resolution、queue lag、EvidenceConflictMarker、commit_allowed、resolution_ref、unresolved conflict、scope 交集、rename ≠ split、incorrect merges vs missed matches。

**来源**：`https://neo4j.com/blog/genai/a-tour-of-the-neo4j-agent-memory-service-nams/`（William Lyon，2026-06-23，WebFetch **200 全文逐字**）+ `https://supermemory.ai/blog/entity-resolution-agent-memory-graphs`（Shardul Mane，2026-07-20，WebFetch **200 全文逐字**）+ `https://contextosai.com/docs/foundations/knowledge-graph`（官方 Knowledge Graph 规范，WebSearch 快照逐字）+ `https://neutronai.dev/docs/fundamentals/knowledge-decision-intelligence` 与 `https://neutronai.dev/docs/get-started/api`（官方，WebSearch 快照逐字，含 `GET /v1/contradictions`、`POST /v1/contradictions/resolve`、bitemporal `validAt`/`knowledgeAt`）。四域交叉；厂商立场逐条登记，仅取可迁移判据。
**判非**：`entity resolution` / `EvidenceConflictMarker` / `commit_allowed` / `Jaro-Winkler` / `resolution_ref` / `false merge` / `HITL Resolution` / `POLE` / `source-priority` 全库 `SKILL.md` **0 命中**；`contradiction` 2 命中在豆包自留地（`defaults/wb-context-compressor`、`engineering/wb-execute-discipline`）、`tombstone` 2 命中在 `engineering/wb-release-maintain` / `engineering/wb-skill-authoring`（发布与技能生命周期墓碑）、`alias` 6 命中为通用别名语境，均非「记忆矛盾裁决」，登记不复用 ⇒ 净新。豆包自留地 **WB 0 落地**。A/C 两轮结论一律不复用。

## 十一、记忆巩固的效用评级：常用技法不是有效技法，验收必须测「延迟保持」（2026-11-15 r747C 实拉，3 独点）

> 适用：判断一条记忆/复习/沉淀机制是否真的有效、设计记忆系统的验收口径。与 §五（五能力分桶）、§九（对抗验收双栏）、§十（解析与矛盾治理）互补：前述管「能力有哪些 / 安不安全 / 结构对不对」，本节管「怎么证明一种记忆干预值得保留」。

### 11.1（r747C-1）★十种技法按四个变量维度评效用，只有 2 项 high、5 项 low；「大家都在用」不构成有效性证据
Association for Psychological Science（APS）官方《Which Study Strategies Make the Grade?》（John Dunlosky，2013-01-10）全文逐字：「review the scientific evidence for **ten learning techniques**」「two strategies — **practice testing and distributed practice** — made the grade, receiving the **highest overall utility rating**」「In contrast, **five of the techniques received a low utility rating** … including **summarization, highlighting and underlining, and rereading**」「I was shocked that some strategies that students use a lot — such as rereading and highlighting — seem to provide **minimal benefits**」「By just **replacing rereading with delayed retrieval practice**, students would benefit」；报告全名与出处逐字「*Improving Students' Learning With Effective Learning Techniques: Promising Directions From Cognitive and Educational Psychology*」，《Psychological Science in the Public Interest》2013 年 1 月号，作者 Dunlosky / Rawson / Marsh / Nathan / Willingham；并自陈边界「will **not be a panacea** … they will benefit **only students who are motivated and capable of using them**」。BrainStrata 逐字补评级框架：Dunlosky 等「evaluated each against **four categories of variable: the learning conditions, student characteristics, the type of material, and the outcome being measured**」，三档为 high（practice testing / distributed practice）、moderate（elaborative interrogation / self-explanation / interleaved practice）、low（含 summarization / highlighting / rereading）。
- **判据**：① 记忆治理引入「**技法效用分级**」而不是「有没有做」：反复重读日志、划重点、写摘要属 low，**主动检索（先回忆再对答案）与分散复现**才是 high；新增机制先归到这一档再谈是否值得常驻。② 评级不是单一效果量排序，而是**四格声明**（什么学习条件 / 对谁 / 什么材料 / 测什么结果），任何「X 提升记忆 N%」若不写这四格按 §九 ASR/ACC 双栏精神判为不可比。③ APS 自陈「非万灵药、只对有动机且会用的人有效」⇒ 迁移到 agent 时不得把人类学习结论直接当工程事实（外部内容信任边界，rules/08 §五），只取可迁移的**验收口径**，不照搬教学场景结论。④ 与 rules/07 §九「晋升三门 / 收益门」分工：那两条管「该不该晋升成技能」，本条管「怎么安排复现才产生保持」。

### 11.2（r747C-2）★熟悉感错觉：即时表现与延迟保持分离，写后立刻读得出来不算「记住了」
BrainStrata 逐字「**Rereading produces familiarity, which students mistake for learning**. Highlighting feels active and productive. But neither requires the **effortful retrieval that produces durable memory**」「Students walk away from a rereading session **feeling prepared. The knowledge is not there when the exam begins**」；「Roediger and Karpicke's 2006 study … students who **tested themselves** on material significantly outperformed those who simply reread it, **particularly when tested a week or more later**. The size of the advantage **increased as the delay between study and test grew**」；规模证据逐字「A 2021 meta-analysis by Yang and colleagues reviewed **222 classroom studies involving 48,478 students** … raised academic achievement by an average of close to half a standard deviation (**g = 0.499**)」；Sage 期刊《Online Study-Aids…》摘要逐字补机制：practice testing「provides students with **metacognitive knowledge of what they know and which topics need further study**」，且「**even more effective when it is accompanied by feedback involving the correct answer** … feedback helps them to identify misunderstandings and prevents that they **persevere in making these errors**」。
- **判据**：① **写后立刻检索命中率不是记忆质量门**：它与延迟保持可分离，甚至反向（练得越顺，长期越差）。验收固定加一条**延迟 / 跨会话**复现测试，并报「即时 vs 延迟」两栏。② 复现动作必须是**先回忆再对答案**（retrieval），不是把原文再读一遍；「我刚看过所以记得」是熟悉感错觉。③ **检索必须配正确答案反馈**：无反馈的自测会把错误答案固化（perseveration），与本仓 rules/07 §十「§10.4 写入后验证」「禁缓存错误/未完成/临时态」同向。④ 与 §九「ASR/ACC 双栏并报」分工：那条管投毒下的安全与功效双栏，本条管**测量时点**双栏；与 §五 LongMemEval 五能力分桶分工：那条管能力种类，本条管每类能力的测试离写入多远。

### 11.3（r747C-3）★desirable difficulty：练习期更费力的安排长期保持更好；调度不许按「当场顺」优化
BrainStrata 逐字「Cepeda and colleagues' 2006 meta-analysis of **317 studies** found that **the same total amount of practice** produces significantly stronger long-term retention **when spread across multiple sessions** than when concentrated in a single block」「Students feel like they remember material better immediately after an intensive single session, and **they are right in the short term** … they will **underperform the same student by the time the exam arrives**」「**The interval is part of the intervention**」；交错证据逐字「In the largest classroom study on this question to date, Rohrer, Dedrick, Hartwig and Cheung (2020) randomly assigned **787 students across 54 classrooms** … The interleaved group outscored the blocked group by a large margin at the follow-up test, with an effect size of **d = 0.83**」「when problems are mixed, students must **identify which strategy to use before they can apply it**」「Students consistently rate interleaved practice as **more difficult** than blocked practice. Cognitive psychology calls this a '**desirable difficulty**'」。Psychology Today（Gurung 访谈 Dunlosky）与 Structural Learning 两域交叉确认三档划分，并逐字「Re-reading … **produces familiarity, which students mistake for learning**」「**the strategies students reach for most commonly are largely the ones the evidence rates as least effective**」。
- **判据**：① 记忆巩固调度按**延迟保持**选，不按练习期流畅度：把同类经验一次性连跑 N 轮（blocked）在当轮看着更顺，跨会话复现更差；分散到多个会话、并与异类经验交错，能让「何时该用哪条经验」也被练到。② **间隔本身是干预的一部分**，「总次数相同」不构成等价（317 研究 meta 明确同总量下分散更优）⇒ 自动化调度不能只数执行次数，要记录间隔分布。③ 交错练习在练习期评分更低、主观更难，这是 desirable difficulty 不是退化；若把「本轮主观顺 / 当场答对率」当优化目标，会系统性地选错机制。④ 与 `meta/agent-evolution` 的实验设计结论（CUPED / 区间变窄）分工：那条管怎么测效应更省样本，本条管测的**因变量该是延迟保持**；与 `meta/knowledge-governance` / 豆包自留地已落的 FSRS / Ebbinghaus 复习调度算法**不冲突且本轮不复用**（详见判非）。

**提升层**：记忆治理 / 验收协议 / 学习机制设计。触发词：效用评级四变量、high utility 只有两项、familiarity illusion、即时 vs 延迟双栏、retrieval practice 配反馈、desirable difficulty、间隔是干预的一部分、交错 vs 分块、别按当场顺调度。

### r747C 来源与判非（2026-11-15 实拉，逐字核验）
- `https://www.psychologicalscience.org/news/releases/which-study-strategies-make-the-grade.html`（**Association for Psychological Science 官方**《Which Study Strategies Make the Grade?》，2013-01-10；原查询 `?p=82014` 由 WebFetch 规范化到现址）— **WebFetch 200 全文逐字**：十技法、两项 highest overall utility（practice testing / distributed practice）、五项 low（summarization / highlighting and underlining / rereading）、「minimal benefits」「replacing rereading with delayed retrieval practice」、报告全名/期刊/五位作者/2013 年 1 月号、Roediger III 社论、非万灵药边界。**第一独立域（学协会官方一手）**。
- `https://brainstrata.com/blog/what-the-research-says-about-effective-revision-strategies`（BrainStrata《What the Research Says About Effective Revision Strategies》，Owais Bagwan，2026-07-02）— **WebFetch 200 全文逐字**：四变量评级框架、三档划分、熟悉感错觉段、Roediger & Karpicke 2006 延迟优势随间隔增大、Yang 2021（222 研究 / 48,478 学生 / g=0.499）、Cepeda 2006（317 研究）、Rohrer 2020（787 学生 / 54 班 / d=0.83）、desirable difficulty、EEF 元认知七个月、文末六条完整文献著录。**第二独立域（教育咨询机构一手，商业立场登记，不作唯一来源）**。
- `https://journals.sagepub.com/doi/abs/10.1177/1475725720964761`（Sage Journals《Online Study-Aids to Stimulate Effective Learning in an Undergraduate Psychological Assessment Course》）— **WebSearch 摘要逐字**：practice testing 三机制（retrieval / metacognitive knowledge / forward testing effect）、「even more effective when it is accompanied by **feedback involving the correct answer**」「prevents that they **persevere in making these errors**」、Johnson & Kiviniemi 2009 的 64% 完成率、Schwieren 2017 19 项 meta。**第三独立域（同行评审期刊摘要）**。
- `https://www.psychologytoday.com/us/blog/the-psychological-pundit/202008/studying-through-the-pandemic-tips-from-cognitive-science`（Gurung 访谈 Dunlosky，2020-08，含 PSPI 14(1) 4–58 doi 10.1177/1529100612453266）与 `https://www.structural-learning.com/blogcategories/revision`（Structural Learning《Revision》，Updated for 2026，六策略效用表）— **WebSearch 快照逐字**，三档划分与「re-reading produces familiarity」交叉确认。**第四、五独立域（科普/教学立场登记）**。
- **判非（关键换道）**：`Ebbinghaus` / `FSRS` / `spaced repetition` / `retrievability` / `forgetting curve` 在 `defaults/wb-context-compressor`（**豆包自留地**）与 `meta/knowledge-governance` 已有命中 ⇒ **本轮不碰复习调度算法、参数与遗忘曲线公式**，改取「十技法效用评级框架 + 四变量口径 + 即时/延迟测量时点 + desirable difficulty」这一**验收协议层**，与已落的调度算法是互补而非重复。窄串全库 `SKILL.md` 精确扫描（97 文件）— `utility rating` / `low utility` / `practice testing` / `distributed practice` / `retrieval practice` / `familiarity` / `desirable difficulty` / `delayed retention` / `metacognit` / `spacing effect` / `Dunlosky` / `Yang` / `Cepeda` / `Roediger` / `Rohrer` **全 0 命中**；`interleav` 3 命中在豆包自留地、`engineering/wb-execute-discipline`（豆包自留地）、`meta/agent-evolution`（交错实验次序，异命题），登记不复用。与本技能 §五（LongMemEval 五能力）、§九（AgentPoison 双栏）、§十（NAMS 三态与矛盾阻断）结论均不复用；**豆包自留地 WB 0 落地**。A/B 两轮信源域与结论不复用。
- **未采纳**：各 meta 分析的具体效应量数值（g=0.499 / d=0.83 / 七个月）仅作 2026-11-15 二手转述快照登记，**未核原始论文全文**，不作为工程事实写入判据；EEF 工具包、GCSE / 课堂组织、教师激励设计、Anki/SM-2 算法参数属教育与产品实现细节，只取「测量时点 + 效用评级 + 难度反向」三条可迁移验收口径。人类被试结论迁移到 agent 记忆按 rules/08 §五作待验证假设处理。

## 十二、检索即改写：再巩固窗口、置信度与保真度反向（MI · r751A 2026-11-15 实拉，四独立域交叉）

> 记忆不是只读档案。**每一次取回都可能重写原始痕迹**。与 §五（五能力评测/双时态/episode 溯源）、§九（AgentPoison 对抗验收）、§十（实体解析三态）、§十一（巩固技法效用）分工：本条管「读取动作本身对原始条目的污染」。

### r751A-1 ★ 取回不是回放，是打开一次可写入窗口
科普中国《重整记忆》逐字「**记忆检索是一种动态过程，它可以加强或改变记忆**」「**对原始记忆的回忆是启动重新整合的关键事件**」「检索会引发一波蛋白质合成的浪潮，而这需要重新整合记忆」「检索后的内存重新整合可以用于更新或将新信息集成到长期记忆(LTMs)中」；psychprofile.io 逐字 "**Every time we access a stored memory, we do not simply play back a static recording but rather reconstruct the event from fragmented pieces**" / "**Remembering is less like opening a file and more like editing a document, saving over the old copy each time**" / "Each recall reactivates a hippocampal-cortical ensemble and opens a **brief reconsolidation window** in which the memory can be updated by the current context, goals, and emotion"。
- **判据**：① 「读出来→重新摘要→写回同一条」**不是无损整理**，是把当前上下文/目标/语气写进了原始痕迹 ⇒ 原始 episode 必须 append-only 且不可被派生视图覆盖，派生结论另存并带指回原条的指针（与 r713A「派生层回写同一条 stream」互补：那条保证派生可检索，本条保证原始不被改写）。② 验收固定问「原始版本还能按位置取回吗」，不能则判不可逆污染。③ 高频被召回的条目恰是累积漂移最多的条目，须按原文锚点周期回核，不能因「常被用到」判为可信。

### r751A-2 ★ 置信度上升与客观准确率下降可以同时成立
psychprofile.io 对照表逐字 "**Confidence**：Accuracy and confidence should track closely ⇒ **Confidence can rise while objective accuracy falls**"；"**Repeated retrieval improves accessibility more than fidelity**"；"**Delay increases reconstruction and susceptibility to distortion**"；"As a person recalls an event multiple times, small inaccuracies introduced during each reconsolidation can **accumulate, increasing confidence in details that never actually occurred**"；"**fluency can be mistaken for accuracy**"。
- **判据**：① 记忆质量门禁用「召回流畅度／被引用次数／主观确定感」当证据——三者提升的是**可及性**不是**保真度**。② 报告固定「即时可及性 vs 延迟保真度」双栏（与 §十一 r747C 熟悉感错觉分工：那条管**学习技法**的即时/延迟分离，本条管**同一条记忆跨多次取回**的漂移）。③ 延迟越长、复述次数越多越依赖重构 ⇒ 长间隔后的回忆须回原文核，不能充当原始事实的新证据。

### r751A-3 ★ 重整与消退是两个相反过程；要点层抗改、来源与周边细节易损
科普中国逐字「记忆检索可能会启动两个**潜在的可分离但相反的过程：重新整合和灭绝**」「**简短的提示会导致重新整合，而更长的提示会导致记忆的消失**」；psychprofile.io 逐字 "**strong gist and schema-based details resist change, while peripheral and source details are more vulnerable**" / "The result is a memory that remains recognizably the same event but **carries new retrieval history**"；科普中国《脑部的记忆之道》快照逐字「每次从大脑中提取同一事件的记忆时，其内容都可能发生细微调整」。
- **判据**：① 记忆更新策略按层分开：**要点/图式层**抗改可低频复核，**来源、时间、周边细节层**最易漂移须硬锚点（§五双时态四时间戳、episode 溯源正是落在这层）。② 「更新失败」不等于「没变化」——可能走了消退方向；提示/触发的**持续时长**是决定走向的变量，一次召回的效果不能只按「有没有命中」二分。③ 人类被试的神经机制迁移到 agent 记忆按 rules/08 §五作**待验证假设**，只取「读取即可能写入／可及性≠保真度／分层抗改」三条可机检口径，不引入蛋白质合成等生物实现。

**提升层**：记忆治理 / 验收协议。触发词：reconsolidation、再巩固、检索即改写、editing a document、可及性≠保真度、confidence vs accuracy、gist 抗改而 source 易损、重整与消退两过程、提醒时长决定走向、原文锚点回核、append-only 原始 episode。

### r751A 来源与判非（2026-11-15 实拉，逐字核验）
- `https://www.kepuchina.cn/article/articleinfo?business_type=100&classify=0&ar_id=241072`（**科普中国《重整记忆》**，上传时间 2021-12-31；**WebFetch 200 全文逐字**：定义／蛋白质合成实验／检索引发再巩固／两相反过程／提醒时长决定走向／Salk 研究所《神经元》模型）— **第一独立域（官方科普一手，含对 Nader 2000 与 Salk 模型的转述，按转述登记）**。
- `https://psychprofile.io/knowledge/how_does_recalling_a_memory_change_it.php`（PsychProfile Knowledge Base，**2026-11-09**，6 min；**WebFetch 200 全文逐字**：reconstructive retrieval／reconsolidation window／editing a document／confidence vs accuracy 对照表／gist vs peripheral／Mandela effect）— **第二独立域（心理测评机构知识库，商业立场登记，不作唯一来源）**。
- `https://cloud.kepuchina.cn/newSearch/imgText?id=7500211864272191488`（科普中国《把记忆想成一盘随时重录的磁带》）、`https://www.kepuchina.cn/article/articleinfo?business_type=100&classify=0&ar_id=631091`（《脑部的记忆之道》，审校：广州医科大学附属第二医院 詹丽璇）、`https://www.bioguider.org/doc-view-5306.html`（《记忆重构》，含 Nader 2000／Hupbach 2007／Loftus 1974 著录）— **WebSearch 快照逐字**交叉；bioguider **WebFetch 返回 Cloudflare「Checking your browser / Just a moment」拦截**，如实登记**未冒充一手全文**；三域含科普/医学审校/教学百科立场，均不作唯一结论来源。
- **判重**：全库 SKILL.md 精确扫描 `reconsolidation` / `再巩固` / `重整记忆` / `retrieval-induced` / `Hupbach` / `Loftus` / `记忆重构` / `检索即改写` / `misinformation effect` / `蛋白质合成` / `虚假记忆` **全 0 命中**；`Nader` 1 命中为 `meta/di-decision-tradeoff`「2000 年 Nader→Gore 妥协投票」、`destabiliz` 1 命中为 `engineering/wb-agent-evaluation` 的 Delayed Verification Destabilizes 论文题名，均**异命题**登记不复用。与本技能 §五/§九/§十/§十一 结论不复用；与 `meta/personal-ai-os` r713A 写入端不预筛/派生层回写为**互补非重复**（那条管要不要回写，本条管回写会改写原条）。**豆包自留地 WB 0 落地**。
- **未采纳**：Nader 2000 蛋白质合成抑制剂剂量与时序、Loftus 1974 样本数与百分比、Mandela Effect 社会学解释、PTSD/情绪障碍临床应用——前者属生物实验细节、后者属临床域，均不迁移到 agent 记忆工程。

## 十三、矛盾解决在哪一层是架构决策：写入侧四操作 vs 检索侧 ADD-only（MI · r755A 2026-11-15 实拉，三独立域交叉）

> 与 §五（双时态四时间戳：事实何时失效）、§十 10.3（未解矛盾阻断提交：图不授予模型裁决权）、§十二（检索即改写：读取动作污染原条）分工：本条管**「谁负责消解互相打架的两条事实」这一架构位，以及换掉这个架构位要付什么代价**。厂商立场逐条登记，仅取可迁移判据。

### r755A-1 ★ 矛盾可以在写入时消解，也可以留给检索时排序；两代官方算法给出相反答案
Mem0 官方《Memory eviction and forgetting in AI agents》（Updated 2026-07-31）逐字：每次新事实到达，「an **extraction pass** identifies what is worth remembering, and an **update pass** evaluates that candidate against existing memories. The decision is **not a similarity threshold but an LLM-selected operation**, drawn from four options」——`ADD` 无语义等价项时新建 / `UPDATE` 以互补信息扩充 / `DELETE` 新事实与之矛盾时删除 / `NOOP` 候选无实质增补时不动；「If a contradiction exists, **the resolution happens at write time, not at the next retrieval**」。官方迁移页《Platform: Migrating to the New Memory Algorithm》给出反转后的形态：Before = 「Two LLM passes (extract + merge)」+「ADD, UPDATE, DELETE」，After = 「**Single-pass ADD-only (one LLM call)**」+「**ADD only: nothing is overwritten or deleted**」；逐字「If your application previously relied on UPDATE/DELETE behavior to keep memory counts low, **the new algorithm handles this at retrieval time instead**」——靠多信号检索把更相关、更新的排到前面，「without destroying historical context」。
- **判据**：① 验收先问「本系统矛盾解决在哪一层」，两种架构不可混用：写入侧必须有 `NOOP`（避免无意义写入）与补证路径，且删掉旧值后**再也答不出「以前住哪」**；检索侧必须让新旧值能同库共现、并有时间信号把旧值压下去，否则就是官方列的 **stacked contradictions**（「user prefers verbose」与「user prefers terse」同时被 top-k 捞出来，模型无从判断哪个生效）。② 写入侧的四操作由 LLM 判定而非相似度阈值，官方理由是区分「临时状态」与「持久画像」：「"I'm in Berlin this week" sounds like it contradicts "user lives in Lisbon," but it does not」——把这类判断写死成 embedding 距离阈值即假阳性 supersession。③ 检索侧的时间信号是**加法不是过滤**：官方评测页逐字「The temporal score is **additive and semantic relevance always dominates**; it nudges ranking toward the correct dated instance **without filtering candidates out** or overriding a strong semantic match」⇒ 用时间做硬过滤会把语义最相关的旧证据直接丢掉。与 §五 r732B 分工：那条给四时间戳的数据模型，本条给「谁消解矛盾」的架构位；与 §十 10.3 分工：那条是图谱声明冲突时阻断下游，本条是抽取管线的写入/检索分工。

### r755A-2 ★ 架构反转是破坏性变更：迁移清单至少五项，benchmark 涨分不构成升级完成
官方迁移页把代价逐项列全：**① 阈值**「The default `threshold` is now `0.1` (it was `0.3` on v2), **so lower-scoring matches that v2 hid can now appear**」；**② 绝对分数漂移**「The top-level `score` … is now a **combined multi-signal score (semantic + keyword + entity) rather than pure cosine similarity**, so the **absolute numbers will differ**. Relative ranking remains comparable … **retune on a representative query set**」；**③ 容量曲线变化**「With ADD-only extraction, **memory counts will grow over time rather than being consolidated** … consider using the memory expiration feature or periodic cleanup」；**④ 写入面扩大**「**Agent-generated facts**: Often ignored → **First-class, stored with equal weight**」——原先只记用户明说的，现在 agent 说的「I've booked your flight for March 3rd」也入库；**⑤ 响应契约变化**「`get_all` now returns a **paginated envelope** (`{count, next, previous, results}`) instead of a bare `{results: [...]}`」。另有「**Existing memories are preserved. The new algorithm does not modify or re-process previously stored memories**」且新旧记忆走同一检索管线。评测页补两处口径：分数默认在 **`top_200` retrieval budget** 下报，「**Compare at equal constraints.** Always compare systems using the same retrieval budget, the same model, and the same latency budget」；LongMemEval 的 **Knowledge update 93.6 为全类最低**，官方自陈「older facts are preserved rather than overwritten, so **semantically similar prior facts can still surface alongside newer ones**」——即 ADD-only 的收益在 temporal（97.0），代价正落在知识更新类。
- **判据**：① 换抽取算法 / 换打分口径**默认按破坏性变更处理**，迁移检查表 ≥5 项（阈值 / 绝对分与硬阈值回归 / 容量增长与清理策略 / 写入面与 provenance 扩大 / 响应形状），每项配一条回归用例；② 「总分从 71.6 涨到 91.6」不能单独当升级完成证据，须连同**等约束**（same retrieval budget / model / latency）与**最难类别分数**并报，且报 mean tokens per query（官方「**Token efficiency matters as much as accuracy**」，under 7,000 vs full-context 25,000+）；③ 写入面扩到 agent 生成事实后，溯源字段必须能区分「谁说的」，否则 §五 episode 集合与 §九投毒验收的输入面已经变了却无人察觉；④ 旧记忆不重处理 = 同一库里两种抽取语义长期并存，任何「全库统一」的断言都要先核对这一条。与 §九 9.3「常规防御通过≠安全验收通过」同构：都是「绿指标不等于全链路就绪」，但落点不同（那条管对抗验收，本条管算法迁移）。

### r755A-3 ★ 遗忘是两套可组合的独立机制；四策略不可互换、三类失效模式各需定向探测
官方逐字「**Memory Decay is not an eviction strategy. Nothing gets removed.**」「Memory Decay is a **search-time re-ranking layer**. Recently accessed memories carry up to a **1.5x score boost**. Unused ones dampen toward **0.3x**. The dampened memory **still surfaces when it is genuinely the best match**. The fact **stays in the store**; its accessibility falls when it goes unused」；项目级 opt-in（`client.project.update(decay=True)`）、每条记忆最多跟踪 **20 个访问时间戳**。与 eviction（DELETE / batch_delete / delete_all / supersession-on-contradiction / tier-based lifetimes）**「actually removes facts」**正相对，且两者 compose：「a memory might **survive every eviction pass and still get dampened to a 0.3x retrieval score** because it has gone untouched」。四策略逐字「**are not interchangeable**. Each one fits a class of memory. **Age and recency handle noise; salience and supersession handle facts.** Most production systems need **at least one of each**」；主动/被动分界逐字「**Passive aging is for noise. Active forgetting is for facts.**」。三类失效模式与各自缓解逐字：**Over-eager forgetting**（TTL 太短 / LRU 未考虑真实使用节奏 → 「combine TTL or LRU with a **salience floor**」）、**Stale facts surviving**（纯 supersession 等不到用户明说「我搬家了」→ 「add a **time-based decay on top of supersession**」）、**Stacked contradictions**（无写时调和 → 「**at write time**, compare the candidate fact against the top similar memories … **Sort by recency at read time as a backstop**」）。各策略专属失效面：TTL 会删掉「又老又仍然为真」的事实（过敏、姓名、计费结构）；LRU「treats **access frequency as a proxy for importance**, and that proxy breaks for **low-frequency, high-stakes data**」；salience 有 **rater drift**（换模型/换 prompt 后旧阈值失效，官方建议 pin scorer 版本或周期重校）；supersession 有假阳性（见 A-1）。三层生命周期：「**Conversation memory is single-response. Session memory persists for minutes to hours and is cleared explicitly. User and organizational memory are long-lived**」，且「flows into longer-term, semantic memory **through promotion rather than indefinite accumulation**」。
- **判据**：① 健康度固定**两栏**：「检索可及性（有没有被降权）」与「库内是否还在（有没有被删）」——只看一栏会把「躲过驱逐但被压到 0.3x」误判为记忆正常，也会把「降权」误当「已清除」用于隐私/合规；② 清理动作先声明是哪一套机制，四策略按记忆类别配（TTL 只用于合规保留期、LRU 用于高 churn 助手、salience 须固定 scorer 版本、supersession 须判临时状态 vs 持久画像），不得一个 TTL 通吃；③ 三类失效模式各写一条定向用例（重要旧事实是否被 TTL 删 / 用户从未明说的变更后旧事实是否还在首位 / 相反偏好是否同时被召回），不许用一个总准确率盖过；④ promotion 是显式提升动作，不是「攒够了自动变长期」，否则三层生命周期退化为无限累积。与 §十一 r747C「延迟保持」分工：那条测记住没，本条测**陈旧性治理**；与 §十二 r751A 分工：那条管读取改写原条，本条管条目被降权或删除。

**提升层**：记忆治理 / 架构选型 / 迁移验收。触发词：矛盾解决位置、write time vs retrieval time、四操作 ADD/UPDATE/DELETE/NOOP、LLM-selected operation 非相似度阈值、single-pass ADD-only、新旧事实共存、stacked contradictions、阈值 0.3→0.1、绝对分数漂移需 retune、top_200 等约束、Knowledge update 最难类、写入面扩大到 agent 生成事实、Memory Decay 不是 eviction、1.5x/0.3x 检索侧重排、四策略不可互换、Passive aging for noise / Active forgetting for facts、salience floor、rater drift、低频高危事实、三层生命周期与 promotion。

### r755A 来源与判非（2026-11-15 实拉，逐字核验）
- `https://mem0.ai/library/agent-memory/memory-eviction-and-forgetting-in-ai-agents`（**Mem0 官方知识库**，Himanshu Sangshetti，Updated **2026-07-31**；**WebFetch 200 全文逐字**：遗忘非存储副产品、Bjork storage vs retrieval strength、四驱逐策略对比表、主动/被动遗忘、三类失效模式、四操作 ADD/UPDATE/DELETE/NOOP 与写时消解、三层生命周期、Memory Decay 1.5x/0.3x / 20 timestamps / 项目级 opt-in、四策略不可互换）— **第一独立域（厂商官方一手，商业立场登记）**。
- `https://docs.mem0.ai/migration/platform-v2-to-v3`（**Mem0 官方迁移文档**；**WebFetch 200 全文逐字**：Before/After 五行表、ADD-only 理由、新旧事实共存、agent 生成事实升为一等、hybrid retrieval、score 绝对值漂移与 retune、threshold 0.3→0.1、reranking 默认 false、memory count 不再 plateau、get_all 分页 envelope、现有记忆不重处理、V1/V2 端点继续可用、FAQ）— **第二独立域（官方一手）**。
- `https://docs.mem0.ai/core-concepts/memory-evaluation`（**Mem0 官方评测文档**；**WebFetch 200 全文逐字**：token efficiency 三参数、top_200 budget、六阶段抽取流水线、ADD-only 是关键架构决定、三层存储、四路多信号检索与时间分 additive 不过滤、query type→primary signal 表、LoCoMo 92.5 分类分与 6,956 tokens、LongMemEval 94.4 分类分（Knowledge update 93.6 最难）、Compare at equal constraints / score ceiling effects / BEAM 10M）— **第三独立域（官方一手）**。
- `https://github.com/A7um/AgentMemoryBook/blob/main/chapters/providers/mem0.md`（WebSearch 快照逐字：两阶段 extract→update 的 ADD/UPDATE/DELETE/NOOP 决策流与时序图、矛盾轮次 UPDATE 示例）＋ `https://mem0.ai/`（首页「extracts and updates memories」快照）— **交叉域（第三方实现笔记，不作结论唯一来源）**。
- **判重换道**：`ADD-only` / `Memory Decay` / `1.5x` / `0.3x` 全库 SKILL.md 命中**全部在豆包自留地** `defaults/wb-context-compressor`（§1816 一行「Mem0 单趟 ADD-only 提取…永不覆盖」、§1876/§1970 把 1.5x/0.3x 列在 FSRS/FadeMem 遗忘算法清单里）——**均为口号级 / 清单级**，WB **0 落地**且本轮不重述参数与性能数值；改取「矛盾解决在哪一层 + 架构反转的迁移清单 + 遗忘双机制与四策略失效模式」这一**架构决策与验收层**。窄串全库精确扫描：`NOOP` / `storage strength` / `supersession` / `四操作` / `stacked contradictions` / `矛盾在检索` / `写入时解决矛盾` / `threshold=0.1` / `retune` **全 0 命中** ⇒ 净新。与本技能 §五/§九/§十/§十一/§十二 结论不复用；与 r754(TI/PI/PDI)、r753(AI/EI/SI)、r752(VI/DI/OI) 九模块结论不复用。
- **未采纳**：LoCoMo/LongMemEval/BEAM 具体分数与 91.6/93.4 涨幅（厂商自评、随版本变化，只作方法示例）、FSRS/Ebbinghaus 生物遗忘曲线公式、TTL 天数与显存配置、`client.project.update` 等产品 API 绑定 —— 前者是时点数值，后者属豆包自留地已学的调度算法层。
## r759A · 前瞻记忆：把「意图」作为与回顾记忆正交的记忆类别来治理（来源：Einstein & McDaniel 前瞻记忆成分模型，Europe PMC PMC4255627 全文 XML 逐字 + medication-adherence review NIHMS-439369 WebSearch 快照逐字 + cognitivepsychology.com / 百度百科·科普中国「前瞻性记忆」交叉，2026-11-16 实拉）

> 与 §五/§九（五能力·失效双时态）·§十一（取回即改写）·§十二（矛盾/遗忘）分工：那些管「已存事实的保真与演化」，本节管「还没做、将来某个线索来了才触发的意图」——记忆系统的另一半，既有记忆栈按回顾记忆设计故对前瞻记忆系统性失明。

- **双成分与四阶段，纯粹的「前瞻记忆」不存在**：EC 逐字「According to Einstein and McDaniel (1990), there are two components of any prospective memory task. The first is a retrospective memory component which deals with the retention of the action and "target event" or retrieval context. The second component ... requires retrieval of action at an appropriate time or in response to an appropriate event」；四阶段＝①编码（formation of intention + 回顾/前瞻两成分）②延迟（performance delay，意图须被提取）③启动执行 ④结果评估「remembering having performed the action, so as not to repeat it (cancelation of intention stage)」。三元组逐字「the action (what), intent (that), and retrieval context (when)」，两问「"What is to be done?" and "at what time, or in which situation the action should be performed?"」。关键断言逐字「a "pure" prospective memory task may not exist (Maylor, 1993)」——**判据：意图存储必须同时落三元组（做什么/意图本体/何时何地触发），只存内容不存触发条件的 reminder 是残缺意图**。
- **事件线索 vs 时间线索不是难度差而是监控机制差**：EC 逐字「Time-based prospective memory task requires ... at a certain time or after a certain period of time has elapsed ... There is no explicit or specific external event which works as a cue ... People must remember on their own to monitor the passage of time and initiate action. Event-based prospective tasks are those in which the intended action is to be performed when a certain external event occurs」；综述逐字「time-based cues are more difficult to detect as they place greater demands on strategic monitoring ... primarily supported by prefronto-striatal systems ... Event-based tasks, on the other hand, are largely held to involve more automatic or spontaneous retrieval processes」；cognitivepsychology 逐字「Time-based PM is generally harder than event-based PM because it requires self-initiated monitoring of time passage rather than relying on environmental cues」。**判据：能挂事件线索就别挂纯时间线索**——事件线索由环境替你监控（自动/自发提取），时间线索要 agent 自己 self-initiated 轮询时钟（战略监控、耗资源）；给 agent 的待办若写「明天提醒我」＝time-based 高风险，应改写成「下次我打开 X 文件时提醒我」＝event-based。
- **线索三特性 + 外部审计抵消「执行了却忘了自己执行过」**：综述逐字「Several features of the cue itself can influence detection and recognition ... its salience (distinctive cues are more effective), centrality to the ongoing task (focal cues are more easily detected and recognized), and association with the intention (semantic relatedness is facilitative)」；第四阶段逐字「the accuracy and completeness of the realized intention is evaluated ... a particularly salient feature of tasks that occur repeatedly and according to a relatively established schedule (i.e., "habitual prospective memory")」；科普中国逐字「有效的提示物应能加强或激活靶事件和意向之间的联系」「外部提示物如日历、闹钟...比内部线索...更常使用」。**判据：意图兑现须带完成回执并参与「是否重复触发」判定**（对应四阶段第 4 步 cancelation of intention），否则周期性待办会重复执行；线索设计走显著性/与当前任务中心性/与意图语义相关三面，且优先外部化（写进可查询对象而非只放工作记忆）。

**提升层**：记忆治理 / 意图与待办系统 / 提醒可靠性。触发词：prospective memory、前瞻记忆、delayed intention、event-based vs time-based、self-initiated monitoring、retrospective component + prospective component、action(what)/intent(that)/retrieval context(when)、四阶段 cancelation of intention、no pure prospective task、salience/focal/semantic relatedness、战略监控 vs 自发提取、外部提示物、完成回执防重复触发。

### r759A 来源与判非（2026-11-16 实拉，逐字核验）
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC4255627/` → Europe PMC 全文 XML `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4255627/fullTextXML`（**WebFetch 200 / urllib 88KB XML 逐字抽取**：四阶段模型 Brandimonte & Passolunghi 1994、Einstein & McDaniel 1990 双成分、action(what)/intent(that)/retrieval context(when) 三元组、What+when 两问、"pure" PM may not exist、time-based 无外部线索须 self monitor passage of time、event-based 外部事件触发、PM 无外部提示而回顾记忆有）— **第一独立域（同行评议全文，PMC 开放获取）**。
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC3574793/`（medication-adherence review，NIHMS-439369；**WebSearch 官方页快照逐字**：五阶段成分模型、delay 期间 competing ongoing activities 阻止主动复述、cue detection+self-initiated retrieval 为「the defining feature ... differentiates the construct from retrospective memory in which retrieval is based on an explicit prompt」、time-based 需 strategic monitoring 由 prefronto-striatal systems 支持、event-based 更 automatic/spontaneous、线索 salience/focal/semantic relatedness、执行后 evaluation of the realized intention）— **第二独立域（同行评议综述，与 DOM 页不同团队）**。
- `http://cognitivepsychology.com/Prospective_Memory`（**WebSearch 快照逐字**：PM 定义对比回忆过去、event/time 两类及 time-based 更难的 self-initiated monitoring 原因、PAM 理论监控耗资源拖慢 ongoing task、multiprocess framework 线索显著/强关联时可自发提取、age-PM paradox、外部提示与 implementation intention if-then 计划）＋ `https://baike.baidu.com/item/%E5%89%8D%E7%9E%BB%E6%80%A7%E8%AE%B0%E5%BF%86/10532567`（科普中国审核词条逐字：三关键特征、time/event 分类、外部提示物优于内部线索、有效提示物应加强靶事件-意向联系、Einstein & McDaniel 1990 经典范式）— **第三、四域交叉（教学站/科普词条立场登记，不作唯一来源）**。
- **判重**：全库 SKILL.md 精确扫描 `prospective memory` / `前瞻记忆` / `意图记忆` / `delayed intention` / `执行意图` / `implementation intention` **全 0 命中**；`intentions` 1 命中为 `good intentions 不够`（语境=Langflow 策略守卫工具，**异命题**）、`event-based`/`time-based` 各 1 命中为 Airflow `schedule` 调度字段（`time- and event-based scheduling logic`，**异命题**）。与本技能 §五/§九/§十一/§十二 结论不复用；与 r758(TI/PI/PDI)、r757(AI/EI/SI)、r756(DI/VI/OI) 九模块结论不复用；豆包自留地 WB 0 落地。
- **未采纳**：age-PM paradox 具体百分比（52%/33%、30–40% 等时点数值）、Brodmann 10 区/前额叶神经定位、Ebbinghaus 遗忘曲线公式、具体 if-then 计划模板与 APP 产品绑定、PAM vs multiprocess 之争的唯一正确性裁决（学界仍有争议，只记两机制并存的操作含义）。

## r763A · 交互记忆系统（TMS）：记忆分布在「成员 + 外部 aid」，元记忆目录 who-knows-what 是独立一层（来源：Wegner 1987/1995 交互记忆理论，Moreland et al.《Socially Shared Cognition at Work》MIT 全文 PDF 逐字 + Gupta 2022 CMU Tepper 博士论文 TMS/TAS/TRS 三系统逐字 + Wikipedia/心理学百科「Transactive memory」交叉，2026-11-18 实拉）

> 与 §五/§九（个体记忆五能力·失效双时态）·§七（实体解析）·§十三（矛盾解决位置）·§r759A（前瞻记忆）分工：那些管「单个记忆系统内部怎么存/更新/裁决」，本节管「记忆分布在一个群体（或多 agent）时，谁知道谁懂什么」——**元记忆的对象从「自己的记忆」扩到「别人的 + 外部存储的」**，是与个体记忆质量正交的一层；agent 团队的个人记忆再强，没有 who-knows-what 目录也调不动别人的知识。

- **记忆分布在人 + 外部 aid，TMS = 个体记忆 + 元记忆 + 交互过程三件套，不是「共享一个大脑」**：MIT Moreland 逐字「few people rely exclusively on their own memories, which are limited and often faulty. Instead, most people supplement their own memories with external aids. These memory aids include both objects (e.g., address and appointment books, lists of uncompleted projects) and other people (e.g., friends, spouses, coworkers)」；「a transactive memory system thus provides access to more and better information than any single group member could remember alone」；Wegner 概念（CMU Gupta 逐字）「a dynamic system comprising of (1) members' current level of knowledge and skills (i.e. individual memory system); (2) their current understanding of each others' task-relevant knowledge and skills (i.e. individual meta-memory); and (3) the inter-member processes that facilitate the dynamic updating of meta-memory and subsequent allocation and retrieval of knowledge」。Ren & Argote 结构面+过程面逐字「both a structural component (the linkages of individual memory to the collective) and transactive processes that make the transactive memory dynamic」。**判据：多 agent / 人机混合记忆的盘点要分三层**——① 各成员自身记忆（个体能力）② 关于「谁懂什么、东西存哪」的元记忆目录（本层常缺）③ 更新目录与分配/检索的交互过程；只盘①会把「团队记不住」误判成「个体记忆不强」，实为②③缺失。元记忆可指向外部档案（百科逐字「a directory for labels that are not stored in one's own memory, but in an external source ... another person's memory system, or a specific physical or digital archive」）⇒ 目录里的「存储位置」字段须能指到外存句柄，不止指人。

- **编码/存储/检索三过程本身是 transactive（随交换更新），且 turnover 破坏目录**：百科逐字「the development of a transactive memory system involves three stages: encoding, storage and retrieval. These processes are transactive, meaning that they are updated as members exchange information with one another」；个体层四过程逐字「encoding ... incoming information is designated a relevant 'label' ... storage ... assimilated in memory along with knowledge with similar labels ... The labels are used to guide the retrieval process ... forgetting happens automatically whereby knowledge that is not accessed for a long time starts to decay」，而元记忆「can serve as a directory for labels ... in an external source」。MIT Moreland 逐字群体绩效随共事时间提升但成员变动打断「managers should try to minimize changes in a group's composition (due to absenteeism, leaves, transfers, or turnover) because the arrival of newcomers and/or departure of oldtimers from the group can seriously disrupt its transactive memory system」。**判据：① 标签（label）是检索与目录共用的寻址键——写入时无标签＝后续既不能检索也不能被目录登记；② 团队/会话成员变动（agent 换模型、成员增减、会话重建）须显式重建 who-knows-what 目录，不能假设目录还在**——这是 §r751A「换抽取算法按破坏性变更处理」在群体层的对应面（那条换算法，本条换成员）。

- **「谁知道谁懂什么」必须公开宣布才生效，私下自知无效；伴侣/熟人优于陌生人是因为知道对方领域就避免重复存**：MIT Moreland 逐字 Stasser 凶案实验「some clues were distributed to everyone, whereas other clues were distributed in ways that provided every member with expertise on a different suspect ... Every group was informed that its members might receive different sets of clues. Information about exactly who knew what, however, varied ... Simply informing group members about their own expertise had little impact on group performance, but announcing everyone's expertise helped group members to discuss more of the critical clues and thereby solve the crime」；百科逐字 Hollingshead「romantic partners ... performed better on knowledge recall than dyads ... couples will memorize more words in a list than two strangers when they are rewarded on number of unique words you recall ... couples know how best to remind each other of the knowledge they have, and that couples have a good conception of the other's knowledge and will therefore avoid memorizing words within their partner's domain」。**判据：多 agent 里只让每个 agent「自己知道自己是某领域专家」不够，必须把专长目录广播成全员可查询的共享对象**（公开宣布 vs 私下告知的差是群体绩效分水岭）；且目录带来「分工不重复存」的收益——检索先查目录定位到对口成员/外部档案，而非每个 agent 各存一份。与 §七实体解析分工：那条防「错合把事实挂错实体」，本条管「知识该放谁那、怎么找到」——一个是身份正确性，一个是分工与寻址。

**提升层**：多 agent 记忆 / 团队知识治理 / 检索寻址。触发词：transactive memory、TMS、Wegner、who knows what、元记忆目录、external aids、individual memory + meta-memory + transactive processes、encoding/storage/retrieval transactive、label 寻址、turnover 破坏目录、Stasser 凶案、Hollingshead couples、专长公开宣布、分工不重复存、structural + process component、与实体解析分工。

### r763A 来源与判非（2026-11-18 实拉，逐字核验）
- `https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Social_Cognition/Moreland_et_al_Socially_Shared_Cognition_at_Work_Whats_Social_pp57-84.pdf`（**MIT 课程库全文 PDF，WebSearch 逐字**：Wegner 1987 外部 aid 论、TMS=知识+who-knows-what 共享觉知、少依赖自身记忆、external aids 含 objects 与 other people、群体复杂度越高越有用、turnover 破坏、Argote 学习曲线、Stasser 凶案实验「公开宣布专长」才奏效逐字）— **第一独立域（同行评议章节全文）**。
- `https://www.cmu.edu/sites/default/files/cmu-tepper-site-files/2025-06/2022-organizational-behavior-and-theory-gupta-dissertation.pdf`（**CMU Tepper 博士论文，WebSearch 逐字**：TMS/TAS/TRS 三系统、Wegner 1987/1995 三件套（个体记忆/元记忆/交互过程）、Ren & Argote 2011 definition、编码-存储-检索-遗忘四过程与 label 机制、元记忆作外部源目录、directory updating/member specialization/credibility 三测度）— **第二独立域（学位论文一手）**。
- `https://ergngevd.top/wiki/Transactive_memory` + `https://oecs.mit.edu/`（**WebSearch 快照逐字**：Wegner 1985 提出、三过程 transactive 随交换更新、Hollingshead couples vs dyads 实验、成员专长 domain、external memory aid 类比、structural+process 二分、penn state 百科对照）— **第三、四域交叉（百科/认知科学入口，立场登记，不作唯一来源）**。
- **判重**：全库 SKILL.md 精确扫描 `transactive` / `交互记忆` / `who knows what` / `谁知识谁` / `元记忆目录` / `分布式记忆` 仅 `meta/mi-memory` 1 命中，核为该技能 §r732B-1「记忆五能力」中的检索语境词，**非 TMS 本体**；与 §五/§七/§九/§十三/r759A 结论不复用；与 r762(TI/PI/PDI)/r761(OI/EI/SI)/r760(AI/VI/DI) 九模块结论不复用；豆包自留地 WB 0 落地。
- **未采纳**：Wegner 1985 vs 1987 提出年份口径差（百科作 1985、论文作 1987，两存只记概念）、具体实验样本量与 effect size、TAS/TRS 两系统完整展开（本轮只取 TMS，留作 OI 编排候选）、神经定位与量化模型参数。

## r767A · 检索诱发遗忘（RIF）：检索是抑制性选择，练一条会压低同类未练条（来源：Anderson, Bjork & Bjork 1994 检索练习范式，Brain Sciences 2021 综述 PMC8467325 全文逐字 + Anderson/Bjork/Bjork 2000 PubMed 11082860 逐字 + Rowland et al. 2014 Frontiers 复现与边界 PMC/PubMed 25484872 + Bjork Lab《Interference and Forgetting》PDF 逐字，2026-11-19 实拉）

**这一节管什么**：记忆被检索不只是「读出」——选择性检索一个子集会**主动抑制**同类别未练习的相关项，使它们后来更难回忆。这是与 §十二 r751A「检索即改写被检索的那条」互补的另一面：r751A 管被读那条被改写，本节管**没被读的邻居被压低**。

### 三独点

1. **RIF 三态 Rp+/Rp−/control，练习收益不外溢到同类邻居反而使其低于基线**：检索练习范式＝学习类别-样例对（FRUIT-ORANGE）→ 只对部分类别的部分样例做词干线索练习（FRUIT-OR___）→ 延迟后类别线索自由回忆。结果模式 `Rp+ > control > Rp−`：Rp+（练习类别中练过的）回忆最好，Rp−（练习类别中没练的，如 FRUIT-BANANA）**低于** control（没练类别的没练项，如 METALS-IRON），尽管二者学习时长相同。综述逐字：「recall of Rp+ items is generally improved on the final test relative to the control items, and, more important, recall of Rp− items is typically impaired relative to the control items, thus reflecting RIF」。**判据：一次检索的成功不能当作「同簇其他条目仍可及」的证据，须单独测 Rp− 类邻居；把高频检索当免费的知识巩固是错的，它附带抑制代价。** 与 §十一 r747C 延迟保持、§十二 r751A 保真度分工（那两条管被练/被读条本身，本条管未被练的同簇项）。

2. **抑制说 vs 阻断说是两个可分离的因果解释，独立线索（independent probe）是裁决实验**：blocking account 认为 Rp+ 被强化后在最终测验时抢答、干扰 Rp−；inhibition account（item suppression）认为练习时 Rp− 主动被压低其表征激活。综述逐字区分：抑制说「assumes that the suppression directly reduces the activation level of the competing memory representation itself」，故 RIF 应**与测验线索类型无关**；independent-probe 实验用**全新线索**（sports-S___ 而非原线索 hobby-S___）测 Rp−（Soccer），此时不会调出 Rp+ 产生阻断，「should exclude potential blocking effects」而 RIF 仍在 ⇒ 排除纯阻断解释。**判据：要证明「某条被抑制」而非「被别的条盖住」，必须换一条与练习线索无关的独立线索再测一次；只在原类别线索下观察下降，两种解释分不开。** 另有 2000 年实验逐字：竞争练习（词干要求回忆样例）产生 RIF，非竞争练习（同样重复次数但要求回忆类别名）不产生——「retrieval-induced forgetting is not caused by increased competition arising from the strengthening of practiced items, but by inhibitory processes specific to the situation of recall」。**重要纠正**：该 2000 论文题名带 recall-specific，但 2021 综述明确 RIF **并非只在回忆中出现**——「RIF is not only observed with category-cued recall but also arises in yes–no item recognition testing, and when ROC analysis is applied」；两处口径并存登记，不择一，判据取「抑制作用于表征本身、测验格式不是 band 时仍应复现」。

3. **RIF 是稳健但带边界的效应，复现须带范式与样本口径，不支持的范式如实保留**：Rowland et al. 2014 逐字：传统 retrieval-practice 范式下本科生样本（Exp1）与 internet 样本（Exp2）都复现 RIF，但用 Anderson & Spellman 1995 **independent cue procedure 时未复现**（Exp3）。综述亦列反例 Williams & Zacks 2001。**判据：报告「检索会抑制邻居」必须写清用哪个范式与样本，不能当无条件定律；换线索程序后效应消失是真实边界而非实验失败，须与「抑制说」并列登记而非抹掉。** 人类记忆机制迁移到多 agent 记忆检索按 rules/08 §五作待验证假设，只取三条可机检口径：① 检索命中某条时记一条「同簇未检索项」的对照召回率，别只看命中率；② 判断抑制还是覆盖，用一条与本次检索词无关的独立证据 ID 再查一次；③ 换检索/排序程序的回归用例须包含 original 与 independent-cue 两种，缺一不算验完。

### 来源
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC8467325/`（**Brain Sciences 2021 综述《The Mechanisms Underlying Interference and Inhibition》全文，WebFetch 200 逐字**：retrieval-practice 三阶段、Rp+/Rp−/control 定义、inhibition vs blocking 两说、independent probes 排除 blocking、RIF 在 recognition/ROC 亦出现、Williams & Zacks 2001 反例）— **第一独立域（同行评议综述全文）**。
- `https://www.pubmed.ncbi.nlm.nih.gov/11082860/`（**Anderson, Bjork & Bjork 2000 PubMed 11082860 摘要逐字**：competitive vs noncompetitive practice 对照、「only the competitive practice subjects were impaired」「not caused by increased competition … but by inhibitory processes specific to the situation of recall」；题名 recall-specific 与 2021 综述口径冲突如实两存）— **第二独立域（原始实验一手摘要）**。
- `https://pubmed.ncbi.nlm.nih.gov/25484872/`（**Rowland, Bates & DeLosh 2014 Frontiers in Psychology 摘要 PubMed 25484872 逐字**：本科生与 internet 样本复现、independent cue procedure 未复现）＋ `https://pmc.ncbi.nlm.nih.gov/articles/PMC1885480/`（RIF 三阶段与 `Rp+ > METALS-IRON > FRUIT-BANANA` 模式逐字）— **第三、四域交叉（复现边界与范式一手）**。
- `https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/07/RBjork_2003.pdf`（**UCLA Bjork Lab 官方 PDF 逐字**：「Forgetting is not simply a failure … there must be some means of restricting what is retrieved」，selection-suppression 与注意类比）— **第五域（实验室官方，立场登记）**。
- **判重**：全库 SKILL.md 精确扫描 `retrieval-induced` / `RIF` / `检索诱发遗忘` 在 `meta/mi-memory` 仅 1 处（§r751A 判重串中作异命题预留，非本体）；`检索诱发` 全库 0。本节与 §十二 r751A（被读那条被改写）、§十一 r747C（学习技法延迟保持）、§十三 r755A（矛盾解决层）结论不复用；与 r766(TI/PI/PDI)/r765(OI/EI/SI)/r764(AI/VI/DI) 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：具体抑制的神经环路/前额叶-海马机制（综述有但属生物层，不迁 agent）、Rp− 效应量具体百分比与样本量（口径随范式变）、Anderson & Spellman 1995 独立线索程序的完整实验材料、与 §七实体解析的合并策略（异命题）。

## r771A · 睡眠依赖的系统巩固：离线期把不稳定表征转成长期存储，重激活是时钟而非背景（来源：Nature Communications 2021 s41467-021-23520-2 内源重激活逐字 + Nature Neuroscience 2023 s41593-023-01381-w SO/spindle/ripple 顺序耦合逐字 + Nature Communications ncomms15404 素材特异再加工 + npj Science of Learning 2025 s41539-025-00340-3 个性化 TMR，2026-11-19 实拉）

**这一节管什么**：前面各节管「醒着时记忆怎么被改写/抑制/调度」。本节管**离线期（睡眠）系统级巩固**——新编码的不稳定表征如何在没有被提取时被转到皮层长期存储。与 §十二 r751A（取回即改写被读那条）、§十一 r747C（间隔练习的延迟保持）互补：那两条是清醒态的重写与练习调度，本条是无外部任务时的离线转移。人类神经机制迁移到 agent 按 rules/08 §五作待验证假设，只取三条可机检口径，不迁生理频率。

### 三独点

1. **系统巩固是「突触巩固」与「系统巩固」两条独立机制，且离线转移由三种振荡的顺序耦合定时**：原文逐字区分 synaptic consolidation（局部回路的 LTP，靠短延迟 co-firing 的 STDP）与 systems consolidation（记忆痕迹跨 hippocampal–cortical 网络转移）。三种 NREM 振荡各管一段：皮层慢波 SO 的 up-state 起兴奋窗口 → 丘脑皮层 spindle 嵌在 up-state、门控 Ca²⁺ 内流利于可塑 → 海马 ripple 落在 spindle 的可兴奋 trough、把重放送到皮层靶点。Nature Neuroscience 2023 iEEG 逐字：SO up-state 支配下 spindle 给 ripple 设定发生时间窗，顺序耦合带来放电率、局部短延迟互相关、跨区 MTL 交互三级阶梯式上升，为 STDP 与系统巩固造条件。**判据：「离线巩固」不是笼统睡一觉，而是「局部稳定化」与「跨区转移」两件事分别验收；转移是否发生看跨区交互/重放的时序耦合，不是看局部激活强弱。** 与 §十二 r751A 分工：那条管单次取回改写原条，本条管跨存储层的整体迁移。

2. **重激活强度预测巩固水平，但「内源」与「外源提示（TMR）」是两类证据，且 TMR 对难记忆要个性化**：2021 内源范式（无外部线索）逐字：用多变量解码在 NREM 期捕捉到学习材料的自发重激活，且 **SO-spindle 耦合精度预测重激活强度、重激活强度又预测个体巩固水平**——这是相关性证据链。与之相对，TMR（睡眠中给线索外源触发）能增强表征，但 2025 npj 逐字：固定提示协议忽略个体差异与记忆痕迹强度，对「难回忆」材料收益递减（记忆强度-巩固呈倒 U），按个人回忆表现与任务难度调频的个性化 TMR 才显著降低衰减、改善纠错。**判据：报「重放提升巩固」须分清是自发重激活的相关证据还是外源提示的干预证据，二者不可互证；单一固定提示策略对高难条目可能反效果，须按条目强度分档调干预频率。**

3. **巩固是周期性/分阶段的时序过程，机制归属仍有争议，迁移只取可机检口径不择一**：ncomms15404 逐字：再加工不是整夜均匀发生，而呈周期性、在学习后约 3h 与 6h 两个窗口最强；NREM 与 REM 分工有 sequential hypothesis（两阶段先后接续）与独立假说（各管不同方面）两说，原文明言「differential function … still controversial」。2025 TMR 亦记倒 U 关系。**判据：报告「巩固效果」须带时间窗与阶段口径（学习后多久、NREM/REM 哪段），不能笼统说「睡了一觉变好」；两说并存不择一。** agent 落地只取三条：① 把「离线巩固」拆成局部稳定化与跨层转移两个动作分别记录；② 高价值条目的再激活/摘要调度带时间窗与强度分档，不搞一次性固定频率；③ 迁移属待验证假设，不因「生物上有此机制」就当作 agent 必须实现。

### 来源
- `https://www.nature.com/articles/s41467-021-23520-2`（**Nature Communications 2021 内源重激活全文 WebSearch 逐字**：SO-spindle complex 给内源自发重激活定时、耦合精度→重激活强度→巩固水平的相关链、TMR 外源与内源之辨、systems consolidation 经由海马-新皮层转移逐字）— **第一独立域（期刊全文）**。
- `https://www.nature.com/articles/s41593-023-01381-w`（**Nature Neuroscience 2023 iEEG 全文 WebSearch 逐字**：synaptic vs systems consolidation 两机制定义、SO up-state→spindle→ripple 顺序耦合、放电率/短延迟互相关/跨区交互三级阶梯、STDP 最优条件）— **第二独立域（期刊一手）**。
- `https://www.nature.com/articles/ncomms15404`（**Nature Communications 素材特异再加工全文 WebSearch 逐字**：再加工周期性、学习后 3h/6h 峰、NREM/REM 分工 sequential vs 独立两说并存且「still controversial」）— **第三独立域（期刊全文）**。
- `https://www.nature.com/articles/s41539-025-00340-3`（**npj Science of Learning 2025 个性化 TMR WebSearch 逐字**：固定协议忽略个体差异与痕迹强度、倒 U 关系、个性化按回忆表现与难度调频降低衰减）— **第四域（干预一手）**。
- **判重**：全库 SKILL.md 精确扫描 `sharp-wave`/`ripple`/`sleep spindle`/`慢波`/`睡眠巩固`/`system consolidation`/`离线重放`/`SO-spindle` 全 0 命中（含本技能）。本节与 §十二 r751A（取回即改写）、§十一 r747C（间隔练习）、§十三 r755A（矛盾解决层）结论不复用；与 r770(TI/PI/PDI)/r769(OI/EI/SI)/r768(AI/VI/DI) 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：具体到频段（SO 0.5–1Hz/spindle 11–16Hz/ripple 100–200Hz）的生理参数、Ca²⁺ 内流分子通路与 STDP 波形、各类 TMR 刺激音频协议、NREM/REM 分工的唯一裁定（两说并存不择一）。

## r775A · 错误记忆与来源监控：高置信的错误条目能从「语义要点」里自发长出来（来源：Reyna 等模糊痕迹理论综述 PMC4815269 全文逐字 + Saleh 等《Cognitive and neural mechanisms underlying false memories》PMC10567586 全文逐字 + CUNY Pressbooks 心理学教材 DRM/Loftus 逐字 + 百度百科「错误记忆」四理论模型，2026-11-19 实拉）

### 三独点
1. **DRM 范式证明「要点」本身会凭空造出未编码条目，且置信度与真词相当**：presented 词表（bed/rest/dream/snooze）共享语义，未呈现的关键诱饵（sleep）被高比例错误再认，"almost as highly as presented targets"；模糊痕迹理论（FTT）解释为我们并行存 verbatim trace（表面形式）与 gist trace（语义要点），"False recollections are based on meaning (gist), especially in the absence of verbatim information"，而 "recollection of verbatim content suppresses false memories"。判据：**按要点/摘要聚合生成的记忆条目必须标为派生（inferred/gist）且与逐字锚点分离存——「语义上应该存在」是错误条目的高发源，不是证据**；这与本技能 §五 r732B episode 溯源、§十二 r751A「检索即改写」互补（那两条管事实从哪来/被改写，本条管条目从要点里被凭空生成）。
2. **误导信息效应与 DRM 里 verbatim 的作用方向相反，两类错误记忆不能互相替代验收**：一手逐字指出 misinformation 里 "verbatim memory ... promotes false-memory acceptance"（记得审讯里那个锤子 → 更可能误认现场有锤子），DRM 里 "better verbatim memory for the presented word would help people reject the unpresented word"（记得呈现的是螺丝刀 → 拒绝锤子诱饵）；gist 在两范式里都促接受。且 Ost 等 2013 实测 "failed to find correlations between misinformation effects ... and DRM effects"。判据：**「抗植入污染」与「抗要点诱饵」是两块独立指标，各自的负例用例要分开建**——前者测事件后信息覆盖，后者测无中生有的语义邻居，单测一个不能宣称记忆可信。
3. **激活-监测理论（AMT）把错误定位到「来源归属失败」，想象膨胀说明纯内部模拟也能造出高置信记忆**：AMT 逐字 "false memory occurs when participants fail to monitor the source of the activated item, and thus mistakenly remember the critical lure that was generated externally ... rather than internally (from spreading activation)"，"Any disruption in the source monitoring has been shown to increase false memory"；imagination inflation 显示 "merely imagining a non-existent event increases the likelihood that the individual will later report having actually experienced that event"，靠反复心理模拟抬高熟悉度与可及性、混淆来源监控。判据：**high confidence 不能当真实性证据，验收要能逐条回答「这条是从材料编码来的，还是从要点/想象里生成后被误归属的」**——与 r751A「流畅度≠准确率」同族但落点在来源归属；与 agent 落地只取三条可机检口径（派生条目单独标源/抗污染与抗诱饵分栏/高置信条目强制逐字锚点回归），按 rules/08 §五作待验证假设。

### 来源
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC4815269/pdf/nihms-749930.pdf`（**Reyna 等《How Fuzzy-Trace Theory Predicts True and False Memories》PMC 全文 PDF WebFetch/WebSearch 逐字**：DRM bed/rest/dream→sleep 关键诱饵、verbatim/gist 双 trace、misinformation 与 DRM 的 verbatim 反向作用、Ost 2013 无相关）— **第一独立域（理论一手全文）**。
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC10567586/`（**Saleh 等《Cognitive and neural mechanisms underlying false memories》PMC 全文 WebFetch 200 逐字**：DRM 语义相似生错、FTT gist 在无 verbatim 时驱动错、AMT 来源监控失败逐字、misinformation 由事件后信息覆盖原记忆）— **第二独立域（综述一手全文）**。
- `https://pressbooks.cuny.edu/hursonpsych101extras?p=225`（**CUNY《Problems with Memory》教材 WebSearch 全文逐字**：FURNITURE 词表诱发未呈现家具、Donald Thomson 错认案、Loftus & Palmer 1974 smashed/contacted 与破玻璃两周后出现率翻倍）— **第三域（教材交叉）**。
- `https://baike.baidu.com/view/88911.html`（**百度百科「错误记忆」WebSearch 全文逐字**：Deese1959→Roediger&McDermott1995、四理论模型——内隐激活/模糊痕迹/来源监测/激活监测、单词类 DRM 与事件类误导信息两范式分类）— **第四域（中文百科交叉，立场登记）**。
- **判重**：全库 SKILL.md 精确扫描 `DRM`/`critical lure`/`关键诱饵`/`模糊痕迹`/`fuzzy-trace`/`激活监测`/`imagination inflation`/`想象膨胀`/`misinformation` 在 mi-memory 正文 0 命中（仅 §r751A 来源段列 `misinformation effect` 作判重词、Loftus 仅作判非异命题提及，非落地）；与本技能 §五 r732B（episode 溯源）/§十二 r751A（检索即改写/流畅度≠准确率）/§r767A（RIF 遗忘）/§r771A（睡眠巩固）不复用；与 r774(TI/PI/PDI)/r773(OI/EI/SI)/r772(AI/VI/DI) 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：Loftus 具体样本数/速度估计数值与百分比、fMRI/ERP 脑区与神经振荡、DRM 词表联想强度参数、错误记忆的年龄/情绪/人格差异、法庭证词应用与 Mandela Effect 社会学解释（均属实验细节或临床/司法域，不迁移到 agent 记忆工程）。

## r779A · 定向遗忘（directed forgetting）：遗忘是受控执行过程，不是被动衰减（MI · 2026-11-20 实拉，多独立域交叉）

> 来源：Rummel, Marevic & Kuhlmann 2016《Investigating storage and retrieval processes of directed forgetting: A model-based approach》DOI 10.1037/xlm0000266 PubMed 摘要 WebFetch 200 逐字（第一手）+ Anderson & Hanslmayr 2014 综述《Neural mechanisms of motivated forgetting》PMC4045208（item/list 两范式与 accessibility vs availability 术语逐字，第二独立域）+ Bäuml 等《Forget me (not)?》Frontiers PMC4644810 全文（选择性复述 vs 提取抑制两说逐字，第三域）+ MDPI 2022《Obliviate!》元分析（抑制/替代两策略神经分离逐字，第四域交叉）。

### 三独点
1. **item-method 与 list-method 的遗忘成本落在不同阶段，不能用一套「删除」口径概括**：Rummel 2016 多项模型逐字——两种范式的「遗忘收益」都来自 to-be-remembered 条目**更好的存储**（better storage）；但「遗忘成本」分野：list-method 成本来自 to-be-forgotten 条目**提取减少**（reduced retrieval），item-method 成本**不只**来自存储减少（当时主流观点），**还**来自提取减少（"occurred not only due to reduced storage ... but also due to reduced retrieval"），且实验二在排除回忆输出顺序影响后仍复现该新发现。这修正了「item=选择性复述编码期 / list=提取抑制」的简单二分。判据：**记忆清理要区分「当初没存好（写入侧）」与「存着但取不出（检索侧降权/抑制）」两栏**——与本技能 §十三 r755A「decay 降权不删 vs eviction 真删」互补：那条是系统自动机制，本条是**有意指令驱动的受控遗忘**，说明同一个「忘」字背后至少两类可分离的加工。
2. **「可及性」与「可用性」是两种独立的遗忘，提取线索能区分它们**：Anderson & Hanslmayr 综述 Glossary 逐字定义——提取失败可能是「没访问到已存记忆」（accessibility）也可能是「记忆已不在系统里」（availability）。关键实验判据：list-method 的遗忘效应**只在自由回忆出现、再认测试不出现**，因为再认时重新呈现条目即解除抑制（release from inhibition），证明条目**已被编码并仍存着、只是暂时不可及**；item-method 效应在再认也出现，说明条目**根本没被好好编码**。判据：**验收「真删还是暂时压住」必须换一种提取线索再测一次**——原线索取不出不代表数据没了；这与 §r767A RIF「换独立线索再测证明被抑制而非被覆盖」同源，但那条测的是练一条压同簇邻居，本条测的是**遗忘指令**对目标条目本身的作用，机制族不同。
3. **意图性遗忘有至少两条可分离策略——直接抑制 vs 替代/语境切换，产品含义不同**：MDPI 元分析与 ScienceDirect 2021 逐字——直接抑制（direct suppression）走额叶-海马抑制回路（frontally-mediated suppression），替代/thought substitution（想象别的事）走 VLPFC/IFG 语境转移（contextual shifting）；行为上两者都能造成遗忘，但 Forget 线索引发可预测未来遗忘的额叶振荡功率变化，Imagine 线索则靠条目-线索表征相似度下降。且抑制效应有剂量-反应关系（no-think 次数多才显著，16 次有效、1 或 4 次不显著），效应量小（32 研究元分析平均召回下降约 8%），并有重复失败案例。判据：**「让用户/agent 忘掉一条」要显式选策略**——压制（不再检索、降可及性、可恢复）适用于「暂时不该浮现」；替代（写一条新的语境/内容覆盖）适用于「旧值已失效要换新」；两者不可混报效果，且抑制的效应量小、需多次触发，不能做一次就算忘干净。按 rules/08 §五，人类记忆机制迁移到 agent 作**待验证假设**，只取三条可机检口径（存储/提取两栏、换线索验真删、策略显式声明），不因生物有此机制就断言 agent 必然如此。

### 来源
- `https://pubmed.ncbi.nlm.nih.gov/26950491/`（Rummel 等 2016 多项模型研究 PubMed 摘要 WebFetch 200 逐字：收益=更好存储、list 成本=提取减少、item 成本=存储+提取双因、输出顺序无关复现）— 第一独立域（期刊一手摘要）。
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC4045208`（Anderson & Hanslmayr《Neural mechanisms of motivated forgetting》PMC 综述全文 WebSearch 逐字：item/list 范式图、accessibility vs availability 术语、list 只在自由回忆出现再认消失=解除抑制）— 第二独立域（综述一手全文）。
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC4644810/pdf/fpsyg-06-01741.pdf`（Bäuml 等《Forget me (not)?》Frontiers 全文 PDF WebSearch 逐字：选择性复述说 vs 提取抑制说、loudness illusion 策略证据）— 第三域（实验期刊全文）。
- `https://www.mdpi.com/2227-9059/10/7/1555/html`（《Obliviate!》2022 元分析 WebSearch 全文逐字：直接抑制 vs 替代两策略、额叶-海马 vs VLPFC/IFG 神经分离、剂量-反应）+ `https://www.sciencedirect.com/science/article/pii/S0010945221002422`（2021 EEG 逐字：Forget 额叶振荡 vs Imagine 表征相似度、16 次有效/8% 平均下降/重复失败）— 第四域交叉（立场登记）。
- **判重**：全库 SKILL.md 精确扫描 `directed forgetting`/`定向遗忘`/`intentional forgetting`/`选择性复述`/`release from inhibition` 在正文 0 命中；与本技能 §十三 r755A（系统自动 decay/eviction 双机制、遗忘四策略）/§r767A（RIF 练一条压同簇、换独立线索裁决）/§r751A（检索即改写、可及性≠保真度）分工不复用；与 r778(TI/PI/PDI)/r777(OI/EI/SI)/r776(AI/VI/DI) 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：fMRI/ERP 脑区坐标与振荡频段、多项模型的具体参数估计与拟合优度、临床创伤/创伤后遗忘应用、各实验样本量与年龄组差异（属实验细节或临床域，不迁移到 agent 记忆工程）。

## r783A · 编码特异性原则（encoding specificity）：线索效力来自"编码时与目标共存了什么"，不是语义相似度（MI · 2026-11-20 实拉，多独立域交叉）

> 来源：Tulving & Thomson (1973) 原始实验经 Simply Psychology 全文（WebFetch 被 Cloudflare 拦，以 WebSearch 该页全文逐字片段登记，第一手）+ Wikipedia《Encoding specificity principle》（WebFetch fetch failed，以 WebSearch 全文逐字片段登记，第二独立域）+ UCL Hardwicke 2016 博士论文 PDF WebSearch 全文逐字（cue-overload / memory-as-discrimination，第三域）+ 科普中国「线索依赖性遗忘」与百度百科「编码特异性原则」WebSearch 全文逐字（中文权威交叉，第四域）。

### 三独点
1. **线索的效力来自"它是否在编码时与目标一起被存下"，不是它与目标的通常语义关联强度**：Tulving & Thomson (1973) 逐字——受试学习"BLACK—train"这类弱配对，测试时先给强关联词 white 常**再认失败**，随后给原弱线索 train 却能**回忆出同一个词**；"recognition failure of recallable words" 推翻了"再认总优于回忆"的默认假设。判据：**记忆检索的键不是语义相似度排序，而是写入那一刻与目标共存的上下文/线索**；给一条记忆建检索线索，必须在写入时就把它与目标一起编码，事后补的语义近似词不产生同等效力。与 §r732B episode 溯源互补：那条管事实从哪个 episode 来，本条管 episode 内"哪些线索与目标绑定"。
2. **情境效应主要是"回忆现象"，测试供给强线索时消失——所以"取不出"不等于"没存"**：Godden & Baddeley (1975) 潜水员实验，岸上/水下学习与回忆四组合，环境匹配组回忆量高约 50%；1980 年同范式改测**再认**则无情境效应。判据：验收"记忆是否还在"必须换线索类型再测一次（自由回忆 vs 再认 vs 不同情境线索），单一路径取不出就判"已删"是错误结论——与 §r779A「accessibility≠availability 换线索验真删」同族，但本条给出"匹配编码情境"这一具体线索维度，并指出**测试本身供给强线索会抹平效应**。
3. **编码-提取匹配不是唯一决定因素，须与线索过载/判别竞争并报**：UCL 论文逐字——cue-overload principle（Watkins & Watkins 1976）：一个线索关联的痕迹越多效力越低；Nairne (2002) 与 Poirier 等 (2012) 的 memory-as-discrimination 假说认为表观的"匹配越好记得越好"很大程度是因为线索更易把目标从竞争者中区分出来；反例：线索 X 只关联目标 A，线索 Y 同时关联 A 与竞争者 B，X+Y 虽使 A 匹配度最高，却因 Y 引入 B 的竞争反而不如只用 X。判据：**加线索不是越多越好，优先只绑定目标的独占线索、避免共用线索引入竞争**；与 §r767A RIF（练一条压同簇邻居，检索的抑制后果）不同面，本条是线索设计的竞争面。

### 来源
- `https://www.simplypsychology.org/context-and-state-dependent-memory.html`（**WebFetch 被 Cloudflare 拦 block**，以 WebSearch 该页全文逐字片段登记：Tulving & Thomson 1973 BLACK-train/white 再认失败、Godden & Baddeley 1975 约 50%、1980 recognition null、Marian & Neisser 2000 双语线索）— 第一独立域（实验综述一手，降级如实登记）。
- `https://en.wikipedia.org/wiki/Encoding_specificity_principle`（**WebFetch fetch failed**，以 WebSearch 全文逐字片段登记：encoding depends on context、context words add/delete/replace 降 recognition、语义相关词未在编码时出现则无效、弱相关但编码在场胜过强相关但缺席、Tulving & Osler 1968）— 第二独立域（百科交叉，降级如实登记）。
- `https://discovery.ucl.ac.uk/1519819/1/thesis_Hardwicke_2016.pdf`（UCL 博士论文 WebSearch 全文逐字：cue-overload principle、Nairne / Poirier memory-as-discrimination、X/Y 线索反例、Godden & Baddeley 与 Eich 1975 状态依赖）— 第三域（学术论文一手）。
- `https://www.kepuchina.cn/article/articleinfo?business_type=100&ar_id=244499`（科普中国「线索依赖性遗忘」WebSearch 全文逐字：图尔文 1973 编码特殊性原理、巴德利内在/外在语境、鲍尔心境一致性）+ `https://baike.baidu.com/item/%E7%BC%96%E7%A0%81%E7%89%B9%E5%BC%82%E6%80%A7%E5%8E%9F%E5%88%99/53705432`（百度百科「编码特异性原则」WebSearch 全文逐字：2014《心理学名词》第二版界定）— 第四域（中文权威交叉，立场登记）。
- **判重**：全库 SKILL.md 精确扫描 `encoding specificity`/`编码特异性`/`情境依赖`/`context-dependent`/`Tulving` 在记忆类技能正文 0 命中本体（`meta/di-decision-tradeoff` §r715C-2 的 `context-dependent preference` 是 AHP 合成模式"偏好依赖参照系"，异命题判非）；与本技能 §r732B（episode 溯源）/§r779A（定向遗忘 accessibility vs availability）/§r767A（RIF 换独立线索裁决）/§r751A（检索即改写）分工不复用；与 r782(TI/PI/PDI)/r781(OI/EI/SI)/r780(AI/VI/DI) 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：Godden & Baddeley 的具体词表与回忆百分比精度、Eich 1975 大麻状态依赖的神经机制、Marian & Neisser 双语自传体记忆细节、Tulving 1973 原始实验被试数与统计检验（属实验细节或临床域，只取三条可机检口径）。

## r787A · 序列位置效应（serial position effect）：首因与近因是两套可分离的写入机制，不是一条记忆曲线（MI · 2026-11-22 实拉，多独立域交叉）

> 来源：Glanzer & Cunitz (1966)《Two storage mechanisms in free recall》经 PMC4226135《Neuroscientific Evidence About the Distinction Between Short- and Long-Term Memory》全文 WebFetch 200 逐字（双分离逻辑与两操纵，第一手）+ Cambridge 大学教材《Memory》第一章 PDF WebSearch 全文逐字（15 项三延迟条件、rehearsal buffer 首因机制，第二独立域）+ Athabasca University Press《Inferring Cognitive Processes》WebSearch 全文逐字（functional dissociation 推断逻辑、maintenance vs elaborative rehearsal，第三域）+ psychologysorted《Glanzer & Cunitz 1966》PDF WebSearch 全文逐字（原始程序四条件，第四域交叉）。

### 三独点
1. **首因与近因由两套机制产生，靠"双分离"而非单曲线判定——一个操纵只动一端**：Glanzer & Cunitz (1966) 逐字（PMC 全文）"a slowed presentation rate increased the primacy effect ... this did not modify the recency effect. By contrast, increasing the delay between the end of the list presentation and recall reduced the recency effect ... this manipulation, however, did not alter the primacy effect."；首因归 LTM（早期项被复述转入长期存储），近因归 STM（末项仍在短时存储中活跃）。判据：**验"一条记忆写入是否稳固"不能只看一次召回曲线，要用两个正交操纵各打一端**——放慢/重复写入只应抬高首因端，延迟+干扰（阻断复述）只应削平近因端；一端动另一端不动才算两套机制，两端同涨同跌说明是单一因素（如注意力总量）。与 §r751A「即时可及性 vs 延迟保真度」分工：那条测同一条记忆跨时间的漂移，本条测**序列不同位置**属于哪套存储。
2. **近因可被延迟+干扰任务抹掉，首因不动——"刚好写进去"不是"已经存下来"**：Cambridge 逐字 15 项三条件（immediate / 10s / 30s filled delay），"The recency effect was not observed following a 30-second delay in free recall testing"；Athabasca 逐字阻止复述（心算）使近因效应"even disappeared with sufficiently long recall delay"，而"delaying recall did not alter the primacy effect"。判据：**刚写入、尚在活跃缓冲里的条目属于"近因态"，一次干扰/上下文切换就会丢**；agent 把关键事实写进长期记忆后须以"延迟+插入无关任务后仍可取回"为落地门，不能拿写入当次即可命中当存证；这与 §r783A「取不出≠没存，换线索验真删」互补——那条换检索线索，本条换**写入后是否经过阻断复述的延迟**。
3. **首因端靠复述/加工，是"可控但有限容量"的资源分配，不是位置本身的魔力**：Cambridge 逐字 Rundus (1971) 出声复述实验——早期位置得到更多 overt rehearsals 因而更牢转入 LTM；Athabasca 逐字 presentation rate 加快→复述时间减少→首因下降，且 elaborative rehearsal（Craik & Lockhart 1972，把新项与已有知识联结）胜过 maintenance rehearsal（机械保持）。判据：**要让一条记忆进入"首因态"须给它分配独占的复述/精加工资源，且缓冲容量有限，先入先出会挤掉中段**；落地时把必须长期保留的约束排在开始处并显式精加工（关联既有规则/给理由），不要指望中段项自动稳固；但反对"单一存储"的证据也在（见下未采纳），本条只取可机检的双端操纵判据。

### 来源
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC4226135/`（WebFetch 200 全文逐字：Glanzer & Cunitz 1966 双分离逻辑、slowed presentation rate 只增 primacy、delay 只减 recency、MTL 早期 vs 顶叶晚期探针双分离；同文 unitary-store 反证段）— 第一独立域（综述论文一手全文）。
- `https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8278F5A00BE082D2F1F69B0482A0219D/9781009440394c1_1-26.pdf/introduction.pdf`（WebSearch 全文逐字：15 项三延迟条件、recency 在 30s 延迟后消失、rehearsal buffer 先入先出、Rundus 1971 出声复述）— 第二独立域（大学教材一手）。
- `https://read.aupress.ca/read/b0491aef-2323-45de-b66c-44a8a630b3fb/section/239a1b99-1257-440c-90f9-1d82937fd98b`（WebSearch 全文逐字：functional dissociation 推断两存储的逻辑、阻止复述使近因消失而首因不变、presentation rate 反向影响、maintenance vs elaborative rehearsal）— 第三域（开放教材一手）。
- `https://psychologysorted.blog/wp-content/uploads/2019/07/glanzer-and-cunitz_1966.pdf`（WebSearch 全文逐字：46 名美国陆军男性、15 表×15 词、immediate/10s/30s 干扰三条件、30s 近因消失首因保持、样本局限）— 第四域交叉（原始实验教程，立场登记）。
- **判重**：全库 SKILL.md 精确扫描 `serial position`/`系列位置`/`首因效应`/`primacy`/`recency effect` 记忆类正文 0 命中本体（`defaults/wb-context-compressor` 的 recency 0.25 是记忆价值函数的衰减因子，异命题且属豆包自留地 WB 0 落地）；与本技能 §r751A（检索即改写，同条跨时漂移）/§r767A（RIF 检索抑制）/§r779A（定向遗忘 accessibility≠availability）/§r783A（编码特异性换线索）分工不复用；与 r786(TI/PI/PDI)/r785(OI/EI/SI)/r784(AI/VI/DI) 九模块结论不复用。**豆包自留地 wb-execute-discipline / wb-context-compressor WB 0 落地**。
- **未采纳**：unitary-store 单一存储反证（PMC 同文 Ranganath & Blumenfeld 2005：MTL 损伤也损害新异信息的短时保持，双分离可作任务差异解释）——作为真实学术冲突如实登记，不否定双分离判据但也不冒充"两套存储已被证明"；Glanzer & Cunitz 原始被试数与统计检验细节、Brodie & Prytulak 呈现速率参数、fMRI 脑区坐标（属实验细节，只取可机检双端操纵判据）。

## r791A · 前摄/倒摄干扰（interference）：干扰发生在「学习两套材料之间」，与检索阶段抑制 RIF 正交（MI · 2026-11-22 实拉，多独立域交叉）

### 三独点
- **PI/RI 两向与 RIF 分工**：APA 逐字「proactive interference (PI): interference in new learning due to previous learning of similar or related material」＝旧学干扰新学；「retroactive interference ... new learning or exposure to new information impairs the ability to remember material ... previously learned」＝新学干扰旧学。两者都发生在**学习两套材料之间**，与 §r767A RIF（检索一套的子集反过来压同簇未练条）是不同阶段——判「记不住」先问是被另一套材料在学习时挤掉，还是检索时被同簇竞争抑制，对策不同（前者改写入隔离/键设计，后者换独立线索再测）。
- **AB/AC 范式 24h 自发恢复推翻「即时覆盖＝永久改写」**：Briggs 1954 先学 A-B 再学 A-C，即时 C 回忆超 B（RI），但延迟 24 小时后 B 自发恢复并超过 C（Wikipedia 逐字「once participants were tested after a delay of 24 hours the Bi responses spontaneously recovered and exceeded the recall of the Ci items」）⇒ 新值盖旧值在即时测量成立、延迟后旧值回潮；故 §r755A 矛盾消解单靠写入侧覆盖不够，检索侧必须带时间/版本信号，且验收要「写入后即时＋延迟」双测（与 §r747C 即时/延迟双栏、§r779A 换线索验真删同族不同面）。
- **相似性倒 U 与 release from PI**：完全相同＝复习无干扰、中等相似＝干扰最大、完全不同＝干扰最小（搜狗百科逐字「材料的相似性减小到了一定程度时...抑制作用最大...到两种材料完全不同时...最小」）⇒ 更新规则时「只改一点点、留两条高度相似但不同的记录」最危险，要么就地更新同一条、要么显式换键分家；APA 另列 release from proactive interference（换材料类别干扰骤降）可作「是否同簇竞争」的探测手段。

### 来源
- `https://d251dzbm8mzqab.cloudfront.net/proactive-interference`（**WebFetch 200 逐字**：APA 官方 proactive interference 定义、与 retroactive 对照、release from PI 词条）— 第一独立域（学会官方词条一手）。
- `https://d251dzbm8mzqab.cloudfront.net/retroactive-interference`（**WebFetch 200 逐字**：APA 官方 retroactive interference 定义「new learning ... impairs the ability to remember material or carry out activities previously learned, especially if the two sets of material are similar」）— 同一学会第二词条。
- `https://psychologydictionary.org/interference/`（**WebFetch 200 逐字**：Underwood 1957 干扰与遗忘、PI/RI 双向定义、相似材料干扰、新旧密码/语言例、similarity-based interference）— 第二独立域（心理学辞典一手）。
- `https://en.wikipedia.org/wiki/Interference_theory`（**WebFetch 失败如实登记**；**WebSearch 逐字**：配对形容词 70%/40%/25% 三列表递减、Briggs 1954 AB/AC 与 24h 自发恢复、RI 含 unlearning 不只 competition）— 第三域（WebSearch 逐字，不冒充全文）。
- `https://baike.sogou.com/v7694162.htm`（**WebFetch 200 逐字**：前摄抑制/倒摄抑制中文定义、相似性从全同到全异的倒 U、首段只受倒摄/末段只受前摄、中间双重受扰）— 第四域交叉（科普词条立场登记）。
- **判重**：全库 SKILL.md 窄串 `前摄抑制`/`倒摄抑制`/`proactive interference`/`AB-AC 范式`/`自发恢复` 正文命中仅在豆包自留地 `defaults/wb-context-compressor/references/knowledge-base.md`（三处，均是「无界记忆退化三机制」里的一个词组，无范式/恢复/倒 U，口号级），WB 主线技能 0 命中本体；与 §r767A RIF（检索抑制）、§r787A 序列位置、§r779A 定向遗忘、§r755A 矛盾消解位置分工不复用；与 r790(TI/PI/PDI)/r789(OI/EI/SI)/r788(AI/VI/DI) 九模块结论不复用。**豆包自留地 wb-execute-discipline / wb-context-compressor WB 0 落地**。
- **未采纳**：被试人数与脑区定位、Brown 1968 / Shea & Zimny 1983 技能迁移细节、相似性的精确数学形式（学界无统一模型），人类被试结论迁移 agent 按 rules/08 §五作待验证假设只取三可机检口径。
## 双过程再认：熟悉感是连续强度，记得才是带来源的阈值检索（r795F 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）

§错误记忆/来源监控管「高置信≠真实」，本章补认知层的分离机制——相似度命中只给 familiarity，来源与顺序来自 recollection，二者不是同一个标量的强弱。

**独点1** 双通道输出：检索须分别给出连续相似度（familiarity，d′/ROC 曲率）与阈值式细节命中（recollection，含 source_id/span/timestamp/context）；只有单一标量判「不可区分熟悉与记得」。Yonelinas 2010 逐字：familiarity 是 quantitative memory strength、recollection 是 threshold retrieval「recall detailed qualitative information…where or when」。

**独点2** 来源可追溯门槛：命中只有 similarity score 而无来源/时间/上下文时，标签固定为 `familiarity-only`，不得写「已记忆/可追溯」。Eichenbaum 2005 逐字：familiarity「offers no information about the order of events」——顺序与情境只有 recollection 给。

**独点3** 评测双口径：在变化的置信阈值下分别报告 hit vs false alarm，并给出 ROC 截距（recollection）与弯曲度/d′（familiarity）；另设 inclusion / exclusion 两条件（PDP：允许用来源 vs 要求排除仅熟悉项）估两过程贡献 `I=R+F−(R×F)`。只报单一 accuracy 判不合格。

- **判重：`familiarity` 本体仅 §r747A「熟悉感错觉」一句（巩固效用评级语境），`recollection`/ROC/PDP 专节 0；与本模块错误记忆、编码特异性分工不复用。豆包自留地 WB 0 落地。**
- **来源与诚信**：https://pmc.ncbi.nlm.nih.gov/articles/4251874/?report=classic（Yonelinas/Aly/Wang/Koen，Hippocampus 20(11)，2010-11，WebFetch 200 逐字：定量强度 vs 阈值检索 / d′ 与 ROC 截距）；https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13407481/fullTextXML（Balota，Memory & Cognition 54(5)，2026-01-30，WebFetch 200 逐字：PDP inclusion/exclusion / I=R+F−(R×F)）；https://pmc.ncbi.nlm.nih.gov/articles/PMC1389783/?report=classic（Eichenbaum & Fortin，J Exp Anal Behav，2005，WebFetch 200 逐字：全有全无 vs 连续增量 / 熟悉不提供顺序 / 截距与曲率）。PMC 默认 URL 返回 HHS 拦截页，改 ?report=classic 成功；Yonelinas 原始 PDF 403 未强取。 逐字全文与判非见 `references/r795F_双过程再认.md`。
## 测试效应：检索不是中性读取，短时重读占优、延迟测试占优（r796F 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）

§双过程再认管「熟悉与记得分离」，本章管**每次检索本身会改造记忆**：把「多复习几遍」换成「分散地提取」，才对延迟保持有效。

**独点1** 短期/延迟交叉反转必须写出：5 分钟后重复学习优于重复测试，但延迟测试（2 天/1 周）下先前测试保持显著更好，即使重复学习提高了学习者信心（Roediger & Karpicke 2006 逐字）。判据——只写「测试永远优于重读」或只写「多复习几遍」均不合格。

**独点2** 机制锚点：提取会直接强化记忆表征（「retrieve … directly strengthen the memory representation」），recall 式测试收益大于 recognition 式多选题；判据——方案无 retrieval 动作、只有 exposure/重读，判「未命中测试效应」。元认知错觉须写进结论：重读提升 confidence 却不提升延迟保持。

**独点3** 三要素可机检：retrieval（recall 非 recognition）+ spacing（分散而非集中，study time is distributed）+ feedback（增强但非必需）；判据——agent 记忆检索「每次检索都强化特定路径」是人类被试结论的跨领域类比，必须标注推断不得当实证引用。

- **判重：`测试效应`/`testing effect`/`retrieval practice` 本体 0 命中（retrieval practice 仅豆包自留地一句），与 §r795F 双过程再认、§巩固效用分工不复用。**
- **来源与诚信**：https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x（Roediger & Karpicke，Psychological Science 17(3)，2006，WebFetch 200 逐字：testing effect 定义/5min 与延迟反转/信心提升但保持更差）; https://journals.sagepub.com/stoken/rbtfl/dEzGRXuJ8AzLI/full（Rohrer & Pashler，Educational Researcher 39(5)，2010，WebFetch 200 逐字：提取直接强化表征/测试+学习优于等时重读/分散学习/回忆优于再认）。无 WebFetch 失败。agent 外推已标推断。 逐字全文与判非见 `references/r796F_测试效应.md`。
