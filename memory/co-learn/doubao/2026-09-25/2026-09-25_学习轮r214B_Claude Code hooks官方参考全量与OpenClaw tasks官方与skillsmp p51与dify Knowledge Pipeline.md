# 学习轮 r214-B：Claude Code hooks官方参考全量与OpenClaw tasks官方与skillsmp p51与dify Knowledge Pipeline（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/51（#5001-5056，5946/11720 取） | OK（agent-memory/project-artifact/seo-geo 等） |
| 2 | dify.ai/blog 续读（59974-65568） | OK（Knowledge Pipeline 生态/Introducing Knowledge Pipeline/TrueFoundry） |
| 3 | docs.anthropic.com claude-code/hooks（5992/34780 取前半） | OK（27 事件/matcher/5 种 handler） |
| 4 | docs.langflow.org/quickstart | 死链（link dead，计数） |
| 5 | docs.anthropic.com claude-code/hooks 续读（5992-11988） | OK（exec vs shell form/exit code 语义/JSON output） |
| 6 | github.com/trending | OK（paperclip ★83,229，r214-A 已落不重落） |
| 7 | deeplearning.ai/short-courses 续读（25832-30299） | OK（Claude Code 官方课程，其余重复） |
| 8 | docs.n8n.io 根页（1227B） | OK（llms.txt 索引+n8n MCP HTTP transport 三客户端连接） |
| 9 | docs.openclaw.ai/automation/tasks（5962/6951 取） | OK（任务=活动账本/生命周期/lost 语义/媒体幂等护栏） |
| 10 | modelscope.cn 首页（4833/9001 取） | 低方法（本周 trending 模型/数据集趋势，无方法增量） |

## 独点（4 个）
### B1：Claude Code hooks 官方参考全量：27 事件 / matcher 三语义 / exec vs shell form / exit code 三语义（来源：docs.anthropic.com claude-code/hooks，2026-09-25 实拉）
- **27 个 hook 事件按节奏分三类**：session（SessionStart/End）、turn（UserPromptSubmit/Stop/StopFailure）、tool 循环（PreToolUse/PostToolUse）；另含 PreCompact/PostCompact、InstructionsLoaded、ConfigChange、CwdChanged、FileChanged、WorktreeCreate/Remove、Elicitation/ElicitationResult（MCP 请求用户输入）、PermissionRequest/Denied、Notification、SubagentStart/Stop、TaskCreated/Completed、TeammateIdle、PostToolBatch、PostToolUseFailure。
- **matcher 三语义**：`*`/空=全部；纯字母数字下划线管道符=精确字符串或 `|` 列表（`Bash`/`Edit | Write`）；含其他字符=JS 正则（`mcp__memory__.*` 匹配 memory server 全部工具，**注意 `mcp__memory` 是精确串匹配不到，必须带 `.*`**）。
- **if 字段**：permission rule 语法（`Bash(git *)`/`Edit(*.ts)`），只对 tool 事件生效（其他事件设 if 永不运行）；Bash 逐子命令匹配且剥离前置 `VAR=value`；无 && || 组合语法，多条件拆多个 handler。
- **exec form vs shell form**：args 设置=exec form（无 shell、路径 placeholder 免引号、特殊字符原样）；args 省略=shell form（sh -c/Git Bash/PowerShell）；**Windows .cmd/.bat shim 不是可执行文件不能 exec，用 node+script-path 模式**（`"command":"node","args":["${CLAUDE_PLUGIN_ROOT}/scripts/x.js"]` 全平台可跑）。
- **exit code 三语义**：0=成功（解析 stdout JSON，仅 exit0 才处理 JSON）；**2=阻塞错误（stderr 回 Claude、忽略 stdout/JSON）**；其他=非阻塞错误；**exit 1 也是非阻塞——要 enforce 政策必须 exit 2**；WorktreeCreate 任何非零=abort。
- **exit2 逐事件表**：PreToolUse/PermissionRequest/UserPromptSubmit/UserPromptExpansion/Stop/SubagentStop/TeammateIdle/TaskCreated/TaskCompleted/ConfigChange/PostToolBatch/PreCompact/Elicitation/ElicitationResult/WorktreeCreate 可阻断；PostToolUse/PostToolUseFailure 等已发生事件不可阻断只显 stderr。
- **5 种 handler**：command/http/mcp_tool/prompt/agent；HTTP 非 2xx=非阻塞，block 需 2xx+JSON decision；MCP tool hooks 的 server 必须已连接（SessionStart/Setup 常先于连接好，首跑"not connected"正常）；prompt/agent hooks 用 $ARGUMENTS。
- **JSON output**：每 hook 只能选 exit-code 或 exit0+JSON 一种；stdout 只含 JSON（shell profile 打印会干扰解析）；output 字符串上限 10000 字符（超限存文件）；continue:false 完全停（stopReason 给用户）；suppressOutput/systemMessage/terminalSequence（OSC 0/1/2/9/99/777+BEL allowlist，v2.1.141+，hooks 无控制终端不能直接写 /dev/tty）。
- **disableAllHooks 层级**：settings 临时禁全部；**managed 层的 disableAllHooks 才能禁 managed hooks**（用户/项目/本地层禁不掉管理员配的）。
- **提升层**：可复用 Skill / 工作流（执行纪律钩子化）。

