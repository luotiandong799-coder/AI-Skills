# r252-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（agent memory/orchestration 面） | ✓ | Agent 节点：Max Iterations 安全上限（简单 3-5，复杂研究 10-15）；Memory=TokenBufferMemory 窗口（大窗口上下文多但 token 贵）；Tool Parameter Auto-Generation；两种记忆：会话短期 TokenBufferMemory/长期 Knowledge Base+vector DB；Window Size 50-100 起步；API 调用始终传 conversation_id 保持连续性；1.0+ 长期记忆三能力：自动记忆（AI 提取关键事实）/手动记忆（开发者显式写）/记忆检索（语义相似）+记忆过期 TTL；生产架构 Redis 热数据（LRU 1h TTL）+PostgreSQL 持久化+滑窗上下文摘要；Hindsight 插件 Retain/Recall/Reflect 三工具（跨 run 长期记忆）；MemOS 插件自动保存记忆（交互后存事实摘要+偏好，检索增强个性化） |
| 2 | n8n（RAG 面） | ✓ | 本地 RAG：Ollama nomic-embed-text + Qdrant（递归字符分块 overlapping）；混合检索：Qdrant 768 维 dense + BM25 sparse vector 字段（hybrid RAG over PDFs，per-point BM25 payload）；知识保鲜：scheduled trigger 查 Google Sheet 标记 deleted 记录→从 Supabase vector store 移除+删 Drive 文件；参数实践：chunk 1000 字符+100 重叠；上传 <10MB 防解析超时；query flow 缓存检查；MongoDB Atlas vector index 名 data_index 必须匹配；Supabase pgvector match 函数名匹配；Ollama mxbai-embed 本地嵌入 |
| 3 | LangFlow（memory 面） | ✓ | Memory Base=per-flow vector store（自动摄取会话消息；跨 session 持久；语义检索最相关上下文而非最近消息——区别于 Message History 时间顺序从 messages 表取、区别于手工填充的 knowledge base）；Message History 组件（存储/检索 chat memory；Langflow storage 或 Mem0/Redis 专用 chat memory DB；Agent 组件内置 chat memory 默认启用多数场景够用；sessionID 过滤参数 GET /v1/messages）；1.10 DB Providers 可配置向量后端+多语言；LangChain vector store 实例驱动（RedisVectorStore/ValkeyVectorStore FT. 等 provider 参数） |
| 4 | Activepieces（AI agent builder/copilot 面） | ✓ | AI-first：平实语言给任务（无需 prompt 工程）；agent 自己定步骤/顺序/开什么；工具=已连接 app+任意 MCP server；Approval gates（钱/客户/生产步骤挂闸）；AI Agent Builder：设定目标+选 app/flows/files 权限；admin 一次配 provider（你的模型你的 key）；Flow Builder 多 agent（设角色/传数据/连接 app 单 flow）；SDK 自定义 agent；从句子建 agent（"summarise my unread emails every morning"→草稿 agent：名字/指令/工具）；agent 从"flow step 设置包"变"可命名/可对话/可复用"实体；工具添加 From Piece 或 From Flow（现有 workflow 转可调工具）；chat 界面立即测；AI piece MIT 开源 760+ 集成 |
| 5 | Make（branching/error 面） | ✓ | LangGraph conditional routing 纪律：纯 router 函数返回 path key；path keys 映射 node/END；显式 path maps 胜过散落 magic strings；unexpected router output 加 default/fallback path；table-driven 单元测试每 branch；router 返回字符串必须对应 conditional_edges key 否则 KeyError；重试决策函数（output→success/retry_count<3→retry 循环/failed→error_handler）；n8n AI Fallback Router（validation_status passed/failed→主 workflow 传对象给 fallback router 避免双重花费）；Make incomplete executions：retry 从报错模块用原始输入开始，但 run 可能被 reorder（社区 2025-01 未答复） |
| 6 | Pipedream（secrets/env 面） | ✓ | 加密：OAuth grants/key credentials/env vars 静态加密（AWS KMS AES-256 GCM；私有网络 DB；备份加密）；SOC 2 Type 2；secrets 最佳实践：connected accounts（Pipedream 集成 app）或 environment variables；不硬编码 API key 进 code step；process.env.VARIABLE_NAME；env 两级：Project variables（项目内）+Workspace variables（跨项目）；Project secret 值加密 UI 不可读；组件里 env 变量不可直接访问（sources 用 secret props；actions 用 object explorer 选变量）；外部凭据运行时：Vault/AWS Secrets Manager/Nango；MCP 连接（凭据隔离/不对 AI 模型和客户端暴露/可撤销） |
| 7 | Claude Code（subagents 面） | ✓ | Skills vs prompts/Projects/MCP/subagents 对比；subagent 可用 Skills（python-developer 用 pandas-analysis Skill）；三形态：fan-out/fan-in（parent 并行 N 等全部合成——研究/多文件分析/并行 review）/pipeline（A 输出作 B 输入——research→plan→execute）/background；orchestrator 循环：分析任务→识别子任务→构造 Agent tool call（详细 prompt）→执行→返回→synthesize 检查正确性→finalize 或再 spawn；子代理特性：独立生命周期/隔离上下文窗口/可配置能力；动态选择 description 具体+面向动作；故障：step budget 显式限制（"no more than 20 tool calls"）+Agent View 监控；merge conflicts 前 file-level dependency analysis（列出每个子任务触碰文件验证无重叠）；tool-calling 每轮并行天花板 vs code-execution 递归 harness（Task() 脚本可发上千 subagent） |
| 8 | skills.sh（CLI 安装面） | ✓ | skills CLI：npx skills add <owner>/<skill-name>（无需安装）；--skill 指定具体（npx skills add vercel-labs/agent-skills --skill vercel）；支持 18+ agents（Cline/Windsurf/GitHub Copilot 等）；GitHub CLI v2.90+：gh skill install github/awesome-copilot；@tag 指定版本（gh skill install github/awesome-copilot documentation-writer@v1）；阿里云 SkillsPortal：Skills CLI（通用多 agent）或 ClawHub CLI（OpenClaw 专属）；范围=当前项目（可随项目提交 Git，安装路径项目根目录）或全局；localskills：localskills install <slug> --target cursor claude --project --symlink（平台/范围/安装方法选择可跳过）；Databricks aitools CLI 自动检测支持的 coding agents 安装 skills |
| 9 | deeplearning.ai（RAG/agentic 课程面） | ✓ | RAG 课程（Zain Hasan，24h33m，49 视频 9 代码 10 作业，PRO）；Agentic RAG with LlamaIndex（router→工具使用→推理决策；最简单=router 两选一）；新课程信号：Knowledge Graphs for RAG/Long-Term Agentic Memory With LangGraph（LangMem 记忆管理）/Evaluating AI Agents（metrics/error analysis/production deployment）/Voice for AI Agents（三种集成模式 embedded/layered/callable tool）/Spec-Driven Development with Coding Agents/A2A；Agentic AI 课程：reflection/tool use/planning/multi-agent workflows |
| 10 | WaytoAGI（RAG/知识库面） | ✓ | WayToAGI 知识库用法（从下往上看；Agent 板块快闪共学；知识库访问权限/智能体接收文档）；知识库接入 deepseek 教程（模型 API 调用/API key 位置/创建 RAG 应用/上传非结构化文件/数据解析/切分段落）；RAG 语音 agent prompt 纪律（只用检索上下文回答；1-2 短句口语；每个事实声明加 [chunk_id] 引用；上下文无答案明说；不编造）；2026 AI Agent 趋势（MCP 标准化/记忆优先设计/Agentic RAG 检索作为推理步骤/Voice-forward 实时流/成本感知架构智能模型路由）；RAG Agent 分类（Observation-based 观察环境/知识密集型 RAG Agent） |

