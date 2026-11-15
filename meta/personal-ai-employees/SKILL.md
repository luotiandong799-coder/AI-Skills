---
name: personal-ai-employees
description: >-
  个人 AI 员工体系（8 岗）总路由与五步执行协议。把用户目标自动分派给 8 个专职 AI 员工（战略顾问/供应链专家/职业发展顾问/销售顾问/学习教练/信息分析师/自动化工程师/知识管理专家），每岗统一走「任务分析→执行方案→输出结果→复盘优化→Skill沉淀」，并复用 personal-ai-os 与现有 wb-* / 专家技能，不新建重复能力。触发词：个人AI员工、AI员工体系、AI战略顾问、AI供应链、AI职业发展、AI销售顾问、AI学习教练、AI信息分析、AI自动化工程师、AI知识管理、哪岗来做、分派任务、员工路由、agency、个人AI公司、我的AI团队。
version: 1.3.0
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
