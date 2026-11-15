---
name: agent-evolution
version: "1.11.0"
description: 智能体持续进化引擎：将每次高价值任务自动沉淀为可复用 Skill、经验与规则，并统一调度已有 Skill 体系完成智能调用、持续优化、工作流记忆、安全检查与生命周期治理，杜绝重复造轮子。触发：完成复杂任务后需总结方法、发现可复用流程想生成 Skill、任务收尾想自动复盘、希望 Agent 少问多想自主进化时调用。
license: MIT
metadata:
  layer: meta
  role: 协调器/路由器（不重实现，全部委派给已有技能）
  reuse:
    - meta/personal-ai-os
    - engineering/distill-cat
    - engineering/wb-skill-authoring
    - skills/knowledge-governance
    - engineering/wb-spec-driven
    - engineering/wb-execute-discipline
    - engineering/wb-debug-loop
    - system/skills-security-check
    - agent/agent-guild
module: AI
modules: AI
---

# 智能体能力进化引擎（agent-evolution）

本 Skill 是 **Hermes Agent 式长期进化的常驻协调层**。它不重实现任何能力，而是定义一条「任务后自动进化循环」，并把八大能力逐一路由到已有 Skill。目标：让 WorkBuddy 每完成一次高价值任务，就自动变强一点，同时**保持 Skill 库精简**。

> 最高约束（来自用户原则，优先生效）：**少而精、禁止重复、优先复用、持续进化、结果导向**。本 Skill 自身不存放方法论正文，只做编排与触发。

## 一、八大能力 → 已有技能路由表（优先复用，禁止重造）

| # | 能力 | 实际执行者（已有 Skill） | 本层只做 |
|---|---|---|---|
| 1 | Skill 自动沉淀 | `engineering/distill-cat`（蒸馏成技能包）+ `engineering/wb-skill-authoring`（写法/审计/接线） | 触发判定 + 传料 |
| 2 | Skill 智能调用 | `meta/personal-ai-os` 路由 + 各 Skill 触发词；多 Skill 组合走 `engineering/wb-spec-driven` 编排 | 路由决策 |
| 3 | Skill 持续优化 | `engineering/wb-skill-authoring`（体检/盲测）+ `skills/knowledge-governance`（巡检）+ `engineering/wb-debug-loop` | 排程复盘 |
| 4 | 工作流记忆 | `skills/knowledge-governance`（记忆分层）+ `agent/agent-guild`（跨 agent 共享）+ 工作记忆文件 | 写入规范 |
| 5 | Agent 执行规划 | `engineering/wb-spec-driven`（规约驱动）+ `engineering/wb-execute-discipline`（零省略） | 生命周期串接 |
| 6 | 自动安全检查 | `system/skills-security-check` + `meta/personal-ai-os` §4–§8（三级权限/停止条件） | 前置+后置清单 |
| 7 | Skill 生命周期 | `engineering/wb-skill-authoring`（合并去重/双路由防呆）+ `skills/knowledge-governance`（合并/压缩/归档） | 触发治理 |
| 8 | 多入口适配 | `meta/personal-ai-os` Computer Agent + `system/browser-automation`/`bsk-*` + `system/computer-use-windows` + 各连接器 | 统一收口进本循环 |

## 二、持续进化主循环（统一生命周期）

每次任务严格走：

```
需求分析 → 任务规划 → 调用 Skill → 执行工具 → 结果检查 → 沉淀总结 → 优化迭代
```

- **需求分析**：先判断任务指向，再定入口层（见 `meta/personal-ai-os` 信息获取梯度）。
- **任务规划**：≥3 步的实现任务先立规约（`wb-spec-driven`）。
- **调用 Skill**：命中即加载，不凭记忆复述冒充加载；多步组合用编排。
- **执行工具**：Agent 模式全程自主，仅安全/不可逆/系统强制手势才请用户介入。
- **结果检查**：独立验证（`wb-artifact-verification` 思路）+ 清理垃圾文件（见下「后置安全检查」）。
- **沉淀总结**：跑 §三 复盘清单，决定是否沉淀（§四）。
- **优化迭代**：更新相关 Skill 或记忆，触发 §七 生命周期治理。

## 三、任务后自动复盘清单（每次高价值任务必跑）

逐项回答，结论写进工作记忆，不达标则进入优化：

1. **是否完成目标** —— 是/否；未达成原因与证据。
2. **哪一步效率低** —— 标出耗时/调用最多的环节，给具体优化动作。
3. **是否产生错误** —— 报错/失败/返工；根因与修复（走 `wb-debug-loop`）。
4. **是否需更新 Skill** —— 若某步骤方法可复用且现有 Skill 未覆盖或已过时 → §四 判定。
5. **是否产生新用户习惯/决策规则** —— 是则写入 `skills/knowledge-governance` 记忆层，避免下次再问。

## 四、自动沉淀判定（何时生成/更新 Skill）

**价值门（先过门，再谈 §四 条件）**——以下**一律不沉淀**，直接跳过：
一次性操作 · 临时路径 · 当前机器专属细节 · 偶然命令 · 一次失败的临时 workaround ·
纯环境差异 · 无法复用的聊天上下文 · 普通成功任务。

过门条件（**同时满足**「可复用」与「有增益」两条才继续）：
- **可复用**：跨任务 / 跨场景能用，不是本次独有。
- **有增益**：明显提升效率、明显提升正确率、修复普遍性 bug、用户明确要求长期保留、原 Skill 已明显过时。

过门后再看 §四 的触发条件（≥2 次同类任务 / ≥8 步可迁移 / 普适性坑 / 用户明说 / 已有 Skill 过时）：

- 同一类任务 **≥2 次**出现，或单次任务步骤 **≥8 步**且方法可迁移。
- 踩过坑且根因具有 **普适性**（不止本次有效）。
- 用户明确说「以后这类都按这个来」。
- 现有 Skill **已过时/描述失准** → **更新而非新建**。

**目标：经验越来越精，不是越来越多。** 沉淀后必须能回答「下次哪个任务会因此少一步」，答不出 = 不该沉淀。

沉淀方式：调用 `engineering/distill-cat` 产出技能包草稿 → `engineering/wb-skill-authoring` 审计（PyYAML 全解析、description≤1024、触发词只加末尾、首句<30字、无标点开头）→ 接线（写入相邻技能分工表/触发词）→ 同步仓库+live+push。

**禁止重复硬规则**：新建前必须先 `grep`/全局技能清单确认无同类；存在同类则合并或扩展，绝不平行新建。

## 五、工作流记忆写入规范（避免重复询问）

| 内容 | 落点 | 说明 |
|---|---|---|
| 用户习惯 / 常用操作 / 决策规则 | `~/.workbuddy/MEMORY.md`（跨项目）或项目 `MEMORY.md` | 长期偏好，显式写入 |
| 每日工作留痕 | `项目/.workbuddy/memory/YYYY-MM-DD.md` | 追加式，不覆盖 |
| 工作模板 / 可复用流程 | 独立 Skill（见 §四）或 `memory/` 参考文件 | 不塞进对话 |
| 跨 agent 共享身份/规则/交接 | `agent/agent-guild` | 纯本地 Markdown/JSON |

## 六、前置安全检查（执行前）

逐项过 `meta/personal-ai-os` §4–§8：

- 权限是否足够（L0 自动 / L1 提示 / L2 必须确认）。
- 是否涉及敏感操作（删文件、改注册表、发消息、付费、push）。
- 是否需要用户确认（不可逆/合规/安全风险 → 停手请示）。
- 是否可能造成错误（影响面、回滚点：`personal-ai-os` §5 先建状态与回滚点）。

安装/更新外部 Skill 前必跑 `system/skills-security-check`（纯静态审计，绝不执行被审脚本）。

## 七、后置安全检查（执行后）

- 文件是否正确生成/修改（独立读取核对）。
- 数据是否完整（无截断、无丢失、无部分写入）。
- 是否留下垃圾文件/缓存（`personal-ai-os` §17–§19：临时目录、缓存、垃圾清理规则）。
- 个人目录（Desktop/Downloads/Documents）**绝不**递归删/清空；只生成只读报告。

## 八、Skill 生命周期治理（保持精简）

定期（或每 N 次任务后）触发，复用既有技能：

- **创建**：仅 §四 判定通过，且全局无同类。
- **更新**：方法演进/触发词失效 → `wb-skill-authoring` 改 description/正文。
- **合并**：功能位重叠 → `wb-skill-authoring` 合并判据（同一功能位+触发词互覆盖才合并；市场/第三方只划边界不文件级合并）。
- **删除**：低价值/长期不用/被更好替代 → 经 `meta/knowledge-governance` 归档评估后删除；删除前先确认无依赖引用。
- **核心纪律**：数量随功能位伸缩，不为「变强」无脑堆量（见 `personal-ai-os` §36）。

## 九、多入口适配（统一收口）

所有入口都归一进 §二 主循环，不在入口侧各自实现逻辑：

- 微信/企业聊天消息 → 解析意图 → 进主循环。
- Windows 操作 / 文件处理 / 浏览器任务 / 自动化流程 → 路由到 `personal-ai-os` Computer Agent 与对应执行 Skill。
- 连接器（邮件/会议/网盘等）→ 取数据后归一为任务输入。

## 十、执行原则（常驻，不可被覆盖）

1. **少而精**：宁缺毋滥，一个功能位一个 Skill。
2. **优先复用**：能用现有 Skill 解决的，绝不新建。
3. **持续进化**：每次高价值任务必须考虑沉淀，但只沉淀真有价值的。
4. **结果导向**：Skill 必须提升实际效率，不产出「看起来很强」的无用资产。

## 十一、Hooks 五类型 + 自改进技能循环：必然行为进确定性触发，反思进 learnings（来源：Anthropic Claude Code hooks 文档，2026-09-27 r232 并发线手交 / WorkBuddy 实拉核验）

- **★"每次 X 自动做 Y"的必然行为必须进确定性触发（command / HTTP / mcp_tool），不能靠提示词叮嘱**：hooks 五类型里 command/HTTP/mcp_tool 是确定性触发（发生 X 就跑，不经过模型判断）；prompt / agent 才用模型判断。判据：**凡是你希望"百分百发生"的动作，写进 hook 而不是写进 system prompt**——提示词会被忽略、会被长上下文稀释，hook 不会。
- **★PreToolUse 退出码 2 = 阻断工具执行、0 = 放行**：用退出码表达"这个工具调用该不该发生"，比事后纠错便宜得多；Git 安全网（block force push / hard reset）是单条最值得装的 hook（对应本仓库 §Git 红线：禁强推）。
- **★自改进技能循环 = reflection hook（技能调用后评估有没有帮上忙，没帮上就建议编辑 SKILL.md）+ reflections 存 learnings 文件下次加载读**：不靠人手动复盘，技能自己记录"这次用得好不好"并建议改进。判据：**技能进化不该等人来推，调用后的反思要自动沉淀成下次加载能读的东西**。
- 与 §十 执行原则（少而精/优先复用/持续进化）的分工：那条管"要不要沉淀"的价值观；本条管"**怎么让沉淀自动发生、且必然行为不靠叮嘱**"。
- 提升层：可复用 Skill / 工作流。

## 十一、策展与执行器是一对耦合件：换执行器即退化，须在线行为画像 + 时间归因（来源：arXiv 2609.36746《EASE: Behavior-Adaptive Skill Curation》，2026-10-02 r350A 实拉 42,298B）

