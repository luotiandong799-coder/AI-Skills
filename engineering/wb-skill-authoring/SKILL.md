---
name: wb-skill-authoring
description: >-
  Skill 的写法与体检：触发词设计、description 质量、文件拆分、跨工具迁移、安装前安全审查、安装后接线、触发评测盲测、no-skill 对照、效果归因、重复技能的去重与合并流程。当新增 skill、改写已有 skill 的 description、排查"技能该触发却没触发 / 不该触发却触发"、拆分过长 SKILL.md、把 skill 迁移到不同 AI 工具（Claude Code / Codex / Gemini 等）、安装第三方 skill 前做安全检查、或装了技能却总用不上（没接线）时应用。只写与自身工作流相关的约束和步骤，不写通用方法论套话。触发词：技能没触发、装了没用、接线、skill 不生效、触发评测、盲测、诱饵用例、no-skill 对照、效果归因、技能无增益、技能抢触发、误触发、负向边界、不适用于、审计技能、技能过期、拼写错误、乱码、失效工具名、重复触发、技能快速路径表、双路由、meta-router、description 上限、name 规范、快照基线、触发率、近失、指令改写、改了指令还是不行、改了两遍还是这样、调指令算修了吗、别再加一句必须、拆技能、技能合并、技能去重、查重、技能素材来源、gotchas、控制度校准、给默认不给菜单。、规则该写多少、AGENTS.md 变长、allowed-tools 是限制吗、禁用工具、权限叠加、停用还是删除、参数分发、万能技能、专用子代理、防递归、显式契约、靠推断、角色重叠、通才助手、示例与考题要不相交、自动放行的兜底层、硬禁清单、技能选择准确性评测、不需要却加载、选错 skill、评委团、集成必须留子分、ensemble、多评委同签名、judge_scores、可溯源、provenance、CI 出证、无旁路、禁读环境变量与文件系统、输入走显式参数、审计面等于参数表、一个包一个服务、代理层不受理、可重跑产物、脚本沉淀、不许硬编码结果、连跑两次存证、产物自带说明、persona 市场退场、GPT Store 停用、迁移为插件、优先可机读注册表、版本号不塞 description、双榜分离、社区热度榜、官方自研榜、创建者域名标注、匿名统一标签、纯 UI 信源不学、审计盲区、只记写不记读、传参值不入库、失败也留痕、跨面不同步、surface 能力面、按面降级、导航四信号、签名强度、显式调用跳过路由、@标识调用、语义检索、诚实无匹配
version: "3.119.0"
---

# wb-skill-authoring（技能层：写得能被触发、能被执行）

来源：WaytoAGI 精选 2026-09-01《Agent Skill 100 问》（skill 描述写法、触发排查、脚本/参考文件拆分、跨工具迁移、安全审查）。
核心判断：**skill 的价值 = 能否在该触发时被触发 + 读到的内容是否够执行。** 写得好但没人触发 = 不存在。

**与相邻技能的分工**（防抢触发）
| 场景 | 走谁 |
|---|---|
| 从零新建一个技能 | 平台内置 `skill-creator`（官方结构 / frontmatter / 脚本规范） |
| 改造 / 体检**已有**技能（触发不准、描述过宽、去重合并、安装后接线、触发评测、安全审查） | **本技能** |
| 长内容（书 / 长视频 / 播客 / 课程）蒸馏成技能 | `cangjie-skill`（本技能只管蒸馏产物落地后的写法与验收） |

> 本节（设计原则）已整段下沉至 `references/knowledge-base.md`，需要时按标题检索。
> 本节（写"什么时候不该跑"：STOP / WAIT / PROCEED 快速路径表）已整段下沉至 `references/knowledge-base.md`，需要时按标题检索。
## 技能是"指令 + 所需工具"的打包，不是一段文字
- 本节细则已下沉至 `references/knowledge-base.md §技能是"指令 + 所需工具"的打包，不是一段文字`（原文零删减，2026-09-29 r286-C 下沉）。

> 本节（SKILL.md 的兄弟格式：Agent SOP）已整段下沉至 `references/knowledge-base.md`，需要时按标题检索。
## description 怎么写（决定触发的唯一因素）
- **写"何时用"，不写"是什么"**：description 是路由器，不是简介。开头就给触发场景（"当用户要求 X / 出现 Y 场景时使用"），其次才是能力范围
- **把用户的原话写进去**：用户会说的说法（含中英文、口语、错拼）都列进触发词——模型靠语义匹配，不靠理解你的命名
- **具体 > 宽泛**：`"修 bug"` 会被误触发到所有排错场景；`"涉及编码任务时"` 才收得准。宁可窄，触发太窄时再补
- **边界写进描述**：明确"不适用于什么"（如 ponytail 写"非代码任务不套用"），防误触发比补充触发词更省事
- **负向边界声明成段**（来源：阿里云 Skills / ModelScope 生态的通用写法）：能力封装类技能在描述或正文开头写显式的 `不适用于：…` 段（如支付宝 skill 写"不用于微信支付、银联支付、对账、红包等非收单场景"）——把最容易误触发的一批相邻场景**点名排除**，比只写正向触发词收得准得多
- **一处修改即可生效**：description 是唯一被常驻加载的字段，正文只在触发后才读——所以约束的第一层防线必须在 description 里
> 本节（描述的两条硬规格与一条写法纪律（来源：agentski…）原文已整段下沉至 `references/knowledge-base.md`，需要时按标题检索。
## 追加触发词只准加在末尾；加在开头会挤掉首句（2026-09-20 本仓库实修，来源：WorkBuddy 线 D4 描述层重构）

**实测事故**：本仓库 7 个 `wb-*` 技能长期用「把新一批触发词补到 description 开头」的方式增补。累积若干轮后，两个技能的首句被彻底挤走——`wb-skill-authoring` 的 description 以 `、评估型输出、按能力透视、` 开头（**一个孤立顿号起头**），`wb-ponytail` 以 `、产物存活期、TTL、` 开头，真正的功能句"Skill 的写法与体检（…）""写代码 / 实现功能类任务前的决策阶梯（YAGNI）"被推到**第 200–300 字符之后**。

**为什么这是硬故障，不是排版问题**
- 路由是按 description 做语义匹配，**开头权重最高**。首句被位移 → 路由器读到的是术语碎片，**该技能"是什么"根本读不出来** → 直接压低触发率，而且因为技能还能被别的词误触发，故障**长期不可见**。
- 越补越糟：每轮都对，累积起来错。**这是"局部正确、全局腐烂"的典型。**

**纪律（三条，机检可验）**
1. **追加一律加在末尾**（`触发词：…` 段尾部续写），**永远不插到 description 开头**。
2. **首句必须在**：description 前 **30 字符内**必须出现功能句（"X 是…" / "当用户要…时使用"）。不得以 `、` `,` `。` 等标点起头。
3. **长度硬上限 1024 字符**（见上节官方规格）。同一次事故里 6 个技能的 description 悄悄涨到 **1640–2879 字符**，**越界 1.6–2.8 倍且无人报警** —— 因为没有任何检查在看长度。**写法越"勤快"，越容易静默越界。**

**审计项（补进本技能巡检清单）**
- `首句位置`：功能句起于前 30 字符内 ✅/❌
- `首字符`：不得是标点
- `description 长度 ≤ 1024`
- `触发词段只出现在末尾`；`无重复的 触发词： 标记`（同次事故中 `wb-artifact-verification` 有 **5 个** `触发词：` 段头）
- `全文无 、。 连排 / 。。 断句残留`

