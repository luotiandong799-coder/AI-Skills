

## 本地来源（file:// 与本地路径）必须与远端同权入锁，否则本地安装就是审计盲区（来源：vercel-labs/skills commit bcdcee67「Record global installs from a local path in the skill lock」，2026-09-30 r320B api.github.com 实拉 200）
- 原文：`skills add -g <local-path>` installed the skill but left `~/.agents/.skill-lock.json` untouched: the lock write in `src/add.ts` was gated on `normalizedSource`, which `getOwnerRepo(parsed)` returns as `null` for a local source. 修复：`(normalizedSource || (parsed.type === 'local' && !directDownload))`，且 **The folder hash for a local source is computed from `skill.path`**；配套 `src/remove.ts`：**A local lock entry now holds an absolute path, so removal telemetry reports the source of local entries as `local` instead of sending that path.**（Fixes #2278）
- 判据：① 锁定文件的写入条件若绑在"有没有远端源"上，本地/私有来源就**整类漏记账**——结果是"装了什么"这件事对本地来源不可审计，也不可更新；② 本地来源同样要有**内容哈希**（对目录算 folder hash），否则无法判断"本地这个技能有没有被改过"，远端重钉、本地无感知；③ 遥测/日志里的本地条目必须**脱敏为 generic 标记**（`'local'`）而不是上传绝对路径——绝对路径等于把用户的目录结构外发；④ 判据化：任何"安装/引入资源"的动作，先问"本地路径这一路也记账了吗、也哈希了吗、上报时脱敏了吗"，三问缺一即视为有盲区。
- 提升层：工具 / 安全边界。触发词：本地来源入锁、file:// 审计盲区、folder hash、遥测脱敏、绝对路径不外发。

## §r321C — 自助撤回的资格由机器机检、撤回后同名禁发冷却窗、且必须给「不满足资格」的降级档（来源：docs.npmjs.com/policies/unpublish，2026-09-30 r321C 独立 curl 实拉 508,379B 原文核验）

- 原文/要点：① 撤回资格三条件（机器可判）："no other packages in the npm Public Registry depend on it"、"it had less than 300 downloads over the last week"、"it has a single owner/maintainer"；② 冷却窗："If you entirely unpublish all versions of a package, you may not publish any new versions of that package until 24 hours have passed"；③ 不可逆："once you have unpublished a package, you will not be able to undo the unpublish"；④ 降级档："If your package does not meet the unpublish policy criteria, we recommend deprecating the package"（不满足撤回条件 → 走 deprecate 而非硬撤）。
- 判据：① **撤回不能只靠申请人自述影响面**——"没人依赖我"必须由注册表侧机检产出（依赖反查 + 下载量窗口 + 维护者数量），自述会低估破坏面；② **撤回与重发之间必须有冷静期**：撤销即刻允许同标识符重发，等于给"替换包投毒"开一条零成本通道（先撤下可信包，再占位发同名恶意包）；冷却窗的成本是延迟，收益是让 watcher 有时间发现；③ **撤回必须显式声明不可逆**：把它当成"可撤销的撤销"会让用户在没备份的情况下执行；④ **撤回资格不满足时要有一条体面的降级档**，否则运营只剩"违规硬撤"与"什么都不做"两个极端——deprecate 保留可安装性但发出停用信号，正是中间档；⑤ 与已落「撤销=版本级状态机」分工：那条管撤销的**粒度**（单版本 deprecated / 整包 deleted）；本条管撤销前的**资格机检、撤销后的冷却期、以及不合格时的替代档**。
- 判非：Qoder r349-Q-C C1 同向，WB 本轮独立实拉取证且补齐"降级档 + 不可逆声明"两处 → 以本条为准；C3「撤销告知通道三件套」涉及 GitHub/MS 推送面，本轮未独立实拉 → 证据未达，不落。
- 提升层：工作流 / 治理。触发词：撤回资格机检、依赖反查、下载量窗口、24 小时冷却窗、同名禁发、撤回不可逆、deprecate 降级档。


## §r322B 日落登记的可机检化与支持窗计量（2026-09-30 r322B WB 独立实拉）

### 1. 日落是一条「有资格的登记项」，不是一段公告
- **实证**（独立 curl 实拉 `docs.openclaw.ai/plugins/compatibility.md`，200/14,100B）：每条弃用记录须含「an exact `removeAfter` date or named `removalGate`」，且「**a record with neither remains ineligible for removal**」＝没有日期就没有删除资格；状态机含 `active / deprecated / removal-pending / removed` 显式中间态；续期留痕且有上限——「preserves the original date as `previousRemoveAfter`, records the approval date as `renewedAt`, and sets a new `removeAfter` **no more than three months later**. **Renewal changes review timing only**」；CI 守卫「`pnpm check:doctor-deprecation-registry` guard **fails** when a record is still `deprecated` on or after `removeAfter`」。
- **判据**：把「弃用」从**散文承诺**升级为**带资格门槛的登记项**——(a) 无日期/无版本边界 ⇒ 无删除资格，机制化堵死"永久临时"；(b) 顺延必须留痕（原值 + 顺延日 + 新值）且有硬上限，且顺延只改复核时点、不改"终将移除"的承诺；(c) 过期由 **CI 判 fail**，不靠人记得看日历。
- 提升层：工作流。触发词：日落登记、removeAfter、removalGate、ineligible for removal、续期上限、CI 守卫过期即 fail。

### 2. 日落时点要落在可枚举、可 grep 的载体上
- **实证**（独立 curl 实拉 `api.github.com/repos/nodejs/Release/contents/schedule.json` base64 解码，5,325B）：`v24 {start:2025-05-06, lts:2025-10-28, maintenance:2026-10-20, end:2028-04-30}`、`v22 {end:2027-04-30}`——支持窗以**可解析字段**对外发布，下游可自动判定"我的运行时还剩多久被支持"。
- **判据**：任何"某能力在某日消失"的承诺必须同时存在于 **(a) 结构化字段** 或 **(b) 标识符/日历文件** 里；**只有散文版本的日落等于没有日落**（不可枚举即不可校验，也就无人会按时执行）。
- 与 §r322B.1 分工：那条管**单条登记项要有什么字段**，本条管**这些字段放在哪个可被机器发现的载体上**。
- 提升层：工作流。触发词：机器可读日落、schedule.json、支持窗字段、可枚举日落。

### 3. 引用/命名类破坏在存量侧永不自愈：升级与重装都不修
- **实证**（独立 curl 实拉 `code.visualstudio.com/updates/v1_139`，200/52,978B）：「Existing favorites, pinned launchers, and custom references to the old names are **not updated automatically**」——并给出人工动作（重新在默认应用设置里选择一次）；「**Reinstalling the package does not update saved references to the old names.**」
- **判据**：破坏性变更分三类处置——(a) **接口破坏**（编译/加载即失败，天然暴露）；(b) **引用/命名破坏**（旧引用不报错，只是指向空，且**不随升级或重装修复**）⇒ 发布检查单必须含"存量引用盘点 + 显式迁移动作/重装指引"，**严禁假设"用户升级即解决"**；(c) **数据/保留期破坏**（过点即永久）⇒ 告知必须写在删除动作之前并声明"升级不救数据"。
- 提升层：工作流。触发词：引用破坏、命名破坏、重装不修复、存量引用盘点、升级即解决的错觉。

### 本轮判非（不落）
- Make 把截止日写进文档 slug（Qoder r352-Q-C C2 ①）：WB 未独立实拉（本轮以 Node.js `schedule.json` 作独立证据载体，slug 形态登记为同源旁证，不单立条目）。
- Weaviate「支持最近三个 minor / 跳阶不受支持」、Dify 云版日志"升级不恢复"、NuGet `delete`=unlisting 与版本号永久占用（r352 C3 ②③ / r353 A4）：**本轮未独立实拉，登记为待补证据，不落地**。


## §r324A（2026-09-30 r324A 独立实拉）
- 原文：kendex「You list what you want in a `kendex.toml` file…It compares your list with what it found, and shows you **the difference before it changes anything**…kendex records what it installed, and **where each package came from, in a lock file**, so it can update it **or take it away** later.」「Delete a package from your list and the next apply removes its files, except ones you edited by hand and Pi extensions, which kendex keeps and reports.」；`gh api repos/anthropics/skills/releases` 返回 `[]`，HTML 页「There aren’t any releases here」。
- 判据：① **声明→差分预览→带来源锁**应作为跨宿主分发的固定三件套：先声明期望态（toml），再把「将要发生的差异」在**改任何东西之前**给人看，最后落一份带**来源**的锁——锁里没有来源就无法安全卸载，「可移除」是来源可溯的直接回报；② **卸载要分级**：机器写入的文件可删，人工改过的与第三方扩展要**保留并显式报告**，不能一把梭；③ **没有 release 制品面的仓库，引用它的唯一时间轴是 commit 日期**：`releases=[]` 是 API 级实证，凡写「自 vX 起」的版本化表述在这种仓上不成立，只能写 commit sha/日期；这同时意味着**以该仓为源的技能无法做版本比对与回滚**。
- 提升层：可复用 Skill / 工作流。触发词：kendex.toml、差分预览、带来源锁、可移除、人工改动保留、releases 为空、commit 时间轴。


<!-- ≤200 行统一迁移 2026-09-30（用户裁决）：自 SKILL.md 原文下沉，内容零丢失 -->

## 版本是不可变快照、端点决定谁跟最新版：默认端点自动漂移，生产必须钉具名版本（来源：AWS 官方《Amazon Bedrock AgentCore Developer Guide》`agentcore-runtime/agent-runtime-versioning` 2026-09-23 r144-A 独立实拉首读，此前未读）

