# r280C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r280A/B 二十词 + r279 全表 30 词 + r278 全表 30 词错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（KB search modes） | OK | 三检索模式：Vector（语义）/Full-text（关键词精确，适合产品码/ID）/Hybrid（混合推荐+rerank）；检索设置（Rerank 模型如 gte-rerank、Top K 默认 3、Score Threshold）；多模态 embedding（Vision 图标、图文跨模态检索）；混合权重（weaviate alpha 默认 0.75、向量 0.7+关键词 0.3 加权）；腾讯云稠密+稀疏双路；Qdrant 混合检索 |
| 2 | n8n（HTTP request errors） | OK | Retry on Fail（Settings 开、Max Tries 上限 5、Wait Between Tries 上限 5 秒、指数退避可选）；rate limit 场景 Wait > rate limit；429 分支（Continue On Fail + If node 查 $json.error.response.status === 429）；Timeout 合理设（30s）；REST retry endpoint（/api/v1/executions/{id}/retry）；"最便宜的可靠性 win" |
| 3 | LangFlow（custom components） | OK | Component 类继承；class 属性（display_name/description/icon）；inputs/outputs 列表（MessageTextInput、Output method=build_message）；方法定义行为+内部错误处理与日志变量；自定义组件可作 agent 工具（Code pane 输 Python）；contribute bundles（xxx_component.py + __init__.py）；LANGFLOW_ALLOW_CUSTOM_COMPONENTS=false 禁止任意代码执行（安全开关）；Langflow Assistant 自然语言建组件（View Code 检查） |
| 4 | Activepieces（versioning） | OK | draft 编辑→publish（发布版锁定不可编辑）；编辑已发布 flow→自动建新 draft 复制已发布版本（可回滚旧版编辑不影响发布版）；piece version pinning（每 step 记录确切版本 0.5.3，**不自动升级**，升级显式经 builder，跨 minor/major 有警告）；versioned automations 跨团队审核测试上线 |
| 5 | Make（audit logs） | OK | Audit logs（Enterprise 计划、谁改 scenario 何时改、org owner/admin/team admin 访问）；Scenarios>Logs API（/scenarios/{id}/modules/{id}/logs，execution id/timestamp/status）；执行日志存场景结构**快照**（触发修改/删除后历史数据仍在日志——审计需区分 live 结构与历史快照）；audit trail 记录（run_id/trigger_id/model_id/action_taken 等可重放）；PII-safe redaction（"Data is confidential" 不存 payload、加非 PII telemetry）；Make MCP server（list_scenario_logs 调试） |
| 6 | Pipedream（triggers/sources） | OK | 两类 trigger：App-based event sources / Native triggers；event sources 独立资源可触发多个 workflow；触发类型（HTTP/Cron/Email/Event sources）；source 能力（props 部署接受输入、HTTP/Timer 接口、emit 事件、built-in key-value store、deduping strategies）；RSS source 三消费（SSE 流/触发 workflow/批处理 REST）；timer polling 自动取历史事件；Connect 触发（HTTP webhook 推荐 OAuth client / deploy event source） |
| 7 | Anthropic（prompt caching） | OK | 定价乘数：5m cache write=1.25×base、1h cache write=2×base、cache hits/refreshes 仅 10%（Opus 4.7 base $5/MTok→写 $6.25/$10、命中 $0.50、输出 $25）；两种启用：Automatic caching（顶层 cache_control 字段）/显式 breakpoint；新闻原文：写缓存 +25%、用缓存仅 10% |
| 8 | GitHub Copilot（agent mode） | OK | agent 模式（chat 底部 agents dropdown 选 Agent）；autonomous peer programmer 多步任务（分析 codebase/读文件/propose edits/跑命令测试/响应编译 lint 错误/自动纠错循环）；terminal 命令需用户确认；**coding agent vs agent mode 区别**（coding agent 在 GitHub Actions 环境自主完成 issue/chat 任务建 PR；agent mode 本地 IDE 直接改） |
| 9 | deeplearning（fine-tuning） | OK | Fine-tuning & RL for LLMs: Intro to Post-training（Sharon Zhou、6h10m、43 视频课、11 评分作业；核心 fine-tuning/RLHF/reward modeling/PPO/GRPO/LoRA）；Generative AI with LLMs Week 2（instruction fine-tuning/multi-task/PEFT LoRA）；微调决策（Fine-tuning Decision、Data Strategy、LoRA/QLoRA in Practice） |
| 10 | OpenClaw（agents/channels） | OK | multi-agent routing（tools agentToAgent enabled+allow）；channel routing（discord/googlechat/imessage/irc/line/signal 等，每个 provider 独立配置块）；channel config（allowFrom、textChunkLimit、chunkMode length/newline、mediaMaxMb、sendReadReceipts、groups requireMention）；各渠道凭据（Telegram botToken、Discord botToken+applicationId、Slack botToken+appToken+signingSecret、WhatsApp phoneNumberId+accessToken+webhookUrl，令牌用环境变量）；自定义渠道（allowed_channels/ignore_channels/max_messages_per_hour/cooldown_seconds/auto_reply/typing_indicator） |

