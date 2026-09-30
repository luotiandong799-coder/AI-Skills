---
name: wb-max-token-saver
description: >-
  动作与 token 压缩、答案优先（已合并原 caveman 技能，**管输出侧：我 → 用户**；输入侧"读进来怎么取舍"不归本技能，走 `wb-context-compressor`）。每轮回复默认应用：先给结论（answer-first）、无空泛套话、无 AI 味填充、无重复开场白；工具输出 / 日志 / 长文本只保留与问题相关的要点，不原样堆砌；做长任务时控制上下文与工具调用的消耗（少读、按需读、不重复读）；完整文档 / 报告 / 分析任务按完整交付、不因"简短"缩水；结论必须基于已核实证据；安全警告 / 不可逆确认 / 多步顺序 / 用户要求澄清时临时恢复完整句式，之后立刻恢复压缩。触发词："caveman mode" / "use caveman" / "less tokens" / "省 token" / "降低调用成本" / "换便宜模型" / "模型降档" / "先强后弱" / "一次性成本" / "边际成本" / "减少轮数" / "换挡信号" / "热路径" / "别唠叨" / "正常模式" / "off"。关闭："stop caveman" / "normal mode" / "正常模式"。
version: 1.62.0
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

## 学习轮条目索引（正文已归档至 references/knowledge-base.md「学习轮条目归档」区）

| 条目 | KB 锚点 |
|---|---|
| 流式 UX 阶段模式：TTFT 是关键指标 / 四阶段加载 / partial JSON 修复 / 增量渲染 | 学习轮条目归档 |
| 不可变前缀：缓存友好的提示布局 + 发送前数 token | 学习轮条目归档 |
| 脚本输出隔离：确定性操作打包成脚本，代码永不进上下文，只回输出 | 学习轮条目归档 |
| 记忆 token 分层 + agent 工具化迁移：core 常驻保持小，迁移是工具调用不是批处理 | 学习轮条目归档 |
| 推理模型提示反向原则：三删 + effort 控深度，与标准模型 CoT 策略相反 | 学习轮条目归档 |
| 检索上下文排序与预算：top-few 硬预算 + 关键放首尾（lost in the middle） | 学习轮条目归档 |
| System prompt 分层预算：identity/capability/behavioral/context 各层 | 学习轮条目归档 |
| 记忆写入时序：先响应后提取，提取用便宜模型，收尾合并 session→global | 学习轮条目归档 |
| 代码库上下文：repo map（AST+PageRank+token 预算）+ launch point 决定可见性 | 学习轮条目归档 |
| 工具输出落库指针 + 按需检索召回：大输出不进上下文，进可检索库 | 学习轮条目归档 |
| 精简优先的实证：Claude Code 删掉 80% system prompt 而无评估损失 | 学习轮条目归档 |
| 上下文注入顺序：关键信息放首尾，中间是注意力盲区 | 学习轮条目归档 |
| 记忆读取按需触发 + 摘要锚点定向：不 always-on 检索，不确定才查 | 学习轮条目归档 |
| 上下文作为演化工件：轨迹提炼教训→结构化增量更新，防内容崩溃 | 学习轮条目归档 |
| 样例驱动渐进式引导：让 AI 从样例归纳方法论，人只判断对错 | 学习轮条目归档 |
| 上下文显式分节标签：系统指令/检索上下文/对话摘要分块标注，不混单块 | 学习轮条目归档 |
| 技能加载会话快照：清单会话内定格，变更才刷新 | 学习轮条目归档 |
| 第三方技能选型三判据：安装量/来源信誉/源仓库热度 | 学习轮条目归档 |
| 注入出口检测两法：canary 被动证据 + LLM 主动检测器 | 学习轮条目归档 |
| 主张级可审计四维（deep research 引用的可审计标准）：来源覆盖/来源健全/矛盾透明/审计成本 | 学习轮条目归档 |
| 技能开发两实例迭代闭环：基线→最小草稿→实测→精修 | 学习轮条目归档 |
| 运行时工具集稳定性纪律：不中途换工具/模型，用工具模拟状态迁移，延迟加载而非删除 | 学习轮条目归档 |
| 缓存命中率当 uptime 监控：缓存破坏按事故告警，fork/分支共享父前缀 | 学习轮条目归档 |
| 工具返回字段裁剪：工具只回 LLM 需要的字段，非完整 API JSON | 学习轮条目归档 |
| 按需装载工具/能力 + 缓存安全的节奏提醒：上下文要"省"也要"不忘" | 学习轮条目归档 |
| 工具循环的 O(n²) 隐藏账单：每步重放全量历史→固定窗口截断回 O(n)，且要故意为之 | 学习轮条目归档 |
| RAG 检索的时效与顺序：先去重后检索 + 时间戳过滤陈旧上下文；提示漂移用类别清单 + 模式解析兜底 | 学习轮条目归档 |
| 人机路由的过升级治理：收紧置信阈值 + 补边界示例，不是加规则 | 学习轮条目归档 |
| 模型迁移收尾三清单：集成测试 / 长度控制提示词调优 / 成本-限流重基线化 | 学习轮条目归档 |
| 技能触发评测配比规格：20 条 queries 8-10/8-10、每条跑 3 次算触发率、基线对比含 token 用量 | 学习轮条目归档 |
| 记忆按业务主体（actor）归属，能力随调用携带 | 学习轮条目归档 |
| durable execution：父休眠子继续、崩溃不级联 | 学习轮条目归档 |
| 输出校验参数化：最终答案校验器 + 每步前后状态日志 | 学习轮条目归档 |
| harness 全能力插件化：循环/调度/存储/UI 也是插件 | 学习轮条目归档 |
| 长输入编排：文档置顶、query 置底 | 学习轮条目归档 |
| 规则文件 200 行上限 + 按路径作用域拆分 | 学习轮条目归档 |
| 实现后独立评审子代理：不带实现上下文 | 学习轮条目归档 |
| 代码执行 import 白名单：默认最小集 + 显式声明 | 学习轮条目归档 |
| 记忆摄取打分门控 + NO_INGEST 显式拒绝 | 学习轮条目归档 |
| 远端 MCP 多用户隔离透传：external-user-id | 学习轮条目归档 |
| Skill 编排的字段映射是关键步：先声明 schema，再显式对接 | 学习轮条目归档 |
| Agent 成本熔断 + 一键回滚链 | 学习轮条目归档 |
| 动作敏感记忆五要素：记忆记的不是事实，是行为条件 | 学习轮条目归档 |
| 子代理 prompt 完整自足：只有 prompt+CLAUDE.md，不许占位符 | 学习轮条目归档 |
| 子代理输出原样透传：父默认会转述，要原文须显式指令 | 学习轮条目归档 |
| 插件安装 10 项安全评测清单 | 学习轮条目归档 |
| 汇报是产品不是流水账：给决策所需的最小充分面，状态卡只发一次 | 学习轮条目归档 |
| 推理模型成本三纪律：thinking 也计费 / caching 静默失败 / router 按盈亏平衡 | 学习轮条目归档 |
| Qoder 净新（2026-09-27 · 全量消化） | 学习轮条目归档 |
| 工具定义的上下文预算：可见工具 30-50 起衰减；defer 必须留非延迟锚点 | 学习轮条目归档 |
| 提醒/追问型输出要写死次数上限 + 负面清单 | 学习轮条目归档 |
| 治理档位要成对出现，且「续活」必须区分交互写与非交互写；压缩要有损失准入门 | 学习轮条目归档 |
| 成本账按「时长 × 内存档位 × 段数」归因，并显式列出豁免项与是否结转 | 学习轮条目归档 |
| 激活决策要后置一次：检索命中 ≠ 真的需要它 | 学习轮条目归档 |
| 分页契约三要素：整名 + 游标 + 按工具结果预算切页，绝不返回半个文件名 | 学习轮条目归档 |
| r308A 视觉 token 预算管理 | 学习轮条目归档 |
| 上下文工程与缓存治理 2026：四动词分类法/三层内存与八层权威/prompt caching 最高杠杆/rolling | 学习轮条目归档 |
| 推理模型与思考工程 2026：两问决策框架/thinking 成本数量级/knee 预算/effort 档位/思考与工具 | 学习轮条目归档 |
| 本地 LLM 与隐私优先 2026：零遥测工具审计/下载元数据足迹/Q4_K_M 显存公式/硬件三档/全本地 RAG/8 | 学习轮条目归档 |

