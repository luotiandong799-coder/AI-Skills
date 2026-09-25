# 学习轮 r209-B：Anthropic skills官方页完整版与subagents管理与skillsmp p32 UI调查（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/32（#3101-3145） | OK（ui-walkthrough/enrich-context 等） |
| 2 | docs.anthropic.com/claude-code/skills（0-5000） | OK（bundled skills/commands 合并/dynamic injection） |
| 3 | docs.n8n.io/advanced-ai/ | OK（导航+Cluster nodes，低方法） |
| 4 | docs.activepieces.com 根 | fetch error（死链记录） |
| 5 | anthropic skills 续读（5000-8135 全取完） | OK（权限三法/描述预算/visual output） |
| 6 | dify.ai/blog 列表续读（0-3498） | OK（New Agent 聊天建 agent，低方法） |
| 7 | docs.pipedream.com 根 | OK（source-available 组件注册表，与 r207B 重叠确认） |
| 8 | general_search WaytoAGI | OK（Skills 蓝皮书线索，低方法） |
| 9 | docs.anthropic.com/claude-code/subagents（全 2546B） | OK（/agents 管理/链式/工具继承） |
| 10 | make.com/en/help | OK（导航低内容） |

## 独点（3 个）
### B1：Anthropic skills 官方页完整版：bundled skills 与动态上下文注入与描述预算（来源：docs.anthropic.com/claude-code/skills 全 8135B，2026-09-25 实拉；与 r204C 机制细则/r205C spec 页互补的官方实现层）
- **Custom commands 已合并进 skills**：`.claude/commands/deploy.md` 与 `.claude/skills/deploy/SKILL.md` 都创建 `/deploy` 且行为一致；旧 commands 文件继续工作；skill 与 command 同名时 **skill 优先**。
- **Bundled skills 五件套**：`/batch`（跨代码库并行大规模改动：研究→分解 5-30 独立单元→计划获批→每单元后台 agent 在**隔离 git worktree** 实现→测试→开 PR）；`/claude-api`（按语言加载 API 参考，import anthropic 自动激活）；`/debug`（读会话 debug 日志排障）；`/loop [interval]`（会话内按间隔重复跑 prompt：轮询部署/babysit PR）；`/simplify`（最近改动文件**三并行评审 agent** 聚合发现并修复）。
- **动态上下文注入 `` !`cmd` ``**：skill 内容发给 Claude **之前**先执行 shell 命令，输出替换占位符（预处理，不是 Claude 执行）——PR 摘要 skill 用 `!`gh pr diff` 等取实时数据；内容含 **ultrathink** 关键词启用 extended thinking。
- **skill 描述预算（上下文管理新方法）**：skill 描述加载进上下文让 Claude 知道有什么；**预算动态 = 上下文窗口 2%，fallback 16,000 字符**；超限技能被排除（/context 查警告）；`SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量可覆盖——技能库膨胀时的硬治理开关。
- **invocation 控制矩阵**：disable-model-invocation=true（仅用户可调，description 不进上下文）；user-invocable=false（仅 Claude 可调，description 常驻）；描述常驻、全文调用时加载。
- **权限三法**：deny `Skill` tool 全部禁用；`Skill(commit)`/`Skill(review-pr *)` 精确/前缀规则允许或拒绝；disable-model-invocation 隐藏单个。
- **skill↔subagent 双向组合**：context: fork（系统 prompt=agent 类型，task=SKILL.md 内容，另载 CLAUDE.md）vs subagent 带 skills 字段（系统 prompt=subagent 正文，预载 skills+CLAUDE.md）。
- 判据：**技能库大了用描述预算开关治理**；批量改动走 /batch worktree 并行；动态数据用 !`cmd` 预处理注入。
- **提升层**：工具 / 工作流 / 可复用 Skill。

