# 学习轮 r204-B：auto memory细则与Make指令工程与Dify实时变量调试与子代理系统细则与实时文档查询（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.n8n.io/advanced-ai/intro-tutorial/（续 3041-6591） | OK（节点配置/credentials 助手） |
| 2 | docs.dify.ai/en/guides/workflow/chatflow | 死链 |
| 3 | docs.anthropic.com/en/docs/claude-code/memory（全文 5714） | OK（CLAUDE.md vs auto memory 全页） |
| 4 | help.make.com/make-ai-agent-new-best-practices | OK（3135 字，官方 best practices 全文） |
| 5 | deepseek-plugin.org/plugins（续 13224-19785，#29-31） | OK（armor-breaking/sandbase 无大新） |
| 6 | docs.pipedream.com/workflows/ | OK（1090 字：steps/step notes） |
| 7 | skills.sh/skills | OK（56 字：仅 GitHub official secure-code-game） |
| 8 | skillsmp.com/skills/page/19（全文 11612，#1801-1900） | OK（100 项） |
| 9 | openagentskill.com/agents | OK（622 字：Agent fit 按 9 个 agent 排 fit） |
| 10 | waytoagi.com/（3149/80377） | OK（工具精选导航壳） |
| 11 | docs.langflow.org/storages | 死链 |
| 12 | docs.anthropic.com/en/docs/claude-code/sub-agents（3995/13044 首段） | OK（子代理系统细则） |
| 13 | general_search Dify 调试 | OK（Variable Inspector/step-by-step/类型不匹配） |

## 独点（5 个）
### O1：Anthropic auto memory 细则：MEMORY.md 200 行/25KB 加载上限 + topic files 按需 + compact 后 CLAUDE.md 重注入 + InstructionsLoaded hook（来源：docs.anthropic.com/en/docs/claude-code/memory，与 r204-A N1 互补）
- **auto memory 存储**：`~/.claude/projects/<project>/memory/`，`MEMORY.md` 入口（**前 200 行或 25KB 先加载**，Claude 主动保持精简、把细节挪到 topic files）；topic files（debugging.md/api-conventions.md）不在启动加载，按需用文件工具读。
- **autoMemoryDirectory 不接受 project settings**（只接受 policy/local/user）——防共享项目把记忆写向敏感位置。
- **compact 后 CLAUDE.md 从磁盘重读重注入**——写进 CLAUDE.md 的指令不丢；"压缩后指令消失"的真相是那指令只在会话里口头说过，没落盘。
- **CLAUDE.md 以 user message 送达而非 system prompt**——不保证严格遵从；要进 system 用 `--append-system-prompt`（每次调用传）。
- **InstructionsLoaded hook**：日志记录哪些指令文件加载、何时、为何——调试 path-specific rules / 子目录懒加载。
- **claudeMdExcludes**：glob 排除无关团队 CLAUDE.md（settings 层数组合并；managed policy 不可排除）。
- **@import 语法**：`@README`/`@~/.claude/my-project-instructions.md`，相对路径从包含文件解析，最深 5 层递归，首次外部导入弹批准框。
- 判据：**记忆文件是分层接口**——入口薄（200 行内）、细节厚（topic 按需）；压缩后规则存活靠落盘不靠会话。
- **提升层**：工作流 / 上下文管理。

### O2：Make AI Agent 指令工程七要素：工具名含否定条件 / 输入输出示例 / guardrails 定义期望与不期望 / 知识三不用 / 模型先大后小 / LLM 改写指令 / token 优化留空会话（来源：help.make.com/make-ai-agent-new-best-practices）
- **工具命名与描述**：名+描述决定 agent 选不选它——描述要写**何时调用 + 何时不调用**（"add customer email to spreadsheet. Do not add if email address is invalid or already exists"）。
- **指令七大项**：全步骤/每步调的工具（含名+功能）/每步引用哪些知识文件+含什么/guardrails（**定义期望与非期望行为**）/输入输出示例含格式/异常情况怎么响应。
- **knowledge 三不用**：模糊信息、敏感数据（客户信息/账单）、频繁变化数据（客户目录）、低质样本——GIGO，低质输入出低质输出。
- **模型先大后小 scale-down**：先大 LLM 确认好表现，再逐步降级小模型；小模型够用简单分类/路由，复杂多步用大模型。
- **AI improved instructions**：多数错误源于指令不清——用 LLM 改写 prompt 而不是手改，加 reasoning tab 的思考内容再迭代。
- **token 优化**：filter inputs（把搜索限到日期/字段、只映射单值）、filter tool outputs（只选要的字段）、reference 文件作 knowledge、**留空 conversation id 减少历史传参**；子代理当工具只在需要自身推理时用。
- **数据最小化**：只给所需数据（暴露 free/busy 而非整个日历）；guardrails 可能被忽略，按"任何人都可能看到数据"来选数据。
- 判据：**指令是简报文件**——越具体越少不可预测；工具描述要写"什么时候别用"。
- **提升层**：提示工程 / 工作流。

