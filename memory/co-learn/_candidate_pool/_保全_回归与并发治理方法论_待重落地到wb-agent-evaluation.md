version: 3.293.0
## Token 预算分配公式：total=model_max×0.85（预留 15% 输出）· system ≤12% capped · history 35% dynamic decay · tools ≤4096（来源：CSDN SRE 拆解 Dify 上下文引擎（**total_budget = model_max_tokens * 0.85 保留 15% buffer for generation；system_tokens = min(2048, total_budget*0.12) capped & weighted；history_tokens = total_budget*0.35 dynamic decay；tools_tokens = min(4096,...)**）+ Wire 生产分配（**system 10-15% / tools 15-20% / retrieval 30-40% / history 20-30% / buffer 10-15%**）+ AgentixForce（**Mistake 2: 不预留输出空间——总是预留 1,500-2,500 tokens 给输出**）2026 实拉；与 §上下文预算管理（compressor 侧）分工——那边管"何时规划压缩"，本条管"窗口内各区域分多少 token"）
Token 先分账：总预算留 15% 输出，system/history/tools 按权重封顶，再按生产比例核对。
- **总预算公式**：**total = model_max×0.85，15% buffer 留给生成**（CSDN 原文）→ 判据：**先算总账**；生成区不许被输入挤占。
- **区域权重**：**system min(2048, 12%)·history 35% dynamic decay·tools min(4096)；生产比例 10-15/15-20/30-40/20-30/10-15**（CSDN+Wire 原文）→ 判据：**区域有配额**；超配即裁。
- **输出预留**：**至少 1,500-2,500 tokens 输出空间**（AgentixForce 原文）→ 判据：**输出先留**；不预留=生成被截断。
- **提升层**：工具/工作流（预算分配）。

## 上下文降级顺序与多级预算：4 轮工具→512 字节截断→移除更旧 · per_turn 12k/per_story 120k/per_feature 800k+模型路由升级（balanced→deep-reasoning）（来源：mayanklahiri/virtualme（**预留 512 tokens 给 chat-template+estimator error、≥1024 给 completion；放不下按序降级：①最多保留最近 4 轮工具轮次 ②较旧普通工具结果截断到前 512 字节 ③移除更旧工具轮次**）+ heymishy/skills-repo（**token_policy: per_turn_soft_budget 12000 / per_story_budget 120000 / per_feature_budget 800000；routing: default balanced → escalation deep-reasoning**）2026 实拉；与 §Token 预算分配公式（同轮 ①）分工——那边管"配额怎么分"，本条管"超配额时按什么顺序降级+多级预算怎么配模型"）
超限先降级：按固定顺序砍内容，多级预算配模型路由升级。
- **降级顺序**：**4 轮工具→旧工具结果截 512 字节→移除更旧轮次**（virtualme 原文）→ 判据：**顺序固定**；先保新近工具轮。
- **三级预算**：**per_turn 12k / per_story 120k / per_feature 800k 软预算**（heymishy 原文）→ 判据：**预算分层**；按任务粒度配。
- **模型路由**：**default balanced → escalation deep-reasoning**（heymishy 原文）→ 判据：**超预算升模型**；不是升提示。
- **提升层**：工具/工作流（预算治理）。

## token 用量监控与异常告警：per workflow/agent/tool call 跟踪 · 突增=prompt 问题/循环超预期/无界增长 · context usage 可视化（来源：n8n Production Playbook（**Monitor and set budgets：track token usage per workflow execution、per agent、per tool call；设异常消费告警阈值；token 突增通常=prompt 问题、循环跑超预期迭代、context 无界增长**）+ Make Reasoning tab（**Context usage 显示模型 context window 用量（如 575/400k tokens）**）2026 实拉；与 §Token 预算分配公式（同轮 ①）分工——那边管"分多少"，本条管"实际用了多少+异常怎么发现"）
用量先监控：每执行/每 agent/每工具调用记账，突增即查三类病因。
- **记账粒度**：**per workflow execution、per agent、per tool call 跟踪 token**（n8n 原文）→ 判据：**用量可归因**；异常能定位到层。
- **突增三因**：**prompt 问题 / 循环跑超预期迭代 / context 无界增长**（n8n 原文）→ 判据：**先查三类**；不是先调模型。
- **可视化**：**context usage 显示（575/400k）**（Make 原文）→ 判据：**用量可见**；每轮看余量。
- **提升层**：工作流（监控治理）。
## 共享状态隔离与并发异常：两+ agent 无隔离契约=race · 34% cache coherence 失败 split-reads 最常见 · 语义相等≠引用相等（CAS 失效）（来源：AgentPatterns（**两个及以上 agent 读写共享 memory store/vector index/tool registry 无隔离契约时出现 race conditions——与经典数据库并发控制同类异常；反模式=假设 agent stack 默认协调安全，通常因为 demo 跑两个 agent 没崩**）+ Daily AI World（**34% 多 agent 生产部署遭遇 cache coherence 失败，split-reads 最常见；agent LLM 调用 200ms-5s 期间共享状态可能被其他 agent 写；A/B 都写 approve 但一个指 approve transfer 一个指 approve display——传统 CAS 操作失效**）2026 实拉；与 §多 Agent 协作纪律（既有）分工——那边管"拆了怎么协作"，本条管"共享状态并发安全的隔离契约"）
共享状态先立契约：默认不安全，隔离+识别语义冲突。
- **隔离契约**：**两+ agent 读写共享 store 无隔离契约=race，与数据库并发异常同类**（AgentPatterns 原文）→ 判据：**先立契约**；demo 没崩≠安全。
- **量化风险**：**34% 部署 cache coherence 失败，split-reads 最常见；LLM 200ms-5s 期间状态被写**（Daily AI World 原文）→ 判据：**默认会坏**；读时状态可能已变。
- **语义冲突**：**同词不同义（approve transfer vs approve display）CAS 失效**（Daily AI World 原文）→ 判据：**比较语义**；不能只比 token。
- **提升层**：工作流（并发安全）。

## 记忆冲突仲裁：last-writer-wins 不安全（低能力覆盖高评估）· role/confidence-aware（orchestrator/voting/trust model）· 四失败模式（泄漏/陈旧传播/矛盾持续/来源崩溃）（来源：TechRxiv（**不同 agent 对同一事实得出不相容结论并写冲突条目；last-writer-wins 常不安全——低能力 agent 覆盖更好评估；MAS 需 role/confidence-aware 方案：orchestrator/voting/trust model 仲裁谁 authoritative；provenance 对此关键**）+ Governed Shared Memory（**shared memory 作为 governed operational state（scope/provenance/temporal supersession）；四失败模式：unauthorized leakage、stale propagation、contradiction persistence、provenance collapse**）2026 实拉；与 §共享状态隔离（同轮 ①）分工——那边管"防并发异常"，本条管"冲突发生后谁说了算+哪些失败模式要防"）
冲突先定仲裁：LWW 不安全，按角色/置信度仲裁；四失败模式逐项防。
- **仲裁方案**：**orchestrator/voting/trust model 决定哪个 entry 权威；低能力 agent 不得覆盖高评估**（TechRxiv 原文）→ 判据：**LWW 禁用于异质 agent**；仲裁有权重。
- **四失败模式**：**未授权泄漏 / 陈旧传播 / 矛盾持续 / 来源崩溃**（Governed 原文）→ 判据：**逐项检查**；陈旧与矛盾要显式解决。
- **provenance**：**写冲突条目时来源可追溯**（TechRxiv 原文）→ 判据：**条目带来源**；仲裁依赖它。
- **提升层**：工作流/可复用 Skill（冲突治理）。

## 写前查状态+并发写纪律：开工先 recall 最新状态防重复 · 乐观并发版本化（version 不匹配失败重试）· 主题分区（agent 各自 topic）· 默认 sequential writer（来源：AWS（**Pattern 1 Shared task state：多 agent 写分解任务进度到共享 memory；开工前先 query 最新状态避免重复——existing_work = recall_memories(query_text=f"progress on {task_id}")**）+ Yen.Dev Blackboard（**乐观并发版本化：每条目 version，writer 版本不匹配失败重试；主题分区：不同 agent 拥有不同 topic 无跨主题竞争；2026 多数框架默认 sequential writer，因为 LLM 调用够慢竞争罕见**）2026 实拉；与 §记忆冲突仲裁（同轮 ②）分工——那边管"冲突谁说了算"，本条管"写之前/写的时候怎么避免冲突"）
写前先查状态：开工 recall 进度防重复；写入用版本化或分区，必要时串行。
- **写前查**：**开工先 recall 最新状态（progress on {task_id}）避免重复工作**（AWS 原文）→ 判据：**先查后写**；防重复。
- **版本化**：**每条目 version，版本不匹配失败重试（乐观并发）**（Blackboard 原文）→ 判据：**写带版本**；冲突即重试。
- **分区与串行**：**agent 各拥 topic 无跨域竞争；2026 默认 sequential writer（LLM 慢，竞争罕见）**（Blackboard 原文）→ 判据：**先分区**；竞争少就串行。
- **提升层**：工具/工作流（写入纪律）。
## A/B 量化纪律：样本量非谈判（10k+/variant 或 power analysis 100-500）· eval harness 门禁（gold dataset semantic+schema）· guardrail metrics（latency/幻觉/cost bounds）赢者也不许破（来源：Zen van Riel（**A/B 需更大样本量+多指标评估（概率输出）；sample size non-negotiable：每 variant 计划 10,000+ interactions 分离信号与模型噪声；eval harness gates every ship：自动化 semantic+schema validation against gold dataset 在任何 variant 达用户前；guardrail metrics：latency/hallucination rate/cost bounds，赢的 variant 也不许破**）+ FeatBit（**AI 实验需一个 primary metric+几个 guardrails：primary 回答 treatment 是否值得保留，guardrails 回答 exposure 是否允许继续**）+ NiteAgent（**最小样本量由 power analysis 决定，通常 100-500 samples per variant 视 effect size**）2026 实拉；与 §评估驱动迭代（r627A 既有）分工——那边管"评估方法论"，本条管"A/B 实验的样本量/门禁/护栏量化"）
A/B 先定门槛：样本量按功效定，gold dataset 门禁，guardrails 对赢者同样生效。
- **样本量**：**10k+/variant 分离信号与噪声；或 power analysis 100-500/variant**（Zen+NiteAgent 原文）→ 判据：**先算样本**；样本不足=噪声当信号。
- **harness 门禁**：**semantic+schema 验证 against gold dataset，任何 variant 达用户前**（Zen 原文）→ 判据：**gold 先过**；不过不出门。
- **guardrails**：**latency/幻觉率/cost bounds，赢者也不许破；primary 管保留，guardrail 管暴露**（Zen+FeatBit 原文）→ 判据：**护栏独立于胜负**；赢不能破线。
- **提升层**：工具/工作流（A/B 纪律）。

## 回归验证分层：capability vs regression 分离双套件 · 版本化 test fixtures（生产失败变永久 case）· 分级容差（1-2% 精度 vs zero-tolerance 安全/schema）· regression_tolerance 2 分（来源：MLflow（**separate capability from regression：跑不同 eval suites 改进难任务+防已有功能回退；CI/CD regression gates 阻止部署（per-metric thresholds）；automated LLM judges 需连续 recalibrate against human-labeled sets**）+ AWS Bedrock AgentCore（**versioned test fixtures：author scenarios（inputs/expected outputs/assertions/tool sequences）publish 为 immutable numbered versions 不在 run 下漂移；mutable draft 迭代到锁 checkpoint；生产失败变永久 test case 每次部署重跑**）+ Codeables（**分级容差：允许 1-2% 精度损失 vs zero-tolerance failures（安全违规/schema 失败）**）+ Growth Engineer（**regression_tolerance：eval 有 run-to-run 噪声，允许分数降 2 点绝对分才 fail build**）2026 实拉；与 §A/B 量化纪律（同轮 ①）分工——那边管"新变体怎么测"，本条管"部署前回归怎么分层防回退"）
回归先分层：能力与回归分套件，fixtures 版本化，容差分级。
- **双套件**：**capability 套件改进难任务，regression 套件防回退**（MLflow 原文）→ 判据：**两套分开**；不混测。
- **fixtures 版本化**：**scenarios 发布为 immutable numbered versions；生产失败变永久 test case 每次部署重跑**（AWS 原文）→ 判据：**fixture 钉版本**；失败即入库。
- **容差分级**：**1-2% 精度损失可容忍；安全/schema 零容忍；分数降 2 点才 fail build**（Codeables+Growth 原文）→ 判据：**容差分层**；安全零容忍。
- **提升层**：工具/工作流（回归治理）。

## 统计回归判定：A/B 50x→p-value/effect size/95% CI · delta≥0 或 Welch t-test p≥alpha · per-segment diff（long-context↑ multi-tool↓）（来源：agent-regress-cli（**statistical regression testing：run version A/B 50x each→p-value/effect size/95% CI 判断行为是否真移动**）+ FutureAGI Four-Stage Gate（**delta = mean(candidate)-mean(baseline)；delta≥0 → no regression；否则 Welch t-test（ttest_ind equal_var=False）p 与 alpha 比较决定**）+ Codeables（**dashboard：overall diff/per-metric diff/per-segment diff（"improved on long-context queries, regressed on multi-tool flows"）**）2026 实拉；与 §回归验证分层（同轮 ②）分工——那边管"防回退的套件结构"，本条管"结果判定用统计还是目测"）
判定先统计：A/B 各 50 次出 p 值，delta≥0 即过，分段看 diff。
- **统计判定**：**A/B 各 50 次→p-value/effect size/95% CI**（agent-regress-cli 原文）→ 判据：**用统计判**；不凭感觉。
- **四阶段门**：**delta≥0 → no regression；否则 Welch t-test p≥alpha 才过**（FutureAGI 原文）→ 判据：**门禁公式化**；不合格不放行。
- **分段 diff**：**overall/per-metric/per-segment（long-context 提升但 multi-tool 回退）**（Codeables 原文）→ 判据：**分段看**；总体掩盖局部。
- **提升层**：工具/可复用 Skill（统计门禁）。
## 实测预算设定：有效窗口≠广告窗口（1M→200-300K 有效；400k→220k）· 压缩阈值按实测分布（873 次中位数 pre-compaction 575K/post 65K）· 预算目标设现实值（目标 30K 实际中位 62K）（来源：BurnRate《Context Window Quality Cliff》2026-05（**Claude Opus 4.7 广告 1M/有效 ~200-300K（90% 检索）/400K+ 急剧下降/1M 时 78%→32% MRCR**）+ BenchLM《Advertised vs Effective》（**advertised 是箱子尺寸，effective 是模型真能无损推理的量；marketing number 不随 recall curve 移动**）+ FutureAGI（**GPT-5.1 广告 400k/有效 ~220k（RULER multi-needle）**）+ LangWatch《Optimal Context Window》（**873 次 compaction 中位数：pre-compaction 574,875 / post-compaction 65,588 / summary 4,382**）+ aura-frog TOKEN_BUDGET（**Target: ≤30K tokens per workflow. Actual median: 62K**）2026 实拉；与 r628A 既有 §Token 预算分配公式 分工——那边管"按广告窗口的分配公式"，本条管"预算值该按实测有效窗口与分布定"）
预算先实测：按有效窗口设上限，压缩阈值用实测分布，目标值设现实。
- **有效窗口**：**广告 1M 有效 200-300K；广告 400k 有效 ~220k**（BurnRate+FutureAGI 原文）→ 判据：**按有效窗口定预算**；不按规格书。
- **压缩阈值**：**873 次实测中位数 pre-compaction 574,875（~58% 窗口）触发、post 65,588（~6.5%）**（LangWatch 原文）→ 判据：**阈值用实测分位**；拍脑袋的 80% 常晚。
- **现实目标**：**目标 30K 实际中位 62K**（aura-frog 原文）→ 判据：**目标设现实值**；预算贴着实际走。
- **提升层**：工具/工作流（预算设定）。

## 实测 prompt 组成与分桶：会话历史 48%+函数调用 28%+system 14%+repo 10% · 四桶预算（system 500-2000 固定/history 最易失控/retrieved 按质量/输出保留）· 用户异质性 50x（5 archetypes）（来源：arXiv《Agentic Coding in the Wild: Characterizing GitHub Copilot at Production Scale》2608.00101（**prompt 组成：Conversation history 48%/Function-call messages 28%/System prompt 14%/Repo instructions and context 10%；users highly heterogeneous 50x token range across 5 archetypes；工作日 prompt-token 1.2-1.7M、周末 1.9-2.4M**）+ Agency Script《Token Limits in Production》（**四桶：system 固定 500-2000 保持恒定/history 最易失控最常被搞错/retrieved context 按检索质量而非便利定大小/output reservation 预留输出**）2026 实拉；与 §实测预算设定（同轮 ①）分工——那边管"总量设多少"，本条管"总量怎么按实测分给各组件"）
分桶先实测：按生产数据组成分预算，history 是最大变数。
- **实测组成**：**会话历史 48%/函数调用 28%/system 14%/repo 10%**（arXiv 原文）→ 判据：**按组成分桶**；不是平均分。
- **四桶模型**：**system 500-2000 固定；history 最易失控；retrieved 按检索质量定；输出保留**（Agency Script 原文）→ 判据：**history 单独管**；它是最大漏洞。
- **异质性**：**用户间 50x token 范围、5 archetypes**（arXiv 原文）→ 判据：**按人设预算**；全局中位数不适合重用户。
- **提升层**：工作流（分桶预算）。

## 每步成本累积与溢出处理：reasoning 150+call 100+result 500=750/步 · 输出保留 1000 · count→check→prune→compress→checkpoint→rebuild→re-check · budget manager 跟踪每组件+强制限额（来源：BrainDrip《Context Window Pressure》（**每步成本累积：Agent reasoning/CoT 150 + tool call 100 + tool result 500 = 750/步；输出保留 1,000 tokens must be reserved**）+ AgentixForce《Context Window Budgeting》（**溢出处理流程：Count tokens→Budget check→Prune 低相关→Compress 摘要旧轮→Checkpoint 状态快照→Rebuild 重建→重跑 budget check**）+ Yen.Dev《Context Engineering》（**budget manager 跟踪每组件 token 用量并强制限额；滑动窗口保留 K 最近轮全文、旧轮丢弃或摘要**）2026 实拉；与 §实测 prompt 组成（同轮 ②）分工——那边管"静态分桶"，本条管"运行时逐步骤累积与溢出动作"）
溢出先预算：每步成本可加，输出保留不可动，溢出走五步流程。
- **每步成本**：**750/步（reasoning 150+call 100+result 500）；多步任务预算=750×步数+输出保留 1000**（BrainDrip 原文）→ 判据：**步数×单步**；长任务预算先按步数估。
- **溢出流程**：**count→check→prune→compress→checkpoint→rebuild→重查**（AgentixForce 原文）→ 判据：**流程固定**；溢出不随机删。
- **预算管理器**：**跟踪每组件用量+强制限额；滑动窗口 K 最近轮**（Yen.Dev 原文）→ 判据：**组件可审计**；限额强制非建议。
- **提升层**：工具/可复用 Skill（溢出治理）。
## 工具错误分类驱动策略：无效参数→结构化错误返回模型恢复 · 外部 API 瞬时失败→指数退避≤3 · 认证失败→立即返回不重试 · 资源错误→降级运行（预算/超时/记忆超限 graceful degradation with reduced capability）（来源：Ransford Notes《Tools and Actions》2026-09（**Invalid parameters（如不存在的 ticker symbol）应返回 structured error object 让模型决定如何恢复；External API failures（rate limits/timeouts）触发 exponential backoff 最多 3 次再返回错误；Authentication failures 立即返回不重试——retrying with an expired credential wastes time**）+ AI Agents Plus《Error Handling & Retry Strategies》2026-03（**四类错误：Hallucinations/Tool call errors（invalid params）/Format violations（schema 不符）/Safety issues→Strategy: validation, re-prompting, or fallback to safer models；Resource Errors（Budget limits/Timeout limits/Memory limits）→Graceful degradation with reduced capability**）2026 实拉；与 r628B 既有 §重试分两类管（transport vs tool）分工——那边管"重试的归类"，本条管"按错误类型决定策略（含不重试）"）
错误先分类：类型决定策略——可重试/不可重试/交模型恢复/降级。
- **三型策略**：**无效参数→结构化错误交模型恢复；瞬时 API 失败→指数退避≤3；认证失败→立即返回不重试**（Ransford 原文）→ 判据：**按类型分流**；认证失败重试=白费时间。
- **四类错误**：**幻觉/工具调用错误/格式违规/安全→验证或 re-prompt 或回退更安全模型**（AI Agents Plus 原文）→ 判据：**错误有分类法**；不一律重试。
- **资源降级**：**预算/超时/记忆超限→降级运行（reduced capability）而非崩溃**（AI Agents Plus 原文）→ 判据：**资源错误降级**；降级优于失败。
- **提升层**：工具/工作流（错误策略）。

## handler 与模型分工+错误作为数据：handler 管瞬时重试（指数退避）、模型管语义恢复 · 工具错误返回 content+is_error:true 不抛异常（异常杀死循环）（来源：Anthropic《Handle tool calls》官方（**工具执行错误（如网络错误）在 content 中返回错误消息+is_error: true**）+ Developers Digest《Tool Use in the Claude API: Production Patterns》（**errors come back as data, not exceptions——throwing an exception kills the loop；Transient network errors 应在 handler 内指数退避重试；Permanent errors（4xx, validation）返回给 Claude 让模型决定；mental model: the handler is responsible for transient retries, Claude is responsible for semantic recovery**）2026 实拉；与 §工具错误分类（同轮 ①）分工——那边管"分类"，本条管"谁负责什么+错误形态"）
分工先明确：瞬时重试归 handler，语义恢复归模型，错误当数据不当异常。
- **错误即数据**：**工具错误返回 content+is_error:true；抛异常杀死工具循环**（Anthropic+Developers Digest 原文）→ 判据：**错误走返回不走异常**；异常=循环终结。
- **双层分工**：**handler 管瞬时重试（指数退避）；4xx/校验永久错误返回给模型语义恢复**（Developers Digest 原文）→ 判据：**分工固定**；模型不背瞬时重试的锅。
- **提升层**：工具/可复用 Skill（错误形态与分工）。

## 断路器三态与 retry storm 防制：3-5 连续失败→打开 fail-fast→cooldown→half-open 测试调用 · per-provider 隔离 · jitter 非谈判（1s/32s/0.5-1.5x）防协调雪崩 · node-level 固定延迟无 jitter 是陷阱（来源：Quantum Flow《Five Patterns That Make Tool Calling Production-Reliable》（**断路器跟踪工具连续失败，阈值通常 3-5 连续失败打开：所有调用立即失败不再尝试超时；cooldown 后半开允许一个测试调用，成功→关闭恢复正常，失败→保持打开**）+ DEV/Dify（**Redis 分布式断路器状态、5 连续失败 fail-fast 60 秒、per-provider 隔离——OpenAI 故障不触发 Anthropic breaker**）+ TianPan《CAP Theorem for AI Agents》（**指数退避+jitter 非谈判：初始 1s/最大 32s/jitter 0.5-1.5x 防协调重试雪崩；无 jitter 的同步重试多实例造成 retry storm 加重 outage**）+ n8n DEV《Retry Storms》（**node-level Retry On Fail 是固定延迟 per-item per-worker，无 jitter 无跨 worker breaker；queue 模式 retry 状态 per-process**）2026 实拉；与 §重试分两类管 分工——那边管"重试参数"，本条管"断路器状态机与重试风暴机制"）
断路器先三态：打开即 fail-fast，半开放行一个测试，jitter 必须有。
- **三态机**：**3-5 连续失败打开→所有调用立即失败→cooldown→half-open 一个测试调用，成功关闭/失败保持**（Quantum 原文）→ 判据：**打开即拒**；不再试超时。
- **隔离与分布**：**per-provider 隔离（OpenAI 故障不触发 Anthropic breaker）；分布式状态（Redis）**（Dify/DEV 原文）→ 判据：**按依赖隔离**；一个故障不株连全家。
- **jitter 非谈判**：**初始 1s/最大 32s/抖动 0.5-1.5x；无 jitter 同步重试=retry storm 加重 outage；框架内置固定延迟（无 jitter 无跨 worker breaker）是陷阱**（TianPan+n8n 原文）→ 判据：**重试必须抖动**；固定延迟重试会放大故障。
- **提升层**：工具/工作流（断路器与重试风暴）。
## 分级路由与"最便宜能过的"原则：按任务复杂度分档（简单分类→Haiku/GPT-4o-mini · 结构化提取→Sonnet/GPT-4o · 复杂推理→Opus/GPT-4）· offline gate 先过再上 · 质量地板保护（初始响应低于阈值自动升级更强模型）（来源：Alibaba Cloud《Model Routing Explained: Send Each Request to the Cheapest Model That Passes》（**路由核心=send each request to the cheapest model that passes——offline gate 先过再上**）+ Claude《Choosing the right model》官方（**balance capabilities, speed, and cost；Sonnet 5.5 日常 coding/agent/enterprise 默认；升级标准数据驱动非 vibes，output_config.effort 每档先调再上大模型**）+ Mahmoud Zalt《Which Model Should You Use for Your AI Agent》（**routing/classification→Haiku 4.5；tool-calling/structured output→Sonnet 4.6；complex multi-step reasoning→Opus 4.8——按角色匹配降 60-80% 成本**）+ Microsoft Learn《Optimize Multi-Agent Performance》（**routing strategy with quality floor protection：初始响应低于质量阈值自动升级到更强模型，防成本优化劣化体验**）2026 实拉；与 r628C 既有 §A/B 量化纪律 分工——那边管"怎么测新变体"，本条管"生产流量怎么分到模型档"）
路由先分级：任务复杂度→模型档，offline gate 把关，质量地板兜底。
- **按复杂度分档**：**简单分类→Haiku/GPT-4o-mini；结构化提取→Sonnet/GPT-4o；复杂推理→Opus/GPT-4；每请求选最便宜能过的**（Zalt+Alibaba 原文）→ 判据：**先分级再路由**；不分级=全用贵的。
- **gate 与地板**：**offline gate 先过再上；初始响应低于质量阈值自动升级更强模型（quality floor protection）**（Alibaba+Microsoft 原文）→ 判据：**有门禁有兜底**；便宜档不裸奔。
- **升级标准数据驱动**：**升级标准是数据不是感觉；每档先调 output_config.effort 再上大模型**（Claude 原文）→ 判据：**先调小档**；不急着上大模型。
- **提升层**：工具/工作流（分级路由）。

## 路由经济学与何时不路由：省 60-80%（价格差 50x/70%）· 70% 流量是简单/中等先路由出 frontier · 月 1 万请求以下或单一任务类型不路由（router 维护成本超节省）· 分类决策用类型化分类器（$0.000006 vs $0.02，3000x）（来源：OverpayingForAI《AI Model Routing》（**通常省 60-80% API 支出；价格差：DeepSeek V4 Flash 输入比 GPT-5.4 便宜 50x、GPT-5.4 mini 便宜 70%——每个通过便宜档审查的请求都是省下的钱**）+ Developers Digest《Model Routing Recipes》（**70% 流量是简单/中等工作，把该份额路由出 frontier=可持续账单 vs 预算爆掉；开源权重编码模型约 1/6 frontier 每 token 价**）+ Alibaba Cloud（**When not to route：月 1 万请求 all-Max 账单 $70，router 构建维护成本超过节省；单一任务类型直接选最便宜能过 offline gate 的档**）+ DEV《Your Agent Harness Is Paying LLM Prices for Classifier Decisions》（**router decision 本质是分类问题：typed classifier ~$0.000006/决策 vs frontier LLM ~$0.02/决策**）2026 实拉；与 §分级路由（同轮 ①）分工——那边管"怎么分档"，本条管"什么时候值得路由+路由决策本身怎么省"）
路由先算账：值得才路由，分类决策用便宜分类器。
- **节省量级**：**通常省 60-80%；价格差 50x/70%；开源编码模型约 1/6 frontier 价**（Overpaying+Developers Digest 原文）→ 判据：**有价差才路由**；无价差白折腾。
- **何时不路由**：**月 1 万请求以下或单一任务类型不路由（维护成本超节省）**（Alibaba 原文）→ 判据：**量小不路由**；router 也有成本。
- **分类器代替 LLM**：**路由决策是分类不是生成：typed classifier ~$0.000006 vs frontier LLM ~$0.02（3000x）**（DEV 原文）→ 判据：**分类决策用分类器**；别为路由付 LLM 价。
- **提升层**：工作流（路由经济学）。

## 预算硬上限与成本感知选型：virtual key 硬预算到顶即停（失控任务/泄漏 key 不能悄悄烧钱）· max_price 硬上限（无 provider 符合则失败而非超支）· 按 max(context,required)×input+output×output 成本排序选模型（输出重任务选便宜输出模型）（来源：LiteLLM 官方（**attribures every request automatically、每团队 virtual key with a hard budget；key 到顶即停——runaway job 或 leaked key 不能 quietly run up the bill；spend 导出 Prometheus/Datadog/CloudZero chargeback**）+ OpenRouter《Lowest-Cost LLM Inference》（**`:floor` 后缀总是路由到该模型最便宜 provider；`max_price` 硬预算上限——无 provider 符合则请求失败而非花超计划的钱；最便宜列表价有时是 quantized 端点**）+ pi-auto-model（**cost policy 按本次请求估计成本排序：max(context, required) tokens × input price + required output tokens × output price——输出重任务偏好便宜输出模型、大缓存上下文偏好便宜输入模型**）2026 实拉；与 §路由经济学（同轮 ②）分工——那边管"要不要路由"，本条管"预算怎么硬性兜底"）
预算先硬上限：key/max_price 到顶即停，选型按本次请求成本排序。
- **硬预算**：**virtual key 硬预算到顶即停；max_price 无 provider 符合则失败而非超支**（LiteLLM+OpenRouter 原文）→ 判据：**预算硬性**；失控任务烧到顶即停。
- **成本感知排序**：**按 max(context,required)×input+output×output 选模型——输出重选便宜输出、缓存大选便宜输入**（pi-auto-model 原文）→ 判据：**按请求成本排序**；不看裸价目表。
- **`:floor` 最低价**：**总是路由到该模型最便宜 provider；警惕最便宜列表价是量化端点**（OpenRouter 原文）→ 判据：**同模型取 floor**；但量化端点要辨。
- **提升层**：工具/工作流（预算硬上限）。
## 本地推理引擎选型决策树：Ollama=本地/开发最易（单二进制·GGUF·CPU 可跑）· vLLM=GPU 生产最快（continuous batching/PagedAttention/OpenAI 兼容 API）· llama.cpp=纯 CPU 最优（比 Python 框架快 3-8x）· LM Studio=非技术用户 GUI · 别把 Ollama 当高吞吐多用户服务器（来源：Zero to AI《05 LLM Server And API》（**Ollama 是开发最易起点；vLLM 是 GPU 生产最佳；llama.cpp server 在纯 CPU 机器上赢；LM Studio 对非技术用户最好；Apple Silicon 用户经 Ollama 免费获得 Metal GPU 加速；GGUF Q4_K_M 是推荐默认量化——质量损失最小+只占 fp16 的 25% 内存；自托管在规模上相对 API 定价显著省钱；监控 latency p95**）+ DEV《Deploying LLMs Locally: Ollama, llama.cpp, and vLLM Comparison》（**vLLM continuous batching+PagedAttention；llama.cpp CPU 比 Python 框架快 3-8 倍**）+ negiadventures《Quantization Coding Models》（**Ollama 别当高吞吐多用户推理服务器用**）+ n8n blog《Self-Hosted LLM vs Cloud APIs》2026 实拉；与 r629C 既有 §分级路由 分工——那边管"云端模型怎么分档路由"，本条管"本地引擎怎么选怎么搭"）
本地先选引擎：按硬件与场景选，别一律 Ollama。
- **四引擎定位**：**Ollama=开发/本地最易；vLLM=GPU 生产最快；llama.cpp=纯 CPU 最优（快 3-8x）；LM Studio=非技术用户 GUI**（Zero to AI+DEV 原文）→ 判据：**按场景选引擎**；开发用 Ollama、生产 GPU 用 vLLM、纯 CPU 用 llama.cpp。
- **默认量化**：**GGUF Q4_K_M 推荐默认——质量损失最小+只占 fp16 的 25% 内存**（Zero to AI 原文）→ 判据：**本地默认 Q4_K_M**；内存紧张再降档。
- **定位边界**：**Ollama 别当高吞吐多用户推理服务器**（negiadventures 原文）→ 判据：**Ollama 管小规模**；多用户并发上 vLLM。
- **提升层**：工具/工作流（引擎选型）。

