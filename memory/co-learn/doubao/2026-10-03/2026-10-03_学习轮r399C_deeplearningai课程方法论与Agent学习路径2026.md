# 2026-10-03 学习轮 r399C：deeplearning.ai 课程方法论与 Agent 学习路径 2026

轮次：r399C（批 r399 第 3 轮）
判重：双键 grep KB 4372 行 → 历史已有规划反思（r345A/r394A）、评估驱动（r390C/r397B）、Skills 规范（r399A）；本批增量在**课程体系的方法论结构**（四大 agentic 设计模式一体框架+自主度分级/convergence score 收敛指标/spec-first 三层开发范式/Harness Engineering 第三代方法论/课程新鲜度评估），净增 5 独点。
实拉：3 query（corporate-deeplearning-agentic-ai/learn-deeplearning-agentic-ai/learn-deeplearning-autogen-patterns/corporate-deeplearning-autogen/community-deeplearning-spec-first/learn-deeplearning-crewai/arxiv-patterns-catalogue/corporate-deeplearning-evaluating-agents/learn-deeplearning-mcp-course/dev-deeplearning-courses/pythonandr-course-verdict/aidoers-agentic-three-blocks/learnbysource-agentic-ai/techfuturism-agentic-ng/aiwiki-andrew-ng/agentskillsdev-harness-engineering/community-deeplearning-practice），逐站带来源标识。

## 落地 5 独点（每点标注提升层）

### 1. Agentic 设计模式四件套 + 自主度分级 + 先原理后框架（工作流）
来源：corporate-deeplearning-agentic-ai / learn-deeplearning-agentic-ai / learn-deeplearning-autogen-patterns / learnbysource-agentic-ai / community-deeplearning-practice
- **四大模式一体框架**：Reflection（AI 批评自己输出并迭代改进=自动化的 code review；**用外部反馈**评估反射影响）/ Tool Use（连数据库/API/外部服务真正执行动作，不只看生成文本）/ Planning（复杂任务分解为可执行步骤并适配意外）/ Multi-Agent（协调多个专用系统处理复杂工作流不同部分）。
- **Tool use 两态**：有预定义函数→把函数交给 agent 用；没有预定义函数→**让 agent 写它需要的代码，检查正确性后执行**（code execution）。
- **自主度分级（degrees of autonomy）**：从单步生成到多步自主动作的谱系——先定自主度再选架构；任务分解=识别工作流中的步骤。
- **先原理后框架**：用 Python 从第一性原理构建四大模式，再叠加 AutoGen/CrewAI 等框架——理解底层机制后才用框架（框架只是加速器不是替代理解）。
- **练习方法**：改工具看 agent 如何选（tool use）/查 agent 如何存历史交互（memory）/找 Self-Correction 步骤（reflection）——跑 agent 时用这三处可视化理解。
- 判据：搭 agent 先按四模式拆解需求（哪个模式解决哪部分），定自主度，先裸实现再叠框架。

### 2. 评估组件化 + convergence score 收敛分数（工作流/可复用 Skill）
来源：corporate-deeplearning-evaluating-agents / learn-deeplearning-agentic-ai-module4
- **per-component 评估器选型**：为 agent **每个组件**（skills/router 决策等）选合适评估器——code-based / LLM-as-a-Judge / human annotations 三类，按组件特性选。
- **从 traces 建测试集**：从收集的运行轨迹（traces）创建测试示例，并为 LLM-as-judge 准备详细 prompt——评估集来自真实运行而非人工编造。
- **convergence score（收敛分数）**：评估示例 agent 能否在**高效步数内**响应查询——不只测正确率，还测是否"几步就走完"，是效率维度的评估指标。
- **结构化评估流程**：组件级评估+错误分析（error analysis）定优先级——先找最大错误源再修，不平均用力。
- 判据：agent 评估三件套=组件级评估器选型+traces 测试集+收敛分数（正确+效率双维度）。

### 3. spec-first 三层开发范式：spec 是大脑、agent 是肌肉（工作流）
来源：community-deeplearning-spec-first / aidoers-agentic-three-blocks
- **替代 vibe coding**（prompt→hope→fix→repeat）：先写**规格**——spec 是"大脑"，agent 是"肌肉"；vibe coding 不 scale，spec 创建**持久工件**：跨上下文窗口重置存活、降低认知负荷。
- **三层结构**：Constitution（项目级）/ Feature specs（特性级）/ Replanning（特性之间）——你当建筑师拿蓝图，agent 当施工方。
- **执行要点**：三个文件与 agent 在对话中一起写；**每个步骤在新 agent 上下文发生**；遵循开放标准（AGENTS.md 类项目指令文件）。
- 判据：agent 编码任务先 spec 后 code——项目级 Constitution+特性级 specs+特性间 replanning；spec 是唯一权威（跨上下文存活），agent 只是执行器。

### 4. Harness Engineering：第三代 AI 工程方法论（可复用 Skill/工作流）
来源：agentskillsdev-harness-engineering / aiwiki-andrew-ng
- **三代演进**：Prompt Engineering →（第二代）→ **Harness Engineering（2026 第三代）**——从"写好提示词"升级到"搭好整套 harness"：可复用 Skills + MCP + Subagents 组合构建复杂工作流。
- **Agent Skills with Anthropic 课程范式**（吴恩达×Anthropic，Elie Schoppik 主讲）：创建可复用 Skills，结合 MCP 与 Subagents，覆盖 **Claude.ai / Claude Code / Claude API / Agent SDK 全平台**——同一技能四端复用。
- 判据：2026 起做 AI 工程按 harness 思维：技能（可复用指令包）+ 连接（MCP 工具数据）+ 分工（subagents 专职）三层搭，不单靠 prompt 文本。

### 5. 2026 课程地图与新鲜度评估（工作流）
来源：dev-deeplearning-courses / pythonandr-course-verdict / learn-deeplearning-mcp-course
- **2026 值得学的新课**：MCP: Build Rich-Context AI Apps with Anthropic（建 MCP Server/Client+Prompt/Resource 特性+远程部署）/ Gemini CLI（开源 agentic coding assistant，命令行协调本地工具与云服务）/ DSPy: Build and Optimize Agentic Apps（Databricks）/ Long-Term Agentic Memory（LangChain）/ Llama 4（多模态长上下文）/ Claude Code 课程。
- **课程新鲜度评估体系**（verdict 表）：按发布年龄+概念耐久度分级——`redundant → drop`（内容过时或被覆盖）、`concept-durable → keep`（概念耐久值得学）、`fresh`（新出）、`fine`（可用）——学习型任务先过 verdict 再投入时间。
- 判据：选课先查 verdict（年龄+概念耐久），redundant 的课不学、concept-durable 的课滚动保留——与"滚动学习历史优质内容"偏好同源。

