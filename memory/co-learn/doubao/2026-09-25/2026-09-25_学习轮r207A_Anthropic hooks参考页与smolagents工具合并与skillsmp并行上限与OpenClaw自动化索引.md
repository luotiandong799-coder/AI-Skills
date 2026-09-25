# 学习轮 r207-A：Anthropic hooks参考页exit语义与terminalSequence与smolagents工具合并与skillsmp并行上限与OpenClaw自动化索引（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.anthropic.com hooks 页（10000-13997/34780） | OK（exit 1≠阻塞/terminalSequence/additionalContext/HTTP hooks） |
| 2 | skillsmp.com/skills/page/26（#2501-2537） | OK（sumeru 子agent上限/cumcm 审核门控/git-guardrails） |
| 3 | docs.pipedream.com/workflows/events/ | 死链 |
| 4 | general_search Hugging Face smolagents | OK（工具合并/final_answer_checks/沙箱分档） |
| 5 | dify.ai/blog/multi-agent-orchestration | 死链 |
| 6 | blog.n8n.io ai-agent-memory（3866/5683） | OK（Chat Memory Manager/单 memory 子节点约束，CoALA 已落增量层） |
| 7 | deepseek-plugin.org/plugins?limit=10 | fetch error（死链，累计第 5 次） |
| 8 | docs.openclaw.ai/automation/cron-jobs（1076 全） | OK（/loop 快捷/condition watchers/hooks 端点索引） |
| 9 | activepieces.com/docs/build-chatbot/chat-bot-using-pieces | 死链 |
| 10 | waytoagi.com/ 续读（3149-6260） | OK（低价值工具卡片，不落） |

## 独点（5 个）
### X1：Anthropic hooks 参考页：exit code 语义陷阱与 terminalSequence 与 additionalContext 纪律（来源：docs.anthropic.com hooks 10000+ 段 2026-09-25，r205-A R4 hooks 三层安全的参考页增量）
- **exit 1≠阻塞**：Claude Code 只把 exit 2 当 blocking error；**exit 1 是非阻塞错误，执行继续**（1 是 Unix 惯例失败码但这里不拦）——强制策略必须用 exit 2；JSON 输出只在 exit 0 时处理。
- **exit 2 per-event 全表**：可阻塞=PreToolUse（block 工具调用）/PermissionRequest（deny）/UserPromptSubmit（**erase 提示**）/Stop/SubagentStop/TeammateIdle/TaskCreated（回滚）/TaskCompleted/ConfigChange/**PreCompact（阻止压缩）**/WorktreeCreate（**任何非零即失败**）；不可阻塞=PostToolUse/PostToolUseFailure/SessionStart/FileChanged 等（仅 stderr 展示给 Claude）。
- **terminalSequence 白名单**：hooks 无控制终端，写 /dev/tty 失败——用 terminalSequence 字段代发；仅允许 OSC 0/1/2/9/99/777+BEL；**光标/颜色/剪贴板（OSC 52）/超链接（OSC 8）一律拒绝**（hook 不能破坏屏上提示）。
- **additionalContext 纪律**：返回字符串被 system reminder 包裹注入上下文；**用事实陈述而非命令式**（"The deployment target is production" 而非祈使句——命令式会触发 prompt-injection 防御导致 surface 而非当上下文）；resume 回放保存文本不重跑 hook（**时间戳/commit SHA 会 stale**），SessionStart 在 resume 时重跑（source=resume）可刷新；>10000 字符写文件给路径；静态指令用 CLAUDE.md（不跑脚本）。
- **HTTP hooks 阻塞**：不能单靠状态码表达阻塞，必须 2xx+JSON body 带 decision 字段。
- 判据：**策略 hook 只用 exit 2**；hook 注入走事实陈述；无终端时用 terminalSequence 白名单。
- **提升层**：工具 / 工作流。

