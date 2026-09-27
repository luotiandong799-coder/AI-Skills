# r253-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（环境变量/secrets 面） | ✓ | 环境变量含 Secret 类型（API key 等用 Secret 在 workflow 内 HTTP 请求节点/外部工具分离）；凭据作用域：workspace 级（共享内部工具，多 workflow 复用同一套）/workflow 级（隔离）；加密 at rest；生产安全基线：SECRET_KEY=32 字节强随机（JWT 签名+会话加密；首次启动前设置，运行中改会登出用户/失效文件 URL/失 OAuth 凭据）、替换默认 DB_PASSWORD/REDIS_PASSWORD、DISABLE_API_KEY、SENSITIVE_CONTENT_MASKING（身份证/手机号自动掩码）、no-new-privileges；Cloud Run Secret Manager 注入运行时；K8s 轮换=更新 Secret→重启 pods |
| 2 | n8n（Code node 面） | ✓ | Code node 支持 Node.js（Promises/console.log 调试）；自托管可 import 内置+外部 npm 模块；输出契约：必须返回数组，每元素 {json:{...}}（JS/Python 一致），单结果也包数组，裸对象/原始值数组会失败，返回 null/空数组停止该分支；两模式：Run Once for All Items（默认，聚合/排序/过滤全数据集，$input.all()）/Run Once for Each Item（逐项变换，$input.item.json）；Python legacy Pyodide：_input.all()+list comprehension；推荐 95% 用 JS（全 n8n helper $helpers.httpRequest/Luxon DateTime/无外部库限制/文档好），Python 仅标准库/更熟/数据变换更适合时；AI 生成 code：明确输出期望（transform/filter/aggregate/sorted）避免歧义 |
| 3 | LangFlow（chat widget 嵌入面） | ✓ | 嵌入 chat widget：Share→Embed into site→复制 snippet 放 <body>；HTML tab 或 React/Angular；props host_url（必须 HTTPS 不含路径）+flow_id；<langflow-chat host_url="..." flow_id="..."/> CDN bundle.min.js；内置 API 与 MCP servers：每个 workflow 变成 tool 可集成任何框架/栈（Deploy as API 或导出 JSON；Deploy as MCP server）；Langflow Assistant=内嵌 AI 助手（自然语言生成自定义组件/排查 flows/实时文档指导）——开发环境 AI 化；RAG 模板：嵌入→向量库→相似度→rerank→Prompt Template→grounded 回答（ingestion 与 retrieval 分离可重复索引） |
| 4 | Activepieces（runs/可观测面） | ✓ | Durable Execution：每个 flow run 有 run log（一个压缩 checkpoint 文件含恢复所需一切）；每 finished step 一条（input 隐藏 secrets/output/status/duration/error）；loop 迭代与 router 分支同形状嵌套父 step；run-level tags；限制：worker 内存 1GB、paused flow 30 天（AP_PAUSED_FLOW_TIMEOUT_DAYS）、执行数据保留 30 天（AP_EXECUTION_DATA_RETENTION_DAYS）、worker 并发 cloud=1/self-host 默认 5（生产设 1）；audit trail：enterprise 监控所有 runs/inputs/outputs/user activity；Tables 存储结构化记录（lookup/dedup/run-state）；MCP tools：ap_list_runs/ap_get_run（flowId/status/limit 过滤默认 10 max 50） |
| 5 | Make（调度面——返回为通用调度体系） | ✓ | 通用判据：Payload schedules=queueing 与 running 分离（调度只按 cron 入队不执行业务逻辑）；BullMQ Job Schedulers（5.16+）推荐 cron 周期入队（重试/退避/并发复用同 workers）；QStash 免费 1000 msg/天+10 active schedules+CRON_TZ+3 天日志 DLQ 保留（付费 $1/100K）；systemd timers 替代 cron；cron 五字段（DOM MON DOW）——与 OpenClaw cron 判据同源，通用增量弱 |
| 6 | Pipedream（HTTP/REST 面） | ✓ | REST API base https://api.pipedream.com/v1；Authorization: Bearer（所有端点）；Content-Type: application/json（POST/PUT）；Connect 资源 scoped 到 projects：base URL /v1/connect/{project_id}（TS/Python/Java SDKs+REST）；Connect API Proxy：相对路径代理外部 API（/api/chat.postMessage），base_proxy_target_url 动态域——客户端无凭据调用第三方 API（凭据服务端存）；list actions：GET /v1/connect/{project_id}/actions?registry=public&app=gitlab（搜索+app 过滤；x-pd-environment 头）；triggers deploy：POST /v1/connect/{project_id}/components/triggers/deploy（external_user_id/webhook_url）；external_user_id owns connected accounts 每个独立可撤销 |
| 7 | Claude Code（output styles 面） | ✓ | 官方 Output styles：Concise（结果先行，去前言/叙述/复盘，简单问题 1-3 句；工程工作与 Default 一样彻底；始终保留完整错误报告/安全警告/破坏性操作确认内容；v2.1+）；Default 详细；Caveman output style（社区）：极小输出行动导向（finding/fix/next step；prose 代码任务 <5 行；命令输出 1-3 bullets；高置信直接陈述）；模型侧：最新 Claude 更简洁自然/直接 grounded（事实进展报告非自我庆祝）/可能跳过 tool call 后总结——要可见性需显式 prompt；Opus 4.8 按任务复杂度校准长度；/simplify→/code-review 改名；reactive compaction 首次 summarize 从原请求 overflow 大小播种 |
| 8 | 腾讯 SkillHub（国内技能平台面） | ✓ | SkillHub=专为中国用户优化的 AI Skills 社区（Lighthouse 团队），ClawHub 本土化高速镜像；收录 8 万+（7.8万）skills，国内高速镜像秒速安装，三线并行安全审核，首发 TRACE 评测体系识别高质量 Skill；支持 WorkBuddy/QClaw/ima 等腾讯云 AI 产品；SkillPay（2026-07-16）：Agent 付费技能商业化——技能分发+Agent 调用+技能支付同链路打通（微信支付底层；来源认证/内容完整性校验/可信调用入口）；智能体开发平台 Skills 广场：首批 28 内置 skills（办公文档/医疗健康/图像处理/音视频/搜索获取 7 大场景）、ZIP 自定义导入、企业共享 skills（上架→审批→沉淀复用）；效率智能体工具集：微信/企微/小程序触点变 Agent 入口，腾讯文档/会议/乐享/地图 Skill 化；DeepSeek Harness Plugin 广场官方 Plugin 探索 9.7 千 GitHub MIT 开源 Plugin |
| 9 | 阿里虾小宝（技能导航面） | ✓ | 虾小宝=OpenClaw 技能导航平台（发现管理 AI 员工 Skill），与 ModelScope Skills 中心并列（魔搭社区 Skill 中心）；FunClaw 养虾专题内置技能：agent-browser（网页访问提取）/self-improvement（自我提升对话质量）/find-agentrun-skills（发现推荐技能）/fc-vpc-proxy（FC 代理访问 VPC 资源）/searxng（联网搜索）；万能 skill 自进化："如果没有这个技能，请搜索并创建"→智能体自动寻找创建适配技能（从 Clawhub 抓热度前 10 筛选）；Model Studio Skills：官方+自定义，SKILL.md 规范，上传创建/更新/添加 agent（详情页/应用配置）/测试效果；POST /skills 创建（status checking/latest_version）；Qoder CN create-agent 技能：交互引导创建自定义智能体（名称描述+工具权限） |
| 10 | WaytoAGI（智能体教程面） | ✓ | 工作流驱动 Agent 搭建：任务分解为子任务（逻辑顺序依赖）→设计执行方法→Coze 工作流框架设节点逻辑→配置子任务节点验证；输出字段定位：字段名+「查看示例」+试运行定位；学习路径：基础（大模型底层+提示词工程+API）→Agent 核心范式（React→CoT 思考-行动-观察-循环）；多智能体=状态机（随时回滚/编辑共享状态/保存状态三天后继续/故障快速定位）——企业级核心工程实践；评估：工具调用准确率；动手项目 Multi-Agent（选题→写作→审查） |