- **★技能策展（curation）是执行器依赖的**：用不同执行器训练出来的策展器，各自只在自己那个训练执行器上最好——换执行器就系统性退化。判据：**"沉淀什么技能"的决策质量不能脱离"谁来用这些技能"评估**；策展器与执行器要成对看，不能只优化策展侧。
- **★对策 = 单策展器 + 在线行为画像**：维护近期执行模式的在线行为画像，把策展条件化在「画像 + 当前轨迹 + 检索到的技能」三者上，再决定 add / modify / remove。判据：**策展输入必须含执行器行为画像，只有轨迹和技能库不够**。
- **★优化信号用检索感知 + 行为感知的时间归因**：只对"能被下游观测到影响"的策展动作分配优化权重，其余不归因。判据：**技能库改动要有可归因的下游影响，否则 RL/反馈信号是噪声**。
- **★"少而精"是可测指标不是口号**（EASE 跨 ALFWorld/ScienceWorld/WebShop、执行器 Qwen3-8B/32B、GPT-OSS-120B 到未见 Kimi K2.6 / DeepSeek V4 Flash / Gemini 3.5 Flash）：技能数 **−34.5–41.0%**、技能检索 **+36.3–38.7%**、编辑效用 **+51.8–60.0%**、部署期推理 token **−9.1–14.5%**。判据：**技能库变小 + 检索变准 + 效用变高应该同时发生**；只涨数量不涨检索命中 = 堆量不是进化。
- 与 §十 执行原则的分工：那条给价值观（少而精/优先复用），本条给度量口径与耦合约束。
- 提升层：可复用 Skill / 工作流。

## 十二、反思式自我改进：Reflexion / Self-Refine（不改权重，靠"说"变强）

> 来源 2026-11-07 实拉：morphllm.com/self-improving-ai（Reflexion/SEAL/边界）、zooz.com（自改进五步环）。

- **Reflexion（Princeton）**：任务失败后，agent 用自然语言写一段**自我批判**存进情节缓冲；下次同类任务先读这条反思再决策。**不改模型参数**，靠"言语反思"提升（HumanEval 通过率显著提升）。判据：失败 → 必须先产出"为什么错 + 下次怎么改"的可用反思，不是重试。
- **Self-Refine**：同一轮内 self-critique → revise 迭代，直到自评达标或触上限。
- **纯提示优化 vs 权重自改进的边界（重要）**：Reflexion / Self-Refine / GEPA / DSPy 只改**提示与系统组织**，不改权重——快、可逆、安全；SEAL / Self-Rewarding LM 改权重——能力更深但慢、贵、难回滚。**"什么真正有效"= 有界优化环**（把提示改好），不是递归自我进化（真正"改自己改进能力"的系统尚未落地）。
- **安全护栏（实拉）**：对高影响自改进加分层审批 + 置信度触发更新 + 失败回退到安全基线 + 结构化 self-critique 管线；反思必须回写长期文件（learnings/skill/memory），留在会话里 = 下轮必犯。

## 十三、提示进化优化：GEPA / DSPy（把"改提示"变成可优化问题）

> 来源 2026-11-07 实拉：morphllm.com（GEPA ICLR 2026 Oral, arXiv 2507.19457；超 GRPO ~10%/最多 20%、用 ≤35× 更少 rollout、超 MIPROv2 10%+）、cioage.com（六步算法/反馈函数）、zooz.com（概念框架）。

- **GEPA 核心 = 反思式提示进化（Genetic-Pareto）**：采样执行轨迹 → 用**自然语言诊断失败**（不是只看标量分）→ 沿 Pareto 前沿交叉/变异生成新提示 → 在同样本上重跑，更好才接受。
- **六步循环**：① 从候选提示种群选父代 → ② 选要变异的模块（模块间轮转）→ ③ 抽少量样本（如 3 个）→ ④ rollout 收集完整轨迹 + 反馈函数输出 → ⑤ 反思 LLM 读轨迹+反馈生成新提示 → ⑥ 同样本重跑，更好接受否则拒绝；循环到预算耗尽取最优。
- **反馈函数 = 分数 + 自然语言说明**（关键）：越具体越有用（多跳问答点出缺哪个 gold doc、代码返回编译/测试错、改写点出质量问题+PII）；只给"错了"就退化成标量优化。
- **DSPy**：把提示当可编程模块，用优化器（MIPROv2 等）按指标自动调。
- **能力天花板（必须诚实）**：GEPA **不能让模型获得它本不会的新能力**——只能把已有能力"问出来 / 组织好"；基础模型根本不会的，仍需微调。
- **判据**：技能/流程改完后，用"丢样本 + 自然语言诊断 + 重测接受/拒绝"闭环，而不是凭感觉改 description；改动要有可归因的下游效果（接 §十一 EASE 时间归因）。

## 十四、分层自改进与成熟度阶梯（来源：pzsr.cn / safeguard.sh / exzilcalanza.info / CSDN，2026-11-07 实拉）

**四层自改进机制（由轻到重）**：
1. **反思报告层**：任务后评估器（同/更强/更便宜模型均可）输出结构化反思（目标/结果/好点固化/失败原因/下次怎么做）→ 写入知识库 → 下次检索注入。改动最小，已能规避大量重复错误。
2. **经验记忆与技能库层**：成功流程固化为可复用、可组合、可检索的能力单元（触发条件/输入输出/步骤/错误处理）；**新技能入库前必须验证**，防把错误流程固化（Voyager 模式）。
3. **元级策略调整层**：调整"系统本身的工作方式"（默认启用某模式/自动换备用工具/改拆解粒度/调检索参数）。**安全落法：元层只生成"策略修改建议"，人确认后才生效**，积累足够样本再逐步放开自动化。
4. **自编辑层**（最高风险）：改自身脚手架/代码，必须 benchmark 验证 + 治理门，只适合离线研究或严控流水线。

**记忆成熟度五级阶梯**：Stateless（每次都是陌生聪明人）→ Session（会话内）→ Persistent（事实存取，手动调优）→ **Experiential（蒸馏经验+技能，带评审闭环）** → Self-editing（治理+可审计的自改）。目标级 = Experiential；往上必须带治理。

**Voyager 消融教训（量化）**：去掉自验证 → 发现项 **-73%**（最重要反馈信号）；自动课程换随机 → **-93%**；无技能库 → 后期停滞。**技能=未评审代码**，自验证会误判成功、课程会提议不存在的东西——入库走 §13 六步+人工门。

**Generative Agents 记忆流三因子（打分取用）**：Recency（指数衰减 0.995）+ Importance（1-10 创建时打分）+ Relevance（嵌入余弦）；近期重要性累计过阈值（150）触发反思——回答"最近经验说明什么高层问题"，产出带指针的抽象结论，可再反思形成信念树。

**治理铁律**：没有仪表化的自改进 = 无监督漂移（unsupervised drift）。谁能写记忆/冲突谁赢/如何审计，三问不答就不许升 Self-editing；kill switch / 审计链 / 第二意见不是摩擦，是系统能被允许自主的前提。

## 十五、自适应的「何时改」与「改完怎么算好」：漂移门 + 对照验收（2026-11-08 r706A 实拉）

> 与 §十一 EASE（策展输入须含执行器行为画像）、§十三 GEPA（同样本重跑、更好才接受）分工：那两条管「拿什么决定改」与「改完要不要接受」；本节管**触发时机**（策略何时被判定失效）与**验收对照实验怎么搭**（什么比较才算有效证据）。§十四 治理铁律只说"无仪表化即漂移"，本节给仪表本身。

### 15.1 触发门：把「该改了」做成单变量变点检测

- **ADWIN** 保持变长窗口，切成 W0/W1 两子窗比均值；同分布假设不成立即报漂移，随后 `W0 ← W1` 并初始化新 W1 ⇒ **旧数据自动出窗，无需人工决定忘掉多少历史**。
- **★监控性能指标，不监控原始数据**：River 原文 "Drift detectors monitor the model usually through a performance metric"、"Drift detectors work on univariate data. This is why they are used to monitor a model's performance and not the data itself"。对 Agent：喂 0/1（本轮做对/做错）或单一质量分，**不要把整段上下文塞进检测器**。
- **检测器对输入有期望**（"define their expectations regarding input data. It is important to know these expectations to feed a given drift detector with the correct data"）⇒ 换监控指标必须重标阈值，照搬别处的 δ 无效。
- **参数即「灵敏度 vs 误报」的显式权衡**（River dev 文档）：`delta=0.002`（显著性）、`clock=32`（每 32 点查一次，越大越省算力但检测延迟增加）、`min_window_length=5`（越小延迟越低、误报越多）、`grace_period=10`（不足 10 点不检测）。⇒ **自改进不能一有波动就改策略**，先定最小观察窗与误报预算。
- 检测后 `reset()` 是官方示例里的好习惯 ⇒ 报一次漂移 = 一次有界状态重置，不是持续报警。

### 15.2 分清漂移类型，避免「环境变了就重写策略」

- **虚拟漂移**：只有 P(X) 变、X→y 关系不变 ⇒ 输入分布变了但既有策略仍有效，**不改策略**（只更新触发词/描述）。
- **真实漂移**：P(X,y) 变 ⇒ 策略与目标的关系失效，才触发改写；再分 **abrupt**（立即切换）与 **gradual**（需累积证据）。
- 判据：**「最近题目不一样了」不等于「方法不行了」**。混为一谈会洗掉仍有效的经验，是 §十一 EASE「换执行器即退化」之外的另一类自伤。

### 15.3 验收门：与同时部署的等价基线比，不与历史成绩比

- **★基线必须同时部署**：Spinnaker 逐字 "always compare the canary against an equivalent baseline, deployed at the same time"——基线用当前生产同版本同配置、同时部署、同规模、同流量，只留「版本/配置」一个变量，排除缓存预热/堆大小等混淆。⇒ 策略 A/B 必须**同一批任务、同时段**跑新旧两版；拿上周成绩当对照无效。
- **★关键指标一票否决**：`critical: true` 使该指标被判 High/Low 时整个 canary 直接 `score = 0`，"regardless of group scores"；或把关键指标单独成组。⇒ 安全/合规类指标**不参与加权平均**，不能被一堆变好的指标掩盖（"Don't put too many metrics in one group"）。
- **双阈值**：`marginal`（任一 run 低于即整体立即失败）与 `pass`（最终 run 必须 ≥，比较含等号）；官方起点 **75 / 95**。⇒ 既要「过程中没崩」也要「终态达标」，只看终分会把中途劣化放过。
- **样本量下限**：每指标至少 **50 个时序点**才有统计效力（官方起点 3 小时 × 3 run）。⇒ 小样本试跑的「变好了」不构成验收证据。
- **缺数据 ≠ 通过**：judge 对 NaN 有 `remove`/`replace` 与 `Nodata`/`NodataFailMetric`/`Pass` 分类，`mustHaveData: true` 让缺数据计为失败；仅误差类指标适合 `replace`（无数据=零错误）。⇒ 验收里「这项没采到」必须与「这项通过」分开记账。
- **判定要同时过统计显著与效应量**：Mann-Whitney U 非参数检验 + 98% 置信 + `allowedIncrease/allowedDecrease` 效应阈值 + ±(0.25×|Hodges-Lehmann|) 容差死区；离群用降敏 IQR 剔除。⇒ 微小但显著的差异不该触发策略切换。
- **验收门自身可低成本迭代**：用 `retrospective analysis` 拿历史监控数据回放调配置，不必等实时数据攒够。

