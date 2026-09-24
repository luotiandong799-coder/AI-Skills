# 学习轮 r189-C：并行化两形态与ACI防错设计与难度路由模型与显式flush与evaluator信号（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | openai.github.io/openai-agents-python/tracing | OK |
| 2 | anthropic.com/engineering/building-effective-agents | OK 五种workflow模式 |

## 独点（5 个）
### C1：并行化分两种——sectioning 拆子任务 vs voting 同任务多跑取共识（来源：Anthropic）
- sectioning：独立子任务并行后聚合；voting：同一任务跑多遍，多个输出投票/多数决提升置信。
- 判据：**"并行"不是一个模式**——要速度用 sectioning，要置信用 voting；guardrail 拆成"生成+审查"两个独立调用属于 sectioning。
- **提升层**：工作流。

### C2：ACI poka-yoke——把工具参数设计成想错都难（来源：同上 Appendix 2）
- SWE-bench 实现发现模型用相对路径会错，改成强制绝对路径后零失误；多相似工具时 docstring 要像给 junior 写。
- 判据：**别靠 prompt 叮嘱模型别犯错，改参数结构让它没法犯**——比加"请用绝对路径"管用。
- **提升层**：工具。

### C3：routing 不仅分任务类型，还按难度路由模型大小（来源：同上）
- 路由 easy/common 给小模型（Haiku），hard/unusual 给大模型（Sonnet）；与任务类型路由正交。
- 判据：**路由表两个维度——类型 × 难度**；别所有问题都用大模型。
- **提升层**：成本/工作流。

### C4：长驻 worker 结尾显式 flush_traces()（来源：OpenAI Tracing）
- 默认后台批量导出，Celery/RQ/FastAPI background job 结束后 trace 不保证立刻可见；要实时可观测就在 trace() 块退出后调 flush_traces()。
- 判据：**"trace 写了"≠"trace 可见了"**；job 结束就被回收的场景必须显式 flush。
- **提升层**：可观测。

### C5：evaluator-optimizer 两个适配信号——反馈能改进 + LLM 能给反馈（来源：Anthropic）
- 两个信号都满足才闭环：人 articulate 反馈时输出确实变好，且 evaluator LLM 自己能给出有用 critique；缺一个就别上这个模式。
- 判据：**迭代写作闭环不是默认该开**；先小样本验证这两个信号。
- **提升层**：工作流。

## 判重说明
- workflow 五模式整体 → 此前已记 orchestrator-worker/routing；取"sectioning vs voting 区分"和"难度路由模型"增量。
- trace 默认开/group_id 关联 → 工程细节。