### B2：OpenClaw background tasks 官方：任务=活动账本、生命周期与 lost 语义、媒体生成幂等护栏（来源：docs.openclaw.ai/automation/tasks，2026-09-25 实拉；与 r213-C C2 schedules 同站互补增量）
- **任务记录不是调度器**：ACP runs/subagent spawns/所有 automation runs/CLI ops/session 媒体生成都建任务记录；heartbeat turns/普通交互聊天/直接 /command 响应**不建**。
- **生命周期与 lost 语义**：queued→running→terminal（succeeded/failed/timed_out/cancelled/lost）；**backing state 消失 >5 分钟 → lost**，且 lost 是运行时感知的（ACP 需 live in-process turn、subagent 需 child session、automation 需 runtime 仍拥有 job+durable 历史无终态、CLI 用 run id）；**terminal 后不再降级**（已 cancelled/failed 的任务后续 success 信号不改变状态）。
- **执行/交付分离细节**：subagent 任务可 succeeded 而 deliveryStatus session_queued/failed；终态 succeeded（交付后）vs blocked（活干完但结果交不回）；blocked 任务保留 canonical result 7 天，`tasks retry`（fenced 新交付代）+`tasks dismiss`（记录有意不交付）；handoff 重试 30 分钟指数退避。
- **通知策略**：done_only（默认）/state_changes/silent（automation/CLI/media 默认 silent）；direct delivery（requesterOrigin 通道）vs session-queued（**立即 heartbeat wake 不用等下个 tick**）。
- **媒体生成幂等护栏**：同一 prompt/request 重复调用返回匹配 active task status 而非启动重复；distinct prompt 可启动自己任务；blocked media 任务保留有界附件引用。
- **audit findings**：stale_queued>10min（warn）/stale_running>30min（error）/lost/delivery_failed/missing_cleanup/inconsistent_timestamps；TaskFlow findings 含 cancel_stuck（取消请求 >5min 仍非终态）/blocked_task_missing/stale_waiting。
- **存储与保留**：SQLite ~/.openclaw/state/openclaw.sqlite（task_runs/task_delivery_state/flow_runs）；sweeper 60s；terminal 记录 7 天（lost 24h）自动清理；v2026.6.1 起共享库替换 sidecar。
- **提升层**：工作流 / 工具（后台任务运维账本）。

