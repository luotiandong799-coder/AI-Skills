---
name: wb-release-maintain
description: >-
  仓库发布与依赖维护（合并 Claude Code 自动化 Skill 的 Changelog Miner、Release Notes、Dependency Guard 三个能力：从代码改动找关键变更补遗漏、从 diff 提炼用户可读的更新说明、升级依赖前先看破坏面）。当需要为仓库写更新说明/发布说明、梳理一段改动里哪些是关键变更哪些有遗漏风险、升级依赖前评估影响范围时使用。不用于日常 git 操作（走 github skill / gh CLI）、不用于排障（走 wb-debug-loop）。、输入集版本化、评测集版本、复现门票、未版本化不许续、增量版本、旧引用钉旧版、兼容面判定、存量自动升级、新老行为并存、版本区间声明、特性声明单一来源、轻量版本化、发布态语义、草稿发布不可变快照、回滚重发旧版、提升扇出、停用挡在用
version: "1.75.0"
agent_created: true
sources:
  - Claude Code 自动化 Skill 清单（Changelog Miner + Release Notes + Dependency Guard，用户提供文章 2026-09-17）
---

# wb-release-maintain（发布维护：改动要讲人话，升级要先看破坏面）

## 核心原则

**发布说明写给用户看，不是写给代码看**。从 diff 里提炼的是"用户感知到的变化"，不是文件列表；**升级依赖前先算破坏面**，不拍脑袋升级。

## 一、Release Notes：从 diff 提炼用户可读的更新说明

1. **取改动范围**：git log 最近一段（如 `git log --oneline -20`）或指定版本区间，列出提交清单。
2. **按提交逐个提炼**：每个提交问三个问题——
   - 用户会感知到什么？（新功能/修复/性能/行为变化）
   - 有没有破坏性变更？（接口/格式/默认值/删除项）
   - 一句话怎么说人话？
3. **分类整理**：新功能 / 修复 / 改进 / 破坏性变更（放最前标注⚠️）/ 其他。
4. **写人话**：不用代码术语堆砌，每条以"现在可以…/修复了…/提升了…"开头；破坏性变更必须写清"升级前要改什么"。

## 二、Changelog Miner：找关键改动，补遗漏风险

1. **diff 里找高信号区域**：新增/删除函数签名、配置项、环境变量、依赖版本、数据格式、对外接口——这些最容易产生遗漏风险。
2. **对照 changelog 找缺口**：已有 changelog 时，逐条核对提交是否都覆盖；缺失的提交按影响判断补不补。
3. **标注风险级**：
   - 🔴 破坏性/涉及对外契约（接口、格式、权限、依赖大版本）
   - 🟡 行为变化（默认值、边界、报错方式）
   - 🟢 无感改动（重构、注释、内部实现）
4. **重点查"悄悄改掉的东西"**：删除的配置、废弃的选项、改名的字段——diff 里不明显但用户会踩。

## 三、Dependency Guard：升级依赖前先看破坏面

升级依赖前按序检查，**先看后升，破坏面不清晰就不升**：

1. **查升级跨度**：当前版本 → 目标版本跨了几个大版本？大版本升级（major）默认破坏性变更，先读升级指南/迁移文档。
2. **查依赖树**：目标包的依赖是否变了（新增传递依赖、Python 版本要求、Node 版本要求、系统库）——`pip show` / `npm view` / `gh api` 或包管理器依赖树命令。
3. **查破坏性变更清单**：目标包 release notes / migration guide 里列出的 breaking changes，逐条对照本项目用没用受影响 API。
4. **查使用面**：仓库里哪些文件 import/require 了这个包（grep 包名），每个使用点核对是否受影响。
5. **判定**：
   - 破坏面小（无受影响 API）→ 可升
   - 破坏面中（少数使用点受影响）→ 升 + 逐个修 + 回归测试
   - 破坏面大或迁移文档缺失 → **不升**，记原因，等补丁版或迁移就绪
6. **升级后必回归**：跑测试/构建/关键路径，验证"升级本身没引入问题"——参考 wb-debug-loop 的修复验证纪律。

## 四、发布态语义：草稿/发布不可变快照与提升安全
（来源：Activepieces `flows/versioning.md` + `about/changelog.md`，2026-09-30 实拉）

1. **发布态=不可变只读快照，草稿=可变工作副本**：已发布版本一经发布即锁定、不可改；任何修改都先生成新的草稿（从已发布版复制），已发布版不被触碰。线上跑的永远是「某个已发布快照」，编辑中的永远是「草稿」——两者解耦，编辑永不污染线上。
2. **回滚=重发旧快照，不是「删掉新版」**：要回到旧行为，把某一历史已发布版重新发布为新发布态即可；旧版本始终保留、可随时重发，回滚因此是无损、可逆的一等公民操作，不依赖「撤销提交」或「删除最新版」。
3. **提升（发布）自动扇出到下游**：被引用的构件（如 agent）发布后，所有已引用它的下游（flow）在下次运行即生效，无需各下游手动重发——提升是「推广播」，不是「等各消费者手动拉」。
4. **停用/删除必须挡在用或显式声明受影响面**：仍在被已发布流程引用的构件不可直接删除/移动（删除前须先暴露其波及的下游清单）；「删除」操作要诚实列出后果，而不是静默留孤儿。

## 备份必须显式列举「不含什么」；恢复有身份前置且默认不改变运行态（来源：docs.n8n.io/deploy/host-n8n/keep-n8n-running/backup-and-restore.md 8,397B，2026-09-30 r338B 独立实拉）

1. **备份的覆盖面要按「缺什么」声明，且够不够用按恢复目标分档**：官方写明 CLI `--backup` 只导出 workflows + credentials，**不含四类**——用户与角色、执行历史与日志、变量、实例设置（含凭据加密密钥）。结论是同一份备份「迁移工作流够用、恢复整实例不够用」。判据：**任何备份方案必须输出一张「不含清单」**，并写明它够支撑哪一类恢复目标；只说「我备份了」等于没说恢复了什么。
2. **恢复的前置是身份面已重建，且恢复顺序会决定所有权归属**：导入命令需要实例上已有用户、导入的凭证需要 owner；全新实例会重新出现 owner 设置页，**第一个完成设置的人成为 owner**。判据：恢复动作不是纯数据搬运——**谁先完成身份初始化，谁就拿到所有权**；恢复演练必须把「身份与权限重建」排在「数据导入」之前。
3. **恢复默认停用，「连激活态一起恢复」是带前置条件的独立开关**：导出保留原 ID ⇒ 目标端同 ID 项被静默覆盖；导入的工作流默认 **deactivated**，要恢复导出时的开启状态须传 `--activeState=fromJson`，而该开关**仅在 queue / multi-main 模式可用**。判据：**恢复不应顺带把系统推回运行态**——「恢复数据」与「恢复运行」是两个动作，后者还要单独满足运行模式的条件。

## 判定纪律

- **用户可读 ≠ 代码术语**：写不出人话的条目要么没提炼到位，要么这条对用户无感（删掉）。
- **破坏性变更永远放最前并加 ⚠️**：用户最怕升级后悄悄坏掉。
- **依赖升级是待验证假设**：升级完成 ≠ 升级成功，必须回归测试通过才算。
- **不越权**：本技能负责"提炼/评估/建议"，实际升级动作与改动以用户指令为准。

## 孤儿回收是独立阶段，不是 cleanup 的副产品：调度器须单列 orphan 回收且各计时面彼此独立（来源：docs.n8n.io/configure-n8n/durable-scheduler.md、.../environment-variables/scheduler.md、docs.openclaw.ai/automation/cron-jobs/how-it-works，2026-10-01 r362-Q-C 实拉；落在 WB r326B 指定可继续挖方向①「谁负责删、谁负责留」）
- 判据：① n8n durable-scheduler 五阶段 `plan / dispatch / crash-recovery / cleanup / orphan`（orphan 单列），多 main 靠 claim 无 leader，保证等级 at-least-once："not that it runs only once"；整套 `N8N_SCHEDULER_ENABLED` 默认关闭、`TRIGGER_NODE_MODE=legacy`。② 计时面彼此独立：executor 5s / materialization 10s / reaper 30s / retention 3600s / owner-reconcile 900s，保留期 failed 604800 / quarantine 86400 / grace 上限 30 天。③ openclaw cron 重启时 coalesces missed ticks、按存量 deadline + run receipts 重查、**逾期延期而非立即补跑**，去重靠"同 ID 运行中则拒绝并发"。⇒ "孤儿回收"是专职阶段而非 cleanup 的副产品。
- 提升层：工作流。触发词：orphan 独立回收阶段、at-least-once 非 exactly-once、计时面独立、逾期延期非补跑、N8N_SCHEDULER_ENABLED 默认关。

## 学习轮沉淀区（本段）
（r历史 起的连续学习轮章节共 262 章已下沉 references/knowledge-base.md §≤200迁移，正文留此指针）


## 环境间提升必须单向；删除不随拉取传播；跨环境只搬「形状」不搬「秘密」（来源：docs.n8n.io `/administer/use-source-control-and-environments/push-and-pull-changes.md` 12,333B + move-work-between-environments 4,207B + understand-source-control 1,929B，2026-10-01 r339B 独立 curl 实拉逐串命中）
- **原文**：①「work goes in one direction: **either to Git, or from Git, but not both**」（同一实例又推又拉官方明确不推荐）；②「When workflows, credentials, variables, tags, and data tables are **deleted from the repository**, your local versions of these resources **aren't deleted automatically**. … n8n notifies you about any **outdated resources** and asks if you'd like to delete them」；③「**Credential stubs** - name and type. Any other fields are included only if they are expressions.」「When the changes include new variable or credential stubs, n8n notifies you that you need to **populate the values for the items before using them**」；④「n8n **syncs data table schemas** … **Row data isn't synced.**」；⑤「**Workflow and credential owner may change on pull**」——按项目名匹配，无匹配则新建项目并把当前用户设为 owner；⑥「If you have more than one Git branch, you need to **merge the branches in your Git provider** to copy work between environments. **You can't copy work directly between environments in n8n.**」
- **判据**：① **提升（promotion）链路要设计成单向**：源环境只推、目标环境只拉。同一节点双向同步会把「谁是最新的」变成运行时问题，官方宁可劝退也不做合并策略。⇒ 设计环境同步前先回答方向，方向不定就不该上线同步。② **删除是唯一不自动传播的动作**：仓库里删了，本地仍在，只会被标为 outdated 并等你确认。⇒ 「删了怎么还没生效」是预期行为；反过来说，**任何声称「同步」的通道都必须逐类声明删除是否传播**——不声明就是埋雷。③ **跨环境只同步形状，不同步秘密值**：凭据只走 name+type 的 stub，真实值由目标环境自备。⇒ 这既是安全边界（秘密不跨环境漂移）也是可用性约束（新 stub 未填值即不可用，必须在**使用前**阻塞而不是运行时才炸）。④ **schema 与 row 的同步策略必须分开声明**：结构同步、数据不同步，是默认且合理的——把两者绑成「全量同步」会让一次结构变更带走/覆盖生产数据。⑤ **跨环境迁移会改写归属**：owner 可能在新实例上被重指派。⇒ 迁移验收清单里必须有「权限/归属是否被改」这一项，否则迁移完成但责任人对不上。⑥ **环境间的"复制"要借道 Git 的合并能力，不要在应用内复制**：应用提供 push/pull 两端，合并语义交给真正的版本系统。
- **提升层**：工作流/发布治理。触发词：单向提升、one direction、删除不传播、outdated resources、credential stub、值缺失阻塞使用、schema 同步 row 不同步、owner 在 pull 时变更、跨环境不直接复制。

