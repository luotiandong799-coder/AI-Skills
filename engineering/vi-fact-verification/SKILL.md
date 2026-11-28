---
name: vi-fact-verification
description: 事实与结果验证（Verification Intelligence）。事实声称/来源引用/数据核对/改动验收/完成判定。独立性+来源分级+真/误导/夸大/缺证据/假评级。EI验执行过/VI验对不对，互补。、变异测试（mutation testing·变异算子·存活/等价变异体·耦合效应）、Youden指数J（Se+Sp−1·ROC最大垂直距离·阈值选取与患病率无关·Se/Sp联合置信域）、多重检验校正、FWER、FDR、Bonferroni、Holm、Benjamini-Hochberg、q值、family边界、假阳性膨胀、SelfCheckGPT、采样一致性幻觉检测、零资源黑盒、AUC-PR、谱偏倚、验证偏倚、预设指标、DeLong检验、相关ROC AUC比较、结构分量、协方差校正、conformal prediction、保序预测、覆盖保证、非一致分数、split conformal、CQR、marginal与conditional coverage、覆盖率引导模糊测试、SanitizerCoverage、corpus、crash最小化、基准污染、benchmark contamination、去污染、decontamination、n-gram overlap、成员推断MIA、canary string、推理时去污、模糊重复fuzzy duplicate、对抗验证、adversarial validation、数据集偏移、dataset shift、covariate shift、域分类器、ROC AUC分布相似度、特征漂移归因、对抗验证集、训练服务偏斜、核验权分离、接受权限、证据复用三同、Bland-Altman、一致性界限、limits of agreement、相关不是一致、平均差、比例偏倚、异方差、可接受差异Δ、interchangeability、评分者间信度IRR（kappa/ICC/alpha·kappa悖论·信度≠效度·须报CI）、量具GR&R/MSA（EV重复性/AV再现性·GRR=√(EV²+AV²)·%GRR两口径10/30·ndc≥5·均值极差vs ANOVA·10×3×3盲测·第一类研究）、生存分析（Kaplan-Meier乘积限·删失·log-rank·Cox比例风险·风险比HR·PH假设检验）·Brier分数（严格适当评分·Murphy分解·可靠性图·低分不等于更准）
module: VI
modules: VI,EI
version: "1.25.0"
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


## 十四、似然比（r768B · 全文下沉 references/r768B_似然比.md）

> 本节三独点（LR 定义与 portable 性 / 验前 odds×LR=验后 odds 与 Fagan / LR+≥3 与 DOR 与自然频率沟通）与四域一手来源逐字全文已下沉 `references/r768B_似然比.md`，结论仍有效：验前概率不同时预测值不能照搬，用 LR 迁移；与 §13 谱偏倚、§26 生存分析分工不复用。


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

