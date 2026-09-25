# 学习轮 r210-B：Claude Code permissions与security官方页与skillsmp p35与openagentskill新信源（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.n8n.io/workflows/ | OK（121B 导航，低内容记录） |
| 2 | skillsmp.com/skills/page/35（#3401-3448） | OK（context-mode/ML投毒检测/n8n凭证自动化） |
| 3 | docs.activepieces.com/getting-started/overview | fetch error（多次失败记录） |
| 4 | docs.anthropic.com/claude-code/security（全 2338B） | OK（安全基线/WebDAV 风险/cloud credential） |
| 5 | make.com/en/help/ai | fetch error（记录） |
| 6 | docs.pipedream.com/ 根页（全 813B） | OK（与 r207B 重叠确认） |
| 7 | general_search WaytoAGI/飞书 | OK（Lark CLI/Agent 三能力线索） |
| 8 | docs.anthropic.com/claude-code/permissions（5995/6225 取） | OK（规则评估/Bash wildcard/compound/wrapper） |
| 9 | openagentskill.com/trending（4926/35546 取） | **新信源**（7 天活动窗口排名/interactions 六维） |
| 10 | docs.langflow.org/components（全 720B） | OK（component 版本/Group/Freeze 增量） |

## 独点（4 个）
### B1：Claude Code Permissions 官方页全量：规则评估 deny→ask→allow / Bash wildcard 词边界 / compound 子命令独立匹配 / wrapper 剥除陷阱（来源：docs.anthropic.com/claude-code/permissions 5995/6225B，2026-09-25 实拉；与 r210-A A1 settings 互补——A1 管配置体系，本条管权限细节）
- **权限由 Claude Code 执行不靠模型**：prompt/CLAUDE.md 只能塑造"Claude 想做什么"，不能改变允许范围——改权限只能 /permissions、规则、permission mode、PreToolUse hook。
- **评估顺序 deny → ask → allow，第一个匹配获胜**；deny 绝对优先（任一作用域 deny，其他层不能 allow）。
- **五权限模式**：default（首次提示）/acceptEdits（自动接受编辑+固定文件系统命令）/plan（只读探索）/auto（后台安全检查）/dontAsk（未预批全拒）/bypassPermissions（**跳过所有提示含 .git/.claude/.vscode/.idea/.husky 写；rm -rf / 和 ~ 仍提示作 circuit breaker**；仅隔离环境用）。
- **Bash wildcard 词边界语义**：`Bash(ls *)`（空格+* 强制词边界，匹配 ls -la 不匹配 lsof）vs `Bash(ls*)`（无边界，两者都匹配）；`:*` 是尾通配等价写法但只在模式末尾识别。
- **compound 命令：规则须独立匹配每个子命令**（&&/||/;/|/|&/&/换行）；批准 compound 时**每个子命令单独保存规则**（git status && npm test → 存 npm test，后续任何前缀都识别）；最多保存 5 条。
- **process wrapper 剥除**：timeout/time/nice/nohup/stdbuf 剥除后匹配（`Bash(npm test *)` 匹配 `timeout 30 npm test`）；无 flag 的 xargs 剥除；**devbox run/direnv exec/npx/docker exec 不在列表——`Bash(devbox run *)` 会匹配 devbox run rm -rf ..**（环境 runner 执行其参数为命令）→ 必须写含 runner+内命令的完整规则；watch/setsid/ionice/flock 与 find -exec/-delete 总是提示。
- **read-only 命令内建集**（ls/cat/echo/pwd/head/tail/grep/find/wc/which/diff/stat/du/cd+git 只读形式）全模式免提示；**unquoted glob 仅当命令全 flag 只读才允许**（find/sort/sed/git 带 glob 仍提示——glob 可展开成 -delete 等 flag）。
- **Bash 参数约束脆弱**：curl URL 过滤被 option 位置/协议/重定向/变量/多余空格绕过 → **用 deny 阻断 curl+wget 改用 WebFetch(domain:github.com)**，或 PreToolUse hook 验证 URL；WebFetch 单独不禁网络（Bash 允许时 curl 仍可达任意 URL）。
- **symlink 双路径检查**：allow 规则须 symlink 路径+目标**都**匹配（项目内 symlink 指向 ~/.ssh/id_rsa 被阻断）；deny 规则任一路径匹配即阻断。
- **Agent(AgentName) 规则**：deny Agent(Explore) 禁用特定 subagent（--disallowedTools 同效）。
- **PreToolUse hook 与权限规则关系**：hook 输出**不能 bypass 权限规则**（deny/ask 仍评估）；**blocking hook（exit 2）优先于 allow 规则** → 可"Bash 全 allow + hook 拒特定命令"。
- **additionalDirectories 只授予文件访问不授予配置**：.claude/ 配置大多不从 add-dir 发现；例外 .claude/skills/（live reload）、enabledPlugins/extraKnownMarketplaces、CLAUDE.md（需 CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1）。
- **sandbox 与权限互补**：权限=工具层（全工具），sandbox=OS 层（只 Bash+子进程）；autoAllowBashIfSandboxed=true 时沙箱化 Bash 免提示，但 rm/rmdir 关键路径仍提示——**纵深防御：权限 deny 阻止尝试，sandbox 阻止注入绕过**。
- 判据：**权限规则只写能精确表达意图的**（参数级约束不可靠换工具级 deny）；环境 runner 命令必须写含 runner 的完整规则；hook 是加严器不是放宽器。
- **提升层**：工具 / 可复用 Skill（权限工程 / 安全）。

