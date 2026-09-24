# 学习轮 r204-A：ClaudeCode成本管理八法与outcome反馈闭环与行为保持重构与论文配图双格式与agent工作流记忆（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/en/guides/workflow/ | OK（614 字：Workflow vs Chatflow 节点差异） |
| 2 | docs.n8n.io/advanced-ai/intro-tutorial/ | OK（3041+ 字：LLM vs Agent 对比表） |
| 3 | docs.n8n.io/advanced-ai/agent-architecture/ | 死链 |
| 4 | docs.langflow.org/configuration | 死链 |
| 5 | pipedream.com/docs/http/ | OK（8585 字：pre-built actions/HTTP Request Action/auth 自动配置） |
| 6 | docs.anthropic.com/en/docs/agents-and-tools | 区域限制 |
| 7 | docs.anthropic.com/en/docs/claude-code/costs | OK（3281 字：成本管理全页） |
| 8 | skills.sh/trending | OK（2143 字：190 项榜单，anthropics/obra/wshobson/baoyu 家族） |
| 9 | skillsmp.com/skills/page/18 | OK（10735 字：#1701-1773） |
| 10 | openagentskill.com/api | OK（4368 字：API Reference 全端点） |
| 11 | deepseek-plugin.org/plugins | OK（#23-25 与 r203-C 重复，无新增） |
| 12 | general_search Make AI agent | OK（官方 best practices + blog 失败模式表 + workflow memory） |
| 13 | general_search GitHub trending | OK（claude-code/cline/jev-chat/Grok Build/repomix 确认） |
| 14 | waytoagi.com/roadmap、/tools | 死链 |

## 独点（5 个）
### N1：Claude Code 成本管理八法：hooks 预处理减 context / CLAUDE.md 瘦身到 <200 行 / /compact 自定义压缩指令 / MCP deferred 加载（来源：docs.anthropic.com/en/docs/claude-code/costs）
- **hooks 预处理数据，不让 Claude 读原始大文件**：PreToolUse 钩子 grep 日志只回 `ERROR` 行——万行日志从数万 token 降到几百 token；"codebase-overview" 技能给架构上下文免探索。
- **CLAUDE.md 瘦身门槛：<200 行只装核心**——详细工作流指令（PR review/DB 迁移）搬进 on-demand skills，否则每会话都付这些 token。
- **/compact 自定义压缩指令**：`/compact Focus on code samples and API usage` 告诉压缩保留什么；CLAUDE.md 里也可写 Compaction 指令段。
- **MCP tool definitions deferred by default**：默认只载工具名，用工具时才进 context；CLI 工具（gh/aws/gcloud）比 MCP 省（零 per-tool 列表）；`/mcp` 停用不用的 server。
- **子代理委托 verbose 操作**：跑测试/查文档/处理日志放子代理，输出留在子代理 context 只回摘要；团队模式比普通会话贵约 7x（各自 context window），任务要小而自含。
- **/usage 本地估算 + /clear+/rename+/resume 会话管理**：切换任务先 rename 再 clear，防止 stale context 每消息付钱。
- 判据：**先让钩子把数据变小，再让模型读**；CLAUDE.md 是常驻成本，超过 200 行就该拆进技能。
- **提升层**：工作流 / 上下文管理。

### N2：技能注册表的结果反馈闭环：outcome 六态+版本归因 → Agent Proven 背书分 → evals 预安装评估门 → 稳定回执（来源：openagentskill.com/api 全端点，r203-B L1 的深度增量）
- **POST /api/agent/outcome**：六结果态 `success/failed/not_relevant/blocked_by_risk/setup_required` + `output_quality 1-5` + `used_in_production` + `human_review_required` + `error_type(install_failed/runtime_error/permission_blocked/low_quality_output/timeout/other)` + **`source_version{version,commit_sha,content_hash,ref,path}` 版本归因**（从 resolve receipt 复制并对照源历史核验）——反馈可审计到具体版本。
- **Agent Proven Score**：由 outcomes 总量/近期成败/安装成功率/输出质量/生产使用/独特 agent 数/风险与 setup 惩罚合成——0-100 背书分，排行 `rankings?slug=agent-proven`。
- **GET /api/agent/evals（预安装评估门）**：`status: passed|review|failed` + `decision: shortlist|manual_review|do_not_auto_install` + `validation_plan`（生产前具体沙箱验证步骤）——装之前先过门，不只信 trust 分。
- **GET /api/agent/receipt**：稳定安装回执（selected skill/install/safety/risk notes/alternatives/outcome event id）——pre-install 执行记录。
- **integration-kit**：`/.well-known/agent-manifest.json` + supported_agents/recommended_flow/stable_response_fields/safety_rules 平台模板——agent 先取模板再调 resolve。
- 判据：**安装不是终点，outcome 回传形成闭环**；版本归因让"哪个版本好用"可回答；预安装评估门 + 沙箱验证计划 = 装前纪律。
- **提升层**：工具 / 工作流。

