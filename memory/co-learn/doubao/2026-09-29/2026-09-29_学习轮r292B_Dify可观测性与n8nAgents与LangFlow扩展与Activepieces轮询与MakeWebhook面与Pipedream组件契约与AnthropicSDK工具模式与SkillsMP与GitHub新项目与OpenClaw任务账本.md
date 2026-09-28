# r292B 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r292A 全表。查询词与既往全表错开（本轮=应用发布/可观测性、Agents 形态、扩展系统、轮询、webhook/HTTP 面、组件契约、SDK 工具模式、SkillsMP、GitHub 新项目、OpenClaw 任务账本）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | 可观测性：Variable Inspector 中间值检查 / traces 流到 7 个外部栈（Langfuse/LangSmith/Opik/W&B/Arize/Phoenix/ARMS over OpenTelemetry）/ Agent 沙箱 Squid 代理隔离+bearer token 认证（1.16.1） | 合并保留增量（r289A HTTP 语义/r292A 聚合器，本点=可观测性+沙箱隔离） | 工作流 |
| 2 | n8n | n8n Agents 新形态：agent 定义一次随处用（直接聊/作为 workflow 节点/接 Slack/定时跑）/ Skills 按需加载跨 agent 共享 / Sub-agents 互调 / Knowledge 上传文件 grounding | 合并保留增量（r292A Webhook 面，本点=Agents 独立实体） | 工具 |
| 3 | LangFlow | extension 系统：lfx extension init（extension.json v0 manifest+pyproject pip 可装）/ bundles 组件组贡献回项目 / langflow-builder-mcp 用 MCP 构建组件 | 合并保留增量（r291B 组件安全开关/r292A 记忆库，本点=扩展打包） | 可复用 Skill |
| 4 | Activepieces | Polling Trigger：On Enable 存游标（last timestamp/id）到 context store / Run 每 5 分钟增量取新项 / test 函数返回最近项 / 游标去重防重复 | 合并保留增量（r292A Webhook 三阶段，本点=轮询游标） | 工具 |
| 5 | Make | Webhook 面：JSON pass-through 选项访问原始 JSON / payload 上限 5MB / HTTP v4（原生分页+keychain 存储+简化配置）/ 每场景独立 webhook URL 不复用 | 合并保留增量（r292A 错误语义，本点=webhook/HTTP 模块面） | 工具 |
| 6 | Pipedream | 组件契约：$.interface.timer（intervalSeconds/cron+timezone）/ $.interface.http+customResponse / Destination 异步投递（workflow 完成后才发） | 合并保留增量（r292A 事件源，本点=组件开发接口） | 可复用 Skill |
| 7 | Anthropic | SDK 工具模式：Schema 质量=工具可靠性最大预测因子（名/描述/参数文档）/ 程序化调用三要求（详细输出描述/结构化数据/简洁响应）/ Agent SDK 免手写 stop_reason 循环 / 幂等键防重发 / ToolError 而非 raise | 新面 | 可复用 Skill |
| 8 | SkillsMP | 280k+ SKILL.md 聚合（GitHub 源）/ 语义搜索+AI 语义+职业分类（SOC 美国职业分类系统）/ 公开 API / 独立社区项目 | 合并保留增量（r290A SkillHub/r292A skills.sh，本点=SOC 分类+语义检索） | 可复用 Skill |
| 9 | GitHub 生态 | mempalace（59.3k stars 最佳基准开源 AI 记忆系统）/ ruflo（Claude 多 agent swarms 编排）/ ToolJet AI（企业应用生成，经 MCP 从 Claude Code/Codex/Cursor 构建）/ Dirac（Terminal-Bench-2 榜首编码 agent） | 合并保留增量（r292A 生态面，本点=记忆/编排/终端基准） | 工具 |
| 10 | OpenClaw | 任务账本：任务=记录不是调度器（定时任务+Heartbeat 决定何时运行，任务跟踪发生了什么）/ 状态机 queued→running→terminal 五终态 / childSessionKey+requesterSessionKey 双引用 / 子智能体独立会话 agent:<id>:subagent:<uuid>+完成通知回渠道 / NO_REPLY 抑制后台轮次流式泄露 | 合并保留增量（r291B hooks/r291C 编排，本点=任务账本+NO_REPLY） | 工作流 |

判重口径：增量判定。本轮 1 新面 + 9 合并保留增量，零纯重复。