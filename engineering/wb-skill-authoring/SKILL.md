---
name: wb-skill-authoring
description: >-
  Skill 的写法与体检：触发词设计、description 质量、文件拆分、跨工具迁移、安装前安全审查、安装后接线、触发评测盲测、no-skill 对照、效果归因、重复技能的去重与合并流程。当新增 skill、改写已有 skill 的 description、排查"技能该触发却没触发 / 不该触发却触发"、拆分过长 SKILL.md、把 skill 迁移到不同 AI 工具（Claude Code / Codex / Gemini 等）、安装第三方 skill 前做安全检查、或装了技能却总用不上（没接线）时应用。只写与自身工作流相关的约束和步骤，不写通用方法论套话。触发词：技能没触发、装了没用、接线、skill 不生效、触发评测、盲测、诱饵用例、no-skill 对照、效果归因、技能无增益、技能抢触发、误触发、负向边界、不适用于、审计技能、技能过期、拼写错误、乱码、失效工具名、重复触发、技能快速路径表、双路由、meta-router、description 上限、name 规范、快照基线、触发率、近失、指令改写、改了指令还是不行、改了两遍还是这样、调指令算修了吗、别再加一句必须、拆技能、技能合并、技能去重、查重、技能素材来源、gotchas、控制度校准、给默认不给菜单。、规则该写多少、AGENTS.md 变长、allowed-tools 是限制吗、禁用工具、权限叠加、停用还是删除、参数分发、万能技能、专用子代理、防递归、显式契约、靠推断、角色重叠、通才助手、示例与考题要不相交、自动放行的兜底层、硬禁清单、技能选择准确性评测、不需要却加载、选错 skill、评委团、集成必须留子分、ensemble、多评委同签名、judge_scores、可溯源、provenance、CI 出证、无旁路、禁读环境变量与文件系统、输入走显式参数、审计面等于参数表、一个包一个服务、代理层不受理、可重跑产物、脚本沉淀、不许硬编码结果、连跑两次存证、产物自带说明、persona 市场退场、GPT Store 停用、迁移为插件、优先可机读注册表、版本号不塞 description、双榜分离、社区热度榜、官方自研榜、创建者域名标注、匿名统一标签、纯 UI 信源不学、审计盲区、只记写不记读、传参值不入库、失败也留痕、跨面不同步、surface 能力面、按面降级、导航四信号、签名强度、显式调用跳过路由、@标识调用
version: 3.68.0
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
## 技能内脚本的 agentic 契约：输出尺寸要可预测，因为 harness 会截断（来源：agentskills.io《Using scripts in skills》2026-09-27 实拉）
- **原文要点**：`Many agent harnesses automatically truncate tool output beyond a threshold (e.g., 10-30K characters), potentially losing critical information. If your script might produce large output, default to a summary or a reasonable limit, and support flags like --offset so the agent can request more information when needed. Alternatively, ... require agents to pass an --output flag that specifies either an output file or - to explicitly opt in to stdout.`
- 判据：**脚本作者要为"输出会被截断"负责，不能让 agent 去猜被截掉了什么**。默认给摘要或合理上限 + `--offset` 翻页；若输出天生大且不好分页，就**强制 `--output` 显式 opt-in**（`-` 才写 stdout）。
- 同族契约（同一节原文，配套记忆）：①**禁止交互式提示**（agent 跑在非交互 shell，等 TTY 输入会无限挂起，缺参数要直接报错并给出可选项与用法）；②**`--help` 是 agent 学接口的主要入口**（简述+flags+示例，但要短，因为它同样占上下文）；③**报错要说清"错在哪/期望什么/可以试什么"**（`Error: --format must be one of: json, csv, table. Received: "xml"`）；④**结构化输出优先 + stdout 放数据、stderr 放诊断**；⑤**幂等、可拒绝歧义输入、破坏性操作给 `--dry-run`、不同失败类型给不同退出码并写进 `--help`**。
- 与 `wb-context-compressor` §大输入转检索 分工：**那条管"已经拿到的大材料怎么塞进上下文"，本条管"脚本从一开始就该产出多大的输出"**——一个在消费端补救，一个在生产端设上限。
- 反模式：脚本一次吐几百 KB 让 harness 静默截断（丢的往往是尾部的关键错误）；或用对齐的空白表格当输出（agent 与 `jq/cut/awk` 都不好解析）。
- 提升层：工具 / 可复用 Skill。
## 指针的措辞决定路由可靠性：先磨措辞，磨不动才内联（来源：skills.sh `mattpocock/skills/writing-for-agents`，2026-09-27 r200-C 实拉 75,462B 页面 / 2,436B 正文）

- **★★决定 agent 什么时候去取材料的，是指针的措辞，不是它指向的那份材料**：原文定义 *context pointer*——留在 agent 上下文里、点名某份上下文外材料、并编码"什么条件下该去取它"的引用；技能的 `description` 就是一种 pointer，`AGENTS.md` 里点名某文档的那一行也是同一种东西。判据：**一份必须拿到的材料挂在一条弱措辞的指针后面 = 一个方差 bug**（有时取到，有时取不到）；补材料不如补措辞。
- **★升级路径是固定的：先 sharpen 措辞，措辞磨到头仍不可靠才内联材料**：原文 "sharpen the wording first, and inline the material only if sharpening fails"。判据：**内联是最后一个手段**——它救的是这一处，代价是常驻上下文永久变贵；先动措辞成本更低，且不透支预算。
- **★一个 branch 一条触发，同义词是同一个 branch 写了两遍**：原文 "Synonyms that rename a single branch are one branch written twice; collapse them"——把同一件事换几种说法全列上去不是提高召回，是把预算重复花在同一条路径上。判据：**能合并成一个 branch 的写法必须合并，只保留真正会走出不同路径的分支**。
- **★指针里要砍掉正文已经自带的身份**：原文 "Cut identity the body already carries"——材料自己会说清自己是什么的那部分，不必在指针里再讲一遍。
- 与 §description 三条机检纪律 的分工：那条管描述字段的机械约束（首句位置 / 追加只加末尾 / ≤1024）；本条管**措辞够不够锋利，以及"措辞 → 内联"这条升级路径**。
- 提升层：可复用 Skill。
## 两种预算：model-invoked 花上下文负载，user-invoked 花人的认知负载（来源：skills.sh `mattpocock/skills/writing-great-skills`，2026-09-27 r200-C 实拉 75,086B 页面 / 2,550B 正文）

- **★技能存在的理由是"从随机系统里拧出确定性"，而确定性的度量是过程不是输出**：原文 "Predictability — the agent taking the same *process* every run, not producing the same output — is the root virtue"。判据：**评估一个技能好不好，看它能不能让 agent 每次走同样的流程**；拿"两次输出是否一字不差"当标准，是把随机系统的正常波动误判成缺陷。
- **★调用方式的选择是两种负载的取舍**：**model-invoked** 保留 `description`，agent 能自主触发、别的技能也能引用它，代价是描述每轮都占上下文（context load）；**user-invoked** 把描述从 agent 视野里摘掉，零上下文负载，代价是**你自己成了索引**（cognitive load）——只有手动敲名字才能调，别的技能也够不到它。判据：**只在"agent 必须自己够到它"或"别的技能必须引用它"时才付 context load**；只是偶尔手敲的技能做成 user-invoked 不亏。
- **★user-invoked 技能多到记不住时，解药是一个 router skill**：原文 "that piled-up cognitive load is cured by a router skill"——一个 user-invoked 技能把其他技能的名字与各自何时用列出来。判据：**认知负载堆到记不住，不是把每个技能都改成 model-invoked，而是加一层索引**；前者把成本转回上下文，后者只付一份。
- 与 §命名时态、§description 三条机检纪律 的分工：那两条管"名字与描述怎么写对"；本条管"**这个技能到底要不要对模型可见**"——先定可见性，再打磨描述。
- 提升层：可复用 Skill / 工作流。
## 技能静默成本与描述截断治理：不触发也花钱、触发短语放最前、/doctor 查截断（来源：Anthropic《Skill Costs》实测 + claude.com/blog/lessons-from-building-claude-code，2026-09-27 r231-B/C 实拉）
- **技能不触发也花钱**：5 技能 × 7 小时实测，dormant skills 描述层 **231K tokens 占 11% 账单**，3 个从没触发的技能占 18%——**每个 description 每轮都进上下文，装技能不是免费的**（与 §两种预算·model-invoked context load 同源：那条管"可见性取舍"，本条管"装了之后的账单"）。
- **提交技能前用 token counting API 估算描述成本**，超预算先砍描述再装。
- **触发短语放描述最前**：上下文压力下 description 会被截断，**截掉的就是调用入口**；`/doctor` 可检查描述是否被缩短。
- **副作用技能禁止自动调用**：deploy/commit/notify 类设 `disable-model-invocation: true`——有副作用的技能不该被模型顺手调用；触发权=风险权。
- **触发信号诊断表**：不加载→描述加细节关键词；过度触发→加负面触发更具体；输出不一致→加 examples/ 好输出示例。
- 判据：**描述是技能唯一的广告位**——先量它的每轮成本，再把最重要的触发词放最前；副作用技能手动触发。
- **清单本身的预算是"模型上下文窗口的 1%"，溢出时按调用频率削减 description 而非拒绝加载**（来源：Claude Code 技能文档 `code.claude.com/docs/en/skills.md` 全文端点，2026-09-28 r315-Q-C 实拉，作本节能**计量口径**升级）：官方 **"skill-listing budget scales at 1% of the model's context window"**，溢出时丢弃顺序 **"starting with the skills you invoke least"**，被削的是 **description 文本**（可降到 `skillOverrides:"name-only"`），另有 `skillListingMaxDescChars`/`skillListingBudgetFraction`/`SLASH_COMMAND_TOOL_CHAR_BUDGET` 三旋钮与 `/doctor`、`/skill-doctor`、`--debug` 三诊断入口；`description`+`when_to_use` 合并 **"truncated at 1,536 characters in the skill listing"**，正文 **"Keep SKILL.md under 500 lines"**。判据：① 库规模成本 ≈ min(预算, 每技能首 1536 字符 × 技能数)，**超预算的代价由最少用的技能承担**——新技能边际成本取决于它被调用多少次，预计低频就主动写成 name-only 或合并进家族；② **触发关键词必须落在 description 前 1536 字符内**（超出部分在清单里根本不存在）；③ 失效诊断顺序：先 `claude plugin validate`/`/skill-doctor` 确认字段解析 → 再看是否被清单预算削掉 description → 最后才怀疑模型不遵守。
- 提升层：可复用 Skill。
## Gotchas section 是技能最高信号内容：从失败点积累，随时间更新（来源：claude.com/blog/lessons-from-building-claude-code，2026-09-27 r231-C 实拉）
- **技能的 Gotchas 区写"用这个技能时真实撞到的失败点"**，随使用持续更新（Anthropic 例：subscriptions 表是 append-only 是踩过坑才知道的）——**价值一半在别人踩过的坑，把坑写进 Gotchas 不是写进正文**。
- 判据：写技能时先问"用的时候最容易在哪出错"，Gotchas 区是该答案的固定归宿；正文写怎么做，Gotchas 写别怎么做、为什么。
- 与 §技能写作十项 checklist 的分工：checklist 管"结构齐不齐"，本条管"失败经验的沉淀位置"。
- 提升层：可复用 Skill。
## 工具描述即 prompt：模型完全按描述决定调用，每个描述=迷你操作手册（来源：musketeerstech.com《Prompt Engineering Best Practices for AI Agents 2026》+ pickaxe.co，2026-09-27 r231-C 实拉，与 §工具描述可注入 互补——那条管"安全面"，本条管"写法的质量面"）
- **工具型 agent 里模型依据 name/description/parameter docs 决定调用什么、传什么参数**——**模糊描述产生错误调用，没有 system prompt 能修**；每个工具描述按写 prompt 的标准写（做什么/何时用/参数契约）。
- **单 agent 封顶约 4 个 action**：更复杂→waterfall 路由到专门 sub-agents，**不把 10 个工具塞进一个 prompt**（工具数超过认知负载就拆层）。
- **atomic-over-composite（单 action 单能力）**（Activepieces 设计哲学，2026-09-27 r231-A 实拉）：每个 action 只做一件能力、输入显式化——复合操作拆成原子步，模型好理解、失败好定位；配 throttling 防 agent 淹没 API。
- 判据：**写工具描述按写 prompt 的标准来，不是填空**；工具超过 4 个就分层，不硬塞。
- 提升层：可复用 Skill。
## 持久声明纪律：自我声明必须绑定会失效的机制，而非自证（来源：skillsmp.com/skills p98「context-architecture」No.9727，2026-09-27 r232-B 实拉；skillsmp 全量 10,991 技能中唯一把"声明可信度"上升为原则的一条）
## 技能家族与多渠道分发：命名空间前缀 + setup 引导技能 + 单一真身仓库（来源：skills.sh 榜单 2026-09-27 r206-B 独立实拉（All Time 安装 1,568,868；mattpocock/skills 11 个技能合计 4.3M、open.feishu.cn 一组 lark-* 21 个合计 16.0M、microsoft/azure-skills 8.5M，头部出现 setup-matt-pocock-skills 898.5K 这类安装器技能）；GitHub dotnet/skills 5,494 星（厂商官方语言技能仓）、netresearch/skill-repo-skill（技能仓库结构 + multi-channel distribution）交叉取证；与 §技能供应链可信 互补——那条管「单个技能可信不可信」，本条管「一组技能怎么组织与分发」）
- 三要点：家族用前缀共享命名空间（lark-doc / azure-messaging，前缀即边界自解释）；家族超约 5 个补一个 setup-<家族> 入口技能管装与配；多渠道分发 = 一个真身 + 多个发布面，分歧一律以真身为准，不在发布面改。
- 细则（含各平台规模与本轮判重）见 references/knowledge-base.md §r206-B。

