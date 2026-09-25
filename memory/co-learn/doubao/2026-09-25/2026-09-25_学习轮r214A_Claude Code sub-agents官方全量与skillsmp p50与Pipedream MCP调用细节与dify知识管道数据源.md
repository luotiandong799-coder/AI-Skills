# 学习轮 r214-A：Claude Code sub-agents官方全量与skillsmp p50与Pipedream MCP调用细节与dify知识管道数据源（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/50（#4901-4961，5971/10976 取） | OK（one-off-operations/data-quality-checker/lengdu 等） |
| 2 | dify.ai/blog 续读（54378-59974） | OK（Qdrant/Bright Data/Tavily/Visual Agentic Workflow） |
| 3 | docs.anthropic.com claude-code/sub-agents（5989/13044 取前半） | OK（内置三件套/frontmatter/作用域） |
| 4 | docs.langflow.org/configure-tools | 死链（link dead，计数） |
| 5 | docs.anthropic.com claude-code/sub-agents 续读（5989-11987） | OK（skills 预载/记忆/前台后台/resume/fork） |
| 6 | github.com/trending（不带 offset，4180/73442 取） | OK（paperclip ★83,222 新条目） |
| 7 | deeplearning.ai/short-courses 续读（21346-25909） | OK（Multi-vector Image Retrieval/Spec-Driven） |
| 8 | pipedream.com 根页重拉（4320B） | OK（remote MCP URL/x-pd-external-user-id/pd.proxy） |
| 9 | github.com/trending 续读（3161-7303） | OK（claude-plugins-official ★36,734，与 r213-C 重叠） |
| 10 | waytoagi.com 根页（4188/80377 取） | 低方法（工具导航页） |

## 独点（4 个）
### A1：Claude Code sub-agents 官方页全量：内置三件套 / 5 级作用域 / frontmatter 全字段 / 记忆与 fork（来源：docs.anthropic.com/en/docs/claude-code/sub-agents，2026-09-25 实拉）
- **内置子代理**：Explore（Haiku 只读，thoroughness quick/medium/very thorough）/ Plan（plan mode 研究，防无限嵌套——**子代理不能再生子代理**）/ general-purpose（全部工具复杂多步）；statusline-setup/claude-code-guide 辅助。
- **5 级作用域优先级**：Managed settings（组织级最高）> --agents CLI（仅本次会话，JSON 定义）> .claude/agents/（项目，可进 VC）> ~/.claude/agents/（个人）> plugin agents/（最低，**插件子代理不支持 hooks/mcpServers/permissionMode**）。
- **frontmatter 全字段**：name（必填，小写连字符）/description/tools（allowlist）/disallowedTools（denylist，先 applied 再 resolved）/model（sonnet/opus/haiku/全 ID/inherit 默认）/permissionMode（default/acceptEdits/auto/dontAsk/bypassPermissions/plan）/maxTurns/skills（**预载注入完整内容非仅描述**；不能预载 disable-model-invocation:true）/mcpServers（**内联定义作用域子代理且不进主对话省 context**；字符串引用共享父连接）/hooks/memory/background/effort/isolation:worktree（临时 git worktree 隔离，无改动自动清理）/color/initialPrompt。
- **spawn 限制**：`Agent(agent_type)` 语法 allowlist 限制主线程 agent 可 spawn 的类型；省略 Agent 则完全不能 spawn；模型解析顺序 env > 单次参数 > 定义 > 主对话。
- **persistent memory 三 scope**：user（~/.claude/agent-memory/）/project（.claude/agent-memory/ 进 VC）/local（.claude/agent-memory-local/ 不进 VC）；**system prompt 含首 200 行或 25KB MEMORY.md**+curate 指令；Read/Write/Edit 自动启用；模式：开始前查记忆、完成后存记忆。
- **前台 vs 后台**：前台阻塞透传权限提示；后台并发、自动拒绝会提示的调用、clarifying 失败继续；fork mode 时全部后台。
- **resume/fork**：SendMessage 带 agent ID（agent teams 实验开关）；transcript 独立于主对话（主对话 compact 不影响，cleanupPeriodDays 默认 30 天）；fork（CLAUDE_CODE_FORK_SUBAGENT=1，v2.1.117+）继承全部会话并**复用父 prompt cache 更便宜**，工具调用不进主对话只回结果；fork 不能再 fork。
- **选择判据**：频繁往返/共享上下文/快速定向/延迟敏感→主对话；verbose 输出/工具限制/自包含→子代理；/btw 快速问题（全 context 无工具答案丢弃）。
- **提升层**：可复用 Skill / 工作流（多 agent 官方参考）。

