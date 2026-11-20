---
name: vi-fact-verification
description: 事实与结果验证（Verification Intelligence）。当任务涉及事实声称、外部来源引用、数据/计算结果核对、代码或文件改动验收、或"判断任务是否真正完成"时调用。落实独立性原则与来源分级，识别未经证实的结论，给出"真/误导/夸大/缺证据/假"评级。注意：EI 的 CCS 验"执行过"，VI 验"对不对"——二者互补不重复。、多重检验校正、FWER、FDR、Bonferroni、Holm、Benjamini-Hochberg、q值、family边界、假阳性膨胀、SelfCheckGPT、采样一致性幻觉检测、零资源黑盒、AUC-PR、谱偏倚、验证偏倚、spectrum effect、two-gate case-control、single-gate cohort、work-up偏倚、预设指标、conformal prediction、保序预测、覆盖保证、非一致分数、split conformal、CQR、marginal与conditional coverage、覆盖率引导模糊测试、coverage-guided fuzzing、SanitizerCoverage、corpus、变异策略、crash最小化、基准污染、benchmark contamination、去污染、decontamination、n-gram overlap、成员推断MIA、canary string、推理时去污、模糊重复fuzzy duplicate
module: VI
modules: VI,EI
version: "1.11.0"
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
## 十、评估独立性：验证分数虚高可能来自管线，不是模型（r748A 实拉 · 2026-11-15，3 独点）

> 适用：任何用留出集 / 交叉验证 / 评测集给结论打分的验证场景（模型选型、Agent 评测、检索质量、脚本验收）。
> 与 §九分工：变异测试测「断言有多强」；本节测「评估流程本身有没有偷看答案」。二者互补，不重述。

### 10.1（r748A-1）★泄漏的定义是「预测时拿不到的信息被用进建模」，不是「偷看了测试集」
- scikit-learn 官方 1.9.1《Common pitfalls》§12.2 逐字：「**Data leakage occurs when information that would not be available at prediction time is used when building the model**」；后果固定为「**overly optimistic performance estimates** … poorer performance when the model is used on actually novel data」。
- 官方硬数字反例（200 样本 / 10000 随机特征 / **完全随机的标签**，理论准确率 ≈0.5）：先在全数据做 `SelectKBest(k=25)` 再切分 → `accuracy_score` = **0.76**；先切分、只在训练集 fit 选择器 → **0.5**；用 `Pipeline` + `cross_val_score` → **0.43±0.05**。
- 判据：**随机标签基线是泄漏探针**。给数据换成随机标签后分数线仍显著高于 chance，说明泄漏在评估管线里，不是模型学到了东西；验收报告先声明「baseline on random labels = X」，再看真实分数。绿灯高分本身不构成「已验证」。
- 与 §9.1（覆盖率只测执行）对齐：一个虚高的分数和一个虚高的覆盖率是同一类错误——把「测到了」当成「测对了」。

### 10.2（r748A-2）★`fit` / `fit_transform` 与 `transform` 是两道门，Pipeline 是结构性防线
- 官方 §12.2.1 三条硬规则逐字：①「**Always split the data into train and test subsets first, particularly before any preprocessing steps**」；②「**Never include test data when using the `fit` and `fit_transform` methods**」，`fit(X)` 会给过于乐观的分；③ `transform` 应当同时用于 train/test（train 上 `fit_transform`，test 上 `transform`）。
- 泄漏面覆盖「almost all transformations … including (but not limited to) `StandardScaler`, `SimpleImputer`, and `PCA`」——缩放均值、插补统计量、PCA 基、特征选择、文本词表、重采样，凡从数据里学出来的都算。反例：归一化用全数据均值时「information from the test subset is influencing the model」。
- 同一文档 §12.1 给出**反方向的错**：train 缩放而 test 不缩放 → MSE **62.80**，两侧都变换 → **0.90**。⇒ 两个方向都要测：把 test 信息带进 fit 是虚高，漏给 test 做 transform 是虚低，症状相反但根因都是变换边界没声明。
- 判据：**验收报告逐项声明每个 `fit` 的数据边界**（哪个对象、在哪个 split 之后、只吃哪些行），并优先用 `Pipeline` 把「学」与「应用」绑成一个对象；手工 `fit_transform` 调用链一律列为高风险。只报分数不报 fit 边界 = 未验证。

### 10.3（r748A-3）★嵌套 CV 的内外环按「谁看了什么」分；折叠结构必须匹配部署时「新数据」的含义
- 内外环职责（TechBloat / RottenWiFi / Jypi 三独立域快照逐字交叉）：**内环**承担全部数据依赖决定——超参、模型族、特征集、阈值选择、概率校准、早停点、评分指标（「If a threshold is selected after reviewing outer-fold predictions … the outer estimate is no longer a clean evaluation」）；**外环**只做一次性能估计，只报外层分数分布（mean ± std），**禁止把 inner best score 当最终性能**（「the clean estimate comes from the outer loop, not from the final tuning run」）。
- 阈值/校准/早停属于调参，不是后处理：看完外层预测再挑阈值，等于让外层参与了选择，估计不再干净。嵌套 CV 的输出是「这套建模过程的性能估计」，不是最终那个模型；部署前需在全部训练数据上 refit。
- 折叠策略按数据结构选，不是默认 KFold：类别不平衡 → `StratifiedKFold`；同一患者/客户/设备/家庭的多条记录 → 组感知切分（官方 `GroupKFold` 逐字「**Each group will appear exactly once in the test set across all folds**」）；时序预测 → `TimeSeriesSplit` + 必要时 embargo，匹配预测视界与重训节奏。
- 判据：**「技术上正确的嵌套流程仍可能答错问题」**——嵌套 CV 修不了跨折重复样本、非代表性抽样、标签错误、以及「预测时根本拿不到的特征」。验收固定四问：切分单位是什么、同组是否跨折、时间是否穿越、哪些特征在预测时不可得。四问答不出，分数作废。

**提升层**：可复用 Skill（验证协议）/ 工作流（评测管线准入清单）/ VI 验证（评估独立性）。触发词：data leakage、nested cross-validation、outer loop、fit_transform、Pipeline、GroupKFold、TimeSeriesSplit、threshold selection、随机标签基线、评估管线偷看。

**来源（r748A 独立实拉 2026-11-15，≥2 独立域交叉，逐字核验）**：
- `https://scikit-learn.org/stable/common_pitfalls.html`（scikit-learn **1.9.1 官方文档** §12.1/12.2/12.2.1/12.2.2，WebFetch **200 全文逐字**：泄漏定义、0.76/0.5/0.43±0.05、62.80/0.90、三条防泄漏规则、Pipeline + cross_val_score 用例）——**第一独立域（官方一手）**。
- `https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html`（scikit-learn 1.9.1 官方 API 页，WebFetch **200 全文逐字**：「Each group will appear exactly once in the test set across all folds」、`shuffle`/`random_state` 1.6 起、`n_splits` 默认 0.22 从 3 改 5）——**第二独立域（同官方不同规范页）**。
- `https://scikit-learn.numpy.tw/1.6/common_pitfalls.html` 与 `/1.8/common_pitfalls.html`（中文镜像 1.6/1.8 双版本，WebSearch 快照逐字：「永遠不要在測試資料上呼叫 fit」「特徵選擇應僅使用訓練資料」）——**第三独立域（版本化镜像，交叉核验口径跨版本一致）**。
- `https://www.techbloat.com/nested-cross-validation-for-machine-learning-with-python.html` · `https://rottenwifi.com/nested-cross-validation-why-it-matters-and-how-to-use-it-in-python` · `https://jypi.org/topics/machine-learning-with-scikit-learn-1`（三独立教学/技术域，WebSearch 快照逐字：内外环分工、inner best score 禁作最终性能、内层须含阈值/校准/早停/指标选择、StratifiedKFold / GroupKFold / TimeSeriesSplit + embargo、嵌套 CV 修不了重复样本与标签错误；教学立场登记，不作唯一结论来源）。
- **判非**：`nested cross` / `train-test contamination` / `group k-fold` / `preprocessing leakage` / `temporal leakage` / `cross-validation pitfall` / `feature selection inside` 全库 `SKILL.md` **0 命中**；`data leakage` 1 命中属豆包自留地 `engineering/wb-execute-discipline`（术语表），`leakage` 5 命中分别属 CI 上下文、安全、写作、实验语境，均异命题。与 §9.1/9.2/9.3 变异测试族、§8.x 无 oracle 族分工明确（那条管断言与 oracle，本条管评估流程的独立性）。按 rules/07 去重铁律「优＝加厚现有」，不新建。豆包自留地 **WB 0 落地**。


