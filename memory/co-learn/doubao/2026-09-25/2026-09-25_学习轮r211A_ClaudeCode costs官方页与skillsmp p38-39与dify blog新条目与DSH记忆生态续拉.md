# 学习轮 r211-A：Claude Code costs官方页与skillsmp p38-39与dify blog新条目与DSH记忆生态续拉（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/38（#3701-3752） | OK（ponytail-debt/arbor/astro-code-review 等） |
| 2 | dify.ai/blog 续读（4603-10042） | OK（Asqav 可验证收据/Patch 模式） |
| 3 | docs.anthropic.com/claude-code/costs（全 3281B） | OK（团队费率表/agent teams 7x） |
| 4 | docs.openclaw.ai/guides/agent-skills | **link dead**（记死链） |
| 5 | skillsmp.com/skills/page/39（#3801-3843） | OK（watermarks-remover/codegraph/hive-chart） |
| 6 | docs.langflow.org/configuration | **link dead**（记死链） |
| 7 | deepseek-plugin.org/categories/memory | **fetch error**（记死链） |
| 8 | docs.n8n.io/advanced-ai/intro-tutorial（4196/13856 取） | OK（LLM vs Agent 表，低方法） |
| 9 | deepseek-plugin.org/plugins 续读（4458-8857） | OK（mem9/Aegis/CloudBase） |
| 10 | waytoagi.com/ai/awesome | **link dead**（记死链） |

