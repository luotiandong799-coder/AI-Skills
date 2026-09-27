# r264A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（知识库 chunking 面） | ✓ | **Advanced Markdown Chunker 插件**：max_chunk_size 默认 4096/chunk_overlap 200/**adaptive 规则=max(实际)=min(overlap, chunk×0.35)**/strategy auto/code_aware/list_aware/structural/fallback；官方知识管线编排：Maximum Chunk Length 超限强制分段/Chunk Overlap 提升召回/Child Delimiter+Child Max+**Parent Mode=Paragraph 或 Full Document**；推荐值：通用文档 500-800、技术文档 800-1200；overlap 建议分段 10-25%；默认 500 tokens 上限 4000；**600 tokens+100 overlap 为多数文档理想值** |
| 2 | n8n（表达式面） | ✓ | **$now/$today 语义差异**：now=当前完整时间戳 Luxon 对象，today=向下取整到日（hour/min/sec 归零）；**节点间日期以字符串传递需 parse**；DateTime.diffTo(other, unit) 自定义函数；Date & Time 节点五操作（Extract Part/Format/Get Current/Get Time Between）；**$now 用工作流时区**（可在 workflow settings 改）；表达式=inline JS |
| 3 | LangFlow（调试面） | ✓ | Playground 实时测试：与 flow 对话/查看修改 memories/监控 agent tool calls 输出；**按 session ID 查看 Message Log**；**Inspect output 单组件输出排查**（数据丢失/格式错定位）；1.8 起 **traces**（spans+latency+token usage）+Inspection panel 实时检查组件内部状态/输入/输出；需 Chat Input 或 Output 组件才可开 |
| 4 | Activepieces（AI Copilot 面） | ✓ | **AI-first 一体化**（agents/chat/flows/tables/760+ apps）；**Agents 页一句话建 agent**（写"summarise my unread emails every morning"→draft agent 名+instructions+工具）；**agent=可命名/对话/复用的一等实体**（不再是 flow step 配置包）；**Copilot 内建 builder**：自然语言描述→建议步骤/完整 workflow；flow 断了 Copilot 帮定位；agent 工具=app action/自有 automation/MCP server/上传文件；provider 一次配置用自己 key；Human Review 审批点 |
| 5 | Make（嵌套决策面） | ✓ | **Nested if-else and Merge 已可用（2026-09 新）**：一个 scenario 内多级决策，if else 内嵌 if else，不用散到多条 router 链；**合并相关分支同处一图**便于 review 追踪；场景成本优化（Dre Dyson）：**源头过滤**（别拉 1000 条过 20 模块最后丢 950）；**禁用未用 router 路由**（不活跃路由执行仍被评估耗 operations，每月审计）；**Sleep 模块代替高频轮询**省 operations；AI 场景拆分小调用（extract JSON/classify/response draft 各一调用更简单更省） |
| 6 | Pipedream（GitHub Sync 面） | ✓ | **GitHub Sync 双向同步**：Pipedream 改→push GitHub；本地改→push GitHub→deploy Pipedream；branches/diffs/PRs；GitHub 触发源（New Commit/Workflow Run Completed Instant/Project Item Status Changed/issue opened）；Schedule trigger（Every/Cron）；**components=triggers+actions 自包含可执行单元**（源码公开）；SDK 3000+ APIs OAuth/key 一键；**REST API/私有 SSE 流消费事件源** |
| 7 | Claude Code（权限模式面） | ✓ | **Plan mode**：只读工具照常，文件编辑**永不 auto-approve**（即使 allow rule 匹配也走 canUseTool 回调）；四类权限模式（default/accept edits on/plan mode on/dontAsk——**dontAsk 读写全自动但不跳过安全检查**，未授权操作静默拒绝）；**blockReadsOutsideWorkingDirectories 持久化**（用户设置跨会话跨模式生效）；**内置 read-only bash 命令集**（ls/cat/head/tail/grep/find/wc/diff/stat/du/cd/read-only git）不可配置，要提示需加 ask/deny 规则；**auto mode**（Anthropic engineering）：固定 allowlist 只含不可改状态工具，**进入时丢弃已知授予任意代码执行的规则**（blanket shell/wildcarded 解释器/包管理器 run） |
| 8 | GitHub Models（退役面） | ✓ | **2026-07-30 完全退役**（playground/model catalog/inference API/BYOK 全不可用）——信源健康度：GitHub Models 已死，替代=Azure AI Foundry（VS Code BYOK）；Copilot 模型对比（GPT-5 mini 默认/Claude Sonnet 4.6）+**evaluation models 警告**（安全类提示词可能表现更差，需人审） |
| 9 | OpenClaw（任务队列面） | ✓ | durable subagent completion handoffs **30 分钟带封顶指数退避重试**；queued handoff 未确认交付前不算 delivered；delivery 失败→blocked 终态+**保留 canonical result 7 天**；`openclaw tasks retry`=fenced 新交付代/`tasks dismiss`=记录有意不交付；cron recurring 失败**退避阶梯 30s/1m/5m/15m/60m**成功重置；one-shot 终态后禁用；**LiveSessionModelSwitchError**：持久化切换的 provider/model 再重试，外循环限 2 次后中止；**Telegram long-polling ~8 分钟静默死**（issue #7526）需显式 retry policy 自愈；**transient vs permanent 分类**（rate limit/provider overload/network/server/Cloudflare=transient 重试；auth/config/validation=permanent 不重试） |
| 10 | deeplearning.ai（课程生态面） | ✓ | **Agentic AI 课程**（9h55m 模块式：Reflection Design Pattern/改善 SQL 生成/Module3 tool use：creating tool/tool syntax/code execution/MCP/Email Assistant Workflow）；**评测驱动**：Arize Evaluating AI Agents 2h36m structured assessments、DSPy Build and Optimize Agentic Apps 59m；crewAI 多智能体（2h49m 规划/估算/分配；12h58m tools/MCP/no-code agent）；smolagents 54m；Gemini CLI 1h23m；Agentic Knowledge Graph Construction（Neo4j 3h18m） |

