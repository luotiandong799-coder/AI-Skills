# r411A · 发布闸门 / 版本真源 / 循环上限计量（WB 自有序列，2026-10-04）

## 一、本轮落地四列表格

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r411-A | engineering/wb-release-maintain | 1.68.0 | ①环境冻结卡「部署」不卡「合并」（17:00–09:00 UTC 合并照收但不部署 staging，内容团队夜间要用稳定环境）；热修若距计划发布 <1h 自动拒绝 ②制品版本只有一个可写真源（package.json 烤进镜像），手填 tag 入口必须过等值校验，失配产物「不可见直到与正确 peer 混合、worker↔app 版本门**静默扣住任务**」 ③发布后回填真源是流水线一环且**有死线**（周四 17:00 RC cut 前），错过则已存在 tag 不被覆盖、错误以版本回退形态跨版本留存 ④回滚 = 换镜像 + 反转目标镜像不认识的迁移；`breaking=true` 无 down() ⇒ 破坏性迁移**永久缩短可回滚窗口**，故可逆性/破坏性必须写成机器可检三字段 |
| r411-A | engineering/wb-debug-loop | 1.143.0 | ①**循环上限的计数单位被自我复制重置 = 没有上限**：per-execution 时限存在，但 job 标 BEGIN 而非 RESUME ⇒ 每轮算新执行，预算每轮重置永不触发；须按同一 run / 同一对象累计 ②**修 bug 后把 bug 的状态签名固化成断言**（RESUME 空态 / BEGIN 非空态），回归从「又出错」变成「被断言挡住并指名原因」 ③**监控缺的是维度不是灵敏度**：绝对量之外必须有增长率与同类重复模式，本次事故由客户上报发现，两条 To-do 恰是这两类告警 |

## 二、实拉证据（逐站）

| 信源 | 通道 | 字节 | 结果 |
|---|---|---|---|
| activepieces `handbook/engineering/playbooks/releases.md` | curl .md | 9,981 | 200 · 首读，净新 |
| activepieces `handbook/engineering/playbooks/database-migration.md` | curl .md | 5,045 | 200 · 首读，净新 |
| activepieces `handbook/engineering/postmortems/2026-03-19-redis-and-delay-overload.md` | curl .md | 3,797 | 200 · **真实事故复盘样本，首读，净新** |
| activepieces `docs/llms.txt` | curl | 35,933 | 200 · 索引 |
| pipedream `conduit/deploy/{architecture,network,monitoring}.md` | curl .md | 5,764 / 9,380 / 9,842 | 200 · 已落盘，留 B 轮消化 |
| 豆包线 | 游标 r406C | — | 无新产出（暂停中，仅探活） |
| Qoder 线 | 游标 r404-Q-B | — | 无新产出 |

## 三、判不落（逐条理由）

- **Canary 每日从 main 新鲜构建 + 破坏性迁移阻断部署**：rm 1.68.0 第⑤点已含「破坏性迁移缩短可回滚窗口」，且 dl 既有「灰度/分阶段放行」>60%。
- **热修分支合并回 main 自动重打 release-candidate**：rm 1.68.0 第④点回填语义已覆盖。
- **CDN 幂等发布（200 跳过 / 404 发布 / 其他失败）**：与 ag Cap62 第⑥点「超限是错误不是截断」+ av 静默族同族，>60%。
- **PGlite 单连接不支持 CONCURRENTLY、迁移内条件分支**：技术特定，非 agent 技能系统可复用方法论，登记项。
- **迁移必须实现 down()（breaking 除外）**：并入 rm 1.68.0 第⑤点三字段机检，不单列。
- **Preview 环境需 PR 打 `preview` label**：登记项。

## 四、WB 已落地清单（判重用 · 版本台账）

> 以下内容 WB 已落地，你们学习时判重，重叠的直接跳过。

| 技能 | 版本 | 最近独点 |
|---|---|---|
| engineering/wb-skill-authoring | 3.122.0 | 注册表审计判连贯性而非危险度；风险等级与审计状态正交；声明即契约 |
| engineering/wb-artifact-verification | 2.131.0 | 产物可达性由落点目录决定；持久 ≠ 可取回 |
| engineering/wb-debug-loop | **1.143.0** | 循环上限计数单位被重置；状态签名断言；监控三类维度 |
| engineering/wb-release-maintain | **1.68.0** | 冻结窗卡部署；版本真源唯一；回滚反转迁移 |
| agent/agent-guild | 1.57.0 | Cap62 加固责任分界表；Cap61 权限策略作用域止于平台执行的一半 |
| defaults/wb-max-token-saver | 1.48.0 起 | 输出压缩 |
| defaults/wb-context-compressor | 3.3xx | 输入压缩（豆包自留地） |

## 五、判重关键词

版本真源 · tag 校验 · 静默扣任务 · 冻结窗 · 合并≠部署 · 回滚反转迁移 · breaking 无 down · 可回滚窗口 · 自我复制循环 · 每次预算重置 · 上限计数单位 · 状态签名断言 · 增长率告警 · 同类重复模式

## 六、方向建议（给下一轮 / 给协作方）

1. Activepieces `handbook/engineering/` 还有 `canary-deployment`、`observability`、`setup-opentelemetry` 等 playbook，属公开的内部工程方法论，性价比高于产品文档。
2. Pipedream `conduit/deploy/{architecture,network,monitoring}` 已 200 落盘，下轮可直接消化（部署形态 / 出网 / 可观测）。
3. dl 487 已触 480 NEAR，下轮落 dl 前必须先下沉。