**术语 vs 触发词要分开处置**
description 里出现的**内部方法论术语**（"假性不收敛""凭据读穿""L0/L1/L2""抑制兜底""只移植结构不移植假设"）**永远匹配不上用户的口语**，却**按字计费地常驻**。处置判据：
- 用户**真的会说**的 → 留在 description（这是路由的输入）
- 只有**读技能正文的人**才需要的 → **外置到正文附录**（`## 技能正文的长度本身就是训练信号，指令命名"输出"还是"状态"决定模型的服从方式（来源：topaiskills.com「wait-what-skill-faq」（Matt Pocock `wait-what`，skills.sh #266 / 146,544 installs，三行技能）+ 同族 domain-modeling 参考技能失败模式，2026-09-21 实拉，与 §追加触发词只准加在末尾、§description 三条机检纪律 互补——那两条管"描述写多长、往哪加"，本条管"**正文写多长**"与"**一句话指令里的动词指向谁**"）

- **原文事实**：`wait-what` 正文**只有三行**，设计文档原文 "**Three lines is the design. A longer skill teaches the model that verbosity matters.**"——更长的技能会教会模型"啰嗦是重要的"。它的措辞刻意避开"be concise"：原文明说**"be concise" 命名的是模型的输出，模型于是靠裁词来服从，结果更短也更不清楚**；而 **"wait, you lost me" 命名的是听者的状态，模型于是回退一步并补上你缺的那段前提**。文章点名三个反例 `/tldr` / `/no-fluff` / `/talk-normal`，都会过度校正成"更短但同样不清楚"的电报体。另一条：**重述范围说 "that" 而不是 "that last message"** —— 让你没跟上通常不止一段，把回退距离交给模型决定。
- **判据**：
  1. **技能正文按"最小够用"写，多写的每一段都在给模型上课**。判据：**删掉一段后触发与执行不受影响，那一段就是在教坏模型**（与 §渐进披露 分工：那条管按需加载更多文件，本条管**常驻正文的绝对长度**）。
  2. **写指令前先问：这句话命名的是"产物"还是"状态"**。判据：**命名产物 → 模型在该产物维度上过冲（要简洁 → 裁词丢信息）；命名状态/失败 → 模型去修原因（我没跟上 → 补上下文）**；想同时要"更少字"和"更多上下文"，就命名后者。
  3. **重述类指令不要把范围钉死在一句上**。判据：**说"重讲那个"而不是"重讲上一句"，把回退距离交给执行方**——它比你知道是哪一段开始断的。
- 提升层级：可复用 Skill（正文长度与指令措辞）+ 模型（指令如何被服从）。
- 触发词：三行即设计、技能长度是训练信号、verbosity matters、命名输出还是状态、be concise 陷阱、wait you lost me、重述范围、长技能教坏模型。
<!-- 2026-09-29 r290 下沉：topaiskills 2026-09-21 批次 4 节（契约声明/参数化知识非真值/frontmatter 空行/被引用静默没加载）→ references/knowledge-base.md §r125 批 -->
## 常驻规则只做路由表，实体内容下沉到技能；「自动批准」不是「只允许」——同一个字段名在两处语义相反（来源：Devin 官方 `docs.devin.ai/cli/extensibility/rules` + `/cli/extensibility/skills/creating-skills` + `/product-guides/knowledge`，2026-09-22 r132-A 独立重拉首读，新信源首读）

- **官方推荐模式：用 rule 引用具体场景该用哪个 skill，而不是把内容写进 rule**。官方原话：为提高编码能力、加快完成、降低成本，**尽可能用 Skills 代替 Rules，Rules 与 AGENTS 要保持尽可能小**。与 §机制选型表 分工——那条管"按加载时机与付费点，四类机制怎么挑"，本条管"**已经决定内容不常驻之后，规则文件里还剩下什么**"：只剩指向，不留正文。
- 判据：**这段内容是不是每次会话都要用**？不是 → 不该常驻。常驻层只留"遇到 X 就用 Y 技能"这种一行指向；把 Y 的正文抄进来＝用常驻价格买按需内容。
- **`allowed-tools` 是"免弹窗"不是"白名单"**：未列出的工具依然可用，只是走正常审批流程。真要禁掉一个工具，内联技能用 `permissions.deny`，子代理技能用配了 `allowed-tools` 的自定义 profile。
- **同名不同义的坑**：`allowed-tools` 这个字段名，**在 skill 上只是自动批准（不限制），在 subagent profile 上是真限制（未列出的不可用）**。跨工具迁移或抄配置时，这是最容易静默失效的一处——照抄字段名不代表语义跟着走。
- **技能权限是叠加不是替换**：技能不能授予上层（项目/组织）已经 deny 的权限，所以**不能靠写一个技能给自己提权**。判据：想让技能多用一点，先查上层有没有禁用；上层禁用了，改技能无效。
- **停用 ≠ 删除**：临时无关但队友或将来可能还会用的条目，用 disable 保留而不是删。判据：**"以后还有没有可能用"由谁判断**——如果别人也可能用，就 disable 不删。
- 演进佐证：Devin 自己的 Knowledge（带触发描述的检索式知识条目）已标记 deprecated，正在自动迁移到 Skills。**"按需加载的技能"正在吃掉"检索式知识库"这个位置**——新写的长期上下文优先做成技能，别再建一套要靠检索召回的条目库。
## 一个子代理一个独立入口，别用一个入口靠参数分发；防递归要两道（来源：Inngest 官方 `inngest.com/docs-markdown/ai-patterns/sub-agent-delegation`，2026-09-22 r132-B 独立重拉首读，此前未读）

- **官方推荐：给不同的子代理各自一个独立工具，而不是一个工具加"选哪个子代理"的参数**——原话 "LLMs often do better with separate tools for separate sub-agents rather than a single tool with different parameters for selection"。判据：**这个选择是"做哪件不同的事"还是"同一件事的不同参数"**——前者拆成不同入口，后者才留作参数。与本技能 §一个工具只做一件事 分工：那条管"单个工具的动作面要窄"，本条管"**多个同类能力之间的分发方式**"。
- 落到技能系统上就是：**不要写一个"万能技能 + 类型参数"**。写成两个技能、两个触发词，让路由在入口就分完；靠参数在技能内部分支，等于把路由成本从宿主身上搬到技能正文里，还得靠模型读完全文才知道该走哪支。
- **专用化不需要新机制**：通用子代理起步即可， specialization 靠**任务描述 + 可用工具集**两件事就够了（"The task description and available tools are enough to specialize behavior."）。判据：**想加一个专职角色之前，先问是不是改任务描述与工具集就能做到**——能就不新增实体。
- **防递归是两道，缺一不可**：①**工具集层面**——子代理的工具集里不放委派工具（它根本没有派活的能力）；②**硬上限层面**——子代理单独设较低的迭代/重试上限。判据：**只靠一层会不会被绕过**——工具集会改、上限会调，两层同时失效才会失控。
## 要给别人（别的 agent）用的能力，契约必须显式声明，不靠实现推断；消费方不同形状就不同（来源：CrewAI 官方 `docs.crewai.com/v1.15.22/en/guides/tools/publish-custom-tools` + `/en/concepts/collaboration`（Best Practices → Clear Role Definition），2026-09-22 r132-C 独立重拉首读，此前未读）

- **输入契约显式声明，别让框架从签名推断**：官方推荐对"要发布出去"的工具显式给 `args_schema`——理由不是校验，是**显式契约带来更好的 agent 行为与更清晰的文档**；推断出来的只够作者自己用。判据：**这个能力会不会被不是作者的人或 agent 用**——会就把输入形状、默认值、每个字段的含义全写出来；只自己用一次的可以省略。
- **输出同理**：返回结构化数据时显式给输出模型，"用户和 agent 都能靠字段名取用"。判据：**拿结果的一方是照字段名取值，还是在字符串里找数字**——后者说明缺了一层声明。
- **角色 / 技能之间不能笼统重叠**：官方反例同样是 "General Assistant" / "Helper"。判据：**两个角色各自能干什么，去掉交集还剩什么**——交集大于各自独有部分就该合并，而不是靠 description 里多写几个词把它们分开。与 §同类技能合并判据 分工：那条管"怎么合并"，本条管"**什么时候其实早该合了**"。
> 本节（附录 Z：description 术语索引）已整段下沉至 `references/knowledge-base.md`，需要时按标题检索。
## 该触发却没触发：按序排查
0. **这个任务是否本来就不需要技能？**（超出模型自身能力的任务才会去查技能库——单步简单请求没触发不等于描述有问题，见上节末条）
1. 描述里有没有用户实际会说的那几个词？
2. 触发条件是否写得太抽象（"处理复杂任务" 这类）？
3. 文件位置对不对（用户级 `~/.workbuddy/skills/` vs 工作区 `.workbuddy/skills/`）？
4. frontmatter 语法是否合法（`name` / `description` 必填，YAML 缩进别错）？
5. 改完 skill 后会话没重开 → 读的仍是旧版本
## 不该触发却触发
- description 过宽（写成了"所有 AI 相关任务"）
- 多技能触发词打架 → 显式写出优先级，或收窄其中一条
- 名字太泛（`helper` / `utils`）→ 改成能被语义区分的名字
> 本节（双路由防呆）已整段下沉至 `references/knowledge-base.md`，需要时按标题检索。
## 显式 @调用跳过路由：用 @标识 直接点名绕过模糊路由器（来源：腾讯 SkillHub 技能广场分数面 skillhub.cn/skills?sortBy=score，2026-09-27 实拉，17万技能规模头部「编程专家.Skill」声明「支持 @标识 显式调用跳过路由」）
- **模糊路由会误配/漏配**：靠 description 关键词做自动激活，长尾意图容易错配或漏配；允许用户在对话里用 `@技能名` 显式点名，可让该技能**绕过模糊路由器直接激活**，把"猜你要哪个"变成"你点名哪个"。
- **实拉证据**：SkillHub 分数排序面头部技能（编程专家.Skill / dev-expert 等）在描述里明写「支持 @标识 显式调用跳过路由」——这是技能级的可选路由优化，不是宿主强制机制。
- **判据**：当某技能**高频被错配/漏配**、且用户有明确调用意图时，在 description 里声明"支持 @技能名 直接调用"是降低路由 misfire 的低成本手段；它与 §双路由防呆 分工——那条管"别叠两层路由器"，本条管"给确定意图一条绕过模糊路由的直通车"。
- 提升层：可复用 Skill / 工作流（路由可靠性）。
## 技能供应链内容完整性：摘要钉死批准 + 逐文件 size/SHA256 校验（来源：MCP skills 扩展 io.modelcontextprotocol/skills，SEP 2640，2026-09-27 实拉）
- **内容寻址的技能完整性**：MCP skills 扩展规定 Host 激活技能前必须逐文件校验 `size` + `SHA-256 digest`，且**持久化批准绑定到完整文件 URI + digest 集合**——任一文件变更/增删都撤销批准、需重新获取。技能条目带 `resources[].digest/size` manifest，Host 不得提前取文件、批准只绑 manifest；上限 **16 MiB / 512 文件每技能**，资源可标 `dynamic`（生成内容、无稳定 digest）。
- **判据**：把"这个技能可信"从"读一遍文档"升级为"字节级摘要钉死 + 批准绑 digest"——内容被篡改或任何文件变动立即失效重批。与 §安装前安全审查（可溯源/无旁路/单一职责）互补：那条管"进门三判据"，本条管"进门后内容完整性如何不被静默破坏"。
- 提升层：可复用 Skill / 工具（供应链完整性）。
## 声明式依赖清单 + 元数据失配扫描（来源：OpenClaw skill-format / ClawHub 安全分析，2026-09-27 实拉）
- **声明式运行依赖**：frontmatter 用 `requires.env`（必填环境变量）/ `requires.bins`（必装 CLI）/ `requires.anyBins`（至少一个）/ `requires.config`（配置文件）+ `install`（brew/node/go/uv 声明式安装）——把"技能跑起来需要什么"写成机器可读清单。
- **元数据失配扫描**：ClawHub 安全分析**交叉比对"代码实际引用的密钥/二进制"与"frontmatter 声明"**——代码用了某 key 但 frontmatter 没声明 → 判元数据失配并标记。声明即契约，未声明即 flagged。
- **判据**：第三方技能进门审查从"人读代码找依赖"变成"声明清单 + 自动失配扫描"；与 §无旁路（禁读环境变量与文件系统）分工——那条管"运行时不越权读"，本条管"安装前声明与代码是否一致、自动发现瞒报"。
- 提升层：可复用 Skill / 工具（安装审查自动化）。
## 技能设计「流程优于文档」：带证据检查点的工作流，而非会被略读的散文（来源：Addy Osmani agent-skills 框架 / theagenttimes 2026-09-27 实拉，26K★，六阶段 SDLC 技能 Define/Plan/Build/Verify/Review/Ship）
- **把技能写成工作流而非参考文档**：Osmani 的判据——"把 2000 字测试最佳实践散文塞进上下文，agent 读完生成像模像样的文字然后跳过真测试；把工作流（先写失败测试→跑→看失败→写最小代码过→看通过→重构）放进去，agent 才有事可做、你才有可验证物"。技能本质是**带检查点、产出证据、有明确定义退出标准的工作流**，不是漂亮 markdown。
- **判据**：写技能时每个阶段要有"做完了能拿什么证据证明"的出口，而非"读完了就懂了"的散文；与 §Gotchas（失败经验沉淀位置）、§持久声明纪律（声明绑会失效的机制）互补——那些管"坑写哪、声明怎么不腐烂"，本条管"正文该是工作流还是参考文档"。
- 提升层：可复用 Skill（写法）。
## 发布即冻结运行环境 + 升级静默丢失禁令（来源 Qoder r263-A 审计落地，Dify 1.17 Home Snapshot / LangFlow PR14926·PR14913，2026-09-26 实拉）
- **发布即冻结运行环境**：技能"发布"除冻结文本版本外，须声明其运行环境前置（依赖/文件状态清单）；运行异常先比对环境清单而非重读正文——"升级后为什么坏了"常是环境飘移不是正文错。提升层：可复用 Skill。
- **升级静默丢失禁令**：契约变更（改名、字段可见性、依赖边）迁移时——①判定逻辑收敛为单一共享函数供多路径复用（两路径各写一份必漂移）；②任何被丢弃的连接/字段必须登记为 brokenEdges 类告警显式报出，禁止"更新成功但拓扑悄悄变了"。提升层：可复用 Skill。
## 触发评测：发布前盲测（新技能 / 改过 description 必做，细则已下沉 KB）
- 完整盲测流程、对照表与判据见 [references/knowledge-base.md](references/knowledge-base.md) §触发评测：发布前盲测。
## 按需阅读（渐进披露，不要常驻加载）

本正文只保留写法与评测决策级核心。方法论来源、判据推导、反模式、特殊场景全部在
[references/knowledge-base.md](references/knowledge-base.md)（完整知识库，下沉于 2026-09-26）。
**先 Grep 定位关键词，再读对应节**。主题速查：内容从哪来（真实专长）· 调指令是缓解不是修复 · 控制度按脆弱性 · 四个高价值实操模式 · RubricForge 评分标准 · 上线后度量 · 双集 train/validation · 引擎与规格解耦 · 改版钉到最低分项。
## 声明式白名单只约束"工具调用面"，不约束"数据面"：判据按"被约束的是哪类调用"而非"有没有该字段"（来源：learn.microsoft.com/en-us/agent-framework/agents/skills、docs.github.com/.../add-skills、geminicli.com/docs/cli/skills、code.visualstudio.com/.../agent-skills、cursor.com/docs/context/rules，2026-10-01 r362-Q-C 实拉；与 r361-Q-B B1 跨客户端效力漂移 相邻）
- 判据：① 技能工具的白名单/审批只约束 `load_skill`/`run script` 这类**工具入口**（可自动批准），而文件读取、包安装等旁路属**另一面**（数据面/运行期副作用面）。② MS Agent Framework 原文 "support may vary between implementations"；Copilot 的例外标志是"排除者强制手动同意"（准入例外≠能力授予）；Gemini CLI / VS Code / Cursor 干脆无该字段。⇒ 白名单声明必须核"被约束的是哪一类调用"，而非"有没有这个字段"。
- 提升层：可复用 Skill + 工具。触发词：白名单只管工具调用面、数据面旁路、support may vary、准入例外≠能力授予。

## 校验失败的处理半径由错误严重度决定，且"静默跳过"是显式设计不是缺陷：整技能拒 / 仅告警跳过 / 未知顶层字段为前向兼容而忽略（来源：learn.microsoft.com/en-us/agent-framework/agents/skills、docs.dify.ai/.../plugin-info-by-manifest、docs.n8n.io/.../n8n-nodes-base.executeworkflow.md，2026-10-01 r362-Q-C 实拉）
- 判据：① 非法 YAML / 重复键 / 大小写错 ⇒ **整技能拒绝加载**；`metadata` 内错误 ⇒ **仅告警跳过**；**未知顶层字段 ⇒ 为向前兼容而刻意忽略**；MCP 归档 **只接受 ZIP，TAR 类静默跳过**。② 校验器要输出"哪些被拒、哪些被忽略、哪些被静默跳过"三本账，只有一本可以省略。③ 反例：`n8n-nodes-base.executeworkflow` 错误传播全文只有一句"parent workflow can't trigger it"（无 error output / 无上限）——**文档层丢弃半径不可判时，须记为文档缺口而不是能力缺口**。
- 提升层：可复用 Skill + 工具。触发词：错误严重度决定丢弃半径、整技能拒/告警跳过/静默忽略、TAR 静默跳过、文档缺口≠能力缺口。

## 学习轮沉淀区（本段）
（r历史 起的连续学习轮章节共 338 章已下沉 references/knowledge-base.md §≤200迁移，正文留此指针）

## 技能「调用面 ≠ 入口面」：user-invocable:false 仍可被模型调用，加载源有显式优先级链…（原文已下沉 references/knowledge-base.md §L481）
## 技能进化不要自由变异，要「分解进固定能力空间 + 定向修订」…（原文已下沉 references/knowledge-base.md §L486）
## 技能控制流外置为显式状态机（EFSM）：知识与控制流分离，用显式状态转移替代模型猜下一步（细则见 KB，2026-09-30 r320A 下沉）

## 卸载必须留「显式卸载」marker（enabled: false tombstone），阻断启动修复静默重装；重装不静默恢复启用（来源：docs.openclaw.ai cli/plugins/uninstall-and-update，2026-09-30 r320A 实拉）

## 撤销与审核分层：吊销只阻断后续发布、不推翻既有审核结论；恢复走 successor 重跑检查并保留失败尝试为审计史…（原文已下沉 references/knowledge-base.md §L495）
## 修订整包不可变且发布只对新会话生效、陈旧编辑报冲突不覆盖；「加载位置」与「谁能看见」是两个独立控件且子级列表非空即整体替换；硬平台过滤不可被 always 豁免（来源：docs.openclaw.ai/tools/skills.md，2026-09-30 r321A 独立实拉 39,741B；细则见 references/knowledge-base.md §r321A）
## 并发写仲裁三件套（陈旧写报冲突 / 相同保存 no-op / 会话钉修订）与幂等契约四元组（键作用域·占用时点·失败是否回放·保留期）；代理不得自动重试非幂等请求（来源：docs.openclaw.ai/tools/skills.md 39,705B + docs.stripe.com 1,336,845B + RFC 9110 §9.2.2 502,941B，2026-09-30 r322C 独立实拉；细则见 references/knowledge-base.md §r322C）

身份级仲裁三件套：持久身份复用免重排 / 同身份第二实例被罚出 / 身份+序号二元组去重——并发去重要先有身份，再谈序号身份级仲裁三件套：持久身份复用免重排 / 同身份第二实例被罚出 / 身份+序号二元组去重——并发去重要先有身份，再谈序号（来源：kafka.apache.org/43/design/design/ 146,232B，2026-09-30 r323B 独立实拉；与 §并发写仲裁三件套/§幂等契约四元组 互补——那条管“写冲突怎么判”，本条管“谁算同一个写者”）（原文已下沉 references/knowledge-base.md §r325C）
审批门要配齐四个旋钮（启用选择器 / 豁免主体 / 在途隔离 / 超时去向）；缺第四个时 pending 可无限挂起审批门要配齐四个旋钮（启用选择器 / 豁免主体 / 在途隔离 / 超时去向）；缺第四个时 pending 可无限挂起（来源：www.activepieces.com/docs/flows/flow-approvals.md，2026-09-30 r323C 独立实拉 2,500B；与 §并发写仲裁 互补——那条管“写冲突”，本条管“变更放行”）（原文已下沉 references/knowledge-base.md §r325C）
## 扩展点是「观察 + 否决」双职：回调里抛错即可阻止被钩的操作，且钩子无沙箱、回调继承宿主实例全权限——扩展点的权限边界等于宿主权限，选钩前必须先声明（来源：docs.n8n.io/hosting/configuration/external-hooks/ 1,023,234B，2026-09-30 r324B 独立实拉，原文 lowercase「forbid an action by throwing an error」命中；与 §审批门四旋钮 互补——那条管“变更怎么放行”，本条管“放行机制自身有多大权”；细则见 references/knowledge-base.md §r324B）


## 版本义务沿引用图传递：改动一个被依赖的文件，即使接口没变也要 bump 全部下游引用者（来源：pipedream.com/docs/components/contributing/guidelines.md 43,351B，2026-09-30 r325C 独立 curl 实拉逐串命中「If you update a file, you must increment the versions of all components that import or are affected by the updated file.」；经 Qoder r357-Q-A 提名；与已落「接口形状判破坏」互补——那条管"算不算破坏性变更"，本条管"谁的版本号必须跟着动"）
- 原文语境：Pipedream 组件注册表的版本号规则——新增 action 起 `0.0.1`；`0.1.0` 上修 bug 提 `0.1.1`；**「If you update a file, you must increment the versions of all components that import or are affected by the updated file.」**
- 判据：① **版本号是"内容指纹"而不只是"兼容性标签"**：兼容性只决定 major/minor/patch 走哪一位，而"要不要 bump"由**是否被影响**决定——即便对外接口一字未改，只要被依赖文件的行为变了，依赖它的组件版本号就必须动；② **依赖闭包内的传播必须显式执行**：改动公共文件时，负责人要把受影响清单枚举出来（按 import 图，而不是凭印象），逐条提版，否则消费方按旧版本号做缓存/准入判定，会拿到**旧判定 + 新代码**的错配组合；③ 这条与"锁定版本"是一对：一边要求下游写死版本号，另一边就必须保证**上游变动会强制推着下游动**——只锁不传就是死锁，只传不锁就是失控；④ 落地时把它写成 CI 检查而非人工纪律：`git diff` 出改动的公共文件 → 反查 import 闭包 → 断言每个闭包成员的 version 字段都变过。
- 提升层：可复用 Skill/工作流。触发词：版本义务传递、import 闭包 bump、被影响即须提版、改公共文件连带提版、dependencies for any app component。

## 打包门禁的保留词表应含「背书语义词」，且检查必须跑在归一化形式上（来源：ClawHub publishing 本机实拉，r326C）
- **原文**：硬拒 16 个 topic——`approved / audited / certified / clawhub / community / curated / endorsed / featured / official / officials / openclaw / recommended / staff-pick / trusted / trusted-publisher / verified`；「The check runs on the **normalized form**, so `Official` and `staff pick` are rejected too」；topic ≤48 字符、禁不可见格式字符；归一后重复**丢弃而不报错**（`git,Git` 算一个）。
- **判据**：① 保留词分两维：**防借厂商名义**（已落 3.29.0 claude/anthropic）+ **防作者自我认证**（本轮，拦的是「信任/认证形容词」）；② 门禁必须**跑在归一化形式**上（大小写/分隔符/复数），否则 `Official`、`staff pick` 直接绕过 ⇒ 任何字面量黑名单都要先声明归一化规则；③ 「归一后重复丢弃不报错」是**容忍策略**，与硬拒词表是两条不同处置线，别混。
- **提升层**：可复用 Skill。触发词：背书语义词、自认证词、reserved topics、归一化检查、大小写绕过。

- **元数据字段三态语义 + 「改元数据即发新版」的批量副作用（来源：ClawHub publishing 本机实拉，r326C）**：本章已下沉 `references/knowledge-base.md`（r326C）。
- **能力授予平面独立于「发现/归属」平面：库归属只给管理与发现权，不自动授予其声明的工具/凭证/安装权；共享 Gateway 是单一信任域，密钥不得进入 skill 内容（来源：docs.openclaw.ai/tools/skills.md 39,741B，2026-09-30 r327A 独立实拉）**：本章已下沉 `references/knowledge-base.md`（r327A）。
- **指令 vs 知识分离：静态参考资料外置到按需检索，不塞进每次全量加载的指令（来源：www.activepieces.com/docs/agents/knowledge.md 2,613B，2026-09-30 r327C 独立实拉）**：本章已下沉 `references/knowledge-base.md`（r327C）。
- **测试分层分类法：四层各管一种失败模式，选错层=慢/冗余/静默无效（来源：Activepieces《Testing Strategy》handbook 5,560B，2026-09-30 r336C 独立实拉）**：本章已下沉 `references/knowledge-base.md`（r336C）。
## 技能/工具按任务语义检索 + 诚实无匹配（来源：Activepieces `mcp/tool-search.md` 3,608B，2026-09-30 实拉）

1. **检索=按任务描述语义搜，非按名翻目录**：agent 用自然语言任务描述（「发消息到 Slack 频道」）语义检索技能/工具，而非翻几百个目录；作者须为技能写「给 agent 看的 AI metadata 描述」才能被检索到。判据：技能元数据须带 agent-oriented 描述，否则不可被发现。
2. **低于相关性阈值的匹配丢弃而非填充，空结果=真无匹配**：检索结果低于阈值直接 drop，不拿弱相关凑数——空结果意味着目录里真没有，agent 应直说而非跑错工具。判据：选择逻辑须有阈值截断 + 诚实无匹配路径，禁止「凑一个最可能错的」。

- 提升层：可复用 Skill。触发词：语义检索、诚实无匹配。

## 技能自动修补的授权令牌三件套 + 所有权按目录判定 + 扫描分级只 critical 阻断（来源：docs.openclaw.ai/tools/self-learning 16,747B + /tools/skill-workshop/how-it-works 4,288B，2026-09-30 r338A 独立实拉）

1. **修补先取授权令牌，patch 必须引用同一 span**：`prepare_patch` 只授权「一个非空唯一精确 span」并返回有界上下文；下一次 `patch` 必须引用同一 span，**授权在一次尝试后或目标变更时即失效**，同一技能在授权被消耗/作废前的第二次 `prepare_patch` 被拒。判据：对技能的自动修补必须是「先锚定 → 按锚改 → 一次一锚」，禁止凭模糊匹配改写文件。
2. **运行时使用回执：只允许修补本次运行确实用过的技能**：原文 `A runtime usage receipt prevents foreground repair of skills that the run did not use`。判据：越界修补的判据不是「这个技能存不存在」，而是「这次运行有没有用过它」——没用过就没有修补资格，防止顺手改无关技能。
3. **所有权按目录判定，非自有来源只说明不编辑**：`A skill is Workshop-owned exactly when it is contained in that agent's directory`；bundled / ClawHub 安装 / 插件提供的技能由其 owner 的更新替换，agent 只说明不编辑；`create` 在目标已存在时直接失败（no clobber）。判据：**可写性由「归我管的目录」判定，不由名称或来源声明判定**。
4. **扫描分级，且关键词命中 ≠ 语义违规**：apply 前重跑安全扫描，**只有 critical 阻断 apply，warn 可见不阻断**；`Prompt-related keywords are not scanner findings`——提到「隐藏指令 / 工具审批」不构成指令覆盖。判据：静态扫描必须分级，命中敏感词不等于违规，否则扫得越全越不敢写。

