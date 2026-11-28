# r820B · Decision Transformer：把 RL 当成条件序列建模（全文）

> 来源：arXiv:2106.01345《Decision Transformer: Reinforcement Learning via Sequence Modeling》（Chen/Lu/Rajeswaran et al., NeurIPS 2021, submitted 2021-06-02 / v2 2021-06-24）abs + HTML 全文（WebFetch 200 逐字）；NeurIPS'22《You can't count on luck: why decision transformers and RvS fail in stochastic environments》(ACM DL abstract) + Duke D2T2《Steering Decision Transformers via Temporal Difference Learning》(cpsl.pratt.duke.edu PDF) + alphaXiv 2410.24108《RL 梯度作为在线微调 DT 的维生素》+ JOVANA 中文词条（WebSearch 逐字，独立第二域）。落点 `meta/agent-evolution/SKILL.md` §三十七 → 1.29.0。AI 模块 · 2026-11-28 实拉。

## 独点1 把 RL 改写成条件序列建模：token 格式与生成目标

**核心**：abstract 逐字「We introduce a framework that abstracts Reinforcement Learning (RL) as a sequence modeling problem」「Decision Transformer, an architecture that casts the problem of RL as conditional sequence modeling」「Unlike prior approaches to RL that fit value functions or compute policy gradients, Decision Transformer simply outputs the optimal actions by leveraging a causally masked Transformer」「By conditioning an autoregressive model on the desired return (reward), past states, and actions, our Decision Transformer model can generate future actions that achieve the desired return」。

**轨迹 token 序列**（式2）：`τ=(R̂₁,s₁,a₁,R̂₂,s₂,a₂,…,R̂_T,s_T,a_T)`，每步三模态 token=(return-to-go, state, action)。R̂_t=Σ_{t'≥t} r_{t'} 是**未来累计回报**，不是过去 reward——原文「nontrivial to model rewards since we would like the model to generate actions based on future desired returns, rather than past rewards」。只喂最近 K 步共 3K 个 token。

**架构**：各模态线性 embedding + layer norm + **per-timestep**（非标准 per-token）位置编码（因一步对应三 token）；视觉输入用卷积编码器；GPT 因果自注意力掩码，预测时只看当前及之前 token；监督只在 state token 对应输出预测动作（离散 CE，连续 MSE/L2，逐步平均）。原文「We did not find predicting the states or returns-to-go to improve performance」。self-attention 直接做 credit assignment——「Transformers can perform credit assignment directly via self-attention, in contrast to Bellman backups」；绕开 bootstrapping 与「deadly triad」、不需折扣未来奖励。

**推理**：用期望回报+起始状态作 prompt 初始化，每执行一步动作拿到 reward 后**递减**目标 RTG（`R←[R, R[-1]−r]`）直到终止。原文「the desired target returns and the true observed returns are highly correlated on every task」；Pong/HalfCheetah/Walker 近乎完美匹配目标，Seaquest 出现超过数据最高回报的外推。

## 独点2 为什么不需要 value pessimism / behavior regularization：与 TD 类离线 RL 的分工

作者猜想：TD 类「learn an approximate value function and improve the policy by optimizing this value function」，而「This act of optimizing a learned function can exacerbate and exploit any inaccuracies in the value function approximation, causing failures in policy improvement」；DT 不做这种显式优化，「avoids the need for regularization or conservatism」。故与 §r815B CQL（离线加保守防 OOD 高估）是**不同路线**：CQL 仍属 value-based+TD，DT 完全绕开 value/critic/policy gradient。