## OpenAI 兼容 API=本地-云端万能接口：Ollama/vLLM/llama.cpp 均暴露 OpenAI 兼容端点——改一个 Base URL 切换本地/云端 · Claude Code 三环境变量（ANTHROPIC_BASE_URL+ANTHROPIC_AUTH_TOKEN=ollama+API_KEY 留空）接本地 · Make 用 HTTP 模块无鉴权头 · Activepieces openai-custom piece（来源：SitePoint《Claude Code on Ollama》（**ollama pull qwen2.5-coder:14b→curl localhost:11434/v1/chat/completions 验证→Claude Code 指向本地 API**）+ 腾讯云《Claude Code 完美接入 Ollama》（**export ANTHROPIC_AUTH_TOKEN=ollama；export ANTHROPIC_BASE_URL=http://localhost:11434；claude --model qwen2.5-coder:7b**）+ Ertas AI《Make.com + Local AI》（**Ollama 是 OpenAI-compatible API；Make 用 HTTP 模块 POST /v1/chat/completions，无需 Authorization header**）+ Activepieces openai-custom（**连任何 OpenAI 兼容自托管/代理端点：Ollama/OpenRouter/vLLM/LiteLLM/LM Studio/Groq/FastChat/Azure 代理**）+ Zero to AI（**OpenAI 兼容=改一个 URL 切换本地与 OpenAI**）2026 实拉；与 §本地引擎选型（同轮 ①）分工——那边管"选哪个引擎"，本条管"应用怎么连本地"）
本地先连 API：OpenAI 兼容是万能接口，应用端只改 Base URL。
- **万能兼容**：**Ollama/vLLM/llama.cpp 都暴露 OpenAI 兼容端点；改一个 URL 在本地与 OpenAI 间切换**（Zero to AI 原文）→ 判据：**本地部署优先选 OpenAI 兼容暴露**；应用端零改造。
- **Claude Code 接本地**：**ANTHROPIC_BASE_URL 指向本地 + AUTH_TOKEN=ollama + API_KEY 留空 + claude --model qwen2.5-coder:7b**（腾讯云原文）→ 判据：**三变量+--model**；一条命令切换云端/本地。
- **无鉴权头**：**本地 Ollama 无需 Authorization header**（Ertas AI 原文）→ 判据：**本地端点免鉴权**；云端才配 key。
- **提升层**：工具/工作流（本地接入）。

## 量化格式决策树与默认档：CPU→GGUF（Q4_K_M 默认，25% fp16 内存）· reasoning→FP8 · multi-LoRA→GPTQ · 常规 GPU 聊天→AWQ · 消费级→GPTQ/AWQ-4bit · A100/H100→BF16 · GGUF 单文件自包含但 GPU 非最优（CPU/Metal 设计）· 关键层 16-bit 其余 4-bit（UD quants 小模型不丢精度）（来源：quantization-picker 决策树（**CPU→GGUF；reasoning→FP8；multi-LoRA on vLLM→GPTQ；routine GPU chat→AWQ；产出 GGUF Q4_K_M/Q5_K_M/GPTQ-Int4+Marlin/AWQ-Int4+Marlin/FP8/NVFP4+FP8 KV 按决策树选**）+ Zero to AI（**消费级 GPU→GPTQ-4bit 或 AWQ-4bit；CPU/Edge→GGUF Q4_K_M 或 Q5_K_M；A100/H100→BF16 或 AWQ-4bit**）+ yennanliu skill-quantization（**GGUF 变体 Q2_K/Q3_K_S/M/L/Q4_K_S/M/Q5_K；推荐默认 Q4_K_M 质量/体积最佳；GGUF 自包含单文件、混合精度、大生态；弱点=非 GPU 最优（设计给 CPU/Metal）**）+ Unsloth Dynamic 2.0（**UD quants 关键层保持 16-bit 精度、其余压到 4-bit——小模型量化不丢精度的核心**）2026 实拉；与 §本地引擎选型（同轮 ①）分工——那边管"选引擎"，本条管"模型怎么量化"）
量化先按决策树：格式跟着硬件和用途走，默认 Q4_K_M。
- **决策树**：**CPU→GGUF；reasoning→FP8；multi-LoRA→GPTQ；常规 GPU 聊天→AWQ；消费级→GPTQ/AWQ-4bit；A100/H100→BF16/AWQ-4bit**（quantization-picker+Zero to AI 原文）→ 判据：**按硬件+任务选格式**；别一律 4-bit。
- **默认档**：**Q4_K_M 质量/体积最佳平衡；CPU/Edge 用 Q4_K_M/Q5_K_M**（yennanliu 原文）→ 判据：**本地默认 Q4_K_M**；有理由才换。
- **格式本质**：**GGUF 自包含单文件、混合精度；设计给 CPU/Metal 非 GPU 最优**（yennanliu 原文）→ 判据：**GPU 场景别硬用 GGUF**；选 GPTQ/AWQ。
- **小模型不丢精度**：**关键层保持 16-bit 其余 4-bit（UD 2.0）——标准量化在小模型上丢精度，混合精度保关键层**（Unsloth 原文）→ 判据：**小模型用动态量化**；保住关键层。
- **提升层**：工具/可复用 Skill（量化决策）。
## 多 agent 三规则先导+编排模式权衡：先单 agent（协调只在 demonstrably fails 时加）· Pattern>framework（同模式跨 LangGraph/CrewAI/AutoGen 移植）· 每 agent 必须有预算（turns/tokens/tools/wall-clock，否则是 bug）· Pipeline=固定序列易调试但错误累积 · Supervisor/Worker=动态分解但路由可能错 · Swarm=并行探索须硬性轮数上限 · Blackboard=共享工作空间（来源：ai-portal《Multi-Agent Orchestration》（**Anthropic rule of thumb：01 Start with a single agent. Add coordination only when it demonstrably fails；02 Pattern > framework——同一模式可跨 LangGraph/CrewAI/AutoGen 移植；03 Every agent must have a budget—turns, tokens, tools, wall-clock. Or it's not an agent, it's a bug**）+ aibuilderclub《Agents 101 Part 4》（**Pipeline：固定变换序列、简单可预测易调试、错误累积一个坏步骤毁全部下游；Supervisor/Worker：任务结构复杂或随输入变化、灵活处理边界、supervisor 可能做坏路由决策难调试计划**）+ MESHLAUNCH《多Agent协作架构实战》（**Swarm：Agent 点对点传递任务无中央协调者、靠终止规则停止——生产环境慎用须设硬性轮数上限（AutoGen GroupChat+max_round）；Blackboard：所有 Agent 共享结构化工作空间**）+ Knowlee《Orchestration Guide 2026》2026 实拉；与既有 §多 Agent 协作纪律 分工——那边管"拆了之后怎么协作（按技能建/共享层/质检）"，本条管"选哪种编排形状+每 agent 必须有预算"）
多 agent 先守三规则：单 agent 起步、Pattern 优先于框架、每 agent 有预算。
- **三规则**：**先单 agent，协调只在 demonstrably fails 时加；Pattern > framework（同一模式跨框架移植）；每 agent 必须有预算（turns/tokens/tools/wall-clock）否则是 bug**（ai-portal 原文）→ 判据：**先单后多**；模式可移植、框架不可锁死；没预算的 agent 是失控。
- **模式权衡**：**Pipeline=固定序列易调试但错误累积（坏一步毁下游）；Supervisor/Worker=动态分解灵活但路由可能错难调试计划**（aibuilderclub 原文）→ 判据：**按任务确定性选模式**；固定流程用 Pipeline、变化任务用 Supervisor。
- **Swarm 边界**：**Swarm 点对点无中央协调、靠终止规则停——生产环境须硬性轮数上限**（MESHLAUNCH 原文）→ 判据：**Swarm 设轮数上限**；否则无限对话。
- **提升层**：工作流/可复用 Skill（模式选择）。

## Handoff 契约与防 stale：well-formed handoff summary 是 coordinator 契约（type/reason/urgency）· 80% 上下文创建的 handoff 变 stale——委派 agent 用 fresh context+实现一任务+完成时创建 handoff+磁盘持久化（压缩后重读继续）· 动态 handoff（@tool 返回 Handoff 实例按返回值路由非图边）（来源：ccaf-exam《Coordinator–Subagent Patterns》（**well-formed handoff summary 是 coordinator 契约一部分：handoff type=human_escalation/reason=policy_exception_required/urgency=medium/customer…**）+ Continuous-Claude v3（**Handoffs created at 80% context become stale——委派给 agents：fresh context 起步、实现一个任务、完成时创建 handoff、返回 orchestrator；handoffs 持久化磁盘，压缩后重读继续**）+ AG2 Action-Driven Network（**任何 @tool 可返回 Handoff 实例——框架从工具结果提取目标覆盖该轮图规则，drafter 不需要单独 ToolCalled 路由**）+ Agiflow（**团队靠纪律架构不靠更好模型：role separation/handoff contracts/verification gates 在漂移传播前抓住**）2026 实拉；与 §多 agent 三规则（同轮 ①）分工——那边管"模式选择"，本条管"交接怎么设计怎么防 stale"）
交接先立契约：handoff 有模板、防 stale 靠委派+磁盘持久化、动态路由按返回值。
- **契约模板**：**handoff summary 是 coordinator 契约：type/reason/urgency/customer 等字段**（ccaf-exam 原文）→ 判据：**交接有固定字段**；缺字段=交接失败。
- **防 stale**：**80% 上下文创建的 handoff 变 stale——委派 agent fresh context+完成时创建 handoff+磁盘持久化（压缩后重读继续）**（Continuous-Claude 原文）→ 判据：**交接在任务完成时创建**；压缩不丢交接。
- **动态路由**：**@tool 返回 Handoff 实例——按返回值覆盖图规则**（AG2 原文）→ 判据：**动态交接按结果路由**；不需预设边。
- **提升层**：工作流/可复用 Skill（交接契约）。

## Agent 预算与按角色分模型：按 agent 监控成本（每 agent 每任务类型追踪+超阈值告警）· 只对强推理角色用高端模型（supervisor/代码），范围窄的 agent（研究/审查）用低成本模型——成本降 40% · 模型异构（supervisor 生成 JSON 任务队列+执行 agent 干确定性活；Opus 高层+Sonnet 执行）（来源：腾讯云《多智能体三种编排模式》（**按每个智能体、每种任务类型追踪成本，单次任务费用超阈值触发告警；核心优化=只对真正需要强推理的角色（supervisor、代码智能体）用高端模型，任务范围更窄的智能体（研究、审查）换低成本模型——成本降 40%**）+ singularitymoments《Inside Dify》（**模型异构：DeepSeek-R1/Claude 3.5 Sonnet 当 supervisor 生成结构化 JSON 任务队列；Qwen2.5-Coder-32B/GPT-4o 干确定性代码生成与工具调用**）+ Make Mary（**Claude Opus 4.6 高层推理+Sonnet 4.6 sub-agents 执行**）+ Dify 华为云（**R1 规划+V3 执行**）2026 实拉；与 §分级路由（r629C）分工——那边管"单请求怎么选档"，本条管"多 agent 系统按角色分模型"）
多 agent 先分模型：强推理角色用贵模型、范围窄角色用便宜模型，成本降 40%。
- **按角色分档**：**只对 supervisor/代码等强推理角色用高端模型；研究/审查等窄任务用低成本模型——成本降 40%**（腾讯云原文）→ 判据：**角色定档**；全用高端=浪费。
- **模型异构**：**supervisor 生成 JSON 任务队列（R1/Claude 3.5）+执行 agent 干确定性活（Qwen2.5-Coder-32B/GPT-4o）；Opus 高层+Sonnet 执行**（singularitymoments+Make 原文）→ 判据：**规划/执行分模型**；规划重推理、执行重确定。
- **成本监控**：**每 agent 每任务类型追踪成本+超阈值告警**（腾讯云原文）→ 判据：**按 agent 记账**；谁烧钱看得见。
- **提升层**：工具/工作流（按角色分模型）。
## 回归阈值双表与灰度放量：pass rate 跌 >3% 阻止部署 · Kanopy 多阈值（完成率跌>2pp/高严重度用例开始失败/平均成本涨>20% 阻止 merge）· RockB 双表（CI Gate 85%/95%/0 vs Production SLO 90%/98%/0）· 10% 灰度 48-72h online eval 再全量 · 路由感知阈值（threshold table 在 CI config：casual_chat groundedness 0.70 vs support_agent 0.80）（来源：Kunalganglani《3-Level Framework》（**Level 1 unit tests→Level 2 LLM-as-judge golden dataset 对比 pass rate→3% 回归阈值阻止部署；10% 流量灰度+online eval 48-72h**）+ Kanopy《Agent Testing Frameworks》（**CI 对比 eval 结果 baseline=main 分支；任务完成率跌>2pp、之前通过的高严重度用例开始失败、平均每任务成本涨>20% 任一触发阻止 merge；PR 发详细对比评论显示场景+实际 agent 输出**）+ RockB《Agent CI/CD Eval Pipeline》（**指标表 CI Gate vs Production SLO：task completion 85% vs 90%；grounded response 95% vs 98%；policy violations 0；p95 latency**）+ Future AGI《LLM Eval vs Software Testing》（**路由感知阈值：threshold table 住 CI config 不住测试体——ROUTE_THRESHOLDS={casual_chat: groundedness 0.70/task_completion 0.75；support_agent: 0.80/0.85；regulated_advice…} 按路由分档**）2026 实拉；与既有 §三级测试栈 分工——那边管"测什么层级"，本条管"阈值定多少+怎么放量"）
回归先定阈值：pass rate 3% 起步、多指标组合、灰度 10% 48-72h。
- **单一阈值**：**pass rate 跌 >3% 阻止部署；10% 流量灰度+online eval 48-72h 再全量**（Kunalganglani 原文）→ 判据：**3% 起步**；灰度验证后再放量。
- **组合阈值**：**完成率跌 >2pp / 高严重度用例开始失败 / 平均成本涨 >20%——任一阻止 merge**（Kanopy 原文）→ 判据：**多指标组合**；不只盯一个。
- **双表**：**CI Gate 85%/95%/0 vs Production SLO 90%/98%/0**（RockB 原文）→ 判据：**门禁严于生产**；SLO 是运营承诺。
- **路由感知**：**阈值表在 CI config 按路由分档（casual 0.70 vs support 0.80）**（Future AGI 原文）→ 判据：**不同路由不同阈值**；不写死测试体。
- **提升层**：工具/工作流（阈值与放量）。

## CI evals 工程四要：PR 门小高信号（几百例）+大套件 nightly · 缓存确定性部分（tool mocks/retrieval results）· 便宜 judge 模型粗评分 · 强制时间限制（evals 别成 40 分钟 commit 税）· eval job 设为 required status check（来源：Kunal Ganglani《Regression Gates》（**PR 门保持小高信号（几百例）跑得快；大套件 nightly；缓存确定性部分如 tool mocks 和 retrieval results；便宜 judge 模型粗评分；强制时间限制——evals 别变成每次 commit 的 40 分钟税**）+ AWS Bedrock AgentCore 参考实现（**GitHub Actions 部署 agent+OAuth MCP server→test prompts 调用评分→行为回归阻止 PR；配置 eval job 为 required status check 通过 branch protection/rulesets 防合并**）+ ScrollTest PromptFoo CI Eval Gate（**QA 团队测 UI 跳过 prompt 行为本身——昂贵回归藏那里；每个 PR 跑+证据+告诉团队 AI 改动安全与否**）2026 实拉；与 §回归阈值（同轮 ①）分工——那边管"阈值定多少"，本条管"evals 在 CI 怎么跑"）
CI evals 先控成本：小门+夜跑+缓存+时间限制，eval job 设为 required check。
- **分层跑**：**PR 门几百例高信号；大套件 nightly；缓存确定性部分（tool mocks/retrieval）**（Kunal 原文）→ 判据：**快慢分离**；PR 不背夜跑。
- **时间限制**：**强制时间限制——evals 别成 40 分钟 commit 税**（Kunal 原文）→ 判据：**设硬时限**；超时降级。
- **门禁机制**：**eval job 设为 required status check（branch protection/rulesets）**（AWS 原文）→ 判据：**merge 前强制过 eval**；不是建议。
- **提升层**：工具/工作流/可复用 Skill（CI evals）。

## 三套件裁决与数据治理：JSON 结构化裁决+锚点校准+人工抽检（推理模型当裁判模糊判定稳定）· 每个生产失败变回归测试（tag incident，回归套件编码每个硬教训）· 从 20-50 个真实生产失败用例起 · Error Feed 每周推进 vs frozen baseline 反模式（2024 集评 2026 产品是 benchmark 非回归套件）（来源：华为云《Agent 评测体系实战》（**DeepSeek-R1 当裁判：推理模型在模糊判定上稳定性优势；JSON 结构化裁决+锚点校准+人工抽检三件套；三件套落地=离线评测工作流（批量跑+R1 裁决+聚合报告）、线上灰度对比（同请求双跑+对比裁决）、CI 回归门禁（阈值+版本管理）；Agent 迭代必须从"感觉"升级为评测驱动**）+ Kanopy（**每个生产失败变成回归测试——agent 处理错的 edge case 加到测试套件带正确预期；回归套件随时间成为最有价值资产编码每个硬教训；tag 回归测试带引发它的 incident**）+ RaftLabs（**从 20-50 个真实生产失败用例起**）+ Future AGI（**Error Feed 每周推进；静态数据集冻结=2024 集评 2026 产品是 benchmark 不是回归套件**）2026 实拉；与 §CI evals 工程（同轮 ②）分工——那边管"CI 怎么跑"，本条管"用例从哪来+怎么审"）
评测先治理数据：生产失败入库、每失败一回归、基准每周滚。
- **三件套**：**JSON 结构化裁决+锚点校准+人工抽检——推理模型当裁判模糊判定更稳**（华为云原文）→ 判据：**裁判结构化输出**；锚点校准+人工抽检兜底。
- **失败变回归**：**每个生产失败变回归测试并 tag incident；回归套件编码每个硬教训**（Kanopy 原文）→ 判据：**失败即用例**；带 incident 标签。
- **数据新鲜**：**Error Feed 每周推进；冻结集=benchmark 非回归套件**（Future AGI 原文）→ 判据：**基准每周滚**；旧集只当 benchmark。
- **提升层**：工作流/可复用 Skill（评测数据治理）。
## 结构化输出五步 recipe 与 JSON 四层次：Pydantic/Zod 定义一次→strict mode 原生参数→同模型验证业务规则→仅失败时验证错误喂回重试 · JSON 四层次（看起来像 JSON→语法合法→符合 Schema→满足业务规则——只靠 prompt 只到第一层）· JSON mode vs Schema mode 分工（JSON mode 管结构合法性仍需运行时验证；Schema mode=constrained decoding grammar 自动生成）（来源：andrew.ooo《2026 Guide: Get Structured JSON Output From LLMs》（**recipe 五步：①Pydantic/Zod 定义形状一次 ②发 JSON Schema+strict mode 给 provider 原生 structured-outputs 参数 ③用同模型验证解析结果业务规则 ④仅 step3 失败时以验证错误作反馈重试**）+ 腾讯云《2026AI面试题-怎么让模型严格输出 JSON？为什么只靠 Prompt 不可靠》（**能否区分"看起来像 JSON"（prompt 引导可到）/"语法合法"/"符合 JSON Schema"/"满足业务规则"四层——只靠 prompt 只到第一层**）+ Max Gherman《Structured Output & Constrained Decoding》（**JSON mode 处理括号匹配/字符串转义/结构合法性但不强制具体 schema，仍需运行时验证键存在；Schema mode 传 JSON Schema 输出保证符合——constrained decoding grammar 从 schema 自动生成**）+ Learn Agent《结构化输出》（**不是在提示词里说清格式，而是生成 Token 过程中直接屏蔽不合规 Token，根源杜绝格式错误**）2026 实拉；与 §约束解码（同轮 ③）分工——那边管"底层机制与库"，本条管"应用层 recipe 与分层"）
结构化输出先分层：prompt 只到第一层，schema 约束到第三层，业务规则要后置验证。
- **五步 recipe**：**Pydantic/Zod 定义一次→strict mode 原生参数→同模型验证业务规则→仅失败时验证错误喂回重试**（andrew.ooo 原文）→ 判据：**schema 单一定义**；重试只在验证失败时。
- **JSON 四层次**：**看起来像 JSON→语法合法→符合 Schema→满足业务规则；只靠 prompt 只到第一层**（腾讯云原文）→ 判据：**分层自查**；到不了哪层补哪层手段。
- **JSON mode≠Schema mode**：**JSON mode 管结构合法性仍需运行时验证；Schema mode 输出保证符合 schema**（Max Gherman 原文）→ 判据：**按需选档**；JSON mode 后必须验证。
- **提升层**：工具/工作流（结构化输出 recipe）。

## Schema 设计四律与严格工具 use：可选参数翻倍 grammar 状态空间→有默认值改必填 · 扁平化嵌套 · 多 strict 工具拆分到请求/subagents · 工具描述=性能最重要因素（做什么/何时用/每参数含义）· additionalProperties:false+tool_choice 锁定强制确定性 · strict:true 工具调用恒符合 input_schema+name 恒有效（grammar 缓存 24h）（来源：Anthropic 官方 platform.claude.com/docs/en/build-with-claude/structured-outputs + strict-tool-use（**每个可选参数大致翻倍 grammar 状态空间——总有合理默认值的参数改必填让 Claude 显式提供默认；深嵌套可选字段复合复杂度→扁平化；多 strict 工具拆到多个请求或 subagents；persistent 合法 schema 问题带 schema 联系支持**；**strict tool use 用同 pipeline 编译工具 input_schema 为 grammar；工具 schema 临时缓存最多 24h**；**additionalProperties:false+tool_choice:{type:tool,name:...} 锁定执行保证 tool_use 块内确定性结构化输出**）+ Anthropic 工具实现最佳实践（**描述是工具性能最重要的因素：做什么/何时用（何时不用）/每参数含义**）2026 实拉；与 §五步 recipe（同轮 ①）分工——那边管"应用流程"，本条管"schema 怎么写才省状态空间"）
schema 先省状态空间：可选改必填、扁平化、拆分；工具描述是性能第一因素。
- **四律**：**可选参数翻倍 grammar 状态空间（有默认值改必填）；深嵌套扁平化；多 strict 工具拆分；工具描述=性能最重要因素**（Anthropic 原文）→ 判据：**schema 越平越省**；描述写全三问。
- **锁定执行**：**additionalProperties:false+tool_choice 锁定——tool_use 块内确定性输出**（ZeroLabs 原文）→ 判据：**锁 tool_choice**；不靠 prompt 碰运气。
- **strict tool use**：**strict:true 工具调用恒符合 input_schema、name 恒有效；grammar 缓存 24h**（Anthropic 原文）→ 判据：**严格模式开**；缓存有效期 24h。
- **提升层**：工具/可复用 Skill（schema 设计）。

## 约束解码 token mask 与本地库选型：编译 schema/CFG/regex 为状态机+违规 token 概率置零（模型仍选合法 token 但物理不可能非法）· XGrammar/Outlines 自托管 serving 层 · vLLM guided_json（Pydantic schema）· Ollama format:json · PydanticAI decorator 工具注册自动生成 JSON schema · 多 provider 可移植（一个 schema+provider 适配器+统一验证层；CI 每 provider 测 dialect 差异）（来源：XGrammar-2（**"fast, customizable structured generation" 引擎针对 agentic LLM workloads；token 级约束解码保证 100% 结构正确性，生成时阻止无效 token**）+ Outlines（**15.9k stars，Python 引导输出到 JSON/regex/grammar，可自托管为 serving 层保证 schema-conformant 生成，支持 Transformers/llama.cpp/vLLM 本地模型**）+ PydanticAI（**decorator 工具注册自动从类型提示生成 JSON schema**）+ vLLM 文档（**Pydantic schema→guided_json；本地 GuidedDecodingParams 或服务端 extra_body；hosted API response_format**）+ Ollama（**format:json 限制 token 采样到合法 JSON**）+ promptmake《Structured Output Prompting》（**fallback router 多 provider：CI 同 schema 每 provider 测；记录 dialect 差异 additionalProperties/enum 处理/重试行为；JSON mode 跨 provider 不 byte-for-byte 可移植；一个 schema 定义+provider 适配器+统一验证层**）2026 实拉；与 §五步 recipe（同轮 ①）分工——那边管"托管 API 流程"，本条管"本地/自托管机制与多 provider"）
约束解码先懂机制：token mask 物理阻断非法输出；本地用 XGrammar/Outlines，多 provider 用适配器。
- **token mask**：**编译 schema/CFG/regex 为状态机，违反结构 token 概率置零——模型仍选合法 token 但物理不可能非法**（WorthPosting 原文）→ 判据：**结构合法是物理保证**；不是提示约束。
- **本地库**：**XGrammar（agentic 引擎）/Outlines（自托管 serving 层）；vLLM guided_json；Ollama format:json**（各库原文）→ 判据：**本地先选约束解码库**；不靠 prompt。
- **多 provider**：**一个 schema+provider 适配器+统一验证层；CI 每 provider 测 dialect 差异（additionalProperties/enum/重试）**（promptmake 原文）→ 判据：**schema 单源**；适配器层隔离差异。
- **提升层**：工具/可复用 Skill（约束解码选型）。
## Spec-Driven feature loop 与验证先于自主性：Plan→Implement→Validate 每步 fresh agent context+独立 Git 分支+spec 与代码同 commit（反 vibe coding）· 验证先于提升自主性三规则（先写失败测试/验收标准映射测试/agent 不能编辑的 oracle——说不出检查保持短链）· 连续两次干净通过才收敛（大变更单次通过不足）（来源：DeepLearning.AI《Spec-Driven Development with Coding Agents》（**反 vibe coding（prompt→hope→fix→repeat），先写 spec——spec 是脑 agent 是手；feature loop：Plan→Implement→Validate 每步 fresh agent context+自己 Git 分支+spec 文件与代码一起 commit**）+ Developer Toolkit《specify, verify, then delegate 三规则》（**先 spec 后生成（每文件具名人员接受后才进下一阶段）；验证先于提升自主性——只有存在"错误行为会变红"的检查（先写失败测试/验收标准映射测试/oracle agent 不能编辑）才让 agent 长时间无人跑；说不出检查就保持短链**）+ Codex 189 文件重构案例（**PostToolUse hooks 作验证门 exit code 2 喂回发现；连续两次干净通过才收敛，单次通过对大跨切变更不足；spec 是主要 artifact——diff 可再生 spec 不可再生**）2026 实拉；与 §AI 生成代码收 diff 五连查（r629 前）分工——那边管"收 diff 前查什么"，本条管"流程怎么编排"）
编码 agent 先立流程：spec 先行、验证先于自主、双 clean 才收。
- **feature loop**：**Plan→Implement→Validate 每步 fresh context+独立分支+spec 与代码同 commit**（DeepLearning.AI 原文）→ 判据：**每步换新上下文**；spec 跟代码一起提交。
- **三规则**：**先 spec 后生成（文件级具名接受）；验证先于自主（先写失败测试/验收映射测试/oracle agent 不能编辑）；说不出检查保持短链**（Developer Toolkit 原文）→ 判据：**检查可命名才放手**；不能命名就短链。
- **双 clean**：**连续两次干净通过才收敛；单次通过对大跨切变更不足**（Codex 原文）→ 判据：**大变更双 pass**；一次绿不算完。
- **提升层**：工具/工作流/可复用 Skill（编码代理流程）。

## spec 是主要 artifact 与 spec 未覆盖即补 spec：diff 可再生 spec 不可再生 · 发现 spec 未覆盖→加 spec 不只修代码（否则同 bug 重演）· 高层验证（符合 spec/破坏已有，不逐变量名）+跑应用点击用户流+自动化测试=done 定义 · spec 三层次（first/anchored/as-source）+spec stub 最小 schema 捕获业务逻辑（来源：Codex 案例（**spec 是主要 artifact——diff 可再生 spec 不可再生**）+ imgabi（**验证关注高层：符合 spec 吗/破坏已有吗，不需查每个变量名；跑应用点击用户流（validation doc）；跑自动化测试=每 feature done 定义；发现 spec 未覆盖→加 spec 不只修代码，否则同样 bug 重演**）+ Augment Code（**spec 三层次：spec-first 写前/spec-anchored 完成后保持维护/spec-as-source spec 主源文件生成代码当 build artifact；spec stub 定义最小 schema 捕获业务逻辑省略实现**）2026 实拉；与 §feature loop（同轮 ①）分工——那边管"流程步骤"，本条管"spec 本身的地位与维护"）
spec 先定性：可再生 diff 换 spec，spec 未覆盖必补，验证对 spec 不对变量名。
- **spec 主位**：**diff 可再生、spec 不可再生——spec 是主要 artifact**（Codex 原文）→ 判据：**保 spec 优先**；diff 丢了可重生成。
- **补 spec**：**发现 spec 未覆盖→加 spec 不只修代码，否则同样 bug 重演**（imgabi 原文）→ 判据：**修码同修 spec**；漏 spec 即埋雷。
- **高层验证**：**符合 spec/破坏已有（不逐变量名）+跑应用点击用户流+自动化测试=done 定义**（imgabi 原文）→ 判据：**对意图验证**；不对代码逐行审计。
- **三层次**：**spec-first（写前）/spec-anchored（保持维护）/spec-as-source（spec 主源+生成码=build artifact）**（Augment 原文）→ 判据：**先定 spec 层次**；不同层次不同维护投入。
- **提升层**：工作流/可复用 Skill（spec 治理）。

