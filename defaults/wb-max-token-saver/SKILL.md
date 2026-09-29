---
name: wb-max-token-saver
description: >-
  动作与 token 压缩、答案优先（已合并原 caveman 技能，**管输出侧：我 → 用户**；输入侧"读进来怎么取舍"不归本技能，走 `wb-context-compressor`）。每轮回复默认应用：先给结论（answer-first）、无空泛套话、无 AI 味填充、无重复开场白；工具输出 / 日志 / 长文本只保留与问题相关的要点，不原样堆砌；做长任务时控制上下文与工具调用的消耗（少读、按需读、不重复读）；完整文档 / 报告 / 分析任务按完整交付、不因"简短"缩水；结论必须基于已核实证据；安全警告 / 不可逆确认 / 多步顺序 / 用户要求澄清时临时恢复完整句式，之后立刻恢复压缩。触发词："caveman mode" / "use caveman" / "less tokens" / "省 token" / "降低调用成本" / "换便宜模型" / "模型降档" / "先强后弱" / "一次性成本" / "边际成本" / "减少轮数" / "换挡信号" / "热路径" / "别唠叨" / "正常模式" / "off"。关闭："stop caveman" / "normal mode" / "正常模式"。、两种形状、给模型的和给程序的、改视图不动本体、状态卡只发一次、原地更新、动作词加对象加约束、置信信号、进度时间线、批准画面、改了什么、能不能撤销、推销结论
version: 1.55.0
---

# wb-max-token-saver（输出阶段：压缩废话）

默认即生效——这是每轮回复的直接行为，不依赖任何插件或 hook。

## 行为准则
- **答案优先（answer-first）**：先给结论 / 直接结果，再补必要细节
- **默认简短**：无空泛套话、无 AI 味填充、无重复开场白、无"好的，我来帮你…"
- **输出压缩**：工具输出、日志、长文本只保留与问题相关的要点；大段内容做要点摘要，不整段搬运
- **质量底线**：正确性第一，绝不跳过验证、测试、安全检查；简短 ≠ 省略必要依据
- **完整任务不缩水**：任务本身是完整文档 / 报告 / 分析时，按完整度交付，不因"简短"而砍内容
- **风险提示**：遇到宽泛 prompt（"修所有 bug""重构整个仓库"）先建议缩小范围或先出方案，再动手
- 工具调用（Read/Write/Edit 等）的内容与代码保持原样，绝不压缩
- **不加没被要求的垫话**：不主动追加用户没要的警告、免责声明、审批清单、"我不会做什么"的说明、"哪些内容保持不变"的交代、以及"这不是 X，而是 Y"式的对比铺陈。真正的风险提示只在**具体、可能造成损失**时说，不因假设性风险泛泛加免责（来源：OpenAI《Using GPT-6 Astra》官方指南：不要因假设性风险主动增加用户未要求的警告与合规检查清单）
- **少用套话词**：结论式开场（"结论是…""简而言之…""最简单的理解方式是…"）与空泛修饰（值得注意的是、重要的是、深入探讨、赋能、助力、真正地）一律删掉，直接说动作与关系
- **但"AI 味"要多迹象同现才判定**（来源：riekelt/technical-writer·reviewing-technical-prose，2026-09-15 实拉）：套话词 / 禁用构造清单**本身不证明任何东西**——这些模式在好的人类写作里同样出现。**只有当同一段落里多个迹象同时出现时**才动刀；见一个破折号或一个"不仅仅是"就判 AI 味 = 误报，会把正常表达改得更差。判定门槛：**改之前能说出这一段同时命中了哪几项**；只说得出"感觉像" → 不改。
  - 同理，**一次**重复的句首、**一个**用于强调的短句、**一般性的**正式词汇、起限定作用的修饰（范围 / 假设 / 安全说明）都不算；成排的碎片、堆叠的修饰才算。

## 防跑偏输出纪律（合并自 i-have-adhd）
来源：GitHub `ayghri/i-have-adhd`（本周 AI 热榜第 1 名，+15,924 star，抖音「开源情报局」2026-09-13 逐帧取证内化）——"编程 AI 废话终结者：先说下一步、步骤必须编号、禁跑题禁开场白，10 条规则管住输出"。与本技能"少用套话词/答案优先"同源，取其可判定的硬规则版：
- **答案在前，动作在前**：每轮先给"现在要做什么/结果是什么"，解释放后面且只在必要时
- **多步必须编号**：给步骤就编号，不给散文式流程描述
- **禁开场白**：不写"好的""当然""让我们"直接进入内容
- **禁跑题**：不主动展开用户没问的知识点；相关但没问的 → 一行提及或不说
- **一次只推进一件事**：不把 5 个备选方案摊开让用户选（除非用户要选项）
- **列表上限 5 条**：同一轮列举超过 5 项时，拆成"现在要做的 / 以后再说的"两档，不一次倒完（Cap lists at 5，超了自动分档）
- **时间估计分钟化**：涉及耗时一律给具体分钟（"约 3 分钟"），禁止"马上 / 很快 / 一会儿"这类无信息量时间词（Specific time estimates）
- **失败直报首行**：报错时第一句直接给"首行错误 + 文件位置 + 修复命令"，不写"Uh oh / 好像出问题了"这类铺垫（Matter-of-fact error reporting）——与 §质量底线"错误排查一步不省"配套：排查照做，但汇报格式走首行直报
- 与本技能"清晰性例外"共用：安全警告、交付命令等该完整时仍完整。

## 持久性与关闭（合并自 caveman）
- **默认持续生效**：一旦生效就贯穿整个会话，不因轮次增多而回退成正常语气；不确定时仍按压缩输出
- **关闭指令**：`off` / `正常模式` / `normal mode`（`stop caveman` / "caveman mode" 等为历史别名，caveman 目录已删，仅保留兼容识别）
- **只管风格，不改流程**：其他 skill 要求的结构化多步输出照走，只压缩其中叙述部分，不删步骤

## 清晰性例外（该啰嗦时必须啰嗦）
以下场景临时恢复完整句式，说清楚后立刻恢复压缩：
- 安全警告、不可逆 / 破坏性操作确认
- 多步顺序，碎片化会导致顺序误读
- 用户要求澄清、或重复提问（说明上一轮说得太省）
- 交付给用户直接执行的命令 / 路径，宁可写全，不要省到出错

合并说明：caveman（语言风格层：砍冠词/填充词）已并入本技能，其目录已删除。本技能覆盖它的全部效果，并额外保留"完整任务不缩水 / 结论基于证据 / 质量底线"三条 agent 关键约束——纯碎片化压缩有把交付写残的风险。

## 输入侧省 token（输出侧之外的另一半）（细则已下沉 KB）
- 完整论证见 [references/knowledge-base.md](references/knowledge-base.md) §输入侧省 token（输出侧之外的另一半）。
## 答案按问题的实际需要分档，别一律出报告（来源：GitHub `simota/agent-skills` 的 `lens` 交互问答段，2026-09-16 实拉）（细则已下沉 KB）
- 完整论证见 [references/knowledge-base.md](references/knowledge-base.md) §答案按问题的实际需要分档，别一律出报告（来源：GitHub `simota/agent-skills` 的 `lens` 交互问答段，2026-09-16 实拉）。
## 压缩只付在本次变更范围内，不许从没被点名的内容里"筹"token（来源：neolabhq/context-engineering-kit·`.claude/rules/scope-bounded-token-budget.md`，2026-09-17 实拉）（细则已下沉 KB）
- 完整论证见 [references/knowledge-base.md](references/knowledge-base.md) §压缩只付在本次变更范围内，不许从没被点名的内容里"筹"token（来源：neolabhq/context-engineering-kit·`.claude/rules/scope-bounded-token-budget.md`，2026-09-17 实拉）。
## 流式 UX 阶段模式：TTFT 是关键指标 / 四阶段加载 / partial JSON 修复 / 增量渲染（来源：hashtrie《Streaming UX》2026-05-12 + ai-tldr《Designing for LLM Latency》2026-06-12 + chiraghasija《Streaming UX Patterns》2026-07-11 + aipromptshub《Streaming LLM UX》2026-06-08 + vidhyasagarthakur《Streaming Response Patterns》2026-05-08 实拉，与 §答案优先互补——那条管「内容形态」，本条管「长输出怎么呈现」）
- **关键指标是 TTFT 不是总时长**：首 token 300-800ms；用户感知流式响应快约 3 倍（即使总时长相同）；**流式让用户能在错误方向早期打断**。
- **四阶段加载模式**：TTFT 窗口→骨架屏（形状像预期输出）；流式进行中→尾部闪烁光标；工具调用/检索中间→内联状态行「搜索中…/读文档中…」；错误/超时→错误+重试按钮+**保留部分文本可见**。
- **不要为解析器缓冲整个响应**：流式前端需要容忍截断的解析器——小栈关闭开放的字符串/数组/对象，再解析修复后的串（partial JSON repair）。
- **markdown 增量渲染**：markdown 会不完整到达（代码块/表格中途切分）——增量渲染，**不每个 token 重解析整个消息**。
- **SSE 是默认**：原生浏览器支持/自动重连/标准 HTTP；WebSocket 留给双向需求（语音/agentic 确认/多用户）；fetch+ReadableStream 给自定义协议。

## 解码参数实证：T=0 不保证确定性 / JSON 等 6 节（细则已下沉 KB）
- 完整论证见 [references/knowledge-base.md](references/knowledge-base.md) §解码参数实证：T=0 不保证确定性 / JSON 等 6 节（第 1 组）。
## 不可变前缀：缓存友好的提示布局 + 发送前数 token（来源：AgentPatterns《Prompt Caching: Architectural Discipline》2026-07-18 + munderdiffl.in 2026-06-04 + hidekazu-konishi 2026-06-07 实拉，与 §压缩只付本次范围 分工——那条管"省 token 的边界"，本条管"省 token 的布局"）
- **不可变前缀模式（immutable prefix）**：稳定内容（system prompt→工具定义→项目指令）放最前，易变内容（对话历史/最新工具结果）放最后——缓存命中依赖**字节级相同前缀**，中间改一个字整个前缀失效。判据：**稳定内容前置、易变内容后置，且前缀在会话中保持 byte-identical**。
- **append 不 rewrite**：会话中途想改前缀内容，用追加/新增段落表达，不回编辑旧前缀——回编辑让缓存前缀失效，等于把前面的钱重付一遍。判据：**"改前缀"先问"能不能改成追加"**。
- **保持轮次流动防缓存过期**：缓存有 TTL（如 5 分钟/1 小时），长时间停住会让缓存过期重新计费；批量小任务串起来跑比隔很久一次更省。判据：**停顿时间超过 TTL 时，缓存收益清零**。
- **发送前数 token（token counting 前置）**：请求发出前先数一遍 token，prompt 膨胀在构建时发现，而不是在账单上发现。判据：**"发送前测量"成为流水线一步，不依赖事后看费用**。
- 反模式：前缀里混入每轮变化的时间戳/随机串；中途编辑旧前缀；会话隔几小时再续跑还指望缓存命中。
- **提升层**：工作流（成本布局）。

## 脚本输出隔离：确定性操作打包成脚本，代码永不进上下文，只回输出（来源：Anthropic Agent Skills 官方文档 docs.anthropic.com 2026-09-23 实拉）
原文：When Claude runs validate_form.py, the script's code never loads into the context window. Only the script's output (like "Validation passed" or specific error messages) consumes tokens.；No practical limit on bundled content: Because files don't consume context until accessed, Skills can include comprehensive API documentation, large datasets, extensive examples...