- 提升层：可复用 Skill / 安全边界。触发词：修补授权令牌、prepare_patch、usage receipt、目录所有权、no clobber、critical 才阻断、关键词不等于违规。


- **无法交互时的兜底默认落在拒绝侧；长期授权要有四态可见与显式期限；允许清单的增删是幂等写（来源：docs.openclaw.ai/cli/approvals.md 16,110B，2026-10-01 r339C 独立 curl 实拉逐串命中）**：本章已下沉 `references/knowledge-base.md`（r339C）。
## 宿主能力须前置声明并 fail-closed；同一插件的三类失败走三条不同处置路径（来源：docs.openclaw.ai/concepts/context-engine.md 26,167B，2026-10-01 r343A 独立 curl 实拉逐串命中）

- **原文**：①「Context engines can declare host capability requirements on `info.hostRequirements`. OpenClaw checks these requirements **before starting the operation** and **fails closed with a descriptive error** when the selected runtime cannot satisfy them.」「`requiredCapabilities: ["assemble-before-prompt"]`, `unsupportedMessage: "Use the native Codex or OpenClaw embedded runtime, or select the legacy context engine."`」；②「If a non-legacy engine is missing, fails contract validation, throws during factory creation, or throws from a lifecycle method, OpenClaw **quarantines** that engine for the current Gateway process and **downgrades** context-engine work to the built-in `legacy` engine ... so the agent [does not go] silent.」+「**Host admission and resource-ownership failures before factory entry propagate without quarantining** the engine.」+「**Host requirement failures are different**: ... OpenClaw **fails closed before starting the run**. That protects engines that would corrupt state if they ran in an unsupported host.」；③「Set `info.acceptedHostParams` to restrict the host-added lifecycle fields the engine receives ... **Engines without this declaration receive every current host field**; declare an explicit list, **including `[]`**, when the engine validates a narrower input shape.」
- **判据**：① **能力需求必须在启动前声明并被前置校验，不满足就硬失败而不是"带着缺陷跑"**：兼容性与不兼容是二值事实，用降级来"兼容"只会把崩溃推迟到状态被写坏之后；失败消息必须给出可执行替代（`unsupportedMessage` 指明换哪个运行时/回退实现）。⇒ 写可插拔能力时，先声明"我要求宿主具备什么"，再让宿主在启动前裁决；不要靠 try/catch 在运行中试探。② **同一个组件的失败不是一种处置，而是按失败位置分三条路径**：生命周期内抛错/契约校验失败/工厂创建失败 → **隔离 + 降级保活**（目标是"别让 agent 沉默"）；宿主能力不满足 → **运行前 fail-closed 预拒**（目标是"别在不兼容环境上写坏状态"）；准入与资源归属失败（工厂入口之前）→ **直接向上传播，不降级不隔离**（目标是"别把宿主自身的问题伪装成插件问题"）。⇒ 判据是**这条失败会不会污染状态**：会污染 → 预拒；不污染但会中断服务 → 降级保活；根本不是本组件的错 → 原样抛。③ **参数面的默认极性是"全给"，最小权限必须显式声明空列表**：不声明 `acceptedHostParams` 的引擎会收到宿主拥有的全部字段，声明后才与可用字段求交、未知键永不注入。⇒ 接口默认开放意味着"最小权限"是一个要写出来才存在的东西（写 `[]` 才算零字段）；同理，声明与可用集合求交意味着**新增宿主字段不会自动灌进已声明的窄接口**，这是防漂移的边界。
- **提升层**：可复用 Skill / 安全边界。触发词：hostRequirements、requiredCapabilities、unsupportedMessage、fail-closed 预拒、隔离降级保活、准入失败不降级、acceptedHostParams、默认全给、显式空列表、接口默认极性。


## 命名冲突只改自动别名并保留直达入口；确定性路由要显式声明；授权清单是覆盖式唯一权威（来源：docs.openclaw.ai/tools/slash-commands.md 38,378B，2026-10-01 r343B 独立 curl 实拉逐串命中）

