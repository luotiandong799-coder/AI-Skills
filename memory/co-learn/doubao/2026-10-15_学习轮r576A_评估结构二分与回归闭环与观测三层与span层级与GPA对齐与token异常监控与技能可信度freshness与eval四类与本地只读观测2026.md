# 学习轮 r576A（2026-10-15 · AI 技能库工程与方法论 + AI 智慧进化）

十站实拉（全量逐站，r576 批第 1 轮，角度为评估与可观测性，与 r575 批错开）：Dify / n8n / LangFlow / Activepieces / Make / Pipedream / Anthropic / skills.sh / GitHub 生态 / deeplearning.ai。判重基准：execute 3.95.0（r575C 3 章）+ compressor 3.692.0（r575C 3 章）+ r575A/B 12 章 + r574 批 18 章 + 更早批次 + WB 留痕。

## 落地（execute 3.95.0 → 3.96.0，+3 章）

1. **评估结构二分与回归闭环：transcript（轨迹）vs outcome（终态）+ Evaluation Trigger 旁路生产 + 发现 bug 加数据集全量回归**（来源：Anthropic《Demystifying evals for AI agents》2026-01-09 + n8n《Production AI Playbook: Evaluation and Monitoring》2026-05-05 + n8n《How to evaluate the performance of AI agents》2026-04-21）
   - 评估记录二分（transcript 完整记录 vs outcome 终态）；评估旁路生产（Evaluation Trigger 独立路径+Check if Evaluating 路由）
   - 回归测试闭环（bug 输入入库+修复全量重跑）；评估指标按 workflow 类型选（分类=intent accuracy/Support=groundedness/提取=field accuracy）
   - **提升层**：工作流 / 可复用 Skill

2. **观测三层与 span 层级 + GPA 对齐 + inline 运行时评估**（来源：NextPage 2026-05-24 + MLflow 2026-05-22 + DeepLearning.AI 2026-05-10）
   - 观测三层（software telemetry/AI behavior/business controls）；span 三层级（会话→推理→工具调用，父-子 span 重构调用链）
   - GPA 三对齐（goal/plan/actions，LLM-as-judge 双评）；inline 运行时逐步骤评估
   - **提升层**：工作流 / 可复用 Skill

3. **token 异常监控与循环检测：按 agent 聚合 token 用量超 200% 滚动均值告警 + 递归重试风暴（47 次×8k token）+ 推理成本占比 55%**（来源：PromptRefinery 2026-07-15 + Soul of the Machine 2026-03-24 + Fordel Studios 2026-09-02）
   - token 异常阈值（>200% 滚动均值告警，预算超支前发现）；循环检测（重试次数+token 累计双指标）
   - 推理成本事实（2026 占基础设施支出 55%+ 首超训练；无控制 30 倍）
   - **提升层**：工作流 / 可复用 Skill

## 落地（compressor 3.692.0 → 3.693.0，+3 章）

1. **技能可信度与 freshness：verified（人跑过通过 QC）vs edited（git 记录）分离 + SkillSpec Doctor 五查 + SkillsBench 量化 33.9%→50.5%**（来源：mohitagw15856 2026-10-12 + skillspec.sh 2026-07-31 + NerdLevelTech 2026-08-09）
   - verified≠edited（已知可用 vs 上次编辑）；Doctor 五查（token load/buried instructions/name collisions/missing proof/public URL risk）
   - SkillsBench 量化（87 任务双标，好技能成功率 33.9%→50.5%，+16.6pp）
   - **提升层**：可复用 Skill

2. **OpenAI eval 四类与 must-pass 小清单 + harness 分层（确定性检查跑 JSONL 轨迹）**（来源：wal.sh《2026 Q2 Skills》2026-06-24）
   - eval 四类（outcome/process/style/efficiency）+must-pass 小清单；harness 分层（JSONL 确定性检查打底+上层语义）
   - **提升层**：可复用 Skill

3. **本地只读观测与 OTel 标准化 + aiMetadata agent 向描述**（来源：tokentelemetry.com 2026-09-29 + AI Workflow Lab 2026-07-12 + Activepieces Changelog 2026-09-03）
   - 本地只读观测（读已有日志+无 SDK+100% 本地）；OTel GenAI conventions（Q2 2026 迁移免重插桩）
   - aiMetadata（agent 向描述+幂等声明）+audience targeting（人类/agent 视图分离）
   - **提升层**：工具 / 可复用 Skill

## 十站实拉要点（逐站留痕）

