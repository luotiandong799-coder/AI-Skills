

## r565B · 评测失效两条（来源：arXiv 2610.16067 / 2610.15884，2026-10-14 实拉）
- **实证**：① 「When Agent Evaluation Becomes Unreliable: An Empirical Study of Oracle Failures and Configuration-Dependent Measurement in an LLM Agent Benchmark」——基准中 oracle 自身会失效，测量结果依赖配置；② 「RetryBench: Separating Retry Permission from Recovery Outcomes in GPT Tool Use」——重试许可与恢复结果被显式分离度量。
- **判据**：① **oracle 失效与能力不足分账**，且「配置依赖测量」单独记账：配置随版本漂移时跨次分数不可比，配置本身要版本化。② **重试许可与恢复结果分别入分**：给更多重试机会拉高成功率但不代表单次恢复更可靠。
- 提升层：工具（评测可靠性）/ 工作流（指标设计）。
- 触发词：oracle 失效、配置依赖测量、重试许可与恢复结果分离。

## r566B · 授权集与缓存口径两条（来源：arXiv 2610.15137 / 2610.15093，2026-10-14 实拉）
- **实证**：① 部署/编码 agent 的审批存在「被批准文件未变」情形——此时授权集（authority-set）完整性成为唯一判据，按文件判定的批准不再成立；② 循环工程的成本须按缓存感知口径计，观测次数不等于真实成本。
- **判据**：① **审批有效性双条件**：被批准文件内容未变 **且** 授权集未漂移，任一不满足即复校；不得以「文件没动」单独放行。② **预算与成本对照用 cache-aware 口径**：缓存命中不计入轮次成本，报告须同时给命中/未命中分解，否则预算对照无效。
- 提升层：工作流（审批有效性判定）/ 工具（成本与预算测量口径）。
- 触发词：授权集完整性、被批准文件未变、复校授权、缓存感知、轮次成本、观测次数不等于成本。


## r573B/C 下沉条目（2026-10-15，来源见文末，均为一手实拉）
① **评测器本身必须作为实验变量审计：需求契约化 + 冻结候选只扰动评测剖面**——tool-grounded requirement profiles：把每条需求的含义绑定到「可执行证据 + 比较规则」的机器可读契约，并带跨需求门、不确定性处理与溯源；审计方法是**冻结候选对、只扰动评测剖面**。预注册对照（6 个设计 / 12 对 / 3 个需求族 / 6 个评测条件 / 72 次判定）中，通用 cell-count 评测器对 12 对里的 6 对（50%）报出了**不被支持的改进**。判据：① 评测结论须在「只改评测契约、不动候选」下复测稳定性，报改进前先证明该改进在剖面扰动下不翻转；② 需求不能是自然语言断言，必须携带证据来源与比较规则；③ 安全规则/协议义务/目标上下文/可行性门/不确定性策略/溯源约束任一被省略都可能制造假的「更好」。来源：arxiv.org/abs/2610.17445（export API 200，逐字 `machine-readable contracts binding each requirement's meaning to its executable evidence and comparison rule` / `a generic cell-count evaluator reports unsupported improvement for 6/12 pairs (50%)`）。触发词：requirement profiles、评测器作实验变量、冻结候选只扰动评测、50% 改进不成立、需求契约化。
② **归因必须落到「断言↔证据单元」的映射，并把「缺失干预」与「抽样不确定性」分开**——RelLedger：agent 组织里共享记录决定了后续决策能用到哪些事实，而跨历史的投递缺口既不显示是哪段关系驱动了选择、也不显示该记录下游是否重要；方法是固定事件/证据/风险/消息，交叉发送方的历史与「事件目标」和「无关角色」，用角色重分配与历史重写定位控制性线索，并用消息/成本干预定位效应出现的条件；归因账本把每条断言映射到它必需的响应单元。判据：① 归因结论必须列出支撑它的具体响应单元，不能只给方向；② 「没做干预/没送到」与「抽样噪声」是两种失效，混在一起会让干预效果无法解释。来源：arxiv.org/abs/2610.16281（export API 200，逐字 `A delivery gap across histories does not show whose relationship drove the choice or whether the resulting record matters downstream` / `separates missing interventions from sampling uncertainty`）。触发词：RelLedger、attribution ledger、缺失干预 vs 抽样不确定性、断言↔证据单元映射、角色重分配定位。
③ **不接受「完美同事」隐含假设：协作验收须覆盖 Misaligned / Incomplete / Missed 三型失败**——现有多 agent 系统与评测默认同事「信息正确、完整、响应及时」；UnCoBench 用答非所问（Misaligned）、细节不足以支撑决策（Incomplete）、根本不响应（Missed）三类行为失败，**把「解题能力」与「从不可靠取证过程中恢复的能力」分开**；主 agent 需要验证上下文正确性、诊断信息缺口、跟踪未决请求。判据：① 委派/协作类评测必须把「同事可靠」从隐含假设改为显式变量；② 三型失败各自单独计分，混合计分会掩盖「会做题但不会发现被喂错料」；③ 主 agent 侧须有未决请求的跟踪面。来源：arxiv.org/abs/2610.16117（export API 200，逐字 `an implicit perfect-colleague assumption` / `Misaligned, Incomplete, and Missed settings` / `verify contextual correctness, diagnose information gap and track unresolved`）。触发词：UnCoBench、perfect-colleague assumption、Misaligned/Incomplete/Missed、未决请求跟踪、取证过程恢复。
④ **评测通道必须与被评对象的真实使用形态一致：交互型产物不能只靠代码分析与单测**——Interaction-as-a-Judge：人类是**交互着**评估网站/桌面应用/游戏的，而自动评测主要做代码分析与单元测试，这个错配让 LLM 判官漏掉人类一眼可见的失败；做法是让 computer-use agent（CUA）直接交互应用来评判，同时改善评测与生成，并发布 6,858 对带人类偏好的应用＋agent trace 与 222 个带人工核验需求标签的应用。判据：① 评测协议须声明「评测通道 vs 使用通道」的一致性，交互型产物用静态通道得到的结论要标注覆盖边界；② 判官的输入形态（能操作 vs 只能读码）是评测有效性的独立变量。来源：arxiv.org/abs/2610.17895（export API 200，逐字 `While humans assess these applications interactively, current automated LLM evaluations primarily focus on code analysis and unit tests` / `computer-use agents (CUAs) directly interact with an application`）。触发词：Interaction-as-a-Judge、CUA 交互评判、静态评测漏检、交互型产物、6,858 对偏好数据。
⑤ **安全评测四道有效性门：投递确认 / 实参级评分 / 误拒与能力分账 / 审计轨迹**——审计一个间接提示注入（IPI）基准与其 harness，识别四类缺陷，每类都能产出「看起来合理、可发表」的结论：① **silent payload non-delivery**（攻击载荷根本没送达却当成防御成功）；② 攻击成功按**工具身份**而非实参判定；③ 误拒率与模型能力不足混为一谈；④ 没有审计轨迹。判据：安全/对抗类评测在报结论前须过四门——证明载荷真的送到、在实参级判攻击成功、把「不肯做」与「做不到」分开计、保留可复核轨迹。注：与库内 r572 登记的 Silent Failure 2606.08162 **非同篇**（不同 arXiv 号与机制），勿互判重。来源：arxiv.org/abs/2609.32691（export API 200，逐字 `silent payload non-delivery, attack success scored by tool identity rather than arguments, false-rejection rate conflated with model incapacity, and the absence of an audit trail`）。触发词：silent payload non-delivery、按工具身份评分、误拒与能力混算、审计轨迹、IPI harness 缺陷。

## r574B 下沉条目（2026-10-15 arXiv abs 一手 https 200）
① harness 自演化：更新目标 / 提议机制 / 准入机制三者分离，解释态与工具代码分开设定保留界（retention bound），accepted revisions persist across runs（arXiv 2610.18813 Self-Evolving Agent Harness）。
② 评测加载语义须与运行语义一致：单次回答口径 +0.41 合规增益，真实懒加载下四 agent 平均仅保留约 51%、三开源模型约 38%；加载一次技能正文使 episode token +50%（arXiv 2610.04832 Agent Skill Evolution，经 Qoder r628-Q-C③ 提名）。

