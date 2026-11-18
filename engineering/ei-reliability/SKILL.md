---
name: ei-reliability
description: 执行可靠性工程（Execution Intelligence · Reliability）。当任务涉及长流程、多步骤、可失败/可重试的写操作、跨系统动作、需要崩溃续跑或补偿回滚时调用。提供 Saga 编排、补偿事务、幂等键、断点续跑（持久化步骤状态）、有界重试+抖动、死信队列、超时。与 execution_intelligence.py 互补：本技能管"失败后怎么不丢状态、能续、能回"，EI 管"规划/门禁/证书"。 触发：分布式锁安全性、fencing token、租约过期。
module: EI
modules: EI,VI
version: 1.6.0
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


## 十一、双写不可原子与事务发件箱：at-least-once 的完整边界（r743B 实拉 · 2026-11-14，3 独点）

> 与 §十（重试预算/超时链）分工：§十管**瞬时故障**的放大与取值；本节管**结构性缺口**——两次写入不共享事务时，任何重试次数都补不了。与 `execution-intelligence` §十一（写操作三态/effect class/幂等键）分工：那条管单次写操作的契约，本节管「本地库 + 消息代理」这条发布链。

### 11.1（r743B-1）双写的四种排列全有崩溃窗口，重试补不了
- **原文**：microservices.io 官方 Pattern: Transactional outbox 逐字「The command must **atomically** update the database and send messages ... However, **it is not viable to use a traditional distributed transaction (2PC) that spans the database and the message broker**. The database and/or the message broker might not support 2PC」；「sending a message **in the middle of a transaction is not reliable. There's no guarantee that the transaction will commit**」「if a service sends a message **after committing the transaction** there's no guarantee that it won't crash before sending the message」。exashard 逐字「**There is no ordering of two independent writes that is safe.** This is the dual-write problem, and **it is not solvable by being careful. It is solvable only by making the two writes into one write**」；「**Retries fix transient broker failures. They cannot fix a crash in the gap between two systems, because the intent to publish was only ever held in memory.**」。
- **判据**：① 规格先画「两次写入的四种顺序 × 崩溃点」表：先发后写（宣布可能回滚的变更）/ 先写后发（崩溃丢事件）/ 事务中发（事务可能不提交）/ 2PC（组件不支持或耦合）。② 遇到不一致，禁止把「加一层重试」当修复——重试只覆盖 broker 瞬时故障，崩溃时重试循环本身已不存在。③ 正解是把事件写入业务数据的**同一个本地事务**（outbox 表），由独立 relay 发布；2PC 仅在明确支持且接受耦合时才列为候选，不默认。

### 11.2（r743B-2）outbox 保证的是 at-least-once，重复窗口不能靠换顺序关掉
- **原文**：microservices.io 官方 Result context 逐字「**The Message relay might publish a message more than once.** It might, for example, **crash after publishing a message but before recording the fact that it has done so**. When it restarts, it will then publish the message again. **As a result, a message consumer must be idempotent**, perhaps by tracking the IDs of the messages that it has already processed」。exashard 逐字「**You cannot close that gap by reordering, either: mark the row published first and a crash before the publish loses the event entirely, which is worse. Any two-system operation has this property, which is exactly the dual-write problem reappearing one layer down**」；「**The outbox and idempotent consumers are one design, not two**」；「It gives **at-least-once, not exactly-once**. Consumers must be idempotent by event ID」。
- **判据**：① 规格把「有效一次」写成公式：**at-least-once 投递 + 消费侧按稳定 event ID 去重**，两半是一个设计，缺一不得写「恰好一次」。② 稳定 event ID 随事件发布，消费端把已处理 ID 与本地状态变更放进**同一本地事务**（inbox 表）；内存态去重在重启后失效。③ relay 的「发布→标记」两步本身是又一处双写，禁止用「先标记后发布」交换顺序来掩盖（会变成丢事件）。④ 与 §十一（execution-intelligence）的 effect class / point of no return 合用：不可逆副作用排最后，且必须能承受重复投递。

### 11.3（r743B-3）豁免要两条件同时成立，替代方案各有明码代价
- **原文**：exashard 逐字唯一豁免 ephemeral presence telemetry 两条件 **AND**：「The producing service **holds no database state** that the event needs to be consistent with ... There is no dual write here, because there is **no first write**」「The stream is **loss-tolerant**」；「**If only the first condition holds, you still want durability. If only the second holds, you still have a dual write that can announce a rolled-back change.** Both together, and the outbox is pure overhead」。六方案对比逐字：publish then write「Announces changes that may roll back; corrupts consumers」/ write then publish「Loses events on crash; no record that an event was owed」/ 2PC「Poor performance, poor broker support, **blocking on coordinator failure**」/ event sourcing「Solves it completely, but **re-architects your whole persistence model**」/ CDC without an outbox「**Leaks your internal schema as your public event contract**」，且「**If you use CDC, point it at the outbox table, not at your domain tables**」。microservices.io 官方 drawback 逐字「**Potentially error prone since the developer might forget to publish the message/event after updating the database**」。sourcegarden 逐字「a high-write outbox table accumulates dead rows fast ... bloat and vacuum pressure. **The outbox needs pruning and monitoring like any hot table**」。
- **判据**：① 豁免须两条件同时成立并书面登记，只满足其一仍走 outbox；业务事件（注册/支付/订阅变更）自动不满足第二条。② 选型表逐条写失败模式，不写「性能更好/更简单」这种无边界结论；relay 在 polling（运维简单、有轮询延迟）与 CDC（低延迟、多一套基础设施）之间按延迟与运维成本定。③ outbox 表要有清理与监控策略，把它当队列表而非业务表。④ 官方 drawback 落到验收：业务写入与 outbox 插入必须封装在同一入口，防「忘记插事件」。