## 十八、对抗验证：先验「测试集到底是不是同一分布」，再谈交叉验证分数（r784B 独立实拉 2026-11-20，≥2 独立域一手交叉，3 独点）
> §10 管建模时用了预测时拿不到的信息的管线泄漏、§17 管题目进训练语料的基准污染；本章管一个更早的问题：**训练集与测试集/生产集本身是否可比**。CV 分数再高，若测试分布已偏移，生产仍会静默崩。
- **r784B-1 ★合并打标训二分类器，AUC 是分布相似度不是模型成绩**：三步逐字（33rdsquare/inferensys）：合并 train 与 test，train 标 0、test 标 1，训二分类器（LightGBM/RF/逻辑回归），看 ROC AUC——**≈0.5 分不出=无显著偏移、0.5–0.7 轻微、>0.7 显著 covariate shift、>0.9 疑似时间/目标泄漏**（inferensys 阈值表）。与标准 CV 是两问："Standard k-fold cross-validation assumes that all folds are drawn from the same underlying distribution. Adversarial validation explicitly tests this assumption."；"Cross-validation measures how well a model generalizes within the training distribution. Adversarial validation measures whether the test set is even from the same distribution to begin with."（inferensys 逐字）⇒ 验证报告在 CV 分数前先给对抗验证 AUC，高分 CV 不得直接写成「已验证可上线」。
- **r784B-2 ★特征重要性是诊断主体，且能抓单变量检验看不见的多变量联合漂移**：分类器给出"a ranked list of features most responsible for distinguishing training from test data"，SHAP/Gini 高的就是漂移载体（inferensys 逐字）；"Unlike statistical tests such as the Kolmogorov-Smirnov test or Population Stability Index (PSI), which evaluate each feature independently, adversarial validation captures multivariate interactions. The classifier can detect shifts that are invisible to univariate methods because it learns the joint distribution. A high AUC confirms that P_train(X) ≠ P_test(X), even if individual feature distributions appear stable."（inferensys 逐字）。处置=迭代删/变换高漂特征后重跑到 AUC→0.5、重要性加权、或构造"最像 test 的 train 样本当验证折"（33rdsquare Step5 逐字）；但 >0.9 常是 data leakage 而非真漂移——"A feature with near-perfect importance often indicates a temporal or target leakage"，删前先判泄漏还是漂移（inferensys 逐字）。
- **r784B-3 ★只测 P(X) 不测 P(Y|X)，且大样本/漏放大是三个易错边界**："Does not detect concept drift: It only identifies shifts in P(X), not changes in the conditional relationship P(Y|X). A model can pass adversarial validation (AUC ≈ 0.5) yet still fail due to a changed decision boundary."（inferensys 逐字）⇒ 须配性能监控做两段诊断（纠了 covariate shift 后仍掉分→判 real concept drift）。另两条："A moderately elevated AUC (e.g., 0.55-0.60) on very large datasets may be statistically significant but practically negligible. Always pair AUC with sample size context."；"If the original data pipeline contains a subtle target leak, adversarial validation will amplify its signal, potentially leading to the removal of genuinely predictive features."（inferensys 逐字）；33rdsquare 补"can tell you that there is dataset shift, but not necessarily why"与"if the test data contains wholly new categories or concepts not seen in training, adversarial validation may not be as effective"。⇒ 报告固定四栏：AUC/样本量/高重要特征是漂移还是泄漏/是否配了生产性能监控。
**来源（r784B 独立实拉 2026-11-20，≥2 独立域一手交叉）**：
- `https://inferensys.com/glossary/quantitative-finance-and-algorithmic-trading/high-frequency-time-series-forecasting/adversarial-validation`（WebFetch 200 全文逐字）— CV 假设 vs 对抗验证明确对比、AUC 阈值表、SHAP 漂移归因、迭代收敛到 0.5、covariate/concept shift 两段诊断、walk-forward 配对。**第一独立域·一手术语页**。
- `https://inferensys.com/glossary/financial-fraud-anomaly-detection/model-drift-and-continuous-evaluation/adversarial-validation`（WebFetch 200 全文逐字）— P(X) vs KS/PSI 独立特征、多变量交互、验证集构造、三点 limitations（不测 P(Y|X)/大样本 AUC 夸大/泄漏放大）、MMD/KL/PSI/OOD 对照。**同域第二页·一手（如实登记同域）**。
- `https://33rdsquare.com/adversarial-validation-improving-ranking-in-hackathon/`（WebFetch 200 全文逐字）— 三步流程、dataset shift 三型（covariate/prior/concept）数学定义、AUC 0.926 实例、adversarial validation set 构造代码、四条 caveats。**第二独立域·一手教程**。
- 交叉快照（不冒充一手全文）：`https://github.com/wenmin-wu/ds-skills/.../adversarial-validation/SKILL.md`（LightGBM 5-fold 代码与 AUC>0.7 阈值）· `https://www.skillsdirectory.com/skills/wenmin-wu-adversarial-validation`（同技能镜像）。
- **判非/去重**：`adversarial validation`/`对抗验证`/`domain classifier`/`covariate shift detection` 全库 SKILL.md 本体 0（agent-evolution 命中是 CUPED 判非句里 covariate shift 一词、pdi-forecasting 命中是 conformal coverage shift，均异命题）。与 §10 管线泄漏、§15 conformal、§17 基准污染逐条分工。豆包自留地 WB 0 落地。
- **未采纳**：MMD/KL 的数学检验构造、domain adaptation 的梯度反转层实现、walk-forward 完整框架（异命题与建模细节，留后续）。
## 十九、Bland–Altman 一致性：相关不是一致，差值的均值与离散才是答案（r788B 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）
> §十三管「换人群/换评测准确率就变」、§十四似然比管「检验强度与验前拆开」、§十八对抗验证管「测试集是否同分布」；本章管一个更基础的问题：**两把尺子（两种测量方法/两个评审/旧版与新版）对同一对象读数是否可互换**。相关系数高不等于一致——这是方法比较里最普遍的误判。
- **r788B-1 ★相关高≠一致：Y=X 与 Y=2X 的 r 完全相同**：系统综述（PMC3360667）逐字："it is possible to have perfect correlation (r = 1) for both situations of Y = X or Y = 2X. However in terms of agreement, we can say that there is an agreement in the first case of Y = X, but not for Y = 2X."表 4 实证："The correlation coefficient r for the relationship between variables A and B is 0.9798. Although the variable C is twice the value of B, the correlation coefficient of A and C is exactly the same (r = 0.9798). It is obvious that there is no agreement between A and C" ⇒ 结论逐字："it is clear that the correlation coefficient does not represent agreement."；r² 同理不合适（"being related to the correlation coefficient relies on a similar concept and is thus not suitable"）。MedCalc 逐字："Two methods that are perfectly correlated but where one consistently reads twice as high as the other will produce r=1.0 while disagreeing at every single observation. Correlation answers the wrong question." ⇒ 验收"两方法是否一致"禁只报 Pearson r，须报差值分布。
- **r788B-2 ★LoA=平均差±1.96×差值的 SD，横轴用两法均值而非单一方法**：公式逐字（PMC3360667）："Limits of Agreement = mean difference ±1.96 x (standard deviation of differences)"，依赖两假设"the mean and standard deviation of the differences are constant throughout the range of measurement, and that the distribution of these differences approximately follows a normal distribution"。横轴取均值 mi=(Ai+Bi)/2 的理由（MedCalc 逐字）："it is the best available estimate of the true (unknown) value, and using either method's value alone would create an artificial correlation between the axis variable and the plotted differences."非正态时改用"2.5th and 97.5th percentiles of the observed differences"。散点图"was initially used only to check these assumptions and not for the analysis of agreement"（PMC3360667）；85% 一致性研究用此法（178/208 篇）。⇒ 报告固定三行：bias（平均差）、上下 LoA、差值是否随测量水平变化。
- **r788B-3 ★可接受界限 Δ 须事前定，判定看 95%CI 不看点估计；比例偏倚/异方差要换回归式 LoA**：MedCalc 逐字："Agreement can only be declared adequate if the limits of agreement are clinically acceptable. This requires pre-specifying a maximum allowable difference Δ ... interchangeable when both limits of agreement, including their confidence intervals, lie within [−Δ,+Δ]"。血钾例逐字："a clinically acceptable difference might be Δ=0.5 mmol/L. If the upper limit of agreement is +0.45 mmol/L with a 95% CI extending to +0.52 mmol/L, the CI exceeds Δ and agreement cannot be declared adequate — despite the point estimate being within bounds. The confidence interval, not the point estimate alone, determines the verdict."；"how small LoA should be to conclude that methods agree sufficiently is a clinical, not a statistical, decision, and it is a decision that ideally is made in advance"（AJO 逐字）。图上有斜率=比例偏倚、漏斗形=异方差违反恒定 SD 假设，此时用回归式 LoA(A)=(b0±2.46c0)+(b1±2.46c1)·A（MedCalc 逐字）；同一对象重复测量须用 Bland-Altman 重复测量扩展（Bland & Altman 2007 / Zou 2013）。另禁混淆：配对 t 检验/McNemar 不显著是"均值差小"不是"一致"（AJNR 逐字）。
**来源（r788B 独立实拉 2026-11-22，≥2 独立域一手交叉）**：
- `https://medcalc.org/en/book/bland-altman.php`（WebFetch 200 全文逐字）— 相关为何错（r=1.0 仍处处不一致）、横轴取均值理由、bias/LoA 公式与非正态百分位、Δ 与 interchangeability 的 CI 判定、血钾 Δ=0.5 例、比例偏倚/异方差/回归式 LoA、重复测量扩展。**第一独立域·一手方法页**。
- `https://pmc.ncbi.nlm.nih.gov/articles/PMC3360667/`（WebFetch 200 全文逐字）— 系统综述：Bland-Altman 占 85%（178/208）、LoA 公式与两假设、Y=X vs Y=2X 及表 4 的 r=0.9798 完全相同、散点图初仅查假设、r²/回归系数/比均值均不合适。**第二独立域·一手系统综述**。
- 交叉快照（WebSearch 逐字，WebFetch 走外部跳转未直取）：`https://www.ajnr.org/...`（AJNR 常见陷阱：相关 r=0.98 仍一致差、配对检验不显著≠一致、LoA 多窄是临床决策）· `https://www.ajo.com/article/s0002-9394(08)00773-3/abstract`（AJO：相关依测量范围、bias 与个体一致性两面、Δ 事前定）。
- **判非/去重**：`Bland-Altman`/`limits of agreement`/`一致性界限`/`一致性评价`/`相关不是一致` 全库 SKILL.md 本体 0（命中"一致性"多为 LLM-as-Judge 一致率、Cronbach、模型集成语义，异命题）。与 §十三谱依赖、§十四似然比、§十八对抗验证逐条分工。豆包自留地 WB 0 落地。
- **未采纳**：Passing–Bablok / Deming 回归椭圆与截距斜率检验细节（是 刻画系统误差的补充，不直接回答"是否在可接受界限内"，异命题）；Cohen's kappa / ICC 用于分类与评分者间信度（变量类型不同，留后续）。