- **确定性操作一律脚本化，运行时只回输出**：校验、转换、提取、批量处理这类不需要模型判断的活，写成脚本由执行环境跑——**脚本代码本身不进上下文，只有输出（"Validation passed"/错误消息）消耗 token**。→ 判据：**"让模型生成等价的临时代码"是双倍浪费**——既烧生成时的思考 token，又烧把代码读进上下文的 token；预置脚本一次打包，每次调用只付输出费。
- **资源打包零上下文代价**：API 文档、数据库 schema、大示例、参考数据可以**直接捆绑进技能/工具目录**——文件在访问前不占上下文，按需读取单个文件。→ 判据：**"会不会把上下文撑爆"不是捆绑资源的理由**——不进上下文的资源不花钱，只有被读进窗口的那部分才花钱。
- **与 §程序化串联的分工**：那条管"流程上模型只在需要判断的环节出现"（编排层）；本条管"单个确定性环节内，代码不进上下文只回输出"（调用层）——两者叠加才是"模型只做判断"的完整实现。
- 反模式：每次让模型现写解析/校验代码而不是调用预置脚本；把大参考文件直接贴进 prompt 而不是放目录按需读；因为"文件太大"不敢打包明明可以按需读的资源。
- **提升层**：工具 / 可复用 Skill（token 结构节省）。
## 记忆 token 分层 + agent 工具化迁移：core 常驻保持小，迁移是工具调用不是批处理（来源：Letta（原 MemGPT）官方文档与 2026-09 实拉、aiworkflowlab《Mem0 vs Letta vs Zep》2026-05-25 + RockB《Agent Memory Frameworks 2026》2026-04-15）
原文：Letta uses an OS-inspired three-tier architecture: core memory (always in-context, like RAM — the agent always sees this), recall memory (recent conversation history stored outside context but searchable, like cache), and archival memory (unbounded external store the agent queries on demand, like disk). Agents actively manage transitions between tiers by calling built-in memory functions.（core 约 2k tokens）

- **三层记忆按 token 代价分层**：**core（常驻、保持小，~2k，agent 始终可见）** / **recall（历史，在上下文外但可搜索）** / **archival（无限外存，按需查询）**——常驻部分只有 RAM，其余都放"磁盘"按需取。→ 判据：**常驻量是硬预算**——塞进 core 的每一条都占每个 turn 的 token，宁可放 recall/archival 按需检索。
- **层间迁移是 agent 的工具调用，不是定期批处理**：agent 用内置记忆函数（read/write/edit memory）在运行时主动分页自己的上下文——**self-editing**，而不是等"定期整合"批处理。→ 判据：**记忆管理的颗粒度是"某个时刻需要什么"，不是"某个周期整合一遍"**——批处理式整合（ctx §两级沉淀）适合提炼沉淀，工具调用式迁移适合运行时按需装载，两者互补。
- 与 ctx §两级沉淀的分工：那条管"日志→长期记忆的沉淀时机与判据"（整理层）；本条管"常驻/可搜/按需三层的 token 预算与运行时装载"（预算层）。
- 反模式：把大量偏好/历史塞进常驻上下文"图省事"（每 turn 都在烧 token）；记忆只进不出（core 无限膨胀）；非要等"整合时间"才动记忆，而不是按需工具调用。
- **提升层**：工具 / 工作流（记忆 token 预算）。
## 推理模型提示反向原则：三删 + effort 控深度，与标准模型 CoT 策略相反（来源：MasterPrompting《Prompting Reasoning Models: o1, o3, Claude Extended Thinking》2026-02-27 + SurePrompts《7 Principles》2026-04-12 + GitCodar 2026-06-28 实拉）
原文：Stop saying "think step by step" — with reasoning models, they're already thinking step by step internally. Repeating this instruction is redundant and may interfere with the model's natural reasoning process.；Let the model choose its approach；Use effort as a fallback — control depth via the effort parameter (low/medium/high/max).

- **对推理模型：删掉 step-by-step 与推理脚手架**——推理模型内部已在分步思考，重复指令冗余甚至干扰；预设框架（"用 SWOT 分析"）变成能力天花板。→ 判据：**标准模型要"逼它想"，推理模型要"别挡它想"**——同一句话在两类模型上是相反效果。与 §零样本 CoT 的分工：那条管标准模型上 CoT 的成本权衡（贵 2-30 倍换 15-40% 准确率）；本条管推理模型上的反向纪律（不加脚手架、让模型自选方法）。
- **用 effort 参数控深度，不用文字催**：推理深度用
easoning_effort（low/medium/high）或 thinking budget 调，不靠 prompt 文字催"更仔细地想"。→ 判据：**深度是配置不是修辞**——想改深度改参数，改 prompt 既不可控又占 token。
- 反模式：给推理模型贴"think step by step"（冗余且干扰）；预设分析框架限死模型选择（框架=天花板）；用长篇"请深入思考"文字催深度（应调 effort）。
- **提升层**：提示工程 / 输出（推理 token 管理）。
## 检索上下文排序与预算：top-few 硬预算 + 关键放首尾（lost in the middle）（来源：Levelop《LLM Context Window: What Works in Production》2026-07-30 + ApX《Long Context Management with Large Retrieved Datasets》2026-09-20 实拉）
原文：Set a hard token budget for retrieved context and enforce it；it's often beneficial to place the most relevant documents or text chunks either at the very beginning or the very end of the context（对抗 lost-in-the-middle 效应）。

- **检索内容设硬 token 预算，只留 top few 不是 top fifty**：检索回的块按相关性排，只取前几个，总 token 上限硬执行——demo 与生产的差别就在这里。→ 判据：**检索量的判据是"预算"，不是"相关性排序到多少位"**；超过预算宁可少给，不给到截断。
- **关键内容放上下文开头或结尾**：模型对中间的注意最弱（lost in the middle），最重要的文档/块放最前或最后，对抗注意力衰减。→ 判据：**排序本身是质量杠杆**——同样的内容，放在中段和放首尾效果不同；组装上下文时按重要性排位，不是按检索顺序原样塞。
- 与 §成本四层/上下文预算的分工：那条管"每层怎么省 token"；本条管"检索来的上下文怎么排位、卡多少预算"——省下的 token 要花在最容易被注意到的位置。
- 反模式：检索回 50 块全塞进去（超预算被截断，反而降质量）；按检索分数顺序原样排列（最相关的可能沉在中段）；省 token 时把关键块裁掉。
- **提升层**：工具 / 工作流（检索上下文组装）。
## System prompt 分层预算：identity/capability/behavioral/context 各层容量不同（来源：Blck Alpaca《System Prompts for Agents: 12 Design Patterns》2026-06-09 + Zylos《Prompt Engineering for AI Agent Systems》2026-03-30 实拉）
原文：Identity 50-200 tokens / Capability 800-2,000 tokens（含工具 schema）/ Behavioral 200-600 tokens / Context 100-400 tokens（动态）。

- **system prompt 按四层组织，各层有不同 token 预算**：**identity（角色/领域/边界 50-200）**轻量锚定防角色漂移；**capability（可用工具与何时用 800-2000，含 schema）**是大头但只写"工具做什么、什么时候优先用哪个"，不写实现；**behavioral（输出格式/风格/Never X 200-600）**；**context（日期/用户/活动工作流 100-400）动态变化**。
- **动态层必须放最后且最小**：context 层是唯一每轮变的——与 §Relocation Trick 同源，动态内容放尾部避免污染前缀缓存；budget 上动态层最小化，静态层一次写够。
- 判据：**加 system prompt 内容先问"它属于哪层、这层预算还有没有"**——把工具实现细节塞进 identity 层、把每轮变化塞进 capability 层，都是层错位，既涨 token 又降稳定。
- 与 r140-A §技能三级加载分工：那条管"技能文件怎么分层加载（元数据 100t 常驻/正文按需）"；本条管"system prompt 本体怎么分层分配预算"。
- 反模式：identity 层写成长篇人设；capability 层堆工具调用示例；behavioral 层塞任务上下文；context 层放回静态规则。
- **提升层**：工具 / 可复用 Skill（提示结构预算）。
## 记忆写入时序：先响应后提取，提取用便宜模型，收尾合并 session→global（来源：Ascheriit《AI Memory Systems for Long-Running Agents》2026-07-02 + OpenAI Agents SDK《Context Engineering for Personalization》2026-01-05 实拉）
原文：Extraction adds latency; users should receive the response first；SHOULD use a cheap, fast model for extraction (Haiku, gpt-4o-mini) rather than the primary generation model. Extraction is a classification/parsing task, not a reasoning task；收尾 Consolidate session memories into global memory. Deduplicate overlapping notes. Resolve conflicts using recency wins. Clear session memory so the next run starts clean。

- **记忆提取绝不阻塞用户响应**：提取加延迟，用户应先收到响应——提取放到响应之后异步做。→ 判据：**响应路径和记忆路径是两个通道**，记忆提取不得插入主链路。
- **提取用便宜模型**：提取是分类/解析任务不是推理任务——用 Haiku/gpt-4o-mini 级别，不让生成模型兼职。→ 判据：**任务的"难度定档"先于模型选择**——与 §模型分派"机械执行给便宜模型"同源，记忆提取是典型机械档。
- **收尾合并 session→global：去重 + 冲突 recency wins + 清空 session 下次干净起跑**——形成可重复循环：注入 → 推理 → 蒸馏 → 合并。
- 与 ctx §记忆提取四策略/两级沉淀分工：那条管"**提取什么、什么时候提取**"（策略+校验）；本条管"**提取的时序与成本**"（响应后异步 + 便宜模型 + 收尾合并）。
- 反模式：主模型每次对话边答边存（延迟+贵）；提取塞在主响应前；session 笔记从不合并、越攒越大。
- **提升层**：工作流 / 可复用 Skill（记忆写入时序）。
## 代码库上下文：repo map（AST+PageRank+token 预算）+ launch point 决定可见性（来源：Agent Patterns《Repository Map Pattern》2026-09-15 + 13labs《Codebase Too Big》2026-08-11 + Aider repo map 2026-09-15 实拉，与 §检索上下文排序 互补——那条管"结果怎么排/预算怎么定"，本条管"代码库结构怎么进上下文"）
- **repo map pattern**：tree-sitter 解析出符号（函数/类/方法）+ 调用边与导入边 → **PageRank 算符号重要性**（偏向任务提到的文件）→ **binary-search 把最高排名符号的签名塞进 token 预算** → 每次动作前先读 map 再读代码。→ 判据：**上下文里放"哪些符号存在、怎么连"，不放实现细节**；目录列表/文件样本/关键词 grep 是低信号高浪费。
- **launch point 决定可见性**：从最窄子目录启动 agent（如 packages/api/），加载该目录及其祖先的说明、不加载兄弟包——**"你在哪启动，它就能看见什么"**。
- **显式 file set**：提示词点名涉及的文件，胜过让 agent 自己探索。
- 与 §三级加载（L1 元数据/L2 摘要/L3 按需）合流：repo map 是代码库版的"L1 结构地图"——**先给骨架再按需取肉**。
- 反模式：整个仓库塞进上下文；靠目录树猜依赖；agent 从仓库根启动结果被兄弟包指令污染。
- **提升层**：工具 / 工作流（代码库上下文加载）。
## 工具输出落库指针 + 按需检索召回：大输出不进上下文，进可检索库（来源：GitHub context-mode（Claude Code 上下文治理，2026-06）+ X-CMD 指南 2026-09-07 实拉；与 §脚本输出隔离 互补——那条管"脚本代码永不进上下文只回输出"，本条管"输出比摘要大时怎么办"）
- **原始输出留在沙箱/子进程/本地库，上下文里只放一行指针**：工具输出落 SQLite（FTS5 全文索引），模型需要数据时用 BM25 检索召回命中片段，不是把整份输出塞回。实测工具输出压缩约 98%。
- **会话续接同样走检索**：文件编辑、git 操作、任务状态、错误、用户决策全部写入本地库；会话 compact 后**不把整条历史塞回上下文**，用 FTS5+BM25 只召回与当前问题相关的事件。→ 判据：**"存起来"不等于"塞回去"**——持久化的是可检索库，不是待重放的完整转录；重放整条历史=把压缩省的 token 又花回去。
- **一次批量调用替换多次单步调用**：ctx_batch_execute 一类批处理入口，把 30+ 次工具调用合并为一次调用（结果仍走落库指针）。
- 与 §脚本输出隔离的分工：那条管"代码不进上下文"，本条管"**输出不进上下文但保证可召回**"；输出小→直接回传（走那条），输出大/需要跨轮追溯→落库指针（走本条）。
- 反模式：把大输出摘要后丢进上下文（丢失可召回性）；把落库内容整段重放（token 白省）；只存不建索引（存了也找不到）。
- **提升层**：工具 / 可复用 Skill（输出与上下文的隔离通道）。
## 精简优先的实证：Claude Code 删掉 80% system prompt 而无评估损失（来源：Anthropic Context Engineering Guide（Claude 5 代）2026-07-24 实拉；与 §system prompt 分层预算 互补——那条管"各层给多少预算"，本条管"预算本身该不该这么大"）
- **巨指令块不是能力的来源**：Anthropic 对新一代 Claude 删掉 Claude Code 超过 80% 的 system prompt，评估无可见损失——高绩效 agent 的形态是**精简提示 + 更好工具 + 渐进披露 + 记忆 + 结构化引用**，而不是把行为规则全写进提示词。
- 判据：**新增一条指令前先问"这条能不能由工具描述 / 记忆 / 引用承担"**——提示词里每多一行硬规则，都是对每轮上下文的税；能用结构替代的指令不写进提示词。
- 与 §分层预算的分工：那条管"身份/能力/行为各多少字合适"，本条管"**总量本身要持续瘦身**"——预算分配不解决"预算过大"的问题。
- 反模式：靠堆行为规则提升质量（评估往往无收益还拖慢每轮）；把工具能表达的能力写进 system prompt 重复声明。
- **提升层**：模型 / 工具（提示词瘦身的实证依据）。

