# r245-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（工作流编排/变量/条件面） | ✓ | Variable Aggregator（汇聚互斥分支 If/Else Question Classifier 为单一输出——下游只定义一次处理避免每分支重复下游节点）；Human Input Node（人工介入：表单显示用户 query+LLM 分析，comment 输入变输出变量供下游；三决策按钮 Confirm/Regenerate/Forward 各映射分支；Timeout 3 天无响应自动 Forward）；系统变量（sys.workflow_run_id 记录运行状态执行日志/sys.timestamp 每次执行开始/sys.conversation_id 会话分组）；Code Node（Python/JS 双语言 def main(input)->dict 沙箱运行）；错误处理建议（If/Else 用于业务条件；LLM/HTTP/Code/Tool 失败用内置 retry/default-value/fail-branch） |
| 2 | n8n（AI Agent/LangChain 面） | ✓ | LangChain 节点已原生并入 n8n AI 套件（不再是单 LangChain 节点，功能分散多个 AI 节点：聊天模型/向量存储/文档加载器——搜索 AI 类别）；Agent 记忆分层（Postgres/Redis Chat Memory 存对话历史时序；向量存储 Pinecone/Weaviate/Qdrant 存语义/情节记忆相似检索——长期记忆用外部向量库）；cache-first RAG（LangCache Redis 向量库+OpenAI embeddings 客服场景快+省钱）；模板模式（Retrieve Parsed Content→Default Data Loader→Embeddings→Insert vectorStoreInMemory 原型用内存 store 上线换 DB） |
| 3 | LangFlow（组件/模板面） | ✓ | 预构建模板（RAG/CSV Agent/总结/市场研究/会议准备模板起步；新 workspace 默认 Starter Project 文件夹）；Agentics bundle（aMap 逐行填列/aReduce 多行折叠一行/aGenerate 按 schema 生成合成行——LLM 转换表格数据）；CSV Agent pattern（Chat Input/Output+LangChain CSV Agent LLM 推理 CSV 文件）；组件三分类（通用 输入输出数据存储+专门 代理语言模型 embedding）；grouped components 存为 reusable custom components；flow import/export JSON 完整资产 |
| 4 | Activepieces（AI Agent/MCP 面） | ✓ | MCP Server 集成（项目 Settings 启用 MCP Server 工具类别白名单 Server URL；Claude/Cursor 可运行你建的 flow create_invoice/find_customer/post_message；agent 也可用外部 MCP servers）；AI-first 设计（agent 自选工具所有已连接 app+指到的 MCP server；Approval where it counts 碰钱步骤设门禁）；AI SDK（内置 AI 工具/逻辑直接进 workflow）；Tables（data every flow and agent can read and write）；认证 tokens 留在模型外；data masking 敏感细节不出现在日志 |
| 5 | Make（HTTP/Webhook 面） | ✓ | HTTP v4（新版本简化设置更安全 keychain 存储原生 pagination——legacy v3 区分）；Webhook 响应（默认 200/Accepted；Webhook response module 定制；router 按请求参数分路径）；webhook 只能放 scenario 开头 instant trigger；Redetermine data structure 自动定数据结构；Meta webhook 验证陷阱（返回 ONLY raw hub.challenge 字符串无引号无 JSON wrapper，header text/plain，3 秒内响应超 meta 3 秒限制超时）；Content-Type 对应（text/plain/text/html/application/json/application/xml） |
| 6 | Pipedream（代码步骤/props 面） | ✓ | Props 抽象（code steps 接受 props 提高复用性——builder 填参数不改代码；只支持 Node.js code steps Python/Bash/Go 无此功能）；Data Store 作 prop（$.service.db 或 dataStore prop this.dataStore.get/set JSON-serializable 值；run()/hooks/methods 读写范围）；Step Exports（步骤输出供下游引用）；Python code step 结构（def handler(pd:"pipedream") pd.steps["trigger"]["context"]["id"]） |
| 7 | Anthropic（Claude Code 模型选择面） | ✓ | 模型分级选型（Haiku 机械任务查找/变量重命名 Low effort；Sonnet 默认写函数/测试/多文件编辑 Medium 速度快；Opus 架构设计/调试失败测试 High；Fable 5 最难题跨切重构/并发 bug/昂贵迁移 $10/$50 per M）；选型信号（Claude 有全部相关 context 明确试过仍错→升级模型；跳文件/没跑测试/中途放弃重构→不是模型问题是执行问题别升级）；降级（先 Haiku 快模型实现→测试→性能达标→降 effort 或降模型）；effort 调整（先默认 effort 按工作类型调整体偏好不逐任务调） |
| 8 | skills.sh（优秀技能/分类面） | ✓ | Brainstorming (obra/superpowers) 147.7K installs（skills.sh trending 数据最火技能包——superpowers 系列）；搜索结果大量职场技能类（resume skills）非生态技能，有效增量弱 |
| 9 | OpenClaw（工具/技能开发面） | ✓ | Skill Workshop（OpenClaw 治理路径创建/更新自有生成技能——proposal pending draft+content+target binding+scanner state+hashes+rollback metadata 应用后才变 live skill；自动背景学习+每周 collection review 直接编辑不建 proposal）；Skill 命名（SKILL.md frontmatter 定义非目录路径；skills/ 文件夹最高优先级 override 一切）；技能结构（SKILL.md instructions 必需+tools/ scripts 可选；TypeScript 模块暴露工具 Name/Description/Parameters JSON Schema/Handler async）；验证（openclaw tools list 检查加载 tool.json 有效 JSON） |
| 10 | GitHub（生态面） | ✓ | paperclipai/paperclip（今日 #1 open-source app 管理工作中的 agents）；vectorize-io/hindsight（Agent Memory That Learns Python）；dream-num/univer（Office Harness for AI Agents Spreadsheets/Docs/Slides/Canvas/Relational Tables/PDF 一个 runtime）；awesome-n8n-templates 25,589★（280+ 免费 n8n 模板最大开源模板集）；n8n-io/n8n 206,047★（fair-code workflow automation native AI 400+ integrations）；cherry-studio 52,159★（AI productivity studio 智能聊天/autonomous agents/300+ assistants）；ai-agent-book 51,071★（《深入理解 AI Agent：设计原理与工程实践》李博杰 开源主仓库 全书正文/PDF/按章代码） |