## 二十、变异测试：验的是「测试套件的检错能力」，不是代码覆盖率（r792A 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）
> §r776B 覆盖率引导 fuzz 管「喂畸形输入找实现缺陷」、§十三蜕变测试管「没有 oracle 时靠派生关系判对错」；本章管另一个盲点：**覆盖率只证明代码被执行过，不证明断言在验对错**——一行 `apply_discount(100,10)` 无断言即 100% 行覆盖却零检错。变异测试故意往代码里注入小错（mutant），看测试是否失败来反测测试本身。
- **r792A-1 ★两大基础假说是 CPH + 耦合效应，决定了「只测简单变异体」为何有意义**：Mutation Testing Repository 逐字：Competent Programmer Hypothesis（DeMillo et al. 1978）"programmers … tend to develop programs close to the correct version … faults are merely a few simple faults which can be corrected by a few small syntactical changes"；Coupling Effect "Test data that distinguishes all programs differing from a correct one by only simple errors is so sensitive that it also implicitly distinguishes more complex errors"。Offutt 扩展成 Coupling Effect Hypothesis「complex faults are coupled to simple faults … a test data set that detects all simple faults … will detect a high percentage of the complex faults」⇒ 传统变异只取 simple mutants 不是偷懒，是假说支撑的抽样。mutant = 单点语法变换（算术/关系/条件算子替换、语句删除、变量替换）；killed = 至少一个测试在其上失败，survived = 全过。
- **r792A-2 ★等价变异体不可判定，MS 的分母要减等价、100% 不是可达目标**：等价 mutant「syntactically different but functionally equivalent」（如 `a+b`→`b+a`），任何测试都杀不死，仓库逐字 "Automatically detecting equivalent mutants is impossible [BuddA82, OffuttP97], because the problem would involve detecting equivalence" ⇒ 只能人工判定排除。Mutation Score = killed /（total − equivalent）；仓库把 MS→1 表述为「目标」，GitHub 实践页立刻更正「never treat 100% as an achievable target」，建基线后要求**不回退 + 新代码门槛高于遗留**才是可持续门禁。另注 human oracle problem——「checking the original program's output with each test case … oracle cost is often the most expensive part of the overall test activity」，变异让用例变多会同步抬高 oracle 成本。
- **r792A-3 ★survivor 要逐条分诊，别追分数；成本靠增量+稳定测试+排除无信号码压下来**：每个 survivor 是一个可复现缺口，GitHub 页给四分类处置——缺断言→补断言、缺边界→补边界测试、不可达/等价→标等价记理由、死代码→删；「Never chase the score. Read the mutants.」。成本侧：先要快速稳定的测试（flaky 失败会把 mutant 误判 killed 抬分）、按 diff 增量只跑改动文件、排除生成码/DTO/样板、用增量缓存与并行分片；「Applying it uniformly across a whole legacy codebase on day one」是反模式。另两条易错：timeout 未必算 killed（须确认工具分类）；它测不到缺失功能（只变异已存在的代码）。与 fuzz 分工逐字：fuzz 生成随机/畸形输入找崩溃，mutation 改代码本身验现有测试，互补不可替代。
**来源（r792A 独立实拉 2026-11-22，≥2 独立域一手交叉）**：
- `https://mutationtesting.uni.lu/theory.php`（WebFetch 200 全文逐字）— CPH、Coupling Effect、Offutt 扩展假说、mutant/operator/killed/survived/equivalent 定义、MS 公式、等价不可判定（BuddA82/OffuttP97）、high computational cost、human oracle problem。**第一独立域·一手学术库**。
- `https://github.com/gbb-acelerators/awesome-harness-primitives/blob/main/harness/claude-code/skills/mutation-testing/SKILL.md`（WebSearch 一手逐字）— 无断言的 100% 行覆盖例、MS 口径、survivor 四分类、「never treat 100% as achievable target」、非回退基线、增量/diff/并行/排除生成码、flaky 污染、timeout 分类、fuzz vs mutation 分工、输出模板与质量门。**第二独立域·一手实践规范**。
- 交叉快照（WebSearch 逐字）：`https://etheses.whiterose.ac.uk/id/eprint/36618/1/Roslan_Firhard_MinorCorrections.pdf`（White Rose 论文：RIPR 模型、killed/survived/equivalent/stubborn/trivial 四分、mutation score 定义与 CPH 起源）· `https://inferensys.com/glossary/recursive-error-correction/verification-and-validation-pipelines/mutation-testing`（算子表、mutant sampling/higher-order/weak mutation/并行四类优化、与覆盖率对照表）· `https://byteledger.vizleo.com/blog/what-is-mutation-testing-2026`（Stryker/PIT 增量变异、mutation score 50–75% 健康区间、与 fuzz/property-based 组合）。
- **判非/去重**：`变异测试`/`mutation testing`/`mutation score`/`变异体`/`等价变异体`/`胜任程序员假设`/`耦合效应`/`human oracle` 全库 SKILL.md 本体 0（§r776B fuzz 命中「变异策略」是覆盖率引导的输入变异，异命题）。与 §r776B fuzz（改输入找崩溃）、§十三蜕变测试（造 oracle）、§r784B 对抗验证（验分布）逐条分工，不并存。豆包自留地 WB 0 落地。
- **未采纳**：RIPR 模型的感染/传播形式化（属检错链路分解，不直接给测试套件验收动作）、higher-order/weak mutation 的实现细节（是降本变体，单元操作仍以 simple mutant 为主）、各语言工具的具体 CLI 配置（工程操作细节，留后续）。

## EXT-S1 · 核验结论与接受权限分记 + 证据复用边界（2026-11-22 外部共学，Solo to Team）
- **★核验≠接受**：证据支持什么就报告什么；「核验通过」本身不授予验收权。先确认当前版本核验通过，再确认接受决定或明确适用的既有授权——两项都满足才记「已验收」；仅有核验时如实记「核验通过，待有权者决定」，保留未完。核验人已有该项授权则直接沿用不重复报批；执行人自查不替代独立核验（独审=非制作的真实上下文实际打开同版成品，见过已有结论不称盲审）。
- **★有效证据=版本/范围/环境三同**：复用须写明哪一次核的哪个版本；之后有改动、出过失败或换环境（换机/换账号/换版本）的部分**只补核受影响部分**，不必整套重验，拿不准影响面就放大范围；他人报告只是线索不是证据；核旧版本或别的范围不算。只报「进行到哪」不触发重验，一旦说「这部分做完了」该部分就必须过检——换说法暗示做完与违反铁规同罪。
- **★核对本身不得变成危险动作**：核对用只读、本地可逆手段；不为「试试能不能发出去」真发一条、不为测试下单、不为核对删东西；核对须碰对方账号/会被外人看到的，先走报审；实在核不了就说核不了并标「待核实」，不硬说做完。
- **★交付三核分列**：「文件在某处」「宿主已上传附件」「用户原会话可取得」是三个独立事实，不能用路径/哈希/下载提示代替收件事实；「已交回」只是交付事实，不自动等于已验收。
- 来源：GitHub `dabingfy-dot/solo-to-team-skills`（MIT，commit fedfd4e 2026-11-17，1091 stars）`skills/dispatch-accept-verify`+`evidence-before-done`+`ops-case-notes`+`beginner-ops-writing` 正文直读 + `alexzhu0/orchivane`（MIT，commit 5265857 2026-10-28）SKILL.md 全文直读；该包自述改写自 `obra/superpowers` verification-before-completion（MIT，commit 22f0b46）。2026-11-22 外部项目共学（EXT-S1），判重=四载体全库关键词 0 命中本体，判「增」。
## 九、统计功效：没显著差异不等于没效果，事后功效不等于证据（r795D 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）

§八验「证据是否足够支持结论」，本章补一个高频误判：只报 `p` 不报效应量与区间，把样本不足造成的「没检出」写成「不存在」。

**独点1** 三元组完整性：任何验证报告须同时出现功效、效应量、置信区间并给出 α；只有 `p<0.05/0.01` 而无 CI 判不合格。Giner-Sorolla 2024 逐字：四参数 α / population effect size / sample size / power 绑在一个设计上；「Once the study is analyzed, confidence intervals replace calculated power in describing results」。

**独点2** 非显著措辞禁令：`p>α` 时正文禁止写「无效应/等效/证明无效」，只允许「未检出/证据不足」；要声称等效须给等效性界值并证明 CI 完全落在界内。Greenland 2016 逐字：除点估计恰好等于零外，「it is a mistake to conclude from P > 0.05 that a study found 'no association'」。

**独点3** 事后功效禁令：效应量来自同一样本又用于回算该样本 power → 无效证据（Giner-Sorolla：no new information is gained）。只允许先验设计功效，或输入固定/外部效应量的 sensitivity analysis，其输出是 MDE（最小可检测效应）：「inputs the desired power and likely usable sample size, returns the minimum population effect size detectable at this power」。

