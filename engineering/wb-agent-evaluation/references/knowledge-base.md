

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
