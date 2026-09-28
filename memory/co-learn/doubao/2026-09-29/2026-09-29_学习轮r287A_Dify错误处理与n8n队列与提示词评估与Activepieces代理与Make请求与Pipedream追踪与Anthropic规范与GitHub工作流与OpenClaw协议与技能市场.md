# r287A 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r284-r286 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（LLM 节点/工作流指南） | OK | **节点内建错误处理：LLM/HTTP/Code/Tool 节点支持 retries + failure behavior（stop / typed default value / fail branch 三选）**；**每个 LLM 节点单一职责（分类/生成/规则格式化分开，不同验证）**；**run logs 监控 token 用量（inputs/outputs/latency/usage）**；**Context Variables 注入外部知识保留来源归因（RAG）**；**变量引用格式 {{#节点ID.变量名#}}，用鼠标点选不要手打**；**DIFY_AGENT_SERVER_SECRET_KEY 生产必须替换 dev 默认值（secrets.token_urlsafe(32)）**；Dify 145,764 GitHub stars / 22,915 forks / 460+ contributors，v1.14.2（2026-05）安全加固 |
| 2 | n8n（Queue Mode/调度） | OK | **Queue Mode 架构：main 只处理 timer/webhook 生成执行 ID → Redis 队列（Bull）→ worker 消费执行，写回数据库**；**EXECUTIONS_MODE=queue + Redis broker + Postgres**；**更新顺序纪律：先停全部 workers → 停 main → 重启 main → 再拉 workers（防 ghost triggers 重复触发）**；**EXECUTIONS_TIMEOUT 限制单次执行时长（限制 ghost execution 伤害）**；**清理 stale Bull jobs：redis-cli KEYS "bull:n8n*"**；**N8N_ENCRYPTION_KEY 所有 worker 必须相同**；**规模判据：<1,000 执行/天 Regular；1,000-10,000 Queue 2-3 workers；>10,000 auto-scaling；关键任务 multi-main HA**；**dev/prod 分离 + workflow 版本化（Git/JSON 导出）** |
| 3 | LangFlow（Prompt/评估） | OK | **Prompt Template 组件：natural language + fixed values + dynamic variables**；**prompt 评估四陷阱：用调优数据评估会高估（holdout 测试集）/ 只测 happy path（评估集 ≥20% adversarial）/ 未校准的 judge / 不更新 golden dataset（每季度加 10-20 生产样例、退役平凡样例）**；**触发评估三时机：prompt 变更 / model 变更 / infrastructure 变更（检索索引/embedding/工具输出格式）**；**五步迭代法：minimal prompt → 跑 5-10 次（一次运行≠信号）→ 诊断失败模式 → 一次只改一个变量 → 版本化（prompt + test set + scoring rubric）**；**评估工具选型：Promptfoo（CI-friendly）/ LangSmith（LangGraph 近）/ Langfuse（开源自托管 EU/GDPR）/ DeepEval（pytest 原生）** |
| 4 | Activepieces（Agents/版本） | OK | **Agents 可复用、可对话、可放置（Reusable, Chattable, Yours to Place）：agent 不再是 flow step 里的设置包，而是命名/简报/对话/复用的一等公民**；**一句话建 agent（Agents page prompt box）**；**agent 嵌入 flow 作为 step，提供 prompt 让它知道执行什么；agent 可链式串联（chain together，每个处理不同环节）**；**Custom Tools：TypeScript 写自己的 integration**；**Pieces CI/CD：离线开发 → 增量 piece version（package.json）→ PR → merged 后 CLI 或 GitHub/GitLab Action 触发同步**；**Piece Builder Skill for AI coding agents（.agents/skills/piece-builder：Patterns/Triggers/Outputs/Build commands）** |
| 5 | Make（HTTP 模块） | OK | **HTTP 无 bundle 返回三法：子场景只负责 HTTP 调用（≥1 bundle 返回 webhook response 200；<1 bundle 返回错误码 + 主场景 BREAK error handler）**；**Bad Request 常见原因：required parameter 缺失或 null（尤其 iterator 映射的字段）**；**错误处理模式：HTTP module 右键 → Add error handler → Resume → Slack 通知，含 {{2.statusCode}} 和 {{2.data}}**；**429 rate-limit：检查响应头 Retry-After** |
| 6 | Pipedream（重放/触发器/Connect） | OK | **pd.flow.retry 暂停/恢复/重跑：外部服务 HTTP callback 回来后同一步处理（TIMEOUT 86400*1000）**；**trigger 事件字段：replay（boolean）/ trace_id（同一原始事件的所有执行共享同一值——跨执行追踪锚）/ ts / workflow_id**；**source 事件经 SSE 和 REST APIs 访问**；**Connect API 项目作用域：TypeScript/Python/Java SDK + REST API + OpenAPI spec**；**Connect CLI：安装 → 创建 project → OAuth client**；**list triggers API：GET /v1/connect/{project_id}/triggers（搜索+app 过滤）**；10,000+ 预建 + 3,000+ APIs proxy |
| 7 | Anthropic（Agent Skills 最佳实践） | OK | **frontmatter 强制两字段：name（≤64 字符、仅小写字母数字连字符、不能含 XML 标签、不能含保留词 "anthropic"/"claude"）+ description（非空、≤1024 字符、不能含 XML 标签、描述做什么和何时用）**；**可选字段：allowed-tools（无需询问即可用的工具）/ model（指定模型）/ license / compatibility / metadata.author**；**SKILL.md 膨胀拆分：mutually exclusive 或极少同用的上下文分开引用减少 token 用量**；**code 可同时当可执行工具和文档——明确 Claude 是直接跑脚本还是读进上下文参考**；**Think from Claude's perspective**；**keep it focused：多个聚焦技能比一个大技能组合性好；include examples（输入输出示例）；test incrementally**；**Skills 集成 Messages API 通过 code execution tool**；**自定义 skill 上传 zip 或单文件，创建返回 skill_* ID 引用** |
| 8 | GitHub（Agentic Workflows） | OK | **渐进启用：先低风险输出（comments/drafts/reports）再 PR creation；coding 先 goal-oriented（重构/测试覆盖/简化）再 feature work**；**report 指令具体定义 "good"（format/tone/links/when to stop）**；**2026-06-11 起无需 PAT：内置 GITHUB_TOKEN + Copilot 计费单一权限 flag**；**安全护栏：safe-outputs: staged: false→true 晋升线（Restraint/Injection resistance/Output quality/Cost 四判据）**；**token 优化：Optimizer 交叉比对 tool manifests 与实际调用剪掉未用 MCP tools（每调用省 8-12KB 上下文）；GitHub CLI 替代 GitHub MCP 做数据读取**；**Docker Sandboxes 作为 agent runtime（microVM 隔离 + network policy + secrets injection）**；**least-privilege：permissions: issues: write contents: read 而非 write-all**；**CI 失败自动调查：agent 分析日志/诊断根因/提修复 PR** |
| 9 | OpenClaw（ACP agents） | OK | **ACP = Agent Client Protocol：从任意 chat 界面 spawn/控制外部 coding harness（Claude Code/Codex/Gemini CLI/Cursor/Copilot）**；**/acp spawn codex、sessions_spawn(runtime: "acp", agentId: "codex")**；**/acp steer <id> <instruction>（向活动 agent 发新指令不新开会话）/ /acp attach <id>（把当前消息通道绑定到特定 ACP session 输出）**；**配置在 plugins.entries.acpx：acp.enabled / acp.dispatch.enabled / acp.backend（acpx）/ acp.allowedAgents / acp.maxConcurrentSessions（8）/ acp.stream.coalesceIdleMs（300）**；**persistent ACP bindings：/new 和 /reset 重置绑定 runtime**；**pluginToolsMcpBridge：让 Codex/Claude Code 调用 OpenClaw 插件工具（memory recall/store）**；**channel admission 后确保 ACP session 存在** |
| 10 | 技能市场生态（skills.sh/SkillsMP） | OK | **skills.sh：Vercel（vercel-labs）开源项目，MIT，2026 年初发布——"npm for Agent Skills"（CLI skills + web directory leaderboard）**；**安装 npx skills add <name>，跨 Claude Code/Codex CLI/Cursor/OpenClaw**；**规模：数百技能、410,000+ 总安装；top3：find-skills（1.5M installs）/ frontend-design（420K）**；**find-skills 技能（900K+ 周安装）**；**四大 marketplace：Skills.sh / Claude Skills Registry / Hugging Face Skills Hub / Microsoft Copilot Studio Skills Marketplace**；**SKILL.md 格式成为新 wire protocol（"Agent Skills Are the New APIs"）**；**SkillsMP：跨平台聚合器（mostly forks/mirrors）80,000+ 条目索引、无自有安装命令**；**maketocreate 数据：skills.sh 目录 650+ skills；claudemarketplaces.com ~6,700 entries**；**skill-creator（anthropics/skills）：创建/修改/评估技能、evals、variance analysis、优化 description 触发准确率** |

