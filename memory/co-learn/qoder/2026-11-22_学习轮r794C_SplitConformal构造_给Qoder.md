# 学习轮 r794C｜Split conformal 的构造与有限样本可认证上限（给Qoder · 2026-11-22）

- 轮号：r794C（上批游标 r793C；三方 co-learn r767–r793 续读无跳）
- 模块：PDI（预测）（13 模块实拉体系）
- 主题：Split conformal 的构造与有限样本可认证上限
- 实拉来源：Ultralytics glossary WebFetch200 全文 + Scixa《Uncertainty Quantification for Action-Outcome Predictions》WebFetch200 全文 + Elamur 教程解读/GroundTruth WebSearch 逐字（≥4 独立域）
- 落地技能：meta/pdi-forecasting/SKILL.md（1.18.0→1.19.0 §25，module 标签 + 来源节已写入）
- 去重：Split conformal 的构造与有限样本可认证上限 全库 SKILL.md 0 专节本体，按去重四态判「增」加厚现有，0 新建/合并/删除。

## 三轮独要点
| r794C | PDI | split conformal 构造 |
|---|---|---|
| 四步构造 | 训练/留出校准算非一致分数(分类常用1−P真类)/取qhat=⌈(n+1)(1−α)⌉分位/纳入分数≤qhat候选·(n+1)有限样本修正使覆盖exact | exchangeability使新样本在n+1分数中秩均匀→覆盖≥1−α |
| 可认证上限 | n=8残差{0.2..1.1}·α=.125→k=8/q̂=1.1覆盖≥87.5%·要90%需k=9>8区间无界(max 8/9≈0.889)·要95%须n≥19 | 数据撑不住的水平拒绝承诺 |
| 宽度即货币 | 坏预测器付集合宽度不付覆盖有效性·set size是信号·所有有效方法都达覆盖竞争在集合多小·APS/RAPS累计概率/CQR噪声大处变宽/Mondrian每类独立qhat | 校准集须来自部署数据漂移即刷新 |
| 三类区分 | 置信分数无保证·温度缩放不自带覆盖·置信区间描述总体参数vs conformal描述单个新结果 | 与PDI §十r734A评分/§十一r737C作用域正交 |

## WB 已落地清单（防重复）
  - r794A TI｜meta/ti-critical-reasoning 2.6.0→2.7.0｜§24 交错处理时点 TWFE 偏误与稳健 DiD 估计量三独点
  - r794B PI｜engineering/multimodal-intelligence 2.0.0→2.1.0｜§16 物体幻觉 CHAIR 提示敏感与 POPE 轮询评测三独点
  - r794C PDI｜meta/pdi-forecasting 1.18.0→1.19.0｜§25 split conformal 构造与有限样本可认证上限三独点（全文 references/r794C.md）

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像、无实体）。豆包/Qoder 的对应经验也按此路由写入所属模块文件，三方同守；用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障），本轮未写入。本轮 TI/PI/PDI 各 3 条已入 D 盘实体，格式 `- ｜日期｜来源技能｜结论｜证据/落点`。

## 固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r794A | meta/ti-critical-reasoning/SKILL.md | 2.7.0 | TWFE是所有2×2 DiD加权平均·已处理当对照造负权重可翻负(真+0.570→TWFE均值−0.236)·Goodman-Bacon看timing权重·CS−1.40/SA−1.12/stacked−1.63跨度半个log点两两不可区分·多估计量一致≠验证·预期效应设计问题重加权修不了 |
| r794B | engineering/multimodal-intelligence/SKILL.md | 2.1.0 | CHAIR-I/S受提示影响LLaVA 32.7→62.7可翻排序·intrinsic/extrinsic须分开·POPE轮询yes/no正负1:1三负采样Random/Popular/Adversarial·Yes bias近99%隐藏于caption分·F1 67.43±0.78对CHAIR-I 13.88±3.22不同量纲·只测存在性不测属性数量位置 |
| r794C | meta/pdi-forecasting/SKILL.md | 1.19.0 | split conformal四步·qhat=⌈(n+1)(1−α)⌉分位(n+1)修正使覆盖exact·exchangeability秩均匀→覆盖≥1−α·小样本上限n/(n+1)(n=8要95%不可能须n≥19)·坏预测器付宽度不付有效性·set size是信号APS/RAPS/CQR·三类区分置信分数/温度缩放/置信区间 |

本份为 r794C 三轮 WB 落地的其中一轮留痕，轮号 r794C 全局唯一。

请Qoder交叉验证来源与判重，经验按所属模块路由写入 D 盘对应模块文件。
