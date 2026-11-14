---
name: ei-reliability
description: 执行可靠性工程（Execution Intelligence · Reliability）。当任务涉及长流程、多步骤、可失败/可重试的写操作、跨系统动作、需要崩溃续跑或补偿回滚时调用。提供 Saga 编排、补偿事务、幂等键、断点续跑（持久化步骤状态）、有界重试+抖动、死信队列、超时。与 execution_intelligence.py 互补：本技能管"失败后怎么不丢状态、能续、能回"，EI 管"规划/门禁/证书"。
module: EI
modules: EI,VI
version: 1.1.0
---

# EI · 执行可靠性（Reliability Engineering）

> 本技能是 Personal AI OS 13 模块中 **EI（执行智能）** 的可靠性载体（与 `engineering/execution-intelligence` 互补：后者管 EDG 依赖图 / Guard 风险门禁 / GDR 复用判定 / CCS 证书；本技能管"失败后怎么不丢状态、能续、能回"）。
> 方法论实拉（2026-11-07 实拉）：learn.microsoft.com（Azure Saga）、microservices.io（Saga 模式原文）、adevguide.com（编排/合唱/补偿/幂等）、theaugmenteddev.com（持久化状态/幂等/超时）。

## 一、核心问题：执行不是"跑完就行"

长任务 / 多步骤 / 跨系统动作会失败（网络、崩溃、超时、部分成功）。朴素脚本失败即"未知状态"，下次只能重头来——但重跑会重复副作用（重复扣款、重复建单）。可靠性 = 失败后可续、可补偿、副作用不重。

## 二、Saga：把长事务拆成可补偿的本地步骤

- 一个业务操作拆成 **sequence of local transactions**，每步在自己服务内提交。
- 若某步失败，对已完成的步骤执行 **补偿事务（compensating transaction）** 撤销——但补偿不是回滚：邮件发不出去不能"撤回"，只能退款 / 标记人工。
- **可补偿 / pivot（不归点）/ 可重试** 三类步骤：pivot 之后不再可补偿，之后步骤须幂等可重试。

## 三、两种协调

| 方式 | 机制 | 取舍 |
|---|---|---|
| Orchestration 编排 | 中心协调器发命令、记状态、失败时跑补偿 | 复杂/多步/严格顺序首选；协调器须高可用 + 崩溃可恢复 |
| Choreography 合唱 | 服务间事件自发反应 | 短流程/事件边界清晰；难可视化、易事件环 |

经验法则：≥3–5 步、需严格顺序或显式补偿 → 编排；短流程 → 合唱。持久化协调状态（每步 STARTED/COMPLETED）是"可恢复工作流"与"内存脚本"的分界。

## 四、幂等（Idempotency）—— 不可协商

每步与每次补偿都会被重试（网络失败、协调器重启）。每个命令边界须带 **幂等键**（如 `sagaId:stepName`），首结果持久化，重复到达只返回原结果。消费者确认重复前先确认原结果。保护重试 / 重投 / 协调器故障转移。

## 五、断点续跑（Checkpoint / Resume）

- 持久化当前步、尝试次数、correlationId、补偿状态，崩溃后 worker 能恢复而不猜"发生了什么"。
- 不可逆步骤放最后；向客户端暴露 PENDING_COMPENSATION；耗尽失败进复核队列。

## 六、有界重试 + 抖动 + 死信 + 超时

- 重试须 **有界**（次数上限）+ **抖动**（避免惊群）；指数退避。
- **死信队列（DLQ）**：耗尽重试的工作持久化到可复核队列，暴露"可恢复状态"而非谎称成功。
- **超时**：每步独立超时（扣款快、发货慢），挂起 saga 须有路径重试或补偿 + 告警。

## 七、与本仓 EI 工具集成

