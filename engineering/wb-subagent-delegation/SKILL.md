---
name: wb-subagent-delegation
description: >-
  子Agent委派纪律（Subagent Delegation Workflow）。只有当任务能真正并行或明显提升效率时才调用子Agent；主Agent负责目标、任务拆分、分工、结果汇总；子Agent只处理明确范围，不重复调查他人已负责内容；子Agent返回结构化结果；主Agent统一去重、冲突检查与最终整合；简单任务禁止为"看起来高级"而调用多个Agent。触发词：子Agent、子代理、委派、并行处理、分给几个Agent、多Agent、并行跑、delegate、能不能并行、分工、派活、同时跑、并发、聚合结果、去重整合、等不等子代理。
version: 1.14.0
agent_created: true
---

# 子Agent委派纪律（能一次完成就不要拆多个Agent）

## 核心判断
调用多个Agent是手段不是目的。多数任务主Agent直接做更快、更省、更少出错。**只有"真能并行"或"明显提效"才委派**——这与 `personal-ai-os` 的"最短路径"和 AGENTS §0.12 的反过度流程化一致。

## 何时委派（准入）
满足其一才派：
1. 子任务之间**无依赖**、可真并行（如同时抓 N 个独立来源、同时读 N 个独立文件、同时跑 N 个独立验证）。
2. 单个子任务**明显更重**（长上下文、独立探索），放进主上下文会挤占或串味。
3. 需要**隔离上下文**避免互相污染（如互相矛盾的假设各自验证、互不信任的来源各自取证）。

**禁止**：为"看起来高级"派多个Agent；简单任务（单文件 / 单来源 / 一步到位）派多个Agent；把本可顺序做的串行任务硬拆并行；派出去却无汇总。

## 主Agent职责（四件必须做）
1. **定目标**：一句话说清总目标 + 验收标准；说清"哪些算完成"。
2. **拆 + 分工**：拆成最小独立子任务；每个子Agent的**范围、输入、输出契约、截止产物**写死，且边界**不重叠**。
3. **派发**：用 Agent 工具；prompt **自包含**（含背景、范围、返回格式、明确"不该碰哪些已由他人负责的领域"）。
4. **汇总**：统一**去重、冲突检查、最终整合**成一份交付物，并对受影响结果重新核对。

## 子Agent职责
- 只处理分配到的明确范围，**不重复调查其他子Agent已负责的领域**（派发时显式列出"你不该碰 X/Y"）。
- 返回**结构化结果**，固定字段便于主Agent直接拼接去重：
  - `结论`：直接给答案
  - `关键事实`：事实性内容
  - `证据来源`：出处 / 文件 / 页码 / URL
  - `未覆盖`：哪些没做到
  - `不确定项`：标注假设 / 待验证 / 信息不足
- 失败或超出范围 → **显式回报**，不编造、不静默跳过、不伪装完成。

## 与现有技能分工
| 场景 | 走哪 | 本技能只补什么 |
|---|---|---|
| 领域角色路由（8 岗分派） | `personal-ai-employees` | 它管"派给哪个领域角色"；本技能管"是否 / 如何用 Agent 工具并行做" |
| 跨Agent共享记忆 / 交接 | `agent-guild` | 子Agent共享身份 / 规则 / 记忆走它；本技能管运行时委派纪律 |
| 子任务需规约驱动实现 | `wb-spec-driven` | 每个子任务落地可交给它的计划-实现-验证循环 |
| 子任务内部失败根因 | `wb-debug-loop` | 子Agent内部排障走它，本技能不管具体排障 |

## 失败处理
- 子Agent失败 / 超时：主Agent先**重试一次并收紧范围 / 澄清输入**；仍失败则主Agent**自己补做该块**或明确标注"未覆盖 + 原因 + 可继续位置"。
- **严禁**：为"继续执行"掩盖子Agent真实失败；把未完成的块伪装成已完成；把冲突块擅自选边不报。
- 整合后必须对**冲突块与受影响结果重新核对**（尤其多个子Agent结论互相打架时）。

