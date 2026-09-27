# r243-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（编排/队列面） | ✓ | Queue-based Graph Engine（1.9.0：workflow engine 重建围绕 queued graph execution，支持 pause/resume 中间、breakpoint、human-in-the-loop、trigger-based execution）；Graphon 架构（stored graph config→Graphon Graph，GraphEngine 事件转 Dify queue events；拓扑排序构建 DAG→识别就绪节点→前置完成触发→通知下游重复）；Knowledge Pipeline（visual pipeline raw data→高质量 context，source 到 context 可控）；Multimodal KB（text+image 一个 semantic space）；生产 agent 配置（max_steps 10/max_parallel_tool_calls 3/timeouts step 5s total 60s/queue rabbitmq routing_key/state_store）；Hybrid search 权重可配；Rerank 两型（model-based 专用 RerankModel/weighted score） |
| 2 | n8n（向量库/嵌入面） | ✓ | Embedding 模型必须匹配（ingestion 用啥 retrieval 用啥，不匹配向量空间不对齐）；Dimension matching #1 pitfall（text-embedding-3-large 3072 维，表/索引必须匹配，不匹配静默失败）；Metadata Toggle（1.74.0 带 metadata 让 agent 引源=信任信号，文档太大关 metadata）；Vector Store Memory 五模式（primary memory sub-node 二合一 vs RAG-as-tool）；dual-layer Postgres+pgvector nightly 增量管线（Schedule→last_vector_id→增量向量化） |
| 3 | LangFlow（安全/部署面） | ✓ | 无租户隔离（单进程不 enforce user 隔离/不限制磁盘网络访问；flow visibility 为易用非安全；多租户靠基础设施级安全）；生产安全（readOnlyRootFilesystem:true/密钥存 K8s secrets 或 Vault/禁 LANGFLOW_AUTO_LOGIN/反代+认证/不暴露端口）；Flow DevOps Toolkit SDK（1.9：lfx init 脚手架/版本化测试部署 flows 从终端/environments.yaml 控制部署）；公开部署（ngrok/zrok 转发外部 MCP server/serve API/公开 Playground） |
| 4 | Activepieces（Agent/模板面） | ✓ | Agent 三要素（name+description 目的上下文→详细 instructions 做什么/用什么数据/怎么响应→tools From Piece 内建集成或 From Flow 把 workflow 转 agent 可调工具）；工具四来源（app action/自己 automations/MCP server/上传文件）；从模板开始（lead routing/onboarding/reporting/content creation→review steps→adjust inputs）；分级模型流水线（便宜模型分类 intent+强模型生成，共享完全相同的检索上下文 canvas 传递）；需检查的先等 approval |
| 5 | Make（错误处理/数据存储面） | ✓ | Rollback error handler（停止 scenario 回滚支持事务模块 mysql/data store；不支持事务的 gmail 发邮件/dropbox 删文件无法撤销；失败 bundle 不继续；标记 error 不禁用）；Error Router 按 error.type 分型（Rate Limit→1 分钟等待/认证→通知管理员/数据→跳过；{{error.type}}/{{error.message}} 变量）；Data Store 失败重放（error route 写 bundle：scenario_name/bundle_data JSON/error_message/timestamp/replayed bool 修复后重放）；顺序处理（每 run 完成前不开始下一个，incomplete execution 存在时新 run 暂停）；agent workflow memory（data store 插入现有 scenario 不重建，失败路由防 corrupted state 写回 memory store） |
| 6 | Pipedream（组件开发面） | ✓ | Component API（hooks deploy/activate/deactivate 生命周期；props user input/interface HTTP timer；dedupe strategies）；Props 纪律（只放 3-4 个最相关选项，label 镜像用户语言）；$.service.db 跨 run 持久；共享 request helper（归一化 statuses/summaries/cursors，不导出 signing secrets/raw signatures/完整请求头）；dynamicProps.id 必须带回（后续 runAction/deployTrigger 必须含 dyp_ id） |
| 7 | Anthropic（skill 创作面） | ✓ | Context window is a public good（skill 与 system prompt/历史/其他 skill 元数据共享；启动只预载 metadata，SKILL.md 相关时才读，附加文件渐进）；Start with evaluation（先在代表任务上跑 agent 观察挣扎/缺上下文→针对性建 skill；task 失败是 spec，模型已处理好不进 skill 每 token 与对话竞争）；每 skill 3-5 测试查询（触发/不触发/模糊边缘，跨模型层）；三层选择（prompt caching 稳定指令长参考多轮重复/tools scripts 确定性操作/extended thinking 只给难推理）；Self-Correcting Loop（generate→verify→fix→verify again）；Skills 组合（compliance skill 调 document analysis skill） |
| 8 | agentskills.io（市场面） | ✓ | Anthropic 2026-04 末开放 Agent Skills open standard hub agentskills.io；市场质量参差（平均公开 skill 6.2/12 分 SkillsBench；36% 危险）；Agensi 8 点安全检查（prompt injection/data exfiltration/secret detection/dangerous commands/obfuscation/external fetches/credential access/privilege escalation 每条 listing 上线前扫）；curated registry 价值（vetted 可靠/自动扫描/兼容性测试/可信任安装）；skills.sh ~3.07M visits/mo 自动 telemetry 收录 |
| 9 | docs.openclaw.ai（skills 面） | ✓ | skills update --all（更新所有工作区）；--version 指定版本/--force 强制；skill 即放即用（cp -r 进 skills/ 目录无构建/编译/配置，下轮 run 拾取）；ClawHub 发布/同步（openclaw skills 安装更新或 clawhub CLI 发布）；5000+ 社区技能收录（聊天框 search 再 install） |
| 10 | GitHub（生态面） | ✓ | deepseek-harness 208,095★（模块化框架 "Everything is a Plugin"——数据到模型每组件可插件替换扩展）；MemOS 11,502★（self-evolving memory OS：ultra-persistent/hybrid-retrieval/cross-task skill reuse 35.24% token 节省）；i-have-adhd（Trending #1 让 AI 先说答案的输出技能）；ToolJet 40,999★（enterprise app generation from prompt/Claude Code/Codex/Cursor over MCP）；jev-chat-jarvis 6,591★（手机 IM 内对话副驾 QQ/X/飞书）；wechat-bot 11,369★（多平台 IM AI Agent） |

