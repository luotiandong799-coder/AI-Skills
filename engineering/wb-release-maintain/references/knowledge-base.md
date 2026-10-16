

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


## r516A · 两把 hash 锁锁的是两样东西：`expectedHash` 锁策略制品，`expectedAttestationHash` 锁「上一次通过的检查结果」；修复权另由 `workspaceRepairs` 单独开关（来源：docs.openclaw.ai `cli/policy/running-checks.md` 4,521B，2026-10-11 独立 curl 取 `.md` 原文通道实拉、逐串命中）
- **实证（逐串）**：`Optional hash-lock for the approved policy artifact.`（锁**已批准的策略制品**）；`Optional hash-lock for the last accepted clean policy check.`（锁**上一次通过的检查结果**）；`Allow doctor --fix to edit policy-managed workspace settings.`（是否允许自动修复改策略托管配置，**默认关闭**）；`In a multi-agent fleet with explicit ownership, pass --agent <id> ... OpenClaw never selects an arbitrary first agent`；`checksRun` / `checksSkipped` 与 `findingsHash` 一并进 attestation。
- **判据**：① **"锁配置"与"锁检查结果"是两种保鲜期完全不同的约束**：制品 hash 只在文件被改时失效，而 attestation hash 会因**环境/后端/检查集**变化而失效——混用会让一次无害的环境变更表现为"基线被篡改"，或反过来让真正的改写在"上次通过"的掩护下溜过去。② **自动修复权要单独成开关且与检查权分离**：`workspaceRepairs=false` 意味着"能检查出问题"不等于"允许机器改它"，把两者绑在一个开关上会让 `--fix` 顺手改掉策略托管面。③ **attestation 要带 `checksSkipped`**：只报 `checksRun` 的话，"跑了 5 条全绿"与"该跑 50 条只跑了 5 条"长得一样——跳过数必须和通过数同栏出具。④ 发布/合规制品的最小可信集：**制品 hash + 检查集指纹 + 跳过数 + 结论 hash**，缺一项则该证明可被合法绕过。
- 提升层：工作流（发布与合规制品的锁定面）。触发词：expectedHash 与 attestation hash 分工、锁制品不锁结论、workspaceRepairs 默认关闭、checksSkipped 必须同栏。

## r516B · 弃用入口在迁移期仍是所有权根：升级到新认证前**必须先用旧凭据认证一次**，旧入口不能先关（来源：docs.flowiseai.com `configuration/authorization/app-level.md` 7,734B，2026-10-11 独立 curl 取 `.md` 原文通道实拉、逐串命中）
- **实证（逐串）**：`To prevent unauthorized ownership claims, you must first authenticate using the existing username and password configured as FLOWISE_USERNAME and FLOWISE_PASSWORD`（建新 admin 前**必须**用旧凭据认证，官方理由是防未授权的所有权主张）；`a short-lived access token (default 60 minutes) and a long-lived refresh token (default 90 days)`；`Set to 'true' to invalidate all tokens on server restart`（`EXPIRE_AUTH_TOKENS_ON_RESTART`，把"重启"做成显式失效触发器）。
- **判据**：① **标记为 deprecated 的入口在迁移完成前是权限根，不是可先关的垃圾路径**——关掉它等于同时关掉"证明我是原主"的唯一通道；迁移计划里旧的入口必须保留到新所有权建立之后。② **所有权转移要有"先证明旧所有权"这一步**，只靠"新账号第一个注册"会把抢注变成合法流程。③ **长短令牌是两套失效时钟**（60 分钟 / 90 天），轮换策略必须分别给：访问令牌泄露的窗口是分钟级，刷新令牌泄露的窗口是季度级，按同一个周期处理必然有一边过度或不足。④ **把"重启"做成失效触发器时，要同时声明它对在场会话的影响**——这是"以可用性换安全"的开关，不是无副作用的配置项。
- 提升层：工作流（认证迁移与发布变更）。触发词：弃用入口是所有权根、先证明旧所有权、长短令牌双时钟、重启即失效。

## r516C · 准入面被刻意排除在 API 授权面之外：没有任何 API-client scope 能改身份提供者 / SCIM / provisioning；机器令牌绑定 audience，在 `/mcp` 被拒（来源：pipedream.com/docs/conduit/use/api/scopes.md 3,110B，2026-10-11 独立 curl 取 `.md` 原文通道实拉、逐串命中）
- **实证（逐串）**：`Identity inventory is read-only: sso:read and provisioning:read can inspect sanitized settings and mappings, but no API-client scope can create or modify identity providers, SCIM tokens, or provisioning rules`；`Those writes govern who can sign in or be provisioned as a human`（官方给的理由：这些写操作决定**谁能作为人登录或被供给**）；`Invites, API-client management itself, changing member roles, and workspace telemetry configuration are likewise not on the API-client surface in this release`；`a machine token is bound to the API audience and is rejected at /mcp`。
- **判据**：① **能列举的授权清单必须同时声明它的排除面**：本例明确"邀请 / API 客户端自身管理 / 改成员角色 / 遥测配置"不在本版 API 面内 ⇒ "清单里找不到"要能被读成"这一版刻意不提供"，而不是"以后会加"。② **"谁能进来"这一类写操作被排除在机器面之外，是边界设计而非功能缺口**：决定人类准入的写操作不应由机器凭据完成，评审"为什么 API 不能做这件事"时先按边界判定，不按排期判定。③ **同一身份跨入口不是同一个身份**：机器令牌绑定 audience，在 `/mcp` 端点被拒 ⇒ 拿到令牌不等于拿到全部入口，"已授权"必须带上"对哪个入口授权"。④ 发布说明里新增 API 面时，**排除清单与能力清单同等重要**，只写能力会让集成方按"迟早会有"做设计。
- 提升层：工作流（授权面与发布说明的覆盖面）。触发词：准入面排除在 API 外、排除清单与能力清单同重、令牌绑定 audience、跨入口不是同一身份。

## r517A · 可移植制品只搬逻辑不搬连接；保留期是三套独立时钟（来源：help.make.com `blueprints.md` 5,849B + `delete-a-scenario.md` 1,942B + `scenario-version-control.md` 7,836B，2026-10-11 r517A 一手 curl 取 `.md` 原文实拉、逐串命中）
- **实证（逐串）**：`While blueprints include scenario modules, settings, and mapped values, users still need to create connections for their accounts after importing the blueprint. `；`Before running the scenario, you may need to choose where to start and reconnect any webhooks. `；`Make stores each saved version for 60 days, except the latest version, which it keeps until you save a newer one. `；`When you move a scenario to **Trash**, Make stores it for 30 days before permanently deleting it.`
- **判据**：① **导出 / 导入的可移植边界要显式声明**：蓝图包含模块、设置与映射值，**不含连接** ⇒ 拿到制品不等于拿到可运行系统；同理从回收站恢复后 webhook 需要重连 ⇒ **恢复的是「定义」，不是「连接状态」**。② **保留期不是一个数，而是按对象分的三套时钟**：历史版本 60 天、最新版无期限（直到出现更新的版本）、回收站 30 天 ⇒ 用「平台保留多久」这种单值提问得不到答案。③ **制品的备份价值与可运行价值要分开评估**：官方把蓝图第一用途列为「以防失去访问权限或换账号」⇒ 备份保住逻辑、保不住凭据与连接，恢复演练必须把连接重建算进工时。
- **与既有能力分工**：§「治理名单自身是可回滚制品」管**名单的版本与回滚**；本条管**制品的可移植边界**与**保留期多时钟**。
- 提升层：工作流 / 发布治理。触发词：blueprint 不含连接、导入后重建连接、reconnect any webhooks、三套保留时钟、60 天版本 / 30 天回收站 / 最新版无期限。

## r517B · 密钥体积上限随后端变化且单位不统一；备份密钥库必须与主用不同位置（来源：docs.zenml.io/deploying-zenml/deploying-zenml/secret-management.md 12,931B，2026-10-11 r517B 一手 curl 取 `.md` 原文实拉、逐串命中）
- **实证（逐串）**：`you can reason about its size as the sum of the UTF-8 size of every key name and every value in the map, not a per-key limit. Non-Latin text usually needs more bytes per character than English in that total. `；官方上限表：Default(server database) / AWS / GCP **64 KiB**、Azure Key Vault **25 KB**、HashiCorp Vault(KV v2) **~512 KiB to ~1 MiB**（depends on storage back-end）、Custom **Varies**；`register another ZenML secret (a new name), split keys across secrets, or keep the file in an artifact or object store and only put a reference in a value. `；`Using the same location for both the primary and backup Secrets Store will not provide any additional benefits and may even result in unexpected behavior.`
- **判据**：① **上限是后端属性不是平台属性**：同一 secret 在默认 SQL / AWS / GCP 是 64 KiB，Azure 只有 25 KB ⇒ 迁移密钥后端会静默改变可用体积，超限时报的是写入失败而不是「你超限了」，易误判成权限 / 网络问题。② **单位差异本身就是坑**：64 **KiB** 与 25 **KB** 混排在同一张表（相差约 2.4%），照抄数字不算换算会算错边界；非拉丁文本每字符占更多字节 ⇒ 中文密钥值会比同字符数英文更早撞线。③ **超限正解是拆分或只放引用**，不要把大块内容塞进 secret 再指望后端放宽。④ **备份的判据是「位置不同」而非「配了两份」**：主备指向同一位置时官方明写无额外收益且可能异常 ⇒ 验证备份有效性要问「是否落在不同后端 / 账户 / 区域 / 项目」，只核对配置项数量不算验证。
- **与既有能力分工**：§「SecretRef 三字段固定 + 换默认不回填存量引用」管**引用语法**；本条管**后端决定的体积上限**与**备份位置独立性**。
- 提升层：工具 / 发布治理。触发词：64 KiB vs 25 KB、密钥上限随后端、UTF-8 总和口径、非拉丁占字节更多、备份密钥库须不同位置、same location no additional benefits。

## r517C · 归档不等于下线：版本非增量保存、线性无分支，旧 HEAD 归档后仍永久可调用（来源：www.windmill.dev/docs/core_concepts/versioning.md 2,089B，2026-10-11 r517C 一手 curl 取 `.md` 原文实拉、逐串命中）
- **实证（逐串）**：`**Not diff-based**: every version of a Script contains its entire content and not just the diff between it and its direct parent. `；`**Linearity**: the lineage ... there is no branching and there is no merging. `；`scripts are never overwritten, they are instead subsumed by a child script which corresponds to the new version of the parent. `；`The previous "HEAD" is archived but still deployed forever.`
- **判据**：① **「归档」是版本链上的位置变化，不是下线**：旧 HEAD 被归档但仍永久处于部署状态 ⇒ 把归档当「已停用」会留下一条仍在被调度 / 被调用的路径；下线必须是独立动作。② **版本链线性无分支无合并** ⇒ 没有「从历史点开并行线」的能力，「回退」只能是重新部署某个历史版本成为新 HEAD，链上会多出一个新的子版本，而不是切回分支。③ **全量保存而非增量** ⇒ 体积随版本数线性增长，且「两版内容几乎一样」推不出二者可互相替代（每版都是自包含实体）；容量与清理规划按「版本数 × 单份体积」算，不要按 diff 算。
- **与既有能力分工**：§「评测集用语义化版本、发布后不可修改」管**版本号语义**；本条管**归档与下线的区别**及**版本存储形态**。
- 提升层：发布治理 / 工作流。触发词：archived but still deployed forever、归档不等于下线、Not diff-based、线性无分支、子版本替代父版本。

## r519B · 升级只换服务端不换制品：不可变快照内嵌旧运行时须全部重建，调度须删旧建新；演练环境镜像漂移则绿灯无效，且「升级成功」判据须双方预先约定（来源：docs.zenml.io/deploying-zenml/upgrade-zenml-server/best-practices-upgrading-zenml.md 8,955B，2026-10-11 r519B 一手 curl 取 `.md` 原文实拉、逐串命中）
- **实证（逐串）**：`Pipeline snapshots may now break as they have the older version of the ZenML client installed. Therefore, you would need to rebuild the snapshot and associated images.`；`Rebuild **all snapshots** in prod`；`**Reschedule** recurring pipelines (delete old schedules, create new ones).`；`When you change a stack in production, immediately update the twin in staging.`；`the platform and data science / ML engineering teams should have mutually: Agree on a smoke test suite of pipelines or steps / Maintain shared expectations on what counts as "upgrade success"`；`Always have **two environments**: *production* and *staging*.`
- **判据**：1. **不可变快照同时冻结了它所依赖的运行时**：快照里装的是旧版 client，服务端升级后旧快照不是"仍然可用"，而是"不可变且已过期" ⇒ 升级动作必须含**重建全部制品**这一项；只升服务端等于升了一半，且失败会表现为"升级完了老流水线反而坏了"。 2. **调度不随升级迁移，必须删旧建新**：`delete old schedules, create new ones` ⇒ 升级后"调度还在跑"不代表跑的是新版本，也不代表绑定的是新制品；升级验收要逐个确认调度被重建（本条为 §「调度是运行期状态、不随代码回滚」原登记待复核点取到原文，方向确证）。 3. **演练环境的价值由镜像漂移度决定**：prod 变更 stack 必须**立即**同步 staging twin ⇒ 漂移的 staging 出的绿灯无意义，等同于没测；把 staging 结果当验收证据前先对一次镜像 / 配置时间戳。 4. **"升级成功"是双方约定，不是升级方自定**：平台方与使用方需**事先共同**约定 smoke 套件与成功判据 ⇒ 没有预先约定的验收，升级后只能靠"暂时没人报错"，而沉默不等于通过；升级说明里要写清"本次升级成功的判据是什么、由谁确认"。 5. **回滚位要提前留实体**：`Keep the old Docker image tag handy for rollbacks` + 升级前数据库备份 + 保留 migration job 日志 ⇒ 回滚位不是声明出来的，是**具体留存的旧实体**；没有旧 tag 与备份，"可回滚"只是口头属性。
- **与既有能力分工**：与 §备份必须显式列举「不含什么」互补——那条管**备份覆盖面**；本条管**升级这一动作的完整组成**（制品重建 + 调度重排 + 演练镜像同步 + 判据约定 + 回滚实体）。
- 提升层：工作流 / 可复用 Skill。触发词：rebuild the snapshot、Rebuild all snapshots、Reschedule delete old schedules、update the twin in staging、what counts as upgrade success。

## r524A · 组件降级的故障信号是 revision 名对不上，官方正解是「清理重建」而不是「回滚迁移」：`Revision not found` 意味着 schema 迁移不可逆，须 drop 库 + 同名 create 重建，升级前必须另有库快照（来源：docs.zenml.io/deploying-zenml/upgrade-zenml-server/troubleshoot-your-deployed-server.md 5,796B，2026-10-11 r524A 一手 curl 200 实拉、逐串命中 `Revision not found` in your `zenml-db-init` logs, one way out is to drop the database and create a new one with the same name`；来源 Qoder r521-Q-A）
- **判据**：① **降级失败的信号不是"报错"，而是一个名字对不上**：`Revision not found` 说的是"当前库里没有这次要降到的那个迁移版本" ⇒ 看到它应立刻判为**迁移不可回退**，而不是去修权限/修连接（那两类故障另有专属错误号，本例 MySQL 1045/2003）。② **不可逆迁移的正确处置是重建而非回滚**：官方给出的出路是 drop 库 + 同名 create ⇒ 这类场景里"回滚 migration"根本不存在，只能**从快照/备份重建**；因此**升级动作的前置条件必须包含"留一份可重建的库快照"**，否则降级路径形同没有。③ **同名重建是有意设计**：要求"create a new one **with the same name**" ⇒ 连接串/配置不用改，代价是数据全清；判据上要把"配置不用改"与"数据会没"分开说，不能因为前者而低估后者。④ 推论：**发布/升级文档应显式区分三类降级路径**——可逆迁移（有 down）、快照重建（不可逆但可恢复）、净重建（数据不保）；把三者统称"回滚"会让运维在真正需要时选错。
- **与既有能力分工**：rm 1.101.0「归档≠下线」管**制品还在不在服务**；本条管**schema 往下走时到底能不能退**。r519B「快照内嵌旧运行时须全量重建」管**快照的内容完整性**；本条管**快照是唯一退路时的前置留取**。
- 提升层：工作流（发布与降级路径）/ 工具（故障信号判读）。触发词：Revision not found、drop the database and create a new one with the same name、迁移不可逆、降级需快照重建、不可逆迁移。

## r524C · 锁/清单文件遇到不可识别版本时，正确姿态是「清空重取」而不是「猜测迁移」；且以目录 tree SHA 作指纹意味着粒度到目录不到文件（来源：raw.githubusercontent.com/vercel-labs/skills/main/src/skill-lock.ts 8,573B，2026-10-11 r524C 一手 curl 200 实拉、逐串命中 `CURRENT_VERSION = 3; // Bumped from 2 to 3 for folder hash support (GitHub tree` / `// If old version, wipe and start fresh (backwards incompatible change)` / `// v3 adds skillFolderHash - we want fresh installs to populate it` / `skillFolderHash: string`；来源 Qoder r526-Q-B）
- **判据**：① **版本不认识就整库清空，而不是逐字段猜**：源码注释直接把这一改动标为 backwards-incompatible，并让旧版本走 wipe-and-start-fresh ⇒ 迁移逻辑写起来最省事的做法（尽力解释旧格式）在这里被明确放弃，因为半懂不懂地解释出来的状态比没有更危险。② **清空重取有前提：源必须可重取**：锁文件本身保留了 `source/sourceType/sourceUrl/ref/skillPath` 等可重取字段，并按 `getSkillsBySource()` 分组批量更新 ⇒ "丢掉重建"只有在**能按源批量重取**时才成立；写这类策略时必须同时给出重取路径，否则清空=数据丢失。③ **目录 tree SHA 作指纹 = 粒度到目录**：`skillFolderHash` 取 GitHub Trees API 的整目录 tree SHA，目录内**任一文件变动**都判整包变更 ⇒ 好处是零漏检（不存在"改了某文件但指纹没变"），代价是噪声更新（改一个字也要整包重取）。选它就要接受重取成本，不能又想要目录级简单又想要文件级精确。④ 推论：**为任何"缓存/锁/索引"写版本策略时，要同时给出三件事**——当前版本号、遇到旧版本的姿态（迁移 or 清空）、以及清空后的重取路径。
- **与既有能力分工**：rm「备份密钥库须不同位置」管**备份的可恢复性**；本条管**元数据不可识别时的处置姿态**。av「缓存键须含策略哈希」管**结论缓存何时失效**；本条管**结构缓存（锁文件）何时废弃**。
- 提升层：工作流（升级与迁移策略）/ 工具（指纹粒度选型）。触发词：CURRENT_VERSION、wipe and start fresh、backwards incompatible、skillFolderHash、目录 tree SHA、不可识别版本清空重取。


## r526A · 发布治理的「撤销闭环」是三态而非单向：promote 可更新到新版本 → revoke 有审核流与直接动作两条路径 → 撤销后仍可再 promote，且全程保留审计历史；该能力依赖持久层迁移，升级前须先备份库（来源：api.github.com/repos/iflytek/skillhub/releases?per_page=8 67,447B，2026-10-12 r526A 一手 curl 200 实拉、逐串命中 `Global Skill promotions can now be updated to a newer team Skill version, revoked through review or direct action, and promoted again after revocation.` / `Add global Skill promotion updates, revocation review and direct revocation, retained audit history, and safe re-promotion` / `Back up PostgreSQL before upgrading. Flyway V66-V67 add the persistence required for promotion updates and revocation.`；来源 Qoder r528-Q-C）
- **判据**：① **撤销不是删除，而是「更新 → 撤销 → 再发布」三态闭环**：官方把 promotion 的更新、撤销与安全再发布放在同一条能力线上发布 ⇒ 只实现「撤下」不实现「可再发布」，治理动作就是单向不可逆的，被撤对象回不到可用态，下一次只能靠重建绕过治理。② **两条撤销路径必须分别留痕**：`revoked through review or direct action` ⇒ 有人复核的撤销与管理员直接撤销是两种不同证据强度的动作，审计历史若把二者混记，事后无法判断这次撤销是否经过复核。③ **再发布要「安全」（safe re-promotion）**：撤销后允许再发布，但它是被设计的独立动作而非撤销的反向操作 ⇒ 实现上要有独立入口与独立校验，不能让「撤销」按钮兼作切换开关。④ **撤销能力是持久层功能，不是界面开关**：官方升级说明要求先 `Back up PostgreSQL`，Flyway V66→V67 才补上 promotion 更新与撤销所需的持久化 ⇒ 治理/撤销类能力上线前必须确认持久层迁移完成并已留备份；把它当纯逻辑开关，会出现「界面能点、状态存不下、重启后回到原态」。
- **与既有能力分工**：rm「归档≠下线」管**制品是否还在服务**；rm「组件降级 Revision not found → drop+create」管**schema 往下走能不能退**；本条管**发布态本身的可撤销 / 可再发布闭环**及其**持久化前提**。av「晋升可撤销」侧管证据面，本条管治理面。
- 提升层：工作流（发布治理与审计）。触发词：revoked through review or direct action、promoted again after revocation、retained audit history、safe re-promotion、Flyway V66-V67、撤销闭环。


