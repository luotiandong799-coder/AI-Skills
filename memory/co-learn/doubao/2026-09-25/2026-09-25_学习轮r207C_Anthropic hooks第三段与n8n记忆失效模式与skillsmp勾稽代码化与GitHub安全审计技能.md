# 学习轮 r207-C：Anthropic hooks第三段defer机制与n8n记忆失效模式与skillsmp勾稽代码化与GitHub安全审计技能（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.anthropic.com hooks 页续读（17983-21977/34780） | OK（PreToolUse 四决策/defer/updatedToolOutput/权限规则注入） |
| 2 | skillsmp.com/skills/page/28（#2701-2727） | OK（audit-report-checker 勾稽/no-negative-echo/scipilot Gate8） |
| 3 | docs.openclaw.ai/automation/how-automations-work | 死链 |
| 4 | general_search GitHub Trending（hot/trendshift/ranking 多源） | OK（security-audit-skill/archify/video-use） |
| 5 | deepseek-plugin.org/about | fetch error（死链，累计第 7 次） |
| 6 | blog.n8n.io llm-memory（3892 全） | OK（context rot/Agentic RAG 可观测/relevance drift） |
| 7 | docs.pipedream.com/connect/security/ | 死链 |
| 8 | docs.langflow.org/overview | 死链 |
| 9 | make.com/en/help/functions | 空页（仅导航目录，无实质内容） |
| 10 | activepieces.com/docs/getting-started/overview | 死链 |

## 独点（4 个）
### Z1：Anthropic hooks 第三段：PreToolUse 四决策与 defer 机制与 updatedToolOutput 与权限规则注入（来源：docs.anthropic.com hooks 17983+ 段 2026-09-25，r207-A/B 的续读增量）
- **PreToolUse permissionDecision 四值**（在 hookSpecificOutput 内，非顶层 decision）：`allow` 跳过权限提示 / `deny` 阻止 / `ask` 提示用户确认 / `defer` 优雅退出稍后恢复；多 hook 不同决策优先级 **deny>defer>ask>allow**；**deny/ask 规则无论 hook 返回什么都会评估**——hook 的 allow 不能覆盖 deny 规则。
- **updatedInput 执行前改参**：替换整个 input 对象（未改字段一起带上）；配 allow=自动批准，配 ask=展示修改后输入。
- **defer 机制（v2.1.89+）**：Claude Code 作为子进程运行（Agent SDK/自定义 UI）时暂停工具调用→进程以 `stop_reason: "tool_deferred"` 退出+`deferred_tool_use`（id/name/input 保留在 transcript）→调用方自己 UI 收集输入→`claude -p --resume <session-id>` 恢复→同一工具再触发 PreToolUse→hook 返回 allow+updatedInput（如 AskUserQuestion 的 answers 对象）→工具执行。**无超时无重试限制**（30 天 cleanupPeriodDays 默认保留）；defer 只在**单工具调用**时有效（多工具批里被忽略）；恢复时 MCP server 未连接→`tool_deferred_unavailable` 且 is_error。
- **AskUserQuestion/ExitPlanMode 非交互解阻塞**：`-p` 模式这两工具会 block；hook 返回 allow+updatedInput（echo 原 questions+answers 映射）即可程序化完成——集成 SDK 场景的标准解法。
- **PostToolUse updatedToolOutput 改写工具输出**（值必须匹配工具输出 shape）——hook 层可净化/改写工具结果；`duration_ms` 排除权限提示与 PreToolUse 时间（真实执行耗时）。
- **PermissionRequest updatedPermissions 规则注入**：addRules/replaceRules/removeRules/setMode/addDirectories/removeDirectories 六类条目，destination=session（内存）/localSettings/projectSettings/userSettings 四档持久化；hook 可 echo permission_suggestions=替用户选 always allow；**setMode bypassPermissions 只在会话已启用 bypass 时生效，且永不持久化为 defaultMode**。
- **Agent 子代理 telemetry**：PostToolUse tool_response 带 totalTokens/totalDurationMs/totalToolUseCount/usage（input/output/cache_creation/cache_read）——**per-subagent 成本记账**；run_in_background=true 时返回 async_launched+outputFile 无 usage。
- 判据：**集成 SDK 用 defer 流而非轮询**；hook 改工具输入用 updatedInput（整对象替换）；权限规则注入明确 destination 持久化档位。
- **提升层**：工具 / 工作流。

