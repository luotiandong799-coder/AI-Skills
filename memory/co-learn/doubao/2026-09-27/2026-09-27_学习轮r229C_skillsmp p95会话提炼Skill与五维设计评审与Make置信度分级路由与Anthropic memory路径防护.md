# 学习轮 r229C：skillsmp p95会话提炼Skill与五维设计评审与Make置信度分级路由与Anthropic memory路径防护（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/95（#9401-9436，total_length=10673 首段 3907） | OK |
| 2 | Dify（Template node 编程能力/sys.* 系统变量/LLM prompt 配置） | OK |
| 3 | n8n（Retry-After 尊重/两层错误处理/默认重试状态码清单） | OK |
| 4 | LangFlow（1.10 Assistant 建 flow/1.11 HITL+A2A/1.12 OpenTelemetry/CUGA） | OK |
| 5 | Activepieces（Chat to Automation/Tables 版本化 prompts/AI Adoption Stack） | OK |
| 6 | Make（置信度分级路由/Make MCP Server 3000 apps/Agent SQL） | OK |
| 7 | Pipedream（prebuilt triggers/actions/webhook 唯一 URL） | OK |
| 8 | Anthropic（Memory tool 路径防护/context editing+memory 组合/记忆版本化+并发控制） | OK |
| 9 | GitHub 生态（antigravity-awesome-skills ★46,661 625 技能/MineContext/ECC harness） | OK |
| 10 | WaytoAGI（Agentic Prompting PLAN-EXECUTE-VERIFY/生产 prompts 合集） | OK |

## 独点（4 个）
### C1：skillsmp p95 精选：会话提炼 Skill / 五维设计评审 / 文献四目录（来源：skillsmp.com/skills/page/95，2026-09-27 实拉）
- **make-skill：从会话提炼可复用 Skill（agentscope-ai/QwenPaw ★35,194）**：**从当前会话的可复用决策、知识、模板或工作流创建聚焦 workspace Skill——触发 /make-skill + focus 参数；不做一次性摘要，不做普通文件创建**（可复用 Skill 层：与 skill-creator-for-work 分工——官方创建器管从零写，本方法管"会话里哪些点值得提炼成 Skill"，正是本学习批的落地机制本身）。
- **critique：五维专家设计评审（nexu-io/open-design ★97,471）**：**对任意 HTML artifact 跑五维评审——Philosophy/Visual hierarchy/Detail/Functionality/Innovation 各 0-10 分——输出单文件自包含 HTML 报告：雷达图+证据支撑的分数+三列表 Keep/Fix/Quick-wins**（工作流层：评审=五维评分+证据+三列表，可并入 wb 交付前设计检查）。
- **obsidian-literature-workflow：项目级文献四目录（Galaxy-Dawn/claude-scholar ★5,594）**：**Sources/Papers 存原始文献→合成结果落 Knowledge→写作交接在 Writing→默认画布 Maps/literature.canvas——目录结构本身约束工作流**（工作流层：文献项目按"原始→合成→写作"分目录，天然防污染）。
- **youtube-transcript：字幕多形态重格式化（browser-act/skills ★5,969）**：**YouTube 字幕提取→全部时间戳分段→转成摘要/章节大纲/X 推文串/博客/金句**（工作流层：长视频→多形态输出的重格式化管线，内容再创作个人可用）。
- **patent-drafter：agent team 单次完成专利四件套（revfactory/harness-100 ★1,276）**：**prior art search/claims/specification/drawing descriptions 由 agent 团队协作单次生成**（工作流层：专利草拟面，个人项目可用）。
- **提升层**：可复用 Skill / 工作流。

### C2：Make 置信度分级路由 + Anthropic memory 路径防护与版本化（来源：make.com/en/how-to-guides/llm-integration + docs.anthropic.com + zenml.io，2026-09-27 实拉）
- **置信度分级路由表**：**Any category ≥0.85→自动动作（如 Gmail 起草）；0.7-0.85→人工复核（Slack 消息）；无匹配→fallback 记录（Google Sheets 日志）——分类置信度直接映射到自动化等级，不是"要么全自动要么全人工"**（工作流层：与 WB Fast/Deep 同构——阈值决定自动化深度，低置信度一律进人审）。
- **Memory tool 路径防护**：**实现 client-side handler 时必须拒绝 /memories 之外的路径——路径遍历是 memory 工具第一个安全坑**（安全层：文件类工具 handler 一律校验路径前缀）。
- **记忆版本化 + 并发控制**：**存储所有版本的记忆支持回滚；跟踪每次更新的触发上下文（哪个 session/transcript）和修改者元数据，形成完整审计轨迹；并发写用 hashing 机制防止冲突**（工作流层：长期记忆文件 = 版本化+审计+并发锁，与本学习留痕机制同构）。
- **Context editing + memory 组合**：**上下文接近清除阈值时 Claude 收到自动警告，先写重要工具结果到 memory 文件再被清除——清除前主动保存，不是清除后补救**（上下文管理层：与 wb-context-compressor 互补，压前留痕）。
- **提升层**：工作流 / 安全 / 上下文管理。

