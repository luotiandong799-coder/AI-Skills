# 2026-10-15 学习轮 r577B：RAG 与知识工程 / 检索增强

主题：AI 技能库工程与方法论 + AI 智慧进化（硬锁）
轮次：r577B（本次触发批 r577 之第 2 轮，共 3 轮连跑）
判重基准：WB r575/r574/r573/r572/r571；doubao r577A（6 章）+ r576A/B/C（18 章）+ r575A/B/C

## 十站实拉（全量逐站，带来源）

| 站 | 实拉要点 | 来源 |
|---|---|---|
| Dify | 多模态检索（图像可搜索/可排名/可作证据）；混合检索+重排 Top1 命中 4/4；parent-child 双层切块（子块单句匹配+父块上下文）；Summary Index（summary 字段随块检索，轻量替代 GraphRAG）；Q&A mode Q-to-Q 策略 | dify.ai/blog + dify 1.16/1.12 + DeepWiki |
| n8n | 切块 500-1000 字符+overlap 10-20%+Recursive splitter；嵌入维度须匹配、插入与检索用同一模型；引用 1-3 个源 URL | n8n vector stores + workflows |
| LangFlow | 多向量检索（ColBERT late interaction+ColPali 视觉文档检索）；DB Providers 可配置向量后端；RAG-as-middleware 解耦 | docs.langflow.org + blog |
| Activepieces | Agent Knowledge：文件切块索引、按需检索（vs 全贴 instructions 每轮全读）；新文件触发自动重索引 | activepieces.com/docs |
| Make | Context 文件上传→切块→向量存 RAG 库→按查询取最相关块（省 token）；embedding tokens+AI tokens 计费 | help.make.com |
| Pipedream | RAGSmith query rewriting/expansion（doc2query/HyDE）；8 RAG patterns（GraphRAG 多跳/混合检索）；diversity-first 上下文选择 | arXiv + DZone |
| Anthropic Skills | Project Knowledge RAG 自动扩容 10x（近上下文上限触发）；解析→语义边界切块→嵌入→索引→检索附来源引用；200K 上下文+prompt caching 改变 RAG 架构 | support.claude.com + claudexia |
| skills.sh | contextual retrieval（context prepending 减 67% 失败+40/60 BM25/向量权重）；Skill-RAG 隐藏态探测+技能路由；SkillSeek 技能检索市场级（39/49 skill 零提升） | lobehub + arXiv |
| GitHub 生态 | ContextEngine Recall@k/MRR/nDCG/Hit@k 检索回归信号；BGE-Reranker-v2-m3/Qwen3-Reranker 开源 top；rerank 提升 15-25% | github + presenc + OSSAlt |
| deeplearning.ai | RAG Triad（Context Relevance/Groundedness/Answer Relevance）；sentence-window/auto-merging 检索；Building Multimodal Search and RAG（contrastive learning 多模态嵌入） | learn.deeplearning.ai |

## 落地（execute 3.99.0→3.100.0 / compressor 3.696.0→3.697.0，各 +3 章）

| 文件 | 新增章节 | 提升层 |
|---|---|---|
| wb-execute-discipline 3.100.0 | RAG 切块参数与双层结构（500-1000 字符/10-20% overlap/递归 splitter；parent-child 双层；summary index 轻量替代 GraphRAG） | 工作流/可复用 Skill |
| wb-execute-discipline 3.100.0 | rerank 成本模型与选型（20-50 候选→cross-encoder→top 3-8；15-25% 提升；BGE/Qwen3；多模态 rerank） | 工具/工作流 |
| wb-execute-discipline 3.100.0 | RAG 评估三件套与排名指标（RAG Triad 定位检索错/幻觉/跑题；Recall@k/MRR/nDCG/Hit@k；RAG-as-middleware 解耦） | 工作流/可复用 Skill |
| wb-context-compressor 3.697.0 | contextual retrieval 与混合检索权重（context prepending 减 67% 失败；40/60 权重；RAG 自动扩容 10x） | 可复用 Skill/工作流 |
| wb-context-compressor 3.697.0 | Q-to-Q 检索与 FAQ 知识库（查询匹配问题；chunk 富化：标题前置+假设性问题 metadata） | 可复用 Skill |
| wb-context-compressor 3.697.0 | diversity-first 上下文选择与上下文预算（多样性优先；保守改写；检索块预算） | 工作流/可复用 Skill |

## 判重说明（增量判定）

六点均含独有增量：切块参数数字（500-1000/10-20%/递归 splitter）与既有 §知识库工程（双路召回/标题分块）互补非重复；parent-child 双层结构与 summary 字段未见于前批；rerank 成本模型（20-50→3-8/15-25% 量化）与 BGE/Qwen3 选型未见于前批；RAG Triad 三指标与排名指标清单未见于前批（r575 评估驱动是 agent eval，Triad 是 RAG eval，独有）；context prepending 减 67% 失败与 40/60 权重在既有双路召回基础上为独有增量（合并保留）；Q-to-Q 检索策略与 chunk 富化未见于前批；diversity-first 与检索块预算未见于前批。

## 功能套件核查（⑦）

wb-ponytail / wb-max-token-saver / wb-context-compressor：本轮 compressor +3 章（contextual retrieval/Q-to-Q/diversity-first）直接增强检索与上下文选择能力；ponytail 与 token-saver 无对应增量，暂不迭代。

## 清理（⑨）

删了什么：无（全程 general_search 实拉，无本地临时文件落盘）。保留什么：*.bak 与全部核心产物（两 SKILL.md + 本留痕）。

## 批内备注

git commit/push 因通道缺失挂起（累计 r546→r577A 共 33 批 + 本批），不重试、不启 VPN、不补推。
