# 学习轮 r210-C：Claude Code statusline与hooks官方页与HF Skills生态与skillsmp p36-37与DSH插件目录（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.anthropic.com/claude-code/statusline（4999/13743 取） | OK（可编程状态栏/JSON schema） |
| 2 | skillsmp.com/skills/page/36（#3501-3554） | OK（goal-plan/sepia/ds-vision-skill 等） |
| 3 | docs.n8n.io/advanced-ai/（全 1742B） | OK（导航页，与 r209 重叠记录） |
| 4 | docs.anthropic.com/claude-code/statusline 续读（4999-12991） | OK（完整 schema/缓存纪律/subagentStatusLine） |
| 5 | general_search Hugging Face agents skills | OK（HF Skills ★11,059/VisionCodeAgent 30% 降本） |
| 6 | docs.anthropic.com/claude-code/hooks（4994/34780 取） | OK（30 事件/五 handler 类型） |
| 7 | docs.anthropic.com/claude-code/hooks 续读（4994-11994） | OK（exit code 语义/JSON 输出/terminalSequence） |
| 8 | skillsmp.com/skills/page/37（#3601-3651） | OK（knowledge-agent/codehealth-mcp 等） |
| 9 | dify.ai/blog 列表（4603/176413 取） | OK（$30M 融资/Agent chat-to-skill 低方法） |
| 10 | deepseek-plugin.org/plugins（4458/96587 取） | **DSH 插件目录**（12,507 总量/记忆生态） |

## 独点（5 个）
### C1：Anthropic statusLine 官方页全量：可编程状态栏 + 上下文窗口 JSON schema（来源：docs.anthropic.com/claude-code/statusline 12991/13743B，2026-09-25 实拉；与 wb-max-token-saver 同域——实时成本/上下文监控的官方机制）
- **statusLine 是底栏任意 shell 脚本**：stdin 收 JSON 会话数据，stdout 显示；`/statusline` 自然语言生成脚本；本地运行不消耗 API token。
- **完整 JSON schema**：model/cwd/workspace（current_dir/project_dir/added_dirs/git_worktree）/cost（total_cost_usd/total_duration_ms/total_api_duration_ms/lines_added_removed）/context_window（total_input_tokens/total_output_tokens/size/used_percentage/remaining_percentage/current_usage{input/output/cache_creation/cache_read}）/exceeds_200k_tokens/effort/thinking/rate_limits（five_hour/seven_day used_percentage+resets_at）/vim/agent/worktree/transcript_path/version/output_style/session_id。
- **v2.1.132 起 total_input/output 是当前用量不是累计**；**used_percentage 只按 input 算**（input+cache_creation+cache_read，不含 output）；current_usage 在 /compact 后为 null 直到下个 API 响应。
- **rate_limits 仅 Claude.ai 订阅者出现**（Pro/Max），每窗口可独立缺失——用 `// empty` 处理缺失。
- **更新时机**：每条 assistant 消息后/compact 完成/权限模式变更/vim 切换；300ms debounce；运行中取消 in-flight；**refreshInterval 定时重跑**（时钟/后台 subagent 改 git 时 idle 期保持最新）。
- **缓存昂贵操作纪律**：git status/diff 每 5 秒缓存——**缓存文件名用 session_id 而非 PID**（PID 每次调用都变，session_id 会话内稳定跨会话唯一，避免并发会话互读脏缓存）。
- **subagentStatusLine**：agent 面板每行自定义——stdin 收全部可见 subagent 行 JSON（tasks 数组 id/name/type/status/description/label/startTime/tokenCount/tokenSamples/cwd）→stdout 每行 `{"id","content"}`；空 content 隐藏该行、省略 id 保留默认。
- **Windows**：Git Bash 或 PowerShell（`powershell -NoProfile -File`）；多行/ANSI 颜色/OSC 8 可点击链接（iTerm2/Kitty/WezTerm）。
- **陷阱**：stdout 只留状态行（stderr 不进显示）；长输出截断；disableAllHooks=true 会连带禁用 statusLine。
- **提升层**：工具 / 工作流（上下文预算与成本实时可视化的官方数据源）。

