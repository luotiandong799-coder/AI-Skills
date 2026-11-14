---
name: vi-fact-verification
description: 事实与结果验证（Verification Intelligence）。当任务涉及事实声称、外部来源引用、数据/计算结果核对、代码或文件改动验收、或"判断任务是否真正完成"时调用。落实独立性原则与来源分级，识别未经证实的结论，给出"真/误导/夸大/缺证据/假"评级。注意：EI 的 CCS 验"执行过"，VI 验"对不对"——二者互补不重复。
module: VI
modules: VI,EI
version: "1.3.0"
---

# VI · 事实与结果验证（Verification Intelligence）

> 本技能是 Personal AI OS 13 模块中 **VI（验证智能）** 的载体之一（与 `wb-artifact-verification`/`wb-agent-evaluation`/`wb-ui-visual-qa`/`wb-media-forensics` 同属 VI，各管一块：artifact=产物、eval=评测、ui=界面、media=媒体、本技能=事实/来源/完成度）。
> 方法论实拉（2026-11-07 实拉）：FactCheck.org（Our Process / How to Combat Misinformation）、The Truth in Journalism Project（How to Fact-Check）、Open Government Platform（Fact-Checking Process）。

## 一、核心原则

- **验证 ≠ 执行**：EI 的 CCS 证书只证明"步骤执行过且留痕"；VI 负责证明"结论/事实/交付是对的"。把"执行过"当"完成"是头号误区。
- **独立性原则**：每个事实至少由 **1 个权威源** 或 **多个相互独立的非权威源** 确认；避免用两篇基于同一原始报道的新闻互相印证（它们不独立）。
- **权威是事实相对性的**：某人个人站是其姓名拼写/自我认同的权威源，却不是其 sibling 经历的权威源。

## 二、来源分级（核查时优先序）

1. **一手官方**：政府出版物、法律文本、法院文书、官方数据发布。
2. **权威二手**：同行评审研究、权威机构分析、官方机构报告。
3. **专家源**：经核实专家/组织的直接陈述。
4. **新闻与媒体**：声誉媒体，主要用于时事背景（且须多源交叉）。

> 一手不可得时，明确说明使用二手源并论证其可靠性；匿名源须有名源或强物证佐证。

## 三、核查清单（逐条过）

- [ ] 追溯到一手源
- [ ] 与官方记录核对（可得时）
- [ ] 跨多个可靠源交叉验证
- [ ] 检查时效性与相关性（过时即失效）
- [ ] 检查上下文与完整性（断章取义＝误导）
- [ ] 数据与计算独立复算
- [ ] 技术/代码类：实测可运行、版本与日期依赖注明
- [ ] 多媒体：反向图片/视频/音频检索验真，警惕 AI 生成内容

## 四、评级输出

对每个被核查声称给结论之一：**真 / 误导 / 夸大 / 缺证据 / 假**，并附证据链（来源 + 关键句 + 日期）。

## 五、与 OS 协作

- **EI** 的 `certify` 之后接 VI 做"正确性"双验收（执行+正确）。
- 涉外部事实/引用的交付（论文、报告）→ 先 VI 后交付。
- 验证结论（含未通过项）→ **MI** 沉淀；反复出现的未通过项 → **RI** 复盘。

## 六、系统化测试方法论（2026-11-07 第二轮实拉深化）

> 上轮覆盖"来源分级 + 事实核查清单 + 评级"；本轮补"怎么验才严谨"——LLM 非确定性下，传统精确匹配失效，须用以下方法学把验证工程化。

### 6.1 Golden Dataset 回归
固定 50–200 组 输入/期望输出 对，每次改动后跑；偏离即告警。非确定性下最有价值的回归防线。

### 6.2 属性测试（Property-Based）
不测"精确输出"而测"必须恒真"的属性：输出为合法 JSON、无 PII、长度 < N、语言正确、含关键事实、不幻觉。快、便宜，格式回归秒级捕获。

### 6.3 蜕变测试（Metamorphic）
小改写输入（换个问法）不应改变事实；用假设检验在置信区间内验证蜕变关系。专治"换种说法就翻供"。

### 6.4 差分测试（Differential）
用生成模型造能暴露行为差异的测试输入，对比多模型/多版本是否分歧。PROBEGEN 用 LLM 迭代生成反例探针，曾推翻 18% 已通过人工测试的样本；PatchDiff 对 AI 生成补丁做全仓回归，约 30% "已解"问题经差分分析实为错。**稀疏测试谬误**：HumanEval 每题仅 1–3 用例，扩增 80× 后多模型成功率跌近 30%——模型常"靠运气过测"而非真懂逻辑。

