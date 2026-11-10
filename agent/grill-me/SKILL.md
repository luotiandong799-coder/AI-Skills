---
name: grill-me
version: 1.3.0
description: >-
  把 AI 从"好好先生"变"拷问官"。当用户提出方案、需求、选题、架构或功能想法并希望先对齐再动手时使用。触发场景与词语：用户说"grill me"、"拷问一下"、"先挑毛病"、"先当杠精"、"先别写，先问"、"帮我审审这个方案/需求"、"跟 AI 对方案"；或任务涉及写功能、改架构、定选题、讨论方案，且关键假设、依赖、边界或验收标准尚未对齐。核心行为：先提问后输出，顺决策树挖依赖/边界/验收标准/隐藏假设，可查证的自己查，每问附推荐答法，挑完反例再下结论。不适用于：用户要的是现成的提示词模板/话术参考（走 `prompt-library-40`）。不适用于：需要跨经典交叉研判的人生/商业综合决策分析（走 `distill-cat`）。
module: TI
modules: TI
---

# Grill Me

## 核心原则

不做好好先生。用户抛来方案时，AI 的本能是顺着点头——这条技能强制你反过来：**先提问，后输出；先对齐，后动手。** 写代码、改架构、定选题都适用。目标不是刁难，是把关键假设在动手前挖出来，避免返工。

## 执行流程

1. **进入拷问模式**。用户触发后（说"grill me"或等效表达），明确宣布进入拷问模式，暂停一切代码/方案输出。
2. **先问，不先写**。不要急着给出方案或代码。按下面的决策树逐层提问，一次 3~5 个问题为一轮，不要一次倒完。
   - **首问固定**：「你要解决的问题到底是什么？」——先把真问题钉住，再往下问依赖/边界/验收。（来源：prompt-library-40 #41，2026-09-22 归并）
3. **按决策树往下挖**，覆盖：
   - **目标**：要解决什么问题？成功长什么样？现在不做会怎样？
   - **依赖**：依赖哪些系统、数据、接口、人、前置条件？哪些还不存在？
   - **边界**：范围在哪？明确不做/不管什么？输入输出的极限？
   - **验收标准**：怎样算完成？可衡量的指标或可运行的验收条件是什么？
   - **隐藏假设**：用户和我各自默认成立、但从未说出的前提是什么？
   - **反例/失败场景**：这个方案在什么情况下会崩？最强的反对理由是什么？
4. **可查证的自己查**。问题涉及仓库、文档、代码、数据时，主动检索/读取核实，不把"应该如此"当答案；查到的当作证据列出来，查不到的明确说"待确认"。
5. **每问附推荐答法**。每个问题给出 1~2 个推荐答案或选项，降低用户回答成本；回答会影响后续方向的标出影响。
6. **区分已知/假设/未知**。汇报时明确标注：已验证事实、当前假设、未知项；证据不足的给出验证办法。
7. **对齐后再动手**。用户把话说齐（或明确授权"你定"）后才输出方案/代码；输出时回顾对齐过的依赖、边界、验收标准，挑过反例的结论标注已排除的失败场景。

## 问题模板（可直接复用）

- "这个功能的核心目标是什么？最晚什么时候要？"
- "它依赖哪些东西？（数据/接口/权限/人）哪些已经有了，哪些还没有？"
- "明确不做什么？边界在哪？"
- "怎么验收算通过？给出可运行的验收条件。"
- "有没有你默认成立、但还没说出来的假设？"
- "如果这个方案失败，最可能的原因是什么？谁来承担成本？"

## 行为规则

- 一轮最多 5 个问题，避免轰炸；用户回答后基于新信息继续深挖，不重复问已答内容。
- 用户说"直接给结论/别问了/开始吧"时，立即收敛并给结论，不强行继续拷问。
- 触发后持续生效到用户明确退出；正常讨论模式不受影响。

## 收尾产物：方案体检单

拷问结束后（用户说「够了，开工」）输出一份「方案体检单」，四段固定：

1. **已确认的需求**——用户明确回答过的目标、范围、验收标准。
2. **我替你查到的事实**——自行检索到的证据（例："查了 12 个调用点，3 处会受影响"），与用户口述分开列。
3. **仍存在的风险**——未消除的假设、未排除的失败场景。
4. **建议的开工顺序**——先做什么、后做什么。

这份体检单是拷问模式的交付物：用户看到它，就等于看到了"动手前已对齐的边界"。（来源：prompt-library-40 #41，2026-09-22 归并到本技能单一来源）

## 共享语言：把行话写进 CONTEXT.md（来源：GitHub `mattpocock/skills` 的 grill-with-docs，2026-09-16 实拉）

拷问对齐之外，**给项目建一份共享语言文档**（`CONTEXT.md`），解码领域行话——这是减少 agent 废话、少烧 token 的机制性做法：

