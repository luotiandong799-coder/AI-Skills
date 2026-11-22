---
name: execution-intelligence
description: 执行智能主动调用治理规范（方案 A）。当任务属于多步骤/依赖/批量改动/部署/条件分支/验收类，或需要明确风险边界与执行证明时，按本规范主动调用 _tools/execution_intelligence.py 做 EDG 规划、Guard 判定、GDR 复用与 CCS 验收。不注册 Hook、不接管宿主工具调用、不改模型路由/权限。契约测试、contract testing、Pact、consumer driven contract、消费者驱动契约、provider verification、Pact Broker、can-i-deploy、provider states、contract by example。Property-based testing、property testing、QuickCheck、基于属性测试、generator、shrink、收缩反例、不变式、invariant
module: EI
modules: EI
version: 1.4.0
---

# execution-intelligence · 执行智能主动调用治理规范（方案 A）

> 采用方案 A：**被动架构下 Agent 主动调用**。不注册 Hook、不接管宿主工具调用链、不改模型路由/权限/现有工作流。
> 依托工具：`D:\腾讯AI\skills\_tools\execution_intelligence.py`（EDG / GDR / CCS，纯标准库，已自测 8/8 + 验收对照通过）。
> 本文件是"何时调、怎么调、安全边界"的治理约定，不是工具本身。

## 一、定位

execution_intelligence.py 不是每次对话必跑的工具，而是**复杂 / 确定性 / 多步骤 / 高风险**任务的规划与验证组件。它只做"已确定动作的保存、校验、复用与记账"，不代宿主跳过模型回调——真正的跳过由宿主按 `plan` 输出执行。

### 本质：执行治理层，不是又一个 AI 助手

EI 不负责替代大模型思考，也不负责生成答案；它帮助 Agent 在执行复杂任务时做到：**先规划、再执行、控制风险、减少重复、最后验收**。

四大模块对应职责：

| 模块 | 作用 | 通俗理解 |
|---|---|---|
| EDG | 执行依赖图编译 | 把复杂任务拆成有先后关系的步骤 |
| Guard | 条件与风险判断 | 判断当前步骤能不能执行 |
| GDR | 执行复用判定 | 判断以前做过的工作能不能复用 |
| CCS | 执行证书 | 检查任务是否真正完成，留下验收依据 |

与 Agent / Skill / Hook 的关系（各司其职，不越位）：

| 技术 | 核心职责 |
|---|---|
| 大模型 | 思考、理解、决策 |
| Agent | 调度工具、执行任务 |
| Skill | 提供专业知识和操作能力 |
| Hook | 在特定执行节点自动触发逻辑 |
| EI | 管理执行计划、约束、复用和验收 |

一句话总结：**EI 不负责告诉 AI 应该想什么，而是负责让 AI 把决定要做的事情，有计划、有约束、可追踪、可验收地完成。**

### 三个必须守住的边界

1. EI 不会让模型本身变得更聪明——它只治理"执行过程"，不改造"思考质量"。
2. EI 不会自动提高所有任务的回答质量——仅对多步骤 / 确定性 / 高风险 / 需验收类任务有收益。
3. EI 若规划逻辑不准确，反而可能增加执行成本——故坚持"先审计、后设计、再实施、最后验证"；GDR 仅在条件全满足时复用，不确定一律交回 LLM 重新判断。

## 二、触发条件（应主动评估并优先调用）

满足任一即启用：

1. 多步骤、存在依赖关系的复杂任务。
2. 多个 Skill / 工具需要协同执行的任务。
3. 涉及文件批量修改、代码部署、配置变更的任务。
4. 存在明确条件分支、执行约束或失败回退要求的任务。
5. 自动化工作流及需要结果验收的重要任务。
6. 需要明确风险边界和执行证明（证书）的任务。

**默认不调用**：普通问答 / 翻译润色改写 / 简单资料查询 / 纯创意讨论 / 调用成本明显高于收益的简单操作。

## 三、执行流程

1. 判断任务是否符合触发条件。
2. 检查 EDG 规划输入（spec）与事实数据（facts）是否完整。
3. 调用工具：`compile` → `plan` →（执行后）`certify` → `stats`。
4. 读取并核对 `plan` 的 Guard / GDR 结果（reuse / already_done / needs_llm / confirm_required / blocked）。
5. 按结果制定执行策略：**reuse/already_done 才可跳过模型重判**；needs_llm 必须交回 LLM；confirm_required 须先取得用户确认；blocked 不得执行。
6. 执行任务，**禁止把规划结果等同实际完成**。
7. 完成后验证真实结果（证据），不得伪造成功。
8. 对适用步骤生成 / 校验 CCS 证书（**无真实 evidence 默认拒发**）。
9. 工具不可用时，回退到 WB 原有执行流程并明确说明。

## 四、调用接口（工具路径固定）

