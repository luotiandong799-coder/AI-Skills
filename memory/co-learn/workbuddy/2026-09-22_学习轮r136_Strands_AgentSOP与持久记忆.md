# 学习轮 r136 · Strands Agent SOPs 与持久记忆（2026-09-22）

> 轮号接续：r135 → r136。本轮回合来源 = r133「下轮提示」指定的主源（Strands s23 agent SOPs / s09 session managers）+ OpenAI Agents SDK sessions 旁证。
> 实拉：VPN 关闭（33210 未监听），直连 200；Strands / OpenAI Agents 官方站均可达。

## 一、落地（4 个独点 → 2 个技能升版）

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r136 | engineering/wb-spec-driven/SKILL.md | 1.61.0 → 1.62.0 | ① 半确定性步骤约束（RFC 2119 MUST/SHOULD/MAY）；② SOP 链式分解（artifact handoff 消除重复） |
| r136 | engineering/wb-skill-authoring/SKILL.md | 2.54.0 → 2.55.0 | ③ Agent SOP 是 SKILL.md 的兄弟格式、可互转（`strands-agents-sops skills`）；④ SOP 参数化 + RFC 2119 步约束可借到 SKILL.md |

## 二、独点详述（来源：strandsagents.com，2026-09-22 首读）

**① 半确定性（determin-ish-tic）甜点**——控制-灵活光谱两端是「代码写死流程」（控制强但加行为要重写上百行、脆）与「纯模型驱动」（灵活强但难稳定导到同一目标）。中间地带 = 自然语言步骤 + **RFC 2119 关键字**给每步定「精确控制但不写死」的语义：`MUST` 不可偏离 / `SHOULD` 偏离须显式说明理由 / `MAY` 可选。Amazon 内部数千 SOP 实证：既消「同 agent 不同结果」不一致，又免改 prompt 前长周期人工评测。落法：`SHOULD` 被跳过必须在进度写明理由，否则约束退化成装饰。

**② SOP 链式分解（artifact handoff）**——把整开发周期塞给一个 agent 会 lost focus、偏离预期。改用聚焦 SOP 链，每 SOP 只做一事、把发现浓缩成「聚焦产物」作下一步精简输入：codebase-summary（出文档）→ pdd（出规格）→ code-task-generator（出任务清单）→ code-assist（按已知架构实现）。收益：消除重复劳动（不重复分析同一代码库）+ 规模远超单体。与「委派子 agent」互补：委派给干净上下文，SOP 链靠产物衔接，跨 agent 编排可叠加。

**③ SOP ↔ SKILL.md 互转**——SOP 是「标准化 markdown 自然语言工作流」，与 SKILL.md 同属「一类任务的做法固化」，不是竞争。`strands-agents-sops skills` 直接生成 Anthropic 格式 SKILL.md（每 SOP 一目录）。SOP 多给一步「参数化」（required/optional + 默认值），把单次 prompt 变灵活模板。

**④ 步骤约束借 RFC 2119**——写 SKILL.md 步骤同样适用 MUST/SHOULD/MAY；偏「人在环中、按步交互、要进度可恢复」用 SOP 更轻，偏「被 agent 静默调用、讲究触发准确性」用 SKILL.md 体系更合适，二者并存、SOP 是技能库补充来源。

## 三、判非重复（已查重，不落地）

- **Session / Memory / Storage 三层分离**（Strands Lesson 9：session manager 管单会话对话续接；memory manager 管跨会话持久知识，opt-in 且与 session 解耦；storage 是统一字节后端，三者可共用一 backend；SnapshotSessionManager 原子 blob + immutable checkpoint 回滚）——与 `agent-guild` 的跨 agent 记忆模型重叠 >60%，仅记要点，不重复写。
- **OpenAI Agents SDK sessions**（openai.github.io/openai-agents-python/sessions）：「automatic history persistence + memory controls」与我们既有会话记忆思路一致，无新机制，不落地。
- **AWS AgentCore** 未深读（本轮主源已够；下轮若需可转）。

## 四、清单外新信源（已计入必须项？待用户定）

- `strandsagents.com` 全站（llms.txt 136KB 机器可读索引 + 博客/学习/API 三类 .md 变体）——本轮主源，方法论密度高，建议计入。
- 当前 `urls.txt` 已含 `strands_agents_llms`（第 108 路，r133-C 加），本轮补实际深读页面路径，不新增清单条目。

## 五、审计（待收尾脚本跑）

- 改 2 文件：wb-spec-driven 1.62.0 / wb-skill-authoring 2.55.0。
- PyYAML 解析、CRLF / STRAY_CR / FFD / TRAILING_WS / description>1024 收尾统一校验。
- push：SSH over 443，非强推；cp 回 live 后全量 sha256。
