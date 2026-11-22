# r796L｜AI｜优先经验回放 PER：按 TD error 采样，用 IS 权重把偏差买回来

访问日期：2026-11-22；每轮独立实拉禁止复用上轮。

## 一手来源逐字

- https://arxiv.org/abs/1511.05952（Schaul 等，DeepMind，ICLR 2016，arXiv:1511.05952，WebFetch 200 逐字：均匀回放按原始频率/41 of 49 games 胜过基线）

- https://arxiv.org/html/1511.05952v4（WebFetch 200 逐字：两变体对 |δ| 单调且 rank-based 抗异常/改变分布即改变收敛解/diversity 损失/IS 纠正）

## 独有点

1. 两变体都随 |δ| 单调：proportional `p_i=|δ_i|+ε`、rank-based `p_i=1/rank(i)`；论文逐字：rank-based「insensitive to outliers」更稳健。判据——只写「按 TD error 采样」不写明 proportional/rank-based 变体与其异常值敏感度，判不完整；均匀随机基线 = α=0 / 无 PER。

2. 偏差必须显式纠正：`w_i=(1/N·1/P(i))^β`，β=1 完全补偿非均匀采样偏差；论文逐字：prioritized replay changes the distribution「in an uncontrolled fashion, and therefore changes the solution that the estimates will converge to」。判据——用了优先采样却没有 IS 权重纠正，判偏差未处理。

3. 权衡与边界：优先回放导致 loss of diversity，用 stochastic prioritization 缓解、用 IS 纠偏；论文称 DQN+PER 在 41/49 款游戏胜过均匀回放（一手数字），但这是 Atari 设定不迁移为本仓阈值。罕见经验遗忘的原文措辞是「rapid forgetting of possibly rare experiences」，不要泛化写成「灾难性遗忘」当引用。

## 判重与判非

- 判重：`优先经验回放`/`PER` 全库 SKILL.md 0；与 §23 持续学习 EWC（防遗忘）、§r795L 主动学习（选新样本）分工不复用。豆包自留地 WB 0 落地。

- 抓取失败：DeepMind 官方实现仓库未取到一手，第三方实现全排除；abs 与 html 为同论文两视图非两独立文档已如实登记。