## 执行环境隔离 → 中间产物必须走显式句柄，不能假设共享工作区（来源：Pipedream `docs/connect/components/files.md` File Stash，2026-09-27 r198-A 实拉 12,405B）
- **★每一步执行都在自己的隔离环境里**：上一步写到临时目录的文件，下一步默认**看不见**。跨步骤要传产物，必须把它同步到外部存储并拿到一个**可复用的句柄**，后续步骤显式带上同一个句柄。判据：**"它应该还在那儿"是链式执行最常见的静默失败——不报丢文件，只报结果为空**。
- **★句柄要复用而不是每步新建**：新建句柄会生成新的存储空间，同链上多步之间就断了关联；正确做法是第一步生成、后续步骤传入同一个值（服务端通常允许用空串 / 布尔真 / "NEW" 触发新建，之后一律回填）。判据：**每步新建句柄 = 每步都在一个新的空目录里找上一步的产物**。
- **★"要不要句柄"由结构化能力声明决定，不是按名字猜**：组件元数据里带 `stash: required|optional` 这类字段时，`required`=该步必然产出文件、必须给句柄；`optional`=看输入是本地路径还是远端 URL 二选一。名字里含 file/upload/download 之类的**名称启发式只在声明缺失时才用，且要标注为猜测**。判据：**声明是契约，名字是巧合；把巧合当契约会漏掉所有不按套路命名的产物**。
- **★产出物与访问凭证时效要分开看**：产物本体与它的临时访问链接通常是两套时效（本体可存更久、签名链接短期失效）。判据：**把"链接过期"当成"文件没了"会触发无谓的重跑；把"文件已过期"当成"链接还能刷"会拿到空结果**。

## 拓扑选型：先定连接形状，再谈要不要并行（来源：Activepieces `blog/ai-agent-orchestration` 六种编排模式 + `blog/agent-harness-vs-agent-loop` 对比表，2026-09-27 r198-B 实拉 23,416B / 16,866B）
- **★六种基础连接形状，按判据选而不是按喜好选**：
  | 形状 | 判据 | 典型误用 |
  |---|---|---|
  | 顺序（pipeline） | 后一步依赖前一步产物、阶段清晰 | 本可并行却排队 |
  | 并行（fan-out） | 子块互不依赖、要速度 | 有依赖硬拆并行，汇总时对不上账 |
  | 交接（handoff） | 首步是分拣/分类，不同类别流向不同专能 | 用顺序链路模拟分支，每个分支都白跑一遍无关节点 |
  | 评审团（group） | 需要多视角 / 有质量门 / 发布前必审 | 草拟与复核用同一视角，评审变成复读 |
  | 集中路由（centralized） | 下一步取决于上一步结果，需要动态路由 | 编排者自己下场干活，变成瓶颈 |
  | 分层（hierarchical） | 规模大到一层管不过来，需子编排者 | 层数超过实际需要，沟通成本吃掉并行收益 |
- **★先问"这一步的序列能不能预先枚举"**：能枚举（路径固定、工具顺序已知）→用确定性骨架（harness），模型只在指定节点做判断；不能枚举（要探索未知页面/非结构化材料）→才放自主循环。**判据：序列化不等于自动化——用自主循环跑一条已知路径，付出的是不可预测的成本与不可复现的结果，换不来任何额外能力。**
- **★选错的代价是不对称的**：该用骨架却用了循环 → 失败模式是"转圈烧预算且从不收敛"；该用循环却用了骨架 → 失败模式是"遇到没预料到的分支就断"。**宁可直接报错，也不要让它假装跑完。**
- 与 §委派准入 的分工：那条管"要不要派"；本条管"派出去之后怎么连"。

## 并行度不是免费的：顺序保证、写冲突与超限语义必须先声明好（来源：Pipedream 官方 `docs/workflows/building-workflows/settings/concurrency-and-throttling`，2026-09-27 r199-A 实拉 10,537B）
- **★并行会取消顺序保证，而且覆盖是静默的**：文档举的例子是两个事件同时往同一张表写同一行，后写的把先写的盖掉，**不抛任何错**（"one event can overwrite data from another event … and no error will be thrown"）。**判据：只要多个并行块写同一个目标（同一文件 / 同一行 / 同一外部资源），就降级为串行（单 worker）；只有目标集合互不相交时才谈并行。**
- **★限并发不只是填个数，还要定"超了怎么办"**：待处理事件进队列，队列有**上限**（免费档每工作流 100 条，付费可提到 10,000），满了之后**直接丢弃**，只在事后留下 `Event Queue Full`。→ 委派并行任务前必须写明三件事：**允许的同时执行数 / 超限是排队还是丢弃 / 丢弃时有没有可见信号**。漏写任何一项 = 默认"静默丢"，而主 Agent 拿到的结果看起来只是"少了几条"。
- **★固定窗口 ≠ 均匀间隔**：节流 `1 次 / 5 秒` 的含义是"任意固定 5 秒窗口内至多一次"，**不是"每次执行相隔 5 秒"**；突发流量下二者实际速率差一个数量级。声明速率要求时必须写清是哪种窗口语义。
- 把速率上限设为 `0` 是暂停的正确写法：队列停投递但事件保留，比直接关掉触发器少一个"开关状态与业务状态不同步"的坑。
- 与 §执行环境隔离、§拓扑选型 的分工：那两条管"中间产物要不要落显式句柄""块之间怎么连"；本条管"**连好之后允许几块同时跑、以及跑不上的那块最后去了哪**"。
- 提升层：工作流。