```bash
cd "D:/腾讯AI/skills/_tools"
python execution_intelligence.py schema                                       # 查看 spec/facts 结构约定
python execution_intelligence.py compile <spec.json> <edg.json>               # 结构/权限/参数三重校验 -> EDG
python execution_intelligence.py plan   <edg.json> <facts.json>              # GDR 五态判定
python execution_intelligence.py guard  <edg.json> <facts.json> <step_id>    # 单条 Guard 求值
python execution_intelligence.py certify <edg.json> <facts.json> --ledger <certs.jsonl>   # 签发证书（需证据）
python execution_intelligence.py run    <edg.json> <facts.json> [--apply] [--write-facts out.json]  # 保守执行器，默认 dry-run
python execution_intelligence.py stats  <certs.jsonl>                        # 账本聚合
python execution_intelligence.py selftest                                  # 8 组内置用例
```

返回约定：成功返回 JSON + 退出码 0；编译/文件/参数错误返回 `{"ok":false,...}` + 退出码 2。

## 五、安全边界（硬性）

- 不绕过 WB 原有权限与安全机制；不擅自注册 Hook；不擅自改模型路由。
- 规划工具不得自动执行未授权操作；高风险步（risk=high）未确认绝不执行（见 E6 验证：deploy 高风险步 `--apply` 仍不执行）。
- 缺失事实不得当成已验证事实；facts 中 `evidence` 字段必须来自真实执行，否则证书拒发。
- 工具不可用时回退原有流程并说明。

## 六、试运行记录（2~4 周）

每次调用记录：调用次数与原因、EDG 规划有效性、Guard 判断准确性、GDR 复用效果、CCS 验收情况、额外耗时、误/漏调用与失败。试运行结束后形成评估报告，再决定是否进入 Hook 灰度。

## 七、诚实边界（工具侧，不得宣称已解决）

1. 不代宿主跳过模型回调：`plan` 只输出"该步是否需要模型重新判断"。
2. `tokens_saved_estimate` 为估算口径（默认 1200 输入 + 300 输出/次），非实测。
3. 未实现 RSI（自动改提示/Guard/配置）：缺独立验证集与回滚通道，按规范 P2/P3 暂缓。
4. Guard 表达式仅支持比较与布尔组合，不支持函数调用；未知字段返回 unknown 而非 false。
5. **已知限制（待修复，本轮不重构）**：`run --apply` 执行子进程时，若子进程输出含非 UTF-8 字节（如 GBK 路径），后台读线程会抛 `UnicodeDecodeError`，导致 evidence 截断；默认 dry-run 不受影响。修复需改 `run_steps` 的 subprocess 编码处理，留待后续轮次。

## 八、停用 / 回滚

- 停用：不再在触发任务中调用即可，零副作用（工具不被任何 Hook/自动化引用）。
- 卸载：删除本 SKILL.md 及 `D:\腾讯AI\skills\_tools\execution_intelligence.py` + 其 `_acceptance_ei_*` 验收件；未改动任何既有工具、规则、模型配置或插件权限。


## 九、契约式执行：Guard 的最小完备集与责任归属（2026-11-08 实拉，r715A）

> 方法论实拉：CMU SEI《API Security through Contract-Driven Programming》（2024-03-18，WebFetch 一手全文逐字）+ llm-coding.github.io/Semantic-Anchors·Design By Contract + 中文维基《契约式设计》+ sagecode.org Eiffel 教程，共 4 独立域交叉。与 §三 Guard 判定分工：§三管「五态结果怎么读」，本节管「断言该写哪三类、失败算谁的」。

- **r715A-1 契约三问＝执行规格的最小完备集**：每步（每次调用）须同时答 ① **expect** 前置条件（运行前必须为真）② **guarantee** 后置条件（运行后必须为真）③ **maintain** 不变式（无论怎么变换都不许变）——SEI 逐字 `What does the contract expect? / What does the contract guarantee? / What does the contract maintain?`（Hoare triple 三问）。且**每条断言只有一个责任方**：前置违反＝调用方（client）的 bug，后置或不变式违反＝实现方（supplier）的 bug；SEI 原文 `A caller or consumer that uses an API function whose preconditions are not met is not entitled to the postconditions`。⇒ 落地到本技能：EDG 每步 Guard 不只写「能不能跑」，要写明三类断言；CCS 拒发证书时按责任方分类（输入不合规 / 输出没达标 / 状态被破坏），而非一律「未完成」。**不双方重复防御性检查**（Semantic Anchors 逐字 `No defensive double-checking on both sides`）：内部可信接缝由调用方保证前置即可，供应商不必再校验被自己前置排除的状态。
- **r715A-2 契约继承三不可违 + 边界张力**：复用/替换既有步骤（子类型、新实现、换工具）时，SEI 逐字 `Preconditions cannot be strengthened` / `Postconditions cannot be weakened` / `Invariants cannot be weakened`——实现不得收窄可接受输入、不得放大输出范围、不得改变不变式（`pop()` 不许新增「栈至少 5 个元素」的前置；`size` 永不为负）。这是 Liskov 替换原则的契约级表述。安全反例：OWASP 2023 API 头号风险 **BOLA** 即「实现未履行前置条件」（请求须携带对**该特定对象**有效的授权 token）⇒ 安全缺陷可归约为契约违约。与 **Postel 定律**按边界分工：DbC 对**可信内部模块缝**严格、违约 fail hard；Postel 对**不可信外部输入**宽松；混用会把无效状态放进内部。⇒ 判据：换实现先验这三条，别只看「接口签名没变」。
- **r715A-3 机检天花板：不是每条契约都能自动生成断言**：OpenAPI 能表达前置（输入域、security scheme）与后置（返回码 + schema），**无法表达不变式**——SEI 逐字 `there is, however, no way to document outside of a text description what an endpoint may or may not change in terms of state`（REST 的 GET 幂等只能写文字）。RESTler / Dredd 从 OpenAPI 自动生成测试用例、JML 编译器把 Javadoc 转成运行时断言，前提都是契约**机器可读**。⇒ 验收设计必须把「能自动生成的断言」与「只能人工复核的文字约定」分开列；文档里写了一句「幂等」不等于已验收，CCS 对后者只能标「需人工」，不得据文字描述签 PASS。

