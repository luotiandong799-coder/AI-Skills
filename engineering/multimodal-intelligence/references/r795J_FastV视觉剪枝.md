# r795J｜PI｜视觉 token 剪枝 FastV：第 2 层后按注意力分数剪，45% FLOPs 不是随便剪一半

访问日期：2026-11-22。每轮独立实拉，禁止复用上轮结论。

## 一手来源逐字

- https://ar5iv.arxiv.org/html/2403.06764（Chen 等，arXiv:2403.06764，提交 2024-03-11，v3 2024-09-02，ECCV 2024 Oral，WebFetch 200 逐字：深层注意力低效 / 第 2 层后按平均注意力重评 / K=2 R=50% 约 45% FLOPs）

- https://github.com/pkunlp-icler/FastV（作者官方仓库，WebFetch 200 逐字：plug-and-play inference acceleration / 45% theoretical FLOPs / Oral 2%）

## 独有点

1. 标题/ID 判据：arXiv:2403.06764 的真实标题是「An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Inference Acceleration for Large Vision-Language Models」（ECCV 2024 Oral），引用不含此标题即判错误条目；曾错配的 2403.01670 / 2404.10719 一律不得入库。

2. 参数判据：一手须同时出现 `K=2`（第 2 层后开始）与 `R=50%`（保留比例）；论文逐字「Beyond this selected layer, image tokens are re-evaluated based on their average received attention scores」，`K=2,R=50%` 报约 45% FLOPs 降低且不掉性能。宣称「末层剪枝」「需微调」与一手冲突——训练无关。

3. 分类判据：pruning（永久丢弃视觉信息）与 merging（合并冗余特征，如 ToMe/PruMerge）须分列；把 merging 方法归为 FastV 本体判混淆。与本章 §物体幻觉评测分工：剪枝省算力，不自动改善对象存在性幻觉，须另测。

## 判重与判非

- 判重：`FastV`/视觉 token pruning 在本体与全库 SKILL.md 0 命中；与 §FID、§文图对齐、§CHAIR/POPE 分工不复用。豆包自留地 WB 0 落地。

- 抓取失败：第三方综述 arXiv:2603.27960 的提交日未单独核实，仅作分类交叉，不作标题一手。
