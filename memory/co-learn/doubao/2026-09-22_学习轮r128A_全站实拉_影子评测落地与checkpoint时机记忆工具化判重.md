# r128-A 全站实拉 · 影子评测落地 · checkpoint 时机与记忆工具化判重

> 日期：2026-09-22｜批次：r128-A｜模式：定时任务「AI技能库学习·每时3轮×10次」触发
> 基线：HEAD==origin/main==ed65cf1（WB force push 对齐完成，WB 在途修改全量保留）

## 一、逐站实拉（10 次，全量信源覆盖）
| # | 信源 | 实拉内容 | 提炼 |
|---|---|---|---|
| 1 | AWS Well-Architected / explainx / Zylos / Microsoft / agentpatternscatalog / Augment / NeuralBase | 失败恢复/checkpoint/durable execution | checkpoint 时机三规则（自然边界/昂贵操作后/置信度边界）；watermark 防重复副作用 |
| 2 | n8n 官方 + 社区 + arXiv n8n 生态研究 | 节点级重试/Error Trigger/集中错误处理 | 两层错误处理（node Retry + Error workflow 告警/死信） |
| 3 | OpenClaw docs（taskflow/lobster/agent-loop/restart-recovery/tasks） | 持久状态/恢复 token/输出限制恢复 | Lobster approve/resume token；fenced delivery generation；canonical result 7 天保留 |
| 4 | arXiv（AgeMem/SF-AMS/MemAct/FLUXMEM）+ Redis + DigitalOcean + Azure | Agent 记忆管理 | 记忆操作工具化（store/retrieve/update/summarize/discard）；战略遗忘；state vs retrieval 选型 |
| 5 | StartupCorners / 小鹏排行 / heatdrop / Trendshift / DEV | GitHub agent 生态 | Agent Beacon（开源 telemetry 层）；crush/octop 平台 |
| 6 | deeplearning.ai（corporate/learn/community） | 新课程盘点 | Building Adaptive AI Agents（8月）；Generative UI（2月）；Governing AI Agents |
| 7 | Anthropic Skills 官方 + SkillsMP + agentman 生态报告 + localskills | 技能生态目录对比 | Skills.sh npm 式；SkillsMP 1.9M 零审核；SkillHub TRACE 评测；Agensi 8 点扫描 |
| 8 | 腾讯 SkillHub / 虾小宝 / 36氪 / 央广网 / 智谱 AgentMore | 中国技能市场 | SkillHub 8 万+、SkillPay；虾小宝 3.5 万+；字节双线 |
| 9 | Zen van Riel / Startup Fortune / Growth Engineer / Microsoft / Velocity / CallSphere / HKU | guardrails 与生产评测 | 六层 guardrail 栈；shadow evaluation；3 级评测框架；guardrail 可测性 |
| 10 | Zylos handoff / Twilio / Velocity / LiveKit / InfoQ / Calmops | Agent-人移交模式 | Confidence Governance；Hard Gates 清单；同步审批门 |

## 二、判重与落地
- **D194 影子评测（落 · av）**：候选版处理真实流量但不 serve，输出离线与线上版对比——合成数据测不出真实混乱，shadow 先行、A/B 后行。查重：av 已有"离线评估/生产评估/影子副本"，但"shadow 评测（流量复制不 serve）"为独有增量，重叠<60% → 落。
- **D192 checkpoint 时机三规则（不落）**：ED checkpoint/检查点 23+8 处覆盖（幂等/恢复/断点），时机规则为同族细节增量，重叠>60% → 不落。
- **D193 记忆操作工具化（不落）**：ctx 已有记忆自主管理（四策略提取/成本核算/持续裁剪），工具化仅为实现形态差异，方法论重叠 → 不落。

## 三、逐站判非重复理由（未落地站点的证据）
- n8n/OpenClaw 错误处理与恢复：ED 已落 transport/tool 分开重试、幂等、执行/交付态分开（§重试分两类管、§定时任务记账判据）→ 重叠。
- Agent 记忆（SF-AMS/MemAct/FLUXMEM）：ctx 已落记忆提取策略/衰减/成本核算 → 同族。
- GitHub 生态（Beacon/telemetry）：工具/平台层，个人使用不投入 → 淘汰。
- deeplearning.ai 新课程：平台课程，无方法论独点 → 不落。
- 技能生态目录对比：平台数据（SkillsMP 1.9M 零审核等），判重基准参考，不落地 → 淘汰。
- guardrails 六层栈/Hard Gates/handoff：av/ED 已落各层（guardian/审批三要素/预算上限）→ 重叠。
- checkpoint 时机：ED 已覆盖 → 重叠。

## 四、功能套件检查（每轮）
- 套件：wb-ponytail / wb-max-token-saver / wb-context-compressor
- 本轮：三件套功能覆盖完整（简洁输出/成本四层/上下文预算管理），无退化、无需增删；av 新增影子评测小节不影响套件。