**来源（r743B 独立实拉 2026-11-14，≥2 独立域交叉）**：
- `microservices.io/patterns/data/transactional-outbox.html`（Chris Richardson 官方 pattern 页，WebFetch 200 全文逐字：2PC 不可行、三种 forces、Solution 四参与者、relay 重复与 idempotent consumer、Polling/Transaction log tailing 两实现、官方 drawback）
- `exashard.com/posts/transactional-outbox-pattern`（2026-07-31 独立一手全文逐字：四种排列、重试无效、at-least-once not exactly-once、重排无解、豁免两条件、六方案对比表、CDC 只指 outbox 表）
- `sourcegarden.com/blog/the-dual-write-problem`（独立一手全文逐字：relay 崩溃窗口、outbox 表 bloat/vacuum、CDC vs polling 选型）；`penluma.com/blog/system-design/11-distributed-transactions-and-idempotency`（独立一手：三档交付语义、idempotency key scope 到 operation 不是 record、check-then-act 竞态）；`codetoclarity.in`（独立一手：Transactional Inbox 模式与 OOM 崩溃时序）
- 立场登记：`systemweakness.com`（社区长文，仅作 at-least-once 口径交叉）、`qaskills.sh` 无关不采。作者个人平台纪律（「every producer writes through a transactional outbox」）为经验立场，登记不作规范结论。

## 十二、截止时间与取消信号沿调用链传播（r749B 独立实拉 2026-11-15）

> 与 §十（r739A 重试预算/多层重试/超时取值）分工：那条管**瞬时故障的放大与取值**；本节管**总预算与取消信号是否真的传到每一跳、派生工作是否真的停下**。与 §十一（r743B 双写/outbox）分工：那条管崩溃窗口的结构性缺口。三者互补不重述。

### 12.1（r749B-1）deadline 是绝对时间点不是时长；默认不设 = 可能永远等，且「收到超时码」不等于「工作停了」
- **原文**：gRPC 官方《Deadlines》逐字「A **deadline** is used to specify **a point in time past which a client is unwilling to wait** ... A **timeout** is the max duration of time that the call can take. A timeout can be converted to a deadline by adding the timeout to the current time」「**By default, gRPC does not set a deadline** which means it is possible for a client to end up waiting for a response **effectively forever**」「the client will give up and fail the RPC with the **`DEADLINE_EXCEEDED` status**」；服务端侧逐字「A gRPC server deals with this situation by **automatically cancelling a call (`CANCELLED` status)** once a deadline set by the client has passed」「**the server application is responsible for stopping any activity it has spawned** to service the RPC. If your application is running a long-running process you should **periodically check if the RPC that initiated it has been cancelled** and if so, stop the processing」。Microsoft Learn（ASP.NET Core 9.0）逐字「**There is no default deadline value. gRPC calls aren't time limited unless a deadline is specified**」「The client immediately aborts the underlying HTTP request and throws a `DeadlineExceeded` error」「On the server, the executing HTTP request is aborted and `ServerCallContext.CancellationToken` is raised. **Although the HTTP request is aborted, the gRPC call continues to run on the server until the method completes.** It's important that **the cancellation token is passed to async methods** so they are cancelled along with the call ... **Passing a cancellation token allows the canceled call to complete quickly on the server and free up resources**」。官方示例（C++/Go/Java）逐字 `context->IsCancelled()` / `ctx.Err() == context.Canceled` / `Context.current().isCancelled()`。
- **判据**：① 规格里**同时写**「入口绝对 deadline」与「每跳 timeout」，并注明二者换算点；**禁止所有下游各自拍一个 timeout** 而入口无总预算。② 客户端 `DEADLINE_EXCEEDED` 与服务端 `CANCELLED` 是**两侧不同行为**，验收断言必须落到「**派生工作/子查询/后台任务是否停止**」，不是「调用方是否拿到了超时错误码」；HTTP 请求中止但方法继续跑是官方明示的正常现象。③ 长任务在**昂贵计算之前**先查取消（`IsCancelled` / `ctx.Err()`），运行中周期性查；每个异步 DB/HTTP 调用都要接 `CancellationToken`。④ 收尾清理若必须在取消后继续，须用 `context.WithoutCancel`（见 12.3）显式脱离并写明，否则超时连清理一起砍掉。

### 12.2（r749B-2）传播要传「扣掉已耗时的 timeout」，不是原样传绝对时间点；按语言分叉且取最小 deadline
- **原文**：gRPC 官方逐字「Automatically propagating the deadline from an incoming RPC to an outgoing one is **supported by some gRPC implementations**. In some languages this behavior **needs to be explicitly enabled (e.g. C++)** and in others it is **enabled by default (e.g. Java and Go)**」「**Since a deadline is set point in time, propagating it as-is to a server can be problematic as the clocks on the two servers might not be synchronized. To address this gRPC converts the deadline to a timeout from which the already elapsed time is already deducted. This shields your system from any clock skew issues.**」；官方时序算例 `Request at 13:00:00` / `Should complete in 2s` / `GetUserProfile(deadline: 13:00:02)` / `0.5s spent before calling billing server` / `GetTransactionHistory(timeout: 1.5s)`。Microsoft Learn 逐字「**Manually propagating deadlines can be cumbersome. The deadline needs to be passed to every call, and it's easy to accidentally miss**」「`EnableCallContextPropagation()`: **Automatically propagates the deadline and cancellation token to child calls** / **Doesn't propagate the deadline if the child call specifies a smaller deadline** ... **When multiple deadlines are available, the smallest deadline is used**」「the deadline **tracks time across all retries** for a gRPC call. If the deadline is exceeded ... **skips any remaining retries**」；`ServerCallContext.Deadline` 手动传播示例逐字。中文官方镜像（grpc.org.cn / grpc.programming.tw）同口径逐字核验。
- **判据**：① **跨主机禁止原样传绝对时间点**（时钟未同步）；传「剩余时长」= 入口 deadline − 已耗时，官方算例即 2s−0.5s=1.5s。② 规格固定四栏（入口总预算 / 每跳已耗时 / 该跳剩余预算 / 子预算 < 父剩余），**总预算在入口一次设定**；子预算取 `min(父剩余, 本跳自定义)`，且**重试共用同一条 deadline**、超限跳过剩余重试（与 §10.1 重试预算 token bucket 是两条独立机制，别互相顶替）。③ **自动传播不是全域默认**：C++ 需显式启用、Java/Go 默认、.NET 需 `EnableCallContextPropagation()`；换语言/换客户端工厂时必须重新验证，禁止把「框架会传播」当无条件事实。④ 手工逐跳传播易漏，验收用「调用栈 × 每跳 deadline」表逐行核对，漏一跳即该跳可能无限等。

