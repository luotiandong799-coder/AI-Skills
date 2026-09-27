# r237-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（Agent 节点/策略面） | ✓ | Agent Strategies（Function Calling vs ReAct 按模型能力选，插件化）；Agent Node=workflow 内大脑；Allowed tools 白名单（指定名字只发这些工具，留空全量）；Agent Strategy Plugin（session.tool.invoke()）；Human Input Node v1.13.0（暂停等人审，批准/编辑/改路由）；Agentic RAG（迭代分析意图→选工具/来源→重写查询→评估证据→重试/回退）；Legal Research Agent 模板（动态选 1-2 集合，不足 Google fallback） |
| 2 | n8n（AI Gateway/LLM 路由面） | ✓ | LLM Routing 架构（查询级成本强制+SLA 分级：premium 快模型/free 便宜+Failover routing 监测 provider 可达性自动改道）；routing 决策在 session 级 token 处理前；路由子工作流（Anthropic/Gemini/Mistral/OpenAI 归一化响应+token 用量+成本表）；Kestrel 智能路由（ML 分类器按复杂度选模型+语义缓存省 60%） |
| 3 | GitHub（榜单 B 面） | ✓ | siyuan 46.5K（隐私优先自托管知识工作区，人+AI agent 协作）；LibreChat 45K（Agents/MCP/Skills/多模型切换/message search/Code Interpreter/Secure Multi-User Auth）；jev-chat-jarvis（手机对话副驾 QQ/X/飞书，当日 +182 stars）；Ollaya（Ollama 式 Jev 决策模型服务）；shadcn-ui/lint（agent-first linter for Tailwind：写 agent 可验证的设计系统规则）；vanna（Text-to-SQL via Agentic Retrieval） |
| 4 | LangFlow（1.10-1.12 面） | ✓ | 1.10（Assistant 建整个流+Memory bases 长期语义记忆+DB Providers 可配置向量库+7 语言）；1.10.3 安全加固（outbound request protection+Docker+MCP stdio/component 加固）；1.11（HITL checkpoints+A2A 协议+AG-UI streaming+Multi-Vector Retrieval）；1.12（OpenTelemetry service health+flow runs）；1.10.0 preload.py CoW 内存共享；1.8 streamable HTTP MCP |
| 5 | Activepieces（AI Agent builder 面） | ✓ | 一句话建 agent（prompt 框写需求→自动草拟名字+指令+所需工具）；Agent 一等实体（命名/brief/对话/复用）；AI Copilot（自然语言建议步骤+流坏定位）；agent 知道何时 pause 等人审（草拟+查规则+review 再发）；你选工具（app action/自动化/MCP/文件）+你的模型你的 key（admin 一次配置） |
| 6 | 智谱 AgentMore（功能面） | ✓ | AgentMore（智谱清言多 Agent 协作：最多 5 Agent 拉入同群组；头脑风暴/任务分配双发言模式；7×24 云端+共享工作区+自我进化）；Skills 技能广场（推荐/SkillHub/开源社区三类来源一键安装）；任务拆解多步多 Agent（调研→写作→分析→总结）；AutoGLM（自主执行 50+ 步跨 app）；AutoGLM 版 OpenClaw（官网一键 OpenClaw+飞书机器人配置数小时→几分钟）；GLM-4V 多模态（图生文/图生视频+画框/截图/读网页工具） |
| 7 | deepseek-plugin.org（DeepSeek Harness 面） | ✓ | DSH（Everything is a plugin：模型/工具/技能/会话/沙箱/存储/循环/调度/UI 全可插拔）；官方内置 100+ 插件；Plugin 广场 9.7 千 GitHub MIT 插件；dsh-market（harness 内浏览搜索安装+按已装推荐）；modlens（贴图提取 OCR/布局/语义证据）；skills-management 插件（管理本机全部 coding agent 技能一键收编+6600+ 技能市场+注入开销 token/字符统计排序+模型可见性治理+每日同步）；graph-memory（结构化三元组建知识图谱，压缩上下文 75%，跨会话复用）；dsh-genui（回复转交互 UI） |
| 8 | agentskills.io（目录面） | ✓ | AgenticSkills 189+ curated 16 类别；agentskills.me 492 skills；agentskills.codes 开源注册表；top-agent-skills 204 skills 20 类别（按真实效用排）；agskills.dev 423 plugins/2,849 skills；目录选择矩阵（生产→explainx；开源→skills.sh；细分→SkillsMP；GCP→Google /skills；Azure→Microsoft /skills；参考实现→Anthropic GitHub） |
| 9 | WaytoAGI（知识库面） | ✓ | 900 万 AI 学习者开源知识库；社区每日整理 AI 工具/行业资讯/论文速读；Prompt 工程教程（从帮我写到替我思考）；Coze/Dify/OpenClaw 框架入门到实战；飞书知识库问答机器人；投资与创业者目录 |
| 10 | ModelScope（Skills Central/Agent 面） | ✓ | Skills Central（npx skills add/modelscope skills add/curl install.sh 三通道安装）；awesome-skills 合集（自动记录成功经验与错误）；Agent 大本营（勾选内置 tool：图片生成/识别/艺术字；API 注册为 tool 成 smart API；AgentFabric 快速创建）；向日葵 MCP 上架；Agents-A1（35B 达万亿参数性能：agentic reasoning+tool use+科学推理） |

## 判重基准
双键检索：n8n（r236-A/C+r237-A 已落，本条独有增量=LLM 路由三模式 token 前决策+查询级成本强制）；LangFlow（r236-C 已落 1.8/1.9 面，本条独有增量=1.11 HITL+A2A+AG-UI+1.12 OTel+CoW preload）；Dify（r236-A/C+r237-A 已落，本条独有增量=Agent 策略选型+Allowed tools 白名单+Agentic RAG 迭代框架）；DSH（r236-A/B 已落注入成本/code-as-action，本条独有增量=全插件化+skills-management 注入开销统计+graph-memory 三元组压缩）；Activepieces（r236-A 已落 AI-ready 目录，本条独有增量=一句话生成 agent+AI Copilot）；ModelScope（r236-C 已落平台面，本条独有增量=Skills Central 三通道+smart API tool）；WaytoAGI 独有增量不足 40%，不落。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① n8n LLM 路由三模式 | 查询级成本强制+SLA 分级路由（token 前决策）+Failover 自动改道 | 工作流 | wb-execute-discipline |
| ② LangFlow HITL+A2A+OTel | 1.11 人工检查点+A2A+AG-UI streaming；1.12 OpenTelemetry；CoW 内存优化 | 工具 | wb-execute-discipline |
| ③ Dify Agent 策略+白名单+Agentic RAG | Function Calling vs ReAct 插件化选型；Allowed tools 白名单；迭代检索框架 | 工具 | wb-execute-discipline |
| ④ DSH 全插件化+技能管理 | 能力全可插拔；skills-management 注入开销统计+模型可见性治理；graph-memory 75% 压缩 | 工具 | wb-execute-discipline |
| ⑤ Activepieces 一句话 Agent+AI Copilot | 一句话生成 agent（名字+指令+工具推导）；agent 一等实体；Copilot 排障 | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造；WaytoAGI 增量不足按规则不落。
- 功能套件检查：wb-context-compressor 长度控制合并评估继续挂账；wb-ponytail 无变化需求。
- 垃圾：本轮未产生临时文件。
