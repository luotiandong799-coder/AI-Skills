# 学习轮 r208-A：Anthropic hooks事件矩阵与n8n自纠正循环与skillsmp规则蒸馏与阿里云技能门户（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.anthropic.com hooks 页续读（21977-29977/34780） | OK（PostToolBatch/Task 门控/ConfigChange/Worktree/PreCompact） |
| 2 | skillsmp.com/skills/page/29（#2801-2832） | OK（rules-distill/goalpro/neat-freak/multi-expert-analyzer2） |
| 3 | blog.n8n.io production-ai-playbook 续读（10774-19237 全取完） | OK（自纠正循环/写评分离/链vs代理/成本五策略） |
| 4 | docs.pipedream.com/docs/cron/ 续读 | 死链 |
| 5 | docs.openclaw.ai 根页续读（3451-4870 全取完） | OK（WhatsApp allowFrom/群@mention，低增量） |
| 6 | skills.sh 首页 | OK（npx skills add 单命令安装，低内容） |
| 7 | cloud.tencent.com/product/skillhub | fetch error |
| 8 | open.bigmodel.cn/agentmore | 空页（仅站点名） |
| 9 | general_search 阿里虾小宝/阿里云技能门户 | OK（skills.aliyun.com find-skills/AI Registry/FunClaw） |
| 10 | learn.deeplearning.ai | OK（notebook 操作指引，低价值） |

## 独点（4 个）
### A1：Anthropic hooks 事件矩阵第三段：PostToolBatch 批级上下文与 Task 完成门控与 ConfigChange 审计（来源：docs.anthropic.com hooks 21977+ 段 2026-09-25，r207 三段的续读增量）
- **PostToolBatch 批级上下文注入**：并行工具调用时 PostToolUse 每工具一次并发触发；PostToolBatch 在整批全部 resolve 后**恰好一次**——注入依赖"这组工具整体"的上下文（如"这些文件属于 ledger 模块，完成前跑 pytest"）；输入带 tool_calls 数组，`tool_response` 是模型看到的序列化 tool_result 内容（与 PostToolUse 的结构化 Output 不同，Read 返回带行号文本）；decision block/continue false 可停 agentic loop。
- **PostToolUseFailure**：工具失败钩子（error/is_interrupt/duration_ms 顶层字段），additionalContext 给 Claude 纠正反馈。
- **PermissionDenied retry 机制**（auto mode 专用）：分类器拒绝工具后，hook 返回 `retry: true` 可让模型重试（**拒绝本身不撤销**，只是加一条"可以重试"消息）；不返回或 false 则拒绝成立。
- **Task 生命周期门控**：TaskCreated/TaskCompleted/TeammateIdle 三个钩子——exit 2 阻止任务创建/标记完成/teammate 空闲（stderr 作为反馈喂回模型）；JSON `continue:false+stopReason` 停整个 teammate；TaskCompleted 可强制"测试通过才能关任务"；TeammateIdle 可要求"构建产物存在才允许 idle"。
- **Stop/StopFailure**：stop_hook_active 字段防死循环（检查它避免阻塞永不可解的条件）；**8 次连续 block 后 Claude Code 强制结束本轮**；StopFailure 按错误类型 matcher（rate_limit/authentication_failed/billing_error/max_output_tokens 等）做告警与恢复。
- **ConfigChange 五源审计**：user_settings/project_settings/local_settings/policy_settings/skills 五种 source；exit 2/decision block 阻止配置生效；**policy_settings 变更不可阻断**（企业托管设置永远生效，hooks 只做审计）——内部 skill 文件变更也在审计范围（skills source）。
- **CwdChanged/FileChanged**：目录/文件变化钩子；`watchPaths` 返回数组动态设置 FileChanged 监听（空数组清空动态列表）；FileChanged matcher 双角色（按字面文件名建监听列表 + 按 basename 过滤钩子组）；两者都有 CLAUDE_ENV_FILE 持久化。
- **WorktreeCreate/Remove**：自定义 worktree 创建（SVN/Perforce/Mercurial 替换默认 git worktree），命令钩子 stdout 返回绝对路径、HTTP 钩子 worktreePath 字段；`.worktreeinclude` 不处理（需钩子脚本内复制 .env 等）；Remove 收尾必须配对否则目录残留。
- **PreCompact 阻止压缩**：matcher manual（/compact）/auto（窗口满）；exit 2 阻止；**auto 时机决定效果**（主动提前压缩时跳过继续运行 vs 已因超限报错时底层错误上浮请求失败）。
- 判据：**批级注入用 PostToolBatch（单次非并发）**；完成门控放 Task/Teammate 钩子；企业托管配置只审计不阻断。
- **提升层**：工具 / 工作流。