### A2：skillsmp p50 精选：一次性 vs 可复用 / 内容数据质量门 / 专家会诊 / 读感校验三角色（来源：skillsmp.com/skills/page/50，2026-09-25 实拉）
- **one-off-operations（n8n-io/n8n ★203,692）**：一次性操作（导出/复制/迁移/回填/清理）——**请求是"发生一次的具体效果"，无触发/排期/复用意图；用户很少说 one-off，从任务形状推断**；"workflow 是载体不是交付物"；用户会再次运行的自动化不加载——**一次性 vs 可复用判别**。
- **data-quality-checker（BaggaT236/AI-Trading-Skills ★125）**：市场分析文档发布前数据质量门——价格刻度不一致（ETF vs futures）、instrument 记法、日期/星期不匹配、分配合计错误、单位不匹配；**Advisory mode 标记为警告供人审，不作阻断**。
- **multi-expert-analyzer（digoal/blog ★8,578）**：多领域专家联合分析——主控识别领域→调度 1~N 专家并行搜证→**事实核查员与红队克制温和二次审查**→综合成第一人称面向小白 markdown。
- **lengdu（asass-11/lengdu ★36）**：中文小说读感校验闭环——主 Agent 写正文、作者侧校准者查人物形成缺失/叙事过满、长期进化普通 Reader 判断读感；用户要求兼顾朱雀人工特征时**以隐藏版本身份 A/B 冷读守住原稿读感**。
- **dashboard-design（mckinsey/vizro ★3,795）**：设计 dashboard 前强制 3 步（需求/布局/可视化），实现走 dashboard-build——**设计与实现分两个 skill 路由**。
- **ccf-literature-searcher（mikubaka88/CCFA-Skills ★2,711）**：检索 vs 监视 vs 审计分工——检索/prior art/benchmark 归 searcher，recurring 论文监视归 monitor，现有引用审计/手稿评估/结果 schema 各归其主。
- **提升层**：可复用 Skill / 工作流。

### A3：Pipedream MCP remote server 调用细节 + GitHub paperclip（来源：pipedream.com 根页 + github.com/trending，2026-09-25 实拉；与 r213-A A4 Pipedream MCP 概念合并保留增量）
- **remote MCP server 具体形态**：`https://remote.mcp.pipedream.net` + 请求头 `x-pd-external-user-id`——点任意 MCP client（url+headers 两行接上）；agent 选工具、认证已处理（`client.callTool({name:"slack-send-message",...})`）。
- **代理 API 模式**：`pd.proxy.post({url, externalUserId, accountId, body})`——从代码直接调任意 API，认证托管。
- **规模事实**：10,000+ tools、3,000+ APIs、1M+ 开发者、source-available 组件注册表。
- **paperclip（paperclipai/paperclip ★83,222，+15,117 today）**：管理工作中 agent 的开源 app——agent 运维管理面成为独立品类。
- **提升层**：工具 / 工作流。

### A4：dify 知识管道数据源矩阵 + deeplearning.ai 多向量检索（来源：dify.ai/blog + deeplearning.ai，2026-09-25 实拉）
- **向量库矩阵**：Qdrant（Rust 高性能，**hybrid search**）；TiDB Vector（**分布式语义搜索、可扩展上下文管理**）——生产级知识管道按规模选型。
- **外部实时数据源入管道**：Bright Data Web Scraper 插件（实时结构化 web 数据）、Tavily web search API（实时网页数据直接嵌入知识管道增强准确性）——知识管道不只静态文档，可接实时 web 源。
- **Visual Agentic Workflow**：OpenAI AgentKit 印证 Dify 长期追求——可视化、可靠编排是构建智能的未来；开放、模型中立。
- **Multi-vector Image Retrieval（Qdrant 课程）**：用多个向量表示图像，文本查询与视觉内容细粒度匹配——多向量图像检索范式。
- **提升层**：工作流（RAG/知识管道架构）。

## 判重说明
- A1 → Claude Code sub-agents 官方全量（内置三件套/作用域/frontmatter/记忆/fork），新页，落。
- A2 → skillsmp p50 精选（一次性判别/质量门/专家会诊/读感校验），全新，落。
- A3 → Pipedream remote MCP 调用细节+paperclip，与 r213-A A4 合并保留增量，落。
- A4 → dify 向量库矩阵+实时数据源+多向量检索，RAG 层增量，落。
- 未落：claude-plugins-official（与 r213-C C1 重叠）、WaytoAGI（工具导航低方法）、ai-engineering-from-scratch（与 r211-B 重复）、langflow configure-tools（死链计数）。
