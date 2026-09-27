# r250-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（混合检索/重排面） | ✓ | 重排序放检索最后阶段（合并排序不同检索系统结果；百万文档相关性计算低效需前置检索）；Hybrid Search（dense vector cosine 语义相似+sparse/BM25 keyword 精确匹配产品码/名称/术语；融合后 Rerank 第三方模型重打分重排）；Rerank Model 默认禁用（需先配 API key；多模态 embedding 配多模态 rerank）；Weighted Score 仅当所有知识库 High Quality 模式索引可用；Top K 控制（K 小起步防噪声/阈值适中/必要时重排取上澄）；Metadata Filtering（标签/分类过滤检索对象）；检索策略代码实现（SEMANTIC_SEARCH/FULL_TEXT_SEARCH/HYBRID_SEARCH/KEYWORD_SEARCH Jieba BM25） |
| 2 | n8n（AI agent 新形态面） | ✓ | n8n Agents 新形态（2026-09-25：AI Agent 节点定义在单 workflow；新 Agent 定义一次 own builder+own memory+project home；Workflow 用 Message an Agent 节点发消息；同一 agent 同时答 Slack+跑 schedule+服务其他 workflow）；Human Oversight Playbook（Inline Chat Approval：Chat node 两操作 Send a message…）；Think-Plan-Act 模板（THINK 结构化推理 goal/subgoals/tools/assumptions→ACT 逐步执行）；ReAct 并入 Tools Agent（standalone ReAct Agent deprecated；Tools Agent 已含 ReAct 原则；现代 LLM 直接支持）；AI Assistant（workflow-building agent 内建 2.29.9 Preview：自然语言建/测/修 workflow，产物是标准 n8n workflow）；Multi-agent（AI Agent Tool 把第二 agent 配置成 tool；orchestrator 拥有 tools 其中工具本身是完整配置的 agent）；Bedrock AgentCore harness（GA：持久 memory/real tools/任意模型；社区节点进视觉编辑器）；多会话 chat agent（Data Table memory 按 session_id 加载/更新；sliding window 10 turns） |
| 3 | LangFlow（检索评测面） | ✓ | PLAID 多向量检索评测（text 单向量 top-100+multi-vector rerank 90.7 vs multi-vector via PLAID 94.7；image 单向量 22.6 vs top-100+rerank 56.6 vs PLAID 89.7——多向量对图像检索增益巨大）；Langflow 1.11.0 Multi-Vector Retrieval NextPlaid；LLM-as-a-judge（Langfuse self-host：Score Value 0.94+Score Comment 理由）；评测方法论（Future AGI：define rubric/test set 100-500 cases/faithfulness+instruction-following+task-specific evaluators）；Data Quality Validator 模板（业务规则校验数据集/隔离坏记录 syntax/logic/decimal precision；quarantine pipelines 带原因；Batch Run 组件注入时间上下文解析 JSON；汇总指标 failure rates by rule/top error types）；性能基准（简单 flow 200-500ms/复杂多 agent 2-5s/自托管并发 50-100） |
| 4 | Activepieces（code/custom piece 面） | ✓ | Code 步骤（JS/TS 直接插入 workflow 处理复杂逻辑/数据转换；npm 包支持；prebuilt 集成没有的功能）；Custom pieces（packages/pieces/custom/ 私有集成：实例私有/专有集成/内部 API；与 community pieces 同框架）；TypeScript SDK（createAction/createPiece/PieceAuth；框架从 typed props 生成 UI）；MCP tools（读 CODE step 完整源码/package.json/input mappings 调试）；100+ pieces 开源（MIT、10K stars、self-hosted 无限 flows） |
| 5 | Make（调度/时区面） | ✓ | Make 用组织时区设置场景执行时间（Profile→Time zone options→Scenarios→My organization）；once/every day/自定义；cron 时区教训（服务器 UTC 但以为本地 9AM 实际 3:30AM IST；CRON_TZ 变量；K8s/EventBridge/GitHub Actions UTC 专属）；DST 悖论（Spring Forward 2:00-3:00 小时不存在任务跳过）；Overlap 风险（job 运行超时 vs 间隔多实例并行）；Versely（表达式错=bug，重写 cron 重新 schedule_workflow 重算 next_run_at，不编辑数据库行） |
| 6 | Pipedream（Connect SDK 面） | ✓ | Connect SDK（@pipedream/sdk；前端 PipedreamClient 处理连接流程；服务端 SDK 检索账户/代用户调用 workflow）；Managed auth（3,000+ APIs；托管 OAuth clients/secure token storage/自动 refresh；用户连接秒级永不碰凭证；credentials encrypted at rest 按 project scope）；Connect Link（托管连接流 UI 不用自己建；BYO OAuth clients）；MCP server（10,000+ tools 给 AI agent）；免费至 1,000 connected accounts（2,400+/3,000+ APIs） |
| 7 | Claude Code（security 面） | ✓ | Sandboxed bash tool（filesystem+network isolation；/sandbox 定义自主工作边界；减少权限提示）；Working directory boundary（Manual 模式只能写启动文件夹及子文件夹；不能改父目录无显式权限；可读外部文件）；OS-level sandbox（macOS Seatbelt/Linux bubblewrap；reads allowed/writes workspace/network denied default；84% 权限提示减少；开源 runtime 可审计）；--dangerously-skip-permissions 限制（root/sudo 拒绝启动；仅隔离环境容器/VM/dev container 无网；Cloud sessions 不 honor）；Web search summarization（搜索结果摘要化而非原始内容进上下文——降低恶意网页 prompt injection）；五部分安全模型（permissions/tool access/MCP permissions/sandboxing/auditability 层叠） |
| 8 | OpenClaw（plugins 面） | ✓ | 插件开发者分层（Plugin Developers TS/JS 深度扩展：自带 skills/加 tool providers/改 Gateway 行为；Integration Specialists 接外部系统）；defineToolPlugin SDK（2026.5.18：定义工具契约/build/validate/ship 带 manifest 元数据；openclaw plugins build）；2026.3.22 breaking plugin overhaul（before_prompt_build hook 注入 ClawHub skills 动态上下文；SSH/browser 会话更严沙箱）；Context engine plugin interface；External Secrets Management（openclaw secrets workflow audit/configure/apply/reload）；/subagents spawn 确定性子 agent；Policy Plugin（conformance checks/linting/auto-repair） |
| 9 | GitHub Copilot（custom agents 面） | ✓ | Custom agents（.agent.md 文件放 .github/agents/ 目录；YAML frontmatter+Markdown 指令；定义 prompts/tools/MCP servers；agent profiles）；与 instructions/skills 区别（instructions 被动应用；skills 处理单个任务；agents 定义完整工作风格——整个会话怎么思考/用什么工具/怎么沟通）；Copilot CLI /agent slash command 选择；repo-level 只适用所在 repo；Copilot cloud agent 付费计划全部仓库可用；Agent HQ（Claude/Codex 可选 agent；automated first-pass review；metrics dashboard public preview 追踪；audit logging） |
| 10 | WaytoAGI（提示词/Agent 面） | ✓ | 提示词最简化原则（不含作者/版本信息；注意分类正确避免相似目标困惑——"提供改进建议及原因" vs "评分 1-10" 易混淆，放达成目标后）；样例驱动渐进式引导法（一泽 Eze：利用 AI 高效设计提示词生成预期内容）；Coze 工作流万字实践（开场白引导；AI 精读专家智能体复刻公众号创作力）；Agent 学习路径（00.Agent 共学快闪：从下往上看逐个视频）；角色提示具体化（别只写"你是专家"：场景+目标+输出偏好）；2026 提示词新范式（从"指挥 AI"到"委托 AI"：目标+成功标准+约束+"请自主规划最优处理方案并执行，如有不确定先说明再执行"）；AI Agent 定义（LLM 大脑+工具手脚+记忆+规划循环） |