## 冻结位、改名断链防护、去重合并都必须是发布面的显式动作：本地安装态可被钉死，且重命名/合并不破旧链（来源：github.com/openclaw/clawhub README 8,522B（9,474★）+ Activepieces piece-syncing + Pipedream CLI 版本闸，2026-10-01 r348A 独立 curl 实拉）
- 原文：①「Pin local skill installs so updates and force reinstalls cannot overwrite frozen copies.」②「Rename an owned skill without breaking old links or installs.」③「Merge duplicate owned skills into one canonical slug.」④第二证：AP「Each step is pinned to an exact version」/「Flows never auto-upgrade」/「The pin stays until a human changes it」。⑤第三证：Pipedream「If you fail to update the version, the CLI will throw an error」+ account 级 `key` 全局唯一。
- 判据：① **「冻结」要落在安装态而不是版本号**：钉住本地副本，使 update 与 force reinstall 都覆盖不了它。⇒ 只靠记住版本号来复现是不够的 —— 真正的冻结位必须能挡住强制重装这条最宽的通道。② **重命名与合并必须保旧链**：合并到 canonical slug 后旧链接仍可用，否则每次治理都在制造一批死链（表现为用户报 404，而不是合并成功）。③ **版本未 bump 要在构建期拦下**：CLI 直接抛错而不是放行后靠人巡检。⇒ 发布面三件套 = 冻结位、断链防护、构建期版本闸，缺一件就只能靠约定。
- 提升层：工作流。触发词：pin 冻结本地安装、force reinstall 不可覆盖、rename 不断旧链、merge canonical slug、版本未 bump 构建期抛错。

## 增量扫描的哈希键必须含规则集版本；豁免到期必须显式「回到扫描面」（来源：github.com/tech-leads-club/agent-skills SECURITY.md 16,248B，2026-10-01 r348B 独立 curl 实拉取 base64 解码）
- 原文：①「Each installed skill records a SHA-256 content hash computed from all its files」+ 缓存 `.security-scan-cache.json`；「hash unchanged → load from cache (fast, no re-scan)」「hash changed → re-scan」。②「`expiresAt: '2027-01-01'` # Optional but strongly recommended」。
- 判据：① **只按文件内容哈希做增量扫描有一个隐含缺口：规则升级但文件未变 ⇒ 老结论永久有效**。⇒ 哈希键必须同时含「扫描器版本/规则集版本」，否则规则更新后存量包永远不会被重扫——这是增量扫描最常见的静默漏报。② **到期不等于恢复可见**：豁免条目必须有到期日（原文强推荐），且到期后要显式把该文件重新纳入扫描面。⇒ 「豁免表必须有到期」只写了一半；缺了后半句，到期与永久豁免在行为上没有区别。
- 提升层：工作流。触发词：内容哈希增量扫描、哈希键含规则集版本、规则升级不重扫、expiresAt 到期、回到扫描面。

## 市场侧准入是四级闸：命名空间内可见 ≠ 全局可见，晋升为显式一级动作（来源：github.com/iflytek/skillhub README 38,482B，2026-10-01 r348B 独立 curl 实拉取 base64 解码）
- 原文：「Namespaces — Organize skills under team or global scopes」「namespace has its own members, roles (Owner / Admin / …)」「promotions to the global scope. Governance」。
- 判据：① **域内可用与全局可见是两个状态，中间那一步（晋升）必须是显式动作并留痕**。⇒ 把「通过审核」直接等同于「所有人可搜到」，等于把治理决定隐式化；发布面要给晋升单独一个闸，而不是在域内验证的同一格里打勾。② **准入按格式封闭枚举**（扩展名/包型白名单）而不是事后过滤。⇒ 白名单的作用是「不接受未知形态」，与「扫描是不是干净」是两个不同的门。③ **初始凭据强度不足即拒绝**：弱 bootstrap 凭据应阻断而非告警——告警会被批量忽略，而初始凭据正是最容易被长期沿用的那一批。
- 提升层：工具/工作流。触发词：namespace 作用域、全局晋升闸、扩展名白名单、弱 bootstrap 凭据拒绝、域内可见不等于全局可见。

## 持久小存储的「结构演进作用域」与「删除可逆性」必须写进契约：改结构只作用新数据，删记录无回滚位（来源：help.make.com/l6du-data-stores.md 28,223B，2026-10-01 r349A 独立 curl 实拉，`apply only to the new data` / `You cannot roll back deleted records.` 逐串命中；经 Qoder r366-Q-A 提名）
- 原文：①「The changes to the data store structure **apply only to the new data** you put in the data store. Make doesn't change or validate the original data to fit the updated structure.」②「**You cannot roll back deleted records.**」（恢复只能手工从历史 run 日志提取）。
- 判据：① **结构变更不回溯＝库内静默双 schema**：改完结构后新旧记录各按自己形态存在，系统不校验也不转换 ⇒ 读侧必须自己知道「这条是旧结构的」，否则字段缺失会被当成数据问题而不是结构问题。② **删除无回滚位必须明写**：有 migration / rollback 的假设在轻量 store 上根本不成立，误以为可回滚就会把「删除」当可逆操作用。③ 与既有「schema 与 row 同步策略分开声明」互补：那条管跨环境搬运，本条管**同库内的时间维演进**。
- 提升层：工具/工作流。触发词：结构变更只作用新数据、库内双 schema、删除不可回滚、恢复靠历史 run 日志、持久小 store 契约。

## 生命周期钩子要按「触发次数」分档（deploy 型一次 / activate 型每次），撤除是「先停用后删除」两步（来源：pipedream.com/docs/components/contributing/api.md 55,159B + sources-quickstart.md 22,817B，2026-10-01 r349B 独立 curl 实拉，`each time a component is deployed` / `each time a component is deployed or updated` / `Executed each time a component is deactivated` 逐串命中；经 Qoder r367-Q-B 提名）
- 原文：deploy 钩子「each time a component is **deployed**」；activate 钩子「each time a component is **deployed or updated**」；另有 `deactivate`「Executed each time a component is deactivated」。
- 判据：① **幂等设计前先问该钩子会不会随更新重跑**：deploy 型只跑一次、activate 型每次更新都跑——把初始化写进 activate 型钩子，等于每次发版重放一遍。② **撤除是两步且补偿要落在第一步**：先 deactivate 再 delete；删除前的停用才是可逆的那一步，直接删没有补偿位。③ 与既有「卸载残留态 tombstone」互补：那条讲卸载后的可见性，本条讲**钩子触发次数语义**。「调度是运行期状态、不随代码回滚」本轮未独立取到原文，登记待复核。
- 提升层：工作流。触发词：deploy 型钩子、activate 型每次更新、钩子触发次数分档、先停用后删除、补偿落第一步。

## 换鉴权机制的传播半径包含存量会话；身份主语的字符集约束是防碰撞设计，不是风格（来源：help.make.com/single-sign-on.md 14,821B + manage-connection-and-key-usage-notifications.md 2,598B，2026-10-01 r349B 独立 curl 实拉，`logged out immediately` / `lowercase characters and dashes` / `adds one of your keys or connections to a scenario` / `enabled by default` 逐串命中；经 Qoder r367-Q-B 提名）
- 原文：①切换 SSO「You will be **logged out immediately**」；②「Namespace must include only **lowercase characters and dashes**」；③他人「**adds one of your keys or connections to a scenario**」触发通知，且该通知 `enabled by default`。
- 判据：① **鉴权面切换会让所有在场会话立刻失效** ⇒ 发布计划必须计入「在场重登成本」，否则一次配置变更表现为大面积掉线事故。② **身份主语（namespace/域名）做字符集规范化是防碰撞**：大小写与分隔符自由会把同一实体拆成两个账号，且合并成本远高于当初约束。③ **「别人用了我的凭据」默认开通知**：凭据归属者天然是第一告警受众 ⇒ 这类事件默认关闭才需要显式申报（与「默认公开无鉴权」的判据方向相反，别混用）。
- 提升层：工作流。触发词：切换 SSO 立即登出、存量会话失效、namespace 字符集、身份防碰撞、凭据被他人使用默认开通知。

## 热重载能力必须声明边界：读者用「最后成功快照」、语法错误整份拒收、debounce 不可调、不可热更字段成清单（来源：docs.openclaw.ai/gateway/configuration/hot-reload.md 33,314B，2026-10-01 r349C 独立 curl 实拉，`last successfully applied` / `debounce window` / `rejected` 逐串命中；经 Qoder r368-Q-C 提名）
- 原文：①替换事务提交前读者持续读「**last successfully applied**」快照；②语法错误「**rejected** before persistence」，整份拒收且不覆盖在役配置；③`debounce window` 不可配（防调成竞态窗口）。
- 判据：① **热重载的可见性边界要先声明**：读者在事务提交前一直读旧快照 ⇒ 「改了没立刻生效」不必然是故障，可能是尚未提交；不声明这一点，排障会把正常延迟当 bug。② **语法错误整份拒收而非部分应用**：保证在役配置不被半份覆盖，代价是「一处错、全份不生效」——这个代价必须写进文档，否则会被当成「改了很多只有一处生效」。③ **不可配的项要显式点名**（debounce、port/bind/auth/TLS 类不可热更字段）：把「不是所有字段都能热更」说成默认全部可热更，是最常见的越界来源。
- 提升层：工作流。触发词：热重载边界、最后成功快照、语法错误整份拒收、debounce 不可配、不可热更字段清单。

## 破坏性变更注记要固定两段式并标注迁移类别：只写「改了什么」等于没写（来源：www.activepieces.com/docs/install/reference/breaking-changes.md 82,191B，2026-10-01 r349C 独立 curl 实拉，`What you need to do` ×N / `migration only adds columns and leaves the existing ones in place` 逐串命中；经 Qoder r368-Q-C 提名）
- 原文：条目固定两段「What changed / **What you need to do**」（全页逐条重复）；迁移说明「migration only adds columns and **leaves the existing ones in place**」。
- 判据：① **两段式是硬要求**：「改了什么」是事实陈述，「你要做什么」才是可执行动作；只有前者的变更日志，读者仍需自己推断是否需要动作 ⇒ 升级事故多出在这一段缺失。② **迁移要写明是加列还是改列**：只加列并保留旧列，意味着旧代码短期仍能读；改列则不是。不区分就无法判断「能不能先升级代码再升级数据」。③ 与既有「迁移三字段 CI 闸 breaking/release/down()」互补：那条闸**声明在场**，本条闸**注记内容形态**。
- 提升层：工作流。触发词：What changed / What you need to do、破坏性变更两段式、迁移只加列不改列、升级注记形态。

## r350A · 订阅面：族订阅不是通配，未知键仍注册成功 → 必须有告警面（来源：docs.openclaw.ai/automation/hooks/event-types，2026-10-02 r350A 实拉 224,709B）

