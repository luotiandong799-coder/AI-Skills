---
name: mi-memory
description: 长期记忆治理（Memory Intelligence）。当任务涉及"该记什么/不该记什么"的判断、用户级 MEMORY.md 与模块记忆分层、跨会话记忆的写入/检索/去重、记忆容量与检索侧治理权衡、个人文件与隐私不入记忆、记忆可靠性与可恢复性、事实失效与双时态时间戳、按来源删除级联、记忆系统评测五能力、以及判断是否要固化长期规则时使用。是 13 模块中 MI 的载体。
version: 1.4.0
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
