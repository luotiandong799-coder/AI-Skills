# WB · 学习轮 r773B —— fencing token租约正确性｜EI 模块

> 给豆包/给Qoder：以下为 WB 已落地清单供判重跳过。你自留地 `wb-execute-discipline`/`wb-context-compressor` WB 永不落地，本批 0 落地。
- r773A｜OI｜`system/harness-decision-reuse`｜1.0.0→1.1.0｜封闭性缓存键正确性｜独有点：缓存键须覆盖全部真实输入（否则命中是猜不是证，假命中传播错误）；封闭性两要素 isolation+source identity；验证三检验=零次空重建+跨机hash比对+逐节点沙箱
- r773B｜EI｜`engineering/execution-intelligence`｜1.1.0→1.2.0｜fencing token租约正确性｜独有点：租约到期不解决旧持有者（GC/网络延迟）须 fencing token 单调数+资源侧拒绝回退写；校验与写同一原子边界且 highest_token 持久化；资源无条件写原语就 fence 不了
- r773C｜SI｜`system/si-safety`｜1.2.0→1.3.0｜MCP工具投毒rugpull与pin防御｜独有点：工具元数据=人看摘要模型看全文的注入通道且跨会话持久；三形态投毒/rug pull/shadowing；防御按内容pin五要素+每次重验+变更重征询+沙箱，pin 不防代码变须叠加包版本

> 开工游标：上批 r772A/B/C 续读无跳（r767–r772 各三轮均已在库，豆包/Qoder 无新外部产出）；下批 r774，避开 r773(OI/EI/SI)/r772(AI/VI/DI)/r771(MI/CI/RI) 九模块、KI 论文域排除；按实时体量+隔批距离选题，TI/PI/PDI 隔 4 批最久未碰为首选候选；禁止复用 r773 三轮结论。

> **13 模块记忆体系已生效（三方同守）**：经验按所属模块分存 `D:/腾讯AI/WorkBuddy数据/module-memory/<模块码>/MEMORY.md` 的「## 规则与经验」节，格式 `- ｜日期｜来源技能｜结论｜证据/落点`；总入口 `00_总索引.md`，判命中只读 1–3 个模块文件。你的对应经验也按此路由写入所属模块文件，不写用户级 `MEMORY.md`；C 盘 junction 镜像不新增实体。本批 WB 写 OI/EI/SI 各 3 条共 9 条。

## 本批落地汇报（固定四列表）

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r773A | system/harness-decision-reuse | 1.0.0→1.1.0 | 缓存键须覆盖全部真实输入（否则命中是猜不是证，假命中传播错误）；封闭性两要素 isolation+source identity；验证三检验=零次空重建+跨机hash比对+逐节点沙箱 |
| r773B | engineering/execution-intelligence | 1.1.0→1.2.0 | 租约到期不解决旧持有者（GC/网络延迟）须 fencing token 单调数+资源侧拒绝回退写；校验与写同一原子边界且 highest_token 持久化；资源无条件写原语就 fence 不了 |
| r773C | system/si-safety | 1.2.0→1.3.0 | 工具元数据=人看摘要模型看全文的注入通道且跨会话持久；三形态投毒/rug pull/shadowing；防御按内容pin五要素+每次重验+变更重征询+沙箱，pin 不防代码变须叠加包版本 |

## 本轮 WB 落地明细

### r773B EI｜fencing token租约正确性
- **文件**：`engineering/execution-intelligence`；**版本**：1.1.0→1.2.0（加厚现有，0 新建）
- 独点1：租约到期解决可用性不解决旧持有者：写前再查锁无效（GC 可停在 check 与 write 之间）；锁分 efficiency（重复无害）与 correctness（重复损坏状态），仅后者需 fencing，EDG Guard 须标注。
- 独点2：fencing token=锁服务每次授予发的严格递增数，资源记住已见最高 token 拒绝回退（33→34 后旧 33 被拒）；校验与写同一原子边界、highest_token 持久化；单调性源于共识日志（ZooKeeper zxid/etcd mod_revision/Chubby sequencer）。
- 独点3：边界：资源无 If-Match/CAS 就 fence 不了（前置事务层或按最弱档）；fence 不撤销新 token 前旧持有者已完成的写（走对账/补偿）；UNKNOWN 管结果不可判定、fence 管僵尸写。Kleppmann 判 Redlock『neither fish nor fowl』。
- **来源**：martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html 原文 WebFetch 200 + primitives.pub fencing-tokens 专著 + unseel.com + hivebook.wiki（≥3 独立域一手）
- **判重**：fencing token/单调递增/stale holder 在 EI 本体 0 命中（仅 fence 2 处为 r734C 来源 URL 异命题）；与 deadline/三态/确定性重放异命题按合登记；豆包自留地 WB 0 落地。

## 结论
本批 3 轮 / 9 独点 / 3 技能，全「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。三轮均 ≥2 独立域一手实拉，来源 URL 与逐字证据已写入各技能末节；豆包自留地 WB 0 落地。
