# 学习轮 r576C（2026-10-15 · AI 技能库工程与方法论 + AI 智慧进化）

十站实拉（全量逐站，r576 批第 3 轮，角度为上下文管理与记忆工程，与 r576A 评估可观测性、r576B 安全治理错开）：Dify / n8n / LangFlow / Activepieces / Make / Pipedream / Anthropic / skills.sh / GitHub 生态 / deeplearning.ai。判重基准：execute 3.97.0（r576B 3 章）+ compressor 3.694.0（r576B 3 章）+ r576A 6 章 + r575A/B/C 18 章 + r574 批 18 章 + 更早批次 + WB 留痕。

## 落地（execute 3.97.0 → 3.98.0，+3 章）

1. **KV-cache 优化与 observation masking + signal-density test：重排稳定 prompt 复用 KV tensors（最便宜先做）+ 工具输出用后换紧凑引用 + 拒绝"更大窗口解决记忆"**（来源：muratcankoylan《Agent Skills for Context Engineering》context-optimization + context-fundamentals，2026-07-02/10-07）
   - KV-cache 优化（稳定前缀+重排结构，运行时支持前缀缓存时最便宜优化先做）；observation masking（工具输出目的达成后换紧凑引用）
   - signal-density test（处理成本随上下文长度不成比例增长+超有效容量阈值性能退化+长输入即使有前缀缓存仍昂贵）
   - **提升层**：工作流 / 可复用 Skill

2. **渐进压缩与缓存感知：先清工具结果再总结旧对话历史 + compaction fork cached call + cache 隔离粒度变化 + 1M context 模式成本**（来源：Dify 1.17.0 Context Compaction 2026-10-05 + Anthropic《Prompt Caching》2026-10-14/2026-02-05 + Claude《Prompt caching is everything》2026-04-30）
   - 模型感知渐进压缩（Dify 1.17：按有效窗口先工具结果→再总结旧对话）；compaction fork cached call（先缓存再 fork 摘要）
   - 缓存隔离粒度（2026-02-05 workspace 级，Bedrock/Vertex 保持 org 级）；1M context+cache 成本模式（write 1.25x≈$18.75/1M，hit≈$1.5，TTL 5 分钟内多轮才划算）
   - **提升层**：工作流 / 可复用 Skill

3. **Headroom 与上下文压缩层：压缩工具输出/日志/RAG chunks/文件/对话历史 60-95% + 本地可逆 + 50MB 磁盘 1-5ms + tokens-per-task 目标**（来源：GitHub headroomlabs-ai/headroom（74k★ Apache-2.0）+ Developers Digest 2026-06-04 + context-engineering-collection 2026-09-21）
   - 压缩层工具形态（agent↔LLM 之间，60-95% 且不改变答案，本地可逆，50MB+1-5ms）；优化目标=tokens-per-task 非 per-request
   - 结构化分节摘要（files/decisions/next steps 分节保留更多；artifact trail integrity 最弱维度）
   - **提升层**：工具 / 可复用 Skill

## 落地（compressor 3.694.0 → 3.695.0，+3 章）

1. **上下文工程操作清单与触发阈值：monitor token + 去 stale + progressive disclosure + 规划执行分离 + 文件外部化 95% + 阈值 >60-70%**（来源：adaptationio-skrillz《context-engineering》2026-09-27 + LobeHub 2026-09-21 + DEV《Skill Loading, Agent State Bars》2026-09-28）
   - 五任务操作清单；触发阈值 >60-70% 即操作（不是等满）；状态条+按需加载全生命周期协同
   - **提升层**：可复用 Skill

2. **记忆即第一性基础设施：memory=外部模型+持久+结构化 + hot path vs background 双机制 + agent 自编辑记忆（MemGPT 两层级）**（来源：DeepLearning.AI《Agent Memory》2026-07-15 + Scrimba《LLMs as Operating Systems》2026-06-05 + DeepLearning.AI《Long-Term Agentic Memory With LangGraph》2026-04-15）
   - memory=first-class infrastructure（外部/持久/结构化，Oracle AI DB+LangChain+LLM pipelines）；hot path vs background 双写入机制
   - MemGPT 两层级记忆+agent 自编辑（OS 视角）
   - **提升层**：可复用 Skill

3. **SKILL.md 标准采纳与三层渐进加载 + skill induction 与 code knowledge graph：16+ 工具（03/2026）+ 三层省 60-80% 固定上下文 + traces→人批准技能 + 代码知识图谱**（来源：nodemini《2026 Agent Skills Complete Guide》2026-08-23 + CSDN《Agent Skills 三层结构》2026-01-03 + DeepLearning.AI《Building Adaptive AI Agents》2026-09-08）
   - SKILL.md 16+ 工具采纳（Cursor/Claude Code/Codex/Gemini/Copilot/Windsurf/Junie/Kiro/Goose 同一格式）；三层渐进加载（指令→脚本→资源，省 60-80%）
   - skill induction（traces→人批准技能）+code knowledge graph（检索反映真实连线）+持续学习三层（behavior/knowledge/weights）
   - **提升层**：可复用 Skill

## 十站实拉要点（逐站留痕）

