# 学习轮 r229A：skillsmp p93尾页master-skill生成器与Dify推理策略插件化与Anthropic subagents判据与RAG grounded模板（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/93 剩余（#9282-9300，total_length=11016 读满） | OK |
| 2 | Dify（Agent Strategies/Agentic RAG/Allowed tools/多模态检索） | OK |
| 3 | n8n（memory sub-nodes 选择判据/echo filtering/多会话 agent） | OK |
| 4 | LangFlow（RAG grounded prompt/reranking/Parser 组件） | OK |
| 5 | Activepieces（AI Agent Builder 工具四来源/审批门 30 天暂停） | OK |
| 6 | Make（external memory 三要素/Data Store 去重/webhook response 前置） | OK |
| 7 | Pipedream（try/catch 错误处理/空结果条件检查） | OK |
| 8 | Anthropic（subagents 使用判据/多 agent 相对增益/Claude Agent SDK） | OK |
| 9 | GitHub 生态（agno ★42,294/langgraph ★42,117/repomix ★28,494/ECC #1） | OK |
| 10 | WaytoAGI（Skills 蓝皮书/BMW Agents @ 符号路由/Context Engineering） | OK |

## 独点（4 个）
### A1：skillsmp p93 尾页精选：master-skill 行业生成器 / email 监听器 / 模板绘图（来源：skillsmp.com/skills/page/93，2026-09-27 实拉）
- **master-skill：行业 Master OS 六轨调研生成器（swaylq/master-skill ★132，2026-09-06）**：**输入"我做的细分行业"→自动完成行业大佬调研/工具地图/工作流/知识正典/信息源/术语标准六轨深度调研→提炼为自包含的 {industry}.master skill 目录——任何 hermit/Claude Code/OpenClaw/Codex agent 都能安装，让 AI 立刻进入"这行的资深人"模式**（可复用 Skill 层：把行业知识固化为可安装技能，生成器模式可复用）。
- **listener-creator：事件驱动 email 监听器（anthropics/claude-agent-sdk-demos ★2,751）**：**监听特定条件（老板紧急邮件/新闻归档/包裹跟踪）并执行自定义动作——条件化触发而非全量处理**（工作流层：监听器按条件路由，不是所有邮件都处理）。
- **paper-plot：模板适配优先于从零画图（ResearAI/DeepScientist ★3,331）**：**结构化数值数据→按捆绑的论文风格绘图模板适配出 publication-quality 图，而不是即兴从零新图**（工具层：先找模板再适配，与 wb-doc-writing"镜像结构"同源）。
- **market-sentiment-monitor：A股市场情绪与风险预警（aliyun/qwen-dianjin ★619）**：**实时跟踪北向资金/两融余额/龙虎榜资金流向/波动率指标，生成情绪与风险预警信号**（工具层：个人可用的 A 股情绪监控四指标）。
- **提升层**：可复用 Skill / 工作流 / 工具。

### A2：Dify 推理策略插件化 + 工具白名单 + n8n 记忆选型判据 + 回声过滤（来源：dify.ai/blog + marketplace.dify.ai + blog.n8n.io + n8nlogic.com，2026-09-27 实拉）
- **Agent Strategies 是插件化推理逻辑模块**：**决定 LLM 如何思考和用工具的策略可插拔——通过自定义接口实现 CoT/ToT/GoT/BoT 等不同推理策略，从 Marketplace 安装**（编排层：推理策略与 agent 本体解耦，可换）。
- **Agent Node 的 Allowed tools 白名单**：**可选列表——有名字时只有这些工具发给模型并允许运行；留空才发全量工具列表**（安全层：工具可见性显式收窄，默认全量是隐患）。
- **n8n memory 选型判据**：**Simple Memory（window buffer）单进程内、进程消失即失；Postgres/Redis/MongoDB Chat Memory 多 worker 或需跨重启存活时必换；Simple Memory 在 queue 模式不持久，只适合单实例测试**（工具层：记忆后端按拓扑选型，不默认）。
- **Facebook Messenger 回声过滤**：**FB 会把 bot 自己发的消息回传给 webhook——不按 sender ID vs page ID 过滤会死循环**（工作流层：webhook 集成先做回声过滤防自触发）。
- **提升层**：工作流 / 工具 / 安全。