### O3：Dify Variable Inspect 实时调试：全局变量面板 + 直接编辑测下游免重跑昂贵上游 + 类型不匹配静默失败（来源：Dify 1.5.0 官方博客 + DeepWiki 调试文档）
- **Variable Inspect Panel**：画布底部全局面板，实时显示整个 workflow 所有变量；**直接编辑变量值**测试下游节点，不用重跑昂贵上游（LLM 调用/API 请求/DB 查询）——边缘用例测试成本大降。
- **Step-by-step 执行**：跑到目标节点→开 Variable Inspect→编辑缓存变量（复杂类型支持 JSON 编辑）→"run step" 让下游用修改值执行。
- **调试纪律**：**描述性变量名**（filtered_customer_list 而非 output1）；**历史对比**（对比成功/失败 run 找间歇问题）；先查上游再查下游。
- **类型不匹配静默失败**：source 输出与 destination 输入类型不一致时，路径语法正确也会运行期静默失败——变量映射先对齐类型。
- 判据：**调试的杠杆在"不重跑上游"**——能直接改中间变量测边界，就别反复烧昂贵调用。
- **提升层**：工具 / 工作流。

### O4：Claude Code 子代理系统细则：内置四类 + scope 五级优先级 + plugin 安全字段忽略 + --agents 会话级 JSON（来源：docs.anthropic.com/en/docs/claude-code/sub-agents，r203-B 的深度增量）
- **内置四类**：Explore（Haiku 只读，thoroughness 三档 quick/medium/very thorough，拒绝 Write/Edit）/ Plan（plan mode 只读，**防无限嵌套——subagents 不能再生 subagents**）/ general-purpose（全工具多步）/ 其他（statusline-setup 等）。
- **scope 优先级**：managed settings（组织，最高）> `--agents` CLI（会话级）> `.claude/agents/`（项目）> `~/.claude/agents/`（用户）> plugin agents（最低）；同名高优先级赢；**同 scope 同名静默丢弃不警告**。
- **plugin subagents 安全限制**：不支持 `hooks`/`mcpServers`/`permissionMode` frontmatter（加载时忽略）——需要就复制到项目/用户目录。
- **--agents JSON**：会话级定义（description/prompt/tools/model 等），适合脚本化快速测试，不落盘。
- **isolation: worktree**：子代理可拿仓库隔离副本；`cd` 不跨 Bash 调用持久、不影响主会话。
- **agent teams 复用 subagent 定义**：teammate 用其 tools/model，body 追加为附加指令。
- 判据：**子代理的权限面=定义字段**——plugin 来的定义天然少 hooks/权限字段，想用就走本地目录。
- **提升层**：工具 / 工作流。

### O5：实时文档代替训练数据 + 发信验证闭环 + 测试点五维 XMind（来源：skillsmp p19：documentation-lookup/email-ops/generator-testcase-xmind）
- **documentation-lookup**：查库/框架文档走 Context7 MCP 实时源，不靠训练数据——setup 问题/API 参考/代码示例触发。
- **email-ops（evidence-first 邮箱）**：triage/草稿/**发送验证**（证明什么真的进了 Sent）+ sent-mail-safe 跟进——邮件交付以 Sent 为证，不猜。
- **generator-testcase-xmind**：用户故事→测试点→XMind 思维导图，覆盖功能/边界值/异常/业务规则/非功能五维 + P0/P1/P2 优先级标注。
- 判据：**文档查实时源**；**邮件发没发以 Sent 为证**；**测试点输出成可评审的图**。
- **提升层**：工具 / 可复用 Skill。

## 判重说明
- O1 → r204-A N1 已有成本页；memory 页的"加载上限/topic 按需/compact 重注入/InstructionsLoaded hook/claudeMdExcludes"为独有增量，落。
- O2 → 与 wb-execute-discipline 提示词纪律互补；"工具描述含否定条件/guardrails 双定义/知识三不用/scale-down/留空会话 id"为独有增量，落。
- O3 → 与 r204-A N5（Make 工作流记忆）互补；"变量面板直接编辑免重跑/类型不匹配静默失败"为独有增量，落。
- O4 → r203-B 子代理 fork 已录；"内置四类/scope 优先级表/plugin 安全字段忽略/--agents JSON"为深度增量，落。
- O5 → documentation-lookup/email-ops/xmind 测试点均为独点（无既有记录），落。
- skillsmp 家族项（hands-on-deck/context-compression/superppt）→ 与豆包 ppt/context 套件重叠或增量不足，不落；waytoagi 导航壳、skills.sh /skills 单源页、pipedream workflows 无大新，不落。
