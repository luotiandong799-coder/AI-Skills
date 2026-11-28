# r824B · Premortem 事前验尸：把复盘推到事故之前（RI · 2026-11-28 实拉，≥3 独立域一手交叉）

> 全文支撑 `meta/ri-retrospective/SKILL.md` §r824B 摘要节。本文件为完整取证与判重留痕。

## 主题定位

本技能 §7.1/r738C 管「事后要不要复盘的触发条件」、§十四 r751C 管「关闭≠修复」、§十五 r755C 管「复盘会第二道门」、r767C AAR 管「每次行动后的薄门」——全部是**事后**。premortem 是同一「无责说出担忧」纪律在**事前**的用法：项目尚未启动就假设它已经失败，让异议者合法发声。与 §十三 r746C 标签、r814B HAZOP（引导词枚举操作偏差）互补，不复用结论。

## 三独点

### 独点 1 · 核心机制是 prospective hindsight：把失败从「可能」改成「已经发生」，释放不敢说的担忧

HBR 原文（Gary Klein, 2007-09）逐字：「Projects fail at a spectacular rate. One reason is that too many people are reluctant to speak up about their reservations during the all-important planning phase. By making it safe for dissenters who are knowledgeable about the undertaking and worried about its weaknesses to speak up, you can improve a project's chances of success.」「Research conducted in 1989 by Deborah J. Mitchell, of the Wharton School; Jay Russo, of Cornell; and Nancy Pennington, of the University of Colorado, found that prospective hindsight—imagining that an event has already occurred—increases the ability to correctly identify reasons for future outcomes by 30%.」

HBR 逐字：「Unlike a typical critiquing session, in which project team members are asked what might go wrong, the premortem operates on the assumption that the 'patient' has died, and so asks what did go wrong. The team members' task is to generate plausible reasons for the project's failure.」

牛企（2026-10-13）逐字：「加里·克莱因2007年在《哈佛商业评论》上提出过一个叫'事前验尸'（premortem）的方法：在项目启动前，先宣布它已经死了，然后让所有人写死因。卡尼曼在书里专门推荐了这个做法，理由是它能合法地释放团队里那些平时不敢说的担忧。」

**判据**：premortem 不是「列风险清单」——关键在于把疑问句（可能出什么问题）换成完成时陈述句（已经失败了，死因是什么）。让唱衰从「反对老板」变成「完成演练任务」，才释放沉默者的信息。

### 独点 2 · 标准流程是「独立写 → 轮流念 → 合并 → 溯源到方案」；AI 只能列通用风险，本地风险须人补

HBR 逐字流程：「A typical premortem begins after the team has been briefed on the plan. The leader starts the exercise by informing everyone that the project has failed spectacularly. Over the next few minutes those in the room independently write down every reason they can think of for the failure—especially the kinds of things they ordinarily wouldn't mention as potential problems, for fear of being impolitic.」「Next the leader asks each team member, starting with the project manager, to read one reason from his or her list; everyone states a different reason until all have been recorded. After the session is over, the project manager reviews the list, looking for ways to strengthen the plan.」HBR 实战例：某军方算法项目里一直沉默的成员提出「算法装不进野战笔记本、要跑几小时」，原来开发者已有捷径却一直没说—— substitution 后项目成功。

fourweekmba 逐字四步：①「Fix the outcome — State the failure as a fact, not a possibility: 'The launch failed.'」②「Explain backwards」③「Make dissent safe — Because everyone is asked to imagine failure, raising doubts becomes the task rather than disloyalty」④「Feed the plan — Turn the top reasons into owners, checks and early warning signs before work starts」。同页对比表逐字：premortem 问「It failed. Why?」用于 before committing；postmortem 问「It failed. What did we learn?」用于 after；scenario planning 问「What futures are plausible?」；risk register 问「What could go wrong, and how likely?」；red team 问「How would an opponent beat this?」。同页 AI 边界逐字：「a language model can draft a list of generic failure reasons quickly, but the team still needs to add the specific risks only insiders know.」

