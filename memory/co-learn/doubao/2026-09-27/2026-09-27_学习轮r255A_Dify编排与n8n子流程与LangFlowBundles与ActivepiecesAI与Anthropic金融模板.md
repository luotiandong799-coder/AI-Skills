# r255-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（工作流编排面） | ✓ | Workflow Studio 可视化画布（模型/知识检索/工具/代码/分支/触发器/人工审核）；Runtime Prompt Graph：多阶段推理节点拖拽编排（提问→意图识别→知识库路由→多源融合→合规重写）可版本化 A/B 测试；Execution Graph IR：节点统一抽象为确定性 I/O Schema+显式生命周期事件，DSL 编译器实时生成带版本签名执行图+CLI 触发编译；2026 新功能：并行节点执行/条件分支正则+JSON path/循环节点迭代列表/节点级错误捕获和重试/变量池全局共享；Human Input node（v1.13）：流程暂停+表单发指定人+决策按钮+沿分支继续；New Agent（8.27）：Agent 拆成独立应用可复用资源（模型/Prompt/Skills/文件/工具一处维护），独立运行或 Workflow Agent 节点调用；图片/文档分流（List Operator 拆分，图片走 vision/文档先转文本）；检索参数（count/score threshold/reranking）用代表性问题测试 |
| 2 | n8n（子流程面） | ✓ | Sub-workflow：Execute Workflow node 调另一 workflow；被调方首节点用 Execute Sub-workflow Trigger；用途：复用（多 workflow 拉数据统一调一个生成报表）/大 workflow 拆小（防内存问题）；调试：右键 Open sub-workflow/CTRL+SHIFT+O；LangChain 节点更名：AI Agent 主节点/Chain 序列/AI Memory/Embeddings/Vector Store 子节点挂 AI Agent；搜索：SearchApi community node/Bright Data MCP+n8n-nodes-mcp/Brave MCP+Telegram |
| 3 | LangFlow（bundles 面） | ✓ | lfx-bundles metapackage：opt-in 扩展（Langflow+standalone LFX 均可）：uv pip install "lfx-bundles[<bundle>]"；Agentics 2.0：arXiv 2603.04241 "Logical Transduction Algebra for Agentic Data Workflows"；Code Agents bundle；LangChain bundle（CSV Agent/SQL Agent/LLM Math Chain/Natural Language to SQL/Retrieval QA/Self Query Retriever/JSON Agent/VectorStoreRouterAgent）；1.10 四新 bundle：lfx-arxiv/lfx-docling/lfx-duckduckgo/lfx-ibm；Composio bundle（aggregate Composio Tools 供 agent 当工具）；1.12：OpenTelemetry（service health+flow runs）；Exa bundle（lfx extension list 确认加载）；一次装全部无 Torch opt-in："langflow[bundles]"；CrewAI Sequential Task Agent（role/goal 参数） |
| 4 | Activepieces（AI agent/files/forms 面） | ✓ | AI Agent Builder：进程 inbox 发票；选工具（任意 app action/自己的自动化/MCP server/上传文件给它读）；模型+key（admin 一次配 provider：OpenAI/Anthropic/Gemini/Azure/Bedrock）；审批前置；Hosted Forms：文本/长文本/文件/toggle 字段托管页；Document Processing：AI 解析 PDF/图片→提取结构化字段→normalize 日期金额→JSON 映射下游动作；Tables 存元数据/提取值/状态；减少幻觉：强制结构化输出（JSON schema）+写入前校验/从 curated Tables/APIs 检索事实+引用/来源字段/高影响更新加 review gate；760+ apps；每 piece 可暴露给 Claude/Cursor/Windsurf/MCP client |
| 5 | Make（模板/迁移面） | ✓ | Blueprints：保存/复制共享复用（含模块设置/mapped values）；备份（丢访问/换账号）；策略：high-risk change 前 export blueprint+中央仓库存储+命名约定+scenario description changelog+known-good rollback；import 到未保存 scenario 会覆盖变更（import=部署动作非 casual paste）；Clone scenario：同 team 全复制（webhooks 需重设）/跨 team 需重设 connections；Module Migrator：legacy 模块自动迁移（非所有 app 支持）；Templates：make.com/en/templates 预配置（含免费 tier）；迁移 playbook：数据 parity 验证→cohort 稳定→final cutover（暂停 scenarios→按 waves decommission→监控 webhook 事件量→全 billing cycle 干净后删除） |
| 6 | Pipedream（sources 面） | ✓ | pd.triggers.deploy API：程序化部署 trigger（id/externalUserId/webhookUrl）；10,000+ prebuilt triggers/actions；四类触发：HTTP/Cron/Email/Event sources（app 事件实时流）；Polling source：timer intervalSeconds 配置；默认 15 分钟（registry 全局默认可覆盖）；source 开发：run() 方法 echo body+emit 事件；this.http.respond |
| 7 | Anthropic（金融 agents 面） | ✓ | 10 个 ready-to-run agent templates：pitch book/KYC screening/GL reconciler/month-end closing/credit memo/Earnings Reviewer（读财报 transcript+监管文件更新财务模型+flag 关键变化风险因素）/Statement Auditor（报表一致性完整性审计准备）；部署形态：Claude Cowork/Claude Code plugins+Claude Managed Agents cookbooks（/v1/agents 部署）+vertical plugins（底层 skills/slash commands/data connectors）；三阶段 adoption playbook：foundation→pilot→scale；subagent delegation research preview（headless 多 agent 部署需额外审查）；Claude Opus 4.7 Vals AI Finance Agent benchmark 64.37% |
| 8 | GitHub（AI agent 仓库面） | ✓ | LangGraph ~33K（production standard，Klarna/Cisco/Vizient 生产用）；superpowers 269K（agentic skills framework）；MetaGPT 68.8K；LibreChat 44,962（ChatGPT clone：Agents/MCP/Skills/DeepSeek/Anthropic/OpenAI）；crewai 53.8K；qwen-agent 13.3K；AgentScope 26.9K；casdoor 14,474（Agent-first IAM/LLM MCP & agent gateway：OAuth/OIDC/SAML/WebAuthn）；Maestro（多 AI coding agents 并行桌面指挥中心：Claude Code/Codex/Gemini CLI）；arXiv 2607.02453：808,042 stars/73,997 PR/86,241 commits 分析 15 框架——star 数反映 hype cycles 不可靠 |
| 9 | OpenClaw（automation 面） | ✓ | Automations=内置 scheduler：persists jobs/wakes agent/deliver output 到 chat channel/webhook/nowhere；支持 one-shot reminders/recurring intervals/cron/inbound webhook triggers；openclaw automations CLI（cron 是 alias）；openclaw automations create "时间" --name --session --system-event；Tasks=background task ledger（ACP runs/subagent spawns/isolated automation runs/CLI operations）；cron-mastery skill：>1 min 延迟禁 act:wait 或内部循环→用 cron:add one-shot at；执行精度依赖 Gateway Heartbeat（10-60s tick） |
| 10 | WaytoAGI（教程面） | ✓ | Hermes Agent 接入（API Base URL llm.waytoagi.com/v1）；Agent 共学快闪活动/Coze 学习路径/个人 AI 知识库方案；腾讯云方法论：加约束（权限边界/确认机制/操作日志）；别从全自动开始→先半自动（Agent 干你审，跑顺逐步放权）；多数翻车源于给 Agent 过高自主度；ZyVOP：Week 1 构建 research agent 跑 10 真实查询只观察不修；Week 2 加 RAG 测检索质量调 chunk size 和 k |

