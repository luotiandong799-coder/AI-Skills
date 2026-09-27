# r265B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站，查询词与 r265A 及历批全错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（MCP 双向发布面） | ✓ | **MCP 双向原生**（v1.6.0：MCP server 当工具导入/发布 app 暴露为 MCP server——service description 让外部 LLM 知道何时调用+parameter description 文档 Start 节点输入→发 server URL）；**mcp-server 插件**（Extension-type 把任意 app 变 MCP 工具，Cursor/Claude Desktop 直调）；**Endpoint 机制**（Extension 插件处理自定义 HTTP 请求+reverse calls：自定义 web 界面/OpenAI-compatible API/异步事件触发）；**server_code 16 字符 token 即访问凭证**（POST /mcp/server/<server_code>/mcp 无独立 API key）；**DSL 导出含 MCP server 依赖**（跨环境迁移：同 ID 添加 MCP server+完成 OAuth+URL 可达）；**A2A 插件**（AgentCard .well-known/agent.json+JSON-RPC 双向多 agent） |
| 2 | n8n（AI agent 工具调用面） | ✓ | **Tools Agent 节点**（工具=连接可视化，n8n 管执行循环：model 结构化请求→API 调用→回传）；**MCP 支持**（agent 连任意 MCP-compatible 工具 server）；**工具错误处理**（单条可视化执行 trace 显示哪个 tool 失败/为何/LLM 传了什么参数）；**工具网关模式**（Webhook 收 MCP tool 调用→Validate API key/JWT/MCP schema→Tool Registry 解析工具名到后端配置+权限 scope→LLM Intent Verification 参数安全合规→Rate Limit→执行）；**Microsoft Agent 365**（n8n agent 以团队成员身份进 Teams/Outlook/Word，@mention 调用） |
| 3 | LangFlow（知识库/向量面） | ✓ | **知识库=向量数据库**（存 embeddings；默认 Chroma 本地，可配 Chroma Cloud/OpenSearch/Postgres pgvector；与 memory bases 共享 DB Providers）；**Load Data 子流 vs Retriever 子流分离**（Load：读文件→chunk→embed→存，不每次 flow run 重灌——性能关键；Retriever 只检索）；**DB Providers**（Settings 配置）；**多向量检索**（1.11.0 lfx-nextplaid：ColBERT late interaction+ColPali 视觉文档检索零胶水）；**RAG 管线**（embed 查询→相似度检索→可选 rerank→Prompt Template→LLM→grounded 回答） |
| 4 | Activepieces（审批/HITL 面） | ✓ | **Human Approval Steps**（暂停 run、收集 reviewer 决策、按结果恢复 flow，captured inputs 传下游）；**To-Do step**（工作流暂停等人批/审）；**无座位审批**（approver 无需账号/seat）；**Role-Based Routing**（条件逻辑+Tables 查找映射 request type/cost-center/owner→正确 approver，assign tasks+escalation delays）；**Execution Logs**（step-level 记 inputs/outputs/timing/failure points）；**敏感连接审批**（sensitive connections 使用前需审批） |
| 5 | Make（webhook 响应面） | ✓ | **Webhook response 模块**（status/headers/body 定制；默认 200/Accepted）；**GET 场景双路径**（filter 前置→Match Found/Match Not Found 分响应）；**POST 响应**（确认收到/返回相关数据/按 scenario 结果发不同响应）；**Meta 验签实战**（hub.challenge 必须原样返回文本无引号无 JSON，header text/plain，3 秒内响应）；**异步模式**（webhook 立即响应→独立 HTTP 模块异步调 downstream 防超时）；**Custom webhook 唯一性**（每 scenario 各自 URL 不可复用） |
| 6 | Pipedream（code step 调试面） | ✓ | **6MB 载荷上限**（log()/step exports/原始事件合计→Function Payload Limit Exceeded）；**$.respond() 每路径都要响应**（webhook 触发 workflow 报 Error 先查此）；**console.log/error**（黑/红）；**依赖自动更新陷阱**（默认 npm/pypi 自动升最新→新版带 bug 即 Internal Error，应钉版本）；**Event History 全局失败视图**（filter by workflow/time）；**Data Store 建查找表**（姓名不精确匹配教训）+try/catch 1 秒重试 |
| 7 | Anthropic（skills authoring 量化面） | ✓ | **质量清单**（description 具体+含关键术语+写"做什么+何时用"；body<500 行；附加细节分文件；无时效敏感信息；术语一致；示例具体；引用一层深；渐进披露）；**三级加载**（L1 metadata 恒载 ~100 tokens/skill；L2 body 触发才载<500 行；L3 reference 按需）；**Freedom Levels 三档**（high 文本指令/medium 参数化脚本/low 确定性脚本）；**hooks 示例**（PreToolUse matcher Bash validate.sh once:true/PostToolUse Write|Edit lint.sh/Stop）；**约束**（name 64 字符小写数字连字符；description 1024；禁 emoji/Windows 路径/深层嵌套/保留词）；**测试**（should-not-trigger 3-5 个防误触发；held-out 40% 验证泛化；"描述先钉死，没别的修复比它更提升触发准确度"） |
| 8 | 阿里虾小宝（生态面） | ✓ | **虾小宝**（xiaxiaobao.cn：中国用户优化 AI Agent Skills 安全社区，3.5 万+ 安全审核技能，覆盖写作/自媒体/数据分析）；**阿里生态**（OpenClaw Skill 中心=ModelScope Skills 中心+虾小宝导航；JVS Claw 一键养虾自进化"万能 skill"——"没有这技能请搜索并创建"；JVS 套件 Claw/Crew/Mobile；阿里云"悟空"企业 AI 原生平台 ATH 事业群；DTClaw 专业虾上百 skills+熟虾模板；天猫龙虾版生意管家） |
| 9 | 智谱 AgentMore（平台面） | ✓ | **AgentMore**（智谱清言 AI 智能体协作平台 2026-05-25：多 Agent 协作+技能市场扩展+任务执行+工作流编排，多角色并行+工具调用；基础免费+Skills 生态部分收费）；**AutoGLM**（自主 50+ 步长步骤、跨 app、数十网站无人驾驶；GLM-PC 像人操作计算机）；**GLM-5**（744B MoE 40B active/context 202,752/out 131,072/DSA）；**TAC**（Token 架构能力=智能调用量×智能质量×经济转化效率）；2025 营收 7.24 亿/MaaS ARR 17 亿 |
| 10 | WaytoAGI（知识库面） | ✓ | **定位**（中文 AI 知识库+社区，900 万人/访问量超亿次/联动 180 所/上万篇免费内容）；**Claude Agent Skills 蓝皮书**（五篇二十章：Skill 是给普通人的礼物→Agent Team→自动进化收尾，WaytoAGI×黄叔）；**学习路径**（入门 AI 学习路径课程，李宏毅等）；**API 面**（llm.waytoagi.com/v1，Hermes Agent 接入 claude-sonnet-4-6）；**AI 编程课程**（trae 课程/金句卡片生成器）；**共创**（AI 春晚、离谱村短片） |

