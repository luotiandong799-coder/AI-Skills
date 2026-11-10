---
name: mi-memory
description: 长期记忆治理（Memory Intelligence）。当任务涉及"该记什么/不该记什么"的判断、用户级 MEMORY.md 与模块记忆分层、跨会话记忆的写入/检索/去重、记忆容量与检索侧治理权衡、个人文件与隐私不入记忆、记忆可靠性与可恢复性、事实失效与双时态时间戳、按来源删除级联、记忆系统评测五能力、以及判断是否要固化长期规则时使用。是 13 模块中 MI 的载体。
version: 1.2.0
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
