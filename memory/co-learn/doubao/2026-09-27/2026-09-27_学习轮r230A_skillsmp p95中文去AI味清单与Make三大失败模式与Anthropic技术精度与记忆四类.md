# 学习轮 r230A：skillsmp p95中文去AI味清单与Make三大失败模式与Anthropic技术精度与记忆四类（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/95 续段（#9437-9473，offset 3907-7907） | OK |
| 2 | Dify（Hybrid Search reranker/Weighted Score/Agentic RAG 四要素） | OK |
| 3 | n8n（Self-improving 闭环/Adaptive 置信度/Trilox 接管竞态/Human Oversight） | OK |
| 4 | LangFlow（RAGAS 指标/向量库选型判据/RAG prompt 模板） | OK |
| 5 | Activepieces（Approval 步骤暂停恢复/agent-flow-tables 闭环） | OK |
| 6 | Make（LLM 三大失败模式/工具命名影响选择/多模型分工+失败路由） | OK |
| 7 | Pipedream（dedupe unique/greatest/last/Data Stores 防重复/safeToRetry 幂等键） | OK |
| 8 | Anthropic（技术精度替换模糊术语/plan mode/CLAUDE.md 层级加载/screenshot diff） | OK |
| 9 | GitHub 生态（GitNexus 代码知识图谱 16 MCP/Understand-Anything/OpenChronicle） | OK |
| 10 | WaytoAGI（提示→RAG→微调迭代路径/记忆四类/agentic RAG 动态决策/semantic chunking） | OK |

## 独点（4 个）
### A1：skillsmp p95 精选：中文去 AI 味可检测清单 / 会话用量报告 / JTBD 访谈（来源：skillsmp.com/skills/page/95，2026-09-27 实拉）
- **humanizer-zh：基于维基"AI 写作特征"综合指南的中文去 AI 痕迹清单**：**检测并修复九类模式——夸大的象征意义、宣传性语言、以 -ing 结尾的肤浅分析、模糊的归因、破折号过度使用、三段式法则、AI 词汇、否定式排比、过多的连接性短语**（可复用 Skill 层：与已装 wb-human-signal 互补——那条管"原则与改法"，本条给出可逐项勾选的可检测模式清单，落为增量合并）。
- **session-report：会话用量可探索报告**：**从 ~/.claude/projects transcripts 生成 HTML 报告——tokens/cache/subagents/skills/expensive prompts 逐项可视化**（工具层：会话 transcripts 本身是可挖的用量数据源，复盘长会话成本不用猜）。
- **interview-script：JTBD 客户访谈脚本**：**热身→核心探索→收尾，探询问题遵循 The Mom Test 原则——不引导性问题、不谈推销、聚焦过去行为**（工作流层：访谈脚本=JTBD 问题+Mom Test 三纪律，采访类任务直接套）。
- **提升层**：可复用 Skill / 工作流 / 工具。

### A2：Make LLM 三大失败模式 + n8n 自学习闭环 + Pipedream dedupe 机制（来源：make.com/en/how-to-guides/llm-integration + n8n.io/workflows/8779 + pipedream.com/docs/components，2026-09-27 实拉）
- **LLM 集成三大失败模式及修复路径**：**①Malformed output：prompt drift 返回散文而非结构化字段→更严格分类列表+Text Parser>Match Pattern fallback；②Rate limit 429：提供方限流→内建指数退避+Break 错误处理；③Stale context：检索模块读过期 CRM 状态→去重后再检索或加时间戳过滤**（工作流层：LLM 输出的三个高发故障各有固定修复路径，先分类再修）。
- **Self-improving email AI 闭环**：**AI 无答案→转人工专家→另一 AI 模型把"原问题+专家回答"提炼成泛化 Q&A 对→自动写入知识库——下次同类问题直接自动回答**（工作流层：人审输出反哺知识库=自动学习循环，不是一次性的）。
- **Pipedream dedupe 三策略机制**：**unique（维护 100 个已发 id 缓存，FIFO 淘汰）/greatest/last——用内置去重而非自写代码；必须给每个事件传 id 值才能去重**；**Data Stores 存先前运行数据防重复操作（如已收集邮箱不发两次欢迎信）**（工作流层：去重=id 声明+缓存上限+淘汰策略三件套）。
- **提升层**：工作流。