## 判重基准
双键检索（相对 r241-A/B/C + r242-A/B/C 已落章节）：Dify（r242-A 落 agent 一等实体——"Queue-based 执行引擎+pause/resume"独有增量深化）；n8n（r242-A 落记忆子节点选型——"embedding 匹配纪律+metadata 引用"独有增量深化）；LangFlow（r241-C 落自托管安全——"DevOps Toolkit 终端部署"独有增量深化）；Activepieces（r242-B 落 durable execution——"agent 三要素+分级模型"独有增量深化）；Make（r243-A n8n dead-letter 已落——"rollback 事务边界+error.type 分型"独有增量深化）；Pipedream（r242 落 trigger 部署语义——"props 纪律+hooks 生命周期"独有增量）；Anthropic（r242-B 落 SKILL.md 触发纪律——"创作三层选择+先评测后建"独有增量深化）；agentskills.io（r242-A 落 skills CLI——"8 点安全检查单"独有增量）；openclaw（r242-A 落多源安装矩阵——"update --all/即放即用"重叠>60% 独有增量<40% 不单落）；GitHub（r242-C 落 MCP RCE Guard——"Everything-is-a-Plugin+跨任务 skill 复用"独有增量深化）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify Queue-based Graph Engine | pause/resume/breakpoint/HITL/trigger-based；Graphon 拓扑排序执行计划 | 工作流 | wb-execute-discipline |
| ② n8n embedding/维度匹配纪律 | ingestion-retrieval 同模型；维度不匹配静默失败；metadata 引源 | 工作流 | wb-execute-discipline |
| ③ LangFlow DevOps Toolkit+安全边界 | lfx init 脚手架 environments.yaml 终端部署；无租户隔离责任在己 | 工具 | wb-execute-discipline |
| ④ Anthropic Skill 创作三层+先评测后建 | cache 稳定指令/script 确定性/extended thinking 难推理；task 失败是 spec | 可复用 Skill | wb-execute-discipline |
| ⑤ Everything-is-a-Plugin+跨任务 skill 复用 | 组件全可插件替换；记忆 OS 混合检索 35% token 节省 | 工具/工作流 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
