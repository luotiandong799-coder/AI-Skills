# 学习轮 r206-A：Anthropic技能官方页增量与GitHub agent生态多仓与Dify聊天构建Agent与OpenClaw网关架构与superpowers闭环（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.langflow.org/（1946 全） | OK（tweaks 运行时覆盖/单组件隔离测试，低增量） |
| 2 | skills.sh/trending（190 项） | OK（superpowers/softaworks/anthropics 系列） |
| 3 | deepseek-plugin.org/plugins | fetch error（死链，下轮换 offset 分页格式重试） |
| 4 | general_search GitHub Trending agent 生态 | OK（AX DevOps/Grok Build/orca/BrowserSkill） |
| 5 | docs.anthropic.com/en/docs/claude-code/skills（3994/8135） | OK（skill/command 合并+新字段+替换+双控） |
| 6 | docs.openclaw.ai/ 根页（3464/4862） | OK（trusted gateway 架构/多通道/multi-agent routing） |
| 7 | blog.n8n.io/agents/ | 死链 |
| 8 | dify.ai/blog（3498/176413） | OK（New Agent 聊天构建/自动技能） |
| 9 | make.com/en/help/ai | fetch error（死链） |
| 10 | waytoagi.com/ 根页（3149/80421） | OK（精选工具分类，低增量） |
| 11 | docs.openclaw.ai/agents/context | 死链 |

## 独点（5 个）
### U1：Anthropic skills 官方页增量：skill/command 合并+四级位置+新 frontmatter+替换变量+双控矩阵（来源：docs.anthropic.com skills 页 2026-09-25 实拉，r204-C P1/P3 与 r205-C T1 的官方页增量）
- **Custom commands 已并入 skills**：`.claude/commands/deploy.md` 与 `.claude/skills/deploy/SKILL.md` 都创建 `/deploy` 同样工作；旧 commands 兼容，**同名时 skill 优先于 command**。
- **四级位置+优先级**：enterprise > personal（~/.claude/skills/）> project（.claude/skills/）> plugin（**plugin-name:skill-name 命名空间**不冲突）；同名高级别覆盖。
- **monorepo 嵌套发现**：`packages/frontend/.claude/skills/` 编辑该目录文件时自动发现——每个包自己的技能。
- **--add-dir 的 skills 自动加载+live change detection**（会话中编辑无需重启）；其 CLAUDE.md 需环境变量才加载。
- **frontmatter 新字段（r205-C spec 之外）**：argument-hint（自动补全提示 [issue-number]）/ model（激活时模型）/ effort（low-medium-high-max）/ context: fork（fork 子代理上下文）/ agent（fork 时选 subagent 类型）/ **hooks（skill 生命周期 hooks）**。
- **String substitutions**：$ARGUMENTS / $ARGUMENTS[N] / $N / ${CLAUDE_SESSION_ID}（会话日志/会话文件/输出关联）/${CLAUDE_SKILL_DIR}（bash 注入引用 skill 捆绑脚本，不受 cwd 影响）。
- **双控矩阵**：disable-model-invocation=true 仅你触发（deploy/commit/send-slack-message 副作用——"不想 Claude 因为代码看起来准备好了就决定部署"）；user-invocable=false 仅 Claude 触发（legacy-system-context 背景知识）。
- 判据：**有副作用的技能默认只许人触发**；背景知识技能默认只许模型加载；路径引用用 ${CLAUDE_SKILL_DIR} 不靠 cwd。
- **提升层**：可复用 Skill。

