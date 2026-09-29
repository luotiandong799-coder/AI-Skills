# r298A 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r297 全量（r297A/B/C 三十独点）+ 并行侧。查询词与 r296/r297 全错开（本轮=变量作用域调试/LLM路由/A2A协议/worker规模/自定义app/密钥管理/技能文件结构/API审计聚合/AgentPlugins/工具调用纪律主题）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | 三层变量作用域（workflow 级 {{node.var}} 单次执行重置 vs conversation 级跨会话）；Node Execution Traces（输入/输出/状态/耗时/token）；调试四面板含追踪面板全链路时序；缓存变量编辑（改值即测不重跑全流程） | 独立落地（r297C #1 分块参数=RAG 调参，本点=变量作用域与调试） | 工作流 |
| 2 | n8n | LLM 路由三层：策略路由（会话级、token 处理前按 SLA/订阅选模型）+失败转移（主模型不可用重路由）+成本执行（查询级强制成本，不在账单里发现超支）；模型层+工具层双 fallback 链 | 独立落地（r297C #2 预算熔断器=预算前置检查，本点=路由策略与故障转移） | 工作流 |
| 3 | Langflow | A2A 三原语（Agent Card 名片/Task/Message；JSON-RPC 2.0 over HTTPS+SSE 长任务）；MCP 给 AI 手、A2A 给 AI 同事；LANGFLOW_A2A_ENABLED=false 默认关+ALLOW_PRIVATE_WEBHOOKS=false 防私网回调；AG-UI streaming | 合并保留增量（r297B #3 提到 1.11 A2A 一句话，本点=三原语+开关细节） | 工作流 |
| 4 | Activepieces | Worker 规模公式：workers=peak concurrent flows（concurrency-1 流程全程占用最长 10 分钟，按并发流程非触发率）+apps=ceil(workers/10)；everything queue-backed（超限不丢、排队+指数退避）；基准纪律：并发对齐各自槽位不固定数字，否则读到 backlog | 合并保留增量（r296B #4 1:10 比例，本点=worker 占用逻辑+队列不丢+基准纪律） | 工具 |
| 5 | Make | 自定义 app 三组件最小集：Base（公共设置继承）+Connections（认证配置与测试）+Modules（单模块）；Base 四要素（Base URL/Authorization/Error handling/Sanitization）；Scenario blueprint 场景级复用（模块+设置+映射值打包） | 独立落地（r296C #6 AI Toolkit 工具化，本点=自定义 app 开发结构） | 可复用 Skill |
| 6 | Pipedream | secret prop（加密存储+浏览器隐藏+执行时解密，仅 string prop）；组件无 workspace/project 变量直接访问权（必须显式 prop 引用 {{process.env.X}}）；project 变量覆盖 workspace 变量（最小可见范围）；运行时外部凭据（Vault/AWS Secrets Manager/Nango） | 独立落地（r297B #4 是 Activepieces 凭据，本点=Pipedream 具体机制） | 工作流 |
| 7 | Anthropic | 技能目录结构：SKILL.md（必填）+REFERENCE.md（可选按需加载）+scripts/（确定性脚本）；按需文件访问零 token（脚本代码不进上下文只进输出）；链式组合靠输出格式对接；别包含未用技能（影响性能） | 独立落地（r297A #7 frontmatter 保留词=元数据，本点=目录结构与加载机制） | 可复用 Skill |
| 8 | skills.sh | 安全审计多源聚合（Gen Agent Trust Hub/Socket/Snyk/Runlayer/ZeroLeaks 五伙伴一个接口）；API 认证=Vercel OIDC 短命 token 自动轮换无长期密钥；类别规模 AI Tool 232k+；四大市场（Skills.sh/Claude Skills Registry/HF Skills Hub/Copilot Studio） | 合并保留增量（r297A #8 遥测排行榜，本点=多源审计+OIDC 认证） | 工具 |
| 9 | GitHub | Agent Plugins 1.0（2026-08-12 GA）：spec 插件跨工具共享（VS Code/CLI/app 发现同一包的 skills+MCP 配置）；Awesome Copilot 默认市场（175+ agents/208+ skills/48+ plugins）；GitHub agent apps 进 issues 与 workflows；护栏模式 allowlists+least privilege+PR review | 独立落地（r297C #9 Copilot 运行时能力，本点=插件市场与跨工具分发） | 工具 |
| 10 | deeplearning | 工具调用纪律：同一响应全部工具调用执行完再发起下一轮 LLM 调用（并行必须全解析）；条件工具执行（基于 tool_call 决定是否真调用，不盲信）；schema description 精度（做什么/何时用/返回什么）；工具函数 try/except+描述性错误 | 合并保留增量（§工具循环终止条件=stop_reason 检查，本点=并行全解析+条件执行） | 工作流 |

判重口径：增量判定。10 独点=5 独立+5 合并保留增量，零纯重复。