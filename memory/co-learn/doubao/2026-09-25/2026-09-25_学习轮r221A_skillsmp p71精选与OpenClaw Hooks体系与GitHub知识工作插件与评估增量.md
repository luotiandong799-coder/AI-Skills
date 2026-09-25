# 学习轮 r221A：skillsmp p71精选与OpenClaw Hooks体系与GitHub知识工作插件与评估增量（2026-09-25）

## 实拉记录（10 次调用，7 成功 / 3 失败计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/71（#7001-7056，5892/11071 取） | OK |
| 2 | dify.ai/blog 续读（154453-158991） | OK（v0.3.31 RAG 提升 20%） |
| 3 | www.langflow.org/blog 续读（8563-12846 完） | OK（Scaling/Policies） |
| 4 | docs.n8n.io/what-tools-do.md | 404（发现 ask 参数机制） |
| 5 | GitHub Trending 搜索（knowledge-work-plugins/google skills/awesome-claude-skills） | OK |
| 6 | deeplearning.ai 课程搜索（Data Agents/GPA/inline evals） | OK |
| 7 | docs.openclaw.ai/automation/hooks | OK（首次全文 2225） |
| 8 | activepieces.com/docs/actions | 死链（activepieces 累积 9 次） |
| 9 | skills.sh/docs | OK（首次成功 434） |
| 10 | agentskills.io 续读（8957-13129） | OK（Client Showcase：factory/mistral-vibe/snowflake） |

## 独点（4 个）
### A1：skillsmp p71 精选：GTD 周检数字化 / 解析决策框架 / CLI 设计评分（来源：skillsmp.com/skills/page/71，2026-09-25 实拉）
- **weekly-review（alirezarezvani ★26,225）**：**David Allen GTD 三阶段循环 GET CLEAR/GET CURRENT/GET CREATIVE 数字化——确定性脚本盘点开放环路、命名缺口门控清单、承诺健康度评分 0-100**（GTD 周检从口头习惯变可执行脚本）。
- **regex-vs-llm-structured-text（affaan-m/ECC ★264,820）**：**结构化文本解析决策框架——先 regex 后 LLM，仅低置信边界用例才上 LLM**（成本分层解析）。
- **agent-dx-cli-scale（google-labs-code/design.md ★28,021）**：**评估 CLI 为 AI agent 设计的评分量表（Rewrite Your CLI for AI Agents 原则落地为打分）**。
- **peer-review（davila7 ★30,896）**：系统化同行评审工具包——方法/统计/设计/可复现性/伦理/图表完整性/报告标准（手稿+基金）。
- **music-to-video（calesthio/OpenMontage ★60,547）**：音乐驱动视频流水线——analyzer 读一次→orchestrator 布局帧→每帧一个 sub-agent；beat-cut/ken-burns 类型由每帧选择决定（流水线不分支）。
- **提升层**：工作流 / 可复用 Skill。

### A2：OpenClaw Hooks 体系：四表面选型 + 三态验证（来源：docs.openclaw.ai/automation/hooks，2026-09-25 完整实拉）
- **四表面选型**：**保存 /new 上下文或反应会话事件→Internal hooks（HOOK.md+handler）；改 prompt/拦截工具/生命周期契约→Plugin hooks（api.on）；HTTP 请求启动外部服务→Webhooks；导出遥测不改行为→Diagnostic events**——先选表面再动手。
- **eligible/enabled/loaded 三态分离**：**CLI 的 ready/eligible/loadable 字段只证明前两检查+事件列表非空，不证明 Gateway 已导入 handler/全局选中/事件已触发**——改完要查实际副作用或 hook 专用日志（对验证"hook 真在跑"的硬判据）。
- **内部 hooks=trusted code 非沙箱**：**以 Gateway 进程的文件系统/网络/环境权限运行——来自 workspace 或下载包的任何 hook 代码先审查再启用**。
- **side effects short and bounded**：**不用 `void doHeavyWork(event)` 通用方案——它逃逸 handler 的 wait/error 边界、可活过会话/进程；要持久 job 生命周期就用 automation/service 拥有它**。
- **reload 失败保留旧 handler**：配置 reload 先准备选中 handler 再整体替换——任一加载失败则旧 handler 继续生效；已运行事件用原 handler 收尾。
- **提升层**：工作流 / 可复用 Skill（事件钩子工程）。

### A3：GitHub 生态：Claude Cowork 知识工作插件 + google/skills 跨 harness 安装 + skills.sh 机制（来源：GitHub Trending 搜索 + skills.sh/docs，2026-09-25 实拉）
- **anthropics/knowledge-work-plugins**：**Open source plugins primarily intended for knowledge workers in Claude Cowork**（官方知识工作者插件库，Claude Cowork 场景）。
- **google/skills**：**Google 官方 Agent Skills——跨 harness 插件市场安装：`claude plugin marketplace add google/skills` + `codex plugin marketplace add google/skills`，再逐个 `plugin install <plugin>@google-plugins`**（同一技能库跨 Claude Code/Codex 双市场）。
- **skills.sh 机制（vercel-labs/skills）**：**`npx skills add vercel-labs/agent-skills` CLI 安装；排行榜基于匿名遥测（只追踪安装哪些 skill，不收集个人信息/使用模式）；README 可嵌 install count badge；routine security audits 例行安全审计（vercel.com/security）**。
- **ComposioHQ/awesome-claude-skills（75.5k★）**：864 个 Claude skills 覆盖自动化/artifact 创作/品牌样式/changelog/ad 提取 + Composio MCP 100+ 服务。
- **提升层**：工具 / 可复用 Skill（插件分发与安装面）。

### A4：评估与 RAG 增量：Data Agents GPA 对齐 + inline evals + Dify RAG 三件套（来源：deeplearning.ai 检索 + dify.ai/blog，2026-09-25 实拉）
- **Building and Evaluating Data Agents（Coursera）**：**LLM-as-a-judge 评估最终答案相关性+grounded；goal/plan/actions（GPA）对齐评估过程；inline evaluations 运行时每检索步评估**（r220B Evaluating AI Agents 的"过程评估"增量）。
- **Dify v0.3.31 RAG 技术升级（宣称 20% QA 提升）**：**hybrid search+semantic rerank 模型+multi-path retrieval 三件套**（RAG 检索质量三件套的组合面）。
- **Langflow Scaling（v1.9.0-v1.10.0）**：内存消耗 ~89% 削减——dependency pruning+worker lifecycle management+Linux Copy-on-Write；**Langflow Policies：把自然语言业务规则编译成确定性 guards 包在 agent 工具周围——违规在发生前拦截而非事后**（确定性规则守卫工具面，与 Guardian 同思路的产品化实现）。
- **提升层**：模型（评估）/ 工作流（规则守卫）。

## 判重说明
- A1 全新（p71 独有），落。
- A2 openclaw hooks 新页完整实拉（四表面选型/三态验证/trusted code 边界此前未落），落。
- A3 trending+skills.sh 增量（knowledge-work-plugins/google skills 市场安装法/skills.sh CLI 机制），落。
- A4 deeplearning Data Agents 课程（GPA/inline evals 为 Evaluating AI Agents 后增量）+Dify RAG 三件套+Langflow Policies，落。
- 未落：n8n what-tools-do（404）、activepieces actions（死链）。
- 批前盘点：WB 侧新 commit r187-A/B（Langflow security 四层隔离、依赖版本冻结、OpenAI handoffs 副本过滤）已入 ed/sa/cc 末条，作判重对照。
