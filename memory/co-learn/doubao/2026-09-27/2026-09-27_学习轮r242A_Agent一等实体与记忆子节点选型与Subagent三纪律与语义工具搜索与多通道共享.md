# r242-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（工作流编排/多 Agent 面） | ✓ | Agent 即一等实体（Invite an Agent 中心化管理能力——发布 agent 后所有使用它的 workflow 自动获得更新 "full-time employee" 模型；聊天构建 agent 自动生成可复用 skills）；Nested agent nodes（v1.3+ 一个 agent 作为 tool 被另一 agent 调用——专业 LLM 角色涌现行为）；Nacos A2A 插件（跨请求会话上下文管理 conversation_id 映射自动维护；单一配置发现所有 agent）；Human Input node v1.13（人工判断原生进工作流）；Agentic RAG（Agent Node 集中决策引擎意图分析/工具编排/源选择/重试逻辑） |
| 2 | n8n（AI agent 记忆面） | ✓ | 记忆子节点选型（Simple Memory window buffer 最后 N 条配置窗口大小/Postgres Chat Memory/Redis/MongoDB 数据库持久）；检索管线比存储重要（向量搜索返回 50 条边缘相关记忆不如 5 条高相关——调 embedding 模型/相似度阈值/rerank）；多通道持久记忆架构（会话总结→embed→Supabase 向量库长期召回；Extract Memory Info 子工作流提取关键信息→MongoDB Atlas 向量库）；独立 sessionId 隔离（每浏览器窗口自动唯一 Session ID 对话分离） |
| 3 | LangFlow（agent/记忆面） | ✓ | Memory bases（1.10 每 flow 向量存储自动摄取对话消息——跨 session 语义检索 vs session-scoped memory；DB Providers 可配置向量后端 Chroma Cloud/OpenSearch/PG pgvector）；session_id 分组（聊天记忆按 session ID 分组，自定义 session ID 隔离不同用户/应用）；内置 chat memory 默认开启（rolling context window per session）；Guardrails 组件（LLM 校验 flow） |
| 4 | Activepieces（AI 功能/搜索面） | ✓ | Tool search 按任务不按名字（ap_search_actions/ap_search_triggers MCP 工具自然语言描述 "send a message to a Slack channel"→语义相似排名最相关 actions/triggers）；honest no-match（低于相关度阈值结果被丢弃而非返回次优）；Run Agent piece（复杂多步推理用工具迭代直到完成；choose its tools app 动作/自己自动化/MCP server/上传文件）；AI Copilot（builder 内引导建议步骤/flow 断裂定位） |
| 5 | Make（AI 面） | ✓ | 多模型编排（单 scenario 内按步骤路由不同模型——分类步骤快廉价模型复杂起草重模型模块级成本优化）；MCP Tools 到 AI Agents（外部 MCP server 访问工具同 run 内与原生模块一起）；多模态 agent（直接输入输出 PDF/图像/CSV 不用外部 OCR）；AI Provider 免 key（内置 OpenAI/Claude 模型所有计划可用自定义 provider 付费计划） |
| 6 | Pipedream（AI 面） | ✓ | Edit workflows with AI（builder 内 AI 编辑——自然语言改整个 workflow/单 code step/报错调试）；AI tooling llms.txt（文档为 AI 消费优化自动生成 llms.txt 供助手/IDE 直接获取文档 API 参考代码示例）；10,000+ prebuilt triggers/actions 组件注册表 |
| 7 | Anthropic（subagents 面） | ✓ | Subagent 三纪律（单职责一个 subagent 一件事/受限工具 read-only reviewer 只 read-only tools/详细 prompt 具体指令示例约束）；三选型（Parallel Claude 独立终端+worktree 多无关任务/Subagents 主会话委托聚焦子任务隔离上下文/Agent Teams 大任务拆分独立工作流协调）；独立 review（未受实现过程影响的评审不知道 tradeoff/被拒方案/假设——外部视角发现主会话漏的）；permission-mode 每 agent 专属工具；Claude 生成初始 subagent 再迭代 |
| 8 | skills.sh（CLI 面） | ✓ | localskills CLI（npm i -g @localskills/cli；版本 pin my-skill@1.2.3 精确/@^ 范围；无参数列表交互选择；flags 平台/scope/install method）；skills CLI 命令矩阵（npx skills find [query] 交互或关键字/add <package> GitHub 或其他源/check 检查更新/update 更新）；find-skills 94.1K 装机量榜首（-g 全局跨所有项目）；多 agent 目标（20+ agents 安装 CLI 声称 70+ 兼容同一 SKILL.md 格式） |
| 9 | docs.openclaw.ai（agent 能力面） | ✓ | 多通道共享上下文（25+ 消息平台单 agent 实例同时处理 WhatsApp 开始 Discord 继续上下文不丢；群聊 mentioned 才响应）；纯文本记忆（无数据库无 embeddings store——plain text files 用户完全控制记忆）；per-agent sandbox+tool 配置（v2026.1.6 每 agent 独立 sandbox 工具限制）；群聊路由（mentionPatterns+group allowlists 严格门控）；fast talk mode（短对话快速模式/长任务返回普通模式带 bounded fallback） |
| 10 | GitHub（生态面） | ✓ | stablyai/orca（ADE agent development environment 桌面/移动/远程运行时跑并行 agent 舰队 +944 趋势）；BuilderIO/agent-native（agentic apps 构建框架）；generalbots/generalbots（多 agent AI 平台 80 自托管 app Chat/CRM/Mail/Drive/Calendar/Advanced RAG Rust）；Letta 25k★（stateful LLM agents 长期记忆前 MemGPT）；VoltAgent/voltagent 10.6k★（TypeScript agent 编排模块化+视觉监控）；AnyJev（任意 LLM 转 Jev 式决策引擎 typed outputs+calibrated probabilities 零训练）；loopx（本地 token-free 决策生成纯推理循环） |

