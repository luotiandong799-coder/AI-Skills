# r270C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r266-r270B 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（评估/监控面） | ✓ | **Arize-Phoenix 集成**（开源可观测层——每次模型调用/工具调用/链步骤自动 trace；inputs/outputs/latencies/metadata；不猜 prompt 调整为什么有用）；**LangSmith/Langfuse 集成**（性能监控 accuracy/latency/资源；连续改进+人工标注；成本优化 token 细节）；**日志功能**（对话日志完整 input/output 历史+timing+系统元数据；用户反馈 thumbs up/down；系统上下文 model/token 消费/响应时间/errors）；**Annotation Reply**（调试时标注 AI 回复预对齐期望；hit tracking 命中监控/覆盖率分析/问题模式/匹配质量；不命中=覆盖缺口）；**Monitoring**（总对话数/token 使用/session 长度） |
| 2 | n8n（错误处理模式面） | ✓ | **两错误类**（NodeApiError API 相关+NodeOperationError 操作/验证/配置）；**重试默认表**（重试 408/409/425/429/500/502/503/504；不重试 400/401/403/404/422）；**退避公式**（waitSeconds=min(maxDelay, baseDelay...jitter）；**三模式**（A node-level isolation+error routing 推荐默认——隔离风险调用路由独立路径，主路径仅有效输出继续，错误路径持久化+告警；B sub-workflow containment——关键步骤子工作流 fail fast 返回结构化错误；C dead-letter queue——重试耗尽后 payload+最终错误写 durable store 回放）；**Error workflow 铁律**（全局 error workflow 是实例第一配置——Error Trigger+Slack 赋每工作流；Retry on Fail 每网络节点 3 tries；On Error Stop vs Continue 判据）；**workflow 级重试循环**（Code+Wait+IF 指数退避；HTTP 调 n8n API 按 ID 重试；IF 阈值+Set 计数）；**失败详情存储**（workflow_id/tenant_id/error step/retry count；幂等；failed jobs 保留回放）；**circuit breaker**（Redis 状态 OPEN+RESET_TIMEOUT） |
| 3 | LangFlow（部署/性能面） | ✓ | **K8s 生产最佳实践**（runtime headless backend-only 服务；最小 2Gi RAM+1000m 1 CPU×3 replicas；HPA 动态扩缩）；**多 worker**（LANGFLOW_WORKERS 增并发；每进程内存 build queue——Redis Streams job queue 任一 worker 服务）；**内存优化**（v1.9-v1.10 依赖裁剪+worker 生命周期+Linux CoW——~89% 内存降）；**基准参考**（简单 flow 200-500ms/复杂 2-5s/内存 150-300MB/自托管并发 50-100）；**生产缺口**（不内置 auth/rate limiting/DB 持久化；OSS 无 RBAC；缓存层内存泄漏风险）；**HashiCorp 模式**（--backend-only+Vault secrets+Prisma AIRS+外部 PostgreSQL）；**指标**（P50/P95/P99 延迟/错误率/外部 API 成本/检索命中率；高成本推理拆独立水平扩展+批处理+缓存；向量索引 k 邻居/shard） |
| 4 | Activepieces（连接/认证面） | ✓ | **PieceAuth.OAuth2**（displayName/grantType AUTHORIZATION_CODE/authUrl/tokenUrl/scope）；**Override OAuth2 Apps**（Platform Admin→Setup→Pieces 换自己的 Client ID/Secret——品牌显示自己公司名+更高限额）；**MCP OAuth**（client 首次浏览器认证；credentials 永不暴露——连接秘密/API keys 加密）；**Embeddable MCP quick token**（generateMcpToken() 前端——无 app 注册/PKCE/popup）；**connections/upsert 端点**（OAUTH2 client_id/code/code_challenge/scope/authorization_method HEADER/BODY）；**SSO**（Google OAuth redirect URI+SAML Okta）；**embed connections**（SDK 用户创建连接存 Activepieces） |
| 5 | Make（聚合/数据处理面） | ✓ | **内置函数**（map/get/first/last 访问数组集合值；map(array; key; [key for filtering])）；**Array Aggregator**（nested array 提取坑——map 返回空数组时用 key）；**嵌套数组扁平化**（webhook JSON suppliers[].offer.variants[].prices——flatten/map；Make Code 单模块 JS 处理 structured output 解析标签+价格数组可映射）；**reduce**（聚合数组最强——迭代累积单结果） |
| 6 | Pipedream（运行时/限制面） | ✓ | **执行限制**（HTTP/Email 触发默认 30s；cron 默认 60s；paid 上限 750s 12.5 分钟；每 segment 12 分钟）；**内存**（可调——浏览器自动化推荐 2GB；selected steps 扩展内存限制高内存只跑该段省 credits）；**pd.flow.suspend**（暂停/恢复/重跑——默认 24h 自动取消，可设 7 天 timeout）；**上传限制**（HTTP body 默认 512KB——pipedream_upload_body=1 query 或 x-pd-upload-body: 1 header 传任意大小）；**浏览器自动化**（离开前关闭浏览器实例否则 step 不交接）；**并发**（同步 5-50 分钟/异步 90 分钟/15-300 plan-gated） |
| 7 | Anthropic（缓存配置/成本面） | ✓ | **定价结构**（5m cache writes +25% base input；1h cache writes 2× base；cache hits 10% base）；**Opus 4.6 表**（$5/MTok base/$6.25 5m write/$10 1h write/$0.50 hit/$25 output）；**盈亏平衡**（write 成本 2 次 read 回本——第三次起每次省 90%）；**breakpoints 免费**（cache_control 本身无成本；更多 breakpoint 不增成本）；**缓存破坏因素**（图像变化/工具使用配置修改→破坏缓存）；**成本示例**（Pilot 1000 req/day 20k ctx——$60/月 vs $600 省 $540；Production 10000 req——$600 vs $6000）；**持久缓存**（enterprise 需要 persistent caching+BAA）；**缓存目标**（system prompts/tool definitions/documents 大重复段） |
| 8 | deeplearning.ai（RAG 课程面） | ✓ | **RAG 课程（Intermediate 24h33m）**（Weaviate+真实新闻数据集——chunking/indexing/retrieving；Module 3：Chunking 6m+Code 1h+Advanced 5m+Query parsing 5m+Cross-encoders and ColBERT 8m+Reranking 4m；Module 2：BM25/semantic/hybrid）；**chunking 策略**（固定尺寸 N tokens M overlap；advanced techniques）；**arXiv 系统分析**（更大 chunk 减少上下文数增加 abstention 窄证据错过；summaries 小 C；factoid QA C≈2.5k；减少 NONE 增大 C 更小 S；避免 overlap；默认 sentence chunking） |
| 9 | GitHub（记忆/上下文面） | ✓ | **记忆层生态**（mem0 57.3k/mempalace 53.2k/Understand-Anything 47.8k/supermemory 23.5k；claude-mem 90k——跨 session 记录一切+AI 压缩+inject 回下一 session 支持多 agent）；**agentmemory（rohitg00 4.2k→6.5k+）**（跨 session 持久记忆 16+ agents——四层管线 Working→Episodic→Semantic→Procedural+三流混合搜索 BM25/vector/knowledge graph+50+ MCP 工具）；**Honcho（Plastic Labs 4.3k★ AGPL）**（stateful agents 记忆基础设施——90.4% LongMem peer-centric/MCP/self-hostable/SOTA）；**TencentDB Agent Memory（2 万★ 90 天）**（长短期记忆——Conversations/Documents/Code/Skills 成 Team Memory 多 agent 协作；Trending 多次第 1）；**cognee**（6 行代码记忆）；**memU**（24/7 proactive agents 专用） |
| 10 | OpenClaw（技能/知识面） | ✓ | **Skills 机制**（Markdown 指令文件教 agent 何时怎么用工具——SKILL.md YAML frontmatter+正文；AgentSkills 兼容；加载时按环境/config/binary presence 过滤）；**三目录优先级**（Workspace ~/.openclaw/workspace/skills/ 最高优先；Managed ~/.openclaw/skills/ ClawHub 跨 agent；Bundled 预装——同名高优先胜）；**frontmatter 字段**（name snake_case 必填/description 必填/os 过滤/requires.bins PATH/requires.config）；**Skills ≠ 权限**（指令文件不等于工具权限——执行仍受权限系统管）；**CLI 命令**（skills list/info/search/update/uninstall/enable）；**ClawHub 目录**（60+ curated——clawhub CLI 单命令；安全提示 review 安装前 treat like third-party code）；**内置**（Web Search Brave/Web Fetch/Browser） |

## 判重（双键检索结果）
- Dify 评估：库内已落 §评估驱动/§Dify 节点——Arize trace+LangSmith 集成+日志标注+Annotation Reply 命中跟踪为独有增量 ≥40% → 落地
- n8n 错误：库内已落 §错误工作流（r269A）——NodeApiError/OperationError 两类+重试状态码表+三模式+全局 error workflow 铁律+circuit breaker 为独有增量 ≥50% → 落地
- LangFlow 部署：库内已落 §部署 API（r269A/r270A）——K8s runtime headless+HPA+多 worker Redis+89% 内存降+生产缺口为独有增量 ≥50% → 落地
- Activepieces 认证：库内已落 §连接面——PieceAuth.OAuth2+Override 品牌+quick token+SSO+upsert 端点为独有增量 ≥40% → 落地
- Make 聚合：库内已落 §Data Store——map/get/first/last 内置+Array Aggregator 嵌套坑+flatten/reduce 为独有增量 ≥40% → 落地
- Pipedream 运行时：库内已落 §限制面——执行限制表+内存分段+suspend 24h/7d+512KB 上传+浏览器 2GB 为独有增量 ≥40% → 落地
- Anthropic 缓存：库内已落 §prompt caching（r268C）——定价表细节（5m +25%/1h 2×/hit 10%）+盈亏平衡 2 reads+破坏因素+持久缓存为独有增量 ≥40% → 合并保留增量落地
- deeplearning.ai RAG：库内已落 §RAG 检索——课程结构+chunking 策略+arXiv 系统分析（C≈2.5k/sentence/避免 overlap）为独有增量 ≥40% → 落地
- GitHub 记忆：并入记录（生态情报 agentmemory/TencentDB/Honcho）
- OpenClaw 技能机制：库内已落 §技能权限/§插件配置——三目录优先级+frontmatter 字段表+Skills≠权限+CLI+ClawHub 为独有增量 ≥40% → 落地

## 独点落地（9 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r270C-1 | wb-execute-discipline | 3.28.0+ | n8n 错误处理三模式与全局 error workflow（增量合并 §错误工作流） | 工作流 |
| r270C-2 | wb-execute-discipline | 3.28.0+ | LangFlow 生产部署与扩展 | 工作流 |
| r270C-3 | wb-execute-discipline | 3.28.0+ | Dify 可观测性与标注回复 | 可复用 Skill |
| r270C-4 | wb-execute-discipline | 3.28.0+ | Anthropic 缓存定价与盈亏平衡（增量合并 §prompt caching） | 工具 |
| r270C-5 | wb-execute-discipline | 3.28.0+ | OpenClaw 技能三目录与 frontmatter（增量合并 §技能权限） | 可复用 Skill |
| r270C-6 | wb-execute-discipline | 3.28.0+ | Make 数组聚合与嵌套处理 | 工作流 |
| r270C-7 | wb-execute-discipline | 3.28.0+ | Pipedream 运行时限制与暂停恢复 | 工具 |
| r270C-8 | wb-execute-discipline | 3.28.0+ | Activepieces 认证配置 | 可复用 Skill |
| r270C-9 | wb-execute-discipline | 3.28.0+ | deeplearning.ai RAG chunking 策略 | 可复用 Skill |

## 复核
九独点均有当日实拉来源；均为增量合并或新面落地；并入记录：GitHub agent 记忆生态。垃圾：本轮未产生临时文件。