### 15.4 落地清单（自改进策略换版四步）

1. 定单一监控指标（0/1 或质量分）+ 最小观察窗 + 误报预算，才允许自动触发改写。
2. 触发后先判虚拟/真实漂移；虚拟只更新描述，不动策略。
3. 改写版与**同时部署的等价基线**同批任务对照跑，安全指标一票否决，样本 ≥50，缺数据单独记。
4. 过 marginal + pass 双阈值才接受；否则回滚基线并留痕（接 §十四 kill switch / 审计链）。

### 15.5 来源（2026-11-08 r706A 实拉，逐字核验）

- riverml.xyz/latest/introduction/getting-started/concept-drift-detection（虚拟/真实漂移、abrupt/gradual、监控性能指标、单变量、输入期望；WebFetch 全文）
- riverml.xyz/0.11.0/api/drift/ADWIN · /dev/api/drift/ADWIN/ · /0.15.0/api/drift/ADWIN/（W0/W1 切分、检测后 W0←W1、delta=0.002 / clock=32 / min_window_length=5 / grace_period=10 / reset；Bifet & Gavalda 2007 SIAM SDM）
- spinnaker.io/guides/user/canary/best-practices/（baseline not production、critical: true、marginal 75 / pass 95、≥50 data points、retrospective analysis；WebFetch 逐字）
- spinnaker.io/docs/guides/user/canary/judge/（NaN 策略与 Nodata 分类、Mann-Whitney U 98%、效应量阈值、HL 容差死区、IQR 离群）
- spinnaker.io/docs/guides/user/canary/canary-overview/ · /config/canary-config/（基线对照、指标分组与权重）
- 判非：BS 分解三病灶、验收六要素等已在本仓 `engineering/*` 与 `meta/pdi-forecasting` §六，本轮不重复落。

## 十六、自适应的探索-利用门：别把「在线自适应」和「确认谁更好」混成一种实验（2026-11-08 r717A 实拉）

> 与 §十五 分工：§15.1 ADWIN 管「何时判定策略失效」，§15.3 管「改完与同时部署的等价基线比」；本节管**改之前那笔探索预算怎么花**，以及**哪种实验目标该用哪种分配**。两节合起来覆盖「触发→探索→验收」全链。

### 16.1 ★目标函数分裂：regret 最小化 ≠ 估计方差最小化
- dswok 逐字："Bandits minimize cumulative regret during learning: the loss from not picking the best arm on each round. A/B tests minimize estimation variance on a specific contrast: the uncertainty about which arm is best after a fixed sample."；"Use A/B when a clean ship/kill decision matters more than regret during the decision period."
- 同一页收口："Bandits are not a substitute for a well-designed A/B test when the goal is a confirmed causal effect estimate for a specific contrast."
- ⇒ **策略改版验收（§15.3 要干净的 ship/kill 判定）与在线流量自适应是两种不同实验，禁止混用**：要「确认的因果效应估计」必须固定分配；拿自适应分配的数据去签「新版更好」的验收证书，会被流量分配本身污染。DataExpertise 逐字："Standard A/B testing is epsilon-greedy with ε = 0.5 ... which is optimal for hypothesis testing but suboptimal for regret minimisation because it never increases allocation to the better-performing variant during the test." ⇒ 反过来也成立：为省 regret 而动态调流量，就放弃了假设检验的最优性。先声明目标，再选分配。

### 16.2 ★探索预算按不确定性分配，恒定随机试＝永不学习
- DataExpertise 逐字：ε-greedy "explores uniformly — it is equally likely to explore the arm that has been pulled 5 times and the arm that has been pulled 500 times — wasting exploration budget on well-characterised arms"；UCB1 用 `argmax_k [x̄_k + sqrt(2 log t / n_k)]` 让少拉的臂自动拿到探索奖励，Thompson 用后验采样；两者 `O(K log T)`，ε-greedy 固定速率是线性 regret。
- Vitor Sousa 逐字："Linear regret R(T) = Θ(T) would mean we're making a constant mistake forever—we never learn."；判定标准是**次线性** "R(T)=o(T)"，即平均每轮 regret 趋 0。其 10,000 轮数值：linear ~10,000 / ε-greedy ~464 / UCB ~130 / Thompson ~100；LinUCB `O(d√(T log T))` 为维度付 √d 代价。
- ⇒ 自改进不能「每次固定拿 10% 任务随机试新写法」——那是恒定 ε、线性 regret。探索额度应随候选已被验证的次数衰减（UCB 的 n_k 项 / Thompson 后验收窄），并把「候选池的累积遗憾是否次线性」当作进化引擎是否真在学习的体检指标。Lai & Robbins 下界 `Ω(log T)` 提醒：**不确定性下的学习有不可消除的成本**，不存在零代价探索。

### 16.3 三个让朴素自适应失效的现实条件（归因窗口 / 漂移 / 相关候选）
- dswok "Common pitfalls" 逐字：① "Delayed rewards break naive bandit algorithms. Attribution windows must be modeled explicitly, or credit lands on the wrong arm."；② "Non-stationary reward distributions invalidate the regret bounds. Sliding-window or discounted-reward variants handle drift."；③ "Correlated arms (shared features, similar content) mean independent bandits waste data. Contextual bandits share statistical strength across arms with similar context."
- Vitor Sousa 的**部分反馈**："We only observe rewards for actions we take ... we never know what would have happened if we'd chosen differently (the counterfactual outcome)." ⇒ 只跑一个候选就永远没有反事实对照，这与 §15.3「同时部署等价基线」是同源要求。
- ⇒ 落到 Agent 自改进：任务结果常**延迟**（收尾才有 0/1 成败），必须先显式定「哪一段反馈归属于哪一版策略」的归因窗口，否则把上一版的成果记到新版头上；环境非平稳时（接 §15.2 真实漂移）regret 界失效，改用滑窗/折扣计数而非继续按原界验收；同源候选（同一提示词的多个改写）应按 context 共享统计强度，别为每份变体从零攒样本。
- 判非：§15.1 漂移门、§15.3 基线对照与双阈值、§十三 GEPA「同样本重跑更好才接受」均不重复落地；本轮只补「探索侧」与「实验目标分叉」。

### 16.4 来源（2026-11-08 r717A 实拉，逐字核验，三独立域交叉）

- dswok.com/General-ML/Multi-armed-bandits（2026-07-31；"Regret vs estimation" 两目标分叉、"Common pitfalls" 延迟奖励/非平稳/相关臂、bandit 非 A/B 替代、ε-greedy 线性 regret；WebFetch 全文逐字）
- www.dataexpertise.in/multi-armed-bandits-online-learning-thompson-sampling-explore-exploit/（2026-10 前后；ε-greedy 均匀探索浪费、UCB1 公式 `sqrt(2 log t / n_k)`、`O(K log T)`、A/B=ε=0.5 固定分配、FTRL/Vowpal Wabbit 在线学习；WebFetch 全文逐字）
- www.vitorsousa.com/blog/contextual-bandits-math（2025-11-15；regret 界表 ε O(T^2/3) / UCB O(√(T log T)) / TS O(√T) / LinUCB O(d√(T log T))、10,000 轮 10000/464/130/100、partial feedback 反事实不可观测、`R(T)=o(T)` 次线性、Lai-Robbins Ω(log T) 下界、LinUCB α=0.1–2.0；WebFetch 全文逐字）
- 判非：`UCB` / `LinUCB` / `epsilon-greedy` / `部分反馈` / `延迟奖励` 全库词边界 0 命中；`bandit` 命中均在豆包自留地 `defaults/wb-context-compressor/references/knowledge-base.md`（测试时算力缩放 / shadow-first bandit），与 regret 理论、探索预算分配无关，不重复；`Thompson` 命中仅为同 KB 的路由实验，不同维度。豆包自留地 WB 0 落地。

## r733C · 离线策略评估的前提、方差与灰度边界（来源：2026-11-11 r733C 本轮独立实拉，≥2 独立域一手交叉）

> 模块：AI｜二轮深化第 4 批｜本轮定位：AI 3926B/6 条（第三薄、主技能数仅 1）

### r733C-1 ★倾向性概率是离线评估的前提：日志 schema 漏一个字段，就永久失去「用历史证明新版更好」这条路

neuralmasteryai 逐字："A bandit in production logs every decision: the context, the arm shown, the reward, and the probability with which the logging policy chose that arm"；"That last number makes it possible to estimate how a different policy would have done, without deploying it"；更硬的限定 "Store the probability of the chosen action with every logged decision. Without it, off-policy evaluation is impossible and every new policy has to be tested live with an A/B test."。PracHub 逐字 "Logged propensities are mandatory for IPS/SNIPS; without them, estimates can be arbitrarily biased"。GeekChamp 给出完整字段链："Log complete decisions: timestamp, context, candidates, chosen action, policy ID, propensity, reward definition, reward timestamp, and model version"，并须 "Verify propensities were recorded before action selection"。判据：① 策略/提示词/Skill 改版前先查历史日志是否带 propensity + 候选集 + 策略版本 + 奖励定义与时间戳；缺任一则该批日志**不可**用来签「新版更好」，只能退回 §15.3 同时部署等价基线；② 日志 schema 是决策能力的前提而非可后补的运维细节——记录时没写就永久丢失反事实，事后补造等于伪造证据（与 agent-guild Cap31 审计不补造同源）；③ 与 §16.3「未选中动作的反事实收益永不观测」互补：那条陈述限制，本条给出唯一可绕过的条件（记录 propensity 后用 IPS 加权估计）；④ "No single library supplies the difficult operational pieces automatically" ⇒ 不能指望框架自带这套日志。

### r733C-2 ★IPS 无偏但高方差，权重尾部主导结论；旧策略没试过的动作得到的是「假 0」而非「差」

neuralmasteryai 逐字："Inverse propensity scoring (IPS) reweights each logged round by πnew(a|x)/πlog(a|x): rounds where the old policy chose what the new one would choose count more, the rarer the old policy made that choice"；数值例：旧策略 article0 占 0.90、其余各 0.05，评估「总出 article1」只能用其中 2,482 轮、每轮权重 20，估 0.055 而真值 0.060；"The variance comes from those large weights, and it is why logging policies keep some exploration: an arm the old policy never shows can never be evaluated"；代码注释逐字 "set eps = 0.0. Article 1 is never logged, every weight is zero, and IPS estimates 0: you cannot evaluate an action the old policy never took"。PracHub 逐字："Self-normalized IPS (SNIPS) reduces variance but introduces small bias; watch tail weights"；"Candidates often quote a single metric (e.g., IPS uplift) without checking weight distribution or support mismatch. If a few impressions carry huge weights, your estimate is fragile—show diagnostics: effective sample size, clipping analyses, and sensitivity to propensity misspecification"；"Direct Method, IPS, and Doubly Robust trade bias–variance; DR helps when either model or propensities are imperfect"。判据：① 报离线提升必须同时报权重分布 / 有效样本量 / 裁剪敏感性 / propensity 误设敏感性，单报一个 uplift 数字不可采信；② 支持集条件（positivity）不满足时，估计值 0 是**不可估**不是**效果为零**，禁止据此淘汰候选；③ 与 §16.2「探索预算按不确定性衰减」呼应但不同层：那条管在线 regret 最优化，本条管离线评估的可行性边界——ε=0 的纯贪心历史日志虽然在线看着省，却把整条离线评估路径关掉了。

