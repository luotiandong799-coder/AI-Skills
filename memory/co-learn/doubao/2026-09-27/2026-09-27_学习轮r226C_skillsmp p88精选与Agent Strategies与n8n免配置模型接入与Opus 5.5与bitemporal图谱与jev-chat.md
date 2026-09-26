# 学习轮 r226C：skillsmp p88精选与Agent Strategies与n8n免配置模型接入与Opus 5.5与bitemporal图谱与jev-chat（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/88（#8701-8753 实拉） | OK |
| 2 | Dify 检索（Agent Node/Agent Strategies/A2A 插件） | OK |
| 3 | n8n 检索（n8n Agents 正式发布/Gateway credits/Raposa 审批节点） | OK |
| 4 | LangFlow 检索（1.8-1.11 release：HITL/A2A/Memory bases） | OK |
| 5 | Activepieces 检索（Changelog 2026-09：Agents 实体化） | OK |
| 6 | Make 检索（AI Agent 新 app open beta/Sales outreach 用例） | OK |
| 7 | Pipedream 检索（Connect/MCP server/Templates） | OK |
| 8 | Claude 检索（release notes 2026-09：Opus 5.5/Fable 5.1/cache diagnostics） | OK |
| 9 | GitHub 生态（ngjoo 2026-09-26/github.hot/yanzhifeng radar/vLLM） | OK |
| 10 | Hugging Face/模型生态（mattpocock/Ollaya/Agnes/Kimi K2.8） | OK |

## 独点（4 个）
### C1：skillsmp p88 精选：token 效率方法包 / 小红书获客三段式 / 直播运营知识库 / 鸿蒙视觉自动化（来源：skillsmp.com/skills/page/88，2026-09-27 实拉）
- **token-efficiency（rohitg00/pro-workflow ★2,875）**：**减少 token 浪费 40-60% 的方法包——anti-sycophancy 规则（禁止讨好式冗余）/工具调用预算（限制调用次数）/一次性编码（one-pass coding）/任务画像（task profiles）/读前写强制（read-before-write）**（token 面增量：与 wb-max-token-saver 互补，具体新方法）。
- **xhs-content-writing（Aria1ever ★41，中文）**：**小红书获客文案三段式：定位→下笔→校对——①他者的面孔定位（阶级光谱+四步定位法，找准读者和信任路径）②情绪弧线下笔（相似感/当事人那句话/开口子，有拦截点才加 Q&A）③说人话收尾（去黑话/去官腔/去焦虑/说完就走）；也用于把 AI 腔改成人话**（新媒体写作增量：高客单种草文方法链）。
- **live-commerce-operations-knowledge-builder（limecloud/lime ★1,473，中文）**：**把直播排期/货盘节奏/场控流程/主播话术/互动机制/异常预案/复盘指标整理成符合 Agent Knowledge v0.6 document-first 标准、可被 AI 安全调用的运营知识库**（知识库构建面：document-first 标准）。
- **harmonyos-device-automation（web-infra-dev/midscene-skills ★311）**：**Midscene 视觉驱动的鸿蒙 NEXT 设备自动化——纯截图操作，不需要 DOM 或无障碍标签，自然语言命令控设备（点按/滑动/输入/启动 app）**（设备自动化面：视觉驱动）。
- **提升层**：工作流 / 可复用 Skill。

### C2：Dify Agent Strategies / n8n Gateway credits 与审批节点 / A2A 互操作（来源：dify.ai/blog Agent Node 2025-03 + marketplace.dify.ai A2A 插件 + blog.n8n.io 2026-09-17/09-25 + community.n8n.io Raposa 2026-09-07，实拉）
- **Dify Agent Strategies（可插拔思考策略）**：**Agent 节点=workflow 里的"大脑"；Agent Strategies 是可插拔逻辑模块，决定 LLM 如何思考和使用工具**（Agent 策略插件化面：与 r226-A workspace skill 管理互补）。
- **A2A Client 插件（ryan_duff/dify-a2a-plugin）**：**连接 Dify agents 到任何实现 A2A 协议 v0.3.0 的外部 agents 协作**（跨 agent 互操作面，新）。
- **n8n Gateway credits（2026-09-17）**：**v2.36 起 n8n Cloud 计划可免建 provider 账号/API key 直接使用 6 家模型提供方+5 个工具服务**（免配置模型接入面，新）。
- **Raposa Approval 节点（n8n community，MIT）**：**工作流暂停直到指定人批准——支付步骤前加人工审批按钮，也可作为 AI agent 工具**（工作流人工审批节点面，新）。
- **提升层**：工作流 / 工具。

