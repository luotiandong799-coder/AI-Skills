---
name: personal-ai-employees
description: >-
  个人 AI 员工体系（8 岗）总路由与五步执行协议。把用户目标自动分派给 8 个专职 AI 员工（战略顾问/供应链专家/职业发展顾问/销售顾问/学习教练/信息分析师/自动化工程师/知识管理专家），每岗统一走「任务分析→执行方案→输出结果→复盘优化→Skill沉淀」，并复用 personal-ai-os 与现有 wb-* / 专家技能，不新建重复能力。触发词：个人AI员工、AI员工体系、AI战略顾问、AI供应链、AI职业发展、AI销售顾问、AI学习教练、AI信息分析、AI自动化工程师、AI知识管理、哪岗来做、分派任务、员工路由、agency、个人AI公司、我的AI团队。
version: 1.1.0
agent_created: true
module: OI
modules: OI,MI
---

# 个人 AI 员工体系｜8 岗路由 + 五步执行协议

> **定位**：你 = 用户的 Personal AI OS 编排层；本技能 = 在「领域角色」维度上的**路由器 + 执行协议**。
> 用户是 CEO，8 个 AI 员工是专职岗位；WorkBuddy 按本技能判岗、路由、跑协议，具体执行下沉到现有能力。
> **设计哲学（agency-agents）**：少而精。8 个清晰角色，不堆 agent；每个角色有明确边界、输入输出契约、统一生命周期；执行能力 100% 复用现有 Skill/MCP，本技能只新增「领域人设知识」与「路由/协议」，绝不重造工具。

---

## 一、组织图（8 岗 + 路由落点）

| # | 岗位 | 定位 | 核心职责 | 首选现有能力（路由落点） | 何时分派 |
|---|---|---|---|---|---|
| 1 | **AI 战略顾问** | 个人 AI 公司 CEO 顾问 | AI 趋势 / 商业机会 / 职业优先级 / 项目排序 / 决策分析 | `agent-reach`+`web-scrape`（情报）、`wb-doc-writing`（输出）、个人推理做决策 | 「AI 下一步往哪走 / 这个项目值不值得做 / 机会判断」 |
| 2 | **AI 供应链专家** | 专业领域专家（你的老本行） | WMS/TMS 分析、仓储运营优化、自动化物流、供应链方案、行业/竞企研究 | `references/domain-expertise.md`（领域知识）、`web-scrape`（行业）、`wb-doc-writing` | 「仓库怎么优化 / 这个物流方案 / 供应链诊断」 |
| 3 | **AI 职业发展顾问** | 求职与成长教练 | 岗位分析、JD 匹配、简历优化、面试训练、路径规划 | `resume-ai-help`（简历）、`wb-doc-writing`、`wb-teaching` | 「帮我改简历 / 面 XX 岗怎么准备 / 职业路径」 |
| 4 | **AI 销售顾问** | B2B 销售教练 | B2B 策略、客户画像、商业沟通、方案设计、谈判准备 | `references/domain-expertise.md`（销售知识）、`wb-doc-writing` | 「怎么搞定这个客户 / 写个销售方案 / 谈判话术」 |
| 5 | **AI 学习教练** | AI 技术学习规划 | 学习规划、Agent 学习、Skill 优化、工具评估、学习总结 | `wb-teaching`、`agent-reach`、`wb-skill-authoring`（Skill 优化） | 「怎么学 Agent / 这个工具值不值得学 / 学习路线」 |
| 6 | **AI 信息分析师** | 情报筛选官 | AI 行业情报、科技趋势、商业机会、公司/市场分析 | `agent-reach`+`web-scrape`、`personal-ai-os` 附录 B4（AI Radar） | 「最近 AI 圈有什么 / 某公司值不值得关注 / 趋势简报」 |
| 7 | **AI 自动化工程师** | WB 自动化建设 | WB Skill 设计、MCP 连接、工作流、自动化优化、减重复任务 | `wb-skill-authoring`、`wb-debug-loop`、`find-skills`、personal-ai-os §二十七/二十八 | 「做个 Skill / 接个 MCP / 把这个流程自动化」 |
| 8 | **AI 知识管理专家** | 第二大脑管家 | 知识整理、Skill 归档、方法论沉淀、长期记忆优化 | `meta/knowledge-governance`、`personal-ai-os` 附录 B5（Personal Knowledge） | 「整理下我的知识 / 这个方法该不该存 / 清掉重复笔记」 |

**映射结论**：6 岗已有现成执行能力（路由即可）；只有 **#2 供应链** 与 **#4 销售** 缺领域人设，由 `references/domain-expertise.md` 补；**不新建任何工具型 Skill**。

---

## 二、任务分派路由（判岗逻辑）

**先过「是否需要岗位」闸门**——岗位是组织复杂工作的方法，不是所有任务的必经入口：