## 十一、多重检验校正：错误率承诺、依赖结构与 family 边界（r756B 实拉 · 2026-11-15，3 独点）

> 与 §十 r748A（评估管线泄漏让分数虚高）、§九 r743A（变异测试测的是测试套件）、§八（无 oracle 怎么写断言）分工：那三条管**单个分数/单条断言**是否可信，本条管**同时下 N 条判定**时「至少一条显著」的联合假阳性。按 rules/07「优＝加厚现有」不新建。

### 11.1 「显著」是 family 属性，不是单条结论属性
- NBIS（瑞典国家生物信息基础设施《Statistical Methods for Life Sciences》§12.2）逐字：`P(No type I errors in m tests) = (1 − α)^m`、`**P(At least one type I error in m tests) = 1 − (1 − α)^m**`；CASRAI 给出读数「At m = 5 that is about **23%**; at m = 20 it is about **64%**; at m = 100 it is effectively certain」。
- 判据：验证报告若同时跑多条断言 / 多个指标 / 多个子组 / 多组两两比较，必须**先声明 family 边界与 m**，再谈其中某条 p<0.05。「我们跑了 20 项检查、其中 1 项显著」在无校正时是**预期内的噪声**，不构成发现。与 §十的泄漏探针同样属于「绿灯 ≠ 已验证」，但成因正交：泄漏是数据边界被污染，多重检验是判定数量本身抬高假阳性。
- 输出固定四栏：`family 定义 / m / 未校正联合假阳性 1−(1−α)^m / 校正方法与结果`。缺前两栏，任何单条 p 值不得写成结论。

### 11.2 FWER 与 FDR 是两种承诺，不是「严格程度」的刻度
- NBIS §12.2 逐字：「**FWER: family-wise error rate, control the probability of one or more false positive P(N_FP>0)**」；「**FDR: false discovery rate, control the expected value of the proportion of false positives among hits (rejected hypotheses), E[N_FP/(N_FP+N_TP)]**」；cttir 教程给标准式 `FWER=P(V≥1)`、`FDR=E[V/max(R,1)]`。
- CASRAI 逐字：「**A 5% FDR does not mean any single result has a 5% chance of being wrong**; it means that, on average, no more than 5% of everything you called "significant" is expected to be a false positive」；「the FDR is **a property of the whole rejected set, not of each p-value in isolation**」。⇒ q 值不得降格为「这条结论有 5% 概率是错的」。
- 选型按**代价**不按「哪个更严谨」（CASRAI：「a decision about the cost of a false positive relative to the cost of a false negative in your specific study, **not a rule about which procedure is "more rigorous" in the abstract**」）：确认性 / 监管 / 一个假阳性即灾难 → FWER（Bonferroni / Holm）；探索性大批量筛查、宁可短名单里混几条错 → FDR（BH）。与 §十「false accept 是验收指标」呼应，但本条给的是**一批判定的错误率口径**。

### 11.3 方法受依赖结构约束；family 须事前冻结；校正救不了欠功效
- **依赖结构**（statsmodels 0.15.0 官方 API 逐字）：方法清单 `bonferroni / sidak`（one-step）、`holm-sidak / holm`（step-down）、`simes-hochberg`（step-up, independent）、`hommel`、`fdr_bh : Benjamini/Hochberg (non-negative)`、`fdr_by : Benjamini/Yekutieli (negative)`、`fdr_tsbh / fdr_tsbky`（two stage）、`fdr_gbs`、`lfdr`；Notes「**All procedures that are included, control FWER or FDR in the independent case, and most are robust in the positively correlated case**」。NBIS §12.4：「The Benjamini-Hochberg procedure controls the FDR level … **under the assumption of independence (and also under certain forms of positive dependence)**」；CASRAI：「The standard Benjamini-Hochberg procedure assumes independence or positive regression dependence among the tests; under arbitrary or negative dependence, **the more conservative Benjamini-Yekutieli variant is the correct choice**」；「**Bonferroni is valid under any dependency structure**」。
- **Holm 无代价优于 Bonferroni**（CASRAI 逐字）：「it is a step-down procedure that still guarantees FWER control (unlike FDR methods) but is **uniformly more powerful than plain Bonferroni** … **Holm-Bonferroni dominates plain Bonferroni with no downside**」；artofds 目录页逐字「**Holm over Bonferroni, always. Same promise, and never fewer findings**」。⇒ 需要 FWER 且 m>少量时默认取 Holm，不取 Bonferroni。
- **α 与校正 p 值解耦**（statsmodels Notes 逐字）：「**Except for 'fdr_twostage', the p-value correction is independent of the alpha specified as argument. In these cases the corrected p-values can also be compared with a different alpha**」；两阶段法例外（「the corrected p-values are specific to the given alpha」）。⇒ 改判定阈值不必重算校正值，除非用了 `fdr_tsbh/fdr_tsbky`。
- **family 按推断目标定义、事前冻结**（cttir 逐字）：「Correct for all tests that belong to the same family; **a family is defined by the inferential goal, not by software runs**」；「**Pre-specify the family and the method in the protocol; post-hoc changes to the correction are data-snooping**」；CASRAI「**Define the family before you see the results**」「Running a correction only over the tests that already looked promising, after seeing all the results, defeats the purpose and is **a form of p-hacking**」。⇒ 只把显著的那几条拿去校正 = 无效；须留「事前冻结的 family 清单 + m + method」三项可核查记录。
- **校正不修功效**（CASRAI 逐字）：「**A correction does not rescue an underpowered study**」「A large, all-null result after correction can mean there is genuinely nothing there, **or it can mean the study was never powered** to detect the effect once the multiplicity penalty was applied — distinguishing the two requires a power calculation」。⇒ 校正后全不显著只能写「未检出」，不得写「验证通过/无差异」（与 §10.2 配对检验「p≥α 不得写等价」同族，但本条给出功效这一额外排查项）。
- 公式备查（NBIS §12.3–12.5 逐字）：Bonferroni `p ≤ γ/m`、adjusted `p̃_i = min(m·p_i, 1)`；BH step-up「Sort the p-values `p_1≤…≤p_m`. Find the **maximum j** such that `p_j ≤ γ·j/m`. Declare significance for all tests `1,2,…,j`」；BH q 值 `q_i = min((m/i)·p_i, 1)`，解释为「the **lowest FDR** at which the corresponding null hypothesis will be rejected」。⇒ BH 不是逐条独立卡阈值，是**找最大 j 后把前 j 条整批判为发现**，单独拿第 k 条的 q 值做结论会读错。

