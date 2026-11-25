---
name: personal-ai-employees
description: >-
  个人 AI 员工体系（8 岗）总路由与五步执行协议。把用户目标自动分派给 8 个专职 AI 员工（战略顾问/供应链专家/职业发展顾问/销售顾问/学习教练/信息分析师/自动化工程师/知识管理专家），每岗统一走「任务分析→执行方案→输出结果→复盘优化→Skill沉淀」，并复用 personal-ai-os 与现有 wb-* / 专家技能，不新建重复能力。触发词：个人AI员工、AI员工体系、AI战略顾问、AI供应链、AI职业发展、AI销售顾问、AI学习教练、AI信息分析、AI自动化工程师、AI知识管理、哪岗来做、分派任务、员工路由、agency、个人AI公司、我的AI团队。finalizer、终结器、两阶段删除、deletionTimestamp、finalizers 清空、删除钩子、owner reference 清理、卡住的 finalizer、强制删除 unsafe-delete、孤儿资源清理。Actor模型、actor、消息传递、mailbox、无共享状态、位置透明、有状态worker。工作流确定性、非确定性错误、replay重放、Event History、Command比对、版本化patch、Worker Versioning、SideEffect、计时器顺序
version: 1.14.0
agent_created: true
module: OI
modules: OI,MI
---

# 个人 AI 员工体系｜8 岗路由 + 五步执行协议

> **定位**：你 = 用户的 Personal AI OS 编排层；本技能 = 在「领域角色」维度上的**路由器 + 执行协议**。
> 用户是 CEO，8 个 AI 员工是专职岗位；WorkBuddy 按本技能判岗、路由、跑协议，具体执行下沉到现有能力。
> **设计哲学（agency-agents）**：少而精。8 个清晰角色，不堆 agent；每个角色有明确边界、输入输出契约、统一生命周期；执行能力 100% 复用现有 Skill/MCP，本技能只新增「领域人设知识」与「路由/协议」，绝不重造工具。

---

## 一、组织图（8 岗 + 路由落点）

| # | 岗位 | 定位 | 核心职责 | 首选现有能力（路由落点） | 何时分派 |
|---|---|---|---|---|---|
| 1 | **AI 战略顾问** | 个人 AI 公司 CEO 顾问 | AI 趋势 / 商业机会 / 职业优先级 / 项目排序 / 决策分析 | `agent-reach`+`web-scrape`（情报）、`wb-doc-writing`（输出）、个人推理做决策 | 「AI 下一步往哪走 / 这个项目值不值得做 / 机会判断」 |
| 2 | **AI 供应链专家** | 专业领域专家（你的老本行） | WMS/TMS 分析、仓储运营优化、自动化物流、供应链方案、行业/竞企研究 | `references/domain-expertise.md`（领域知识）、`web-scrape`（行业）、`wb-doc-writing` | 「仓库怎么优化 / 这个物流方案 / 供应链诊断」 |
| 3 | **AI 职业发展顾问** | 求职与成长教练 | 岗位分析、JD 匹配、简历优化、面试训练、路径规划 | `resume-ai-help`（简历）、`wb-doc-writing`、`wb-teaching` | 「帮我改简历 / 面 XX 岗怎么准备 / 职业路径」 |
| 4 | **AI 销售顾问** | B2B 销售教练 | B2B 策略、客户画像、商业沟通、方案设计、谈判准备 | `references/domain-expertise.md`（销售知识）、`wb-doc-writing` | 「怎么搞定这个客户 / 写个销售方案 / 谈判话术」 |
| 5 | **AI 学习教练** | AI 技术学习规划 | 学习规划、Agent 学习、Skill 优化、工具评估、学习总结 | `wb-teaching`、`agent-reach`、`wb-skill-authoring`（Skill 优化） | 「怎么学 Agent / 这个工具值不值得学 / 学习路线」 |
| 6 | **AI 信息分析师** | 情报筛选官 | AI 行业情报、科技趋势、商业机会、公司/市场分析 | `agent-reach`+`web-scrape`、`personal-ai-os` 附录 B4（AI Radar） | 「最近 AI 圈有什么 / 某公司值不值得关注 / 趋势简报」 |
| 7 | **AI 自动化工程师** | WB 自动化建设 | WB Skill 设计、MCP 连接、工作流、自动化优化、减重复任务 | `wb-skill-authoring`、`wb-debug-loop`、`find-skills`、personal-ai-os §二十七/二十八 | 「做个 Skill / 接个 MCP / 把这个流程自动化」 |
| 8 | **AI 知识管理专家** | 第二大脑管家 | 知识整理、Skill 归档、方法论沉淀、长期记忆优化 | `meta/knowledge-governance`、`personal-ai-os` 附录 B5（Personal Knowledge） | 「整理下我的知识 / 这个方法该不该存 / 清掉重复笔记」 |

**映射结论**：6 岗已有现成执行能力（路由即可）；只有 **#2 供应链** 与 **#4 销售** 缺领域人设，由 `references/domain-expertise.md` 补；**不新建任何工具型 Skill**。

---

## 二、任务分派路由（判岗逻辑）

**先过「是否需要岗位」闸门**——岗位是组织复杂工作的方法，不是所有任务的必经入口：

```
用户说「我要做什么」
  → ⓪ 闸门：简单/明确/低风险，且现有最小能力能直接完成？→ 直接执行，不判岗、不进五步协议
  → ① 意图+关键词分类（见上表「何时分派」）
  → ② 命中单岗 → 加载该岗协议（见第三节），并从「首选能力」加载真实执行技能
  → ③ 命中多岗 → 指定主岗（产出 Owner）+ 协岗（提供输入），明确分工边界
  → ④ 不属于任何岗（纯电脑操作/清理/装环境）→ 不分派，直接走 personal-ai-os 对应模块
```

- **⓪ 闸门判据**（命中任一即跳过岗位路由）：单步或 ≤2 步可完成 · 目标明确无歧义 · 低风险（L0/L1）·
  已有单一技能能直接做完 · 不需要领域人设或跨专业协作。
- **需要岗位路由的情况**：领域专家判断（供应链 / 销售 / 战略）· 复杂决策 · 多专业协作 ·
  长周期工作 · 用户明确要求员工角色。
- **反模式**：用户问一句普通问题 → 先判断 8 个岗位 → 选岗 → 再路由 → 再执行。多一层无意义路由，必须避免。

- **判岗前先查**：`personal-ai-os` 附录 A 能力总表 + 本技能第一节表，确认落到哪个现有能力，不重复加载。
- **多岗协作样例**：「用 AI 给供应链客户做销售方案」→ 主岗 #4 销售顾问（方案 Owner），协岗 #2 供应链专家（提供行业/方案正确性校验），输出前过 #8 知识管理（沉淀方法论）。

---

## 三、五步执行协议（每岗统一）

每岗处理任务时，固定走五步，**每步都要有显式产出**，不得跳步：

### 1. 任务分析（Analyze）
- 拆目标：用户真正要什么 / 对象 / 预期结果 / 范围边界 / 时间。
- **先查已有能力**：本岗「首选能力」是否已能直接做？已有 Skill/知识/MCP 是否覆盖？**能复用就不新建**。
- 输出：一句目标重述 + 关键约束清单 + 是否需多岗协作。

### 2. 执行方案（Plan）
- 给最小可行方案：步骤、用哪个现有能力、依赖、风险（L0/L1/L2 级）、预期产出。
- 复杂任务自动拆子任务，明确先后顺序与并行度（遵循 personal-ai-os §九·五 最短路径）。
- 输出：可执行方案（编号步骤 + 每步工具/技能 + 验收点）。