### 12.3（r749B-3）Context 是取消树，取消原因可归因；Cancel 与 DeadlineExceeded 是两类错误，收尾要显式脱离
- **原文**：Go 官方 `context` 包文档（go1.27.3）逐字「Package context defines the Context type, which **carries deadlines, cancellation signals, and other request-scoped values across API boundaries and between processes**」「**Incoming requests to a server should create a Context, and outgoing calls to servers should accept a Context. The chain of function calls between them must propagate the Context**」「**When a Context is canceled, all Contexts derived from it are also canceled**」「**Failing to call the CancelFunc leaks the child and its children until the parent is canceled. The go vet tool checks that CancelFuncs are used on all control-flow paths**」；规则逐字「**Do not store Contexts inside a struct type**; instead, pass a Context explicitly to each function that needs it」「**The Context should be the first parameter, typically named ctx**」「**Do not pass a nil Context** ... Pass `context.TODO`」「Use context Values **only for request-scoped data** that transits processes and APIs, **not for passing optional parameters**」。两错误逐字「`Canceled` is the error returned by Context.Err when the context is canceled **for some reason other than its deadline passing**」「`DeadlineExceeded` ... **due to its deadline passing**」；`Cause` 逐字「**The first cancellation of c or one of its parents sets the cause**」「if parentContext is canceled with cause1 before childContext is canceled with cause2, then Cause(parentContext) == Cause(childContext) == cause1」「if childContext is canceled with cause2 before parentContext is canceled with cause1, then Cause(parentContext) == cause1 and Cause(childContext) == cause2」；`WithoutCancel` 逐字「returns a derived context ... **is not canceled when parent is canceled**. The returned context **returns no Deadline or Err, and its Done channel is nil**」。17golang 教学逐字「**取消不是错误噪音**：`context.Canceled` 和 `DeadlineExceeded` 应该被统计，但不一定都算业务错误」「**用户主动断开、上游超时和本服务处理超时要区别分析**」「日志里保留 request id、deadline、依赖名和剩余耗时」。
- **判据**：① **取消是树不是布尔标志**：入口一次取消，所有派生 context 同步取消；长流程规格画「取消树」并标每跳是否接入 ctx，禁止把 context 塞进 struct 或当可选参数包传。② **`CancelFunc` 每条控制流路径都要调用**（go vet 可机检），否则子 context 与定时器泄漏到父取消为止；这是资源泄漏不是功能 bug。③ **`Canceled` ≠ `DeadlineExceeded`**：分别计数、分别归因（用户主动断开 / 上游超时 / 本服务超时），禁止把用户取消当服务端错误报警，也禁止把两者合并成单一「失败率」。④ 需要**归因原因**用 `WithCancelCause` / `WithDeadlineCause` + `Cause()`，并记住**首次取消定 cause**、父子各自取消时各保留自己的 cause。⑤ **收尾/清理动作必须显式选 `WithoutCancel` 并写明**：它不带 Deadline、不带 Err、Done 为 nil；否则超时后补偿、日志落盘、outbox 标记这类收尾会被父取消一并砍掉（与 §11.2 relay「发布→标记」崩溃窗口呼应）。

**来源（r749B 独立实拉 2026-11-15，≥2 独立域交叉）**：
- `https://grpc.io/docs/guides/deadlines`（gRPC 官方《Deadlines》；WebFetch 200 **全文逐字**：deadline vs timeout 换算、默认不设、DEADLINE_EXCEEDED、服务端自动 CANCELLED 与应用责任、传播按语言分叉、时钟偏移→扣已耗时的 timeout、13:00:00/2s/0.5s/1.5s 算例、Java/Go/C++/Python 示例链接。**第一独立域·官方一手**）
- `https://go.dev/pkg/context/`（Go 官方标准库文档 **go1.27.3**；WebFetch 200 **全文逐字**：跨 API 边界与跨进程、入站建/出站收/链条必须传播、父取消派生全取消、CancelFunc 泄漏与 go vet、Cause/WithCancelCause、Canceled vs DeadlineExceeded、四条形参规则、WithoutCancel 语义。**第二独立域·官方一手**）
- `https://learn.microsoft.com/en-us/aspnet/core/grpc/deadlines-cancellation?view=aspnetcore-9.0`（Microsoft Learn；WebFetch 200 **全文逐字**：无默认 deadline、两侧行为差异、HTTP 中止但方法继续跑、CancellationToken 传入异步调用、deadline 跨所有重试累计且超限跳过剩余重试、`EnableCallContextPropagation()` 自动传播与最小 deadline 规则、`ServerCallContext.Deadline` 手动传播示例。**第三独立域·官方一手**；页面自带「This isn't the latest version ... .NET 10 version」提示，**如实登记按 9.0 归档版引用**）
- `https://golang.org/src/context/context.go?s=2460:6019`（官方源码逐字）· `http://godocs.io/context@v1.7.0-beta.1` + `https://golang-org.appspot.com/tip.golang.org/pkg/context`（旧版/镜像双版本语义交叉，逐字：「CancelFunc does not wait for the work to stop」「adjusted to be no later than d」）· `https://grpc.org.cn/docs/guides/deadlines` + `https://grpc.org.cn/blog/deadlines` + `https://grpc.programming.tw/blog/deadlines/`（官方中文镜像三页，跨语言/版本口径一致）· `https://www.17golang.com/article/619791.html`（中文教学：入口总预算 SLO 反推、子预算 50/200/300ms、取消不是错误噪音、常见误区与日志字段）。**第四~六独立域·源码/版本化镜像/教学立场，逐条登记不作唯一结论来源**。
- **判非**：`DEADLINE_EXCEEDED` / `deadline propagation` / `CancelFunc` / `CancellationToken` / `clock skew` / `context.WithTimeout` / `截止时间传播` / `子预算` 全库 `SKILL.md` **0 命中**；`截止时间` 2 命中经查属 `meta/di-decision-tradeoff`（决策澄清里的成功标准截止时间）与 `engineering/wb-release-maintain`（服务停止日 vs 数据删除日），**均异命题**；模块 `EI/MEMORY.md` §10 重试预算/超时链、§11 双写与 outbox 亦为异命题、不复用。豆包自留地 **WB 0 落地**。
- **未采纳**：.NET Executor/线程池调优、gRPC retry policy 完整配置、具体超时毫秒数（SLO 反推只取结构）、`context.WithValue` 的键设计实现细节。


## 十三、扇出把尾部放大：对冲请求、绑定请求与取消预算（r753B 独立实拉 2026-11-15，≥2 独立域一手交叉，3 独点）

