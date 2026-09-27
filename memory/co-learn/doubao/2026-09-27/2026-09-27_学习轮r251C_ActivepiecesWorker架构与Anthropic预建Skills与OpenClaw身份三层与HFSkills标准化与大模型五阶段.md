# r251-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Activepieces（worker/execution 面） | ✓ | Worker=跑 flow 的容器（从 Redis 拉 job→沙箱池分配→engine 执行→结果回 app）；AP_EXECUTION_MODE 沙箱策略（UNSANDBOXED/SANDBOX_PROCESS/SANDBOX_CODE_ONLY/SANDBOX_CODE_AND_PROCESS；企业推荐 SANDBOX_CODE_ONLY V8 隔离=多租户安全+非特权容器+Activepieces Cloud 同款）；AP_CONTAINER_TYPE（APP API only/WORKER worker only/WORKER_AND_APP both；同镜像两角色）；AP_WORKER_CONCURRENCY（默认 5；生产推荐 1 一 worker 一 flow；0.5vCPU/1GB 每 worker 约 300MB 温进程开销）；AP_REUSE_SANDBOX=true 复用 engine 进程；Crash recovery（runs durable 自动 re-queue；rolling worker 无需 drain 无 in-flight loss）；Autoscaling（worker 是扩缩单位） |
| 2 | Make（Data Store/watch 面，实拉偏泛） | ✓ | NATS KV 分布式配置管理七纪律（use appropriate history 平衡版本与存储/watch handlers 动态响应/TTL 清理临时数据/namespaces 前缀 app.db./monitor bucket size 告警/test failure scenarios 验证断连/document key schemas）；MongoDB change streams 实时（需 replica set/sharded cluster 不工作 standalone；break 后第 4 事件被消费丢弃用 change_count>3 防 race）；n8n-nodes-keyvalue（KeyValue Trigger 监视目录新/改记录触发；poll 默认 30s 最小 5s）；Ditto store observer backpressure（registerObserverWithSignalNext 控制更新频率） |
| 3 | Pipedream（schedule/cron 面） | ✓ | Schedule 触发属性（interval_seconds/cron/timestamp/timezone_configured/timezone_utc）；props timer $.interface.timer（组件内定时 source：intervalSeconds 或 cron+timezone）；1 秒级 cron jobs（Custom Interval Every second；Daily/Weekly/Monthly；Cron Expression 0 0 * * * 午夜）；免费 tier 也有 schedule triggers（2026-04 起全 plan）；业务小时 cron（*/15 8-17 * * *）；默认 timeout 60s |
| 4 | Anthropic Skills 官方库（API/managed agents 面） | ✓ | 预建 Skills（API 里 PowerPoint pptx/Excel xlsx/Word docx/PDF pdf）；Agent Skills 经 messages API code execution tool 集成；Managed Agents attach pre-built/custom/从 GitHub repo 加载；Skills=文件夹（SKILL.md/docs.md/slide-decks.md/apply_template.py；Git 版本化；渐进访问 domain expertise）；自定义 Skills 安全（附可执行代码谨慎/不硬编码敏感信息/下载启用前审查/外部服务用 MCP 连接）；Skills 自动触发（agent 相关时自动调用） |
| 5 | OpenClaw（agents concepts/identity 面） | ✓ | 身份三层（Soul SOUL.md 行为哲学/声音/价值观；Identity IDENTITY.md 呈现/persona；Configuration openclaw.json+TOOLS.md 技术能力/模型选择）；stateful agent（记忆保留；简单记住名字/复杂调试会话进度）；层级 agent 模型（parent 拆任务/子 agent 隔离 session 执行返回结果/result routing）；heartbeat 自主运行（定期查任务列表评估行动或等待下一周期）；腾讯云 PG 记忆+向量后端（长期记忆/知识检索/多轮）；Gateway 架构（central hub 通道消息→AI brain→Skills→Memory） |
| 6 | GitHub agent 生态（awesome lists/仓库面） | ✓ | PraisonAI（自反思生产级多 agent；3.77μs 实例化；100+ LLM；MCP；route/parallel/loop/repeat agentic workflows；内置记忆；Py+JS SDK）；OpenAgents（多协议 WebSocket/gRPC/HTTP/MCP/A2A）；superpowers 269K stars（agentic skills 框架——技能取代逐行编码）；OfficeCLI 31,251 stars（AI agents 用 Office 套件单二进制无需装 Office）；graphiti 31,170（实时知识图谱）；microsoft/autogen 59K/composio 28.8K；iGPT（邮件线程转 JSON for agents）；DarkMoon（自托管渗透 MCP host 80+ 工具）；Atomic Agent（本地 CLI 56 built-in tools） |
| 7 | Hugging Face（agents/skills 面） | ✓ | HF Skills=标准 Agent Skills 格式（SKILL.md YAML frontmatter；兼容 Claude Code/Codex/Gemini CLI/Cursor；OpenAPI+JSON schema 工具定义）；huggingface_hub 抽象层（数据查/模型卡提取评测分/跨架构比较选型/远程训练 AutoTrain+HF Training Cluster 微调；uv 内联依赖 PEP 723 脚本零本地安装）；Skill Card 标准化（类似 Model Card：能力/限制/适用场景/评估指标）；版本管理（Skill 像模型版本控制 A/B 测试；兼容性矩阵标注各模型表现差异）；AWS 合作（SageMaker 部署 6 技能 planner 协调 5 其他） |
| 8 | ModelScope（Agent/创空间面） | ✓ | ModelScope-Agent 开源框架（github.com/modelscope/modelscope-agent；连接模型能力与万物；魔搭开源版 GPTS 个人超级智能体；modelscope-agent-7b 核心开源模型本地可用；DashScope 托管无需本地 GPU）；魔搭创空间部署 Skill（Gradio/Streamlit/Docker/静态站；创建/代码同步/部署/日志监控/明文与 secret 变量管理/自动诊断修复）；魔粒体系（全站激励积分）；技能服务墙（展示商业服务）；Agent 大本营 |
| 9 | 智谱 AgentMore/清流 | ✓ | AgentMore=智谱清言 AI 智能体协作与 Skills 扩展平台（2026-05-25；多 Agent 协作/技能市场/任务执行与工作流编排；网页/APP 创建 Agent 安装 Skills；基础免费）；智谱清流=企业级智能体开发平台（GLM-4 底座；零/低代码编排；企业知识库 RAG；效果评测迭代闭环；AutoGLM 界面操作代理；平台编排+代理执行组合；API/SDK/URL 三集成）；大模型五阶段（Chat→Coding→Agent→Co-work→Autonomous AI：一次性问答/可运行代码/多步任务链/可复核专业成果/持续自主运行系统）；AutoGLM 50+ 步长操作跨 app |
| 10 | 腾讯 SkillHub | ✓ | SkillHub=腾讯云基于 OpenClaw 官方开源生态的本土化技能平台（2026-03-11 上线；1.3 万→8 万+技能；ClawHub 本土化高速镜像；中文搜索；国内节点分发秒速安装；Top 50 精选榜；三线并行安全审核全量扫描；兼容 WorkBuddy/QClaw/ima）；SkillPay 支付体系（2026-07-16；技能分发+Agent 调用+支付同链路；来源认证/内容完整性校验/可信调用入口；微信支付底层）；TRACE 评测体系（识别高质量 Skill）；SkillHaS 端侧隐私保护（身份证/人脸/文档 7 万+ 检测）；DeepSeek Harness Plugin 广场（9.7 千 GitHub MIT 开源 Plugin） |

