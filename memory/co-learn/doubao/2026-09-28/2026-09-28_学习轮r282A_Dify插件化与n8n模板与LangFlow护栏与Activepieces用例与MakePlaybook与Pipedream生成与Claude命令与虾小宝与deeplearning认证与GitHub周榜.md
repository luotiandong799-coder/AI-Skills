# r282A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站；查询词与 r281A/B/C 三十词 + r280 三十词 + r279 三十词 + r278 三十词 + r277/276 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（v1.0 版本演进） | OK | 插件化架构（Models/Tools 迁移到 Plugins，引入 Agent Strategies/Extensions/Bundles）；Agent node（Workflows/Chatflows 智能编排，ReAct Think-Act-Observe / Function Calling 两种可下载策略，引擎与控制系统解耦）；Endpoint Plugin（自定义服务处理外部 Webhook 事件）；Extension 插件（Dify 内托管自定义服务）；Dify Marketplace（社区插件共享市场）；v1.1.0 Metadata as Knowledge Filter（知识检索元数据过滤）；46,558 行开源 |
| 2 | n8n（模板市场） | OK | 官方 marketplace 1000+ 模板（核心团队+社区）；第三方市场（n8n Markets 2000+、n8ntemplatestore、n8ntemplates.me 7000+/12320+ 声称）；导入形态=workflow JSON 打包（load bundled workflow JSON→connect credentials→activate，自托管或云皆可）；~50% 免费、付费 $9-$200；模板按类别（CRM/邮件/DevOps/电商）；AI 生成模板；Re-run single steps 测试、pin data 防重复触发 |
| 3 | LangFlow（版本演进+Policies） | OK | 1.7 Streamable HTTP MCP、webhook 认证、ALTK/CUGA agent 组件；1.8 全球模型供应商集中配置、V2 workflow API（v2/workflow 端点、简化响应）；1.10 Assistant 建流、Memory bases 长期语义记忆、DB Providers 向量库后端、国际化 7 语言；1.11 stream 支持 EventManager+AG-UI 协议；1.12 发布；**Policies 组件：自然语言业务规则→buildtime 生成 guard code→runtime 工具调用前检查（guarded tools）**；Agentics bundle（aMap/aReduce/aGenerate 表格数据转换）；Graph RAG 组件（数据关系检索） |
| 4 | Activepieces（用例形态） | OK | AI-first automation 定位；23 个示例 agent（Support triage 支持分诊 4min 前运行、Invoice intake 发票收件、Inbound lead routing 线索路由按分钟内转交）；400+ 集成；**工作流可嵌入人工 review 阶段（pauses until designated user input）**；JavaScript code steps 注入处理数据转换；用例域：Edtech（入学流程/课程同步）、数据驱动（CRM 同步/报表）、RevOps（线索路由/合同后记录更新）、多系统（多层审批路由） |
| 5 | Make（场景库/Playbook） | OK | **Make AI Playbook（全用例目录：按团队/影响/AI maturity 阶段分类）**；7 个可复制 AI 示例（新员工入职：Airtable 监控→Slack 欢迎消息，按 onboarding stage 触发）；TripleTen 案例（广告创建 5-7 倍提速：创意库→多广告平台 API→统一命名上传）；AI 线索评分（Sheets→OpenAI 打分 0-100→CRM 路由）；AI 黑客松 10 agent（活动组织 agent）；Make Academy AI 自动化课程 |
| 6 | Pipedream（AI 代码生成/模板化） | OK | **AI code generation（代码步内用 AI 生成代码，props 自动接线）**；REST API 程序化创建 workflow（create workflow endpoint 从 workflow share link + 自己的 connected accounts/step props）；workflow share link 模板化分享；示例：Asana 任务从 Slack 触发词创建（10 秒内、tag 优先级+回溯链接）、Calendar→Slack 通知；Twitter 模式（tweet→SQS/EventBridge/Lambda/Telegram）；agent 功能（自然语言→自动工具调用） |
| 7 | Anthropic（Claude Code 斜杠命令） | OK | 自定义命令=Markdown 文件（.claude/commands/xxx.md，**文件名即命令名**）；Project 级（项目内共享）vs Personal 级（~/.claude/commands/ 跨项目）；frontmatter 配置（description/model/allowed-tools/disable-model-invocation）；**命令文件可覆盖同名内置 skill（shadowing）**；插件=打包分享 slash commands+agents+MCP servers+hooks（四个扩展点组合）；迁移坑清单（缺 user-invocable:true→/菜单不显示；allowed_tools 下划线→allowed-tools 连字符；$ARGUMENTS 参数展开；disable-model-invocation 防模型从上下文自动调用）；可让 Claude 直接创建命令文件 |
| 8 | 阿里虾小宝（首次实拉） | OK | **虾小宝中国 AI Agent Skills 地图（skillhub.wanuai.cn v3.0.3）**；**自主技能生成器技能（/learn <主题>：网络搜索+浏览器工具→发现/提取/综合文档→生成可复用技能）**；FunClaw（阿里云 FC 智能体：智能对话+技能扩展，企业/我的技能区；技能集：find-agentrun-skills 发现技能、fc-vpc-proxy VPC 代理、searxng 搜索引擎、agent-browser 浏览器、self-improvement 自我提升）；1688 遨虾跨境 AI 智能体（选品决策/工厂寻源/智能询价/内容生成）；Qwen 淘宝 agentic 购物 |
| 9 | deeplearning（课程认证体系） | OK | 课程三档：**Short Course（1-2hr，免费，无官方证书，PRO 完成得 Accomplishment）/ Course（3-10hr，可分享证书）/ Professional Certificate（10+hr，职业证书）**；Build with Andrew（PRO 完成评估得证书）；证书可验证（证书 ID 链接）；Coursera 合作（TensorFlow/PyTorch 专精）；Gartner 70% 开发者 2028 前用 AI 编码 |
| 10 | GitHub（agent 生态周榜） | OK | **claude-mem（94,765★：跨会话持久上下文——捕获 session→AI 压缩→未来会话注入相关上下文，兼容 Claude Code/OpenClaw/Codex/Gemini/Hermes/Copilot/OpenCode）**；Tencent/AI-Infra-Guard（AI 基础设施安全）；mattpocock/skills（技能标准化封装）；**ZeroClaw（Rust 重写 secure by default：默认拒公网暴露、限制文件访问）、NanoClaw（每对话独立容器、OS 级隔离）、TrustClaw（OAuth 托管凭据+远程沙箱）**；Orca（ADE 并行 agent 舰队）；EnvoyMesh（去中心化 P2P 自治 agent）；Comp AI CRM（agentic-first CRM）；Vibe-Trading（个人交易 agent）；Maestro（多 agent 编排） |