- **判重：`统计功效` 全库仅 agent-evolution 一句实验层交集流量不足；`power analysis` 0，本体 0 专节；与 §八 oracle/mutation、§九 Bland-Altman 分工不复用。豆包自留地 WB 0 落地。**
- **来源与诚信**：https://pmc.ncbi.nlm.nih.gov/articles/PMC11193916/?report=classic（Giner-Sorolla 等，Personality and Social Psychology Review，2024，WebFetch 200 逐字：四参数 / MDE sensitivity / 事后功效循环 / CI 替代 power）；https://pmc.ncbi.nlm.nih.gov/articles/PMC4877414/?report=classic（Greenland/Senn/Rothman 等，Eur J Epidemiol，2016-05-21，WebFetch 200 逐字：power 的 pre-study 定义 / type-II / P>0.05 误读禁令 / 必看 CI）；https://pmc.ncbi.nlm.nih.gov/articles/PMC1771282/（Br J Ophthalmol 社论，WebFetch 逐字：1−β 定义与样本量/α/MDE/方差 关系）。EBI Europe PMC fullTextXML HTTP 500；PDF 仅返回下载页；改用 ?report=classic 成功。 逐字全文与判非见 `references/r795D_统计功效.md`。
## 十、等效性检验 TOST：不显著不是等效，先定等效界才有权说「一样」（r796D 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）

§9 管「没检出不等于没有」（防误报无效应），本章补正向命题——想证明「两者确实等效」必须换一套检验，不能靠 p>α。

**独点1** 先看数据前写 Δ（±Δ 须附领域/成本-收益理由）与 α，再据 Δ 算样本量；判据——事后按结果挑 Δ、把 0 当等效界均判违规。Lakens 2017 逐字：researchers often incorrectly conclude an effect is absent based a nonsignificant result；「not possible to conclude there is no effect when p > α」。

**独点2** 做两个单侧检验 H01:Δ≤−ΔL 与 H02:Δ≥ΔU，取较大 p 与 α 比；判据——两个都显著才等效，禁止用 p>α 宣布等效，禁止对两次检验做多重比较校正（Lakens 2018 逐字：not necessary to control for multiple comparisons）。若既非显著不同也非统计等效 → 写「数据不足」，不得二选一硬判。

**独点3** 90% CI 必须完全落入 [−ΔL,+ΔU] 才写等效；判据——以「95%CI 含 0 / 不显著」替代等效结论、把等效检验与优效性 NHST 混用均判违规。界值来自 SESOI，界越窄所需样本越大（Lakens 2018 逐字）。与 §9 分工：§9 防止误报「无效应」，本条给「有界等效」的正向证据路径。

- **判重：`TOST`/`等效性检验`/`equivalence test` 全库 SKILL.md 0；与 §9 统计功效（防误判）分工不复用。豆包自留地 WB 0 落地。**
- **来源与诚信**：https://journals.sagepub.com/servlet/linkout?dbid=4&doi=10.1177%2F14761270251410355&key=10.1177%2F1948550617697177&site=sage&suffix=e_1_3_5_47_1（Lakens，SPPS 8(4)，2017，WebFetch 200 逐字：p>α 不能推出无效应/TOST 两单侧/90%CI 排除界/0 假设不可能被支持）; https://journals.sagepub.com/servlet/linkout?dbid=4&doi=10.1177%2F25152459251323480&key=10.1177%2F2515245918770963&site=sage&suffix=e_1_3_5_19_1（Lakens/Scheel/Isager，AMPPS，2018-06，WebFetch 200 逐字：取较大 p/无需多重校正/不显著=数据不足/90%CI 全落界内/SESOI 决定样本量）。FDA 生物等效性指南限定域检索无结果，未虚构 URL；Δ 预先定的「before looking at data」原句被截断，标注为谨慎外推。 逐字全文与判非见 `references/r796D_TOST等效性.md`。

## 二十一、评分者间信度（inter-rater reliability）：系数按标签形状选，kappa 低可能是流行率假象（VI · 2026-11-23 实拉，≥2 独立域一手交叉，3 独点）

§十九 Bland–Altman 管「连续测量的两人一致性」，§十九末留钩子「Cohen's kappa / ICC 用于分类与评分者间信度（变量类型不同，留后续）」——本章填该坑：多 judge 判定一致时，先按标签类型选系数，再警惕 kappa 悖论。

**独点1** 系数选择表按标签形状，不是按习惯：名义/2 人→Cohen's kappa；有序→weighted kappa（二次加权在标准条件下≈两因素 ICC）；名义/≥3 人→Fleiss' kappa；缺评/每人评不同条/名义到比率→Krippendorff's alpha；连续→ICC（须报 model/type/definition + 95%CI，共 10 种形式）；区域→Dice/IoU；时序事件→event-level F1（先定匹配规则）（Cogn-IQ 选择图 + Metrics Reloaded 表逐字）。判据——用 ICC 评类别、kappa 评连续分均判 category error；只报 percent agreement 判不合格（无机会校正）。可信度是效度的前提不是证据：两个 judge 按同一错定义也能高度一致（CASRAI 逐字）。

**独点2** kappa 悖论必须随报告拆开：95% 观察一致率在不同流行率下 kappa 可为 0.90 / 0.26 / −0.02（CASRAI 表逐字）；原因是主导类别使机会一致项 pe 变大、压掉高于机会的余量。Feinstein & Cicchetti 要求 kappa 永远配报原始一致率与边际分布，并分报 ppos/pneg；偏斜流行率下考虑 Gwet's AC1（但其机会定义有争议，须预注册、不得事后因 kappa 难看才换）（CASRAI + Cogn-IQ + PaloAltoHealthLabs 三源逐字）。判据——只报单个 kappa 不报边际判不完整。

**独点3** 阈值是约定不是推导 + 样本量按 CI 宽度反推：Landis & Koch 0.61–0.80 substantial、Krippendorff α≥0.800 都是 convention；高风险逐人决策常要求 ICC>0.90，群体研究可放宽（Koo & Li 2016）。样本量无通用下限：2 平衡类别、kappa≈0.6 要 95%CI±0.1 需约 246 观测；稀有类别需更多。Low agreement 先归因三因——定义模糊/类别重叠/训练不足，而非直接换系数（MCP Analytics + Quali-Fi 逐字）。

- **判重：`评分者间信度`/`inter-rater reliability`/`Krippendorff` 本体仅 §十九末一句留后续钩子（无专节）；`kappa`/`ICC` 命中为统计功效/Bland-Altman 语境异命题；与 §十九 Bland–Altman（连续两人）、§八 oracle/mutation 分工不复用。豆包自留地 WB 0 落地。**
- **来源与诚信**：https://cogn-iq.org/learn/theory/inter-rater-reliability/（全文逐字：加权 kappa≈ICC / Fleiss / Krippendorff / ICC 族与 Koo & Li / Landis & Koch / kappa 两悖论）；https://mcpanalytics.ai/articles/cohens-kappa-agreement-beyond-chance（全文逐字：kappa 公式与决策指南 / 95% 全负仍 82% 机会一致 / 246 观测样本量 / 负 kappa 涵义）；https://paloaltohealthlabs.com/resources/inter-rater-agreement-medical-data-labeling.html（全文逐字：按标签形状选系数表 / Dice-IoU-event-F1 / Koo & Li 10 种 ICC / ppos/pneg 修补）；https://casrai.org/guides/inter-rater-reliability-choosing-a-coefficient（全文逐字：95% 一致率对应 kappa 0.90/0.26/−0.02 / 信度≠效度 / Gwet AC1 争议 / Krippendorff α≥0.8）；https://quali-fi.com/learn/inter-rater-reliability（全文逐字：kappa 公式 / 低一致三因 / 信度工作流 pilot 10–20% 至少 30–50 例）。均 WebSearch 返回页面全文逐字，未冒充期刊原文。 逐字全文与判非见 `references/r798B_评分者间信度.md`。