### r733C-3 ★离线结论只能排在灰度之前：三段验收链不可跳，且离线分本身有四类污染源

PracHub 逐字："Another miss is jumping straight to a 50% A/B after 'good' offline results. Strong answers pair OPE with high-confidence bounds, then propose a guardrailed ramp with pre-defined stop criteria on core metrics and safety checks for long-tail cohorts"；"Confidence intervals matter: bootstrap, concentration bounds, or HCOPE for safety guarantees"；"Safe policy improvement (e.g., SPIBB) constrains changes where data are uncertain"；"Rollout tactics: canaries, shadow serving, interleaving, staged ramps, automatic kill-switches"。GeekChamp 逐字："Offline results should precede a staged rollout, not replace a holdout, guardrails, and rollback plan." ⇒ 验收链三段不可跳：**离线过滤（带置信下界）→ 小流量灰度（预置停止条件 + 长尾子群检查）→ 全量**；「离线更好」不构成发布证据。四类污染逐字："Leakage: a feature or label unavailable at decision time makes offline results unrealistically strong"；"Delayed attribution: ... require a clear link to the original action and treatment of censored outcomes"；"Perverse incentives: a policy can improve a target metric while harming users or another business objective"；"Changing scale: seasonality, inflation, traffic mix, or reward-definition changes break comparisons across time"；并要求 "Track guardrails such as complaints, bounce rate, latency, safety violations, fairness measures, and long-term retention alongside the optimized reward"。判据：① 报离线结论前逐项排除四类污染，尤其决策时不可得特征与奖励定义漂移；② 优化目标之外必须同报护栏指标，防止代理指标反激励；③ 与 §15.3 灰度双阈值 / critical:true 分工：那条给灰度内部怎么判，本条补灰度之前那道离线门与灰度之后那道护栏/回滚门；④ 与 §16.1「bandit 与 A/B 目标互斥」不冲突——本条谈的是验收链形状，不是流量分配的目标函数。

**提升层**：可复用 Skill（AI 模块方法论）/ 工作流（决策或编排的验收链）。

### r733C 来源与判非

- neuralmasteryai《Multi-Armed & Contextual Bandits》→ https://neuralmasteryai.com/docs/reinforcement-learning/bandits（WebFetch 200 全文逐字，含可运行 IPS 代码与数值例，2026-11-11）
- PracHub《Off-Policy Evaluation and Safe Rollouts》Last updated 2026-04-25 → https://prachub.com/concepts/off-policy-evaluation-and-safe-rollouts（WebFetch 200 全文逐字）
- GeekChamp《Contextual Multi-Armed Bandits: Algorithms, Evaluation, and Deployment》2026-10-01 → https://geekchamp.com/contextual-multi-armed-bandits-in-reinforcement-learning-algorithms-evaluation-and-deployment/（WebFetch 200 全文逐字；页面含广告插入，如实登记）
- 辅助交叉（WebSearch 快照）：inferensys.com/glossary/.../off-policy-evaluation（五类估计器偏差—方差）、lacuna.tiptreesystems.com/.../overcoming-support-deficiency-in-off-policy-evaluation（common support / positivity 定义）。
- 判非：`off-policy` 唯一命中在豆包自留地 `wb-execute-discipline`；`propensity` / `SNIPS` / `doubly robust` / `effective sample size` 全库 0 命中；豆包自留地 WB 0 落地。

- 窄串 `propensity` / `SNIPS` / `doubly robust` / `effective sample size` / `support deficiency` 全库 SKILL.md **0 命中**；`off-policy` 仅 1 命中，位于豆包自留地 `wb-execute-discipline`（语义为在线策略/离线评估的泛提及，无 IPS / 倾向性 / 支持集机制）；`IPS` 亦无本义命中 ⇒ 净新。
- 既有 §15（漂移门 / 基线对照 / 双阈值）与 §16（bandit vs A/B / 探索预算 / 三失效条件）全部落在**在线改与在线验收**；本轮三点是**不部署能否评估、日志要记什么、离线与灰度的先后**，属不同层，结论不复用。
- 豆包自留地 0 落地；A 轮 OI、B 轮 DI 结论一律不复用；r732/r731/r717/r715 各轮结论不复用。
- 换道：Vowpal Wabbit 命令参数族、逐估计器公式推导属易漂移工具细节，只取可迁移判据不作落地；GeekChamp 页面含 Outbyte 广告插入、PracHub 为面试向内容站，均如实登记立场，结论一律与 neuralmasteryai 的可运行代码/数值例交叉后才采纳。


## 十七、序贯检验与随时有效推断（2026-11-11 r737B 实拉，≥2 独立域一手交叉）

### r737B-1 ★固定视界检验只允许「读一次」，边跑边看边改=假阳性膨胀

t/z 检验的 α 只在预设样本量那一次成立（Statsig 逐字「you read the metrics once, after you reach that target sample size」）；连续监控每次提前决策都是一次额外的拒绝机会，指标与 p 值随噪声进出显著区，「early decisions can only increase the false positive rate, even when you intend to make a less biased decision」。⇒ 自适应策略「看到提升就改版」若没有 anytime-valid 推断，等于把噪声峰固化成策略改进；验收协议必须先写明「读数时刻是预设一次，还是允许的监控节奏」。

### r737B-2 ★随时有效是可报价的交易，不是免费的停止权

mSPRT 以 Λ_t>1/α 保证「probability of ever falsely rejecting ≤α, regardless of how many times you inspect」；置信序列要求 P(∀t: θ∈C_t)≥1−α 同时覆盖所有时刻，代价是区间更宽（Adobe 逐字「更保守」「界限通常比信賴區間計算更寬」；MetricGate 典型比 1.1–1.5、小样本实例 5.065）且小效应需多 20–40% 观测才达同等 power。⇒ 「能随时停」必须用更宽区间 + 更多样本换；τ 必须**实验前**固定（事后按数据调 τ 抬 I 类错误）；结论报最终置信序列而非二元拒绝，「Do not lower alpha post hoc」。与 §16.2 分工：那条管探索预算怎么分配，本条管停止时刻的统计有效性。

### r737B-3 ★随时有效只管停止时刻，不管设计缺陷、多指标与效应量精度

mSPRT 不控制跨指标 family-wise error（Adobe 对两个以上处理用 Bonferroni 补）；早停显著「doesn't guarantee enough power to detect regressions in other metrics」；早停给的是欠功效的 lift 估计，要准确效应量必须等满预设 power；anytime-valid 修不了非随机分配、错误分母、曝光错配、SRM、指标切换、结果成熟度不足（ABLabz 逐字），更不能用 1 日转化的序列宣称 30 日留存。⇒ 越过停止边界前先过数据质量门（SRM / 曝光日志 / 身份变更 / 事件完整性），快速安全监控与长期有效性指标拆成两套具名程序；与 §17 分工：那条管离线过滤→灰度→全量的部署链，本条管读数链的停止规则。

**提升层**：PI 输入保真 / AI 验收协议 / PDI 结算台账（按轮）。触发词：peeking、fixed horizon、always-valid、confidence sequence、mSPRT、1/α、τ 事先固定、family-wise error、早停效应量。

### r737B 来源与判非（逐字核验）

- `docs.statsig.com/experiments/advanced-setup/sequential-testing`（Statsig 官方，WebFetch 200 全文逐字）：「Traditional A/B tests (t-tests and z-tests) are fixed-horizon tests. When you design the experiment, you set the number of units to observe, and you read the metrics once, after you reach that target sample size.」；「Continuous monitoring of an experiment, or peeking, inflates the false positive rate above the significance level you chose.」；「In frequentist procedures, early decisions can only increase the false positive rate, even when you intend to make a less biased decision.」；「an early significant result on some metrics doesn't guarantee enough power to detect regressions in other metrics」；「Early decisions often produce underpowered lift estimates with high uncertainty … If you need an accurate measurement of the effect size, wait for the full power」；mSPRT 用 Zhao et al. arXiv 1905.10493，逐字展开 Z*_{α/2}、τ、σ 与 p-value* 公式。**一手官方全文逐字**
- `experienceleague.adobe.com/zh-hant/docs/journey-optimizer/.../experiment-calculations`（Adobe 官方，最后更新 2026-10-08，WebFetch 200 全文逐字）：「信賴序列是信賴區間的循序類比」「每個實驗只能計算一次95%信賴區間，以提供相同的95%覆蓋率保證；而不是針對每個新使用者」「信賴序列可讓您持續監視實驗，而不會增加『誤判為真』的錯誤率」；「有了信賴序列，您可以隨時檢視和解讀實驗中的資料，並安全地停止或繼續實驗」；「信賴序列會比固定水平線方法更保守。信賴序列的界限通常比信賴區間計算更寬」；两个以上处理「Bonferroni 更正…控制以系列為基礎的錯誤率」；「統計顯著性…不是成功的可能性」。**一手官方中文全文逐字（第二独立域）**
- `metricgate.com/docs/sequential-testing-always-valid/`（WebFetch 200 全文逐字）：「A confidence sequence is a sequence of intervals such that with probability at least 1 − alpha, every interval simultaneously covers the true parameter.」；mSPRT「Reject when Λ_t > 1/α. This threshold guarantees that the probability of ever falsely rejecting is at most alpha, regardless of how many times you inspect the data.」；「The ratio of confidence sequence width to fixed-horizon interval width typically falls between 1.1 and 1.5 at the planned sample size」（mtcars 实例 5.065）；Limitations 逐字「require 20 to 40 percent more observations」「Tau must be chosen before the experiment; tuning it to observed data inflates type I error」「The mSPRT does not control family-wise error across multiple metrics」；「Do not lower alpha post hoc」「Report the final confidence sequence as the summary of evidence rather than a binary decision」。**工具文档一手逐字（第三独立域）**
- `ab-labz.com/glossary/experiment-design/always-valid-inference`（WebSearch 快照逐字）：「P_H0(there exists t such that p_t ≤ α) ≤ α」「It is stronger than saying P(p_T ≤ α) ≤ α for one fixed, preselected T」；「'Always valid' does not mean always useful, always precise, or immune to bad experimentation」；「It does not fix nonrandom assignment, an incorrect denominator, users exposed to the wrong experience, interference, metric switching」；「Inspect sample ratio mismatch, exposure logging, identity changes, and event completeness before acting on a boundary」「Continuous monitoring can quickly detect harm, but it can also quickly act on a tracking outage」；「A confidence sequence for one-day conversion cannot justify a claim about 30-day retention」。**独立术语站交叉（含实验设计前置清单）**

- **判非**：窄串词边界全库 SKILL.md：`peeking` / `always-valid` / `confidence sequence` / `mSPRT` / `family-wise` **全 0 命中**；`Bonferroni` 唯一命中在 `research/wb-experiment-design`（一般多重比较校正，无 anytime-valid 机制）；`bootstrap` 10 命中均为重采样取区间，无停止规则语义。与既有三节正交：§15 管「何时改（漂移门）」、§16 管「流量怎么分配（bandit vs A/B）」、r733C §十七 管「不部署怎么评估（OPE）」；本轮管「何时可以停」。豆包自留地 WB 0 落地。
- **换道/未采纳**：换道：Statsig 的 Z*_{α/2} / τ / σ 闭式解、MetricGate 的 mtcars 具体数值属厂商实现细节，只取可迁移判据不作公式搬运；Adobe 的「宣告实验为有结论」产品行为不搬；r735A 的 SRM 已由 VI 模块落地，本轮仅把它列为数据质量门的一项，不重复立论。A/C 两轮结论一律不复用。

