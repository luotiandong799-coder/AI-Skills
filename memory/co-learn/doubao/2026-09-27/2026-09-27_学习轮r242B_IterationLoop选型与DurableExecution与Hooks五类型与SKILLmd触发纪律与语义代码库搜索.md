# r242-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（迭代/循环面） | ✓ | Iteration node（数组输入 Parameter Extractor/Code/Knowledge Retrieval/HTTP；内置变量 items[object] 当前元素 + index[number] 从 0 开始；Sequential/Parallel 模式并行最大 10）；Loop node（2026 循环变量+结束条件+最大循环次数与 iteration 不同）；Parameter Extractor（LLM 从非结构化文本提取结构化参数——自然语言输入到工具/API 所需参数桥）；Workflow as Tool（发布 workflow 为 tool 供复用） |
| 2 | n8n（数据变换面） | ✓ | 确定性步骤 vs AI 步骤（模板化输出用 Set 节点固定格式只变数据结果一致——AI 生成只用于输出真需按上下文变化；"Models are probabilistic. Math is not."）；Set 节点五连（With Expressions {{}} $json/$now/Complex Data 对象数组嵌套/Clean Output Keep Only Set/条件 Sets）；Auto-discovery 数据管线（PostgreSQL 元数据发现→表分析筛选→动态行拉取→行转文档→embedding 批→upsert） |
| 3 | LangFlow（API/流式面） | ✓ | v2 workflow API（POST /api/v2/workflows 简单响应+异步后台任务）；AG-UI streaming（stream_protocol "agui" 每 data: 行一个 AG-UI 事件 TEXT_MESSAGE_CONTENT/TOOL_CALL_RESULT/RUN_FINISHED；SSE text/event-stream）；sequence_id 续流（可选从特定点恢复流式）；?stream=true LLM token 流式响应 |
| 4 | Activepieces（触发/队列面） | ✓ | Durable execution（中断运行从最后 checkpoint 恢复而非从头——worker 死亡时新 worker 重用每个已完成步骤保存输出只跑第一个未完成步骤防重复发邮件/重复扣款/重复 API 调用；覆盖 crash/deploy/长暂停/重试）；Queue 分优先级（EXECUTE_PROPERTY 运行时加载动态属性/EXECUTE_EXTRACT_PIECE_INFORMATION 安装时获取 piece 信息/EXECUTE_VALIDATION 运行前校验 flow/EXECUTE_TRIGGER_HOOK 触发前后特殊逻辑）；Schedule triggers（Every X minutes/hour/day/week/month/Cron） |
| 5 | Make（MCP 面） | ✓ | MCP Server scenario 变工具（active+on-demand scenarios 供外部 AI 调用；AI 识别匹配任务自动触发）；Execute an action with AI 链式（客户支持分诊两模块链：快模型分类工单优先级→强模型高价值案例详细摘要）；超时语义（scenario run tool 调用超时后 scenario 在 Make 继续跑最多 40 分钟返回 executionId 供 AI 取输出） |
| 6 | Pipedream（触发/集成面） | ✓ | Trigger 类型（HTTP/Webhook/Schedule/Email/RSS/App-based Twitter GitHub Google Calendar）；instant webhook 注册；Trigger 部署语义（source 配置后必须部署才开始监听事件；定义 webhook URL 或 workflow ID 消费事件——source 语义与 actions 不同）；10,000+ prebuilt triggers/actions 公共注册表 |
| 7 | Anthropic（hooks/rules 面） | ✓ | Hooks 五类型（command/HTTP/mcp_tool 确定性触发 + prompt/agent 用 Claude 判断）；hooks 低上下文成本（结果注入而非全文）；CLAUDE.md 纪律（/init 生成 starter 基于项目结构再精化；会话开始就读；含 Bash 命令/代码风格/工作流规则）；hooks 注册位置（settings.json/托管策略/skill/agent frontmatter） |
| 8 | skills.sh（技能创作面） | ✓ | SKILL.md frontmatter 纪律（name+description 是 Claude 决定触发时读的唯二字段，body 触发后才加载——按需加载不占上下文）；目录规范（分类 lowercase 无空格/skill 目录 lowercase-hyphen/支持文件 lowercase-hyphen.md/persona Title Case）；arXiv 2607.01456 实证研究（"From Anatomy to Smells" 首个 SKILL.md systematic study）；authoring 检查清单（gerund 动词+ing/lowercase hyphens max 64/描述第三人称/含触发条件/body <500 lines） |
| 9 | docs.openclaw.ai（CLI/插件面） | ✓ | skills install 来源矩阵（@owner/slug registry/skills-sh:owner/repo/slug/git:owner/repo@ref/./path --as custom-name 本地/--global 所有本地 agent）；plugins 命令（list/search/install --link --force --pin --marketplace/inspect --runtime --json）；--pin 钉版本；--agent <id> 定向安装到某 agent |
| 10 | GitHub（生态面） | ✓ | Claude Context（Zilliz 语义代码库搜索 MCP ~40% token 节省 coding agents 一次安装整代码库语义搜索免每会话文件加载）；CrabTrap（Brex LLM-as-Judge HTTP 代理保护生产 AI agents）；Maskit（本地隐私脱敏网关自动遮蔽 AI 服务请求敏感数据流式响应无缝恢复支持 Cursor/Claude Code 等可配置 Base URL 工具）；Jev 生态（jev2mcp context-aware MCP/plugin/tool 选择智能层/jev-mcp MCP server 包装 typed noul/choice/score 判断）；mksglu/context-mode 21.4k★ 上下文窗口优化；agent-browser 43.2k★ Rust 浏览器自动化 CLI |

