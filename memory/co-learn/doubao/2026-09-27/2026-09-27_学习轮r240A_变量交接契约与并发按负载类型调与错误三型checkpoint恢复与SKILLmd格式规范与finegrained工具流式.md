# r240-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（工作流变量/批处理面） | ✓ | 变量交接契约（跨节点变量需两个显式动作：源节点声明为输出+接收节点完整路径引用；漏一边"工作流执行不报错数据消失"silent data loss）；sys.workflow_run_id 系统变量追踪历史执行；批处理模式（Run Batch tab→CSV 模板→每行一次执行→并行+实时进度）；分支汇聚（exclusive branches 汇聚统一变量；array 模式收集全部分支输出成列表+Code 节点处理）；Output 节点（分支无 Output 返回无值；多 Output 支持唯一命名）；迭代节点（items/index 内建变量；Parallel Mode 显著提效 DeepSeek R1 推理慢→并行）；Session Variable（chatflow 专属 Variable Assigner 可变跨轮持久）；LLM 节点 {{variable_name}} 双花括号+Context Variables 注入知识保留来源归因 |
| 2 | n8n（队列/并发调优面） | ✓ | 并发与 DB 连接池陷阱（低并发值+大量 worker 耗尽连接池致处理延迟失败）；concurrency 默认 10 官方建议 5+；按负载类型调（I/O 密集 HTTP/DB/webhook 10-20 per worker；CPU 密集大变换/图像/重 Code 节点 2-5+加 worker 扩容）；起始规则一 worker 每可用 vCPU 2-CPU 从 5 开始；N8N_CONCURRENCY_PRODUCTION_LIMIT 生产并发限制默认 5；worker 无端口只连 Redis+Postgres；Little 定律算 worker 数（峰值 RPS×平均执行秒/concurrency）；Redis 6.2+ AOF appendonly yes+PostgreSQL 替代 SQLite；太高饿死工作流 CPU 太低浪费空闲 |
| 3 | LangFlow（自定义组件/工具面） | ✓ | Tool Mode 组件转工具（启用后组件输入被修改 agent 可调用；Web Search/URL/Calculator 开 Tool Mode 连 Agent Tools port）；自定义组件（Python 类继承 Component；class-level 属性描述；输入输出列表决定数据流）；LANGFLOW_ALLOW_CUSTOM_COMPONENTS 环境变量禁用自定义 Python 组件执行（安全）+LANGFLOW_COMPONENTS_PATH 白名单；CUGA bundle 1.10（lite_mode_tool_threshold 默认 25 工具数低于阈值自动启用 CugaLite；decomposition_strategy flexible 多子任务/exact 每 app 一子任务；browser_enabled）；Agentics bundle 多 provider LLM；MCP server 部署 flow 转工具 |
| 4 | Activepieces（执行/错误处理面） | ✓ | 三种重试策略（step-level 自动退避可配最大尝试/flow-level error handler catch block 任何步骤失败触发/manual retry UI 从失败步骤重跑）；错误类型三分（STEP_ERROR stepName+statusCode/Timeout 执行超时/Sandbox）；可靠性模式（指数退避+熔断器+DLQ 死信队列；rate limit 分支按状态码；节流+幂等键防重复）；checkpoint 恢复（store checkpoints 操作员从最后安全步骤恢复）；错误处理四件套（wrap retries+timeouts+fallback/errors 集中中央表 payload+step+correlation ID/通知正确渠道/human triage 暂停 resume）；webhook 幂等（idempotency keys+correlation IDs 存 Tables 检测重复 short-circuit）；step-level 执行日志 inputs/outputs/errors per run+event audit trails；postmortem 教训（监控 Redis 队列深度增长率/计划任务量尖峰——被客户发现不是自动化告警） |
| 5 | Make（高级模块面） | ✓ | 高级模块三件套（Router 分叉/Aggregator 聚合多 bundle 成单数组或文本摘要/Iterator 列表拆 bundle）；经典批量模式（Iterator 拆 500 联系人→Router 分支并行 HTTP+AI 分析→Aggregator 聚合→bulk 更新）；Router 配置（每 route 多 filter ET/OU；计算变量动态决策；默认两路径+按钮加）；Text Aggregator（source module+text 模板+row separator）；HTTP 模块连无官方集成服务；Error 端口分支专用错误处理场景（Slack/邮件+状态码+响应） |
| 6 | Pipedream（数据存储/开发面） | ✓ | Data Store 三用法（去重 dedup/计数器/工作流状态 KV 内置无需外库）；get 前设默认值 ?? 0；组件开发模式（app file 复用方法；JS Docs 轻量文档 description+@params+@returns 默认值；source 用 $.service.db set/get）；最佳实践（code steps 管逻辑/app steps 管标准操作/data stores 管状态/HTTP triggers 管 webhook/try-catch+自动重试/managed auth）；GitHub 双向同步（workflows 序列化进 repo dev branches commits diffs PRs production merges）；四语言 Node/Python/Go/Bash；保留策略 workflow exports/logs/execution data |
| 7 | Anthropic（流式/tool use 面） | ✓ | fine-grained tool streaming（eager_input_streaming=true 任意工具细粒度流式；全模型全平台 Claude API/Bedrock/Vertex/Foundry 无 beta header）；Streaming 输入模式推荐（持久交互会话长生命周期处理输入/中断/权限请求/会话管理 vs single mode）；Tool runner SDK（stream=True+get_final_message 累积）；SSE 桥接（异步生成器桥 Server-Sent Events FastAPI+Agent SDK）；API primer stream.text_stream 逐 token |
| 8 | skills.sh（SKILL.md 格式规范面） | ✓ | frontmatter 平台差异（agentskills.io 允许 name/description/license/metadata/compatibility/allowed-tools；Claude settings importer 拒绝未识别字段）；name 规则（kebab-case 无空格大写匹配文件夹名最大 64 字符）；description 规则（必须含做什么+何时用触发条件；<1024 字符；无 XML 标签；含具体任务短语；提及文件类型——description 是文件最重要一行模型决定加载的唯一所见 progressive disclosure 只有 name+description 在上下文直到调用）；allowed-tools 限制技能激活时工具（只读技能不许编辑）；body 规范（## 二级标题；具体示例；license 标识） |
| 9 | 腾讯 SkillHub（生态数据面） | ✓ | 生态规模（月下载 1700万+ 累计突破 6000万+ 2026-07；平台 8万+/76万+ Skills 不同口径最新 76万+；全球 AI Agent 工具 44万+ AI Skill 近 30万 日均新增 1300+）；TRACE 评测体系识别高质量 Skill；三线并行安全审核+国内镜像秒装+中文搜索+Top 50 榜单；QClaw/WorkBuddy/ima 兼容；复制提示词粘贴 agent 数秒装好摒弃下载安装更新存储占用；Plugin 广场开源 Plugin；企业 PAY 本月调用 12.8万次收益 3.19万元 |
| 10 | GitHub（生态面） | ✓ | browser-use 116,025★ OSS agent framework；TradingAgents 108,236★ 多 agent 交易框架；agent-browser 43,207★ Rust 浏览器自动化 CLI；agno 42,345★ agent platform；jev-chat-jarvis 今日热门 #1 +849★ 手机对话副驾（QQ/X/飞书读懂对方给候选回复一键填入只读屏幕不 hook 不改包非侵入）；CowAgent 47,122★ 开源超级 assistant & Agent Harness（计划任务跑工具技能自进化记忆多 agent 多模型多渠道单行安装）；langchain 147,117★ PyPI 1.62 亿下载；vLLM 0.30 GPU weight cache 引擎重启跳过磁盘（Fast Start 量化权重常驻 GPU 内存） |

