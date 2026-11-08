---
name: research/ki-knowledge-graph
description: 知识图谱 / GraphRAG（Knowledge Intelligence）。当需要从大量文档/语料构建知识图谱、做跨文档多跳问答、全局主题归纳、实体关系推理，或问"GraphRAG 怎么用 / 知识图谱怎么搭 / 文档间关系"时调用。提供 GraphRAG 四阶段（实体关系抽取→Leiden 社区检测→分层社区摘要→local/global 查询）、LightRAG 双层检索与增量更新、图谱何时优于向量 RAG 的判据，以及实体漂移/陈旧图/成本等坑。不用于单点事实查询（向量 RAG 更优）。
module: KI
modules: KI,CI
---

# KI · 知识图谱 / GraphRAG（Knowledge Intelligence）

> 本技能覆盖 Personal AI OS 13 模块中 **KI（知识智能）** 的图谱侧。与 `research/local-semantic-search`（向量检索）互补：向量管"点查/模糊匹配"，图谱管"多跳/跨文档/全局归纳"。
> 方法论实拉自 2026-11-07 WebSearch（真实可核验）：aiwiki.ai/wiki/knowledge-graph（GraphRAG 四阶段/Leiden）、lightrag.github.io（双层检索/增量/去重）、callsphere.ai（GraphRAG vs LightRAG 成本/决策树/坑）、bloss0m.com（query policy/local-global 分工）、lup.lub.lu.se（KG 三元组/LightRAG keyword 双层）。

## 一、何时用（Graph vs Vector 判据）

| 问题形态 | 选 | 理由 |
|---|---|---|
| 单点事实 / 模糊语义匹配（"合同里付款条款是什么"） | **向量 RAG** | 就近块检索最快最省 |
| 跨文档多跳（"这个人→公司→投资人→竞品"链路） | **图谱** | 沿实体关系遍历，块检索拼不出 |
| 全局主题归纳（"这 5000 条评论的主导主题"） | **图谱（GraphRAG global）** | 社区摘要 map-reduce，向量只能取最近邻 |
| 实体约束查询（"X 是否在 Y 的网络内"） | **图谱** | 结构化约束遍历 |
| 混合（多数生产栈） | **向量+图谱，按 query 类型路由** | 各取所长 |

**判据**：需要"跨整份语料归纳"或"多跳关系推理"才上图谱；纯点查上图谱是过度工程。

## 二、GraphRAG 四阶段流水线（Microsoft 路线）

1. **索引（Indexing）**：文档分块 → LLM 抽取（subject, predicate, object）三元组 + 实体描述；实体按嵌入相似度**去重**；边按共现加权。
2. **社区检测**：用 **Leiden 算法**把图划分成密集连通社区（典型语料几十到几百个社区）。
3. **分层摘要**：LLM 为每个社区生成多抽象层级摘要（粗到细的语料地图）。
4. **查询**：全局问题 → 每个社区摘要各出部分答案 → 再 reduce 成总结；局部问题 → 取实体邻域。

**代价**：索引阶段每块多次 LLM 调用，全量 GraphRAG 成本高（实拉：1M token 约 $20–40 @gpt-4o）。

## 三、LightRAG（低成本替代）

- 保留实体/关系抽取，**砍掉昂贵的社区摘要**，改用**双层检索**：低层关键词（具体实体/术语）→ 匹配实体嵌入取邻域；高层关键词（抽象主题）→ 匹配关系嵌入取主题连接；两路合并 + 图扩展。
- 实体/关系各自嵌入，并带 **provenance 回链**到源块（需要原文时可回溯，不必整块检索）。
- **增量更新**：新文档走同样抽取→与旧图合并节点/边，不重建全图。
- 成本对比（实拉）：LightRAG ~$0.50 vs GraphRAG $20–40 / 1M token，质量相当或更好。

## 四、查询策略（当 query policy，不是全局开关）

- GraphRAG：`local`（实体展开）/ `global`（社区摘要 map-reduce）/ `drift`（逐步探索）。
- LightRAG：`naive` / `hybrid`（低+高层关键词）/ `mix`（图上短描述 + 回链原始 chunks）。
- **铁律**：GraphRAG 的 global ≠ "更大的 local"；extractive 精确定值问答用 local/hybrid，别用 global 吃掉细节。

## 五、坑与护栏