## r575B · 评测的 oracle 自身也要审计：用状态完整性不变量查「分数表看不出」的可靠性缺陷（来源：arxiv.org/abs/2610.16067《When Agent Evaluation Becomes Unreliable: An Empirical Study of Oracle Failures and Configuration-Dependent Measurements》，2026-10-15 r575B 一手 curl 摘要 200）
——评测 harness 本身是软件系统，会有状态残留、夹具污染、判定泄漏。公布分数前先过不变量，否则结论没有地基：分数可复现不等于评分逻辑可信。
## r575B · 分数变化先归因评测变更，再谈能力变化（来源：arxiv.org/abs/2610.11678《TRACE: Diagnosing Verifier Brittleness in Agentic Evaluation》，2026-10-15 r575B 一手 curl 摘要 200）
——分数变化通常被直接读成能力变化，但它也可能只反映评测变了。判据=发布「能力变化」结论前，先跑归因协议把「能力变」与「评测变」分开，两者可同时为真。
## r575B · 重执行判定不变不等于策略风险消解（来源：arxiv.org/abs/2610.14460《Re-executing Coding-Agent Evaluations: Unchanged Decisions and Unresolved Policy Risk》，2026-10-15 r575B 一手 curl 摘要 200）
——重跑得到同样判定只说明结论稳定，不说明评分配置与准入策略没有风险。复现性与策略合规是两条独立结论，必须分别报告，不得用前者替代后者。
## r575B · 证据方法与声明强度必须匹配，残余要显式声明（来源：arxiv.org/abs/2610.04710《Organising Trajectory Evidence for Language-Model Agent Assurance: Fragments, Methods, and the Residual》，2026-10-15 r575B 一手 curl 摘要 200）
——规则检查、技能覆盖分析、支持检查、前缀监控、执行门、稀有事件估计各只看一段运行，能给出的声明强度不同。混用而不标注会把弱声明读成强保证。判据=结论须写明所用方法、覆盖哪一段、残余是什么。
## r575B · 用户模拟器普遍过度配合会高估鲁棒性（来源：arxiv.org/abs/2610.16155《Uncovering Robustness Weaknesses in LLM Agents via Persona Evolution with Task-Integrity Constraints》，2026-10-15 r575B 一手 curl 摘要 200）
——标准化 LLM 用户模拟器行为过于合作，漏掉真实交互下的失败，分数系统性偏乐观。判据=交互类评测须注入多样且带任务完整性约束的用户人格，并单独报告「对抗人格下」的分数。
## r575C · 评测用例须在真实操作者身份下运行（来源：api.github.com/repos/windmill-labs/windmill/pulls/11768 `run global ai eval cases under builder operator profiles`，2026-10-15 r575C 一手 gh api 200）
——以特权/服务账号跑评测会绕过权限校验，通过的用例在真实用户身份下可能全败。判据=评测环境复用生产授权路径，禁止为「跑得通」而放宽身份。
## r575C · 恢复/容错评测三判据（来源：arxiv.org/abs/2606.05806《When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents》，2026-10-15 r575C 一手 curl abs 200 逐串命中 `2 x 2 taxonomy`；候选来源 Qoder r631-Q-C）
——① 按扰动类型分档（显式/隐式 × 瞬时/持久），隐式语义失败最致命；② 用扰动恢复率而非只看最终成功率，否则「蒙对」与「恢复」不可分；③ 容错与执行是两条不同的缩放曲线，堆模型规模换不来容错能力。
## r575C · 自愈「成功」须加安全门：被修复代码改动的运行时状态是否经 taint 分析触达受保护操作（来源：arxiv.org/abs/2609.39086《Trustworthy Runtime Error Healing in Real-World Repositories: A Benchmark and Guardrail》，2026-10-15 r575C 一手 curl abs 200 逐串命中标题与 `safety concerns`；候选来源 Qoder r631-Q-C）
——通过目标测试的自愈执行里仍有相当比例可能越权；自愈成功 ≠ 自愈安全。判据=安全门作为独立通过条件，与测试通过并列，二者都过才算自愈成功。

## r577C · **等价 schema 表述是被测混淆变量：评测与跨方案对比前须做表述敏感性测试**
- **实证**：arXiv 2609.34971《Action-Space Shaping for LLM Agents: Measuring and Mitigating Tool-Schema Bias》（abs 200 一手逐串命中）——工具 schema 不是 agent 的动作空间，**只是它的一种接口表示**；同一个可执行动作可以通过多种功能等价的工具定义暴露，真正学会了任务的 agent 应当在它们之间表现一致。作者指出当前 agent 常常做不到，称为 **schema bias**；并给出可执行变换框架，用 **nine operators**（含合并与拆分工具等）重写原生 schema，在 **eleven LLMs、最多 32 种 schema 变体**上测：`success rates range from complete failure to 97% depending solely on the schema`。
- **判据**：① **不归一化等价表述，测的是 schema 措辞而不是能力/兼容性**——同一动作换个写法成功率可从"完全失败"到 97%，此时任何跨模型/跨方案的对比结论都不可信。② **评测控制变量清单要显式包含"接口表述"**：现有评测通常控模型、数据、harness，未控"等价 schema 表述"这一变量（本库此前 0 命中）。③ 技能/工具作者视角的反面：工具的 schema 写法本身是性能因素，改 schema 等于改被测对象，因此**改 schema 后必须重测而不能沿用旧结论**。
- 提升层：可复用 Skill（评测有效性）/ 工作流（跨方案对比口径）。触发词：schema bias、等价表述、Action-Space Shaping、nine operators、32 schema variants、表述敏感性测试、混淆变量。（经 Qoder r632-Q-B 提名，WB 一手复核属实。）


## r581C · **裁决要连同「解释」一起报：把解释显式化成结构化卡片，才能定位分歧来自证据还是来自读法**
- **实证**：arXiv 2610.20457《Same Claim, Different Interpretations: How LLM Agents Resolve Ambiguity in Scientific Claims》（abs 200 一手）——面向专家写的科学论断常欠定、可有多种站得住的解释；验证 agent 通常隐式地挑一种，而基准直接拿它的裁决对专家标签打分，不记录双方解释，导致分歧无法归因。做法 **Claim Cards**：在取证**之前**把验证方对论断的解释记成 9 个字段，每字段标注 stated / inferred / default。GPT-5.4 agent 在 60 条专家标注的材料 / 生物医学论断上各跑 5 次（有卡片、无卡片、卡片冻结跨轮）共 900 次：**>40% 的卡片字段并非 stated**；加卡片约增加 1/10 的 token 与时间却**不显著改变**与专家标签的一致率；agent 自己的解释在轮间会变，但这种变化在单条论断内不显著影响裁决。而**刻意改动冻结卡片的一个字段**（把量词改成全称、或把支持阈值改严）让约 **1/3** 的论断裁决翻转，远高于随机预期（约 1/7，p<0.001）；在 24 条带计算工具的材料科学论断上，严阈值还改变了 agent 让工具去算什么。作者据此主张：裁决应与其解释一并报告，基准可公开每个标签背后的解释。
- **判据**：① **欠定任务的分歧要先归因再优化**：分歧可能来自「读法不同」而非「证据不足」，不把解释显式化就无法区分，改 prompt 调证据多半无效。② **解释卡片的价值在「改一个字段能翻转裁决」**：既证明卡片确实捕获了裁决所依赖的读法，也提供了一个便宜的可验证实验（单字段扰动）。③ **成本要诚实记账**：加卡片约 +1/10 token 与时间且不自动提升一致率，价值在于可归因与可报告，不在于提分——报收益时不能只报后者。④ 输出纪律：裁决与解释同批报告，解释字段标注 stated / inferred / default，禁止把 inferred 当既定前提往下传。
- 提升层：可复用 Skill（裁决可归因）/ 工具（结构化解释卡片）。触发词：Claim Cards、9 字段、stated/inferred/default、40% 非 stated、单字段翻转 1/3、解释与裁决同报、欠定论断。

## r581C · **「准确率高」不是可部署的证明：模块误差的相关性有符号，独立假设会系统性算错**
- **实证**：arXiv 2610.19051《Smart Alone, Blind Together: Why Accuracy Fails to Certify Theory of Mind in Multi-Agent Teams》（abs 200 一手）——协调者依据对队友的推断行动，通常用推断准确率认证；本文论证准确率是错误的证书，两个原因：① 行动所需的准确率取决于**做错动作的代价**，门槛属于部署而非模块；② 模块误差很少独立，且**相关性有符号**——误差正相关时在损害重叠处互相帮忙、在损害叠加处互相放大，因此基于准确率的阈值会**朝可预测的方向失效**。实验（任务分配、Level-Based Foraging、Hanabi + 注入误差 + 训练 / 贝叶斯模块 + 5 个语言模型 + 人类判断）显示准确率双向失效：在 Hanabi（误差叠加）里放行了有害的语言模型部署，在任务分配（错动作代价高且罕见）里拒绝了有益的部署。冗余收益远低于独立假设预测：从 GPT-5.4-mini 到 Claude Opus 5.5，对「有证据的队友」的误差从 32% 降到 11%，但**三个观察者同时误判同一人**的概率只从 16% 降到 9%（独立假设预测 3.4% → 0.15%）。提出 **Blind-Spot Gate**：在**不部署模块**的前提下，用误差代价、两两交互与实测相关性定价；在其开发所用 cell 的留出数据上 20 个切分无显著误放行（准确率 3.2 次/切分），在未参与开发的模块上预注册测试里既找回准确率拒掉的（7 个分类器 regret 0.004 vs 0.479）也抓住准确率放过的（贝叶斯模块 20 个切分中准确率误放 17 次、该门 1 次）。
- **判据**：① **认证对象应是部署而不是模块**：同一模块在不同代价结构下门槛不同，把「准确率 X%」当可部署证明是错层的。② **冗余度必须用实测相关性估，不能用独立性估**：本例实测同时误判 9% vs 独立假设 0.15%，差 60 倍——按独立假设设计的冗余会严重不足。③ **相关性符号决定它帮忙还是伤害**：误差重叠处正相关有利、叠加处有害，因此验收要分别在这两类场景下测，只测一种会得到方向相反的结论。④ 不部署也能做门：用历史失败样本估代价矩阵与两两相关性，作为预部署闸门。
- 提升层：可复用 Skill（部署认证与冗余度评估）/ 工具（误差相关性治理）。触发词：准确率不是证书、误差相关性符号、冗余度按独立性高估、32%→11% vs 16%→9%、Blind-Spot Gate、不部署预认证、regret。

