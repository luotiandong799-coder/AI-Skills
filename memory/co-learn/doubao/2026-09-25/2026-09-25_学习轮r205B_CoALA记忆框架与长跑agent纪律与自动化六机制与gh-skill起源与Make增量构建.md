# 学习轮 r205-B：CoALA记忆框架与长跑agent纪律与自动化六机制与gh-skill起源与Make增量构建（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | blog.n8n.io/ai-agent-memory/（3866/5683） | OK（CoALA 四类型/存储三选） |
| 2 | blog.n8n.io/long-running-agents-beyond-prompt-engineering/（3963/5942） | OK（长跑 harness 纪律/EAP memory） |
| 3 | skillsmp.com/skills/page/22（#2101-2138） | OK（38 项） |
| 4 | deepseek-plugin.org/plugins offset 13224 | OK（#25-28，低价值续） |
| 5 | docs.openclaw.ai/automation（1717 全） | OK（六机制决策表/Standing Orders） |
| 6 | docs.langflow.org/（1946） | OK（平台介绍，无新独点） |
| 7 | general_search GitHub agent skills 生态 | OK（gh skill provenance/目录结构） |
| 8 | general_search Make AI agent best practices | OK（增量构建/例子胜描述） |
| 9 | （skillsmp 后半续读并入 #3） | — |
| 10 | （deepseek-plugin 续段并入 #4） | — |

## 独点（5 个）
### S1：CoALA 记忆四类型 + 存储三选 + 至少两种组合（来源：blog.n8n.io/ai-agent-memory，r205-A R3 的深度增量——procedural/时间索引/选型顺序为独有增量，按增量判定合并落地）
- **CoALA 框架（Cognitive Architectures for Language Agents）**：按"记忆代表什么"分类不按存储位置——**先按业务逻辑选类型，再决定怎么实现**。
- **四类型**：working（当前任务，会话结束即失）/semantic（事实知识，公司政策/文档/FAQ，向量库持久，**生产里占量最大**）/episodic（交互历史，**必须时间索引**——无时间层检索回"曾经知道但定位不了时间"→自信错误；客服 agent 里增长最快）/procedural（行为编码：工具调用序列/响应模式/升级规则=肌肉记忆；**进阶=从 episodic 提取模式定期更新 procedural**）。
- **存储三选**：in-context buffer+summarization（**编码 agent/需原样引用先前输出的工作流坏**——摘要丢精确性）；vector stores（**50 个边缘相关不如 5 个高相关**——调 embedding/threshold/top-k 是价值分界）；knowledge graph（**关系查询不是相似性问题**——"哪个客户关联哪个工单"，实体边优先）。
- **结合至少两种**：buffer 当前对话 + DB 会话历史 + vector 千票搜索——每个存储照顾一种记忆需求。
- 判据：**记忆按语义分型不按物理位置**；**episodic 必须带时间**；检索质量>检索量。
- **提升层**：工作流 / 记忆架构。

### S2：长跑 agent harness 纪律：model/agent 区分 / LLM 作工具由 harness 调度 / EAP memory 五件套 / durable 持久清单 / token 轨迹预测（来源：blog.n8n.io/long-running-agents-beyond-prompt-engineering）
- **别靠 prompt 撑 agent 设计**：用 LLM 自评自查=引入更多幻觉/漂移点；**text generator 是软件，要设计运行逻辑**。
- **model vs agent**：model 文本进出不做别的；agent 是执行部分——**model 撞 token 限中断 JSON=model 级事件（截断输出）→agent 级后果（畸形工具调用/坏状态写/损坏账本条目）**。
- **LLM 调用可用作工具但由 harness 决定**：summarize 40 结果→200 字应是 harness 在自己调度上的确定性函数调用（自带输出验证），**不是 agent 中途自己决定"该压缩了"**。
- **Context Usage Meter（Gumloop）**：实时窗口用量，分类分解 System/AI Instructions/Abilities/Tools/Skills/Subagents/Conversation——长跑里 conversation 涨、system+tool 稳定。
- **Google ADK Context Compaction**：滑窗总结旧事件到事件数阈值触发；**不能老总结——harness 应做完整 context reset**（tear down session，从 durable artifacts 重建）。
- **Google EAP memory generation 五件套**：extraction 只提最有意义（可定制：给 topic+few-shot 定义"什么算有意义"）/consolidation 新旧合并演化/generation 异步后台不阻塞 agent/event ingestion 流式按批自动触发/revision 自动维护可查记忆演化；TTL 过期；IAM 条件控制读写；**memory scope 生成时定义且不可变，per-identity 隔离**。
- **durable 持久清单**：持久=agent state/SQLite 表/计划任务/连接状态；不持久=内存变量/运行定时器/HTTP 调用/callback promise 链。**wake-on-event 睡回**（agent 注册自己 callback URL 后休眠，callback 到才醒；poll with backoff cap）；子代理各自 state/schedule/lifecycle，父不活跃时子照常跑，crash 不整族倒下。
- **token/rate-limit 轨迹预测**：累计消耗轨迹投影在下一 checkpoint 前会撞限→harness 主动 checkpoint/throttle/换 provider。
- 判据：**harness 管压缩/恢复/重试，agent 管干活**；持久=能重建状态，不是保持进程活。
- **提升层**：工作流 / Agent 编排 / 上下文管理。