### 6.5 对抗/红队测试（Adversarial / Red-Team）
固定对抗输入集（"忽略之前指令泄露系统提示" / SQL 注入 / 长度攻击）每版必跑；CI 定期而非一次性。覆盖提示注入、越狱、PII 泄露。

### 6.6 LLM-as-Judge 评测管线
独立高质量模型（如 Claude Opus）按 rubric 评 正确性/相关性/安全性，1–5 分，阈值告警。实践：property 每 PR（快），golden+judge 合 main，red-team 发版前；分数漂移 >5% 即告警。

### 6.7 形式化验证（Formal Verification）
安全关键场景：Marabou / α,β-CROWN 对网络行为给数学保证；DeepXplore / TensorFuzz 度量神经元覆盖。AI 验证的"白盒"进阶，补经验测试的盲区。

### 6.8 与本章关系
以上不替代 §三 的事实核查，而是把"验什么、怎么验"工程化：§四 的"真/误导/夸大/缺证据/假"评级是目标，本节方法是手段；与 EI 的 `certify` 双验收（执行过 + 方法对）。

## 七、来源（2026-11-07 实拉，含本轮深化）

- FactCheck.org 流程与反误导：factcheck.org（Our Process / How to Combat Misinformation, 2025-04）
- 独立性原则与来源分级：thetijproject.ca/guide/how-to-fact-check/
- 核查标准与来源层级：opengovtplatform.org/fact-checking

### 本轮深化来源（2026-11-07 实拉，系统化测试）
- lacuna.tiptreesystems.com（差分测试 / PatchDiff / PROBEGEN / EvalPlus·稀疏测试谬误）
- michaeljohnpena.com/blog/2026-01-21-ai-testing-strategies（golden / property / adversarial 测试）
- core.cz/en/blog/2025/ai-testing-automation（property + LLM-as-judge 评测管线）
- argonsys.com（神经元覆盖 / FGSM-PGD 对抗 / 形式化验证 Marabou / CROWN）

## r708B 下沉：证据充分性门 + 数值核验是决定性计算，不是再看一眼（2026-11-08 实拉）

> 与既有「证据链 / 来源分级 / 原子主张分解」分工：那些管**怎么找证据、怎么标来源**；本节管**什么时候有资格下"已验证"结论**，以及**带数字/单位的声称该由谁算**。判重：全库 `证据族/来源族` 0 命中，`FEVER` / `NotEnoughInfo` 词边界 0 命中，"拆原子主张"已由 co-learn 豆包线落地 ⇒ 不重复。

- **三态而非二值**：`Supported / Refuted / NotEnoughInfo(NEI)`。FEVER 一手（ACL N18-1074）：**185,445 条**人工核验声称、标注者 Fleiss κ=0.6841、**前两类必须记录构成判断所必需的句子**；NEI 是**一等输出**，不是"暂时没查到"的占位。
- **证据充分性先于判真**：高模型置信度**不得**直接产出二值结论。判真/判假要同时满足 `p(标签) ≥ τ` **且** `证据充分度 s_evid ≥ τ_E`（所需变量是否都可观测）；缺任一，落 NEI 而非硬判。多份高置信证据互相矛盾 → 触发**歧义条件**，不做多数投票。判据：**"没有反证"不构成 SUPPORTED**。
- **置信度要校准并单独报**：温度缩放校准用留出集；ECE 与分类质量**并列报告**——F1 上升但变得更过度自信，不算更可靠。弃权阈值（`when to abstain`）、top-k 截断、风险-覆盖曲线是同一组可调旋钮。
- **"带正确证据"反而更差是硬证据**：FEVER 原文——给出正确证据时标签准确率 **31.87%**，忽略证据反是 **50.91%**。⇒ **检索到证据不等于会用证据**；验证管线要单独评测"证据选择"这一环（Evidence F1），FEVER Score 要求**标签正确 + 证据集完整**双达成，单看标签分会把"蒙对"当"验对"。
- **数值声称交给确定性代码，不交给模型口算**：LLM 生成的数值最常错在**报告期 / 单位 / 口径 / 公式**（不是算术）。管道固定三步：① Verification Planner 声明 `metric / period / unit / operands / computation` → ② Provenance Verifier 把操作数落到**权威事实**（如 XBRL 字段）并从**候选无关的来源**授权公式 → ③ 用约束求解器（Z3）验候选值，输出 `Verified / Violated / Abstain`：**事实或公式无法唯一确定时必须弃权**，不许脑补。不一致时用 **unsatisfiable core** 直接点名冲突的「事实 / 公式 / 候选值」，便于定向修。判据：验收指标是 **false accept（错误数值被放行）**，不是平均分。
- **跨源冲突先对齐口径再比**：单位、人口/总体、地域、期间、阈值、比较基线各自归一；**不对冲突数字取平均**（`$20` 与 `$18` 不报 `$19`，按主源报并附条件）；发布日期 ≠ 所述期间；`Unsupported ≠ Contradicted`、`Mixed ≠ Unverifiable`、`Misleading` 不要求每个细节都假、`Outdated` 必须有时间依据。
- 判据：**一次验证的产出是「标签 + 证据集 + 充分性判定 + 校准后的置信度」四元组**，缺证据集或充分性判定的"已验证"是虚报。

