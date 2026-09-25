# 学习轮 r210-A：Claude Code settings全量治理与TanStack ai沙箱与GitHub trending新条目（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/34（#3301-3353） | OK（ai-sandbox/review-duplication/seedance-antislop 等） |
| 2 | deepseek-plugin.org/tutorials | 死链（记录，不重试） |
| 3 | agskills.dev 续读 | offset 越界（total 8535 已取 3022，参数无效记录） |
| 4 | docs.anthropic.com/claude-code/settings（0-5000） | OK（四作用域/managed-settings.d） |
| 5 | anthropic settings 续读（5000-10993） | OK（skillListingBudgetFraction/worktree/sandbox） |
| 6 | dify.ai/blog/introducing-new-agent | 死链（记录） |
| 7 | skills.sh 续读（13380-18501） | OK（图片为主，低内容记录） |
| 8 | anthropic settings 续读（10993-17493 全取完） | OK（marketplace 七源/strictKnownMarketplaces/policyHelper） |
| 9 | general_search GitHub Trending 2026-09-25 | OK（headroom/scientific-agent-skills/ponytail +12.6k） |
| 10 | modelscope.cn/docs/intro | link parse error（记录） |

## 独点（4 个）
### A1：Claude Code settings 全量治理体系：作用域优先级链 / 数组跨作用域拼接 / 预算与折叠 / marketplace 策略前检查（来源：docs.anthropic.com/claude-code/settings 全 17493B，2026-09-25 实拉）
- **四作用域 + 完整优先级链**：Managed（server-managed > MDM/OS 策略 > file-based managed-settings.d + managed-settings.json > HKCU registry；**只用一个 managed source，不跨层合并**）> 命令行参数 > Local（.claude/settings.local.json gitignored）> Project（.claude/ 提交 git）> User（~/.claude/）。**数组设置跨作用域拼接去重而非覆盖**（sandbox.filesystem.allowWrite / permissions.allow 多源合并）。
- **managed-settings.d/ drop-in 目录（systemd 风格）**：base 合并后 *.json 按字母序合并；标量后者覆盖、数组拼接去重、对象深合并；数字前缀控制顺序（10-telemetry.json/20-security.json）——多团队独立下发策略片段无需协调编辑单文件。
- **权限评估顺序：deny 先 → ask → allow，第一个匹配获胜**；权限规则格式 `Tool(specifier)`（Bash(npm run *) / Read(./.env) / WebFetch(domain:example.com)）；ignorePatterns 已废弃改 permissions.deny。
- **skill 列表预算双控**：`maxSkillDescriptionChars`（单 skill 描述+when_to_use 字符上限，默认 1536）+ `skillListingBudgetFraction`（listing 占用上下文窗口比例，默认 0.01=1%）；**listing 超预算时最不常用 skill 描述折叠成裸名**（还能调用但看不到 why）；`/doctor` 显示截断数与受影响 skill；`skillOverrides`（on/name-only/user-invocable-only/off）**不改 SKILL.md 就隐藏/折叠**，/skills 菜单写入 settings.local.json。
- **marketplace 管理**：`strictKnownMarketplaces`（managed only）**enforced BEFORE network/filesystem ops（被拦源永不落盘）**，add/install/update/refresh/auto-update 全程检查——**策略设置前已添加的 marketplace 一旦不匹配 allowlist 也不能再用**；`extraKnownMarketplaces`（任意作用域）仓库级预注册+trust 提示安装；`enabledPlugins` 格式 `plugin@marketplace: true/false`，project 覆盖 user，managed force-enable 不可被 local 禁用；marketplace source 七型：github/git/url/npm/file/directory/hostPattern（regex）。
- **policyHelper 动态策略（fail-closed）**：管理员部署可执行文件在启动时计算 managed settings；stdout JSON envelope 的 settings 必须放 `managedSettings` key 下（**裸对象解析出 undefined 什么都不应用**）；helper 启动非零退出 → 拒绝启动（要弹性就从缓存 serve 并退出 0）。
- **沙箱 fail-closed**：`sandbox.enabled + failIfUnavailable` 起不来就报错退出（硬门禁）；`allowUnsandboxedCommands=false` 彻底禁用 dangerouslyDisableSandbox 逃生口；filesystem.allowRead **优先于 denyRead**（可建工作区只读白区）；network.deniedDomains 优先 allowedDomains；allowManagedDomainsOnly 只认 managed allowlist。
- **autoMemory 安全**：autoMemoryDirectory **只接受 policy/user/--settings，不接受 project/local**（克隆仓库可把记忆重定向到敏感位置）；defaultMode auto 在 project/local 被忽略（仓库不能自己授予自己 auto，v2.1.142 起）。
- **worktree 隔离**：baseRef fresh（origin 主干干净）vs head（含未推 commit）；symlinkDirectories（node_modules 符号链接防复制）；sparsePaths（sparse-checkout）；bgIsolation worktree 默认阻塞主 checkout Edit/Write 直到 EnterWorktree；`.worktreeinclude` 文件把 .env 等 gitignored 文件带进 worktree。
- 判据：**配置治理四问**——同一设置多源时按完整优先级链（含数组拼接语义）；技能库膨胀用 listing 预算+折叠+skillOverrides 而不是删技能；市场/插件准入走策略前检查；沙箱要 fail-closed 不静默降级。
- **提升层**：工具 / 可复用 Skill（配置治理 / 上下文预算 / 安全）。