## 判重（双键检索，增量判定）
- Dify 插件化（r281A 插件市场/r281B 编排）→ v1.0 架构+Agent Strategies 可插拔+Endpoint 插件为独有增量 → **增量合并**
- n8n 模板市场（r281B code node/r281A 二进制）→ 新面（模板生态+JSON 导入形态）
- LangFlow Policies（r281C 向量/r281B 多代理）→ 新面（护栏组件）
- Activepieces AI-first（r281C 错误处理/r281B 构建）→ 新面（AI 分诊形态+human-in-loop）
- Make Playbook（r281C 模板/r281B 回滚）→ 新面（用例目录）
- Pipedream AI 代码生成（r281C 并发/r281B 签名）→ 新面
- Claude Code 斜杠命令（r281A CLAUDE.md 记忆/r281B agent skills）→ 新面（命令机制+插件打包）
- 阿里虾小宝 → 全新站点首次实拉 → **新面**
- DeepLearning 三档（r281C 编码课程/r281A 编排）→ 新面（认证体系）
- GitHub agent 周榜（r281 未拉具体榜）→ 新面（claude-mem/ZeroClaw 等）

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 插件化架构与 Agent 策略 | 工具 |
| 2 | n8n 模板生态与导入形态 | 工具 |
| 3 | LangFlow Policies 护栏组件 | 可复用 Skill |
| 4 | Activepieces AI-first 与人工环节 | 工作流 |
| 5 | Make Playbook 用例目录 | 工具 |
| 6 | Pipedream AI 代码生成与模板化 | 工具 |
| 7 | Claude Code 自定义斜杠命令 | 可复用 Skill |
| 8 | 阿里虾小宝技能生态 | 可复用 Skill |
| 9 | DeepLearning.AI 课程三档体系 | 工作流 |
| 10 | GitHub agent 生态周榜 | 工具 |

## 复核
十独点均有当日实拉来源；一点增量合并（Dify 含独有增量）、九点新面；无纯重复。版本建议 3.62.0。