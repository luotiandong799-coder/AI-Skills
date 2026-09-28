# r282C 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站；查询词与 r282A/B 二十词 + r281A/B/C 三十词 + r280 三十词 + r279 三十词 + r278 三十词错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（变量聚合节点） | OK | **Variable Aggregator（原 Variable Assigner）把互斥分支（If/Else、Question Classifier 只执行一路）输出收敛为单变量，下游只定义一次**；**类型约束：聚合变量必须同类型（配置时强制）**；输出=实际执行分支的值；List Operator（按属性过滤/排序 ASC/DESC/取前 N 项）；Variable Assigner（Chatflow only 写会话变量：overwrite/clear/set/算术/数组 append/extend/remove）；DeepResearch 案例：Assigner 用 append 累积 findings、IF-ELSE 检查 shouldContinue |
| 2 | n8n（webhook 响应模式） | OK | **四种响应模式：Immediately（200 + "Workflow started"，fire-and-forget）/ When Last Node Finishes（全流程执行后返回末节点输出+可配状态码）/ Using Respond to Webhook node（按 Respond 节点定义）/ Streaming response（实时流式返回）**；**streaming 隐含启用（仅 Response Mode=Using Respond to Webhook 时可用；Immediate 与 streaming 不可同用）**；测试 URL（/webhook-test/ 与生产 /webhook/ 分离）；认证（Basic/Header Auth）；Wait 节点 resume webhook suffix（多 Wait 节点唯一化） |
| 3 | LangFlow（组件目录体系） | OK | **组件分层：Core components（基础通用：Inputs/Outputs/Data，循环/解析）+ Bundles（第三方集成：LangChain bundle 文本分割器、Composio 聚合工具、Agentics）**；**自定义组件=Python 代码即工具（New Custom Component→Code 面板写 Python）**；**legacy 组件替换路径（Legacy banner 提示，Search by provider/service/name 找替换）**；Data Operations 组件（提取/过滤/编辑键值）；vector store 组件族（embedding 存储/相似度搜索/Graph RAG/OpenSearch） |
| 4 | Activepieces（控制流） | OK | **Router executor（表达式条件分支）+ Loop executor（遍历数组，顺序/并行）**；**ap_add_branch MCP 工具（给 router 加条件分支，插到 Otherwise 前）**；**Tables 内建存储（路由矩阵/区域映射/审批异常状态，多步共享进程状态）**；auto-retries（瞬态失败自动重试不中断下游）；custom pieces（TypeScript 自定义 pieces+HTTP 请求步+可复用模块接内部 API）；条件/循环/并行/延迟/重试协调多步（审批/升级/交接） |
| 5 | Make（data store 限制） | OK | **Data store=跨 scenario 持久数据共享（像 spreadsheet worksheet）**；**记录上限 512KB/条；大小按套餐（Core 1MB/store、Pro/Teams 10MB/store、Enterprise 自定义）**；**每 10k operations 配额：数据转移 5GB、数据存储 10MB、incomplete executions 10MB（2GB max）、webhook 队列 667（10k max）**；Searches 模块每 run 最多 3200 对象或 5MB；每模块 5MB/run 数据限制；API 限额另行适用 |
| 6 | Pipedream（triggers/event sources） | OK | **triggers=sources；两类部署：app-based event sources / native triggers**；**event sources 是独立于 workflow 运行的资源：一个 source 可触发多个 workflow；事件可经 API/SSE 被外部消费**；组件能力（props 输入、HTTP/timer/cron/manual 触发、emit 事件、内建 KV store 状态、内建 deduping 策略）；**timer-based polling sources（定时轮询+自动拉历史事件）**；四类触发：HTTP/Cron/Email/Event sources；Twitter 实时源（tweet/关注/点赞，SSE/REST 访问） |
| 7 | Anthropic（Claude Code subagents） | OK | **subagent 字段：name 唯一标识（hooks 收到 agent_type；文件名不必匹配；不能含 :）、model 可省略继承、permissionMode（default/acceptEdits/auto/dontAsk/bypassPermissions/plan）**；**深度限制（默认主 agent 下 3 层，设 1 禁止再 spawn）+并发限制（默认 20 个同时，超出拒绝 spawn）**；**deny 数组禁用特定 subagent（Agent(name) 格式）**；**工具限制（tools 字段：省略=继承所有，指定=只能用列出的→只读分析 agent 模式）**；**位置优先级五级：Managed settings（组织级 1）> --agents CLI（当前会话 2）> .claude/agents/（项目级 3）> ~/.claude/agents/（个人级 4）> Plugin agents（5）** |
| 8 | deeplearning（课程评估结构） | OK | 课程结构=分周（每周 Video 4-10min + Lecture Notes + **Graded Quiz 1h**）；评测=每课测验+编码挑战；**单一实数评估指标优于多指标（多指标难比较）**；幻觉减少=grounded retrieval 最佳；BloombergGPT 领域特定训练示例；Generative AI with LLMs 课程（week 1-2：instruction fine-tuning/multi-task/模型评估） |
| 9 | GitHub（agent 框架生态） | OK | **2026 agent 框架四层架构标准化（LAMP 时刻）**；**Agency Swarm 10k★ production-first：工具=Pydantic 模型全验证+类型安全+错误处理、显式通信图**；**harnesses.sh：75 harnesses 9 轴能力 schema（curated cross-vendor 目录）**；**OpenClaw 283k★、superpowers 113.5k★（技能框架无营销爆红）**；nanobot 48.6k★（超轻量自托管个人 agent：WebUI/tools/memory/MCP/多 agent/自动化）；CowAgent 47.1k★（super AI assistant & Agent Harness：规划/跑工具技能/自进化）；DeepSeek Harness "Everything is a Plugin"；hermes-agent 228k★（persistent 学习适应）；RAGFlow 2 万★（AI 原生数据库+RAG 端到端） |
| 10 | agentskills.io（技能目录生态） | OK | **技能=文件夹含 SKILL.md（最少 name+description 元数据+指令，可捆绑脚本/参考/模板）——open format 定义**；agentskills.io 社区目录（链接 Anthropic Skills/ClawHub）；**AgenticSkills 181+ 策展技能（Testing 17/AI-ML 16 按类）**；**Anthropic cybersecurity skills 754 技能 26 域（MITRE ATT&CK+NIST CSF 2.0 映射+Navigator layer）**；**agentskills.codes 19,296 技能分类（Coding 6,343/Productivity 1,216/Planning 786/Data 692）**；agentskills.me 492 技能（Claude Code/Cursor/OpenCode/Codex/Gemini CLI） |