### A3：RAG grounded 标准模板 + reranking + Parser 组件 + Make 外部记忆三要素（来源：explainx.ai + masterprompting.net + docs.langflow.org + make.com/en/blog，2026-09-27 实拉）
- **RAG grounded prompt 标准模板与守则**：**只用提供的 context 回答；不在 context 就说不知道；每个主张引用来源编号 [1]/[2]；信息不足明说；部分可答就答部分；结构化输出带 citations/confidence/needs_follow_up 字段**（提示工程层：grounding 六条硬规则+可解析输出 schema）。
- **reranking 必要性与代价**：**vector similarity 是 relevance 的代理——偏词汇/语义重叠、不懂深层意图、受 embedding 质量影响；reranker（cross-encoder 或 LLM 打分器）对 top-K 重排更贵但更准**（RAG 层：先取 top-K 再精排两级检索）。
- **Parser 组件避免整块原始结果进 LLM**：**搜索返回的 JSON 先经 Parser 抽 text 字段再传 Prompt Template——不把整块原始搜索 JSON 塞给模型**（工具层：结构化中间处理）。
- **Make external memory 三要素**：**外部记忆是 agent 之外的持久存储——场景末写入结构化状态、场景初取回；payload 紧凑、类型化、绑定业务键（customer ID/active case ID）**（记忆层：跨天跨触发器的外部记忆设计）。
- **提升层**：提示工程 / RAG / 工作流。

### A4：Anthropic subagents 使用判据 + 多 agent 相对增益 + BMW @ 路由 + Pipedream 错误处理（来源：claude.com/blog + resources.anthropic.com + arxiv.org/pdf/2406.20041 + pipedream.com/docs，2026-09-27 实拉）
- **subagents 值得用的判据**：**3+ 独立任务、每个 10+ 秒、不同任务需不同工具权限（安全扫描器不需要 Write）、已验证 context 污染确实损害质量；overkill 场景：2 个任务且 B 依赖 A 输出、总运行 <5 秒（spawn 开销超过收益）、简单问答**（编排层：子代理不是默认，是条件触发——与 WB Decision Deep 六条件同构）。
- **多 agent vs 单 agent 相对分**：**Anthropic 研究：多 agent（Opus 4 + Sonnet 4 subagents）190.2 vs 单 agent Opus 4 100（相对分）；复杂任务多方向并行时多 agent 系统 outperform 90.2%**（事实：多 agent 有量化增益但非免费）。
- **BMW Agents @ 符号显式路由**：**每轮迭代 Planning→Next→Action 三阶段；Next 阶段用 @Self/@OtherAgent 符号显式指定下一个 agent 继续任务——路由不是隐式的**（编排层：显式符号路由让多 agent 交接可审计）。
- **Pipedream 错误处理具体模式**：**API 调用包 try/catch 只在失败时发通知；空结果条件检查——Wrike 返回 0 任务（假期/安静冲刺）时返回"今日无任务"而不是空 payload 让 Slack 拒绝调用**（工具层：边界输入显式处理）。
- **提升层**：工作流 / 可复用 Skill / 编排。

## 判重说明
- A1 master-skill（行业 Master OS 生成器新面）；listener-creator（条件化触发新）；paper-plot（模板适配优先新）；market-sentiment（A股情绪四指标新）；落。
- A2 Agent Strategies 插件化（r227-C 有 Dify Agentic RAG 框架，本批"推理策略可插拔 CoT/ToT/GoT/BoT"为增量合并）；Allowed tools 白名单（r227 受限 key 面互补，具体机制新）；memory 选型判据（r228-B Data Table 会话记忆互补，本批"Simple vs DB 按拓扑选+queue 失效"为增量合并）；echo filtering（新）；落。
- A3 grounded 模板（RAG 面多轮有相关，本批"六条硬规则+引用编号+结构化 schema"具体化增量）；reranking（r227-C 未落，新）；Parser 组件（新）；Make external memory（新——紧凑类型化绑定业务键）；落。
- A4 subagent 判据（r227-A"先技能后 subagent"与 r228-B Bedrock 多 agent 互补，本批"3+ 任务 10+ 秒/不同权限/已验证污染 vs 2 依赖任务<5 秒"为量化决策增量）；BMW @ 路由（r227-B prompt chaining vs delegation 互补，@ 显式符号机制新）；190.2 相对分（事实）；try/catch 空结果（工具面增量）；落。
- 未落：WaytoAGI Skills 蓝皮书（r227-B 已落）；Context Engineering"开发者从写流程的人变成提供上下文的人"（r227/r228 已多轮覆盖）；LangGPT 提示链（r227-B 已落）；agno/langgraph 排名事实（数量事实无方法增量）。
