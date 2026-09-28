# r281C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r281A/r281B 各十词 + r280 全表 30 词 + r279 全表 30 词 + r278 全表 30 词错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（chatflow memory） | OK | Conversation Variables（短期记忆单元、多轮保留关键细节）；Variable Assigner 节点（读写关键用户输入）；Chatflow vs Workflow（Chatflow 每轮触发、内置记忆）；LLM 节点 memory + Window Size（50-100 起点）；TokenBufferMemory 短期 vs Knowledge Base 长期；API 调用必须传 conversation_id 维持连续性；Conversation History/Metadata（sys.conversation_id/sys.dialogue_count）；Mem0 插件（Add/Search/Get/Update/Delete Memory） |
| 2 | n8n（AI agent） | OK | AI Agent 节点 1.82 起统一为 Tools Agent（旧类型设置移除）；必须连至少一个工具 sub-node；Conversational Agent（Chat Trigger+memory sub-node、memory 不跨会话持久、系统提示描述工具+解析 JSON tool calls）；Plan and Execute Agent（先高层计划再逐步执行、结构化任务）；Require Specific Output Format（Auto-fixing/Item List/Structured Output Parser）；Enable Fallback Model（主模型失败用备份）；Return Intermediate Steps；LLM vs AI Agent 对比（文本生成 vs 目标导向任务完成、多步+工具） |
| 3 | LangFlow（vector RAG） | OK | Vector Store RAG starter（Load Data 子流程+Retriever 子流程、Astra DB 示例）；vector store 组件（embedding 存储/similarity search/Graph RAG traversals/OpenSearch）；Local RAG（Ollama+ChromaDB 全本地无外部网络）；Web-based RAG（URL/RSS→清洗分块→embed→grounded 回答）；Langflow 1.11 多向量检索（ColBERT late interaction + ColPali 视觉文档检索，lfx-nextplaid 免胶水代码）；PGVector 组件；Embedding Model 组件；RAG chatbot（Load Data Flow 只管加载、Retriever Flow 应答） |
| 4 | Activepieces（error handling） | OK | 每步可配 Continue on Failure（失败继续）/ Retry on Failure（自动重试）；自动 action-level 重试（指数退避、瞬态失败）；手动 flow-level 重试策略（持久失败）；Execution error types（分类失败模式判重试资格）；AI workflow 模式（validation 步骤、log prompt IDs+outputs 审计、分支重试/回退/升级、run status 记表、未解决转人工）；LLM workflow（重试+timeout+fallback 分支、JSON schema 结构化输出、检索事实+引用减幻觉、checkpoint 恢复）；webhook（幂等键+correlation ID 防重复、backoff）；step-level run logs（输入输出错误）；AP_MAX_FLOW_RUN_LOG_SIZE_MB 截断日志 |
| 5 | Make（templates） | OK | 两类模板：Public（Make+社区、7500+ 用例）/ Team（自己与团队创建、默认私有→发布可链接分享→可提交评审转 public）；Blueprint（可复用版本含模块/模块设置/映射值；备份、导出分享、导入复用）；Templates tab 左侧栏；AI 模板注意 prompt design/JSON 输出解析/错误处理 |
| 6 | Pipedream（concurrency） | OK | Concurrency=并行 worker 数（设 1=串行有序，前一个执行完才处理下一个）；Throttling=execution rate controls（每单位时间执行数）；超过并发/节流的事件进 workflow 专属队列（FIFO）；队列上限免费 100、可提到 10000；冷启动（约 5 分钟不活动后首次请求要 spin up 新环境）；HTTP endpoint QPS 限制可申请提高；全局节流方案（单 workflow 统一管理并发再按请求属性转发，内建不支持优先级） |
| 7 | Anthropic（tool use） | OK | **合并相关操作为更少工具（create_pr/review_pr/merge_pr→单工具 action 参数）减少选择歧义**；Tool Search Tool（工具定义>10K tokens 或 10+ 工具或 MCP 多 server 时先搜索再调用；<10 工具或全频繁用没必要）；computer use 提示（每步后截图评估、显式展示评估）；writing tools 五原则（选对工具/namespacing 定义边界/返回有意义 context/优化 token 效率/提示工程描述）；12-step tool loop（user query→list tools→Claude→tool call→result→response）；resources vs tools（数据加载 vs 行动） |
| 8 | skills.sh（首次实拉） | OK | Vercel 技能目录+排行榜；SKILL.md 指令包、任何 GitHub 仓库可发布、20+ AI agent 可装（npx skills add owner/repo）；官方 curated 集（makers 教自己产品，/api/v1/skills/curated）；find-skills 技能（发现+验证+安装，集成 skills CLI）；微软/Vercel/Anthropic/WordPress/OpenAI 官方技能库；免费、MIT 开源 CLI；leaderboard 排行 |
| 9 | deeplearning（AI coding） | OK | Generative AI for Software Development 专精（prompt LLM 做编码任务到复杂设计模式与数据库架构、保持代码质量与设计控制权、Gartner 70% 采用预测）；AI Coding Workflows: Hybrid to Local（JetBrains Paul Everitt、PyCharm AI Chat、开源权重模型、控制/选择/成本动机）；AI Python for Beginners（Andrew Ng、AI 助手调试代码/解释概念） |
| 10 | OpenClaw（gateway auth） | OK | **默认 localhost 也要求认证**；gateway.auth.token/password（或 OPENCLAW_GATEWAY_TOKEN 环境变量）；WebSocket 握手 connect.params.auth.token/password；Tailscale Serve 身份头（gateway.auth.allowTailscale:true）；trusted-proxy 模式（identityScopes 逐 scope 授权、trustedProxy.userHeader）；claude auth login 复用本地 CLI 登录（两阶段：网关主机登录 Claude Code→openclaw models auth login 指向 claude-cli 后端）；模型 provider API key 在 gateway host 配置（export PROVIDER_API_KEY）；auth.mode:none 仅单机本地；openclaw doctor --fix 启用 token 认证 |

