---
name: wb-skill-authoring
description: >-
  Skill 的写法与体检：触发词设计、description 质量、文件拆分、跨工具迁移、安装前安全审查、安装后接线、触发评测、盲测、诱饵用例、no-skill 对照、效果归因、技能无增益、技能抢触发、误触发、负向边界、不适用于、审计技能、技能过期、拼写错误、乱码、失效工具名、重复触发、技能快速路径表、双路由、meta-router、description 上限、name 规范、快照基线、触发率、近失、指令改写、改了指令还是不行、改了两遍还是这样、调指令算修了吗、别再加一句必须、拆技能、技能合并、技能去重、查重、技能素材来源、gotchas、控制度校准、给默认不给菜单。、规则该写多少、AGENTS.md 变长、allowed-tools 是限制吗、禁用工具、权限叠加、停用还是删除、参数分发、万能技能、专用子代理、防递归、显式契约、靠推断、角色重叠、通才助手、示例与考题要不相交、自动放行的兜底层、硬禁清单、技能选择准确性评测、不需要却加载、选错 skill、评委团、集成必须留子分、ensemble、多评委同签名、judge_scores、可溯源、provenance、CI 出证、无旁路、禁读环境变量与文件系统、输入走显式参数、审计面等于参数表、一个包一个服务、代理层不受理、可重跑产物、脚本沉淀、不许硬编码结果、连跑两次存证、产物自带说明、persona 市场退场、GPT Store 停用、迁移为插件、优先可机读注册表、版本号不塞 description、双榜分离、社区热度榜、官方自研榜、创建者域名标注、匿名统一标签、纯 UI 信源不学、审计盲区、只记写不记读、传参值不入库、失败也留痕、跨面不同步、surface 能力面、按面降级、导航四信号、签名强度、显式调用跳过路由、@标识调用、语义检索、诚实无匹配、skillContentHash、baseSkillHash、保存缺基准 400、基准过期 409、publish pins refs、delete refused names agents、scope inheritance、flag off 全路由 404、reviewability debt、accountable contribution、预烘技能包、baked bundle、manifest hash 不命中、分发面与可见面、load_skill 不服务、能力判定单一真身、默认模块不设也开
version: "1.221.0"
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
> 本节原文已零删减下沉 `references/knowledge-base.md §r442B 下沉：技能是"指令 + 所需工具"的打包，不是一段文字（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·技能是指令所需工具的打包不是一段文字）`（正文预算 ≤500 行）
## 触发评测：发布前盲测（新技能 / 改过 description 必做，细则已下沉 KB）（全文见 references/knowledge-base.md §下沉·触发评测发布前盲测新技能改过description必做细则已下沉KB）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r513C · 触发评测：发布前盲测（新技能 / 改过 desc）
## 按需阅读（渐进披露，不要常驻加载）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·按需阅读渐进披露不要常驻加载）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r513C · 按需阅读（渐进披露，不要常驻加载）（全文见 re）

## 声明式白名单只约束"工具调用面"，不约束"数据面"：判据按"被约束的是哪类调用"而非"有没有该字段"（来源：learn.microsoft.com/en-us/agent-framework/agents/skills、docs.github.com/.../add-skills、geminicli.com/docs/cli/skills、code.visualstudio.com/.../agent-skills、cursor.com/docs/context/rules，2026-10-01 r362-Q-C 实拉；与 r361-Q-B B1 跨客户端效力漂移 相邻）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·声明式白名单只约束工具调用面不约束数据面判据按被约束的是哪类调用而非有没有该字段）
## 校验失败的处理半径由错误严重度决定，且"静默跳过"是显式设计不是缺陷：整技能拒 / 仅告警跳过 / 未知顶层字段为前向兼容而忽略（来源：learn.microsoft.com/en-us/agent-framework/agents/skills、docs.dify.ai/.../plugin-info-by-manifest、docs.n8n.io/.../n8n-nodes-base.executeworkflow.md，2026-10-01 r362-Q-C 实拉）（全文见 references/knowledge-base.md §下沉·校验失败的处理半径由错误严重度决定且静默跳过是显式设计不是缺陷整技能拒仅告警跳过未知顶层字段为前）

## 学习轮沉淀区（本段）（全文见 references/knowledge-base.md §下沉·学习轮沉淀区本段）

## 技能「调用面 ≠ 入口面」：user-invocable:false 仍可被模型调用，加载源有显式优先级链…（原文已下沉 references/knowledge-base.md §L481）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r513C-2 · 技能「调用面 ≠ 入口面」：user-invoc）

## 技能进化不要自由变异，要「分解进固定能力空间 + 定向修订」…（原文已下沉 references/knowledge-base.md §L486）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r513C-2 · 技能进化不要自由变异，要「分解进固定能力空间 +）

## 技能控制流外置为显式状态机（EFSM）：知识与控制流分离，用显式状态转移替代模型猜下一步（细则见 KB，2026-09-30 r320A 下沉）（全文见 references/knowledge-base.md §下沉·技能控制流外置为显式状态机EFSM知识与控制流分离用显式状态转移替代模型猜下一步细则见KB202）

## 卸载必须留「显式卸载」marker（enabled: false tombstone），阻断启动修复静默重装；重装不静默恢复启用（来源：docs.openclaw.ai cli/plugins/uninstall-and-update，2026-09-30 r320A 实拉）（全文见 references/knowledge-base.md §下沉·卸载必须留显式卸载markerenabledfalsetombstone阻断启动修复静默重装重装）

## 撤销与审核分层：吊销只阻断后续发布、不推翻既有审核结论；恢复走 successor 重跑检查并保留失败尝试为审计史…（原文已下沉 references/knowledge-base.md §L495）
## 修订整包不可变且发布只对新会话生效、陈旧编辑报冲突不覆盖；「加载位置」与「谁能看见」是两个独立控件（原文已零删减下沉 references/knowledge-base.md §r631A 下沉，2026-10-27 r631A；触发词：修订包不可变、发布对新会话生效、陈旧编辑冲突、加载位置与可见性分离）
## 并发写仲裁三件套（陈旧写报冲突 / 相同保存 no-op / 会话钉修订）与幂等契约四元组（键作用域·占用时点·失败是否回放·保留期）；代理不得自动重试非幂等请求（来源：docs.openclaw.ai/tools/skills.md 39,705B + docs.stripe.com 1,336,845B + RFC 9110 §9.2.2 502,941B，2026-09-30 r322C 独立实拉；细则见 references/knowledge-base.md §r322C）（全文见 references/knowledge-base.md §下沉·并发写仲裁三件套陈旧写报冲突相同保存no-op会话钉修订与幂等契约四元组键作用域占用时点失败是否）

## 扩展点是「观察 + 否决」双职：回调里抛错即可阻止被钩的操作，且钩子无沙箱、回调继承宿主实例全权限——扩展点的权限边界等于宿主权限，选钩前必须先声明（来源：docs.n8n.io/hosting/configuration/external-hooks/ 1,023,234B，2026-09-30 r324B 独立实拉，原文 lowercase「forbid an action by throwing an error」命中；与 §审批门四旋钮 互补——那条管“变更怎么放行”，本条管“放行机制自身有多大权”；细则见 references/knowledge-base.md §r324B）（全文见 references/knowledge-base.md §下沉·扩展点是观察否决双职回调里抛错即可阻止被钩的操作且钩子无沙箱回调继承宿主实例全权限扩展点的权限边）

## 版本义务沿引用图传递：改动一个被依赖的文件，即使接口没变也要 bump 全部下游引用者（来源：pipedream.com/docs/components/contributing/guidelines.md 43,351B，2026-09-30 r325C 独立 curl 实拉逐串命中「If you update a file, you must increment the versions of all components that import or are affected by the updated file.」；经 Qoder r357-Q-A 提名；与已落「接口形状判破坏」互补——那条管"算不算破坏性变更"，本条管"谁的版本号必须跟着动"）（全文见 references/knowledge-base.md §下沉·版本义务沿引用图传递改动一个被依赖的文件即使接口没变也要bump全部下游引用者来源pipedre）

## 打包门禁的保留词表应含「背书语义词」，且检查必须跑在归一化形式上（来源：ClawHub publishing 本机实拉，r326C）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r513C-3 · 打包门禁的保留词表应含「背书语义词」，且检查必须）

## 技能/工具按任务语义检索 + 诚实无匹配（来源：Activepieces `mcp/tool-search.md` 3,608B，2026-09-30 实拉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r513C-3 · 技能/工具按任务语义检索 + 诚实无匹配（来源：）

## 技能自动修补的授权令牌三件套 + 所有权按目录判定 + 扫描分级只 critical 阻断（来源：docs.openclaw.ai/tools/self-learning 16,747B + /tools/skill-workshop/how-it-works 4,288B，2026-09-30 r338A 独立实拉）

1. **修补先取授权令牌，patch 必须引用同一 span**：`prepare_patch` 只授权「一个非空唯一精确 span」并返回有界上下文；下一次 `patch` 必须引用同一 span，**授权在一次尝试后或目标变更时即失效**，同一技能在授权被消耗/作废前的第二次 `prepare_patch` 被拒。判据：对技能的自动修补必须是「先锚定 → 按锚改 → 一次一锚」，禁止凭模糊匹配改写文件。
2. **运行时使用回执：只允许修补本次运行确实用过的技能**：原文 `A runtime usage receipt prevents foreground repair of skills that the run did not use`。判据：越界修补的判据不是「这个技能存不存在」，而是「这次运行有没有用过它」——没用过就没有修补资格，防止顺手改无关技能。
3. **所有权按目录判定，非自有来源只说明不编辑**：`A skill is Workshop-owned exactly when it is contained in that agent's directory`；bundled / ClawHub 安装 / 插件提供的技能由其 owner 的更新替换，agent 只说明不编辑；`create` 在目标已存在时直接失败（no clobber）。判据：**可写性由「归我管的目录」判定，不由名称或来源声明判定**。
4. **扫描分级，且关键词命中 ≠ 语义违规**：apply 前重跑安全扫描，**只有 critical 阻断 apply，warn 可见不阻断**；`Prompt-related keywords are not scanner findings`——提到「隐藏指令 / 工具审批」不构成指令覆盖。判据：静态扫描必须分级，命中敏感词不等于违规，否则扫得越全越不敢写。

- 提升层：可复用 Skill / 安全边界。触发词：修补授权令牌、prepare_patch、usage receipt、目录所有权、no clobber、critical 才阻断、关键词不等于违规。

- **无法交互时的兜底默认落在拒绝侧；长期授权要有四态可见与显式期限；允许清单的增删是幂等写（来源：docs.openclaw.ai/cli/approvals.md 16,110B，2026-10-01 r339C 独立 curl 实拉逐串命中）**：本章已下沉 `references/knowledge-base.md`（r339C）。
## 宿主能力须前置声明并 fail-closed；同一插件的三类失败走三条不同处置路径（来源：docs.openclaw.ai/concepts/context-engine.md 26,167B，2026-10-01 r343A 独立 curl 实拉逐串命中）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·宿主能力须前置声明并 fail-closed；同一插件的三类）
## 命名冲突只改自动别名并保留直达入口；确定性路由要显式声明；授权清单是覆盖式唯一权威（来源：docs.openclaw.ai/tools/slash-commands.md 38,378B，2026-10-01 r343B 独立 curl 实拉逐串命中）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·命名冲突只改自动别名并保留直达入口；确定性路由要显式声明；授）
## 权限上限在创建时刻快照且不可自增；一次性提权四要素；管理权不转移归属（来源：docs.openclaw.ai/automation/cron-jobs/payloads.md 27,960B + managing-jobs.md 17,374B，2026-10-01 r343C 独立 curl 实拉逐串命中）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·权限上限在创建时刻快照且不可自增；一次性提权四要素；管理权不）
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
> 正文预算管理：「r351C · 技能成本是"区间"不是标量：分发侧须公示上下界（来源：skill」（全文已零删减下沉 references/knowledge-base.md §下沉·r351C技能成本是区间不是标量分发侧须公示上下界来源skillsaliyuncomapipublicskillscat）
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

## 能力面是 resource:action 二维矩阵；正反动作与「开关权/查看权」各占独立开关位（来源：docs.n8n.io `.../create-custom-project-roles.md` 11,109B，2026-10-03 r388A 独立实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·能力面是 resource:action 二维矩阵；正反动作）
## 密钥的输入通道本身就是泄漏面；凭据分类是持久属性，自动推断只在首次生效（来源：docs.openclaw.ai/cli/secrets.md 16,115B，2026-10-03 r388C 独立实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·密钥的输入通道本身就是泄漏面；凭据分类是持久属性，自动推断只）
## 能力声明必须自带前置面与受限面：能用 ≠ 被允许在生产用（来源：docs.n8n.io `administer/manage-credentials/end-user-credentials.md` 9,720B，2026-10-03 r390A 独立 curl 取 `.md` 原文实拉；与 §SecretRef 禁 OAuth 等规范条款互补——那几条管规范合规面，本条管能力可用性的声明面）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·能力声明必须自带前置面与受限面：能用 ≠ 被允许在生产用）
## 能力面按组声明时，组名是展开式简写且自带排除清单；能力缺失应当是「隐藏」而不是「回落到更宽的面」；沙箱里的技能是投影不是本体（来源：docs.openclaw.ai `gateway/sandbox-vs-tool-policy-vs-elevated.md` 9,792B + `gateway/sandboxing/what-gets-sandboxed.md` 1,573B + `gateway/sandboxing/workspace-access.md` 7,119B，2026-10-03 r391A 独立 curl 取 `.md` 原文实拉；与 §能力面是 resource:action 二维矩阵 / §能力前置面四件套 互补——那两条管声明维度与门槛，本条管简写展开、缺失降级与运行期投影）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·能力面按组声明时，组名是展开式简写且自带排除清单；能力缺失应）
## 声明能力必须分「可提升」与「不可提升」两类限额；把内容交给第三方模型时，外发清单必须同时写「发什么」与「不发什么」（来源：pipedream.com/docs `workflows/limits.md` 9,083B + `workflows/building-workflows/errors.md` 9,150B，2026-10-03 r391B 独立 curl 取 `.md` 原文实拉；与 §能力前置面四件套 / §能力面是 resource:action 矩阵 互补——那两条管门槛与维度，本条管资源上限的可协商性与外发数据的负声明）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·声明能力必须分「可提升」与「不可提升」两类限额；把内容交给第）
## 托管额度是「按节点」的凭据选择，便利性换的是覆盖面；能力切换时隐藏与警告两种处理取决于当前状态（来源：docs.n8n.io `build/understand-workflows/use-gateway-credits.md` 6,208B，2026-10-03 r391C 独立 curl 取 `.md` 原文实拉；与 §能力前置面四件套 / §可提升与不可提升限额 互补——那两条管门槛与资源上限，本条管凭据粒度、覆盖面差集与切换行为）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·托管额度是「按节点」的凭据选择，便利性换的是覆盖面；能力切换）
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