## 判重基准
双键检索（相对 r241-A/B/C 已落章节）：Dify（r241-C 落过分块三策略/插件四件套——"Agent 一等实体+nested agent"独有增量）；n8n（r241-C 落过错误恢复——"记忆子节点选型+检索质量优先"独有增量）；LangFlow（r241-C 落过组件执行开关——"Memory bases 自动摄取"独有增量）；Activepieces（r241-B/C 落过 piece 双角色/沙箱——"语义工具搜索+no-match"独有增量）；Make（r241-A/C 落过错误五型/Functions——"多模型编排+免 key provider"独有增量）；Pipedream（r241-B/C 落过 credit/props——"llms.txt+AI 编辑"独有增量）；Anthropic（r241-A/C 落过流式/JIT——"subagent 三纪律+独立评审"独有增量）；skills.sh（r241-A/C 落过评估驱动/评测八层——"CLI 命令矩阵+版本 pin"独有增量）；openclaw（r241-C 落过 cron 健康——"多通道共享+纯文本记忆"独有增量）；GitHub（r241-C 落过 GNAP/memwyre——"ADE+agent-native+AnyJev"独有增量）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify Agent 一等实体+nested agent | 中心化管理发布即全工作流生效；agent 可作 tool 被调用 | 工作流 | wb-execute-discipline |
| ② n8n 记忆子节点选型+检索质量优先 | Simple window buffer vs 数据库持久；50 边缘不如 5 高相关 | 工作流 | wb-execute-discipline |
| ③ Anthropic Subagent 三纪律+独立评审 | 单职责+受限工具+详细 prompt；reviewer 不知道实现过程 | 工作流/可复用 Skill | wb-execute-discipline |
| ④ Activepieces 语义工具搜索+honest no-match | 按任务描述搜工具语义排名；低于阈值丢弃不返回次优 | 工具 | wb-execute-discipline |
| ⑤ OpenClaw 多通道共享+纯文本记忆+per-agent 隔离 | 跨平台无缝续聊；无 DB 记忆文件用户可控；每 agent 独立 sandbox | 工具/工作流 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