### B2：skillsmp p32：ui-walkthrough 全状态 UI 调查与 enrich-context 业务上下文缺口目录（来源：skillsmp.com/skills/page/32 #3101-3145，2026-09-25 实拉）
- **ui-walkthrough（全 UI 调查流程）**：枚举当前分支 feature 的**每个视图和状态**——空/填充/加载/错误、每个 dialog/menu/panel、响应式断点、light+dark+RTL；stubbed Playwright harness 捕获；拼成**单图 HTML walkthrough 带全局 light/dark 切换滑块**；跑两轮评审（视觉/一致性：对齐、间距、专业度、明暗一致性、对比、截断 + UX/易用性：流程、可发现性、affordance、空/错误态、预期）；`--fix` 自动应用安全前端修复并重捕获；`--theme` 限定主题、`--no-rtl` 跳过 RTL。判据：**UI 验收=枚举全部状态快照+双维度评审，不靠肉眼抽查**。
- **enrich-context（业务上下文十类缺口目录）**：给 DB schema 带不来的语义补上下文——枚举值含义、单位（USD vs cents、ms vs sec）、NULL 语义、魔法哨兵（-1=unknown）、软删除默认过滤、业务同义词、时间粒度/TZ 约定、跨系统标识符、货币规则、规范表偏好、命名聚合指标（ARR/churn/DAU/NRR）propose 为 cubes；**grill/auto-pilot 双模式**（一次一问用户驱动 vs agent 推断应用、仅冲突和高爆炸半径新增上报）；读 raw/ 下全部材料（PDF/词汇表/手册/代码/数据字典），按**十类缺口目录+cube 提案流**填洞，写回正确 sink。
- **refine-prompt（提示工程纪律）**：refine 用户 prompt 输出改写版+简要理由，**从不执行 prompt**——提示工程与执行解耦。
- **hypothesis-generation（证据约束假设）**：从观察/初步发现生成**证据有界的**科学问题、候选假设、竞争解释、因果/关联主张、判别性预测、测量、preregistration 就绪分析计划——**不把假设当事实**（与用户对话规则 1 同源）。
- 附：document-skills umbrella（伞形 skill 分发到最具体文档 skill 降噪）、benchmark（性能基线/PR 前后回归检测/栈替代比较）。
- **提升层**：工作流 / 可复用 Skill。

### B3：Anthropic subagents 官方页：/agents 交互管理与工具继承与链式（来源：docs.anthropic.com/claude-code/subagents 全 2546B，2026-09-25 实拉；与 r202A 五级 scope 互补的实操层）
- **文件格式与管理**：subagent = Markdown + YAML frontmatter（`.claude/agents/` 项目级优先 / `~/.claude/agents/` 用户级）；字段 name（小写连字符）/description/tools；**tools 省略=继承主线程全部工具含 MCP**，指定=粒度控制；`/agents` 交互式命令管理（查看内置/用户/项目、创建/编辑/删除、**重复时显示哪个激活**）。
- **鼓励主动委托**：description 里加 **"use PROACTIVELY" / "MUST BE USED"** 提高自动委托频率——触发词影响路由。
- **链式 subagent**：复杂流程可链式调用（先 code-analyzer 找性能问题再用 optimizer 修）。
- **最佳实践**：Claude 生成初始 agent 再个性化迭代；**单一职责**（一个 subagent 只做一件事，可预测性更高）；详细 prompt（指令+示例+约束）；**限制工具**（只授必要工具，安全+聚焦）；项目级 subagent 进版本控制团队共享。
- **性能**：子代理每次以干净上下文启动（保留主上下文、延长会话，但首次需自建上下文有延迟）。
- 判据：**subagent 建"人设"用文件+frontmatter，路由靠 description 触发词**；工具默认继承、按需收紧。
- **提升层**：工具 / 可复用 Skill。

## 判重说明
- B1 → r204C（Anthropic skills 机制细则）/r205C（AgentSkills spec）同域但本页为 **Claude Code 官方实现层新内容**（bundled skills 五件套/dynamic context injection/描述预算 2%/commands 合并/Skill() 权限规则），增量 >60%，落。
- B2 → 新（ui-walkthrough 全状态调查/enrich-context 十类缺口/refine-prompt 永不执行），落。
- B3 → r202A 子代理五级 scope 同族，但官方页实操层（/agents 命令/tools 继承/PROACTIVELY/链式/单一职责）为独有增量，合并保留增量落地。
- 未落：dify New Agent（低方法）、Pipedream 根（r207B 重叠确认）、n8n advanced-ai（导航）、Make help（导航）、Activepieces 根（死链）、WaytoAGI（蓝皮书线索低方法）。