- **★订阅有"精确键"和"族"两档，族不等于通配**：可订阅精确键（如 `command:*` 下的具体动作）或裸族（`command`/`session`/`agent`/`gateway`/`message`），族订阅收到该族全部动作；但 **`session:compact` 既不是族也不是通配**——要拿到压缩事件必须显式订阅两个精确 compaction 键。判据：**形如 `a:b` 的中间节点默认不是通配**，别假设订阅了父级就能收到子事件。
- **★未知订阅（如拼错的 `command:nwe`）仍会被注册成功**，只是 loader 告警、`hooks info` 会报出来。判据：**注册成功 ≠ 语义有效**；事件系统必须提供"已注册但无对应事件"的查询面，否则拼写错误是静默失效。
- 发布检查项：新增/改名事件键时，同步核对订阅清单里是否出现旧键与新键并存（双注册会重复触发），并跑一遍"已注册但零命中"清单。
- 提升层：工作流 / 工具。

## r351A · 同步通道：传输的是"保存态"不是"发布态"，且冲突自动解的覆盖面≠你以为的覆盖面（来源：docs.n8n.io `administer/use-source-control-and-environments/push-and-pull-changes.md` 12,333B + `understand-source-control.md` 1,929B，2026-10-02 r351A 独立 curl 实拉逐串命中）

- **★同步通道搬运哪一态必须先说清**：原文 "n8n pushes the **current saved version, not the published version**, of the workflow. You need to then separately publish versions on the remote server."；反向同理——拉取一个已发布的工作流时 "n8n **unpublishes** the workflow while pulling, then **republishes** it. This may result in a **few seconds of downtime**"。判据：**发布态是独立于工作态的一层**，同步通道默认只搬工作态；误以为"同步=同步发布"会导致远端停在旧版本，或拉取动作造成生产短中断。
- **★"能自动解冲突"是有适用对象的，不是全局能力**：原文 "n8n's implementation of source control is opinionated. It **resolves merge conflicts for credentials and variables automatically**. n8n **can't detect conflicts on workflows**."（另处 "Credentials and variables can't have merge issues, as n8n chooses the version to keep"）。判据：把"系统帮我解冲突"当成系统级承诺是错的——**自动解只覆盖无结构歧义的资源（凭据/变量），有结构的工作流恰恰完全不检测**。写同步方案时必须逐类列明哪类自动、哪类不管。
- **★删除默认不级联，但"按名匹配"会把身份悄悄合流**：仓库侧删掉的资源 "aren't deleted automatically"，只在 pull 时提示确认；然而数据表是例外——"If a data table exists locally but not in Git, **pulling deletes it, including all its row data**"，且 force pull（API/自动化）"delete the table **without asking**"；同名重建则 "n8n treats it as the same table: it **reconciles the local table's ID to the incoming one**"。判据：**"不级联删除"的默认只保护交互式路径，自动路径绕过确认**；且**匹配键是名字不是 ID** 时，删除-重建会被识别为同一对象，本地 ID 被改写。
- **★同步方向的权限是非对称的**："Instance owners and instance admins can **push** changes to and **pull** changes from the connected repository. **Project admins can push changes... They can't pull**." 判据：授予"可写"不等于授予"可读回"；把双向同步权限当成一个开关配置，会让只能推的一方以为自己也能拉。
- 发布检查项：① 同步脚本末尾是否显式发布（别假设 push 会带发布）；② 冲突检测能力按资源类型逐类声明，别写笼统的"自动合并"；③ 自动化 pull 一律视为 force 路径，先列将被删除的对象再执行；④ 同步凭据只有 push 权时，方案里不能出现 pull 步骤。
- 提升层：工作流 / 可复用 Skill。触发词：saved 而非 published、同步通道发布态、自动解冲突覆盖面、删除不级联、force pull、按名匹配身份合流、只能推不能拉。

## r352C · 验证并发的两条纪律：取消还是排队看消费者对 HEAD 的绑定；并发是预算不是能力（来源：docs.openclaw.ai `ci/pipeline` 79,609B + `ci/capacity` 95,474B，2026-10-02 r352C 独立 curl 实拉逐串命中；与 §r350A 订阅面 互补——那条管事件覆盖面，本条管验证资源的调度与配额）

- **★取消 vs 排队由"消费者认不认 HEAD"决定，不是一刀切**：原文 canonical main 用 **run-number 奇偶两槽**，"Each slot is **non-canceling** and keeps one **coalesced pending tip**: a new merge **replaces** that slot's older pending run instead of canceling work that already registered"；两槽可乱序完成，而 "exact-head consumers remain **bound to their requested SHA** and are unaffected"；反过来 "Pull requests still **cancel superseded heads**"、manual dispatch 用隔离组；草稿事件在门禁前用**逐 run 隔离组**，"a delayed draft event cannot displace pending or running ready-for-review CI"。判据：**只认最新结果的作业可以取消旧运行（PR），绑定具体提交/产物的作业必须排队不取消（exact-head）**；给两者套同一套取消策略，前者浪费资源、后者丢证据。延迟到达的低优先事件要单独隔离，否则会顶掉高优先的在途验证。
- **★省资源的智能裁剪必须能被显式关掉，且降级 fallback 不许扩张范围**：原文 `preflight` "classifies the diff and **turns expensive lanes off** when only unrelated areas changed"；而 "Ordinary manual `workflow_dispatch` runs **intentionally bypass smart scoping and fan out the full graph** for release candidates and broad validation"；"Exact-head `release_gate` fallbacks **retain the pull request's** macOS, iOS smoke, and native generated-locale scope **instead of forcing unrelated** Apple lanes or locale parity"。判据：**发布候选走全量，日常变更走裁剪**——把裁剪设成不可绕过，等于让最需要全量验证的那次跑得最少；而自动降级（fallback）只许保持原范围，不许顺手扩张到无关车道。
- **★并发额度按"最坏情况占用"申请，稀缺资源留给真需要的作业，且别人的余量不算你的容量**：原文把 Blacksmith 标签当稀缺资源，"Jobs that only **route, notify, summarize, select shards**, or run short CodeQL scans should stay on GitHub-hosted runners unless they have measured Blacksmith-specific needs"；新增矩阵/并发/高频工作流 "must **show its worst-case registration count** and keep the org-level target below about **60% of the live bucket**"（10,000 桶 → 6,000 目标）；并点明 "This is **planned admission, not proof** that the provider supplies 130 runners simultaneously"、"its pooled reader's unused quota **does not establish organization-wide free capacity**"。判据：**扩容的论证材料是最坏情况数，不是平均值**；余量要留给重试/突发/邻近仓库；观测到别人没用满不构成自己可以加量的理由。
- 发布检查项：① 这条验证的消费者是 exact-head 还是 latest-wins（决定是否允许取消）；② 发布候选路径能否绕过裁剪跑全图；③ 新增加密/并发是否已报最坏情况注册数且组织级占用 <60%；④ 低优先延迟事件是否有独立隔离组。
- 提升层：工作流 / 工具。触发词：两槽流水线、non-canceling、coalesced pending tip、exact-head 绑定、草稿隔离组、智能裁剪、发布候选全量、fallback 不扩张、最坏情况注册数、60% 余量、别人余量不算容量。


## r353B · 日志配置热更存在 half-applied 窗口，轮转归档数是硬编码的（来源：docs.openclaw.ai `gateway/logging` 23,470B，2026-10-02 r353B 实拉）

- **★日志类配置热更对"下一条记录"生效，但已排队记录写回原文件**：`logging.level` / `logging.file` / `logging.maxFileBytes` 在开启配置热重载后 "apply to the **next log record**, including records from long-lived channel loggers"，同时 "**Queued records finish writing to their original file.**"。判据：**改日志路径后存在一个窗口期：新记录进新文件、旧记录还在写旧文件**——做日志归档/切割时要按"两个文件都可能被写"来处理，不能以为切换是原子的。
- **★轮转参数与保留份数是固定的**：活跃日志按 `logging.maxFileBytes`（默认 100 MB）轮转，"keeps up to **five** numbered archives (`.1` through `.5`)，and continues to write a fresh active file"。判据：**保留份数不可配 ⇒ 日志的历史深度有硬上限**，依赖长周期回溯的审计必须外送到独立存储，不能指望本地滚动文件。
- **★启动日志会声明解析后的默认值**：网关启动时打印 resolved default agent model 与影响新会话的模式默认值（`thinking` / `fast`），未设置时 `thinking` 显示 `medium`；若插件重载覆盖了启动加载，则"model line, loaded-plugin summary, and channel warnings **use the replacement configuration**"。判据：**启动日志是"最终生效配置"的取证点，不是配置文件的回显**——排查"配置没生效"先看这一行，且要意识到插件重载会改写它。
- 提升层：工具 / 工作流。触发词：日志热更、排队记录、轮转 5 份、启动日志解析默认值。


## r355A · 同一配置键在不同运行模式下语义不同：值不变而作用域漂移，回退条件必须显式写出（来源：docs.n8n.io `scaling/control-concurrency.md` 4,111B + `use-n8n-cloud/understand-concurrency.md` 3,828B 独立 curl 取 `.md` 原文，2026-10-02 r355A 实拉）

- **★同一个环境变量在两种模式下管的不是同一个东西**：`N8N_CONCURRENCY_PRODUCTION_LIMIT` 在 regular mode 下限制**整个实例**的生产并发；在 queue mode 下它决定**单个 worker** 能并行处理多少 job，原文 "Concurrency control in queue mode is a **separate mechanism** from concurrency control in regular mode, but the environment variable … controls **both** of them. In queue mode, n8n takes the limit from this variable **if set to a value other than `-1`**, falling back to the `--concurrency` flag or its default"。判据：**换运行模式时配置值不变、语义已变**——上队列模式 / 扩容 / 迁移的变更单里必须重算这个数的含义，不能直接沿用旧值；且**回退条件要显式写出**（-1 才回退到另一参数），否则"设了没生效"与"生效过头"都无法定位。
- 提升层：工作流 / 工具。触发词：配置语义漂移、运行模式、实例级与 worker 级、回退条件、并发上限迁移。


## r355C · 破坏性变更公告要带「迁移动作 + 时间点 + 不受影响面」；数据库只向前迁移 ⇒ 换载体等于空实例；被移除的配置是静默忽略，必须配存量自查（来源：docs.n8n.io `changelog/v30-breaking-changes.md` 21,374B 独立 curl 取 `.md` 原文，2026-10-02 r355C 实拉）

- **★破坏性变更公告的三件套缺一不可**：文档对每条都给「变更是什么 + **What to do** + 计划时点（scheduled for October 2026）」。判据：**只列变更不给迁移动作的公告不可执行**；没有时点的变更无法排期。⇒ 写升级说明时按「变更 / 动作 / 时点」三栏出，任一栏为空即视为未完成。
- **★要显式声明「不受影响面」，否则使用者会整体停用**：原文 "The remaining changes affect the `n8n-node dev` test loop **only**. `n8n-node build`, `n8n-node lint`, `n8n-node release`, and `npm create @n8n/node` are **unchanged**"。判据：**破坏性变更的影响面是双向声明**——说清哪些变了，也要说清哪些没变；只写变更面会让用户在没受影响的地方做无谓迁移。
- **★运行/部署形态本身是可被删除的兼容面**："Self-hosted n8n will require a **Docker-based deployment**. n8n 3.0 will no longer support installations run using `npm` or `npx n8n`"，且因 "n8n 3.0 doesn't publish a runnable `n8n` package to npm"，连开发用的 `n8n-node dev` 也改为跑容器。判据：**依赖登记不能只登记 API 与字段名**，安装/运行方式是同等重要的兼容面——它的移除会让一整类存量一次性失效，且迁移动作是"换部署"而非"改代码"。
- **★数据库只向前迁移 ⇒ 换镜像等于拿到空实例，旧数据不会跟过来**："Data from earlier versions **doesn't carry over**. Each `--n8n-image` gets its own volume, because n8n **only migrates a database forward**: switching images gives you an **empty instance** rather than a database an older n8n can't read"，并要求 "Export any test workflows you want to keep before you upgrade or change images"。判据：**迁移的单向性要写进升级单**——回滚到旧版本时库可能已不可读；换载体/换镜像前必须先导出，不能指望"数据跟着走"。
- **★被移除的配置项是"静默忽略"，所以必须配存量自查工具**：`N8N_PRE_EXECUTE_ERROR_CREATES_EXECUTION` 移除后 "After you upgrade, n8n **ignores the variable**"，官方给的应对是 "Check the n8n 3.0 **migration report** in Settings to see if **this instance** sets it"。判据：**删除一个配置不等于使用者会发现**——移除必须同时提供"我这台有没有中招"的自查入口；没有自查工具，静默忽略会把一次变更变成长期的行为谜题。
- 提升层：工作流 / 工具。触发词：破坏性变更公告、迁移动作、不受影响面、部署形态兼容面、数据库只向前迁移、换镜像空实例、静默忽略、迁移报告存量自查。

