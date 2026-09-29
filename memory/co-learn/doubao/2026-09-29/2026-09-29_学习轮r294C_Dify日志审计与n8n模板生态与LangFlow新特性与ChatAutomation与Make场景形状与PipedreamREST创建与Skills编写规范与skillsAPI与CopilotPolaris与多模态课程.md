# r294C 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r294B 全表。查询词与既往全错开（本轮=监控日志/模板市场/新版本特性/模板/场景设计/工作流示例/Skills编写/教程API/新AI项目/多模态课程）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | 2026 日志审计体系（OpenTelemetry 结构化 JSON+TraceID+实时告警）/ SLS 存储切换插件（控制台体验不变）/ XXL-JOB 节点级下钻（执行历史+调度事件+节点追踪）/ 节点级错误策略（继续/记录日志/切替代路径+通用错误处理器） | 合并保留增量（r292B OTel，本点=SLS+XXL-JOB+节点错误策略） | 工具 |
| 2 | n8n | 官方模板库 11,741 个（2026-08，75%+ 含 LLM 集成，8,300→10,700→11,741 增长）/ 第三方付费市场（n8nmarkets 2,000+、垂直行业包 $9-$200+） | 合并保留增量（r293A 模板库，本点=n8n 规模+付费模式） | 工作流 |
| 3 | LangFlow | 1.11 HITL 门控工具评审+A2A 协议+AG-UI 流式 Workflow API / 1.12 OpenTelemetry / Python Interpreter microVM sandbox（LANGFLOW_SANDBOX_BACKEND=exec-sandbox） | 合并保留增量（r292B/r293C，本点=1.11/1.12+microVM） | 工具 |
| 4 | Activepieces | Chat-to-automation builder（自然语言直接建 flow）/ 400+ MCP Servers（2026-06）/ Railway 一键部署（App+PostgreSQL+Redis+SSL） | 合并保留增量（r293A 模板，本点=chat-to-automation+400MCP） | 工作流 |
| 5 | Make | 四阶段场景形状（Trigger→Modules→Filter/Router→Action）/ 生产最佳实践（命名前缀/Notes 内联文档/子场景 webhook 模块化/幂等设计）/ Make Grid 依赖映射 / ChatGPT 官方 plugin（2026-09） | 合并保留增量（r293A/r293C，本点=四阶段+Grid+幂等） | 工作流 |
| 6 | Pipedream | REST API create workflow（从 share link 创建+传 connected accounts/step/trigger props）/ $send.s3()/HTTP/email 目的地 | 合并保留增量（r293A ShareLink，本点=REST 创建+$send） | 工具 |
| 7 | Agent Skills | Field Guide 三原则（description says when/body right altitude/self-contained+deterministic parts are code）/ name 规范字段级约束（1-64 字符/小写数字连字符/匹配父目录，多平台一致）/ deepagents 技能数量治理（少而精胜重叠多） | 合并保留增量（r293B 结构/r294A 分发，本点=name 规范+field guide） | 可复用 Skill |
| 8 | skills.sh | API Reference（无 key 60/min、有 key 600/min；audit 端点）/ CLI 管理三命令（list/update/remove）/ 交互式 find | 合并保留增量（r293A CLI/r293C 规模，本点=API+管理命令） | 可复用 Skill |
| 9 | GitHub | Copilot CLI Rubber Duck（跨模型家族独立评审）/ Project Polaris（2026-08 替代 GPT-4 Turbo，MoE 带 Rust/Haskell 语言专家）/ 模型退役表（2026-10-02 批量）/ GitHub Next（Chopin/Autoloop/Repo Mind） | 合并保留增量（r293B Copilot，本点=Rubber Duck+Polaris+退役表） | 工具 |
| 10 | deeplearning.ai | Document AI agentic doc extraction（OCR 丢布局→agentic 保留合并单元格/图表关系/多栏阅读顺序）/ Multi-Vector Image Retrieval（patch 级多向量）/ Multimodal Data Pipelines（媒体转文本） | 合并保留增量（r293B/r293C，本点=多模态面） | 可复用 Skill |

判重口径：增量判定。本轮 10 合并保留增量（每点均含≥40% 独有增量），零纯重复。