## 独点（4 个）
### A1：Claude Code costs 官方页全量：团队费率建议表 + agent teams 7x + CLI 优于 MCP（来源：docs.anthropic.com/claude-code/costs 全 3281B，2026-09-25 实拉；与 wb-max-token-saver 强相关，官方口径增量）
- **企业费率建议表（TPM/RPM 每用户）**：1-5 用户 200k-300k/5-7；5-20 用户 100k-150k/2.5-3.5；20-50 用户 50k-75k/1.25-1.75；50-100 用户 25k-35k/0.62-0.87；100-500 用户 15k-20k/0.37-0.47；500+ 用户 10k-15k/0.25-0.35——**团队越大每用户 TPM 越低**（并发使用率低），限额在组织级不按个人，个人可临时超算。
- **Agent teams 约 7x token**（teammates 在 plan mode 各持独立上下文窗口）；**teammates 空闲也持续耗 token**；建议 Sonnet 做 teammate；`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 启用；spawn prompt 里每字都从开始加进 teammate 上下文。
- **企业平均成本 $13/开发者/活跃日、$150-250/月**，90% 用户低于 $30/活跃日；背景 token（resume 摘要、/usage 检查）每会话 <$0.04。
- **CLI 工具（gh/aws/gcloud/sentry-cli）比 MCP server 更省上下文**——MCP 无 per-tool listing，只有工具名进上下文直到被用；MCP 工具定义默认 deferred。
- **CLAUDE.md 保持 <200 行**：把专门工作流指令（PR 评审/数据库迁移）移进 skills 按需加载——base 上下文只留 essentials。
- **任务间 /clear 切换**（/rename 先改名→/resume 找回）；/compact 自定义压缩指令（`/compact Focus on code samples and API usage`）+ CLAUDE.md 自定义 compact 行为。
- **hook 预处理省 token**：10,000 行日志文件，hook grep ERROR 只回匹配行——上下文从几万 token 降到几百；skill 给领域知识省探索（codebase-overview skill 描述架构/目录/命名约定，一次调用替代读多文件）。
- **代码智能插件（typed languages）**：一次"go to definition"替代 grep+读多个候选文件；装语言 server 自动报类型错误。
- **extended thinking 默认开启按 output token 计费**，/effort 降级或 `MAX_THINKING_TOKENS=8000`；subagent 委托 verbose 操作（测试/文档/日志，输出留子代理上下文只回摘要）。
- **具体 prompt 省探索**："improve this codebase"（广泛扫描）vs "add input validation to login function in auth.ts"（最小文件读）。
- **提升层**：工具 / 工作流（成本治理的官方口径与可操作策略）。

### A2：skillsmp p38-39 精选：ponytail-debt 债务台账 / arbor HTR 迭代优化 / 评审边界纪律（来源：skillsmp.com/skills/page/38-39，2026-09-25 实拉）
- **ponytail-debt（DietrichGebert/ponytail ★143,784）**：把代码库里所有 `ponytail:` 注释收进债务台账——刻意捷径/延期被追踪而不是烂成 "later means never"；一次性报告、不改任何东西。判据：**延期决策要有显式台账，注释标记只是入口不是终点**——与用户 ponytail 套件直接互补（套件管"怎么留"，debt 管"留了之后怎么还"）。
- **arbor（K-Dense-AI ★45,497）**：Hypothesis Tree Refinement（HTR）自主迭代优化真实产物（代码/训练配方/agent harness/数据流水线/prompt），对目标和评估器——**分支探索竞争想法+防 dev/test 差距 overfit**；Claude 做协调者，子代理在隔离 git worktree 执行。
- **astro-code-review（withastro/astro ★62,721）**：静态只读 PR 评审——**只报 merge 相关发现，从不编辑代码/不运行项目**（边界纪律：评审者不越权执行）。
- **watermarks-remover（★47）**：AI 溯源标记三层剥离——Layer A 不可见 Unicode/空格同形字（确定性）/Layer B 统计 token 采样水印（agent 引导重写 best-effort）/C2PA/EXIF/XMP 元数据（覆盖 Claude/Gemini SynthID-Text/OpenAI/Kirchenbauer）。
- **codegraph（alibaba/neug ★166）**：图数据库（neug）+向量索引（zvec）代码知识图谱——调用图/死代码/热点/模块耦合/**PR 风险评分/冲突检测/auto-merge 候选**/bug 根因。
- **hive-chart（aden-hive/hive ★11,062）**：图表渲染单工具嵌入契约（chart_render 实时图表+PNG 落盘）；**ECharts（数据 viz）vs Mermaid（结构图）决策**；BI 级审美基线（no chartjunk/克制配色/单图单消息）。
- **提升层**：可复用 Skill / 工具。

### A3：dify blog 新条目：Asqav 可验证防篡改动作收据 / Agent patch 现有软件模式（来源：dify.ai/blog 4603-10042B，2026-09-25 实拉）
- **Asqav（Dify Marketplace 生态伙伴）**：Dify Agents 经 Asqav 路由的动作可产出**可验证、防篡改的 receipts（tamper-evident receipts）**——"From Logs to Evidence"，每个 agent 动作可验证。判据：**agent 动作的"可审计性"是市场级卖点**——日志是事后、收据是可验证证据。
- **I Patched Calendly with New Agent**：用 Agent **修补现有软件**（让已有软件按你的方式工作）而不重建整个东西——"patch 而非 rewrite" 模式。
- **Why We Redesigned Dify's Agent**：agents 与 workflows 不是孤立组件，而是支持日常工作的**协作者**。
- **提升层**：工具 / 工作流（可验证动作 + 增量修补）。

### A4：DSH 记忆生态续拉：mem9 云端持久记忆 / Aegis 工作纪律（来源：deepseek-plugin.org/plugins 4458-8857B，2026-09-25 实拉；与 r210-C C5 同域增量）
- **mem9-ai（★1.2k）**：云端持久记忆——**每轮前自动检索相关对话历史、会话结束后写回记忆**，暴露五个记忆工具给模型调用（与 MemOS/hindsight 同域但为"云上+轮前检索+轮后写回"形态增量）。
- **Aegis（GanyuanRan ★1.1k）**：给 AI 编程助手加**工作纪律**——改代码前读项目基线、出错时调查根因、附（后续）——与 wb-execute-discipline 直接同理念，印证方向（业界在把执行纪律做成插件形态）。
- **CloudBase-AI-Toolkit（TencentCloudBase ★1.1k）**：数据库/认证/函数执行后端服务给 AI agents。
- **提升层**：工具 / 工作流。

## 判重说明
- A1 → costs 官方页全量（费率表/7x/CLI vs MCP/CLAUDE.md 行数），与 wb-max-token-saver 同域但为官方量化口径与策略清单，增量 >60%，落。
- A2 → skillsmp p38-39 精选（ponytail-debt/arbor/astro 评审边界/watermarks/codegraph/hive-chart）全新，落。
- A3 → dify blog 新条目（Asqav 可验证收据/Patch 模式）全新，落。
- A4 → DSH 记忆生态续拉（mem9 轮前检索轮后写回/Aegis 工作纪律）为 C5 增量，落。
- 未落：n8n intro-tutorial（与 r209 重叠，教程性低方法）。
