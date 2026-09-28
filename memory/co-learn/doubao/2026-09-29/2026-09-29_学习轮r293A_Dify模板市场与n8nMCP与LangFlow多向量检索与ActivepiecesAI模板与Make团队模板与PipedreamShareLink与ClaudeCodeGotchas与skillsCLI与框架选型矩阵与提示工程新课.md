# r293A 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r292 全表。查询词与既往全表错开（本轮=工作流版本/模板市场、AI助手部署、RAG向量库、流程模板、场景模板、集成模板、Code技能最佳实践、skill安装教程、框架对比、提示工程课程）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | Creator Center & Template Marketplace（creator 发布模板+用户一键采用+Affiliate 分佣 5%）/ 声明式 JSON Schema 工作流引擎（可视化 DSL+AI 辅助生成+热重载） | 新面（r292C 插件治理之外的市场+引擎面） | 工作流 |
| 2 | n8n | n8n-MCP（MCP 服务器把节点知识注入 AI 上下文，3 部署：dashboard 免装 100 次/天免费/Docker/Railway/npx）/ Data Table memory by session ID（多会话长期记忆持久化） | 合并保留增量（r292B Agents/r292C 模板，本点=Data Table 记忆+n8n-MCP） | 工具 |
| 3 | LangFlow | 1.11.0 Multi-Vector Retrieval with NextPlaid（连接 NextPlaid server 做 ingestion/search+vLLM Multivector Embeddings 产生 ColBERT token-matrix embeddings）/ Chroma Cloud DB Providers / 全本地 RAG 模板（Ollama+ChromaDB） | 合并保留增量（r292B Memory Bases/DB Providers，本点=NextPlaid 多向量检索） | 工具 |
| 4 | Activepieces | AI 工作流模板库（CV Scanning/Newsletter Curation/Lead Nurturing/Airtable MCP 5 模板/Inbound Qualification 克隆即用） | 合并保留增量（r292A 触发器/r292C 嵌入，本点=模板内容面） | 工作流 |
| 5 | Make | 团队模板共享（Team templates tab）/ 危机管理分层路由模板（负关键词触发→情绪+紧急度评分→Critical/Medium/Low 三档分层响应） | 合并保留增量（r292A 错误语义/r292C 记忆，本点=团队模板+分层路由） | 工作流 |
| 6 | Pipedream | Workflow Share Link（分享唯一 key 含 triggers/steps/settings，私有资源需重连）/ 10,000+ tools across 3,000+ APIs / Pipedream MCP server（供 n8n 等集成） | 合并保留增量（r292B 组件契约/r292C Connect，本点=Share Link+MCP server） | 工具 |
| 7 | Claude Code | Gotchas 章节（技能最高信号内容，从常见失败点构建并随时间更新）/ 每阶段一技能选择标准（同阶段多技能让 Claude 犹豫）/ 无怜悯删减（已能做对的事删或转 hook） | 合并保留增量（r291A 注入/r292B SDK 模式，本点=Gotchas+每阶段一技能） | 可复用 Skill |
| 8 | skills.sh | CLI 参数面（-g 全局、-y 跳过确认、--skill 单装、@commit 钉版本、npx skills find 交互搜索）/ VSCode 扩展管理（侧边栏浏览/安装/启动/分享） | 合并保留增量（r292A 遥测，本点=CLI 参数+VSCode 扩展） | 可复用 Skill |
| 9 | GitHub | 框架选型矩阵（coding→Claude Code/MCP→Goose/沙箱→Codex CLI/多平台→OpenClaw）+ 快速推荐表（初学→Langflow/生产→LangGraph/多 agent→CrewAI/工作流→n8n） | 合并保留增量（r291B 沙箱/r292A 生态，本点=选型矩阵） | 工具 |
| 10 | deeplearning.ai | AI Prompting for Everyone（吴恩达新课：deep research 模式/pretrained knowledge vs web search 分界/AI critique 模块） | 合并保留增量（r291A 课程信号/r292A 四模式，本点=deep research+AI critique） | 可复用 Skill |

判重口径：增量判定。本轮 1 新面 + 9 合并保留增量（每点均含≥40% 独有增量），零纯重复。