## 判重（双键检索，增量判定）
- Dify KB 检索（r280A 变量/r280B 供应商/r279A 分块/r278A 混合检索）→ r278A 已落 hybrid rerank，本面=三模式+Top K/Score Threshold+多模态 embedding → **增量合并**
- n8n HTTP 重试（r280A 表达式/r280B 模板/r279A 错误）→ r279A 已落 n8n 错误处理，本面=HTTP 节点 Retry 配置细节（上限 5/指数退避/429 分支/REST retry endpoint）→ **增量合并**
- LangFlow 组件（r280A widget/r280B secrets/r279C 工具）→ r279C 已落 LangFlow 工具面，本面=自定义组件+安全开关 → **增量合并**
- Activepieces 版本（r280A MCP/r280B AI/r279C 流程）→ r279C 已落流程控制，本面=flow draft/publish 版本控制+piece 钉版 → **增量合并**
- Make 审计（r280A 优化/r280B 时区/r279C 数据存储）→ 新面（审计日志/PII 脱敏/结构快照陷阱）
- Pipedream sources（r280A 认证/r280B 组件/r279A 调度）→ 新面（事件源/去重策略/RSS 三消费）
- Anthropic 缓存（r280A subagent/r280B hooks/r279C 缓存已落）→ r279C 已落缓存面，本面=定价乘数+Automatic 启用 → **增量合并**
- GitHub Copilot（r280A reusable/r280B 搜索/r279C Copilot 已落）→ r279C 已落 Copilot agent，本面=agent mode 细节+coding agent 区别 → **增量合并**
- deeplearning 微调（r280A 四模式/r280B prompt/r279A 评估）→ 新面（微调/RLHF/PEFT 决策）
- OpenClaw 渠道（r280A 记忆/r280B hooks/r279C 配置/r278C 多代理）→ r278C 已落 sub-agents、r279C 已落配置，本面=渠道路由/凭据/多代理 routing → **增量合并**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 检索三模式与重排设置 | 工具 |
| 2 | n8n HTTP 节点重试与限流 | 工具 |
| 3 | LangFlow 自定义组件与安全开关 | 工具 |
| 4 | Activepieces flow 版本与 piece 钉版 | 工具 |
| 5 | Make 审计日志与 PII 脱敏 | 工具 |
| 6 | Pipedream 事件源与去重策略 | 工具 |
| 7 | Anthropic 缓存定价与启用 | 工具 |
| 8 | GitHub Copilot agent 模式 | 工具 |
| 9 | deeplearning 微调与 PEFT | 工作流 |
| 10 | OpenClaw 多代理与渠道路由 | 可复用 Skill |

## 复核
十独点均有当日实拉来源；六点为增量合并（均含独有增量）、四点为新面；无纯重复。版本建议 3.58.0+。