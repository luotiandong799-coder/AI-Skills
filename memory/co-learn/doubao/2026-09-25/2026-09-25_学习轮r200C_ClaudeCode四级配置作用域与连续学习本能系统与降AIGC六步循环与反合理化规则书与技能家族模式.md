# 学习轮 r200-C：ClaudeCode四级配置作用域与连续学习本能系统与降AIGC六步循环与反合理化规则书与技能家族模式（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/rag/ | 死链 |
| 2 | docs.n8n.io/executions/ | 死链 |
| 3 | docs.langflow.org/ | OK 全文（Langflow 1.11.x 概览） |
| 4 | make.com/en/help/modules/ | fetch error |
| 5 | pipedream.com/docs/components/quickstart/ | OK 全文（Pipedream Registry） |
| 6 | docs.anthropic.com/en/docs/claude-code/settings | OK 全文 17493 字 |
| 7 | skills.sh/trending | OK 全文（190 项） |
| 8 | skillsmp.com/skills/page/8 | OK（#701-736） |
| 9 | WaytoAGI（搜索《通往AGI之路》更新） | OK |
| 10 | GitHub 生态（neodrop/agentconn 搜索） | OK |

## 独点（5 个）
### C1：Claude Code 配置四级作用域 + managed-settings.d 合并语义 + autoMemory 防重定向（来源：docs.anthropic.com/en/docs/claude-code/settings 全文）
- **四级 scope**：Managed（server/plist/registry/系统 managed-settings.json，全机器，IT 部署，**不可被任何东西覆盖**）> User（~/.claude/）> Project（.claude/ 进 git 共享团队）> Local（.claude/settings.local.json gitignored）；优先级链 Managed > 命令行参数 > Local > Project > User。**权限规则例外：不覆盖而是跨 scope 合并**（allow/ask/deny 全部并集）。
- **managed-settings.d/ drop-in 目录**（systemd 约定）：base 先合并，目录内 *.json 按字母序叠上；**数字前缀控制合并顺序**（10-telemetry.json / 20-security.json）；数组拼接去重、对象深合并、`.` 开头文件忽略——多团队各自部署策略片段而不用共编一个文件。
- **autoMemoryDirectory 不接受 project/local settings**——克隆仓库能塞 .claude/settings.json 把记忆写入敏感位置，所以该键只从 policy/user/--settings 接受（防重定向攻击的显式设计）；autoMemoryEnabled 可用 CLAUDE_CODE_DISABLE_AUTO_MEMORY 关。
- **autoMode 分类器**：environment/allow/soft_deny/hard_deny 四数组 prose 规则，`"$defaults"` 字符串继承内置规则；managed 专属安全键：allowedMcpServers（denylist 优先）/allowManagedPermissionRulesOnly（禁用户定义权限规则）/blockedMarketplaces/strictKnownMarketplaces/allowedChannelPlugins。
- 配置自动时间戳备份保留 5 份防数据丢失；Windows managed 路径 `C:\Program Files\ClaudeCode\`（旧 ProgramData 路径 v2.1.75 起弃用）。
- 判据：**配置是"作用域 × 合并语义 × 安全例外"三件事**——权限合并不覆盖、记忆目录防克隆仓库重定向、drop-in 目录按前缀叠；安全键全部只在 managed 层生效。
- **提升层**：工具。

### C2：连续学习本能系统 + 视频蒸馏成 Skill（来源：skillsmp #705 + WaytoAGI《通往AGI之路》更新）
- **continuous-learning-v2（ECC）**：**基于本能的持续学习系统**——通过 hooks 观察会话 → 创建**原子本能（instincts）+ 置信度评分** → 进化成 skills/commands/agents；**v2.1 加 project-scoped instincts 防跨项目污染**（项目 A 的经验不污染项目 B）。与学习留痕机制同源的外部正式化，且补了"本能 → 置信度 → 晋升为技能"的成长路径 + 跨项目隔离。
- **awesome-seedance（WaytoAGI 更新，卡尔开源）**：**463 个 AI 视频案例复现、评分、分类**，整理成开源项目，沉淀出**可直接改写的提示语模板和 AI 视频 Skills**——"案例 → 复现 → 评分分类 → 蒸馏成模板/Skills"是一条可复制的技能沉淀流水线。
- 判据：**学习产物的晋升路径是"本能→置信度→技能"三级**且要按项目隔离；批量案例先复现评分再蒸馏成模板，优于逐个手工学。
- **提升层**：可复用 Skill / 工作流。

### C3：降 AIGC 六步循环 + 水印溯源诚实声明（来源：skillsmp #724 de-aigc-skills）
- **de-aigc-skills（3,709★）**：学术论文降 AI 味——**六步循环**：intake → audit → **claim-evidence check（主张-证据核对）** → differentiated rewrite（差异化改写）→ **five-dimension self-score（五维自评）** → cold-reader recheck（冷读者复查）；22 英文 + 17 中文双模式库；逐节策略；**硬保护：每个数字、系数、引用原样保留**。
- **水印溯源层（2026-08 起）**：确定性、CJK 安全的不可见字符载体 + 文件元数据清理（docx/png/jpg/svg/pdf 含 C2PA）；诚实说明 Claude 统计水印；作者"所有权通行证"——**永不声称文本无痕**。
- 判据：**降 AI 味是"审→证→改→自评→复核"循环不是一次改写**；数据/引用是硬保护不参与改写；去水印要诚实——清理了什么、不能保证什么，写清楚。
- **提升层**：可复用 Skill。

### C4：反合理化规则书 + 诚实披露缺陷（来源：neodrop 评测 + agentconn《Agent Skills Are the New Dotfiles》）
- **anti-rationalization tables（45,400★/77,500 installs，3 周）**：**规则书预判 AI agent 跳过 spec/测试/评审的每条捷径**——把"跳过计划""跳过测试""跳过 review"的合理化借口逐条列成表，模型碰见借口即返回对应硬规则；目标 = 给 coding agent 一本"它无法忽略的规则书"。
- **诚实披露**：README 明确列出 2 个未解决 routing bugs + context-bloat 上限——**披露缺陷成为可信度的构成部分**（不是只报优点）。
- 生态数据：GitHub Trending 前 8 有 5 个是 agent infra；obra/superpowers 252k、mattpocock/skills 165k（+10.8k/周）、addyosmani/agent-skills 77k——三仓合计近 50 万星；skillleaderboard 追踪 36.4k skills、30 天 +529k stars。
- 判据：**对抗"合理化跳过"要列逐条借口→规则映射表**，不是一句"必须遵守纪律"；公开已知缺陷 + 限制边界 = 可信度资产。
- **提升层**：可复用 Skill / 输出。

### C5：技能家族模式 + 技能评判技能 + 榜单结构（来源：skills.sh/trending 190 项 + skillsmp）
- **作者级技能家族**：softaworks/agent-toolkit 通用家族（humanizer/skill-judge/reducing-entropy/session-handoff/plugin-forge/command-creator/dependency-updater）、antfu/skills（vue 生态 20+：vite/vue/pinia/vitest/tsdown/turborepo）、wshobson/agents（前后端+测试+API 模式库）、coreyhaines31/marketingskills（CRO 全家：page-cro/signup-flow-cro/paywall-upgrade-cro/form-cro/popup-cro/ab-test-setup）——**一个作者用一个仓库覆盖一个领域的完整技能矩阵**，比散装单技能好发现、好维护。
- **skill-judge（agent-toolkit）**：评判技能质量的技能——技能开发流程里"评测技能"本身技能化（与 wb-skill-authoring"闭合邻域评测"同主题的外部实现）。
- 榜单结构：trending 190 项按 installs 排序；anthropics/skills 官方技能稳定在列（frontend-design/pdf/pptx/xlsx/docx/webapp-testing/mcp-builder/canvas-design）；Karpathy 规则已技能化（karpathy-guidelines）。
- 判据：**判断一个技能生态成熟度看"家族仓库 vs 散装"**；技能质量评测有专用技能；官方仓（anthropics/skills）是稳定基线。
- **提升层**：生态观察。

## 判重说明
- C1 → r199-C C3 已记 MCP 三 scope/allowlist；settings 页首次拉全，四级 scope 优先级 + drop-in 合并语义 + autoMemory 防重定向 + 权限跨 scope 合并且为独有增量。
- C2 → r196/r197 已记记忆分层/连续学习相关（wb 侧 r159 记忆三态等）；continuous-learning-v2 + 视频蒸馏成 Skill 首次见，本能-置信度晋升 + 项目隔离 + 463 视频流水线为独有增量。
- C3 → r199-C 已记 anti-defensive-writing（叙事定位）；de-aigc 首次见，六步循环 + claim-evidence 核对 + 数字硬保护 + 水印溯源诚实声明为独有增量。
- C4 → r197/r198 已记多篇执行纪律/规则；anti-rationalization tables + 诚实披露缺陷首次见。
- C5 → r199-A 已记 skills.sh trending 家族仓（anthropics/wshobson/marketing/baoyu/obra）；softaworks 家族 + skill-judge + CRO 全家 + 作者家族模式为独有增量。
