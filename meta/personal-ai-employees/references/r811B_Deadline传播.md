# r811B 逐字存档｜Deadline Propagation（OI · 2026-11-26）

## 实拉来源（WebFetch 200 逐字，≥3 独立域）

### 源1 · gRPC 官方《Deadlines》
URL: https://grpc.io/docs/guides/deadlines/

逐字引文：
- "A deadline is used to specify a point in time past which a client is unwilling to wait for a response from a server. This simple idea is very important in building robust distributed systems."
- "Note that while some language APIs have the concept of a deadline, others use the idea of a timeout. When an API asks for a deadline, you provide a point in time which the call should not go past. A timeout is the max duration of time that the call can take. A timeout can be converted to a deadline by adding the timeout to the current time when the application starts a call."
- "By default, gRPC does not set a deadline which means it is possible for a client to end up waiting for a response effectively forever. To avoid this you should always explicitly set a realistic deadline in your clients."
- "If a server has gone past the deadline when processing a request, the client will give up and fail the RPC with the DEADLINE_EXCEEDED status."
- "A gRPC server deals with this situation by automatically cancelling a call (CANCELLED status) once a deadline set by the client has passed."
- "Please note that the server application is responsible for stopping any activity it has spawned to service the RPC. If your application is running a long-running process you should periodically check if the RPC that initiated it has been cancelled and if so, stop the processing."
- "Deadline Propagation: Your server might need to call another server to produce a response. In these cases where your server also acts as a client you would want to honor the deadline set by the original client. Automatically propagating the deadline from an incoming RPC to an outgoing one is supported by some gRPC implementations. In some languages this behavior needs to be explicitly enabled (e.g. C++) and in others it is enabled by default (e.g. Java and Go). Using this capability lets you avoid the error-prone approach of manually including the deadline for each outgoing RPC."
- "Since a deadline is set point in time, propagating it as-is to a server can be problematic as the clocks on the two servers might not be synchronized. To address this gRPC converts the deadline to a timeout from which the already elapsed time is already deducted. This shields your system from any clock skew issues."
- 图中时序：Client 13:00:00 请求、2s deadline → Billing Server 0.5s 已耗 → 下游 `GetTransactionHistory(timeout: 1.5s)` → 13:00:02 超时 → DEADLINE_EXCEEDED + 各跳 Cancel/Clean up。
- gRPC blog 补充（https://grpc.io/blog/deadlines）："both the client and server make their own independent and local determination about whether the remote procedure call (RPC) was successful. This means their conclusions may not match! An RPC that finished successfully on the server side can fail on the client side."；"services should specify the longest default deadline they technically support, and clients should wait until the response is no longer useful to them"；用 flag 调 deadline 而非硬编码。

### 源2 · zrz.io《Propagate the deadline》(ZFN-61)
URL: https://zrz.io/zfn/61

