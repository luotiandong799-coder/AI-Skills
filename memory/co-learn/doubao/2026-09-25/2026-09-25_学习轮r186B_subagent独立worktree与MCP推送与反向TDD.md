# 学习轮 r186-B：subagent独立worktree与MCP推送通道与反向TDD（2026-09-25）

## 实拉记录（5 站）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.n8n.io/workflows/error-workflows | 死链，留痕 |
| 2 | huggingface.co/spaces | OK：本周榜全是图像/视频/音乐 demo，无方法论不落 |
| 3 | make.com error handling | fetch error，记 1 |
| 4 | skills.sh 榜 | OK：find-skills 2.5M 居首；mattpocock 矩阵（grill/tdd/triage/to-prd/handoff）；caveman 346K |
| 5 | agentskills.io overview | OK：渐进披露 Discovery→Activation→Execution，判重复 |
| 搜索 | GitHub trending agent skill | OK：Claude Code Agent Teams/Channels、wshobson/agents 四类、ECC 反向 TDD |

## 独点（4 个）
### B1：subagent 并行时各持独立 worktree（来源：AI Coding Agent Update 2026-04 · Claude Code Agent Teams）
- Agent Teams：多 Claude 实例共享实时任务列表，1 orchestrator + N subagent，**每个 subagent 拿隔离 git worktree**；最佳用例是并行 code review（安全/性能/测试覆盖率三路同时看）。
- 判据：**多 agent 并行写同一工作区会互相踩，并行的隔离单元是 worktree 不是目录**；reviewer 类并行只读不写才不需要 worktree，真正并行改代码必须每人一个 worktree。与 §多 agent 按技能建 agent 分工——那条管"怎么拆"，本条管"并行写时怎么隔离"。
- **提升层**：工作流/工具。

### B2：MCP 不只被调用，还能 push 消息进 session（来源：同上 · Channels）
- Channels 让 MCP server 主动把消息推进 Claude session，接 Telegram/Discord/webhook——agent 不必轮询外部事件，事件来了 MCP 推进来。
- 判据：**工具默认是 pull（agent 调一次），事件源要 push（外部推一次）**；与 §等待完成靠通知不靠轮询 同源，本条把它落到 MCP 通道层。
- **提升层**：工具/工作流。

### B3：bug 修复反向 TDD——先写失败测试复现，再修（来源：ECC Claude Code 68 agents 286 skills，cosmonet.info 2026-09-08）
- 修 bug 顺序与新功能相反：功能开发是 plan→写代码→测试；修 bug 是**先写一个能复现错误的失败测试→再让它转绿**。
- 判据：**没复现的 bug 修复等于没修**——失败测试是"我确实改对了"的证据，也是回归保护；与 wb-debug-loop 错误签名索引互补：那条管"错误经验怎么记"，本条管"修复动作本身怎么先拿证据"。
- **提升层**：工作流。

### B4：技能仓库四类分目录——agents/skills/orchestrators/tools（来源：gstars.dev/wshobson/agents 85/47/15/44）
- 大技能库按职责分四类：specialized agents（领域专家人格）/ skills（渐进披露知识包）/ workflow orchestrators（多 agent 协调）/ dev tools（脚手架/扫描/测试）。
- 判据：**技能库超过几十个就该分层**，否则"找技能"和"装技能"混在一起；与 §技能矩阵分发互补——那条管怎么装，本条管怎么组织。
- **提升层**：可复用 Skill（仓库组织）。

## 判重说明
- find-skills（vercel-labs）装前先找技能 → r185-A setup 元技能判重，不落。
- agentskills 渐进披露三阶段 → 老知识判重。
- HF spaces 榜是模型 demo，无方法论。
- n8n error-workflows 死链、Make fetch error，留痕。
- 功能套件无新候选。
