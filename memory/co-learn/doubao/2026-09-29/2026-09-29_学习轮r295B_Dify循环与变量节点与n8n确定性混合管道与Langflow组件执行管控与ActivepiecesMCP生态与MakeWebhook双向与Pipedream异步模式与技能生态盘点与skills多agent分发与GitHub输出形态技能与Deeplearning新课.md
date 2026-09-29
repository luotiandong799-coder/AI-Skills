# r295B 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r295A 全量 + WorkBuddy r294 续作（ede6bb1）。查询词与 r295A 全错开（本轮=工作流变量循环/工作流模板最佳实践/组件自定义开发/触发器集成/Webhook场景/工作流异步事件/开源仓库/CLI使用/GitHub AI开源/学习社区课程）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | Loop vs Iteration 选择判据（前次依赖用 loop、数组处理用 iteration）+循环变量 1.2.0 自动管理（免手动维护索引）+loop_count 必设防死循环 + 变量聚合器/变量赋值节点职责分工（互斥分支汇合/更新会话状态与循环页码） | 合并保留增量（r295A 编排面，本点=循环/变量节点语义） | 工作流 |
| 2 | n8n | 确定性步骤+AI 步骤混合管道（AI 分类→Code 节点验证分类与置信度→Guardrails 查 NSFW/密钥→IF 分支）/ flat vs sub-workflow 判据（复制同逻辑>15 步拆子工作流）/ Tools Agent 配置（system message 命名允许动作+Max Iterations=最长真实工具链+2） | 合并保留增量（r295A 重试/r294C 模板，本点=AI+确定性混合与子工作流判据） | 工作流 |
| 3 | LangFlow | LANGFLOW_ALLOW_CUSTOM_COMPONENTS 禁用自定义组件执行（+LANGFLOW_COMPONENTS_PATH allow-list）/ 1.12 uv 精简默认安装+opt-in providers 按需装 / lfx extension init 脚手架（extension.json manifest） | 合并保留增量（r295A 安全基线，本点=组件执行管控+精简安装） | 工具 |
| 4 | Activepieces | 400+ MCP servers 原生 agent 集成（type-safe pieces 框架）/ webhook 双角色（触发器或动作）/ ~60% pieces 社区贡献且全部 npm 发布 / 763 集成 | 合并保留增量（r295A Flow-as-Tool，本点=MCP 面+社区贡献） | 工具 |
| 5 | Make | webhook-triggered AI agent 双向（收数据→agent 回写 webhook）/ mailhook 邮件即时触发（email webhook 非轮询）/ webhook vs polling（Stripe 无轮询触发器时 webhook 唯一路径） | 合并保留增量（r295A Make AI Agent，本点=webhook/mailhook 触发面） | 工具 |
| 6 | Pipedream | 异步处理 parallel+queued 执行模式 / Data stores 持久 KV 跨执行保持状态 / 版本控制回滚 / 默认超时 60 秒 / Workday 2025-11-19 收购（2026-01 完成） | 合并保留增量（r295A MCP 端点，本点=异步模式+数据存储+版本回滚） | 工具 |
| 7 | Agent Skills 开源 | 生态头部盘点：addyosmani/agent-skills 98.4K（SDLC 六阶段 20 技能）/ affaan-m/ECC 268K（harness 性能优化）/ antigravity-awesome-skills 889+ 通用技能 / Anthropic 官方 skills 仓库发布 | 合并保留增量（r294C 模板生态，本点=仓库级盘点） | 可复用 Skill |
| 8 | skills.sh CLI | npx skills add 自动检测本机 51 个 agent 写入各自技能目录 / find/add/check/update 四核心命令 / --skill 精确安装单个 / localskills 匿名共享（Ed25519 密钥对，免账号） | 合并保留增量（r295A Pin SHA，本点=多 agent 分发+匿名共享） | 可复用 Skill |
| 9 | GitHub 趋势 | 输出形态技能霸榜（i-have-adhd 先说答案/caveman 说短话省 token/humanizer 去 AI 味）+ freellmapi 29K（34 免费 LLM provider 单 /v1 端点+自动 failover+加密 key）+ RAG_Techniques 29.6K 高级 RAG notebook 合集 | 合并保留增量（r294C 模板生态，本点=输出技能面+免费聚合） | 可复用 Skill |
| 10 | deeplearning.ai | Building Adaptive AI Agents 新课（2026-08-26）/ Building AI Assistants with On-Device Memory（设备端记忆）/ Spec-Driven Development with Coding Agents（JetBrains 合作，r293B 已落相关）/ 185 门课程盘点 | 合并保留增量（r295A Agentic，本点=新课面） | 可复用 Skill |

判重口径：增量判定。本轮 10 合并保留增量，零纯重复。