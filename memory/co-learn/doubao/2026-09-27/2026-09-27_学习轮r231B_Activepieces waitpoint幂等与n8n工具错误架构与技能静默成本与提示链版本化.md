# 学习轮 r231B：Activepieces waitpoint幂等与n8n工具错误架构与技能静默成本与提示链版本化（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/96（#9576-9600，p96 尾段，p96 已尽 total 10991） | OK |
| 2 | Dify（Plugin 六类型/Plugin Daemon 隔离进程/模型提供方四步） | OK |
| 3 | n8n（sub-workflow 包装工具错误/Continue on Fail/Never Error/AI 分类重试+dead letters/Window Buffer 截断破坏 tool_calls） | OK |
| 4 | LangFlow（1.11 Multi-Vector PLAID 多向量检索/Guardrails 组件/AI Response Evaluation） | OK |
| 5 | Activepieces（waitpoint durable checkpoint/resume 信号/HITL 四要素/审批队列 owner-SLA-过期） | OK |
| 6 | Make（webhook response 前置防超时/Data Stores 重复检查） | OK |
| 7 | Pipedream（Connect token 4 小时过期/managed auth 2400+ API） | OK |
| 8 | Anthropic（kenimoto 技能静默成本实测/token counting API/成本优化七步顺序） | OK |
| 9 | GitHub 生态（DeepSeek 一切皆插件框架/jev-chat-jarvis 非侵入/JeecgBoot Skills 生成模式） | OK |
| 10 | WaytoAGI（Prompt Chaining 减 4.5x 迭代/handoff points/结构化框架/版本化） | OK |

## 独点（4 个）
### B1：Activepieces waitpoint 幂等 + HITL 四要素（来源：activepieces.com/docs/install/architecture/waitpoints + anhtu.dev + tutorialslogic.com，2026-09-27 实拉）
- **waitpoint=durable checkpoint**：**run 标记 PAUSED、执行状态持久化、resume 信号=HTTP 调用 resume URL 或 scheduled job；同一 action 会跑两次（一次创建 waitpoint、一次读 resume payload）——所以 pausing action 必须幂等**（工作流层：暂停/恢复机制的根约束是"同一 action 跑两遍"——设计任何会暂停的步骤先想幂等）。
- **HITL 四要素**：**interrupt（风险动作前暂停不丢上下文）/ notification（按类型/风险路由到对的人）/ review interface（展示 proposed action + agent 推理——approver 不能盲目点）/ resume（proceed / modify-then-proceed / cancel 从暂停点精确恢复）**（工作流层：人审不是"加一步确认"，是把"上下文+推理+精确恢复"一起给审的人）。
- **审批队列要 owner/SLA/提醒/过期行为/fallback；执行前重验时间敏感事实（proposed 时有效、approved 时可能已过期）**（工作流层：审批等得越久，被审的事越可能过期——重验是审批流的固定环节）。
- **提升层**：工作流。

### B2：n8n 工具错误处理架构：子流程包装 + AI 分类重试（来源：blog.n8n.io + community.n8n.io + n8n.io/workflows/16744，2026-09-27 实拉）
- **工具逻辑放进独立 sub-workflow + "Continue on Fail"**：**主流程的 Continue-on-error 抓不住工具子节点的错误；把 HTTP 调用包进子流程，子流程总能完成并回干净响应给 agent，主流程不会死**（工作流层：工具错误隔离在子流程边界，agent 收到"结果"而非"崩溃"）。
- **Never Error toggle**：HTTP Request 节点开 Never Error 后保持"绿"即使失败（工具层：只读查询类工具可用，写操作仍要真实报错）。
- **AI 分类重试流水线**：**错误上下文送 Anthropic 返回结构化 JSON（category/confidence/remediation）→ per-incident retry counter（最多 3 次）→ transient+confidence 够+预算内→指数退避重试→记录结果；不可重试或耗尽→dead letters 表 nightly 重放**（工作流层：重试决策交给"分类+置信度+预算"三元判断，不是一律重试或一律放弃）。
- **Window Buffer Memory Truncation 副作用**：**截断可能切掉 assistant 的 tool_calls 块，留下孤立 role:tool 消息 → OpenAI 400（tool 消息必须紧跟匹配的 tool_calls）**（工具层：记忆截断要按 tool_calls 块为边界，不能按窗口硬切）。
- **提升层**：工作流 / 工具。