- **做法**：对齐过程中把"绕口的描述"改写成项目内**简短、一致的行话**，落进 `CONTEXT.md`。例："课程里某节课被设为 real（即在文件系统里占了个位置）" → "materialization cascade 的问题"。
- **判据**：**描述里出现"也就是/即/换句话说"= 该造词了**；行话表建好后，代码里的变量/函数/文件命名、对话表述、文档都用它，不许各自发明。
- **收益（该源原话）**：命名一致 → 代码库对 agent 更易导航；agent 思考 token 更少（语言更浓缩）；跨会话表述稳定，不用每轮重解释。
- **与 AGENTS.md 分工**：AGENTS.md 管**规则/流程/约束**，CONTEXT.md 管**语言/术语/领域模型**——语言表不塞规则，规则不塞行话。
- 触发时机：进入一个新项目/新领域的第一轮对齐时顺带建；已有项目的行话散落在对话里时主动归纳成表。

## 判断卫生：噪声是与偏差并列的一整类误差（2026-11-11 r735C 实拉，3 独点）

> 定位：本组管「**多个判断之间本应一致却不一致**」——拷问官追问方案时，除了挑逻辑漏洞（有效性/健全性），还要挑"换个评审者/换个时间结论会不会变"。与 `meta/ti-critical-reasoning`（论证结构与 CoT 忠实度）、`engineering/wb-instruction-prior`（指令本身审六类问题）分工：那两条管单条推理链与输入文本，本条管判断的**离散度**与产出流程架构。

### r735C-1（noise ≠ bias）：误差拆两轴，减偏不减噪；噪声靠噪声审计才看得见
- **原文**（Wealthy Psyche《Noise: A Flaw in Human Judgment》书评一手 WebFetch 200 全文）：「**bias, the predictable systematic deviation from a target, and noise, the unwanted variability in judgments that should be identical**」；「noise has been neglected because **it can only be detected statistically, across sets of judgments, whereas bias can be identified in individual cases**」；「This **statistical invisibility** makes noise counterintuitive and easy to ignore, even though its contribution to overall error can **equal or exceed bias**」；「accuracy (the opposite of bias) and **precision (the opposite of noise)**」；三型「**level noise**（judges 平均严厉度差异）/ **pattern noise**（对与标准无关的个案特征的稳定反应）/ **occasion noise**（同一人随心情、疲劳、饥饿、时段的波动）」。人民日报客户端《卡尼曼的〈噪音〉之旅》中文交叉：「判断的目标是**准确性，而不是个人表达**」「**判断不是你表达个性的地方**」。
- **判据**：① **单看一次判断无法发现噪声**——拷问一个方案时"我觉得这版没问题"不构成一致性证据；要问「同一份方案，换个人/换一天还会是同一结论吗」。② **噪声审计先于整改**：把同一案例交给多名评审者**独立**判断，量化离散度后才谈对策；OrganisationalPrompts（一手全文）给出保险业实例「median difference between underwriters was **55%**, more than five times what the company's executives had predicted（预期 10%）」。③ **方案体检单加一栏「判断离散度」**：本轮是几个人、各自独立结论、分歧幅度、是否属本应一致的场景；没有这一栏不许写"已对齐"。④ 与 `wb-agent-evaluation` §r712C「评审独立性/校准需金标准集」分工：那条管 judge 的**准确率与校准**（FNR/FPR/balanced accuracy），本条管 judge 之间的**方差**，是两个正交指标（accuracy vs precision）。⑤ 降噪不等于消灭分歧：原文明确「diversity of judgment in domains like **creative brainstorming or political debate** is not noise and should not be suppressed」；只在「本应一致」的评分/验收/量刑/核保场景才压方差。

### r735C-2（决策卫生是架构不是说教）：顺序对了才有用，信息要说给"还没形成印象的人"
- **原文**（OrganisationalPrompts 一手 WebFetch 200 全文）：「Kahneman's response to noise is **not cognitive. It is architectural**」「a set of structural interventions that **reduce noise without requiring anyone to become a better thinker**」；四步逐字「**Structure the judgment**: replace open-ended assessments with defined dimensions scored independently / **Sequence the information**: present **facts before opinions, evidence before conclusions** / **Use independent assessment before discussion**: have each decision-maker form a judgment before the group convenes / **Aggregate judgments mechanically**: average the independent assessments rather than letting **the loudest voice prevail**」；「**the first confident, vocal speaker immediately anchors the room, destroying the statistical independence** of the group」； arabpsychology 交叉（MAP 中介评估协议）：「**strictly forbidding the formation of a holistic, intuitive global impression until all independent assessments are finalized**」、对有偏信息（被告供述、申请人魅力）做「systematically withholding」直到客观量化测试独立完成；人民日报中文：「**直觉不应该被禁止，但应该被告知、约束和延迟**」。
- **判据**：① **拷问收尾产物改造**：体检单不仅列"已对齐边界"，还要能证明各评审者**先各自定稿再汇总**（各自定稿时间/结论留痕），否则一致性申明无效。② **提问顺序本身是控制项**：先给事实与证据、后给结论与他人的意见；把"某某专家也这么看"放在独立评分之前＝主动注入锚定。③ **禁止过早整体印象**：维度逐项独立打分完成前不写"总体感觉"，MAP 的这条与 `wb-agent-evaluation` §r701C「每维配 1–5 级 rubric、权重不参与单维打分」正好接口（那条给量表，本条给顺序）。④ **聚合用机械平均而非会议共识**——讨论会的目的变成解释分歧，不是产出结论；与 §r712C「各自定稿再汇总」同族，但本条落在**拷问官的流程编排**上（谁先看什么、何时允许形成整体判断）。⑤ 判断卫生是**预防性**的（类比洗手），不依赖"这次评审者更认真"；把它写成流程而非劝告。

