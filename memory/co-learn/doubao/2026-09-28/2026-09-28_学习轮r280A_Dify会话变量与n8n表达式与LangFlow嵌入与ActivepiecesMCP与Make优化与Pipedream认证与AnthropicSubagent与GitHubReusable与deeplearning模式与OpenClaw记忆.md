# r280A 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r279 全表 30 词 + r278 全表 30 词 + r277/r276 概要错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（prompt variables） | OK | 双花括号 {{var}} 引用（模型前替换）；会话变量 6 类型（String/Number/Object/Array[string]/Array[number]/Array[object]）；变量赋值节点；append mode（Array[object] 持续追加=简易 OpenAI memory）；Context Variables（外部知识注入保持来源归属）；变量解析纪律（大小写敏感 user_name≠UserName、用变量选择器不手打、空值默认渲染空串、Strict Mode 开关、节点输出引用 {{llm_xxx.output}}）；输入字段类型（Paragraph/Number/下拉/单选/Checkbox/API-based 256 字符） |
| 2 | n8n（expressions） | OK | 表达式核心对象：$json（当前项）/ $binary / $("NodeName").first()/.item/.all() / $now/$today/$workflow/$node；$jmespath()（JMESPath 查复杂嵌套对象）；JSONata 函数（$string/$merge/toJsonString 等）；表达式与 Code node 通用 |
| 3 | LangFlow（chat widget） | OK | 嵌入式 chat widget（host_url 必须 HTTPS + flow_id 最小 props）；HTML script 嵌入（cdn bundle）；React/Angular 嵌入；API pane（Python/JS/curl 代码片段）；Share→Embed into site / Shareable Playground；Chat Input/Output 组件 + Files Input；react-native-langflow-chat |
| 4 | Activepieces（MCP） | OK | 单 MCP server 驱动整个平台（build flows/763 apps/manage tables/debug runs 自然语言）；OAuth 认证（首次浏览器授权）；mcpServers 配置加 URL；可嵌入 MCP（authRequestId→Authorize→code→token→跑用户 flows）；MCP piece（flow 内 1 trigger+1 action）；Personal AI/AITable/AirTable/ProvenExpert 等 app 均同一 URL；Settings→MCP Server 开启；Claude/Cursor/Codex/VS Code 客户端 |
| 5 | Make（场景优化） | OK | 四杠杆：Bundle Size 聚合器（Array/Text/Numeric/Table Aggregator）、Filters 条件执行（省 80% 无用记录）、Aggregators 批量 API（50 条→1 次调用省 98% 操作）、Sub-Scenarios 并行化（=函数）；合并小场景成大工作流（最高 ROI 省 operation count）；指数退避+缓存降 90% 错误；去重过滤器省 40%；AI agent 最佳实践（tool naming/prompting/data access） |
| 6 | Pipedream（REST/MCP 认证） | OK | REST API 双认证：OAuth access token / User API keys，均 Bearer Authorization 头；Connect SDK（clientId/clientSecret/projectEnvironment/projectId）；Connect API Proxy（client_credentials 换 token）；MCP server 认证头：Authorization Bearer + x-pd-project-id + x-pd-environment + x-pd-external-user-id + x-pd-app-slug；为终端用户跑 workflow 需自定义 OAuth client（oauthAppId） |
| 7 | Anthropic（subagents/skills） | OK | subagent=markdown 文件 .claude/agents/（YAML frontmatter name/description/model/tools/skills/mcpServers + body=system prompt）；skills 字段=启动时**完整注入**上下文（非仅描述）；tool restrictions（omit=继承全部工具、specify=仅列工具——只读分析 agent 不能改文件）；SDK 侧经 Agent tool 调用；skills 与 CLAUDE.md 范围区别（CLAUDE.md 全时加载、skill 按需加载）；disable-model-invocation: true（有副作用技能禁止模型自动触发） |
| 8 | GitHub Actions（reusable/matrix） | OK | workflow_call 定义 reusable workflow 的 inputs/outputs/secrets 映射；matrix include/exclude 展开组合（fruit×animal、exclude 跳过不支持组合、include 追加特殊 job）；matrix 调用 reusable workflow 传不同 inputs；reusable workflows 与 agentic workflows 互补（agent 调用已批准的确定性 reusable workflow 而非复制逻辑）；跨仓库共享、GHES 支持 |
| 9 | deeplearning（building agents） | OK | Andrew Ng 四 agentic 设计模式：Reflection（审视自身输出改进）/Tool use（LLM 决定调哪些函数）/Planning（拆解复杂任务成可执行步骤、异常时适配）/Multi-agent collaboration（多个专门系统协作）；Agentic AI 课程强调从第一原理构建再框架；Browser Agents（AgentQ=MCTS+self-critique+DPO 教 agent 决策）；crewAI 多 agent 协作 |
| 10 | OpenClaw（memory） | OK | 三层记忆文件：MEMORY.md（长期 curated 事实/偏好/决策，会话开始加载）/ memory/YYYY-MM-DD.md（每日 append-only 日志）/ 会话自动归档（session database）；全局 ~/.openclaw/workspace/MEMORY.md vs 项目层；SQLite/Redis backend、memory.max_entries 可配；周审日志→提取模式→更新 MEMORY.md；文件过大 inflate 每次请求 token（每文件几千词上限）；boot-md hook 加载 |