## 判重（双键检索，增量判定）
- Dify 变量聚合（r273A 用过聚合）→ 聚合节点类型约束+List Operator+Assigner 数组操作为独有增量 → **增量合并**
- n8n webhook 响应（r279A 用过 webhook）→ 四响应模式+streaming 隐含启用+测试 URL 为新面 → **新面**
- LangFlow 组件（r272C/r280C 组件）→ Core vs Bundles 分层+自定义组件即工具+legacy 替换为独有增量 → **增量合并**
- Activepieces 控制流（r282A 用例/r282B 构建）→ Router/Loop executor+ap_add_branch+Tables 为新面 → **新面**
- Make data store（r268B 用过 data store）→ 配额限制+记录上限+searches 上限为新面 → **新面**
- Pipedream triggers（r274A 用过 triggers）→ sources 独立资源+单源多流+dedup+KV store 为新面 → **新面**
- Claude subagents（r269B 多代理）→ 深度/并发限制+权限模式+工具白名单+优先级五级为新面 → **新面**
- deeplearning 课程（r282A 认证体系）→ 周结构+分级测验+单一实数指标为独有增量 → **增量合并**
- GitHub agent 框架（r282A 周榜）→ 四层架构+Agency Swarm Pydantic+harnesses 目录为新面 → **新面**
- agentskills.io（r281B 目录）→ open format 定义+规模分类+安全域映射为独有增量 → **增量合并**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 变量聚合与列表操作 | 工具 |
| 2 | n8n webhook 响应模式 | 工具 |
| 3 | LangFlow 组件分层与自定义组件 | 工具 |
| 4 | Activepieces 控制流与进程状态 | 工作流 |
| 5 | Make data store 配额与限制 | 工具 |
| 6 | Pipedream sources 架构 | 工具 |
| 7 | Claude subagents 深度/并发/权限 | 可复用 Skill |
| 8 | 课程结构与评估方法论 | 工作流 |
| 9 | agent 框架四层架构生态 | 工具 |
| 10 | agentskills 技能目录生态 | 可复用 Skill |

## 复核
十独点均有当日实拉来源；五点增量合并（均含≥40% 独有增量）、五点新面；无纯重复。版本建议 3.64.0。