## r581C · **不确定度可以从推理链的逻辑结构里出，不必再采样：论证图后验 vs token / 一致性基线**
- **实证**：arXiv 2610.20328《Argument Graph Uncertainty: Quantifying Uncertainty from the Logical Structure of Reasoning Chains》（abs 200 一手）——现有不确定度估计多依赖昂贵采样或浅层 token 级信号、忽略输出的内部逻辑结构。做法（事后框架、多选题任务）：用轻量指令模型或纯确定性规则把单条 CoT 推理链切成命题单元，用 NLI 模型推断关系边并构建两张互补的论证图，把边分数聚合成答案选项上的 **Dirichlet 后验**，其浓度即校准的不确定度，同时反映**局部步间连贯**与**全局逻辑一致**。在 GPQA / MMLU-Pro / TruthfulQA 上跨多个推理模型**一致超过** token 级与一致性基线；组合分析显示它与既有方法**信号正交**，可作为集成中的互补分量；**全程不需要被评估模型再调用**，只用小型辅助模型，产出**逐节点的可解释不确定度归属**，算力成本低。
- **判据**：① **不确定度可以事后从已有轨迹算，不必新增采样**：当成本敏感或采样不可行时，先考虑「从单次 CoT 的逻辑结构里出」这条更便宜的通道。② **不同信号源要按正交性而非强弱来用**：与一致性采样信号正交 ⇒ 应进集成而非二选一。③ **要拿「逐节点归属」而非单一标量**：可解释的定位能力决定了这个数能不能用来改流程（定位到哪一步开始不可靠），标量只能用来做门。
- 提升层：工具（不确定度估计）/ 可复用 Skill（自检门限设计）。触发词：论证图不确定度、Dirichlet 后验、NLI 命题边、正交信号、逐节点归属、零额外被测调用、超一致性采样。

## r586C · 评测 oracle 自身要被审计；有状态路由须带会话历史（来源：arXiv 2610.16067 / 2610.19292，2026-10-15 r586C 一手 abs 200）

- **实证**：① oracle-integrity 审计给出**五条状态完整性不变量 + 三个 known-answer 控制**；注入七类 oracle 缺陷跨两任务域 + 一合成域全部被检出，修好的 oracle 无假阳性；用于真实 benchmark 时揭示一个 reward-function 缺陷——**在 post-run 打分之前改变环境状态**；4,320 episode 中回放式修正把 database-pass 标签从 4,194 改为 2,883，测得成功率从 **94.3% 降到 65.5%**；component ablation（3,240 episode）显示 agent 的 policy 文档、工具描述、工具错误字符串都影响观测到的轨迹可靠性，**工具描述的探索性影响最大**（2610.16067）。② 多数路由器把请求当独立请求；有状态 agent 的一个用户轮可能含多次模型与工具调用，难度取决于前几轮产生的状态，换模型还会牺牲会话 prompt 缓存复用；零样本、成本感知、在**用户轮边界**路由并系统变化「是否可见会话历史」，在 SheetCopilot 与 SpreadsheetBench 2 多轮版上：**同等 offloading 率下给路由器会话历史比不给的通过率更高，且对每个模型对都有增益**，history-aware 路由与始终用最贵模型的差距在一个百分点内（2610.19292）。
- **判据**：① **分数表看不见 oracle 缺陷，评测器本身要与被测对象一样被审计**：五条状态不变量 + known-answer 控制是校准锚点，缺它则所有分数无参照。② **oracle 若在打分前改环境状态，历史分数全部不可迁移**（94.3%→65.5%），修正后必须走回放重算；组件消融显示工具描述是最大影响面 ⇒ 评测口径必须声明 prompt / 工具描述 / 错误字符串等非代码变量已固定。③ **有状态场景的路由输入必须含会话历史**（跨轮依赖决定难度），无历史路由会把跨轮依赖算到单个请求头上；**换模型破坏 prompt 前缀缓存** ⇒ 缓存复用必须计入路由成本口径；路由点选在用户轮边界，避免把一个逻辑任务切成两半。
- **提升层**：工作流（评测可信度与路由设计）/ 工具（oracle 审计与成本口径）。
- **触发词**：oracle 完整性、五条状态不变量、known-answer 控制、reward function 改环境、94.3% 降到 65.5%、回放重算、组件消融、工具描述影响最大、有状态路由、会话历史路由、用户轮边界、prompt 缓存复用代价、offloading 率、跨轮依赖。

## r590A · **裁决层不能只有 LLM judge：机械数值检查 + 空真（vacuity）检查补盲区，指标用 accepted-error rate**（来源：arXiv 2610.20573《Beyond LLM Judge: Mechanical Verification for Agentic Autoformalization》，2026-10-15 r590A 一手 arXiv API 200 逐串命中）
- **实证**：方法 `combines LLM-based semantic review with mechanical numerical and vacuity checks, providing checkable feedback and detecting errors missed by LLM judges`；指标口径为 `the lowest accepted-error rate among the evaluated methods, measured as the fraction of incorrect statements accepted by the verification method`；此外 `Expert review of the results also identifies translation and source defects in existing datasets`（金标集本身有缺陷）。
- **判据**：① **语义评审不得作唯一裁决面**：可机械判定的项（数值关系、空真）走确定性检查，零成本零噪声且能发现 judge 漏项，语义层留给开放判断。② **指标用 accepted-error rate（错误陈述被接受的比例）而非通过率**——通过率可被「全拒」刷高，与 r577C「误拦不是正确拒绝」同源。③ **金标集本身是受审对象**：基线数据集的翻译/来源缺陷会被所有对比结论继承，报分前先做专家复核。
- **提升层**：工具（验证层）/ 可复用 Skill（评测裁决）。
- **触发词**：mechanical verification、vacuity check、accepted-error rate、错误被接受率、LLM judge 盲区、基线数据集缺陷。

## r590A · **rubric 聚合不得等权：改用两两重要性比较 + 校正不一致 + 主特征向量导权**（来源：arXiv 2610.19915《Not All Criteria Matter: Importance-Aware Criteria Weighting for Rubric-Based LLM Evaluation》，2026-10-15 r590A 一手 arXiv API 200 逐串命中）
- **实证**：`existing methods commonly aggregate the verification results with uniform weighting, which assigns minor and overlapping criteria the same weight as essential ones and thus produces misleading evaluation scores`；`direct weighting requires a holistic judgment over all criteria that LLMs struggle to make reliably`；做法是 `transforms the holistic judgment over all criteria into a series of pairwise importance comparisons, checks and revises inconsistent comparisons, and derives the weights from the principal eigenvector of the comparison matrix`。
- **判据**：① **次要/重叠准则与核心准则同权 = 分数失真**：rubric 越写越长，等权聚合越偏。② **别让模型直接给权重**：全准则整体判断不可靠，改成两两比较 + 不一致校正 + 主特征向量导权。③ 与 r588A「要求全部约束满足率须与单项 rubric 通过率分开报」分工：那条管报两个口径，本条管**聚合时的权重本身要算出来**。
- **提升层**：工具（rubric 聚合）。
- **触发词**：ICW、criteria weighting、等权聚合失真、两两重要性比较、主特征向量权重、整体判断不可靠、rubric 加权。

## r590A · **单一聚合准确率会掩盖干预类评测的两类反向效应：恢复了失败 / 破坏了成功**（来源：arXiv 2610.19827《MAPLE: A Multi-Axis Parametric Knowledge Extraction Lens for LLM Evaluation》，2026-10-15 r590A 一手 arXiv API 200 逐串命中）
- **实证**：`their evaluations centered on aggregate accuracy, which obscures diverse effects by collapsing recovered failures and disrupted successes into a single score`；诊断指标在 `surface, probability, and beyond-sampling levels` 三层拆开，测 `answer recovery and disruption`、`gold-token rank shifts on unrecovered failures`、`recovery of answers missed by fixed-budget sampling`。
- **判据**：① **一个总分说明不了干预有没有用**：恢复与破坏是两种权衡，合成为一个数后无法比较 ⇒ 干预/引导类评测必须双向分开报。② **分三层测**：表层（答对没）/ 概率层（gold token 排名）/ 超采样层（固定预算下漏掉的答案能否捞回）。③ 结论句写「该干预有效」前必须给出恢复与破坏两个数。
- **提升层**：工具（评测指标口径）。
- **触发词**：MAPLE、aggregate accuracy 掩盖、recovery vs disruption、表层/概率/超采样三层、gold-token rank shift、KEE 双向报告。

## r590A · **整体合理性打分要拆成场景级可验证二元 QA：定向问题换成泛问，评测精度直接掉到随机水平**（来源：arXiv 2610.19823《PhyMetric: Diagnosing Physical Plausibility in Text-to-Video Generation via Scene-Level QA》，2026-10-15 r590A 一手 arXiv API 200 逐串命中）
- **实证**：`recasts physical plausibility evaluation as verifiable, scene-grounded question answering`，含 1,115 场景 / 50 类 / 8,920 答案平衡二元问题 / 12 个评测维度；关键消融——`when each targeted question is replaced by a single generic plausibility query, evaluator accuracy drops to the chance level`；`Structured physical priors offer a complementary signal that improves human alignment of the resulting scores`。
- **判据**：① **泛问式整体评分不可信**：一条「整体是否合理」的泛问会把评测精度打到随机水平 —— 与「没有证据不给通过章」同源。② **每条判据要可逐条核对**（是/否 + 可观测签名），再按场景→维度→类别→模型分层聚合。③ **结构化先验（支配定律 / 期望时序 / 可观测签名 / 常见失效模式）本身是独立信号**，不能只当题干背景。
- **提升层**：可复用 Skill（评测协议设计）。
- **触发词**：PhyMetric、场景级二元 QA、泛问掉到随机水平、结构化先验、可观测签名、常见失效模式、整体评分不可信。

