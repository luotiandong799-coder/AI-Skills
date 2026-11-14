---
name: ci-context
description: 上下文工程与预算（Context Intelligence）。当任务涉及长上下文压缩、token 预算与窗口退化、提示缓存（prompt caching）命中率、多 agent 上下文隔离与缓存税、把必须每次成立的约束放进确定性 hook 而非 advisory context、"上下文够不够/会不会静默丢规则"的判断、注意力预算的架构根因、干扰项与结构连贯性对准确率的影响、压缩不可逆与窗口外可查询上下文对象、标称窗口与有效上下文长度的区分、长上下文基准族各自证明不了什么、以及评估顺序与配置误判时使用。是 13 模块中 CI 的载体。
version: 1.4.0
module: CI
modules: CI
---

# CI · 上下文工程与预算（Context Intelligence）

> 本技能是 13 模块中 **CI（上下文智能）** 的载体。完整经验日志在 D 盘：`D:\腾讯AI\WorkBuddy数据\module-memory\CI\MEMORY.md`。关联子技能（长期默认运行）：`defaults/wb-context-compressor`、`defaults/wb-max-token-saver`、`defaults/wb-ponytail`。

## 一、核心认知

- 有效上下文窗口是任务复杂度的函数，非标称容量：检索类可扛几千 token，排序 / 摘要类 400–1200 即崩；退化静默无报错（实测 ~40% fill 开始跳过旧规则）⇒ 预算须显式告警、按最重操作测窗口。
- 规则上限按条数不按行数：~200 条 ceiling（system prompt 已占 ~50），超出后遵守率约 70% 且与文件长度无关；**必须每次成立的约束放确定性 hook 而非 advisory context file**；规则增退役成对。

## 二、触发与协作

- 何时加载：长上下文任务开工前估预算；调 prompt caching 命中率异常时；要不要把某规则改成 hook 时；多 agent 并发设计缓存策略时。
- 与 EI（执行）：预算约束影响计划拆解粒度；与 OI（编排）：缓存税是 agent 调度成本项。

## 三、窗口退化与规则上限方法论（实拉 r710A，2026-11-08）

> 来源：`dotex.org/epic/meta-programming/context-engineering` 一手 WebFetch；arXiv 2602.11988 经 dotex 回读原文（p=.87 / +20% cost）。

- **（r710A-1）窗口是任务复杂度的函数**：检索类可扛几千 token，排序 / 摘要类 400–1200 即崩；退化**静默无报错**（实测 40% fill 开始跳过旧规则）。⇒ 预算须显式告警，且按"最重操作"测窗口，不能只看平均。
- **（r710A-2）规则上限按条数不按行数**：~200 条 ceiling（system prompt 已占 ~50），超出后遵守率约 70% 且与文件长度无关。⇒ 必须每次成立的约束放**确定性 hook**而非 advisory context file；规则增 / 退役**成对**进行，避免 orphan。
- **（r710A-3）多 agent 隔离自带 cache tax**：14 子代理 700K cache_create / 0 cache_read，TTL 5 分钟、缓存键含 model id。⇒ 并发须贴近 TTL 窗口、顺序管线共享上下文落成文件、换模型即缓存清零。

## 四、提示缓存方法论（实拉 r715B，2026-11-08）

> 来源：OpenAI 官方 `platform.openai.com/docs/guides/prompt-caching`（Cloudflare 拦，3 独立域交叉补足）+ aiwiki 厂商表；intuitionlabs 2026-09 五家定价表；落地 `defaults/wb-max-token-saver/references/knowledge-base.md` §r715B-1/2/3 → 1.102.0。

- **（r715B-1）缓存键 = 渲染后的完整前缀**：不是用户可见提示词。隐藏 system 指令、tools 定义与顺序、`parallel_tool_calls`、`text.format` schema、`reasoning.effort`、`context_management` 压缩都参与匹配，任一变化自断点后失配。⇒ 排查 miss 先查**不可见渲染层**。
- **（r715B-2）最小可缓存长度按模型档位分裂**：GPT-5.6+ 1024 / 更老 2048，隐藏 system 内容不计入门槛，命中按 128-token 增量。⇒ "请求总长够" ≠ "可缓存前缀够"——整体超阈值但稳定前缀不足仍 `cached_tokens=0`；同一应用跨型号升级会静默改变可缓存性，参数族须标型号与日期。
- **（r715B-3）缓存是三档计费不是开关**：写 1.25x / 读 0.1x / 未读未写原价，一写一读 1.35x vs 2x、一写九读 2.15x vs 10x；每请求最多 4 写断点、读回溯最近 50 断点取最长匹配、TTL 30m 从写入或复用起算且刷新不另收费。`cache_write_tokens` 高而 `cached_tokens` 低 = 断点前混入变化内容的可机检信号。