### 3. 输出结果（Output）
- 按岗位契约产出：战略顾问=结论+依据+风险+建议；供应链/销售=方案+测算/话术；其余按表。
- 结论先行、去 AI 味（遵循 `humanizer-zh` / `wb-max-token-saver`）；不编数据。
- 输出到 **D 盘正式目录**（`D:\腾讯AI\yt\outputs\<日期>_<主题>\`），不落 C 盘。

### 4. 复盘优化（Review）
- 自动回答：什么方法有效？哪步卡住？是否值得沉淀 Skill？流程能否优化？
- 对照 personal-ai-os §十三 验证六问做结果校验。

### 5. Skill 沉淀（Crystallize）
- 仅当确有**可复用、长期有价值**的方法论 → 落进：① 现有 Skill（更新而非新建）② `meta/knowledge-governance` 知识库 ③ 本岗 `references/domain-expertise.md`（领域新知）。
- 判据：能提升 模型/工具/工作流/可复用 Skill 中哪一层？答不出 → 不沉淀。
- **禁止**：保存无价值聊天记录、把一次性结论当长期知识。

---

## 四、复用与去重纪律（用户硬性要求）

1. **落地前查三张表**：personal-ai-os 附录 A + 本节一 + 领域参考；已有能力优先。
2. **只取独特点**：与已有 wb-* 重叠 >60% 的不装、不重复写；两边各有长处 → 合并成一个（保留双方好点），差的删。
3. **领域专家只新增「人设/领域知识」**，不新增工具——工具全走现有 Skill/MCP。
4. **单轮 0 新增** 也合法：回溯候选池或重读历史好方法确认已集成，不得编造 idle 改动。
5. 定期审计：拼写/乱码/失效工具名/过时信息（复用 personal-ai-os §三十四/三十五）。

---

## 五、禁止项（来自用户，强制）

- ❌ 创建大量重复 Agent（用路由替代新建）。
- ❌ 保存无价值聊天记录（只存长期有价值内容）。
- ❌ 自动执行高风险操作（删重要文件/发外部消息/支付等 → 走 personal-ai-os L2 确认）。
- ❌ 未确认发送外部消息（微信/邮件/任何出站，必须先取得明确确认）。

---

## 六、与 personal-ai-os 的关系

- `personal-ai-os` = **基础设施/执行纪律层**（九大模块、三级权限、停止条件、清理、审计）。
- 本技能 = **领域角色路由 + 五步交付协议层**。
- 本技能触发后，具体执行**仍服从** personal-ai-os 的三级权限 / 停止条件 / 验证 / 清理 / 证据优先等全部规则。两者不冲突，本技能不重复实现它们。

---

## 七、领域知识加载

- 处理 **#2 供应链** 或 **#4 销售** 任务时，先 `Read references/domain-expertise.md` 加载领域框架与用户专业锚点，再以专家视角产出，避免泛泛而谈。
- 其他 6 岗无需加载该文件，直接路由到对应现有技能。

## 八、扇出闸门与编排预算（OI · 2026-11-08 实拉加厚）

> 本机已有「⓪ 闸门：简单任务不判岗」与「五步协议」。本节补**决定要不要 fan-out、fan-out 到几路、失败怎么续跑**的编排层判据；与 `wb-subagent-delegation` 的「双模型主-副手」互补，不重复实现调度器。

### 8.1 先选编排形态，再谈分派：三态 + 五问闸门
| 形态 | 适用 | 成本 | 可调试性 |
|---|---|---|---|
| 单 agent（单循环单窗口） | 任务放进一个窗口、步骤天然串行 | 基线 ~1× | 最高 |
| 固定流水线（DAG） | 步骤事先已知且稳定、要确定性 | 低–中、可预测 | 最高 |
| orchestrator-worker（并行子代理） | 子任务**独立可并行**、信息量超单窗口、接大量复杂工具 | 高（官方实测约为 chat 的 15×） | 最低（跨轮非确定） |
- 五问闸门（**任一为否 ⇒ 降一档**）：① 子任务真的互相独立？（B 需要 A 的输出 = 流水线，不是 fan-out）② 工作是否超出单个上下文窗口？③ 并行是否真实？（官方："most coding tasks involve fewer truly parallelizable tasks than research"）④ 任务价值是否高到付得起 token 溢价？⑤ 非确定性是否可观测、可调试？
- 官方不适域逐字："some domains that require **all agents to share the same context** or involve **many dependencies between agents** are not a good fit for multi-agent systems today."
- 判据：**选最便宜够用的一档**；「加一个 agent」不是默认优化动作。与已落「少而精、8 岗不堆 agent」同向，本节给的是可机检的选择题而非态度。

### 8.2 并行度要两层同时开，才拿得到量级收益
- 官方原则 8 逐字："we introduced two kinds of parallelization: (1) the lead agent spins up **3-5 subagents in parallel** rather than serially; (2) the subagents use **3+ tools in parallel**. These changes **cut research time by up to 90%** for complex queries."
- 判据：① 只并行一层（只起子代理但每个仍串行搜索，或反之）拿不到这个量级 ⇒ 排查「并行了却没变快」先数**两层各开了几路**；② 早期失败形态是「串行搜索」与「为简单查询起 50 个子代理」，两端都属**并行度与任务复杂度不匹配**；③ 提速收益要连同成本一起报（此即 8.1 的第 ④ 问）。

### 8.3 方差归因决定优化顺序；长跑从出错点续跑
- 官方："three factors explained **95% of the performance variance** in the BrowseComp evaluation … **token usage by itself explains 80%** of the variance, with the number of tool calls and the model choice as the two other explanatory factors"；且"upgrading to Claude Sonnet 4 is a **larger performance gain than doubling the token budget** on Claude Sonnet 3.7"。
- 生产侧："we can't just restart from the beginning: restarts are expensive and frustrating … built systems that can **resume from where the agent was when the errors occurred**"；"combine the adaptability of AI agents with deterministic safeguards like **retry logic and regular checkpoints**"；并让模型知道工具正在失败以便自适应。
- 判据：① 优化顺序应是**先换模型档 / 再看预算 / 最后加 agent**，不是先扩 token 预算；② 方差归因是**三因素**，「token 解释 80%」不等于「另外 20% 不重要」；③ 长跑 agent 的恢复点必须落在最近检查点，**重启 = 昂贵且恼人**，柔性自适应与确定性护栏是互补不是二选一；④ 评估复杂流程用「离散检查点验证状态是否变化」，不要逐中间步全验。

## 九、恢复语义：checkpoint 不等于可恢复，重试不等于恢复（OI · r738A 2026-11-11 实拉，三独立域交叉）

§8.3 的 "resume from where" 与 "regular checkpoints" 给出了长跑 agent 的恢复点，没有回答「恢复时凭什么敢跳过已完成步骤」。持久化执行（durable execution）的答案是：编排本身不持有状态，状态在服务端的 Event History 里，Worker 靠**重放历史**重建决策；因此 "same history, same Workflow decisions" 是硬约束，不是优化目标。

- **（r738A-1）重试是战术，恢复是策略，两者不共用一套计数**。官方逐字："Retry is a tactic where we are re-executing a failed operation." / "Recovery is a strategy where resuming a workflow from a known good state without re-executing completed steps." / "Do not use application-layer retries as a substitute for durable state." ⇒ 应用层的 `for i in range(3)` 在 Worker 崩溃时计数归零（"if the worker crashes on attempt two, the retry count resets"），而服务端协调的 activity 重试让 "retry count, back-off timing, and failure state survive any worker restart"。判据：① 编排层的恢复资格由**外部历史**判定，不由进程内计数器判定；② "已完成步骤不重跑" 要能举证（历史里有记录），否则只是"从头再来了一次且恰好幂等"；③ 迁移到多 agent 长跑时，先问"checkpoint 存的是结果还是可重放的事件序列"。
- **（r738A-2）确定性约束落在编排代码，副作用落在 Activity，边界按「碰不碰外部系统」划**。Temporal 官方逐字："The Temporal Platform requires that Workflow Definitions are deterministic." / "Non-deterministic work such as API calls, and database queries should be placed in Activities, which Temporal retries reliably."；官方 FAQ 对 LLM 更严："Workflow code must be deterministic — it is replayed from history whenever a Worker recovers from a failure."，同一 prompt 两次调用可能不同，故 LLM 调用、prompt 本身、凭据读取都必须进 Activity（"Prompt versioning and replay safety"）。判据：① 编排代码里出现 `random` / `now()` / 直接 HTTP / 遍历无序 map，重放时可能产出与历史不同的 Command 序列 → nondeterminism error；② 换 prompt 只影响新执行、在飞执行仍按历史里的 Activity 结果重放，这本身就是版本隔离；③ 凭据不要从 Workflow 参数传（会被序列化进历史），在 Activity 内从 secret store 取。
- **（r738A-3）幂等键与补偿动作是设计期产物，编排代码改动要给在飞执行留桥**。官方逐字："A Retry Policy makes Activity completion observable exactly once, but it does not make the Activity code execute exactly once."；幂等键用 Workflow Run ID + Activity ID 组合，**不要含 attempt number**（重试间必须稳定）。补偿："Compensating activities must be defined at the time the forward activity is written, not after a partial failure is observed in production."；改编排逻辑会破坏重放，故需 Worker Versioning 或三步 Patching（`patched()` → `deprecate_patch()` → 旧执行退留存后移除），官方 danger 注记 2025 年前的实验版 Worker Versioning 于 2026-03 从 Server 移除。判据：① 每个写操作配一个与尝试次数无关的幂等键 + 一个已写好的反向动作；② "exactly once 可观测" 不等于 "副作用只发生一次"；③ 部署新编排前问"有没有在飞执行会拿旧历史重放新代码"，有则先 patch 再发；④ 事后补恢复被标注为 3–5× 成本（xgrid，商业立场登记）。

**判非**：`deterministic` / `replay` 在本载体已有命中（§8.3 regular checkpoints、Anthropic 长跑恢复），本轮**不复用**该层，只补"凭什么可恢复"的确定性/幂等/版本化三层；`idempotency key` / `event history` 全库命中集中在 agent-guild 的审批/审计语境（Cap31/Cap51），与编排恢复语义不同族，不判为重复。窄串 `nondeterminism error` / `patch marker` / `deprecate_patch` / `compensating activit` / `replay test` / `continue_as_new` 全库 0 命中（本批机检）。

## 十、来源（2026-11-08 首拉 / 2026-11-11 r738A 增补）
- Anthropic Engineering《How we built our multi-agent research system》（2025-06-13）**一手全文 WebFetch 逐字核验**：90.2% / 95%·80% / 4×·15× / 3-5 subagents / 3+ tools / up to 90% / resume from where / regular checkpoints / rainbow deployments → https://www.anthropic.com/engineering/multi-agent-research-system
- BackendBytes《Designing a Multi-Agent Backend: The Orchestrator Pattern》三态决策表与五问（独立交叉）→ https://backendbytes.com/articles/multi-agent-orchestrator-backend
- The Daily Brief 独立摘要（八条 prompt 原则、评测与生产章节结构交叉）→ https://www.beri.net/learning/anthropic-multi-agent-research-system
- Back From The Future《Workflows vs Agents》（fan-out 适用边界独立交叉）→ https://www.backfromthefuture.nl/en/insights/workflows-vs-agents
- 判非登记（豆包自留地，WB 不重复落地）：`effort scaling 三档` 见 `wb-execute-discipline/KB:994`、`rainbow deployments` 见 `wb-execute-discipline/KB:999`、`15×/4× token 与 BrowseComp 80%` 见 `wb-context-compressor/KB:3619,5229`（均为二手引述）。本轮只取全库 0 命中的 `3-5 subagents / 3+ tools / 95% of the performance variance / resume from where / regular checkpoints` 与一手三态闸门。

### 2026-11-11 r738A 增补来源（三独立域交叉，逐字核验）
- `docs.temporal.io/develop/python/workflows/versioning`（Temporal 官方，WebFetch 200 全文逐字：deterministic / Activities / 两种 Versioning / patched 三步 / deprecate_patch / 2026-03 danger 注记）
- `go.temporal.io/platform-hub/faqs`（Temporal 官方 FAQ，搜索快照逐字：LLM 必须进 Activity、continue_as_new、凭据在 Activity 内取、Prompt versioning and replay safety）
- `learn.temporal.io/tutorials/go/background-check/durable-execution/`（Temporal 官方教程，搜索快照逐字：Replay test / intrinsic non-determinism / 随机·时钟·map 遍历清单 / nondeterminism error 日志）
- `www.xgrid.co/resources/temporal-recover-instead-of-restart/`（独立第三方一手 WebFetch 200 全文逐字：retry vs recovery / idempotency key / saga upfront / 3–5x retrofitting；厂商立场登记）
- `github.com/Nevaberry/nevaberry-plugins/.../workflows-activities-and-replay.md`（Temporal 知识补丁镜像，搜索快照逐字：attempt-independent key 不含 attempt number / replay-safe values / Replay guards observability-only）
- 判非登记：`docs.temporal.io/encyclopedia/determinism` 与 `/workflow-execution/workflow-determinism` 均 **WebFetch 404**，如实登记、未冒充一手；改由官方 versioning 页 + 官方 FAQ + 官方教程三页交叉补足。
## 十一、资源池槽位与排队优先级：并发预算不是「任务数」（r748C 实拉 · 2026-11-15，3 独点）

> 适用：多 Agent / 多子任务 / 多工作流并行时的容量分配与执行顺序。
> 与 §八分工：§8.1–8.3 管「要不要扇出、并行几路、优化顺序」；本节管「扇出后谁先拿到资源、每路占多少容量」。与 §九分工：那条管失败后怎么续，本节管没失败时的排队秩序。

### 11.1（r748C-1）★并发预算的单位是「资源槽」不是「任务数」，且存在一层隐式天花板
- Airflow 3.4.0 官方《Pools》逐字：pools「can be used to **limit the execution parallelism on arbitrary sets of tasks**」，按名称分配 worker slots；「if tasks are not given a pool, they are assigned to a default pool `default_pool`, which is **initialized with 128 slots** and can be modified through the UI or CLI (**but cannot be removed**)」。
- `pool_slots` 让单个任务占多槽：官方 2 槽池算例里 `heavy_task` 占 2 槽即耗尽池，两个 `light_task` 各占 1 槽可并发，而 heavy 「would have to wait for **two** pool slots to become available」；「in terms of resource usage, the heavy task is **equivalent to two light tasks running concurrently**」。池级还可选是否把 **deferred tasks 计入已占槽**（3.4.0 新增）。
- 判据：**编排预算表固定写四栏**——每类任务占几槽 / 池总槽 / 未指定池时的默认值 / 挂起任务是否仍占槽。只写「并发数 = N」会把 `default_pool` 的隐式 128 当成无限，也会把重任务与轻任务等价计价。分派前先问「这一路打的是哪个外部系统的容量」，把共享同一瓶颈的任务归进同一个池。

### 11.2（r748C-2）★优先级是排队排序规则，不是抢占；默认 `downstream` 会把下游权重加到上游
- Airflow 3.4.0 官方《Priority Weights》逐字：「`priority_weight` **defines priorities in the executor queue**」、默认 `1`、「larger numbers mean higher priority」；每个任务的 **true weight** 由 `weight_rule` 计算，三法：`downstream`（默认，effective weight = 所有**下游**后代权重之和 ⇒「**upstream tasks will have higher weight**」，适合先把所有 dag run 的上游跑完）、`upstream`（相反，适合逐个 dag run 做完）、`absolute`（精确值，且「**significantly speeding up the task creation process**」用于超大 DAG）。ASF #15183 commit diff 原文「the highest summed value wins」。
- 关键时序：pools 页逐字「Tasks will be **scheduled as usual while the slots fill up**. Once capacity is reached, runnable tasks get **queued** … As slots free up, queued tasks start running based on the Priority Weights」⇒ **优先级只在槽满排队时生效**，槽没满不产生顺序差异。32 位整数限制（2,147,483,647 / −2,147,483,648）也是官方明写的边界。
- 判据：**报告优先级必须同时写明 `weight_rule` 与所属 pool**。「给关键任务调高权重」在默认 `downstream` 下可能先抬高它的全部上游，意图与效果相反；要精确控制用 `absolute`。自定义 `PriorityWeightStrategy` 自 **2.9.0** 起且官方标 **experimental**；官方示例 `DecreasingPriorityStrategy` 让权重随 `try_number` 递减 ⇒ **重试次数会改变排队位次**，故障期的执行顺序不能用静态优先级表预测。

### 11.3（r748C-3）★容器不继承资源约束，三层预算互相独立
- 官方 warning 逐字（pools 页 + ASF #15183 diff）：「**Pools and SubDAGs do not interact as you might first expect. SubDAGs will not honor any pool you set on them at the top level; pools must be set on the tasks inside the SubDAG directly**」⇒ 在父容器上设的容量约束不会下沉到子任务，分组/嵌套结构必须逐层显式声明。
- ASF #15183 官方 config diff 给出三个**独立旋钮**：`parallelism = 32`（「the maximum number of task instances that can run concurrently … **regardless of scheduler count and worker count**」）、`dag_concurrency = 16`（单 DAG 所有 run 的运行实例累加）、`max_active_runs_per_dag = 16`（活跃 run 数）。三者改一个不影响其余；`pool` 是第四层（按任务集合）。
- 判据：**编排验收分列四层**（全局实例数 / 单工作流所有批次 / 活跃批次数 / 资源池槽）并逐层核对，任一层的「已限流」不能替代其余。跨版本语义会变（1.10.2 无 `pool_slots` 且优先级为「summed with downstream、highest wins」；2.2.4 引入 `pool_slots`；3.4.0 引入 deferred 占槽开关与自定义 weight rule），引用具体数值必须**绑定版本**，不把某版本默认值写成通用工程事实。

**提升层**：可复用 Skill（容量与排队验收清单）/ 工作流（并发预算表）/ OI 编排（扇出后的资源治理）。触发词：pool_slots、default_pool 128、weight_rule downstream、absolute、priority_weight、deferred tasks、SubDAG 不继承、parallelism 与 dag_concurrency、排队优先级、资源槽、并发预算四层。

**来源（r748C 独立实拉 2026-11-15，≥2 独立域交叉）**：
- `https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/pools.html`（Airflow **3.4.0 官方**，WebFetch **200 全文逐字**：limit the execution parallelism on arbitrary sets of tasks、`pool_slots` heavy/light 算例、`default_pool` 128 槽不可删、deferred tasks 占槽可选）——**第一独立域（Apache 官方规范一手）**。
- `https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/priority-weight.html`（Airflow 3.4.0 官方，WebFetch **200 全文逐字**：三种 weight_rule 定义、默认 downstream、32 位整数上下界、自定义策略 2.9.0 起 experimental、DecreasingPriorityStrategy 示例）——**第二独立域（同官方不同规范页）**。
- `https://lists.apache.org/thread/fojrbyb76jh6jto0xwj8qk704prfxtqo`（ASF 官方邮件归档 · commit #15183 `38ecbd6`，WebFetch **200**；**AI 摘要 60s 超时 → 前 15,000/31,653 字原文逐字，如实登记**：`parallelism=32` / `dag_concurrency=16` / `max_active_runs_per_dag=16` 三层定义、priority-weight.rst 新增 61 行三法全文、「the highest summed value wins」旧文、Pools and SubDAGs warning）——**第三独立域（官方源码变更一手 diff）**。
- `https://lists.apache.org/thread/9wwzyxt75khs92jnfn53mh06xs6rtgqv`（ASF commit #20257 `pool_slots` 文档，WebSearch 快照逐字）+ `https://airflow.apache.org/docs/1.10.2/concepts.html` · `/docs/apache-airflow/2.2.5/administration-and-deployment/pools.html` · `http://airflow.org.cn/docs/apache-airflow/3.2.0/administration-and-deployment/pools.html`（三个官方/社区版本页，WebSearch 快照逐字：跨版本语义演化核对）——**第四、五独立域（多版本归档交叉）**。
- **判非**：`pool_slots` / `default_pool` / `weight_rule` / `priority_weight` / `128 slots` / `排队优先级` 全库 `SKILL.md` **0 命中**；`资源池` 2 命中经查属 `engineering/wb-release-maintain`（发布资源清单）与 `meta/personal-ai-os`（OS 资源目录），均异命题；`choreography` / `token bucket` / `backpressure` 命中属 `engineering/ei-reliability`（重试预算与编排模式表）、`engineering/wb-subagent-delegation`（编排模式表）、豆包自留地 `engineering/wb-execute-discipline`（术语表）与 `defaults/wb-context-compressor`，**均异命题、豆包自留地 WB 0 落地**。与 `engineering/wb-subagent-delegation` r745B（trigger rules / catchup）分工：那条管「哪些上游状态允许下游跑」，本节管「有多少槽、排队时谁先跑」，互补不重述。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。