## r526A · 恢复能力由两个彼此独立的持久面合成：状态面（checkpoint→Postgres/S3）与排队面（queue→Redis），只配好一个 = 半恢复；已回 200 的异步 webhook 也可能整批丢（来源：www.activepieces.com/docs/install/guarantees/crash-recovery.md 3,487B，2026-10-12 r526A 一手 curl 200 实拉、逐串命中 `a checkpoint of each completed step persisted to Postgres/S3` / `the queue itself inherits the durability of your Redis` / `**Redis durability is yours.** Queued runs live in Redis. A Redis that loses its dataset loses queued jobs — including async webhooks already acknowledged with a `200` / `At-least-once, not exactly-once.` / `checkpoint cadence is fixed at 15 seconds`；来源 Qoder r529-Q-A）
- **判据**：① **「可恢复」不是一个布尔，而是逐持久面分别成立**：step checkpoint 落在 Postgres/S3，排队中的 run 落在 Redis，两者持久性各自配置 ⇒ 只把 Postgres 配扎实而 Redis 无持久化，得到的是「跑了一半能续、但已排队没开跑的全丢」。② **已应答 200 不等于已落库**：官方明写已 ack 的异步 webhook 也随 Redis 掉数据而丢 ⇒ 对外说「已接收」时，承诺必须绑定具体持久面；只凭 HTTP 状态码判断「收下了」是错的。③ **恢复粒度是时间窗不是零丢失**：`At-least-once, not exactly-once` + checkpoint 固定 15 秒节奏 ⇒ SLA 要按「最多丢多久 / 最多重跑几次」写，不能写「不丢」。④ 推论：**备份与恢复演练清单须逐持久面分列并各自验收**，恢复演练里最容易漏的正是「队列持久面」这一项——因为它平时不产生可见产物。
- **与既有能力分工**：rm「备份密钥库须不同位置」管**备份放哪儿**；本条管**多个持久面各自构成一部分恢复能力、缺一即半恢复**，以及**对外已应答的语义边界**。
- 提升层：工作流（恢复与演练）/ 工具（持久面盘点）。触发词：checkpoint persisted to Postgres/S3、queue inherits the durability of your Redis、Redis durability is yours、at-least-once not exactly-once、15 seconds、已 ack 仍会丢、半恢复。


## r526C · 发布的「到达语义」不是整体原子切换，而是按变更集切分出的触发器级增量激活：未变更的触发器保持运行，验收须逐单元确认到达且把「未变更仍在线」写成断言（来源：docs.n8n.io/build/understand-workflows/save-and-publish-workflows.md 10,173B，2026-10-12 r526C 一手 curl 200 实拉、逐串命中 `n8n works out which triggers changed between your last published version and the new one, then applies only those changes in the background. Triggers that h`；来源 Qoder r530-Q-A）
- **判据**：① **发布 = 变更集应用，不是整体替换**：平台先算出「上次发布版本与本次之间哪些触发器变了」，再只把这些变更在后台应用 ⇒ 发布后系统里同时存在「本次变更过的单元」与「沿用旧版本的单元」，把发布当成一次性全量切换会导致验收清单与实际不符。② **「未变更的持续运行」是要断言的事实，不是可以假设的背景**：原文把 `Triggers that haven't changed keep running without interruption` 作为承诺写进文档 ⇒ 验收时要逐触发器确认「变了的是否已生效、没变的是否未中断」，只验前者会漏掉发布副作用（例如某项被误判为未变更而实际没生效）。③ 推论：**发布说明的颗粒度应匹配到达粒度**——按触发器/入口单元写「本次实际生效范围」，而不是写「发布了 vX」；发布失败/部分生效时，回滚范围也要按同一单元切分。
- **与既有能力分工**：r283-C「按钮态（可部分生效）」管**失败时的可见性**；本条管**成功时的到达语义**（到达到哪一级、未变更部分怎么办）。rm「归档≠下线」管**旧制品是否还在服务**；本条管**新版本到达到哪些单元**。
- 提升层：工作流（发布与验收）。触发词：works out which triggers changed、applies only those changes、Triggers that haven't changed keep running、到达粒度、逐触发器验收、部分到达。

## r532B · 迁移暂停窗口的放行面按副作用而非 HTTP 方法界定，并用会红的枚举检查兜住新增入口；「完成」标记绑定实际写入目标，目标变更即 blocked/destination_changed，失效范围按真实写入部件精确回退（来源：api.github.com/repos/langflow-ai/langflow/pulls/15633 + /pulls/15613，2026-10-12 r532B 一手 curl 200 逐串命中 `Two GET routes stored data anyway` / `fails this test until its author adds the path to READS` / `172 of them today` / `blocked with destination_changed` / `Another bucket sends back only the file copy`）
- **判据**：① **「读」的定义是副作用不是方法名**：两条 GET 路由（OAuth 浏览器回跳）会在数据库拷贝后写 token ⇒ 维护窗口按方法批量放行只读，会把浏览器回跳 / 回调 / 审计留痕这类隐式写入漏在外面。② **隐式写入最爱藏在「读的副作用」里**：3 条只是「记一行谁读了谁的数据」却改变状态 ⇒ 判只读要单独审审计 / 指标 / 会话 / 令牌。③ **卡点必须会红**：新增 GET 路由不进 `READS` 白名单或不声明 `changes_the_instance` 就测试失败，且作者明写代价与退出条件 ⇒ 治理规则只发规范没有自动化卡点等于没有。④ **白名单要可枚举可 diff**：`172 of them today` ⇒ 「放行多少条、最近新增哪几条」是审计项。⑤ **完成是带目标的状态**：目标一变旧 done 立即失效并给原因码 ⇒ 跨环境迁移步骤要存「完成到哪」。⑥ **回退按写入部件切不按步骤名一刀切**：换 bucket 只回退文件拷贝 ⇒ 依赖图按「写了哪些部件」建模。
- 提升层：工作流（升级与迁移）/ 工具（放行面清单）。触发词：migration pause、GET 也会写、changes_the_instance、READS 白名单、destination_changed、按写入部件回退。

- **判据**：① **慢迁移是启动可用性杀手**：慢回填 + CONCURRENTLY DDL 卡在 boot lock 下、replica 空等 ⇒ 迁移/升级阻塞启动的系统要把慢步骤拆出启动锁后台跑。② **拆双轨看"持不持启动锁"**：DDL 原子变更留 boot 锁；数据回填可重试可观察移出。③ **后台轨必须健康门控**：状态落库 + /health 暴露 failedMigration ⇒ 发布节奏挂在"后台迁移是否完成"信号上。④ **跳过版本有 boot lockout 黑洞**：依赖上一版后台回填的阻塞迁移在跳版时 guard 抛错→启动失败→runner 永不跑⇒要 catchup 循环（类型化错误 + 硬上限 10 次）。⑤ **全新安装防"表不存在"假错**：guard 前 ensure 表存在。
- 提升层：工作流（升级与迁移）/ 工具（健康门控）。触发词：non-blocking background migration、双轨迁移、boot lock 拆分、post-listen、background_migrations、health 暴露 failedMigration、跨版本 catchup。

## r535C · 内部操作绑自身内址而非外网 public URL；耦合外部可达性是分体/容器部署隐性故障面（来源：api.github.com/repos/activepieces/activepieces/pulls/16037，2026-10-12 r535C 一手 curl 200 逐串命中 `Workers downloaded piece bundles from the app's public URL` / `public URL did not lead back to this app from inside the worker container` / `fetch failed when the public URL is localhost` / `internalApiUrl ... worker already uses for its socket and every engine callback` / `Single-container installs resolve it to 127.0.0.1`）- **判据**：① 内部操作（安装/回调/引擎通信）绑组件自身内部/loopback 地址，不是 public URL。② 外部可达性不是内部依赖：分体部署下 public URL 指不回本 app = 隐性故障面。③ 内部用 internalApiUrl、对外只用 publicUrl，二者分用途不可混。④ 删能力后复查其引入的地址/依赖耦合。⑤ 用「收到的是哪个 URL」断言内部绑定，不只测能装上。- 提升层：工作流（部署与拓扑）/ 工具（内部地址绑定）。触发词：worker downloaded from app's public URL、internalApiUrl vs PUBLIC_URL、fetch failed localhost、PIECE_BUNDLE_NOT_AVAILABLE、split app/worker、single-container 127.0.0.1、public URL only for outside。

## r541A · 形状迁移防御=让旧形状编译期不兼容：内联 JSON 迁行表时漏改一处读者=看到空集且不报错（来源：api.github.com/repos/n8n-io/n8n/pulls/40754 25,179B，2026-10-12 r541A 一手 curl 200 逐串命中 `moves agent skill refs out of the agents.schema and agent_history.schema JSON into rows` / `If B2 misses one of them, that code sees an agent with no skills, and nothing fails.` / `Its skills key is opaque, so a stored config does not fit AgentJsonConfig` / `The compiler rejects every direct or indirect reader of stored skill refs` / `AgentSkillRefsService has refsForDraft, refsForVersion and replaceDraftRefs` / `toAgentDocument and fromAgentDocument compose and split the document`）- **判据**：① 漏改一处直接读者=静默看到空集，防御是旧形状 opaque + 编译器拒绝每个读者，把风险从人漏前移到编译器拦。② 读写集中单一服务 + 边界 compose/split，后续迁移只改一个服务内部。③ 不兼容须在编译期发生，前提是存储类型与文档类型显式分家。④ 与 rm KB:31（对外引用破坏）分工：那条管对外发布引用盘点，本条管对内存储形状迁移的编译期防护。- 提升层：工作流（迁移工程纪律）/ 工具（类型系统当门禁）。触发词：opaque stored type、compiler rejects direct readers、sees an agent with no skills and nothing fails、one service refs、document at the edges、形状迁移编译期不兼容。

## r541B · 版本号是跨部署面一致性对象：off-cycle 发版须同步回全部部署面（Helm appVersion/compose app+worker 双 tag/package.json），漏改即下次发布读陈旧版本且不报错（来源：api.github.com/repos/activepieces/activepieces/pulls/16203 23,419B + /files（Chart.yaml/docker-compose.yml/package.json 三文件），2026-10-12 r541B 一手 curl 200 逐串命中 `version bump is not on main` / `the next weekly release does not read a stale version` / `Merge before the next release-candidate cut (Thursday 5 PM UTC)`；提名 Qoder r540-Q-A ⑤）- **判据**：① off-cycle 发版绕过 bump 流程会版本分叉，发版检查单须含「版本号写回全部部署面」。② 版本号消费方是一组面，漏改任一面下游按陈旧版本运行且不报错；同步 PR 验收=逐面断言版本相等。③ 同步 PR 带时限锚点（下一个 RC 切点前），无时限即漂成部署债。④ 与 rm 1.116.0（调用地址一致性）分工：同属「同一事实多面各存一份」，一个在地址面一个在版本面。- 提升层：工作流（发布治理）/ 工具（版本同步检查）。触发词：off-cycle release、stale version、Helm appVersion、compose app+worker image pin、package.json version、RC cut 时限锚点。

## r541B · 退场记两个日期（服务停止日≠数据删除日）+ 保留期可调但有硬顶，未选定时用硬顶（来源：pipedream.com/docs/workflows.md 2,474B + activepieces audit-logs/overview 385,091B，2026-10-12 r541B 一手 curl 200 逐串命中 `shut down on March 31, 2027` / `permanently deleted by April 30, 2027, including the credentials and OAuth tokens` / `from 30 to 3650 days. The cap is a hard limit` / `A platform that has not chosen a period uses the cap`；提名 Qoder r539-Q-A ②）- **判据**：① 服务停止与数据删除是两个日期，迁移窗口=差值；凭据随数据删除要单列高危。② 保留期同时记可调范围与硬顶（3650 天=容量表上界来源），硬顶兼作未选定默认值 ⇒ 默认值不可推断，先查是否显式设过。③ 与迁移准入四门分工：那条管作业开跑前，本条管时间边界台账。- 提升层：工作流（依赖退场与容量规划）/ 工具（保留期配置审计）。触发词：shut down vs permanently deleted、迁移窗口、credentials deleted、AP_AUDIT_LOG_RETENTION_DAYS、30 to 3650 hard cap、未选定用硬顶。

## r545B · 实例-分支拓扑与单向流动纪律：同一实例不要既 push 又 pull（双向流=冲突+覆盖+data loss）；多环境晋升用「每环境一分支+PR 过闸」买安全层，用「一分支多环境」买即时性（代价=误推直接进生产）；版本灰度可用「同分支新实例」；分支切换非事务——不清空实例，旧分支内容全部残留成混合态（来源：docs.n8n.io `administer/use-source-control-and-environments/choose-branching-patterns.md` 6,562B，2026-10-12 r545B 一手 curl 200 实拉、逐串命中 `n8n doesn't recommend this. To reduce the risk of merge conflicts and overwriting work, try to create a process where work goes in one direction: either to Git, or from Git, but not both.` / `Pushing and pulling to the same instance can cause data loss as changes are overridden when performing these actions.` / `You have to do a pull request in GitHub to copy work between environments.` / `you can create a new n8n instance with the new version, connect it to the Git branch and test it, while your production instance remains on the older version until you're confident it's safe to upgrade.` / `n8n doesn't clean up the existing contents of an instance when changing branches. Switching branches in this pattern results in all the workflows from each branch being in your instance.`）
- **实证（逐串）**：官方建议 don't push and pull to the same n8n instance——work goes in one direction: either to Git, or from Git, but not both（降低 merge conflicts 与 overwriting work 风险）；同实例双向 push/pull can cause data loss as changes are overridden。四模式：① Multiple instances, multiple branches——每实例绑自己的分支，dev 推分支 → GitHub PR → prod 分支 → pull 到 prod 实例；优势是 added safety layer（必须过 PR 才能把工作复制到生产）且支持两个以上实例；劣势是手动步骤多。② Multiple instances, one branch——多实例同一分支，工作流/标签/变量处处相同，push 即对其他环境可用；可用于版本测试（新版本实例连同一分支试跑，生产实例停在旧版本 until you're confident it's safe to upgrade）；风险是误推直接把工作送进生产，用 GitHub Action 自动 pull 到生产时要么回到多分支模式、要么保证永不推不想进生产的内容。③ One instance, multiple branches——owner 可切换实例连哪个分支，用于评审（评审实例在不同分支间切换加载不同人的工作）；**No cleanup**：切换分支不清空实例，结果是把各分支的工作流全部混在一个实例里。④ One instance, one branch——最简单。
- **判据**：① **发布拓扑先定流动方向**：同一实例既 push 又 pull = 双向流，冲突与覆盖风险随双向性而来（官方明示 data loss as changes are overridden）⇒ 内容要么单向进 Git、要么单向出 Git；确需双向必须有显式过闸（PR/评审），不能靠「小心一点」。② **环境晋升的安全层是「过闸动作」不是「意识」**：每环境一分支 + PR 过闸 = 复制到生产前有一道无法绕过的评审；一分支多环境用即时性换掉这道闸，代价是误推直达生产 ⇒ 自动化 pull 到生产的场景必须配多分支拓扑，或证明「永不推不想进的内容」是可执行约束。③ **分支拓扑即灰度开关**：同分支新实例试跑新版本、生产实例钉旧版本直到有信心——灰度不需要额外机制，是拓扑属性。④ **分支切换非事务，残留是默认行为**：切换不清空 ⇒ 「切过去看看」必然留下混合态；评审/试跑用完要显式清理，不能假设切换=替换（与 rm §归档不等于下线同向：位置变化≠状态重置）。⑤ 与 §版本号是跨部署面一致性对象（rm 1.118.0）分工：那条管版本号本身要同步到所有部署面，本条管实例-分支拓扑与内容流动方向。
- 提升层：工作流（发布拓扑与环境晋升）/ 工具（多环境治理）。触发词：don't push and pull to the same instance、one direction only、多实例多分支、PR 过闸晋升、一分支多环境、误推进生产、同分支新实例灰度、分支切换不清空、mixed state instance、overwriting work data loss。

## r545B · 共享文件改动的版本传播 + 提交前版本复位：改一个被导入的文件，所有受影响组件都要 bump；本地迭代号不是注册表版本，提交前必须复位（来源：pipedream.com/docs/components/contributing/guidelines.md 43,298B，2026-10-12 r545B 一手 curl 200 实拉、逐串命中 `If you update a file, you must increment the versions of all components that import or are affected by the updated file.` / `make sure to set it to the version it should be at in the registry prior to submitting your PR. For example, when you add an action to the registry, the version should be 0.0.1. If the action was at version 0.1.0 and you've fixed a bug, change it to 0.1.1 when committing your final code.` / `increment the MAJOR version when you make incompatible API changes, MINOR when you add functionality in a backwards compatible manner, and PATCH when you make backwards compatible bug fixes.`）
- **实证（逐串）**：① 改了文件，必须 bump **所有 import 或受该文件影响的组件**的版本——版本传播面=被影响面，不是被改面。② 本地开发把版本递增过多次后，提交 PR 前必须设成注册表应有的版本：新 action 进 registry = `0.0.1`；曾在 `0.1.0` 修了 bug ⇒ 提交最终代码时改 `0.1.1`——本地调试计数器与发布计数器是两回事。③ semver 三档判据：MAJOR=不兼容 API 变更，MINOR=向后兼容的新功能，PATCH=向后兼容的 bug 修复。
- **判据**：① **共享文件改动有隐藏的依赖方面**：改一个被 N 个组件导入的文件，只动文件本身不够——N 个消费方的版本全部要递增，否则下游拿着旧版本号引用新内容（或拿着新号跑旧内容），且不报错；发布检查必须算「被影响面」而不是「被改面」。② **本地迭代号 ≠ 发布号**：本地调试递增的版本号带着开发痕迹，原样提交会让版本历史失去语义（一个「修复」可能顶着一个 0.4.7）⇒ 提交前复位到目标 registry 版本（新进=初始版，修复=补丁位，新功能=次版本）。③ **semver 档位按兼容性判，不按改动量判**：「改了挺多」可以是 PATCH，「只改一行」可以是 MAJOR（签名/契约变了）——档位判据是兼容性影响面。④ 与 §版本号是跨部署面一致性对象（rm 1.118.0：同一制品的所有部署面要同步）分工：那条管**同一制品多面**，本条管**共享依赖的多消费方传播 + 本地/发布两个计数器**。
- 提升层：工作流（版本治理）/ 工具（发布前检查清单）。触发词：increment versions of all affected components、共享文件改动传播版本、被影响面不是被改面、本地迭代号 vs 注册表版本、提交前版本复位、0.0.1 新进、0.1.1 修复位、semver 三档按兼容性。

## r546A · 导入/合并配对按稳定 id 优先于名称：名称变更因此降为非破坏性（rename-column 不再挡 apply、不再要确认）；破坏性判定只留真正丢数据的操作（删列/改类型）；拒绝集显式枚举且拒写（名称 swap/cycle、id 跨表冲突、包内重复 id，拒绝时 nothing written）；旧包按名称配对并静默采纳包 id（表计 matched 需 dataTable:update）；竞态限制诚实声明（两 import 争同一 id→第二张表 DB 错误回滚）（来源：api.github.com/repos/n8n-io/n8n/pulls/40709，2026-10-12 merged 14:11Z，一手 gh api 逐串命中）
- **实证（逐串）**：改名的数据表列在包导入与晋升 apply 时**保留其值**——导出含每列 id，导入按 id 配对。配对（`overwrite`、`overwrite-non-destructive`）：**先按 id、再按名称**；目标列接纳包 id，新表保留；无 id 的旧包按名称配对如初。**改名是非破坏性的**：新增 `rename-column` 变更类型，只有删列或改类型才算破坏性 ⇒ 改名不再挡 apply、不再要确认。旧导入来的表列 id 不同：首次导入按名称配对并**静默采纳包 id**，表计 `matched` 且需 `dataTable:update`。**拒绝且什么都不写**：同表内列名 swap 或成环、某列 id 已被另一张表使用、一个包内同一列 id 用两次。顺带修：删列不再误报 `reorder-columns`；CLI/API/UI 文案不再把改名称为破坏性。已知限制：旧版 n8n 导不进带列 id 的包（先升级导入方实例）；两个导入争同一列 id 时第二张表以数据库错误回滚。
- **判据**：① **配对/合并按稳定标识优先于名称**：名称可改而 id 稳定 ⇒ 按 id 配对让"改名"从破坏性变更降为非破坏性——名称配对下每次改名都触发冲突确认，按 id 配对后改名只是 `rename-column`。② **破坏性判定按数据损失判，不按"字段变了"判**：删列/改类型丢数据算破坏性，改名不丢——变更分类判据是数据损失面。③ **拒绝集显式枚举且拒写**：名称 swap/cycle、id 跨表冲突、包内重复 id——拒绝时什么都不写（nothing written），不做部分应用；拒绝理由逐类命名。④ **旧数据迁移路径显式**：无 id 旧包按名称配对并静默采纳包 id、表计 matched 需 `dataTable:update`——兼容路径的账要记清，不能假装一次到位。⑤ **竞态限制诚实声明**：两导入争同一 id⇒第二张表 DB 错误回滚，作为 known limitation 写明，不假装原子。⑥ 与 r436B（同名主键冲突按破坏性变更申报）分工：那条管"同名冲突怎么申报"，本条管"按 id 配对把改名降为非破坏性 + 拒绝集形状"。
- 提升层：工作流（导入/晋升变更分类）/ 工具（配对与拒绝集设计）。触发词：配对按 id 优先、改名非破坏性、rename-column、破坏性按数据损失判、拒绝集拒写、swap/cycle 拒绝、id 跨表冲突、旧包静默采纳 id、matched 需 update、竞态回滚已知限制。


## 方向性 diff 的面板锚点应是「将被更新的那一方」，不是固定的本地/远程（来源：docs.n8n.io/administer/use-source-control-and-environments/compare-versions.md 4,906B，2026-10-13 r547C 一手 curl 200 实拉逐串命中，KB-direct：SKILL.md 正文已达 500 行上限）
- **实证**：n8n 工作流 diff 视图在**推**与**拉**两种场景下上下两个面板的本地/远程位置**互换**——推送时上面板=Git 仓库最新版本（远端）、下面板=实例当前保存版本（本地）；拉取时上面板=实例当前版本（本地）、下面板=Git 版本（远端）。但 n8n 明确了一条恒定规则："**In both cases, the top panel always displays the workflow that will update with changes.**"变更以三类着色：新增（绿 + "N"）、修改（橙 + "M"）、删除（红 + "D"）；修改的节点可点开再看**该节点的 JSON diff**，在决定推或拉之前核对确切配置。
- **判据**：① **方向性对比视图的锚点是"谁会被改"，不是"本地/远程"**：推与拉互换了位置，若按位置标注（"上面是远端"），有一半场景读者会把方向读反，且反得毫无察觉——**把位置语义换成影响语义，视图在两种方向下都自洽**。② **"决定前可核对"是差异视图的存在理由**：页面定位是"understand the exact changes ... **before you decide to either push or pull**"——差异视图不是装饰，是把不可逆动作前移成可审动作的装置；没有 diff 的推/拉等于盲签。③ **变更分类要三态齐全且可机读**（新增/修改/删除各带颜色与图标）：只有"有变化"会让读者自己去分辨是加还是删。④ **汇总层之下要有逐项下钻**（修改节点 → JSON diff）：只看汇总无法判断配置是否被改坏，下钻到对象级才是可裁决的粒度。⑤ 与 rm 1.120.0（实例-分支拓扑与单向流动）+ av 2.231.0（证明哈希排除时间戳）配套：前者定"往哪流"，本条定"流动前看什么"，后者定"证明怎么存"。
- 提升层：工具（版本对比视图设计）/ 工作流（推拉前的变更评审）。触发词：diff 面板锚点、top panel 将被更新的一方、推拉面板互换、影响语义替代位置语义、三类变更 N/M/D、节点级 JSON diff、决定推拉前先核对、compare-versions。