> 正文预算下沉：本节原文已零删减移入 `references/knowledge-base.md`（外部解析器/命令的准入校验是一条有先后顺序的链；`${VAR:-fallback}` 是配置文本…）。
> 正文预算下沉：本节原文已零删减移入 `references/knowledge-base.md`（白名单的三种「空态」语义可能两两相反且删条目会回落默认；沙箱态是独立于用户配置的一层 clamp…）。
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

## 配置来源二选一时，声明式托管必须把交互面降级为只读；可选项由请求方声明，接收方不得自造（来源：docs.n8n.io `administer/observe-and-log/stream-logs-to-external-systems.md` 23,919B + docs.openclaw.ai `tools/exec-approvals-advanced.md` 27,837B，2026-10-03 r408A 独立 curl 取 `.md` 原文实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·配置来源二选一时，声明式托管必须把交互面降级为只读；可选项由）
## 逐项覆盖与集合默认构成三层继承；覆写键必须是服务端上报的原始名，改名即失效（来源：docs.bigmodel.cn `cn/managed-agents/permission-policies.md` 6,620B + `cn/managed-agents/skills.md` 6,574B（经 `llms.txt` 49,320B 定位），2026-10-03 r408C 独立 curl 取 `.md` 原文实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·逐项覆盖与集合默认构成三层继承；覆写键必须是服务端上报的原始）
## 安装形态本身就是审查对象：「下载即执行」类形态一律视为不可审查而拒（来源：docs.openclaw.ai `clawhub/acceptable-usage.md` 8,781B，2026-10-04 r411C 独立 curl 取 `.md` 原文实拉；与 §安装前安全审查 / §供应链摘要钉死 互补——那两条管"进门三判据"与"进门后内容是否被改"，本条管"这个安装方式有没有给人留出在跑之前看一眼的窗口"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·安装形态本身就是审查对象：「下载即执行」类形态一律视为不可审）
## 治理判据：统计信号只决定「要不要看」，规模要配「薄/重复/失维护/刷量」才算问题；处置按可逆性排序且不承诺先警告（来源：docs.openclaw.ai `clawhub/acceptable-usage.md` 8,781B + `clawhub/security-audits.md` 5,974B，2026-10-04 r411C 独立 curl 取 `.md` 原文实拉；与 §注册表审计判连贯性 互补——那条管给单个技能定级的口径，本条管批量治理时的判定与处置梯度）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·治理判据：统计信号只决定「要不要看」，规模要配「薄/重复/失）
## 加固的例外面必须逐条显式枚举并按「谁声明」分档；非法豁免条目拒绝启动；检查点在 DNS 解析之后（来源：pipedream.com/docs `conduit/deploy/network.md` 9,380B，2026-10-04 r412A 独立 curl 取 `.md` 原文实拉；与 §收紧出网会让相邻能力连带失效 / §安装形态本身就是审查对象 互补——那两条管"收紧的连带面"与"安装方式可不可审查"，本条管"运行期出网的例外怎么开、开给谁"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·加固的例外面必须逐条显式枚举并按「谁声明」分档；非法豁免条目）
## 技能注入是「边际收益递减且会转负」的量，不是越多越好：聚焦 ≤3 模块优于穷尽捆绑，收益主要由配置决定而非"装了技能"；装载成本应成为目录的一等可筛选字段（来源：arXiv `abs/2602.12670` SkillsBench 52,788B + `skills.aliyun.com/api/public/skills` 329,845B 公开 JSON，2026-10-04 r416C 独立 curl 实拉；与 §挂载每个 Skill 都占会话上下文 ⇒ 数量需有上限 互补——那条给出"要有上限"的方向，本条给出档位、代价曲线与"把它做成可筛选字段"的落地形态）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·技能注入是「边际收益递减且会转负」的量，不是越多越好：聚焦 ）
## 评测装置本身要先过参照解，题目坏与被测坏必须在机制上分开（来源（全文见 references/knowledge-base.md §r438A-sink1）
- **判据**：见下沉全文。（触发词保留在原 KB 条目）

## 审核进度映射为「运行能力上限」而不是「能否安装」（全文见 references/knowledge-base.md §r438A-sink2）
- **判据**：见下沉全文。（触发词保留在原 KB 条目）

## 安装策略门必须穷举「全部获取通道」、在裁决器自身故障时 fail-closed，（全文见 references/knowledge-base.md §r438A-sink3）
- **判据**：见下沉全文。（触发词保留在原 KB 条目）

## 派生 / 重写类制品必须附「与源的残留相似度读数」：把"我已重写"这句自陈降格为别人可复测的程度声明（来源：github.com/partme-ai/full-stack-skills 仓根 `PROVENANCE.md` 21,892B，2026-10-06 r428-B 经 `cdn.jsdelivr.net/gh/...` 实拉一手（raw.githubusercontent 本轮 SSL 直连不可达，已换通道并登记）；消化 Qoder r426-Q-C C-3，**并经 WB 亲自复拉更正其数值**）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·派生 / 重写类制品必须附「与源的残留相似度读数」：把"我已）
## 不可信元数据的解析器不得具备代码求值能力：解析器能力裁剪是与「来源白名单」「白名单键丢弃」并列的第三条独立门（来源：api.github.com/repos/vercel-labs/skills/contents/src/frontmatter.ts 一手 595B JSON→base64 解码正文，2026-10-06 r430-A 独立 curl 实拉逐串命中；与 §供应链准入=三重最小证明 互补——那条管"字段可信吗、来源是谁"，本条管"用什么解析器去读它们"）
- 原文逐字：`Minimal frontmatter parser. Only supports YAML (the `---` delimiter). Does NOT support `---js` / `---javascript` to avoid eval()-based RCE that exists in gray-matter's built-in JS engine.`
- 判据：① 元数据解析链的攻击面有**三个不可互相替代的维度**——字段维度（哪些键可信）、来源维度（从哪来）、**解析器维度（解析器自身能做什么）**；前两条都做到，只要解析器保留求值能力，"解析"这个动作本身就是代码执行面；② 该面**不需要攻击者触发任何功能**：读到格式标记即触发，能力存在即暴露，与"你有没有主动调用它"无关；③ 因此加固形态是**能力裁剪（capability stripping）而非输入过滤**——在构造解析器时就不给它求值通道，而不是在输入侧拦 `---js` 这类字符串（拦名单天然落后于解析器能力面）；④ **"用主流库"不等于"安全默认"**：gray-matter 这类事实标准库内建 JS 引擎，选型时要问的不是"它流不流行"，而是"它支不支持关掉求值"；⑤ 与 §供应链准入三重证明 是分层关系不是并列关系——身份层防顶名、来源层防中间人、元数据层防伪造字段，本条是它们的**第零层**：解析器一旦可求值，前三层连生效机会都没有。
- 提升层：可复用 Skill / 工具（技能加载与解析链的选型与实现约束）。

## 验签的宽松开关是「带文档化义务的例外」而非配置偏好：加上它之后结论必须改写成「已签文件通过、未签文件未判定」，生产默认严格（来源：docs.nvidia.com/skills/signing-agent-skills/ 414KB 一手实拉 2026-10-06 r431C + developer.nvidia.com 同题博客 271,692B 交叉印证，去标签后 **逐串命中**；与 sa KB「同一条『要求签名』在不同产品上强度不同（强制型/提示型）」互补——那条管**跨产品**的强度档位差异，本条管**同一个验证命令内部**结论作用域被一个开关收窄，以及该例外的举证义务）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·验签的宽松开关是「带文档化义务的例外」而非配置偏好：加上它之）
## 技能正文的「呈现格式」本身是自变量：「完整指南」与「最小提示」两种交付格式对成功率与成本均有影响（全文见 references/knowledge-base.md §下沉·呈现格式自变量；触发词：SkillAlign、完整指南 vs 最小提示、呈现格式自变量）

## 技能库成本要分两笔账：常驻目录占比（线性可算）与「引用文件全载」的最坏溢出（全文见 references/knowledge-base.md §下沉·技能库成本两笔账；触发词：7.1% of a 200,000-token reference window、112.7%、29 of the 46、一层深引用）

## 按「谁能调起」把技能二分，并用拓扑禁止同型级联：编排职责只给 user-invoked，纪律职责给 model-invoked（来源：api.github.com/repos/mattpocock/skills/readme 16,912B（`Accept: application/vnd.github.raw+json`），2026-10-07 独立 curl 实拉逐串命中 `User-invoked` / `Model-invoked` / `A user-invoked skill may invoke model-invoked skills, but never another user-invoked one.`；与 §防递归 / §角色重叠 互补——那两条靠纪律约束递归与角色，本条把它变成结构约束）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·按「谁能调起」把技能二分，并用拓扑禁止同型级联：编排职责只给）
## 技能升级传播模型必须显式二选一：共享发布（publish 即全部引用方原子生效、不留 per-agent 副本）vs 精确钉版（step 锁 exact version、发布时不再解析）；两者对「谁能在什么时候被牵连」的答案完全相反（来源：docs.dify.ai/en/self-host/use-dify/build/skills.md 4,325B 逐串命中 `When you publish an update to a skill, every agent that uses it picks up the latest version.` + activepieces.com/docs/install/reference/breaking-changes.md 85,989B 逐串命中 `Piece versions are no longer stored with wildcards (~1.2.0, ^1.2.0). All piece steps now use exact versions (e.g. 1.2.0).` / `The LOCK_AND_PUBLISH operation no longer resolves piece versions at publish time`；2026-10-08 独立 curl 实拉。与 §成本两笔账 互补——那条管常驻/激活的 token 账，本条管更新的传播语义）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·技能升级传播模型必须显式二选一：共享发布）
## 再分发资格要按「子目录粒度」核许可，不得以仓库标称许可推定：同一仓库可并存多层许可（anthropics/skills 多数 Apache-2.0，但 `docx/pdf/pptx/xlsx` 子目录为 source-available 且限定演示与教学用途，根目录无 LICENSE）（来源：github.com/anthropics/skills/ 284,255B，2026-10-08 独立 curl 实拉逐串命中 `These are source-available, not open source` / `These skills are provided for demonstration and educational purposes only.`；与 §技能发现目录优先级 互补——那条管从哪找，本条管找到之后能不能带走）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·再分发资格要按「子目录粒度」核许可，不得以仓库标称许可推定：）
## 热度/排序信号须在「单技能层」计算再按来源去重：榜单若以来源仓库为聚合单位，单一厂商可垄断整张热榜（skills.sh RSC payload 组件名 `SkillsLeaderboardBySource`，`totalSkills=9964`、`view=trending` 为 24h 窗口）（来源：www.skills.sh/trending 371,118B，2026-10-08 独立 curl 实拉逐串命中 `SkillsLeaderboardBySource` / `"totalSkills":9964` / `"view":"trending"`；与 §技能家族模式 互补——那条记榜单存在与家族形态，本条记聚合粒度本身会扭曲信号）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·热度/排序信号须在「单技能层」计算再按来源去重：榜单若以来源）
## description 只写「何时触发」，绝不总结正文流程；且指导形式必须按「失败类型」选（来源：api.github.com/repos/obra/superpowers/contents/skills/writing-skills/SKILL.md 一手 37,635B JSON → base64 正文 26,523B，2026-10-08 r438A 独立 curl 实拉逐串命中 `NEVER summarize the skill's process or workflow` / `Match the Form to the Failure` / `trended worse than even the no-guidance control` / `NO SKILL WITHOUT A FAILING TEST FIRST`；全库 grep 两个金句均 0 命中）
- **① description 是触发面不是内容摘要**：原文实证——某技能正文流程图写的是两阶段评审（spec 合规 → 代码质量），description 里写了「code review between tasks」，模型就只做了一次评审；把 description 改成纯触发条件「Use when executing implementation plans with independent tasks」后，模型才去读正文并跑完两阶段。判据：**description 里出现任何流程动词，正文就降级成"可跳过的文档"**；写 description 时逐个词问「这是触发条件还是步骤」，是步骤就删。
- **② 禁令不是默认形式——按 baseline 失败类型三选一**：纪律型失败（明知故犯、压力下绕规则）→ 禁令 + 合理化表 + 红旗清单；输出形状错（该简洁却冗长、结论被埋）→ 正向 recipe / 契约，写清输出"是什么、有哪几段、什么顺序"；漏必需元素 → 结构化必填槽位。原文实测反证：**在"输出形状"类失败上用禁令式，结果比正向 recipe 更差，甚至差于"完全不给指导"的对照组**。判据：写约束前先跑一次 baseline 记录它到底怎么坏；**坏法不同，写法必须不同**，不许一律加"禁止/必须"。
- 提升层：可复用 Skill（技能写法）/ 工作流（先测 baseline 再写约束）。触发词：description 总结流程、只做了一次评审、照 description 执行、跳过正文、Match the Form、trended worse、禁令式反而更差、正向契约、recipe、red flags、rationalization table、NO SKILL WITHOUT A FAILING TEST


