# r243-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（提示/模型管理面） | ✓ | Prompt 接口按模型类型适配（chat models 用 message roles System 行为/User 输入/Assistant 示例；completion models 纯文本续写）；变量双花括号引用 {{variable_name}} 到模型前替换；Agent node 工具引导（模型基于每 query 动态决定何时用哪个工具，更精确引导在 prompt 里点名工具名+描述何时用）；Dify tools 扩展 agent（实时数据/网络搜索/查询数据库） |
| 2 | n8n（数据转换/子工作流面） | ✓ | LLM 输出当 untrusted input（agent/LLM 节点后接 tiny Code node 三件事：去 fence+前言，从第一个 { 或 [ 到最后匹配 } 或 ] 取子串再解析）；Webhook payload 单点归一化（不在 raw payload 上分支，Webhook 后单个 Code node 归一化到固定 schema，防御性读 key，schema shift 只碰这一个 node）；Continue on Fail（HTTP Request 开启防单失败杀整个执行，输出含 $error 字段供下一节点决定）；Error Workflow（Settings 捕获未处理失败 log 到 DB；AI-powered error workflow Error Trigger→LangChain Agent 深分析根因/方案/影响/紧急度）；Retry+Exponential Backoff 处理超载 API |
| 3 | LangFlow（向量库/RAG 面） | ✓ | Knowledge base 不每次 flow run 重摄取（预摄取一次更高效，默认本地 Chroma 可配外部 provider Chroma Cloud/OpenSearch/PGVector）；Memory base vs Message History（memory base 消息嵌入 vector store 按语义相似度检索最相关上下文而非最近消息；Message History 按时间顺序）；Multi-vector retrieval 1.11.0（lfx-nextplaid 扩展 bundle ColBERT-style late interaction+ColPali-style 视觉文档检索）；避免传整个 raw 搜索结果给 LLM（retriever 解析搜索结果再传） |
| 4 | Activepieces（flow 结构/逻辑面） | ✓ | MCP tools（ap_add_branch 给 router step 加条件分支插入在 fallback Otherwise 前；ap_flow_structure 看现有分支条件和索引）；Branch/loop 处理 AI 可变输出（builders 基于模型响应定义特定路径；code steps 转换非结构化文本为格式化数据）；AI 工作流人工复核阶段（AI 输出暂停验证再继续，确保与运营标准对齐再执行）；Steps 定位（stepLocationRelativeToNewParent AFTER/INSIDE_LOOP/INSIDE_BRANCH+branchIndex） |
| 5 | Make（数据转换/IML 面） | ✓ | IML 函数变 standalone modules（Make Functions app 把之前只在 mapping 字段内用的 IML 函数转成可视化模块，链式步骤数据转换工作流复杂逻辑可读可维护无需嵌套代码）；空输入安全（空/null/missing 值输出空结果不停止 scenario）；Array 函数（contains/deduplicate/distinct key 参数访问复杂对象属性点符号嵌套/数组第一项 index 1/first/last/map/get）；Iterator/Aggregator（数组转 bundle 序列，多数据合一个；iterator 和 aggregator 之间模块输出不可达 aggregator 之外） |
| 6 | Pipedream（调度/触发器面） | ✓ | Cron triggers（invoke workflow on schedule；interval_seconds/cron/timestamp/timezone_configured/timezone_utc 属性）；多触发器限制（不能在一个 workflow 直接用多触发器，用 emitted events 链多个 workflow：listener HTTP/Webhook 触发+emitter 用 emit）；Schedule cron 表达式控制特定星期/天（简单 interval 不能 target 特定星期） |
| 7 | Anthropic（上下文工程/提示面） | ✓ | Prompt caching 两种启用（Automatic caching 顶层 cache_control 自动把 breakpoint 应用到最后一个可缓存块随对话增长前移最佳多轮；Explicit cache breakpoints 放指定块）；缓存成本（reads 0.10× 正常输入价格，writes 1.25× 5m TTL 或 100% 更多 1h TTL；cache_control 放最后一个跨请求一致块绝不放 per-request 变化内容）；1h TTL（document review queues/overnight batch/scheduled jobs 用 anthropic-beta header+cache_control ephemeral，5 分钟不够低频率工作流）；Cache 存 KV cache+cryptographic hashes 不存 raw text（适合 ZDR 型数据保留承诺）；Adaptive thinking（模型动态决定何时多深推理）；Token counting 构建时测防 prompt bloat |
| 8 | skills.sh（生态/目录面） | ✓ | 生态规模格局（AI skills 332,023 项 55.5% > MCP servers 239,448 40.1% > autonomous agents 26,278 4.4%）；目录策展对照（Anthropic official 小手工策展验证/skills.sh 数十万开放 npm-style CLI builder-side auditing/SkillsMP ~190万 scraped 无 review 装前自查/SkillHub 7000+ AI-evaluated/Agensi 小上架前审查 8 点安全扫描）；find-skills 1.3M+ 安装（meta-skill 搜和装其他技能）；兼容 Cursor/Claude Code/GitHub Copilot/Codex/Goose/Windsurf |
| 9 | docs.openclaw.ai（会话/记忆面） | ✓ | Session 两层持久化（session store sessions.json key/value map sessionKey→SessionEntry 小可变安全可编辑 track 元数据；transcript 每会话独立文件）；记忆三层架构（MEMORY.md 每个新 session 加载；daily notes memory/YYYY-MM-DD.md 按需搜索 /new 或 /reset 后重新预载近期；compaction 前 agent flush durable facts 到 daily notes 防长对话静默丢失）；Session end 写入（写短时上下文到 daily log+更新 MEMORY.md 新 durable truths，旧/纠正条目更新或移除）；Honcho memory 插件（跨会话 conversations persist after every turn context 跨 session reset/compaction/channel switch 延续；user modeling 每用户 profile preferences/facts/communication style+agent personality/learned behaviors）；Recall bounded（compaction/provider context/retrieval scope 限制） |
| 10 | GitHub（生态面） | ✓ | agentmemory 9,361★（Persistent Cross-Session Memory for Claude Code 和 16 其他 agents；95.2% R@5 on LongMemEval-S 超 mem0 68.5%/Letta 83.2%；~170K tokens/年 vs paste-full ~19.5M）；addyosmani/agent-skills 85k★（production-grade agent skills 最大趋势）；awesome-mcp-servers 92K★+MCP Python SDK 24K★；memU（Memory for 24/7 Proactive Agents OpenClaw 类）；cognee（Memory for AI Agents in 6 Lines of Code）；Perseus Vault（单 Rust 二进制 durable cross-session memory MCP-native server，一二进制一 SQLite 文件无 Docker/Postgres/cloud，55 MCP tools entity CRUD） |