## 单向迁移线的两侧都要有检查：线前「前置条件清单」按本次实际需要裁剪，线前最后一刻「对副本重跑同一批检查」；差异处置只有重拷与显式认领两条（来源：api.github.com/repos/langflow-ai/langflow/pulls/15679 一手 curl 200，2026-10-13 r549B 实拉正文逐串命中）
- **实证**：问题面："The page walked an admin through the checks and the copies, and then stopped. The last two steps said 'Coming soon'. The data was copied and people were still locked out, and nothing on the page said how to tell that everything had arrived or how to start the new instance. Nothing at the top said what had to be ready either, so an admin found out one step at a time, the last of it after the pause." 新增前置面："'What you'll need' sits above the steps. It lists what has to be ready elsewhere, **each thing only when this instance's move calls for it**: an empty PostgreSQL database for an instance on SQLite, the pgvector extension when knowledge bases are on this server, a bucket and its keys when files are, then access to where the new instance runs, a place off this server for the backup, and a time when people can pause their changes. It is open until the first check is done, then closed and one click away." 收口面："'Check the copy' is the last step before the one-way line. It runs the checks of the first step against the copied data and sets each result beside this instance's. It runs **before the new instance starts, so what is missing can still be copied again**. A copy that matches is done with no click. With a difference, the step shows **only what differs, with what each side said**, and the admin either copies again or ticks that the difference is expected and continues. That word names the check the admin read..."
- **判据**：① **前置条件必须先于步骤清单呈现，且按本次迁移的实际形态裁剪**：全量罗列会让管理员自己判断哪条适用，漏判恰好发生在"以为不适用"的那条上 ⇒ **"需要准备什么"要由系统按实例配置推导，而不是交给执行者筛**。② **单向线之前必须用同一批检查重跑副本**：首步检查的是源，跨过不可逆线前检查的必须是目标 ⇒ **只验一遍等于承认"复制过程无损"这个没人证明过的假设**；重跑点要放在"还能再拷一次"的位置。③ **差异只呈现差异，并同时给出两侧各自的说法**：全量重排会让管理员在大量相同项里找不同，而只给结论不给两侧原值则无法判断谁对 ⇒ **比对输出的最小充分单元是"这一项 + 两侧原值"**。④ **差异处置只允许两条路，且都要显式**：重拷，或勾选"该差异是预期的"——勾选动作必须**指名它所依据的那条检查**（原文 "That word names the check the admin read"）⇒ **"我知道了"不是裁决，指名依据才是**。⑤ **向导里未完成步骤（"Coming soon"）是一种停机故障**：流程走到断点、数据已拷贝、用户被锁在外面却没有任何指引 ⇒ **流程类界面的半成品状态必须自带"现在你该怎么办"，否则它就是新的故障源**。⑥ 与 rm 1.117.0（形状迁移让旧形状编译期不兼容）/ av 2.238.0（回滚只恢复代码不恢复数据形态）分工：那两条管**迁移的不可逆性怎么表达**，本条管**不可逆线两侧的验证与差异裁决怎么做**。
- 提升层：工作流（迁移/升级编排与单向线管理）/ 工具（迁移向导与比对输出设计）。触发词：单向线前重跑检查、对副本重跑、前置条件按形态裁剪、只显示差异与两侧原值、差异预期显式勾选、勾选要指名依据、Coming soon 是停机故障、迁移页断点、副本核验、check the copy。

## 运行时迁移会静默改写资源上限：上限由多层共同决定，「不设限」要用 null 显式表达而不是给个大值（来源：api.github.com/repos/activepieces/activepieces/pulls/16400 一手 curl 200，2026-10-13 r549C 实拉正文逐串命中）
- **实证**："Deno code steps run with a hardcoded 128MB V8 heap cap (`--v8-flags=--max-old-space-size=128`), but the legacy lane it replaced only capped the heap in the **code-only** execution modes (the v8-isolate sandbox, `memoryLimit: 128`). In `UNSANDBOXED` and `SANDBOX_PROCESS` — the cloud path — legacy spawned `node --eval` with **no V8 flags**, so the only ceiling was the sandbox cgroup." 后果："Migrating to Deno **silently tightened the per-step limit** from 'hundreds of MB (cgroup)' to 128MB." 现网表现："flow ... ran successfully 12×/day for a week on legacy, then died with `Deno process exited with code null and signal SIGTRAP` on its first Deno run. Reverted as containment; this PR restores parity so it can be re-migrated." 修复形态："`deno.run` accepts `memoryLimitMb: null`, which **omits the `--max-old-space-size` flag entirely** (default stays 128MB for all existing callers...)"，并按 legacy 的 mode 划分逐一对齐（`UNSANDBOXED`/`SANDBOX_PROCESS` → null；code-only 两档 → 128MB）。
- **判据**：① **换运行时等于换一套默认资源上限，而这不在 release notes 里**：迁移评审要单独列一项"每种执行模式下的内存/CPU/超时上限各是多少"，逐模式比对新旧 ⇒ **只比对"能不能跑通"，会让收紧型变更在长时间稳定运行后才暴露**（此处稳定跑了一周才在首次 Deno 运行炸）。② **上限是分层的，只对齐一层不算对齐**：V8 标志是一层、cgroup 是另一层；旧路径"没有 V8 标志 + cgroup 兜底"，新路径"128MB 硬顶" ⇒ **"加了一个更严格的上限"与"把上限设满了"是两种变更，不能互相代替**。③ **"不设限"是一个需要显式建模的值**：用 `null` 表达"不传这个标志"而不是填一个很大的数 ⇒ 用大数表达"不限"会在某个真实工作负载上变成新的隐性天花板，且从配置里看不出来。④ **失败信号是 SIGTRAP / exit code null，不是 OOM 报错**：资源上限触发的崩溃形态随运行时而变 ⇒ **迁移后的故障判读要重新校准，不能沿用旧运行时的错误字典**。⑤ **先回滚再对齐，不要在线上边跑边调**：原文明确以回滚作为遏制手段、恢复语义对等后才重新迁移 ⇒ **语义对等是重新迁移的前置条件，不是迁移后的优化项**。⑥ 与 rm 1.124.0（单向线前对副本重跑检查）互补：那条管**数据/形态迁移的验证**，本条管**执行环境的资源语义对等**。
- 提升层：工作流（运行时/沙箱迁移评审）/ 工具（多层资源上限建模）。触发词：迁移静默收紧上限、逐执行模式比对、V8 标志与 cgroup 两层上限、memoryLimitMb null 不设限、大数表达不限是隐性天花板、SIGTRAP、exit code null、先回滚再对齐、语义对等后才能重迁、默认上限漂移。


## 特性退役的验收是「非对称」的：新增只需一处增益、移除必须零回归，且必须按候选集合而非单特性评估（来源：arxiv.org/abs/2610.13806 FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems，45,808B，2026-10-13 r551C 实拉 abs 页逐串命中 `feature-lifecycle asymmetry: adding new features must produce gains on some metric, while feature removal must not regress any metric` / `it evaluates candidate feature sets constructed from all the low-rank features through grouped ablation` / `Lineage tracing identifies all downstream consumer models to realize the full savings` / `3 nested candidate sets of 32, 48, and 59 features` / `Online guardrails rejected the largest treatment` / `removing 43.3% of the model features` / `the impact on efficiency depends on model characteristics`；r551C 落地）
- **实证**：生产推荐系统的特性生命周期不对称——新增只要在某个指标上有增益即可，移除必须在**任何**指标上都不回归。退役难以排期的六个原因：与别的特性交互、重要性逐日变化、模型或数据漂移前无法评估、与其他上线争抢 A/B 位、在线 A/B 里造成回归、被多个模型消费需协调。FORTE 的做法：高效扰动实现支持**每日**评估；为处理交互，用**分组消融**评估由全部低秩特性构造出的候选**集合**，其离线结果足以预测在线 A/B；**血缘追踪**找出全部下游消费模型以实现完整收益。验证：搜索相关性模型给出 3 个嵌套候选集（32/48/59 个特性），**在线护栏否掉了最大的那一档**，48 个特性那档被选中，移除该模型 **43.3%** 的特征；大型排序模型识别 8 个候选，重训 + A/B 确认无回归；效率收益依赖模型特性，非通用结论。
- **判据**：① **增删不能用同一套验收标准**：新增的判据是「存在增益」，移除的判据是「不存在回归」⇒ 把「证明有价值」当成退役门槛，退役永远排不上队，系统只增不减。② **交互使单特性评估无效**：一个特性「看起来可删」但删不掉，是因为它与其他特性共同起作用 ⇒ 评估单位必须是**候选集合 + 分组消融**，逐个评估会在最后一步失败并浪费整轮预算。③ **收益面由消费者数量决定，要先做血缘追踪**：只从训练集删掉而下游消费模型仍在，节省就没兑现 ⇒ 退役清单要包含「谁还在消费它」，否则 ROI 计算是虚的。④ **离线结论要能预测在线才配占 A/B 位**：A/B 位是与上线争抢的稀缺资源，离线结果若与在线无关，退役实验就是纯成本 ⇒ 进在线前先声明离线-在线的可预测性依据。⑤ **候选集要嵌套给出，把护栏留在回路里**：一次给 32/48/59 三档，在线护栏否掉最大档、选中 48 档 ⇒ 只提交一个「最优集」会把护栏降级成通过/不通过，失去可回退的中间档。⑥ **收益必须按模型分报并声明非通用**：43.3% 属于搜索相关性模型，排序模型只识别出 8 个候选 ⇒ 退役收益是模型特性相关的，跨模型外推要先声明。⑦ 与 §批量退役三闸（PRUNE_CAP / 期望集+豁免名册）分工：那条管**清理动作的破坏面上界**（别误删、失败即停），本条管**退役决策的验收非对称、交互处理与在线护栏嵌入**（凭什么删、一次删多少）。
- 提升层：工作流（特性与能力退役治理）/ 工具（评估与 A/B 资源分配）。触发词：特性退役非对称、分组消融、候选集合评估、血缘追踪找下游消费者、嵌套候选集、在线护栏否掉最大档、离线预测在线、退役收益按模型分报。

## r552A · 准入控制要前置到「选择/分发」阶段：只在下游转换点设限，会把必然被拒的请求也发出去，换来拒绝-重排循环、优先级反转和被拒者占用他人配额（来源：api.github.com/repos/PrefectHQ/prefect/pulls/23084，2026-10-13 r552A 一手 gh api 200 逐串命中 `Deployment concurrency limits are enforced at the Scheduled -> Pending transition, but the work-pool polling query knows nothing about them` / `a deployment with 300 queued runs and 1 free slot has all 300 runs handed to a worker, 299 get rejected into AwaitingConcurrencySlot and rescheduled ~30s out, and the same set is re-selected on the next poll` / `FIFO inversion within a tier, because a bumped run loses its place to runs that were scheduled later` / `runs of a deployment with no slots left are skipped in the innermost lateral, so they don't consume queue or pool slots another deployment could use` / `a deployment with partial capacity contributes at most limit - active_slots runs, earliest scheduled first` / `CANCEL_NEW deployments are exempt: those runs must reach a worker so the transition can cancel them` / `an inactive limit offers no slots` / `SecureFlowConcurrencySlots is untouched and stays the authority for races between concurrent workers — this only stops handing out runs that the transition would certainly reject` / `Slot decay is not modeled in the query` / `The per-deployment cap is applied after the pool-level LIMIT in the Postgres template, so a poll can return fewer runs than the pool has capacity for`；r552A 落地）
- **实证**：部署级并发上限原先只在 `Scheduled -> Pending` 转换点执行，而 work-pool 轮询查询完全不知道它。于是「300 个排队运行、只剩 1 个空位」时，300 个全部发给 worker，299 个被拒进 `AwaitingConcurrencySlot` 并在约 30 秒后重排，下一轮轮询又选中同一批。两个后果：每次尖峰都来一轮 poll/reject/reschedule 循环，压 API 与数据库；同层内 FIFO 反转——被挤下去的运行把位置输给了更晚上才被调度的运行。
- **判据**：① **只在下游转换点设限，等于不设限**：准入判断若只有执行点有，选择器会把必然被拒的候选也发出去 ⇒ 限额类约束要在「选谁」与「放谁过」两层都实现，且两层的判据必须同源。② **被拒的请求会消耗别人的配额**：299 个被拒运行仍占着 queue/pool slot，别的部署本可以用 ⇒ 准入失败不能免费，浪费面要按「谁因此拿不到资源」算。③ **拒绝-重排会形成正反馈循环**：同一批被反复选中、反复拒、反复重排 ⇒ 看到「尖峰时下游压力飙升」先查选择器是否在重复投递注定失败的候选。④ **部分容量按最早优先取上限差**：`limit - active_slots`，「剩 1 个槽、几百个合格」时取 1 个，不是 0 也不是几百 ⇒ 限流取值要写成可算的表达式，别用「还有空位就全给」。⑤ **需要到达才能取消的形态必须豁免**：`CANCEL_NEW` 部署的运行必须到达 worker，转换点才能取消它们，否则它们永远停在 Scheduled ⇒ 豁免清单要按「下游要靠这次到达完成什么动作」逐条列，不能一刀切。⑥ **权威仍在竞态裁决处，本层只挡必然被拒**：原文明写 `SecureFlowConcurrencySlots` 仍是并发 worker 间竞态的权威，本次改动只停止投递确定会被拒的运行 ⇒ 分层准入要声明各层负责哪类不确定性，重叠或留空都会出事故。⑦ **未建模维度要按保守处理并写进结论**：slot decay 未进查询（部署级限额 `slot_decay_per_second = 0` 故精确；衰减型限额会被保守对待一个轮询周期）⇒ 简化假设的方向必须是「少给」而不是「多给」。⑧ **分层位置决定容量填不满，要诚实声明**：Postgres 模板里每部署上限加在池级 `LIMIT` 之后，池有余量时一次轮询也可能返回更少运行 ⇒ 已知的容量缺口要写进设计说明，别让运维按「池有多少空位就返回多少」做预期。
- 提升层：工作流（准入控制分层与配额归属）/ 工具（选择/分发查询的准入前置）。触发词：准入只在下游转换点、300 runs 1 slot、poll reject reschedule 循环、FIFO inversion、被拒者占他人 slot、limit - active_slots earliest first、CANCEL_NEW 豁免、权威仍在竞态层、slot decay 未建模、分层 LIMIT 容量填不满。
- 与 rm「关键环境的准入闸门要做成动作级硬约束，不是流程文档」分工：那条管**发布/上线类动作的准入如何绕不过去**，本条管**运行时配额型准入在选择阶段的前置与被拒者成本归属**。

## r552B · 退场残留的清理要按「残余代价」定默认值：纯视觉且不计费的残留不值得默认开启清理，清理失败只能警告不能掩盖主结果，清掉面板条目不等于清掉证据（来源：api.github.com/repos/zenml-io/zenml/pulls/4993，2026-10-13 r552B 一手 gh api 200 逐串命中 `After a step sandbox finishes, the Modal app entry remains in the Modal dashboard as deployed, Tasks: 0` / `This is purely visual clutter — idle apps incur no compute charges — but accumulates quickly for users running many ZenML pipelines or steps on Modal (each step run creates one app named zenml-<step-run-id>-<step-name>)` / `a new stop_app_after_run: bool = False setting` / `early-returns when the setting is False, otherwise calls stop_modal_app() with warning-only error handling so cleanup can never mask the step result` / `modal.App has no public .stop() method. The Modal CLI is the only supported programmatic path for stopping a deployed app` / `inject MODAL_TOKEN_ID / MODAL_TOKEN_SECRET from ZenML's configured credentials so the call works regardless of ambient auth state` / `Stopped apps are still visible in the "recently stopped" section with their full log history intact, so debugging is unaffected`；r552B 落地）
- **实证**：step 沙箱结束后，Modal 面板里留下一条 `deployed, Tasks: 0` 的 app 记录——纯视觉杂乱，空闲 app 不计算力费用，但每个 step run 都会建一个 `zenml-<step-run-id>-<step-name>`，跑得多了积累很快。修复新增 `stop_app_after_run: bool = False`（step operator 与 orchestrator 两个 flavor 共用的 `ModalSettingsMixin`），开启时覆盖 #4990 引入的 `cleanup_step_submission()` 钩子，在沙箱到达终态后经 subprocess 调 `modal app stop --yes <app-name>`，面板条目从 deployed 转为 stopped。
- **判据**：① **清理的默认值由残余代价定，不由「看起来干净」定**：本例残留不计费、不占配额，只是列表变长 ⇒ 默认关闭、按积累速度由使用者决定；若残余会计费、会耗尽配额或会顶到配额表上界，默认值就必须反过来。② **清理失败只能警告，不能掩盖主结果**：`warning-only error handling so cleanup can never mask the step result` ⇒ 附属动作的失败不得翻转主动作的终态，否则一次面板清理失败会让整个 step 判红。③ **清理后必须保留可观测性**：stopped 的 app 仍在「recently stopped」区且日志历史完整 ⇒ 「面板上不再显示 deployed」不等于「证据被销毁」，退场动作要先确认残留物是否仍可取证。④ **没有公开 API 时的替代路径要显式注入凭据**：`modal.App` 无公开 `.stop()`，CLI 是唯一受支持的编程路径；凭据从 ZenML 自身配置注入而不依赖 ambient auth ⇒ 否则换一个执行环境（无环境变量、不同身份）调用就静默失效。⑤ **钩子可覆盖且关闭时早退**：设置为 `False` 时 `cleanup_step_submission()` 直接 early-return ⇒ 可选清理要走可覆盖钩子 + 默认早退，不要把清理逻辑焊死在主路径里。
- 提升层：工作流（资源退场与清理分级）/ 工具（退场残留的默认值决策）。触发词：deployed Tasks 0 残留、stop_app_after_run 默认 False、warning-only 不掩盖主结果、recently stopped 保日志、无公开 API 走 CLI、凭据注入不靠 ambient auth、cleanup 钩子早退。
- 与 av「收尾清理失败不许被'结果已出'吞掉——清理失败要改成显式错误，否则下一次运行带着脏状态却显示上轮绿」分工：那条管**残余会造成脏状态影响下一次运行**（此时必须显式错误），本条管**残余只是视觉 clutter 且不计费**（此时警告即可）——判据是「没清理掉的残余会不会影响下一次运行」，不是清理动作本身重不重要。
## r553A · 引用必须自足到能唯一确定目标：缺一个维度，解析就退化为「当前排名」，环境一变即静默改绑（来源：api.github.com/repos/activepieces/activepieces/pulls/16264，2026-10-13 r553A 一手 gh api 200 正文逐串命中）
- **实证**："the server's default model on agent create saved a provider and model but no key, so the run (and the picker) followed whichever key ranked first. Adding a second key of the same provider silently moved the agent to it." 修法："Create pins the chat key"、「Any save that names a provider without a key pins the key a run would use right then」、"Moving an agent keeps its key if the target project can use it, otherwise re-pins… This runs inside the move transaction, on the locked row and its connection."；失效呈现："A pick that no longer exists shows an amber `Unavailable` chip and is never swapped silently. A deleted tier shows its replacement as `Moved`."；不完备记账："Agents saved before this PR stay unpinned until their next save. There is no backfill migration."
- **判据**：① **缺省一个维度不是"少记一个字段"，而是把绑定从显式改成动态**：引用不完整时，解析只能回落到运行时状态（当前排名）⇒ **环境里任何新增同类资源都会改写既有绑定的指向**，且没有任何报错。② **补全要以"此刻运行时会选到谁"为准，并在同一事务的锁定行上完成**：移动/改名时的重绑必须落在事务内、对锁定记录做，事后异步补会留下漂移窗口。③ **目标失效要显式呈现，不替代用户换**：不存在标 `Unavailable`、已删给 `Moved`（附带迁移路径），选择层"never writes a default by itself" ⇒ **静默替换是把一次需要用户确认的变更伪装成没有发生**。④ **迁移的不完备必须写进台账**：无 backfill 迁移要让"存量仍是未 pin 状态、下次保存才补全"显式可见，否则账实不符。⑤ **与既有条目分工**：rm「配对按稳定 id 优先于名称 / 改名因此降为非破坏性」管**标识变了怎么配对**；rm「换默认不回填存量引用」管**默认值变动与存量的关系**；本条更前置——**问引用本身是否自足**，不自足时前两条都无从生效。
- 提升层：工作流（引用与绑定治理）/ 可复用 Skill。触发词：引用缺维、provider 无 key、运行时排名解析、静默改绑、补全 pin 到事务锁定行、Unavailable 不替、Moved 给迁移路径、无 backfill 诚实声明。

