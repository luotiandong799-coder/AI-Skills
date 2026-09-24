# 学习轮 r192-B：TDD纵向切片与handoff不重复引用与action敏感记忆与compaction前flush与dreaming打分（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | skills.sh/mattpocock/skills/tdd | OK（SKILL.md 全文） |
| 2 | skills.sh/mattpocock/skills/handoff | OK |
| 3 | docs.openclaw.ai/concepts/memory | OK 重量级 |

## 独点（5 个）
### B1：TDD 纵向切片——一测一实现；RED 时禁 refactor（来源：mattpocock/tdd）
- 反模式 horizontal：先写全部测试再写全部实现→测的是想象行为、对真实变化不敏感。正确 vertical：一个 RED→GREEN→下一个。测试通过公共接口验行为，不 mock 内部/测私有方法。
- 判据：**改名内部函数测试就挂 = 你测的是实现不是行为**；GREEN 之前不许 refactor。
- **提升层**：工作流/工程。

### B2：handoff 文档存 temp 目录+引用 artifact 路径不重复+红敏感+suggested skills 段（来源：mattpocock/handoff）
- 不存 workspace；PRD/ADR/commit/diff 按路径引用而非复述；带"下一个 agent 该调哪些 skill"段；红 API key/PII。
- 判据：**交接文档是指针不是副本**——重复内容会漂移。
- **提升层**：工作流/多 agent。

### B3：action-sensitive memory——记"何时/条件/过期/授权源"不只记事实（来源：OpenClaw memory）
- 涉审批/临时约束/交接/过期/安全时机/来源权威的记忆，必须记动作边界：什么变、何时生效、何时过期、该避免什么、谁授权。
- 判据：**"记住 X"不够，要记"在 Y 条件下才对 X 行动"**——否则过期授权会被旧记忆触发。
- **提升层**：记忆/上下文。

### B4：compaction 前自动 memory flush——静默私有 turn，不进用户轮（来源：OpenClaw）
- 压缩前跑一个私有 copy 的 turn 提醒 agent 存盘，housekeeping 消息不进后续 user turn，写盘正常。
- 判据：**压缩是丢上下文的高危点**——先 flush 再压，用私有 turn 不污染对话。
- **提升层**：上下文/压缩。

### B5：dreaming 后台整合——recall 信号打分+阈值 gate+人审 DREAMS.md（来源：OpenClaw）
- 收集短期召回信号→打分→过 recall-frequency/query-diversity gate→promotion 进 MEMORY.md；阶段摘要写 DREAMS.md 供人审。
- 判据：**长期记忆不是"写完就存"，是"按被召回频率打分才升格"**——从不被想起的不该占长期位。
- **提升层**：记忆。

## 判重说明
- handoff → r189-A 已记 handoff 历史过滤；取"存 temp+引用路径+suggested skills 段"增量。
- memory flush → r189-B 已记 stale compaction；取"压缩前私有 flush turn"增量。
- dreaming 打分 → wb-context-compressor 已有日志→长期两级；取"recall 频率/query diversity gate"增量。
