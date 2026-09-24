# 学习轮 r189-A：guardrail三位置分工与parallel/blocking取舍与handoff历史过滤与input_type边界（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | openai.github.io/openai-agents-python/guardrails | OK 三位置+两模式 |
| 2 | openai.github.io/openai-agents-python/handoffs | OK 历史过滤 |
| 3 | openai agents 首页 / ADK 首页 | OK 概览 |

## 独点（5 个）
### A1：guardrail 三位置分工——input链首/output链尾/tool每次调用前后（来源：OpenAI Agents SDK）
- input guardrail 只跑链上第一个 agent，output 只跑产出最终结果的那个；中间 specialist 之间的检查靠 tool guardrail（每次 function tool 调用前后都跑）。
- 判据：**别以为 agent 级 guardrail 能覆盖委托链**——triage 转 refund 转 billing，agent 级 input/output 只在两头；中间每步要审必须挂 tool guardrail。
- **提升层**：安全。

### A2：input guardrail parallel vs blocking——延迟与成本的开关（来源：同上）
- parallel（默认）：guardrail 和 agent 并发跑，延迟低，但 tripwire 触发时贵模型已烧 token；blocking：guardrail 跑完才启动 agent，省钱但慢。
- 判据：**高风险/贵模型用 blocking 防 token 白烧，低风险用 parallel 保延迟**；默认 parallel 是性能取向，不是安全取向。
- **提升层**：工作流/成本。

### A3：用便宜小模型当 guardrail 审贵模型输入（来源：同上 math homework 例）
- 贵模型慢且贵，前置一个便宜模型判"这是不是越界用途"，命中就 tripwire，不启动贵模型。
- 判据：**审查本身可以用小模型**——guardrail agent 也是 agent，output_type 结构化返回 tripwire_triggered。
- **提升层**：成本/安全。

### A4：handoff 时新 agent 默认继承完整对话历史，敏感内容必须 input_filter（来源：Handoffs）
- 接管=新 agent 看到全部历史；`remove_all_tools` 等预设 filter 可用；nest_handoff_history 把可摘要历史压成段但**不脱敏**——tool args/结果可能进摘要，敏感内容必须自己 filter 掉。
- 判据：**交接不是干净开始**；默认历史全量转发，下一个 agent=信任方，敏感数据得在交接时主动剔。
- **提升层**：安全/上下文。

### A5：input_type 是 handoff 时刻模型决定的元数据，应用状态走 ctx（来源：同上）
- handoff 工具可带 input_type schema（reason/priority/summary），模型在交接时填；但应用状态/依赖走 RunContext.context，两者别混。
- 判据：**模型生成的交接理由 vs 本地已有的应用状态是两个通道**——别让模型传它不该知道的内部状态。
- **提升层**：工作流。

## 判重说明
- handoff 本身=agent as tool → 多 agent 协作已记。
- guardrail 三问 → wb-context-compressor guardian 已有；本条取"三位置分工"和"parallel/blocking 开关"增量。