## r383A · 迁移工具的能力边界、兼容闸门极性、迁移收敛性、存量搁浅（来源：developers.make.com Module Migrator + difyctl + docs.langflow.org migration，2026-10-02 r373-Q-A / r374-Q-B 实拉；经 Qoder 提名）
- 迁移工具的「能力边界」= 引用可达性而非资产全集：只搬被引用的资源、未引用资源静默跳过；验收必须二次「全量清点 vs 已搬清单」对账，并把「工具自述边界」当需实测的声明。
- 兼容闸门按「谁更可能是错的一方」分向：低于下界硬停（exit 6 从不读缓存）、高于上界放行并告警、unknown 与 incompatible 同档处理；两个方向都要跑。
- 迁移不收敛条件：库里是否有别人的表（非 Langflow 表共库时 `--fix` 反复降级重放可能失败），须单实例启动 + 命名空间锁；回滚镜像与回滚数据是两个动作，预案必须成对写。

## r385A · 恢复契约必须切分责任边界并把重复面定位到唯一一处（来源：www.activepieces.com/docs/install/guarantees/crash-recovery.md 3,487B 独立 curl 取 .md 原文，2026-10-02 实拉；经 Qoder r385-Q-A 提名）
- **★容灾声明里的每个底座依赖都要标 owner，否则等于全保背书**：官方原文「**Redis durability is yours.** Queued runs live in Redis. A Redis that loses its dataset loses queued jobs — including async webhooks already acknowledged with a `200` — so use a managed Redis or enable persistence」。判据：**平台管的（已完成步不重跑、run log 检查点落 Postgres/S3、worker 无状态自动重排队）与用户自备的（Redis 持久性）必须在同一份声明里分列**；只写"我们保证不丢"而不写"哪部分不归我管"，是把底座故障悄悄算进自己的 SLA。
- **★at-least-once 的重复窗口要精确到"哪一步"，不能整包声明**：原文「**At-least-once, not exactly-once.** That in-flight step is the one place a replay can repeat work」，且「the interrupted step is **guaranteed not to repeat**」。判据：**重复可能性不是均匀铺在整条链路上**——已完成步复用记录输出、在飞那一步才可能重放。写幂等要求时只标这一处，别让下游为整条链路做去重而抬高成本；与 §r325A「异步暴露窗=已应答者不重试」分工：那条管**是否重试的判据**，本条管**重复可能性的空间定位**。
- **★"从不静默丢弃"是继承来的属性，不是自证的**：「Work is never silently dropped by Activepieces — the queue itself **inherits the durability of your Redis**」。判据：凡"绝不丢"类承诺，都要追到它的**继承源**；继承源的持久性一变，承诺等级随之变，声明里必须写上这个依赖名。
- 提升层：工作流 / 安全边界。触发词：恢复契约责任边界、Redis durability is yours、at-least-once 重复窗口、在飞那一步、承诺继承源、底座依赖标 owner。

## r385B · 审批门禁的覆盖面要做差集机检：差集里的对象不是「不受影响」，而是「改了立即生效」（来源：docs.n8n.io `build/manage-workflows/workflow-reviews.md` 10,012B 独立 curl 取 .md 原文，经 llms.txt 287,049B 定位，2026-10-02 实拉；经 Qoder r386-Q-A 提名）
- **★门禁只覆盖它能 diff 的东西，覆盖面必须显式做差集**：原文「A review covers the contents of one workflow: its **nodes and connections**, as captured in the pinned saved version. The visual diff and the approval **only apply to those contents**」，随后「A review **doesn't cover the resources the workflow depends on**. These **aren't part of the diff**, **aren't gated by approval**, and **apply to the published workflow as soon as you change them, even while a review is open**」——点名五类：Workflow settings（timezone / error workflow / execution order）、Credentials、Variables、Data tables、Sub-workflows。判据：**可变更对象集合 − 门禁实际 diff 的对象集合 ≠ 空 即为漏口**，而差集里的对象不是"不受影响"，恰恰相反——它们**绕过审批直接进生产**，比门内的对象更危险。设审批门禁时必须同时出「门内清单」与「门外清单」两张表。
- **★差集沿调用图传递，子对象各审各的不等于整体被审**：「Each sub-workflow is **its own workflow with its own review**, if any」。判据：**子资源的独立门禁不能替代主资源的覆盖声明**——"子工作流有自己的评审"是分散的覆盖，不是传递的覆盖；主流程批准时若子流程评审缺失或已过期，主流程的批准并不覆盖它。
- **★门禁的状态机要写清"挡什么"**：`Waiting for review` →「n8n **blocks publishing**」；`Changes requested` → 要求改后再提；且「A workflow can have **only one open review at a time**」，重提不会开新评审，须向既有评审提交新版本。判据：**"有审批"不等于"挡住了发布"**——只有明确写出被阻断的动作名（publish），门禁才是可验收的；与 §r385A「恢复契约责任边界」同族：那条管**承诺的负声明**，本条管**门禁的负声明**。
- 提升层：工作流 / 安全边界。触发词：门禁覆盖面差集、aren't gated by approval、门外清单、差集沿调用图传递、子工作流各有评审、Waiting for review 阻断 publish。

## 写入成功 ≠ 生效：发布是独立一步；降级发布分 stale / cold 两档，判据是「非密契约有没有变」（来源：docs.openclaw.ai/cli/secrets.md 16,115B，2026-10-03 r388C 独立实拉）
- **原文**：「A successful write reminds you to run `openclaw secrets reload` before a config-referenced value can take effect.」「re-resolves refs and atomically publishes the owner-aware runtime snapshot (no config writes)」「Eligible failed owners become **stale** only when their ref identities, provider definitions, and complete non-secret owner contract are unchanged. New or changed failures become **cold**. This degraded activation succeeds and reports `warningCount`. Strict or unmapped failures return an error and preserve the previously active snapshot.」
- **判据**：① **改值与生效是两次独立动作**——写库成功只代表"存下来了"，引用它的运行期仍是旧快照；发布（reload）才是原子切换点，且不改配置本身。发布流程里必须把"写完还剩一步"写进定义完成，否则出现"我改了但没生效"的伪故障。② **部分失败的降级不是一档而是两档**——失败方的引用标识、提供方定义、非密契约**全部未变**才算 stale（可带警告上线）；只要契约变了就是 cold（语义已经不是原来那个），两者处置完全不同，不能都用"降级上线"概括。③ **不可归类的失败必须保住旧快照**——strict / unmapped 失败直接报错并保留上一个可用快照，而不是带着未知状态上线；"先上再说"在这里等于把旧快照也弄丢。
- 提升层：工作流 / 可复用 Skill。触发词：写入≠生效、reload 是发布、stale vs cold、非密契约未变、保住旧快照、降级两档。


## 存储满时的取舍只有两档：停服或丢记录，没有第三选项；保留期与运行时长都是套餐属性（来源：help.make.com `errors-that-dont-create-incomplete-executions.md` 1,401B + `audit-logs.md` 8,460B，2026-10-03 r390C 独立 curl 取 `.md` 原文实拉；与 §破坏性变更公告三件套 互补）
- **原文**：「When your incomplete executions storage is full, Make checks the **enable data loss** setting: If the data loss is **disabled**, Make **disables the scenario**. If the data loss is **enabled**, Make keeps scheduling scenario runs and **discards the incomplete execution** if it cannot be stored」；「When the scenario runs longer than the **scenario run duration limit**. You can check the limit for your **plan**」；「Audit logs are stored for **12 months**.」
- **判据**：① **容量耗尽是一次显式的二选一，不是可以两全的配置**：要么停掉服务保住记录，要么继续服务丢掉记录。**"允许数据丢失"是一个业务开关不是技术细节**——它的默认值决定了这个系统在压力下的行为是"宁可停"还是"宁可丢"，必须在上线前明确选过。② **运行上限与保留期都是套餐属性**：时长上限按套餐定，审计日志只留 12 个月 ⇒ 做容量/合规承诺时不能按理想值写，要按当前套餐的实际值写，并在续费/换档时复核。③ **"记录被丢弃"要有可观测出口**：既然选了继续服务，就必须让用户能知道丢了多少、什么时候丢的，否则"丢了"和"没发生"在现象上一致。
- 提升层：工作流 / 工具。触发词：存储满二选一、enable data loss、停服 vs 丢记录、运行时长按套餐、审计保留 12 个月。


## 已发布版本是不可变对象；配额告警阈值随套餐分档；依赖的生命周期终止日期必须写进前置面（来源：www.activepieces.com/docs `flows/versioning.md` 1,323B + pipedream.com/docs `workflows/limits.md` 9,083B + `workflows/building-workflows/errors.md` 9,150B 顶部公告，2026-10-03 r391B 独立 curl 取 `.md` 原文实拉；与 §破坏性变更公告三件套 / §门禁覆盖面差集 互补——那两条管变更怎么宣布与门禁漏口，本条管版本不可变性、告警分档与 EOL 前置面）
- **原文**：版本模型「You can edit a flow as many times as you want in **draft** mode … Once you're done with your changes, you can publish it. **The published version will be locked and uneditable.** If you try to edit a published flow, Activepieces will **create a new draft** … and **copy the published version** to the new version.」；告警分档「| Free tiers | You'll receive an email when you reach **100%** of your usage. | | Paid tiers | You'll receive an email at **80% and 100%** …」；EOL 公告「> **Workflows and String are shutting down on March 31, 2027.**」置于文档顶部 Warning；「**These limits are subject to change at any time**」。
- **判据**：① **发布即冻结：published 版本锁定且不可编辑，再次编辑走的是"新建 draft + 复制已发布内容"** ⇒ 任何"改线上"的动作在实现上都是"复制一份新的再改"，回滚因此天然可用（旧版本还在）。设计发布流程时不要把"已发布"当成可写对象，否则就失去了可回滚性这一前提。② **告警阈值要按套餐写成表，不能写一个数**：免费档只在 100% 报警一次，付费档在 80% 与 100% 各报一次 ⇒ 同一套代码在不同套餐上"有没有提前预警"是两种体验；把阈值写死成单个百分比，等于默认所有人都有提前量。③ **生命周期终止（EOL）属于前置面，位置要在文档最顶部**：平台自己把"Workflows 与 String 将于 2027-03-31 关停"放在文档开头当 Warning ⇒ 选型与验收清单里必须有"依赖项的 EOL 日期"一栏，写在附录里等于没有写。④ **限额声明要带"可随时变更"的保留条款**：官方明说限额随时可能调整 ⇒ 把具体数值硬编码进自己的校验逻辑，会在对方调整的那天产生假失败；数值应可配置，且失败信息要能指出"撞的是哪条限额"。
- 提升层：工作流 / 治理。触发词：published 锁定不可编辑、编辑即新建 draft、回滚天然可用、告警阈值分档、80% 与 100%、EOL 日期前置面、限额可随时变更。


