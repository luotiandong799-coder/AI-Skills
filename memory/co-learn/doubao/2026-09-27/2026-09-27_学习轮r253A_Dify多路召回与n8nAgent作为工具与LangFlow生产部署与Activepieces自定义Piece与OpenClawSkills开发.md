# r253-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（knowledge retrieval 多路召回面） | ✓ | Multi-path Retrieval：同时查询 Context 连接的全部知识库，收集所有相关 chunks，最后 Rerank 策略选最优（多知识库同时召回更全更准）；Knowledge Retrieval 节点支持 1+ 知识库（多库同时检索后按节点级设置合并）；Vision 标签支持跨模态；Citations and Attribution：Chatflow 默认响应旁展示引用可关（Studio→Add Features 开关；引用来源段落+Jump to Knowledge Base 链接）；检索三模式：vector search 语义/full-text BM25 关键词/hybrid；rerank 用 Cohere Rerank 等；多模态知识库：text+image 统一语义空间（AWS Bedrock/Google Vertex/Jina/Tongyi 多模态 embedding+rerank）；聚合实现：所有线程结果收集共享列表→去重+rerank（DatasetRetrieval.multiple_retrieve） |
| 2 | n8n（AI Agent tools 面） | ✓ | Tool calling 内建 AI Agent 节点：视觉连接工具，n8n 处理执行循环（model structured request→API call→back）；Tools Agent=Langchain tool calling 接口（描述工具+schemas）+标准输出格式+增强输出解析；MCP 支持：agents 可连任何 MCP-compatible tool server；AI Agent Tool 节点：root agent 可把其他 agent 作为 tool 调用（orchestrator 有多个 tools，其中工具本身是完整配置的 agent 有自己的模型——多 agent 编排简化）；OpenAI Functions Agent=函数检测模型（必须 OpenAI Chat Model）；生产复杂 agent 模式：AI Agent Tool=第二 agent 配置成 tool |
| 3 | LangFlow（deploy production 面） | ✓ | Langflow runtime（production）：headless backend-only 服务专注 Langflow API，flows 作为 endpoints 暴露，只跑 serve 每个 flow 的进程；最低 2Gi RAM+1000m(1CPU)/实例×3 replicas；外部 PostgreSQL 推荐（替代默认 SQLite 提升扩展性可靠性）；部署形态：Docker（--backend-only --env-file --host 0.0.0.0 --port 7860，LANGFLOW_AUTO_LOGIN）/Nginx+SSL（Let's Encrypt+Certbot 自动证书）/Caddy/K8s；Flow DevOps Toolkit SDK：lfx init 项目→environments.yaml 控制部署（local→production；api_key_env 环境变量名引用 API key）；容器环境变量：LANGFLOW_COMPONENTS_PATH/LANGFLOW_LOG_ENV=container |
| 4 | Activepieces（custom piece 面） | ✓ | 扩展性：用户和开发者都能建 piece（TypeScript 框架），自定义 triggers+actions 部署 flows 或分享社区；CLI：npm run build-piece 提示输入 piece 名→编译导出 .tgz；npm run pieces -- build --name=your-piece-name 生成 dist/packages/pieces/your-piece-name tarball→Platform Admin→Catalogue→Pieces→Install Piece；Piece Type：custom（自用）/community（共享）；开发：AP_DEV_PIECES 环境变量（逗号分隔列表）从本地 dist 加载不走 DB；认证：PieceAuth.CustomAuth 收集属性（base_url+access token props）；CI/CD：离线开发→package.json 增版本→PR main→merge 后手动 CLI 或 GitHub/GitLab Action 同步 |
| 5 | Make（blueprint 面） | ✓ | Blueprint=可复用场景版本（含模块+设置+映射值）；保存/复制为 blueprint 共享（组织内外）；备份场景（换账号/失去访问）；导出复用；List Blueprint Versions API（scenarioId；归档只保留 60 天内版本）；Export scenario blueprints API；Scenario sharing：链接共享（无需登录可看，永远最新版，替代模板共享）；Templates API：blueprint 对象（general setup+apps+modules+settings）+scheduling+controller（wizards） |
| 6 | Pipedream（concurrency/error 面） | ✓ | Auto-retry on errors（Advanced plan）：失败 step 重跑至多 8 次/10 小时指数退避（不重试 OOM/timeout）；maxRetries 默认 10（python rerun），超限→workflow 继续下一步（要异常则 raise）；自定义错误处理：catch rate limit→解析 Retry-After 头→等待→原 payload 重试；validation error→转换数据→修正 payload 重试；Concurrency：限 1 worker=序列化按序执行（每事件等前一事件完成）；超队列大小→事件丢失+错误邮件（付费可增至 10,000 队列）；Event History 重放一个/多个过去事件（bulk replay failed）；全局 $error event stream 订阅 |
| 7 | Anthropic Skills（预建 skills 面） | ✓ | 预建 4 个：pptx（演示文稿）/xlsx（表格分析）/docx（文档）/pdf（PDF 生成）；Skill IDs 短名（pptx/xlsx/docx/pdf），日期版本（20251013 或 latest）；custom skills 生成 skill_01AbCd.../skver_01...；可用：claude.ai/Claude API/AWS Platform/Microsoft Foundry（需 Hosted on Anthropic）；Messages API 一次最多 8 个 skills；官方仓库 anthropics/skills（source-available 非 open source；含 canvas design/docx/pdf/pptx/xlsx/frontend design/MCP builder/skill creator）；金融服务 10 个 ready-to-run agent templates（pitchbooks/KYC/月结）plugin 形式 Claude Cowork+Claude Code；Claude add-ins 跨 Excel/PPT/Word/Outlook |
| 8 | GitHub（trending AI 仓库面） | ✓ | 9/23 trending：AI agents+coding assistants 最大集群；superpowers 269K stars（obra/superpowers）agentic skills framework（skills 供 agent 使用）；LibreChat 44962 stars（ChatGPT clone：Agents/MCP/Skills/DeepSeek/Anthropic/AWS...自托管）；OpenClaw 382K stars（MIT 自托管个人 AI assistant）；harnesses.sh：75 harnesses profiled 9-axis capability schema；trendshift：rocketride-server（C++ core+50+ Python-extensible nodes，13+ model providers/8+ vector DBs）/tigerless-labs/agent-memory/browser-use jev-ultrafast/mattpocock skills；ii.dist.by top-100：n8n 187.8K stars 第一 |
| 9 | OpenClaw（skills 开发面） | ✓ | Skills=插件扩展 agent 能力（SKILL.md+支持文件）；skills/ 目录（~/.openclaw/workspace/skills/），可放子文件夹组织，命名由 frontmatter 决定；安装：clawhub install <skill-name>（10,700+ skills）/openclaw skill install web-search（ClawHub 或 Git repo：下载+验证 manifest+注册）；clawhub update --all/clawhub sync --all（扫描本地+发布更新）；配置：openclaw skill configure web-search（交互或 config 文件）；OAuth/API key 授权；安全：安装时 VirusTotal scan passed 验证（~/.openclaw/skills/<skill-name>.md，即装即用无需重启）；创建：mkdir -p ~/.openclaw/workspace/skills/hello-world；SKILL.md frontmatter（name/description） |
| 10 | DeepSeek（插件生态/市场面） | ✓ | awesome-deepseek-integration 官方维护：54 款应用/插件（应用 24：Chatbox/Cherry Studio/NextChat 等）；DeepSeek V4 for Copilot Chat：VS Code 插件把 V4 Pro/Flash 加入 Copilot 模型选择器（保留 Copilot agent mode/tool calling/Skills/MCP 由 DeepSeek 驱动）；dsh.so：DSH Plugin Trust & Discovery Registry（15,009 install-tested L4，8,610 run-tested L5；security scan 2026-09-22）；deepseekplugin.cn：DSH 插件目录（dsh-market 市场）；必装三件：dsh-market（可视化市场）/dsh-vision-toolkit（纯文本模型看图/OCR/还原 UI 补读图短板）/dsh-balance（余额实时+峰谷价错峰） |

