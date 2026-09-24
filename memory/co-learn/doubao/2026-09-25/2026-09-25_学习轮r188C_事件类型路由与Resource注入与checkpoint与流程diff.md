# 学习轮 r188-C：事件类型路由与Resource注入与checkpoint复跑与流程diff（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.llamaindex.ai workflow | OK |
| 2 | mastra.ai/docs introduction | 死链跳过 |

## 独点（5 个）
### C1：事件类型即路由——step 按 event 类型自动触发，不写 if/else（来源：LlamaIndex Workflows）
- 每个 step 装饰器标输入 event 类型，框架只在对应 event ready 时调度；类型注解同时做静态校验（接线对不对跑前就报）。
- 判据：**"下一步走哪"由数据类型决定，不是 central dispatcher 里的 if/elif**；加新分支=定义新 Event，不碰老代码。
- **提升层**：工作流。

### C2：Resource() 依赖注入，默认单例共享、cache=False 每步独立（来源：同上）
- 外部依赖（memory/db/http client）用 `Annotated[Mem, Resource(factory)]` 注入，factory 默认只调一次全 step 共享；要每步新实例传 `cache=False`。
- 判据：**依赖生命周期要显式声明**——别让每个 step 自己 new，也别默认全局单例；共享 vs 隔离是个开关不是隐式。
- **提升层**：工具。

### C3：每步 checkpoint，run_from 从任意步重跑（来源：WorkflowCheckpointer）
- 每步完成自动存 checkpoint；调试时不从头跑，`run_from(checkpoint=k)` 从第 k 步续。
- 判据：**长工作流调试成本在重复跑前半段**；与 r188-B fork 互补——fork 从快照 hydrate 新 run，checkpoint 是框架自带的逐步存档。
- **提升层**：工作流。

### C4：ctx 跨 run 传递保持状态（来源：同上）
- 一次 run 完拿到 handler.ctx，下次 `w.run(ctx=handler.ctx)` 续用——多轮交互在同一 workflow 实例上累积状态。
- 判据：**对话状态不是塞进 prompt，是外置 ctx**；与 r187-B blackboard 同源。
- **提升层**：记忆/工作流。

### C5：draw_all_possible_flows vs draw_most_recent_execution——diff 就是死分支（来源：同上）
- 用类型注解画"所有可能路径图"vs"本次实际走过路径图"，两张图 diff 出来的就是声明了但从没触发的分支。
- 判据：**路由死代码能可视化发现**——和 wb-skill-authoring 里"该响没响"互补：那条测单 skill，这条测整个流程的接线死区。
- **提升层**：可复用 Skill（评测/调试）。

## 判重说明
- 事件驱动、context 外置 → 与 CrewAI/LangGraph 同源，取"类型即路由"和"两张图 diff 死分支"增量。
- HITL → @human_feedback 已覆盖。