## 十二、扇出负载超过消费能力：背压是需求信号，不是限速（r765A · OI 编排）

> 上一节（§11）管「有多少并发槽、排队谁先跑」；本节管「当入队速率持续超过出队速率、槽与队列都要满时，压力怎么传到源头」。两者同一资源治理链的不同环：§11 是静态预算，本节是动态过载。判非：`backpressure` / `demand signal` / `request(n)` / `Little's law` / `load shedding` 在本技能既有正文 0 专节（§11 判非串提及为异命题），全库命中属异命题或豆包自留地，WB 0 落地。

**独点 1 — 背压的本质是消费者声明需求，不是生产者自我限速（reactive pull）**。Reactive Streams 官方 `Subscription` 逐字：`No events will be sent by a Publisher until demand is signaled via this method`；`Whatever has been requested can be sent by the Publisher so only signal demand for what can be safely handled`；累计需求达 `Long.MAX_VALUE` 可被当作 `effectively unbounded`。判据：① 需求信号由下游向上游传（`request(n)` 授权发 n 个），发多少由消费端的处理能力决定，不是生产者按固定速率推；② 「只请求你能安全处理的量」是硬约束——把需求声明成无界等于主动放弃背压；③ 与 throttling/rate-limit 区分：后者是生产者无论消费者闲忙都自我封顶（见 `ei-reliability` 的限流），背压是消费者驱动的按需拉取。落到编排：fan-out 的子任务领取应按「空闲 worker 数」拉取（`prefetch` 上限），不是领导者一次性把全部子任务注入队列。

**独点 2 — 无界队列把速率失配变成 OOM，有界队列才把它变成信号**。多域一致：生产 10000/s、消费 8000/s， backlog 每秒 +2000、一小时 720 万；有界缓冲把「内存无限涨」变成「满了必须 block/drop/shed」。缓冲定容用 Little's law：`in-flight = 到达率 × 系统内停留时间`；若 2000 req/s 下最多容忍 500ms 排队，队列应≤约 1000 项，再大只是没人等的延迟。四策略按数据类型选：block/pull（每条都不能丢，如文件/ETL）· drop old/new（遥测/实时帧/位置，陈旧即无价值）· sample/aggregate（极端量级日志）· reject early（用户请求，边缘 429/503 + `Retry-After`，快失败优于慢超时）。事件循环内 **不能** 用阻塞 put 做背压（会死锁整个 loop），必须靠有界 channel + 显式 reject/drop 或异步拉取。

**独点 3 — 压力必须传到真正源头，且背压只管瞬时过载、不管容量不足**。逐层背压：任何一层「吸收压力却不再向上游传」就变成下一个无界缓冲；gRPC/HTTP2 用 `WINDOW_UPDATE` 接收窗口把流控跨网络传（gRPC 官方：`the gRPC framework will wait before returning from a write call`，并警告同步读写双方都大量写不读会 **deadlock**）。与熔断器分工：背压管**流速**，熔断器（见 `ei-reliability` §15）判定服务已失败后**切断全部流量**， Resilience 管线两者都要。联邦/跨组织边界（外部 webhook 进入）不是流控而是 rate-limit 合约。边界声明：持续需求高于产能是**容量规划问题**，背压/卸载只是桥接不是解药；削掉的压力若源头不配合重试退避（jitter + 重试预算）只是把踩踏搬个位置。

**落地形态**：8 岗路由 fan-out 与并发委派时，工作队列一律有界 + 空闲 worker 按 `prefetch` 拉取；满队列按「数据能否 replay/是否实时」选 drop/reject，禁止无界 `LinkedBlockingQueue` 或 `Promise.all(unbounded[])`；验收报出每段的队列上限（按 Little's law 定）、满时策略、监控项（队列深度 + 最旧项 age，不盯 CPU）、以及压力能否回传到源。

