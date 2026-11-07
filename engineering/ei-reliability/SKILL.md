---
name: ei-reliability
description: 执行可靠性工程（Execution Intelligence · Reliability）。当任务涉及长流程、多步骤、可失败/可重试的写操作、跨系统动作、需要崩溃续跑或补偿回滚时调用。提供 Saga 编排、补偿事务、幂等键、断点续跑（持久化步骤状态）、有界重试+抖动、死信队列、超时。与 execution_intelligence.py 互补：本技能管"失败后怎么不丢状态、能续、能回"，EI 管"规划/门禁/证书"。
module: EI
modules: EI,VI
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
