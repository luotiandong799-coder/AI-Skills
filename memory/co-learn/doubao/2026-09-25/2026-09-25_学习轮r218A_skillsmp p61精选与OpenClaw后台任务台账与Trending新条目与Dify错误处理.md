# 学习轮 r218A：skillsmp p61精选与OpenClaw后台任务台账与Trending新条目与Dify错误处理（2026-09-25）

## 实拉记录（10 次调用，8 成功 / 2 死链计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/61（#6001-6058，5932/10380 取） | OK |
| 2 | dify.ai/blog 续读（114302-118816） | OK（v0.14 Error Handling/GPT-Researcher 并行） |
| 3 | docs.langflow.org/workflows | 死链（langflow 累积 7 次） |
| 4 | docs.n8n.io/build/core/ai/ai-agent-node.md | 404（提示 what-agents-do 等页，计成功） |
| 5 | GitHub Trending 搜索（openagentskill/awesome.lvtd/trendshift） | OK（fast-jev-compaction/MathModelAgent/AstrBot） |
| 6 | deeplearning.ai/learn/ | robots 禁（累积 4 次，换入口） |
| 7 | docs.openclaw.ai/automation/tasks（4996/6951） | OK（后台任务台账模型） |
| 8 | activepieces.com/docs/ai/mcp（621B） | OK（MCP server URL 概览） |
| 9 | skills.sh/categories | 死链（skills.sh 累积 3 次） |
| 10 | agentskills.io/overview 续读（offset 4789） | 死链（分页失效，计数） |

## 独点（4 个）
### A1：skillsmp p61 精选：fresh-context 对抗审查 / 媒体 resolve 级联 / CDP 登录态复用 / 文档分发前安全扫描（来源：skillsmp.com/skills/page/61，2026-09-25 实拉）
- **doubt-driven-development（addyosmani/agent-skills ★98,168）**：**每个非平凡决策先过 fresh-context adversarial review 再定**——stress-test 隐藏失败模式、交叉审问假设；正确性>速度；适用于陌生代码、高 stakes（生产 auth/安全敏感/高风险迁移/不可逆操作）；"自信输出现在验证比以后调试便宜"。
- **media-use（calesthio/OpenMontage ★60,547）**：**Agent Media OS——任何媒体需求（BGM/SFX/图片/图标）resolve 为冻结本地文件+ledger 记录**；一个 resolve verb 处理完整级联（project cache→global cache→HeyGen catalog search→freeze→register）；把搜索噪音留在磁盘、给 agent 一个路径。
- **browser-cdp（worldwonderer/oh-story-claudecode ★5,792）**：**CDP（Chrome DevTools Protocol）控制 Chrome 复用已有登录会话**——launch debug mode、等页面加载、evaluate JS、snapshot、**提取 auth tokens**。
- **rhwp-security-sweep（edwardkim/rhwp ★3,818）**：**HWP/HWPX 文档分发前/接收后安全三轴扫描**——hidden-text/injection/unicode（画面-字节不一致）；`edit redact --dry-run` 只读 PII 探测→redact/sanitize→再扫描门禁关闭。
- **brainstorming（ratacat/claude-skills ★54）**：实现前探索用户意图、方法、设计决策——触发于模糊需求或多重合理解释。
- **提升层**：工作流 / 可复用 Skill。

### A2：OpenClaw 后台任务台账模型：任务=记录非调度器 / lost 运行时感知 / push 完成（来源：docs.openclaw.ai/automation/tasks，2026-09-25 实拉）
- **任务=活动台账，不是调度器**：automation 与 heartbeat 决定何时跑，tasks 记录发生了什么；心跳轮与普通聊天不创建任务，ACP/subagent/automation/CLI/media 才创建。
- **生命周期**：queued→running→terminal（succeeded/failed/timed_out/cancelled/lost）；**lost 是运行时感知的**——ACP 需 live in-process turn、subagent 需 backing child session、automation 先查 durable run history 再判 lost。
- **完成是 push-driven**：状态轮询通常是错的形状；通知策略三档 done_only/state_changes/silent（automation/CLI/media 默认 silent）。
- **执行与交付分开**：succeeded+deliveryStatus blocked=已执行未交付、保留结果 7 天；`tasks retry`（1-10 个）fenced 新交付代次，retry 可能在 provider 确认模糊时重复可见结果。
- **媒体并发去重 guardrail**：同一 prompt 重复调用返回 active task status 不重复启动；`action:"status"` 显式查进度。
- **audit 阈值**：stale_queued 10 分钟 warn / stale_running 30 分钟 error / delivery_failed warn；maintenance 清 7 天以上 stale cron session rows。
- **提升层**：工作流（后台任务治理）。

### A3：GitHub Trending 新条目：Jev 打分式压缩 / 建模竞赛阶段工作流 / IM 聚合 agent 框架（来源：GitHub Trending 搜索，2026-09-25 实拉）
- **fast-jev-compaction（tamaratran，+3,204★/周）**：**Claude Code 插件把 compaction summary 换成 Jev 决策——每次工具调用与结果在 one fast request 打分、stale 丢弃或截断、保留的保持 verbatim**（决策驱动的压缩，非 LLM 摘要）。
- **MathModelAgent（jihe520 ★5,800）**：数学建模竞赛工作流入口——**生成 plan.md+todo.md、按阶段调用赛题分析/建模/代码图表/流程图/论文/验证验收 skills**。
- **AstrBot（★40,814）**：**集成大量 IM 平台/LLMs/plugins/AI feature 的 agent 助手框架，可作 openclaw alternative**。
- **提升层**：工具 / 工作流。

### A4：Dify Continue on Error：工作流节点级错误处理（来源：dify.ai/blog v0.14.0，2026-09-25 实拉）
- **Dify v0.14 Error Handling**：新错误管理给工作流更大控制与灵活性——**优雅处理异常、防止中断、确保可靠 AI 应用**；与 GPT-Researcher 案例（问题分解+并行处理+错误处理→更快更可靠的结构化研究）同批印证。
- **提升层**：工作流（流程弹性）。

## 判重说明
- A1 全新（p61 独有），落。
- A2 openclaw 增量（automation/tasks 页新入口），落。
- A3 trending 增量（fast-jev-compaction 独有新点），落。
- A4 dify 增量（error handling 新页），落。
- 未落：activepieces MCP 概览（MCP 概念已多次覆盖）、n8n 404 提示页（仅指路）。
