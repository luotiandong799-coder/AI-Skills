# r196-A 审计：Pipedream 深拉 —— 落 1 点（已验证结果的 stale 传播）

- 时间：2026-09-27 03:1x（r196-A）
- 主源：`docs.pipedream.com/llms.txt`（26,255 B，CT=text/plain）+ 6 篇 `*.md` 变体实拉（合计 61,196 B）
  - `connect/mcp/developers`（13,840）· `connect/components/custom-tools`（4,829）· `code/nodejs/rerun`（9,640）· `control-flow`（17,978）· `code/nodejs/using-data-stores`（10,830）· `ai-tooling`（4,029）

## 逐站实拉证据
| 站 | 结果 | 证据 |
|---|---|---|
| docs.pipedream.com/llms.txt | 200 / 26,255 B | 收录 6 篇入选深拉 |
| pipedream.com/llms.txt | 200 / 442,990 B | 应用目录（非方法论面，未深拉） |
| pipedream.com/docs/connect/mcp/developers.md | 200 / 13,840 B | isError + attribution 原文 |
| pipedream.com/docs/workflows/.../control-flow.md | 200 / 17,978 B | **stale 传播原文** |

## 落地（1 点）
- `engineering/wb-artifact-verification` 2.28.0 → **2.29.0**：上游变更后下游中间结果必须降级为 stale，且只沿**已确认执行路径**传播；条件块内延后判；改前序步骤会清空已执行路径。
- 原文坐实：`If prior steps in a workflow are modified or retested, Pipedream marks later steps in the execution path as *stale* ... only marks steps that are in the confirmed execution path as stale.`

## 判非重复理由（逐条 grep 证据）
| 候选点 | 命中 | 结论 |
|---|---|---|
| 工具错误 isError 而非协议级 | `ed` §568/§569「isError: true 是最高影响改动」+ `mcp-builder` §288 | 重叠 >60%，**不落** |
| 挂起超时 / cancel_url / resume 数据 | `ed` §1865 审批挂起超时、§2741 挂起双出口、触发词含「取消链接、resume 与 cancel」 | 重叠 >60%，**不落** |
| **stale 沿执行路径传播** | grep `stale` 仅命中 browser-skill（DOM 陈旧）/ cc（数据过期）/ agent-guild（归档） | **0 命中 → 净新，落** |

## 提升层
工作流 / 可复用 Skill。
