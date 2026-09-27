# 学习轮 r231A：skillsmp p96委派判据与Activepieces原子化工具与Anthropic技能写作十项与agentic RAG自检（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/96（#9539-9575，p96 offset 4000-7894） | OK |
| 2 | Dify（Knowledge Retrieval 双层架构/多模态知识库/Hybrid 权重滑块/chunk 推荐值） | OK |
| 3 | n8n（Enrichment 异步元数据流水线/chat memory 多轮/Wait 限速） | OK |
| 4 | LangFlow（Assistant 1.10 自然语言建 flow/Workflow API 三模式/Load Data 与 Retriever 子流程分离） | OK |
| 5 | Activepieces（AI Metadata atomic over composite/Selective Exposure/throttling/dropdown 缓存） | OK |
| 6 | Make（Rollback 默认行为/Commit/Scenario recovery blueprint/Incomplete executions） | OK |
| 7 | Pipedream（dedupe unique/greatest 策略/自然键指纹模式/幂等反模式清单） | OK |
| 8 | Anthropic（Skill authoring best practices 十项清单/三级披露/上下文公共品） | OK |
| 9 | GitHub 生态（Agent 技能化持续/AgentConn 排名/openagentskill 平台） | OK |
| 10 | WaytoAGI（RAG 提示词优化路径/agentic RAG 自检/RAG as tool） | OK |

## 独点（4 个）
### A1：skillsmp p96：委派判据 + 桌面操作 CLI 纪律 + 引用转设计交接（来源：skillsmp.com/skills/page/96 #9559/9560/9546，2026-09-27 实拉）
- **cavecrew 委派判据**：**investigator=找代码 / builder=1-2 文件小编辑 / reviewer=diff 审查；他们的输出被压缩，所以主上下文撑得更久**（工作流层：委派给子代理不只是分工，输出压缩本身在省主上下文——把"谁干"和"输出多小"一起选）。
- **agent-computer-use CLI 纪律**：**桌面操作一律 agent-cu（open/snapshot/click/type/key/find/scroll/drag/batch/wait-for）——能读回状态、能验证；禁止 osascript/xdotool 等 shell 绕行，它们读不回状态、不验证、跨应用更新脆弱**（工具层：GUI 自动化选"能回读状态"的通道，回读=可验证的前提）。
- **reference-design-contract**：**把模糊品味/截图/URL/产品笔记转成 grounded DESIGN.md + 实现交接（可复用视觉方向而非一次性 prompt），用在原型/重设计/图像重混之前**（工作流层：先落"方向文档"再动手，视觉工作同样需要规约先行）。
- **提升层**：工作流 / 工具。

### A2：Activepieces 原子化 action + Dify 双层检索 + n8n 元数据增强检索（来源：activepieces.com/docs/build-pieces/piece-reference/ai-metadata + deepwiki.com/langgenius/dify-docs/8.7 + n8n.io/workflows/8008，2026-09-27 实拉）
- **atomic over composite：给 agent 的 action 要原子化**：**一个 action 映射一个能力、显式输入；agent 自己组合多步（Create Task 优于 Create Task and Notify）；配输出 schema 描述输出；description 字段变成 MCP 工具描述**（工具层：agent 工具设计=能力最小单元+清晰 schema，组合留给 agent 而非预拌）。
- **throttling + dropdown 缓存**：**piece 定义内限流防止 agent 淹没 API；动态 dropdown 选项缓存 5-10 分钟降延迟**（工具层：为 agent 设计的 API 要考虑 agent 的调用频率，限流进定义不靠外部）。
- **Dify Knowledge Retrieval 双层架构**：**KB 级设置定初始检索策略与候选池；节点级设置通过 reranking/filtering 精化结果（node result 带元数据+图片附件注入 LLM 上下文）；Hybrid Search 权重滑块调 vector vs keyword 比例**（工作流层：检索分两级——先扩候选再精化，节点输出可注入；权重可调比固定模式稳）。
- **n8n Enrichment 异步流水线**：**定时任务拉新 chunk → LLM 生成元数据（topics/use_case/risks/audience_level/summary）→ 写回向量库改进检索与过滤**（工作流层：检索质量提升不靠换 embedding，靠给 chunk 加结构化元数据让过滤有抓手）。
- **提升层**：工具 / 工作流。