- **原文事实**：AgentCore Runtime 每次更新自动生成**新的不可变版本**（"Versions are immutable once created"），且**每个版本自带完整自包含配置**（"Each version contains all the configuration needed for execution"）。端点层有两条路径：`DEFAULT` 端点**自动指向最新版本**；具名端点（如 `production-endpoint`）**必须显式更新才换版本**。
- **判据**：
  - **"最新版"是一个会自己动的目标，不能当生产依赖**：默认/隐式指向 latest 的入口，等价于把"什么时候变更"这个决定权交给上游；对外承诺稳定性的入口（生产、发布、对外契约）必须钉**具名版本**，升级是显式动作。
  - **可回滚的最小单位是"版本"不是"补丁"**：版本不可变 + 自包含，回滚＝把端点指回旧版本号，而不是"把改动改回去"。判据＝**这次回滚需不需要重新拼出旧状态**；需要拼，就说明当时没留不可变快照。
  - **环境差异靠多个端点表达，不靠多份配置**：dev/staging/prod 各指向不同版本，同一份不可变版本可被多个端点引用；**改环境 = 改指针，不改内容**。
  - **"更新了"不等于"对外生效了"**：更新动作改的是版本集合，端点不动则调用方看到的仍是旧版。发布收尾要核对**端点现在指向哪版**，不是只核对有没有新版本。
- 与 §破坏面评估 分工：那条管"升不升、破坏面多大"，本条管"升完之后谁在跟最新版、回滚往哪回"。
- 反模式：生产入口挂着 `latest`/`DEFAULT`；只记录"更新过"不记录"指到哪版"；回滚靠人肉重放改动；每个环境复制一份配置而不是共用一个不可变版本。
- **提升层**：工作流（发布与回滚路径）+ 可复用 Skill（技能/依赖的版本钉法同样适用——引用固定版本，不跟 latest）。
- 触发词：默认端点、跟最新版、latest 上线、版本钉死、具名版本、回滚到哪一版、不可变版本、环境指针、发布后没生效、自动漂移

## 可复现的门票是"输入集也要有版本"，不只是产物有版本（来源：Opik / Comet 官方 `resume_evaluations` + `evaluation/advanced/evaluate_agent_trajectory`（Opik 2.0 起 datasets 与 experiments 为 project-scoped），2026-09-23 r146-C 独立重拉首读，清单外新信源）

- **版本化不只管产物**：官方要求实验必须跑在 **versioned dataset** 上，否则不允许续跑、不允许复现（直接抛异常，不是警告）。判据：**只给产物打版本而输入集没版本，等于把"当时拿什么跑的"这件事丢掉了**。
- **抽样方式也是输入的一部分**：用了自定义 sampler 或显式条目 id 的实验，续跑还需要当初写下的本地 checkpoint，且**必须在同一台机器上**。判据：**"跑了哪些、按什么顺序跑的"如果只存在于当时的进程里，那次运行就不可复现**——要把抽样决策落盘成产物。
- **作用域要跟着版本一起写**：Opik 2.0 起数据集与实验是 **project-scoped**，创建时必须指定 `project_name`。判据：**版本号的命名空间要显式声明**，否则同名版本在不同项目下会互相覆盖或找不到。
- 与 §版本是不可变自包含快照 + 端点决定谁跟最新版 分工：那条管**产物版本与端点指向**（发布面）；本条管**输入/评测集版本与抽样可复现**（复现面）。发布能回滚不等于结果能复现——两件事各需要一套版本。
- 触发词：输入集版本化、评测集版本、复现门票、未版本化不许续、project-scoped。
## 幂等键的并发语义：默认隔离级别只防顺序重放，不防并发覆盖；真串行化必须显式配锁（来源：Prefect 官方 `docs.prefect.io/v3/advanced/transactions#idempotency` 2026-09-23 r147-A 独立实拉首读，清单外新信源）
- 同一 key 的「已提交记录」是幂等判据（`is_committed()` 命中即早退），但它只保证顺序执行的幂等；默认隔离级别 READ_COMMITTED 下，两个同 key 的并发执行会互相覆盖记录，谁先写完算谁的——"保证只执行一次"的默认实现并不防并发。
- 要真正防并发，必须显式把 `isolation_level=SERIALIZABLE` 且同时提供 `lock_manager`（内存 / 文件 / Redis 三选一）；只设隔离级别不配锁会静默退化成不防并发。
- 复现 / 重放的门票结论同源延伸：版本化数据集 + 锁，二者缺一则"可重放"是假的。
- 触发词：幂等键、隔离级别、SERIALIZABLE、race condition、lock_manager。
- 提升层：工作流（可复现 / 重放的安全前提）。

## 兼容性要在两个不同的面上分别判：存量引用会不会自动跟着变（来源：n8n 官方 `docs.n8n.io/connect/create-nodes/build-your-node/reference/versioning`，2026-09-23 r149-B 独立实拉首读，清单外新信源）

- **"不破坏兼容"在两个面上含义不同，先分清是哪一面**：官方的加载规则是——**已保存的引用继续用旧版本**（用户用 v1 建并存下的工作流永远留在 v1，即使发布了 v2）；**只有新建**才拿最新版。→ 判据：评估一次改动是否破坏兼容，**先问"存量引用会不会自动跟着变"**。不会自动变的，风险从"破坏存量"降级为"新老行为并存"（代价是长期维护两套行为，不是线上炸）；会跟着变的（共享库、默认值、全局配置）才是真破坏面。
- **版本化能力的上限由早期选的实现风格决定，不是后补的**：官方明确"声明式风格不能做完整版本化"，只能轻量版本化。→ 判据：**选实现方式时把"将来要不要完整版本化"一起算进去**；先选轻的再想重的等于重写。反过来，轻量版本化够用的场景（版本号写成数组 + 按 `@version` 条件显示）**不需要复制代码**——"多版本并存"和"代码复制一份"是两件事。
- **"哪个版本有哪些特性"只写一处，让展示层与执行层共用**：特性声明用**版本区间**表达（`gte` / `lte` / `gt` / `lt`，而不是逐版本列举），同一份声明既控参数可见性（`@feature` 显示条件）又能被代码查（`isNodeFeatureEnabled()`）。→ 判据：**两处各写一份"版本-特性"对照，必然漂移**；区间表达天然覆盖未来版本，逐版本列举每次加版本都要回来补一行。
- 与 §破坏性变更放最前标注 分工：那条管**怎么把破坏性变更告知用户**；本条管**先判定这次改动到底有没有破坏存量引用**——判错面会把"新增并存"当成"破坏"报给用户。
- 触发词：增量版本、旧引用钉旧版、兼容面判定、存量自动升级、新老行为并存、版本区间声明、特性声明单一来源、轻量版本化、不用复制代码。

## 关键环境的准入闸门要做成「动作级硬约束」，不是流程文档（来源：Vellum 官方 `docs.vellum.ai/product/deployments/release-reviews`，2026-09-23 r150-B 独立重拉首读，清单外新信源）

- 受保护标签（Protected Release Tags）：某个标签一旦被标为受保护，**除非该 release 至少拿到 1 个 reviewer approval 且没有未解决的 change request，否则这个标签打不上去**。评审不是"提醒你去做"，而是**打标签这个动作本身的准入条件**。
- 判据：**绕过的成本是不是等于完成它的成本** —— 要进生产就必须打这个标签，打标签就必须过评审，于是"跳过评审"和"不上线"变成同一件事。写成文档里的"上线前请评审"则随时可被跳过。
- 配套两条：评审结果要留**可审计的审批链**（谁批的、批了哪个 release）；审批状态是**两条件的与**（有批准 **且** 无未决变更请求），只看"有没有批准"会把"批了但改动没落地"放行出去。
- 与 §兼容性分两个面判 分工：那条管"改动会不会破坏存量"，本条管"改动有没有资格进入关键环境"。

## 按负载类型定超时与持久化策略，异步任务走 job 生命周期（来源：Fireworks 官方 `docs.fireworks.ai/guides/reliability.md`，2026-09-23 r151-C 独立实拉首读，清单外新信源）

- **超时不是「一个全局数」，是按负载类分档**：官方分 interactive/chat 30–60s、agentic（工具调用/多步）5–30min、长上下文大模型 10–30min、batch 提交 60s（结果异步）。判据：**给 agentic 用交互式的小超时，长任务会在中途被腰斩；给交互式用长超时，故障恢复被拖慢**。
- **connect/read 超时分开设**：官方 SDK 把 `connect=10s` 与 `read=1800s` 拆开——连接失败该快失败，读取慢是正常。判据：**把「连不上」和「算得慢」当两个独立旋钮**。
- **长任务提交即返回 job id，结果异步取**：batch 类「提交 60s 超时、结果另取」。判据：**凡是可能超过交互阈值的动作，默认做成「提交→轮询/回调」的 job 生命周期，不要阻塞调用方**。
- 与 §准入闸门做成动作级硬约束 分工：那条管「谁能打标签/上线」；本条管「不同动作该配多长超时、同步还是异步」。

