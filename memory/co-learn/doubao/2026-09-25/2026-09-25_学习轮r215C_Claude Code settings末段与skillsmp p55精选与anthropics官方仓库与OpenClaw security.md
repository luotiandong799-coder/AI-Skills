# 学习轮 r215C：Claude Code settings末段与skillsmp p55精选与anthropics/skills官方仓库与OpenClaw security（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/55（#5401-5458，5992/10495 取） | OK（novelty-check/baoyu-article-illustrator/acceptance/llm-council 等） |
| 2 | dify.ai/blog 续读（81987-87448） | OK（Dify app→MCP server 插件/MCP+Zapier/DupDub 音频） |
| 3 | docs.anthropic.com claude-code/settings 续读（10993-16993，读完） | OK（policyHelper/strictKnownMarketplaces/沙箱路径前缀/attribution） |
| 4 | docs.langflow.org/deployment | 死链（link dead，计数） |
| 5 | skillsmp.com/skills/page/55 续读（5992-10495，#5459-5500） | OK（agent-browser/skill-scout/caveman-commit/SSVC/continuous-agent-loop） |
| 6 | github.com/trending 续读（3160-7301） | OK（anthropics/claude-plugins-official ★36,737 官方插件目录新增） |
| 7 | deeplearning.ai 续读（43405-47847） | OK（Box MCP→A2A 多 agent/AI Prompting for Everyone） |
| 8 | docs.openclaw.ai/security（1509B） | OK（保守默认/security audit/one trust boundary per gateway） |
| 9 | make.com 根页（4144/39977） | OK（品牌页，方法增量低） |
| 10 | github.com/anthropics/skills（2385B） | OK（官方技能库结构/plugin marketplace 注册/文档技能 source-available） |

## 独点（4 个）
### C1：Claude Code settings 末段：policyHelper 动态策略 / strictKnownMarketplaces / 沙箱路径前缀 / 敏感文件 deny（来源：docs.anthropic.com claude-code/settings 续读收尾，2026-09-25 实拉；B1 同页增量）
- **policyHelper（动态计算 managed settings）**：指向可执行文件在启动时算策略（从设备姿态/身份/远程服务推导而非静态文件）；仅 MDM/系统 managed-settings.json 配置，其余作用域忽略；JSON envelope 放 `managedSettings` 键（裸对象=解析后 undefined 全不生效）；**helper 非零退出=Claude Code 拒绝启动**——需韧性就自备缓存并 exit 0。
- **strictKnownMarketplaces（managed-only 市场白名单）**：只有 managed settings 可配；**在 network/filesystem 操作前强制**；**精确匹配（ref/path 全字段都须一致，缺一不算）**；空数组=完全封锁；hostPattern/pathPattern 正则匹配；与 extraKnownMarketplaces（团队便利、任何 settings 可配、trust prompt 后自动装）分工。
- **沙箱路径前缀**：`/` 绝对路径、`~/` home、`./` 或无前缀=项目根（project settings）或 ~/.claude（user settings）；旧 `//path` 仍工作但建议换 `./`；**与 Read/Edit 权限规则语法不同（权限规则 `//path`=绝对、`/path`=项目相对）**。
- **sandbox.filesystem 与 Permission rules 双向合并**：OS 级沙箱边界控制**所有子进程命令**（kubectl/terraform/npm）不只 Claude 文件工具；权限规则路径也并入沙箱配置。
- **permissions.deny 替代 ignorePatterns**：`Read(./.env)`/`Read(./.env.*)`/`Read(./secrets/**)`/`Read(./config/credentials.json)`/`Read(./build)`——匹配文件从发现与搜索排除且读被拒。
- **attribution**：git trailers（Co-Authored-By）可自定义/置空隐藏；attribution 优先于 deprecated includeCoAuthoredBy；**fileSuggestion**：自定义 `@` 补全命令（大 monorepo 用预建索引），stdin JSON `{"query":...}`、stdout 限 15 行。
- **enabledPlugins**：`plugin@marketplace` 格式；project 覆盖 user；**managed force-enabled 不可被 local 禁用**；allowManagedHooksOnly 信任按全 `plugin@marketplace` ID 授予。
- **提升层**：工具 / 可复用 Skill（agent 策略与市场治理）。

