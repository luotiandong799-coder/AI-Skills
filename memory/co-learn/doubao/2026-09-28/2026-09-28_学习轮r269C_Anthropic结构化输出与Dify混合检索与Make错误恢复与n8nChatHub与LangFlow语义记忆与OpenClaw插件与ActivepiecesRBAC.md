# r269C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r266/r267/r268/r269A/r269B 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（混合检索/重排面） | ✓ | **检索方法四选**（语义向量/关键词全文/混合）；**混合流程**（语义+全文两路→融合→重排——RetrievalService._retrieve）；**Rerank 模型**（默认禁用——启用需 Integrations→Model Provider 配 API key；排序混合返回 chunks 让 LLM 取更精确信息；多模态 embedding 需多模态 rerank）；**重排定位**（搜索最后阶段——前置检索算全库相关性太贵；合并排序多检索系统结果）；**权重配置**（hybrid 两路加权）；**score threshold 语义**（混合+重排时阈值应作用于重排后分数——pre-rerank 分数阈值 bug 已修）；**选型判据**（precision+recall 都重要→hybrid；大语料/短语匹配→full_text） |
| 2 | n8n（Chat Model 配置面） | ✓ | **AI Agent 内模型**（内置支持列表；OpenAI Chat Model 节点 attach；基础账号仅 gpt-4o-mini）；**Chat Hub**（Custom Agents 带 name/description/system prompt；复杂场景用 workflow agents——Chat Trigger+streaming 才可发布）；**多 agent @mentions**（OpenRouter identifier "openai/gpt-4o"/"anthropic/claude-3.7-sonnet"+systemMessage 人格）；**模型参数**（Completion Tokens 按响应长度 150/500+/1000+；Top P 0.9 多数应用；Reasoning Effort 复杂推理提高）；**多会话记忆**（Data Table 存 chat_session_data+Data Table Tool）；**Redis Chat Memory**（消息历史持久化）；**LLM 节点单选**（Gemini/OpenAI 只激活一个）；**升级转人工**（Groq+Postgres 历史+Pinecone 知识库） |
| 3 | LangFlow（记忆/向量面） | ✓ | **MemoryBase vs Message History**（Message History 从 messages 表按时间序取最近；MemoryBase 把消息嵌入向量库按语义相似检索最相关——跨会话长程历史）；**MemoryBase 配置**（display name/linked kb_name/embedding model/ingestion threshold/auto-capture/preprocessing；backend_type 活在关联 KnowledgeBase 行）；**Vector Store 组件**（读写向量数据——embedding storage/vector search/Graph RAG/OpenSearch/Elasticsearch/Vectara；多数连远程部分本地）；**组件体系**（HCD/Valkey FT 索引 langchain-aws/Chroma 远程内存带持久化/Astra DB Data API+DevOps API——基于 LangChain vector store 实例）；**本地 RAG 模板**（ChromaDB+Ollama 全本地无网络）；**Load Data/Retriever 子流**（加载嵌入+内容/相似搜索） |
| 4 | Activepieces（RBAC 面） | ✓ | **四默认角色**（Admin 全权含 billing/Editor 创建编辑运行/Operator 运行/Viewer 只读）；**权限表**（View Flows 四角色✓）；**Custom Roles**（Platform Admin→Security→Project Roles——细粒度 READ_FLOW/WRITE_FLOW/READ_APP_CONNECTION/WRITE_APP_CONNECTION/READ_RUN）；**SCIM Provisioning**（IdP 自动同步用户组快 onboarding）；**Visibility Control**（按团队显隐集成）；**企业安全**（SSO Okta/Entra+audit logs+secret managers 凭据自持 vault+加密+数据位置控制）；**付费层**（SCIM/custom roles/Git Sync/audit logs/secrets 高 tier） |
| 5 | Make（错误监控/恢复面） | ✓ | **四错误处理器**（Resume 造假输出保持流——邮件失败记日志继续/Commit 事务确认——DB 多模块部分成功/Rollback 事务取消——部分失败全回滚/Break incomplete execution 存储+重试——一般运营）；**Break 处理器**（存储错误消息/mappings/剩余流程为 incomplete execution——自动或手动完成；最有用生产指令）；**Retry error handler**（暂停失败 bundle 自动或手动重试）；**Incomplete executions**（保存数据+失败 blueprint——rerun 防丢失；模块设置/输入/输出到失败模块）；**Scenario recovery**（后台自动保存 blueprint——崩溃/断连/误关恢复；非 autosave 恢复后手动保存）；**Version history 60 天**；**Failed Bundles Data Store 模式**（scenario_name/bundle_data JSON/error_message/timestamp/replayed——修复后回放） |
| 6 | Pipedream（组件发布面） | ✓ | **pd publish**（发布 action；--dev 自动迭代）；**TypeScript 流程**（pd publish/dev 编译后 dist JS——dist 目录必须）；**Custom Tools**（Connect 同开发流程——mjs --connect-environment flag；custom tools 是 actions）；**Sources 部署**（CLI 本地部署或发布账号 UI 实例化）；**Actions 仅发布**（发布后 workflow UI 添加）；**可见性**（默认仅自己账号；团队账号可被发现）；**Registry 贡献**（fork 公开 repo+组件放对应 app 目录——key/version/name 唯一；发 marketplace）；**REST API**（先创建 component 拿 id/code/configurable_props 再部署 source） |
| 7 | Anthropic（结构化输出面） | ✓ | **json_schema format**（output_config.format.type=json_schema+schema——properties/required/additionalProperties=False 强制精确）；**用途**（从图提取/agent 编排/外部 API 集成——消除 schema 解析错误与失败工具调用；public beta 保证响应匹配 schema 或工具定义）；**strict tool use**（工具定义 enum/format date/additionalProperties false）；**JSON Schema 子集限制**（enum 仅 strings-numbers-booleans-nulls/const/anyOf/allOf 有限/$ref/$defs 递归不支持；Array minItems 仅 0/1；ipv4/ipv6/uuid format）；**SDK outputFormat**（type json_schema+query options）；**工具定义三字段**（name regex ^[a-zA-Z0-9_-]{1,64}$/description 何时用/input_schema） |
| 8 | deeplearning.ai（提示工程课程面） | ✓ | **ChatGPT Prompt Engineering（1h30m，Isa Fulford+Andrew Ng，免费）**（两大原则 guidelines/iterative；五核心任务 summarizing/inferring/transforming/expanding/chatbot；zero-shot/few-shot；迭代提示方法论）；**AI Prompting for Everyone（3h4m，Andrew Ng）**（web search+deep research 获取有源答案）；**Prompt Engineering with Llama 2&3（1h53m，Meta Amit Sangani）**（Helper Function/multi-turn/模型对比） |
| 9 | GitHub（trending agent 仓库面 2026-09） | ✓ | **herdr（40.8k★ Rust）**（coding agents runtime）；**TiDB（40.6k★ Go）**（agentic workloads——ACID+事务+分析+向量搜索原生）；**Hindsight**（Agent Memory That Learns 本周 7.2k★）；**Tencent/WeKnora（30.4k★）**（raw docs→RAG+自主推理 agent+自维护 Wiki）；**anthropics/claude-code**（终端 agentic coding——git workflows 自然语言）；**blader/humanizer**（去 AI 写作痕迹 agent skill）；**cline**（SDK/IDE 扩展自主 coding agent）；**BuilderIO/agent-native**；**stablyai/orca**（parallel agents ADE——自己订阅跑任意 coding agent）；**CopilotKit/openmuse**（个人 agent 浏览器/终端/文件）；**Grok Build（xAI）**（8 并行 agent Society of Mind）；**graphify 120.7k★/browser-use 116k★** |
| 10 | OpenClaw（工具/插件配置面） | ✓ | **插件配置结构**（plugins.enabled 主开关/allow 白名单/deny 拒绝列表 deny 获胜/load.paths 额外文件目录/entries.<id>.enabled+config）；**启用命令**（openclaw plugins enable <plugin-id>；allow 设置时 id 必须在列表才能加载）；**配置验证**（plugin config 按 manifest JSON Schema 验证；用户经 entries.<id>.config；plugin 经 api.pluginConfig 注册时收到）；**channel setup contract**（defineChannelSetupContract——runtime 推断输入类型）；**installs 声明**（source npm+spec 声明式安装）；**tool plugins**（defineToolPlugin id/name/description/tools()；configSchema 可选——省略则 strict empty object schema manifest 仍含）；**自写技能最安全**（10 分钟 mkdir+SKILL.md） |