## 判重基准
双键检索（相对 r244 三批已落章节）：Dify（r244-A 落四形态发布/r244-C 落检索——"Variable Aggregator+Human Input 人工介入"独有增量新面）；n8n（r244-A 落 parser/r244-B 落 webhook/r244-C 落 Code Node——"LangChain 并入 AI 套件+记忆分层+cache-first RAG"独有增量新面）；LangFlow（r244-B 落 API 流式/r244-C 落 memory——"Agentics bundle 表格 LLM 操作"独有增量新面）；Activepieces（r244-B 落模板/r244-C 落部署——"MCP 双向+类别白名单"独有增量深化，本轮未选）；Make（r244-A 落 AI Toolkit/r244-B 落 Data Store——"HTTP v4 原生分页+验证陷阱"独有增量新面，本轮未选）；Pipedream（r244-A 落代码面/r244-C 落触发器——"props 复用+datastore prop"独有增量深化，本轮未选）；Anthropic（r244-A 落动态模型路由/r244-B 落工具合并/r244-C 落 caching——"模型分级+升级信号+先轻后重"独有增量深化）；skills.sh（r244-B 落 Skill Packs/r244-C 落 CLI——superpowers 147.7K 生态数据增量弱暂缓）；openclaw（r244-B 落 session hooks/r244-C 落网关——"Skill Workshop proposal+rollback"独有增量新面）；GitHub（r244-C 落自进化 Context DB——"hindsight 记忆学习+univer office harness"独有增量深化）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify Variable Aggregator+Human Input | 互斥分支汇聚单输出；人工介入三按钮+超时自动转发 | 工作流 | wb-execute-discipline |
| ② n8n LangChain 并入+记忆分层 | AI 套件分散节点；Chat Memory 时序 vs 向量语义 | 工作流/工具 | wb-execute-discipline |
| ③ LangFlow Agentics bundle | aMap/aReduce/aGenerate 表格 LLM 操作 | 工具 | wb-execute-discipline |
| ④ Claude 模型分级+升级信号 | Haiku/Sonnet/Opus/Fable 分级；有 context 试过仍错才升级 | 模型/工作流 | wb-execute-discipline |
| ⑤ OpenClaw Skill Workshop | proposal→apply 变 live+rollback metadata | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
