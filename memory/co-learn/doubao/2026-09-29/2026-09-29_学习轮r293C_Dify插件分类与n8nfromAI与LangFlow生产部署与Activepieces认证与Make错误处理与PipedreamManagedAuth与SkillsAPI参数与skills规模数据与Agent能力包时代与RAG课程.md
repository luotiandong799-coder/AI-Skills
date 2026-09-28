# r293C 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r293B 全表。查询词与既往全错开（本轮=插件开发、Agent工具、API部署、连接器认证、错误处理、Connect认证、Skills API、排行榜、仓库趋势、RAG课程）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | 六类插件分类（Tool/Trigger/Extension/Model/Datasource/Agent Strategy）/ Agent Strategy Plugin（自定义推理决策逻辑：选工具/调用/处理结果）/ daemon 生命周期管理 | 合并保留增量（r292C 插件安全，本点=六类+Agent Strategy） | 工具 |
| 2 | n8n | $fromAI() 表达式自动填充参数 / 工具描述引导 AI 何时使用 / 工作流暴露为 MCP 工具（MCP server trigger） | 合并保留增量（r292B Agents/r293A n8n-MCP，本点=$fromAI+工具描述） | 工作流 |
| 3 | LangFlow | headless runtime 生产部署（仅服务 API 无可视化编辑器）/ LFX serve（POST /flows/{id}/run，需 API Key）/ Flow DevOps Toolkit SDK（url+api_key_env） | 合并保留增量（r292B bundles/r293B Agentics，本点=生产部署面） | 工具 |
| 4 | Activepieces | Piece Auth 声明式认证（auth 参数定义在 createPiece/createTrigger/createAction）/ predefined connections（嵌入应用免重输认证） | 合并保留增量（r293A 模板/r293B MCP，本点=认证面） | 工具 |
| 5 | Make | Retry handler 细节（暂停失败 bundle 存错误/映射/流程）/ incomplete executions（保存失败 run 的 blueprint+日志可重跑）/ AI 错误解释 | 合并保留增量（r292A 四策略，本点=incomplete executions） | 工作流 |
| 6 | Pipedream | Managed Auth+Connect Link 双通道（externalUserId+服务器端 token / 无法执行 JS 时替代）/ Workday 收购（2026-01-31 完成，MCP 集成最大验证事件） | 合并保留增量（r292C Connect/r293A ShareLink，本点=Managed Auth+收购） | 工具 |
| 7 | Anthropic | Skills API container 参数（{"type":"anthropic","skill_id":"pptx","version":"latest"}）+ code execution 前置 / files_from_dir+ant apply 目录上传 | 合并保留增量（r292B SDK/r293B 仓库结构，本点=API 参数面） | 可复用 Skill |
| 8 | skills.sh | 生态规模（2026-06 ~669,670 skills、find-skills 2.0-3.4M 安装、frontend-design 531.8-881.3K）/ 分类周榜（context-compression 榜首） | 合并保留增量（r292A 遥测/r293B 三标准，本点=规模+周榜） | 可复用 Skill |
| 9 | GitHub | Agent Skills 能力包时代（openai/skills+anthropics/skills 集中上线，可组合/版本化/可审计；GitHub Explore 新增 agent skills 标签）/ Agentic Workflows（2026-02 仓库任务自动化） | 合并保留增量（r292A 生态/r293A 框架，本点=能力包时代） | 工具 |
| 10 | deeplearning.ai | sentence-window+auto-merging 两种高级检索法 / RAG triad 指标评估 / 课程退役策略（模型弃用→video-only 保留架构价值） | 合并保留增量（r293B 记忆工程课，本点=RAG 课程面） | 可复用 Skill |

判重口径：增量判定。本轮 10 合并保留增量（每点均含≥40% 独有增量），零纯重复。