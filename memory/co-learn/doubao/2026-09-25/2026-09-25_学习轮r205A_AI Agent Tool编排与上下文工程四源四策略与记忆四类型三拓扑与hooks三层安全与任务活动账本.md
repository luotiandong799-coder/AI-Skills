# 学习轮 r205-A：AI Agent Tool编排与上下文工程四源四策略与记忆四类型三拓扑与hooks三层安全与任务活动账本（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | blog.n8n.io/production-ai-playbook-complex-agent-patterns/（续读 3273-7049/19237） | OK（AI Agent Tool 编排/子工作流取舍） |
| 2 | blog.n8n.io/context-engineering-llm/（3993/6486） | OK（四源+四策略） |
| 3 | blog.n8n.io/llm-memory/（3892 全） | OK（记忆四类型+三拓扑+三失败） |
| 4 | dify.ai/blog/dify-1-5-0（续读 6588-9728/13429） | OK（Test in steps/LAST RUN 面板/skipped 提示） |
| 5 | skillsmp.com/skills/page/21（#2001-2066 两段） | OK（66 项） |
| 6 | deepseek-plugin.org/plugins offset 9928 | OK（#25-28，DSH 生态续，低价值） |
| 7 | docs.openclaw.ai/automation/agents | 死链 |
| 8 | general_search Claude Code hooks 安全 | OK（三层检查/Inference hooks/CVE） |
| 9 | docs.openclaw.ai/automation/tasks（4000/6951） | OK（任务活动账本） |
| 10 | waytoagi.com/ai-tools | 死链 |

## 独点（5 个）
### R1：n8n AI Agent Tool 编排模式 + 子工作流取舍：orchestrator 不学 specialist 细节 / 工具描述定路由 / research-writer-reviewer 管线（来源：blog.n8n.io/production-ai-playbook，r204-C P2 的续篇增量）
- **AI Agent Tool 动态委托**：orchestrator agent 把 specialist agent 当工具调（billing/technical/account 各带独立 model/system prompt/tools）；**orchestrator 不需要知道 specialist 领域细节（退款政策/技术诊断），只需理解请求并路由给对的 specialist**；每个 specialist 自包含，调优一个不影响其他。
- **工具描述决定路由**：orchestrator 调哪个 specialist 由你写的 tool description 驱动——**模糊描述导致错误路由**；要具体写"管什么"+"不管什么"。
- **子工作流 vs AI Agent Tool 取舍**：执行路径可预测/需复用/独立测试优先→子工作流（Call n8n Workflow Tool 打包为工具）；动态委托/路由歧义→AI Agent Tool。子工作流四优点：独立测试、跨父复用、团队分维护、独立版本回滚。
- **内容管线三子工作流**：research→writer→reviewer（reviewer 用 LLM-as-Judge 按准确/语气/完整评分，**低于阈值 loop 回 writer 带修订意见**）。
- 判据：**编排者只路由不干活**；**路由质量=工具描述质量**；**可预测管线用子工作流，歧义路由用 agent tool**。
- **提升层**：工作流 / Agent 编排。

### R2：上下文工程四源四策略：system prompt 永久税 / 裸 JSON 幻觉 / 工具定义 RAG 检索 / Write-Select-Compress-Isolate（来源：blog.n8n.io/context-engineering-llm）
- **prompt 工程 vs 上下文工程**：prompt=静态单轮文本；context engineering 把窗口当**动态数据缓冲**，每次调用程序化组装/过滤——生产里 system prompt 常只占窗口一小部分，其余是记忆/RAG/工具输出。
- **四类填充源**：①system prompt（臃肿=**每次调用 1000-2000 token 永久税**）；②conversation state（盲追加全部历史→早期交互无关甚至矛盾，丢主线）；③retrieved knowledge（**裸 JSON/大文档碎片=幻觉触发器**；最佳=干净 just-in-time 添加，剥元数据/结构标记，只提精确文本块）；④tool definitions（**全局工具目录的 schema 就能耗尽整个 token 预算**——建 RAG 检索工具定义，Anthropic 有 Tool search tool 探目录只加载相关）。
- **四策略：Write（每句 system prompt 挣位置）/Select（进窗口前过滤）/Compress（压旧交互）/Isolate（子代理隔离上下文）**。
- **context rot**：模型忽略密集 prompt 中央只记头尾——高价值指令被低价值执行数据埋没。
- 判据：**窗口是动态缓冲不是静态文件**；工具多了要检索工具定义而不是全量注入。
- **提升层**：工作流 / 上下文管理。

