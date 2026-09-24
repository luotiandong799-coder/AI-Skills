# 学习轮 r193-C：多agent圆桌四铁律与自动化六件套分工与数据强制标注与WebGPU浏览器跑27B（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillhub.cloud.tencent.com/skills/muti-agent-stock | OK 全文 |
| 2 | docs.openclaw.ai/automation | OK 全文 |
| 3 | huggingface.co/spaces | OK 周榜 |

## 独点（5 个）
### C1：多 agent 圆桌四条铁律——编排者不写专业判断、成员不直接通信、保留独立声音不调和（来源：SkillHub muti-agent-stock）
- ① 全团队流程必走，禁"问题简单"跳过；② TeamCreate 只能主编执行；③ 消息必经主编聚合，禁成员直连；④ 主编只编排不写专业判断。报告"保留每位专家独立卡片，不合并、不调和"。
- 判据：**多 agent 的价值是独立视角，不是凑人数**——一旦允许互相通信或主编代笔，就退化成一个 AI。
- **提升层**：多 agent 编排。

### C2：OpenClaw 自动化六件套分工（来源：docs.openclaw.ai/automation）
- Automations（定时/一次性/webhook 入口）/ Tasks（台账记录，非调度器）/ Task Flow（多步持久流+revision）/ Hooks（生命周期事件 /new /reset /compaction）/ Standing Orders（AGENTS.md 常驻注入每 session）/ Heartbeat（系统自带 30min 主会话巡检，不建 detached task）。**inferred commitments 已废弃**。
- 判据：**"定时"不是一个东西**——排期、后台任务、多步流、事件钩子、常驻指令、环境监控各有各的载体。
- **提升层**：工作流/自动化。

### C3：数据来源强制标注格式——`根据[工具][代码]，[数据]`，禁"据市场消息"（来源：SkillHub muti-agent-stock）
- ✅ "上证指数3,150.2点 [来源：web_fetch 东方财富]"；❌ "据市场消息……"。
- 判据：**每个数字必须可回溯到工具调用**——模糊来源 = 幻觉温床。
- **提升层**：输出校验。

### C4：Ternary Bonsai 27B 浏览器 WebGPU 本地跑（来源：huggingface.co/spaces 周榜）
- Ternary-Bonsai-2-27B 在浏览器 WebGPU 跑；Qwen-Image-2.1、Wan2.2 14B 视频、StepAudio 3 音乐。
- 判据：**27B 模型已能纯浏览器推理**——本地/零部署 demo 成为主流形态。
- **提升层**：模型/工具。

### C5：合规边界清单——禁买卖建议/禁价格目标/必挂"仅供参考"声明（来源：SkillHub muti-agent-stock）
- ❌ 买入/卖出/持有/加仓；❌ 预测具体价格；❌ "必涨/稳赚"；✅ "本报告仅供信息参考，不构成投资建议"。
- 判据：**领域 agent 要自带合规红线段**——不写就是法律风险。
- **提升层**：安全/合规。

## 判重说明
- C1 多 agent 圆桌 → r188 已记多 agent 共享层；取"四条铁律+不调和"增量。
- C2 六件套 → r192 已记 cron 三条判据；取"Tasks/Task Flow/Hooks/Standing Orders/Heartbeat 分工"增量。
