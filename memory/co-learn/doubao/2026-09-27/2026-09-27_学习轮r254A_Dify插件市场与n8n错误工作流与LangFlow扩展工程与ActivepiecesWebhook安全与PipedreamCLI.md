# r254-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（插件市场面） | ✓ | Dify Marketplace 800+ 社区+官方插件（模型供应商/工具/数据源/MCP 集成，一键安装，团队跨应用复用已审批插件）；应用交付五形态：standalone web app/backend service API/tools in other Dify apps/MCP servers/marketplace templates；Trust Is a Feature 插件生态治理（marketplace 清单+saas 调用数据）；Creator Center & Template Marketplace（创作者发布 workflow 模板，Affiliate Program 收益）；热门插件 ComfyUI/Firecrawl/Bright Data Web Scraper/飞书云盘/腾讯TokenHub |
| 2 | n8n（error handling 面） | ✓ | Error Workflow：Workflow Settings 设置，执行失败触发，必须以 Error Trigger 开头，可复用多 workflow，发邮件/Slack 告警；Continue on Fail：HTTP 单请求失败不杀整个执行，输出含 $error 字段下节点判断重试/继续；AI 错误诊断模板：Error Trigger 传完整错误上下文（message/stack trace/failing node）给 LangChain Agent 根因分析+结构化输出（category/confidence/remediation）；恢复模式：扫描 status='failed' and retry_count<max → 读 Last Successful Step 从断点恢复（Switch/子 workflow）而非重启全流程；执行日志调试五步（开失败执行→找节点记名字+错误→检查输入→…）；LLM tool calling 可视化 trace；模型 failover 链（Agent Variables 计数 fail_count+指数退避） |
| 3 | LangFlow（custom component 面） | ✓ | Custom Component：继承 Component 类；display_name/description/icon 元数据；inputs（MessageTextInput 等）+Outputs+process 逻辑；lfx extension init my-extension 工程化：extension.json（v0 manifest）/pyproject.toml（pip-installable）/src/lfx_my_extension（__init__.py）；组件 bundle=相关组件打包（贡献回 Langflow 需 bundle）；LANGFLOW_ALLOW_CUSTOM_COMPONENTS=false 禁用自定义组件执行（安全开关）+LANGFLOW_COMPONENTS_PATH 白名单 allow-list；langflow-builder-mcp（tool_mode=True 生成自定义组件代码）；1.9 Assistant+Flow DevOps Toolkit+MCP for IDEs |
| 4 | Activepieces（webhook 面） | ✓ | 三触发技术：Polling/Webhooks/App Webhooks（OAuth2 developer app，Slack/Square 每 app 单 webhook）；handshakeConfiguration+onHandshake 返回 WebhookResponse{status, body}；安全最佳实践：secret tokens+HTTPS+TLS+每次请求验签+payload 结构验证+严格认证+rate limit+审计日志+端点不公开+定期轮换凭据；HMAC 签名验证（Code step 计算比较，早期拒绝，记录签名+时间戳审计，nonce 防重放）；AP_APP_WEBHOOK_SECRETS 环境变量；webhook waitpoints（flow 暂停到特定回调 URL，run 唯一 URL，带 body/headers/query，async+sync respond-when-done）；Event Streaming 审计事件转发 webhook 建自定义告警；256-bit 加密凭据+日志掩码敏感信息 |
| 5 | Make（data store 面） | ✓ | Data Stores：场景运行间持久化查询数据；Search Records 模块（field+operator+value）；操作符 Equal/Not equal/Contains/Does not contain 等——与 Activepieces Tables 同类，细节增量弱 |
| 6 | Pipedream（CLI 面） | ✓ | pd init（app/action/source 模板生成）；pd init connect（Connect 项目初始化：创建项目/OAuth client/选择 demo app）；pd login；pd publish action.js（发布 component 为 action）；pd deploy my-source.js（本地部署 source）；pd events -n 10 <source>（取最近 10 事件）；Edit with AI：workflow builder 内 AI 编辑现有 workflow/代码 step/调试；Python code steps（handler(pd)；环境变量；文件存储）；Connect SDK npm i @pipedream/sdk（10,000+ tools/3,000+ APIs/managed auth） |
| 7 | Anthropic（Agent SDK 面） | ✓ | claude-agent-sdk（Python+TS）：query/ClaudeAgentOptions/AssistantMessage/ResultMessage；Agent=应用通过规划自身步骤+调用工具（读文件/跑命令/改代码）完成任务；SDK 给与 Claude Code 相同 tools+agent loop+上下文管理；npm install @anthropic-ai/claude-agent-sdk；pip install claude-agent-sdk；Managed Agents：client.beta.sessions.create（agent/environment_id/title）；跨会话上下文管理+file+git 状态持久化模式 |
| 8 | SkillsMP（技能市场面） | ✓ | 技能库 800,000+ 且增长中；按职业浏览（U.S. Dept of Labor SOC taxonomy 800+ 职业）；分类目录规模：内容创作 36,330/项目管理 101,753/销售营销 311,661；changelog：搜索升级更快更相关；免责声明：分类/GitHub stars/源时效是组织信号非质量认证，用前打开详情审查源码；aiskillstore/marketplace（agent 自主发现购买出售 AI 能力，escrow 支付） |
| 9 | OpenClaw（MCP 面） | ✓ | openclaw mcp 双角色：openclaw mcp serve（OpenClaw 作为 MCP server 暴露 tools）；list/show/set/unset（管理 outbound MCP server 定义）；servers 配置 launch（streamable-http URL）/tools/resources/listChanged；工具太多混淆 agent：用 allowed_tools 只暴露所需、移除当前角色不需要的 server、按任务拆分配置；最佳 MCP servers：Parallel Search/Task/GitHub OAuth/Playwright/Notion；OAuth server 重认证 openclaw mcp login <name> |
| 10 | DeepLearning.AI（新课程面） | ✓ | 新课程：Agent Memory（Oracle+LangChain，长期记忆=外部模型持久化结构化一等公民基础设施）；Building Adaptive AI Agents（2026-08）；AI Code Review（2026-09）；Pydantic for LLM Workflows（Ryan Keenan，结构+可靠性+验证）；Multimodal Data Pipelines；Document AI: OCR to Agentic Doc Extraction（LandingAI，传统 OCR 丢表格合并单元格布局/图表-标题关系/多栏阅读顺序→agentic 提取）；Build Interactive Agents with Generative UI（自定义 UI 图表/表单/白板按需生成）；AI Coding Workflows From Cloud to Local（JetBrains） |

