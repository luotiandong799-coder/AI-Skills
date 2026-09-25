# 学习轮 r221B：skillsmp p72精选与自改进Agent基础设施与Langflow 1.12版本面与文件化规划（2026-09-25）

## 实拉记录（10 次调用，5 成功 / 5 失败计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/72（#7101-7160，5998/10237 取） | OK |
| 2 | dify.ai/blog 续读（158991-163733） | OK（Expert Mode 提示词编排/Dataset 增强） |
| 3 | langflow releases 搜索（1.12 OTel/1.12.2 guardrails/1.8.0 streamable HTTP） | OK |
| 4 | docs.n8n.io ask 参数问答接口 | dead（带 ask 参数也拦） |
| 5 | GitHub Trending 搜索（reef/nasiko/zcode/ponytail 145k） | OK |
| 6 | deeplearning.ai 课程搜索（Browser Agents/sandbox coding agents） | OK |
| 7 | docs.openclaw.ai/automation/webhooks | dead |
| 8 | activepieces.com/docs/ 根目录 | OK（首次成功 4399） |
| 9 | skills.sh/faq | dead |
| 10 | agentskills.io/faq | dead |

## 独点（4 个）
### B1：skillsmp p72 精选：文件化规划 / PRD 拆 issue / 文风蒸馏（来源：skillsmp.com/skills/page/72，2026-09-25 实拉）
- **planning-with-files（OthmanAdi ★27,047）**：**基于文件的多步 agent 规划——task_plan.md/findings.md/progress.md 持久落盘，lifecycle hooks 注入所选项目规划上下文；自动恢复只读规划文件（不读别处）；session-catchup.py --metadata 只读同项目本地 agent 会话记录、只发聚合计数（--replay 可发 bounded nonce 框定摘录）；gated 模式仅在宿主支持时请求继续、永不运行 Markdown 里声明的命令；技能无网络上传路径**（文件化规划+隐私边界：恢复范围/计数输出/无上传路径三约束）。
- **prd-to-issues（mattpocock）**：**PRD 拆成可独立工作的问题，每个写成本地 markdown 文件 issues/**（PRD→可执行 issue 的确定性转换）。
- **wjs-distilling-style（jianshuo ★130）**：**从几篇样本文章捕捉作者声音并改写——"蒸馏文风/提炼风格/学笔法改写"，任意作者**（与已有 voice-lock 60% 重叠、含 40% 增量：样本→可复用风格规则、任意作者风格转移，合并保留增量）。
- **design-review（Donchitos ★25,342）**：游戏设计文档评审——完整性/内部一致性/可实现性/符合项目设计标准，**交程序员前必跑**。
- **ppt-template-creator（anthropics/financial-services ★35,854）**：从用户提供的 PPT 模板创建**可复用 PPT template SKILLS（非演示文稿）**。
- **提升层**：可复用 Skill / 工作流。

### B2：GitHub 生态：自改进 agent 持续学习基础设施 + Rust agent 控制平面（来源：GitHub Trending 多站检索，2026-09-25 实拉）
- **Human-Agent-Society/reef**：**Continual learning infra for self-improving agents——自改进 agent 的持续学习基础设施**（自改进闭环的基建面）。
- **Nasiko-Labs/nasiko（8.9k★）**：**开源 Rust 编写的 AI agents developer control plane——CLI + coding-agents + LLM-router 组件，Docker 快速开始免装 Rust**（agent 控制平面的 Rust 实现面）。
- **gitpicks 增速数据**：openclaw/openclaw +1284 stars/day、mattpocock/skills +1152、affaan-m/ECC +1069、obra/superpowers +831、NousResearch/hermes-agent +579（生态头部迁移速度证据）。
- **zai-org/ZCode**：+959/周（TS，代码智能增量）。
- **提升层**：工具 / 工作流。

### B3：Langflow 1.12/1.12.2/1.8.0 版本面 + Activepieces 三构件互调（来源：langflow release notes 检索 + activepieces.com/docs，2026-09-25 实拉）
- **Langflow 1.12（2026-09-01）**：**OpenTelemetry 导出——health traces/metrics/logs 经 OTLP 输出到自有后端**（自托管可观测面，与 r221-A openclaw hooks 的 diagnostic events 同思路不同实现）。
- **Langflow 1.12.2**：**guardrails component 升级——可选 combined rule and model checks（规则+模型双检组合）**。
- **Langflow 1.8.0**：**streamable HTTP transport for MCP client/server 双端——SSE 保留为向后兼容 fallback**（MCP 传输协议演进面）。
- **Activepieces 三构件互调**：**Agents/Flows/Tables 三构件任意互调——agent 可调用 flow、flow 可跑 agent、两者可读写同一 tables；760+ apps；governance and security built in（自带治理与安全）**。
- **提升层**：工具 / 工作流（编排平台构件模型）。

### B4：deeplearning 增量：沙箱代码执行 agent + Computer Use 入门（来源：deeplearning.ai 检索，2026-09-25 实拉）
- **Building Coding Agents with Tool Execution（deeplearning.ai）**：**写代码并执行代码的 agent——在 sandboxed cloud environments 中运行，保护你的系统不受不受信代码**（代码执行 agent 的安全运行面）。
- **Building toward Computer Use with Anthropic（1h47m Beginner）**：AI assistant 如何在电脑上使用并完成任务。
- **Building AI Browser Agents（AGI Inc，1h5m）**：browser agent 用视觉（截图）+结构（HTML/DOM）双模态推理，可登录/填表/点击/下单；AgentQ 深入（r220B 已落 Browser Agents 课程面，本项为深入细节增量）。
- **提升层**：模型（评估）/ 工作流（沙箱执行）。

## 判重说明
- B1 planning-with-files 文件化规划+恢复范围+无上传路径为独有增量；wjs-distilling-style 与 voice-lock 重叠>60% 含增量（任意作者风格转移）合并保留；落。
- B2 reef/nasiko 全新（r220 各轮未落），落。
- B3 Langflow 1.12/1.12.2/1.8.0 为 1.11 之后版本增量；Activepieces 三构件互调首成根目录页，落。
- B4 沙箱代码执行为 deeplearning 增量面，落。
- 未落：n8n ask（拦）、openclaw webhooks（死）、skills.sh/faq（死）、agentskills.io/faq（死）、archify/ponytail（r220 已落，判重不重复）。