## 十八、自改进闭环会改写自己的评估分布：反复重训收敛到的未必是最优（2026-11-14 r741C 实拉，≥2 独立域一手交叉）

> 与既有各节分工：§15 管「何时改」（单变量变点/漂移类型）、§16 管「探索-利用流量分配」、r733C 管「不部署怎么评估（OPE 的 propensity/IPS/灰度链）」、§17 管「何时可以停（anytime-valid）」。本节管一个更前置的问题：**策略本身就是数据生成器，改版会改变被评估的分布**，因此「拿旧数据评新版」「一直重训到不动」这两条默认做法都不成立。

### r741C-1 ★分布随策略参数变，不是外部漂移：D(θ) 取代固定 D
- **原文**（TOC for Fairness，作者 Tijana Zrnic 2021-05-06 一手）：「In supervised learning, the decision-maker observes pairs … drawn from a *fixed* distribution. The key difference in performative prediction is that there is **no longer an unknown static distribution generating observations**; rather, data is drawn from a **model-dependent distribution**」；「performative distribution shift is **not due to external factors independent of the model** … Rather, the distribution shift is **triggered directly by the choice of predictive model**」。两个反向实例：预测性警务是 self-fulfilling（加强巡逻→记录到的犯罪更多），ETA 是 self-negating（预报低→都走那条→真的堵）。Berkeley 论文逐字：Twitter 排序「If the model predicts a user is unlikely to engage with a tweet, **they will never observe that piece of content, and hence never click on it**」；Google ETA「drivers will be more likely to choose it, hence increasing traffic on this route and **altering the true travel time**」，且两者都「continuously trained on historical datasets … **These datasets were themselves influenced by predictions generated by historical models**」。
- **判据**：自改进闭环启动前先判「这次改版会不会改变被观测数据的生成方式」（曝光位次、路由、阈值、谁被采样）。会 ⇒ 旧日志是**旧策略诱导的 D(θ_old)**，拿它当新版真值等于用旧策略的盲区评分（与 §15.2 的虚拟/真实漂移分工：那条管环境自己变，本条管**策略自己把环境变了**）。验收台账固定记录「本批数据由哪个 θ 生成」，跨版本数据不得混池当作同一分布比较；自证指标要区分 self-fulfilling 与 self-negating 两个方向，不能一律读作「预测变准了」。

### r741C-2 ★反复重训收敛到稳定点，稳定 ≠ 最优；稳定点可能是自己造出来的坏世界
- **原文**：「We call a model that satisfies the fixed-point equation above **performatively stable**. Performative stability arises naturally when the decision-maker applies the heuristic of **myopically updating the model based on the distribution resulting from the previous deployment**」；「If this retraining strategy converges, then it **necessarily converges to a performatively stable solution** … **stability eliminates the need for retraining**」。博弈论对应逐字：「a performatively **stable** solution corresponds to a **Nash** equilibrium, while a performatively **optimal** solution corresponds to a **Stackelberg** equilibrium」；「Only in special cases, such as in well-behaved zero-sum games … **performative prediction is typically not a zero-sum game** … **stable solutions and performative optima can be very different**」；「**naive retraining strategies only converge to stability … myopic updates can be an inadequate method**」。Lacuna 方向综述补一个更硬的失效形态：一个**校准良好**的预测器可以「accurately predict a negative social outcome that it helped create」，稳定而自觉地维持坏状态。
- **判据**：把「重训到不再变化」当收敛信号是错的——那只是自洽（fixed point），不是最优。自改进循环必须显式声明追的是 stability 还是 optimality；追 optimality 时禁止只靠 myopic retraining，须建模 θ→D(θ) 的影响（PerfGD / two-stage outside-the-echo-chamber / 诱导分布上的稳健优化）。验收加两栏：① 策略自身指标；② **被它诱导出的世界是否变好**（长期风险、子群公平、曝光多样性），只有第①栏达标不算完成。「改到不改了」不能替代「改对了」。

### r741C-3 ★凸损失不保证凸风险，收敛有两条前置；反馈强时重训可能根本不收敛
- **原文**：「even if the loss is convex in θ, [performative risk] **need not be convex**」；「retraining converges to a stable solution **if the loss is well-behaved and the performative feedback effects are not too strong. If either of those two conditions is violated, there is no guarantee of convergence**」。Berkeley 论文逐字「if the performative effects are **weak, and well-conditioned**, several variants of this natural retraining dynamic are guaranteed to **rapidly converge** to a stable point」「If performative effects are a second-order concern … **retraining is actually a principled way**」；Columbia 博客独立交叉给出同一条件的具体形式：loss 需 smooth + strongly convex，且分布映射 D(·) 需 sufficiently Lipschitz（「your response distribution can't be too sensitive to changes to the model parameters」，即 ε-sensitivity 低）。另有 Fair-When-Trained-Unfair-When-Deployed 一类结果：训练时公平的指标在部署诱导的概念偏移后失效。
- **判据**：上线「按反馈自动改版」前先估反馈强度 ε 与损失条件，不满足则不得启用自动重训环，改为小步人工评审 + 固定 holdout（holdout 必须**不受策略曝光决策影响**，否则它也被 D(θ) 污染）。收敛声明必须同时给出两条前置的核验结果，缺一条就写「未证明收敛」。多智能体共享同一人群时，网络拓扑决定是否走向均衡或混沌，不能沿用单模型收敛结论。
- **与 r733C / r737B 的边界**：r733C 的 propensity 是「日志字段缺失导致离线评估不可用」，本条是「**日志本身是策略行为的产物**，字段齐全也不代表可当真值」；r737B 的 anytime-valid 解决「边跑边看抬 FPR」，本条解决「**看的对象在跟着策略动**」，前者不能修后者。

### r741C 来源与判非（逐字核验）
- `toc4fairness.org/self-fulfilling-and-self-negating-predictions-a-short-tale-of-performativity-in-machine-learning/`（作者 Tijana Zrnic，2021-05-06；Perdomo/Zrnic/Mendler-Dünner/Hardt ICML 2020 作者本人撰写）— WebFetch 200 全文逐字：model-dependent distribution / self-fulfilling 与 self-negating 两例 / performative risk 非凸 / fixed point / Nash vs Stackelberg / general-sum 非 zero-sum / 收敛两条件 / myopic updates 不足。**一手作者原文（第一独立域）**。
- `www2.eecs.berkeley.edu/Pubs/TechRpts/2023/EECS-2023-80.pdf`（Berkeley EECS 博士论文《Performative Prediction: Theory and Practice》）— **WebFetch 返回 `application/pdf` 非文本、字节丢弃，按 r731 先例如实登记为 WebSearch 快照逐字核验，未冒充一手全文 WebFetch**；逐串命中 Twitter / Google 两个反馈环、重复重训三步定义（θ_t → D(θ_t) → θ_{t+1}）、weak + well-conditioned 快速收敛、「retraining is actually a principled way」。**第二独立域（学位论文）**。
- `lacuna.tiptreesystems.com` 两篇方向综述（Stability–Optimality Gap / Learning in Performative Environments，WebSearch 快照逐字）— stable 点可能诱导坏世界、PerfGD 越过 mediocre stable points、公平指标部署后失效、非凸与弱凸条件；`statmodeling.stat.columbia.edu/?p=45740`（Gelman 博客，WebSearch 快照逐字）— smooth + strongly convex 与 D(·) Lipschitz / ε-sensitivity 的独立交叉。**第三、四独立域；综述站与博客立场均登记，不作唯一结论来源**。
- **判非**：窄串词边界全库 SKILL.md — `performative` / `performative risk` / `performative stability` / `Stackelberg` / `distribution map` / `D(θ)` / `D(theta)` / `self-fulfilling` / `self-negating` / `feedback loop` **全 0 命中**；`Nash` 在 co-learn 台账为 0 命中（grep 实测）；`position bias` 2 命中属搜索排序偏差语义，与本节「策略诱导分布」不同层。与既有 §15/§16/r733C/§17 正交，未复用任何一轮结论。豆包自留地 WB 0 落地。
- **未采纳**：PerfGD / PerfRL 的具体算法与收敛界、Lacuna 的网络拓扑博弈结论属实现细节与扩展场景，只取可迁移判据，不作公式搬运；「Twitter/Google 的具体系统实现」只作机制例证，不写成产品事实。

- **提升层**：AI 自改进验收 / VI 数据质量门 / PDI 结算台账。触发词：performative prediction、performative stability、performative optimality、model-dependent distribution、D(θ)、self-fulfilling、self-negating、Nash vs Stackelberg、myopic retraining、反馈强度 ε、holdout 被污染、收敛两前置。

## 十九、CUPED 预实验协变量方差缩减（2026-11-14 r745C 实拉）

> 与 §15（概念漂移 / canary 验收）、§16（bandit regret vs estimation、探索预算）、§17（peeking / anytime-valid、OPE 字段与灰度链）、§十八（performative prediction、D(θ)）分工：本节只管**同一个对照实验怎么在不加样本的前提下更灵敏**，不管对照怎么设、什么时候能停、数据分布是不是被策略带偏。判重：`CUPED` / `variance reduction` / `pre-experiment` / `control variate` / `stratification` / `post-stratification` / `difference-in-differences` / `pooled population` / `pre-experiment period` / `Hyperband` / `successive halving` 全库 SKILL.md **0 命中**；`covariate` 1 命中在 `meta/pdi-forecasting`（保序预测 covariate shift，异命题）、`MDE` 3 命中在 `research/wb-experiment-design`（样本量/MDE 定死）与豆包自留地、`ASHA` 1 命中在 `engineering/ei-reliability`（异命题）⇒ 净新。

