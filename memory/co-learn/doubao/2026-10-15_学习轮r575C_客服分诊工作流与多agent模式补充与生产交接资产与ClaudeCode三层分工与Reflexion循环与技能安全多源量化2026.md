# 学习轮 r575C（2026-10-15 · AI 技能库工程与方法论 + AI 智慧进化）

十站实拉（全量逐站，r575 批第 3 轮，角度为案例/模板/实战，与 A/B 错开）：Dify（客服案例角度）/ n8n（模板案例角度）/ Langflow（模板案例角度）/ Activepieces（模板案例角度）/ Make（模板案例角度）/ Pipedream（集成案例角度）/ Anthropic（Claude Code 工程化角度）/ skills.sh 生态（安装榜角度）/ GitHub 生态（Trending 今日榜角度）/ deeplearning.ai（设计模式/多智能体案例角度）。判重基准：execute 3.94.0（r575B 3 章）+ compressor 3.691.0（r575B 3 章）+ r575A 6 章 + r574 批 18 章 + 更早批次 + WB 留痕。

## 落地（execute 3.94.0 → 3.95.0，+3 章）

1. **客服与分诊工作流：问题分类器路由差异化路径 + LLM 数据结构化 JSON 防错位 + 分诊输出结构（category/team/confidence）+ 情绪标注写回 + 阈值警报分支**（来源：阿里云 2026-06-09 + 腾讯云 2026-05-31 + DEV 2026-10-02 + 51CTO 2026-09-21 + Make 2026-09-24 + n8n 2026-06-15 + Activepieces 2026-03-06）
   - 问题分类器路由差异化路径（分类→各分类独立处理链）；LLM 数据结构化防错位（清洗映射 JSON 字段+下游 API 写入）
   - 分诊输出结构（category/team/confidence+低置信人工）；情绪标注写回行（即时过滤）；KPI 阈值警报分支（降 10% 单独警报+失败通知）；Ask AI+router 分流
   - **提升层**：工作流 / 可复用 Skill

2. **多 agent 模式补充与垂直分工：Debate/Ensemble/Supervisor-Worker + 投资小组四角色 + crewAI 三要素 + Planning 判据 + spec 驱动循环**（来源：James Hu 2026-09-13 + CSDN 2026-09-26 + Prasanth 2026-02-16 + hub.cissychen 2026-05-23 + DeepLearning.AI 2026-09-03）
   - 补充三模式（Debate 对抗/Ensemble 聚合/Supervisor-Worker 上下文负担）；投资小组垂直分工四角色（数据→分析→风控→整合）
   - crewAI 三要素（role/goal/backstory）+task 二要素；Planning 触发判据（≥8 步/每步贵/信息足）；spec 驱动循环（spec→implement 分支→validate 人审→replanning）
   - **提升层**：工作流 / 可复用 Skill

3. **生产交接与资产：handoff 交接技能 + Blueprint 导出（结构不含数据）+ 结果回写 + 内容复用链 + REA 证据附注 + Architect Agent 跨文件重构**（来源：抖音 2026-10-14 + Make Guide + Jodoo 2026-09-22 + DeepUseCase 2026-09-02 + 36kr 2026-10-12 + 豆包权威 2026-10-08）
   - handoff 交接技能（AI 间活交接）；Blueprint 导出（结构不含数据+跨区复制）；动作+回写闭环（邮件发完 log 回表）
   - 内容复用链（JSON 逐平台复用+平台化约束）；REA（MCP+CLI+全本地+结论附证据）；Architect Agent（跨文件依赖分析+一致性同步）
   - **提升层**：工具 / 可复用 Skill

## 落地（compressor 3.691.0 → 3.692.0，+3 章）

1. **Claude Code 三层分工与技能库生态：Skill 单类事+大资料拆 supporting files / Hook 简单确定性约束 / Subagent 复杂决策+上下文隔离 + skills.sh 安装榜 + Trending 抓榜技巧**（来源：今日头条 2026-04-05 + 抖音 2026-10-14 + CSDN 2026-10-08）
   - 三层分工判据（按确定性分层：简单→hook，复杂→skill/subagent）；skills.sh 安装榜（find-skills 380 万/handoff/agent-browser，6 个同仓）
   - Trending 抓榜技巧（周一 UTC 周榜+语言分流过滤）
   - **提升层**：可复用 Skill

