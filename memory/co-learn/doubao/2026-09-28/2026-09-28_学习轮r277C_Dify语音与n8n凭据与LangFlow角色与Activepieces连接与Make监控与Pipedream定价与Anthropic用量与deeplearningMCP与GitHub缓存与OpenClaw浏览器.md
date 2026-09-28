# r277C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（语音对话） | OK | App Toolkit：Text to Speech（配语言/音色）+Speech to Text（配默认 STT 模型后 Features 面板才出现麦克风）；语音市场插件（ElevenLabs TTS/STT、Fish Audio TTS+voice cloning、Agora/TRTC Conversational AI 实时语音）；Whisper 自动；语言参数需匹配 ASR/LLM 格式 |
| 2 | n8n（凭据管理） | OK | External secrets：外部 vault 集中管多环境凭据，用时才加载；credential sharing=分享 template 不分享 connection（他项目用户自连账号）；credential overwrites=全局设用户不可见（OAuth Connect 按钮免暴露 client secret）；OAuth 自动刷新 token；多租户=tenant 凭据分存+动态按 tenant_id 加载+角色隔离 |
| 3 | LangFlow（RBAC/认证） | OK | 内置角色 viewer/developer/admin（permission slugs：flow:read、flow:write+execute 等）；/admin 超管页建用户/设权限/重置密码；roles API 建自定义角色（须 enforcement plugin 注册才生效）；external auth：JWT claim 映射 access level（默认 viewer）+DISABLE_API_KEYS_FOR_EXTERNAL_USERS 防 API key 绕过；安全文档明示：Langflow 自身不做租户隔离，多租户靠基础设施级 |
| 4 | Activepieces（连接/OAuth） | OK | Piece Auth refresh callback：token 取一次缓存服务端，注入 context.auth.access_token，到期前 15 分钟自动续（短寿命 token 钳半生命周期）；Embeddable MCP token 15 分钟过期用 refresh_token grant 续；预定义连接（platform admin 建全局连接+API Key，用户免重输凭据）；Project Variables 项目级复用（Editor/Admin 可 reveal 明文）；连接集中化减少漂移简化轮换 |
| 5 | Make（监控/通知） | OK | 通知 per user/per scenario 配置；scenario stop 默认开（mail+in-app）；Incomplete Executions 有 DLQ 逻辑才开否则噪音；Operations limit reached 给 owner；无错误处理时通知迅速变噪音；可接 Datadog/Better Stack/自定义 webhook 通知 |
| 6 | Pipedream（定价/配额） | OK | 1 credit=30s@256MB；Free=100 credits/天、3 workflows；Basic $29/mo=2000 credits/天；Advanced $79/mo=10000 credits/天；Business 定制；event sources 无限（各自限内）；付费不限量超了加收（可设 usage cap）；执行积分制区别于 Zapier task 制/Make operation 制 |
| 7 | Anthropic（用量/成本 API） | OK | Usage & Cost Admin API：/v1/organizations/cost_report（服务级成本，USD cent 十进制串）+usage_report（按分钟/小时/天桶，可拆 product/model/region）；Agent SDK cost-tracking：result message 含 total_cost_usd+usage dict 累计总量；每 step 只计费一次；parallel tool uses 同 ID 消息取其一；modelUsage 按模型分解（Haiku subagent vs Opus main）；缓存 token 定价与失败对话需计入 |
| 8 | deeplearning（MCP 课程） | OK | MCP: Build Rich-Context AI Apps with Anthropic：FastMCP 建本地 server（tools/resources/prompt templates）+MCP Inspector 测试+MCP client 动态连接+Anthropic 参考 servers（filesystem/fetch）+Claude Desktop 配置+远程部署；2 小时课 Python only；DataCamp Advanced MCP：sampling（server 把 prompt 交回客户端模型省 API key）+stream log/progress+跨 transport |
| 9 | GitHub Actions（缓存优化） | OK | 缓存限制：7 天未访问清除、repo 总 10GB、超限按最后访问时间驱逐；cache key=OS+包管理器+lockfile hash（勿用 commit SHA）；分层 restore keys+分离依赖/构建缓存+默认分支预热；setup-node cache:'npm'/setup-python cache:'pip'；npm ci 优于 install；命中省 60-80% 构建时间；Docker layer cache+Turborepo remote cache |
| 10 | OpenClaw（浏览器自动化） | OK | 双模式：managed browser（专用 Chrome/Edge 隔离 profile，Gateway 本地 loopback 控制）+extension relay（复用现有 Chrome）；内置 browser skill（Playwright 驱动，headless server 沙箱 Chromium 不碰个人浏览器）；browser-use 插件（导航/点击/填表/截图/提取）；Browser Relay（聊天内网页自动化，WhatsApp/Telegram/Discord）；Rust agent-browser CLI |

## 判重（双键检索，增量判定）
十站与库内既有锚点重叠>60% 的按增量合并落地：
- Dify 语音（库内语音锚点有限）→ 新面（App Toolkit TTS/STT+语音插件生态）
- n8n 凭据（r274B n8n 相关锚点）→ 增量=external secrets+credential sharing/overwrites 机制
- LangFlow RBAC（r269B LangFlow 权限锚点）→ 增量=角色 permission slugs+external auth 防绕过+租户隔离边界
- Activepieces 连接（r267 锚点）→ 增量=refresh callback 自动续期+预定义连接+Project Variables
- Make 监控（r275A Make 监控锚点）→ 增量=通知分级配置（stop/incomplete/limit）+噪音判据
- Pipedream 定价（无定价锚点）→ 新面
- Anthropic 用量 API（r274C 输出 tokens 锚点）→ 增量=Usage & Cost Admin API+SDK cost-tracking 语义
- deeplearning MCP（r274B MCP 锚点）→ 增量=FastMCP 课程+sampling+远程部署
- GitHub Actions 缓存（r276B Actions 锚点）→ 增量=缓存限制/驱逐策略+key 设计
- OpenClaw 浏览器（库内无浏览器自动化锚点）→ 新面

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 语音对话与 TTS/STT | 工具 |
| 2 | n8n 凭据管理与外部密钥 | 工具 |
| 3 | LangFlow RBAC 角色与外部认证 | 工具 |
| 4 | Activepieces 连接与 OAuth 自动续期 | 工具 |
| 5 | Make 监控与通知配置 | 工作流 |
| 6 | Pipedream 定价与配额 | 工具 |
| 7 | Anthropic 用量与成本 API | 工具 |
| 8 | deeplearning MCP 课程 | 可复用 Skill |
| 9 | GitHub Actions 缓存优化 | 工具 |
| 10 | OpenClaw 浏览器自动化 | 工具 |

## 复核
十独点均有当日实拉来源；均增量合并或新面；无并入未落地项。版本建议 3.49.0+。