## 二十二、序贯检验与 peeking：同一个检验「多看几次」就会假阳性膨胀，与多重检验正交（VI · 2026-11-23 实拉，≥2 独立域一手交叉，3 独点）

**独点1** 固定样本 p<0.05 的 5% 错误率只对「看一次」成立；随查看次数累积——1 次≈5%、5 次≈19%、10 次≈30%、20 次≈54%（gravityfield 逐字），「daily check and stop on significance」是从噪声里做决定（growthstack 逐字：30 天日查可把假阳性抬到 25%+，机制是零假设下运行 z 统计量是随机游走、看足够多次必穿越固定阈值）。医学原文给出概念式：「Testing twice with a 5% risk of error each time leads to an approximately 10% overall risk of error」（ScienceDirect/Statistics in Medicine 逐字）。判据——验证/监控流程若「每次跑完看一眼显著就收工」且无事先冻结的停止规则，判为 peeking 违规；与 §十一多重检验的分工：那是**横向**一次内 m 条结论（family），这是**纵向**同一条结论随时间反复看，两者不可互相顶替。

**独点2** 解法一是 alpha spending：把 0.05 总预算按函数分摊到各次 interim，每次用更严阈值、总支出不超 0.05（gravityfield 逐字）；两族边界方向相反——O'Brien-Fleming「reserve most of the type I error for the final analysis」、早期极严（第一次 |z|>3.438 即 p<0.0006，末次 p<0.0471 即接近名义 0.05），Pocock「split α equally among the k analyses」（两次各 p<0.015 双侧）（ScienceDirect 逐字）。Lan-DeMets 等 flexible alpha-spending 允许事先不固定查看次数、每次查看「cost」一点 α（ScienceDirect/Principles of Clinical Research 逐字）。判据——写「随时看且不调整阈值」判违规；须声明属于固定 schedule 的 group sequential（OBF/Pocock）还是 flexible spending，并给出各次阈值。

**独点3** 解法二是 e-value / always-valid inference：e_t = e_{t-1} × LR_t（逐步骤似然比相乘），e_t ≥ 1/α 即停，核心性质是「validity holds under any stopping strategy — including a discretionary one」（gravityfield 逐字）；mSPRT、confidence sequences（Howard/Ramdas）同族（growthstack 逐字）；贝叶斯事后分布理论上不受停止规则影响但操作特性仍依赖它。代价要说全：always-valid 区间比固定样本宽、无早停时达显著更慢（calibreos 逐字），且它只管统计错误、不管「novelty effect/周周期导致短期信号≠稳态」（calibreos）。判据——方案若把「随时可停」写成零成本，判不完整；须并报功效代价 + 最短运行时（至少一个完整业务周期）护栏。

**判重：`序贯`/`sequential`/`alpha spending`/`peeking`/`always-valid`/`e-value`/`O'Brien-Fleming`/`Lan-DeMets` 在 VI 技能 0 专节（description 新增词条属本轮）；§十一多重检验是横向 family 校正异命题、§八 oracle 分工不复用。全库命中在 agent-evolution §mSPRT 早停（异命题，仅对比提及）、豆包自留地、co-learn 与配置文档，WB 0 落地。**
**来源与诚信**：https://gravityfield.ai/glossary/sequential-testing（WebFetch 200 全文逐字：假阳性 1/5/10/20 次=5/19/30/54% / alpha spending / e_t=e_{t-1}×LR_t 停于 1/α / 任意停止有效 / 与贝叶斯对照）——第一独立域（工具站一手，商业立场已登记）；https://www.sciencedirect.com/topics/medicine-and-dentistry/interim-analysis（WebFetch 200 全文逐字：两次 5%≈10% / spending function / OBF 早期 3.438 p<0.0006 末次 1.985 p<0.0471 / Pocock 均分 / Lan-DeMets flexible / 伦理早停）——第二独立域（医学教材原文一手）；https://www.growthstack.dev/glossary/peeking-problem + https://www.calibreos.com/decoder/sequential-testing + https://markusloecher.github.io/pValue-Hacking-Solutions（WebSearch 全文逐字：随机游走穿越阈值 / mSPRT / confidence sequences / 功效代价 / 最短一周护栏 / 三法 recommend 顺序）——第三、四、五域交叉。数字均挂可复拉 URL；未冒充 RCT 原始论文。逐字全文与判非见 `references/r802B_序贯检验peeking.md`。


## 二十三、回归均值（regression to the mean）：极端样本「自然回落」不是干预的效果证据（VI · 2026-11-25 实拉，≥2 独立域一手）

**独点1** RTM 是抽样选择效应，不是干预效应：凡按「含随机成分的指标」挑出极端样本（最低分阅读班、最高击球率球员、SAT 表现低于预期者），再测必向均值回落。数学必然形式是标准化回归 `ZY′ = r·ZX`——只要 `|r|<1`，预测 Y 就永远比 X 更靠近 0 均值；`r=0`（纯运气）时无论 X 多极端，重测预测恒为均值（LibreTexts 抛硬币 12 次猜对 10 次者重测最佳预测仍是 6）。判据：见到「干预后极端值显著改善」先问「当初是否按该极端值选人 + 有无对照组」；无对照则回归效应与真实效应混淆——propranolol 提 SAT 研究里 25 名学生按「表现低于预期」选出，重测涨 120 分、单纯重测预期仅 38 分，官方教材明写「regression effects and propranolol effects were confounded，no firm conclusions should be drawn」。

**独点2** RTM 的成立条件比直觉宽：Britannica 逐字「**RTM does not depend on the assumption of linearity, the level of measurement of the variable (for example, the variable can be dichotomous), or measurement error. Given a less than perfect correlation between X and Y, RTM is a mathematical necessity**」——不依赖线性、变量测度水平、也不依赖测量误差；把回落一律解释成「测量误差消失」或「只在线性场合成立」是错的。相关系数越小效应越大（`r` 从 0.835 的 Math→Verbal SAT：X=1.6 SD 预测 Y=0.835×1.6=1.34 SD）。Kahneman 飞行教官「表扬后动作变差、责骂后变好」正是 RTM：极端动作含运气，运气不延续，**after the praise but not because of it**。

**独点3** 四种可机检的解混淆设计：①随机分配到对照使 RTM 对两组均等，组间差才是真效应；② placebo 组均值变化估 RTM+安慰剂，处理组变化减 placebo 组变化=调整后效应；③按多次测量均值选人而非单次；④一次测量筛选、第二次治疗前测量作基线——若 post 与首次测量的 r 等于两次前测的 r，则无期望 RTM 均值变化。数字锚：Schall & Smith 2000 选 1998 年击球率最高 10 人，1999 年 7/10 下降、平均降 33 点，但个别反升——RTM 是群体预测，不对每个个体成立（「although the predicted scores for every individual will be lower, some of the predictions will be wrong」）。

**判重**：全库 SKILL.md / module-memory 对 `回归均值` / `regression to the mean` / `向均值回归` 0 命中；辛普森悖论在 ti-critical-reasoning §13（因果识别「该条件化哪个变量」，异命题）、幸存者偏差在 wb-agent-evaluation/references（打分集选择偏差，异命题）、Goodhart 在 ti §10.3/agent-evolution §22（指标被优化腐蚀，异命题）、agent-evolution always-valid 节只把 SRM/RTM 列入前置检查未立论。豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地。