### B3：技能静默成本实测 + token counting API + 成本优化顺序（来源：kenimoto.dev + developersvoice.com + platform.claude.com/cookbook，2026-09-27 实拉）
- **技能不触发也花钱——实测证据**：**5 技能 × 7 小时实测：dormant skills 描述层 231K tokens 占 11%（3 个从没触发的占了 18% 账单）；Conversation/CLAUDE.md/code reads 82% 是另一回事**（可复用 Skill 层：装技能不是免费——每个 description 每轮都进上下文；技能瘦身=持续省钱，与 r231-A 上下文公共品互证）。
- **progressive disclosure 的成本含义**：**重复 prompt 换成 skill 只省在"完整指令只在触发时加载"，每次请求仍付 trigger description 30-60 tokens**（可复用 Skill 层：描述写得长=每轮多花；写短=省）。
- **token counting API**：**提交前估算 input tokens（system/messages/tools/images/PDF 全支持），用于成本/限流管理、路由决策、把 prompt 压进目标长度**（工具层：先量后发，把超长 prompt 在请求前发现）。
- **成本优化七步顺序**：**先在能干的模型上跑通→建 eval 测基线→prompt caching→输入管理（让模型通过工具发现上下文）→agent-loop 防多轮上下文复合→输出管理更紧约束→Batch API 异步→模型选择与 effort**（工作流层：优化的先后就是收益的先后——先能跑再省，eval 先行）。
- **提升层**：可复用 Skill / 工具。

### B4：Prompt Chaining + 交接点 + 版本化 + 多向量检索（来源：skillgen.io + promptfluent.com + docs.futureagi.com + langflow.org/blog/blog-nextplaid，2026-09-27 实拉）
- **Prompt Chaining**：**拆复杂任务成顺序 prompt，输出喂下一步；比单 prompt 减 4.5x 手动迭代；机制=减少指令漂移、收窄模型注意力、允许中间验证检查点**（工作流层：链式不是风格，是"每步一个任务+中间可验"）。
- **handoff points（交接点）**：**链断大多断在交接——"这是草稿→改它"是坏交接；先定义每步的输入输出格式与验收，再写链**（工作流层：链质量由交接契约决定，不是由每步 prompt 决定）。
- **Prompt Versioning**：**模板提交编号版本→标 production 标签→运行时 SDK/dashboard serve 正确版本→评估后 promote→可回滚**（工作流层：提示词当代码管——版本、标签、serve、回滚四件套，与 r230-C DSL IaC 同源扩展）。
- **LangFlow 1.11 PLAID 多向量检索**：**文本多向量 94.7 vs 单向量 top-100+rerank 90.7；图像检索提升更大（22.6 → 89.7）——视觉文档检索是最大受益场景**（模型层：多向量（late interaction）在图文混合文档上碾压单向量，尤其图像）。
- **提升层**：工作流 / 模型。

## 判重说明
- B1 waitpoint 幂等（r229-C approval 面增量——waitpoint 机制+双跑幂等）；HITL 四要素展示推理（新）；审批队列治理（新）；落。
- B2 子流程包装（r231-A Enrichment 面互补增量——错误隔离包装）；AI 分类重试（r230-A Make 429 面互补增量——三元判断+dead letters）；截断破坏 tool_calls（新）；落。
- B3 静默成本实测（新强相关——数据支撑）；token counting（新）；优化七步顺序（r230-A 成本四层面互补增量——操作顺序化）；落。
- B4 chaining（新）；handoff（新）；版本化（r230-C DSL IaC 面互补增量——提示词版本化机制）；PLAID 多向量（新强相关）；落。
- 未落：Dify Plugin 六类型/Plugin Daemon（面窄）；repo-wiki 增量更新（r230-C 增量索引面已覆盖）；shipping-and-launch 发布清单（面窄）；Make webhook 前置（面窄）；DeepSeek 插件框架/JeecgBoot（数量堆积无方法论增量）。