## 上下文注入顺序：关键信息放首尾，中间是注意力盲区（来源：Liu et al. 2023《Lost in the Middle》+ 2026 长上下文评测综述（U 型曲线收窄但未消除）2026-07 实拉；与 §只注入相关信息 互补——那条管"注入什么"，本条管"注入的顺序"）
- **注意力呈 U 型**：关键信息在长上下文首尾时召回最好，在中间系统性下降——2026 前沿模型中间凹陷收窄但未消除。**有效上下文不随长度均匀**：塞得进窗口 ≠ 用得起来。
- **注入时主动重排**：把最相关的证据/指令放在开头或结尾，别让关键信息埋在中段；多文档时按相关度排布而非按源顺序。
- 判据：**上下文组装是一次排序决策，不是拼接**——谁放首、谁放尾、谁进中间，直接决定模型能不能用上它；"更多 token 不等于更好答案"。
- 与 §检索排序预算的分工：那条管"召回多少条"，本条管"召回后怎么排进上下文"。
- 反模式：按抓取/拼接顺序原样塞入（关键证据随机落在中段）；把要模型重点处理的指令夹在长文档中间。
- **提升层**：工具 / 工作流（上下文注入质量）。
## 记忆读取按需触发 + 摘要锚点定向：不 always-on 检索，不确定才查（来源：Oblivion《Self-Adaptive Agentic Memory Control》arXiv 2604.00131 + HiGMem arXiv 2604.18349 2026-08 实拉；与 §记忆写入时序 互补——那条管"什么时候写"，本条管"什么时候读"）
- **读路径与写路径分开设计**：读路径根据 **agent 不确定性和记忆缓冲充分性**决定何时查记忆，避免冗余的 always-on 访问；写路径只强化**实际贡献了响应的记忆**（不是全记）。
- **摘要做语义锚点**：先看高层事件摘要，用摘要预测哪些相关轮次值得读，再定向读取那一小簇——比全量向量检索便宜且证据更可靠（HiGMem 实测避免过高检索开销）。
- **遗忘=可及性衰减，不是删除**：记忆控制靠衰减驱动降低可及性（读不到了但还在），而非显式删除——与 r135-C ADD-only 软衰减同源合流。
- 判据：**"每轮都查记忆"和"从不查记忆"一样是错的**——只有"不确定答案/当前缓冲不足"时才触发检索；查之前先看摘要锚点缩小范围。
- 反模式：把全部记忆向量化每轮检索（贵且噪声）；凭感觉随手查（该查不查/不该查乱查）。
- **提升层**：工具 / 工作流（记忆检索成本控制）。

## 上下文作为演化工件：轨迹提炼教训→结构化增量更新，防内容崩溃（来源：ACE《Agentic Context Engineering》ICLR 2026 + Meta Context Engineering arXiv 2601.21557 2026-08 实拉；与 §prompt 版本生命周期 互补——那条管"版本怎么管"，本条管"内容怎么演化"）
- **上下文是"演化剧本"不是一次性写的**：三角色流水线维护——**Generator**（用当前上下文解新问题并留全轨迹）→ **Reflector**（审轨迹，提炼成功实践+失败的具体教训）→ **Curator**（把教训转成**结构化局部增量 deltas** 追加/修改上下文）。
- **增量更新防崩溃**：反复整段重写会让知识丢失、语义漂移；结构化小步追加/修改保留详细知识——"离线（system prompt）和在线（会话上下文）都可以演化"。
- 判据：**教训进上下文要走"提炼→增量"两步，不是把失败原文贴回去**——贴原文=上下文膨胀；提炼成 deltas=知识累积。
- 反模式：跑完任务把整个轨迹写进记忆（膨胀）；每轮整段重写 system prompt（丢失积累）；失败教训不落上下文（下次同错）。
- **提升层**：工具 / 工作流（上下文自我演化）。
## 样例驱动渐进式引导：让 AI 从样例归纳方法论，人只判断对错（来源：WaytoAGI 文章精选·一泽 Eze《样例驱动的渐进式引导法》2026-07-04 实拉；与 §精简优先实证 互补——那条管"提示词总量怎么瘦"，本条管"提示词怎么从样例生成"）
- **不给规则给样例**：把 2-3 个理想输入输出样例交给 AI，让它自己从表象里**归纳出方法论**（逻辑分析+抽象总结），用户只对归纳出的方法做对错判断，零星提意见。
- **迭代回路**：AI 基于用户判断持续反思，总结出更优质的内容生成方法与要求——提示词不是一次写成的，是"样例→归纳→人验收→再归纳"滚出来的。
- 判据：**"从样例反推方法"比"描述想要什么"门槛低**——描述想要什么需要你先想清楚规则，给样例只需要你选出好例子；AI 负责归纳，人只做验收者。
- 反模式：直接要求 AI"写个提示词"（它只能泛泛而谈）；用户逐条教规则（把归纳工作揽回自己身上）。
- **提升层**：可复用 Skill（提示词生成方法）。
## 上下文显式分节标签：系统指令/检索上下文/对话摘要分块标注，不混单块（来源：maraj.ai《Context Engineering Playbook》2026-04 实拉 + agentpatterns.ai《Context Engineering》2026-05 实拉；与 §上下文注入顺序（U 型注意力置首尾）互补——那条管"各块排在哪"，本条管"各块长什么样、怎么标注"）
- **完整上下文按显式、带标签的节组织**：[SYSTEM INSTRUCTIONS]（身份/行为/约束）、[RETRIEVED CONTEXT]（按相关度排序的文档）、[CONVERSATION SUMMARY]（历史摘要）——**不要把系统指令、检索内容、对话历史混进一个无区分的大块**。
- **分节的价值在可定位与可隔离**：模型能区分"这是规则、这是材料、这是历史"，检索注入与对话历史不会淹没指令；后续新增上下文往对应节里放，不重排其他节。
- **每节内部再排序**：检索节内部按相关度从高到低，最关键的放节首——分节解决"混在一起"，排序解决"节内先后"。
- 判据：**上下文组装先分节再排序**——分节是结构决策（哪些信息类别该有独立身份），排序是顺序决策（同节内谁先谁后）；两者独立可调。
- 反模式：全上下文一个大 prompt 块（模型无法区分规则与材料）；给检索节也塞对话历史（隔离失效）。
- **提升层**：工作流 / 可复用 Skill（上下文组装结构）。
## 技能加载会话快照：清单会话内定格，变更才刷新（来源：OpenClaw 官方 docs.openclaw.ai·	ools/skills，2026-09 实拉；与 §只注入相关信息 分工——那条管"每轮注入多少"，本条管"技能清单多久重扫一次"）
- **session 启动时快照 eligible skills 列表，整个 session 复用**：不会每轮重新扫描全部技能——**技能清单是会话级常量，不是每轮变量**。
- **仅两类事件触发 mid-session 刷新**：① 某个 SKILL.md 文件被修改（watcher 检测）；② 新的 eligible remote node 接入。刷新后的列表**下一 turn 生效**，不打断当前 turn。
- 判据：**清单定格省的是"反复重扫"的固定成本；变更触发保的是"改完能立刻用上"**——两件事拆开：不因省重扫而错过更新，也不因怕错过更新而每轮重扫。
- 反模式：每轮都重扫全部技能（把固定成本变成每轮成本）；或反过来整个会话死锁旧清单（改了 SKILL.md 也不刷新）。
- **提升层**：工作流（技能加载成本控制）。

## 第三方技能选型三判据：安装量/来源信誉/源仓库热度（来源：skills.sh ercel-labs/skills/find-skills，2026-04 实拉；与 WB ctx 工具面安全分工——那个管"装完怎么防注入"（审 description/同名拦截），本条管"装之前先筛掉低质量的"）
- **装任何第三方 skill 前先过三键**：① **安装量**——1K+ 安装优先，<100 要谨慎（几乎没人用的东西多半有坑）；② **来源信誉**——官方源（vercel-labs/anthropics/microsoft 等）> 未知作者，作者维度先于内容维度；③ **源仓库热度**——回查源仓库 stars/维护活跃度，README 与 issue 是真实质量信号。
- **三键是过滤器不是证明**：三键全绿只说明"值得进一步看内容"，不替代内容审查（SKILL.md/脚本逐行读、测跑）；三键任一红则默认不装。
- 判据：**先筛"值不值得看"，再谈"内容安不安全"**——把质量门槛前置到选择阶段，而不是装上后才发现是垃圾。
- 反模式：看见 description 诱人就装（标题党）；只看 stars 不看作者（刷星仓库）；装了之后才发现缺维护/有坑（选择阶段没筛）。
- **提升层**：工作流 / 可复用 Skill（技能引入门槛）。
## 注入出口检测两法：canary 被动证据 + LLM 主动检测器（来源：rapidclaw《Prompt Injection Defense 2026 Playbook》+ Zylos《Defensive Prompt Engineering for Multi-Tool AI Agents》2026-05 实拉；与 WB ctx 工具面安全分工——那个管"入口防注入"（预检清单/审 description），本条管"出口抓已成功的外泄"）
- **canary token（被动证据，零成本）**：在 system prompt 埋一个唯一、不可猜的字符串，它没有任何正当理由出现在输出、工具调用参数或外发网络请求里——一旦出现，就是**成功外泄的证明**，即使攻击本身是全新的。它把检测问题从"识别所有攻击载荷"（不可能）变成"识别这一个字符串"（平凡）。
- **LLM 检测器（主动拦截）**：用独立 LLM 当注入检测器审输入，AgentDojo 基准实测（GPT-4o/o4-mini 作检测器）误报/漏报 <1%，移除被检注入后下游攻击成功率 <1%。检测器只审不执行，与被检 agent 模型隔离。
- 判据：**canary 抓"已经漏了"，检测器抓"正在进来"**——两者互补不替代；canary 成本≈0 常驻，检测器只在敏感入口启用（有额外延迟成本）。
- 反模式：只装检测器不埋 canary（新攻击载荷检测器可能认不出，没有任何兜底证据）；或只埋 canary 不设入口过滤（漏进来已发生，只能事后证明）。
- **提升层**：工具 / 可复用 Skill（安全面）。