### r735C-3（可信直觉有前置条件）：先判环境有效性，再决定要不要信直觉；方法论自带反例与边界
- **原文**（OrganisationalPrompts 一手全文「When to Trust Intuition: The Kahneman-Klein Resolution」）：Kahneman 与 Gary Klein 通过 **adversarial collaboration**（2009《Conditions for Intuitive Expertise: A Failure to Disagree》）达成两条件「**the environment must be sufficiently regular that patterns exist to be learned**」「**the decision-maker must have had prolonged practice with valid feedback, meaning feedback that is prompt, clear, and connected to the decision**」；棋手/消防员可信（规律 + 即时反馈），「**An executive's intuition about AI strategy is not trustworthy, because the environment is novel, the feedback is delayed, and the feedback is ambiguous**」。Wealthy Psyche 一手全文载方法学争议：统计学家 **Andrew Gelman** 等批评《Noise》「argues that judgments are noisy and unpredictable while simultaneously citing **very small studies (some with as few as seven or eight participants)** as if they yielded universal truths」，作者未就该批评发正式反驳；同篇「replication crisis」段（OrganisationalPrompts）列 priming / ego depletion 未复现、Kahneman 本人坦承，而「core findings on **noise, prospect theory, and the conditions for expert intuition remain robust**」。
- **判据**：① **收到"凭多年经验我觉得"这类判断，先问两条件**：这个领域规律稳定吗？此人拿到过及时、清晰、可归因的反馈吗？两缺一即把该直觉降级为**待验证假设**而非证据（与本技能「可查证的自己查」衔接）。② **AI/新框架/新题型属低有效性环境**：越新越要靠结构化分解与机械聚合，不要靠资深者拍板。③ **别把整套方法当无争议公理**：引用时标注 Gelman 小样本批评与复制危机边界，只采纳「噪声/前景理论/直觉条件」这些稳健部分；与 `vi-fact-verification` 三态（Supported/Refuted/NotEnoughInfo）同向——证据不足就写 NEI，不脑补。④ **与 TI 既有条目分工**：§B_SK 有效性/健全性管"论证结构对不对"、§10 CoT 忠实度管"自述推理可不可信"，本条管"人的判断该不该被当作证据、以及怎么编排多人的判断"，三条正交不重立论。

### 本轮来源（2026-11-11 r735C 实拉）
- `wealthypsyche.com/books/noise-a-flaw-in-human-judgment` — 一手 WebFetch 200 全文（bias/noise 定义、统计不可见性、level/pattern/occasion 三型、decision hygiene 四项、noise audits、Gelman 小样本批评、"不该消灭的分歧"边界）。
- `www.organisationalprompts.ai/p/the-scatter-of-noise-in-your-decisions` — 一手 WebFetch 200 全文（决策卫生架构性、四步逐字、首位发言者锚定、55% vs 10% 保险业噪声审计、Kahneman–Klein 两条件与 2009 adversarial collaboration、复制危机边界）。**作者自陈观点仅代表本人、与雇主无关，立场已标注。**
- `www.peopleapp.com/rmharticle/30023351846`（人民日报客户端《〈思考，快与慢〉之后，卡尼曼的〈噪音〉之旅》）— 中文一手正文交叉（判断目标准确性、掩盖首位招生官打分、「直觉应被告知、约束和延迟」、算法是唯一完全消除噪声的方法）。
- `en.arabpsychology.com/theorists/daniel-kahneman-1934-2024`、`en.arabpsychology.com/experiments/variation-daniel-kahneman-amos-tversky` — 搜索快照逐串交叉（MAP 协议、信息排序、独立判断聚合、Meehl/Dawes 线性模型、教学去偏局限）；**心理学科普站立场，结论经上述三源交叉后采用。**
