# 学习轮 r223A：skillsmp p77精选与Make-Pipedream AI Agent面与国内技能平台生态与跨会话记忆工具面（2026-09-26）

## 实拉记录（10 次调用，7 成功 / 3 失败计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/77（#7601-7663，5999/10026 取） | OK |
| 2 | Make.com 检索（AI Agent New/Reasoning Panel/sub-agents） | OK |
| 3 | Pipedream 检索（Edit with AI/MCP Server/Embedded builders） | OK |
| 4 | 腾讯 SkillHub 检索（1.3万→7万 skills/SkillPay） | OK |
| 5 | 阿里虾小宝/百炼检索（JVS Claw/Skill 能力包） | OK |
| 6 | 智谱 AgentMore/AutoClaw 检索（零Token/GLM Office） | OK |
| 7 | gaojihao.github.io/github-hot | dead（security 拦） |
| 8 | docs.openclaw.ai/concepts/retry-policy | dead |
| 9 | GitHub trending 搜索替代（github.hot/StartupCorners/yuxiaopeng） | OK |
| 10 | deeplearning.ai 检索（Agentic AI/Agent Skills with Anthropic） | OK |

## 独点（4 个）
### A1：skillsmp p77 精选：仓库级失败沉淀 / 交互状态序列审计 / 内容哈希缓存（来源：skillsmp.com/skills/page/77，2026-09-26 实拉）
- **harness-engineering（github/awesome-copilot ★39,255）**：**仓库级 harness 工程——把重复 AI coding-agent 错误变成持久指令、漂移检查、回归测试、失败记忆、采用报告（tailored to target repository）**（把失败沉淀做成仓库级闭环，与 wb-debug-loop 失败经验记忆互补——那条管"按错误签名索引"，本条管"仓库级落地形态"）。
- **click-path-audit（affaan-m/ECC ★264,820）**：**用户按钮/触点完整状态变更序列追踪——找"功能各自正常但互相取消、生成错误终态、UI 留矛盾状态"的 bug**；用于系统性调试已找到但用户报按钮坏的场景、共享状态 store 大重构后。
- **content-hash-cache-pattern（ECC）**：**SHA-256 内容哈希缓存高成本文件处理结果——路径无关（同内容换路径仍命中）、自动失效（内容变哈希变）、服务层隔离**。
- **agent-introspection-debugging（ECC）**：AI agent 故障结构化自调试——捕获/诊断/封存恢复/内省报告。
- **harness 前向参考**：**prd-writer（chituai ★268）**——vibe coding 场景非 PM 用户从零写 PRD，**即使描述简短也要触发不跳过**；**detect-foreign-keys**——启发式+值重叠+引用完整性识别外键。
- **提升层**：可复用 Skill / 工作流。

### A2：Make AI Agent 推理面板与上下文供给 + Pipedream Edit-with-AI（来源：Make/Pipedream 检索，2026-09-26 实拉）
- **Make AI Agent (New) app（2026-09 open beta）**：创建 agent/加工具/加知识/聊天测试；所有计划可用（自定义 provider 连接在付费计划）。
- **Reasoning Panel**：**实时查看 agent 怎么想、调用哪些工具、为何走每条路径——build with confidence / debug faster / prove what happened**（推理透明面板，与 r222 progress-drafts 的"进度流"互补：那条管进度播报形态，本条管"推理过程可视化面板"）。
- **上传文件即上下文**：**给 agent 上下文只需上传文件，无需自建 RAG+vector DB**（vs n8n 需自定义 RAG）；agents 可跨团队/工作流共享，可经 Make MCP server 变可调用工具；Make AI Sub-Agents 产品化。
- **Pipedream Edit with AI**：**工作流构建器里用自然语言编辑现有 workflow（改 header 或 code step）**；Embedded workflow builders（把 Pipedream 核心嵌入自研 app）；MCP Server 暴露 3000+ APIs 为 agent 工具；被 Workday 收购（2025-12）。
- **提升层**：工具 / 工作流（可视化编排平台面）。

