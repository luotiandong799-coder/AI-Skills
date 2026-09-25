# 学习轮 r208-B：Anthropic hooks终段prompt与async与n8n队列隔离与dify插件治理与智谱AgentMore（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.anthropic.com hooks 页终段（29977-34780 全取完） | OK（prompt/agent hooks/async/Elicitation/SessionEnd） |
| 2 | skills.sh 续读（8259-13380） | 低内容（图片为主） |
| 3 | agentskills.io 续读（3749-11040） | OK（Client Showcase 生态名单，低方法增量） |
| 4 | docs.pipedream.com/components/api 续读 | 死链 |
| 5 | skills.sh/docs | OK（npx skills add/匿名排行/badge/安全审计） |
| 6 | blog.n8n.io ai-agent-memory 续读（3866-5683 全取完） | OK（queue 隔离/编程式记忆/Zep 实体记忆） |
| 7 | dify.ai/blog 列表续读（3498-8951） | OK（插件治理/Asqav 行为收据） |
| 8 | waytoagi.com 首页 | OK（工具导航，低价值） |
| 9 | docs.openclaw.ai/capabilities | 死链 |
| 10 | general_search 智谱 AgentMore | OK（多 Agent 协作/7.4 万技能零 Token） |

## 独点（4 个）
### B1：Anthropic hooks 终段：prompt/agent-based hooks 与 async hooks 与 Elicitation 程序化应答（来源：docs.anthropic.com hooks 29977-34780 2026-09-25，r207 三段+r208-A 的收尾增量）
- **Prompt-based hooks（type: prompt）**：用 LLM（Haiku 默认）评估 allow/block——hook input JSON 经 `$ARGUMENTS` 注入 prompt，LLM 返回 `{ok: true/false, reason}`；ok:false 的 **per-event 行为表**：Stop/SubagentStop→reason 作为下一条指令回合继续；PreToolUse→deny+reason 作为工具错误；PostToolUse 默认回合结束 reason 作警告行（continueOnBlock:true 可继续）；**PostToolBatch/UserPromptSubmit/UserPromptExpansion 无论 continue 都结束回合**；PostToolUseFailure/TaskCreated/TaskCompleted→reason 作为工具错误；**PermissionRequest ok:false 无效**（要 deny 用 command hook）。
- **Agent-based hooks（type: agent，实验性）**：spawn 带工具的子代理（Read/Grep/Glob/跑测试）验证条件，最多 50 轮，返回 ok；默认超时 60 秒——**验证需要看真实文件/测试输出而非只评估输入数据时用 agent hook**；生产优先 command hooks。
- **Async hooks（async: true，仅 command）**：后台执行不阻塞 Claude；完成后 additionalContext 下一轮投递（systemMessage 给用户）；**asyncRewake exit 2 在会话空闲时立即唤醒 Claude**；每次执行独立进程**无去重**；默认超时与同步一致 10 分钟。
- **Elicitation/ElicitationResult**：MCP server 中途请求用户输入——hook 可程序化应答（action accept/decline/cancel+content），form-mode（requested_schema）/url-mode（浏览器认证 url）；ElicitationResult 可**覆盖用户响应**（改 action 或 content）；exit 2=拒绝并显示 stderr。
- **SessionEnd 超时控制**：reason 六值（clear/resume/logout/prompt_input_exit/bypass_permissions_disabled/other）；**默认超时仅 1.5 秒**，per-hook timeout 可设、总预算自动升到最高 per-hook（上限 60 秒，plugin 提供的 hook 不计入）；`CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` 环境变量显式覆盖。
- **Windows PowerShell shell**：command hook 设 `shell: "powershell"` 直接跑 PowerShell（pwsh 7+ 自动检测回退 5.1），无需 CLAUDE_CODE_USE_POWERSHELL_TOOL。
- **Hook 安全最佳实践**：command hooks 全权限运行；校验并清洗输入、**始终引用 shell 变量**、阻断路径穿越（`..`）、用绝对路径（exec 形式 ${CLAUDE_PROJECT_DIR}）、**跳过敏感文件（.env/.git/keys）**。
- **Debug hooks**：`--debug-file <path>`/`--debug`；`CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose` 看 matcher 匹配细节。
- 判据：**评估类 hook 用 prompt（便宜），需看真实状态用 agent（带工具）**；长任务旁路用 async+asyncRewake；MCP 交互程序化应答免对话框。
- **提升层**：工具。