## 分离 reasoning/action/validation 与 trust-then-verify gap：validation=每次 action 提交前确定性真实代码检查（不是模型给自己作业打分）· agent 不拿 raw DB 访问给小型审计能力集 · 换模型不用重写 · trust-then-verify gap（看似合理实现不处理边界）→总是给可执行验证（测试/构建/截图）不能验证别 ship · 每次改动后跑测试套件+保持上下文紧 · 包建议用 npm view 验证防幻觉（来源：CruxBit《Agentic Coding in Production 2026 Field Guide》（**架构分离 reasoning/action/validation：action=工具 API 正常函数正常验证，agent 不拿 raw DB 访问给小型审计能力集；validation=每次 action 提交前确定性检查——不是模型给自己作业打分，是真实代码验证输出合理；这样换模型不用重写**）+ Claude Code best practices（**trust-then-verify gap：Claude 产生看似合理实现不处理边界；总是提供验证（测试/脚本/截图），不能验证就别 ship**；**给 Claude 可执行验证=可离开的会话 vs 只能盯着的会话；无验证"看起来完成"是唯一信号**）+ code.live（**每次改动后跑测试套件+保持上下文紧；提供 context pack+包建议用 npm view 验证防幻觉**）2026 实拉；与 §spec feature loop（同轮 ①）分工——那边管"编排流程"，本条管"三层架构与验证哲学"）
编码架构先三分离：reasoning 决策、action 小能力集、validation 确定性代码。
- **三层架构**：**reasoning/action/validation 分离——action 正常函数验证、agent 无 raw DB 给审计能力集、validation 确定性真实代码非模型自评、换模型不用重写**（CruxBit 原文）→ 判据：**验证不是自评**；能力面可审计。
- **TTV gap**：**看似合理实现不处理边界→总是给可执行验证，不能验证别 ship**（Claude Code 原文）→ 判据：**可执行验证在手才放行**；无验证"像完成"不可信。
- **幻觉包**：**包建议用 npm view 验证；每次改动跑测试+上下文紧**（code.live 原文）→ 判据：**包级验证**；防幻觉依赖。
- **提升层**：工具/工作流（编码验证架构）。
## 合成数据生成 pipeline 三闸：pre-generation 数据卫生层（凭证/PII/毒内容）· hostile-evaluator judge（不同模型家族按任务定义评 faithfulness/intent clarity/plausibility/novelty，0.7 阈值，raw 生成典型再拒 40-60%）· append-only per-sample provenance 链（被拒样本带结构化原因）· 六 source format readers+自动 schema 检测+八 LLM 生成任务+三互补质量门（provenance-exact 幻觉验证）+结构化自适应恢复+五种训练导出格式（来源：arXiv 2606.21631《Data Curation and Synthetic Data Generation for LLM Post-Training》（**框架=六 source format readers+自动 schema 检测，pre-generation 数据卫生层处理凭证/PII/毒内容，八 LLM 生成任务，三互补质量门带 provenance-exact 幻觉验证，结构化自适应恢复，五种训练导出格式兼容 TRL/Unsloth/AlignTune；每条 pipeline 决策记录 append-only per-sample provenance 链，被拒样本带结构化原因**）+ Future AGI《How to Generate Synthetic Data With LLMs 2026》（**hostile-evaluator LLM judge：与生成器不同模型家族；judge 按任务定义评分 faithfulness/intent clarity/plausibility/novelty vs seed；低于 0.7 阈值拒绝；raw 生成典型再拒 40-60%**）+ GTO 实践（**LLM 数据需系统 curation 缓解幻觉/不一致/质量变化；样本过滤=启发式检查（规则验证/置信阈值/域信号）+LLM-as-judge 独立 LLM 按显式标准评估**）2026 实拉；与 §合成比例（同轮 ②）分工——那边管"配比与去重"，本条管"生成管线的卫生与闸门"）
合成数据先设闸：生成前卫生、生成后 hostile judge、全程 provenance。
- **三闸**：**pre-generation 卫生层（凭证/PII/毒内容）→hostile judge（不同家族+0.7 阈值+再拒 40-60%）→provenance 链（append-only 每样本决策记录+被拒样本结构化原因）**（arXiv+Future AGI 原文）→ 判据：**闸门独立**；judge 与生成器不同家族。
- **复现框架**：**六 reader+自动 schema 检测+八生成任务+三质量门+自适应恢复+五种导出格式（TRL/Unsloth/AlignTune）**（arXiv 原文）→ 判据：**管线模块化**；导出格式兼容训练栈。
- **judge 标准**：**按任务定义评 faithfulness/intent clarity/plausibility/novelty**（Future AGI 原文）→ 判据：**评分有任务定义**；不是拍脑袋打分。
- **提升层**：工作流/可复用 Skill（合成数据管线）。

## 合成比例与防坍缩：70/30 人-合成比例（≥70% 高质量去重人类网页数据锚定熵防模型坍缩）· 双模型各半生成（防单一模型风格习惯主导数据集，减少分布坍缩保留输出广度）· 双阶段去重（MinHash LSH 结构 n-gram 近重复+embedding-based SemDeDup 语义冗余）· Self-Instruct 扩展（20-50 seed→teacher 生成与 seed 不相似的新例子）+Evol-Instruct 演化更难更具体更受限（来源：shyankdev《Role of Synthetic Data in Training Frontier LLMs》（**70/30 Human-to-Synthetic Ratio：从不纯合成训练预训练模型，≥70% 高质量去重人类网页数据锚定熵防模型坍缩；双阶段去重 MinHash LSH 结构 n-gram 近重复+embedding SemDeDup 语义冗余，剪除候选合成样本**）+ AI/TLDR《Synthetic Training Data for LLM Fine-Tuning》（**一半数据一个模型生成另一半另一个模型生成——防止单一模型风格习惯主导数据集，减少分布坍缩保留输出广度；Self-Instruct：20-50 人写 seed 例子→teacher 生成新的不同例子不与 seed 集相似**）+ ZeroEntropy（**Evol-Instruct：每代演化指令更难更具体更受限，产出更尖锐的难度分布；Magpie：instruct LLM 只给 system prompt 会幻觉出它愿意回答的用户指令**）+ Daily AI World（**Self-Instruct 实操：8 个 seed task→teacher 生成 20 个相似但不同任务；语义 embedding 过滤确保足够不同最大化多样性；100 seed 迭代扩**）2026 实拉；与 §合成数据三闸（同轮 ①）分工——那边管"卫生与闸门"，本条管"配比、多样性与防坍缩"）
合成配比先防坍缩：70% 人类锚定、双模型分半、双阶段去重。
- **70/30**：**≥70% 高质量去重人类数据锚定熵防模型坍缩；从不纯合成训练**（shyankdev 原文）→ 判据：**人类数据打底**；纯合成是死路。
- **双模型**：**两个模型各生成一半——防单一风格主导、减少分布坍缩**（AI/TLDR 原文）→ 判据：**生成器去单一化**；风格不垄断。
- **双去重**：**MinHash LSH（结构近重复）+SemDeDup（语义冗余）双阶段**（shyankdev 原文）→ 判据：**结构和语义各去一遍**；单层漏一半。
- **Self-Instruct**：**20-50 seed→teacher 生成不相似新例；Evol-Instruct 演化更难**（各原文）→ 判据：**seed 少而精**；演化增难度。
- **提升层**：工作流/可复用 Skill（防坍缩配比）。

## 合成数据评测先于大跑与三维独立评分：评测集不用训练相同模板/seeds/模型版本（冻结真实集+独立对抗 case+schema 执行测试+slice 指标+记忆探测+隐私探测+生产失败回归）· fidelity（KS/chi-square/Anderson-Darling+相关联合分布）/utility（合成训练真实测试 AUC 差异）/privacy（membership+attribute inference；DP epsilon 1-10）三维独立通过或失败 · 覆盖度=minority class 保留（不平衡数据生成器少表示 minority——欺诈/异常检测恰是下游要学的）（来源：ITIS（**build evaluation before the large run——评测集不能用训练相同模板/seeds/模型版本生成；包括冻结真实集+独立写的对抗 case+schema 和执行测试+target taxonomy slice 指标+对 seeds 记忆探测+safety/privacy probes+生产失败回归例**）+ JobsByCulture（**三维权衡：fidelity（KS/chi-square/Anderson-Darling）/utility（合成训练 vs 真实训练可比）/privacy（DP epsilon 1-10）**）+ luizneto（**三闸：统计保真+隐私抵抗（membership/attribute inference）+多样性覆盖（edge-case/minority）；只有 4/17 学术调查提供可复现验证工件**）+ BlueGen（**resemblance/utility/privacy 三维独立评分——可独立通过或失败，resemblance 满分仍 fail privacy；DP 在生成过程内建非事后加噪**）+ Arjun Jaggi（**Dimension E: Exact Coverage——覆盖度测合成数据是否保留稀有关键事件；生成器优化平均分布精度会少表示 minority class；欺诈/临床试验/网络异常检测 minority 恰是下游要学的**）2026 实拉；与 §评测信封（r629 前）分工——那边管"agent 评测"，本条管"合成数据质量评测"）
合成评测先立集：评测集独立于训练、三维独立评分、覆盖度盯 minority。
- **评测先立**：**评测集不用训练同模板/seeds/模型版本——冻结真实集+对抗 case+schema 测试+记忆/隐私探测+生产失败回归**（ITIS 原文）→ 判据：**评测与训练隔离**；防自证。
- **三维独立**：**fidelity（KS/chi-square/AD）/utility（合成训练真实测试）/privacy（membership+attribute inference；DP epsilon 1-10）独立通过或失败**（BlueGen+JobsByCulture 原文）→ 判据：**一维高分不掩他维**；逐维验收。
- **覆盖度**：**生成器优化平均分布精度会少表示 minority class；欺诈/异常检测 minority 恰是下游要学的**（Arjun Jaggi 原文）→ 判据：**盯 tail coverage**；平均好不等于够用。
- **提升层**：工具/工作流（合成数据评测）。
## Agent 编排者职责与五纪律：orchestrator 读任务清单→每任务 spawn 隔离 worker（任务作上下文）→收集草稿→review subagent 查一致性/重复覆盖/质量→写盘+摘要回执（来源：OpenClaw Multi-Agent Orchestration Guide（**orchestrator 职责：读 content brief 列表→对每个 brief spawn 隔离 writer subagent（brief 作 task context）→收集完成草稿→spawn review subagent 接收全部草稿查一致性/重复覆盖/质量→写最终输出到磁盘并发摘要给 requester channel**）+ OpenClaw Agent Orchestrator skill（**Best Practices：Start small 从 2-3 agents 开始按模式扩展 / Clear boundaries 每 agent 拥有特定交付物 / Explicit handoffs 用结构化文件做 agent 间通信 / Fail gracefully agent 报失败 orchestrator 处理恢复 / Log everything 状态文件跟踪调试**）+ OpenClaw Playbook（**maxSpawnDepth: 2 解锁 agent 生 agent；specialist workers 狭窄任务令——"You are a security reviewer. Look only at auth flows." 窄令比一个 agent 全干产出更好**）2026 实拉；与 §多 Agent 协作纪律（r629 前）分工——那边管"拆了之后怎么协作/共享层"，本条管"编排者具体的职责清单与五条运营纪律"）
编排先定职责：orchestrator 按清单 spawn 隔离 worker、review 收口、写盘回执；五纪律兜底。
- **编排者职责链**：**读任务清单→每任务 spawn 隔离 worker（任务作上下文）→收集→review subagent 查一致性/重复覆盖/质量→写盘+回执**（OpenClaw 原文）→ 判据：**worker 隔离、review 收口**；不做无审合并。
- **五纪律**：**start small（2-3 agents 起步按模式扩展）/clear boundaries（每 agent 拥有特定交付物）/explicit handoffs（结构化文件通信）/fail gracefully（报失败交恢复）/log everything（状态文件跟踪）**（skill 原文）→ 判据：**边界+交接+留痕**；无声失败最贵。
- **窄令原则**：**specialist workers 狭窄任务令——"只查 auth flows"比一个 agent 全干产出更好**（Playbook 原文）→ 判据：**令窄产出优**；不追求全能 worker。
- **提升层**：工作流/可复用 Skill（编排运营）。

## HITL 是治理要求不是 UX：interrupt_before+checkpointer 每步持久化精确恢复 · "Autonomy without a pause button is a liability, not a feature" · 高风险人工批准（Dify 审批节点低风险自动/高风险人工 / n8n human approves anything that ships）· 低风险直通高风险暂停的 conditional edge 路由（来源：LangGraph HITL 教程（**Classify 判意图→Plan Action 提议写动作+风险分→Respond 执行；conditional edge 低风险直通 Respond 高风险暂停等人工批准；批准后从精确 checkpoint 恢复**）+ Alice Labs（**HITL 不是 UX feature 是企业治理要求；任何写数据库/金融交易/外部通信/不可撤销动作都必须人工批准检查点；interrupt_before 编译时参数**）+ Diego Rodriguez（**rescue 项目最常见错：demo 好好的第一周给错订单退了真钱；Autonomy without a pause button is a liability, not a feature**）+ LangChain blog（**durable execution：模型驱动步骤不确定，checkpointing 每步持久化，失败 run 从已做决策恢复**）+ Dify 审批节点 + n8n（**human approves anything that ships**）2026 实拉；与 §Agent 间接口契约（r629 前）分工——那边管"交接结构"，本条管"暂停/恢复机制与治理定位"）
HITL 先定位：治理要求不是 UX；暂停点+精确恢复是标配。
- **治理定位**：**写库/金融交易/外部通信/不可撤销动作必须人工批准检查点**（Alice Labs 原文）→ 判据：**不可撤销=必审批**；不是可选。
- **暂停-恢复**：**interrupt_before 编译时指定+checkpointer 每步持久化，批准后从精确 checkpoint 恢复**（LangGraph 原文）→ 判据：**暂停可恢复**；不重跑已做决策。
- **风险路由**：**conditional edge 低风险直通/高风险暂停**（教程原文）→ 判据：**按风险分流**；demo 好≠生产好。
- **提升层**：工作流（治理机制）。

## Agent 框架选型判据：CrewAI 角色委派快速上线（role/goal/backstory/Flow 事件驱动）vs AutoGen 显式 sender/receiver 确定性可重放（微软 maintenance mode→社区 fork AG2 接棒）· OpenAI SDK model-native harness+native sandbox（agent 跨文件工具工作+受控 workspace）· Claude SDK 迁移对照（@input_guardrail→UserPromptSubmit hook 循环前纯函数 / @output_guardrail→ResultMessage.result 纯函数）· 按可重放性/决策可见性/维护状态选（来源：CrewAI vs AutoGen 2026 对比（**CrewAI role-based Crew（role/goal/backstory/tools）从 Flow 委派；1.14.0 runtime state checkpointing；AutoGen explicit sender/receiver 对话模型确定性可重放；2026 微软把 AutoGen 放 maintenance mode 社区 fork AG2 接棒**）+ OpenAI Agents SDK 演进（**model-native harness agent 跨文件工具在计算机上工作+native sandbox 执行安全运行+受控 workspace+可设定记忆+沙盒感知编排+类 Codex 文件系统工具**）+ Claude Cookbook 迁移对照（**@function_tool→@tool+create_sdk_mcp_server；@input_guardrail→循环前纯函数或 UserPromptSubmit hook；@output_guardrail→ResultMessage.result 纯函数**）+ Microsoft Learn（**group chat 轮转 vs dynamic 发言**）2026 实拉；与 §多 Agent 协作纪律（r629 前）分工——那边管"模式怎么选"，本条管"具体框架怎么选"）
框架先判据：可重放性/可见性/维护状态三轴；guardrail 是纯函数不是特殊机制。
- **两轴判据**：**CrewAI 角色委派快速上线但决策可见性低；AutoGen 显式对话确定性可重放；维护状态看 fork 活力**（对比原文）→ 判据：**要确定性选显式对话**；要快上线选角色委派。
- **SDK harness**：**model-native harness 让 agent 跨文件工具工作+native sandbox+受控 workspace+可设定记忆**（OpenAI 原文）→ 判据：**沙箱原生**；不是事后套壳。
- **guardrail 本质**：**迁移对照——输入防护=循环前纯函数，输出防护=result 上纯函数；不是 SDK 独有魔法**（Claude 原文）→ 判据：**防护=纯函数/hook**；换框架不丢语义。
- **提升层**：工具/工作流（框架选型）。
## Agent 生产首配告警与成本护栏：error rate 2%/5min · P95 总延迟 5s · TTFT P50 1.5s · hourly cost 预算 · cached token ratio · 成本告警最被忽视（agent loop bug 烧钱）· 工具错误率 5%/15min（工具错误级联不同于模型错误）· 异步批量导出器 span 内存排队定期刷新——遥测后端故障只丢 trace 不阻塞 agent · 执行前强制迭代上限+单工具调用次数限制+阻止重复相同工具请求（来源：DEV《Implementing AI Observability: Tracing LLM Calls End-to-End》（**首配四告警：error rate 2% over 5 minutes / P95 total latency 5s / TTFT P50 1.5s / hourly cost budget threshold / cached token ratio；cost alert 最被忽视——loop bug 在 agent 里会烧钱**）+ Agentbrisk（**工具调用错误率超 5% rolling 15-min 告警——工具错误级联方式不同于模型错误；P95 延迟告警，context bloat 也会让模型变慢**）+ InfoQ（**异步批量导出器：span 内存排队定期刷新，遥测后端临时故障只丢追踪数据不阻塞 agent；执行前强制严格迭代上限+单工具调用次数限制+执行前检查阻止重复相同工具请求**）+ OpenObserve（**四告警：P99 agent.step span 超 10s 5-min 窗口 / gen_ai.usage.output_tokens 每小时超 7 天基线 3x**）2026 实拉；与 §工具结果断言层（r629 前）分工——那边管"调用后可疑结果打标"，本条管"生产级告警阈值与成本护栏"）
Agent 先立护栏：四类告警首配、成本最被忽视、遥测不阻塞主循环。
- **首配告警**：**error 2%/5min、P95 5s、TTFT P50 1.5s、hourly cost、cached token ratio**（DEV 原文）→ 判据：**上线前配齐**；先立基线再调。
- **成本护栏**：**loop bug 烧钱；执行前强制迭代上限+单工具调用次数+阻止重复相同请求**（DEV+InfoQ 原文）→ 判据：**成本告警必配**；循环失控静默烧钱。
- **工具错误**：**工具错误率 5%/15min——工具错误级联不同于模型错误**（Agentbrisk 原文）→ 判据：**工具层单独告警**；级联要早发现。
- **遥测隔离**：**异步批量导出器 span 排队定期刷新——后端故障只丢 trace 不阻塞 agent**（InfoQ 原文）→ 判据：**遥测异步化**；观测不能拖慢被观测对象。
- **提升层**：工作流/工具（生产护栏）。

## Golden trace 回归与执行路径测试：每条关键用户旅程抓真实生产 trace（模型调用/工具调用/最终输出全序列），CI 重放输入+judge 对比新旧输出；30-80 traces 覆盖 happy paths/edge cases/已修 bug——信号大多在这 · 测执行路径不只最终输出——span 层评工具选择/参数正确性+断言任务完成+失败模拟 case（工具报错/返回空）· 多轮 agent 用场景模拟（每跑对新版本生成新对话），重放旧 transcript 测不出新版本怎么引导对话（来源：72Technologies《Agent Evals in CI: Regression Tests That Actually Work》（**golden trace replays：每条关键用户旅程抓真实生产 trace——模型调用/工具调用/最终输出全序列；CI 重放输入 judge 对比新旧输出；30-80 traces 覆盖 happy/edge/已修 bug，信号大多在这**）+ Confident AI《LLM Regression Testing》（**测执行路径不只最终输出：span 层评工具选择和参数正确性，断言任务完成 vs 场景预期结果，含失败模拟 case 工具报错或返回空；多轮 agent 用 scenario-based simulation——每跑对新版本生成新对话，重放旧 transcript 测不出新版本怎么引导**）+ arXiv 2601.22025（**evaluation-driven iteration：golden set 部署前跑发现引用合规下降；"better" prompt 强调 helpfulness 导致证据不足也自信回答；加显式拒答指令重测确认修复无新回归**）2026 实拉；与 §评测信封（r629 前）分工——那边管"agent 能力评测方法"，本条管"生产 trace 重放回归门禁"）
回归先抓金迹：真实生产 trace 重放、测路径不只输出、场景模拟不重放旧稿。
- **golden trace**：**30-80 条真实生产 trace（happy/edge/已修 bug）CI 重放+judge 对比**（72Tech 原文）→ 判据：**信号在真实 trace**；别造理想样例。
- **测路径**：**span 层评工具选择/参数正确性+任务完成断言+失败模拟 case**（Confident 原文）→ 判据：**测执行路径**；最终输出会骗人。
- **场景模拟**：**多轮 agent 每跑生成新对话——重放旧 transcript 测不出新版本引导**（Confident 原文）→ 判据：**对话现生成**；旧稿重放是假回归。
- **提升层**：工作流/可复用 Skill（回归门禁）。

## 工具调用契约测试与模型升级回归：工具调用参数 JSON Schema 校验+版本化 schema（变更显式）· golden tool traces（prompt/tool calls/tool responses/final output）重放 CI 对 mock tool server 确定性测试+软门查系统是否先选对工具 · 模型升级 pin 精确模型 ID+读回 model 字段断言匹配（允许 alias-to-snapshot 解析），fallback/容量绕路产生的分数测的什么都不是且别处不显示 · 基线候选同 case 同 reps 同 scaffold（来源：Kunal Ganglani《AI Engineering Evals: Regression Gates》（**工具调用用 contract testing：工具调用参数 JSON Schema 校验+版本化 schema 变更显式；记录 golden tool traces（prompt/tool calls/tool responses/final output）CI 重放对 mock tool server 确定性测试；软门检查系统是否先选对工具**）+ Seminal《Evaluating LLM applications》（**pin 精确模型 ID+从每个响应读回 model 字段断言匹配，允许 documented alias-to-snapshot 解析；fallback/容量绕路产生分数测的什么都不是且可能别处不显示；跑前查 live model index 当前标识符与上下文限制；基线候选同 case 同 reps 同 scaffold**）2026 实拉；与 §AI 生成代码收 diff 五连查（r629 前）分工——那边管"代码交付验收"，本条管"工具调用与模型升级的回归门禁"）
工具先契约：参数 schema 版本化、golden trace 对 mock 重放、模型 pin 精确 ID。
- **契约测试**：**工具参数 JSON Schema 校验+版本化 schema**（Kunal 原文）→ 判据：**参数契约化**；schema 变更显式。
- **mock 重放**：**golden tool traces 对 mock tool server 确定性重放+软门查选对工具**（Kunal 原文）→ 判据：**确定性测试**；真服务不可重放。
- **模型 pin**：**pin 精确模型 ID+读回 model 字段断言；fallback 绕路分数无效且别处不显示**（Seminal 原文）→ 判据：**pin 到快照**；alias 解析必须文档化。
- **同构对比**：**基线候选同 case 同 reps 同 scaffold**（Seminal 原文）→ 判据：**控制变量**；否则数字不可比。
- **提升层**：工作流/可复用 Skill（契约与回归）。
## Claude 5 代提示新规则与 mid-conversation system 注入：新代模型 system prompt 可删 80%+ 无可测损失（模型进化提示更少）；加上下文/动机（why）帮模型理解目标；明确成功标准+鼓励多源验证 · mid-conversation system messages 在相关点 append {"role":"system"} 而非编辑顶层 system 字段——缓存前缀不变，下个请求仍读缓存（来源：Claude《The new rules of context engineering for Claude 5 generation models》（**Claude Code 的 system prompt 对 Opus 5/Fable 5 删掉 80%+ 无可测损失——新代模型提示规则变了**）+ Anthropic prompting best practices（**提供上下文/动机——解释 why 重要帮 Claude 理解目标；明确成功标准；鼓励多源验证**）+ platform docs（**mid-conversation system messages：在相关点 append {"role":"system"} 消息而非编辑顶层 system 字段；缓存前缀不变，下个请求仍读缓存，新指令在相关点生效**）2026 实拉；与 §压缩后规则重声明（r629 前）分工——那边管"压缩后规则复活"，本条管"运行时注入与提示随模型代际演进"）
提示先随代际：模型越强提示越少、why 动机注入、mid-conversation 追加不编辑。
- **代际规则**：**新代模型 system prompt 删 80%+ 无可测损失**（Claude 原文）→ 判据：**模型进化提示减量**；别抱着旧 prompt 不放。
- **why 注入**：**提供上下文/动机——解释 why 帮理解目标；明确成功标准+多源验证**（Anthropic 原文）→ 判据：**给动机不给步骤**；模型会泛化。
- **mid-conversation**：**在相关点 append system 消息而非编辑顶层字段——缓存前缀不变仍读缓存**（platform 原文）→ 判据：**追加不编辑**；保缓存命中。
- **提升层**：模型/工作流（提示演进）。

## 指令文件分工与 monorepo 层级：CLAUDE.md（rules）/skills/hooks/subagents 分工——subagents .claude/agents/ YAML frontmatter（name/description/可选 model/tool access）+body=system prompt，body 大上下文不 session start 加载（只有 name/description/tool list 加载）· AGENTS.md monorepo 层级 root 共享约定+子目录 package-specific override，nearest file 解析 · list exact commands（agent 自动执行 build/test 命令）· @AGENTS.md import 或 /init pass（dual read 未 shipped）· subagent name≤256 字符不能含 :（plugin-scope 保留）（来源：Claude《Steering Claude Code》（**CLAUDE.md/skills/hooks/subagents 四类分工；subagents YAML frontmatter name/description+可选 model/tool access，body 成 system prompt；subagent 类似 skills 但 body 大上下文不在 session start 加载**）+ Codex KB（**AGENTS.md 跨工具可移植；list exact commands agent 自动执行；monorepo 层级 root 共享+子目录 override；nearest file 解析**）+ Morph（**AGENTS.md spec 推荐 sections；dual read 请求 open 未 shipped 2026-08，用 @AGENTS.md import 或 /init pass**）+ Claude Code docs（**subagent name 256 字符；hooks 收 agent_type；名字不能含 : 保留 plugin-scope**）2026 实拉；与 §项目级指令文件（r629 前）分工——那边管"指令怎么写"，本条管"四类机制分工与文件层级规范"）
指令先分机制：rules/skills/hooks/subagents 各司其职、层级覆盖、精确命令。
- **四类分工**：**CLAUDE.md 规则/skills 技能/hooks 必然执行/subagents 隔离助手**（Claude 原文）→ 判据：**按机制归位**；规则别塞进技能。
- **subagent 结构**：**frontmatter name/description/model/tool access+body=system prompt；body 大上下文不 session start 加载**（Claude 原文）→ 判据：**启动只加载轻元数据**；重 body 按需。
- **monorepo 层级**：**root 共享约定+子目录 override；nearest file 解析；list exact commands**（Codex KB 原文）→ 判据：**就近覆盖**；命令精确列出。
- **引用方式**：**@AGENTS.md import 或 /init pass（dual read 未 shipped）**（Morph 原文）→ 判据：**显式导入**；别等自动双读。
- **提升层**：工具/可复用 Skill（指令文件治理）。

## Prompt 版本管理：versions 不可变历史（每次保存新版本）+labels 指针（production/staging），代码引用 label 不引用版本——"生产跑哪个版本是数据问题不是代码问题" · promote 移 label 原子操作+客户端缓存 60-300s 生效 · metrics/eval scores 按 prompt 版本分段，score 掉=回滚信号 · pinned commit 固定应用直到改引用，tag 让 promote/reverse 只改引用（来源：Langfuse Prompt CI/CD（**Stage1 version every change：不可变版本+label 部署；代码引用 label 如 production——生产跑哪个版本是数据问题不是代码问题；评审 1-2 人 optional；promote 移 label 原子，客户端缓存 60-300s 后新版本生效；observe：metrics/eval scores 按版本分段，score 掉=回滚信号**）+ LangSmith prompt tags（**每次保存 prompt 变更=commit；reference commit 或 assign tag；pinned commit 固定应用；tag 促进回滚只改引用**）+ Langfuse 数据模型（**versions 不可变历史 1,2,3...；labels 指向特定版本；代码指 labels**）2026 实拉；与 §工具结果断言层（r629 前）分工——那边管"调用结果"，本条管"prompt 本身怎么版本化发布"）
Prompt 先版本化：不可变历史+标签指针、发布是数据问题、按版本分段观测。
- **版本/标签**：**versions 不可变+labels 指针（production/staging）；代码引用 label**（Langfuse 原文）→ 判据：**代码永远指标签**；版本号只在平台。
- **发布原子**：**promote 移 label 原子+客户端缓存 60-300s 生效**（Langfuse 原文）→ 判据：**发布=移标签**；不是改代码。
- **版本观测**：**metrics/eval scores 按 prompt 版本分段，score 掉=回滚信号**（Langfuse 原文）→ 判据：**按版本分账**；评分掉先查版本。
- **回滚**：**pinned commit 固定/tag 只改引用**（LangSmith 原文）→ 判据：**回滚=移标签**；秒级可逆。
- **提升层**：工具/工作流/可复用 Skill（Prompt 发布工程）。

## 技能库检索即 RAG：230k+ Skills 时代"选择是瓶颈"——两阶段 IR 经 MCP 暴露，成本降 46% 超 LLM 循环（来源：arXiv 2609.38822《SkillSeek》+ AICoder 2026-10-02 实拉，r633A 落地，与 §工具结果断言层分工——那边管"调用结果可疑"，本条管"技能多到选不出来怎么办"）
技能聚合超过 230,000 个后，选择而非创作成为瓶颈；文献主流答案是把选择外包给 agent 自己（LLM 循环改写查询/细化候选，每个任务都付 LLM token）。
- **两阶段 IR 替代 LLM 循环**：**BGE-base bi-encoder（粗筛）→ small cross-encoder（精排）两级检索，经 MCP 暴露给 agent**（SkillSeek 原文）→ 判据：**技能检索是检索问题不是推理问题**——"LLM 循环挑技能"=每个任务都付推理 token；"两阶段 IR"=固定成本+确定性。
- **量化收益**：**89 项 SkillsBench 任务在 OpenHands 上匹配或超过 LLM 循环，成本省 46%**（原文）→ 判据：**检索省的是推理预算**——匹配质量不降、成本近半；与 §混合检索分工：那条管"知识文档召回"，本条管"技能定义召回"。
- **提升层**：工具/工作流/可复用 Skill（技能检索）。

