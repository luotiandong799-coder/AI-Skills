# r252-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（RAG/knowledge pipeline 面） | ✓ | Agentic RAG：Agent Node=集中决策引擎（意图分析+工具编排+源选择+重试逻辑）；Qdrant vector+hybrid search/Google Search/custom API 为工具；agent 迭代分析意图/选工具选源/改写查询（区别于 one-shot retrieval-then-generation）；Legal Research Agent 模板：动态选 1-2 个相关 collection，结果不足 fallback Google Search；Knowledge Pipeline：可视化 RAG ETL（源连接/文档解析/chunking 策略逐节点，插件化 text/images/tables/scans）；多模态检索（text+image chunks；LLM Vision 模式+变量聚合节点）；TiDB Vector 分布式向量存储；InfraNodus GraphRAG 外部知识库（刷新延迟显示+测试查询验证）；Tavily live web 知识管线（LLM 提取关键信息生成 Q&A 对）；NVIDIA DGX 私有部署（Ollama/vLLM/TensorRT-LLM 推理层） |
| 2 | n8n（agent memory 面） | ✓ | Simple Memory (Window Buffer)：存最后 N 条消息作上下文；窗口可配；超窗完全遗忘（trade-off）；适用单 agent 对话/支持聊天；memory 节点画布化（AI Agent 连接 memory 子节点：存储方式/持久时长/何时检索或清除可见）；contextWindowLength 默认 10+sessionKey 可改；per-user isolation（Teams channelId 作 session ID）；Data Table 多 session 持久+sliding window last 10 turns；双两层记忆：Layer1 Postgres memoryPostgresChat（custom session key 每用户独立，15 消息窗口即时加载）→ Layer2 pgvector 长期语义；Buffer Window Memory 用 webhook timestamp 作 session ID；context engineering（memory backends/context window thresholds/retrieval timing/tool-call scopes 可配节点） |
| 3 | LangFlow（testing/export 面） | ✓ | Playground：运行流/对话/查看输入输出/实时修改 LLM 记忆微调响应；编辑或删除 message log 单条消息/删除整个 chat session 影响后续行为；Import/export：项目页导出/Share 导出/API /flows/download 导出项目备份；Traces：记录详细执行 traces（debug/延迟/token 用量）无需外部 observability；Flow Activity 页每次 run 一个 trace（span 链）；按 session/status/时间排序；下载 JSON；Flow DevOps SDK（1.9）：lfx validate 本地验证 flow JSON 再推送/版本化/测试/终端部署；flow version history：点时间版本/只读预览/恢复早期版本；A2A server：发布 flow 作 A2A endpoint 测试 |
| 4 | Activepieces（MCP 面） | ✓ | 内置 MCP server：URL 加进 MCP client config，OAuth 浏览器认证；连接 Claude/Cursor/Codex 任一 MCP client 驱动整个平台；self-host 支持（连接和数据留自己环境，host root 或 reverse-proxy 子路径）；763/760+ apps 单 URL 全暴露；MCP in 3 steps：UI 连接工具→加 Server URL 到 Claude/Cursor/Windsurf→让 AI 做；AI-ready pieces：ap_search_actions 按任务搜索动作（不是按名字）→inspect schema→run；280+ open source MCPs（self-host 或 cloud）；数据 masking：敏感细节不出现在 logs；AI agents 经 MCP 调暴露工具和工作流（结构化输入 lookup/create tickets） |
| 5 | Make（webhooks 面） | ✓ | 自定义 webhook 模块：生成唯一 webhook URL；每场景自己的 webhook，不能多个场景共用同一 webhook（一个 webhook 只能用于一个场景，创建新场景需新建 webhook）；GET 请求数据交换：Webhook response 模块返回 200+body 映射 JSON；headers 设 content-type: application/json |
| 6 | Pipedream（OAuth/connected accounts 面） | ✓ | Connect token 4 小时过期；tokenCallback 自动向 backend 取新 token（不自己管过期）；Managed auth：托管 OAuth 客户端/安全 token 存储/自动 refresh；可带自己的 OAuth client；凭据静态加密；2,400+ APIs；免费 1000 connected accounts；REST API client credentials 模型（OAuth client ID+secret 换 access token）；SDK 自动刷新 token；两类 OAuth app：key-based（静态凭据，加密存储经 API 暴露）/OAuth（Pipedream 管 flow 保证 fresh token）；Access token 1 小时过期可随时 revoke |
| 7 | Claude Code（memory 面） | ✓ | Managed Agents session 默认 fresh context；memory store 跨 session（用户偏好/项目约定/先前错误/领域上下文）；Auto Memory（v2.1.59+）：Claude Code 默认写 MEMORY.md；首个 200 行或 25KB 会话开始加载；三层：CLAUDE.md（显式项目记忆，root 加载，跨 session/成员轮换/repo clone 存活，层级机制大仓库重要）→ Auto Memory MEMORY.md（隐式学习层，会话中自主发现写回）→ Memory Tool（API 层，长运行程序化 agent）；记忆不跨工具/repo/团队（Mem0 补）；4 patterns：CLAUDE.md 分层/hooks SessionStart/claude-mem（capture-compress-replay）/graphify（knowledge graph 可查询）；1M context GA（Opus 4.6/Sonnet 4.6 标准定价无倍数） |
| 8 | SkillsMP（marketplace 面） | ✓ | SkillsMP：2,154,976 collected SKILL.md files；built around open SKILL.md；支持 Claude Code/Codex CLI/ChatGPT；搜索关键词+检查 GitHub 源+比较；分类目录（content-creation/sales-marketing/data AI/DevOps/testing）；目录信号：categories/GitHub stars/source recency 排序——"不是背书/质量认证/安全审查/匹配保证"，用前 inspect source；发布路径：publish skill 到 Skillstore/SkillMap 等（audit public safety/build public package/create GitHub repo/submit repo URL to intake endpoints）；社区技能例：learning-data-collection（train/val/test split+normalize schemas+metadata，npx skills add 安装） |
| 9 | OpenClaw（memory 面） | ✓ | 文件式记忆：plain Markdown 在 workspace（~/.openclaw/workspace）；模型只记落盘内容无隐藏状态；MEMORY.md 长期（会话开始加载，持久事实/偏好/决策）+memory/YYYY-MM-DD.md 每日笔记；提取整合：agent 从每日笔记提炼到 MEMORY.md+删除过时长期条目（workspace instructions+Heartbeat 定期做，不手动编辑）；memory-wiki 插件（原始笔记变维护的知识库）；分层次：plain files+one SQLite index；不同 trust levels/write rules/injection behavior；durable memory 唯一主写入者=dreaming consolidation pass；防御 junk/poisoning；会话两层：sessions.json（sessionKey→SessionEntry 元数据可编辑）+transcript（完整记录）；三种状态：short-term context（RAM 快易失）/long-term structured（SQLite/JSON 持久可查）/semantic memory（vector DB 概念召回） |
| 10 | DeepSeek（plugin 生态面） | ✓ | DSH（DeepSeek Harness）v0.1 开源（2026-08-13，MIT）；"一切皆插件"：模型适配器/系统提示词/工具目录/会话/存储/沙箱/Agent loop/Web UI/模式（标准/PTC/极简/创造）全由 Cordis 插件机制组合；Harness=Cordis Context；packages/core=Session/System Prompt；插件生态爆发：内测几天 300 插件；awesome-dsh-plugin 收录 1206 插件；dsh-plugin 主题 400+ 仓库；代表插件：ModLens 视觉/Web UI 全家桶/dsh-web-ui ⭐1312/aegis（coding agent 安全 agentic bench）；调度层：Claude Code/Codex 作为子代理被装进 Harness 调度（竞对产品变零件）；awesome-deepseek-integration（官方团队维护：模型训练/部署/监控/优化分类） |

