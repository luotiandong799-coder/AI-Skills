# 2026-10-03 学习轮 r390A：Agent 上下文工程与 need-to-know 注入 2026

轮次：r390A（本批第 1 轮）
判重：双键 grep KB 4192 行 → need-to-know=0 / 上下文注入=4 / 输出约束=1；避让 WB r390（执行身份绑定/会话隔离/重试白名单）、r389（路由/数据/分解）、r387-r388（权限/评测/日志）。本批净增 7 独点。
实拉：4 批×3 次 general_search 全部成功（12 query，逐站带来源标识）。

## 落地 7 独点（每点标注提升层）

### 1. 上下文工程四动作框架 write/select/compress/isolate + 成本风险表（可复用 Skill）
来源：mastra-context-engineering / vzhukov-context-engineering / professionaldeveloper-context-discipline / zylos-context-system-level / addyosmani-context-engineering
- **四动作操作清单**：write=把信息存到窗口外（任务状态对象/用户偏好笔记/人工纠错/工具结果摘要）；select=恰当时刻拉对内容（代码库检索/记忆选择/本任务相关文件）；compress=只留本步需要的 token（摘要/返回引用而非 blob）；isolate=隔离无关上下文防干扰（sub-agent 独立窗口/按任务隔离存储/文件系统作外部记忆）。
- **各策略成本风险**：write=低（存储+读 I/O）风险陈旧笔记；select=中（检索延迟）风险阈值过狠漏相关；compress=中（额外 LLM 调用）风险摘要丢信息；isolate=高（多次 LLM 调用）风险协调开销+跨域 nuance 丢失。
- **何时删的清单**（addyosmani）：过去的失败尝试及其错误输出→跨过就删结论不删旅程；verbose 工具输出（长 find 结果/完整文件列表）→提取完就删；对话来回→决定达成即删；被替换的旧代码草稿→替换立即删（当前文件就是记录）。
- **isolate 优先于 inclusion**（Zylos）：产生大量一次性输出的操作（log dumps/宽文件搜索/多步研究）进 sub-agent 或沙箱调用返回摘要，不内联在主上下文；工作状态外化到文件而非在上下文中复述。
- 判据：上下文出问题先归因到四动作之一——是没写出去、没选对、没压掉、还是没隔开。

### 2. 检索注入两模式 + need-to-know 选择性注入 + 检索内容=不可信数据（工作流）
来源：agentscope-rag-modes / jesseliberty-rag-overview / atlan-context-window-management / devto-context-engineering-2026 / zalt-rag-inside-agents / aiorbitx-knowledge-grounded / explainx-context-injection
- **两模式**：Generic Mode=每步推理前自动检索注入（简单、任何 LLM 可用，但不需要时也检索）；Agentic Mode=agent 用工具自己决定何时检索（灵活、只按需取，但需强推理能力）。Microsoft 对应 BeforeAIInvoke vs OnDemandFunctionCalling。
- **need-to-know 选择性注入**（Atlan）：检索前先分类查询意图，只交付匹配当前任务的上下文产品，不加载所有潜在相关信息——需要 context routing layer（查询类型→上下文产品类目映射）。
- **两层上下文结构**（AgentPatterns）：Startup 层=指令/约定/工具描述/技能元数据（会话开始加载）；On-demand 层=文档页/文件内容/搜索结果/API 响应（任务需要时才工具调用取）。agent 保持 lean 启动、为推理保留预算。
- **检索内容=不可信数据**：知识库文章/邮件正文可能含"忽略之前指令"类注入——系统必须假设检索内容是 data 不是 authority；控制=明确分隔符隔开系统指令与检索段落+告诉模型文档是不可信证据+block 不在白名单的工具调用+检索内容放明确标记区段。
- **低置信度显式信号**：所有 chunk 低于相似度阈值时返回显式低置信信号，系统提示词指示"如果 retrieve_context 无高置信匹配就明确说不，不继续需要事实基础的步骤"+高价值步骤配人环护栏（低置信触发升级而非自信但错的回答）。
- **接地指令**："Using only the information in the RETRIEVED CONTEXT"——防模型把检索上下文与参数知识无缝混合；不消除幻觉但让失败更可检出（引用上下文中不存在的事实=易被抓）。
- **技能描述注入攻击**：YAML description 字段（初始加载进系统提示词、早于用户任务处理）注入可使攻击成功率 +10.6pp（平均）/ +16.8pp（warning 条件）——描述级攻击可反制安全导向提示（arxiv-2602.20156）。
- 判据：注入时机（自动 vs 按需）× 注入范围（全量 vs need-to-know）× 注入可信度（权威 vs 数据）三个旋钮分别定，缺一个就漏一半。