## 密钥轮换后的系统是「混合密钥态」；功能开关与数据格式绑定后，关掉开关等于永久数据丢失（来源：docs.n8n.io `deploy/host-n8n/configure-n8n/security/rotate-encryption-keys.md` 5,972B + `build/manage-workflows/view-change-history.md` 4,190B，2026-10-03 r391C 独立 curl 取 `.md` 原文实拉；与 §破坏性变更三件套 / §数据库只向前迁移 互补——那两条管版本升级方向，本条管加密格式与开关的耦合、以及轮换完成后的真实状态）
- **原文**：双层模型「**Instance encryption key** (`N8N_ENCRYPTION_KEY`): your master key, set at deployment time. **This key never changes.** n8n uses it only to protect the data encryption keys. / **Data encryption key**: the key that directly encrypts your credential data. **This is the key you rotate.**」；惰性重加密「n8n generates a new data encryption key and **uses it for all future writes**. Existing data encrypted with the previous key **remains readable**. n8n **silently re-encrypts each record to the new key the next time you update it**.」；单向「**Enabling encryption key rotation is a one-way change. There's no rollback path.**」；「Once you enable … n8n begins writing … in a new format that includes a key identifier. **Older versions of n8n, and instances running without the feature flag, can't read this format.**」；「**Don't disable the feature flag** after any data has been written in the new format. … makes all data encrypted after you enabled the feature **permanently inaccessible**. **Don't downgrade your n8n version** after enabling.」；「The only recovery path is **restoring from a database backup taken before you enabled the feature**.」；前置「All n8n instances, main and all workers, **share the same `N8N_ENCRYPTION_KEY` value** … You need to be the **instance owner**」；版本历史保留「Versions from the last **24 hours** are available for all users. Versions from the last **five days** are available on n8n Cloud Pro. Full workflow history … **Enterprise**」；「n8n **never prunes named versions automatically**」；「n8n creates a new version when you: **Save** your workflow. **Restore an old version** (n8n saves the latest version before restoring). **Pull from a Git repository** (n8n saves versions to the **instance database, not to Git**)」；「**Changes to workflow settings do not create a new version.**」
- **判据**：① **轮换的对象要能说清是哪一层**：主密钥部署时设定、永不变更、只用来保护数据密钥；真正轮换的是数据密钥（本身加密存在库里）。⇒ 说"我们定期轮换密钥"而不分层，等于没说轮换的是什么、丢了会怎样。② **轮换完成后系统是混合态，不是"全部换新"**：新密钥只作用于之后的写入，旧数据保持可读，**每条记录要等下一次更新才被静默重加密**。⇒ 验收"轮换是否完成"不能只看新写入，必须能查出还有多少记录仍是旧密钥；声称"已全量重加密"而没给出存量统计的，基本是没查。③ **功能开关一旦改变了数据格式，关掉开关就是销毁数据**：新格式带 key id，旧版本与未开 flag 的实例读不了；撤掉 flag 或降级会让启用之后写入的数据永久不可读，且**没有自动回退工具**，唯一路径是启用前的数据库备份。⇒ 带格式变更的开关必须同时具备：前置备份要求（原文用 danger 提示）、staging 先验证、**禁止关闭与降级**的显式条款。这不是"谨慎建议"，是数据可用性的硬约束。④ **回滚能力本身有保留期，且默认窗口极短**：版本历史 24 小时（全用户）/ 5 天（Pro）/ 完整（Enterprise），**命名版本永不自动清理**。⇒ 把"能回滚"当能力声明时，必须给出默认窗口；需要长期保留的版本必须显式命名钉住。⑤ **什么算一次版本要写明，含"不算"的部分**：保存、恢复旧版本、从 Git 拉取都会产生版本（且版本存在实例库不是 Git 里），**改工作流设置不产生版本**。⇒ 用户以为"配置改了会有历史"的期待会落空；而"恢复"本身也会先存一份当前版本，回滚不是让历史消失。
- 提升层：治理 / 工作流。触发词：双层密钥、轮换的是数据密钥、惰性重加密、混合密钥态、单向迁移、关 flag 即永久丢失、禁止降级、启用前全量备份、24h 版本历史、命名版本不清理、改设置不产生版本。

## 覆盖值的合法区间由别的配置项动态界定：上下界都是活的，上界变更后会自动 clamp（来源：www.activepieces.com/docs/install/reference/limits.md 6,779B，2026-10-03 r393A 独立 curl 取 `.md` 原文实拉；与 §已发布版本是不可变对象 / §存储满只有两档 互补——那两条管版本与取舍，本条管配置覆盖面的区间约束）

- 两个保留期不是独立旋钮：`AP_PAUSED_FLOW_TIMEOUT_DAYS` **不能大于** `AP_EXECUTION_DATA_RETENTION_DAYS`——暂停的流程不能比它恢复所需的数据活得更久。
- 项目级 override 的合法区间由实例级变量界定：下界 = paused timeout，上界 = instance retention；`null` 表示**回退到实例值**，不是"不限制"。
- 实例变量变化后，已保存的 override 不会失效也不静默越界，而是在 cleanup 时被 **clamp 回新边界** ⇒ 收紧上层限额会连带改写下层已存值，属于**无 diff 的隐式变更**，发布前必须清点。
- 想让某个项目取到更宽的值，必须先把实例上界抬高（原文：raise the instance value if you need a wider range）⇒ 局部放宽的前提是全局先放宽，反过来推不动。

## reload 不是单一动作，要先问断开半径：哪些热应用、哪些会重连、在跑的活会不会丢（来源：docs.openclaw.ai `gateway/config-gateway.md` 36,884B，2026-10-03 r393B 独立 curl 取 `.md` 原文实拉；与 §写入成功 ≠ 生效：发布是独立一步 互补——那条管 reload 这一步存不存在与失败怎么降级，本条管 reload 落下去了会波及谁）

- 变更分三类，处置各不同：①角色定义、代理信任、identity scopes、Tailscale 认证、trusted-proxy 策略 **热应用且不掉线**；②超出模型策略的变更会**重连现有客户端**（以当前权限重新建立）；③已验证的 WebSocket 登录**保留连接**，且**已接受的运行继续执行**。
- 因此发布前必须回答三问：这次改动属于哪一类？会不会断现有连接？在跑的任务会不会丢？——只看"配置保存成功"回答不了任何一个。
- 热应用让"改配置"变成一种无版本、无 diff 的发布 ⇒ 与 §覆盖值区间变更后自动 clamp 同族：凡是热生效的配置，都要在发布清单里点名，否则复盘时没有变更点可查。


## CI 定义类文件是特权路径，判据是「路径+模式+blob」精确三元组，内容等价不构成授权；发布幂等四要素缺一不可；发布管线保留已提交字节不做行尾重整（来源：docs.openclaw.ai `gateway/config-secrets-env.md` 10,309B + `gateway/config-tools.md` 7,517B 索引页 + `gateway/config-tools/github-identity.md` 17,020B，2026-10-03 r395A 独立 curl 取 `.md` 原文实拉）

- **特权路径按文件类别分权，不按仓库统一授权**：`.github/workflows/*.yml|yaml` 的提交/删除/重命名一律要求原始请求者的完整 operator 写权限，会话级写权限不够 ⇒ 发布门禁要先把路径分成「普通源码」与「能改变 CI 行为的定义文件」两类，后者单独要权。
- **判定用精确三元组而不是内容等价**：与已发布分支/PR base 比对的是 exact paths + modes + blobs（含已删除的定义）。未变更的已发布定义允许；继承自目标分支且仍匹配共同祖先的更新允许；但**新写的变更与冲突解决即使最终内容与目标分支一致，仍然要求完整写权限** ⇒ 「结果一样」不能反推「有授权」。
- **无法证明明确继承时按从严处理**：仓库级 checkpoint 证明不了来自已分叉源的明确继承，也推断不出合并关系，这类模糊更新仍要维护者 ⇒ 证明责任在变更方，证据不足不是「放行」的理由。
- **发布幂等要四件套齐备**：durable request ID + 精确 commit marker + 远端分支观测 + 按 head branch 查 PR，四者共同保证网关重启或响应丢失也不会产生重复 commit / push / PR；push 是**条件推送**（条件于观测到的远端 head 或分支不存在），并发改分支即被拒 ⇒ 只靠「请求 ID」一个键撑不起幂等。
- **结算完成不授权下一次**：连接断开或权限结束后，已接受的 PR 响应仍会完成它自己那份回执，本地分支更新也会完成匹配的 index 事务，但这次收尾**不授权再一次 push 或建 PR**；未确认的结果保留其原有的人工确认/恢复要求 ⇒ 「系统善后成功」不等于「下一次可以自动来」。
- **发布保留已提交文件字节**：发布按普通 Git 属性转换暂存，显式保留未变更文件的原有字节，**包括已存在的 CRLF 行尾**，不做无关文件的行尾重整 ⇒ 发布管线默认不 renormalize，否则会制造大量与本次改动无关的 diff（呼应本机 CRLF 机检教训）。


## 并发预算是多轴且互不联动；换运行时就换账本；陈旧引用会被拒绝执行而不是无害忽略；写配置默认拒绝破坏性替换（来源：docs.openclaw.ai `gateway/config-tools/sessions-and-subagents.md` 9,632B + `gateway/config-tools/custom-providers.md` 13,129B，2026-10-03 r395B 独立 curl 取 `.md` 原文实拉）

- **并发不是一个数，是三条互不联动的轴**：`maxConcurrent`（并发运行数，默认 8）、`maxChildrenPerAgent`（每会话准入子代数，默认 5，**提高并发上限并不会提高这个**）、以及生命周期总额度（swarm 的 `maxTotalPerGroup`，默认 200）⇒ 调一条不动另一条，扩容时三条要分别核对，否则会被最紧的那条静默卡住。
- **预算的作用域与账本随运行时变**：`maxConcurrent` 是按「直接派生的那个控制会话」计数，**独立会话之间不共享这笔预算**；swarm collector 子进程走独立的 `tools.swarm.maxConcurrent`，不占用父级的普通子 agent 车道；Codex-native 子 agent 用自己的调度器与限额 ⇒ 「并发是多少」这个问题必须先回答「在哪个运行时、按哪一级计」。
- **陈旧引用会被拒绝执行，且需要显式清理**：`allowAgents` 里指向已删除 agent 的条目，`sessions_spawn` 会**直接拒绝**，并从 `agents_list` 中省略；需要跑 `doctor --fix` 才能清掉 ⇒ 引用完整性不是文档问题，是运行时拒绝面，删除主体后必须有一道清理动作。
- **写配置的默认值是「拒绝破坏性替换」**：安全编辑走 `--strict-json --merge`（追加式），`config set` 默认拒绝会覆盖整块的替换，只有显式 `--replace` 才放行 ⇒ 自动化写配置时把「破坏性」做成需要额外开关的动作，能挡掉一整类误覆盖。