## r590A · **基于内部信号的检测器必须配负控制并归一化：读轨迹演化而非静态快照**（来源：arXiv 2610.20319《Beyond Static Cues: Unified Dynamic Detection of MLLM Backdoors via Dual-Flow Trajectory Analysis》，2026-10-15 r590A 一手 arXiv API 200 逐串命中）
- **实证**：批评既有防御 `fundamentally constrained by a reliance on static snapshots and attack-specific heuristics`；方法 `shifting the diagnostic paradigm from static observations to dynamic output evolution`，双通道为 Attention Flow 与 Logits Flow，并 `normalize them against negative-control signatures so that natural perturbations are less likely to be mistaken for backdoor evidence`；优于 BYE / TCAP 等基线。
- **判据**：① **没有负控制的内部信号读数不可用**：自然扰动会被当成攻击证据 ⇒ 任何「读注意力/概率/内部状态」的检测器，评估时必须问归一化基准是什么。② **攻击类型未知时，静态快照 + 攻击特定启发式会被绕过** ⇒ 检测须覆盖多形态触发（文本注入 / 亚感知噪声 / 跨模态协同）。③ 审计面：扫描器自述「基于内部统计」不等于有效，须追问负控制与形态覆盖。
- **提升层**：工具（检测器评估）。
- **触发词**：EVO-Detect、负控制签名、轨迹演化 vs 静态快照、自然扰动误判、Attention Flow / Logits Flow、攻击类型未知。

## r591A · **开放网页检索 agent 的评测污染是独立污染面：评测期间取回 benchmark 内容即高估；轨迹构造管线必须可验证可复现**（来源：arXiv 2610.16998v1《Glasseek: A Transparent Recipe for Training and Trustworthy Evaluation of DeepSearch Agents》，2026-10-12）
- **实证**：开放网页 agent 在**评测期间从开放网页检索 benchmark 内容**造成污染、高估性能——首次系统性审计开放网页 agent 的测试集泄漏，发布可插入现有 harness 的模块化**反泄漏插件**；全透明深度搜索框架（数据/权重/训练配方/代码全释放）；可验证轨迹构造管线系统化生成高质量探索路径；CM-GSPO=搜索与摘要同策略、只优化执行子轨迹，实现跨**上下文压缩边界**的端到端搜索策略训练；严格协议下 9B agent 在几乎所有深度研究基准超前沿闭源 agent。
- **判据**：① 评测污染面清单必须含「开放网页检索回 benchmark 内容」——对策=反泄漏插件+受保护测试协议，不能只防训练集泄漏。② 轨迹构造管线不透明=训练数据不可审计=结论不可复现。③ 跨压缩边界训练揭示压缩造成的训练/推理错配——评训练数据时单列一项。
- **提升层**：工具（评测污染审计）/ 工作流（反泄漏协议）。
- **触发词**：Glasseek、测试集泄漏、开放网页污染、anti-leakage plugin、可验证轨迹构造、CM-GSPO。

## r591A · **注入探针评估必须配 matched negatives：会话位置/文本长度单独即可拿 0.91-0.98 AUROC，探针学到的是会话不是注入**（来源：arXiv 2610.18408v1《Prompt-Injection Probes Learn the Conversation, Not Just the Injection》，2026-10-13）
- **实证**：隐状态线性探针当廉价 IPI 监控器（筛工具输出、可疑送二查）；标准评测**不用模型就能过**——会话位置与文本长度单独达 **0.91-0.98 AUROC**；标准探针把多数无害案例（同会话无注入版/注入格式的无害文本）标错；把此类案例作为 **matched negatives** 加入训练后：无注入会话误报 **41-80%→4-27%**、无害相似样本误报 **92-98%→3-16%**；阈值设在正常流量上仍中位捕获 **95%** 曾骗过 agent 的攻击（不加此类数据为 91%）；新应用上误报保持低但检测依赖模型与阈值设定；同数据亦助益纯文本过滤器。
- **判据**：① 探针/监控器评测必须配 matched negatives（同会话无注入版+注入格式无害文本），否则位置/长度伪相关即刷出高 AUROC。② 捕获率须报「阈值设于正常流量」版本，不用默认阈值。③ 应用内/新应用分开报：泛化依赖模型与阈值。
- **提升层**：工具（监控器评估）。
- **触发词**：matched negatives、注入探针、伪相关、误报率、正常流量阈值、linear probe。

## r591A · **表观攻击成功须经 label-consistency 校验；抗输入扰动 ≠ 抗注入，两类鲁棒性分开报**（来源：arXiv 2610.19118v1《DecisionRobust: Benchmarking Robustness for JEV Style Decision Models Across Text and Vision》，2026-10-13）
- **实证**：类型化决策模型（JEV 式）跨文本/视觉鲁棒性基准；攻击含语义保持文本扰动、图像扰动、双模态提示注入；30 个文本配置/17 个视觉配置（含 24/12 个**候选选择排除的 held-out 模型**）；发现：① 攻击暴露超出构造/选型所用模型的漏洞（优化图像扰动跨目标迁移弱）；② 相对鲁棒性随任务与攻击类型变化——**抗输入扰动不蕴含抗提示注入**；③ **label-consistency 检查大幅压低测得攻击成功率** ⇒ 表观失败必须验证。
- **判据**：① 报 ASR 前先过 label-consistency 校验：表观攻击成功可能是标注/判定伪影。② 抗扰动与抗注入分项评测报数，禁合并成「鲁棒性」。③ held-out 模型仍被攻破 ⇒ 选型集内结论外推要保守。
- **提升层**：工具（鲁棒性评测）。
- **触发词**：DecisionRobust、类型化决策模型、label-consistency、表观失败校验、held-out 模型、扰动 vs 注入。

## r592B · **伪工具使用：只看结果正确会漏掉「按错误理由行动」——评测必须带工具必要性判据**（来源：arXiv 2609.16268《Spurious Tool Use: When RL Agents Learn the Wrong Reason to Act》）
- **实证**：在受控合成环境（事实问答 + 数学推理）中注入与特定工具强相关、但对工具必要性**因果无关**的线索；反事实评测（线索在、工具不必需）下，伪工具调用率最高升 **39%**。捷径**并非普遍形成**：只在 agent 已可靠学会使用该目标工具之后才出现 ⇒ **任务胜任度而非数据不平衡**是捷径学习的关键因素；换线索分析显示线索与工具的**语义对齐**会显著放大该效应。缓解手段是决策级稠密奖励——用 LLM judge 评估**每次工具调用的必要性**，在保持任务表现的同时抑制线索驱动的工具使用（arxiv.org/abs/2609.16268 HTTP 200 逐串命中）。
- **判据**：① 工具使用评测不能只看最终成功率 / 调用正确性，须加「**必要性**」判据（去掉该工具是否仍被需要）。② **反事实对照组**（线索在 / 工具不必需）是识别捷径行为的标准手段。③ 能力成熟度会改变失效形态——**越熟练越易走捷径**，评测结论须标注模型能力档与训练阶段。④ 与 oracle 完整性审计同族：都是「结果对但过程不可信」，须把过程判据与结果判据分开报（承 r586C oracle 五条不变量）。
- **提升层**：工作流（评测设计）/ 可复用 Skill（工具必要性判据）。
- **触发词**：伪工具使用、捷径、必要性、反事实评测、决策级奖励、语义对齐放大、过程不可信。

## r593B（arXiv · 2026-10-16 abs 200 逐串命中）

- **不确定性要先路由来源，再决定动作**（来源 arXiv 2609.32255 *Clarify the User or Verify the World? Uncertainty Routing for Proactive Agents*）。
  - **原文**：`Existing proactive approaches often specialize in either user clarification or environment verification, without explicitly determining the appropriate information source for each decision`；把动作不确定性拆为 `disagreement across plausible user-goal interpretations, which signals user-side ambiguity` 与 `the entropy remaining within each interpretation, which signals missing world-side evidence`，在 ACT / CLARIFY / VERIFY 三者间路由，查询生成器用 `a mode-conditioned information-gain reward` 训练。
  - **判据**：**「不确定」不是一个动作，而是要先判不确定来自用户意图分歧还是世界证据缺失**——前者该问人，后者该查环境；选错方向会把澄清当验证（反复问用户客观事实）或把验证当澄清（去环境里猜用户意图）。落地自检：触发澄清前先做一次「多个用户意图解释之间是否存在分歧」的判断，无分歧则走环境验证。
  - 提升层：模型 / 工作流。

## r594A（GitHub 八仓活跃 issue 面 · 一手命中 · 2026-10-16）

- **① 成本计量按「已完成步骤」而非「尝试」，子 agent 成本须单独归集且不污染主模型上下文**（来源 activepieces/activepieces #16576 一手命中）。
  - **实证**：此前一轮对话的 token 日志**只覆盖主聊天**，无法知道 task agent / deep research 花了多少。修复：① `ap_run_task` 与 `ap_deep_research` 结果携带 `tokens:{input,output}`，与 `billedToolCalls` 一样**排除在主模型可读内容之外**；② 任务在被截断后继续时 token **跨轮累计**（此前只保留最后一轮）；③ `runAgentTurn` 改为**按已完成步骤**计数而非按尝试（此前一条流在某步失败后，已跑步骤的 token 被整体丢弃）。
  - **判据**：**按"尝试"计量会在失败流上系统性低估成本**——失败恰好是最需要成本可见性的场景；按"已完成步骤"计量才能让失败也有账单。子 agent/深度检索的成本必须单独归集，且**归集内容不能回灌进主模型上下文**（否则既污染又放大）。落地自检：成本日志要能回答"这一轮里每个子任务各花了多少"，并单独验证"失败轮的成本不为 0"。
  - 提升层：工具（计量口径）/ 工作流（成本归因）。触发词：token 只记主聊天、失败轮成本为 0、子 agent 成本归集、按步骤计量。