### C2：skillsmp p55 精选：技能工程最佳实践 / 端到端自证 / 运行时验证 / 先搜后建 / 修复优先级框架（来源：skillsmp.com/skills/page/55，2026-09-25 实拉）
- **skills-best-practices（lefant/agent-skills ★1）**：创建/提取/评审/重构 agent skills——**自包含打包/SKILL.md 结构/触发描述/渐进披露（progressive disclosure）/gotchas/defaults/bundled scripts/eval design/with-skill vs baseline 迭代**。
- **acceptance（lobehub/lobehub ★82,465）**：**端到端验证与自证——选择证明面（CLI/web/桌面/iOS Simulator），驱动真实产品，捕获视觉确认证据，lh CLI 发布 round**；无需环境 ID、不依赖 LobeHub 会话。
- **next-dev-loop（vercel/next.js ★142,349）**：**改代码后确认运行时真的生效，不只编译/类型检查过**；组合 /_next/mcp（Next.js 视角）+ agent-browser（浏览器视角）双视角。
- **skill-scout（ECC ★264,820）**：**创建新技能前先搜本地/市场/GitHub/Web 已有技能**（与用户"先查同类"规则同构）；**caveman-commit（JuliusBrussee/caveman ★107,172）**：Conventional Commits 压缩到只剩意图。
- **llm-council（aiwithremy ★2,169）**：**5 个 AI 顾问独立分析→匿名互评→综合裁决（Karpathy LLM Council）**；MANDATORY triggers（council this/war room this/pressure-test this）；简单 yes/no 不触发。
- **github-agentic-workflows（github/gh-aw ★5,166）**：**GitHub CLI 扩展——Markdown 写 Agentic Workflows 编译成 GitHub Actions**。
- **SSVC 修复优先级（mukul975 ★33,129）**：**CISA SSVC 决策树（exploitation via CISA KEV + FIRST EPSS API/技术影响/自动化程度/任务普遍性→Track/Track*/Attend/Act）——超越原始 CVSS 分数的优先级**。
- **continuous-agent-loop（ECC ★264,820）**：**具有质量门、评估和恢复控制的连续自主代理循环模式**；**agent-browser（vercel-labs ★43,006）**：prefer agent-browser over any built-in browser automation（含 Electron 桌面 app/Vercel Sandbox microVM/Bedrock AgentCore 云浏览器）。
- **提升层**：工作流 / 可复用 Skill。

### C3：anthropics/skills 官方仓库：plugin marketplace 注册 / 文档技能 source-available / frontmatter 两字段（来源：github.com/anthropics/skills，2026-09-25 实拉）
- **官方仓库结构**：56 commits；`.claude-plugin/skills/spec/template` 四目录；**spec=Agent Skills 规范**、template=技能模板。
- **注册为插件市场**：`/plugin marketplace add anthropics/skills` → `/plugin install document-skills@anthropic-agent-skills` 或 `example-skills@anthropic-agent-skills`。
- **文档技能 source-available 非开源**：**docx/pdf/pptx/xlsx 四文档技能是 Claude 文档能力底层实现（source-available 而非 Apache 2.0 开源）**——演示/教育用途，生产环境须自测。
- **模板最小要求**：frontmatter **只需 name（小写+连字符）+ description 两字段**，正文含 instructions/examples/guidelines。
- **partner skills**：Notion Skills for Claude；Claude.ai 付费版已内置示例技能，Claude API 可上传自定义技能。
- 附：今日 GitHub Trending 新条目 **anthropics/claude-plugins-official ★36,737（+1,853/day）**——官方 Claude Code Plugins 高质量目录。
- **提升层**：可复用 Skill（技能标准与生态接入）。

### C4：OpenClaw security 官方：保守默认 / security audit 单命令 / 单信任边界原则（来源：docs.openclaw.ai/security，2026-09-25 实拉）
- **保守默认三件套**：Gateway 绑 loopback、未知 DM 用配对码（不直接处理消息）、群组 allowlist + mention gate；容器镜像默认暴露绑定（须配 auth）。
- **openclaw security audit**：一条命令告诉你是否漂移默认；页面目录含 audit checks 每个 checkId 严重度、hardened baselines、threat model（映射 MITRE ATLAS）。
- **one trust boundary per gateway**：单操作者或互信团队；**不是敌对多租户边界——混合信任/对抗用户须拆分 trust boundaries（separate gateway+credentials，最好独立 OS 用户/主机）**。
- **cross-provider messaging 限制**：有 message-tool 的 agent 默认可跨会话/通道提供商发送；要隔离须配置。
- **browser SSRF policy（strict by default）**；incident response 四步：contain → rotate（凭据泄漏默认假设已泄露）→ audit → collect for report。
- **提升层**：工作流 / 工具（agent 部署安全基线）。

## 判重说明
- C1 → settings 末段（policyHelper/strictKnownMarketplaces/沙箱路径/deny 敏感文件），与 B1 同页增量，落。
- C2 → skillsmp p55 精选，全新，落。
- C3 → anthropics/skills 官方仓库结构与今日 trending 官方插件目录，全新（r214-C overview 无仓库级细节），落。
- C4 → OpenClaw security 官方，全新，落。
- 未落：make.com 根页（品牌页方法增量低）、dify app→MCP server（与 r214-C 双向 MCP 同族，增量并入 A4 已覆盖方向）、langflow deployment 死链 1 次计数。