逐字引文：
- "Every request has a deadline whether you set one or not — the caller's patience."
- "Set the deadline once, at the edge, from product truth — how long is this interaction worth to a human or a calling system? — not from per-hop latency folklore."
- "The default, in almost every HTTP shop, is per-hop timeouts chosen independently: the gateway gives 30s, the service calls the next with its client default of 60, which calls the database with 30 more."
- "The reframe: a timeout is a local, defensive guess; a deadline is a fact about the request — after instant T, the answer has no value."
- "Carry it on every hop as an envelope field, as remaining budget (a duration, decremented per hop) rather than an absolute timestamp, so no two machines' clocks need to agree."
- "An absolute timestamp is cleaner arithmetic and a cross-machine clock dependency you must not take; measure the decrement with the monotonic clock."
- "Set the per-hop timeout from the propagated remainder — the local guess becomes the fallback, not the truth."
- "Timeouts stack with retries multiplicatively. Three tiers each retrying three times with independent timeouts is up to 27 attempts against the struggling dependency — retry amplification wired in at design time."
- "Fit retries inside the deadline, never on top of it. Retries live inside the budget. The retry policy and the deadline are one design: each attempt gets a slice, backoff between slices, and the whole envelope closes when the budget does."
- "`deadline_exceeded` is a distinct, terminal, non-retryable error code: retrying it against the same budget is definitionally pointless. Hedged requests, if you use them, also spend from the same allowance."
- "Where the deadline physically rides: an envelope field defined once, carried by every hop, decremented in middleware — never a body field re-invented per endpoint."
- "Middleware and generated clients own the mechanics: decrement, check, propagate, cancel — application code reads the remaining budget only when it can genuinely adapt (return partial results, skip the enrichment, choose the cheaper path)."
- "Cancel downstream when the caller is gone. A dead deadline should ripple down the call tree and stop work everywhere. When the caller disconnects or the budget dies, propagate cancellation down the tree — modern stacks carry a context/abort signal for exactly this; the work is honouring it in handlers and queries (databases can kill a running query; most services never ask)."
- "Cancellation correctness is real work: a mutation killed mid-flight must be safe to retry or abandon — idempotency and fencing are prerequisites, not nice-to-haves, before you cancel aggressively around writes."
- "Make every state-changing endpoint idempotent (idempotency keys for create/charge/send); a non-idempotent retry double-applies."
- "Every hop must play, or the chain breaks silently — the proxy that drops the header, the legacy service that ignores it, the language client with no cancellation story. Partial propagation degrades soft (inner hops fall back to local timeouts), but audit where the chain actually ends."

### 源3 · iT 邦帮忙 Day11（引 Google SRE Book）
URL: https://ithelp.ithome.com.tw/articles/10414863

逐字要点（对 SRE Book 为二手转述，立场登记）：
- "Google SRE Book deadline 是「剩餘預算」,不是「固定時長」" —— deadline propagation 最常被误解处。
- 反例：handler 已花 0.8s 排队、provider client 仍给自己固定 0.25s → 用户等 1.05s 超原承诺 1.0s 无人发现。
- 正解心算：`remaining = deadline - time.monotonic()`，再与 `CLIENT_TIMEOUT_SECONDS` 取 min；「deadline 沿著呼叫鏈往下傳遞時,往下傳的應該是「還剩多少」,不是「原本設定多少」」。
- "「每一層都有 timeout」是必要條件,不是充分條件,沒有把剩餘預算往下傳,各層 timeout 就只是各自為政的保險絲:上游已經放棄,下游卻還在傻傻做工。"
- 引用 Google Shakespeare Search 66 分钟资源泄漏案例（例外处理路径未释放干净）。

### 源4（二手交叉）
- https://engineering.denis-darkin.xyz/distributed-patterns/timeout-design："Every network call must have a finite deadline"；Timeout Budgets：request 有总 deadline、每步消耗部分预算；Canonical Sources: Nygard《Release It!》+ Google SRE Book。
- https://www.linkedin.com/posts/... (Rowland Adimoha)："A timeout is not simply: 'How long should I wait?' It is: 'How much of this request's latency budget am I willing to spend here?'"；"a child operation can outlive its parent request" 是反模式。
- https://www.100xsystems.dev/... : "Per-call timeouts that are independent let the total budget balloon (10 calls × 500ms = 5s)."；"Propagate deadlines, not independent timeouts"。

## 判非
- deadline（时间点/请求事实）≠ timeout（时长/本地猜测）；传绝对时间戳要付跨机时钟依赖，gRPC 的做法是转 timeout 并扣已流逝时间抗 clock skew。
- 客户端 DEADLINE_EXCEEDED 与服务端 CANCELLED 两端独立判定、可不一致；服务端成功但响应晚于 deadline 客户端仍失败。
- 取消不是只停当前跳：要 ripple down 整树 + 应用主动停衍生工作；写操作取消正确性依赖幂等+fencing。
- partial propagation 静默退化（丢 header/老服务忽略/语言无取消），须审计传播链在哪断。
- 与 §r765A 背压（流速）、§r807B PM（流程状态+补偿）、§r748C 并发预算、§r738A 恢复资格分工：本节管时间预算的跨跳契约。
- 豆包自留地 WB 0 落地；按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。
