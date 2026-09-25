# 学习轮 r212-B：agentskills官方Specification字段级与Anthropic overview后半运行时约束与skillsmp p45与deepseek-plugin目录生态（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/45（#4401-4450，5916/11558 取） | OK（nature-figure/codebase-analysis/zach-search-term 等） |
| 2 | dify.ai/blog 续读（26578-32106） | OK（intent-based email routing/State Infrastructure Gap，企业级为主） |
| 3 | docs.anthropic.com agent-skills/available-skills | 死链（区域不可用，App unavailable，计数） |
| 4 | docs.langflow.org（1946B 全，v1.11.x） | OK（MCP server/client、tweaks 运行时覆盖，中方法） |
| 5 | docs.activepieces.com 根 | 死链（link fetch error，累计计数） |
| 6 | make.com/en（4144/39977 取） | OK（可视化/代码/prompt 三方式，低方法） |
| 7 | agentskills.io/specification（1797B 全） | OK（frontmatter 全字段规格+目录结构+skills-ref validate） |
| 8 | deepseek-plugin.org（596B 全） | OK（12,733 插件+Top10 榜单） |
| 9 | github.com/trending 续读（offset 4183） | OK（vectorize-io/hindsight ★28,462 347 today） |
| 10 | docs.anthropic.com agent-skills/overview 剩余段（offset 5000-6399 全读完） | OK（运行时约束/预构建四件套/cross-surface） |

## 独点（4 个）
### B1：agentskills.io Specification：frontmatter 字段级约束 + 目录规范 + 校验工具（来源：agentskills.io/specification，2026-09-25 实拉；与 r211-C C1 三阶段同源，字段级独有增量 ≥40% 合并落）
- **name 字段完整约束**：≤64 字符、仅小写字母数字连字符、**不能以连字符开头/结尾、不能连续连字符（--）、必须匹配父目录名**。
- **description 字段**：1-1024 字符，应描述"做什么+何时用"，**应包含帮助 agent 识别相关任务的具体关键词**（官方示例 Good vs Poor："Extracts text and tables from PDF files, fills PDF forms..." vs "Helps with PDFs."）。
- **compatibility 字段（可选，≤500 字符）**：环境要求——目标产品/系统包/网络访问（`Requires Python 3.14+ and uv`）。
- **allowed-tools 字段（实验性）**：空格分隔预批准工具列表（`Bash(git:*) Bash(jq:*) Read`）——**"skill 允许用哪些工具"进 frontmatter 声明**。
- **SKILL.md 建议 <500 行**；引用文件保持**一层深**（避免深层嵌套引用链）；目录结构 SKILL.md 必 + scripts/references/assets。
- **校验工具：`skills-ref validate ./my-skill`** 检查 frontmatter 有效性与命名规范。
- **提升层**：可复用 Skill（authoring 规格）。

### B2：Anthropic overview 后半：运行时环境约束三平台 + 预构建四件套 + Custom Skills 不跨 surface（来源：docs.anthropic.com agent-skills/overview offset 5000-6399，2026-09-25 实拉；与 r212-A A1 同页续读，增量落）
- **运行时环境约束（写 Skill 前必看的三平台差异）**：**Claude API = 无网络访问（不能外部 API/互联网）+ 无运行时包安装（只有预装包）+ 仅预配置依赖**；**Claude Code = 完整网络访问（同用户电脑上其他程序）+ 全局包安装不鼓励（只应本地装避免干扰用户电脑）**；**claude.ai = 网络访问 vary（按用户/管理员设置 full/partial/none）**。
- **Pre-built Agent Skills 官方四件套**：PowerPoint(pptx)/Excel(xlsx)/Word(docx)/PDF(pdf)，可用在 Claude API/AWS/Microsoft Foundry/claude.ai；开源技能 Claude API（8 种语言 API 参考，bundled with Claude Code）。
- **Cross-surface availability：Custom Skills 不自动跨 surface 同步**——claude.ai 上传需单独再传 API；API 上传不在 claude.ai；Claude Code 文件系统独立。
- **Sharing scope**：claude.ai 仅个人（每成员单独上传、无中央管理）；Claude API workspace-wide；Claude Code personal `~/.claude/skills/` 或 project `.claude/skills/`，可经 Plugins 共享。
- **安全细则**：audit 所有捆绑文件找异常模式（意外网络调用/文件访问）；**外部 URL 抓取内容可能含恶意指令，即使可信 skill 也会因外部依赖随时间变化被攻破**；treat like installing software。
- **Data retention：Agent Skills 不覆盖 ZDR**。
- **提升层**：可复用 Skill（跨环境兼容规划）。

