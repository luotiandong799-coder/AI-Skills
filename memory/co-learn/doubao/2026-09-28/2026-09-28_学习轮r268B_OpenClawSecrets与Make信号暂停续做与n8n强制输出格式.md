# r268B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r268A 及 r266/r267 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（编排面） | ✓ | **Iteration/Loop 节点**（迭代=对数组每项执行同样步骤直到全部输出；Loop=直到条件满足）；**Loop 跨迭代传信息**（Deep Research 六变量跟踪：findings/executed_querys/current_loop/visited_urls/image_urls/knowledge_gaps——防止查询重复/来源追踪/知识缺口识别）；**Context Variables**（注入外部知识保留来源归属——{{knowledge_retrieval.result}} 自动追踪 citations 用户可见来源）；**Start 节点两种互斥**（User Input/Trigger 不能同画布；API/定时/Webhook/插件事件启动）；**Workflows as Tools**（Parameter Extractor）；**代码执行节点**（Python/JS 数据处理，function 返回 dict 声明 Output Variables）；**Agentic RAG 框架**（Agent Node 集中决策引擎：意图分析+工具编排+源选择+重试逻辑） |
| 2 | n8n（AI agent 面） | ✓ | **Tools AI Agent 节点**（Take from previous node chatInput / Define below；**Require Specific Output Format 强制输出格式开关**）；**Nodes as tools 新特性**（HTTP Request tool+Telegram node tool——LangChain Agent 决定何时用哪个工具）；**MCP Client**（MCP HTTP API credential——Brave Search MCP；MCP Trigger）；**Memory Buffer**（session memory）；**manager agent with sub-agent tools**；**LangChain Code node**（自托管专属——完全可定制提示词减少保留 tool-calling 功能的 token 消耗）；**RAG+Cohere reranking**（Gemini 2.5+Pinecone+Postgres Memory） |
| 3 | LangFlow（组件/API 面） | ✓ | **Custom components**（Python class 继承 Component；类级属性标识；input/output lists 定数据流）；**API**（POST /v1/custom_component 从代码构建组件；/update；/validate/code 验证 Python snippet；flow_id/api_key 嵌入权限）；**Bundles**（第三方集成打包——CometAPI/DataStax Astra DB Graph/Graph RAG/Agentics/Notion）；**Workflow API (Beta)**（组件标识符 dot notation {component_id}.{parameter_name}——inputs 对象覆盖组件参数） |
| 4 | Activepieces（数据/代码面） | ✓ | **Tables for Sync State**（存 cursors/last-seen timestamps/per-record status——reruns 可 resume、retries 只针对失败项、sync history 排障可查询）；**Field Mapping And Transforms**（HTTP/code steps/内置数据处理 map fields/normalize formats/merge records——写 CRM/DB 保持 identifiers 一致）；**架构**（PostgreSQL TypeORM 存元信息+File Storage 中转）；**MCP flows**（Airtable MCP：AI 起草+自动发送+结果回写） |
| 5 | Make（AI agents 面） | ✓ | **五 agent 模式扩展**（Routing agent 条件树不可管理时动态选 workflow/Qualifier agent lead scoring 申请筛选 内容审核/Orchestrator 协调多工具多 agent）；**AI Sub-Agents（新）**（orchestrator 实时调 specialist 按请求需求而非固定路径；每 agent 自己 tools/system prompt/job；逐个测试优化再插回）；**wait-resume-complete 模式**（首操作建状态暂停等信号——approval/payment/文档上传；信号再触发检索 prior record 交 agent 续做全连续性）；**multi-model orchestration**（单 scenario 分步路由不同模型——分类用快速廉价模型/起草用重模型；测 latency/cost/capability 谱系；不重建架构不绑定单 provider）；**透明度**（visual canvas 可见工具调用/推理/需人监督点） |
| 6 | Pipedream（sources/组件面） | ✓ | **组件能力**（deploy 时 props 收输入；触发 HTTP/timers/cron/manual；emit events；内置 key-value store；内置 deduping 策略）；**deploy() hook**（source 部署时自动创建 webhook subscriptions；可跑任意 Node.js）；**pd dev**（CLI 开发模式 watch 本地变化自动更新）；**components 组织**（每 app /sources /actions 子目录；每组件独立子文件夹 slugified 名）；**event sources**（run as separate resources——同一 source 触发多个 workflow）；**registry**（source-available 注册表+PR 贡献）；**10,000+ prebuilt tools** |
| 7 | Anthropic（Agent Skills 规范面） | ✓ | **name 规范**（≤64 字符；仅小写字母数字连字符；不以连字符开头结尾；无连续连字符；匹配父目录名）；**description 上限 1024**；**多技能组合策略**（任务多文档/域时组合——Excel+PPT/Word+PDF/自定义域+文档生成；**避免包含未用 Skills 影响性能**）；**skills 三类**（Foundational/Partner/Community）；**评估先行**（代表性任务观察 struggle 处再建）；**规模结构化**（SKILL.md 臃肿拆多文件引用；互斥/少共用 context 分开路径降 token）；**分层选择**（prompt caching 稳定指令/长参考；tools/scripts 确定性操作；extended thinking 只给真正困难推理）；**scripts 不进 context**（200 行脚本代码从不进上下文只有输出——排序/解析/表单验证/数学；自包含+依赖文档+帮助性错误消息）；**description 最重要**（唯一在加载前读；结构=[做什么]+[何时用]+[关键能力]）；**清单**（无 obvious 废话/渐进披露/SKILL.md<500 行/config 外置/env 文档化/目标约束非僵硬脚本） |
| 8 | deeplearning.ai（agentic AI 课程面） | ✓ | **Agentic AI 完整课**（Andrew Ng 9h19m/31 视频/8 graded——reflection/tool use/planning/multi-agent；集成数据库/API/网页搜索/代码执行；评估优化 performance metrics/error analysis/production）；**evaluations 模块**（evals/error analysis/component-level evaluations）；**新课程情报**（Building Adaptive AI Agents 2026-08-26/Evaluating AI Agents（Arize）2h36m 结构化评估/A2A Protocol 课程）；**DSPy（Databricks）**（DSPy+MLflow 调试优化 agentic apps）；**AutoGen 设计模式**（Sequential Chats/Reflection/Tool Use）；**Building AI Browser Agents**（AgentQ：MCTS+self-critique+DPO） |
| 9 | GitHub（Trending/agent 生态面） | ✓ | **Trending 2026-09-21**（anthropics/claude-code +419 当日——terminal agentic coding；FareedKhan-dev/train-llm-from-scratch 从零训练 walkthrough）；**周榜**（BuilderIO/agent-native 新 agentic apps 框架；stablyai/orca——ADE for fleet of parallel agents 桌面/移动/远程 runtime）；**2026-09-23 周榜**（addyosmani/agent-skills 98.4K stars +4,224 周增；Open-Dev-Society/OpenStock 18.4K；Panniantong/Agent-Reach 84.8K agent 读互联网）；**trendshift ai-agent**（RepoTagger AI issue triage 标 issue/flag dup/追踪自身成本；one-rulebook Claude Code+Codex 一规则本 hooks 强制）；**paperclipai/paperclip**（85,428 stars MIT TypeScript 管理工作 AI agents）；**排行榜**（browser-use 116k stars；herdr 40.8k Rust coding agents runtime；NanoBot 48.5k） |
| 10 | OpenClaw（secrets/环境面） | ✓ | **SecretRef 对象**（{source:"env",provider:"default",id:"VAR"}——所有受支持凭据字段；config env 块自身不解析 SecretRef/file:...）；**secrets providers 三源**（default env/file path ~/.openclaw/secrets.json mode json/singleValue/exec command vault-resolver——1Password/Vault/Bitwarden/sops 接入）；**环境优先级**（Process env>cwd .env>global ~/.openclaw/.env；**绝不覆盖已有值**）；**多环境 secret 文件**（config.yml 共享+secrets.dev/staging/prod.env；OPENCLAW_SECRETS_FILE 切换）；**config**（JSON5 ~/.openclaw/openclaw.json；缺省 safe defaults；owned writes 原子替换 rename）；**gateway**（bind 127.0.0.1/port 18789/token——localhost 优先/token 存 .env 不 commit） |

