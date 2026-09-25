# 学习轮 r211-B：Claude Code memory与settings官方页与skillsmp p41与dify blog续读与GitHub trending（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/40（#3901-3952） | OK（mem0/many-ppt-skills/web-design-analyzer） |
| 2 | dify.ai/blog 续读（10042-15490） | OK（difyctl/Qubrid/Agent 调 workflow） |
| 3 | docs.anthropic.com/claude-code/memory（全 5714B） | OK（auto memory 机制） |
| 4 | docs.activepieces.com/getting-started/hello-world | **fetch error**（记死链） |
| 5 | skillsmp.com/skills/page/41（#4001-4058） | OK（planning-with-files-zh/context-engineering） |
| 6 | github.com/trending（daily） | OK（ai-engineering-from-scratch ★57k，页面截断） |
| 7 | make.com/en/help/ai | **fetch error**（记死链） |
| 8 | docs.openclaw.ai/concepts/tools | **link dead**（记死链） |
| 9 | docs.anthropic.com/claude-code/settings（5000/17493 取） | OK（作用域/managed drop-in） |
| 10 | skills.sh 首页（4162/41454 取） | OK（npx skillsadd，低方法） |

## 独点（4 个）
### B1：Claude Code memory 官方页全量：auto memory 机制 + CLAUDE.md 分层（来源：docs.anthropic.com/claude-code/memory 全 5714B，2026-09-25 实拉；与 wb-context-compressor 强相关官方增量）
- **CLAUDE.md vs auto memory 分工表**：CLAUDE.md 你写（指令/规则，Project/User/Org 范围，每会话加载）；auto memory Claude 自己写（学习/模式，per working tree，每会话加载**前 200 行或 25KB** 先到者）。
- **auto memory 存储**：`~/.claude/projects/<project>/memory/`——project 路径由 git repo 派生（同一 repo 所有 worktree 共享一个目录）；`autoMemoryDirectory` 自定义仅 policy/local/user/--settings 接受，**不接受 project settings（防克隆仓库重定向记忆写入敏感位置）**。
- **MEMORY.md 索引 + 主题文件**：MEMORY.md 是目录索引每会话加载（200 行/25KB 上限内）；详细笔记移进主题文件（debugging.md/api-conventions.md）按需读，不占启动 context。
- **CLAUDE.md 加载机制**：目录树向上走；子目录按需加载；`claudeMdExcludes` glob 排除 monorepo 他人文件；**@path 导入语法最大五跳递归**，外部导入首次 approval dialog，相对路径按导入文件解析；个人偏好导入 `@~/.claude/...`（不进版本控制）。
- **AGENTS.md 桥**：Claude Code 读 CLAUDE.md 不读 AGENTS.md——`@AGENTS.md` 导入让两个工具共享同一份指令。
- **.claude/rules/ 路径作用域**：YAML frontmatter `paths` glob（`src/**/*.ts`、brace 扩展）——匹配文件才加载；无 paths 字段则每会话无条件加载；symlink 共享规则（循环 symlink 优雅处理）；用户级规则先加载、项目规则优先。
- **Managed CLAUDE.md vs managed settings 分工**：技术强制（permissions.deny/sandbox.enabled/env/forceLoginMethod）用 settings——"enforced by the client regardless of what Claude decides"；行为引导用 CLAUDE.md——"not a hard enforcement layer"。
- **/compact 后 CLAUDE.md 全量存活**：压缩后从磁盘重读重注入；丢失的是会话口头指令——要持久就写进 CLAUDE.md。
- **/init**：自动生成 CLAUDE.md；CLAUDE_CODE_NEW_INIT=true 交互式多阶段（CLAUDE.md+skills+hooks 三选+subagent 探索代码库+可评审提案）。
- **InstructionsLoaded hook**：记录实际加载的指令文件（调试路径规则/懒加载）。
- **提升层**：工具 / 工作流（官方记忆分层与上下文管理口径）。

