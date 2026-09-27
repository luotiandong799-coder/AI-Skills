# r237-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（插件生态面） | ✓ | Trust Is a Feature（插件生态治理：进包什么/能达什么/审哪个版本/证据变化怎么办）；Creator Center+Template Marketplace（发布模板+PartnerStack affiliate 佣金）；Ollama 插件（本地模型+thinking output+tool calling）；Unstructured 插件（PDF/DOCX→Markdown/JSON 供 RAG 增强）；GPUStack（开源 GPU 集群管理）；SageMaker 插件 |
| 2 | n8n（AI Assistant/模板面） | ✓ | Build your first AI agent 模板（Chat Model+2 tools+Conversation Memory）；OpenClaw Clone 模板（Telegram+多模型+子工作流+MCP+webhook）；Multi-Agent 个人助理（Manager 编排 memory/todo/email/calendar/research）；ZapPro WhatsApp triage（10s 缓冲+urgency regex/AI 打标 {handoff}+human takeover "unlock"）；Jarvis MCP 生产力 agent；Agent 节点参考（Tools Agent：system message 列允许动作与精确最终格式+Max Iterations=最长工具链+2） |
| 3 | GitHub（MCP 生态面） | ✓ | official GitHub MCP（HTTP+OAuth 一条命令）；n8n-mcp 21.8K；modelcontextprotocol/servers 87.3K；jev2mcp（context-aware MCP/plugin/tool 选择层）；mcpvault（Obsidian 安全 MCP）；routa（workspace-first 多 agent 协调：Specs+Kanban+MCP/ACP/A2A）；crawl4ai/firecrawl MCP |
| 4 | Anthropic（官方文档面） | ✓ | Skill 运行时限制（代码执行容器：无网络访问/无运行时包安装/隔离 fresh container）；字段规格（name≤64 小写字母数字连字符禁 XML 禁保留词 anthropic/claude；description 非空≤1024）；触发双向调优（undertriggering 加细节/术语；overtriggering 加 negative triggers）；Iterate with Claude（让 Claude 捕获成功方法与常见错误进 skill，跑偏自省）；安全考量 |
| 5 | Pipedream（MCP 面） | ✓ | 2600+ integrated apps 全部发布为 MCP servers（个人免费）；remote.mcp.pipedream.net 托管端点 10,000+ tools/3,000+ APIs；per-user auth+tool discovery built-in；streamable HTTP transport（+SSE+stdio）；debug flag 看 tool call 实际 API |
| 6 | Make（AI 能力面） | ✓ | Maia（对话式 AI 同事：自然语言建自动化+可视化构建步骤+create/modify/debug；public beta 全付费，free 30 天）；下一代 AI Agents（建在 scenario builder 同画布：built/run/debugged+激进透明每个决策可见可控）；Make AI Agent（New）app（run an agent 创建 agent+工具+知识）；3,000+ Verified Apps |
| 7 | skills.sh/ClawHub（排行面） | ✓ | Self-Improving Agent 419K+ downloads（3K+ stars 最强社区信号：记录发现/批判输出/数周改进）；Ontology Memory ~188K（跨会话持久记忆）；Google Workspace (gog) ~185K；Felo Search ~145K；Agent Browser（社区公认第一必装：语义搜索技能库匹配需求推荐最佳 Skill+一键安装自动配置）；skills-search CLI |
| 8 | OpenClaw（能力面） | ✓ | Plugin skills（openclaw.plugin.json skills 字段，插件启用时加载；browser 插件带 browser-automation）；PDF 一等工具（原生分析路由 Anthropic/Google，其余 fallback 文本/图像；agents.defaults.pdfModel）；Skill Workshop（proposal→pending draft+hash/rollback→applied 才 live）；多渠道网关+Mobile nodes；v2026.6.9 独立 provider 插件 npm 发布 |
| 9 | deeplearning.ai（AI Code Review 课程面） | ✓ | AI Code Review（Qodo 合作 1h4m Intermediate：从早跑 review 到给 reviewer 正确 context；自建 review agent；context 是 review 可靠关键）；Agentic AI 9h55m（Module 4 evals/error analysis/component-level evals）；Vibe Coding 101 with Replit；Claude Code: A Highly Agentic Coding Assistant |
| 10 | 腾讯 SkillHub（企业专区/新动态面） | ✓ | 团队空间（2026-06 正式开放：技能沉淀/安全审核/权限管控/多端调用企业级管理）；自定义 Skill 提交企业共享（审批通过沉淀为企业共享供全空间复用）；企业 PAY SKILL（按调用计费）；腾讯云 AI 服务 Skills 上架（tencentcloud-faceid/aigc-recog-video/image/text，ClawHub/SkillHub 安装配密钥即用） |

## 判重基准
双键检索：Anthropic（r236-A/r237-A 已落规格/清单，本条独有增量=字段规格 64 字符禁保留词+触发双向诊断+运行时容器三无）；Pipedream（r236-A/r237-A 已落，本条独有增量=全 app 发布 MCP+单端点+streamable HTTP+debug flag）；Make（r236-B/r237-B 已落，本条独有增量=agent 与场景同画布+激进透明+Maia 对话 debug）；ClawHub（r235-C 已落自改进，r237-A 已落 LobeHub，本条独有增量=Ontology Memory+Agent Browser 语义匹配+排行实证 419K）；OpenClaw（r236-A/r237-A/B 已落，本条独有增量=plugin 打包技能+PDF 一等工具原生路由+workshop proposal 双态）；腾讯（r235-C/r237-A 已落，本条独有增量=团队空间治理+企业共享提交审批+腾讯云服务 Skills 上架）；Dify 插件治理与 r236-A 重叠>60% 含部分增量，并入工具层已有条目不单列。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Anthropic Skill 字段规格+触发调优 | name≤64 禁保留词；under/overtriggering 双向诊断；运行时容器无网络/无装包/隔离 | 可复用 Skill | wb-execute-discipline |
| ② Pipedream 全 app MCP | 2600+ app 全部发布 MCP；单端点万工具；per-user auth+streamable HTTP | 工具 | wb-execute-discipline |
| ③ Make agent 同画布+Maia | agent 在 scenario 画布内 built/run/debug；激进透明；Maia 对话构建 debug | 工具 | wb-execute-discipline |
| ④ ClawHub 排行观察 | Self-Improving 419K 首装；Ontology Memory 跨会话；Agent Browser 语义匹配推荐 | 可复用 Skill | wb-execute-discipline |
| ⑤ OpenClaw plugin 技能+PDF+Workshop | 插件打包技能随启用加载；PDF 一等工具原生路由+fallback；proposal→applied 双态 | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：wb-context-compressor 长度控制合并评估继续挂账（Skill 官方清单 500 行+渐进披露已足够支持，下轮批处理）；wb-ponytail 无变化需求。
- 垃圾：本轮未产生临时文件。