## 判重（双键检索结果）
- Dify 编排面：库内已饱和（§循环与迭代节点/§Iteration vs Loop/§变量全路径引用）——六变量 Deep Research 模式与 Context Variables 来源归属增量<40% → 并入记录
- n8n AI agent 面：库内已落 §Tools Agent 原生 tool-calling/§workflow as tool/§结构化输出解析器/§CodeAgent vs ToolCallingAgent——增量点=Require Specific Output Format 强制开关+Nodes as tools（HTTP Request tool）→ 增量≥40% 合并落地
- LangFlow 组件/API：库内已落 §Custom Components 脚手架/§Workflow API v2/§运行时 tweaks——dot notation 具体语法增量<40% → 并入记录
- Activepieces Tables Sync State：r268A 已并入 Tables 协调记录——cursor/per-record status 细节并入补充
- Make AI agents：库内已落 §Make AI Sub-Agents/§多 agent 四角色/§LLM 路由三模式/§模型路由——增量点=wait-resume-complete 业务信号暂停续做+场景内 multi-model 分步路由（区别于错误恢复/网关请求级路由）→ 增量≥40% 合并落地
- Pipedream sources：库内已落 §components 开发/进阶/§event source 部署 API（dedup+kv 已含）——deploy() hook 细节增量<40% → 并入记录
- Anthropic Skills 规范：库内已落 §64/1024/500 量化约束/§渐进披露/§脚本解决非踢皮球——组合策略+分层选择增量<40% → 并入记录
- OpenClaw secrets/环境：库内仅 Dify secrets 纪律，无 OpenClaw secrets 章节——SecretRef 三源机制/环境优先级/多环境文件切换为独有增量 ≥40% → 落地
- deeplearning.ai / GitHub Trending：并入记录

## 独点落地（3 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r268B-1 | wb-execute-discipline | 3.21.0+ | OpenClaw SecretRef 三源与环境优先级（增量合并 §Dify 秘密键纪律） | 可复用 Skill |
| r268B-2 | wb-execute-discipline | 3.21.0+ | Make wait-resume-complete 业务信号暂停续做 + 场景内 multi-model 分步路由（增量合并 §场景蓝图/§LLM 路由） | 工作流 |
| r268B-3 | wb-execute-discipline | 3.21.0+ | n8n Tools Agent 强制输出格式 + Nodes as tools（增量合并 §结构化输出/§workflow as tool） | 工作流 |

## 复核
三独点均有当日实拉来源；r268B-1 新面落地（OpenClaw secrets 无既有章节），r268B-2/3 增量合并落地（重叠>60% 但含≥40% 独有增量）；并入记录：Dify 六变量模式/Context Variables、LangFlow Workflow API dot notation、Pipedream deploy hook、Anthropic 组合策略、deeplearning.ai 课程情报、GitHub Trending 情报、Activepieces Sync State 补充。垃圾：本轮未产生临时文件。
