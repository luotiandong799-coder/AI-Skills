# 学习轮 r229B：skillsmp p94知识合成与预算告警阶梯与Dify变量聚合器与Anthropic containment五层（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/94（#9301-9340，total_length=11271 首段 4000） | OK |
| 2 | Dify（Knowledge Retrieval 最佳实践/Variable Aggregator/error_strategy fail-branch） | OK |
| 3 | n8n（sub-workflow vs AI Agent Tool/gatekeeper/Error Trigger 独立错误工作流） | OK |
| 4 | LangFlow（traces 1.8 调试/knowledge bases 本地向量库/Mustache 模板） | OK |
| 5 | Activepieces（audit logs 审计流/data masking/Event Streaming 事件转发/Tables 状态存储） | OK |
| 6 | Make（五种错误处理指令/Router 条件分支/incomplete executions 重试语义） | OK |
| 7 | Pipedream（Connect 组件/10,000+ 预建工具/deduping 策略） | OK |
| 8 | Anthropic（containment 边界强制/auto mode 五层安全/harness 三 pattern） | OK |
| 9 | GitHub 生态（trending：paperclip/jev-ultrafast +20,120/day/open-code-review ★41,206） | OK |
| 10 | WaytoAGI（Skills 蓝皮书/Agent Skills arXiv 论文/组织级 skill 部署） | OK |

## 独点（4 个）
### B1：skillsmp p94 精选：知识合成置信度 / 预算告警阶梯 / 检索五项组合（来源：skillsmp.com/skills/page/94，2026-09-27 实拉）
- **knowledge-synthesis：多源结果合成（anthropics/knowledge-work-plugins ★25,304）**：**把多来源搜索结果合并成连贯、去重、带来源归属的答案——置信度基于时效性（freshness）和权威性（authority）打分，并有效汇总大结果集**（工具层：合成不是拼接，置信度=新鲜度×权威度）。
- **cost-budget-check：预算利用率告警阶梯（ruvnet/ruflo ★73,010）**：**读累计成本追踪+预算配置→计算利用率→发出 50/75/90/100% 四级告警阶梯**（工具层：成本控制=利用率分级告警，不是一次性红线）。
- **memory-search：SOTA 语义检索五项组合（ruvnet/ruflo ★73,010）**：**hybrid（sparse+dense）+ Graph RAG multi-hop + MMR diversity reranking + recency weighting——检索质量是多机制组合不是单一向量**（RAG 层：五项组合器可逐项开关）。
- **academic-figure-generation：论文图五 agent 管线（jxtse/scientific-research-skills ★70）**：**从论文方法文本+目标 caption 生成出版级学术图——本地 PaperBanana 多 agent 流水线：Retriever→Planner→Stylist→Visualizer→Critic**（工作流层：图生成也是分角色流水线+末尾批评家把关）。
- **提升层**：工具 / RAG / 工作流。

### B2：Dify 变量聚合器防静默 null + Make 五种错误指令 + 门卫 agent（来源：dify-6c0370d8.mintlify.app + academy-content.make.com + smartprocessflow.com + blog.n8n.io，2026-09-27 实拉）
- **Variable Aggregator：互斥分支汇合**：**If/Else 和 Question Classifier 只执行一支——分支后节点不会自动拿到另一支声明的变量，会静默收到 null；用聚合器把互斥分支输出收敛成单一变量，下游只定义一次处理；array 模式收集所有分支输出成列表再进 Code 节点**（工作流层：分支汇合是静默丢变量的高发坑，必须显式聚合）。
- **Make 五种错误处理指令**：**Resume（忽略错误继续下一项）/ Ignore（跳过该记录）/ Break（停止场景）/ Commit（处理所有成功项、停在首个错误）/ Rollback（撤销本次运行所有更改——数据库原子操作用）；错误处理路由可连接到任意模块，仅在该模块出错时运行**（工作流层：错误处理是路由不是设置，五种语义按场景选）。
- **incomplete executions 重试语义**：**重试从"引发错误的模块"开始、用原始输入——但运行可能被重排（reordered），不能假设重试幂等；DLQ 策略：Ignore 指令丢弃失败 bundle 并把执行状态置 Success，立即释放调度器取下一个 webhook，绕过全局场景暂停**（工作流层：重试不是无副作用操作，队列阻塞时用 Ignore 释放）。
- **n8n gatekeeper 门卫 agent**：**按意图或复杂度路由：简单请求直接处理，复杂委托专家 sub-agent——Hierarchical coordination 层级协调**（编排层：门卫=快路径+慢路径分流，与 WB Fast/Deep 同构）。
- **提升层**：工作流 / 编排。

