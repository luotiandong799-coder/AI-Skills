# r172-A 工具描述工程与选择可靠性：排除式条款、Looking-is-not-picking、工具数=精度旋钮

实拉时间：2026-09-24 20:14
信源：dev.to ulnit《wrong tool bug in 6 lines JSON》2026-09-09 / sureprompts / adaline labs 2026-05 / belsoftsolutions 2026-07 / explainx MCP descriptions 2026-06 / ai-tldr function-calling best-practices + designing-tools / zylos 2026-04 / theneuralbase description-engineering + tool-descriptions-quality + wrong-tool-selected / aibootstrapper 2026-08 / aistoollab 2026-08 / arXiv 2606.16364 Looking is not picking / apidog 2026-08 / respan 2026-05 / codex KB readout bottleneck 2026-09 / tallyfy 2026-05（工具选择组，满 10 站）

## 实拉证据（关键原文）
- dev.to ulnit：描述里写「NEVER use for anything about a specific customer's order…even if the customer hasn't given an order number yet.」——那个 **"even if…"** 排除条款修掉的失败比其他所有改动加起来还多，因为它命名了一个前置缺失参数时模型会走错的分支。
- arXiv 2606.16364：「on real BFCL failures the model attends most to the correct tool 80% of the time (vs. 21% chance); the gold tool is the under-attended segment on only 10%. The model looks at the right tool and still picks wrong, so the failure lies at the decision readout, not in the harness.」
- codex KB 2026-09：「selectivity collapse…model attends correctly but cannot reliably commit to the right output when multiple plausible candidates compete at the logit level.」
- tallyfy 引 OpenAI 文档：「Keep the number of functions small for higher accuracy…Aim for fewer than 20 functions at any one time.」adaline：「When a tool list grows beyond ten to twelve tools, distribute across specialized sub-agents.」
- aibootstrapper：「Rewrite descriptions as 'when to use', not 'what it does'…Gives the model the discriminating condition it needs at the decision step, not just a label.」
- ai-tldr designing-tools：两个相似工具描述重叠时「Add explicit 'Use this for X, NOT Y' language to both. If they genuinely cover similar ground, consider merging them into one tool with a parameter.」

## 独点清单（3 个真独点）

### 独点1：描述里写"even if…"排除前置缺失参数的分支（工具/可复用 Skill 层）
- 判据：工具描述不仅写"什么时候用我"，还要写**当关键信息缺失时模型容易猜的那条路别走**——典型句式"即使客户还没给订单号，也别用这个查通用文档，去用查订单状态的工具"。
- 独有增量（与 r166B 函数调用可靠性区别）：那条管调用后失败怎么重试；本条管**描述文本怎么写才能在决策步就选对**——尤其"信息不全时模型倾向于用宽泛工具"这个分支是常规描述写作没覆盖的。
- 提升层：可复用 Skill（工具描述写作）。

### 独点2：Looking is not picking——模型 80% 注意力在正确工具上仍选错，失败在 logit 读出层（工作流层）
- 判据：BFCL 真实失败案例中，正确工具是模型注意力最高的段占 80%（随机基线 21%），gold tool 被忽视只占 10%。**模型看对了还是选错**——不是没找到正确工具，是多个相似候选在 logit 层竞争导致 selectivity collapse。
- 独有增量：这条改写了"选错工具=描述不清/模型笨"的归因——相当比例的错误是**读出层竞争**，修法不是再写更花的描述，而是**减少同时竞争的相似工具数量**（合并/拆分/按子任务筛工具子集），让 logit 层没有势均力敌的候选。
- 提升层：工作流（工具集设计）。

### 独点3：工具数是精度旋钮，OpenAI 官方建议 <20，超 10-12 拆 sub-agent（工具层）
- 判据：工具菜单长度直接拉低选择精度（OpenAI 硬上限 128 但官方建议瞄准 <20）；超过 10-12 个相似工具时，架构上把工具按子域拆给专门 sub-agent，每次只给主 agent 一个低重叠子集。判据：**不是越多工具越强，是菜单越短越准**。
- 独有增量：与 r169B 技能市场重叠不同，本条是**运行时注入工具数的硬上限与拆集机制**，有官方数字锚点。
- 提升层：工具。

## 判非重复理由
- r166B 函数调用可靠性=调用后重试/幂等；本条=调用前选择错误的根因与描述工程，增量 >40%。
- respan"错误返回文本非异常"、zylos"分开 query/update 工具"多源重叠 >60% 只留证据。
