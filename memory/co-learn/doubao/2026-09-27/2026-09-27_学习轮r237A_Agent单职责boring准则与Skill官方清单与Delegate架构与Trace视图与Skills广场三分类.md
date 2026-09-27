# r237-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（AgentOps/可观测面） | ✓ | LangSmith/Langfuse 增强可观测（评估成本/延迟/质量）；Trace 视图（节点耗时/prompt 构造/token 用量/响应延迟/失败信息+中间值定位错误节点）；日志集成 Langfuse/LangSmith/Arize/Opik/W&B Weave；publish app 为 MCP-compatible tools；AgentOps（跨 agent token/cost 追踪+保存 completions 微调便宜 25x）；阿里云 AgentLoop full-stack observability（token/延迟精确追踪定位成本热点） |
| 2 | n8n（模板/实战面） | ✓ | Supervisor AI 路由 Expert agents（多 agent 混合 RAG 模板）；agent 单职责 boring 准则（get account context/add note/page on-call）；complex agent patterns（orchestrator 决定 specialist：billing/tech/account）；Shopify triage agent 总是返回 reasoning+confidence（API 失败告警携带推理链，低置信先人审）；支持收件箱 triage（分类/优先级/起草，人仍发送）；Dual-RAG（Qdrant+Gemini/Qwen）；低延迟语音 agent（Retell AI+日历） |
| 3 | GitHub（榜单面） | ✓ | stablyai/orca（agent 开发环境 ADE：桌面/移动/远程并行 agent 舰队）；BuilderIO/agent-native；agent-browser（Rust 43K stars）；Grok Build（8 并行 agent，Society of Mind）；deer-flow（long-horizon SuperAgent harness：沙箱+记忆+工具+技能+子 agent+消息网关）；casdoor（agent-first IAM：OpenClaw/MCP/OAuth/OIDC/SAML）；executing-plans 技能（分块执行每步验证 200K 下载） |
| 4 | Anthropic（Skill 官方最佳实践面） | ✓ | Skill authoring best practices 清单（Description 具体含关键术语+何时用；SKILL.md <500 行；额外细节独立文件；无时效敏感信息；术语一致；示例具体；文件引用一层深；渐进披露；工作流步骤清晰）；多 Skill 组合（Excel+PPT/Word+PDF）；避免未用 Skill（影响性能）；Managed Agents（system/tools 在 agent 不在 session，agent 创建一次 ID 引用）；官方预建 Skills（PPT/Excel/Word/PDF） |
| 5 | Pipedream（2026 面） | ✓ | Managed auth 全公开（hosted OAuth+secure token storage+自动 refresh；凭据加密 at rest scoped per project）；Retrieve end user credentials via API（免费 1000 账户）；AI Agent Builder（平台内 prompt/run/edit/deploy 秒级）+AI Code Generation；externalUserId token callback；MCP server 10,000+ tools |
| 6 | Make（integration 面） | ✓ | Maia by Make（AI 协同）；MCP client 更新；monday.com AI modules；API endpoint credential requests 新版本+scenario usage tracking+connection filtering；Claude Opus 5/Gemini 3.6 Flash 支持+OpenAI 降 credit；Make AI Agent（New）app（run an agent：创建 agent+工具+知识） |
| 7 | skills.sh/LobeHub（市场面） | ✓ | LobeHub Skills Marketplace 334,137 Skills；Agent Teams skill（Claude Code agent teams 多 agent 团队编排）；mcp-builder（创建 MCP server 的技能）；proactive-agent（任务响应转主动）；matt-pocock skills 263.3K stars 超 React（/grill-with-docs+/tdd red-green 循环） |
| 8 | docs.openclaw.ai（delegate/权限面） | ✓ | Delegate architecture（每组织一 delegate agent；先加固 tool restrictions/sandbox/hard blocks/audit trail；IdP 最小权限；standing orders 自主操作；cron 定期；信任建立调能力层）；skills-config（agents.defaults.skills 基线+entries.*.skills 特定）；tool policy 模型调用前执行（移除则收不到 schema）；acpx permissionMode 独立于 exec 审批；官方插件免能力同意/第三方非交互不授 |
| 9 | deeplearning.ai（新课程面） | ✓ | AI Code Review（2026-09-14）；AI Coding Workflows: From Cloud to Local（09-06）；Building Adaptive AI Agents；Document AI: From OCR to Agentic Doc Extraction；AI Prompting for Everyone（Andrew Ng）；Voice for AI Agents |
| 10 | 腾讯 SkillHub（官方技能生态面） | ✓ | Skills 广场（腾讯云智能体平台技能扩展中心：首批 28 内置 Skills 覆盖办公/医疗/图像/音视频/搜索 7 大场景；ZIP 自定义导入；ClawPro 安装使用）；三分类（内置安全审查+质量验证/企业共享/自定义）；SkillPay 支付体系（2026-07-16 同链路：分发+调用+支付，微信支付底层）；官方实时口径（全球 AI Agent 工具 44 万+、Skill 近 30 万、日均新增 1300+） |

## 判重基准
双键检索：n8n（r236-A/B/C 已落，本条独有增量=单职责 boring 准则+reasoning+confidence 不因工具失败丢失）；Anthropic（r236-A 已落规格/安全审查，本条独有增量=官方 best-practices 清单 500 行/一层引用/渐进披露+agent/session 生命周期分离）；OpenClaw（r236-A/B 已落注入成本/会话级 send，本条独有增量=delegate 架构加固先行+skills 基线继承+tool policy 前置）；Dify（r236-A/C 已落节点定位/插件评级，本条独有增量=Trace 视图观测载体+多观测平台集成+AgentOps 成本热点定位）；腾讯（r235-C 已落 SkillPay，本条独有增量=Skills 广场三分类+ZIP 导入+腾讯生态内置+官方口径修正）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① n8n 单职责 boring+推理保留 | agent 只做一件事；输出必带 reasoning+confidence；工具失败不丢推理，低置信先人审 | 工作流 | wb-execute-discipline |
| ② Anthropic Skill 官方清单 | 500 行上限/一层引用/渐进披露；多 Skill 按需组合；agent 一次创建 session 每次跑 | 可复用 Skill | wb-execute-discipline |
| ③ OpenClaw delegate 架构 | 每组织一 agent；加固先行+IdP 最小权限+standing orders+信任分级；skills 基线继承；tool policy 模型前执行 | 工作流 | wb-execute-discipline |
| ④ Dify Trace 视图+AgentOps | 节点耗时/中间值定位；多观测平台集成；成本热点定位到工具/模板 | 工具 | wb-execute-discipline |
| ⑤ 腾讯 Skills 广场三分类 | 内置/企业共享/自定义三分类+ZIP 导入；腾讯生态原生；官方实时口径修正 | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：wb-context-compressor 可吸收"Skill 官方清单 500 行上限/渐进披露"控制自身体积（下轮评估合并）；wb-ponytail 无变化需求。
- 垃圾：本轮未产生临时文件。
