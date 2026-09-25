# 学习轮 r222A：skillsmp p74精选与Dify 1.17版本面与OpenClaw调度与常设指令与Langflow NextPlaid（2026-09-25）

## 实拉记录（10 次调用，6 成功 / 4 失败计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/74（#7301-7345，5971/11961 取） | OK |
| 2 | Dify 版本检索（1.17.1/1.16.0/New Agent/1.14.1） | OK |
| 3 | Langflow 版本检索（1.12 blog/1.11 NextPlaid/1.9 Assistant） | OK |
| 4 | docs.n8n.io retrieve-relevant-context.md | dead（security 拦，已知死路重确认） |
| 5 | GitHub Trending 检索（Understand-Anything/voicebox/worldmonitor/orca） | OK |
| 6 | deeplearning.ai 检索（Evaluating AI Agents convergence/Spec-Driven） | OK |
| 7 | docs.openclaw.ai/automation/cron-jobs/schedules（3279 全） | OK |
| 8 | activepieces.com/docs/flows（1160 全） | OK |
| 9 | openagentskill.com 续读（4234-8394） | OK（创作者 showcase 面，增量低） |
| 10 | docs.openclaw.ai/automation/standing-orders（2343 全） | OK |

## 独点（4 个）
### A1：skillsmp p74 精选：媒体统一 resolve 层 / 部落知识提取生成数据分析 skill / docx 智能表格填充（来源：skillsmp.com/skills/page/74，2026-09-25 实拉）
- **media-use（heygen-com/hyperframes ★52,018）**：**Agent Media OS——单一 skill 覆盖项目全部媒体需求：BGM/SFX/图/icon/品牌logo/voice/调色/LUT 统一 resolve 为冻结本地文件或可粘贴块+台账记录（一个动词 resolve）；目录缺失时经 TTS/音乐/图像模型生成；语音/转写/字幕/去背景共享一个音频引擎；资产跨项目复用**（媒体需求的统一抽象+台账纪律）。
- **data-context-extractor（anthropics/knowledge-work-plugins ★25,304）**：**从分析师处提取部落知识（tribal knowledge）生成公司专属数据分析 skill——BOOTSTRAP 模式（发现 schemas/问关键问题/生成带参考文件的初始 skill）+ITERATION 模式（加载现有 skill/问定向问题/追加更新参考文件）**（企业专属数据分析 skill 的双模式生成）。
- **fill-docx-template（LeoYeAI ★2,128）**：**docx 模板填充语法——普通占位符 {name} + 智能表格填充 {name|r:x,c:y}（从标记行向下填充、保留上方内容）+插入图片+批量生成**。
- **claude-superpowers（mohitagw ★1,320）**：4 阶段编码纪律框架——plan before coding → isolate on branch → write tests first → self-review twice（双审清单）。
- **critique（nexu-io/open-design ★97,471）**：5 维度设计评审（Philosophy/Visual hierarchy/Detail/Functionality/Innovation 各 0-10）→ 单 HTML 报告（雷达图+证据评分+Keep/Fix/Quick-wins）。
- **提升层**：可复用 Skill / 工作流。

### A2：Dify 1.17.1 / New Agent / Workflows 团队资产（来源：dify.ai 检索+社区版本摘要，2026-09-25 实拉）
- **Dify 1.17.1（2026-09-10）**：**知识库 API 密钥可限定到具体 dataset（不只整个 workspace）；Chatflow Agent V2 修复对话间记忆丢失+正常处理推理模型未闭合 think 标签；Human Input 节点可放进循环/迭代节点内+超时分流**（记忆稳定与权限细化面）。
- **Dify 1.16.0-rc1**：**技能以标准化方式打包分发；Agent builder（UI 建 Dify Agent，base prompt 可配）**。
- **Introducing New Agent（1.1x 系列）**：**通过对话构建 agent——Dify 自动生成可复用 skills 并在对话中保留上下文；ready 后作为 agent 节点加进 workflow**（chat-to-skill 的构建面）。
- **1.14.1 Workflows Become a Team Asset**：workflow 从"built"到"continuously used and reused"（团队资产化）。
- **提升层**：工具 / 工作流（编排平台版本面）。