> 定位：本节管「**没失败但慢**」这一态。与 §十（重试预算按错误类型计价）、§十一（双写与 outbox 的崩溃窗口）、§十二（deadline 与取消树传播）分工：那三条管失败、状态一致性与截止时间；本节管一次成功请求里某个并行子调用拖尾，以及用冗余副本换尾部时的成本与反作用。**对冲不是重试**：重试发生在失败/超时之后，对冲发生在仍在途但超过分位阈值时；把两者混写会把「慢」修成「重复副作用」。

### 13.1（r753B-1）服务 p99 拼不出产品 p99；验收要按扇出度算联合分位
- **原文**：Dean & Barroso《The Tail at Scale》（**CACM 56(2):74–80, 2013-02-01**, DOI 10.1145/2408776.2408794）逐字「Variability in the latency distribution of individual components is **magnified at the service level**」「consider a system where each server typically responds in 10ms but with a **99th-percentile latency of one second**. If a user request is handled on just one such server, **one user request in 100 will be slow**」「If a user request must collect responses from **100 such servers in parallel, then 63% of user requests will take more than one second**」「Even for services with only **one in 10,000 requests** experiencing more than one-second latencies at the single-server level, a service with **2,000 such servers will see almost one in five** user requests taking more than one second」；变异来源逐字「**Shared resources** / **Daemons** / **Global resource sharing** / **Maintenance activities**（BigTable log compactions、garbage collection）/ **Queueing**」，硬件侧「**Power limits**」「SSD ... **increase read latency by a factor of 100**」「**Energy management**」。mlsysbook.ai《13 Model Serving》逐字「If sub-task completion events are independent and each has a **99 percent probability** of finishing within latency threshold, the probability that all N backends finish within the SLO is **(0.99)^N**」「For a fan-out of N=10, only **≈90.4%** of requests meet the target; at **N=100**, that probability drops to **≈36.6%**, meaning nearly two-thirds of user requests experience a tail delay」「**the overall user request completes only when the slowest sub-task finishes**」。
- **判据**：① **用户侧延迟是必需子调用的最大值，不是均值或各服务分位的拼接**：规格写「扇出度 N + 每跳分位 + 联合分位」，禁止用「每个服务 p99<50ms」推出「端到端 p99<50ms」。② **验收在边缘测**（网关/BFF/RUM），不在单个 shard 测；N 从 10 增到 100 时命中率从 90.4% 掉到 36.6% 是乘法效应，加机器不解决，减少必需扇出才是首选（缓存、批处理、可选项异步/降级）。③ **变异来源要逐类排查**：共享资源、后台守护、全局资源共享、维护活动（压实/GC）、多层排队、功耗/SSD GC/节能；把它们一律归为「网络抖动」会漏掉本地成因。④ 「prediction that arrives after the client has timed out has no value however accurate it is」（mlsysbook 逐字）⇒ 与 §十二 deadline 衔接：分位目标必须落在调用方 deadline 内，超出即等同失败。

### 13.2（r753B-2）hedged 与 tied 触发条件不同，且都只适用于幂等只读
- **原文**：CACM 逐字「**Hedged requests**. A simple way to curb latency variability is to issue the same request to multiple replicas and use the results from **whichever replica responds first**」「a client first sends one request to the replica believed to be the most appropriate, but then **falls back on sending a secondary request after some brief delay**. **The client cancels remaining outstanding requests once the first result is received**」「**defer sending a secondary request until the first request has been outstanding for more than the 95th-percentile expected latency** ... **limits the additional load to approximately 5%**」「in a Google benchmark that reads the values for **1,000 keys** stored in a BigTable table distributed across **100 different servers**, sending a hedging request after a **10ms delay** reduces the **99.9th-percentile latency ... from 1,800ms to 74ms while sending just 2% more requests**」「The overhead ... further reduced by **tagging them as lower priority than the primary requests**」；tied 逐字「**Tied requests** ... **enqueuing copies of a request in multiple servers simultaneously** and allowing the servers to **communicate updates on the status of these copies to each other**」「When a request begins execution, it **sends a cancellation message to its counterpart**」「**There is a brief window of one average network message delay where both servers may start executing**」「it is useful therefore for the client to introduce a **small delay of two times the average network message delay (1ms or less ...)** between sending the first request and sending the second」。mlsysbook 逐字「**Tied requests instead enter several server queues at once and cancel the other copies when one server begins processing, which avoids waiting to detect a slow response**」「**Both techniques create duplicate work**」「**Canary requests**, a different use of the word from the canary rollouts that shift traffic between model versions, apply the same idea to fan-out, sending the request first to one or two servers and **committing to the full fan-out only if they answer within the expected time**」。教学域交叉逐字「**Works for idempotent reads. Dangerous for non-idempotent writes**」「**Hedging writes. Double charge**」（pradeepbangalore.in）。
- **判据**：① **hedged = 阈值触发**（首请求超过 p95 期望时延才发副本，额外约 5% 负载）；**tied = 同时入队**（多个副本带彼此标识，谁先开工谁取消对方，省掉检测等待）。两者不是同一开关的两个名字，选型看主导延迟是排队还是执行本身。② **两发之间要错开 2×平均网络消息延迟**，否则空队列时双执行窗口会常态命中；官方给的 1ms 是当时数据中心量级，绑版本登记不写成固定值。③ **只用于幂等只读**：写操作对冲＝双扣/双发，与 §十一「补偿不是回滚、不抹历史」同向；规格必须标 effect class，`read/reversible` 才允许挂对冲。④ **败者必须显式取消**：CACM 明写「client cancels remaining outstanding requests once the first result is received」；不取消等于 2× 负载且尾部更差（教学域逐字「**No cancellation. Hedged twins both run to completion; you paid 2× for the privilege**」）。⑤ 副本标低优先级、canary 请求先探 1–2 台再决定是否全量扇出，是降低开销的可选手段；`canary request` ≠ `canary rollout`（§15.3 灰度发布），同名不同义须并列定义（同 Cap76 口径）。

