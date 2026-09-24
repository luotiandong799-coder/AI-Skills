# 学习轮 r190-A：Loop与Iteration区分与循环变量外置与退出节点与props参数化（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/workflow/node/loop | OK |
| 2 | docs.n8n.io/workflows/code | 死链 |
| 3 | pipedream.com/docs/workflows/steps | OK |

## 独点（5 个）
### A1：Loop vs Iteration——每轮依赖前序 vs 每轮独立（来源：Dify Loop）
- Loop：每轮结果喂下一轮（递归/优化/迭代打磨）；Iteration：批次里每项独立处理（批处理/并行）。
- 判据：**"要循环"先问上一轮结果是不是下一轮输入**——是→Loop，否→Iteration；混了会让独立批处理被迫串行依赖。
- **提升层**：工作流。

### A2：Loop Variables 跨轮持久且循环退出后仍可读（来源：同上）
- 计数器/中间稿（verse）在轮间保持，循环结束后下游节点还能读到最终值。
- 判据：**循环里的累加状态别藏在某轮的 output 里**——显式变量才能在循环外拿终值。
- **提升层**：工作流。

### A3：Exit Loop Node 立即退出，与 termination condition 二选一触发；无退出条件靠 max count 兜底（来源：同上）
- 满足任一立即出；不配退出条件=while(true) 跑到 max count。
- 判据：**任何 AI 迭代循环必须配 max iterations**——"直到满意"没有硬上限就是死循环。
- **提升层**：工作流/安全。

### A4：Pipedream props 把 step 参数表单化，跨 workflow 复用不改代码（来源：Pipedream Steps）
- 用 props 声明输入，workflow builder 自动生成表单；step 一次写好到处填参。
- 判据：**复用不是 copy-paste step，是参数化**——代码不变、参数进表单。
- **提升层**：工作流。

### A5：step 旁 markdown notes 写给未来的自己（来源：同上）
- 每个 step 可挂 markdown note 解释意图/坑；不是注释代码里。
- 判据：**workflow 节点图上的上下文注释**——图读不懂的部分写在节点上，不是文档里。
- **提升层**：可维护性。

## 判重说明
- 循环 max iterations 兜底 → 与 stop_reason/while 终止已有部分重叠；取"两种循环模式区分"和"循环变量外置"增量。