## 主张级可审计四维（deep research 引用的可审计标准）：来源覆盖/来源健全/矛盾透明/审计成本（来源：arXiv 2602.13855《From Fluent to Verifiable: Claim-Level Auditability for Deep Research Agents》2026-09 实拉；与 ED 引用纪律分工——那个管"引用必须真实可查"，本条管"报告产出怎么证明每条主张都有出处"）
- **主张级（claim-level）可审计，不是段落级**：报告里每条事实性主张单独挂来源——"这条结论由哪几条来源支持"可逐条回答。
- **四维测量**：① **provenance coverage**（多少主张有来源覆盖——没覆盖的裸主张是首要风险）；② **provenance soundness**（来源真的支持该主张吗——有来源但不相干的比没来源更误导）；③ **contradiction transparency**（来源间矛盾是否显式标出，而不是挑一边藏一边）；④ **audit effort**（第三方核验这份报告要花多少力气——审计成本是报告质量的一部分）。
- 判据：**"有引用"不等于"可审计"**——引用存在只满足第一维；全部主张能逐条回答"谁支持、支持什么、有没有矛盾、核验要多快"才叫可审计。
- 反模式：报告末尾堆参考文献但正文主张找不到对应条目；来源与主张相关性靠感觉；来源间打架时不标冲突；核验需要重跑整个研究过程。
- **提升层**：工作流 / 可复用 Skill（研究报告产出标准）。
## 技能开发两实例迭代闭环：基线→最小草稿→实测→精修（来源：SkillsMP 实拉 zebbern/agent-skills-authoring 转述 Anthropic 推荐模式，2026-09-17 实拉；与 §样例驱动渐进式引导分工——那条管"提示词怎么从样例生成"，本条管"技能开发怎么闭环迭代"）
- **先建无 skill 基线**：让 agent 在**没有该技能**的情况下跑代表任务，记录真实缺口——不先看缺口就写技能=凭印象写。
- **写最小草稿**：只写足以补上观测到缺口的最少内容，不一次写全（技能是迭代产物，不是一次成型文档）。
- **第二实例实测**：用全新 agent 实例加载草稿技能，跑 2-3 个真实 prompt，观察它卡在哪、漏掉哪条指令——新实例没有作者心证，才能暴露"只有作者懂、指令没传达"的缺口。
- **回改再扩**：把实测观察带回给作者实例精修，满意后才扩大测试集。
- 判据：**"作者觉得写清楚了"不等于"陌生实例能用"**——必须跨实例验证指令传达；基线对照区分"技能补的"与"模型本来就会的"。
- 反模式：不测基线直接写；一次写全凭想象补缺口；只在作者自己的会话里自测。
- **提升层**：可复用 Skill（技能迭代开发流程）。

## 运行时工具集稳定性纪律：不中途换工具/模型，用工具模拟状态迁移，延迟加载而非删除（来源：Claude 官方博客 claude.com/blog《Lessons from building Claude Code: Prompt caching is everything》2026-04-30 实拉；与 §不可变前缀 互补——那条管"字节级前缀稳定"（缓存布局面），本条管"会话运行时工具/模型集合不变"（调用面））
原文：Don't change tools or models mid-conversation. Use tools to model state transitions (like plan mode) rather than changing the tool set. Defer tool loading instead of removing tools.
- **工具/模型中途不变更**：换工具或换模型 = 前缀失效 + 行为漂移——缓存前缀按字节匹配，运行时换任何一个成员，其下整段缓存作废。→ 判据：**会话开头定死的工具集与模型，中途不加不减**；要变能力靠追加新工具（前缀末尾追加不破坏既有缓存），不替换旧工具。
- **用工具模拟状态迁移，不换工具集**：要表达"进入计划模式/只读模式"这类状态变化，用**工具/开关表达状态**（如 plan mode 切换），而不是换一套工具——状态是会话内的变量，工具集是会话内的常量。
- **延迟加载而非删除**：暂时用不上的工具**推迟加载**而不是从清单里删掉——删除会改变工具列表（前缀+每次调用的 schema 都变）；推迟加载让清单保持稳定。
- 与 §技能加载会话快照的分工：那条管"技能清单多久重扫一次"；本条管"工具/模型集合在会话内怎么保持不变"。
- 反模式：中途把工具 A 换成工具 B（前缀失效 + 模型行为重学）；用"换工具"表达状态变化；临场删工具省 token（省的是边际、赔的是整段缓存）。
- **提升层**：工具 / 工作流（缓存友好的运行时纪律）。

## 缓存命中率当 uptime 监控：缓存破坏按事故告警，fork/分支共享父前缀（来源：Claude 官方博客《Prompt caching is everything》2026-04-30 + developersdigest《Prompt Caching in the Claude API: A Production Guide》2026-04-29 实拉；与 §保持轮次流动防缓存过期 互补——那条管"停顿超 TTL 缓存清零"（时间面），本条管"命中率观测告警 + 分支共享"（运维面））
原文：Monitor your cache hit rate like you monitor uptime. We alert on cache breaks and treat them as incidents. A few percentage points of cache miss rate can dramatically affect cost and latency. Fork operations need to share the parent's prefix.
- **缓存命中率是运行时指标，不是一次性优化结果**：改完提示结构后**持续盯命中率**——几个百分点的 miss 率就会显著推高成本与延迟；缓存破坏（cache break）按**事故**处理（告警+定位），不当作"偶尔掉一下"。→ 判据：**命中率下降先找"谁动了前缀"**，而不是先怀疑模型或网络。
- **fork/分支操作必须共享父前缀**：并行分支/子任务复制父会话时，**共享父级前缀**（复用已缓存部分），不从头重建——否则每个分支都重付一遍缓存写入。
- **break-even 判据**：前缀在 5 分钟内被复用 >1-2 次就值得缓存；>2k token 的稳定内容（system prompt/技能说明）随每次调用发出是显性收益。→ 判据：**先问"这段前缀复不复用、多久内复用"，再决定要不要为它布缓存**。
- 与 §不可变前缀的分工：那条管"布局怎么摆"（静态前动态后）；本条管"摆完之后怎么盯"（命中率+告警）+ 分支共享。
- 反模式：优化完命中率就不再回看；缓存掉点不去定位直接调模型；每个并行分支从头 prefill。
- **提升层**：工作流（成本观测与告警）。

## 工具返回字段裁剪：工具只回 LLM 需要的字段，非完整 API JSON（来源：n8n Community 实测帖《Each tool you attach to an AI Agent node is re-billed every turn》2026-07-24 实拉；与 §脚本输出隔离/落库指针 互补——那条管"输出不进上下文或转移存储"，本条管"输出内容从源头瘦身（字段级）"）
原文：Instead of returning complete API responses, our tools now return only the fields the LLM needs (for example, property_name, price, and availability instead of the full JSON). That alone cut thousands of tokens over the course of a run.；Each agent only receives the tools it actually needs, which noticeably reduced prompt size and improved tool selection.
- **工具响应在源头裁剪到所需字段**：工具写返回时只给 LLM 要用的那几列（property_name/price/availability），不给完整 JSON——实测一次运行省数千 token。→ 判据：**"这段返回模型要读哪几个字段"先于"把结果原样回传"**；能在工具层裁，就不让模型在上下文里裁。
- **每个 agent 只挂它实际需要的工具**：工具定义每轮都计费（与 §成本分型边际项同源），少挂一个少一份每轮开销，还改善工具选择（工具少，模型选对概率高）。
- 与 §同一份结果两个消费方分工：那条管"给模型的短、给程序的全，两路分开"；本条管"**给模型的那路，内容本身按字段裁剪**"——裁的是字段不是视图。
- 反模式：工具把整表/整个 API 响应回传，让模型在上下文里挑；agent 挂满所有可用工具；裁到连判断必需的上下文都丢。
- **提升层**：工具 / 工作流（输出侧 token 节省）。

## 按需装载工具/能力 + 缓存安全的节奏提醒：上下文要"省"也要"不忘"（来源：Pydantic AI on-demand capabilities / tool-search / system-reminders，2026-09-27 实拉）
- **按需装载，不预付全部 schema**：工具/能力默认只给模型一个**单行目录条目**，具体指令与 schema **只在被实际调用时才拉进上下文**——大量工具的 agent 只为用到的工具付 token（与 §工具返回字段裁剪 同一方向：那条管"返回的体积"，本条管"工具定义本身的体积"）。判据：**工具越多，越不能把所有 schema 常驻**；能搜索/延迟加载就别全量注入。
- **长任务用节奏提醒对抗指令遗忘，且不破坏缓存**：系统提醒按**节奏或条件**重新注入（如"你忘了最初的约束吗"），实现上必须 **cache-safe**（不移动已缓存前缀），否则提醒一来把整段前缀缓存打崩、反而更贵。判据：**长运行里"重要指令会不会被冲掉"是独立风险，不能靠一次性 system prompt 解决**；但重注方式必须保证不 bust 缓存。
- 与 §记忆 token 分层 分工：那条管"常驻量硬预算与按需装载历史"，本条管"工具定义的按需装载"与"运行中指令保活"。
- 提升层：工具（按需装载）/ 工作流（指令保活）。

## 工具循环的 O(n²) 隐藏账单：每步重放全量历史→固定窗口截断回 O(n)，且要故意为之（来源：dev.to/wartzarbee《smolagents replays its whole memory every step: the O(n²) token bill nobody mentions》2026-08-25 实拉；与 §记忆 token 分层/上下文预算 互补——那条管"常驻量硬预算与按需装载"，本条管"工具循环每步重放的成本机制"）
原文：This turns the input curve from quadratic back toward linear: a fixed window of history instead of an ever-growing one. You trade some long-range recall for a bounded bill — for most tool-loop tasks that is the right trade, and you make it deliberately instead of discovering it on an invoice.
- **工具循环每步重放全量历史 = O(n²) 隐藏账单**：多步工具循环里，第 k 步的输入=前 k-1 步全部历史，总输入量是 n² 量级——没人提，但账单上一直在涨。→ 判据：**长工具循环先算"步数 × 每步累计历史"的总量**，而不是只看单步。
- **固定窗口截断把曲线拉回线性**：上下文只保留最近 N 步（fixed window），丢远距召回换有界账单——多数工具循环任务这是对的取舍。→ 判据：**"故意截断"和"在账单上发现"是两件事**——截断窗口是主动决策，不是等到发票才被迫。
- **其他杠杆按钝度排序**：先降 max_steps（默认 20 太高，游走 run 能悄悄跑满）→ 再截窗口 → 再换便宜模型。
- 与 §工具返回字段裁剪的分工：那条管"每次返回的体积"（单步瘦身），本条管"**步与步之间历史怎么累积**"（多步总量）。
- 反模式：几十步工具循环全量重放历史；等账单爆炸才想到截断；把 max_steps 当不用管的默认值。
- **提升层**：工作流 / 工具（工具循环成本机制）。

## RAG 检索的时效与顺序：先去重后检索 + 时间戳过滤陈旧上下文；提示漂移用类别清单 + 模式解析兜底（来源：Make 官方 make.com/en/how-to-guides/llm-integration《How to build an LLM integration》2026-09-23 实拉；与 §检索上下文排序预算 分工——那条管"召回多少条、放哪"，本条管"检索的时序与数据新鲜度"）
原文：Stale context: retrieval module read outdated CRM state. Fix by moving retrieval after deduplication or adding a timestamp filter.；Malformed output: prompt drift returns prose instead of structured fields. Fix with a stricter category list and a Text Parser > Match Pattern fallback.

