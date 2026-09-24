# 学习轮 r201-A：Pipedream触发器特殊参数与ClaudeCode钩子28事件与上下文预算审计技能与六信号评测（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/ | OK 全文（Dify 概览 + llms.txt） |
| 2 | docs.n8n.io/flow-logic/if-else/ | 死链 |
| 3 | docs.langflow.org/integrations/ | 死链 |
| 4 | make.com/en/help/webhooks/ | fetch error |
| 5 | pipedream.com/docs/cron/ | OK 全文 9855 字（Triggers 大页） |
| 6 | docs.anthropic.com/en/docs/claude-code/hooks | OK 全文 34780 字 |
| 7 | skills.sh/collections | 死链 |
| 8 | skillsmp.com/skills/page/9 | OK（#801-827） |
| 9 | deepseek-plugin.org/about | 死链 |
| 10 | GitHub 生态（openagentskill rankings 搜索） | OK |

## 独点（4 个）
### D1：Pipedream 触发器特殊参数 + 大 payload 上传机制 + 事件源/工作流分离（来源：docs.pipedream.com/docs/cron 全文）
- **x-pd-nostore / x-pd-notrigger 两个特殊请求参数**：`x-pd-nostore: 1` 执行全部步骤但不记录任何数据（inspector/Event History 不可见）；`x-pd-notrigger: 1` 发测试事件不触发生产版本工作流（在测试事件列表里可见）——**"跑但不留痕"与"测试不触发生产"是 webhook 调试的两个关键开关**。
- **大 payload 上传**：默认 body 512KB；加 `pipedream_upload_body=1` query 或 `x-pd-upload-body: 1` header 可发任意大小（上限 5TB）；raw body 存 S3 生成 signed URL **30 分钟有效后删除**（访问 `steps.trigger.event.body.raw_body_url`）；Send HTTP Request action 下载最多 6MB；multipart/form-data 自动解析为 JS 对象、header 自动小写。
- **event source 与 workflow 分离模型**：source 运行代码收集事件并 emit，**一个 source 可 trigger 任意多个 workflow**——"服务产生的数据（source）与处理逻辑（workflow）分离"；SSE/REST API 可平台外访问事件；一个 workflow 可加**任意数量 trigger**。
- **HTTP 授权两内建**：static custom token（Bearer）/ OAuth（Pipedream SDK 自动刷新 token + `invokeForExternalUser` 按外部用户 ID 调用）；自定义 auth 可在 workflow 开头做 JWT 校验；支持 custom domains（endpoint.yourdomain.com）。
- 判据：**webhook 型入口要设计"测跑不触发生产 + 跑完不留痕"双开关**；大文件走"临时签名 URL + 过期清理"而非直接进内存；事件采集与处理解耦才可多消费。
- **提升层**：工具 / 工作流。