**提升层**：工作流（执行规格与验收判定）+ 可复用 Skill。触发词：契约三问、expect/guarantee/maintain、责任归属、前置不可加强、后置不可削弱、不变式、BOLA、Postel 边界、OpenAPI 不表达不变式、fail hard、断言自动生成。

**判非（本轮独立实拉 5 域，登记不落地）**：progressive delivery 线（`sre.google/workbook/canarying-releases/` / `alerting-on-slos/` 的 canary 受控实验、error budget、multi-window multi-burn-rate、time confounding；Argo Rollouts `AnalysisTemplate` 自动 abort；`DrHazemAli/enterprise-system-design` change class CH0–CH4 + gate invariants I1–I10；techsensedev GKE SRE pipeline；kubo.hexabase 5% 流量×20% 错误率→整体 1%）已逐域取证，但 `engineering/wb-release-maintain` 现存 canary 概念 4 处，且该线属发布运维而非 EI 契约语义 ⇒ 按 rules/07 去重铁律判非换道，留候选池，不冒充本轮独点。

## 十、来源（2026-11-08 r715A 实拉）

- `resources.sei.cmu.edu/blog/api-security-through-contract-driven-programming/`（CMU SEI，2024-03-18，WebFetch 一手全文逐字：Hoare 三问、三不可违、BOLA、OpenAPI 不表达不变式、RESTler/Dredd/JML）
- `llm-coding.github.io/Semantic-Anchors/anchor/design-by-contract`（DbC 语义锚：责任归属、契约继承与 LSP、Postel 边界张力、No defensive double-checking）
- `hackcn.de/zh-cn/契约式设计`（中文维基：契约三问、供应商不校验前置、fail hard、发布版可移除断言）
- `sagecode.org/roadmap/pgp/eiffel/`（Eiffel require/ensure/invariant 语法与继承规则）


## 十一、写操作的三态结果、对账先于重试、不可撤销边界（2026-11-11 r734C 实拉，五独立域交叉）

> 与 §九（契约三问／责任归属／LSP／机检天花板）分工：§九是**静态契约断言**（expect / guarantee / maintain）；本节是**失败语义与恢复协议**——调用返回后到底发生了什么、谁有权决定重试、补偿的边界在哪。EDG 每步 Guard 与 CCS 证书据此扩展，不改动 `_tools/execution_intelligence.py` 现有接口。

- **r734C-1 ★写结果必须三态，超时是「未知」不是「失败」；未知态禁止让模型重新生成调用**：vdf.ai《Transaction-Safe AI Agents》(2026-08-17) 逐字 "Separate three write outcomes: **confirmed success** ... **confirmed rejection** ... **unknown outcome**: the caller cannot establish whether the target committed"；"Connection reset, timeout, worker crash, and lost acknowledgement usually belong in the third category. The orchestrator should **preserve the same operation identity** and query or retry according to the tool contract. **It must not ask the model to regenerate the call: regeneration can change parameters and turn one ambiguous operation into a new one**"；reazromen.com 逐字 "**A timeout is an ambiguity boundary** — After a timeout, the caller does not know whether the remote operation happened"；hyperacademia 逐字 "Unknown is **not a temporary synonym for failure**"。判据：① EDG 步骤状态除成功／失败外须有 `OUTCOME_UNKNOWN`／`RECONCILING`／`MANUAL_REVIEW` 三分支，CCS 不得据超时签 FAIL 并触发重发；② 未知态下保持同一 operation identity 去查或按契约重放，**禁止模型自行重写参数重试**——那会把一个歧义操作变成第二个业务意图；③ 与 §九「前置违反归调用方」互补：三态说的是「结果不可判定」，不是「断言被违反」，两者不能混为一条 Guard。

- **r734C-2 ★重试权在对账者不在执行器；「查无此对象」是弱证据**：developers.dev《Ambiguous Timeouts in Consequential API Calls》逐字 "**Notice what is missing: there is no retry loop in the executor. Retrying is a decision made by the reconciler, with knowledge of the target's contract, not a reflex of the sender**"；"**A lookup that finds nothing is weak evidence.** Several explanations coexist: the request never arrived, it arrived and is still executing, it committed but the read path lags behind, or it was rejected"；转 `FAILED_TERMINAL` 须三条同时成立（目标有 read-after-write 语义或已过文档化传播上限；操作已过 deadline 且能 cancel／fence 迟到请求；同键重放不可用或返回文档化的「无副作用」确定错误），否则 "keep the state UNKNOWN and keep the reconciliation task alive, or escalate. **An unresolved operation sitting visibly in a queue with an owner is a healthier outcome than a guess**"；同篇给出四类目标能力表（A 幂等键 + 留存窗口内可重放／B 按自有引用查询／C 目标侧 If-Match 条件变更／D 全无 → "**Do not auto-retry**"）；并明写 "If you also run saga-style multi-step workflows, **the UNKNOWN state becomes an explicit branch in the saga, handled before any compensation is issued**"。判据：① EDG 每步 Guard 标注该目标属于 A/B/C/D 哪一类，未标注按最弱档 D 处理；② 补偿必须在未知态收敛之后，先补偿未确认的操作是独立事故源；③ reazromen 逐字 "Retries are for transient failures, **not uncertainty**"（亦见 GitHub jpcaparas 分布式韧性表）——重试资格由结果可判定性决定，不由错误码或重试次数决定。