## 判重基准
双键检索：Dify MCP 双向（§2194 动作多入口/§1642 RAG-MCP 管"MCP 安全"——app→MCP server 发布流程+server_code 凭证+Endpoint 扩展+DSL 迁移依赖新面落）；n8n 工具网关（§6018 可观测/r265A 身份——网关五步管"工具调用入口治理"新面落）；LangFlow 知识库（§2239 policies 守卫工具管"自然语言规则"——向量库/Load 子流/DB Providers/多向量检索新面落）；Activepieces 审批（§510 HITL 三要素管"审批设计通用原则"——无座位审批/角色路由/sensitive connections 审批为平台实例增量≥40%，合并保留增量落）；Anthropic authoring 量化（§2221 内容结构纪律管"内容合格"——64/1024/500/100 tokens/三档自由/触发测试为量化增量≥40%，合并保留增量落）；Pipedream 调试（§6058 工具结果太大/§2732 Pipedream errors 管"错误处理"——6MB 载荷上限+钉版本为增量并入记录）；虾小宝/AgentMore/WaytoAGI（r256A 三平台已入/台账"转售"——规模数字+新面并入记录）。

## 独点落地（5 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r265B-1 | wb-execute-discipline | 3.20.0+ | Dify MCP 双向发布：app→MCP server 与 server_code 凭证 | 工具 |
| r265B-2 | wb-execute-discipline | 3.20.0+ | n8n 工具网关五步：收调→验证→注册表→意图校验→限流 | 工作流 |
| r265B-3 | wb-execute-discipline | 3.20.0+ | LangFlow 知识库 Load/Retriever 子流分离与 DB Providers | 工作流 |
| r265B-4 | wb-execute-discipline | 3.20.0+ | Activepieces 无座位审批与角色路由（合并 §510 增量） | 工作流 |
| r265B-5 | wb-execute-discipline | 3.20.0+ | Anthropic authoring 量化约束（合并 §2221 增量） | 可复用 Skill |

## 复核
五独点均有当日实拉来源（逐站 URL 见各站摘要）；r265B-1/2/3 新面，r265B-4/5 增量合并落地；备选并入记录不单独落地（Pipedream 调试/虾小宝/AgentMore/WaytoAGI/Make webhook）。垃圾：本轮未产生临时文件。