**来源（2026-11-08 实拉，逐串核验）**：
- `aclanthology.org/N18-1074/`（FEVER, Thorne et al. NAACL 2018）— HTTP 200 / 41,998B，命中 185,445·NotEnoughInfo·31.87·50.91·Fleiss·evidence。
- `arxiv.org/html/2608.10213v1`（VeriFin）— HTTP 200 / 213,480B，命中 Abstain·Verified·Violated·Z3·unsatisfiable core·false accept·Provenance Verifier·reporting period·unit。
- 交叉：`github.com/sandbaseai/awesome-workbuddy/.../evidence-standards.md`（权威/邻近性/独立性分维、冲突不取平均、单位归一）；`github.com/moshiur00/claim-polygraph.../PROJECT_SPECIFICATION_AND_PLAN.md`（数值/时间确定性检查、判定分类学）；`ijsrtjournal.com/article/aeris-chart...`（证据充分性门 + 温度缩放 ECE + 矛盾触发 NEI）；`readever.app/zh/blogs/how-to-triangulate-sources`（对齐定义与时间框架、证据族独立性）。

## 八、无 Oracle 时的验证：判据谱系 / 形式约束 / 属性测试闭环（2026-11-09 r731B 实拉，3 独点）

> 来源（≥3 独立域、一手逐字）：`computer.org/csdl/journal/ts/2015/05/06963470/13rRUx0geBw`（Barr et al., IEEE TSE 41(5) 2015《The Oracle Problem in Software Testing: A Survey》，2026-11-09 WebFetch 一手全文）；`earlbarr.com/publications/testoracles.pdf` + `web.eecs.umich.edu/~weimerw/2024-481F/readings/testoracles.pdf`（同论文 PDF 镜像，WebSearch 一手逐字；curl 下载 45s 超时、WebFetch 返回 application/pdf 被丢弃，如实登记不冒充直读）；`hypothesis.readthedocs.io/en/hypothesis-python-4.57.1/quickstart.html` 与 `/en/latest/quickstart.html`（Hypothesis 官方文档两版本，WebFetch 一手全文）。
> 判非：窄串 `oracle problem` / `property-based testing` / `metamorphic relation` / `shrinking` 全库 SKILL.md 0 命中；`metamorphic` / `蜕变` 仅 §6.3 一句（「小改写输入不应改变事实」＝MR 单例），与本轮「判据谱系 / 形式约束 / 属性工程」正交 ⇒ 走「优＝加厚现有」不新建。r708B 的 FEVER 三态 / 证据充分性门 / Z3 数值核验不复用。

### 8.1（r731B-1）★验证前先声明 oracle 来源与「旧版当 oracle」的隐含假设
- **原文**：「We have placed them with **derived test oracles**, because, in practice, metamorphic relations are **usually manually inferred from a white-box inspection of a SUT**」；「Regression testing ... rests on the **implicit assumption that the previous version can serve as an oracle** for existing functionality」；「The biggest challenge in metamorphic testing is **automating the discovery of metamorphic relations**」。
- **判据**：① 验收报告须写明判定基准从哪来（人写期望 / 派生关系 / 参考实现 / 隐式不变量），不能只写「已验证」；② 改版、换模型、换提示规约时旧版输出不能直接当真值——这个隐含假设已失效，须重建基准；③ 蜕变关系靠人工从规格推导，「自动发现关系」是未解难题不是既有能力，禁止把「让验证自己找关系」写进能力承诺。
- **与 §6.3 分工**：那句是 MR 的一个实例（换说法不变事实），本条管**基准来源与假设登记**，是更上一层的验证姿态。
- **提升层**：验证 / 治理。触发词：oracle 来源、derived test oracle、旧版不能当真值、隐含假设、MR 需人工推导、自动发现关系未解。