## 触发面三机制：意图收敛状态机 / 混合意图依赖排序 / 覆盖矩阵约束路由边界（来源：腾讯 SkillHub 分数面头部 skill 实拉 2026-09-28 r207-A；包拯.SKILL 3931.3 万、育儿大师.Skill 2610 5.5 万；与 §r252-C A「四档可信度+熔断+changelog+前置门控」互补——那条管"质量信号"，本条管"触发与路由"）
- **渐进式意图收敛协议（N 轮状态机，典型 3 轮）**：领域技能不要在第一轮就假设听懂了需求，用固定轮数的状态机收敛意图再动手。判据：**把"猜"换成"收敛"**——用户描述不完整时，状态机按轮次补关键信息，而不是用默认假设填空。
- **混合意图自动任务拆解：按依赖排序 → 合并 → 顺序执行**：同一句话含多个意图时，先按依赖关系拓扑排序，能合并的合并，其余顺序执行。判据：**多意图不是并行乱跑，是先定依赖序**；无依赖才并行，有依赖必须串行。
- **领域覆盖矩阵约束路由边界**：用一张"领域 × 子类"矩阵显式声明本技能覆盖哪些格、不覆盖哪些格（如 22 类法律领域矩阵），**落在矩阵外的请求自动回落通用模板，而不是硬答**。判据：**边界写不出矩阵 = 边界其实没想清楚**；矩阵外回落比"勉强答"更好。
- **危机干预出口优先于一切领域分析**：技能必须声明一类"先于专业分析执行"的出口（如自杀/家暴/未成年人侵害先于法律分析）。判据：**专业能力越强，越要先声明它不适用、要让路的场景**；没有让路规则的领域技能是风险面。
- **隐式触发词清单进 description**：不要求用户说出领域关键词——"我家孩子""宝宝""娃"这类日常开场即触发；把这些口语开场白**逐条写进 description**，而不是只写领域术语。判据：**用户不会用你的分类词说话**。
- 提升层：可复用 Skill / 工作流。触发词：意图收敛、收敛协议、混合意图、依赖排序、覆盖矩阵、矩阵外回落、危机干预、让路规则、隐式触发、口语开场。

## 家族内触发边界仲裁：区分轴 / 家族导航技能 / 同族不并列竞争同一动词（来源：skills.sh All Time 榜 2026-09-28 r207-C 独立实拉首读；All Time 1,570,819；lark-* 21 个合计 16.0M（lark-doc 731.3K / lark-okr 709.5K / lark-markdown 695.0K / lark-apps 639.6K / lark-vc-agent 672.7K）；mattpocock/skills 11 个 4.3M；microsoft/azure-skills 多组（4.2M / 4.8M 两口径）；genmedia-labs/skills 5 个（video-edit / ai-music / ai-video-generation / image-to-video / ai-image-generation）；heygen-com/hyperframes 3 个（hyperframes / hyperframes-cli / hyperframes-registry）。与 §r206-B 家族分发互补——那条管"家族怎么组织与分发"，本条管"家族内部谁响应哪个请求"）
- 四要点：家族内必须有显式**区分轴**（lark-* 按业务对象 / hyperframes-* 按交互面 / genmedia 按模态+动作），同族对同一动词只留一个主响应者；家族超约 10 个补"导航技能"（find-skills 3.6M、wayfinder 573.6K）而不仅是 setup 入口；目录站"家族合计"口径会自相矛盾（azure 同页 4.2M 与 4.8M），只引单技能数字。
- 全文（含三个家族逐项规模与判据）见 references/knowledge-base.md §r207-C。触发词：技能家族、家族内抢触发、区分轴、同族竞争、导航技能、wayfinder、find-skills、家族合计口径。

## 打包门禁：保留字禁入技能名 + 改名与描述裁剪必须联动做（来源：github.com/anthropics/skills commit `0a64e39` / PR #1605，2026-09-28 r208-A 独立实拉）
- **技能名含厂商/产品保留字会被上传校验直接拒**：`claude-academy-guide` 为打包成可上传自定义技能被重命名为 `academy-guide`——依据 agent skills best-practices，技能名不得含 `claude` / `anthropic` 等保留字；重命名同时改了三处：技能目录名、SKILL.md frontmatter `name`、marketplace.json 的 entry name 与 path。判据：**只改一处会导致目录 / 元数据 / 市场条目三处不一致，装得上但注册不上**。
- **改名必须连带复测 description 长度**：同一 commit 把 description 从 1,176 压到 992 以过 1024 上传校验，且压后文本是"内部实测过的版本"——不是随手截断。判据：**改名和描述裁剪是同一次打包门禁的两半，分两次做会漏掉一半**。
- **面向分发的技能要按"可分发性"反推命名，不是先起名再想分发**：该 commit message 明示改名的唯一目的是 make the skill packageable，无其他内容改动。判据：**命名争议先问"它要不要上传"，要上传就受保留字与长度双重约束**。
- 提升层：可复用 Skill / 工具。触发词：技能改名、打包失败、上传校验、保留字、技能名规范、description 超限、marketplace 条目、可分发性。

- **防同名接管要落到"归一化后比较"，不是比较字符串**（来源：Claude Code 技能文档 `code.claude.com/docs/en/skills.md`，2026-09-28 r315-Q-C 实拉，作本条目**升级**）：官方规则——保留名 `synced`（**任意大小写**）与 `anthropic-skills`/`anthropic-skills:*` **直接不加载**；且 **"name matching ignores case, spacing, invisible characters, compatibility forms"**（全角字符视为同名）。判据：① 技能体检脚本里加一条**同名冲突判定**——把待安装/新建技能名做归一化（转小写、去空格、剥不可见字符 U+200B/U+200E/U+2060 等、NFKC 兼容形式折叠、全角转半角）再比对库内既有技能与保留名清单——**只看字面比较会漏掉同形欺骗**（与 0.7「同类判定看功能不看名字」原则层互补，本条补可执行算法）；② 自建**保留名清单**（如 synced/master/system/core），防外部包用我方命名习惯反向冒充；③ 归一化后同名的技能若确为不同物，**拒绝安装而非后者覆盖前者**（与 §技能仓治理 stored name 不可变 配套）。

## 易变上游规则只放链接不放副本，改链接时同步校正已漂移断言（来源：github.com/anthropics/skills commit `3337550` / PR #1825，2026-09-28 r208-A 独立实拉）
- **会变的外部数字/规则（计费、限额、配额、价格、SLA）不要复述进技能正文，改为指向上游文档对应小节**：PR 把 claude-api 技能里每句 refusal billing 的规则改成指向文档"How refusals are billed"小节，而不是在技能内重述规则。判据：**副本一旦复制就与上游解耦，漂移是时间问题而非概率问题**。
- **改链接的那一次，必须顺带核对并修正技能内已漂移的旧断言**：同一 PR 同时修正两条与文档不符的说法（无输出前的拒答计入速率限制；流中拒答对已 stream 的输出同样计费）。判据：**只换链接不改正文 = 保留了错误信息又给了正确出处，比不换更糟（读者会以为正文与链接一致）**。
- **技能正文只留"稳定判据"，把"易变事实"外包给链接**：稳定的是"拒答怎么计费"这个概念需要存在，易变的是具体计费口径与限额数字。判据：**写技能时对每个外部事实问一句"它半年内会变吗"，会变的只留指针**。
- 提升层：可复用 Skill / 工作流。触发词：技能过期、技能内容漂移、规则复述、放链接还是复述、文档同步、断言失效、计费规则变了。

## 封装层的向下告知义务：上游破坏性变更必须主动推给使用者并分级标注（来源：Make Help Center 发布公告栏 2026-09-28 r208-B 独立实拉）
- **做了封装，就接下了"上游 changelog 的下游推送"这份责任**：发布栏连续挂出的是上游第三方的弃用与破坏性变更——OpenAI 旧模型 2026-09-28 弃用、Sora 与 Video 模块 2026-09-24 弃用、Dynamics 365 API v1.0「Action required」、Shopify「Update an Inventory Level」标 Breaking change、Alegra resource ID 格式变更。判据：**使用者通过封装间接依赖上游，看不到上游 changelog；你不做推送，他的场景就在某个截止日静默失效。**
- **变更公告必须带三要素：截止日期 + 影响的具体模块名 + 需要的动作**：上述每条都给了明确日期与受影响的模块/连接。判据：**只说"某服务将升级"的公告等于没发；没有截止日期和模块名的通知无法被使用者转成待办。**
- **分级标注要能一眼区分"会坏"和"要改"**：Breaking change（会坏，必须改）与 Action required（还能跑，但需迁移）是两类，混在一起会让使用者对真正的 P0 麻木。判据：**分级的目的不是整理信息，是让使用者能排序。**
- **对技能/包装的推论**：包装第三方能力的技能，其正文应写明"上游变更如何到达使用者"（版本钉 / 弃用提示 / 失败时的指向），而不是假设使用者会自己盯上游。判据：**封装的价值是屏蔽复杂度，不是屏蔽变化——变化必须透传，复杂度才被屏蔽。**
- **破坏性变更可写成一条机械规则，不用主观分级**（来源：Activepieces 官方 piece 版本规则 `docs/.../piece-versioning.mdx`，经 api.github.com/contents 通道，2026-09-28 r314-Q-B 实拉，作本条目**判定侧**升级）：官方原文 **"any removal is breaking, any required addition is breaking, everything else is not"**（配 semver；另有 `minimumSupportedRelease` 声明依赖的宿主最低兼容版本）。判据：① 改技能/升级前先查两类动作——**删掉任何字段/文件/步骤**、或**把任何可选项变必填**——命中即破坏，其余一律非破坏，**无需主观判断**；② 配套引入 `minimumSupportedRelease` 式字段，让不兼容在**安装前**就失败而非运行中失败；③ 本点是"向下告知义务"的**判定侧**补充——那条管"怎么告知"，本条管"怎么判定"（闭合 WB r208 点名索取的"平台/RFC 层正式定义"）。
- 提升层：可复用 Skill / 工作流。触发词：上游变更、破坏性变更、弃用通知、Breaking change、Action required、封装层告知、间接依赖、截止日期、模块名。

