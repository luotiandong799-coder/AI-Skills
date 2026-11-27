# r815B CQL 保守 Q 学习（全文 · 2026-11-27 实拉）

## 一手来源与逐字要点
1. arXiv:2006.04779《Conservative Q-Learning for Offline Reinforcement Learning》 — https://arxiv.org/abs/2006.04779 （WebFetch 200 摘要 + 版本史）与 https://arxiv.org/pdf/2006.04779v2 （WebFetch 200 全文逐字）
   - 作者 Kumar / Zhou / Tucker / Levine（UC Berkeley + Google Research Brain Team）；Submitted 8 Jun 2020 v1，revised 19 Aug 2020 v3；NeurIPS 2020。
   - 摘要逐字：「standard off-policy RL methods can fail due to overestimation of values induced by the distributional shift between the dataset and the learned policy, especially when training on complex and multi-modal data distributions」；CQL「learning a conservative Q-function such that the expected value of a policy under this Q-function lower-bounds its true value」；「augments the standard Bellman error objective with a simple Q-value regularizer」；「often learning policies that attain 2-5 times higher final return」。
   - 引言逐字：offline RL = batch RL；直接套 value-based off-policy「generally results in poor performance, due to issues with bootstrapping from out-of-distribution actions and overfitting」「typically manifests as erroneously optimistic value function estimates」；只要求**期望**价值下界而非逐点下界，以避免逐点保守导致的额外低估。
   - 关键思想逐字：「minimize values under an appropriately chosen distribution over state-action tuples, and then further tighten this bound by also incorporating a maximization term over the data distribution」。
2. alphaXiv https://www.alphaxiv.org/abs/2006.04779 （WebFetch 200 全文逐字，公式与数值）
   - 式1 基础保守更新：`min_Q α E_{s~D,a~μ(a|s)}[Q(s,a)] + ½ E_{s,a,s'~D}[(Q(s,a)−B̂^πQ̂^k(s,a))²]`
   - 式2 更紧下界：`min_Q α( E_{s~D,a~μ}[Q] − E_{s~D,a~π̂β}[Q] ) + ½ E_D[(Q−B̂^πQ^k)²]`。第一项惩罚 μ 下高 Q，第二项在数据分布上最大化 Q，防对分布内动作过度低估。
   - CQL(H) 离散：`α( E_s[log Σ_a exp Q(s,a)] − E_{s,a~D}[Q] ) + ½TD`（正则取相对均匀先验的负 KL）。
   - CQL(ρ) 连续：`R(μ)=−D_KL(μ||π_{k−1})`，以上一策略为先验，高维连续动作更稳。
   - 理论：lower-bound property、gap-expanding（拉大 in-distribution 与 OOD 的 Q 差，BEAR 未做到）、safe policy improvement。
   - 实证：D4RL `halfcheetah-random-expert` CQL 92.5 vs 次优 SAC 53.0；Adroit 手操作任务只有 CQL 变体持续优于 BC、2–9×；Atari Q*bert 1% 数据 CQL 14012.0 vs 次优 383.6（36×）。
   - 实现：「fewer than 20 lines of code」叠在 SAC 或 QR-DQN 上；无需显式行为策略估计；α 可用 Lagrangian dual gradient descent 自动调或固定。
3. 交叉 WebSearch 逐字：NeurIPS 2020 proceedings 摘要 · apxml《保守Q学习》（BCQ 约束候选集 vs CQL 改 Q 学习目标；`L_CQL=αR_CQL+L_TD`）· aiknowledge.cn 6.3（BCQ/CQL/IQL 三种保守面孔；α 太小外推膨胀复发、太大退化行为克隆；离线评估必配）· jovanaeducation（下界是保证非启发法、权重过大过度胆怯）。

## 诚信与判非
- 判重：全库 SKILL.md + module-memory 对 `离线强化学习` / `offline RL` / `CQL` / `保守Q学习` 0 专节；§r733C「离线策略评估」是 OPE 前提（日志字段/IPS/positivity），与本节「学保守 Q」异命题；r768A GRPO 一句「off-policy 样本效率」旁及，非机制。
- 豆包自留地 WB 0 落地。按 rules/07「优＝加厚现有」：加厚 `meta/agent-evolution`，0 新建。
- 数值按原文/alphaXiv 立场登记，不跨数据集普适化；不把 CQL 写成通用在线训练法。