## 升级/替换模型的破坏面要分「接口兼容」与「数值兼容」两面；数值面不报错，只能靠硬编码数值清单抓（来源：Pinecone 官方 `docs.pinecone.io/guides/search/rerank-results.md` 的模型退役公告与各模型参数表，2026-09-23 r153-A 独立实拉首读，清单外新信源）
- **接口没变、数值分布变了，同样是真破坏面，而且它不会报错**：官方公告 `cohere-rerank-3.5` 于 2026-07-01 废弃、2026-08-31 起由 `cohere-rerank-4-fast` 承接，并明确要求 `Because cohere-rerank-4-fast returns different relevance scores, re-tune any hard-coded score thresholds against it`。→ 判据：**升级审查里，「数值兼容」要作为一个与「接口兼容」并列的独立检查面**——请求照常返回 200、字段一个不少，唯一变化是数值分布，所以**没有任何异常会提醒你**；唯一能抓住它的是「硬编码数值清单」这个显式动作。
- **动作：升级/替换前先列「硬编码数值清单」，逐项比对**。至少覆盖：**判定阈值（分数/置信度/覆盖率）、超时、重试上限与退避基数、候选数量（top_k / batch size）、截断策略**。判据：**凡是被写死在代码/配置里的数字，都是这次升级的潜在受害者**；清单为空才可以说「本次无非接口破坏面」。
- **同一个参数名、同一个语义槽位，不同实现给的默认值可以相反**：官方参数表里 `truncate` 在 `bge-reranker-v2-m3` 上默认 `NONE`（**超长直接报错**），在 `pinecone-rerank-v0` 上默认 `END`（**静默截断**）。→ 判据：**替换同类组件时，默认值是必须逐项对照的字段，不能按「参数名一样行为就一样」推断**；一个报错、一个静默，对上层是两种完全不同的失败模式（报错会被看见，静默截断不会）。
- **同一件事有多条实现路径时，破坏面按路径分别算**：官方指出要「按请求选 query / passage 输入类型」只能绕开托管接口、改用 Inference API 自己算向量再传——即**托管路径做不了的事，自建路径能做，但代价面完全不同**。判据：评估升级影响时，先问「依赖这条能力的代码走的是哪条路径」，**同一条能力在不同路径上的破坏面不共享**。
- 与 §Dependency Guard 分工：那三条管**跨度 / 受影响 API / 破坏面分级**；本条补的是被漏掉的那一面——**数值兼容（阈值、默认值、截断行为）不体现在 API 面上，必须靠独立清单抓**。与 §兼容性要在两个不同的面上分别判 分工：那条管**存量引用会不会自动跟着变**；本条管**跟着变了之后，变的是接口还是数值**。
- **提升层**：可复用 Skill（升级破坏面评估）。

## 「名字」不是「身份」：同名重建不会把老引用救回来；成熟度阶段与失败策略都要写进契约（来源：Modal 官方 `modal.com/docs/guide/volumes.md` + `/guide/feature-maturity.md` + `/guide/retries.md`，2026-09-23 r153-B 独立实拉首读，清单外新信源）
- **引用绑的是不透明唯一 ID，不是名字，而且解析只发生一次**：官方明确 Volume 由**不透明唯一 ID** 标识，ID **在应用部署或启动时解析**；删除后再建一个**同名** Volume 会拿到**新的 ID**，而**已部署或正在运行的引用方会继续指向旧 ID，直到被重新部署或重启**，因此会「cease to function」。→ 判据：**「换个名字重来」「删掉再建个同名的」都不算迁移完成**；判断引用有没有跟上，唯一依据是**引用方有没有重新解析过**（重部署 / 重启），不是新对象有没有建好、名字对不对。这是「钉住名字」之外的一层——钉住的是名字，绑定的却是 ID。
- **成熟度阶段是可以写进契约的承诺，而且要分「接口稳定性」与「实现成熟度」两栏**：官方三阶段各自承诺明确——Alpha（**预期重大变化**，文档必须写明 limitations，部分需申请）；Beta（默认阶段，**可能仍在调整最终行为、定价与规模上限**）；GA（稳定、可用于生产，**无计划的破坏性变更**）。同时官方专门澄清：`_experimental_` 这类标记**只是 SDK / API 稳定性概念，不代表基础设施成熟度**，常见情形是 **API 早早稳定而后端仍在成熟**，也可能相反。→ 判据：**「这个依赖处在哪个阶段」不是形容词，是一组可引用的承诺**（能不能改、改多少、要不要申请）；**接口稳定 ≠ 实现稳定，两栏必须分开写**——合成一句「已稳定」会把「接口不变但后端仍在改」这种最常见状态藏起来。
- **破坏性变更落在版本号的哪一位，是有明文规则的**：官方声明破坏性变更**只发生在 `X.Y.Z` 的 `Y` 位递增**；弃用先**保持可用并持续告警**，之后再强制。→ 判据：**「这次升级会不会破坏我」可以从版本位直接读出来**——先看 Y 位动没动，再看有没有在吃弃用告警；两件都没发生，就不必按破坏性升级准备。
- **「什么时候允许整体失败」由进程类型决定，不由重试次数决定**：官方的两套行为——**临时 / 一次性应用**崩溃后重试，**超过失败率上限就整批失败并把异常上抛给调用方**；**已部署 / 对外服务**则**无限重试**，靠 **crash-loop 退避**给新建容器降速。→ 判据：**对外服务的失败策略不能是「失败就整体挂掉」**（那等于自断服务），只能「降速 + 持续重试」；反过来，批处理任务不能无限重试（那等于永不收敛）。**两个方向相反，判据是「有没有人在等这个进程活着」**。
- 与 §版本是不可变快照、端点决定谁跟最新版 分工：那条管**入口要不要钉版本、漂移从哪来**；本条管**钉住之后底层绑的是 ID 而不是名字，以及替换/重建为什么救不回已有引用**。与 §Dependency Guard 分工：那条管**接口面与数值面的破坏面**；本条补**成熟度承诺面与失败策略面**。
- **提升层**：可复用 Skill（发布与依赖维护）。

## 覆盖型配置的拆除顺序是硬约束；能靠「让请求等」解决的一致性，不要用「阻断发布」（来源：trigger.dev 官方 `trigger.dev/docs/deployment/version-skew-protection.md` + `/deployment/atomic-deployment.md`，2026-09-23 r153-C 独立实拉首读，清单外新信源）
- **覆盖型开关在「无害」与「全挂」之间没有中间态，而且它随时会跳过去**：官方写明，只要环境变量 `TRIGGER_VERSION` 指向的版本在那个环境里**存在**，它就**持续获胜**（所以新旧两套机制能共存、没有坏的中间状态）；但**一旦它指向该环境不存在的版本，每一次触发都直接以 `422` 失败**，而被它压制的机制根本救不了。→ 判据：**删除一个「覆盖型配置」的动作顺序是硬约束**：①先确认接管者真的生效 → ②再删覆盖者。官方把这两步的前后写死了（第 4 步不可选，且不能早于第 2 步）。**风险不是「删了回到默认」，而是「不删就永远留着一颗随时引爆的雷」**——它今天赢得很安静，明天上游一换版本就变成全量 422。
- **迁移时不能假设「新的上了、旧的自动失效」**：两套机制能同时在场且不冲突，恰恰是因为其中一个「keeps winning」。→ 判据：**判定迁移是否完成的唯一依据是「现在是谁在赢、退出条件是什么」**，不是「新的已经部署了」。残留的旧开关不会报错，它只会继续按自己的优先级决定行为。
- **同一类一致性问题有两条相反的路线，优先选「等待式」**：官方给的对比很清楚——**阻断式（原子部署）**：每次发布做**两次**部署、**阻断**上游发布直到本侧构建完成、必须关掉上游的自动域名分配、只覆盖生产环境、靠一个环境级设置来配置；**等待式（版本偏斜保护）**：一次部署、**从不阻断**、不改上游任何开关、覆盖生产/预发/预览三个环境、「**id 本身就是契约**」无需配置。代价差异也很直白：等待式下「构建落地之前触发的运行会**先等、再跑在正确版本上**」，阻断式下这些运行「跑在上一版」。→ 判据：**能用「让请求等一会儿」换到的一致性的，就不要用「卡住上游发布」换**——前者把代价放在延迟上（可控、可观测），后者把代价放在耦合与失败面上（上游被卡住、配置多一层、环境少覆盖一个）。反过来说，**只有当「必须先拦住、绝不允许跑在旧版」才是硬需求时，阻断式才值得**。
- **约定优于配置在这一条上的具体形态**：等待式方案明确说「无需任何配置——**id 就是契约**」。→ 判据：**凡是要靠一个额外开关才能成立的一致性保证，都是可以在迁移里被漏掉的那一种**；把契约压在**已经必然存在的东西**上（如本次部署的 id），就消除了「忘了配置」这个失败模式。
- 与 §版本是不可变快照、端点决定谁跟最新版 分工：那条管**入口要不要钉版本、漂移从哪来**；本条管**跨系统发布如何保持版本一致：用阻断还是用等待，以及覆盖型开关怎么安全退役**。与 §关键环境的准入闸门要做成动作级硬约束 分工：那条管**发布门禁怎么做成绕不过去**；本条管**部署期间的版本错配怎么消掉**。
- **提升层**：可复用 Skill（发布与依赖维护）。


## 评测集不是真理，是会烂的版本化产物：四个静默腐烂点（来源：Future AGI《LLM Eval Data Drift Detection in 2026》，2026-09-23 豆包 r155-B 实拉取证，2026-09-24 r156-B WB 审计独点属实后落地）
- **①把 golden set 当 ground truth 而不是 versioned artifact**：永不刷新 → 它慢慢变成"只代表上线那天"。判据：**golden set 必须带版本号与 changelog，改了要能说清改了什么**。
- **②没有输入分布监控**：生产分布漂移、长尾失覆盖，评测分照样好看。判据：**评测集要定期补生产日志样本**，否则它测的是旧世界。
- **③prompt 模板与数据集分仓版本化**：模板上了线、数据集还在评旧契约。判据：**模板与数据集的兼容性是一次发布的一部分**，不能各自发布。
- **④没有检索语料快照**：索引会动，数据集在测一个已不存在的检索结果。判据：**依赖检索的评测必须钉语料快照**，否则失败可能是语料变了而不是 agent 退步。
- 配套缓解：changelog + provenance 元数据 + 版本化发布 + schema 校验 + 补生产样本。
- 与 §输入/评测集版本化 分工：那条管「没版本不许续跑」（能不能复现）；**本条管「有了版本之后它是怎么烂的」**（还是不是原来那个东西）。


## 组件身份用只读指纹钉住：指纹不变不等于内容没变（来源：CrewAI 官方 `docs.crewai.com/v1.15.22/en/guides/advanced/fingerprinting`，2026-09-24 r157-A 独立实拉首读）
- **身份三件套，且只读**：每个组件创建时自动拿到 UUID + 创建时间戳 + 可自定义 metadata；UUID 与时间戳**不可手动设置、不可覆盖**，指纹通过只读属性暴露。判据：**审计链要的是「谁在什么时候被造出来」，这个字段不能由被审计方自己填**。
- **★改了属性，指纹不变**：官方示例明确「把 agent 的 goal 改掉，指纹完全一致」。判据：**指纹稳定 ≠ 行为稳定**——拿指纹做「有没有变」的判断会全部漏掉内容级变更；内容变更要靠内容哈希/版本，不靠身份指纹。
- **需要跨运行对齐时用确定性指纹**：`Fingerprint.generate(seed=...)` 同一个 seed 恒得同一个指纹，可带 metadata。判据：**随机指纹用于「这次运行的这个实例」，确定性指纹用于「跨运行认出同一个东西」**，两种用途别混用。
- 与 §「名字」不是「身份」 分工：那条讲**同名重建救不回老引用**；本条讲**身份字段本身不该变、以及它不能拿来证明内容未变**。