## 「可选项」与「可写值」必须分开：模型可从已批准配置清单里选，但不得用自然语言改写配置值——配置是不可变引用（来源：help.aliyun.com `/zh/model-studio/parse/integration-skill` 54,875B，2026-10-08 一手实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·「可选项」与「可写值」必须分开：模型可从已批准配置清单里选，）
## 只增不减的技能库不是治理库：必须自带「退化计量」，AI 协作占比要能说出来（来源：arxiv.org/abs/2609.05677 43,152B，2026-10-08 一手实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·只增不减的技能库不是治理库：必须自带「退化计量」，AI 协作）
## 中心策略设的是「地板」不是默认值：局部只能更严不能更松；策略所有权归声明源（env/IaC），UI 只是只读视图（来源：docs.n8n.io/deploy/host-n8n/configure-n8n/security/manage-security-policies.md 8,773B + security/block-specific-nodes.md 2,425B，经 llms.txt 287,049B 定位真路径后 2026-10-08 一手 curl 取 `.md` 原文逐串命中 `instance-wide minimum redaction policy that individual workflow settings can't weaken` / `the **Enforce two-factor authentication** and **Personal Space** toggles on this page become read-only` / `NODES_EXCLUDE`；与 §deny-only 继承 互补——那条管分层作用域谁能放大，本条管中心策略与局部配置之间的方向性）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·中心策略设的是「地板」不是默认值：局部只能更严不能更松；策略）
## 供给源消失即本地自动清除：技能库要有「请求方溯源」字段，删依赖=删技能的判据来源（来源：api.github.com/repos/vercel-labs/skills/commits 141,723B 一手 JSON，2026-10-08 实拉逐 commit message 命中 `cf07a49` remove skills that dependencies no longer ship / `15c88cc` remove skills by source / `a1f58a2` add --include and --exclude filters / `b381064` read npm: entries from package.json skills fields / `42f3441` read skills from direct dependencies only；与 §deprecation rate 互补——那条计删除率，本条给删除的正当事由与执行机制）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·供给源消失即本地自动清除：技能库要有「请求方溯源」字段，删依）
## 技能装载对坏 frontmatter 是 fail-open：解析失败不拦截、静默丢掉全部约束字段；本库必须反着做成 fail-closed（来源：code.claude.com/docs/en/skills 1,194,488B，2026-10-08 一手 curl 逐串命中 `If the YAML between the markers doesn't parse, the skill still loads with no fields set` / `ignores a field it doesn't recognize without reporting an error` / `reads the frontmatter only when the opening --- is the file's first line`；与 §frontmatter 校验类既往条目 互补——那边管字段填什么，本条管"填坏了会发生什么"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·技能装载对坏 frontmatter 是 fail-open）
## 宿主（客户端）落地四事：宽容错是**有边界的分级**、压缩须豁免已激活技能正文、同名冲突要留诊断、发现面要有上界与信任门（来源：agentskills.io/client-implementation/adding-skills-support 426,790B → 去标签 26,969B + /specification 443,754B，2026-10-08 一手 curl 逐串命中 `YAML is completely unparseable → skip the skill, log the error` / `exempt skill content from pruning` / `project-level skills override user-level` / `max 2000 directories` / `gating project-level skill loading on a trust check`；与 §frontmatter fail-open 互补——那条是某实现的行为，本条是规范侧的分级与宿主面其余三机制）
- **实证**：规范原文四段——① 宽容错分级「**Lenient validation**: Warn on issues but still load the skill when possible: Name doesn't match the parent directory name → **warn, load anyway**; Name exceeds 64 characters → **warn, load anyway**; Description is missing or empty → **skip the skill** (a description is essential for disclosure), log the error; **YAML is completely unparseable → skip the skill, log the error**」+「**Record diagnostics** so they can be surfaced to the user」；② 上下文保护「If your agent truncates or summarizes older messages when the context window fills up, **exempt skill content from pruning**. Skill instructions are durable behavioral guidance — losing them mid-conversation **silently degrades the agent's performance without any visible error**」；③ 冲突与发现「**project-level skills override user-level skills** … either first-found or last-found is acceptable — **pick one and be consistent. Log a warning when a collision occurs so the user knows a skill was shadowed**」+「Set reasonable bounds (e.g., **max depth of 4-6 levels, max 2000 directories**) to prevent runaway scanning」；④ 信任门「Project-level skills come from the repository being worked on, which may be untrusted (e.g., a freshly cloned open-source project). Consider **gating project-level skill loading on a trust check** — only load them if the user has marked the project folder as trusted. This prevents untrusted repositories from **silently injecting instructions** into the agent's context.」
- **判据**：① **宽容错不是一律放行，而是「降级 vs 跳过」两档分级**：外观类问题（命名不匹配目录、名字超 64）警告后照常加载；**失去可发现性或失去结构（description 缺失、YAML 完全不可解析）必须跳过并记诊断** ⇒ 判据是"这个缺陷会不会让技能变得不可见或不可控"，不是"是不是格式错"。② **规范与实现可以相反，装载器必须显式声明站哪一侧**：本规范写"不可解析→跳过并记日志"，而 Claude Code 文档写"不可解析→照常加载、无字段"（见 §frontmatter fail-open）⇒ 审核一个技能库时，先问"你的装载器坏了怎么反应"，再谈字段填什么；两侧行为不一致时，"我按规范写的"不构成安全证据。③ **上下文压缩必须豁免已激活技能正文**：技能正文是持续性行为约束，被压缩掉不会报错、只会静默退化 ⇒ 压缩策略里要有一个显式的"活跃指引保留位"，否则 Agent 后半程的行为漂移无法归因。④ **同名冲突必须留诊断日志**：冲突本身按"项目级覆盖用户级"解决，但不打日志就等于静默遮蔽——用户以为在跑 A，实际在跑 B。⑤ **发现面必须有上界与信任门**：目录遍历要设深度/数量上限防失控扫描；项目级技能来自可能被克隆的不可信仓库，须过信任门 ⇒ 否则 clone 一个仓库就等于让别人往你的上下文里写指令。
- **与既有能力分工**：§frontmatter fail-open 管**某一实现遇到坏 frontmatter 的实际行为**；本条管**规范侧该不该放行、以及宿主面其余三项（压缩豁免/冲突诊断/发现面上界与信任门）**。
- 提升层：工作流（宿主实现）/ 工具（装载器）。触发词：Lenient validation、warn load anyway、skip the skill log the error、exempt skill content from pruning、project-level overrides user-level、log a warning when a collision occurs、max 2000 directories、trust check for project skills。


## 技能可见性有三态而不是两态：未设=继承默认、空数组=全断、非空=完全替换（不 merge）；装载优先级七档同名最高源胜出，发现面有五个各自独立的限额（来源：docs.openclaw.ai/tools/skills.md 48,338B + gateway/config-extensions.md 21,481B，2026-10-08 一手 curl 逐串命中 `agents.entries.*.skills: []` to expose no skills / `A non-empty ... list is the **final** set — it does not merge with defaults` / `highest precedence first` / `limits.maxSkillsPromptChars` / `An empty result with partial coverage does not prove that no applicable skill exists`；与 §r441C 宿主四事（宽容错分级/压缩豁免/同名诊断/发现面上界）互补——那条给出上界数值，本条给授权三态与优先级表）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·技能可见性有三态而不是两态：未设=继承默认、空数组=全断、非）
## description 的调优不是「改写得更好」，而是一套带负例、带重复、带切分、带封顶的定量协议（来源：agentskills.io/skill-creation/optimizing-descriptions.md 13,307B，2026-10-08 一手 curl 逐串命中 `Aim for about 20 queries: 8-10 that should trigger and 8-10 that shouldn't` / `3 runs each, that's 60 invocations` / `above a threshold (0.5 is a reasonable default)` / `Train set (~60%)` / `Validation set (~40%)` / `Five iterations is usually enough`；兑现 r442A 挂起项——当时缺一手文本，本轮原文全数值到账）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·description 的调优不是「改写得更好」，而是一套带）
## 供给端「自动同步」与消费端「自动升级」是两个必须分离的开关：目录可以每小时 reconcile，但已装配的每一步钉死精确版本、永不自动升版（来源：www.activepieces.com/docs/install/architecture/piece-syncing 310,613B，2026-10-08 一手 curl 逐串命中 `Each step is pinned to an exact version.` / `Flows never auto-upgrade. Version bumps are explicit, through the builder.` / `OFFICIAL_AUTO` = `Hourly reconcile against the cloud registry. Default for all deployments.` / `never touched by the sync job.`；与 §供给源消失即本地自动清除 互补——那条管"上游没了怎么回收"，本条管"上游一直有、而且很勤快地更新时，下游该不该跟着动"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·供给端「自动同步」与消费端「自动升级」是两个必须分离的开关：）
## 写技能前先做「能力缺口评测」：先跑代表任务定位缺口、再为命名的缺口写技能（来源：anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills 138,441B，2026-10-08 一手 curl 实拉逐串命中 `Start with evaluation: Identify specific gaps in your agents' capabilities by running them on representative tasks`；与 §触发评测盲测 / §描述定量调优协议 互补——那些管"写完后怎么验触发/调 description"，本条管"动笔前先确认该不该写、写给哪个缺口"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·写技能前先做「能力缺口评测」：先跑代表任务定位缺口、再为命名）
## 技能库治理应建模为「fitness-driven 生命周期」：trial→active→stable→retired，stable 后回落即 obsolescence，borderline 走 LLM 突变重写而非直接删（来源：arxiv.org/html/2610.09832v1（SkillForge）567,160B→去标签全文 98,121B，2026-10-08 一手 curl 逐串命中 `fitness-driven skill lifecycle of trial , active , stable , and retired states` / `a skill whose fitness once reached the stable state but later drops below the retirement threshold` / `borderline-fitness skills rewritten by an LLM-guided mutation operator`；与 r439C「只增不减不是治理库」/ r441B 批量退役三闸 互补——那些管"删不删/怎么批量删"，本条管"每个技能在库里处在哪个态、怎么流转"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·技能库治理应建模为「fitness-driven 生命周期」）
## 组件/技能发现面用「显式映射表 + 模块代理 + 前缀 finder」三件套实现；第三方 bundle 没有公开 hook 可挂，准入必须改在解析层（来源：cdn.jsdelivr.net/gh/langflow-ai/langflow@main/src/backend/base/langflow/__init__.py，2026-10-08 一手 curl 逐串命中 `module_mappings`/`LangflowCompatibilityModule`/`_PACKAGE_OVERRIDES`/`MetaPathFinder`；纠正 r442A 猜的 `_dynamic_imports` 串 curl 实测 0 命中；r445A 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·组件/技能发现面用「显式映射表 + 模块代理 + 前缀 fi）
## 不可信发现清单的解析器要「逐项丢弃 + 空集合」而非「尽力解析 + 报错」：skill://index.json 只收 ZIP、digest 抽取前校验、整份损坏返回空列表（来源：learn.microsoft.com/en-us/agent-framework/agents/skills，ms.date 2026-10-02，2026-10-08 一手 curl 逐串命中 `skill://index.json`/`application/zip`/`digest`/`sha256`/`Archive`/`skip`；r445B 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·不可信发现清单的解析器要「逐项丢弃 + 空集合」而非「尽力解）
## 技能库「同职共存」冲突必须独立计量：任务完成度指标对此完全盲，被顶替的技能会静默丢失独占约束（来源：arxiv.org/abs/2610.11647（One Skill Too Many）44,009B，2026-10-09 一手 curl 逐串命中 `skills come from independent sources` / `picks between them by name and description alone` / `20,947` / `822,109` / `3,754` / `312` / `6,368 runs, 169,294 tool calls, 542 agent-hours` / `nearly one in four` / `37%` / `one in five runs` / `over a third` / `a ban on touching git` / `0.9%`；r472A 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·技能库「同职共存」冲突必须独立计量：任务完成度指标对此完全盲）
## 发布通道可以是「仓库即注册表」：CI 监听 SKILL.md 变更自动发布，slug 按 owner/name 钉死、改分类不改 slug，目录自带 eval 即装即测（来源：api.github.com/repos/hayka-pacha/skills/readme 3,142B，2026-10-09 一手 curl 逐串命中 `Open registry of reusable SKILL.md packages` / `published to [Smithery] automatically on every push to main` / `hayka-pacha/<skill-name>` / `Moving a skill to another domain re-publishes it with the new URL; the slug does not change` / `do not use generic buckets` / `evals/evals.json`；`hayka` 在 co-learn 全库 0 命中；r472A 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·发布通道可以是「仓库即注册表」：CI 监听 SKILL.md）
## 语义相关 ≠ 执行可用：检索到的技能是「可调草稿」不是既定指令，瓶颈已从「技能够不够多」转向「有没有结构化编排机制」（来源：arxiv.org/abs/2608.06880（SkillAligner）42,920B + arxiv.org/abs/2604.17870（GraSP）42,046B，2026-10-09 一手 curl HTTP 200 逐串命中 `semantic relevance does not guarantee execution utility` / `skill--execution misfit` / `training-free execution-time skill adaptation` / `resolving dependencies, conflicts, and redundancy across skills` / `skill ecosystems ... providing agents with more skills does not monotonically improve performance` / `focused sets of 2-3 skills outperform comprehensive documentation` / `the first executable skill graph architecture that introduces a compilation layer between skill retrieval and execution` / `typed directed acyclic graphs (DAGs) with precondition-effect edges` / `locality-bounded repair through five typed operators -- reducing replanning from O(N) to O(d^h)`）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·语义相关 ≠ 执行可用：检索到的技能是「可调草稿」不是既定指）
## 兼容性门槛有「规范侧」与「宿主侧」两个断点，谁都不提供机读面：技能声明兼容不能用产品整体版本表达，依赖哪个子能力就要在哪个子能力的最低版本上取严（来源：agentskills.io/specification.md 7,697B + code.claude.com/docs/en/skills.md 106,492B，2026-10-10 一手 curl 逐串命中 `compatibility`×7 / `Max 500 characters` / `metadata:`+`version: "1.0"` / `skillOverrides`×12 / `name-only`×4 / `user-invocable-only`×3 / `v2.1.196`×3 / `v2.1.218`×4 / `v2.1.252` / `v2.1.273`×2 / `v2.1.283` / `v2.1.286`；r486B 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·兼容性门槛有「规范侧」与「宿主侧」两个断点，谁都不提供机读面）
## 绑定语义分「按名解析」与「按版解析」两种：前者默认浮动升级，会让已落地的锁版判据静默失效（来源：help.aliyun.com/zh/model-studio/introduction-to-skill 38,750B，2026-10-10 一手 curl 逐串命中 `重新上传同名`×2 / `审查通过后，已添加该 Skill 的智能体会自动使用最新版本` / `官方 Skill 由平台统一维护和更新，已添加到智能体的官方 Skill 会自动使用最新版本` / `不可与当前账号`；r486C 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·绑定语义分「按名解析」与「按版解析」两种：前者默认浮动升级，）
## r490B-2 · 清单字段严格性按「对象位置」分档，两档失败后果相反；组件路径守卫有「越根 / 不存在」两态且都要机读错误位（来源：code.claude.com/docs/en/plugins-reference 827,749B，2026-10-10 r490B 一手 curl 实拉逐串命中 `Top-level fields: the field is stripped and the plugin loads` / `Strict objects: userConfig options, channels entries, lspServers configs, and monitors entries are strict. An unknown key inside one is an error, and the plugin doesn't load` / `<component> path escapes plugin directory` / `Existence: a path that doesn't exist doesn't load` / `version A version string, not checked against semver`）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r490B-2 · 清单字段严格性按「对象位置」分档，两档失）
## r492C-2 · 「被静默忽略」不该只靠运行后对照去发现，它可以前移成静态可机检错误：把写时 illegal 变成加载前报错（来源：github.com/agent-sh/agnix README 10,555B，2026-10-10 r492C 一手经 api.github.com/repos/agent-sh/agnix/readme 取原文）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r492C-2 · 「被静默忽略」不该只靠运行后对照去发现，）
## r495C · 「覆盖」的单位是命令而不是技能，且命名空间与链接形态各自独立决定共存与否；装载栈必须同时声明覆盖单位与共存条件（来源：code.claude.com/docs/en/skills 1,200,668B，2026-10-10 r495C 一手 curl 实拉逐串命中 `Your skill replaces the bundled command, but not its aliases` / `In a local terminal session, your skill replaces the built-in command, but not its aliases` / `Both load, because plugin skills are namespaced as /plugin-name:skill-name` / `Claude Code reads SKILL.md from the target and loads the skill once even if several locations point at the same target` / `Enterprise over personal, and personal over project`）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r495C · 「覆盖」的单位是命令而不是技能，且命名空间与）
## r513C · 技能评测必须是「有技能 / 无技能」双跑对照 + 每轮干净上下文；断言先看第一轮产出再补（来源：agentskills.io/skill-creation/evaluating-skills.md 16,957B，2026-10-11 r513C 一手 curl 200 实拉逐串命中 `once **with the skill** and once **without it**` / `clean context` / `Start with 2-3 test cases` / `first round of results` / `iteration-1` / `benchmark.json`）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r513C · 技能评测必须是「有技能 / 无技能」双跑对照）
## r513C-2 · description 触发评测要有「近似未命中」负例；且触发率低先分诊是不是 agent 自认为能处理（来源：agentskills.io/skill-creation/optimizing-descriptions.md 13,307B，2026-10-11 r513C 一手 curl 200 实拉逐串命中 `Aim for about 20 queries` / `8-10 that should trigger` / `near-misses` / `beyond what they can handle alone` / `Err on the side of being pushy` / `1024`）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r513C-2 · description 触发评测要有「近）
## 错误面分两类设计：外部/API 故障（NodeApiError，可重试/自愈）vs 操作/校验/配置错（NodeOperationError，输入或配置问题重试无意义）；多 item 处理须把错误绑定到具体 itemIndex（pairedItem）而非整批标红，continueOnFail 时推回 {error, pairedItem} 让其余 item 继续（细则见 KB，2026-10-11 r520C 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·错误面分两类设计）
## 被发现是三个独立门inventory装了readiness依赖齐visibility经宿主过滤后露出且显式指定远端后绝不回退本地同名（细则见 KB，2026-10-11 r524B 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·被发现是三个独立门）

