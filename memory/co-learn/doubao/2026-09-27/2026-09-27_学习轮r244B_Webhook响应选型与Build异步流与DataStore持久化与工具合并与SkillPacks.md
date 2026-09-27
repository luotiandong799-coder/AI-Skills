# r244-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（插件/市场面） | ✓ | Marketplace 插件生态（Discover. Extend. Build；trending/popular Excel Analysis/Self-Refine Agent Strategy/Hermes Agent Chat；verified by Dify partner/certified badge；社区+Cloud 双版本；自动更新）；插件开发→发布链（dify plugin package ./slack_bot 打包→提交 Marketplace 仓库→approved 合并 main branch→pipeline 发布）；安装方式（Marketplace 一键/GitHub 仓库地址选版本装包）；插件双类型（Model Plugin：LLM/embedding/rerank vs Tool Plugin：图像生成等）；MCP Compatible Dify Tools |
| 2 | n8n（Webhook/响应面） | ✓ | Webhook 响应四形态（All Entries 数组/First Entry JSON/First Entry Binary 二进制/No Response Body）；默认响应模式 When Last Node Finishes（同步短工作流几秒完成）；慢工作流陷阱（40 秒 workflow 连接被调用方/反向代理超时切断即使 run 完成）；Respond to Webhook 节点（响应重要时 hand control 到独立节点立即回响应再继续处理）；Streaming response（Webhook Response Mode Streaming+AI Agent Enable Streaming ON）；Wait 节点 Webhook Suffix（多 Wait 节点唯一 resume URL） |
| 3 | LangFlow（API/流式面） | ✓ | Workflow API 流式（mode: stream 开 SSE；stream_protocol 两选 langflow EventManager 默认帧/agui AG-UI 客户端；sequence_id 从特定点恢复流）；Build 异步（/build 返回 job_id→/build/$JOB_ID/events 流式执行结果）；A2A server（message/stream SSE JSON-RPC 帧）；OpenAI Responses API 兼容（stream true 逐 chunk）；TypeScript client（client.flow(id).stream(input) ReadableStream） |
| 4 | Activepieces（模板/市场面） | ✓ | 模板库（curated template library 按部门 HR/Finance/Marketing/Sales/Operations；Pick→Customize→Test→Go live 四步）；700 integrations（dev/staging 环境免费；self-host free forever；custom pieces TypeScript 同 SDK；AI agents/MCP servers/human approvals in the box）；Human Approval Steps（workflow 暂停等人工审查 seller listings/dispute，批准/拒绝后自动恢复） |
| 5 | Make（Data Store/变量面） | ✓ | Data Store 持久化（跨 scenario runs 持久；Get a Record/Search records/Add a record）；checkpoint/cursor 模式（多步 email 序列/分页导出记 export_cursor 恢复位置）；AI 响应缓存（hash 查询→text similarity>90% 返回缓存→7-day TTL；FAQ 30-40% 命中率）；变量 scope（SetVariables scope: roundtrip 跨多次执行周期；与 webhook trigger 多 routes/branching 组合会混淆）；Scenario Builder 可见性（直接显示 context 在哪捕获/传递/写入/丢失） |
| 6 | Pipedream（Connect/OAuth 面） | ✓ | Managed Auth（3000+ APIs；hosted OAuth clients/secure token storage/automatic refresh；用户连接账户你永不碰 credential）；Connect Link/Client SDK（托管连接流；bring your own OAuth clients）；credentials encrypted at rest scoped per project；MCP server（给 AI agent 10000+ tools）；自定义 OAuth client 要求（end users 用 OAuth app Google Drive/Slack/Notion 必须自带 custom OAuth clients 注册后加 oauthAppId）；Connect token 一次性有效会过期 |
| 7 | Anthropic（Tool use 面） | ✓ | 工具合并（create_pr/review_pr/merge_pr 合成单工具带 action 参数——减少选择歧义）；Schema 质量是工具可靠性最大预测器（模型按名称/描述/参数文档选工具，两工具听起来像就选错且失败不可见直到用户抱怨）；input_examples（复杂输入/嵌套对象/格式敏感参数提供 schema 验证过的示例）；Programmatic tool calling（小固定开销容器启动/脚本生成换 tool-result tokens 与 round-trips 大节省；强适合 fan-out 并行 50 端点/20 记录、大工具结果先过滤聚合总结再进 context、agentic search 迭代查询）；tool_choice auto（默认判断，答案已在 context 直接回答） |
| 8 | skills.sh（创建/贡献面） | ✓ | 安装渠道（npx skills add owner/repo 无 registry 账户；CLI 声称 70+ 兼容 agents 20+ tracked）；Leaderboard（按安装数 telemetry 排名，安装即自动纳入）；Skill Packs（多技能捆一个 pack，skills.sh/p/<pack-id> URL 分发）；多目录结构（根 SKILL.md/skills//skills/.curated//skills/.experimental/，单仓库多技能 CLI 自动扫描）；skill-architect（贡献必须用它引导质量） |
| 9 | OpenClaw（记忆/会话管理面） | ✓ | 记忆三文件（MEMORY.md 长期 load 在 session 开始；memory/YYYY-MM-DD.md 每日；memory_search semantic/memory_get exact excerpt）；Plugin hooks session 生命周期（session_start/session_end，reason 枚举 new/reset/idle/daily/compaction/deleted/shutdown/restart/unknown；shutdown/restart 由 Gateway finalizer 触发进程停止/重启时完成 phantom records；finalizer 时间有限慢插件不能阻塞 SIGTERM/SIGINT）；Mem0 插件 skills mode（agent 控制记什么 triage/怎么回忆 recall/周期清理 dream；run_id 会话级短期 vs memory_add 长期）；原生记忆插件三层（Context Tree/Workspace Memory/Daily Memory Git-like 版本） |
| 10 | GitHub（生态面） | ✓ | Agent Skills 生态爆发（2026 第 35 周 AI/Agent 占比超 45%，MCP 工具热度环比+30% 标准化集成阶段）；ponytail 132.1k★（think like the laziest senior dev）/humanizer 45.4k★（去 AI 味）/hyperframes 47.7k★（视频）；stablyai/orca（ADE agent development environment 桌面/移动/远程并行 agent fleets +944）；BuilderIO/agent-native（agentic apps 框架）；siyuan 46.5k★（隐私优先自托管知识工作空间人与 agent 协作）；LibreChat 45k★（Agents/MCP/Skills 多模型）；官方 MCP Registry v2.0.1 |

