# r238-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（Agent 编排/发布面） | ✓ | Workflow Studio 可视化协作画布（模型调用/知识检索/工具/代码/分支/触发器/人工审核）；发布前测试三类问题（知识库有明确答案/答案模糊/完全超出范围——agent 是否承认不确定用 fallback 不编造；logs+annotation 显示每轮工具与检索段落）；publish_agent 发布为 AgentConfigSnapshot 快照可回滚；Chat/Embed/API 三出口（public chatbot URL 主题化+conversation starters；test 不影响发布版）；Agent best practices（清晰工具描述/适当迭代限制防 runaway 成本/详细指令/记忆管理平衡上下文 token）；多模型路由（cheap 模型接简单问题 strong 接难题，第三模型分类）；模型 agent mode Function Calling/ReAct 自动显示 |
| 2 | n8n（自托管/生产部署面） | ✓ | 队列模式架构（Webhook/Main node UI+API 不执行只推 job 到 broker；Redis 队列弹性缓冲扛尖峰；无状态 workers 拉 job 执行 `--scale n8n-worker=3`）；PostgreSQL+Redis+Queue mode 唯一生产 setup 其他都临时；切换时机 ~80% CPU（EXECUTIONS_MODE=queue+QUEUE_HEALTH_CHECK_ACTIVE=true）；生产纪律五条（pin 版本不 :latest 升级可破 webhook workflows/execution pruning 必须否则 2-4 周磁盘满/encryption key 一次生成存 secrets manager 绝不 Git/SQLite 不能并发/Community 无 SSO+audit 需 Enterprise；K8s 100+ workflows）；Render 托管（render.yaml IaC 托管数据库/autoscaling）；N8N_BASIC_AUTH |
| 3 | GitHub（Trending/生态面） | ✓ | Trendshift 周榜（Orca ADE fleet parallel agents desktop/mobile/remote runtime；pi AI agent toolkit unified LLM API+agent loop+TUI+coding agent CLI）；2026-09-09 Agent Skills 周（ponytail 132.1K +12,598/humanizer 45.4K 去 AI 味/hyperframes 47.7K 视频）；GNAP Git-Native Agent Protocol 4 JSON 文件协调 agent no server no DB；siyuan 46.5K 隐私优先自托管知识工作空间人+AI agent 协作；LibreChat 44.9K（Agents/MCP/Skills/多模型/Code Interpreter/OpenAPI Actions/消息搜索/安全多用户 auth）；Tencent AI-Infra-Guard；anthropics/skills 官方组织方式 |
| 4 | Anthropic（Skills 规范面） | ✓ | 渐进披露三级（Level 1 YAML frontmatter 常载 system prompt ~100 tokens 只够判断何时用；Level 2 SKILL.md body 触发时载 <5k tokens 完整指令；Level 3 linked files 捆绑脚本按需近乎无限）；SKILL.md body 保持 <500 行逼近拆 references/；技能是文件夹不是 markdown 文件（整个文件系统是 context engineering；告诉 Claude 文件清单它会在适当时读；references/api.md 拆签名用法）；不过度约束（高重要领域除外；编码特定意见/知识/best practices）；字段规格 name≤64 字符 description≤1024 |
| 5 | Pipedream（SDK/MCP 开发者面） | ✓ | remote MCP server（https://remote.mcp.pipedream.net + x-pd-external-user-id 头；agent 挑工具 auth 已处理）；SDK（pip install pipedream；Pipedream(client_id/client_secret/project_id/project_environment)；pd.components.list({app}) 多 app 并发 Promise.all；external_user_id 稳定 ID）；MCP+OpenAI SDK（tools:[{type:'mcp', server_label, server_url}]）；managed auth connectAccount onSuccess/onError；前端 ComponentFormContainer componentKey slack-send-message；异常 4xx/5xx 抛 |
| 6 | Make（Observability 面） | ✓ | Reasoning Panel（实时看 agent 怎么想/调什么工具/为何走每条路径；视觉 trace 替代 log 搜索与推断；11pm 出问题能看到发生了什么）；场景=orchestration/state/logs 单一事实源；Make Grid（整个自动化全景实时地图；跨平台同视图 n8n workflows/claude managed agents/relevance ai assets 依赖追踪）；audit-ready 模式（trigger→evidence capture→policy gate）；Maia reasoning out loud 无黑盒；新 agent 架构暴露每个决策 |
| 7 | skills.sh（热门技能/规模面） | ✓ | 规模（~669,670 skills 2026-06；top vercel-labs find-skills 2.0M installs；Anthropic frontend-design 531.8K 发布 5 个月）；热门技能（obra/superpowers Brainstorming 147.7K；ai-video-generation 2.2 万日装并列第一；google-agents-cli-scaffold/deploy/observability 系列 9,8xx 安装；Deep Research Pro 最下载研究技能；GOG Google Workspace 184,900+；Karpathy Behavioural Skill 172K+ 零运行时依赖单 SKILL.md）；2026-09-03 榜单 AI 视频图像生成包场；top 3 hubs（explainx 10k+ reviewed；skills.sh 57k+ public；SkillsMP 1.2M+ scraped 网页搜索）；proactive agent/smart charts 高下载效率技能 |
| 8 | OpenClaw（Hooks/自动化面） | ✓ | 内部 hooks 事件驱动脚本（agent lifecycle 事件 /new /reset /stop+session compaction+Gateway 启动+消息流；目录自动发现 openclaw hooks 管理）；插件 hooks 进程内扩展点（校验/修改 agent 运行、工具调用、消息流、会话生命周期、子 agent 路由、Gateway 安装/启动）；hooks 纪律（重启/进程退出丢 in-flight 工作→副作用短而有界：handler 内 await+网络超时+限制数据大小+幂等；不用 void doHeavyWork(e) 逃逸 handler 等待/错误边界）；webhooks HTTP 外部回调 |
| 9 | deeplearning.ai（社区/课程细节面） | ✓ | Agent Skills 课程 10 视频 2h19m（Prompt Engineering→Agent Engineering 范式转移）；社区总结（Custom Workflows/Skills L12 自动化重复 SDD prompts；Skills 项目级或全局；MCP servers 正被 Skills+CLI tools 部分替代；Agent Replaceability L13 AGENTS.md/Agent Skills/MCP/ACP 开放标准不锁单一 agent/IDE）；Skill 关键=description 决定是否加载（最常被草率写的一行）；组合思维（最强能力来自组合多技能非单体 agent）；Agentic AI 课程（reflection/tool use/planning/multi-agent 弧线+同一个 research-agent 贯穿五模块+Self-Refine 论文+LLM-judge position bias 警告） |
| 10 | 腾讯 SkillHub（榜单/生态面） | ✓ | GitHub Skills 热榜（anthropics/skills 官方组织方式；msitarzewski/agency-agents AI agency 拆专业 Agent 清晰任务交付；garrytan/gstack CEO/设计/工程管理工具组合；ui-ux-pro-max）；WeHub 中文 Agent Skill Top 200（skillhub-{排名}-{skill名} 独立仓库）；2026-08 热榜 Agent Skills 席卷（ayghri/i-have-adhd 23.3K 让 Agent 别把答案埋在废话里；TencentCloud/TencentDB-Agent-Memory 23.9K 团队级 Agent 记忆中枢；virgiliojr94/book-to-skill 24.3K 技术书 PDF 转 Claude 技能）；官方厂商 Skills（Redis agent-skills/Svelte ai-tools/Nuxt ui/LiveKit agent-skills）；mukul975/Anthropic-Cybersecurity-Skills 754 安全技能映射 MITRE ATT&CK/NIST CSF 2 五大框架 |

