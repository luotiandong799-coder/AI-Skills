# r816C · 多目标跟踪（MOT）评测：MOTA / IDF1 / HOTA 逐字与判非

> 落地：engineering/multimodal-intelligence SKILL.md 2.4.0 → 2.5.0（加厚现有，0 新建）；共学路由 PI。实拉 2026-11-27，≥2 独立域一手交叉，3 独点。

## 一手来源（URL + 日期 + 抓取方式）

1. **HOTA 原论文** Luiten et al.《HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking》，IJCV（accepted 19 Aug 2020），arXiv:2009.07736v2 — `https://arxiv.org/html/2009.07736v2` WebFetch 200 全文逐字（式 2/4/5/6/13–27）。**第一独立域·原论文一手**。
2. **MOTChallenge 官方归档** `https://motchallenge.net/method/MOT=2950&chl=5&vidSeq=MOT16-12` WebFetch 200 全文逐字（19 项指标全称表 + MOT16 实测 MOTA 61.9/IDF1 56.2/HOTA 46.2；页面标「evaluation service is closed，Archive state of 16 April 2026」如实登记）。**第二独立域·官方一手**。
3. docsaid.org 中文解读 `https://docsaid.org/zh-hans/blog/papers/multi-object-tracking/hota` + qubittool HOTA 词条 + CSDN `blog.csdn.net/qq_46220313/article/details/148293414`（WebSearch 逐字）——第三～五域交叉（立场登记，CSDN 公式错误已按一手纠正）。

**诚信**：`arXiv:2009.13713` 号错配（实为数学论文《Chaos and frequent hypercyclicity for composition operators》），WebFetch 检出后整篇弃用，改用正确号 `2009.07736`，不虚构。

## 独点1：三个指标偏科不同，必须分报不可互证

原论文 Fig.1 逐字：「Three different trackers are shown in order of increasing detection accuracy and decreasing association accuracy. **MOTA and IDF1 overemphasize the effect of accurate detection and association respectively.** HOTA balances both of these by being an explicit combination of a detection score DetA and an association score AssA.」；「MOTA performs both matching and association scoring at a local detection level which biases scores toward measuring detection, while IDF1 performs both at a trajectory level which ends up being biased towards association. HOTA matches at the detection level while scoring association globally over trajectories.」

- **MOTA**（式2）`MOTA = 1 − (|FN|+|FP|+|IDSW|)/|gtDet|`：检测级逐帧一对一匹配；IDSW=「a TP which has a prID that is different from the prID of the previous TP (that has the same gtID)」，只与**上一个** TP 比，不计 ID Transfer（同一 prID 换到不同 gtID）。论文指出「IDF1 … exhibits unintuitive and non-monotonic behaviour in regards to detection」。
- **IDF1**（式4/5/6）`IDF1 = |IDTP|/(|IDTP|+0.5|IDFN|+0.5|IDFP|)`，ID-Recall/ID-Precision 分别以 IDFN/IDFP 为分母；轨迹级匹配 gtTraj↔prTraj，对身份保持敏感。
- 判据（docsaid 逐字）：DeepSORT 论文「ID 切换少了 45%，MOTA 只多了 1.6 分」；FairMOT「只训练检测、re-ID 特征几乎是随机的模型，MOTA 居然比两个任务一起训练的还高」——MOTA 高 IDF1 低说明老丢 ID 又重启；两者都高才是好跟踪；互相矛盾时用 HOTA 综合裁断。

## 独点2：HOTA 是几何平均不是调和平均，且跨阈值积分有顺序约束

原论文逐字：「The final HOTA score is the **geometric mean** of these two scores averaged over different localisation thresholds.」；式21 `HOTA_α = √(Σ_{c∈TP}𝒜(c)/(|TP|+|FN|+|FP|)) = √(DetA_α · AssA_α)`；式18 `DetA_α=|TP|/(|TP|+|FN|+|FP|)`；式19 `AssA_α=(1/|TP|)Σ𝒜(c)`；式14/20 `𝒜(c)=|TPA(c)|/(|TPA(c)|+|FNA(c)|+|FPA(c)|)`——论文称「double Jaccard formulation」。