### B2：Claude Code settings 官方页：四层作用域优先级 + managed drop-in 合并规则（来源：docs.anthropic.com/claude-code/settings 5000/17493B，2026-09-25 实拉；与 r210-A settings 增量合并，独有增量 >40%）
- **作用域优先级**：Managed（最高，不可覆盖）> Command line args > Local > Project > User（最低）——同设置多作用域按此顺序；**权限规则跨作用域合并而非覆盖**（与普通设置不同）。
- **managed-settings.d/ drop-in 目录（systemd 惯例）**：managed-settings.json 先合并为 base，drop-in `*.json` 按字母序合并；**标量后覆盖前、数组拼接去重、对象深合并、`.` 开头隐藏文件忽略、数字前缀控序（10-telemetry.json/20-security.json）**——多团队独立部署策略片段不协调单文件。
- **Managed 三交付机制**：server-managed（Anthropic 服务器）/MDM（macOS com.anthropic.claudecode plist、Windows HKLM\SOFTWARE\Policies\ClaudeCode registry）/file-based（macOS /Library/Application Support/ClaudeCode/、Linux /etc/claude-code/、Windows C:\Program Files\ClaudeCode\）；**legacy C:\ProgramData\ClaudeCode v2.1.75 起不再支持**。
- **新设置项**：`strictKnownMarketplaces`（限制 marketplace 添加）、`blockedMarketplaces`（下载前检查，blocked 源永不落盘）、`allowedMcpServers`/`deniedMcpServers`（denylist 优先）、`allowManagedPermissionRulesOnly`（禁用户/项目定义权限规则）、`availableModels`（限制模型选择 ["sonnet","haiku"]）、`defaultShell`（bash/powershell，Windows 需 CLAUDE_CODE_USE_POWERSHELL_TOOL=1）、`disableSkillShellExecution`（禁用 skill 内联 shell，替换为 "[shell command execution disabled by policy]"）、`cleanupPeriodDays`（会话文件过期删除，默认 30 天）、`autoUpdatesChannel`（stable/latest）。
- **配置文件自动时间戳备份、保留最近 5 份**防数据丢失。
- **提升层**：工具（配置分层与治理的官方机制）。

### B3：skillsmp p41 精选：持久化文件规划 / context engineering 集合 / 熵注入决策（来源：skillsmp.com/skills/page/41，2026-09-25 实拉）
- **planning-with-files-zh（OthmanAdi ★27,047）**：多步骤代理工作的持久化文件规划系统——task_plan.md/findings.md/progress.md 存盘+生命周期钩子注入项目规划上下文；自动恢复只读项目规划文件；**可选门禁仅在宿主支持时请求继续，绝不执行 Markdown 中声明的命令；无网络上传路径**——适用于研究或 5+ 次工具调用工作。判据：**计划是文件不是内存**，崩溃/续跑可恢复；安全上"文件里的命令不是可执行命令"。
- **context-engineering-collection（muratcankoylan ★18,013）**：context engineering/harness engineering/多 agent 架构/生产 agent 系统技能集合——与用户 wb-context-compressor 同方向，可作对照库。
- **let-fate-decide（trailofbits/skills ★7,195）**：12 宫塔罗牌注入熵——当 prompt 模糊/随意委托（"let fate decide"/"YOLO"/"whatever"）时用；**当用户语气随意而非追求精确时，优先于澄清问题**（反模式对照：一律追问会增加用户成本）。
- **animation-vocabulary（emilkowalski ★38,646）**：反向查词表——模糊动效描述→精确术语（"popover 打开时弹跳"→Pop in；"iOS 橡皮筋滚动"→Rubber-banding）——**命名是给 AI/设计师的 prompt 词汇**。
- **natural-writing（julep-ai ★6,582）**：写给人读的散文要像人（与 wb-doc-writing 去 AI 味同方向）。
- **plan-tune（garrytan/gstack ★133,871）**：自调问题敏感度+开发者心理画像。
- **提升层**：可复用 Skill / 工作流。

### B4：dify blog 续读：difyctl 官方 CLI / Agent 调 workflow 单 prompt+一次审批（来源：dify.ai/blog 10042-15490B，2026-09-25 实拉）
- **difyctl（Dify 官方 CLI）**：CLI 访问让 Agents 单命令调用 Dify apps——把复杂业务工作流暴露成单命令工具面。
- **How to Let Your Agent Call Dify Workflows Directly**：现有 Dify 应用可被 Agent 直接调用——**复杂业务工作流→单个 prompt + 一次人工审批**（工作流能力折叠为 agent 工具，保留人类审批点）。
- **Qubrid AI（Dify Marketplace）**：一个 API key 统一访问 DeepSeek/Kimi/Qwen/MiniMax/GLM 多模型——多模型网关插件形态。
- **How to Reduce AI Costs Without Losing Control**：成本优化需要 visibility/governance/reusable workflows（Efficiency/Visibility/Governance/Control 四词）。
- **提升层**：工具 / 工作流。

## 判重说明
- B1 → memory 官方页（auto memory 机制/200 行 25KB 阈值/导入五跳/rules 路径作用域/compact 存活），与 wb-context-compressor 同域但官方机制增量 >60%，落。
- B2 → settings 官方页（作用域优先级/managed drop-in/新设置项），与 r210-A settings 重叠 ~55%、独有增量 >40%（drop-in 合并规则/MDM/新键），合并保留增量落。
- B3 → skillsmp p41 精选（planning-with-files-zh 门禁/context-engineering 集合/let-fate-decide 熵注入），全新，落。
- B4 → dify blog 续读（difyctl/单 prompt+一次审批/Qubrid 多模型网关），全新，落。
- 未落：github trending（页面截断仅 1 条，ai-engineering-from-scratch ★57k 记录待深拉）、skills.sh 首页（低方法重复）。