### B3：skillsmp p45 精选：绘图前定义结论 / 脚本编排探索 / 人机分工词根继承（来源：skillsmp.com/skills/page/45，2026-09-25 实拉）
- **nature-figure（jing1312/nature-figure-skill ★143）**：Nature 级论文图表工作流——**绘图前先定义图的结论、证据逻辑、导出需求、评审风险；用户未选语言先问 "Python or R?" 并停**；只用所选后端生成/预览/导出/QA。
- **codebase-analysis（solatis/claude-config ★907）**：代码库理解任务 **Invoke IMMEDIATELY via python script——Do NOT explore first, the script orchestrates exploration**（"脚本编排探索"反直觉方法：探索由确定性脚本驱动而非模型自由探索）。
- **zach-search-term-report-analyzer（zach22-1999/amazon-skills ★196）**：Amazon Ads 搜索词报告——**确定性脚本负责清洗/时间窗聚合/词根聚类/决策计算，AI 只负责词根级语义分类**（人机分工明确）；**词根继承减少长尾词待判定比例**；输出 Markdown/CSV/HTML/JSON。
- **disk-cleaner（xiaofenggan01/disk-cleaner-skills ★35）**：磁盘清理——**扫描全程只读**、AI 语义分析识别垃圾、交互式 HTML 报告+一键清理；**明确 RAM≠存储边界（"哪个进程吃内存"不归它管）**。
- **ctf-reverse（ljagiello/ctf-skills ★3,323）**：逆向边界判定——**漏洞已理解且剩利用时不用于 reverse（走 pwn）；纯 web 流程/日志取证/独立 crypto 也不用**——"边界先写进 description 再发布"范例。
- **incident-runbook-templates（wshobson/agents ★39,856）**：事件响应 runbook（逐步骤/升级路径/恢复动作，面向凌晨 3 点的大脑）。
- **提升层**：可复用 Skill / 工作流。

### B4：deepseek-plugin.org 目录生态：12,733 插件 + Top10 新条目（来源：deepseek-plugin.org，2026-09-25 实拉；与 r211-A A4 DSH 生态同域，Top10 榜单与记忆分层增量落）
- **目录规模 12,733 个 DeepSeek Harness 插件，每日更新**。
- **Top10 by stars**：reactive-resume/dsh-plugin ★41,287（MCP 读改在线简历）；**Tencent dsh-weknora ★21,008（原始文档→可查询 RAG + 自主推理 agent + 自维护 Wiki 知识管理）**；**vectorize-io hindsight ★20,431（长期项目记忆：知识页自动召回/会话自动保存/每 repo 共享记忆库；GitHub 侧 ★28,462 347 today）**；anywhere-labs dsh-plugin-desktop ★16,300（Electron 桌面）；**MemTensor MemOS ★10,843（本地四层长期记忆 L1 trajectory/L2 strategy/L3 world model/skills，每用户轮自动检索，注册六种记忆工具）**；yjh051108 dsh-routing-suite ★6,979（injector + router-standard：先装运行时 injector 再装 task-aware 推理模式 router preset，P1-P23）；**Q00 ouroboros ★5,588（uvx 启动 Python 引擎提供 spec-driven AI workflows 作为 MCP 工具：Interview→Seed→Execute→Evaluate→Evolution loop）**；liustack modlens ★3,388；agentscope-ai typescript ★3,374（跨会话记忆 kit）。
- **提升层**：工具 / 可复用 Skill（记忆分层与路由生态索引）。

## 判重说明
- B1 → agentskills.io spec 字段级（allowed-tools/compatibility/name 匹配目录/skills-ref validate/<500 行/一层深），与 C1 三阶段同源增量 ≥40%，落。
- B2 → Anthropic overview 后半（运行时约束三平台/预构建四件套/cross-surface/安全细则），A1 未覆盖增量，落。
- B3 → skillsmp p45 精选（nature-figure/codebase-analysis/zach-search-term/disk-cleaner/ctf-reverse），全新，落。
- B4 → DSH 目录 Top10（weknora/hindsight/MemOS 四层/ouroboros/routing-suite），同生态新条目增量，落。
- 未落：dify blog（intent-based email routing——企业级，背景记录）、Langflow tweaks（中方法记录）、Make 平台事实（低方法）、GitHub trending hindsight（与 B4 同源重复）、Anthropic available-skills 死链、Activepieces 死链（累计计数）。
