# 学习轮 r303B 十独点（2026-09-29）

批前判重基线：doubao 留痕 2026-09-29 目录 58 条（r284A~r302C + r303A）+ workbuddy 18 条 + SKILL.md 七章（r301A/B/C+r302A/B/C+r303A）。本批十批 × 3 查询 = 30 次信源全量实拉（与 r302A/B/C 86 词、r303A 30 词、r303B 前批查询词全部错开）；无站点打不开、无健康度问题，未删未加信源。每点=来源 URL 清单 + 判重说明 + 提升层 + 触发词。

## 1. Dify RAG 调优顺序与参数带（来源：dify-hosting.com/en/guides/dify-rag/；generative-ai.sejuku.net/blog/16105/；mimilog-news.com/dify-nocode-chatbot-rag-review/；generativeai.tokyo/media/dify-business-automation-rag-guide-2026/；ai-tool-lab.info/dify-knowledge-accuracy-not-improving-fix/；blog.csdn.net/m0_59012280/article/details/163312037；withnext.net/articles/dify-rag-implementation-guide）
- 调优顺序=先检索测试判定"拾取了吗"，再从可回退配置（分数阈值/Top-K/检索方式）小步调，最后才动 chunk 与源材料质量；推荐参数带=chunk 300-500 字符（另一来源 500-800）/overlap 50-100 防上下文切断/Top-k 5-8/分数阈值 0.3-0.4 先松后紧/段落切分优先。
- Markdown 直接导入会碎片化分块、数值无语义标注（180 无法区分价格还是库存）→ 检索极差；CSV 结构化分隔字段语义清晰→准确率大幅提升；全文检索适合型号/固有名/代码精确匹配，混合搜索+rerank 是抑制幻觉的现实设计；生产部署 6 worker 节点。
- 判重：r301C/r302C 检索四件套为组件清单轴，本点=调优方法论+参数带+数据格式轴，重叠约 40% → 落地。
- 提升层：工作流。触发词：Dify RAG、调优顺序、分数阈值、Top-K、CSV 优于 Markdown。

## 2. Activepieces agent 实体化 + 一句话建 agent + MCP 每 app 工具化（来源：activepieces.com/docs/about/changelog；activepieces.com/product/ai-agent-builder；activepieces.com/mcp/webhook；activepieces.com/resources/automation-use-cases/automation-for-ai-agents；activepieces.com/pieces/webhook）
- agent 从"flow 一步里的设置包"变为可命名/简述/对话/复用的实体；一句话建 agent（"每天早上总结未读邮件"→草稿 agent 含名字+指令+所需工具）；agent 触发 webhooks/schedules/events/manual。
- MCP server 每 app 动作成工具、认证一次全 app 复用；approval 步骤暂停等人工检查再恢复下游；Webhook MCP 使 760+ app 工具可被 Claude/Cursor 调用；TypeScript 内联处理最难步骤、其余可视化。
- 判重：r301-r303A 无此轴 → 全新点。
- 提升层：工具。触发词：Activepieces、agent 实体、一句话建 agent、approval 步骤、Webhook MCP。

## 3. Langflow 记忆三态区分 + session ID 默认流级 + Memory 数据类型（来源：docs.langflow.org/memory；docs.langflow.org/memory-bases；docs.langflow.org/message-history；docs.langflow.org/guides-chat-memory；docs.langflow.org/1.8.0/session-id；docs.langflow.org/next/bundles-valkey；docs.langflow.org/1.8.0/bundles-datastax）
- 默认 session ID=flow ID（整个 flow 一个大会话池）；多用户 flow 建议自定义 session ID（如 user ID）隔离各用户上下文；session ID 可跨 flow 共享。
- memory base=向量化长程聊天历史语义检索（区别于 Message History 按时间序取最近、区别于人工填充的知识库）；Agent 组件内置聊天记忆默认启用；Message History 接 Langflow storage 或 Mem0/Redis；Valkey/DataStax Chat Memory 组件以 Memory 数据类型在组件间传递。
- 判重：r302B Langflow 记忆四层为记忆选型轴，本点=session 隔离+组件数据传递轴，重叠约 45% → 落地。
- 提升层：工具。触发词：session ID、memory base、Message History、Memory 数据类型、user ID 隔离。