## Claude Skills 访问机制三细节：触发才读、脚本只收输出、repo 挂载自动注入（来源：platform.claude.com Agent Skills docs + Managed Agents Cookbook 2026-07 实拉，r633A 落地，与 §技能库检索分工——那边管"怎么选技能"，本条管"选中后怎么进上下文"）
- **触发时才读，不是常驻**：**skill 触发时 Claude 用 bash 读 SKILL.md 进上下文窗口；SKILL.md 引用的其他文件（FORMS.md/数据库 schema）再通过额外 bash 命令读**（原文）→ 判据：**按需加载**；常驻注入 200+ skills 会把窗口撑爆。
- **脚本代码不进上下文**：**可执行脚本经 bash 运行，Claude 只接收输出——脚本代码本身永不进上下文**（原文）→ 判据：**执行与阅读分离**；长脚本当工具跑，不当文本读。
- **repo 挂载自动注入三元素**：**session 挂载 GitHub repo 时 harness 扫描根 .claude/skills/，把每个 skill 的 name+description+沙箱内 path 注入 system prompt，模型按需读**（Cookbook）→ 判据：**注入口令不注正文**——三元素是索引，正文按需取；把每个 skill 都传 Skills API 并 pin 版本=重复劳动且 repo 一改就漂移。
- **提升层**：工具/可复用 Skill（技能加载机制）。

## GraphRAG Zero 无 cluster summarization 模式 + RAGFlow 版面分析先切分：图只引导候选选择，文档先懂版式再分块（来源：GitHub Next Repo Mind Light 2026-04 + agentindex RAGFlow 92k★ 2026-10 实拉，r633A 落地，与 §LightRAG 轻量方案分工——那边管"增量建图轻量图 RAG"，本条管"第三代图 RAG 怎么免预计算摘要、复杂文档怎么先理解版面"）
- **GraphRAG Zero：检索锚定 embeddings+chunk，图结构只指导候选选择，不做 cluster summarization**（Repo Mind Light 原文：retrieval stays grounded in embeddings and chunk retrieval, with graph structure guiding candidate selection rather than relying on precomputed cluster summaries）→ 判据：**免预计算摘要**——cluster summaries 是 GraphRAG 最大成本源；"零摘要模式"=图当路标不当答案。
- **RAGFlow：切分前先版面分析**（深度文档理解：layout 分析识别表格/图/多栏后再切分，杂乱文档变可靠上下文）→ 判据：**懂版式再切块**——"PDF 直接按字符切"=表格跨块、栏序错乱；"先版面分析"=结构感知分块。
- **提升层**：工作流/工具（图 RAG 第三代 + 复杂文档管线）。

## Qwen-MM-Plugins 多模态能力包架构：能力=skill+可选 MCP server；core 工具面含 OCR/grounding/分割/ASR，native mode 免模型 API 调用（来源：qwenlm.github.io Qwen MM Plugins Hub（plugins/core + api + search cookbook，2026-09~10 实拉）+ arXiv 2609.25611 + WPS 社区 2026-08，r633B 落地，与 §多模态 rerank 分工——那边管"图文结果怎么排"，本条管"怎么给任意 harness 加多模态能力"）
- **能力包两件套**：**每个能力 = 一个 skill 定义 + 一个可选 MCP server；qwen-mm-plugins-core 的 MCP server 暴露媒体读取（图/视频）、文件可视化、OCR、grounding、segmentation、ASR、视觉聊天为工具**（原文）→ 判据：**技能与工具解耦可组合**——"只给 skill"=无工具通道；"skill+MCP"=指令与执行都有；装包即让任意 agent harness 多模态原生。
- **native mode 免 API 调用**：**默认原生模式工具返回文本+图片供 agent 检查，无需模型 API 调用；Core 本地文件检查可读可视化本地文件、查媒体元数据、裁剪标注图片、保存文档页/视频帧**（原文）→ 判据：**本地检查零 API 成本**——"每次看图都调模型"=token 烧光；"native 返回图+文"=agent 自己看得懂；API 模式留给需语义理解的场景。
- **扩展插件形态**：**16 插件含 qwen-mm-plugins-video-memory（长视频 QA 的分层图记忆，4 级树 Root→Super→…）与 Video-Spatio（无模型 3D 空间推理：build_scene/triangulate/visualize_bev/camera_motion/orient_facing 几何/VLM 工具，由宿主模型驱动）**（Hub 原文）→ 判据：**能力包不止读图**——视频时序记忆、3D 空间推理、物理硬件操作（Model Hardware Standard 读传感器/摄像头）都是插件形态；按任务选包不是全装。
- **提升层**：工具/可复用 Skill（多模态能力包）。

## Omni Skill Creator：从任务演示蒸馏 SOP 成可复用技能——单一演示→可分享能力（来源：arXiv 2609.25611《Qwen3.8-Omni》2026-09 实拉，r633B 落地，与 §技能库检索分工——那边管"多技能怎么选"，本条管"技能从哪来、怎么从演示生成"）
- **演示→技能流水线**：**从任务演示提取标准操作程序（SOPs），蒸馏工具使用、决策标准与关键洞察；生成的技能经验证和评估**（原文：extracts standard operating procedures from task demonstrations and distills tool usage, decision criteria, and key insights；skills undergo verification and evaluation）→ 判据：**技能由证据生成不由人写**——"手写技能"=贵且过时；"从演示蒸馏"=一次演示产出可复用资产。
- **单一演示即资本**：**单一演示捕获的知识可转化为可复用、可分享、可自动化执行的能力**（原文）→ 判据：**演示是种子**——一段高质量演示的复利是技能库；与 §重复工作流固化四块结构分工：那边管"手动跑几遍再编码"，本条管"演示自动蒸馏成技能"。
- **提升层**：工作流/可复用 Skill（技能生成）。

## 多模态执行验证两机制：UI 渲染正确性先行验证 + 视觉反馈闭环（观察→行动→验证→修正）+ 纯文本模型外挂视觉（来源：Activepieces Step 5 Preview 2026-10 + 蚂蚁百灵 Ling-3.0-flash-VL 2026-09 + modlens（liustack）2026-10 实拉，r633B 落地，与 §工具结果断言层分工——那边管"返回值合理性断言"，本条管"视觉状态怎么当执行闸门"）
- **UI 状态作执行闸门**：**Step 5 原生多模态引擎处理静态帧+时间流数据，能解释软件界面视觉状态变化——验证 UI 元素已正确渲染再继续自动化测试的下一步**（原文）→ 判据：**先看渲染再走下一步**——"盲走脚本"=元素没出来就点=测试假失败；"视觉验证闸门"=渲染正确才推进。
- **视觉反馈闭环**：**蚂蚁视觉反馈闭环把任务推进为"观察→行动→验证→修正"持续循环（非一次性看图生成），用于医疗报告解读/前端代码生成/GUI 自动化场景基于视觉反馈持续修正执行结果**（原文）→ 判据：**看图要闭环**——"看一次就生成"=错版没修正；"观察→行动→验证→修正"=执行质量随轮提升。
- **纯文本模型外挂视觉**：**modlens（第一个 DeepSeek Harness 视觉插件、text-only coding agent 的 vision bridge）粘贴图片即得结构化 JSON 证据（OCR、版面、语义）**（gstars 原文）→ 判据：**不换模型补视觉**——"纯文本模型"=看不了图；"外挂视觉插件"=图变结构化 JSON 证据进上下文。
- **提升层**：工具/工作流（视觉执行验证）。

## 推理引擎选型：prefix-heavy 负载与优化杠杆顺序（来源：SGLang 官方 sglang.io + PyPI 0.5.20 + ChatForest 2026-05 + Runpod Playbook 2026-10 实拉，r633C 落地，与 §成本四层分工——那边管"成本构成怎么想"，本条管"引擎怎么选、优化先动哪根杠杆"）
- **prefix-heavy 负载选 SGLang 类引擎**：**RadixAttention 前缀缓存对 RAG 管线/多轮聊天/共享 system prompt 的 agent 框架这类 prefix-heavy 工作负载，有时比其他开源引擎快 6 倍；统一 radix tree 缓存分支点后 DeepSeek-V4-Flash token 命中率从 43.8% 升到 60.8%；xAI 用 SGLang 服务 Grok 3、微软 Azure 用 SGLang 服务 DeepSeek R1**（原文）→ 判据：**负载形态决定引擎**——"多轮/共享前缀"=缓存命中率是主指标；"一次性长输入"=缓存红利少，比的是 prefill 吞吐。
- **优化杠杆有顺序**：**FP16→AWQ 在 4090 上每百万 token 成本降 70%；调 --max-num-seqs 与 --gpu-memory-utilization 到饱和再恢复 20-30% 吞吐；3-GPU 配置加投机解码**（Runpod）→ 判据：**先量化再调批再投机**——"一上来就加卡"=最贵的杠杆；"先动量化+批参数"=零硬件成本先榨。
- **结构化输出是引擎层特性**：**SGLang 通过三语法后端（xgrammar 默认/outlines/llguidance）支持四约束格式（JSON Schema/Regex/EBNF），OpenAI 兼容与原生 API 均接受约束参数**（Hivebook）→ 判据：**输出校验下沉到引擎**——"靠提示词保证 JSON"=不稳定；"引擎层约束生成"=语法级保证；与 §输出校验四台阶分工：那边管"生成后怎么查"，本条管"生成时就锁死格式"。
- **提升层**：工具/工作流（推理引擎选型）。

## MoE 激活参数选型与端侧模型矩阵：选型三轴=激活参数/上下文/量化可用性（来源：Codex Qwen3.6-35B-A3B 2026-04 + 蚂蚁 Ling-3.0-tiny 2026-08 + 中国电信 Xing4.0 2026-09 + Recursive Flint 2026-10 + Cohere North Mini + SmolLM2 2026-10 实拉，r633C 落地，与 §量化部署决策框架分工——那边管"位宽怎么选"，本条管"模型本身怎么选（总参/激活参/上下文）"）
- **激活参数比总参数更决定成本**：**Qwen3.6-35B-A3B（35B 总/3B 激活）SWE-bench Verified 73.4 接近 frontier API 模型且消费硬件可跑——本地模型论证从"简单任务够用"变成"frontier 级"；Flint 40B/2.5B、Cohere North Mini 30B/3B 同模式**（原文）→ 判据：**按激活参数估成本**——"看总参数挑模型"=低估 MoE 效率；"看激活参数"=每 token 计算成本直接可比。
- **端侧专用形态**：**Ling-3.0-tiny（7.9B 总/1.3B 激活，KDA-MLA 混合线性注意力 3:1，INT4 达 115 tok/s，目标 Apple Silicon MacBook/DGX Spark）；SmolLM2 4-bit 量化 1.8GB 设备内存 75 tok/s（Apple Silicon/Snapdragon），GSM8K 与多轮 JSON 工具调用超 prior sub-3B**（原文）→ 判据：**端侧看 tok/s 与内存预算**——"能跑≠好用"=要看 75-115 tok/s 是否够交互；"1.8GB 设备内存"=手机/笔记本可行性。
- **国产栈与长上下文**：**星辰 Xing4.0-29B-A4B（29B/4B 激活，256K 原生上下文可扩 512K，Apache-2.0，国产算力+国产框架训练）**（原文）→ 判据：**上下文与激活分账**——"长上下文任务"=256K 档位；"代码/推理任务"=激活参数与 SWE 分数优先；国产栈=部署环境约束。
- **提升层**：模型/工具（端侧选型）。

## vLLM Humming 量化内核与推理工具链分工：统一内核架构、输出兼容矩阵（来源：vLLM Blog Humming 2026-10 + Qwen3.8-2.4T-A95B Day-0 2026-08 + NVIDIA Model Optimizer 2026-09 实拉，r633C 落地，与 §推理引擎选型分工——那边管"引擎与杠杆顺序"，本条管"量化内核与工具链谁产出谁消费"）
- **Humming 统一量化内核**：**vLLM Humming（蚂蚁+vLLM 社区 2026-10 开源）统一架构支持稠密与 MoE 的多种权重+激活格式组合（整数/浮点多位宽+多种缩放方案），显著超越 vLLM Marlin/FlashInfer/DeepGEMM**（原文）→ 判据：**量化内核是共享基建**——"每格式一套内核"=重复建设；"统一架构"=量化格式互操作；新量化格式出来先查 Humming 支不支持。
- **FP4 生产实践**：**Qwen3.8-2.4T-A95B Day-0：FP8/BF16 checkpoints+NVFP4/MXFP4 量化权重；对含路由专家在内的选定层用 RTN 量化+激活校准到 FP4，验证量化精度保持完整；注意"增加推理预算才能复现评估结果"**（原文）→ 判据：**FP4 需校准与复验**——"直接 RTN 不校准"=激活离群毁精度；"激活校准+推理预算复验"=质量与成本双保。
- **工具链分工**：**NVIDIA Model Optimizer 输出跑 vLLM/SGLang/TensorRT-LLM，不跑 llama.cpp/Ollama；速度收益锁 RTX 40/50 系 tensor core——多数家庭用户应消费其 checkpoint 而非自己跑优化**（原文）→ 判据：**产出方与消费方分清**——"自己跑优化器"=费 GPU 时间；"消费别人产出的 checkpoint"=即取即用；引擎兼容矩阵决定 checkpoint 能不能用。
- **提升层**：工具（量化内核与工具链）。

## Agent 模型路由形态学：任务分类路由/分层路由/政策路由（来源：n8n Model Selector + OpenRouter Routing Agent 模板 + OpenClaw ClawRouter docs + NeMo Switchyard 2026 实拉，r634A 落地，与 §模型路由与混合部署分工——那边管"请求派给谁、本地还是云"，本条管"路由怎么分类、政策怎么约束"）
- **任务分类路由**：**n8n Model Selector 按输入类型分类路由——Opus 4 处理 coding、Gemini Thinking Pro 处理 reasoning、GPT 4.1 mini 处理其余；OpenRouter 动态路由让 Routing Agent 分析查询内容与目的选最佳模型；本地 Ollama 动态 router 按任务性质选模型（文本 qwq/llama3.2/phi4、代码 qwen2.5-coder、视觉模型分车道）**（n8n 模板）→ 判据：**先分类后路由**——"单一模型硬扛全部任务"=要么贵要么弱；"分类键（任务类型/内容性质/模态）→模型"=每类任务用最匹配模型。
- **分层路由**：**Reason with Opus——多步规划、歧义根因分析、硬重构、合成冲突源这类"错答代价高且路径不明显"的任务才用旗舰，占少数调用；简单任务走廉价模型（Opus Plans, Haiku Executes：全 opus 时连扫描目录都烧 $5/$25 per million 是 agent 成本危机）**（DEV + exploreagentic）→ 判据：**成本栈要分层**——"旗舰做规划+廉价执行"=成本按任务难度分配；"一律旗舰"=简单任务多付 10-50 倍。
- **政策路由**：**ClawRouter 一个 policy-scoped key 覆盖多个上游模型 provider——bundled 插件只发现该 key 允许的模型、按声明协议路由、报告 key 预算与聚合用量；上游凭据与 provider 转发留在 ClawRouter，用户不用逐个安装认证上游；NeMo Switchyard 把每个 LLM 调用路由到"能干活的最便宜模型"且不改 agent**（OpenClaw + NVIDIA）→ 判据：**路由策略是授权的一部分**——"key 只发现允许的模型"=政策即路由面；"per-call 最便宜能干活"=成本优化自动化；与 §最小权限 分工：那边管"agent 能碰什么"，本条管"agent 用哪个模型碰"。
- **提升层**：工具/工作流（模型路由形态）。

## 工具调用工程细节：并行结果打包、tool_use_id 路由、空结果触发 fallback（来源：Anthropic Tool Calling 决策树 + n8n fallback 模板 + claudearchitectcertification 2026-10 实拉，r634A 落地，与 §工具循环终止条件分工——那边管"循环何时停"，本条管"结果怎么回、路由靠什么"）
- **并行 tool_result 打包**：**并行工具调用时把所有 tool_result 块打包进单一 user message——拆分成多条消息导致 400 错误；数组内顺序无关，tool_use_id 负责路由**（Anthropic）→ 判据：**结果块聚合成一条**——"每结果一条消息"=400/乱序；"单一 user message 内含全部结果"=tool_use_id 精确对应。
- **fallback 看内容不看状态码**：**Claude primary + OpenAI fallback 模板检查 answer 字段本身——空 HTTP 200 也触发 fallback（"It checks the answer field itself, so an empty HTTP 200 also triggers the fallback"）**（n8n）→ 判据：**fallback 判据=内容非空性**——"只看状态码"=空 200 被当成功；"检查 answer 字段"=空结果正确转 fallback；与 §工具结果断言层分工：那边管"结果合理否"，本条管"结果有无 → 要不要换模型重试"。
- **工具边界语义**：**Commerce agents：agent 的工具应调用系统而非重新实现，工具边界=系统逻辑结束+模型判断接管；search_products 返回的结果应已排序（工具侧排好），agent 的职责是决定展示哪些、多少、怎么呈现；tool results are context——返回模型推理需要的字段**（Anthropic）→ 判据：**工具做确定性、模型做判断**——"工具里塞判断逻辑"=模型失去决策权；"结果字段只留推理所需"=上下文最小化。
- **提升层**：工具/工作流（工具调用细节）。

## Guard 化工具与策略护栏：自然语言规则变 Guarded Tools、策略即工具面（来源：Langflow Policies 官方博客 2026-05-20 + Anthropic commerce agents 指南 + Dify Agent Strategies 实拉，r634A 落地，与 §工具面安全分工——那边管"恶意注入怎么防"，本条管"正常业务规则怎么变成工具护栏"）
- **Policies 转 Guarded Tools**：**Langflow Policies 把自然语言业务规则（限额/限制/程序）变成 Guarded Tools——agent 每次触碰工具时必须遵循这些约束；"good intentions are not enough"——agent 可能需要遵守限制、禁令或流程，光靠提示词意图不够**（Langflow）→ 判据：**业务规则固化成工具层护栏**——"规则写提示词里"=可被忽略/遗忘；"规则变 guarded tool"=每次调用强制执行；与 §角色与边界分工：那边管"agent 是什么"，本条管"agent 碰工具时被什么约束"。
- **Agent 策略插件化**：**Dify Agent Strategies 插件（Function Calling/ReAct 等推理策略可插拔），Agent 节点可选模型/工具/任务指令/最大迭代次数+记忆**（Dify marketplace）→ 判据：**推理策略可插拔**——"策略写死"=换场景重写；"策略插件化"=按任务类型换推理形态（FC 精准/ReAct 复杂推理）。
- **提升层**：可复用 Skill/工作流（工具护栏）。

## 结构化输出工程：grammar-constrained sampling、strict tool use、JSON Schema 校验前置（来源：Anthropic Strict Tool Use 官方 docs + Dify Workflow 结构化输出 + 阿里百炼 JSON Object 模式 + Zod/Pydantic 教程 2026 实拉，r634B 落地，与 §工具结果断言层分工——那边管"调用后返回值合理性"，本条管"生成侧输出怎么约束成合法结构"）
- **语法约束采样**：**Anthropic strict tool use：工具定义设 strict:true 用 grammar-constrained sampling 约束模型 token 采样到 schema 合法输出——保证 tool inputs 匹配 JSON Schema；structured outputs 同理（strict:true 顶层属性）**（Anthropic）→ 判据：**约束在采样层而不在提示层**——"提示词要求 JSON"=模型仍可能出格式错；"采样约束到合法 token"=按构造保证合法；与 §outlines 受约束解码分工：都是约束生成，那条在开源栈，本条在 API 层。
- **JSON Schema 校验前置**：**百炼 JSON Object 模式：输出传给下游业务前用 jsonschema/Ajv/Everit 校验，避免字段缺失/类型错/格式不规范导致下游解析失败；失败用重试/大模型改写修复；Dify Workflow 结构化输出：LLM 生成也须符合预设格式，下游无需额外清洗；schema 需 additionalProperties:false**（阿里 + Dify + DataLLM）→ 判据：**校验是交付闸门**——"输出直接进下游"=解析失败才暴露；"schema 校验前置+修复策略"=失败在边界处理；schema 复杂度超限拆小（"Schema is too complex"→减少 strict:true 工具数）。
- **stop_reason 守卫**：**生产路径要 stop_reason guards 带 typed result union——refusal（已计费、拒绝文本优先于 schema）/max_tokens（可能截断 JSON 中间字段）都要当异常路径处理；tool_use schemas 用 nullable 字段+enum 约束合法值**（Zod 教程 + Wasil）→ 判据：**schema 只约束形状不约束中断**——"只查解析成功"=refusal/max_tokens 被当正常输出；"stop_reason 分支处理"=三类终止各自归位。
- **提升层**：工具/工作流（结构化输出工程）。

## 生成后验证三层：NLI 蕴含检查、引用核对、原子事实提取（来源：阿里开发者社区 LLM 幻觉架构级修复 + regolo.ai 原子事实 + ai-agentsplus context 校验 + aitooly Agentic QA + openclaw-output-vetter-mcp 2026 实拉，r634B 落地，与 §RAG 防幻觉与评估分工——那边管"RAG 管线专用指标"，本条管"任意生成的通用验证手段"）
- **NLI 蕴含检查**：**生成后验证——用一个 NLI（Natural Language Inference）模型判断生成答案是否能被源文档蕴含（entailed）：答案里有源文件支撑不了的说法这一步就挂；引用验证核对被引文档是否真含所声称信息——捏造引用是幻觉最常见的一种**（阿里）→ 判据：**验证独立于生成**——"生成模型自己审自己"=同源错误放大；"独立 NLI 模型判蕴含"=第二双眼睛；引用必须回到源文档核对。
- **原子事实提取**：**别"trust but verify"整段读——让 agent 提取原子可检查事实（names/dates/laws/numbers/percentages，LLM 最易幻觉处）；第一 agent 只做"把答案变 claim 列表"；context 校验 prompt："Does the proposed answer contain any information NOT supported by the context? Respond YES or NO"**（regolo + ai-agentsplus）→ 判据：**校验对象是 claim 不是段落**——"整段判断"=笼统无法定位；"原子 claim 逐个核对"=精确到句；事实型字段先提取再验证。
- **Agentic QA 审计-重写循环**：**Agent A(Drafting) 基于 RAG 生成 → Agent B(Audit) 拿内容+Truth Source 找出每个不被源支持的 claim → Agent A(Refining) 基于审计重写——模拟人类编辑流程；openclaw-output-vetter-mcp 单转写 inline grounding-check：响应陈述事实不在输入上下文、代码静默吞异常代用 mock 数据、多轮转写矛盾/未验证完成声称**（aitooly + PyPI）→ 判据：**审计者与重写者分离**——"同一个 agent 自检自改"=盲区延续；"审计-重写双 agent"=编辑闭环；验证者还能查代码层问题（吞异常+mock 数据）。
- **提升层**：工作流/可复用 Skill（生成后验证）。

## 先校验后行动：验证节点前置、结构/业务校验分层、失败重试回路（来源：n8n Production AI Playbook 2026-04-02 + n8n 模板 4316 + Activepieces Reliable Harness 2026-10-14 + Nodbot 2026 实拉，r634B 落地，与 §Guard 化工具分工——那边管"规则变工具护栏"，本条管"AI 输出进外部系统前怎么设闸"）
- **先校验后行动**：**Always validate AI outputs before acting on them. Never pass raw AI output directly to a node that modifies external systems. Always add a validation step in between——五分钟的校验节点省下数小时下游神秘故障排查**（n8n 原文）→ 判据：**AI 输出不能直通外部系统**——"raw AI 输出直接改外部系统"=故障在别人家爆；"中间加校验节点"=失败在自家边界；凡动作型节点（写库/发消息/改配置）前必加。
- **结构/业务校验分层**：**Structured Output Parser 管结构（valid JSON、正确字段名、enum 值），Code node 专注业务校验（confidence/evidence/forbidden actions）；可疑全部送 human review；非 LLM 层（Pydantic model）做最终校验强制 agent 可能忽略的业务逻辑（类型提示保证字符串不冒充整数）**（n8n + Nodbot + Activepieces）→ 判据：**两层校验分开做**——"结构校验里混业务规则"=改规则要动解析器；"结构层+业务层分离"=各管一摊；最终闸门是非 LLM 的确定性校验。
- **失败重试回路**：**自定义 schema 检查后接 Switch：输出不匹配 schema → 路由回 AI Agent 带修正 prompt 重试（上限 4 次防无限循环）；匹配才进 Set 节点；百炼失败用重试/大模型改写修复**（n8n 模板 + 阿里）→ 判据：**校验失败要有修复回路**——"校验失败直接丢弃"=一次失误丢整个结果；"带回修正 prompt 重试+次数上限"=自愈且有限；重试 prompt 要说明错在哪。
- **提升层**：工作流/可复用 Skill（先校验后行动）。

## MCP 工具面工程：渐进发现三层、工具合并、薄服务器前置（来源：Model Context Protocol Client Best Practices + Anthropic Managed Agents Tools + thebiglearn MCP 生产指南 + AWS MCP strategies 2026 实拉，r634C 落地，与 §工具数量阈值 15-20 分工——那边管"一 agent 多少工具"，本条管"工具面怎么设计、怎么被模型发现"）
- **渐进发现三层**：**MCP 官方 client best practices：progressive discovery 三层——Layer 1 Catalog：host 暴露小集 meta-tools 供搜索（search_tools 接受自然语言 query 返回匹配工具名+简述）**（MCP 官方）→ 判据：**工具面分层暴露**——"全量工具常驻上下文"=窗口爆炸+选择变差；"catalog meta-tool 按需搜索"=只载入选中的；工具越多越要渐进发现。
- **工具合并与过滤**：**Anthropic Managed Agents：consolidate related operations into fewer tools——create_pr/review_pr/merge_pr 归并成单工具带 action 字段；AWS：tool filtering/semantic search——动态给 LLM 缩小后的工具集（工具名精确/模式匹配、描述语义匹配、域/类别标签），提高选对工具准确性+减少上下文占用**（Anthropic + AWS）→ 判据：**工具粒度按操作族设计**——"每个操作一个工具"=工具数爆炸；"action 字段合并同族"=语义聚类；语义搜索对"用户意图 vs 工具描述"匹配特别有效。
- **薄服务器前置**：**thebiglearn：薄 MCP server 前置到已批准 API 操作——模型友好工具→确定性 API 调用、缩窄 schema、保留 CRM 授权模型、为上下文塑形结果；业务逻辑在领域服务而非协议装饰器里（防 lock-in）**（thebiglearn）→ 判据：**协议层薄、业务层厚**——"业务逻辑塞进 MCP 装饰器"=换接口就废；"薄协议层翻译成确定性 API"=授权模型不变、换协议不影响业务。
- **提升层**：工具/工作流（MCP 工具面工程）。

## MCP 服务器工程规范：结构化日志、超时与输出限制、优雅关闭、错误分类（来源：LobeHub MCP Engineering skill + OpenClaw CLI mcp + Claude Managed Agents self-hosted sandboxes 2026 实拉，r634C 落地，与 §轻量自动化三模式分工——那边管"自动化形态"，本条管"MCP 服务器本身怎么按生产标准写"）
- **生产八件套**：**MCP Engineering：结构化日志（request ID/tool name/latency/status）/health check 端点（/health）/优雅关闭（finish in-flight requests）/外部调用超时（别让工具挂死 forever）/输出大小限制（截断大响应）/错误分类（4xx client vs 5xx server）/CORS（浏览器客户端连时）/TLS**（LobeHub）→ 判据：**服务器是生产组件不是脚本**——"工具挂死"=agent 等一辈子；"超时+输出截断+错误分类"=故障可定位；每项都是可观测性基建。
- **生命周期管理**：**OpenClaw CLI mcp：list/show/status/doctor/probe/add 管理 outbound MCP server 定义；worker 启动时连同一 MCP server、async_mcp_tool() 转换工具注册进 beta_agent_toolset_20260401()，为 worker 生命周期保持一个 MCP 会话**（OpenClaw + Claude）→ 判据：**连接有生命周期**——"每请求重连"=握手开销+状态丢失；"worker 生命周期单会话"=一次连接反复用；MCP 定义要可探查（probe/doctor）。
- **提升层**：工具/可复用 Skill（MCP 服务器规范）。

## MCP+Skills 双组合与能力分层：MCP 给数据、Skills 教用法、bundle 成插件（来源：Anthropic Building agents that reach production with MCP + Skills explained + fwdslash MCP 构建指南 + Claude Managed Agents agent-setup 2026 实拉，r634C 落地，与 §技能加载机制分工——那边管"技能怎么进上下文"，本条管"MCP 与 Skills 怎么分工、怎么组合"）
- **双组合**：**MCP 给 agent 访问外部系统工具与数据的通道，skills 教 agent 如何使用这些工具完成真实工作的程序性知识——最强 agent 两者都用，skills 让 MCP servers 从少量连接规模化扩展；两种组合模式：bundle skills+MCP servers as a plugin**（Anthropic 原文）→ 判据：**工具+用法成对装**——"只有 MCP 没有 skills"=agent 有工具不知道流程；"skills+MCP bundle"=连接即能力；插件化让 MCP 超过"几个连接"的规模。
- **三分法**：**fwdslash：模型决定何时跑=工具（tool）；宿主挂为上下文=资源（resource）；用户主动选=提示词（prompt）**（原文）→ 判据：**按触发方分型**——"该当工具当资源"=上下文浪费或调用不可控；"该当资源当工具"=常驻占用；三分明确 MCP 能力怎么暴露。
- **能力配置版本化**：**Claude Managed Agents：agent=可复用 versioned configuration（model/system prompt/tools/MCP servers/skills 捆绑）；创建一次按 ID 引用，跨会话版本化管理；well-defined roles：subagent 明确专门角色+defined tool access levels+成功/完成标准**（Claude）→ 判据：**能力包版本化**——"每会话手工拼工具"=不可复现；"agent 配置按 ID 引用+版本化"=能力集可管理；子 agent 按角色配工具访问级别。
- **提升层**：工作流/可复用 Skill（MCP+Skills 组合）。

## 检索两阶段与质量门：混合检索管召回、重排管精度、TopK 是上限不是保证（来源：Dify 检索管线三阶段质量门 + professionaldeveloper hybrid-recall-rerank-precision + Microsoft Databricks retrieval quality + n8n 元数据富化 2026 实拉，r635A 落地，与 §知识库工程双路召回分工——那边管"双路怎么建"，本条管"召回后怎么过滤、排序、把关"）
- **两阶段职责分离**：**Stage 1 hybrid search（recall）——广撒网 top~50 候选，要的是"右块在集合里某处"；Stage 2 cross-encoder rerank（precision）——精确打分压缩到给 LLM 的 3-5 条；2026 生产 RAG 混合检索不再是可选**（professionaldeveloper + theplanettools）→ 判据：**召回与精度分阶段**——"一步到底"=召回少或噪声多；"wide net + 重排压缩"=先保不漏再保准；rerank 一行改动约 +15% 质量（Databricks）。
- **质量门三阶段**：**Dify 检索管线 quality-first：pre-retrieval SQL metadata 过滤 → 并发 vector+keyword 搜索（阈值延迟应用）→ post-fusion rerank 打分；top_k 是结果数上限不是保证——任何阶段可把结果集减到零**（Dosu/Dify）→ 判据：**TopK 不是配额**——"以为 TopK=必返 N 条"=空结果被硬凑；"每阶段可归零"=宁可无证据不塞噪声；加权混合用 semantic weight+keyword weight 双权重（仅高质量索引模式）。
- **检索前元数据富化**：**n8n 异步富化：每个 chunk 用 LLM 生成 metadata（topics/use_case/risks/audience level/summary）入库供过滤；向量库作 agent 工具时给 description+Include Metadata；嵌入模型必须与入库时一致**（n8n）→ 判据：**检索面先富后搜**——"裸 chunk 只靠相似度"=过滤无从谈起；"LLM 元数据+向量同模型"=可按主题/风险/受众筛；给工具的 description 决定 agent 何时用它。
- **提升层**：工具/工作流（检索两阶段与质量门）。

