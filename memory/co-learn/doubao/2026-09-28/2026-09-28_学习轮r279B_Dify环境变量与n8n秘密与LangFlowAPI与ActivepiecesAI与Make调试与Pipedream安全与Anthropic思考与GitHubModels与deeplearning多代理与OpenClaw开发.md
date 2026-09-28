# r279B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r279A/r278/r277/r276 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（环境变量/秘密） | OK | 环境变量应用级存储、执行时只读；三类型 String/Number/Secret（Secret 显示 ******、导出 DSL 防泄露）；SECRET_KEY（openssl rand -base64 42 生成、首启前设置、JWT 签名/会话加密）；DIFY_AGENT_SERVER_SECRET_KEY（JWE 加密 key、生产替换默认）；GKE Secret Manager（SECRET_KEY+DB 密码注入 pod、明文不进 spec、不旋转）；最佳实践=敏感 key 放环境变量不硬编码 |
| 2 | n8n（凭据安全） | OK | 凭据数据库加密存储默认限制访问；external secrets（AWS Secrets Manager/Azure Key Vault/Google Secret Manager/HashiCorp Vault/1Password/Akeyless）；引用语法 {{$vault.secret.path}} 或 $env:SECRET_NAME、运行时取最新版；多租户隔离（共享逻辑、租户凭据分离、tenant_id 动态加载、禁硬编码/共享 config/跨租户访问）；_FILE 后缀从文件读敏感值（Docker secrets）；Azure Key Vault v1.52.0 支持 |
| 3 | LangFlow（API 执行） | OK | Langflow 是 IDE 也是 runtime（Python/JS/HTTP）；/v1/run/{flow_id_or_name} 基础、/v1/run/advanced/{flow_id}（显式 inputs/outputs/tweaks）；Workflow API /api/v2/workflows 三模式 sync/stream(SSE)/background；/build/$FLOW_ID/flow 返回 job ID 流式事件；自动生成 Python/JS/curl 代码片段；--backend-only headless（无前端暴露 API）；LFX CLI（lfx run 一次执行流式 stdout、无 API key、lfx serve 暴露 HTTP）；TypeScript client |
| 4 | Activepieces（AI pieces） | OK | AI piece（Text AI Ask AI 等 6 actions、MIT 开源可自托管、与 760+ apps 组合）；OpenAI piece（Create Embedding/Search Embeddings/Generate Image/Edit Image/Text-to-Speech）；AI Agent Builder（admin 设 provider 一次：OpenAI/Anthropic/Gemini/Azure/Bedrock 或任意兼容端点、approval before 执行、max steps 20/run、外部 MCP）；MCP 暴露 workflows/tools 给外部 AI |
| 5 | Make（场景历史/调试） | OK | Scenario history（run 时间/名称/状态 success-warning-error/时长/操作数/credits + 用户改动日志）；Make DevTool（Scenario Debugger 历史日志、按模块名/ID 搜索、双击开设置）；执行日志（每模块 input/output+执行细节）；incomplete executions（防数据丢失）；执行日志是快照非实时引用（改 trigger 后旧结构残留）；错误监控 5 模式（Break/Resume/Retry、外部 DB 记录时间/场景/错误做趋势）；Make Code App（每执行完全可观测 inputs/outputs/error/execution logs 实时） |
| 6 | Pipedream（webhook 安全） | OK | 所有 webhook 投递 HMAC-SHA256 签名（x-pd-signature 头 t=timestamp,v1=signature 可验证）；HTTP 触发器默认公开无授权→推荐配置 authorization（custom token/OAuth）；Validate Webhook Auth action（第三方自有认证零代码校验）；Connect 代理（3,000+ APIs、credentials 加密 rest 按 project scope、永不经过你的服务器、一 API 调用撤销账号）；secrets 不进客户端代码、全 HTTPS、server-side 请求 |
| 7 | Anthropic（扩展思考） | OK | thinking: {type:"enabled", budget_tokens:N}；最小 1,024 tokens；预算必须 < max_tokens（思考和最终答案共享输出预算）；>32K 常不消耗满；手动模式（可预测延迟/精确成本）；adaptive thinking（max_tokens 硬限+effort 软指导）；Opus 4.6 budget_tokens deprecated 改 adaptive；调参从最小开始逐步增；成本实测 8k 输入+4k thinking≈3 倍费用；延迟 1-2k=+2-4s、4-8k=+5-10s、10-20k=+10-25s |
| 8 | GitHub Models | OK | playground（side-by-side 双模型对比、model presets 保存 prompts/参数/messages）；API（PAT with models scope→curl）；**2026-07-30 退役**——playground/model catalog/inference API/BYOK 全不可用，迁移 Microsoft Foundry Models；隐私承诺（prompts/outputs 不与模型提供商共享） |
| 9 | deeplearning（多代理课程） | OK | Design, Develop, Deploy Multi-Agent Systems with CrewAI（38 视频 6 代码 7 作业、production-ready）；Multi AI Agent Systems with crewAI（agents 元素/tools/多 agent 协作/customer support/event planning/financial analysis）；Practical Multi AI Agents（复杂 crews、内外集成、项目规划估算分配、progress report、性能测试+人类反馈优化）；CrewAI 框架（Crews+Flows、hierarchical manager、conditional tasks、async kickoff、or_/and_ 逻辑、zoom-in/out 观测、配置版本化） |
| 10 | OpenClaw（技能/插件开发） | OK | Skills 目录（workspace/skills/<name>/SKILL.md、frontmatter 命名非路径、可子文件夹分组）；插件随附 skills（openclaw.plugin.json 列出 skills 目录）；插件分发 npm、manifest（name/version/description/secrets）、CLI kebab/camel 避冲突；skills 开发 TypeScript/YAML、可私有或发 ClawHub（80% 分成）；Evolver 协议（agent 自举：自己写并安装新 Skill、知识生产/消费/验证闭环）；VISION（core lean、可选能力插件化、core per-call tax）；openclaw init my-plugin 脚手架 |