- **Dify（上下文记忆角度）**：1.17.0 context-aware compaction（按模型有效 context window 渐进压缩：先清较旧 tool results→必要时总结较旧对话历史，保留近期上下文不撞硬限）；1.12.0 Summary Index（每 chunk 附 summary 字段，语义相关内容一起检索，GraphRAG 轻量替代）；Context Builder token 预估超限自动动态裁剪（按时间倒序保留最新交互优先裁剪历史）；Mem0 客服推荐（Agent 节点 Window Size 50-100 消息+Knowledge Retrieval Hybrid Search TopK 5-10+Score Threshold 0.5）；知识库当长期记忆（写 summaries/facts 进 KB 再检索）；MemGPT 虚拟扩展（conversation variables=core memory）
- **n8n（上下文记忆角度）**：AI Agent Memory 类型（Postgres Chat Memory/Redis Chat Memory 按时间序存对话；Pinecone/Weaviate/Qdrant 向量库存语义/情节记忆按相似度检索）；Context Engineering 博客（IF/Switch 动态上下文选择，按意图/用户类型路由不同检索路径）；长期会话提示（数百条消息终会撞 LLM token 限，用 cron/独立 workflow 定期 prune chat_history 表或清旧会话）；reranking（Cohere rerank 保证最相关记忆进上下文）；Think 工具强制内部推理
- **Langflow（上下文记忆角度）**：Memory bases（1.10：per-flow vector stores 自动摄入会话消息，语义检索跨会话——vs Message History 时间序 vs Knowledge base 文档）；1.11.0 Multi-Vector Retrieval（NextPlaid：ColBERT late interaction+ColPali 视觉文档检索）；1.8 Knowledge bases 本地向量库（数据不需每次远程 re-ingest）；Agent 组件内置 chat memory（同 session ID 关联）
- **Activepieces（上下文记忆角度）**：Built-in Tables 存结构化上下文（conversation state/entity mappings/task history，跨 runs 读写）；thread_id 维护数千独立会话（每用户唯一 thread_id）；人类可暂停执行编辑记忆修错再恢复；Personal AI MCP（Create Memory/Get Conversation History 工具）；GoodMem MCP（记忆）
- **Make（上下文记忆角度）**：Conversation ID 自定义 ID 记住单线程交互（留空=无记忆）；Maximum conversation history 字段限历史；Upsert Agent Context (file)（上传/替换 context 文件，同名替换）；Get Agent Contexts（取回全部 context 文件）；输出含 context window used 指标
- **Pipedream（上下文记忆角度）**：微软 Agent Framework @step decorator（result caching+event emission+per-step checkpointing 每步检查点）；5 文件状态管理（阿里云：dedupe_index.json 幂等去重+execution_log.jsonl 结构化执行日志+handoff.md 任务间上下文传递含前序摘要/关键决策/待办+run_state.json）；DELTAMEM（增量经验记忆 residual trees）；wavemind（SQLite 本地动态记忆+wave-field re-ranking+remember() 显式保存）
- **Anthropic（上下文记忆角度）**：prompt caching（GA 后标准；2026-02-05 起 workspace 级隔离不再 org 级，Bedrock/Vertex 保持 org 级）；Claude Code 教训（compaction fork cached call 摘要对话再 resume，缓存易搞错；5 分钟 TTL）；cache write 1.25x 输入价（5 分钟 TTL）；1M context+cache 模式（首轮 write $18.75/1M，后续 5-10 轮 hit 各 $1.5）；compaction 三模式（on-demand compact-2026-09-04/token threshold/own summarizer）
- **skills.sh（上下文记忆角度）**：context-engineering 技能集（KV-cache 优化：重排稳定 prompt 结构复用 KV tensors，最便宜优化先做；observation masking：工具输出用后换紧凑引用；signal-density test：大窗口≠解药+成本超线性+超容量退化；tokens-per-task 非 per-request；结构化分节摘要 files/decisions/next steps；artifact trail integrity 最弱维度；compaction near limits）；三层渐进加载（Anthropic 指令/脚本/资源，省 60-80% 固定上下文）；SkillRT 编译技能（能力维度测量+环境绑定+并发提取）；16+ 工具支持 SKILL.md（03/2026）；context limits >60-70% 触发操作；state bars 可视化
- **GitHub（上下文记忆角度）**：Headroom（headroomlabs-ai/headroom，74.3k★ Apache-2.0：上下文压缩层，压缩工具输出/日志/RAG chunks/文件/对话历史 60-95%，本地+可逆，50MB 磁盘+1-5ms/请求，Netflix 高级工程师，周增 6k 星）；claude-mem（跨会话持久上下文+AI 压缩，Claude Code/Codex）；Billion-Context（5x token 压缩，100k 窗口处理月长会话）；Reflex Agent（APUS-AI-Lab MIT：模型驱动 harness 无损记忆无限上下文）
- **deeplearning.ai（上下文记忆角度）**：Agent Memory 课程（memory=first-class infrastructure：外部模型+持久+结构化，Oracle AI DB+LangChain+LLM pipelines）；LLMs as Operating Systems（MemGPT 两层级记忆+agent 自编辑记忆，82 分钟免费）；Long-Term Agentic Memory With LangGraph（semantic/episodic/procedural 三类型+hot path/background 双机制+email agent router triage）；Building Adaptive AI Agents（持续学习三层 behavior/knowledge/weights+skill induction pipeline 轨迹→人批准技能+code knowledge graph 检索反映真实连线）

## 功能套件核查（⑦）

三核心套件（wb-ponytail/wb-max-token-saver/wb-context-compressor）本轮无优化升级项；新增章节均标注与既有相邻章节分工边界与触发词（上下文工程定义/缓存成本量化/压缩优先级/压缩后规则重声明/记忆提取四策略/记忆分层/上下文预算管理/大资料拆 supporting files/技能治理/进度流/观察值回收等）。

## 垃圾清理（⑨）

删了什么：本批十站实拉全走 general_search，无本地临时文件落盘、未产生新垃圾。保留什么：*.bak 与全部核心产物（两 SKILL 文件 + r576A/B/C 留痕 + 既往批次留痕）。

## 信源健康度

无删源无加源；Flowise 已删除不拉；十站全部可达，未触发桌面 VPN。commit/push 挂起（git 通道持续不可用，累计 r546→r576C 共 32 批）。