### 19.1（r745C-1）灵敏度有两条正交路径：加样本/加时长 vs 降方差，收益是 ρ² 不是「数据更多」
- **原文**：Deng, Xu, Kohavi, Walker (WSDM 2013)《Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data》摘要逐字「We propose an approach (CUPED) that utilizes data from the **pre-experiment period** to reduce metric variability and hence achieve better sensitivity. ... The results on Bing's experimentation system are very successful: **we can reduce variance by about 50%, effectively achieving the same statistical power with only half of the users, or half the duration.**」；§1 逐字「improving the sensitivity of experiments allows for more precise assessment of value, or equivalently running the experiments on smaller populations (supporting more experiments) or for shorter durations (improving the feedback cycle and agility)」；§3.2.1 公式 (3)(4)(5) 逐字「Ŷcv = Y − θX + θEX, where θ is any constant. Ŷcv is an unbiased estimator of E(Y) since −θE(X) + θE(X) = 0」「var(Ŷcv) is minimized when we choose **θ = cov(Y, X)/var(X)**」「with this optimal choice of θ, we have **var(Ŷcv) = var(Y)(1 − ρ²)**, where ρ = cor(Y, X) is the correlation between Y and X ... **the variance is reduced by a factor of ρ²**」；同节「The optimal θ turns out to be the ordinary least square (OLS) solution of regressing (centered) Y on (centered) X」；§3.2.2「To achieve a large correlation and hence better variance reduction, an obvious approach is to choose **X to be the same as Y**, which naturally leads to using the same variable during pre-experiment observation window as the control variate ... this indeed turns out to be the most effective choice we found」。MetricGate (2026-04) 逐字给出对照表：ρ=0.3→9% / 0.5→25% / 0.7→49% / 0.85→72% / 0.95→90% 方差缩减；「A correlation near 0 does almost nothing」(mida.so)；论文 §3 逐字「Unlike Monte Carlo simulations, in the world of online experiments, the population is dynamic and data arrive gradually ... We cannot design a sampling scheme in advance and then collect data accordingly. However ... because we have pre-experiment data, we can adapt Monte Carlo variance techniques by applying them "**retrospectively**."」。
- **判据**：① 改版验收遇到「样本不够 / 跑不出显著」，**先问有没有实验前同指标可做协变量**，再考虑加流量、延长实验、降 MDE；后者是同一条轴上的加码，前者是另一条轴。② **先估 ρ 再算收益**：ρ=0.3 只省 9% 样本，复杂度换不来收益就不上 CUPED；收益声明必须连 ρ 一起报，禁止只说「用了方差缩减所以更快」。③ 最优 θ 是 Y 对 X 的 OLS 斜率，别手工拍一个常数；把 X 取为「同一指标在实验前窗口的值」是论文实测最有效的选择。④ CUPED 是**回顾式**（retrospectively）应用：不改采样方案、不改分流，只在分析阶段调整指标 ⇒ 它不引入新的线上风险面，但也不修任何设计缺陷。⑤ 与 §15.3（canary 须与同时部署的等价基线对照）、§16.2（探索预算按不确定性衰减）分工：那两条管「对照怎么设」「预算怎么花」，本条管「同一个对照怎么更灵敏」。
- **提升层**：AI 自适应 / 验证 / 实验设计。触发词：CUPED、pre-experiment data、方差缩减 ρ²、半样本半时长、θ=cov/var、回顾式应用、先估 ρ 再上。

### 19.2（r745C-2）无偏性来自「分配前测量」这一时间边界与三个条件，不来自公式；用实验期数据会把真实效应减掉
- **原文**：论文 §3.2.2 逐字「Although in general it is not easy to find control variate X with known E(X(t)) and E(X(c)), **a key observation is that E(X(t)) − E(X(c)) = 0 in the pre-experiment period because we have not yet introduced any treatment effect.** By using only information from before the launch of the experiment to construct the control variate, the randomization between treatment and control ensures that we have EX(t) = EX(c).」「Notice how Δcv **does not depend on the unknown E(X(t)) and E(X(c)) at all as they cancel each other**.」「There is a slight subtlety that's worth pointing out. The pair (Y, X) may have different distributions in treatment and control when there is an experiment effect. **For Δcv to be unbiased, the same θ has to be used for both control and treatment. The simplest way to estimate it is from the pooled population of control and treatment.**」；§3.1.2 逐字「It is important to note that by using only the **pre-experiment** information, the stratification variable X is **independent of the experiment effect. This ensures that the stratified delta is unbiased**.」；MetricGate 逐字三条件「1. **Pre-experiment measurement.** X must be observed before random assignment, so it cannot be affected by treatment. 2. **Common θ across arms.** Estimate θ on pooled data (or on control), not separately per arm. **Per-arm fitting introduces a small bias proportional to the treatment-induced difference in covariate means.** 3. **Centred covariate.** Subtract X̄ so that the adjustment has mean zero across the experiment population.」「**Avoid post-treatment variables.** Anything measured after assignment can be affected by treatment and will bias the estimator.」；mida.so 逐字「A common mistake is using an in-test behavior as X, such as "pages viewed during the test." The variant changes that number, so **the adjustment removes part of the treatment effect and can hide a real winner**.」「The covariate has to be measured before assignment. Using something the variant changed will bias the result.」「If X is missing for new users, say how you treated them. **Dropping every new user changes the population.**」；atticusli 逐字「Validate with A/A tests that CUPED doesn't introduce bias before rolling out」「Re-estimate theta on each experiment — correlations drift」。
- **判据**：① **准入四项缺一即不得采信 CUPED 结论**：X 在分配前测且不受处理影响 / θ 全池估计两臂共用 / X 中心化 / 新用户缺 pre-period 的处理方式显式写出。② **按臂各拟合 θ 是隐蔽偏差源**（偏差与处理引起的协变量均值差成正比），比「θ 拍脑袋」更难发现。③ 把实验内行为当协变量**不是降噪而是抹掉效应**：它会把处理造成的一部分变化从 Y 里减掉，让真实赢家看起来没效果；这是本节最危险的误用，验收清单里单列一条。④ 上线前用 **A/A 测试**验证调整没引入偏差；θ 每次实验重估（相关结构会漂移），禁止跨实验复用。⑤ 报告同时给 **naive 与 adjusted 两栏**（MetricGate「Report both the naive and the CUPED estimates as a sanity check」/ mida「Publish both the raw lift and the adjusted lift」），两栏背离时先查准入四项，不要直接采信更显著那栏。
- **提升层**：AI 自适应 / 验证 / 数据质量门。触发词：分配前测量、三条件无偏、同一 θ 两臂共用、per-arm fitting 偏差、post-treatment variable 抹掉效应、新用户缺 pre-period、A/A 验证、naive 与 adjusted 双栏。

### 19.3（r745C-3）方差缩减与「能不能提前看」是两套程序；DiD / 分层不是另两个新能力
- **原文**：论文 §3.3 逐字「when the covariate X is categorical (say, with discrete values 1,…,K) **the two approaches produce identical estimates**」「To this end, **the control variates technique is an extension of stratification**, where both continuous and discrete covariates are applicable.」；MetricGate 逐字「**DiD is actually a special case of CUPED with θ fixed at 1**」「DiD is **variance-reducing only when the pre-post regression slope is close to 1. If the slope is 0.4 (typical for noisy revenue metrics), DiD *increases* variance relative to the raw outcome.** CUPED dominates DiD because it picks the optimal slope automatically.」；mida.so 逐字「Another is **applying CUPED and then peeking early because the interval got tighter. The sample plan still has to be the plan you set.**」；论文 §3 逐字「we can adapt Monte Carlo variance techniques by applying them "retrospectively."」；DataField Ch.33 著录「Johari et al. (KDD 2017) prove that continuous monitoring with fixed-horizon p-values inflates the type I error rate to 5-10 times the nominal level and derive always-valid p-values」与「Deng et al. ... demonstrate 30-50% variance reduction on real Bing experiments」并列为两项独立技术。
- **判据**：① **置信区间变窄 ≠ 允许提前停**：CUPED 只降方差，peeking 的 FPR 由 §17（r737B anytime-valid / mSPRT / 置信序列）那套管，两者不能互相替代，也不能因为「用了 CUPED 区间更窄」就缩短预设观察窗。② **DiD 是 θ=1 的次优特例**，斜率偏离 1 时反而放大方差；别把「前后差值」当成独立的方差缩减方法再立一层（rules/07 去重铁律：合，不增）。③ **stratification 与 control variates 在离散协变量上是同一解**，按同一族治理，不新建并行流程；CUPAC / 多协变量只是 X 从标量扩成向量。④ §17 已列「离线只排在灰度之前，不能替代 holdout / 护栏 / 回滚」与「数据质量门先行」——CUPED 属分析层，SRM、曝光错配、指标切换、结果成熟度这些设计缺陷它一个都修不了，越界前先过数据质量门。⑤ 与 §十八（performative：日志本身是策略产物）分工：那条说「字段齐全也不代表可当真值」，本条说「字段齐全且合法时才谈得上降方差」。
- **提升层**：AI 自适应 / 治理 / 实验设计。触发词：CUPED 不等于可提前停、DiD 是 θ=1 特例、stratification 与控制变量同一解、CUPAC、分析层不修设计缺陷、随时有效推断另走一套。

### r745C 来源与判非（2026-11-14 实拉，逐字核验）
- `https://www.exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf`（Deng / Xu / Kohavi / Walker, **WSDM 2013**, Microsoft；**原始论文 PDF**）— **curl 下载 564,364 B，Content-Type: application/pdf；WebFetch 明确返回「non-text resource，字节丢弃」，按 r731 先例如实登记；改用 `pypdf` 本地逐字提取 10 页正文**；摘要 50% 方差 / 半样本半时长、§3 retrospectively、§3.1.2 pre-experiment 无偏、§3.2.1 公式 (3)(4)(5) 与 OLS 联系、§3.2.2 EX(t)=EX(c) / 同一 θ / pooled population / X 取同一指标最有效、§3.3 分层与控制变量等价。**第一独立域（学术一手原文）**。
- `https://metricgate.com/blogs/cuped-variance-reduction-ab-testing`（MetricGate《CUPED: Cut A/B Test Variance by 50%》，2026-04）— **WebFetch 200 全文逐字**：调整公式 / θ*=Cov(Y,X)/Var(X) / Var=Var(Y)(1−ρ²) / 无偏三条件 / DiD 是 θ=1 特例且 slope 0.4 时反增方差 / ρ 对照表 / 协变量选择 / 实现配方 / naive+adjusted 双报。**第二独立域（厂商技术博客，立场登记，与论文逐字交叉后采纳）**。
- `https://www.mida.so/ab-testing-terms/cuped` + `https://datafield.dev/advanced-data-science/part-06/chapter-33/further-reading.html` + `https://atticusli.com/behavioral-science-glossary/cuped-variance-reduction/` + `https://nishbhana.com/glossary/cuped` — WebSearch 快照逐字（四域）：「measured before assignment」/「removes part of the treatment effect」/「applying CUPED and then peeking early」/ 新用户处理 / WSDM'13 著录与 Bing 33–50% 实测 / CUPAC(Netflix 2020) / Freedman 批评与 fully-interacted regression / Kohavi-Tang-Xu 教材 / A/A 验证 / θ 每次重估。**第三、四独立域（术语站与教材索引，仅作交叉不作唯一结论来源）**。
- **判非**：`CUPED` / `variance reduction` / `pre-experiment` / `control variate` / `stratification` / `post-stratification` / `difference-in-differences` / `pooled population` / `pre-experiment period` / `Hyperband` / `successive halving` / `minimum detectable` 全库 SKILL.md **0 命中**；`covariate` 唯一命中在 `meta/pdi-forecasting` §r737C（保序预测 covariate shift / 边际覆盖 vs 条件覆盖），`MDE` 3 命中在 `research/wb-experiment-design`（样本量与 MDE 定死）与豆包自留地 `wb-execute-discipline` / `wb-context-compressor`，`ASHA` 1 命中在 `engineering/ei-reliability`，`sensitivity` 2 命中为通用语境——均为异命题，登记不复用。与 §15 / §16 / §17 / §十八 正交，未复用任何一轮结论。豆包自留地 **WB 0 落地**。
- **未采纳**：CUPAC 的机器学习协变量、非线性 f(X)=E(Y|X) 最优形式、半参数 GEE / ANCOVA 与 Freedman 批评的理论细节属实现与统计专门问题，只取可迁移判据；「200 实验/季度、50% 缩减等于双倍速度」类厂商营销换算不写成事实。PDF 字体为 CFF Type1 子集、pypdf 报 fontTools 未安装的编码告警，正文英文逐字可核验，未因此改动任何原文。