### 本轮来源（2026-11-15 r756B 实拉）
- `https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html`（**statsmodels 0.15.0 官方 API 页**；`statsmodels.github.io` 请求**重定向到 www.statsmodels.org**，按重定向后 URL 重新 WebFetch 200 全文逐字）— `alpha: FWER, family-wise error rate`、12 种方法清单及 one-step/step-down/step-up 标注、`alphacSidak / alphacBonf`、Notes「Except for 'fdr_twostage', the p-value correction is independent of the alpha」「All procedures … control FWER or FDR in the independent case, and most are robust in the positively correlated case」「fdr_gbs is not verified against another package」、`method='hommel'` 大数组慢（n partitions）。**第一独立域（库官方一手）**。
- `https://nbisweden.github.io/workshop-mlbiostatistics/docs/SM4LS-book/SM4LS-inference/infe_05multiple.html`（**NBIS 瑞典国家生物信息基础设施**官方教程 §12，WebFetch **200 全文 9,501 字逐字**；AI 摘要 60s 超时返回全部原文）— `1−(1−α)^m`、FWER/FDR 两定义、Bonferroni `p≤γ/m`「overly conservative」、BH 三步 step-up、`p̃_i=min(m p_i,1)`、`q_i=min((m/i)p_i,1)` 与 q 值解释、10,000 检验 p/q 对照表。**第二独立域（国家级学术机构教程一手）**。
- `https://casrai.org/guides/bonferroni-correction-and-multiple-comparisons`（CASRAI，发布 2026-08-06 / 更新 2026-09-01，WebFetch 200 全文逐字）— m=5/20/100 的 23%/64%/几乎必然、Bonferroni adjusted α 表（m=2→0.025 … m=100→0.0005）、10 biomarker worked example（**页面自陈「numbers below are constructed for this walkthrough, not drawn from a real study」，按示例登记不冒充实测**）、「the FDR is a property of the whole rejected set, not of each p-value in isolation」、FWER vs FDR 选型按代价、Holm「dominates plain Bonferroni with no downside」、BY 适用任意依赖、「Define the family before you see the results」「A correction does not rescue an underpowered study」。**第三独立域（教学/工具站一手，商业立场已登记）**。
- `https://artofds.com/en/catalogs/multiple-testing`（WebSearch 快照逐字：「**Choose the promise first**」「Two promises, not two strengths」「Holm over Bonferroni, always」「100 independent true nulls tested at 0.05 → about 99.4%」、BY「guaranteed to control the FDR even when the p-values are not from independent tests」、探索/确认分离与 holdout 复用破坏保护）+ `https://cttir.github.io/tutorials/tutorials/inference/multiple-comparisons-overview.html`（快照逐字：`FWER=P(V≥1)` / `FDR=E[V/max(R,1)]`、「a family is defined by the inferential goal, not by software runs」、「Pre-specify the family and the method in the protocol; post-hoc changes … are data-snooping」、R `p.adjust` 五种方法拒绝数 8/8/9/10/7、FDP 是 FDR 在给定数据集上的实现）。**第四、五独立域（教学立场，不作唯一结论来源）**。
- **判非**：`Benjamini` / `fdr_bh` / `multipletests` / `Holm` / `q-value` / `FWER` / `FDR` / `family-wise error rate` / `false discovery rate` 全库 SKILL.md **0 命中**；`Bonferroni` 2 命中、`多重比较` 3 命中逐条查证均为**口号级提及且异命题**——`engineering/wb-agent-evaluation` §10.2/r752A（「多模型先 Cochran's Q 再两两 McNemar + 多重比较校正」，只提需校正未给机制）、`meta/agent-evolution` §r753A 附近（Adobe 对两个以上处理用 Bonferroni 补 family-wise error，主题是 mSPRT 早停）、`research/wb-experiment-design` §36（「多做比较会抬高假阳性，需要 Bonferroni 之类校正」，变体数预算）、`meta/pdi-forecasting` 快照引用（预测示例解析条件）。按「合」登记不重述、不新建并行层。与 §8.2 蜕变关系、§9 变异测试、§10 评估独立性分工明确。豆包自留地 **WB 0 落地**。

## 十二、自一致性幻觉检测：无外部真值时用采样分歧度当信号（r760B 独立实拉 2026-11-17，≥2 独立域一手交叉，3 独点）

> 定位：本节管「**没有权威源、没有外部数据库、只有黑盒模型输出时，怎么给事实性打分**」。与 §二来源分级 / §三 FEVER 三态分工：那两节是**有外部证据**时的核验（拿证据比对声称）；本节是**零资源**（zero-resource）场景的补充手段——拿模型自己对同一问题的多次采样是否一致当弱信号。与 §8.2 蜕变关系分工：蜕变要「同一实现多次执行 + 输出间约束」且需人为设计不变式，本节的不变式是天然的「真事实应被多次采样重现」。与豆包自留地 `wb-context-compressor` §self-consistency 多采样（r648A，CoT majority vote 提答案正确率，**目的是选答案**）分工：那里用一致性**提升**答案质量，本节用一致性**检测**某个具体句子是否幻觉，目的与输出都不同，按「合」引用不重述。**硬约束：自一致性是弱信号，只作排序/预警，不作「真/假」终判**。

### 12.1（r760B-1）核心前提：真事实被多次采样重现，幻觉在样本间发散；两个前置约束是黑盒（无 token 概率）+ 零资源（无外部库）
- **原文**（arXiv:2303.08896《SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative LLMs》Manakul/Liusie/Gales，EMNLP 2023 main，alphaXiv 一手 HTML 全文逐字）：「if an LLM truly 'knows' a fact, multiple stochastic samples generated from the same prompt will be **consistent with that fact**. Conversely, hallucinated information will likely show **inconsistencies across samples**」；两约束「it requires **no access to internal model probabilities (black-box)** and **no external knowledge bases (zero-resource)**」。四步流程：「**Original Response Generation** — low temperature (e.g. 0.0) for deterministic output；**Stochastic Sampling** — N additional samples using higher temperature (e.g. 1.0) to encourage diversity；**Consistency Assessment** — Compare each sentence in the original response against the N samples to compute hallucination scores」。
- **判据**：① 适用前提必须先声明：**模型对该概念「知道」时采样才收敛**；对训练外/长尾事实，采样一致地错也会「一致」——一致性高 ≠ 真，只是「模型稳定地这么认为」。② 温度设定是可复现的关键参数：原答低温（确定性）作基准，N 个探针样本高温（多样性），不写温度无法复现。③ 这是**句子级**信号：判的是原答里每个句子是否被样本支持，不是整段真假；与 §三 FEVER 三态的分工——那里 NEI 是一等输出，这里「样本分歧大」只能报「疑似幻觉/低置信」，不得反推「必假」。④ 与 §一独立性原则不冲突：这里 N 个样本同源，不是独立来源，所以只能当**同一模型的内在一致性自检**，不能当「多源交叉验证」。