## r556A · 默认版本切换只决定「新对象拿哪个版本」：存量按各自已存的版本号解析，且刻意不把旧号重映射到新实现（来源：api.github.com/repos/n8n-io/n8n/issues/40744，2026-10-13 r556A 一手 curl 200 逐串命中 `Makes version 2 the version a user gets when they add a Kafka node or a Kafka Trigger from the nodes panel` / `Version 2 shipped as an opt-in beta on 18 August 2026 ... Version 2 is deliberately not the default until general availability` / `n8n saves typeVersion on every node, and VersionedNodeType.getNodeType() returns the saved version` / `defaultVersion only decides what a new node gets, plus the fallback for a node that carries no typeVersion` / `This deliberately does not remap 1.3 to KafkaTriggerV2, which would move live workflows onto a different library without the user asking`）
- **实证**：Kafka Node / Kafka Trigger 的 `defaultVersion` 由 1→2（触发器由 1.3→2），V2 基于维护中的 `@confluentinc/kafka-javascript`，V1 跑在已不维护的 `kafkajs` 上。原文写明三件「不变」：① 存量工作流不迁移，每个节点上都存了 `typeVersion`，`getNodeType()` 按存的值解析；② 版本 1/1.1/1.2/1.3 保持注册、仍解析到 `KafkaTriggerV1`，既有工作流继续跑旧库；③ **刻意不把 1.3 重映射到 V2**，理由是「会在用户不知情的情况下把线上工作流搬到另一个库上」。`defaultVersion` 只管新节点拿什么，以及**不带 `typeVersion` 的节点**的兜底。beta 期的 hold-back 注释（`Version 2 is deliberately not the default until general availability`）随 GA 一并删除。
- **判据**：① **默认版本是「新建面」的旋钮，不是「存量面」的迁移器**：把两者混为一谈就是经典的静默升级事故——存量对象按自己记录的版本解析，默认值只对**新建对象**与**无版本记录的兜底**生效。② **必须显式声明「不重映射」并给出理由**：不重映射的理由不是懒，是「重映射等于在用户不知情时替他们换实现」；把这条写进发布说明，读者才知道新默认值不会动到老东西。③ **旧版本必须保持注册可解析**：只加新号、不保旧号，等于用默认值掩盖了一次强制迁移；正确形态是新旧并存 + 各自可解析。④ **beta 期要显式 hold-back 默认值并留注释**：把「为什么现在不是默认」写进代码注释，GA 时该注释与 hold-back 一起删除——这样「默认值何时变过」在历史里可查。⑤ **验收要分「新对象」与「存量对象」两条断言**：新加节点/触发器拿到新默认号；已存在 `typeVersion` 的对象解析结果不变；无 `typeVersion` 的走兜底。三条缺一条就等于没验。
- 提升层：工作流（版本默认值与存量解析）/ 工具（发布前新旧并存核对）。触发词：defaultVersion 只管新对象、存量按 typeVersion 解析、刻意不重映射、旧版本保持注册、beta hold-back 默认值、默认值切换 ≠ 静默升级。
- 与既有「增量版本 / 存量自动升级 / 新老行为并存」族分工：那些讲版本号语义，本条讲**默认值的作用面**——同一个「并存」纪律在默认值这个入口上的具体形态（默认值只影响新建面）。


## r557A · 编辑态字段会顺着部署路径泄进持久层与版本控制：同步比较的两侧都要 strip，且「已知无害」字段应从部署面剥离而不是靠调用方自觉（来源：api.github.com/repos/windmill-labs/windmill/issues/11719，2026-10-13 r557A 一手 gh api 200 逐串命中 `parent_version is the low-code app editor's stale-draft base ... It lives on the app value, so every editor deploy persisted it, and wmill sync pull wrote it into app.yaml` / `It shows up as a diff in git-synced files and in version diffs, and was mistaken for the cause of #11717 (it is not)` / `stripEditorState removes it from the pulled app.yaml, from what pushApp deploys, and from both sides of the sync comparison` / `a tracked file that still carries it therefore produces no phantom change and no redeploy` / `No backend strip: the app value is stored as raw JSON, and parsing every app on write to remove one key is not worth it`）
- **实证**：`parent_version` 是低代码 app 编辑器的「过期草稿基线」（打开后别人先部署过时的检测），**只服务于编辑器**。但它挂在 app 值上 ⇒ 每次编辑器部署都把它持久化进已部署实体，`wmill sync pull` 也把它写进 `app.yaml`（进入 git 跟踪文件）⇒ 两个后果：① 每次同步都产生只因该字段变化的 diff，触发**幽灵重部署**；② 排查 #11717 时**误判它是根因**（其实不是）。修法覆盖四处：编辑器部署请求体、草稿部署、CLI `stripEditorState`（pull 出的 yaml / push 的体 / **比较的两侧**）。原文明确不做后端剥离：app 值以裸 JSON 存储，为删一个键而解析每个 app 不划算。
- **判据**：① **编辑态字段与生产态字段必须分面，且「它自己不涨」不代表「它不会变」**：`parent_version` 每次部署都变 ⇒ 判据不是「这个字段内容稳不稳」，而是「这个字段是否只服务于某个界面」。② **部署即持久化 ⇒ 编辑器的内部状态会顺着部署路径进 git**：任何编辑器/客户端专用字段挂在同一个对象上，部署一次就进了同步面 ⇒ 加字段时必须问「它会不会被 sync pull 带走」。③ **同步比较必须两侧都 strip**：只在写入侧 strip，比较侧残留旧值仍会产生 diff ⇒ 校验方式是「比较函数取到的是不是同一条清洗后的路径」，本例明确 `both sides of the sync comparison`。④ **脏文件要能自动消解而非要求用户改**：已跟踪文件里带着该字段时，`no phantom change and no redeploy`，字段在下一次文件被重写时自然消失 ⇒ 兼容性做在读取路径上，不做迁移。⑤ **「已知无害字段造成的 diff」会污染根因判断**：phantom diff 使每次部署看起来都「有变化」，进而把无关字段当根因 ⇒ 版本管理侧要把「字段语义不属于该面」列为独立缺陷类。⑥ 与 §r545B 实例-分支拓扑单向流动、§版本号跨部署面一致性分工：那些管**值跨面一致**，本条管**字段不该跨面存在**——前者是同步什么，后者是不该同步什么。
- 提升层：工作流（部署态与编辑态分面）/ 工具（同步与比较的字段清洗）。触发词：编辑态字段、parent_version、部署持久化、sync pull 写进 yaml、phantom diff、幽灵重部署、比较两侧都 strip、脏文件自动消解、stripEditorState、字段语义不属于该面。

## r557B · 签名 feed 的验签通过不等于可安装：三条件缺一即自签闭环或跨源重放（来源：docs.openclaw.ai/cli/plugins/marketplace.md，2026-10-13 r557B 一手 curl 200 逐串命中 `Public keys must come from a trusted release or operator channel, not from a key endpoint on the feed host` / `OpenClaw verifies the DSSE envelope and, when a profile declares feedId, requires the decoded payload ID to match it` / `The built-in clawhub-public profile always declares its identity, preventing a valid document for another feed from being replayed through that profile` / `existing custom signed profiles that omit feedId retain signature verification without payload-identity binding` / `Use --expected-sha256 <sha256> to require a matching payload checksum` / `the built-in profile does not grant signed-feed install authority`）
- **实证**：OpenClaw 的托管 feed 刷新会保存快照，`refresh` 接受 `--expected-sha256` 要求新鲜载荷匹配钉死的校验和。签名 profile 侧三件事同时成立：① **公钥来源分离**——「公钥必须来自可信的发布或运维渠道，**不能取自 feed 主机自己的 key endpoint**」；② **payload identity 绑定**——验 DSSE 封套后，若 profile 声明了 `feedId` 则要求解码出的载荷 ID 与之匹配，内置 `clawhub-public` 恒声明自身身份，**防止「对另一个 feed 合法的有效文档」被重放进本 profile**；③ **过渡期不对称**——旧的自定义签名 profile 若省略 `feedId`，仍保留验签但**没有身份绑定**；内置 profile 在 ClawHub 交出生产公钥之前**不授予 signed-feed 安装权**。
- **判据**：① **「验签通过」不等于「这份内容属于这个源」**：签名只证明「某把钥匙签过」，不证明「签的是这个 feed 的内容」⇒ 必须有第二维身份绑定（payload ID == profile 声明的 feedId），否则任何一份被合法签过的旧文档都能被重放。② **钥匙与被签物不得同源**：公钥从 feed host 的 key endpoint 取 ⇒ 攻破 host 即可自签任意内容，验签链退化为自签闭环 ⇒ 公钥的信任锚必须是**带外**的发布/运维渠道。③ **过渡期的宽松配置要显式登记为风险**：省略 `feedId` 仍可验签，说明兼容路径存在 ⇒ 审查时把「哪些 profile 缺身份绑定」列成清单，而不是记一句「已验签」。④ **权限授予可以与机制上线解耦**：机制先上、安装权后授（`does not grant signed-feed install authority`）⇒ 「有验签能力」与「可安装」是两个状态，验收要分别断言。⑤ **钉校验和是可选的第四层**：未钉时可回退 bundled/快照（可用性优先），钉后不匹配即失败（一致性优先）⇒ 钉不钉要按场景显式决策，不能默认。⑥ 与 §签名密钥只可用不可读（r551B，ssc）分工：那条管**签名私钥的托管面**，本条管**签名结果的消费面**（这份签名能不能用来安装）；与 §目录级 detached 签名 / OMS 链分工：那些管制品未被改，本条管**制品的归属源**。
- 提升层：工作流（供应链信任）/ 工具（签名与发布源绑定）。触发词：签名 feed、feedId、payload identity、跨 feed 重放、公钥不得取自 feed host、自签闭环、带外信任锚、expected-sha256 钉校验和、过渡期无身份绑定、安装权与验签能力分离。

## r557C · 依赖冲突的修法是「取最小放宽量 + 在约束旁记录理由 + 上界不触破坏性变更」，不是直接删 pin；验收落在解析器干跑（来源：api.github.com/repos/zenml-io/zenml/issues/5341，2026-10-13 r557C 一手 gh api 200 逐串命中 `The LangChain integration pinned langchain==0.3.0 (September 2024). That release requires tenacity<9, so the combined integration environment that fast CI installs cannot be resolved as soon as any other integration needs tenacity 9. This currently blocks #5312` / `This PR relaxes the pin to langchain>=0.3.5,<1.0` / `0.3.5 is the first release that lifted the tenacity<9 pin (it allows <10; 0.3.20 dropped the constraint altogether)` / `<1.0 because LangChain 1.0 removed the langchain.vectorstores and langchain.docstore import paths that the materializers use. Moving to 1.x would need import rewrites and is a separate change` / `The reason is recorded in a comment next to the requirement` / `Resolver dry run (uv pip compile) of the exact fast-CI combined integration list ... resolves cleanly to langchain==0.3.30 ... The same list fails to resolve with langchain==0.3.0`）
- **实证**：LangChain 集成把 `langchain==0.3.0` 钉死（2024-09），而该版本要求 `tenacity<9` ⇒ 任何其他集成需要 tenacity 9 时，fast-CI 装的合并集成环境**解析不出来**，直接阻塞 #5312（typesafe-sdk 要求 `tenacity>=9`）。修法把 pin 放宽到 `>=0.3.5,<1.0`，并逐条给出边界理由：`0.3.5` 是第一个解除 `tenacity<9` 的版本（它允许 `<10`，`0.3.20` 完全去掉该约束）；**上界 `<1.0`** 因为 LangChain 1.0 移除了 materializers 依赖的 `langchain.vectorstores` / `langchain.docstore` 导入路径，迁移到 1.x 需要改写导入、属独立变更。理由**写在约束旁边的注释里**。验收是**解析器干跑**（`uv pip compile`）跑 fast-CI 的确切合并清单：新范围加 `typesafe-sdk>=0.7.1` 干净解析到 `langchain==0.3.30` / `langchain-community==0.3.31` / `tenancy==9.1.4`，同一清单在 `==0.3.0` 下解析失败；另在 Python 3.11 venv 上三个 LangChain materializer 测试通过。
- **判据**：① **冲突修法是「放宽到刚好够」而不是「删掉约束」**：上界 1.0 不因冲突而删除，而是由**独立且已识别的不兼容**（导入路径移除）决定 ⇒ 每条约束要么被证据解除，要么带着理由收窄，禁止无理由删除。② **下界取「第一个解除冲突的版本」，上界取「下一个已知破坏面」**：0.3.5 是首个让位版本，1.0 是首个移除所需 API 的版本 ⇒ 一个范围的两个端点各有各的取证来源，写不出这个来源就说明是拍的。③ **理由必须与约束同处一地（写在旁边）**：原文 `The reason is recorded in a comment next to the requirement` ⇒ 否则半年后没人知道这个上界为什么不是 1.1。④ **验收是解析器干跑，不是安装成功**：干跑能在写盘前证明**合并清单**可解析；只在自己那一个集成里装成功 ≠ 合并环境能解析，而阻塞恰恰发生在合并面。⑤ **旧约束下的失败也要断言**：原文明确「同一清单在 `==0.3.0` 下失败」⇒ 修复类 PR 的测试要能说明「若不修会怎样」，否则无法区分真修复与偶然通过。⑥ **能用旧形态就别做破坏性改写**：1.0 需要导入重写，本轮明确划为独立变更 ⇒ 依赖升级的最小单位是「解除阻塞」，跨大版本的迁移另立项。
- 提升层：工作流（依赖治理）/ 工具（约束求解与验收）。触发词：pin 冲突、最小放宽量、上界由已知破坏面定、tenacity<9、导入路径移除、理由写在约束旁、解析器干跑 uv pip compile、合并集成清单、旧约束下失败断言、迁移另立项。
- 与 §兼容闸门按「谁更可能是错的一方」分向分工：那条管**运行时版本兼容判定**，本条管**构建期约束求解**——同一个版本问题，一个在运行、一个在解析。

## r558A · 自动迁移必须 fail-closed：仅在无损时才执行，不能精确映射则抛错、原件保持不变并逐节点列出例外条件（来源：api.github.com/repos/n8n-io/n8n/issues/40877，2026-10-13 r558A 一手 gh api 200 逐串命中 `A migration runs only when it is lossless. Every parameter maps, runtime behavior stays the same, and the result still runs on 1.x and 2.x. If a node has a configuration that does not map exactly, the migration throws. The workflow stays unchanged, and the report shows the reason` / `Cron -> Schedule Trigger 1.4: Exceptions (the migration throws when) There are no trigger times. Two trigger times are identical. A value is an expression or out of range` / `The PR also groups all node-removal migrations under migrations/node-removals/`）
- **实证**：n8n 为被移除节点做「一键迁移」，原则写在正文里：**只有无损才执行**——每个参数都能映射、运行行为不变、结果在 1.x 与 2.x 都能跑；只要某项配置**不能精确映射就抛错**，工作流**原样不动**，报告给出原因。并且逐节点列出「什么情况会抛错」，例如 Cron→Schedule Trigger 在「没有任何触发时间 / 两个触发时间相同 / 值是表达式或越界（如每 60 分钟、每 24 小时）/ 模式未知」时抛错。所有节点移除迁移统一归档到 `migrations/node-removals/`。
- **判据**：① **自动改写必须声明「无损」的具体含义**，而不是声称等价：本文把无损定义为「参数逐一映射 + 行为不变 + 双版本可跑」三条 ⇒ 设计自动迁移/自动升级时，把这三个条件写成可判定的判据，不能写「尽量保留」。② **不能精确映射就中止，且中止要可见**：抛错 + 原件不变 + 报告列原因，是 fail-closed 的最小三件套；静默跳过会让用户在不知情下拿到半迁移的工作流。③ **例外条件必须逐字段枚举，并覆盖「表达式化」这类逃逸口**：本例多次点名 `is an expression`——用户把常量改成表达式后，迁移的精确映射前提就不再成立 ⇒ 凡是「按值做映射」的迁移，都必须先判断该值是否为表达式。④ **迁移产物要同时在旧新两个版本上可运行**才算通过，否则「迁移」只是把问题推给下一次升级。⑤ **迁移族要集中归档到一个目录**，便于按「移除节点」这一维度统一审计哪些迁移存在、哪些会抛错。
- 提升层：工作流（迁移与升级）/ 工具（自动改写的无损门）。触发词：自动迁移 fail-closed、仅无损时执行、不能精确映射就抛错、原件不变、例外条件逐字段枚举、表达式化逃逸、双版本可运行、迁移族集中归档。

## r558A · 对外副作用的记账以「已发出」为准：发信成功后标记失败仍计为已通知，重发即提醒并刷新时间（来源：api.github.com/repos/n8n-io/n8n/issues/40952 + /40949，2026-10-13 r558A 一手 gh api 200 逐串命中 `A finding is marked notified with a notifiedAt only after its owner's email went out, so a repeated call is a reminder that bumps the date` / `A failed database mark after a sent email is logged and the workflow still counts as notified, so nobody re-sends the email` / `The response names the notified workflows and the skipped ones with a reason: no_owner, no_finding or send_failed` / `The endpoint returns 400 when SMTP is not set up` / `One email per owner lists all of their selected workflows` / `The state select is disabled while a notification is in flight, so a pending email cannot overwrite a newer state`）
- **实证**：n8n 的「通知工作流负责人」端点在**邮件真正发出之后**才把 finding 标记为 `notified` 并记 `notifiedAt` ⇒ 重复调用被设计成**提醒**并刷新该时间。若邮件已发出但随后的数据库标记失败，只记日志，该工作流**仍计为已通知**，以免有人重发邮件。响应显式区分已通知与被跳过，跳过原因枚举 `no_owner` / `no_finding` / `send_failed`；未配置 SMTP 直接返回 400。UI 侧：通知在途时状态下拉禁用，避免一封在途邮件覆盖更新的状态。
- **判据**：① **对外副作用的「完成」判据是副作用发生，不是本地记账成功**：先发信后标记的架构里，标记失败必须按「已发生」处理，否则重试会重复触达外部收件人 ⇒ 凡「发消息/发邮件/下单/建工单」类动作，都要把「记录失败但已发生」写成显式分支。② **重复调用要定义成幂等的提醒而非错误**：同一请求再次进来应刷新时间戳并重复告知，不报错也不静默跳过 ⇒ 与 dl 既有幂等纪律同族（跑第二遍世界不变），本条补的是**面向人的重复触达**语义。③ **跳过必须带原因枚举**：`no_owner` / `no_finding` / `send_failed` 三态让「没通知到」与「通知到了」在同一响应里可分辨；只回一个布尔值会把部分成功压成全失败。④ **前置依赖缺失要在入口硬失败**：无 SMTP 时返回 400，而不是排队等一个永远不会到的发送。⑤ **在途状态不可被更旧的写入覆盖**：通知在途时禁用状态变更 ⇒ 异步副作用与状态机并发时，须有「在途保护」而非依赖时序恰好正确。
- 提升层：工作流（对外副作用记账与幂等）/ 工具（通知类端点语义）。触发词：以副作用为准记账、发信后标记失败仍计已通知、重复调用即提醒、跳过原因枚举、无 SMTP 返 400、在途保护。

## r558B · 模型请求参数的能力假设按「家族 × 版本」维护：关闭型优化在新家族上从优化变成阻断（旧参数可能整体不被支持）（来源：api.github.com/repos/activepieces/activepieces/issues/16451，2026-10-13 r558B 一手 gh api 200 逐串命中 `Agent runs and chat turns on a customer's own Anthropic or Bedrock key failed on their first step with Claude Opus 5.5 ("thinking.type.disabled" is not supported for this model). We sent thinking: disabled for the first step and the discovery phase, and enabled with a budget afterwards. The adaptive-only models (Opus 4.7 and newer, Sonnet 5, Haiku 5.5, Fable) reject both` / `buildProviderOptions now sends adaptive thinking to those models, at low effort where we used to switch thinking off. Older models keep the current behaviour` / `Production: 15 failed EXECUTE_AGENT_RUN jobs on 2026-10-12 across 2 platforms, all claude-opus-5-5 on a direct Anthropic key` / `No live call against Opus 5.5 yet`）
- **实证**：客户自有 Anthropic / Bedrock key 上用 Claude Opus 5.5 的 agent 运行，**第一步就失败**，报错 `thinking.type.disabled is not supported for this model`。做法此前是：首步与 discovery 阶段发 `thinking: disabled`，其后发 `enabled` + budget；而**只支持 adaptive 的家族（Opus 4.7 及更新、Sonnet 5、Haiku 5.5、Fable）两种都不接受**。修法：`buildProviderOptions` 对这些模型改发 adaptive thinking、并在我们原先「关掉推理」的位置给 `low` effort，旧模型保持原行为。生产证据：2026-10-12 单日 15 个 `EXECUTE_AGENT_RUN` job 失败、跨 2 个平台，全部 `claude-opus-5-5`。原文诚实边界：**尚未对 Opus 5.5 做实调验证**。
- **判据**：① **「关掉某能力」不是单调安全的优化，它可能在新版本上变成阻断**：我们把 `thinking: disabled` 当作省成本/省延迟的手段，而新型号直接拒绝这个参数 ⇒ 参数取值必须按**能力矩阵**而非全局默认值下发；出现「参数不被支持」类报错时，先查是不是某个家族的新型号。② **降级路径要跟着家族矩阵走，而不是留在旧默认值上**：修法不是「关掉」也不是「开着」，而是换一种**该家族支持的表达**（adaptive + `low` effort）来达成同样的省算力目的 ⇒ 优化项与兼容项在实现上要分开声明，避免一处改动连带失效。③ **兼容矩阵的粒度是「家族 × 版本」不是「厂商」**：原文列的是具体家族名单（Opus 4.7+ / Sonnet 5 / Haiku 5.5 / Fable），旧模型保持不变 ⇒ 验收要覆盖「矩阵内每一族都发对参数」和「矩阵外仍走原路径」两侧，不能只测一个代表模型。④ **首步失败具有放大效应**：失败发生在第一步 discovery 阶段 ⇒ 表现为「整批作业全灭」而非「某个功能不可用」，监控要能识别这种「同型号批量同错」形态。⑤ **未做实调验证的兼容修复必须标注**：原文自陈无 live call ⇒ 登记为「已按错误信息修复、待真实调用复验」，不得当作已验证能力写进台账。与 §依赖冲突取最小放宽量（r557C，rm）分工：那条管**构建期包版本约束**，本条管**运行时模型请求参数的家族能力**——两者都是「版本推进会让既有假设失效」，一个在解析、一个在请求体。
- 提升层：工作流（模型请求参数治理）/ 工具（能力矩阵与降级路径）。触发词：参数不被支持、thinking.type.disabled、adaptive-only 家族、能力矩阵按家族×版本、降级路径随矩阵更新、关闭型优化变阻断、首步失败批量放大、未实调须标注待复验。

