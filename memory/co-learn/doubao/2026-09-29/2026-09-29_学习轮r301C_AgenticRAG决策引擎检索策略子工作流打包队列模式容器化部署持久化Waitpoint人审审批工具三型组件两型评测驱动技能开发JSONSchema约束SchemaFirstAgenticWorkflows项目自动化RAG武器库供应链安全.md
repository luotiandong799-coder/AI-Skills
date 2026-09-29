# r301C 学习轮（2026-09-29，第 3 组十站全量实拉→十独点）

判重基线：r284~r301B。查询词与 r291~r301B 全错开（本轮=Agentic RAG决策引擎与检索策略/子工作流打包与队列模式/容器化部署/持久化Waitpoint与人审审批/AI Agent工具三型/组件两型与Connect网关/评测驱动技能开发/JSON Schema约束与Schema-First/Agentic Workflows与项目自动化/RAG武器库与技能供应链安全主题）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | Agent Node=中央决策引擎（意图分析+工具编排+源选择+重试逻辑，封装全部 agent 行为）；三检索策略=Vector（语义相似）/Full-Text（精确关键词技术术语）/Hybrid（最高准确率）；自定义分块策略+per-dataset score 阈值微调；RAG 管道=parse→chunk→embed→index；Agentic RAG 模板=Agent 检查问题→选行动（向量库/网络搜索）→摘要引用 | 合并保留增量（r300B 多向量检索，本点=Agent Node+三检索策略） | 工作流 |
| 2 | n8n | 子工作流打包为工具=Call n8n Workflow Tool（独立 trigger+逻辑+输出，父 agent 当工具调用）；Queue mode=Redis 队列+worker 进程并发，触发→job 入队→worker 拉取独立执行，无执行丢失；批处理五段=Prepare→Split In Batches→Process per batch→Accumulate→Aggregate；并行 fan-out=小模型路由/分类，贵模型核心推理 | 合并保留增量（r301A 队列限制，本点=子工作流打包+批处理五段） | 工作流 |
| 3 | Langflow | 容器化部署=langflowai/langflow 基础镜像+flows 目录+持久卷（升级只换容器镜像不丢数据）；生产模式=EKS 无状态 API 驱动微服务+Vault 密钥+Prisma AIRS；Redis-backed job queue（1.10+ 跨 worker 共享构建事件）+Helm 横向扩展；观测=LangSmith/LangFuse | 合并保留增量（r301A scaffold，本点=部署面） | 工具 |
| 4 | Activepieces | Waitpoint=durable 行代表暂停步骤（flow run 只有状态 PAUSED/RUNNING，why 在 waitpoint 上）；Barrier=暂停直到 N 个事物报告（Process in Batches 派发的批次）；Todos=原生 human-in-the-loop（agent/flow 暂停请求人工审批或输入，续行或中止）；多级审批链=分支/循环/条件按 spend/risk/department 路由，拒绝循环回编辑重提 | 合并保留增量（r301B Waitpoint，本点=durable 行+Barrier+审批链） | 工具 |
| 5 | Make | AI Agent 工具三型=模块（Gmail Send email）/场景（Scenarios>Call a scenario module）/MCP（MCP Client>MCP Tools 模块）；多模型路由=便宜模型分类+贵模型起草（Router 后两个 Chat Completion）；AI Toolkit=Analyze sentiment/AI Classifier/AI Text Generator；Simple Text Prompt=零设置 AI 模块 | 合并保留增量（r301B Router，本点=工具三型+AI Toolkit） | 工具 |
| 6 | Pipedream | 组件两型=sources（独立资源/工作流触发器/serverless 函数，props 接受输入，HTTP/定时/cron/手动触发）+actions（输入参数→结果）；Connect=集成基础设施（managed auth+10000+ 预建工具触发器+raw proxy）；Conduit=员工安全连接网关（SSO+访问策略+per-user 权限+审计）；组件生命周期 deactivate hook（更新/删除时调用） | 合并保留增量（r301B 重试重放，本点=组件两型+Connect 网关） | 工具 |
| 7 | Anthropic | 评测驱动开发=先评测后构建（代表任务跑找 gap 再增量建技能）；迭代信号=under-triggering（不加载/手动启用→加描述关键词）+over-triggering（无关加载/禁用→加负面触发词）+execution issues；Gotchas 章节=技能最高信号内容（常见失败点累积）；Skill-Creator=官方 meta-skill（创建/测试/优化其他技能，内置评测框架+盲测对比） | 合并保留增量（r301A 技能验证清单，本点=评测驱动+迭代信号） | 可复用 Skill |
| 8 | 提示工程 | JSON Schema 三键=required（必填字段）/additionalProperties:false（禁模型发明额外字段）/enum（固定值集合比自由文本可靠）；Schema-First=任务描述前先定义确切 schema（模型知道输出形状优于生成时推断）；Structured Outputs 原生=output_config.format {type:json_schema}+forced tool use 可移植替代；规则=未提及字段→null（不是猜测）+键跨版本稳定 | 合并保留增量（r300B Strict 语法，本点=schema 三键+Schema-First） | 可复用 Skill |
| 9 | GitHub | Agentic Workflows=Markdown 描述期望结果→coding agent 在 Actions 执行（标准 workflow+沙箱/权限/控制/审查 guardrails）；项目自动化=GraphQL API+Actions 自动加 PR 到项目（ready for review→Task+Status+日期字段）；五工作流=create-branch（Issue labeled）/ci-tests/代码审查 agent/update-project；GitHub MCP Search Toolset=search_commits 直接搜索提交 | 合并保留增量（r301A Actions 安全，本点=Agentic Workflows+项目自动化） | 工作流 |
| 10 | deeplearning | RAG 武器库=混合检索（BM25 关键词+语义，40%/60% 权重）+RRF 融合+重排（cross-encoder 逐对打分重排 TopK）+Parent Document 两阶段（小 chunk 搜索精度+父文档上下文）+Graph RAG 兜底（向量 RAG 全局问题失败后跑）；ToxicSkills=13.4% 技能含严重安全问题（534 个，恶意分发/提示注入/暴露密钥）/36.82% 任意级别缺陷（1467 个），私有注册表防御（镜像+审查后提升+只从私有源安装），扫描器失效（混淆/归档字节码隐藏 payload）；AI 记忆层=agentmemory 28.9k/TencentDB Team Memory 20k/Letta LoCoMo 74%/vLLM Fast Start（GPU 常驻后量化权重重启免重载） | 合并保留增量（r300A 亲子检索+r300B 自适应 Chunk，本点=RRF+Graph RAG+供应链安全） | 工作流 |

判重口径：增量判定。10 独点全为合并保留增量（各有≥40% 独有增量），零纯重复零编造。