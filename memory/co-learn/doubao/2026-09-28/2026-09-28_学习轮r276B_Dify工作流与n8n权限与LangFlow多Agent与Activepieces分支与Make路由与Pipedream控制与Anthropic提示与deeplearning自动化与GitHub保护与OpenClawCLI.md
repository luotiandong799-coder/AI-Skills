# r276B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（工作流控制面） | ✓ | **Variable Aggregator 变量聚合器**（收敛互斥分支为单一输出——If/Else、Question Classifier 创建互斥分支每 run 只一路径——避免下游重复——全部聚合变量须同数据类型——运行时只有实际执行分支贡献值——String/Number/Object/Boolean/Array——v0.6.10+ advanced feature；array 模式收集全部分支输出到列表）；**If-Else 节点**（条件求值路由——IF/ELIF 多个/ELSE——AND/OR 复杂条件——text patterns contains/starts with——value comparisons/empty states）；**Question Classifier**（基于意图分类路由查询）；**Parallel Branch**（v0.8.0 并行加速——双 IF/ELSE 嵌套——End 前合并）；**错误处理建议**（LLM/HTTP/Code/Tool 节点失败用内置 retry/default-value/fail-branch 不是 If/Else 的活） |
| 2 | n8n（多用户权限面） | ✓ | **实例角色**（每用户一个 instance role——三内置 Owner/Admin/Member——可建 custom instance roles 粒度权限）；**项目角色**（三用户角色 Admin/Editor/Viewer——Project Admin 最高：管理项目设置/成员/项目内 workflows/credentials/executions/创建 end-user credentials 仅 admin）；**自定义项目角色**（仅限所在项目——不同项目不同角色）；**工作流共享**（两工作流角色 creator/editor——不能改 owner 除非删用户——共享允许 editors 用工作流里所有 credentials 含未显式共享的）；**SSO/用户供应**（IDP-driven role sync——从 IdP 同步用户与角色到 instance+project 级——按用户或 IdP 组自动分配） |
| 3 | LangFlow（多 Agent 编排面） | ✓ | **五 agent 深研流**（Research Planner 拆复杂问题 3-7 子问题→Source Finder 带 web search 检索→Summarization 工具调用提取→Reviewer 识别缺口→Professional Research Writer 综合成报告——每 agent 清晰职责）；**Judge/Router 模式**（judge agent 评估查询路由到专业下游——User Query→Judge Agent→Router→Specialized Agent）；**Agent 嵌套**（tool mode——agent 把其他 agent 当工具调用——递归编排多层——Langflow 1.1 agent 组件）；**CrewAI 分层 crew**（Hierarchical crew Manager 角色 agent 连 LLM 推理选工具）；**Sequential tasks agent**（多 Agent 组件单 flow——每 agent 连独特工具——Prompt 连 Agent Instructions 控制行为——逐 agent 建立前 agent 工作）；**supervisor**（只看到高层工具做域级路由）；**CUGA**（orchestrator 分配子任务——planner 读文件更新计划——Plan Controller 管理序列状态） |
| 4 | Activepieces（分支循环面） | ✓ | **数据传递表达式**（Array Operations map/filter/reduce——{{ trigger.items[0] }} 首项/{{ trigger.items.length }}——Object Operations）；**Loop on items**（loop context {item, index, total}——executeSteps 每迭代——results push）；**循环嵌套分支**（loop 里 router——EXECUTE_FIRST_MATCH——分支里再嵌套 loop）；**公式函数**（if(condition; "High value"; "Standard") 三参——length(trim(user_input)) 组合）；**MCP 分支工具**（ap_flow_structure 看分支条件索引——ap_add_branch 加条件分支插到 Otherwise 前）；**数据转换**（JavaScript steps 字段清洗/类型转换/归一化/记录重塑——internal tables 存储状态/去重/查找——并行路径不阻塞主流程） |
| 5 | Make（过滤器路由器面） | ✓ | **Router**（分支场景流为多模块链——每路由按条件处理——Filter 用操作符 less than/greater than——按序排列路由+fallback 路由处理不匹配数据——fallback 也可设 filter）；**Filter**（两模块间附加条件门控——下一模块只在条件为真时运行——Router 里每分支放 filter 决定执行——wrench 图标/连接线→Set up a filter→有意义 label）；**Array Aggregator**（收集多 bundles 合并单数组——发结构化列表给 API/批量插行/传对象集合——例 20 订单行项 enrich 后聚合批量插库一次 API）；**高级路由模式**（数据类型路由 B2B→CRM B2C→不同邮件 campaign；动态优先级评分路由；多通道编排单 trigger 喂 Slack/CRM/ticketing；fallback 链 主→次→三级降级）；**转换模块**（Text Parser regex/JSON 模块/Data stores 临时存储渐进 enrich） |
| 6 | Pipedream（流程控制面） | ✓ | **运算符**（If/Else beta 单路径逻辑分支多输入变量；Delay 1ms-1年；Filter 停止或继续规则；End Workflow 提前终止；Switch 单路径分支基于单输入变量值——规则定义顺序影响路径；Parallel 多路径分支可过滤执行所有匹配分支——顺序不影响路径）；**Parallel 详解**（创建分支/重命名/导出数据到父 flow——Beta 限制——不相关 LLM 查询并行后父 flow 引用响应——分支 last-step exports 合并回父流）；**循环**（loops 就是代码——Node.js for loop 调 action——区别于 Power Automate/Make 显式 Apply to each/Iterator）；**retry/delay per-step 可配置**；**pd.flow.exit**（条件内提前退出工作流 exit("reason")）；**n8n vs Pipedream 实战**（Gmail→Gemini→Slack conditional→Jira→Sheets） |
| 7 | Anthropic（系统提示面） | ✓ | **XML 标签结构化**（XML tags 帮 Claude 无歧义解析复杂 prompt——混合 instructions/context/examples/variable inputs 时每类内容自己的标签 <instructions>/<context>/<input>——减少误解——官方推荐——训练数据含 XML 风格分隔符——比 Markdown headings 更可靠）；**常见标签模式**（<role> 锚定 Claude 视角先读激活相关知识过滤语气——"Senior backend engineer" vs "helpful assistant" 不同响应；<context> 行动前需要的一切——约束/背景/已有决策——不内联任务；数据分隔 <document>/<article>）；**Sonnet 特殊性**（低延迟+锐利指令跟随——显式 XML 标签定义 context/input/rules 得确定性结果——<code_to_review>/<formatting_rules>） |
| 8 | deeplearning（工作流自动化面） | ✓ | **Agentic AI 课程**（四设计模式：Reflection AI 批评自己迭代改进；Tool Use 连数据库/API/外部服务真行动；Planning 拆复杂任务可执行步骤适应意外；Multi-Agent 协调多个专业 AI 系统——评估优化 performance metrics/error analysis/production deployment）；**AI Agents in LangGraph**（Harrison Chase+Tavily Rotem Weiss——agentic search）；**Building Code Agents smolagents**（54m——agents 写执行代码完成任务）；**Practical Multi AI Agents with crewAI**（2h49m——协作解决复杂业务任务）；**Functions Tools and Agents with LangChain**（LCEL 组合 chains/agents）；**Windsurf AI Coding Agents**（1h30m Agentic IDE） |
| 9 | GitHub（分支保护面） | ✓ | **受保护分支**（branch protection rule——推变更前强制工作流/要求含合并 PR——默认禁用 force pushes+防止删除——可选禁用/启用——bypass lists 仅组织仓库可加）；**合并队列**（管理员要求 "Require merge queue"——自动合并忙碌分支 PR——保证分支不被不兼容变更打断——Merge method merge/rebase/squash、Build concurrency、进入队列前要求更新/等待 checks）；**rulesets 规则清单**（Require PR reviews/Require status checks/Require conversation resolution/Require signed commits/Require linear history/Require merge queue/Require deployments succeed/Lock branch/Do not allow bypassing/restrict pushes——线性历史要求 squash/rebase 允许）；**rulesets vs 保护规则**（org 级 rulesets 无 merge queue 规则——repository 级才有） |
| 10 | OpenClaw（CLI 配置面） | ✓ | **CLI 结构**（configure/config/gateway call/health/acp/status/monitor）；**Gateway 配置**（--bind loopback/lan/tailnet/auto/custom 监听绑定；--auth none/token/password/trusted-proxy 认证模式；--token/--password override 也设 CLAWDBOT_GATEWAY_TOKEN/CLAWDBOT_GATEWAY_PASSWORD；--gateway-auth password/--gateway-password 显式；Tailscale Funnel 仍需 password；--gateway-token-ref-env 非交互 SecretRef）；**token auth 建议**（即使 loopback 也建议开着——本地 WS 客户端需认证；token 模式明文 token 生成/保存（默认）或 SecretRef opt-in；password 模式交互式也支持）；**acp**（ACP bridge 连 IDEs 到 Gateway）；**monitor**（本地监控 dashboard 默认 18790）；**gateway start/stop/restart**（进程控制） |