**实验结果（Competitive 有边界，不能写成全面胜出）**：D4RL Medium/Medium-Replay/Medium-Expert 的 HalfCheetah/Hopper/Walker/Reacher 上 DT 多数任务最高、去掉 Reacher 平均 74.7 vs CQL 63.9、全设置 69.2 vs 54.2；但 Medium HalfCheetah 42.6<BRAC 46.3、Medium-Replay HalfCheetah 36.6<CQL 46.2/BRAC 47.7。Atari 用 DQN-replay 1%（50M 中 50 万 transitions），DT 在 4 游戏中 3 个与 CQL 有竞争力，Qbert 15.4 明显低于 CQL 104.2。
**%BC 对照**（top X% 轨迹行为克隆）：数据充足的连续控制中最优 %BC 常能匹敌 DT，DT 对 %BC 优势主要在**数据较少的 Atari**——不能改写成「低质量数据必胜」。
**关键消融**：K=1（无上下文）大幅变差（Pong 106.1→2.5）⇒上下文能识别「哪条策略生成这些动作」；Key-to-Door 长时 credit assignment（1 万随机轨迹）DT 94.6% vs CQL 13.3%，但 %BC 95.1% 说明支持「用事后回报标签」但不足以单独证明 Transformer 优势；延迟奖励 Hopper（奖励全移到终点）DT 保持而 CQL 崩，源于 TD「require densely populated rewards」而 DT「makes minimal assumptions on the density of the reward」。

## 独点3 独立域反证与落地边界：随机环境 RTG 方差、「luck」与在线微调

**NeurIPS'22《You can't count on luck》**（独立域，ACM DL abstract 逐字）：把 RL 归约为预测任务再用监督学习求解（RvS）虽简单/超参鲁棒/离线强，但「simply conditioning a probabilistic model on a desired return and taking the predicted action can fail dramatically in stochastic environments since trajectories that result in a return may have only achieved that return due to luck」——高回报轨迹可能只是运气好，并非可复现策略。ESPER 改为聚类和条件于**平均簇回报**（独立于环境随机性），在 2048、Connect Four 等随机任务上目标—实际回报对齐显著更好且最高性能超过 value-based 基线。
**Duke D2T2**（独立域 PDF 逐字）：根因是「growing variance of returns-to-go, the signal used by DTs to predict actions, accumulated over the horizon」；用 TD 估计的期望回报替换 RTG 表现更高，D2T2 把当前状态映射为引导向量把 DT 导向高奖赏区，还消除了部署时手搓 RTG 的需要；原文亦承认 DT「poor stitching ability」。
**alphaXiv 2410.24108**（独立域）：在线微调时 RTG 若远偏离期望回报会阻碍微调，TD3 的价值/优势函数可解决；TD3 梯度加到 ODT 微调上有效，尤其低 reward 离线数据预训练时。
**落地口径与边界**：报「用了 DT」须写 RTG  conditioning 值/上下文 K/层数与 head/动作损失类型四件；离线训练仍配离线评估（§r733C OPE）；不防：随机环境「luck」导致的条件失配、stitching 弱、需手指定目标 RTG、训练数据偏差、恶意 reward 设计诱发意外行为（原文结论明列）；适合长时/稀疏/延迟奖励与离线数据复用，不适合要求可复现因果策略或强 stitching 的场景。

**来源**：arXiv:2106.01345 abs + HTML v2 全文（WebFetch 200 逐字：Abstract/式2 轨迹/§4 架构/§5 RTG 递减/§6 Atari+D4RL 表/§7 %BC·K=1·Key-to-Door·延迟奖励·讨论）；NeurIPS'22 You can't count on luck（ACM DL abstract WebSearch）+ Duke D2T2 PDF + alphaXiv 2410.24108 + JOVANA 中文词条 + GitHub awesome_study 精读（WebSearch 交叉，独立第二域，按来源族折叠）。判重：全库 SKILL.md+module-memory 对 `Decision Transformer`/`return-to-go`/`RTG` 0 机制专节（wb-context-compressor/personal-ai-employees/co-learn 命中均为 Transformer 子串或「决策」噪声异命题），豆包自留地 WB 0 落地，按 rules/07「增＝加厚现有」0 新建。
