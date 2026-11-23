# r797C PPO 裁剪代理目标 / 信赖域 — 逐字来源与判非

- 轮次：r797C（2026-11-23）· 模块 AI · 载体 `meta/agent-evolution`
- 主题：策略更新「迈多大步」；与 §25 GAE（优势怎么估）、§30 势函数奖励塑形（奖励怎么设）、§23 安全探索 shield（约束整条策略序列）正交。

## 独点1｜步子过大为何崩：分布漂移 + surrogate 的一阶谎言 + KL 下界
一手（Anthony W. Jung, "From TRPO to PPO", anthony0727.github.io, 2025-04-09；WebFetch 200 全文逐字）：
> "In supervised learning, updating parameters doesn't change the data. In RL, updating the policy changes which states you visit, which changes the data distribution. The optimization landscape shifts under your feet with every gradient step. This is why vanilla policy gradient is unstable. A step that looks good under the current data distribution might be catastrophic once the visitation frequencies change."
> 真目标 η(π̃)=η(π)+Σ_s ρ^{π̃}(s)Σ_a π̃(a|s)A^π(s,a)；代理 L_π(π̃)=η(π)+Σ_s ρ^{π}(s)Σ_a π̃(a|s)A^π(s,a)。"The only difference: ρ^{π̃} vs ρ^{π}. The surrogate pretends the state distribution doesn't change. This is the fundamental lie of policy gradient." "L is a first-order approximation — a tangent plane to η at π. Near π, the tangent plane is accurate. Far from π, it diverges from reality."
> Kakade and Langford (2002): "η(π̃) ≥ L_π(π̃) − C · D_KL^max(π‖π̃)"；"D_TV² ≤ ½ D_KL"。

判据：策略梯度不稳的根因是更新改变访问分布，代理目标只是切平面近似，远离 π 即失真；KL 散度给「访问频率能偏多远」上界，留在信赖域内单调改进有理论保证。control.education（WebFetch 逐字）："A policy gradient step that is too large can collapse performance, because the advantages were estimated under the old policy πθold."

## 独点2｜TRPO 二阶 vs PPO 一阶裁剪：保证已被实现破坏，就换便宜机制
一手（同上 anthony0727 + control.education + Emergent Wiki + inferensys glossary，均 WebFetch 逐字）：
- TRPO：max E_{s~ρ^{πold},a~πold}[π(a|s)/πold(a|s)·A^{πold}]，约束 D_KL(πold‖π)≤δ；"The step direction is approximately F⁻¹g — the natural gradient. The Fisher information matrix F defines the Riemannian metric on policy space. It measures how much the distribution changes, not how much the parameters change." "Solved via conjugate gradient + line search. Elegant, but expensive — the Fisher-vector products are the bottleneck." 经 performance difference lemma 给近似单调改进保证。
- PPO 关键论证（anthony0727 逐字）："TRPO's monotonic improvement guarantee requires exact optimization of the surrogate. In practice, you do approximate SGD with finite samples and mini-batches. The theoretical guarantee is already broken by implementation. If the theory is already approximate, use whatever works."
- 裁剪目标：L^CLIP(θ)=E[min(r_t(θ)Â_t, clip(r_t(θ),1−ε,1+ε)Â_t)]，r(θ)=πθ(a|s)/πθold(a|s)，ε≈0.1–0.2（control.education 逐字 ε=0.2）。"The minimum removes any incentive to move the ratio outside [1−ε,1+ε] in the direction the advantage favors, so several epochs of minibatch stochastic gradient ascent can be run on each batch of data."；"No second-order optimization. No conjugate gradient. No line search. First-order SGD, runs on any framework, parallelizes trivially."

判据：PPO 把 TRPO 的硬 KL 约束换成一阶裁剪，论证前提不是「PPO 更优」而是「TRPO 的理论保证在 mini-batch SGD 下本就没保住」；min 让 ratio 越界方向不再产生梯度激励，故可同批数据多 epoch 复用。

## 独点3｜clip 是软惩罚非硬保证；报告须写全四件
一手（anthony0727 + Emergent Wiki 逐字）：
> "The clipping discourages catastrophic updates — but the ratio itself can still go too far. Clipping flattens the surrogate contribution outside the interval; it is not a hard trust-region constraint."
> "PPO doesn't have TRPO's theoretical guarantees. It doesn't need them to be useful... a cheap mechanism that usually prevents the policy from jumping off a cliff, though not a hard guarantee that it cannot."
- RLHF 部署（Emergent Wiki 逐字）："PPO's most consequential deployment has been in Reinforcement Learning from Human Feedback (RLHF)... a reward model, trained on human preference comparisons, provides a scalar reward signal... a KL-divergence penalty prevents the policy from drifting too far from the original pretrained model."；"the pretrained language model is the trust region, and PPO's clip operation is the mechanism that keeps optimization local."
- 局限（同上）："Its sample efficiency remains poor compared to model-based methods and value-based methods like SAC... its reliance on on-policy data means it cannot reuse experience"；"hyperparameter sensitivity — particularly the choice of ε, learning rate, and the number of epochs per batch"。

判据：clip 只压平区间外代理贡献、ratio 仍可跑远，无 TRPO 单调保证只是「通常防跳崖」；RLHF 里预训练模型即信赖域、clip 保增量对齐不灾难覆盖预训练能力；但 on-policy 不能复用经验、样本效率低于 SAC。报「用了 PPO」须写 ε/优势估计器（GAE λ）/每批 epoch 数/KL 系数四件，不可只报算法名。Emergent Wiki："became the default RL algorithm... not because it is optimal"——默认值不等于最优。

## 来源与诚信（判非）
- 一手：anthony0727.github.io（WebFetch 200 全文逐字，含全部公式与 "fundamental lie" / "already broken by implementation" / "not a hard trust-region constraint" 原句）；control.education、Emergent Wiki WebFetch 200 逐字；inferensys glossary WebFetch 200 逐字（r(θ) 定义与剪辑到 [1−ε,1+ε]）。
- Kakade-Langford (2002) 下界与 D_TV²≤½D_KL 为 anthony0727 文中转述公式，未单独取原始论文全文，标为二手转述不冒充一手。
- 判重：全库 SKILL.md 扫描 `PPO` / `TRPO` / `clipped surrogate` / `信赖域` 在本技能命中均为 §23 shield 的 masked-PPO 集成、§25 GAE 默认 λ=0.95（PPO/TRPO 采用）等语境，无「策略更新步长/裁剪代理」专节；豆包自留地 WB 0 落地。与 §25 GAE（A 怎么估）、§30 PBRS（奖励怎么设）、§23 shield（安全序列约束）、§r795L 主动学习（选新样本）正交不复用。
