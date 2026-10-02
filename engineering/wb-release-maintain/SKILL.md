---
name: wb-release-maintain
description: >-
  仓库发布与依赖维护（合并 Claude Code 自动化 Skill 的 Changelog Miner、Release Notes、Dependency Guard 三个能力：从代码改动找关键变更补遗漏、从 diff 提炼用户可读的更新说明、升级依赖前先看破坏面）。当需要为仓库写更新说明/发布说明、梳理一段改动里哪些是关键变更哪些有遗漏风险、升级依赖前评估影响范围时使用。不用于日常 git 操作（走 github skill / gh CLI）、不用于排障（走 wb-debug-loop）。、输入集版本化、评测集版本、复现门票、未版本化不许续、增量版本、旧引用钉旧版、兼容面判定、存量自动升级、新老行为并存、版本区间声明、特性声明单一来源、轻量版本化、发布态语义、草稿发布不可变快照、回滚重发旧版、提升扇出、停用挡在用
version: "1.55.0"
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