### C3：n8n Retry-After 与两层错误处理 + LangFlow HITL/OpenTelemetry + Activepieces Chat to Automation（来源：blog.n8n.io/api-rate-limiting + community.n8n.io + langflow.org + activepieces.com，2026-09-27 实拉）
- **尊重 Retry-After 而不是立即重试**：**429 先查响应头——API 给了 Retry-After 就用它决定等待多久再试；立即重发通常更糟**（工作流层：限流重试以服务端给出的时间为准，不自己拍）。
- **默认重试状态码清单**：**可重试：408/409/425/429/500/502/503/504；不重试：400/401/403/404/422——retryable by default 是有默认值的，403/422 重试纯属浪费**（工作流层：状态码决定重试资格，先分类再重试）。
- **两层错误处理**：**node-level Retry On Fail（maxTries+wait）处理瞬时失败（网络抖动/429）处理大部分；Error Trigger 工作流处理剩下的——告警/dead-letter/记录失败；"re-run the execution"不等于 guaranteed resume**（工作流层：就地重试管可恢复，全局工作流管不可恢复，分工明确）。
- **LangFlow 1.11 HITL + 1.12 OpenTelemetry**：**1.11 增加 gated tool calls 和 reviews（工具调用前人工门控）；1.12 增加 OpenTelemetry 支持（服务健康+flow runs 追踪，进入标准可观测性栈）**（工具层：人审入口和可观测性成为平台标配）。
- **Activepieces Chat to Automation + prompt 版本化**：**自然语言描述工作流→平台生成起始 flow 供精修；prompts 作为 Tables 记录带 version 字段/owners/rollout flags——采样输入跑回归、比较结构化输出、审批升级版本**（工作流层：提示词也要版本管理+回归测试+审批升级，不只是存文本）。
- **提升层**：工作流 / 工具。

### C4：GitHub 生态 + WaytoAGI agentic prompting（来源：awesome-ai-agents.korchasa.dev + zhuangxiaoyi.cn + promptgenius.net，2026-09-27 实拉）
- **antigravity-awesome-skills：625 个高性能 agentic skills 集合（★46,661）**：**跨多平台增强 AI 编码助手，把 agent 变成全栈数字代理**（事实：技能集合形态成为趋势，按需取用不整包装）。
- **ECC：agent harness 性能优化系统（affaan-m/ECC ★264,820）**：**skills/instincts/memory/security/research-first 开发——harness 各维度性能优化成体系**（事实：harness 工程化=技能+直觉+记忆+安全多轨并行）。
- **Agentic Prompting 三步模板（PromptGenius）**：**STEP 1 PLAN（列出子任务+每项用哪个工具/方法）→STEP 2 EXECUTE（逐个执行，每步记录结果是否改变计划）→STEP 3 VERIFY（检查全部子任务完成且一致）——执行前列计划、执行中更新计划、执行后验证一致性**（提示工程层：可复用的 agentic 任务三段式，与 wb-execute-discipline 互补）。
- **MineContext：上下文感知 AI 伙伴（volcengine/MineContext ★5,519）**：**主动收集上下文的 AI 伙伴**（事实：上下文主动采集成为独立产品方向）。
- **提升层**：提示工程 / 工具 / 事实。

## 判重说明
- C1 make-skill（会话提炼可复用点——新，正是本学习批机制本身）；critique 五维评审（r229-B paper-plot 模板互补，五维+雷达图+三列表为独立方法）；literature-workflow 四目录（新）；youtube-transcript 重格式化（新）；patent-drafter（r229-A 判过软著四件套，专利四件套面互补）；落。
- C2 置信度分级路由（阈值→自动化等级映射——新，与 WB Fast/Deep 同构）；memory 路径防护（安全细节新）；版本化+并发控制（r227/r228-B 记忆策略面互补，版本回滚+审计轨迹+并发 hashing 为增量合并）；context editing+memory 组合（r228-B compaction 面互补，清除前主动保存为增量合并）；落。
- C3 Retry-After（新细节）；重试状态码清单（新——具体清单可执行）；两层错误处理（r229-B Error Trigger 面互补，本批"就地重试 vs 全局工作流分工"增量合并）；HITL gated tool calls（r228 HITL 面互补，LangFlow 具体实现增量）；Chat to Automation（新）；prompt 版本化回归（新）；落。
- C4 Agentic Prompting 三段式（r228-B RAILS 互补，PLAN-EXECUTE-VERIFY 模板独立可复用）；ECC/antigravity/MineContext（事实）；落。
- 未落：AI Adoption Stack 企业级仪表盘（企业级不投入）；Agent SQL 场景表（面窄）；Pipedream prebuilt（r229-B Connect 已落）；WaytoAGI Coze 教程（工具换面，方法层无新增量）；promptrefinery 等内容站点（数量堆积淘汰）。
