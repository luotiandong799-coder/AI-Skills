

## 本地来源（file:// 与本地路径）必须与远端同权入锁，否则本地安装就是审计盲区（来源：vercel-labs/skills commit bcdcee67「Record global installs from a local path in the skill lock」，2026-09-30 r320B api.github.com 实拉 200）
- 原文：`skills add -g <local-path>` installed the skill but left `~/.agents/.skill-lock.json` untouched: the lock write in `src/add.ts` was gated on `normalizedSource`, which `getOwnerRepo(parsed)` returns as `null` for a local source. 修复：`(normalizedSource || (parsed.type === 'local' && !directDownload))`，且 **The folder hash for a local source is computed from `skill.path`**；配套 `src/remove.ts`：**A local lock entry now holds an absolute path, so removal telemetry reports the source of local entries as `local` instead of sending that path.**（Fixes #2278）
- 判据：① 锁定文件的写入条件若绑在"有没有远端源"上，本地/私有来源就**整类漏记账**——结果是"装了什么"这件事对本地来源不可审计，也不可更新；② 本地来源同样要有**内容哈希**（对目录算 folder hash），否则无法判断"本地这个技能有没有被改过"，远端重钉、本地无感知；③ 遥测/日志里的本地条目必须**脱敏为 generic 标记**（`'local'`）而不是上传绝对路径——绝对路径等于把用户的目录结构外发；④ 判据化：任何"安装/引入资源"的动作，先问"本地路径这一路也记账了吗、也哈希了吗、上报时脱敏了吗"，三问缺一即视为有盲区。
- 提升层：工具 / 安全边界。触发词：本地来源入锁、file:// 审计盲区、folder hash、遥测脱敏、绝对路径不外发。
