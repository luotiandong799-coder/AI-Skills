# r251-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（HTTP Request 节点面） | ✓ | 认证类型（No Auth/API Key 三子型：Basic base64/Bearer/custom header）；HttpRequestNodeAuthorization 配置；多步 API 调用（Step1 POST auth 用 {{env.api_user}}/{{env.api_pass}}→Step2 GET 数据 fetch）；敏感 key 存 Dify environment variables 不硬编码 node config；Verify SSL certificate toggle；Dify API Bearer 令牌 |
| 2 | n8n（Schedule Trigger/时区面） | ✓ | Schedule Trigger 依赖时区（workflow timezone 优先，否则 instance timezone；self-host 默认 America/New_York；Cloud 检测 owner 时区 fallback GMT）；错时间排查（GENERIC_TIMEZONE env 全局设置；Cloud 设置实例时区）；三处时区源（self-host 读 TZ/GENERIC_TIMEZONE/workflow zone 三处，只修一处只修部分）；node Timezone 设置+Date & Time 节点显式同 zone 防 UTC bug；排期模式（0 8 * * 1-5 周末不跑；公共假日日历集成 booking 冲突检测） |
| 3 | LangFlow（Agent 组件面） | ✓ | Agent 组件=主要 agent actor（LLM 集成响应 chat/file；base LLM 自带工具+Tools 端口附加工具；任何 Langflow 组件可作工具含其他 Agent 和 MCP servers via MCP Tools 组件）；CodeAct Agent（Smolagents CodeAgent 迭代生成执行 Python 代码：写代码→沙箱解释器执行→输出决定下一步直到最终答案）；CUGA Agent（IBM 通用 agent 框架：break down tasks/plans/drive web browser/write custom code）；LangChain bundle 旧组件（CSV Agent allow_dangerous_code 安全；VectorStoreRouterAgent 建议换 Agent/SQL Database 组件）；aGenerate/aMap/aReduce（Agentics bundle：schema 合成数据/逐行自然语言转换/聚合）；RAG template（Parser 归一化 HTML→Markdown/Docling 转换→chunk→embeddings→pgvector/Pinecone/Chroma/Astra/Weaviate） |
| 4 | Activepieces（code piece/TS SDK 面） | ✓ | createAction 结构（name 全 piece 唯一不可改/auth/displayName/description/props/async run(context)）；propsValidation+zod 属性校验；Piece Auth（createPiece/createTrigger/createAction 的 auth 参数可数组但不多于一个 auth 属性；TypeScript SDK 扩展平台）；createCustomApiCallAction（baseUrl (auth)=> 自定义+authMapping 自定义 header）；MCP tools 参考（PIECE: pieceName/actionName/input/auth/continueOnFailure/retryOnFailure；CODE:…）；CSDN 实战（createPiece({name/displayName/actions/triggers}) 标准 TS 模块） |
| 5 | Make（scenario version/recovery 面） | ✓ | Version history（访问并恢复手动保存版本，保留 60 天）；Scenario recovery（所有 plan；编辑时自动保存 blueprint；浏览器崩溃/断连/误关 tab 恢复未保存更改）；Restore 注意（恢复版本不会自动保存——若未手动保存恢复会丢）；Latenode 版本控制最佳实践（编辑工作场景前先 snapshot：Duplicate/Clone→改名 [ARCHIVE] Workflow_Name_v1.0；每次 save/run 创建新版本可回滚） |
| 6 | Pipedream（triggers/dedupe 面） | ✓ | dedupe 策略 unique（缓存 100 个 emitted id；不在缓存发出并加入；FIFO 超 100 清除；RSS 常用）；id 属性（必须传 id 才能去重；不传自动生成则去重失效）；$emit()+dedupe strategy 自动去重；trigger events API（无 webhook 拉取最近事件）；emit_on_deploy 控制（历史事件部署时发出与否）；幂等键（Gmail Message ID 作 dedup key；raw_event_id+event_type 组合查重；$checkpoint dedup；persisted tweet IDs）；HTTP/cron/email triggers |
| 7 | Claude Code hooks（lifecycle 面） | ✓ | Hooks 事件全集（SessionStart/UserPromptSubmit/PreToolUse/PreToolUseFailure/PermissionRequest/PostToolUse/PostToolUseFailure/Notification/Stop；PreToolUse 可 block exit 2 或 JSON allow/deny/ask；PostToolUse exit 2 blocks turn；Stop 强制 Claude 继续）；PreToolUse matcher 按工具名（Bash/Edit/Write/Read/Glob/Grep/Agent/WebFetch/WebSearch/MCP tools）；Subagent 工具事件（PreToolUse/PostToolUse 同样触发主会话配置 hooks，input 带 agent_id/agent_type）；SDK hooks（Python+TS：PreToolUse block/modify 挡危险 shell/PostToolUse audit trail/PostToolUseFailure 处理工具错误）；hooks 配置 .claude/settings.json |
| 8 | OpenClaw（plugins registry/install 面） | ✓ | 安装源五形态（clawhub:<package>@version@beta / npm:<package> / git:github.com/<owner>/<repo>@<ref> / ./my-plugin 本地 / --link 链接）；记录 install source 元数据（updates 可解析同一 registry 包）；非交互安装需 --accept-capabilities 显式 flag（install/update/enable 都要）；ClawHub CLI（npm i -g；registry-authenticated publish/delete/undelete；CLAWHUB_DISABLE_TELEMETRY=1）；Node 22.22.3+/24.15+ 要求；skills search/install/update --all 平行命令 |
| 9 | GitHub Actions（reusable workflows 面） | ✓ | 三阶段使用 input/secret（called workflow 定义 inputs/secrets keywords→caller with: 传 inputs + secrets: 传 secrets→called 里 inputs/secrets context 用）；嵌套 reusable（secret 传给嵌套必须再 jobs.<job_id>.secrets 传）；inputs 类型（boolean/number/string 匹配）；输出返回 caller 后续 job 用；跨仓库 workflow 共享（uses: owner/repo/.github/workflows/file.yml@ref）；github 上下文永远关联 caller；called 自动获得 github.token/secrets.GITHUB_TOKEN；secrets 值被 redacted from logs |
| 10 | WaytoAGI（RAG 知识库问答面） | ✓ | 知识库问答三要素（AI 模型+提示词+知识库；模型=博学的人/提示词=让他干活的指令/知识库=工作手册含规则特殊情况）；提示词格式（设定角色+任务目标+上下文和背景信息+正面要求详细需求和细节性信息+负面要求限制和不需要的内容+回答格式）；飞书知识库问答（RAG 补新鲜知识；智能伙伴搭 FAQ 机器人）；RAG prompt 排障表（Mixed-topic→Query decomposition；Keyword-only→Hybrid rewriting；Hallucinated→Grounded generation [src:N]；Unsafe→Contrastive refusal；Unmeasurable→LLM-as-a-judge rubric） |

