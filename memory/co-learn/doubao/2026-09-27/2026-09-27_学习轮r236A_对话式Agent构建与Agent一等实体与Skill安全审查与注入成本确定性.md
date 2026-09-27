# r236-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（blog/marketplace/updates） | ✓ | New Agent（2026-08-27：chat-to-agent 对话建 agent 自动生成可复用 skills 保留上下文）；v1.16.1 Tool Multi-Select Input+Workflow Node Locator（run-log 错误→画布节点）+默认 OpenAI 插件 API 切 Responses 支持 GPT-5.6；v1.17.1 数据集限定 API 密钥；Human Input node（v1.13：暂停等人审+动态表单+推理文本+分支路由+超时 fallback） |
| 2 | n8n（blog/community 2026-09） | ✓ | n8n Agents 发布（2026-09-25：agent 一等实体一次定义处处用，区别于 AI Agent node）；Gateway credits（v2.36：6 模型+5 工具服务免账号开箱）；Assistant 建 agents/连 MCP；确定性步骤 vs AI 步骤（rule-based 更可靠便宜）；Amazon Bedrock AgentCore 社区节点（跨 session 记忆+浏览器+代码执行） |
| 3 | Langflow（1.11/1.12/1.13 release） | ✓ | 1.11 HITL checkpoints+A2A protocol（flow 发布为 agent 可调+调远程 A2A，默认关）+AG-UI streaming+NextPlaid 多向量检索（ColBERT late interaction+ColPali 视觉检索）；1.12 OpenTelemetry（plain OTLP 兼容 NewRelic/Instana）；1.13 RBAC+MCP server 部署 flow |
| 4 | Activepieces（changelog/releases） | ✓ | Agents 可复用/可对话/可放置+flow step 集成+audit logs；AI-ready pieces（tool search/AI metadata——MCP 连接的 agent 描述任务找 action 查 schema 运行）；0.90.0 Vertex AI+Form.io/Clay pieces+agent 项目管理+MCP 改进；765 integrations 一个统一 MCP server |
| 5 | Make（2026-09 help/whats-new/community） | ✓ | Make AI Agent (New) app（open beta：agents+工具+知识+chat 测试）；AI Sub-Agents（2026-09-01：专家作工具入 orchestrator 替代手动链式）；Library of AI Agents；Opus 5/Gemini 3.6 Flash 支持；GPT-6 Astra |
| 6 | Pipedream（changelog/homepage） | ✓ | Agent Builder（prompt/run/edit/deploy：意图理解+拉数据+代表用户行动）；托管认证（token/refresh/user-level permissions 抽象免 custom auth plumbing）；Git-based version control for workflow 逻辑 |
| 7 | Anthropic（Skills guide/Agent Skills overview） | ✓ | Skill 安全审查（unusual patterns 网络调用/文件访问/不符目的；外部 URL 内容含恶意指令风险；工具误用面）；多技能组合最佳实践（Excel+PPT/Word+PDF/领域+文档，避免未用技能影响性能）；prompt caching 改 skills 列表打破缓存；SDK container；规格（name≤64/禁 XML/禁保留词；description≤1024 非空） |
| 8 | skills.sh（docs/localskills/skillctl） | ✓ | 头部 skill 安装量（find-skills 1.8M/frontend-design 483.8K/vercel-react 440.6K/microsoft-foundry 357.5K/web-design-guidelines 356.2K）；skills CLI 开源（vercel-labs/agent-skills）；localskills.sh（install/publish/push/share+teams/SSO/SCIM/API tokens）；skillctl（manifest/lock/registry/adapters+sha256 content-addressable cache） |
| 9 | GitHub 生态（Trending/排行榜 2026-09） | ✓ | Tencent/WeKnora 28.9K（+5303 周）+Tencent/BrowserSkill 6.6K（+4553 给 agent 借浏览器）+addyosmani/agent-skills 98.4K（+4224）；stablyai/orca（ADE 并行 agent fleet）；BuilderIO/agent-native；claude-code 146K；AutoGPT 187K/langflow 155K 规模参照 |
| 10 | docs.openclaw.ai（skills/creating-skills/skill-workshop/custodian/clawhub） | ✓ | 技能注入成本确定性（base+每技能 ~97 字符线性）；2026.9.4 插件技能发现升级；Skill Workshop propose 模式（每次变更评审）；Custodian（read-only diagnose 推荐修复从不执行，显式批准才 doctor --fix，secret 值不出 logs）；clawhub skill publish（--slug/--changelog，跳过未变，新技能 1.0.0 后续自动 patch）；Skills vs Plugins 分界表 |

## 判重基准
双键检索：Dify（r235-A 已落 RAG 管线/r235-B 迭代错误，本条独有增量=chat-to-agent+错误定位+密钥限定）；n8n（r235-B 编排四拓扑/r235-C 结构化解析器，本条独有增量=agent 一等实体+gateway 免账号+确定性优先）；Anthropic（r235-A JIT 记忆/r235-C 托管，本条独有增量=Skill 安全审查三面+缓存稳定+规格）；OpenClaw（r235-B cron watch/r235-C Memory bases，本条独有增量=注入成本确定性+只诊断不执行+自动 patch 发布）；Activepieces（r235-C 托管 MCP，本条独有增量=AI-ready 描述任务检索 action+audit logs）；Langflow（r235-C Memory bases，本条未单独落地 A2A——并入后续轮）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 对话式构建三件套 | chat-to-agent 自动生成 skill；run-log 错误定位节点；数据集限定密钥；Human Input 人机交接节点 | 工作流 | wb-execute-discipline |
| ② n8n agent 一等实体 | 一次定义处处用；Gateway credits 免账号；确定性步骤优先于 AI | 工作流 | wb-execute-discipline |
| ③ Anthropic Skill 安全审查 | unusual patterns 三面；外部 URL 内容按注入处理；prompt caching 稳定 skills 列表；name/description 规格 | 可复用 Skill | wb-execute-discipline |
| ④ OpenClaw 注入成本与发布 | 每技能 ~97 字符注入税；Custodian 只诊断不执行；clawhub 自动 patch 发布；Skills/Plugins 分界 | 可复用 Skill | wb-execute-discipline |
| ⑤ Activepieces AI-ready 目录 | 描述任务→自动找 action→查 schema→运行；audit logs；765 app 一个 MCP server | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：wb-ponytail/wb-max-token-saver/wb-context-compressor 三件套无新增更优替代，无需增删。
- 垃圾：本轮未产生临时文件。