## 判重基准
双键检索：Dify（r254-A 插件市场/r254-B 知识库/r254-C 日志——工作流编排引擎面独有）；n8n（r254-A error/r254-B queue/r254-C webhook——子流程模块化面独有）；LangFlow（r254-A lfx 扩展工程/r254-B memory/r254-C API——bundle 生态面增量≥40% 合并）；Activepieces（r254-A webhook/r254-B polling/r254-C MCP——AI agent builder+防幻觉面增量≥40%）；Make（r253 多面/r254-A data store/r254-B webhook/r254-C AI agent——blueprint 迁移策略面新）；Pipedream（r254-A CLI/r254-B MCP/r254-C schedule——sources 部署 API 面新）；Anthropic（r254-A SDK/r254-B hooks/r254-C MCP——金融 agents 模板面新）；GitHub（r253/r254 榜面——生态 star 分析弱增量备选）；OpenClaw（r253-A cron/r254-B memory/r254-C 审批——automation 调度面增量 40% 备选）；WaytoAGI（半自动放权方法论备选）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 工作流引擎增强 | Runtime Prompt Graph+并行/循环/错误捕获+Human Input+New Agent | 工作流 | wb-execute-discipline |
| ② n8n 子工作流模块化 | Execute Workflow+复用/拆分/调试+AI 节点结构 | 工作流 | wb-execute-discipline |
| ③ LangFlow lfx-bundles 生态 | opt-in bundle+一次性安装+OpenTelemetry | 工具 | wb-execute-discipline |
| ④ Activepieces AI Agent 与防幻觉 | JSON schema+写入前校验+review gate+暂停审批 | 工作流 | wb-execute-discipline |
| ⑤ Anthropic 金融 agents 模板 | 10 模板+plugin vs Managed Agent 部署 | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 备选未落：OpenClaw automation 调度/GitHub star 不可靠/WaytoAGI 半自动放权/Pipedream sources API/Make blueprint 迁移。
- 垃圾：本轮未产生临时文件。
