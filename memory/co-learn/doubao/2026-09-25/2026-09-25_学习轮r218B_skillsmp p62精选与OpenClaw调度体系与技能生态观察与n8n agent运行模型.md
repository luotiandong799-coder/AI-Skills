# 学习轮 r218B：skillsmp p62精选与OpenClaw调度体系与技能生态观察与n8n agent运行模型（2026-09-25）

## 实拉记录（10 次调用，7 成功 / 3 死链计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/62（#6101-6151，5900/11339 取） | OK |
| 2 | dify.ai/blog 续读（118816-123288） | OK（Workflow File Upload/Cross-Platform Copywriting） |
| 3 | www.langflow.org/（4240/20182） | OK（Langflow 1.12/组件类示例） |
| 4 | docs.n8n.io/what-agents-do.md（667B） | OK（agent 多次运行模型） |
| 5 | GitHub Trending 搜索（CSDN 周报/gaojihao/llmnews/agskills.dev） | OK（技能能力包时代/OpenSpec） |
| 6 | deeplearning.ai/articles/ | robots 禁（累积 5 次，换入口） |
| 7 | docs.openclaw.ai/automation/cron-jobs（1076B 索引） | OK（调度器/standing orders/inbound webhooks） |
| 8 | activepieces.com/docs/getting-started/what-is-activepieces | 死链 |
| 9 | skills.sh/how-it-works | 死链（skills.sh 累积 4 次） |
| 10 | agentskills.io/overview（offset 0） | 死链（agentskills 累积 3 次，疑似改版） |

## 独点（4 个）
### B1：skillsmp p62 精选：候选池机制 / AI 味实证规律 / 术语先 grounded / 财务长文 fact-check（来源：skillsmp.com/skills/page/62，2026-09-25 实拉）
- **cheat-trends（XBuilderLAB/cheat-on-content ★7,112）**：**从配置热点源（HN/Reddit/YouTube trending/B 站热门）抓今天热门话题——去重+粗打分+写入 candidates.md；"绝大部分人没有候选池——这是让'我没素材'问题在 onboarding 第二步就消失的钥匙"**（选题候选池机制）。
- **aigc-down-skill（Yezery ★245）**：**降低中文学术写作 AIGC 检测率的实证规律（真实改写实验 AIGC 率 >50% 降至 11%）**——检测修复典型模式：理论依据式起笔、套路结尾、整齐并列句、模板化问题陈述、被动分析套话、过度对称、画蛇添足总结句、模糊归因、滥用 AI 高频词。
- **writing-beats（vinvcn/mattpocock-skills-zh-CN ★4,362）**：**把原始素材组装成节拍旅程——在某个 beat 依赖一个术语之前先把它 grounded（先立术语再引用）**。
- **deep-company-series（HKUDS/Vibe-Trading ★33,795）**：8 部分公司深度系列（~120k words）——**核心 IP 是 REVISING 而非写作：严格 fact-check checklist 抓 pseudo-precision（概率加权预期/第三方 MAU 出入/线性外推）、绝对语言、跨篇数字不一致**。
- **pdf-translate（L27z18328742 ★65）**：PDF 英译中用 PDFMathTranslate-next（pdf2zh）——monolingual 中文 PDF+bilingual 对照 PDF、公式图表版式保留、uv 自动装环境、复用已配置模型/API、无 key 回退免费 SiliconFlow。
- **提升层**：工作流 / 可复用 Skill。

### B2：OpenClaw automations 调度体系：one-shot reminder / standing orders / inbound webhooks（来源：docs.openclaw.ai/automation/cron-jobs，2026-09-25 实拉）
- **automations=内置调度器**：持久化 jobs、按时唤醒 agent、可交付到 chat channel/webhook/无处；`openclaw automations` CLI（`openclaw cron` 为别名）。
- **one-shot reminder 模式**：`openclaw automations create "<ISO time>" --name X --session main --system-event "..." --wake now --delete-after-run`——**一次性任务跑完自动删除**。
- **Standing orders=定时运行所依据的操作授权**（the operating authority a scheduled run acts under）；**Standing intents=事件触发替代调度**（event-triggered work instead of a schedule）。
- **Inbound webhooks**：Gateway HTTP hooks——`POST /hooks/wake`（唤醒）、`POST /hooks/agent`（agent 执行）、`POST /hooks/<name>`（mapped hooks）；Gmail 可走 PubSub 触发（restricted Gmail reader 推荐）。
- **执行可覆盖**：`--model`/`--thinking`/`--light-context`/`--tools`/`--fallbacks`/`--message` agent-turn 选项；main vs current vs isolated vs custom 会话执行样式（isolated=fresh session）。
- **提升层**：工作流（自动化体系）。

### B3：GitHub 技能生态观察：Agent Skills 能力包时代 / 安全验证技能注册表（来源：GitHub Trending 搜索，2026-09-25 实拉）
- **Agent Skills 进入能力包时代**（CSDN 37 周周报）：openai/skills、anthropics/skills 集中上线——**行业焦点从单体 Agent 转向可组合、版本化、可审计的技能模块**；Skills 把提示词、工具调用、权限、业务流程封装成独立资产，适配企业复用与治理；GitHub Explore 新增 agent skills 标签。
- **tech-leads-club/agent-skills（+1,759★/月）**：**secure、validated 的技能注册表——extend Antigravity/Claude Code/Cursor/Copilot**（技能分发信任模型）。
- **Fission-AI/OpenSpec（★70,239）**：Spec-driven development (SDD) for AI coding assistants（spec 驱动开发，与既有 wb-spec-driven 同族观察）。
- **提升层**：工具 / 可复用 Skill（技能治理）。

### B4：n8n agent 多次运行模型：agent=会做决策的 chain（来源：docs.n8n.io/build/integrate-ai/understand-ai-components/what-agents-do.md，2026-09-25 实拉）
- **agent=会做决策的 chain**：chain 遵循预定调用序列；**agent 用 LLM 决定采取哪些动作**（决策者）。
- **agent 多次运行**：执行含 agent 的工作流时 agent 会跑多次——initial setup → 一次 run 调用工具 → 又一次 run 评估工具响应并回复用户（三次心智模型）。
- **n8n 一个 Agent node** 按设置可作不同类型 agent。
- **提升层**：工作流（agent 编排心智）。

## 判重说明
- B1 全新（p62 独有），落。
- B2 openclaw 增量（automation 索引页，r217 只落 cron 记账判据），落。
- B3 trending 增量（技能封装资产化生态观察），落。
- B4 n8n 增量（what-agents-do 新页），落。
- 未落：langflow 官网营销页（实质有限）、dify Workflow File Upload/Cross-Platform Copywriting（节点技巧与既有 dify 点重叠>60%）、activepieces what-is（死链）。
