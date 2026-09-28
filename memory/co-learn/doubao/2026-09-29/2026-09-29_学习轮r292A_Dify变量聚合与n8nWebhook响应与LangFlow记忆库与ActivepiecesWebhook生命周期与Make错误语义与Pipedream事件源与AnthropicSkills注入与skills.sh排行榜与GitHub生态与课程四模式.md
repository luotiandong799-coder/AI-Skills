# r292A 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r291 全表（workbuddy 留痕 + SKILL.md 1,972,533B 最新小节 r291C）。查询词与既往全表错开。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | 变量聚合器：多分支输出收敛为一变量 / array 模式收集全部分支输出成列表→Code 节点处理 / Output 节点可多个但分支无 Output 返回空 / 多模型适配器（Model Adapters）+API Gateway 层 | 合并保留增量（r289A 变量作用域链，本点=聚合节点+array 模式） | 工作流 |
| 2 | n8n | Respond to Webhook：Immediately 模式短同步陷阱（40 秒工作流被调用方超时切断）/ 认证 Webhook（header 校验 secret）/ Webhook 防火墙（IF+Regex 前置拒畸形数据防污染下游）/ 生产/测试双 URL | 新面 | 工作流 |
| 3 | LangFlow | Memory bases：flow 级向量存储自动摄取会话历史跨会话持久（区别于 session-scoped）/ embedding 模型复用保证查询与存储向量可比 / DB Providers 可配置向量后端 | 合并保留增量（r289B 知识库机制，本点=对话记忆持久化） | 工具 |
| 4 | Activepieces | Webhook Trigger 三阶段（On Enable 用 context.webhookUrl 注册+store 存 ID / On Handshake 握手）/ App Webhooks 每 OAuth2 应用单 webhook 约束+AP_APP_WEBHOOK_SECRETS 环境变量注入 / Embeddable MCP：用户宿主应用内登录→一个 Authorize 按钮→后端拿 token 跑用户自动化 | 合并保留增量（r291B 嵌入 JWT 流，本点=Webhook 生命周期+Embeddable MCP） | 工具 |
| 5 | Make | 错误处理四策略语义（Ignore/Retry/Rollback 停 run+撤销变更 vs Commit 停止但标记成功）/ {{error.type}}/{{error.message}} 变量+Router 按错误类型分流 / 三模块骨架（Log 存储+Notify+Guardrail 验证假设）/ Incomplete executions 保存失败时 blueprint+日志可重跑 | 合并保留增量（r289C 错误处理器四型，本点=Rollback 撤销语义+蓝图重跑） | 工作流 |
| 6 | Pipedream | 事件源独立于 workflow 部署（source 收集事件流→workflow 订阅）/ 单工作流多触发器 / 多语言步骤（Node/Python/Go/Bash）/ Secrets 环境变量不硬编码 / built-in OAuth+retries+error handling | 合并保留增量（r291B Connect/r291C AI 面，本点=事件源独立部署+多语言） | 工具 |
| 7 | Anthropic | Skills 注入机制：挂载 GitHub repo 时 .claude/skills 根目录自动扫描→名称/描述/路径注入 system prompt→SKILL.md 内置工具读取（无需上传）/ Skills API GA（2026-08-30 退出 beta）/ 三表面（repo 源/格式规范/产品行为） | 合并保留增量（历史 anthropics/skills 多轮，本点=自动注入+API GA） | 可复用 Skill |
| 8 | skills.sh | ~669,670 skills（2026-06）/ top=find-skills 2.0M installs / 匿名遥测驱动排行榜（all-time+24h trending+热门三视图=安装量即信任度）/ npx skills add owner/repo 一键安装 / find-skills 元技能以技能管技能 | 合并保留增量（r290A SkillHub 数据面，本点=遥测排行榜+元技能） | 可复用 Skill |
| 9 | GitHub 生态 | Google 官方 skills 仓库（google/skills 13 skills 聚焦云产品）/ DeepSeek 智能体框架（一切皆插件：模型适配器/工具/会话日志/agent 循环可替换+开箱 Web UI）/ NVIDIA OpenShell 安全运行时（安全运行时边界+全栈治理）/ 阿里 Open Code Review 混合架构 | 新面 | 工具 |
| 10 | deeplearning.ai | Agentic AI 四设计模式（Reflection 自我批评迭代/Tool Use/Planning/Multi-Agent）/ Agent Skills with Anthropic 课程（开放标准一次构建跨 agent 部署）/ LLMs as OS（MemGPT/Editable memory/Agentic RAG） | 合并保留增量（r291A 课程信号，本点=四模式完整框架） | 可复用 Skill |

判重口径：增量判定。本轮 2 新面 + 8 合并保留增量，零纯重复。