## 分块与嵌入工程：late chunking、contextual retrieval、递归切分（来源：Jina AI late chunking + Anthropic Contextual Retrieval + arXiv 2607.23507 + pplx-embed-v2-context 2026 实拉，r635A 落地，与 §知识库按标题层级分块分工——那边管"日常分块"，本条管"进阶分块与嵌入方法"）
- **late chunking**：**整文档先用 long-context embedding 模型编码一次，再按 chunk 池化 token 向量——每 chunk 免费继承跨文档上下文；修复固定窗口切碎的 coreference（指代）断裂；需要暴露 token 级输出的模型（jina-embeddings-v3）**（Jina AI 2024 + Diego Rodriguez）→ 判据：**先嵌后切**——"先切后嵌"=chunk 各自孤立、指代断裂；"整文档先嵌再池化"=上下文继承零额外 LLM 调用；模型须支持 token 级输出。
- **contextual retrieval**：**Anthropic：chunk 分拆丢失上下文→每 chunk 用模型写 50-100 token 定位上下文（哪个文档/哪节/指代什么）前加；embedding 索引与 BM25 索引都前加；精确率 +35-49%、RAG 失败降 67%**（Anthropic + DataAspirant）→ 判据：**切块时补定位**——"裸 chunk 入索引"=脱离语境的歧义块；"定位上下文前加再嵌"=检索和重排都受益；两条索引同加。
- **切分策略选型**：**递归切分按优先级分隔符（段落→句子→词）保持语义完整、实测更平衡；分层切分建多级索引；固定 512 无重叠窗口切碎实体破坏上下文精度；演进：agentic/late/recursive with semantic boundaries**（arXiv 2607.23507 + FutureAGI）→ 判据：**切分按结构走**——"盲 token 计数切"=实体与标题被腰斩；"递归+语义边界"=块语义完整；固定窗口是 2023 默认，2026 生产默认已换。
- **提升层**：模型/工具（分块与嵌入工程）。

## RAG 评估四指标与生产决策：recall/precision/groundedness/relevance 分开度量（来源：FutureAGI RAG 评估 + deeplearning.ai RAG 课程 retrieval metrics + Sukru 长上下文 vs RAG 决策表 2026 实拉，r635A 落地，与 §先校验后行动分工——那边管"生成后验证"，本条管"检索与生成链路的专项评估"）
- **四指标各管一段**：**context recall（检索器是否浮现金 passage）/context precision（检索到的多少真相关）/groundedness（回答每 claim 是否被检索上下文支持）/answer relevance（回答是否针对问题）**（FutureAGI）→ 判据：**检索与生成分开评**——"只看回答像不像"=检索坏了不知道；"四指标分段"=recall 管召回、precision 管精度、groundedness 管对齐、relevance 管切题；检索质量另用 recall@k/MRR。
- **生产默认清单**：**query 改写与扩展；元数据过滤；上下文数量控制 3-5 块；注意力友好排列顺序（最相关在前）；引用溯源；严格 prompt 约束（仅用给定上下文、不足明说、[1][2] 标注引用）**（Walter Fan + AI Wisdom）→ 判据：**RAG 是系统不是单点**——"只调相似度"=漏改写漏过滤；"全链路清单"=每环节可单独优化；答案必带引用溯源。
- **长上下文 vs RAG 决策表**：**单合同 50K-200K 低频→long context（RAG 开销不必要）；客服 KB 1M+ 高频→RAG（塞不下+高频 blow up 成本）；Claude Projects 知识近窗口自动启用 RAG 扩容量 10x；1M 窗口无乘数计价不改变架构选型**（Sukru + Anthropic）→ 判据：**按卷与频选路**——"小体量低频"=LC 直接塞；"大体量高频"=RAG；体量×频率是变量不是模型名。
- **提升层**：工作流/可复用 Skill（RAG 评估与决策）。

## 浏览器 agent 感知与交互工程：accessibility tree 免视觉、ref 定位、截图坐标（来源：Playwright MCP + WebRetriever arXiv 2609.35904 + Anthropic computer use best practices + smolvlm2-agentic-gui 2026 实拉，r635B 落地，与 §视觉提取三纪律分工——那边管"从图里提取文字/数据"，本条管"浏览器 agent 怎么感知页面、怎么交互"）
- **结构化感知优先**：**Playwright MCP 用 accessibility tree 结构化快照（role+name+ref），免截图/免视觉模型；WebRetriever：browser_snapshot 转文本（元素名/角色/引用），模型按语义选元素直接 click/input，无需预测像素坐标**（Playwright + arXiv）→ 判据：**能读结构不读像素**——"截图让视觉模型数像素"=慢且贵；"accessibility ref 按语义定位"=快且确定；视觉模型只留给结构读不到的（Canvas/图形）。
- **browser use vs computer use 选型**：**任务在网页内+executor 能暴露浏览器会话→browser use（accessibility ref+screenshots+coordinates）；要操作完整桌面、GUI-only 无页面结构的软件→computer use（截图+鼠标键盘）；两者都跑在你的应用侧，不跑在厂商基建上**（Anthropic）→ 判据：**按目标面选型**——"网页内任务开桌面控制"=多余且脆弱；"GUI-only 软件用页面 ref"=无结构可读；先问目标是否有 DOM/accessibility 结构。
- **像素通道纪律**：**1280x720 默认分辨率（约 80% pixel budget）；预降采样截图是最高影响优化——API 内部有图像大小限制，超限被缩放导致点击坐标偏移；点击精度是根基（点不准→表单不填/按钮不按/工作流失联）；GUI 视觉模型用归一化 [0,1] 坐标输出（smolvlm2-agentic-gui 2.2B）**（Anthropic + Ollama）→ 判据：**坐标空间先对齐**——"截图超限被缩放"=返回坐标全偏；"预降采样+声明坐标空间"=点击落点可靠；坐标归一化到 [0,1] 与分辨率解耦。
- **提升层**：工具/工作流（浏览器感知与交互）。

## 浏览器上下文瘦身：智能裁剪、12K 截断、提取模式（来源：arXiv 2511.19477 intelligent trimming + NiteAgent 12K + AI Kick Start extraction mode + DEV 58% token 2026 实拉，r635B 落地，与 §上下文预算管理分工——那边管"总预算怎么规划"，本条管"浏览器页面上下文具体怎么瘦"）
- **智能裁剪**：**全量 accessibility tree 快照+对话历史给轻量模型→返回要保留的元素 ref 范围→构造过滤快照；提示保留全部交互元素（导航/表单/按钮/模态）激进总结重复区；实测浏览器 agent 58% token 花在页面上**（arXiv + DEV）→ 判据：**页面不是全量进上下文**——"整棵 a11y tree 塞给主模型"=58% token 烧在页面；"轻量模型先筛 ref 范围"=只留任务相关+交互元素；裁剪是独立步骤不是主模型自己省。
- **提取模式与截断**：**数据提取用专属模式：open URL→一张截图→模型填你定义的 schema（不用 agent 点击遍历）；产品列表页 DOM 截到 12K 字符够覆盖；temperature 0.05 近确定性提取（temp=0 反而偶发 JSON parse 失败）**（AI Kick Start + NiteAgent）→ 判据：**读页与交互分模式**——"提取数据也走点击循环"=慢且易错；"一截图+schema 填充"=确定性提取；截断到覆盖页列表的字符量而非整 DOM。
- **提升层**：模型/工具（浏览器上下文瘦身）。

## 浏览器自动化放置与安全：浏览器在异常路径、专属 profile、低信任车道（来源：anakinwriters browsers on exception path + OpenClaw browser profile/CDP + sureprompts 爆炸半径 + AIPromptProphet 提取白名单 2026 实拉，r635B 落地，与 §Agent 工具面安全分工——那边管"工具描述注入"，本条管"浏览器这类高权工具怎么放置"）
- **浏览器在异常路径**：**交互式工作流才值得 browser tax：登录/表单提交/截图/视觉断言/文件上传/多步客户端状态；把浏览器当通用读取路径=每个提取变有状态资源问题（进程生命周期/内存上限/页面崩溃/导航超时/代理分配）**（anakinwriters）→ 判据：**能 HTTP 抓不启浏览器**——"每读一页开 headless"=状态资源灾难；"交互才用浏览器、静态用 HTTP"=按需付 browser tax；浏览器是例外路径不是默认路径。
- **专属 profile 与隔离**：**OpenClaw 用专用 Chrome/Brave/Edge/Chromium profile（gateway loopback 控制服务），与个人浏览器隔离——agent profile 从不触碰个人 profile；已有会话 CDP 支持要验证发现的 WebSocket 端点；浏览器来源内容放低信任车道（tighten browser-output boundaries）**（OpenClaw）→ 判据：**agent 浏览器与个人浏览器物理隔离**——"共用 profile"=登录态/历史污染；"专属 profile+CDP 端点验证"=attach 错浏览器可防；浏览器输出默认低信任。
- **架构级防御**：**extension over 日常浏览器的爆炸半径最大（按构造）；防御是架构级非 prompt 级——分离 planning context 与 content-reading context、capability minimization；受控提取 prompt：只开 approved URL 白名单、按页面上所示提取不推断缺失值、忽略要求指令/密码的文本**（sureprompts + AIPromptProphet）→ 判据：**高权通道要最小暴露**——"把 agent 塞进日常浏览器扩展"=爆炸半径最大；"规划与读内容分上下文+能力最小化"=注入面收窄；提取任务给 URL 白名单+不推断。
- **提升层**：工作流/可复用 Skill（浏览器放置与安全）。

## 国产 Agent 生态与技能市场：三大平台、付费链路、自适应调度（来源：腾讯 SkillHub/SkillPay + 阿里 Lingma/SkillsHub/JVS + DeepSeek Harness + 智谱多模态 Coding 2026 实拉，r635C 落地，与 §MCP+Skills 组合分工——那边管"工具与用法怎么配"，本条管"中国市场里技能怎么发现、安装、付费、调度"）
- **技能市场三大平台**：**腾讯 SkillHub（8 万+ skills，国内高速镜像秒装，三线并行安全审核，TRACE 评测体系；官方 Skills=腾讯文档/会议/地图/ima/QQ 浏览器；基于 OpenClaw 生态本土化兼容全量技能）；阿里 Lingma Agent Skills（skill=结构化指令与流程：注入专业知识/标准化流程/可复用）+ SkillsHub 107 精选；ModelScope Skills 中心+80000 外部技能统一检索**（央广网 + 阿里云 + ModelScope）→ 判据：**技能先搜平台再自建**——"闭门造技能"=重复造轮子；"官方 skills 四件套（docx/pdf/pptx/xlsx）+frontend-design 基础必装"=起步清单；平台审核/评测帮筛质量。
- **付费链路与调度**：**SkillPay（2026-07-16）：技能分发+Agent 调用+技能支付同链路打通——商家上架 Pay Skill 获面向 Agent 收费能力，平台负责来源认证/内容完整性校验/可信调用入口；Skill Pilot：自适应技能调度引擎（环境感知路由+用户偏好+自学习优化+fallback+成功率评分），自动选最佳技能满足任务**（央广网 + SkillHub）→ 判据：**技能可商业化可编排**——"只装免费技能"=能力天花板低；"Pay Skill+平台校验"=付费换专业能力；"调度引擎带 fallback 与成功率"=自动换源不中断。
- **一切皆插件与官方集成**：**DeepSeek Harness（dsh）：一切皆插件架构（Cordis 驱动），npx 运行编码 agent，读同一 SKILL.md 格式；官方四件套+create-pr+frontend-code-review 等优先级清单；Agent Skills 自动发现（用户级 ~/.agents/skills/、项目级 ./.deepcode/skills/）；DeepSeek V4 集成进 Copilot Chat 模型选择器保留 agent mode/skills/MCP；智谱原生多模态 Coding 基座（画框/截图/读网页，200k 上下文）**（DeepSeek API docs + 智谱）→ 判据：**先查原生再建插件**——"平台已原生覆盖还自建"=维护双份；"复用官方 skills 优先级清单"=起步有据；多模态感知-行动链路从文本延伸到视觉。
- **提升层**：工具/工作流（国产技能市场与调度）。

## 推理成本杠杆表：prompt caching、semantic caching、batch 与输出约束（来源：TheRouter/varunsingla tokenomics/Compresr/Levelop 2026 实拉，r635C 落地，与 §缓存断点分工——那边管"改配置/换模型破坏前缀缓存怎么防"，本条管"成本杠杆选哪几个、各减多少"）
- **缓存折扣量化**：**OpenAI GPT-5.5 cached $0.50/MTok vs base $5.00（90% off）；Anthropic 90% off cached input；缓存是稳定高复用 system prompt 的最高杠杆 FinOps 干预；GPT-6 默认更高缓存命中率；输出缓存管确定性/近确定性查询（FAQ）**（TheRouter + AgamiSoft）→ 判据：**先锁稳定前缀**——"每次请求重算 system prompt"=90% 折扣白扔；"system prompt+schemas 锁定"=缓存命中；输出缓存只适用确定答案。
- **杠杆表**：**prompt caching −70% input；semantic caching（60% hit）−60% total；model routing（70% 路由便宜模型）−42% total；截断会话历史 −40% input；精简 prompt −30% input；限制输出长度 −30% output；batch 处理（50% off）−50%；动态上下文压缩（query-aware 切 RAG/历史/输出）可减 60% input**（varunsingla + Compresr）→ 判据：**杠杆按场景组合不单点**——"只靠一种"=上限低；"缓存+路由+截断+约束叠加"=70% 级降本；先量化各杠杆影响再排优先级。
- **路由分级**：**按任务复杂度路由：简单查询（"Paris is in France?"）不需要 frontier——最经济能处理的模型即可；80% 查询预算层解决可砍 65-80%；团队加路由层常报 40-85% 账单降幅；案例 $48K→$19K（路由单独省 $7K/月）**（Boundev + Levelop）→ 判据：**预算层承接大头**——"所有请求都走旗舰"=为简单任务付溢价；"复杂度分级+80% 预算层解决"=成本与质量解耦；路由是独立层不是模型内建。
- **提升层**：工具/工作流（推理成本杠杆）。

## 推理工程新范式：MoE 稀疏激活与 spec decoding 无损加速（来源：DeepSeek-V4.1-Flash + vLLM speculative decoding + NVIDIA Jetson 边缘 2026 实拉，r635C 落地，与 §推理引擎选型分工——那边管"选哪个引擎/部署形态"，本条管"MoE 结构与投机解码机制"）
- **MoE 稀疏激活**：**DeepSeek-V4.1-Flash：552B backbone MoE，prefill 仅激活 8B、decode 16B；196B Engram 记忆层+视觉编码器（总权重 763B），100 万 token 上下文——稀疏激活让超大模型推理成本可控**（钛媒体）→ 判据：**看激活不看总参**——"总参 552B 吓人"=实际按激活计费；"prefill/decode 分开激活"=成本按阶段算；记忆层与视觉编码器是额外权重。
- **spec decoding 无损保证**：**小 draft 模型猜 5-8 tokens→大模型单次前向验证全部（成本≈生成 1 token）；数学上与单独跑大模型相同（理论无损到硬件数值精度）；20-50% 加速；draft 与主模型匹配关键（Qwen 3.5 0.8B 配 27B）；vLLM v0.16+ 支持含结构化输出；suffix decoding 动态推测 16/32**（InsiderLLM + vLLM）→ 判据：**无损加速优先**——"投机解码有损"=谬误（理论无损）；"draft 匹配+单次验证"=20-50% 白赚；结构化输出也支持就不是 llama.cpp 专属。
- **本地部署参数**：**vLLM recipes：Qwen3.6-27B（--kv-cache-dtype fp8 --attention-backend flashinfer --gpu-memory-utilization 0.5）；Qwen3.8-Flash-Next 原生 262,144 context；Jetson 边缘用 nvfp4 量化+spec decoding 提推理性能**（vLLM + NVIDIA）→ 判据：**部署参数可复现**——"凭感觉配显存"=OOM 或浪费；"recipes 参数照抄再调"=起步可复现；fp8 kv-cache+量化是显存杠杆。
- **提升层**：模型/工具（推理工程新范式）。

## 语音 Agent 架构选型：级联 vs 全双工、四件事循环、分级委派（来源：arXiv 2603.05413 + OpenAI GPT-Live + AssemblyAI + Modern AI Guide + ByteDance Seeduplex + NVIDIA VoiceChat 2026 实拉，r636A 落地）
- **级联 vs 语音原生**：**cascaded（STT→LLM→TTS 分段）控制可调试性高、工具使用成熟确定，适合复杂任务 agent；speech-native（全双工原生语音模型）更像黑盒、工具使用欠成熟，适合自然低复杂度对话——2026 诚实答案：自然对话用原生、需要工具用级联；且级联栈 2026 已够快：良好 Claude 语音栈 sub-700ms 响应低于人类感知"停顿"阈值**（Modern AI Guide + Claudexia）→ 判据：**按任务复杂度选架构**——"无脑上全双工"=工具调用不稳；"无脑级联"=自然感差；工具多→级联、纯闲聊→原生。
- **四件事循环与"何时说"**：**每个语音 agent 循环做四件事——STT 转文本、LLM 决定说什么、TTS 转回语音、orchestration 决定何时说（最被低估的部分）；Turn-taking 是体验核心**（AssemblyAI）→ 判据：**编排是第四件事**——"只管听和说"=抢话/冷场；"显式管何时说"=自然轮次；turn detection（RNNT ~450ms / 神经 VAD sub-20ms）是编排的输入。
- **全双工与分级委派**：**GPT-Live：从音频路径移除轮次检测器，语音模型全双工同时听说；需要更深推理/工具时 consult GPT-5.5 等前沿模型而不打断对话节奏（分级委派）；Seeduplex：原生"边听边说"框架+语音语义联合建模+RL→精准抗干扰、动态判停**（OpenAI + 字节 Seed）→ 判据：**主语音模型≠最强大模型**——"一个模型扛所有推理"=对话冻结；"轻快主模型+重推理委派前沿"=节奏与深度兼得；全双工省掉单独轮次检测器。
- **提升层**：模型/工作流（语音架构选型）。

## 语音延迟与打断工程：预算、jitter 治理、barge-in 状态机（来源：Tenzed + TestMu + SkillMD + Anthropic cookbook + Better Stack Qwen Audio + Open Jarvis 2026 实拉，r636A 落地）
- **延迟预算三锚点**：**端到端 240-320ms（WebRTC 媒体网关+双向 PCM+speculative tokenization）；TTFW（呼叫者说完到 agent 第一音频字节）<800ms 避免可感知停顿；FBL <300ms；级联下 system prompt <500 tokens 降延迟（长提示直接抬 latency）**（Tenzed + TestMu + Relinns）→ 判据：**预算拆到阶段**——"只盯总延迟"=不知道卡在哪；"TTFW/FBL/端到端三锚点"=分段归因；提示短=延迟低（语音场景提示要极简）。
- **jitter 治理**：**目标：标准差<100ms、P95-P50 gap<200ms；手段：模型 warm 保持/连接开始预加载、音频输出 buffer（50-100ms 平滑、填满才播）、处理 LLM 生成方差**（SkillMD voice-agents）→ 判据：**平滑比快更重要**——"平均快但忽快忽慢"=听感差；"warm 模型+输出缓冲"=抖动压平；P95-P50 差距是 jitter 的真指标。
- **barge-in 是状态机转换不是截断**：**用户打断：VAD（AEC 后持续跑）检测说话→触发 barge_in_detected→截断 agent 音频输出流、抑制 in-flight 部分泄漏、开始新输入 turn；打断干净的关键=当状态机转换处理而非简单 cutoff；支持工作先落地（volume ducking/双 VAD 防误读 turn 结束）；双向：后台任务完成 agent 也可主动打断用户；误报一次=该通电话信任不恢复**（Better Stack + ChatdollKit + Prodinit）→ 判据：**打断要走状态机**——"硬切音频"=泄漏/卡顿；"VAD→截断→抑制→新 turn"=干净；误报率是最被低估的指标。
- **提升层**：模型/工具（语音延迟与打断工程）。

## 语音栈选型与工具面：协议、运行时、模型、插件（来源：火山引擎 RealtimeAPI + 阿里云 Qwen-Audio + fp8.co + CSDN LiveKit + OpenClaw voice-call + HF/ModelScope 2026 实拉，r636A 落地）
- **协议与弱网**：**端到端语音 API 三协议：WebSocket/AOQ/WebRTC；AOQ（阿里）推荐用于稳定延迟、弱网络韧性、内建全双工降噪与回声消除；豆包 RealtimeAPI 支持 WebSocket 流式边发边收**（阿里云 + 火山引擎）→ 判据：**协议按网络环境选**——"都走 WebSocket"=弱网掉链；"AOQ/WebRTC 弱网优先"=韧性；降噪回声消除是弱网体验的一半。
- **开源运行时**：**Qwen Audio Agent（阿里开源）：WebRTC server+音频预处理+推理编排+合成流式，持久双向连接 sub-300ms，模型无关；LiveKit Agents：可自托管 WebRTC、STT→LLM→TTS、实时 speech-to-speech、turn detection/barge-in、SIP 电话接入**（fp8.co + CSDN）→ 判据：**先查开源运行时再自建**——"从零拼管线"=重复造轮；"Qwen Audio/LiveKit 起步"=协议/打断/编排现成；自托管=数据不出域。
- **模型与插件**：**TTS：MOSS-TTS-Nano 0.1B CPU 可跑无需 GPU（本地 demo/轻集成）；ASR：SenseVoice 五能力（识别/语种/情感/声学事件/逆文本正则）+FunASR 统一工具包一行调用、Qwen3-ASR 52 语言；Agent 侧：OpenClaw voice-call 插件（initiate/continue/speak_to_user/end_call + callId 生命周期）与 voice-tts skill（clawhub install）；三种语音集成模式：embedded voice / voice layered on existing agents / voice as callable tool**（ModelScope + HF + OpenClaw + deeplearning.ai Vocal Bridge）→ 判据：**语音是能力不是产品**——"语音=整套基建"=重；"语音作为可调用工具"=按需加层；callId 显式管理多路通话；0.1B CPU TTS=端侧可行。
- **提升层**：工具（语音栈选型与工具面）。

## Agentic 视频管线：多阶段分离、多 agent 分工、有界自主（来源：OpenMontage + aitutorialmaker + OpenClaw Video Podcast Maker + Seedance 2.0 2026 实拉，r636B 落地）
- **2026 主导=agentic orchestration**：**视频创建当多阶段管线——专用模型处理特定任务，不是单一整体模型做一切；分离 ideation/资产生成/编辑/后期四阶段→质量控制+显著降早期幻觉率；OpenMontage（15K★ AGPLv3）12 pipelines/52 工具/500+ skills 把 Claude Code/Cursor 变视频工作室，给 prompt→agent 研究主题/写脚本/生成检索视觉/录旁白/找配乐/装配**（aitutorialmaker + Neodrop）→ 判据：**管线分离不是炫技**——"一个模型全包"=幻觉高；"四阶段分离+每阶段专用模型"=质量可控；编排器是生产系统不是 wrapper。
- **三 agent 分工与自动返工**：**Scriptwriter Agent（研究趋势+高转化脚本）→Visual Director Agent（拆脚本成 storyboard+生成模型 prompt）→Footage Reviewer Agent（分析生成 clips 质量一致性，自动 re-roll 不达标素材）——返工是循环内建的**（OpenClaw News）→ 判据：**审片是独立角色**——"生成完直接过"=残次素材进装配；"reviewer 自动 re-roll"=质量门槛内建；每 handoff=检查点。
- **有界自主+人工检查点**：**agentic editing 自主不保证可靠——合理部署是有界：给 agent 访问权限+request human checks before delivery；Video Podcast Maker 9 步流程含 mandatory stop（Remotion 合成+Studio 预览后必须停）；Seedance 2.0 统一多模态音视频联合生成（文字/图片/音频/视频四模态输入+最全多模态参考编辑）**（aitutorialmaker + openclawai + 字节 Seed）→ 判据：**自主与检查点并存**——"全自动无人审"=翻车；"mandatory stop 人工看"=关键节点把门；参考图绑定节拍=一致性来源。
- **提升层**：工具/工作流（Agentic 视频管线）。

## 视频提示与分镜工程：结构化提示、时间戳模板、草稿迭代（来源：Dreamina Seedance 2.5 + Opten + 即梦短剧 + 掘金短视频实战 2026 实拉，r636B 落地）
- **结构化电影提示与资产绑定**：**Seedance 2.5：30 秒连续叙事而非一次性描述；"@"标签绑定资产到精确节拍（@Image1 close-up/@Image2 wide）；定义镜头语言（push-in/tracking/orbit）/光照/情绪/节奏/声音方向；扩展生成模式到 180 秒；Seedance 2.0 四模态输入**（Dreamina）→ 判据：**提示是叙事不是描述**——"一句话场景"=模型自由发挥；"@绑定+镜头语言+情绪节奏"=可控叙事；资产引用进 prompt 是跨镜头一致的关键。
- **时间戳分镜模板**：**15s 模板：0-4s ENTRY（setup）→4-10s REVELATION（turn，dolly-in/crash-zoom）→10-15s ACTION RESPONSE（resolution，手持+运动模糊）；8s=两幕 ENTRY→PAYOFF；10s=SETUP→…；短提示实践：4-6 秒提示词+1 参考图+生成 2-4 草稿→选最佳运动方向→更紧约束重写→终版**（Opten + Seedance guide）→ 判据：**分镜有节奏结构**——"匀速平铺"=无张力；"ENTRY/REVELATION/PAYOFF 三幕"=信息结构；草稿→选向→重写=迭代收敛。
- **多模态素材管线**：**即梦短剧：角色图（每人大头照+全身照）+场景图→Seedance 2.5 全能参考→上传三图→按模板写镜头；实战：脚本输出 JSON 数组（scene_id/duration/visual_prompt/narration）→人工审脚本重点检查画面描述可生成性（避免抽象"数据流穿梭"改"蓝色粒子沿光线流动赛博朋克"具体描述）→关键帧生成；Wan2.2 8G 显卡本地 Qwen 量化跑分镜脚本**（腾讯云 + 掘金 + 阿里云）→ 判据：**画面描述要可生成**——"抽象概念进 prompt"=模型瞎画；"具体视觉描述"=可控；角色图/场景图先锁定外观再生成。
- **提升层**：工作流/可复用 Skill（视频提示与分镜工程）。

## LoRA/QLoRA 微调工程：成本、数据规模与 PEFT 选型（来源：AI Herald + Future AGI + PEFT 实证 + nirajiitr SLM + dev.to 数据集错误 2026 实拉，r636B 落地，与 §推理引擎选型分工——那边管"部署选型"，本条管"微调方法与成本"）
- **LoRA 成本与质量**：**LoRA 冻结模型训小低秩适配器：比全微调快 60%、VRAM 减半、质量损失通常<2%；7B LoRA 更新<1% 总参数，任务性能接近全微调；QLoRA：8B 级单张 24GB 消费 GPU 过夜训 10K 样本，云 spot $5-30；70B 需 80GB H100；SLM（1-4B）推理成本固定（硬件）非可变（per token）、延迟低本地、隐私主权**（AI Herald + Future AGI + nirajiitr）→ 判据：**微调先算成本账**——"全微调起步"=贵且慢；"LoRA/QLoRA 起步"=$5-30 试错；SLM 场景=固定成本换确定性。
- **PEFT 选型反常识**：**PEFT 低数据场景收敛比全调慢（实证反常识）；资源受限推荐：低/中数据全调、高数据+时间受限用 PEFT；内存受限 BitFit/IA³ 最优（低资源）、IA³ 中高资源；性能受限 IA³/LoRA**（arXiv 2304.14999）→ 判据：**数据量决定方法**——"数据少也上 LoRA"=收敛慢；"低/中数据全调+高数据 PEFT"=按数据规模选；方法选型看约束轴（时间/内存/性能）。
- **RL 后训练与数据**：**DPO 数据集 prompt/chosen/rejected 三列（ultrafeedback_binarized）+DPOTrainer；RLHF/DPO 数据预算 2-5k 对；评估 holdout 5-10%（最少 ~500），按 prompt 聚类分切防近似重复跨侧；preference accuracy（chosen 高于 rejected）是比训练 loss 好得多的早停信号；合成数据微调：生成 prompt 最重要（弱 prompt→窄重复数据集），指定任务类型+输出格式 JSON**（Hyperion + Misar + AI/TLDR）→ 判据：**偏好数据是双样本**——"单条好回答"=没对比；"chosen/rejected 对+聚簇 holdout"=可测偏好；preference accuracy 早停优于 loss。
- **提升层**：模型/工具（LoRA 微调工程）。

## 品牌一致图像工作流：参考池、品牌表、锁定骨架（来源：Adpicto + Modern Creator + FRPROTECH + Domer + FindAiverse + MindStudio 2026 实拉，r636C 落地）
- **参考优先是最大杠杆**：**上传实际产品照/品牌生活方式照/团队照/室内照 15-30 张代表品牌视觉世界，AI 用作参考池（主体处理/光照/调色/放置惯例），新生成继承参考池惯例（"周二的新图继承你周一的光照"）；锁 1-2 个批准参考=保持系列连贯的最大杠杆；固定 prompt 骨架（style/lighting/palette/framing 语言相同，只改主体）**（Adpicto + FRPROTECH）→ 判据：**一致性靠参考不靠运气**——"每次重写 prompt"=风格漂移；"参考池+锁批准参考+骨架只改主体"=系列连贯；15-30 张参考池是品牌视觉世界的采样。
- **品牌表与 source pack**：**brand sheet：单张 AI 生成图编码色板/字体/情绪词/视觉语言，随每个 prompt 上传=视觉锚点（一次建表替换每次手工设计决策）；source pack：品牌色+批准产品截图+允许参考图+禁用图+示例构图+brief；先加维度与安全区（防一张景观图裁坏成方形/竖版/缩略图）**（Modern Creator + FindAiverse）→ 判据：**资产先建后用**——"每张图从零设计"=不一致；"brand sheet 单图锚定"=prompt 旅行；"维度+安全区先定义"=多比例不翻车。
- **可复用 style system 与 logo 边界**：**品牌指南转 prompt 块（光照/镜头感/调色板/纹理+负面约束"无可见 logo/无文字/无塑料光泽"），存共享文档+参考图——目的不是消除人类判断而是消除猜测（三个设计师写 prompt 得三套风格）；AI 模型更擅长 logo 探索而非 logo 交付（按 wordmarks/icon+wordmark 类别生成视觉方向，目标不是成品 logo）**（Domer + MindStudio）→ 判据：**风格块是组织资产**——"个人凭手感写"=三人三风格；"共享 prompt 块+负面约束"=可复现；logo 先探索方向再交付成品。
- **提升层**：工作流/可复用 Skill（品牌一致图像工作流）。