## 4. Anthropic 官方 skills 仓库结构 + skill-creator 迭代闭环 + managed agents 两到达方式（来源：resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf；deepwiki.com/anthropics/skills/1-overview；localskills.sh/blog/anthropic-skills-explained；platform.claude.com/docs/en/managed-agents/skills.md；mech.app/articles/anthropic-agent-skills-dynamic-loading/）
- anthropics/skills 135K+★；document-skills（docx/pdf/pptx/xlsx）source-available 非 open source、驱动 Claude 生产文档能力；example-skills Apache 2.0。
- skill-creator 内置 Claude.ai/Claude Code：自然语言生成带 frontmatter 的 SKILL.md、审技能（标记常见问题/过欠触发风险/建议测试用例）、迭代改进（把使用后 edge case 带回 skill-creator）。
- 技能=运行时 loader 动态注入专门指令与工具（非 function-calling wrapper）；managed agents 两种到达=skills 数组挂载或 GitHub repo 会话装载（repo 根 .claude/skills 自动发现）。
- 判重：r302A 渐进披露/r302B Copilot skills 绑定 MCP 为不同轴，本点=官方仓库结构+创作闭环轴，重叠约 40% → 落地。
- 提升层：可复用 Skill。触发词：anthropics/skills、document-skills、skill-creator、.claude/skills、迭代闭环。

## 5. MCP Server 安全基线四件套 + T/TAF 352—2026 行业标准 + token delegation（来源：taf.org.cn/upload/AssociationStandard/TTAF 352—2026（MCP Server 安全技术要求）.pdf；learn.microsoft.com/en-ca/azure/foundry/mcp/build-your-own-mcp-server；mcpgee.com/blog/mcp-server-security-guide）
- 远程模式必须客户端鉴别（API 密钥或对称共享密钥）；安全基线=强制认证（除非场景明确需要否则禁匿名）/凭证按 secret 存密钥库（不硬编码不进 git）/下游调用最小权限/记录并监控工具调用。
- OAuth 2.1/OIDC 强制、每次请求校验 iss/aud/exp/签名；token delegation（RFC 8693）在限权同时保留独立服务非人身份（NHI）；access/refresh token 都按 secret 服务端强加密存储。
- 判重：wb-context-compressor MCP 安全为工具面威胁轴，本点=服务端认证基线+行业标准+OAuth 委托轴，重叠约 50% 增量明确 → 落地。
- 提升层：工具。触发词：T/TAF 352、远程 MCP、token delegation、NHI、密钥库。

## 6. skills.sh 发布模型 + gh skill 内容寻址变更检测 + 不可变 release（来源：docs.localskills.sh/cli/；github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/；vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context；raw.githubusercontent.com/witanlabs/witan-cli/HEAD/skills/README.md；cloud.tencent.com/developer/news/3850849）
- skills.sh 无注册提交流程——"发布"=放 git repo+分享 repo+npx skills add 遥测自动 listing；--version 显式 semver 必须大于最高已发布版本（build metadata 不支持）、--patch/--minor/--major 递增、--prerelease [id] 发布但非 installs 解析版本。
- gh skill publish 关联 git tag、可开启不可变 release（发布后内容不可改、管理员也不能）；内容寻址变更检测=每安装技能记录源目录 git tree SHA、update 比较 SHA 非时间戳；--pin <commit> 锁定可复现安装、--verify-signature 验发布者签名（Sigstore/GitHub Attestations）；锁定版本被 update --all 跳过；witan semver 语义=patch typo/minor 内容/major 重构+CHANGELOG Unreleased 条目。
- 判重：r302A skills.sh find-skills 为发现轴，本点=发布/版本/供应链轴，重叠约 35% → 落地。
- 提升层：工具 / 可复用 Skill。触发词：gh skill publish、tree SHA、不可变 release、--pin、--prerelease。

## 7. 多 Agent 编排七模式 + handoff 上下文压缩 + 唯一编排者 + 路由授权双校验（来源：velsof.com/ai-agents/multi-agent-ai-orchestration-patterns/；twilio.com/en-us/blog/insights/ai-agent-orchestration；aiworkflowlab.dev/article/building-multi-agent-ai-systems-2026-architecture-patterns-mcp-production-orchestration；zilionix.com/blog/multi-agent-orchestration-enterprise/；cloud.tencent.com/developer/article/2689451）
- 七模式=Parallel/Supervisor/Handoff/Routing/Pipeline/Hierarchical/Blackboard；handoff 两大生产故障：全量 12K token 上下文传递太贪婪、责任转移语义丢失；supervisor 模式必须唯一编排者——两个 agent 都认为在协调→重复工作/矛盾指令/竞态。
- routing vs supervisor 区别=系统先分类送入口 vs 会话内决定调用谁；授权不得仅依赖 router 模型输出——目的地仍需校验身份/租户/操作、低置信度/新类别需显式 fallback。
- 判重：wb-execute-discipline 多 Agent 协作纪律为拆后协作轴，本点=handoff 上下文压缩+唯一编排者+授权双校验增量，重叠约 55% 增量明确 → 落地。
- 提升层：工作流。触发词：handoff、上下文压缩、唯一编排者、路由授权双校验、七模式。

