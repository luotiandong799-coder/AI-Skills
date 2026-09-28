# r279A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r278/r277/r276 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（知识库分块检索） | OK | 索引方法 High-Quality（向量/全文/混合可用）vs Economical（倒排索引）；Parent-child 分块（Paragraph/Full Doc 父块模式）；分块参数（最大块长默认 500 token、分隔符 \n\n、重叠 50 token、预处理去冗余）；知识检索节点 TopK 默认 3、Score Threshold 默认 0.5、rerank 加权分数（语义/关键词权重）；多模态 rerank 注意（非多模态会剔除图片附件）；Economical 模式 chunk 关键词（≤10 个）提升可检索性 |
| 2 | n8n（错误处理重试） | OK | 三层策略：per-node Retry On Fail（瞬时错误 2-3 次、指数退避 1s/2s/4s）→ Error Trigger workflow → Executions 手动重试；永久错误（401/畸形 payload）直接告警不重试；AI 分诊（Anthropic 分类 transient/logic + OpenTelemetry + 事故重试计数器 ≤3 次）；可复用重试子工作流（Execute Workflow 调用、指数退避+jitter）；重试配置 JSON（attempts/delay/backoff/maxDelay/conditions）；最终兜底=紧急通知 |
| 3 | LangFlow（会话记忆） | OK | Agent 组件内建 chat memory 默认开启（Langflow storage、按 session ID、最小配置=消息数）；Message History 组件（Langflow storage 或 Mem0/Redis 外部存储，结构化或解析输出）；Memory Base（向量化长期记忆、语义检索跨会话，区别于 Message History 时间顺序/知识库人工填充）；Playground Message Logs 按 session ID；Chat Input/Output 的 should_store_message 开关 |
| 4 | Activepieces（触发器） | OK | Trigger Technique=polling/webhook 两类型；Webhook 触发器注册（flow 发布时 register/unregister、sampleData）；Catch Webhook（任意 HTTP 方法）；Respond and Wait for Next Webhook（返回响应等下一个 webhook 恢复 flow）；Event Streaming（audit events 转发 webhook→flow 路由 Slack/Gmail/Teams）；Audit Log Events（flow lifecycle/run status/connection changes/user activity/admin actions）；MCP Webhook server（unique URLs） |
| 5 | Make（Webhook） | OK | Custom webhook 模块=唯一 URL 由第三方调用；webhook 只能放场景开头（instant trigger）；Redetermine data structure（自动确定入站结构）；Webhook response 模块（404/状态码/body）；HTTP 模块认证（No auth/API key/Basic Auth/OAuth 2.0 client credentials） |
| 6 | Pipedream（定时调度） | OK | Schedule source（预设间隔 15/30min/每小时/每天/每周/每月 + Cron Expression 完整控制含时区）；组件 timer interface（$.interface.timer、intervalSeconds）；一秒级 cron jobs（Custom Interval）；执行时限：HTTP/Email 触发 30s、cron 60s、付费档 750s |
| 7 | Anthropic（工具结果/结构化） | OK | tool_result content（字符串/嵌套 content blocks/document blocks）；structuredContent（JSON 机器可读数据与 content 并存）；isError=true 标记失败；Structured outputs 两特性：JSON outputs（output_config.format）+ Strict tool use（strict:true 校验工具名与输入 schema）；Agent SDK structured outputs（定义 JSON Schema→agent 自由用工具→返回 validated JSON，result 带 structured_output 字段）；content block 类型表（image/video/document/search_result/tool_use/tool_result/thinking） |
| 8 | 技能市场生态 | OK | skills.sh（npx skills add <owner/repo>、CLI、leaderboard）；SkillsMP（280,000+ 开源 skills、AI 搜索/分类、npx/bunx/pnpm 一键安装、无官方 CLI 需 ZIP）；VSCode Agent Skills 扩展（2,513+ 官方 + 91,000+ 社区、9-stage security pipeline）；awesome-agent-skills（npx skills find/add 装到 .cursor/skills/）；aiagentskills.net（verified 目录、一行命令）；CodeAgentSwarm（按 stars 排序、选安装位置） |
| 9 | deeplearning（评估驱动开发） | OK | NVIDIA GTC Eval-Driven Design（human-created datasets 迭代、continuous eval/iterate、prompt 实验）；AI Engineering 课程（shadow mode 真实流量对比、canary rollout 监控延迟/成本/错误自动回滚、golden dataset 专家验证对、field-level eval scores 门禁部署 CI/CD）；DeepEval（Answer Relevancy/Faithfulness/Precision/Recall/G-Eval、Golden Datasets、trace-based 组件级测试） |
| 10 | OpenClaw（会话记忆持久化） | OK | 三层记忆：短期=会话上下文、中期=每日日志（session-memory hook 天到周）、长期=MEMORY.md（无限期每周策展）；MEMORY.md 加载每个新会话、/new /reset 后重注近期日志、compaction 前把持久事实刷进日志；会话存储（sessions.json 元数据 + <sessionId>.jsonl append-only 树结构 id/parentId）；Honcho（用户/agent 画像、语义搜索过去观察、跨会话跨 channel）；ByteRover（domain→topic→subtopic 层级树全 markdown、curation agent）；外部批评=MD 记忆对上下文压力大 token 费用难控 |

## 判重（双键检索，增量判定）
- Dify 分块（r278A 混合检索/r278C 可观测）→ 新面（分块参数/parent-child）
- n8n 错误（r278A 队列/r278C 源控制）→ 新面（三层重试策略）
- LangFlow 记忆（r278B 向量存储）→ 新面（会话记忆组件/Message History）
- Activepieces 触发器（r278B piece 开发/r278C 嵌入）→ 新面（触发器类型/事件流）
- Make Webhook（r278B 蓝本/r278C 团队）→ 新面（webhook 模块配置）
- Pipedream 调度（r278B 协作/r278C CLI）→ 新面（cron/定时触发）
- Anthropic 结构化（r278A 缓存/r278B Computer Use/r278C Batch）→ 新面（tool_result/structured outputs）
- 技能市场（r278A/B/C 未直接覆盖市场目录发现机制）→ 新面（skills.sh/SkillsMP/CLI 生态）
- deeplearning 评估（r278A agentic RAG/r278B 编码代理/r278C 记忆）→ 新面（评估驱动开发）
- OpenClaw 会话记忆（r278A 安装/r278B 配置/r278C 多代理）→ 新面（会话存储/三层记忆）

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 知识库分块与检索 | 工具 |
| 2 | n8n 错误处理分层与重试 | 工作流 |
| 3 | LangFlow 会话记忆体系 | 工具 |
| 4 | Activepieces 触发器与事件流 | 工具 |
| 5 | Make Webhook 配置 | 工具 |
| 6 | Pipedream 定时调度 | 工具 |
| 7 | Anthropic 工具结果与结构化输出 | 工具 |
| 8 | 技能市场发现与安装生态 | 可复用 Skill |
| 9 | deeplearning 评估驱动开发 | 可复用 Skill |
| 10 | OpenClaw 会话与记忆持久化 | 可复用 Skill |

## 复核
十独点均有当日实拉来源；均新面或增量合并；无纯重复。版本建议 3.53.0+。