## 图像生成提示词工程：八段结构、五维评分、诊断式迭代（来源：ToolWorthy + Taylor & Francis 五维框架 + FreeAcademy + Floniks 2026 实拉，r636C 落地）
- **结构化提示八段与可控参数**：**Subject→style→camera/lens→lighting→composition→materials→constraints→negative；锁 seed（出好结果就锁住复现变化）；调 creativity/CFG/图像参考/LoRA/style adapters；生成 3-5 初始候选**（ToolWorthy）→ 判据：**提示按段写不混写**——"一句散文"=模型自由发挥；"八段结构"=每段可单独调；seed 锁定+CFG/参考=可控变量。
- **五维美学评分框架**：**Color（具体色相与意象）/Style（语流节奏原创）/Composition（空间层次焦点层级）/Lighting（光源强度情绪明确）/Characteristics（情感共鸣）——审美分<8 就继续精修增强描述丰富度与五维平衡**（Taylor & Francis）→ 判据：**评分先于精修**——"看感觉改"=无基准；"五维评分<8 触发精修"=量化门槛；每维给具体增强方向。
- **诊断式迭代循环**：**第一代是诊断不是最终结果（哪些 prompt 层生效哪些需调）；四步循环 generate→diagnose→isolate→adjust，每迭代只针对一个元素（composition 先→lighting→style→fine details 后）；小批量 4 张→选最接近目标（非最漂亮）→平实写下错在哪→每次只改一个→5-10 遍胜过 50 次随机**（Floniks + FreeAcademy）→ 判据：**迭代是诊断驱动的**——"一次生成撞运气"=方差高；"小批量+隔离变量+每次改一个"=收敛；首选构图后细节=杠杆顺序。
- **提升层**：工具/工作流（图像生成提示词工程）。

## 深度研究 Agent 栈：按工作选工具、研究生命周期、四阶段学术栈（来源：TechieHub + OpenAI Deep Research + Nous Hermes + FluxGrowth 2026 实拉，r636C 落地，与 §检索质量门分工——那边管"RAG 检索质量"，本条管"研究 agent 工具选型与编排"）
- **2026 无单一最优研究工具**：**最佳研究栈不是单工具而是组合：ChatGPT Deep Research（最长最结构化报告）、Perplexity（最快+透明引用）、Claude Research（推理综合最强）、Gemini（Google Workspace 内）、Elicit（学术文献综述）——多数专业人士组合 2-3 个；按工作选：广综合/工作区接地/文献发现/引用审计各有其主**（TechieHub + Rework）→ 判据：**先定研究工作再选工具**——"一把锤子打所有"=错配；"按工作类型选 2-3 组合"=互补；引用透明/结构化/推理各有长板。
- **研究生命周期与自改进**：**Deep Research（OpenAI）：独立 agent——给 prompt 就 find/analyze/synthesize 数百在线来源，研究分析师级综合报告（o3 优化 web browsing+data analysis）；Hermes Agent（Nous）：研究是生命周期非一次性查询——research-paper-writing skill 覆盖全文综述→实验执行监控→分析→起草→修订，每次交互学习、skills 自我改进**（OpenAI + NXplace）→ 判据：**研究是可复用生命周期**——"每次从零查"=无积累；"综述→实验→分析→起草→修订闭环"=过程可再跑；自改进=技能随交互长。
- **四阶段学术栈**：**Consensus Meter（读全文前看领域立场）→Semantic Scholar/Elicit（扩展搜索相邻子话题）→ResearchRabbit（丢 5-10 种子论文表面引用簇/关键作者/漏掉论文）→Connected Papers（单主题聚焦图）；Elicit 系统综述：表格列自定义提取（sample size/intervention/outcome/effect size/conclusion）+引用保留+CSV 导出，报告省 80% 时间**（FluxGrowth + Elicit + AiPedia）→ 判据：**学术检索分阶段**——"一步到位"=漏相邻子话题；"立场→扩展→引用簇→聚焦图"=覆盖递增；表格化提取把综述变结构化劳动。
- **提升层**：工具/工作流（深度研究 Agent 栈）。

## Text2SQL 与数据访问 Agent 架构：探索范式、语义层、两层修复（来源：APEX-SQL + 语义层中介 SMQ + FlexSQL + LangGraph Six-Node + eScholarship 2026 实拉，r637A 落地，与 §检索质量门分工——那边管"RAG 检索质量"，本条管"自然语言到数据库的结构化访问"）
- **从被动翻译到 agentic 探索**：**APEX-SQL 把 Text2SQL 从 passive translation 转为 agentic exploration——hypothesis-verification loop 把模型推理接地到真实数据；schema linking 阶段：logical planning 语言化假设+dual-pathway pruning 减搜索空间+parallel data profiling 对照真实数据验证列角色+global synthesis 保拓扑连通**（arXiv 2602.16720）→ 判据：**写 SQL 前先验证假设**——"凭 schema 一次翻译"=列角色猜错；"假设-验证循环+数据 profiling 对照真实数据"=接地；双路剪枝=搜索空间可控。
- **语义层中介与确定性编译**：**不直接对原始表写 SQL——agent 在语义层推理（Semantic Model Query 紧凑中间表示），确定性引擎编译 SMQ→方言正确 SQL，agent 检查/组合/执行；意图与物理执行解耦（single-tool think-act）；Text2SQL 上下文分层=DB Schema（表/列/类型/键关系）+Sample Data（代表行推断格式）**（arXiv 2606.31041 + eScholarship）→ 判据：**语义层把"意图"和"执行"分开**——"对裸表写 SQL"=方言/结构耦合；"SMQ+确定性编译"=意图稳定、执行可换；schema+样本数据双上下文=生成对齐真实结构。
- **灵活交互与两层修复**：**FlexSQL 核心=灵活数据库交互：推理任意时刻可探索 schema/查数据值/跑验证查询；生成多样执行计划覆盖多查询解释；每计划 SQL 或 Python 按任务；两层修复（代码级错误回溯到计划级修订）**（arXiv 2605.02815）→ 判据：**探索权不只在生成时**——"一次生成执行"=多解释漏覆盖；"任意时刻探索+多样计划"=歧义可控；两层修复=小错不推倒重来。
- **共享状态与重试记账**：**LangGraph Six-Node StateGraph：共享 state 携带 question/sql_query/schema/results/answer/error_log/retry_count/is_relevant 六节点顺序执行——错误日志与重试次数显式进状态，节点可据 error_log 决定修正路径**（arXiv 2609.22917）→ 判据：**状态里显式记账**——"错误只进日志不读"=无法修正路径；"error_log+retry_count 进共享 state"=节点可决策；SQL agent 的关键=重试不是重跑而是修。
- **提升层**：模型/工作流（Text2SQL 与数据访问 Agent）。

## 电子表格与 BI Agent 模式：描述意图、计划批准、四层仪表板（来源：Copilot in Excel + Agent Mode + Lapu + Excel MCP + Quick BI + HENGSHI + FutureAGI 2026 实拉，r637A 落地）
- **交互从操作位移到描述意图**：**Quick BI 智能小 Q：用户选数据集后自然语言提问→意图识别/数据匹配/可视化生成+多轮追问下钻（先整体趋势→区域差异→波动原因）；做图表从"配置"变"对话"**（阿里云）→ 判据：**意图识别是多轮入口**——"点按钮配置"=人找功能；"说清问题+多轮下钻"=能力进对话；追问下钻=分析路径可续。
- **Excel agent 描述→计划→批准→执行**：**Agent Mode in Excel：描述想完成什么，agent 用 Excel 内建工具执行步骤（预算更新/财务建模/数据分析）；工作流=读工作簿→草拟计划（改哪些列/写哪些公式/建哪些 sheet）→等批准→执行真实文件；任务描述例：'dedupe by email, normalize Date 列 ISO, build pivot by region, save as Q2-clean.xlsx'；Excel MCP Server 通过官方 COM API 驱动真实 Excel（Power Query/DAX/VBA/PowerPivot/Python in Excel），需 Windows+桌面 Excel**（Microsoft Learn + Lapu + excelmcpserver）→ 判据：**改文件前先批计划**——"直接执行"=可能改错列；"草拟计划+等批准"=可控变更；COM API 驱动真实 Excel=引擎保真（非模拟）。
- **四层仪表板架构**：**NL-to-SQL planner（读问题生成 SQL 计划）→可视化层（自动选图表类型/交互/下钻）→Narrative engine（写摘要/建议下一步/生成标题）→自动化（定时刷新/异常告警/Slack 邮件路由）；HENGSHI 数据特征选图规则（明确时间趋势→折线图，<5 类别→饼图，复杂维度组合→热力图）**（FutureAGI + 衡石）→ 判据：**仪表板是四层不是一张图**——"只生成图表"=缺叙述/自动化；"planner→可视化→叙述→自动化"=完整闭环；特征驱动选图=类型有依据。
- **提升层**：工具/工作流（电子表格与 BI Agent 模式）。

## 自主数据科学 Agent 与数据平台：全管线、触发边界、路由（来源：DeepAnalyze + n8n Agents/ClickHouse + 阿里问数 Agent/DataWorks + OpenClaw data-analyst 2026 实拉，r637A 落地，与 §MCP 工具面工程分工——那边管"工具面安全"，本条管"数据 agent 平台能力与触发边界"）
- **全管线自主数据科学**：**DeepAnalyze（人大数据实验室 4.7K★）：给任务+文件跑全管线无人介入（数据准备/分析/建模/可视化/报告生成）；开放数据研究（探索多来源→分析师级书面报告）；Docker 沙箱+API key 管理+托管部署（企业就绪）；Insight Orchestra 自托管 4 agents+沙箱代码执行+可选 LLM**（AI/TLDR + Bright + DEV）→ 判据：**数据科学可全自主也可半自主**——"每步人介入"=慢；"全管线 agent+沙箱"=无人介入；沙箱=代码执行有界。
- **平台能力形态**：**n8n Agents（2026-09）：描述 agent 该做什么+选模型+给 tools 和工作流即可，agent 自己决定步骤；ClickHouse node 10 操作（参数化查询/批量 Insert 10 万行/Upsert 自动检测 ReplacingMergeTree/Create Table 自动推断 schema）；Conversational PostgreSQL agent+MCP（自然查询→摘要/图表/增删改记录）**（n8n Blog + Community）→ 判据：**平台 agent 把编排交给描述**——"手工拖节点"=改一次动一次；"描述+模型+tools"=步骤 agent 定；数据库节点操作齐全=数据交互闭环。
- **问数与路由**：**阿里问数 Agent：意图识别/数据匹配/逻辑生成/可视化呈现秒级返回+多轮追问；DMS 问数 Agent 可定制可发布作为统一数据服务层全天服务；DataWorks Data Agent 自动路由到 ChatBI Skill（数据问题自动路由不用切工具，也可显式 /dataworks-chatbi-s 指定）；OpenClaw data-analyst skill 触发边界=交付物必须是 spreadsheet 文件（主交付物是 Word/HTML/独立 Python 脚本/数据库管线/Google Sheets API 集成时不触发，即使涉及表格数据）**（阿里云 + OpenClaw LobeHub）→ 判据：**路由与触发边界先定**——"问题跨工具"=人切工具；"自动路由 ChatBI+显式可指定"=双通道；skill 触发边界=交付物形态定（spreadsheet 才接）。
- **提升层**：工具/工作流（自主数据科学 Agent 与数据平台）。

## 代码审查 Agent 组织化：上下文注入、触发模型、硬规则约束（来源：GitHub Copilot Docs + CodeRabbit + alibaba/open-code-review + PR-Agent 2026 实拉，r637B 落地，与 §AI 生成代码收 diff 五连查分工——那边管"收 AI 代码时人怎么查"，本条管"用 agent 审 PR 的组织方式"）
- **组织上下文注入**：**agent skills+MCP servers 用于需要组织特定上下文的 review——标准 checklist 应用到迁移 PR/语言框架特定审查 pass（monorepo）/优先风险区（authorization/billing 逻辑）；MCP 从第三方平台拉上下文（issue trackers/文档系统/service catalogs）；MCP 决策框架=先决定要 agent 做什么：要在 PR 线程发评论只有 GitHub MCP 能写回 GitHub，其他 server 分析交回 findings，转评论需 GitHub MCP 在链中**（GitHub Docs + mcpfind）→ 判据：**review 上下文按组织注入**——"通用审查"=漏迁移 checklist/风险区；"agent skills 标准清单+MCP 外部上下文"=组织特定；写回能力=先定决策再选 server。
- **触发模型与门禁**：**手动审查（精确控制何时介入）vs 自动审查（一致覆盖：打开时/草稿/每次新 push 可选）；Repository Ruleset 自动审查每个 PR 到目标分支；Branch Protection 把 Copilot review 设为 required status check——阻止 merge 直到关键发现解决**（GitHub Docs + msbart2）→ 判据：**审查触发是策略不是默认**——"全员手动点"=覆盖不一致；"Ruleset 自动+required status check"=门禁化；自动触发时机（开/草稿/每次 push）按风险选。
- **AI 注释识别与硬规则**：**Copilot review 注释看起来像人类注释（除非看 avatar）——PR 模板标注"Copilot auto-review enabled——verify AI suggestions before accepting"；merge 前审 'Fix with Copilot' commits；alibaba/open-code-review（48K★）'pins the LLM down with hard rules'——确定性工程×Agent 混合架构，F1 超 Claude Code、Token 仅 1/9、行级精准零误报；PR-Agent slash commands（/describe /review /improve）**（RockB + CSDN + Qodo）→ 判据：**AI 注释要可识别且规则要硬**——"AI 注释混入人类"=怀疑失配；"PR 模板标注+审 Fix commits"=怀疑恰当；硬规则约束 LLM=降 token 升精度。
- **提升层**：工具/工作流（代码审查 Agent 组织化）。

## 对抗式测试生成与变异驱动：双 agent 对抗、反馈定向、变异分真相（来源：AdverTest + TATG + LLMutantKiller + TestSuiteBench + mutagen-ai 2026 实拉，r637B 落地，与 §微调评估分工——那边管"模型训练评估"，本条管"用对抗/变异验证测试与代码"）
- **对抗双 agent**：**AdverTest：测试生成 agent（T）与突变生成 agent（M）配对——M 持续创建突变'hack' T 当前套件的盲点，T 迭代精修测试'kill'挑战性突变，交互由覆盖与突变分数引导；TATG（Tracking-Aware Testing Objective）超 KTester/PANTA：行覆盖+22.15/分支+20.14/变异分数+37.66 个百分点，50 focal methods 达专有工业工具可比**（arXiv 2602.08146 + arXiv 2607.03194）→ 判据：**测试强度靠对抗**——"单 agent 生成"=盲点固定；"测试-突变双 agent 对抗"=盲点被 hack 后补；覆盖率数字背后=变异分才是强度真相。
- **反馈定向修复**：**LLMutantKiller：feedback-directed——测试没 kill 给定 mutant 则 LLM 重提示指定次数（每次带场景特定反馈：语法错误/依赖违规/执行日志）；mutagen-ai：摄入仓库→找欠覆盖函数→LLM 生成 pytest→只保留真 kill mutants 的测试**（Frank Tip + PyPI）→ 判据：**重试带反馈不带空转**——"重试同 prompt"=同错再现；"kill 失败→场景反馈重提示"=定向修正；只留 kill 突变体的测试=套件不掺水。
- **变异分真相与盲区**：**TestSuiteBench：前端 coding agent 从 spec 生成测试套件变异分<60%（最好 56%，四/六 agent <40%）——测试有效但弱（88% 通过参考实现仍弱）；每个 mutant 从单需求生成+隔离行为（73% 被恰好一个参考测试 kill，平均仅 0.2% 剩余测试 kill）；evals 盲区：passing eval 只是测试通过的证据，mutation testing 问'规则被破坏时测试会失败吗'，surviving mutant=保护的规则坏了测试没发现**（arXiv 2610.13065 + DEV）→ 判据：**通过率≠强度**——"88% 测试通过"=有效但弱；"surviving mutant"=规则保护失效；强测试=从 spec 每需求生成+变异验证。
- **提升层**：模型/工作流（对抗式测试生成与变异驱动）。

## 测试维护与修复 Agent：首次尝试预算、自愈扩展、失效分类（来源：TUM flaky + arXiv 2605.01471 + Polito flakiness + Breaking/Stale/Missing + NIO 2026 实拉，r637B 落地）
- **首次尝试与预算**：**TUM flaky 修复对比：第一次修复尝试最关键（占多数成功修复），agent 性能后续迭代快速下降——三次尝试预算足够抓可操作修复避免浪费资源；Claude Code 比 Gemini CLI 快 40%+（更可扩展）**（TUM）→ 判据：**修复预算设上限**——"无限重试"=资源浪费+性能衰减；"3 次尝试预算"=覆盖主要成功区；首次质量>次数。
- **自愈多 agent 与失效分类**：**多 agent 自愈（LangGraph+Playwright+RAG）：从人指导→高自主特征发现执行——无显式目标发现 100+ 可测特征（10 UI 屏）+运行时 DOM 分析动态扩展 15-30 特征+迭代修复失败测试无人工干预；Breaking/Stale/Missing 基准：七配置三框架（Claude Code/Codex CLI/OpenCode）六模型收敛 identification F1 45.7-49.4%——共同天花板；Test-Stale 最难（F1~36%，依赖执行失败信号缺主动检测）**（arXiv 2605.01471 + arXiv 2605.06125）→ 判据：**失效分类定修复策略**——"全当 broken 修"=stale 误诊；"breaking/stale/missing 三类"=各配策略；主动检测 stale（无执行失败信号）=天花板突破点。
- **flaky 与状态污染**：**Agentic flakiness 检测修复率 79.9-90.4%（三模型），多数修复不影响套件其他部分，回归检查约 1/10 破坏另一测试；NIO（non-idempotent-outcome）三阶段：检测（隔离环境重跑记录状态+自定义 JUnit listener 检测多次运行 stacktrace 变化揭示状态污染）→探索→修复；Mobile GUI 修复单次交互 73.8%/多次 91.8% 超 Healenium-Appium 50.8%/68.8%**（Polito + Marinov + 论文）→ 判据：**修复后必做回归检查**——"修好一个"=可能破坏另一个（1/10）；"修复+回归检查"=不引入新坏；stacktrace 变化=状态污染的指纹。
- **提升层**：模型/工作流（测试维护与修复 Agent）。

## Agent 红队框架与自适应攻击：闭循环收敛、角色分离、自改进对抗（来源：SkillAttack + Cart + GPT-Red + UDora + Adaptive Adversaries + SLIP 2026 实拉，r637C 落地，与 §Agent 工具面安全分工——那边管"工具面四个具体威胁"，本条管"红队流程框架与自适应攻击方法"）
- **闭循环收敛与角色分离**：**SkillAttack：动态验证 skill 漏洞可利用性——vulnerability analysis+surface-parallel attack generation+feedback-driven exploit refinement 闭循环搜索渐进收敛到成功利用（10 LLM/71 对抗+100 真实技能 ASR 0.73 超全基线）；Cart（Closed-Loop Adaptive）：每次结果指导下一步测什么——先广风险覆盖→跟随弱点→保持 probe 多样→记录证据与来源；分离 Challenger（创建测试）/Target（文本模型或有界工具 agent）/Judge（评估结果）角色可独立研究**（arXiv 2604.04989 + arXiv 2609.27336）→ 判据：**红队是闭循环搜索不是一次性清单**——"固定测试集"=漏后续弱点；"结果反馈+弱点跟随+证据留痕"=渐进收敛；角色分离=测试质量/目标鲁棒/评估标准各自归因。
- **自适应与自改进**：**Adaptive Adversaries：自主 LLM 攻击者观察 defender 响应跨轮 pivot——只评第一攻击轮 ASR 0-1%，允许 15 轮自适应攻击显著提升：单轮评估严重低估自适应攻击；GPT-Red（OpenAI）：self-play RL——GPT-Red 与多样化 defender 集合同时训练，攻击者奖励成功诱导失败、defender 奖励抵抗+完成原任务——defenders 更鲁棒则攻击被迫发现更强攻击**（arXiv 2607.18063 + OpenAI）→ 判据：**防御要按自适应攻击测**——"静态测试"=低估真实威胁；"多轮自适应"=贴近真实攻击者；攻防同时进化=鲁棒性评估免过时。
- **推理劫持与自越狱**：**UDora：生成模型推理 trace→自动识别最优插入点→插定向扰动→扰动推理作 surrogate 优化→迭代诱导恶意行为/调用恶意工具；SLIP（UIUC）：对齐 LLM 可自己越狱自己——只用目标模型自身输出走多轮对话到有害目标（黑盒，11 LLM 平均 94.7% AdvBench ASR）——不需要第二个 attacker LLM**（arXiv 2503.01908 + DREAM Lab）→ 判据：**推理链是攻击面**——"只看输入输出"=漏推理层操纵；"trace 插入扰动"=规划被劫持；自我越狱=防御不能假设 attacker 外部。
- **提升层**：模型/工作流（Agent 红队框架与自适应攻击）。

## 注入攻击面与检测防御：五模式、蜜罐工具、堆叠防御（来源：Respan + arXiv 2604.18248 + WebMCP + ATR + MLflow + LLM-Hacking 2026 实拉，r637C 落地，与 §提示架构注入防御分工——那边管"结构性防御（Dual-LLM/XML 标签）"，本条管"攻击面枚举+检测方法+工具化"）
- **五攻击模式覆盖 90%**：**system-prompt extraction/instruction override/role hijacking/exfiltration via tool calls/indirect injection via retrieved content；三层检测：input filter（regex+classifier）+output filter（查泄露秘密或拒了却完成的任务）+dual-LLM watcher（独立模型筛输入输出）；每个 detector 有 FP 率**（Respan）→ 判据：**检测分层叠**——"单层 regex"=漏语义变体；"输入+输出+watcher 三层"=互补；FP 率已知=阈值可调。
- **蜜罐工具 100% 精度**：**agent 框架暴露工具定义列表——加 canary 工具（get_admin_access/dump_database/reveal_system_prompt/disable_safety_filters）无合法调用路径；观察到任何调用=100% 精度确认间接注入事件；ATR 工具响应规则：regex 检测 tool_response 字段身份/角色重指派 payload（you are now/new instructions/your real purpose）；WebMCP 中会话工具注入：恶意网页调用 registerTool() 注册工具 agent 可调用**（arXiv 2604.18248 + agentthreatrule + Evvo）→ 判据：**蜜罐把攻击变可观测**——"被动等告警"=误报难判；"canary 工具零合法路径+调用即确认"=100% 精度；工具响应层要单独扫。
- **检测器逃逸与堆叠防御**：**activation-based detectors 被 adversarial suffix 逃逸（GCG 搜索通用 suffix 骗过逐层 probe 同时保持注入有效）；MLflow 防御=least-privilege tool scoping+结构化 prompts 带 per-request nonces+确定性输入/输出过滤器+高风险动作人工审批——核心失败模式不是缺 classifier；堆叠廉价确定性层+昂贵概率层**（LLM-Hacking + MLflow）→ 判据：**检测器会被绕**——"单点检测"=逃逸即全破；"确定性层（nonces/过滤器/审批）堆叠+概率层"=纵深；nonce 每请求=重放注入失效。
- **提升层**：模型/工具（注入攻击面与检测防御）。

## 多模态对抗攻击：最窄最不设防通道、并发注入、联合优化（来源：arXiv 2609.09404 + AdvWave + AudioAgentSecurity + JAMA + NeuralStack 2026 实拉，r637C 落地，与 §语音安全合规分工——那边管"语音 agent 转录注入面"，本条管"多模态攻击通道的系统性评估"）
- **音频是最窄但最不设防通道**：**多模态注入实验扩展到音频（前沿模型唯一接受的其他原始感知通道）：五模型仅两摄入音频/六框架仅三传递，但信号到达处攻击在 49% cells 完成（一模型 75%）——仅报完成率低估暴露，感知通道更窄但防御少得多；AdvWave：~30 查询对 GPT-4o speech-to-speech API 越狱；universal acoustic attacks=固定/条件触发段（Whisper 演示后）**（arXiv 2609.09404 + NeuralStack）→ 判据：**通道防御按传递率配**——"通道窄=少防御"=危险错觉；"信号到达 49% 完成率"=暴露与传递率相乘；音频通道越小越要补防御。
- **并发注入与不可闻命令**：**audio piggyback：instruction augmentation+scenario concealment 让恶意音频指令不可察觉'piggyback'到用户语音劫持 agent——AudioAgentSecurity 首个音频指令注入基准（8 真实场景）；超声（>20kHz）/次声（<20Hz）编码不可闻指令；叙事与构成框架：不每个音频攻击都需要不可感知噪声**（arXiv 2607.28165 + Ayi）→ 判据：**音频注入可与合法语音并发**——"单条音频分析"=漏 piggyback；"指令增强+场景隐藏"=并发劫持；不可闻≠不可注入。
- **联合优化跨模态**：**JAMA（Joint Audio-Text Multimodal Attacks）：同时扰动文本+音频输入绕过安全对齐——文本 GCG 离散后缀+音频 PGD 连续扰动联合优化推模型隐藏态跨安全边界**（Promptfoo LM Security DB）→ 判据：**跨模态联合攻击绕过单模态防御**——"只护文本"=音频通道借道；"文本 GCG+音频 PGD 联合"=单模态防线失效；防御须多模态同步。
- **提升层**：模型/工具（多模态对抗攻击）。

## 模型路由范式与级联：单决策 vs 顺序升级、偏好二元优化、质量估计器（来源：RouteLLM + FrugalGPT + Dynamic Model Routing Survey + Cascade Routing 2026 实拉，r638A 落地，与 §推理引擎选型分工——那边管"选哪个引擎跑"，本条管"请求怎么分给多个模型"）
- **Routing 与 Cascading 是两种不同范式**：**routing 单决策把 query 映射到模型池中一个模型——快但误分类直接错答；cascading 顺序运行：先小快模型，质量估计不足才升级大模型——安全但升级双付+延迟**（arXiv 2603.04445 + UsageBox）→ 判据：**高频可识别流量用 routing，错不起的任务用 cascading**——"一次分类定死"=便宜但误分类错答；"小模型先跑+verifier 升级"=质量兜底但双付。
- **RouteLLM：路由是 human preference 二元优化，不是难度预测**：**LMSYS 把路由重构成"强贵模型 vs 弱廉模型选哪个"的人类偏好学习；四种 router：MF（preference pairs+OpenAI Embedding API）/BERT（分类标签无外部依赖）/SW-Ranking（无训练+Embedding API）/Causal LM（preference pairs+GPU）；成本减少 >2 倍不牺牲质量**（arXiv 2406.18665 + pi-smart-router）→ 判据：**路由判据是偏好不是难度**——"预测 prompt 抽象难度"=不可学；"人在强/弱模型间的偏好"=可监督；数据增强提升性能。
- **Cascade 的质量估计器是成败关键**：**FrugalGPT：~80% 真实查询简单到小模型够——只有剩余难查询需要贵模型；cascade 的"looks unreliable"必须便宜可查（confidence score/schema validation failure/长度/格式检查）；Cascade Routing 统一框架证明 routing+cascading 最优性——质量估计器=模型选择范式成功的临界因素**（jonathanding + aiwisdom + arXiv 2410.10347）→ 判据：**升级判据要便宜**——"人工审查质量"=贵过升级本身；"confidence/schema/长度/格式"=自动可查；估计器好则 cascade 胜单独方法。
- **提升层**：模型/工作流（模型路由范式与级联）。

## LLM 网关选型与路由模式：托管 vs 自托管、六路由模式、model-neutral（来源：OpenRouter + LiteLLM + Portkey + NeMo Switchyard + Zylos + agentgateway 2026 实拉，r638A 落地，与 §重试分两类分工——那边管"重试怎么管"，本条管"网关这一层选什么形态"）
- **选型判据=自托管需求**：**无自托管需求→OpenRouter（广度/易用/SOC 2/GDPR/zero-data-retention 路由；买 credits 加 5.5% fee；provider 对象过滤 price/throughput/latency/data policy/ZDR/quantization）；自托管→LiteLLM（140+ providers/MCP servers/agents 单一 OpenAI 兼容 API+成本追踪+budgets；零 per-token fee；LiteLLM Rust p99 0.66ms/2800+ req/s vs Portkey 2.29ms）**（OpenRouter + litellm.ai）→ 判据：**数据主权/费率决定托管还是自托管**——"要合规与零保留"=托管；"要基础设施控制+零平台费"=自托管；延迟基准（p99）是硬指标。
- **六路由模式与虚拟模型**：**LiteLLM：weighted pick/latency-based/rate-limit-aware/least-busy/lowest-cost/custom（写 Python）——fallback 列表让 proxy 失败时试下一个模型；agentgateway 虚拟模型：weighted/conditional/failover 路由；AI Gateway pattern=共享模块把"which model"与"what to do"解耦——运行时改模型不改代码**（openrouter-vs-litellm + aaif + Zylos）→ 判据：**路由策略按目标选**——"均衡/延迟/限流/最省/自定义"=六模式各司其职；"虚拟模型"=策略配置化；which-what 解耦=模型变更不动业务逻辑。
- **Model-neutral 与工具治理**：**NeMo Switchyard：开源编排层把路由逻辑与 provider endpoints 分离——model-neutral 路由；tuning-free routers（LLM classifier/stage/escalation）+tunable prefill routers（从 workload 学预测成功可能性）；agent 网关把 MCP tool calls 与模型调用同层路由过滤（Agent tool governance）**（NVIDIA + Maxim）→ 判据：**路由逻辑与端点解耦**——"路由写死在 endpoints"=换模型重写；"model-neutral"=策略独立；工具调用同层治理=一个控制面管全请求。
- **提升层**：工具/工作流（LLM 网关选型与路由模式）。