## 判重基准
双键检索：Dify（r238-A/B 已落，独有增量=发布前三类测试+AgentConfigSnapshot 快照+三出口）；n8n（r238-B 已落，独有增量=队列模式生产架构 UI/执行分离+生产纪律五条）；GitHub（多轮已落，独有增量=GNAP git 原生 4 JSON 协调+siyuan 人机协作知识空间）；Anthropic（多轮已落，独有增量=渐进披露三级 token 量化 100/<5k/无限+文件系统即披露）；Pipedream（r238-A/B 已落，remote MCP 端点与既有组件重叠并入不单列）；Make（r238-A/B 已落，Reasoning Panel 与 r238-A 激进透明重叠并入不单列）；skills.sh（r238-B 已落，独有增量=规模实证 669K/2M+热门技能形态零依赖）；OpenClaw（r237-C 已落 hooks，独有增量=副作用有界纪律+两类 hooks 分工）；deeplearning（多轮已落，独有增量=MCP 被 Skills+CLI 部分替代+可替换性开放标准四件套）；腾讯 SkillHub（r237-A 已落，独有增量=书转技能+Agent 记忆中枢+754 安全技能框架映射）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 发布前三类测试+快照 | 有答案/模糊/超范围三分类测；publish_agent 快照可回滚；Chat/Embed/API 三出口 | 工作流 | wb-execute-discipline |
| ② n8n 队列模式生产架构 | UI/执行分离+Redis 缓冲+无状态 worker；80% CPU 切换；pin 版本+pruning+密钥外置五纪律 | 工作流 | wb-execute-discipline |
| ③ GNAP+siyuan | git 原生 4 JSON 协调 agent 无 server 无 DB；隐私优先自托管知识空间人机协作 | 工具 | wb-execute-discipline |
| ④ 渐进披露三级 token 量化 | frontmatter 100 tokens 常载/body <5k 触发/捆绑文件按需；正文 <500 行拆 references；文件系统即披露 | 可复用 Skill | wb-execute-discipline |
| ⑤ OpenClaw hooks 纪律 | 副作用短而有界+handler 内 await+幂等；不逃逸 handler；内部 hooks vs 插件 hooks 分工 | 工作流 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：wb-context-compressor 长度控制合并评估连续 3 轮挂账——本批批末为最终落地窗口；本轮三级渐进披露（100/<5k 量化）直接可作 compressor 优化输入。
- 垃圾：本轮未产生临时文件。