## 解码参数实证：T=0 不保证确定性 / JSON 等 6 节（细则已下沉 KB）
- 完整论证见 [references/knowledge-base.md](references/knowledge-base.md) §解码参数实证：T=0 不保证确定性 / JSON 等 6 节（第 1 组）。

## 成本与基础设施簇（细则已下沉）
- 完整细则见 references/knowledge-base.md「成本与基础设施簇」；正文只保留触发线索与结论：成本四层、Relocation Trick、路由阈值学习、Q4_K_M 量化、KV 亲和性、Batch 50% 折扣、两阶段模型路由。


## 配额的粒度决定公平性：共享池式（per-run）配额下单个大户可饿死全部，须下沉到逐单元（per-step）；大载荷外置传引用而不是塞进记录（来源：www.activepieces.com/docs/install/troubleshooting/truncated-logs.md 2,279B，2026-10-01 r340C 独立 curl 实拉逐串命中）
- **原文**：①「Flow runs have a maximum log size (default **25 MB**) ... truncating large step **inputs** — you'll see `(truncated)` in place of the original value」；②「step input values are replaced with `(truncated)`, **starting from the largest**, until the run fits」；③「A planned enhancement will move this limit **from per-run to per-step**, giving more granular control over how much data each step can retain」；④「prefer passing files between steps using the built-in file storage ... **rather than embedding raw bytes in step outputs**」。
- **判据**：① **同一份预算，按什么粒度切，决定了谁能抢到**：按整次运行（per-run）设总量，一个肥步骤就能吃光所有人的额度，其余步骤表现为"莫名其妙被截"——而它们本身一点都不大。⇒ 设预算时先问粒度：共享池式配额必然带来大户饿死小户，逐单元配额才可控；看到"某些内容被无故截断"时，先查是不是被同一池子里的其他人挤掉的。② **降级要有可见顺序并且可解释**：从最大的开始截、截到装得下为止，每一步都留 `(truncated)` 占位。⇒ 被压缩方要能一眼看出"这里原本有东西、被截了"，而不是看到空值以为是本来就没有。③ **大体量载荷的正确归宿是外置存储 + 传引用**，不要把原始字节塞进运行记录/上下文。⇒ 凡是"把大文件 base64 之后放进某条记录"的设计，都会在某个阈值上把整条链路撑爆；引用进记录、实体进存储。④ 与 §有损压缩须留省略标记 同源：那一条管"标记与计量"，本条管"配额粒度与依赖侧不可截"。
- **提升层**：工具/工作流。触发词：per-run 配额、per-step 配额、大户饿死小户、从最大的开始截、truncated 占位、大载荷外置传引用、配额粒度。