## 判重（双键检索结果）
- Dify 工作流控制：库内 §Dify 类锚点——Variable Aggregator/If-Else 条件/Parallel 分支/Question Classifier 为独有增量 ≥40% → 落地
- n8n 多用户权限：库内 §n8n 类锚点——实例角色/项目角色/自定义角色/工作流共享/SSO 为独有增量 ≥40% → 落地
- LangFlow 多 Agent：库内 §LangFlow 类锚点——五 agent 深研流/Judge Router/agent 嵌套/CrewAI 分层为独有增量 ≥40% → 落地
- Activepieces 分支循环：库内 §Activepieces 类锚点——loop context/公式函数/MCP 分支工具/数据传递表达式为独有增量 ≥40% → 落地
- Make 过滤器路由器：库内 §Make 类锚点——Router+fallback/Filter 门控/Array Aggregator/高级路由模式为独有增量 ≥40% → 落地
- Pipedream 流程控制：库内 §Pipedream 类锚点——Parallel/Switch/If-Else/Delay/Filter/End/loops=code 为独有增量 ≥40% → 落地
- Anthropic 系统提示：库内 §Anthropic 类锚点——XML 标签结构化/常见模式/role 锚定为独有增量 ≥40% → 落地
- deeplearning 工作流自动化：库内 §deeplearning 类锚点——Agentic AI 四模式/smolagents/crewAI 课程为独有增量 ≥40% → 落地
- GitHub 分支保护：库内 §GitHub 类锚点——branch protection/merge queue/rulesets 规则清单为独有增量 ≥40% → 落地
- OpenClaw CLI：库内 §OpenClaw 类锚点——CLI 结构/gateway 认证模式/token auth 建议/monitor 为独有增量 ≥40% → 落地

