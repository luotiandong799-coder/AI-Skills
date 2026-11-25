# 学习轮 r805C｜EI Amdahl与Gustafson（给豆包 · 2026-11-25）

> 轮号 r805C（上批 r804C）。共学两写 WB/豆包，Qoder 已卸载 qoder 席位移除。勿复用 r804 结论。本批遵用户追加指令按 13 模块顺序轮转，r805=TI/DI/EI。

## 三轮固定四列表（本轮行）
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r805C | meta/ei-reliability/SKILL.md | 1.16.0 | Amdahl 固定规模 S=1/((1−P)+P/N)，90% 可并行 N→∞ 也仅 10×；先扩大 P 而非堆核；忽略通信同步开销使理论上界偏乐观。 |

## 核心独点（供豆包写入 EI 模块记忆）
1. Amdahl 固定规模 S=1/((1−P)+P/N)，90% 可并行 N→∞ 也仅 10×；先扩大 P 而非堆核；忽略通信同步开销使理论上界偏乐观。
2. Gustafson 弱扩展规模随核增 S=N+(1−P)(1−N)，视角是执行时间恒定；Intel 32核1%串行得 31.69× vs same-P 误套 Amdahl 24.43×；前提串行不随规模同比增长。
3. 两定律 P 含义不同是最常见混淆（Amdahl 固定问题并行比例 vs Gustafson 放大后并行机测的比例）；报数必附定律+P定义+规模假设；先定应用画像再估上界实测。

## 一手来源（URL+日期）
- NVIDIA CUDA Best Practices 官方 WebFetch 全文 / Stanford Sol 组博士论文 WebFetch / Intel 官方 PDF WebFetch / HPC101 教程 WebFetch

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像无实体）。豆包对应经验也按此路由写入所属模块文件（本批 TI/DI/EI 各 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`），两方同守；Qoder 已卸载，`co-learn/qoder/` 禁止再写。用户级 MEMORY.md 保持纯指针索引（本批未写入）。

WB 已落地清单：r805A TI 贝叶斯因子 2.10.0 / r805B DI OODA 1.25.0 / r805C EI Amdahl-Gustafson 1.16.0（0 新建，全「增＝加厚现有」）。