## 判重（双键检索，增量判定）
- Dify 错误处理（r286A 编排、r286B RAG、r286C Agent）→ 节点错误处理三选/变量引用格式 新面 → **新面**
- n8n Queue Mode（r286B 已落"部署 headless runtime/worker/Redis 队列"）→ 重叠约 60%，增量=更新顺序纪律（先停 worker 防 ghost triggers）/EXECUTIONS_TIMEOUT/Bull 清理/N8N_ENCRYPTION_KEY 一致/规模判据（≥40%） → **合并保留增量**
- Prompt 评估（r286A 上下文工程、r285A 提示词编排）→ 评估四陷阱/golden dataset 季度更新/触发三时机 新面 → **新面**
- Activepieces Agents（r285C MCP 760+、r286C tool search）→ Agents 可复用可对话/一句话建 agent/chain/Pieces CI/CD 新面 → **新面**
- Make HTTP 错误（r285A 场景蓝图、r286C AI Toolkit）→ HTTP 无 bundle 子场景三法/error handler Resume/429 Retry-After 新面 → **新面**
- Pipedream trace_id（r286A 触发器、r286C 事件源独立）→ trace_id 跨执行追踪/pd.flow.retry/Connect 项目作用域 新面 → **新面**
- Anthropic Skills frontmatter（r285B Skills 结构、r286B Skills API/触发双诊）→ 重叠约 60%，增量=frontmatter 硬约束（name≤64 禁保留词/allowed-tools/model 可选字段）/膨胀拆分法（≥40%） → **合并保留增量**
- GitHub Agentic Workflows（r285C MCP server、r286C Copilot 安全）→ 渐进启用/GITHUB_TOKEN/token 优化（剪 MCP tools 省 8-12KB）/Docker sandbox 新面 → **新面**
- OpenClaw ACP（r286A ACP 会话、r286C slash 命令）→ 重叠约 65%，增量=/acp steer /acp attach/plugins.entries.acpx 配置族/pluginToolsMcpBridge（≥40%） → **合并保留增量**
- skills.sh 生态（r286B 已落"技能市场四层生态 + npx skills add"）→ 重叠约 60%，增量=skills.sh 规模数据（410K installs/find-skills 1.5M/四大 marketplace）/SKILL.md 新 wire protocol/SkillsMP 聚合器定位（≥40%） → **合并保留增量**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 节点内建错误处理与变量引用纪律 | 工作流 |
| 2 | n8n Queue Mode 更新顺序纪律（合并增量） | 工具 |
| 3 | 提示词评估四陷阱与触发时机 | 可复用 Skill |
| 4 | Activepieces Agents 可复用与 Pieces CI/CD | 工作流 |
| 5 | Make HTTP 模块错误处理模式 | 工具 |
| 6 | Pipedream trace_id 跨执行追踪 | 工具 |
| 7 | Anthropic Skills frontmatter 硬约束（合并增量） | 可复用 Skill |
| 8 | GitHub Agentic Workflows 渐进启用与 token 优化 | 工作流 |
| 9 | OpenClaw ACP 三命令与配置（合并增量） | 工具 |
| 10 | skills.sh 生态规模与 find-skills（合并增量） | 可复用 Skill |

## 复核
十独点均有当日实拉来源；6 新面 + 4 合并保留增量（增量均≥40%），零纯重复。版本建议 3.73.0。