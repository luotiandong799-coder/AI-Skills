# 学习轮 r199-A：Pipedream事件源消费模型与ClaudeCode技能调用控制矩阵与全家桶技能仓与图像技能宿主适配与决策型压缩插件（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/application-design | 死链 |
| 2 | docs.langflow.org/concepts | 死链 |
| 3 | activepieces.com/docs/agents/agent-skills | 死链 |
| 4 | make.com/en/help/scenarios/scenario-inspector | fetch error |
| 5 | pipedream.com/docs/sources | OK 全文 |
| 6 | docs.anthropic.com/en/docs/claude-code/skills | OK 全文 8135 字 |
| 7 | skills.sh/trending | OK（190 项全列表） |
| 8 | skillsmp.com/skills/page/3 | OK（#201-235） |
| 9 | docs.openclaw.ai/concepts | 死链 |
| 10 | GitHub 生态（搜索） | OK |

## 独点（5 个）
### A1：Pipedream event source 消费模型——事件流可转 API，HTTP source 即请求 bin（来源：docs.pipedream.com/sources）
- event source 独立于 workflow 的资源：一个 source 可触发**多个 workflow**；**事件可用三种方式在平台外消费**：实时 SSE stream / CLI `pd events` / 批量 REST API——"把事件流变成 API"。
- **HTTP source = 可管理 API 的请求 bin**：创建得唯一 HTTP endpoint，任何请求可查 payload/headers，用 REST API 或 SSE 消费。
- **cron source = 用 event source 跑任何 Node 代码定时调度**，轮询外部 API 发事件（Airtable 无 webhook 就每几分钟 poll）。
- **Test Events 三源**：最近事件自动抓（最多 50）/ 在应用中手动产生真实事件 / 静态 sample（硬编码代表数据 + Modify Test Event 定制 + Reset 重置）；测试事件是端到端测 workflow 的前提，没有它 builder 里没法测。
- 限制：source 默认 timeout 5min、memory 256MB 固定。
- 判据：**触发器不只触发 workflow，还能被程序化消费**——REST/SSE 是事件源的"第二出口"；开发 workflow 先保证有 test event。
- **提升层**：工作流 / 工具。

### A2：Claude Code 技能调用控制矩阵——两个 frontmatter 字段定"谁能调"，custom commands 已并入技能（来源：docs.anthropic.com/en/docs/claude-code/skills）
- **调用控制两字段四象限**：`disable-model-invocation: true`（只有人能调，副作用操作如 /deploy /send-slack-message 用——Claude 不会因为你代码看起来好了就部署）；`user-invocable: false`（只有 Claude 能调，后台知识如 legacy-system-context——`/名字` 无意义动作）；默认双可。
- **custom commands 已并入 skills**：`.claude/commands/deploy.md` 与 `.claude/skills/deploy/SKILL.md` 都生成 `/deploy` 行为一致；技能增加支持文件目录 + 调用控制 + 自动加载；同名时 skill 优先。
- **技能层级**：enterprise > personal > project（同名高优先级覆盖）；plugin 用 `plugin-name:skill-name` 命名空间不冲突；**monorepo 嵌套自动发现**（`packages/frontend/.claude/skills/`）。
- **字符串替换**：`$ARGUMENTS` / `$ARGUMENTS[N]` / `$N` / `${CLAUDE_SESSION_ID}` / **`${CLAUDE_SKILL_DIR}`**（bash 注入时引用技能自带脚本，不依赖 cwd）。
- **allowed-tools 免问白名单**：激活时这些工具不用问权限；另有 `context: fork`（fork 子代理上下文跑复杂技能，不占主线）。
- **Bundled /batch**：跨代码库并行大改，分解 5-30 独立单元，批准后**每单元一个后台 agent + 隔离 git worktree + 各开 PR**；/simplify 派 3 个 review agent 并行聚合。
- 判据：**"技能该由谁触发"是显式设计不是默认**——有副作用的禁模型自动调，后台知识禁用户手动调；引用自身文件用 ${CLAUDE_SKILL_DIR} 不赌 cwd。
- **提升层**：可复用 Skill（调用控制）。