- **r734C-3 ★契约要写 effect class 与 point of no return；补偿不是回滚，验收断言业务后果**：vdf.ai 契约字段表逐字 `Effect class | Read, reversible, compensable, or irreversible`、`Success receipt | Stable target ID, version, timestamp, and effect`、`Status lookup | How an ambiguous outcome is reconciled`、`Compensation | Action, required inputs, approval, and deadline`、`Point of no return | Stage after which automatic reversal is unsafe`；"**A sent message cannot be unsent**; its compensation may be a correction or human follow-up"；FAQ 逐字 "Compensation is **a new, domain-specific action** ... It **does not erase history, may not restore the exact original state, and can itself fail**"；"Put irreversible legal, physical, or financial actions **last**, behind deterministic checks and required human approval"；验收逐字 "**Assert business outcomes—one case, one message, one reservation—not merely successful HTTP responses**"；幂等键按业务意图生成而非载荷——"**Do not derive the key solely from the payload.** Two legitimate orders may have identical parameters"、"**Retention must exceed the maximum replay window.** A key that expires after an hour cannot protect yesterday's restored workflow"（reazromen 逐字 "**The idempotency window is part of the contract**"）。判据：① CCS 证书除「调用成功」外须记 success receipt 与 effect class，HTTP 200 不构成业务完成证明；② 不可逆动作排在流程最后并前置确定性检查 + 人工审批；③ 故障注入点须覆盖 dispatch 后／目标 commit 后／receipt 入库前／补偿中途，并测「同键不同参数」「留存过期后重放」；④ 与 `engineering/ei-reliability` 的 Saga 骨架分工：那边管「失败后不丢状态、能续能回」，本节管「结果三态、对账资格、补偿不是撤销」。

**提升层**：工作流（执行台账与恢复协议）+ 可复用 Skill。触发词：OUTCOME_UNKNOWN、ambiguity boundary、confirmed rejection、reconcile before retry、no retry loop in the executor、weak evidence、四类目标能力、If-Match、effect class、irreversible、point of no return、success receipt、sent message cannot be unsent、assert business outcomes、idempotency window、retention exceed replay window。

**判非（本轮独立机检，登记不落地）**：`ambiguity boundary`／`weak evidence`／`Assert business outcomes`／`no retry loop`／`durable operation`／`effect class`／`retention window`／`point of no return`／`cannot be unsent`／`Diebold-Mariano` 全库 SKILL.md **0 命中**；`OUTCOME_UNKNOWN` 2 命中与 `unknown outcome` 1 命中位于豆包自留地 `engineering/wb-execute-discipline`（r726A 语义为「恢复续跑时哪些动作需先检查」）与 `system/browser-skill`／`bsk-drive-logged-in-browser`（`borrow_outcome_unknown` 为浏览器标签借用结果枚举），**均无三态契约／对账资格／effect class／补偿边界**；`reconcil` 6 命中、`idempotency key` 2 命中、`retry budget` 1 命中同样集中在豆包自留地，语义为幂等键造法、重试预算、checkpoint 续跑与定时任务 owner 回收 ⇒ 按去重铁律取「优＝加厚现有」，本轮落 `engineering/execution-intelligence` 且 **WB 0 落地** `wb-execute-discipline` / `wb-context-compressor`；`engineering/ei-reliability` 既有 Saga／补偿／幂等／超时骨架不重立论，本节只补失败语义层。

### 2026-11-11 r734C 增补来源（逐字核验，五独立域交叉）