### 3. 检索精度>召回：ranking not stuffing + rerank/hybrid + 最小充分证据集（模型/工具）
来源：shaped-ranking-not-stuffing / redis-context-quality / chiraghasija-context-discipline / arxiv-2512.14465-context-picker / arxiv-2502.11811-compselect / hub-gazar-window
- **注意力平方成本**：2x 上下文 token=4x 计算成本；塞满上下文降低质量（LLM 被无关上下文干扰）；研究一致显示**检索精度比召回更影响下游任务表现**；cosine similarity≠ranking（向量搜索返回"相似"结果，训练过的排序模型返回"有用"结果）。
- **rerank 是修复**：一个更好的检索器没有精度层会让问题更糟；cross-encoder 在进上下文前重排候选——broad recall 检索后 tight precision 重排；hybrid search（BM25+dense）补各自漏。
- **两阶段 RL 选择**（Context-Picker）：阶段 1 提关键段落召回率，阶段 2 剪冗余蒸馏紧凑证据集——把上下文选择当"最小充分证据子集"而非相似度排序。
- **Clue 提取三模块**（CompSelect）：clue extractor+reranker+truncator——提供充分有效推理线索同时降推理成本。
- **三种注入失败模式**（gazar）：Distraction=上下文太多模型过度关注忽略自身推理→trim 检索更少更好 chunk；Confusion=无关但看似合理内容把答案带偏→rerank 丢弃低相关段落；Clash=两个检索段落矛盾模型选错→dedup 优先最新/最权威来源——每种都随 token 增加变糟。
- 判据：检索管线=recall 阶段 + precision 阶段分离；评估同时报 Precision@K 与 Recall@K，只看端到端答案无法调试检索质量。

### 4. lost-in-the-middle 定位与对策：bookend / multi-pass / eviction 三策略（模型/工具）
来源：arxiv-2307.03172-lost-in-the-middle / twnside-bookend / devto-lost-in-middle / aiexpert-context-engineering / arxiv-2606.23961-nexus-sampling / promptandlearn-context-management
- **位置偏差实证**：相关信息在开头/结尾时性能最高，在长上下文中间显著退化（即使显式长上下文模型）；20 chunks 时最可能用的是 0 位和 19 位，中间最少被用。
- **Bookend 策略**：必须给大块上下文时，开头放关键点精简摘要+结尾重复同样关键点——信号在两个高注意力边界都出现，合成测试中接近完美检索准确率。
- **Multi-pass 提取**：关键应用分两遍——第一遍每文档独立提取相关事实（每文档获得全注意力，完全避开位置偏差），第二遍综合这些事实成答案。
- **Eviction 三策略**：recency-based（最旧先删）/ relevance-based（与当前任务最不相关先删）/ importance-based（低优先级标签先删）——给上下文项标 priority 级别，需要驱逐时按序删。
- **Nexus Sampling**：训练无关 KV-cache 驱逐——Nexus scoring（直接注意力迭代走暴露 bridge token）+ weighted reservoir sampling（按包含概率保留）；80% KV-cache 驱逐时匹配 dense attention（±内）。
- **历史重排**：每 8-10 轮用 embedding/轻模型给历史消息按当前话题相关性打分，只留 top 5-7 相关轮+最近 2 轮——turn 50 时上下文大多是死重。
- 判据：长上下文不是免费——要么用定位技巧对抗位置偏差，要么干脆剪到 5-7 相关轮。

### 5. 压缩分层与保护区：keep-verbatim / tool clearing / Anchored Iterative Summarization（工作流）
来源：agentnative-context-compaction / muratcankoylan-context-compression / agentpatterns-context-compression / DenisSergeevitch-context-memory-compaction / arxiv-2606.31564-ace / y-agent-inside-claude-code
- **Keep-verbatim 保护区**：系统提示词与工具 schema（字节稳定保前缀缓存命中）、任务陈述与验收标准、最近 5-7 轮全保不摘要——压缩层级里最便宜的第一杠杆是 tool-result clearing（旧可重取的输出换占位符，保留"调用发生过+返回什么"一行记录）。
- **Anchored Iterative Summarization**：长会话中维护结构化持久摘要（session intent/文件改动/决策/下一步明确分节）；压缩触发时只摘要新截断跨度并与现有摘要合并，不从零再生成——全量再生成每次都有丢模型认为低优先级但任务需要的细节的风险（漂移累积）。
- **分层滚动摘要**：阈值触发重写历史；hierarchical=递归摘要（1-50 轮→1-100 轮含首摘要）；map-reduce=分块独立摘要（map）再合并（reduce）。
- **摘要保留/丢弃清单**（agentpatterns）：保留=当前目标/关键工件/决策与理由/下一步；丢弃=探索性回合/被取代指令/已解决错误/不影响结果的中间推理；**load-bearing 推理例外**——跨工具调用仍承重的工作假设推理丢弃会让 agent 每轮重推假设。
- **压缩后重建**（DenisSergeevitch）：压缩后 reattach 活动计划/工作流状态/目标/审批/已加载指令/已调用技能/连接器状态；bulky 工件存外部+引用不内联。
- **per-type retention**（agentpatterns）：compaction 把安全规则按与聊天消息相同速率摘要=危险——不同内容类型保留速率不同（安全规则/凭据/约束比闲聊保留更久）。
- 判据：先做零 LLM 成本杠杆（清除/截断/占位），LLM 摘要是兜底不是首选；保护区字节稳定保前缀缓存。