### X2：HF smolagents：工具合并减少 LLM 调用 + final_answer_checks + 沙箱分档（来源：HF docs smolagents 2026-09-25 搜索）
- **工具合并原则**：能合并两个 API 为一个工具就合并（返回连接输出）——"尽可能减少 LLM 调用次数"降低延迟/成本/错误风险。
- **工具文档必须 pristine**：agent 完全依赖函数签名理解工具——type hints+docstring 质量=工具可用性。
- **配置表**：简单单任务=无高级特性；复杂多步=planning_interval=3+max_steps=30；委托专家=ManagedAgent（agent/name/description）；**质量保证=final_answer_checks=[validator_func]**（最终答案前校验函数）；分步回调=step_callbacks；事后检查=return_full_result。
- **沙箱分档**：E2B（Firebase 微VM，最简，生产真实选择）/Modal（规模更便宜）/Docker（自托管）/Pyodide+Deno WASM（边缘/无 Docker socket 环境）。
- **护栏工具**：guardrail tool 必须在 final answer 前调用（validate_output）；imports 显式授权。
- 判据：**先减调用再优化单次**；回答前必有校验函数；生产环境选托管沙箱。
- **提升层**：工作流 / 可复用 Skill。

### X3：skillsmp p26：并行子 agent 上限与审核门控工作流与 git 安全 hooks（来源：skillsmp.com/skills/page/26 2026-09-25，与 r206-B V4 完成纪律互补）
- **sumeru-worldbuilder**：网文全流程创作，**所有章节级操作子 Agent 并行处理，每个 Agent 最多负责 3 个章节**——给并行子代理设每代理工作上限，防单点过载与上下文爆炸。
- **cumcm-step-review（数学建模分步审核）**：每部分先给分析与候选方案→用户审核通过→写代码→写入 Word 论文草稿**再次供用户审核**→全部定稿后按规范生成 AI 使用声明——**两段式审核门控**（方案级+成稿级）。
- **git-guardrails-claude-code**（mattpocock/skills ★267k）：hooks 阻止危险 git 命令（push/reset --hard/clean/branch -D）执行前拦截——与 hooks 参考页 exit 2 语义直接配套的现成技能。
- 判据：**并行子代理必须有每代理上限**；交付分"方案审核+成稿审核"两道门；危险操作走 hook 硬拦。
- **提升层**：工作流 / 可复用 Skill。

### X4：OpenClaw automation 索引页：/loop 快捷与 condition watchers 与 mapped hooks（来源：docs.openclaw.ai/automation/cron-jobs 2026-09-25，r205-B S3 六机制的索引页增量）
- **Automations 内置调度器**：持久化 jobs、唤醒 agent、交付到 chat channel/webhook/nowhere；`openclaw automations create` one-shot（--wake now --delete-after-run）；`openclaw cron` 是 alias。
- **/loop chat shortcut**：聊天内循环（chat 里发 /loop 即可循环执行）。
- **event triggers（condition watchers）**：事件条件触发的自动化（非时间调度）。
- **inbound webhooks 三端点**：POST /hooks/wake、POST /hooks/agent、**mapped hooks POST /hooks/<name>**（命名映射端点）。
- **Gmail PubSub triggers**：restricted Gmail reader 模式（受限读取模型，验证 reader boundary）。
- **Unattended run contract** + Dynamic cadence（pacing 动态节奏）。
- 判据：**调度之外还有事件触发与聊天快捷入口**；外部调用走 mapped hooks。
- **提升层**：工具 / 工作流。

### X5：n8n 单 memory 子节点约束与 Chat Memory Manager（来源：blog.n8n.io ai-agent-memory 2026-09-25，r205-B S1 CoALA 的实现层增量）
- **每个 AI Agent 节点只接受一个 memory sub-node**——组合记忆类型=memory sub-node 存对话历史 + vector store 连接为 agent tools。
- **Chat Memory Manager**：检查 memory size、清特定条目等高级记忆管理。
- **native memory layer 在画布上可检查可改**：不写自定义基础设施代码。
- 判据：**对话记忆与语义检索分层接线**；记忆管理节点显式可见。
- **提升层**：工具。

## 判重说明
- X1 → r205-A R4（hooks 三层安全）参考页增量（exit 1 陷阱/terminalSequence/additionalContext/HTTP hooks/PreCompact），落。
- X2 → 新（smolagents 首次详拉）；与 r205-A R1 编排互补（管理式 agent/校验式配置），落。
- X3 → r206-B V4 互补（另一页生态）；并行上限/双段审核/危险 git hooks 新，落。
- X4 → r205-B S3（六机制）索引页增量（/loop/condition watchers/mapped hooks/Gmail reader），落。
- X5 → r205-B S1（CoALA 四型三存储）实现层增量（单节点约束/Manager），落。
- 未落：waytoagi 续读（工具卡片低价值）、n8n ai-agent-memory 概念层（与 r205-B 全重复）、pipedream/activepieces/dify 死链。