## 判重基准
双键检索（相对 r224-r253 已落章节）：Dify（r252-A 记忆/r252-B RAG/r252-C 会话变量——多路召回+引用面独有）；n8n（r252-A RAG/r252-B 记忆/r252-C Retriever——agent-as-tool 面独有）；LangFlow（r252-B 调试/r252-C 组件——生产部署面独有）；Activepieces（r252-A builder/r252-B MCP/r252-C triggers——custom piece 开发面独有）；Make（r252-C filter——blueprint 面独有但内容中）；Pipedream（r252-B OAuth/r252-C sources——error/concurrency 面独有）；Anthropic（r251-C 预建 Skills API 集成——重叠>60%，增量=8 skills 上限/日期版本/Foundry 条件，合并风险高不落）；GitHub（r251 多次——生态增量合并备选）；OpenClaw（r251-C 身份/r252-B memory——skills 开发面独有）；DeepSeek（r252-B DSH 生态——信任分级/vision-toolkit 增量合并备选）。未选素材：Make blueprint/Pipedream error（单点弱，已留痕）；Anthropic 预建（重叠）；GitHub/DeepSeek（增量并入已落生态观察类，不单落）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify Multi-path Retrieval | 多知识库同时召回+Rerank+引用开关 | 工作流 | wb-execute-discipline |
| ② n8n AI Agent Tool | agent 作为 tool+Tool calling 内建 | 工作流 | wb-execute-discipline |
| ③ LangFlow 生产部署 | headless runtime+K8s 最低配+lfx 部署控制 | 工作流 | wb-execute-discipline |
| ④ Activepieces 自定义 piece | TS 开发+.tgz 安装+AP_DEV_PIECES | 工具 | wb-execute-discipline |
| ⑤ OpenClaw skills 开发 | frontmatter+clawhub 三命令+VirusTotal | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
