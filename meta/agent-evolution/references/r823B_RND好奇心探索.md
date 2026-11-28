# r823B · RND 随机网络蒸馏 / 好奇心驱动探索全文实拉（AI · 2026-11-28）

## 一手来源（≥2 独立域）
1. arXiv:1810.12894 abs `https://arxiv.org/abs/1810.12894`（WebFetch 200 全文逐字；Submitted 30 Oct 2018，Burda/Edwards/Storkey/Klimov）。
2. ar5iv 全文 `https://ar5iv.labs.arxiv.org/html/1810.12894`（WebFetch 200 全文逐字：§2.2 RND、§2.2.1 Sources of prediction errors、§2.3 Combining intrinsic and extrinsic returns、§2.4 Reward and Observation Normalization、Algorithm 1）。
3. 独立域 WebSearch 逐字交叉：alphaXiv `https://www.alphaxiv.org/abs/1810.12894`（noisy-TV、双头不同折扣因子 γ_E=0.999/γ_I=0.99）、Walking Labs 教材 `walkinglabs.github.io/hands-on-modern-rl/...intrinsic-motivation-exploration`（RND 相对 ICM 不需逆模型/不依赖动作/抗噪声电视）、kg.rounds-tech 论文解读（大规模并行 128–1024 环境）。
诚信：OpenAI 官方 blog 旧路径 404、Lilian Weng blog 与 arxiv/html 直连受 WebFetch 本地回退禁用，均如实登记不冒充来源。

## 独点1 · 机制：固定随机目标 + 可训练预测器，误差只反映认知不确定性
- 原文逐字：「This involves two neural networks: a fixed and randomly initialized *target* network which sets the prediction problem, and a *predictor* network trained on data collected by the agent.」；「The target network takes an observation to an embedding $f:\mathcal{O}\to\mathbb{R}^{k}$ and the predictor neural network $\hat{f}:\mathcal{O}\to\mathbb{R}^{k}$ is trained by gradient descent to minimize the expected MSE $\|\hat{f}({\textnormal{x}};\theta)-f({\textnormal{x}})\|\^{2}$」；「This process distills a randomly initialized neural network into a trained one.」
- 内在奖励（Algorithm 1 逐字）：`i_t = || f_hat(s_{t+1}) - f(s_{t+1}) ||^2`。摘要：「The bonus is the error of a neural network predicting features of the observations given by a fixed randomly initialized neural network.」
- 误差来源三分，只有第一类可用：原文列「1. *Amount of training data*. Prediction error is high where few similar examples were seen by the predictor (epistemic uncertainty).」，并逐字点明「**Factor 1 is what allows one to use prediction error as an exploration bonus.**」；另两类（环境随机性/模型误设）不是探索信号。
- 为什么不会 stale：「Such prediction errors tend to decrease as the agent collects more experience similar to the current one.」；「RND obviates factors 2 and 3 since the target network can be chosen to be deterministic and inside the model-class of the predictor network.」——把预测问题定义成输入的确定性函数（固定随机网络的输出），从根上躲开 noisy-TV：原文反例「an agent trying to maximize this prediction error will tend to seek out stochastic transitions, like those involving randomly changing static noise on a TV, or outcomes of random events such as coin tosses.」
- 效果（abs 逐字）：Montezuma's Revenge「first method that achieves better than average human performance on this game without using demonstrations or having access to the underlying state of the game, and occasionally completes the first level.」

## 独点2 · 内外奖励组合：双 value 头 + 内在 non-episodic
- 线性分解（逐字）：「the return is linear in the rewards and so can be decomposed as a sum $R=R_{E}+R_{I}$ of the extrinsic and intrinsic returns respectively.」；「Hence we can fit two value heads $V_{E}$ and $V_{I}$ separately using their respective returns, and combine them to give the value function $V=V_{E}+V_{I}$.」；Algorithm 1「Calculate combined advantages $A_{i}=A_{I,i}+A_{E,i}$」。
- 为什么必须分开：「there may still be a benefit to having separate value functions since there is an additional supervisory signal... especially for exploration bonuses since the extrinsic reward function is stationary whereas the intrinsic reward function is non-stationary.」；「two value heads is necessary for combining reward streams with different characteristics, and so all further experiments use two value heads.」双头还允许不同折扣因子（alphaXiv：γ_E=0.999、γ_I=0.99）。
- 情节边界非对称：内在奖励用 non-episodic——「In that setting the return is not truncated at 'game over'」，因为「the agent's intrinsic return should be related to all the novel states that it could find in the future, regardless of whether they all occur in one episode or are spread over several」；外在奖励必须 episodic，否则「could be exploited by a strategy that finds a reward close to the beginning of the game, deliberately restarts the game by getting a game over, and repeats this in an endless cycle.」

## 独点3 · 归一化是必需件：奖励尺度 + 观测白化
- 奖励（逐字）：「the scale of the reward can vary greatly between different environments and at different points in time, making it difficult to choose hyperparameters that work in all settings.」⇒「we normalized the intrinsic reward by dividing it by a running estimate of the standard deviations of the intrinsic returns.」
- 观测：「Observation normalization is often important in deep learning but it is crucial when using a random neural network as a target, since the parameters are frozen and hence cannot adjust to the scale of different datasets.」；「Lack of normalization can result in the variance of the embedding being extremely low and carrying little information about the inputs.」方案逐字「we whiten each dimension by subtracting the running mean and then dividing by the running standard deviation... clip the normalized observations to be between -5 and 5」，公式 `x -> CLIP((x - μ) / σ, [-5, 5])`；predictor 与 target 同用、policy 不用；优化前用随机 agent 走少量步初始化归一化参数。
- 落地口径：报「用了 RND」写四件——目标网络固定/noisy-TV 规避方式、内在奖励公式、双 value 头（γ_E/γ_I）与 non-episodic 选择、两层归一化（奖励 running std + 观测白化 clip）。缺任一件等于只用了「预测误差」这个词而非 RND 机制。

## 判非 / 去重 / 边界
- 与 §r717A 探索利用门（UCB/Thompson bandit：选臂 regret）、§r788A PBRS（加中间奖励但保最优策略不变）、§r792B 课程学习（数据顺序）、§r796L PER（按 TD error 采样）分工——RND 是**状态新颖性的内在奖励**，靠固定确定性随机目标把误差限在认知不确定性；不改最优策略、不改数据顺序、不是采样权重。豆包自留地 WB 0 落地；按「增＝加厚现有」0 新建。
- 不防：环境的真实 aleatoric 随机性（只能靠目标确定性规避而非消除）、奖励 hacking（agent 可学会寻找预测器尚未拟合的无关新状态）、目标网络容量过小导致 embedding 分辨率不足；纯内在奖励在真实外部奖励稀疏任务上的最终目标达成需另设验收。