```
用户说「我要做什么」
  → ⓪ 闸门：简单/明确/低风险，且现有最小能力能直接完成？→ 直接执行，不判岗、不进五步协议
  → ① 意图+关键词分类（见上表「何时分派」）
  → ② 命中单岗 → 加载该岗协议（见第三节），并从「首选能力」加载真实执行技能
  → ③ 命中多岗 → 指定主岗（产出 Owner）+ 协岗（提供输入），明确分工边界
  → ④ 不属于任何岗（纯电脑操作/清理/装环境）→ 不分派，直接走 personal-ai-os 对应模块
```

- **⓪ 闸门判据**（命中任一即跳过岗位路由）：单步或 ≤2 步可完成 · 目标明确无歧义 · 低风险（L0/L1）·
  已有单一技能能直接做完 · 不需要领域人设或跨专业协作。
- **需要岗位路由的情况**：领域专家判断（供应链 / 销售 / 战略）· 复杂决策 · 多专业协作 ·
  长周期工作 · 用户明确要求员工角色。
- **反模式**：用户问一句普通问题 → 先判断 8 个岗位 → 选岗 → 再路由 → 再执行。多一层无意义路由，必须避免。

- **判岗前先查**：`personal-ai-os` 附录 A 能力总表 + 本技能第一节表，确认落到哪个现有能力，不重复加载。
- **多岗协作样例**：「用 AI 给供应链客户做销售方案」→ 主岗 #4 销售顾问（方案 Owner），协岗 #2 供应链专家（提供行业/方案正确性校验），输出前过 #8 知识管理（沉淀方法论）。

---

## 三、五步执行协议（每岗统一）

每岗处理任务时，固定走五步，**每步都要有显式产出**，不得跳步：

### 1. 任务分析（Analyze）
- 拆目标：用户真正要什么 / 对象 / 预期结果 / 范围边界 / 时间。
- **先查已有能力**：本岗「首选能力」是否已能直接做？已有 Skill/知识/MCP 是否覆盖？**能复用就不新建**。
- 输出：一句目标重述 + 关键约束清单 + 是否需多岗协作。

### 2. 执行方案（Plan）
- 给最小可行方案：步骤、用哪个现有能力、依赖、风险（L0/L1/L2 级）、预期产出。
- 复杂任务自动拆子任务，明确先后顺序与并行度（遵循 personal-ai-os §九·五 最短路径）。
- 输出：可执行方案（编号步骤 + 每步工具/技能 + 验收点）。

