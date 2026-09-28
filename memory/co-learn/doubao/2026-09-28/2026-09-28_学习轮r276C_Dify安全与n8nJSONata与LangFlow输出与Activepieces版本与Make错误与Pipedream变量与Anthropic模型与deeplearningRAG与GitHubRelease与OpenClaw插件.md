# r276C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（安全隐私面） | ✓ | **企业版安全特性**（SSO SAML/OIDC；fine-grained RBAC 到 workflow 级；SCIM provisioning；session policies；按需部署 K8s Helm+AWS Terraform+隔离网络；数据主权 VPC/区域/边界内+BYOK 加密+无模型训练泄露；多租户隔离 单集群多业务单元 租户级配额/计费/访问策略）；**合规认证**（SOC 2 Type I&II、ISO/IEC 27001:2022、GDPR——DPA/隐私政策/年度 ROPA）；**内容审核三选项**（OpenAI Moderation 6 主类 13 子类缺细粒度；Custom Keywords 手动维护；API Extension 外部审核 API）；**Palo Alto 插件**（AI Runtime Security 输入检查拦 prompt injection/DoS/不安全链接+输出保护防泄露；Workflows/Agents/Chatflows 无缝集成）；**插件生态治理**（本地验证：安全解压/secret patterns/manifest 字段/README/依赖 OSV 检查/network.domains 声明）；**权限**（团队成员单位——部署级知识分割 Partial Members——工具最小权限 AI 只读） |
| 2 | n8n（JSONata 数据变换面） | ✓ | **表达式 vs 数据节点**（expressions JS-like 代码直接放节点参数 {{ ... }}——动态设参数值用前序数据/metadata/env vars——即时预览——能 expression 就 expression）；**表达式参考**（array.map(x = x.id)；$jmespath(obj, expression) 查询复杂嵌套对象无效返 undefined；Luxon 日期/JMESPath 两库）；**数据访问**（$json 当前项/$('Node').json 指定节点/$input.all() 所有项）；**示例**（首项/计数/filter+map+join/reduce 求和 toFixed(2)）；**JSONata Mapper 社区节点**（源字段映射目标路径；JSONata 表达式；点符号嵌套；JSON Schema 验证源+目标；缺字段默认；AI-assisted 映射生成） |
| 3 | LangFlow（输出解析面） | ✓ | **Structured Output 组件**（LLM 变换任意输入为 JSON/Table/Data/DataFrame——自然语言格式指令+输出 schema——验证层转 agent 响应一致 JSON）；**Output Schema 参数**（表字段 Name/Description/Type str/int）；**legacy Output Parser**（已替换——CommaSeparatedListOutputParser）；**Parser 组件**（Message 空/意外值=映射错误/空值/不适合纯文本提取；Table 模板；搜索结果 JSON 提取 text 避免整块喂 LLM）；**Agent Structured Response**（1.10.0 agent 回复按 Output Schema 格式化 Data）；**模板**（合同 8 字段 schema 验证 database-ready） |
| 4 | Activepieces（版本控制面） | ✓ | **Project Releases**（Git 连接项目——Push Everything 推所有 flows/connections/tables——commit message→Push；也可单独推）；**Git Sync**（外部备份+environments+版本历史——flow 名旁箭头 Push to Git；approval 流 development/production 两分支+PR）；**Pieces CI/CD**（离线开发→package.json 增量版本→PR→合并后 CLI 或 GitHub/GitLab Action 触发同步）；**环境体系**（Preview per-PR/Staging/Canary 每日 main 切/Production）；**Project Replace CLI**（Environments 需 plan；SERVICE principal API key；同 project id；同 major 版本目标≥源）；**Breaking Changes**（连接引用变更现在被 diff 看见——flow 只改连接也会被应用） |
| 5 | Make（错误处理面） | ✓ | **Incomplete executions**（失败 run 保存数据+blueprint——rerun 防丢信息——模块设置/输入/输出到失败模块）；**Retry error handler**（失败 bundle 暂停——存错误/mappings/剩余 flow——自动或手动重试）；**Break error handler**（移除 erroring bundle——存 incomplete execution——自动完成或人工解决——最有效于临时错误 ConnectionError）；**重试模式**（Exponential Backoff：error handler route→Sleep 30s→Router 回原模块→Set Variable 计数限 3 次；Fallback Module 备用）；**Break+Auto-Retry**（瞬态 429/502/503/Timeout——attempts 3/interval 15 分钟/allow storing yes）；**管理**（仅激活 scenario 可重试——Incomplete executions tab）；**监控**（执行记录+incomplete 列表——外部 DB Notion/Airtable 记趋势） |
| 6 | Pipedream（环境变量面） | ✓ | **env vars 分离秘密与静态配置**（API key 不直接放代码——process.env.API_KEY 引用）；**安全最佳实践**（秘密两种存储：Pipedream 集成 app→connected accounts；不支持 app 或任意配置→environment variables）；**env vars 值私有**（Node.js process.env.VARIABLE_NAME 任何 workflow 引用）；**组件限制**（env vars 在 sources/actions 不可直接访问——sources 用 secret props——actions object explorer 选变量）；**外部凭证运行时**（HashiCorp Vault/AWS Secrets Manager/DB/Nango——HTTP request 或 fetch from DB 步内）；**CLI 配置**（pd config file 含 API keys——XDG_CONFIG_HOME 时 $XDG_CONFIG_HOME/pipedream）；**SDK**（PipedreamClient clientId/secret/projectId/projectEnvironment production） |
| 7 | Anthropic（模型选择面） | ✓ | **四模型谱系**（Fable 5.1 严苛推理+长时 agentic；Opus 5.5 长时 agentic coding+知识工作；Sonnet 5 速度+智能最佳；Haiku 4.5 最快近前沿）；**规格**（上下文 1M/1M/1M/200K；max output 128K/128K/128K/64K；cutoff Jun 2026/Jun 2026/Jan 2026/Feb 2025）；**Opus 5**（法律 agent 显著提升——低推理层级保持质量——比 Opus 4.8 max 少 26% tokens）；**Sonnet 5**（接近 Opus 4.8 更低价——agentic 性能大幅提升）；**Opus 5.5 基准**（CursorBench 4.0 57.8% vs Fable 51.8%/Opus 5 46.6%/GPT-5.6 Sol 41.7%；GDPval-AA 1846）；**SWE-bench**（Opus 4.6 80.8% vs GPT-5.4 ~78%/Gemini ~76%） |
| 8 | deeplearning（RAG 进阶面） | ✓ | **RAG 课程**（Coursera——检索+生成协同组件级设计——keyword/semantic/hybrid search、chunking、query parsing——healthcare/e-commerce——prompt design/evaluation/deployment——5 模块 26 小时 49 视频 9 代码 10 作业——Zain Hasan——语义搜索 vs BM25 vs RRF）；**Advanced RAG（LlamaIndex+TruEra）**（Jerry Liu+Anupam Datta——2 小时免费——RAG Triad metrics/Sentence-window retrieval/Auto-merging retrieval）；**Multimodal RAG**（LangChain+BridgeTower Intel——chat with videos）；**7-stage pipeline**（ingestion/chunking/embedding/FAISS/retrieval/cross-encoder reranking/context assembly——background indexing——TF-IDF sparse——hybrid+RRF）；**RAG 质量清单**（chunking 评估迭代） |
| 9 | GitHub（Releases 面） | ✓ | **自动生成 release notes**（Draft→Choose tag→Target 分支→.github/release.yml 配置 YAML 指定 PR labels/作者排除——changelog.exclude.labels）；**Conventional PR 流程**（脚本收集合并 PRs——conventional commits 定版本生成 changelog——PR merge 触发 workflow 建 tag+release）；**semantic-release**（自动版本化+changelog——tag_format v${version}）；**release-please**（自动 semver bump major/minor/patch——生成 PR 含版本 bump+完整 changelog）；**CHANGELOG.md**（conventional commits 生成——parse commit messages between tags——按 features/fixes/breaking 分类）；**Tag 格式**（v 开头——workflow 读 changelog entry 转 Added/Changed/Fixed——上传 artifact 建 Release）；**commit 提取版本**（[release] v1.2.3 grep） |
| 10 | OpenClaw（插件系统面） | ✓ | **插件四来源**（git 仓库 branch/tag/commit——install git:github.com/owner/repo@branch；local path 开发测试 install --link ./my-plugin；marketplace Claude-compatible install --marketplace；npm-pack 本地打包）；**安装解析**（按名装无来源内置优先级——ClawHub 先查无则 npm fallback；bare spec 匹配 bundled id）；**构建发布**（Node >=22——不必进 OpenClaw 仓库——ClawHub 或 npm publish——install clawhub:<package>——plugins inspect --runtime --json）；**ClawHub**（公共社区插件主发现面——live listing/release history/scan status/install hints——外部 channel catalogs 合并 ~/.openclaw/mpm/plugins.json）；**社区插件类型**（channels/tools/providers/hooks）；**市场兼容**（Claude-compatible extensions 直接拉入——plugins.load.paths）；**CLI 管理**（list/inspect/uninstall update/marketplace feeds） |

