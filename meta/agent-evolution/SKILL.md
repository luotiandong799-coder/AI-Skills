---
name: agent-evolution
version: "1.30.0"
description: 智能体持续进化引擎：把高价值任务沉淀为可复用 Skill/经验/规则，统一调度已有 Skill 完成调用、优化、记忆、安全检查与生命周期治理，杜绝重复造轮子。 触发：任务后复盘总结、发现可复用流程想生成 Skill、希望 Agent 少问多想自主进化、并发实验分层、层间正交、发布层灰度、安全探索、shield 护栏、约束 MDP、代价 critic、持续学习灾难性遗忘、EWC、Fisher 信息、弹性权重整合、在线 EWC、突触智能、经验回放、稳定性可塑性权衡、异质性处理效应、因果森林、CATE、honest splitting、GRF、DML、DR-learner。、Hyperband、Successive Halving、多保真预算分配、纯探索无限臂bandit、early stopping、bracket网格、envelope函数、BOHB、贝叶斯优化、GP代理模型、采集函数、Expected Improvement、PI、UCB、探索利用权衡、异步并行评估、multi-fidelity、高维BO。、元学习、MAML、学会学习、快速适配、内循环外循环、支持集查询集、FOMAML、Reptile、Meta-SGD、任务分布初始化、势能奖励塑形、potential-based reward shaping、PBRS、策略不变性、F(s,s')=γΦ(s')−Φ(s)、望远镜抵消、势函数、奖励设计、稀疏奖励、Wiewiora Q值初始化、Dynamic PBRS、课程学习、curriculum learning、scoring function、pacing function、自步学习、self-paced learning、全局难度、局部难度、难例挖掘、anti-curriculum。DPO、直接偏好优化、隐式奖励、参考模型、Bradley-Terry、sigmoid loss、chosen/rejected、偏好对、KL 约束、β 温度。GRPO、组相对策略优化、组内优势归一化、去 critic、可验证奖励。CQL、保守Q学习、offline RL、离线强化学习、分布偏移、OOD动作高估、保守Q函数下界、MBPO、模型基策略优化。Decision Transformer、条件序列建模、return-to-go、RTG、回报条件化、RvS、因果掩码动作生成。RND、随机网络蒸馏、好奇心探索、内在奖励
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
# 一、八大能力 → 已有技能路由表（优先复用，禁止重造）

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

## 十六、探索-利用门：regret 与估计方差是两种目标（r717A · 全文下沉）

> 目标分叉（A/B 固定分配求干净 ship/kill vs bandit 最小 regret）、探索预算按不确定性衰减（UCB/Thompson 次线性 vs ε-greedy 线性 regret）、三个失效条件（延迟奖励/非平稳/部分反馈）三独点，全文见 `references/r717A_探索利用门.md`。本节仅留路由，以该 references 为准。
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

## 二十二、并发实验的重叠基础设施：层是参数子集，域是流量划分（r757A 独立实拉 2026-11-16，≥2 独立域一手交叉，3 独点）

> 定位：本节管「**上百个实验同时在线时，流量怎么复用、结论还成不成立**」。与 §17 序贯检验（何时能停）、§18 自改进闭环改写分布、§19 CUPED（方差缩减）、§20 时间效应、§21 SUTVA（随机化单元与干扰）分工：那五条都在**单个实验内部**；本节管**实验与实验之间的空间结构**。与 `engineering/wb-agent-evaluation` §9 SRM（分流比失衡 ⇒ 本轮数据整体不可采信）正交：SRM 是数据质量门，本节是分流架构。

### 22.1（r757A-1）多因素实验不可用不是算力问题是参数不独立；「层」是参数子集不是流量切片
- **原文**（Google KDD 2010 Diane Tang / Ashish Agarwal / Deirdre O'Brien / Mike Meyer《Overlapping Experiment Infrastructure: More, Better, Faster Experimentation》中文全译稿，一手 WebFetch 200 全文逐字）：「**多因素实验并不适用于`Google`的实验场景，因为实验参数可能并不相互独立（比如，粉色的字和粉色的背景）**」·「`Google`有几千个参数，并且不能被独立的分析…虽然『蓝色』对两个参数都是合法值，但是如果两个参数都取『蓝色』，那么页面是不可读的」·「**本文提出的解决方案是将参数分成子集，每个参数子集包含相互不能独立修改的参数。一个参数子集会与一个包含实验的层相关联，不同层的实验的流量是正交的**」·「**同一参数不能出现在多个层中**」·「每个请求最多会被 N 个实验处理（每层一个实验）」·单层实验的两个独立失效：「**流量饥饿**（上游模块的实验可能优先处理了所有请求，导致下游模块的实验没有请求）和**偏置**（`bias`）（比如，上游模块的实验处理了所有英语的请求，导致下游模块的实验就只有非英语请求）」。
- **判据**：① 想同时跑 N 个实验，第一动作不是「给每个实验切 x% 流量」（十个实验各 10% 就流量耗尽），而是**把参数空间划成互不相交的子集**；同一参数出现在两层则两个实验会互相覆盖，分层失效。② 判「能不能分层」看的是参数是否可独立修改，不是看模块边界——按服务划分只是**起点**（「一个程序所有的参数并不一定要在一个参数子集中」），还须按已知独立性或历史共改实验再切。③ 报告须写「参数→层」映射表 + 每请求最多命中实验数 N；缺这张表不能声称「实验正交」。④ 单层架构下若上游吃满流量，下游实验读数天然带偏：这不是统计偏差，是**采样结构缺陷**，加权修不回来（与 wb-agent-evaluation §9.3 同源）。

### 22.2（r757A-2）域 / 层 / 实验三分且可嵌套；发布层测跨特性交互，正常层测不出来
- **原文**（同上论文全译稿逐字）：「**域**是指流量的一个划分（一部分流量的意思）。**层**是指系统参数的一个子集。**实验**是指在一个流量划分上，进行零个或多个参数的修改，并最后改变请求处理的过程」·「**域和层可以相互嵌套。域中包含层。层中包含实验，层中也可以包含域**」·「一个域只有一个单一层（非重叠域），和一个有三个层的重叠域…请求只能在非重叠域或重叠域其中之一」·非重叠域三好处「同时进行改变大量参数值的组合实验」「允许我们进行不同参数划分方式」「嵌套可以更有效地利用空间」·**发布层**（`Launch layers`）四条：「发布层总是在默认域中」「**一个参数最多只能同时在一个发布层和最多一个正常层中**」「在发布层中的实验会为覆盖参数的默认值，作为新的默认值」「如果实验层的实验覆盖了默认值，那么实验就会用这个覆盖的值，**而不是系统的默认值，或是发布层实验中的参数值**」·「因为在正常层中，实验流量比较少，交集比较小，所以相互影响很难检测」⇒ 发布层「可以用于测试特性之间的相互影响」。另（伴鱼技术团队《AB 测试平台的设计与实现》2020-03-29 / 更新 2023-06-26，一手 WebFetch 200 全文逐字）：「**同一层的多个试验，只能参加其中一个，确保互斥。不同层的试验之间，完全独立**」。
- **判据**：① 域切流量、层切参数，两者是**两个正交维度**，别把「域」当成「层的容器别名」——嵌套是双向的（层里能再切域）。② 强交互（两个都改首页布局）必须放同一互斥层或专门保留流量测组合效应；跨层默认假设「可加」，不可加就得显式留非重叠域。③ 发布层是**灰度机制**不是实验层：它改的是默认值，正常实验层的覆盖优先；把发布层当普通实验层会写出「上线后实验组突然变对照组」的假结论。④ 想测「A 特性 × B 特性」交互，靠两个正常层实验的交集流量统计功效不足 ⇒ 用发布层的大流量，或明确写「本轮不检验交互」（与 §21 SUTVA 分工：那条说干扰会让估计失效，这条说正常层交集小到测不出干扰）。

### 22.3（r757A-3）层间正交不是天然的：哈希必须掺 layer salt，且同层只许一种分配类型
- **原文**（论文全译稿逐字）：「对于基于`cookie`取模的实验，我们用 **`mod = f(cookie, layer) % 1000`**，而不是`f(cookie) % 1000`的方式」「在`cookie`取模时加入了层`id`的信息」·四种分配类型「用户`id`取模和`cookie`日期取模…**我们当前只支持的四种分类型**」·固定优先序「**以特定的顺序对不同的流量分配类型进行分流：用户`id`，`cookie`，`cookie`日期，随机。一旦这个请求被某高优先级分配方式抽中后，其它低优先级的分配方式将忽略这个请求**」·「**在同一层中1%的`cookie`取模流量会比1%的随机流量大**」「**在实践中，一层之中一般只应有一种分流类型，实验和对比实验必须使用相同的分流类型，最主要的影响是不同的分流类型实验需要不同的样本量**」。伴鱼（一手全文逐字）：「**carryover effect**…第一个试验中分配到方案 A1 的用户，在第二个试验中也全都被分配到同一个方案(比如 A2)，这会**严重降低统计结果的可信度**」「这个问题，可以通过哈希时加 **salt** 来解决…这保证了，即使两个试验的方案数量及权重都完全相同，同一个 `client_id` 在两个试验中被分配的方案也被充分打散」·CSDN《AB实验方法论》（快照逐字）：「通过给不同实验使用不同的实验层盐值，可以让用户在不同实验中的桶号相互独立——这是**正交分层的数学基础**」「**任何实验的流量矩阵可审计，禁止业务代码里私写分流逻辑——私写分流是 SRM 和『鬼实验』的主要来源**」。
- **判据**：① 只按用户 ID 做一次哈希、各层复用同一桶号 ⇒ 跨层分配完全相关，carryover 会把 A 层效应混进 B 层读数，**层级越多污染越深**；正交是 `f(cookie, layer)` 换来的，不是「分成几层」自动带来的。② 上线前跑 A/A 交叉表：两层桶号应近似独立（χ² 或互信息），不独立先查 salt 是否漏加/重名。③ 同一层内混用分配类型（cookie 1% vs 随机 1%）会让名义流量相同而实际样本不同，实验与对照**必须同型**，否则样本量/功效口径全错。④ 分流配置必须集中声明可审计；业务代码私写分流等价于绕过 salt 与层登记（与 §19 CUPED 分工：CUPED 用实验前协变量降方差，本节用层 salt 保跨层独立，两者可叠加但不互相替代）。⑤ 四种类型优先序是**平台契约**，改顺序等于改所有在跑实验的样本池，须按配置变更评审。

