# 学习轮 r201-C：Pipedream事件追踪键与意图访谈95阈值与DSH插件生态与并行agent舰队（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/concepts/ | 死链 |
| 2 | docs.n8n.io/advanced-ai/ | OK 1742 字（导航 + Cluster nodes 概念） |
| 3 | docs.langflow.org/configuration/ | 死链 |
| 4 | make.com/en/help/scenarios/scenario-settings | fetch error |
| 5 | pipedream.com/docs/workflows/events/ | OK 全文 1293 字 |
| 6 | docs.anthropic.com/en/docs/claude-code/ci | 死链 |
| 7 | skills.sh/hot | OK 首页（41830 字大页，前段返回） |
| 8 | skillsmp.com/skills/page/11 | OK（#1001-1035） |
| 9 | deepseek-plugin.org/plugins | OK 96587 字（大目录前段） |
| 10 | GitHub 生态（trendshift weekly 搜索） | OK |

## 独点（4 个）
### F1：Pipedream 事件数据/元数据分离 + trace_id 多执行关联键 + 队列保留上限（来源：docs.pipedream.com/docs/workflows/events 全文）
- **event 与 context 两槽分离**：`steps.trigger.event` 存事件数据（HTTP：body/client_ip/headers/method/path/query/url；Cron：interval_seconds/cron/timestamp/timezone_configured/timezone_utc；Email 走 Amazon SES 结构）；`steps.trigger.context` 存执行元数据：deployment_id（工作流版本全局唯一）/ id（每执行唯一）/ owner_id / platform_version / replay（是否 UI 重放）/ **trace_id** / ts / workflow_id / workflow_name。
- **id vs trace_id 的分工是重试追踪键**：同一原始事件触发多次执行（auto-retry 重试 3 次、$.flow.suspend() 挂起后续跑）——**每次执行的 id 都变，但 trace_id 不变**；"一个事件产生了哪些执行"用 trace_id 聚合，"这一条执行"用 id 定位。
- **事件队列保留上限**：Free/Basic 每工作流只保留最后 100 个事件，超了删最旧；Advanced/Business 升级额度；跨工作流全历史用 Event History（按状态/时间过滤）。
- 判据：**事件处理系统要有"业务事件 ID 与执行 ID 分离"的关联键**——重试/挂起后还能按原始事件聚合；队列保留要有上限策略（超限删最旧是默认）。
- **提升层**：工具 / 工作流。

### F2：意图访谈 95% 置信度阈值 + 输出塑形 + Karpathy 可验证成功标准（来源：skillsmp #1011/#1010/#1021/#1034）
- **interview-me（addyosmani/agent-skills 98,168★）**：ask 未明确定义（"build me X" 缺 for whom/why now）或用户显式召唤（interview me/grill me/are we sure?/stress-test）时，**一次一问直到 ~95% 意图置信度**——**在模型静默填补歧义需求之前触发**——给"先问再做"一个明确停止阈值（不是问几轮，是问到 95% 置信）。
- **i-have-adhd（49,311★）输出塑形**：为 ADHD 读者塑形输出——**lead with next action / 多步工作编号 / 跨轮重申状态 / 抑制离题 / 给具体时间估计 / 让进展可见**；/i-have-adhd 开启持续到 stop——"读者认知特性是输出格式的输入"。
- **unslop（cursor/plugins）**：`Cut AI tells from any writing. Must always apply.`——去 AI 味作为**强制默认**技能（不等待用户要求）。
- **andrej-karpathy-skills**：think before coding / keep changes simple / edit surgically / **define verifiable success criteria before implementation**（实现前定义可验证成功标准——与 wb-spec-driven 同主题的外部表达）。
- **pptx-html-fidelity-audit（open-design）**：审计 python-pptx 导出 vs 源 HTML deck 的布局/内容漂移（footer overflow/cropped content/missing italic/lost styling/off-rhythm spacing）并重导出——**HTML→PPTX 往返保真是可审计可修复的**。
- 判据：**先问后做的停止条件是"置信度阈值"不是"问了几轮"**；输出格式按读者认知塑形；成功标准在实现前定义；往返转换（HTML↔PPTX）要有保真审计。
- **提升层**：可复用 Skill / 工作流。

