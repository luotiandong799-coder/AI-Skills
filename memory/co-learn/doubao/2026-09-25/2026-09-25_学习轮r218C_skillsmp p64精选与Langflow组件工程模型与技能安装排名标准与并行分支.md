# 学习轮 r218C：skillsmp p64精选与Langflow组件工程模型与技能安装排名标准与并行分支（2026-09-25）

## 实拉记录（10 次调用，5 成功 / 5 失败计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/63 | 抓取失败（计 1 次） |
| 2 | dify.ai/blog 续读（123288-127723） | OK（v0.8 Parallel Branch/o1 集成） |
| 3 | www.langflow.org/ 续读（4240-8406） | OK（AgentComponent 组件工程模型） |
| 4 | docs.n8n.io/how-memory-works.md | security strategy 拦截（计 1 次） |
| 5 | GitHub Trending 搜索（openagentskill official/aibestskill/agskills） | OK（npx skills add/anthropics 官方库） |
| 6 | deeplearning.ai/the-batch/ | security strategy 拦截（累积 6 次） |
| 7 | docs.openclaw.ai/concepts/standing-orders | 死链 |
| 8 | activepieces.com/docs/security/overview | 死链（activepieces 累积 3 次） |
| 9 | skillsmp.com/skills/page/64（#6301-6355，5927/11677 取） | OK |
| 10 | docs.n8n.io/agents-vs-chains.md（4986/5628） | OK（chain 无 memory/tools） |

## 独点（4 个）
### C1：skillsmp p64 精选：主张验证四链 / 双模式验证门 / 文档强制咨询 / Wikipedia AI 写作模式（来源：skillsmp.com/skills/page/64，2026-09-25 实拉）
- **academic-verify（garrytan/gbrain ★30,213）**：**研究主张/学术引文验证四链——publication→methodology→raw data→independent replication**；路由 perplexity-research 真实网络查证，格式化为 citation-checked brain page。
- **citation-check-skill（serenakeyitan ★246）**：**视觉增强验证门+网页搜索——两模式：search mode 对照权威在线来源 / doc-only mode 一切追溯所提供文档（无外部知识）**；验证图表/表格准确性、审计 AI 生成内容。
- **claude-mega-brain（guhcostan ★126）**：**OKF 知识导航——session 出现 `<mega-brain>` 块时必须先查项目文档再答数据/schema/metrics/API 问题；不确定时直接读文件**（项目文档强制咨询机制）。
- **writing-anti-ai（Galaxy-Dawn/claude-scholar ★5,594）**：**基于 Wikipedia「Signs of AI writing」指南**——检测修复 inflated symbolism、promotional language、superficial -ing analyses、vague attributions、AI vocabulary、negative parallelisms、excessive conjunctive phrases（英文去 AI 味模式清单）。
- **harness（revfactory ★9,045）**：**元技能——构建 harness：定义专家 agent + 创建该 agent 使用的技能**（agent-技能配对的元层工程）。
- **ecommerce-seo（nowork-studio ★3,820）**：电商 SEO 审计——**faceted navigation 的 crawl-budget/duplicate-content 陷阱、canonical for variants、out-of-stock 处理、Product/Offer/Review/AggregateRating/BreadcrumbList 结构化数据**。
- **提升层**：工作流 / 可复用 Skill。

### C2：Langflow 组件工程模型：Python 类声明组件（来源：www.langflow.org/ 续读，2026-09-25 实拉）
- **组件=Python 类**：`class AgentComponent(AgentComponent)`——类属性 display_name/icon/beta/name + `inputs` 列表声明（MultilineInput role / HandleInput llm / HandleInput tools / DataInput input_message+chat_history）。
- **runnable 方法契约**：`create_agent_runnable()`——先校验（"Prompt must contain input"）、再构建 messages 列表（system prompt / `("placeholder","{chat_history}")` / HumanMessagePromptTemplate / `("placeholder","{agent_scratchpad}")`）。
- **Drag. Drop. Deploy**：视觉状态流+可复用组件+快速迭代；**Python under the hood——用 Python 定制一切**（低代码与代码同源）。
- **提升层**：工具（低代码平台组件工程）。

### C3：GitHub 技能生态：npx skills add 标准安装 / 双信号排名（来源：GitHub Trending 搜索，2026-09-25 实拉）
- **标准安装 CLI**：`npx skills add openai/skills --skill figma-implement-design`——**按 repo+skill 名精确安装**；openai/skills 4 skills/180K★（figma-implement-design=Figma 设计转生产级 UI 代码）。
- **anthropics/skills=官方生态标杆**（60.9k+★）——Claude Skills 体系源头、生产级技能集合；agskills.dev featured：obra/superpowers（agentic skills framework & software development methodology）。
- **aibestskill.com 排名信号=stars+measured growth+maintenance 双维**（approved shortlist 24 个/1.8m★/+30k★/周）；detail 页显示 **SKILL.md proof、来源摘录、安装说明、邻近替代**。
- **提升层**：可复用 Skill（技能分发与选择标准）。

### C4：Dify Parallel Branch 并行分支 + n8n agents-vs-chains 差异（来源：dify.ai/blog v0.8.0 + docs.n8n.io agents-vs-chains.md，2026-09-25 实拉）
- **Dify v0.8.0 Parallel Branch**：工作流并行处理——**多个分支同时运行、并行执行各种任务，显著提升执行效率**（start→3 并行块→end）。
- **n8n chain vs agent**：**Basic LLM Chain 不支持 memory 或 tools**；Agent 节点与工作流其他组件交互并决策用什么工具；**memory 让 agent 访问此前对话部分**——agent 强于 chain 的关键两点（工具+记忆）。
- **提升层**：工作流（并行与 agent/chain 选型）。

## 判重说明
- C1 全新（p64 独有），落。
- C2 langflow 增量（组件工程页，补 r217A 存储架构面），落。
- C3 trending 增量（安装 CLI+排名标准新点），落。
- C4 dify+n8n 增量（Parallel Branch+agents-vs-chains 新页），落。
- 未落：deeplearning the-batch（security 拦截）、openclaw standing-orders/activepieces security（死链）、skillsmp p63（抓取失败）。