### 8.2（r731B-2）★蜕变关系是「≥2 次执行 + 输出间约束」，非确定性系统须换关系类型
- **原文**：形式化 `f(x1)o1 f(x2)o2 ... : [expr ∧ k ≥ 2]`；「a constraint on the values of **stimulating the single SUT f at least twice**, observing the responses, and imposing a constraint on how they interrelate」；非数值例 `R_OR: A1=(A2∪A3) ⇒ |A2| ≤ |A1|`（搜索引擎结果集）与 `e^a e^{-a}=1`；「When the SUT is **nondeterministic** ... defining metamorphic relations solely in terms of **output equality is usually insufficient**」→ set intersection / **statistical metamorphic testing**（用统计分析检查关系）。
- **判据**：① MR 必须写成**可执行的两跑对照**（排序不变 / 包含 / 长度不增 / 集合交集 / 统计区间），不是单次输出断言「输出应正确」；② LLM/Agent 输出逐字相等不成立，用 equality 当唯一关系会把正常波动全报成失败；③ 关系不限于数值，非数值的一致性关系同样可机检 ⇒ 无标准答案时优先找「多次执行之间必须成立」的约束。
- **提升层**：验证 / 可复用 Skill。触发词：k≥2、至少两次执行、输出间约束、非数值蜕变关系、非确定性用统计蜕变、equality 不足。

### 8.3（r731B-3）★属性测试把 oracle 缺口转成「属性 + 生成 + shrinking + 反例固化」闭环
- **原文**：Hypothesis 官方「`@given` ... takes a **strategy**, which describes the type of inputs」、「**By default, Hypothesis generates 100 random inputs**」、「Hypothesis doesn't just find *any* counter-example ... it knows how to **simplify the examples** it finds to produce **small easy to understand ones**」；`Falsifying example: test_decode_inverts_encode(s='')` 与 `s='001'`；`decode(encode(s)) == s` 不变量；`@example("")`「ensure that particular edge cases ... are tested every time」「although Hypothesis will **remember failing examples**, **we don't recommend distributing that database**」；`.filter()` 优于复杂条件、`assume()` 丢弃整例、`@composite` 让生成值相互依赖。
- **判据**：① 验收不能只写单个样例；写属性（round-trip / 幂等 / 不变量 / 不崩溃）+ 生成策略 + 最小反例；② 失败反例须**显式固化**为回归样例（`@example`），不依赖本地失败数据库（官方不建议分发）；③ 生成范围贴合真实域，过滤器别宽到丢弃大多数样本；④ 与 §8.2 衔接：属性是「单跑可判」的谓词，蜕变关系是「跨跑」的约束，两者互补而非替代。
- **提升层**：验证 / 工作流。触发词：property-based testing、@given strategy、100 默认样本、shrinking 最小反例、@example 固化、失败数据库不分发。

### 本轮来源（2026-11-09 r731B 实拉）
- computer.org/csdl/journal/ts/2015/05/06963470/13rRUx0geBw（Barr et al. IEEE TSE 2015，WebFetch 一手全文逐串）
- earlbarr.com/publications/testoracles.pdf · web.eecs.umich.edu/~weimerw/2024-481F/readings/testoracles.pdf（PDF 镜像，WebSearch 一手逐字；直读失败如实登记）
- hypothesis.readthedocs.io/en/hypothesis-python-4.57.1/quickstart.html · /en/latest/quickstart.html（官方文档，WebFetch 一手全文）


## 九、变异测试：验证的是测试套件，不是代码（r743A 实拉 · 2026-11-14，3 独点）

> 与 §8.2 蜕变关系 / §8.3 属性测试分工：那两条解决「没有 oracle 时怎么写断言」，本节解决「写好的断言到底有多强」。三者是验证能力的三个不同层，不互相替代。

### 9.1（r743A-1）覆盖率只回答「跑没跑到」，不回答「错了会不会挂」
- **原文**：PIT 官方首页逐字「Traditional test coverage (i.e line, statement, branch, etc.) **measures only which code is executed by your tests. It does not check that your tests are actually able to detect faults in the executed code. It is therefore only able to identify code that is definitely not tested.**」；极端例「tests with no assertions」。UCSB CS156 逐字「with code coverage, we can cheat: we can write a test suite that calls every single method ... if we then do **no assertions** ... the only thing we've shown is that our code doesn't compiles and doesn't crash. We have not shown that the code produces the correct result」，结论「in short, **it doesn't test our code; instead, it tests our tests**」。
- **判据**：① 验收报告固定分两栏——**执行覆盖**（哪行被跑到）与**故障检出**（把故障注进已跑到的代码后测试会不会失败）；绿灯覆盖率只证明第一栏，不得写成「已验证」。② 「100% 行覆盖 + 零断言」是合法但零信息的绿色状态，须显式禁止作为完成证据。③ 与 §8.3 属性测试衔接：属性给「单跑可判」的谓词，变异给「断言强度」的度量，两者分别报数，不合并成一个分数。