### 6. 平台原生上下文机制：Anthropic vs OpenAI（工具）
来源：platform.claude-compaction/context-editing / anthropic-context-management / anthropic-effective-context-engineering / anthropic-managed-agents / openai-agents-sdk-sessions/context / openai-responses-native-compaction
- **Anthropic**：官方推荐 server-side compaction（自动处理、token 计算准确、无客户端限制）> SDK compaction；compaction_control 参数已 deprecated；memory tool=文件系统持久化（agent 建知识库/跨会话项目状态/引用既往学习，不全部留在上下文）；context editing=token 预算填满自动剪旧工具输出；Managed Agents 把 session 当上下文对象放窗口外（getEvents() 按位置切片选事件流，brain 从任意处续起）。
- **OpenAI**：Responses API native compaction=最新模型经训练分析先前对话状态生成 compaction item（加密 token 高效表示），下一上下文窗=compaction item+高价值旧窗部分；Agents SDK 三状态策略=result.to_input_list()（应用内存/小对话环/全手动）/ session（你的存储+SDK/持久可恢复/自定义存储）/ conversation_id（服务端命名会话/跨 worker 共享）；短程记忆两旋钮=context_limit（真实用户轮数上限，超限前摘要）+ keep_last_n_turns（摘要时保留多少最近轮 verbatim），不变量 keep_last_n_turns≤context_limit；RunContextWrapper 结构化状态对象+hooks+context-injection=上下文个性化（跨 run 持久、记忆/笔记/偏好演化）。
- **prompt 分节**（Anthropic）：系统提示词组织成 distinct sections（XML tagging 或 Markdown headers 划界）——指令与数据域分离，也是注入防御的形态基础。
- 判据：优先用平台原生压缩（省集成+对齐训练方式），客户端自建摘要仅在需定制时；状态对象外化是两家共识方向。

### 7. 上下文质量评测：五维指标 + Context Fails First 四判据（可复用 Skill）
来源：usewire-measure-context-quality / explainx-context-engineering-clean / devops-gheware-context-metrics / aicharcha-eval-framework / clouatre-multi-agent-reliability / arxiv-2607.14275-context-fails-first / arxiv-2606.10209-less-context
- **五维**（Wire）：correctness / completeness / faithfulness / relevance / freshness；LangChain 2026 调查 1300+ AI 工程师：89% 有 observability 但只有 52% 跑 eval——大多数人对自己 agent 实际收到什么失明。
- **Context Fails First**（arxiv 2607.14275）：agent 失败前上下文先失败——四判据=Tool schema quality（工具名/类型参数/描述/副作用边界/错误行为/when-to-call → 工具误用）/ Grounding sufficiency（上下文是否提供足够可靠证据 → 幻觉）/ Injection hardening（可信指令是否与不可信内容分离 → 注入）/ Token efficiency（是否避免冗余样板 → 上下文膨胀）——按判据归因不怪模型。
- **业务指标**：repair turn rate <15%（需后续纠正的轮次占比）；hallucination rate <5%（输出含上下文外事实错误占比）；token cost per task（上下文工程可省 30-50%）；completion rate；context utilisation（注意力分析/消融测上下文实际被引用比例）。
- **检索/组装指标**（aicharcha）：retrieval recall@K（覆盖率缺口）/ first relevant rank（决定性证据多快出现）/ context precision（组装上下文被评审认为有用的份额）/ context recall（任务所需事实/来源进入上下文的份额）——context precision/recall 评"最终上下文包"不只搜索。
- **多代理专项**（clouatre）：inter-agent leakage rate（一个 agent 的 token 泄漏到另一个）/ retrieval precision@k（0.70@k=5 目标）/ task success delta（full-context vs scoped-context 的准确率差，正 delta 证明隔离提升表现）。
- **实证**（C4, arxiv 2606.10209）：last-5-tool-calls 修剪+摘要=91.6% 完整分项 / 99.64% 平均金额分项（对比 71.0%），同时 token 从 1.48M 减到 553K（-62.6%）。
- 判据：上下文质量先于模型能力——评估集测"模型拿到了够不够/对不对"；低于 85% 先 debug 上下文再怪模型。