## 判重（双键检索结果）
- Dify 混合检索/重排：库内已落 §RAG 检索配置（r268A）——混合融合流程+rerank 配置+score threshold 语义+选型判据为独有增量 ≥40% → 落地（合并增量）
- n8n Chat Model：库内已落 §AI agent/§多agent——Chat Hub Custom Agents+模型参数+@mentions 为独有增量 ≥40% → 落地
- LangFlow 记忆/向量：库内已落 §记忆面（r268A）——MemoryBase 语义检索差异+配置字段+Vector Store 组件体系为独有增量 ≥40% → 落地
- Activepieces RBAC：库内已落 §企业治理（r267A）——四角色权限表+Custom Roles 细粒度+SCIM 为独有增量 ≥40% → 落地
- Make 错误监控/恢复：库内已落 §错误处理链（r267C）+wait-resume——四错误处理器语义+Incomplete executions+Scenario recovery+Version history 为独有增量 ≥40% → 落地
- Pipedream 组件发布：库内已落 §components（r266/r268C）——pd publish/--dev/dist/Custom Tools flag/Registry 贡献流程为独有增量 ≥40% → 落地
- Anthropic 结构化输出：库内已落 §输出校验/§工具描述——json_schema+additionalProperties 强制+strict tool use+JSON Schema 子集限制为独有增量 ≥50% → 落地
- deeplearning.ai 提示工程：并入记录（课程情报——方法论已在库）
- GitHub trending：并入记录（生态情报）
- OpenClaw 插件配置：库内已落 §技能安装/插件——plugins 配置结构+configSchema 验证+installs 声明式+tool plugins 为独有增量 ≥40% → 落地