**来源（r757A 独立实拉 2026-11-16，≥2 独立域一手交叉）**：
- `https://github.com/SuperWaterY/translations/blob/master/overlapping-experiment-infrastructure-more-better-faster-experimentation/README.md`（Google KDD 2010《Overlapping Experiment Infrastructure: More, Better, Faster Experimentation》Diane Tang 等，**2010-07**，基于火光摇曳 lexqu 译稿 v1.2.0 的中文全译；WebFetch 200 **全文逐字**：序言「更多/更好/更快」三目标、多因素实验不适用与蓝字蓝底、参数子集与层、同一参数不跨层、域/层/实验三定义与相互嵌套、非重叠域 vs 重叠域、发布层四条、四种分配类型与优先序、`f(cookie, layer)%1000`、流量饥饿与偏置、cookie 模 1000 与 42 梗、结论与四条展望。**第一独立域·原论文全译一手**；原文链接 `http://research.google.com/pubs/pub36500.html` 登记但不作独立访问源）
- `https://tech.ipalfish.com/blog/2020/03/28/ab_test/`（伴鱼技术团队 颜发明《AB 测试平台的设计与实现》，**2020-03-29 发表 / 2023-06-26 更新**；WebFetch 200 **全文逐字**：同层互斥不同层独立、粉色字粉色背景例、carryover effect 与 salt 打散、白名单/fallback 兜底方案、层内权重与分桶为何无意义（100 桶 40/60 导致新试验无桶可用）、App≈Domain、Grpc 接口与 6 步分配逻辑、Douglas Bowman 41 度蓝轶事。**第二独立域·工程实现一手**）
- `https://blog.csdn.net/CaiNiaoXinBing/article/details/165452833`（CSDN《AB实验方法论》，WebSearch 快照逐字：确定性哈希三性质、层盐值是正交数学基础、UI/推荐/推送/广告各吃 100% 流量、互斥层处理强交互、配置即代码与鬼实验、AA 平衡检查的多重比较陷阱）· `https://www.52nlp.cn/...`（达观数据，快照逐字：域纵向/层横向、非重叠域单实验可改任意参数、重叠域三层九实验）· `https://www.uxren.cn?p=58841/`（UXRen，快照逐字：三目标与四种分配函数、流量偏置）。**第三~五独立域·教学/厂商立场，逐条登记、不作唯一结论来源**。
- **失败与降级如实登记（rules/08 §二）**：`https://research.google/pubs/overlapping-experiment-infrastructure-more-better-faster-experimentation/` → **WebFetch fetch failed**；`https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36900.pdf` → **fetch failed**；`https://docs.statsig.com/experiments-plus/layers` → **WebFetch 200 但命中 Statsig 自家 gate-check 404 页**（原文逐字 `HTTP 404 · gate returned false / path: /experiments/layers / reason: Unrecognized`），按「页面不存在」登记**不作信源**；Google 论文 PDF 全文未取得 ⇒ 本节所有「原文」均出自**中文全译稿逐字**，不冒充英文原文一手，论文结论以译稿口径登记。
- **判非 / 换道**：`overlapping experiment` / `流量饥饿` / `发布层` / `Launch layers` / `f(cookie, layer)` / `正交分层` / `配置即代码` 全库 `SKILL.md` **0 命中**；`carryover effect` 1 命中属 `meta/agent-evolution` §21（时间维度 switchback 残留效应，**异命题**，按「合」登记不重述）；`SRM` / `Sample Ratio Mismatch` / `样本比例` / `chi-square` / `卡方` / `Fabijan` 命中集中在 `engineering/wb-agent-evaluation` §9（已成一节 3 独点）+ 本技能 §17 ⇒ 按 rules/07 四态判「**换道**」：本轮不重做 SRM，改取「并发实验空间结构」这一未覆盖轴；`layer` / `domain` 各 15/16 命中均为通用词（层级/领域），非本命题。模块 `AI/MEMORY.md` §15 漂移/canary、§16 bandit、§17 peeking/OPE、§18 performative、§19 CUPED、§20 时间效应、§21 SUTVA 均异命题、不复用。与 r756/r755/r754 九模块结论不复用。**豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地**。
- **未采纳**：论文中 cookie 模 1000/42 的具体常数、`5.2.1 样本量` 公式与实验委员会流程、发布层 YAML 语法、伴鱼 Grpc protobuf 接口与白名单实现细节、厂商「每天上百实验」量级数字、41 度蓝轶事。

## 二十三、安全探索：策略优化时「学的过程」本身要被约束，不只最终策略（r760A 独立实拉 2026-11-17，≥3 独立域一手交叉，3 独点）

> 定位：本节管「**agent 在试错/自适应优化过程中，中间策略会不会先闯祸**」。与 §15–§22 分工：那八节全是「怎么把策略改对、改对没对」（漂移/验收/bandit/OPE/peeking/performative/CUPED/时间/SUTVA/并发分层），前提是**试错本身无害**；本节补上这个前提不成立时的机制——当探索动作有不可逆代价（真实环境、生产系统、金钱、物理安全），须把「安全」独立于「性能」做成一道硬约束层。与 `system/si-safety-governance` 分工：那条管静态工具/权限/供应链安全，本节管**学习/优化回路中的在线动作过滤**。与 `meta/ti-critical-reasoning` §10.3（monitorability tax / 不优化推理链）正交：那条防「监督通道被优化掉」，本节防「探索动作造成不可逆损害」，两者都是 Goodhart 家族但约束对象不同。

### 23.1（r760A-1）安全探索约束的是整条策略序列的中间态，不是只看最终策略；初始策略豁免但之后每步都有违规概率上界
- **原文**（NSF PAR《Safe Exploration in Reinforcement Learning by Reachability Analysis over Learned Models》一手全文逐字）：定义安全规格 `φ` 为「a quantifier-free Boolean combination of linear inequalities over the environment state variables」，`s |= φ` 当且仅当 `φ(s)` 为真；安全探索定义为「a learning process π0, π1, …, πT such that πT = π* and ∀1≤j≤T, 0≤t≤H, P_{ζ∼πj, s_t∈ζ}(¬φ(s_t)) < δ」——「the end goal is for the final policy πT to optimize long-term rewards, while **each intermediate policy (excluding π0) is constrained to a limited probability δ of unsafe behavior**. This definition does not place safety constraints on π0 as the environment dynamics is not known and hence π0 can exhibit arbitrary (unsafe) behavior」。
- **判据**：① 「最终收敛到最优」与「学习途中不闯祸」是**两个独立约束**，只验收前者等于把试错成本甩给环境；报告安全结论须写明是对**整条序列** `π1..πT` 的违规概率上界 δ，不是对最终策略的一次测量。② `π0` 豁免是有前提的——**环境动态未知**，所以初始的任意行为是信息获取代价；一旦拿到数据建了模型，豁免即失效，不能拿「初始阶段」当永久放行理由。③ δ 与视界 H 必须同时声明：同一个 δ 在 H=10 与 H=10⁴ 上的累积暴露完全不同，只报「违规率 <δ」不报 H 是半句结论。④ 落地到自适应策略：每次策略改写都是一次 `πj→πj+1`，须有「这一步会不会把系统带出安全状态集」的显式检查，而不是等回测指标变坏再回滚（与 §15 变点检测分工：那是事后发现性能漂移，这是事前约束动作）。

### 23.2（r760A-2）shield 分前置/后置两种干预位；「没有安全动作」在形式上算不出 shield，只能降安全要求，不能硬凑
- **原文**（《Shields for Safe Reinforcement Learning》TU Graz/Elsevier 综述 PDF，WebFetch 取 PDF 失败后 curl + pypdf 提取 9 页 50,650 字一手全文逐字）：「**post-shielding**：The shield is positioned between the agent and the environment, continuously monitoring … classifies the action as safe or unsafe, and **replaces any unsafe action with a safe one**」；「**pre-shielding**, in which the shield provides a list of all safe actions, allowing the agent to select the best available option」；「it is **formally not possible to compute a shield if no safe action exists**. In such cases, the practical solution is to **lower the safety requirements, if possible**」。PPO / Deep Q-learning 有 masked 版本「that take a list of forbidden actions as extra input, making pre-shielding simple to integrate」，此时最终选择权仍在算法；无 masked 版本时 pre-shield 难接。post-shield 易接（直接覆写）但有两个副作用：「First, by overwriting the agent's actions, the shield may **slow down the exploration** … can often select a 'good' alternative … such as choosing an action **similar to the one originally selected** … ranked list … choose the **second-best option**. Second, a post-shield can **disrupt the association between an action and its reward**. To address this, **the reward should be tied to the action chosen by the shield rather than the agent's original choice**」。
- **判据**：① 两种 shield 的**决策权归属不同**：pre-shield 给白名单、agent 自选（可解释性/可控性保留在策略层），post-shield 直接替换（策略层看到的动作与实际执行的动作不一致）。选哪种先看「策略层是否需要知道自己被拦了」。② **无安全动作 = 形式无解**，正确动作是报告「此状态无可行安全动作」并降低/放宽规格，不是随便挑一个「看起来最不坏」的——后者是悄悄把安全约束降级成启发式。③ 后置 shield 的两个副作用是**验收必查项**：探索被拖慢（要选相近替代/次优项缓解）与动作-奖励错配（**奖励必须绑 shield 实际执行的动作**，否则策略学到的是「我原本的动作得了奖」而真实执行的是另一个，反馈彻底失真）。④ 落地：任何「护栏层/拦截器/过滤器」接进自适应回路时，都要写清它属于前置还是后置、无可行解时的降级路径、以及奖励/反馈绑的是谁的动作（与 §20.3 代理指标分工：那条说代理指标别直接优化，这条说反馈信号要绑到真实执行的动作）。

