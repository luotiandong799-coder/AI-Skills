# 学习轮 r226B：skillsmp p87精选与Agentic RAG动作路由与SKILL.md简洁三问与剪映headless与RAG提示词三层（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/87（#8601-8653 实拉） | OK |
| 2 | Dify 检索（Blog/Marketplace：Agentic RAG 模板/SchemaRAG 插件） | OK |
| 3 | n8n 检索（Agentic Workflow Patterns/表达式/模板库） | OK |
| 4 | LangFlow 检索（Custom Python components/extension bundles） | OK |
| 5 | Activepieces 检索（AI Agent Builder/Piece Definition） | OK |
| 6 | Make 检索（新函数/Scenario Blueprint） | OK |
| 7 | Pipedream 检索（Triggers 文档/Component API） | OK |
| 8 | Anthropic 检索（Skill authoring best practices） | OK |
| 9 | GitHub 生态（firecrawl best repos/hype.replicate 2026-09-21） | OK |
| 10 | WaytoAGI/RAG 提示词检索（sureprompts/wickedsmartdata） | OK |

## 独点（4 个）
### B1：skillsmp p87 精选：招聘初筛闭环 / 服务器巡检并发 / 海报元技能路由 / 角色演技（来源：skillsmp.com/skills/page/87，2026-09-27 实拉）
- **boss-daily-brief-v2（Viy1204/boss-daily-brief ★109，中文）**：**Boss 直聘每日招聘初筛完整闭环——CLI 拉候选人列表和简历→AI 初筛生成推荐等级→写入飞书云文档+多维表格→推送文档链接到飞书机器人；首用 "boss init" 初始化，日常一句话触发**（招聘自动化闭环面：CLI 拉数据→AI 评分→飞书双写→机器人推送）。
- **linux-perf-check（wanghel2020/linux-perf-check ★32，中文）**：**SSH 远程 Linux 全量巡检——模块级 5 线程并发把单机全量巡检从 20+ 分钟压到 1-2 分钟，阻塞模块自动跳过不卡死；MySQL 深度诊断 23 项（健康/安全审计/锁分析/备份调度/SQL 审核）；安全约束：SSH 密钥登录禁止密码、仅只读命令、数据库仅 SELECT**（巡检性能面：并发+只读安全约束）。
- **dog-poster（ZhouYinLong-lab/Dog-Skills，中文）**：**海报设计元技能——上游风格询问确定需求，下游自动路由到三个生成器：信息图风→article-poster、通用设计→canvas-design、手工拼贴→torn-paper-collage-poster**（元技能路由面：风格询问→工具路由，与 r225-C agent 路由互补）。
- **storyboard-character-acting（2799662352/ai-image-master，中文）**：**修复 AI 视频角色"NPC感/假笑/用力过猛"演技——把"开心/生气/悲伤"情绪标签改写成微表情序列+协同肢体小动作+环境声音线索**（角色演技面：情绪标签→微表情序列）。
- **video-copy-analyzer（ALBEDO-TABAI/video-copy-analyzer ★209，中文）**：**视频文案一站式——下载在线视频（B站/YouTube/抖音）+FunASR 高速中文语音转录+自动校正文稿+三维度分析（TextContent/Viral/Brainstorming）**（中文转写面：FunASR 本地转写）。
- **提升层**：工作流 / 可复用 Skill。

### B2：Agentic RAG 动作路由 / SchemaRAG / Make 新函数与场景蓝图（来源：marketplace.dify.ai + dev.to Dify 5 Hidden Uses + help.make.com 2026-07-29 + thinkbot.agency 2026-04-08，实拉）
- **Agentic RAG 动作路由（Dify Marketplace Legal Research Agent 模板）**：**Agent 节点检查用户问题并选择动作：搜预建 Qdrant collections 或做 Google web search——检索与网络搜索在动作层分流**（r225-B 混合检索互补：动作级路由而非仅多路检索模式）。
- **SchemaRAG 插件（joto/schemarag）**：**自动创建数据库 schema 知识库来构建 RAG——包含 natural language to SQL 功能**（DB schema→RAG→NL2SQL 面，新）。
- **Make 新函数（2026-07-29 release）**：**arraydiff/arrayintersect/set/escapejson 四个内置函数——直接在映射字段比较数组、更新集合、准备原始 JSON，减少模块数**（映射字段内数据转换面）。
- **Make Scenario Blueprint（thinkbot）**：**生产级 scenario 蓝图——contract-first（稳定输入输出使场景可复用）+routers/subscenarios/data stores/标准化 payload+重试/幂等/限流/日志/告警/运行历史诊断+治理（文档/版本/环境分离）**（模块化场景架构面）。
- **提升层**：工作流 / 工具。