## 技能常驻是有预算、会截断、会被整条丢弃的条件保证：重挂保留每技能前 5000 token、全部共享 25000 池、按最近调用优先回填、重入按渲染内容差异判定（细则见 KB，2026-10-11 r525B 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r525B 技能常驻是有预算会截断会被整条丢弃的条件保证）
## 技能调用的信用须拆成选择与执行两条独立通道且选择信用带唯一命中约束基线算在 action 上、调用包装层与技能正文显式无主（细则见 KB，2026-10-11 r525C 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·r525C 技能调用的信用须拆成选择与执行两条独立通道）
## 包元数据每条声明须分强制校验静默忽略继承三类被忽略项不得写进契约身份键参与标识符（细则见 KB，2026-10-12 r526C 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·包元数据里的每一条声明都要先分三类）

## 多宿主适配是独立manifest矩阵不是一份声明加兼容层须逐宿主枚举并独立验收（细则见 KB，2026-10-12 r526C 下沉）（全文见 references/knowledge-base.md §下沉·wb-skill-authoring·一份技能资产的多宿主适配是独立manifest矩阵）

## 命名冲突要有独立的「所有权评审」通道，且与举报、账号申诉三路分流；能自管的先自管，走评审只解决你管不了的对象（来源：docs.openclaw.ai/clawhub/namespace-claims.md 4,167B，2026-10-12 r527B 一手 curl 200 逐串命中 `Org and Namespace Claims` / `reserved, transferred, renamed, hidden, quarantined, aliased, or otherwise changed` / `Use this path for public, non-sensitive ownership review. Do not use in-product reports or the account appeal form for namespace claims.` / `Use a claim when you cannot manage the current owner or when staff needs to resolve a dispute.`；r527B 落地）
- **实证**：ClawHub 把 owner handle / org handle / skill slug / 插件包名 / package scope 都当公共命名空间；出现归属争议时用专门的 issue 表单申请 staff review，处置动作枚举为 `reserved, transferred, renamed, hidden, quarantined, aliased`。页面明确**不要用产品内举报或账号申诉表单**提命名空间主张，且**评审只管所有权、不管漏洞披露**（「The namespace claim form is for ownership review, not emergency vulnerability disclosure」）；证据要求「public, non-sensitive」，逐条说明「what each link proves」，明确禁止放 token / 签名密钥 / DNS 挑战 token / 身份文件。
- **判据**：① **"被占用"有六种不同处置，价值差别很大**：保留/转移/重命名/隐藏/隔离/别名 ⇒ 提主张时必须指明要哪一种，否则评审方只能自己挑，结果与诉求错配。② **三条上报通道必须分流**：所有权评审 vs 安全举报 vs 账号申诉，用错通道等于排队到错的队列且可能把敏感证据公开 ⇒ 提交前先判"这件事的争点是不是归属"。③ **证据的可公开性本身就是约束**：既然评审在公开 issue 里进行，证据就必须是不依赖密钥也能成立的（仓库/发布/文档/域名/三方包 registry 控制权/商标）⇒ 凡是"只能靠出示私钥证明"的归属，在这个通道里无法成立，需要另找路径。④ **自助优先，评审兜底**：`Before You File` 要求先确认为自己就是命名空间匹配的 owner，能改名/转移/隐藏/删除就自己做 ⇒ 把能自管的争议提交评审，是把治理成本转嫁给平台。⑤ **与"认领态字段"是互补两面**：市场上 `claim_state: unclaimed` 这类字段只描述当前状态，而评审通道描述**状态可以被推翻** ⇒ 只有字段没有通道时，"被抢注"没有救济；审计一个技能市场要同时看这两样。
- 提升层：可复用 Skill（发布治理）/ 工作流（争议处理）。触发词：namespace claim、命名空间归属评审、skill slug 抢注、report/appeal/claim 三路分流、公开非敏感证据、quarantined/aliased 处置。

## 技能自带的工具授权声明是可被宿主策略整条作废的声明：受管环境下 allowed-tools 被忽略并改走组织规则，且作废必须可枚举；技能侧的 disallowed-tools 是消息级临时限制不是会话级（来源：code.claude.com/docs/en/skills.md 107,130B，2026-10-12 r528C 一手 curl 200 逐串命中 `When your organization sets allowManagedPermissionRulesOnly in managed settings, Claude Code ignores allowed-tools in project and personal skills and in the other sources the setting's entry lists. This requires Claude Code v2.1.282 or later.` / `The tools an affected skill lists go through your organization's managed rules and the normal permission prompt instead.` / `Run /status to list each skill whose allowed-tools Claude Code has ignored so far in the session.` / `A skill can grant itself broad tool access, so review the allowed-tools of skills checked into a repository before you run Claude Code there.` / `To remove tools from Claude's available pool while a skill is active, list them in disallowed-tools ... The restriction clears when you send your next message.`；r528C 落地）
- **实证**：技能 frontmatter 可以自带 `allowed-tools`（如 `Bash(git add *)` 一类的粒度）与 `disallowed-tools`；官方同时给出三条反向事实：① 组织设置 `allowManagedPermissionRulesOnly` 后，**项目技能与个人技能里的 `allowed-tools` 被整条忽略**，改走组织受管规则与常规权限提示，**且该行为需要 v2.1.282 以上**；② 被忽略的技能要能被枚举——`/status` 列出"本会话至今被忽略 allowed-tools 的技能"；③ `disallowed-tools` 的作用期是**到下一条消息为止**，并像 deny 规则一样无法在还有其他工具时移除 `EndConversation`。
- **判据**：① **"我在技能里声明了权限"不等于"运行时有这个权限"**：声明面与生效面之间隔着一整套宿主策略 ⇒ 技能作者不得把 `allowed-tools` 当作能力承诺写进文档，正确写法是"本技能需要 X 工具，若被策略忽略请改用组织规则放行"。② **作废必须可枚举，否则不可排障**：官方专门提供 `/status` 列出被忽略项 ⇒ 任何"静默忽略包内声明"的机制都必须配一个"列出被忽略项"的查询面；没有这一面，用户遇到"技能说能跑但一直弹权限"只能猜。③ **忽略是版本绑定的**：`requires Claude Code v2.1.282 or later` ⇒ 组织策略的覆盖面随客户端版本变化，同一份策略在旧客户端上不生效；验收受管策略时要先核版本下限。④ **限制的作用期要写明粒度**：`disallowed-tools` 是**消息级**（下一条消息即清除），不是会话级也不是技能级 ⇒ 把"技能内禁用"当持久收窄来设计，会在下一条消息就失效。⑤ **"技能可自我授予宽权限"是审查项不是便利**：官方直接警示 `A skill can grant itself broad tool access, so review the allowed-tools ... before you run` ⇒ 上架/入库审查必须把 `allowed-tools` 列表作为独立受审面逐项过，而不是只看描述与代码。⑥ 与 §声明分三类（强制/静默忽略/继承，sa 1.119.0）互补：那条给出"声明不被采纳"的分类，本条给出**谁有权让它不被采纳（组织策略）+ 如何举证它被忽略了**。
- 提升层：工具（权限声明面）/ 工作流（受管环境适配）。触发词：allowed-tools 被忽略、allowManagedPermissionRulesOnly、/status 列出忽略项、disallowed-tools 消息级、技能自我授予权限、受管策略版本下限。

## 一条消息里可以堆叠多个技能，但展开有硬上限且停在第一处非「内联用户可调用技能」的 token 上；停止点之后的全部文本会被灌给所有已展开技能当参数，无占位符接收时宿主把它追加到正文末尾（来源：code.claude.com/docs/en/skills.md 107,130B，2026-10-12 r529B 一手 curl 200 逐串命中 `You can also stack several skills at the start of one message.` / `Claude Code expands the first skill plus up to five more stacked after it.` / `Expansion stops at the first token that isn't an inline user-invocable skill` / `That token and everything after it become the argument text for every expanded skill.` / `/code-review runs as a forked subagent from v2.1.218` / `If you invoke a skill with arguments but no placeholder in the skill's content receives one, Claude Code appends ARGUMENTS: <your input> to the end of the skill content so Claude still sees what you typed.` / `An indexed placeholder with no argument at its position stays as literal text and doesn't count as receiving one. A named placeholder counts even when its position has no argument`；r529B 落地）
- **实证**：官方允许在一条消息开头连写多个技能（示例 `/write-tests /fix-issue 123`），并给出三条此前未落的边界：① **展开上限是"第一个 + 之后最多五个"**（`the first skill plus up to five more stacked after it`），不是不限量；② **展开在第一处"非内联用户可调用技能"的 token 处停止**——跑在分叉子 agent 里的技能（`/code-review`，自 v2.1.218 起）会终止堆叠；参数本身可能以斜杠开头的技能（如 `/loop`）同样终止；③ **停止点及其之后的全部文本，成为每一个已展开技能的 `$ARGUMENTS`**。参数落位规则另含两条反向事实：**索引占位符（`[0]`/`$1`）在对应位置无参数时保持字面文本且不算"接收到参数"**，**命名占位符即使展开为空也算接收到**；若全文没有任何占位符接到参数，宿主把 `ARGUMENTS: <你的输入>` 追加到技能正文末尾，而不是静默丢弃。
- **判据**：① **"能一次挂几个技能"是规格不是习惯**：上限六个（1+5）必须写进文档与验收；依赖"多挂几个"来编排的组合式设计，超过六个会静默少挂 ⇒ 组合前先数个数，别靠试。② **堆叠的终止条件是语义类别而非分隔符**：决定在哪停的是"这个 token 是不是内联用户可调用技能"，不是空格或斜杠 ⇒ 把子 agent 型技能（forked subagent）插进栈中间，会造成"后面的技能全都变成参数文本"——表现是后面的技能没被执行，且**没有报错**。③ **终止点之后的文本会被重复消费**：`become the argument text for every expanded skill` ⇒ 同一段文本同时进入多个技能的 `$ARGUMENTS`，任何一个技能里的"把全部参数当指令执行"写法都会被放大成多份；设计多技能编排时，参数归属要么显式前缀，要么别堆叠。④ **"有没有接到参数"的判定规则要按占位符类型分别记**：索引型缺参=保持字面且不计数，命名型空值=仍计数 ⇒ 同一句"我传了参数没生效"，原因可能是索引位缺参导致整段被追加到末尾，而不是被填进占位符。⑤ **无处安放的参数被追加而非丢弃**：宿主宁可把 `ARGUMENTS: <输入>` 贴在正文末尾也要让模型看见 ⇒ 反过来说，**不能**靠"没写占位符"来屏蔽用户输入；真要忽略参数必须显式说明。⑥ **子 agent 化是破坏性变更**：`/code-review` 从内联改为 forked subagent（v2.1.218）直接改变了它在栈里的行为 ⇒ 技能的运行形态（inline / forked）属于对外契约，改变形态要按破坏性变更发布并给出版本下限。⑦ 与 §覆盖的单位是命令不是技能（sa KB r495C）、§授权面四个派生通道（sa KB:3667③）分工：那两条管"同名谁赢 / 哪些通道能看见"，本条管**同一条消息里多个技能如何被展开、在哪里断、断后的文本归谁**。
- 提升层：可复用 Skill（调用契约）/ 工作流（多技能编排）。触发词：技能堆叠、stacked skills、1+5 展开上限、forked subagent 终止堆叠、停止点后全为参数、ARGUMENTS 追加到末尾、索引占位符缺参保持字面、命名占位符空值也算、/code-review v2.1.218。