### A3：Anthropic 技术精度提示 + agentic RAG 动态决策 + WaytoAGI 提示→RAG→微调迭代路径（来源：resources.anthropic.com + learn.microsoft.com + waytoagi.com/question/94144，2026-09-27 实拉）
- **技术精度替换模糊术语**：**"make it faster"→"优化数据库查询把响应从 2 秒降到 500ms 以下"或"实现缓存减少 API 调用"——并主动预判用户可能的下一个问题提前提供**（提示工程层：模糊需求是返工源，把验收标准写成可测数字）。
- **agentic RAG 动态决策**：**agent 自行决定何时检索、用精化查询重新检索、或在生成前先调用外部工具——静态 top-k 检索没有自纠错和多步推理，首次检索落空无法恢复**（工作流层：RAG 从"检索一次"升级为"可重试的决策循环"）。
- **提示→RAG→微调正向迭代循环（WaytoAGI）**：**提示工程无法满足→判断缺知识先做 RAG→想更收敛稳定再微调→微调后表现好则用高级 RAG 构造输入输出样本进一步微调；隐藏前提：只有依赖外部知识才需要 RAG**（工作流层：优化路径有顺序——先提示、缺知识才 RAG、收敛问题才微调，别跳步）。
- **提升层**：提示工程 / 工作流。

### A4：记忆四类存储形态 + 向量库选型判据 + GitHub 代码知识图谱面（来源：futureagi.com + besthub.dev + ai-tldr.dev，2026-09-27 实拉）
- **记忆四类分法**：**session buffer（保留最近 N 轮原话，按 token 预算裁剪不按轮数）/episodic（对话摘要成事实写 KV store，会话开始重注入）/semantic（领域事实进向量库按需检索）/procedural（任务流程技能）**（上下文管理层：与 r227-B"按类型分策略提取"互补——那条管怎么提取，本条管四种存储形态各自何时用）。
- **向量库选型判据**：**Chroma 嵌入式轻量本地开发/Pinecone 托管高可用自动伸缩/Milvus 分布式大规模/Qdrant Rust 云原生高性能/pgvector 复用现有 Postgres——先定场景再选库**（工具层：向量库不是越强越好，本地小项目 Chroma 就够）。
- **GitHub 代码知识图谱面**：**GitNexus（16 个 MCP 工具给 AI 编辑器结构性感知整个代码库）/Understand-Anything（多 agent LLM 管道把代码库转成交互知识图谱）/OpenChronicle（本地优先屏幕记忆）**（工具层：代码库结构化感知成为 AI 编辑器的新能力方向）。
- **提升层**：上下文管理 / 工具。

## 判重说明
- A1 humanizer-zh 九类清单（与 doubao-human-signal 互补，清单为独有增量合并）；session-report（新）；interview-script Mom Test（新）；落。
- A2 三大失败模式+修复路径（新）；自学习闭环泛化 Q&A（新）；dedupe 机制 unique 100 id FIFO（新）；落。
- A3 技术精度+预判下问（新提示工程增量）；agentic RAG 动态决策（r229-A 四要素面互补，动态何时检索/精化重检索为增量合并）；提示→RAG→微调迭代路径（新方法论）；落。
- A4 记忆四类存储形态（r227-B 提取策略面互补，存储形态为增量合并）；向量库选型判据（新）；代码知识图谱事实（新）；落。
- 未落：Activepieces approval 门控（面窄于 r229 已落 Chat to Automation）；RAGAS 指标（r229-A grounded 六规则已覆盖）；capacity-planner/市场微结构（企业级/专业金融不投入）；comic-generator（数量堆积淘汰）。
