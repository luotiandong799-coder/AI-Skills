# r233-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（credentials/workflow guide/plugin governance） | ✓ | 凭证范围分层（workspace vs workflow 级）、60-90 天轮换、敏感值不进 traces/exports 位置、插件治理 CI（贡献模板记录风险级+沙箱验证） |
| 2 | n8n（ai-agent-memory/chat memory） | ✓ | 单 agent 单 memory 子节点、记忆选型矩阵（Simple/Redis 1-5ms/Postgres 生产审计/MongoDB）、Chat Memory Manager、上下文窗口长度是成本开关、sessionId 一致性 |
| 3 | LangFlow（split-text dead→components-processing 补） | ✓ | Split Text 参数化、chunk_size 行为语义（separator 切后合并小块、超限块原样输出）、chunk_size ≤ embedding token 上限、Docling HybridChunker |
| 4 | Activepieces（changelog/MCP overview） | ✓ | ap_search_actions 按任务搜动作（描述→schema→运行）、审计日志 Action/Performed By/Project 过滤+JSON payload viewer、数据掩码永不进 logs、One MCP server for all pieces |
| 5 | Make（academy context engineering） | ✓ | Conversation ID 完整记录模型、大窗口三失败模式（poisoning/distraction/confusion/clash）、20-30 条存储平衡、30 天裁剪、上下文工程三原则 |
| 6 | Pipedream（triggers/contributing guidelines） | ✓ | webhook 优先于 polling（实时+省算力）、同一事件双模式并存（Calendly premium webhook vs REST polling）、intervalSeconds 配置 |
| 7 | Anthropic（agent skills best practices） | ✓ | 渐进式披露三层（100 tokens 常驻/5000 触发/无限按需）、上下文窗口公共品三问、frontmatter 规范（64/1024/保留词） |
| 8 | skills.sh trending tab | ✓ | Leaderboard 实拉（与 hot 相同，静态缓存），无新内容 |
| 9 | GitHub 生态（search：trending） | ✓ | deepseek-harness 235k（一切皆插件）、ECC 267k（harness 性能优化）、Superpowers 276k（brainstorm-plan-execute-review-ship）、harnesses.sh 75 目录 |
| 10 | 智谱 AgentMore（search） | ✓ | 多 Agent 群组协作（最多 5 个、头脑风暴/任务分配模式）、Skills 广场三类来源、智能体广场模板（体验→看画布→一键复制）、技能模块化零额外 Token |

## 判重基准
双键检索（来源标识+概念词）：凭证分层/插件治理 CI、按任务搜动作/掩码、Conversation ID/大窗口失败、渐进式披露/token 预算——均无同类已有落地。n8n 记忆矩阵与 r233-A Make data store 部分重叠但选型矩阵+sessionId 一致性为独有增量；Pipedream 触发器选型与"轻量自动化三模式"重叠~50% 但"webhook 优先+polling 双模式并存"为增量，未单独立点。

## 独点落地（4 个，全部真独点）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① 凭证范围分层+插件治理 CI | workspace vs workflow 级凭证；60-90 天轮换；敏感值不进 traces/exports；插件 PR 模板+CI 沙箱 | 工具/工作流 | wb-execute-discipline |
| ② 按任务搜动作+敏感掩码 | ap_search_actions 描述→schema→运行；敏感详情永不进 logs | 工具/工作流 | wb-execute-discipline |
| ③ Conversation ID 全记录+大窗口失败 | 完整对话账本；poisoning/distraction/confusion/clash；20-30 条平衡+30 天裁剪 | 工作流 | wb-execute-discipline |
| ④ 渐进式披露三层+公共品三问 | 100/5000/无限 三层 token 预算；写每段三问；frontmatter 规范 | 可复用 Skill | wb-execute-discipline |

## 复核
- 无编造凑数：四独点均有当日实拉原文来源。
- 功能套件检查：④ 渐进式披露与 wb-skill-authoring 直接互补（authoring 纪律）；③ 与 wb-context-compressor 记忆章节互补；wb-max-token-saver 与 ③ 大窗口成本互补；wb-ponytail 无新增归属。
- 垃圾：未产生临时文件。