## 技能市场的商业化层：付费/分润、插件入口、赛事供给——规模数字要按面拆开读（来源：腾讯 SkillHub 技能广场 `skillhub.cn/skills?sortBy=score` 2026-09-28 r209-A 独立实拉；导航区同时挂出「插件 NEW」`skillhub.cn/plugins`、「SkillPay」、「大赛」`skillhub.cn/contest` 三个入口；页面声明共 17.0 万技能，来源分「全部来源 / 认证企业 / 用户自主发布」，排序面分 score / 近期飙升 / 下载量 / 最近上新，部分技能标「需配置 API Key」）。与 §技能家族与多渠道分发 互补——那条管"一个真身多发布面"，本条管"市场用什么机制把供给拉进来"
- **市场进入商业化阶段后，"分润/付费"本身成为一个可核验信源**：此前 SkillDepot 分润因缺可信源长期 pending；本轮在 SkillHub 官方导航直挂 SkillPay 入口，说明技能付费/分润已是一等入口而非第三方传闻。判据：**判断"技能能不能卖钱"不要找二手文章，去看官方市场导航有没有独立入口**。
- **供给端三条腿要分开看：发布、售卖、激励**（发布 Skill / SkillPay / 大赛），一条腿的繁荣不代表另两条——本轮 17.0 万技能是"发布"口径，与下载量、score 不同面。判据：**引用市场规模数字必须写明是哪个面的口径**；"17 万技能"不等于"17 万有人用"。
- **来源标签先于内容判断**：页面把来源分为公开渠道 / 认证企业 / 用户自主发布，并在页脚声明"使用前请注意识别相关风险"。判据：**市场自己都不背书的来源，使用者更不能默认可信**；采纳第三方技能先看来源标签再看描述。
- **"需配置 API Key"是准入门槛信号，写在卡片上而非藏在文档里**：头部技能（腾讯文档、ima-skills、钢联 AI）在列表页直接标出。判据：**有前置依赖的技能必须把依赖写在能被看到的地方**，否则用户安装即失败。
- **付费技能的"验收"验的是支付链路不是技能质量；争议与退款整体让渡给支付渠道，平台声明自己不是交易方**（来源：腾讯 SkillHub SkillPay 官方门槛 + bundle 内付费治理字段，api.skillhub.cn + skillhub.cn，2026-09-28 r314-Q-B 实拉；闭合 WB r210/r211/r212 连续三轮 pending 的验收口径）：原文门槛 **"提交后平台将核验完整的微信 AI 支付下单链路，校验无误才可审核通过"**；价格约束 **最小 0.01 元、最大 100 元、单位「元/次」**，字段面 `paid`/`paidWhitelistOnly`/`amount`/`currency`/`pricing`；入驻需**人脸实名**；退款原文 **"用户可在对应微信/支付宝账单发起咨询或退款，平台依据所选渠道规则协助处理"**；平台免责 **"不作为该笔交易的收款方或服务实际提供方"**。判据（三点可迁移）：① 凡我方交付物涉及外部副作用（推仓/发消息/写库），**验收标准须含端到端链路跑通且状态可回查**，只看产物合格不够；② "协助处理 + 依渠道规则"是把争议责任外置到既有仲裁机制——遇到"我改坏了用户的东西"同理（明确指向 git 历史/回收站这类既有回滚机制，而非自承诺恢复）；③ 若要给技能加付费面，必须同时备齐"实名 + 链路核验 + 免责定位"三件，缺一就不该开。
- 提升层：可复用 Skill / 工作流。触发词：技能付费、SkillPay、技能分润、技能市场、大赛、插件入口、来源标签、认证企业、需配置 API Key、市场规模口径。

## 技能仓治理：生效 / 隔离 / 下架三态 + 标识符不可变（来源：ClawHub moderation + docs.openclaw.ai/clawhub，2026-09-28 r314-Q-B 实拉；与 §分发双通道（r312-Q-B 上游可被改写）互补——那条管"分发通道风险"，本条管"仓内可疑技能的处置流程"）
- **技能状态不该是"装/不装"二值，市场级实践是三值以上**：ClawHub moderation 原文 **"A listing may be held, hidden, quarantined, revoked, or otherwise unavailable"**（五种非生效态，quarantine 与 revoked/hidden 并列）；**"Signed-in users can report… Moderators can review reports, hide or restore content, and ban abusive accounts"**（举报→人工复核→可恢复的双向动作）；违规恢复走独立申诉入口 `appeals.openclaw.ai`；防同名接管的唯一明文机制是 **"Catalog lists may shorten long names visually without changing the stored name"**（**stored name 不可变**，展示名可变）；条目暴露 `verificationTier:"source-linked"` 分级字段。
- **判据**：① 审计发现可疑技能时，**先转"隔离态"（保留文件 + 记录理由 + 禁用触发，不删）**，判清后再决定 restore/删除——现在"发现重复/可疑就直接删或只标注"是二值化导致要么丢能力要么留风险；② **技能目录名一旦落地就不可变**（改名＝身份变更，会让外部引用与安装记录指向错对象）；③ 给每个技能补 `verificationTier` 式分级（source-linked / 实拉验证 / 未验证），让"这条建议的证据强度"变成字段而非行文语气；④ 处置必须可逆且有第二人复核——我方由 WorkBuddy 单点审计，至少留"用户一句话可回滚"的显式恢复路径（与 AGENTS 0.8 同向）。
- 提升层：工作流（技能仓治理）+ 可复用 Skill（分级字段）。触发词：技能下架、quarantine 隔离态、stored name 不可变、verificationTier、申诉恢复、技能仓治理。

## description 内容合规门禁：触发面不是广告位、不是恐吓位（来源：腾讯 SkillHub 技能广场 skillhub.cn/skills?sortBy=score 2026-09-28 r210-A 独立实拉）
- **实证（三类污染同一页并存）**：① **导流型**——「专利初稿助手」（3620.0 万）在技能介绍正文末尾直接写「学习交流欢迎联系微信号 A26dian4」；② **自夸型**——「编程专家.Skill」（278160.5 万）自称「P8 级编程助手，25 年实战经验」，头衔写进能力描述；③ **恐吓触发型**——「web-tools-guide」（21625.3 万）写「Without reading this skill, you WILL handle failures incorrectly」，用「不读就必错」逼触发。
- **判据**：description 是**机器路由信号 + 人的能力边界说明**，不是营销位。写之前过三问——① 这句话能被核验证伪吗（「P8 / 25 年」不能 → 删）；② 删掉它会不会影响触发（微信号不影响 → 删）；③ 它描述的是「何时该用」还是「不用你就完了」（后者 → 改写成触发条件）。
- **合规写法**：能力声明只写**可核验事实**（支持的格式、覆盖的接口、明确的触发场景）；自我评级、联系方式、「不用就错」式措辞一律移出 description。
- **★站外联系方式 = 供应链逃逸信号（判据后果升级，r213-A SkillHub 实拉复核）**：description 内出现微信号 / 二维码 / 私信引导（如「专利初稿助手」末行「联系微信号 A26dian4」），不只是「营销污染」——它是**作者把用户引流到平台审核之外**的逃逸通道。后果升级：① 出现即判**不可信来源**，整技能不落 / 不引用，并记入 supply-chain 风险台账；② 同理「达到及格即可」式能力自评 = 作者明示低质态度，一并作低质信号。本点补 r210-A「移出联系方式」的**处置后果**，不重复其写法约束。
- 与 §打包门禁（命名禁保留字）互补——那条管「名字合不合法」，本条管「描述里能不能塞广告与虚价」。
- 提升层：可复用 Skill / 工具。触发词：description 合规、技能描述、导流、自夸、技能营销、能力声明、触发面、供应链逃逸、站外联系方式、低质信号。

## 市场同内容多副本与分数分叉：选型先过来源标签与描述实质，不看分数（来源：同上，r210-A）
- **实证（同页三组重复供给，分叉达百倍级）**：「编程专家.Skill」（作者前缀 indiv-ebandao，278160.5 万）与「dev-expert」（user_814dbe54，1593.0 万）**描述近乎同一份**；「防骗大师.Skill」（indiv-ebandao，2766.5 万）、「anti-fraud」（user_814dbe54，0.40 万）、「防诈专家」（indiv-skill，135.7 万）**同题材三个副本并存**；腾讯文档、ima-skills 等则带「已认证」徽标。
- **作者前缀即身份**：indiv- 个人 / org- 企业 / tencent-adm 平台官方 / user_ 匿名注册——前缀是页内唯一不靠自述的身份信号。
- **判据**：① **分数与下载量是流行度不是质量**，同内容副本之间能差 100 倍以上，不作选型依据；② **先按来源标签与认证徽标过滤，再比对描述实质判重**——同描述副本取认证/官方那一支；③ **引用「某技能多火」时必须带作者前缀**，否则数字对不上对象。
- 与 §技能市场的商业化层（来源标签先于内容判断）互补——那条定「先看来源」的顺序，本条给出「同内容多副本怎么挑」的具体动作。
- 提升层：工作流 / 可复用 Skill。触发词：技能选型、重复技能、同内容副本、技能评分、下载量、来源标签、已认证、市场去重。

## 工具集是带依赖顺序的图，不是扁平清单：触发路由之外还有「调用顺序」约束（来源：deeplearning.ai 短期课程《Knowledge Graphs for AI Agent API Discovery》SAP，1h14m，2026-09-28 r210-C 独立实拉）
- **课程主张**：构建知识图，使 agent 能够**以正确的顺序发现并调用正确的 API**——「正确顺序」被当作独立于「选哪个 API」的能力来教。
- **判据**：① 当工具/技能数量上到十几个，**扁平清单会退化**——模型看得见全部名字，却看不见「A 必须在 B 之前」「C 的入参来自 D 的产物」；这类错误表现为**选对了工具、调错了顺序**。② **顺序约束要显式写进技能正文**（前置条件 / 产出被谁消费），不能指望从名字推断。③ 与 `wb-max-token-saver` 的「可见工具 30–50 就衰减」互补——那条管**数量**带来的衰减，本条管**结构**缺失带来的错序；减数量与补顺序是两件事，不能互相替代。
- 与 §家族内触发边界仲裁 互补——那条管「同一族里谁响应这个请求」（横向竞争），本条管「同一族里谁必须先跑」（纵向依赖）。
- 提升层：可复用 Skill / 工作流。触发词：工具顺序、API 发现、调用顺序、依赖关系、工具集组织、扁平清单。

## 同一份 SKILL.md 会被 40+ 异构客户端直接消费：按「最小公分母」写，别用任何单客户端私有特性（来源：agentskills.io 官方 Client Showcase（2026-09-28 r211-B 独立实拉）+ docs.openclaw.ai 首页（同期独立实拉）；与 §技能家族与多渠道分发（r206-B）互补——那条管「发布到几个面」，本条管「写的时候能被多少种客户端读得动」）
- **消费端清单是异构的**：官方 Showcase 同时列了 Claude、ChatGPT & Codex、Cursor、VS Code、Gemini CLI、GitHub Copilot、Kiro、Goose、OpenHands、Letta、Amp、opencode、Roo Code、TRAE、Factory、Qodo、Mistral AI Vibe、Spring AI、Snowflake Cortex Code、Pulumi Neo、JetBrains Junie、Databricks Genie Code、OpenClaw 等 40+ 客户端；规范由 Anthropic 发起后作为**开放标准**发布，接受外部贡献。
- **可被普遍消费的最小公分母只有三样**：`name` + `description` + Markdown 正文（规范明示 "metadata (name and description, at minimum) and instructions"）；`scripts/`、`references/`、`assets/` 是可选且**只在 Activation/Execution 阶段按需加载**。
- **因此有三条硬约束**：① 正文不得依赖某一客户端独有的能力（专有命令、专有 frontmatter 字段、专有目录约定）——依赖了不会报错，只会在其他客户端**静默退化成普通散文**；② 脚本路径用相对路径与 POSIX 兼容写法（OpenClaw 官方并列给出 macOS / Linux / WSL2 / 原生 Windows 四条安装路径，Windows 不是例外而是并列一等公民）；③ 关键行为不能只写在 `scripts/` 里，必须在正文留一行人类可读的等价说明——脚本在无执行环境 / 未授权执行的客户端里根本不会跑。
- **判据**：把技能想象成「要发给一个你不认识的实现者读」——凡是只有你自己这套环境才懂的部分，都是它在别处失效的地方。写完自问：**这个技能在我的客户端之外的第二种客户端上，行为会不会变？**
- 提升层：可复用 Skill / 工具。触发词：跨客户端、客户端兼容、最小公分母、开放标准、私有特性、静默退化、相对路径、Windows 一等公民。