### A3：Anthropic Skill authoring 官方十项清单 + 上下文公共品（来源：console.anthropic.com/docs/en/agents-and-tools/agent-skills/best-practices + skillmd.io，2026-09-27 实拉）
- **十项 checklist**：**description 具体含关键词 + 写明做什么与何时用 / SKILL.md body <500 行 / 附加细节放独立文件 / 无时效信息 / 术语一致 / 示例具体不抽象 / 引用一层深 / progressive disclosure 恰当 / 工作流步骤清晰**（可复用 Skill 层：技能质量有官方可勾选清单，写后逐项自查）。
- **三级披露量化**：**metadata（name+description）常驻约 100 词 → SKILL.md body 触发时 <5k 词 → bundled resources 按需（脚本执行不占上下文窗口）**（可复用 Skill 层：把长内容下沉到可执行资源，脚本能跑就不必读进窗口）。
- **上下文是公共品**：**每段内容写前挑战三问——Claude 真需要这条吗 / 训练里已有吗 / 这段话值它的 token 成本吗；30 个技能=30 个名字+30 条短描述，够 Claude 决定用哪个**（可复用 Skill 层：技能描述层的 token 预算意识，与 wb-max-token-saver 面互补——这问的是"技能本身怎么写得省"）。
- **提升层**：可复用 Skill。

### A4：agentic RAG 自检指令 + RAG as tool + 检索优化路径（来源：dzone.com/articles/building-agentic-rag + zyvop.com + articles.waytoagi.com，2026-09-27 实拉）
- **自检减少静默幻觉**：**合成阶段显式要求模型 flag contradictions 与 insufficiency（证据矛盾/证据不足都要标出），"这比提示工程里几乎任何其他改动都更能压幻觉"；返回前加一遍廉价自检——合成是否偏离了检索证据**（模型层：把"发现矛盾与不足"写进指令=把幻觉从静默变可见；自检放最后一步成本低收益高）。
- **RAG as tool**：**知识库暴露成 agent 可选工具而非每次查询都检索——agent 判断何时需要检索**（工作流层：RAG 不是固定流水线而是工具选择，与 agentic RAG 动态决策同源）。
- **优化路径**：**prompt 先跑通 → 指令遵循不足就加强约束/提示词太长就精简 → 缺知识才做 RAG → RAG 后要收敛就微调**（工作流层：迭代路径的先后顺序本身就是方法——不要一上来就 RAG/微调）。
- **提升层**：模型 / 工作流。

## 判重说明
- A1 委派输出压缩面（新，与 r229-C subagent 面互补）；agent-cu 回读纪律（新）；引用转设计（新）；落。
- A2 atomic action（r230-C Make 工具命名面互补增量）；throttling/缓存（新）；双层检索（r230-A hybrid 面增量——两层级+权重滑块）；Enrichment 元数据（新）；落。
- A3 十项 checklist（r230-B Gotchas 面互补增量——官方清单）；三级披露量化（新细节）；上下文公共品（新）；落。
- A4 自检指令（r230-A agentic RAG 面增量——具体指令与成本论）；RAG as tool（新）；优化路径（r230-A 提示→RAG→微调面重叠，但"先精简提示词再加强约束"为增量，合并保留）；落。
- 未落：Make Rollback 默认行为（r230-B 已落事务边界）；Pipedream dedupe（r230-A 已落）；LangFlow Assistant 自然语言建 flow（面窄无方法论增量）；geo-audit/presentation-designer（面窄）；GitHub 趋势新闻（无增量）。