## r594B（arXiv 五轨 · abs 200 逐串命中 · 2026-10-16）

- **① 基准的「真实」必须绑定到具体用例的 Task Flow，否则「更真实」无意义**（来源 arXiv 2610.09633 *Coding-Agent Benchmarks Should Match Their Users' Task Flows*）。
  - **原文**：采集 `4,782 agent sessions of real software engineers in JetBrains IDEs`；长会话（≥3 条用户消息，占 33%）与 issue 派生基准有两点不同：`(i) user requests span a far wider mix of task types` 与 `(ii) users switch between types throughout a session`；`Long-session samples from three public interaction corpora exhibit markedly different Task Flows (the distributions of session lengths, task types, and type-to-type transitions), so no single interaction distribution is universally realistic: benchmarks should name a target use case and calibrate to measurements from it`；SWE-TaskFlow 在 `preserves the verified tasks and tests` 前提下把交互导向目标 Task Flow。
  - **判据**：**"Task Flow = 会话长度分布 + 任务类型分布 + 类型间转移分布"三者共同定义真实性**；不同交互语料的这三个分布差异显著，所以不存在通用真实分布。落地自检：选用/自建基准时先写出目标用例并给出这三个分布的实测值；改造既有基准时保留已验证任务与测试，只改交互结构。
  - 提升层：工作流（基准选型）/ 可复用 Skill（评测设计）。触发词：Task Flow、type-to-type transition、基准校准到用例、SWE-TaskFlow。

- **② 多 agent 协议风险必须成对测 + 归因到后果：局部成功 ≠ 端到端影响**（来源 arXiv 2610.15529 *Agent-Canary-Mas: End-to-End Evaluation of Protocol Risk in Long-Horizon Multi-Agent Systems*）。
  - **原文**：`A locally successful protocol attack, however, may be rejected by a later agent or propagated into a consequential task decision. Measuring local exploitability alone leaves this difference unresolved and provides limited evidence about which participant caused the final outcome`；覆盖 `five risk classes and 13 subclasses across A2A, ANP, and BCS`，`975 matched malicious--benign task pairs in five business domains`；`Matched runs separate local protocol success from downstream consequences`；证据链 `participant selection, message consumption, tool activity, and task-state changes`；另有 protocol-context Guard `checks an object's authority at consequential handoffs`。
  - **判据**：**只测"某一步能不能被利用"既低估传播（后续 agent 采纳）也高估影响（后续 agent 拒绝），且无法归因到具体参与者**；必须用恶意-良性配对运行分离局部成功与下游后果，并保留完整证据链。落地自检：多 agent 评测至少报告三个数——局部协议成功率、下游后果发生率、可归因的参与者；在后果性交接点校验对象权限。
  - 提升层：工作流（多 agent 评测）/ 工具（权限校验点）。触发词：matched malicious-benign pairs、局部成功 vs 下游后果、协议风险归因、后果性交接。

## r594C（技能生态仓 issue 面 · 一手命中 · 2026-10-16）

- **① 并行评测必须隔离工作目录：并行度直接进入测量值**，判据是"换成无关变量测量值不应改变"（来源 anthropics/skills #1706 一手命中）。
  - **实证**：`skill-creator` 的 trigger-eval 把**所有 worker 的临时命令文件写进同一个目录**（`project_root/.claude/commands/{clean_name}.md`），并行 worker 互相看到彼此的文件；每个 `claude -p` 面对 N 个**仅 UUID 不同**的同名技能，只有选中自己那个才计为"触发"。于是**实测触发率塌缩到 ~1/num_workers，与被测 description 无关**；`--num-workers` 默认 10 ⇒ `run_loop.py` 实际是在对约 10% 缩放的噪声做优化。
  - **判据**：**并行评测的共享目录＝污染通道**；更一般地，任何"多 worker 共享可变工作区"的评测，其测得的量里混入了并行度。落地自检：并行 worker 一律给独立工作目录/命名空间；并用**无关变量替换试验**验证测量有效性——把被测项换成只影响身份不影响质量的变量（本例 UUID），若测量值随之改变，说明测的不是质量而是并行度。
  - 提升层：工作流（评测并行）/ 工具（评测隔离）。触发词：并行 worker 共享目录、触发率塌缩 1/N、num_workers 污染、无关变量替换试验。

## r595A（2026-10-16 · 来源 GitHub 技能生态仓 · wb-agent-evaluation 1.39.0）

1. **派生评审的强度不得继承调用方**（mattpocock/skills#1270）：`code-review` 派生 Standards/Spec 子 agent 时不指定模型与推理强度，于是"用便宜模型实现"这一优化把评审强度一起降级——**评审强度被实现成本反向决定**。**判据**：评审/把关类子任务的模型与 effort 须显式钉住，与被测对象的执行成本解耦。
2. **独立性以隔离上下文为判据，并须有完成回执**（mattpocock/skills#1268）：在实现者的既有上下文里"取一下评审指南、看一眼 diff"不能被报成一次独立评审；harness 缺少并行子 agent 机制或需显式授权时，必须给出明确的 blocked/not-reviewed。**判据**：独立评审 = 新鲜上下文 + 授权 + 完成回执三要素齐备，缺一即须报未评审，不得降级为"已审"。
3. **夹具的便利性裁剪会使覆盖声明失实**（mattpocock/skills#1269）：端到端测试重放生产真实调用参数，其中一个"必须是已存在目录路径"的 flag 因为造目录麻烦被删掉，而恰好有两个生产调用点把该 flag 与被测特性组合使用 → 覆盖率数字没变，实际覆盖面缩水。**判据**：重放型夹具删改输入须留痕并复核"被删参数是否参与被测组合"，否则覆盖声明即为虚报。

## r595B（2026-10-16 · 来源 arXiv · wb-agent-evaluation 1.40.0）

1. **读对 ≠ 做对：理解与决策必须分开诊断**（2610.18579）：System One 模型在 agent 循环中能把输入读对（理解正确）却在下一步决策上失败，整体准确率把两类错误混为一谈。**判据**：agent 评测至少拆成「读/理解」与「决策/行动」两层分别归因，否则提升理解的努力会被决策错误掩盖，反之亦然。
2. **可用性来自失败模式分解 + 置信信号，不是整体准确率**（2610.20417）：把 LLM 抽取的失败模式拆开、并给出可用置信信号后，系统从"不可用"变"可用"，而整体准确率数字并未显著变化。**判据**：评测报告须给失败模式分布与置信度可用性，单一准确率无法支撑"能不能上"的判断。
3. **统计保证在自适应对抗下有极限**（2610.18948）：对手会随评测方调整时，"用 N 次采样得到 p 的统计保证"不再成立。**判据**：评测结论须声明其保证类型与对手模型（固定 vs 自适应）；对自适应对手的通过率不得外推为部署后通过率。

判非：2610.16859 ANCHOR（仓库级约束层级与排序）与 ae 已落「全部约束 vs 单项 rubric 分开报」重叠 >60%；2610.19422 AgentSafeEvo（对抗共进化红队）与 ssc 已落 ASPIRE 开放域红队同族。

## r595C（2026-10-16 · 来源 GitHub 第二生态面 · wb-agent-evaluation 1.41.0）

1. **假成功要建成 known-answer 回归集，用例取自真实受阻场景**（browser-use/browser-use#6031）：把"已知答案却报成功"的场景（403 被拦、禁用点击、等 6 类）固化成回归集。**判据**：假成功不是偶发噪声而是可枚举的失败族；评审须维护一份"答案已知、必须判失败"的用例集，且用例来源是真实受阻环境而非人工构造的干净样例。

判非：langchain#41166（token 计量在 content 为 list 时漏算 tool call）、crewAI#8197（Bedrock/Gemini 用量未进 OTel span）与 ae 已落"计量口径"面（ap#16576）重叠 >60%；langchain#41254（merge_message_runs 把非法工具调用提升为合法）、#41149（XML 解析删掉合法元素）、#41185（白名单配置导致静默返回空）、#41259（裁剪后仍超预算）、crewAI#8204（配置声明的 callback 从未接线）分别落入本轮 av「合并/解析/静默空结果」与既有「注册成功≠消费方可选」面，重叠 >60%。

## r596C（2026-10-16 · 来源 arXiv + GitHub 生态仓实拉 · wb-agent-evaluation 1.42.0）