## 判重基准
双键检索：Dify chunking 参数（§6411 RAG 分块选型树 r263B 已落策略选型——Dify 平台参数/插件 adaptive 为独有增量合并）；Make 嵌套 if-else+场景成本（§6160 错误处理为另一面——新面）；Claude Code Plan/auto mode（§r263A 插件作用域/§r258C 安全模型——Plan mode 编辑永不批准/auto mode 丢弃任意代码执行为增量合并）；OpenClaw 任务队列（§2732 重试硬顶/§6244 session 治理——handoff 30min/blocked 7 天/tasks retry/退避阶梯/transient 分类为增量合并）；Pipedream GitHub Sync（§6129 错误处理为另一面/§r254A CLI——双向同步新面）。备选并入记录：n8n Luxon 表达式（§r249A 表达式安全写法——$now/$today 语义增量）、LangFlow Playground（§r258A 可观测——调试面增量）、Activepieces Copilot（§r255A AI——一句话建 agent 增量）、GitHub Models 退役（信源健康度记录，不进技能）。

## 独点落地（5 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r264A-1 | wb-execute-discipline | 3.20.0+ | Dify 知识库 chunking 参数与插件 adaptive 规则 | 工作流 |
| r264A-2 | wb-execute-discipline | 3.20.0+ | Make 嵌套决策与场景成本优化 | 工作流 |
| r264A-3 | wb-execute-discipline | 3.20.0+ | Claude Code Plan/auto mode 权限安全 | 工具 |
| r264A-4 | wb-execute-discipline | 3.20.0+ | OpenClaw 任务队列与重试语义 | 工作流 |
| r264A-5 | wb-execute-discipline | 3.20.0+ | Pipedream GitHub Sync 双向同步 | 工具 |

## 复核
五独点均有当日实拉来源（逐站 URL 见各站摘要）；r264A-1/3/4 按增量判定合并保留增量；r264A-2/5 新面；备选并入记录不单独落地；GitHub Models 退役记入信源健康度（2026-07-30 已死，后续不再拉该面）。垃圾：本轮未产生临时文件。
