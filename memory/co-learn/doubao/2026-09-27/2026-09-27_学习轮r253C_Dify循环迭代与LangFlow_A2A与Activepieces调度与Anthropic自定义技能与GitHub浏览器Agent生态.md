# r253-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（循环/迭代节点面） | ✓ | 迭代节点=对数组逐条执行相同步骤（输入须为列表）；循环节点=迭代友好版；循环变量跨迭代传递状态（Deep Research 6 变量：findings/executed_querys/current_loop/visited_urls/image_urls/knowledge_gaps）；最大迭代次数默认上限 100，超出自动终止触发中断，可设 break_conditions 提前退出；节点类型：开始（用户消息/API/定时/Webhook/插件事件/上传数据）/推理检索/控制流（分支/迭代/循环/合并）/执行（Dify 工具/自定义 API/MCP）；2026 引擎升级：并行节点执行（独立节点真并行）、条件分支支持正则/JSONPath、节点级错误捕获与重试 |
| 2 | n8n（workflow 模板/共享面） | ✓ | n8n.io/workflows 模板 11,229→12,239；分类目录（CRM 471/AI 7379）；社区模板经济：$29 一次性 3 个生产模板（Lead CRM/Stripe fulfillment/Form→Sheets+Slack，含 clean commented JSON+setup guide+test checklist）；33 垂直行业 pack（bookkeeping/legal/healthcare/gym/restaurant/YouTube，每包 10 个 workflow JSON）；ZapPro WhatsApp AI Agent 模板 $297/$497（triage/handoff/follow-up；error monitoring workflow 捕 DNS 失败告警 WhatsApp；credentials 走 credential manager 无硬编码）；自托管 n8n+Ollama 11 模板无需 API key（8GB RAM） |
| 3 | LangFlow（A2A 面） | ✓ | A2A（Agent2Agent）协议支持：LANGFLOW_A2A_ENABLED=true 开启（默认关，1.11）；发布 flow 供其他 agent 调用+flow 内调用远程 A2A agents；Agent Card：/.well-known/agent.json 标准 JSON 元数据（skills/modalities/endpoints）；A2A=跨框架跨厂商 agent 通信（Client/Server Remote Agent；任务委托）；1.12 OpenTelemetry（OTLP 兼容任何 backend）——服务健康+flow runs 可观测；1.11 Human-in-the-Loop+AG-UI streaming；A2ABreak 安全分析：Multi-Hop Identity Loss（身份仅传输层建立不跨 hop 传播，多跳委托链下游无法验证原始主体与委托来源）；AgentMaster：A2A 管 agent 间通信+MCP 管工具调用 |
| 4 | Activepieces（schedule 面） | ✓ | Schedule piece：6 triggers（Cron Expression 2 fields/every_hour 预设）；flow JSON schedule{cronExpression, timezone}；后台任务最佳实践：scheduled triggers+条件逻辑限新增/变更记录，在 Tables 持久化 last successful cursor/timestamp 只处理增量（delta）；Delay steps+自动重试恢复瞬时失败；Schedule piece MIT open source；每日报告/周期数据同步/定时通知/维护任务用例 |
| 5 | Make（integrations 面——返回偏通用 connector 生态） | ✓ | Make 2026 周更机制（facebook CAPI conversion value/linear/xero 稳定性/zoho recruit 搜索扩展；openai legacy 模型 9/28 弃用）；通用 connector 生态（MS 1,000+ connectors/Replit integrations/Unito 双向同步）——非 Make 特有，留痕"增量弱" |
| 6 | Pipedream（GitHub triggers 面） | ✓ | GitHub triggers：New Webhook Event (Instant)/New Workflow Job Completed (Instant)/New Workflow Run Completed (Instant)/New Commit/New Card in Column/New Collaborator；admin 权限=webhook 即时，无 admin=轮询；components=triggers+actions 自包含可执行代码单元（source-available GitHub registry 免写 boilerplate）；triggers deploy（externalUserId/id/webhook_url）；webhook 目标：trigger 级优先于 project 级；Trigger 类型：HTTP/Cron/Email/Event sources |
| 7 | Anthropic Skills（custom skill 创建面） | ✓ | Custom Skills 打包领域专长+组织知识，全产品可用：Claude Code 创建/Claude API 上传/claude.ai 设置添加；AWS/Microsoft Foundry 通过 Skills API 上传；SKILL.md 需 YAML frontmatter（name/description）；Agent Skills Cookbook 学创建；Python API beta.skills.create（files 同一顶层目录含 SKILL.md/display_name）；POST /v1/skills；API 使用：anthropic+自定义结构一致，指定 type+skill_id，可 version 钉版本；社区 5 步：~/.claude/skills/<name>/→SKILL.md（元数据+正文）→scripts/和 reference/→重启→测试迭代 |
| 8 | 智谱 AgentMore（平台面） | ✓ | AgentMore=智谱清言多 Agent 云端协作平台（2026-05-25）；GLM 体系升级；一句话招募最多 5 个 AI Agent 组队多智能体并行协作；Skills 技能广场一键配置现成专业技能；功能：智能体构建/工具调用（网页/文档/代码/业务系统）/流程自动化（重复操作沉淀为可复用流程）/协作扩展；BigModel 平台：GLM-5.3-Flash 原生多模态（自主完成研究分析/文档制作）、智能体市场/MCP/知识库/模型微调；智能体开发平台（零代码拖拉拽+批量调试+页面嵌入/API 发布）；AutoGLM 自主执行 50+ 步跨 app；GLM-PC 像人操作计算机；GLM Coding Plan 可接入 OpenClaw |
| 9 | Hugging Face（agent 模型面） | ✓ | 2026 上半年五款 Agent 开源模型（Ornith/Laguna/Nex N2/Devstral/Nemotron——训练目标"把事情办成"非"回答得好"，可本地部署）；Agents-A1（上海 AI 实验室 InternScience，35B MoE 基于 Qwen3.5-35B-A3B，256 专家 8 active，Apache 2.0，长视界研究/科学/工程）；DeepSeek-V4：百万 token 上下文、preserved reasoning traces 跨 tool-call 边界+用户轮次、XML-based tool-call schema 专用 token 减少解析失败、Rust 沙箱 DSec 用于 RL 训练真实工具环境；galileo-ai/agent-leaderboard（LLM for AI Agents 排行榜）；Llama 4 社区变体（编程/法律/医学/教育/业务/autonomous agents） |
| 10 | GitHub（browser agent 生态面） | ✓ | browser-use/browser-use：113K+ stars MIT（Playwright+vision+DOM hybrid 提取，YC W25）；vercel-labs/agent-browser：浏览器自动化 CLI for AI agents 40K stars apache-2.0；BrowserSkill：4.7K stars TS MIT（2026-09-18 trending #4）——登录态复用痛点（无痕浏览器被验证码/短信/SSO 拦，AI 网页任务最别扭的是登录状态）；BrowserAct：anti-detection/持久会话/并行执行/SkillHub 100K+ skills——"last mile"问题；Gbrow：OpenClaw AI agents headless browser（accessibility tree snapshot/@ref clicks/tabs/JS execution）；BrowserOS 开源 Agentic browser；microsoft/magentic-ui、lavague-ai/lavague |

