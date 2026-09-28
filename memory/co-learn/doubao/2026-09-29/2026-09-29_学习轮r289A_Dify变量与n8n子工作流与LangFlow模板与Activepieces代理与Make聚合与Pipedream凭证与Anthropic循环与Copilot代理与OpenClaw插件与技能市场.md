# r289A 学习轮留痕（2026-09-29）

> 批次说明：r288 编号已被凌晨另一流程占用并 push（34d48fa/af181fc/47eecef/df6ad80，各 3 独点落 agent-guild 等），本批顺延为 r289，判重基线纳入 r288 九独点。

## 信源实拉清单（10 站全量逐站；查询词与 r284-r288 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（变量作用域） | OK | **Workflow 变量={{node_name.variable_name}} 路径语法，作用域=单次执行、每次运行重置**；**会话变量经 Variable Assigner 节点持久化（同一 conversation_id 永续，设计不明清即跨轮引用）**；**系统变量全集：sys.user_id/app_id/workflow_id/workflow_run_id/files/query/dialogue_count/conversation_id（Workflow 与 Chatflow 差异）**；**显式声明输出否则不自动传播**；**作用域链查找顺序：节点变量→会话变量→环境变量，同名节点变量优先；局部变量覆盖同名全局变量** |
| 2 | n8n（子工作流） | OK | **子工作流输入三模式：Define using fields（父调用自动拉入字段）/ Define using JSON example / Accept all data（方便但生产不安全，field/JSON 更安全因调用方可见期望值）**；**数据流自动：父输入 items 直接进子触发（Execute Sub-workflow Trigger），子最后节点输出=父节点输出**；**Call n8n Workflow Tool：把任何 workflow 打包成 AI agent 可调用工具（独立触发/逻辑/输出）**；**只映射子工作流真正需要的字段；用业务语义命名；可预测路径/多处复用同 agent 逻辑→子工作流更干净（vs AI Agent 节点）** |
| 3 | LangFlow（提示词模板） | OK | **{VARIABLE_NAME} 动态变量；双大括号 {{}} 转义字面大括号防被解释为变量**；**全局变量经 API 端点 /responses 传：自定义 header X-LANGFLOW-GLOBAL-VAR-{VARIABLE_NAME}**；**Prompt 节点输出接 LLM 系统消息槽作全局角色指令**；**LangChain partial variables：预填值可为 callable（运行时惰性求值）**；**变量名拼写/下划线必须与 key 完全一致否则 KeyError** |
| 4 | Activepieces（AI Agent） | OK | **agent 三要素=指令（instruction）+ 允许的工具 + 给的知识（上传文件/表格）**；**工具=任何集成（678+ pieces）/另一个自动化（flow as tool）/自己的 MCP servers**；**两个限制：runs 之间不记忆、无 SharePoint/Drive/Notion 实时同步**；**agent 作为 flow 的一个 step 插入，处理数据传给下一部分；flow 内给 prompt 指定该 step 任务；链式 agent（research/writing/review 分工）**；**human approval steps 暂停执行直到人确认；结构化数据输出 push clean JSON**；**AI MCP server：一个 URL 暴露 6 工具（Ask AI/Summarize/Generate）+ 760+ apps** |
| 5 | Make（数据处理） | OK | **merge() 合并同结构数组；Set Variable 模块让 merge 输出清晰**；**Array Aggregator 多 bundle 合成单数组（批量插入/结构化列表）**；**关键坑：聚合分组依赖 rowId 一致性——rowId 缺失/不一致则无法正确分组，下游模块会跑 N 次**；**Map + Get/First 内置函数取数组值（map(complex array; key; [filter key]; [csv values])）**；**Router + Filter 分支（Status=New/Done/Error → 不同 Slack/Email）**；**Text Parser（regex）/ JSON Parser / Iterator 逐项** |
| 6 | Pipedream（凭证/认证） | OK | **secrets 两通道：connected accounts（平台支持时）或 environment variables（任意配置数据），永不硬编码在代码**；**外部认证 External auth：从 DB/secrets store 取凭证，账户选择器右下 Use external authentication 选项，按提示填 oauth_access_token/api_key**；**给最终用户跑 workflow 必须用自己的 custom OAuth clients（自己注册 OAuth app、加 oauthAppId）**；**迁移到代码映射：$auth→环境变量、OAuth→Supabase Vault、data store→对应 KV** |
| 7 | Anthropic（Agent SDK/loop） | OK | **agent loop=while 循环，stop_reason != "tool_use" 才停（end_turn 停止）——Ring 1 假设只调一次工具是错的，真实任务常需多次调用**；**toolRunner() 返回 async iterable，for await...of 迭代（tool call loop）**；**Agent SDK 把 Claude Code 的工具/agent loop/上下文管理变成库（Python/TypeScript）**；**Managed Agents 迁移映射：@tool 函数→声明 {"type":"custom"} 在 Agent 上（客户端处理 agent.custom_tool_use events 回 user.custom_tool_result）；内置工具→agent_toolset_20260401 在 session sandbox /workspace 跑**；**错误 subtype：error_max_budget_usd 预算超限、turn limit 可 Resume with higher limit 恢复会话** |
| 8 | GitHub（自定义 agent/指令） | OK | **自定义 agent=.github/agents/*.agent.md（YAML frontmatter + Markdown 指令）；Copilot CLI 用 /agent 选自定义 agent**；**custom instruction files 带 YAML header applyTo 字段嵌入仓库（编码规范/架构决策/项目指南），Chat 处理请求自动读入**；**custom instructions 改动不立即生效于活动 CLI 会话——退出后 resume（copilot --continue）或 /new**；**Copilot code review 支持 agent skills + MCP（GA 2026-07-29），review 时调用团队工具/标准，SKILL.md 放仓库**；**VS skills panel 创建 skill；场景文件放 .github/skills/ 或 .github/upgrades/skills/，scenarioTraitsSet 定义匹配特征** |
| 9 | OpenClaw（插件机制） | OK | **插件扩展 channel/model provider/agent harness/tools/skills/speech/realtime transcription/voice/media/web fetch/search**；**安装：openclaw plugins install clawhub:<package>（ClawHub 发布）或 npm: 裸包**；**能力同意机制 capability consent：/plugins install clawhub:<package> --accept-capabilities（同意才装）**；**插件 hooks：api.on("hook_name", handler)，三套 hook 系统（typed plugin hooks/before_tool_call 等）**；**Plugin SDK=typed contract；Capability model：registerProvider/registerCliBackend/registerEmbeddingProvider/registerSpeechProvider**；**CLI：plugins update/registry/doctor/init/build；ClawHub 5000+ 社区技能；Kimi Claw 接入 ClawHub（模型厂商下场）** |
| 10 | skills.sh / 生态 | OK | **npx skills add <repo> 一行装：fetch repo → 检测本地 agent → 写入正确目录，支持 51 agents**；**skills.sh 2026-01-20 Vercel 发布，2026-06 列 ~669,670 skills，2026-09 达 1M skills + ~280M installs（7 个月；GitHub 用 27 个月到 1M）**；**排行榜基于匿名遥测：find-skills 2.0M installs / frontend-design 531.8K**；**安全：NXplace 报道 36% 技能危险**；**目录治理对比：Anthropic 官方（人工精选/验证）、skills.sh（开放 npm 式、builder 侧审计）、SkillsMP（~1.9M 从 GitHub 抓取、无审查——装前自查）、SkillHub（7,000+ AI 评估自动打分）、Agensi（评审后上架 + 8 点安全扫描）**；**agentskills.sh 命令商店：search/info/install/install-skillset/list** |

## 判重（双键检索，增量判定）
- Dify 变量（r287A 已落"节点错误处理与变量引用"）→ 重叠约 60%，增量=作用域链顺序（节点→会话→环境）/系统变量全集/显式声明输出/局部覆盖全局/会话变量 conversation_id 永续 → **合并保留增量**
- n8n 子工作流（r284-r288 未落子工作流结构）→ 输入三模式/数据流自动传递/Call n8n Workflow Tool 打包 agent 工具/只映射所需字段 → **新面**
- LangFlow 提示词模板（r284-r288 未落模板机制）→ 双花括号转义/全局变量 header 传递/partial callable 预填/变量名严格一致 → **新面**
- Activepieces Agent（r287A 已落"Agent 资产化"）→ 重叠约 60%，增量=三要素定义（指令+工具+知识）/两限制（无跨 run 记忆/无实时同步）/flow step 定位/链式 agent/human approval → **合并保留增量**
- Make 聚合（r287B 已落"fan-out then fan-in 四步"）→ 重叠约 60%，增量=merge() 函数/Set Variable 清晰化/聚合分组 rowId 一致性坑/Map+Get 取数组值 → **合并保留增量**
- Pipedream 认证（r285A 已落"Pipedream认证"）→ 重叠约 60%，增量=external auth 选项/给最终用户跑必须 custom OAuth clients/迁移到代码映射（$auth→env/OAuth→Vault/data store→KV）/connected vs env 决策 → **合并保留增量**
- Anthropic loop（r284 已落"工具循环查终止条件"）→ 重叠约 60%，增量=Agent SDK 具体实现（toolRunner async iterable）/错误 subtype（error_max_budget_usd/turn limit resume）/Managed Agents 迁移映射（@tool→custom/内置→sandbox toolset）→ **合并保留增量**
- GitHub Copilot（r287B 已落"Copilot Code Review 技能化"）→ 重叠约 60%，增量=.agent.md 文件格式/applyTo YAML header/CLI /agent 选择/instructions 不立即生效需重启会话 → **合并保留增量**
- OpenClaw 插件（r284-r288 未落插件架构）→ capability model/能力同意机制/ClawHub 发布/hooks 三套系统/CLI 命令族 → **新面**
- 技能市场（r287A 已落"技能市场 npm 化+find-skills 规模"）→ 重叠约 65%，增量=36% 危险安全警告/目录治理对比表/agentskills.sh 命令族/1M skills 规模数据 → **合并保留增量**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 变量作用域链与会话变量持久性（合并增量） | 工作流 |
| 2 | n8n 子工作流输入契约与 Call Workflow Tool | 工作流 |
| 3 | LangFlow 提示词模板转义与全局变量传递 | 工具 |
| 4 | Activepieces Agent 三要素与流内定位（合并增量） | 工具 |
| 5 | Make 数组合并与聚合分组 rowId 契约（合并增量） | 工具 |
| 6 | Pipedream 凭证三通道与外部认证（合并增量） | 工具 |
| 7 | Anthropic Agent SDK loop 与迁移映射（合并增量） | 工具 |
| 8 | GitHub 自定义 agent 文件契约（合并增量） | 工作流 |
| 9 | OpenClaw 插件架构与能力同意 | 工具 |
| 10 | skills 市场治理对比与安全警告（合并增量） | 工作流 |

## 复核
十独点均有当日实拉来源；3 新面 + 7 合并保留增量（增量均≥40%），零纯重复。版本建议沿用 3.74.0。