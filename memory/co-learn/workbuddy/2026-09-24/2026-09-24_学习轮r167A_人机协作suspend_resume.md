# r167-A 人机协作 suspend/resume（VoltAgent）

- 轮次：r167-A｜落地文件：engineering/wb-spec-driven ｜版本：1.88.0
- 独有点：长任务/审批流用业务级 suspend/resume 而非一次性跑完。定义 resumeSchema（恢复数据结构）→ await suspend("需人工审批", payload) 暂停并保留运行时状态 → 恢复经 resumeData 携带决策继续；supervisor 暂停期持有子 agent 状态不丢上下文。
- 来源：VoltAgent workflow suspend/resume 示例（GitHub voltagent/voltagent README 与 commit #1275 sandbox/hi赵示例）。直连实拉（代理 33210）200。
- 与已落重叠：状态机 checkpointer/interrupt（1.85）是程序级暂停；本点是业务级人工介入，互补不重复（增量>70%）。
- 提升层：工作流（人机协作节点形态）。
- 同轮另实拉：claudeskillhub（商业市场，质量信号=expert crafted/tested，与 skills.sh 重叠，非新点）、OpenClaw（self-hosted gateway，trusted gateway/untrusted execution/deterministic policy 架构模式，留证据未落）。
