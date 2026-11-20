# r784A 元学习 / MAML：把「学」的目标从单任务表现改成「几步就能适配」

> 独立实拉 2026-11-20，≥2 独立域一手交叉。归属 AI 模块，落 `meta/agent-evolution` §29。

## 独点1：目标函数换了——学的不是某任务的最优权重，而是「对任务分布敏感」的初始化点
- 优化型元学习 = "learning to learn"：训练模型初始化或更新规则，使其用极少数据快速适配新任务（aiwiki 逐字）。
- MAML（Finn/Abbeel/Levine 2017）原话逐字："the parameters of the model are explicitly trained such that a small number of gradient steps with a small amount of training data from a new task will produce good generalization performance on that task"（aiwiki 引原论文）。
- 双层优化（wikiprompt 逐字公式）：内循环 `θ'_T = θ − α∇_θ L_T(f_θ, D_tr)`（支持集上一步/几步梯度，模拟测试时适配）；外循环 `min_θ Σ_T L_T(f'_θT, D_te)`（查询集算 meta-loss，梯度穿过内循环反传）。关键不在 θ 已在某任务上好，而在 θ 位于"梯度下降特别有效"的参数区域——优化的是损失对初始化的敏感度。
- α（内）/β（外）两个学习率、内步数 k、任务分布 p(T) 是四个必须显式声明的量；报告"用了元学习"须写任务分布/内外学习率/内步数三件，否则不可复现。

## 独点2：二阶梯度是代价核心，FOMAML/Reptile/Meta-SGD 是同一目标的不同「过不过二阶 / 学不学逐参学习率」旋钮
- 穿过内循环反传需要二阶导（gradients of gradients），"computationally expensive"；FOMAML 丢掉二阶项，"often performs nearly as well in practice while being computationally cheaper"（aiwiki/wikiprompt 两源一致）。
- Reptile（Nichol/Achiam/Schulman 2018）：不对优化过程求导，"repeatedly performs several steps of SGD on a task and then moves the initialization toward the resulting parameters"，性能与 MAML 相当（aiwiki 逐字）。
- Meta-SGD（Li 等 2017）：连每参数学习率与更新方向一起 meta-learn，非固定学习率，报称能让"any differentiable learner in just one step"适配（aiwiki 逐字）。
- 模型无关性：可套任何梯度下降可训模型（分类/回归/RL），不引入新参数不改架构；但梯度要求限定了适用范围，实测多在小型 conv/resnet，Omniglot 5-way 1-shot 98.7%、miniImageNet 48.7%（5-way 1-shot）/63.1%（5-way 5-shot）。

## 独点3：与迁移学习 / §24 持续学习是三个不同问题，且 MAML 有任务分布前提与 meta-overfit 边界
- 迁移学习预训练参数为单一源任务优化；MAML 为任务分布优化、显式鼓励可适配——"the goal is to minimize the number of fine-tuning steps required"（wikiprompt 逐字）。二者不并存。
- 与 §24 持续学习分工：那章管"连续学新任务别忘旧任务"，MAML 管"见到新任务时几步适配"，目标函数与验收指标都不同。
- 前提与边界（wikiprompt Limitations 逐字）：单一初始化服务全部任务的前提"may not hold for highly diverse task sets"；对内学习率与内步数敏感需调；"performance degrades when the task distribution is not smooth or when tasks are very different"；任务分布窄时 meta-overfit；更简单的"预训练+好正则微调"基线在某些 benchmark 能追平 MAML。⇒ 启用前先问"任务是否真的共享结构、分布是否足够宽"，否则退回复用已有训练流程。
- 与 §27 Hyperband/§28 BO 分工：那两章管一次性搜索怎么分配预算/怎么选下一个点，本章管跨任务的初始化怎么学，三者正交。

## 来源与诚信（≥2 独立域一手交叉）
- `https://aiwiki.ai/wiki/one-shot_learning`（AI Wiki One-Shot Learning 条目，WebFetch 200 全文逐字）— MAML 原话引用、inner/outer 两循环、FOMAML、Reptile、Meta-SGD、四族方法对比表、48.70% miniImageNet、Finn 2017 ICML 70:1126-1135 著录。**第一独立域·一手百科**。
- `https://www.wikiprompt.org/wiki/model-agnostic-meta-learning`（Wikiprompt MAML 条目，WebFetch 200 全文逐字）— 双层公式与 α/β、transfer learning 对比段、limitations/meta-overfit、Reptile/Meta-SGD/ProMPL、98.7%/48.7%/63.1%、计算代价。**第二独立域·一手百科**。
- 交叉快照（不冒充一手全文）：`https://web.cs.umass.edu/publication/docs/2022/UM-CS-PhD-2022-002.pdf`（UMass 博士论文 WebSearch 逐字：内循环式 2.4 / 外循环式 2.5、α 可 meta-learn、iMAML/Latent Embedding Optimization）· `https://ai360xpert.com/papers/maml`（Finn/Abbeel/Levine 2017 论文综述 WebSearch 逐字：golden initialization 与二阶梯度解释）。
- 降级如实登记：尝试抓 `https://arxiv.org/abs/1707.02937` 以为是 MAML 原论文，实际返回的是 checkerboard artifact 论文（Aitken 等），**ID 抓错、该源弃用不冒充 MAML 一手**；原论文结论以上面两域一手百科 + UMass 博士论文逐字公式登记。
- 判非/去重：`MAML`/`元学习`/`learn to learn`/`内循环`/`外循环`/`few-shot adaptation` 全库 SKILL.md 本体 0（唯一命中 `engineering/wb-artifact-verification` 的 RATED 是"在线 bandit 按执行反馈重排工具"，异命题）。与 §16 bandit、§24 持续学习、§27/§28 搜索三章分工。豆包自留地 WB 0 落地。
- 未采纳：iMAML / Latent Embedding Optimization / ProMPL 的实现细节、MAML 与 Transformer/ICL 结合的实证（异命题与建模细节，留后续）。