## 提示面按运行角色分档；技能目录预算与运行时摘录预算是两个池（来源：docs.openclaw.ai/concepts/system-prompt.md 25,568B，2026-10-01 r342A 独立 curl 实拉逐串命中）

- **原文**：①「The runtime sets a `promptMode` per run (**not user-facing config**): `full` (default): all sections above. / `minimal`: used for sub-agents; omits the memory prompt section (bundled as **Memory Recall**), **Model Aliases**, **User Identity**, **Assistant Output Directives**, **Messaging** ... / `none`: returns only the base identity line.」；②「**Sizing is owned by the skills subsystem, separate from generic runtime read/injection sizing**」+ 双列表「Skills prompt budget `skills.limits.maxSkillsPromptChars` | Runtime excerpt budget `agents.defaults.contextLimits.*`」；③「The runtime excerpt budget covers `memory_get`, **live tool results**, and **post-compaction `AGENTS.md` refreshes**.」
- **判据**：① **省 token 的第一刀是「按运行角色分档」，不是按全局开关**——full/minimal/none 三档由运行时按单次 run 推导（子代理自动落 minimal），不是让用户配的开关。⇒ 同一份提示别无差别塞给所有执行体；给子代理 / 心跳 / 后台轮次单独配档，把「身份、记忆提示、输出指令」这些非必要节整段省掉。② **预算是分域的多个池，不是一个总池**——技能目录提示与运行时摘录各自独立计量，不能拿一个池的余量去补另一个池的超额。⇒ 归账时分开记：「技能列表变长」与「工具结果变大」是两笔账，压一个不会救另一个。③ **运行时摘录池把「检索、实时工具结果、压缩后重载」归到同一池**⇒ 这三者互相挤占，属同一个监控对象；压缩后刷新 AGENTS.md 也算进这个池，不要以为它免费。
- **提升层**：模型/工具。触发词：promptMode、角色分档、sub-agent minimal、技能提示预算、运行时摘录预算、预算分域、post-compaction refresh。

## 隐性成本与剥离层：工具 schema 看不见但计入；指令不进模型输入（来源：docs.openclaw.ai/concepts/context.md 10,756B，2026-10-01 r342C 独立 curl 实拉逐串命中）

- **原文**：①「Tools affect context in two ways: 1. **Tool list text** in the system prompt (what you see as "Tooling"). 2. **Tool schemas** (JSON). These are sent to the model so it can call tools. **They count toward context even though you don't see them as plain text.**」+「`/context detail` breaks down the biggest tool schemas so you can see what dominates.」；②「**Directives**: `/think`, `/fast`, `/verbose`, `/trace`, `/reasoning`, `/elevated`, `/exec`, `/model`, `/queue` are **stripped before the model sees the message**. Directive-only messages persist session settings. Inline directives in a normal message act as per-message hints.」
- **判据**：① **算 token 账时最大头常常是看不见的那部分**——工具 schema 以 JSON 发送、不作为可见文本出现，却同样计入上下文。⇒ 省 token 不能只盯正文长度；先拆「可见文本 / 不可见 schema」两笔账，通常 schema 才是大头（用 `/context detail` 这类按 schema 拆解的手段定位）。② **能放进剥离层的就别写进正文**：指令在模型看到消息之前被剥离，持久设置走 directive-only 消息、一次性偏好走内联提示。⇒ 反复写进正文的「请如何如何」应该升级成设置项或指令层，正文只留真正需要模型理解的内容；这是把稳定偏好从每次输入里搬出去的标准手法。③ **剥离层有两种作用域**：单独一条指令=持久化会话设置，内联指令=只对当前这条消息有效。⇒ 放剥离层时要选对作用域，否则要么污染后续所有轮次，要么每次都重新说一遍。
- **提升层**：模型/工具。触发词：工具 schema 隐性成本、可见文本 vs 不可见 schema、指令剥离层、directive-only 持久化、内联提示作用域。