### U2：GitHub agent 生态多仓：AX 三件套与 Society of Mind 与 fleet 编排与真实浏览器（来源：general_search GitHub Trending/agentconn/trendshift 2026-09-25）
- **Google AX DevOps agent**：开源分布式运行时编排自主 agent 工作负载——**sandboxing/checkpointing/network fencing 三件套**（隔离/断点/网络围栏）。
- **Grok Build（xAI）**：**8 并行 agent 代码生成，Multi-agent "Society of Mind" 架构**（分工写作-评审聚合）。
- **orca（stablyai）**：ADE（agent development environment）for fleet of parallel agents——**用自己的订阅跑任意 coding agent**（桌面/移动/远端）。
- **BrowserSkill（Tencent）**：CLI+browser 扩展让 agent 用**真实已登录浏览器不打断你工作**。
- **mastra（★28k TS）**：现代 TS 框架 for AI-powered apps/agents。
- 判据：**并行 agent 要隔离执行域**；agent 用你的真实浏览器省去登录态维护。
- **提升层**：工具 / 工作流。

### U3：Dify New Agent：聊天构建+自动技能沉淀+上下文保持（来源：dify.ai/blog《Introducing New Agent》2026-08-27）
- **Build agents by chatting**：自然语言描述→Dify 自动生成可复用 skills，**对话中保持上下文**；就绪后**并入 workflow 成为更大流程的一环**。
- **三层落地路径**：standalone app / 加入 workflow / 复用沉淀技能。
- 与 r205-C T2（skill induction 课程方法论）互补：T2 是原理（traces→人批准技能），U3 是产品化实现（聊天即沉淀）。
- 判据：**构建 agent 的副产品就是可复用技能**——对话过程自动沉淀，不另写文档。
- **提升层**：工作流 / 工具。

### U4：OpenClaw 网关架构：trusted gateway + untrusted execution + deterministic policy（来源：docs.openclaw.ai 根页 2026-09-25）
- **Trusted gateway**：会话/路由/通道连接的单一事实源（single source of truth）。
- **Untrusted execution**：agent 执行环境与网关分离。
- **Deterministic policy**：策略确定性，不靠 prompt 软约束。
- **Multi-agent routing**：per agent/workspace/sender 隔离会话；一网关多通道（Discord/iMessage/Signal/Slack/Telegram/WhatsApp/WebChat）；ClawHub 插件市场；Mobile nodes 相机/屏幕/语音。
- 判据：**网关管状态、执行环境不可信、策略用代码写死**——三分离才谈得上多通道常驻。
- **提升层**：工作流 / 架构。

### U5：superpowers 计划-执行-验证-评审闭环 + session-handoff（来源：skills.sh/trending 2026-09-25）
- **obra/superpowers 方法论包**：brainstorming→writing-plans→executing-plans→**verification-before-completion（交付前验证）**→requesting-code-review/receiving-code-review→subagent-driven-development；配套 using-git-worktrees/dispatching-parallel-agents/finishing-a-development-branch。
- **softaworks/agent-toolkit**：session-handoff（会话交接）/reducing-entropy（降低系统熵）/feedback-mastery/skill-judge/dependency-updater/humanizer。
- **anthropics/skills 官方**：mcp-builder（MCP 构建）/canvas-design/doc-coauthoring/web-artifacts-builder。
- **安装**：`npx skills add <owner/repo>` 单命令。
- 判据：**写计划→执行→验证→评审是标准闭环**；会话交接让换 agent 不断线。
- **提升层**：可复用 Skill / 工作流。

## 判重说明
- U1 → r204-C P1（skills 机制）/P3（SKILL.md 硬约束）+ r205-C T1（官方 spec）：同源；**新字段 argument-hint/model/effort/hooks、替换变量、双控矩阵、四级位置优先级、skill/command 合并**为独有增量，合并落地。
- U2 → 无既有 agent 生态多仓记录（r205-B S4 是 gh skill 管理），落。
- U3 → r205-C T2 互补（方法论 vs 产品化），保留增量落。
- U4 → r205-B S3（OpenClaw 自动化六机制）互补（机制 vs 架构），落。
- U5 → r204-A N3（行为保持重构）与 r205-C T5（系统变更评估）无闭环组合；superpowers 计划-执行-验证-评审为独有组合，落。
- 未落：Langflow tweaks（弱）、WaytoAGI 工具分类（弱）、deepseek-plugin/Make/n8n/openclaw context 死链。
