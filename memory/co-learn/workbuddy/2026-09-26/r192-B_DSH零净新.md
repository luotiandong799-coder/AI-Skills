# r192-B 学习轮审计：DSH Plugin Hub（dsh-plugin.org，0 净新）

日期：2026-09-26 | 角色：WorkBuddy（审计 + 落地）| 主源：`dsh-plugin.org`（用户 2026-09-18 计入 must-item；直连可达，无 VPN）

通道：`curl` 首页(171KB) + sitemap 索引 + plugins/tutorials 分类页 + 单插件详情页（`dsh-routing-suite`，154KB），直连 200。

## 一、实拉证据（逐源 + 成功/未达）

| 源 | 状态 | 要点 |
|---|---|---|
| 首页 | ✅ 200/171KB | 社区维护非官方插件市场；**11,117 插件索引 / 11,029 验证 / 89,904 stars**；11 类（UI/Sessions/Memory/Tools/Agents/Workflow/Integrations/Models/Dev/Knowledge/Fun）；「everything is a plugin」架构（模型/工具/技能/接口皆插件，可替换重组）；human-verified + traceable + 公开 stars/forks/update time；兼容性状态须标注；插件 export `apply(ctx)` 注册能力 |
| sitemap 索引 | ✅ 200 | pages / plugins(22,200 URL) / tutorials 三个子表 |
| /plugins / /tutorials | ✅ 200 | 列表可访 |
| /categories | ❌ 404 | 无该路径（分类在首页内联，非独立页） |
| 单插件 `dsh-routing-suite` 详情 | ✅ 200/154KB | 市场自身信任模型：Verified 徽章 + Listed/Page-last-updated + 公开 Stars 7,207 / Forks 177 / Open-issues / License MIT / Version 0.0.1-rc1 / Repo-last-push 2026-09-19 / Repo-created；插件正文含「runtime injector + 任务感知推理模式路由 + 分级任务协议 + 红队闸」、针对「长任务验证勤勉度衰减 / 首轮路由漏判」 |

## 二、判非重复理由（grep 在册 wb-skill-authoring 正文）

| 候选点 | grep 表达式 | 在册命中 | 判定 |
|---|---|---|---|
| 市场信任模型：human-verified 徽章 + 公开 stars/forks/open-issues + 溯源 repo/version/license/last-push + 新鲜度 page-updated | `技能推荐前质量三信号`、`安装数`、`来源信誉`、`GitHub stars`、`溯源`、`provenance`、`双 ?URL`、`内容哈希`、`检查时点`、`仓库级.*星标`、`漏斗`、`迭代次数.*质量` | `sa:977-979`（三信号：安装数/来源信誉/stars）、`sa:1361`（星标是仓库级非条目级）、`sa:1364`（溯源双 URL+内容哈希+checkedAt）、`sa:1365`（不可溯源者排除出索引）、`sa:1395`（downloads/installs/stars/versions 漏斗不同段）、`sa:1399`（迭代≠质量）、`sa:915`（provenance 块 + confidence） | **重叠>60% → 不落**（DSH 的信任信号是 sa 已系统性覆盖集合的子集，且 sa 已带更严判据：仓库级失真、双公式准入/排序分离、溯源四件齐） |
| 「everything is a plugin」组合架构 | `组合`、`插件架构`、`模块化` | 技能系统本就模块化；属框架设计哲学，非「提升 agent 技能系统哪一层」的可复用方法论点 | **不落**（架构哲学，无对应层） |
| 兼容性状态须标注（preview/breaking changes） | `compatibility`、`兼容性`、`版本.*标注` | `sa` frontmatter `compatibility` 字段（上限 500）+ glama 三轴已含 maintenance 轴；`wb-release-maintain` 版本化纪律 | **重叠>60% → 不落** |
| 插件正文：长任务验证勤勉度衰减 + 红队闸 + 分级任务协议 | `验证.*衰减`、`red.?team`、`分级任务`、`长任务` | `wb-execute-discipline` 已落「长任务保持验证 rigor / 重放边界 / 运行收据」；`wb-artifact-verification` 已立红队式独立证据 | **单插件 anecdote，未成体系 → 不入本轮**；转候选池（下轮深挖 DSH 插件 README 集群确认是否规模性存在） |

## 三、结论
B 轮 0 净新。DSH Plugin Hub 市场级方法论（信任/溯源/新鲜度/分类/兼容标注）已被 `wb-skill-authoring` 全面且更严地覆盖。无编造 idle commit。
候选池新增（不本轮落）：「长任务验证勤勉度衰减 → 须红队闸/分级任务协议维持」待下轮批量深读 DSH 插件 README 核验规模性后再判。