## 同一次 run 里，自主步骤与确定性步骤必须落在同一条 trace 上（来源：Activepieces《AI Agent Security vs Application Security in 2026》§Auditable logs，2026-09-27 r200-B 实拉 22,167B）

- **★自主决策与固定逻辑跑在同一个 run 里，trace 就不能按类型分家**：原文——因为两类步骤在同一个 run 内执行，安全团队能在 Run Details 里检查整条链，**而不是跨系统去拼碎片记录**。判据：**主代理要能在一处看完"哪个决定是模型做的、哪个是固定逻辑做的、它们怎么串起来"**；只要子代理的轨迹写在另一处，归因就退化成人工拼图。
- **★委派协议里除了"回报什么结论"，还要写"轨迹写到哪个共同位置、以什么格式能被整条取走"**：同一条 trace 还要支持整条导出（原文导出为 event stream 进 SIEM），否则审计只能看截图。判据：**能逐条取走的轨迹才算证据**，只能在 UI 里翻的不算。
- **★trace 要能区分"基础设施失败"与"prompt 里的逻辑错误"**：原文按步记录输入输出，用来分辨是基础设施挂了还是 agent 的指令写错了。判据：**子代理回传失败时必须带足够信息让主代理判断"重试有没有用"**——基础设施类重试有效，逻辑类重试只会再错一次。
- 与 §执行环境隔离（显式句柄）、§拓扑选型 的分工：那两条管"产物放哪""块怎么连"；本条管"**连起来之后整条链的记录在不在一处、能不能整条取走**"。
- 提升层：工作流 / 可复用 Skill。

## 双模型主-副手编排：强模型规划审查 + 廉价模型执行，各持上下文与缓存（来源：The Batch issue-372「One Agent Works, Another Directs」Devin Fusion / Sakana Fugu 实测，2026-09-27 r232-A 实拉，Cognition 独立评估 + Artificial Analysis Coding Agent Index v1.5）

- **★一个强 lead 管规划与审查，一个廉价 sidekick 干大部分执行活**：lead 负责消解用户请求歧义、写 plan、审 sidekick 的产出；sidekick 读/改/测并回报。两者**各自持有自己的工具与上下文（各自的 prompt cache）**，不是把任务从一个模型顺次交给另一个。判据：**"用两个模型"的省法不是路由切换，是"让贵的只做贵的活（规划/审查/难块），便宜的做重复执行活"**；lead 在 sidekick 卡住时收回任务重派。
- **★交换的是 brief / 结果 / 反馈，不是整段对话**：lead 给 sidekick 的 task brief 写明约束与成功标准；sidekick 回传结果与问题；彼此不搬对方的全量上下文。判据：**每个 agent 保住自己的上下文与缓存折扣的前提是"只传契约不传历史"**——把全文塞给对方就退化成单 agent 长上下文，缓存红利消失。
- **★换模型必须在 compaction 边界做，否则省下的钱被重填缓存吃掉**：普通"中途把任务交给另一个模型"会清空缓存，按 frontier 价格重填就把路由省下的钱抵消掉；compaction（agent 总结前文缩小上下文，缓存本就被丢弃）是换模型的零成本时机——轻量分类器在 compaction 时判断是否把 sidekick 的活交回 lead、或把 sidekick 角色升级成更强模型。判据：**模型路由的净收益 = 省下的 token − 重填缓存的成本；换模型必须挑缓存本来就要丢的时机，否则路由是负优化**。
- **★实证锚点**：Devin Fusion（lead Claude Fable 5.1 + sidekick SWE-2）在 Coding Agent Index v1.5 上匹配 Claude Code 用同模型（62分），但每个任务便宜 **36%**（$7.90 vs $12.40）；Sakana Fugu 走 dispatcher 派单（低成本模型拆任务派给池里最合的模型）是另一种已被验证的形态。判据：**多模型不是噱头——架构对，能在同质量下明显降本；但"哪个模型当 sidekick"要按实测效率选，不是按单 token 单价选**（SWE-2 比更便宜也更聪明的 GPT-5.6 Luna 又快又省）。
- 与 §拓扑选型（分层 hierarchical）、§同 run 同 trace 的分工：那条管"派出去之后怎么连""记录在一处"；本条补"**连的是两个不同档位的模型、且各自保缓存**"这一具体成本形态，与 `wb-max-token-saver` 的"整体成本四层"互补但本体是委派架构（重叠 <60%）。
- 提升层：工作流 / 成本。

