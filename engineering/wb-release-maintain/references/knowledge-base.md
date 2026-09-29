

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