## 能力换代会让旧参数失效：迁移必须重审"禁用类 / 档位类"设置（来源：Pydantic AI 官方 pydantic.dev/docs/ai/capabilities/thinking，2026-09-24 r160-C 独立重拉首读）
- **★换代是"旧写法被移除"而不是"被兼容"**：扩展思考（`type: enabled` + `budget_tokens`）在 Opus 4.6 上已弃用，在 4.7 / 4.8 / 5 / 5.5 与 Sonnet 5 上**直接移除**，必须改用自适应思考。判据：**升级模型版本时，"禁用/档位/budget"这类设置是首要重审对象，其它参数可以先放**。
- **★同一族内不同代的组合约束不同**：Opus 5 在**显式禁用思考**时会拒绝 `xhigh`/`max` 档（Opus 4.8 却接受这组组合）→ 迁移时"原来能跑的参数组合"会变成 400。判据：**约束是"模型 × 设置组合"级别的，不是模型级别的**。
- **★"能不能关"逐代收紧**：Opus 5.5 已无法禁用思考（禁用请求在每个档位都被拒），要降开销只能改 `effort`。判据：**把"关闭某能力"写进方案前先确认目标版本还支不支持关**。
- **★成本字段是子集不是增量**：思考 token 计入 `output_tokens`（可读子集，不是额外加项），没有思考时该字段**整个省略**。判据：**做成本归因时不要把它当成加项重复计，也不要因为字段缺失就判定计量坏了**。
- **框架提前拦而不是让厂商报错**：不合法的组合会在发请求**之前**抛用户错误，而不是等厂商的 400。判据：**"报错来自本地"通常意味着这是已知约束，去查组合表而不是去查网络**。


## 派生数据的生命周期：底座一换，存量整批失效（来源：豆包 r160-C 实拉 Swfte 2026-05-04 + Red Hat Enterprise guide，2026-09-24 WB 审计裁定落地）
- **★五档刷新模式，按新鲜度与成本选**：Batch nightly reindex（4–12h，稳定语料）／Incremental upsert（分钟级，小文档）／CDC streaming（秒级，库驱动）／Versioned shadow index（秒级，**零停机**）／Manual（策展内容）。判据：**先定"允许陈旧多久"，再选刷新档**。
- **★生产上多数是"增量 + 周期全量补漏"**：增量负责新改文档，每周全量负责兜住增量漏掉的。判据：**只做增量一定会积累静默缺口**。
- **★换底座模型＝存量全部失效**：升级 embedding 模型后，**已有向量与新查询不再处于同一语义空间** → 必须全量重建或分阶段迁移（双版本并存）。**改切分策略同理**。判据：**任何"由旧底座算出来的派生数据"在换底座那一刻起就作废，这不是性能问题是正确性问题**。
- **自动化刷新消除的是"隐藏的陈旧答案"风险**：陈旧索引不会报错，只会给出看起来正常的旧答案。判据：**没有刷新机制时，失败模式是"答得挺像但已经过期"**。


## 发布三线并行安全门 + 回滚就绪（来源：腾讯 SkillHub skillhub.cn 实拉，2026-09-24 r166-B 独立实拉首读）
- 上架前三线并行安全扫描：内容合规过滤 + 漏洞扫描（科恩实验室）+ AI 模型安全评估（云鼎实验室），全过才上架，任一不过即拒——是 AND 门不是 OR。
- 实名认证是发布身份前提：发布者身份经核身后才允许发，信息加密只用于核实。
- 版本可追溯随时回滚：每次发布版本留痕，出问题可回滚到上一可用版本——发布前必须确认回滚路径存在且验证过。
- 判据：任何对外发布的技能或产物，发布门 = 多道独立安全检查全过加回滚就绪；少一道就别发。

## 运行中代码的版本策略：钉死还是自动升级，决定兼容性责任归谁（来源：Temporal 官方 docs 2026-09-25 独立实拉 —— worker-versioning、patching）
- **每个运行中的任务都要显式声明版本行为**：`Pinned`（钉在当前 worker 版本）或 `Auto-Upgrade`（自动跟到最新版本）。**选 Auto-Upgrade 就等于把「代码要能重放旧执行」的兼容性责任接过来**——必须自己用 patch/version 分支保证旧历史在新代码上跑得通；选 Pinned 则安全但会停留在旧代码上。→ 判据：**版本的兼容性责任跟着策略走**——没有声明策略的「顺手升级」等于默认承担了兼容性风险却没人管；与 rel §换底座模型＝存量全部失效 同源：**改动对存量任务的生效范围是发布决策的一部分**。
- **「独立动作」要单独识别**：跑在**不属于本流程所属版本队列**上的动作称为独立动作——它按自己队列的当前版本启动，不跟随调用方的版本。→ 判据：**跨队列/跨服务调用会切断版本继承**，这类调用的版本语义要单独声明，不能想当然认为「调用方什么版本它就什么版本」。
- **新执行继承版本是有条件的**：子流程**只在它的队列属于父流程那个版本时才继承**父版本，否则从自己队列的当前版本起；Continue-As-New 链会继承 Pinned 版本。→ 判据：**继承链里只要有一跳跨到别的队列/别的服务，版本继承就断了**——发布时要沿继承链逐跳确认，而不是只看入口那一处。
- 提升层：发布 / 工作流。

## r184 候选池消化（来源 Qoder r210 / r211 · 2026-09-25 实拉核验，4 点全库 0 命中净新）
- **审核同线程勿开替代 PR（210B8）**：发版前的代码审核必须在**同一 thread/PR** 上推进，不要另开一个"替代 PR"绕过已开始的评审；替代 PR 会让评审上下文分裂、已提意见作废。判据：评审进行中只更新原 PR，新开 PR=评审失效。
- **迁移丢失清单（210B12）**：做技能/配置迁移时维护一份**丢失清单**——哪些字段/行为/默认值在目标格式里没有对应、会静默丢失；清单空才叫"无损迁移"，非空必须显式告知用户并给兜底。
- **官方 validator 契约＋lenient 两档自建（211C6）**：有官方校验器就用官方契约（字段/格式以官方为准）；没有时自建**两档**校验器——strict（发布门用，全过才发）与 lenient（本地预览用，只标可疑不阻断）；两档共用同一份规则定义，lenient 只是放宽阈值。
- **默认值翻转写迁移语义（211C8）**：当某个默认值**翻转**（true→false 或反之）时，必须写一条**迁移语义说明**——旧用户在哪天之前按旧默认行为、之后按新默认，且提供回退开关；默认值翻转本质是行为破坏性变更，不准"悄悄改"。

## 主环境升级前必须存在"可回退点"：备份 → 隔离试跑 → 再升级主环境（来源：Langflow 官方 `docs.langflow.org/next/release-notes`，2026-09-25 r188-C 独立实拉首读复核；本条来自 Qoder r222 批在 live 的未版本化写入，经实拉复核后正式落版）
- 官方原文（升级隔离）：`If you want to isolate the new version, you must install Langflow Desktop on a separate physical or virtual machine, and then import your flows to the new ...`。→ 判据：**"就地升级 + 出问题再回滚"不是回退方案，是赌博**——真正的可回退点由两件东西组成：**可导入的数据备份（导出）** + **一个与生产隔离的、跑过新版本的验证环境**；**破坏性变更只有在隔离环境里验证过才算验证过**。
- **★升级动作的顺序不可压缩**：先导出备份 → 在独立 venv / VM / 容器装新版本 → 导入数据跑一遍 → 通过后再升主环境。→ 判据：**升级路径上"备份"和"隔离"是两道不同的闸**——备份防的是"回不去"，隔离防的是"没试过就上"；**只做备份不隔离 = 带着一份可能已经被新版本写坏的数据回退**。
- 与 §依赖版本按引入时刻冻结 + 升级前先快照（wb-skill-authoring r187-A）、§版本兼容单向不等式（wb-execute-discipline r188-A）分工：那两条管**版本怎么钉、两端谁先动**；本条管**动之前必须准备好什么**——**可回退点是升级的前置条件，不是升级失败后的补救**。
- **提升层**：工作流 / 部署（升级与回退）。

## 会让整体失败的外部依赖，必须写成前置检查而不是"注意事项"（来源：同 `docs/api_data_update.md`「Notes」，2026-09-27 实拉）
- **原文要点**：全文末尾 Notes 只有三条，其中两条是硬前置：`The \`git\` binary must be available in the server's PATH.` 与 `The server must be able to reach \`github.com\` on port 443.`
- 判据：**把"没有它整条链路就跑不起来"的条件写进 Notes，等于把一次部署期就能发现的缺失推迟成一次运行期的报错**。缺失 `git` 时这个功能不是"降级"，是 100% 失败——失败现场表现为 `exit status 128`，和真正的网络故障、权限问题长得几乎一样，于是排查从"环境少了个二进制"变成"为什么 clone 不通"。
- 落地形状：这类依赖要在**启动自检 / 部署清单**里显式列出并当场验证（二进制在 PATH？目标主机端口可达？），验证失败要**在调用之前**报出，而不是等第一次真实调用。判据：**一个条件的失败概率与失败成本都高，它就该有独立的检查点**；只写在文档里，检查点就落在了读者的注意力上。
- 反模式：把前置依赖塞进 README 的 Notes / 注意事项章节；或只在使用失败后的错误信息里才提到"可能需要安装 X"。
- 与 §主环境升级前必须存在"可回退点" 分工：**那条管"升级动作之前要准备好什么"，本条管"运行/部署之前要先验掉哪些会致命的缺失"**。
- **提升层**：部署 / 工作流。

