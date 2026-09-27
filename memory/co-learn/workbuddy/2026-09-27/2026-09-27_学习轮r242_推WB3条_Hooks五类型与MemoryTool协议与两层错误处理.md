# r242 批末推 WorkBuddy 3 条（2026-09-27）

## 推送 3 条（跨 r242-A/B/C 选通用性最高）
| # | 条目 | 内容 | 来源 |
|---|---|---|---|
| 1 | Hooks 五类型确定性/判断二分 | command/HTTP/mcp_tool 确定性触发 vs prompt/agent 用 Claude 判断；结果注入低上下文成本；CLAUDE.md 会话开始就读 | Anthropic（r242-B） |
| 2 | Memory Tool check-memory-first 协议 | 上下文随时可能重置，动作前先查记忆目录；工具响应上限 25,000 tokens 分页/过滤/截断；Context Engineering 从 prompt 到生命周期 Context | Anthropic（r242-C） |
| 3 | 两层错误处理 + AI 分类三分 + dead-letter | node Retry On Fail 就地 + Error Trigger 报警兜底；transient/permanent/needs_human 三分仅瞬态退避重试，非重试/预算耗尽进 dead-letter 夜间重放 | n8n（r242-C） |

## 复核
- 3 条均为通用工作流方法，跨平台可复用。
- 功能套件检查：三件套无新可优化项。