## 判重基准
双键检索（相对 r241/r242/r243-A/r243-B 已落章节）：Dify（r243-A 落 queue engine/r243-B 落可观测——"工具点名引导"独有增量深化）；n8n（r242-C 落两层错误处理/r243-B 落 RBAC——"LLM 输出规范化+webhook 单点归一化"独有增量深化）；LangFlow（r242-A 落记忆子节点选型/r243-A 落 DevOps——"memory base 语义检索+多向量检索 ColPali"重叠>60% 含≥40% 独有增量合并保留）；Activepieces（r243-B 落 worker 扩展——"AI 输出人工复核门+router 程序化分支"独有增量深化）；Make（r243-B 落触发选型——"IML 函数模块化+空输入安全"独有增量深化）；Pipedream（r242-B 落 trigger 部署/r243-B 落 Actions——"emitted events 链式多触发器"独有增量深化）；Anthropic（r243-A 落 caching 原则/r243-B 落 MCP 安全——"缓存成本模型+位置纪律+1h TTL+不存 raw text"重叠>60% 含独有增量合并保留）；skills.sh（r242-A 落 CLI 纪律/r243-B 落 skills.json——"生态规模格局+目录策展对照"独有增量深化）；openclaw（r242-A 落记忆面/r243-B 落 Gateway——"两层会话持久化+compaction 前 flush durable facts+Honcho 用户建模"独有增量深化）；GitHub（r243-A 落 MemOS——"agentmemory 评测基准 LongMemEval-S+单二进制记忆 server"独有增量深化）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify Agent 工具点名引导 | prompt 里点名工具名+何时用，模型动态决定 | 工作流 | wb-execute-discipline |
| ② n8n LLM 输出规范化 | LLM 输出当 untrusted；去 fence 取子串；webhook 单点归一化 | 工作流 | wb-execute-discipline |
| ③ LangFlow memory base 多向量检索 | 语义检索记忆 vs 时间顺序；ColPali 视觉检索 | 工具 | wb-execute-discipline |
| ④ Prompt caching 成本模型 | reads 0.10×/writes 1.25×；breakpoint 位置；1h TTL | 模型/工作流 | wb-execute-discipline |
| ⑤ agentmemory 评测基准 | LongMemEval-S 95.2% R@5；单二进制记忆 server | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
