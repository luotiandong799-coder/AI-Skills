---
name: local-semantic-search
description: >-
  本地语义搜索：在个人电脑上按「意图」而非关键词找内容。覆盖本地文件搜索、PDF 搜索、工作资料查找、历史记录检索、图片与文档关联搜索。核心是理解用户需求后找到相关内容，而非字符串匹配。当用户要在本机找资料、搜历史对话/文档、按意思查文件、跨 PDF 与笔记关联检索时使用。触发词：帮我找、本地搜索、搜一下我的、按意思搜、相关文件、历史记录里、之前那个文档、跨资料检索、语义搜索、找讲过的内容。不适用：联网全网搜索（走 web-scrape/agent-reach）、精确文件名查找（用 Glob/Grep）。
version: 1.2.0
module: KI
modules: KI
---

# local-semantic-search（本地语义搜索）

定位：信息检索层。源自 DeepLearning.AI「Local Semantic Search」模块。

## 一、与关键词搜索的区别

- 关键词搜索：匹配字面（Glob/Grep 已够用，不重复造）。
- 语义搜索：理解「用户真正想要什么」，把「讲过物联网安全的内容」映射到具体笔记/对话/PDF，即使标题没这几个字。

## 二、流程

```
用户需求（自然语言）
  → 解析真实意图（主题/时间/类型/相关人）
  → 选检索面（本地文件 / PDF / 记忆日志 / 历史对话 / 归档）
  → 语义召回候选
  → 按相关度排序 + 给出出处
  → 关联扩展（同主题的其他资料）
```

## 三、安全与边界（硬规则）

- **默认限制目录**：只允许在用户显式授权的目录检索（如 D:/腾讯AI、工作文档目录），不扫系统盘/其他用户目录。
- **扫描前必须授权**：首次检索某目录先问用户，不静默全盘爬。
- **不读取隐私文件**：密钥、cookie、token、私人聊天不在检索与索引范围。
- **支持删除索引**：用户可随时清除已建索引；索引不含原文外发。
- **结果可溯源**：每条命中必须带文件路径/时间，便于用户复核，不凭空生成「我找到了」。

## 四、验收

能给「之前讲过 X 的那份资料在哪」一个带出处路径的答案；找不到时直说「无匹配」，不拼凑。

## 五、多路召回融合（RRF · 2026-11-08 实拉加厚）

> 本机语义检索已有 `_tools/semantic_search.py`（向量）与 Glob/Grep（字面）。当两路召回都要用、分数又不可比时，按本节融合。

### 5.1 用秩不用分数，异构相关性免调参
- 官方原文逐字："Reciprocal rank fusion (RRF) is a method for combining multiple result sets with **different relevance indicators** into a single result set. **RRF requires no tuning**, and the different relevance indicators **do not have to be related to each other** to achieve high-quality results."
- 公式（官方）：`score = Σ_q 1 / (k + rank(result(q), d))`，rank 从 1 起；k 为 ranking constant。
- 判据：① BM25 分数与余弦距离**量纲不同**，不要试图归一化到同一尺度再相加——直接换成「名次倒数」求和；② 融合至少需 **2 个子检索器**，且各子检索器**等权**（"Each child retriever carries an equal weight"）；③ 支持多 standard 检索器组合（BM25 + ELSER/稀疏向量），不必强依赖 kNN。

### 5.2 两根独立旋钮，默认值跨版本漂移
| 参数 | 含义 | 默认值（按版本） |
|---|---|---|
| `rank_constant` (k) | 越大 ⇒ 低排名文档对最终排序影响越大；须 ≥1 | **60**（三版一致） |
| `rank_window_size` / 旧 `window_size` | 每个子检索器参与融合的候选池深度；越大越准越慢；须 ≥ `size` 且 ≥1 | 8.8：**100** · 8.18：**10** · current：**= size** |
- 官方：`k` 大于窗口时结果**截断到窗口**，`k` 小于窗口时取 `k`；最终融合集再剪到 `size`。
- 判据：① 融合窗口是**独立于返回条数**的旋钮，窗口设得比 `size` 小会把「只在某一路长尾出现」的正确文档直接排除在融合之外，且不会报错；② 8.8 用 `rank.rrf` + `window_size`，current 用 `retriever.rrf` + `rank_window_size`，**同一算法跨版本参数名与默认值都变** ⇒ 抄旧文档配置会静默配错，落配置前先核对实际版本文档。