## r559A · schema 变更的兼容窗口 = 活跃进程里已缓存计划的寿命，须「自愈 + 迁移期不改类型 + 版本门控延迟生效」三段一起做（来源：windmill-labs/windmill #11737，2026-10-14 r559A 一手 gh api 200 逐串命中 `cached plan must not change result type` / `OVERRIDDEN_MIGRATIONS` / `before_acquire` / `MIN_VERSION_SUPPORTS_AEAD_SECRETS`）
- **实证**：迁移 `20261012213357_widen_variable_value`（1.831）把 `variable.value` 从 `VARCHAR(15000)` 改成 `VARCHAR(15040)`。Postgres 把 varchar 长度变化**当作结果类型变化**，于是**每个活跃进程早已 prepared 的语句在此列上全部失败**（`cached plan must not change result type`），直到该连接关闭。sqlx 按池连接保存 prepared statement，服务端连接池寿命最长 30 分钟 ⇒ 滚动升级期间**上一版本的服务器持续读变量/资源失败**，最长半小时。修法三段：① **自愈**：进程遇到的第一个 stale-cached-plan 错误即通过连接池的 `before_acquire` 退役该错误之前开启的全部池连接，代价从「最长 30 分钟失败」降为「每个进程约一次失败查询」；② **迁移时刻不改类型**：尚未迁移的库通过 `OVERRIDDEN_MIGRATIONS` 覆写为**只加 CHECK 约束**，迁移文件与其校验和不变 ⇒ 已迁移的库完全不受影响；③ **延迟加宽**：由 server monitor 在 `MIN_VERSION_SUPPORTS_AEAD_SECRETS`（1.832，即本修复所在版本 ⇒ 此时全部活跃 worker 都已具备自愈能力）满足**且**该条件持续成立后才真正改列类型。
- **判据**：① **schema 变更的爆炸半径要按「活跃进程里已缓存的东西」计算，不是按「迁移脚本跑了多久」**：本例的失败窗口 = 连接池寿命（30 分钟），远长于迁移本身 ⇒ 评估任何类型/约束变更前，先问「谁已经把旧形状缓存住了、缓存多久」。② **兼容窗口的实现顺序是固定的**：先给旧版本装上自愈能力 → 再让迁移期不改变实际类型（只加可在旧版上成立的约束） → 最后等「全部活跃实例都带自愈」的版本门槛满足才真正变更。**顺序颠倒（先改类型再指望自愈）会正好落在没有自愈能力的一批实例上**。③ **版本门槛是延迟生效的开关而不是提示**：`MIN_VERSION_*` 判断的是「存量实例是否已具备承受该变更的能力」⇒ 凡不可逆的结构变更都应挂这样一个门槛，而不是假定滚动升级瞬间完成。④ **覆写迁移要保住文件名与校验和**：`OVERRIDDEN_MIGRATIONS` 只改实际执行的 SQL，文件与校验和不变 ⇒ 已执行过的库不会被认成「迁移不一致」；**改迁移文件本身会让历史库的校验失败**。⑤ **自愈的代价必须明码标价并优于原故障**：一次失败查询换掉 30 分钟不可用是可接受的取舍，但必须写清「每个进程仍会失败一次」⇒ 不要把自愈包装成零影响。
- 提升层：工作流（滚动升级与 schema 演进）/ 工具（连接池与 prepared statement 缓存）。触发词：cached plan must not change result type、列类型加宽、连接池寿命即失败窗口、before_acquire 退役连接、OVERRIDDEN_MIGRATIONS、迁移期只加约束、MIN_VERSION 门槛延迟生效、校验和不变。

## r560A · 「已发布」不等于「已生效」：发布写入被存储层约束静默拒绝时，指针先更新、数据后失败，结果是无限期继续服务旧版本（来源：api.github.com/repos/n8n-io/n8n/issues/40606，修复 PR #41007 `Accept trigger node ids longer than 36 characters on Postgres`；2026-10-14 r560A 一手 gh api 200 逐串命中 `varchar(36)` / `value too long for type character varying(36)` / `the editor shows the new version as active (activeVersionId is updated), but webhooks keep being served by the previously published version indefinitely` / `Nothing is surfaced in the UI`）
- **实证**：`workflow_publication_trigger_status."nodeId"` 是 `varchar(36)`，而 node id 在别处**没有任何 36 字符约束**——经 public API 或 source control 导入的工作流可带 37–54 字符的 node id（报告方有 14 条这样的活跃工作流）。发布时为该节点写触发状态，Postgres 以 `value too long for type character varying(36)` 拒绝写入；但编辑器侧 `activeVersionId` 已更新并把新版本显示为 active ⇒ **webhook 无限期地继续由上一个已发布版本服务**，UI 不报任何东西，只有服务器日志一行。
- **判据**：① **「已发布」与「已生效」是两个状态，必须分别可观测**：写入被存储层拒绝时，发布这个动作要整体失败并回退已推进的指针，绝不能「指针先走、数据后失败」。② **存储层约束（列宽/类型/取值域）是发布面的一部分**——凡 schema 有约束的字段，写入前要有与之一致的上游校验，否则约束只能在运行时以「静默拒绝」的形式出现。③ **跨面 id 的长度约束必须同源声明**：别处无约束、此处 `varchar(36)` 本身就是契约分裂，导入/API 通道绕过了编辑器侧的隐式限制。④ 长期后果是「服务旧版本」而不是「报错」⇒ 需要有对账手段（发布版本号 vs 实际服务版本号）才能发现，不能依赖用户察觉。
- 提升层：工作流（发布与生效对账）/ 工具（存储约束前移校验）。触发词：发布静默失败、仍服务旧版本、activeVersionId 已更新但不生效、varchar 列宽拒绝发布、已发布≠已生效、约束不同源、导入通道绕过编辑器限制。

## r561A · 第三方依赖的内置默认值会压过平台自己的可配置项：双重限流取交集时，不可配的那一层才是实际上限（来源：api.github.com/repos/n8n-io/n8n/issues/40539 `N8N_OAUTH_SERVER_*_RATE_LIMIT is capped by hardcoded MCP SDK rate limits`，2026-10-14 r561A 一手 gh api 200 逐串命中）
- **实证**：`oauth.controller.ts` 挂载 MCP SDK 的 handlers 时**没有传 `rateLimit` 选项**；只要该选项不是 `false`，SDK 就会自己加一层 `express-rate-limit`（按 IP、内存态、每个主实例各算一份：authorize 100/15min、token 50/15min、revoke 50/15min、register 20/1h）。n8n 同时把自有的可配 `ipRateLimit` 用在相同路由上 ⇒ **每个请求必须连过两道闸门**，SDK 的硬编码值成为 `N8N_OAUTH_SERVER_*_RATE_LIMIT` 的实际天花板，默认值下即已生效。
- **判据**：① **限流叠加取交集而不是取配置值**：引入依赖自带的限制等于新增一条独立阻塞来源，把自己那层调到很大不会有任何效果。② **依赖的「默认行为」必须显式关闭或显式确认**——不传参不等于不生效，常常等于启用其内置的保守默认。③ 升级依赖可能悄悄改配额：这类上限不在自己的配置文件里，只在被依赖方的源码里 ⇒ 依赖升级的验收清单要包含「被依赖方是否自带限额/超时/重试」。④ 内存态、按实例的计数意味着**实际阈值随副本数放大**，容量评估不能用单实例数值外推。⑤ 与既有「多标签叠加是交集」分工：那条管**自有配置的组合语义**，本条管**自有配置被依赖方默认值覆盖**——后者更隐蔽，因为配置项存在、可调、看起来生效。
- 提升层：工具（限流与容量）/ 工作流（依赖升级验收）。触发词：限流被 SDK 默认值压过、双重限流取交集、不传参即启用内置默认、依赖自带限额、按实例内存计数、调大配置无效。

## r561A · 「键不存在」与「键为空/为默认值」是两种状态，只支持后者的更新接口让精确还原不可能（来源：api.github.com/repos/n8n-io/n8n/issues/40549 `Workflow settings cannot unset callerIds after workflowsFromAList; exact restore is impossible`，2026-10-14 r561A 一手 gh api 200 逐串命中）
- **实证**：工作流临时改为 `callerPolicy = workflowsFromAList` + `callerIds = DISPOSABLE_CALLER_EXACT` 之后，没有任何受支持的设置更新路径能把原始配置还原到**`callerIds` 键完全不存在**的状态；还原 `callerPolicy = none` 能正确阻断子工作流调用（不是越权问题），但 `callerIds` 的旧值会残留 ⇒ 使用「变更前快照 + 变更后原始设置逐字节比对」的一方无法完成精确回滚。
- **判据**：① **可逆性必须到键级，不只是值级**：能改回语义等价的配置 ≠ 能还原到变更前的表示；凡以原始表示做对账/审计/漂移检测的系统，前者不合格。② **更新接口要同时支持 set / unset / reset-to-absent 三种意图**，只提供 set 的接口会把「删除一个键」变成不可能操作。③ **迁移与临时授权类变更要先落快照并验证可还原**，尤其是「临时放开再收回」这类操作——放开容易，收回留残值等于把一次性的授权固化进配置。④ 残留键位在语义上无害但在**合规与对账**上有害，验收标准要写明哪一类使用者会因此失败。
- 提升层：工作流（变更可逆与状态还原）/ 工具（配置接口完备性）。触发词：无法 unset、精确还原不可能、键缺失 vs 空值、配置漂移对账、临时授权收回留残值、快照回滚失败。

## r561A · 编译期常量的默认值无法演进：要能分批改版本，默认值必须先落成每条记录上的具名值（来源：api.github.com/repos/windmill-labs/windmill/pulls/11656 `record each instance's python version and start new ones on 3.13`，2026-10-14 r561A 一手 gh api 200 逐串命中）
- **实证**：Python 版本在实例未显式指定时走的是**编译期常量**——对每一个从未碰过「Instance Python Version」的实例都是同一个值，把它调高就会**一次性移动全部存量实例**，因此实际上永远不能调。修复：服务端在实例没有该值时写入一个具体值（刚建库写入 3.13，其他既有库冻结在 3.12）⇒ 存量继续跑 3.12，新建实例走 3.13，以后再推进只需改一个常量（`PyVAlias::NEW_INSTANCE`）。新实例选 3.13 而非更新版本有实证理由：3.15 对 100 个常用原生包中的 24 个缺 wheel，3.14 改变了既有脚本依赖的运行时行为。
- **判据**：① **「没配置」如果解析成一个共享常量，那个常量就成了全体绑定**：演进它等于一次性迁移，结果是事实上的冻结。② 要让默认值可演进，必须在首次可判定时把它**物化成记录上的具名值**（backfill），此后存量与新量的默认值才能分叉。③ **新建走新值、存量冻结在旧值**是唯一安全的默认演进形状；「统一升级」看似干净，实际是把风险集中到一次不可回滚的切换上。④ 版本选择要有**外部生态的实证依据**（wheel 覆盖率、运行时行为变更），而不是「越新越好」。⑤ 与既有「schema 兼容窗口 = 活跃进程缓存寿命」分工：那条管**类型变更的在线窗口**，本条管**默认值本身的演进路径**——两者都说明「隐式共享状态」是演进的主要障碍。
- 提升层：工作流（默认演进与 backfill）/ 工具（运行时版本治理）。触发词：编译期常量默认值、默认值无法演进、物化默认值、新建走新值存量冻结、wheel 覆盖率、PyVAlias::NEW_INSTANCE、一次性迁移风险。

## r561B · 关停没有排空期：应用一进关闭流程就对在途回调回裸 503，被依赖方会把这当成自己的故障（来源：api.github.com/repos/activepieces/activepieces/issues/16218 `[BUG] API shutdown refuses in-flight engine callbacks with a bare 503 (no drain)`，2026-10-14 r561B 一手 gh api 200 逐串命中）
- **实证**：`SIGTERM/SIGINT → stop()` 期间，`app.close()` 进行中 Fastify 的 `kState.closing === true` 会对**所有**请求返回固定的 80 字节体 `{"error":"Service Unavailable","message":"Service Unavailable","statusCode":503}`——没有 `Retry-After`、没有 drain 期、没有区分在途与新请求。凡使用 `context.server.apiUrl` 回连本服务 API 的 piece（Tables 的 `convertTableExternalIdToId`、Store、Call Flow、Human Input…）都会在每次重启时失败，run 终态 FAILED，UI 把责任指向 piece 本身（0.91.1 自托管 K8s，Pylon 6209）。
- **判据**：① **关闭是一个有中间态的过程，不是一个瞬间**：`closing` 期间仍要能完成已经收下的请求，尤其是来自自身执行体的回调；一口回绝会把「平台在重启」伪装成「用户的 piece 坏了」。② **关停响应必须可区分**：给 `Retry-After`、给明确错误码/语义，让调用方知道可重试而不是判为永久失败；裸 503 是最容易被误读的形态。③ **排空顺序要显式定义**：先摘流量（ readiness false / 从 LB 摘除）→ 等待在途完成或超时 → 再 `close()`；滚动重启下这一步决定每次发布是否产生一批假失败。④ **诊断信息要指向真正的责任方**：错误里不带「本服务正在关闭」的事实，排障时间就浪费在被误指的组件上。⑤ 与既有「周期性回收须豁免在途」（r560C，langflow #15712）分工：那条管**运行期回收任务**的在途豁免，本条管**进程级关停**的排空期与响应语义——同一原则的两个层次。
- 提升层：工具（服务生命周期与优雅关停）/ 工作流（滚动发布与重启安全）。触发词：裸 503、no drain、kState.closing、SIGTERM 打在途回调、Retry-After、摘流量再 close、重启产生假失败、piece 被误指。

## r562A · 锁必须与它协调的操作同源定义——key 与超时从被协调方导出并共用，各写一份常量就等于给「锁形同虚设」留缝（来源：api.github.com/repos/activepieces/activepieces/issues/16469，2026-10-14 r562A 一手 gh api 200 逐串命中 `rollback coordination lock` / `backgroundMigrationLockKey(name)` / `BACKGROUND_MIGRATION_LOCK_TIMEOUT_SECONDS` / `distributedLock.runExclusive`）
- **实证**：阻塞迁移的 `down()` 若触碰后台迁移正在处理的表/索引/列，会与另一 pod 上仍在运行的 runner 并发执行冲突 DDL（滚动回滚场景下：老版本 pod 还在消费 BullMQ，新版本 pod 已在跑 `down()`）。runner 持有按迁移名键控的 Redis 分布式锁，但 `rollback-migrations.ts` **无法与之协调**。以 #14888 的 `ReshapeFlowRunListIndexesForBarrierChildren` 为例，三种后果：reshape 在 `down()` 删掉 `idx_new_1` 之后刚把它建完 → **幽灵索引**；`down()` 恢复 `idx_old_1` 后 reshape 又把它删掉 → **缺失索引**；reshape 仍在引用某列构建索引时该列被 drop → 一侧报错。修法不是"提醒调用方小心"，而是**把 runner 的锁暴露为共享原语**：`backgroundMigrationLockKey(name)` 与 `BACKGROUND_MIGRATION_LOCK_TIMEOUT_SECONDS` 提升为 runner 上的导出常量（runner 自身也用这两个常量，key 与 timeout 无法漂移），再提供 `migrationHelpers.withBackgroundMigrationLock({ log, migration, fn })` 包住 `distributedLock.runExclusive`，用同名 key 与 240s 超时；该迁移在途则等 `runOne` 返回后再执行 `fn`，空闲则立即获取。
- **判据**：① **锁的定义必须与被锁的操作同源**：key 与 timeout 由被协调方导出、双方引用同一常量；"两边各写一份看起来一样的字符串"是最典型的伪锁——一旦某侧改动，锁的就是另一把锁，且没有任何报错。② **异步后台任务与同步 schema 回滚是同一资源的两个写者**，滚动发布/回滚期间必然共存 ⇒ 迁移框架必须提供"等待在途后台任务"的原语，只给"启动 + 状态查询"是不够的。③ **并发 DDL 的失败形态是静默的结构损坏**：幽灵索引/缺失索引都不抛错，只是索引集与代码假设不一致，直到某次查询计划劣化或被下一个迁移撞上才暴露 ⇒ 迁移验收要核对索引与列的**最终集合**，而不是只看迁移有没有报错。④ **修复要落在共享契约而非调用纪律**：把 key/timeout 提升为导出常量，让"用错锁"在引用层面不可表达；靠文档要求调用方自己拼 key 必然漂移。⑤ 与既有「schema 兼容窗口 = 活跃进程缓存寿命 / 迁移期只加 CHECK / MIN_VERSION 门槛」（rm 1.136，windmill #11737）分工：那条管**运行期 schema 兼容窗口**，本条管**迁移执行期的互斥**——发布安全的两个不同阶段，前者是"新旧共存时谁读谁写合法"，后者是"同一时刻只能有一个写者在改结构"。
- 提升层：工具（迁移与分布式锁原语）/ 工作流（滚动发布与回滚安全）。触发词：rollback coordination lock、backgroundMigrationLockKey、runExclusive 超时常量、幽灵索引、缺失索引、并发 DDL、锁 key 漂移、等待在途后台迁移。
## r562A · 协议演进的兼容单位是「首包字节」——新增可选参数必须让缺省场景保持与原请求完全一致，且分页终止条件不能只信任对端（来源：api.github.com/repos/langgenius/dify/issues/43867，2026-10-14 r562A 一手 gh api 200 逐串命中 `follow pagination in MCP tools/list` / `nextCursor` / `request params stay off the wire entirely when no cursor is passed` / `stop if the server echoes back a cursor we already saw`）
- **实证**：`MCPClient.list_tools()` 只发一次 `tools/list` 请求并返回第一页，后续页的工具被**静默丢弃**（#43841）。修法：ClientSession 的四个 `list_*` 方法接受可选 cursor，且**无 cursor 时请求参数完全不上线**，使已存在的服务端看到的首页请求与此前**逐字节相同**；`MCPClient.list_tools()` 跟随 `nextCursor` 到耗尽；再加一道"重复 cursor 保护"——若服务端回吐已见过的 cursor 就停止，否则会永久自旋（作者自陈该保护并非确定项，替代方案是信任服务端直到 `nextCursor` 为 null，但一个坏服务端就会挂住每一次工具同步）。
- **判据**：① **向后兼容的度量单位是线上的首包字节，不是字段名的语义**：新增可选参数时，"不传"分支必须产出与原请求完全一致的请求体（缺省参数不上线）；只在代码里"默认 None"但序列化时仍带 `params: {}` 或 `cursor: null`，对严格服务端就是行为变更。② **对端驱动的循环必须自带终止保护**：分页/流式这类由对端告知"还有下一页"的协议，要在客户端维护已见游标集合；"信任对端直到它说停"与"被一个坏对端挂死"之间要显式选边并把理由写进代码注释（本例选择了可用性优先）。③ **截断型缺陷的后果是能力静默缺失**：少拉一页等于工具集不全，而上层无法区分"工具不存在"与"工具没被拉到" ⇒ 列举类接口应返回"拉取了 N 页 / 游标是否耗尽"的可观测信息。④ 与既有「枚举面静默截断的代价是动作重复」（av 2.268，activepieces #16327）分工：那条管**枚举动作**的翻页终止与 upsert 幂等，本条管**协议层**分页语义与演进时的字节级兼容约束——同一失效模式的两个层次。
- 提升层：工具（协议客户端与分页语义）/ 工作流（接口演进的兼容性验收）。触发词：nextCursor、缺省参数不上线、首包字节兼容、重复 cursor 保护、trust the server 取舍、分页截断丢工具、list_tools 只取首页。

## r562C · 对比型校验必须跑在生产那条完整路径上——只跑一半迁移的校验环境，会把正确实现判成「schema 漂移」（来源：api.github.com/repos/activepieces/activepieces/pulls/16439，2026-10-14 r562C 一手 gh api 200 逐串命中 `build the background track before the schema drift check` / `runs only getMigrations()` / `20 spurious CREATE/DROP INDEX statements` / `a crashed migration was reported as schema drift`）
- **实证**：一旦某个后台迁移会构建实体声明的索引，`check-migrations` 就必然失败，这直接阻塞了把 #14888 的 `flow_run` 索引 reshape 移出启动路径的首次真实使用。原因：校验脚本用 `typeorm migration:run` 建库，而它**只跑 `getMigrations()`（阻塞迁移）**；生产路径是 `runMigrationsWithCatchup` **再跑全部后台迁移**；漂移检查于是拿"仅含阻塞迁移的 schema"去比实体，把后台迁移建的每一个索引都报成缺失——在新 `HOME`（CI 不缓存 `~/.activepieces`）上复现：拆分后的 #14888 报出 **20 条虚假的 CREATE/DROP INDEX**，未拆分的同一 commit 通过。修法：新增 `src/migrate.ts`（仿 `src/rollback.ts`）依次跑 `runMigrationsWithCatchup` → `backgroundMigrationRunner.run` → `destroy()`，且与启动路径**共用同一个 `distributedLock`**，使 CLI 拿到真实 runner（真实的 `background_migrations` 行、受保护的阻塞迁移照启动时那样 catch up）；并以 `process.exit` 收尾——因为内存 Redis 的锁会启动 `redis-memory-server`，其连接让事件循环在迁移结束后仍存活，不显式退出则 `main()` 已 resolve 而该步骤永不结束（其 killer 进程会在父进程消失后停掉 `redis-server`）。同时 `check-migrations` 改为运行 `migrate.ts` 且输出可见，**只有漂移这一步打印 "Schema changes detected"**——在此之前，一次迁移崩溃会被报成 schema 漂移；`db-migration` 也先跑 `migrate.ts`，使生成的迁移与**完整 schema** 对比，不会重建后台迁移已建的索引。
- **判据**：① **校验工具必须走与生产完全一致的执行路径**：只跑一半迁移的校验环境，其"漂移"结论是环境伪影（20 条虚假语句）⇒ 凡对比型校验（schema drift、golden file、契约对照），先问"被对比的两侧在这个环境里是否都被完整生成过"。② **后台/异步产物的结构必须在校验环境中被真实产出**，否则基线天然缺一块，正确实现被判为漂移 ⇒ 引入后台迁移就等于给所有 schema 校验工具加一条"必须先跑完后台轨道"的前置。③ **崩溃与漂移必须是两类出口**：迁移一崩就报成漂移，会把人引向改 schema 而不是修崩溃 ⇒ 校验流水线要把"前置步骤失败"与"对比结果不一致"分开成两个错误类别与两条提示。④ **脚本化入口要显式管理进程生命周期**：锁/连接/内存服务会持有事件循环，脚本必须以显式退出收尾**并把理由写进注释**（本例交代了 redis-memory-server 的行为与其 killer 的善后）。⑤ 与既有「锁必须与它协调的操作同源」（rm 1.140.0，ap #16469）同源于同一批 PR：那条管**运行期互斥**，本条管**校验期路径一致**——同一个后台迁移机制引入的两类风险，缺一都会在 CI 或回滚时以假故障形态出现。
- 提升层：工具（迁移与 schema 校验流水线）/ 工作流（CI 与生产路径一致性）。触发词：check-migrations、只跑 getMigrations、虚假 CREATE/DROP INDEX、崩溃被报成漂移、先建后台轨道、显式 process.exit、redis-memory-server 持有事件循环。