### 12.2（r760B-2）五种一致性度量变体共用同一框架；样本数 10–15 后平台化，多采样成本是硬约束
- **原文**（同上 alphaXiv 一手全文逐字）：五变体——「**SelfCheckGPT-BERTScore** uses semantic similarity：`S_BERT(i) = 1 − (1/N) Σ_n max_k BERTScore(r_i, s_{n,k})`」；「**SelfCheckGPT-QA** generates multiple-choice questions from each sentence and evaluates consistency by comparing answers derived from the original response versus the samples」；「**SelfCheckGPT-n-gram** trains n-gram language models (1-gram to 5-gram) using the collected samples and computes hallucination scores from negative log-probabilities：`S_n-gram(i) = max_{token∈r_i}(−log p_n-gram(token))`」；「**SelfCheckGPT-NLI** employs Natural Language Inference models to determine whether sentences … are **entailed by, neutral to, or contradicted by** the samples」（NLI 用 DeBERTa-v3-large）；「**SelfCheckGPT-Prompt** uses an LLM as an evaluator, directly prompting it to assess whether sentences are supported by the sample contexts」。样本量：「Performance generally increased with more samples but **plateaued between 10–15 samples** for most variants」；效率：「even simple approaches like SelfCheckGPT-Unigram … achieved AUC-PR of 85.63 for non-factual detection」。**口径冲突如实登记**：alphaXiv 的 AI 摘要页报「SelfCheckGPT-Prompt achieved the highest AUC-PR of 93.42 … Pearson 78.32 / Spearman 78.30」，而 arxiv.org/html/2401.08358 综述引用原论文表报「combined approach … highest Pearson correlation of 69.05」——两者同指 Sentence-level AUC-PR / Passage-level Corr 但数字不同（疑似不同数据集切分或版本 v1/v3），**不合并、各自标注来源，落地只用「 Prompt/组合变体最优」这一定性结论**。
- **判据**：① 五个变体是**同一框架换一致性度量**，不是五种方法：换的只是「怎么算原句与 N 样本的支持度」（语义相似/QA 答案比对/n-gram 概率/NLI 三分类/LLM 评审），原答+高温采样+逐句打分的主流程不变。② 成本—收益有硬拐点：10–15 个样本后性能平台化，再堆样本只增成本；轻量场景 n-gram 变体（Unigram AUC-PR 85.63）就够，不必上 LLM 评审。③ NLI 变体的 entailed/neutral/contradicted 三态与 §三 FEVER 的 Supported/Refuted/NotEnoughInfo 同构但**来源不同**（前者对比本模型样本，后者对比外部证据），不得互报。④ 数字冲突时按 rules/08 §二「来源冲突保留不确定性」处理：只取各来源一致的定性结论（Prompt/组合最优、10–15 平台期），不挑一个数字当权威；要引用具体 AUC-PR 必须带上「哪一版、哪个数据集切分」。

### 12.3（r760B-3）WikiBio 数据集的三类人工标注与降维结论；适用范围限于传记类且跨模型代理概率不可迁移
- **原文**（同上一手全文逐字）：作者自建数据集，「used GPT-3 (text-davinci-003) to generate Wikipedia-style passages for **238 concepts** from the WikiBio dataset」，人工逐句标注三类「Accurate (0) / Minor Inaccurate (0.5) / Major Inaccurate (1)」，「final dataset contained **1,908 annotated sentences** … **39.9% major-inaccurate, 33.1% minor-inaccurate, and 27.0% accurate**」；样本数实验「diminishing returns beyond 10–15 samples」；局限「The current evaluation focuses primarily on **biographical content**, and extension to other domains remains to be explored」；跨模型「Using proxy LLMs to estimate token probabilities performed **poorly** compared to SelfCheckGPT, indicating that different LLMs have distinct generation patterns that **don't transfer well**」。另（arXiv/html/2401.08358 三星蒙特利尔综述一手全文，WebFetch 200）：三变体 BERTScore/QA/n-gram + NLI(DeBERTa-v3-large) + prompt，238 passages/1908 sentences，标注分布同为 761 major(39.9%)/631 minor(33.1%)/516 accurate(27.0%)，「the combined approach being the best-performing system」。
- **判据**：① 标注三类（准确/轻微不准/严重不准）而非二值，说明「不准」有程度；检测时把 major+minor 合并成 non-factual 是**一种口径选择**，须声明，否则 AUC-PR 数字不可比。② 样本高度失衡（73% 不准 vs 27% 准）——这正是用 **AUC-PR 而非 accuracy** 的原因（与 §10 评估独立性呼应：类别失衡下准确率会虚高）。③ 适用边界要写死：**传记类、有可查事实密度的段落**验证有效；对开放式观点、推理链、创造性文本无证据支持，不得外推。④ 跨模型代理概率不迁移 ⇒ 不能用 A 模型的 token 概率去估 B 模型的自我一致性；本方法必须用**被测模型自己**的高温采样（黑盒特性正好满足）。⑤ 落地为「弱信号预警」：句子一致性分低 → 标记「待人工/外部源核验」（交回 §二/§三流程），不直接判假。

**来源（r760B 独立实拉 2026-11-17，≥2 独立域一手交叉）**：
- `https://alphaxiv.org/abs/2303.08896`（arXiv:2303.08896 Manakul/Liusie/Gales《SelfCheckGPT》，剑桥大学，EMNLP 2023 main，**WebFetch 200 一手 HTML 全文逐字**）— 黑盒+零资源两约束、真事实收敛/幻觉发散前提、四步流程与温度设定、五变体公式（BERTScore/QA/n-gram/NLI DeBERTa-v3-large/Prompt）、WikiBio 238/1908 与三类标注分布、10–15 样本平台期、Unigram AUC-PR 85.63、局限（传记类/跨模型不迁移）。**第一独立域·论文一手**。
- `https://arxiv.org/html/2401.08358`（Samsung AI Center Montreal《Hallucination Detection and Mitigation: An Investigation》综述，**WebFetch 200 一手全文逐字**）— 独立复述 SelfCheckGPT 五变体、238 段落/1908 句、761/631/516 标注分布、combined 最优 Pearson 69.05、AUC-PR 与 Pearson/Spearman 口径。**第二独立域·学术综述一手（交叉核验，数字口径差异如实登记）**。
- `https://arxiv.org/abs/2303.08896` + `https://searcharxiv.com/abs/2303.08896`（官方摘要与镜像，WebSearch 快照逐字，EMNLP 2023 / v3 2023-10-11）· `https://www.alphaxiv.org/zh/abs/2303.08896`（中文版摘要交叉）— 提交历史与作者著录，仅作版本/出处交叉，不单列结论来源。
- **判非**：`SelfCheckGPT` / `采样一致` / `零资源黑盒` / `AUC-PR` 全库 SKILL.md **0 命中**；`self-consistency` 4 命中、`幻觉检测` 2 命中逐条查证全在豆包自留地 `wb-context-compressor`（§self-consistency 多采样 r648A 提答案质量、§RAG 幻觉检测 MARCH 三 agent、§NLI 蕴含检查）与 `wb-execute-discipline`（LLM-as-Judge consistency 协议），**均为异命题且 WB 0 落地**——那里用一致性**选更好的答案**、用外部源/NLI 验 RAG 答案，本轮用同源高温采样分歧度**给单句幻觉打分**，按「合」引用不重述。`NLI` / `DeBERTa` 在豆包自留地 RAG 语境（答案是否扎根检索片段），与本节「原句是否被本模型样本蕴含」不同义。与 §二来源分级、§三 FEVER 三态、§8.2 蜕变、§10 评估独立性、§11 多重检验逐条分工，均不并存。豆包自留地 **WB 0 落地**。
- **未采纳**：BERTScore/QA/n-gram/NLI/Prompt 的完整实现代码、WikiBio 原论文数据集下载链接、alphaXiv AI 摘要与 arxiv html 正文的具体 AUC-PR 数字冲突（只取定性结论，不择一冒充实测）、原子事实级检测与多模态扩展（论文 future work，未验证）。


## 十三、验证结论的「谱」依赖：换个人群/换种评测，准确率就变了（r764B 独立实拉 2026-11-18，≥2 独立域一手交叉，3 独点）

> VI 前面各章管「这个分数是不是被管线/多重比较/采样虚高」，本章管一个更前置的问题：**这个准确率数字本身对它被测量的人群与评测方式有多依赖**。一个在特定样本上验证出的高准确率，换到真实使用人群可能系统性偏高——不是谁造假，是「准确率不是检验的固定固有属性」。

- **r764B-1 ★准确率是 context/人群/评测法的函数，不是检验的固有常数；spectrum effect ≠ spectrum bias**：一手综述逐字「It is a common misconception that diagnostic accuracy is a fixed and inherent property of a medical test. There is empirical evidence that, in reality, diagnostic accuracy is also affected by the context in which it is deployed, the population in which it is used, and the methods by which it is evaluated」。要分两个概念：**spectrum effect**（预期变异）＝检验表现本就随疾病严重度/亚群而变，这是真实存在的异质性；**spectrum bias**（系统偏离）＝「in addition to expected variability, estimates … are distorted due to systematic deviations from their true values because of inadequate patient selection」。⇒ 验证报告固定写一行「本准确率测得的人群谱 + 预期随哪些亚群变（effect）+ 抽样是否系统性偏离真实使用场景（bias）」；把 effect 当 bias 会误判噪声为错误，把 bias 当 effect 会把抽样缺陷合理化。