### F3：DSH 插件生态：12,507 插件 14 分类 + 四层记忆 + spec-driven 工作流循环（来源：deepseek-plugin.org/plugins 大目录）
- **目录规模与分类**：12,507 插件、14 分类——Official 226 / UI Enhancements 2,691 / Developer Tools 1,648 / Integrations 4,308 / Themes & Skins 519 / Models & Routing 867 / Task & Automation 1,527 / Knowledge & Search 1,263 / Vision & Multimodal 225 / **Memory 398** / Security & Governance 174 / Creative 108 / Fun 557——**记忆类插件 398 个是独立大类**（记忆 = 一级需求）。
- **安装分发双通道**：`dsh plugin --profile web add <name>`（npm 风格）+ `github:owner/repo#path:...`（github 路径）+ `@scope/name`（scoped）。
- **Top 插件代表**：MemOS（本地四层长期记忆 L1 trajectory/L2 strategy/L3 world model/skills，每轮自动检索 + 注册 6 个记忆工具，10.8k）/ hindsight（长期项目记忆：自动召回知识页与上下文、会话自动保存、每仓库共享记忆库，20.4k）/ dsh-weknora（腾讯：原始文档 → 可查询 RAG + 自主推理 agent + 自维护 Wiki，21.0k）/ **ouroboros（Q00：spec-driven AI 工作流 MCP——Interview→Seed→Execute→Evaluate→Evolution 循环，uvx 运行零安装）** / dsh-routing-suite（任务感知推理模式路由，injector + P1-P23 预设）/ dsh-market（800+ 社区插件市场：浏览/一键安装/主题切换/备份恢复/批量分组/诊断）。
- 判据：**插件生态的成熟标志是"分类目录 + 双分发通道 + 市场管理工具"**；记忆按层级实现（轨迹/策略/世界模型/技能）；spec 驱动循环（访谈→播种→执行→评估→进化）可整体打包为 MCP。
- **提升层**：生态观察 / 工具。

### F4：并行 agent 舰队 + 双 agent 单规则书 + 免费多模型网关（来源：trendshift weekly 系）
- **stablyai/orca（ADE，Agent Development Environment）**：**面向并行 agent 舰队的开发环境**——用自己的订阅跑任何 coding agent，desktop/mobile/remote runtime 三端——"同时跑多个 agent 的统一工作环境"是新基建品类。
- **mikerCZ/one-rulebook**：**一条规则书服务所有 agent**——Claude Code + Codex CLI 同一机器，hooks 强制规则，finder-not-fixer review lanes，一个指令文件管两个 agent——"多 agent 单规则源，hooks 强制执行，审查车道只找不修"。
- **diegosouzapw/OmniRoute**：**免费 MIT AI gateway——1 endpoint / 359 providers（150+ 免费）/ 1200+ 模型**——兼容 Claude Code/Codex/Cursor/OpenCode/Cline/Copilot 的通用网关（与我们的免费多模型路由需求同主题）。
- 另有：langflow-ai/openrag（Langflow+Docling+Opensearch 单包 RAG 平台）、rohitg00/agentmemory（#1 持久记忆，基于真实基准）、phuryn/pm-skills（PM 技能市场 100+）、《深入理解 AI Agent》开源书（bojieli/ai-agent-book）。
- 判据：**多 agent 并行的价值前提是"统一环境 + 单规则源 + 网关"三层**；记忆与网关类基础设施按真实基准（非 demo）排名。
- **提升层**：工具 / 生态观察。

## 判重说明
- F1 → r201-A D1 已记 triggers 页；workflows/events 页首次拉全，event/context 分离 + trace_id vs id 重试关联 + 队列保留上限为独有增量。
- F2 → grill-me/wb-doc-writing 已有"先问先对齐"；interview-me 的 95% 置信度阈值 + i-have-adhd 输出塑形 + unslop 强制默认 + Karpathy 可验证成功标准为独有增量。
- F3 → r198-B 已记 DSH 插件生态（初版）；plugins 目录 96,587 字本轮全量重拉，12,507 规模 + 14 分类 + 记忆独立大类 398 + MemOS 四层 + ouroboros spec-driven 循环 + dsh-market 为独有增量。
- F4 → r200-A 已记多 agent 编排纪律；orca ADE + one-rulebook 单规则源 + OmniRoute 网关 + openrag 为独有增量。