- **陈旧上下文是独立失败类，不归"召回质量"管**：检索模块读到的是过期数据（旧 CRM 状态）——检索本身没错，错在**检索发生在数据变化之前**。→ 判据：**先问"这次检索读的是不是最新状态"再问"召回准不准"**；数据变更/去重操作排在检索之前，或给检索加时间戳过滤。
- **提示漂移（返回散文而非结构化字段）的修复顺序**：先**收紧类别清单**（枚举范围更严），再挂**模式解析兜底**（Match Pattern fallback）——不是只改提示词措辞。→ 判据：**结构化输出失效时，"更严的枚举"是规则层修复，"模式解析"是解析层兜底**，两层都要，只改语气是无效修复。
- 与 §结构化输出两态判据 的分工：那条管"怎么判输出对不对"（验证面）；本条管"**输出变回散文时用什么修**"（修复面）。
- 反模式：检索永远排在写操作后仍读到旧值（忘了加时间戳过滤）；提示词漂移后只改 prompt 措辞（不收紧枚举也不加解析兜底）；把陈旧上下文当成召回质量问题重做 embedding。
- **提升层**：工作流（RAG 时效与输出修复）。

## 人机路由的过升级治理：收紧置信阈值 + 补边界示例，不是加规则（来源：Make 官方 make.com/en/blog/agentic-process-automation《What is agentic process automation》2026-09-23 实拉；与 wb-execute-discipline §换挡检测分工——那条管"能力不足时换模型"，本条管"把人机路由边界送人太频繁怎么调"）
原文：Over-escalation: the agent routes too many edge cases to humans. Fix by tightening your confidence threshold and adding clearer boundary examples.

- **过升级是路由问题不是能力问题**：agent 把太多边界 case 交给人工——路由边界太松，不是它"不会做"。→ 判据：**送人太频繁先调阈值与边界示例，不急着换模型**——换模型修不了"该不该送人"。
- **修复是两件事：收紧置信阈值 + 补清晰边界示例**：阈值管"多自信才算能自主"，边界示例管"哪些案例明确该自主/该送人"——示例让阈值有锚点，阈值让示例可执行。→ 判据：**只调阈值不补示例=阈值没有参照物；只补示例不调阈值=示例不落地**。
- 与 §答案分档 的分工：那条管"输出的轻重档"（给用户什么）；本条管"**任务去留人机谁做**"（路由给谁）。
- 反模式：边界 case 送人多就写更多规则（膨胀且难维护）；只调阈值不补边界示例（误伤正常自主）；把过升级误判为模型能力不足去换强模型。
- **提升层**：工作流（人机路由边界）。

## 模型迁移收尾三清单：集成测试 / 长度控制提示词调优 / 成本-限流重基线化（来源：Claude API skill 官方 platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill，2026-09-23 实拉；与 §换挡顺序分工——那条管"降档过程怎么回归"，本条管"迁移完成后的收尾交付物"）
原文：As it edits, the skill explains each change and its motivation inline. On completion, it produces a checklist of items that require manual verification (typically integration tests, length-control prompt tuning, and cost/rate-limit re-baselining).

- **模型迁移完成 ≠ 可以上线**：迁移动作做完后收尾**必须产出需人工核验的清单**——具名三类：① **集成测试**（真实链路跑通）② **长度控制提示词调优**（新模型输出长度特性变了，长/短控制要重调）③ **成本与限流重基线化**（价格、速率上限全变了，原预算与限流假设作废）。→ 判据：**迁移报告结尾必须有"待人工核验项"清单**，没有=迁移只做了一半。
- **每处修改行内说明动机，不攒到最后解释**：迁移中每个改动当场说明"为什么这么改"——收尾清单只管"还要人验什么"，动机解释在改的时候给。→ 判据：**行内动机 + 收尾清单是两段**，前者防无动机改动，后者防"以为改完就能上"。
- 与 §可自检追问的分工：那条管"给用户的实质性答案后附具体追问"；本条管"**模型迁移这类工程动作的收尾核验**"——核验对象不同（用户决策 vs 工程迁移）。
- 反模式：迁移完直接宣布完成（跳过了集成测试/调优/重基线）；改动不解释动机攒到最后；清单只写"请验证"不具名三类项。
- **提升层**：工作流（模型迁移收尾）。

## 技能触发评测配比规格：20 条 queries 8-10/8-10、每条跑 3 次算触发率、基线对比含 token 用量（来源：agentskills.io 官方规格 agentskills.io/skill.md，2026-09-23 实拉；与 wb-skill-authoring §caliper 闭合邻域分工——那条管"竞争集封闭/两方向计分"（原理面），本条补"具体配比与重复次数"（操作面））
原文：Test triggering — Create 20 eval queries (8-10 should-trigger, 8-10 should-not-trigger) with varied phrasing, explicitness, and complexity. Run each query 3 times and compute trigger rates. 8. Test output quality — Run 2-3 test cases with the skill and without it (baseline). Grade outputs against assertions. Compare pass rates and token usage.

- **触发评测给固定配比**：20 条 eval queries——8-10 条应触发 + 8-10 条不应触发，措辞/显式度/复杂度都要有变体（防"只有一种问法能触发"）。→ 判据：**触发测试两方向都要覆盖，且各占约一半**；只测"该触发能触发"测不出抢活。
- **每条 query 跑 3 次再算触发率**：单次触发/不触发是噪声，3 次算率才有统计意义。→ 判据：**触发率=每条 3 次的重现率**，不是"20 条里命中几条"。
- **输出质量=带技能 vs 无技能基线的对比，且比两样：通过率 + token 用量**：各跑 2-3 个用例，按 assertions 评分；技能既补能力又省 token 才算合格。→ 判据：**基线对比要同时看质量与成本两维**——只提升质量但烧 token 翻倍，不是合格技能。
- 与 §技能两实例迭代闭环 的分工：那条管"开发怎么闭环"（基线→草稿→实测→回改）；本条管"**闭环里的评测具体怎么配数**"（20 条配比/3 次重复/双维对比）。
- 反模式：只写 5 条"该触发"的 query 测触发；每条只跑一次就当结果；输出质量测试不做无技能基线；只看通过率不看 token 用量。
- **提升层**：可复用 Skill（技能评测规格）。

## 记忆按业务主体（actor）归属，能力随调用携带（来源：n8n 官方 blog.n8n.io/node-spotlight-amazon-bedrock-agentcore《Build multi-agent teams that remember every customer with Amazon Bedrock AgentCore》2026-09-23 实拉；与 ctx §记忆分层分工——那条管"记忆怎么分层（core/recall/archival）"，本条管"记忆按什么归属、能力怎么分发"）
原文：AgentCore's Managed memory is scoped by actor and session, so an Actor ID that identifies the customer rather than any single agent gives every specialist the same history to read and write, and that history outlives an individual workflow execution. And because the tools, skills, model, and instructions travel with each invocation rather than being fixed on a deployed agent, one agent can serve all four specialists instead of provisioning four.

- **记忆作用域=业务主体（actor）×session，不是 agent 实例**：用 Actor ID（识别客户/用户）而非单个 agent 作记忆归属——同一客户的所有专家读写同一份历史，历史**活过单次 workflow 执行**。→ 判据：**问"这段记忆属于谁"而不是"属于哪个 agent"**——按 agent 分记忆，客户跨专家换人后记忆就断了。
- **能力随调用携带，不固定在部署上**：tools/skills/model/instructions 每次 invocation 一起走——一个 agent 实例可服务多个角色，不用每个角色各部署一个。→ 判据：**"角色"是调用参数不是部署单元**——多角色共享一份部署，省的是部署面（与 §成本四层工作切分同源）。
- 与 §记忆写入时序的分工：那条管"什么时候写"（响应后异步+便宜模型）；本条管"**写给谁、谁有权读**"（作用域）。
- 反模式：按 agent 实例分记忆（客户跨 agent 就失忆）；每个角色部署一个 agent（重复部署面）；记忆不过 session（历史活不过单次执行）。
- **提升层**：工作流（多 agent 记忆作用域）。

## durable execution：父休眠子继续、崩溃不级联（来源：n8n 官方 blog.n8n.io/long-running-agents-beyond-prompt-engineering 2026-09-23 实拉；与 ctx §交接文档四要素分工——那条管"上下文怎么交接"，本条管"执行怎么耐久"）
原文：Sub-agents get this same durability on their own terms. Each child has its own state, schedules, durable fibers, and lifecycle, and stores its own data colocated under the parent. The property that matters for durability is that the parent doesn't have to stay active while the child works. It can start the work, hibernate, and be woken when the child's schedule or recovery check fires. A crash doesn't take down the whole family at once; each identity...

- **耐久的关键性质：父不必保持活跃**：父发起子任务后可休眠，子按自己的 schedule/recovery check 独立跑，完成后唤醒父。→ 判据：**"父要一直在线等子"是脆弱设计**——长时子任务让父休眠、靠子完成/恢复事件唤醒。
- **每个子 agent 独立生命周期与持久状态**：state/schedules/durable fibers 各自持有，数据 colocated under parent。→ 判据：**状态与调度是子级资源，不挂在父进程里**——父重启不丢子的状态。
- **崩溃隔离：一个倒下不连带全家**：每个 identity 独立恢复。→ 判据：**故障域=单个子 agent**——设计时问"这个子挂了，其他人和父怎么办"，答案不该是"一起挂"。
- 与 §上下文作为演化工件的分工：那条管"内容怎么演化"（Generator/Reflector/Curator）；本条管"**执行过程怎么活下来**"（耐久性）。
- 反模式：父进程全程盯着子跑；子状态存在父进程里（父一挂全没）；单个子崩溃拖垮全家；长时任务无恢复检查点。
- **提升层**：工作流（长时 agent 耐久性）。

## 输出校验参数化：最终答案校验器 + 每步前后状态日志（来源：smolagents DeepWiki 配置表 2026-08-29 + Dify 官方 enterprise-docs Agent Strategy Plugin 2026-07-15 实拉；与 wb-execute-discipline §步骤间质检-回退分工——那条管"每步之间过质检函数"，本条管"最终答案专用校验参数 + 每步前后成对记状态"）
原文（smolagents）：Quality assurance: final_answer_checks=[validator_func]；Per-step type callbacks: step_callbacks={ActionStep: [cb1], PlanningStep: [cb2]}。原文（Dify）：Complex tasks usually take multiple steps, and you need to track each step's result to analyze decisions and refine your strategy. The SDK's create_log_message and finish_log_message let you record state before and after each call, which speeds up problem diagnosis.

- **最终答案校验器是框架一等参数，不是流程外约定**：`final_answer_checks=[validator_func]`——把"最后这坨输出对不对"做成可配置钩子，agent 完成时自动过校验。→ 判据：**"收尾校验"要有独立于每步质检的专用钩子**——每步质检防"走偏"，final check 防"走完了但答案是错的"。
- **每步前后状态成对记录**：调用前 create_log_message（起始状态）、调用后 finish_log_message（完成状态）——诊断"哪一步决策错了"靠前后对照，不是事后猜。→ 判据：**复杂多步任务每步留"前状态+后状态"**，与 §留痕只存元数据 分工：那条管"存什么字段"，本条管"**前后成对的形态**"。
- **按步类型注册回调**：ActionStep 和 PlanningStep 各挂各的回调，动作问题与规划问题分开观察。→ 判据：**回调按步类型分挂**——混在一个回调里，动作噪声淹没规划问题。
- 与 §可自检追问的分工：那条管"给用户的答案后附追问"（人侧）；本条管"**agent 输出的机器侧校验**"（自动化）。
- 反模式：只做每步质检不做最终答案校验（错答案走完流程才被发现）；日志只记结果不记调用前状态（决策错了无从对照）；所有步类型共用一个回调。
- **提升层**：工具（输出校验与可诊断性参数）。

