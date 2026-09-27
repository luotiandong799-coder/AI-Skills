# r240-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（Agent/RAG 面） | ✓ | Agentic RAG 模板（Legal Research Agent：Agent 自动选 1-2 collections Hybrid Search；检索质量低→重试其他 collections 或切 Google Search；LLM 总结）；RAG 排障顺序（先查检索质量再改 prompt——缺失或分错块的源无法靠 prompt 修复）；Knowledge Retrieval 节点（User Input→Knowledge Retrieval→LLM 输出作上下文）；RAG 流水线 ingestion→chunking→embedding→vector storage→retrieval→reranking 全托管（Weaviate/Qdrant/Milvus/Pinecone/pgvector/Chroma）；Agent node（LLM 工具自主控制迭代决定；Agent Strategies 定义思考行动） |
| 2 | n8n（错误处理/调试面） | ✓ | 调试四步（1 打开失败执行日志不动生产工作流→2 找失败节点记名字+错误消息→3 查该节点输入数据→4 判断数据是否如预期）；debug 字段技术（items.length+_debug_sample={{$json.items[0]}} 输出全原始数据+debug 字段看失败前数据；IF 节点条件日志仅当数据满足条件才记）；错误分层三层（per-node Retry On Fail 瞬时→error workflow 通知→fallback service 备用服务）；Fallback Service 模式（主 API continueOnFail+alwaysOutputData→IF 检查错误→切备用服务）；Error Trigger 只在 live/activated 时运行 |
| 3 | LangFlow（1.10-1.13 release 面） | ✓ | 1.11（Human-in-the-Loop checkpoints；A2A 协议支持发布 flow 供其他 agent 调用+flow 内调远程 A2A agent，LANGFLOW_A2A_ENABLED=true 默认关；AG-UI streaming Workflow API）；1.11.0 NextPlaid（multi-vector retrieval：ColBERT-style late interaction+ColPali-style visual document retrieval 开箱）；1.10（Assistant flow building；Memory bases 长期记忆；可配置向量库后端；七语言）；1.12.2（guardrails 组件升级组合 rule+model checks）；Gunicorn preload（LANGFLOW_GUNICORN_PRELOAD=true 重初始化只在 master 进程 fork 前做一次：加载组件/构建 types cache/建 starter projects→内存大省+可靠） |
| 4 | Activepieces（认证/安全面） | ✓ | RBAC+SSO（角色访问控制+SAML 单点登录减少多凭据攻击面）；Piece Auth refresh 缓存（login 换短时 token；不缓存则每次 action 前 login 触发 429——refresh callback 取一次缓存服务端注入 context.auth.access_token）；Secret manager 集成（连接存 secret 引用非实际凭据；运行时从 Vault/CyberArk/1Password 取；按需取从不存；更新后缓存过期≤1h 或清缓存立即生效）；SSRF 风险（API server 自身 outbound HTTP OAuth claim/refresh/Vault/webhook 目标/MCP tool validation URL 来自 admin config 或 user input——永远开着） |
| 5 | Make（Webhook/HTTP 面） | ✓ | 自定义 webhook 规则（每 scenario 自己 webhook URL 不能复用同一 webhook 多个 scenario；custom mailhook）；webhook 响应三态（json/urlencoded/text；status/headers/body 配置）；异步回调管道（外部服务完成→回调第二 Make webhook→JSON Parse→Iterator→Text Aggregator newline 拼可读块 clean async pipeline）；HTTP v4（简化设置+更安全 keychain 存储+原生分页；v3 legacy） |
| 6 | Pipedream（GitHub sync 面） | ✓ | 双向同步（push+pull 拉取；dev branches 编辑；commit 历史+merge 历史；link users to commits；从 Pipedream merge 或 GitHub 建 PR merge；本地编辑器编辑经 GitHub 同步）；Projects 组织（workflows 必须在 Projects 里；configure GitHub Sync 解锁分支开发/commit/pull/diff/PR）；CI/CD 最佳实践（tag with SHA 每镜像精确 commit SHA；flaky 测试 48h 内 quarantine 修或删否则 rerun 常态化信号无意义） |
| 7 | Anthropic（Claude Code 权限/hooks 面） | ✓ | 权限模式分级（default 受控执行正常权限检查/acceptEdits 隔离文件快速迭代/bypassPermissions 跳过提示但安全保护仍在生产或敏感系统避免；模式动态切换按任务进度和信心）；hooks 优先级（deny>ask>allow 任一 deny 操作阻塞其他 allow 不能推翻；规则检查→权限规则→默认 Ask）；hooks 当安全代码（PreToolUse/PostToolUse 拦截每个工具调用；好用例阻断读 secret 路径/编辑 .github/.claude/.mcp.json/部署清单/基础设施文件；PermissionRequest 事件代用户 allow/deny 匹配 tool name）；hook 安全（确认自己写的/读源码 plain JS/SHA256 验证；不从不可信 repo 装 hooks CVE-2025-59536 恶意 repo 注入 hooks 会话启动跑）；Manual 模式只读默认+显式批准 |
| 8 | skills.sh（市场/发现面） | ✓ | API 三端点（/api/v1/skills 分页 leaderboard；/search 按名或描述搜；/curated 官方策展）；leaderboard 先行（先查 leaderboard 按安装量排名展示最流行久经考验再跑 CLI 搜索；all-time+24h trending 视图）；规模（~669,670 skills 开放未策展任何人可发布；tech-leads-club 80 个人工策展过静态分析+Snyk 扫描）；find-skills 技能（搜 ecosystem 推荐技能当 how do I do X 自助 concierge） |
| 9 | docs.openclaw.ai（gateway/hooks 面） | ✓ | gateway hooks 配置（enabled+token+path /hooks+maxBodyBytes 262144；mappings match path→action agent→agentId→deliver；defaultSessionKey hook:ingress；allowRequestSessionKey=false+allowedSessionKeyPrefixes ["hook:"]）；gateway auth（mode token/token 值/allowTailscale；bind loopback；controlUi）；webhook token 安全（Authorization: Bearer 推荐；x-openclaw-token；query-string tokens 拒绝 ?token= 返回 400） |
| 10 | GitHub（生态面） | ✓ | 2026 第 36 周趋势（Agent 技能化/MCP 工具化/AI 工程化；chrome-devtools-mcp/awesome-mcp-servers/pdf-inspector/crawl4ai/firecrawl MCP 基础设施）；GitHub 官方 MCP Server（33.2k★ 读文件/搜代码/issues 直接交互）；Casdoor（Agent-first IAM：MCP & agent gateway+auth server 支持 OpenClaw/MCP/OAuth/OIDC/SAML）；MCP RCE Guard（Layer-3 RCE 防御 policy synthesis 从声明语义合成 per-tool 策略执行时强制 closes tool-injection-RCE class 侧载扫描器抓不到）；n8n-mcp 23k★ 用 MCP 建 n8n workflows；agent 框架生态（LangChain 147k/LlamaIndex 52k/CrewAI 59k/Autogen 61k） |