## 意图路由双轨：模型只解释意图，执行保持确定性（来源：Dify blog intent-based email routing，2026-09-27 r232 并发线手交 / WorkBuddy 实拉核验）

- **★分类场景先问"模型输出直接决定动作吗"——应改成"模型决定类别，路由逻辑决定动作"**：原文 "Interpretation is model-based; execution remains deterministic"——LLM 作为固定节点上的路由分析者，从预定义类别集里选 intent + confidence + structured verification，taxonomy 在流程内固定、模型不能发明新类别。判据：**让模型做"解释/归类"这种它擅长且可逆的判断，把"执行动作"钉死在确定性逻辑里**。
- **★高置信非敏感自动路由，敏感或低置信进人工审查**：人工审核位提供三种恢复决策（approved / edited / rerouted），不只是"批/不批"。判据：**凡是"模型吐个标签就直接触发业务动作"的设计，都是把不确定性的代价转嫁给下游；双轨把解释与执行解耦，模型只负责它该负责的**。
- 与 §拓扑选型（集中路由）、§双模型主-副手 的分工：那些管"派出去之后怎么连""两个模型怎么省"；本条管"**单步里，模型的判断权该到哪为止**"——解释归模型，动作归逻辑。
- 提升层：工作流。

## 让出（yield）交接：传的是"完成所有权"，不是"执行授权"；已完成义务不可再装填；进度文本不是完成证据（来源：docs.openclaw.ai/concepts/subagent-yield-handoff 11,858B + tools/subagents/thread-bound-sessions 6,691B，2026-10-01 r344B 独立 curl 实拉；与 §同 run 同 trace / §双模型主-副手 互补——那两条管"轨迹在一处""两个模型怎么省"，本条管"委派方让出后，谁拥有完成、以谁的授权继续"）
- **★让出转移的是完成义务与任务谱系，不转移工具/审批/通道/回调权限**：原文 "Yield transfers ownership before closing the old execution"；"**No revived authority** — Neither a stored run ID nor provenance revives a closed execution. The successor … receives **fresh execution authority**. **Adoption preserves task lineage, not old tool, approval, channel, or worker callbacks.**" 判据：**交接面上跑的是"谱系 + 义务"，不是"权限"**；把 run ID 或出处当授权凭据，等于让一次已结束的执行继续签发新动作。
- **★完成源托管与执行分离，权限上限在发起时刻快照**：注册处把"活的 operator source"与执行分开保留，个体投递与结算用**当时捕获的权限上限**，而不是后来调度清理的异步调用者；"Retained results do not retain usable authority after that release"；取消专用批次保留**原取消调用者的准入**，不用已吊销的目标去授权新回合；混合结果/取消批次要求每个原始 source 仍存活且兼容。判据：**"谁发起的"决定"能用多大权限"，且这个上限在发起那一刻被冻结**——后来的调用者不继承，被吊销的目标不得反向授权。
- **★一个完成只能有一个 owner，已履行的义务不可再装填**："An existing visible-final receipt for the exact turn and child batch prevents rearming an already fulfilled obligation"；"a repeated callback cannot finalize it again"；迟到的公告失败 "cannot replace the batch's delivery state; **already committed delivery evidence remains valid**"。判据：**完成是幂等的单 owner 义务**——一次迟到报错若能把"已交付"改写成"未交付"，重试链会被反复重新武装。
- **★进度文本不是完成证据**："**progress text is not proof that a child finished or that its result was delivered**"；"Yield closes the old execution, not the delegated work"；等待确认只解决"没静默"。判据：**进度 / 等待回执 / 子任务已完成且结果已送达 是三件事**，验收只能认第三条。
- **★确定性批次 + 三档有界投递**：冻结的 run ID 排序、以创建/完成时间与子会话身份打破平局、被取代的子行排除，批次身份含 requester 身份 + 子 ID + 让出代数；投递上限 **3 次尝试 / 3 次歧义重放 / 10 次陈旧延迟**（活动后代不消耗陈旧延迟预算），findings 4,096 字符、单条结果 512、路由通知 1,024；"ambiguous replay reuses its attempt key; it does **not** assert global exactly-once delivery across Gateway restarts"。判据：**批次要确定性可复现（排序 + 平局规则），投递要三档封顶并显式声明"不承诺跨重启全局恰好一次"**——不写这条声明，下游会把重试键当成恰好一次的证明。
- 与 §拓扑选型 / §并行度 的分工：那两条管"块怎么连""允许几块同时跑"；本条管"**委派方中途离场后，完成归谁、继任者凭什么继续、什么才算真的完成**"。
- 提升层：工作流 / 安全边界。