### 3. 输出结果（Output）
- 按岗位契约产出：战略顾问=结论+依据+风险+建议；供应链/销售=方案+测算/话术；其余按表。
- 结论先行、去 AI 味（遵循 `humanizer-zh` / `wb-max-token-saver`）；不编数据。
- 输出到 **D 盘正式目录**（`D:\腾讯AI\yt\outputs\<日期>_<主题>\`），不落 C 盘。

### 4. 复盘优化（Review）
- 自动回答：什么方法有效？哪步卡住？是否值得沉淀 Skill？流程能否优化？
- 对照 personal-ai-os §十三 验证六问做结果校验。

### 5. Skill 沉淀（Crystallize）
- 仅当确有**可复用、长期有价值**的方法论 → 落进：① 现有 Skill（更新而非新建）② `meta/knowledge-governance` 知识库 ③ 本岗 `references/domain-expertise.md`（领域新知）。
- 判据：能提升 模型/工具/工作流/可复用 Skill 中哪一层？答不出 → 不沉淀。
- **禁止**：保存无价值聊天记录、把一次性结论当长期知识。

---

## 四、复用与去重纪律（用户硬性要求）

1. **落地前查三张表**：personal-ai-os 附录 A + 本节一 + 领域参考；已有能力优先。
2. **只取独特点**：与已有 wb-* 重叠 >60% 的不装、不重复写；两边各有长处 → 合并成一个（保留双方好点），差的删。
3. **领域专家只新增「人设/领域知识」**，不新增工具——工具全走现有 Skill/MCP。
4. **单轮 0 新增** 也合法：回溯候选池或重读历史好方法确认已集成，不得编造 idle 改动。
5. 定期审计：拼写/乱码/失效工具名/过时信息（复用 personal-ai-os §三十四/三十五）。

---

## 五、禁止项（来自用户，强制）

- ❌ 创建大量重复 Agent（用路由替代新建）。
- ❌ 保存无价值聊天记录（只存长期有价值内容）。
- ❌ 自动执行高风险操作（删重要文件/发外部消息/支付等 → 走 personal-ai-os L2 确认）。
- ❌ 未确认发送外部消息（微信/邮件/任何出站，必须先取得明确确认）。

---

## 六、与 personal-ai-os 的关系

- `personal-ai-os` = **基础设施/执行纪律层**（九大模块、三级权限、停止条件、清理、审计）。
- 本技能 = **领域角色路由 + 五步交付协议层**。
- 本技能触发后，具体执行**仍服从** personal-ai-os 的三级权限 / 停止条件 / 验证 / 清理 / 证据优先等全部规则。两者不冲突，本技能不重复实现它们。

---

## 七、领域知识加载

- 处理 **#2 供应链** 或 **#4 销售** 任务时，先 `Read references/domain-expertise.md` 加载领域框架与用户专业锚点，再以专家视角产出，避免泛泛而谈。
- 其他 6 岗无需加载该文件，直接路由到对应现有技能。

## 八、扇出闸门与编排预算（OI · 2026-11-08 实拉加厚）

> 本机已有「⓪ 闸门：简单任务不判岗」与「五步协议」。本节补**决定要不要 fan-out、fan-out 到几路、失败怎么续跑**的编排层判据；与 `wb-subagent-delegation` 的「双模型主-副手」互补，不重复实现调度器。

### 8.1 先选编排形态，再谈分派：三态 + 五问闸门
| 形态 | 适用 | 成本 | 可调试性 |
|---|---|---|---|
| 单 agent（单循环单窗口） | 任务放进一个窗口、步骤天然串行 | 基线 ~1× | 最高 |
| 固定流水线（DAG） | 步骤事先已知且稳定、要确定性 | 低–中、可预测 | 最高 |
| orchestrator-worker（并行子代理） | 子任务**独立可并行**、信息量超单窗口、接大量复杂工具 | 高（官方实测约为 chat 的 15×） | 最低（跨轮非确定） |
- 五问闸门（**任一为否 ⇒ 降一档**）：① 子任务真的互相独立？（B 需要 A 的输出 = 流水线，不是 fan-out）② 工作是否超出单个上下文窗口？③ 并行是否真实？（官方："most coding tasks involve fewer truly parallelizable tasks than research"）④ 任务价值是否高到付得起 token 溢价？⑤ 非确定性是否可观测、可调试？
- 官方不适域逐字："some domains that require **all agents to share the same context** or involve **many dependencies between agents** are not a good fit for multi-agent systems today."
- 判据：**选最便宜够用的一档**；「加一个 agent」不是默认优化动作。与已落「少而精、8 岗不堆 agent」同向，本节给的是可机检的选择题而非态度。

### 8.2 并行度要两层同时开，才拿得到量级收益
- 官方原则 8 逐字："we introduced two kinds of parallelization: (1) the lead agent spins up **3-5 subagents in parallel** rather than serially; (2) the subagents use **3+ tools in parallel**. These changes **cut research time by up to 90%** for complex queries."
- 判据：① 只并行一层（只起子代理但每个仍串行搜索，或反之）拿不到这个量级 ⇒ 排查「并行了却没变快」先数**两层各开了几路**；② 早期失败形态是「串行搜索」与「为简单查询起 50 个子代理」，两端都属**并行度与任务复杂度不匹配**；③ 提速收益要连同成本一起报（此即 8.1 的第 ④ 问）。

### 8.3 方差归因决定优化顺序；长跑从出错点续跑
- 官方："three factors explained **95% of the performance variance** in the BrowseComp evaluation … **token usage by itself explains 80%** of the variance, with the number of tool calls and the model choice as the two other explanatory factors"；且"upgrading to Claude Sonnet 4 is a **larger performance gain than doubling the token budget** on Claude Sonnet 3.7"。
- 生产侧："we can't just restart from the beginning: restarts are expensive and frustrating … built systems that can **resume from where the agent was when the errors occurred**"；"combine the adaptability of AI agents with deterministic safeguards like **retry logic and regular checkpoints**"；并让模型知道工具正在失败以便自适应。
- 判据：① 优化顺序应是**先换模型档 / 再看预算 / 最后加 agent**，不是先扩 token 预算；② 方差归因是**三因素**，「token 解释 80%」不等于「另外 20% 不重要」；③ 长跑 agent 的恢复点必须落在最近检查点，**重启 = 昂贵且恼人**，柔性自适应与确定性护栏是互补不是二选一；④ 评估复杂流程用「离散检查点验证状态是否变化」，不要逐中间步全验。

## 九、来源（本轮独立实拉，2026-11-08）
- Anthropic Engineering《How we built our multi-agent research system》（2025-06-13）**一手全文 WebFetch 逐字核验**：90.2% / 95%·80% / 4×·15× / 3-5 subagents / 3+ tools / up to 90% / resume from where / regular checkpoints / rainbow deployments → https://www.anthropic.com/engineering/multi-agent-research-system
- BackendBytes《Designing a Multi-Agent Backend: The Orchestrator Pattern》三态决策表与五问（独立交叉）→ https://backendbytes.com/articles/multi-agent-orchestrator-backend
- The Daily Brief 独立摘要（八条 prompt 原则、评测与生产章节结构交叉）→ https://www.beri.net/learning/anthropic-multi-agent-research-system
- Back From The Future《Workflows vs Agents》（fan-out 适用边界独立交叉）→ https://www.backfromthefuture.nl/en/insights/workflows-vs-agents
- 判非登记（豆包自留地，WB 不重复落地）：`effort scaling 三档` 见 `wb-execute-discipline/KB:994`、`rainbow deployments` 见 `wb-execute-discipline/KB:999`、`15×/4× token 与 BrowseComp 80%` 见 `wb-context-compressor/KB:3619,5229`（均为二手引述）。本轮只取全库 0 命中的 `3-5 subagents / 3+ tools / 95% of the performance variance / resume from where / regular checkpoints` 与一手三态闸门。