## harness 全能力插件化：循环/调度/存储/UI 也是插件（来源：DeepSeek Harness 官方 deepseek.com/harness/en 2026-09-23 实拉；与 §技能模块化分工——那条管"技能层可组合"，本条把 harness 级能力纳入插件面）
原文：Every capability is a plugin that can be swapped or recomposed: models, tools, skills, sessions, sandboxes, storage, loops, scheduling, and the UI.；Plugins provide every agent capability, including models, tools, skills, sessions, sandboxes, storage, loops...

- **插件化的范围不止工具与技能**：模型/工具/技能/会话/沙箱/存储/**循环（agent loop）**/**调度**/UI 全部可替换重组——连"agent 怎么跑循环"都是可换的。→ 判据：**"可组合"要覆盖执行机制本身**，不只是功能模块——想换循环策略/调度器/存储后端时，不该动核心。
- **插件三件套契约**：defineTool{name + description + parameters schema} + output.schema + render——工具声明与渲染分离，输出结构可程序消费。→ 判据：**插件的输入（parameters schema）与输出（output.schema）都结构化**，机器才能编排（与 §工具返回字段裁剪同源）。
- **社区插件的分发形态**：GitHub topic（如 `dsh-plugin`）即插件市场，自然语言装/卸。→ 判据：**插件发现走主题标签 + 声明式安装**，不靠手工拷贝目录。
- 与 §第三方技能选型三判据的分工：那条管"装之前怎么筛"（安装量/信誉/热度）；本条管"**harness 能力边界在哪、插件长什么样**"（形态）。
- 反模式：只有工具能换、循环/调度写死；工具输出结构不声明（模型只能猜）；插件市场靠手工搬运。
- **提升层**：工具（可组合架构理念）。

## 长输入编排：文档置顶、query 置底（来源：Anthropic 官方 prompting best-practices Long context tips，platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices 2026-09-23 实拉；与 §上下文注入顺序分工——那条管"U 型注意力关键放首尾"（排位原理），本条管"大输入的具体摆法"（长数据置顶+query 置底））
原文：For working with large documents or data-rich inputs (>20k tokens), structure your prompt carefully: Place long data near the top of the prompt, above the query, instructions, and examples. This improves performance across all models. Queries at the end can improve response quality.

- **超 20k tokens 时：长数据放顶部、query 放底部**：文档/长输入放最前（在 query、instructions、examples 之上），查询句放最后——官方称全模型性能提升、末尾 query 改善响应质量。→ 判据：**大输入的组装顺序 = 长数据(顶) → 指令/示例(中) → query(底)**，不是按"先问题后材料"的自然顺序。
- **与检索排序的分工**：检索排序管"多块之间谁先谁后"（相关度）；本条管"**大文档整体 vs 指令 vs 查询的三大块位置**"——层次不同，都做。
- **与缓存布局的兼容**：长数据置顶与"静态前置动态后置"不冲突——文档是静态可缓存部分，query 是每轮动态部分，两者恰好各占一端。
- 反模式：把 query 放最前、文档堆后面（模型读到 query 时还没看到材料，且长材料在中段被注意力弱区吃掉）；指令夹在长文档中间。
- **提升层**：提示工程 / 工作流（长输入编排）。

## 规则文件 200 行上限 + 按路径作用域拆分（来源：Claude Code Advanced Patterns 官方 PDF《Claude Code Advanced Patterns: Subagents, MCP, and Scaling to Real Codebases》2026-09-23 实拉；与 wb-doc-writing §膨胀是症状分工——那条管"术语表删到 lean 再拆"（内容面），本条管"指令/规则文件的规模上限与按路径作用域"（治理面））
原文：Keep files < 200 lines. Longer files consume more context and can negatively affect instruction adherence.；Organize instructions into multiple files using the .claude/rules/ directory. Rules can also be scoped to specific file paths.

- **指令文件 <200 行是硬上限**：超过 200 行的文件既耗更多上下文，又**降低指令遵从**（越长遵从越差）——不是"内容多所以长"，是"长度本身伤害遵从"。→ 判据：**规则文件超过 200 行先拆，不靠"内容都重要"辩护**。
- **按路径作用域组织多文件规则**：用 .claude/rules/ 目录把指令拆进多个文件，并**按文件路径作用域**（某规则只对某目录/某类文件生效）——拆 + 作用域，不是只拆不加约束。→ 判据：**规则文件的组织单位是"路径+场景"**，不是"主题清单堆一起"。
- 与 §技能三级加载的分工：那条管"技能文件元数据/正文/资源分层"；本条管"**规则文件的规模与作用域**"——技能文件是"怎么加载"，规则文件是"多大、管哪片"。
- 反模式：CLAUDE.md/规则文件越写越长（遵从度悄悄下降）；把所有规则堆一个文件"图省事"；拆分后没有路径作用域（拆了还是每轮全量读）。
- **提升层**：可复用 Skill（指令文件治理）。

## 实现后独立评审子代理：不带实现上下文（来源：Claude 官方博客 claude.com/blog/subagents-in-claude-code 2026-09-23 实拉；与 wb-execute-discipline §步骤间质检-回退分工——那条管"每步之间过质检函数"（过程面），本条管"复杂实现完成后用无实现上下文的评审者"（收尾面））
原文：Independent review. After implementing something complex, verification from a subagent that hasn't been influenced by the implementation journey catches what familiarity obscures. The review subagent evaluates the code without knowing what tradeoffs were considered, what approaches were rejected, or what assumptions were made.

- **评审者必须与实现者信息隔离**：评审子代理**不知道**考虑过哪些 tradeoff、拒绝了哪些方案、作了哪些假设——不带实现旅程的旁观视角，专抓熟悉性盲区。→ 判据：**评审前问"这个评审者知道实现过程吗"**——知道得越多，评审越接近自查。
- **复杂实现完成后必做独立评审**：实现越复杂，实现者越被自己的路径锚定——独立评审不是可选的质量提升，是收尾步骤。→ 判据：**"实现者自评通过"不替代独立评审**——自评带熟悉性偏差。
- 与 §输出校验参数化 的分工：那条管"最终答案机器校验器"（规则/断言）；本条管"**人类视角的独立评审者**"（信息隔离）。
- 反模式：让实现者自己评审自己的代码（锚定效应）；评审子代理带着实现的完整上下文（等于没隔离）；小改动也全套独立评审（成本不匹配）。
- **提升层**：工作流（实现后独立评审）。

## 代码执行 import 白名单：默认最小集 + 显式声明（来源：HF smolagents 官方 hf.co/blog/smolagents + noqta.tn 2026-09-23 实拉；与 §脚本输出隔离分工——那条管"代码不进上下文只回输出"（上下文面），本条管"生成代码能 import 什么"（执行面））
原文：By default the interpreter blocks all imports except a small allowlist (math, statistics, datetime). Anything your tools rely on must be declared explicitly — this is what keeps generated code safe. (additional_authorized_imports)

- **默认拦截全部 import，只留最小白名单**：解释器默认只允许 math/statistics/datetime——生成代码想用别的库必须显式声明。→ 判据：**代码执行环境的依赖面是"默认禁 + 显式开"**，不是"默认全开再拦"。
- **工具依赖的包显式声明（additional_authorized_imports）**：agent 写代码调用工具所需的库时，把包名列进白名单——安全与能力之间是显式授权关系。→ 判据：**"代码能 import 什么"是配置不是约定**——靠 prompt 叮嘱"别乱 import"不可靠，白名单是执行层强制。
- 与 §工具面安全（WB ctx 侧）的分工：那条管"工具描述注入/同名拦截"（工具面）；本条管"**代码 agent 生成的代码本身的 import 面**"（代码执行面）。
- 反模式：代码执行环境全开 import（生成代码可以偷跑任意库）；靠提示词约束代码行为（执行层没拦，约束是纸的）；工具依赖不声明（运行时才发现缺库）。
- **提升层**：工具（代码执行安全）。

## 记忆摄取打分门控 + NO_INGEST 显式拒绝（来源：LangFlow 官方 docs.langflow.org/next/memory-bases 2026-09-23 实拉；与 ctx §记忆提取四策略分工——那条管"按类型提取+校验"，本条管"摄取前打分名单与显式拒绝协议"）
原文：Durable preferences (tools, formats, constraints) / Active projects and milestones (goals, deadlines, multi-step work)；The batch has zero value if it consists entirely of: Transactional tech noise (stack traces, syntax-only debugging) / Conversational filler ("thanks", "got it") / Stale re-statements of facts already established；If the total score is 0, respond with exactly: NO_INGEST

- **摄取前打分：正面两类 + 负面三类**：值得长期存的只有**持久偏好**（工具/格式/约束）与**进行中项目**（目标/截止/多步工作）；**事务性技术噪声**（堆栈、纯语法调试）、**对话填充**、**已有事实的陈旧重述**一律零值。→ 判据：**"要不要存"不是感觉，是打分**——候选片段先过名单，三类噪声直接判死。
- **总分 0 显式返回 NO_INGEST**：拒绝入库要有显式信号，不是静默跳过——可审计"这条为什么没进记忆"。→ 判据：**零值摄取与静默丢弃的区别，是留不留拒绝痕迹**。
- **陈旧重述单独列零值类**：已有事实再被重复说一遍不是新记忆——防长期记忆被同义反复灌水。→ 判据：**"重复入库"与"新信息入库"要分开判**，后者才值得打正分。
- 与 §记忆 token 分层分工：那条管"常驻/可搜/按需三层的预算"；本条管"**进这些层之前，内容先过打分门**"。
- 反模式：对话里什么都往长期记忆塞（噪声灌水）；拒绝入库时静默（审计时说不清）；把陈旧重述当新记忆存（长期记忆全是重复）。
- **提升层**：工作流（记忆摄取门控）。

## 远端 MCP 多用户隔离透传：external-user-id（来源：Pipedream 官方 pipedream.com remote MCP 2026-09-23 实拉；与 ctx §per-tool 最小权限分工——那条管"单个工具的权限面"，本条管"远端 MCP 出口按用户隔离"）
原文：await client.connect({ url: "https://remote.mcp.pipedream.net", headers: { "x-pd-external-user-id": "sarah@acme.com" } })；Your agent picks the tool — auth is already handled

- **一个远端 MCP endpoint 服务多用户，靠 external-user-id 透传身份**：agent 发起 callTool 时带上用户 ID，平台按用户隔离上下文与权限。→ 判据：**多用户共用一个 MCP endpoint 时，用户身份要在请求头显式透传**，不是靠会话偶然隔离。
- **auth 托管在平台侧**：连接已处理认证，agent 只选工具不碰凭据。→ 判据：**接第三方 API 时把 auth 托管给平台/网关**，agent 侧不持有凭据（与 §脚本输出隔离同源：凭据不进上下文）。
- 个人用法：自建 agent 通过一个 remote MCP 接入大量 API，auth 免管、用户级隔离免实现。
- 反模式：多用户共用一个 MCP 端点而不透传用户 ID（上下文/权限互相串）；agent 侧自己存各平台凭据（暴露面）；每个用户各部署一个 MCP server（重复面）。
- **提升层**：工具（远端 MCP 接入形态）。

