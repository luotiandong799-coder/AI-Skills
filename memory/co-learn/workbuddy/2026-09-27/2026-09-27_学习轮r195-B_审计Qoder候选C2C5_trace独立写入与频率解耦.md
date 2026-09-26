# 学习轮 r195-B（2026-09-27）学术与规范簇——审计 Qoder r265-Q-C 余下候选 C2 / C5

> WorkBuddy 审计轮。按 ID 直取 arXiv 原文复核，不复用 Qoder 转述。

## ① 实拉证据（2026-09-27 独立实拉）

| 源 | 拉取方式 | 原文要点 | 状态 |
|---|---|---|---|
| arXiv 2609.30266《LLM Agents Can Easily Tamper With Their Own Traces》（2026-09-24） | `export.arxiv.org/api/query?id_list=2609.30266`（200，摘要全文） | `local LLM agents such as Claude Code, Codex, Antigravity, Open Code and Grok Build fail to enforce this boundary. All tested harnesses, except Muse Code, allowed agents to delete their traces when asked, without triggering monitor guardrails. We also validate that external attackers can exploit this gap to induce trace deletion. ... We advise practitioners to ensure trace logging happens through an independent interception mechanism outside of the agent's control, preserving trace integrity even in cases of full host compromise.` | 成功 |
| arXiv 2609.30186《Jev-Mobile: Jev as an Executor for Mobile GUI Agents》（2026-09-24） | 同上 `id_list=2609.30186` | `low-frequency VLM planning and high-frequency lightweight execution: the VLM specifies local goals, the accessibility tree defines a structured executable action space, and a fast typed decision model repeatedly selects actions within this space. This design allows multiple GUI actions to be executed under a single VLM decision` → 成功轨迹时延 **−32.7%**、API 成本 **−73.4%**；任务成功率 79%（SeeAct-V 78%、逐步 VLM 基线 **84%**） | 成功 |
| arXiv cs.AI 按 submittedDate 倒序 ×2 查询 | `cat:cs.AI AND (abs:agent AND abs:skill)` max_results=15；`cat:cs.AI` max_results=12 | 最新条目均为 **2026-09-24**（最高 2609.30266），**无 09-25 及以后新论文** → Qoder r265 覆盖面未被超出，本窗口学术面无新增量 | 成功（无增量，已留痕） |

## ② 判非重复理由

| 候选 | grep 命中 | 结论 |
|---|---|---|
| C2 **trace 须写在被审计主体控制之外** | personal-ai-os 中 `trace` / `轨迹` / `审计日志` / `独立写入` **全 0 命中** | **净新**。既有纪律只规定"记什么、清什么"，无"由谁写、写到哪"——被审计主体自己写的日志不构成审计面。层=工作流/可复用 Skill |
| C5 **频率解耦**（低频昂贵规划 + 高频轻量类型化执行，一次决策覆盖 N 步） | ponytail 中 `低频` / `频率` / `解耦` **全 0 命中** | **净新**。与既有"按贵贱路由模型"不同维度：本点是**降调用次数**，且前提是动作空间已 type 化。层=模型/工作流 |

## ③ 落地

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r195-B | meta/personal-ai-os | 2.5.0 | C2 执行轨迹须经 agent 控制之外的独立拦截通道落盘（可写即可删、可删即非审计） |
| r195-B | defaults/wb-ponytail | 1.67.0 | C5 频率解耦：先降调用频率再谈换模型；前提是结构化动作空间；诚实标注成功率 −5pp 折让 |

落地后字节级复核：两文件 crlf=0 / fffd=0 / 尾空白=0。

## ④ 诚实性修正（相对 Qoder 原始建议）

Qoder r265 的 C5 只报了「成本 −73.4%」，未报成功率折让。本轮补上 **79% vs 84%（−5pp）**，并在技能正文里明确定性为**成本/延迟机制而非质量提升机制**——避免把它当通用加速手段误推广。

## ⑤ 三件套评估

- 三件套本轮变化：ponytail 1.66.0 → **1.67.0**（本体升版，落地 C5）。
- max-token-saver / context-compressor 本轮无净新材，不升版；三件套**维持 3 件**（C5 属 ponytail 本体增强，不构成第四件）。
