# r285C 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r285A/B、r284 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（可观测） | OK | **OpsTraceManager 异步分发 trace 数据到多个第三方可观测平台（LangSmith/Langfuse/Arize Phoenix/阿里 ARMS）；凭证加密、动态 provider 实例化、重试机制**；**Trace ID 传播：Flask after_request hook 注入 OpenTelemetry trace headers，关联日志与 trace**；**Arize Phoenix：模型调用/工具调用/链步骤自动 trace；输入输出延迟元数据**；**Audit Log：资源变更/权限操作/配置调整结构化记录、精确过滤、导出** |
| 2 | n8n（数据映射） | OK | **Item Linking：pairedItem 属性追踪哪个输入 item 产生哪个输出；Code 节点需手动 supply pairedItem**；**$input.item / $('节点名').item 沿 item linking 链找父 item**；**表达式引用：$json（当前 item）、$node["X"].json（任意命名节点）、$() 现代等价**；**数据映射四操作：添加字段/修改字段/mapping（系统间格式转换）/清理** |
| 3 | LangFlow（API keys） | OK | **API key 验证两种模式：db（默认，数据库存）vs env（LANGFLOW_API_KEY 环境变量，K8s/CI/CD 用）**；**JWT 认证：LANGFLOW_ALGORITHM（HS256/RS256/RS512）+ SECRET_KEY/PRIVATE_KEY/PUBLIC_KEY**；**全局变量：用户定义存数据库，可源自环境变量（OPENAI_API_KEY）**；K8s secrets 推荐 secretKeyRef；x-api-key header 或 query 参数 |
| 4 | Activepieces（MCP） | OK | **一个 Activepieces MCP server 暴露 760+ app 集成给 AI agent（Claude/Cursor/Windsurf 等任何 MCP client）；每个 piece 自动成为 MCP server**；**AI-ready pieces：tool search（按任务描述搜 action，ap_search_actions）+ AI metadata + audience**；**MCP tool exposure：工作流作为可调用工具暴露、结构化输入**；Human Review Steps（审批暂停 run 等人工）；凭证加密 |
| 5 | Make（Data Store） | OK | **Data Store 模块操作表：Delete All Records（清除全部）/ Get a Record（按唯一 key 读单条）/ Search Records（过滤读取）/ Check the Existence（存在性检查不取数据）/ Count Records（聚合计数）/ Add/Replace a Record**——**读写分离：existence check 与 count 不拉数据** |
| 6 | Pipedream（共享/子模块） | OK | **Components 发布：publish 到账户私有使用或贡献到 Pipedream registry；Verified Components（GitHub PR 流程验证）**；**GitHub Sync：workflow.yaml 引用私有组件需前缀 @workspacename**；**step exports 共享数据（run({steps,$}) 中 steps 参数）**；**自定义 Node.js 模块复用常量/GraphQL strings/简单函数**；common 模块抽象跨组件复用（.app.mjs 模式） |
| 7 | Claude Code（Hooks） | OK | **Hooks 事件：SessionStart/SessionEnd（会话级）、UserPromptSubmit/Stop/StopFailure（turn 级）、PreToolUse/PostToolUse（每次工具调用）、Setup（--init-only/CI 一次性准备）、UserPromptExpansion（可阻止扩展）、DirectoryAdded/FileChanged/WorktreeCreate**；**Hook 回调返回决策字典：{} 允许，permissionDecision allow/deny；可改 updatedInput（如重写 Write 的 file_path 到 /sandbox）**；**SDK 两种 hooks：filesystem（settings.json 命令）+ programmatic（query() 回调函数）**；**沙箱：npx @anthropic-ai/sandbox-runtime claude 启动，filesystem 与网络边界配置** |
| 8 | GitHub（MCP server） | OK | **远程 GitHub MCP Server（GitHub 托管，api.githubcopilot.com/mcp）+ 本地版**；**dependabot toolset：依赖漏洞扫描（发送依赖信息到 GitHub Advisory Database，返回受影响包/严重度/建议修复版本）**；**secret scanning：AI 编码 agent 在 commit/开 PR 前扫描暴露密钥（需 GitHub Secret Protection）**；mcp-github-agent（PyPI）：search_code/list_issues/create_issue（policy-guarded）；Copilot code review 支持 agent skills+MCP GA |
| 9 | agentskills（生态） | OK | **AgenticSkills.io：189+ 验证技能/16 分类，按平台/质量/用例过滤**；**agentskills.codes：开放注册表 19,296 可安装技能、扫码每日、一条命令安装兼容所有主流 coding agent**；**Agent Skills Marketplace（aiskillstore）：官方市场，遵循 Agent Skills 规范**；**Agent Skill Exchange：2788 技能/17 分类/10 框架，trust 与 adoption 信号**；安全技能库（754 skills MITRE ATT&CK+NIST CSF 映射） |
| 10 | WaytoAGI（知识库） | OK | **开源 AI 知识库+共学社区（900 万 AI 学习者），面向中文 AI 学习者/创作者/企业实践者**；**系统化知识库：AI 入门/Prompt/Agent/AIGC 创作/开发实践/行业报告/论文资讯，可检索可引用可复用**；**AI 智能问答：飞书群集成 AI 问答机器人，知识库全文向量化，提问映射原文段落给出处链接**；每日晚 8 点直播共学；学习路径用布鲁姆分类法设计 |