1. **能机械验证的就不要交给 LLM judge**（arXiv 2610.20573《Beyond LLM Judge: Mechanical Verification for Agentic Autoformalization》）：形式化任务上用机械验证器替代 LLM 评审，绕开 judge 的偏见与不可复现。既有 ae 1.34.1「judge 盲区」指出 LLM judge 的问题，本条给**替代路径与适用边界**。规则：评测设计先问「这一项能否机械判定」（编译通过/格式校验/约束求解/回放比对），能机械判定的项不得用 LLM 打分凑数；LLM judge 只保留给真正无机械判据的面，并必须声明评分不可复现的风险与置信区间。
2. **已授权动作被静默降级成交互表单＝验收失败，不是"更谨慎"**（anthropics/claude-code#101300）：owner 明确要求创建 PR，连接器却弹出表单让用户自己填，且没有任何「为什么不执行」的说明。与 ae「评审强度不继承调用方」（r595A）互补——那条管评审，本条管**执行侧的静默降级**。规则：验收要断言「授权动作产生了预期副作用」，而不是「系统没有报错」；任何把已授权动作降级为请求用户再确认的路径，都必须显式标注为降级并计入失败，否则"保守"会成为不执行的遮羞布。

判非（本轮核实）：arXiv 2610.20417（失败模式分解与置信信号）为 r595B 已落同族；arXiv 2610.20532（ActiveEvidence 证据图）与既有证据溯源条目重叠 >60%；browser-use#5057（工具调用评测 harness RFC）为提案无实证，登记待观察。

## r597（2026-10-16 · wb-agent-evaluation 1.43.0）

1. **无人值守循环要同时看比率指标与"重复重建"检测**（anthropics/claude-code#102565 + #97218）：模型每 30 分钟重装一个从未被要求的 Monitor，持续 17 小时，烧掉 2300 万缓存 token；另一份报告用约 30× 的 API-min/wall-min 比值发现长会话后台轮询异常并伴随质量退化。规则：评测与常驻自动化的资源账里必须有"单位墙钟时间的 API 时间"这类比率指标，并对"同一个对象被反复重建"设检测；只看总量会漏掉"没有进展但一直在烧"。
2. **终局成功率之外要有分维度轨迹画像**（arXiv 2610.04168 Agentic Cognitive Depth）：把 agentic 系统看成 Planning / Memory / Tools / Control Flow 四块 + LLM 的循环，定义五维画像——上下文敏感性 C、时间连续性 T、多模态协调 M、自适应交互 A、元认知监控 Mc；前四维分别量四类组件的跨轨迹使用质量，第五维量系统是否监控并调节整趟运行；每维给可操作代理指标 + 扰动程序。规则：只报一个 end-to-end 分数，无法知道是哪一维塌了；每个维度配自己的探针，不做加权总分。
3. **廉价代理基准要验证"结论一致"，不是"分数接近"**（arXiv 2610.20099 EvalBuilder）：把自动基准构建形式化为元评测——给 agent 一份昂贵的参考基准，让它造出低成本代理基准，然后按保真度（保持模型排序）、效率、鲁棒性（对 held-out 模型与新鲜采集响应的泛化、校准性与区分度）三维评估。规则：用代理基准替代昂贵基准之前，先证明它复现的是同一套排序结论与 calibration，而不是分数数字相近。
4. **"是否行动"要分离灵敏度与判据**（arXiv 2610.15415 FlipAct）：单一准确率分不出"没认出该行动"和"认出了但不敢动"。FlipAct 用 2×2 quad（固定所需知识、翻转状态）+ 分级证据分把 Yes/No 边界钉在 0，曲线斜率测灵敏度、半高处交叉点测判据；44 个开源模型的结果显示，模型对证据的**符号**而非幅度做出反应——"让状态没变好"的动作与真正有帮助的动作，被接受得一样频繁。规则：工具调用评测要分开测"能不能识别该动手"与"敢不敢动手"，并检查是否对证据强度敏感。
5. **过程稳定性单独评分**（arXiv 2610.19900 GraceBench）：现有基准主要看最终任务成功或少数里程碑，逐步行为不清；GraceBench 把移动端 App 的可达交互空间建为 UI 转换图（UTG），据此诊断是否偏离可行路径、是否进入循环、是否停滞、能否从不稳定的动作中恢复。规则：结果正确但轨迹不稳（多余动作、绕路、抖动）同样要扣分，因为这些会带来不可逆副作用与数据污染；给重复性流程先建一张可达状态图作诊断参照。

判非（本轮核实）：arXiv 2610.14346（LLM 作为客服技能的执行者）属基准论文无评测方法论增量；2610.12190（DataSense-Bench）、2610.05398（MMPostTrainBench）为特定域基准；2610.11482（本地模型 agent 可复现性研究）结论复用 icse 面既有判据。

## r598B（2026-10-16 · arXiv 八轨 450 条 · wb-agent-evaluation 1.44.0）

1. **模型/路径选型的评估口径是端到端成本，不是单价**（arXiv 2610.19316）：图工作流中把任务换到更便宜的提供方，往往要重新处理已累积的上下文；把依赖任务留在同一提供方才能复用上下文——路由决策与状态复用是耦合的。规则：比价时把"上下文重处理成本 + 依赖聚集收益"计入，只比每 token 单价会选出更贵的方案；同理，比较模型要按"完成一个任务"而非"一次调用"计。
2. **集合级奖励不能广播成个体信用**（arXiv 2610.20293）：一次生成多个检索动作、下游只给一个集合级奖励时，把奖励广播给每个动作是有效的梯度估计，却不能回答"哪个动作起作用"。规则：归因要另做干预（逐个/子集替换后重测），不能把集合分数除以个数当成个体贡献。
3. **重复支持不等于独立确认；审议协议要按实例的未决程度分配算力**（arXiv 2610.17869）：固定协议在推理前定死，无法把算力分给未解决实例，且会把同一来源的重复支持误当成相互独立的确认。规则：① 计"支持"时要按来源去重，独立源数 ≠ 表态数；② 多轮审议的轮数/参与方应由"本例是否已决"决定，不是常量。
4. **基准本身要先过可信度核查**（arXiv 2610.19447 / 2610.20221）：修 bug 基准存在测试样本出现在训练集的污染；把基准翻译成多语时又会丢失任务语义。规则：用任何基准前先查两件事——是否被训练数据污染、派生版本（翻译/改写/采样）是否保持了原任务语义；二者任一不成立，分数测的是别的东西。
5. **多 agent 评测必须包含"信息冲突"场景**（arXiv 2610.19128）：现有基准大多假设各方信息一致、协作无冲突，而真实协作里 peer 与子 agent 经常给出不一致信息。规则：多 agent 评测集要显式构造冲突/不一致输入，否则测到的是理想协作而非真实协作。
6. **成败可以在轨迹空间被早期预测，评估不必等到结束**（arXiv 2610.19614）：同一任务成功与失败的 rollout 在动作-观测嵌入空间里分离，简单的单任务判别器就能预测留出 rollout 的成败。规则：把"运行中预测"当评估与监控手段——轨迹一旦进入失败簇就早停或换策略，而不是跑完再统计。
7. **评价多 agent 系统要看分布尾部的持续行为者，平均态会掩盖**（arXiv 2610.19863）：社会科学的结论是持久的尾部行动者会不成比例地塑造集体动态，现有工作却只看代表性人格与平均表现。规则：多 agent 评测除了均值，必须报告尾部（最差/最持久偏离者）的行为与其对集体的影响。
8. **评估要验最终产出物，不是验交互文本**（arXiv 2610.20195）：社交类 agent 的评估多靠 LLM judge 给对话打分，却不检查最后形成的计划是否真的吻合各方约束。规则：凡"协商/讨论/多轮交互"类任务，判据落在产出的计划/文档/配置上；只评交互文本等于奖励谈得好而不是做得对。

判非（本轮核实）：2610.19345（小模型更绿）与既有模型路由/难度分档规则同面；2610.20572（教师可恢复性）属训练层；2610.19868（自弈任务须可分解可验证）与 av「模型产出须配可机械复算的接受条件」同族；2610.18157（扇出 vs 中继）为特定数据场景；2610.17751（集中/去中心自由度）并入 ag 规模化点；2610.19698 / 2610.16919 / 2610.16402 为特定域基准或特定工程域；2610.19167 / 2610.18745（功能正确之外的质量维度）与既有「测试通过≠满足规格」同面。

## r599A（2026-10-16 · GitHub mattpocock/skills#1280 一手 gh api 200 · wb-agent-evaluation 1.45.0）

1. **审问/评测类问题必须自包含，不得依赖会话早前捏造的实体名或未定义术语**（mattpocock/skills#1280）：grilling 实践七周里约 40 次「听不懂/请简化」，几乎每次问题都依赖会话前半段才出现的标签（agent 自己编的 "fund accumulator"）、早前消息里的发现、或受试者看不到的文档。规则：评测/审问/红队提问要可独立作答——实体、术语、上下文都须内含在题目里或明确可取得；凡需要「记得上半场说了什么」才能答的题，结果不可复现且测的是记忆而非能力。提升层：可复用 Skill（评测问题设计）。触发词：评测问题自包含、会话内捏造命名、不可复现提问、grilling 可答性。

判非（本轮核实）：mattpocock#1283（决策地图新会话可发现）与 compressor「入口发现/渐进披露」重叠 >60%；其余 ae 相关近期为基准/训练层，无方法增量。

## r601A · 自纠错收益必须按「挽回/破坏」两率分开报：聚合准确率掩盖破坏面，内部事后信号做门不总优于无条件策略（来源：arxiv.org/abs/2609.35832《When Should LLMs Trust Their Own Revisions? A Risk-Aware Study of Intrinsic Self-Correction》abs 一手，2026-10-16 实拉逐串命中 `improves by 25.5 percentage points on GSM8K` / `refinement changes 19.1% of initially correct answers into wrong ones` / `Aggregate accuracy can conceal substantially different revision behavior`）
- **判据**：① 报自纠错收益必须同时给「正确→错误」破坏率——29 模型上 GSM8K +25.5pp 与 19.1% 破坏并存，只报净增益等于把伤害藏进统计量；② 修订的接受判据不能只挂模型内部事后信号（原文：不总优于无条件策略），要挂外部可得证据；③ 与 §修订哈希/候选面 分工：那条管改动的可追溯，本条管「这次修订该不该被接受」的计量口径。提升层：模型/工作流（自纠错评估）。触发词：修订破坏率、挽回数与破坏数、聚合准确率掩盖、自纠错门控、内部事后信号。