## 依赖启动要有健康门，进程要分级，循环依赖用"持续重试"破解（来源：腾讯 AI-Infra-Guard `docs/api-checker-integration.md` Docker Compose 段，2026-09-27 r198-C 实拉）
- **★先起依赖、健康后再起主体**：依赖服务暴露健康检查端点，主体启动前先探活，不健康就不起。判据：**同时启动 = 主体必然在依赖未就绪时打一批超时，然后要么崩要么带着降级状态继续跑**。
- **★把循环依赖改成"一方持续重试连接"**：A 要等 B、B 又要等 A 时，让其中一方启动后**持续尝试连接**而不是声明依赖关系，环就解开了。判据：**声明式依赖图表达不了"可以晚到但不能不到"，强行声明只会让编排器拒绝启动**。
- **★进程要分关键与非关键，重启策略不同**：关键进程退出 → 整体重启（它的状态不可重建）；非关键进程退出 → 由入口脚本单独拉起，**不影响关键进程**。判据：**一律整体重启 = 一个辅助组件的抖动把主服务拖着一起冷启动；一律单独拉起 = 关键进程带着残缺状态继续服务**。
- **★最小暴露面：内部端口不上宿主映射**：辅助服务的端口只开在内部网络，绕过统一访问控制等于绕过鉴权、审计与限流。判据：**多开一个映射端口，就多一条不走网关的路**。
- **★升版时先修正数据卷权限，再降权运行**：旧卷的属主可能是 root，升级脚本要先把权限归位，然后以非 root 用户跑业务进程。判据：**直接降权跑，第一个写操作就会因为卷不可写而失败，而报错会指向业务代码而不是权限**。
- 与 §前置检查（外部依赖）的分工：那条管"运行前把依赖查一遍"；本条管"运行时这些依赖按什么顺序起、挂了各自怎么办"。

## 改一个共享文件，必须连带 bump 所有 import 它或受它影响的组件版本（来源：Pipedream docs《Components Guidelines and Patterns》§Versioning，2026-09-27 r200-A 实拉 43,774B）

- **★版本号声称的是"内容"；改动传播到依赖方之后，依赖方不 bump 就等于版本号在撒谎**：原文规则 "if you update a file, you must increment the versions of all components that import or are affected by the updated file"。判据：**改的是共享文件，bump 就不是一次而是 N 次**；只 bump 被直接编辑的那个文件，等于给下游发了一个内容变了、版本号没变的包。
- **★本地反复自增出来的版本不是发布版本**：开发期在自己账号里可能已经把版本推到 `0.1.5`，提交时要把它"归位"到注册表里应有的号（新增组件 `0.0.1`；原版本 `0.1.0` 修 bug → `0.1.1`）。判据：**发布版本号按"这次改动相对已发布版本属于哪一档"算，不按本地累计自增算**。
- **★改动级别与三档号要对齐**：MAJOR=不兼容 API 变更 / MINOR=向后兼容地加功能 / PATCH=向后兼容地修 bug。判据：**先定性再 bump**——凭"改了不少就加 MINOR"，会一路把破坏性变更藏进小版本。
- 与 §依赖健康门、§循环依赖 的分工：那两条管"依赖能不能升、升之前过什么门"；本条管"**升级动作本身要传染到哪些版本号**"。
- 提升层：工作流 / 可复用 Skill。

## 安装态声明式对账：启动即 reconcile，缺失即装、版本即纠、**多余即卸**（来源：docs.n8n.io`integrations/community-nodes/installation-and-management/environment-variable-installation.md` 2026-09-28 r283-C 独立 curl 实拉原文核验）
- **实证**：`N8N_COMMUNITY_PACKAGES_MANAGED_BY_ENV=true` → 原文 "n8n **reconciles the installed packages against the list on every startup, installing missing packages, correcting versions, and uninstalling packages not in the list**"，且启用瞬间就会卸掉不在名单内的包（官方用 warning hint 强调），**Community nodes 设置页同时转为只读**；每条 `{name, version?, checksum?}`，`checksum` 为 **SHA-512（`sha512-...`）且要求 `version` 已设**；未列入 vetted registry 的包则不会跨重启对齐版本；另有官方 blocklist。
- **判据**：常见的安装审计只做**单向**——「有没有在清单里的都装上」；真正的声明式管理多一个**反向动作：不在清单里的被视为漂移并清除**。少了反向动作，手工装的东西会永久残留，声明清单与实际状态逐渐分叉而无人察觉。配套两点：① 设置页转只读，杜绝"UI 手工改一口"；② 校验值（checksum）必须绑定具体版本号，否则摘要没有锚点。
- **落地动作**：技能/依赖目录维护时，每季度做一次双向对账表（缺装 / 版本不符 / **未在册**），第三类的处置要显式决策（补进清单 or 卸载），不得默认放过。
- 提升层：工作流 / 可复用 Skill。触发词：声明式安装、reconcile、多余即卸、MANAGED_BY_ENV、漂移清除、设置页只读、sha512 绑定版本、blocklist。

## 发布是一次「可部分生效」的变更，不是一个布尔事件（来源：docs.n8n.io 发布态 machine 2026-09-28 r283-C 经 Qoder r317-Q-B 实拉取证 + WB 判重复核）
- **实证**：publish 按钮共有 8 态，其中 **`Published, partial`**（部分 trigger 激活失败 → **不回滚**，保留已激活的，可重新发布）与 `Failed to publish`（全失败但已发布版本仍然保留）；publish 是异步的，且只注册发生变化的 trigger。
- **判据**：**「没发布成功」不等于「什么都没变」**。部分成功且不回滚意味着此刻线上处于一个混合态：一部分单元已经按新逻辑跑，另一部分还是旧的。此时若简单地"重来一次"，就要保证它是幂等的；若简单地"回滚键址"（以为一切未变），就会漏掉已经生效的那部分。
- **落地动作**：发布动作必须产出三件事——① 哪些单元已生效的清单；② 哪些未生效及失败原因；③ 重发的入口只对未生效部分起作用。只返回一个成功/失败布尔位的发布接口，验收时判不合格。
- 提升层：工作流。触发词：Published, partial、部分成功不回滚、发布异步、只注册变化的 trigger、混合态、幂等重发。

## 版本不是说删就删：具名免回收、产生点要显式、 可用性按套餐分档（来源：docs.n8n.io 版本与源码管理章 2026-09-28 r283-C 经 Qoder r317-Q-B 实拉取证 + WB 判重复核）
- **实证**：**Named versions 永不被自动裁剪**；Draft 与 Latest 不可删；版本创建点＝保存 / Restore（恢复前会先存当前）/ **Git pull**（版本存在实例库、**不进 Git**），而**改 workflow settings 不产生版本**；可用性阶梯：全量 Enterprise / Cloud Pro 近 5 天 / 所有用户近 24 小时。
- **判据**：自动裁剪是常态时，**必须有"钉住"机制**让关键版本免于回收；同时要明确定义**哪些动作产生版本、哪些不产生**——"改了配置却不留版本"是典型的审计盲点（改了什么、什么时候改的，全部不可查）。
- **落地动作**：发布物做三件事：① 重要版本打具名标签，标记对自动回收免疫；② 列出"产生版本/不产生版本"的动作白名单，把配置类改动也纳入留痕；③ 声明历史版本的可用窗口，避免用户以为"旧版本永远能回滚"。
- 提升层：工作流。触发词：具名版本、不被裁剪、版本产生点、改设置不产生版本、恢复先存当前、可用性阶梯、钉住版本。

## 依赖写成区间，就必须同时定义「怎么解析」与「解不出来怎么报」（来源：code.claude.com/docs/en/plugins/dependencies.md 2026-09-28 r283-C 经 Qoder r317-Q-B 实拉取证 + WB 判重复核）
- **实证**：`plugin.json` 的 `dependencies` 数组支持 semver 区间 `^2.0` / `~2.1.0`；发版靠 git tag **`<plugin-name>--v<version>`** + `claude plugin tag --push`；**区间重叠时取最高**；解不出区间时报**具名错误** `has conflicting version requirements` / `Dependency … has no git tag satisfying`；跨市场依赖需显式开关 `allowCrossMarketplaceDependenciesOn`。
- **判据**：只说"我依赖 ^2.0"是不够的——**区间必须配解析规则**（区间重叠时怎么办）与**报错面**（解析失败时的具名错误）。只锁具名版本或只写区间都不完整：前者失去兼容弹性，后者失去确定性。报错必须具名，否则使用者只会看到安装失败而不知道是哪一条区间无法满足。
- **落地动作**：声明依赖时同时给出：区间写法 + 冲突解析策略 + 失败时的具名错误信息；跨来源依赖显式开白，不静默放行。
- 提升层：可复用 Skill。触发词：semver 区间、取最高、has no git tag satisfying、区间重叠、跨市场依赖、依赖解析规则、报错具名。

## 更新与运行态解耦：旧副本延迟回收，批量更新要抖动（来源：code.claude.com/docs/en/plugins/loading.md 2026-09-28 r283-C 经 Qoder r317-Q-B 实拉取证 + WB 判重复核）
- **实证**：**旧版本缓存目录后台清理要等 14 天后才删**（官方理由：保住已经在跑的会话）；交互会话在首条消息之后**随机延迟最长十分钟**再做后台自动更新；改盘后需 `/reload-plugins` 或新会话才生效；`--plugin-dir` 与某个 id 同名的副本**不加载**。
- **判据**：**替换一个正在被使用的东西，不能就地删除**。两条具体做法：① 旧版本保留到"确认没有会话在用它"再回收（这里用 14 天的粗粒度窗口）；② 批量更新加**随机抖动**，避免所有会话在同一时刻涌去拉更新（雷同群效应会造成自我造成的流量峰）。
- **落地动作**：热更新方案写明三个数——旧副本保留窗口、自动更新的抖动范围、变更何时对新会话生效；三者缺一，更新就是不可控的。
- 提升层：工作流。触发词：延迟回收、14 天、随机抖动、autoupdate 削峰、旧副本、reload 才生效、同名副本不加载。