- **r764B-2 ★two-gate case-control 高估，single-gate cohort 才是解**：一手综述逐字：只收「advanced disease」病人对照「healthy controls」的两门（case-control）设计「the resulting sensitivity and specificity are likely to be overestimated…does not capture the actual mix of cases across the spectrum」；正确做法是「single-gate 'cohort' approach, enrolling patients who represent the intended use population」。CFP 官方给出机制：只查最病的人、不查同样多的健康人 ⇒ 制造虚假的正向关联（1970s 二尖瓣脱垂被报与胸痛/心律失常/卒中强相关，Framingham 社区样本严格标准后这些关联全消失；肥厚型心肌病在三级转诊中心被描述为高症状高致命，社区研究显示多数相对良性）。⇒ 验收一个「检测器/验证器」时，先问它的阳性样本是不是只取了「明显的重症例」、阴性是不是只取了「明显健康例」；若是，报出的高指标不可外推到真实混合人群，须重采样 single-gate 或标注适用人群边界。

- **r764B-3 ★验证偏倚有方向，不是一律高估；且指标须预设防事后挑**：偏倚方向分型（Anesthesia Key 表 6.2 逐字）：partial verification bias（阳性更可能做金标准）→ sensitivity 假高、specificity 假低；differential verification bias（阳性做侵入金标准、阴性靠随访）→ 对可自愈病 sensitivity/specificity 双高、对只在随访期可检出的病双低；incorporation bias（index test 参与构成金标准）→ 两者双高；exclusion of ambiguous tests（剔除模棱两可结果）→ 双高；imperfect gold standard → 依误差是否相关方向不定。AJR 官方 PIOPED II 实例：低概率且 V/Q 阴性者未做侵入性肺动脉造影，因其随访极少发病可按阴性分析。另外「a study should focus on a limited set of predefined accuracy outcomes to avoid post hoc selection of the measure that appears more favorable」⇒ 验证报告须（a）声明每个偏倚的存在与方向，不笼统写「可能有偏倚」；（b）在看到结果前冻结用哪个指标，禁止事后挑最有利的那个报。

**来源（r764B 独立实拉 2026-11-18，≥2 独立域一手交叉）**：
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC13665641/`（PMC13665641《Diagnostic Accuracy Studies: Sensitivity, Specificity, and Beyond》WebFetch 200 全文逐字）— 准确率非固有属性原句、Table 4 六类偏倚定义、two-gate vs single-gate、spectrum effect/bias 区分、预设指标避免事后挑选、Geersing 假阴性率<2.0% 样本量例。**第一独立域·一手综述**。
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC4644738/table/d35e1910/`（PMC4644738《Sources of Bias and Variations in Studies Evaluating Diagnostic Test Accuracy》WebFetch 逐字）— 四类偏倚 taxonomic（population-related / reference-standard-related / interpretation-related / analysis-related）：spectrum effect、sample selection、inappropriate reference、differential/partial verification、disease progression、diagnostic/test/clinical review、incorporation、indeterminate results、arbitrary threshold。**第二独立域·一手分类表**。
- 交叉快照（不冒充一手全文）：`https://www.ajronline.org/doi/full/10.2214/AJR.11.7249`（AJR 官方 critically appraised topic，PIOPED II 验证偏倚实例、Bosniak 囊肿谱例、narrow spectrum 高估）· `https://aneskey.com/understanding-bias-in-diagnostic-research`（Anesthesia Key 表 6.2 各偏倚对 sensitivity/specificity 的方向）· `https://www.cfp.ca/.../62/9/708.atoms`（Canadian Family Physician 谱偏倚官方，二尖瓣脱垂/肥厚型心肌病社区对照、work-up bias 用 Bayes 或回归校正）。
- **判非 / 去重**：`谱偏倚` / `spectrum bias` / `verification bias` / `work-up bias` / `two-gate` / `single-gate` / `incorporation bias` / `诊断准确性` 全库 SKILL.md **0 命中**；`sensitivity`/`specificity` 命中在 §8/§12 的 AUC-PR/自一致性语境（异命题）。与 PDI r734A/r737C 的 conformal 覆盖率保证分工：那两章管「区间覆盖率这个数保证不了什么」，本章管「准确率这个数依赖什么人群与抽样」，不并存。与 r763/r762/r761 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：STARD 报告清单逐条、Fagan nomogram 计算、似然比与预测值公式、Bayes 校正 work-up bias 的具体回归法（属诊断学建模细节，留给后续）。


## 十四、似然比：把「检验有多强」与「这个人验前多可能」拆开，验后才能 portable（r768B 独立实拉 2026-11-19，≥2 独立域一手交叉，3 独点）

> §13 管「准确率这个数依赖什么人群与抽样」，本章管一个互补的操作问题：**当被验证对象的验前概率与你手里的研究人群不一样时，阳性/阴性预测值不能照搬，得用似然比把它迁移过来**。这正是 §13 末尾「未采纳 Fagan/似然比」预留的位置。核心洞察：sensitivity/specificity 描述「有病的人会不会被检出」（post hoc，相对穩），预测值描述「这个结果有多可信」（随患病率变）；似然比是二者的桥。

- **r768B-1 ★LR 是「给定结果时，有病与无病者的似然之比」，与患病率无关故可 portable 到个体**：定义逐字（BMJ EBM 两步 Fagan）「The LR represents the direction and the strength of evidence provided by a test result. It is calculated by dividing the likelihood of the test result among patients with the condition by the likelihood of this same test result among patients without the condition」；二值检验两个 LR 可从 sensitivity(Se)/specificity(Sp) 直接算：**LR+ = Se/(1−Sp)**，**LR− = (1−Se)/Sp**。LR 取值 0→∞，**LR=1 无诊断价值**，离 1 越远证据越强；LR+>1 支持有病、LR−<1 支持无病。关键性质（Grimes PDF 逐字）：预测值「driven by the prevalence … even excellent tests have a poor positive predictive value when the disease is rare」，而 LR「portable … useful across an array of disease frequencies … can be applied to a specific patient」；LR 含 2×2 表全部四格且不限于二值（连续/有序结果可分层各算一个 LR，不必 dichotomise 丢信息）。⇒ 验证结论迁移到新场景时，报 Se/Sp + LR，不直接报研究人群的 PPV/NPV；PPV 只在「验前概率与研究人群相同」时成立（§13 的谱偏倚正是破坏这一前提）。

- **r768B-2 ★验前 odds × LR = 验后 odds，再换回概率；Fagan 列线图是免换算的图形版**：贝叶斯更新在 odds 空间是乘法（先验 × 似然 = 后验）：`验前 odds = p/(1−p)` → `验后 odds = 验前 odds × LR` → `验后概率 = odds/(1+odds)`（Wikipedia pre/post-test 逐字）。验后概率还能作为下一个检验的验前概率串联（Grimes：「the post-test odds of the first test becomes the pretest odds for the second」）。Fagan 列线图三轴（左=验前概率、中=LR、右=验后概率）画一条直线即得，刻度按 log-odds 等距（De Gruyter 逐字：「a Fagan plot works on the log scale … the tick marks are spaced at the log odds scale」）。一手数值例（PMC5707117）：Se=90%/Sp=80% ⇒ LR+=4.5、LR−=0.125；验前 2% ⇒ odds=0.0205，阳性验后 odds=0.092 → 约 8.4%；验前 25% 者阴性验后约 3%。⇒ 验证器给「结果 + 置信度」时，置信度若要随场景迁移，必须走 odds×LR 而非照搬百分比；序列验证把前一步验后当后一步验前。

