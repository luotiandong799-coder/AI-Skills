# r295C 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r295B 全量 + WorkBuddy r294 续作（ede6bb1）。查询词与 r295A/B 全错开（本轮=知识库RAG/错误处理日志监控/知识库文档处理/AI agent构建步骤/AI场景模板用例/HTTP请求代码步骤/技能编写规范/生态安装配置/GitHub搜索AI仓库/课程最新九月）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | Agentic RAG（agent 迭代分析意图→改写查询→选工具/来源→评估证据→重试/回退）/ 多模态检索两段式（Embedding 首轮相似度+Reranking 精确相关性）/ 分块策略（自动/自定义 800-token+150 重叠/Parent-Child/Q&A pairs） | 合并保留增量（r292B Agentic 检索，本点=多模态+分块策略） | 工作流 |
| 2 | n8n | 错误分诊自动化闭环（Error Trigger 捕获→AI 分类+置信度+修复建议→去重 hash→Jira 查重→重试计数器≤3）/ Execution Data 节点打搜索元数据标签（user ID/entry point/outcome/session id）/ 可观测性告警（高延迟/token 超用/工具调用失败） | 合并保留增量（r294C 日志审计/r295A 重试，本点=AI 分诊+去重+标签过滤） | 工作流 |
| 3 | LangFlow | 知识库不随每次 flow run 重摄取（向量库持久化，Chroma 本地/Chroma Cloud/OpenSearch/pgvector）/ Docling 文件描述生成（子进程避免大文件内存压力）/ 1.11.0 NextPlaid 多向量检索（ColBERT late interaction+ColPali 视觉文档检索） | 合并保留增量（r295B 组件管控，本点=知识库+多向量检索） | 工具 |
| 4 | Activepieces | agent 构建三要素（Self-review 二次检查输出/记忆三分：短期·长期·用户/审批门：接触钱·客户·生产环境的步骤设审批）+agent 步骤放"思考"处动作后置保持输出可预测+测试样例集（low-fit/high-intent/"not now"查语气路由边界） | 合并保留增量（r295B MCP 生态，本点=agent 构建步骤面） | 工作流 |
| 5 | Make | Make AI Toolkit 内置模块免外部 API key（Categorize Text 全套餐可用）/ AI Playbook 88 用例（8 团队×AI 成熟度组织，每用例含问题/受众/影响/可部署场景）/ LLM 集成五步（连接→分类→验证输出→按类别路由） | 合并保留增量（r295A Maia/r295B webhook，本点=AI Toolkit+playbook） | 工具 |
| 6 | Pipedream | $.send.http() 无阻塞 destination（发完继续跑）/ connected account 认证（自动轮换 OAuth token）/ Python 代码步骤（requests，def handler(pd)） | 合并保留增量（r294C REST/r295A MCP，本点=send.http+Python 步骤） | 工具 |
| 7 | Agent Skills 编写 | frontmatter 硬约束（name≤64 小写连字符匹配目录名/description 1-1024 承载触发唯一机制含三层信息：功能+情境+价值/license SPDX/compatibility≤500/metadata 键值）/ 标准时间线（2025-10 Claude 特性→2025-12-18 agentskills.io 开放→2026 中 40+ 产品同格式）/ 简洁原则（只写模型缺乏的上下文+WHY 不只 WHAT） | 合并保留增量（r293C 编写/r294B，本点=spec 字段级约束+时间线） | 可复用 Skill |
| 8 | skills.sh 生态 | npx 免全局安装（总是最新版，按项目安全）/ external_dirs 共享技能目录配置（Hermes config.yaml 指向 ~/.agents/skills）/ 安装遥测排行榜（按装机量排名）/ @skill 精确+20-70+ agent 兼容 | 合并保留增量（r295B 51 agent 分发，本点=external_dirs+遥测榜） | 可复用 Skill |
| 9 | GitHub 搜索 | repomix 28.5K（整仓库打包单 AI 友好文件喂 LLM）/ herdr 40.9K（coding agents runtime，Rust）/ Bumblebee（Perplexity，扫描依赖与 MCP servers 供应链威胁）/ nanochat（Karpathy 最小可读 LLM 训练栈）/ archify 41.8K 图表技能（+25K/周） | 合并保留增量（r295B 仓库盘点，本点=工具面） | 工具 |
| 10 | deeplearning.ai | AI Code Review 新课（2026-09-14）/ Document AI: From OCR to Agentic Doc Extraction 新课 / AI Coding Workflows 2026-09-06（r293 已落）/ Multi AI Agent Systems with crewAI | 合并保留增量（r295B 新课面，本点=AI Code Review+Document AI） | 可复用 Skill |

判重口径：增量判定。本轮 10 合并保留增量，零纯重复。