# r297B 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r297A 全量（含 r297A 十独点）+ 并行侧。查询词与 r296 三轮及 r297A 全错开（本轮=策略插件化/Critic评分循环/HITL门控/凭据生命周期/错误处理四选项/托管OAuth/官方技能分类/SOC职业分类/CI控制面MCP/Inspector测试与四者对比主题）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | Agent 策略插件化：ReAct（Reason+Act 交替）vs FunctionCalling（原生 function calling，适合 GPT-4/Claude 3.5 强函数调用模型）vs CoT——按模型能力选策略；插件生态治理 P0-P2 分级维护（Top 20%+criticality≥4→P0） | 合并保留增量（r297A #1 策略匹配，本点=具体策略判据+生态治理） | 工作流 |
| 2 | n8n | Production AI Playbook：Critic Agent 评分循环——Critic 按 accuracy/clarity/relevance/conciseness 打分，低于 minScore 循环回 Writer 带具体问题修订，maxIterations 上限退出路由人工审查 | 合并保留增量（r296A 模型分工，本点=评分循环+迭代上限+人工兜底） | 工作流 |
| 3 | LangFlow | 版本演进：1.11 Human-in-the-Loop（gated tool calls+reviews）；1.12 OpenTelemetry（service health+flow runs 可观测）；Extension bundles 模型（lfx-arxiv/lfx-docling 等四包）；1.8 全局模型 provider 设置减少 credential sprawl | 合并保留增量（r295B 审批门/r296B 可观测，本点=HITL 门控+OTel+bundles） | 工作流 |
| 4 | Activepieces | 凭证生命周期：256-bit 加密+**无读取 API**（只在处理时发送、之后撤销）；日志数据掩码（敏感信息永不进日志）；OAuth2 限定 scope；Secret Manager 集成（1Password/Vault）+定期轮换 | 合并保留增量（r296A 入站认证，本点=凭据无读取+日志掩码+外部 Secret Manager） | 工具 |
| 5 | Make | 四错误处理选项：Resume（忽略继续）/Ignore（跳过该 bundle）/Rollback（取消开始以来所有变更）/Commit（确认错误前变更）；Incomplete Executions 暂存手动处理；指数退避自动重试（connectionerror/moduletimeouterror） | 合并保留增量（r296A 节点失败三选项，本点=四选项含事务语义） | 工作流 |
| 6 | Pipedream | 托管 OAuth 全程（hosted clients+secure storage+automatic refresh，用户永不碰凭证）；**short-lived Connect tokens（4h）+tokenCallback 模式**（前端 SDK 用回调问后端要新鲜 token，不自己管过期）；Connect Link 托管流免构建 | 合并保留增量（r296A OAuth 刷新，本点=前端短命 token+callback） | 工具 |
| 7 | Anthropic | 官方 skills 仓库分类：Creative & Design/Development/文档（Word/PDF/PPT/Excel production-ready）；官方发布要求=公开 repo+清晰 README 安装说明+示例与截图；生态：awesome-claude-skills（ComposioHQ）26k+★、obra/superpowers 行为技能集 | 合并保留增量（r296A gh skill，本点=官方分类+发布清单） | 可复用 Skill |
| 8 | skills.sh | /api/v1/skills/search 按名称/描述搜索；类别体系（Web Dev/Testing/DevOps/Docs/Code Quality）；**SkillsMP 800k+ skills 按 SOC 税业分类（800+ 职业）找技能**；find-skills 模糊+语义双搜索 | 合并保留增量（r296C AI 目录，本点=SOC 职业分类导航） | 工具 |
| 9 | GitHub | **GitHub Actions MCP Server**：给 agent CI/CD 管道控制面（list/view/trigger/cancel/rerun runs+失败日志分析）——现有 GitHub MCP 不能碰管道；MCP server 测试三件套=unit+contract+schema drift（cron+push+PR 触发）；AWS 模式=只读调查/写操作分工具 | 合并保留增量（r295B MCP 安全，本点=CI 控制面缺口+contract/schema drift） | 工具 |
| 10 | deeplearning | MCP 课程（Anthropic）：FastMCP 建 server（tools/resources/prompts）→**MCP Inspector 测试**→chatbot 内建 client 动态连接→参考服务器（filesystem/fetch）；Agent Skills 课程：skills 与 tools/MCP/subagents 四者关系对比、按需加载 | 合并保留增量（r295B MCP 架构，本点=Inspector 测试+四者对比） | 工作流 |

判重口径：增量判定。本轮 10 合并保留增量，零纯重复。