## 判重基准
双键检索（相对 r224-r250C+r251A/B 已落章节）：Activepieces（r232-A 治理四件套/r227 自托管——worker 拆分 AP_CONTAINER_TYPE+SANDBOX_CODE_ONLY+concurrency=1+crash recovery 为独有新面）；Anthropic Skills（r249-B frontmatter 契约已落——本面 API 层 code execution tool 集成+Managed Agents 挂载+预建技能目录+自定义安全审查为 ≥40% 独有增量，重叠>60% 按增量判定合并保留增量落地）；OpenClaw（r251-A gateway 路由/r249 skill 开发——身份三层 SOUL/IDENTITY/config+heartbeat 自主运行为独有新面）；Hugging Face（r246/r250 模型面——HF Skills 标准化+Skill Card 三件套+版本管理 A/B 为独有新面）；智谱（r249-C 国内平台生态已落——AgentMore/清流细节+大模型五阶段为独有增量面）。未选素材：Pipedream schedule（r251-A 组件 API 已覆盖部分，schedule 属性增量中等）；GitHub 生态仓库速览（r249-A trending 已落，具体新仓库信号增量中等）；ModelScope 创空间（r250-B 部署私有化已落，创空间 Skill 增量中等）；SkillHub（r249-C DSH 生态已落，SkillPay/TRACE 增量中等）；KV 配置管理（r244-B DataStore 已落，NATS 治理纪律切入面相近）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Activepieces worker 架构与沙箱 | 拆 app/worker+CODE_ONLY+并发 1 | 工具 | wb-execute-discipline |
| ② Anthropic 预建 Skills 与 API 集成 | code execution tool+挂载+审查 | 工具 | wb-execute-discipline |
| ③ OpenClaw 身份三层与 heartbeat | SOUL/IDENTITY/config+自主循环 | 工作流 | wb-execute-discipline |
| ④ HF Skills 标准化与 Skill Card | OpenAPI 定义+Card 三件套+版本 | 可复用 Skill | wb-execute-discipline |
| ⑤ 大模型五阶段（智谱） | Chat→Coding→Agent→Co-work→Autonomous | 工作流 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