## 五、注意力预算的架构根因与上下文可恢复性（实拉 r732C，2026-11-11）

> 来源：Anthropic 官方《Effective context engineering for AI agents》（`anthropic.com/engineering/effective-context-engineering-for-ai-agents`，WebFetch 200 全文逐字）；Anthropic 官方《Scaling Managed Agents: Decoupling the brain from the hands》（WebFetch 200 全文逐字）；Chroma《Context Rot: How Increasing Input Tokens Impacts LLM Performance》（Kelly Hong / Anton Troynikov / Jeff Huber，2025-07-14）经 13labs.au / masterprompting.net / qatronic.com / adroit.io 四独立域交叉回读；Liu et al.《Lost in the Middle》TACL 2024 经 13labs.au 逐字引用。

- **（r732C-1）退化是连续梯度不是悬崖，根因在 n² 注意力与训练分布**：Anthropic 逐字 "This results in **n² pairwise relationships** for n tokens"、"models develop their attention patterns from training data distributions where **shorter sequences are typically more common** than longer ones"、"These factors create a **performance gradient rather than a hard cliff**"。⇒ "窗口没满"**不构成**继续堆料的理由：每引入一个 token 都在消耗有限的 attention budget（"Every new token introduced depletes this budget by some amount"），收益递减先于容量上限出现。目标是 "the **smallest possible** set of high-signal tokens"，且官方明确 "minimal does not necessarily mean short" ⇒ 判据是**信号密度**不是字符数；调参顺序为先最大召回、再按失败模式提精度（compaction prompt 亦然）。与 §三 r710A 分工：那条给"按最重操作测窗口"的工程口径，本条给为什么会这样 + 为什么不能等告警才动手。
- **（r732C-2）干扰项比噪声更毒，结构连贯反而更差；位置效应是任务依赖不可照抄**：Chroma 在固定任务复杂度、只加无关内容的 18 模型实验里，单个 **topically-related distractor** 即把表现压到 needle-only 基线之下、四个复合加剧；低 needle-question 相似度随长度退化更快；**"shuffled haystacks did better across all 18 models"**（结构连贯的噪声反而更抢注意力）；11 个 needle 位置**无显著变化**，与《Lost in the Middle》多文档 QA 的 U 型曲线结论并列 ⇒ 位置效应依赖任务类型，"把关键放首尾"是**待验证假设不是通用定律**，须在本域跑位置探针。⇒ 检索 top-20 不是 20 条证据，而是 1 条答案 + 19 个近似干扰；裁剪动作应按"与问题语义相似度"筛掉近义命中，而非按长度截断。LongMemEval 306 prompts 全量 ~113k tokens vs 聚焦 ~300 tokens，所有模型聚焦版更好 ⇒ **包装形状与信息量同等重要**。
- **（r732C-3）压缩是不可逆决定，正解是把上下文做成窗口外的可查询对象**：Anthropic 逐字 "the standard ways to address this all involve **irreversible decisions** about what to keep"、"It is difficult to know which tokens the future turns will need"、"these are **recoverable only if they are stored**"。Managed Agents 把 context 从"窗口内容"改为**持久化的 session log 对象**，`getEvents()` 让 brain 按位置切片、回退若干事件看前因、重读特定动作前的上下文；harness 负责变换（含为 prompt cache 命中率做重排），**存储与变换分离**——理由是不能预测未来模型需要哪种上下文工程。⇒ 压缩前先把原始轨迹落盘可检索，压缩产物只是**视图**而非唯一真相；验收问"被压掉的内容还能按位置取回吗"。同一架构解耦 brain/hands 后 p50 TTFT 降约 60%、p95 降超 90%（不得混同为压缩收益）。与 §一「必须每次成立的约束放 hook」互补：那条防规则静默丢失，本条防原始上下文不可逆丢失。

## 六、工具面上下文压力先按来源分四路，别把四种手段当四个开关（CI · r738B 2026-11-11 实拉，四独立域交叉）

前几节处理"窗口里装什么"（注意力预算、干扰项、压缩可逆性）。工具面是另一条独立压力源：工具定义与累积的 `tool_result` 块在任务开始**之前**就在占窗口。Claude 官方把这一面拆成四条互不替代的路径，选哪条取决于 token 去了哪里，不是"全开更好"。