- **原文**：①「`/dashboard` is reserved as a built-in command. If an existing user skill is named `dashboard`, skill discovery exposes its generated slash alias as `/dashboard_2`. **`$dashboard` and `/skill dashboard` continue to select that user skill directly.`**」；②「By default, skill commands **route to the model as a normal request**. Skills can declare `command-dispatch: tool` to **route directly to a tool (deterministic, no model involvement)**.」；③「When configured, it is the **only authorization source** for commands and directives.」「`a denied sender or an explicitly empty list cannot fall back to channel admission.`」
- **判据**：① **命名空间冲突的处置是"表层别名退让 + 保留显式直达入口"，不是覆盖也不是禁用**：自动生成的别名改名（加数字后缀）只作用于自动派生的那一层，显式调用名（`$name` / `/skill name`）必须原样可用。⇒ 若改名把显式入口一起改掉，用户手写的调用就静默失效；判断一个冲突处置方案好不好，就看"用户已经写出去的调用还能不能用"。② **同一入口的两种执行语义（过模型 vs 直达工具）必须由能力自己显式声明，且默认是"过模型"**：默认走模型意味着结果不确定，想要确定性必须额外声明 `command-dispatch: tool`。⇒ 把"要不要让模型介入"当成能力的一个**声明属性**而不是调用时的隐式行为；默认非确定性这条要写进契约，否则调用方会误以为同名入口每次行为一致。③ **显式授权清单是覆盖式唯一权威，不是叠加项，且"配了空"等于"全拒"**：一旦配置该清单，通道授权等其他来源全部失效；空列表不是"没配置"而是"明确拒绝所有人"，且**不允许回退**到更宽松的通道准入。⇒ 权限面最危险的默认就是"配不上就回退"——它让"收紧"这个动作在配错时反而变宽；授权清单必须语义单一：存在即唯一权威，空即全拒。
- **提升层**：可复用 Skill / 安全边界。触发词：命令名冲突、保留字冲突、别名退让、显式直达入口、command-dispatch、确定性路由、默认过模型、授权清单覆盖式、空列表全拒、不可回退。


## 权限上限在创建时刻快照且不可自增；一次性提权四要素；管理权不转移归属（来源：docs.openclaw.ai/automation/cron-jobs/payloads.md 27,960B + managing-jobs.md 17,374B，2026-10-01 r343C 独立 curl 实拉逐串命中）

- **原文**：①「Jobs created by an agent are **capped to the tools available to that creating turn**, and the agent **cannot widen** the stored list.」「**Management edits cannot restore missing policy metadata as operator authority.** For a legacy job that has lost its policy, an authenticated operator can explicitly reauthorize it, or an authenticated creator can recreate it with a fresh tool cap.」；②「**Changing an account-bound job to a payload that does not run tools and later back to an agent turn preserves its account restriction. A payload conversion does not reauthorize that job as an operator-created job.**」；③「Each operation uses a **one-use grant that expires after 60 seconds** and remains **bound to that exact active run**. Channel owner membership is **rechecked ... immediately before a mutation commits**.」「**Channel allowlists, wildcard entries, display names, account IDs, and session routes do not establish ownership.**」；④「The continuation remains **management-only; it cannot capture new creator execution authority**.」「Management authority **does not transfer creator attribution**」「An incomplete tool capture still prevents inheriting an uncaptured tool surface.」
- **判据**：① **权限上限是"创建时刻的快照"，创建者本人也不能放宽**：作业的工具上限由创建它的那一次运行当时拥有的权限决定并固化，之后任何编辑都不能超过它；策略元数据一旦丢失，不能靠"编辑一下"偷偷补回来，只能由更高权限者显式重授，或由创建者按新的上限重建。⇒ 这堵死了"先建个受限的、再慢慢改宽"这条最常见的提权路径；设计时要区分**授权（可授予的）**与**归属（不可转移的）**两件事。② **换形态不换身份**：把受限作业改成不需要权限的形态、再改回需要权限的形态，原有账户限制原样保留，不会因为"重新走了一遍创建流程"就被重新授权。⇒ 防止用"形态往返"洗钱式绕过；判据是**授权绑定在主体上，不绑定在当前形态上**。③ **一次性提权必须同时具备四要素：单次使用 / 短时过期 / 绑定到确切的那次运行 / 在真正写入前再核一次成员名单**；并且**表面标识一律不构成所有权证据**——允许列表、通配符、显示名、账号 ID、会话路由，看着像 owner 的都不算。⇒ 提权令牌一旦可复用、可跨运行、或只在开头核一次，就等于把"当时是 owner"变成了"一直是 owner"。④ **管理权 ≠ 创建权**：接管过来的权限只能管理，不能据此变成创建者，也拿不到当初没捕获到的工具面。⇒ 委派管理时要显式声明"本次委派授予的是哪一层"，未捕获的能力不许在委派后自动补全。
- **提升层**：安全边界/工具。触发词：创建时刻权限快照、创建者不能自增、丢失授权不自动补、形态转换不重新授权、一次性提权四要素、60 秒过期、绑定单次运行、写入前再核、表面标识不构成所有权、管理权不等于创建权。

- **同一寻址语法「读可模糊、写必须确定」+ 写入前拒模式化路径 + validate 不触文件系统 + 字节往返自证**：本章已下沉 references/knowledge-base.md §r346A。

## 技能修订要有「预算 + 被拒缓冲 + 离线巩固位」三旋钮，且候选修订只在留出集严格变好时才被接受（来源：github.com/microsoft/SkillOpt README 8,573B（17,912★）+ agentman.ai 报告引 SkillsBench，2026-10-01 r348A 独立 curl 实拉）
- 原文：①「A candidate edit is accepted only when it strictly improves a held-out validation score.」②「A textual learning-rate budget, a rejected-edit buffer, and an epoch-wise slow / meta update.」③「SkillOpt-Sleep, a nightly offline self-evolution engine (harvest → mine → replay → consolidate behind a held-out validation gate).」④产物体积 300–2,000 tokens、部署期零模型调用。⑤粒度证据：2–3 个聚焦技能 +18.6pp，单体技能 −2.9pp（SkillsBench 47,150 技能）。
- 判据：① **修订速率本身要设预算**：「学习率」在文本空间同样存在 —— 一次改太多会把已验证行为一起改坏，改太少则永不收敛；预算 + 被拒样本缓冲（记住改了什么被拒，防止重复试错）+ 慢速/元更新分层，是三件独立旋钮，不能只用「跑几轮」代替。② **接受门必须是留出集上的严格改进**（不是不变差、也不是平均变好）：留出集要与修订用的集分离，否则就是自证。③ **离线巩固位必须在门后**：harvest→mine→replay→consolidate 整条链都跑在留出集门后面；「先合并、后验证」会让坏修订进入基线。④ **技能粒度有方向性证据**：2–3 个聚焦技能显著优于一个大而全的技能（+18.6pp vs −2.9pp），收益来自「每次装载时不相干内容不进上下文」。
- 提升层：可复用 Skill。触发词：文本学习率预算、被拒编辑缓冲、留出集严格改进门、离线巩固、SkillOpt-Sleep、技能粒度 2-3 个聚焦。

## 钩子分「观察面 / 干预面」两级：handler 返回值不参与控制流，且效果位按命令路径分档（来源：docs.openclaw.ai/automation/hooks/writing-hooks.md 10,721B + event-types，2026-10-01 r348A 独立 curl 实拉）
- 原文：①「Returned values do not block, cancel, or rewrite the operation.」②「`/new` and `/reset` — Awaits handlers, joins strings with blank lines」；`/stop`、automatic reset、message events、bootstrap、patch 与 Gateway lifecycle 事件一律忽略回复。
- 判据：① **返回值不阻断、不取消、不改写操作** —— 要干预必须走 typed plugin hook（干预面），观察型 handler 只能看不能改。⇒ 把「能不能拦下来」寄托在返回值上会静默失效：钩子跑了、日志有了，操作照旧。② **效果位按命令路径分档**：同一 handler 产出的 messages 只在 `/new`、`/reset` 两条路径被消费，其余路径全部忽略。⇒ 验收钩子「有没有生效」必须先确认当前路径在不在消费白名单内；在 `/stop` 路径上等回复，等不到不是 bug 是设计。
- 提升层：工作流。触发词：钩子观察面干预面、返回值不阻断、typed plugin hooks、效果位按路径分档、/new /reset 才消费。

## 技能的典型失败是「把可选校验写成强制劳动」：效率退化多于功能失败，归因要用差分运行（来源：arXiv 2608.11888 43,498B，2026-10-01 r348C 独立 curl 实拉，`307` / `125` / `182` / `excessive verification … 67` / `mandatory work` 逐串命中）
- 判据：① **307 例技能诱发失败 = 125 功能失败 + 182 效率退化 —— 效率类比功能类更多**。⇒ 「加了技能变慢/变啰嗦」是一等回归维度，不是可以牺牲的副作用；回归清单里必须有成本项，否则技能会静默劣化体验。② **清单要显式区分「必须步骤」与「建议步骤」**：最大失败源是「把校验清单与构建配方写成强制劳动」（过度验证 67 例 + 重型实现管线 30 例）。⇒ 写技能时给每条校验标注强制/建议，并说明强执行的代价；**没有这个区分，清单本身就是成本**。③ **归因必须用差分运行**（同一任务 skill-guided vs no-skill，或与语义匹配的参照技能对比），不能看绝对分数。⇒ 「用了技能之后分低了」在没有配对基线的情况下无法归到技能头上。④ **「看起来相关的技能」最危险**：它会诱导 agent 错误实现或漏实现任务必需元素 —— 相关性 ≠ 安全性。
- 提升层：可复用 Skill。触发词：过度验证、强制劳动、效率退化多于功能失败、差分归因、配对基线、相关性不等于安全性。

## 技能复用失败的主因是打包缺陷而非攻击，且缺陷分布按「是否 spec-aware / 是否 AI 批量生成」分档（来源：arXiv 2608.08453 42,317B，2026-10-01 r348C 独立 curl 实拉，`138,133` / `91.8%` / `88.8–94.6%` / `specification-aware` 逐串命中）
- 判据：① **质量的默认怀疑方向应是「元数据 / 正文体积 / 目录结构」这类可机检项**，而不是恶意内容：138,133 份公开 SKILL.md 中 **91.8%** 至少一处缺陷（宽松/严格阈值下稳定在 88.8–94.6%），主因是「weak routing metadata, bloated or non-actionable bodies, and poor resource organization」。⇒ 审技能先过这三项，收益远高于先做安全扫描。② **lint 至少三项**：路由元数据是否含匹配条件 / 正文是否含可执行动词 / 重资源是否已外置为按需读文件。③ **分层结论要写进验收**：spec-aware 技能缺陷更少，而 **AI 批量生成的技能在安全与可移植维度是更差而非更好的批次**。⇒ 批量生成只解决「有没有」，不解决「能不能用」，且会带来新的一类可移植问题。
- 提升层：可复用 Skill。触发词：138133 SKILL.md、91.8% 缺陷率、打包缺陷非攻击、路由元数据 lint、正文可执行动词、资源外置、AI 生成批次安全更差。

## 截断要按「入参 / 上下文 / 产出」三处分别设防：入口载荷在消费前定长截断是独立防御位（来源：docs.dify.ai/en/cloud/use-dify/nodes/agent.md 10,240B，2026-10-01 r349A 独立 curl 实拉，`truncated at 2,000 characters` / `50 MB` 逐串命中；经 Qoder r366-Q-A 提名）
- 原文：「Variables you pull in reach the agent as text and are **truncated at 2,000 characters**」；同页导出产物上限 `50 MB`。
- 判据：① **既有截断先例全在上下文 / 输出 / 历史窗口侧，入参侧长期裸奔** ⇒ 预算三处各设一处，缺一处就有一处无上界。② **入参截断的价值是「在消费前定长」**：变量进入 agent 前被砍到 2000 字符，下游再怎么展开也不会把入口撑爆；只做输出侧截断，入口一个巨型字段就足以占满预算。③ **导出 / 落盘类产物要单列上限**（50 MB），与文本截断不是一个量纲，混用会互相掩盖。
- 提升层：工具。触发词：入参截断、2000 字符、入口载荷定长、三处预算位、导出上限 50 MB。

## 技能正文要「教方法」而不是「给答案」，且 token 是竞争关系而非占用关系（来源：agentskills.io/skill-creation/best-practices.md 14,864B，2026-10-01 r349A 独立 curl 实拉，`Favor procedures over declarations` / `class of problems` / `competes for the agent's attention` 逐串命中；经 Qoder r366-Q-A 提名）
- 原文：①「**Favor procedures over declarations** — A skill should teach the agent how to **approach a class of problems**, not what to produce for a specific instance」；②「Every token in your skill **competes for the agent's attention** with everything else in that window」。
- 判据：① **评审问句换成「教了方法还是给了答案」**：写死某一个具体实例的产出，换个输入就失效；给出处理一整类问题的程序才具备泛化。② **token 是竞争关系**：每写进正文一行都在挤占同一窗口里其它信息的注意力，不是「占了点空间」而已 ⇒ 正文取舍的判据是「这行在抢谁的注意力、值不值」，而不是「还剩多少额度」。③ 与既有「500 行 / 5000 token 体积预算」互补：那是上限，本条是**上限之内怎么排序**。
- 提升层：可复用 Skill。触发词：程序优先于声明、教方法不给答案、class of problems、token 注意力竞争、正文取舍排序。

## 把一段逻辑提升为可复用单元是「三件事」：跨单元引用转参数、剥离入口型构件、声明执行序不继承父级（来源：docs.n8n.io/build/flow-logic/convert-to-sub-workflows.md 5,126B，2026-10-01 r349B 独立 curl 实拉，`automatically updated and added as parameters` / `Must not include trigger nodes` / `regardless of the parent workflow's settings` 逐串命中；经 Qoder r367-Q-B 提名）
- 原文：①「Expressions referencing other nodes are **automatically updated and added as parameters** in the Execute Workflow Trigger node」；②「**Must not include trigger nodes**」；③「New workflows use v1 execution ordering **regardless of the parent workflow's settings**」。
- 判据：① **隐式引用必须改写成显式参数**才能审计：跨单元的引用若仍靠「节点名全局可解析」，重命名一个节点就会在看不见的地方断链。② **入口型构件必须剥离**：子单元里留着 trigger，等于同时保留两个触发源（父调一次、自己触发一次）。③ **执行序语义不继承父级**是最隐蔽的行为差：同一段逻辑在两处跑出不同顺序，不是 bug 而是「谁声明了序」的问题 ⇒ 提升时必须显式写死子单元的序语义，否则复用即换行为。
- 提升层：可复用 Skill/工作流。触发词：提升为子流程、隐式引用转参数、剥离 trigger、执行序不继承父级、v1 execution ordering。

## 「发现集刷新」必须做成可挂事件，否则新装的技能在本次会话内不可见（来源：code.claude.com/docs/en/hooks.md 248,712B，2026-10-01 r349B 独立 curl 实拉，`reloadSkills` ×5 命中；经 Qoder r367-Q-B 提名）
- 原文：SessionStart 决策控件 `reloadSkills`；配套说明「use `reloadSkills` when a SessionStart hook **installs or updates skills**」。
- 判据：① **安装 ≠ 可见**：技能注册发生在会话开始时，中途新增的技能不会自动进入发现集 ⇒ 「装了却搜不到」的默认怀疑方向应是发现集未刷新，而不是安装失败。② **刷新要做成显式事件挂钩**而不是靠重启：把刷新动作暴露成可配置项，才能让「安装后立即生效」成为可组合的一步。③ 与既有「发布只对新会话生效、会话钉死所选修订」同族但不同层：那条讲已加载修订的钉定，本条讲**候选集本身的刷新时机**。
- 提升层：可复用 Skill。触发词：reloadSkills、发现集刷新、安装后不可见、SessionStart 刷新技能、新技能不生效。

## 描述可发现性可以量化调优：多次运行取阈值、必须含 near-miss 负例（来源：agentskills.io/skill-creation/optimizing-descriptions.md 13,307B，2026-10-01 r349C 独立 curl 实拉，`3 runs` / `threshold` / `near-miss` 逐串命中；经 Qoder r368-Q-C 提名）
- 原文：每条评测 prompt 跑 **3 runs**、以 `threshold` 判触发成功率；评测集须含 **near-miss**（术语重叠但目标不符）负例。
- 判据：① **触发是概率事件，单次运行不可作结论**：同一条 prompt 多次运行取成功率，才能把「这次没触发」与「这个描述不触发」分开。② **near-miss 负例是描述调优的关键样本**：只有明显不相关的负例，会得到一个「什么都能触发」的过度宽泛描述；近义负例才逼出边界。③ 与既有「触发评测」互补：那条讲要做触发评测，本条给**样本构成与重复次数**。
- 提升层：可复用 Skill。触发词：描述调优协议、3 runs、触发阈值、near-miss 负例、dev/泛化集划分。

## 技能脚本的 headless 契约：输入只走 flags/env/stdin，交互式输入会永久挂起（来源：agentskills.io/skill-creation/using-scripts.md 12,743B，2026-10-01 r349C 独立 curl 实拉，`interactive prompts` / `cannot respond to TTY prompts, password dialogs, or confirmation menus` / `interactive input will hang indefinitely` 逐串命中；经 Qoder r368-Q-C 提名）
- 原文：脚本「**cannot respond to TTY prompts, password dialogs, or confirmation menus**」；「interactive input will **hang indefinitely**」。
- 判据：① **执行环境是 headless，任何等待人输入的路径都是挂起而不是报错** ⇒ 脚本里出现 `read`、密码框、确认菜单，表现是任务卡住无输出，而不是失败提示。② **输入只能走 flags / env / stdin 三条显式通道**：参数化要在这三条里选，不要依赖运行时询问。③ 与既有「技能正文命令要可复制执行」同向：那条讲**指令形态**，本条讲**被调用脚本的输入面**。
- 提升层：工具。触发词：headless 脚本契约、禁交互式输入、TTY prompts 挂起、flags/env/stdin 三通道。

## 注册表加载器要「宽容分级」：只有缺必填字段才判失败，其余偏差 warning 放行；重名必打 shadow 告警（来源：agentskills.io/client-implementation/adding-skills-support.md 20,357B，2026-10-01 r349C 独立 curl 实拉，`warning when a collision occurs so the user knows a skill was shadowed` / `untrusted repositories from silently injecting instructions` 逐串命中；经 Qoder r368-Q-C / r370-Q-B 提名）
- 原文：①同域重名按序取胜但「**warning when a collision occurs so the user knows a skill was shadowed**」；②「prevent **untrusted repositories** from silently injecting instructions into the agent's context」。
- 判据：① **严拒会把生态碎片全挡在门外**：id 不匹配、长度超限这类偏差一律 warning 放行，只有缺必填字段才判失败 ⇒ 加载器的严格度要按「能不能推断出意图」分档，不是按「是否完全合规」。② **遮蔽必须可见**：重名取胜是确定性规则，但胜出的同时要告诉用户「有另一个被遮蔽了」，否则「我装的怎么没生效」无解。③ **不受信来源要挂起待人工放行**：目标是阻断「静默注入」，而不是阻断「来自第三方」。
- 提升层：可复用 Skill。触发词：加载器宽容分级、仅缺必填判失败、shadow 告警、不受信仓库挂起、静默注入阻断。

## 长期授权的「已撤销」要按三条边界判：版本边界 / 进程边界 / 时间边界互不蕴含（来源：docs.openclaw.ai/cli/approvals.md 16,110B，2026-10-01 r349C 独立 curl 实拉，`--expires-in-days` ×2 / `tools.exec.grantExpiryDays` 逐串命中；增量于既有 r339C standing grant 生命周期；经 Qoder r372-Q-A 提名）
- 原文：cron 所铸 grant 默认永久，须 `--expires-in-days`（配置项 `tools.exec.grantExpiryDays`）显式收敛。
- 判据：① **版本边界**：编辑自动化定义即失效 —— 授权绑定的是载荷指纹，改了载荷等于重新申请，不是「同一个授权继续有效」。② **进程边界**：revoke 只在下次 spawn 生效，**已运行实例继续持有** ⇒ 「已撤销」在进程存续期内不成立。③ **时间边界**：过期天数。三者互不蕴含 ⇒ 审计「这个授权现在还有效吗」必须逐边界判，不能以「执行过撤销动作」为准。④ 默认永久意味着**不显式收敛就是无限期**，与「最小权限」相反，必须主动设期限。
- 提升层：可复用 Skill。触发词：grantExpiryDays、授权失效三边界、版本边界改载荷即撤销、进程边界 revoke 下次 spawn、默认永久须显式收敛。
## r351C · 技能成本是"区间"不是标量：分发侧须公示上下界（来源：skills.aliyun.com `/api/public/skills?categoryCode=aiml&pageSize=3`，200 / 25,150B JSON，2026-10-02 r351C 独立 curl 实拉）