## 判重（双键检索结果）
- Dify 安全：库内 §Dify 类锚点——企业版安全特性/合规认证/内容审核三选项/PANW 插件/插件生态治理为独有增量 ≥40% → 落地
- n8n JSONata：库内 §n8n 类锚点——表达式 vs 数据节点/表达式参考/JMESPath/JSONata Mapper 为独有增量 ≥40% → 落地
- LangFlow 输出解析：库内 §LangFlow 类锚点——Structured Output/Output Schema/Parser/Agent Structured Response 为独有增量 ≥40% → 落地
- Activepieces 版本控制：库内 §Activepieces 类锚点——Project Releases/Git Sync/Pieces CI/CD/环境体系/Project Replace CLI 为独有增量 ≥40% → 落地
- Make 错误处理：库内 §Make 类锚点——Incomplete executions/Retry/Break 错误处理器/重试模式为独有增量 ≥40% → 落地
- Pipedream env vars：库内 §Pipedream 类锚点——env vars 分离秘密/connected accounts vs env/组件限制/外部凭证运行时为独有增量 ≥40% → 落地
- Anthropic 模型：库内 §Anthropic 类锚点——四模型谱系规格/Opus 5/Sonnet 5/Opus 5.5 基准/SWE-bench 为独有增量 ≥40% → 落地
- deeplearning RAG：库内 §deeplearning 类锚点——RAG 课程 5 模块/Advanced RAG/Multimodal RAG/7-stage pipeline 为独有增量 ≥40% → 落地
- GitHub Releases：库内 §GitHub 类锚点——自动 release notes/release.yml/semantic-release/release-please/tag 格式为独有增量 ≥40% → 落地
- OpenClaw 插件：库内 §OpenClaw 类锚点——插件四来源/ClawHub/构建发布/CLI 管理/市场兼容为独有增量 ≥40% → 落地

