# 学习轮 r196-C：LangFlow_ToolMode与双输出节流与session分组记忆与n8n集群节点与everything-is-a-plugin（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/workflow | 死链 |
| 2 | docs.n8n.io/advanced-ai | OK |
| 3 | docs.langflow.org/agents | OK 1.12.x |
| 4 | make.com/en/help/scenarios | 标题壳 |
| 5 | docs.anthropic.com agent-skills/cookbook | region 不可用 |
| 6 | modelscope.cn/studios | OK 16,285 |
| 7 | pipedream.com/docs/workflows/steps/params | 死链 |
| 8 | skills.sh/leaderboard | 死链 |
| 9 | deepseek-plugin.org | OK 复核与 r195-B 一致 |
| 10 | GitHub AI 生态（robots 禁走搜索） | OK |

## 独点（5 个）
### C1：LangFlow Tool Mode——任意组件一键变 agent 工具（来源：docs.langflow.org/agents）
- 任何组件（含其他 agent、MCP server）开 Tool Mode 即变成工具：组件输入被改造 + 出现 Toolset 端口，连到 Agent 的 Tools 端口；MCP 工具走专用 **MCP Tools** 组件。
- 判据：**"把组件当工具"是显式开关不是隐式行为**——不开 Tool Mode 组件只是数据节点。
- **提升层**：工作流。

### C2：LangFlow 双输出各一次独立 LLM call——要纯结构化只连 Structured Response（来源：docs.langflow.org/agents）
- Agent 组件 Response 与 Structured Response 两个输出**同时连 = 两次 LLM 调用**；只要结构化数据就只连 Structured Response。
- 判据：**双输出是双成本**——按需只接一个。
- **提升层**：成本/工作流。

### C3：LangFlow chat memory 按 session_id 分组 + 外部记忆走 Message History（来源：docs.langflow.org/agents）
- 默认内置记忆按 session_id 分组滚动窗口；多用户同 flow 必须自定义 session_id 隔离；接 Mem0 等外部记忆必须加 Message History 组件；Structured Response 输出时不写 chat history 不推 Playground 事件。
- 判据：**记忆隔离靠 session_id，扩展靠 Message History**。
- **提升层**：记忆。

### C4：n8n AI 能力=Cluster nodes root+sub-nodes + 1.19.4+ + @n8n/chat widget（来源：docs.n8n.io/advanced-ai）
- Conversational Agent=root node，Model/Memory/Tool Output/Parser 是 sub-nodes；AI 功能 Cloud/self-hosted 1.19.4+；官方 chatbot widget 是 npm 包。
- 判据：**n8n 的 agent 是"根+子"组合不是单节点**。
- **提升层**：工作流。

### C5：GitHub 生态新信号——Everything is a Plugin / YAML 声明式安全研究 / 自进化 harness（来源：GitHub AI 生态走搜索）
- deepseek-harness 206.5k★：一切皆插件（reasoning 策略/tools/输出格式都可替换）；Taskflow Agent（GitHub Security Lab）MIT：YAML 声明式 taskflow + MCP，LLM 自动发现 80+ 真实漏洞；CowAgent 47.1k★：开源超级助理 + harness，plan→run tools/skills→自我进化（memory/knowledge）。
- 判据：**agent 框架竞争已到"可替换一切 + 自我进化"层**。
- **提升层**：生态观察。

## 判重说明
- C1/C2/C3 → r196-B 已记 LangFlow 1.11.x 定位；取 Tool Mode/双输出/session_id 记忆增量（更深一层）。
- C4 → r194-B 已记 n8n sub-workflow 死链；advanced-ai 首次真抓；全新。
- C5 → r195-A/B 已记 GitHub 生态（scientific-agent-skills/google-ax）；取 deepseek-harness/Taskflow/CowAgent 增量。