## 品质形容词不配锚点就是废话：官方自己把「distinctive」改成了「反例对照 + 显式确认」（来源：anthropics/skills PR #1713 "Update frontend-design skill to avoid generic design defaults"，2026-09-28 r211-B 经 GitHub API 取 diff 实拉核验；与 §易变上游规则只放链接（r208-A，同仓库 PR#1825）同源不同条——那条管链接，本条管措辞）
- **原文（被改掉的版本）**：`pin it yourself before designing: name one concrete subject... and state your choice` —— 「自己定，然后声明你的选择」。
- **改后版本**：`identify it yourself before designing, **and confirm with the client**` —— 把「内部猜测 + 自我声明」升级为**一次对外确认动作**。判据：**只要求模型「声明」等于允许它自己给自己发许可证；要求「确认」才引入第二方。**
- **同时给形容词补了可对照反例**：新增一句 `a design for a toy for girls aged 8–11 will be very aesthetically different from a dashboard for financial analysts`。判据：**"distinctive / opinionated / 高质量 / 专业"这类词在没有对照物时不可判别**——模型只会用它见得最多的那个模板当作「符合要求的输出」。
- **通则可核验的写法**：每写一个品质形容词，必须同时给三者之一——① 一个具体反例（「A 长这样，B 长那样，本技能要的是 B」）；② 一个可执行的确认动作（问谁、问什么、拿到什么算确认）；③ 一组可数的判据（数字 / 字段 / 清单长度）。**三者全无 → 删掉这个形容词**，它只在增加字数。
- **自检**：grep 技能正文里的 `distinctive|opinionated|专业|高质量|合理|优雅|完善`，逐条问「凭什么说现在这份输出符合/不符合」；答不上就是待补锚点。
- 提升层：模型 / 可复用 Skill。触发词：形容词、distinctive、opinionated、反例对照、显式确认、不可判别、模板输出、品质词要有锚点。

## 目录站数字有两种失真：家族「求和」与父级「复制」，识破法是比同族多条目（来源：skillsmp.com 首页（2026-09-28 r211-C 独立实拉）；与 §家族内触发边界仲裁（r207-C）互补——那条给出「合计口径不可引」的结论，本条给出「怎么一眼看出它不可引」）
- **失真一（求和）**：目录把同一家族/仓库的多个技能加总成一个数字。
- **失真二（复制，本轮实证）**：SkillsMP 首页 `frontend-design`（anthropics/skills）与 `skill-creator`（anthropics/skills）安装数**同为 177.5k**；同页其他仓库条目则各不相同（`brainstorming` 289.8k / `ui-ux-pro-max` 129.6k / `ppt-generation` 82.8k / `vercel-react-best-practices` 31.4k）。**同一父级下多个子项数字完全相同 = 该数字挂在父级（仓库/家族）上，被复制给每个子项**，不是单技能的量。
- **识破法（可写进选型清单）**：在同目录里挑**同一作者/仓库的两个以上技能比对数字**——雷同即复制口径；再看目录是否单列「+N more from X (M total)」聚合行——有即求和口径。两种口径都不能当单技能热度用。
- **同一页还有第三种口径差**：`ui-ux-pro-max` 的 129.6k 与 `brainstorming` 289.8k 差距是真实量级差，说明**不是所有数字都失真**——判据：**先做同族比对确认口径，再决定这个数字能不能引；不要一律不信，也不要一律照抄。**
- 提升层：可复用 Skill / 工具。触发词：目录数字、口径失真、父级复制、同族比对、安装数雷同、skillsmp、市场数字不可引。

## 目录的分类轴决定技能被谁发现：按「职业」编目的市场要求 description 写岗位名（来源：skillsmp.com 首页分类区（2026-09-28 r211-C 独立实拉））
- **实证**：该市场用**职业大类**而非技术领域编目——`Computer and Mathematical Occupations` 2,103,881、`Business and Financial Operations Occupations` 340,647、`Arts, Design, Entertainment, Sports, and Media Occupations` 141,550、`Office and Administrative Support Occupations` 67,817（合计约 265 万）。分类名取自标准职业分类（O*NET/SOC 体系），**不是「前端/后端/数据库」这类技术轴**。
- **推论**：技能放在不同目录里，最有效的可发现性信号不一样——**按职业编目的目录，命中靠「谁会用它」（岗位名、职务、行业场景）；按技术编目的目录，命中靠「它做什么」（框架名、动作、文件格式）。**
- **做法**：`description` 里至少各放一个——① 一个岗位/角色名（财务分析师、前端工程师、运营、HR）；② 一个技术动作（生成、校验、转换、比对）。**只写技术动作的技能，在职业编目市场里等于没有检索面。**
- **判据**：把技能投到某个目录前，先问「这个目录用什么轴编目」；轴不对，触发词写得再全也排不进正确的分类桶。
- 提升层：可复用 Skill / 工具。触发词：分类轴、职业编目、O*NET、岗位名、可发现性、目录分类、检索面。

## 触发词洪水与语义劫持：把 description 做成吸尘器，会饿死别的技能（来源：腾讯 SkillHub 技能广场 skillhub.cn/skills?sortBy=score，2026-09-28 r212-A 独立实拉）
- **实证（同一作者三技能同模式，且都在分数面头部）**：「育儿大师.Skill」（indiv-ebandao，26105.5 万）写「只要用户的问题涉及孩子……**即应触发本技能，无需用户明确说出「育儿」二字**」，并在正文铺开上百个生活词（疫苗/湿疹/厌学/二胎/隔代/感统……）；「防骗大师.Skill」（同作者，2766.5 万）写「**主动亮剑**」「**即使对方并未询问反诈**」；「包拯.SKILL」（同作者，3931.3 万）写「主动嗅探风险词并插入预警」。三份 description 都是**同一个人写的同一种扩张模式**。
- **判据**：`description` 的作用是**在 Discovery 阶段竞争**（见 §渐进式披露三阶段：启动时只有 name + description 参与）→ 谁把描述铺得越宽，谁抢到的路由越多。触发扩张不是「写得更全」，是**把别人的请求也圈进自己的触发面**；代价不由作者承担，而由**被抢的其他技能与最终用户**承担（该响的技能没响）。三问扩展一问：**这句话是在描述「我何时该用」，还是在声明「你不叫我也该我上」**——后者一律删。
- **合规写法**：触发条件写**用户会真的说出口的那句话**；同义扩展控制在可枚举的几条内，禁止「无需用户明说」类表述。
- 与 §description 内容合规门禁 互补——那条管描述里塞广告/自夸/恐吓（内容污染），本条管**触发面无限扩张**（路由抢占）。
- 提升层：可复用 Skill / 工具。触发词：触发词洪水、语义劫持、路由抢占、description 过长、无需明说、主动触发、技能饥饿。

## 触发扩张是「作者级指纹」：按作者前缀聚类，一次判一批重复供给（来源：同上，r212-A）
- **实证**：分数面同页内，indiv-ebandao 一人同时占「编程专家.Skill」（278160.5 万）、「育儿大师.Skill」（26105.5 万）、「防骗大师.Skill」（2766.5 万）、「包拯.SKILL」（3931.3 万）、「李白.Skill」（5630.3 万）五个头部位；且「编程专家.Skill」与 user_814dbe54 的「dev-expert」（1593.0 万）描述近乎同一份、「防骗大师.Skill」与同前缀作者的「anti-fraud」（040.0 万）也是同一份。
- **判据**：① **先按作者前缀聚类再看条目**，同一作者的多个技能往往共用一套写法（扩张模式、模板结构、措辞习惯），判出一个模式就能**批量判掉一批**，不必逐条比内容；② 作者前缀还暴露**同内容多副本的搬运方向**（官方/认证前缀 → 匿名 user_ 前缀）。
- 与 §市场同内容多副本与分数分叉 互补——那条给「同描述副本怎么挑」，本条给「怎么一次性找出这批副本」（按作者聚类）。
- 提升层：工作流 / 可复用 Skill。触发词：作者聚类、技能去重、批量判重、同作者多技能、作者前缀、供给方指纹。

## 技能正文必须内建「宿主既有约定 > 本技能全部指南」的让渡条款（来源：raw.githubusercontent.com/anthropics/skills/main/skills/xlsx/SKILL.md 2026-09-28 r312-Q-B 实拉；r279-C 复核）
- **实证**：Anthropic 官方 `skills/xlsx/SKILL.md` 硬约束末尾原文 "When editing an existing file, match its conventions exactly — they override every guideline here"；同文件要求**每个假设/硬编码数字就地注明并给可核外部出处**（样本 "Company 10-K FY2024 Page 45 [SEC EDGAR URL]"）。
- **判据**：写技能时显式给一条优先级声明——**操作既有工件/既有仓库时以对象自身约定为准，本技能规则让位**，否则技能会把自身风格强加到用户既有产物上（与 0.7「宿主产物不可逆改动需谨慎」同向）；「逐处内联标注假设 + 外部可核出处」比现有 AV 的"结论级标注"更细一档，作 AV 产物侧实例。
- 提升层：可复用 Skill（次要 AV 工具层）。触发词：让渡条款、宿主约定优先、match its conventions、内联出处标注、假设就地注明。

## 「提醒/追问」类技能必须自带触发上限 + 负面清单（来源：api.github.com/repos/anthropics/skills/contents/skills/discernment-nudge 2026-09-28 r313-Q-A 实拉；r279-C 复核；与 wb-max-token-saver 输出纪律互补）
- **实证**：Anthropic 新技能 `discernment-nudge` 频控硬规则原文 "Offer the nudge at most once per conversation"，并把 **When to offer / When not to** 写成独立章节（排除＝创意写作、闲聊、琐碎查询、纯教育），frontmatter 只留 name/description/license 三字段、无脚本无 tool-use。
- **判据**：我方凡"每轮补一句建议/追问/核查提示"型条目（去 AI 味、防跑偏、落地提醒）**都要写死一个次数上限**，并把"什么时候不要触发"作为与"什么时候触发"同等篇幅的独立章节——没有负面清单的提醒型技能会随对话变长退化为噪音，且这类噪音不计入 token 却持续降信任。结构上复用其五段顺序（Why→When to→When not→Writing→Output）作提醒型技能模板骨架。
- 提升层：可复用 Skill（次要：输出侧 token 纪律）。触发词：提醒上限、负面清单、once per conversation、When not to、追问噪音、提醒型技能模板。