### 23.3（r760A-3）安全规格必须与学习目标形式分离，且「绝对保证」与「概率保证」是两种承诺；shield 自带保守偏差与可扩展性上限
- **原文**（同上 Shields 综述 PDF 一手全文逐字）：shield「are rigorously computed from a **formal specification of safety-critical properties** and an **abstract model of the environment**. This specification distinguishes permitted (safe) and forbidden (unsafe) behaviors and is **independent of the agent's learning objective**. Thus, a shield maintains a **clear separation between an agent's safety and performance**」；推导技术含「reactive synthesis, supervisory control, theorem proving, or model checking」；保证分两种——「When using **deterministic models** … safety as a **qualitative, absolute** measure … specified safety-critical properties are guaranteed to **never be violated**, regardless of what may occur in the environment in the future」，而现实场景「absolute safety guarantees may be unrealistic」（UAV 无法排除与不规则飞行器相撞），概率模型下「An action is deemed unsafe if it induces an **unacceptably high risk** … classified as safe if **this probability is below some threshold**. By adjusting this threshold, shields can be generated that are either more liberal or more restrictive」。局限：「shielding suffers inherently from the limitations of model-based verification … state-of-the-art shielding approaches are able to handle environments with **billions of states**, real-world applications may demand far larger scalability」。另（arXiv 2505.17342v2《A Survey of Safe RL and Constrained MDPs》WebFetch 200 全文逐字）：「Shielding approaches have the advantage of **hard safety** (no violations in theory), but they often rely on having additional knowledge … They also may introduce **performance bias** (the agent might become too conservative if the shield is not carefully designed, since it never experiences certain parts of state space). Combining shielding with CMDP-based learning is an interesting direction: one can use shielding in early training and **gradually lift it** as the agent's own policy becomes safe」；Dalal 2018 安全层用 QP 最小调整动作、「guaranteed zero constraint violations during training」但需模型；Alshiekh 2018 / ElSayed-Aly 2021 用形式化验证 + 时序逻辑预计算禁入状态-动作对。
- **判据**：① 安全规格必须**独立于学习目标**写死（允许/禁止行为清单 + 抽象模型），不得让被优化的策略自己定义什么叫安全——否则又是 Goodhart（与 §10.3 推理链不优化同构，但对象是动作）。② 报「安全保证」须标明是 absolute（确定性模型、理论上永不违反）还是 probabilistic（低于阈值即放行、阈值可调松紧），两者承诺强度差一个量级，混用会误导。③ shield 有**保守偏差**：被屏蔽的状态-动作空间策略永远见不到，可能过度保守；故工程上取「早期强 shield + 策略学会安全后逐步 lift」，而不是全程硬罩。④ 适用场景有硬上限：模型检查虽可到十亿状态，现实更大系统仍不可扩展；安全能力受限于模型准确性（与 §15 "换指标须重标阈值"呼应：抽象模型换了，shield 须重算重验）。⑤ 与 CMDP（把代价进约束 `J_c ≤ d`，拉格朗日法）是**两条互补路径**：shield 给硬保证但需外部知识，CMDP 从数据学约束但只有期望意义的安全；报告里两者不可互相冒充。

**来源（r760A 独立实拉 2026-11-17，≥3 独立域一手交叉；原选 reward hacking/monitorability 主题因与 `meta/ti-critical-reasoning` §10.3 r731A 重叠 >60% 按去重铁律换题）**：
- `https://tugraz.elsevierpure.com/ws/portalfiles/portal/93576031/Shields_for_Safe_Reinforcement_Learning.pdf`（《Shields for Safe Reinforcement Learning》TU Graz/Elsevier 综述，WebFetch 判 PDF 拒读 → **curl 200 下载 4.72MB + pypdf 提取 9 页 50,650 字一手全文逐字**）— pre/post-shielding 两干预位、无安全动作形式不可算只降规格、masked PPO/DQ 集成、post 两副作用与 reward 绑 shield 动作、形式规格独立于目标、absolute vs probabilistic、billions of states 可扩展性。**第一独立域·综述一手**。
- `https://par.nsf.gov/biblio/10511029/media/xml`（NSF PAR《Safe Exploration in Reinforcement Learning by Reachability Analysis over Learned Models》一手全文逐字）— 安全规格 φ 定义、安全探索形式定义 `∀1≤j≤T, P(¬φ)<δ`、π0 豁免理由、VELM 用学习模型+reachability 算 shield、shield 拦截不安全动作替换为 π′ 安全动作、相对 SPICE 每个时间步调 QP 的计算效率优势。**第二独立域·论文一手**。
- `https://arxiv.org/html/2505.17342`（arXiv 2505.17342v2《A Survey of Safe RL and Constrained MDPs》WebFetch 200 全文逐字）+ `https://arxiv.org/pdf/2505.17342v2`（PDF 快照交叉）— Figure 12 shield pipeline、安全层 QP 最小调整 Dalal 2018 零违反、formal methods shielding Alshiekh 2018/ElSayed-Aly 2021 multiagent、human/oracle intervention Saunders、Lyapunov actor-critic Chow 2018、hard safety + performance bias + 早期 shield 逐步 lift、CMDP 结合方向。**第三独立域·综述一手**。
- **判非 / 换道**：原选 `reward hacking` / `monitorability tax` / `obfuscated reward hacking` / Baker 2503.11926 命中 `meta/ti-critical-reasoning` §10.3（r731A 已落三条独点）+ 豆包自留地 `wb-context-compressor`（WB 0 落地）⇒ 按去重铁律四态判「**换道**」，不重述、不改 TI 技能，改取 AI 模块未覆盖的「探索过程安全约束」轴；`safe exploration` / `安全探索` / `CMDP` / `约束马尔可夫` / `安全动作` / `shield` 全库 SKILL.md **0 命中**；`Thompson` / `UCB` / `LinUCB` / `contextual bandit` / `regret` 命中集中在本技能 §16（bandit 探索/OPE，异命题，按「合」不重述）与 `wb-artifact-verification`（contextual bandit 异命题）；`Bayesian optimization` 命中豆包自留地（WB 0 落地）。与 §15 漂移、§16 bandit、§17 peeking、§18 performative、§19 CUPED、§20 时间、§21 SUTVA、§22 并发分层逐条分工，均不并存。与 r759/r758/r757 九模块结论不复用。**豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地**。
- **未采纳**：VELM 的 reachability 具体算法与符号模型公式细节、QP 求解器实现、LTL 时序逻辑语法、Safety Gym benchmark 具体分数、CMDP 拉格朗日对偶推导、risk-sensitive CVaR 目标函数（异命题，留给后续）。

## 二十四、持续学习的灾难性遗忘：改完就忘是默认态，保留旧能力要靠显式机制（r764A 独立实拉 2026-11-18，≥2 独立域一手交叉，3 独点）

> 自改进闭环每轮改提示/改参数/改规则，本质是**连续任务学习**。默认顺序训练会把旧任务编码过的参数用新任务覆写——「灾难性遗忘」不是异常，是不加约束时的默认结果。「改到新版指标涨了」不等于旧能力还在（与 §18 performative「改到不改了≠改对了」同族，但本章管的是能力保留）。

- **r764A-1 ★先声明任务身份在测试时是否可得，再选方法与评测口径**：continual learning 三场景不是同一道题——Task-Incremental（测试时有 task ID，输出空间每任务独立 head，关键在保每任务参数，最易）／Domain-Incremental（测试时无 task ID，输出共享，关键在抗 domain shift，中等）／Class-Incremental（测试时无 task ID，输出空间随任务增长，关键在区分所有类，最难）。AI Wiki 逐字表：Task ID at test time=Yes/No/No、Output space=Separate head per task/Shared across tasks/Grows with each task、Classic benchmark=Split MNIST (with task ID)/Permuted MNIST/Split MNIST (without task ID)。⇒ 自改进台账先登记「这次升级后，旧能力还会被显式点名调用吗」：能点名（task ID 可得）与不能点名（共享一个入口、类数还在涨）是两种难度，后者才是真实 agent 场景；拿 Task-IL 的通过率宣布 Class-IL 已解决是口径错配。

- **r764A-2 ★EWC 是逐参数二次锚定，不是全局 L2；且「保旧」有硬前提**：EWC（Kirkpatrick et al. 2017 PNAS）把旧任务 posterior 近似为以 θ*_A 为均值、精度由 Fisher 信息矩阵对角线给出的高斯，损失 `L(θ)=L_B(θ)+Σ_i (λ/2)·F_i·(θ_i−θ*_A,i)²`——高 Fisher 参数被重罚、低 Fisher 参数放自由改（AI Wiki 逐字：「Parameters with high Fisher information … penalized more heavily, while parameters with low Fisher information are left free to adapt」）。它是 per-parameter 各向异性弹簧，与 L2「一律同等压小」不同。但一手综述（arXiv 2112.14146）列三条边界：① Fisher 对角线精确计算复杂度随输出数线性增长，「limiting the applicability of this method to low-dimensional output spaces」；② 二次惩罚项「only derived for the two-task case in the original paper」，多任务合理性被 Huszár 2018 质疑；③ Kemker 2018 实证「EWC fails to learn new classes incrementally in response to accumulating training data」。Online EWC（Schwarz 2018）用 Fisher  running average 把每任务一份矩阵压成单一惩罚项以支撑多任务。Synaptic Intelligence（Zenke 2017）在训练中在线累积每个参数对降 loss 的贡献分，EWC 是每任务结束后离线算——两者在 Permuted MNIST 性能相近。⇒ 声明「旧能力已保留」须附：锚的是哪些参数/用什么重要性度量/几任务场景/是否用了在线近似；单任务对单任务的 EWC 通过率不能外推到持续累积类。