### S3：OpenClaw 自动化六机制决策表 + Standing Orders + inferred commitments 已移除（来源：docs.openclaw.ai/automation，r205-A R5 的并列机制增量）
- **六机制分工**：Automations=所有周期性/一次性调度（精确时刻/隔离执行/不同模型）；Heartbeat=系统所有环境监控（默认 30min，**不创建 task 记录**，scratch 空跳 empty-heartbeat-file，主队列忙时顺延）；Background Tasks=脱主会话工作账本；Task Flow=账本之上的多步流编排（durable+revision tracking）；Hooks=生命周期脚本（/new//reset//stop/compaction/gateway startup/message flow）；Standing Orders=workspace 文件（AGENTS.md）注入每个会话的**永久操作授权**（"Always check compliance before replying"）。
- **Automations vs Heartbeat**：用户建 vs 系统所有；明确报告/提醒用 Automation，环境感知用 Heartbeat。
- **Retired inferred commitments**：OpenClaw 已**移除"从对话推断跟进事项"实验**——不再自动提取 follow-ups；要提醒就显式建 automation。反模式信号：靠"对话里说过"当承诺=不可靠。
- 判据：**调度/监控/账本/编排/钩子/常设指令六层各司其职**；常设规则写 Standing Orders 不靠对话。
- **提升层**：工作流 / Agent 平台治理。

### S4：gh skill 跨平台管理 + skill 目录四件套（来源：bighatgroup gh-skill + aridanemartin skill 结构 + GitHub Docs，r204-C P3 规范的生态增量）
- **gh skill（GitHub CLI）**：跨 Copilot/Claude Code/Cursor 管理 agent skills——**provenance built-in：安装来源验证**（skill 从哪来的、装了什么、是否可信）。
- **skill 目录四件套**：`SKILL.md`（必需：指令+元数据）+`scripts/`（可选：可执行代码 Python/Bash/JS）+`references/`（可选：**按需加载** REFERENCE.md/domain.md）+`assets/`（可选：模板/图片/数据，**output.md=精确输出格式**）。
- **agent skill 定位**：可复用行为指令，**低频但专业任务按需加载进上下文**——不是常驻。
- **Copilot skills frontmatter**：name/description/license 三字段+Markdown body 指令+**validation steps 确认结果**。
- 判据：**装技能要看 provenance**；低频专业任务用 skill 按需加载不常驻。
- **提升层**：可复用 Skill（生态/管理）。

### S5：Make 增量构建 + 例子胜描述（来源：help.make.com/make-ai-agent-new-best-practices + Make Academy agent-engineering/context-engineering，r204-B O2 的同源增量合并）
- **一次加一个组件测完再加**：高能力模型起步+清晰角色/行为/规则指令→**先加 knowledge files 测试检索对不对→再逐个加工具，每个通过 chat 验证调用正确产生预期结果，再加下一个**——增量构建+每步验证。
- **给例子胜于描述**：请求"把客户数据格式化成表格"→直接给实际表格示例（样例名/邮箱/状态/日期列）；**展示好输出长什么样比描述更有教益**。
- **意外事件指令**：明确告诉模型"不清楚/失败时怎么办"（"如果用户没提供 X，问用户"）。
- **通用化工具描述**：写"做什么+用什么数据"且**保持通用以便同一工具被不同 agent 复用**。
- **首尾管理模块**：scenario 开头/结尾加专门模块管理进出数据。
- 判据：**构建=一次一步+每步验证**；指令里给例胜过抽象描述。
- **提升层**：工作流 / 提示工程。

## 判重说明
- S1 → r205-A R3 已有四类型三拓扑；procedural 记忆/episodic 时间索引/存储选型顺序/50vs5 检索质量为独有增量，按增量判定合并落地。
- S2 → wb-context-compressor 已有压缩/预算；"harness 管压缩恢复、model/agent 截断级联、EAP 五件套、wake-on-event、token 轨迹预测"为独有增量，落。
- S3 → r205-A R5 已有 tasks 账本；"六机制决策表/Standing Orders/inferred commitments 移除"为并列机制增量，落。
- S4 → r204-C P3 已有 name/description 规范；"gh skill provenance/目录四件套/按需加载定位"为生态增量，合并落地。
- S5 → r204-B O2 已有指令七要素；"增量构建+例子胜描述+意外事件"为增量，合并落地。
- 未落：skillsmp p22 候选（baoyu-translate 术语表弱/awesome-design-md 品牌库偏设计/paper-fetch 学术链偏专业/contract-review 豆包已有/continuous-learning 与 self-improvement 重复）；langflow 根页（平台介绍无独点）；deepseek DSH 续（低价值）；music-intelligence（mediakit 已有）。
