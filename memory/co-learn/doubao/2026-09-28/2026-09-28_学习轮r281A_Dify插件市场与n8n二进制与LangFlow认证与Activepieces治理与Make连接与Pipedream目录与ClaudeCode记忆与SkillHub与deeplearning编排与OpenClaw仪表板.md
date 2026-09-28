# r281A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r280 全表 30 词 + r279 全表 30 词 + r278 全表 30 词错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（plugin marketplace） | OK | Marketplace 官方目录（官方标签 263 项、928 列出插件、907 有安装记录）；插件类型（Models/Tools/Data Sources/Triggers）；PR 到 langgenius/dify-plugins + 12 项 reviewer checks；治理 blog「Trust Is a Feature」；EdgeOne Pages 插件（ZIP/HTML 即时部署 public URL）；DupDub 音频插件（语音转写/声纹克隆/TTS）；v1.0 时 120+ 插件 |
| 2 | n8n（binary data） | OK | 三个二进制专用节点：Convert to File / Extract From File / Read-Write Files from Disk；item 结构（json 键必含，binary 键=Base64 data+mimeType+fileExtension）；Combine by Position 修复分支丢失 binary；`$(nodeName).item` 回取任意前节点 binary；Code node Buffer 造 CSV；form upload 多文件（Files_0/Files_1）；Split In Batches reset:false 循环 |
| 3 | LangFlow（api keys） | OK | API key（x-api-key header 或 query 参数）；/v1/run/$FLOW_ID 默认要求 key；key 校验可在 DB 或 env var；**key 只允许访问创建者用户的 flows/components**；Workflow API（POST /flows/{flow_id}/run）；lfx serve 起 FastAPI server（公开可访问必须 LANGFLOW_API_KEY）；JWT 认证（HS256 默认、可配 RS）；LANGFLOW_SECRET_KEY（Fernet 加密敏感数据） |
| 4 | Activepieces（projects） | OK | Projects 每团队独立空间 sealed off；Access Control（Okta/Entra SSO、Admin/Editor 等角色、Create/Edit/Run 细粒度）；governance（组织决定可用哪些 app、IT 管理 service accounts 团队复用）；cross-team versioned workflows draft-to-publish；workflow owner/backup owner/escalation path + review gates + runbooks；agent 归属项目（项目决定 agent 可达 connections/flows/files）；Centralize credentials/variables + RBAC |
| 5 | Make（connections） | OK | Manage providers 对话框；连接外部 provider（如 Relevance AI：name/api key/region/project）；AI agents 配置 tab（create/duplicate/configure/delete）；agents 与 connections 一样团队共享 |
| 6 | Pipedream（apps directory） | OK | 公共目录 3,224 apps / 14,966 registry tools；registry 结构（components/[app-slug]/[app-slug].app.mjs + actions/ + sources/）；app slug 用于 MCP headers/tool keys；pcloud 示例（OAuth Pipedream-managed、12 actions 1 trigger）；llms.txt（https://pipedream.com/llms） |
| 7 | Anthropic（Claude Code memory） | OK | CLAUDE.md vs auto memory 两套系统；CLAUDE.md=用户写指令规则、每会话开始加载；auto memory=Claude 自己写（~/.claude/projects/<project>/memory/、四类笔记 user/feedback/build/debug、MEMORY.md 作索引）；两者是 context 非强制配置（强制用 PreToolUse hook）；memory tool（跨会话存储检索、BetaAbstractMemoryTool 子类）；/memory 命令；server-side memory（Settings>Memory、pause/reset/delete 单条）；三层记忆论（CLAUDE.md 2026 更新） |
| 8 | 腾讯 SkillHub（首次实拉） | OK | 中国优化 Skills 社区；8万+ Skills；国内高速镜像秒装；三线并行安全审核；支持 WorkBuddy/QClaw/ima；首发 TRACE 评测体系；SkillPay（经验封装成 Skill 调用计费变现）；办公（腾讯文档 skill、PPT 一键生成）/营销（QQ浏览器抓竞品）/开发（WorkBuddy 零代码报表）；技能锻造炉（元技能：创建/升级/重铸/审计、10 维加权评分）；微信公众号 AI 创作发布全链路 skill（4 套写作模板+去 AI 味清单+12 项质检+自包含 publish.py）；EdgeOne Skill（ClawHub/SkillHub 分发） |
| 9 | deeplearning（community/charonhub） | OK | The Batch（charonhub.deeplearning.ai）；Meta 代理编排研究（agent 间 message passing 提升性能、memory surrogate 一个 agent 替另一个记）；DeepLearning.AI Pro（150+ 课程、Agentic AI course、LLM Post-training by Sharon Zhou、PyTorch 证书）；AI Engineering Skills Map |
| 10 | OpenClaw（dashboard） | OK | Gateway Control UI（默认 /，gateway.controlUi.basePath 覆盖）；http://127.0.0.1:18789/；openclaw dashboard（short-lived one-time owner pairing link → 签名浏览器获得 durable administrator device credential，重开不依赖共享 Gateway token；同一浏览器重开 fresh handoff 可修复受限设备凭据）；openclaw gateway status 监听 18789；TLS 时 https/wss；远程连接需 Gateway token & pairing 修复 |

## 判重（双键检索，增量判定）
- Dify 插件市场（r280A 变量/r280B 供应商/r280C 检索/r279 分块环境变量 Agent）→ 新面（插件生态与治理）
- n8n 二进制（r280B 模板/r280C 重试/r276 数据转换）→ 二进制节点结构与数据键规范为独有增量 → **落地**
- LangFlow API key（r280B secrets 环境变量）→ 重叠>60% 但认证机制（x-api-key/JWT/lfx serve/Fernet）含 ≥40% 独有增量 → **增量合并**
- Activepieces 项目治理（r280C 版本治理/r279C 流程）→ 新面（项目隔离+RBAC+governance）
- Make 连接（r280A 优化/r280B 时区/r280C 审计）→ 新面（connections 与外部 provider）
- Pipedream 应用目录（r280B 组件开发已落 registry 结构）→ 重叠>60% 但公共目录 3224/14966+llms.txt+app slug 为独有增量 → **增量合并**
- Anthropic Claude Code 记忆（r280A 记忆三层/r279 无）→ 新面（CLAUDE.md vs auto memory 机制）
- 腾讯 SkillHub → 全新站点首次实拉 → **新面**
- deeplearning（r280A 四模式/r280B prompt/r280C 微调/r279 评估）→ 新面（代理编排研究+Pro 生态）
- OpenClaw dashboard（r280A 记忆/r280B hooks/r280C 渠道）→ 新面（dashboard 配对与凭据）

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 插件市场与治理 | 工具 |
| 2 | n8n 二进制数据处理 | 工具 |
| 3 | LangFlow API key 与认证 | 工具 |
| 4 | Activepieces 项目治理与 RBAC | 工具 |
| 5 | Make 连接与外部 provider | 工具 |
| 6 | Pipedream 应用目录与 registry | 工具 |
| 7 | Anthropic Claude Code 记忆系统 | 工具 |
| 8 | 腾讯 SkillHub 平台 | 可复用 Skill |
| 9 | deeplearning 代理编排研究 | 工作流 |
| 10 | OpenClaw dashboard 配对与凭据 | 工具 |

## 复核
十独点均有当日实拉来源；两点为增量合并（均含独有增量）、八点为新面；无纯重复。版本建议 3.59.0+。