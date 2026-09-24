# r167-C RAG 检索质量与 Chunking 工程实践（2026-09-24）

来源：Future AGI 2026-05-14 / arXiv 2608.00824 / n8n blog 2026-08-06 / pavlo.sh 2026-04-21 / Hooman Digital 2026-04-24 / Tensoria 2026-05-15 / Redis blog 2026-07-21 / Rag About It 2026-05-31 / Saram Consulting 2026-07-08 / DEV 2026-06-13 / Collabnix 2026-07-22 实拉。

## 独点 1：Chunking 四策略按文档类型选 + title-chain prefixing 零 LLM 提升 MRR@5 +23.8%（提升层：可复用 Skill）
- **Fixed-size**（N token + M overlap）：简单，prose 可用；结构化文档（表格被切、代码块断）直接崩。
- **Semantic chunking**：每句 embedding，相邻句余弦相似度降阈即切；建索引贵 5-20x，混合主题文档大胜、长而连贯的文档边际收益小。
- **Structural chunking**：按标题/段落/表格/代码块边界切，技术文档最佳。
- **Title-chain prefixing（零 LLM 提升）**：复用文档自身标题层级做 chunk prefix（"章节A > 子节B > 小节C"），不调 LLM 生成摘要；1600 query 生产 Markdown 库评测上 MRR@5 从 0.374→0.463（+23.8%）。
- 判据：**没有万能 chunk size**——关注"每个 chunk 能否独立回答一个问题"；重要信息被切到两个 chunk = 边界要调，不是 size 问题。
- 判非重复：现有 wb-context-compressor 讲"怎么压对话历史"，本条讲"知识库文档怎么切分入库"——正交。

## 独点 2：两阶段检索（recall 宽→rerank 准）+ hybrid BM25/vector 是 production 标配（提升层：可复用 Skill / 工作流）
- **Stage 1 recall（宽）**：vector top 50 + BM25 top 50，RRF（Reciprocal Rank Fusion）融合去重。
- **Stage 2 precision（准）**：cross-encoder reranker 对 query+doc pair 重排，取 top 5 喂给 LLM。
- **数据**：23,088 query 金融 benchmark 上加 reranker 是单项最大提升——MRR@3 +17.2、Recall@5 +12.1。
- **精确匹配查询占技术文档生产流量 20-40%**（API 名/错误码/SKU/合同编号）——纯 dense vector 对这类 exact match 召回失败，必须 BM25 补。
- **四个失败模式对照修复**：rare-token recall ceiling→加 BM25；lost in the middle→rerank+trim；position bias（chunk 在第 1 位被过度引用）→rerank 把最相关放第一；lexical-semantic mismatch→融合两路。
- 判据：**recall 和 precision 用不同工具**——vector 管语义召回，BM25 管精确词，reranker 管最终排序；三者不是替代是流水线。
- 判非重复：r166C 落了 eval/trace/judge，本条讲检索本身的两阶段流水线——正交。

## 独点 3：GraphRAG 按 query 路由，不是替代是升级（提升层：可复用 Skill）
- **GraphRAG 在多跳问题上准确率 3x**；entity hallucination 从 8.7%→1.2%；Microsoft 分层社区方法在多跳/关系问题上 86% vs vector RAG 32%（+54pp）。
- **降幻觉机制**：图里 Entity A 不连 Entity B，模型在检索阶段就不能"发明"连接——确定性 grounding vs 概率性"语义 vibes"。
- **但不是替代 naive RAG，是按 query 路由**：单跳事实查询用 vector RAG 足够便宜；需要跨文档链式推理（"哪个 SOP 因设备 X 偏差更新了"）才走 GraphRAG。两者互补，生产系统按 query 特征动态路由。
- 判据：**先问"答案需要跨文档链式推理吗"**——不需要就别上 GraphRAG，建图贵且维护重；需要再上。
- 判非重复：r167-A 落了记忆三范式选择（Mem0/Letta/Zep），本条讲检索架构选择（naive vector / hybrid / GraphRAG）——Zep 是时序记忆图，GraphRAG 是知识库关系图，场景不同不重叠。