- **实体漂移**：同一人变 3 个实体（"Sagar S"/"Sagar Shankaran"）→ 用嵌入 + 别名规则做实体消解（resolution）。
- **陈旧图**：重建贵 → 用增量更新或接受每日刷新；标注图的新鲜度。
- **索引成本**：先小规模试，优先 LightRAG；只在必须社区级推理时才上全量 GraphRAG。
- **问题形态错配**：graph 强在 global/多跳，vector 强在点查；别拿错工具。
- **图不完整**：KG 天生不完整，缺边会导致错误推断；关键结论须回溯源块核验（provenance 回链）。
- **抽取提示词定生死**：实体/关系抽取 prompt 钉死并版本化，它决定整图质量。

## 六、与 OS 协作

- 检索选型与预算 → **CI**（`wb-context-compressor` 的检索降级链）。
- 图谱上的概率/趋势推断 → 委派 **PDI**（`meta/pdi-forecasting`）。
- 图谱结论的事实核验 → **VI**（`engineering/vi-fact-verification`）。
- 图规模大、需分治构建 → **OI/EI** 编排多步抽取流水线。

## 七、来源（2026-11-07 实拉）

- GraphRAG 四阶段 / Leiden / 分层摘要 / global map-reduce：aiwiki.ai/wiki/knowledge-graph
- LightRAG 双层检索 / 增量更新 / 去重 / provenance：lightrag.github.io
- GraphRAG vs LightRAG 成本与决策树 / 实体漂移 / 陈旧图 / 问题形态：callsphere.ai/blog/vw6g-microsoft-graphrag-knowledge-graph-2026
- query policy（local/global/hybrid/mix）非全局开关：bloss0m.com/blog/101-unified-knowledge-graph-rag
- KG 三元组 / LightRAG keyword 双层 / 与向量混合：lup.lub.lu.se/student-papers/record/9239602
## r712C 下沉：建图的三级取证与边级置信——确定性优先、LLM 只碰语义层（来源：GitHub `Graphify-Labs/graphify`·`docs/how-it-works.md` 5,903B + `docs/node-summaries-rfc.md` + `docs/superpowers/specs/2026-05-04-incremental-updates-dedup-design.md`，★144k，2026-11-08 一手实拉）

- **三级取证，按成本从零到贵**：**Pass 1** 用 Tree-sitter 抽类/函数/import/调用图/注释，**纯本地零 API 成本**；**Pass 2** 音视频本地转写（faster-whisper），转写 prompt 用已建图里的 top god nodes 做领域偏置，转写结果缓存；**Pass 3** 只有文档/论文/图片/转写文本才交给 LLM 子代理并行抽 nodes/edges。→ 判据：**代码不进 LLM 语义抽取**——把"结构化能拿到的"交给解析器，把"只有语义能拿到的"才花钱；纯代码语料整个 Pass 3 跳过。
- **每条边必须带取证等级，不许一律平等**：`EXTRACTED`（源码里直接可见：调用/import，置信恒 1.0）/ `INFERRED`（模型推断，带 0–1 分）/ `AMBIGUOUS`（不确定，进报告待人工复核）。INFERRED 用**离散档**而非连续小数：0.95 近确定（显式跨文件引用且目标唯一）/ 0.85 强证据（命名+上下文吻合）/ 0.75 合理（有上下文但不显式）/ 0.65 弱（仅命名相似）/ 0.55 推测。
- **重复证据不丢，压到 `also_seen`**：同一对节点同一关系的多次发现，边只保留**置信最高**的那份，其余每次的 confidence/score/source_file/location 依弱到强列进 `also_seen`。→ 判据：**去重不等于删证据**——保留"还有谁这么说过"，才能事后判断这条边是不是同一来源反复自证。
- **增量靠内容哈希，不靠时间戳**：每个文件按内容 SHA256 指纹，重跑只处理新增/改动文件，缓存落在 `graphify-out/cache/`。→ 判据：**时间戳会骗人（重新 checkout、touch 都改 mtime），内容哈希不会**。
- **结构本身就是相似度信号**：社区发现用 Leiden 按边密度聚类，模型抽出的 `semantically_similar_to` 边直接参与聚类，**不另建 embedding 与向量库**。→ 判据：小语料（6 文件）图的价值是结构清晰不是压缩，语料越大 token 收益才复利（52 文件实测 71.5×）。