## r563A · 管理型 API 的四条契约决策：一路由一读模型、敏感字段用「置空值」三态、破坏性解绑须显式开关、许可只 gate 写（来源：api.github.com/repos/n8n-io/n8n/pulls/40975，2026-10-14 r563A 一手 gh api 200 逐串命中 `GET / returns a summary (id, name, capabilities, surfaces) for every caller. GET /:id returns the full row and needs trustedSource:read` / `one read model per route, no per-caller branching in the controller` / `replaces config.authentication.client.clientSecret with the credential blanking value. A PATCH that sends the blanking value keeps the stored secret. Another value replaces it. An absent key clears it` / `PATCH drops bindings only when the body sets clearBindings: true` / `The license gates create and update only, so an instance that loses its license can still list, read, delete and re-check`；r563A 落地）
- **实证**：n8n 为「可信来源」（接受其令牌的外部身份提供方）加管理 API。六条路由里，列表对所有人返回摘要、详情需 read 权限；详情把 clientSecret 换成凭据置空值，PATCH 发置空值＝保留原密钥、发其他值＝替换、键缺省＝清除；PATCH 只在 `clearBindings: true` 时解绑，仅改 issuer 保留绑定；license 只 gate create/update，丢许可仍能 list/read/delete/check；写操作发 `trusted-source-created|updated|deleted` 审计事件并由日志流中继为 `n8n.audit.trusted-source.*`。
- **判据**：① **同一资源的不同读面拆成不同路由**，不在 handler 里按角色分支——分支会把权限矩阵埋进控制流，改权限就要改控制流。② **敏感字段的编辑契约必须三态**（置空＝不改 / 新值＝替换 / 缺省＝清除）：两态无法表达「不改」，而「不改」是编辑表单的默认情形。③ **破坏性副作用必须由独立显式字段触发**，不能挂在普通字段编辑上——改 issuer 时隐式解绑会在「修一个错别字」时摧毁全部用户链接。④ **许可降级只收回写能力，读与删除必须保留**，否则丢许可的实例既不能自证现状也不能自清。⑤ 写操作与审计事件同发并进入统一中继，审计不是事后补的旁路。
- 提升层：工具（管理 API 契约设计）/ 工作流（许可降级与审计）。触发词：trustedSource、clearBindings、credential blanking value、一路由一读模型、license 只 gate 写、issuer 变更保留绑定、n8n.audit.trusted-source。

## r563A · 「初始化默认状态」必须用追加语义实现，不能用整体替换：锁定对象下替换必然 409，重试只是放大延迟（来源：api.github.com/repos/langgenius/dify/pulls/43086，2026-10-14 r563A 一手 gh api 200 逐串命中 `HTTP 409 Conflict / code = 409 / reason = RBAC_ACCESS_POLICY_BINDING_LOCKED / rbac access policy binding is locked and cannot be modified` / `The task retries and eventually fails even though the workspace member initialization itself only needs to add the default member bindings` / `The task already uses the existing batch append whitelist operation when synchronizing a newly joined workspace member`；r563A 落地）
- **实证**：启用 Enterprise RBAC 后默认访问策略绑定是 locked bindings。创建 app/dataset/agent 会触发异步 `app_rbac` 初始化器，它对工作区成员批调用「替换用户访问策略」接口 ⇒ 该接口要改被锁定的默认绑定 ⇒ 409 `RBAC_ACCESS_POLICY_BINDING_LOCKED`；任务重试、最终失败，而初始化本身只需要追加默认成员绑定。同一任务在「同步新加入成员」时早已使用 batch append 白名单操作。修法：资源创建初始化复用同一 append 操作，显式用户策略替换 API 保持不变；不需要数据库迁移、队列改造或环境变量。
- **判据**：① **幂等初始化的写操作只能是增量的**：整体 replace 会碰到不可变/锁定对象并失败；选错动词（replace vs append）会让重试永不收敛。② **判据是「重试会不会改变结果」**：锁定对象导致的失败是确定性的，重试只增加延迟与噪音。③ **同一系统内已存在的正确操作应当复用**：同步新成员用的是 append，资源创建初始化就该用同一个，而不是新建一个替换调用。④ 修复面要窄：显式用户策略替换 API 保持不变，不因初始化改掉管理面语义。
- 提升层：工具（初始化与后台任务写操作选型）/ 工作流（重试收敛性判定）。触发词：app_rbac initializer、RBAC_ACCESS_POLICY_BINDING_LOCKED、replace vs append、locked binding 409、batch append whitelist、重试不改变结果、初始化幂等。

## r563A · 编码/加密格式切换时，「体积开销预算」必须按所有支持格式的最大值取，否则上限判定在更胖的格式下误伤（来源：api.github.com/repos/windmill-labs/windmill/pulls/11734，2026-10-14 r563A 一手 gh api 200 逐串命中 `encrypt ai session backups with aes-256-gcm` / `CipherFormat::current() is V2` / `PREVIOUS_RELEASE_ROLLOUT_UPTIME` / `CIPHER_PADDING goes from 16 to MAX_BYTES_OVERHEAD` / `Without this, a head at its cap and a multi-part push's token would read back as "grown" under GCM, and the second part of every multi-part push would be refused` / `Reads accept either format, so existing CBC objects keep restoring and are not rewritten`；r563A 落地）
- **实证**：AI 会话备份从 AES-256-CBC（`magic_crypt`）切到 AES-256-GCM（`wmA2`）。新对象只在两个条件同时成立时写 GCM：`CipherFormat::current()` 为 V2（所有 worker ≥1.832），且本服务 uptime ≥ `PREVIOUS_RELEASE_ROLLOUT_UPTIME`（30 分钟，滚动升级中旧版本副本仍在服务）。读侧 `decrypt_bytes` 先试 GCM 再回落 CBC，已有 CBC 对象不重写、下次浏览器推送该分片时自然迁移。**关键净新点**：`CIPHER_PADDING` 从 16 改为 `MAX_BYTES_OVERHEAD`（48）——GCM 在块填充之外还要加 magic/nonce/tag；不改则在「头部正好到上限」时，多段推送的第二段会被读回判定为「变长」而拒。
- **判据**：① **任何按密文长度做的上限判定，其开销预算必须取所有支持格式的最大值**：换到更胖的格式会把原本合法的数据判成越界，且只在边界值上出现。② **格式切换要「版本门 + 滚动升级窗口门」两道**，读侧必须同时接受两种格式，否则升级窗口内必然读到不能解的对象。③ **迁移不做原地重写**，靠下次写入自然升级，避免一次性全量改写带来的窗口与回滚成本。④ **误伤的表现是「第二段被拒」而不是「整体失败」**：分段协议的下限/上限判定要按段分别验证。
- 提升层：工具（加密格式与存储开销预算）/ 工作流（滚动升级兼容）。触发词：aes-256-gcm、MAX_BYTES_OVERHEAD、CIPHER_PADDING、CBC fallback、PREVIOUS_RELEASE_ROLLOUT_UPTIME、不重写旧对象、多段推送第二段被拒、密文上限误伤。

## r563A · 发布标签必须能被机器区分「稳定 / 预发布」：semver 不带通道信息，自动升级工具无法只取稳定版（来源：api.github.com/repos/n8n-io/n8n/issues/41000 与 40998，2026-10-14 r563A 一手 gh api 200 逐串命中 `a semver tag gives no info whether this is a stable or a beta version` / `That makes it impossible for automated tools like renovate to only pick stable versions` / `add stable suffxied docker tags`；r563A 落地）
- **实证**：n8n 的容器标签只有 semver，无法区分 stable 与 beta/prerelease，依赖自动升级的工具（renovate）因此无法只挑稳定版本。后续 PR 40998 的做法是**增加带 stable 后缀的镜像标签**（双标签），而不是改 semver 语义。
- **判据**：① **发布产物的通道可区分性是给机器用的**：消费方是自动升级工具，人眼可读的 release note 不能替代可判别的标签。② **修法是加标签而不是改语义**：另发一套「稳定」后缀标签，与完整 semver 标签并存，历史消费方不受影响。③ **依赖自动升级的下游应被当作发布契约的一方**：发布设计要给出「只取稳定」的可判定条件。④ 同理适用于技能/插件市场：版本号必须能被机器判断稳定通道，否则自动更新只能全量跟随。
- 提升层：工作流（发布通道与依赖自动升级）/ 可复用 Skill（技能市场的版本通道）。触发词：stable vs beta tag、renovate 只取稳定、stable 后缀镜像、semver 无通道信息、双标签并存。

## r563C · 配额/限流的计数键要在认证边界就确定并挂在身份对象上，且键必须在凭证轮换后保持稳定（来源：api.github.com/repos/n8n-io/n8n/pulls/40986，2026-10-14 r563C 一手 gh api 200 逐串命中 `ApiKeyAuthStrategy now sets apiKeyId on the TokenGrant` / `The rate limiter needs a stable counter key for each API key` / `The strategy already loads the key record but did not pass its ID on` / `The ID stays the same when a key is rotated, so rotation does not reset a budget` / `Session-cookie and scoped-JWT grants do not set it`；r563C 落地）
- **实证**：为 Public API 做「按 API key 计数」的限流器，第一步是把身份键固定下来：`ApiKeyAuthStrategy` 在 `TokenGrant` 上写入 `apiKeyId`，下游从 `req.tokenGrant` 读取；session-cookie 与 scoped-JWT 两种授予不设该字段。三条理由：限流器需要稳定计数键；认证策略本来就加载了 key 记录只是没往下传；**key 轮换时 ID 不变，所以轮换不会重置预算**。
- **判据**：① **限流/配额的计数键要在认证边界确定并随身份对象传递**，不要在下游重新推断——推断会随调用路径变化。② **键必须在凭证轮换后保持稳定**：若用「密钥材料本身」或会随轮换变化的值做键，轮换等于重置预算，构成绕过口。③ **不同授予类型要显式声明是否提供该键**：不设即表示不适用，而不是「未知」，下游不得拿默认值兜底。④ 这条与「授权判定缓存的键必须覆盖决定答案的全部输入」（r557A）互补：那条规定键的**维度完备性**，本条规定键的**生命周期稳定性**。
- 提升层：工具（限流与配额）/ 工作流（凭证轮换与预算连续性）。触发词：apiKeyId、TokenGrant 携带计数键、轮换不重置预算、stable counter key、session-cookie 不设该键。

## r563C · 标识符一旦发布就是契约：改名要枚举全部受影响面，破坏说明要写清「谁要做什么」（来源：api.github.com/repos/windmill-labs/windmill/pulls/11743，2026-10-14 r563C 一手 gh api 200 逐串命中 `Renames the Outlook OAuth provider added in #11694 (released in v1.831.0) from outlook to ms_outlook` / `so Microsoft 365 products all follow the ms_<product> naming (snake_case, one underscore per word boundary)` / `backend/oauth_connect.json: key outlook -> ms_outlook` / `frontend/src/lib/components/icons/index.ts: icon map key outlook -> ms_outlook` / `an admin who set up outlook OAuth in instance settings on v1.831+ has to reconfigure it as ms_outlook (redirect URI becomes <instance>/oauth/callback/ms_outlook), and resources created with the outlook type need to be recreated`；r563C 落地）
- **实证**：Outlook OAuth provider 在 v1.831.0 发布一天后被重命名为 `ms_outlook`（统一 `ms_<product>` snake_case）。受影响面逐项列出：后端 `oauth_connect.json` 的键、前端图标映射的键、回调 URI（`<instance>/oauth/callback/ms_outlook`）、以及**已用 `outlook` 类型创建的资源**（必须重建）。校验手段：`validate-oauth-connect.ts --integration ms_outlook` 静态检查通过。
- **判据**：① **标识符一旦进入发布就是对外契约**：改名成本 = 发布后时长 × 已被配置/引用的数量，超过极短窗口就必须提供别名或迁移路径，不能只说 breaking。② **改名必须枚举全部受影响面**：配置键、前端映射、URI 路径、已持久化数据的类型字段——漏一个就留下「半迁移」状态，且这种状态不会报错。③ **破坏说明要写成动作清单**（管理员重新配置 + 资源重建），而不是一句「breaking change」。④ **命名规范应在首次引入时就确定**：事后统一命名要付真实迁移成本。⑤ 静态校验脚本是改名类改动的必备验收项。
- 提升层：工作流（发布契约与破坏性变更说明）/ 工具（配置与资源迁移）。触发词：ms_outlook、provider 重命名、回调 URI 变化、已创建资源需重建、breaking 说明写动作清单、命名规范事后统一。

## r563C · 部署产物要声明「运行所需的前置条件」，让目标环境在写入前就能拒绝；解析顺序必须与运行时一致（来源：api.github.com/repos/langflow-ai/langflow/pulls/15668，2026-10-14 r563C 一手 gh api 200 逐串命中 `declare what their flows' MCP servers need where they are deployed, so a deploy target can refuse a project whose tool calls would fail instead of discovering it on the agent's first attempt` / `A server outside the installation needs a credential only whoever runs that environment can supply` / `One of our own projects needs to already be deployed there, and its connection is rebuilt against the target rather than copied` / `schema_version is 6 only when one of them is non-empty, so a project with no MCP servers packages byte-identically to before` / `The URL match is anchored to the whole path, so https://elsewhere.example/?next=/api/v1/mcp/project/<uuid>/x names no project` / `A server is resolved by name against the owner's mcp_server rows before it is classified, matching the precedence resolve_mcp_config applies at run time`；r563C 落地）
- **实证**：部署产物（manifest 与 deployment snapshot，顶层 + 每 flow）新增 `required_mcp_variables` 与 `required_mcp_projects`，声明其流里的 MCP server 需要什么，部署目标可在**写入前**拒绝一个「工具调用必然失败」的项目。两类需求分开建模：安装之外的 server 需要只有该环境运行者能提供的凭据；自家项目则需要已在目标处部署，且连接按目标重建而非复制。三条关键约束：`schema_version` **仅当声明非空**才升到 6（无 MCP server 的项目打包字节级不变）；URL 匹配**锚定整条 path**（query 里的伪装路径不指名任何项目）；server **按名字先对 owner 的 `mcp_server` 行解析再分类**，与运行时 `resolve_mcp_config` 的优先级一致——否则会照过期内联配置去供给项目，而流实际调用的是 row 指名的那个。
- **判据**：① **把「这里跑不起来」前移到写入前**：部署前声明前置条件，胜过运行时第一次调用才失败。② **不同类的需求要分开建模**（凭据 vs 已部署项目），因为它们的修法与责任方不同。③ **声明为空时产物必须字节级不变**（schema_version 条件升版），否则每次打包都产生无意义 diff 与假变更。④ **解析顺序必须与运行时一致**，否则部署期与运行期会供给不同目标（双解析分叉），且只在「行配置改过、内联配置留着」时出现。⑤ **URL 匹配要锚定整条路径**：只匹配子串会让 query 参数里的伪装路径通过校验。
- 提升层：工具（部署前置条件声明）/ 工作流（部署期验收与 schema 演进）。触发词：required_mcp_variables、required_mcp_projects、schema_version 条件升版、字节级不变、URL 锚定整条 path、解析优先级与运行时一致、部署前拒绝而非运行时失败。

## r563C · 自动初始化要提供「跳过」开关，且回归测试要用「拒绝创建」的替身验证默认路径没被改坏（来源：api.github.com/repos/n8n-io/n8n/pulls/40437，2026-10-14 r563C 一手 gh api 200 逐串命中 `Add a Skip Table Initialization option to the Postgres PGVector Store node for insert, load, and retrieve modes` / `skips extension and table creation when the database is already set up. Keep initialization enabled by default` / `Add regression tests for insert and retrieve with a mock database that rejects extension creation` / `Confirm that the default behavior still creates the extension and table` / `Use a database role that can read and write the table but cannot create extensions`；r563C 落地）
- **实证**：PGVector Store 节点新增 **Skip Table Initialization** 选项（insert/load/retrieve 三种模式），传给 `PGVectorStore` 以在数据库已建好时跳过 extension 与 table 创建；**默认仍初始化**。动机用例：数据库角色能读写表但**不能创建 extension**（基础设施由 DBA 预置、运行账号权限最小化）。回归测试用一个「拒绝创建 extension」的 mock 数据库覆盖 insert 与 retrieve，并**另外确认默认行为仍会创建 extension 与表**。
- **判据**：① **自动初始化要可跳过**：基础设施由外部预置、运行账号权限最小化是常态，硬编码初始化会让这类环境完全不可用。② **默认值保持不变**：跳过是显式选择，不能因为加了开关就翻转默认语义。③ **回归测试必须两条路径都测**：只测「跳过生效」会漏掉默认路径被改坏；正确做法是构造一个**拒绝执行初始化**的替身，验证跳过路径可用，同时验证默认路径仍真的去初始化。④ 这类开关的验收点是「权限不足的账号也能跑通功能」，而不是「开关能打开」。
- 提升层：工具（集成节点的初始化策略）/ 工作流（最小权限环境的可用性）。触发词：Skip Table Initialization、不能创建 extension 的角色、默认仍初始化、拒绝创建的 mock 验默认路径、基础设施外部预置。

## r564A · 默认载体决定跨重启语义；存在性检查要走对象的同一套访问路径；复用判据要比"当前实际"而不是比"目标"（来源：api.github.com/repos/PrefectHQ/prefect/issues/23389、/23382、/23381 与 repos/zenml-io/zenml/issues/5347，2026-10-14 r564A 一手 gh api 200 逐串命中 `The default lease storage is process memory, but `active_slots` is a database column. After a restart the lease is gone and the count stays.` / `Every deploy of a single-process server is a restart, so each deploy removes whatever capacity is held at that moment.` / `git rev-parse` echoes the input, so the check was always true and `pull_code` returned before fetching. Because the default destination does not include the commit, a deployment updated to a new `commit_sha` kept running the old code` / `the list branch of `apply_values` always dropped items that resolved to `NotSet`, regardless of `remove_notset`` / `For remote artifact stores (e.g. S3, GCS, Azure), the URI scheme causes `os.path.exists` to always evaluate to `False`, returning `"unknown"`` / `legitimate cross-version safety checks fail remotely`）
- **判据**：① **默认载体本身就是语义声明**：租约默认存进程内存，而 `active_slots` 是数据库列 ⇒ 重启后租约没了、计数还在，回收器无东西可过期、持有者自己的 `decrement-with-lease` 找不到租约回 204 什么也不释放，容量永久占满且没有任何日志行。**凡"承诺 + 计数"分置两处的机制，默认载体必须选与计数同寿命的那个**；内存态默认把"每次部署"变成"每次丢容量"（单进程服务的每次部署就是一次重启）。② **存在性检查必须走与对象同一套访问路径**：`os.path.exists` 遇到 `s3://` / `gs://` 恒假 ⇒ 记录的 Python 版本一律变 `"unknown"`，于是远程加载恒报"假版本不匹配"警告，真正该生效的跨版本安全检查在远程全部失效。**本地文件系统 API 不能直接用在远端 URI 上**——它不会报错，只会稳定地返回"不存在"。③ **"已存在"不等于"已是目标版本"**：`git rev-parse <commit_sha>` 对完整 40 字符 SHA 回显输入，比较恒真，`pull_code` 直接返回 ⇒ 持久化工作目录里，部署更新到新 `commit_sha` 却一直跑旧代码。**复用判据必须比较"当前实际状态"与"目标"（解析 `HEAD` 与 `<sha>^{commit}` 再比），而不是比较"目标"与"目标"**；自证恒真的检查是最危险的一类，且它同时解释了另一半症状——缩写 SHA 因为恒不相等而每次重 fetch，`git fetch origin <short-sha>` 又必然失败，于是删掉整个 checkout 重新 clone。④ **同一开关在不同容器类型上的行为必须一致**：`apply_values` 的 dict 分支在 `remove_notset=False` 时保留未解析值，list 分支无条件丢弃 ⇒ 只含步骤输出占位符的列表项在它依赖的步骤跑之前就被删掉（部署 inspect 出 `tags: ['prod']` 而 `description` 正常解析成 `commit abc123`）。**"标量正常、列表丢项"这类部分成功最难查**，因为它看起来像配置写错了。
- 提升层：可复用 Skill（发布/部署面的默认值与复用判据）/ 工作流（升级与回滚）。触发词：默认租约存储、重启丢租约、active_slots 不释放、每次部署丢容量、os.path.exists 对远端恒假、python_version.txt、unknown 版本、假版本不匹配、rev-parse 回显输入、自证恒真、复用判据比当前态、apply_values list 丢项、部分成功最难查。

## r564B · 特性生命周期是不对称的；缓存要存原始输入而不是派生状态（来源：export.arxiv.org/api/query 2026-10-14 r564B 一手 https 实拉，逐串命中 arXiv 2610.13806《FORTE》`adding new features must produce gains on some metric, while feature removal must not regress any metric` / `a feature can fail to be removed if it interacts with other features, its importance changes daily, it cannot be evaluated before production models change or data drift occurs, it is in contention for A/B test space with other launches, it causes regressions in an online A/B test, or it is consumed by multiple models that need to coordinate its deprecation` / `Lineage tracing identifies all downstream consumer models to realize the full savings of removing a feature`；arXiv 2610.13778《ReplaySSM: Cache SSM Inputs, Not State》`unrolls the recurrence to represent the state as a checkpoint and a buffer of recent SSM inputs` / `Keeping recent inputs also makes speculative rollback a buffer-pointer operation and enables output-only verification without materializing intermediate states` / `a low-precision checkpoint to serve output computation on most steps while a higher-precision checkpoint serves recurrent updates, so rounding error in the low-precision copy never enters later updates`）
- **判据**：① **加入与移除的判据必须不对称**：新增只要在某个指标上有增益，移除则要求**任何指标都不回退** ⇒ 用同一个门槛管两个方向，结果必然是只增不减。② **「能移除」的前置是消费方血缘**：被多个模型消费的特性，其下线需要这些模型协同；**没有血缘追踪就无法兑现移除的全部收益**，而且会在"以为没人用"的时候删掉在用项（与 rm「卸载要分级」「差分预览」互补）。③ **重要性是时变量，评估必须周期化**：原文列举"重要性每天变、在生产模型变更或数据漂移前无法评估、与其他上线争抢 A/B 位" ⇒ **一次性评估不足以支撑下线决策**，需要可日频、低开销的评估实现。④ **交互要靠分组消融（grouped ablation）而不是逐个测**：特性间的相互作用让"单独去掉 A 无回退"不能推出"去掉 {A,B,C} 也无回退" ⇒ 候选集要按低秩分组构造，离线结果要对在线 A/B 有预测力才放行。⑤ **缓存层要选原始输入而不是派生状态**：把循环展开成「checkpoint + 近期输入缓冲」，于是**回滚退化成一次指针操作**、可以只验输出而不物化中间状态。判据：**凡"状态 = 历史输入的派生"的结构，缓存输入比缓存状态更可回滚、更省 I/O**。⑥ **降级副本不得回流进权威状态**：低精度 checkpoint 只服务输出计算、高精度 checkpoint 服务循环更新，**于是低精度副本的舍入误差永远不会进入后续更新** ⇒ 性能优化引入的近似只能落在"用完即弃"的面上，绝不能写回权威状态（与 rm「崩溃≠漂移」「迁移期只加 CHECK」同族，本条管精度/近似面）。
- 提升层：工作流（特性生命周期治理）/ 工具（缓存与回滚设计）。触发词：特性加入与移除不对称、feature deprecation、消费方血缘、分组消融、日频评估、缓存输入而非状态、回滚是指针操作、低精度副本不回流、输出计算与循环更新分离。