## 判重基准
双键检索（相对 r241-A/B/C 已落章节 + r242-A 本批）：Dify（r241-A 落过并发按负载/r242-A 落过 Agent 实体——"Iteration vs Loop 选型+Parameter Extractor"独有增量）；n8n（r241-B 落过确定性安全栈——"确定性步骤优先+Keep Only Set"独有增量深化）；LangFlow（r240-C 落过 LFX 无头执行——"AG-UI 协议+sequence_id 续流"独有增量）；Activepieces（r241-C 落过 Scan+Resume——"durable execution checkpoint 防重复副作用"独有增量深化）；Make（r241-A 落过执行态交付态——"executionId 超时取输出"独有增量深化）；Pipedream（r241-B 落过触发器——"trigger 部署语义+类型选型"独有增量深化）；Anthropic（r240-C 落过 hooks 优先级权限分级——"五类型确定性/判断二分+低上下文成本"独有增量深化）；skills.sh（r240 落过 SKILL.md 格式规范——"frontmatter 唯一触发读取+实证研究"独有增量）；openclaw（r242-A 落过 skills CLI——"openclaw 多源安装+--agent 定向"不同平台独有增量）；GitHub（r241-C 落过 GNAP/memwyre——"语义代码库搜索 MCP+脱敏网关+judge 代理"独有增量）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify Iteration vs Loop 选型+Parameter Extractor | 数组批处理用 Iteration 并行；条件循环用 Loop 结束条件；非结构化→结构化参数桥 | 工作流 | wb-execute-discipline |
| ② Activepieces durable execution checkpoint | 中断从最后已完成步骤续跑防重复副作用；队列优先级分型 | 工具/工作流 | wb-execute-discipline |
| ③ Anthropic Hooks 五类型确定性/判断二分 | command/HTTP/mcp_tool 确定性 + prompt/agent 判断；结果注入低上下文成本 | 工具/工作流 | wb-execute-discipline |
| ④ SKILL.md frontmatter 唯一触发读取 | name/description 是触发读取唯二字段 body 按需加载；目录命名规范；实证研究 | 可复用 Skill | wb-execute-discipline |
| ⑤ GitHub 语义代码库搜索 MCP+脱敏网关 | Claude Context 一次安装整库语义搜索省 40% token；Maskit 请求遮蔽流式恢复 | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