## 声明即契约：接口声明了的参数必须真的传到下游（静默忽略 = 接口在撒谎），文档承诺「省略则用默认」必须在代码里有空值路径；两者都要用「另一侧样本」和「完全省略」用例来测（来源：api.github.com/repos/PrefectHQ/prefect/pulls/23300 + /pulls/23334，2026-10-12 r532C 一手 curl 200 逐串命中 `accepted --hours (default 1) but never passed it to the API, so it listed every scheduled run in the pool however far ahead` / `it computed the window from --hours but didn't use it in the work-pool branch` / `Both now pass scheduled_before to get_scheduled_flow_runs_for_work_pool` / `The CLI help text already describes the intended behavior; this makes the command match it` / `raising a TypeError when its optional contents argument is omitted or explicitly None` / `it currently assigns into None. Normalize only None to a fresh dictionary before adding metadata` / `The follow-up also resolves an omitted project name to path.resolve().name`；r532C 落地）
- **实证**：两个已合并 PR 是同一类缺陷的两端。① **传了但不生效**（#23300）：`prefect work-pool preview <pool> --hours N` 接受该参数（默认 1）却从未把它传给 API，结果列出池内**任意远**的全部计划运行；`work-queue preview --pool` 更复杂——它按 `--hours` 算出了 `window`，却在 work-pool 分支里没用上。修法是两条路径都把 `scheduled_before` 传给 `get_scheduled_flow_runs_for_work_pool`（非 pool 分支本来就是这么做的）。作者还留下一句关键自证：`The CLI help text already describes the intended behavior; this makes the command match it`——帮助文本早已宣称该行为，实际从未实现。② **没传就崩**（#23334）：`create_default_prefect_yaml(path, name="demo")` 的 `contents` 参数文档说省略则用内置默认，实际向 `None` 赋值抛 `TypeError`；修法是只把 `None` 归一成空字典，显式字典与「文件已存在则提前返回」保持原样；后续补的另一半：省略项目名时回退到 `path.resolve().name`。测试侧作者给了可复核的过程：原 5 例是 2 失败 3 通过，修后 5 通过，再加「两个可选参数都省略」扩到 6 例全通过，且**单独撤掉 name 回退会让新增回归红**（1 失败 5 通过）。
- **判据**：① **「参数存在」不等于「参数生效」**：本例 `--hours` 有默认值、有帮助文本、不报错，只是从不被使用 ⇒ 接口自测必须断言「改变该参数，输出应当随之改变」，只断言「命令不报错」永远测不出静默忽略。② **同一命令的多个分支要各自验证参数贯通**：`work-queue preview` 的非 pool 分支对了、pool 分支漏了 ⇒ 加分支（pool / 非 pool、远程 / 本地、批量 / 单条）时参数贯通要按分支逐一测，不能因为「主路径对了」就认为整条命令对了。③ **默认值会掩盖静默忽略**：默认 1 小时本应只列近一小时，实际列全部——用户若只看「有结果」不会发现 ⇒ 断言要造**窗口内 + 窗口外**两个样本，只造一侧的测试等于没测。④ **帮助文本 / 文档是契约的一部分**：作者在 PR 里明确「帮助文本已描述预期行为，本 PR 让命令与之一致」 ⇒ 文档与实现不一致时，修的可能是实现而不是文档；排查「文档说有这功能」时先别急着改文档。⑤ **「可选」的准入条件是有空值路径**：`optional` 参数被省略或显式传 `None` 都必须走通 ⇒ 凡是文档写了「省略则用 X」的参数，回归用例里必须有「完全省略」和「显式 None」两格，只测「传了正常值」会让可选参数实际变成必填。⑥ **归一化的边界要窄**：`Normalize only None to a fresh dictionary`——只归一 `None`，空字典与显式字典保持原行为 ⇒ 修空值路径时别顺手把「空值」和「空容器」混为一谈，两者在调用方语义上可能不同。⑦ **回退值也要有测试兜底**：单独撤掉 name 回退会让回归红 ⇒ 顺手补的回退逻辑必须配独立用例，否则下一次重构会把它悄悄删掉。⑧ **自证要给出前后对比数字**：本例「2 失败 3 通过 → 5 通过 → 6 通过 / 撤掉则 1 失败 5 通过」 ⇒ 验证记录写「改前失败、改后通过、反向撤除复红」三段，比只写「测试通过」可信得多。⑨ 与 §一条消息可堆叠多技能（sa 1.123.0）、§包内授权声明可被整条作废（sa 1.122.0）分工：那两条管**宿主如何展开 / 作废声明**，本条管**作者自己写的声明（参数、文档、默认值）与实现是否一致**，落点是技能 / 脚本对外接口的自测清单。
- 提升层：工具（接口自测）/ 工作流（回归用例设计）。触发词：参数被静默忽略、--hours 未传给 API、分支漏传参数、帮助文本与实现不符、可选参数省略崩溃、assigns into None、空值路径未实现、窗口内外双样本、完全省略用例、撤除复红。

## 测试里的外部依赖要用「无效 host」注入，让失败立刻发生而不是随机超时（来源：api.github.com/repos/activepieces/activepieces/pulls/16302，2026-10-12 r533B 一手 curl 200 逐串命中 `The agent eval gate failed at random on AI PRs` / `Tests that run an agent turn fetched the real model catalog from the CDN. When the CDN was slow from the runner, the first tests waited up to 10s and hit their 5s timeout` / `Worker tests now point the catalog at an .invalid host, the same way the API tests already do for model tiers, so the fetch fails at once and lookups fall back like they do with no catalog` / `Reproduced first: with AP_MODEL_CATALOG_URL on a host that never answers, 6 tests in 3 files timed out at 5s` / `Same hanging host with this change: 64 passed, 1 skipped`；r533B 落地）
- **实证**：Activepieces 的 agent eval 门在 AI PR 上**随机失败**。跑 agent turn 的测试从 CDN 拉真实 model catalog；CDN 从 runner 侧变慢时，最前面的几个测试等了最多 10s 撞上自己的 5s 超时。修法是把 catalog 指向 `.invalid` host（与 API 测试对 model tiers 已做的那样一致），fetch 立刻失败、lookups 像"无 catalog"一样走 fallback；eval 脚本复用 worker 的 vitest config 拿到同一套 setup。复现过程可复核：把 `AP_MODEL_CATALOG_URL` 设成永不响应 host，3 文件 6 测试 5s 超时；同 host 加此修复，64 通过 1 跳过（与改前 10 文件 65 测试一致）。
- **判据**：① **测试随机失败（flaky）几乎都是外部依赖没隔离**：本例"CDN 慢 → 前几个测试随机超时" ⇒ 任何偶发失败的测试，先查它是否偷偷依赖了真实外部服务（CDN/API/网络/时钟），而不是先怀疑测试逻辑。② **隔离手段是「让依赖立刻失败」而非「加长超时」**：作者没把 5s 调到 30s，而是把 catalog 指到 `.invalid` 让 fetch 立即失败走 fallback ⇒ 真正的确定性来自"依赖不存在时行为可预测"，不是"多等一会儿"；加超时只是把 flaky 变成"偶发更慢"，没消除根因。③ **无效 host 是标准隔离技法**：`.invalid` 是 RFC 2606 保留的永远不解析 TLD，配合已存在的 fallback 路径 ⇒ 注入"依赖缺失"比 mock 整个调用更轻、更真实（走的是生产 fallback 代码，不是测试替身）。④ **复用已有 setup 保持一致性**：worker 测试早已对 model tiers 用 `.invalid`，eval 脚本改用同一 config ⇒ 隔离策略要在全仓库统一，别让某些测试走真实依赖、某些走隔离，否则排障时无法判断"这次失败是依赖问题还是代码问题"。⑤ **复现先于修复、且用同一坏输入**：作者先用"永不响应 host"稳定复现 6 测试超时，再验证修复后同 host 下 64 通过 ⇒ 验证 flaky 修复不能靠"多跑几次碰巧绿"，要用能稳定触发坏输入的样本证明修前必红、修后必绿。⑥ **flaky 测试是发布门控的隐性债务**：eval gate 随机红会让人在 AI PR 上反复重跑、或习惯性忽略红 ⇒ 测试可靠性本身是可复用资产，不是"能过就行"。⑦ 与 §声明即契约（sa 1.124.0）分工：那条管"作者自己写的声明（参数/文档/默认值）与实现一致、自测清单"，本条管"测试本身对外部依赖的确定性"，落点是测试环境的隔离与 flaky 治理。
- 提升层：工具（测试隔离）/ 工作流（flaky 治理）。触发词：flaky test、外部依赖未隔离、CDN 慢导致随机超时、.invalid host 注入、立刻失败走 fallback、复用已有 setup、复现先于修复、确定性测试。

## 模板装配的顺序决定用户代码里字面量是否被毁：先把结构占位符在「 pristine 模板」上替换完，再注入用户代码到单一槽位，绝不回扫整段产物（来源：api.github.com/repos/langgenius/dify/pulls/43438，2026-10-12 r535B 一手 curl 200 逐串命中 `insert the user's source at {{code}} then replace every {{inputs}} occurrence with the base64-serialized input JSON` / `any {{inputs}} literal inside the user's own code ... is silently rewritten into the base64 input payload, corrupting valid Python/JavaScript programs` / `serialize the inputs and replace {{inputs}} in the pristine template first` / `then insert the user code at the single top-level {{code}} slot` / `No post-insertion substitution remains, so user-code literals are preserved verbatim.` / `Both Python and JS runners inherit the fix from the shared base class.`；r535B 落地）- **实证**：Dify code-executor 的装配顺序是：① 把用户源码插入 `{{code}}`；② 再对**整段已装配脚本**替换每个 `{{inputs}}` 为 base64 序列化输入 JSON。因为步骤 2 跑在装配后的产物上，用户代码里**自身的** `{{inputs}}` 字面量（字符串 / 模板串 / 注释）被静默改写成 base64 输入，合法 Python/JS 程序被毁（#43435 复现：用户字面量处返回 base64）。修复调换顺序——先在 pristine 模板上替换 `{{inputs}}`，再把用户代码插入单一顶层 `{{code}}` 槽；不再有「插入后替换」，字面量原样保留。Python/JS runner 从共享基类继承修复。- **判据**：① **装配顺序决定安全性**：先注入用户内容再整体替换占位符，等于把用户代码也当模板扫一遍 ⇒ 凡是「模板 + 用户内容」拼接，必须先把结构占位符在 pristine 模板上替换完，再注入。② **单一注入点优于多处替换**：用户代码只进一个顶层 `{{code}}` 槽 ⇒ 注入面收敛到一处，便于断言「用户内容没被二次解析」。③ **绝不回扫装配产物**：插入后不再做全局占位符替换，避免把用户字面量当占位符 ⇒ 任何「拼接后再扫描」的写法都会重复解析用户内容。④ **用户字面量必须 verbatim 保留**：用户代码里的 `{{inputs}}` 是数据不是指令 ⇒ 模板引擎要把「用户的文本」与「系统的占位符」严格分开，不能因为长得一样就替换。⑤ **共享基类保证多端一致**：Python/JS 从同一基类继承修复 ⇒ 多语言 / 多 runner 的装配逻辑要抽公共基类，避免一种语言修了一种没修。⑥ 与 §声明即契约（sa 1.124.0）、§测试依赖隔离（sa 1.125.0）分工：那两条管「参数声明 / 测试确定性」，本条管「模板装配的指令 / 数据隔离」，落点是 skill/runner 里用户代码拼接的安全顺序。- 提升层：可复用 Skill / 工具（模板装配安全）/ 工作流（注入点收敛）。触发词：assemble_runner_script、先插入用户代码再替换、post-insertion substitution、user literal corrupted、pristine template first、single {{code}} slot、verbatim preserved、共享基类。

## 技能供应链治理：immutable 发布 + 变更检测用内容寻址 + 更新是读变更之后做的决定（来源：GitHub CLI `gh skill` v2.90+ 文档 + mdr 仓库 2026 实证 + shskills 0.2 + mr.technology Skills 市场数据 + skill-finder，2026-10-12 r540B 实拉）

技能从仓库到 agent 的链路是一个供应链，供应链的每个环节都有确定的做法：

- **immutable 发布防历史被改**：`gh skill` 只认 tag/release 作为技能源，**release 不可变**——仓库被接管后 push 新 commit 改不了已发布版本。消费端 `skills install <repo>@<tag>` 或 `--pin <commit-sha>` 钉死精确版本，绝不使用 floating ref（默认分支）。判据：**能防"装的时候是好的、之后被人换掉"**——仓库托管方的口令丢失、账号被接管是真实威胁，浮动引用把已装技能的稳定性押在别人的账号安全上。
- **变更检测用 tree SHA，不用版本号比对**：`skills.status` 用 git tree SHA 检测内容变更（目录树任何文件一变，SHA 变）；provenance frontmatter 记录来源（repo/ref/path）+ 最后更新的 commit SHA。判据：**版本号可以不变而内容变**（上游忘了 bump），内容寻址才是变更的可靠信号——"要不要升级"看 tree SHA 是否变化，不看版本号高低。
- **更新是读变更之后做的决定（mdr 实证）**：mdr 监控 47,724 个 agent markdown，**19.9% 在 14 天内变化**（SKILL.md 19.4% / AGENTS.md 27.8% / CLAUDE.md 23.2%）；75 份字节精确副本中 **62.7% 是旧版本**——"钉住的"大多数其实是钉住了旧版。正确姿势：`mdr outdated` 退出码 2 供 CI 感知、`mdr diff` **先读变更内容再决定更新**、SHA-256 校验 + source commit 记入 lock 文件、>200 文件的仓库拒绝安装。判据：**"有更新"和"该更新"是两件事**——先看变更内容（是否修复了我依赖的行为 / 是否引入破坏），再决定更新；看到"新版本"就升，等于把供应链决策外包给上游的版本号。
- **CLI 治理参数簇（shskills）**：`--dry-run`（预览不落盘）、`--clean`（清理源上已不存在的孤儿技能）、`--strict`（冲突即中止）、`--force`（**内容变更**才覆盖）。判据：**安装是写操作**——先 dry-run 预览、冲突中止、孤儿清理、内容未变不覆盖，四个开关让批量安装可审计可回滚。
- **分层信源 + eval 采纳门禁（skill-finder）**：信源分四层——Tier 1 anthropics 官方 → Tier 2 知名团队 → Tier 3 高星验证仓库 → Tier 4 GitHub topic 搜索；采纳前先过 eval（waxa-eval：连续 2 轮零 unclear 收敛、分歧 reject、fork-and-fix 修复上游）。判据：**信源层级决定信任起点，eval 决定是否采纳**——Tier 1-2 降低审查成本但不过 eval 不装；Tier 4 的高星不等于已验证。
- **市场侧事实（mr.technology）**：180k+ 公共注册技能、4,200/周新增；Claude Skills Registry 审核 **5-12 天、拒稿率 31%**，主因注入模式 + 未声明网络调用。判据：**审核是供应链的最后一道闸**——装技能前过一遍"它声明了网络调用吗 / 描述里有注入模式吗"，这两条占拒稿主因，个人装技能时同样适用（与既有 §Agent 工具面安全"工具描述可注入"互证）。
- **提升层**：可复用 Skill（技能供应链）/ 工作流（更新决策纪律）。触发词：gh skill、immutable release、tree SHA 变更检测、provenance frontmatter、pin commit、floating ref 禁止、mdr outdated、先读变更再更新、62.7% 钉旧版、shskills --dry-run/--clean/--strict、Tier 分层信源、eval 采纳门禁、Skills Registry 拒稿 31%。

## Agent Skills 生态安全实证：stdout 捕获泄露 + 脚本捆绑 2.12x + 安装前审查纪律（来源：arXiv 2604.03070 + arXiv 2601.10338 + matrix.tencent.com（腾讯朱雀 2026-04-24）+ Snyk ToxicSkills 2026-10-12 实拉，r541A 落地，与 §技能供应链治理互补——那条管"安装/更新/发布流程"，本条管"生态级威胁实证与装前审查点"）