### A3：OpenClaw 调度类型与常设指令：五调度 / stream 批处理 / condition watcher / standing orders（来源：docs.openclaw.ai/automation/cron-jobs/schedules + standing-orders，2026-09-25 实拉）
- **五种调度类型**：`at`（一次性）/`every`（固定间隔）/`cron`（5/6 字段+--tz）/`on-exit`（被看管命令退出时触发，存活过 turn teardown）/`stream`（operator-authored argv 命令常驻 Gateway，从 stdout/stderr 行触发——**事件驱动非时间到期**）。
- **stream 批处理语义**：mode line（默认全行）/match（regex 匹配才收）；batch 在 batchMs 安静后关闭（默认 250ms，clamp 50-5000）；maxBatchBytes 16KB（clamp 1024-65536，到顶批尾标 [truncated]）；每 job 只保留 1 次 payload fire+1 个 bounded pending batch（防无界队列）；**failed payload 不重试（可能不幂等）**；无原生 WebSocket 源（websocat 桥接）。
- **condition watcher（事件触发）**：headless 条件脚本必须返回 `{fire, message?, state?}`；**state 上限 16KB**；30s 最小间隔+30s wall-clock 预算+5 工具调用；`once:true` 首成功 fired 后禁用；**author watchers around actionable state，不只 success——检查失败/超时却安静=看似健康实则坏了**；fire 时 message 必须自包含（成为 fired run 的完整事件上下文）；**触发脚本与 script payload 默认以 agent 全工具策略（含 exec）无人值守运行=不受信代码执行面，硬停用 cron.triggers.enabled:false**。
- **standing orders（常设指令）四要素**：Scope（授权做什么）/Triggers（何时执行）/Approval gates（哪些需人签）/Escalation rules（何时停手求助）；放 AGENTS.md 自动注入；**standing orders 定义 what、automations 定义 when**。
- **Execute-Verify-Report 模式**：**每任务执行→验证→报告；"I'll do that"≠执行、"Done"没有验证不可接受、失败重试一次换方法、仍失败报诊断、最多 3 次尝试后升级、绝不静默失败**。
- **提升层**：工作流（调度/常设授权/执行纪律）。

### A4：Langflow NextPlaid multi-vector + deeplearning 评估增量（来源：langflow.org/blog + deeplearning.ai，2026-09-25 实拉）
- **Langflow 1.11.0 NextPlaid**：**lfx-nextplaid 扩展 bundle 提供 first-class multi-vector retrieval——ColBERT-style late interaction + ColPali 视觉文档检索开箱即用，无自定义胶水代码**（多向量检索面，r220B 落 1.11 未含此面）。
- **Evaluating AI Agents（Arize，2h36m）convergence score**：**评估 agent 能否在高效步数内响应查询——收敛分（步数效率）**；为 skills 与 router 决策建 code-based/LLM-as-judge 评估（从 traces 建测试示例+详细 LLM-judge prompt）；structured evaluations（r221-A 已落课程主面，convergence 为增量）。
- **Spec-Driven Development with Coding Agents（JetBrains，1h16m）**：**constitution 创建→feature validation→project replanning→MVP→legacy support→agent replaceability**（constitution 驱动的 agent 开发流程）。
- **提升层**：模型（评估）/ 工作流（多向量 RAG）。

## 判重说明
- A1 media-use/data-context-extractor/fill-docx-template 全新面，落。
- A2 Dify 1.17.1 dataset 限定密钥+Agent V2 修复为版本增量（r220 落 1.14 前），落。
- A3 stream/on-exit/watcher/standing orders 为 openclaw 自动化新面（r220 落 cron OR、r221 落 hooks，本面互补），落。
- A4 NextPlaid multi-vector 为 1.11 增量；convergence score 为 Evaluating AI Agents 增量（重叠>60% 含≥40% 增量合并保留），落。
- 未落：n8n retrieve（security 拦）、activepieces flows 基础（r221B 已落三构件）、openagentskill 创作者 showcase（低增量）。
