# r168-C 长时程Agent状态持久化、Handoff边界与Harness演进纪律

实拉时间：2026-09-24 18:47
实拉信源（10 站，全量逐站，不复用 r168-A/B）：GitHub Trending 每日榜+AI标签仓库 / Anthropic engineering blog / modelcontextprotocol.io 官方客户端最佳实践 / LangGraph vs CrewAI vs AutoGen 基准对比 / OpenAI Agents SDK handoffs+guardrails 官方文档 / LangGraph checkpointer+time travel 官方文档 / brycewatson harness 分析 / 框架对比博客群（groundy/beri/rohitraj）/ heatdrop.ai 热榜 / 腾讯云 MCP 工程实践

## 实拉证据（逐站）

1. **GitHub Trending/热榜**：ponytail（"AI think like laziest senior dev, prefer minimal code"）、jev-chat-jarvis（手机对话副驾）、colibri（纯 C 轻量 MoE 推理机）——生态观察，无方法增量。
2. **Anthropic engineering**（managed-agents + building-c-compiler + brycewatson harness 分析）：同一套 harness 在 Opus 4 上调好的 context reset 行为，升到 Opus 4.5 后消失了，reset 变成 dead weight——所以做了 Managed Agents：长时程 agent 通过少量持久接口运行，不绑死具体 harness 实现；Initializer agent（搭环境+路线图）/ Coding agent（短 burst 增量、每 session clean state）分工，context reset 靠结构化 handoff artifact 传递而非续上下文。
3. **MCP 官方客户端最佳实践**（modelcontextprotocol.io/docs/.../client-best-practices）：工具目录提供多档详情（name-only / name+description / full schema 让模型自选）；工具定义 host 端 memoize，不每次 tools/list round trip；server 发 list_changed 才重新索引；least-privilege schema（不暴露 search_all_tickets，暴露 get_my_tickets 带 user-scoped filter）；secret masking（KEY/SECRET/TOKEN 环境变量自动 REDACTED）；工具描述对着标注的工具选择轨迹数据集自动改写，ToolSelectionAccuracy 提 10-25 点，报告 per-tool delta 只采纳涨分改动。
4. **框架基准对比**（JATIR 论文 + groundy + rohitraj + beri.net）：LangGraph 原生 checkpointing 容错最强（83.3%，API 超时恢复 91.2%）；CrewAI sequential runner 无 mid-pipeline state 持久化——agent 3 挂了整个 crew 从 agent 1 重跑（有人因此单条任务浪费 ₹8400 token）；AutoGen critic-agent 模式处理幻觉最可靠（82.4%）；CrewAI 条件路由弱（"researcher 没结果就跳过写作"要手写 Router agent 绕）。
5. **OpenAI Agents SDK**（openai.github.io handoffs+guardrails 官方）：`agent.as_tool()` = lead 保持控制权调专家汇总输出；`handoffs=[...]` = 专家接管对话 own 最终响应；input guardrails 只作用链上第一个 agent，output guardrails 只作用产出最终输出者，每个自定义 tool 周围要查就用 tool guardrails；handoff 时 inputFilter 可 removeAllTools 清历史。
6. **LangGraph checkpointer**（docs.langchain.com checkpointers + use-time-travel + persistence）：Checkpointer（thread-scoped state 快照：对话连续/HITL/time travel/容错）与 Store（cross-thread key-value：用户偏好/事实/共享知识）**两层分开**；time travel = 从历史 checkpoint replay 或 fork 新轨迹；**replay 不是读缓存——LLM 调用/API/interrupt 会重新触发，结果可能不同**；resume 不是从断点那行代码继续，而是回到 checkpoint 边界重放向前，已完成 task/subgraph 结果从 checkpointer 恢复不重算；interrupt 恢复值按节点内顺序匹配。
7-10. brycewatson/groundy/heatdrop/腾讯云 MCP 实践：均为上述主题的佐证/转述，无新增量。

## 独点清单（3 个真独点）

### 独点1：Checkpointer/Store 两层分离 + Time Travel fork 调试 + replay 不命中缓存（工作流/可复用 Skill 层）
- 原文判据：「Checkpointer persists graph state snapshots per thread; Store persists cross-thread key-value. Time travel forks alternative trajectories. Replay re-executes nodes—LLM calls fire again and may return different results. Resume returns to a checkpoint boundary, replays forward, restoring completed task/subgraph results without recomputing.」
- 独有增量（与 WB r168 suspend_resume / 已有错误恢复的区别）：suspend_resume 只管"暂停后接着跑"，本条管三件 WB 侧没有的：①记忆两层按作用域分——thread 内短期快照与跨 thread 长期事实是两个存储，别混；②调试可以 fork 历史 checkpoint 试另一条路，而不是从头重跑；③重放不是确定性回放，模型调用会重新发生、结果可能变——拿 checkpoint 调试时别把"这次跑出来不一样"当 bug。
- 提升层：工作流。

### 独点2：as_tool vs handoff 的归属边界 + guardrail 三层位置（可复用 Skill 层）
- 原文判据：「Use agent.as_tool(...) when the lead should stay in control, call specialists, combine outputs. Use handoffs=[...] when the specialist should take over and own the final response. Input guardrails apply only to the first agent; output guardrails only to the agent producing final output; use tool guardrails around each custom function call.」
- 独有增量（与已有"多 agent 接口契约/按技能建"的区别）：那条管 agent 怎么拆和接口格式，本条管**决策权归属**——lead 还要汇总就用 as_tool（专家是工具），专家 own 最终答案才 handoff（对话交出去）；以及 guardrail 放哪一层不是随便加——input 只管入口、output 只管出口、中间每个 tool 周围要查就得加 tool guardrail，不加就漏。
- 提升层：可复用 Skill（编排纪律）。

### 独点3：Harness 会随模型版本过期，旧 workaround 要回头清（模型/工作流层）
- 原文判据：Anthropic 实测——「同一个 harness 在 Opus 4.5 上 behavior was gone. The resets had become dead weight.」因此 Managed Agents 按小持久接口设计，不绑死具体 harness。
- 独有增量（与 r168-B「按季度锁模型」的区别）：那条管模型选型多久换一次，本条管**换/升级之后怎么办**——为旧模型行为加的 prompt 补丁、reset 技巧、workaround 在新模型上可能变成负资产（dead weight），每次模型升级要回头审一遍"这些约束现在还需要吗"，不需要就删。与"季度锁模型"合起来才是完整闭环：锁版本→稳定跑→季度评估→升级后清理旧 workaround。
- 提升层：工作流（维护纪律）。

## 判非重复理由
- 独点1 vs WB r168 suspend_resume / 已有错误恢复：两层存储+fork 调试+replay 非确定性 vs 暂停恢复，增量>40%。
- 独点2 vs 多 agent 接口契约/as_tool 已有概念：归属边界（谁 own 最终答案）+ guardrail 三层位置 vs 接口格式，增量>40%。
- 独点3 vs 季度锁模型：升级后清理旧 workaround vs 选型节奏，增量>40%。
- GitHub Trending/MCP 安全最佳实践/框架选型博客群与已有工具面安全/渐进披露重叠>60%，已按规则不落、只留实拉证据。