## 结构 lint 与安全门物理分离：lint 通过 ≠ 安全担保（来源：arxiv.org/html/2608.08453v1《13.8 万 SKILL.md 缺陷实证》2026-09-28 r313-Q-C 实拉；r279-C 复核）
- **实证**：10 万+ 份样本分档——确定性 lint 实测 58.4% 可自动修，**内容安全门实证 0% 可自动修**（必须独立人工/裁判）；路由元数据（触发指引）是第一优先修复项（实测 +6pp hit@1：88.5%/0.906 vs 82.6%/0.855）；缺陷分档 R1 67.0% / 缺触发指引 52.3% / 正文 44.3% / 资源 32.1%。
- **判据**：技能体检流水线拆成「确定性 lint（可自动修）」与「内容安全门（必须人工/裁判）」两道，**禁止用 lint 通过当安全担保**；并把**路由元数据（触发指引）列为第一优先修复项**——缺触发指引的技能再"干净"也先修触发面。
- 提升层：可复用 Skill + 工具。触发词：lint 安全盲区、结构 lint、内容安全门、触发指引优先、58.4% 可修、0% 安全可修。

## 技能的失败是「域」级的，最常见失败态是静默降级而不是报错（来源：`code.claude.com/docs/en/skills` 官方 Gotchas，2026-09-28 r315-Q-C 实拉；与上条 lint/安全门并读——那条管"修什么"，本条管"怎么发现它根本没生效"）
- **实证**：官方 Gotchas 两条原文——**"malformed YAML → skill still loads with no fields set"**（技能照常加载但字段全空 ⇒ 永远不会被触发，无任何错误提示）；**"A failed command aborts the entire skill invocation, not just its own placeholder"**，对策原文 **"Append `|| true` to any other command you expect to exit non-zero"**；官方自检三入口 `claude plugin validate .claude/skills`（v2.1.233+）、`/skill-doctor`、`/debug`。
- **判据**：①技能体检在"能解析"之上加一条**"字段数为 0 即视为坏技能"**断言——只保证解析成功不保证解析出了东西，**零字段技能在列表里存在、行为上不存在，是最难归因的一类失效**（与"description 含半角 `: ` 导致静默失败"同族，本条给通用判据）；②技能正文内嵌命令**默认按"一处非零退出＝整技能中断"设计**，可容忍的失败必须显式 `|| true` 或先判存在再执行，不能假设失败只影响它自己那一段；③"技能没生效"的排查次序固化为四层：**字段解析 → 清单预算被削（见 §清单 1% 预算）→ 压缩丢弃（r173B）→ 模型不遵守**，逐层排除后才允许改文案。
- 提升层：可复用 Skill（体检判据）+ 工作流（归因次序）。触发词：静默降级、零字段、malformed YAML、`|| true`、整技能中断、技能不生效归因、claude plugin validate、skill-doctor。

## 技能的可写数据必须落在「跨升级保留」的独立目录，且同步型技能只能下不能上（来源：`code.claude.com/docs/en/skills` + api.github.com `zai-org/GLM-skills/skills/glmv-stock-analyst/SKILL.md`，2026-09-28 r315-Q-C 实拉；与 §分发双通道（r312-Q-B 上游可被改写）同源——那条是被改写的代码，本条是被吃掉的状态）
- **实证**：官方字段面有专门的持久目录 **`${CLAUDE_PLUGIN_DATA}`（原文 "survives plugin updates"）**，与只读的 `${CLAUDE_SKILL_DIR}` / `${CLAUDE_PLUGIN_ROOT}` 分列；同步型技能原文 **"downloads synced skills and never uploads them"**（永不回写上游），同步检查节奏 **"about every 10 minutes"**，入站内容做消毒（"removes control characters… escapes angle brackets"）。第三方同构实证：智谱 `glmv-stock-analyst` 用 `{SKILL_DIR}` 占位符、**输出落 `os.getcwd()` 的 workspace 而非技能目录**，并在正文自带版本号 **"stock-analyst v3.2"**。
- **判据**：①凡技能需要记忆/缓存/状态（跑批游标、上次学到哪），**必须写进独立数据目录并明确该目录不受技能文件更新影响**——否则一次订阅制自动更新就吃掉游标；②技能自带版本标识写在正文（v3.2 式），使"我用的到底是哪一版"可独立于仓库历史回答；③同步/镜像型技能一律按**单向只读**对待，本地改动不会回传，**不要在同步型技能里写"本地经验"**；④入站消毒（控制字符/尖括号转义）作为"从市场拉技能"的固定预处理，与防注入纪律同线。
- 提升层：可复用 Skill（结构约定）+ 工具（落盘路径）。触发词：CLAUDE_PLUGIN_DATA、跨升级保留、同步型只下不上、游标落盘、技能自版本、入站消毒。

## 计数失真第三形态：数据源自己承认不精确——先看「自认标记」再决定要不要横向比对（来源：skillsmp.com 分页块 2026-09-28 r283-B 经 Qoder r316-Q-A 实拉取证 + WB 判重复核；续 sa 3.35.0 ③）
- **实证**：分页块 `{total:1200, totalIsExact:false, isCapped:true, maxResults:1200}`——数据源**明写总数不精确、结果集已封顶**；语言字段兜底枚举 `mul`(mixed) / `und`(undetermined)，元数据缺失时给 `null`。
- **判据**：3.35.0 ③ 的前两形态（父级复制 / 家族求和）都**要横向比对才能识破**；本形态不需要——数据源主动挂了「我不精确」的标签。**判据顺序因此改写：读任何计数，先看有没有自认不精确／封顶标记；没有，才需要去同族比对。** 附带：兜底枚举（`mul`/`und`/`null`）本身就是「这份元数据不完整」的明示，不能当真实值参与排序。
- 提升层：工具。触发词：totalIsExact、isCapped、自认不精确、封顶标记、mul、und、目录数字失真第三形态。

## 机器读端点的探测次序：robots.txt 的 Allow 行 → 站点自述 /api/llms.txt → 才轮到猜端点（来源：skillsmp.com/robots.txt 与 /api/llms.txt 2026-09-28 r283-B 独立 curl 实拉全文核验）
- **实证**：`robots.txt` 对 `ClaudeBot` 明写 `Allow: /api/llms.txt`、`Disallow: /api/`、`Disallow: /api/github-contents`、`Disallow: /auth/`、`Crawl-delay: 5`；顺着 `Allow` 那一行取到的 `/api/llms.txt` 是**站点自述的机器读契约**：「REST API for searching and discovering **3M+ Agent Skills**」，匿名 50/天·10/分钟、API Key 500/天·30/分钟、`Daily counters reset at 00:00 UTC`、限额只作用于 `/api/v1/skills/search` 不作用于 `/mcp`；MCP 面 `POST /mcp` 无鉴权、「There is no daily MCP quota」，但 **Ingress 50 POST/10s/IP × valid tool call 30/60s/IP，且 "A valid tool call consumes **both** ingress and tool-call capacity"**，「On HTTP 429: honor Retry-After」。
- **判据**：抓外部站时**先读 robots 的 Allow/Disallow 与站点自述 llms.txt，再猜端点**——一次就能拿到配额、鉴权、端点全集，而不是反复试错。**额度分层是相乘不是相加**：一次有效调用同时扣两层，只盯一层会算错容量。
- **落地动作**：新建信源时固定三步：① `robots.txt` 找 Allow 行里的机器读入口；② 取 `/llms.txt`、`/api/llms.txt`、`/openapi.json`；③ 把配额/鉴权/429 处理写进抓取脚本再开始批量拉。
- 提升层：工具。触发词：robots.txt Allow、api/llms.txt、站点自述契约、机器读端点、探测次序、额度相乘、429 Retry-After、Crawl-delay。

## 最小自证机检：把「声明数」钉死到「表内求和」，双语各验一次（来源：full-stack-skills `scripts/validate_catalog.py` + `.github/workflows/catalog-check.yml` 2026-09-28 r283-B 经 Qoder r316-Q-A 实拉取证；与 sa 3.35.0 ③ 互为正反）
- **实证**：30 行脚本做的事——`repositories.txt` 必须 **sorted and unique**；只统计表格中 label==repository 的行；做 **duplicate / missing / unexpected 三集合比对**；正则抓 README 标题里的声明数字，断言 `declared_packages == len(inventory)` 且 `declared_skills == sum(表内计数)`；**`README.md` 与 `README.en.md` 双语各跑一次**；成功打印 `README.md: 50 packages, 774 skills`。
- **判据**：sa 3.35.0 ③ 教「怎么识破别人目录数字失真」，本条是反面——**用最小 CI 把自己目录的声明数与表内求和钉死**。它的边界也说清楚：**只校验可数一致性，不校验技能质量**——别把它当成质量门。
- **落地动作**：任何"目录/清单/总表"类文件，挂三条断言：条目排序且唯一、声明总数 == 条目数、声明分项和 == 各表求和；多语言副本逐份各验。
- 提升层：可复用 Skill。触发词：自证机检、声明数、表内求和、sorted and unique、双语各验、catalog-check、可数一致性不是质量。

## 规范通过 ≠ 规范背书：合规检查只能证明"没犯它列的错"（来源：agentskills.io`/specification` 2026-09-28 r283-B 经 Qoder r316-Q-A 实拉取证；与 r312-Q-B「零执行面负声明」互补）
- **实证**：官方规范 optional 字段**全集只有 4 个**——`license` / `compatibility` / `metadata` / `allowed-tools`；全文**无 version 字段、无发布语义、无缓存语义、无依赖解析语义、无安全边界章节、无错误码语义**；失败语义唯一出处是 "Scripts should … be self-contained / include helpful error messages / handle edge cases gracefully"（should 级，非 MUST）。进披露预算倒是带数字（Metadata ~100 tokens / Instructions < 5000 tokens recommended / SKILL.md < 500 lines）。
- **判据**：一个技能**通过规范校验**，只说明它没犯规范列出的那几条错；**规范没写的维度（版本、依赖、安全边界、错误语义）等于没有背书**。与「零执行面负声明」互补：那条是被审对象自证，本条是**规范本身不提供担保**。
- **落地动作**：引用"符合 XX 规范"作为可信依据时，必须同时列出**该规范不覆盖的维度**，否则就是拿合规当质量证明。
- 提升层：可复用 Skill。触发词：规范不给担保、合规不等于背书、optional 字段全集、无 version 语义、无安全边界章节、should 不是 MUST。

## 「只看 description 判相关性」有系统性失准代价，正文级复筛要留口子（来源：arXiv 2603.22455《SkillRouter: Skill Routing for LLM Agents at Scale》2026-09-28 r284-B 独立拉 abstract 原文核验；**不推翻**渐进式披露三阶段，补的是它的精度代价侧）
- **实证**：约 **80K** 候选技能语料上，progressive disclosure（只暴露名字+描述、隐藏正文）导致**路由准确率掉 37–44 个百分点**；对照实验证明缺的信号是**正文驻留的**而非长度假象——正文蒸馏出的描述仍比全字段路由低 7–21 点，只训元数据的编码器低 **14.0** 点。作者方案 SkillRouter（1.2B body-aware retrieve-and-rerank）Hit@1 **74.0%**，参数少 **13×**、快 **5.8×**。
- **判据**：现有「扫清单 → 按 description 判强相关/无关 → 加载 1–3 个」的流程里，对**低频专业任务**与**边界模糊命中**必须保留一次**正文级复筛**（读 SKILL.md 头部再定去留），不得把「只看 description」当无损判定。反过来说，description 的写法目标是"让正文级复筛不必发生"——写不出这一点的 description 就该重写。
- 提升层：工作流。触发词：路由准确率、SkillRouter、只有描述不够、正文级复筛、boundary 命中、progressive disclosure 代价。

## 供应链审计证据要按「版本」挂载，不能用最新发布代查全部版本（来源：`api.skillhub.cn/api/v1/skills/<slug>/versions` 2026-09-28 r284-B 独立实拉 200，逐版本取回 `changelog/createdAt/securityReports`）
- **实证**：该端点返回每个版本各自带 `versionId/changelog/createdAt` + `securityReports` **双扫描器 `keen` + `sanbu`**，各含 `status`/`statusText`/`reportUrl`（实测样例 `tencent-docs`：两扫描器均 `benign`/"安全，无风险"）；sanbu 报告是 **sha1 预签名 URL**，带 `q-sign-time` 有效期。对照既有"三扫描器 / Skill Card"是**单次发布**口径。
- **判据**：升级技能或依赖版本时取**目标版本**的审计记录——"上一版 Clean"不构成新版担保，版本号一变就是新证据需求。预签名有效期意味着**证据会过期**：报告链接失效即视为**无证据**，不是"曾经查过"。
- 与既有内容寻址（r202-B，管 what）与 Ed25519 作者签名（r204-A，管 who）互补：本条管**哪个版本**。
- 提升层：工具。触发词：按版本取证、versionId、逐版本安全报告、预签名过期、上一版 Clean 不作数。