## r564C · 发布动作不得隐式重解析依赖锁；清理要按「先叶子后父」且失败要留下可重试的锚点（来源：api.github.com/repos/windmill-labs/windmill/pulls/11739 与 repos/n8n-io/n8n/pulls/40995，2026-10-14 r564C 一手 gh api 200 逐串命中 `change-versions.yml` ran `cargo generate-lockfile` after bumping the version, which re-resolves the whole lockfile. Each release therefore also shipped about 100 semver-compatible dependency upgrades that nobody reviewed.` / `Release 1.831.0, for example, moved `cc` from 1.6 to 1.8 and `aws-lc-rs` from 1.18.1 to 1.18.2.` / `the restored rust-cache was useless. The run compiled 745 crates instead of the usual ~95, the compile took 23 min, and the step timed out`；`Pruning an execution now deletes its binary files before it deletes the database row.` / `After an instance moves to Azure, prune removed the execution row and the Azure execution payload, but left the binary files. Azure had no directory delete, and the disk store was not called while the mode was Azure. A failed file delete now keeps the row so the next prune can retry it.`）
- **判据**：① **"改版本号"这种最无害的发布动作，可能夹带一百个没人审过的依赖升级**：release 工作流在 bump 之后跑 `cargo generate-lockfile`，等于全量重解析 ⇒ 每次发版顺带发布约 100 个 semver 兼容升级。判据：**发布提交必须在既有锁上工作，禁止重新解析**；把"升级依赖"与"发版本"合成一个提交，会让依赖变更既无评审也无回滚粒度。② **重解析的代价不止是安全/正确性，还有缓存与时间的确定性**：`cc` 从 1.6 到 1.8 就足以让 rust-cache 失效，编译从约 95 crate 涨到 745、耗时 23 分钟并撞上 30 分钟超时 ⇒ CI 起超时前先问"这轮是不是重解析了锁"，**超时的根因常常在依赖层不在测试层**。③ **时间预算要按最慢的 runner 留余量**：正常热缓存 22–28 分钟、而部分 runner 链接慢一倍 ⇒ 把超时贴着均值设，等于让机器差异变成随机红灯。④ **清理必须按「先叶子后父、先外部后记录」**：prune 先删执行行与 Azure payload，却留下二进制文件（Azure 无目录删除、且 mode=Azure 时不再调 disk store）⇒ 孤儿文件。**凡跨存储后端的删除，要为每个后端各写一条删除路径，并在模式切换时覆盖"旧模式的残留"**。⑤ **删除失败要留下可重试的锚点**：文件删除失败则保留数据库行，让下一轮 prune 可以再试 ⇒ 把"行已删"当成清理完成，会让残留永远无法被再次发现。**清理的可重入性比清理的原子性更实用**。
- 提升层：工作流（发布流水线与依赖治理）/ 工具（存储清理）。触发词：发布提交重解析锁、release 夹带依赖升级、generate-lockfile、rust-cache 失效、745 crates、先删叶子再删父、Azure 无目录删除、删除失败保留行、清理可重入。


## r565A · 发版完整性与产物身份五条（来源：GitHub issue 面八仓，2026-10-14 一手实拉）
- **实证**：① windmill #11669 两个 workspace 部署同一脚本共享一个 hash，workers 对两者跑同一个 workspace 的锁；② Flowise #6623 镜像 flowiseai/flowise:3.1.3 内含的 CLI 版本是 3.1.2；③ windmill #11309 官方 Docker 镜像内嵌 Go 工具链在应用版本之间不更新，累计 14 个以上 HIGH CVE（含符号链接穿越）；④ zenml #5174 数据库备份在写失败后可复用不完整制品；⑤ zenml #5215 请求 webhook 事件的幂等支持、activepieces #16422 Google Drive 触发器在重新发布时重置轮询 checkpoint（丢失 isRepublish 标志）。
- **判据**：① **身份键必须含作用域维度**：内容哈希相同不等于同一对象，租户/命名空间维度缺一就跨租户共用锁；发版与运行时一致性都要用带维度的身份键。② **发版完整性要断言每个自带版本的内嵌组件**：只断言主程序版本等于镜像 tag 是典型假通过。③ **运行时/工具链是发版检查单的一等条目**，跨版本不更新的运行时是静默的累积风险面。④ **产物可见性必须由提交标记控制**：先写临时位置 + 成功后才可见，失败件留可诊断但不参与复用；「复用先例存在」≠「先例完整」。⑤ **外部进度状态有两个丢失口**——入站事件重投递与流程复发布/重建；前者要幂等键，后者要保留游标标志位，两者同源于「进度不可被重建路径重置」。
- 提升层：工作流（发版与身份键）/ 工具（产物可见性）。
- 触发词：内容哈希缺租户维度、跨租户共用锁、发版内嵌组件不一致、镜像内工具链 CVE、写失败产物被复用、提交标记才可见、入站幂等键、复发布丢 checkpoint。


## r565B · 撤销的结果契约（来源：arXiv 2610.15991，2026-10-14 实拉）
- **实证**：「Revocation Is Not Complete at Receipt: An Executable Outcome Contract for Distributed Agent-Tool Gateways」——在分布式工具网关里，收到撤销请求并不构成撤销完成。
- **判据**：① **撤销要定义为可执行的结果契约**（可验证终态 + 传播完成判据），而非消息投递完成；② 传播窗口内被缓存的授权仍可放行，验收必须断言「窗口内调用被拒」；③ 窗口期内调用单独记档。
- 提升层：工具（授权网关）/ 工作流（撤销语义）。
- 触发词：撤销不完整、收讫不等于生效、传播窗口、可执行结果契约。

## r566C · 声明输入不虚报 / 发布产物可核 / 告警关闭条件三条（来源：activepieces #16140 / #16457、Flowise #6623、windmill #11309，2026-10-14 实拉）
- **实证**：① piece 声明的 inputs 从未被 run() 发送（多组件同时存在）；② Docker 镜像内 Flowise CLI 版本与 release 标签不一致；官方镜像内嵌 Go 工具链跨发布不更新（14+ HIGH CVE）；③ 队列告警工单需显式保持开启直到修复部署。
- **判据**：① **声明-发送一致性验收**：对每个声明输入做一次端到端发送断言，无断言即视为未声明，禁止依赖调用方自觉。② **发布产物内含物逐项核版本**：镜像内 CLI、脚本、工具链、内置组件版本与发布标签逐项比对，任一不符即发布不可信。③ **告警生命周期绑定修复上线**：告警关闭条件＝修复已部署并验证，而非"已派单"或"已知悉"。
- 提升层：工作流（发布验收/告警治理）。
- 触发词：声明输入不发送、发布产物版本不一致、镜像内工具链、告警不得早关、关闭条件绑定部署。


## r568C 下沉细则（wb-release-maintain）
1. **版本复用核对兼容 range**（langflow #15657）：reuse-stable 只看 PyPI 版本存在 ⇒ RC pin 另一发布线的 bundle（lfx range 不符装不上）；每条 minor 线拥有自己的 bundle minor；range 未知 fail closed；错误命名冲突 range+bump 指引；同 commit 开两条发布线。
2. **预校验先于所有写动作**（activepieces #16514）：LOCK_AND_PUBLISH 先锁草稿+设 publishedVersionId 才 404 ⇒ 半发布；live flow 被切 trigger-less 版本变 DISABLED；三入口（直接/审批/CHANGE_STATUS）同漏；400 FLOW_OPERATION_INVALID 替代 404 undefined@undefined。
- 提升层：工作流（发布前校验/版本复用判定）。
- 触发词：reuse-stable、lfx range、range 未知 fail closed、预校验先于写、半发布状态、三入口同漏、FLOW_OPERATION_INVALID。


## r571C 下沉条目：权限与权益必须在使用点校验，不能只在配置点校验（来源：activepieces PR #16158，2026-10-15 r571C 一手 gh api 200 逐串命中）

1. **使用点校验**（activepieces #16158）：Team/Enterprise 特性过去**只在 admin 配置时校验** ⇒ 计划期/试用期内配好的能力在过期后继续生效；修复把校验下沉到使用点——SAML 登录/ACS、embedded 登录、交给 run 的全局连接、secret-manager 读取，全部在使用时判定 entitlement。
- 判据：① 权限/配额/套餐权益的判定点是**使用点**不是配置点，配置点校验只做「当时允许」的快照，过期后必须失效；② 每个使用该权益的新入口都要单独接校验，新增入口遗漏是此类缺陷的主要来源（本条四入口同漏）；③ 权益失效的默认动作必须是拒绝并给出可操作的续期路径，不得静默降级为「继续可用」；④ 与 §暴露-收紧配对律（ssc 1.96.0 Flowise #5930/#6578）分工：那条管能力面暴露与收紧成对出现，本条管权益时效的判定位置。
- 提升层：工作流（权限治理）/ 工具（准入校验）。
- 触发词：entitlement 使用点校验、配置点快照失效、试用期后继续生效、四入口同漏、静默降级为可用。



## r572C 下沉条目：并发限流器的槽位必须在同一执行上下文中获取与释放（来源：pydantic/pydantic-ai GHSA-6fqq-452j-qhrp，2026-10-15 r572C 一手 gh api security-advisories 200 逐串命中）

1. **跨任务释放导致槽位永久泄漏**：用 `ConcurrencyLimitedModel` / `limit_model_concurrency` 包装模型时，若流式请求的**释放槽位发生在与获取槽位不同的 task 上**，共享并发容量会被**永久**丢失。触发条件包括流提前结束，以及用默认 `stream_text()` 去抖完全消费流的**正常路径**。后果：把受影响的流式端点暴露给网络客户端、且多个请求共享一个长生命周期 limiter 时，客户端反复「起流—断连」即可逐步耗尽全部容量。
   - 判据：① 任何 acquire/release 配对的限流原语，释放必须与获取在同一执行上下文（同一 task / 同一协程 / 同一请求作用域），跨上下文释放 = 泄漏；② 泄漏型缺陷的回归用例必须包含「正常完整消费」路径，只测「异常中断」会漏掉默认路径上的泄漏；③ 长生命周期共享限流器 + 可被外部触发的端点 = 可被单客户端放大的资源耗尽面，必须配每客户端配额或空闲超时回收；④ 与 §并发写冲突（既有面）分工：那条管数据正确性，本条管**容量资源**的不可恢复丢失。
- 提升层：工具（资源管理/流式接口）。
- 触发词：ConcurrencyLimitedModel、limit_model_concurrency、槽位泄漏、跨 task 释放、stream_text 去抖、起流断连耗尽容量、长生命周期 limiter。

## r573A/C 下沉条目（2026-10-15，来源见文末，均为一手实拉）
① **失败清理不得删除已注册产物：不确定归属的产物一律保留**——步骤执行可能在「产物已注册 / 服务端已完成」之后才抛错，此时 launcher 的异常处理器删掉输出目录 ⇒ **已持久化的元数据指向缺失文件**。修法：从该处理器移除自动删除，并文档化「失败后保留部分/未使用文件」。明确否掉的两种删除门：按 step status 或按返回的 artifact response 判断——两者都排不掉「在飞或未确认的注册」。判据：① 删除只在归属确定后发生，不确定即保留（不可逆数据丢失优先于整洁）；② 完成恢复与孤儿清理拆成独立工序，不在失败路径上顺手做。来源：github.com/zenml-io/zenml#5362（gh api 200，逐字 `Step execution can raise after artifact registration or server-side completion has already succeeded. The launcher's exception handler then deleted output directories, leaving persisted metadata pointing to missing files` / `neither safely excludes an in-flight or unacknowledged registration`）。触发词：失败后删除输出、元数据指向缺失文件、保留优先、删除门不可靠、在飞注册不可判。
② **传输/协议选择不得由隐式默认决定，缺失必填须指名配置来源**——CustomMCP 的 `getTools()` 只在 `CUSTOM_MCP_PROTOCOL === 'stdio'` **且** 配置带 `command` 时走 stdio，否则一律按 `'sse'` 构造；`MCPToolkit.createClient()` 在无 `url` 时抛 `URL is required for SSE transport`，而用户面对的是 Agent 节点里一句不含配置路径的报错。判据：① 协议/传输必须显式声明，隐式回落要可观测；② 「缺少必填字段」的报错要指出**哪个配置对象的哪个字段**，只报库内错误串＝无法自助修复。来源：github.com/FlowiseAI/Flowise#6716（gh api 200，逐字 `always constructs the toolkit with the 'sse' transport type unless CUSTOM_MCP_PROTOCOL === 'stdio' and the config has a command` / `the non-stdio branch throws when the config has no url`）。触发词：CUSTOM_MCP_PROTOCOL、默认回落 sse、URL is required、配置来源未指名、mcpServerConfig 缺 url。
③ **预检 / 默认值 / UI 三处必须与运行时单一真源对齐，「兄弟健康」不得掩盖「默认不可达」**——langflow #15733 修三处不一致：① 预检 `probe_opensearch` 原本不做后端实际做的 SSRF/KB 允许列表校验 ⇒ 运行时拒绝的 URL 预检放行，结果每次 create 都 422（现在启动即失败并给出 `LANGFLOW_SSRF_ALLOWED_HOSTS` 修复指引）；② **默认后端**（配了 pgVector 就用它，否则 OpenSearch）不可达必须启动失败，兄弟后端健康只配 warn 并打印修复提示；③ `/config` 暴露 `default_vector_store_backend`，KB/MB 选择器与 DB Providers 页跟随它而非硬编码假设 pgVector，环境变量提供的 OpenSearch 也算已配置，`use_ssl/verify_certs` 不再对 env 提供的 URL 强置 true。判据：预检复用运行时同一个校验函数；默认后端不可达＝启动失败（不是警告）；UI 默认值读配置面而非写死。来源：github.com/langflow-ai/langflow#15733（gh api 200，逐字 `probe_opensearch now runs the same SSRF / KB-allow-list validation as the backend` / `boot fails when the default backend is unreachable, even if a sibling is healthy` / `the KB/MB pickers and DB Providers page follow it instead of assuming pgVector`）。触发词：preflight vs runtime 不一致、SSRF allow-list、default backend unreachable、UI 默认硬编码、/config 单一真源、兄弟健康掩盖默认失效。
④ **回收责任必须落到 PID 1，孤儿累积是失效的可见信号**——worker 容器以纯 `node` 跑 PID 1，node 只回收自己 spawn 的子进程；当 worker **杀掉一个活着的沙箱**（如引擎无响应超时），isolate 内部进程被 reparent 到 PID 1 且永不回收（引擎自己 OOM/崩掉的沙箱反而干净退出）。专用复用沙箱集群上 7 天累积 250–280 个 `[isolate] <defunct>`，每个僵尸给 worker 的 15s `si.processes()` 扫描多加一行——该扫描占容器 CPU 84%（约 76ms/次），**CPU 随容器年龄增长**。修法：`Dockerfile` 与 `Dockerfile.worker` 装 tini 并置于 entrypoint 前（转发信号，shutdown 仍到 node）；`docker run --init` 用户行为不变。对照实验：引擎 SIGKILL 场景两臂均 0 僵尸；引擎 SIGSTOP 冻结→worker 超时杀活沙箱场景，无 tini 产生 5 个 `PPid: 1` 僵尸、有 tini 为 0。判据：① 容器 PID 1 必须有 reaper；② 「监控扫描成本随时间增长」就是孤儿泄漏的指纹，要当缺陷信号而非调优项。来源：github.com/activepieces/activepieces#15770（gh api 200，逐字 `node only reaps children it spawned itself` / `250-280 [isolate] <defunct> per container after ~7 days` / `84% of container CPU on the worker MainThread`）。触发词：tini、PID 1 reaper、orphan reparent、defunct 累积、si.processes 扫描成本、CPU 随容器年龄增长。
⑤ **回收器的计数键粒度决定漏网场景：按 transport 计数则「初始化从未完成」的对象永不可回收**——n8n #36850 空闲回收按 transport 而非 session id 计数。判据：回收/租约的计数单位必须覆盖「未完成初始化」的对象（它们从未进入常规计数面），否则该类对象永久漏网；验收用例必须含「创建后立刻失联、从未完成初始化」这一态。来源：github.com/n8n-io/n8n#36850（gh api 200；经 Qoder r628-Q-A⑤ 提名，本轮一手复核属实）。触发词：per transport vs per session、初始化未完成、永不可回收、idle evict 粒度。

## r574A 下沉条目（2026-10-15，GitHub issue 面八仓 gh api 一手实拉）
① **清理动作必须幂等：已确认缺失的目标判成功，不得把「不存在」当错误抛出**——企业版删除时 HomeSnapshot 清理非重试安全：快照已经不存在仍抛 `BindingDestroyError`，导致已完成的删除被回滚/重试卡死。判据：删除/清理路径要把「目标已不存在」归一为成功（与「删除失败」区分），重试安全是清理动作的准入条件；验收用例必须含「目标已被删过一次」的重入场景。来源：github.com/langgenius/dify#44086（gh api 200，逐字 `Enterprise HomeSnapshot cleanup is not retry-safe — an already-missing snapshot raises BindingDestroyError`）+ 修复 PR #44085 `treat a confirmed-missing Home Snapshot as a success on Enterprise delete`。触发词：清理非幂等、已缺失仍报错、BindingDestroyError、重入删除、重试安全、confirmed-missing。
② **权益降级后遗留的高权限对象仍须保留删除通道**——降级的平台能删掉遗留的 AI provider key，却不能新增/编辑：清理动作被同一道权益门挡住，等于把高危残留永久留在系统里。判据：权限门对「写」与「清理」要分开——降级状态下写被拒是预期，清理/回收必须仍可执行；验收要覆盖「降级态下遗留凭据能否清除」，否则降级=残留固化。来源：github.com/activepieces/activepieces#16273（gh api 200，逐字 `Downgraded platforms can delete leftover AI provider keys but cannot add or edit them`）。触发词：降级残留、清理被权益门挡、可删不可改、遗留凭据固化、回收通道与写通道分离。

## r574C 下沉条目（2026-10-15，GitHub PR 面 gh api 一手实拉）
① **删除容器必须级联清理其内部产物，重跑必须清理或复用前次样本，否则留孤儿**——删 loop/router 时只删容器，里面的步骤测试数据仍留在存储里；重新测试一个 trigger 会把旧样本文件留在存储中。判据：容器与内容是同一生命周期，删除动作要沿包含关系级联；「重跑/重测」要么复用前次产物（同一标识）要么先清理，禁止叠加留下多份无主数据；验收断言删除后按内容标识查为空。来源：github.com/activepieces/activepieces#16530 / #16542（gh api 200，逐字 `deleting a loop or router now also deletes the test data of the steps inside it` / `re-testing a trigger no longer leaves old sample files in storage`）。触发词：级联清理、容器与内容同生命周期、孤儿测试数据、重跑留旧样本、删除后按内容查空。
② **技能传播是供应链：修复不随源传播，审计位须按传播影响力排而非按流行度排**——Skill Constellations（arXiv 2610.11169，2026-10-15 arxiv.org/abs 一手 200 标题命中 `Tracing the Supply Chain of Agent Skills on GitHub`）：跨仓拷贝网络里技能副本几乎不随源变更（`Skill copies almost never change with their source`，源上的修复很少到达副本），星数不指源（`GitHub stars do not identify`），按其排名最高的 100 个仓库做审查可阻止 14.9% 的高风险技能后续被采用，而按星数最高的 100 个只有 0.5%（29.8 倍差）。判据：① 修安全问题时不得假设「上游修了=下游好了」，要发版本化引用而非拷贝；② 审计/准入优先级按传播网络位置排，流行度是无效代理（经 Qoder r628-Q-C① 提名，本轮一手复核标题与数字属实）。触发词：拷贝供应链、修复不随源、星数不指源、14.9% vs 0.5%、版本化引用代替拷贝、审计位按传播排。

## r575A · 被宿主流程调用的 agent 运行结束必须关闭：调用方生命周期不等于被调用 agent 的生命周期（来源：api.github.com/repos/n8n-io/n8n/pulls/41128 `Close agent after run when invoked from workflow`，2026-10-15 r575A 一手 gh api 200）
——从工作流内调用的 agent 若不显式收口，会话/连接/内存会跨运行残留，表现为越跑越慢与连接泄漏，且泄漏量随调用次数线性累积。判据=谁发起调用谁负责收口，收口动作须在成功与失败两条分支都存在。
## r575C · 旁路写入不得提交调用方事务：日志/暂存用独立 flush，禁止绑定调用方会话提交（来源：api.github.com/repos/langgenius/dify/pulls/44084 `stage hit-testing query log with flush instead of committing caller session`，2026-10-15 r575C 一手 gh api 200）
——旁路写入若提交调用方事务，就把「记录一下」变成「改变业务状态」，故障时还会连带回滚或污染调用方一致性。判据=旁路写入的提交边界独立，且失败不得影响主流程。
## r575C · 替换类写操作必须入审计：覆盖/替换/整体重写要留可追溯记录（来源：api.github.com/repos/langflow-ai/langflow/pulls/15754 `audit project replacement operations`，2026-10-15 r575C 一手 gh api 200）
——替换是「删除+新建」的复合动作，只审新建会漏掉被替掉的那份，事后无法回答「原来是什么」。判据=审计同时记录被替换对象标识与新对象标识。