- **r764A-3 ★稳定性—可塑性是权衡不是优化目标；replay 三族的代价各不同**：一手综述逐字「balancing stability of existing representations with the plasticity required to efficiently learn new ones is a major unresolved topic of research in continual learning」，CLEAR 用 off-policy+行为克隆换稳定、on-policy 保可塑。正则化之外 replay 三族：原始缓冲（CLEAR「might prove unsuitable in cases where storage of a complete memory buffer is intractable」）／生成式重放（Deep Generative Replay 用生成模型造旧任务代表数据混进新数据）／压缩索引重放（REMIND 用 product quantization 压表征，「store one million compressed representations compared to just 20,000 when raw data input is stored」，同等内存下 50 倍）。GEM 类用情景记忆梯度约束更新方向（AI Wiki：gradient episodic memory 每任务存 M_k，既降当前 loss 又不让旧任务 loss 升）。⇒ 自改进留旧能力时按「存什么」选型：能存原始样本→ER；不能存数据但能训生成模型→生成式；内存受限→压缩表征；都不行才退正则化锚参数。验收必须同时报「新任务达标」与「旧任务回退幅度」两栏，只报前者等于没测遗忘。

**来源（r764A 独立实拉 2026-11-18，≥2 独立域一手交叉）**：
- `https://arxiv.org/html/2112.14146`（arXiv 2112.14146《Towards continual task learning in artificial neural networks: current approaches and insights from neuroscience》WebFetch 200 全文逐字）— EWC 公式与三限制（Fisher 对角随输出线性/二次项只对两任务推导/Kemker 2018 增量类失败）、SI 在线锚定、LwF 蒸馏与训练时间随任务线性、CLEAR 稳定性可塑性、Deep Generative Replay、REMIND 100万 vs 2万、stability-plasticity tradeoff。**第一独立域·一手综述**。
- `https://aiwiki.ai/wiki/continual_learning/revisions/4`（AI Wiki continual_learning 条目 WebFetch 200 全文逐字）— 三场景逐字对比表（Task ID/Output space/Key challenge/Difficulty/Best methods/Benchmark）、三方法族、EWC quadratic + Fisher diagonal、Online EWC running average、SI online vs EWC offline。**第二独立域·一手百科**。
- 快照交叉（不冒充一手全文）：`https://mbrenndoerfer.com/writing/online-offline-continual-learning-world-models/catastrophic-forgetting`（Fisher 定义式与 GEM 投影逐字）· `https://www.edgechat.ai/elastic-weight-consolation`→实为 elastic-weight-consolidation（PNAS Kirkpatrick 2017 存在性与 8000+ 引用、λ=5000 建议、TransE 12.62%→6.85% 45.7% 降幅）· `https://crad.ict.ac.cn/.../2022-06-1213.shtml`（中文综述 EWC/GEM/RWalk 公式交叉）。
- **判非 / 去重**：`灾难性遗忘` / `catastrophic forgetting` / `continual learning` / `持续学习` / `EWC` / `弹性权重整合` 在本技能（agent-evolution）正文 **0 命中**；全库命中在 `engineering/wb-agent-evaluation` r568A（ServeLearnBench 用 Continual Harness 做演化环境评测——评测构造维度，异命题）与豆包自留地 `wb-context-compressor`/`wb-teaching`（口号级，WB 0 落地）。与本章「能力保留机制」不同命题，按「合」不重述、不改那些文件。与 §16 bandit 探索、§18 performative、§23 安全探索逐条分工。与 r763/r762/r761 九模块结论不复用。**豆包自留地 WB 0 落地**。
- **未采纳**：Fisher 信息矩阵完整推导、Kronecker-factored 近似实现、product quantization 算法细节、各 benchmark 具体分数、λ 交叉验证网格（工程实现细节，留给后续）。

## 二十五、优势估计的偏差—方差旋钮：GAE 用一个 λ 在「信 critic」与「信采样回报」间插值（r768A 独立实拉 2026-11-19，≥2 独立域一手交叉，3 独点）
> §23 管「学的过程安全」、§24 管「改完别忘」，本章回到策略梯度本身的信号质量：**策略梯度的方差几乎处处是瓶颈，而优势估计器是那个旋钮**。REINFORCE 用整局回报当优势（无偏但方差爆炸），一步 TD 用 critic 自举（低方差但有偏且完全依赖 critic 准不准）。GAE（Schulman et al. ICLR 2016）不二选一，而是对所有 n-step 优势做指数加权，把偏差—方差变成一个连续滑块 λ。
- **r768A-1 ★GAE 是所有 n-step TD 误差的指数加权和，λ 是唯一旋钮；两个端点分别是 TD(0) 与 MC**：定义单步 TD 误差 `δ_t = r_t + γV(s_{t+1}) − V(s_t)`（critic 的「一步意外」：实际转移比 V 预测好多少）。GAE 定义 `A_t^GAE(γ,λ) = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}`，实现用反向递推 `A_t = δ_t + γλ A_{t+1}`（终态 `A_T=0`，一次反向扫描即可、无需显式求和）。推导关键：k-step 优势可望远镜成 TD 误差和 `Σ_{l=0}^{k−1} γ^l δ_{t+l} = G_{t:t+k} − V(s_t)`；GAE 就是把硬截断 k 换成对 δ 的指数衰减 λ^l。两端点（aiwiki/Chemnitz 讲义逐字一致）：**λ=0 ⇒ A_t=δ_t**（一步 TD，只用一个转移+一次价值查询，方差最低，但未来被 critic 的 V(s_{t+1}) 替代，critic 的偏差直接灌入）；**λ=1 ⇒ A_t=G_t−V(s_t)**（蒙特卡洛优势，全程用真实回报故无偏，但聚合整条轨迹噪声、方差随视界增长）。⇒ 调 GAE 就是调「远近 TD 误差各自占多少」：中间 λ 保留每个 horizon、用 (γλ)^l 压低远处更吵的项，近处信采样、远处信 critic。
- **r768A-2 ★γ 与 λ 是两个不同的旋钮，且偏差只在 critic 不完美时才出现**：一手逐字（braindrip）「γ defines the effective planning horizon (part of the MDP definition), while λ controls the estimator's bias-variance properties」——γ 属 MDP 定义（多远算未来），λ 属估计器属性（偏差—方差权衡），混淆两者是常见错误。更关键的一条：**「When V_φ is perfect, all values of λ produce unbiased estimates. The bias-variance trade-off only arises because V_φ ≠ V^π in practice」**——即 GAE 的偏差不是 λ 自带的，是 critic 近似误差带来的；λ 只决定「在多大程度上暴露于 critic 误差」。实践甜点 λ≈0.95（PPO/TRPO 默认，Schulman 原论文报 λ∈[0.93,0.99] 在多种 MuJoCo 连续控制任务上稳健），λ∈[0.9,0.99] 多数环境良好。⇒ 落地顺序：先评估 critic 质量——critic 准（状态空间小/拟合好）可把 λ 调小以降方差提速；critic 噪声大或环境随机（如 LLM RLHF 巨大状态空间、价值函数必然不完美）则调大 λ 更依赖真实观测回报；λ=0 配一个错 critic 会把策略直接带偏，不是「保守」。
- **r768A-3 ★GAE 不是纯降噪正则、也不是 TD(λ)；critic 目标要用 λ-return 且两者都从采样期 critic 算**：三条易错点逐字澄清：① 误区「GAE 只是平滑噪声的正则技巧」——错，λ 设错「fundamentally changes what signal the policy receives」，λ=0 配错 critic 让策略朝错误方向走（theneuralbase）。② **GAE(λ) ≠ TD(λ)**：TD(λ) 用资格迹更新价值函数，GAE(λ) 用同一指数加权为策略梯度估优势——数学形式相同、用途不同（braindrip）。③ 带 GAE 时 critic 的回归目标不是一步 TD 而是 **λ-return** `R̂_t = A_t^GAE + V_t^old`，且「Both A_t^GAE and V_t^old are computed from the data-collecting critic and held fixed during the update of φ」（arXiv 2606.16733 逐字）——采样期 critic 算出的优势与目标在更新 critic 时当作常数，避免在线移动目标。另外优势通常在 batch 上做零均值单位方差归一化以稳定学习率；`E_{a~π}[A(s,a)]=0`（优势恒中心化，有正有负）。⇒ 自改进/策略优化落地四件套：δ_t 定义、λ 按 critic 质量选、critic 目标用 λ-return、优势 batch 归一化；缺一件都会让「方差降了」的假象掩盖信号被改坏。
**来源（r768A 独立实拉 2026-11-19，≥2 独立域一手交叉）**：
- `https://arxiv.org/abs/1506.02438`（Schulman/Moritz/Levine/Jordan/Abbeel《High-Dimensional Continuous Control Using Generalized Advantage Estimation》arXiv:1506.02438 v6，WebFetch 200 一手摘要逐字）— 原文「value functions to substantially reduce the variance of policy gradient estimates at the cost of some bias, with an exponentially-weighted estimator of the advantage function that is analogous to TD(lambda)」、trust region 第二挑战、3D 双足/四足 locomotion。**第一独立域·原论文一手**。
- `https://aiwiki.ai/wiki/policy_gradient`（AI Wiki policy_gradient 条目 WebSearch 一手逐字）— GAE 定义式与 δ_t、 Schulman et al. ICLR 2016「exponentially-weighted estimator analogous to TD(λ)」「reduce variance at the cost of some bias」、λ=0.95–0.97 标准、PPO/TRPO/IMPALA 采用、variance-reduction 技术表、与 RLHF/InstructGPT 的关系。**第二独立域·一手百科**。
- 交叉快照（不冒充一手全文）：`https://samyarmodabber.github.io/course-deeprl-vitay/slides/pdf/2.5-TD.pdf`（Chemnitz  Deep RL 课程 PDF，`A^GAE=(1−λ)Σλ^nA^n=Σ(γλ)^kδ_{t+k}` 两式与两端点逐字）· `https://notes.lukasl.dev/Knowledge/Generalised-Advantage-Estimation`（递归式与两端点偏差—方差机制逐字）· `https://mbrenndoerfer.com/writing/ppo-algorithm-proximal-policy-optimization-reinforcement-learning/generalized-advantage-estimation`（λ=0.95 sweet spot、边界条件 A_T=0、反向递推逐字）· `http://theneuralbase.com/rlhf-theory/learn/intermediate/gae-generalized-advantage-estimation`（λ 偏离 1 的"common misconception"与 critic 好坏如何定 λ 逐字）· `https://braindrip.blog/courses/reinforcement-learning/04-policy-gradient-methods/advantage-estimation`（γ≠λ、V 完美时各 λ 均无偏、GAE≠TD(λ)、A 中心化逐字）· `https://arxiv.org/html/2606.16733`（λ-return `R̂_t=A^GAE+V_t^old` 与「held fixed during update of φ」逐字）· `https://zhangyongtian.github.io/.../基线原理与优势函数公式推导`（中文推导 λ=0.95 PPO 甜点交叉）。
- **判非 / 去重**：`广义优势估计` / `GAE` / `generalized advantage estimation` / `优势估计` / `λ-return` 全库 SKILL.md **0 命中**（初判 GAE 命中 `wb-context-compressor` 经核为 self-consistency 语境异命题、且属豆包自留地 WB 0 落地）。与本章 §16 bandit 探索/regret、§23 安全探索、§24 持续学习逐条分工——那三章管「学什么/学得安不安全/别忘」，本章管「策略梯度信号本身的方差—偏差」。与 §19 CUPED 区别：CUPED 用实验前协变量做结果方差缩减（频率派实验估计），GAE 用 TD 误差指数加权做优势估计（RL 策略梯度），两者的"方差缩减"分属不同统计对象，不并存。与 r767/r766/r765 九模块结论不复用。**豆包自留地 WB 0 落地**。 **未采纳**：GAE 的完整理论证明（Schulman 原论文 §4 的 λ 与 γ 联合偏差界）、PPO clip 机制细节、MAPPO 多智能体 GAE、Retrace/V-trace off-policy 校正、GRPO 去 critic 路线（异命题，留给后续）。
## 二十六、异质性处理效应与因果森林（r772A 独立实拉 2026-11-19，≥2 独立域一手交叉，3 独点；正文下沉 `references/r772A_异质性处理效应与因果森林.md`）：§19 CUPED 估准整体 ATE、§21 SUTVA 管随机化独立，均只给平均效应；本章管「同一处理对不同人效果可能相反、ATE 把异质性平均掉」——ULE+unconfoundedness 下用因果森林估 CATE τ(x)。**独点1** honest splitting（构树/估计集分离）+ 分裂准则最大化处理效应异质性（非最小化 MSE），Wager&Athey JASA2018 证 pointwise consistent + 渐近正态 + 可构造置信区间，无关协变量多时强于最近邻匹配。**独点2** 变体分工：Causal Forest（直接平均诚实树 CATE）/ GRF（梯度分裂+importance weights 进局部矩条件，推广出 unconfoundedness）/ DML（DR efficient score 回归低维 CATE）/ DR-learner（高维 CATE 带 oracle 误差上界）/ mcf（多处理、CATE 的 MSE 找分裂），选型先对「统计推断/内部一致/新数据仅凭协变量预测」三性质表。**独点3** τ(x) 是条件平均非 ITE、依赖 unconfoundedness、pointwise 尾部方差大；输出 CATE+置信区间作差异化决策输入层，接 §十五 VOI 判「该 subgroup 再收集信息值不值」、§二十深不确定准则处理区间跨 0。判重：causal forest/因果森林/CATE/DML/GRF 全库本体 0；与 §19/§21/§25 分工不并存，豆包自留地 WB 0 落地。**三独立域逐字来源 + 判非全段见下沉文件。**

