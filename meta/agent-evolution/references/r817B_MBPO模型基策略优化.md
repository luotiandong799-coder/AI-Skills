# r817B · MBPO 模型基策略优化：用短分支 rollout 解耦模型视界与任务视界

> AI · 2026-11-28 独立实拉 · ≥2 独立域一手交叉（arXiv:1906.08253 MBPO 原文 HTML 全文 + arXiv:2510.01457v4 2025 取证分析全文；WebFetch 200 逐字）· 3 独点。Dyna 骨架（Sutton 1991）：学世界模型 → 在模型中想象转移 → 用想象数据加速策略训练；MBPO = bootstrap 概率集成 + 从真实 replay 状态出发的短 rollout + SAC 作策略学习器。

## 判重与定位
- 全库 `SKILL.md`+`module-memory`+`co-learn` 对 `model-based RL`/`MBPO`/`Dyna`/`world model` 0 机制专节：仅 §r801C SAC 一句「twin Q（同 TD3）」、§r795K JWT 无关的 "world of online experiments" 字串、§23 安全探索「learned model 上做 reachability」（异命题——那条管安全规格，这条管样本效率）。豆包自留地 WB 0 落地 ⇒ 按 rules/07「增＝加厚现有」0 新建。
- 分工：§r801C SAC 管「在线 off-policy + 熵目标」、§r815B CQL 管「离线零交互防 OOD 高估」、§r808B DPO 管偏好对；本章管**有模型可学、但模型会错时，怎么把模型用到收益最大且不崩**。