## 判重基准
双键检索：Dify（r239-C 落过检索三模式选型，"检索排障顺序+Agentic RAG 重试"独有增量）；n8n（r239-B 落过错误分层三型+测试四件套，"调试四步+debug 字段+fallback service 模式"独有增量）；LangFlow（r240-A/B 落过 Tool Mode/JWT，"A2A 协议+NextPlaid 多向量检索+preload"独有增量）；Activepieces（r239-B/r240-B 落过 MCP 安全/按任务搜工具，"refresh 缓存+secret manager 引用式"独有增量）；Make（r240-A/B 落过批量三件套/四角色，"异步回调管道+HTTP v4 分页"独有增量）；Pipedream（r240-A/B 落过 Data Store/双传输，"GitHub sync 双向全景+CI 纪律"独有增量）；Anthropic（r240-B 落过技能编写五建议，"hooks 优先级+权限模式分级+不从不可信 repo 装 hook"独有增量）；skills.sh（r238-C/r240-B 落过安装方法论/use 免安装，"API 三端点+leaderboard 先行+开放 vs 策展"独有增量）；docs.openclaw.ai（r239-B 落过 cron/tasks，"gateway hooks mappings+token 传输纪律"独有增量）；GitHub（r240-A/B 落过生态，"官方 MCP server+RCE Guard+Agent IAM"独有增量）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 检索排障顺序+Agentic RAG | 先查检索质量再改 prompt；低质量→换 collection/切搜索重试 | 工作流 | wb-execute-discipline |
| ② n8n 调试四步+fallback service | 先看执行日志不动生产+查节点输入；debug 字段看失败前数据；continueOnFail+IF 切备用 | 工作流 | wb-execute-discipline |
| ③ LangFlow A2A+多向量检索 | 发布 flow 供其他 agent 调用默认关；ColBERT late interaction+ColPali 视觉检索开箱 | 工具/工作流 | wb-execute-discipline |
| ④ Anthropic hooks 优先级+权限分级 | deny>ask>allow；hooks 当安全代码；default→acceptEdits 动态切换；不从不可信 repo 装 hook | 可复用 Skill | wb-execute-discipline |
| ⑤ skills.sh API 三端点+发现顺序 | leaderboard 先行再 CLI 搜索；开放 67万 vs 策展 80 带安全扫描 | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：wb-ponytail/wb-max-token-saver/wb-context-compressor 无新可优化项（hooks 优先级与 wb-execute-discipline 工具断言层互补已覆盖）。
- 垃圾：本轮未产生临时文件。