## 独点落地（10 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r276C-1 | wb-execute-discipline | 3.46.0+ | Dify 安全与数据隐私 | 工作流 |
| r276C-2 | wb-execute-discipline | 3.46.0+ | n8n JSONata 与数据变换 | 工具 |
| r276C-3 | wb-execute-discipline | 3.46.0+ | LangFlow 输出解析与结构化输出 | 工具 |
| r276C-4 | wb-execute-discipline | 3.46.0+ | Activepieces 版本控制与环境 | 工作流 |
| r276C-5 | wb-execute-discipline | 3.46.0+ | Make 错误处理与场景健康 | 可复用 Skill |
| r276C-6 | wb-execute-discipline | 3.46.0+ | Pipedream 环境变量与秘密管理 | 工具 |
| r276C-7 | wb-execute-discipline | 3.46.0+ | Anthropic 模型选择与能力基准 | 模型 |
| r276C-8 | wb-execute-discipline | 3.46.0+ | deeplearning 上下文工程与 RAG 进阶 | 可复用 Skill |
| r276C-9 | wb-execute-discipline | 3.46.0+ | GitHub Releases 与版本管理 | 工具 |
| r276C-10 | wb-execute-discipline | 3.46.0+ | OpenClaw 插件与扩展系统 | 工具 |

## 复核
十独点均有当日实拉来源；均增量合并或新面；无并入未落地项。垃圾：本轮未产生临时文件。