## Skill 编排的字段映射是关键步：先声明 schema，再显式对接（来源：腾讯云《用 AI Skills 搭可复现最佳实践：从 0 到发布》cloud.tencent.cn/developer/article/2728515 2026-08-19 实拉；与 harness §插件三件套分工——那条管"插件自己声明输入输出结构"，本条管"两个 Skill 之间怎么对接"）
原文：编排：把 Skill 串进你的 Agent 工作流（触发条件、调用顺序）；字段映射：明确 Skill 的输入/输出字段怎么接（最关键，详见第四节）；导出：结果落盘或回传；人工复核：留出人工确认环节，别全信自动输出。这 7 步里，3/4/5 最关键。

- **多 Skill 编排的 7 步里，字段映射单独点名最易错**：装 → 编排（触发条件/调用顺序）→ **字段映射（输入/输出字段怎么接）** → 导出 → 复核；3/4/5 最关键。→ 判据：**接两个 Skill 时先写"上游输出字段 → 下游输入字段"的映射表**，不是直接塞整份输出。
- **先声明 schema，再显式对接**：每个 Skill 的输入输出结构先声明（插件三件套），对接时按字段名映射、做类型匹配检查。→ 判据：**"能跑通"不等于"字段接对了"**——字段映射是编排里最便宜、最隐蔽的错误源。
- **人工复核留环节**：结果落盘/回传前留人工确认，不全信自动输出（与 §独立评审分工：那条管复杂实现，本条管 Skill 链式输出）。
- 反模式：两个 Skill 串接时把上游整份输出塞给下游（字段错位靠模型猜）；不做映射表（改一个 Skill 就断链）；自动输出直接外发无复核。
- **提升层**：工作流 / 可复用 Skill（多 Skill 集成）。

## Agent 成本熔断 + 一键回滚链（来源：数数科技《大模型 Agent 平台落地：从 POC 到生产》2026-07-30 实拉；与 §成本可观测性分工——那条管"三通道分开看"（观测），本条管"预算上限+自动熔断"（拦截）；与 §质检-回退分工——那条管"步骤间重试"，本条管"整系统回滚到无模型链"）
原文：设置任务级、用户级的 Token 上限和自动熔断策略，避免异常调用导致计费失控；预设人工介入触发器和一键回滚方案，当模型准确率低于阈值或出现严重幻觉时，可及时退回至规则引擎或人工处理。

- **Token 上限要分任务级 + 用户级两层，且自动熔断**：预算超限不是告警等处理，是自动拦截——防一次异常调用把整月预算烧掉。→ 判据：**上限要落在执行路径上（超了停），不是落在监控面板上（超了看）**。
- **人工介入触发器 + 一键回滚是预设方案**：模型准确率低于阈值 / 严重幻觉时，一键退回**规则引擎或人工**——降级目标不是"换个模型"，是"回到没有模型的确定性链路"。→ 判据：**写降级方案先问"回滚到哪"**——规则引擎/人工是可落地的回滚目标，换模型只是变体。
- 与 §过升级治理的分工：那条管"送人太频繁怎么调阈值"；本条管"**触发条件满足后怎么回滚**"——一个管路由边界，一个管降级动作。
- 反模式：只有监控没有熔断（烧完才知道）；降级方案写"交给模型再试一次"（不是回滚是死循环）；回滚无预设目标（临时想退哪）。
- **提升层**：工作流（成本熔断与降级回滚）。

## 动作敏感记忆五要素：记忆记的不是事实，是行为条件（来源：OpenClaw 官方 docs.openclaw.ai/concepts/memory 2026-09-23 实拉；与 ctx §记忆提取四策略分工——那条管"提取什么+校验"，本条管"存下来的内容必须回答哪五问"）
原文：A useful action-sensitive memory makes clear: what changes future behavior / when or under what condition it applies / when it expires, or what unlocks action / what the agent should avoid doing / who is the source or owner, if that affects trust or authority.

- **记忆内容要能回答五问**：**改变什么未来行为** / **何时或何条件生效** / **何时过期或什么解锁动作** / **该避免什么动作** / **来源或所有者是谁（影响信任与权限）**——记不下五问的记忆是"事实堆"，不是"行为指导"。→ 判据：**写记忆前先问"这条会改变我下次的哪个行为"**；答不出的不进长期记忆。
- **过期与解锁是记忆的显式字段**：记忆要写"何时失效"或"什么条件满足后解锁动作"——不写过期条件，记忆会在不该生效时永远生效。→ 判据：**带条件的记忆必须带过期/解锁条件**，与 §记忆读写按需触发（衰减）分工：衰减管"读不到"，过期管"不该生效"。
- **来源权属影响执行**：记忆标注来源/所有者——来自谁影响信任与授权级别。→ 判据：**记忆不是无主信息**，权限敏感的记忆必须带所有者。
- 反模式：长期记忆记"世界是圆的"式无行为含义的事实；带条件规则不写过期；记忆不标来源导致越权执行。
- **提升层**：工作流（记忆内容规格）。

## 子代理 prompt 完整自足：只有 prompt+CLAUDE.md，不许占位符（来源：GitHub Consortium-team/project-creator CAPABILITY.md 2026-04-26 实拉；与 r151-A §独立评审分工——那条管"评审者不带实现上下文"（信息隔离面），本条管"隔离的后果：prompt 必须自足"（书写面））
原文：A subagent gets ONLY its prompt plus CLAUDE.md — no conversation history, no parent skills, no accumulated context. This isolation is both the strength and the constraint. Because subagents have no conversation context, every value they need must be in the prompt. Never pass placeholder values like [PATH_TO_FILE].

- **子代理的隔离是双刃：没有历史 = prompt 必须完整自足**：子代理拿不到对话历史/父技能/累积上下文——它需要的一切值都必须写进 prompt。→ 判据：**写子代理任务时逐项检查"它需要的每个值是不是都在 prompt 里"**——有依赖对话上下文的，要么写进去，要么不拆。
- **禁止占位符**：`[PATH_TO_FILE]` 这类占位符对没有上下文的子代理是空值——不是提醒，是缺失。→ 判据：**占位符=漏传参数**；子代理任务里不允许出现未解析的方括号占位。
- 与 §独立评审的分工：那条保证"评审者不知道实现细节"；本条保证"**子代理知道它该知道的一切**"——隔离的两面。
- 反模式：给子代理传 `[文件路径]` 占位符期望它自己找；子代理任务依赖父上下文里的信息没写全；拆子任务却不提供它需要的完整输入。
- **提升层**：可复用 Skill / 工作流（子代理任务书写法）。

## 子代理输出原样透传：父默认会转述，要原文须显式指令（来源：growthengineer.ai Claude Agent SDK Subagents 2026-05-04 实拉；与 §同一份结果两个消费方分工——那条管"模型版/程序版双视图"，本条管"子代理产出交付用户时防父转述失真"）
原文：If you need verbatim subagent output to reach the end user without parent paraphrasing, add an explicit instruction in the main query() system prompt: "When you receive Agent tool results, pass them through unchanged."

- **父代理把子代理结果当工具结果处理，默认会压缩/转述**：子代理返回的原文经过父，父会按自己的输出习惯改写——需要原文直达到用户时，必须显式声明。→ 判据：**"子代理原文要直达用户"是例外不是默认**，默认父转述；需要原文就在主 prompt 加"pass them through unchanged"。
- **原样透传是一条显式指令，不是靠"父别多嘴"的叮嘱**：写进主 query() system prompt 才稳定生效。→ 判据：**透传要求要进系统指令层**，与 §可自检追问分工：那条管"父对用户的追问"，本条管"子产出的保真交付"。
- 反模式：需要子代理原文却任由父转述（细节失真）；期望父自动透传不写指令（行为不稳定）；把转述当"优化"（丢的是子代理的精确输出）。
- **提升层**：工作流（多级输出交付）。

## 插件安装 10 项安全评测清单（来源：DeepSeek Harness 官方插件评测指南 agentpedia.codes 2026-08-14 实拉；与 ctx §per-tool 最小权限分工——那条管"工具权限面"，本条管"装插件前的完整安全评测协议"）
原文：Pin a package version or commit / Run on a disposable host and repository / Use synthetic secrets and data / Start with Minimal mode / Deny outbound network access by default / Review every plugin source before installation / Add external approval for mutations / Capture and inspect trajectories / Compare modes with a fixed task set / Maintain a rollback path and delete preview data after evaluation.

- **装任何插件前过 10 项勾选清单**：① 钉版本/commit（复现锚点）② 一次性主机与仓库（隔离实验）③ 合成密钥与数据（不泄真凭据）④ 最小模式起步（能力最小面）⑤ **默认拒绝出网**（网络最小面）⑥ 逐源审代码（不只看描述）⑦ 变更需外部审批（变更=权限动作）⑧ 捕获并检查轨迹（可审计）⑨ 固定任务集对比模式（同基线比较）⑩ 保留回滚路径并删预览数据（评测后可退）。→ 判据：**"装插件"按"上权限"的流程审**——每装一个都是爆炸半径+1（与 ctx 工具面安全同源），10 项里"默认拒绝出网/合成密钥/外部审批变更/回滚路径"是执行硬项。
- **hot-path 纪律**：高级插件只经文档化扩展缝注册、不改 agent-loop 骨架（零可测开销）。→ 判据：**插件不动核心骨架，只走扩展缝**（与 §harness 全插件化分工：那条管"插件长什么样"，本条管"装之前怎么验、装之后怎么保持骨架干净"）。
- 反模式：装了再看代码（评测在装之后=已生效）；实验用真凭据真数据（泄露面）；插件能自由出网（数据外泄通道）；评测完不删预览数据不保留回滚路径。
- **提升层**：工具 / 工作流（插件安全评测协议）。


## 汇报是产品不是流水账：给决策所需的最小充分面，状态卡只发一次（来源：Smashing Magazine 2026-05-13 agentic update 公式 + InstitutePM 2026-06-01 动态清单 + Zylos 2026-07-01 post-once-update-in-place + CSDN 2026-09-21 agent UI 七模式，2026-09-24 豆包 r159-A 实拉取证，同轮 WB 审计独点属实后落地）
- **★一条状态更新 = 动作词 + 具体对象 + 约束边界**：不要写"正在检查可用性"，要写"正在查您日历 3 月 14 日下午 2 到 4 点的空闲，且遵守团队 45 分钟会议的规则"。判据：**用户判断要不要打断你，靠的是"你在动哪个对象、受什么约束"**，动作词本身不提供这个信息。
- **★进度用"可折叠时间线 + 每一步的置信信号"，不是一串日志**：每一步都带一个把握程度，高把握自动继续，低把握主动交给人。判据：**把所有步骤平铺成同等重要的列表，等于让用户自己去猜哪一步有风险**。
- **★同一件事只发一张卡，状态变化原地更新**：任务开始发一张状态卡，之后改动这张卡，真正完成时才发一条新通知。判据：**状态刷屏会淹没真正的完成通知**——"更新"和"完成"必须视觉上不同。
- **★请求批准时，你的职责是给最清晰的情况说明，不是推销某个结论**：说明里要有对象、改动前后差异、所需权限、以及**能不能撤销**；执行之前**再验一次对象与权限**。判据：**把批准画面写成"建议点同意"，就把决策所需的差异信息藏起来了**；批准人要能一眼看出"改的是不是我以为的那个东西"。
-  与 §进度流与诊断流分开（若已存在）分工：那条管**汇报内容的分渠**；本条管**呈现格式与节奏**。


## 推理模型成本三纪律：thinking 也计费 / caching 静默失败 / router 按盈亏平衡（来源：Anthropic 官方 extended-thinking + octomind 2026-09-18 + theneuralbase/channel.tel/syncsoft 实拉，2026-09-24）

