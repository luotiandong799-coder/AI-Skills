# 学习轮 r198-C：Anthropic SKILL最佳实践与Pipedream组件架构与厂商技能仓库入场与DSH插件生态（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/agent | 死链 |
| 2 | docs.n8n.io/templates | 死链 |
| 3 | docs.langflow.org/deployment | 死链 |
| 4 | activepieces.com/docs/actions/overview | 死链 |
| 5 | make.com/en/help/functions | 标题壳 |
| 6 | pipedream.com/docs/components | OK 全文 |
| 7 | docs.anthropic.com agent-skills/best-practices | OK 全文 |
| 8 | skills.sh/hot | OK（49KB 全文下载读全） |
| 9 | huggingface.co/spaces | 安全策略拦截 |
| 10 | GitHub AI 生态（robots 禁走搜索） | OK |

## 独点（4 个）
### C1：Anthropic SKILL.md 官方最佳实践——Claude A 建 / Claude B 测的迭代法 + 硬性规格（来源：docs.anthropic.com agent-skills/best-practices）
- **命名**：名词短语或动作式（pdf-processing / process-pdfs），禁 vague/通用词/保留字；**description 必须第三人称**（description 注入 system prompt，视角不一致破坏发现）且含"做什么+何时用"；frontmatter 硬校验：name≤64 字符（小写/数字/连字符）、description≤1024 字符、无 XML 标签。
- **SKILL.md 正文 <500 行**，超限拆文件；progressive disclosure 两模式：高层引导+引用（FORMS.md/REFERENCE.md 按需加载）/ 领域组织（finance.md/sales.md 分开避免加载无关上下文）。
- **迭代法（observe-refine-test）**：用 Claude A 创建/精修 skill，Claude B（新实例加载 skill）做真实任务测试，观察 B 哪里卡/漏/偏 → 带具体观察回 A 改（如"忘了过滤测试账户，规则不够突出，用 MUST 措辞"）→ 再测。逐条基于真实 agent 行为而非假设。
- **脚本纪律**：utility scripts 优于让 Claude 现写（更可靠/省 token/一致）；脚本**自己处理错误不甩给 Claude**（solve don't punt）；禁 voodoo constants（每个值要有注释理由）；假设包已装是反模式（写明 pip install）。
- **测试检查清单**：至少 3 个 evals；**用 Haiku/Sonnet/Opus 三模型测**；真实使用场景测试 + 团队反馈。
- 判据：**skill 是"作者(A)设计-使用者(B)验证"的产物，改 skill 必须带观察证据回炉**；正文 500 行是官方性能上限。
- **提升层**：可复用 Skill（创作方法）。

### C2：Pipedream Components 架构——sources 可独立当 serverless 函数 + Verified 评审制（来源：docs.pipedream.com/components）
- Components=Node.js 模块跑 serverless，**3,000+ apps 托管 auth、npm 包免安装**；两类：sources（可实例化为独立资源，可当触发器**也可当 standalone serverless 函数**；支持 HTTP/timer/cron 触发、props 输入、内置 KV store、内置 deduping strategies、可被 API 消费）/ actions（只能 workflow 内当步骤，可 return JSON）。
- **Verified Components 走 GitHub PR 评审制**（可信、统一模式、Pipedream 支持）；社区组件不评审不入选 curated；private 发布仅自己/团队可见，Unpublish 永久需谨慎。
- 判据：**触发器组件 = 独立资源（可单独部署/单独调 API 消费事件），动作组件 = 流程内步骤——边界清晰才能组合**；"Verified"是一种平台背书信号。
- **提升层**：工作流/工具。

### C3：skills.sh Hot 实时榜——厂商官方技能仓库大规模入场 + 安全审计技能（来源：skills.sh/hot 全文 49KB）
- All Time 总量 **91,623 skills**；Hot 榜（1H 变化）：find-skills(vercel-labs) +829、vercel-react +163、microsoft-foundry +198、supabase-postgres +85、deploy-to-vercel +47、remotion-best-practices +146、using-superpowers(obra) +101、wecomcli-manage-doc(腾讯企业微信 CLI, 594 总安装) +99、skill-vetter(useai-pro/openclaw-skills-security) +25。
- **厂商官方技能仓库集中入场**：vercel-labs、microsoft/azure-skills(4.6K)、supabase、expo、flutter、cloudflare、hashicorp、redis、antfu/skills、tavily-ai、greensock/gsap-skills(149)、firecrawl/cli(208)、github/awesome-copilot（大量）、**火山引擎 skills.volces.com（byted-web-search +17 / iga-pages +8）**、bytedance/agentkit-samples（byted-las-pdf-parse-doubao +5）、openclaw 系（awesome-openclaw-skills）、mattpocock/skills（grill-me +25 同名信号）。
- 判据：**技能市场进入"官方入场"阶段——头部框架/云厂商/大厂发自己的 skill 仓做事实标准**；新装技能优先看厂商源+安全审计（skill-vetter 类）双校验。
- **提升层**：生态观察。

### C4：GitHub 生态——Everything is a Plugin 与科学技能库（来源：GitHub 生态走搜索）
- deepseek-harness **234,602★（+38,794/30d）**："Everything is a Plugin"哲学；scientific-agent-skills 46,008★（190,000+ 科学家、165 个 validated 技能 + 100+ 科学数据库）；archify 70,817★（+54,890）；AgentConn 四层 stack 分析（agent/agent-skills/skills marketplace/harness）；AI gateway：一个端点 359 providers（150+ free）、1200+ 模型、quota-aware auto-fallback、RTK+Caveman 压缩省 15-95% token。
- 判据：**插件化是 harness 层的核心抽象（一切皆插件）；科学/垂直域技能库已到 46k★ 规模证明"技能包"商业与生态双成立**。
- **提升层**：生态观察。

## 判重说明
- C1 → r195-C/r196-B 已记 progressive disclosure 三阶段与 50+ 客户端；best-practices 页首次真拉，Claude A/B 迭代法 + 500 行 + 三模型测试 + frontmatter 硬校验增量。
- C2 → r196-A 已记 Pipedream 快速测试/挂起恢复；components 架构页首次真拉，sources 独立资源 + Verified 评审制增量。
- C3 → r197-C 已记 all-time 榜头部；/hot 页首次真拉，厂商入场 + 火山引擎/腾讯 wecom + skill-vetter 增量。
- C4 → r198-A/B 已记 GitHub 生态多 repo；deepseek-harness 23 万★ + scientific-agent-skills 46k★ 增量。
