# 学习轮 r186-C：trace_id贯穿重试与记忆攒批阈值与NO_INGEST门控与价值打分（2026-09-25）

## 实拉记录（3 站深抓）
| # | 站点 | 结果 |
|---|---|---|
| 1 | pipedream.com/docs/workflows/events | OK：id vs trace_id、事件队列 100 条 |
| 2 | docs.openclaw.ai/ | OK：多渠道网关概览，trusted/untrusted/deterministic r185-A 已记判重 |
| 3 | docs.langflow.org/memory-bases | OK：threshold 攒批/auto-capture 补追/kill phrase/三支柱打分 rubric 全文 |

## 独点（4 个）
### C1：id vs trace_id——重试与挂起恢复靠 trace 串联（来源：pipedream events）
- `context.id` 每次执行唯一（自动重试 3 次 = 3 个 id；suspend 后恢复 = 新 id）；`context.trace_id` 同一原始事件的所有执行共享。
- 判据：**单次执行 id 管"这一次跑的是谁"，trace_id 管"这一串重试/恢复属于同一件事"**；排障时按 trace 串起一次请求的所有执行，而不是孤立看每个 id。与 §执行态与交付态分开 互补——那条管状态记两套，本条管同一逻辑事件多次物理执行怎么关联。
- **提升层**：可观测性/工作流。

### C2：记忆 ingestion 攒批阈值触发，不是每条即写（来源：langflow memory-bases）
- 每跑一次流程消息计数，**累计到 threshold 才异步写向量库**；auto-capture 关期间计数停，重开后自动补处理积累的消息。
- 判据：**记忆写入按批攒，不按条写**——每条都 embed 贵且碎；关了再开必须补追，否则关的那段永久丢。与 r185-C（两阶段提交/游标/去重 join）合起来是完整记忆管线：攒批触发→LLM 蒸馏→写向量库→游标前进。
- **提升层**：记忆/工作流。

### C3：kill phrase 门控——无价值批次跳过入库但游标照进（来源：同上）
- LLM 预处理时若对话无价值，返回 `NO_INGEST`，该批不写向量库；**但 ingestion cursor 仍前进**，下次不重复评估同一批。
- 判据：**跳过 ≠ 不处理**——无价值批次也要"过一遍然后翻篇"，否则游标不动会反复评估同一批空对话。
- **提升层**：记忆。

### C4：记什么不记什么——三支柱打分 rubric（来源：同上 context extraction rubric）
- 每批按三支柱各 +1：核心用户特质（履历/价值观/关系）/ 持久偏好（工具/格式/约束）/ 进行中的项目与里程碑；0 分条件：事务性技术噪音（堆栈/纯语法调试）、客套废话、对已确立事实的陈旧复述。总分 0 → NO_INGEST；≥1 → 只摘持久事实，丢临时调试细节。
- 判据：**记忆入库前过打分 rubric，不一把抓**——与 wb-context-compressor 记忆四策略（语义/摘要/偏好/情节提取）互补：那条管"用什么策略提取"，本条管"提取出来的值不值得长期存"。
- **提升层**：记忆/可复用 Skill。

## 判重说明
- OpenClaw trusted gateway/untrusted execution/deterministic policy、501c3 无遥测 → r185-A 已记。
- DM 共享 session/群聊各自 session/allowFrom 白名单 → session 隔离已覆盖。
- r185-C 已记 chat vs memory base、Filter by Session、落库脱敏，本轮只取"攒批触发/kill phrase/打分"增量。

## 功能套件检查
- wb-context-compressor：C4 三支柱打分 rubric 可直接作为记忆提取的价值门（提取后先打分，0 分丢弃）；当前记忆文件无打分步骤，记为候选升级，不擅改。