### N3：行为保持重构纪律（orch-refine-code）：绿→重构→绿→review→gated commit（来源：skillsmp #1701，affaan-m/ECC）
- **行为保持重构闭环**：确认测试绿 → 重构（结构改善但不改行为）→ 测试保持绿 → review → **gated commit**（门控提交）。
- 触发：结构该改善但行为不能变时——**重构的验收 = 行为不变**，不是"看起来更整洁"。
- 判据：**"行为不变"用测试绿来证明**，重构与功能变更分开提交，门控防混入。
- **提升层**：工作流。

### N4：论文配图双格式管线（thesis-figure-skill）：LaTeX/TikZ 结构化 + draw.io XML 装饰，统一"分析→画图指令→代码→编译验证→交付"（来源：skillsmp #1763，NeverSight/learn-skills.dev）
- **双格式按用途分流**：TikZ 适合系统架构/数据流/几何示意（可直接嵌入论文）；draw.io XML 适合技术路线图/科研展示/学术汇报配图（渐变色/阴影/自由布局，app.diagrams.net 可编辑）。
- **统一工作流**：分析输入（文案/图片/论文）→ 画图指令 → 代码生成 → **编译验证** → 满分交付；自动识别论文领域并以该领域专家身份配图。
- 判据：**配图也过编译验证**，代码生成的图必须能编译；先定格式再画，不混两种输出。
- **提升层**：工具 / 可复用 Skill。

### N5：Agent 工作流记忆与失败模式表：lookup 无记录三选一 / run 失败后 reconcile 状态 / 验证放 AI 模块前 / 自信误分类与输出丢字段两失败模式（来源：make.com/en/blog/agent-workflow-memory + /en/blog/llm-agents + baeseokjae Make AI Agents Guide 2026）
- **lookup 无记录三选一**：初始化状态 / 延迟处理 / 升级人——不是静默空跑。
- **run 失败后的状态对账**：agent 已决策并发响应后 run 失败 → 把 bundle 路由进错误处理路径 reconcile 状态，等下次触发前先对齐——**防止"决定做过了但状态没改"**。
- **验证节点放 AI 模块前**：条件分支缺失字段、防无效记录污染状态（与 M4 错误对象互补：那个管工具报错，本条管数据入口）。
- **两失败模式表**：①agent 自信误分类输入（边缘案例 prompt 没见过：第二语言工单/双分类主题/测试集外账号类型）→ 下游人发现投错团队，"输出看起来对"最危险；②结构化输出丢必填字段（短/异常格式输入→部分 payload）→ 下一模块静默失败或写空白值。
- **confidence scoring**：agent 自评置信度 0-100，<70% 升级人审；**Reasoning Panel 推理轨迹留痕**用于合规审计。
- 判据：**记忆的状态要可 reconcile**；失败模式表是排查入口；置信度低就升级，不硬跑。
- **提升层**：工作流。

## 判重说明
- N1 → wb-context-compressor/wb-max-token-saver 已有压缩与成本层；"hooks 预处理数据 + CLAUDE.md <200 行 + /compact 自定义指令 + MCP deferred"为独有增量（≥40%），合并保留。
- N2 → r203-B L1 已录四层+resolve；"outcome 反馈闭环/Agent Proven/evals 预装门/receipt/integration-kit"为深度增量，落。
- N3 → 与 image-to-code 六纪律/收 diff 五连查不同：专管行为保持重构闭环，独点，落。
- N4 → 论文配图双格式管线（TikZ/draw.io+编译验证），与论文写作套件互补，独点，落。
- N5 → r203-C M4 已录错误对象+人审；"lookup 三选一/失败后 reconcile/验证前置/失败模式表/置信度阈值/推理轨迹留痕"为独有增量，落。
- skills.sh 家族（anthropics/obra/wshobson/baoyu）→ r202-A 已录集中趋势，本轮仅确认不重复落；caveman-compress 与用户 caveman 插件同源不落。