### Z2：n8n llm-memory：context rot 中心忽视与 Agentic RAG 可观测性与 relevance drift 反馈环（来源：blog.n8n.io llm-memory 2026-09-25，r205-B S1 CoALA 框架的实现层失效模式增量）
- **context rot 机制**：Transformer 模型**忽略密集提示的中心内容，优先开头结尾**——长任务 agent 丢核心需求却还记得问候语；缓解=**定期压缩旧对话成简洁状态摘要，关键元数据放模型高召回区**。
- **episodic 记忆膨胀**：跨会话记忆（session ID 检索总结日志/用户画像）没有总结或遗忘策略→历史变成膨胀的混乱拖慢每次响应。
- **三拓扑取舍**：RAG（线性管线，chunk 太小丢上下文、太大超 token 预算；需管 chunking/embedding/检索延迟）；**Agentic RAG**（检索交给 LLM 用工具决定是否搜/搜哪/怎么 refine；多源复杂研究更灵活，但**非确定性检索路径更难调试、成本更高**；n8n 执行视图可见每一步——哪个工具/什么 query/返回什么/是否再搜）；GraphRAG（知识图谱遍历，适合高度互联数据，LLM 提实体关系贵）。
- **top-k 语义相似≠相关**：大规模下检索拉入共享关键词但缺上下文的噪声 chunk→distract 模型+撑爆 token；缓解=**hybrid dense+sparse 向量+re-ranker 评分后进上下文**。
- **agentic loops relevance drift**：agent 自己生成搜索 query 时，单次近失配检索→用噪声信息指导下一搜→**错误反馈环越搜越偏**；缓解=supervisor 节点或 **relevance guardrail（置信度低于阈值强制 query reset 或向用户澄清）**。
- 判据：**长任务定期压缩+关键信息前置**；检索路径必须可观测可诊断；agent 自搜要加相关性护栏防反馈环。
- **提升层**：工作流。

### Z3：skillsmp p28：审计勾稽算术代码化与 no-negative-echo 交付残留纪律与引用幻觉门控（来源：skillsmp.com/skills/page/28 2026-09-25，与 r204-C U3 对抗验收补洞互补）
- **audit-report-checker（审计勾稽）**：财务报表+附注勾稽/加总/格式检查；**算术 100% 走代码计算，AI 只负责语义定位与结构判断**——50-150 页合体大报告也撑得住；输出 7 sheet Excel+Markdown 复核报告。
- **no-negative-echo**：finalize 产物时**不把被拒绝/放弃的会话内备选方案 echo 进标签、元数据、commit、PR、交接文档**——"此地无银三百两"式残留会让未来的读者误以为曾考虑过那条路；不是普通删除/弃用/迁移的许可。
- **scipilot-cite-skill（引用检索）**：Semantic Scholar/OpenAlex/Crossref **三源并行检索真实文献**，DOI+多源交叉验证真实性；**Gate 8 末端幻觉门控审计，FAIL 即拒绝交付**；Stage 0 必须主动询问篇数/格式/年限/章节/分区等偏好，**禁止默默用默认值**。
- **ponytail-audit**：whole-repo over-engineering 审计（非 diff）：排名列表（删/简化/换 stdlib 原生），one-shot report 不改代码——与现有 ponytail 套件互补（diff vs whole-repo）。
- 判据：**数字核对全走代码，AI 只定位结构**；交付不留被拒方案的痕迹；引用交付前必过幻觉门控。
- **提升层**：可复用 Skill。

### Z4：GitHub Trending：cloudflare 安全审计技能与 archify 可验证图表与生态新仓库（来源：general_search GitHub Trending 多源 2026-09-25，r206-A U4 的增量监控）
- **cloudflare/security-audit-skill**（2026-09-19 热榜第一）：coding-agent 技能，**多阶段安全审计、独立验证、机器可读 findings**——审计结论带可验证证据，与"只报告实际能证明的"同纪律。
- **tt-a1i/archify**（55,857★）：agent skill 生成**可验证的架构/工作流/时序/数据流/生命周期图**——self-contained HTML，带 motion 与 crisp export。
- **browser-use/video-use**（2026 新上榜）：用 coding agents 编辑视频（agent 化视频编辑）。
- **Tencent/BrowserSkill** 上榜（生态事实：腾讯浏览器技能开源）；**mastra**（28,256★ TypeScript agent 框架）、**crush**（Go agentic coding）同榜。
- **hermes-agent**（248,528★，NousResearch）：The agent that grows with you——one-three-one-rule（1-3-1 决策简报：一个问题/三个选项/一个选择）出自其技能库。
- 判据：**安全类技能要机器可读可验证 findings**；图表类产物 self-contained HTML 可离线展示。
- **提升层**：可复用 Skill / 工具。

## 判重说明
- Z1 → r207-A/B 同源续读增量（四决策/defer/updatedToolOutput/权限注入/子代理 telemetry），落。
- Z2 → r205-B S1（CoALA 分类框架）的实现层失效模式增量（context rot 中心忽视/hybrid+rerank/relevance drift 护栏），落。
- Z3 → r204-C U3 互补页（勾稽代码化/交付残留纪律/引用门控），落。
- Z4 → r206-A U4（GitHub agent 生态）增量监控（security-audit-skill/archify/video-use），落。
- 未落：make functions（空页）、activepieces/pipedream-security/langflow-overview/openclaw（死链）、deepseek（第 7 次失败）、superpowers/hermes 排名（与 r206-A 重复）。