## 判重基准
双键检索（相对 r241-r244A 已落章节）：Dify（r244-A 落四形态发布/r243-B 落插件治理——"插件市场发布链+双类型"独有增量深化）；n8n（r243-C 落 payload 归一化/r244-A 落 parser——"Webhook 响应四形态选型+Respond to Webhook 防超时"独有增量新面）；LangFlow（r242-B 落 Flow API v2 流式/r244-A 落 Extension——"build 异步 job 事件流+A2A server"独有增量深化）；Activepieces（r243-B 落 worker/r244-A 落 AI piece——"模板库四步+700 integrations"增量较弱暂缓）；Make（r243-B 落触发/r243-C 落 IML/r244-A 落 AI Toolkit——"Data Store checkpoint+cache"独有增量新面）；Pipedream（r243-B 落组件开发/r244-A 落 AI code gen——"Managed Auth 托管认证+自带 client"独有增量深化）；Anthropic（r242-A 落工具调用/r243-C 落工具点名/r244-A 落 hooks——"工具合并+input_examples+programmatic calling"独有增量深化）；skills.sh（r242-B 落 frontmatter/r243-B 落 skills.json——"Skill Packs+多目录结构"独有增量新面）；openclaw（r243-C 落会话记忆/r244-A 落 cron 隔离——"session hooks+Mem0 skills mode 三职能"独有增量深化）；GitHub（r243 落 agentmemory/r244-A 落多模型编排——"ADE+Agent Skills 爆发信号"独有增量新面）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① n8n Webhook 响应选型 | 同步快响应默认 vs Respond to Webhook 防超时 vs streaming | 工作流 | wb-execute-discipline |
| ② LangFlow Build 异步流+A2A | /build job_id→events 流式；message/stream SSE | 工具 | wb-execute-discipline |
| ③ Make Data Store 持久化 | checkpoint/cursor+AI 响应缓存+roundtrip scope 陷阱 | 工作流/工具 | wb-execute-discipline |
| ④ Anthropic 工具合并+Schema | 相关操作合并少选择歧义；input_examples；programmatic calling | 模型/工作流 | wb-execute-discipline |
| ⑤ skills.sh Skill Packs | 多技能捆 pack-id URL；多目录结构自动扫描 | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