## 判重基准
双键检索（相对 r224-r250C+r251A 已落章节）：Dify（r251-A 兼容端点/r250-C 编排——HTTP 节点认证三子型+多步 API 认证-取数+key 存 env 为独有增量）；n8n（r251-A AI Assistant/r250-C 错误工作流——时区三源纪律 TZ/GENERIC_TIMEZONE/workflow zone 为独有新面，与定时记账判据互补不同面）；LangFlow（r251-A LangSmith/r250-C 嵌入——Agent 组件工具端口+CodeAct/CUGA 为独有新面）；版本恢复（r250-B n8n 版本管理——Make version history 60 天+scenario recovery+构建前 snapshot 最佳实践为独有增量跨平台）；GitHub Actions（r250-B caching——reusable workflows 三阶段 inputs/secrets+嵌套再传+跨仓库共享为独有新面）。未选素材：Claude Code hooks 事件全集（r249-A hooks 事件驱动已落，重叠>60%，事件表/subagent 传播/SDK 三件套增量约 40% 边缘不落）；OpenClaw 安装源（r239-C ClawHub 安装源五形态已落，--accept-capabilities 增量弱）；Pipedream dedupe（r244-B DataStore 去重用途已提及，unique 100 缓存机制增量中等）；WaytoAGI 三要素（r226-C RAG 提示词三层已落，重叠高）；RAG prompt 排障表（r240-C 检索排障顺序已落，切入面相近）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify HTTP 请求认证与凭据 | 认证三子型+多步 API+key 存 env | 工作流 | wb-execute-discipline |
| ② n8n 时区三源纪律 | TZ/GENERIC/workflow zone | 工作流 | wb-execute-discipline |
| ③ LangFlow Agent 组件与工具端口 | Agent actor+CodeAct/CUGA | 工具 | wb-execute-discipline |
| ④ 场景版本恢复与构建前 snapshot | 60 天历史+自动 blueprint+[ARCHIVE] | 工作流 | wb-execute-discipline |
| ⑤ GitHub Actions 可复用 workflow | 三阶段 inputs/secrets+嵌套 | 工作流 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