### 13.3（r753B-3）取消时机决定成本、相关性决定成败；要显式写「重复工作预算」
- **原文**：mlsysbook 逐字「**Hedging: The term is borrowed from finance ... The insurance is not free**」「For ML systems, the losing hedged request **may still occupy accelerator time if inference has already launched, because ordinary GPU kernels are not cheaply canceled mid-execution**」「**a hedging policy must budget duplicate work as well as the latency benefit**」「**Cancellation before dispatch prevents a losing copy from consuming accelerator time, whereas cancellation after dispatch only discards its result, so either needs spare capacity and an explicit duplicate-work budget**」「With a stable latency distribution, a threshold at the historical 95th percentile duplicates about 5 percent of requests; **correlated slowdowns raise that fraction and can make hedging amplify overload instead of reducing the tail**」「Replicas or streams on one machine can also race requests, but **sharing an accelerator or memory bus can correlate their slowdowns and exhaust the same headroom**」「Latency SLOs are not enforced by fast inference alone; **they are enforced by headroom**」；CACM 逐字「**Although naive implementations of this technique typically add unacceptable additional load**, many variations exist that give most of the latency-reduction effects while increasing load only modestly」「The technique works because **the source of latency is often not inherent in the particular request but rather due to other forms of interference**」。教学域交叉逐字「**Hedging cannot fix correlation because the hedge target is correlated with the primary by construction; only architectural separation ... decorrelates**」「compute the i.i.d. prediction ... and the observed user-side tail ... **the gap is your correlation budget**」（learn.padho.ai，独立立场登记）。
- **判据**：① **规格固定四栏**：扇出度 / 分位阈值 / 重复工作预算（允许的最大额外负载）/ 取消点与取消可达性（before dispatch 才省算力，after dispatch 只丢结果）。② **对冲要吃余量**：不是「不增加机器」的免费优化，需要 spare capacity 与 headroom；在利用率贴顶时开对冲会把瞬时抖动放大成过载。③ **i.i.d. 假设必须声明**：共享依赖（同一 auth 服务、同 DNS 解析缓存、同加速器/内存总线、热键定向）会让各副本同时变慢，此时 `0.99^N` 的预测与实测尾部的差就是相关性预算；**正确动作是找并拆共享依赖，不是加更多对冲**。④ **与 §十分工**：重试预算按错误类型计价、管故障期放大倍数；本节预算按「慢而成功」计价、管尾部削减；两者可叠加但须分账，禁止把对冲副本计入重试次数或反之。⑤ 与 §十二分工：取消树保证一次取消沿链传播，本节要求**赢者返回时主动取消败者**，两个方向都要实现，且收尾日志仍按 §12.3 显式脱离父取消（WithoutCancel / 不继承 deadline）落盘，否则取消把证据一起砍掉。

**来源（r753B 独立实拉 2026-11-15，≥2 独立域一手交叉）**：
- `https://cacm.acm.org/research/the-tail-at-scale/`（Jeffrey Dean & Luiz André Barroso《The Tail at Scale》，**CACM Vol.56 No.2 pp.74–80, Posted Feb 1 2013**, DOI `10.1145/2408776.2408794`；WebFetch 200 **全文逐字**：变异五类来源 + 三类硬件趋势、100 台并行 63% 超 1 秒 / 2000 台万分之一异常近 1/5、hedged 定义与取消、p95 阈值约 +5%、BigTable 1000 keys/100 servers/10ms/1800ms→74ms/仅 +2% 请求、副本标低优先级、tied 定义与跨服状态更新、一个平均网络消息延迟的双执行窗口、错开 2× 平均网络延迟、低实现额外负载警告。**第一独立域·原论文一手**）
- `https://mlsysbook.ai/vol1/13_model_serving/13_model_serving.html`（《Machine Learning Systems》Vol.1 Ch.13 Model Serving；**curl 200 / 980,966 B 全文落盘后逐字提取**，WebFetch 因 99,537 字 AI 摘要 60s 超时仅返回前 15,000 字，**如实登记并以 curl 全文为准**：`(0.99)^N`、N=10→90.4% / N=100→36.6%、最慢子任务决定完成、serving inversion 与 headroom、The insurance is not free、GPU kernel 不可廉价中途取消、cancellation before/after dispatch、explicit duplicate-work budget、相关减速放大过载、canary requests 与 canary rollouts 区分、同机共享加速器/内存总线相关性、SLO 由 headroom 保障。**第二独立域·大学教材一手**）
- `https://system-design-in-depth.vedgupta.in/topic/tail-latency`（快照逐字：0.99^100=36.6%、p95 阈值、1800ms→74ms/+2%、tied 同时入双队列、coordinated omission 与 wrk2/HdrHistogram）· `https://www.pradeepbangalore.in/post/tail-at-scale`（快照逐字：fan-out tax、**Works for idempotent reads. Dangerous for non-idempotent writes**、No cancellation 付 2×、cells/bulkheads、Little's Law、90% 利用率尾部恶化）· `https://learn.padho.ai/wiki/the-tail-at-scale-dean-barroso`（快照逐字：i.i.d. 预测 vs 实测的 correlation budget、共享依赖才是对冲失效根因、排队主导选 tied / 执行主导选 hedging、容量经济学）· `https://www.javacodegeeks.com/?p=144918/`（快照逐字：hedged ≈2–5% / tied ≈10% 额外负载、Bigtable 数值复述）。**第三~六独立域·教学/技术站立场，逐条登记、不作唯一结论来源**；其中案例化数值（PaisaBridge 22 调用 280ms→1.4s、45%/10% 一类厂商样本）**未采纳为通用工程事实**。
- **判非**：`hedged request` / `tied request` / `duplicate-work` / `取消前` / `对冲请求` / `Tail at Scale` / `bulkhead` / `load shedding` 全库 `SKILL.md` **0 命中**；`fan-out` 8 命中经查均属 agent 编排/并行委派（**异命题**）、`p95` 5 命中属各技能性能读数（异命题）、`重复工作` 3 命中属执行去重与技能编写（异命题）、`尾部延迟` 1 命中在豆包自留地 `defaults/wb-context-compressor`（口号级，本轮取机制层，按「合」登记不重述）。模块 `EI/MEMORY.md` §10 重试预算/超时链、§11 双写与 outbox、§12 deadline/取消树均为异命题、不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：GPU 调度/批处理窗口调优、Little's Law 容量推导、coordinated omission 压测工具细节、具体毫秒阈值（只取结构）、canary rollout 部署流程、hedging 的产品化配置语法。

## 十四、分布式锁的正确性边界：租约、进程暂停与 fencing token（r757B 独立实拉 2026-11-16，≥2 独立域一手交叉，3 独点）

> 定位：本节管「**拿到锁之后，还能不能安全地写共享资源**」。与 §十（重试预算计价）、§十一（双写与事务发件箱 at-least-once）、§十二（deadline 与取消树）、§十三（扇出尾部与对冲请求）分工：那四条管**失败后不丢状态、能续、能回**与**慢而成功**；本节管**互斥本身在什么条件下根本不成立**。§十三的 hedged/tied 只适用幂等只读，本节说明「写」为什么需要资源侧的第二道门。