**来源（r765A 独立实拉 2026-11-19，≥2 独立域一手交叉）**：
- `https://www.reactive-streams.org/reactive-streams-1.0.4-javadoc/org/reactivestreams/Subscription.html`（Reactive Streams 1.0.4 规范官方；WebFetch 200 逐字：`No events will be sent ... until demand is signaled via this method` / `only signal demand for what can be safely handled` / `effectively unbounded`）——第一独立域·规范一手。
- `https://grpc.io/docs/guides/flow-control/`（gRPC 官方 Flow Control，last modified 2023-10-05；WebFetch 200 逐字：`wait before returning from a write call` / `the receiver has more capacity` / 同步读写双方 deadlock warning）——第二独立域·框架官方。
- 交叉快照：`stackpractices.com/patterns/back-pressure-pattern`（bounded buffer / request(n) / Kafka max.poll.records+pause / 缓冲区按 p99 定容）、`designrounds.in/learn/backpressure`（10000 vs 8000 算例 / Little's law 1000 项 / Netflix-Envoy adaptive concurrency）、`inferensys.com/.../backpressure-handling`（DROP_OLDEST vs DROP_LATEST / edge load shedding）——第三域群，快照非一手不冒充。
- **失败与降级如实登记**：官方规范页只取 demand 语义，未取完整 TCK 规则全文；背压数值算例（720 万/1000 项）来自二手教学域，只取定性量级与 Little's law 公式，不作为生产定值。
- **判非**：`backpressure` / `request(n)` / `Little's law` / `load shedding` 在本技能正文 0 专节；全库命中均属异命题或豆包自留地（`wb-execute-discipline` 术语表 / `wb-context-compressor`），**豆包自留地 WB 0 落地**。与 §11（静态并发预算）互补不重述；与 `ei-reliability` 限流（生产者侧封顶）按「谁驱动速率」分工。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。
- **未采纳**：Reactive Streams TCK 完整规则集、Project Reactor/Akka 具体 API 代码、Kafka `pause()/resume()` 逐行实现、Envoy adaptive concurrency 算法参数（只取可落编排纪律的判据）。

## §13 r777A · 编排即协调控制循环（reconcile loop）：level-triggered 而非 edge-triggered

> 实拉来源见本节末。适用于本体系 fan-out/多 agent 编排、GitOps 式收敛、任何「声明期望→驱动现状逼近」的自动化。

- **★编排的正确心智模型是「非终止的控制循环」，不是「执行一串动作」**：官方原文「a *control loop* is a non-terminating loop that regulates the state of a system」，controller「watch the state of your cluster, then make or request changes where needed… tries to move the current cluster state closer to the desired state」。对象用 `spec` 表期望、`status` 报现状。⇒ 编排纪律固定三动作 observe→diff→act，且没有「完成退出」——只要控制体还在运行就持续纠偏；把一次性脚本当编排会丢掉自愈。官方「your cluster never reaches a stable state… as long as the controllers are running and able to make useful changes, it doesn't matter if the overall state is stable」⇒ 验收看「是否在收敛」而非「是否静止」。
- **★level-triggered：按当前状态决策，不按触发事件决策，这是丢事件/重启不丢正确性的根因**：level 派「reacts to the current state」，丢一个事件下次 observe 会重新看到、自动补齐；edge 派「reacts to event」丢事件即永久失步、须重放事件日志。watch 事件只是「something changed, look again」的提示、不是「做什么」的指令——reconciler 不消费 event payload，先 `client.Get()` 读最新状态再从那里算。⇒ fan-out 编排禁止把「处理进度/是否已处理」存成内存 flag（内存态重启即丢、且资源被重投时对错乱），须把进度落成可观测的 status 子资源（observedGeneration/conditions/lastTransitionTime）；把 edge 逻辑塞进 level 控制器是最常见引入的错误。
- **★一次 reconcile 只处理一个 key 且必须幂等 + 可乱序/迟到/读旧缓存**：controller-runtime 的 `Request` 只带 namespace/name 键，`workqueue` 对同对象多次更新去重、worker 一次取一个 key；幂等=「create if missing / update if different / do nothing if converged」，跑两次=跑一次。返回 `Result{}` 成功忘掉 key、`Requeue:true` 立即再排（受 rate limiter）、`RequeueAfter:30s` 定时轮询外部系统（绕过 rate limiter）、`err` 指数退避重排（默认 base 5ms/翻倍/cap 1000s，全局 10/s burst 100）。⇒ 常见新手 bug 是「返回 err 当重试」而非 `RequeueAfter`；外部云 API 副作用本身也必须幂等，否则控制循环正确但副作用重复。乐观并发（resourceVersion / 409 Conflict 后 reread+retry）解决多 controller 竞争同一对象。
- **★收敛失败与「reconcile 不解决什么」要写进声明**：convergent = 反复 reconcile 最终逼近期望，与起始状态无关。不收敛三类=期望不可达（replicas:100 但 20 节点每 Pod 16 CPU）、期望自相矛盾（replicas:5 + PDB minAvailable:10）、世界非幂等（动作改变期望本身）。reconcile 不保证：stateful 一致性（只能保 5 个 Pod 在跑、不保其 DB 状态一致）、应用级不变量（web 不得先于 DB 迁移启动）、跨集群一致性（单集群是边界）、时限保证（eventually consistent，无「T+5s 必到位」）。⇒ 规格把这些交给 init container/readiness probe/admission policy/GitOps 外部系统，别指望 reconcile 兜住；排障先读 controller events 与 status.conditions（「controller has logged what it is waiting for」），不要直接改运行态对象——reconciler 会把它改回 spec（「kubectl edit 在运行对象是临时的，这是设计不是 bug」）。
- **判非/去重**：`reconcile` / `level-triggered` / `edge-triggered` / `控制循环` / `期望状态` / `observedGeneration` 在本技能与 wb-subagent-delegation 正文 0 专节；与 §12 背压（消费者驱动速率）、§11 静态并发预算、wb-subagent-delegation 的 Airflow 重试/僵尸/Asset 事件均为异命题（那些管失败恢复与调度语义，本节管「声明期望→持续纠偏」的控制模型）。与 `wb-debug-loop` 期望状态断言为互补（那条是个别动作后的 verify，本节是全局收敛模型）。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除；**豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地**。
- **来源与诚信**：① `https://kubernetes.io/docs/concepts/architecture/controller/` — Kubernetes 官方一手 WebFetch 200 全文逐字（control loop 定义 / spec 期望 status 现状 / Job 控制器经 API server 间接控制 / direct control / desired vs current「never reaches a stable state」/ 简单多控制器 / 多个 controller 用 label 区分对象；Last modified 2024-09-01）——**第一独立域·官方一手**；② `https://www.kbytechnologies.com/lexicon/level-triggered-reconciliation` — 一手全文逐字（level vs edge 定义 / 丢事件与重复 create 的后果 / read-your-writes 与 resourceVersion / resync 抖动 10%/thundering herd / 把 edge 逻辑塞进 level 控制器的失败模式）——**第二独立域**；③ `https://runbook.academy/courses/kubernetes/lessons/kubernetes-i-06-desired-state-and-reconciliation` + `https://devopsbeast.com/courses/k8s-architecture-chaos/architecture-mental-model/reconciliation-loops` + `https://k8s-notes.home.liskl.com/controllers` + `http://www.golinuxcloud.com/kubernetes-reconcile-loop-explained` — 四独立一手交叉（收敛失败三类 / informer+workqueue+rate limiter 管线 / RequeueAfter 四返回值与默认参数 / status 规则 observedGeneration+conditions / 409 Conflict 重读重试）。数值参数（5ms/1000s/10-per-sec/10% 抖动）挂 controller-runtime 与第三方口径，不写成普适常量；官方 controller 页未逐字给 level-triggered 术语，该术语取 kbytechnologies/devopsbeast 一手并如实登记。
- 提升层：工作流 / 编排。触发词：reconcile loop、协调控制循环、level-triggered、edge-triggered、期望状态 vs 现状、spec/status、observedGeneration、幂等收敛、RequeueAfter、丢事件自愈、informer+workqueue、read-your-writes、GitOps 收敛、编排不是执行一串动作。

## §14 r781A · 编排器多实例的主节点选举：Lease + 乐观并发，而非抢内存锁

> 实拉来源见本节末。适用于本体系 8 岗编排器被多副本部署、任何「同一时刻只允许一个 active 编排者执行写动作」的场景。与 §13 reconcile 分工：那节管「声明期望→持续纠偏」的控制模型，本节管「多个同构副本里谁有资格当那个纠偏者」。

