# 2026-09-24 学习轮 r159-A Human-in-the-Loop 与 Agent 协作界面

轮次：r159-A｜批：每时 3 轮×10 次｜实拉 10 站全量逐站

批前判重基准：WB r158 三份（束级门控/缓存前缀四档/压缩可见性边界/轨迹断言；输入检查门四则/存储开关/记忆双标识符；时间旅行/后台任务资格/持久目标/线程信号）+ 豆包 r158 三面。本轮角度=Human-in-the-Loop 与 Agent 协作界面（审批门/自主性分级/ask-vs-assume/状态汇报 UI），WB r158 管工具层持久化与门控，本面管人与 agent 的接口层——互补新面。

## 一、实拉证据（URL + 原文片段，10 站）

| 站 | URL | 关键原文 |
|---|---|---|
| 审批门架构 | anhtu.dev（2026-05-25）+ openlegion.ai（2026-06-01） | "**生产审批门四组件=Proposed action+reasoning → 暂停并持久化 checkpoint → 通知 approver → 批准后恢复；pre-execution approval gate=不可逆动作执行前一刻阻断，agent 编排提议后 halt，显式批准信号前任何部分不执行——唯一真保护，因中断编码在工作流结构中 agent 无法绕过**" |
| 风险分级 | AWS AGENTREL02-BP05（2026-09-21）+ aigentlab.tech（2026-09-08）+ devsakaso.com（2026-07-18） | "**三 tier：Autonomous=低风险可逆；Notify=中风险执行并知晓；Approve=高风险不可逆需显式批准；用策略在网关边界强制分级（运行时而非文档）；阈值动态分级（小额低风险自动/超阈值批准）避免全件批准；批准等待期间不产生副作用；对象变更/过期时旧批准失效**" |
| 审批画面 | zalt.me（2026-07-08）+ devsakaso.com | "**agent 的职责=准备最清晰的 briefing 而非推销特定结果；触发人工场景=删客户账户/GDPR、群发、超阈值购买退款、触碰凭证访问控制、生成署名真实个人的内容、指令歧义；画面显示对象/差分/权限/可否撤销；执行前再验证对象与权限**" |
| ask vs assume | OpenAI Model Spec（2026-08-18）+ Behavioral Guidelines for Coding Agent Work（2026-06-01）+ waynetools.rdkworld.com（2026-07-13） | "**不静默假设或隐藏困惑：影响解的重要假设要声明；多个合理解释存在时呈现而非静默选择；需求真不清晰且本地上下文解决不了才问；简单明显任务不打断；多轮成本=每轮付整个历史输入、随轮数平方增长——问的成本与轮的平方相关，静默错做的成本=返工+用户信任**" |
| 自主性分级 | arXiv 2506.12469 Levels of Autonomy + apptitude.io（2026-05-10）+ futurium.ec.europa.eu（2026-07-10） | "**分级谱系：L2 人工确认后执行（提案→一键确认→落地）；L3 人工主导（辅助分析、人掌握最终决策权）；Level 2=guardrails 内自主执行然后报告（适合高量可逆任务，等待成本>偶错成本）；confidence is not authority——治理不问模型置信分，问动作/错误成本/可逆性/谁授权/用了什么上下文/执行后留什么证据**" |
| 澄清策略 | arXiv 2607.21143（2026-09-16）+ arXiv 2602.11199 AskBench（2026-08-28） | "**澄清策略可度量：平均轮数/总成本/总惩罚（unsupported/noisy 累积）；区分简洁消歧 vs 冗长重复交互；交互式循环评测=模型回复 vs judge 判定（澄清问句 or 最终答案）**" |
| 状态汇报 | Smashing Magazine（2026-05-13）+ codeguilds.com（2026-05-15）+ designpixil.com（2026-06-01）+ institutepm.com（2026-06-01） | "**Agentic update 公式=Action Word+Specific Item+Limits（'检查可用性'→'正在查询您日历中 3 月 14 日下午 2-4 点的空闲时段，遵守您团队 45 分钟会议规则'）；动态清单=总体目标/当前步骤/已完成摘要/剩余步骤或时间；progress ledger=可折叠实时时间线+每步置信信号（90%+ 自动继续，低置信要人）**" |
| IM 状态更新 | zylos.ai（2026-07-01） | "**post once, update in place：任务开始发一张状态卡，状态变化原地更新，任务完成才发新通知——消除整类状态刷屏；Teams 用 update-message API 把交互卡片替换为静态摘要**" |
| elicitation loop | neodrop.ai（2026-06-19） | "**Linear 'Write with Agent'：调用后不产完整草稿等批准，而是先问优先级/缺失上下文/强调点——刻意摩擦让用户在成稿前陈述意图；不是澄清缺失数据，是保持认知参与**" |
| agent UI | CSDN（2026-09-21）+ max-gherman.dev（2026-08-08）+ brainy.ink（2026-04-28） | "**Agent UI 围绕 Run 展开非消息列表；事件类型=Task/Plan/Approval/Artifact/Event；七模式=任务框架/自主性滑杆/计划面/进度流/确认门/错误恢复/交接；错误 UX=区分工具超时 vs 对用户意义（文件没保存）、给具体下一步、保留部分进度（7/10 步显示 7 步结果）**" |

