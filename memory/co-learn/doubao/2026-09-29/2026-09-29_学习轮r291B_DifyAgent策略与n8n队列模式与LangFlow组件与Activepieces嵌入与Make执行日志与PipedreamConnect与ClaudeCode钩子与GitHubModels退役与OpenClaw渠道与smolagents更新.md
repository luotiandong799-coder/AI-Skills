# r291B 学习轮（2026-09-29，十站实拉→十独点）

判重基线同 r291A（r284~r290 全表 + SKILL.md 1,949,252B）。查询词与既往全表错开。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | Agent 策略可插拔：Agent Strategy=推理算法模块（引擎与控制分离式设计）/ Function Calling vs ReAct 选型判据（有原生 FC 用 FC，开源模型用 ReAct Thought→Action→Observation）/ cot_agent 两策略（自治-控制谱系）/ Iteration Limit 迭代限制 / session.tool.invoke(provider+tool_name+parameters) 调用契约 | 合并保留增量 | 工具 |
| 2 | n8n | queue mode 架构：EXECUTIONS_MODE=queue（main 收触发调度+worker 执行+Redis broker+Postgres 13+，SQLite 不推荐）/ 单实例陷阱（开 queue 无 worker→全部 pending 不执行）/ 全进程共享 N8N_ENCRYPTION_KEY / worker health 端点 / docker --scale n8n-worker=N | 合并保留增量 | 工具 |
| 3 | LangFlow | 自定义组件开发：Component 类四要素（继承/类属性 display_name+icon/inputs+outputs 列表/methods）/ bundle 按服务商组织组件组 / LANGFLOW_ALLOW_CUSTOM_COMPONENTS=false 阻断任意代码执行 / tool_mode=True 把输入暴露为 agent 工具 | 合并保留增量 | 工具 |
| 4 | Activepieces | embedding 嵌入 SDK：activepieces.configure(instanceUrl+jwtToken+containerId) iframe 内嵌 / JWT 认证交换流（后端生成→iframe query 传→换长期 token）/ activepieces.connect({pieceName}) 按需打开连接对话框 / 导航同步 handler / provision users 自动开通 / 白标商用（非 MIT 核心） | 新面 | 工具 |
| 5 | Make | 执行历史留存与观测契约：Execution History 留存梯度（7 天免费/30 天付费/60 天 Enterprise，全数据流+JSON payload）/ structured log（scenario_id/execution_id/correlation_id/step/status 五字段）；附带：Dify 无原生调度→XXL-JOB 外部调度器补（cron/一次性+告警+观测） | 新面 | 工作流 |
| 6 | Pipedream | Connect 集成面：managed auth（OAuth client 统一管）/ external_user_id 关联（≤250 字符，代用户发起连接与调用）/ Connect API+SDK 双端（服务端发连接流+前端或托管 URL）/ 10,000+ 预构建工具 / remote.mcp.pipedream.net 托管 MCP（Bearer+x-pd-project-id/environment/external-user-id 请求头）/ API proxy 无预构建工具时带用户凭证转发 | 新面 | 工具 |
| 7 | Claude Code | hooks/subagents/checkpoints：31 个 hook 事件三节奏（每会话/每轮/每次工具调用，可 shell/HTTP/LLM prompts）/ SubagentStop hook 的 hookSpecificOutput.additionalContext 可扩展子代理回合（非二元错误）/ subagents 独立上下文窗口只回摘要（防上下文膨胀）/ 5 层嵌套 / checkpoints 每回合快照（最近 100 个、默认 30 天清理 cleanupPeriodDays） | 合并保留增量 | 工具 |
| 8 | GitHub Models | 2026-07-30 完全退役（playground/model catalog/inference API/BYOK 全下线）→ 迁移 Microsoft Foundry Models；Foundry 旗舰规格（gpt-5.6-sol：105 万 context/128k 输出/multi-agent orchestration preview/computer use） | 新面 | 工具 |
| 9 | OpenClaw | channels 渠道面：官方插件一键装（openclaw plugins install）/ Telegram 内置核心（grammY Bot API 群组）/ Discord（Bot API+Gateway 服务器/频道/私信）/ dmPolicy: "pairing" 配对模式（仅 UI 配对用户可对话，防陌生人耗 API 额度）/ 50+ 渠道适配器与自定义渠道指南 / openclaw vault 存 token | 合并保留增量 | 工具 |
| 10 | smolagents | 1.26.0：CodeAgent（代码型行动：Python 片段+嵌套/循环/条件组合）vs ToolCallingAgent（JSON 调用）关键区别 / sandbox='e2b'/'local' 生产显式指定（e2b 需 E2B_API_KEY+~25s 延迟）/ 原生无并行子代理（concurrent.futures threading 补）/ 生产前四查（执行环境/工具权限/密钥边界/smoke check）/ Hub 共享加载工具 | 合并保留增量 | 可复用 Skill |

判重口径：增量判定。本轮 4 新面 + 6 合并保留增量，零纯重复。