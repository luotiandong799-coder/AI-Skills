# r796J｜PI｜图表问答 ChartQA：人写与机器增广两半分报，逻辑+算术推理不是 OCR

访问日期：2026-11-22；每轮独立实拉禁止复用上轮。

## 一手来源逐字

- https://arxiv.org/abs/2203.10244（ChartQA，ACL 2022 Findings，2022-03-19，WebFetch 200 逐字：复杂逻辑与算术推理/T5 生成 23111 问题）

- https://arxiv.org/html/2203.10244v1（WebFetch 逐字：OCR 错误或同义词使空间编码分类法失效/表 1 双半数据量）

- https://github.com/vis-nlp/ChartQA（作者官方数据集仓库，WebFetch 200 逐字：train_human.json 与 train_augmented.json 双文件/split 结构）

## 独有点

1. 双半数据必须分报：ChartQA-H（human-authored，4.8K 图 / 9.6K QA）与 ChartQA-M（machine-generated，17.1K 图 / 23.1K QA，由人写图表摘要经 T5 生成并人工抽检）；判据——合并成单一分数判不合格。论文逐字：generated another 23,111 questions automatically from human-written chart summaries using a T5 model。

2. 推理类型判据：问题需「logical and arithmetic operations」并引用视觉属性（颜色、峰值）；判据——只用 OCR 文本匹配、不看图表视觉表示的方法在 OCR 出错或问题用同义词指代图表元素时会失效（论文逐字）。与文档 TableQA 分工：那里输入是结构化表格，这里输入是图表视觉编码。

3. 拆分与可复现：官方仓库 train/val/test，train 含 train_human.json 与 train_augmented.json 双文件；判据——报结果须写明在哪一半与哪个 split。relaxed accuracy 容差、盲基线数值、图表幻觉术语本轮未从一手取到，不得写成已验证事实。

## 判重与判非

- 判重：`ChartQA`/图表问答在本体与全库 SKILL.md 0；与 §FID/文图对齐/CHAIR-POPE/FastV 分工不复用。豆包自留地 WB 0 落地。

- 抓取失败：初抓 2003.10244 错配地球物理论文已更正 2203.10244；HTML 全文 60s 超时仅前 15000 字，metric/盲基线未取到。
