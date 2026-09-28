# r286A 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r284/r285 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（工作流编排） | OK | **Hybrid Agent/Tool 模式：确定性工具先行（Tool Node 取数）+ Agent Node 只处理复杂/可变部分（分析决策）——省 agent 开销、保确定性**；**Agent Node 最佳实践：清晰工具描述/适当迭代上限（防 runaway cost）/详细指令/内存管理平衡上下文保留与 token 效率**；**一个 workflow 一个 job，拆子工作流用 HTTP 节点调用，不做单体**；**条件节点当 guard：进 LLM 前校验输入，无效输入不浪费 token**；**Iteration 优先于 Loop：Iteration 可并行化子流，数量级更快**；**Code 节点清洗数据：LLM 输出不稳定，过 Python/JS 校验转换**；**节点错误处理：LLM/HTTP/Code/Tool 节点支持 retries 和失败行为（停止/返回类型化默认值/走 fail 分支）**；**嵌套 Agent 节点：一个 agent 可调用另一个作工具（v1.3+）** |
| 2 | n8n（错误恢复） | OK | **工具失败最可靠修法：不用直接工具节点，用 "Call n8n Workflow" 工具——工具逻辑放子工作流，子工作流节点开 Continue on Fail，保证子工作流总返回干净响应回 agent，主工作流不崩**（known bug：Agent 的 Continue on error 不捕获工具子节点的错误）；**Code 节点 try/catch 返回结构化错误对象 {success:false, error} 而非抛异常**；**模型故障转移链：Agent Variables 节点递增 fail_count，主模型失败自动 fallback 到 GPT/Gemini**；**Execution Data 节点给执行附加可搜索元数据（user ID/entry point/outcome/session ID），失败可按字段过滤**；**错误触发子工作流：失败时捕获错误+取完整 workflow 结构发 AI agent 根因分析**；**HITL 安全路径：高端模型多次失败生成无效工具调用后，自动路由到 human-in-the-loop 或确定性安全路径** |
| 3 | LangFlow（扩展/缓存/评估） | OK | **scaling：资源管理与生产稳定性优化（多 agent 环境）**；**prompt caching 中间件（LangChain anthropicPromptCachingMiddleware）**；**semantic caching（arXiv：语义缓存+意图驱动上下文优化，缓存版本化按 schema hash 失效）**；**MASEval 评估库（多 agent 系统统一基准接口，GAIA/MMLU 或自定义任务）**；**Agent Framework 原生发 OTel spans（configure_otel_providers()）** |
| 4 | Activepieces（版本/模板/RAG） | OK | **Flow Versioning：publish/draft 状态+回滚**；**Piece version pinning：每步钉死 piece 版本（如 0.5.3），升级走 builder 显式选择，跨 minor/major 弹警告**；**Tables 存结构化上下文（prior prompts/entity IDs/validation flags），支持 stateful branching 跨 run 复用历史**；**LLM workflow：prompts 存 Tables 带 version 字段/owners/rollout flags**；**formula & data manipulation functions in flow builder**；**Flow Templates 跨项目/团队复用** |
| 5 | Make（错误处理） | OK | **Error Handler 附加任意模块（右键 Add error handler），错误时生成替代路径**；**五指令：Resume（忽略错误继续下一模块）/ Ignore（跳过当前 bundle 其他继续）/ Rollback（撤销场景开始后所有事务模块更改）/ Commit（确认错误前更改）/ Break（移除出错的 bundle，存 incomplete execution，自动或手动完成）**；**Rollback 适用于支持事务的模块（MySQL/Data Store）**；**Retry error handler：暂停失败 bundle、存错误消息+映射+剩余流程，自动或手动重试**；**错误 handler 常见配对：Resume 用于瞬时失败、Break 用于畸形响应需人工审查**；**dead-letter 实践：错误日志进 Google Sheet/Slack #scenario-errors/dead-letter Airtable**；**LLM 集成 stale context：检索在去重后或加时间戳过滤** |
| 6 | Pipedream（触发器/事件源） | OK | **触发器四类：HTTP（请求触发）/ Cron（时间调度）/ Email（入站邮件）/ Event sources（app 事件）**；**Connect webhooks：CONNECTION_SUCCESS/CONNECTION_ERROR 事件，payload 不含用户凭证**；**triggers.deploy() 可编程部署 HTTP webhook**；**subscriptions API：单 workflow 监听 10 个不同 RSS 源（emitter_id/listener_id）**；**组件生命周期 hooks：activate()/deactivate() 管理 webhook 订阅**；**REST API 批量取事件 /v1/sources/{id}/events?n=1** |
| 7 | Anthropic（上下文工程） | OK | **prompt caching：cache_control breakpoint（最多 4 个），缓存 breakpoint 前所有 token 的 KV 状态；cache read 0.10×、cache write 1.25×；TTL 5 分钟（默认，write 无额外费用）/1 小时（extended，write 2×）**；**增量缓存：每轮对话最后 block 标 cache_control，后续自动复用最长前缀**；**server-side compaction 是长对话/agentic 工作流推荐策略，自动总结旧上下文**；**上下文工程三层组合：token counting（发前测，catch prompt bloat at build time）/ context engineering（trim/summarize/externalize，少带）/ model selection（每单元工作路由到能胜任的最小模型）** |
| 8 | GitHub（Copilot CLI） | OK | **内置 specialized custom agents：Explore（快速代码分析不污染主上下文）/ Task（跑命令，成功给摘要失败给全输出）/ Plan（分析依赖结构做实现计划）/ Code-review（高信噪比）/ Research（深研带引用）/ Rubber duck**；**/fleet 并行子 agent 执行；/delegate 交给 cloud agent；/remote 从 GitHub.com 或 mobile 控制本地会话；/ide 连 IDE；/mcp 管理 MCP；/plugin 管理插件市场；/skills 管理技能；/tasks 看后台任务**；**自定义 agent profile 在 .github/agents 目录**；**copilot --allow-tool='write' 允许免确认文件编辑**；**/after 30m 调度非重复 prompt** |
| 9 | OpenClaw（ACP/插件） | OK | **ACP agents：OpenClaw 通过 ACP backend 插件跑外部 coding harness（Codex/Claude Code/Gemini CLI），sessions_spawn runtime:"acp"**；**子 agent 上下文默认限定 AGENTS.md+TOOLS.md，persona/记忆/用户/heartbeat 文件排除在委托 worker 之外**；**/acp spawn --agent claude --thread auto|here**；**兼容更新回滚（failed updates 恢复前包与配置）**；**Unified Plugins workspace（ClawHub + bundled 一处管理）**；**/steer 实时引导 active run 不新开 turn**；**sessions 原生绑定+transcript mirror+tool/media/terminal-outcome/settled-turn results** |
| 10 | Hugging Face / ModelScope | OK | **HF Skills：标准化 agent skills 框架（huggingface/skills 仓库 7,374 stars），面向 AI/ML 任务（数据集创建/模型训练/评估），从脆弱的原始代码生成转向结构化工具执行，兼容 Claude Code/Codex/Gemini CLI/Cursor，遵循标准化 Agent Skills 格式**；**HF 'agents that think in code' harness（~1,000 行核心 Apache 2.0）：模型写可执行 Python 作动作格式而非 JSON 工具调用，可选沙箱（E2B/Docker/WebAssembly）、managed sub-agents、Hub 分享 tools+agents**；**Agents-A1（InternScience 35B MoE agent 模型）：GAIA 96、SciCode 44.3，tool use/function calling 原生**；**Nex-N2 Agentic Thinking 闭环（需求理解→任务规划→代码实现→环境反馈→评估调试→持续迭代）**；ms-agent v1.6.0rc1 Agentic Insight v2 |

