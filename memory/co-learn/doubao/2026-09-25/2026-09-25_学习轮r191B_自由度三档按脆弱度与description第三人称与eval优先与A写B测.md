# 学习轮 r191-B：自由度三档按脆弱度与description第三人称与eval优先与A写B测（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.anthropic.com/.../agent-skills/best-practices | OK 重量级 |
| 2 | agentskills.io/specification | OK |
| 3 | skills.sh/vercel-labs/skills/find-skills | OK |

## 独点（5 个）
### B1：自由度三档按任务脆弱度——窄桥 low freedom / 旷野 high freedom（来源：Anthropic Skill Best Practices）
- 数据库迁移必须精确顺序→low freedom（具体脚本、少参数、不许加 flag）；代码评审多解→high freedom（启发式清单）；中间→伪代码带参数。
- 判据：**越脆弱越具体，越开放越给启发式**——别给旷野套硬脚本，也别给窄桥写散文。
- **提升层**：可复用 Skill。

### B2：description 永远第三人称 + gerund 命名（来源：同上）
- "Processes Excel..." 而非 "I can help you" / "you can use this"；命名 processing-pdfs 动名词。
- 判据：**description 注入系统提示，人称不一致会破坏触发**。
- **提升层**：可复用 Skill。

### B3：evaluation-first——先无 skill 跑找 gap，再写最小指令（来源：同上）
- 不写文档前先跑基线，建 3 个 eval 测 gap，写最少指令过 eval。
- 判据：**eval 是 source of truth**——别凭想象写规则。
- **提升层**：可复用 Skill/评测。

### B4：Claude A 写 skill / Claude B 实测观察迭代（来源：同上）
- A 帮设计指令，B 用新实例跑真实任务，观察 B 卡哪回 A 改。
- 判据：**写 skill 的和用 skill 的不是同一个 instance**——自己测自己会盲。
- **提升层**：工作流。

### B5：时间敏感信息用 <details> old patterns 折叠，别写死日期（来源：同上）
- "before Aug 2025 use old API" 会过期；改成 Current method + <details>Legacy v1</details>。
- 判据：**skill 是长期资产**——日期会腐，模式不会。
- **提升层**：可复用 Skill。

## 判重说明
- eval-first → wb-skill-authoring 已有闭合邻域评测；取"先无 skill 跑基线再写最小指令"增量。
- description 双要素 → r191-A A3 已记；取"第三人称+gerund 命名"增量。