## 二十、时间维度：效应会退化，代理指标不等于北极星（r749A 独立实拉 2026-11-15）

> 与 §17（r737B anytime-valid：什么时候可以读数）、§18（r741C performative：数据生成随策略变）、§19（r745C CUPED：同一指标怎么降方差）分工：本节管**「效应本身随暴露时间变」与「拿哪个指标当效应」**。四者正交，互不替代。

### 20.1（r749A-1）短测试假设处理效应恒定；novelty 与 primacy 是方向相反的两个偏差，且多数疑似趋势是累计曲线的统计假象
- **原文**：UX Brighton UXDB 方法条目逐字「**Short A/B tests assume a constant treatment effect**, but visible changes often provoke novelty clicks or change aversion that fade as users adapt」「**Per-day effect plots, using each day's own visitors rather than cumulative plots that create false trends**, show decline (novelty) or growth (primacy, learning)」「**New users are a check: if a change wins only for them, suspect novelty**」「in Google's 2010 search redesign, **high-frequency users who met the change most looked better early, and others converged after a longer run**; large visual changes may need **about six weeks**」；其 Steps 逐字「Segment by usage frequency and tenure: **if high-frequency users already look better, exposure and learning are driving the early result**」。Atticus Li 逐字引 Kohavi/Tang/Xu 定义「**Primacy effect is when you change something on the site and experienced users may be less efficient until they get used to it**」，并给出反向签名「variant launches at **-8%** vs control in week one, recovers to **-3%** in week two, **-1%** in week three, and to a small positive lift by week four」；donnuab 逐字著录 Kohavi KDD 2012《Five Puzzling Outcomes Explained》「**most suspected primacy and novelty trends are statistical artifacts** of reading a cumulative curve early, not real decay」与 KDD 2014《Seven Rules of Thumb》「in practice **novelty and primacy effects are uncommon**」「no experiment was found in which a significant result reversed direction because of these effects」。
- **判据**：① **默认把「效应恒定」列为待验假设**，改版验收第一栏写「本次变化属于提高显著性（新按钮/徽章/通知）还是打断习惯（导航/布局/工作流）」——前者短期偏差向上（虚高发货），后者向下（虚低回滚）；**用同一条「跑两周」启发式同时犯两个方向的错**。② 曲线必须用**当日访客逐日效应**，累计曲线结构性隐藏衰减；同时画「前 1–2 天首次暴露 cohort」的效应，并按使用频次/ tenure 分层。③ **新用户是判别器**：只在回访用户身上出现差异指向习惯/novelty；只在新用户身上赢亦可疑；高频用户早期更好 = 暴露与学习驱动早期结果。④ novelty/primacy **是要检验的假设，不是对不喜欢结果的默认解释**（KDD 2012 口径）；但确实存在时不可提前宣判，需延长到稳态（大视觉改动量级约六周，绑 UXDB 方法条目，不写成通用事实）。

### 20.2（r749A-2）长期效应不是「把测试跑久一点」，而是换设计；长跑自带三类新陷阱
- **原文**：UXDB 逐字「For durable estimates, **cohort analysis tracks stable signed-in users**; **post-period analysis switches the treatment off and measures the residual learned effect** (Google found users learned to click fewer ads as ad load rose); **time-staggered treatments start a second copy later and declare convergence when the two agree**」；Steps 逐字「choose a design: **stable signed-in cohort reweighted by pre-experiment strata**, post-period analysis after switching the treatment off, or a time-staggered second treatment copy」「**Test convergence, separate user-learned from system-learned effects**」。Atticus Li 逐字著录 Dmitriev/Frasca/Gupta/Kohavi/Vaz (2016)《Pitfalls of Long-Term Online Controlled Experiments》：**cookie churn invalidating up to 75% of long-term cookie-based identification** / **survivorship bias from differential user attrition between arms** / **interaction with other concurrent experiments**，并明写「the literal solution — '**just run the test longer**' — introduces its own pitfalls」「'just run the test longer' is **necessary but not sufficient**」。Technometrics 2022 Vol.64 No.4 p.524-534（DOI 10.1080/00401706.2022.2124309，《Novelty and Primacy: A Long-Term Estimator for Online Experiments》）摘要逐字「we propose an observational approach, based on **difference-in-differences technique to estimate user-learning at scale** ... compare our approach with the existing experimental method ... higher statistical power, and ... **limitation in presence of other forms of treatment interaction with time**」。
- **判据**：① 长期结论必须从**三种设计里选一种并写明**（稳定登录 cohort + 实验前分层重加权 / 关掉处理后的 post-period 残差学习效应 / 时间错开第二份处理且两者一致才宣告收敛），禁止用「延长同一个短测试」冒充长期估计。② **长跑要按长跑的坑设计**：标识稳定性（cookie churn）、两臂差异化流失的幸存者偏差、并发实验交互逐条登记；缺任一条不得把长跑结果写成因果长期效应。③ **分离 user-learned 与 system-learned**（用户学会少点广告 vs 系统侧排序/模型学会），两者混在一个 lift 里无法外推到未来短测试。④ 与 §17 分工：anytime-valid 管「能不能提前看」，本节管「看到了是不是稳态」；与 §18 分工：performative 管分布随策略参数变，本节管同一策略下效应随暴露时长变。

### 20.3（r749A-3）代理指标与北极星的关系不能靠相关或朴素 OLS 估；加实验数只会更精确地估出偏掉的斜率
- **原文**：Netflix TechBlog（**2024-08-26**, KDD 2024，Bibaut/Chou/Ejdemyr/Kallus）逐字「how do we establish that a treatment that improves short-term (statistically sensitive) outcomes also improves long-term (statistically insensitive) outcomes?」「The click-through rate is a **proxy metric (S, for surrogate)** while retention is a downstream **business outcome or north star metric (Y)**」；用户级相关陷阱「promoting **clickbait may have the opposite effect**」「there are many **confounders between S and Y** — many of which you can never reliably observe and control for」；处理效应相关陷阱「**correlated measurement error** — if S and Y are positively correlated in the population, then treatment arms that happen to have more users with high S will also have more users with high Y」「covariances between **estimated** treatment effects can appear misleadingly causal」「**the true relationship between S and Y can be negative even if the OLS slope is positive**」「**Only more data per experiment could diminish this bias — using more experiments as data points will only yield more precise estimates of the badly biased slope**」。三估计量逐字：**TC**「subtracting the scaled measurement error covariance ... Under the assumption that the correlated measurement error is the same across experiments (**homogeneous covariances**), the bias ... is inversely proportional to the **total number of units across all experiments**」；**JIVE**「converges to the same OLS slope ... **does not require the assumption of homogeneous covariances**」「removing each observation's data from the computation of its instrumented surrogate values」；**LIML**「statistically efficient as long as there are **no direct effects between the treatment and Y (that is, S fully mediates all treatment effects on Y)**」「We find that LIML is **highly sensitive to this assumption** and **recommend TC or JIVE for most applications**」。Lacuna（独立复核）逐字 CV 框架「decoupling decision-making from evaluation using historical data splits ... **unbiased estimator of long-term business impact**」「123 historical A/B tests at Netflix ... **over 33%** ... cumulative returns to the North Star metric」，并声明「assumes **independence between experiments and stationarity in user behavior over time**」。
- **判据**：① **代理指标不是北极星的替身，而是一条待验证的结构假设**：报告里写「本轮决策用的是哪个代理、它与北极星的关系用哪种方法验证过、前置假设是什么」，禁止把「CTR 显著涨了」直接写成「长期价值涨了」。② **两种朴素验证都要排除**：用户级相关被混杂污染；历史实验 (S,Y) 处理效应散点的 OLS 斜率被相关测量误差污染，**加更多实验只会把偏得更厉害的斜率估得更精确**，能降这个偏差的是**每个实验更多单元**，不是更多实验。③ 若采用估计量：**默认 TC 或 JIVE**（官方对 LIML 的完全中介假设明确警告），用 TC 须声明齐次协方差假设，用 LIML 须证明 S 完全中介。④ **结论边界**：Netflix/Lacuna 的具体数字（33%、123 实验、95% 一致率/79% 精确率/65% 召回率一类）仅绑论文与厂商样本作例证，不移植为通用工程事实；HTA/留存/营收等量纲与 OEC 治理不采纳。⑤ 与 §19 CUPED 分工：CUPED 降**同一指标**的方差；本节判**这个指标本身代不代表想优化的东西**。

**来源（r749A 独立实拉 2026-11-15，≥2 独立域交叉）**：
- `https://netflixtechblog.com/improve-your-next-experiment-by-learning-better-proxy-metrics-from-past-experiments-64c786c2a3ac`（Netflix Technology Blog，**Published Aug 26, 2024**，KDD 2024；WebFetch 200 **全文逐字**：proxy S / north star Y、clickbait、confounders、correlated measurement error、OLS 斜率反号、TC/JIVE/LIML 三估计量与前置、LIML 高度敏感建议改 TC/JIVE。**第一独立域·厂商研究一手**）
- `https://uxbri.org/uxdb/methods/novelty-primacy-and-long-term-effect-estimation-9c196757`（UX Brighton UXDB 方法条目；WebFetch 200 **全文逐字**：短测试恒定效应假设、per-day 用当日访客、Google 2010 高频用户、约六周、新用户判别、三设计、user/system-learned 分离；著录 King et al. 2017《Designing with Data》与 Kohavi et al. 2020《Trustworthy Online Controlled Experiments》。**第二独立域·方法库一手**）
- `https://www.atticusli.com/replication-crisis/ab-testing-novelty-primacy-effects` + `/ab-testing-surrogate-metric-trap`（WebSearch 快照逐字：Kohavi primacy 定义、-8%→-3%→-1%→正、Dmitriev 2016 三陷阱与 75% cookie churn、Athey 2019 surrogate index / Prentice 假设、Netflix 95%/79%/65%、OEC 验证与长期 holdout 基础设施口径）· `https://donnuab.com/blog/en/novelty-effect-ab-testing`（快照逐字：KDD 2012 统计假象、KDD 2014 不常见与推荐系统例外、两周整周窗口、每周 vs 累计双栏）· `https://lacuna.tiptreesystems.com/work/evaluating-decision-rules-across-many-weak-experiments`（快照逐字：winner's curse、CV 折外评估、Theorem 3.1 Poisson、123 实验 33%、独立性与平稳性前提）· `https://library.unpar.ac.id/index.php?id=276411&p=show_detail`（Technometrics 2022 书目页，DiD 估 user-learning 摘要逐字）· `https://abstractopedia.org/domain-specific/novelty_effect` · `https://www.emergentmind.com/topics/surrogate-index`（公式渲染为占位符，**如实登记不引用其数值**）· `https://boboru.net/?p=495/`（中文二手，仅作交叉）。**第三~六独立域·教学/学术书目/知识库立场，逐条登记不作唯一结论来源**。
- **判非**：`novelty effect` / `primacy effect` / `surrogate metric` / `proxy metric` / `north star` / `correlated measurement error` / `long-term holdout` / `time-staggered` / `change aversion` / `user-learning` / `winner's curse` 全库 `SKILL.md` **0 命中**；模块 `AI/MEMORY.md` 已有 §15 漂移/canary、§16 bandit regret、§17 peeking、§18 performative、§19 CUPED 均为异命题、不复用。豆包自留地 **WB 0 落地**。
- **未采纳**：HTA/医疗报销语境、Netflix 与 Lacuna 的具体收益数字、预实验协变量机器学习化（CUPAC）、Freedman/ANCOVA 理论细节、OEC 治理与执行签批流程。