2. **Reflexion 循环与记忆机制 + Web RAG 双工具分工 + 多键检索 + pandas 校验 LLM 解释 + 线索评分权重**（来源：hub.cissychen 2026-05-23 + karam-nus 2026-04-01 + Langflow 2026-08-15/2026-06-28 + CSDN 2026-03-02 + Keerok 2026-05-14）
   - Reflexion 循环（反思写记忆+重做，Shinn 2023 论文实证）；Web RAG 双工具（URL 拉新 vs 向量搜索）
   - 多键组合检索（意图+地区）；pandas 校验+LLM 解释修复；线索评分权重（预算 40/特异性 30/公司类型）
   - **提升层**：可复用 Skill

3. **技能安全多源量化与技能库生态：SkillSpector 26% 漏洞率 + tsecbench 进攻型技能库 + 技能市场规模 334k + 科学技能库**（来源：MagicNetWorld 2026-09-29 + 腾讯 2026-10-07 + LobeHub 2026-09-30 + OpenAgentSkill 2026-10-11）
   - 多源印证（NVIDIA 26% vs Snyk 36.82% 两扫描器交叉）；tsecbench 进攻型技能库 3 库（防御学习从进攻入手）
   - 技能市场规模（LobeHub 334k skill+科学库 140 技能/100 数据库/160k 科学家）
   - **提升层**：可复用 Skill

## 十站实拉要点（逐站留痕）