- **★选主的真相在共享租约 + 乐观并发，不是本地布尔标志**：Kubernetes 官方 Lease 页逐字「leases ... provide a mechanism to lock shared resources and coordinate activity between members of a set」，Lease 是 `coordination.k8s.io` API 组的轻量对象，承载 `holderIdentity`（当前 leader 身份）、`acquireTime`、`renewTime`、`leaseDurationSeconds`、`leaseTransitions`（易主次数）。协调选主页逐字「When the Lease does not exist or has expired (current time > `renewTime` + `leaseDurationSeconds`), candidate instances attempt to update the Lease with their identity. Kubernetes relies on **optimistic concurrency control** via the object's `resourceVersion`: **only one update succeeds due to version mismatch on concurrent attempts**. The instance whose update is accepted becomes the *leader*」。⇒ 编排纪律：多副本部署的 leader 判定必须落在**共享、可比对版本号的租约对象**上，禁止用「进程内存里的 `is_leader=True`」或「谁先启动谁当主」——后者在并发/重启时必然双主。租约字段固定四栏=holderIdentity / renewTime / leaseDurationSeconds / transitions，再加 resourceVersion 做 CAS。
- **★续约周期与过期判定是两条独立参数，且 leader 要按半租期主动续**：官方逐字「the leader periodically renews its Lease by updating the `renewTime` field (for example, performing renewal every `leaseDurationSeconds` ÷ 2, in order to avoid conflicts when the Lease is about to expire)」；「If the current leader fails to renew the Lease within the selected timeout period, the remaining candidates compete to acquire leadership」；候选者「should wait this long plus a small grace period before attempting to acquire an expired lease」。⇒ 规格写清三个量=租约有效期 / 续约周期（约半租期）/ 过期后 grace，验收断言「leader 停更后，新主在 有效期+grace 内产生」；续约周期内不得反复抢锁（制造抖动），过期后不得无人接管（availability 空洞）。与 r757B/ei-reliability 的 fencing token 互补：租约选主解决「谁当主」，fencing 解决「旧主没意识到自己已不是主时仍写资源」——两者须叠加，选主不是互斥的完整解。
- **★版本 skew 场景要确定性选主，不能让「随便一个活着的副本」上台**：Kubernetes v1.37 `CoordinatedLeaderElection`（Beta，默认关，需 `CoordinatedLeaderElection` feature gate + `coordination.k8s.io/v1beta1`）官方逐字「allows control plane components to **deterministically select a leader** ... useful to satisfy Kubernetes version skew constraints during cluster upgrades」；唯一内置策略 `OldestEmulationVersion`「preferring the leader with the lowest emulation version, followed by binary version, followed by creation timestamp」；候选通过 `LeaseCandidate` 登记 identity / binary version / emulation version。⇒ 编排纪律：滚动升级期间若「任意存活副本都能当主」，新版本副本上台可能与旧版本状态/协议不兼容；选主规则须可声明「优先谁」，并把版本/创建时间作为 tie-break。注意该特性默认关闭且绑 v1.33+，引用须带版本号不写成普适默认。
- **★主动释放锁可缩短切换延迟，但属 alpha 且默认关；实例身份靠名称防碰撞**：Lease 页 `ControllerManagerReleaseLeaderElectionLockOnExit`（v1.36 Alpha，默认关）逐字「actively releases its leader election lock during leader transitions, rather than waiting for the lock's TTL to expire. This allows a new leader to be elected more quickly, reducing leader transition latency」。API server identity（v1.26 Beta，默认开）用 Lease 发布身份，「if you do use a Lease, it's a good practice to define a name for the Lease that is obviously linked to the product or component」；「select a name prefix and pick a mechanism (such as hash of the name of the Deployment) to avoid name collisions for the Leases」。⇒ 交接延迟分两档=等 TTL 过期（长）vs 主动释放（短，需 feature gate）；编排器上线须先规划 Lease 命名（绑产品名 + Deployment 名 hash 前缀）避免多套系统互相踩租约。API server identity 的「同名新实例接管既有 Lease 而非新建」说明身份应由稳定标识推导而非随机生成。
- **判非/去重**：`leader election` / `Lease` / `holderIdentity` / `选主` 在本技能与 wb-subagent-delegation 正文 0 专节；wb-debug-loop §r631C「选主后定时器不重挂」为 HA 切换后的**等待态 re-arm** 异命题（那条管切主之后，本条管怎么选出主），ci-context「按 workflow 类型选主指标」与 distill-cat「主要矛盾」均为子串误命中。与 §11 静态并发预算、§12 背压、§13 reconcile 正交（那些管资源/流速/纠偏，本节管副本间的 leader 资格）。**豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地**。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。
- **来源与诚信**：① `https://kubernetes.io/docs/concepts/architecture/leases/` — Kubernetes 官方一手 WebFetch 200 全文逐字（Lease 定义 / holderIdentity+acquireTime+renewTime+leaseDurationSeconds+leaseTransitions / node heartbeat / leader election / lock release on exit v1.36 alpha / API server identity v1.26 beta / Lease 命名防碰撞；Last modified 2026-03-31）——**第一独立域·官方一手**；② `https://kubernetes.io/docs/concepts/cluster-administration/coordinated-leader-election/` — Kubernetes 官方一手 WebFetch 200 全文逐字（resourceVersion 乐观并发 only-one-update-succeeds / 过期判定式 / 半租期续约 / LeaseCandidate / OldestEmulationVersion 确定性选主 / feature gate 与 v1beta1 前置；Last modified 2026-08-05）——**第二独立页·官方一手**。两页同域名但主题互补（Lease 原语 vs 协调选主策略），如实登记为「同官方两页」而非两独立厂商；续约「÷2」与 grace 为官方示例口径，不写成跨系统常量。
- 提升层：编排 / 多副本一致性。触发词：leader election、主节点选举、Lease、holderIdentity、renewTime、leaseDurationSeconds、leaseTransitions、resourceVersion 乐观并发、only one update succeeds、半租期续约、过期 grace、fencing token 互补、CoordinatedLeaderElection、OldestEmulationVersion、LeaseCandidate、版本 skew 选主、主动释放锁、leader transition latency、Lease 命名防碰撞。

## 十六、Actor 模型编排：无共享状态 + 每 actor 串行信箱（r789A｜2026-11-22 实拉）

> 与 §十一静态并发预算（发多少）、§十二背压（流速）、§十三 reconcile（纠偏）、§十四选主（谁当主）、§十五删除（怎么删）正交：那些管「资源/流速/资格/删除」，本节管「并发计算单元本身怎么建模」。来源：Autonomy 官方 actors 页 + UIUC Agha 团队 Actors 综述双一手 WebFetch/WebSearch 逐字。

- **★四要素=地址+信箱+私有状态+行为；单 actor 一次只处理一条消息，故状态天然安全无需加锁**：官方逐字「Actors are lightweight, stateful objects that communicate using messages. Each actor has: A unique address ... A mailbox where incoming messages queue up and wait to be processed. Internal state that only this actor can access or modify. Behavior, logic that defines how this actor reacts to each message it receives」；「Each individual actor processes only one message at a time. Messages wait in the actor's mailbox and are handled sequentially. This means you never need to worry about two threads modifying an actor's state simultaneously; it simply can't happen」；「No shared state ... This eliminates entire classes of concurrency bugs like race conditions and deadlocks. Actors can only influence each other by sending messages」。UIUC 综述补四语义属性：state encapsulation / atomic execution of a method in response to a message / fairness in scheduling and delivery / location transparency。⇒ 编排纪律：员工/agent 建成有状态 actor，状态私有、跨员工只靠消息；并行发生在 actor 之间而非内部，与 §十一给单员工加并发预算是两层——给一个 actor 加线程反而破坏其串行安全假设。

- **★异步发送+位置透明+空闲不耗 CPU，是多常驻员工调度的关键**：官方逐字「When Actor A sends a message to Actor B, it doesn't have to wait for B to process it or respond ... A can continue with its work immediately. This non-blocking communication allows actors to work concurrently without waiting on each other」；「Sending or receiving a message from another actor looks the same whether that other actor is running on the same machine or across the network. This makes it natural to distribute work and scale horizontally」；「When an actor is idle and there are no messages in its mailbox, it consumes no CPU ... the actor runtime automatically gives the CPU core to a different actor that has a new message to process」。⇒ 落地：员工 A 委派员工 B 不等回执即可继续；本地/远程同一发送接口，横向扩容不改编排代码；LLM/工具等待期让出 CPU 给别的 actor，故可常驻数千有状态员工不空转。与 r738A「编排代码确定性可重放、副作用进 Activity」叠加：确定性约束落在行为函数，等待/调度交给 actor runtime。

- **★消息无到达顺序保证，要 FIFO 得显式建队列 actor；locality 限定只能给「已知/消息带来/自己创建」的地址发**：UIUC 综述逐字「the path a message takes, as well as network delays it may encounter, are not specified. Thus the arrival order of messages is indeterminate」；维基 Actor model 逐字「Hewitt argued against adding the requirement that messages must arrive in the order in which they are sent ... If output message ordering is desired, then it can be modeled by a queue actor」；locality「an actor can send messages only to addresses that it receives in the message, addresses that it already had before it received the message, and addresses for actors that it creates while processing the message」，resumption/continuation 地址随消息传递以构造「arbitrarily variable topological relationships」。⇒ 规格须写明：① 需要有序处理的员工链显式经队列 actor，不假设 mailbox 保序；② 回信目标作为地址随消息传（resumption 模式），不靠全局共享回调表；③ actor 名全局唯一不可猜、可经消息传递获知——capability 式寻址，别用可枚举序号当地址（与 SI 模块 BOLA「不可预测 ID」同向、异命题不混写）。

- **判非/去重**：`Actor 模型` / `mailbox` / `无共享状态` / `位置透明` / `有状态 worker` 全库 SKILL.md 正文 0 命中；`worker` 在 §五步协议为「AI 员工」业务称谓、r761A 为 Airflow map 实例，均异命题子串。与 r738A Temporal（确定性重放/幂等键）、r785A finalizer（怎么删）正交，本节取「并发单元建模」新轴。**豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地**。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。

- **来源与诚信**：① `https://autonomy.computer/docs/applications/actors` — Autonomy 官方一手 WebFetch 200 全文逐字（四要素 / no shared state 消除 race&deadlock / 串行信箱 / 异步非阻塞 / location transparency / 空闲零 CPU / stateful worker 案例）——**第一独立域·官方一手**；② `https://osl.cs.illinois.edu/media/papers/karmani-2011-actors.pdf` — UIUC Open Systems Laboratory 综述 Karmani & Agha《Actors》WebSearch 全文逐字（定义 / 四语义属性 / 到达顺序不定 / locality / resumption / queue actor）——**第二独立域·学术论文一手**；③ Wikiwand/Wikipedia 演员模型条目 WebSearch 逐字交叉（1973 Hewitt 提出 / 地址即 mail address / 私有状态间接互影响避免基于锁同步）。位置透明与「零 CPU」为 Autonomy 运行时实现口径，不写成所有 actor 框架的普适保证。

## 十五、finalizer 两阶段删除编排（r785A｜2026-11-20 实拉）

> 与 §十三 reconcile（纠偏循环）、§十四 leader 选主（谁当主）正交：那两节管「怎么建/怎么纠/谁来管」，本节管「怎么删」——删除是**两阶段协议**不是一个 delete 信号。来源：Kubernetes 官方 finalizers 页 + API concepts「资源删除」页双一手 WebFetch 200 全文逐字。

- **★删除是两阶段：先打标（deletionTimestamp）再清空 finalizers，最后才真删**：官方逐字「When you tell Kubernetes to delete an object that has finalizers specified for it, the Kubernetes API marks the object for deletion by populating `.metadata.deletionTimestamp`, and returns a `202` status code (HTTP "Accepted"). The target object remains in a terminating state while the control plane, or other components, take the actions defined by the finalizers. After these actions are complete, the controller removes the relevant finalizers... When the `metadata.finalizers` field is empty, Kubernetes considers the deletion complete and deletes the object」。中文官方「当你 delete 资源时，操作将分两个阶段进行：1. 终结（finalization） 2. 移除」「当最后一个终结器也被移除时，资源才真正从 etcd 中移除」。**finalizer 只是键列表不是代码**（「Finalizers don't usually specify the code to execute. Instead, they are typically lists of keys on a specific resource similar to annotations」），控制器看到 deletionTimestamp 后执行清理、逐条满足条件就摘除该键。⇒ 编排纪律：凡编排器曾创建外部资源（云资源/租约/订阅/影子对象），删除主对象前必须先登记 finalizer 挂清理钩子，否则留下孤儿；202 Accepted 只是「受理删除请求」不是「已删完」，验收断言 finalizers 是否清空、依赖对象是否已清理，不是断言 delete 调用返回成功。与 r743B outbox「写与发封装同入口」同向：删与清理也必须同一入口登记。

