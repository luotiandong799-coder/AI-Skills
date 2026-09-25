# 学习轮 r216C：skillsmp p57精选与dify Agent Node与OpenClaw CLI与Agent Skills规格（2026-09-25）

## 实拉记录（12 次调用，10 成功 / 1 死链 / 1 分页修正）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/57（#5601-5663，6000/9489 取） | OK |
| 2 | dify.ai/blog 续读（96256-100856） | OK（Agent Node/Plugin Endpoint/Brave） |
| 3 | docs.n8n.io 首页（1227B） | OK（MCP 连接命令/fair-code） |
| 4 | docs.langflow.org/components-tools（4655/7750） | OK（Components 总览/Freeze/端口） |
| 5 | GitHub Trending 搜索（github.hot/trendshift/ai-tldr） | OK（agent-skills registry/arcbox/VoiceStudio） |
| 6 | learn.deeplearning.ai offset 53552 | 越界（已读尽 53552，计数） |
| 7 | docs.openclaw.ai/cli（2576B） | OK（CLI 全览/skills workshop 审批流） |
| 8 | activepieces.com/docs（4399/19123） | OK（agent-flow-tables 三角模型） |
| 9 | skills.sh offset 4162 | OK（仅图片，无文本增量） |
| 10 | agentskills.io/specification offset 4789 | 分页越界（total 1797，修正重读） |
| 11 | agentskills.io/specification（1797B 全取） | OK（frontmatter 字段/allowed-tools/三层预算） |
| 12 | skills.sh/docs（434B） | OK（CLI/遥测排行/安全审计） |

## 独点（4 个）
### C1：skillsmp p57 精选：loop 全生命周期治理 / 纯文字模型抽帧审计 / 模型迁移纪律 / 并行加速（来源：skillsmp.com/skills/page/57，2026-09-25 实拉）
- **loopy（Forward-Future/loopy ★3,143）**：**可重复 AI-agent loops 全生命周期——发现/比较/审计/修复/适配/制作/运行/复盘/保存/发布；目标访谈成有界 loop、审 loop 弱检查或危险权限、带证据回执执行、完成后学习、验证提交 Loop Library**。
- **video-screenshot（Chinese skill）**：**视频截图证据线索精筛——有界高召回抽关键帧/过滤切换中间态；本地 OCR 多锚点+无文字图像主体→证据线索索引（不保存原文）；为普通或弱多模态模型提供受预算/封闭类别/非破坏性的分类概括包；只做减法+覆盖存活门禁去重；纯文字模型可完成全部本地流程**。
- **claude-opus-4-5-migration（anthropics/claude-code ★147,483）**：**模型迁移纪律——Sonnet 4.0/4.5/Opus 4.1→Opus 4.5：模型字符串更新+已知行为差异的提示词调整；明确不迁移 Haiku 4.5**。
- **memory（google-gemini/gemini-cli ★107,125）**：**持久 bot 记忆维护——Task Ledger 与先前会话同步+决策日志保留**。
- **graphing（anthropics/claude-tag-plugins ★50）**：chartkit 原语从表格数据做精致图表（时间序列/柱/线/面积/饼/散点）→PNG/SVG/自包含交互 HTML。
- **caveman-review（JuliusBrussee/caveman ★107,172）**：压缩代码审查——每发现一行=位置+问题+修复。
- **poster-style-transfer（jiemianduan ★45）**：分析参考海报→提取可复用设计系统→迁移到新主题/文案的新海报。
- **parallel-execution-optimizer（ECC ★264,820）**：并行工作/并发 agents/批量工具调用/隔离 worktree/多独立验证通道加速任务不损正确性。
- **提升层**：工作流 / 可复用 Skill。

### C2：dify Agent Node 插件式决策 + Plugin Endpoint serverless 回调（来源：dify.ai/blog，2026-09-25 实拉）
- **Dify Agent Node**：工作流内 Agent 节点像大脑，LLM 自主决策；**可定制 Agent Strategies 是插件式逻辑模块，规定 LLM 怎么想、怎么用工具——灵活性与控制并存**。
- **Extension Plugin Endpoint**：**插件处理自定义 HTTP 请求+reverse calls（回调）——自定义 web 界面/OpenAI 兼容 API/异步事件触发**，serverless 灵活性。
- **Brave Search API 插件（Dify v1.0.0）**：实时搜索进 AI 应用。
- **提升层**：工作流（agent 决策可插拔）。

### C3：OpenClaw CLI 官方全览：skills workshop 审批流 / 状态隔离 / JSON 失败信封（来源：docs.openclaw.ai/cli，2026-09-25 实拉）
- **skills workshop 治理流**：`workshop list|inspect|propose-create|propose-update|revise|apply|reject|quarantine`——**技能变更走 propose→revise→apply/reject/quarantine 审批流，不是直接写文件**（与本地 skill 治理同构）。
- **状态隔离**：`--dev` 隔离 `~/.openclaw-dev`（网关端口 19001）/`--profile <name>` 隔离 `~/.openclaw-<name>`/`--container` 容器内跑 CLI——平行环境互不污染。
- **JSON 失败信封**：`{ok:false,error:{type,message}}`，Gateway 已接受的 run 记录 `runId`+`origin:"gateway"`；**失败消息消毒**、诊断走 stderr——脚本解析 stdout+查退出码。
- **完整命令树**：setup/configure/backup/database/migrate/agent/mcp/status/triage/sessions/resume/audit/models/infer/memory/wiki/approvals/exec-policy/sandbox/tui/browser/worktrees/cron/tasks/hooks/webhooks/security/secrets/skills/plugins。
- **提升层**：工具 / 工作流（CLI 治理范式）。

### C4：Agent Skills 规格官方：allowed-tools 白名单 / progressive disclosure 三层 token 预算 / name 硬约束 / skills-ref 校验（来源：agentskills.io/specification，2026-09-25 实拉）
- **frontmatter 字段**：name（**1-64 字符、仅小写字母数字+连字符、不得起止连字符/连续连字符、必须匹配父目录名**）/description（1-1024，写做什么+何时用+关键词）/license/compatibility（环境要求）/metadata（键值映射）/**allowed-tools（实验性：预批准工具白名单，如 `Bash(git:*) Bash(jq:*) Read`——技能只声明它被允许用什么工具）**。
- **Progressive disclosure 三层带 token 预算**：①**Metadata ~100 tokens**——启动全载 name+description ②**Instructions <5000 tokens 推荐**——激活时载全文 ③**Resources 按需**——scripts/references/assets 用到才载；**SKILL.md 建议 <500 行，长内容拆引用文件，文件引用保持一层深**。
- **校验器**：`skills-ref validate ./my-skill` 检查 frontmatter 有效性与命名约定。
- **提升层**：可复用 Skill（技能规格与校验）。

## 判重说明
- C1 全新（p57 独有），落。
- C2 dify 增量（Agent Node Strategies/Plugin Endpoint 新页），落。
- C3 openclaw cli 官方新页（r215 拉过 security/channels，本页为新），落。
- C4 规格官方（B4 为 overview 三阶段，本页为字段级规格+token 预算+校验器），增量≥40% 合并保留，落。
- 未落：trending 本轮多为工具目录（与 A3 重复）、n8n 首页（MCP 连接命令与 r213C 插件页重复度高）、activepieces docs（产品定位为主）、skills.sh docs（遥测机制小增量）。