- **（r738B-1）四种手段各减一样东西，组合前先定位压力源**。官方逐字表：Tool search → "Tool definitions loaded upfront"，适合 "Many tools (10+), most of which aren't needed every turn"；Programmatic tool calling → "`tool_result` roundtrips"，适合 "Chains of tool calls that can run as a single script"；Prompt caching → "Token cost of repeated tool definitions"，适合 "Stable tool definitions across many requests"；Context editing → "Old `tool_result` blocks in history"，适合 "Long conversations where early results are no longer relevant"。官方结论："each approach targets a different source of context pressure" / "Pick the one that matches where your tokens are going."。判据：① 工具定义膨胀 ≠ 工具结果堆积，减前者用 defer、减后者用脚本化或旧结果裁剪，混用会"开了但没省到地方"；② 组合允许（"You can use these approaches together, because each solves a different part of the problem"），但起步顺序按瓶颈来，不是一次全上。
- **（r738B-2）缓存不减少上下文，只减少重复付费；与 §四的计费口径互补不重复**。官方逐字："Prompt caching doesn't reduce the number of tokens in context, but it reduces what you pay for them on subsequent requests."；"Cache writes carry a 25 percent markup over base input pricing, which pays back on the second request that hits the cache." ⇒ 把 cached_tokens 上升读成"窗口压力下降"是口径错：窗口里那批工具定义仍在，退化风险（§五 n² 梯度、干扰项）一分未减。判据：① 报上下文健康度时把"占窗口的 token 数"与"计费 token 数"分两栏；② 工具集大而**固定**才是缓存主场，工具集频繁变动要回到 r715B 的渲染前缀失配问题；③ 10 个工具以下、每轮都要用全，别为了省基线引入额外一轮检索。
- **（r738B-3）省上下文要付延迟，脚本化改变的是"中间结果进不进历史"**。官方逐字："This trades a small amount of latency (one extra turn to look up a tool) for a large reduction in baseline context usage."；程序化调用把多次 `tool_use`/`tool_result` 往返折叠成一段在沙箱里跑的脚本，"The intermediate results never enter the conversation history."。判据：① 工具搜索的收益要用"基线占用下降"减"多一轮的时延"来算，低延迟交互场景不必然划算；② 判断该不该脚本化，看的是"中间结果有没有资格进历史"，不是"调用次数多不多"；③ 旧结果裁剪是不可逆动作，与 §五 r732C 的正解配套：裁剪前先把原始轨迹存成窗口外可查询对象。

**判非（重要）**：`defer_loading` / `Tool Search Tool` / `Programmatic Tool Calling` / `Tool Use Examples` 的**机制本体**已由豆包自留地学过（`defaults/wb-max-token-saver/references/knowledge-base.md` §788 r206-A 可见工具衰减量化、`defaults/wb-ponytail/references/knowledge-base.md` §193 Tool Use Examples、`engineering/wb-execute-discipline/KB` §7467/10225/13478 tool_choice 与 programmatic 判据），WB **0 落地**这些文件、不复述机制数字（134K / 8.7K / 85% / 49%→74% 均不搬）。本轮只取官方《Manage tool context》一页的**分流判据**：四压力源、缓存不减窗口 token、延迟代价、按瓶颈起步。窄串 `25 percent markup` / `10 or more tools` / `one extra turn` / `four approaches` / `context pressure` 全库 0 命中（本批机检）。

## 七、来源

- dotex.org/epic/meta-programming/context-engineering（窗口退化 / 规则上限）
- arXiv 2602.11988（规则上限 ~200 条 ceiling，回读原文）
- OpenAI 官方 prompt-caching 文档 + aiwiki 厂商对照表（缓存键 / 档位 / 三档计费）
- intuitionlabs 2026-09 五家定价表
- 落地：`defaults/wb-max-token-saver/references/knowledge-base.md` §r715B-1/2/3
- r732C：Anthropic 官方《Effective context engineering for AI agents》+《Scaling Managed Agents》两篇 WebFetch 一手逐字；Chroma Context Rot 技术报告（2025-07-14）经 13labs.au / masterprompting.net / qatronic.com / adroit.io 四域交叉；Liu et al.《Lost in the Middle》TACL 2024 逐字引用

- r738B：`platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context`（Claude 官方，**WebFetch 被地区重定向至 app-unavailable-in-region，如实登记**；由官方中/英双页 WebSearch 快照逐字核验四行表、Combining approaches 与 25% markup 原文）+ `anthropic.com/engineering/advanced-tool-use`（官方，WebFetch 200 全文逐字，仅作机制本体判非与背景，不搬数字）+ `www.safeguard.sh` 等不相关域未采纳。