## 判重基准
双键检索（相对 r224-r251C 已落章节）：Dify（r250-C 编排 strategies/r251-A 兼容端点——记忆体系面独有新）；n8n（r251-A AI Assistant/r251-B 时区——RAG 向量面独有新）；LangFlow（r251-B Agent 组件/r251-C 记忆未落——Memory Base 三分类独有）；Claude Code（r250-A 安全/r251-B settings——subagents 编排面独有）；skills.sh（r227-B 规模/r251-A trending——CLI 安装面独有）；deeplearning.ai（r249-C 社区——新课程信号增量合并）；WaytoAGI（r250 未落 RAG 教程——趋势+语音 RAG prompt 纪律增量）。未选素材：Pipedream secrets（r251-A 组件 API 已落部分，KMS/两级 env 增量中等）；Activepieces AI builder（r251-A billing/r251-C worker——builder 面增量中等并入）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify Agent 记忆体系 | TokenBuffer+三能力+TTL+conversation_id | 工作流 | wb-execute-discipline |
| ② n8n RAG 生产实践 | 本地嵌入+混合检索+知识保鲜 | 工作流 | wb-execute-discipline |
| ③ LangFlow Memory Base 三分类 | 语义检索 vs 时间顺序 vs 手工填充 | 工具 | wb-execute-discipline |
| ④ Claude Code subagents 三形态 | fan-out/pipeline/编排循环+依赖分析 | 工作流 | wb-execute-discipline |
| ⑤ skills 安装 CLI 生态 | npx/gh/databricks/localskills | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