**来源与诚信**：`https://stats.libretexts.org/Courses/Luther_College/Psyc_350:_Behavioral_Statistics_(Toussaint)/10:_Regression/10.07:_Regression_Toward_the_Mean`（WebFetch 200 全文逐字：抛硬币重测=6、`ZY′=r(ZX)`、SAT 0.835×1.6=1.34、Kahneman 教官、Schall & Smith 7/10 降 33 点、propranolol 120 vs 38 与无对照结论）；`https://www.britannica.com/science/regression-to-the-mean`（WebFetch 200 全文逐字：RTM 定义、不依赖线性/测度/测量误差、Galton 930 成人子女身高、四类去混淆设计）；两域均一手全文，日期 2026-11-25 实拉。


## 二十四、Youden 指数 J：选阈值时「敏感度+特异度−1」，不是准确率也不是 AUC（VI · 2026-11-26 实拉，≥3 独立域一手）

**独点1** J 是二值诊断测试的单数性能量，与 PPV/准确率正交：定义 `J = sensitivity + specificity − 1 = TPR + TNR − 1 = TP/(TP+FN) + TN/(TN+FP) − 1`，展开后 `J = (TP·TN − FP·FN)/((TP+FN)(TN+FP))`。取值 0（对有病/无病两组给出相同阳性比例=无用）到 1（无假阳无假阴），形式上的负值只表示把正负标签接反了，纠正标签后回到 0–1。**J 对假阳与假阴等权**——原始论文明确「all tests with the same value of the index give the same proportion of total misclassified results」⇒ 若业务里漏报与误报代价不等（漏一个病的代价远高于多一次复查），J 相等的两个模型不可互换；此时须改显式代价加权阈值而不是默认 J。与 §十三谱偏倚分工：那里管「换人群准确率会变」，这里管「同一人群内选哪个阈值、按什么权重」。

**独点2** J 用于选阈值而 AUC 用于评排序，两者不互相替代：对连续输出在每个截点 c 算 `J(c)=Se(c)+Sp(c)−1`，取 `max` 得 J-point；几何上等于 ROC 曲线到对角机会线的**最大垂直距离**（ScienceDirect 逐字），而「最近左上角」是另一个准则（只在 ROC 近似凸时才大概率与 J 重合，非同一判据）。SCI 原文强调「markers with the same Youden index can have very different sensitivity and specificity at the optimal cut-off point」⇒ 报告阈值时必须同时报该点的 Se/Sp 二元组，只报 J 或只报 AUC 都丢掉决策信息。J 相對患病率不变（PMC 逐字 `independently from the outcome prevalence`），这是它相对 PPV/NPV 的优势，但「等权」这一价值前提不会因此消失。

**独点3** Se/Sp 在最优截点处相关，置信区间不能按两个独立比例各算一个：最优 c 同时由病人组与健康组数据估计，故该点的 Se 与 Sp **相关**，须报联合置信域而非两条边际区间（ScienceDirect S0167947314000450 全篇即为此）；固定预设阈值时 J 是两独立二项比例之差，可用两比例 Wald 区间；阈值是**从数据里挑出来的**时，选择过程额外引入方差，须用 delta method 或 bootstrap（Wikipedia 镜像逐字）。实证做法：PMC6355005 用 2000 次 bootstrap 重抽样给最优截点的 95% CI；另需注意 J 逼近上界（J≥0.90）时常规 bootstrap 覆盖变差，改用修正 bootstrap 或参数法。判据——凡报告「最佳阈值」，验收栏固定四格：`J 点估计 / 该点 Se·Sp / 阈值 CI（含选择不确定性）/ J 的区间方法`，缺任一判不完整。

**判重**：全库 SKILL.md / module-memory / co-learn 对 `Youden` / `Youden index` / `J statistic` 0 专节；§十四似然比（验前验后与 portable）、§十九 Bland–Altman（一致性非相关）、§二十一评分者间信度（系数按标签形状选）、§九统计功效均异命题；与 PPV/准确率/ROC 是阈值选择与排序评价的分工，非重复。豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地。

**来源与诚信**：`https://pmc.ncbi.nlm.nih.gov/articles/PMC6355005/`（WebFetch 200 全文逐字：J 定义、0–1、`independently from the outcome prevalence`、2000 repeats bootstrap CI、closest-top-left 对照）——第一独立域·同行评议开放全文；`https://www.sciencedirect.com/science/article/abs/pii/S0167947314000450`（WebSearch 摘要+Introduction 全文逐字：Se/Sp 在估计截点相关、须联合置信域、相同 J 不同 Se/Sp）——第二独立域·统计学期刊；`https://www.sciencedirect.com/science/article/pii/S0167947317300592`（WebSearch 全文逐字：最大垂直距离、等权前提、J≥0.90 边界覆盖）——第三独立域·统计学期刊；`https://wikipedia.com/wiki/Hanssen%E2%80%93Kuipers_discriminant` 镜像（WebSearch 全文逐字：展开式、负值语义、固定阈值 vs 优化阈值的区间区别；Wikipedia 原页 WebFetch failed 未冒充一手）交叉。逐字全文与判非见 `references/r810A_Youden指数J.md`。


## 二十五、测量系统分析 MSA / 量具 GR&R：先证明「量尺本身」可信，再谈数据结论（VI · 2026-11-27 实拉，≥4 独立域一手）

**独点 1｜变差分解：EV 重复性 × AV 再现性，GRR 是两个方差的合成而非相加。** 总变差 σ²_total = σ²_parts + σ²_repeatability + σ²_reproducibility。EV（equipment variation，重复性）= 同一操作者、同一量具、同一零件多次测量的波动，反映设备/夹具/分辨率/定位/方法本身；AV（appraiser variation，再现性）= 不同操作者对同一零件测量平均值的差异，反映手法/读数/基准理解/培训一致性。**GRR = √(EV² + AV²)**（按方差合成，不是 EV+AV），再与零件间变差 PV 合成总变差 TV = √(GRR² + PV²)。两口径必须分开看：`%GRR = GRR/TV × 100%`（占总变差，用于过程监控，反映测量噪声在过程波动中的占比）；`%P/T = GRR/TOL × 100%`（占公差带，用于公差判级/放行，反映测量误差吃掉多少规格）。只报一个口径不足以支撑结论——生产监控看前者、公差放行看后者。

**独点 2｜AIAG MSA 4th 判定门槛与「GRR<10% 就合格」的陷阱。** 门槛：%GRR < 10% 可接受；10%–30% 条件可接受（按应用重要性/成本/风险决定）；> 30% 不可接受必须改进。可区分类别数 **ndc = 1.41 × (PV/GRR) ≥ 5**——ndc 与 %GRR 是一枚硬币两面（%GRR 越小 ndc 越大），ndc<5 说明量具分不出零件差异，即便 %GRR 数字好看也不合格。**核心陷阱：%GRR 是相对指标**，分母 TV 含零件真实差异——挑选覆盖公差带的大范围零件会压低 %GRR，制程优化后 TV 变小则同一把量具 %GRR 反而升高。故须同时检查量具分辨率、ndc、偏倚 Bias、线性 Linearity、稳定性 Stability 与实际过程能力，并核对取样零件是否代表正常过程范围；EV 明显大于 AV 时改进优先夹持定位与量具分辨率，而非先加强人员训练。