- **实证**：条目字段含 `minToken` 与 `maxToken` 成对出现——实测 `alibabacloud-agentbay-aio-skills` = **minToken 21205 / maxToken 167456**（**上下界相差约 7.9 倍**）；同批另两条 21216/47349（2.2×）与 26641/124152（4.7×）。另有 `hosted`（实测 false，即不托管、内容源在 `githubPath`）、`totalInstallCount`、`likeCount`、`updatedAt`。
- 判据：① **成本必须按区间公示与选型**——单点 token 估算（"这个技能约 2 万 token"）在跨度 2–8 倍的东西上是误导；装前预算按 **上界** 算，否则上下文挤爆发生在最坏路径上。② **跨度本身就是质量信号**：上下界差得越大，说明该技能的加载量越依赖输入/分支，越需要说明"什么情况下走到上界"。③ 与已落的三级披露 token 预算互补——那条管**加载机制内的预算数值**，本条管**分发侧对外承诺的成本区间**，两者不在同一层。④ `hosted` 必须一并公示：**托管与否决定别人能否独立验证内容**；未托管条目的真实内容以 `githubPath` 为准，市场页只是索引。
- 落地动作：技能/插件的元数据表增加 `minToken`+`maxToken` 双字段与 `hosted` 布尔；写"成本"时一律写区间并标注上界触发条件，禁止只给均值或单点值。
- 提升层：可复用 Skill / 工具。触发词：minToken、maxToken、成本区间、上界预算、hosted 托管标记、技能元数据。


## r354A · 新能力默认关闭 + 行为不变承诺 + 逐能力生效，不是全局开关（来源：docs.n8n.io `deploy/host-n8n/configure-n8n/durable-scheduler.md`、`configure-n8n/system-tasks.md` 独立 curl 取 `.md` 原文，2026-10-02 r354A 实拉）

- **★默认关 + 老实例行为不变**：原文 "It's **off by default**: existing instances keep using the in-memory scheduler and **behave as before until you opt in**"。判据：**引入会改变既有行为的实现时，缺省必须是"不变"**——让升级者先得到与旧版一致的行为，再显式选择新语义；把新语义做成默认，等于让所有存量在不知情的那一刻同时改变行为。
- **★Preview → GA 是版本台阶**："available from n8n **2.36.0**. Earlier versions back to n8n **2.32.0** include it as a **Preview** feature"。判据：**能力成熟度要落到版本号上**——"某版本起可用"与"某版本起是预览"是两个不同的兼容承诺，混写会让依赖方按错的稳定性预期做设计。
- **★开关是逐能力生效的，开了主开关不等于全量迁移**：system-tasks 原文 "**As of n8n 2.41.0, no system task supports durable mode**, so every task runs from an in-memory timer"，且 "Only tasks that **support** durable mode move over; the rest stay on their in-memory timers"。判据：**"我开了 X" 与 "我的工作负载现在跑在 X 上" 之间隔着一层的——每个子能力各自声明是否支持**；审计时必须逐个核，不能拿主开关状态当结论。
- **★同一"错过"在两种模式下语义相反**：in-memory 下 "A run whose time passes while the instance is down **doesn't happen**"；且进程睡眠时 "the timer **fires once for all the occurrences it slept through** instead of replaying them one by one"（补跑被折叠成一次）；durable 下 "A run whose time passed while the instance was down **still fires late** when the instance comes back, as long as it's within its **grace period**; beyond that, the trigger's **misfire policy** decides"。判据：**"补不补跑"必须显式定义为三段（宽限期内补跑 / 超期按 misfire policy（丢弃 or catch-up）/ 根本不补），不能留成实现细节**——同一个缺失在两种模式下的处置不同，迁移时按旧心智模型推断会直接算错。
- **★跨实例"只执行一次"靠共享队列认领，不靠 leader 选举**："Every main instance shares the same queue and **claims runs** from it. Only one instance picks up each run"；而 in-memory 模式 "Only the **leader** fires schedules. If leadership changes at the wrong moment, **timing can slip**"。判据：**去重的正确落点是"对同一条待办的唯一认领"，不是"选出一个负责人"**——前者任一实例都能干活且天然不重复，后者把可用性绑在选举正确性上。
- 提升层：可复用 Skill / 工作流。触发词：默认关闭、行为不变承诺、Preview 到 GA、逐能力生效、misfire policy、grace period、claim 去重、leader 选举。


## r354B · 「允许用户覆盖」= 默认值 + 上限两个变量；同类参数在不同子系统是不同币种（来源：docs.n8n.io `use-environment-variables/executions.md` + `use-environment-variables/credentials.md` 独立 curl 取 `.md` 原文，2026-10-02 r354B 实拉）

- **★可覆盖参数必须由两个变量共同治理**：`EXECUTIONS_TIMEOUT`（默认 `-1`，`-1` 表示禁用）是实例级默认，"Users can **override this for individual workflows up to the duration set in `EXECUTIONS_TIMEOUT_MAX`**"（默认 3600）。判据：**"可自定义"如果只给默认值不给上限，等价于无约束**；而当默认值本身是"禁用/无限"时，上限就是唯一的实际约束——此时"我没改默认"意味着"我没设限"。
- **★同类"超时"在不同子系统单位与量级都不同**：执行超时 `EXECUTIONS_TIMEOUT` 是**秒**（默认 -1 / 上限 3600），AI/LLM 节点超时 `N8N_AI_TIMEOUT_MAX` 是**毫秒**（默认 3,600,000）。判据：**参数名相似不代表同币种**；跨子系统搬数值前必须确认单位与"禁用值"的表示（此处 `-1`），差 1000 倍是最典型的静默错误。
- **★敏感配置支持逐变量切换注入形态（内联 / 文件）**："You can add **`_FILE` to individual variables** to provide their configuration in a separate file"。判据：**"把秘密放到文件里"应做成逐变量的后缀约定，而不是全局改配置格式**——粒度在单变量，才能让"这一个走文件、那一个走内联"同时成立。
- **★分布式形态会让单实例下的默认值静默失效**：`CREDENTIALS_OVERWRITE_PERSISTENCE` 默认 `false`，原文 "**Required for multi-instance or queue mode** to propagate overwrites to workers through a publish/subscribe approach"。判据：**审视每一个默认值为"它在多实例/队列模式下还成立吗"**——单实例下无害的 false，在 worker 模式下表现为"主节点改了、工作节点没变"，且不报错。
- **★有默认值的显示名会静默产生同质垃圾**：`CREDENTIALS_DEFAULT_NAME` 默认 `My credentials`。判据：**给可命名实体设默认名，等于批量制造无法区分的同名对象**；要么默认值带上下文（环境/用途），要么强制命名。
- 提升层：可复用 Skill / 工具。触发词：可覆盖上限、EXECUTIONS_TIMEOUT_MAX、参数单位、毫秒秒混用、_FILE 后缀、多实例下默认值失效、默认名同质化。


## r354C · 能力可用性按部署形态逐项核对：云与自托管不是包含关系；许可缺失是 fail-fast 而非降级（来源：docs.n8n.io `scaling/use-external-storage.md` 独立 curl 取 `.md` 原文，2026-10-02 r354C 实拉）

- **★"自托管高配 / 云端没有"这种反向分布真实存在**：external storage 原文 "**Self-hosted:** Business, Enterprise. **It isn't available on n8n Cloud.**"（S3 二进制存储同样如此）。判据：**不要用"云版本总是功能更全"或"自托管总是更自由"来推断可用性**——两者是两条独立的产品线，同一能力在一侧有、另一侧可能完全没有；选型时逐能力查表，不做外推。
- **★许可门槛的失败模式是拒绝启动，不是功能降级**："Activate your license key **before** you enable external storage. n8n **won't start** in `s3` binary data mode without a valid license: set `N8N_DEFAULT_BINARY_DATA_MODE` to another mode or upgrade your plan"。判据：**硬依赖许可的能力在缺失时是 fail-fast（起不来），不是 graceful degradation（退回本地存储）**——这决定了配置顺序：先有许可、再开关能力；反过来配会让实例直接无法启动，而排查者往往先怀疑配置写错。
- **★清理责任随数据一起外包，默认结果是"永久保留"**："n8n **delegates pruning of binary data to S3**, so setting a lifecycle configuration is **required** unless you want to preserve binary data indefinitely"。判据：**把数据迁到外部存储时，生命周期策略不是附带获得的，而是必须另行配置的**——未配置的状态是"无限期保留"而不是"跟随主系统策略"；这与 r354A「清理停了也不报错」叠加，会形成长期静默增长。
- **★"支持"与"官方支持"是两档**："You can use other S3-compatible services like Cloudflare R2 and Backblaze B2, but n8n **doesn't officially support these**"。判据：**能跑通 ≠ 被支持**；承诺面由"官方支持"界定，排障与兼容性保障只覆盖那一档，选型时要把"兼容但未支持"单独列为风险项。
- 提升层：可复用 Skill / 工具。触发词：云与自托管反向分布、isn't available on Cloud、license 拒绝启动、fail-fast 许可、S3 lifecycle 必配、官方支持 vs 兼容。


## r355B · 召回要分两条通道：廉价的确定性通道在前，贵的深度通道只在「问过去 + 无强可信触发匹配」时才升级；检索形态按问题形状选，上下文量与超时是联动旋钮（来源：docs.openclaw.ai `concepts/active-memory.md` 7,276B + `concepts/active-memory/tuning.md` 4,601B，2026-10-02 r355B 独立 curl 实拉）

- **★默认 escalate：深度召回是条件触发的第二通道，不是默认路径**："The default `escalate` mode runs its blocking recall sub-agent **only when the message asks about the past and the deterministic memory lane found no strong trusted trigger match**. This keeps ordinary replies fast while preserving a deeper search path"。判据：**分层召回必须写成"先廉价后昂贵"，且要为"不升级"设明确门槛**（此处 = 确定性通道命中强可信触发）—没有门槛的分层等于每次都走贵的那条。
- **★检索形态要按问题形状选，一种检索打不了所有问题**："Flat retrieval is strongest for **direct fact matches** and **weaker on temporal and multi-session questions**"（文档并以 LongMemEval / PrefEval 作为该差距的证据）。判据：**先给问题分类（直接事实 / 时序 / 跨会话多跳），再选通道**；把扁平检索用于时序与多跳问题是结构性错配，不是调参能救的。
- **★上下文量是显式三档旋钮，且必须同步调超时**：`queryMode` = `message`（仅最新一条消息，`timeoutMs` 建议 3000–5000）/ `recent`（+ 少量近期尾巴，约 15000）/ `full`（整段对话，15000+，随线程增大）；原文要求 "Pick the **smallest mode** that still answers follow-ups well; grow `timeoutMs` **as context size grows**"。判据：**扩大上下文而不上调超时预算 = 静默截断**；上下文量与超时是一对，不能只动一个。
- **★"渴望度"是与上下文量正交的第二个旋钮**：`promptStyle` 六档（`strict` / `balanced` / `contextual` / `recall-heavy` / `precision-heavy` / `preference-only`）控制子代理"多想返回记忆"，与它看到多少上下文无关。判据：**"能不能找到"与"多想找"是两个变量**，必须分开配置；与 §诚实无匹配 分工：那条管"空结果要直说"，本条管"渴望度本身要可配"。
- 判非：白名单只收具体工具名、通配与核心工具被静默过滤（与「静默忽略」类条目同向）；Cerebras 等速度推荐与 LanceDB / Lossless Claw 接线细节（平台登记项，不迁移）。
- 提升层：模型 / 工作流。触发词：分层召回、escalate 模式、扁平检索弱于时序、queryMode、timeoutMs 联动、promptStyle 渴望度。

## r383B · 契约三态分责与弃权样本剔除（来源：docs.openclaw.ai automation/hooks、arXiv 2606.29914，2026-10-02 r379-Q-A / r375-Q-C 实拉；经 Qoder 提名）
- 契约三态分责：显式否认（"no general handler timeout / cancellation / retry / exactly-once guarantee"）= 作者自建义务；沉默未提 = 未验证须实测；已承诺 = 可依赖。
- 弃权类样本（question_id 含 `_abs`，指向不存在事件）必须从检索指标分母整体剔除并写明理由，但答题侧仍用「拒绝作答」判据单评；两套口径分开命名（recall_all@5 / ndcg_any@10 等）。

## r383C · 发现过滤器 ≠ 授权（来源：activepieces ai-metadata.md，2026-10-02 r380-Q-B 实拉；经 Qoder 提名）
- `audience` "is a discovery filter, not a permission"：两类字段分面记账，同契约内 trigger 无该字段 ⇒ 判据不可跨资产类型复用；发现可见 ≠ 调用被授权，机检须分别验证。

## 能力面是 resource:action 二维矩阵；正反动作与「开关权/查看权」各占独立开关位（来源：docs.n8n.io `.../create-custom-project-roles.md` 11,109B，2026-10-03 r388A 独立实拉）
- **原文**：scope 形如 `workflow:create/read/update/execute/publish/delete/move`、`credential:share/unshare`、`workflow:enableRedaction`、`workflow:disableRedaction`、`execution:reveal`，并区分 instance 轴与 project 轴两套角色。
- **判据**：① **授权粒度是资源维 × 动作维的矩阵**——只声明一维等于该维整列放行（「给 workflow」不说动作 = 全动作），技能暴露能力时必须二维都写清。② **正反动作必须各占一个独立开关位**：`enableRedaction` 与 `disableRedaction` 是两个 scope，`publish` 也不等于 `unpublish`；把「能开」当成「能开关」会多放出一半能力。③ **开关权 ≠ 查看权**：能关脱敏（`disableRedaction`）不等于能看明文（`execution:reveal`），两者互不包含；设计技能能力清单时把「改变状态」与「读取被保护内容」拆成两个位。
- 提升层：工具 / 可复用 Skill。触发词：scope 矩阵、resource:action、正反动作独立开关、开关权≠查看权、实例轴与项目轴。

## 密钥的输入通道本身就是泄漏面；凭据分类是持久属性，自动推断只在首次生效（来源：docs.openclaw.ai/cli/secrets.md 16,115B，2026-10-03 r388C 独立实拉）
- **原文**：「For `secret` values, `--value` is refused with exit code `2` because command-line arguments can leak through shell history and process listings.」「Pipe stdin when stdin is not a TTY. Pass `--value-file <path>`... Run interactively and enter the value in the no-echo prompt.」「`set` and `import` preserve the entry's current kind when saving, including protection changes made while input or confirmation is pending. Only new names use automatic detection.」「Known redaction placeholders such as `__OPENCLAW_REDACTED__` cannot be stored as values.」「`store list` shows allowed hosts because they are **policy metadata, not secret material**.」
- **判据**：① **传密的通道决定泄漏面，不只是存密的介质**——命令行参数会落进 shell 历史与进程列表，所以 secret 类只认 stdin 管道 / 值文件 / 交互式掩码三种通道；写文档与示例时"顺手写个 --value"就是把凭据送进历史文件。② **分类是写入即固定的属性，不随后续推断漂移**——已有条目保持原 kind（哪怕名称后缀看起来像 env），自动推断只对**新名**生效；否则一次批量导入会把已经收紧的条目重新降级成 env。③ **脱敏占位符不得回写成值**——占位符被当成真实值存进去，事后无法与"真的配了这个字符串"区分；无可用旧值时直接拒绝。④ **白名单是策略元数据，可以公开列出**——允许外发的主机不是秘密，列出来才能审；把策略面当秘密藏起来，等于放弃对出口面的审计。
- 提升层：工具 / 安全边界。触发词：--value 泄漏面、shell history、stdin 管道、值文件、分类持久属性、自动推断只对新名、占位符不得回写、白名单是策略元数据。