跨阈值（式16）`HOTA = ∫₀¹ HOTA_α dα ≈ (1/19) Σ_{α∈{0.05,0.1,…,0.95}} HOTA_α`，每个 α 值**各自重新匹配** gtDets 与 prDets。顺序约束逐字：「DetA and AssA should only be combined into HOTA before integrating over a range of α values, not afterwards.」

判据（诚信点）：CSDN `qq_46220313` 把 HOTA 写成 `2·AssA·DetA/(AssA+DetA)`（调和平均）是**错的**，以原论文几何平均为准；qubittool 词条正确给出 `HOTA_α=sqrt(DetA_α·AssA_α)`。报 HOTA 须带 α 网格与「先合成后积分」顺序，否则口径不可比。

## 独点3：五类基本错误拆成子指标，单一标量不足以定位

原论文逐字：「false negatives, false positives, fragmentations, mergers and deviations. These are equivalent to detection recall, detection precision, association recall, association precision, and localisation, respectively.」

- DetRe（式22）`|TP|/(|TP|+|FN|)`、DetPr（式23）`|TP|/(|TP|+|FP|)`、DetA（式24）`DetRe·DetPr/(DetRe+DetPr−DetRe·DetPr)`
- AssRe（式25）/AssPr（式26）逐 TP 对 𝒜 的 recall/precision 版本取平均、AssA（式27）同式合成；「a low AssRe will result when a tracker splits an object up into multiple predicted tracks」「a low AssPr will result if a predicted track extends over multiple objects」
- LocA（式17）逐 TP 的空间相似度 𝒮(c) 跨 α 积分，「similar to MOTP, however evaluated over multiple localisation thresholds」
- MOTChallenge 官方 19 项（全称逐字）：MOTA / IDF1 / HOTA / MT(Ratio of Mostly Tracked Trajectories) / ML(Ratio of Mostly Lost Trajectories) / FP / FN / Rcll(Recall) / Prcn(Precision) / AssA / DetA / AssRe / AssPr / DetRe / DetPr / LocA / FAF(False Alarm Per Frame) / ID Sw.(#ID switches，ratio=#ID switches/recall) / Frag(#Track Fragmentations，FM ratio=#FM/recall)。MOT16 MOTeD 实测 MOTA 61.9 / IDF1 56.2 / HOTA 46.2 / ID Sw. 1003(14.6%) / Frag 2776(40.5%)——说明同一跟踪器三项分数差距大。

判据：分数掉了先定位是漏检（DetRe）/误报（DetPr）/碎轨（AssRe）/合轨（AssPr）/定位（LocA）哪一类，再改模型，不拿单一 MOTA 当 go/no-go；用 TrackEval 等官方脚本复现 benchmark protocol 避免手算误差；本任务载体 multimodal-intelligence 此前只评单帧检测/分割（§r766B）/生成（§r790B）/幻觉（§r794B），本节补「跨帧身份关联」这一维度。

## 判非与去重

- `MOTA`/`IDF1`/`HOTA`/`多目标跟踪` 全库 SKILL.md 0 专节（Grep 全库无命中）；豆包自留地 WB 0 落地。与 §r766B 检测/分割评测（单帧 IoU/mAP/Dice）、§r790B 文图生成对齐、§r794B 幻觉评测分工：那些评单帧或单图，本节评跨帧 ID 关联与时序轨迹。
- 按 rules/07「增＝加厚现有」，本轮 0 新建 / 0 合并 / 0 删除。

## 诚信登记

- 原论文式 2/4/5/6/13–27 逐字转录；Fig.1 的「45%/1.6 分」取自 docsaid 对 DeepSORT 论文的转述（立场登记，非 HOTA 原文数字）。
- MOTChallenge「evaluation service is closed / Archive state 16 April 2026」如实登记，历史榜单仅作指标口径佐证。
- arXiv:2009.13713 号错配弃用；正确论文 2009.07736。二手 CSDN 调和平均公式已按一手纠正。
