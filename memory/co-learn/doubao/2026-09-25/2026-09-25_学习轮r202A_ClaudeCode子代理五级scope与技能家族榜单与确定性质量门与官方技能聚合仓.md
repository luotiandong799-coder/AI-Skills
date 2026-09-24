# 学习轮 r202-A：ClaudeCode子代理五级scope与技能家族榜单与确定性质量门与官方技能聚合仓（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/application-orchestrate/ | 死链 |
| 2 | docs.n8n.io/hosting/ | OK（完整原文已下载，导航为主、正文弱） |
| 3 | docs.langflow.org/api-reference/ | 死链 |
| 4 | make.com/en/help/functions | fetch error |
| 5 | pipedream.com/docs/workflows/steps/code/ | 死链 |
| 6 | docs.anthropic.com/en/docs/claude-code/sub-agents | OK 全文 13044 字 |
| 7 | skills.sh/trending | OK 2143 字（190 项榜单） |
| 8 | skillsmp.com/skills/page/12 | OK（#1101-1136） |
| 9 | deepseek-plugin.org/official | 死链 |
| 10 | GitHub 生态（awesome-agent-skills 搜索） | OK |

## 独点（4 个）
### G1：Claude Code 子代理体系：五级 scope 优先级 + 身份=name + 插件子代理三字段忽略（来源：docs.anthropic.com/en/docs/claude-code/sub-agents 全文）
- **子代理的用途判据**：side task 会淹没主对话（搜索/日志/文件内容不会再引用）→ 子代理在自己上下文做、只返回摘要；**每次用同样指令派同样 worker → 定义自定义子代理**。
- **内置子代理**：Explore（Haiku + 只读工具，**thoroughness 三档 quick/medium/very thorough**）/ Plan（plan mode 研究，**防无限嵌套——子代理不能再生子代理**）/ general-purpose（全工具）/ statusline-setup / claude-code-guide。
- **五级 scope + 优先级**：Managed settings（组织级，1 最高）→ --agents CLI flag（当前会话，2，JSON 定义可测）→ .claude/agents/（项目，3）→ ~/.claude/agents/（用户，4）→ Plugin agents/（5 最低）。
- **身份 = name frontmatter，子目录不影响识别**；**同 scope 内同名静默丢弃一个（无警告）**——name 全树唯一；插件内子目录成为 scoped identifier（my-plugin:review:security）。
- **插件子代理安全限制**：不支持 hooks/mcpServers/permissionMode 三个字段（加载时忽略）——要这些能力必须复制进 .claude/agents/。
- **frontmatter 完整字段**：name/description（必填）+ tools/disallowedTools/model/permissionMode/mcpServers/hooks/maxTurns/skills/initialPrompt/memory/effort/background/isolation/color——**isolation: worktree 给子代理隔离仓库副本**；**User scope 持久记忆目录 ~/.claude/agent-memory/**（跨会话累积 codebase patterns 与重复问题）。
- **agent teams 可引用子代理类型**：teammate 用其 tools/model，定义 body 附加进 teammate system prompt。
- 判据：**子代理是上下文隔离单元**（只回摘要不回过程）；身份与路径解耦、同名必须全局唯一；不可信来源（插件）的子代理要削权（禁 hooks/MCP/permission）。
- **提升层**：可复用 Skill / 工具。

### G2：技能家族集中趋势：厂商/作者级技能家族成为分发主流（来源：skills.sh/trending 190 项实证）
- **技能家族清单（本次榜单实证）**：anthropics/skills 15 个（frontend-design/pdf/pptx/xlsx/docx/webapp-testing/mcp-builder/canvas-design/doc-coauthoring/web-artifacts-builder/theme-factory/algorithmic-art/brand-guidelines/template-skill/internal-comms/slack-gif-creator）；obra/superpowers 14 个（brainstorming/systematic-debugging/test-driven-development/writing-plans/executing-plans/requesting-code-review/subagent-driven-development/using-superpowers/writing-skills/verification-before-completion/using-git-worktrees/receiving-code-review/dispatching-parallel-agents/finishing-a-development-branch）；antfu/skills 16+（vite/vue/vitest/unocss/nuxt/tsdown/vitepress/turborepo/slidev/pinia/pnpm/antfu）；coreyhaines31/marketingskills 20+（seo-audit/copywriting/marketing-psychology/programmatic-seo/launch-strategy/pricing-strategy/competitor-alternatives 等）；softaworks/agent-toolkit 30+（humanizer/skill-judge/commit-work/c4-architecture 等）；jimliu/baoyu-skills 中文 10+（baoyu-image-gen/slide-deck/article-illustrator/infographic/cover-image/xhs-images/post-to-wechat/compress-image 等）；wshobson/agents 20+；expo/skills；vercel-labs（find-skills/react-best-practices/web-design-guidelines/agent-browser）。
- **superpowers 家族特征**：writing-plans→executing-plans→requesting-code-review→receiving-code-review→verification-before-completion→finishing-a-development-branch——**同一工作流不同阶段各一个技能、按序引用**（管线式技能家族）。
- 判据：**选技能先看家族**——同一作者/厂商成体系技能（可配套使用、命名一致）优先于孤立单技能；榜单顶部被家族占据是生态成熟信号。
- **提升层**：生态观察 / 可复用 Skill。

### G3：确定性质量门脚本化：质量门不靠模型自觉 + 体检模式 + Stage 0 逐项询问（来源：skillsmp #1101/#1104/#1110）
- **novel-outline（eternityspring/shuohao-skills）**：小说→短剧大纲五件套（改编说明/人物表/爽点表/分集梗概/资产清单）+ outline.json + Markdown + 单页评审报告；**14 道质量门全部由脚本确定性检查**（角色分档上限、主场景上限随集数动态、爽点间隔≤3 集、每集钩子悬念必填）——"**不靠模型自觉**"；**体检模式：贴现成大纲只跑质量门给诊断**（不重做）；零依赖零 API key。
- **scipilot-writing-skill**：学术写作**质量证据链**——每次交付前强制跑 scripts/writing_lint.py 机器自检（AI 指纹词/机械连接词/悬垂 -ing/破折号滥用/否定式平行/空泛归因/模型名所有格/LaTeX 转义/中文全角标点/被动比例/句长节奏）+ AI 审稿人视角自审闭环（最多 3 轮）；**Stage 0 主动逐项询问**（任务类型/文本载体 .tex/.docx/.md/纯文本/目标期刊/语言方向/学科/修改保守度）——"**禁止默默假设**"。
- **ai-regression-testing（ECC）**：AI 辅助开发回归测试——**sandbox-mode API 测试免数据库依赖** + 自动化 bug-check 工作流 + **捕捉 AI 盲点：同一个模型写代码又评审代码**。
- **product-marketing（coreyhaines）**：创建 `.agents/product-marketing.md` 上下文文档作为**产品/受众/定位单点事实源**，所有其他营销技能引用它——避免跨任务重复基础信息。
- 判据：**质量门做成可跑脚本（确定性检查）而非提示词（依赖模型自觉）**；诊断/体检模式与生产模式分开；开始前逐项询问影响产出的参数，不默默假设。
- **提升层**：可复用 Skill / 工作流。

### G4：官方技能聚合仓：30+ 厂商 1500+ 技能单仓库（来源：awesome-agent-skills VoltAgent 搜索）
- **VoltAgent/awesome-agent-skills**：30+ 厂商**官方技能**聚合单仓库，1500+ 技能，31,800+ stars / 3,400+ forks——"Agent Skills 生态最受贡献的参考点"（官方技能 vs 社区杂货的分发层级）。
- **antigravity-awesome-skills**：1445+ 技能库（Claude Code/Gemini CLI/Cursor/Copilot/Antigravity 多平台）+ npm installer。
- **philipbankier/awesome-agent-skills**：跨平台 curated（MCP servers/Agent Skills/Cursor rules 混合）。
- **nanoskill 精选 9 技能**：skill 编写/网页应用测试/完成前验证/系统化调试/并行 agent 调度——"训练 agent 的最佳技能集"。
- 判据：**技能分发的信任分层：官方聚合 > 社区精选 > 个人仓库**；选技能优先查官方聚合仓（质量保证 + 跨平台兼容）；技能库要有 npm installer（安装即用）。
- **提升层**：生态观察。

## 判重说明
- G1 → r199-C 已记"Claude Code 子代理体系"（浅）；sub-agents 页 13044 字首次拉全，五级 scope 优先级 + name 唯一性 + 插件子代理三字段忽略 + Explore 三档 + 不能嵌套 + agent-memory 持久目录 + worktree isolation 为独有增量（≥40%）。
- G2 → r198-B 记"厂商技能仓库入场"、r200-C 记"作者级技能家族模式"（概念）；本次 skills.sh/trending 190 项榜单实证家族清单（anthropics 15/obra 14/antfu 16/marketingskills 20/softaworks 30/baoyu 10）+ 管线式家族（writing-plans→…→finishing-branch）为独有增量，合并保留。
- G3 → wb-artifact-verification 已有验证机制；"质量门=脚本确定性检查不靠模型自觉 + 体检模式 + Stage 0 逐项询问 + 单点事实源文件"为独有增量。
- G4 → r199-B 记 VoltAgent 厂商联合仓（概念）；1500+ 技能具体规模 + 31,800 stars + antigravity 1445+ 多平台 + npm installer 为独有增量，合并保留。