## 安全机制必须声明自己是第几层防御；凭据轮换要「先并存后摘旧」且依赖停用会级联；离职撤销的作用域是三层差集（来源：docs.n8n.io `security/enable-ssrf-protection.md` 3,822B + `security/block-specific-nodes.md` 2,425B + `basic-configuration/use-environment-variables/ssrf-protection.md` 7,039B + pipedream.com/docs `conduit/configure/access-control.md` 13,330B + `conduit/configure/scim.md` 9,789B，2026-10-03 r395C 独立 curl 取 `.md` 原文实拉；n8n 与 Pipedream 均经各自 `llms.txt`（287,049B / 34,240B）定位）

- **安全机制要写明自己是第几层**：n8n 官方对 SSRF 保护明确写「这是**附加的应用层防御**，你应当始终以网络层防护（防火墙、安全组、网络策略）作为主防线，本机制只在此基础上加一层纵深」 ⇒ 交付安全能力时必须带「不替代什么」，只写「已启用 SSRF 防护」会让人误以为主防线有了。
- **轮换的正确顺序是先并存后摘旧**：生成新 token → 更新 IdP → **再**禁用或删除旧的（一个工作区可同时持有多个 token）⇒ 反过来先删旧的必然产生中断窗口；把「允许并存」写进轮换流程是无中断轮换的前提。
- **依赖被停用会级联到凭据**：禁用 token 立即停止其 IdP；**禁用或删除该 token 所绑定的 SSO provider 也会连带停掉这个 token**——一个被关掉的身份提供方既不能供给，也不能再让任何人登录 ⇒ 停用某个上游能力前，先清点挂在它下面的凭据。
- **部署形态变化会让既有令牌失效**：绑定到实例登录 provider 的 token 只在「单工作区模式 **且** 该工作区是实例原始工作区」时有效，切到多工作区模式即失效，曾是多种配置的历史部署同样失效 ⇒ 令牌的有效性依赖部署形态，形态变更要进发布检查表。
- **离职/撤销是三层不同半径**：在 IdP 停用或移除用户，会①从该工作区移除、②**实例级**撤销其活动会话（会话跨工作区）、③结束该工作区内的组成员与策略授予；但**其他工作区的成员身份不受影响**，他们重新登录即可继续用 ⇒ 撤销声明必须把「本工作区成员身份 / 实例级会话 / 其他工作区」三层分开写，否则要么高估要么低估影响面。
- **最后一位 owner 的处置要预先声明**：若离职者是工作区最后一位 owner，由**任职最久的 admin 自动晋升为 owner** ⇒ 所有权不能出现真空，自动晋升规则要写进文档，否则事后无法解释权限从哪来。

## 配置权威源分离：env 管理的配置对运行时写 409 只读、读仍返回 env 值，不静默覆盖（来源：docs.n8n.io `connect/n8n-api/log-streaming.md` 46,321B，2026-10-03 r405B 独立 curl 取 `.md` 实拉；与 §发布态不可变快照 互补——那条管发布产物不可变，本条管"配置有两个权威源（env vs API）时谁赢、写冲突怎么报"）

- **env-managed 配置对运行时 API 写是 409 拒绝、读仍返回 env 当前值**：n8n Log Streaming 目的地若由环境变量定义，create/update/delete 经 API 一律 409 拒绝创建/变更/删除（nothing is created/changed/removed），但 read 仍返回环境变量当前值 ⇒ env 是配置权威源，API 只是只读视图，冲突显式报错而非静默覆盖（避免"API 说改了、实际 env 覆盖"的隐形分叉）。
- **判据**：多权威源配置（env + API/UI/文件）必须声明唯一可写源，其余一律只读+写时显式拒绝（409/只读错误），绝不能"写看似成功实则被另一源覆盖"；读接口要如实返回生效值（env 当前值），不能伪装成可写成功。
- **scope 粒度独立**：`eventBusDestination:list/create/test/read/update/delete` 每个动作独立 scope ⇒ 配置管理 RBAC 可按动作细分（与 r395C RBAC 资格判定/投递验收 同族）。
- 提升层：发布/配置治理。触发词：env 权威源、409 只读、配置多源冲突、immutable 配置、scope 粒度独立。

## 审计保留期是可配置项且按许可分层；审计查询空结果须分因三态（403 无权限 / 402 未授权 / 真无事件）（来源：Qoder r400-Q 审计净新，2026-10-03；与 §审计覆盖面保留期 互补——av 2.127.0 管"声明保留期"，本条管"保留期本身是配置且按许可分层"与"空结果不是单一含义"）

- **保留期按许可分层，不是固定值**：审计日志保留期随许可证层级不同（如 Enterprise 12 月、其他层更短或不可得），保留期是配置项而非常量；声明保留期时要按许可层级分别写，不能给一个统一数字糊弄。
- **审计查询空结果须分因三态**：返回空可能是「无权限(403)」「未授权(402)」「真无事件」三种，空结果不能一律当"没有"——403/402 是权限面缺失、真无才是数据面缺失，验收/排障要先分清是哪一态再下结论。
- 提升层：发布/配置治理。触发词：保留期按许可分层、审计空结果三态、402/403 分因。

## 引用完整性的责任在产品间相反：归档会主动终止引用方、删除不做引用计数、跨对象引用须同请求原子替换（来源：docs.bigmodel.cn `cn/managed-agents/{cloud-environment,mcp,skills}.md` 6,579B / 6,511B / 6,574B，2026-10-04 r409A 独立 curl 取 `.md` 原文实拉；与 §删除被引用 409 / latest 迁移 / 归档不解除引用 对照——那条是"平台替你挡住"，本条是"平台不挡，责任回到调用方"）
- **原文**：`归档：阻止新的会话 / 部署绑定；仍引用它的会话在下一次消费环境的交互时被终止（不使用沙箱工具的纯模型会话豁免）`；`删除：不做引用计数：引用方在下一次使用时得到 not found，定时部署的下一次触发在创建会话阶段失败。删除前请确认没有活跃引用`；`更新 Agent 时，含 mcp_toolset 的 tools 必须与 mcp_servers 在同一次请求中一起替换，保证引用一致`；`删除整个 Skill 时，只要仍有持久化配置引用它，就会返回 409`。
- **判据**：① **同一个产品里两种删除语义并存**（Skill 删除有 409 保护、Environment 删除无引用计数）⇒ 不能把"平台会拦"当通用前提，**变更/退役前必须自己数引用并写进变更单**，否则下一次触发才炸。② **归档不是惰性状态而是有连带杀伤**：归档后仍引用它的会话会在"下一次消费该环境"时被终止，豁免条件是"根本不使用沙箱工具的纯模型会话" ⇒ 归档评估要按"引用方是否真的消费这个资源"分叉，纯对话型负载不受影响、工具型负载会被杀。③ **失败时点不同**：无引用计数的删除把错误推迟到"下一次使用/下一次定时触发"，属于**延迟暴露**类风险，监控必须覆盖定时任务创建阶段而不只是运行阶段。④ **跨对象引用须同请求原子替换**：`mcp_toolset` 与 `mcp_servers` 分开更新会产生悬空引用，发布脚本要把这组对象当作一个原子变更单元。⑤ 快照语义（Environment 在创建会话时固化为快照，之后更新只影响新会话）与"归档终止存量"并存 ⇒ **存量运行不受配置更新影响，但受归档影响**，两类变更的爆炸半径完全不同，变更评审要分开看。
- 提升层：发布/配置治理。触发词：归档终止引用方、删除无引用计数、延迟暴露、跨对象原子替换、快照语义、变更爆炸半径。

## 漏洞响应是一条独立于发布的流水线：回执先于评估、禁运期内只做补丁、披露分两批、复盘按严重度分档（来源：www.activepieces.com/docs `handbook/engineering/playbooks/security-advisory-response.md` 7,251B，2026-10-04 r410C 独立 curl 取 `.md` 原文实拉；与 §引用完整性 / §依赖守卫 互补——那两条管"改了什么会连带谁"，本条管"收到一个安全报告之后按什么顺序走完"）
- **原文**：`Reply in the advisory thread on intake confirming the report was received, with a confidentiality reminder. Do this first, before reproduction and scoring, so the response is never delayed by triage depth`；`Score with CVSS 4.0 … Buckets: 0.1–3.9 low, 4.0–6.9 medium, 7.0–8.9 high, 9.0–10 critical`；`Send evaluation within 7 business days … Clock starts at the report timestamp`；`Use a temporary private fork`；`A public PR or push collapses the embargo. Double-check the remote URL before pushing`；`Set the embargo … Default 60 days. Hold publication until the patch is on cloud production and customers have been notified`；`Always a patch bump (e.g. 0.71.0 → 0.71.1). Never bundle with feature commits`；`7-day lead time before public publication. Patched version must already be on cloud production before sending`；`Postmortem Required for high/critical, optional for medium, skip for low`；模板五段 `Summary … no exploit detail / Impact / Patches / Workarounds（或注明唯一安全选项是升级）/ References`。
- **判据**：① **回执必须先于评估**：先确认收到并附保密提醒，再做复现与打分 ⇒ 报告的响应时延不该被分诊深度拖长；把"查清楚再说"当流程第一步，等于让报告人在最需要反馈的窗口里等一个不确定的时间。② **修复与发布是两条线，补丁发布只带补丁**：补丁只做 patch bump、绝不和功能提交打包 ⇒ 混在一起会让"为了修漏洞必须升级"变成"必须接受一批新功能"，反之则让"这个版本改了什么"失去可判定性。③ **禁运是有形资产，一次公开推送即失效**：修复在临时私有 fork 的 `security/<ghsa-id>` 分支上做，公开 PR 或 push 直接打破禁运 ⇒ 凡"先私下修"的流程，必须把远程地址当作危险操作来复核。④ **披露分两批且顺序不可颠倒**：先通知客户（提前 7 天）且**补丁必须已在生产生效**，再公开 CVE ⇒ "公开披露"与"用户可修复"之间若没有这个提前量，公告本身就成了一份攻击指南。⑤ **复盘按严重度分档而不是一律做**：high/critical 必做、medium 可选、low 跳过 ⇒ 复盘成本要花在爆炸半径大的那类上，一律复盘会稀释注意力、一律不复盘会丢掉最该学的那次。⑥ **公告正文有固定五段且明确不含利用细节**；Workarounds 段若没有可行缓解，**必须明写"唯一安全选项是升级"** ⇒ 留空会被读成"不升级也有办法"。
- 提升层：工作流 / 治理。触发词：漏洞响应生命周期、回执先于评估、CVSS 4.0 分桶、7 工作日评估、临时私有 fork、公开推送破禁运、只做 patch bump、60 天禁运、客户先于公开 7 天、复盘按严重度分档、advisory 五段模板、no exploit detail。