## 独点1 · 单调改进界与两类误差（原文 §4.1 Theorem 4.1 逐字）
- 目标形式 `η[π] ≥ η̂[π] − C`：只要模型下改进超过误差项 C，真 MDP 上即保证改进。Theorem 4.1 用每步期望 TV 距离上界 ε_m 与策略散度上界 ε_π 给出 `C(ε_m,ε_π)=2γr_max(ε_m+2ε_π)/(1−γ)² + 4r_max ε_π/(1−γ)`。
- 两类误差：①**泛化误差**（采样造成，ε_m = max_t E_{s~π_{D,t}}[D_TV(p‖p_θ)]，实践中用模型在数据采集策略 π_D 时变状态分布上的验证损失估计）；②**分布偏移**（策略更新后遇到模型没见过的状态，ε_π = max_s D_TV(π‖π_D)，实践中测策略 KL 再用 Pinsker 不等式转 ε_π）。
- 理论界的两处悲观（§4.2）：可能根本不存在 `η̂[π]−η[π]>C` 的策略⇒无改进保证；分析假设**全程模型 rollout**使误差复合，界里出现随有效视界 `1/(1−γ)` 二次放大的因子。⇒ 结论不是「用模型」，而是「模型不准时少用模型、多用真实数据」。
- §4.3 实证修正：模型误差随 π 与 π_D 的偏离增大，但**数据越多、对附近分布泛化越好**；用线性近似 `ε̂_{m'}(ε_π) ≈ ε_m + ε_π·(dε_{m'}/dε_π)`（斜率从图 1 经验估计），即可得到「合理到足以支持使用截断 rollout」的折衷。Theorem 4.3 给出 k-branched rollout 界，其中 `k* = argmin[γ^{k+1}ε_π/(1−γ)² + γ^k ε_π/(1−γ) + k ε_{m'}/(1−γ)] > 0` 当 ε_{m'} 足够小——**最优模型视界不是 0，也不是任务长度，而是一个正的短值**。

## 独点2 · 核心机制：短分支 rollout 解耦视界 + 概率集成（原文 §4.2/§5）
- branched rollout 逐字：从**上一策略状态分布** `d_{π_D}(s)` 的一个状态出发，在学到的模型 p_θ 下按当前策略 π 跑 k 步；Dyna 可视为 k=1 的特例。实践中「用大量从 replay buffer 状态出发的短 rollout，替换少量从初始状态分布出发的长 rollout」。
- 解耦视界（§1/§5 逐字）：「we disentangle the task horizon and model horizon by querying the model only for short rollouts」；从初始分布长 rollout 把**模型长度绑死任务长度**，误差复合使别人只能评截断版基准；分支策略解除这一限制，故 MBPO 能扩到「让其他模型基方法彻底失败」的长视界任务。
- 概率集成（§5）：bootstrap ensemble `{p_θ^1,...,p_θ^B}`，每个成员输出对角协方差高斯 `N(μ_θ^i, Σ_θ^i)`；单个概率模型捕获**偶然不确定性**（输出噪声），bootstrap 捕获**认知不确定性**（参数不确定性，数据稀缺区最易被策略利用）；生成预测时随机均匀选一个模型，**同一条 rollout 的不同步可由不同动力学模型采样**。
- 实用算法（Algorithm 2）：真实环境采样入 D_env → MLE 训模型 → 每步从 D_env 均匀采 s_t → k 步模型 rollout 入 D_model → 在 D_model 上做 G 次策略梯度（每环境样本 20–40 次更新，模型数据降低过拟合风险）。G 比 model-free 高得多，但**没有模型数据的「高 G SAC」对照仍追不上**——收益确来自模型。
- 原文性能声明：Ant 任务 30 万步 MBPO ≈ SAC 300 万步；部分任务比 model-free 快一个数量级；模型回报倾向**低估**真实回报，短 rollout 下策略「may not exploit the model at all」。

## 独点3 · rollout 长度的实证边界与 2025 反例（不把「样本效率」写成普适）
- 原文 §6.2：Hopper 最佳调度 k 从 1 线性升到 15，但**固定 k=1 保留大部分收益**；200 步也够准但用于策略优化比短值差，500 步「too inaccurate for effective learning」；MVE/STEVE 式「只改目标值」与「模型数据增强」原则上互补，但初步实验未给 MBPO 带来改进。
- 2025 取证分析（arXiv:2510.01457v4）给出**两个耦合失效**，说明「短 rollout + 集成」不是充分条件：
  - **目标尺度错配**：MBPO 把下一状态与奖励拼成多分量目标联合回归，**输入做 running normalization、输出不做**；DMC 奖励有界 0–1 却仍被预测到近 0，合成转移主导 critic batch 后把 Q 拖向严重低估（量级达 −10^8）。因果链逐字：「improper target scaling → reward model bias → critic underestimation → policy failure」。
  - **残差预测**：学 `s′−s` 而非 `s′` 在慢变状态是强归纳偏置，但在不稳定区放大误差指数复合、抬高集成方差；「despite seemingly low one-step model error」合成反事实已不可靠。
  - **FTFL 两处修复且缺一不可**：①对 next state 与 reward **分别**做 running mean–variance 目标归一化（并反归一化输出）；②用绝对下一状态预测替代残差。单独归一化仅小幅改善、单独直接预测仍近随机；合起来在 7 个此前失败的 DMC 任务中 5 个超过 SAC、Gym 六个任务不掉。hopper-hop/hopper-stand 仍未修复——不连续接触力通道不能被对角高斯单峰头捕捉。
  - **不确定性门控也不是解药**：M2AC（相对不确定性过滤 + 奖励惩罚）与 MACURA（阈值拒绝）在标准 MBPO backbone 上仍失败，换了 FTFL backbone 才恢复 ⇒「dominant bottleneck lies in the learned transition/reward model itself rather than in the uncertainty-based synthetic-data usage rule alone」。
  - 基准差异：STFL 扫 6 个 Gym + 15 个 DMC，Gym 全胜、DMC 7/15 仅等于随机初始策略；同样 MuJoCo 物理引擎、类似奖励结构，结论不可跨基准搬运。

## 来源（URL + 日期 + 状态）
- `https://arxiv.org/html/1906.08253` — WebFetch 200 全文逐字（Janner/Fu/Zhang/Levine, UC Berkeley, *When to Trust Your Model: Model-Based Policy Optimization*：Abstract / §3 Algorithm 1 / §4.1 Theorem 4.1 / §4.2 Theorem 4.2 / §4.3 Theorem 4.3 / §5 predictive model + Algorithm 2 / §6.1–6.2 / §7）。第一独立域·原论文一手。
- `https://arxiv.org/html/2510.01457v4` — WebFetch 200 全文逐字（Barkley & Fridovich-Keil, UT Austin, *A Forensic Analysis of Synthetic Data in RL: Diagnosing and Solving Algorithmic Failures in MBPO*：摘要 / §4.2 尺度错配 / §4.3 残差预测 / §5 FTFL + M2AC + MACURA / 附录 A–D / Figure 1）。第二独立域·2025 独立取证一手。
- WebSearch（2026-11-28）另命中 arXiv:2007.01995 BMPO（双向模型扩展，引 Dyna/MBPO 为骨架）、arXiv:2110.02758（模型-策略联合目标下界）、arXiv:2412.14312 STFL（6 Gym/15 DMC 基准扫描）——按来源族折叠为交叉旁证，不重复计数。

## 不防什么
- 不证明任意环境下样本效率优势：Gym 成立、DMC 可崩；不防模型目标尺度错配与残差预测病理；不确定性过滤/惩罚/拒绝单独不足以修复；短 rollout 不消除模型误差只是压住复合；不替代离线评估（§r733C）或安全护栏（§23）。
