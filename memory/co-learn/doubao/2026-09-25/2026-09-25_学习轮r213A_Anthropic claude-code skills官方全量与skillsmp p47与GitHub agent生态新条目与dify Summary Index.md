# 学习轮 r213-A：Anthropic claude-code/skills 官方全量与skillsmp p47与GitHub agent生态新条目与dify Summary Index（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/47（#4601-4651，5916/11699 取） | OK（oh-my-issues/learning-to-learn/29-dropshipping 等） |
| 2 | dify.ai/blog 续读（37625-43212） | OK（Summary Index/Prompt as spec/GraphRAG 集成） |
| 3 | docs.anthropic.com claude-code/skills（5996/8135 取） | OK（调用控制/字符串替换/位置分层/预算） |
| 4 | docs.langflow.org 根（1946B 全，v1.11.x） | OK（中方法，与 r212-B 已拉重复） |
| 5 | pipedream.com（4320/21308 取） | OK（10,000+ tools / 3,000+ APIs / MCP remote server） |
| 6 | github.com/trending 续读（offset 12457） | 死链（link fetch error，计数） |
| 7 | deeplearning.ai/short-courses 续读（offset 9101-13450） | OK（On-Device Memory/Adaptive AI Agents） |
| 8 | agentmore.chatglm.cn（1029B 全） | OK（官网直拉确认定位，无增量） |
| 9 | general_search GitHub agent 生态（trending 替代） | OK（书→技能转化/npx skills add/herdr/Bumblebee） |
| 10 | docs.anthropic.com claude-code/skills 剩余段（offset 5996-8135 全读完） | OK（codebase-visualizer 示例/描述预算/Troubleshooting） |

## 独点（4 个）
### A1：Anthropic claude-code/skills 官方页全量：调用控制三态 / 字符串替换 / 位置分层 / 描述预算（来源：docs.anthropic.com/en/docs/claude-code/skills，2026-09-25 实拉；与 r212-A A1、r212-B B2 同源，本页 Claude Code 技能配置全量+预算数字增量 ≥40% 落）
- **Custom commands 已合并进 skills**：`.claude/commands/deploy.md` 和 `.claude/skills/deploy/SKILL.md` 都创建 `/deploy` 且行为相同；skill 与 command 同名时 skill 优先。
- **调用控制三态表（写 Skill 必查）**：默认=双方可调（description 常载 context、触发时全量加载）；`disable-model-invocation: true`=只有人可调（description 不入 context，适合 /deploy /commit 等副作用流程）；`user-invocable: false`=只有 Claude 可调（背景知识如 legacy-system-context）。
- **位置分层**：Enterprise（managed settings）> Personal `~/.claude/skills/` > Project `.claude/skills/` > Plugin（`plugin-name:skill-name` 命名空间，不与各层冲突）；**嵌套目录自动发现**（编辑 `packages/frontend/` 文件时同时找 `packages/frontend/.claude/skills/`，monorepo 支持）。
- **字符串替换**：`$ARGUMENTS` / `$ARGUMENTS[N]` / `$N` 简写 / `${CLAUDE_SESSION_ID}` / `${CLAUDE_SKILL_DIR}`（bash 注入引用脚本时用，不依赖当前工作目录）。
- **动态上下文注入**：`` !`<command>` `` 语法——skill 内容发给 Claude **前**运行 shell 命令，输出替换占位符（预处理，不是 Claude 执行）；"ultrathink" 关键词启用 extended thinking。
- **context: fork 子 agent 执行**：skill 内容成为子 agent 的 prompt；`agent` 字段选 Explore/Plan/general-purpose 或自定义（如 deep-research skill 用 Explore agent）。
- **技能描述字符预算（官方数字）**：skill descriptions 载入 context 的预算**动态为 context window 的 2%，fallback 16,000 字符**；`/context` 查被排除警告；`SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量覆盖。
- **frontmatter 完整字段**：name/description/argument-hint/disable-model-invocation/user-invocable/allowed-tools/model/effort/context/hooks。
- **提升层**：可复用 Skill（authoring 完整参考）。

### A2：skillsmp p47 精选：issue 按根因聚类 / 学习方法论 / 子技能路由边界（来源：skillsmp.com/skills/page/47，2026-09-25 实拉）
- **oh-my-issues（thedotmack/claude-mem ★94,424）**：**按根因把 GitHub issue 积压聚类成少量 plan-master issues**——标准化评论重定向子 issue、架构修复 PR 原子性闭合整个 cluster（"issue 聚类治理"：几十个表象报告归到少数共享根因）。
- **learning-to-learn（THU-MAIC/OpenMAIC ★38,274）**：概念中心课堂里并行注入学习策略与元认知——**检索练习、自我解释、预测后反馈、监控理解、刻意复习、生产性失败**（学习方法论，与用户"内化好方法"偏好同向）。
- **29-dropshipping-mastery-global（minhnv0807/ai-business-skills ★586）**：12 阶段端到端管道；**Not for 边界写进 description 做子技能路由**（ad copy 见 05 / product page 见 12 / account audit 见 21 / pricing 见 17）——"大技能拆子技能+路由"范例。
- **apology-letter（mohitagw15856/pm-claude-skills ★1,320）**：真诚道歉结构=承认+担责+共情+具体修复+预防+补救提议，无借口/无伪道歉。
- **ad-agency-performance-master（swaylq/master-skill ★132）**：广告外包绩效管理——**创意/知识工作"不可量化 vs 必须可考核"元矛盾**、KPI/OKR/BSC/360/MBO/KSF/积分制/提成制对比、分岗位绩效（创意最难量化/媒介最易量化）。
- **pptx-reference-deck-analysis（wshobson/agents ★39,856）**：参考 PPTX **只读分析**（结构/主题/字体/版式节奏/诊断/衍生模板目录/安全 OOXML 包检查）——"参考分析不改文件"。
- **提升层**：可复用 Skill / 工作流。

### A3：GitHub agent 生态新条目：书→Agent 技能自动转化 / npx skills add / 新工具（来源：general_search GitHub agent 生态，2026-09-25 实拉；trending offset 死链以搜索替代，不绕过）
- **书→Agent 技能自动转化工具（HelloGitHub 2026-09-25）**：把技术书籍和文档**自动生成 SKILL.md + 按章节拆分文件 + 术语表 + 速查表**，Token 消耗比整本书进上下文**少 20-50 倍**，支持 PDF/EPUB/DOCX/Markdown——"书→技能"自动化（与 A3 轮 deep-learning-book 手动 delta 层互补：一个手动提炼、一个自动转化）。
- **anthropics/skills 官方安装命令**：`npx skills add https://github.com/anthropics/skills -skill web-artifacts-builder`（官方 skills 仓库按技能名安装）。
- **herdr（Rust ★40,115）**："the runtime your coding agents live on"。
- **Bumblebee（Perplexity）**：扫描依赖与 MCP server 的供应链威胁（与既有工具面安全同向）。
- **awesome-claude-skills**：1,000+ production-ready Claude Code skills/plugins。
- **mvanhorn/last30days-skill（周 +12,053）**：跨平台研究 Skill；**chopratejas/headroom（14,272）**：LLM Token 压缩。
- **提升层**：工具 / 工作流（书→技能可复用）。