### 14.1（r757B-1）先问「锁失效会怎样」：效率锁与正确性锁是两个问题；带 TTL 的锁在进程暂停面前没有互斥
- **原文**（Martin Kleppmann《How to do distributed locking》，**Published 08 Feb 2016**，一手 WebFetch 200，AI 摘要 60s 超时 ⇒ 返回前 15,000 / 29,464 字原文逐字，如实登记）：「At a high level, there are two reasons why you might want a lock in a distributed application: **for efficiency or for correctness**」·「**Efficiency:** …the result is a minor increase in cost…or a minor inconvenience」·「**Correctness:** …the result is a corrupted file, data loss, permanent inconsistency, **the wrong dose of a drug administered to a patient**」·「You need to be very clear about which one of the two you are dealing with」·「The client that acquired the lock is **paused for an extended period of time while holding the lock** – for example because the garbage collector (GC) kicked in. The lock has a timeout (i.e. it is a **lease**)…if the GC pause lasts longer than the lease expiry period, and the client doesn't realise that it has expired, it may go ahead and make some unsafe change」·「This bug is not theoretical: **HBase used to have this problem**」·「"stop-the-world" GC pauses have sometimes been known to last for **several minutes**」·「in a famous incident at GitHub, packets were **delayed in the network for approximately 90 seconds**」·「**You cannot fix this problem by inserting a check on the lock expiry just before writing back to storage. Remember that GC can pause a running thread at *any point***, including the point that is maximally inconvenient for you (between the last check and the write operation)」·「You simply cannot make any assumptions about timing, which is why the code above is fundamentally unsafe, **no matter what lock service you use**」。
- **判据**：① 声明锁用途是**第一动作**：效率锁（避免重复算/重复发信）单实例即可，崩溃丢锁可接受；正确性锁失效即数据损坏 ⇒ 不能靠「多部署几个节点」升级，Redlock 的 5 节点多数只是看起来像正确性方案。② **自动释放（lease/TTL）是 liveness 必需，但正是它打开了互斥漏洞**：暂停原因不止 GC——页错误、EBS 同步网络读、CPU 争抢、SIGSTOP、网络包延迟 90 秒，任何一处都能让旧持有者在租约过期后回来写。③ 「写之前再查一次锁过期」是**无效修复**：暂停可以落在检查与写之间的任意点；任何客户端侧的时序检查都不构成互斥证据。④ 与 §十二分工：deadline/取消树保证「一次取消沿链传播」，本节说明即使取消正确，一个**已经发出的写请求**仍可能在租约过期后抵达存储，取消树管不到它。

### 14.2（r757B-2）fencing token 是资源侧的第二道门，不是锁服务的附加字段；Redlock 没有它
- **原文**（同上 Kleppmann 全文逐字）：「**The fix for this problem is actually pretty simple: you need to include a *fencing token* with every write request to the storage service. In this context, a fencing token is simply a number that increases (e.g. incremented by the lock service) every time a client acquires the lock**」·「Client 1 acquires the lease and gets a token of **33**…Client 2 acquires the lease, gets a token of **34**…the storage server remembers that it has already processed a write with a higher token number (34), and so it **rejects the request with token 33**」·「**this requires the storage server to take an active role in checking tokens, and rejecting any writes on which the token has gone backwards**」·「if you are using ZooKeeper as lock service, you can use the **`zxid` or the znode version number** as fencing token」·「**Redlock…does not have any facility for generating fencing tokens**…The unique random value it uses does not provide the required monotonicity. Simply keeping a counter on one Redis node would not be sufficient, because that node may fail. Keeping counters on several nodes would mean they would go out of sync. It's likely that you would need a **consensus algorithm just to generate the fencing tokens**」·时间面：「**the algorithms make no assumptions about timing**…The only purpose for which algorithms may use clocks is to **generate timeouts**…timeouts are just a **guess** that something is wrong」·「Redis **uses `gettimeofday`, not a monotonic clock**, to determine the expiry of keys…subject to discontinuous jumps in system time – that is, it might suddenly jump forwards by a few minutes, or even jump back in time (e.g. if the clock is stepped by NTP)」。
- **判据**：① 互斥的**最终裁定权在被保护资源**，不在锁服务：资源必须记住已见最大 token 并拒绝回退写，只把 token 挂在请求上而资源不校验 = 没做。② token 必须**严格单调**：随机唯一值不能替代（不可比较大小）；单节点计数器会随节点故障回退，多节点计数器会不同步 ⇒ 生成 token 本身是共识问题， ZooKeeper 的 zxid / znode version 是现成解。③ 报告固定四栏：锁用途（效率/正确性）/ token 来源（哪个单调量）/ 资源侧是否实现回退拒绝 / 暂停窗口与租约时长的关系；缺第三栏不得写「并发安全」。④ 时钟只准做超时猜测，不准做正确性依据；用非单调时钟算 key 过期，NTP step 会让锁提前失效。⑤ 与 §十一分工：outbox 保证「消息至少发一次 + 消费侧幂等」，本节保证「同一时刻只有一个写者被资源接受」；两者可叠加，但幂等键不能当 fencing token（幂等去重复，不拒绝旧持有者）。

