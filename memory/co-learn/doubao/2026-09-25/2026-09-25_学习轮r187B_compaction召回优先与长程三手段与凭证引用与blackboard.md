# 学习轮 r187-B：compaction先recall后precision与长程三手段分工与凭证引用与blackboard外置（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | anthropic.com/engineering/effective-context-engineering | OK 全文（2025-09-29） |
| 2 | openlegion.ai/en/learn/context-engineering | OK 全文四slot/凭证/blackboard/审计 |

## 独点（5 个）
### B1：compaction 调优先拉满召回，再迭代提精度（来源：Anthropic context engineering）
- 压缩 prompt 先在复杂 trace 上 maximize recall——确保每个关键事实都被摘要；再逐轮提 precision 删冗余。**overly aggressive 会丢"当时看不出重要、后来才关键"的上下文**。
- 判据：**压缩第一步是召回率，不是压缩率**；先宁多勿缺，多了再删。与 r187-A"压缩预算按成功率定"是同一枚硬币两面：那条定目标，本条定调优顺序。
- **提升层**：可复用 Skill（context-compressor）。

### B2：长程三手段按任务形态选，不混用（来源：同上）
- compaction 适合多轮来回的对话流；structured note-taking（NOTES.md/todo）适合有里程碑的迭代开发；sub-agent 适合并行研究——主 agent 只收 1-2k token 摘要，详细探索隔离在 sub。
- 判据：**别一个手段包打天下**；要连续对话用压缩，要记进度用笔记，要并行深挖用 sub。
- **提升层**：工作流。

### B3：凭证用 `$CRED{name}` 引用，vault 网络层解析，原值永不进 context（来源：openlegion）
- API key/JWT/连接串绝不写进系统提示词；agent context 只放引用名，真要时 vault proxy 在工具调用网络层解析。注入攻击让模型"复述系统提示词"时没有凭据可吐。
- 反模式四条：提示注入提取/可观测平台日志整段提示词/工具调用 Authorization 头入日志/多轮任务全程常驻。
- 判据：**最小权限管"给多少权"，本条管"凭据根本不进上下文"**——注入攻击面就从整任务时长缩到零。与 §Agent 工具面安全 互补。
- **提升层**：安全/工具。

### B4：中间状态外置 blackboard，不堆对话历史（来源：openlegion）
- 步骤结果按 key（如 `research/{competitor}`）写外部黑板，不留在对话里；下一步按 key 取。100 步任务 context 大小恒定，step 80 能按 key 查 step 3 输出而它从未占 steps 4-79 的窗口。
- 判据：**对话历史不是记事本**——会被反复重发的中间产物该外置；与 §进度流/诊断流分开、§NOTES.md 同源，本条把它形式化成 key-value 黑板。
- **提升层**：工作流/记忆。

### B5：每轮 context 内容 hash 入不可变审计日志（来源：openlegion）
- 对照 OpenAI Assistants API ~32k 静默截断——开发者看不见当时到底塞了什么，事故时"那轮上下文里有什么"无答案。做法是每轮记录完整 context 内容 hash，事后能精确重建。
- 判据：**静默压缩/截断是正确性负债**——压了什么必须可审可复；与 r186-A 上下文可视化互补——那条给用户实时看，本条给事后审计留证。
- **提升层**：可观测性。

## 判重说明
- context rot/attention budget/n² 是背景事实，不作独点。
- just-in-time retrieval/轻量标识符引用 → r186-A @不读全文、r187-A typed context 已覆盖，不重复。
- 工具结果 1:50~1:250、小模型提取 → 工具结果断言层已覆盖，只取 B3/B4/B5 增量。
