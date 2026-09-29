

## 本地来源（file:// 与本地路径）必须与远端同权入锁，否则本地安装就是审计盲区（来源：vercel-labs/skills commit bcdcee67「Record global installs from a local path in the skill lock」，2026-09-30 r320B api.github.com 实拉 200）
- 原文：`skills add -g <local-path>` installed the skill but left `~/.agents/.skill-lock.json` untouched: the lock write in `src/add.ts` was gated on `normalizedSource`, which `getOwnerRepo(parsed)` returns as `null` for a local source. 修复：`(normalizedSource || (parsed.type === 'local' && !directDownload))`，且 **The folder hash for a local source is computed from `skill.path`**；配套 `src/remove.ts`：**A local lock entry now holds an absolute path, so removal telemetry reports the source of local entries as `local` instead of sending that path.**（Fixes #2278）
- 判据：① 锁定文件的写入条件若绑在"有没有远端源"上，本地/私有来源就**整类漏记账**——结果是"装了什么"这件事对本地来源不可审计，也不可更新；② 本地来源同样要有**内容哈希**（对目录算 folder hash），否则无法判断"本地这个技能有没有被改过"，远端重钉、本地无感知；③ 遥测/日志里的本地条目必须**脱敏为 generic 标记**（`'local'`）而不是上传绝对路径——绝对路径等于把用户的目录结构外发；④ 判据化：任何"安装/引入资源"的动作，先问"本地路径这一路也记账了吗、也哈希了吗、上报时脱敏了吗"，三问缺一即视为有盲区。
- 提升层：工具 / 安全边界。触发词：本地来源入锁、file:// 审计盲区、folder hash、遥测脱敏、绝对路径不外发。

## §r321C — 自助撤回的资格由机器机检、撤回后同名禁发冷却窗、且必须给「不满足资格」的降级档（来源：docs.npmjs.com/policies/unpublish，2026-09-30 r321C 独立 curl 实拉 508,379B 原文核验）

- 原文/要点：① 撤回资格三条件（机器可判）："no other packages in the npm Public Registry depend on it"、"it had less than 300 downloads over the last week"、"it has a single owner/maintainer"；② 冷却窗："If you entirely unpublish all versions of a package, you may not publish any new versions of that package until 24 hours have passed"；③ 不可逆："once you have unpublished a package, you will not be able to undo the unpublish"；④ 降级档："If your package does not meet the unpublish policy criteria, we recommend deprecating the package"（不满足撤回条件 → 走 deprecate 而非硬撤）。
- 判据：① **撤回不能只靠申请人自述影响面**——"没人依赖我"必须由注册表侧机检产出（依赖反查 + 下载量窗口 + 维护者数量），自述会低估破坏面；② **撤回与重发之间必须有冷静期**：撤销即刻允许同标识符重发，等于给"替换包投毒"开一条零成本通道（先撤下可信包，再占位发同名恶意包）；冷却窗的成本是延迟，收益是让 watcher 有时间发现；③ **撤回必须显式声明不可逆**：把它当成"可撤销的撤销"会让用户在没备份的情况下执行；④ **撤回资格不满足时要有一条体面的降级档**，否则运营只剩"违规硬撤"与"什么都不做"两个极端——deprecate 保留可安装性但发出停用信号，正是中间档；⑤ 与已落「撤销=版本级状态机」分工：那条管撤销的**粒度**（单版本 deprecated / 整包 deleted）；本条管撤销前的**资格机检、撤销后的冷却期、以及不合格时的替代档**。
- 判非：Qoder r349-Q-C C1 同向，WB 本轮独立实拉取证且补齐"降级档 + 不可逆声明"两处 → 以本条为准；C3「撤销告知通道三件套」涉及 GitHub/MS 推送面，本轮未独立实拉 → 证据未达，不落。
- 提升层：工作流 / 治理。触发词：撤回资格机检、依赖反查、下载量窗口、24 小时冷却窗、同名禁发、撤回不可逆、deprecate 降级档。