## 判重（双键检索，增量判定）
- Dify 环境变量（r279A 分块/r278C 可观测）→ 新面（Secret 类型/部署密钥管理）
- n8n 外部秘密（r279A 错误处理/r278C 源控制）→ 新面（vault 集成/多租户隔离）
- LangFlow API（r279A 记忆/r278C 可观测）→ 新面（程序化执行三模式）
- Activepieces AI（r279A 触发器/r278C 嵌入）→ 新面（AI piece/Agent Builder）
- Make 调试（r279A webhook/r278C 团队）→ 新面（历史/日志/DevTool）
- Pipedream 安全（r279A 调度/r278C CLI）→ 新面（webhook 签名/授权）
- Anthropic 思考（r279A 结构化/r278C Batch）→ 新面（thinking 预算/adaptive）
- GitHub Models（r279A 技能市场/r278C service containers）→ 新面（模型服务/退役迁移）
- deeplearning 多代理（r279A 评估/r278C 记忆）→ 新面（CrewAI 课程）
- OpenClaw 开发（r279A 会话/r278C 多代理）→ 新面（skill/plugin 开发与分发）

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 环境变量与秘密管理 | 工具 |
| 2 | n8n 外部秘密管理 | 工具 |
| 3 | LangFlow API 程序化执行 | 工具 |
| 4 | Activepieces AI pieces 与 Agent Builder | 工具 |
| 5 | Make 场景历史与调试 | 工具 |
| 6 | Pipedream webhook 安全 | 工具 |
| 7 | Anthropic 扩展思考 | 工具 |
| 8 | GitHub Models 与迁移 | 工具 |
| 9 | deeplearning 多代理课程 | 可复用 Skill |
| 10 | OpenClaw 技能与插件开发 | 可复用 Skill |

## 复核
十独点均有当日实拉来源；均新面或增量合并；无纯重复。版本建议 3.54.0+。