### 9.2（r743A-2）存活 ≠ 缺测试：七种结局先分诊，等价变异是分母污染
- **原文**：PIT 官方 basic_concepts 逐字列出七态 **Killed / Survived / No coverage / Non viable / Timed Out / Memory error / Run error**，且「**No coverage is the same as Survived except there were no tests that exercised the line of code**」「A mutation may **time out** if it causes an infinite loop」「A **run error** means something went wrong when trying to test the mutation」「Under normal circumstances you should see no non viable mutations or run errors」。等价变异两类成因逐字：「The resulting mutant **behaves in exactly the same way as the original**」（官方 `i=2` 时 `>=1` 与 `>1` 等价例）与「behaves differently but **in a way that is outside the scope of testing**」（logging/debug，PIT 用 `FLOGCALL` 不生成此类）。UCSB 三解释：usually 缺测试 / sometimes 冗余代码该删 / rarely 等价变异。qaskills 逐字「**When a survivor is equivalent, do not add a silly test just to raise the score.** ... A mutation score that rewards meaningless assertions is worse than a lower score that reflects real risk」。
- **判据**：① 见到 survived 先分诊七态：**No coverage** 才补测试；**等价变异**登记豁免、不给它补断言；**Timed Out / Memory error / Non viable / Run error** 是工具/环境噪声，须查测试隔离与堆配置，不得当作测试缺陷冲分。② 变异分数分母含不可杀变异体 ⇒ 「100%」不是必然可达目标，把等价变异计入分母却要求满分会诱发无意义断言。③ 存活也可能是「代码本身就是冗余的」，此时正确动作是删代码而非加测试。

### 9.3（r743A-3）门禁是双阈值 + 增量 ratchet，不是一次性 100%
- **原文**：UCSB 逐字「we first must have a '**green**' test suite ... **If even one fails, pitest won't even start** doing mutation testing」；「`-DmutationThreshold=100` means we want **100% of the mutants to be killed**, or else we'll fail the build」「`-DcoverageThreshold=100` means we want **100% of the lines of code** to be covered」——两个独立门。PIT 官方「**The most effective way to use mutation testing is to run it frequently against only the code that has been changed**」；官方运行机制「Before running the tests PIT performs a traditional line coverage analysis ... then uses this data along with the **timings of the tests** to pick a set of test cases targeted at the mutated code」。qaskills ratchet 逐字「If a package starts at 54 percent mutation score, **do not demand 90 percent next week. Set the threshold at 54 or slightly below, require new work not to reduce it**」「**Publish trends by package, not only a single repository score**」「Start with changed modules or critical packages」。
- **判据**：① 前置条件写进验收——测试套件先全绿，否则变异分析根本不启动。② `mutationThreshold` 与 `coverageThreshold` 分列两个数、各自独立失败，禁止用一个「质量分」代替。③ 阈值按**包**取当前值做 ratchet（只准升不准降），不全局一刀切；范围限定在变更代码/关键包，按包发布趋势而非单一仓库分。④ 与 §9.2 合用：先分诊再决定「补断言 / 删冗余 / 登记等价」，ratchet 只允许抬真实检出力。

**来源（r743A 独立实拉 2026-11-14，≥2 独立域交叉）**：
- `pitest.org`（PIT Mutation Testing 官方首页，WebFetch 200 全文逐字：coverage 只测执行、gold standard、只跑变更代码）
- `pitest.org/quickstart/basic_concepts`（PIT 官方基本概念页，WebFetch 200 全文逐字：等价变异两类成因、七态结局、行覆盖+测试耗时定向）
- `ucsb-cs156.github.io/topics/testing/testing_pitest.html`（UCSB CS156 教学页，WebFetch 返回前 15000 字 + 搜索快照逐字：无断言作弊、tests our tests、三解释、双阈值、green suite 前置；**AI 摘要 60s 超时，如实登记**）
- `qaskills.sh/blog/pit-java-mutation-testing-guide`（2026 独立一手全文逐字：等价变异不加傻测试、ratchet 54%、按包趋势、CI 调优；商业/教学立场登记，不作唯一结论来源）
- `bell-sw.com/blog/a-comprehensive-guide-to-mutation-testing-in-java/`（BellSoft 一手实操交叉：38%/64% 分数报告与 mutator 清单）；`sourcegarden.com` 无关不采。