### A2：n8n production playbook 后半：自纠正循环与写评分离与链-代理混合与失败域隔离（来源：blog.n8n.io production-ai-playbook-complex-agent-patterns 10774-19237 2026-09-25，r207-B Y2 的工程实现层增量）
- **自纠正 agent loop 配方**：生成→确定性验证（Code 节点 schema/规则）或 LLM-as-judge→**带具体错误列表的反馈**（"confidence 1.5 超出 0-1 范围；category 'misc' 不在允许列表"而非"再试一次"）→maxAttempts 上限退出转人工；响应信封跨成功/失败稳定（success/hitMaxAttempts/routedTo: human_review）；两独立状态层=memory 跨会话连续 + 循环内质控。
- **Writer/Critic 分离双 agent 循环**：Writer 起草、Critic 按四维加权评分（accuracy/clarity/relevance/conciseness）+ 枚举问题；Writer 永不自评、Critic 永不写；**可给 Writer 便宜模型、Critic 强模型**；maxIterations 退出保留最后草稿+未解决 feedback 给人审。
- **Prompt Chaining vs Agent Delegation 决策**：链=固定序列每步简单 LLM 调用（可预测/可调试/省 token）；代理=运行时涌现路径（输入依赖/多行动选择/novel 输入/迭代推理）；**最佳系统两者混合：可预测部分用链（清洗/格式化/终验），灵活部分用代理，其余确定性逻辑**——最小化 agent 推理范围。
- **拆架构三档框架**：flat（3-5 步线性无分支/单人维护/单用例/原型期）；break sub-workflow（跨流重复逻辑/超 15-20 节点难导航/不同专业维护/需独立测试/失败需隔离）；add multi-agent（输入模糊需推理定路径/子任务需根本不同模型工具提示词/novel 任务/单 agent 上下文溢出）。**先单 agent 后分解**。
- **失败域隔离**：每 agent 自带错误处理，返回结构化失败响应（success/error.type/message/attemptCount/lastOutput/fallback），失败不级联崩溃编排器；回退四策略=简化 prompt 重试→更简单模型→人工升级→低风险安全默认模板（模板响应优于幻觉或静默失败）；**显式超时 30 秒起点，agent 挂起卡整个管线**。
- **成本五策略**：①scope context per agent（只传相关上下文不传全量历史）②right model per task（分类/路由/简单提取用轻量模型）③limit loop iterations（2-3 次足够，超过是 prompt 或任务定义问题）④**minimize tool descriptions（每个工具描述每请求都进上下文，15 工具只用 3 个→拆聚焦 agent，省 token 且选择更准）**⑤monitor+budget（按执行/agent/工具调用跟踪，异常 token 尖峰=prompt 问题/循环超预期/上下文无界）。
- **确定性路由优先**：能 Switch 分类就别让 agent 选（快/便宜/不会误读描述）；agent 路由只在输入真正模糊时；日志编排者每次路由决策+触发输入（审计轨迹修 misroute）。
- 判据：**循环必有上限且带具体反馈**；写评分离可换模型强度；先链后代理最小化推理面；每个组件都要能答"失败会怎样"。
- **提升层**：工作流。

