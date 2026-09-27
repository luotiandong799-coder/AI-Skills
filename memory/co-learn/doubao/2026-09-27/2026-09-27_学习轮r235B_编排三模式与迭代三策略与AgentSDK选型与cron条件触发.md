# r235-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（Workflow Studio+Iteration/并行节点+生产实测） | ✓ | 四类节点（推理检索/控制流/执行/人工介入）；Variable Aggregator 收敛互斥分支；Iteration 并行最多 10 元素+错误三策略（终止/忽略 null/移除错误输出）；性能边界（30 元素/10 分钟超时）；循环 vs 迭代选型（退出条件 vs 数组逐项）；并行路径同上游多路并发 |
| 2 | n8n（AI Agent 架构模式/复杂模式/模板） | ✓ | 四拓扑（Orchestrator-Executor/Pipeline/Parallel Fan-Out-Fan-In）；Fan-In 用 Wait 暂停聚合；Queue mode（Redis 队列+worker 调度执行分离）；内存子节点（Simple Window/Postgres/Redis/MongoDB）；agent-kit（executionTrace 每 agent token 用量+Skill Loader 从 GitHub 加载 SKILL.md） |
| 3 | Activepieces（changelog 2026-09+AI Agent Builder） | ✓ | Agent 实体化（具名/可对话/可复用，一句描述建 agent）；agent 自选工具（所有连接 app+MCP）；approval 敏感门控（触碰钱/客户/生产设审批）；MCP 暴露工作流为可调用工具给 Claude/Cursor/Windsurf；400+ 集成 |
| 4 | Anthropic（Claude Agent SDK/Managed Agents/Agent Skills 标准） | ✓ | Agent SDK=与 Claude Code 同 harness（loop/内建工具/权限/上下文/subagent）；Managed Agents=托管 harness+state/memory/permissions/scheduled execution；选型五问（数据住哪/工具执行/可观测性/成本/谁运维 runtime）；Agent Skills 开放标准时间线（2025-10-16 产品内→2025-12-18 开源） |
| 5 | GitHub 仓库（claude-flow 13K/Hindsight 20K） | ✓ | claude-flow（hive-mind swarm+SQLite .swarm/memory.db+MCP 套件+SONA 自学习路由 0.05ms）；Hindsight（图记忆引擎+hooks 在 session start/compaction/end/team task 边界自动管道上下文+subagent 共享记忆+一库多工具） |
| 6 | 智谱（AgentMore/ZCode/GLM-5.3） | ✓ | AgentMore（2026-05-25 多 Agent 协作+技能市场+工作流编排）；ZCode Goal 模式（可验收目标拆多轮任务自动改代码跑命令测试按结果决定继续）；GLM-5.3 混合架构（线性+稀疏注意力 320B/18B KV 缓存降）；跳入条件（按意图跳对应 LLM 节点） |
| 7 | OpenClaw（2026.7.1 release+skill-workshop+changelog） | ✓ | cron watch 条件触发（外部命令完成/条件变化才跑）；reapply 同声明原地更新保留 identity/history；Skill Workshop（proposal 草稿+hash+回滚→applied 才 live）；原子更新不破坏 agent；VirusTotal 扫 Claw Hub 技能；iOS/Android 原生 app |
| 8 | agentskills.io/skills.sh（生态注册表+find-skills） | ✓ | skills.sh 7 个月 1 百万技能/2.8 亿安装（GitHub 27 个月/App Store 5 年对比）；find-skills（Vercel Labs：agent 按需检索代装技能六步）；agenticskills.io 189+ verified 16 类；agentskills.codes 19,296 installable 每日扫描；兼容 10+ agent（Claude Code/Cursor/Copilot/Codex/Windsurf/Gemini CLI 等） |
| 9 | WaytoAGI（蓝皮书+Agent Skills 中文生态） | ✓ | Claude Agent Skills 蓝皮书（五篇二十章：认知→Agent Team→自动进化，WaytoAGI×黄叔）；GLM-5.3 Long-Horizon Task（长期跨度维持目标/文件/终端/浏览器状态） |
| 10 | ModelScope/Hugging Face（官方 Skills+生态） | ✓ | ModelScope 官方 Skills 205 个（严格测评+安全扫描+版本历史）；Google Agent Skills（Addy Osmani 20 技能/7 Slash 命令/3 Agent 人设覆盖全生命周期）；anthropics/claude-plugins-official 178K stars；Agents-A1（35B 达万亿参数性能） |

## 判重基准
双键检索：Dify 编排（r225A/r229B 已落变量聚合器，本条独有增量=迭代错误三策略+性能边界+循环/迭代选型）；n8n 编排（r234A 已落多 agent 协作，本条独有增量=Fan-In Wait 聚合+Queue mode+executionTrace 审计）；Anthropic（r233A 已落 Agentic 三模式，本条独有增量=SDK vs Managed 选型五问）；OpenClaw（r234C 已落记忆三工具，本条独有增量=cron watch 条件触发+reapply 原地更新+Skill Workshop 双态）。

## 独点落地（4 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① n8n 编排三模式 | Fan-Out/Fan-In 用 Wait 聚合；Queue mode 调度执行分离；executionTrace token 审计 | 工作流 | wb-execute-discipline |
| ② Dify 迭代节点三错误策略+边界 | 终止/忽略 null/移除错误输出；并行 10 元素/30 元素/10 分钟边界；循环 vs 迭代选型 | 工作流 | wb-execute-discipline |
| ③ Agent SDK vs Managed Agents | runtime 归属五问选型（数据/执行/可观测/成本/运维） | 工作流 | wb-execute-discipline |
| ④ OpenClaw cron 条件触发+Skill Workshop 双态 | watch 条件变化才跑；reapply 原地更新；proposal→applied 双态治理 | 工作流 | wb-execute-discipline |

## 复核
- 四独点均有当日实拉原文来源，无编造。
- 功能套件检查：① 与 wb-execute-discipline 编排面互补；② 与 wb-max-token-saver 边界管理互补；③ 与 wb-debug-loop 互补；④ 与 wb-context-compressor 记忆面互补。三件套无新增归属。
- 垃圾：未产生临时文件。