- **r768B-3 ★LR+≥3 才常用于确认、诊断 odds ratio 合并两个 LR；自然频率是给非专业者的无错沟通法**：一手阈值（PMC5707117）「Commonly, only tests with a LR(+) of 3 or more are considered for a positive diagnosis」，ROC 曲线上某点的斜率正是该点的 LR+（「the coordinates of the points are equal to the LR(+) of the quantity value and correspond to the slope of the ROC curve」）——把 LR 与 ROC 接起来。诊断 odds ratio = LR+/LR−（一个阳性把 odds 放大 10×、阴性缩到 0.1× ⇒ DOR=100，PMC12427917 逐字）。沟通层面（De Gruyter）：概率式「患病率 43%、Se 44%、Sp 74%」人易算错，改说**自然频率**「1000 人中 434 人患病、其中 190 人验阳；566 人健康、其中 148 人假阳」再算 PPV=190/338≈57%，误差显著下降（Hoffrage & Gigerenzer）。⇒ 验证报告三件套：报 LR+ / LR−  quantifying 证据方向与强度；DOR 给单一区分度总结（但掩盖两 LR 各自的非对称）；对人沟通验后概率用自然频率而非条件概率句式。

**来源（r768B 独立实拉 2026-11-19，≥2 独立域一手交叉）**：
- `https://ebm.bmj.com/content/18/4/125.full.pdf+html`（BMJ Evidence-Based Medicine《The two-step Fagan's nomogram》全文 PDF WebFetch 逐字）— LR 方向/强度定义、LR 取值 0→∞ 与 LR=1 无价值、LR+=DSe/(1−DSp)、LR−=(1−DSe)/DSp、二值/有序/连续均可算、Fagan 三轴用法、乳腺癌 MRI Se75%/Sp96% 验前 2% → 验后 28%/0.6% 例。**第一独立域·期刊一手**。
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC5707117`（PMC5707117《Bayes' theorem, the ROC diagram and reference values》WebSearch 一手全文逐字）— LR+/LR− 定义与 Se/Sp 关系、LR+≥3 阈值、odds 乘法公式、Se90%/Sp80% 数值例、ROC 斜率=LR+。**第二独立域·论文一手**。
- 交叉快照（不冒充一手全文）：`https://www.mwc.com.br/files/L-Epid02-03-Grimes[A784]%20-%20Likelihood%20ratios.pdf`（Grimes《Refining clinical diagnosis with likelihood ratios》逐字：LR portable、predictive value 随 prevalence、序列检验验后串验前、2/3 已发表产科检验高估价值）· `http://en.wikipedia.com/wiki/Pre-test`（验前/验后 odds 公式与 Fagan nomogram、PPV/NPV 与验后概率数值等价的条件与局限逐字）· `https://www.degruyter.com/.../cclm-2022-0225`（De Gruyter 诊断统计 Fagan plot log 刻度、natural frequencies 43% 改 1000 人例逐字）· `https://pmc.ncbi.nlm.nih.gov/articles/PMC12427917/pdf/diagnostics-15-02148.pdf`（DOR=LR+/LR−、10×/0.1×→100 逐字）· `https://www.sciencedirect.com/science/article/pii/S0093-691X(10)00023-3`（LR+=Se/(1−Sp)=16.4、验前37.4%→验后91% ELISA 孕检例逐字）。
- **判非 / 去重**：`似然比` / `likelihood ratio` / `Fagan` / `验后 odds` 在本技能正文仅 §13「未采纳」一句预留，本章正式展开、不覆盖 §13 谱偏倚结论；`LR+/LR−` 与 §8 AUC-PR、§12 SelfCheckGPT 一致性、§13 spectrum bias 逐条分工——§8/§12 管分数怎么算、§13 管分数依赖什么人群，本章管「验前不同时怎么把结论迁过去」。与 PDI conformal 覆盖率、DI r764C 前景理论（参照点）、TI 贝叶斯更新异命题，不并存。与 r767/r766/r765 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：有序/连续检验的分层 LR 具体计算、似然比置信区间公式、work-up bias 的 Bayes 回归校正、Fagan nomogram 绘图实现（诊断学建模细节，留给后续）。

## 十五、Conformal prediction：不信模型概率、只信校准集，给预测集合一个有限样本覆盖保证（r772B 独立实拉 2026-11-19，≥2 独立域一手交叉，3 独点）
> §13 管「换个评测人群准确率就变」、§14 管「验前不同怎么迁移结论」，本章管一件更基础的事：**当模型的概率输出根本不可信时，还能不能给出一个"错率有证明"的验证结论**。Conformal prediction 的答案是——把点预测换成集合预测，用一块模型没见过的校准集，换一个可写进 SLA 的硬承诺 `P(Y∈C(x))≥1−α`。它验的不是"模型准不准"，而是"这个集合的覆盖是不是真的达到了你说的比例"。
- **r772B-1 ★覆盖保证是 marginal、finite-sample、distribution-free，唯一前提是 exchangeability，不要求模型概率正确**：一手逐字（Cognis Digital）「a finite-sample, distribution-free guarantee that holds no matter how badly the underlying model is specified… P(Y∈C(x))≥1−α」，且「It does not ask you to believe the model's internal probabilities. It only asks that your future data look, statistically, like your calibration data — the assumption of exchangeability」。这和 calibrated softmax 是**两类契约**：后者把含义押在"模型是个好的概率拟合"上，前者只要求校准集与测试集可交换（比 IID 弱）。保证是 marginal（对所有测试点的随机性平均成立），不保证每个子群、每个个体都达到 1−α——「a method can hit ninety percent overall while under-covering a minority segment and over-covering the majority」。⇒ 验证报告引用 conformal 覆盖数时必须连三件事一起报：α、是否 marginal、exchangeability 假设是否成立；把 marginal 覆盖当成"每个子群都达标"是误用。
- **r772B-2 ★split conformal 四步只加一次分位数计算，覆盖对分数选择不敏感但"集合有没有用"完全取决于分数**：四步逐字（Cognis/Inferensys 一致）：①留出模型从未训练的干净校准集；②定义 nonconformity score `s(x,y)`（分类常用 `1−softmax(真类概率)`，回归常用绝对残差 `|y−ŷ|`），分数越大表示输入与标签越不一致；③在校准分数上取 adjusted 经验分位数 `q̂ = Quantile(s₁..sₙ; ⌈(n+1)(1−α)⌉/n)`（n+1 与向上取整是有限样本有效性的关键修正）；④对新输入输出 `C(x)={y:s(x,y)≤q̂}`。关键分野：「The coverage guarantee is indifferent to the choice of nonconformity score, but the usefulness of the sets is not」——naive 分数能平均正确却在难例上给出无用集合；分类用 APS（按 softmax 降序累积直到真类入集）在模型真不确定处放大集合、RAPS 加正则抑制长尾标签空间集合爆炸；回归用 CQR（conformalized quantile regression，先训上下条件分位再对残差做 conformal 校准）得"可预测处窄、噪声大处宽"的自适应区间。⇒ 验收把两件事分开：**有效性**（覆盖）由 exchangeability + 分位数公式保证，换分数不动它；**效率**（平均集合大小）靠分数设计，这才是工程优化对象。
- **r772B-3 ★这是一个可版本化、可审计的"操作契约"，但条款要读：子群欠覆盖、漂移失效、校准集必须自己持有**：Cognis 把 conformal 的本质定义为组织层面的收益——「converts uncertainty from a soft signal into a term you can put in writing… set α to your risk budget and the machinery honors it」，下游可据集合形态自动行动（单点→自动执行、集合大→升级人工、空集→拒绝），且集合大小可作 drift 监控信号。但同一篇明确列出条款：① marginal 覆盖在子群风险不等时是 liability，缓解要 group-balanced / class-conditional 分段算分位（代价是每段要有足够校准数据）；② distribution shift / temporal drift 下保证弱化，另有 weighted conformal / adaptive conformal inference / time-series 变体；③「you cannot conformalize what you cannot hold out, you cannot recalibrate on your distribution, and you cannot audit the quantile」——校准集必须留在自己的治理流水线内。⇒ VI 落地判据：优先本地校准而非消费远端不确定性服务；把"覆盖达标"写成带 α、带分段检查、带 drift 监控的可复算契约，而不是一个一次性的验证分数；子群有不同代价时主动分段报覆盖，不让 marginal 数字掩盖欠覆盖群。

