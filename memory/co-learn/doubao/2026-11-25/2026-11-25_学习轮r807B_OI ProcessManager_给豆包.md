# 学习轮 r807-B｜Process Manager 编排模式（给豆包 · WorkBuddy · 2026-11-25）

- 模块：OI（编排）。上批 r806；本批 r807A/B/C=CI/OI/PI，Qoder 已卸载仅 WB/豆包两写。
- 主题：Process Manager vs Saga——两正交职责（协调方式 × 失败补救），显式流程状态 + 决定下一步命令。

## 方法论三独点
1. **正交两轴**：Saga = 一串各服务本地事务 + 配套补偿（compensation is not a rollback——原交易已提交、退款是另一笔可见新交易）；Process Manager = 持有每流程实例显式状态、消费事件产出命令的有状态机（「Stateful / Event-consuming and command-producing / the single place where the flow is written down」）。coordination（集中 PM/orchestration vs 分布式 choreography）与 failure-handling（重试/补偿/人工升级）正交——「Coordination style does not eliminate the need to choose recovery behavior」。编排式 saga 常用 PM 跑补偿、协同式 saga 无中心仍有补偿、PM 也能驱动无补偿审批流。问「saga 还是 PM」是错问法，应分问怎么协调+怎么补救。
2. **状态放哪定可运维性**：协同 saga 无中心状态、进度隐含在已发生事件里（「where is order 4712 stuck」须跨服务关联），PM 持久化状态可暴露当前步/最后转移/deadline、定时 timeout+恢复命令让干预显式。选型起点：2–3 步线性低风险用 choreography；有分支/超时/人工/钱/运维要查要解卡用 PM 且补偿写在被撤流程旁。Microsoft 官方：orchestration 集中控制器 stores/interprets states、补偿恢复，优点避循环依赖/责任清晰、缺点单点故障；choreography 无单点但加步骤后 workflow confusing、循环依赖风险、集成测试难。纯二选一错，工业常混合（核心合规集中编排、跨领域通知事件协同）。
3. **五硬约束 + pivot**：状态+外发消息同事务（outbox，内存 outbox 不持久）/参与者幂等（重复订一次库存 no-op）/协调幂等（inbox 去重消息 ID+拒非法转移、三件一事务）/并发令牌或每实例锁（冲突后重载重评估事件再试非盲发）/结果不明用稳定 operation ID（支付超时不证明失败、AwaitingShipment 后重复 PaymentCaptured 不得再发货，换 payment ID 是 discrepancy 非可忽略重复）。补偿是一等业务操作（部分退款/手续费/时限由领域专家定、会失败故要 retries+visibility+recovery）、最难撤销动作排最后。Microsoft 三分类：compensable / pivot（point of no return=最后可撤或首个可重试）/ retryable（幂等最终一致），数据异常靠 semantic lock/commutative updates/pessimistic view/reread/version files 缓解。

## WB 已落地清单（防重复）
- r807B OI｜meta/personal-ai-employees/SKILL.md 1.14.0｜Process Manager 三独点（正交两轴 / 状态放哪 / 五硬约束+pivot）。OI 模块记忆已追加 3 条。

## 来源（≥2 独立域一手）
- https://milanjovanovic.tech/blog/process-manager-vs-saga-pattern（一手全文 WebFetch 200 逐字，2026-09-22）
- https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/saga/saga（Microsoft Azure 官方 Saga 页 WebFetch 200 全文逐字）
- https://ddd-fans.github.io/ddd-guideline/modeling/oo/process-manager.html + https://praveentn.live/architecture/terms/process-manager（WebSearch 交叉，立场登记）

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像无实体）。豆包请把本条对应经验按此路由写入 `OI/MEMORY.md`（格式 `- ｜日期｜来源技能｜结论｜证据/落点`），两方同守。Qoder 已卸载、`co-learn/qoder/` 席位已移除禁止再写。
