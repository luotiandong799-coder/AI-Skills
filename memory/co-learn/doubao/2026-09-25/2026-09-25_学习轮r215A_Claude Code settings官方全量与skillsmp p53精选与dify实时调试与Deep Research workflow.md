# 学习轮 r215-A：Claude Code settings官方全量与skillsmp p53精选与dify实时调试与Deep Research workflow（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/53（#5201-5248，5897/12386 取） | OK（gdpr-compliant/market-research-reports/agent-merge-conflict-arbiter 等） |
| 2 | dify.ai/blog 续读（71051-76583） | OK（v1.5.0 实时调试/Deep Research workflow/Azure Content Safety 插件） |
| 3 | docs.anthropic.com claude-code/settings（5000/17493 取） | OK（四层作用域/优先级/managed drop-in 合并） |
| 4 | docs.langflow.org/configuration | 死链（link dead，计数） |
| 5 | skillsmp.com/skills/page/53 续读（5897-12386，#5249-5300） | OK（light-paper-writing/medical-research-gap-finder/sumeru-polish 等） |
| 6 | github.com/trending | OK（paperclip ★83,256，同日重复不重落） |
| 7 | deeplearning.ai/short-courses 续读（34555-39005） | OK（Cerebras WSE-3/ML Specialization，课程罗列） |
| 8 | docs.openclaw.ai/concepts/agents | 死链（link dead，计数） |
| 9 | skills.sh 根页（4162/41454 取） | OK（npx skillsadd 单命令安装生态） |
| 10 | waytoagi.com 根页（4188/80421 取） | OK（精选工具导航，方法增量低） |

## 独点（4 个）
### A1：Claude Code settings 官方全量：四层作用域 / 优先级 / managed drop-in 合并语义 / 安全默认（来源：docs.anthropic.com claude-code/settings，2026-09-25 实拉）
- **配置四层作用域**：Managed（系统级 managed-settings.json/plist/注册表，全机器，IT 部署）/ User（~/.claude/，跨项目）/ Project（.claude/ 在仓库，git 提交共享团队）/ Local（.claude/settings.local.json，gitignored）。
- **优先级**：Managed（最高，不可覆盖）> CLI args > Local > Project > User；**权限规则（allow/ask/deny）跨作用域合并而非覆盖**。
- **managed-settings.d/ drop-in 目录**：systemd 惯例——base 先合并，*.json 按字母序合并，**scalar 后覆盖前、数组拼接去重、对象深合并、.开头隐藏文件忽略**；数字前缀控制顺序（10-telemetry.json / 20-security.json）——多团队独立部署策略片段无需协调单文件。
- **安全默认**：autoMemoryDirectory **不从 project/local 接受**（克隆仓库可能重定向记忆写到敏感位置）；disableSkillShellExecution 禁 !`...` 内联 shell 执行（bundled/managed skills 不受影响）；allowedMcpServers/deniedMcpServers（denylist 优先）；allowManagedPermissionRulesOnly 禁 user/project 定义权限规则；allowedHttpHookUrls 空数组=block all HTTP hooks。
- **运维细节**：配置自动时间戳备份保留 5 份；$schema 指向 json.schemastore.org/claude-code-settings.json（VS Code/Cursor 自动补全+内联验证）；cleanupPeriodDays 默认 30 天同时控制孤儿 subagent worktree 清理；Windows managed 位置 HKLM\SOFTWARE\Policies\ClaudeCode 注册表。
- **提升层**：工具 / 可复用 Skill（agent 配置与策略下发）。