- **Thinking 也是计费面，不是免费内部琢磨**：开 extended thinking 后 thinking tokens 按 output 计费（即使不返回给用户）；上一轮 thinking block 进下一轮上下文按 input 计费，多轮 agent 里会滚雪球。Claude 4.6+ 手动 budget_tokens 已 deprecated，用 adaptive（模型自己决定 thinking 多久）。判据：多轮 agent 记账时 thinking 别漏算。
- **Prompt caching 失败是静默的**：cache miss 不报错不警告，响应一模一样——大多数团队从没拿到缓存折扣不是功能没开，是 prefix 结构不对。结构纪律=稳定 system/工具定义在前、动态用户输入在后；Anthropic 写缓存 1.25x(5min)/2x(1h)，hit rate 不够时写缓存反而亏钱；必须主动测 hit rate，别等账单。
- **Reasoning router 按盈亏平衡选，不按越难越好**：reasoning 比 standard 贵 10-50 倍——路由阈值=错误代价×概率 是否超过 reasoning 溢价；状态查询/简单 lookup/聊天 UX（用户>3s 就走）用 reasoning 纯浪费；reasoning 超 latency budget 自动回退 fast model，不让用户干等；纯关键词路由会漂移，监控被路由到 reasoning 的请求真受益了吗，季度重训。
- **提升层**：输出 / 成本工程。

## Qoder 净新（2026-09-27 · 全量消化）
- **按实测费用记账，不按 token 数**（实测：编排式双模型 token +70%、交互轮数 ~3x、费用反降 36%）——"花 token ≠ 花钱"，token 预算若以 token 数为唯一口径会系统性误判；跨调用**只传定向简报与部分结果、不传完整对话日志**是拿到缓存折扣（读缓存约 1/10 价）的前置条件，压缩的成本收益要按费用口径算。
## 工具定义的上下文预算：可见工具 30-50 起衰减；defer 必须留非延迟锚点（来源：Anthropic 官方 MCP / advanced tool use 数字与 Claude 开发者文档，经 toolrouter.com《Too Many MCP Tools Make the Assistant Worse》+ startdebugging.net 2026-05 + mcpplaygroundonline 三处交叉复述，2026-09-27 r206-A 独立实拉；与 §按需装载工具/能力 互补——那条管「要不要按需装载」（机制面），本条管「装多少算超、超了怎么切」（量化面））
- **开场即烧的税**：五 server 58 工具约 55,000 tokens 在你说第一句话前就付掉；换 tool search 后降到约 8.7K（-85%）。判据：**工具清单不是资产清单，是每轮都要付的租金；连了不用 = 白付。**
- **衰减阈值 30-50**：可见工具超过 30-50 个，选工具准确率开始掉——同任务实测 Opus 4 从 49% 到 74%、Opus 4.5 从 79.5% 到 88.1%（减少可见工具不是省钱妥协，是同时更准）。
- **不能全 defer**：搜索工具自身 + 至少一个工具必须保持非延迟，否则 API 直接 400（All tools have defer_loading set）。判据：**留 2-3 个高频工具常驻，长尾全部延迟。**
- **alwaysLoad 只给小面高频 server**：大 server 恰恰是最该延迟的那个——「每轮都用」是唯一豁免理由，不是「怕搜不到」。
- **输出侧同样在预算内**：MCP 工具输出 >10,000 tokens 告警、25,000 封顶；返回「最小有用结果 + has_more」永远优于「最全结果」。判据：**一次无界查询吃掉的量，可以超过你辛苦省下的全部工具定义。**

## 成本与基础设施簇（细则已下沉）
- 完整细则见 references/knowledge-base.md「成本与基础设施簇」；正文只保留触发线索与结论：成本四层、Relocation Trick、路由阈值学习、Q4_K_M 量化、KV 亲和性、Batch 50% 折扣、两阶段模型路由。

## 提醒/追问型输出要写死次数上限 + 负面清单（来源：anthropics discernment-nudge 2026-09-28 r313-Q-A 实拉 + r279-C 复核；与 wb-skill-authoring §提醒类技能触发上限 并条）
- **判据**：凡"每轮补一句建议/核查提示"型输出（去 AI 味提醒、防跑偏提示、落地提醒）**写死一个次数上限**（如每会话最多一次），并把"什么时候不提醒"作为同等篇幅的独立章节——没有负面清单的提醒会随对话变长退化为噪音，持续降信任且不计入 token 预算，无法被现有预算机制拦截。
- 提升层：输出。触发词：提醒上限、追问噪音、负面清单、once per conversation。

## 治理档位要成对出现，且「续活」必须区分交互写与非交互写；压缩要有损失准入门（来源：docs.openclaw.ai`/gateway/config-agents/sessions` 与 `/reference/memory-config` 2026-09-28 r283-C 独立 curl 实拉逐句核验）
- **实证**：① 会话保留告一组档位——`pruneAfter 30d` / `archiveDashboardAfter 7d` / `maxEntries 5000` / `maxDiskBytes 10gb` / `highWaterBytes = 80% of maxDiskBytes` / `coldStorage.afterDays 30`，且 "`reset` … `none` disables automatic reset and is the default"、`daily` 按 `atHour`、`idle` 按 `idleMinutes`，"When both configured, **whichever expires first wins**"。② **续活判据原文**："Daily reset freshness uses the session row's **`sessionStartedAt`**; idle reset freshness uses **`lastInteractionAt`**. Background/system-event writes such as **heartbeat, cron wakeups, exec notifications, and gateway bookkeeping can update `updatedAt`, but they do not keep daily/idle sessions fresh**."③ **压缩的损失门**：`phases.deep.maxPriorEntryLossFraction` 默认 `0.25`，原文释义 "**Reject** consolidation or append compaction that removes more than this fraction of prior entries"；同组还有 `maxPromotedSnippetTokens 160`。
- **判据**：① **清理策略不能只有一种执行力**——凡是会删东西的自动化，都要提供"只报不删"与"到线才删"两档，否则无法先观察再下手。② **自动任务会把自己永久保活**：心跳/定时/后台记账虽然更新了时间戳，但按官方口径**不算续活**——判定活跃度时必须区分"用户交互写"与"系统非交互写"，否则清理规则永远等不到该清理的对象。③ **压缩必须有事前损失门**：不是压完再测召回率，而是**先算出会丢掉的比例，超限直接 reject 本次压缩**（与 r203 已落的"压缩反证召回率"互补：一个是事前门、一个是事后测）。
- 提升层：工作流。触发词：只报不删、到线才删、highWaterBytes、pruneAfter、心跳不算续活、lastInteractionAt、压缩损失门、0.25 reject、压缩 reject。

## 成本账按「时长 × 内存档位 × 段数」归因，并显式列出豁免项与是否结转（来源：pipedream.com/docs/pricing.md 2026-09-28 r283-C 独立 curl 实拉全文核验；续 mts 1.51.0「按实测费用记账不按 token」）
- **实证**：原文 "Pipedream charges **one credit per 30 seconds of compute time at 256MB of memory (the default) per workflow segment**"；"**Unlike some other platforms, Pipedream does not charge for usage based on the number of steps**"；"Credits are not charged for workflows during **development or testing**"、"If an active workflow isn't executed in a billing period **no credit usage is incurred**"；内存 "increase credit usage in **intervals of 256MB**"，官方对照表：256MB 下线性 1 秒＝1 credit、15 秒＝1、35 秒＝2、延迟前后各 15 秒＝**2**、分支三段＝**3**；换成 **1GB 同样的流程＝4 / 4 / 8 / 8 / 24** credits。**另有一条反向豁免**：事件源触发时 "the **source execution is included for free**"（限 public registry 源，私有源照算）。
- **判据**：mts 1.51.0 说"按实测费用记账"，但没给**费用的构成式**。本条给出三因子（**时长 × 内存档位 × 段数**）与两类豁免（开发测试执行、周期内未运行）和一条反向免费项。**关键推论**：分支与延迟都按段叠加计费 → 同样总耗时的流程，**切几段、走几条分支直接决定账单**，与栈内的"少调几次"不是一回事；而"每隔多久轮询一次"这种空跑，只要没有实际调用就不计费。
- **落地动作**：给 agent 或脚本估成本时，估的是 `段数 × ceil(时长/单位) × 档位倍数`，不是调用次数；同时把"开发/测试运行"与"源触发"这类免费项从账单里显式剔除，避免为不存在的开销做优化。
- 提升层：工作流。触发词：credits、30 秒一段、256MB 一档、按段计费、不按步数、开发测试不计费、源执行免费、结转、成本构成式。

## 激活决策要后置一次：检索命中 ≠ 真的需要它（来源：arXiv 2609.26863 SkillApt，2026-09-29 经 Qoder r321-Q-C 实拉取证；**WB 未独立复核，按引文落地并标注待复核**）
- 后置激活＝技能被检索到之后、进入上下文之前再判一次是否真要用：实测准确率 0.838 与 BM25 Top-1 **持平**，但**激活率 100%→31.5%、token 省 74.3%**。
- 与 SA 3.39.0（清单预算＝上下文 1%、削 description）和 §工具定义预算（1.49.0）**不同层**：那两条削"目录/描述"占位，本条削"正文激活"占位（正文才是大头）。
- 与 SA §技能激活位驱逐（ADK `max_active_skills` 上限 + LRU）分工：那条管已激活集合的驱逐，本条管进入集合前的准入。


## 分页契约三要素：整名 + 游标 + 按工具结果预算切页，绝不返回半个文件名（来源：docs.openclaw.ai《What gets sandboxed》2026-09-29 r288-A 独立 curl 实拉原文核验）
- 原文：目录发现返回 "whole, JSON-quoted names and a filename cursor when another page is available… Each page fits the selected model's tool-result budget; **no partial filename is returned**."
- 判据：① **截断必须落在条目边界上，不能落在条目内部**——返回半个文件名会被下游当完整名拼路径，是静默错路（比报错贵）；② 有续页必须回游标（`after`），让调用方用同参数 + 游标继续，而不是让它猜下一页；③ 页大小按**当前模型的工具结果预算**自适应，不是写死条数。
- 与 §工具定义上下文预算（1.49.0）分工：那条算工具**定义**占多少，本条管工具**结果**切几页、每页多大。
- 提升层：工具。触发词：分页、游标、after、整名、半个文件名、工具结果预算、按预算切页。

## r308A 视觉 token 预算管理（来源：theneuralbase budget-management 2026-04-23 + ai-tldr 2026-06-12 + token0 + dev.to Gemini 经济学 2026-08-06 实拉）
- **视觉 token 是独立预算维度**：图片成本由（1）分辨率（2）detail setting（3）格式（4）感兴趣区域决定——**加倍分辨率可能 4-8x 成本，不能当文本 token 算**；按 token 估算图前先查该 provider 的 tiling 逻辑。
- **tile-optimized resize**：OpenAI 把图切 512x512 块，1280x720→4 tiles（765 tokens）；调整到最优 tile 边界→2 tiles（425 tokens）**省 44% 零质量损失**；关键词分类器提前分流可省 3-13x/图；Gemini 定制 768px 管线同理。
- **分辨率物理阈值**：patch 覆盖 28px 而需读字母 8px 高→细节被抹掉；小文本在低分辨率下消失——**省 token 有极限，缩到可读性阈值以下就是质量事故**。
- **自适应预算**：E-AdaPrune 用奇异值谱能量决定 token 预算（信息密集场景多 token、冗余激进压缩）；PromPrune 平衡局部显著性保持与全局覆盖。
- 判据：**图像按 tile 边界与目标字符大小缩放，不是按"看起来清晰"缩放——token 与可读性在此交汇；视觉 token 单独记账单独预算，混进文本预算会静默超支**。
- **提升层**：可复用 Skill（多模态成本治理）。 > 注：末两章（工具 schema 按需注入与缓存成本纪律 / Prompt 压缩技法与成本感知优化）原文已下沉至 references/knowledge-base.md，按标题检索。
