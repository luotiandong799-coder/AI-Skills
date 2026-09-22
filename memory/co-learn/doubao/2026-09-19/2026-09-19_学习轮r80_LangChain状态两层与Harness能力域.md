# 2026-09-19 学习轮 r80（工程类 · LangChain agents + AutoGen 索引 + 新技能候选）

来源：LangChain agents 官方文档（深读 15519 tokens）、AutoGen AgentChat 索引页；karpathy-guidelines / wshobson/agents 被 robots.txt 拦截（不绕，记观察位）。

## 本批独点（并入 wb-execute-discipline 2.19.0 → 2.20.0）
1. **状态两层分工**：thread_id 管会话级（消息历史/checkpoints 持久化）vs context 管运行级（user_id/API keys/feature flags 单次注入，经 runtime.context 读取）；state_schema/context_schema 分别定型，不混一个 schema。
2. **middleware 钩子数据契约**：钩子读当前 AgentState、返回 dict 合并回去（读 state 写 state）——与 r79 六干预点互补（时机 vs 契约）；messages append-only 只追加不替换。
3. **Harness 能力六域**：execution / context / planning / fault tolerance / guardrails / steering；create_deep_agent 预组装默认栈（filesystem+summarization+subagents+prompt caching）——常用能力按场景预组装，不每次自行拼。

## 判重说明
- 六干预点（r79 已入 ed）→ 本条补"钩子数据契约"增量，不重复。
- append-only / 合并语义 → ed 已有，引用不重写。
- 会话生命周期（OpenClaw reset 三模式，r75 ctx）→ 管"何时换会话"，本条管"会话态与运行态两个槽"——不同维度。

## 观察位
- karpathy-guidelines（forrestchang/andrej-karpathy-skills）→ robots.txt 拦截，暂不可拉。
- wshobson/agents（api-design-principles / architecture-patterns 等 20+ 工程技能）→ robots.txt 拦截，暂不可拉。
- baoyu-skills 系列（微信/小红书生态）→ 候选池（非工程类，按用户指令本轮不深学）。

## 信源健康度
AutoGen 4 → **5**（索引页无新独点）/ LangChain 有收获不计 / LlamaIndex 5 / CrewAI 4。未达 10 无删源。

## 版本变更
- ed 2.19.0 → **2.20.0**（状态两层分工 + 钩子契约 + Harness 六能力域）