## 判重基准
双键检索（相对 r224-r253B 已落章节）：Dify（r253-B 环境变量/r253-A 多路召回——循环迭代控制流面独有）；LangFlow（r253-B widget/r253-A 部署——A2A 协议+OTel 面独有）；Activepieces（r253-B run 可观测/r253-A custom piece——schedule+增量处理面独有）；Anthropic Skills（r253-A 预建 4 个/API 集成——custom skill 创建四通道+skills.create API ≥40% 独有增量可合并）；GitHub browser agent（r251-C 生态观察——browser agent 专项 4 库+登录态复用 ≥40% 独有增量可合并）；智谱 AgentMore（未落——多 Agent 5 个组队+技能广场+AutoGLM 50 步，备选）；Hugging Face Agent 模型（r252-C ModelScope 微调/数据集——agent 化模型新面，备选）；n8n 模板经济（r252 多面——弱增量不落）；Pipedream GitHub triggers（r253-B proxy/r252-C sources——admin webhook vs 轮询增量弱不落）；Make（r253-A blueprint/r253-B 通用调度——本周更机制弱不落）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 循环与迭代节点 | 迭代=列表逐条+循环跨迭代状态+最大次数/break+并行执行 | 工作流 | wb-execute-discipline |
| ② LangFlow A2A | LANGFLOW_A2A_ENABLED+Agent Card+flow 双形态（发布/调用）+OTel | 工作流 | wb-execute-discipline |
| ③ Activepieces Schedule | cron trigger+timezone+Tables 游标增量处理 | 工作流 | wb-execute-discipline |
| ④ Anthropic Custom Skills 四通道 | frontmatter+四产品通道+skills.create API+版本钉 | 可复用 Skill | wb-execute-discipline |
| ⑤ GitHub Browser Agent 生态 | browser-use hybrid+agent-browser CLI+登录态复用+anti-detection | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 备选未落：AgentMore 多 Agent 组队/Agent 模型（生态/模型层增量，留痕存档后续批次再判）。
- 垃圾：本轮未产生临时文件。