- **Dify（评估观测角度）**：Arize Phoenix 集成（每个模型调用/工具调用/链步骤自动 trace）；观测栈（Grafana/Langfuse/Arize Phoenix/Opik）；变量检查器（中间值）+节点级类型化错误元数据；OTel 流向 7 外部栈（Langfuse/LangSmith/Opik/W&B Weave/Arize/Phoenix/阿里云 ARMS）；异步集成不影响运行时性能；监控面板（usage/cost/交互质量）
- **n8n（评估角度）**：Evaluation Trigger 节点（独立执行路径旁路生产，Data Table 逐行喂）；Evaluation 节点 "Check if Evaluating" 操作（评估分支 vs 生产分支）；回归测试（发现 bug→加输入到数据集→修复后全量重跑）；指标（Helpfulness 1-5 AI 打分/String Similarity 编辑距离 0-1/Categorization 0-1/Tools Used/Correctness AI judge）；按 workflow 类型选主指标（分类/Support/提取各配主+辅）
- **Langflow（评估角度）**：Openlayer 集成自动收集 tracing；LangChain 多轮评估（跨整段对话评 agent 是否达成目标，LLM-as-judge 自动打分语义意图/结果/轨迹含工具调用）；在线评估（生产流量采样子集，实时检测漂移/质量退化）；Annotation Queues（领域专家无代码审阅）；Align Evaluators（few-shot 对齐 judge 与专家反馈）
- **Activepieces（评估角度）**：audit logs（每次 flow run/用户动作/系统事件+actor+timestamp，SIEM 实时流）；step 级 run logs（输入输出错误）；AI metadata（agent 向描述+幂等声明）；audience targeting（actions 可 target 人类/agent/两者，agent-only 动作不污染人类选择器）；secret manager（Vault/AWS Secrets/1Password，worker 内解析永不暴露给 agent）
- **Make（评估角度）**：agentic loop 四阶段（Perceive→Reason→Act→Observe）；autonomous AI 默认每次日志（variance analysis/performance review 可规模化）；audit logs MCP（查询审计）；observability 三层（software telemetry/AI behavior/business controls）
- **Pipedream（跨站观测角度）**：span 层次（agent 会话顶层 span→reasoning spans→tool call spans 子 span，结果记在 span 属性）；OTel GenAI conventions（Q2 2026 可迁移不用重新插桩）；每边界捕获输入输出+成本延迟；异常路由进 eval loop；Langfuse 被 ClickHouse 收购（$400M Series D，核心 MIT）
- **Anthropic（eval 结构角度）**：Demystifying evals（transcript=trace/trajectory=完整记录含输出/工具调用/推理/中间结果；outcome=环境最终状态）；Agent SDK 可观测性（OTel 导出）；managed agents define_outcome 事件（per-outcome 评估状态）；unintended model actions 研究（agent 为完成任务利用软件漏洞执行命令）
- **skills.sh（技能评估角度）**：SkillSpec Doctor（token load/buried instructions/name collisions/missing proof/public URL risk）；Snyk ToxicSkills 36.8%/3984 技能/13.4% critical=534；agentskill.sh Quality Score 0-100（4 维度）；officialskills.sh 评审（活跃维护/清晰文档/官方或声誉贡献者/非 AI 批量生成）；verified frontmatter（人跑过通过 QC，区别于 git edited）；SkillsBench（87 任务，33.9%→50.5% +16.6pp）；wal.sh（OpenAI eval 四类 outcome/process/style/efficiency+must-pass 小清单；harness 分层确定性 JSONL 检查）
- **GitHub 生态（本地观测工具角度）**：hawkeye（本地 LLM observability stack）；AgentLens（10 行代码内 agent observability）；Token Telemetry（100% 本地/MIT，只读 Claude Code/Codex/Cursor/Gemini CLI 等 12+，无 SDK 无注册）；Opik（21k★ Apache-2.0）；GitHub MCP Server 33.1k★
- **deeplearning.ai（评估课程角度）**：Evaluating AI Agents（观测→组件级 eval→实验迭代）；Building and Evaluating Data Agents（GPA=goal/plan/actions 对齐；LLM-as-judge 评答案相关+grounded+过程对齐；inline evaluations 运行时逐 retrieval step）；Agentic AI（evals 模块+组件级评估+错误分析优先级）

## 功能套件核查（⑦）

三核心套件（wb-ponytail/wb-max-token-saver/wb-context-compressor）本轮无优化升级项；新增章节均标注与既有相邻章节的分工边界与触发词（eval 先定义 good/评估四数/agent 日志三看/结果断言/推理循环限迭代/成本四层/技能评测闭合邻域/SkillSpec 三阶段/插件签名安全等）。

## 垃圾清理（⑨）

删了什么：本批十站实拉全走 general_search，无本地临时文件落盘、未产生新垃圾。保留什么：*.bak 与全部核心产物（两 SKILL 文件 + r576A 留痕 + 既往批次留痕）；历史探针垃圾待删除通道可用时清理。

## 信源健康度

无删源无加源；Flowise 已删除不拉；十站全部可达，未触发桌面 VPN。commit/push 挂起（git 通道持续不可用，累计 r546→r576A 共 31 批）。
