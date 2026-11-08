---
name: local-semantic-search
description: >-
  本地语义搜索：在个人电脑上按「意图」而非关键词找内容。覆盖本地文件搜索、PDF 搜索、工作资料查找、历史记录检索、图片与文档关联搜索。核心是理解用户需求后找到相关内容，而非字符串匹配。当用户要在本机找资料、搜历史对话/文档、按意思查文件、跨 PDF 与笔记关联检索时使用。触发词：帮我找、本地搜索、搜一下我的、按意思搜、相关文件、历史记录里、之前那个文档、跨资料检索、语义搜索、找讲过的内容。不适用：联网全网搜索（走 web-scrape/agent-reach）、精确文件名查找（用 Glob/Grep）。
version: 1.1.0
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
