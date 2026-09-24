# r170-A Agentic RAG：检索质量自评、三级纠错路由与指标诊断分工

实拉时间：2026-09-24 19:49
信源（10 站/组）：rapidclaw.dev / jvoltci mosaic / futureagi / openlegion / marsdevs / zylos / essamamdani / elegantsoftwaresolutions / 腾讯云 techpedia / genai4a11（Agentic RAG 模式组）；vucense / docs.ragas.io / invra / qaskills.sh / arXiv 2607.14400 / 腾讯云 article / sukruyusufkaya（RAGAS 评估组）；aiwiki / superteams / iotdigitaltwinplm / npblue / arXiv 2401.15884 / deepwiki NirDiamant / arXiv 2603.16169（CRAG 组）；pavlo.sh / infoservices / chenk.top / krunalkanojiya / ragaboutit / mudassirkhan / digitalocean / superml / iitsnl / ailearningguides（生产失败模式组）

## 实拉证据（关键原文）
- CRAG 原文 arXiv 2401.15884：Correct（≥τ+）→ decompose-then-recompose 提炼内部知识；Incorrect（全部 <τ-）→ 丢弃本地结果转 web search；Ambiguous → 内外合并。复现 arXiv 2603.16169 确认阈值按数据集调：PopQA 0.59/-0.99、PubHealth·ARC 0.50/-0.91、Biography 0.95/-0.91——下限阈值接近 -1，意味着"几乎从来不是全错"，大量 case 落 Ambiguous 走 hybrid。
- RAGAS 分工（invra/qaskills/腾讯云）：Faithfulness=答案论断被上下文支持的比例；Context Precision=相关 chunk 是否排前面（LLM 有 recency/primacy 效应，排第 4-5 位等于没召回）；Faithfulness 低+retrieval 好 = generation prompt 没限死"只从上下文答"，模型在用 parametric memory——改 prompt 不改检索。
- arXiv 2607.14400：前沿模型会**正确识别相关文档但生成时不用**（correctly identify relevant documents without using their context）——只测检索准确率不够，必须测"生成时到底用了没"。
- 生产模式（pavlo/mudassirkhan/ailearningguides）：两阶段 vector top-20→cross-encoder rerank→留 top 3-5（端到端质量 +15-30%）；hybrid BM25+vector+RRF+reranker 比纯 vector 错误率降 ~69%；embedding drift——语料格式变了旧 embedding 邻域失效，每月 held-out 集重测、MTEB 漂移 >5% 就重新 embed；冲突源（旧政策 vs 新政策同时召回）要让模型**暴露冲突而非静默选一个自信输出**。
- Agentic RAG 工具纪律（elegantsoftwaresolutions）：3-5 个聚焦工具起步、tool 描述要具体（"Search company policies and HR documents" 而非 "Search internal docs"）、iteration 上限 5-7 次、必须有 "give up" 分支。

## 独点清单（3 个真独点）

### 独点1：CRAG 三级路由——检索结果先过轻量自评，再决定用/弃/补（工作流层）
- 判据：检索后、生成前插一个**轻量** evaluator（不是生成大模型本身）给每个 chunk 打置信分。Correct 用本地、Incorrect 全丢转外部搜索、Ambiguous 内外合并。
- 独有增量（与已有"工具结果断言层"区别）：那条管工具返回值合不合理，本条管**检索结果值不值得喂给生成**——naive RAG 不管检索到的是什么都生成，CRAG 显式回答"这次本地库有没有货"。
- 阈值按数据集调，别拍 0.5/0.7 常数；下限阈值可以极低（论文里接近 -1），意味着"全错"是少数，大量走 hybrid。
- 提升层：工作流（RAG 管线）。

### 独点2：RAG 指标诊断分工——哪个分低修哪端，别一上来全改（可复用 Skill 层）
- 判据：Faithfulness 低但 context_recall/precision 都好 = 生成端问题（prompt 没锁死"只从上下文答"），改 prompt；Context Precision 低 = 相关 chunk 排太后，加 cross-encoder rerank；Context Recall 低 = 检索端漏召回，改 chunk/embedding/hybrid。
- 独有增量：前沿模型会"找对了文档但生成时不用"（arXiv 2607.14400）——检索准确率高 ≠ 答案用了上下文，要加"引用忠实度"指标而不是只看 top-k。
- 与 r167 chunking 互补：那条管怎么切 chunk，本条管切完之后怎么定位是哪端坏了。
- 提升层：可复用 Skill（评估诊断）。

### 独点3：冲突源暴露纪律 + embedding drift 月度重测（工作流层）
- 判据：检索结果里新旧政策/草稿/定稿同时出现时，prompt 要让模型**列出冲突**而不是静默选一个自信输出；embedding 不是一次永久——语料格式/词汇变了，每月 held-out 集重测检索质量，漂移 >5% 重新 embed。
- 独有增量（与已有 RAG 条目区别）：chunk/retrieval 类已有条目管"怎么召得准"，本条管两个生产期问题——召回来的东西互相打架怎么办、embedding 怎么知道过期了。
- 提升层：工作流（运维纪律）。

## 判非重复理由
- r167 已覆盖 RAG chunking/chunk 大小；r168-B 已覆盖 golden task 回归/成本监控。本条 3 独点分别落在检索后自评路由、指标诊断分工、生产期 drift/冲突治理，与已有条目增量 >40%。
- HyDE/step-back/sub-query decomposition/graphRAG 属经典模式，多源重叠 >60% 不落，只留证据。