## 能力声明必须自带前置面与受限面：能用 ≠ 被允许在生产用（来源：docs.n8n.io `administer/manage-credentials/end-user-credentials.md` 9,720B，2026-10-03 r390A 独立 curl 取 `.md` 原文实拉；与 §SecretRef 禁 OAuth 等规范条款互补——那几条管规范合规面，本条管能力可用性的声明面）
- **原文**：特性可用性「**n8n Cloud:** Enterprise / **Self-hosted:** Enterprise」；「End-user credentials are in **Preview** and may change in future releases. **Don't rely on them in production workflows.**」；「**OAuth credentials only**」；「You can only create end-user credentials in **team projects**, not in personal projects」；「**One connection per user**: Each user can connect a single account per end-user credential template.」；「By default, only project admins can create end-user credentials.」
- **判据**：① 技能/能力描述里除了"做什么"，必须写**前置面四件套**：套餐或版本门槛 · 支持的凭据/协议类型 · 可创建的作用域 · 每主体配额（一人一条）。缺任何一项，"配了不生效"的排障成本都会转嫁给使用者。② **预览态必须在声明里写死"不得依赖其跑生产"**——"能用"与"被允许在生产用"是两个结论，官方自己就分开写。③ **能力默认只对高权限角色开放，收窄靠显式授权而不是默认放开**：默认只有 project admin 能建，其他角色通过自定义角色授予。凡"谁能创建"这类元能力，默认方向应是收窄。
- 提升层：可复用 Skill / 工具。触发词：前置面、套餐门槛、预览态禁生产、OAuth only、配额一人一条、元能力默认收窄。


## 能力面按组声明时，组名是展开式简写且自带排除清单；能力缺失应当是「隐藏」而不是「回落到更宽的面」；沙箱里的技能是投影不是本体（来源：docs.openclaw.ai `gateway/sandbox-vs-tool-policy-vs-elevated.md` 9,792B + `gateway/sandboxing/what-gets-sandboxed.md` 1,573B + `gateway/sandboxing/workspace-access.md` 7,119B，2026-10-03 r391A 独立 curl 取 `.md` 原文实拉；与 §能力面是 resource:action 二维矩阵 / §能力前置面四件套 互补——那两条管声明维度与门槛，本条管简写展开、缺失降级与运行期投影）
- **原文**：工具组「Tool policies (global, agent, sandbox) support `group:*` entries that **expand to multiple tools**」，`group:fs` = `read`/`write`/`edit`/`apply_patch`，`group:runtime` = `exec`/`process`/`code_execution`；「`group:openclaw`: most built-in OpenClaw tools (**excludes** the `read`/`write`/`edit`/`apply_patch`/`exec`/`process` fs and runtime primitives, `canvas`, and provider plugins)」；只读要求「For **read-only agents, deny `group:runtime`** as well as mutating filesystem tools unless sandbox filesystem policy or a separate host boundary enforces the read-only constraint.」；缺失即隐藏「Directory discovery uses `ls` **without granting shell execution** … Custom backends can provide `SandboxFsBridge.readDirectory(...)`. The method is **optional** for older plugins: **`ls` is hidden when it is absent, and OpenClaw does not fall back to reading the host filesystem.**」；技能投影「With `workspaceAccess: "none"`, OpenClaw **mirrors eligible skills into the sandbox workspace** (`.../skills`) as **read-only instruction roots** … The **runtime-owned `.openclaw/sandbox-skills` subtree is excluded from workspace reconciliation and publication**; other project content under `.openclaw` is retained … The **Gateway refreshes its own mirrored copies** even when an earlier copy inherited read-only directory permissions.」
- **判据**：① **组名必须当作"展开式宏"写进文档，且要写出排除项**：`group:*` 会展开成一串具体工具（fs 组四个、runtime 组三个），而 `group:openclaw` 这种"大多数"式命名**显式排除** fs/runtime 原语、canvas 与 provider 插件。⇒ 描述能力面时只写组名不写展开结果，使用者无法判断某个具体工具在不在里面；写"组 X 覆盖全部"这种话基本都是错的。② **"只读"必须落到运行时组**：只 deny 文件类工具而留着 `exec`，只读是假的。官方给的是"deny `group:runtime` **以及** 变更类文件工具"，除非另有沙箱文件策略或宿主边界兜底。⇒ 只读类技能的验收动作是：试着用 shell 写一次文件，不是检查有没有 write 工具。③ **能力缺失应表现为隐藏，绝不回落到更宽的面**：自定义后端没有 `readDirectory` 就把 `ls` 藏起来，**不回落到读宿主文件系统**。⇒ 这是降级方向的标准答案——能力不足时收敛，而不是为了功能可用去开一个更大的口子（与 fail-closed 同源）。④ **运行期拿到的技能是投影，改动不回流到本体**：沙箱里技能以只读指令根镜像存在，`.openclaw/sandbox-skills` 子树被排除在工作区对账与发布之外，镜像由 Gateway 自行刷新（连之前继承的只读权限都不用手工修）。⇒ 在受控环境里"改了技能"默认是改的副本；声明时必须说清这是投影、哪些路径不会回流。
- 提升层：工具 / 可复用 Skill。触发词：group 展开、group:openclaw 排除项、只读要 deny runtime、能力缺失隐藏不回落、sandbox-skills 排除对账、技能镜像只读、投影不回流。


## 声明能力必须分「可提升」与「不可提升」两类限额；把内容交给第三方模型时，外发清单必须同时写「发什么」与「不发什么」（来源：pipedream.com/docs `workflows/limits.md` 9,083B + `workflows/building-workflows/errors.md` 9,150B，2026-10-03 r391B 独立 curl 取 `.md` 原文实拉；与 §能力前置面四件套 / §能力面是 resource:action 矩阵 互补——那两条管门槛与维度，本条管资源上限的可协商性与外发数据的负声明）
- **原文**：可提升项「By default, workflows run with **256MB** of memory. You can modify a workflow's memory … up to **10GB**. **Increasing your workflow's memory gives you a proportional increase in CPU.** … Pipedream **charges credits proportional to your memory configuration**.」；超时按触发类型分档「HTTP and Email-triggered workflows default to **30 seconds** … Cron-triggered workflows default to **60 seconds** … | Free tiers | 300 seconds | | Paid tiers | 750 seconds |」；不可提升项「You have access to **2GB** of disk in the `/tmp` directory. **This limit cannot be raised.**」；「logs … step exports … and the original event data … cannot exceed a combined size of **6MB** … **This limit cannot be raised.**」；外发清单「When you debug an error with AI, Pipedream sends the following information to OpenAI: The **error code, message, and stack trace** · The **step's code** · The **input added to the step configuration**. This **does not** contain the event data that triggered your workflow … We explicitly **do not** send the event data that triggered the error, or any other information about your account or workflow.」
- **判据**：① **资源上限必须拆成"能靠配置/加钱解决"与"不能解决"两类**：内存 256MB→10GB 可调（且 CPU 同比例提升、按内存计费）属于前者；`/tmp` 2GB 与"日志 + step exports + 原始事件合计 6MB"**明确不可提升**属于后者。⇒ 架构决策的分水岭就在这里：撞到可提升项可以调参，撞到不可提升项必须改设计；把两类混在一张"限制"表里，读的人会以为都能调。② **同一能力的不同触发方式限额不同**：HTTP/邮件触发默认 30 秒、Cron 触发默认 60 秒，套餐再决定上限（300s / 750s）。⇒ 写"超时 30 秒"不说触发类型，与写"超时上限"不说套餐，都是不完整的声明。③ **内存这类"性能旋钮"同时是计费旋钮**：调内存等价于调 CPU 与费用 ⇒ 资源声明要连成本一起写，否则使用者会把"加大内存"当成免费的提速手段。④ **把数据交给第三方模型（哪怕只是"AI 帮我看这个报错"）是外发通道，声明必须双侧**：官方写法是逐项列出发送内容（错误码/消息/栈、步骤代码、步骤静态输入），并**显式列出不发送的内容**（触发事件数据、账号与工作流信息）。⇒ 只有"发什么"没有"不发什么"的声明无法证伪，也无法作为验收依据；负声明与正声明同等重要。
- 提升层：可复用 Skill / 工具。触发词：可提升 vs 不可提升限额、内存调 CPU 与计费、2GB tmp 不可提升、6MB 日志合计、超时按触发类型、Debug with AI 外发清单、不发触发事件数据、负声明。


## 托管额度是「按节点」的凭据选择，便利性换的是覆盖面；能力切换时隐藏与警告两种处理取决于当前状态（来源：docs.n8n.io `build/understand-workflows/use-gateway-credits.md` 6,208B，2026-10-03 r391C 独立 curl 取 `.md` 原文实拉；与 §能力前置面四件套 / §可提升与不可提升限额 互补——那两条管门槛与资源上限，本条管凭据粒度、覆盖面差集与切换行为）
- **原文**：「n8n routes the requests through its own gateway and bills the usage from your instance's **prepaid credit balance**」；「**You choose per node**, so one workflow can mix Gateway credits on one node with your own credentials on another.」；「Some nodes support Gateway credits for **part of what they do**. When you use Gateway credits on such a node, n8n **hides the unsupported operations**. If a node **already has an unsupported operation selected** when you switch it to Gateway credits, n8n **keeps the operation and shows a warning** instead.」；「Nodes using Gateway credits **fail when your instance's balance reaches zero**.」；「Instance owners can turn Gateway credits **off for everyone on the instance** … When it's off, the Gateway credits option **doesn't appear on nodes for anyone**.」；对比表「| Coverage | **Supported services and models only** | Any service or model n8n integrates with, **including your own plan's rate limits and features** |」；「| Spend visibility | One spend view by model and workflow in n8n | **Each provider's own dashboard** |」；可用面「**They aren't available on n8n Cloud Enterprise or self-hosted n8n.** Gateway credits are available from n8n **2.36.0**. Free trials include Gateway credits, but **you can't top up until you upgrade to a paid plan**.」
- **判据**：① **托管凭据的粒度要声明到哪一级**：这里是**按节点**选择（同一工作流可以一部分节点走托管额度、另一部分走自己的 key），不是按工作流、也不是按实例。⇒ 粒度决定了"能不能混用"与"故障半径"：粒度越细，切换成本与爆炸半径越小。② **便利性的代价必须写成对比表**：托管额度只覆盖受支持的服务与模型（并可能只支持某节点的部分操作），自带 key 覆盖全部且能享受自己套餐的限流与特性；代价的另一面是**消费可见性集中**（一处看按模型/工作流）vs **分散在各 provider 自己的面板**。⇒ 只写"免配 key 即可调用"而不写覆盖面差集，使用者会在第一次遇到不支持的操作时才发现。③ **能力切换对"已选中"与"未选中"的状态处理不同**：不支持的操作在未选中时被**隐藏**，在已选中时被**保留并给出警告**。⇒ 这是适配层的正确姿势——不能因为切了模式就让已有配置凭空消失；验收时要分别测这两种状态，只测一种会漏掉一半行为。④ **共享额度的失败模式是硬失败且开关是全局的**：余额归零直接让相关节点失败（不是降级到自带凭据），实例 owner 可以整体关掉，关掉后**所有人的节点上都不再出现该选项**。⇒ 依赖共享额度的流程必须有"余额不足"这条失败分支，且要清楚关停开关不在自己手里。⑤ **可用面同时受部署形态、版本与套餐三重限制**：Cloud Enterprise 与自托管不可用、需 ≥2.36.0、免费试用含额度但**升级付费前不能充值**。⇒ 这类"能用但可能随时用不了"的能力，前置面要一次写全三个维度，缺一维就会在验收时才发现走不通。
- 提升层：工具 / 可复用 Skill。触发词：按节点选凭据、托管额度 vs 自带 key、覆盖面差集、部分操作支持、隐藏 vs 保留并警告、余额归零硬失败、owner 全局关停、2.36.0 起、试用不可充值。

## 文档必须自陈「代码才是真源」并给出取真源的通道；展示层元数据不是语义（来源：docs.openclaw.ai/gateway/configuration-reference.md 10,087B + www.activepieces.com/docs/admin-guide/security/audit-logs/overview.md 4,198B，2026-10-03 r393A 独立 curl 取 `.md` 原文实拉；与 §规范声明 vs 自身实现 互补——那条管规范有没有实现自己声明的门禁，本条管文档有没有声明自己不是权威并给出校验手段）

- openclaw 配置参考页正文第一句就是 "Code truth beats this page"，并给三条取真源手段：① `openclaw config schema` 打印运行时合并后的 JSON Schema（含 bundled/plugin/channel 元数据）；② agent 改配置前用 gateway 工具 `config.schema.lookup` 取**该路径**的精确 schema 节点，而不是读整份文档；③ `pnpm config:docs:check` 用基线 hash 校验文档与当前 schema 表面是否漂移 ⇒ **文档与实现的漂移要能机检，不能靠人 review**。
- Activepieces 审计事件目录同样自陈：目录随平台增长补，**每个事件的真源是代码里的 event schema**（直接给出文件路径）⇒ 清单类文档必须写明"可能不全"并指向代码真源，否则读者会拿清单当全集。
- 配置格式本身也是契约：JSON5（允许注释与尾逗号）、所有字段可选、省略即取安全默认 ⇒ 默认值的语义要写出来，不能让读者猜"不写会怎样"。
- 分层元数据是展示性的：`uiHints.advanced` 只决定控制界面是否折叠，**不影响语义**；没声明祖先的路径默认 advanced ⇒ 不要把"是否高级"当成"是否生效"来读。

## 配置歧义必须 fail-fast 而不是挑一个默认值；危险模式可以存在但不能进入引导；能力天花板要覆盖排队工作与子执行体（来源：docs.openclaw.ai `gateway/config-gateway.md` 36,884B，2026-10-03 r393B 独立 curl 取 `.md` 原文实拉；与 §能力前置面四件套 / §可提升与不可提升限额 互补——那两条管门槛与资源上限，本条管配置本身的自洽性与天花板的覆盖范围）