## 二十七、Hyperband：固定预算下的多保真资源分配（r776A 独立实拉 2026-11-19，≥2 独立域一手交叉，3 独点；正文下沉 `references/r776A_Hyperband多保真资源分配.md`）：§16 bandit 管「在线自适应怎么分试验预算以最小 regret」，本章管「一次性超参搜索怎么把有限训练预算在候选间重分配」，同用 bandit 语言但目标与部署形态不同。**独点1** 把 HPO 写成 pure-exploration non-stochastic infinite-armed bandit，预算（迭代/样本/特征）分配给随机采样配置，靠 adaptive resource allocation + early-stopping 加速随机搜索（JMLR 2018 报 order-of-magnitude speedup）。**独点2** Successive Halving 的两难是候选数 K 与单候选预算 B/n 不能同时最大：K 大 budget 小会早停误杀慢热候选、K 小会把资源浪费在差配置；envelope 宽度与终损间距决定何时可区分，故首轮预算不是越小越好。**独点3** Hyperband 用 bracket 网格枚举多组 (K,b) 把两难交给预算自动扫（s_max=⌊log_η R⌋, B=(s_max+1)R, K=⌈Bη^s/(R(s+1))⌉, b=Rη^{-s}；s=s_max 最激进、s=0 即随机搜索），用户只给最短检查时间与最长 deadline；但 bracket 相互独立、下个 bracket 仍随机采样浪费前序信息，BOHB 用 TPE 补。判重：Hyperband/successive halving 本体 0（§19 判非句自我登记除外）；豆包自留地 WB 0 落地。**三独立域逐字来源 + 判非全段见下沉文件。**
## 二十八、贝叶斯优化：评估很贵时，用代理模型决定「下一个试哪个配置」（r780A 独立实拉 2026-11-20，≥3 独立域一手交叉，3 独点；正文下沉 `references/r780A_贝叶斯优化与采集函数.md`）：§27 Hyperband 管「固定预算怎么在随机候选间重分配训练资源」，本章管「每次评估都很贵、无法求导时，用历史观测建概率代理并主动选下一个评估点」——一个改资源分配、一个改选点方式，可叠加不合并。**独点1** BO=概率代理+采集函数两段式，适用「黑盒/昂贵/有噪/无梯度」；GP 后验给 μ（均值）与 σ（不确定性），采集函数把两者合成选点准则，目的是「不陷进第一个局部最优」；GP 精确推断 O(n³) 且观测数通常只在数十到数百，n 上千即失去便宜前提。**独点2** EI/PI/UCB 三种采集函数是同一权衡的不同旋钮：EI 无额外参数、PI 由 ξ 从利用推向探索、UCB 由 κ 增大探索；三者流行的真原因是可微、易算、能用 L-BFGS-B 直接最大化；LCB 是把「纯探索的 σ」repurpose 成 μ−κσ。报告「用了 BO」须写代理/采集函数/旋钮值/当前最优定义四件。**独点3** 解析采集函数只对顺序单点有效，并行批/异步下 intractable，须换 Monte Carlo 采集（reparameterization + Cholesky 下三角 L + 随机优化器 Adam），异步把 pending points 当 fixed 处理；三类扩展 multi-fidelity（便宜近似加速）/batch（并行机会）/高维（降维或结构核）各有存在理由。判重：BO 本体全库 0 专节（豆包自留地 DSPy MIPROv2 一句 WB 0 落地；§16 bandit 最小 regret 异命题）⇒「优＝加厚现有」。**三独立域逐字来源 + 判非全段见下沉文件。**
## 二十九、元学习 / MAML：学的是「几步就能适配新任务」的初始化，不是单任务最优权重（r784A 独立实拉 2026-11-20，≥2 独立域一手交叉，3 独点；正文下沉 `references/r784A_元学习MAML.md`）：§24 持续学习管「别忘旧任务」、§27/§28 管「搜索怎么分配/选点」，本章管「跨任务学一个对梯度敏感、少量样本即可适配的初始化」。**独点1** 双层优化=内循环 `θ'=θ−α∇L_T(D_tr)` 支持集适配 + 外循环 `min_θ ΣL_T(θ',D_te)` 穿过内循环反传，目标是把 θ 放在梯度下降特别有效的区域；须声明任务分布/内外学习率/内步数三件。**独点2** 二阶导是代价核心；FOMAML 丢二阶近乎不掉性能、Reptile 不穿优化只把初始化朝适配后参数推、Meta-SGD 连逐参学习率一起学——同一目标的不同「过不过二阶/学不学逐参」旋钮。**独点3** 与迁移学习（为单一源任务优化）不同、需任务共享结构前提；任务太杂/分布太窄 meta-overfit，简单微调基线可追平 ⇒ 启用前先验任务共享性。判重：MAML/元学习/learn-to-learn 本体全库 0（artifact-verification 命中 RATED 在线 bandit 重排，异命题）。**两独立域逐字来源 + 判非全段见下沉文件**（WebFetch 200 全文：aiwiki + wikiprompt；arxiv 1707.02937 ID 抓错弃用如实登记）。
## 三十、基于势函数的奖励塑形：加中间奖励而不改变最优策略（r788A 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点；正文下沉 `references/r788A_基于势函数的奖励塑形.md`）：§23 安全探索管「学的过程受约束」、§28/§29 管「评估很贵/跨任务怎么学」，本章管「稀疏奖励下加中间奖励，怎样保证不改原本最优策略」。**独点1** Ng/Harada/Russell 1999 定理：势函数 Φ 有界但任意，塑形项 F(s,s′)=γΦ(s′)−Φ(s) 使 V~*=V*−Φ、Q~*=Q*−Φ 故最优策略不变；沿轨迹折扣求和望远镜抵消只剩 −Φ(s0)+γTΦ(sT)、终态势能为 0 时退化成只与起点有关的常数，策略序不变；非此形式的附加项会改最优策略（抓取奖励被反复抓取—松开刷分、悬停不拉抽屉）。**独点2** 定理不给「首选 Φ」：取 Φ=V* 时贪心即时塑形奖励即最优但 V* 未知；距离势 Φ=−d(s,goal)、γ=1 ⇒ F=d(s)−d(s′)；Wiewiora 2003 证 PBRS 等价于 Q 值初始化（Q-learning/Sarsa），Dynamic PBRS（Devlin & Kudenko 2012）势函数随 MDP 时间步变仍收敛，BSRS 是 MDP 步固定但训练步变——两个「动态」含义不同须分清。**独点3** PBRS 只保策略不变不保学得更快更稳，写不出势函数（「这段对话进展如何」）时不适用；线性变换 r′=pr+q(p>0) 也保策略不变但 indefinite horizon 下 q 大正/负诱发放弃或循环；与 §16 bandit 目标函数分裂、§23 安全规格独立分工，判重全库本体 0，豆包自留地 WB 0 落地。**两独立域逐字来源 + 判非全段见下沉文件**（WebFetch 200 全文：arXiv2501.00989 + Walking Labs 中文教程；growbotics/AAAI/ICAPS 交叉快照）。
## 三十一、课程学习：同一批数据按什么顺序喂，也是自适应旋钮（r792B 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点；正文下沉 `references/r792B_课程学习.md`）：§27/§28/§29/§30 管预算/选点/跨任务初始化/奖励塑形，本章管「单任务内数据顺序」。**独点1** 一门课程 = scoring function（人工先验/教师置信度/自身 loss 三路定难度）+ pacing function（难样本进池速度）；自步学习用当前 loss 自构课程免教师，但阈值升太慢会锁死难样本成反馈环（JMLR 逐字过拟合/不稳定 + TheoremPath 反馈环）。**独点2** 全局难度（最优假设处的 loss）vs 局部难度（当前假设处的 loss）解开「课程 vs 难例挖掘」矛盾：课程按外在全局难度排、同时不在对当前假设太易的样本上浪费时间；收敛率随全局难度单调降、随固定全局下的局部难度单调升；hard mining/boosting 降梯度方差、课程找好 basin，解不同问题非互斥。**独点3** 收益比直觉少（Wu/Dyer/Neyshabur 数千次训练：标准图像基准上随机增长池追平易到难，只在预算受限/标签有噪时明显获益）；窄课程烤进 shortcut；RL 晋升规则须多迭代平均+换关后等待+低失败率与长 episode 双条件，单迭代规则被噪声带跑。与 continual/active/transfer learning 分工：那些改任务或标签，课程只重排单一固定任务数据。判重：课程学习/self-paced/scoring/pacing 全库本体 0，豆包自留地 WB 0 落地。**三独立域逐字来源 + 判非全段见下沉文件。**
## 主动学习：用标注预算换信息增益，随机采样是必须报告的基线（r795L 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）