### C2：Anthropic Hooks 参考页全量：30 事件 + 五 handler 类型 + exit code 语义表（来源：docs.anthropic.com/claude-code/hooks 11994/34780B，2026-09-25 实拉；与 r210-B B1 分工——B1 管"hook 与权限规则的关系"，本条管 hooks 体系全量参考）
- **30 个 hook 事件三节奏**：会话级（SessionStart/SessionEnd）、轮级（UserPromptSubmit/UserPromptExpansion/Stop/StopFailure/PostToolBatch/InstructionsLoaded/ConfigChange/CwdChanged）、工具调用级（PreToolUse/PostToolUse/PostToolUseFailure/PermissionRequest/PermissionDenied/Notification/SubagentStart/SubagentStop/TaskCreated/TaskCompleted/TeammateIdle/FileChanged/WorktreeCreate/WorktreeRemove/PreCompact/PostCompact/Elicitation/ElicitationResult/Setup）。
- **五 handler 类型**：command（shell 命令）/http（POST 事件 JSON）/mcp_tool（调已连接 MCP server 工具，文本输出当 stdout）/prompt（单轮模型 yes/no 决策）/agent（实验性：可读 Grep/Glob 验证再决策）。
- **matcher 语法三态**：`*`/空=全匹配；纯字母数字下划线| = 精确串或 | 列表；含其他字符=JS 正则——`mcp__memory` 是精确串匹配不到任何工具，必须 `mcp__memory__.*`；`mcp__.*__write.*` 匹配任意 server 的 write* 工具。
- **if 字段**：permission rule 语法，只评估工具事件；**前导 VAR=value 赋值剥除后匹配**（`if: Bash(git push *)` 匹配 `FOO=bar git push`）；Bash 太复杂无法解析时总是运行。
- **exec form vs shell form**：args 存在=exec（无 shell、无 tokenization、路径占位符原样替换）；**Windows .cmd/.bat shim 不是可执行文件**——npm/npx/eslint 的 .bin shim 需 shell 形式或 `node + script path` 模式（跨平台可用的正确写法）。
- **exit code 2 阻断语义表**：PreToolUse 阻断调用/PermissionRequest 拒权限/UserPromptSubmit 拒提示/Stop 阻止停止/SubagentStop 阻止结束/ConfigChange 阻断配置变更/PreCompact 阻断压缩/PostToolBatch 停 agentic loop/**PermissionDenied 忽略 exit code 用 JSON retry:true 告诉模型可重试**/PostToolUse/PostToolUseFailure 不阻断（已发生）→stderr 给 Claude。
- **exit 1 ≠ blocking**：约定 Unix 失败码 1 非阻断（继续执行），只有 2 阻断——**强制策略 hook 必须 exit 2**；WorktreeCreate 任何非零都失败。
- **JSON 输出控制**：continue:false（停止整个处理）/stopReason/systemMessage/suppressOutput/**terminalSequence**（OSC 0/1/2/9/99/777+BEL allowlist，hook 无控制终端不能写 /dev/tty，由 Claude Code 代发通知/标题/铃声）；stdout 必须只含 JSON；输出 10k 字符上限（超限存文件+预览）。
- **async/asyncRewake**：后台运行不阻塞；exit 2 唤醒 Claude 显示系统提醒（stderr 或 stdout）。
- **hooks 位置**：user/project/local settings/managed/plugin hooks.json/**skill 或 agent frontmatter（组件活动时生效，once 只对 skill hooks 有效）**；subagent 的 Stop hook 自动转 SubagentStop。
- **disableAllHooks 层级**：managed 层的 disableAllHooks 才能禁用 managed hooks；user/project 层不能禁用 managed hooks。
- **HTTP hooks**：非 2xx 非阻断；阻断须 2xx + JSON decision block/permissionDecision deny。
- **提升层**：工具 / 可复用 Skill（生命周期自动化的完整事件面）。

### C3：Hugging Face Skills 生态：标准化框架 + VisionCodeAgent 30% 步骤降低（来源：general_search huggingface/skills ★11,059，2026-09-25 实拉）
- **huggingface/skills（★11,059，2025-11 创建，2026-09-17 更新）**：为 coding agents（Codex/Anthropic/多工具互操作）提供 HF 生态标准化 machine-readable skills——模型管理/Gradio UI 部署/评测分数提取/训练任务启动。
- **范式转移**：从脆弱的 raw code generation → **结构化 tool execution（declarative, agent-native）**——agents 原生执行复杂 ML 工作流（数据集整理/模型训练/性能评估）。
- **VisionCodeAgent**：**直接 Python 执行代替 JSON tool-calling——30% LLM steps 和运营成本降低**；原生 VLM 支持处理视觉输入。
- **Arize Phoenix 集成**：自治工作流"黑盒"问题——观测集成（追踪/traces）。
- **技能市场总量（2026-07 实拉）**：公开注册表（skills.sh/Claude Skills Registry/HF Skills Hub/awesome-agent-skills+40 小注册表）**合计 180,000+ 技能**——技能分发已成独立软件表面。
- 判据：**"skill 化"的边界 = 有明确工具面（可声明、可验证）而非自由文本**；HF 生态的标准化工具体系是 agent 消费 ML 能力的入口。
- **提升层**：工具 / 可复用 Skill（生态级标准化模式）。

### C4：skillsmp p36-37 精选：GOAP 目标规划 / sepia 四操作去 AI / claude-mem 知识库 / CodeScene 门禁（来源：skillsmp.com/skills/page/36-37，2026-09-25 实拉）
- **goal-plan（ruvnet/ruflo ★73,010）**：Goal-Oriented Action Plans（GOAP）——precondition 分析 + 成本优化 + 自适应重规划；与 define-goal（openai/skills ★27,529 动手前定义可测量目标）配成"目标定义→行动规划"链。
- **sepia（Nanako0129/sepia ★2,716）**：去 AI 味四操作——write/review（只诊断不编辑）/refactor（最小就地编辑）/recreate（重写）；专业文本按域规则路由（release notes/公告/PR 回复/代码评审评论/事故复盘/工单/技术文章/博客/长文新闻）。
- **knowledge-agent（thedotmack/claude-mem ★94,424）**：**从 claude-mem 观察记录构建可查询 AI 知识库**——"brains" from observation history，问过去工作模式/编译专项知识。
- **codehealth-mcp（affaan-m/ECC ★264,820）**：CodeScene MCP 实时结构性代码健康——**评审前检查/修改后验证 score delta/提交 PR 门禁**（与"结果断言层"互补：断言管业务合理性，CodeHealth 管结构退化）。
- **ds-vision-skill（★165）**：为纯文本推理模型补视觉——vision-router.ps1 自动路由（图片理解先免费池 GLM/Agnes→custom/local；文档解析 MinerU；纯文字 Baidu OCR/Windows OCR）→标准 JSON 交主模型。
- **feishu-connect（★3）**：飞书 MCP 连接管理（授权流程/token 刷新/会话启动自动检测）。
- **investment-research（xbtlin/ai-berkshire ★16,479）**：巴菲特-芒格-段永平-李录四大师综合分析框架。
- **token-efficiency（★20）**：模型选择纪律（Opus 学习/Sonnet 开发调试）+ bash 优于读文件（印证 max-token-saver 方向）。
- 判据：**"目标→规划→执行→评估"链在技能层可复用**；记忆型技能的价值在"观察记录→可查询知识库"的沉淀形态。
- **提升层**：可复用 Skill / 工作流。

### C5：DSH 插件目录与记忆生态：12,507 插件总量 / MemOS 四层记忆 / ouroboros spec-driven 循环（来源：deepseek-plugin.org/plugins 4458/96587B，2026-09-25 首拉）
- **DSH（DeepSeek Harness）插件目录**：12,507 插件总量——分类：Official 226/UI 2,691/Dev Tools 1,648/Integrations 4,308/Themes 519/Models & Routing 867/Task & Automation 1,527/Knowledge & Search 1,263/Vision 225/Memory 398/Security 174/Creative 108/Fun 557；安装语法 `dsh plugin --profile web add ...`。
- **MemOS memos-local-plugin（MemTensor ★10.8k）**：**本地四层长期记忆（L1 trajectory/L2 strategy/L3 world model/skills）**，每用户轮自动检索，注册六个记忆工具——记忆分层+自动检索形态（与 wb-context-compressor 同域增量）。
- **hindsight（vectorize-io ★20.4k）**：长期项目记忆——每会话自动召回知识页+上下文、对话自动保存、**按仓库共享记忆库**。
- **memsearch-dsh（zilliztech ★2.5k）**：共享 Markdown 记忆——自动捕获/**pre-step 上下文注入**/可搜索召回/审查面板。
- **ouroboros（Q00 ★5.6k）**：uvx 启动 Python 引擎提供 spec-driven AI workflows 作为 MCP 工具——**Interview→Seed→Execute→Evaluate→Evolution 五阶段循环**，无安装无额外代码。
- **dsh-weknora（Tencent ★21.0k）**：raw documents→queryable RAG+自主推理 agent+自维护 Wiki。
- **BrowserSkill（Tencent ★1.2k）**：bsk 命令行封装成 DSH 原生 browser_* 工具——AI 驱动真实 Chromium。
- 判据：**记忆插件的共性形态 = 分层 + 每轮自动检索 + 共享库**；spec-driven 循环（Interview→Evaluate→Evolution）是"执行+自进化"的模板。
- **提升层**：工具 / 工作流。

## 判重说明
- C1 → statusline 官方页全量，与 wb-max-token-saver 同域但为官方机制（schema/缓存纪律/subagentStatusLine），增量 >60%，落。
- C2 → hooks 参考页全量，与 r210-B B1 分工明确（B1=hook 与权限关系，C2=30 事件/五 handler/exit code 语义表），落。
- C3 → HF Skills 生态（★11,059/30% 降本/180k 市场总量）全新，落。
- C4 → skillsmp p36-37 精选（GOAP/sepia/knowledge-agent/codehealth）全新，落。
- C5 → DSH 插件目录（12,507 总量/MemOS 四层记忆/ouroboros spec-driven）首拉，落。
- 未落：n8n advanced-ai 导航（r209 重叠）、dify.ai/blog 列表（融资新闻+Agent chat-to-skill 与 r209 相关重叠，仅记录）。