**独点 3｜两算法与试验设计：均值极差法 vs ANOVA；10×3×3 与自动化第一类研究。** 均值极差法（Xbar-R）用极差估 EV、用操作者均值极差估 AV，简单可 Excel，但**无法分解「操作者×零件」交互作用**、受异常值影响大。ANOVA 把变差拆成零件、操作者、交互作用、重复性四块（EV=MSE，AV 含 (MSA−MSAP)/(n×r) 与交互 (MSAP−MSE)/r，PV=(MSP−MSAP)/(k×r)，估计值<0 取 0），可处理不平衡数据，是 AIAG MSA 4th 推荐完整方法；交互作用大 = 某些人量某些零件特别不一致（如形状导致有人侧量有人顶量），均值极差法会把它混进其他项。标准设计 **10 零件 × 3 操作者 × 3 次 = 90 读数**，零件须覆盖过程公差范围（不是挑 10 个几乎一样的），随机顺序、操作者互不知零件编号、不参考自己上轮读数（否则记忆偏差）。自动化设备/单一夹具再现性≈0 时，用**第一类研究**（一个工件 ≥25 次连续测量，σ_repeat = √(Σ(xᵢ−x̄)²/(n−1))，EV=6σ_repeat）替代完整 GR&R 在统计上更诚实；若仍有人工装载/选点则再现性重新引入，须做完整交叉/巢状 GR&R。

**判据（VI 落地）**：凡以「同一套测量/标注/评分流程得出的数字」做结论——代码测试通过率、标注一致率、A/B 指标、模型评测分——先问三件事：① 量尺变差是否被分解并量化（重复 vs 再现 vs 对象差异）；② 门槛与口径是否事前声明（%GRR 还是 %P/T，阈值取几）；③ 取样范围是否被人为选择而压低了变差占比。不能回答者，结论只算「未验证测量系统下的观测」，不得升级为事实。与 §十九 Bland–Altman（两方法一致性）、§二十一 IRR（评分者间信度系数）、§九统计功效分工：本节点在「量尺自身的可重复/可再现与分辨力」，IRR 在「多个评分者系数的选择」，Bland–Altman 在「两方法可否互换」，均异命题。

**判重**：全库 SKILL.md / module-memory / co-learn 对 `测量系统分析` / `GR&R` / `Grubbs` / `重复性再现性` 0 专节；豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地。

**来源与诚信**：`https://www.6sq.net/intro/grr/`（WebFetch 200 全文逐字：EV/AV/GRR/PV/TV 定义、两口径、10/30 门槛、ndc 公式、两算法、10×3×3 设计）——第一独立域·行业工具站；`https://jiahon.com.tw/?p=124432`（WebSearch 全文逐字：AIAG 第四版 K 系数、%GRR 对总变异 10.1% / 对公差 15.3% 算例、ndc=13、EV 9.3%>AV 3.8% 的改进指向、ANOVA 四块方差分解式）——第二独立域·计量技术页；`https://jcetech.cn/equator-grr-ppap`（WebSearch 全文逐字：PPAP 公差带口径、GRR=√(EV²+AV²)、ndc≥5、10×3×3=90 读数、零件须覆盖过程变差）——第三独立域·检测厂商；`https://industrialmonitordirect.com/zh-hant/blogs/knowledgebase/alternatives-to-grr-msa-methods-for-industrial-measurements`（WebSearch 全文逐字：AIAG 门槛表含 Study Variation 30%/60% 对应、10×3×3 三点局限、第一类研究 ≥25 次 σ_repeat 与 6σ 公式、多夹具则须完整 GR&R；明言 MSA 是参考框架非法规、CSR 可改限值）——第四独立域·工业测量站；`https://ucourse.org/p/14482`（WebSearch 全文逐字：GRR 是相对指标受制程变异影响、ndc<5 时 %GRR 5% 仍不合格）——第五独立域·质量培训。逐字全文与判非见 `references/r814A_测量系统分析GRR.md`。


## 二十六、生存分析（time-to-event）：还没发生的样本不是「成功」，也不是缺失值（VI · 2026-11-28 实拉，≥2 独立域一手交叉，3 独点）

**独点 1｜删失不是缺失值、也不是事件：KM 乘积限把「最后一次观察时间」和「是否发生事件」两列同时用起来。** 生存分析的结局是「从起点到某事件发生的时间」（故障/死亡/流失/漂移），研究结束时未发生事件者是被**右删失**（right censoring：只知事件在 t 之后、不知确切时刻），既不能当「已发生」也不能整条丢弃。Kaplan–Meier 乘积限估计 `Ŝ(t)=∏_{tᵢ≤t}(1−dᵢ/nᵢ)`：在每个事件时刻 tᵢ，dᵢ 为该时刻事件数、nᵢ 为恰在 tᵢ 前的风险集人数，删失者在其删失时刻之前计入 nᵢ、之后退出；S(t) 是「到 t 仍未发生事件」的概率，S(0)=1 随 t 递减。StatsDirect 明列三条假设：① 删失者与继续随访者生存前景相同——**无法检验且会人为压低 S**；② 早晚期入组者生存前景相同（可检验）；③ 事件在规定时刻被记录，迟记会人为抬高 S。⇒ 凡「跑一段时间才知道结论」的验证（功能多久后出错、用户多久流失、设备多久失效），验收表必须同时有「末次观察时间」与「事件是否发生」两列，只统计已发生者或把未发生当作成功都判违规。

**独点 2｜中位生存期是首次 S≤0.5 的时刻，曲线比较用 log-rank 而非某一时点的率。** 中位生存期 = S 首次降到 0.5 或以下的时刻（Brookmeyer–Crowley 给 95% CI）；平均生存期是 S 曲线下面积，受最长随访时间限制，删失多时只能估到删失比例以内的分位（statsmodels：约 30% 受试者死亡时，只能估 0.3 概率点以下的分位数，如 0.25 分位），拿平均生存期冒充典型值会掩盖重尾。比较两组不能挑某个时点的生存率比大小（选点即引入选择偏差）；`survdiff` 默认 **log-rank** 是非参数、对整条曲线做检验，另有 Gehan–Breslow（按风险集人数加权，更重早期差异）、Tarone–Ware（按 √风险集加权）、Fleming–Harrington（按合并生存时间加权，p=1 更重晚期）——**不同加权回答不同问题，须事前声明**，不能看完哪条显著再挑。⇒ 验证报告写「A 组更可靠」须给出曲线、log-rank p 值与所用权重，缺一不算。

**独点 3｜Cox 比例风险模型估的是乘性效应，比例风险假设是前提而非可选项。** Cox 模型 `h(t|x)=h₀(t)·exp(xᵀβ)`：基线风险 h₀(t) 非参数、不必指定形状，协变量效应以**风险比 HR=exp(βₖ)** 表达——「瞬时事件率被乘以某个倍数」，不是「某时刻生存率高多少」，也不是概率。估计用**部分似然**（只用到事件时刻的风险集）。核心前提 **PH 假设**：任意两人的风险比不随时间变化；违例时 HR 是随时间变化的平均值、不可照搬。检验用 log-log 生存曲线是否平行、Schoenfeld 残差是否随时间有趋势、或引入时变协变量；违例改用**分层 Cox**（对违背 PH 的变量分层、对其余变量估系数）或**扩展 Cox**（含时变变量）。⇒ 凡报 HR 必同时报 95% CI、PH 假设检验结果与基线风险未参数化这一事实；把 HR 讲成「概率提升 x 倍」或跳过 PH 检验，判为误读。

**判据（VI 落地）**：以「经过一段时间才见分晓」的指标做验证时，先问三件事——① 删失样本是否被显式记录而不是被删/被当成功；② 曲线比较是事前声明的 log-rank 与权重，还是事后挑时点；③ 若用 Cox 报效应，是否带 CI 且验过 PH 假设。三者缺一，结论只算「在有偏观测上的描述」，不得升级为事实。与 §九统计功效（多少样本）、§二十二序贯检验（何时看）、§二十四 Youden（阈值怎么选）、§二十五 MSA（量尺是否可信）分工：本节点在「时间到事件且结局尚未全部揭晓时怎么验证」，均异命题。