## 读第三方技能的脚本：消费侧默认动作是 `--help`，不是读源码（来源：github.com/anthropics/skills `skills/webapp-testing/SKILL.md` 2026-09-28 r284-C 经 raw 通道独立取正文核验 + agentskills.io《Using scripts in skills》独立实拉；与 §脚本契约五条（3.13.0，作者侧怎么写脚本）方向互补不重叠）
- **实证**：webapp-testing 正文原文——**"Always run scripts with `--help` first to see usage. DO NOT read the source until you try running the script first and find that a customized solution is absolutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window."**；agentskills.io 同向规定脚本按**黑盒**使用、`--help` 是 agent 学接口的主途径。
- **判据**：3.13.0 管的是"作者把脚本写成什么样"，本条管"**拿到别人的脚本你怎么读**"——先 `--help`，跑不通或确实需要定制才读源码，且读之前先想清楚要改哪一行。**脚本是上下文污染源**，整份读进上下文是纯浪费。
- 提升层：工作流。触发词：先 --help、不要读源码、黑盒脚本、上下文污染、脚本怎么读。

## 「改完技能正文，当前会话会不会生效」是跨客户端实现差异，取最小公分母（来源：agentskills.io《How to add skills support to your agent》2026-09-28 r284-C 独立实拉；并入 §跨客户端最小公分母（3.35.0）作为新实例）
- **实证**：规范写明正文**可在发现时缓存、也可在 activation 时才读**（"reading it at activation time"），并支持**跨激活热更新**与重复激活 **skip re-injection**；而 WB 自有 r175-C 已落「渲染正文进入即常驻、后续轮次不重读文件」。**同一行为两说**。
- **判据**：**不要假设技能正文修改在当前会话内生效**——改完技能要**新开会话复验**，否则会把"实现没重读"误判成"我改错了"。写技能时同理：不要在正文里写"如果你刚改过我，请重新读我"这类依赖客户端行为的指令。
- 提升层：可复用 Skill。触发词：改完技能没生效、会话内热更新、activation 时读正文、最小公分母、新开会话复验。

## 解析器要有「格式降级重试」，且自由文本字段不是能力契约（来源：agentskills.io`client-implementation/adding-skills-support.md` 2026-09-29 r285-A 独立实拉全文核验）
- 未加引号的冒号会让 YAML 解析失败（原文示例 `description: Use this skill when: the user asks about PDFs`），处置是**包引号或改 block scalar 后重试**，不是直接报错——大量跨客户端失配源于标点而非语义。
- `compatibility` 是 500 字符自由文本、`allowed-tools` 官方自标 Experimental 且跨宿主实现有差异 → **两者都不能当门禁判据**；`metadata` 是唯一安全扩展位（自定义键名要够独特防冲突）。
- 与 §跨客户端最小公分母（3.34.0）互为正反：那条管"别依赖私有特性"，本条管"解析层要容忍别人的不合规"。

## 技能校验失败要分档：可容忍缺陷告警后照常加载，致命缺陷才丢弃（来源：同上，2026-09-29 r285-A 独立实拉）
- 宽松校验表：`name` 与目录名不匹配 / 超 64 字符 → **warn, load anyway**；`description` 缺失或 YAML 完全不可解析 → **skip the skill**。禁止"一律跳过"或"一律加载"两个极端。
- 被过滤的技能要**从目录整条隐去**（原文 "Hide filtered skills entirely"），而不是列出来在激活时拦——否则模型会反复去试一个不该存在的入口。
- 项目级技能的加载前置是**仓库信任判定**（gating on a trust check），不是内容检查：防的是不可信仓库静默注入指令。
- 与 AV §闸门自带拦截计数（2.46.0）不同轴：那条管"拦下要留痕"，本条管"丢弃要分档 + 可见面要清干净"。

## 从分发清单里删 ≠ 停止分发：删除会传导到用户机器，改名必须留映射（来源：Claude Code `plugins/marketplace-reference`，2026-09-29 经 Qoder r319-Q-A 实拉取证；**WB 本轮该 docs 通道未达，按引文落地并标注待复核**）
- `forceRemoveDeletedPlugins:true` 原文语义＝"你从清单里移除的插件会在用户机器上被卸载"——**删除有两个必须显式选的语义**（保留已装 / 传导卸载）。
- `renames`（former→current，映射到 `null` 表示不迁移）＝改名不留映射会把旧名位空出来供仿冒；仿冒被处理时"卸载其插件**并删除已保存数据**"（数据不是附属物，是同生共死）。
- 与 §下架语义择一（r312-Q-B）相邻：那条立原则，本条给字段位与后果实证。

## 黑白名单门禁必须写明求值次序，且策略按会话起点重算（来源：同上；待复核同前）
- `blockedMarketplaces` 原文 "checked before the allowlist"——**拒绝类先于允许类**必须写进文档，否则"既在拒绝又在放行"未定义。
- 策略在**每次 session start 重算**（改门禁后旧会话不受影响）；`strictKnownMarketplaces:[]` 是最大封禁而非"不限制"；`enabledPlugins:false` 同时屏蔽并隐藏。
- 与已落「空数组语义要显式声明」同族：空值不是"没配"，往往是最强档。

## 收敛式停机三档门：技能正文要写清「何时算写完」（来源：anthropics/skills `skills/doc-coauthoring/SKILL.md` 2026-09-29 r285-B 独立取正文核验）
- 原文三档：① `3 consecutive iterations with no substantial changes` 才允许收束；② 进阶门＝"questions show understanding - when edge cases and trade-offs can be asked about"；③ 终态＝**模拟读者验收**（Reader Claude consistently answers questions correctly），不是作者自评。
- 与既有「必须配 max iterations」反死循环门（r190A，数量层面）分层：那条防跑不完，本条防**收敛了但其实没到位**。

## description 的反向禁令：不得写流程步骤（来源：addyosmani/agent-skills `docs/skill-anatomy.md`，2026-09-29 经 Qoder r322-Q-A 实拉取证；**WB 本轮 raw 通道 000，按引文落地并标注待复核**）
- 原文："Do not summarize the workflow — if the description contains process steps, the agent may follow the summary instead of reading the full skill."
- 机制＝描述含步骤会诱导模型按摘要执行，**绕过渐进披露第二层的全文加载**——"把正文写进元数据"会瓦解披露设计本身。
- 与正向规格（what + Use when / 第三人称 / ≤1024）互补：那是"要写什么"，本条是"多写了什么会坏事"；与 §description 三问（3.36.x）同节并读。

## 技能有保质期：再审计要固定周期，并在扫描器或模型变更时立即触发（来源：K-Dense-AI/scientific-agent-skills README 2026-09-29 r285-B 独立取正文核验）
- 原文："full rescan of everything at least every 30 days and whenever the scanner or model changes"；日常为每周增量扫，未变更条目沿用上次结论。
- 配套：改正文必须 `Increment metadata.version`；新增打包脚本必须带 `tests/`（CI 拦下无测试的 PR）；并过 canonical `skills-ref validate`。
- 与 §审计证据按版本挂载（3.43.0）分工：那条解决"何时留证据"，本条解决"多久必须重看一次"——只挂证据不设周期，旧版的 Clean 会被当成永久担保。

## 工具访问控制的判定依据应是「操作元属性」而非工具名（来源：arXiv 2609.31039 MetaPermit + 2602.12430v4，2026-09-29 经 Qoder r321-Q-C 实拉取证；**WB 未独立复核，按引文落地并标注待复核**）
- 现状是按**工具名/命令名单**判危险，新工具名一出现即漏判；改为属性组合：**是否外发 / 是否写盘 / 是否删除 / 是否需凭证 / 是否不可逆**。
- 判据：工具名只是属性的载体；新增技能或工具时**只需标属性即自动纳入闸门**，不用回改名单。
- 与豆包权限四档、guild 1.12.0（HITL 锁在执行通道层）、SA 2.65.0（无旁路）分工：那几条管"在哪拦/分几档"，本条管"按什么判"。


## 升级策略要写成可选档位而不是开关，且对外标识符发布即冻结（来源：Dify 官方 llms-full.txt「Integrations / update strategy」2026-09-29 r286-A 独立实拉 2.99MB 全文核验 + Activepieces 官方仓 `.agents/skills/piece-builder/SKILL.md` 经 cdn.jsdelivr.net 取原文核验）
- Dify 原文："Each category ... has its own update strategy (off, patch versions only, or always the latest), applied to every integration in the category or a chosen subset."——**三档 + 可按类别或子集分别施加**，比「钉版 vs 滚动」二选一多一个中间档（只滚 patch）。
- Activepieces 原文："Action/trigger `name` fields are permanent — never change them after publishing; flows store them by name."——**对外标识符发布即冻结**，下游按名持久引用，改名等于断链。
- 判据：任何「要不要自动更新」的答案都不该是布尔——先给三档，再问受众面（全类别 / 子集）。与 §破坏性变更机械判定（3.39.0）分工：那条判「什么算破坏」，本条给「以什么节奏接受变更 + 什么永不许变」。


## 钩子 / 扩展是「进程内受信代码」不是沙箱脚本：入口面与事件面是两个独立开关（来源：docs.openclaw.ai《Hooks》2026-09-29 r286-B 独立实拉原文核验）
- 原文："Internal hooks are trusted code, not sandboxed scripts."——与「装来的第三方脚本」是两套威胁模型；同页并列 "These are separate systems. `hooks.internal` configures ... event handlers; `hooks.enabled` configures HTTP ingress."，**入口开关与事件处理器开关互不替代**。
- 判据：任何"插件 / 钩子"类扩展先分两类——**进程内受信代码**（拿宿主全权限，只能靠来源审查与安装门禁）vs **沙箱脚本**（可限权）；把前者按后者管＝限了个寂寞。
- 排障次序：钩子没执行时先分清查哪个面（入口 enabled 还是事件 internal），再谈逻辑。
- 与 §内容寻址 + Ed25519 签名（3.20.x）互补：那条管"装进来的是不是那份"，本条管"装进来之后它以什么身份在跑"。


## 目录数字失真第三形态：同一页混用两种聚合口径（来源：skills.sh 首页 2026-09-29 r286-C 独立实拉原文核验 + agentskills.io/clients.md 同轮实拉）
- 实测同页两个数字：站标 **All Time (1,467,427)**＝收录技能数；榜首 `find-skills` 的 `"installs":3607107`（3.6M）＝安装次数。**3.6M > 1.467M**，即"榜首比全站还多"——不是数据错，是两个口径相邻展示且未标注。
- 识破法：引用任何目录数字前先问一句**"它统计的是对象还是事件"**（技能个数 / 安装次数 / 下载次数 / 仓库星数），再看榜首与总量是否同一量级。与 §父级复制 / §家族求和（3.35.0）合成完整三类，识破动作统一为"取 2+ 条目交叉比数字 + 问统计对象"。
- 附登记：agentskills `clients.md` 客户端清单实测 **46 个**（此前"40+"为估值，已精确化，不改结论只改口径精度）。
- 提升层：可复用 Skill（选型与证据引用）。触发词：口径混用、收录数 vs 安装量、榜首大于全站、数字失真。