### B3：SKILL.md 简洁性三问 / custom commands 并入 skills / n8n agentic 度分级（来源：platform.claude.com agent-skills best-practices 2026-09-03 + code.claude.com/docs/en/skills + n8nlogic.com 2026-06-05，实拉）
- **SKILL.md 简洁性三问（Anthropic 官方）**：**上下文窗口是公共资源——启动时只预载所有技能的 metadata（name+description），SKILL.md 仅在相关时加载；默认假设"Claude 已经很聪明"，对每段信息挑战三问：①Claude 真的需要这个解释吗 ②能假设 Claude 知道吗 ③这段值得它的 token 成本吗；好例约 50 token vs 坏例约 150 token**（SKILL.md 简洁判据，与 r224-B SKILL.md 规格互补）。
- **custom commands 已并入 skills**：**.claude/commands/deploy.md 与 .claude/skills/deploy/SKILL.md 都创建 /deploy 且工作相同；skills 增加支持文件目录、frontmatter 控制谁调用、按需自动加载**（命令与技能统一面，新事实）。
- **n8n agentic 度分级（n8nlogic）**：**大多数 "agentic" n8n workflow 不该是 agentic——默认确定性 pipeline + 单个 AI Agent node 做唯一真正需要判断的推理步骤；需要工具选择才用单 agent+tools；只有存在各自需要独立 system prompt 和工具集的技能域才用 orchestrator+sub-agents（AI Agent Tool 子节点）；每个 agent 需要 Max Iterations 上限、紧凑工具列表、存在的理由**（agentic 度分级面——与 wb-execute-discipline 简单不深判同源）。
- **提升层**：可复用 Skill / 工作流。

### B4：剪映 headless / MCP 供应链扫描 / RAG 提示词三层与五部分（来源：hype.replicate.dev 2026-09-21 + firecrawl.dev + sureprompts.com 2026-04-12 + wickedsmartdata.com 2026-09-23，实拉）
- **jianying-headless（mcncarl ★2,227）**：**剪映原生草稿隔离编辑/导出 + 独立 Agent Skill——草稿原生处理不走 GUI**（剪映自动化面，新）。
- **Bumblebee（Perplexity）**：**扫描依赖和 MCP servers 的供应链威胁**（MCP 供应链安全面——与 OWASP 工具面安全互补：装 MCP 前先扫）。
- **RAG 提示词三层（sureprompts）**：**RAG prompts 三层——system prompt（定义检索规则）/query prompt（改善抓取）/synthesis prompt（忠实使用检索块）；最大生产失败来自 synthesis prompts 没强制引用或让模型在检索上下文外作答**（RAG 提示词层，与 r225-B 混合检索互补）。
- **RAG system prompt 五部分（wickedsmartdata）**：**①角色与专长定义 ②grounding 指令 ③引用与归属规则 ④"我不知道"协议 ⑤格式与长度指导**（可直接复用的 RAG system prompt 模板）。
- **提升层**：工具 / 工作流。

## 判重说明
- B1 全为新面（招聘闭环/巡检并发/海报元技能/角色演技/中文转写），落。
- B2 Agentic RAG 动作路由（动作级）与 SchemaRAG 新；Make 新函数与 Scenario Blueprint 新；落。
- B3 SKILL.md 简洁三问（50/150 token 判据）为 r224-B 规格的新增量；commands 并入 skills 新事实；n8n agentic 度分级全新；落。
- B4 jianying-headless/Bumblebee/RAG 三层全新；落。
- 未落：Activepieces AI Agent Builder（HITL 面与 r225-C/r226-A 重叠>60%）；Pipedream x-pd 参数（个人价值弱）；text-humanizer（检测器绕过，原则争议）；LangFlow 自定义组件骨架（与 r226-A bundle 面重叠）。