## 二十一、实验干扰与 SUTVA：随机化单元决定了结论能不能成立（r753A 独立实拉 2026-11-15，≥2 独立域一手交叉，3 独点）

> 定位：本节管「**这次对照的分派本身是否独立**」，是比读数链更靠前的实验准入。与 §十七（anytime-valid 停止规则）、§十八（performative 分布随策略变）、§十九（CUPED 降方差）、§二十（novelty/长期/代理）分工：那四条管怎么读、方差多大、效应是否稳态；本节管「对照组有没有被处理组污染」，违反时前面所有口径一起失效。与 VI 模块 r735A 的 SRM 分工：SRM 管数据流被污染（分流比失衡），本节管设计本身违反 SUTVA（分派单元不独立），两道门先后独立。

### 21.1（r753A-1）SUTVA 不是默认成立的前提；偏差方向由「谁和谁争/谁和谁补」决定
- **原文**：MetricGate《Switchback Experiment》逐字「Standard randomized controlled trials assume **SUTVA: one unit's treatment does not affect another unit's outcome**」「In two-sided marketplaces this fails — **discounting fares for a treatment group of riders may shift driver supply toward them, harming control riders**」「**Interference: When treatment in one unit affects outcomes in others, user-level randomization fails to isolate the effect**」；Lyft Engineering（Shima Nassiri / Ido Bright，**2025-01-27**）逐字「This situation violates the **Stable Unit Treatment Value Assumption (SUTVA)** which indicates that the control group should not be affected by the treatment」「**interference doesn't always lead to an overestimation of the treatment effect**」「In social networks, treating units ... **boosting control outcomes and thus reducing the perceived treatment effect**」「with **complementary products** ... **underestimating** the treatment effect. Conversely, for **substitutable products** ... **overestimated**」；UXDB 逐字「**Map interference: who affects whom (shared supply, social ties, team accounts)**」。
- **判据**：① **先画干扰图再选随机化单元**：共享供给 / 社交连接 / 团队账号 / 替代品竞争任一存在，用户级 A/B 的「处理 vs 对照」就不是两个独立总体，结论不可直接解读；禁止把「随机分流了」当成 SUTVA 已满足。② **偏差方向不固定**：争抢稀缺资源（司机、库存、曝光位）→ 对照组被压低 → 效应**高估**；社交外溢或互补品 → 对照组被抬高 → 效应**低估**。⇒ 复盘时不能笼统写「有网络效应所以结果偏乐观」，须写明共享的是哪种资源、两臂谁受谁影响。③ **验收动作**：报告先列「随机化单元 + 干扰图 + 判定该单元是否隔离」，缺这三项不得引用 lift 数值。④ 与 §十八分工：performative 是策略参数改变数据生成分布，本节是**同一时刻**一个单元的处理改写了另一个单元的结果，两者可同时发生但归因不同。

### 21.2（r753A-2）换随机化单元＝换有效样本量；switchback 结构性没有 holdout
- **原文**：MetricGate 逐字「The **effective sample size is the number of time blocks, not users** — substantially reducing statistical power」「This is typically **20–100 rather than thousands**, which is why switchback experiments are often underpowered」「**shorter blocks give more periods but amplify carryover**」「**Adding more regions or extending duration are the primary levers for increasing power**」；UXDB 逐字「**Estimate the intra-cluster correlation and compute the design effect (1 + (m - 1) x ICC) for sample size**」「choose **window length longer than carryover time** and randomise sequences; consider **burn-in periods**」；Lyft 逐字「**it's not possible to include a holdout group in a time-split experiment, making them unsuitable for assessing long-term impacts**」「time-split experiments ... **designed to capture short-term marketplace behavior**」「**Experimenters might opt to run a combination of a time-split experiment followed by a user-split experiment**」「**costly to implement and can delay decision making by several weeks**」「region-split experiments often suffer from **low statistical power due to smaller effective sample sizes**」。
- **判据**：① **功效按独立单元数算，不按曝光量算**：switchback 的 n 是时间块（20–100 量级），cluster 的 n 是簇且要乘设计效应 `1+(m−1)·ICC` ⇒ 把「有百万用户」写成功效充足是量纲错误。② **窗口长度是权衡不是越短越好**：短块换更多块数但放大 carryover；设计规格同时写「块长 > 携带残留时间」「过渡窗是否排除 / burn-in 是否设置」。③ **time-split 无 holdout 是结构性限制**，不能用来评长期效应；要长期结论必须接一段用户级实验或另设长期 holdout，并把两段结论分栏报，不混成一个 lift。④ 与 §二十分工：§20.2 管「同一个短测试跑久一点不等于长期估计」，本节管「这类设计根本装不下 holdout」，是设计能力边界而非运行时长问题。⑤ 可干净分离时优先 cluster/geo（功效更高），按「判非」登记不重述 geo 实现细节。

### 21.3（r753A-3）分析口径必须跟着分派单元换：cluster-robust、carryover 检验与双栏报告
- **原文**：MetricGate 逐字「Because observations within a block share the same assignment, **cluster-robust standard errors are required**」「The sandwich estimator applies a **small-sample correction of n_c/(n_c−1)**, and **degrees of freedom are based on the number of blocks, not individual observations**」「**SE inflation factor: The ratio of cluster-robust to naive standard error. A factor of 2 or more means naive p-values are severely anti-conservative and must not be used**」「**Carryover effects: ... Diagnosed by regressing the outcome on both current and lagged treatment indicators**」「Run the carryover test; **if significant, widen blocks or exclude transition windows**」「**power below 0.5 means a null result should not be interpreted as evidence of no effect**」；完整报告口径逐字「A complete write-up reports: The block-adjusted treatment effect and its confidence interval / The **cluster-robust standard error (clustered by block) and the SE inflation factor** / The cluster-robust t and exact p, **plus the number of time blocks as the effective sample size** / Any carryover finding」；示例数值逐字「SE 1.5526 vs the naive 1.2976 — an **inflation factor of 1.1965** ... cluster-robust p=0.3471」（示例数据，绑页面不作为通用事实）。UXDB 逐字「Analyse with **cluster-robust or mixed-effects models**, or design-based estimators」「**Compare with user-level estimates to quantify interference bias**」。
- **判据**：① **块内相关不能用朴素 SE**：自由度按块数、小样本修正、报膨胀因子；膨胀因子 ≥2 时朴素 p 值反保守，禁止用于上线决策。② **carryover 是假设检验不是目测**：当期 + 滞后处理指示一起回归，显著则加宽块或排除过渡窗；不得「看起来恢复了」就继续读数。③ **报告固定五栏**：block-adjusted 效应 / 两种 SE 与膨胀因子 / cluster-robust p / 块数（有效 n）/ carryover 结论；power<0.5 的 null 写「未检出」不写「无效应」。④ **与用户级估计并列**可量化干扰偏倚大小（UXDB 第 6 步），两栏差异本身就是「用户级随机是否可用」的诊断证据。⑤ 与 §十九 CUPED 分工：CUPED 降**同一个正确分派下**的方差，本节修的是**分派不独立**；分析层修正替代不了设计层换单元（同 SRM 不可重加权修，按「合」登记不重述）。

**来源（r753A 独立实拉 2026-11-15，≥2 独立域一手交叉）**：
- `https://metricgate.com/docs/switchback-experiment/`（MetricGate《Switchback Experiment》方法文档；WebFetch 200 **全文逐字**：SUTVA 与双边市场失效、有效样本量=块数 20–100、cluster-robust 与小样本修正 n_c/(n_c−1)、自由度按块数、SE inflation factor ≥2、carryover 当期+滞后回归、7 步流程、APA 五栏报告、power<0.5 判据、示例 SE 1.5526/1.2976/1.1965、局限与替代方法。**第一独立域·实验方法文档一手**）
- `https://eng.lyft.com/using-marketplace-marginal-values-to-address-interference-bias-a11aff6e670f`（Lyft Engineering，Shima Nassiri & Ido Bright，**Published Jan 27, 2025**；WebFetch 200 **全文逐字**：SUTVA 定义与供给受限下高估、社交/互补品低估、替代品高估、cluster randomization 与低功效、time-split 全单元同一处理、**无法包含 holdout 故不适于长期影响**、time-split 后接 user-split 的组合与数周代价、region-split 低功效、MMV/shadow price 建模路线与 10% 决策改变/45% 量级下降（**厂商样本数值仅作例证，不移植为通用事实**）。**第二独立域·厂商工程研究一手**）
- `https://uxbri.org/uxdb/methods/switchback-and-cluster-randomised-experiments-7a8e3e51`（UX Brighton UXDB 方法条目；WebFetch 200 **全文逐字**：干扰图映射、随机化单元选择、设计效应 `1+(m−1)×ICC`、窗口长于 carryover 与 burn-in、cluster-robust/混合效应/设计型估计量、与用户级估计对比量化偏倚；著录 Hayes & Moulton 2009、Bojinov/Simchi-Levi/Zhao 2023 Management Science、Kohavi/Tang/Xu 2020。**第三独立域·方法库一手**）
- `https://lacuna.tiptreesystems.com/paper/faster-rates-for-switchback-experiments/art_2f2f2a52ff7b4a13871508d899fa9a1f`（WebSearch 快照逐字：Su Jia/Bhattacharya/Kallus/Yu arXiv 2023 Clustered Switchback、空间×时间干扰、truncated HT 与 rapid-mixing MDP、O~(1/NT)、DIMBI 漂移失效）· `https://datarekha.com/interview/statistics/network-effects-interference`（快照逐字：SUTVA、graph clustering / geo / ego-network / switchback 四类设计、network exposure models 假设更强）· `https://metricgate.com/docs/cluster-randomized-experiment/`（同站关联页，判非时不作独立来源）。**第四~五独立域·学术仓储/教学立场，逐条登记不作唯一结论来源**。
- **判非**：`SUTVA` / `switchback` / `interference bias` / `carryover` / `cluster-robust` / `design effect` / `spillover` / `时间块` / `溢出效应` 全库 `SKILL.md` **0 命中**；`interference` 2 命中经查属 `engineering/wb-agent-evaluation`（技能库语义干扰，异命题）与 `meta/agent-evolution` §17 数据质量门一句（只列名未立论，按「合」不重述）；`SRM` / `sample ratio` 命中属 VI 模块 r735A（分流比失衡），命题为数据流污染，与本轮设计层 SUTVA 正交，`网络效应` 1 命中属 `research/wb-hv-research`（异命题）。模块 `AI/MEMORY.md` §15 漂移/canary、§16 bandit、§17 peeking/OPE、§18 performative、§19 CUPED、§20 时间效应均为异命题、不复用。豆包自留地 **WB 0 落地**。
- **未采纳**：MMV/shadow price 建模实现、厂商具体收益数值（10%/45%/90% 用户级实验占比）、truncated HT 理论界与 MDP 快速混合证明、geo 实验的季节/局部混杂细节、R 代码与 MetricGate 计算器操作、Bojinov 2023 估计量推导。