## 判重基准
双键检索（相对 r224-r253A 已落章节）：Dify（r253-A 多路召回/r252-C 会话变量——secrets/凭据作用域面独有）；n8n（r252-C Retriever/r253-A agent-as-tool——code node 契约面独有）；LangFlow（r253-A 生产部署/r252-B 调试——embed/Assistant 面独有）；Activepieces（r253-A custom piece——run 可观测/限制面独有）；Claude Code（r252-A subagents/r252-B 记忆/r251 多面——output styles 面独有）；腾讯 SkillHub（r251-C 新页——SkillPay/TRACE/三线审核增量≥40% 可合并，本轮备选）；阿里虾小宝（未落——万能 skill 自进化/Model Studio SKILL.md 规范，备选）；WaytoAGI（r252-A 知识库——状态机视角与已落多 Agent 编排重叠>60% 增量弱，不单落）；Pipedream（r253-A error/r252-B OAuth——proxy 面增量合并备选）；Make（r253-A blueprint——调度面通用重叠不落）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 环境变量与凭据作用域 | Secret 类型+workspace/workflow 级+SECRET_KEY 纪律 | 工作流 | wb-execute-discipline |
| ② n8n Code node 契约 | {json:...} 输出契约+两模式+JS 优先 | 工具 | wb-execute-discipline |
| ③ LangFlow Chat Widget | host_url/flow_id 嵌入+workflow=API/MCP 双形态 | 工作流 | wb-execute-discipline |
| ④ Activepieces 可观测 | run log checkpoint+30 天保留+ap_list_runs | 工具 | wb-execute-discipline |
| ⑤ Claude Code Output Styles | Concise/Caveman+关键内容不压缩 | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 备选未落：SkillHub SkillPay/虾小宝 万能 skill（生态增量，留痕存档后续批次再判）；WaytoAGI 状态机（重叠不落）。
- 垃圾：本轮未产生临时文件。