- **调试日志成为最大泄漏面**：17,022 skills 抽样 520 个（3.1%）含 1,708 处凭据泄漏，84% 开发者疏忽；76.3% 只能靠 NL 描述+编程逻辑联合分析检测；3.1% 纯 NL prompt injection 无任何代码。**print/console.log 占漏洞 73.5%——agent 框架把 stdout 捕获进 LLM 上下文窗口，记在日志里的凭据可被自然语言查询取回**；72% 硬编码凭据带 AI 辅助编程签名。
- **恶意 skills 组合攻击**：83 个中 37.3% 组合 Base64 混淆+反向 shell 等多模式；89.6% 可利用性经动态沙箱证实。Snyk ToxicSkills：3,984 个公开 skills 中 1,467（36.82%）含缺陷、76 个确认恶意 payload、5 个具名威胁组织跨平台；36% prompt injection。
- **风险统计特征**：>500 行 skills 漏洞概率 2.14x；含脚本技能 40.6% vs 仅指令 24.2%（OR=2.12）；依赖≥5 个 47.9%。OWASP Agentic Skills Top 10（AST10）2026-04 发布，覆盖 OpenClaw/Claude Code/Cursor-Codex/VS Code 并点明跨平台复用风险；腾讯朱雀 ClawHub 5 万+ skills 扫描，ClawHavoc 2026-01：1,184 恶意 skills、12 个被入侵发布者账号、24.7 万次安装、230 万美元被盗；AMOS macOS Stealer 变体经 skills 分发。
- **安装前审查纪律**：① 技能含 print/console.log 调试残留 → 查是否硬编码凭据（stdout 会被框架捕获进上下文）；② 脚本型技能（非纯指令）→ 漏洞率近 2 倍，重点审；③ >500 行技能 → 更易藏注入，逐段过；④ 依赖≥5 个 → 供应链面大，逐依赖核来源；⑤ 描述含 Base64/反向 shell/混淆模式 → 拒装；⑥ 装前看发布者信誉与更新时间，装后审计一次工具面。
- **判据**：① 凭据泄露的第一现场是日志不是代码——审查先扫 print/log 残留，再扫硬编码串；agent 的 stdout 捕获让"调试残留"升级为"可被自然语言检索的泄密通道"。② 脚本型/超长型/多依赖型是风险特征组合——三项命中任意两项按高风险审。③ 生态级数字（36.82% 缺陷率）说明"默认信任"不可维持——安装第三方技能按装权限流程审，不是按下载流程审。
- **提升层**：工作流（安全治理）/ 可复用 Skill（安装审查清单）。触发词：stdout 捕获泄露、print console.log 占 73.5%、凭据泄漏 3.1%、NL 联合分析检测、脚本捆绑 OR 2.12、>500 行 2.14x、ToxicSkills 36.82%、AST10、ClawHavoc、恶意技能组合攻击、Base64 混淆、安装前审查纪律、装前扫调试残留。

## 技能运行时加载的 6 级优先级谱系 + 会话快照 + Node 冲突命名（来源：docs.openclaw.ai/es/tools/skills + zh-CN/tools/creating-skills 2026-10-12 实拉，r541B 落地，与 §同名冲突留诊断日志互补——那条管"冲突怎么记"，本条管"加载顺序与运行时模型"）

- **6 级加载优先级（最高→最低）**：① Workspace `/skills` → ② Project `/.agents/skills` → ③ Personal `~/.agents/skills` → ④ Managed `~/.openclaw/skills` → ⑤ Included（随安装内置）→ ⑥ extraDirs + 插件技能。**同名冲突高优先级胜出**——同名技能在不同层级共存时，永远高优先级覆盖低优先级，不打平、不报错（是否留诊断日志见既有章节）。
- **roots 支持分组结构，识别即命中**：SKILL.md 出现在配置 root 下任意位置即被识别（**最深 6 层**），子目录只影响组织不影响识别——技能名以 frontmatter `name` 为准，目录路径可自由分组。
- **会话快照：清单会话内定格**：会话开始时对 eligible skills 拍快照，同会话所有后续 turn 复用该列表——**skills/配置改动下一次新会话才生效**。判据：调试技能加载问题时先问"这是本会话快照里的列表吗"——会话内改了技能文件不生效不是 bug 是快照语义。
- **Node 托管技能的冲突命名**：连入 Node 可发布其 `~/.openclaw/skills` 下技能；冲突时 **local/Gateway 保留原名、Node 技能获确定性 Node 前缀名**；v1 Node 托管技能要求**目录名 == frontmatter name**；需 `exec host=node node=<id>` 加载，**改文件后重启 Node host**。
- **symlink 显式开关**：`extraDirs` + `allowSymlinkTargets` 支持符号链接技能目录；Workshop 写符号链接目标需显式 `allowSymlinkTargetWrites`。
- **判据**：① 同名冲突的裁决是"优先级谱系"不是"后装覆盖先装"——装技能前先查同目录层级与目标层级，高优先级层已有同名技能时低层级安装是白装。② 快照语义下"改了不生效"要按会话边界排查——跨会话才刷新是特性。③ Node 技能命名是确定性的（前缀），不靠运气——冲突侧永远有可预测的新名字。
- **提升层**：工具（技能运行时加载）/ 工作流（调试）。触发词：6 级加载优先级、Workspace skills、Project .agents、Personal、Managed、Included、extraDirs 插件、同名冲突高优先级胜、roots 分组、最深 6 层、会话快照、清单会话内定格、变更下会话生效、Node 前缀名、目录名等于 frontmatter name、exec host=node、allowSymlinkTargets。

## SkillHub TRACE 评测五维 + no-skill 参照组 + 三线审核：平台侧评测要能证明"真实增益"，个人侧可借同一框架（来源：skillhub.cloud.tencent.com/announcements + cloud.tencent.com.cn/developer/techpedia/2618 + news.cn + tech.cnr.cn 2026-10-12 实拉，r541B 落地，与 §触发评测发布前盲测互补——那条管"个人发布前的盲测"，本条管"平台/第三方评测的维度体系与增益归因"）

- **TRACE 五维评测体系**：**T Trust**（安全红线一票否决——任一安全维度不过即拒）/ **R Reliability**（稳定性与可复现）/ **A Adaptability**（跨场景适配）/ **C Convention**（规范符合度）/ **E Effectiveness**（效果有效性）。判据：**安全是否决项不是评分项**——五维里 T 单独行使一票否决权，其余四维才是可加权打分的维度。
- **E 维度的客观对照设计**：**no-skill 参照组**客观对照实验 + 旗舰模型主观盲评——**只有带来显著真实增益才合格**。判据：评测"这个技能有没有用"必须回答"比没有它强多少"——用参照组做增益归因，不是跑一遍看绝对值；主观盲评防"知道品牌后的偏好偏差"。
- **三线并行审核（上架前）**：内容合规过滤 + 科恩实验室深度漏洞扫描 + 云鼎实验室 AI 模型安全评估——**三线全部通过才上架，任一不过即拒**；风险检测清单含供应链/命令执行/网络数据外传/文件敏感路径/prompt 注入/远程脚本执行/可疑混淆。判据：**平台侧上架 = 三线合议制**——个人装技能时把三条线压缩成自己的检查单（合规 → 静态扫 → 模型层评估），缺一条都不装。
- **发布者实名认证**（腾讯云人脸核身）后才可发布，每技能附安全评估报告。判据：**发布侧实名 + 报告留档是供应链的可追溯性**——装技能时先看有没有安全评估报告，没有报告的技能按"未审计"处理。
- **平台规模信号**：8万+ Skills、月下载 1700万+、5.3万+ 已审核个人技能；SkillPay 微信支付 AI 专属卡原生触发支付。判据：生态规模是选平台信号不是选技能信号——平台大不等于单个技能好，每个技能仍按五维+三线过。
- **提升层**：可复用 Skill（评测维度体系）/ 工作流（安全治理）。触发词：TRACE 五维、T Trust 一票否决、no-skill 参照组、旗舰模型盲评、真实增益、三线并行审核、科恩漏洞扫描、云鼎 AI 安全评估、实名认证上架、安全评估报告、SkillPay。

## Eval-first 六步迭代 + undertrigger 实证 + 重复工作打包信号（来源：skillsmp.com zebbern/agent-skills-authoring + anthropics/skills skill-creator + cherryhq skill-creator + skill-maker 2026-10-12 实拉，r541C 落地，与 §触发评测发布前盲测互补——那条管"发布前的归因盲测"，本条管"编写过程的 eval-first 循环与防欠触发"）

- **Eval-first 六步迭代**：① 建立基线——无技能时让 Claude 跑代表任务；② 写最小草稿——只够覆盖观察到的缺口；③ 换一个全新实例（Claude B）加载技能跑 2-3 个真实 prompt；④ 观察 B 的行为——哪里挣扎/哪里漏指令；⑤ 回到编写实例（Claude A）精修——把观察结果喂回去；⑥ 满意后扩大测试集。判据：**评测先于打磨**——先跑无技能基线、再写最小草稿、用新实例验证，比"先写完再补测"收敛快；两实例分离（编写者≠执行者）防"写的人知道意图所以跑得出效果"的自证偏差。
- **undertrigger 是 Claude 的已知倾向**（anthropics/skills 官方 skill-creator 明示）：「Claude has a tendency to undertrigger skills」——**description 是模型唯一看到的触发依据，防欠触发要把描述写得"推一把"（pushy）**：不只说技能做什么，还要写清"什么时候用、别错过"。判据：触发失败的常见原因是"描述太保守/太含蓄"——描述写作目标是"该触发时必然触发"，宁可过一点不可不足。
- **重复工作打包信号**：测试跑批后看 transcripts——若多个测试用例都各自写了相似的 helper 脚本/重复走同一步骤，**这就是技能该捆绑脚本的信号**（写成一次、放 scripts/、告诉技能用）。判据：重复出现=沉淀信号——一次出现是特例，跨用例重复就是技能内容。
- **判据**：① 迭代以"观察行为"为燃料，不以"感觉"为燃料——每次精修必须来自真实运行观察。② 最小草稿原则——只补缺口，不预写大而全；技能随测试集长大。③ 与 §触发评测盲测的分工：那条管"发布前验证触发是否该响/不该响"，本条管"开发中如何迭代到触发可靠"。
- **提升层**：可复用 Skill（编写迭代法）。触发词：Eval-first 六步、无技能基线、最小草稿、双实例 A/B、undertrigger 倾向、描述要 pushy、防欠触发、重复工作打包信号、helper 脚本捆绑、观察驱动精修。

## SkillTrustBench 模型底座评测 + wxa-skill-eval 配置驱动多模型：扫描器固定、只换模型；评测跑在提交审核前（来源：matrix.tencent.com SkillTrustBench + cloud.tencent.com.cn developer/2685200 wxa-skill-eval + cloud.tencent.com/developer/2687265 云鼎四道防线 2026-10-12 实拉，r541C 落地，与 §TRACE 五维互补——那条管"技能本体五维评测"，本条管"评测基建（换模型测安全扫描能力 + 上架前自动评测）"）

- **模型底座评测法（SkillTrustBench）**：**固定扫描器配置，仅替换底层推理模型**，观察不同模型作为技能安全扫描工具的表现——Claude Opus 4.6 与 GLM-5.1 在风险推断/指令关联分析/意图识别均衡性最佳。判据：**评测"哪个模型适合当安全扫描器"时，控制变量=只换模型、其余固定**——否则分不清是扫描器配置的问题还是模型能力的问题；该法同样适用于"选哪个模型做我的技能评测 judge"。
- **wxa-skill-eval：提交审核前自动跑评测**：微信官方开源评测工具，提交前自动跑完四维度评测输出可视化报告；**接云开发后一套配置驱动混元/DeepSeek/Kimi 等主流模型，不用单独注册各家账号**。判据：评测要前置到"提交前"并自动跑——手测覆盖不了质量维度，评测报告是上架材料的一部分。
- **云鼎四道防线自动化审查**：每个新增 Skill 经过多道自动化安全审查，详情页展示"安全检测"模块与完整报告——审查结果对消费端可见可查。判据：**审查结果要落到消费端可见的位置**——"审过"没有用户可见的证据等于没审；装技能先看检测模块。
- **判据**：① 选评测模型按"固定扫描器只换模型"的消融法——评测结论归因到模型能力而非配置差异。② 评测自动化+前置——提交前自动跑、报告留档，人工抽查兜底。③ 与 r541A 安装前审查纪律分工：那条管"装前个人检查清单"，本条管"平台/官方的评测基建怎么搭"。
- **提升层**：可复用 Skill（评测基建）/ 工作流（上架治理）。触发词：SkillTrustBench、固定扫描器只换模型、模型底座评测、wxa-skill-eval、提交前自动评测、配置驱动多模型、云鼎四道防线、安全检测模块、评测前置。

## Skill Workshop：技能创作过审批队列，代理不直接写 SKILL.md（来源：clawdocs.org/guides/skill-workshop + docs.openclaw.ai/start/why-openclaw 2026-10-12 实拉，r542A 落地，与 §安装前审查互补——那条管"装第三方前查什么"，本条管"技能创建本身的治理路径"）

- **创作入口与激活分离**：Skill Workshop（OpenClaw v2026.6.1 引入）让代理**通过 review queue 提议技能，而不是直接写 SKILL.md 文件**——技能先进评审队列，**人工批准后才激活**。判据：技能是可执行资产，创建=变更=审批；绕过审批队列直写 SKILL.md 等于把"上生产"混进"开发"。
- **治理四件套随创建流程走**：**audit trails**（谁提的/改了什么全程留痕）、**security scanning**（安全扫描随提议触发）、**hash binding**（内容哈希绑定防篡改）、**rollback**（出问题可回滚）。判据：审批不是"看一眼放行"，是四条记录线都落了才激活；没有哈希绑定的技能库，改没改过无从断言。
- **判据**：① 技能创作默认进队列，直写是例外（需显式授权）——人批准前技能不激活。② 治理四件套缺一不可——留痕（audit）+扫描（security）+防篡改（hash）+回滚（rollback），缺一个都是"假治理"。③ 与 §发布前盲测/TRACE 分工：那条管"技能质量与触发"，本条管"技能创建流程的审批与审计"。
- **提升层**：工作流（技能库治理）/ 可复用 Skill（创作流程）。触发词：Skill Workshop、审批队列、review queue、人工批准激活、audit trails、hash binding、回滚、创建与激活分离、直写 SKILL.md 需授权。