- **并发去重：leader 选举 vs 共享队列 claim（失效形态不同）+ 内层超时须短于外层租约 + 状态对分开落盘即失步窗口 + 放弃=状态不推进 + 预检失败整体降级并点名**：本章已下沉 references/knowledge-base.md §r346C。

## 多 agent 的软/硬边界：路由建议不是调度器；默认作用域不共享，共享必须是显式动作（来源：docs.openclaw.ai/concepts/multi-agent.md 30,442B，2026-10-01 r348A 独立 curl 实拉）
- 原文：①「`delegationMode:"prefer"` — prompt guidance, not a scheduler」；`subagents.allowAgents` 才是硬 spawn 边界。②跨 agent 记忆 builtin 只搜自身语料，共享须显式 `memory.search.extraPaths`；vault 按 `scope:"agent"` 追子目录。③次级 agent OAuth 过期时 read-through 借 main 同 profile 的 **freshest** token，但**不回拷 refresh token**；静态 `api_key/token` 才可按 `copyToAgents` 移植。
- 判据：① **「建议性路由」不能当硬闸用**：`prefer` 只是给模型的提示，真正可派发的集合由硬边界名单决定；两者混用会出现「配了却没生效」或「以为限制了其实没限制」。② **默认作用域是各搜各的**：跨 agent 记忆与凭据默认不共享，共享必须写成显式路径/显式许可。⇒ 判两个 agent 有没有共享知识，看的是有没有那条显式声明，不是看它们是不是同一个系统。③ **凭据借道是有方向的**：借到的是当前最新访问令牌，refresh material 不回拷 —— 次级 agent 到期后仍须回主 profile 续期，不会自立门户；而静态密钥一旦 `copyToAgents` 就是真复制，传播面与吊销半径差一个数量级。
- 提升层：工作流/安全边界。触发词：delegationMode prefer 软路由、allowAgents 硬边界、extraPaths 显式共享、凭据 read-through 不回拷 refresh、copyToAgents 静态密钥。

## 子代理的三个预算不可互换；「等不到」不等于「已终止」，取消的作用域还要再分一档（来源：docs.openclaw.ai/tools/subagents/nesting.md 5,380B + operations.md 11,501B，2026-10-01 r348B 独立 curl 实拉；经 llms.txt 210,587B 定位真实路径）
- 原文：①嵌套深度 `maxSpawnDepth: 2`、`range 1-5`；每 agent 子代数与全局并发各自独立计数；②`Cascade stop` 分「`cascades through its descendant`」与「`cancels children only if the captured`」两档；③`cancellation does not cancel`；`completion is delivered does not move its execution`。
- 判据：① **深度、每节点子代数、全局并发是三个独立预算，任一耗尽即停止扩张，其余两维仍有余额**。⇒ 排障时不能用「并发还有余量」推断「还能继续下钻」，也不能用「深度够了」推断「并发不会打满」；三个计数器要分别断言。② **取消的作用域本身就是一档配置**：级联停分「只停本支」与「连后代一起停」。⇒ 写停止逻辑时先声明作用域，否则一次取消会越过预期边界（或反过来，以为停了整链其实只停了一支）。③ **等待超时不取消**：`agent.wait` 超时只是观察者放弃等待，被等的子代理仍在运行；同样「完成已投递」不等于「执行已推进」。⇒ 「我以为它死了」是独立于「成功/失败/超时」的第四种解释分支；重启后补完更意味着**不能把「没等到结果」当成「没有副作用」**。
- 提升层：工作流。触发词：三重预算不可互换、maxSpawnDepth、级联停分档、wait 不取消、完成投递不等于执行推进、重启补完 interrupted-run。