- **EDG 步骤 ↔ Saga 步骤**：`execution_intelligence.py compile` 产出的 EDG 每步即一个 Saga step；每步加幂等键（edg_hash + step 名）。
- **补偿入口**：EDG 步若失败，CCS `certify` 已写证书——扩展为同时记录"补偿入口"（补偿命令 + 状态），崩溃后按证书续跑。
- **run 保守执行器**：当前 `run` 默认 dry-run、命令白名单；可靠性层在其上叠加重试/超时/DLQ，高风险 `--apply` 仍须 HITL（接 SI/Guard）。
- **已知缺口（诚实标注）**：当前 `run --apply` 子进程非 UTF-8 输出会触发 UnicodeDecodeError（见 EI 试运行记录），修复前长任务续跑的 evidence 截断风险存在；本技能不掩盖该缺口。

## 八、适用判定

- **用 Saga**：单一业务操作要更新多个"各自拥有数据"的服务，且要一致性又不要分布式锁（下单 / 支付 / 预订 / 开通）。
- **不用**：操作落在单一服务库内 → 本地 ACID 事务即可；若疯狂写 8 步跨 6 服务的 saga → 设计异味，数据本该在一起。

## 九、来源（2026-11-07 实拉）

- learn.microsoft.com/en-us/azure/architecture/reference-architectures/saga/saga（Azure Saga 模式：可补偿 / pivot / 可重试）
- microservices.io/patterns/data/saga.html（Saga 模式原文：编排 vs 合唱、补偿）
- adevguide.com/backend/distributed-systems/saga-pattern（编排 / 合唱 / 补偿 / 幂等、可靠实现）
- theaugmenteddev.com/blog/saga-pattern-distributed-transactions-microservices（持久化状态 / 幂等 / 超时、何时用）

## 十、重试预算计价、层数相乘与超时取值方法论（r739A 实拉 · 2026-11-14）

> 本节是 §六「有界重试 + 抖动 + 死信 + 超时」的**元层加厚**：§六给的是「要有界」的动作清单，本节给「界从哪来、按什么计价、在哪一层生效」。与 `engineering/execution-intelligence` §十一（写操作三态 / 对账先于重试 / effect class）分工：那条管「这次结果能不能判、判不了怎么办」，本条管「判得了之后重试总量怎么算」。豆包自留地已学退避参数模板与限流预算三层，本节不搬参数、只取未学的计价与取值语义。

### 10.1 重试预算是「按错误类型计价 + 成功回补」的独立机制，不是请求限流
AWS SDK standard 模式官方逐字：token budget 容量 **500 tokens**；每次 **transient（非限流）重试扣 14**、**throttling 重试扣 5**；重试成功只退还**该次**的成本，首次请求成功回补 **1 token**；预算耗尽时「the SDK stops retrying and returns errors directly to your code」。三条常被漏掉的语义：
- **配额永不延迟首次请求**（「The retry quota never delays or blocks the initial request. Only retries are affected.」）——它是重试闸门，不是准入闸门。
- **成功只补本次**：若第一次重试失败、第二次成功，净亏 14 tokens（不是全部退还），所以「多次重试才成功」也会缓慢消耗预算；耗尽最快的是「重试全失败」。
- **作用域是单个 SDK client 实例**（「typically scoped to a single SDK client instance ... It is not shared across processes or hosts」）——多进程/多机部署不能靠它做全局背压。

判据：**次数上限管单次调用，预算管整个客户端在故障期的放大倍数**，两者必须同时写。只写 `max_attempts=3` 不等于限制了重试风暴；验收要报出「预算容量 / 每类错误单价 / 耗尽后的行为 / 作用域」，并机检默认 3 次尝试下持续 transient 失败 >约 **22%**、throttling >约 **32%** 才开始净流失（低于此值成功回补快于消耗，预算看起来「没生效」）。把 token bucket 当成限流器复用会读反方向：限流器削的是正常流量，重试预算削的是「已经失败的那部分流量」。