- **★删除期约束不可逆，故删除入口必须幂等可重入**：官方逐字「You can remove existing finalizers (deleting an entry from the `finalizers` list) but you cannot add a new finalizer. You also cannot modify the `deletionTimestamp` for an object once it is set」「After the deletion is requested, you can not resurrect this object. The only way is to delete it and make a new similar object」；自定义 finalizer 名「must be publicly qualified finalizer names, such as `example.com/finalizer-name`. ... the API server rejects writes」⇒ 三条硬约束写进删除规格：① 删除期只能减 finalizer 不能加；② deletionTimestamp 一旦设不可改（重启/重试后从该时间戳续做清理，不是重发 delete 期待加速）；③ 对象不可复活，误删只能重建相似对象（故 finalizer 的清理动作须幂等且对同一对象可重入）。finalizer 名绑域名限定，避免自造裸名被 API 拒写。与 r738A「重试是战术恢复是策略、外部历史判资格」呼应：deletionTimestamp 就是那外部历史。

- **★finalizers 之间无强制顺序（共享字段可被任意重排），顺序化会死锁；卡住时禁止手工摘**：中文官方逐字「一旦设置了 `.metadata.deletionTimestamp`，作用于终结器的外部控制器可以在任何时间以任何顺序开始执行它们的清理工作。终结器之间**不存在**强制的执行顺序，因为这会带来卡住 `.metadata.finalizers` 的重大风险。`.metadata.finalizers` 字段是共享的：任何有权限的参与者都可以重新排序。如果终结器列表是按顺序处理的，那么这可能会导致这样一种情况：在列表中负责第一个终结器的组件正在等待列表中稍后负责终结器的组件产生的某些信号（字段值、外部系统或其他），从而导致死锁」。官方 finalizers 页警告「In cases where objects are stuck in a deleting state, avoid manually removing finalizers to allow deletion to continue. Finalizers are usually added to resources for a reason, so forcefully removing them can lead to issues in your cluster. This should only be done when the purpose of the finalizer is understood and is accomplished in another way (for example, manually cleaning up some dependent object)」。owner reference 段：删 Job 时 Kubernetes 用 owner references（不是 labels）判定哪些 Pod 需清理，且「finalizers can block the deletion of dependent objects, which can cause the targeted owner object to remain for longer than expected」⇒ 纪律：每个清理钩子写成**可乱序、幂等、无相互信号依赖**的独立动作，不按列表位置编排；卡住先查 owner 与依赖对象两侧的 finalizers 找真因，不靠强摘掩盖。强制删除（`ignoreStoreReadErrorWithClusterBreakingPotential`，Beta since v1.37 默认启用但底层需 Alpha feature gate `--feature-gates=AllowUnsafeMalformedObjectDeletion=true` + `unsafe-delete-ignore-read-errors` 权限）「会忽略终结器（Finalizer）约束，并跳过前置条件检查」，仅用于损坏对象不可读取，不当常规逃生阀——引用绑版本，不写成普适默认。

- **判非/去重**：`finalizer` / `deletionTimestamp` / `两阶段删除` / `owner reference 清理` 全库 SKILL.md 正文 0 专节；`强制删除` 在 ci-context 命中为 pod-lifecycle 优雅终止（§18 SIGTERM 排空，异命题——那条管「怎么优雅停服务」，本条管「删对象前怎么保证资源清干净」）。与 §13 reconcile「期望态收敛」互补：reconcile 的期望态通常不是「不存在」，删除是它的特殊终点态，需独立协议。**豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地**。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。

- **来源与诚信**：① `https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/` — Kubernetes 官方一手 WebFetch 200 全文逐字（两阶段删除 / 202 / deletionTimestamp / 不可加新 finalizer / 不可改 timestamp / 不可复活 / qualified name / pv-protection / owner references 判定 / 卡住禁手工摘 / 强制删除警告）——**第一独立页·官方一手**；② `https://kubernetes.io/zh-cn/docs/reference/using-api/api-concepts/` — Kubernetes 官方中文一手 WebFetch 200 全文逐字（「资源删除」两阶段 / 无强制顺序 / 共享字段可重排 / 顺序化死锁 / 最后一摘才从 etcd 删 / 强制删除 Beta v1.37 与 Alpha feature gate 与权限）——**第二独立页·官方一手**。两页同域名主题互补（对象语义 vs API 删除协议），如实登记为「同官方两页」而非两独立厂商；「÷2 半租期」类示例口径与具体 feature gate 状态绑版本，不写成跨系统常量。


## 十七、工作流确定性重放编排（r793A｜2026-11-22 实拉）

> 与 §十三 reconcile（纠偏收敛）、§十四 leader 选主（谁当主）、§十五 finalizer（怎么删）正交：那三节管「状态如何收敛/谁来管/怎么删」，本节管「多步骤员工工作流在崩溃后靠重放续跑时，代码凭什么保证每次重放走出同一序列」。来源：Temporal 官方 Workflow Definition / Python SDK sandbox / safe-deployments 多页 WebFetch 200 全文逐字。

- **★确定性 = 同一输入必须产生同一序列的 Workflow API 调用，非确定操作一律下沉到 Activity**：官方逐字「A critical aspect of developing Workflow Definitions is ensuring that they are deterministic. Generally speaking, this means you must take care to ensure that any time your Workflow code is executed it makes the same Workflow API calls in the same sequence, given the same input」；非确定来源逐字「To handle non-deterministic operations like API calls, LLM/AI invocations, database queries, and other external interactions, put them in Activities. Activities execute outside the replay path and are automatically retried so they don't cause non-determinism errors」。判据：员工工作流里凡是调 LLM、查库、发消息、取当前时间、取随机数——全部沉到 Activity（沙箱外的可重试单元），编排层只保留确定性步骤；把 LLM 调用写进编排主干 = 重放时可能产生不同 Command 序列甚至重复副作用。与 r738A Temporal「幂等键/重试是战术恢复是策略」互补：那条管失败后怎么恢复，本条管恢复重放凭什么不走样。

- **★重放是「重发 Command 比对 Event History」，不是「重跑业务逻辑」**：官方逐字「use of certain Workflow APIs in the function is what generates Commands. Commands tell the Temporal Service which Events to create and add to the Workflow Execution's Event History. When the Workflow's code replays, the Commands that are emitted are compared with the existing Event History. If a corresponding Event already exists within the Event History that matches that command, then the Execution progresses」；例子逐字「using an SDK's Execute Activity API generates the ScheduleActivityTask Command ... that Command is compared with the Event that is in the same location within the sequence」，不匹配即「non-deterministic error」。⇒ 员工工作流的正确性单位是 Command 序列与历史事件逐位对齐，不是「函数体执行一遍结果对」；验收用 replay testing——拿历史事件喂当前代码逐条比对（官方「Replay testing takes one or more existing Event Histories that ran against a previous version of Workflow code and runs them against your current Workflow code, verifying that it is compatible」），而不是只在理想样例上跑通。

- **★会产生 Command 的 API 调用不可重排/新增/删除（除非走版本化）；不产生 Command 的调用才安全**：官方列出产生 Command 的调用包括「Starting or cancelling a Timer / Scheduling or cancelling Activity Executions (including local Activities) / Starting or cancelling Child Workflow executions / Signalling or cancelling signals to external Workflow Executions / Scheduling or cancelling Nexus operations / Ending the Workflow Execution in any way / Upserting Workflow Search Attributes / Upserting Workflow Memos / Running a SideEffect or MutableSideEffect」，这些「must not be reordered, added, or removed without proper Versioning techniques」；可安全改动的是「input parameters, return values, and execution timeouts of Child Workflows and Activities（但改 types 或 IDs 不安全）」「duration of Timers（部分 SDK 改成 0 不安全）」「add/remove 不产生 Command 的 API 如 GetInfo」。判据：改员工编排步骤顺序 = 高风险必须版本化；只改 Activity 入参/超时 = 低风险可灰度；记不住这张清单就一律当高风险。

- **★沙箱只是「帮助发现」非「完全隔离」，版本演进靠 pin 或 patch 而非直接改在跑的工作流**：Python SDK 官方逐字「The Temporal Python SDK sandbox ... help prevent non-determinism errors ... is not completely isolated, and some libraries can internally mutate state, which can result in breaking determinism」；非确定的库调用被代理对象拦截，全局状态用 exec 隔离、依赖默认从沙箱外 pass through（只应 pass「已知无副作用」模块）。版本化两法逐字「Worker Versioning: keep Workers tied to specific code revisions, so that old Workers can run old code paths and new Workers can run new code paths」与「Versioning with patching: make sure your code changes are compatible across versions」；patch 三步「Use Patched to patch in new code and run it alongside the old code / Remove the old code and apply DeprecatePatch / Once all old Workflows have left retention, remove DeprecatePatch」。⇒ 长生命周期员工工作流改步骤时：① 新执行用新版本、在跑的继续旧版本（pin 或 patch），不直接覆写；② 沙箱检测到非确定即让该 Task 失败、修好代码才继续（官方「The Workflow will not progress until the code is fixed」）——把「fail closed 等修复」写进规格，不让非确定步骤静默带病重放。与 SI 模块「沙箱不是安全边界」同向、异命题（那条管安全隔离，本条管确定性）。

- **判非/去重**：`工作流确定性` / `非确定性错误` / `Event History` / `Command 比对` / `Worker Versioning` / `SideEffect` 在 OI 本体 SKILL.md 0 专节；`replay` 命中全在豆包自留地 `wb-context-compressor`（重放 payload 做 staging 验证、崩溃恢复双保证，异命题——那条测输入重放，本条是编排代码重放保证 Command 序列一致）与 `wb-max-token-saver`（O(n²) 历史重放，异命题）。与 r738A Temporal 同技术但不同轴：r738A 取幂等键/恢复策略，本条取确定性约束与版本化，互补不并存新层。豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。

