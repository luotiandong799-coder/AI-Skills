# r776A 下沉全文｜Hyperband 多保真资源分配（AI / agent-evolution）

> 独立实拉 2026-11-19，≥2 独立域一手交叉。正文下沉，SKILL.md §27 留指针以守 500 行上限。

## 一、把超参搜索写成「纯探索无限臂老虎机」——早停是资源重分配，不是省钱的权宜计
- Hyperband 的原论文（Li/Jamieson/DeSalvo/Rostamizadeh/Talwalkar, JMLR 18(185):1-52, 2018, arXiv:1603.06560）把超参优化形式化为一个 **pure-exploration non-stochastic infinite-armed bandit**：预算（迭代数 / 数据样本 / 特征）被分配给随机采样的 configurations，通过 **adaptive resource allocation and early-stopping** 加速随机搜索；论文原文报在多种深度学习和核学习问题上「over an order-of-magnitude speedup over our competitor set」。
- 与 agent-evolution §十六 bandit 探索—利用门的分工必须写清：§十六管的是「在线自适应时怎么分配试验预算以最小化 regret」，动作的奖励是任务表现；本机制管的是「一次性搜索最好配置时怎么把有限训练预算在候选间重分配」，臂就是候选配置、奖励是验证集表现。两者同用 bandit 语言但目标函数与部署形态不同，不并存、不互相替代。
- 一手原文：`https://jmlr.org/papers/v18/16-558.html`（WebFetch 200 摘要逐字，pure-exploration non-stochastic infinite-armed bandit / adaptive resource allocation and early-stopping / over an order-of-magnitude speedup）。

## 二、Successive Halving 的核心两难：候选数 K 与单候选预算 B/n 不能同时最大
- 机制（MLSys 2022《Improving Model Training with Multi-Fidelity Hyperparameter Evaluation》算法 4 逐字）：给定 K 个配置、最小预算 b、淘汰比 η，`s=⌊log_η(K)⌋`、总预算 `B=Kbs`；每轮 `K_r=⌊Kη^{-r}⌋`、`b_r=bη^r`，评估当前 K_r 个配置后保留前 K_r/η 个，重复到剩一个。Jamieson & Talwalkar 的主定理给出 SH 在总预算 B 超过某阈值时能返回真正最优配置。
- 两难原文（MLSys 2022 §A.2 / CMU-ML-20-104 §2.3.1）：固定 B 时用户必须选 K——「Trying larger K and assigning a small budget to each can result in prematurely terminating good configurations while trying only a few and assigning them a larger budget can result in wasting resources on evaluating a poor configuration」。CMU 论文用 envelope 函数解释：两配置的中间损失与终损偏差包络不再重叠时才能区分；包络更宽（收敛慢）或终损更接近时需要更多资源才能区分 ⇒ 收敛慢 / 候选质量接近时该少候选长预算，收敛快 / 候选多劣质时该多候选短预算。
- argmin.net《Embracing the Random》(2016-06-23) 逐字量化：N 个配置先各跑 T，保留 N/2 跑 2T，重复 log₂(M) 轮，同样计算预算下 successive halving 比纯随机搜索多看 `M/log₂(M)` 倍配置；但「just because a parameter setting looks bad at the beginning of a run of SGD, doesn't meant that it won't be optimal at the end」——低学习率前期差后期可能最优，缓解是「start the halving process later」（给更长的初段预算再淘汰）。
- 落地判据：SH 不是「一律早停」，而是「先定 envelope 何时可区分再定首轮预算」；首轮预算过短会系统性误杀慢热候选。

## 三、Hyperband 用 bracket 网格枚举多组 (K,b) 把两难交给预算自动扫
- 机制（MLSys 2022 算法 5 逐字）：输入最大预算 R 与 η，`s_max=⌊log_η(R)⌋`、`B=(s_max+1)R`；外层 `s = s_max, s_max-1, ..., 0`，每 bracket 取 `K=⌈Bη^s/(R(s+1))⌉`、`b=Rη^{-s}`，随机采样 K 个配置后调用 SH。s=s_max 时 K 最大、每候选预算最小、最激进早停；s=0 时每候选都拿满 R，即经典随机搜索。
- 用户只需给两个「约束式」参数：愿意在开始比较前跑的最短时间 T（须大于检查开销）与最长愿意跑的时间 M（deadline），Hyperband 自动生成 bracket 网格；argmin.net 原文「The only parameter that needs to be given to Kevin's code is M」。
- 边界（MLSys 2022 §A.2 逐字）：「the brackets in HB are independent of each other. And, the configurations in the next bracket are still sampled randomly without any guidance which means the information of previous brackets wastes」；BOHB（Falkner/Klein/Hutter）用 TPE 贝叶斯采样替换纯随机采样补这个浪费；ASHA 是 SH 的异步并行版。
- 落地判据：报告 HB 结果必须写明 bracket 网格（s_max/B/R/η）与每 bracket 的 K、b，不能只报「随机搜索快 N 倍」；低学习率等慢热场景把首轮预算或 bracket 起点抬高，避免 early stopping 误杀。

## 来源（≥2 独立域一手交叉）
- `https://jmlr.org/papers/v18/16-558.html`（JMLR 18(185):1-52, 2018 官方页，WebFetch 200 摘要逐字）— 第一独立域·原论文一手。
- `https://proceedings.mlsys.org/paper_files/paper/2022/file/c4d41d9619462c534b7b61d1f772385e-Paper.pdf`（MLSys 2022 官方 PDF，算法 4 Successive Halving / 算法 5 HyperBand 与两难原文逐串命中）— 第二独立域·会议论文一手。
- 交叉快照（不冒充一手全文）：`http://reports-archive.adm.cs.cmu.edu/anon/anon/usr0/ftp/ml2020/CMU-ML-20-104.pdf`（CMU 硕士论文 §2.3.1/2.3.2 envelope 函数与 n vs B/n 两难逐字）· `https://archives.argmin.net/2016/06/23/hyperband/`（argmin.net 2016-06-23 M/log₂(M) 与 start halving later 逐字）· `https://www.diva-portal.org/smash/get/diva2:1464560/FULLTEXT02`（DiVA 学位论文 budget allocation 分类与 BOHB 补浪费逐字）。

## 判非 / 去重
- `Hyperband` / `successive halving` 全库 SKILL.md 本体 0 命中（唯一两处命中是 agent-evolution §19 CUPED 章节 r745C 的判非句里「全库 0 命中」的自我登记，非本体落地）；`ASHA` 1 命中在 `engineering/ei-reliability` 为异命题（那里是异步执行可靠性语境），登记不复用。
- 与 §十六 bandit（在线 regret / 探索预算）、§十九 CUPED（不增样本提灵敏度）分工：那两章管「对照实验怎么设、何时停、如何在不加样本下更灵敏」，本章管「一次性超参搜索里训练预算怎么在候选间重分配」。与 r768A GAE / r772A 因果森林（策略梯度信号 / 异质性处理效应）不复用。
- 豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地。与 r775/r774/r773 九模块结论不复用。
- 未采纳：BOHB 的 TPE 采样数学、ASHA 异步并行调度细节、Median Stopping Rule / Bayesian Optimal Stopping 等其他 early-stopping 系列（异命题，留给后续）。