§27/§28 管搜索预算与选点、§31 管同一批数据的顺序，本章管**该给哪些样本打标**：在反馈昂贵时，让模型自己挑最有信息量的样本，而不是把预算均摊。
**独点1** 场景判据：须归入 pool-based（整池排序选样）/ stream-based（逐个到达即时决定标注或丢弃）/ membership query synthesis（合成新样本）三者之一；错分即错误条目。Settles 2009 逐字：主动学习让算法「choose the training data from which it learns」，以 fewer labeled instances 达更高精度。
**独点2** 子策略判据：least confidence（top1 概率最低）、margin（top1−top2 差最小）、entropy（分布熵最大）须分列，不得互相替代或混称 QBC；QBC 用委员会分歧、expected error reduction 用预期误差下降，计算代价高须显式说明。Gal 2017 逐字：许多采集函数依赖模型不确定性，而深度模型很少表示这种不确定性。
**独点3** 基线判据：声称「优于随机」须同时给 random baseline 与 cold start 处理（首轮模型太弱，常随机抽）；缺其一判证据不足。IEEE 逐字：不确定性采样是「the baseline every new method is measured against」，冷启动使早期 query 由过弱模型做出。
- **判重：`主动学习`/`active learning` 本体与全库 SKILL.md 0 命中；与 §16 UCB/Thompson（决策选臂）、§31 课程学习（数据顺序）分工不复用。豆包自留地 WB 0 落地。**
- **来源与诚信**：https://minds.wisconsin.edu/handle/1793/60660（Settles，Active Learning Literature Survey，TR1648，UW-Madison CS，2009，机构元数据页逐字摘要：核心思想 / oracle 查询）；https://proceedings.mlr.press/v70/gal17a.html（Gal/Islam/Ghahramani，Deep Bayesian Active Learning with Image Data，ICML 2017，PMLR 70:1183-1192，WebFetch 200 逐字：不确定性依赖 / 深度模型缺不确定性表示）；https://technav.ieee.org/topic/active-learning（IEEE Technology Navigator，访问 2026-11-22，WebFetch 200 逐字：不确定性采样为默认基线 / cold start 首轮随机）。Settles PDF 正文 WebFetch 不支持（application/pdf），只取机构元数据页摘要，未伪装成正文引文。 逐字全文与判非见 `references/r795L_主动学习.md`。
## 优先经验回放 PER：按 TD error 采样，用 IS 权重把偏差买回来（r796L 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）
§r795L 主动学习管「该标哪些新样本」，本章管**已有经验怎么复用**：均匀回放按经历频率重放，PER 按「学得还不够好」的程度重放，但会改变收敛解。
**独点1** 两变体都随 |δ| 单调：proportional `p_i=|δ_i|+ε`、rank-based `p_i=1/rank(i)`；论文逐字：rank-based「insensitive to outliers」更稳健。判据——只写「按 TD error 采样」不写明 proportional/rank-based 变体与其异常值敏感度，判不完整；均匀随机基线 = α=0 / 无 PER。
**独点2** 偏差必须显式纠正：`w_i=(1/N·1/P(i))^β`，β=1 完全补偿非均匀采样偏差；论文逐字：prioritized replay changes the distribution「in an uncontrolled fashion, and therefore changes the solution that the estimates will converge to」。判据——用了优先采样却没有 IS 权重纠正，判偏差未处理。
**独点3** 权衡与边界：优先回放导致 loss of diversity，用 stochastic prioritization 缓解、用 IS 纠偏；论文称 DQN+PER 在 41/49 款游戏胜过均匀回放（一手数字），但这是 Atari 设定不迁移为本仓阈值。罕见经验遗忘的原文措辞是「rapid forgetting of possibly rare experiences」，不要泛化写成「灾难性遗忘」当引用。
- **判重：`优先经验回放`/`PER` 全库 SKILL.md 0；与 §23 持续学习 EWC（防遗忘）、§r795L 主动学习（选新样本）分工不复用。豆包自留地 WB 0 落地。**
- **来源与诚信**：https://arxiv.org/abs/1511.05952（Schaul 等，DeepMind，ICLR 2016，arXiv:1511.05952，WebFetch 200 逐字：均匀回放按原始频率/41 of 49 games 胜过基线）; https://arxiv.org/html/1511.05952v4（WebFetch 200 逐字：两变体对 |δ| 单调且 rank-based 抗异常/改变分布即改变收敛解/diversity 损失/IS 纠正）。DeepMind 官方实现仓库未取到一手，第三方实现全排除；abs 与 html 为同论文两视图非两独立文档已如实登记。 逐字全文与判非见 `references/r796L_PER.md`。

## PPO 裁剪代理目标：信赖域与「迈多大步」（AI · r797C 2026-11-23）
§25 GAE 管优势怎么估、§30 PBRS 管奖励怎么设、§23 shield 管安全序列；本章管**每次策略更新步子多大**。
**独点1** 策略梯度不稳根因：更新改变访问分布，代理目标用旧 ρ 冒充新 ρ 是「一阶切平面近似」（fundamental lie），远离 π 即失真。Kakade-Langford 下界 η(π̃)≥L_π(π̃)−C·D_KL^max 给「留在信赖域内单调改进」保证，D_TV²≤½D_KL。
**独点2** TRPO 用自然梯度 F⁻¹g＋共轭梯度＋线搜索（Fisher 度量分布而非参数，昂贵）。PPO 论证＝「TRPO 保证在 mini-batch SGD 下本就没保住，理论既已近似就用便宜机制」：L^CLIP=E[min(rÂ,clip(r,1−ε,1+ε)Â)]，r=πθ/πold、ε≈0.2，min 让 ratio 越界方向无梯度激励 → 同批数据可多 epoch 复用，一阶 SGD 无二阶/共轭梯度/线搜索。
**独点3** clip 是软惩罚非硬保证（not a hard trust-region constraint，ratio 仍可跑远，usually prevents...not a hard guarantee）。RLHF 里预训练模型即信赖域、clip 保增量对齐不覆盖预训练能力；但 on-policy 不复用经验、样本效率低于 SAC、ε/lr/epochs 敏感。报「用了 PPO」写 ε/GAE λ/epoch 数/KL 系数四件。
判重：本体 0 专节（命中的是 shield masked-PPO 与 GAE 默认值语境）；豆包自留地 WB 0 落地。
来源与诚信：anthony0727.github.io《From TRPO to PPO》WebFetch 200 全文＋control.education/Emergent Wiki/inferensys WebFetch 逐字；Kakade-Langford 公式为文中转述标二手。逐字全文与判非见 `references/r797C_PPO裁剪代理.md`。

## 三十二、SAC 软演员-评论家：熵写进目标换 off-policy 样本效率（AI · r801C · 全文下沉）
> 最大熵目标 `J(π)=E[Σγ^t(R+αH)]`、soft Bellman log-sum-exp / Boltzmann 策略、twin Q min、squashed Gaussian、reparameterization、α 自动调节目标熵 `L(α)=E[−α(logπ+H̄)]`、对偶推断视角、与 PPO 分工及来源，全文见 `references/r801C_SAC软演员评论家.md`。本节仅留路由，以该 references 为准。