## 判重基准
双键检索：Dify（r239-B/C 已落 Agent Node/RAG 检索，变量交接契约+迭代并行+Session Variable 独有增量）；n8n（r238-C 队列模式/r239-B/C 已落，按负载类型调并发+Little 定律+连接池陷阱独有增量细节）；LangFlow（r239 各轮已落，Tool Mode 组件转工具+白名单安全开关独有）；Activepieces（r238/r239 已落，错误类型三分+checkpoint 恢复+DLQ 独有）；Make（r239-A/C 已落，批量三件套模式独有）；Pipedream（r239 已落，Data Store+GitHub sync 独有）；Anthropic（r238/r239 已落，fine-grained tool streaming+eager_input_streaming 独有）；skills.sh（r239-B/C 已落创建五步/ClawHub，SKILL.md description 唯一所见+allowed-tools+平台差异独有）；腾讯 SkillHub（r239-A 已落 SkillPay 链路，生态规模数据+TRACE 评测+三线审核独有）；GitHub（r238-C/r239 已落，jev-chat-jarvis 只读+CowAgent+vLLM weight cache 独有）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 变量交接契约+迭代并行+Session Variable | 源声明输出+接收完整路径引用，漏一边数据静默消失；items/index+Parallel Mode；Session Variable 可变跨轮 | 工作流 | wb-execute-discipline |
| ② n8n 按负载类型定并发+Little 定律 | I/O 密集 10-20/CPU 密集 2-5；一 worker 每 vCPU；峰值 RPS×执行秒算 worker；低并发多 worker 耗尽 DB 连接池 | 工作流 | wb-execute-discipline |
| ③ Activepieces 错误类型三分+checkpoint 恢复 | STEP/TIMEOUT/SANDBOX 三型；step 退避/flow catch/manual rerun 三策略；DLQ+幂等键；checkpoint 从最后安全步骤恢复 | 工作流 | wb-execute-discipline |
| ④ SKILL.md description 唯一所见+allowed-tools | description 含做什么+何时用+任务短语是唯一所见；allowed-tools 限制技能权限；frontmatter 跨平台差异 | 可复用 Skill | wb-execute-discipline |
| ⑤ Anthropic fine-grained tool streaming | eager_input_streaming 细粒度流式全平台；Streaming 输入模式推荐长生命周期；SSE 桥接 | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：wb-ponytail/wb-max-token-saver/wb-context-compressor 无新可优化项（description 唯一所见与 compressor 渐进披露同源，已覆盖）。
- 垃圾：本轮未产生临时文件。