**来源（r772B 独立实拉 2026-11-19，≥2 独立域一手交叉）**：
- `https://cognis.digital/research/library/distribution-free-coverage-with-conformal-prediction`（Cognis Research《Coverage You Can Prove》WebFetch 200 全文逐字）— finite-sample distribution-free guarantee 公式、exchangeability 契约、split conformal 四步与 ⌈(n+1)(1−α)⌉/n 分位、coverage indifferent to score but usefulness is not、APS/RAPS/CQR、marginal vs conditional 与 group-balanced 缓解、本地校准可审计论证。**第一独立域·一手工程文章**。
- `https://inferensys.com/glossary/algorithmic-explainability-and-interpretability/conformal-prediction/split-conformal-prediction`（Inferensys split conformal 术语页 WebSearch 一手逐字）— nonconformity measure / calibration set / marginal coverage guarantee / inductive vs transductive 成本 / exchangeability 失效场景 / Mondrian / CQR / weighted conformal 分类体系。**第二独立域·一手术语库**。
- 交叉快照（不冒充一手全文）：`https://inferensys.com/glossary/generative-engine-optimization/factual-grounding-techniques/conformal-prediction`（Conformal vs Bayesian/MC-Dropout/Ensemble 对比表、Conditional Coverage Extensions）· `https://www.sciencedirect.com/science/article/pii/S2590037425000536`（多尺度 conformal：按尺度分 α 仍保 marginal coverage、尺度依赖可致保守覆盖，ScienceDirect 摘要）· `https://vispikarkaria.github.io/Deep-UQ/methods/conformal`（Deep-UQ 文档：split/CQR/APS/RAPS 实现与公式）。
- **判非 / 去重**：`conformal` / `保序预测` / `覆盖保证` / `nonconformity` / `CQR` 全库 SKILL.md **本体 0 命中**（唯一命中是本技能 §14 r768B 判非句里「与 PDI conformal 覆盖率…异命题」的一次"别处概念"提及，PDI 技能本体并未落地 conformal，本次为首次本体落地）。与 §13 spectrum bias（人群改变使准确率变）、§14 似然比（验前迁移）逐条分工——§13 管"分数依赖什么人群"、§14 管"验前不同怎么迁"，本章管"模型概率不可信时如何仍给出错率有证明的集合"；与 PDI 分位数预测是"给区间"vs"给有覆盖证明的区间"两件事，不并存。与 r771/r770/r769 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：full conformal（对每个测试点重训）的实现与计算成本、Mondrian conformal 的分组细节、weighted/adaptive conformal 的数学、多尺度 conformal 的 α 分配优化（多为异命题与建模细节，留给后续）。

## 十六、覆盖率引导模糊测试：验证「没想到的输入」时，把覆盖率当反馈而不是当结论（r776B 独立实拉 2026-11-19，≥2 独立域一手交叉，3 独点）
> §8 蜕变/属性测试管「无 oracle 时怎么把关系写成断言」、§9 变异测试管「测试套件能不能抓错」，本章管一件更靠前的事：**当输入空间大到枚举不完、你根本不知道该测哪些输入时，怎么系统性地找到那些让系统出错的输入**。答案是让覆盖反馈驱动输入变异，而不是把覆盖率数字当验证通过的证据。
- **r776B-1 ★fuzzing 是自动喂畸形/半畸形输入找 bug，测试设计「free of preconceptions about system behavior」，但只找简单 bug、是补充不是替代**：OWASP 官方逐字「Fuzz testing ... by automatically providing a program with unexpected, malformed, or semi-malformed inputs」「The great advantage of fuzz testing is that the test design is extremely simple, and free of preconceptions about system behavior」「Fuzzers usually tend to find simple bugs」「It doesn't replace them, but is a reasonable complement」。⇒ VI 落地：fuzzing 的定位是「找实现层缺陷（崩溃/越界/DoS/解析漏洞）」，不是「证明功能正确」；「MS04-028  JPEG GDI+ 零长 comment 字段」说明一个字段级畸形就能出漏洞。验收写清 fuzz 覆盖了哪类输入（数字/字符/元数据/二进制）与协议/格式约束，不写「fuzz 过了所以正确」。
- **r776B-2 ★覆盖率引导 vs 盲 fuzz 的分野：只有「触发未覆盖路径的变异」才存入 corpus，覆盖率是搜索反馈信号不是通过判据**：LLVM libFuzzer 官方逐字「in-process, coverage-guided, evolutionary fuzzing engine」「tracks which areas of the code are reached, and generates mutations on the corpus of input data in order to maximize the code coverage」「If a mutation triggers execution of a previously-uncovered path ... then that mutation is saved to the corpus for future variations」。盲 fuzz 靠已知危险值向量（0/负数/极大整数、转义字符、SQL 引号、随机二进制，OWASP Fuzz Vectors），不知道自己走到哪；覆盖引导靠 SanitizerCoverage 插桩给的方向。⇒ 验收把「cov/ft（覆盖块/边数、特征数）」当进度指标、「corp 语料条目数」当覆盖存档，但明确 cov 上升≠缺陷清零；结构化输入（PNG/JPG/GIF）要给有效+无效 seed 语料，否则「libFuzzer will work without any initial seeds, but will be less efficient if the library under test accepts complex, structured inputs」。
- **r776B-3 ★崩溃/超时/OOM 按 sha1 落盘、corpus 可最小化，复现性是交付契约**：libFuzzer 官方逐字「Any crashes or sanitizer failures will be reported ... the particular input that triggered the bug will be written to disk (typically as `crash-<sha1>`, `leak-<sha1>`, or `timeout-<sha1>`)」「if a mutation triggers ... previously-uncovered path ... saved to the corpus」「`-merge=1` ... minimize it while still preserving the full coverage」「`-minimize_crash` minimizes the provided crash input」，超时（-timeout 秒）与 RSS 超限（-rss_limit_mb）都被当失败案例。⇒ VI 落地：一次 fuzz 的可交付物固定四件套=①触发输入文件（带 sha1）②输入到崩溃的最小化链（-minimize_crash）③最小化后仍保全程覆盖的 corpus（-merge=1）④失败类别（crash/leak/timeout/OOM）。「跑了很多轮没崩」不构成通过——它是「在本语料/本时段/本插桩下未发现」，报告写清三限定。
**来源（r776B 独立实拉 2026-11-19，≥2 独立域一手交叉）**：
- `https://llvm.org/docs/LibFuzzer.html`（LLVM 官方文档 WebFetch 200 全文逐字）— in-process coverage-guided evolutionary 定义、corpus 与 previously-uncovered path 存语料、NEW/REDUCE 事件、crash/leak/timeout-<sha1> 落盘、-merge=1 最小化、-minimize_crash、结构化输入需 seed。**第一独立域·官方一手**。
- `https://owasp.org/www-community/Fuzzing`（OWASP Fuzzing 社区页 WebFetch 200 全文逐字）— fuzzing 定义、1989 Wisconsin-Madison 起源、fuzz vectors、协议/文件格式依赖、conformance-testing-oriented fuzzing、 advantages/limitations「free of preconceptions」「usually find simple bugs」「reasonable complement」、MS04-028 JPEG 实例。**第二独立域·权威安全机构一手**。
- 交叉与降级登记：AFL++ `https://aflplus.plus/docs/fuzzing_in_depth.md` 与 OSS-Fuzz `https://google.github.io/oss-fuzz/getting-started/continuous-fuzzing/` 两个候选页本次均返回 404，未取到正文，**不冒充一手、不作为证据来源**，如实登记。
- **判非 / 去重**：`覆盖率引导模糊测试` / `coverage-guided fuzzing` / `SanitizerCoverage` / `corpus 最小化` 全库 SKILL.md 本体 0 命中（§6.5「对抗/红队测试」是异命题，管人为构造对抗样例；§8.3 shrinking 是属性测试反例简化，不依赖覆盖反馈，分工不并存）。与 §8 蜕变/属性、§9 变异逐条分工：§8 管「oracle 缺口怎么写断言」、§9 管「测试套件能不能抓错」，本章管「输入空间枚举不完时怎么系统性找触发输入」。与 r772B conformal（集合覆盖保证）是「概率覆盖承诺」vs「代码覆盖反馈」两件事，不并存。与 r771/r770/r769 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：AFL++ 的 edge coverage 位图与确定性/随机变异阶段细节、libFuzzer 的 entropic power schedule 数学、Fuzz Vector 完整清单（页 404 或建模细节，留给后续）。