### A3：skills.sh Trending 揭示"全家桶技能仓"——官方/编程/营销/中文内容四大家（来源：skills.sh/trending 190 项全量）
- **anthropics/skills 官方 14 项**：pdf/pptx/xlsx/docx/webapp-testing/mcp-builder/canvas-design/doc-coauthoring/web-artifacts-builder/theme-factory/algorithmic-art/brand-guidelines/template-skill/internal-comms/slack-gif-creator——官方把办公文档/Web artifact 做成技能集。
- **wshobson/agents 22 项通用编程模式**：typescript-advanced-types/python-performance-optimization/api-design-principles/architecture-patterns/nextjs-app-router-patterns/nodejs-backend-patterns/prompt-engineering-patterns/postgresql-table-design/e2e-testing-patterns/mobile-ios/mobile-android/dotnet-backend 等——按语言/框架/测试分层全覆盖。
- **coreyhaines31/marketingskills 25 项营销 CRO 全家桶**：seo-audit/copywriting/marketing-psychology/pricing-strategy/social-content/form-cro/paywall-upgrade-cro/ab-test-setup 等——页面转化优化流程化。
- **jimliu/baoyu-skills 13 项中文内容创作**：image-gen/slide-deck/infographic/comic/xhs-images/post-to-wechat/post-to-x/compress-image 等。
- obra/superpowers 14 项软件工程流程（brainstorming→writing-plans→executing-plans→requesting-code-review→verification-before-completion）；另有 karpathy-guidelines（forrestchang）、skill-creator（anthropics）、audit-website（squirrelscan）上榜。
- 判据：**"技能市场"头部已被"成套卖的技能包"占据**——单技能 vs 全家桶是两种商品形态；装技能先看它属于哪个体系，体系内自洽度更高。
- **提升层**：生态观察。

### A4：图像生成技能按宿主能力三模式适配——有工具本地跑/没工具当提示词引擎/全无当顾问（来源：skillsmp #211 gpt-image-2, ConardLi/garden-skills 12,561★）
- 三模式：(A) Garden 本地模式——宿主有 OpenAI 兼容接口直接出图落盘；(B) Host-Native 模式——宿主有自带图像工具时，技能只做**提示词工程引擎**，渲染好 prompt 交给宿主工具；(C) Advisor 模式——宿主无任何图像工具时退化为**高质量 prompt 顾问**。18 大类 80+ 结构化模板（海报/UI/产品/信息图/学术/架构图/漫画/头像/分镜/IP 周边/编辑工作流）。
- 同页其他强技能：**CLI-Anything（HKUDS, 49,636★）258 命令 FreeCAD harness**（全 workbench 覆盖、headless 导出 8 格式）；editaplot（本地 Origin 自动出可编辑图）；jianying-editor（剪映 AI 自动化封装 3,373★）；nature-skills（paper-card 论文精读卡 + 论文转专利 43,560★）。
- 判据：**可复用技能要能在宿主能力光谱上降级**——有工具执行、没工具当指引、全无当顾问；否则技能在弱宿主上直接不可用。
- **提升层**：可复用 Skill（宿主适配）。

### A5：GitHub 生态——决策型压缩插件 + 混合架构代码审查（来源：GitHub 生态搜索）
- **fast-jev-compaction（tamaratran, +3,204/周）**：Claude Code 插件**用 Jev 决策替换 compaction 摘要**——压缩不是"总结对话"而是"提取决策"，与 wb-context-compressor 的"结论优先低损折叠"同源的外部验证。
- **alibaba/open-code-review（40,356★, +4,330）**：混合架构代码审查——确定性流水线 + LLM Agent、line-level 评论、内置多语言规则集（NPE 等），在阿里规模 battle-tested。
- Understand-Anything（+5,600/天）多 agent 管线把代码库转成交互知识图谱 + React dashboard；codebase-memory-mcp 41,536★（停止每个问题重读仓库）；ECC 265,784★ harness 优化系统。
- 判据：**压缩/记忆类问题的解是"保留决策而非复述内容"**；代码审查的有效形态是确定性规则 + LLM 判断混合，纯 LLM 或纯规则都不够。
- **提升层**：工作流 / 工具。

## 判重说明
- A1 → r198-C C2 已记 sources 独立资源/KV/deduping；本页首次拉，REST/SSE/CLI 消费 + HTTP source 请求 bin + cron source + test events 三源 + 5min/256MB 为独有增量。
- A2 → r198-C C1 已记 best-practices（创作方法/500 行/三模型）；本页首次拉，调用控制两字段 + commands 并入 + 层级 + ${CLAUDE_SKILL_DIR} + allowed-tools + bundled /batch 为独有增量。
- A3 → r198-C C3 已记 Hot 榜厂商入场；/trending 页首次拉，四大家全家桶清单为独有增量。
- A4 → r197-B 已记 skillleaderboard 类榜单；garden-skills 三模式首次拉，宿主适配思想为独有增量。
- A5 → r198-A/B 已记 GitHub 生态多 repo；fast-jev-compaction + open-code-review 首次见，决策型压缩 + 混合审查为独有增量。
