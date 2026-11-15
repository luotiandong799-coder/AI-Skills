---
name: ei-reliability
description: 执行可靠性工程（Execution Intelligence · Reliability）。当任务涉及长流程、多步骤、可失败/可重试的写操作、跨系统动作、需要崩溃续跑或补偿回滚时调用。提供 Saga 编排、补偿事务、幂等键、断点续跑（持久化步骤状态）、有界重试+抖动、死信队列、超时。与 execution_intelligence.py 互补：本技能管"失败后怎么不丢状态、能续、能回"，EI 管"规划/门禁/证书"。
module: EI
modules: EI,VI
version: 1.3.0
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