## r350B · 运行期注入（steer）有明确的不可打断边界，且模式决定是否走该路径（来源：docs.openclaw.ai/concepts/queue-steering，2026-10-02 r350B 实拉 235,599B）

- **★注入不打断已在跑的工具调用**：转向只在"LLM 调用之前"这个边界生效；已在执行的工具调用不受影响。判据：**注入点的粒度是"下一次模型调用"，不是"当前这一步"**——期待"立刻生效"的期望本身是错的。
- **★被运行期拒绝的注入按原顺序留在队列**，不是丢弃；被接受的注入在下一次 LLM 调用前以原消息精确插入；若注入正在等待，**尚未启动的串行尾部会被跳过**。判据：**被拒 ≠ 被丢，接受 ≠ 插队**；同时"跳过尾部"意味着注入会改变后续步骤集合，审计时要记录被跳过的是什么。
- **★注入边界对内部更新同样适用**（子 agent 完成报告走同一边界）。判据：**外部指令与内部事件共用同一注入通道 → 二者会互相排队**，内部报告堆积会延迟外部转向被看到。
- **★模式决定是否进入该路径**：steer 模式下正常入站消息走转向路径；followup / collect 模式下正常消息**跳过此路径、等到当前运行结束**；显式 `/steer <message>` 命令另行处理。判据：**同一条消息在不同模式下语义不同**——排查"指令没被理会"先确认当前模式。
- 提升层：工作流 / 模型。

## r350C · 队列是 lane-aware FIFO：每条 lane 独立并发上限，全局再封一层顶（来源：docs.openclaw.ai/concepts/queue，2026-10-02 r350C 实拉 256,946B）

- **★并发上限分 lane 配置，默认值各不相同**：未配置 lane 默认 1；`main` = `max(8, 可用 CPU 并行度 × 4)`；普通子 agent 队列每个发起会话默认 8；Swarm collector 队列每个 group 默认 32；入站会话再进全局 main lane，由 `agents.defaults.maxConcurrent` 封顶；Swarm collector 子项另有 group 预算 `tools.swarm.maxConcurrent`。判据：**"并发不够"要先定位是哪条 lane 的哪一层顶住了**——子 agent 队列打满和全局顶满是两种处置。
- **★默认参数是一组而不是一个**：未设置时所有入站通道面统一为 `mode: "steer"` + 内置 500ms debounce（steer/followup/collect 批处理）+ `cap: 20` + `drop: "summarize"`。判据：**队列满时的丢弃策略是"摘要"而不是"拒绝"**——消息不会原样保留，审计时看不到原文。
- **★可观测性有阈值与"假即时"两处坑**：等待超过约 2 秒才打 notice（短等待完全静默）；typing indicator 在**入队时立即触发**，用户侧看起来已经在跑，实际还在排队。判据：**用户感知的"开始"早于真实开始**，用交互信号推断执行状态会误判。
- 提升层：工具 / 工作流。


## r353A · 转向可注入性随 turn 类别分裂，批处理保内序不保原子（来源：docs.openclaw.ai `plugins/codex-harness-runtime/queue-and-feedback`，2026-10-02 r353A 实拉）

- **★同一个 steer 在不同 turn 类别下结论相反**："Codex review and manual compaction turns can **reject same-turn steering**" → 此时等当前 run 结束再启动该 prompt；而"Automatic compaction inside a regular turn **keeps steering available**"——输入被缓冲到下一个 model boundary。判据：**能不能插话由当前 turn 的性质决定，不是由队列配置决定**；报"转向没生效"先问这是哪一类 turn。
- **★批处理合成一次请求但保留内部次序**：安静窗口内 steer-mode 消息按**到达顺序**合成单个 `turn/steer`；内联图与存储附件**保留原图序**、沿用新 turn 的 hydration/大小/文件系统限制。判据：**合并发送不等于合并语义**——顺序被保留，所以顺序依赖型指令仍是安全的。
- **★失败粒度是"整条"而非"部分"**：附件无法准备、或转向被拒 → "the **complete message** remains queued for a follow-up turn"。判据：**不存在半送达**，要么整条下一轮再来，要么没进；据此不要设计"部分内容先生效"的假设。
- 提升层：工具 / 工作流。触发词：转向被拒、compaction turn、批处理保序、整条留队。
