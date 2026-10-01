---
name: wb-release-maintain
description: >-
  仓库发布与依赖维护（合并 Claude Code 自动化 Skill 的 Changelog Miner、Release Notes、Dependency Guard 三个能力：从代码改动找关键变更补遗漏、从 diff 提炼用户可读的更新说明、升级依赖前先看破坏面）。当需要为仓库写更新说明/发布说明、梳理一段改动里哪些是关键变更哪些有遗漏风险、升级依赖前评估影响范围时使用。不用于日常 git 操作（走 github skill / gh CLI）、不用于排障（走 wb-debug-loop）。、输入集版本化、评测集版本、复现门票、未版本化不许续、增量版本、旧引用钉旧版、兼容面判定、存量自动升级、新老行为并存、版本区间声明、特性声明单一来源、轻量版本化、发布态语义、草稿发布不可变快照、回滚重发旧版、提升扇出、停用挡在用
version: 1.39.0
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

## 学习轮沉淀区（本段）
（r历史 起的连续学习轮章节共 262 章已下沉 references/knowledge-base.md §≤200迁移，正文留此指针）


## 环境间提升必须单向；删除不随拉取传播；跨环境只搬「形状」不搬「秘密」（来源：docs.n8n.io `/administer/use-source-control-and-environments/push-and-pull-changes.md` 12,333B + move-work-between-environments 4,207B + understand-source-control 1,929B，2026-10-01 r339B 独立 curl 实拉逐串命中）
- **原文**：①「work goes in one direction: **either to Git, or from Git, but not both**」（同一实例又推又拉官方明确不推荐）；②「When workflows, credentials, variables, tags, and data tables are **deleted from the repository**, your local versions of these resources **aren't deleted automatically**. … n8n notifies you about any **outdated resources** and asks if you'd like to delete them」；③「**Credential stubs** - name and type. Any other fields are included only if they are expressions.」「When the changes include new variable or credential stubs, n8n notifies you that you need to **populate the values for the items before using them**」；④「n8n **syncs data table schemas** … **Row data isn't synced.**」；⑤「**Workflow and credential owner may change on pull**」——按项目名匹配，无匹配则新建项目并把当前用户设为 owner；⑥「If you have more than one Git branch, you need to **merge the branches in your Git provider** to copy work between environments. **You can't copy work directly between environments in n8n.**」
- **判据**：① **提升（promotion）链路要设计成单向**：源环境只推、目标环境只拉。同一节点双向同步会把「谁是最新的」变成运行时问题，官方宁可劝退也不做合并策略。⇒ 设计环境同步前先回答方向，方向不定就不该上线同步。② **删除是唯一不自动传播的动作**：仓库里删了，本地仍在，只会被标为 outdated 并等你确认。⇒ 「删了怎么还没生效」是预期行为；反过来说，**任何声称「同步」的通道都必须逐类声明删除是否传播**——不声明就是埋雷。③ **跨环境只同步形状，不同步秘密值**：凭据只走 name+type 的 stub，真实值由目标环境自备。⇒ 这既是安全边界（秘密不跨环境漂移）也是可用性约束（新 stub 未填值即不可用，必须在**使用前**阻塞而不是运行时才炸）。④ **schema 与 row 的同步策略必须分开声明**：结构同步、数据不同步，是默认且合理的——把两者绑成「全量同步」会让一次结构变更带走/覆盖生产数据。⑤ **跨环境迁移会改写归属**：owner 可能在新实例上被重指派。⇒ 迁移验收清单里必须有「权限/归属是否被改」这一项，否则迁移完成但责任人对不上。⑥ **环境间的"复制"要借道 Git 的合并能力，不要在应用内复制**：应用提供 push/pull 两端，合并语义交给真正的版本系统。
- **提升层**：工作流/发布治理。触发词：单向提升、one direction、删除不传播、outdated resources、credential stub、值缺失阻塞使用、schema 同步 row 不同步、owner 在 pull 时变更、跨环境不直接复制。