## 三十三、DPO 直接偏好优化：把 RLHF 重参数化成偏好对分类损失，权重才是机制（AI · r808B 2026-11-26 实拉，2 独立域一手 + 1 域边界交叉，3 独点；全文见 `references/r808B_DPO直接偏好优化.md`）

§r797C PPO 管「用 clip 限制每次策略更新的步子」，§r801C SAC 管「把熵写进目标换 off-policy 样本效率」；本章管「偏好数据如何不经过显式奖励模型与 RL 直接训练策略」，三者不是同一正则旋钮。
**独点1 隐式奖励重参数化**：从 `max E[r] − β D_KL[πθ||πref]`（π_ref=π_SFT，β 控偏离、保多样性防 mode-collapse）推出 `L_DPO=−E log σ(β log πθ(y_w|x)/π_ref(y_w|x) − β log πθ(y_l|x)/π_ref(y_l|x))`，隐式奖励 `r̂_θ=β log(πθ/π_ref)`；Bradley-Terry+logsigmoid 使偏好学习退化为二分类，无需 reward model/价值网络/采样步。
**独点2 梯度权重是核心**：`∇L=−β E[σ(r̂(y_l)−r̂(y_w))·(∇logπ(y_w)−∇logπ(y_l))]`；权重原文标注「higher weight when reward estimate is wrong」，按隐式奖励排错程度自适应；原论文明言去掉该系数的朴素版「can cause the language model to degenerate」。只做「chosen 加 SFT、rejected 当负样本」等权处理会丢掉机制。
**独点3 工程口径与边界**：两阶段（π_ref 采样成对 completions→人工标注成 D；固定 π_ref/β 优化 πθ）；无 π_SFT 时以 chosen 的最大似然初始化参考缓分布漂移。TRL 默认 sigmoid、β=0.1 且典型 0.1–0.5、β→0 即忽略参考；数据 `prompt/chosen/rejected`、model 与 ref_model 同架构；验收看 `rewards/accuracies` 与 `rewards/margins` 而非只看 loss；hinge/ipo/cDPO/robust 的 β 语义各异禁混报。边界：OOD 泛化、reward over-optimization、>6B 规模原论文自陈开放；条件等价反例（arXiv:2605.20834）证明当 RLHF 最优策略不偏好人类偏好回答时，DPO 只优化相对优势，可「loss 下降却更偏好 rejected」。
**来源与判非**：`https://arxiv.org/html/2305.18290v2`（WebFetch 200 全文，式 3/式 7/梯度/流水线/初始化/Limitations）· `https://huggingface.co/docs/trl/v0.8.0/dpo_trainer`（WebSearch 逐字；WebFetch 直连失败如实登记）· `https://arxiv.org/html/2605.20834` 摘要交叉。全库 DPO/直接偏好优化 0 专节，豆包自留地 WB 0 落地，按「增＝加厚现有」0 新建。

## 三十四、GRPO 组相对策略优化：用组内相对奖励当基线，去掉 critic（AI · r812B 2026-11-27 实拉，2 独立域一手交叉，3 独点；全文见 `references/r812B_GRPO组相对策略优化.md`）

§r797C PPO 管 clip 更新步幅、§r801C SAC 管熵目标换 off-policy、§r808B DPO 管偏好对分类损失；本章管 PPO 的优势基线从哪来——用一个问题多输出的组内相对分数替代需单独训练的 value 网络。§r768A 已把「GRPO 去 critic」标为异命题留后续，本轮补上。
**独点1 动机**：原论文摘要「variant of PPO ... optimizing the memory usage of PPO」；§4.1.1「GRPO foregoes the critic model, instead estimating the baseline from group scores」。双重理由：critic 常与 policy 同规模带来显存/计算负担；LLM 奖励常在末 token，逐 token value 难训准。省的是价值网络这一份资源，不是省奖励信号，基线从 learned value 换成 group score 估计。
**独点2 机制（逐字公式）**：每问采样 G 输出得奖励 r，按组均值/标准差归一化 `Â_it=r̃_i=(r_i−mean(r))/std(r)`，赋给输出全部 token；目标式 3 保留 PPO 的 min(clip ratio) 并把 KL 从 reward 项**挪到 loss 项**「avoiding complicating the calculation of Â_it」；KL 无偏估计（式4）`π_ref/π_θ−log(π_ref/π_θ)−1` 恒正。过程监督版每步奖励同样归一化、token 优势取其后各步归一化奖励之和。报「用了 GRPO」写 G/归一化方式/ε/β/KL 位置四件。
**独点3 边界与退化**：两个误解——省掉的是 learned critic 不是奖励（改规则可验证：答案对错/测试通过），也不是通用训练法（开放写作无可自动裁判即不适用）；一组输出全对或全错时 std→0 优势信号消失，依赖题目难度分布；可验证奖励仍受判题器/测试覆盖制约可 reward hacking，输出变长≠推理更强须正确率+泛化证明；组内归一化不天然更稳，质量受组大小/采样分布/奖励方差影响。判重：本体仅 §r768A 一句异命题 + GEPA 来源一句，非机制专节；module-memory AI 0、co-learn 标题级 0，豆包自留地 WB 0 落地。
**来源与判非**：arXiv:2402.03300《DeepSeekMath》HTML v3（WebFetch 200 全文逐字：摘要/§4.1.1 动机+式3+式4/§4.1.2 outcome 归一化/§4.1.3 process 归一化）+ abs 页（逐字摘要，Submitted 2024-02-05）· toolnavs/aigcbaba/CSDN 教学页 WebSearch 逐字交叉（组均值基线/全对全错信号消失/两个误解，40–50% 显存挂教学页口径不作硬结论）· alphaxiv 2609.04063 虚假优势边界登记。按「增＝加厚现有」0 新建。

## 三十五、CQL 保守 Q 学习：离线 RL 里压低 OOD 动作 Q 值换真实价值下界（AI · r815B 2026-11-27 实拉，2 独立域一手交叉，3 独点；全文见 `references/r815B_CQL离线强化学习.md`）

§r801C SAC 管在线 off-policy + 熵目标、§r808B DPO 管偏好对分类损失、§r812B GRPO 管组内基线去 critic；本章管**只有固定数据集、零环境交互**时怎么避免把没见过的动作估得虚高。
**独点1 病根与保守的目标**：朴素套用 off-policy value-based 方法会因数据集与所学策略的分布偏移，对 OOD 动作给出错误乐观 Q 值，策略再去抓这些虚高值自举放大；原论文摘要逐字「overestimation of values induced by the distributional shift between the dataset and the learned policy」。CQL 与 BCQ 路线不同——BCQ 约束动作候选集，CQL 直接改 Q 学习目标：让策略在该 Q 下的**期望**价值下界真实价值；只要**期望**下界而非逐点下界，就避免过度低估数据内好动作。论文报告复杂多模态数据上 final return 提升 2–5 倍。
**独点2 正则项与两个实例化**：式1 `min_Q α E_{s~D,a~μ}[Q(s,a)] + ½ E_D[(Q−B̂^πQ^k)²]`——在任意动作分布 μ 下压低 Q；式2  tighter 版 `α(E_μ[Q] − E_{π̂β}[Q]) + ½TD`——同时抬高数据集动作 Q，拉大 in-distribution 与 OOD 的 gap。离散 CQL(H) 取相对均匀先验的负 KL：`α(E_s[log Σ_a exp Q(s,a)] − E_D[Q]) + TD`；连续 CQL(ρ) 以上一策略为先验 `R(μ)=−D_KL(μ||π_{k-1})` 稳住高维动作空间。α 是核心旋钮：太小保守不足外推膨胀复发，太大退化成行为克隆。
**独点3 落地口径与边界**：在 SAC / QR-DQN 上「less than 20 lines of code」即可接入、无需显式估行为策略；α 可用拉格朗日对偶自动调。报「用了 CQL」须写 α（或自动调节方式）/正则形式/先验/OOD 采样分布四件。边界：离线训练必配离线评估（§r733C OPE 前提 + 仿真器全流程验证），没有评估的离线训练等于闭眼开药；与 DPO/SAC/GRPO 正交不复用；α 过大会连「数据里真出现过但少见」的好动作一起压掉，回报保守不等于策略更优。
**来源与判非**：`https://arxiv.org/abs/2006.04779`（WebFetch 200 摘要 + 版本史：Submitted 2020-06-08 v1 / revised 2020-08-19 v3，Kumar/Zhou/Tucker/Levine）· `https://arxiv.org/pdf/2006.04779v2`（WebFetch 200 全文逐字：distributional shift / OOD / lower-bound / Q regularizer）· `https://www.alphaxiv.org/abs/2006.04779`（WebFetch 200 全文逐字：式1/式2/CQL(H) logsumexp/CQL(ρ) 先验/gap-expanding/α 对偶）· NeurIPS 2020 proceedings 摘要 + apxml/aiknowledge/jovana WebSearch 交叉。判重：全库 SKILL.md+module-memory 对 `离线强化学习`/`offline RL`/`CQL`/`保守Q学习` 0 专节（§r733C 是 OPE 评估前提、异命题；`r768A` GRPO 一句旁及），豆包自留地 WB 0 落地。

## 三十六、MBPO 模型基策略优化：短分支 rollout 把模型视界与任务视界拆开（AI · r817B 2026-11-28 实拉，2 独立域一手交叉，3 独点；全文见 `references/r817B_MBPO模型基策略优化.md`）