## 判重（双键检索，增量判定）
- Dify 会话记忆（r281B 编排/r281A 插件）→ Conversation Variables+Variable Assigner+Window Size 为独有增量 → **落地**
- n8n AI agent（r281B code node/r281A 二进制）→ 新面（AI Agent 节点与输出解析器）
- LangFlow vector RAG（r281B 多代理/r281A 认证）→ 重叠>60% 但向量组件+多向量检索（ColBERT/ColPali）含独有增量 → **增量合并**
- Activepieces 错误处理（r281B piece 构建/r281A 治理）→ 每步 Continue/Retry+两级重试+AI workflow 错误模式为独有增量 → **落地**
- Make 模板（r281B 回滚/r281A 连接）→ 新面（模板两级制+Blueprint）
- Pipedream 并发（r281B 签名/r281A 目录）→ 新面（并发/节流/队列/冷启动）
- Anthropic 工具设计（r281B Skills/r281A 记忆/r280 工具循环）→ 重叠>60% 但工具设计原则（合并/Tool Search/五原则）含独有增量 → **增量合并**
- skills.sh → 全新站点首次实拉 → **新面**
- deeplearning AI coding（r281B RAG/r281A 编排）→ 新面（软件工程课程生态）
- OpenClaw 网关认证（r281B 附件/r281A dashboard）→ 认证机制（token/trusted-proxy/Tailscale）为独有增量 → **落地**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 会话记忆与变量 | 工作流 |
| 2 | n8n AI Agent 节点 | 工具 |
| 3 | LangFlow 向量存储 RAG 管线 | 工具 |
| 4 | Activepieces 错误处理与重试 | 工具 |
| 5 | Make 模板与蓝图 | 工具 |
| 6 | Pipedream 并发与节流 | 工具 |
| 7 | Anthropic 工具设计原则 | 可复用 Skill |
| 8 | skills.sh 技能目录与 CLI | 可复用 Skill |
| 9 | deeplearning 软件工程课程 | 工作流 |
| 10 | OpenClaw 网关认证 | 工具 |

## 复核
十独点均有当日实拉来源；三点为增量合并（均含独有增量）、七点为新面；无纯重复。版本建议 3.61.0+。