- **来源与诚信**：① `https://docs.temporal.io/workflow-definition` — Temporal 官方一手 WebFetch 200 全文逐字（deterministic constraints / 可安全与不安全改动清单 / 产生 Command 的 API 全集 / Command 与 Event History 逐位比对 / non-deterministic error 两成因 / 内联随机分支反例 / 两版本化策略 / patch 三步 / Worker 故障不由工作流处理）——第一独立页·官方一手；② `https://docs.temporal.io/develop/python/python-sdk-sandbox` — Temporal 官方 Python SDK sandbox 页 WebFetch 200 全文逐字（沙箱两组件 global state isolation + restrictions / 非完全隔离 / passthrough 只放已知无副作用模块 / skip sandboxing 三法 / 非确定即 fail task 直到修代码）——第二独立页·官方一手（不同文档）；③ `https://docs.temporal.io/develop/safe-deployments` 与 `https://docs.temporal.io/develop/typescript/workflows/basics` WebSearch 逐字交叉（replay testing 用历史喂当前代码校验 / Date.now 与 Math.random 替换为确定性版 / WeakRef 移除因 GC 不确定）。同厂商多页，如实登记为「同官方三页主题互补」而非多厂商交叉；Timer 改 0/-1 的不安全口径绑 SDK，不写成跨系统常量。
## DAG 调度：拓扑序只定依赖方向，就绪队列才定执行顺序（r795I 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）

§r785A 并发四层与 weight_rule 管「资源槽怎么分」，本章补**调度器内核**：入度计数、环检测、失败传播，以及「topo_order[i] 不等于第 i 个执行」这一常见误读。

**独点1** 入度/环判据：维护 `indeg[v]` 与 `S={v | indeg[v]==0}`，每消费边 `u→v` 执行 `indeg[v]--`，仅降为 0 才入队；结束断言 `len(order)<|V|` → 报环。复杂度 O(|V|+|E|)。UPenn 讲义逐字：保留「count of the arrows still pointing into it」，剩点无 0 入度则必有环。

**独点2** 顺序≠执行判据：拓扑序只保证每条边前向，同层多源可任选（讲义原文无边时 n! 个拓扑序），因此 `topo_order[i]` 不等于第 i 个被执行的任务；真实执行由就绪队列 + worker / Pool 槽位决定，入队 ≠ 立即执行。

**独点3** 失败传播判据：Airflow 默认 `all_success` 下上游 failed 或 skipped 会级联跳过下游；汇合节点须显式 `none_failed_min_one_success` 才是「任一支成功即继续」。重跑边界须限定在失败节点及其下游依赖闭包，不触碰闭包外已成功节点（此条为工程推断，官方页只直接支持 trigger rule 与 depends_on_past）。

- **判重：`拓扑排序`/依赖调度正文在本体 0 专节；`DAG`/`拓扑` 命中是 Airflow 资源配额与 actor model 语境，异命题；与 §r785A 并发四层、§r793A Temporal 确定性分工不复用。豆包自留地 WB 0 落地。**
- **来源与诚信**：https://www.engineering.upenn.edu/~cit5920/knowledge/objects/graphs-and-trees/dags-and-topological-order（UPenn CIT 5920 讲义，WebFetch 200 逐字：indegree 计数 / 环判定 / n! 个拓扑序 / O(|V|+|E|)）；https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html（Apache Airflow 3.4.0 官方，WebFetch 200 逐字：all_success 默认 / skip 级联 / none_failed_min_one_success / depends_on_past）；https://airflow.apache.org/docs/apache-airflow/2.1.0/concepts/overview.html（Apache Airflow 官方，WebFetch 200 逐字：task queue / 发给 worker 不保证同机 / Pools 限并发）。无。 逐字全文与判非见 `references/r795I_DAG拓扑调度.md`。
## 汇合同步 barrier：Cyclic 可复用、Latch 一次性，坏一个全坏（r796I 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）

§r795I 管 DAG 的入度计数与环检测，本章管**汇合点本身**：等到齐才放行、失败如何传播、以及和 trigger rule 的对应边界。

**独点1** 放行条件不可互换：CyclicBarrier ⇔ `getParties()` 个参与方都调 `await()` 才放行且释放后可复用（cyclic）；CountDownLatch ⇔ `getCount()==0` 放行，one-shot「count cannot be reset」，且调用 countDown 的线程不必等归零。判据——需要可复用同步点却用 Latch、或反之，判错配（Oracle Java 21 官方 API 逐字）。

**独点2** 失败传播 all-or-none：任一参与方 interrupt / timeout / barrier action 抛异常 → 其余所有等待方抛 `BrokenBarrierException`，barrier 置 broken 态；超时版额外抛 `TimeoutException`。判据——汇合点未定义 broken 态与超时出口，判「参与方不足可永久挂死」（该风险由 await 语义推出，非独立论文逐字）。

**独点3** DAG join 映射：trigger rule 决定汇合——`all_success`（默认，全上游成功）/ `all_done`（不分成败）/ `one_success`（任一成功即放行）；barrier 语义对应前两者，不对应 `one_success`（Airflow 官方逐字）。判据——把 barrier 直接等同于任意 join 判错；分布式屏障的失败传播外推须标推断（Spark barrier 章节未取到一手）。

- **判重：`屏障`/`barrier` 本体命中为 actor mailbox/其他语境，同步屏障专节 0；与 §r795I DAG 调度、§r793A Temporal 确定性分工不复用。豆包自留地 WB 0 落地。**
- **来源与诚信**：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CyclicBarrier.html（Oracle Java SE 21 官方 API，WebFetch 200 逐字：全员 await 放行/可复用/BrokenBarrierException 与 broken 态）; https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CountDownLatch.html（Oracle Java SE 21 官方 API，WebFetch 200 逐字：one-shot count cannot be reset/await 阻塞至零/countDown 方不必等）; https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html（Apache Airflow 官方，WebFetch 200 逐字：all_success 默认/all_done/one_success）。Spark Barrier Execution Mode 两页未返回正文；all-or-none 外推分布式标推断。 逐字全文与判非见 `references/r796I_汇合同步.md`。

## r800B · CQRS 读写模型分离：编排「谁写谁读」而非把读写压进一个模型（OI · 2026-11-23 实拉，≥3 独立域一手交叉，3 独点）

**这一节管什么**：前面 §11 背压、§12 reconcile、§13 Lease 选主、§16 Actor、§17 重放、DAG/barrier 都在管「多副本/多步骤怎么协调」；CQRS 补的是**数据结构层的编排分工**——写侧与读侧用不同模型，让一致性边界、扩展与安全门禁各自独立，而非一个模型兼顾两职。与 §17「确定主干/非确定下沉」同构但不同层：那条分离确定性与副作用，本条分离**更新语义与查询语义**。

### 三独点
1. **拆的是「概念模型」而非一定拆库，先判读写形状是否真的不同再决定分不分**：Fowler 逐字「At its heart is the notion that you can use a different model to update information than the model you use to read information」+「having the same conceptual model for commands and queries leads to a more complex model that does neither well」；分三层逐字「The in-memory models may share the same database, in which case the database acts as the communication between the two models. However they may also use separate databases, effectively making the query-side's database into a real-time ReportingDatabase」+「it could be that the same objects have different interfaces for their command side and their query side… But usually when I hear of CQRS, they are clearly separate models」。ThirdBrain 引 Microsoft 分两级「Separate models, one data store（最低成本，代码更清晰）」与「Separate data stores（需同步，读变最终一致）」。**判据**：先问「读写模型形状/负载/安全需求是否显著不同」，否→保持 CRUD 或仅上 ReportingDatabase；是→最低成本档起步（同库分模型），只有读负载确需独立扩展才升到分库。与 §13 选主/§11 背压分工：那些管副本与流速，本条管**读写职责边界**。
2. **命令表达业务任务、查询只回 DTO；分库后最终一致须由事件 + 幂等消费补上**：ThirdBrain 逐字「Commands change state. They should express a business task ("Book hotel room"), not a low-level data edit ("Set ReservationStatus to Reserved"). The write side carries validation, business rules and consistency. Queries never change data. They return data transfer objects (DTOs) shaped for the screen or API, with no domain logic」+「Because a database and a message broker normally cannot share one transaction, Microsoft recommends the Transactional Outbox pattern (persist the state change and the event atomically) and idempotent read-model consumers that tolerate duplicate delivery」。microservices.io 逐字「The application keeps the database up to date by subscribing to Domain events published by the service that own the data」+ 代价「Increased complexity / Potential code duplication / Replication lag/eventually consistent views」。Fowler 逐字「Having separate models raises questions about how hard to keep those models consistent, which raises the likelihood of using eventual consistency」+「If the write model generates events for all updates, you can structure read models as EventPosters」。**判据**：写侧接口须是业务任务级命令、读侧禁止域逻辑；一旦分库必须同事务落状态变更与事件（outbox）+ 读模型消费幂等，验收断言重复投递不产生重复读模型、并显式声明读侧滞后窗口的用户可见性。
3. **CQRS 只用在特定 BoundedContext，是少数场景的复杂交换，不是全局架构**：Fowler 逐字「CQRS should only be used on specific portions of a system (a BoundedContext in DDD lingo) and not the system as a whole」+「CQRS is a significant mental leap for all concerned, so shouldn't be tackled unless the benefit is worth the jump」+「so far the majority of cases I've run into have not been so good, with CQRS seen as a significant force for getting a software system into serious difficulties」+「such suitability for CQRS is very much the minority case. Usually there's enough overlap between the command and query sides that sharing a model is easier」；两个正当收益逐字「a few complex domains may be easier to tackle」与「handling high performance applications… separate the load from reads and writes allowing you to scale each independently… big disparity between reads and writes」；替代逐字「if your domain isn't suited to CQRS, but you have demanding queries… you can still use a ReportingDatabase」。ThirdBrain 同列「O/RM scaffolding cannot generate CQRS code from a schema」「users can see stale data and may act on it」「Fowler's warning: for most systems CQRS adds risky complexity」。**判据**：采用前写出「本 BoundedContext 为何不满足共享模型」的具体证据（域复杂度或读写量级差），否则拒绝；只为查询压力大则降级到 ReportingDatabase；读侧滞后可能致用户基于旧数据行动，交互层须标注新鲜度或读己之写补偿。

### 来源与诚信
- `https://martinfowler.com/bliki/CQRS.html`（Martin Fowler bliki 2011-07-14，WebFetch 200 全文逐字：定义/同库vs分库/任务式UI与事件协作/eager read derivation/eventual consistency/bounded context 限定/CRUD 多数不适用/ReportingDatabase 替代/复杂性警告）——第一独立域·概念原始权威一手。
- `https://www.thirdbrain.tech/KB-SWE/METHODOLOGY/cqrs`（ThirdBrain 知识库，WebSearch 逐字：读写分离两级/Microsoft Transactional Outbox + 幂等消费者/命令表达业务任务/收益成本清单/Fowler 警告；页末列 Microsoft Azure Architecture Center 与 Fowler 来源 2026-10-09 读）——第二独立域·架构资料汇编交叉（转述官方，立场登记）。
- `https://microservices.io/patterns/data/cqrs.html`（microservices.io 官方模式页，WebSearch 逐字：view database 订阅领域事件更新/NoSQL 优化查询/多非规范化视图/复杂度与复制滞后代价）——第三独立域·模式库一手。
- **判非**：全库 SKILL.md / module-memory 对 `CQRS`/`command query responsibility segregation`/`bounded context` 专节 0；与 §17 工作流确定性、§16 Actor、DAG 分工不复用（那些管执行协调，本条管读写模型职责）。豆包自留地 WB 0 落地。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。



