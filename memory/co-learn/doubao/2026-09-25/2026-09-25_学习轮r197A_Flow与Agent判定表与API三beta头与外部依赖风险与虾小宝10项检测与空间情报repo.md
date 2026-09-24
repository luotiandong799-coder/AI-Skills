# 学习轮 r197-A：Flow与Agent判定表与API三beta头与外部依赖风险与虾小宝10项检测与空间情报repo（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/knowledge-base | 死链 |
| 2 | docs.n8n.io/code/cookbook | 目录壳 |
| 3 | docs.langflow.org/components | OK |
| 4 | activepieces.com/docs/agents/overview | OK |
| 5 | make.com/en/help/scenarios/scenario-settings | 标题壳 |
| 6 | docs.anthropic.com agent-skills/overview | OK 全文 |
| 7 | skills.sh/categories | 死链 |
| 8 | ai.skillatlas.cn（虾小宝） | OK |
| 9 | docs.openclaw.ai/automations | 死链 |
| 10 | GitHub Trending（robots 禁走搜索） | OK |

## 独点（5 个）
### A1：Flow vs Agent 判定表——逻辑写一次 vs 每次现算（来源：activepieces.com/docs/agents/overview）
- Flow：逻辑写一次、同输入同步骤、适合已知流程；Agent：每次运行现读情境选工具、同输入可不同处理、适合多变工作；agent 属于一个 project，project 决定它能碰的连接/flow/文件，move 前弹窗告知会破坏什么。
- 判据：**知道步骤用 Flow，不知道步骤用 Agent**；agent 权限边界=project 边界。
- **提升层**：Agent 编排。

### A2：Claude API 用 Skills 需要三个 beta headers + /v1/skills 上传（来源：docs.anthropic.com agent-skills/overview）
- API 用 pre-built/custom skills 必须带：`code-execution-2025-08-25` + `skills-2025-10-02` + `files-api-2025-04-14` 三个 beta header；custom skills 走 `/v1/skills` API 上传，workspace 级共享；claude.ai 上传 zip 个人级不共享不 org 管理。
- 判据：**跨面不同步 + 共享范围三档**（claude.ai 个人 / API workspace / Claude Code 文件级）。
- **提升层**：可复用 Skill（分发）。

### A3：外部 URL 依赖是 Skill 安全短板——可信 skill 也会被依赖变化攻陷（来源：docs.anthropic.com overview 安全节）
- 从外部 URL fetch 内容的 skill 特别危险：fetched content 可能含恶意指令；**即使可信 skill，外部依赖随时间变化也会被攻陷**；Skill 不在 ZDR 覆盖范围。
- 判据：**审 skill = 审它的依赖**——SKILL.md/scripts/镜像全查，异常网络调用/文件访问/与声明不符的操作都是红旗。
- **提升层**：安全/工具。

### A4：虾小宝自主审计工具——10 项安全风险检测 + 依赖项扫描（来源：ai.skillatlas.cn）
- 在 r195-C 三层认证（安全/完整/可执行）之上，新增自主审计工具：技能安全检测（检测 10 项安全风险、识别恶意行为与危险操作）+ 技能依赖项扫描（分析代码依赖/运行环境/外部资源声明完整性）；Skill 评测与自进化"敬请期待"。
- 判据：**审计已从认证扩展到 10 项风险 + 依赖扫描**——装 skill 前先跑检测。
- **提升层**：工具。

### A5：GitHub 生态新信号——空间情报 / 成长型 agent / Dify workflow 合集（来源：GitHub Trending 走搜索）
- bilawalsidhu/gods-eye-view 4.06 万★/月：浏览器内真实数据间谍卫星模拟器；NousResearch/hermes-agent 24.79 万★："agent that grows with you"；n8n-io/n8n 20.53 万★/400+ 集成；svcvit/Awesome-Dify-Workflow 1.08 万★。
- 判据：**垂直场景（空间情报/成长型个人 agent）+ 工作流合集正在霸榜**。
- **提升层**：生态观察。

## 判重说明
- A1 → r196-B 已记 Activepieces 三构件嵌套；取 Flow/Agent 判定表 + project 边界增量。
- A2/A3 → r195-A 已记跨面不同步 + runtime 差异；取三 beta headers + 外部 URL 依赖风险增量。
- A4 → r195-C 已记三层认证；取 10 项检测 + 依赖扫描增量。
- A5 → r196-A 已记科学技能库/google-ax；取 gods-eye-view/hermes-agent/Awesome-Dify 增量。
