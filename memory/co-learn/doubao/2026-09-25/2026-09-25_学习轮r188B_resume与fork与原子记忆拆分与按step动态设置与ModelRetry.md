# 学习轮 r188-B：resume与fork双水合与原子记忆拆分与按step动态model设置与ModelRetry（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.crewai.com/concepts/flows | OK persist/fork/human feedback/memory |
| 2 | ai.pydantic.dev/agents | OK iter/model_settings/ModelRetry/specs |

## 独点（5 个）
### B1：flow 状态两种水合——resume 续历史 vs fork 派生新 run（来源：CrewAI Flows）
- `kickoff(id=uuid)` resume：在原 flow_uuid 下续跑，历史接着写；`kickoff(restore_from_state_id=uuid)` fork：从快照 hydrate 状态但分配新 state.id，源 flow 历史不动。
- 判据：**"接着上次继续"和"拿上次当模板另开一摊"是两回事**——排错/复跑实验要 fork，真续任务要 resume；别用 resume 做实验把干净历史污染了。
- **提升层**：工作流。

### B2：存记忆前先把长文本拆成原子自含 statement（来源：CrewAI extract_memories）
- `extract_memories(findings)` 把一段叙述拆成一条条 self-contained 事实再逐条 remember；不整段塞。
- 判据：**存的粒度是"一条独立事实"不是"一段话"**——检索时命中一条就拿得到全部，不用把整段回忆出来；与 r186-C 提取四策略互补。
- **提升层**：记忆。

### B3：model_settings 按 step 动态 callable，分层合并（来源：Pydantic AI）
- settings 是个收 RunContext 返回 ModelSettings 的 callable，每次发请求前调用，可按当前节点换 temperature/effort；合并顺序 model defaults→agent→capability→per-run。
- 判据：**不是一个 agent 一套参数到底**——抽取节点用便宜低 effort，判断节点升高；与"模型选择"那条对齐但这是 step 级而非任务级。
- **提升层**：工作流。

### B4：工具内 raise ModelRetry 自动让模型重调（来源：Pydantic AI）
- 工具发现参数不对时 `raise ModelRetry("请用中文重传")`，框架自动在对话里插 RetryPromptPart，模型自己改参数重调，不用写重试循环。
- 判据：**参数错是模型的错，让模型自己修**；与 transport 重试互补——那条管网络层，这条管业务参数层。
- **提升层**：工具。

### B5：agent.iter() 手动逐节点驱动，可在节点间 inspect/mutate（来源：Pydantic AI）
- 不一把 run 到底，用 `async with agent.iter(...)` 逐节点 next()，在节点间可检查/改/跳过——插自己逻辑、做特殊分支。
- 判据：**需要在执行中途插手时，别用 run() 也别重写 agent，用 graph 迭代接口**；与 r187-B blackboard 外置互补。
- **提升层**：可复用 Skill。

## 判重说明
- @human_feedback 审批门 → Guardian/审批已有。
- 结构化状态 pydantic → r187-A typed context 已覆盖。
- AgentSpecs YAML 声明式 → 工程细节，不落。