- **Dify（客服案例角度）**：客服系统能力（用户选地区+输入问题→LLM 识别意图→检测地区→按意图+地区检索知识库→生成答案）；问题分类器路由差异化路径（阿里云：按物流/颜色/尺寸三分类，颜色=检索+LLM，尺寸=直接回复）；LLM 数据结构化（清洗映射 JSON 字段+飞书表格 API 防字段错位）；客服三件套（意图识别/RAG 注入/Function Calling 查单）；零代码搭建+一键部署全球加速；钉钉流式输出（dify-on-dingtalk）
- **n8n（模板案例角度）**：Airtable 作流程界面（全部步骤用表从左到右驱动内容创作+人工审核）；财务简报（KPI 摘要→GPT-4o-mini→Telegram 格式→Notion+Telegram，收入降>10% 单独关键警报+失败通知）；发票拍照→Gemini 提取→Notion+摘要+每周图表报告；工单分诊引擎（$0.002/票，Few-shot 提准+category/team/confidence+低置信转人工）；部署避坑（GENERIC_TIMEZONE+TZ 显式设置防 UTC）；五实用自动化（邮件回复/抓取/记忆聊天/文档分析/社媒 agent）
- **Langflow（模板案例角度）**：Notion Meeting Notes Agent（识别任务/行动项/要点→写 Notion）；Web RAG 四件（Prompt 管工具用法→Agent 选工具：URL fetch_content 拉新/Astra DB search_documents 语义搜索）；CUGA 组件（MCP Tools+Calculator+Read File 到 Tools 端口）；通话/工单分类字段集（stage/objection/competitor/sentiment/SLA）；DataFrame 分析（Batch Run 批量情绪/pandas 校验+LLM 解释异常+修复建议/RAG 文档+指标结合）
- **Activepieces（模板案例角度）**：11 个 AI 自动化例子清单（博客生成/社媒排期/SEO/线索评分/销售外联/工单分类/客户回复/发票提取/报告/入职/简历筛选）；社区消息监控（Discord 触发→存表→Ask AI 判紧急→router 分流→发支持频道）；Airtable MCP 五流（供应商评估/活动策划跟进+邮件发完 log 回 Airtable）；发票 PDF（Sheets 新行→Find Rows→Code→HTTP→Gmail）；定位（开源 Zapier 替代 200+ pieces+分支流+TypeScript SDK，采购否决 SaaS 用例）
- **Make（模板案例角度）**：7 个可抄 AI 自动化；反馈情绪标注（Google Sheet 新行→OpenAI 标正/负/中立→写回行，负面高峰即时捕获）；AI 晨报行政助手（Run an Agent+system prompt 定义角色+精确输出格式+JSON payload）；Blueprint 导出（可移植 JSON 含结构逻辑不含数据，备份/分享/跨区复制）；AI 线索评分（预算 40/特异性 30/公司类型权重→只返回结构化 JSON→Parse JSON→Router 分支）；YouTube→Whisper→ChatGPT→WordPress；入门最佳模板（新线索→Slack+Sheets 3 模块 25 分钟）
- **Pipedream（集成案例角度）**：MCP 端用户三用例（Linear 票→产品更新/Google Calendar→会议准备/PostgreSQL→最近客户洞察）；发票异常审阅字段集（异常类型/扣留原因/付款就绪/审阅人/预算负责人/建议处理/优先级+用测试执行/事件检查/请求日志验证 payload 形状）；抓取工作流（网页→LLM 产品摘要）；内容复用链（JSON 传递+平台化 prompt 约束：强观点钩子/问句结尾/不用 hashtag）；邮件→Gemini 摘要分类→Critical 发 Slack→Jira 建单；AI 问答机器人（Slack mention 触发）
- **Anthropic（Claude Code 工程化角度）**：三层分工（Skill=单类事+描述清晰+步骤完整+大资料拆 supporting files；Hook=强制执行规则的拦截层+简单确定性约束+复杂决策交给 Skill/Subagent；Subagent=隔离上下文的工作单元）；Trae Work/Code 模式；Architect Agent（多文件重构+跨文件依赖分析+同步改接口/类型/调用方一致性）
- **skills.sh 生态（安装榜角度）**：skills.sh 全站安装榜（find-skills 380 万/agent-browser/grill-me/setup-matt-pocock-skills/hyperframes-cli 周涨最猛/handoff；前 10 名 6 个同仓；真正值得先装 3 个）；SkillSpector（NVIDIA 26% 漏洞率）；tsecbench 进攻型技能库（Anthropic-Cybersecurity-Skills/ctf-skills/awesome-skills-security 3 库）；LobeHub 市场 334,154 skill；Scientific Agent Skills（140 技能+100 数据库+160k 科学家）
- **GitHub 生态（Trending 今日榜角度）**：REA（Reverse Engineer Anything：一天 54,706 星/72k 总星/MIT；MCP 服务器+CLI 工具+二进制/Electron/APK/网页/固件全拆+全本地+结论附证据）；artcraft（艺术家 AI 图像视频 IDE 4,078 星）；9 月月榜主题（Agent 怎么想/怎么管/怎么记/怎么看见世界）；addyosmani/agent-skills 26k+；抓榜技巧（周一 UTC 周榜+语言分流过滤，综合榜被 Tutorial/Awesome 挤占）；google/agents-cli 4.1k
- **deeplearning.ai（设计模式/多智能体案例角度）**：投资决策小组四角色（数据爬虫→金融分析→风控预警→投资经理整合）；Planning 判据（≥8 步+每步昂贵+信息足）；Reflexion（Shinn 2023 arXiv:2303.11366：跑完反思→写记忆→带反思重做，HumanEval 增益）；多 agent 补充模式（Debate 对抗/Ensemble 投票聚合/Supervisor-Worker 上下文负担）；crewAI 三要素（role/goal/backstory）+task 二要素（description/expected_output）；spec 驱动循环（spec→implement 分支→validate 人审→replanning 更新 constitution/roadmap/workflow）

## 功能套件核查（⑦）

三核心套件（wb-ponytail/wb-max-token-saver/wb-context-compressor）本轮无优化升级项；新增章节均标注与既有相邻章节的分工边界与触发词（执行态交付态/eval/分类器/置信度标注/交接四要素/记忆流水线/双路召回/异常检测/技能榜单/ToxicSkills 等）。

## 垃圾清理（⑨）

删了什么：本批十站实拉全走 general_search，无本地临时文件落盘、未产生新垃圾。保留什么：*.bak 与全部核心产物（两 SKILL 文件 + r575A/B/C 三份留痕 + 既往批次留痕）；历史探针垃圾待删除通道可用时清理。

## 信源健康度

无删源无加源；Flowise 已删除不拉；打不开自动开桌面 VPN（本批未触发，所有站均可达）。commit/push 挂起（git 通道持续不可用，累计 r546→r575C 共 30 批）。
