# r232-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（1.14 release/search） | ✓ | 实时协同编辑（并发编辑+在线状态+self-hosted 默认关）、Pull a Variable、强化沙箱+命令白名单、Metadata as Knowledge Filter |
| 2 | n8n（blog/search） | ✓ | agentic 三模式排序（确定性+单步 agent 是大多数正解）、AI Agent Tool 子 agent、生产可靠性记账五字段 |
| 3 | Langflow docs（assistant） | ✓ | Langflow Assistant 图结构感知、@组件.字段选择器、模型生成代码环境开关、本地模型 prompt 不出环境 |
| 4 | Activepieces（blog/resources/search） | ✓ | Flow as tool、Reusable pieces 参数化+版本化、Agents 可命名可复用 |
| 5 | Make（docs/search） | ✓ | 错误处理四指令 Ignore/Resume/Rollback/Commit、Break 给畸形响应、死信三落点 |
| 6 | Pipedream（blog/search） | ✓ | Workflow as function、MCP over SSE 每工具一端点、AI 脚手架自动搭结构 |
| 7 | Anthropic（hooks 文档/search） | ✓ | Hooks 五类型（command/HTTP/mcp_tool/prompt/agent）、PreToolUse 退出码 2 阻断、自改进技能循环 |
| 8 | 智谱 AgentMore（search） | ✓ | Skills 广场三类来源（推荐/Skillhub 7.4万+/开源社区）、智能体广场模板体验→看画布→一键复制 |
| 9 | 阿里虾小宝（search） | ✓ | 3.5 万+ 安全审核技能、双渠道安装（自然语言/CLI）、安全审核状态看板、阿里云官方 60+ 云产品 Skills |
| 10 | GitHub 生态（search） | ✓ | scientific-agent-skills（165 validated skills+数据库）、hindsight Agent Memory、CLI token 代理降 60-90% |

## 判重基准
双键检索（来源标识+概念词）：协同编辑/元数据权限过滤、agentic 三模式/可靠性记账、错误四指令/死信、hooks 五类型/退出码/自改进循环——均无同类已有落地。Hooks 与用户偏好"hooks 类必然执行机制"部分重叠但补五类型+退出码+反射循环增量（≥40%）。

## 独点落地（4 个，全部真独点）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① 实时协同编辑+元数据过滤 | 同图并发编辑+在线可见性；元数据作 RAG 访问控制（先圈权限集再语义检索） | 工具/工作流 | wb-execute-discipline |
| ② Agentic 三模式+可靠性记账 | 确定性+单步 agent 是大多数正解；记账五字段 input/decision/model/cost/approval result | 工作流 | wb-execute-discipline |
| ③ 错误处理四指令+死信三落点 | Ignore/Resume/Rollback/Commit 按语义选；Break 给畸形输出；Sheet+Slack+DLT 三处可查 | 工作流 | wb-execute-discipline |
| ④ Hooks 五类型+退出码+自改进 | 确定性（command/HTTP/mcp_tool）vs 判断型（prompt/agent）；退出码 2 阻断；reflection→learnings 自改进循环 | 工具/可复用 Skill | wb-execute-discipline |

## 复核
- 无编造凑数：四独点均有当日实拉原文来源。
- 功能套件检查：wb-ponytail/wb-max-token-saver/wb-context-compressor 本次无新增独点归属；④ 与功能套件"hooks 类机制"偏好互补。
- 垃圾：未产生临时文件。