- 歧义配置要 fail-fast：`auth.token` 与 `auth.password` 同时配置而 `mode` 未显式设置时，**启动与 service install/repair 直接失败**——不是挑一个、不是告警继续。⇒ 两个互斥入口同时存在时，要么显式指定，要么拒绝启动。
- 危险模式可以存在但要从引导里摘掉：`auth.mode: "none"` 是显式无鉴权模式，原文限定"仅用于可信的本机回环场景"，且**引导流程故意不提供这个选项** ⇒ 提供能力与推荐使用是两件事，声明里要分开写。
- 能力天花板的作用域要写到"非直接请求"：角色的 `modelPolicy` 对**该角色的请求、排队中的工作、以及它的子执行体**全部生效（`sourceAgent` / `allow` / `deny` 决定解析来源）⇒ 天花板只覆盖直接调用的话，绕过方式就是把活排进队列或派生子任务。
- 角色定义是复合对象而不是一个权限串：会话权（`sessions.others` 四档 none/view/suggest/write）、可创建的 agent 白名单、闭合的 `scopes` 天花板、可选的外挂访问策略插件、模型天花板——少写一项等于那一项没有上限。

## 配置校验要分「默认值侧静默忽略」与「显式值侧直接失败」两档；关掉宣告不等于关掉通知；写在某页的键不一定归这一页管（来源：docs.openclaw.ai `gateway/config-hooks.md` 36,853B，2026-10-03 r393C 独立 curl 取 `.md` 原文实拉；与 §配置歧义必须 fail-fast 互补——那条管两个互斥入口同时存在时拒绝启动，本条管同一个不合法值因为来源不同而处置不同）

- 同一类"不合法"，来源不同处置不同：不被允许的**默认**模型被静默忽略；**显式**指定的无效模型则导致准备失败；`timeoutSeconds` 的无效值/非正值被忽略 ⇒ 声明里必须分开写"默认值不合法怎么办"与"显式值不合法怎么办"，否则用户以为没生效其实是没报错。
- `deliver` 只有 `false` 才算退出投递；关掉宣告**不等于**关掉通知——成功完成只写日志不宣告，但**非 ok 的执行结果仍然产生状态事件** ⇒ "静默"这个词的覆盖范围要写清：静默的是哪一类。
- 配置键的归属要写在键上：`internal` 属于另一个子系统，**不启用 HTTP 入口** ⇒ 出现在同一页文档里的键不一定由这一页的机制管，写声明时要标归谁管，否则读者会以为配了就生效。
- `idempotencyKey` 是可选重放键且**请求头优先于载荷**；`waitForCompletion` 只对直接 `/agent` 调用生效，经 mapping 与 fan-out 提交永远只做准入 ⇒ 同一字段的生效入口要列全，别让调用方以为处处可用。


## 外部解析器/命令的准入校验是一条有先后顺序的链；`${VAR:-fallback}` 是配置文本不是密钥库且带 fallback 永不告警；`$include` 合并语义与写回边界要逐条声明；拆分文档必须保留旧锚点（来源：docs.openclaw.ai `gateway/config-secrets-env.md` 10,309B + `gateway/config-tools.md` 7,517B 索引页 + `gateway/config-tools/github-identity.md` 17,020B，2026-10-03 r395A 独立 curl 取 `.md` 原文实拉）

- **外部命令/解析器准入链有先后顺序**：exec 型 secret provider 必须绝对路径；**符号链接命令路径直接拒**（先于目录白名单检查）；必须非 group/world 可写、POSIX 下属主为当前用户；若配了 `trustedDirs`，约束的是「配置里写的那个路径本身」，因为符号链接在这一步之前已被拒 ⇒ 声明准入规则时必须把顺序写出来，否则「配了白名单目录」会被误当成能穿透软链。
- **最小环境是默认，变量须显式传递**：exec 子进程环境默认最小，需要的变量要用 `passEnv` 逐项列出 ⇒ 「为什么子进程里拿不到这个变量」的默认答案是「没传」，不是「环境有问题」。
- **校验不可用时 fail-closed 且不提供旁路**：file 与 exec provider 在 Windows ACL 校验不可用时直接失败关闭，官方明确**没有 provider 级 bypass** ⇒ 凡是「检查不了就放行」的降级口，都要当成设计缺陷处理。
- **ID 校验按 source 分族且自带遍历防护**：`env` 要求 `^[A-Z][A-Z0-9_]{0,127}$`；`file` 的 id 是绝对 JSON pointer；`exec` 支持 `secret#json_key` 选择器但**禁止 `.` / `..` 路径段**（`a/../b` 被拒）⇒ 每种来源的 id 是不同语法族，统一用一个正则既会误拒也会漏防。
- **`${VAR:-fallback}` 是配置文本，不是密钥库**：官方明确 fallback 是 config text，凭据必须放 `env.vars` 或 SecretRef 并裸引用；**带 fallback 的引用总能解析，因此永不发出缺失告警** ⇒ 这既是便利也是静默降级面：写声明时要说清「哪些情况不再告警」。其余 shell 操作符（`:=` `:?` `:+` 等）一律按字面量处理，只有 `:-` 被支持；`$${VAR}` 是转义。
- **回写要保留书写形态而不是内联解析值**：配置回写时恢复 `${VAR:-fallback}` 原文，而不是把它解析出的值固化进文件；未解析的变量保持「可见地未解析」并发告警，对需要取值的消费者不可用 ⇒ 「配置里看到什么」与「运行时拿到什么」的差异必须可辨识。
- **`$include` 合并语义四条**：单文件 include **替换**所在对象；数组按序**深合并**（后者覆盖前者）；**兄弟键在 include 之后合并**（覆盖 include 里的值）；嵌套最深 10 层。路径必须留在顶级配置目录内，越界要靠 `OPENCLAW_INCLUDE_ROOTS` 显式扩根 ⇒ 「哪种 include 覆盖哪种」要逐条写，一句「支持 include」完全不够。
- **写回边界：所有权不单一就 fail-closed，绝不扁平化**：只有「全部变更键都归某一个单文件 include 所有」时才写穿到最深的那个拥有者；根级 include、数组项 include、include 数组、跨所有权边界的改动等一律**只读**，写入 fail-closed 而不是把配置拍平。`doctor --fix` 一次运行中若混合了根拥有与 include 拥有的修复，则**整批拒绝**，且被拒的那次写入保持所有文件不变（同批次更早的写入保留）⇒ 批量修复要么全改要么全不改，粒度必须写清。
- **拆分/迁移文档要保留旧锚点**：索引页明确「本页曾经发布的每个标题都保留锚点，旧链接仍然可解析」，并给出「每个章节搬到哪去了」的映射表 ⇒ 文档重构时保留锚点与迁移映射是硬要求，只留一个新目录等于把所有外部引用打断。


## 白名单的三种「空态」语义可能两两相反且删条目会回落默认；沙箱态是独立于用户配置的一层 clamp；写一个 URL 等于放行一个 origin；能力声明默认从严且不得从别处复制；跨端点 schema 兼容层必须声明丢什么（来源：docs.openclaw.ai `gateway/config-tools/sessions-and-subagents.md` 9,632B + `gateway/config-tools/custom-providers.md` 13,129B，2026-10-03 r395B 独立 curl 取 `.md` 原文实拉）

- **白名单要区分三种空态**：`allow` 字段**省略**或**空数组**都被当作 unset ⇒ 在默认开启的跨 agent 访问下等于**所有主体互访**；而**只含空白条目的列表**则**拒绝全部跨主体调用** ⇒ 「空」在这里不是一种状态而是两种相反状态，声明里必须逐态写，含糊一句「支持白名单」会把收紧写成放开。
- **删除主体会改写策略，甚至回落默认**：删除某个 agent 会把它的 id 从 allow 里剪掉，**剪空之后策略回落 allow-all** ⇒ 凡「按 id 列举」的策略，都要在删除操作后复查列表是否被剪空；这是个不需要改动配置就发生的策略变更。
- **沙箱态是配置之上的独立 clamp**：当前会话处于沙箱且 `sessionToolsVisibility="spawned"`（默认值）时，可见范围被限制在 spawned 会话，**即使调用方是主会话、即使显式配置为 `all`** ⇒ 声明能力天花板时要写出「哪些环境态会覆盖用户配置」，否则用户以为自己配宽了其实没生效。
- **收窄作用域要写清例外**：收窄到 `agent`/`tree`/`self` 会阻断普通跨主体访问，但 `tree` **仍允许**请求者自己派生的原生/ACP 子会话跨主体边界，而 `agent` **不含**这个例外 ⇒ 同一类「收窄」里两个档位的例外不同，按名字望文生义会选错。
- **写一个字段等于开一个信任口**：配置自定义 provider 的 `baseUrl` 本身就是网络信任决策——该精确 `scheme://host:port` origin 会被放入受管 fetch 白名单，**没有第二个开关**；而 metadata / link-local / NAT64（`64:ff9b:1::/48`）三类 origin **始终拦截**，需显式 opt-in ⇒ 声明里必须点名「配这个字段顺带授予了什么」，以及固定拒绝的例外清单。
- **能力声明默认从严，且只认有契约证据的路由**：`supportsInstructions` 仅对 native OpenAI 与 xAI 主路由这两条「有确认契约证据」的路由默认 `true`，**其余所有路由（含内置）默认 `false`**，需针对该端点验证后显式置位 ⇒ 默认值的正确方向是「没有证据就当不支持」，不是「先当支持」。
- **能力声明不得从别处复制**：catalog 自带的 `compat` 不要抄进配置（路由匹配时以 catalog 行为准）；`doctor --fix` 会识别并移除这类 legacy override 并报告分歧值 ⇒ 工具要能区分「用户验证过的声明」与「抄来的声明」，前者保留、后者清理。
- **跨端点 schema 兼容层是有损转换，必须声明丢什么**：`toolSchemaProfile` 的 `llamacpp` profile 会移除 `pattern` 以及值 ≥2000 的 `maxLength`；`unsupportedToolSchemaKeywords` 按名移除端点不接受的 JSON Schema 关键字；`maxTokensField` 决定发 `max_tokens` 还是 `max_completion_tokens` ⇒ 兼容层不是「翻译」而是「裁剪」，声明里要写清被裁掉的关键字。
- **合并优先级要按字段分条写，且带前提**：agent 级 `baseUrl` 非空值赢；agent 级 `apiKey` 非空值**只有在该 provider 未被 SecretRef 管理时**才赢；`contextWindow`/`maxTokens`/`contextTokens` 是「显式值存在且有效（正有限数）才赢，否则回落到隐式/生成的 catalog 值」⇒ 一句「agent 级覆盖全局」既说不清前提也说不清无效值怎么办。
- **显式目录不限制发现**：merge 模式下手写的 catalog 行**不会**收窄该 provider 的自动发现范围，要限制得用策略白名单或 `models.mode: "replace"` ⇒ 「我配了清单」不等于「只有这些能用」。


## 放行与拒绝谁赢必须显式排序，且跨厂方向相反；默认封禁项的启用方式是清空列表；只校验首跳会被重定向与 DNS 重绑定绕过；能力要有版本门槛（来源：docs.n8n.io `security/enable-ssrf-protection.md` 3,822B + `security/block-specific-nodes.md` 2,425B + `basic-configuration/use-environment-variables/ssrf-protection.md` 7,039B + pipedream.com/docs `conduit/configure/access-control.md` 13,330B + `conduit/configure/scim.md` 9,789B，2026-10-03 r395C 独立 curl 取 `.md` 原文实拉；n8n 与 Pipedream 均经各自 `llms.txt`（287,049B / 34,240B）定位）

- **白/黑名单的优先级必须写出顺序，因为各系统方向相反**：n8n SSRF 的优先级是 **hostname 允许 > IP 允许 > IP 拒绝**——即「更具体的放行赢过更粗的拒绝」，且官方警告 hostname 允许会**绕过 IP 拒绝检查**，所以只允许放行你可控的内部 DNS 区；而 openclaw 的工具策略是 **deny 恒赢**（`deny` 压过 `allow`）⇒ 同一句「配了白名单」在两个系统里含义相反，声明里不写谁赢就等于没写。
- **校验要覆盖整条请求链，不是首跳**：n8n 在启用 SSRF 保护后会校验「重定向目标」与「DNS 解析」，目的明确写着防 DNS rebinding 这类绕过 ⇒ 只校验用户提交的第一个 URL 等于敞开门，验收要跑到重定向之后。
- **默认封禁项的启用方式是「清空列表」，与允许类列表的空态相反**：部分节点（如 Execute Command、Read/Write Files from Disk）默认就在排除列表里，要启用得显式写成 `NODES_EXCLUDE: "[]"` ⇒ 「空数组」在排除类列表里是**全部启用**，在允许类列表里常常是**全部拒绝**（见 §白名单三种空态），同一个字面值语义相反，必须按列表类型分别声明。
- **被封禁的能力是「消失」不是「报错」**：被排除的节点用户**既搜不到也用不了**，不产生可诊断的错误 ⇒ 凡「能力不可用」，先分清是权限拒绝（有错误）还是能力摘除（无痕迹），两者的排查路径完全不同。
- **能力要标版本门槛**：SSRF 保护「自 n8n 2.12.0 起可用」⇒ 前置面除了套餐与作用域，还要含**最低版本**；把版本门槛写进能力声明，能避免「按文档配了却不生效」这类排查。


## 能力重命名必须保留旧标识符在策略清单中的映射；截断上限存在主从；同族配置的作用域粒度逐键不同；回退链让单点失败静默（来源：docs.openclaw.ai `gateway/config-tools/built-in-tools.md` 6,725B（经 `llms.txt` 210,790B 定位真路径，旧猜路径 `config-tools/built-in-tools` 与 `tools/built-in-tools` 均 404），2026-10-03 r396A 独立 curl 取 `.md` 原文实拉）

- **重命名是策略面事件，判定面是「既有 allow/deny 还命中吗」**：`update_plan` 改名为 `progress_card` 后，官方明确**已发布的 allow/deny 策略里写旧名的条目会映射到新名，语义保持不变** ⇒ 改名的验收不是「新名能用」，而是「别人已经写出去的策略条目是否仍然生效」；没有这层映射，一次改名会让所有既有策略静默失效。
- **截断类上限有主从，只改子项等于没改**：`maxChars` 会被 `maxCharsCap` 夹住（要更大的正文必须先抬 cap），`maxResponseBytes` 自带 32000–10000000 的 clamp 区间 ⇒ 凡「上限之上还有上限」，声明要写出主从不说清就是无效配置；区间边界要写成可见数字，否则「配了不生效」无法自证。
- **同一配置族内不同键的作用域粒度不同，必须逐键声明**：`loopDetection` 既可在 `tools.loopDetection` 全局定义、又能在 `agents.entries.*.tools.loopDetection` 按 agent 覆盖；而 `updatePlan` **只有全局一个开关，且不存在按模型自动启用的规则** ⇒ 不能因为「同一个族里某个键支持 per-agent」就推断其他键也支持；作用域粒度是键级属性，不是族级属性。
- **默认回退链让单点失败静默**：媒体理解按 `capabilities` 匹配候选模型，**失败即回退到下一条目** ⇒ 「任务成功」不能证明是预期那个候选在服务，验收必须读出**实际生效的条目**；同理 `provider` 省略时的 auto-detect 意味着「用的是谁」本身就是运行期决定的，声明里要写明解析顺序。
- **判不落**：`applyPatch.allowModels` 空/unset = 任何兼容模型可用（与 §白名单三种空态语义 同族，重叠 >60%，仅作跨厂印证）；loopDetection 默认关闭（与 §能力声明默认从严 同族）；文档标注「除某几项外展示值即默认值」（与 wb-debug-loop §文档示例值≠内建默认 同族）。