## r601A · 评分标准本身要过对抗验收：同模型写 gaming 答案骗不过 rubric 才算修好（来源：arxiv.org/abs/2610.21040《Recursive Reward Improvement via Adversarial Meta-Prompt Evolution》abs 一手，2026-10-16 实拉逐串命中 `reward-hacking adversary` / `two answers` / `HealthBench +10.9/+12.4` / `no external model +10.3` / `unseen tasks +6.6/+8.0`；B 级——修复步数少、adversary 与 scoring 同模型有共谋风险，先登记后验证）
- **判据**：① evaluator 外置红线的补件=rubric 自己也要被攻一遍——用同模型生成「该得高分但不实质」的答案撞评分标准，撞得过就修；② 「solver 点名预期话题而无实质内容」是典型 exploit 形态，固定 rubric 会被它刷分；③ 可无外部模型自跑（同模型既当 adversary 又当 solver）降低采用门槛，但同源共谋风险要在报告里声明。提升层：工作流（评测攻防）。触发词：rubric 对抗验收、reward-hacking adversary、评分标准攻防闭环、点名话题无实质、RRI。

## r602A · 触发评测 harness 的平台假设与探针隔离：静默损坏比报错更坏（来源：github.com/anthropics/skills#1692（2026-10-06）「Trigger-eval harness silently broken on Windows: select() on pipes, probe files leak into glob」一手）

- **判据**：① 评测 harness 的平台可移植性是一等验收项——同一 harness 在另一 OS 静默降级（select() 对管道在 Windows 语义不同）比直接报错更坏，因为它产出看似有效的数字；② 探针/夹具文件不得进被测 glob——泄漏进 glob 会污染触发率的分子分母；③ 与 r594C（并行评测共享目录使并行度进入测量值）分工：那条管并行污染，本条管平台假设+文件泄漏；④ 验收：harness 至少两个 OS 各跑一次冒烟，断言探针文件不出现在被测集合。提升层：可复用 Skill（评测卫生）。触发词：harness 平台假设、select() on pipes、探针文件泄漏 glob、Windows 静默损坏、触发率污染。

## r602B · 交互应用评审以交互为判据：代码分析+单测的 judge 看不到用户一眼可见的失败（来源：arXiv 2610.17895《Interaction-as-a-Judge》一手 abstract：current automated LLM evaluations primarily focus on code analysis and unit tests；this mismatch can cause LLM judges to miss failures that are immediately apparent to human users；computer-use agents directly interact with an application；6,858 preference pairs + 222 human-verified requirement labels；2026-10-16 实拉）

- **判据**：① 网站/桌面应用/游戏类交互产物的验收，人类靠交互判断，而代码分析+单测型 judge 与这个判断方式错位——用户一眼可见的失败（布局塌了/按钮没反应/流程走不通）在静态评审里全不可见；② 交互即裁判（Interaction-as-a-Judge）：用 computer-use agent 直接操作应用，把「用户会做什么」变成评测动作序列；③ 数据形态：人类偏好对 + 人工核验的需求标签两套互补——前者训/评偏好，后者验收需求满足；④ 与 §HTML 报告离线自包含 分工：那条管产物静态属性，本条管动态交互属性的评审通道。提升层：可复用 Skill（评测范式）。触发词：Interaction-as-a-Judge、交互应用评审、CUA 评测、用户一眼可见失败、偏好对+需求标签。

## r602B · 基准的用户中心审计：贡献者≠被代表者，七维扫「谁的规定」（来源：arXiv 2610.19268《Whose Data, Whose Benchmark? A User-Centric Framework for Auditing Evaluation Resources》一手 abstract：distinguishes users who contribute benchmark content from those whose needs evaluation results are intended to represent；seven dimensions across benchmark content, metadata, documentation, and scoring procedures；American-centered conventions 62.4-94.x% across 16 resources；2026-10-16 实拉）

- **判据**：① 基准分数会掩盖「谁的规定定义了成功」——贡献基准内容的用户与结果要代表的用户是两类人，错位时分数对后者不可解释；② 七维审计面：基准内容 / 元数据 / 文档 / 评分程序——每一维都问「这里体现的是谁的习惯与判断」；③ 实证锚：16 个资源里美国中心惯例占 62.4-94.x%——拿跨域基准分数直接外推到自己用户群是系统性误读；④ 与 §基准须绑定 Task Flow 三分布 分工：那条管任务分布绑定，本条管「分布里谁的规定」。提升层：可复用 Skill（基准审计）。触发词：基准用户中心审计、贡献者vs被代表者、七维、谁的规定、美国中心惯例。

## r603B · 自动技能优化会显著放大产物体量：增益必须按体量归一后才准入（来源：https://export.arxiv.org/abs/2610.19951（AtomSearch，2026-10-14 投稿，2026-10-16 abstract 一手）逐串命中 `SkillOpt's final skills contain 2.3-19.7 times as many characters`）
- **实证**：AtomSearch 论文的对照技能优化法（SkillOpt）在提升任务表现的同时，把最终技能文本放到最多约 20 倍体量——而技能正文是要进上下文的（同域预算：Tier1 ~50-100 tokens/skill、Tier2 <5000 tokens）。
- **判据**：① 技能自演化/自动改写产物的验收式 = **增益 ÷ 产物体量（或每次调用的上下文成本）相对 No-Skill 基线**，禁止只报绝对分数；② 产物超基线一定倍数即须给出压缩或拆分证据，否则「优化」实为把成本转嫁给上下文预算；③ 与 §相对 No-Skill 基线的增益、§技能增益预测 分工：那两条管增益怎么算，本条管增益要除以什么算（体量维度）；④ 验收：同一优化前后的技能并列报「任务增益 + 正文字数/估算 token + 增益每千 token」。提升层：工作流（评测/准入口径）。触发词：体量归一、增益除以体量、2.3-19.7 倍、技能膨胀、上下文成本入账、AtomSearch。

## r603B · 长程发现的停滞来自历史累积锚定：周期性全量丢弃搜索状态、从当前最优重启（来源：https://export.arxiv.org/api/query cat:cs.CL 2610.20563《Scaling Discovery Requires Forgetting》2026-10-16 一手 abstract：single-agent long iteration, parallel multi-agent, and inter-agent communication all stall as history accumulates—agents anchor on past attempts and edits shrink；periodically discarding all search state and restarting from the current best candidate improves over parallel agents by up to 15% and over single agents by up to 39% across heuristic programming, kernel optimization, and model training）
- **判据**：① 长程搜索/迭代的失效模式不是随机退化而是**锚定+编辑收缩**——历史累积让后续尝试围绕过去打转、改动越来越小，加算力（并行/通信）只放大同一失效；② 解法是周期性「全量丢弃搜索状态 + 从当前最优候选重启」——保留最优解、丢掉路径依赖；③ 对自改进循环的含义：迭代上限（Cap14）之外还须有状态重置位，只设上限会把死循环变成「放弃」的同族失效；④ 验收：长程任务记录「每轮编辑幅度」曲线，收缩到阈值以下即触发重置；重置后断言从中断前最优继续而非从零。提升层：工作流（自改进循环设计）。触发词：历史锚定、编辑收缩、遗忘重启、搜索停滞、discard and restart、当前最优重启。

## r604A · 用量计量必须消费尾随 metadata 事件：在结束事件处提前退出会把真实用量记成 0（来源：api.github.com/repos/crewAIInc/crewAI/issues/8225，2026-10-16 gh api 一手正文 `usage arrives in a metadata event after messageStop ... reports 0 tokens`）
- **实证**：Bedrock Converse 流把 token 用量放在 `messageStop` **之后**的 `metadata` 事件里；crewAI 的 `BedrockCompletion` 有两个出口在该事件之前就离开流循环（异步侧在每个 `messageStop` 就 break，同步侧只在 `content_filtered` 时 break；带 `response_model` 时两侧都在结构化输出工具块的 `contentBlockStop` 处发完成事件并返回），于是 `get_token_usage_summary()` 报 0、`LLMCallCompletedEvent.usage` 为 None。
- **判据**：① **计量的终点是「用量事件到达」，不是「生成结束事件到达」**——两者顺序由提供方决定，不能假设同时；② 每个提前返回路径都要问「它跳过了哪些计量/留痕」，尤其带结构化输出时的专用出口；③ 与 §成本按已完成步骤计量 分工：那条管计量的粒度口径，本条管计量信号的读取时机；④ 验收：对流式调用断言用量非 0，且与同请求非流式调用一致。提升层：工具（计量正确性）/ 工作流（评测数据可信）。触发词：尾随 metadata、messageStop 后用量、用量记 0、提前 break、结构化输出专用出口。

