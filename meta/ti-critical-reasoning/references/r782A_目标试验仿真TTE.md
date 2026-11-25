## 二十一、目标试验仿真：先写 RCT 协议再让观察数据就位，设计缺陷比统计更致命（TI · r782A 2026-11-20 实拉，≥3 独立域交叉）

> 与 §13–20 分工：那些是「给定研究设计后如何识别/估计」（图识别/IV/DiD/RDD）；本节是**上一步**——在碰数据前把因果问题写成一份假说 RCT 协议，再逐条映射到观察数据。Hernán & Robins 2016 框架。

### 21.1（r782A-1）★七组件协议先写、因果问题定义试验而非数据定义分析；设计缺陷比统计失配更常致错
目标试验协议七组件（Hernán–Robins 2016，NAP 委员会 Table 2-1 逐字）：eligibility criteria（入排标准**全部基于基线时点已确定的特征**，禁事后用基线后信息定义基线资格）、treatment strategies（含初始治疗及停药/换药的方案许可理由）、treatment assignment（基线随机、可按预后因子分层）、start/end of follow-up（基线开始、死亡/结局/失访/行政截尾止）、outcomes（尽量含 negative controls 即已知不受该治疗影响的结局）、causal contrasts（ITT：被分配到策略的效应 vs per-protocol：按方案实际接受的效应）、statistical analysis（预先写明如何调整基线与随访中的预后/依从/失访因素）。关键ORDER：the causal question defines the trial; the trial defines the analysis; the data are made to fit the analysis — not the other way around。scoping review（Zuo 等，96 项研究）：94% 观察性 CER 至少一项设计缺陷，61% 用基线后信息定义基线资格、81% 未声明 ITT 还是 per-protocol；Hernán 强调**协议组件与随机分配的不完整仿效（设计面）比统计调整不足更可能导致错误推断**。判据：报观察性因果结论前先亮七组件表，缺任一格即声明该格是假设不是数据结论；「用了 IPW/PS 匹配等高级统计」不构成 TTE 合格。

### 21.2（r782A-2）★永生时间偏倚是 time-zero 未对齐的产物，不是样本量或模型问题
机制（crvscience 逐字）：用**未来的治疗状态**定义暴露、却把随访起点放在更早的临床事件（确诊/入院）——因为「晚开始用药者必须活到开药那天」，把这段治疗前生存窗口记到治疗组头上，artificially inflating survival benefits。目标试验通过强制对齐消除：每个人**恰在满足资格并被分入策略的那一刻**开始随访（time zero = eligibility met = assignment = follow-up start）。更一般的 three biases：immortal time / prevalent-user / misaligned-follow-up selection bias。扩展：资格可反复满足（多次门诊）→ sequential nested target trials（每个合格月/就诊各起一个嵌套试验、robust variance 处理同一人跨重叠试验相关）；策略含宽限期（如「3 个月内启动他汀」）→ time-zero 分配未知。判据：看到「治疗组生存更好」先核 time-zero 是否与资格/分配同一时刻；错起点下再高级的 Cox/加权也修不回。

### 21.3（r782A-3）★clone-censor-weight 是宽限期策略的仿效主力，克隆消偏倚、IPCW 补信息性删失
宽限期策略在 time-zero 无法知道分配 → 克隆：每个合格者在基线**复制到每个策略各一份**（Di={(i,a=1),(i,a=0)}），两臂都从 time-zero 起贡献人时（neutralizes immortal time bias）；当某人实际轨迹偏离所分配策略时对该 clone **人工删失**；再用 inverse probability of censoring weights（IPCW，以时变混杂为条件估计「仍依从未删失」概率的倒数）校正人工删失带来的选择偏倚，得无偏 per-protocol 生存曲线。边界（crvscience 逐字）：TTE **does not replace randomization**，因果有效性仍落在不可检验的 no unmeasured confounding（条件可交换性）+ positivity 上；价值在消除 self-inflicted design flaws（已多次调和观察研究与 RCT 的分歧：激素替代/他汀/COVID 疗法）。判据：报 per-protocol 效应须写清克隆臂、人工删失触发点、IPCW 是否施加及 positivity 是否成立；「无条件可交换性/无阳性」声明只写「用了 IPW」不合格。

### r782A 来源与判非（2026-11-20 实拉，逐字核验）
- `https://nap.edu/read/25532/chapter/4` → 重定向 `nap.nationalacademies.org` 再转 `www.nationalacademies.org`（**WebFetch 两次重定向放弃逐字抓、以 WebFetch 首跳返回全文片段逐字登记，不冒充完成 WebFetch**）：NAP 委员会 Table 2-1 七组件及逐字描述（「all inclusion and exclusion criteria are based on characteristics ascertained exclusively at baseline」、negative controls、ITT vs per-protocol、protocol/analysis follow from explicit causal question、emulation 是 iterative process）——第一独立域·政府/学术机构原文。
- `https://www.sciencedirect.com/science/article/abs/pii/S0895435623002032`（Zuo 等 TTE scoping review，WebFetch 摘要全文逐字：96 studies / 94% 至少一设计缺陷 / 61% 基线后信息 / 81% 未定义因果对比 / time-zero 防 immortal time bias / statistical methods only a part of TTE design / Hernán 强调设计缺陷更易致错）——第二独立域·同行评议综述。
- `https://crvscience.com/wiki/target-trial-emulation`（WebFetch 200 全文逐字：两阶段、七组件表、immortal time bias 机制、time-zero 对齐、sequential nested trials、clone-censor-weight 公式与 IPCW、does not replace randomization + 条件可交换性与 positivity 边界、Hernán-Robins 2016/JAMA 2022 著录）——第三独立域·方法学 wiki。
- `https://metricgate.com/blogs/target-trial-emulation-observational`（WebSearch 逐字快照：七组件、time zero is sacred、clone-censor-weight recipe 与 IPW vs Matching 交叉）——第四独立域·工程教学。
- `https://www.sciencedirect.com/science/article/abs/pii/S0003496724013220`（RA CER 系统综述 WebSearch 摘要逐字：31 研究 29(94%) 设计缺陷、七组件映射）——交叉佐证。
- **判重**：全库 SKILL.md 精确扫描 `target trial`/`目标试验`/`immortal time`/`clone-censor` 0 命中（`emulat` 命中为 personal-ai-employees 的 K8s emulation version 与 browser-skill 的设备模拟，异命题）；`propensity score`/`倾向得分` 全库 0（r778A 判重行登记）。AIPW/DR 与 `meta/agent-evolution` §off-policy（IPS/SNIPS/Doubly Robust）有重叠按 rules/07 弃用、改取「先写 RCT 协议」这一更上游且正交的子面。豆包自留地 WB 0 落地。