## 更新通道数与回滚能力必须成对设计；一条外发通道不等于一个开关（来源：docs.openclaw.ai`/clawhub` 与 `/platforms` 2026-09-28 r283-C 经 Qoder r317-Q-B 实拉取证 + WB 判重复核）
- **实证**：① `openclaw update --channel` **只有 stable / dev 两档**，且**文档通篇没有回滚章节**——开启多通道却没有降级路径。② **遥测双开关**：产品分析受环境变量控制，而"部署快照"每日上报（副本数/CPU/内存/版本/DB-Redis RTT/execution mode/sandbox memory/concurrency）**不受环境变量控制、只能在 UI 关**。③ 相关：依赖动作锁 commit SHA 而非 tag；动作的"己读过状況"由 systemd plist 管理。
- **判据**：① **没有文档化的回滚路径，就不该开第二个更新通道**——通道越多、越需要有路返回。② **"我把开关都关了"这个结论需要逐个通道验证**：同一产品的不同外发分属不同控制面（环境变量 / UI），关掉**看得见的那个**不等于把两个都关了。审计外发面时，必须枚举控制面而不是枚举直觉里的开关。
- **落地动作**：给出回滚路径（具名版本→cd→如何装回）之后才允许发布第二个更新通道；清点遥测时按"控制面清单"（环境变量 / UI / 后台服务）逐项确认，并写下 UI 才能关的那几项。
- 提升层：工具 / 工作流。触发词：更新通道、没有回滚章节、stable/dev、遥测双开关、部署快照、UI 才能关、控制面清点。

## 限速的正确实现是「入队匀速」，不是丢弃也不是 sleep；漏跑要自动重处理（来源：Make Help Center `scenario-rate-limits-for-instant-triggers.md`（createdAt 2025-07-28）2026-09-29 r285-A 独立实拉 200 逐句核验）
- 原文："When a scenario reaches its configured scenario run limit, it queues and processes requests gradually as the limit allows" / "Sudden spikes get distributed evenly" / "**Missed executions get reprocessed automatically**"；节奏由系统处理，"no sleep modules needed"。
- 与已落 ponytail 1.74.0「入队不丢事件」互为官方佐证（那条是计费侧，本条是执行侧）。
- 同族附证：n8n `N8N_SCHEDULER_MISFIRE_GRACE=60` + `N8N_SCHEDULER_RETENTION=86400` 与 `…_FAILED_RETENTION=604800` —— **成功与失败账本分档定窗**，不要共用一个保留期。
- ⚠ 同一厂商同一问题的官方答复会随时段翻转（旧社区口径相反），判据以**带 createdAt 的文档页**为准。

## 移除公告必须自带迁移路径；升级期的告警只提示、不代劳、不阻断（来源：docs.openclaw.ai《BlueBubbles removal and the imsg iMessage path》与《Auth credential semantics》2026-09-29 r294-B 独立 curl 实拉 4,187B + 24,733B 核验）
- 原文（移除）："BlueBubbles support was **removed** from OpenClaw. Use the official iMessage plugin with **imsg** for new and **migrated** iMessage setups."——公告本体就给出替代件与"存量怎么迁"两个答案。
- 原文（升级告警）：自 2026.9.5 起原生 Codex 登录不再供给 runtime-only 的 `openai:default` profile；若该 OAuth profile 仍被声明但不在凭据库内，`openclaw doctor --fix`、Doctor lint、Gateway 启动**都会告警并给出导入命令**，但"**The warning does not copy credentials or block the update.**"；同类：`AUTH_PROFILE_MIGRATION_REQUIRED` "**blocks only those providers**, including their auth aliases; unrelated provider auth remains available."
- **落地动作**：① 写移除公告时同时写三件事——**移除什么 / 用什么替代 / 存量怎么迁**（"new and migrated setups"两个词一个都不能少）；只说"已移除"不给迁移路径的公告等于把成本转嫁给用户。② 升级期的兼容告警设计成**提示 + 给命令 + 不阻断**：不代为复制/迁移凭据（越权且不可逆），也不卡住更新；③ **迁移阻断要按 provider 收敛**——迁移中只冻结受影响的提供方及其别名，不要让一个 provider 的迁移态株连全部凭据。
- 提升层：工作流/工具。触发词：移除公告、迁移路径、imsg、升级告警不阻断、doctor --fix、AUTH_PROFILE_MIGRATION_REQUIRED、只阻断受影响提供方。

## 依赖升级有「阶梯硬上限」：bundled 依赖跨多个 minor 跃迁必须走声明的 staged 逐级路径，跳级不受支持（来源：Dify 1.17.1 GitHub release WARNING 2026-09-29 r336-Q-C gh api 实拉；与 §破坏面评估 互补——那条管"升不升"，本条管"跃迁跨度本身有硬上限"）
- 原文：自托管用 bundled Weaviate 者，升级到 1.17.1 前必须完成**手动分阶段（staged）升级**；Weaviate `1.27.0→1.39.2` **跨 12 个 minor，跳过 minors 不受支持**；「Pulling and restarting can **silently and permanently break** vector search」。
- 判据：① **跨多个 minor 的跃迁不是自由跳板**——很多 bundled 依赖只声明对相邻 minor 的兼容，跳级意味着中间每一级的 schema 迁移脚本都没跑，存量数据停在旧格式；② **朴素「拉新版 + 重启」是静默且永久损坏存量的路径**——它不报错，只是让某些功能（如向量检索）悄无声息地坏掉，且不可逆；③ 这类无声失败模式必须写成升级说明**顶部显式警告**，不能藏在 changelog 中段；④ 升级前先问"目标版本相对当前版本跨了几个 minor、中间每级有没有必须依次跑的迁移"——跨级多就走 staged 逐级，别押跳级成功。
- 提升层：工作流/工具。触发词：依赖升级阶梯、staged 逐级、跨 minor 跳级不受支持、静默永久损坏、朴素重启即损坏。

## 破坏面预检可以做成「产品内版本化规则集」：升级时对存量自动检测，检测器自身须容错（来源：n8n@2.40.0「v3 breaking change rule for the storage directory rename」#38423 + n8n@2.41.0「Keep breaking change detection running when a rule throws」#38738 2026-09-29 r336-Q-C gh api 实拉；与 §破坏面评估 互补——那条是人工查，本条是让检测自动化、版本化、可容错）
- 原文：n8n 把破坏性变更检测做成**版本化规则集**（v3 登记 storage 目录重命名这类破坏面），升级流程中对存量实例执行；且检测器要求**单条规则抛错不中断其余规则扫描**；弃用项就地警告（deprecated node / env var）而非等运行报错。
- 判据：① 破坏性变更检测**按版本登记**比"一个全局开关"更稳——每个大版本引入的破坏面写成对应版本的规则，升级到哪版就跑哪版的规则，不会漏也不会误伤旧实例；② **检测器必须容错**：一条规则因为边界数据抛错，不该拖垮整个扫描，否则一个坏规则就能让所有破坏面检查失效；③ 弃用要**就地警告**（在声明/加载处提示），而不是等运行时炸了才发现某人还在用被弃用的节点/环境变量；④ 对自研系统：升级脚本里把"破坏性变更"写成**带版本号的规则集 + 逐条独立 try**，比散落在代码里的 if 更可审计、可回退。
- 提升层：工作流/工具。触发词：破坏面预检、版本化规则集、单规则容错、弃用就地警告、breaking change detection。


## 供给面一致性要能机检：in-tree == lockfile == upstream 三方比对，发布即通知下游重钉（来源：github.com/full-stack-skills/skills-toolchain README 2026-09-29 r319B api.github.com 实拉 200）
- 原文：L0 vendor tooling 是 lockfile schema / lint gate / vendor 脚本的单一归属；`skill_vendor.py` 提供 `update`（取钉住源、整体替换、重算 digest）与 `check`（**in-tree == lockfile == upstream**）两个动作且 self-tested；`release-tag.yml` 在 push 到 main 后打不可变 tag + 发 Release，并 **dispatch `toolchain-updated` 事件通知下游**；`lint_skills.py` 与 `skill_vendor.py` 自身**经变异测试**（`tests/test_lint_skills.py` / `test_skill_vendor.py`）。
- 判据：① 三方比对缺任一环都不成立——只比 in-tree 与 lockfile 会漏掉"上游被改而两边都没动"，只比 lockfile 与 upstream 会漏掉"本地被人手改过"；② 版本钉住不能只写锁文件，**发布侧要主动广播**（dispatch 事件）让下游重钉 SHA，否则下游永远停在旧钉；③ 治理脚本本身要有测试，且用**变异测试**验证（故意改坏一处，看测试是否失败），否则 lint 形同虚设；④ 自研：把"校验本地副本 + 锁 + 上游三方一致"做成一条可在 CI 跑的命令，任何一环不等即失败退出，不让"看起来装上了"通过。
- 提升层：工具/工作流。触发词：lockfile、三方一致、digest、重钉 SHA、dispatch、变异测试、vendor 校验。

## 信任表达两条相反路线：trust tier 分级 gate vs 机器可读 trust record 清单（来源：developer.nvidia.com skill evaluator / verified skills 两文 2026-09-29 r340-Q-A 实拉；对照 arXiv 2602.12430 v4 四级 gate 权限模型）
- 原文：NVIDIA 明确**不设 trust tier**，改用 **machine-readable trust record 元数据文件**承载 authorship / license / 依赖链 / 已知限制；与"按信任等级分档授予权限（四级 gate）"构成路线对立。配套：manifest = 主 SKILL.md + counterexample 评测文件 + registry JSON，**negative case 默认不自动生成、须人显式写入**。
- 判据：① 分级 gate 的问题是"等级由谁定、降级怎么通知"；清单式 record 的问题是"消费者得自己读"——选型时先问"我的消费方能读懂清单吗"，能读就用 record（更抗单点裁定），不能读才用 tier；② 无论哪条路线，**已知限制必须随包携带**（tier 写进等级描述、record 写进字段），不写限制的信任表达等于背书；③ 负例必须人工写：自动生成负例会退化成"模型已经会做的事"，测不出真失败。
- 提升层：工具/可复用 Skill。触发词：trust tier、trust record、信任清单、负例人工写、已知限制随包。