## 发布闸门要能「合并而不部署」；制品版本只能有一个可写真源且手填入口必须校验；回滚要反转目标版本不认识的迁移，破坏性迁移会永久缩短可回滚窗口（来源：www.activepieces.com/docs `handbook/engineering/playbooks/releases.md` 9,981B + `playbooks/database-migration.md` 5,045B，2026-10-04 r411A 独立 curl 实拉；与 §漏洞响应是独立流水线 互补——那条管安全修复的披露与补丁纪律，本条管常规发布流水线的闸门、版本真源与回滚半径）
- **原文**：冻结窗 "merges to `main` after 5 PM UTC are **accepted but not deployed** to staging. The content team uses the frozen staging environment overnight"；热修 "Blocked automatically if the next scheduled Sunday promotion is within 1 hour"；版本真源 "Because `package.json` is the single runtime source of truth … a mistyped tag would publish an image whose real version disagrees with its tag — **invisible until it's mixed with a correctly-built peer and the worker↔app version gate silently withholds jobs**"，故有 `Verify tag matches package.json` 步骤；回填 "merge that PR **before the next release-candidate cut (Thursday 5 PM UTC)** … merging after the cut is too late"（0.85.4/0.85.5 因错过而报成 0.85.2）；回滚 "Reverses DB migrations not present in the target image's manifest … `force`: Force rollback even if breaking migrations exist. Default: `false`"；迁移 "CI will fail if `breaking`, `release`, or `down()` are missing on new migrations"，且 `breaking = true` 时可不实现 down()。
- **判据**：① **环境冻结不等于代码冻结，闸门应卡"部署"而不是卡"合并"**——需要一个"稳定但仍被使用"的环境时（内容团队夜间要用 staging），正确做法是继续接受合并、只推迟制品上线；反过来卡合并会把人力堵在门口，而环境并没有因此更稳定。② **版本号只能有一个可写真源，凡手填入入口必须在发布时与真源对齐**：能被烤进制品的那个（package.json）才是真源，手填 tag 只因要带 `-hotfix.N` 后缀而存在 ⇒ 多一个手填入口就必须多一道等值校验，否则产出"真实版本与 tag 不一致"的制品。③ **版本门失配的失败模式是静默扣住任务，不是报错**——worker↔app 版本门在版本不一致时"什么都不做"，症状是任务凭空消失而不是错误日志 ⇒ 排查"任务没有被处理"时要把版本一致性列为候选，只在日志里找错误会一无所获。④ **发布后回填真源是流水线的一环且有截止时点**：热修分支上的版本变更不会自己回到主干，靠自动 PR 回填；而一旦错过 RC 切分点，"已存在的 tag 不会被覆盖"会让错误以"版本回退/重复"的形态跨多个版本留存。⇒ 凡"分支上改了版本、主干不知道"的流程，必须给回填设死线。⑤ **回滚 = 换镜像 + 反向迁移，不是只换镜像**：回滚会反转目标镜像清单里不存在的迁移；而声明为破坏性的迁移没有 down()（CI 允许不实现），一旦合入，**这段历史就再也回不去了**，需要时用 `force` 硬回滚等于承认数据面已不匹配 ⇒ 破坏性迁移的真正代价不在当下，而在它永久缩短了可回滚窗口。因此可逆性与破坏性必须写成机器可检字段（`breaking` / `release` / `down()` 缺一即 CI 失败），不能只写在说明里。
- 提升层：工作流 / 可复用 Skill。触发词：冻结窗只卡部署、合并≠部署、版本真源唯一、tag 与 package.json 校验、版本门静默扣任务、回填真源有死线、回滚反转迁移、breaking 迁移无 down、可回滚窗口、迁移三字段机检。

## 重构不破链：拆分、改名、迁移必须保留旧锚点并给出「旧→新」逐条映射（来源：docs.openclaw.ai `concepts/active-memory.md` 7,276B，2026-10-04 r412B 独立 curl 取 `.md` 原文实拉；与 §版本真源唯一 / §回滚须反转迁移 互补——那两条管"版本从哪来"与"回滚怎么走"，本条管"结构重排后别人的引用还成不成立"）
- **原文**："Every section heading from the previous single-page version keeps its anchor here, so an existing link such as `/concepts/active-memory#lossless-claw` **still resolves**. Each entry points at the page that now holds the content."
- **判据**：① **已发布的链接是对外契约**：重排（拆页 / 改名 / 迁移）时可以改的是自己的组织方式，不能顺手打断别人的引用 ⇒ 旧锚点必须保留并指向新落点，"移动了而已"不是断链的理由。② **迁移留映射表，不留一句"已移动"**：逐条「旧标题 → 新页面#锚点」才可机检核验无遗漏（尤其拆分后一节可能对应多处）⇒ 只有一句"已移动"的迁移，等于把完整性检查推给每一个读者。③ **断链的代价由引用方承担、收益由重构方获得**：这是典型的外溢成本，所以验收标准要写在重构这一侧（旧链接全量探活 200 / 锚点可解析），而不是等下游报错。
- 提升层：工作流 / 交付维护。触发词：重构不破链、保留旧锚点、拆分页面、链接重定向、旧→新映射表、断链验收、外溢成本。


## 把「曾经自动生效的额度」改成「必须显式开启的选项」是一次语义迁移：必须给等价换算式与最坏上界式，否则老配置在新版本表现为间歇性失败（来源：docs.openclaw.ai `concepts/active-memory/recommended-setup.md` 2,673B，2026-10-04 r413A 独立 curl 取 `.md` 原文实拉；与 §重构不破链 / §回滚须反转迁移 互补——那两条管"结构重排后引用还成不成立""回滚怎么走"，本条管"同一个配置项在新版本里换了含义但值没变"）
- **原文**：「Before v2026.5.2 the plugin **silently extended** `timeoutMs` by an extra 30000 ms during cold start… v2026.5.2 moved that grace behind an **explicit** `setupGraceTimeoutMs` config: `timeoutMs` is now the recall-work budget by default unless you opt in.」「If you upgraded from v2026.4.x and tuned `timeoutMs` for the old implicit-grace world … set `setupGraceTimeoutMs: 30000` to restore the pre-v2026.5.2 **effective** budget.」「Worst-case blocking time is `timeoutMs + setupGraceTimeoutMs + 3000` ms」
- **判据**：① **隐式→显式是兼容性最差的一类变更**——值没动、语义变了，配置校验全部通过，失败只在特定条件（冷启动 / 首次调用 / 资源竞争）下出现，于是被当成随机 flaky 而不是升级回归。⇒ 迁移说明里必须给出**等价换算式**（旧有效值 = 新值 + 需补的显式项）而不是一句"新增了 X 配置"。② **最坏上界要写成公式而不是描述**——上界 = 主预算 + 显式宽限 + 固定前后置开销，且内外两层看门狗共享同一有效预算；只写"可能更慢"无法验收。③ **宽限被分离出来之后，默认值的选择就带了取舍**：低值（5000–15000ms）换来的是"重启后第一次调用可能空返回"，这是**被接受的成本**而不是 bug ⇒ 新默认值要连带说明它牺牲了什么。④ **前后置固定开销不延长业务执行**——preflight 与结算各有独立固定额度，不能算进业务预算；把固定开销写进可调预算会让"加机器"看起来像"加超时"。⑤ 对发布/依赖守卫的落点：升级评审清单里单列一类「**语义迁移项**」——字段没增删、类型没变、但有效行为变了，这类项只做 diff 是扫不出来的，必须逐个给换算式与上界式。
- 提升层：工作流 / 可复用 Skill。触发词：隐式宽限变显式、语义迁移项、等价换算式、最坏上界公式、升级后间歇超时、冷启动预算。


## 批量状态迁移要过三闸、批准凭证只绑不可变事实；比对必须先归一化，且三类不同物种分三类处置（来源：docs.openclaw.ai `clawhub/publishing.md` 18,217B，2026-10-04 r416A 独立 curl 取 `.md` 原文实拉；与 §发布闸门只卡部署 / §版本真源唯一 互补——那两条管"什么时候上线"与"版本从哪来"，本条管"一次性改动一大批已有记录时，什么证明你改对了"）
- **原文**：「ClawHub stores what you pass and displays the normalized form」「These topic names are reserved by ClawHub and are rejected: `approved`, … `verified`. The check runs on the normalized form, so `Official` and `staff pick` are rejected too.」「Use `dry_run: true` to preview new and changed skills without publishing.」「Automatic changelog generation and preview use a ten-second provider deadline … If the provider is unavailable or times out, ClawHub returns local fallback notes so publishing and preview can continue.」「Run the default dry run for each of … `cursor` until `isDone`. Apply from the initial cursor with `dryRun: false`, then repeat the dry run to verify no remaining matches.」「Deleting trusted publisher config is the rollback path.」「That workflow route does not accept cancelled parents.」「It defaults to a dry run; add `"dryRun":false` to discard each pending release」「Transfers to another user normally require recipient acceptance.」
- **判据**：① **批准凭证只绑不可变事实，不绑当前状态**：批准的哈希绑「发布物 + 源哈希 + 分类 + 分配」而**刻意排除状态字段** ⇒ 同一凭证跨 preview→accepted→applied 存活，但每次 apply 仍重校验绑定。把可变状态写进凭证会两头错：状态一变凭证就失效（逼人重签），或状态被改而凭证仍"看起来有效"（假批准）。② **批量迁移的两类游标不可互换**：报告游标（读到哪）与预览/apply 游标（处理到哪）是两张表，回退行不可 accept、须用新 run ID 重分类 ⇒ 拿错了游标会把"已读"当成"已处理"，于是漏掉的行永远是漏掉的。③ **apply 前必须做事务内演练并核对已处理条数**：先跑 dry run 直到 `isDone`、apply 后**再跑一次 dry run 验证无剩余匹配**；响应丢失不能绕过这道闸 ⇒ 没有"改完再验一遍"的闭环，批量迁移的完整性只能靠信任。④ **并发迁移互斥是硬闸**：存在未审的 accepted 行或另一个迁移 worker 活跃时直接拒绝 ⇒ 批量状态变更不是可重入操作。⑤ **比对必须先归一化**：保留词表作用于规范化形式，故 `Official`、`staff pick` 与全小写形式同拒 ⇒ 先比对后归一化（或不归一化）等于把过滤做成换个大小写就能绕过。⑥ **三类物种分三类处置，不要合并成一种**：重复项**丢弃且不报错**（无害冗余）、未知分类项**拒发**（不可判定）、保留词命中**拒**（明令禁止） ⇒ 一律报错会把无害重复变成噪音，一律忽略会让不可判定项悄悄过关；正确性是"分类"换来的，不是"严格"换来的。⑦ **被取消的父级不接受**：cancelled parents 不进入该流程 ⇒ 上游已放弃的变更不能继续向下推进，否则会产生没有来源的孤儿状态。⑧ **增强件超时不得阻断主流程**：预览/变更日志有独立的 10 秒 provider 期限，超时就退回本地 fallback notes 让发布继续 ⇒ 辅助能力缺失应降级为"少一点信息"，不能升级为"整批做不了"。⑨ **所有权转移须接受方确认**：转移给另一用户需要对方接受 ⇒ 单向写入他人名下变更是默认禁止，不是默认允许。
- 提升层：发布治理 / 工作流。触发词：批量状态迁移三闸、批准凭证排除状态、报告游标与 apply 游标分表、回退行须新 run ID、apply 后复跑 dry run、迁移 worker 互斥、归一化后比对、保留词表、重复丢弃不报错、未知分类拒发、cancelled parents 不接受、增强件超时降级。