## 独点落地（10 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r276B-1 | wb-execute-discipline | 3.45.0+ | Dify 工作流高级控制 | 工作流 |
| r276B-2 | wb-execute-discipline | 3.45.0+ | n8n 多用户与权限管理 | 工作流 |
| r276B-3 | wb-execute-discipline | 3.45.0+ | LangFlow 多 Agent 编排 | 可复用 Skill |
| r276B-4 | wb-execute-discipline | 3.45.0+ | Activepieces 分支循环与数据转换 | 工作流 |
| r276B-5 | wb-execute-discipline | 3.45.0+ | Make 过滤器路由器与聚合器 | 工具 |
| r276B-6 | wb-execute-discipline | 3.45.0+ | Pipedream 子工作流与流程控制 | 工具 |
| r276B-7 | wb-execute-discipline | 3.45.0+ | Anthropic 系统提示与角色工程 | 可复用 Skill |
| r276B-8 | wb-execute-discipline | 3.45.0+ | deeplearning 工作流自动化课程 | 可复用 Skill |
| r276B-9 | wb-execute-discipline | 3.45.0+ | GitHub 分支保护与仓库治理 | 工具 |
| r276B-10 | wb-execute-discipline | 3.45.0+ | OpenClaw CLI 命令与配置参考 | 工具 |

## 复核
十独点均有当日实拉来源；均增量合并或新面；无并入未落地项。垃圾：本轮未产生临时文件。