## r576A · 删除/替换操作必须按「操作前后差集」清理附属数据，清理失败只能 best-effort（来源：api.github.com/repos/activepieces/activepieces/pulls/16530 + /16542，2026-10-15 r576A 一手 gh api 200，两 PR 合并落一条）
——删 loop/router 时只删了被点名步骤的样本文件，嵌套步骤的文件成孤儿；重测触发器替换了事件行却留下被替换事件的 FILE 行与 S3 对象（FK 级联方向是 file→event，不反向），每次测试按事件数累积直到 30 天 retention。判据=清理目标取"操作前存在、操作后消失"的差集，而不是请求里点名的那个对象；级联方向决定谁被清理；清理失败记 warning 并保留行以便重试，绝不阻断主操作。
- 提升层：工具（存储与级联）/ 工作流（测试与删除的副作用面）。
- 触发词：孤儿附属文件、差集清理、级联方向、替换留旧文件、best-effort 清理、保留行可重试。

## r577A · **依赖外部订阅/租约的触发器必须有续期机制与到期可见性**
- **实证**：n8n #40905——Microsoft Teams Trigger 在发布/激活时创建 Microsoft Graph 变更通知订阅，但**没有任何东西去续期**；Graph 对 `channelMessage` 订阅上限 4320 分钟（3 天），于是触发器在每次激活或 n8n 重启约 3 天后停止收消息。工作流仍显示 **Active**、无执行失败、无报错，只是"静默"；案例中 12 天无人察觉（带图片的消息没被处理）。Graph 生命周期通知（`@odata.type: "#microsoft.graph.subscription"`）会作为正常 trigger item 投递到工作流，但无人处理（无 PATCH、无重新授权、无重建），用户只能手工过滤。`checkExists()` 只保留有效期 >5 分钟的订阅，`create()`/`delete()` 之外**找不到续期逻辑**，也没有处理 `reauthorizationRequired` / `subscriptionRemoved`。
- **判据**：① **有到期时间的外部依赖必须配一条续期路径**，创建/删除齐全而续期缺失 = 定时静默失效；验收要包含"超过最长租期后仍在工作"的时间维度用例。② **状态显示（Active）必须来自实际租约状态**，不能来自"我们创建过它"，否则监控系统本身给出错误的安全感。③ 生命周期/到期类回调必须被显式处理或显式忽略（有日志），默认落到业务流里当普通数据是设计缺陷。
- 提升层：工具（外部订阅生命周期）/ 工作流（触发器健康可见性）。触发词：Graph subscription、租约未续期、3 天后静默停摆、Active 但已失效、reauthorizationRequired、subscriptionRemoved、到期回调当业务数据。

## r577A · **写入失败后不得保留可能错位的内部索引：失败路径要回滚视图或使索引失效**
- **实证**：Activepieces #16343——一次失败的删除会让表格编辑器显示的**位置布局**与后续 API 请求所用的布局不一致，之后一次普通单元格编辑就会打到**合法但非预期**的记录或字段上，请求还返回成功。例：删除 Alice 失败后 Bob 变成可见第一行，把 Bob 改成 Robert 实际发往 **Alice 的 record ID**；删除 Name 列失败后 Email 成为首列，但编辑该单元格发的是 **Name 的 field ID**。触发条件极轻：一次被拒的 DELETE + 同一次编辑器会话里的下一次编辑；已在 DELETE 待定期间排队的编辑同样受影响。作者按上游 commit 518ae709 复现：只拦截 DELETE 返回 500，放行后续 POST。
- **判据**：① **乐观视图与已确认状态必须可区分**：失败后残留的位置映射是"脏索引"，继续用它寻址 = 数据完整性缺陷，而不仅是"少了错误提示"。② **一次失败的操作会污染其后的操作，即使后者本身完全合法**——因此失败处理的验收点不是"报了错"，而是"后续操作不再使用失败前的假设"。③ 并发/排队场景要单独验：失败期间入队的编辑同样会走到脏索引。
- 提升层：工具（写路径状态一致性）/ 工作流（失败后自愈）。触发词：失败后索引错位、乐观视图残留、失败删除后编辑错记录、数据完整性而非报错、排队编辑走脏索引。

## r577A · **发布/重部署动作不得重置运行时消费位点**
- **实证**：Activepieces #16422——带 Google Drive New File/New Folder 触发器的 flow **每次重新发布都把 `lastPoll` 重置为发布时间**，于是上一次轮询（5 分钟节奏）到发布之间创建的文件**永不发出**，且无报错（0.88.4-hotfix.3 + piece 0.10.0，main 上 piece 0.11.3 同代码）。核心修复 #14147（0.87.0）只在触发器把 `context.isRepublish` 转发给 `pollingHelper.onEnable` 时才保留检查点，这两个触发器**把这个字段丢了**；helper 里有 `isRepublish` 判断，调用点没传 ⇒ `store.put('lastPoll', Date.now())` 每次 enable 都执行。清扫 PR #14637（全量转发 context）被关闭未合，只有 HubSpot/Jira 通过 #14644 修好。
- **判据**：① **"部署动作"与"运行时状态"必须解耦**：发布是代码/配置维度的动作，不应连带重置消费位点这类运行时进度；需要重置时必须显式声明（本例用 `isRepublish` 显式区分）。② 这类缺陷是**平台级共性 + 逐组件漏转发**：修好 helper 不等于修好所有调用点，需按"调用点清单"逐一核对是否透传上下文（与 r577A 并发锁的"按调用方清单逐条验"同构）。③ 表现为静默丢事件（不是报错、不是重复），只能靠"发布前后位点不变"的回归用例发现。
- 提升层：工具（轮询触发器契约）/ 工作流（发布与运行时状态分离）。触发词：republish 重置 lastPoll、isRepublish 未透传、发布丢事件、消费位点被重置、helper 修好但调用点漏转发。

## r590B 实证（GitHub 八仓 issue 面，gh api 一手逐串命中）

- **实证**：ap #16568（v23 piece-upgrade 注册表把 ~80 条流重写到「修复前版本」）——自动升级注册表选了带已知 multipart 上传 bug 的版本。机制：注册表目标版本 = 通过 metadata 兼容阶梯的「最新版」，从不比对同 piece 后续 `fix(...)` bump；google-drive 0.7.9 / jira-cloud 0.3.7 等修复在生成前数周已发布却被锁为「目标」（空文件/附件 500）。方法：自动升级注册表须对每条目标版本做「fix 版本反向校验」——目标版本须 ≥ 该 piece 已知修复版本；门控不仅看 unsafeSteps，须列出具体受影响的 attachment/表单能力；升级前审计全量目标（CSV 81 行：43 生成前已修复、5 生成后修复、33 无修复）。提升层：可复用 Skill（升级目标版本审计）/ 工作流（fix 版本反向校验门）。触发词：piece-upgrade 注册表、修复前版本、自动升级重写、fix 版本反向校验、unsafeSteps 门控、metadata 兼容阶梯、0.88.4→0.92.2。

## r594A（GitHub 八仓活跃 issue 面 · 一手命中 · 2026-10-16）

- **① 换执行引擎的迁移：翻默认值 + 保留逃生阀，而不是删旧路径强制迁移**（来源 activepieces/activepieces #16573 一手命中）。
  - **实证**：把代码步骤执行器默认从 legacy（Node/v8-isolate）翻到 Deno 沙箱的做法是——只翻转 `useDeno` 的**默认值**（engine `code-executor`、worker `execute-action`、sandbox `flow-provisioning`、api `pre-warm-workers` **四个读取点统一**），于是**全部既有 flow 自动迁移**：不重写数据、不需要管理员逐 flow 清扫；同时保留 per-flow 逃生阀 `useDeno:false`（行为与迁移前完全一致），且既有 admin `revert-from-deno` 端点写入的正是这个标志 ⇒ **老回滚工具自动变成 opt-out 通道**，不新增第二套语义。
  - **判据**：执行器/运行时替换的迁移成本主要在"存量"与"逃生"两头：删旧路径会把存量一次性推到新路径上，失败时没有退路；翻默认值则把存量平滑带过去，逃生阀复用既有回滚通道可避免"两套回滚语义"。落地自检：凡是"默认值翻转"类迁移，必须枚举**所有读取该默认值的代码点**并一次改齐（本例四个），漏一个就等于同一配置有两种解释。
  - 提升层：工作流（迁移策略）/ 工具（执行器治理）。触发词：useDeno 默认翻转、per-flow opt-out、revert-from-deno、默认值读取点枚举、沙箱迁移。

## r595A（2026-10-16 · 来源 GitHub 技能生态仓 · wb-release-maintain 1.162.0）

1. **破坏性版本必须带机检升级步骤**（mattpocock/skills#1176）：1.2.x 用 `/setup` 建的仓库在插件升到 1.3.x 后保留旧配置（根 `CONTEXT.md` + 指向它的 `domain.md`），唯一迁移说明躺在 changelog 的 1.3.0 条目里 —— 没有任何东西告诉用户"你的仓库需要改"。**规则**：破坏性变更 = 检测脚本/命令 + 提示 + 迁移动作，仅有 changelog 条目等于没有迁移路径。
2. **清理指令须给出"被拒绝时"的替代路径**（mattpocock/skills#1251）：清理步骤只写"清掉所有实现者 worktree"，实现者于是敲 `git worktree remove … && git branch -D …`；而该仓库自身推荐的 `git-guardrails` 正好拦 `branch -D`，复合命令整体失败。**规则**：涉及删除/回收的指令必须写清被护栏拒绝时的替代处置与人工出口，不得假定删除总能成功。
3. **审计记录的主体必须是真实执行者，不是承载容器**（activepieces/activepieces#15192）：项目发布一律被记成 platform owner 所为，"Imported By" 列对每次发布都显示平台属主 —— 多租户嵌入场景下发布历史**无法回答它存在的唯一问题：谁把这次变更推上去的**。**规则**：变更审计要记执行主体（人/身份）而非宿主/容器；共享载体下缺失主体即等于审计失效。

## r596B（2026-10-16 · 来源 GitHub 生态仓实拉 · wb-release-maintain 1.163.0）

1. **更新必须按内容判定幂等：内容相同不重下，不得产生「幽灵更新」**（vercel-labs/skills#2512 / PR#2518「stop reinstalling unchanged skills installed from a snapshot」）：从快照安装的技能每次 `update` 都被无条件重下载，产生**内容完全相同**的更新记录——用户看到「已更新」但没有任何变化，真实变更因此被淹没。既有 rm「幂等设计前先问该钩子会不会随更新重跑」管**钩子触发次数**，本条管**内容等价性**。规则：更新的判定键是**内容哈希**而不是版本号/时间戳；哈希相同即跳过并回执 `unchanged`，不得写更新记录、不得触发下游重装。
2. **活跃会话下不得重定位在用的钩子/脚本文件**（anthropics/claude-code#98839）：插件重新同步时移动了钩子脚本的位置，而此时会话正在运行 → **此后每一个 prompt 都被永久阻断**，且无自恢复路径。既有 rm「撤除是两步：先 deactivate 再 delete」管计划内撤除，本条管**计划外的热重定位**。规则：对运行中被加载的文件，移动/重命名必须先确保无持有者（或走「复制 → 切换引用 → 事后清理」），并保留旧路径的兼容期；任何重定位失败都要能回到原状，不得留下「永久阻断」终态。
3. **接入新模型/新后端必须自带默认参数族，缺失即显式失败而非降级**（openai/openai-agents-python#5336）：GPT-6 系列没有默认 reasoning 设置，带 function tools 请求 `/v1/chat/completions` 直接 400。规则：新增模型/供应商不是「加个名字」，必须同时声明其必需参数与默认值；缺默认值的路径应快速失败并给出「该后端需显式指定 X」，而不是静默用一个不合适的默认继续跑。

判非（本轮核实）：vercel#2484（符号链接计入技能目录哈希）与 r594C symlink 族同族；vercel#2487（安装摘要显示真实落点）与 rules/07 §10.4「写入后验证落位正确」重叠 >60%；claude-code#102546（归档留下本地分支）与 rm「清理被拒替代路径」同族；vercel#2509（在已注册 agent 目录发现技能）与 sa 1.170.0 单一真源同族。

## r597C（2026-10-16 · 新达站点 help.make.com llms.txt（73,201B，前轮超时） + docs.openclaw.ai CI 面 · wb-release-maintain 1.164.0）

1. **回滚能力边界必须按组件能力标注；开了自动提交就等于放弃跨环节回滚**（make/rollback-error-handler）：Rollback handler 只能回滚支持事务的模块（界面上以 ACID 标签标注），不能撤销诸如"发邮件""删文件"这类已发生的外溢动作；且当 Auto-commit 打开时，只有**出错的那个模块**能回滚，此前模块的改动已经提交、不可回滚；关掉 Auto-commit 才能把整个 bundle 内所有支持事务的改动一起回退。规则：交付前先画出这条链路上哪些环节可回滚、哪些不可回滚；把提交模式（自动/显式）写进回滚预案——默认开启的自动提交会把回滚窗口缩到单个环节。
2. **修复逻辑错误后的标准动作是"用旧输入跑新代码"，且调试重放与生产回填要用两个入口**（make/scenario-run-replay）：用上一次运行的触发数据执行**当前版本**的场景。文档给了三类用途：① 测试与调试（Builder 内 "Run with existing data"，边改边重放同一份数据）；② 错误恢复（例如 100 条因逻辑错误失败的运行，先在 Builder 里修好，再重放那 99 条）；③ 数据回填（从 history / Run details 直接重放，不必进 Builder）。规则：别为了复现问题去造新数据——保留触发载荷就能重放；同时要区分"在编辑器里重放调试"与"在生产历史里重放回填"，后者会被当成真实副作用。
3. **按变更作用域选择验证范围，并给作业显式预算；手动派发不得绕过门禁**（openclaw CI 面：ci/scope-and-routing、job-budgets、manual-dispatches）：changed-scope detection 决定哪些 lane 该跑；作业带 UI 分片、并发与作业预算、lint 内存策略、sticky-disk 键；手动派发有 release-gate 回退与 Windows Testbox 检查。规则：① 不要每次都全量验证，按改动的影响面选验证 lane，并定期用全量检查漂移；② 并发数 / 内存 / 磁盘键要写成显式预算，不是"跑起来再说"；③ 手动触发只能改变选择，不能绕过门禁。

判非（本轮核实）：make/exponential-backoff 与 automatic-retry 同一方法 family，并入 wb-debug-loop r597 第 10 点（错误类型白名单 + 退避序列表）；make/incomplete-executions（失败现场默认关闭且有配额）落 wb-debug-loop 第 9 点；openclaw automation delivery 三模式 + 失败告警与 r594C「告警自身失败三态」重叠 >60%。

## r598A（2026-10-16 · GitHub 20 仓 issues · wb-release-maintain 1.165.0）

1. **遗留对象缺字段时用计划值兜底并记录，不要每轮运行都失败**（openclaw/openclaw#173509）：cron 对没有 account 字段的历史自动化，每轮都取不到而整轮失败。规则：迁移期的兼容分支要能把缺失字段补成"计划值 + 已记录"，让任务继续跑；持续失败且不可自愈的兼容问题，优先级高于正确性洁癖。
2. **凭据读取推迟到首次使用，禁止在导入期做**（crewAIInc/crewAI#8116）：模块导入时就读 auth token，导入期无凭据或已过期会直接拖垮启动。规则：凭据/连接类资源的获取放在首次调用点，导入期只允许持有获取函数；副作用（读盘、联网、取令牌）不进模块顶层。
3. **所有出站路径都要走声明的代理，不允许旁路**（crewAIInc/crewAI#8116 同族 · FlowiseAI/Flowise#6542）：AMP 请求、OpenAI 调用各走各的，环境里声明的代理只在部分路径生效。规则：新增任何出站通道时，与既有通道共用同一个代理解析点；"某个库自己发请求"是旁路高发区，要显式接回。
4. **声明的依赖下限必须实测验证**（langchain-ai/langgraph#9320）：`get_input_jsonschema()` 在声明支持的最低 pydantic 版本（>=2.7.4）上就失败。规则：package.json / pyproject 里写的 floor 是声明不是结论，CI 要在 floor 版本上真跑一遍；声明与实测不符时改声明或改代码，不能只留声明。
5. **变量/凭据过期要做成事件并配处理器，不能等用到才失败**（windmill-labs/windmill#10837）：新增"变量值过期时触发 workspace handler"。规则：有有效期的资源（凭据、令牌、缓存键、租约）都要有过期事件与处理入口；只在读取点抛错，意味着失效总是以运行时故障的形式暴露。

判非（本轮核实）：langflow#15789（升级后恢复引导）与既有「破坏性版本机检升级步骤」同族；prefect#23171（线程先于取消域停止）为实现顺序细节；openclaw#141004（记录运行时技能使用）与既有「审计主体=真实执行者」重叠 >60%；#173545（共享系统提示前缀）为性能优化；#150446（投射视图排除内部 URI）属暴露面（自留地）；activepieces#16483（worker 组）、windmill#11780（进程外执行）为基础设施；openai-agents#5369（移除 provider）与既有「清理被拒替代路径」同族。

## r598B（2026-10-16 · arXiv 八轨 450 条 · wb-release-maintain 1.166.0）

1. **换模型会把旧模型的行为习惯一起带过去，切换必须做行为回归**（arXiv 2610.19712）：多会话 agent 为平衡效果与成本切换 LLM 时，需要把历史转移给新模型以保连续；实验发现 recipient 会出现 behavior transfer——沿用 donor 的行为习惯。规则：模型切换的迁移项不止上下文格式与工具契约，还有行为风格（啰嗦度、停止时机、纠错方式）；切换后除了功能回归，还要跑一组行为回归样例，并接受"切换后短期内行为不纯"这一事实。

判非（本轮核实）：2610.17374（修漏洞依赖要保持构建与测试绿）与既有「破坏性版本机检升级步骤」同族；2610.19822（多模型服务显存）为基础设施；2610.20243 / 2610.20191 为特定域。

## r598C（2026-10-16 · 站点 24 站 20 个 200 · wb-release-maintain 1.167.0）

1. **引用外部规范必须钉住版本切片**（modelcontextprotocol.io/llms.txt 50,288B 实拉）：MCP 文档全部按日期版本路径组织（`docs/2026-07-28/...`），索引页本身就带版本前缀。规则：引用外部规范/API 文档时把版本（日期或版本号）写进引用本身；不钉版本等于允许上游改动悄悄改写我们的契约，出问题时也无法回溯当时依据的是哪一版。

判非（本轮核实）：mastra「模型 ID 不得改」落 sa；skillstore 审计状态落 ssc；n8n llms.txt 本轮由 287,833B 变为 1,160B 索引壳（信源形态登记，非独点）。

## r599C（2026-10-16 · 站点 modelcontextprotocol.io/learn/versioning.md 一手 curl 200 实拉 · wb-release-maintain 1.168.0）

1. **协议版本用「最后向后不兼容变更日」日期戳而非语义版本递增；向后兼容的更新不 bump 版本号**（modelcontextprotocol.io/learn/versioning.md）：MCP 协议版本字符串格式为 `YYYY-MM-DD`，只在发生向后不兼容变更时才推进，兼容更新（含新增能力）一律不递增，以保互操作。规则：① 对外契约用「最后破坏性日」作版本锚，比语义版本更直白地表达「我何时改坏过你」；② 兼容性判定优先于版本号——能增量改进就不 bump，避免无谓的升级惊动。提升层：工作流/治理（版本契约）。触发词：日期戳协议版本、兼容更新不 bump、YYYY-MM-DD 版本锚、向后兼容保留。
2. **特性/规范项有三态（Draft/Current/Final）+ 弃用须至少保留 12 个月或 90 天加急移除，且必须给迁移路径**（modelcontextprotocol.io/learn/versioning.md）：Deprecated 项仍属规范但排定移除，至少留 12 个月（或按加急移除例外留 90 天）才真正删，且必须文档化迁移路径（或声明无需迁移）。规则：弃用不是「随时可删」——给下游留出可被机器/人检到的保留窗 + 明确迁移指引，与既有「弃用=带 removeAfter 日期的登记项」互补：本条补「最短保留时长」下限，那条补「无日期无删除资格」的硬门槛。提升层：工作流/治理（弃用生命周期）。触发词：弃用 12 个月保留、90 天加急移除、迁移路径强制、特性三态。

判非（本轮核实）：mcp architecture「协议只定义上下文交换契约、不规定 LLM 使用方式」为通用架构原则无方法增量；mastra「模型 ID 不得改」已落 sa；skillhub 分数面仍为 SPA 壳无判据；agentskills/specification 与 n8n llms.txt 本轮无新方法增量（r598C 已落）。

## r601A · 退役通告须「温和期+与消费方清单联动」：calm notices 列出替代 API 与最终兼容日，断崖式废弃致下游静默坏（来源：api.github.com/repos/openclaw/clawhub/pulls/3962 merged 2026-10-15 一手逐串命中 `show calm API retirement notices` / `lists replacement APIs in expandable details` / `adds an "API update" item to the publisher dashboard` / `preserves deprecatedApi, replacement, and removeAfter` / `The date is inclusive`，2026-10-16 gh api 核验；与 §r322B 日落登记资格化 互补——那条管登记资格与时点载体，本条管通告形态×清单联动）
- **判据**：① 自家接口退役 = 温和期通告 + 替代 API 明示 + 最终兼容日（inclusive，最后一天仍可用），不是直接断供；② 通告与消费方清单联动——「谁还在用旧 API」一目了然，通告才能精准投放；③ 结构化字段（deprecatedApi/replacement/removeAfter）与散文说明并存——只有散文的通告不可枚举、不可机检；④ 发布者仪表盘挂「API update」项——通告是发布流程的一部分，不是事后补救。提升层：工作流（退役工序）。触发词：退役温和通告、calm retirement notices、removeAfter inclusive、替代 API 明示、消费方清单联动、发布者仪表盘。