牛企四步（本地实操版）逐字：①写失败公告（设定具体日期、用过去时写具体损失）②「逼出至少10条死因。注意，是10条，不是3条。数量逼着你往深处想。前3条一般是'市场不行''竞争太激烈'这种废话，第6条之后才会出现真东西」③分两类（能提前防的改方案 / 防不住的备预案）④「倒着标触发点。每条死因往前推，什么信号出现就说明它正在发生？把它变成一个月度检查清单」。

**判据**：产出不是一份死因清单，而是「每条死因 → 可监控指标 → 责任人 → 触发后动作」的映射（牛企逐字「提前写好动作，等于替未来的自己做了决定」——与 §十四 r751C「关闭≠修复」同源：写了不等于验了，这里强调「触发后动作要事前定，免得临场找理由继续投」）。

### 独点 3 · 三种情况下 premortem 反而有害，且它不替代 postmortem

牛企逐字三不适用：①「进入完全陌生的领域。你连这个行业怎么赚钱都没搞明白，倒推出来的死因多半是凭空想象，还不如老老实实做市场调研、找行内人聊」②「团队已经过度悲观。如果一屋子人本来就信心不足，再来一场失败预演，项目可能直接被吓死」③「你已经拍板了，只想找人认同。这种状态下做预演，写出来的死因全是'对手太强''行情不好'，本质还是在给自己找借口」。适用面逐字：「有一定行业经验、决策金额对现金流有实质影响、团队还愿意说实话的场景」。

HBR 逐字边界：「a premortem may be the best way to circumvent any need for a painful postmortem」——是「可能免去事后复盘」而非「替代事后复盘」；prospective hindsight 的 30% 提升是 Mitchell 等 1989 实验结论，HBR 转述，按 rules/08 §五标来源观点不作本项目实测事实。

**判据**：premortem 与 postmortem 是同一纪律的两个时点，不是二选一；对陌生人/过度悲观/已内定三种情境禁用；30% 数字是来源观点须归属 Mitchell 1989，不当本地保证。

## 来源（逐域登记）

- 第一独立域（方法原始一手）：`https://hbr.org/2007/09/performing-a-project-premortem`（Gary Klein, HBR 2007-09，WebFetch 200 摘要段逐字 + WebSearch 原文快照逐字：prospective hindsight 30%、定义、独立写→轮流念→项目经理汇总流程、军方算法与研发项目两例、"circumvent any need for a painful postmortem"）。
- 第二独立域（独立教学站，立场登记）：`https://fourweekmba.com/prospective-hindsight/`（WebSearch 原文快照逐字：Mitchell/Russo/Pennington 1989、Klein 2007、四步、与 postmortem/scenario/risk register/red team 对比表、AI 只列通用风险）。
- 第三独立域（中文实操一手）：`https://www.niuqiclub.com/article/28805.html`（WebFetch 200 全文逐字：卡尼曼推荐理由、四步失败预演、10 条死因门槛、触发点指标表、食品包装厂案例、三不适用、适用面）。
- 诚信登记：HBR WebFetch 仅返回页面开头摘要段，完整正文取 WebSearch 原文快照逐字，不冒充 WebFetch 200 全文；fourweekmba WebFetch 触发 Cloudflare 检查页，取 WebSearch 快照。

## 判重

全库 WB 侧 SKILL.md / module-memory / co-learn 精确扫描 `premortem` / `事前验尸` / `prospective hindsight` / `推进式` / `预先尸检` **全 0 命中**（命中散布在 co-learn 豆包记录与 daily log，非 RI 落地）。`预演`/`心理模拟`/`红队` 命中在 vi-fact-verification / wb-execute-discipline / skills-security-check 等异命题上下文；fourweekmba 对比表已明确 premortem≠red team≠scenario≠risk register，不复用。豆包自留地 WB 0 落地。