### 5.3 融合后排序键改变，且有显式不支持清单
- 8.8 官方全文示例：RRF 结果 `_score: null`，"we instead use **_rank** to show our top-ranked documents"；current 版 `rrf` retriever **不支持 `scroll` / `sort` / `rescore`**，使用即抛异常。
- 官方："It is best to avoid providing a point in time as part of the request, as RRF creates one internally that is shared by all sub-retrievers to ensure consistent results."
- 判据：① **融合后的分数不能当相关性置信度用**（不同路的原始分数不可比，融合分只是名次函数），需要置信度就回到各子检索器自己的分数；② 不支持项是**抛异常**而非静默降级 ⇒ 把 `sort` 挂在融合查询上是配置错误，不是「排序没生效」；③ 一致性由内部共享 PIT 保证，外部再传 PIT 反而破坏这一保证；④ 融合结果要保留「命中了哪几路」的来源标记，便于溯源（本机语义搜索的「结果可溯源」硬规则）。

## 六、来源（本轮独立实拉，2026-11-08）
- Elasticsearch Reference **current**《Reciprocal rank fusion》一手全文 WebFetch 逐字核验（公式 / 等权 / 默认值 / 不支持清单 / PIT / `_rank`）→ https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html
- Elasticsearch **8.8** rrf（`rank.rrf` + `window_size` 默认 100、`_score: null`）→ https://www.elastic.co/guide/en/elasticsearch/reference/8.8/rrf.html
- Elasticsearch **8.18** rrf（`rank_window_size` 默认 10，证实版本漂移）→ https://elastic.co/guide/en/elasticsearch/reference/8.18/rrf.html
- 腾讯云 ES《Hybrid Search (RRF Fusion Ranking)》（rank_constant 60 / 窗口默认 100 / 8.16 `rank_fusion` 与 weight 加权）→ https://indonesia.tencentcloud.com/document/product/845/82242
- 判非登记：`knowledge-governance/SKILL.md:226` 已提「RRF 或 LLM reranker 融合」一句，**未给公式/参数/默认漂移/能力面** ⇒ 本轮为参数族与工程判据净新增，非重复。


## 七、判定池偏差与索引新鲜度（2026-11-11 r736A 独立实拉 · KI）

> 与 §五 RRF 的分工：§五管「多路结果怎么融合成一个排序」；本节管「这个排序的分数本身可不可信」与「刚写进去的资料为什么查不到」。两条轴正交，结论不复用。与 `engineering/wb-agent-evaluation` r702B「Precision@5/nDCG@5 只在判定池内有效」分工：那条是一句判非登记，本节给出可量化的 Hole@10、补标实验、二元退化与冷索引刷新机制。

### r736A-1 ★未判定 ≠ 不相关：评测集本身带着建池检索器的偏见

- BEIR（arXiv 2104.08663v4）§6 逐字：「it is impossible to manually annotate the relevance for all (query, document)-pairs. Instead, existing retrieval methods are used to get a pool of candidate documents which are then marked for their relevance. **All other unseen documents are assumed to be irrelevant.**」「A new retrieval system might retrieve vastly different results than the system used for the annotation. **These hits are automatically assumed to be irrelevant.**」
- 量化实证（Table 4，TREC-COVID Hole@10 = 各系统 top-10 中标注员没见过的比例）：BM25 **6.4%** / docT5query **2.8%**，而稠密检索 ANCE **14.4%** / TAS-B **31.8%**；人工补标 980 对 query-doc 后，docT5query 0.713→0.714 几乎不动，ANCE **0.654→0.735**（从略低于 BM25 变成领先 6.7 分），ColBERT 0.677→0.735。论文结论：「Better datasets, that use **diverse pooling strategies**, are needed for a fair evaluation of retrieval approaches.」
- 判据：① 换召回策略/换 embedding/加语义检索之后，**不能拿旧 qrels 的 nDCG 直接判优劣**——新系统命中越多「池外文档」，被系统性低估越多；② 评测报告必须带 **Hole@10 或等价的未判定率**，且判定池要覆盖所有参评系统的 top-k；③ 本机自建小评测集若只用当前一路（如字面 Grep）产出候选，等于把「字面偏见」固化进标尺，须至少混入向量路/人工补标；④ 与 §三「结果可溯源」互补：溯源证明命中来自哪，本节证明「没命中」不等于「不存在」。

### r736A-2 ★二元判定 + 跨库宏平均：一个总分同时抹平两种差异

- BEIR 18 个数据集的相关形态差异极大（NQ 每 query 单篇相关 vs TREC-COVID 上百篇），故 recall@10 不可跨库比较，headline 取 nDCG@10 按 query 的 ideal DCG 归一化；但标签是**二元**相关，nDCG 设计的 graded relevance 退化为同权——「全面回答」与「顺带提一个词」拿同样分。18 集宏平均把不同任务等权相加，会掩盖单域（生物医学/短 query）的严重崩塌。ZeroEntropy 用 0–10 三评委重标 28 个 MTEB 检索集后排行榜明显重排（商业机构立场，仅作现象佐证，不当方法论源）。
- 判据：① **分库分桶报分**，禁止只报一个平均 nDCG 当上线依据；② 报分同时声明判定粒度（binary / graded）与每 query 相关篇数分布；③ 单库内比较优先用同题集配对检验，而非跨库均值；④ 与前条合起来是「评测有效性双门」：先看判定池覆不覆盖，再看指标配不配题型。与 `engineering/wb-agent-evaluation` r735A 的 SRM（实验分流是否可信）分工：那边管对照组有没有被污染，本节管标尺本身认不认得新答案。

