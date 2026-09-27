# r248-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（插件/市场面） | ✓ | Marketplace 发布流程（PR 到 langgenius/dify-plugins；reviewer+自动化 12 检查；官方目录一键安装）；插件可 GitHub 仓库安装；脚手架调试模式；Dify Creator Center & Template Marketplace（创作者发布 workflow 模板 用户一键采用 PartnerStack affiliate 佣金）；插件类型（Tool/模型 provider/MCP 客户端）；案例（Cloudsway 智能搜索/Excel Analysis/ComfyUI 集成/OpenAI Tools Deep Research） |
| 2 | n8n（webhook 安全面） | ✓ | n8n 无内建 rate limiting（限流在反代层 Nginx limit_req/Caddy rate_limit 100-500 req/min 合理）；内置认证（Basic/Header/JWT/none——none 是默认=问题）；不验 payload 完整性/不防 replay；HMAC-SHA256 签名（共享 secret 绑定请求防篡改）+timing-safe comparison+raw body capture（n8n 解析 body 后 JSON 重序列化可能不匹配原签名 需原始 body）；分层（IP allowlisting+token/HMAC+rate limit 429+Retry-After）；多租户方案（每租户唯一 secret key+时间戳防 replay+加密凭证+隔离 execution）；防护流（Client→Webhook→Identity→Guard→Allowed?→Business Logic→200/429） |
| 3 | LangFlow（工具选择面） | ✓ | Tool Mode（任何组件可变成工具 加 Toolset port 连 Agent Tools port；Run Flow 组件把别的 flow 变工具）；工具类型（Search/Calculator/Python REPL/API calls/Custom Python）；Agent 类型（Zero-shot ReAct/Conversational/OpenAI Functions/Custom）；条件路由（agent 按 query 类型选工具）；生产 agent 失败主因（外部 API 超时/500→工具节点包裹错误处理）；function description 优化（name 动词开头/description 用途场景/parameters 类型描述） |
| 4 | Activepieces（MCP 客户端面） | ✓ | 280+ open source pieces 可作 MCP（Largest Open Source MCP Server）；单 URL 暴露所有已连接 piece（AI 一个连接跨所有 app 调 action）；配置 mcpServers URL；OAuth 首次浏览器认证；Settings→MCP Server 启用；接入 Claude Desktop/Cursor/Windsurf（mcp.json）；Embeddable MCP（用户 app 内点 Authorize 后端拿 token 跑该用户自动化 标准 OAuth）；案例（Apify/APITemplate.io/Claude MCP） |
| 5 | Make（HTTP 模块面） | ✓ | HTTP v4 新版（简化设置/更安全 keychain 存储/原生分页 native pagination；legacy 是 v3）；认证四型（API Key/Bearer Token OAuth2/Basic Auth Base64 自动/OAuth 2.0）；分页指令（pagination collection 根级 url/method/body/response；repeat directive 按 condition 重复+delay+limit；mergeWithParent Boolean）；Choose where to start（当前时刻/特定日期/特定 ID/第一条——只影响首 run 后续 run 跟踪上次变更）；Google APIs OAuth 2.0（选 oauth2 认证类型） |
| 6 | Pipedream（限流/并发面） | ✓ | Concurrency and Throttling 设置（limit 0-10000 事件/interval 秒分时）；HTTP 触发默认限流 ~10 QPS 平均=600 req/min bucket（429 超出 可申请提高）；并发控制（workers=并行事件 1 worker=串行顺序保证处理顺序；增多 workers 提升响应但撞 API 限流）；429 调用方 backoff；自动重试开关；简化 workflow 减少 steps；硬上限（HTTP body 512KB/event retention 7 天） |
| 7 | Anthropic（prompt caching 面） | ✓ | 两种启用（Automatic caching 顶层 cache_control 系统自动把 breakpoint 加到最后 cacheable block 随对话增长前移——适合多轮对话；Explicit breakpoints 手动在缓存块后放 cache_control——system prompt/tool list/长文档）；TTL 默认 5 分钟（从请求开始计时不是响应结束；stream 时间算进 TTL）；1h TTL 可选（writes 2x base vs 5min 1.25x）；计费（cache writes 125% base/reads 10% base）；常用（<5min 间隔）5min 免费刷新；1h 适合 agentic side-agent 超 5 分钟或长对话；静默 miss 监控（log cache_creation_input_tokens/cache_read_input_tokens）；前缀稳定纪律（稳定内容放前变化放后）；Claude Code ENABLE_PROMPT_CACHE 1h；70-90% 账单削减 |
| 8 | OpenClaw（本地模型面） | ✓ | openclaw onboard 装 llama.cpp plugin 选 Managed local server（显示 Gateway host/model/download size/backend 下载前验证真实 tool call 再改默认模型）；配置结构 models.providers.<id>（baseUrl/apiKey/api: openai-completions/timeoutSeconds/models[]）；模型条目字段（id/name/reasoning/input/cost{input,output,cacheRead,cacheWrite}/contextWindow/maxTokens）；后端选择（LiteLLM/OAI-proxy 自定义 proxy；MLX/vLLM/SGLang 高吞吐）；lean mode 兜底（models[].compat.supportsTools:false 完全禁工具）；推荐大 context ≥64k（qwen3-coder/glm-4.7）；NVIDIA agent-ready models |
| 9 | GitHub Actions（安全/secrets 面） | ✓ | 结构化数据不做 secret（JSON/XML/YAML blob 日志脱敏失败——精确匹配难；每个敏感值单独 secret）；触发安全（避免 pull_request_target；第三方 action pin 完整 40 字符 SHA——tag 可移动=两次 run 不同代码 SHA 不可变免疫 force-push；checkout 默认防 fork 不可信代码）；权限最小化（permissions: contents: read；不用 PAT 用 deploy keys/service account 只读）；secrets 经 env 传不用命令行参数（进程列表可见）；untrusted event data 经 env 不直入 run；OIDC 代替长驻静态 cloud key（repo/branch-scoped trust）；2026 新 Scoped secrets（绑定 repo/org/branch/environment/workflow identity/path；reusable workflows 无需 caller 显式传）；CodeQL 免费检查 workflow |
| 10 | WaytoAGI（社区教程面） | ✓ | 任务分解方法论（大任务→可管理子任务→设计每子任务执行方法→实施验证）；学习路径（GPTs/Agents→案例入门→进阶拆解；Workflow 和 Multiagent Flow 核心构成）；社区共学（晚 8 点直播回放/共学文档/智能纪要；OpenClaw 一键部署+百度千帆 7 款官方 Skills 调用；从会聊天到真干活；标准化 Skills 让 AI 成为数字员工）；Coze 工作流实战（开场白引导/消息卡片/触发器/发布 Bot；agent 跳入跳出条件交互；LM 工作流连线）；百炼流程（创建应用→API 凭证→函数计算搭站→引 AI 助手→加私有知识）；提示词六大策略 |