## 十七、基准污染验证：分数虚高的第一嫌疑也可能是「题目在训练数据里」（r780B 独立实拉 2026-11-20，≥2 独立域一手交叉，3 独点）
> §10 管「建模时用了预测时拿不到的信息」的管线泄漏，本章管一个更靠前、更隐蔽的泄漏：**测试题或其近重复进入训练语料，模型靠记忆而非泛化拿到高分**。「测出来准确率高」在第一嫌疑上不再是「模型好」，而是「评测集脏没脏」。
- **r780B-1 ★去污阈值是各家自定的经验值，且 exact n-gram 去重挡不住模糊重复**：一手逐字（arXiv 2405.15523 Mosaic Memory）：GPT-3 用「equivalent of n=25 tokens」重叠检测，比训练预处理常用的 n=50「notably more aggressive」；PaLM「removes samples with at least 70% overlap in 8-grams」，GPT-4「excludes those for which any of 3 random sequences of 50 characters overlap」，Llama-2「filters samples where over 20% of the tokens appear in 10-grams ... allowing a 'skipgram budget' of 4 tokens」，Llama-3 用「the decontamination threshold for which model performance diverges the most」。但「exact n-gram deduplication alone fails to eliminate all fuzzy duplicates」——n=25 下仍残留 Levenshtein 距离 20–50 的模糊重复（「at a Levenshtein distance of 20 an average of 2,500 fuzzy duplicates per sequence persist」，30 时 6,000），且这些重复「still contribute substantially to memorization」。⇒ 验收一份评测报告，先看它写没写去污阈值与 n 的口径；「已做去重」不等于「评测集干净」，尤其对推理题。
- **r780B-2 ★canary/GUID 是事后验证手段，但会被精确去重自己抹掉**：逐字：canary 记忆「has been used as a tool to infer whether certain content was used to train an LLM」，做法是「include exact repetitions of unique sequences — either random token sequences or synthetically generated copyright traps」，BIG-bench 加了「a unique GUID string ... both to facilitate model developers to filter out benchmark files ... and to enable post-hoc verification」。矛盾在于「exact deduplication would likely remove such canaries」——copyright traps「only yield meaningful memorization for 100-token sequences repeated 1,000 times，which would be trivially removed by commonly deployed deduplication techniques」。⇒ 报告「用 canary 验过没污染」必须说明 canary 的序列长度/重复次数与去污是否把它删了；否则 canary 阴性是默认态不是安全证据（同 §11 阴性证据不可反推）。
- **r780B-3 ★黑盒只能做输出侧纠正，白盒修补会在干净题上掉分，detect-then-filter 会改变被测分布**：污染三级（arXiv 2601.19334）逐字：Exact（训练含测试原题）/ Semantic-level（释义或语义等价改写）/ Domain-level（同分布另一次切分）；「Data contamination ... can inflate reported performance by inducing memorization rather than genuine generalization」。黑盒修复：TED「frames decontamination as distribution calibration ... approximates a 'clean' output distribution via repeated stochastic decoding」，ITD「rewrites potentially contaminated prompts using an auxiliary model」——但「prompt rewriting may alter semantics or task difficulty」。白盒修复：neuron/activation patching、attention short-circuiting、ECO prompts，共同问题是「interventions strong enough to reduce contamination often alter model behavior on uncontaminated inputs, leading to non-trivial drops in clean accuracy」。detect-then-filter 用 MIA 剔除疑似泄漏题，但「any non-zero false-negative rate leaves residual leaked items unfiltered」且「filtering contaminated samples fundamentally alters the benchmark, making the resulting evaluation set no longer directly comparable」。⇒ VI 落地：去污方案报三件事——在哪一层（exact/semantic/domain）、是否改了题（改写/剔除）及因此与原始 benchmark 不可比、干净题上的掉分幅度；三者缺一的「去污后分数」不可直接和公开榜单对比。
**来源（B 独立实拉 2026-11-20，≥2 独立域一手交叉）**：
- `https://arxiv.org/html/2405.15523v2`（《The Mosaic Memory of Large Language Models》WebFetch 200 全文逐字）— 各模型去污阈值口径表、n=25 vs n=50、Levenshtein 20–50 残留 2,500/6,000、canary/GUID 双重用途、100-token×1000 次重复。**第一独立域·一手论文全文**。
- `https://arxiv.org/html/2601.19334v1`（《When Benchmarks Leak: Inference-Time Decontamination for LLMs》WebFetch 200 全文逐字）— 污染三级定义、Inflation 公式、TED/ITD 黑盒与局限、neuron patching/attention short-circuiting/ECO 白盒与 clean-evaluation drop、MIA detect-then-filter 的 FNR 与分布改变。**第二独立域·一手论文全文**。
- 交叉快照（不冒充一手全文）：`https://arxiv.org/pdf/2405.05455`（APR benchmark 去污综述：GPT-3 n-gram vs GPT-4 multi-sample substring、「standard decontamination method has not yet emerged」、near-duplicate 可使指标虚高至 100%）· `https://arxiv.org/html/2605.19999v1`（污染抵抗型 benchmark：n-gram/hash/精确串/embedding 相似四法与 recall-precision 权衡、去污管线 fixed point 不覆盖持续预训练间接泄漏）。
- **判非 / 去重**：`benchmark contamination` / `decontamination` / `n-gram overlap` / `canary string` / `成员推断MIA` 在本技能正文 0 命中；全库命中在豆包自留地 `wb-execute-discipline` §评测数据完整性（GPT-4 污染率 1-25%、continuation testing、log-prob、golden dataset 版本化，WB 0 落地）与 `multimodal-intelligence` 的 SPICE n-gram 指标评价（异命题：图像描述自动指标不是训练语料泄漏）。本章取「去污阈值口径/模糊重复残留/canary 自毁/推理时去污与检测过滤副作用」正交子面，按「优＝加厚现有」落 VI 本技能，不改豆包自留地。与 §10 fit/transform 管线泄漏、§11 阴性证据不可反推、§15 conformal 逐条分工。与 r779 三轮结论不复用。
- **未采纳**：machine unlearning 的权重级实现、MIA 统计检验的完整构造、污染抵抗型 benchmark 的 CRD 架构（异命题与建模细节，留后续）。