§r801C SAC 管在线 off-policy 熵目标、§r815B CQL 管离线零交互防 OOD 高估；本章管**有模型可学但模型会错时怎么用到收益最大且不崩**——Dyna 骨架（学世界模型→想象转移→加速策略），MBPO=bootstrap 概率集成+从真实 replay 状态出发的短 rollout+SAC 策略学习器。
**独点1 单调改进界与两类误差**：目标 `η[π]≥η̂[π]−C`，Theorem 4.1 用每步 TV 距离 ε_m 与策略散度 ε_π 给 C（含 `1/(1−γ)` 二次放大）；两类误差=采样**泛化误差**（验证损失估）与策略更新后的**分布偏移**（KL 经 Pinsker 转 ε_π）；理论上悲观到「可能无策略超 C」+ 长 rollout 误差复合，故结论是模型不准时少用模型；§4.3 用线性近似 `ε̂_{m'}=ε_m+ε_π·斜率` 得 Theorem 4.3 的 `k*>0`——**最优模型视界是正的短值，非 0 也非任务长度**。
**独点2 机制解耦视界**：branched rollout 从上一策略状态分布 `d_{π_D}` 出发按当前策略在模型中跑 k 步（Dyna 是 k=1 特例）；「we disentangle the task horizon and model horizon by querying the model only for short rollouts」，大量短 rollout 替换少量长 rollout，才能扩到长视界任务；概率集成 `{p_θ^i}` 输出对角高斯，单体捕获偶然不确定性、bootstrap 捕获认知不确定性，同条 rollout 各步可采不同模型；每环境样本 20–40 次策略梯度，但「无模型的高 G SAC」对照追不上⇒收益确来自模型；Ant 30 万步≈SAC 300 万步，模型回报倾向低估真实回报，短 rollout 下策略「may not exploit the model at all」。
**独点3 反例与边界（不写普适）**：原文 §6.2 固定 k=1 保留大部分收益、200 步够准但优化更差、500 步 too inaccurate；2025 取证（arXiv:2510.01457v4）给出两耦合失效——①多分量目标**输出未归一化**使 DMC 0–1 奖励塌到近 0、合成转移主导 critic 致低估 −10^8；②残差预测 `s′−s` 在不稳定区放大方差、「one-step error 低但反事实不可靠」；FTFL 两处修复（next state 与 reward **分别**归一化 + 绝对下一状态预测）缺一不可，7 个失败 DMC 中 5 个超 SAC、Gym 六个不掉，hopper 不连续接触力仍失败；M2AC/MACURA 不确定性过滤/拒绝**单独都救不回**，换 backbone 才恢复。判重全库 0 机制专节（§r801C 一句 TD3 比较、§23 安全探索 learned model 异命题），豆包自留地 WB 0 落地。
**来源**：arXiv:1906.08253 MBPO 原文 HTML 全文（WebFetch 200：Abstract/§4.1–4.3 三定理/§5 Algorithm 2/§6.2/§7）+ arXiv:2510.01457v4 取证分析全文（WebFetch 200：§4.2/§4.3/§5 FTFL/M2AC/MACURA）；arXiv:2007.01995/2110.02758/2412.14312 WebSearch 交叉按来源族折叠。不防：跨基准搬运/目标尺度错配/残差病理/不确定性门控，不替代离线评估与安全护栏。

## 三十七、Decision Transformer：把 RL 丢掉 value/Bellman 改成条件序列建模（AI · r820B 2026-11-28 实拉，2 独立域一手交叉，3 独点；全文见 `references/r820B_DecisionTransformer.md`）

§r815B CQL 管离线 value-based 加保守防 OOD 高估、§r817B MBPO 管有模型短 rollout；本章管**完全不拟合价值函数、不算策略梯度**的另一条离线 RL 路线——GPT 式因果 Transformer 对轨迹自回归建模，以期望回报为条件生成动作。
**独点1 token 格式与生成目标**：abstract 逐字「casts the problem of RL as conditional sequence modeling」「Unlike prior approaches to RL that fit value functions or compute policy gradients, Decision Transformer simply outputs the optimal actions by leveraging a causally masked Transformer」。轨迹（式2）=`(R̂₁,s₁,a₁,...,R̂_T,s_T,a_T)`，每步三模态 token=(return-to-go, state, action)；`R̂_t=Σ_{t'≥t}r_{t'}` 是**未来累计回报非过去 reward**；只喂最近 K 步共 3K token；各模态线性 embedding + **per-timestep**（非 per-token）位置编码；因果掩码只看当前及之前；监督仅在 state token 输出预测动作（离散 CE/连续 MSE），不预测 state 或 RTG（原文「did not find ... improve performance」）；self-attention 直接做 credit assignment 而非 Bellman backup，绕开 bootstrapping 与 deadly triad、不需折扣未来奖励。推理：期望 RTG+起始状态作 prompt，每步拿 reward 后递减目标 RTG（`R←[R,R[-1]−r]`），实测各任务目标与实际回报高度相关、Seaquest 出现超过数据最高回报的外推。
**独点2 为何不需保守/正则 + 竞争力边界**：作者猜想 TD 类「optimizing a learned function can exacerbate and exploit any inaccuracies in the value function approximation」，DT 不做该显式优化故「avoids the need for regularization or conservatism」——与 §r815B CQL（仍 TD+value pessimism）是不同路线。D4RL 多数任务最高（去 Reacher 平均 74.7 vs CQL 63.9、全设置 69.2 vs 54.2）但 Medium HalfCheetah 42.6<BRAC 46.3、Medium-Replay HalfCheetah 36.6<CQL 46.2；Atari 用 DQN-replay 1%，4 游戏 3 个与 CQL 有竞争力但 Qbert 15.4≪CQL 104.2——**不写全面胜出**。%BC 对照：数据充足连续控制中 %BC 常匹敌 DT，DT 优势主要在**数据较少的 Atari**，不能写成「低质量数据必胜」。消融：K=1 大幅变差（Pong 106.1→2.5）说明上下文有用；Key-to-Door 长时 DT 94.6% vs CQL 13.3% 但 %BC 95.1%⇒支持事后回报标签但不足以独证 Transformer 优势；延迟奖励（奖励全移终点）DT 保持而 CQL 崩（TD 需密集 reward、DT 对其密度假设最少）。
**独点3 独立域反证与边界**：NeurIPS'22《You can't count on luck》逐字「conditioning a probabilistic model on a desired return ... can fail dramatically in stochastic environments since trajectories that result in a return may have only achieved that return due to luck」——高回报可能只是运气，ESPER 改条件于聚类平均回报才对齐；Duke D2T2 指根因是「growing variance of returns-to-go ... accumulated over the horizon」，TD 估期望回报替换 RTG 更好且消除手搓 RTG；alphaXiv 2410.24108 指在线微调时 RTG 远偏离期望会阻碍微调、TD3 价值/优势可解。落地报「用了 DT」写 RTG conditioning 值/上下文 K/层数与 head/动作损失四件，离线训练仍配 §r733C OPE；不防：随机环境 luck 条件失配/stitching 弱/手指定目标 RTG/训练数据偏差/恶意 reward 诱发意外行为；适合长时稀疏延迟奖励与离线复用，不适合要求可复现因果策略或强 stitching。
**来源**：arXiv:2106.01345 abs + HTML v2 全文（WebFetch 200：Abstract/式2/§4 架构/§5 RTG 递减/§6 Atari·D4RL 表/§7 %BC·K=1·Key-to-Door·延迟奖励·讨论）· NeurIPS'22 You can't count on luck（ACM DL abstract）+ Duke D2T2 PDF + alphaXiv 2410.24108 + JOVANA 中文词条 + GitHub 精读（WebSearch 交叉，独立第二域按来源族折叠）。判重全库 0 机制专节（Transformer 子串/「决策」噪声异命题），豆包自留地 WB 0 落地。

## 三十八、RND 随机网络蒸馏：把好奇心写成固定随机网络的预测误差（AI · r823B 2026-11-28 实拉，2 独立域一手 + 1 域交叉，3 独点；全文见 `references/r823B_RND好奇心探索.md`）

§r717A 探索利用门管选臂、§r788A PBRS 管不改最优策略的奖励塑形、§r796L PER 管采样权重；本章管**状态新颖性的内在奖励**。
**独点1** 两个网络：固定随机初始化 target `f:O→R^k` + predictor `f̂` 最小化 `||f̂(x;θ)−f(x)||²`；`i_t=||f̂(s_{t+1})−f(s_{t+1})||²`。误差三因只有「训练样本少=epistemic uncertainty」可作探索信号（原文「Factor 1 is what allows one to use prediction error as an exploration bonus」）；目标固定为确定性函数且在 predictor 模型类内，从根上避开 noisy-TV；访问越多误差越低故不 stale。Montezuma's Revenge 无演示无底层状态首次超人类平均、偶尔通关。
**独点2** 内外奖励组合：`R=R_E+R_I`、`V=V_E+V_I` 双 value 头分开拟合、`A_i=A_I,i+A_E,i`；分开因 extrinsic stationary 而 intrinsic non-stationary 且多一路监督信号，双头允许不同 γ（交叉源 γ_E=0.999/γ_I=0.99）。内在用 non-episodic（不在 game over 截断，跨 episode 的新状态都算），外在必须 episodic（否则「开局拿奖励→故意 game over→无限循环」可利用）。
**独点3** 两层归一化是必需件：内在奖励除以 running std of intrinsic returns 以稳定跨环境尺度；观测白化 `x→CLIP((x−μ)/σ,[−5,5])`——target 参数冻结无法适应尺度，缺归一化会 embedding 方差极低丢信息；predictor/target 同用、policy 不用，先随机 agent 走少量步初始化。报「用了 RND」写目标固定/误差公式/双头+non-episodic/两层归一化四件。
**来源与判非**：arXiv:1810.12894 abs + ar5iv 全文（均 WebFetch 200 全文逐字）+ alphaXiv/Walking Labs/kg.rounds-tech WebSearch 交叉（OpenAI blog 404、Lilian Weng 与 arxiv/html 本地回退禁用如实登记）。与 §r792B 课程学习分工；不防 aleatoric 随机 / reward hacking / 目标网络容量不足；豆包自留地 WB 0 落地，按「增＝加厚现有」0 新建。
