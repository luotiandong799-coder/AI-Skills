

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