## 判重（双键检索，增量判定）
- Dify 可观测（r284 版本控制 / r285A 提示词 / r285B API）→ OpsTraceManager/Trace ID 传播/Audit Log 新面 → **新面**
- n8n Item Linking（r284A 表达式体系 / r285A Webhook / r285B 凭证）→ pairedItem 数据血缘 增量>40% → **合并保留增量**
- LangFlow API keys（r284 记忆/组件 / r285A Tool Mode / r285B 存储）→ db/env 双模式/JWT 新面 → **新面**
- Activepieces MCP（r284 分支/触发器/测试 / r285B 错误）→ 单 server 暴露全部 app/tool search 新面 → **新面**
- Make Data Store（r284C 已落 Data Store 持久化）→ 重叠约 50%，增量=模块操作细分/existence check 不拉数据（≥40%） → **合并保留增量**
- Pipedream 共享（r284A 组件复用系统 / r285B 调度）→ 重叠约 50%，增量=GitHub Sync workflow.yaml/step exports/自定义模块（≥40%） → **合并保留增量**
- Claude Code Hooks（r285B Skills 结构）→ Hooks 事件表/决策字典/updatedInput 重写 新面 → **新面**
- GitHub MCP server（r284C 官方 MCP server 工具面）→ 重叠约 50%，增量=dependabot toolset/secret scanning 前置（≥40%） → **合并保留增量**
- agentskills 生态（r284A Agent Skills 生态与安全）→ 重叠约 45%，增量=agentskills.codes 注册表/AgenticSkills 目录/信任信号（≥40%） → **合并保留增量**
- WaytoAGI（前轮未拉）→ 新面 → **新面**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 可观测与 Trace ID 传播 | 工作流 |
| 2 | n8n Item Linking 数据血缘（合并增量） | 工具 |
| 3 | LangFlow API key 双模式与 JWT | 工具 |
| 4 | Activepieces 单 MCP server 暴露全部集成 | 工作流 |
| 5 | Make Data Store 操作细分（合并增量） | 工具 |
| 6 | Pipedream 组件验证与共享机制（合并增量） | 工具 |
| 7 | Claude Code Hooks 事件与决策字典 | 可复用 Skill |
| 8 | GitHub MCP 安全工具集（合并增量） | 工作流 |
| 9 | agentskills 生态注册表与信任信号（合并增量） | 可复用 Skill |
| 10 | WaytoAGI 开源知识库与共学模式 | 工作流 |

## 复核
十独点均有当日实拉来源；5 新面 + 5 合并保留增量（增量均≥40%），零纯重复。版本建议 3.72.0。