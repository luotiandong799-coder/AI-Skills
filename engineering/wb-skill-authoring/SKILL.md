---
name: wb-skill-authoring
description: >-
  Skill 的写法与体检：触发词设计、description 质量、文件拆分、跨工具迁移、安装前安全审查、安装后接线、触发评测盲测、no-skill 对照、效果归因、重复技能的去重与合并流程。当新增 skill、改写已有 skill 的 description、排查"技能该触发却没触发 / 不该触发却触发"、拆分过长 SKILL.md、把 skill 迁移到不同 AI 工具（Claude Code / Codex / Gemini 等）、安装第三方 skill 前做安全检查、或装了技能却总用不上（没接线）时应用。只写与自身工作流相关的约束和步骤，不写通用方法论套话。触发词：技能没触发、装了没用、接线、skill 不生效、触发评测、盲测、诱饵用例、no-skill 对照、效果归因、技能无增益、技能抢触发、误触发、负向边界、不适用于、审计技能、技能过期、拼写错误、乱码、失效工具名、重复触发、技能快速路径表、双路由、meta-router、description 上限、name 规范、快照基线、触发率、近失、指令改写、改了指令还是不行、改了两遍还是这样、调指令算修了吗、别再加一句必须、拆技能、技能合并、技能去重、查重、技能素材来源、gotchas、控制度校准、给默认不给菜单。、规则该写多少、AGENTS.md 变长、allowed-tools 是限制吗、禁用工具、权限叠加、停用还是删除、参数分发、万能技能、专用子代理、防递归、显式契约、靠推断、角色重叠、通才助手、示例与考题要不相交、自动放行的兜底层、硬禁清单、技能选择准确性评测、不需要却加载、选错 skill、评委团、集成必须留子分、ensemble、多评委同签名、judge_scores、可溯源、provenance、CI 出证、无旁路、禁读环境变量与文件系统、输入走显式参数、审计面等于参数表、一个包一个服务、代理层不受理、可重跑产物、脚本沉淀、不许硬编码结果、连跑两次存证、产物自带说明、persona 市场退场、GPT Store 停用、迁移为插件、优先可机读注册表、版本号不塞 description、双榜分离、社区热度榜、官方自研榜、创建者域名标注、匿名统一标签、纯 UI 信源不学、审计盲区、只记写不记读、传参值不入库、失败也留痕、跨面不同步、surface 能力面、按面降级、导航四信号、签名强度、显式调用跳过路由、@标识调用
version: 3.73.1
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

## 元数据字段三态语义 + 「改元数据即发新版」的批量副作用（来源：ClawHub publishing 本机实拉，r326C）
- **原文**：①「A skill first published without `--categories` is stored as **`other`**」；②「On a later publish, **omitting** `--categories` or `--topics` **keeps the values already stored**…Passing an **empty** value **clears** the field」；③「Passing either flag publishes **even when the files have not changed**, so fixing metadata this way creates a new patch version」；④ API 侧 flags 作用于本次运行的**每一个** skill 并**绕过 unchanged-skill 跳过**（「supply `skill_path` to bound that to one skill」）。跨平台对照：Make data-stores PATCH「Any property that is not provided will be **left unchanged**」。
- **判据**：① 同一字段**三种输入三种结果**：首发缺省→兜底值、后续省略→**保持已存**、传空→**清空**；「省略=清空」是最常见误判，且三态是平台自定义（omit=keep 较通用，缺省与清空不可假定），跨平台迁移须逐平台实测。② **改元数据 ≠ 零风险动作**：它照样出新版本，批量 API 会因「带了 flag」让全部选中项出新 patch ⇒ 元数据修正按发布等级对待（可回滚、可审计），并注意「文件没变却出新版」会污染版本台账。③ 治具：批量修改必须带 `skill_path` 限界，否则一改全库。
- **提升层**：可复用 Skill。触发词：元数据三态、省略保持/空值清空、首发兜底 other、改元数据发新版、unchanged-skip 被绕过、PATCH 未提供即不变。

## 涉密配置做成「给人看的指引工具」，而不是让 agent 经手秘密（来源：Activepieces MCP（/docs/mcp.md 通道）本机实拉，r326C）
- **原文**：`ap_setup_guide`「returns instructions for the user to configure connections in the UI, **rather than handling secrets through MCP**」；「Credentials are **never exposed** — connection secrets, API keys, and OAuth tokens are **never returned by any tool**」；Discovery = read-only tools，「Discovery tools are **always available**. Other categories can be enabled or disabled per-project」。
- **判据**：① 凭证边界的最佳实现是**工具的输出类型选择**（返回指引文本 vs 返回秘密值），而不是一条「禁止泄露密钥」的纪律——agent 侧根本没有拿到秘密的通道，边界由结构保证。② 「涉密步骤交给人、非涉密步骤交给 agent」是可设计的切分：把「在 UI 里配置连接」写成返回给用户的步骤清单。③ 只读能力恒开、写能力按项目开关，是同一思路在权限面的应用（该半条与既落「只读分级」重叠，仅作附条不重复计点）。
- **提升层**：可复用 Skill/工具。触发词：秘密边界结构化、setup guide 交人、工具输出类型即边界、只读恒开写按项目开。
