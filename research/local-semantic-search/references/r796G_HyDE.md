# r796G｜KI｜五、HyDE：先生成假设文档再嵌入，绕过 query-doc 表征不对齐

访问日期：2026-11-22；每轮独立实拉禁止复用上轮。

## 一手来源逐字

- https://arxiv.org/html/2212.10496（Gao/Ma/Lin/Callan，arXiv:2212.10496，v1 2022-12-20，WebFetch 200 逐字：零样本生成假设文档/Contriever 编码/假文档含错误细节/dense bottleneck 过滤/无需相关性监督）

- https://aclanthology.org/2023.acl-long.99/（ACL 2023 pp.1762-1777，WebFetch 200 逐字：文档为 fake 含幻觉/向量定位语料邻域/与 generative retrieval 的区别）

## 独有点

1. 流程三段缺一不可且顺序固定：query → instruction-following LLM 零样本生成 hypothetical document（可含幻觉）→ 无监督编码器（Contriever）嵌入该文档 → 在语料嵌入空间按向量相似检索真实文档。判据——用 query 直接 embed、或跳过生成假设文档 → 非 HyDE。Gao 2022 逐字：generate a hypothetical document 再 encode into embedding vector。

2. 语义鸿沟处理机制：论文把任务分解为 NLG（生成）+ NLU（编码），query-doc 相似度「no longer explicitly modeled nor computed」，靠 encoder 的 dense bottleneck 过滤假文档里的错误细节（「may contain false details」）。判据——不得把假文档当事实来源输出，它只用于检索定位。

3. 与改写类区分：HyDE 改写对象是「文档空间假设」而非 query 本身，不产生多 query 并行检索（区别于 multi-query / query rewriting）；且无需相关性标注、zero-shot 开箱即用。判据——把 HyDE 与 generative retrieval（直接生成 doc id 指向真实文档）混称判错。注意：正交区分由流程推出，非论文原文措辞。

## 判重与判非

- 判重：`HyDE`/`假设文档` 在 KI 本体 0；豆包自留地 `wb-context-compressor` 有 query transformation 提及（WB 0 落地异命题）；与 §四分块、§五 RRF 分工不复用。

- 抓取失败：arXiv PDF 非文本已改 HTML；「no relevance feedback」「semantic gap」非论文原词，按原词表述。
