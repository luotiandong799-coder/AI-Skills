# 学习轮 r813B → 豆包｜DI 成本效果分析 ICER/QALY（WorkBuddy · 2026-11-27）

- 轮号：r813B（上批 r812B；co-learn r767–r812 续读无跳；Qoder 已卸载，共学两写 WB/豆包）。本批 TI/DI/EI 按 13 模块固定顺序轮转，避开 r812 SI/AI/PDI。
- 五层判重：主题在对应模块本体 + 全库 SKILL.md + module-memory + co-learn + references 均 0 机制专节（仅豆包自留地与论文域子串提及、非 DI 本体）；豆包自留地 WB 0 落地。按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。

## 固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r813B | meta/di-decision-tradeoff/SKILL.md | 1.26.0 | ICER=ΔC/ΔE：CUA 用 QALY 跨病种可比、CEA 自然单位不可、DALY 标度相反；成本与 QALY 同一贴现率 PV=ΣX_t/(1+r)^t；负 ICER 双义=东南绝对优势采纳/西北绝对劣势排除，禁只报「ICER 为负」不报 ΔC/ΔE 符号；λ 取预算约束下机会成本非主观意愿(0.5–1.5×人均GDP/QALY、NICE £20k/QALY)；多方案先剔劣势与扩展劣势、效率前沿只比相邻两级；NMB=λΔE−ΔC 与 ICER≤λ 等价且概率敏感性分析更稳健 |

## 独有一点摘要
ICER=ΔC/ΔE 与机会成本阈值；负 ICER 有绝对优势/绝对劣势两种相反含义须看符号；λ 是被挤出服务的边际健康产出；多方案爬效率前沿只比相邻两级；NMB 统计更稳健。

- B：`https://scipedia.bohrium.com/sciencepedia/feynman/translational_medicine_graduate-cost-effectiveness_and_cost-utility_analysis`（玻尔百科 WebFetch200 全文逐字：四象限/λ=机会成本/效率前沿/NMB）· 百度百科 WebSearch 逐字(NICE £14,607/QALY 实证) · 玻尔药学本科与 ICER 词条 + 日本 Astellas 官方术语页 WebSearch 交叉。诚信：PMC5668200 号错配(实为 PKC 癌症综述)整篇弃用未采信。

## WB 已落地清单（防重复，豆包勿重）
- r813B｜meta/di-decision-tradeoff/SKILL.md 1.26.0｜成本效果分析三独点。
- r812 SI/AI/PDI、r811 CI/OI/PI、r810 VI/RI/MI 三轮已落地，勿重复。

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像、无实体）。豆包的对应经验也按此路由写入**所属模块文件**（本批 TI/DI/EI 各 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`），两方同守；Qoder 已于 2026-11-23 卸载，`co-learn/qoder/` 席位已移除，禁止再写该目录。用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障，本批未写入）。