## 八、有效上下文长度必须按基准族测，"窗口没满"从来不是安全声明（CI · r742B 2026-11-14 实拉，三独立域交叉）

§五给退化的架构根因（n² 注意力）与压缩可逆性，§六给工具面四条压力源。本节补的是**验收口径**：标称窗口是"能接受多少输入"，有效长度是"能可靠用上多少"，两者必须分开度量；而一个绿色的单针热力图几乎不能证明任何下游能力。

### r742B-1 ★claimed length ≠ effective length，且两者差距是常态不是例外
Compile N Run《Long Context in Practice》逐字："A config.json that says `max_position_embeddings: 131072` tells you **the largest position the model will accept. It does not tell you whether the model can find, use or reason over a fact that sits 100,000 tokens back**."；RULER（Hsieh et al., NVIDIA, COLM 2024）**effective context length** 定义逐字："the largest tested length at which a model's average score over the 13 tasks stays above a fixed threshold, chosen as **Llama2-7B's score at 4K tokens (85.6%)**"；实测"**Almost every model passes vanilla NIAH at its claimed length and fails RULER's threshold well before it**"：GPT-4 128K→64K、Llama3.1 70B 128K→64K、Qwen2 72B 128K→32K、Mistral-v0.2 7B 32K→16K。Futurecraft《Context Rot》独立逐字："In the authors' words, **'only half of them can maintain satisfactory performance at the length of 32K'**"（17 个声称 32K+ 的模型）；NoLiMa 有效长度表（保持短输入基线 ≥85% 的最长输入）：GPT-4o 声称 128K / 有效 8K、Gemini 2.0 Flash 声称 1M / 有效 4K，"The claimed window is **16x the effective length for GPT-4o and roughly 250x for Gemini 2.0 Flash**"。
- 判据：① 上下文预算按**有效长度**定，不按 model card 的窗口数；② "窗口没满"在 §五 已被判为不构成堆料理由，本条给出可测量的判据——自己任务上按长度扫一遍并定保持率阈值，而不是看 fill 百分比；③ 换型号/换推理配置后有效长度会变，预算表须标型号、基准与日期。与 §三 r710A-1「按最重操作测窗口」分工：那条给工程测法，本条给公开基准对"标称 ≠ 可用"的量化证据与阈值定义方式。

### r742B-2 ★绿色 NIAH 热力图只证明两件事；基准族彼此不可代替
Compile N Run 逐字："**A green heatmap shows that positions work and copying works, nothing more.** Add distractors, multi-hop and non-literal variants."；HELMET（Yen et al., ICLR 2025）逐字："argues that synthetic tests and small task subsets give **noisy, inconsistent rankings**… Across 59 models, it found that **NIAH-style synthetic tasks do not reliably predict downstream performance**, that **categories correlate weakly with each other**, and that open models lag closed ones most on tasks requiring full-context reasoning"；NoLiMa（Modarressi et al., ICML 2025）去掉词面重叠后"at 32K, **11 of the 13 models fell below 50% of their own short-context baseline**, and even GPT-4o dropped from **99.3% to 69.7%**"。Futurecraft 独立交叉："Of 13 models claiming at least 128K, 'at 32K, for instance, 11 models drop below 50% of their strong short-length baselines.' GPT-4o went from 99.3% on short input to 69.7% at 32K."
- 判据：① 基准按"它抓什么"分开记（NIAH＝位置/复制；Lost in the Middle＝位置偏置；RULER＝干扰项/多跳/聚合/QA 的有效长度；NoLiMa＝依赖关键词匹配；HELMET＝应用级下游排名），**不能用 A 的通过给 B 背书**；② 需求若含"跨多段材料推理"或"问题与证据无字面重叠"，单针检索通过率与它无关，必须换对应基准；③ 位置效应按 §五 r732C-2 是任务依赖的待验证假设，基准间的弱相关正好说明"换个任务排名就变"。与 §六 r738B-1「四种手段各减一样」同构但不同面：那条分流**工具面压力**，本条分流**评测能力**。