### R3：LLM 记忆四类型 + 三实现拓扑 + 三失败模式缓解（来源：blog.n8n.io/llm-memory）
- **四类记忆**：in-context（提示内，快准但硬顶）/external（向量检索，近无限但 chunking 错=噪声→幻觉）/parametric（权重内，零延迟但训练后漂移）/episodic（跨会话用户偏好，session ID 检索摘要；**不总结不遗忘=历史膨胀拖慢每次响应**）。
- **三实现拓扑**：RAG（线性管线，静态文档库）；**Agentic RAG**（检索决策给 LLM，多跳调查灵活但不可调试+贵——执行视图要显示每步"哪个工具/什么查询/返回什么/是否再搜"）；**GraphRAG**（知识图谱遍历，500 篇论文跨主题综合；LLM 提取实体贵）。
- **三失败模式+缓解**：①context rot→周期压缩旧交换成状态摘要，元数据留在高召回区；②RAG top-k 噪声→**混合检索 dense+sparse 过 reranker 评分后才进窗口**；③agentic loops relevance drift（近 miss 检索→反馈环漂移越查越偏）→**加 supervisor/相关性护栏，低于置信阈值强制 query reset 或问用户**。
- 判据：**记忆是分层的**（短/长/参数）；检索进窗口前必须评分；agent 自己搜的循环要护栏防漂移。
- **提升层**：工作流 / RAG / Agent 编排。

### R4：hooks 三层安全检查深度 + Inference hooks DLP + hooks 不可绕过 + 恶意 hooks 审计（来源：code.claude.com/security-guidance + claude.com Inference hooks + llm-safe-haven + phosailabs，r204-A N1 hooks 的深度增量）
- **三层检查深度**：①每文件编辑时：**快速模板匹配危险调用（不调用模型）**；②每轮结束：后台模型检查本轮全部改动；③每次 commit/push：**更深 agentic 检查**。
- **Inference hooks（Enterprise）**：DLP 服务器在 prompt 和 tool 响应到达 Claude **之前**检查，block/allow 实时执行——未批准内容到不了模型。
- **hooks 是唯一保证行为的方式**：hooks 由 harness 执行不是模型执行——**模型无法绕过自己的 hooks**（比 deny 规则更强的机制）。
- **CVE-2025-59536**：恶意仓库在会话启动时注入 hooks——**不装不可信 repo 的 hooks**；`npx llm-safe-haven audit` 验证 SHA256。
- **PreToolUse 六事件+Danger Guard**：首装 hook=阻止不可逆 bash（`dd if= / >/dev/sd / curl|sh / wget|sh / chmod 777 / git push -f` 正则预检）；permission creep（accumulated allows）定期审计。
- 判据：**安全检查分深度三层**；关键动作用 harness 级 hook 锁死（模型绕不过）；hooks 本身要审计来源。
- **提升层**：工具 / 安全工作流。

### R5：后台任务活动账本：状态机 lost / 执行交付分离 blocked / 通知三档 / audit finding 阈值 / 幂等媒体任务（来源：docs.openclaw.ai/automation/tasks，r202 执行-交付分离的完整增量）
- **Tasks 是活动账本不是调度器**：记录脱主会话工作（ACP/subagent/automation/CLI/media），automation 与调度器各管各的。
- **状态机**：queued→running→terminal（succeeded/failed/timed_out/cancelled/**lost**）；**lost=backing state 消失超 5 分钟宽限**；terminal 后后续信号不降级。
- **执行与交付分离（补充 blocked 终态）**：subagent 可 succeeded 而 deliveryStatus=session_queued/failed；**blocked=活干完结果没交回**（保留 7 天）；`tasks retry`（新 fence 队列代，可重复可见结果）/`tasks dismiss`（记录有意不交付）。
- **通知三档**：done_only（默认）/state_changes/silent（automation/CLI/media 默认 silent，调度器自己管交付）。
- **audit 九 finding+阈值**：stale_queued 10min warn / stale_running 30min error / lost / delivery_failed / missing_cleanup / inconsistent_timestamps——`tasks audit` 一次出报告。
- **幂等媒体任务**：会话内重复同 prompt 的 image/music/video 生成返回**活动任务状态不重复启动**。
- 判据：**后台工作要有账本**；状态与交付两槽分开记；审计阈值量化（10/30 分钟）。
- **提升层**：工作流（后台任务治理）。

## 判重说明
- R1 → r204-C P2 已有三桶架构；"AI Agent Tool 编排/orchestrator 只路由/工具描述定路由/子工作流四优点/LLM-as-Judge loop"为续篇独有增量，落。
- R2 → wb-context-compressor 已有上下文预算/压缩；"四源拆解/system prompt 永久税/裸 JSON 幻觉/工具定义 RAG 检索（Tool search tool）/Write-Select-Compress-Isolate"为独有增量，落。
- R3 → r205 之前记忆类（wb-context-compressor 记忆提取四策略）已录；"四类型分层/三拓扑对比/三失败缓解（reranker 门+supervisor 护栏）"为独有增量，落。
- R4 → r204-A N1 已有 hooks 预处理；"三层深度/Inference hooks DLP/harness 不可绕过/CVE-2025-59536 审计/危险命令正则"为深度增量，落。
- R5 → r202 已有执行-交付分离原则；"任务账本状态机 lost/blocked 终态+retry/通知三档/audit 阈值/幂等媒体"为完整增量，落。
- 未落：dify Test-in-steps（P5 续细节并入既有）；sn-da-excel Parquet（单一工具弱）；grammar-check 最小干预（弱）；agent-customization 排障（候选下轮）；planning-with-files 文件式规划（候选下轮）；math-modeling/article-rewriter（专业/弱）；workbuddy-checkin（第三方 hack 签到，不落）。