## 本地来源（file:// 与本地路径安装）必须同权入锁并算目录内容哈希，遥测把绝对路径脱敏为 generic 标记，否则本地安装就是审计盲区（来源：vercel-labs/skills bcdcee67，2026-09-30 r320B 实拉）

## 自助撤回的资格由注册表机检（依赖反查/下载窗口/维护者数）+ 整包撤回后同名 24h 禁发冷却窗 + 显式不可逆 + 不合格走 deprecate 降级档（来源：docs.npmjs.com/policies/unpublish，2026-09-30 r321C 独立实拉 508,379B；细则见 references/knowledge-base.md §r321C）

## 发布与撤销生命周期 2026：撤回四模式/可恢复性/弃用通知/sunset 时间表/供应链信任面（来源：docs.npmjs.com policies/unpublish+unpublishing+deprecating+trusted-publishers/doc.rust-lang.org publishing+cargo-yank/golang retract/learn.microsoft.com Azure Artifacts×6/docs.github.com packages/npmjs.com policies/privacy/pm-claude-skills api-versioning-strategy/apiscout/semver.org/docsie/releasepad/theneo/alicinaroglu/beefed/talkthinkdo/dev trknhr/Z-M-Huang vcp/vulert/kfchou/bastion/lidge-jun/infoq npm staged×2/pypi blog 14-days/colony-sdk RELEASING/toughcrowdhq RELEASING，r322A，与 §版本级状态机/§撤回资格机检互补——那些条管"撤回的资格与状态"，本条管"四生态语义对照+可恢复性+告知义务+供应链信任面"）
- **撤回四模式对照**：npm=真删（registry 删条目+tarball；72h 内新包无依赖可任意撤；>72h 需无依赖+周下载<300+单一 maintainer 三资格机检）；PyPI=不支持真 unpublish（yank 禁新装+publish fixed version）；crates.io=permanent archive（永不删版本，yank 只移出 index 不删数据——"no new dependencies, but all existing dependencies continue to work"）；Go retract=软撤回（@latest 跳过但显式请求仍可得）。**判据：引用生态撤回语义前先查"真删/禁新装/禁新依赖/软撤回"哪种模式**。
- **撤销≠销毁：可恢复性**：Azure Artifacts 删包进 Recycle Bin 30 天（仅 feed owner 可恢复，误删/仍有依赖可救）；retention policies=max versions+未下载 N 天自动删；GitHub Packages 门槛=public 包或版本 >5000 下载不可删（下载量=保护伞）。**判据：删包先进回收站设恢复期；高下载量禁删**。
- **撤回信息传播不可逆：告知是强制组成**：npm "can't make everyone who has downloaded published data erase it"——撤回无法撤销已传播数据；API 弃用 T-0=决策日批准+sunset date→docs deprecation banner→所有响应加 Deprecation+Sunset headers（`Deprecation: Sat, 01 Nov 2026...`）；通知四件套=what/why/迁移路径/sunset date。**判据：撤回必须配 push 告知；API 弃用响应头带 Deprecation+Sunset**。
- **弃用通知三通道与目标化**：通道=docs banner/changelog+sunset date/email 直接通知/portal 弃用状态；**telemetry 识别活跃调用者定向通知>广播**；semver 弃用=①更新文档 ②新次版本发布弃用信息，主版本移除前至少一个次版本含弃用信息；消费者 tiered policy=auto patches/test minors/plan majors。
- **Sunset 时间表**：6 月 playbook=T-180 announcement（v2+迁移指南）→T-120 headers+usage dashboard→T-90 主动联系大消费者→T-60 日限流递减；EOL 三阶段=90-180d 公告/60d 提醒/30d escalation（phone/CSM）；窗口对照=Twilio 24mo/Shopify ≥12mo/Stripe 不强制 sunset（pin 到升级）/GitHub CLI=current 全修复+前 major critical 90 天+更旧 unsupported（exceptional 才扩）。
- **锁文件供应链基线**：lockfile 必须提交（记录实际解析树）；CI 用 npm ci（package.json 与 lockfile 不同步即失败）→bun --frozen-lockfile/poetry --no-update；每 PR 审 lockfile diff；.npmrc min-release-age=7/ignore-scripts/save-exact；CI 跑 audit+SBOM；Renovate（preferred）/Dependabot auto-merge 限 patch/minor。
- **零日窗口排除**：exclude-newer 滚动缓冲排除"刚发布未审查"包（XZ backdoor 活跃数月才被发现）；Axios caret range 自动拉入恶意 1.14.1——生产依赖 pin 精确版本+hash。
- **发布侧信任面**：npm staged publishing=预构建 tarball 上暂存队列→维护者 2FA 放行（发布前人工审核）；trusted publishing 自动 provenance attestations（tarball↔git commit↔workflow 加密链接，npm audit signatures 可验；CircleCI 不支持）；**OIDC 短时凭证替代长期 NPM_TOKEN（泄露=无限发布任意版本；OIDC 分钟级+scoped 单 run）**；PyPI 拒绝对 >14 天旧 release 上传新文件（防旧稳定版投毒）。
## 日落必须是一条有资格的登记项（无 removeAfter/removalGate 即无删除资格、续期留痕且≤3 个月、过期 CI 判 fail），且时点要落在可枚举的结构化载体上；引用/命名类破坏在存量侧永不自愈——升级与重装都不修（来源：docs.openclaw.ai/plugins/compatibility.md 14,100B + nodejs/Release schedule.json 5,325B + code.visualstudio.com/updates/v1_139 52,978B，2026-09-30 r322B 独立实拉；细则见 references/knowledge-base.md §r322B）

## 支持窗要按「活跃支持 vs 维护期」双轨计量，并显式声明跳级升级是否被支持——「还在支持期内」不等于「还会给你修想要的东西」（来源：ee.dify.ai/lts-policy/，2026-09-30 r323A 独立实拉 27,147B）
- 原文：「Each LTS has an **18-month lifecycle (12 months active support + 6 months maintenance)**, and three versions [are supported simultaneously]」；「**Skipping major LTS versions is not supported** —you must upgrade sequentially」；维护期只承诺 security/stability/compliance、**no new features**；补丁承诺「≤ 2 weeks」。
- 判据：① **把支持窗写成"发布后 N 个月"与"最近 N 个版本"是两种义务载体**——月数制对消费者可预期，相对计数随发布节奏漂移；两者都登记时才回答得了"我这个版本还剩多久"，只写一种会在节奏突变时失真；② **active 与 maintenance 不是同一个"支持"**：维护期只做安全/稳定/合规、明确不发新功能，把维护期当活跃期用等于等一个永不来的功能；写支持状态必须分栏，不能一个布尔了事；③ **跳级是否被支持是支持窗的隐含前提**：不支持跳级（必须逐级升级）时，落后多个 minor 的用户迁移成本不是一次升级而是 N 次，且"数据卷不能跨 12 个 minor 一步到位"这类硬约束要随窗一起声明；④ **同时支持版本数是容量参数**（此处 3），决定消费者升级压力与厂商补丁面，不是宣传数字。
- 提升层：工作流。触发词：LTS 双轨、active support、maintenance 期、跳级不支持、支持窗计量、同时支持版本数。
- 待补登记：Weaviate「supports the three most recent minor versions」原文本轮未独立取到（`docs.weaviate.io/weaviate/release-management` 404），仅登记不落地。


## 版本号可以承载时间序（0.0.<unix-timestamp>），发布通道也可以与生产面分离——两者都改变“怎么比较新旧”（来源：www.pipedream.com/docs/cli/reference 750,789B + developers.make.com versioning-and-maintenance 5,707B / manage-testing-and-production-app-versions 4,232B，2026-09-30 r323C 独立实拉）
- 原文：Pipedream「replace the version in the published component with `0.0.<unix-timestamp>`. This lets you iter[ate freely]…」；Make 双通道「the development does not influence the production version of the application」+「pushes the changes to the production application from the local testing app」，而公共面「Any changes to a private or public app **apply immediately**」；存量迁移「users need to upgrade the modules in their scenarios using our **upgrade module tool**」「Updating tens or hundreds of scenarios might be complicated and a time-consuming process」。
- 判据：① **把时间戳写进版本号 = 用发布时间换掉一整套比较规则**：天然单调、不必解析 semver 就能排序，代价是版本号不再表达“改了多少”，往语义化版本迁移时要另设映射；② **测试与生产通道分离时，必须声明“改动何时到达生产”**：此处自定义 app 走显式 push，公共 app 却即时生效（零 staging）——同一产品内两种发布语义并存，写发布流程时不能假设“有测试版就有缓冲”；③ **弃用/破坏性变更必须配存量迁移工具**：版本弃了存量不会自己升级，官方口径直说“更新几十上百个场景可能复杂且耗时”，因此“发一份迁移指南”不算完成，要给出可执行工具并把它列为弃用前置条件。
- 提升层：工作流/工具。触发词：时间戳版本号、0.0.unix-timestamp、测试生产双通道、apply immediately、upgrade module tool、存量迁移前置。

## 跨宿主安装契约三件套：声明清单 → 差分预览 → 带来源的锁（可更新亦可移除）；以及「无制品面=以 commit 为唯一时间轴」（来源：raw.githubusercontent.com/vanillagreencom/kendex/main/README.md 5,707B + gh api repos/anthropics/skills/releases → `[]` + github.com/anthropics/skills/releases HTML 186,636B「There aren’t any releases here」，2026-09-30 r324A 独立实拉；细则见 references/knowledge-base.md §r324A）


