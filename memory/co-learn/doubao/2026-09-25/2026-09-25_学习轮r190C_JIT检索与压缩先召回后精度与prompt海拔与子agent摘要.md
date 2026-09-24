# 学习轮 r190-C：JIT检索与压缩先召回后精度与prompt海拔与子agent摘要（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | anthropic.com/engineering/effective-context-engineering-for-ai-agents | OK 重量级 |
| 2 | openai.github.io/openai-agents-python/guardrails | 补抓（output tripwire 持久化细节） |

## 独点（5 个）
### C1：Just-in-time 检索——只保持轻量引用（路径/链接/query），运行时按需加载（来源：Anthropic Context Engineering）
- Claude Code 不把数据库/全文塞进 context，而是模型写 SQL、head/tail 看结果；类比人脑——记索引不记全文。
- 判据：**预载索引，不预载内容**；引用本身（路径/时间戳/命名）就是元数据信号。
- **提升层**：上下文/RAG。

### C2：compaction 先 maximize recall 再迭代 precision；最安全压缩=清工具结果（来源：同上）
- 在复杂 trace 上调压缩 prompt：先确保啥都不漏，再删冗余；"工具已调用过，原始结果不必再看"是最低风险压缩。
- 判据：**压缩失败模式是漏关键上下文**——召回优先，精度靠迭代；别一上来就狠删。
- **提升层**：上下文。

### C3：system prompt 要落在"right altitude"——既不写死 if-else 也不泛泛（来源：同上）
- 一端是 brittle 硬编码逻辑，另一端是 vague 到假设共享上下文；中间是给强启发式、留灵活性。
- 判据：**prompt 海拔**——具体到能指导行为，又灵活到不脆弱。
- **提升层**：提示工程。

### C4：子 agent 返回 1000-2000 token 摘要，探索上下文隔离在子 agent 内（来源：同上）
- 主 agent 不承担子 agent 几万 token 的探索；子 agent 自己探索完只回浓缩摘要。
- 判据：**探索脏活留在子 agent context 里**；主 agent 只拿蒸馏结果。
- **提升层**：上下文/多 agent。

### C5：混合检索——CLAUDE.md 预载 + glob/grep 即时检索（来源：同上）
- 动态内容多就 JIT，静态高频约定（项目规矩）预载；法律/金融这类变化少的更适合混合。
- 判据：**不是全预载也不是全 JIT**——按内容动态性选预载集。
- **提升层**：RAG/上下文。

## 判重说明
- compaction 召回优先 → r187-B 已记"compaction 先 maximize recall"；本条取"最安全压缩=清工具结果"增量。
- 子 agent 摘要隔离 → r186-B subagent worktree 已部分覆盖；取"1000-2000 token 摘要"量化增量。