### B2：skillsmp p35 精选：context-mode 大输出处理 / ML 投毒检测 / 凭证设置自动化（来源：skillsmp.com/skills/page/35，2026-09-25 实拉）
- **context-mode（mksglu/context-mode ★23,896）**：**用 ctx_execute/ctx_execute_file 工具代替 Bash/cat 处理大输出**——分析日志/总结输出/解析 JSON/过滤结果/提取错误/浏览器快照/DOM/Playwright snapshot/测试输出/git log/容器状态/API 响应等；**任何 MCP 工具输出可能超 20 行都触发**；**subagent 路由经 PreToolUse hook 自动处理**——大输出处理自动化（与 wb-context-compressor 同域：输出侧治理的自动化形态）。
- **detecting-data-and-model-poisoning（★33,129，IBM 工具链）**：训练/部署第三方数据或下载 checkpoint 前检测投毒/后门——**IBM Adversarial Robustness Toolbox（activation clustering/spectral signatures/trigger reconstruction）+ Cleanlab 标签质量 + 供应链检查（weight-hash 验证/safetensors 强制）**；怀疑模型行为绑定特定输入（后门触发）时用。
- **credential-setup-with-computer-use（n8n-io/n8n ★203,692）**：用 Computer Use 浏览器工具引导 n8n 凭证设置——从外部服务控制台取 OAuth apps/API keys/client IDs（凭证获取自动化，与用户"电脑操作类"需求相关）。
- **zh-output-example（bytedance/deer-flow ★82,768）**：审查中文技能文档的发表就绪度——中文技能文档质量门。
- **cash-flow-snapshot（anthropics/knowledge-work-plugins ★25,304）**：从账本（MYOB/NetSuite/QuickBooks/Xero/Zoho）+ PayPal/Square/Stripe/CSV 读 AR/AP/历史现金→30/60/90 天现金流预测（百分比方差置信带+命名风险标记）→聊天摘要+XLSX——**置信带+命名风险**是金融预测输出的可审计形态。
- 判据：**大输出先转 ctx 工具再分析**；外部数据/模型入 pipeline 前过投毒检测；凭证获取走 computer use 自动化。
- **提升层**：工具 / 工作流。