## description 双向剪裁：不只防欠触发，还要剪过度触发；1024 字符硬规格（来源：claude.com/blog/improving-skill-creator + support.claude.com + lobehub 2026-10-12 实拉，r542A 落地，与 §Eval-first undertrigger→pushy 互补——那条管"欠触发的方向性修正"，本条管"description 的完整调优闭环与硬规格"）

- **触发调优是双向的**：skill-creator 官方用**样本 prompts 分析当前 description**，同时剪 **false positives（过度触发）与 false negatives（漏触发）**——"too broad and you get false triggers, too narrow and it never fires"。判据：description 调优不是单向 pushy——**技能多了以后误触发与漏触发是同一个调优问题的两端**，只剪一边会把另一边养大。
- **description 硬规格**：**最大 1024 字符、不能含 XML 标签**；须包含"做什么 + 何时用"；技能多时"精确度"优先级上升。判据：规格是校验线不是建议——超长/含标签的 description 直接不合格；触发精确度随技能数量增长成为第一调优项。
- **触发测试用例**：官方触发测试目标"确保 skill 在正确时间加载"——测试用例覆盖该触发/不该触发两侧，评审时识别 over/under-triggering 风险。判据：触发测试与功能测试分开跑——"做得对"和"该不该上场"是两个计分板。
- **判据**：① 每次调 description 都要双侧样本——既能证明"该触发时触发"，又能证明"不该触发时不触发"。② 规格先行——1024/无 XML 是硬校验，装技能前也按此审。③ 与 r541C undertrigger 章分工：那条管"防欠触发的写作姿态（pushy）"，本条管"双侧剪裁闭环 + 规格 + 触发测试用例"。
- **提升层**：可复用 Skill（触发质量）。触发词：双向剪裁、false positives 和 false negatives、样本 prompts 分析、1024 字符、无 XML 标签、触发测试用例、过度触发风险、description 精度随技能数上升。

## 技能文件组织 checklist：跨文件无重复信息 + 引用按需加载（来源：anthropics/claude-code plugin-dev skill-development 官方 checklist 2026-10-12 实拉，r542C 落地，与 §渐进披露三级结构互补——那条管"分几层"，本条管"每层之间不许有什么"）

- **No duplicated information across files**：官方 skill-development checklist 把"跨文件无重复信息"列为测试项——核心概念只在 SKILL.md、详细文档只在 references/、工作代码只在 examples/、工具只在 scripts/。判据：**重复信息是漂移源**——同一事实写两处，改一处忘一处，文件间就开始互相矛盾；一处事实一个家。
- **References load when needed + SKILL.md <500 行**：引用文件按需加载（不进常驻上下文）；主文件超 500 行拆到 references/（复杂技能目标 300 行内）。判据：**500 行是体脂线不是目标线**——主文件瘦到"指令+骨架"，重文档全部下沉；读者按需拉取。
- **触发测试与内容测试分开列**：checklist 同时测"triggers on expected queries"（该触发时触发）与"content is helpful"（内容有用）——触发与内容两个计分板。判据：**触发对≠内容对**——两套测试分开跑，缺一个就有一个盲区。
- **判据**：① 任何新文件落地前问"这个事实在别的文件有没有副本"——有就引用，不复制。② 主文件 500 行内，重内容进 references/ 并确保"需要时加载"。③ 与 §description 双向剪裁分工：那条管"入口触发"，本条管"文件间组织卫生"。
- **提升层**：可复用 Skill（文件组织）。触发词：跨文件无重复信息、No duplicated information、References load when needed、500 行体脂线、触发与内容分测、一个事实一个家、文件组织 checklist。

## 渐进式披露 Progressive Disclosure：只有名称+描述常驻，细节按需加载（来源：lowtouch.ai《Context engineering after Claude 5》2026-08-04 + dreaming.press《Context Engineering the Anthropic Way》2026-08-18 + CSDN《别再堆 Prompt 了!Agent Skill「渐进式披露」才是 2026 年最该懂的上下文工程》2026-10-11 实拉，r543C 落地，与 §References load when needed 分工——那条管"文件级按需加载"，本条管"元数据级：什么该常驻"）

- **只有 name+description 常驻上下文**：技能/工具的细节指令、代码评审流程、验证程序全部下沉到按需加载——"Anthropic 把详细 code review/verification procedure 从 prompt 移进 skills，agent 选择性调用"。判据：**常驻的只有"它是什么"，怎么干按需才读**——把整份 procedure 常驻，就是让每个 turn 都为"偶尔才用的细节"付费。
- **Anthropic 实证：Claude Code 系统 prompt 削减 80% 无评测损失**（Claude 5 代，2026-07-24 官方 guide）：高表现 agent 从"巨型指令块"转向 lean prompt + 更好工具 + 渐进式披露。判据：**指令块大小与质量不是正比**——削减到必要+按需，评测不掉，成本大降。
- **过载工具同样处理**：部分工具定义延迟化，agent 使用时先搜定义再调——"ship more tools without paying for them every turn"。判据：**工具也按渐进披露**——定义不常驻，用时拉取；工具面可更大而每轮成本不变。
- **判据**：① 每个技能问"哪些必须在常驻（name/description/骨架），哪些按需（细节/例子/脚本）"。② 大 procedure 进 references/ 由技能按需引用，不塞主文件。③ 与 §References 分工：那条管"文件怎么组织"，本条管"披露的粒度与节奏"。④ 反模式：把完整评审流程写进主 prompt；每轮都加载全套工具定义。
- **提升层**：可复用 Skill（上下文工程 / 技能设计）。触发词：渐进式披露、Progressive Disclosure、只有名称描述常驻、细节按需加载、系统 prompt 削减 80%、工具定义延迟化、lean prompt、高信号 token。

## 编译器式格式符合度评分：发布质量门不看人气看规范（来源：arXiv 2604.16911《Skilldex: A Package Manager and Registry for Agent Skill Packages》2026-08-15 实拉，r543C 落地，与 §TRACE 规范符合度分工——那条管"评测维度之一"，本条管"发布前的自动格式门禁"）

- **compiler-style format conformance scoring**：Skilldex 对技能包做编译器式格式符合度评分，给 publisher **line-level 可操作反馈**（哪一行不合 Anthropic 技能规范）——grounded in 规范而非社交代理（star/安装量）。判据：**格式质量用规范裁决，不用人气裁决**——star 数可刷、符合度不可辩；发布前跑一遍自动扫描，收到"哪行不合规"而不是"评分低"。
- **skillset 抽象：相关技能共享公共资产**（vocabulary 文件 / templates / persona 定义）——"their outputs remain mutually coherent in a way independent installation cannot guarantee"。判据：**同组技能共享资产保证输出互洽**——独立安装的技能各说各话，共享词汇/模板/人设的输出才一致；把"经常一起用的技能"做成一个 skillset。
- **判据**：① 发布前跑格式符合度扫描，按 line-level 反馈修。② 一组技能输出要互洽时，共享资产（词汇/模板/人设）而不是各自复制。③ 与 §TRACE 分工：TRACE 管"整个技能好不好"，本条管"发布瞬间的格式门禁与同组一致性"。④ 反模式：拿安装量/star 当质量；同组技能各写一份重复模板。
- **提升层**：可复用 Skill（发布质量门 / 技能分组）。触发词：编译器式格式评分、Skilldex、line-level 反馈、规范裁决、skillset 共享资产、输出互洽、发布质量门、格式符合度扫描。

## Agent 多轮评测：评的是中间状态与工具使用，不只最终输出（来源：Anthropic《Demystifying evals for AI agents》2026-01-09 实拉，r543C 落地，与 §触发测试/内容测试分工——那条管"技能层面两计分板"，本条管"agent 系统层面的评测设计"）

- **agent 评测难点来自多轮性**：agent 多轮调用工具、修改状态、根据中间结果调整——"autonomy, intelligence, and flexibility"让评测比单轮难。判据：**多轮系统不能按单轮评测**——只看最终输出会漏掉"中途状态错但结果对"的路径。
- **覆盖中间状态与工具使用**：设计 eval 时包含 agent 在中间轮次的状态变化与工具调用序列（用了哪些工具、顺序对不对、状态改对没）——不只是 final answer。判据：**过程正确性与结果正确性分开测**——工具序列错而结果碰对，是脆弱的正确。
- **判据**：① 给 agent 系统写 eval 时列出"可观测点"：每轮工具调用、状态变更、中间产出。② 评分项覆盖过程与结果两栏。③ 与 §技能评测分工：技能评测测"该不该触发+内容对不对"，agent 评测测"多轮里走得好不好"。④ 反模式：多轮 agent 只按最终输出打通过率；把工具调用错误混在"结果正确"里放过。
- **提升层**：可复用 Skill（评测方法 / Agent 系统）。触发词：多轮评测、Agent evals、中间状态评测、工具使用序列、Demystifying evals、过程正确性、脆弱正确、多轮可观测点。

## 技能安全审查：折叠线以下藏注入 + 发布快照=你审过的版本（来源：SpecWeave《Skills Ecosystem Security Landscape》2026-10-03 + localskills《5 ClawHub Alternatives for Safer Agent Skills》2026-07-03 实拉，r544A 落地，与 §风险统计特征分工——那条管"哪些特征高危"，本条管"审查动作怎么做不漏"）

- **重点查折叠线以下（below the fold）**：攻击者常把注入放在长文件深处——粗看 review 扫不到的地方。判据：**装技能前把 SKILL.md 通读到底，不是扫一眼开头**——威胁藏在正文中后段；只看 description 和前半段的审查等于没审。
- **发布快照（frozen versioned artifacts）**：发布应该快照技能——"What you reviewed is what runs"，审的是哪一版就装哪一版，禁止发布后原地可变的技能源。判据：**审查对象 = 运行对象**——审完 A 版装到 B 版，等于没审；版本不可变才可追溯。
- **发布者身份可溯**：每个技能挂可追溯的 publisher identity（优先你已信任的组织）——"who wrote this?" 在安装前就有答案。判据：**先答'谁写的'再谈装不装**——无归属的技能是匿名投递，风险无法归因。
- **判据**：① 安装前通读 SKILL.md 全文（含折叠线以下）。② 用冻结的版本化产物，不用可变源。③ 未知发布者技能按最高风险档处理。④ 与 §风险统计特征分工：特征管"哪些高危"，本条管"审查动作的完整性"。⑤ 反模式：只看 description 就装；发布后原地改动；跳过发布者核查。
- **提升层**：可复用 Skill（安全审查）。触发词：折叠线以下、below the fold、注入藏深文件、通读到底、发布快照、frozen artifacts、审哪版装哪版、publisher identity、发布者可溯、匿名投递。

## frontmatter 官方硬约束 + 体积上限 + reference TOC（来源：Anthropic《Skill authoring best practices》2026-10-12 + anthropics/skills skill-creator 2026-05-21 实拉，r544B 落地，与 §体积预算分工——那条管"上限内怎么排序"，本条管"可机检的硬规范"）