## 判重基准
双键检索（相对 r224-r249 已落章节）：Dify（r224 知识库/r244 检索模式三选——混合检索 dense+BM25+Rerank 重排/元数据过滤/Weighted Score 为独有增量）；n8n（r226 Agents/r248-B Agents 复用多 agent 委托——"Agent 定义一次用到处"own builder+Message an Agent 节点+ReAct 并入 Tools Agent+AI Assistant 为独有增量）；LangFlow（r248-B lfx 验证链——PLAID 多向量检索评测数据/LLM-as-a-judge Langfuse 实操/数据质量校验模板为独有新面）；Claude Code（r249-A hooks——sandboxed bash/OS 级沙箱 84%/web search 摘要化防注入/权限模式边界为独有新面）；Copilot（r248-B 定制三层/r248-C code review 双路径——custom agents .agent.md 完整工作风格与 instructions/skills 三区分为独有增量）。未选素材：Activepieces code/custom pieces（与 r249-B Pipedream 组件生态重叠高）；Make 调度时区（cron 时区/DST 为通用常识性增量）；Pipedream Connect SDK（r249-B 已覆盖核心）；OpenClaw plugins（r244 defineToolPlugin 契约已落）；WaytoAGI 提示词（与用户已固化工程化指令偏好重叠）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① 混合检索重排纪律 | hybrid 检索+Rerank 重排+元数据过滤 | 工作流 | wb-execute-discipline |
| ② n8n Agent 一等实体 | 定义一次用到处+ReAct 并入+AI Assistant | 工具/工作流 | wb-execute-discipline |
| ③ 多向量检索评测 | PLAID 图像增益+LLM-as-a-judge | 可复用 Skill | wb-execute-discipline |
| ④ Claude Code 安全模型 | sandbox 隔离+权限边界+搜索摘要化 | 工具 | wb-execute-discipline |
| ⑤ Copilot custom agents | .agent.md 完整工作风格 | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