## 语义缓存与成本杠杆：命中率经济学、阈值平衡、缓存对象选择（来源：SemaCache + TrueFoundry + devops.gheware + 阿里云 AI 缓存 2026 实拉，r638A 落地，与 §上下文预算管理分工——那边管"窗口内 token 预算"，本条管"跨请求的响应缓存"）
- **语义缓存定义与经济**：**请求侧缓存层：embedding 入 prompt→查已存 prompt 向量→余弦相似度超阈值返回缓存响应——扩展 exact-match 服务 paraphrase 查询；价值由命中率统治：30% hit=30% 请求跳模型=成本近 30% 降（减 embedding+lookup 成本）；成本削减 up to 80%**（FutureAGI + TrueFoundry + SemaCache）→ 判据：**先算命中率再上语义缓存**——"hit rate 低"=embedding/lookup 成本倒挂；"hit rate 高"=主杠杆；相似度命中=跳模型。
- **阈值与缓存对象**：**向量相似度阈值 0.85-0.92 最佳平衡保真与命中率；缓存动态 prompt 收益可忽略——聚焦结构化查询 embedding+system prompt 组合；网关层或 sidecar 集成在请求到模型前防冗余 token；阿里云 AI cache 命中时 input+output tokens 0 零推理资源**（gheware + Maxim + 阿里云）→ 判据：**缓存对象选稳定的**——"动态 prompt"=命中率崩塌；"结构化查询+system prompt 组合"=可命中；命中=完全零推理消耗。
- **提升层**：工具/工作流（语义缓存与成本杠杆）。

## Agent 成本结构与预算强制：工具调用×重放、三层预算、两阶段对账（来源：MasterPrompting + AIPromptsHub + Imversion + llm_budget + AgentBudget + agustin-otegui 2026 实拉，r638B 落地，与 §成本四层分工——那边管"输入侧注入/输出侧量体裁衣"，本条管"agent 系统级预算与强制机制"）
- **真实成本=工具调用×重放**：**多 agent 系统真实成本不是每次模型费——是每次工具调用都是 LLM 调用；典型 agent loop 账单 5-15× input tokens、8-25× output tokens vs 单次直接回答——对话历史随每次工具调用结果增长，每个工具结果下轮重放为输入；大多团队低估 agent 成本**（MasterPrompting + AIPromptsHub）→ 判据：**agent 成本按循环计不按调用计**——"只看单次模型费"=低估一个数量级；"工具调用×历史重放"=真实账单；轮数下降=成本平方级下降。
- **分层预算与降级执行**：**三层预算强制（task/session/daily）降月 LLM 花费 70% 零 runaway；分层限制：token budget+model-call limits+tool-call limits+retry budgets+dollar caps+downgrade rules+graceful termination（剩余预算无法安全完成任务时）；85% 日预算→降级执行模式（高成本推理模型换低成本参数高效模型）；100%→暂停到管理员批准紧急 token 分配或窗口重置；llm_budget：调用前拒绝（per-agent 美元上限内置 232 模型价）**（dailyaiworld + Imversion + llm_budget）→ 判据：**预算分层不单 cap**——"单 cap"=loop 烧完才发现；"token+调用次数+重试+美元多层+downgrade+优雅终止"=loop 打不穿；执行前拒绝=跑飞前停。
- **两阶段强制与对账**：**AgentBudget：per-session budget envelope 包裹 LLM 调用+工具调用+外部 API 请求（running cost ledger+自动 circuit breaking）；SDK monkey-patching 零代码改；两阶段强制=pre-call 估计+post-call 对账；loop detection+嵌套预算（多 agent）+结构化成本报告；Redis 原子操作 100K+ 并发预算递增无竞态；'Opus plans, Haiku executes'——planner 贵模型+executor 便宜模型的 orchestrator-worker 成本栈**（agentbudget + AgentConn）→ 判据：**预算要包住全部调用面**——"只包 LLM"=工具/外部 API 漏账；"pre-call 估计+post-call 对账"=防超卖；planner-executor 分档=质量不损省钱。
- **提升层**：工具/工作流（Agent 成本结构与预算强制）。

## 并发与投机执行降延迟：并行工具调用、工具-LLM 联合调度、并发控制（来源：W&D + PASTE + CONCUR/PACE + AI/TLDR + DEV 2026 实拉，r638B 落地，与 §多 Agent 协作纪律分工——那边管"agent 怎么拆与协作"，本条管"同一 agent 内工具/生成怎么并行"）
- **并行工具调用与批量**：**Parallel tool calls：同轮请求多工具运行时同时跑；W&D：3 tools/turn 最佳性能超单工具——并行显著降轮数→降 wall-clock 与 LLM API 成本；独立任务并行=最大值不是和（12s+10s 串行 22s 并行 12s）——DAG 依赖满足即跑**（arXiv 2602.07359 + DEV）→ 判据：**独立工具调用并行化**——"一次一个工具"=轮数×延迟；"同轮多工具"=3/turn 最佳；并行成本=max 不是 sum。
- **投机工具执行**：**PASTE：从循环 agent 模式预测具体未来工具调用并在 LLM 生成时投机执行；投机结果隔离到 LLM 确认（不污染状态）；联合调度工具执行与返回 LLM 会话避免瓶颈转移 GPU——任务完成时间 -43.5% 工具延迟 1.8×**（arXiv 2603.18897）→ 判据：**投机执行要隔离**——"执行了没确认"=状态污染；"隔离到 LLM 确认"=安全投机；联合调度=瓶颈不转移。
- **并发控制防 thrashing**：**CONCUR/PACE：congestion-control 启发 admission control 用 KV cache feedback 调节 agent 并发——agentic batch inference middle-phase thrashing 4.09× 吞吐提升**（OpenReview U7c6glPdDW）→ 判据：**并发不是越大越好**——"全开并发"=middle-phase thrashing；"KV cache 反馈准入控制"=吞吐最优；拥塞控制启发=自适应限流。
- **提升层**：模型/工具（并发与投机执行降延迟）。

## 延迟感知 UX 五模式：Streaming 最重要、skeleton 占位、增量披露（来源：Brainy + AYDesign + AI/TLDR + Laioutr + arXiv 2609.35692 2026 实拉，r638B 落地，与 §进度流与诊断流分开分工——那边管"播报形态"，本条管"延迟感知的界面模式"）
- **五模式组合**：**Streaming text/Optimistic UI/Progressive disclosure/Reasoning surfaces/Background agents——每个赢在感知速度的产品至少 3 个，优秀全 5 个；组合：Streaming 给用户读的东西+Optimistic UI 给看的+增量披露给结构**（Brainy）→ 判据：**感知速度是设计不是算力**——"等完整响应"=白屏；"五模式组合"=感知快；至少 3 个=底线。
- **Streaming 是核心 UX 决策**：**模型同/prompt 同/tokens/s 同，但感知速度/信任/愿读围绕 tokens 如何落地 UI——流式做对慢模型显快，做错快模型显坏；三工具：streaming 逐字显示+skeleton（首 token 路上按预期答案形状占位）+stop button（取消不再想要的生成）——7 秒白屏转感知快；agent-driven late-arriving slots 用 skeleton 不阻塞页面**（AYDesign + AI/TLDR + Laioutr）→ 判据：**UI 先给占位再给内容**——"首 token 前空白"=最差体验；"skeleton+streaming+stop"=容忍长生成；晚到内容=骨架承载。
- **Progressive disclosure 增量加载**：**技能渐进披露：frontmatter（name+brief description）初始上下文+按需增量加载完整定义 vs 全量加载——降 token 用量+提可靠性与技能检索质量，代价=更大延迟**（arXiv 2609.35692）→ 判据：**披露与延迟权衡**——"全量加载"=token 高但快；"frontmatter+增量"=省 token 提可靠但慢；按需披露=长上下文 agent 的标准。
- **提升层**：工作流/可复用 Skill（延迟感知 UX 五模式）。

## 编排平台选型判据：n8n/Dify/Langflow/Activepieces/扣子/百炼/千帆（来源：RECATOOLS + n8n vs + Sliplane + scored.tools + InfoQ + 扣子文档 2026 实拉，r638C 落地，与 §轻量自动化三模式分工——那边管"自动化用什么形态搭"，本条管"多平台对比下选哪个平台"）
- **n8n vs Dify 核心判据**：**n8n=AI 主动参与运营（连 CRM/ERP/复杂后端逻辑，AI 跨系统行动）；Dify=专门 AI 应用用户交互优先（复杂 RAG 知识库/hosted chat）；Dify 最有主见 all-in-one（agent 编排+RAG+prompt 管理+observability 一体——少接线多调行为；workflow editor 分支循环干净；多 trigger：schedule/webhook/plugin；workflow-to-webapp）**（n8n.io/vs + scored.tools）→ 判据：**先问"AI 在系统里扮演什么"**——"跨系统行动"选 n8n；"用户交互/RAG 应用"选 Dify；"少接线多调行为"选 all-in-one。
- **MIT 白标 vs 复杂编排**：**Activepieces=真 MIT 可 fork/修改/白标/嵌入自己 SaaS（非技术操作者高度引导线性 step-by-step UI；简单管线；flat-rate 无限任务）；n8n=复杂数据转换/多路径分支/技术用户；Langflow=视觉原型导出真实 Python（source code 访问自定义组件）；Flowise 已 EOL（2026-08-31 归档）**（n8n.io/vs/activepieces + scored.tools）→ 判据：**按操作者与复杂度选**——"非技术+白标+简单管线"选 Activepieces；"复杂转换+多分支"选 n8n；"原型转代码"选 Langflow。
- **国内平台决策清单**：**快速验证/零代码→Coze（插件多上手快几天跑通）；私有化+技术能力→Dify；阿里云/钉钉深度→百炼（全家桶+算力弹性）；知识密集/国企政务→百度千帆（中文理解强）；扣子 3.0=多人多 Agent 协作（一人+多 Agent/@全员）+内置长期记忆/日程/邮箱/云电脑；企业级适配：等保三级+信创+私有化**（InfoQ + 扣子文档）→ 判据：**按企业类型选**——"技术团队数据主权"→Dify；"非技术快速验证"→Coze；"云上生态"→百炼；"政务知识密集"→千帆。
- **提升层**：工具/工作流（编排平台选型判据）。

## 编排拓扑与模式选型：DAG-Plan-Execute、事件驱动、swarm-pipeline-graph、状态机（来源：arXiv 2606.20058 + Zylos + DEV + Stanford CS224G + Mastra 2026 实拉，r638C 落地，与 §多 Agent 协作纪律分工——那边管"agent 拆后怎么协作"，本条管"工作流编排选哪种拓扑"）
- **DAG Plan-Execute-Replanner**：**Planner 生成执行图 upfront+Executor 派发+Replanner 计划变化适配——分离规划执行，并行 agent 调用+系统失败恢复；agent discovery 两阶段（Anthropic Skills 启发）**（arXiv 2606.20058）→ 判据：**规划与执行分离**——"upfront 图+replanner"=可并行+可恢复；规划执行耦合=改计划全重来。
- **事件驱动 vs 拓扑匹配**：**事件驱动：agents 反应式消费者——无中央调度 push 工作，订阅事件流反应相关事件；每 agent 动作产事件、每事件可触发更多动作——workflow 从事件拓扑涌现非 upfront 声明；swarm vs pipeline vs graph：拓扑不统一 per workflow 匹配（真独立并行/顺序路由非独立）——SAP 平均解决时间 38→10 分钟；DAG=数据管线/CI 标准；State Machine（Nodes 修改共享 state+Edges 条件转换——ReAct/Chaining/Routing/Parallelization/Orchestrator-Workers）**（Zylos + DEV + Mastra + Stanford）→ 判据：**拓扑按任务结构选**——"声明式确定流"用 DAG；"响应式松耦合"用事件驱动；"显式状态转换"用状态机；拓扑不匹配=6 个月返工。
- **Router→Specialist 与 workflow vs agent 边界**：**轻量 router LLM 分类意图派发专用 sub-graph（每 specialist 窄域专用工具 prompt）；确定性 workflow=rule-based 固定输入低异常率；agent 只在需要动态规划/非结构化数据解释/上下文敏感工具选择时用**（neelmishra + Olostep）→ 判据：**能 workflow 不 agent**——"规则明确"走确定性流程；"动态规划+非结构化"才上 agent；router-specialist=意图分发的标准省法。
- **提升层**：模型/工作流（编排拓扑与模式选型）。

## 视觉平台 vs 代码框架边界：执行层在代码、视觉层嵌入、决策树（来源：WorkflowBuilder + AI Agents Guide + EmergingTechDaily + Kaxo + Olostep 2026 实拉，r638C 落地，与 §编排拓扑分工——那边管"选哪种拓扑"，本条管"平台还是代码框架"）
- **新标准架构**：**执行层在代码（LangGraph/CrewAI/自定义 Python/Node——repo 版本控制、测试、可部署；管 agent 编排/状态/错误/重试）+视觉层=嵌入式组件——AI 产品标准模式**（WorkflowBuilder）→ 判据：**执行代码化+视觉嵌入**——"全部依赖平台"=编排逻辑不可版本控制；"执行在 repo+视觉嵌入式"=可测试可部署。
- **视觉工具赢的场景**：**已知 trigger+bounded LLM step+几个 app actions（n8n/Zapier/Make 类）——不是 deep multi-agent control plane**（AI Agents Guide）→ 判据：**按控制面深度选**——"已知触发+有界步骤+预建连接器"用视觉工具；"深度多 agent 控制面"用代码框架。
- **决策树与 build-vs-buy**：**显式有状态工作流控制优先→LangGraph；OpenAI tools/handoffs/guardrails 中心→OpenAI Agents SDK；Microsoft 生态→MS Agent Framework；可 hybrid（视觉平台+代码）；build vs buy：Code Framework 复杂多 agent 高 upfront 低 scale 成本/No-Code 单 agent 低 upfront 可变 scale/Claude Code Agents 中复杂 ops-heavy 低 upfront 低 scale**（EmergingTechDaily + Kaxo）→ 判据：**按状态/工具/生态三维走决策树**——"显式状态"→LangGraph；"OpenAI 工具"→Agents SDK；"MS 生态"→Agent Framework；hybrid=常态。
- **提升层**：工作流/可复用 Skill（视觉平台 vs 代码框架边界）。

## 评估驱动开发与回归套件：EDD、scorers-runner-CI gate、属性阈值（来源：HelpMeTest + MetaCTO + Confident AI + BuildPulse + Chirag + FutureAGI 2026 实拉，r639A 落地，与 §评测信封分工——那边管"交付评测方法"，本条管"LLM 应用开发用评估驱动+CI 门"）
- **EDD=TDD 纪律应用到 LLM**：**先写 evals 定义"good"再建功能——failing evals 是你的 spec；结构=开发工作流+red-teaming+回归检测**（HelpMeTest）→ 判据：**评估先行**——"功能未建先写 eval"=规范驱动；"建完再测"=vibes-based QA。
- **回归套件三件套**：**scorers（确定性/LLM-as-judge/human 打分器）+runner（数据集过 SUT 出评分报告）+CI/CD gate（分数回归超阈值拦 PR）；非确定性输出→断言属性+eval 分数超阈值而非精确字符串**（MetaCTO + FutureAGI）→ 判据：**回归测属性不测字符串**——"精确字符串断言"=非确定性输出必 flaky；"属性+分数阈值"=稳定可拦。
- **CI pipeline 形状**：**每个候选变更：CI job 跑 golden dataset→validated metrics 评分→verdicts 对比 baseline→非协商 case 失败或 pass rate 超容差→fail check→results attach PR 作 test comment；model swap 失败用 fixed golden dataset 断言 known-good bar 捕获（模型/提示/代码变更不能静默降质量）**（Confident AI + BuildPulse + FutureAGI）→ 判据：**回归在 CI 不在记忆**——"分数降即拦 PR"=防静默回归；"baseline 对比+非协商 case"=有锚点；model swap 必过 golden set。
- **提升层**：工作流/可复用 Skill（评估驱动开发与回归套件）。

## LLM-as-Judge 校准与可靠性：更强 judge、kappa、gold set、disagreement 检查（来源：MLflow + AIWorkflowLab + opsagent + HysenLabs + GitHub AI Evals Notes 2026 实拉，r639A 落地，与 §评测信封分工——那边管"交付评测信封"，本条管"judge 本身怎么校准到可信"）
- **judge 选型与避免自评**：**judge 用比被测更强的模型且非同一模型（deepseek-v4-pro with thinking on 评 deepseek-flash）——avoid 'grading your own work'**（HysenLabs）→ 判据：**judge≠被测模型**——"同模型自评"=系统性偏袒；"更强+thinking on"=独立裁决。
- **校准三条件与 kappa**：**①gold set 验证 ②机会校正统计（Cohen's kappa）度量一致 ③部署后持续监控——skip validation=shipping black box；well-calibrated frontier judge 与专家人类 80-85% 一致≈两独立人类间一致率；kappa 0.6+ 最低门槛，用自己任务测不靠 vendor benchmarks**（MLflow + AIWorkflowLab）→ 判据：**kappa 自己测**——"0.6+ on your task"=可信底线；"vendor benchmark"=别人的分布不算数；三条件缺一=盲盒打分。
- **校准流程与 disagreement 检查**：**100-200 代表案例人类按 judge 同一 rubric 打分（含 close calls）→judge 以生产同配置跑→量 kappa→检查每个 disagreement 定位偏差（positional/verbosity/self-preference 等）；judge prompt 结构：clear task description+evaluation criteria+success/failure 精确定义+diverse few-shot 含边界（words 难说清但模型重要的）+structured output**（opsagent + GitHub Notes）→ 判据：**校准即测量仪器**——"100-200 案例+同 rubric"=judge 与人类同标尺；"逐个 disagreement"=偏差可定位；few-shot 边界=words 说不清的案例由示例承载。
- **提升层**：模型/工作流（LLM-as-Judge 校准与可靠性）。

## 评估集构建与黄金数据集设计：分桶、四源、期望输出 rubric（来源：FutureAGI + flytebit + Google ADK + OpenRouter + kunalganglani 2026 实拉，r639A 落地，与 §记忆验证分工——那边管"记忆读没读对"，本条管"评估集本身怎么建"）
- **golden set 分桶设计**：**Production sample（分层 trace 导出 60%——系统处理实际流量）+Adversarial（jailbreak 语料/扫描器/红队 15%——压力下扛住）+边界/回归基线等余桶；agent golden test set 四源：生产失败（failure memory pipeline）+生产成功（回归基线）+adversarial edge cases+coverage gaps（该走未走过的路径）；versioned 评估集**（FutureAGI + flytebit）→ 判据：**分桶证明面**——"生产样本管常态+对抗管攻击+gap 管覆盖"=各桶证明不同事；"versioned"=可回滚可比对。
- **期望输出两形态**：**每输入合格者写期望输出——单字符串或 rubric（binary criteria 每标准 MET/UNMET 或 analytic rubric 逐标准打分）——rubric 让打分一致**（OpenRouter）→ 判据：**期望先于评分**——"rubric 写清必须含/必须不声称/语气格式"=打分有标尺；"binary/analytic 二选一"=一致优先。
- **Golden Dataset 与 persona**：**ADK Golden Dataset=agent 正确执行的快照（捕获完美交互非 Q&A 对列表）；persona-based testing：5-7 用户画像不同沟通风格跑系统**（Google + kunalganglani）→ 判据：**快照真实交互**——"完美执行快照"=ground truth 是行为不是问答；"5-7 persona"=覆盖沟通风格差异。
- **提升层**：工作流/可复用 Skill（评估集构建与黄金数据集设计）。

## 分层规划与任务分解：agent 树、plan-execute RL、组件库复用、事件重规划（来源：ReAcTree + HiPER + GraphThink + HCL-GP + CoMuRoS 2026 实拉，r639B 落地，与 §编排拓扑与模式选型分工——那边管"工作流拓扑选型"，本条管"agent 内部规划怎么分层分解"）
- **分层 agent 树**：**ReAcTree：复杂目标分解为可管理子目标在动态构建 agent 树内；每子目标由能推理/行动/继续扩树的 LLM agent node 处理；control flow nodes 协调执行策略；每 agent node 检索 goal-specific subgoal-level 示例（episodic 记忆）**（AAMAS 2026）→ 判据：**树形分层+控制流**——"agent 树动态扩"=子目标粒度自适应；"控制流节点协调"=策略集中；"子目标级示例"=记忆按粒度检索。
- **规划执行分离与 credit**：**HiPER：高层 planner 提子目标+低层 executor 多动作步执行；hierarchical advantage estimation 在规划与执行两级赋 credit（对齐优化与结构）**（arXiv 2602.16165）→ 判据：**两级 credit**——"规划级+执行级分开归因"=优化对齐结构；"单级 credit"=哪层错分不清。
- **组件库与事件重规划**：**HCL-GP：从成功执行自动提取可复用组件→component library 组合策略生成（泛化跨任务实例）；CoMuRoS：中央 task-manager（静态规划规则+动态上下文任务历史/状态/事件）VLM 分类事件相关与否触发 replanning——从破坏事件恢复；GraphThink：task graph 结构化知识稳健规划+scene graph 环境记忆 event-driven replanning——减轻规划幻觉（GRPO 内 task graph 提供精细 reward）**（HCL-GP + CoMuRoS + GraphThink）→ 判据：**组件可复用+事件驱动**——"成功执行提组件"=规划越用越熟；"事件相关分类触发重规划"=只对真事件重规划；"图结构知识"=幻觉可减。
- **提升层**：模型/工作流（分层规划与任务分解）。

## 反思与自修正闭环：generate-critique-revise、早停 sentinel、发散收敛归因（来源：Taskade + EvoResearcher + Meta-Reflexion + ACL Self-Reflection + RLERR 2026 实拉，r639B 落地，与 §自修正分工——那边管"修后怎么验"，本条管"反思闭环本身怎么设计"）
- **反思三环**：**Reflection=generate→critique→revise 闭合环：生成→按具体标准判断→修→直到过或达限——分离产生与判断是抓错误的关键**（Taskade）→ 判据：**产生与判断分离**——"同一模型自评"=judge 与被 judge 同源；"按具体标准判断"=critique 有标尺；"过或达限"=有终止。
- **成本有界反思**：**EvoResearcher：training-free 迭代 generate→self-critique→revise 到最大深度 D 或 critique 返回 CONFIRMED sentinel（隐式早停）——严格受控计算预算下自验证**（arXiv 2608.18884）→ 判据：**预算有界**——"最大深度+CONFIRMED 早停"=自验证不失控；"无界反思"=成本无限。
- **认知惯性与安全反思**：**Meta-Reflexion：divergent-convergent 两阶段——Reflector 生成多样正交 fault-attribution 假设打破认知惯性；[Self-Reflection] marker（~50 token 语义 'Wait'）：检测有害生成早期信号立即产生 marker 启动 self-doubt→pause→reflection；RLERR：强化学习五原则分层奖励系统对齐 Effective Reflection（SCFT 初始化）**（Meta-Reflexion + ACL + RLERR）→ 判据：**反思要破惯性**——"多样正交归因"=不重蹈同一解释；"早期信号 marker"=有害生成未完成即截；"五原则奖励"=反思质量可训练。
- **提升层**：模型/工作流（反思与自修正闭环）。

## 推理时缩放与自适应预算：compute-optimal、两家族、effort 杠杆（来源：Snell + reinforcement-learning + Tenzed + TAB + Zylos + Gambit 2026 实拉，r639B 落地，与 §并发与投机执行降延迟分工——那边管"延迟工程"，本条管"推理时算力怎么分配"）
- **compute-optimal 缩放**：**最有效 compute 分配总是 prompt-dependent；difficulty-based 可 up to 4x 效率 vs 标准基线；小模型+正确测试时策略可 beat 14x 大模型 naive；两机制：dense process verifiers 搜索+策略适配难度（简单=迭代精修一解、难=广泛搜索）；两家族：parallel（best-of-N/self-consistency/verifier search）与 sequential（长 CoT 自纠回溯）**（Snell + RL KB）→ 判据：**按难度分配**——"简单精修难搜索"=预算花对地方；"dense verifier"=逐步验证；两家族按任务选。
- **自适应预算机制**：**TAB：多轮推理=顺序计算分配（multi-objective MDP，GRPO 学策略，reward=accuracy+全局 token 预算遵守凸组合）；HAB：coarse-to-fine——先预测粗推理深度类别映射 step-range 指令→intra-step 每步动态 token 预算（adaptive Pareto 平衡质量效率）；生产杠杆：effort 参数（o3/o4-mini）+thinking budget（Gemini Flash）无需模型级改动**（TAB + HAB + Zylos）→ 判据：**预算可配置**——"顺序分配+凸组合"=准确与预算可调；"coarse-to-fine"=先定深度再分步预算；"effort/thinking budget"=生产无需改模型。
- **thought-level beam search**：**Gambit：周期剪不前途轨迹+立即从高质量 prefix 分支——轻量 scorer 探测 hidden states 集中计算到最有希望轨迹+连续高硬件利用率；同硬件约束 +6.7% 绝对精度**（arXiv 2608.08020）→ 判据：**按轨迹质量聚焦**——"剪枝+高分前缀分支"=算力集中；"hidden states 轻量探测"=不打断高利用率。
- **提升层**：模型/工作流（推理时缩放与自适应预算）。

## 多 Agent 协作模式与框架选型：五模式、心智模型、图工程（来源：Agentbrisk + Microsoft Learn + Developers Digest + ReActNet + Ayi NEDJIMI 2026 实拉，r639C 落地，与 §多Agent协作纪律分工——那边管"拆了怎么协作"，本条管"协作拓扑模式+框架怎么选"）
- **五模式与适用**：**supervisor（中央编排者读目标决定调哪些子 agent 什么顺序，子 agent 返结果 supervisor 综合——多步任务清晰阶段）/swarm（对等 agent 动态 handoff 规则互传控制）/pipeline（线性流水线）/plan-and-execute/ReAct**（Agentbrisk）→ 判据：**模式匹配任务形状**——"多步清晰阶段"→supervisor；"对等动态"→swarm；"线性确定"→pipeline；先选模式再动手。
- **框架心智模型**：**四框架主导 Python 多 agent：Semantic Kernel（Microsoft Agent Framework）/LangGraph（LangChain 生态）/AutoGen（MSR）/CrewAI——各不同心智模型，选择影响语法+架构模式（hub-and-spoke 自然与否）；选型映射：LangGraph=显式可审计控制流+持久状态（需能 staff persistence）/CrewAI=role-task-crew 角色团队共享记忆快速原型（delegation 是 model-mediated）/AutoGen AG2=对话式协调/OpenAI Agents SDK=客户向 handoff 流/ADK=谷歌部署/Claude Code 原生子 agent**（Microsoft Learn + Developers Digest + Qualia）→ 判据：**按控制与心智选**——"要可审计状态"→LangGraph；"要快原型"→CrewAI；"要对话式"→AG2；**AutoGen 2025.10 进 maintenance 模式、MS Agent Framework 2026.4 1.0 GA——网上对比大多过时，别 start AutoGen（README maintenance banner）**。
- **推理时图工程**：**ReActNet：training-free——不优化静态拓扑，合成 task-conditioned temporal workflow graph 联合指定 agent 连接+edge 级通信语义；每 graph snapshot 一推理阶段**（arXiv 2609.05774）→ 判据：**图随任务变**——"静态拓扑"=任务形状固定；"temporal graph"=每推理阶段连接可不同。
- **提升层**：工作流/可复用 Skill（多 Agent 协作模式与框架选型）。

## Agent 记忆架构：OS 资源化与生物启发机制（来源：Aeon + Human-Inspired + mnemos + KeyMem + Agent Zero Memory 2026 实拉，r639C 落地，与 §记忆提取四策略分工——那边管"提取什么/怎么沉淀"，本条管"记忆系统本身怎么架构"）
- **记忆=托管 OS 资源**：**Aeon：Neuro-Symbolic Cognitive OS——记忆非静态存储而是托管资源：Memory Palace 空间索引（Atlas SIMD 加速 Page-Clustered Vector Index：小世界图导航+B+Tree 磁盘局部性最小读放大）+Trace（neuro-symbolic episodic graph）**（Aeon）→ 判据：**记忆按资源管**——"空间索引+磁盘局部性"=读放大可量化；"OS 资源化"=有生命周期有调度。
- **六认知机制**：**sleep-phase consolidation（睡眠整合）/interference-based forgetting（干扰遗忘）/engram maturation（记忆成熟）/retrieval 时 reconsolidation（重固化解 stale-fact）/entity knowledge graphs/hybrid multi-cue retrieval——每机制治 naive accumulation 一失败模式；mutable RAG=检索时重固化**（Human-Inspired + mnemos）→ 判据：**机制对失败模式**——"写时滤低信息（surprisal gate）"=垃圾不进；"检索时重固化"=旧事实更新；"干扰遗忘"=不无限堆。
- **平行记忆与双路检索**：**Agent Zero Memory：provenance-aware 三平行记忆——episodic Memory Events 时间线（when/what 一等公民）+entity-event knowledge graph（跨会话连人项目）+semantic curated citation-locked HDM（耐久事实）；KeyMem：原始对话轮存知识图+dual-path（关键词向量+图遍历）检索，Fragment-based multi-hop expansion 聚合主题相关记忆，source-aware scoring query-local 归一无需预设超参**（Agent Zero + KeyMem）→ 判据：**平行面各自服务**——"时间线管何时/图管关联/HDM 管耐久"=不同查询不同面；"双路+多跳"=复杂查询可聚合。
- **提升层**：模型/工作流（Agent 记忆架构）。

## 上下文工程与预算管理：六步法、compaction 触发、四杠杆（来源：Atlan + withtai + Mallary + Overcut + AnhTu 2026 实拉，r639C 落地，与 §上下文预算管理分工——那边管"用多少开始规划着压"，本条管"上下文工程整套实施步骤+杠杆"）
- **六步实施**：**①prompt 前定义 token budget ②分离 static/dynamic context ③按 agent 类型选技术 ④static 层 enable prompt caching ⑤dynamic 注入加 context routing 层 ⑥治理与可观测——每步建立在前一步，跳到技术选择未先立预算=建在未测量系统上**（Atlan）→ 判据：**预算先行**——"未立预算选技术"=测量缺失；"static caching+dynamic routing"=两层分治。
- **compaction 触发与四杠杆**：**窗口接近 70-80% 容量写结构化摘要（已完成工作/关键决策/触及文件路径/未完成任务）再重启；四杠杆：Retrieval 只拉当前步需文档事实/Compression 摘要旧 turns 工具输出长文档/Isolation 可并行或太吵任务拆独立上下文/Dynamic tool selection 不全加载工具**（withtai + Mallary）→ 判据：**四杠杆按需**——"只拉当前步"=不预加载；"摘要旧输出"=窗口保持 lean；"太吵就隔离"=独立上下文；"工具按需"=不塞满定义。
- **窗口是可见部分**：**context engineering=每步决定窗口有什么（指令/检索代码/工具定义/记忆/早前结果）；窗口只可见部分——依赖知识层（code graph/tickets/docs/团队约定）agent 运行时可工具查询**（Overcut）→ 判据：**窗口后要有层**——"可见窗口+可查询知识层"=小窗口也能干大活；"prompt engineering 管单 prompt/context engineering 管系统"=scope 分清。
- **提升层**：工作流/可复用 Skill（上下文工程与预算管理）。

