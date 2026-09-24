# r173-C 多 Agent Handoff：结构化交接包、路由归 agent 拓扑归开发者、下游当工具描述

实拉时间：2026-09-24 20:19
信源：Microsoft handoff orchestration pattern 2026-05 / Microsoft Learn handoff message schemas / agent-mesh P2P SPEC / Microsoft Copilot Studio multi-agent patterns / IETF agentic AI usecases / Microsoft Agent Framework handoff 2026-08 / Stanford CS224G lecture 7 / Teams A2A bot-to-bot 2026-07（handoff 组，满 10 站）

## 实拉证据（关键原文）
- Microsoft Learn：「Without protocols, autonomous handoffs create context collapse where each transfer loses information. A handoff message is a structured data package.」
- Microsoft handoff pattern：「Routing decisions stay with the agents; topology and guardrails stay with the developer.」开发者声明有哪些 agent 和有向边，框架注入 transfer tool，agent 自己决定下一个谁。
- Copilot Studio：「Treat the entire connected agent as an agentic 'tool' with a description, from the perspective of the parent.」
- Teams A2A：handoff 要带 `aadObjectId`（两个 bot 共享的租户身份）、`tenantId`、`serviceUrl`、`summary`——「one bot sees isn't valid against the other」。
- agent-mesh：handoff payload = `{context, next_step, artifacts}`。

## 独点清单（3 个真独点）

### 独点1：无协议 handoff = context collapse，交接包必须结构化（工作流层）
- 判据：不传结构化交接包、只"把对话传给下一个 agent"，每次 transfer 都会丢信息（context collapse）。交接包固定三槽：`{context 当前状态, next_step 下一步做什么, artifacts 已产出物}`，接收方还要确认收到+能力匹配。
- 独有增量（与 r163B 多智能体协作区别）：那条讲五种编排模式；本条讲**交接时传什么**——具体到 payload schema，且点出无协议 handoff 的 context collapse 失败模式。
- 提升层：工作流。

### 独点2：路由决策归 agent，拓扑和护栏归开发者（工作流层）
- 判据：开发者只声明"有哪些 agent、谁能交给谁"（有向边+护栏），具体下一个谁来说话由 agent 根据上下文自己决定——不是开发者硬编码 if-else 路由。框架把 transfer 做成 agent 可调的工具。
- 独有增量：区分了"拓扑静态配置"和"路由动态决策"两层——不要在代码里写死路由树，也不要放任 agent 乱跳。
- 提升层：工作流。

### 独点3：从 parent 视角把下游 agent 当工具写 description（可复用 Skill 层）
- 判据：parent agent 怎么决定 handoff 给谁？和选工具一样——给每个下游 agent 写一句 description（它擅长什么/什么时候用），parent 根据 description 选。跨系统 handoff 还要带身份上下文（用户 ID/租户/服务地址），因为一个系统的身份在另一个系统无效。
- 独有增量：把 r172-A 工具描述工程的原则直接用到 agent 路由上——handoff 选择和工具选择是同一件事。
- 提升层：可复用 Skill。

## 判非重复理由
- r163B 多智能体五种编排模式；本条讲交接包 schema 与路由分工，增量 >40%。
- A2A/MCP 协议层内容多源重叠只留证据。