### C3：LangFlow 1.11 HITL+A2A / Claude Opus 5.5（来源：langflow.org/blog 1.11 2026-07-22 + platform.claude.com release notes 2026-09-22，实拉）
- **Langflow 1.11（2026-07-22）**：**Human-in-the-Loop（门控工具调用+审查）、A2A 协议原生支持、AG-UI 兼容 streaming 在 Workflow API**（平台级 HITL+A2A 原生支持面，新）。
- **Claude Opus 5.5（2026-09-22 发布）**：**长时程 agentic 编程+知识工作模型；默认 1M token 上下文窗口，最大 128k 输出，adaptive thinking 始终开启不可关闭（thinking disabled 返回 400），用 effort 参数控制思考深度；$4/$20 per MTok（低于 Opus 5 的 $5/$25）**（模型面新事实：effort 参数取代 thinking 开关）。
- **Cache diagnostics GA（2026-09-23）**：**Messages 请求带 diagnostics 对象启用缓存诊断，响应总是含 diagnostics 字段（无诊断时 null）**（可观测性面）。
- **提升层**：模型 / 工具。

### C4：jev-chat 手机对话副驾 / utopia 双时间图谱 / vLLM GPU weight cache / Ollaya 本地决策模型（来源：ngjoo.com/en/trending 2026-09-26 + yanzhifeng.com radar + ai-tldr.dev + dailytrendsignal.com 2026-09-26，实拉）
- **jev-chat/jev-chat-jarvis（★6,591 Kotlin）**：**手机对话副驾——在 QQ/X/飞书里读懂对方、给出候选回复、一键填入输入框，发不发由你；非侵入只读屏幕，不 hook 不改包**（手机 IM 辅助面：只读非侵入设计）。
- **deeplethe/utopia（★10,192 Rust）**：**世界首个开源企业 world model——agent-memory 用 bitemporal（双时间）知识图谱+GraphRAG，可回溯某条事实的历史版本与冲突检测**（双时间知识图谱面：比单时间图谱多"事实版本回溯+冲突检测"增量）。
- **vLLM v0.30.0（2026-09-22）**：**GPU weight cache——Fast Start 让后量化权重驻留 GPU 内存，引擎重启直接映射权重跳过磁盘重载**（推理工程面）。
- **Ollaya**：**Ollama 的开源版用于 Jev 风格决策模型——本机下载/服务决策模型，毫秒级校准答案，数据不出机器**（本地决策模型服务面，与用户 Jev 主题呼应）。
- **提升层**：工具 / 工作流。

## 判重说明
- C1 token-efficiency（anti-sycophancy/工具调用预算/一次性编码/读前写强制）为 wb-max-token-saver 的新增量（≥40%）；xhs-content-writing 含他者面孔定位+情绪弧线独有方法链；live-commerce 知识库 document-first 标准新；Midscene 视觉自动化新；落。
- C2 Agent Strategies（可插拔策略）为 r226-A 的新增量；A2A 插件/Gateway credits/Raposa 审批节点全新；落。未落：Activepieces Agents 实体化（与 r225-C 句子级构建重叠>60% 且独有增量 <40%）。
- C3 LangFlow 1.11 HITL+A2A 原生支持新；Opus 5.5（effort 参数取代 thinking 开关）全新模型事实；落。
- C4 jev-chat（只读非侵入）/utopia（bitemporal 双时间）/vLLM GPU cache/Ollaya 全新；落。
- 未落：Pipedream Connect（r225-C 已落）；Make AI Agent 新 app（与 r225-C AI 面重叠>60%）；transformers-agents 2.0/Agnes/Kimi K2.8（模型列表性质，无方法增量）。