### B3：Claude Code Security 官方页安全基线：写范围限制 / 命令 blocklist / fail-closed / cloud credential 短生命周期（来源：docs.anthropic.com/claude-code/security 全 2338B，2026-09-25 实拉）
- **写访问限制**：只能写启动目录及子目录——读可出项目（系统库/依赖），**写严格限制在项目范围**（清晰安全边界）。
- **命令 blocklist**：curl/wget 默认拦截（fetch 任意 web 内容）；**fail-closed matching**：未匹配命令默认要求手动批准；命令注入检测（可疑 bash 即使 allowlisted 也要求人工批准）；复杂命令附自然语言解释。
- **Web fetch 隔离上下文窗口**：独立上下文避免注入恶意 prompt。
- **trust verification**：首次 codebase 运行+新 MCP server 要求信任验证；**-p 非交互禁用（--worktree 例外仍要求信任已接受）**。
- **Windows WebDAV 风险**：\\* 路径可含 WebDAV 子目录，**触发网络请求到远程主机绕过权限系统**——建议禁用 WebDAV。
- **cloud execution 安全**：隔离 VM/网络默认受限可配置禁用或域名白名单/credential 经安全代理用 **scoped 凭证翻译成 GitHub token**/git push 限当前分支/审计日志/会话后自动清理。
- **Remote Control 会话**：web 界面连本地 Claude Code 进程，代码执行与文件访问全本地；**多个短生命周期窄 scope 凭证，各自限特定用途独立过期——限制单个被攻凭证的爆炸半径**。
- **ConfigChange hooks**：审计/阻断会话中的设置变更（团队安全监控）。
- 判据：**写范围是硬边界**；未匹配命令 fail-closed；外部数据不直接管道给 Claude（建议 VM 跑脚本）；云端/远端执行用短生命周期 scoped 凭证。
- **提升层**：工具 / 工作流 / 安全。

### B4：openagentskill.com 新信源：7 天活动窗口排名 + interactions 六维拆解（来源：openagentskill.com/trending，2026-09-25 首拉）
- **排名方法论**：按 **7 个完整 UTC 天的站内活动窗口**排名（非 lifetime GitHub stars），Snapshot 每日更新；**Interactions 六维拆解**：Page views/Command copies/Comparisons/Saves/Repository clicks/Active days——可看"为什么它排第几"（如 Frontend Design 509 interactions = 338 Comparisons + 121 Page views）。
- **本周 Top 名单**：①Frontend Design（anthropics ★176,554）②holo-card-studio（3D 全息卡牌网站，项目本地 Blender+Three.js+浏览器验证）③Taste Skill Anti-Slop（87,456）④Canvas Design ⑤Vox Director（Vox 风格纸拼贴解说/广告视频，脚本到字幕）⑥Crawlee（Node 爬虫+浏览器自动化+代理轮换）⑦**Open Design（本地优先开源 Claude Design 替代：259+ Skills/142+ Design Systems/沙箱预览/HTML PDF PPTX MP4 导出/17+ CLIs）**⑧Guizang Ppt Skill（editorial+Swiss 布局 HTML slide decks+WebGL 低功耗运行时）⑨Webapp Testing（Playwright 本地 webapp 测试）⑩Last30days Skill（**30 天 Reddit/X/YouTube/HN/Polymarket/GitHub 多源综合简报**）⑪Equity Research ⑫Vercel React Best Practices ⑬Apple Design（Apple 界面设计翻译到 web）⑭PaddleOCR（100+ 语言）。
- 判据：**技能热度看活动窗口而非累计 stars**；interactions 拆解揭示真实使用形态（Comparisons 高=对比试用型，Saves 高=沉淀型）。
- **提升层**：工具 / 可复用 Skill。

## 判重说明
- B1 → 与 r210-A A1（settings 体系）互补：A1 管配置作用域/预算/市场策略，B1 管权限规则细节（wildcard 词边界/compound/wrapper 陷阱/symlink/hook 关系），增量 >60%，落。
- B2 → skillsmp p35 全新增量（context-mode/ML 投毒检测/n8n 凭证自动化），未在前轮出现，落。
- B3 → Security 页独立点（WebDAV 风险/cloud VM 隔离/credential 短生命周期/隔离上下文窗口/trust 验证）与 B1 权限规则不重叠，落。
- B4 → openagentskill.com 新信源首拉，落。
- 未落：n8n workflows 导航（低内容）、Activepieces（多次 fetch error）、Make /help/ai（fetch error）、Pipedream 根页（r207B 重叠）、LangFlow components（低方法，仅 Freeze/Group 微小增量并入说明）、Lark Agent 三能力（general_search 线索级，未深拉，留待后续）。