### D2：Claude Code hooks 28 事件 + matcher/if 两级过滤 + 压缩前后钩子（来源：docs.anthropic.com/en/docs/claude-code/hooks 全文 34780 字）
- **28 个生命周期事件，三节奏**：每会话（SessionStart/SessionEnd）、每轮（UserPromptSubmit/Stop/StopFailure）、每工具调用（PreToolUse/PostToolUse）；另有 Setup（--init-only 一次性准备）、UserPromptExpansion（可阻断命令展开）、PermissionRequest、PermissionDenied（返回 `{retry:true}` 让模型重试被拒调用）、PostToolUseFailure、PostToolBatch（并行批次后）、Notification、SubagentStart/Stop、TaskCreated/Completed、TeammateIdle、InstructionsLoaded（CLAUDE.md/.claude/rules/*.md 加载进上下文时）、ConfigChange、CwdChanged（cd 时，direnv 式反应式环境管理）、**FileChanged（matcher 指定监听文件名）**、WorktreeCreate/Remove、**PreCompact/PostCompact（上下文压缩前后）**、Elicitation（MCP server 请求用户输入）、ElicitationResult、SessionEnd。
- **hook 三级结构**：hook event → matcher group（按工具名粗滤）→ hook handler（shell/HTTP/MCP/prompt/agent）；**if 条件二级细滤**（如 `if: "Bash(rm *)"`）——**不匹配就不 spawn 进程，省开销**；handler 从 stdin 读 JSON，返回 `permissionDecision: deny` 可阻断工具调用。
- **hook 位置五档**：~/.claude/settings.json（用户）/ .claude/settings.json（项目 git）/ .claude/settings.local.json（本地 gitignored）/ managed policy（组织）/ **plugin hooks/hooks.json（插件启用时生效）**。
- 判据：**钩子不是"工具调用前后"两点，是覆盖会话全生命周期的 28 个可编程点**；过滤分层（event→matcher→if→脚本）每层都在省无谓执行；压缩前后有钩子 = 可在压缩动作上加审计。
- **提升层**：工具 / 可复用 Skill。

### D3：上下文预算审计技能 + 三层溯源标记移除 + 决策时刻自动 ADR（来源：skillsmp #823/#814/#811）
- **context-budget（ECC）**：**审计 Claude Code 上下文窗口在代理/技能/MCP 服务器/规则中的消耗**——识别膨胀、冗余组件，给优先 token 节省建议——"上下文预算审计"本身被技能化（与 wb-context-compressor 同主题的外部实现，且管"审计哪里在烧"）。
- **remove-ai-marks（guillaumemeyer/watermarks-remover, 22,454★）**：**三层溯源移除**——不可见 Unicode（Layer A）/ 统计文本水印（Layer B，重写，always offer）/ C2PA/EXIF/XMP/容器元数据（PNG/JPEG/WebP/SVG/PDF/DOCX/ODT/HTML/MD/TEX），覆盖 Claude/Gemini-SynthID/OpenAI provenance——**先 A 层后 B 层，B 层必须提供**。
- **architecture-decision-records（ECC）**：**自动检测决策时刻**、记录 context/alternatives/rationale、维护 ADR log——"会话中哪一刻算决策"由技能判定而非事后补写（与 wb-doc-writing ADR 准入三门槛互补：那条管"什么值得写"，这条管"自动捕获"）。
- 判据：**"省 token"前先审计钱花在哪**；溯源标记分三层处理、重写型方案始终提供；ADR 捕获可自动化但记录结构（context/alternatives/rationale）必须完整。
- **提升层**：可复用 Skill / 工作流。

### D4：openagentskill 六信号评测 + 按 agent 类型路由 + 相似度替代（来源：openagentskill.com rankings 系）
- **六信号 0-100 打分**：Popularity / Quality / Freshness / Agent evidence / **Evidence confidence（证据置信度）** / Install readiness——每个信号可解释榜单排序方法（ordering follows the list's method, not any one score）。
- **best-by-success-rate**：按 reported success rate + recent success + output quality + install success + Trust Score 排序（30 展示/471 候选；mono-color/Vox Director/Archify 100% success）；highest-quality 榜显示六信号明细（如 100/100 Quality、29/100 Freshness——**高分但低新鲜度也给出，不藏**）。
- **按 agent 类型路由**：/agents/cline、/best/browser-automation、/best/local-desktop 等按 agent 与场景细分榜单（1.4M stars 聚合、Trust 93 等）；/alternatives 给出相似度排序替代技能；TencentDB Agent Memory（4 层渐进管线本地长期记忆）VERIFIED EXCELLENT 100。
- 判据：**技能选择要"多信号可解释排序"而非单一星星数**；榜单按 agent/场景细分、替代技能带相似度；证据置信度与新鲜度作为独立信号公开（含低分不藏）。
- **提升层**：工作流。

## 判重说明
- D1 → r199-A A1（sources 消费模型）/r200-A A1（sources vs actions）已记；triggers 页首次拉全，x-pd-nostore/x-pd-notrigger + 大 payload 5TB S3 30min + 授权两内建为独有增量。
- D2 → r199-A A2（skill 调用控制矩阵）已记 hooks 相关；hooks reference 首次拉全，28 事件 + matcher/if 两级 + PreCompact/PostCompact + FileChanged + PermissionDenied retry 为独有增量。
- D3 → r200-C C1（settings 四级 scope）已记；context-budget/remove-ai-marks/ADR 自动捕获首次见，审计技能化 + 三层水印移除 + 自动 ADR 为独有增量。
- D4 → r200-A A5（openagentskill 指标体系）已记；本轮首次见六信号明细 + 证据置信度信号 + 按 agent 路由 + alternatives 相似度 + 低新鲜度不藏，为独有增量。