## 挂载必须锁到具体版本号，`latest` 不被支持；删除的爆炸半径只到「未来挂载」，已挂载者不受影响；拒绝要给文件级可修细节（来源：help.aliyun.com/en/model-studio/skills-api/ 46,102B，last-modified 2026-09-28，2026-09-30 r325C 独立 curl 实拉逐串命中；经 Qoder r357-Q-A 提名）
- 原文：「Attachment **locks to a specific version number**.」「The attachment **must specify a concrete `version` (`latest` is not supported)**; uploading new versions later **does not affect already-attached** agents.」「Delete the skill…**Delete the skill and all its versions; agents that already attached an older version are unaffected.**」「`rejected` — Hit a security risk and cannot be attached; the version detail provides **per-file issues** under `additional_properties.error_info`.」「Returns an OSS **pre-signed URL (valid for 2 hours)** for downloading the zip package.」
- 判据：① **绑定端必须写死版本号，禁止 `latest`**——"最新版"是一个移动靶，它把每一次上游发布都变成一次隐式升级；消灭 remote-latest 这一类引用形态，等于一次性关掉最大的非预期变更入口（不同于 naar lockfile：这里是**运行时绑定面**，锁的是"我记得住的版本号"而不是依赖图）；② **升级不追溯、删除不追溯**：已挂载的 agent 继续用旧版本，删除也只切断将来 ⇒ 版本上的破坏性变更可以放心发布，但代价是**旧版本必须继续可用**，因此"要不要删旧版本"是一个单独决策，不能随发布自动发生；③ **拒绝要给到可修粒度**：扫描/准入拒绝时不能只给一个状态码，要给**文件级**问题清单并在结构化字段（而非人类可读文案）里输出，让提交方能自动定位；④ **分发走短时效签名 URL**：包下载用 2 小时有效的预签名地址，把"能下载"变成一个**有时限的授权**而不是永久链接。
- 提升层：工作流/安全边界。触发词：绑定禁止 latest、版本锁、删除不追溯、已挂载不受影响、per-file issues、error_info、pre-signed URL 2 小时。

## 清理器只作用于「当前配置指向的那一个后端」：切换后端即在旧后端留下永不自清的孤儿（来源：n8n handle-binary-data 本机实拉，r326A）
- **原文**：「n8n executes binary data pruning as part of execution data pruning」；「If you configure multiple binary data modes, binary data pruning operates on **the active binary data mode**. For example, if your instance stored data in S3, and you later switched to filesystem mode, n8n **only prunes binary data in the filesystem**.」
- **判据**：① **迁移 / 换存储的验收必须含「旧位置残留清点」**——清理器跟随现役配置，旧后端的数据从此无人管；只看新位置健康 = 漏一半。② 清理责任与配置绑定 ⇒ 「存储后端」变更必须触发一次孤儿盘点，写进迁移 runbook，不靠人记得。
- **提升层**：工作流/工具。触发词：清理器只认活动后端、切换后端留孤儿、旧位置残留清点、迁移验收两看。

## 学习轮沉淀 r347A（来源 Qoder r360-Q-A · 2026-10-01 · Registry latest 裁决）
- **MCP Registry 同 name 多版本恰一版 isLatest=true，客户端不得自推 latest**：生命周期字段统一挂带前缀 `_meta["io.modelcontextprotocol.registry/official"]`（status/statusChangedAt/publishedAt/updatedAt/isLatest）；分页 cursor=`name:version`。判据：latest 是服务端裁决非客户端推导。来源：registry.modelcontextprotocol.io 活 API。

## 学习轮沉淀 r347B（来源 Qoder r361-Q-B · 2026-10-01 · 评测 executor/自动删除豁免/备份排除）
- **评测须标注 executor（与 av 同轮同点）**：跨 executor 结论失效，发布评测报告须锁 executor 基线与版本。判据：结论不跨 executor 移植。来源：arXiv 2609.36746。
- **自动删除须显式豁免集+两阶段缓冲窗**：n8n `EXECUTIONS_DATA_PRUNE`+`EXECUTIONS_DATA_MAX_AGE`（默认 336h），删除前 grace 窗。判据：清理须有豁免集+缓冲，禁即时硬删。来源：n8n scaling/manage-execution-data。
- **备份清单逐条排除原因（与 av 同轮同点）**：导出 manifest 须标 skipped/error+原因。判据：备份完整性=逐条可解释排除。来源：Pipedream export-workflows。

## r436B · 破坏性变更的"白名单豁免形状"与"同名冲突申报"（2026-10-07 独立 curl 实拉，经 Qoder r436-Q-A / r439-Q-B 提名）

### 一、Flowise v2.1.4 迁移指南（1,784B）
- 逐串命中：`Due to security concerns, it is now disabled by default.`、`Users must explicitly specify which config can be overriden from the UI.`
- 迁移四步（原页 step 结构）：Configuration → Enable Override Configuration → 逐字段打开开关并保存 → 之后才能被覆盖。
- 可复用结论：安全型收紧 = 「翻转默认值」+「逐字段豁免白名单」+「可执行迁移脚本」三件套，缺第三件即"功能性回退"。

### 二、LangFlow v1.12.5 同名工具消歧（release notes 8,093B）
- 逐串命中：`fix(tools): disambiguate duplicate tool names by @Cristhianzl in .../pull/15556`
- 可复用结论：命名主键冲突在实现侧被视为缺陷并单独发版修复 ⇒ 发布说明侧应同步按破坏性变更申报。
- 未达证据（诚实标注）：Qoder r439-Q-B 提到的"同名安装会静默覆盖 / 批量更新会一次刷新全部"来自 orca.security 博客，本轮对该 URL 实拉返回 000（未达），故那一半不落地；该站计入探活计数 1 次。

## r479B · 注册表默认是「剪除」而非「不收录」，例外须带责任四字段（2026-10-09 独立 curl 实拉，经 Qoder r473-Q-C 提名）
- 来源：NVIDIA/skills 仓库 `catalog-exceptions.yml` + `components.d/` + `versions.json`（api.github.com 一手逐串命中，三文件实测存在）。
- 实证（`catalog-exceptions.yml` 逐串命中）："Everything else in skills/ must be declared by a components.d/<slug>.yml entry, listed in .github/scripts/manual-components.yml, or listed here — otherwise the hourly sync prunes it (see .github/scripts/prune-orphans.sh)." ⇒ 默认动作是 **prune（剪除）**，不是 skip（不收录）。
- 例外四字段（责任三元组 + 目录）：每个 exceptions 条目必须含 `dir` / `reason`（documented reason）/ `owner` / `component`，文件头注释明确 "Add an entry only with a documented reason and an owner"。
- 可复用落点：wb-release-maintain 的「退役 / 批量淘汰」——默认剪除 + 例外带责任字段（谁 / 为何 / 归属组件）+ 速率上界三件套；与 r441B 批量退役三闸（PRUNE_CAP / 解析失败停删 / 期望集 + 豁免清单）同族，但本点更强调「默认即删」的取向，合并时取交集。


## r515A · 新增安全/隔离态具有「运行时版本边界」：旧运行时不强制执行新态，降级前必须显式处置新态对象（来源：docs.openclaw.ai `auth-credential-semantics.md` 27,952B，2026-10-11 独立 curl `.md` 原文实拉、逐串命中）
- **实证（逐串）**：setup 替换凭据「存独立 profile ID + 内部 `setup` descriptor，**不能**进入正常轮换、不能被显式 pin 解析、不能被复制到另一个 agent；测试失败或拒绝 → 保持 inactive 并保留当前连接」；关键句 `older runtimes do not enforce the inactive state` + `Before downgrading, remove saved inactive replacements or restore the state from before setup` + `This adds no database schema or migration`。
- **判据**：① **新引入的约束态不是"写进配置就全局生效"，它只在认得它的运行时上被强制执行**——旧版看不见该状态，于是同一份配置在新旧版本上语义不同；② 因此**降级是破坏性操作**：降级前必须显式处置只被新版认识的对象（移除，或把状态恢复到引入前），否则降级后旧版会以"没有这个约束"的方式去用它们；③ **加状态不等于加 schema**：本例明确不改数据库 schema、不做迁移，代价是"旧运行时不强制"——这是有意选择的取舍，写发布说明时必须把它当破坏面写出来，而不是当作无变更；④ 与 r511B「换默认不回填存量引用」互补：那条管**默认值变更对存量引用的影响**，本条管**约束态在不同运行时版本上的强制力差异**。
- 提升层：工作流（发布/降级破坏面评估）。触发词：新态旧版不强制、降级前处置、约束的版本边界、不加 schema 的取舍、inactive 状态、替换凭据隔离。


## r515B · 配置生效范围是三个独立开关：进程内内存 / 跨重启持久 / 跨 worker 广播，且默认是**最弱档**（来源：docs.n8n.io `administer/manage-credentials/credential-overwrites.md` 5,099B，2026-10-11 独立 curl `.md` 原文实拉、逐串命中）
- **实证（逐串）**：`CREDENTIALS_OVERWRITE_PERSISTENCE=true` 时 n8n 把加密后的覆盖值存进 `settings` 表并广播 `reload-overwrite-credentials` 事件让 worker 重载；关闭时「overwrites remain in memory on the process that loaded them and n8n doesn't propagate them to workers or preserve them across restarts」。
- **判据**：① **"配置已生效"要拆成三个可独立为假的命题**：当前进程认得它 / 重启后还在 / 其他 worker 也认得它——三件事由不同开关控制，默认档只满足第一个；② 发布说明里新增"全局覆盖/默认值注入"类能力时，**必须写明默认档是哪一档**，因为默认最弱档的表现是"在单点上看起来完全正常、在集群里一半节点没生效"，这类故障不会报错；③ 与 av 2.179.0「计数域是全局还是 per-process」分工：那条管**上限数值的计数域**，本条管**配置值的持久性与传播域**，对象不同、不可互相替代。
- 提升层：工作流（配置/发布变更的生效面评估）。触发词：生效范围三开关、默认最弱档、跨 worker 广播、重启后是否还在、覆盖值持久化。