## 沙箱内自装的工具不进清单，且「能不能用起来」取决于模型档位：声明式依赖清单 ≠ 实际可执行面（来源：docs.dify.ai `llms-full.txt`《New Agent》2026-09-29 r288-C 独立 curl 实拉全文核验）
- 原文："Beyond the Dify tools you add here, the agent can also install and run command-line tools on its own inside the sandbox when it needs one. **Those tools don't appear in the Tools list.**"；agent 自带沙箱 20 GB 存储，"it runs commands, installs programs, and reads and writes files"，环境变量经 Advanced Settings 注入供沙箱内读取。
- 原文（模型耦合）："Older models often can't make full use of the sandbox: a common symptom is an agent that **never runs commands or installs tools, even when the task needs it**."
- 判据：① **工具/依赖清单不等于可执行面**——凡有沙箱或运行时自装能力的系统，审计必须多问一层"运行时又装了什么"，声明式清单只能覆盖**声明那一刻**的面（与 3.20.0 依赖清单互补：那条管怎么声明，本条管声明之外的隐形面）；② **能力是否生效取决于模型档位**，且失效形态是**静默不作为**（从不调用），不是报错——验证沙箱/工具能力时要专门造"非调用不可"的题，而不是看有没有报错（与 AV 2.54.0 评测题契约同向）。
- 提升层：工具/模型。触发词：自装工具、不进清单、可执行面、旧模型用不好沙箱、静默不作为、sandbox 20GB。

## 市场分类目录是带版本号的受控词表：按 key 引用、active=false 是软下架、sortOrder 稀疏留插入位（来源：api.skillhub.cn/api/v1/categories 2026-09-29 r290-A 独立 curl 实拉，1632B JSON；与 §r211-C 目录分类轴 互补——那条管"用什么轴编目影响可发现性"，本条管"分类本体自身的工程语义"）
- 原文字段：13 个一级分类，每个含 `key` / `level:1` / `version:2` / `sortOrder`（0,10,20…120，步长 10）/ `active:true` / 中英双语 `name`+`nameEn`；技能详情侧只存 `category:"office-efficiency"` + `subCategories:[{key:"office-doc",name:"文档处理"}…]`（二级独立 key）。
- 判据：① **分类是会被修订的资产**——本体带 version，集成一律按 `key` 引用，绝不按 `name`（中英双名会任一改动）；② `active:false` 是**软下架不是删除**，聚合统计要过滤，否则把已撤分类下的技能算进总量；③ `sortOrder` 步长 10 是**显式留出的插入位**，排序顺序本身是产品决策，不要当成稳定序号写进自己的映射表。
- 提升层：工具/工作流。触发词：分类 key、分类版本、active 软下架、sortOrder 步长、二级分类、受控词表。

## 平台侧会主动声明机器消费边界：llms.txt 不只给可引用描述，还点名"不应被索引"的页面（来源：skillhub.cn/llms.txt 2026-09-29 r290-A 独立 curl 实拉 1434B；与 §3.42.0 机器读端点探测次序 互补——那条管"消费方怎么找"，本条管"供给方声明了什么"）
- 原文：文档分「核心入口 / 安装与验证 / **可引用描述** / **抓取边界**」四段；抓取边界明写"以下为登录态页面与管理后台，**不应被索引或引用**"并列出 /dashboard、/enterprise/dashboard、/team-skills、/admin，末尾指向 robots.txt 与 sitemap.xml。
- 判据：① 先读平台自己的 `/llms.txt` 再抓——它同时给出**鼓励引用的口径**（官方措辞，可直接引）与**禁抓清单**，绕过它自行全站抓既低效又踩边界；② 把"禁抓清单"当成平台的**权限面地图**：被点名的路径就是需要凭据的区域，做集成时这些面默认不可用，不要设计依赖登录态的采集链路。
- 提升层：工作流/工具。触发词：llms.txt、可引用描述、抓取边界、不应被索引、禁抓清单、sitemap。

## 身份可信度是三个可独立分叉的字段：来源、组织认证、作者认证、认领态（来源：api.skillhub.cn/api/v1/skills/tencent-docs 详情 2026-09-29 r290-A 独立 curl 实拉 3474B；与 §r209-A 来源标签先于内容判断 互补——那条管"先看哪一类"，本条管"同一条记录内三个信号会互相矛盾"）
- 原文：`skill.source:"enterprise"` + `publisher.verified:true`（`certifiedName:"腾讯科技（深圳）有限公司"`、`orgId`）+ `skill.isAuthorVerified:false` + `authorVerifiedHandle:null` + `claim_state:"unclaimed"` / `claimable:false` / `claimed_user_handle:null`。
- 判据：**企业发布 ≠ 作者已认证 ≠ 已被认领**——同一条记录里组织已认证而作者未认证、且无人认领是完全正常的组合；判可信度要看**字段组合**而不是任一枚徽章，且"未被认领（unclaimed）"意味着没有人为这份内容负责，出问题时找不到责任主体，应单独降一档。
- 提升层：工具/模型。触发词：publisher.verified、isAuthorVerified、claim_state、unclaimed、组织认证、作者认证、字段组合。

## 目录数字失真第四形态：同一条目内部四个指标量级差可达两个数量级（来源：同上详情；与 §r211-C 两种失真形态（父级复制 / 家族求和）互补——那两条是跨条目口径，本条是同条目多指标）
- 原文：`stats: {downloads: 1287043, installs: 8107, stars: 311, versions: 22}` —— 下载:安装 ≈ **158:1**，下载:收藏 ≈ 4137:1。
- 判据：**同一条记录里的 downloads / installs / stars 不是同一个动作的三种说法，而是漏斗的三段**；拿 downloads 当 popularity 去和别家的 installs 排序，等于拿曝光量比留存。引用任何单一数字前先问"这个数字统计的是对象还是事件"（§r286-C），再问"它在漏斗哪一段"。
- 提升层：模型/工具。触发词：downloads、installs、stars、量级差、漏斗、单数字不可比。

## 技能的分发形态决定版本绑定语义：library 技能默认跟随最新版，embedded 技能才钉在包里（来源：docs.dify.ai `llms-full.txt`《Skills》2026-09-29 r294-A 独立 curl 实拉 2.99MB 全文核验；与 §r286-A 升级策略三档 互补——那条管"宿主允不允许自动升"，本条管"消费侧拿到的到底是哪一版"）
- 原文："You can keep up to 500 skills in the library and share them workspace-wide. When you publish an update to a skill, **every agent that uses it picks up the latest version**."；"You can add **up to 20 library skills** to an agent, and it follows the latest published version of each."；embedded skill = "one the agent keeps to itself"，包内需含 `SKILL.md`，默认 ≤50 MB（`UPLOAD_SKILL_FILE_SIZE_LIMIT` 可调）。
- 判据：① **同一平台内两种打包形态的版本语义是相反的**——共享库技能是"活引用"（上游发布即全网生效，作者改一行，所有引用它的 agent 行为当场变），嵌入技能是"死快照"（行为随包固定，升级要重新打包分发）；做能力治理时先问"这条引用是活引用还是死快照"，活引用必须配变更告知（§3.30.0 向下告知义务），否则上游一次静默改动就是一次全下游事故；② **配额是三个互不相干的维度，别混着说**——库存容量（500）、单 agent 挂载数（20）、单个包体积（50MB），任一项触顶的处置动作完全不同（清库 / 拆 agent / 拆包），报"技能满了"之前先指名是哪一层。
- 提升层：工具/工作流。触发词：library skill、embedded skill、跟随最新版、活引用、死快照、500 上限、20 上限、50MB 包。

## 关掉市场是「切断增量」不是「切断存量」：一条开关的四条连锁要逐项列清（来源：同上 `MARKETPLACE_ENABLED` 环境变量说明，2026-09-29 r294-A 独立实拉核验；与 §r285 RM 1.22.0「发布可部分生效非布尔」同向，本条给的是断供面的完整清单）
- 原文：禁用后 ① 控制台隐藏浏览与安装入口；② API 拒绝 Marketplace 插件的**安装与升级**；③ 周期升级检查（`ENABLE_CHECK_UPGRADABLE_PLUGIN_TASK`）停止；④ "**Already-installed plugins keep working**, and installing from GitHub or a local package stays available when permitted by the installation policy."；另有"Template import itself is unaffected. However, if an imported template requires Marketplace plugins that are not already installed, **those dependencies cannot be installed while Marketplace is disabled**."
- 判据：① 把"关开关"当**状态转移**写清四条边——入口面（看不见）、安装面（装不了）、**升级面（已装的也升不了，这条最易漏，等于把存量钉在旧版还停止了漏洞修复）**、存量面（继续跑）；② **断供 ≠ 停服**——已装组件继续工作，所以"禁用市场"后不能假设能力立刻消失，也不能假设还能打补丁；③ **模板依赖是断供的隐性受害者**：模板本身能导入，但它依赖的市场插件装不上 → 导入成功≠可运行，验收模板必须跑到依赖解析完成。
- 提升层：工作流/工具。触发词：MARKETPLACE_ENABLED、市场禁用、断供、已装继续工作、拒升级、模板依赖装不上。

## 规范的「最小合规面」只有 name + description：官方模板实证，且未替换的占位文案是可机检的低质信号（来源：anthropics/skills 官方仓 `template/SKILL.md` 2026-09-29 r294-B 经 cdn.jsdelivr.net 实拉 140B 全文；同轮 `data.jsdelivr.com` 文件树枚举 17 个技能无新增，附带核验）
- 原文（全文）：frontmatter 仅 `name: template-skill` + `description: Replace with description of the skill and when Claude should use it.`，正文仅一行 `# Insert instructions below`。
- 判据：① **规范强制的字段只有两个**（name / description），其余（许可证、版本、allowed-tools、metadata…）都是**宿主或团队的附加约定**——写门禁时不要把附加约定说成"规范不合规"，更不要把规范之外的必填项塞进"合规检查"；② 官方模板自带**未替换占位文案**（`template-skill`、"Replace with description"），这给出一个零成本机检项：**技能名含 `template`/`example`/`placeholder`，或 description 以 "Replace with"/"TODO" 开头 = 直接判未完工**，不必读正文；③ 反过来自建模板也该保留这种"一看就知道没改"的占位串，让漏改在上架前就被机器抓到，而不是靠人工评审。
- 提升层：工具/工作流。触发词：官方模板、最小合规面、只有 name 和 description、占位文案、template-skill、未完工机检。

## SecretRef 只承载静态凭据：OAuth 凭据禁止走引用，因为可变状态不能跨存储分裂（来源：docs.openclaw.ai《Auth credential semantics》"OAuth SecretRef Policy Guard" 2026-09-29 r294-B 独立 curl 实拉 24,733B 核验；与 §3.20.0 声明式依赖清单 requires.env/SecretRef 互补——那条管"怎么声明"，本条管"哪些凭据不许声明成引用"）
- 原文："SecretRef input is for **static credentials only**. OAuth credentials are **runtime-mutable** (refresh flows persist rotated tokens), so SecretRef-backed OAuth material would **split mutable state across stores**."；profile 凭据 `type:"oauth"` 或 `mode:"oauth"` 时，任何凭据字段上的 SecretRef **一律拒绝**，且"Violations are **hard failures (thrown errors)** in startup/reload secret preparation and profile resolution paths."
- 判据：① 判据不是"这个秘密够不够敏感"，而是**"这份凭据会不会被运行时改写"**——静态密钥（API key / token）适合放外部引用并集中轮换；会自我轮换的凭据（OAuth refresh token、短期会话凭据）必须与能写回它的运行时同处一处，否则两个存储各持一份、轮换后必然分叉，且分叉形态是"一边新一边旧"的静默不一致；② 违规必须**硬失败**（启动/重载期抛错）而不是告警降级——这类错误放行了就等于埋了一个随时生效的双向不一致；③ 推广到技能侧：技能声明"我需要某个凭据"时，要同时声明**该凭据是否可被引擎写回**，可写回的不允许外置引用。
- 提升层：工具/模型。触发词：SecretRef、OAuth 禁用引用、runtime-mutable、可变状态跨存储分裂、hard failure、凭据轮换分叉。

