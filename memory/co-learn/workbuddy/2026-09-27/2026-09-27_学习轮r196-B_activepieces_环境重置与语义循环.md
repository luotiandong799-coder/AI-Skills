# r196-B 审计：Activepieces 深拉 —— 落 2 点（环境重置成本 / 语义循环计数）

- 时间：2026-09-27 03:2x（r196-B）
- 主源：`activepieces.com/llms.txt`（129,863 B）+ 3 篇博客 `.md` 变体实拉（合计 60,416 B）
  - `what-is-harness-engineering-building-reliable-ai-agents.md`（19,429）
  - `building-a-reliable-harness-for-multi-agent-ai-systems.md`（19,770）
  - `short-term-vs-long-term-memory-for-ai-agents-2026-guide.md`（21,217）

## 落地（2 点）
1. `engineering/wb-debug-loop` 1.59.0 → **1.60.0**（节一）：**环境重置成本决定容忍污染的程度**。
   原文：`When a sandbox takes 30 seconds to refresh, DevOps teams tend to let agents struggle in "dirty" environments to save time, whereas a 100ms refresh rate makes a clean-slate strategy the most efficient path for the model.`
2. `engineering/wb-debug-loop` **1.60.0**（节二）：**参数微变的循环按"同一工具在同一执行内的调用次数"计数，不按参数签名去重**。
   原文：`"semantic loops," where an agent attempts to solve a task by repeatedly calling the same tool with slightly different parameters` / `filtering logs for identical tool calls occurring within a single execution ID`。

## 判非重复理由（逐条 grep 证据）
| 候选点 | 命中 | 结论 |
|---|---|---|
| blast radius <5 文件 / 限目录 | `ed` §977 风险-可逆性矩阵、`ponytail` §409、`ed` §737 contain 三件套 | 重叠 >60%，**不落** |
| 发送成功 ≠ 执行成功（查系统 API） | `bsk-drive-logged-in-browser` §177/§246、`av` 独立证据源 | 重叠 >60%，**不落** |
| 逐步成功率复合衰减（0.95^10≈0.60） | `ed` §2517 六大反模式 ③reliability paradox 已含 `0.95^5≈0.77、0.95^10≈0.60` | **已落，不重复** |
| supervisor 拒绝逻辑须比创意逻辑更刚性 | `av` 确定性 grader 优先（r190-B 判重已记） | 重叠 >60%，**不落** |
| **环境重置延迟 → 策略翻转** | grep「重置成本/脏环境/clean-slate」仅命中 `debug-loop` §374（失败现场快照，不同面） | **0 命中 → 净新，落** |
| **语义循环按工具次数计数** | grep「semantic loop/语义循环/参数微变」**全 0 命中** | **0 命中 → 净新，落** |

## 提升层
工作流 / 工具（节一）；可观测性 / 工作流（节二）。