### B3：Anthropic containment 边界强制 + auto mode 五层安全 + sub-workflow 判据（来源：anthropic.com/engineering + 01.me + blog.n8n.io + slowhifi.com，2026-09-27 实拉）
- **containment：监督"能做什么"而非"做什么"**：**限制 blast radius 的第二种方法=边界强制——通过 sandbox/VM/egress controls 强制访问边界，而不是监督 agent 的动作；Anthropic 投入最多、也出过最多意外安全失败的地方**（安全层：能力边界>行为监督，与 Guardian 权限面互补）。
- **Claude Code auto mode 五层安全栈**：**①static settings（alwaysDeny/alwaysAllow/alwaysAsk 快速剪枝）→②PreToolUse Hook（用户脚本，exit code 2=block）→③tool attributes（isReadOnly 工具直接白名单放行）→④LLM Auto-Classifier（sideQuery 只见 tool_use block）→⑤rejection circuit breaker（连续 3 次或累计 20 次拒绝后回退交互提示）——每层只处理前一层漏掉的**（安全层：分层漏斗设计，每层只管漏网之鱼）。
- **n8n sub-workflow vs AI Agent Tool 判据**：**执行路径可预测、或同一 agent 逻辑需跨 workflow 复用→把 workflow 包成 sub-workflow（Call n8n Workflow Tool）；执行顺序真正依赖输入无法硬编码→AI Agent Tool 让 agent 自己决策**（编排层：确定性归工具，不确定性归 agent 决策）。
- **LangFlow traces 调试**：**1.8 版 per-component 延迟/token 用量/flow 跟踪——"某个环节坏了"从此可精确定位；调试 flaky node：逐步运行、检查输入输出、加临时 Chat Output tap 可视化中间量、用简单 schema 约束输出让失败显眼**（工具层：可观测性=逐组件 trace，调试点=临时输出 tap）。
- **提升层**：安全 / 编排 / 工具。

### B4：GitHub trending 新仓库 + Make 重试非幂等 + Pipedream Connect 嵌入（来源：repositorystats.com + startupcorners.com + github.hot + pipedream.com/docs，2026-09-27 实拉）
- **趋势生态事实**：**browser-use/jev-ultrafast（最快最便宜 web agent，+20,120/24h）；mitalibaba/open-code-review（混合架构代码评审：确定性管道+LLM Agent，行级精确注释，内置多语言规则集 NPE 等，★41,206 +19,699/24h）；paperclipai/paperclip（管理工作中 agent 的开源 app，今日热榜 #1）**（事实：评审工具走"确定性管道+LLM Agent"混合架构而非纯 LLM）。
- **Pipedream Connect：预建工具嵌入 agent**：**10,000+ 预建工具与触发器、3,000+ 集成 API，可直接嵌入应用或 AI agent；source 自带 deduping 策略与 key-value store**（工具层：第三方集成基建化，无需自建 OAuth）。
- **提升层**：工具 / 事实。

## 判重说明
- B1 knowledge-synthesis（多源合成+新鲜度×权威度置信度——新）；cost-budget-check（利用率分级告警阶梯——新）；memory-search 五项组合（r227 hybrid 面互补，五项组合器为增量合并）；academic-figure 五 agent 管线（r229-A paper-plot 模板面互补，管线结构新）；leadership-succession（人才评估四阶段，个人管理场景可学）；hook-generator（两行公式，内容创作新）；落。
- B2 Variable Aggregator（分支静默 null 坑——新，强相关工作流层）；Make 五种错误指令（r229-A Pipedream try/catch 互补，五指令体系新）；incomplete executions 重排语义（重试非幂等——新）；gatekeeper（r227-B supervisor 互补，意图路由具体化）；落。
- B3 containment（r227 安全纵深互补，"监督能做什么+五层栈机制"为增量合并）；auto mode 五层（r228-B auto mode 面互补，机制细节新）；sub-workflow 判据（r229-A subagents 判据互补，n8n 实现具体化）；traces（新）；落。
- B4 jev-ultrafast/open-code-review/paperclip（事实新）；重试重排语义（新）；Pipedream Connect（工具事实）；落。
- 未落：WaytoAGI Skills 蓝皮书与 arXiv Agent Skills 论文（r227-B 已落技能原理面）；组织级 skill 部署（企业级，不投入）；LangFlow Mustache（小点并入 traces 条）；MetaGPT 等排名事实（无方法增量）。
