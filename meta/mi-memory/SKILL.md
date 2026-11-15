---
name: mi-memory
description: 长期记忆治理（Memory Intelligence）。当任务涉及"该记什么/不该记什么"的判断、用户级 MEMORY.md 与模块记忆分层、跨会话记忆的写入/检索/去重、记忆容量与检索侧治理权衡、个人文件与隐私不入记忆、记忆可靠性与可恢复性、事实失效与双时态时间戳、按来源删除级联、记忆系统评测五能力、以及判断是否要固化长期规则时使用。是 13 模块中 MI 的载体。；记忆巩固效用评级（十技法四变量/熟悉感错觉/即时与延迟双栏/desirable difficulty）。
version: 1.5.0
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
