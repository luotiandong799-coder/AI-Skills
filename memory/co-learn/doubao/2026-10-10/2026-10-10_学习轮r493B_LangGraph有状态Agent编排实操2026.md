# 2026-10-10 学习轮 r493B：LangGraph 有状态 Agent 编排实操 2026

轮次：r493B（doubao 侧批 r493 第 2 轮）
判重：双键 grep KB 5731 行 + 留痕基线 → 已落多 Agent 编排五种模式与共享知识层（r485C，概念面）、LLM Compiler DAG 与并行决策规则（r491B，概念面）、取消协作式（他方 r490A）——本主题=**state 与 reducer 机制/checkpointer 与 thread/时间旅行/interrupt 与 human-in-the-loop/Send API 动态扇出与超步模型/生产持久化选择**——已落偏编排模式概念与 DAG 决策，本面管 LangGraph 具体实现机制与持久化后端选型，重叠约 35%，按增量判定落地；净增 5 独点。
实拉：3 query×10 站（langchain-use-time-travel/langchain-checkpointers-py/langchain-checkpointers-js/nerdleveltech-resuming-time-travel/mintlify-persistence/dev-interrupt-checkpointer/kindatechnical-hitl-langgraph/markaicode-persistence/markaicode-hitl/xbstack-memory-checkpointing/niteagent-hitl-workflows + langchain-graph-api/langchain-use-graph-api/langchain-zh-graph-api/langchain-workflows-agents/nest-langchain-patterns/markaicode-fan-out-fan-in/dev-langgraph-orchestration/matt-harrison-langgraph-part2/langchain-thinking-in-langgraph/langgraph-cheatsheet-send + langchain-add-memory/langchain-subgraphs/activewizards-checkpointing/dev-langgraph-6-architectures/getwidget-claude-agents-langgraph/agentnative-checkpoint-resume/aiworkflowlab-memory-state/runpod-stateful-langgraph/aiworkflowlab-langgraph-th/callsphere-checkpointer-durable，2026-10-10 实拉），逐站带来源标识。

## 落地 5 独点（每点标注提升层）

### 1. State 与 reducer 机制（工具）
来源：langchain-use-graph-api / matt-harrison / langchain-graph-api
- **图状态=TypedDict schema**：节点是收当前 state 返回更新的函数；边决定下一节点；多出边=所有目标节点下个超步并行执行。
- **每 key 独立 reducer**：控制多节点对同一 key 的更新如何合并；**不显式指定 reducer 则默认覆盖**（后写者胜）；**Send 扇出的合并通道必须配 concat reducer**——worker 返回 `{research: findings}` 而 research 没有 concat reducer，并行 worker 互相覆盖、只剩一个结果——这是最常见的 Send 错误（与忘 messagesState 同族）。
- 提升层：工具（图状态合并）。

### 2. Checkpointer 与 thread / 时间旅行 / 分叉（工具）
来源：langchain-checkpointers / nerdleveltech / callsphere / xbstack
- **checkpointer 在每个超步把 state 快照存入 backing store，按 thread 组织**；compile 时挂 checkpointer 才启用 HITL/时间旅行/故障恢复/会话记忆。
- **time travel**：`get_state_history` 列全部 checkpoint → 重放任意前序执行、或在任意 checkpoint **分叉探索替代轨迹**（fork 成新分支）；节点失败可从 checkpoint 重启——丢失至多该超步工作，不丢整个工作流。
- **MemorySaver 只用于开发**（内存态）；生产用 PostgresSaver/SqliteSaver。
- 提升层：工具（持久化与调试）。

### 3. Interrupt 与 human-in-the-loop（工作流）
来源：dev-interrupt-checkpointer / markaicode-hitl / niteagent-hitl / langchain-use-time-travel
- **interrupt() 暂停节点等 Command(resume=...)**；`interrupt_before/interrupt_after` 指定节点前后停——state 在中断点完整保存。
- **时间旅行时 interrupt 会重新触发**：含 interrupt 的节点重执行、再等新 resume；审批闸门=敏感操作（删记录/写生产/涉钱涉客户）interrupt 等人批，恢复时中断节点重执行。
- **跨中断状态一致性**：checkpointer 自动处理，但要理解存了什么没存什么。
- 提升层：工作流（人机审批闸门）。

### 4. Send API 动态扇出与超步模型（工作流）
来源：markaicode-fan-out / langgraph-cheatsheet / dev-orchestration / nest-langchain
- **Send**：路由函数返回 Send 对象列表，动态创建到节点的边——**运行前不知道并行分支数时用 Send**（map-reduce/orchestrator-worker）；每个 Send 启动独立子图运行（如 map over async task queue）。
- **超级步模型**：所有活动节点完成后图才评估边决定下超步——这是并行扇出/扇入的支撑；子图 worker 要交回控制权给父图用 parent handoff；流式取子图输出设 `subgraphs:true`。
- 提升层：工作流（动态并行编排）。

### 5. 生产持久化选择（可复用 Skill）
来源：activewizards / runpod / getwidget / agentnative / aiworkflowlab-th
- **选型阶梯**：MemorySaver=测试；**多进程/容器化部署用 PostgresSaver**（ACID、可查询、兼审计日志、连接池扩展）——需 asyncpg/psycopg_pool 连接池，阻塞连接卡事件循环；**不要用 Redis 做 checkpoint**（TTL 中途过期，HITL 门控或审批工作流跑不完）。
- **checkpoint 粒度与后端选择（Postgres vs Redis vs object storage）先于框架 checkpointer 承诺决定**；thread_id=长期会话；每超步持久化一次（失败至多丢一步）；LangGraph Cloud（2026-04 GA）把 graph 部署为 API，横向扩展+LangSmith 可观测。
- 提升层：可复用 Skill（持久化后端选型）。