**判重**：全库 SKILL.md / module-memory / co-learn 对 `生存分析` / `Kaplan-Meier` / `log-rank` / `Cox 比例风险` 0 专节（仅豆包自留地 `wb-context-compressor` 有 `calibration` 语境一句，异命题且 WB 0 落地）；与 PDI 预测（预测值校准）、VI §十四似然比（验前验后迁移）、§十三谱偏倚（人群依赖）分工不复用。

**来源与诚信**：`https://www.statsdirect.com/help/survival_analysis/kaplan_meier.htm`（WebFetch 200 全文逐字：S(t) 定义、乘积限公式与 dᵢ/nᵢ 语义、删失三条假设、Greenwood 方差、Peterson=−ln(S) 与 Nelson–Aalen、log-rank/Wilcoxon 无需分布假设、Brookmeyer–Crowley 中位 CI）——第一独立域·统计软件官方文档；`https://www.statsmodels.org/stable/duration.html`（WebFetch 200 全文逐字：right-censoring 定义、SurvfuncRight、survdiff 默认 logrank 与 FH/Gehan-Breslow/Tarone-Ware 加权、PHReg Cox 模型、HR 乘性效应、30% 死亡只能估 <0.3 分位）——第二独立域·开源统计库官方文档；`https://zh.wikibooks.org/wiki/数理统计/生存分析与打分检验`（WebSearch 快照逐字：S=exp(−H)、KM 公式、Nelson–Aalen、Cox 部分似然 L(β)、Schoenfeld 残差、Score/log-rank/Wald 三者分工）与 `https://www.eolss.net/Sample-Chapters/C02/E4-31-02-04.pdf`（Kleinbaum 等《Survival Analysis》章节 WebSearch 摘要逐字：censored 定义、PH 假设 log-log 曲线、分层/扩展 Cox）——第三、四独立域教材交叉，WebFetch 本地回退禁用（`CODEBUDDY_WEBFETCH_DISABLE_LOCAL_FALLBACK=1`）如实登记不冒充全文。诚信：`https://www.ncbi.nlm.nih.gov/books/NBK539796/` 号错配（实为桡动脉置管）整篇弃用；`biostathandbook.com/survival.html`/`statology.org/kaplan-meier-curve`/`medcalc.org/manual/cox-*` 均 404 未采纳；维基教科书与 wipedia 同族按来源族折叠。逐字全文与判非见 `references/r819A_生存分析.md`。

## §四十一 r822A · DeLong 检验：AUC 差异是否超出抽样波动（VI · 2026-11-28 实拉，3 页 MedCalc 官方 + PubMed 原论文摘要，3 独点；全文见 `references/r822A_DeLong检验.md`）

§r810A Youden 管选阈值、§r788B Bland-Altman 管两法一致性，本章管**两方法 AUC 谁更高且差异是否显著**。
**独点1 配对必须带协方差，两套公式不能混用**：同一批患者测两检验 → 难分类者两法都模糊 → AUC 正相关，忽略则标准误膨胀、检验保守。DeLong 1988 非参数法起点 AUC≡Wilcoxon 秩和（核 ψ=1/0.5/0），以 structural components（jackknife 推广）估方差与协方差。配对 `z=(θ̂₁−θ̂₂)/√(Var₁+Var₂−2Cov₁₂)`、双侧 p=2Φ(−|z|)、差 CI 同根号；独立样本 Cov=0 直接用 `√(Var₁+Var₂)`，两法混用是方法论错误。
**独点2 k≥3 先全局后两两、Hanley–McNeil 仅存旧法**：k 条同人群曲线算 k×k 协方差，取 k−1 对比向量 c，`χ²=cᵀV⁻¹c` df=k−1，显著后才逐对 z 检验（NGAL/KIM-1/cystatin C 0.84/0.79/0.76 例）。H&M 1983 用平均 AUC+原始分数 r 查表得 r′ 近似，DeLong 直接从数据估协方差故优选；H&M 仅复现旧文献。AUC 的 95%CI 用 binomial exact（**不适用 AUC 之差**）。
**独点3 统计显著≠临床相关**：大样本 AUC 差 0.01 也 p<0.05；0.03 多可忽略、≥0.10 才实质重要；曲线交叉时整体 AUC 掩盖「高敏区 A 优/高特区 B 优」必须看图；AUC 无显著差异时选更便宜/快/低侵入者。报告须含各 AUC+CI、差+CI、p，差的 CI 比单独 p 更有信息。
**来源与判非**：MedCalc book/medcalc.org manual 两页 + PubMed PMID 3203132 全文 WebFetch200；arXiv:1402.9224 not found、1701.06359 主题错配已弃用如实登记。全库 DeLong 0 专节、豆包自留地 WB 0 落地 ⇒「增＝加厚现有」0 新建。声明不替代：阈值选择/一致性评价/临床效用判断。


## §r824A · Brier 分数与概率校准：单一误差值混合了校准与分辨力（VI · 2026-11-28 实拉，scikit-learn 官方 + 百度百科 + 三份可验算笔记，全文见 `references/r824A_Brier分数与概率校准.md`）

§十 ECE 管置信度校准、§十五 Conformal 管覆盖保证、§r810A Youden 管阈值选取、§r822A DeLong 管 AUC 比较，本章管**概率预测自身的严格适当评分与三分量分解**，四者互补不复用。
**独点1 单一 Brier 值不得单独判校准**：scikit-learn 1.16 逐字「Strictly proper scoring rules ... assess calibration (reliability) and discriminative power (resolution) ... as well as the randomness of the data (uncertainty) at the same time」「A lower Brier loss ... does not necessarily mean a better calibrated model, it could also mean a worse calibrated model with much more discriminatory power」。验收固定四格 `Brier/REL/RES/UNC`，缺分解项不得下「校准更优」结论。
**独点2 Murphy 分解 BS=REL−RES+UNC**：REL=Σ(n_k/N)(f_k−o_k)² 越小越好（零只表示「报准了基率」不等于好模型）、RES=Σ(n_k/N)(o_k−ō)² 在恒等式中被减去故越大越好（定义在观测频率而非口头概率的分散）、UNC=ō(1−ō) 由数据固定且跨人群不可比；技能分 SS=(RES−REL)/UNC。数值反例：每次报 0.2 者 REL=0/RES=0/BS=0.16/SS=0（完美校准、零技能）；分报 0.05/0.35 两档者 REL=0.0001（大 100 倍）却 BS=0.1345 好 16%。
**独点3 可靠性图=分箱画预测概率对实际正例频率**：x 轴各箱平均 predict_proba、y 轴箱内正例比例；形状指纹 NB 推 0/1、RF/SVC 呈 S 形；校准器 sigmoid/isotonic 须在**独立留出集**拟合，否则重演 §十泄漏。AUC 只排序，不保证概率等于真实频率。
**来源与判非**：scikit-learn 1.16 官方 WebFetch200 全文 + 百度百科（Brier 1950/Murphy 1973/严格评分/二分类[0,1]）+ cibo.hk 数值反例/codeboy.site 符号辨析/insightful-data-lab 命名陷阱三份可验算笔记；Wikipedia WebFetch 本地回退禁用如实登记，不冒充 200。全库 `Brier`/`reliability diagram`/`calibration curve`/`Hosmer` WB 侧 0 专节，`calibration` 命中为 ECE/Conformal/豆包自留地异命题。