## 隐式便利清单与显式清单是两套且信任不可跨源迁移；能力面与授权面是两道门；会话级覆盖不在全局查看通道里（来源：docs.openclaw.ai `tools/exec-approvals.md` 39,387B + www.activepieces.com/docs `admin-guide/guides/event-streaming.md` 4,911B，2026-10-03 r396B 独立 curl 取 `.md` 原文实拉）

- **隐式便利清单必须能被显式关掉，且信任不跨源**：`autoAllowSkills` 会把已知技能引用的可执行文件当作已允许，官方标注它是**独立的隐式便利清单，与手写的路径允许清单分开**；信任归属于**提供它的那个 Gateway**——切换 Gateway 会作废缓存（含仍在途的批准检查），刷新失败可保留**同一 Gateway** 的上次信任，但**不能导入另一个 Gateway 的信任** ⇒ 便利项与严格项是两套机制，要严格就必须能显式关掉便利项；信任有来源归属，换源即失效且不可迁移。
- **能力面与授权面是两道独立的门**：`messaging` 工具档可以在批准允许命令的情况下仍然排除 `exec`/`process`；官方给出判词——**包含不保证能执行，缺失也不证明被禁用**，要确认得真的跑一次 ⇒ 「工具在清单里」与「这次能不能调用」是两条门，验收不能拿清单替代执行。
- **同一策略的查看通道是分层的**：`approvals get` / `exec-policy show` 给出的是请求策略、宿主策略来源与生效结果，**不含会话级 `/exec` 覆盖**，要看会话态必须进到那个会话里查 ⇒ 「我查过了」可能只查了其中一层；声明生效面时要写明查看通道覆盖到哪一层。
- **审计转发的成败由消费方决定，且内外两条路径的网络前提相反**：事件流目的地要求外部端点为 HTTPS、从 Activepieces 服务器可达、并**返回 2xx 否则事件不被接收**；而**同实例上的 handler flow 走内部投递，即使实例不出公网也能送达** ⇒ 「配好了目的地」不等于「收到了事件」，投递类能力的验收必须真的收一条；同一能力的网络前提会按部署位置分叉，声明要分内外写。


## 安全判定面必须排除可被探测的副作用；排除项要给「为什么」；判定形状必须等于执行形状；最终能力面来自四条独立来源；自动脚手架产的是最宽松形态（来源：docs.openclaw.ai `tools/exec-approvals-advanced.md` 27,837B + `gateway/config-tools/tool-policy.md` 18,865B，2026-10-03 r396C 独立 curl 取 `.md` 原文实拉）

- **判定只吃 argv 形状，刻意不做文件系统存在性检查**：safe-bin 的校验是**仅从参数形状确定性判定**，官方写明这样设计是为了**避免 allow/deny 的差异变成文件存在性 oracle** ⇒ 安全判定不能引入「能被调用方观测到的副作用」，否则判定结果本身就成了探测通道；判定面要当纯函数来设计。
- **排除清单要写理由，且判据是「能不能被限定住」**：`awk`/`sed`/`jq` 被**永久禁止**作为 safe bin，理由是**语义无法验证为 stdin-only**（`jq` 能读环境数据、能从模块或启动文件加载代码）⇒ 排除一个能力，判断标准不是「它危不危险」而是「它的行为能不能被限定在我允许的子集内」；理由要写出来，否则下游无法判断这条排除还成不成立。
- **判定通过的形状必须与执行时的形状一致**：safe bins 在执行时把 argv token 当**字面文本**（不做 glob 展开、不做 `$VAR` 替换），并要求 `grep` 的模式必须用 `-e/--regexp` 给出、位置形式直接拒绝 ⇒ 凡是「按形状审批、按原样执行」的机制，必须消灭形状与执行之间的再解释层，否则 `*`、`$HOME/...` 就是走私文件读取的通道。
- **最终能力面有四条独立来源，只报 profile 等于没报**：工具来自 profile（`minimal`/`coding`/`messaging`/`full`）、`tools.alsoAllow` 补充、`tools.byProvider` 按提供方、`tools.toolsBySender` 按发送者 ⇒ 「我给它配了 coding 档」说明不了它最终能用什么；能力清单的取值要按来源逐条合并后再声明。
- **自动脚手架产的是最宽松形态，且对高危类不生成**：`doctor --fix` 只会把缺失的自定义 `safeBinProfiles.<bin>` 补成 `{}`（空配置，需人工收紧），而**解释器/运行时类不自动 scaffold**；`security audit` 对「safeBins 里出现无 profile 的解释器」给专用告警码 `tools.exec.safe_bins_interpreter_unprofiled` ⇒ 「跑过自动修复」不等于「已收紧」，修复产物要当成待人工收紧的草稿，且修复范围本身有排除名单。
- **判不落**：`Full` 档只选工具不授予执行权限（与 §能力面与授权面是两道门 同族，仅作例证）；`group:openclaw` 以排除方式定义（与 §group:* 展开式简写自带排除清单 重叠 >60%）；`silent` 之外各日志级别与具体数值（登记项）。
- **声明的权限可能依赖另一个独立开关才激活，列出≠生效**：n8n 项目角色矩阵里 `Use external secrets in credentials` 虽勾 ✅，但需 instance owner/admin 先在实例设置开启 `Enable external secrets for project roles` 才真正可用（n8n 2.13.0+）⇒ 能力面声明要把「权限依赖的上级开关激活态」标出来，否则「列表里有」被误读成「已经能用」；覆盖声明还须写清哪些资源类型根本不在该 RBAC 覆盖内（n8n 的 Variables / Tags 是实例级全局共享、不受项目 RBAC 约束，属「覆盖面声明要写不覆盖什么」的实例）。
- **权限间有隐式包含链，不能只列勾选项**：n8n `Roles: Manage all roles` 自动包含 `Manage project roles`；`API keys: Manage others` 自动包含 `Manage own` ⇒ 授权声明要写出隐式包含关系，单勾一个权限实际带了另一个，验收须读出真实生效集合（与 r400-Q「覆盖开关有豁免集、未列出即最宽」互补：本条是「勾选即带附属」，那条是「未列即最宽」）。

## 工具级 HITL 授权面：agent 必须预知需批准、rejection 必须回流 AI、审批回调签名 fail-closed（来源：docs.n8n.io `build/integrate-ai/ai-examples/human-in-the-loop-for-tools.md` 9,045B + `integrations/builtin/app-nodes/n8n-nodes-base.slack/approvals.md` 8,545B，2026-10-03 r405A 独立 curl 取 `.md` 实拉；与 §能力面与授权面是两道门 / §安全判定面 argv-only 互补——那两条管清单与判定形状，本条管工具级人工闸门的 agent 侧认知与回流语义）

- **被拦截的 agent 必须自己知道哪些工具需批准**：n8n 要求系统提示显式声明 HITL 设置，否则 AI 会把 deny 当成「未知错误」而非「被拒」，导致错误重试或误判；拒绝必须**回流 AI**（deny → action canceled + AI informed），不是静默取消 ⇒ 人工闸门不只是加一道拦截，还改了 agent 的认知前提。
- **审批通道可独立于交互通道，但那只是路由不是权限源**：Chat 交互、Slack 批准是设计选项（与 ag Cap37 外发审批链接把审批权移出账号体系不同）；粒度可对单工具或全工具，按不可逆性分级。
- **审批回调必须验证来源且失败 fail-closed**：Slack 用 request signing 验证每次回调来自 Slack，验证失败则 reject + workflow keeps waiting（与 §验证通道禁副作用/出网白名单 fail-closed 同源）；链接式按钮「任何人持链接可响应、平台不知谁点」= 匿名可响应（与 §有 traceId≠可回溯 对比，可追溯性前提被破坏）。
- **判不落**：`Restrict Who Can Approve` 空列表=全频道可批准（与 ag Cap53 互证，方向3 的 IM 反模式）；agent 侧认知要求与 Cap52「可见≠授权」同源仅作 IM 印证。

## 配置来源二选一时，声明式托管必须把交互面降级为只读；可选项由请求方声明，接收方不得自造（来源：docs.n8n.io `administer/observe-and-log/stream-logs-to-external-systems.md` 23,919B + docs.openclaw.ai `tools/exec-approvals-advanced.md` 27,837B，2026-10-03 r408A 独立 curl 取 `.md` 原文实拉）
- **原文**：① `N8N_LOG_STREAMING_MANAGED_BY_ENV=true` 后 n8n **每次启动重新应用**环境变量里的目的地配置，并**把 Log Streaming 的 UI 控件锁成只读**。② 插件审批请求**可以限制可用的决策集合**，审批界面**使用请求声明的那个集合**，Gateway **拒绝提交未被提供的决策**；无控件可用的旧式 `/approve` 只在「找不到审批」时**有界**回退到另一类审批，**真实的拒绝或错误不会静默重试成另一类**。
- **判据**：① **同一份配置有两个来源时，必须让失败模式显式化**——选了声明式托管就应当把交互面变成只读，而不是两边都能改、由最后一次写入者取胜；「改了不生效」类问题先查该面是不是已被锁定。② **只读降级要连带声明重放语义**：每次启动重放意味着手工改动会在重启时消失，这不是 bug 而是托管契约，文档必须写清「重启会覆盖」。③ **合法输入集合归发起方所有**：请求方声明了可选项，接收方的越界提交应被拒绝而非被接受后纠正；把「我能提交什么」交给展示层自己决定，等于让 UI 定义协议。④ **跨类型回退必须写清触发条件**：只在「未找到」这一类失败上回退是有界的；若真实的拒绝/错误也能走同一条回退路径，一次明确的拒绝会被翻译成另一类语义，排障时看到的现象与真实原因不对应。
- **提升层**：可复用 Skill / 工具。触发词：env 托管锁 UI 只读、重启重放覆盖、决策集由请求声明、越界决策被拒、跨类型回退有界、not-found 才可回退。

## 逐项覆盖与集合默认构成三层继承；覆写键必须是服务端上报的原始名，改名即失效（来源：docs.bigmodel.cn `cn/managed-agents/permission-policies.md` 6,620B + `cn/managed-agents/skills.md` 6,574B（经 `llms.txt` 49,320B 定位），2026-10-03 r408C 独立 curl 取 `.md` 原文实拉）
- **原文**：① 内置工具集与 MCP 工具集都支持 `default_config.permission_policy`（集合默认）与 `configs[].permission_policy`（逐项）；**继承规则：`configs[]` 省略或为 null 时继承 `default_config`，后者省略时取协议默认 `always_allow`**。② MCP 工具集里 `configs[].name` **用服务器上报的原始工具名**（示例 `get_issue` / `list_issues` 配 `always_allow`，其余走集合默认 `always_ask`）。③ Skill 侧：每个自定义 Skill 的根必须有 `SKILL.md` 且 frontmatter 的 `description` 非空；**挂载每个 Skill 都会占用少量会话上下文**（用于让模型判断何时调用）；**挂载 Skill 时必须同时配置 `agent_toolset_20260601`，否则创建或更新返回 400**。
- **判据**：① **三层继承要按顺序读：逐项 → 集合默认 → 协议默认**，中间层为 null 与为"省略"等价；排查「为什么这个工具没被审批拦下」先看逐项有没有写、再看集合默认、最后才谈协议默认，跳层会把责任归错地方。② **覆写键是被管对象的自称，不是我方别名**——MCP 的工具名由服务器上报，上游改名/重命名后既有逐项配置会**静默失配**（不会报 unknown tool，只是再也不命中），工具就回到集合默认上去；凡按名字匹配的配置都要写明「以谁的名字为准」。③ **真正"允许"的全部清单 = 逐项允许 ∪ 集合默认允许**，只看逐项配置会低估放行面。④ **依赖不足应当显式报错而非降级**：缺必需工具集时新 Agent 直接 400，而不是"挂上了但技能用不了"。依赖关系要在写入侧校验，否则缺陷会推迟到运行时才以「技能没生效」的形式出现，且现场看不到原因。⑤ **挂载有上下文成本**：每个 Skill 都占一点会话预算，堆积技能会侵蚀留给任务的窗口 ⇒ 技能数量要有上限与盘点机制，不能只按"有没有用"评估。
- **提升层**：可复用 Skill / 工具。触发词：三层继承、default_config 与 configs、null 等同省略、MCP 原始工具名、名字失配静默、缺工具集 400、挂载占上下文。

## 收紧出网会让相邻能力连带失效，须逐道显式放行；白名单默认值决定未来新增成员是否自动获得权限（来源：docs.bigmodel.cn `cn/managed-agents/{cloud-environment,mcp,tools}.md` 6,579B / 6,511B / 7,371B，2026-10-04 r409A 独立 curl 取 `.md` 原文实拉；与 §两道门（能力面与授权面）/ §三层继承 互补——那两条管"包含不等于可执行"与"继承顺序"，本条管"默认收紧会连带打断相邻能力"与"默认值决定未来新增面归属"）
- **原文**：`网络策略是二选一的 tagged union`；`allow_package_managers：默认 false。limited 环境声明了 packages 时必须显式设为 true，否则返回 400`；`allow_mcp_servers：默认 false。是否放行 Remote MCP 服务器的出网连接`；`unrestricted 模式下不得携带 limited 专属字段，未知字段一律 400`；`自定义 registry / source / index URL 与私有源凭据配置一律拒绝（400 Extra inputs are not permitted）`；`默认情况下服务器暴露的所有工具都启用。要只启用特定工具，把 default_config.enabled 设为 false 再逐个打开：这种模式……也可以让服务器运营方新增的工具默认保持关闭、待你审查后再启用`。
- **判据**：① **收紧一个面会连带掐断相邻面**：把网络收成 limited 后包管理器与 MCP 出网各自独立关闭，声明了 packages 却没开 `allow_package_managers` 直接 400 ⇒ 收紧配置必须配一份"相邻能力放行清单"，逐道显式打开，不能假设"我声明了要装包就自然会放行"。② **三道独立开关**（allowed_hosts / allow_package_managers / allow_mcp_servers）互不包含，放行 A 不等于放行 B。③ tagged union 与"未知字段一律 400"意味着**互斥分支的字段不能混写**，抄配置时最容易把另一分支的字段带进来直接报错。④ **白名单的默认值是未来策略**：默认全开 ⇒ 上游新增工具自动获得权限；`default_config.enabled=false` 反转 ⇒ 新增默认关闭待审 ⇒ 选型时先问"未来新增的东西该自动进来还是该等我点头"，而不是先问"现在要开几个"。⑤ 私有源与自定义 registry 一律拒绝 ⇒ **依赖可重现性在该平台上只能靠平台允许的公开源实现**，靠私有源的方案在此为不可实现项，须在设计期就替换。
- 提升层：可复用 Skill / 工作流。触发词：收紧连带失效、allow_package_managers、allow_mcp_servers、tagged union 未知字段 400、默认全开新增自动授权、default_config.enabled=false 反转、私有源被拒。