### r742B-3 ★评估有固定顺序，且配置错误会伪装成"上下文能力差"
Compile N Run 官方《A Checklist for Evaluating an Extended Model》逐字七步：1. **Short-context regression**（≤4K 重跑常规基准，"Static scaling methods can cost some short-context quality"）→ 2. **Perplexity sanity check**（"A blow-up means the configuration is wrong; **a flat curve proves little**"）→ 3. **NIAH grid**（"Anything less than near-perfect here usually means a **configuration error**"）→ 4. **RULER** 按自己业务阈值算 effective length → 5. **Position sweep** 在自家任务上把关键文档从首移到尾 → 6. **语义非字面测试**（NoLiMa 或 HELMET/LongBench/自家长文档任务）→ 7. **Cost and latency**（prefill 与 KV-cache 随长度增长，"Sometimes retrieval over a shorter context beats a long one on both quality and cost"）。《Common Mistakes》逐字："**Equating claimed and effective length**"、"**Reporting only vanilla NIAH**"、"**Using the chat model without its chat template**… which **looks like a context failure but is not**"、"**Forgetting to enable scaling at inference**… measures **extrapolation, not the advertised capability**"、"**Ignoring tokenization in length targets**… build haystacks by **token count**, not by characters"。
- 判据：① 顺序不可跳——先短上下文回归再谈长，否则把配置退化误判成模型能力退化；② 症状"长上下文掉分"先排三个非能力因（chat template / rope_scaling / 字符数当 token 数），排完才归到 §五 的注意力预算；③ 报数字必须带长度口径、分词器、基准名与阈值，跨基准的分数不可比。Futurecraft 明确代际边界："Almost all the work below uses synthetic tasks and models from 2023-2025. **You can't carry its numbers over to current** … no comparable published tables for these models could be found."、"No such table exists for the late-2026 generation" ⇒ 本轮所有数值只作**方法示例**，落地时以自测为准，禁止写死成通用阈值。

### r742B 来源与判非（逐字核验，2026-11-14）
- `www.compilenrun.com/docs/ai/llm/llm-positional-encoding/llm-long-context-evaluation/`（WebFetch 200 全文逐字：RULER 13 任务/85.6% 阈值/有效长度表、HELMET 59 模型、NoLiMa 11 of 13、七步评估顺序、Common Mistakes 六条）— 一手教程全文
- `futurecraft.pro/blog/context-rot`（2026-10-31 发布 / 2026-11-08 更新，WebFetch 200 全文逐字：基准对照表、NoLiMa 有效长度表、16x/250x、only half…at 32K、"put the important parts at the edges isn't universal advice"、代际边界声明）— 独立域一手交叉
- `9to5ai.tech/long-context-recall-explained`（WebSearch 快照逐字：RULER/NoLiMa/HELMET/LongBench v2/AA-LCR/ATLAS 概览与"effective length"口径）— 独立域交叉
- `github.com/fledgeling-co/fledgeling-plugins/.../compaction-gemini.md`（WebSearch 快照：NoLiMa 11/13、GPT-4o 99.3→69.7、PrecisionMemBench / Recall 掩盖检索失败；**单源未复现 + 含 Errata 自述，立场登记不作结论唯一来源**）
- `llm-safety-challenges.github.io/`（WebSearch 快照，评测污染/基准偏差背景，仅判非）
- **判非**：`RULER` / `NoLiMa` / `HELMET` / `effective context length` / `claimed length` / `NIAH` / `needle-in-a-haystack` / `lexical overlap` / `short-context baseline` / `max_position_embeddings` / `rope_scaling` 全库 SKILL.md **0 命中**；co-learn 台账 `RULER` 9 / `NoLiMa` 5 命中**全在豆包自留地**：r139C 明写「长上下文评测基准（RULER/LongBench v2…）模型评测工具事实，个人不跑基准 → 不落」、r318B/r364B/r376C/r386A 学的是记忆基准/退化绝对阈值/长度能力曲线（ATLAS）、r710A 明写「NoLiMa 长上下文评测已落 `wb-context-compressor` ⇒ 判非」。按去重铁律＋豆包自留地纪律，WB **0 落地** `wb-context-compressor` / `wb-execute-discipline`，也**不搬** r386A 的 ATLAS 曲线数字与 r364B 的 32K–100K dumb zone 阈值；本轮只取「claimed≠effective 的预算口径 + 基准族各自抓什么 + 七步评估顺序 + 三个配置误判」这一**验收协议层**。`Lost in the Middle` 3 命中（本技能 §五 r732C 已学 U 型曲线与位置效应任务依赖、`wb-max-token-saver`、`wb-execute-discipline`），本轮不重述该结论、只作基准族分工对照。
- **未采纳**：任何具体模型分数当通用阈值、ATLAS/AA-LCR 等 2026 榜单数字、PrecisionMemBench 精度数值（单源未复现）。A/C 两轮结论一律不复用。