### 14.3（r757B-3）论战的正确抽象：资源侧有没有第二条控制，决定锁是不是必需
- **原文**（Salvatore Sanfilippo / antirez《Is Redlock safe?》，一手 WebFetch 200 全文逐字，与 Kleppmann **立场对立、双方逐字并陈**）：「**Martin's analysis of the algorithm concludes that Redlock is not safe**…However I don't agree with the analysis」·「A distributed lock without an auto release mechanism…is basically useless…a **liveness issue**」·「**If your data store can always accept the write only if your token is greater than all the past tokens, than it's a linearizable store. If you have a linearizable store, you can just generate an incremental ID for each Redlock acquired**」·「**most of the times the result of working to a shared resource is not writing to a linearizable store**…Sometimes we use distributed locks to move physical objects…Or to interact with another external API」·「Each Redlock is associated with a **large random token**（…"**20 bytes from /dev/urandom**"）…you can implement **Check and Set**. When starting to work with a shared resource, we set its state to "`<token>`", then we operate the read-modify-write only if the token is still the same when we write」·「for the same GC pauses Martin mentions, **the order in which the token was acquired, does not necessarily respects the order in which the clients will attempt to work on the shared resource**, so the lock order may not be casually related to the effects」·半同步模型自辩「Redlock assumes a **semi synchronous system model** where different processes can count time at more or less the same "speed"…to be able to count 5 seconds with a maximum of 10% error」。Kleppmann 侧逐字：「**Redlock is not like this. Its safety depends on a lot of timing assumptions**: it assumes that all Redis nodes hold keys for approximately the right length of time before expiring; that the network delay is small compared to the expiry duration; and that process pauses are much shorter than the expiry duration」。
- **判据**：① 双方**都同意**带自动释放的锁在暂停后可能双写，分歧在「谁该负责修」——Kleppmann 要锁服务提供单调 token，antirez 要资源侧自己用 CAS/唯一值兜住 ⇒ 落地时不要站队，改问一句：**被保护资源能不能参与校验？** 能（可线性化存储）则用 token/CAS 把互斥放在资源侧；不能（普通文件、任意 REST API、物理设备）则**锁只保效率，正确性无解**，必须换共识服务或改造资源。② antirez 的「有可线性化存储就不需要锁」是**真判据不是诡辩**：它把「锁」从正确性面降级为效率面，与 14.1 的二分自洽。③ 「有序 token 并非处处必要」：CAS 用唯一随机值也能挡旧写；但**获取顺序 ≠ 作用顺序**（GC 打乱因果），凡按 token 顺序做审计/回放的设计须显式登记这一限制。④ 时序假设必须**逐条列明**（key 持有时长、网络延迟相对 TTL、暂停相对 TTL、时钟漂移 10%）并写进验收；声明「我们用了单调时钟」只解决了四条里的一条。⑤ 与 §十三分工：hedged/tied 只适用幂等只读（额外副本可丢弃），本节说明非幂等写需要资源侧拒绝旧写——两节合起来给出「哪些加速手段可用于写」的边界。

**来源（r757B 独立实拉 2026-11-16，≥2 独立域一手交叉）**：
- `https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html`（Martin Kleppmann《How to do distributed locking》，**08 Feb 2016**；WebFetch 200，**AI 摘要 60s 超时 ⇒ 返回前 15,000 / 29,464 字原文逐字并如实登记**：efficiency vs correctness 二分、`// THIS CODE IS BROKEN` 读改写示例、GC pause 与 HBase 实例、stop-the-world 数分钟、GitHub 90 秒包延迟、写前检查无效、fencing token 33/34、存储侧主动拒绝回退、ZooKeeper zxid/znode version、Redlock 无 fencing 且随机值不单调、异步模型与时钟只做超时、Redis `gettimeofday` 非单调与 NTP step、Chubby 与 Leases (Gray & Cheriton SOSP 1989) 引用。**第一独立域·研究者一手分析**）
- `https://antirez.com/news/101`（Salvatore Sanfilippo《Is Redlock safe?》，一手 WebFetch 200 **全文逐字**：两条 Martin 论点复述、auto-release 与 liveness、linearizable store 反证、20 bytes /dev/urandom 与 CAS check-and-set、token 顺序与作用顺序不必然一致、非事务资源（物理对象/外部 API）、semi synchronous model 与 5 秒 ±10% 自辩、逐条回应三条 timing assumptions、引用 Redlock 规范 `http://redis.io/topics/distlock`。**第二独立域·算法原作者一手回应（对立立场并陈）**；搜索快照 `https://antirez.com/news/101?spm=...` 同源不作独立计）
- `https://openllm.wavise.com/blog/redlock-distributed-lock-reference`（快照逐字：N=5 / 多数 N/2+1 / validity time = TTL−elapsed−clock drift、release everywhere 与 Lua CAS、双方都同意 fencing token 是补救、资源不能 fence 时锁单独不安全是 inherent limitation）· `https://blog.csdn.net/2401_88756258/article/details/166949127`（快照逐字：TTL 到期是正常行为 Redis 无从知道持有者卡住、三类时钟跳变、「既不像鱼也不像禽」概括非原话已标注）· `https://labhub.hopto.org/blog/architecture/2026-03-12-distributed-lock-redis-redlock-zookeeper-etcd-comparison?lang=en`（**2026-03-12**，快照逐字：双方论点对照表、ZooKeeper 临时顺序节点与 Herd Effect、zxid 当 fencing token、etcd lease/revision）· `https://juejin.cn/post/7639941743310946314`（快照逐字：TLA+ 建模声称找到违反互斥路径、CLOCK_MONOTONIC、INCR 增强模式——**二手转述，未采纳为通用事实**）。**第三~六独立域·教学/技术站立场，逐条登记、不作唯一结论来源**。
- **失败与降级如实登记**：`https://redis.io/docs/latest/develop/use-cases/development-testing/` 与 `https://redis.io/blog/redlock-reasonable-distributed-locks-with-redis/` 均返回 **200 但正文为 `Page not found | Redis`** ⇒ 按「页面不存在」登记**不作信源**，Redlock 规范仅以两位作者文中的引用链接 `http://redis.io/topics/distlock` 登记、未冒充本轮一手访问；Kleppmann 全文后半（时钟跳变段之后）因 15,000 字截断未逐字取得，本节所有引文均落在已取得的前 15,000 字内。
- **判非**：`fencing token` / `fencing` / `Redlock` / `GC pause` / `Martin Kleppmann` / `distributed lock` / `锁过期` / `stop-the-world` / `zxid` / `auto release` / `linearizable store` 全库 `SKILL.md` **0 命中**（`fencing` 1 命中属 `engineering/wb-debug-loop` 事件流围栏，异命题；`分布式锁` 1 命中即本技能 §一既有口号级一句 ⇒ 按「优＝加厚现有」）；`lease` 23 / `租约` 6 命中集中在 `defaults/wb-context-compressor`（**豆包自留地**上下文租约/缓存）与 `engineering/wb-artifact-verification` / `wb-release-maintain`（制品租约，异命题）；`互斥` 13 命中均为并发/独占通用词。模块 `EI/MEMORY.md` §10 重试预算/超时链、§11 双写与 outbox、§12 deadline/取消树、§13 扇出对冲均异命题、不复用。与 r757A(AI) / r756 / r755 结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：Redlock 完整加锁/释放 Lua 脚本与 5 节点部署参数、TLA+ 形式化证明细节、ZooKeeper Herd Effect 与读写锁配方、etcd lease 实现、CLOCK_DRIFT_FACTOR 调参、各中文站给出的 TTL/GC 具体毫秒经验值、二手「Redlock 增强模式」命名。

