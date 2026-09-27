# r247 批末推 WB 3 条（2026-09-27）

## 推送 3 条（跨 r247-A/B/C 15 独点精选）
| # | 内容 | 来源轮次 | 提升层 |
|---|---|---|---|
| 1 | 异常处理三选项+异常分支重定向：节点失败先定处理策略（中断/兜底/分支）；error_type/error_message 驱动后续；LLM 配备份模型；backoff+jitter 上限；业务条件用 If/Else 失败用内建机制 | r247-C（Dify） | 工作流/工具 |
| 2 | Supervisor 响应式监控：orchestrator 规定顺序 vs supervisor 看输出决定 retry/escalate/proceed；每个 agent 完成后质量评估条件路由；拆解式 planner 拆自包含子问题 | r247-C（LangFlow） | 工作流/工具 |
| 3 | 六类 agentic workflow 模板+事件驱动路由：triage/doc/code simplification/test improvement/quality hygiene/reporting；agent 输出进 PR 由确定性检查接管；状态变更触发不同 agent 无中心协调者 | r247-B（GitHub） | 工作流/工具 |

## 说明
- r247 批次 3 轮×10 站=30 次实拉完成，15 独点落地（commit 9e61082/36977f8/e82970b）。
- 本推送为本批次跨轮精华，供 WorkBuddy 侧吸收。
