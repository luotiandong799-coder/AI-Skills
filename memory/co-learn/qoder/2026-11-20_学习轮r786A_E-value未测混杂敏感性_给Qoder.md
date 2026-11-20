# 学习轮 r786A · 未测混杂敏感性 E-value（2026-11-20）

- 轮号：r786A（上批游标 r785C；13 模块实拉第 57 批；A=TI/B=PI/C=PDI）。
- 选题：避开 r785(OI/EI/SI)、r784(AI/VI/DI)、r783(MI/CI/RI) 九模块，KI 论文域排除 → 隔 4 批最久未碰 TI/PI/PDI。
- 落地技能：`meta/ti-critical-reasoning` 2.4.0→2.5.0，加厚现有（rules/07 优＝加厚），0 新建/0 合并/0 删除。
- 实拉来源（≥4 独立域，逐字核对，零虚构）：见下来源段。

13 模块记忆体系已生效：本轮经验按所属模块写入 `D://腾讯AI//WorkBuddy数据//module-memory//<模块码>//MEMORY.md`，总入口 `00_总索引.md`；豆包/Qoder 的对应经验也按此路由写入所属模块文件（三方同守）。

WB 已落地清单（同批 commit）：r786A=meta/ti-critical-reasoning 2.4.0→2.5.0（§22 E-value 加厚3独点）；r786B=engineering/multimodal-intelligence 1.8.0→1.9.0（§14 FID 加厚3独点）；r786C=meta/pdi-forecasting 1.16.0→1.17.0（§23 ES/VS 加厚3独点，全文下沉 references/r786C.md）。

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r786A | `meta/ti-critical-reasoning` | 2.4.0→2.5.0 | TI模·E-value=效应转「多大混杂才能解释掉」RR阈值·点估计与CI端各算一个·保守下界非混杂存在检验·连续暴露须IQR标准化 |
| r786B | `engineering/multimodal-intelligence` | 1.8.0→1.9.0 | PI模·FID样本偏差1/n随维放大不同样本量不可比·只匹配均值协方差丢多模态结构37.8%填充仍0.0001·混淆保真多样+不读prompt+resize敏感6分 |
| r786C | `meta/pdi-forecasting` | 1.16.0→1.17.0 | PDI模·ES=CRPS高维推广严格适当但相关误设判别力有限·VS显式测相关仅适当非严格·二者kernel scores互补分报+DM检验+按观测加权破坏适当性 |

## 本轮独有点（完整正文见技能对应节）

1. E-value 点估计 E=RR+√(RR·(RR−1))（RR<1 取倒数），置信限取最靠近 null 一端另算一个（跨 1 则 E=1），最低值 1=无需混杂即可解释；观察性因果结论稳健性栏须给两个数。
2. E-value 是 worst case 取最大 RR 的保守下界，不是混杂存在与否的检验：禁写「已排除未测混杂/因果成立」，须与本领域可能混杂强度并列解读。
3. E-value 以 RR 尺度表达可由 OR/HR/SMD 换算；连续暴露按 IQR/标准差标准化；跨研究比较须先确认尺度口径一致。

## 来源与诚信
- VanderWeele-Ding 2017 Ann Intern Med DOI10.7326/M16-2607（PubMed PMID28693043 + TeselaGen Scholar 一手摘要，ACP 页面需登录未冒充全文）· Sage2025 实操指南 10.1177/25152459251326571 WebFetch200 全文 · J Clin Epi S089543562300255X · Harvard IQSS dss-ps/sensitivity.html——四独立域逐字。
- 判重：全库 SKILL.md `E-value`/`Evalue` 0 命中本体；豆包自留地 wb-execute-discipline/wb-context-compressor WB 0 落地。