- `vdf.ai/blog/transaction-safe-ai-agents-idempotency-compensation`（VDF AI，2026-08-17，WebFetch 200 全文逐字：三态定义、durable operation ID 作用域与留存、契约字段表七行、PLANNED→COMMITTED + OUTCOME_UNKNOWN/RECONCILING/MANUAL_REVIEW 状态机、"A sent message cannot be unsent"、"Assert business outcomes"、补偿非回滚 FAQ、故障注入清单；页面含产品导流，立场如实登记，结论一律与 developers.dev / reazromen 交叉后采纳）
- `www.developers.dev/tech-talk/ambiguous-timeouts-in-consequential-api-calls-a-reconcile-before-retry-design-for-tech-leads.html`（WebFetch 200 全文逐字："no retry loop in the executor"、四类目标能力表 A–D、not found 弱证据与三条 FAILED_TERMINAL 前置、UNKNOWN 作为 saga 显式分支先于补偿、"An unresolved operation sitting visibly in a queue with an owner is a healthier outcome than a guess"）
- `learn.reazromen.com/posts/open-systems-145-timeouts-retries-backoff-and-idempotency.html`（2026-10-07，WebFetch 200 全文逐字："A timeout is an ambiguity boundary"、"Retry only errors that can plausibly recover"、"retry budgets limit amplification"、"Deadlines should be end-to-end"、"**The idempotency window is part of the contract**"、"Retries are safe only when failure ambiguity, deadlines, and operation identity are designed together"）
- `hyperacademia.org/hm/.../effect-reconciliation-compensation-contracts`（WebSearch 快照逐字：intent_id / attempt_id / effect_id / compensation_id 四身份、"Unknown is not a temporary synonym for failure"、While unknown「fence new effects、stop automatic semantic replanning」、Stripe 24h key pruning 为产品特定语义非通用定义）
- `github.com/jpcaparas/skills/blob/main/skills/engineering/maintainable-code/references/distributed-systems.md`（WebSearch 快照逐字："**Retries are for transient failures, not uncertainty**"、"Email sent -> cannot unsend"、幂等键留存须超过 retry + provider uncertainty window、超时分层）· `RFC 9110` / `AWS Builders' Library: Making retries safe with idempotent APIs` / `Microsoft compensating-transaction pattern` 为 vdf.ai 所列一手参考链，本轮未逐篇直读，仅登记不冒充

## 十二、租约正确性：锁到期不等于旧持有者停手，fencing token 把安全落到资源侧（2026-11-19 r773B 实拉）

> 来源（≥2 独立域一手）：`martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html`（Kleppmann 原文，2016-02-08，WebFetch 200 全文逐字）；`primitives.pub/distributed-systems/monographs/fencing-tokens`（独立一手专著，含 resource-server 校验伪码）；`unseel.com/cs/fencing-tokens.html`（独立一手，token 33/34 时序与 ZooKeeper/etcd/Chubby 实例）；`hivebook.wiki/wiki/redis-distributed-locks-redlock-pitfalls-gc-pauses-clock-skew-fencing`（Redlock 反面与 fencing 判据）。> 分工：§十一管「结果三态 / 谁有权重试 / 补偿不是撤销」——那是**调用结果语义**；本节管「同一时刻谁有权写、旧持有者醒来后资源凭什么拒绝」——那是**互斥与资源侧准入**。§r749B deadline 管时间预算，本节管 lease 到期后的僵尸写，三者正交。

- **r773B-1 ★租约到期解决可用性、不解决旧持有者：GC 暂停/网络延迟让两个客户端「同时持锁」**：Kleppmann 逐字「if the GC pause lasts longer than the lease expiry period, and the client doesn't realise that it has expired, **it may go ahead and make some unsafe change**」「**You cannot fix this problem by inserting a check on the lock expiry just before writing back to storage** ... GC can pause a running thread at *any point*, including the point that is maximally inconvenient for you (**between the last check and the write operation**)」；网络面逐字「in a famous incident at GitHub, packets were delayed in the network for approximately **90 seconds**」⇒ 判据：① 别把「写前再查一次锁是否过期」当护栏——检查与写入之间永远有可暂停的缝隙；② 进程暂停来源不止 GC（缺页、EBS 同步网络请求、CPU 争抢、SIGSTOP），语言无 GC 不等于免疫；③ 锁只减少重复劳动（efficiency，重复无害）与锁保护不变量（correctness，重复即损坏状态）是两种用途，Kleppmann 逐字「you need to be very clear about which one of the two you are dealing with」——只有后者需要 fencing，前者单节点锁 + 明确记录「锁只是近似」即可。落到 EI：EDG 每步 Guard 须标注该步的互斥是 efficiency 还是 correctness，后者不得仅凭「有锁/有 lease」签 CCS。
- **r773B-2 ★fencing token 是单调递增数 + 资源侧记住「已见最大值」并拒绝回退的写**：Kleppmann 逐字「a fencing token is simply a number that increases (e.g. incremented by the lock service) every time a client acquires the lock」「Client 1 ... token of 33 ... lease expires. Client 2 ... token of 34 ... sends its write ... including the token of 34. Later, client 1 ... sends its write ... including its token value 33. However, **the storage server remembers that it has already processed a write with a higher token number (34), and so it rejects the request with token 33**」「this requires **the storage server to take an active role in checking tokens**, and rejecting any writes on which the token has gone backwards」「provided that the lock service generates **strictly monotonically increasing tokens**, this makes the lock safe」。primitives.pub 伪码逐字「if request.fencing_token <= highest_token: return REJECT('stale fencing token')」「**The highest_token value must be stored durably**... If the resource server crashes and restarts with highest_token reset to zero, it would accept previously-rejected stale tokens」；unseel 指出 token 必须**跨重启持久且严格递增**——随机 UUID / 墙钟时间戳（受 skew 与 NTP 跳变）/ 锁服务重启即归零的计数器都破坏不变量。⇒ 落到 EI：① CCS 对 correctness 互斥步，除 outcome/effect class 外须记「本次 fencing token」与「资源已见最高 token」，token 回退即拒发证书；② 资源侧校验与写入须在**同一原子边界**（unseel 逐字「The comparison and the protected write must share one atomic boundary」），「先验 token 再过一会写」留新竞态；③ token 单调性源于共识日志（ZooKeeper zxid / znode version、etcd mod_revision、Chubby sequencer）而非本地时钟——对应 §r738A「随机数/时钟/LLM 进 Activity」的同源纪律。
- **r773B-3 ★fencing 的边界：资源不配合就 fence 不了；kleppmann 判 Redlock「两头不靠」**：unseel 逐字「If the resource is a dumb blob store with no conditional-write primitive, **you can't fence it directly** — you must front it with something that can (a transactional layer, or object-storage conditional/If-Match writes)」；hivebook 逐字「Redis by itself does not generate fencing tokens ... you would need a monotonic counter, e.g. INCR, that survives failover — which Redlock's multi-master design does not cleanly provide」「Distinguish efficiency vs correctness locks up front」。Kleppmann 结论逐字「the Redlock algorithm is a poor choice because it is **'neither fish nor fowl'**: unnecessarily heavyweight ... for efficiency-optimization locks, but **not sufficiently safe for situations in which correctness depends on the lock**」「if you need locks for correctness, please don't use Redlock. Instead, please use a proper consensus system such as ZooKeeper ... **And please enforce use of fencing tokens on all resource accesses under the lock**」；Redlock 只在工作于 synchronous 系统模型（有界网络延迟 + 有界进程暂停 + 有界时钟误差）时正确，而「most of the time」对 correctness 不够。⇒ 落到 EI：① 若被保护资源无条件写原语（无 If-Match / 无 CAS），该步不得声明「已互斥」——要么前置事务层/条件写，要么按最弱档处理（同 §r734C-2 A/B/C/D 分类）；② 与 §r734C「UNKNOWN 先于补偿」的衔接：fencing 防的是**旧持有者醒来后的僵尸写**，UNKNOWN 管的是**本次调用结果不可判定**；fence 不能撤销旧持有者在资源见到新 token 之前已完成的写（unseel「Know where the guarantee ends」），那部分仍走 §r734C 对账/补偿。
- **归属与判非**：`fencing` / `fencing token` / `单调递增` / `stale holder` 在 EI 本体 0 命中（机检仅 `fence` 2 处为 r734C 来源 URL 内 "fence new effects" 与租约表述，非 token 机制本体）；全库 `fencing token` 本体 0。与 §r749B deadline / §r734C 三态 / §r738A 确定性重放异命题、按「合」登记不并存新层。豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地。加厚现有 1 技能，0 新建 / 0 合并 / 0 删除。

