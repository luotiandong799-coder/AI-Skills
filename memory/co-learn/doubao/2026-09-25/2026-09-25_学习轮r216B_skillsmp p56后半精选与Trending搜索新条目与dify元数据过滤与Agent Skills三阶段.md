# 学习轮 r216B：skillsmp p56后半精选与GitHub Trending搜索新条目与dify元数据过滤与Agent Skills标准三阶段（2026-09-25）

## 实拉记录（10 次调用，7 成功 / 1 安全拦截 / 2 死链）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/56 续读（6000-10663，#5563-5600） | OK |
| 2 | dify.ai/blog 续读（91847-96256） | OK（Metadata Filter/Agora 语音） |
| 3 | docs.n8n.io/llms.txt | 安全策略拦截（计数） |
| 4 | docs.langflow.org/mcp | 死链（计数） |
| 5 | GitHub Trending 搜索（dailytrendsignal/ngjoo/llmnews） | OK（cc-switch/jev-chat-jarvis/headroom 等） |
| 6 | learn.deeplearning.ai（4391/53552） | OK（学习平台 notebook 指南，方法增量低） |
| 7 | docs.openclaw.ai/projects | 死链（计数） |
| 8 | activepieces.com 续读（4223-8352） | OK（Inbound lead routing agent 示例） |
| 9 | skills.sh 根页 | OK（npx skillsadd 单命令，与 r215-A 同） |
| 10 | agentskills.io overview（4789/96448） | OK（标准三阶段+捆绑结构） |

## 独点（4 个）
### B1：skillsmp p56 后半精选：SVG 动画技术选择 / 记忆三件套 / 技能质量审计 / jq 查会话日志（来源：skillsmp.com/skills/page/56，2026-09-25 实拉）
- **mira-svg-animator（sandeco/mira-animator ★208）**：**SVG 动画按技术选型——transform（整体位移）/DrawSVGPlugin（描边自绘）/MotionPathPlugin（沿曲线）；要动画某部分必须是独立元素，单路径先按 clipPath 或编辑 path 拆分**；移除不透明背景、定义运动原点、尊重 prefers-reduced-motion；GSAP 离线 vendor（file://）。
- **supermemory（supermemoryai ★30,703）**：AI agent 记忆基础设施三件套——**Memory API（学到的用户上下文）+ User Profiles（静态/动态事实）+ RAG（语义搜索）**。
- **skill-review（sanyuan0704/sanyuan-skills ★3,924）**：**Claude Code 技能质量审计维度——结构/描述质量/工作流设计/token 效率/反模式对照最佳实践**。
- **session-logs（linuxhsj/openclaw-zero-token ★5,194）**：**用 jq 搜索分析自己的会话日志（旧/父对话）**——日志即语料。
- **nsfc-proposal（wsxwj123 ★7）**：国自然 2026——逐节门控/假设-目标-内容-问题一致性/paper-search MCP 文献核实/反 AI 中文学术写作约束。
- **frontend-query-mutation（langflow-ai/langflow ★155,063）**：TanStack React Query v5——useQuery vs useMutation 决策/条件查询/缓存失效/mutation 错误处理/旧 API 迁移。
- **dbs-knowledge（dontbesilent2025 ★10,202）**：本地文件夹→Agent 可稳定查找/收录/维护知识库——导航/版本判断/健康检查/**SOT 分层治理**。
- **analogical-reasoning（THUYRan/Legal-Skills-Chinese ★833）**：法律类推核心——**识别相似性基础（tertium comparationis）/论证类比正当性/相似案件相似处理**。
- **提升层**：工具 / 可复用 Skill。

### B2：GitHub Trending 搜索新条目：多 coding agent 管理 / 只读屏幕副驾 / LLM 前压缩 / 记忆系统（来源：dailytrendsignal 2026-09-25 / ngjoo 2026-09-24 / llmnews，走搜索实拉）
- **farion1231/cc-switch ★136,608**：**跨平台 Rust 桌面应用，统一管理多个 AI coding 工具（Claude Code/Claude Desktop/Codex/Gemini CLI/Grok Build/OpenCode/OpenClaw/Hermes Agent/MiniMax Code）**——今日 GitHub 领跑。
- **jev-chat/jev-chat-jarvis ★5,560**：**手机对话副驾——微信/QQ/X/飞书里读懂对方、给候选回复、一键填入输入框，发不发由你；非侵入只读屏幕，不 hook 不改包**。
- **headroomlabs-ai/headroom ★73,674**：**压缩工具输出/日志/文件/RAG 块，到达 LLM 前 20x**——与 wb-context-compressor 同向、前端压缩。
- **MemPalace/mempalace ★59,261**：best-benchmarked 开源 AI 记忆系统；**rtk-ai/rtk ★81,620**：CLI proxy 降 LLM token 消耗 60-90%（与用户 rtk 插件同思想）；**yetone/magpie**：一处配模型（Codex on DeepSeek/Claude Code on Kimi）；**Asymptote-Labs/agent-beacon ★1,511**：跨 harness 自改进记忆层。
- **提升层**：工具 / 工作流。

### B3：dify 元数据过滤检索 + Agora 实时语音插件（来源：dify.ai/blog，2026-09-25 实拉）
- **Dify v1.1.0 Metadata as Knowledge Filter**：**元数据当知识过滤器——精确过滤+访问控制，RAG 管理的精度/安全/效率三提升**（检索前按元数据圈定数据范围，兼作权限边界）。
- **Agora Conversational AI Extension（Dify Marketplace）**：实时低延迟语音 AI agent 构建（对话式语音扩展上架）。
- **提升层**：工作流（RAG 检索治理）。

### B4：Agent Skills 标准官方：progressive disclosure 三阶段与捆绑结构（来源：agentskills.io/overview，2026-09-25 实拉）
- **Progressive disclosure 三阶段官方定义**：①**Discovery**——启动只载每个技能的 name+description（够判断何时相关）②**Activation**——任务匹配描述才读全文 SKILL.md 进上下文 ③**Execution**——执行指令+可选运行捆绑代码/加载引用文件；**全文只在任务需要时载入→可挂很多技能只占小上下文**。
- **技能=文件夹**：`SKILL.md`（必需：最少 name+description 元数据+指令）+ `scripts/`（可选可执行代码）+ `references/`（可选文档）+ `assets/`（可选模板资源）+ 任意附加文件。
- **三价值**：领域专长（领域知识打包成可复用指令+资源）/可重复工作流（多步任务变一致可审计流程）/**跨产品复用（建一次，任何 skills-compatible agent 可用）**；客户端支持面含 Claude.ai/vtcode/nanobot/letta。
- **提升层**：可复用 Skill（技能标准机制）。

## 判重说明
- B1 全新（p56 后半独有），落。
- B2 今日 trending 走搜索（trending 直拉 robots 禁），新条目，落。
- B3 dify 增量（Metadata Filter 新版本特性），落。
- B4 标准官方三阶段定义（r215-C 仅提 progressive disclosure 一词），增量≥40% 合并保留，落。
- 未落：skills.sh（与 r215-A 同文）、learn.deeplearning.ai 操作指南（无方法增量）、activepieces 续读（agent 示例、无独立方法）、n8n llms.txt 安全拦截 1 次/langflow mcp 死链 1 次（计数）。