### 10.2 多层重试按乘法放大，只在栈的一层重试
AWS Builders' Library 原文算例：五层调用栈、每层各重试 3 次，最底层数据库承受 **243x**（3→9→27→81→243）；因此「In general, for low-cost control-plane and data-plane operations, our best practice is to **retry at a single point in the stack**」。同篇另给两个反直觉点：**capped exponential backoff 会让所有客户端在封顶速率上持续重试**（封顶解决了「等多久」，没解决「还在打」）；circuit breaker 虽被广泛推荐，但「introduce modal behavior into systems that can be difficult to test, and can introduce significant addition time to recovery」，AWS 的替代做法是本地 token bucket 限重试。

判据：编排链路上每加一层重试，放大是**乘积不是和**。验收动作固定为画一张「调用栈 × 重试层」图并机检只有一层挂了重试策略；Agent 场景尤其要查 SDK 内置重试 + 应用 handler 重试 + 编排器重试三处叠加（同一请求被三处各重试 3 次即 27x）。不要在每一层都「顺手加个 retry」，也不要靠熔断开关去补一个本该由单层重试解决的结构问题。

### 10.3 超时值由「可接受的假超时率」反推分位数；per-attempt timeout ≠ 整体 deadline
- **取值方法论**（AWS 官方逐字）：「we choose an acceptable rate of false timeouts (such as 0.1%). Then, we look at the corresponding latency percentile on the downstream service (p99.9 in this example)」——超时不是拍脑袋常数，是先认领一个误判率再查分位；且该值「has to fit within the caller's own deadline」。两处已知不适用：跨公网客户端网络时延大、p99.9 与 p50 过于接近的紧时延服务。
- **计时覆盖范围**：官方部署案例——20ms 超时在部署后集中触发，原因是计时器包含了新建 TLS 连接；另有「implementations where the timeout doesn't cover all remote calls, like DNS or TLS handshakes」。故验收必须写清「什么被计时覆盖」，不能只报一个数字。
- **服务端定向延迟**：`x-amz-retry-after` 存在时 SDK 采用服务端给定值，但被钳制在「minimum of the computed backoff delay and a maximum of the computed backoff delay plus 5,000 ms」，且「**The SDK does not apply jitter to this value, because the service is expected to jitter it**」——客户端与服务端各加一次抖动是错的，前提是服务端已加；若下游是自研服务未加抖动，此处必须自行补。
- **四模式的依赖链**（kondevs 2026-10-29 独立一手）：timeouts → retries → idempotency → DLQ「form a dependency chain. Skip one and the next one breaks」；DLQ 最低可运行集是监控告警 / 明确归属 / 留存策略 / **经测试且可安全重放的 redrive**（无幂等的 redrive 会制造新问题）。超时创建的是第三态 `unknown outcome`（r734C 已定三态），不是二值失败。

判据：规格里同时写「per-attempt timeout / 端到端 deadline / 假超时率与对应分位 / 服务端 retry-after 的钳制区间与抖动归属」；只写「timeout=5s」视为未定义。SLO 应报 first-attempt success rate、eventual success rate、DLQ age，而不是单一 uptime——重试会把降级体验掩盖成「最终成功」。

**来源（r739A 独立实拉 2026-11-14，≥2 独立域交叉）**：
- `docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html`（AWS SDK 官方，WebFetch 200 全文逐字；含 500/14/5/22%/32%/20s 上限/x-amz-retry-after 钳制）
- `aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/`（AWS Builders' Library，Marc Brooker 2019-12-05，WebFetch 200 全文逐字；243x、single point in the stack、false timeout 0.1%→p99.9、jitter 于定时任务用同主机一致性方法）
- `www.kondevs.com/content-hub/reliability-patterns-timeouts-retries-idempotency-dlqs`（2026-10-29 独立一手全文逐字；unknown outcome、total deadline、DLQ 四要素与依赖链）
- `sre.google/sre-book/handling-overload/`（Google SRE，**WebFetch fetch failed，如实登记不冒充一手全文**；其 10% client retry budget 口径仅见于 aitechmodel.com 搜索快照，未采信为本轮结论）
- 商业/社区立场登记：`lumigo.io`（AWS 文章摘要）、`aitechmodel.com`（护栏清单）、`learnagent.wiki`（重试卡）仅作定位与交叉，未作结论来源。