- **name 硬约束**：≤64 字符、仅小写字母/数字/连字符、**不能含 XML 标签**、**不能含保留词 "anthropic"/"claude"**。判据：**名字是路由标识不是标题**——违反字符集/保留词，平台直接拒收或路由失效。
- **description 硬约束**：非空、≤1024 字符、**第三人称**（"This skill should be used when..."）、**写何时用不写做什么**、含具体触发场景。判据：**description 是路由元数据**——第三人称+触发条件让 agent 判"这条请求归不归我"；"helps with"类泛化短语是垃圾描述。
- **体积上限**：SKILL.md 保持 **<500 行**；逼近上限时**加一层层级+清晰指针**（告诉模型下一步去哪读），不是硬塞。判据：**500 行是路由预算不是内容预算**——超了不是删内容，是拆层级。
- **reference 文件 >300 行加目录 TOC**：大参考文件开头放目录+每节指针，SKILL.md 里说明何时读哪个文件。判据：**大文件先给地图再给内容**——模型按需跳读，不整文件吞。
- **validation checklist 机检**：SKILL.md 存在且 frontmatter 合法/name+description 字段齐/正文实质存在/**引用的文件真实存在**。判据：**机检先于人工审**——五项结构项扫完再谈内容质量。
- **判据**：① 新建/改技能先过五项结构机检。② 超 500 行拆层级不删内容。③ >300 行 reference 配 TOC。④ 与 §体积预算分工：预算管"正文取舍优先级"，本条管"硬规范边界"。⑤ 反模式：名字带大写/下划线；description 写"做什么"不写"何时用"；500 行超了硬塞；大 reference 无 TOC。
- **提升层**：可复用 Skill（规范 / 路由质量）。触发词：frontmatter 硬约束、64 字符、1024 字符、第三人称描述、何时用不写做什么、XML 标签、保留词 anthropic claude、500 行上限、拆层级加指针、reference TOC、300 行、validation checklist、结构机检。

## 方案沉淀成模板+验证器闭环：跑通的方案固化为"模板+验证器"可复用单元（来源：阿里云大模型 ACA 认证课程 V2.4.2 更新 2026-07-30 实拉，r544C 落地，与 §四块结构分工——那条管"固化的资产骨架"，本条管"固化后怎么自动把关"）

- **复杂任务分段协同执行，跑通后沉淀**：采访→调研→出计划→自检分段协同，把跑通的方案固化成**提示词模板 + 验证器**，形成可复用闭环。判据：**方案固化两件套——模板管"怎么做"，验证器管"做对了没"**——只有模板没有验证器，复用就是复制错误。
- **验证器是闭环质检**：下次套模板时验证器自动把关（输出形状/关键字段/质量阈值），不合格就返工。判据：**模板+验证器成对落库**——拆开用等于没闭环。
- **判据**：① 固化工作流时同时写验证器（判据量化：字段齐、格式对、阈值过）。② 与四块结构分工：四块管"Role/Inputs/输出格式/Hard rules 骨架"，本条管"加验证器闭环"。③ 反模式：只存模板不存验证器；验证器写"看起来不错"这种不可机检的判据。
- **提升层**：可复用 Skill（工作流固化 / 质检闭环）。触发词：方案沉淀、模板+验证器、分段协同执行、采访调研出计划自检、闭环、可复用单元、验证器把关、机检判据。

## Gotchas 章节是技能的最高信号内容：从常见失败点构建，随时间更新累积（来源：Anthropic 官方《Lessons from building Claude Code: How we use skills》2026-06-03 + Claude Platform skill authoring best practices 2026-10 实拉，r545A 落地，与 §三线审核分工——那条管"发布前审一遍"，本条管"技能长期养哪一节"）

- **技能里最高信号的内容是 Gotchas 章节**：frontend design skill 是例子（工程师迭代客户反馈改进 Claude 的设计品味，避开 Inter 字体和紫色渐变等经典模式）。**Gotchas 从 Claude 用你的技能时撞到的常见失败点构建**，并随时间更新累积。判据：**技能养护主战场 = 失败点清单**——不是功能清单，不是示例库；"Claude 在这里栽过跟头"是最高频、最不可替代的知识。
- **与渐进式披露的分工**：披露管"正文怎么分层放"，本条管"层里优先写什么"——Gotchas 应放进最容易被触达的部分（正文靠前或 reference 显眼处），而不是埋在细则末尾。
- **反模式**：技能只有"怎么做"没有"别踩什么"；Gotchas 写一次性问题（不更新不累积）；把已知失败点藏在折叠线以下让模型看不到。
- **提升层**：可复用 Skill（技能长期养护 / 失败知识沉淀）。触发词：Gotchas、常见失败点、技能养护、栽过跟头、最高信号内容、随时间更新、失败知识、Inter 字体紫色渐变反模式。

## 技能开发走评估驱动五步：先量缺口，再写最小指令（来源：Anthropic 官方《Skill authoring best practices》2026-10 + claude.dev《Automating eval design and hillclimbing》2026-09-28 实拉，r545C 落地，与 §Agent 多轮评测分工——那条管"评测设计测什么"，本条管"开发按什么顺序写技能"）

- **五步顺序（gap-first）**：① **Identify gaps**——无 skill 时跑代表性任务，记录具体失败或缺失上下文；② **Create evaluations**——建三个场景测这些缺口；③ **Establish baseline**——量无 skill 时的表现；④ **Write minimal instructions**——**只写刚好够补缺口、能过评测的内容**；⑤ **Iterate**——跑评测对比基线精化。判据：**先有缺口再写指令**——从失败倒推内容，不预判"可能永远不会发生的需求"。
- **指令是"补缺口的最小集合"不是"完整教程"**：skill 是修行为偏差点，不是文档搬运；够过评测就停，多了反稀释。判据：**每段指令都要能指回某个已记录缺口或评测失败**——指不回的段落是猜测性内容。
- **让 Agent 起草、人做删减纠偏**：人写初稿往往过度设计；Agent 先起草 SKILL.md，人只删减和纠偏。判据：**起草归模型、定稿归人**——模型写全、人删到最小，比人从零写更省更准。
- **提升层**：可复用 Skill（开发流程 / 评测驱动）。触发词：评估驱动、gap-first、Identify gaps、minimal instructions、基线对比、先量缺口、三个场景评测、无 skill 跑任务、Agent 起草人纠偏、迭代精化。

## 技能安装与版本治理：来源验证/版本钉死/安装前审查/审计日志；行为退化不抛异常须谱系追踪（来源：GitHub agents-best-practices《skills-and-connectors.md》2026-09-14 + CSDN《Skills 别再造 Agent 去造 Skills》2026-10-08 实拉，r545C 落地，与 §技能安全审查分工——那条管"技能内容里藏注入怎么审"，本条管"技能当软件一样安装与版本治理"）

- **安装前治理清单**：source verification（来源验证）+ publisher identity（发布者身份）+ **version pinning（版本钉死）** + review before installation + permission manifest（权限清单）+ static scan + runtime sandboxing + inventory/audit logs（清点与审计）+ removal/incident response（移除与应急）。判据：**装技能=装软件**——第三方技能按装权限的流程走，不因"只是个 Markdown"豁免。
- **Markdown-only 技能同样有风险**：纯指令技能也要审 prompt-injection risk、overbroad instructions（指令过宽）、hidden policy conflicts（隐藏策略冲突）、excessive tool permissions（工具权限过大）。判据：**注入不止藏在脚本里**——纯 Markdown 技能可以被设计成"什么都接"的过宽指令，同样要过审查。
- **技能版本治理：行为退化不抛异常**：技能演进直接改变 Agent 行为，失效方式比普通软件更隐蔽——**行为退化不会抛异常**。判据：**技能要版本+谱系追踪**——这次改了什么、影响哪些行为、出问题能不能回滚，都该可查；改技能按改代码的纪律（diff/回滚/测试）。
- **提升层**：可复用 Skill（技能治理 / 供应链安全）。触发词：技能安装治理、source verification、version pinning、版本钉死、安装前审查、permission manifest、审计日志、inventory、Markdown 技能风险、overbroad instructions、行为退化不抛异常、谱系追踪、装技能按装权限。


## 技能库只增不修会腐烂：把技能写成版本化「可证伪契约」，并让「契约评估与任务结果不一致」去驱动对既有技能的修订（来源：arxiv.org/abs/2610.11781v1（Skill-V）一手 export.arxiv.org 2026-10-13 r547B 实拉摘要逐串命中）
- **实证**：论文指出既有自演化技能库主要靠**累积新知识**成长——"Failures may lead to new skills, while **previously stored skills are less often revisited as new evidence arrives**"；但"growth alone does not ensure reliability, as **a retrieved skill may be inapplicable under the current task conditions**, and **an existing skill may encode a mis-specified operational boundary**"。Skill-V 的做法：把技能表示为 **versioned, falsifiable contracts that link semantic intent to observable behavioral criteria**（语义意图 ↔ 可观察行为判据）；由环境结果驱动库演化——**任务失败驱动技能新增，而"契约评估与任务结果不一致"（disagreements between contract evaluations and task outcomes）驱动对既有技能边界的修订**；修订的验收是**必须保留受保护的语义约束（preserve protected semantic constraints）且在历史回放证据上满足非回归判据（non-regression criteria for rubric-outcome metrics on historical replay evidence）**；另有 **applicability-aware filter** 排除被判为"确信不适用于当前任务"的候选。ALFWorld 95.3% / WebShop 85.9%，且**库比 growth-oriented 基线更紧凑**；适用性过滤减少错误技能调用，outcome-grounded 修订纠正错设的边界而不损害历史证据上的表现。结论原话："reliable skill evolution requires more than accumulating experience: **the library must learn which knowledge to retain, when to revise it, and when it should be applied**"。
- **判据**：① **"没出事"不是技能边界正确的证据**：技能被检索到 ≠ 适用于当前任务条件；既有技能可能编码了**错设的适用边界**，而这个错误只在检索成功、任务照跑的情况下静默生效 ⇒ 技能库必须有"既有条目被复审"的触发条件，不能只有"新增"触发器。② **修订触发器来自不一致，不是来自失败**：失败触发新增（知识缺口），**契约评估与真实任务结果打架**才触发修订（边界错设）——两者是不同的信号，只接前者会让错误边界永远留着。③ **技能写成可证伪契约**：语义意图必须挂到可观察的行为判据上，否则"这个技能什么时候该用"只能靠人读，随时间腐烂（与 sa KB:2083「自我声明的价值 = 它能多快被发现是假的」同构，本条给的是**契约形态**：版本化 + 意图↔判据绑定）。④ **修订的验收是双向的**：保住受保护的语义约束（不许借修边界改掉硬纪律）+ 历史回放非回归（不许修了 A 坏 B）——**修订不是重写**，两侧判据缺一即不可合入。⑤ **适用性感知过滤是独立机制**：检索命中后还要判"这个技能是否确信不适用"，命中不等于该用；过滤掉的候选要能追溯。⑥ **库更紧凑是可靠的副产品不是目标**：只增不修的库靠堆叠掩盖错设边界，修订机制带来的是"更小的库 + 更高的成功率"。
- 提升层：可复用 Skill（技能库演化与治理）/ 工作流（技能修订的双侧验收）。触发词：只增不修会腐烂、可证伪契约、falsifiable contracts、语义意图绑定行为判据、契约评估与任务结果不一致、不一致驱动修订、受保护语义约束、历史回放非回归、applicability-aware filter、适用性感知过滤、库更紧凑、outcome-grounded revision、错设适用边界。

## 失败轨迹是诊断源不是垃圾；干预必须在策略内实时生成，静态提示库与事后精炼都会退化（来源：arxiv.org/abs/2610.13594（MENTOR）一手 abs 页 42,694B，2026-10-13 r548C curl 200 实拉摘要逐串命中）
- **实证**：RLVR/GRPO 训练存在 "**zero-reward collapse**" —— 任务难度突增导致奖励信号整体消失。"**The conventional approach of discarding these failed trajectories is wasteful, as they contain valuable diagnostic information about the model's cognitive gaps**, a bright side that can be leveraged for recovery." 现有做法的失效："Existing solutions, however, often regress to static, '**off-policy-style**' interventions like pre-defined hint libraries or perform **post-hoc refinement**, failing to provide the adaptive, forward-looking guidance needed to escape the collapse." MENTOR 的做法："diagnoses the root cause of failure **in real-time** and dynamically generates targeted, instructional prompts to **guide the learning agent's next attempt**"；形态上是即插即用："As a plug-and-play module, MENTOR integrates seamlessly into existing policy optimization pipelines like GRPO **without modifying the training infrastructure**"（Llama-3.2-3B-Instruct 上平均相对提升最高 78.3%）。
- **判据**：① **失败样本的默认去处不该是丢弃**：它们承载的是"缺口在哪"的诊断信息 —— 只用失败来记一次错（或只在统计里占一个分母），等于把最贵的数据当垃圾回收 ⇒ **失败要留下"为什么会失败"的可机读归因，而不是只留一个 bool**。② **干预必须是"在策略内"的**：预定义提示库是 off-policy 的，它不与当前这次尝试的具体错误对齐 —— **泛泛的鼓励/通用技巧不构成纠偏**，纠正内容要与当下失败同分布、针对这一次的具体缺口。③ **干预要前向，不要事后**：目标是改变**下一次尝试**的行为，而不是事后给一个正确答案来修补记录 ⇒ **事后精炼改变的是档案，前向干预改变的是行为**，两者不要互相冒充。④ **先做实时根因诊断，再生成干预**：不复述失败现象而定位缺口，否则提示会落在已经掌握的地方 —— 对症的前提是诊断，诊断的前提是这次失败的现场证据。⑤ **改进机制应当以"附着"方式存在**：即插即用、不改动宿主基础设施 ⇒ **要求重写宿主才能生效的改进，落地率会被宿主改造成本吃掉**。⑥ 与 sa 1.139.0（失败驱动新增、契约评估与任务结果不一致驱动修订既有边界）分工：那条管**什么时候触发修订**，本条管**触发之后用何种干预才真的有效**（实时根因诊断 + 在策略内动态生成 vs 静态提示库 / 事后精炼）。
- 提升层：可复用 Skill（失败驱动的自我修订机制）/ 工作流（迭代纠偏环设计）。触发词：失败轨迹不丢弃、zero-reward collapse、on-policy 干预、off-policy 静态提示库、post-hoc refinement 无效、实时根因诊断、前瞻性引导下一次尝试、即插即用不改宿主、诊断信息高于通过率。

## r565A/r565B/r566A/r566C 下沉条目（元数据转义序列化 / 测试套件作改进信号 / 产物保留目标格式结构顺序 / 安装期校验宿主最低版本 + 内联技能归一身份）（原文均在 references/knowledge-base.md）

## r562C/r588C 下沉条目（技能装载接口钉住唯一标识形态 / 预烘物料按分发面与可见面分开取哈希 / 技能迁移性靠穿插教学 / 技能水印 1536 token 窗口）（原文均在 references/knowledge-base.md §r631A 下沉）

## 技能卫生要有「代价口径」：退役判据须同时观测上下文成本与调用频次，且「零通过」不等于「无贡献」（来源：code.claude.com/docs/en/changelog 4,644,825B 一手 curl 200 逐串命中 + arXiv 2610.32322《Beyond Gain: Skill Internalization for Agent Skill Retirement》abs 页 41,826B 一手实拉，2026-10-27 r631A）
- **实证**：①Claude Code changelog 原文「Added **`/skill-doctor`** to show **which loaded skills go unused and what they cost in context**, so you can prune them」——官方把「未被使用」与「占用多少上下文」放在同一条诊断里，另配 `[Claude Tag]` 按技能的运行频次遥测。②arXiv 2610.32322 原文：既有的 gain 规则（对比有/无该技能的两次运行）在「技能已被模型内化」与「模型与技能都做不到（uncovered）」两种情形下 **gain 都近似为零**；在 SkillsBench 上 **28/31 的退役决定建立在「没有任何一次运行完整通过」的探针上**；改用「扣住技能、按该技能合成的任务给模型打分，且仅当另一个模型确实从该技能获益时才采信高分（近一半高分来自没有模型受益的任务）」，无辅助判定的复现性更好（**Cohen's κ 0.42 vs gain 规则的 0.23**）但**跨模型不同**，须逐模型读。论文发布 1,251 技能 × 4 模型的任务与分数。
- **判据**：① **技能卫生要有成本维度，且成本与使用是两个独立指标**——「加载了但没用过」与「用了但很贵」是两种病灶；只统计调用频次会把常驻吃 context 却从不触发的技能判为健康，只看上下文占用会把低频但关键时救命的技能误删 ⇒ prune 依据必须是**「频次 × 上下文成本」双指标同表**，与 §r545A（Gotchas 是养护主战场）分工：那条管"内容养哪一节"，本条管"条目留不留下"。② **「零通过」不是退役的正当理由**——28/31 的退役建立在没跑通过的探针上，等于"模型从未真正用过"被当成"模型已经不需要它" ⇒ 退役判据必须证明**该能力确实已被内化**（扣住技能后仍能做，且别人用它确有增益），不能只证明"这次没跑通"。③ **uncovered 与 internalized 在 gain 口径下不可区分**——两者 gain 都≈0，用单一 gain 阈值退役会成批删掉"其实谁都不会做"的能力 ⇒ 凡"有/无对比"型收益指标，都要先问"零收益的另一种解释是什么"。④ **退役结论要按模型分别读**：κ 0.42 高于 0.23 但仍属中等一致，且跨模型结论不同 ⇒ 一个技能对 A 模型可退役、对 B 模型不可退役，"这个技能该退了"必须带模型主语。⑤ 与 §r547B（只增不修会腐烂 / 可证伪契约）分工：那条管**什么时候触发修订**（契约与结果不一致），本条管**什么时候触发退役**（内化 vs 从未受益的区分 + 成本口径）。
- 提升层：可复用 Skill（技能库卫生与退役治理）/ 工具（遥测口径）。触发词：skill-doctor、未使用技能、上下文成本、prune、退役判据、zero-gain、uncovered vs internalized、Cohen's kappa 0.42、28/31、逐模型退役、技能遥测双指标。

## 技能作用期内的「临时减权」与「条件式工具广告」：正负开关对称、广告按能力存在与否（原文已零删减下沉 references/knowledge-base.md §r631A 下沉，2026-10-27 r631A；触发词：disallowed-tools、技能期内减权、条件式工具广告、2% 清单预算）