## 判重基准
双键检索（相对 r224-r253C 已落章节）：Dify（r253-A/B/C 多面——Marketplace/治理/交付五形态面独有）；n8n（r253-A agent/r253-B code node/r252 多面——error workflow/Continue on Fail/断点恢复面独有）；LangFlow（r253-A/B/C 部署/widget/A2A——r252-C 曾落自定义组件基础，本轮增量=lfx extension 工程化+ALLOW_CUSTOM_COMPONENTS 安全开关+bundle ≥40% 可合并保留增量）；Activepieces（r253-A piece/r253-B run/r253-C schedule——webhook 安全+waitpoints 面独有）；Pipedream（r253-B REST/r253-C triggers/r252-C sources——CLI+AI 编辑面独有）；Anthropic（r253-A 预建/r253-B output/r253-C custom——Agent SDK 面增量≥40%，备选）；SkillsMP（r251 落过基础——80 万规模+SOC 职业浏览增量，备选）；OpenClaw（r253-A skills/r250-C hooks——MCP 双角色面增量，备选）；Make（r251-C Data Store——操作符细节重叠不落）；DeepLearning.AI（未落——Pydantic/Agent Memory/Document AI 方法，备选）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 插件市场与交付五形态 | Marketplace 800+ 插件+治理+应用交付形态 | 工作流 | wb-execute-discipline |
| ② n8n Error Workflow 与断点恢复 | Error Trigger+Continue on Fail+$error+Last Successful Step | 工作流 | wb-execute-discipline |
| ③ LangFlow lfx 扩展工程与安全开关 | extension.json 结构+ALLOW_CUSTOM_COMPONENTS+组件 bundle | 工具 | wb-execute-discipline |
| ④ Activepieces Webhook 安全与 waitpoint | HMAC 验签+nonce 防重放+webhook waitpoint 暂停恢复 | 工作流 | wb-execute-discipline |
| ⑤ Pipedream CLI 与 AI 编辑 | pd init/publish/deploy/events+Edit with AI | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 备选未落：Anthropic Agent SDK/OpenClaw MCP/SkillsMP 规模/DeepLearning.AI 课程方法（留痕存档后续批次再判）。
- 垃圾：本轮未产生临时文件。