### A4：Dify Summary Index + Pipedream MCP remote + Adaptive AI Agents（来源：dify blog / pipedream.com / deeplearning.ai，2026-09-25 实拉）
- **Dify 1.12.0 Summary Index**：**把摘要附加到 chunk，相关内容一起返回**——从碎片化检索到全上下文（RAG 增量：chunk+summary 联合返回）。
- **Prompt Engineering for Workflow-Ready LLM Apps**：**设计 prompts 作为产品规格（product specifications）**，让 LLM 产出稳定、可审计、结构化输出。
- **Pipedream = integration layer for AI agents**：**Managed auth + 10,000+ tools / 3,000+ APIs**；MCP client 连 `remote.mcp.pipedream.net`（x-pd-external-user-id header，agent 选工具 auth 已处理）——"工具即服务的 MCP 代理"。
- **Building Adaptive AI Agents（Oracle）**：agent 会话间不携带任何东西所以重复犯错——**三种修复：①agent traces→可复用、人批准的 skills 管道 ②代码知识图谱改善大代码库检索 ③知道何时适配模型本身**（traces→human-approved skill 是独有方法）。
- **提升层**：工作流 / 工具。

## 判重说明
- A1 → claude-code/skills 官方全量（调用控制三态/字符串替换/位置分层/描述预算 2%），与 overview 同源但本页增量 ≥40%，落。
- A2 → skillsmp p47 精选（issue 聚类/学习方法论/子技能路由），全新，落。
- A3 → GitHub agent 生态新条目（书→技能转化/npx skills add/herdr），同生态新条目增量，落。
- A4 → Dify Summary Index + Pipedream MCP + Adaptive AI Agents 三个小增量合并，落。
- 未落：Langflow 根页（与 r212-B 重复）、AgentMore 官网（无增量）、deeplearning.ai 课程目录（On-Device Memory 与既有记忆方法重复，低方法）、github trending 死链（已用搜索替代实拉）。