## 结构化输出三层强制：API schema 约束、grammar 解码、输出契约（来源：OpenAI + Anthropic + Azure + kissapi + Outlines + guidance + n8n + Dify 2026 实拉，r640A 落地，与 §提示词当规格与四层输出校验分工——那边管"提示当规格+校验层"，本条管"生成侧三层强制机制"）
- **API 层 schema 约束**：**OpenAI response_format json_schema + strict:true 强制符合 schema（消除省略字段/加字段/畸形文本）；Anthropic output_config.format JSON outputs + strict tool use（strict:true 工具名+输入双校验，工具名正则 ^[a-zA-Z0-9_-]{1,64}$）；Azure key ordering：结构化输出遵循 schema 顺序——改输出顺序=改 schema 顺序；structured outputs 不支持并行函数调用；跨模型：网关保持 response_format/tools 载荷一致归一差异**（OpenAI + Anthropic + Azure + kissapi）→ 判据：**约束在 API 层**——"strict schema"=格式由服务端保证；"key ordering"=顺序由 schema 定；"网关归一"=换模型不动载荷。
- **grammar 解码层**：**Outlines：输出类型（JSON/Pydantic/regex/Literal）→ schema/grammar → 编译 token 级自动机 → 生成每步过滤非法 token → 唯一合法 token 时 fast-forward——模型不能提前闭合/输出畸形 JSON/发明 schema 外值；token 级过滤零事后修复；guidance regex 约束具体模式（如 email 格式）**（Outlines + guidance）→ 判据：**生成时强制非事后修**——"过滤非法 token"=非法输出不可能产生；"唯一合法 fast-forward"=加速合法路径。
- **输出契约层**：**n8n Structured Output Parser：AI Agent 开 Require Specific Output Format→选 Structured Output Parser→Define using JSON Schema——parser 自动注入格式指令，AI Agent prompt 不再需要 JSON 格式说明；从 JSON 示例生成 schema：只用类型和名忽略值、每字段当必填；output_schema 缺失时默认 permissive schema {type object, additionalProperties true}；Dify 三法：视觉编辑器（字段名/类型/必填/描述自动生成 schema）/JSON Schema 直接写嵌套数组校验规则/AI Generation**（n8n + Dify）→ 判据：**契约自动注入**——"parser 注入格式指令"=prompt 少写一段；"示例生成每字段必填"=宽松示例变严格契约；"缺失即 permissive"=默认不拦。
- **提升层**：工具/工作流（结构化输出三层强制）。

## 提示工程生产四件套与输出格式纪律（来源：RSFlowHub + WaytoAGI + FutureAGI + Coze + ML Digest 2026 实拉，r640A 落地，与 §提示五件套分工——那边管"提示构成五件套结构"，本条管"生产提示的四件套判据+输出格式纪律+示例/检索分工"）
- **四件套判据**：**可靠 prompt = role + context + task + format/constraints 四件全有；zero-shot 先：加示例为格式、加推理为逻辑、加检索为事实；few-shot 示例胜过长指令匹配格式——RAG 胜过长粘贴上下文取事实**（RSFlowHub）→ 判据：**四件套缺一不可**——"缺 format"=输出不可预测；"示例管格式/检索管事实"=各司其职不互替。
- **输出格式纪律**：**输出格式段落描述每个变量名称/输出内容/输出格式——变量名、输出内容、输出格式前后完全一致否则输出失败；结构化 prompt：Role 作为标题统摄全局、Profile/Rules 二级标题统摄局部；system message 配方：输出 JSON object 匹配 schema + never output any other text + 不把 PII 放 confidence reasoning**（Coze + WaytoAGI + FutureAGI）→ 判据：**格式段落与变量一致**——"名/内容/格式三处一致"=一处不一致即失败；"PII 不进推理理由"=输出侧隐私。
- **示例与迭代纪律**：**few-shot 选代表性示例、保持标签一致、避免示例泄漏、示例集当数据版本化；structured outputs：schemas/allowed values/validation/repair loops/何时安全 fallback；迭代 prompt 有界推进**（ML Digest）→ 判据：**示例集是数据**——"标签一致+版本化"=可复现；"repair loop 有界"=修复可收敛；"safe fallback 明确"=修不动有退路。
- **提升层**：模型/工作流（提示工程生产四件套与输出格式纪律）。

## LangGraph 结构化输出与工具 schema 冲突解法（来源：LangChain Forum + LangChain Docs + CSDN + AgentUpdate 2026 实拉，r640A 落地，与 §结构化输出三层强制分工——那边管"三层机制"，本条管"框架层冲突与响应键"）
- **with_structured_output 传参**：**传 Pydantic 类或 JSON Schema dict（dict 不导入类、清晰记录参数但冗长）；Pydantic 底层转 OpenAI Function Calling Schema**（LangChain + CSDN）→ 判据：**类或 dict 都行**——"Pydantic"=类型安全；"dict"=零依赖自文档。
- **schema 冲突解法**：**with_structured_output() 约束输出 schema 会与工具参数 schema 冲突——解法：在 with_structured_output() 自身里用 tools 参数而非链 bind_tools()，让 LLM 独立理解两个 schema**（LangChain Forum）→ 判据：**冲突=合并到同参**——"独立 bind_tools 链"=两 schema 打架；"with_structured_output 内 tools"=互不干扰。
- **createAgent 结构化响应键**：**LangChain createAgent 自动处理：用户设 schema→模型生成→捕获→校验→返 'structured_response' 键（state）；前端模式：agent 用工具调用返回结构化对象——type-safe 数据/精确渲染控制/跨模型一致格式**（LangChain Docs）→ 判据：**响应有固定键**——"'structured_response' 键"=下游稳定取；"工具调用返对象"=类型安全+渲染可控。
- **提升层**：工具/可复用 Skill（LangGraph 结构化输出与工具 schema 冲突解法）。

## 混合检索+重排管线参数配方（来源：IoT Digital Twin PLM ADR + Markaicode + buildbyzaki + 腾讯云 2026 实拉，r640B 落地，与 §RAG 检索工程·混合检索分工——那边管"要不要混合/双路机制"，本条管"混合管线各环节参数与何时跳级"）
- **标准配方**：**BM25 与 dense 并行各返约 100 候选→RRF 融合（score=Σ1/(k+rank)，k 通常 60，无需分数校准）→top 30-50 给 cross-encoder reranker→只送 top 3-10 给 LLM；跳过 reranker 仅当实测精度已够或延迟受限**（IoT ADR + buildbyzaki + Markaicode）→ 判据：**按环节定参数**——"RRF k=60"=无校准融合；"粗选 100/精排 30-50/送模型 3-10"=逐级收窄；"精度够才跳"=不默认省。
- **粗排精排分工**：**粗排（向量+BM25）快、召回面大、负责别漏；精排（Cross-Encoder 把问题+每个候选文档拼接做深度相关性打分）比双塔向量模型看得更细，判断问题与文档的细粒度相关**（腾讯云）→ 判据：**粗排保召回精排提精度**——"拼接打分"=看交叉交互；"双塔粗排"=只看向量距离。
- **模型与实现**：**BGE-M3 双编码器+向量库原生稀疏支持（Qdrant 1.10 起）；Ollama 两阶段：双索引各取 top-K（K=50-100）→RRF 融合→cross-encoder 重排，代价增 60-150ms 延迟；查询改写（multi-turn RAG 训练无关混合检索管线）**（Markaicode + arXiv）→ 判据：**能力与成本同看**——"原生稀疏"=免外挂 BM25；"60-150ms 换精度"=延迟预算内可接受。
- **提升层**：工具/工作流（混合检索+重排管线参数配方）。

## Contextual Retrieval 三层配方与 RAG 提示协议（来源：DataAspirant + Anthropic + WaytoAGI 2026 实拉，r640B 落地，与 §混合检索配方分工——那边管"检索管线参数"，本条管"chunk 上下文增强三层+提示侧隔离"）
- **三层递减配方**：**chunk 索引前用模型生成上下文预置到每个 chunk——检索失败率降 35%；加 context-enriched BM25 索引与 embeddings 并排——再降达 49%；加 reranker——达 67%**（Anthropic Contextual Retrieval）→ 判据：**上下文先于索引**——"索引前预置上下文"=孤立 chunk 变可检索；"BM25+向量并排"=双通道互补；"reranker 收尾"=精度最后提升。
- **RAG 提示协议**：**<context>{Context}</context> 标签显式分隔检索片段，指示基于标签内知识片段回答用户问题——检索内容与指令域隔离**（WaytoAGI）→ 判据：**片段有界**——"标签定界"=模型知道哪里是证据；"基于标签内回答"=不越界引用。
- **提升层**：工作流/可复用 Skill（Contextual Retrieval 三层配方与 RAG 提示协议）。

## RAG 检索双层指标与生产监控（来源：Kunal Ganglani + Lokesh Reddy + DEV + Apptension 2026 实拉，r640B 落地，与 §评估驱动开发分工——那边管"整体评估流程"，本条管"检索侧两段指标与静默退化"）
- **双层指标**：**retriever 测 recall@N（大 N 如 50-100，对标注相关段落）；reranker 测 MRR@k / nDCG@k（对重排后 top-k）——两段分开测**（Kunal Ganglani）→ 判据：**按段选指标**——"召回看 retriever 大 N"=候选面；"排序看 reranker top-k"=精排质量。
- **静默退化陷阱**：**retriever recall@100 从 0.92→0.80 时 reranker 可能暂时保持 MRR@10 稳定——然后命中相关段落永远没进候选的查询爆发：reranker 救不了召回不足**（Kunal Ganglani）→ 判据：**召回是上限**——"reranker 只重排已召回"=候选缺失不可恢复；"MRR 稳≠健康"=监测要两段一起看。
- **指标语义与生产目标**：**Recall@k=top-k 是否含至少一个所需 chunk（找到证据没）；Precision@k=返回集多少有用（噪声与 token 浪费）；MRR=首个支持 chunk 多靠前（短窗口关键）；多跳算完整所需集 recall 非单个；四层评估=检索质量/生成质量（faithfulness/relevance/hallucination）/端到端（answer correctness/满意度）/观测；生产目标示例：Recall@20≥0.90（golden set）、MRR≥0.70、Coverage≥0.85**（Lokesh Reddy + DEV + Apptension）→ 判据：**指标对齐问题**——"多跳全集 recall"=单块命中不算完成；"四层分层"=故障定位到层。
- **提升层**：工具/工作流（RAG 检索双层指标与生产监控）。

## 长时程执行可恢复性：checkpoint 对齐回退与四性架构（来源：arXiv AgentRewind + AgentR + LangChain Delta Channels 2026 实拉，r640C 落地，与 §执行态交付态分开分工——那边管"状态怎么记"，本条管"错了怎么回退恢复"）
- **对齐 checkpoint 回退**：**AgentRewind：记录 agent 上下文与受控环境的对齐 checkpoint，允许 agent 回到早期状态、携带前次尝试的信息续跑；MettleBench 评估长时程工程任务完成度+部分进度**（arXiv 2608.14380）→ 判据：**错误后可恢复**——"对齐 checkpoint"=上下文与环境同步存档；"带前次尝试信息续跑"=回退不丢经验。
- **四性架构**：**AgentR：Observable 任意时刻可查任何 pipeline stage 状态 / Durable 状态存 PostgreSQL 非 worker 内存或对话上下文 / Recoverable 终态失败经 RE_INITIATED 转换可恢复 / Auditable 状态转换时间戳可追溯**（arXiv 2608.15264）→ 判据：**四性齐才算持久**——"状态存 DB 不存内存"=重启不丢；"终态失败可恢复"=失败非终局；"转换可追溯"=审计可查。
- **delta+快照存储**：**LangChain Delta Channels：每步只存 delta+每 K 步写全量快照——限定恢复延迟、存储成本随会话增长平摊**（LangChain blog）→ 判据：**增量存储**——"每步 delta"=存储线性；"每 K 步快照"=恢复有界；两者平衡恢复速度与成本。
- **提升层**：工具/工作流（长时程执行可恢复性）。

## 持久化引擎：确定性重放与事件溯源（来源：Azure Durable Functions + Temporal + AWS Lambda durable + Diagrid 2026 实拉，r640C 落地，与 §checkpoint 对齐回退分工——那边管"回退策略"，本条管"引擎级重放机制"）
- **确定性重放**：**Durable Functions：每次函数恢复后 orchestrator 从零重跑；每轮重跑查执行历史判断异步任务完成否——已完成任务重放其输出并继续，直到整个 history 重放完；orchestrator 代码必须确定性（重放多次每次结果相同），事件溯源保证可靠执行+维护局部变量状态**（Azure Durable Task）→ 判据：**重放幂等**——"从零重跑+查 history"=已完成不重执行；"orchestrator 确定性"=重放结果一致；非确定性代码（随机/当前时间/外部调用）不能直接写 orchestrator。
- **事件历史重放**：**Temporal：状态在内存时内存消失进度消失；durable execution 把每步记录为不可变 event history——进程死于 step 47/100 时重放事件日志从 step 48 恢复**（Temporal guide）→ 判据：**事件即真相**——"不可变 event history"=进度可重建；"重放从失败后一步"=不重做已完成工作。
- **平台化落地**：**AWS Lambda durable functions：checkpoint/replay——代码从头跑但跳过已完成 checkpoint 用存储结果，支持最长一年执行；Diagrid：记录 workflow 状态+已完成 step 从失败点恢复（agent 常多工具调用+等待外部系统+随时间决策）**（AWS + Diagrid）→ 判据：**时长与失败两维**——"一年执行"=长程可行；"记录已完成 step"=恢复点精确。
- **提升层**：工具/工作流（持久化引擎确定性重放）。

## 恢复语义三原则：重试≠恢复、重入同一 attempt、批级幂等（来源：n8n + Microsoft Foundry + Activepieces + n8n batch 2026 实拉，r640C 落地，与 §重试分两类分工——那边管"transport/tool 怎么重试"，本条管"失败后恢复的语义选择"）
- **重试≠恢复**：**多数自动化平台给 retries 不给 resumes：n8n 对失败执行点 retry 用原始输入重跑整个 workflow；queue 模式 worker 崩溃不丢执行（2.43.7 起关停 worker 不丢）；要恢复必须显式设计（拆 step 状态化+记录进度）**（DEV + zadrig）→ 判据：**retry=重跑、resume=续跑**——"原输入重跑"=从头再来；"worker 崩溃不丢"=执行已持久化；要续跑必须显式状态化。
- **重入同一 attempt**：**Microsoft long-running agent：故障恢复重新进入同一 attempt 状态——不消耗重试限制，真实时间 timeout 不因进程重启重置；持久检查点多智能体编排：每个 agent 调用设 checkpoint，任何 step 失败协调流程自动恢复，已完成 agent 调用恢复时不重新执行**（Microsoft Foundry）→ 判据：**恢复≠新尝试**——"重入同一 attempt"=不烧重试额度；"已完成调用不重执行"=幂等边界明确。
- **批级幂等**：**n8n 批处理恢复设计：每个 batch 幂等+外部记录处理状态→失败 batch 可重试不用重跑完整数据集；Activepieces Durable Execution：worker 中途死→新 worker 复用每个已完成 step 的已存输出、只跑第一个未完成 step——不重发邮件/不重复扣卡/不重调 API；覆盖 crash/deploy/long pause/retry**（n8n support + Activepieces）→ 判据：**粒度=batch/step**——"batch 幂等+外部状态"=重试局部；"复用已完成 step 输出"=副作用不重放。
- **提升层**：工作流/可复用 Skill（恢复语义三原则）。

## 给 agent 验证途径与确定性验证循环（来源：WaytoAGI 生态 agentic-workflow + AgenticBook + deeplearning.ai Spec-Driven + Claude Code 2026 实拉，r641A 落地，与 §AI 生成代码收 diff 五连查分工——那边管"交付前查什么"，本条管"让 agent 自己验证的机制"）
- **给验证途径，agent 才能自主闭环**：**Tests 是金标准——"让这个测试通过"是 agent 无需你就能验证的目标；build/type-check 退出码——非零即无歧义反馈；截图/渲染输出——UI 工作让 agent 用浏览器工具看结果迭代；用 Stop hook 确定性接入验证循环：agent 完成时跑测试套件**（WaytoAGI 生态 ai-agent-guidebook）→ 判据：**验证必须可机检**——"测试通过/退出码/截图"三选一给 agent；没有验证途径的 agent 只能自我感觉良好。
- **PIV：计划-执行分离**：**Plan-Implement-Validate——写计划、审计划、执行单步、测试验证、commit Git、重复；不阻塞主终端，用后台 daemon；Plan 是最高杠杆步骤——先让它说打算怎么解决再批准或纠正：修坏计划一句、修坏实现一下午；一次一个小范围任务**（AgenticBook + simplyexplained）→ 判据：**计划先行且可审**——"计划一句纠偏"远便宜于"实现一下午返工"；单步验证后才 commit，坏计划挡在代码前。
- **Spec 分层驱动**：**deeplearning.ai Spec-Driven：三层=Constitution 项目级/Feature specs 特性级/Replanning 特性间；Feature Loop 每步在新 agent context 执行、各自独立 Git 分支；你当带图纸的建筑师，agent 当施工者**（deeplearning.ai community）→ 判据：**规格三层分离**——"Constitution 管全局/Feature specs 管单特性/Replanning 管变更"；新 context+独立分支=特性间零污染。
- **提升层**：工作流/可复用 Skill（给 agent 验证途径与确定性验证循环）。

## LLM 输出当不可信输入与结构化错误契约（来源：n8n Community + Dify 代码节点 + davila7 n8n-code 2026 实拉，r641A 落地，与 §工具结果断言层分工——那边管"工具返回怎么断言"，本条管"LLM 文本输出怎么解析"）
- **LLM 输出一律当不可信输入**：**strip fences+preamble——一行杀掉 code-fence 和"Sure, here you go"前缀；parse 在 try/catch 内，失败返回结构化错误项 {ok:false, raw:原文} 而不是 throw；IF 节点路由 ok:false 分支——一个 Code 节点防 2am 执行死亡**（n8n Community）→ 判据：**解析失败进分支不进死路**——"不 throw 返结构化错误"=可路由；"保留 raw"=可人工排查。
- **代码节点沙箱与输出限制**：**Dify Code 节点在沙箱环境运行，需要外部网络调用用 HTTP Request 节点；输出限制：String 最大 80,000 字符（null 字节自动移除）/Number -999999999~999999999 最多 10 位小数/Object/Array 最大嵌套 5 层超出截断；生产提示=用前验证结果 Validate the result before using it in code**（Dify 文档 + fjsi.top）→ 判据：**边界已知**——"沙箱无网"=网络走 HTTP 节点；"输出有上限"=构造时预留；"用前验证"=不拿未验结果继续算。
- **Code 节点 checklist**：**代码非空有逻辑/必须 return list of dicts/每项 {"json": {...}} 格式/数据访问用 _input.all() first() item/只用标准库无外部 import**（davila7 claude-code-templates）→ 判据：**节点输出形状固定**——"list of dicts + json 键"=下游统一消费；"无外部 import"=沙箱兼容。
- **提升层**：工具/工作流（LLM 输出当不可信输入与结构化错误契约）。

## 编码 agent 编排与治理配方（来源：TheNextGenTechInsider + KDnuggets + LouisBouchard + Claude Code + GitHub gh-aw 2026 实拉，r641A 落地，与 §多 Agent 协作纪律分工——那边管"多 agent 怎么协作"，本条管"编码场景的编排与收尾治理"）
- **多 agent 分责编排**：**一个管 scaffolding（文件创建/依赖更新）、一个管 business logic、一个跑 static analysis；简单脚本喂前一个输出给下一个，每阶段暂停等人工审批**（TheNextGenTechInsider）→ 判据：**按职责切 agent+阶段闸门**——"脚手架/业务/静态分析"三分；"每阶段人工审批"=失控点前置。
- **Review AI 改动八问**：**解决请求的问题没/改无关行为没/加不必要抽象没/弱化安全没/隐藏错误没/更新测试没/跟项目约定没/diff 能更小吗**（KDnuggets）→ 判据：**逐问核对**——八问全过才收；"隐藏错误"最隐蔽——表面绿但吞掉失败=不可收。
- **成功循环沉淀与配置治理**：**同一成功循环重复 3 次就编码成 skill（带规则/引用/检查/反馈环）；CLAUDE.md 过长会过度指定——规则淹没在噪声里被忽略一半，无情剪枝：Claude 已能做对的指令删掉或转成 hook；无限探索用 subagents 窄化不吞主上下文；Agent 节点配 Clear Tool Descriptions+Appropriate Iteration Limits（防失控成本）+Detailed Instructions；GitHub Agentic Workflows（gh-aw）：Markdown+frontmatter 编译成真实 Actions 工作流，agent jobs 默认只读**（LouisBouchard + Claude Code + Dify + GitHub）→ 判据：**沉淀与收敛**——"3 次重复成 skill"=资产化；"剪枝 CLAUDE.md"=指令密度可控；"iteration limits"=成本有界；"默认只读"=最小权限。
- **提升层**：工作流/可复用 Skill（编码 agent 编排与治理配方）。

## 个人自动化配方：Morning Brief 单 payload 模式与入门工作流（来源：Make Community + WorkflowPick + futureworknavigator + planetspark + 36氪 2026 实拉，r641B 落地，与 §轻量自动化三模式分工——那边管"自动化用什么形态搭"，本条管"个人自动化怎么起手与组装"）
- **单 payload 喂 AI**：**AI Morning Brief：Create JSON 模块把 meetings/emails/tasks/weather/news 五源+日期时区合成一个结构化对象给 AI——一次合成一次推理，多源决策统一入口**（Make Community）→ 判据：**先聚合再推理**——"五源合成单对象"=模型只做一次综合；"带日期时区"=上下文完备。
- **入门配方与起点选择**：**第一个工作流=email 附件自动存 Google Drive（15 分钟教 triggers/模块连接/文件处理）；最优起点模板="new lead form→Slack alert+Google Sheets row"（3 模块 25 分钟 3 operations/次——教 trigger/mapping/多步 action 无需 filter/router）**（futureworknavigator + WorkflowPick）→ 判据：**先跑通核心概念**——"第一单=真实有用+教基础"；"3 模块不碰 filter/router"=概念少失败少。
- **系统可持续原则**：**70% 容量稳定运行的系统胜过几周崩一次的完美系统——简单与可持续是特性不是妥协；每 90 天复盘：什么有效/什么要改，把系统当技能刻意练习**（planetspark）→ 判据：**可持续优先于完美**——"70% 稳定"=能用比好看重要；"90 天复盘"=系统是活实践。
- **平台原生定时**：**Codex 原生支持定时任务——左上角"已安排"选 Templates 复用别人建好的模板，或新建项目告诉 Codex 创建（什么时间跑/频率）**（36氪 ChatGPT Work 10 技巧）→ 判据：**先复用模板**——"Templates 已有任务"=零搭；"描述时间频率"=声明式建。
- **提升层**：工作流/可复用 Skill（个人自动化配方）。

## 自然语言建 flow 与 agent 执行链（来源：Activepieces + Zapier + Langflow 1.13 2026 实拉，r641B 落地，与 §多 Agent 协作纪律分工——那边管"拆了之后怎么协作"，本条管"低代码平台的自然语言编排"）
- **描述即构建**：**Activepieces：有人描述需求→flow 被建好，要改再问一次或开 builder；Zapier Copilot：plain English 描述工作流→AI 构建，连接 6000+ apps**（Activepieces + ITLearning）→ 判据：**需求描述=flow 规格**——"口语描述直接建"=门槛为零；"改=再描述"=迭代闭环。
- **agent 执行链与审批点**：**Activepieces AI agent builder：设目标+选 apps/flows/files，agent 决定步骤并执行；想检查的先等人工审批；例=处理收件箱发票：找发票→匹配 PO→查预算→付款——agent 带审批点的多步链**（Activepieces）→ 判据：**目标+资源+审批点三件套**——"设目标选资源"=agent 自主；"想检查先等审批"=高风险步人闸。
- **协同与审计**：**Langflow 1.13：audit logging/可复用 connections/concurrent editing 检查——多人编辑同一 flow 时保护一个用户的保存不覆盖另一个**（Langflow blog）→ 判据：**并发编辑有保护**——"一个用户保存不覆盖另一用户"=并发安全；"audit logging"=变更可查。
- **提升层**：工具/工作流（自然语言建 flow 与 agent 执行链）。

## Agent 场景模型与技能化差异（来源：腾讯云 Agent 开源模型盘点 + Anthropic Building agents with Skills + HF 榜单 2026 实拉，r641B 落地，与 §编码 agent 编排分工——那边管"编码场景怎么编排"，本条管"为什么 agent 需要 skills"）
- **Agent 模型选型标准**：**五款 Agent 开源模型（Ornith/Laguna/Nex N2/Devstral/Nemotron）：训练目标不是"回答得好"而是"把事情办成"；都能本地部署——数据不上云、不按月付费 API**（腾讯云）→ 判据：**任务达成而非问答**——"把事情办成"=Agent 场景指标；"本地部署"=隐私+成本双赢。
- **Agent 与 Skills 的分工**：**Anthropic：为什么停止构建 specialized agents 改 skills——agents 有 intelligence+capabilities 但不总有 expertise；skills=组织好的文件集合打包领域专长（工作流/最佳实践/脚本）格式 agent 可访问应用，把通用者变专业者**（Anthropic）→ 判据：**能力补专长**——"intelligence+capabilities≠expertise"；"skills 打包领域专长"=可复用专家库。
- **模型与技能生态**：**HF 榜：Qwen3.8-27B 成历史最受欢迎开源模型（超 FLUX.1/DeepSeek-R1/Kimi-K3/Meta-Llama-3）；GLM-5.2 下载 6 万+/百度无限 OCR 一次解析 40+ 页文档 7 万下载；Anthropic 预建 skills=pptx/xlsx/docx/pdf 文档任务，一手技能库 19 个**（36氪 + Anthropic）→ 判据：**按任务选型**——"文档任务=预建 skills"；"下载榜=社区验证"。
- **提升层**：模型/工具（Agent 场景模型与技能化差异）。

## 多跳 RAG 四类架构与程序化重构成（来源：arXiv 2026 多跳 RAG 系列 + ConRAG + MatRAG + UniAI-GraphRAG 实拉，r641C 落地，与 §RAG 检索双层指标分工——那边管"检索怎么评"，本条管"多跳推理怎么架"）
- **三类主流 + 程序化一类**：**现有多跳 RAG 方法：query-side 任务分解（拆查询）/corpus-side 知识图谱构建（建图）；多跳/层级 RAG 架构克服复杂查询约束：结构化知识整合+长上下文理解+多步推理，通过 step-wise retrieval/hierarchical information synthesis/query decomposition 实现**（ConRAG + Engineering the RAG Stack）→ 判据：**按约束选架构**——"知识在多个文档"=多跳；"单文档长上下文"=层级综合。
- **检索-推理程序化**：**PyRAG：把 multi-hop RAG 重构成程序合成与执行——检索-推理过程编码成可执行 Python 程序，中间状态暴露为变量、确定性编译器反馈、可检查推理轨迹，training-free self-repair 和 adaptive retrieval 是执行接口的直接副产品；5 个 QA benchmark 一致增益**（PyRAG）→ 判据：**程序即推理轨迹**——"中间状态变量"=可检查；"编译器反馈"=确定性修正；"self-repair 副产品"=不额外训练。
- **成本与精度平衡**：**MatRAG：MRL+聚类结构语义层级对齐，语料组织成 DAG 聚类（粒度递增）每层低维嵌入索引——同时降存储/检索两类成本保持质量；ConRAG 共识驱动多视角；UniAI-GraphRAG 本体引导抽取+多维聚类+双通道融合（推理/时间查询 F1 超开源方案）**（MatRAG + ConRAG + UniAI）→ 判据：**层级索引降成本**——"DAG 聚类+低维索引"=先粗后细；"共识多视角"=多路互证。
- **提升层**：工具/工作流（多跳 RAG 四类架构与程序化重构成）。

## 引用归因三层：API 结构化 / 强制引文 / 生成后校验（来源：Anthropic Citations API + Google grounding + Constitutional AI + 归因方法 2026 实拉，r641C 落地，与 §输出校验分工——那边管"输出格式校验"，本条管"claim 到来源的可信度"）
- **API 层结构化归因**：**Anthropic Citations API：给 source documents，返回含 source-grounded citations，citation metadata 绑定具体支持段落；关键不是"更好提示"而是 API 层结构化归因——机器可读的 claim↔passage 链接；Google grounding：groundingSupports+groundingChunks 字段把模型陈述直接链接到来源**（TechYorker + Google）→ 判据：**归因在 API 层不在提示层**——"机器可读链接"=程序可验证；"metadata 绑定段落"=精确溯源。
- **提示层双指令**：**cite quotes and sources for each claim + if it can't find a quote, it must retract the claim——要求引文和要求撤回是两个不同指令，多数 prompt 只含第一个；inline "[Source: document_id]" 强制模型把 claim 追溯到段落**（Prompt Architects + BooleanBeyond）→ 判据：**引文+撤回分开写**——"只要求引文不要求撤回"=编造引文照样输出；"uncited claim=unsupported"。
- **生成后机械校验**：**citations 启用=认知约束（每句要 source 指针）；生成后 cited_text 附每 segment——可机械后滤"drop any segment whose citations array is empty"/"reject any number that doesn't appear in the cited text"；编程检查 citation ID 是否在 retrieved context 列表——ungrounded citations 是强幻觉信号；验证≠查源真实（garbage in verified garbage out——检索文档旧或错→faithfully verified wrong answer）**（Claude Lab + BooleanBeyond + Dotzlaw）→ 判据：**后滤是机械的**——"空 citations 数组即删"；"校验 ID 在 context"=引文真实性；"验证不查源真实性"=来源质量另行管。
- **提升层**：工具/工作流（引用归因三层）。

## 检索问题先查检索再怪模型（来源：Future AGI + Atlan + RAG attribution 方法 2026 实拉，r641C 落地，与 §LLM 输出当不可信输入分工——那边管"输出解析"，本条管"输出不可信时先查哪"）
- **先评分检索再动 prompt**：**查检索再怪模型：先评分 retrieved chunks 与问题相关性，不相关修 chunking/embeddings/query 而非 prompt；Validate tool arguments before execution：每工具调用先过 schema 校验**（Future AGI）→ 判据：**根因分层**——"检索不相关=改检索不改提示"；"参数非法=调用前拦"。
- **按复杂度路由**：**Adaptive RAG：2026 实践共识"emerging best practice"——按查询复杂度路由（训练一次小分类器，modular 部署），平衡成本与精度，NAACL 2024 基准超迭代与单步基线**（Atlan）→ 判据：**路由先于检索**——"简单查询=单步/复杂=多步"；"分类器训一次"=成本可控。
- **归因工具包**：**5 个 RAG attribution 方法（2026-05-28 发布）：来源归因是企业 RAG 盲点——证明生成陈述确实来自它声称的文档；RAG 减幻觉 42-68%，医疗+PubMed 89% 事实准确**（RagAboutIt + fwdslash）→ 判据：**归因是独立工程层**——"证明陈述来自文档"=可审计；"RAG 减 42-68%"=有据可查。
- **提升层**：工作流/可复用 Skill（检索问题先查检索再怪模型）。
