### A3：skillsmp p29：rules-distill 规则蒸馏与 goalpro Goal Contract 与 neat-freak 知识收尾（来源：skillsmp.com/skills/page/29 2026-09-25）
- **rules-distill 规则蒸馏**：扫描技能库提取跨切原则，**同一原则在多个技能反复出现→蒸馏进规则文件**（append/revise/create），而非在各技能内重复抄写——规则文件是跨技能原则的唯一归处。
- **goalpro Goal Contract**：把模糊/战略性/多步骤/证据不足的请求整理成**可执行、可验证、可暂停的 Goal Contract**（明确 done/success criteria）；默认只生成 goal 不执行 goal——"先写清验收再动手"的契约化。
- **neat-freak 知识治理收尾**：把项目文档/规则文件（CLAUDE.md/AGENTS.md）/授权 agent 记忆/工作区残留与**代码和运行时实际状态 reconcile**，让下个会话或下个人从**单一当前答案**开始；触发=收尾时"文档和代码对不上了"、stale/冲突的 CLAUDE.md/memory、交接前审计工作区规则是否真被执行。
- **multi-expert-analyzer2 多专家+红队+终稿**：多领域专家并行深度分析→克制的事实核查+红队反驳→"干净大脑"终稿撰写者重写为第一人称/面向小白/图文并茂/留证伪空间的长文——分析、反驳、成稿三段由不同角色承担。
- **mcp-server-patterns**：Node/TS SDK 构建 MCP server 的模式集（工具/资源/提示/Zod 验证/stdio 与可流式 HTTP 对比）。
- **humanize-korean 分级去 AI 味**：10 大类别 70 个 AI 味模式检测分类，内容一字不改只重写文体/节奏/表达；route_hint（light|standard|heavy）分级 1/2/3+ 次调用（诊断→定向润色→finalize）——与 r207-B Y4 白名单去 AI 味互补：**按"AI 味严重度"路由调用次数而非一刀切**。
- 判据：**重复出现的原则归规则文件不重复进技能**；goal 先契约后执行；收尾时文档/记忆/残留对齐运行时真态。
- **提升层**：可复用 Skill。

### A4：阿里云 Agent Skills 门户与虾小宝：云厂商官方技能目录与 find-skills 一行安装（来源：general_search skills.aliyun.com/skillhub.wanuai.cn/阿里云帮助中心 2026-09-25）
- **阿里云 Agent Skills 门户（skills.aliyun.com）**：官方技能目录按产品分类（计算 14/AI 与机器学习 25/开发工具 15/迁移运维 12/存储 22/网络 CDN 4/中间件等）；`find-skills` 按使用场景搜索并安装官方 skills；每 skill 带描述/一行安装命令/质量指标/源码链接。
- **虾小宝（skillhub.wanuai.cn）**：中国 AI Agent Skills 地图 v3.0.3 platform；含**自主技能生成器**——/learn <主题> 从网络学习新技术（搜索+浏览器挖掘+文档综合）生成可复用技能。
- **AI Registry Skill 中心（企业私有化）**：权限管理/版本管理/审计/内容安全防护四件套——个人自建技能库可借鉴的治理维度。
- **FunClaw 预置技能栈**：agent-browser（网页访问信息提取）/self-improvement（持续优化对话质量）/find-agentrun-skills（发现推荐技能）/fc-vpc-proxy（函数计算代理访问 VPC）/searxng（默认搜索）——云函数场景的默认技能组合。
- 生态事实：3 月腾讯/阿里/字节先后上线 Skill 商店；腾讯 SkillHub 本土化 ClawHub（微信小程序生态）；字节双线（火山 FindSkill 企业向 + 扣子开发者向）——大厂 Skill 分发是 2026 生态主线（仅记录不投入）。
- 判据：**需要某云能力时先查官方 find-skills 一行安装**，不自己造轮子；自建技能库参考权限/版本/审计/安全四治理维度。
- **提升层**：工具 / 可复用 Skill。

## 判重说明
- A1 → r207 三段 hooks 同源续读增量（PostToolBatch/Task 门控/ConfigChange/Worktree/PreCompact/PermissionDenied retry 均新事件），落。
- A2 → r207-B Y2（完成标准前置/验证门）的循环实现+架构决策+成本工程增量（Writer-Critic 分离/链vs代理/拆架构三档/成本五策略），落。
- A3 → 新概念（规则蒸馏/Goal Contract/知识收尾/多专家红队），humanize-korean 与 r207-B Y4 分级路由增量合并，落。
- A4 → 新（云厂商官方技能目录/私有中心四治理维度），落。
- 未落：openclaw 根页收尾（WhatsApp 配置与 r207-A X4 同族低增量）、skills.sh（首页低内容，后续轮续读）、腾讯 SkillHub/智谱 AgentMore（打不开）、deeplearning.ai learn（notebook 操作指引非方法论）、agentskills.io Overview（与 r205-B S2 spec 重叠>60%）。