### A3：国内技能平台生态面：腾讯 SkillHub / 阿里百炼 / 智谱 AgentMore（来源：腾讯云/阿里云/智谱检索，2026-09-26 实拉）
- **腾讯 SkillHub（2026-03-11 上线，基于 OpenClaw 生态）**：**本土化镜像平台——中文搜索、国内节点分发、全量安全扫描去恶意/侵权、Top50 精选榜、兼容 WorkBuddy/QClaw；skills 从 1.3 万+（3 月）到 7 万+（6 月）；SkillPay 月下载 1700 万+、累计 6000 万+；全球 AI Skill 近 30 万、日均新增 1300+**；效率智能体工具集（TokenHub 多模型统一调度+SkillHub 生态、微信/企微触点 Agent 化）。
- **阿里百炼 Skill 能力包（2026-08）**：**技能以 zip 包封装工具组合与文档，上传后经安全扫描方可挂载，挂载时锁定具体版本号**（与 ed"依赖版本引入时刻冻结"同源，平台级实现）；智能体托管运行时 API（平台托管会话与工具执行）；JVS Claw（手机端一键养虾，多模型：百炼/GLM/Kimi/DeepSeek/OpenAI 兼容端点）；Qoder Skill Center 批量导入+一步配置（导入 skills+配 MCP 权限+创建 Agent）。
- **智谱 AgentMore**：**Skills 广场三来源（官方严选/SkillHub/开源社区）一键安装、调用技能零 Token 消耗；多 Agent 群组协作（最多 5 个并行，头脑风暴/任务分配模式）**；AutoClaw 自进化（经用户确认写入记忆成持久能力）+**GLM Office Skills 五件套（PPT/DOCX/XLSX/PDF/Charts）细分场景技术路线（HTML/LaTeX 分流）+视觉按论文/合同/简历/海报/商业设计差异化**。
- **提升层**：工具 / 可复用 Skill（平台与分发生态）。

### A4：GitHub 跨会话记忆与代码图谱工具面（来源：GitHub trending 搜索替代，2026-09-26 实拉）
- **claude-mem（★94,437）**：**跨会话持久上下文——捕获 agent 会话期间一切→AI 压缩→注入相关上下文回未来会话；兼容 Claude Code/OpenClaw/Codex/Gemini/Hermes/Copilot/OpenCode 多框架**（记忆工具实现，与 wb-context-compressor 方法论互补——那条管"何时压怎么压"，本条管"全捕获→压缩→再注入"的闭环工具）。
- **LoopX（2026 W33 trending #1）**：**长时运行 agent 加持久状态——目标/待办/证据/交接跨会话继续；agent 可以换，但项目不随一次对话结束而失忆**（"agent 可换、项目不失忆"判据）。
- **CodeGraph**：**本地代码智能图谱（Tree-sitter 解析函数/类/调用/测试关系持久化）——改文件时沿图找受影响的调用方与依赖代码，提供精准上下文，避免读整个代码库浪费 token**（图结构上下文节省）。
- **cloudflare/security-audit-skill**：**多阶段安全审计、独立验证、机器可读 findings**（与 r222 工具面安全审计互补——机器可读 findings 面）。
- **提升层**：工具 / 工作流（记忆与上下文供给）。

## 判重说明
- A1 harness-engineering/click-path-audit/content-hash-cache 全新面，落。
- A2 Make/Pipedream 平台面为首次实拉新面（Reasoning Panel/上传文件上下文/Edit-with-AI），落。
- A3 国内技能平台生态为首次实拉新面（SkillHub 数据/百炼 zip 版本锁定/AgentMore 零 Token），落。
- A4 claude-mem/LoopX 与 wb-context-compressor 方法论重叠>60% 但含≥40% 工具实现增量（全捕获→压缩→注入闭环/agent 可换项目不失忆）合并保留增量；CodeGraph 图结构上下文节省新面，落。
- 未落：deeplearning Agentic AI 课程（r21x 已落 agentic 设计模式面）、github trending 死链。