### B3：skillsmp p51 精选：四级记忆晋升 / 增量刷新状态页 / GEO / 混合路由器暴露路由决策（来源：skillsmp.com/skills/page/51，2026-09-25 实拉）
- **agent-memory（alirezarezvani/claude-skills ★26,225）**：四级存储 L0 transcripts/L1 candidates/L2 project context/L3 stable persona——**提升靠跨会话跨天重复出现赢得，绝不靠单次自信陈述；没有人类采纳，什么都不进已提交文件**——记忆晋升判据（与 r213-B auto memory 互补：那条管结构，这条管晋升门槛）。
- **project-artifact（anthropics/claude-plugins-official ★36,597）**：项目状态页做成 tabbed artifact 发布到默认私有 claude.ai 页——**每 artifact 有 per-project 小 config，刷新重新采集 live state、重部署同 URL、只报 delta**——增量刷新状态页，适合跨 workstream 大项目。
- **seo-geo（AgriciDaniel/claude-seo ★17,388）**：GEO（Generative Engine Optimization）——针对 AI Overviews/ChatGPT search/Perplexity 优化：品牌提及信号、AI 爬虫可达性、llms.txt 合规、passage-level 可引用性评分、平台特定优化。
- **research 混合路由器（alirezarezvani/claude-skills ★26,225）**：research 默认入口——确定性分类→委托 specialist（pulse/litreview/patent/dossier 等）或 fallback（plan-decompose-multi-source-search-synthesize-cite）；**总是暴露路由决策供用户覆盖**。
- **ponytail-debt（zzz2929）**：马尾债务分类账——代码库中注释放入债务分类账，故意捷径和延期被追踪而不是腐烂成"以后意味着永远不会"；一枪报告什么也没改变。
- **plan-canvas（affaan-m/ECC ★264,820）**：计划/HTML 工件在本地浏览器 canvas 打开，人可直接标注、聊天、批准或要求修改——可视化批注评审界面。
- **console-dev（zts212653/clowder-ai ★3,091）**：前端交付四道门禁 Product/Design-System/Implementation/Verification gate。
- **rhwp-bulk-pipeline（edwardkim/rhwp ★3,818）**：批量管道流协议——stdin 一行一路径→stdout 纯 NDJSON、stderr 人用摘要、失败行信封隔离+jq 重试、输入 N=成功+失败 gate。
- **提升层**：可复用 Skill / 工作流。

### B4：dify Knowledge Pipeline 可观测性+插件生态 + n8n MCP HTTP transport（来源：dify.ai/blog + docs.n8n.io，2026-09-25 实拉；与 r213-B B3/RAG 层合并保留增量）
- **Knowledge Pipeline 定位**：可适配、可扩展、**可观测**的 RAG 数据处理管道——企业非结构化数据转成 LLM 可用高质量上下文；**开放插件架构服务 120+ 国家含 Fortune 500**，邀请数据连接/文档处理/向量优化专家共建（数据连接+文档处理+向量优化三类插件方）。
- **TrueFoundry AI Gateway 集成**：实时成本可见性、安全合规控制、250+ LLM 接入，保持 Dify 拖拽简易——企业 LLM 网关接入模式。
- **n8n MCP server HTTP transport 连接命令**：Claude Code `claude mcp add --transport http n8n-mcp`；Codex CLI `codex mcp add n8n-mcp --url ...`；Claude Desktop 走 MCP 客户端配置——**MCP 端点化后三种客户端一行接入**。
- **llms.txt 文档索引**：n8n docs 提供 llms.txt 全索引+`.md` 后缀 Markdown 版本——站点文档可喂 agent 的索引协议。
- **提升层**：工作流（RAG 管道/网关/客户端接入）。

## 判重说明
- B1 → Claude Code hooks 官方参考全量，新页，落。
- B2 → OpenClaw tasks 官方，与 r213-C C2 同站互补（schedules 管"排期"，本页管"任务账本"），增量大，落。
- B3 → skillsmp p51 精选（四级记忆/增量状态页/GEO/路由暴露），全新，落。
- B4 → dify Knowledge Pipeline+n8n MCP 接入，RAG 层增量合并，落。
- 未落：github trending paperclip（r214-A 已落同日重复）、ModelScope（趋势信息无方法增量）、deeplearning.ai 重复课程、langflow quickstart（死链计数）。