## 判重（双键检索，增量判定）
- Dify 会话变量（r279A 分块/r279B 环境变量/r279C Agent/r278A 混合检索/r277 Chatflow 变量）→ r277 有 conversation variables 概要，本面=变量解析纪律+6 类型+append 记忆 → 增量合并
- n8n 表达式（r279A 错误/r279B 秘密/r279C LangChain/r278B 数据转换）→ 新面（表达式对象/JSONata/JMESPath）
- LangFlow widget（r279A 记忆/r279B API/r279C 工具/r278B 向量存储）→ r279B 有 API 面，本面=嵌入发布形态 → 增量合并
- Activepieces MCP（r279A 触发器/r279B AI/r279C 流程/r278C 嵌入）→ 新面（MCP 单入口/OAuth/可嵌入）
- Make 优化（r279A webhook/r279B 调试/r279C 数据存储/r278A 数据存储/r278B 模板）→ 新面（操作优化四杠杆）
- Pipedream 认证（r279A 调度/r279B 安全/r279C code steps/r278A Connect）→ 新面（REST/MCP 认证头/Connect SDK）
- Anthropic subagent（r279A 结构化/r279B 思考/r279C 缓存/r278C Batch）→ 新面（subagent 定义/工具限制/skills 注入）
- GitHub reusable（r279A 技能市场/r279B Models/r279C Copilot/r278A Actions 安全/r278C containers）→ 新面（reusable workflows+matrix）
- deeplearning 四模式（r279A 评估/r279B 多代理/r279C 可观测/r278A agentic RAG/r278C agents memory）→ r279B 多代理已落 crewAI，本面=四设计模式（Reflection/Planning）→ 增量合并
- OpenClaw 记忆（r279A 会话/r279B 开发/r279C 配置/r278C 多代理）→ 新面（MEMORY.md 分层/周审/文件大小 token 成本）

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 会话变量与变量解析纪律 | 工具 |
| 2 | n8n 表达式系统与 JSONata/JMESPath | 工具 |
| 3 | LangFlow 嵌入发布三形态 | 工具 |
| 4 | Activepieces MCP 单入口 | 工具 |
| 5 | Make 场景优化四杠杆 | 工作流 |
| 6 | Pipedream REST/MCP 认证 | 工具 |
| 7 | Anthropic subagent 定义与工具限制 | 工具 |
| 8 | GitHub reusable workflows+matrix | 工具 |
| 9 | deeplearning agent 四设计模式 | 工作流 |
| 10 | OpenClaw 记忆分层与 MEMORY.md | 可复用 Skill |

## 复核
十独点均有当日实拉来源；均新面或增量合并；无纯重复。版本建议 3.56.0+。