## 二、独点清单 + 判非重复理由（6 点，均≥40% 独有增量）

### 1. 审批门四组件架构与不可逆前置门（来源：anhtu.dev 2026-05-25 + OpenLegion 2026-06-01 实拉）
生产审批门四组件=提议+推理 → 暂停持久化 checkpoint → 通知 approver → 批准恢复；**pre-execution approval gate=不可逆动作执行前一刻阻断、中断编码在工作流结构里 agent 无法绕过（唯一真保护）**。
- 判非重复：WB r158A 落"read-before-act 弹回门"（工具加载门）；本点=**不可逆动作的人工批准门**（人 vs 工具）。增量≥80%。
- 提升层：工作流（审批设计）。

### 2. 三级风险分类与动态阈值（来源：AWS AGENTREL02-BP05 + AIgent Lab 2026-09-08 + DevSakaso 2026-07-18 实拉）
Autonomous（低风险可逆）/Notify（中风险执行并知晓）/Approve（高风险不可逆显式批准）；**策略在网关边界强制分级**；阈值动态分级避免"全件批准"；批准等待期无副作用；**对象变更/过期时旧批准失效**。
- 判非重复：点 1 管门怎么建；本点=**哪些动作入哪级门**（分级面）。增量≥65%。
- 提升层：工作流（风险分级）。

### 3. 审批画面要素与 briefing 纪律（来源：Zalt 2026-07-08 + DevSakaso 实拉）
审批画面显示=对象/差分/权限/可否撤销；**agent 职责=最清晰的 briefing 而非推销结果**；执行前再验证对象与权限；触发人工场景清单=删账户/GDPR、群发、超阈值退款、凭证访问、署名真实个人、指令歧义。
- 判非重复：点 2 管分级；本点=**批准时人看到什么/怎么呈现**（画面面）。增量≥60%。
- 提升层：工作流（审批呈现）。

### 4. ask vs assume 决策与澄清成本（来源：OpenAI Model Spec 2026-08-18 + Coding Agent 行为指南 2026-06-01 + arXiv 2607.21143 实拉）
不静默假设：重要假设影响解要声明；多合理解释呈现而非静默选；真不清晰且本地上下文解决不了才问；简单明显任务不打断；**多轮成本随轮数平方增长，静默错做成本=返工+信任损耗；澄清策略用平均轮数/总成本/总惩罚度量**。
- 判非重复：全库无 ask/assume 决策面。增量≥90%。
- 提升层：工作流（交互决策）。

### 5. 自主性分级与"置信不是授权"（来源：arXiv Levels of Autonomy + Apptitude 2026-05-10 + Futurium 2026-07-10 实拉）
分级谱系：L2 人工确认后执行/L3 人工主导；Level 2=guardrails 内自主执行后报告（高量可逆任务，等待成本>偶错成本）；**confidence is not authority——治理问动作/错误成本/可逆性/谁授权/上下文/证据，不问置信分**。
- 判非重复：点 4 管单步问不问；本点=**整体自主度怎么设**（模式面）。增量≥70%。
- 提升层：工作流（自主度设计）。

### 6. Agent 状态汇报与进度 UI 模式（来源：Smashing 2026-05-13 + InstitutePM 2026-06-01 + Zylos 2026-07-01 + CSDN 2026-09-21 实拉）
Agentic update 公式=Action Word+Specific Item+Limits；动态清单=目标/当前/已完成/剩余；progress ledger=可折叠时间线+逐步置信信号（90%+ 自动、低置信要人）；**post once update in place 防状态刷屏**；UI 围绕 Run 非消息列表。
- 判非重复：WB mts 落"进度流与诊断流分开"（汇报内容分工）；本点=**汇报的格式/节奏/可视化结构**（呈现面）。增量≥55%。
- 提升层：工作流/工具（状态 UI）。

## 三、候选未落地（判非重复理由）
- elicitation loop（Linear）：并入点 4（刻意摩擦式澄清变体），不单列。
- 错误 UX（区分工具超时 vs 对用户意义/保留部分进度）：并入点 6，不单列。
- AskBench 交互评测：评测方法面与 WB av 相邻，并入点 4，不单列。

## 四、功能套件检查
wb-ponytail / wb-max-token-saver / wb-context-compressor：本批点 4（ask vs assume 澄清成本/轮数平方增长）与 wb-max-token-saver 成本面**联动候选**（澄清轮数直接乘成本）；点 6 状态汇报与 mts"进度流与诊断流分开"互补。仅留痕记录，不写技能文件。套件覆盖完整，版本不动。

## 五、垃圾清理
本轮仅 general_search，无临时文件。