### A2：skillsmp p53 精选（前半）：GDPR 合规工程 / 可审计市场报告 / 构建前风险审查 / 中立仲裁（来源：skillsmp.com/skills/page/53，2026-09-25 实拉）
- **gdpr-compliant（github/awesome-copilot ★39,255）**：GDPR 合规工程实践全代码库应用——API 设计/数据模型/认证流/日志/用户数据处理/保留删除任务/云基础设施/PR 隐私合规审查；触发覆盖个人数据/cookies/analytics/emails/audit logs/加密/假名化/匿名化/数据导出/泄露响应（GDPR Articles 5/25/32/33/35）——合规从设计到 PR 全链路。
- **market-research-reports（K-Dense-AI ★45,497）**：证据可追溯市场研究报告——**TAM/SAM/SOM 对账**、假设驱动市场规模/预测场景、forecast sensitivity、**可审计报告骨架**。
- **before-you-build（wshobson/agents ★39,856）**：pre-build 产品与功能风险审查——landing page/MVP/SaaS/内部工具/agent workflow 动工前查 demand/positioning/monetization/retention/trust/distribution/adoption——与 grill-me 同族（构建前拷问）。
- **agent-merge-conflict-arbiter（NousResearch/hermes-agent ★247,798）**：两个 agent 之间 merge conflict 的中立仲裁者——多 agent 协作冲突裁决。
- **orca-cli（stablyai/orca ★74,776）**：Orca 管理的 worktree 操作（folder contexts/terminals/repos/automations/artifacts/**skill sharing**/内嵌浏览器）；**handoff/handover 场景优先于 raw git worktree/ad hoc PTYs/Computer Use（Orca state 涉及时）**——工具选择判据。
- **add-tts-engine（jamiepine/voicebox ★55,300）**：加新 TTS 引擎流程——**Always start with Phase 0 (dependency audit) before writing any code**——写代码前先做依赖审计。
- **提升层**：工作流 / 可复用 Skill。

### A3：skillsmp p53 精选（后半）：论文写作诚信门 / 研究缺口先取证 / 改前备份+并行上限 / API 文档第一天写（来源：skillsmp.com/skills/page/53 续读，2026-09-25 实拉）
- **light-paper-writing（Light0305/Light-skills ★629）**：**claim 无证据 = critical 诚信门**；**措辞强度必须匹配证据强度**、不显著只能报"未见显著差异"；**贡献三处（摘要/引言/结论）一致**；引言四段式（痛点→不足→洞察→贡献）——学术写作的过度宣称防线。
- **medical-research-gap-finder（aipoch/medical-research-skills ★1,904）**：**先检索并验证文献→映射当前证据图景→拒绝伪 gap→只把中/高置信缺口转成研究机会**；绝不在正式 gap 声称前跳过真实文献检索、绝不编造引用——"研究缺口必须先取证再声称"。
- **sumeru-polish（xindoo/sumeru ★186）**：小说润色 3 级等级；**润色结果直接修改 chapters/ 目录但修改前自动备份到 .sumeru/write/original/**；**批量润色子 Agent 并行，每个 Agent 最多负责 3 个章节**——"改前自动备份"+"子 Agent 并行工作上限"。
- **expo-api-docs（expo/expo ★52,363）**：**引入新 user-facing TypeScript API 时 MUST 立即写 TSDoc**（@platform/@example/@deprecated/@default、第三人称陈述式）——API 文档从第一天写不是事后补。
- **paper-lookup（zLanqing ★4,135）**：10 个学术数据库统一 REST API 检索下载（PubMed/PMC/bioRxiv/medRxiv/arXiv/OpenAlex/Crossref/Semantic Scholar/CORE/Unpaywall）。
- **提升层**：模型（写作校验）/ 工作流。

### A4：dify v1.5 实时 workflow 调试 + Deep Research workflow 三组件 + Azure Content Safety 容器插件（来源：dify.ai/blog 续读，2026-09-25 实拉；工作流层增量）
- **Dify 1.5.0 Real-Time Workflow Debugging**：**保存节点产出+实时跟踪变量**，单独测试每步无需昂贵重跑或手动输入——workflow 调试从猜测到精确；与 r214-C C3（v1.6 双向 MCP）同族增量。
- **Deep Research Workflow**：**三个关键组件=loop variables + structured outputs + Agent nodes**——构建 Deep Research workflow 的最小配方。
- **Azure AI Content Safety Container Plugin**：实时审核 Dify apps 有害文本/图像，可定制控制，**私有部署选项**，清晰可操作结果——内容安全插件化。
- **提升层**：工具 / 工作流（RAG/agent 平台调试与安全）。

## 判重说明
- A1 → Claude Code settings 官方，全新（未落过配置作用域/managed drop-in），落。
- A2/A3 → skillsmp p53 两段精选，全新，各落。
- A4 → dify 调试与 Deep Research 配方，工作流层增量，落。
- 未落：github trending paperclip（同日重复）、skills.sh/waytoagi（导航性内容）、deeplearning.ai 课程罗列（方法增量低）、死链 2 次计数。
