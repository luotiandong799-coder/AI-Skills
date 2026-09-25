# 学习轮 r206-C：Anthropic子代理官方页与n8n上下文工程顺序判据与skillsmp视觉护栏与Dify六组件与pipedream隐私执行（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.anthropic.com/en/docs/claude-code/sub-agents（3995/13044） | OK（Explore/Plan/general-purpose 分工+防嵌套+scope 五级） |
| 2 | dify.ai/blog/build-your-first-agent-in-dify（3826/16541） | OK（六组件+Build Note） |
| 3 | skillsmp.com/skills/page/25（#2401-2431） | OK（modlens/anti-defensive/officecli 分层） |
| 4 | blog.n8n.io context-engineering-llm 续读（3993-6486 全） | OK（四策略顺序/可调试 JSON payload/MCP 子集） |
| 5 | docs.pipedream.com/cron/（3996/9855） | OK（event source 分离/x-pd-nostore/授权） |
| 6 | docs.openclaw.ai/get-started/overview | 死链 |
| 7 | make.com/en/help/scenarios | 空页（仅 3B） |
| 8 | agentskills.io/specification（1797 全） | OK（与 r205-C T1 全重复，无增量不落） |
| 9 | deepseek-plugin.org/ | fetch error（死链，本轮累计 4 次失败，疑似整体失效待告知） |
| 10 | waytoagi.com/ai-tools | 死链 |

## 独点（5 个）
### W1：Anthropic subagents 官方页：内置子代理分工与 scope 五级与安全限制（来源：docs.anthropic.com sub-agents 2026-09-25，r204-C P2 子代理细则的官方页增量）
- **内置三代理分工**：Explore（Haiku 只读，denied Write/Edit，thoroughness 三档 quick/medium/very thorough）/ Plan（plan mode 研究，只读，**防无限嵌套：subagent 不能 spawn subagent**）/ general-purpose（继承主对话模型+全部工具，复杂多步）。
- **scope 五级优先级**：managed settings > --agents CLI（会话级 JSON，即用即弃不落盘）> .claude/agents/（project）> ~/.claude/agents/（user）> plugin agents/（最低）；--add-dir 只给文件访问**不扫 subagents**。
- **递归扫描与 identity**：子目录组织（agents/review/）不影响调用，identity 只来自 name 字段；**同 scope 内重名静默丢弃一个不警告**；plugin 子目录成 scoped identifier（my-plugin:review:security）。
- **plugin subagent 安全限制**：不支持 hooks/mcpServers/permissionMode（加载时忽略）——需要就拷到本地 agents 目录。
- **isolation: worktree**（给子代理独立 repo 副本）+ **memory: User scope**（~/.claude/agent-memory/ 跨对话累积代码库模式与反复问题）。
- **subagent 只收自身 system prompt**（+基本环境），非完整 Claude Code system prompt；cd 不跨 Bash 调用持久。
- 判据：**探索代理只读、规划代理防嵌套**；插件子代理不信任敏感字段。
- **提升层**：工作流 / 可复用 Skill。

### W2：n8n 上下文工程四策略执行顺序 + 可调试性（来源：blog.n8n.io context-engineering-llm 后半 2026-09-25，r205-A R2 的增量）
- **顺序即成本**：Select→Compress→Isolate——"**Compressing data you shouldn't have selected in the first place is not worth the effort**"（先选再压，压了不该选的没意义）。
- **token-pruning models**（专用去冗余词 token 修剪模型）+ **JSON 结构化事实**（关键字段传 JSON 不传整段）。
- **可调试性**：n8n 把 context 生命周期暴露为可配置可检查节点——agent 失败**打开执行历史直接看那次推理的确切 JSON payload**（输入、模型返回、日志），"you don't have to guess what went wrong"。
- **MCP just-in-time retrieval**：MCP Client Tool 节点查询外部 servers，**只选该 server 暴露工具的子集**，system prompt 保持精简。
- **sub-agent 工具隔离**：data-analysis 子代理只载数据库工具 schema，writing 子代理只载风格指令，只传干净最小输出。
- **provider-agnostic**：换模型不重建编排层。
- 判据：**先选后压**；失败排查看真实 payload 不靠猜。
- **提升层**：工作流。