## 判重基准
双键检索（相对 r224-r252A 已落章节）：Dify（r252-A 记忆体系——Agentic RAG/Knowledge Pipeline 检索面独有）；n8n（r252-A RAG——agent memory 分层面独有）；LangFlow（r250-A evaluation quality metrics——调试/DevOps 面独有）；Activepieces（r252-A AI builder——MCP server 面独有）；Make（r250-A 未落 webhook 细节——webhook 响应纪律独有）；Pipedream（r251-A 组件 API 部分落——OAuth/managed auth 面独有）；Claude Code（r252-A subagents——三层记忆面独有）；SkillsMP（r251-B 规模——目录信号+发布路径增量合并）；OpenClaw（r251-C 身份三层/heartbeat——记忆架构面独有）；DeepSeek（r249-C DSH 生态——最新规模 1206+子代理调度增量合并）。未选素材：Make webhooks（单点细节弱）；Pipedream OAuth（与 r252-A secrets 部分重叠）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify Agentic RAG 与 Knowledge Pipeline | Agent Node 决策引擎+动态源选择+ETL 管线 | 工作流 | wb-execute-discipline |
| ② n8n agent memory 分层 | Window Buffer+画布化 memory+双两层记忆 | 工具 | wb-execute-discipline |
| ③ LangFlow 调试与 DevOps | Playground+Traces+lfx validate+版本历史 | 工具 | wb-execute-discipline |
| ④ Activepieces MCP server | 单 URL 763 app+按任务搜动作+数据 masking | 工具 | wb-execute-discipline |
| ⑤ Claude Code 三层记忆 | CLAUDE.md+AutoMemory+MemoryTool+4 patterns | 工作流 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