### B2：n8n ai-agent-memory 后半：queue mode 会话隔离与 Chat Memory Manager 编程式与 Zep 实体记忆（来源：blog.n8n.io ai-agent-memory 3866-5683 2026-09-25，r207-A X5 的工程细节增量）
- **Simple Memory 单实例开箱即用；queue mode 必须换 Postgres/Redis Chat Memory**：单实例部署会话隔离直接可用，但队列模式多 worker 下 Simple Memory 无法保证跨 worker 会话隔离——这是部署拓扑决定的硬约束。
- **Chat Memory Manager 编程式记忆控制**：插入/检索/清除特定记忆；pruning（查大小/删旧条目）与 injection（插上下文）逻辑所在；配 JS/Python code node 实现标准模式装不下的自定义保留行为。
- **长期记忆后端可换性**：Pinecone/Weaviate/Qdrant 向量存储 + Postgres/Redis Chat Memory；**换存储后端（如 MongoDB Atlas 替换 Pinecone）工作流形状不变，只改后端节点**——记忆层抽象让存储演进不重写 agent。
- **Zep Memory node 实体记忆**：自动从对话提取用户/会话/实体事实（entity extraction+summarization+retrieval 一个子节点），无需手动配置——实体记忆的零配置方案。
- 架构观：n8n 把记忆当**一等工作流原语**（每层可配置/可检视/可修改的节点），覆盖 CoALA 多数记忆类型无需自建基础设施。
- 判据：**部署拓扑决定记忆后端选型**（单实例 vs queue）；记忆增删改查编程式接口+剪枝注入逻辑独立成节点；实体记忆用自动提取免配置。
- **提升层**：工具 / 工作流。

### B3：dify 插件生态治理与 Asqav 可验证行为收据（来源：dify.ai/blog 列表 2026-09-25）
- **Trust Is a Feature（插件生态治理）**：安全/透明/维护三支柱 + 市场治理系统——**Plugin Security Level 分级**；marketplace 点赞/评分/反馈闭环（from discovery to response 更连接的 marketplace）。
- **Asqav 加入 Dify Marketplace**：agent 行为产出**可验证、不可篡改的行为收据（verifiable, tamper-evident receipts）**——每条 routed action 可审计；"From Logs to Evidence"：从日志到证据。
- **Why We Redesigned Dify's Agent**：agents 与 workflows 不是孤立组件而是支持日常工作的协作者（agent 与工作流融合设计观）。
- **I Patched Calendly with New Agent**：用 agent 修补既有软件（不改建、增量增强现成工具）。
- 判据：**插件市场要安全分级+透明度+维护机制**；关键 agent 动作落不可篡改收据（审计证据而非仅日志）；改造存量工具用"patch 式"agent 而非重建。
- **提升层**：可复用 Skill / 工作流。

### B4：智谱 AgentMore 多 Agent 协作与零 Token 技能广场（来源：general_search agentmore.chatglm.cn/智谱官方 2026-09-25）
- **AgentMore 多 Agent 群组协作**：最多 5 个 Agent 同时参与任务；头脑风暴/任务分配两种模式；**"职业+性格+背景+场景"四维人设定义**；自由发言/按需发言双模式；**协作全透明、可干预**（告别系统派单黑盒——每个 agent 的发言与任务可见可控）。
- **Skills 技能广场**：接入 **7.4 万+ 专业技能**（开源社区+第三方主流服务），免费一键安装**不消耗 Token**；技能来源三类=官方严选/Skill Hub/开源社区；技能模块化封装调用零额外 Token。
- **智能体开发平台（docs.bigmodel.cn）**：零代码画布拖拉拽构建任务流+批量调试+页面嵌入/API 接入——"从模型到产品一站式"。
- 生态事实（仅记录）：智谱 4 月 Auto Claw 上线 AgentMore Skills 广场；月之暗面 2 月 Kimi Claw（网页端一键部署 Open Claw+技能库）；美团 xia345（20+ agent/7000+ skill 导航）；觅游社区（3000+ agent/4 万+ skill）——**大模型公司做 Skill 分发最顺理成章：模型本身就是 Skill 宿主**。
- 判据：**多 agent 协作要透明可干预（非黑盒派单）**；技能分发"零 Token 安装"降低采用门槛；人设四维定义让角色可预期。
- **提升层**：工具 / 可复用 Skill。

## 判重说明
- B1 → r207 三段+r208-A 同源 hooks 收尾增量（prompt/agent/async hooks/Elicitation/SessionEnd 均新机制），落。
- B2 → r207-A X5（单 memory 子节点+Chat Memory Manager）的工程细节增量（queue 隔离/Zep 实体记忆/后端可换性），落。
- B3 → 与 r204-C U1（OpenAgentSkill outcome 闭环）互补（市场治理+不可篡改收据），落。
- B4 → 与 r208-A A4（阿里云门户）不同平台不同机制（多 Agent 协作/零 Token/人设四维），落。
- 未落：skills.sh 续读（图片为主）、agentskills.io Client Showcase（生态名单低方法）、pipedream components/api（死链）、waytoagi（工具导航）、openclaw /capabilities（死链）。