### 本轮来源（2026-11-19 r773B 实拉）
- `https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html`（Kleppmann 一手原文，2016-02-08，WebFetch 200 全文逐字：efficiency vs correctness、GC pause 破租约、"between the last check and the write"、fencing token 33/34、ZooKeeper zxid、Redlock 同步假设与"neither fish nor fowl"结论）
- `https://primitives.pub/distributed-systems/monographs/fencing-tokens`（独立一手专著，WebFetch：resource-server 校验伪码、highest_token 必须持久化、token 检查与保护写同一原子边界）
- `https://unseel.com/cs/fencing-tokens.html`（独立一手，WebFetch：token 不可为随机 UUID/墙钟、ZooKeeper zxid / etcd mod_revision / Chubby sequencer、资源不配合则 fence 不了、保证的终点）
- `https://hivebook.wiki/wiki/redis-distributed-locks-redlock-pitfalls-gc-pauses-clock-skew-fencing`（独立一手，WebSearch 全文：Redis 不自生成 fencing token、SET NX PX 与 Lua 释放、效率锁 vs 正确性锁判别）

## 十三、消费者驱动契约测试 Pact（r785B｜2026-11-20 实拉）

> 与 §九「契约三问 expect/guarantee/maintain」、§十一「结果三态与对账」正交：那两节把契约定成规格，本节补「契约怎么变成可执行断言并在部署前机检」。来源：docs.pact.io 官方 Introduction + Pact Broker 页双一手 WebFetch 200 全文逐字。

- **★Pact 把契约从文字约定变成「契约样例」：consumer 测试时生成、只覆盖实际用到的通信，未用行为可自由改**：官方逐字「Pact is a code-first tool for testing HTTP and message integrations using `contract tests`. Contract tests assert that inter-application messages conform to a shared understanding that is documented in a contract」；「**Contract testing** is a technique for testing an integration point by checking each application in isolation to ensure the messages it sends or receives conform to a shared understanding that is documented in a "contract"」；「a common way of implementing contract tests (and the way Pact does it) is to check that all the calls to your test doubles return the same results as a call to the real application would」。CDC 段逐字「Pact is a code-first *consumer-driven* contract testing tool ... The contract is generated during the execution of the automated consumer tests. A major advantage of this pattern is that **only parts of the communication that are actually used by the consumer(s) get tested**. This in turn means that any provider behaviour not used by current consumers is free to change without breaking tests」；与静态 schema 之别「Unlike a schema or specification (eg. OAS), which is a static artefact that describes all possible states of a resource, a Pact contract is enforced by executing a collection of test cases, each of which describes a single concrete request/response pair - Pact is, in effect, **"contract by example"**」。⇒ 落地：§九 expect/guarantee 断言若只写文字，CCS 不得签 PASS；把它落成 consumer 侧的 Pact 测试（每次 concrete 请求/响应对即一条样例），provider 未使用字段的变更不再破坏消费者测试。与 §九 r715A「OpenAPI 无法表达不变式、须分列可自动生成断言与仅人工文字约定」直接衔接：Pact 覆盖前者，文字约定仍留人工复核。

