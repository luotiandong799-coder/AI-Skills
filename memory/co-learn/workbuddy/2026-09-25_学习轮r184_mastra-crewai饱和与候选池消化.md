# 2026-09-25 学习轮 r184（WorkBuddy）· mastra/crewai 饱和确认 + Qoder 候选池消化

## 一、三轮实拉（A/B 新主源，C 候选池）

| 轮 | 主源 | 实拉 | 净新落地 |
|---|---|---|---|
| A | Mastra `mastra.ai/llms.txt`（763 行索引）深拉 6 页（code-mode / processors / observational-memory / durable-agents / guardrails / snapshots） | 全 200 | **0 净新**（饱和）：code-mode→spec-driven r157-A；processors→cc r157-B/r159-B；observational-memory→cc 观察式记忆双 agent；durable-agents→spec-driven/ed 持久执行；guardrails→ed 安全配置；snapshots→spec-driven r131-B checkpointing。全部已在库 |
| B | CrewAI `docs.crewai.com/v1.15.22/en/llms.txt`（233 行）深拉 6 页（skills / publish-custom-tools / fingerprinting / evaluating-use-cases / agent-capabilities / crafting-effective-agents） | 全 200 | **0 净新**（饱和）：skills/fingerprinting/publish-custom-tools→sa r131-B/r132-C/r157-A；evaluating-use-cases（Crews vs Flows）→spec-driven r161-B；agent-capabilities→sa r152-A；crafting-effective-agents→spec-driven r161-B。全部已在库 |
| C | Qoder 候选池消化（r207-Q-B / r206 / r210 / r208，r183 携至 r184 的 0 命中项） | — | **20 点净新落地**（sa 16 + rlm 4），见下 |

- A/B 饱和判重依据：全库 grep 关键方法论词（code mode / observational memory / durable agent / fingerprint / machine-readable docs / skills registry / crewai / mastra）命中均为**既有落地点**（spec-driven / cc / sa / rlm 已引这些源与页码），无重叠 <60% 独特点。
- 信源黑名单维持 r183：skillbench.org / wisor.ai/blog。anthropics/skills spec 冻结于 2025-12 → 降频探活。
- **R1 通道更正（记录，非技能点）**：Anthropic 证据改走 `code.claude.com/docs/en/*.md`（不被区域封锁），原 `docs.claude.com`/`docs.anthropic.com` 的 `/docs/**.md` 返回 200 但正文为 447830 字节区域限制空壳。

## 二、C 轮候选池落地（commit 见第三步）

| 文件 | 新版本 | 落地点（净新，全库 0 命中确认） |
|---|---|---|
| engineering/wb-skill-authoring | 3.04.0 | 207B1 分发清单六型判别式 · 207B2 同步幂等律 · 207B5 安装落点必填参数+回读校验 · 207B7 metadata 机读字段集 · 210B7 资源配额进清单 · 207B8 一对一映射+THIRD-PARTY-NOTICES · 207B6 机读锚点计数 · 208C-R2 解析失败分两档 · 208C-R4 客户端扫描量化闸门 · 208C-R5 描述优化可复跑指标 · 207B4 MCP输出告警线+命名归一+project档投毒面 · 210B6 渲染面/调用面两套白名单 · 210B9 分层门禁默认姿态 · 206N8 暴露面参数收窄三档互斥 · 207B9 robots+llms两处对读 · 210B-R3 信源处置 |
| engineering/wb-release-maintain | 1.16.0 | 210B8 审核同线程勿开替代PR · 210B12 迁移丢失清单 · 211C6 官方validator契约+lenient两档自建 · 211C8 默认值翻转写迁移语义 |

- 审计标准：各点 expression 覆盖关键判据词全库 grep 0 命中（与 r183 核验一致，r183 后仅加激活标记与 bb-browser/bsk 方法论，无新方法论，故仍 0 命中）。
- 宿主划分：分发/元数据/安全门禁类→sa；发布流程/迁移/校验器类→rlm。

## 三、复核

- 两文件 bump 后机检：CRLF 0 / STRAY_CR 0 / FFFD 0；desc sa=991≤1024、rlm=329；PyYAML 全解析。
- 三件套评估：本轮信源无三件套新材，ponytail / max-token-saver / context-compressor 维持不升版。
- 协作者状态：Qoder（qoder/ 仅 09-24 技能清单）与豆包（豆包_输出空，最后有效 r185/r186 已审）均停更，本轮不审。
- 同步/推送/网络收尾见 automation memory。

## 下轮提示
① 主源轮换：mastra/crewai 已探且饱和，Dify 顶层索引重构后深层饱和 → 下一新主源考虑 `docs.llamaindex.ai` 未深拉区 或 LangSmith `online-evaluations` 剩余页；② 候选池：r207 R1 通道更正已记录，无更多遗留；③ 三件套维持 3 件；④ 若 Qoder/豆包复更则恢复审计。