## 己方失陷的止血有固定次序：先停执行体、再收网络暴露面、再收授权面，且轮换默认按「已失陷」处置（来源：docs.openclaw.ai gateway/security/operator-incident-response.md 2,280B，2026-10-04 r417B 独立 curl 取 .md 原文实拉；与 rm 1.67.0「外部报告的补丁与披露流水线」互补——那条管收到报告后怎么发补丁，本条管自己已经出事后先按什么顺序摁住）
- 次序不可换：① 停执行体（终止网关进程，含监管它的宿主应用）；② 收网络暴露（绑定改回 loopback、关掉外网隧道面）；③ 收授权面（高危会话改禁用、移除 `*` 全放行条目）。**先停跑的再关可达性再关许可**，反过来做会在执行体仍在跑的窗口里继续产生副作用。
- 轮换的前提是「假定已经失陷」：网关自身凭据、远程客户端凭据、以及所有 provider / API 凭据（含 SQLite auth store 里的 model key 与加密 secrets 载荷值）一并轮，不先等确证。
- 轮换的热生效面是有限的：**改值可以热应用，改模式或改进程环境里的凭据必须重启**。有效认证模式保持不变时才允许热应用；换 SecretRef 必须显式给出 `mode`。把「轮换」当成一个原子动作会得到「改了但没生效」的假象。
- 事后审计要专门回看「最近有没有把访问面改宽的配置变更」：绑定地址、认证方式、会话/群组策略、提权工具位、插件变更。入侵路径常常藏在一次 widening 变更里，只看日志会漏。
- 取证清单要固定成模板，否则每次现想都会缺项：时间戳、宿主系统与版本号、相关会话转录、脱敏后的日志尾段、**攻击者发了什么与 agent 做了什么**（两侧都要）、以及执行体是否越出 loopback 暴露过。

## 已上架物的「更新」不原地替换：发新条目 + 手动撤回旧版，而不是覆盖原条目（来源：docs.dify.ai/en/cloud/use-dify/publish/publish-to-marketplace.md 6,746B，2026-10-05 r421-C 独立 curl 取 `.md` 原文实拉逐串命中；消化 Qoder r420-Q-A A-1 积压点）
- **原文**：「**To change anything inside the app** (its prompts, tools, model settings, and so on) — **Submit the updated app as a new template. This creates a separate listing rather than replacing the original**, so you can manually unpublish the old version once the new one is published.」；对照「**To change only the listing** (such as the Overview or Setup steps)」走另一条路径（仅改陈列信息可原位）。
- **判据**：① **"改内容"与"改陈列"是两种更新，路径必须分开**——改应用内部（提示词/工具/模型）发新条目，改概览/安装步骤才原位改 ⇒ 把两者合并成一种"更新"，会让使用者以为原地替换是常规动作，从而失去"旧版还在、可回滚"这一层保护。② **新条目先上线、旧版手动下架**——顺序是先有替代者再撤旧，且撤回是**显式人工动作** ⇒ 自动下架会在新条目还没被验证前制造空窗；"更新"这个词默认隐含替换，实现上必须拆成"新增 + 撤回"两个可分别审计的动作。③ **已发布物具有不可覆盖性**——对外可见的东西一旦被人引用（安装/收藏/依赖），原地改写就等于静默改变他人已获得的东西 ⇒ 凡"已出街"的条目，变更一律走新版本标识。④ 与既有「日落资格登记 / 发布态不可变快照」分工：那两条管**能不能退场**与**快照不被后续编辑污染**，本条管**内容变更时的替换语义**——不是能不能改，而是改的时候是"替换"还是"另立"。
- 提升层：工作流 / 发布治理。触发词：更新不原地替换、发新条目再撤旧版、改内容与改陈列分路径、已发布物不可覆盖、撤回是显式人工动作、新增加撤回两动作。

## 发布门可以前移到供给侧：平台把评测工具链下发给供方，让「门」在开发期而非接收侧（来源：skills.aliyun.com/skill-forge，2026-10-05 r422-A 浏览器通道实拉取得渲染后正文——curl 直取仅 1,984B SPA 壳无正文，WebFetch 取得完整正文逐串命中；消化 Qoder r420-Q-B B-1 积压点）
- **原文**：「按「需求定义 → 开发调试 → **安全评测** → **生产验证**」四步走完成 Skill 锻造。平台提供：Skill 开发套件（CLI / SDK / 调试工具）、沙箱测试环境（含真实 API 与脱敏数据集）、**安全合规评测工具链**、性能压测与质量基线检查」；「**通过质量评审后，Skill 自动上架**」；「共建 Skill 质量评估与安全评测体系」；周期侧「共建周期通常在 **2–6 周**」「开放平台团队 **5 个工作日**内审核报名信息」。
- **判据**：① **门的位置决定门的语义**——接收侧扫描只能「拒」（发现问题时工件已成事实、供方无上下文、退回成本最高），供给侧评测可以「修」（供方持有源码与场景上下文、改完再提）⇒ 设计准入流程时先判门该设在哪一侧：只做接收侧检测的系统，本质上把质量成本全部押在最后一步。② **"把工具链下发给供方"是供给侧门能成立的前置条件**——平台不只出要求还出工具（SDK/沙箱/评测链/压测基线），供方才可能在自己环境里跑出可复核结论 ⇒ 只发标准不发工具链的"供方自测"，等价于把门又推回接收侧。③ **人工环节要给时限与位置**——5 个工作日审核落在"场景匹配"（准入前）而非"评审放行"（准入后），2–6 周是共建期 ⇒ 人工不在关键路径上堵着，而在入口做匹配；把人工放在最后一步放行位，吞吐会被单点评审锁死。④ **"通过评审即自动上架"让门变成流水线而非闸门**——门禁结论直接驱动发布动作，不经过第二次人工搬运 ⇒ 自动化的前提是被测物已过双门（自动化策略检查 + 人工/共建期验证），缺一则该自动化只放大错误。⑤ 对 guild 的落点：任何"技能/工具入库"流程，先回答「我们的门在供给侧还是接收侧」，再决定要买/建的是评测工具链还是扫描器；两者不可互相替代。
- **与既有能力分工**：上一条（已上架物更新不原地替换）管**发布之后的变更语义**；接收侧三线扫描（SkillHub，r266B/r417-Q-C 已落）管**到达后的检测**；本条管**到达之前门该放哪**——同一个"质量门"因位置不同变成两种机制。
- 提升层：工作流 / 发布治理。触发词：发布门前移、供给侧评测、平台下发工具链、供方自测门禁、通过评审自动上架、接收侧只能拒、共建周期、人工在入口不在放行位。

## 同一份变更事实要出两份产物：Release notes 给人读（可折叠分区），Changelog 给 agent 读（纯 Markdown），两者同源同量、只有呈现不同（来源：api.github.com/repos/openclaw/openclaw/releases?per_page=5 142,182B，v2026.9.8 release body 一手命中，2026-10-05 r423-B 独立 curl 实拉逐串命中；与 rm「Changelog Miner / Release Notes」分工互补——那两条管"从哪里挖变更"与"写成什么语气"，本条管"同一事实要不要出两份、两份之间是什么关系"）
- **原文**：「The release notes and changelog contain **the same content, presented in two formats**: - [Release notes] — **formatted for people**, with expandable sections. - [Changelog] — **plain Markdown for AI agents and tools**.」同批 v2026.8.34/8.35 为 `extended-stable`（官方自述「our current equivalent to LTS」）的实际发布形态佐证：稳定线同样按同一 content 出双形态。
- **判据**：① **内容与呈现要拆成两件事管**：官方写的是 "same content, two formats"，不是"人版摘要 + 机版日志" ⇒ 若两边各自撰写，两个版本必然漂移（描述口径、条目集合、严重度标签都对不上），而这种漂移无人负责、也无法自动察觉，最终消费方不知道该信哪份。② **判断一份产物是否合格，看它的主要读者能否"不经转换直接取用"**：给人看的要保证可导航（折叠分区、按贡献分组、致谢与背景），给机器看的要保证可机读（稳定锚点、纯 Markdown、可 grep/diff）⇒ 排版装饰对机器是噪声，纯文本堆砌对人也是负担，二者不能用同一份文件同时照顾。③ **当消费方里有 agent（自动生成升级清单/影响面分析/依赖守卫）时，纯 Markdown 通道是硬需求而不是恩赐**——让 agent 去解析带折叠容器的 HTML 展开器，等于把"能不能自动化"寄托在一个无障碍交互能否被脚本触发上 ⇒ 给机器留一条无需 UI 状态即可读完的路径。④ **两份必须在同一次发布动作里同步产出并提交校验**（"— is Current Release"式交叉引用或直接并列链接）⇒ 双通道的价值建立在"它们必然同步"这一前提上；若第二份由后续流程补写，它就退化为摘要的第二版本。
- **与既有能力分工**：上一条管发布门设在供给侧还是接收侧；本条管**发布物自身的读者双通道**。
- 提升层：工作流 / 发布治理。触发词：发布说明双形态、same content two formats、changelog for agents、纯 Markdown 通道、发布物人机双读者、折叠分区对机器是噪声。

## 回溯式巡查必须周期性「全量重扫」，而不是只从上一次回移游标往前推进：游标会固化当年"判定为不回移"的旧结论（来源：api.github.com/repos/openclaw/openclaw/releases?per_page=5 142,182B，v2026.8.34 release body 一手命中，2026-10-05 r423-B 独立 curl 实拉逐串命中；与 rm「批量状态迁移要过三闸」互补——那条管"一次性改动大批记录时怎么证明改对了"，本条管"长期维护分支怎么保证没漏"）
- **原文**：「**Complete rescan:** re-evaluate the full 2026.8.33 discovery range, large mixed-purpose pull requests, and the 2026.7.35 lineage **instead of advancing only from the previous backport cursor**.」上下文为该 `extended-stable`（LTS 等价）线由 113 个审计挑出的修复单元回移组成（「backport 113 audit-selected fix units across upgrades, Doctor, authentication, sessions, channels, plugins, sandboxing, filesystem safety, model runtimes, and release packaging」）。
- **判据**：① **游标只回答"上次看到哪"，不回答"该看的都看了吗"**：按上一次回移游标推进，隐含假设是"当年被判定不回移的那些现在仍然不该回移"——但分支从主线变成 LTS/稳定线的那一刻语境已变（容忍的参数变了：主线上可接受的行为风险，稳定线不可接受）⇒ 长寿命分支必须按周期把整个发现区间重判一遍，"曾经正确地拒绝"会在新语境里变成当下的遗漏。② **巡查清单要显式包含"大型混合目的改动"**：官方把 large mixed-purpose pull requests 单列 ⇒ 混合改动当年整体不合而被拒，其中某一部分在稳定线上恰恰是必要修复；按单个 PR 粒度做是非判断的系统会永久丢掉这些"混在被拒外壳里的正确片段"。③ **跨血缘巡查要覆盖多条 lineage 而非只看上一代**（同时纳入 2026.7.35 lineage）⇒ 血缘断层处的修复最容易永久丢失，因为它既不在当前范围、也不在上一次的回移记录里。④ **这条的本质是"否定的收益率随时间衰减"**：判断题型的输出是布尔值，但决定那个布尔值的前提会漂移 ⇒ 任何"曾经审计过并排除掉"的台账都要有到期重审机制，不能靠记忆或增量维护；对 guild 的落点：把"历史排除清单"当作有时效的台账（附当时的判据快照），每次 LTS 组装/大版本收口时重扫，并显式写明本次用的是"全量重扫"还是"游标推进"。
- 提升层：工作流 / 发布治理。触发词：全量重扫、complete rescan、回移游标、backport cursor、LTS 等价线、混合目的 PR 重判、跨血缘巡查、历史排除台账要到期重审。