### W3：skillsmp p25：modlens 视觉护栏三态 + anti-defensive-writing + officecli 场景分层（来源：skillsmp.com/skills/page/25 2026-09-25，与 r206-B V4 互补）
- **modlens（文本模型视觉插件）**：**三态路由**——图像路径出现在会话且你看不到内容→跑 skill（禁自建 OCR/PIL/tesseract）；能看到→不用；`modlens guard` 拒绝→当前模型有原生视觉必须自己读。护栏式判断而不是每图都跑。
- **anti-defensive-writing（去防御性写作）**：删 unnecessary caveats/disclaimers/hedges/自限否定/过度解释——**保留承重的 scope/accuracy/safety/ethical/legal/methodological 限制**（"删盾牌不拆承重墙"）；在 claim hierarchy 和 integrity audits 定稿后、final sentence pass 前运行。
- **officecli-data-dashboard 场景分层**：多元素 dashboard（KPI cards/charts/sparklines/conditional formatting）→ dashboard 技能；单预算跟踪器/单表 CSV→xlsx；三表/DCF/LBO→financial-model；周报≤1 图<10 行→xlsx——按产物复杂度路由不按名称。
- 判据：**能力边界用可判定条件路由（看得到/看不到/有原生视觉）**；删防御保留承重。
- **提升层**：可复用 Skill。

### W4：Dify agent 六组件与 Build Note（来源：dify.ai/blog/build-your-first-agent-in-dify 2026-09-25，r206-B V2 的 tutorial 视角增量）
- **agent 六组件**：Model（引擎，选原生 tool calling）/ Prompt（角色职责规则期望输出）/ Skills（可复用方法）/ Files（参考材料）/ Tools（动作能力）/ **Build Note（重要决策和变更携带前进，方便继续改进）**。
- **三创建入口**：Create from Blank / Import OSS File / Import from Template。
- **最小可用起步**：先定清晰职责再按需加能力，不一开始配全。
- 判据：**agent=指令+能力+变更记录**三要素；Build Note 是 agent 的"运行日志"。
- **提升层**：工具 / 工作流。

### W5：pipedream event source 分离与隐私执行（来源：docs.pipedream.com/cron/ 2026-09-25）
- **event source 独立于 workflow**：一个 source 可触发多个 workflow——**数据生产与逻辑处理分离**；SSE/REST API 外部消费事件。
- **HTTP trigger 两内建授权**：custom token（Bearer）/ OAuth；默认公开需自行加。
- **x-pd-nostore=1**：执行全部步骤但**不写任何日志**（敏感数据不落 inspector/Event History）；全局用 Data Retention controls。
- **x-pd-notrigger=1**：测试事件不触发生产版 workflow。
- **大 payload**：512KB 上限可经 pipedream_upload_body=1 绕过→S3 signed URL 30 分钟有效后删除。
- 判据：**敏感执行显式禁日志**；触发源与处理逻辑解耦。
- **提升层**：工具。

## 判重说明
- W1 → r204-C P2（子代理系统细则）官方页增量（三代理分工/防嵌套/scope 五级/plugin 安全限制/isolation/memory 目录），落。
- W2 → r205-A R2（上下文工程四源四策略）增量（顺序判据/可调试 payload/MCP 子集/token-pruning），落。
- W3 → r206-B V4 互补（另一页生态）；modlens 三态/anti-defensive 新，落。
- W4 → r206-B V2 同源 tutorial 视角（Build Note 列名/三入口），小增量合并落。
- W5 → 新（pipedream 触发与隐私首次详拉），落。
- 未落：agentskills spec（与 r205-C T1 全重复）、make scenarios（空页）、openclaw overview（死链）、waytoagi ai-tools（死链）。