## 市场安全审计要给「状态」与「爆炸半径」两个独立轴，且官方必须写明"通过不是担保"（来源：docs.openclaw.ai《Security Audits》ClawHub 2026-09-29 r296-B 独立 curl 取 .md 原文 5,974B 核验；与 §3.22.0 四档可信度、§3.36.1 自评式低质信号 互补——那两条管"内容可信吗/质量如何"，本条管"装了它最多能造成多大破坏"）
- 原文六状态：`Pass`（"No visible issue above low risk was found"）/ `Review`（"Read the findings before installing. The release may still be legitimate."）/ `Warn`（"high-impact concern or warning signal"）/ `Malicious`（"Do not install."）/ `Pending`（"Audits have not finished yet."）/ `Error`（"The audit could not be completed."）；并明示："Audits are strong safety signals, but they are **not a guarantee** that a release is risk-free. Always use judgment before granting sensitive access."；"**A `Pass` is reassuring, but it does not replace your own judgment.** This matters most for tools that can publish content, edit data, run commands, read files, or access production systems."；风险等级定义："Risk level describes **blast radius**: how much power the release appears to have **if you use it as intended**."
- 判据：① **「有没有问题」与「能造成多大破坏」必须分成两个轴**——状态轴回答"扫描发现了什么"，风险/爆炸半径轴回答"按它的设计正常使用时，它手里有多大权力"；一个没有恶意但能发内容、改数据、跑命令、读生产系统的技能，状态可以是 Pass 而爆炸半径极高；只看状态会把"干净但权力很大"误判为"可以放心装"；② **"按预期使用"是风险的定义前提**——风险等级衡量的不是"它有多可能被滥用"，而是"你照着它声明的用途用，它能碰到什么"；评估第三方技能时先读它**声明要哪些凭据/权限/环境变量**（官方列为安装前必查项），再决定这个权力面能不能接受；③ **通过不等于担保，且官方必须自己把这句话写出来**——审计方主动声明"不替代你自己的判断"是可核验的诚实信号（与 §3.36.1 作者自评相反：作者自夸是低质信号，审计方自限是高质信号）；④ **Pending 与 Error 是两种不同状态，不能都当"未知"处理**——Pending 是还没扫完（可以等），Error 是扫不动（需要别的手段），把两者混成一个"未判定"会让人一直等一个永远不会完成的结果。
- 提升层：可复用 Skill / 安全边界。触发词：安全审计状态、blast radius、爆炸半径、按预期使用的权力、Pass 不是担保、Pending vs Error、安装前必查权限。

## 技能须声明式写清运行依赖，且依赖缺失校验报告必须「绕开消费侧白名单」独立出具（来源：docs.openclaw.ai《skill-format》+ cli/skills `skills check` 2026-09-29 r334-Q-A 实拉核验；与 §声明式依赖清单 requires.env/SecretRef 互补——那条管"怎么声明"，本条管"声明缺失后校验报告能否被消费侧遮蔽"）
- 原文：技能 frontmatter 用 `requires.env` / `requires.bins` / `requires.config` 写明运行前提；`skills check` 校验依赖缺失时，**报告不被 agent 侧的技能白名单遮蔽**——即使某技能在白名单里被放行，依赖缺失依然独立报出。
- 判据：① 依赖声明是「机器可读的前提契约」，让装技能的环境在加载前就能算出"我缺什么"；② **校验报告必须独立于消费侧准入**——白名单决定"这个技能能不能用"，依赖检查决定"这个技能在当前环境能不能跑起来"，两者职责不同；若依赖缺失的报错被白名单的"已放行"状态盖掉，技能会在异机静默失败（用户看到的是"已授权"，实际跑不起来）；③ 写技能时把"我需要什么"显式声明，并把缺失校验设计成**不被上层放行逻辑吞掉**的独立信号。
- 提升层：工具/可复用 Skill。触发词：requires.env/bins/config、依赖缺失不受白名单遮蔽、skills check 独立报缺、异机静默失败、声明式运行依赖。

## 改变技能解析/安装源的优先级必须显式确认，不得静默把新市场设为优先源（来源：skillhub.cn/install/skillhub.md 首接入问答门槛「是否将 SkillHub 设为优先技能安装源」2026-09-29 r334-Q-A 实拉核验；与 §抓取边界声明 互补——那条管"哪些页不该被索引"，本条管"选谁当默认源要人拍板"）
- 原文：SkillHub 首次接入时有一个**显式确认门槛**——是否将其设为「优先技能安装源」需要用户确认，而不是安装流程默认就把它顶到最高优先级。
- 判据：① 安装源的优先级 = 技能的**解析与信任根**——谁优先，谁的技能就被默认加载、谁的签名/审核口径就成了事实标准；把新市场静默设成优先源，等于未经确认就把解析权交出去；② 这是**解析源劫持**的入口：一个被静默提权的市场，可以把自己仓库里的同名/仿冒技能顶掉你原本信任的来源；③ 任何"换默认源/加优先源"的动作都要做成**显式确认门**，确认项里写清"设成优先源后，原本的 X 源降为次选"。
- 提升层：工作流/安全边界。触发词：优先安装源、解析源劫持、显式确认门、静默提权安装源、首接入确认门槛。

## 技能信任按「来源 provenance → 分级部署权限」做四层 gate 门控；社区贡献技能有实测漏洞基线（来源：arXiv 2602.12430《Agent Skills for LLMs: Architecture, Acquisition, Security》Xu & Yan，2026-09-29 r337-Q-A 实拉；与 §市场安全审计状态/爆炸半径 互补——那条管"装一个的破坏面"，本条管"谁写的、能部署到哪一级"）
- 原文：提出 **Skill Trust and Lifecycle Governance Framework**——four-tier, gate-based permission model，将技能 provenance 映射到分级部署能力（来源越可信，允许自动部署的等级越高）；实证「**26.1% of community-contributed skills contain vulnerabilities**」。
- 判据：① 技能准入不能只有"能跑/不能跑"一档，要按**来源可信度分档授权**——官方/已签名/高 provenance 的技能可自动部署到更高权限等级，匿名社区贡献的技能只放行到受限沙箱；② **26.1% 漏洞率是基线事实**，不是吓人——意味着"从社区拉个技能直接用"的默认动作本身就带 ~1/4 的中招概率，写技能/装技能时默认走隔离与最小权限；③ 把 provenance 当成**一等治理字段**：技能卡上标清"谁发布、有没有签名、过了哪级 gate"，让调用方据此决定部署等级，而不是每个用户自己重新评估。
- 提升层：可复用 Skill / 安全边界。触发词：provenance、四层门控、分级部署权限、26.1% 漏洞率、技能生命周期治理。

## 技能「调用面 ≠ 入口面」：user-invocable:false 仍可被模型调用，加载源有显式优先级链…（原文已下沉 references/knowledge-base.md §L481）
## 技能进化不要自由变异，要「分解进固定能力空间 + 定向修订」…（原文已下沉 references/knowledge-base.md §L486）
## 技能控制流外置为显式状态机（EFSM）：知识与控制流分离，用显式状态转移替代模型猜下一步（细则见 KB，2026-09-30 r320A 下沉）

## 卸载必须留「显式卸载」marker（enabled: false tombstone），阻断启动修复静默重装；重装不静默恢复启用（来源：docs.openclaw.ai cli/plugins/uninstall-and-update，2026-09-30 r320A 实拉）

## 撤销与审核分层：吊销只阻断后续发布、不推翻既有审核结论；恢复走 successor 重跑检查并保留失败尝试为审计史…（原文已下沉 references/knowledge-base.md §L495）
## 修订整包不可变且发布只对新会话生效、陈旧编辑报冲突不覆盖；「加载位置」与「谁能看见」是两个独立控件且子级列表非空即整体替换；硬平台过滤不可被 always 豁免（来源：docs.openclaw.ai/tools/skills.md，2026-09-30 r321A 独立实拉 39,741B；细则见 references/knowledge-base.md §r321A）
## 并发写仲裁三件套（陈旧写报冲突 / 相同保存 no-op / 会话钉修订）与幂等契约四元组（键作用域·占用时点·失败是否回放·保留期）；代理不得自动重试非幂等请求（来源：docs.openclaw.ai/tools/skills.md 39,705B + docs.stripe.com 1,336,845B + RFC 9110 §9.2.2 502,941B，2026-09-30 r322C 独立实拉；细则见 references/knowledge-base.md §r322C）

## Agent 评测与基准 2026：评测数据三来源/评测集版本化/judge 校准/双评分/CI 分层/工具五维/成本延迟/harness 层/轨迹六指标/多 agent 协作…（原文已下沉 references/knowledge-base.md §L502）…（原文已下沉 references/knowledge-base.md §L502）
## 身份级仲裁三件套：持久身份复用免重排 / 同身份第二实例被罚出 / 身份+序号二元组去重——并发去重要先有身份，再谈序号（来源：kafka.apache.org/43/design/design/ 146,232B，2026-09-30 r323B 独立实拉；与 §并发写仲裁三件套/§幂等契约四元组 互补——那条管“写冲突怎么判”，本条管“谁算同一个写者”）
- 原文：「group members to provide **persistent entity ids**. Group membership remains unchanged based on those ids, thus **no rebalance will be triggered**」；「a **fencing mechanism on broker side** will inform your duplicate client to shutdown immediately by triggering a `FencedInstanceIdException`」；「the broker assigns each producer an ID and **deduplicates messages using a sequence number**」。【通道根因】旧 `/documentation` 单页已改 Hugo 跳转壳，此前“57KB 内 0 命中”是**载体改版**而非内容不存在；正确锚点 = `/43/design/design/#static-membership`（KIP-345 静态成员）。
- 判据：① **去重的先决条件是身份，不是序号**——没有稳定身份，“序号从几开始数”没有意义；先给每个写者一个持久 ID，重连才不会被当成新人触发全量重排（rebalance）；② **身份冲突的罚则必须落在仲裁方而不是写者自律**：同身份出现第二实例时由服务端主动踢出并给出具名异常，而不是让两个实例各写各的、靠事后对账才发现；③ **序号只在单一身份内部有效**（producer id + sequence number），跨身份的重复它看不见——声明幂等范围时必须连“键的作用域”一起写。
- 提升层：工具/工作流。触发词：持久身份、static membership、fencing、FencedInstanceIdException、序号去重、身份先于序号。


## 审批门要配齐四个旋钮（启用选择器 / 豁免主体 / 在途隔离 / 超时去向）；缺第四个时 pending 可无限挂起（来源：www.activepieces.com/docs/flows/flow-approvals.md，2026-09-30 r323C 独立实拉 2,500B；与 §并发写仲裁 互补——那条管“写冲突”，本条管“变更放行”）
- 原文：启用选择器「Project Settings → General → toggle **Sensitive Project**」；豁免主体「**Admins publish directly — the gate is skipped for them.**」；在途隔离「The previously published version **keeps running** while the request is being reviewed」；撤回「**Withdraw** the request…while it’s still [pending]」。**缺位反证**：全文无任何 expiration / timeout / TTL 字样。
- 判据：① 门不是一个开关而是**四个旋钮**——谁来开（启用选择器）、谁能绕过（豁免主体）、等待期间跑哪个版本（在途隔离）、超时后怎么办（去向）；只实现前三个的门，默认行为是“永远挂着”，而这通常不是设计意图而是漏项；② **豁免主体必须显式写出是谁**：此处管理员是完全跳过而非预审放行，把“谁可以不走门”写成显式配置，否则门会被未声明的角色绕过去；③ **在途隔离是门的可用性前提**——审批期间旧版本继续服务，变更才敢进审批流，否则审批等于停机；④ 引用任何“已有审批”前先查它有没有超时兜底，**没有超时兜底的审批门等于可选否决权**。提升层：工作流。触发词：审批门、Sensitive Project、Admins publish directly、在途版本继续跑、pending 无超时、豁免主体。
