# r249-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Make（AI agent 工具命名面） | ✓ | 工具命名与描述（agent 按名字与描述选工具；清楚描述做什么何时用）；LLM 是脑工具是手；工具描述即 prompt（Anthropic：工具描述与正常 prompt 同等提示工程关注；OpenAI：详细函数描述、清晰 enums、intern test——人类只看文档能否正确调用）；窄工具 vs 宽包装（get_invoice_by_id(invoice_id) 远安全于 query_database(sql) 把原始 SQL 交给 LLM；类型化 schema 输入输出校验）；AWS 工具契约四要素（clear name getQuarterlyRevenue；explicit parameters region EMEA/APAC/AMER；return format；error conditions 404/503）；Namespacing（asana_search/jira_search 前缀分组）；最小权限（agent 最小 tools/scopes/data/action+approval gates+监控每次调用+定期移除）；数据边界显式（prompt 写 Only orders from last 90 days/Only data for authenticated customer）；OpenAI 工具三型（Data 检索上下文/Action 交互系统/Orchestration agents 作其他 agent 工具 Manager Pattern） |
| 2 | Pipedream（components 面） | ✓ | Components=自包含可执行代码单元（triggers+actions）；用户配置输入产出输出；源码公开 GitHub repo；Registry 结构（components 目录每 app 对应目录：airtable.app.mjs/package.json/actions/sources）；开发流程（本地编辑器开发、自己 repo 维护；CLI 部署/publish；sources 可直接本地部署或 publish；actions 只能 publish）；默认仅自己账号可用；publish 到 team 共享；MCP server（remote/self-host 二选一；2700+ APIs/10000+ tools）；Connect SDK（3000+ apps 嵌进自己的 App/Agent 统一鉴权；pd.triggers.deploy webhook 事件；per-user auth 单调用）；许可证（source-available registry license 禁止用代码跑竞争 SaaS）；主仓库 11.7K stars |
| 3 | Anthropic（skills/frontmatter 面） | ✓ | frontmatter 字段（name 可选显示名目录名兜底 lowercase/numbers/hyphens max 64；description 推荐做什么何时用缺省用正文首段；when_to_use 可选触发词/示例请求追加到 description 计入 1536 字符 cap；argument-hint 斜杠命令参数提示）；description+when_to_use 合并截断 1536 字符（降低上下文占用）；加载机制（仅 name+description 会话开始加载；正文在调用时动态加载——slash command 或自动触发）；位置（.claude/skills/ 个人；SKILL.md name+description+body）；skill authoring best practices（保留词 anthropic-helper/claude-tools；命名一致；documents/data/files 目录约定）；agentskills.io spec 要求 name required vs Claude Code optional |
| 4 | GitHub（awesome agent skills 面） | ✓ | awesome-agent-skills 生态（hesreallyhim awesome-claude-code 综合 Claude Code 生态；ComposioHQ awesome-claude-skills 最大 Claude skills 列表；sickn33 antigravity-awesome-skills 1445+ agentic skills 跨 Claude Code/Gemini CLI/Cursor/Copilot/Codex；heilcheng awesome-agent-skills Skills+tools+tutorials）；VoltAgent awesome-agent-skills 1500 官方技能（fal.ai 15/netlify 12 分类）；anthropics/skills 官方仓库（mcp-builder 技能引导构建 MCP server 处理常见错误；frontend-design）；ghtrends agent-skills（SenseNova-Skills；anysearch-ai unified real-time search engine skill 3326 stars；GPT-Image2-Skill 3057 image prompt library agentic skill CLI）；agent-scripts（steipete 5203 stars）；OASIS（camel-ai 4857 one million agents simulation）；ouroboros（q00 4733 Agent OS Stop prompting Start specifying）；awesome-llm-apps 132k stars |
| 5 | Hugging Face（tools/spaces 面） | ✓ | smolagents（~1000 行核心代码；CodeAgent 写+运行 Python vs ToolCallingAgent JSON 工具调用；模型无关；集成 MCP/LangChain/Hub Spaces 工具；沙箱 E2B/Modal/Docker）；Space as Tool（注册 Space 为工具链调用：识别需求→调用生成 Space→取输出 URL→调用组装 Space→返回结果）；Gradio Space 暴露 agents.md 纯文本 API schema 让 agent 无客户端库调用；Space /api/predict 手动测试（不要假设 payload {"data":[input]} 通用；加 timeout/error handling/响应检查）；Hub MCP（hf_fs 语义搜索/探索 repo；Contribute Repos 创建仓库写文件；Sandboxes 隔离环境）；hf-agentfinder（PyPI registry adapter for HF Spaces） |
| 6 | ModelScope（创空间/智能体面） | ✓ | 魔搭 Agent 大本营（0 代码创建/发布/分享专属 Agent；modelscope-agent 开源）；Studio 创空间（免费灵活 AI 应用展示空间；Gradio/Streamlit/Docker/静态网站；本地项目部署支持：创建/代码同步/部署/日志监控/明文与 secret 变量管理/自动诊断修复）；MCP Plaza（MCP 广场）；魔粒体系（全站通用激励积分；技能服务墙——个人主页展示 AI 专业技能/商业服务）；Agents-A1（35B MoE agentic 模型：Long-horizon Search/Engineering/Scientific Research/Instruction Following/Tool-calling）；Civision 创意内容生成 |
| 7 | 腾讯（元器平台面） | ✓ | 元器（腾讯官方智能体平台：标准模式/单工作流模式/Multi-Agent 模式 3 类应用模式；发布渠道管理：元器官网默认渠道不可改删，可创建发布到微信公众号/小程序/微信客服/API）；公众号智能体（授权公众号发布审核后微信端 AI 分身）；测试验证→发布正式环境；腾讯效率智能体工具集（个人提效/办公提效/企业提效 20+ 垂直场景；QClaw/WorkBuddy/元宝/ima/腾讯文档；WorkBuddy 企业版 AI 工作台）；Hy3 Agent 能力（元宝 Agent：自然语言描述复杂任务生成 PPT/Word/Excel/PDF/HTML） |
| 8 | 智谱（AgentMore 面） | ✓ | AgentMore（智谱清言推出 AI 智能体协作与 Skills 扩展平台：多 Agent 协作、技能市场扩展、任务执行与工作流编排；多角色并行与工具调用；创建 Agent 并安装 Skills 技能；基础免费）；AutoGLM（自主执行 50+ 步长步骤操作，跨 app 执行；电脑操作 GLM-PC；边想边干）；智谱清流（企业级智能体开发平台：零/低代码编排、企业知识库 RAG、效果评测迭代闭环、AutoGLM 界面操作代理；平台编排+代理执行）；大模型五阶段（Chat/Coding/Agent/Co-work/Autonomous AI）；TAC Token 架构能力（智能调用量×智能质量×经济转化效率） |
| 9 | 阿里（智能体生态面） | ✓ | 支付宝超级服务智能体"阿宝"（万余项服务 AI 化接入；八大核心场景：出行打车/餐饮点餐/文旅景区/政务民生；跨端 5 大手机品牌/16 家主流车企；AHA 跨端智能体互联协议；全栈智能体商业底座；联合千问/华为/OPPO/比亚迪/吉利 20+ 企业）；阿里云 OpenClaw 生态（CoPaw 小龙虾 2 月 14 日通义团队发布：钉钉/飞书/QQ/Discord/iMessage 接入、云端或本体部署、GitHub 开源；JVS Claw 一键养虾 3 月 13 日：零代码三步拥有 AI 智能体"龙虾"、无需配置节点和大模型 API 密钥、万能 skill 自进化）；阿里企业级 Agent 平台"悟空"；字节 Ark 云上 SaaS 版"龙虾" |
| 10 | deepseek（DSH 插件生态面） | ✓ | deepseekplugin.cn（DSH 插件目录：28 用途分类/6725 可安装验证/8330 结果；dsh-market 设置页内浏览搜索安装社区插件、分类筛选、一键更新停用、主题切换配置备份）；awesome-dsh-plugin（1206 个插件；UI/记忆/视觉/多 agent/自动化方向；cooljser 门户 701 插件 12 分类 444 作者）；DSH 定位（Everything is a Plugin：模型/工具/UI/SKILL/MCP/API 全部可替换插件；大模型负责理解推理 Harness 负责执行插件让 AI 按需获得专业能力）；插件清单（dsh-market/modlens 模型视觉/dsh-web-ui/better-sidebar 侧边工作台/dsh-at-file 快速引用/desktop 原生桌面端/dsh-web-search-pro 多源搜索/OpenViking 跨会话记忆/dsh-cost-meter 费用看板）；商业化观察（长尾 ToB：数据库巡检/云部署编排插件）；发布数据（8 月 13 日预览版开源 13 天 19.5 万 stars/2.21 万 forks；dsh plugin add dsh-plugins-store 安装） |

