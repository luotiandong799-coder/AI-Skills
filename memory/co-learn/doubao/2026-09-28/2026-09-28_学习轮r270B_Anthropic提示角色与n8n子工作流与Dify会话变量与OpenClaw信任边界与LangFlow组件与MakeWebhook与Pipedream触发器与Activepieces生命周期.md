# r270B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r266-r270A 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（变量/上下文面） | ✓ | **Conversation Variables**（Chatflow 短期记忆单元——跨轮保留重要细节；同 conversation_id 内持久；状态会话/用户个性化/状态化工作流）；**Variable Assigner 节点**（管理持久化 conversation variables——写会话变量；与 workflow 变量不同：workflow 每次执行重置，conversation 跨轮持久）；**变量作用域表**（Input 单次运行不可变/Output 单次运行不可变/Conversation 会话级可变跨轮读写/Session 会话持续时间持久）；**系统变量**（sys.query 初始输入/sys.files 上传图片/sys.dialogue_count 轮数）；**LLM Memory**（节点级跨 LLM 调用保持——USER 模板可自定义；不跨对话持久）；**OpenAI Memory 模拟** |
| 2 | n8n（子工作流/工具面） | ✓ | **Call n8n Workflow Tool 节点**（任意 n8n workflow 打包成 agent 可调工具——子工作流独立 trigger/logic/output，父 agent 传输入收结构化结果）；**sub-workflows vs AI 节点**（执行路径可预测/跨 workflow 复用同一 agent 逻辑→子工作流更清晰）；**Execute Workflow 五阶段路由**（Initialise CONFIG 默认集中/Normalise 合并默认+去 null 字节/模型特化处理/路由）；**Manager Agent 模式**（评估输入分派专用子 agent——各带 role/memory/model）；**Sub-agents**（n8n Agents Add agent 选已发布 agent——When should this agent be used? 分派条件描述）；**Thinking Space 模式**（空子工作流 scratchpad——多次 Tool Workflow 调各唯一命名） |
| 3 | LangFlow（组件构建/前端面） | ✓ | **组件代码接口**（code 决定可视化配置选项+验证输入；name 可选默认类名；定义 inputs/outputs/method——method 名必须匹配 outputs 列表 method 字段）；**发现机制**（__init__.py 注册导出入口）；**Bundle 贡献**（frontend 图标三文件）；**PyPI 扩展**（python -m build+twine upload+pip install lfx-my-extension——服务器启动发现，palette 出现无需配置）；**Langflow Assistant**（提示生成自定义组件——input/output/timeout+error handling/typed methods；模型驱动）；**重建**（make install_frontend/build_frontend/install_backend）；**Embedded chat widget**（内嵌聊天样式配置） |
| 4 | Activepieces（触发器生命周期面） | ✓ | **Trigger 定义三字段**（Display Name UI 名/Description UI 说明/Technique polling 或 webhook）；**Polling 配置**（TriggerStrategy.POLLING；onEnable 初始化状态 store.put('lastId', null)；onDisable 清理；test 返回 []）；**Webhook 生命周期**（On Enable context.webhookUrl HTTP 注册+store webhook Id；On Handshake 挑战握手返回正确响应）；**app 集成**（注册唯一 webhook 启用/unregister 禁用；payload 按 per-webhook shared secret X-SP-Secret 验证）；**Schedule**（Core 菜单表达式 0 0 * * *） |
| 5 | Make（Webhook/响应面） | ✓ | **Custom Webhook 模块**（唯一 webhook URL 第三方调发数据——每 scenario 独立不可共用；即时触发器 vs scheduled 轮询）；**Webhook Response 模块**（定制响应两字段 Status+Body；2xx/3xx/4xx 状态码；配合 JSON 模块+headers 指定）；**响应时效**（Response 须放 scenario 末尾 40 秒内到达否则调用方超时）；**Webhook-triggered AI agent**（第三方发数据→agent 回 webhook） |
| 6 | Pipedream（触发器/工作流面） | ✓ | **HTTP 触发器 event 属性**（body/client_ip/headers/method/path/query/url）；**Connect triggers deploy**（client.triggers.deploy({externalUserId, id, webhook_url})——返回 triggerId+endpoint_url）；**webhook_url 投递**（deploy 带 webhook_url 时 POST 投递；trigger 级优先 project 级）；**project-level webhook**（默认 URL 所有 triggers）；**HTTP Response 配置**（Full HTTP Request/Return custom response）；**REST subscriptions**（POST /subscriptions?emitter_id=&event_name=&listener_id=）；**HTTP/Webhook action**（Postman-like GUI 构建请求） |
| 7 | Anthropic（提示最佳实践面） | ✓ | **角色设定**（system prompt 给 Claude 角色聚焦行为语气——一句就有效；role prompting expert persona；**别过度约束角色**——"helpful assistant" 常优于"world-renowned expert 只会术语"）；**system=behavior/user=task**（规则角色放 system，任务特定指令放 user）；**推荐结构**（Task description→Dynamic content→Detailed instructions→Examples→Repeat critical instructions）；**task contract 六问**（Input/Output/Rules/Context/Failure behavior/Evaluation）；**超具体角色**（"你有 N 年经验的非常具体角色，亲历过特定失败模式，用指定框架思考"）；**minimum effective dose** |
| 8 | deeplearning.ai（函数调用课程面） | ✓ | **Building Systems with ChatGPT API（1h，Isa Fulford+Andrew Ng）**（Python 与 completions 交互——分类查询/eval 安全/chain-of-thought 多步推理）；**Function-calling and data extraction with LLMs（1h9m，Nexusflow）**（what is function calling 9m/variations 12m/external tools 5m/Structured Extraction）；**Reasoning with o1（1h44m，OpenAI）**；**Building Your Own Database Agent**（自然语言查 SQL+function calling+code interpreter）；**function calling 本质**（声明工具 upfront 返回结构化 JSON 而非自由文本；Responses API 统一） |
| 9 | GitHub（agent 技能框架面） | ✓ | **Agent Skills 生态**（283K skills 跨 27+ 平台；开放规范跨 Copilot/Claude Code/Cursor/Codex/Gemini CLI——build once deploy everywhere）；**addyosmani/agent-skills（26k→77k→97k★）**（production-grade 工程技能约束走 SDLC：defining/planning/building/verifying/reviewing；25 技能；70+ agents；单命令安装）；**GitSkills 数据集**（3,797,117 SKILL.md 282,200 仓库 2026-07——1,877,981 唯一内容）；**gh skill 命令**（GitHub CLI 2026-04 单命令安装）；**OpenAI Skills**（Codex 官方目录 ~22k★；Symphony 规范）；**安全 Agents 趋势**（strix/shannon 125k★；记忆 210k★；headroom 66k★）；**OpenCode（~183k★）**（75+ providers/LSP/Tab-switchable agents/SKILL.md）；**Context Engineering Skills（9k★）**（13+ 技能北大引用） |
| 10 | OpenClaw（安全/治理面） | ✓ | **默认安全**（DM Policy 默认 pairing——未知发送者配对流程+过期码；Exec Security 默认 deny+ask: on-miss）；**信任边界**（每 gateway 一个——单 operator 或互信团队；非敌对多租户边界；混合信任拆边界 separate gateway+credentials 最好独立 OS 用户）；**Gateway vs Node**（Gateway=控制面+策略面 auth/tool policy/routing；Node=远程执行面 commands/device；配对后 node actions=trusted operator actions）；**secure by default**（shell/browser/file_write 默认禁用；API keys 永不记录；敏感配置状态打码）；**网络控制**（出站按域名限制；rate limiting；audit logging 每调用记录）；**allow-list 依赖注册表**（限制批准注册表+记录安装）；**一切读取视为不可信输入**（网页/邮件/消息可带 prompt-injection——action-level policy 而非 prompt discipline 作为控制） |