### A2：TanStack ai-sandbox 声明式沙箱适配器 + 可移植快照（来源：skillsmp.com/skills/page/34 #3341 TanStack/ai ★3,127，2026-09-25 实拉）
- **harness 适配器入沙箱**：Claude Code/Codex/OpenCode 适配器跑在隔离沙箱内——`defineSandbox` + `withSandbox` + provider（localProcessSandbox / dockerSandbox）；`defineSandboxPolicy`（allow/ask/deny）声明式策略；SandboxHandle 暴露 fs/git/process。
- **声明式 provisioning**：`createSecrets` + secret/bearer、skills（agentSkill/gitSkill/mcpSkill/fileSkill）、plugins、instructions → **canonical AGENTS.md + 每 harness symlinks 投影**；shallow-clone 默认（depth opt-out）；serial/parallel setup callback 跑在持久 shell；snapshot-after-setup 默认 + snapshotMaxAge TTL。
- **可移植快照（portable snapshots）**：成功终端运行后 `withPersistence` 拿快照、`memorySandboxSnapshots` 存本地示例；`snapshots.save` 命名保存、`snapshots.fork` 从选中检查点分叉、`snapshots.readArtifact` 授权读产物——**沙箱状态可移植、可回放、可审计**。
- `defineWorkspace`（git/setup/scripts/skills/secrets/instructions/plugins）一站式定义工作区。
- 判据：**跑第三方/harness 代码进沙箱是默认不是可选**；沙箱快照化=失败可回放、产物可审计（与 wb-debug-loop"失败经验签名"互补）。
- **提升层**：工具 / 工作流。

### A3：GitHub trending 新条目：headroom 进 LLM 前压缩 / scientific-agent-skills 科学库 / ponytail 本周 +12.6k（来源：general_search GitHub Trending 2026-09-25 + dev.to/startupcorners/ngjoo 线索，2026-09-25 实拉）
- **headroomlabs-ai/headroom（★73,577，+122/天）**：**"Compress tool outputs, logs, files, and RAG chunks before they reach the LLM"**——工具输出/日志/文件/RAG 块进 LLM 前压缩（宣传 20x）——与 wb-context-compressor 直接同域，是"入口侧压缩"的具体工具形态。
- **K-Dense-AI/scientific-agent-skills（★40,962，+1,980/天）**：#1 Agent Skills Library for Science——**190,000+ 科学家使用、165 个 ready validated skills、100+ 科学数据库**（生物/化学/医学/drug discovery）——科学域已验证技能库的规模标杆。
- **tech-leads-club/agent-skills（★6,753，+1,759/月）**：secure, **validated skill registry** for professional AI coding agents——extend Antigravity/Claude Code/Cursor/Copilot——"已验证技能注册表"形态（与 r209-C C3 agskills 索引、caliper 评测同族）。
- **DietrichGebert/ponytail（★132.1k，本周 +12,598）**：代码思考 Agent skill——**用户功能套件 wb-ponytail 的源本周大涨 12.6k stars，印证该能力方向热度**。
- **openagentskill.com/trending**：按 **7 天 UTC 活动窗口排名**（非 lifetime stars），Snapshot 每日更新；本周 Frontend Design 第一。
- 判据：**进 LLM 前压缩是上下文治理的独立工具面**（入口侧，与输出侧/清单预算互补）；科学/专业域技能库走向"已验证+规模化"。
- **提升层**：工具 / 可复用 Skill。

### A4：评审查重复显式化 + fetch 三通道替代（来源：skillsmp p34 google-gemini/gemini-cli review-duplication ★107,125 + UnicomAI/wanwu web-content-fetcher ★2,477，2026-09-25 实拉）
- **review-duplication（google-gemini/gemini-cli ★107,125）**：代码评审时**主动调查代码库的重复功能/重造轮子/未复用项目最佳实践与共享工具**——把"有没有现成的"变成评审的显式检查项（与 wb-execute-discipline"先查现成可改"/AGENTS.md 二·五同源，本点增量=评审 checklist 化）。
- **web-content-fetcher（UnicomAI/wanwu ★2,477）三通道**：常规爬虫被过滤时用替代服务——①r.jina.ai（最稳定）②markdown.new（**Cloudflare 专用**）③defuddle.md（备用）——触发词含 bypass cloudflare；配套 seedance-antislop（★7,378：Seedance 2.0 提示词去 AI 味——通用 filler/空洞最高级/模糊电影语言/臃肿形容词/弱动词→更尖锐制作措辞）。
- 附：ui-pipeline-scheduler（WEB UI 自动化四段闭环 executor→failure-diagnoser→重试→report，熔断兜底）；code-to-image（前端代码+Playwright 渲染任意分辨率 PNG，零 API 成本/中文 100% 准确/Git 可追踪）。
- 判据：**评审不只验正确性还验重复**；fetch 被墙时先试三通道再放弃。
- **提升层**：工作流 / 可复用 Skill。

## 判重说明
- A1 → r209-C C1（plugins 页）管插件封装/分发，A1 管全局配置治理（作用域/权限/预算/沙箱/marketplace 策略），互补不重叠；与 r209-A A1（MCP managed 模式）的 MCP 部分重叠但 A1 主体为 settings 体系，增量 >60%，落（聚焦非 MCP 部分）。
- A2 → TanStack ai-sandbox 全新（r186-r209 未出现），落。
- A3 → 与 r209-C C3（agskills/DSH 生态）不同：A3 为 GitHub trending 新条目（headroom/scientific-agent-skills/tech-leads-club）+ ponytail 热度印证，新增量，落。
- A4 → review-duplication 与 wb-execute-discipline 同源但评审 checklist 化为增量；web-content-fetcher 三通道全新，合并落地。
- 未落：deepseek-plugin.org/tutorials（死链）、agskills.dev 续读（offset 参数无效，已有首拉数据）、dify blog 单篇（死链）、skills.sh 续读（图片为主）、ModelScope intro（link parse error）。