## r804B · 一致性哈希：扩容只动 K/N 个键，虚拟节点才让它真的均匀（OI · 2026-11-25 实拉，≥3 独立域一手交叉，3 独点）

### 三独点
- **mod-N 扩容是全量洗牌，哈希环才是局部编辑**：`hash(key)%N` 在 N 变时绝大多数键改址——加一台时保住原位的概率仅 1/(N+1)、迁移 N/(N+1)（N=4 迁 80%，N=96 迁 99%）；一致性哈希把键与节点一同映射到同一环形空间 [0,2^m−1]，键顺时针遇到第一个节点即归它；加节点只接管其与前驱间的弧、删节点其弧顺延给后继，平均只迁 K/N（K 键数、N 节点数），是再平衡的理论下限，避免缓存雪崩/数据库被瞬时打穿｜Karger 等 1997 STOC《Consistent Hashing and Random Trees》原始构造（经 Vetora/Padho 两域逐字引述）+ nginx 官方 `hash key [consistent]` 指令（不加 consistent「adding or removing a server ... may result in remapping most of the keys」；加了用 ketama「only a few keys will be remapped ... higher cache hit ratio」，ketama_points=160）。
- **虚拟节点不是优化项而是必需项**：裸环少量物理节点弧长极不均（N=10 时最重/最轻可达 4–5×），节点故障整段压到单一后继；给每物理节点多个环位置（vnodes，常见 100–256）后弧长方差从 O(1/N) 降到 O(1/(V·N))、偏斜 <1.05×，故障负载散到多个后继，还能用 vnodes 数量编码异构容量（大机器多给）；Dynamo(2007) 用 128–256，Cassandra 默认曾 256（新版本降到 16 因 repair 成本），Riak 64，nginx ketama=160——数字须绑版本/实现，不可写成普适默认｜nginx 官方 upstream 模块文档 WebFetch 200 全文逐字 + Vetora/Padho/CodeCrown 三域交叉（引 Dynamo/Cassandra/Ketama 数值，立场登记为二手转述）。
- **环只决定「放哪」， membership 与复制是另外的协议**：`consistent hashing gives you placement, not membership`——谁还活着靠 gossip/健康检查；Dynamo 系沿顺时针取 N 个不同节点作副本偏好列表；变体按形状选：Jump hash（Google 2014，零状态纯算术完美均衡，但桶须编号 0..N−1、只适合末尾增删，不适配任意节点故障）、Rendezvous/HRW（每键对每节点打分取最大，无需 vnodes、小 N 优选、O(nodes) 查找）、bounded-load（Google 2017，单节点负载封顶 (1+ε)×均值、溢出顺时针顺延，治倾斜与热键）；哈希只能均衡键数、不能均衡热度，热键另需缓存/扩散策略｜Harshith《Consistent Hashing: Surviving the Resize》+ Padho 环/jump/Maglev 对比 + CodeCrown 应用清单（Akamai/DynamoDB/Cassandra/Chord/Envoy/HAProxy）三域逐字。

### 来源与诚信
- `https://nginx.org/en/docs/http/ngx_http_upstream_module.html`（nginx 官方 upstream 模块文档，WebFetch 200 全文逐字：`hash key [consistent]` 语法/1.7.2 引入/ketama 方法/删加节点 remap 范围/ketama_points=160）——第一独立域·官方实现一手。
- `https://vetoralabs.com/system-design/concepts/storage/partitioning/consistent-hashing` + `https://learn.padho.ai/wiki/consistent-hashing-ring-jump-maglev`（Vetora 系统设计概念页与 Padho 工程 wiki，WebSearch 逐字：Karger 1997 / K·N 迁移 / 100–256 vnodes / 方差 O(1/(V·N)) / mod-N 1/(N+1) 保位 / jump·HRW·bounded-load 变体——第二、三域交叉）。
- `https://harshith.in/blog/consistent-hashing` + `https://codecrown.in/distributed-systems/consistent-hashing-distributed-systems`（Harshith 工程博客与 CodeCrown 分布式专栏，WebSearch 逐字：placement≠membership / 顺时针取副本 / 热键不可被哈希修复 / Dynamo·Cassandra·Ketama·Chord 应用）——第四、五域交叉（C++ 代码段未采纳，立场登记）。
- **判非**：全库 SKILL.md / module-memory 对 `一致性哈希`/`consistent hashing` 0 专节（wb-context-compressor 仅一句「自建一致性哈希」作 session sticky，非方法论节；DLQ/扇出/背压/Lease 选主/Actor/确定性重放/CQRS 各管不同编排面）；豆包自留地 WB 0 落地。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。


## r807B · Process Manager 编排：显式流程状态 + 决定下一步，与 Saga 补救是正交两件事（OI · 2026-11-25 实拉，≥2 独立域一手交叉，3 独点）

**独点1** Saga 与 Process Manager 是两个不同职责、可共存，别混成一个词：Saga = 一串各服务本地事务 + 配套补偿（compensating transaction），失败时语义撤销已完成步骤，**补偿不是回滚**——原交易已提交，退款/释放库存是另一笔可见新交易（Milan 逐字「A compensation is not a rollback...the refund is a second transaction, visible on the customer's statement」）；Process Manager = 持有每个流程实例显式状态、消费事件产出命令的**有状态状态机**（「Stateful / Event-consuming and command-producing / The single place where the flow is written down」）。关键分工： coordination（谁决定下一步：集中 PM/orchestration vs 分布式 choreography）与 failure-handling（重试/补偿/人工升级）是**正交两轴**——「Coordination style does not eliminate the need to choose recovery behavior」；编排式 saga 通常用 PM 跑补偿，协同式 saga 无中心协调者仍有补偿，PM 也能驱动无补偿的审批流。判据——问「用 saga 还是 PM」是错问法，应分别问「怎么协调」+「怎么补救」。

**独点2** 状态放哪决定可运维性，选择判据是「分支/超时/人步骤/钱/运维要能查能解卡」：协同式 saga **无中心状态**——库存听 OrderPlaced、支付听 StockReserved、物流听 PaymentCaptured，订单 4712 卡在哪隐含在「哪些事件已发生」里，要回答得跨服务关联事件拼进度视图；PM 的持久化状态可直接暴露当前步骤、最后转移、deadline，定时 timeout 与校验过的恢复命令让人工干预显式（Milan 逐字「where is this order stuck?」对照两案）。选型起点：2–3 步线性低失败风险→choreography 保持简单；有分支、超时、人工步骤、钱、或运维必须能 inspect/unstick→PM，且补偿定义在它所撤销的流程旁边。Microsoft 官方补充：orchestration 集中控制器「stores and interprets the states of each task, and handles failure recovery by using compensating transactions」，优点避循环依赖/责任清晰、缺点引入单点故障；choreography 无单点但加步骤后「workflow can be confusing」「risk of cyclic dependency」「integration testing is difficult」。判据——纯二选一是错的，工业实践常混合：核心合规/权限用集中编排保确定性，跨领域通知/同步用事件协同。

**独点3** 可靠性的五条 plumbing 是两种模式都绕不开的硬约束，加 pivot 概念定「不可逆点」：① 状态+外发消息**同事务**落库（outbox），只存状态不发命令或反之都会损坏流程，内存 outbox 不持久；② 参与者幂等（重试使每条命令可能到两次，「reserving stock twice for one order must be a no-op」）；③ 协调幂等（inbox 去重消息 ID + 拒绝非法转移，inbox 记录/状态变更/外发消息一个事务）；④ 并发投递用并发令牌或每实例锁，冲突后**重新加载并重评估事件**再重试，不盲目重发旧命令；⑤ 结果不明用稳定 operation ID——支付捕获后超时不证明捕获失败，AwaitingShipment 后重复的 PaymentCaptured 不得再排一次发货，同一操作换 payment ID 是需调查的 discrepancy 而非可忽略的重复。补偿须当**一等业务操作**（部分退款/手续费/时限由领域专家定义、可被重试失败故要 visibility+recovery），因此把最难撤销的动作排最后。Microsoft 官方三分类定 pivot：compensable（可反向）/pivot（不可返回点=最后可撤或首个可重试）/retryable（跟在 pivot 后、幂等、最终一致），数据异常靠 semantic lock/commutative updates/pessimistic view/reread/version files 缓解。与 §十三 reconcile（纠偏循环）、§十四选主（谁当主）、§r738A 恢复语义（checkpoint≠可恢复）、§r800B CQRS（读写分离）分工：那些管纠偏/资格/恢复粒度/读写边界，本节管「谁决定流程下一步 + 补偿与协调为何分轴」。

**判重**：`Process Manager`/`流程管理器`/`编排式 saga`/`pivot transaction`/`协同式 saga` 在 personal-ai-employees 本体 0 命中（§r738A 只有一句 compensating activity 幂等键、§r800B 有 outbox+幂等消费，均为 CQRS 语境非机制专节）；全库 Saga 命中集中在 engineering/ei-reliability、wb-execute-discipline（豆包自留地）、ki-knowledge-graph、wb-subagent-delegation，经查均为异命题或术语提及，豆包自留地 WB 0 落地；与 r804B 一致性哈希、r781A 选主、r793A 重放等结论不复用。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。

**来源与诚信**（≥2 独立域一手）：https://milanjovanovic.tech/blog/process-manager-vs-saga-pattern（Milan Jovanović 2026-09-22 一手全文 WebFetch 200 逐字：saga/PM 定义与正交性 / compensation is not a rollback / 有状态消费事件产命令 / where is order 4712 stuck / 选型起点 / 五条 plumbing / 补偿一等业务操作 / 最难撤销排最后）——第一独立域·一手全文；https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/saga/saga（Microsoft Azure 官方 Saga 页 WebFetch 200 全文逐字：compensable/pivot/retryable 三分类 / pivot=point of no return / choreography vs orchestration 利弊 / 单点故障与循环依赖 / 数据异常五缓解）——第二独立域·官方一手；https://ddd-fans.github.io/ddd-guideline/modeling/oo/process-manager.html + https://praveentn.live/architecture/terms/process-manager（WebSearch 逐字：长业务流程三特征多本地事务/可暂停持久化/耗时；编制集中 vs 编排分散；PM 介于两者之间订阅事件维护状态发命令；全流程用原则选 choreography 的系统往往用状态列+定时任务蹩脚重建 PM）——第三、四域交叉（立场登记）。数字/术语挂可复拉 URL。