## r604B · 有状态 agent 的评估须「证据有界」：结论只能由可引用的证据支撑（来源：https://export.arxiv.org/abs/2610.21177《AgentEval: Evidence-Bounded Assessment of Stateful Agents》2026-10-15，2026-10-16 arXiv API 一手摘要；**摘要级 B**）
- **实证**：AgentEval 针对有状态 agent 提出证据有界的评估方法。
- **判据**：① 对有状态对象的评估，每条结论须绑定**可引用的证据片段**（哪次状态转移、哪个观测），无证据的结论不得进入评分；② 与已落「证据视图」「abstention 三态」分工：那两条给了证据呈现与弃权，本条要求**评分项本身**有证据下界；③ 验收：评估报告每个扣分项都能点回具体证据，点不回的自动降为未评价。提升层：工作流（评测证据）/ 工具（评分可追溯）。触发词：证据有界评估、有状态 agent 评测、结论绑定证据、AgentEval。

## r604B · 记忆评估不能只用下游 QA：答对问题不等于记忆机制正确（来源：https://export.arxiv.org/abs/2610.22209《Beyond Downstream QA: Rethinking How We Evaluate Agent Memory》2026-10-15，2026-10-16 arXiv API 一手摘要；**摘要级 B**）
- **实证**：论文主张重新思考 agent 记忆的评估方式，超越下游问答这一单一口径。
- **判据**：① 下游指标是**间接指标**：它同时被检索、推理、生成能力影响，不能反推记忆机制好坏；② 记忆能力须分层测：写入正确性 / 保留与更新 / 检索命中 / 冲突消解 / 遗忘合规，各层单独给分；③ 与已落「记住 vs 弃权」「证据变更后记忆修复」分工：那两条给了具体记忆行为，本条给**评测分层**；④ 验收：一次记忆能力评测至少输出写入/检索/更新/冲突四层分，而非单一 QA 准确率。提升层：工作流（评测分层）/ 可复用 Skill（记忆评估）。触发词：记忆评估分层、下游 QA 不足、记忆机制评测、写入检索更新冲突。

## r604B · 一致性须定位到动作级差异：任务级总分看不出哪里不一致（来源：https://export.arxiv.org/abs/2610.22031《GraphACM: Graph-based Action Consistency Measurement》2026-10-15，2026-10-16 arXiv API 一手摘要；**摘要级 B**）
- **实证**：重复执行的行为一致性是评估 LLM agent 可靠性的有效信号；但现有方法通常给出单一任务级分数，不指出行为差异发生在哪、动作是否在同一口径下比较。
- **判据**：① 可靠性评测要输出**动作级差异图**（哪一步分叉、分叉后是否再合流），任务级一致率无法指导修复；② 比较动作前须先**对齐比较口径**（参数归一、顺序无关、副作用等价），否则不一致是测量误差；③ 与已落「失败模式分解+置信信号」分工：那条管失败分类，本条管一致性差异的定位与口径对齐；④ 验收：一致性报告给出首个分叉步骤与分叉类型。提升层：工作流（可靠性测量）/ 工具（差异定位）。触发词：动作级一致性、GraphACM、分叉定位、比较口径对齐、任务级总分不足。

## r604B · 基准任务须含歧义澄清与未声明约束：规格完备下的执行不等于真实交付能力（来源：https://export.arxiv.org/abs/2610.22350《FDE-Gym: The Last Mile of AI Delivery》2026-10-15，2026-10-16 arXiv API 一手摘要；**摘要级 B**）
- **实证**：现有 agent 基准通常用 issue 报告、规格或工单把任务定义得很清楚；真实客户交付不同：前置部署工程师必须澄清歧义需求、在活系统里工作、并挖出未声明的约束。
- **判据**：① 基准若把需求写完备，测的是**执行**而非**交付**；评测设计要显式包含「需求含歧义」「存在未声明约束」两类任务；② 澄清行为（提问时机、提问质量、假设记录）应进入评分，而不是被当成多余轮次扣分；③ 与已落「基准须绑定 Task Flow 三分布」分工：那条管分布绑定，本条管任务定义的完备度维度；④ 验收：评测集中至少一类任务在初始描述里故意缺失关键约束。提升层：工作流（评测任务设计）/ 可复用 Skill（交付能力）。触发词：FDE-Gym、歧义需求、未声明约束、交付 vs 执行、澄清行为计分。

## r604B · 输入质量决定 agent 成本：预算须按输入健康度预估而非按任务名义规模（来源：https://export.arxiv.org/abs/2610.21914《CodeHealth Predicts the Token Cost of Agentic Code Review: A Pre-Registered Study of 465 Agent-Authored Pull Requests》2026-10-15，2026-10-16 arXiv API 一手摘要；预注册研究，**摘要级 B**）
- **实证**：组织日益把代码评审委托给按 token 计费的多 agent LLM 流水线；低代码质量抬高人工维护成本，但其对 agent 评审成本的影响此前未被测量。研究检验基线 CodeHealth 是否能预测 agent 评审的 token 成本。
- **判据**：① **成本模型的自变量要含输入质量**：同样「审一个 PR」，输入健康度不同，实际 token 成本可成倍变化；② 预算制定要先测输入指标再做估算，且估算须可回算（预注册口径）；③ 与已落「成本按已完成步骤计量」分工：那条管计量粒度，本条管**预估自变量**；④ 验收：给出成本估算时同时给出所依据的输入质量指标值。提升层：工作流（成本治理）/ 工具（预算预估）。触发词：CodeHealth 预测成本、输入质量自变量、评审 token 成本、预注册口径、预算回算。

## r604C · 分数须由判据计数推导，分母随「适用判据集合」变化；模型自报总分只能作无判据时的 fallback（来源：Qoder r644-Q-B 转来 NVIDIA/SkillEvaluator 今日 main 合入 PR #190/#196，`docs/tier3-live-evaluation.mdx` 一手 44,585B：`Accuracy is calculated from the judge's criterion verdicts, not its numeric total: passing applicable criteria divided by applicable criteria`）
- **实证**：SkillEvaluator 规定准确率按**判据裁决**计算而非模型给的数值总分：通过的适用判据 ÷ 适用判据；负例或无 `expected_skill` 时把 `SKILL_IDENTIFIED` 从分子分母**同时剔除**（分母变 4 而非 5），并落盘 `excluded_criteria` 与 `applicable-accuracy-criteria/v1` 策略串；宿主机与校验器共用完全相同的计分代码。
- **判据**：① 任何 LLM-judge 打分链路应以**判据布尔/计数**为唯一分数来源；② 显式记录「本案例适用判据集合」与剔除项，否则不同案例的分数不可比；③ 模型给的数值总分只允许在无判据时作 fallback，且**可被校验器拒收**；④ 与已落「importance-weighted mean」不同轴（那是加权均值，仍取模型分）；⑤ 验收：评分代码不引用模型返回的数值总分，且每次评分输出适用判据清单。提升层：工作流（评测计分构造）/ 工具（可复算分数）。触发词：判据计数推导分数、适用判据集合、excluded_criteria、模型自报总分 fallback、host 与 verifier 同码。

## r604C · 成对比较两侧若由不同判者打分，该案例须剔除并单独计数（来源：同上 tier3-live-evaluation.mdx 一手：`When the two conditions of a case were judged by different models, the case is left out of that judge's skill lift and counted in judge_mixed_cases in lift.json`）
- **实证**：SkillEvaluator 对「有/无技能」成对试验规定：两侧由不同模型评审时，该案例从该判者的技能增益中剔除，并计入 `judge_mixed_cases`；逐判记录 `judge_model_used` / `judge_reasoning_effort` / `judge_fallback_used`；并规定「判者仍然失败是评测基建失败，不是 0.0 分，受影响的一侧不发布分数」。
- **判据**：① 成对试验的**同判者性**是增益有效性的前提，判者降级/重试不得静默继续计分；② 必须落「混判」计数与「评测基建失败」终态——**不是 0 分、也不是跳过不提**；③ 与已落「P2Patch 异源证据」方向相反（那条要异源，本条禁配对两侧异源），勿混用；④ 验收：lift.json 中 judge_mixed_cases 可统计，且失败判者对应侧无分数发布。提升层：工作流（评测有效性）/ 工具（判者一致性）。触发词：同判者性、judge_mixed_cases、判者降级不得静默计分、评测基建失败非 0 分。

## r604C · 指定资源不可用时默认方向是「降级执行」而非「放行」，且降级事件本身可观测（来源：Qoder r644-Q-C 转来 api.github.com/repos/anthropics/claude-code/releases/tag/v2.1.300 一手：`an unavailable model falls back to the caller's instead of allowing the action`；v2.1.301 另有「compacted over and over, on a model you didn't pick, behind an LLM gateway whose responses name a different model than the one requested」）
- **实证**：claude-code v2.1.300 修掉 agent hook 忽略其 `model` 声明的问题，并规定**模型不可用时不放行该动作**，而是回退到调用方的模型；v2.1.301 暴露另一类：网关返回里自报的模型名与请求的不同，压缩被反复执行到用户未选的模型上。
- **判据**：① 凡「指定资源（模型/判者/评测器/容器）不可用」的分支，安全默认=换成**低权限但仍在授权内**的替代并记录，而不是因为拿不到判决就放行；② **执行者身份的自报不可信**（网关自报模型名），须以外部 revision/标识核；③ 与 r604C「评测器 digest 钉住」互补：那条钉身份，本条钉不可用时怎么退；④ 验收：模拟判者/模型不可用，断言动作被降级执行并留下降级事件，而非放行。提升层：工作流（安全默认）/ 工具（身份核验）。触发词：不可用即降级不放行、fail-degrade、网关自报模型不可信、hook model 被忽略。