## 判重基准
双键检索（相对 r244-r247 已落章节）：Dify（r247-A 落检索/r247-C 落异常处理——"插件市场发布流程+审核 12 检查"独有增量新面）；n8n（r247-C 落记忆/r246-C 落错误——"webhook 分层认证 HMAC+raw body+反代限流"独有增量新面）；Anthropic（r247-C 落 subagents/r246-C 落压缩重声明——"prompt caching 计费纪律+TTL 选择+静默 miss 监控"独有增量新面）；GitHub（r247-B 落 workflow 编排/r247-C 落 Copilot review——"供应链硬化 SHA pin+env 传 secret+OIDC"独有增量新面）；LangFlow（r247-C 落 supervisor/r246-C 落 Run Flow——"Tool Mode 组件变工具+条件路由"独有增量深化）。未选素材：Activepieces 单 URL MCP（r247-C 落重试——"280+ pieces 单 URL+Embeddable MCP"独有增量 本轮未选）；Make HTTP v4 原生分页（r247-C 落 directives——"v4 简化+原生分页+认证四型"独有增量 未选）；Pipedream 限流并发（r247-C 落 code retry——"concurrency/throttling+600req/min bucket"独有增量 未选）；OpenClaw 本地模型（r247-C 落 compaction——"onboard 验证 tool call+supportsTools 兜底"独有增量 未选）；WaytoAGI 任务分解（r247-B 落六类 workflow——"拆自包含子任务+共学模式"独有增量 未选）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 插件市场发布 | PR 到官方仓库+12 审核检查；模板市场一键采用 | 工具/可复用 Skill | wb-execute-discipline |
| ② n8n webhook 分层安全 | HMAC+timing-safe+raw body+反代限流 | 工作流/工具 | wb-execute-discipline |
| ③ prompt caching 纪律 | 自动/显式 breakpoint；TTL 5min/1h；计费；静默 miss 监控 | 工作流/上下文管理 | wb-execute-discipline |
| ④ Actions 供应链硬化 | SHA pin+env 传 secret+OIDC+scoped secrets | 工作流/工具 | wb-execute-discipline |
| ⑤ Tool Mode 条件路由 | 组件变工具+按 query 类型选工具 | 工作流/工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
