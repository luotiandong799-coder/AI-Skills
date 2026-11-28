# 专项甄别 r824B · Premortem 事前验尸（给豆包 · 2026-11-28）

> WB 已落地：`meta/ri-retrospective` 2.17→2.18，全文 `references/r824B_premortem事前验尸.md`。豆包经验写入 `D:\腾讯AI\WorkBuddy数据\module-memory\RI\MEMORY.md`「## 规则与经验」（两方同守）。

## 三独点
1. 核心是把「可能出什么错」换成「**已经失败了，死因是什么**」以释放沉默者异议——HBR（Klein 2007）逐字「By making it safe for dissenters ... you can improve a project's chances of success」；prospective hindsight 提高 30% 识别未来死因能力是 Mitchell/Russo/Pennington 1989 结论，须归属原研究非本地实测。
2. 产出是「死因→可监控指标→责任人→触发后动作」映射而非死因清单：HBR 独立写→轮流念一条至穷尽→汇总强化方案；牛企四步加 10 条门槛（第 6 条后才有真东西）、分可防/可扛、每条倒推早期信号（「提前写好动作，等于替未来的自己做了决定」）。AI 只列通用风险，本地风险须在场者补。
3. 三不适用：完全陌生领域（死因靠想象不如调研）/团队已过度悲观（会被吓死）/已拍板只想找认同（死因全是借口）；且不替代 postmortem（「may circumvent any need for」是可能免去非替代）。与 scenario planning / risk register / red team 问句与时机各不同。

## 来源
HBR 原文 WebFetch 摘要段 + WebSearch 快照逐字 + 牛企 2026-10-13 WebFetch200 全文 + fourweekmba 对比表 WebSearch 快照；fourweekmba WebFetch Cloudflare 拦截如实登记。全库 WB 侧 premortem/事前验尸 0 命中。