## 独点落地（7 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r269C-1 | wb-execute-discipline | 3.25.0+ | Anthropic 结构化输出 json_schema 与 strict tool use（增量合并 §输出校验） | 工具 |
| r269C-2 | wb-execute-discipline | 3.25.0+ | Dify 混合检索与重排（增量合并 §RAG 检索配置） | 工作流 |
| r269C-3 | wb-execute-discipline | 3.25.0+ | Make 错误处理器四语义与场景恢复（增量合并 §错误处理链） | 工作流 |
| r269C-4 | wb-execute-discipline | 3.25.0+ | n8n Chat Hub 与模型参数（增量合并 §AI agent） | 工作流 |
| r269C-5 | wb-execute-discipline | 3.25.0+ | LangFlow MemoryBase 语义记忆与向量组件 | 工作流 |
| r269C-6 | wb-execute-discipline | 3.25.0+ | OpenClaw 插件配置体系（allow/deny/configSchema/声明式安装） | 可复用 Skill |
| r269C-7 | wb-execute-discipline | 3.25.0+ | Activepieces RBAC 细粒度权限（增量合并 §企业治理） | 工作流 |

## 复核
七独点均有当日实拉来源；均为增量合并或新面落地；并入记录：deeplearning.ai 提示工程课程/GitHub trending 生态。垃圾：本轮未产生临时文件。