### r736A-3 ★可查 ≠ 已落盘，且冷索引不会自动变新鲜

- Elastic 官方《Near real-time search》逐字：「A refresh makes all operations performed on an index since the last refresh **available for search**.」新段先写进 filesystem cache 并打开即可被搜，**没有 fsync**；持久化由 flush / translog 承担（2.x《Making Changes Persistent》逐字：「we still need to do full commits regularly to make sure that we can recover from failure」「The translog provides a persistent record of all operations that have not yet been flushed to disk」）。current 文档另给一条易漏条件：「By default, Elasticsearch periodically refreshes indices every second, **but only on indices that have received one search request or more in the last 30 seconds**.」
- 判据：① 「刚写入查不到」有**两个独立成因**——尚未 refresh（可见性）与冷索引压根没在自动刷新（30 秒无搜索），不要把两者都当成写入失败；② 验收要**分两点**：可检索（显式 `_refresh` / `?refresh`）与可恢复（flush / translog / 快照），通过前者不等于通过后者；③ 批量重建索引时可临时 `refresh_interval: -1` 提速，但**完成必须显式恢复并 refresh**，否则索引长期不可见；④ 本机语义检索同理：增量建库后先核「索引时间戳 + 条目数 + 一次抽样查询」三件套，不要凭「写入脚本 exit 0」宣布索引新鲜。

**提升层**：可复用 Skill（检索评测有效性）/ 工作流（索引重建验收链）。触发词：Hole@10、判定池、diverse pooling、标注选择偏差、未判定即不相关、补标、二元标签退化、graded relevance、宏平均掩盖、nDCG@10、可查不等于落盘、refresh vs flush、translog、30 秒冷索引、refresh_interval -1、索引新鲜度。

### r736A 来源与判非（独立实拉，2026-11-11）

- arXiv 2104.08663v4《BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models》§6 全文 HTML 一手 WebFetch 200 逐字（提交 2021-04-17 / v4 2021-10-21，NeurIPS 2021 Datasets & Benchmarks）→ https://arxiv.org/html/2104.08663v4 ；摘要页 → https://arxiv.org/abs/2104.08663
- Elastic Docs current《Near real-time search》一手 WebFetch 200 逐字 → https://www.elastic.co/docs/manage-data/data-store/near-real-time-search
- Elastic 2.x《Making Changes Persistent》(translog) 与《Near Real-Time Search》→ https://www.elastic.co/guide/en/elasticsearch/guide/2.x/translog.html · https://www.elastic.co/guide/en/elasticsearch/guide/2.x/near-real-time.html （**2.x 已 EOL 文档，官方页自带警告**；仅用于 refresh/flush 机制说明，参数默认值以 current 为准）
- ChrisWirz《A review of BEIR》→ https://www.chriswirz.com/natural-language-processing/beir-a-heterogeneous-benchmark-for-zero-shot-evaluation-of-information-retrieval/index.html （独立域交叉：512 word-pieces 截断、多数模型共用 MS MARCO 训练数据、跨库等权平均的混淆）
- zeroentropy.dev《BEIR Benchmark》→ https://zeroentropy.dev/concepts/beir-benchmark/ （商业rerank厂商，binary-label 重排现象仅作佐证，**立场已登记**）
- CSDN BEIR 中文译解 → https://blog.csdn.net/zag666/article/details/128336349 （中文交叉，非一手）
- 判重：`Hole@10` / `annotation selection bias` / `graded relevance` / `macro-average` / `near real-time` / `translog` 全库 SKILL.md **0 命中**；`nDCG` 4 命中均为指标名列举或 reranker 选型（`wb-context-compressor`、`wb-agent-evaluation` r702B、`wb-execute-discipline`），无判定池偏差机制；`refresh_interval` 唯一命中在 `agent/agent-guild` 讲的是缓存过期（同名不同义）；`fsync` 唯一命中在 `wb-execute-discipline` 讲 checkpoint 崩溃安全写（豆包自留地，WB 0 落地）。⇒ 净新，取「优＝加厚现有」不新建。
- 未采纳：BEIR 的模型优劣结论（会过时）；2.x 的具体默认参数（以 current 为准）；ZeroEntropy 自家 leaderboard 排名（商业立场）。r735A 的 SRM / r702B 的判定池一句 / r732A 的 RRF 参数族结论一律不复用。