- **★provider 自证 ≠ 集成契约：只验自己 OpenAPI 不证消费者调用正确，可「spec 完美却 break 全部消费者」**：官方 provider contract testing 段逐字「a technique for ensuring a provider's actual behaviour conforms to its documented contract (for example, an OpenAPI document). This type of contract testing helps avoid integration failures by ensuring the provider code and documentation are in sync with each other. **On its own, however, it does not provide any test based assurance that the consumers are calling the provider in the correct manner, or that the provider can meet all its consumers' expectations, and hence, it is not as effective in preventing integration bugs**」。独立二手交叉（stackpractices.com 逐字）「OpenAPI validation only checks the provider's implementation against its own spec. It catches spec drift but knows nothing about consumers. ... An endpoint can be spec-perfect and still break every consumer that expected a field the spec deprecated quietly.」⇒ 门禁两栏分开：provider-spec 一致性（静态、只防漂移）与 consumer-provider 集成契约（CDC，防真实 break）；验收必须**两边都在 CI 跑**，consumer 写的契约若无人 replay「is just a wish list」。与 §r734C「查无此对象是弱证据」同族：单边证据不作放行依据。

- **★Broker 的四件事与 can-i-deploy 门：没 Broker 就得自己写，CCS 放行以验证结果为准不以契约文件存在为准**：官方 Broker 页逐字「Contract testing is an alternative approach to traditional integration testing that gives you tests that are quicker to execute, and that are more maintainable at scale ... the important information ... is now spread out across many different builds. The Pact Broker is a tool that brings all this information back together again, and allows you to deploy with safety」；无 Broker 须自己写「ensure that your contract tests have passed successfully *before* deploying a consumer or provider application (**can-i-deploy**)」「ensure that the provider verification takes place every time a pact changes (**webhooks**)」「ensure backwards compatibility ... (**branches**/**tags**)」「allow contracts to change without breaking provider builds (**pending pacts**)」。流程逐字：consumer mock 写「requests and the expected responses to a JSON "pact" file - this is the consumer contract」，发布时「specifying the *consumer application version* in the URL, not the pact version. The broker will take care of versioning the pact behind the scenes when its content changes」；webhook 在内容变时触发 provider 构建；provider「retrieves the pact(s) from the Pact Broker, replays each request against the provider, and checks that the responses match the expected responses. If the pact verification fails, the build fails」；provider/consumer 部署前各跑 `can-i-deploy`。⇒ 验收四步固定=consumer 生成并发布契约 → broker 记录版本/变更 → provider 回放验证（失败即构建失败）→ can-i-deploy 判定该版本组合是否可放行；**CCS 签 PASS 以 can-i-deploy 通过为准，不以「契约文件存在」或「本地测试绿」为准**。声明边界：契约只验接口不验系统行为（stackpractices「Contracts verify the interface, not the system」），保留薄 E2E 层，不拿契约测试替代集成/E2E。

- **判非/去重**：`契约测试` / `Pact` / `consumer driven contract` / `can-i-deploy` / `provider states` 全库 SKILL.md 正文 0 命中；EI §r715A「契约三问」与 §r734C「结果三态」为异命题（那条定规格与歧义态，本节定接口怎么机检与谁放行）。`canary` / 渐进交付线已在 r773B/execution-intelligence 明确判非换道（wb-release-maintain 已有 canary 概念），本轮不重做发布策略。**豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地**。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。

- **来源与诚信**：① `https://docs.pact.io/` — Pact 官方一手 WebFetch 200 全文逐字（code-first 定义 / contract testing 隔离验证 / consumer driven / contract by example / only-used-parts / provider contract testing 局限 / when to use；Last updated Aug 25 2026）——**第一独立域·官方一手**；② `https://docs.pact.io/pact_broker` — Pact 官方一手 WebFetch 200 全文逐字（Broker 目的 / 无 Broker 四件自写 / can-i-deploy / 版本化 / webhook / consumer 三步与 provider 回放失败即构建失败 / Step3 回 consumer；Last updated Sep 27 2024）——**同官方第二页·一手**；③ `https://stackpractices.com/patterns/contract-testing-pattern` — 独立一手 WebSearch 逐字（provider state / exact value matching 用 like() / 契约不验系统行为 / OpenAPI vs 契约「spec-perfect still break every consumer」）——**第三独立域交叉**。两官方页同域名如实登记为「同官方两页」而非两独立厂商；「only-used-parts」为 Pact 的 CDC 特性非所有契约测试范式共性。

## 十四、基于属性测试 PBT：随机生成 + 收缩反例验不变式（r789B｜2026-11-22 实拉）

> 与 §九「契约三问 expect/guarantee/maintain」、§十三 Pact（契约样例验接口）正交：那些管「具体请求/响应对」，本节管「用不变式覆盖未枚举的输入空间」。来源：lib.rs quickcheck2 crate + QuickCheck Haskell 官方手册 + Hackage Arbitrary 文档，三一手 WebFetch/WebSearch 逐字。

- **★PBT 断言的是「高层不变式」不是举例：property 是返回 Bool 的函数，随机跑 100 组输入都要为真，失败即产反例**：官方手册逐字「At its simplest, a property is a function which returns a Bool. prop_reverseDoesNotChangeLength xs = length (reverse xs) == length xs. A property declares a high-level invariant of a program. The QuickCheck test runner will evaluate the function with 100 random inputs and check that the result is always True」；lib.rs 逐字「All QuickCheck needs is a property function—it will then randomly generate inputs to that function and call the property for each set of inputs. If the property fails (whether by a runtime error like index out-of-bounds or by not satisfying your property), the inputs are 'shrunk' to find a smaller counter-example」。⇒ 验收纪律：§九 expect/guarantee 若只举三五个样例覆盖不到未列举输入；把不变式（幂等 f(f x)==f x、长度不变、往返恒等 reverse(reverse xs)==xs）写成 prop_ 函数随机压测，作为 CCS 的「未枚举面」证据；PBT 与 Pact 互补不替代——Pact 锁接口契约，PBT 锁输入空间上的性质。

- **★shrink 才是 PBT 核心价值：把费解的随机大反例自动收敛到最小可调试反例**：lib.rs 逐字实例——不收缩时「TEST FAILED. Arguments: ([-17, 13, -12, 17, -8, -10, 15, -19, -19, -9, 11, -5, 1, 19, -16, 6])」pretty mysterious，收缩后「Arguments: ([0])」much easier to debug；「Shrinking is a crucial part of QuickCheck that simplifies counter-examples for your properties automatically」；「The shrinking strategies for lists and numbers use a binary search to cover the input space quickly」。Hackage Arbitrary 类逐字「shrink :: a -> [a] — Produces a (possibly) empty list of all the possible immediate shrinks of the given value. The default implementation returns the empty list, so will not try to shrink the value ... Most implementations of shrink should try at least three things: shrink a term to any of its immediate subterms; recursively apply shrink to all immediate subterms; type-specific shrinkings such as replacing a constructor by a simpler constructor」。⇒ 门禁：失败反例必须是收缩后的最小可复现输入，原始随机大对象不得直接判失败就收工；自定义递归类型要实现 Arbitrary 的 arbitrary（生成）与 shrink（收缩）两方法，否则「配了 PBT」却拿不到可调试反例。

- **★生成器质量决定能否发现 bug；前置条件用 ==> 且极稀有前提会 Gave up（假绿），加轮数有界适合发布前压测**：Hackage 逐字「good generators are often the difference between finding bugs and not finding them. You can use sample, label and classify to check the quality of your test data ... especially if your type is recursive」；手册逐字「If it's very unlikely for arbitrary inputs to match the precondition, QuickCheck can give up early. prop_overlySpecific x y = x == 0 ==> x * y == 0 → *** Gave up! Passed only 31 tests」。⇒ 三条：① 自定义类型先检视生成器分布（sample/label/classify），递归类型专门设计，不用默认 arbitrary 糊弄；② 用 ==> 限制定义域若命中率过低会 Gave up，须把前提编进生成器（如 NonEmpty 列表）而非靠过滤；③ 加轮数用 tests() 或 QUICKCHECK_TESTS，lib.rs 逐字「This will cause quickcheck to run for a much longer time. Unlike the loop approach this will take a bounded amount of time, which makes it more suitable for something like a release cycle」——发布前用有界加轮压测，不拿无限循环当测试。

- **判非/去重**：`Property-based testing` / `QuickCheck` / `generator` / `shrink` / `基于属性测试` 全库 SKILL.md 正文 0 专节；`不变式/invariant` 命中为 §九契约「OpenAPI 无法表达不变式须分列」（异命题——那条说不变式要单列，本节给不变式怎么机检），r734C「补偿不是回滚、验业务后果」为验收哲学非随机测试。`fuzzing` 为 lib.rs 关键词标签，PBT 有明确性质断言区别于无目标 fuzz，不混写。**豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地**。按 rules/07「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。

- **来源与诚信**：① `https://lib.rs/crates/quickcheck2` — quickcheck2 crate 一手 WebFetch 200 全文逐字（property function / 随机输入 / shrink 定义 / 16 元素大反例→[0] / 二分收缩 / tests() 与 QUICKCHECK_TESTS 有界时间 / Arbitrary 生成 struct）——**第一独立域·一手库文档**；② QuickCheck Haskell 官方手册（`so.parthpatel.net/haskell/doc/1156/quickcheck`）WebSearch 全文逐字（prop_ 命名 / 100 随机输入 / ==> 前置与 Gave up / maxSize 限输入规模 / quickCheckAll）——**第二独立域·官方手册**；③ `https://hackage.haskell.org/package/hspec-wai-0.9.1/docs/Test-Hspec-Wai-QuickCheck.html` — Hackage Arbitrary 类文档 WebSearch 全文逐字（arbitrary :: Gen a / shrink :: a -> [a] / 默认空 shrink 不收缩 / 三类 shrink 策略 / good generators 决定发现 bug / recursive 类型）——**第三独立域·一手 API 文档**。100 次为 QuickCheck 默认口径非普适常量，注册时写明。