## 判重（双键检索，增量判定）
- Dify 编排（r284 节点/版本控制、r285A 提示词编排、r285C 可观测）→ Hybrid Agent/Tool/Iteration 并行/条件 guard 新面 → **新面**
- n8n 错误恢复（r284B 已落错误处理）→ 重叠约 50%，增量=子工作流工具隔离/failover 链/Execution Data 元数据（≥40%） → **合并保留增量**
- LangFlow 缓存/评估（r284 记忆/多Agent、r285B 存储）→ 语义缓存/评估库 新面 → **新面**
- Activepieces 版本（r284 分支/触发器、r285B 错误、r285C MCP）→ version pinning/Tables stateful branching 新面 → **新面**
- Make 错误处理（r284 迭代聚合/路由、r285A 蓝图、r285C Data Store）→ 五指令错误处理 新面 → **新面**
- Pipedream 触发器（r284C 已落触发器）→ 重叠约 55%，增量=subscriptions API 多源监听/组件生命周期 hooks（≥40%） → **合并保留增量**
- Anthropic 上下文工程（r285A 连接/MCP、r285B 结构）→ cache_control/TTL/compaction 推荐 新面 → **新面**
- GitHub Copilot CLI（r285A 已落 Copilot 代理）→ 重叠约 55%，增量=专用 agents 四件套/fleet 并行/自定义 agent profile（≥40%） → **合并保留增量**
- OpenClaw ACP（r284 自动化、r285A 命令、r285B 记忆）→ ACP backend 跑外部 harness/子 agent 上下文最小化 新面 → **新面**
- HF Skills（r284A 已落 Agent Skills 生态）→ 重叠约 45%，增量=HF skills 仓库/thinks-in-code harness/Agents-A1（≥40%） → **合并保留增量**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 混合 Agent/Tool 编排与迭代并行 | 工作流 |
| 2 | n8n 子工作流工具隔离与故障转移（合并增量） | 工作流 |
| 3 | LangFlow 语义缓存与多 Agent 评估 | 工作流 |
| 4 | Activepieces 版本钉死与状态化分支 | 工具 |
| 5 | Make 错误处理五指令与死信 | 工具 |
| 6 | Pipedream 触发器分类与订阅 API（合并增量） | 工具 |
| 7 | Anthropic 上下文工程三层与缓存定价 | 可复用 Skill |
| 8 | Copilot CLI 专用代理与并行执行（合并增量） | 工具 |
| 9 | OpenClaw ACP 外部 harness 与上下文最小化 | 工具 |
| 10 | HF Skills 与 think-in-code harness（合并增量） | 可复用 Skill |

## 复核
十独点均有当日实拉来源；7 新面 + 3 合并保留增量（增量均≥40%），零纯重复。版本建议 3.73.0。