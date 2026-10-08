# 2026-10-08 学习轮 r462B：Text-to-SQL 与结构化数据分析 Agent 2026

轮次：r462B（doubao 侧批 r462 第 2 轮）
判重：双键 grep KB 5225 行 + 留痕 r434~r462A 基线 → 已落相关面：混合检索与重排（r452B）、混合检索 hybrid（r440A/r434B）、RAG 幻觉检测（r452C/r461B）、结构化输出（r453A/r457C）、表格理解与表格驱动 RAG（r386B，仅一句带过）——本主题=**结构化数据库问答的可靠性工程（企业断崖基准口径 / schema 链接即 RAG / 执行前三闸门与只读纵深 / 语义层与证据注入 / EX+VES 双指标与工具选型）**，已落面管"文本怎么检索怎么不幻觉"，本面管"精确计算必须交给 SQL 时怎么让它准、安全、可纠错"，与 452B/461B 重叠<60%，独有增量≥40%，按增量判定落地；净增 5 独点。
实拉：1 query×4 站（aiworkflowlab-text-to-sql-production-2026 / changegamer-text-to-sql-agents / rsl-sql 论文摘要 / longan-csdn-结构化数据问答 + langchain-sql-database-toolkit / llamaindex-nlsql / vanna-ai / MCP-postgres 只读 / Spider / Spider2 / BIRD / BIRD-Interact 官方站，2026-10-08 实拉）；主源 aiworkflowlab 用 WebFetch 取正文返回空，**改 curl 一手抓取（55,983 字节）后逐串命中核验**：85% / 88.3% / 75–82% / 33% / 39.1% / 60.5% / 约 60% 幻觉消除 / 三闸门 EXPLAIN dry-run / semantic layer 全部命中。

## 落地 5 独点（每点标注提升层）

### 1. 企业断崖与基准口径纪律（可复用 Skill/工作流）
来源：aiworkflowlab（curl 一手）/ changegamer / CSDN
- Frontier：Spider 约 85% EX、BIRD 75–82%（人类天花板约 93%）；企业真实库：BIRD-Ent 39.1%、Spider-Ent 60.5%、BIRD-Interact 约 33%（每库约 800 列）；Spider 2.0 最优约 21%，Spider 2.0-Lite 上 GPT-4 级一度约 6%。
- 引用失真注意：同一 Spider 在三个源分别是 85% / 88.3%（Arctic-Text2SQL-R1 on Spider-test）/ ">90%（已成基线）"——引用必须带 benchmark 版本 + harness（呼应 r445C 引用失真审计法）。
- 两条教训：① 换更强底座最多约 +10 分，企业断崖不是模型能力问题；② 公开榜单分数不能当自己库的预期，必须在自己的 schema + 自己的问题集上实测。
- 提升层：可复用 Skill（评测口径纪律）/ 工作流（自测门）。

### 2. Schema 链接即 RAG + RSL-SQL 四段式（工具/工作流）
来源：RSL-SQL 论文摘要 / aiworkflowlab / LangChain / LlamaIndex
- 整库 schema 塞进 prompt = schema noise；改为检索问题：检索相关表列 + 动态 few-shot（3–5 条已验证样例）；喂的是 DDL + 列描述 + 样本行而非表名。
- RSL-SQL：① BSL 双向链接（正向选列 + 反向从草稿 SQL 反解实际用到的列，召回 94% 且输入列减 83%）；② CIA 上下文增强（hints：SQL 关键字/过滤条件/列语义描述）；③ BSS 二元选择（全量版 vs 剪枝版两候选由 LLM judge 比对执行结果，对冲剪枝冒进）；④ MTSC 多轮自纠（报错回喂迭代）。
- 成本证据：同一框架下 DeepSeek（便宜约 215×）BIRD 63.56% 反超若干 GPT-4 系统；GPT-4o 配 RSL-SQL = BIRD 67.21% / Spider 87.9%。
- 风险对称：剪太狠漏必需列 vs schema 太简缺 join/消歧上下文。
- 提升层：工具（检索式 schema 链接）/ 工作流（四段流水线）。

### 3. 执行前三闸门 + 只读纵深护栏（工具/可复用 Skill）
来源：aiworkflowlab（curl 一手）/ changegamer / MCP postgres
- 三闸门：语法 parse → 对目标方言 EXPLAIN dry-run → 数据库角色级只读策略（在 driver/role 层强制，不写在 prompt 里）。
- 纵深四条：拒绝系统目录与敏感表 / 禁止语句堆叠（参数化或 prepared statement，禁止把模型输出当多语句串直接喂驱动）/ 写操作显式人工确认 / 强制 LIMIT。
- 透明性：返回结果必须同时返回生成的 SQL（藏 SQL 的 agent 无法审计错答也发现不了注入）；SQL 日志是 few-shot 与微调的第一手信号源。
- 只读模式也必须用 prepared statement（Datadog 注入案例）。
- 提升层：工具（闸门）/ 可复用 Skill（护栏清单）。

### 4. 语义层与证据注入优先于换模型（可复用 Skill/工作流）
来源：aiworkflowlab（curl 一手）/ CSDN
- 带预定义 metric 的 semantic layer 通过约束"允许算什么"消除约 60% 幻觉。
- 外部知识证据：GPT-4 不喂证据 34.88% → 喂领域提示/值映射/同义词后 54.89%（+近 20pp）。
- 把"退款对应哪张表哪个状态码"这类业务黑话显式喂进去，比升级底座模型更有效。
- schema 装不下时走动态选表引擎（`SQLTableRetrieverQueryEngine` 查询时选表）；`SQLDatabaseToolkit` 提供内省/执行/报错反馈三件套并在连接前收敛到只读凭据。
- 提升层：可复用 Skill（降幻觉手法）/ 工作流（语义层前置）。

### 5. EX + VES 双指标与按场景工具选型（工作流/工具）
来源：aiworkflowlab / changegamer
- 只看 EX 不够：正确结果但全表扫描 = 等待发生的生产事故，必须同时看 Valid Efficiency Score（VES）。
- 选型按场景而非分数：Vanna（RAG 框架，吃 DDL+文档串+已验证样例）=嵌入式开发者工具；Wren AI=受治理的企业 BI（不是同一问题的不同价位）；LangChain/LlamaIndex=自建面；MCP Postgres（参考实现已归档，社区后继 crystaldba/postgres-mcp，全部查询跑 READ ONLY 事务）=只读接入面。
- 榜单进步主要来自多步流水线编排而非单点模型能力（BIRD 约 72% → Gemini-SQL2 80.04% / Agentar-Scale-SQL 81.67%）。
- 提升层：工作流（双指标门）/ 工具（选型映射）。

## 判非不落（给一手依据）
- **Vanna / LlamaIndex / LangChain 的安装与 API 用法**：属工具使用文档，非可复用方法论，落到本技能会稀释，留候选池。
- **BIRD / Spider 榜单逐月排名表**：易过期且非判据，本轮只取方法论层结论（"增益来自多步流水线"）不取排行榜快照。
- **SQL 注入攻防通用面**：已在 r455B 提示注入纵深、r455C/安全面沉淀，重叠 >60%，本轮只新增"数据库面只读 role 层强制 + 禁止语句堆叠 + 只读也要 prepared statement"这三条结构化独有项。

## 落地与版本
- `defaults/wb-context-compressor` 3.420.0 → **3.421.0**；KB 5225 → 5232 行（新增 1 章 5 点）。
- 提升层覆盖：工具 4 / 工作流 5 / 可复用 Skill 3。
