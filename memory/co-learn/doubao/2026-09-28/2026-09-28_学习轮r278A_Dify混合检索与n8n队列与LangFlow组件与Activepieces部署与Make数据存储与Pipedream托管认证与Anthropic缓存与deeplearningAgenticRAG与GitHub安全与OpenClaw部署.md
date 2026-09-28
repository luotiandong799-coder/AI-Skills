# r278A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（混合检索/RAG） | OK | Hybrid Search=向量+全文并行（weight 合并或 rerank）；rerank model（Cohere/bge-reranker）语义重排候选文档；权重配置 semantic 0-1/keyword 0-1（1=纯向量/纯关键词）；多路检索（Multi-path Retrieval 跨知识库合并）；rerank 一般放检索流程末段先粗召回再精排；多模态 embedding 需配多模态 rerank（Vision 标记）；RAG 升级 20% 精度提升 |
| 2 | n8n（Queue 模式/扩展） | OK | Queue 模式=main 处理 timer/webhook 生成 execution ID→Redis（Bull）队列→worker 拉取执行；EXECUTIONS_MODE=queue；workers 须共享同一 encryption key 否则解不开凭据；IO 密集并发 10-20/worker、CPU 密集较低；每 worker ≥5 并发防耗尽 DB 连接池；multi-main HA（Enterprise，共享 PostgreSQL+Redis）；benchmark=72 rps/3 秒延迟/200 VU 零失败 |
| 3 | LangFlow（自定义组件） | OK | 自定义组件=继承 Component 类+class-level 属性（display_name/类型）+Input/Output 列表+方法；inline code（langflow-builder-mcp 动态评估建 node template，免重启）vs file-based；LFX_DEV=1 热重载；组件发现机制 component_index.json 缓存+懒加载（Bundles）；Langflow Assistant 可从 prompt 生成组件代码 |
| 4 | Activepieces（自托管） | OK | Docker 单容器嵌入式数据库（数据 ~/.activepieces，零配置）；Docker Compose 生产（Docker Compose v2+≥2vCPU/4GB RAM+Windows WSL2+PostgreSQL+Redis）；app/worker 拆分（AP_CONTAINER_TYPE=APP 只服务 API/UI、WORKER_AND_APP）；deploy.sh 生成 .env；K8s/Helm/AWS Pulumi；数据在 ~/.activepieces |
| 5 | Make（Data Store） | OK | Data Store 模块跨 scenario 运行持久化/查询；真实模式=checkpoint/cursor 追踪状态（多天邮件序列/分页导出记住中断位置）；Get a Record key 读回；场景状态追踪（multi-step workflow 记进度） |
| 6 | Pipedream（Connect/托管认证） | OK | Managed Auth：项目 ID+OAuth client（client ID/secret）；end users 须用你自己的自定义 OAuth client（oauthAppId）；external_user_id=你的系统用户 ID（限 250 字符）关联账号；环境隔离（dev/prod，凭据按 external_user_id+环境保存）；MCP 代理=app 动作暴露 MCP tool，Connect 解析该用户账号不存 token |
| 7 | Anthropic（Prompt Caching） | OK | 缓存定价结构：5m writes=1.25x 基础输入价、1h writes=2x、hits&refreshes=0.1x（Fable 5.1/Mythos 5.1 命中 2.5% 标准输入价、Opus 5.5 命中 5%）；自动缓存（cache_control breakpoint）或手动；与 Batch API 折扣/数据驻留叠加；官方建议=高频重复上下文用缓存+Batch 非实时任务+监控用量 |
| 8 | deeplearning（Agentic RAG 课程） | OK | Building Agentic RAG with LlamaIndex：router（选 Q&A/summarization 引擎）→tool calling（LLM 选函数+推断参数）→research assistant agent（多轮迭代）；RAG 基础课（semantic search/BM25/RRF 对比）；agentic RAG 本质=loop 代替线性 retriever→prompt→answer（LLM 决定是否检索/检什么/结果够不够/要不要再搜）；LangChain create_tool_calling_agent |
| 9 | GitHub Actions（安全加固） | OK | GITHUB_TOKEN 最小权限（permissions: contents: read）；避免 pull_request_target 触发（fork 代码不可信）；第三方 Actions 钉 SHA；workflow_run 防 fork PR 触发（event_name != pull_request）；artifacts 视为不可信（解压临时目录+校验）；CodeQL 审查 workflow；2026 路线图：scoped secrets/reusable workflow inheritance/写权限不再含 secret 管理；runner SBOM |
| 10 | OpenClaw（安装/部署） | OK | 安装脚本（curl install.sh / iwr install.ps1）；Node.js 22+（22.19.0+）；新手引导 openclaw onboard（配置 auth/gateway/channels，--install-daemon）；Windows Hub 桌面应用；npm 方式 npm install -g openclaw@latest / npx openclaw@latest；源码安装 git clone+pnpm build；openclaw status 验证；LLM provider=Anthropic/OpenAI key 或本地 Ollama |

## 判重（双键检索，增量判定）
- Dify 混合检索（库内 RAG 锚点）→ 增量=Hybrid Search 权重合并+rerank 配置+多路检索
- n8n Queue（库内 n8n 部署锚点 r277B LangFlow Docker）→ 新面（队列扩展/HA）
- LangFlow 自定义组件（r276B multi-agent 锚点）→ 新面（组件开发）
- Activepieces 自托管（r277A Pieces 治理锚点）→ 新面（部署）
- Make Data Store（r276A Make modules 锚点）→ 新面（状态持久化）
- Pipedream Connect（r277C 定价锚点）→ 新面（托管认证）
- Anthropic Prompt Caching（r277C 用量 API 提到缓存定价）→ 增量=缓存机制+定价结构+breakpoint
- deeplearning Agentic RAG（r276C context engineering RAG 锚点）→ 增量=agentic loop+LlamaIndex 课程
- GitHub Actions 安全（r277B Actions 复用锚点）→ 增量=最小权限+SHA 钉死+fork 防护
- OpenClaw 部署（r277A hooks/r277B MCP 锚点）→ 新面（安装引导）

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 混合检索与重排 | 工具 |
| 2 | n8n Queue 模式与横向扩展 | 工具 |
| 3 | LangFlow 自定义组件 | 可复用 Skill |
| 4 | Activepieces 自托管部署 | 工具 |
| 5 | Make Data Store 状态持久化 | 工具 |
| 6 | Pipedream Connect 托管认证 | 工具 |
| 7 | Anthropic Prompt Caching | 工具 |
| 8 | deeplearning Agentic RAG 课程 | 可复用 Skill |
| 9 | GitHub Actions 安全加固 | 工具 |
| 10 | OpenClaw 安装与部署 | 工具 |

## 复核
十独点均有当日实拉来源；均增量合并或新面；无并入未落地项。版本建议 3.50.0+。