## 8. n8n Tools Agent 输出解析增强 + LangChain Code 自托管限定 + 工具节点化（来源：docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/tools-agent/；community.n8n.io/t/i-updated-my-n8n-and-cant-find-the-langchain-node/301746；n8n.io/workflows/3820-dynamically-switch-between-llms-for-ai-agents-using-langchain-code/；n8n.io/workflows/3440-track-llm-token-costs-per-customer-using-the-langchain-code-node/）
- Tools Agent 实现 Langchain tool calling 接口（描述工具及其 schema）+增强输出解析保证标准输出格式；LangChain 节点已原生并入 AI 套件（不再单节点）。
- LangChain Code 仅自托管可用：自定义 LLM 初始化/动态切换 LLM（结果不满意回环到下一个 LLM）/token 计费/回调接 Langfuse 追踪；workflow tool+HTTP request tool 让 agent 节点决定何时用哪个工具。
- 判重：r303A n8n queue mode 为并发轴，本点=AI 节点能力轴，重叠约 40% → 落地。
- 提升层：工具。触发词：Tools Agent、LangChain Code、自托管、动态切换 LLM、Langfuse。

## 9. Dify Conversation vs Workflow 变量 + Variable Assigner 持久模式 + LLM Memory node-specific（来源：dify-6c0370d8.mintlify.app/en/learn/key-concepts；dify-6c0370d8-release-1-16-0.mintlify.site/en/cloud/use-dify/nodes/variable-assigner；deepwiki.com/langgenius/dify-docs/4.1-variables-and-data-types；dify.ai/blog/dify-conversation-variables-building-a-simplified-openai-memory；marketplace.dify.ai/plugin/beersoccer/mem0ai）
- Conversation Variables（Chatflow 专属）跨轮持久、会话结束 GC；Workflow 变量每次执行重置；Variable Assigner 写持久数据三模式=渐进清单/智能记忆系统/用户偏好存储。
- LLM 节点 Memory 开关=Chatflow 会话内多轮上下文、node-specific 不跨会话；View cached variables 免重跑整个 workflow 测节点对前序输入的响应；sys.user_id 内置变量；mem0ai 插件 async_mode 默认=写非阻塞读总等待。
- 判重：r302C Dify 输入三件套为输入轴，本点=会话态变量+持久模式轴，重叠约 35% → 落地。
- 提升层：工具。触发词：Conversation Variables、Variable Assigner、node-specific、View cached variables、sys.user_id。

## 10. SWE-bench 评测收敛危机 + scaffold 差异 > 模型差异 + Pro/ProMax 替代（来源：arxiv.org/pdf/2609.17394；codersera.com/blog/ai-agent-benchmarks-state-of-leaderboard-may-2026/；arxiv.org/html/2608.09802v1；arxiv.org/pdf/2606.13995）
- 顶级 coding agents 收敛——同样解决 285/500 实例、同失败 51、解集嵌套 0.935，榜无法排序；scaffold 差异达 29.8pp 超过前三十名差距→测的是 harness 非模型。
- OpenAI 审计发现 SWE-bench Pro ~30% 任务损坏、2026 初停报 Verified（gold-patch 逐字复现）；SWE-bench Pro 抗污染替代、分数低 25-30 点反映真实能力；SWE-Bench ProMax 多语言重构 170 实例 7 语言；Dialogue-SWEBench 对话驱动编码 agent 评测+用户模拟器。
- 判重：r302A/r302C 评测轴均非编码 agent 基准 → 全新点。
- 提升层：模型 / 工作流。触发词：SWE-bench、收敛、scaffold 差异、ProMax、gold-patch。

信源健康度：30 次实拉全部成功返回，无站点连续失败，无需删/加信源。