## 判重（双键检索结果）
- Dify 变量：库内已落 §上下文工程/§RAG 检索——Conversation Variables 会话级持久+Variable Assigner+变量作用域表+系统变量为独有增量 ≥40% → 落地
- n8n 子工作流：库内已落 §AI agent/§多agent——Call n8n Workflow Tool+Execute Workflow 五阶段+Manager Agent+Thinking Space 为独有增量 ≥50% → 落地
- LangFlow 组件：库内已落 §custom components API（r268B）——组件代码接口+发现机制+Bundle 图标+PyPI 扩展+Assistant 生成为独有增量 ≥50% → 落地
- Activepieces 触发器：库内已落 §触发器三技术（r269B）——onEnable store/test 函数+shared secret 验证+Schedule 为独有增量 ≥40% → 落地（合并增量）
- Make Webhook：库内已落 §Webhook 端点化/§HTTP——Custom Webhook 唯一 URL+Response Status/Body+40 秒时效为独有增量 ≥40% → 落地
- Pipedream 触发器：库内已落 §sources/调度——event 属性表+Connect deploy+webhook_url 层级+REST subscriptions 为独有增量 ≥40% → 落地
- Anthropic 提示最佳实践：库内已落 §提示工程/§输出校验——角色设定+推荐结构+task contract 六问+别过度约束为独有增量 ≥40% → 落地
- deeplearning.ai 函数调用：并入记录（课程情报）
- GitHub agent 技能框架：并入记录（GitSkills 数据集/gh skill/OpenCode 生态情报）
- OpenClaw 安全治理：库内已落 §Agent 安全纵深/§工具面安全——信任边界+Gateway/Node 分离+secure by default+一切读取不可信为独有增量 ≥50% → 落地

## 独点落地（8 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r270B-1 | wb-execute-discipline | 3.27.0+ | Anthropic 提示角色与推荐结构（增量合并 §提示工程） | 工具 |
| r270B-2 | wb-execute-discipline | 3.27.0+ | n8n 子工作流工具与 Manager Agent（增量合并 §多agent） | 工作流 |
| r270B-3 | wb-execute-discipline | 3.27.0+ | Dify 会话变量与 Variable Assigner | 工作流 |
| r270B-4 | wb-execute-discipline | 3.27.0+ | OpenClaw 信任边界与默认安全（增量合并 §Agent 安全纵深） | 可复用 Skill |
| r270B-5 | wb-execute-discipline | 3.27.0+ | LangFlow 组件构建与发现机制 | 可复用 Skill |
| r270B-6 | wb-execute-discipline | 3.27.0+ | Make Webhook 响应与 40 秒时效 | 工作流 |
| r270B-7 | wb-execute-discipline | 3.27.0+ | Pipedream 触发器部署与事件属性 | 工作流 |
| r270B-8 | wb-execute-discipline | 3.27.0+ | Activepieces 触发器生命周期（增量合并 §触发器） | 工作流 |

## 复核
八独点均有当日实拉来源；均为增量合并或新面落地；并入记录：deeplearning.ai 函数调用课程/GitHub agent 技能生态。垃圾：本轮未产生临时文件。