## 判重基准
双键检索（相对 r244-r249A 已落章节）：工具设计（r231C 落"工具描述即 prompt"——本批 intern test/窄工具 vs 宽 SQL 包装/契约四要素/namespacing 为增量≥40% 合并保留增量落地）；Pipedream（r241B 落场景转 MCP/credit 计量——components 自包含单元/registry 目录/本地开发 CLI 发布/actions 只能 publish 为独有增量）；Anthropic skills（r237A 落官方清单/r241A 落 frontmatter 契约——1536 字符 cap/仅元数据加载正文动态加载为增量深化合并）；国内平台（r246B 落 SkillHub 本土镜像——元器三模式/AgentMore 技能市场/阿宝 AHA 协议为独有新面）；DSH（r225A/r237B 落全插件化——8330 插件/28 分类/dsh-market/商业化长尾为增量更新）。未选素材：ModelScope 创空间（部署形态+secret 变量+技能服务墙）；HF Space as Tool（agents.md schema+链式调用）；GitHub awesome lists（VoltAgent 1500/antigravity 1445+）；Pipedream MCP remote/self-host。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① 工具设计契约四要素 | 窄工具+intern test+契约四要素+namespacing | 工具/可复用 Skill | wb-execute-discipline |
| ② Pipedream 组件生态 | 自包含单元+registry 结构+CLI 发布 | 工具/工作流 | wb-execute-discipline |
| ③ skills frontmatter 契约 | 1536 cap+元数据加载正文动态加载 | 可复用 Skill | wb-execute-discipline |
| ④ 国内平台生态观察 | 元器三模式/AgentMore/阿宝 AHA | 可复用 Skill | wb-execute-discipline |
| ⑤ DSH 插件生态 | Everything is a Plugin 具体化+插件分类 | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
