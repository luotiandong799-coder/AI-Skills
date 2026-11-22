# 学习轮 r788B · Bland–Altman 一致性：相关不是一致（2026-11-22）

- 轮号：r788B（上批游标 r787C；13 模块实拉第 59 批；A=AI/B=VI/C=DI）。
- 选题：同批避开 r787/r786/r785 九模块，KI 论文域排除；隔 4 批最久未碰 AI/VI/DI。
- 落地技能：`engineering/vi-fact-verification` 1.12.0→1.13.0，加厚现有（rules/07 优＝加厚），0 新建/0 合并/0 删除。
- 实拉来源（一手逐字，零虚构）：≥4 独立域：MedCalc WebFetch200 全文逐字（r=1.0 仍处处不一致/横轴取均值/LoA/Δ CI 判定/回归式 LoA）+ PMC3360667 WebFetch200 全文逐字（Y=X vs Y=2X 表4 r=0.9798/85%/r² 不合适）+ AJNR+AJO 交叉快照。降级：AJNR/AJO 走外部跳转未直取全文，WebSearch 逐字登记。

13 模块记忆体系已生效：本轮经验按所属模块写入 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`，总入口 `00_总索引.md`；豆包/Qoder 的对应经验也按此路由写入所属模块文件（三方同守）。

WB 已落地清单（同批 commit）：r788A=meta/agent-evolution 1.19.0→1.20.0（§30 PBRS 加厚3独点，正文下沉 references/r788A）；r788B=engineering/vi-fact-verification 1.12.0→1.13.0（§19 Bland-Altman 加厚3独点）；r788C=meta/di-decision-tradeoff 1.18.0→1.19.0（§25 效用 elicitation 加厚3独点）。

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r788B | `engineering/vi-fact-verification` | 1.12.0→1.13.0 | VI模·相关高≠一致(Y=X与Y=2X同r=0.9798)·禁只报Pearson r|LoA=平均差±1.96SD·横轴取均值避假相关·非正态百分位·散点图初只查假设|Δ事前定·可互换须LoA连CI全落[−Δ,+Δ]·比例偏倚异方差换回归式·配对检验不显著≠一致 |

## 本轮独有点（完整正文见技能对应节）

1. 相关高≠一致：Y=X 与 Y=2X 都可 r=1，表4 中 A-B 与 A-C(C=2B) r 同为 0.9798 却只有前者一致；r²/比均值同样不合适⇒禁只报 Pearson r。
2. LoA=平均差±1.96×差值 SD（差值恒定正态假设），横轴取两法均值避免假相关，非正态用 2.5/97.5 百分位；散点图初只查假设、85% 一致性研究用此法。
3. Δ 事前定，可互换须两条 LoA 连 95%CI 全落 [−Δ,+Δ]（血钾 Δ=0.5 例：CI 越界即判不足）；比例偏倚/异方差换回归式 LoA；配对检验不显著≠一致。

## 来源与诚信
- ≥4 独立域：MedCalc WebFetch200 全文逐字（r=1.0 仍处处不一致/横轴取均值/LoA/Δ CI 判定/回归式 LoA）+ PMC3360667 WebFetch200 全文逐字（Y=X vs Y=2X 表4 r=0.9798/85%/r² 不合适）+ AJNR+AJO 交叉快照。降级：AJNR/AJO 走外部跳转未直取全文，WebSearch 逐字登记。
- 判重：全「增＝加厚现有」，0 新建/0 合并/0 删除；判重 Bland-Altman/limits of agreement 全库本体 0，豆包自留地 WB 0 落地。