## 十五、熔断器：在重试之上加一道"别再试了"的短路门（r761B 独立实拉 2026-11-18，≥2 独立域一手交叉，3 独点）

### 15.1（r761B-1）熔断与重试是两种相反意图，必须组合而非二选一；状态机是三正常态 + 三特殊态

- 官方原话：Retry「期望最终成功」而重试，Circuit Breaker「阻止执行很可能失败的操作」。二者组合方式是**通过熔断器调用重试**，且重试逻辑必须**对熔断器返回的异常敏感**——一旦熔断指示故障非暂时，立即停止重试。把熔断当成重试的替代品，或让重试无视熔断异常，都是把两个相反意图接反。
- Resilience4j 明确「three normal states: CLOSED, OPEN, HALF_OPEN and three special states METRICS_ONLY, DISABLED, FORCED_OPEN」——后者分别=总是放行 / 总是放行不记指标 / 总是拒绝。原文更点出 METRICS_ONLY 也是「always allow access」，容易被误当作安全态（它只采集不拦截）。
- 转换：CLOSED 下失败率≥阈值→OPEN；OPEN 拒绝调用（抛 CallNotPermittedException）；等待时长到→HALF_OPEN 放有限个探针；探针失败率仍≥阈值→回 OPEN，低于→回 CLOSED。DISABLED/FORCED_OPEN 下除状态转换外不产生事件、不记指标，只能靠显式转换或 reset 退出——即这两个态是「观测盲区」，排障时不能拿「没有指标」当「没有流量」。

### 15.2（r761B-2）失败率不是瞬时比值：最小样本门 + 两种滑动窗口，缺样本时绝不跳闸

- **最小调用门**：官方逐字——若 minimumNumberOfCalls=10，则必须记录满 10 次才计算失败率；只有 9 次时「even if all 9 calls have failed」也不跳闸。默认值 Resilience4j 给 `minimumNumberOfCalls=100`、`slidingWindowSize=100`、`failureRateThreshold=50`（%）。小流量服务照抄默认会导致熔断器**永不生效**（永远凑不满 100），照抄阈值更会在样本不足时乱跳——这两类错方向相反。
- **两种窗口语义不同**：COUNT_BASED 聚合最近 N 次调用（环形数组 N 个 measurement）；TIME_BASED 聚合最近 N 秒（环形数组 N 个 bucket，每 bucket 聚合该秒全部调用，存 3 个 int[失败/慢/总] + 1 个 long 总耗时）。两者都采用 **Subtract-on-Evict**：新结果进来增量更新总量，最旧项被逐出时从总量减去并重置该槽；因此取 Snapshot 是 O(1)、与窗口大小无关，空间 O(n) 且不逐条存调用。
- 计数口径可配：默认所有异常算失败；可指定哪些异常算失败、其余算成功；也可把某些异常标 ignored（既不算失败也不算成功）。⇒ 「失败率」是**按可配分类后的比率**，不是 HTTP 5xx 计数；接入口径不统一时两个熔断器的阈值不可比。

### 15.3（r761B-3）HALF_OPEN 是受控探针而非放行：探测配额、自动转换开关、共享熔断器的资源分叉

- `waitDurationInOpenState` 默认 60000ms 后才可能转 HALF_OPEN；`permittedNumberOfCallsInHalfOpenState` 默认 10 个探针；`automaticTransitionFromOpenToHalfOpenEnabled` 默认 **false**——为 false 时即使等待时长已过，也**必须有调用进来**才触发转换（避免为每个实例起后台监控线程）。即「时间到了」不等于「已进入半开」，验收要区分。
- Azure 官方点出 HALF_OPEN 的意义：防止恢复中的服务被突然涌入的请求再次压垮——恢复期可能只能承载有限流量，探针配额正是这个上限；任一探针失败即回 OPEN 并重启计时器，成功计数需达到阈值（连续成功）才回 CLOSED。Closed 态的失败计数是**按时间周期自动重置**的，用于避免偶发失败就把熔断器打开。
- 四个考量（Azure 逐字）：① OPEN 态可以用定时 ping / 健康检查代替纯计时；② 恢复时间极不稳定时应提供**手动强制闭合/强制打开**覆盖（对应特殊态）；③ 大量并发实例共享同一熔断器时实现不得阻塞请求或给每次调用加过多开销；④ **一个熔断器覆盖多底层 provider 会误判**——多分片场景一片坏一片好，错误混在一起会导致「该访问的被挡、不该访问的放行」。=> 熔断器的粒度要绑「独立故障域」，不是绑「资源类型名」。

**来源（r761B 独立实拉 2026-11-18，≥2 独立域一手交叉）**：
- `https://resilience4j.readme.io/docs/circuitbreaker`（Resilience4j 官方；WebFetch 200 全文逐字：六状态、失败率阈值/最小调用门、COUNT_BASED 环形数组与 TIME_BASED bucket、Subtract-on-Evict、Snapshot O(1)、参数默认值表、异常分类、事件与 CircularEventConsumer）——第一独立域（库官方一手）
- `https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker`（Microsoft Azure Architecture Center 官方；WebFetch 200 全文逐字：上下文问题、Closed/Open/Half-Open 精确行为、与 Retry 组合及异常敏感、半开防压垮、失败计数按时间重置、四个 Problems and considerations）——第二独立域（架构模式官方一手）
- **失败与降级如实登记**：WebSearch 对 resilience4j.readme.io + learn.microsoft.com 限定域首轮 0 结果 → 改用 WebFetch 直接取官方页全文成功；不冒充搜索命中。Azure 页的图示描述取文字转述（diagram 段落），未读到图像本体。
- **判非**：`circuit breaker` / `熔断器` / `half-open` / `半开` 在 `ei-reliability` 目标技能无既有专节；全库命中中 `wb-subagent-delegation` r733A 一行是当时判非说明（非熔断器本体），豆包自留地（wb-context-compressor / wb-execute-discipline / wb-max-token-saver）命中按去重铁律不落地；与 §六有界重试、§十重试预算、§十三扇出对冲正交——本条管「重试之上的短路门与其状态/样本/粒度」。
- **未采纳**：Resilience4j 完整配置 YAML 与 Spring Boot 集成、CircularEventConsumer 事件缓冲代码、Azure 示例 Flow A/B/C 全量步骤、具体重试退避时长表（只取可落纪律的判据与参数默认值口径）。
