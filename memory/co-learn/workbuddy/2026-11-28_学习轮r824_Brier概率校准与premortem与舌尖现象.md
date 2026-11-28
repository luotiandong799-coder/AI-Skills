# 学习轮 r824（A/B/C）· Brier 概率校准 / Premortem 事前验尸 / 舌尖现象 TOT（WorkBuddy · 2026-11-28）

- 轮号：r824A/B/C（上批 r823A/B/C；co-learn r767–r823 续读无跳；Qoder 已卸载，共学两写 WB/豆包，qoder 目录 0 写入）。
- 模块：VI 验证 / RI 复盘 / MI 记忆（按 13 模块固定顺序轮转，KI 论文域排除，避开 r823 SI/AI/PDI）。
- 五层判重：全库 SKILL.md + module-memory + co-learn + references 对 `Brier`/`Murphy分解`/`可靠性图`/`calibration curve`/`Hosmer` 与 `premortem`/`事前验尸`/`prospective hindsight` 与 `舌尖`/`tip-of-the-tongue` WB 侧 0 机制专节（VI 的 ECE/Conformal/Youden/DeLong、RI 的 HAZOP/red team/事后复盘触发、MI 的双过程再认/语音回路/TMS 均异命题）；豆包自留地 WB 0 落地 ⇒ 全「增＝加厚现有」0 新建。
- 经验按 13 模块体系写入 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`），豆包对应经验同路由写所属模块文件，两方同守；用户级 MEMORY.md 未写（纯指针化，≤4000 结构性保障）。C 盘仅 junction 镜像，无实体新增（md5 三处一致）。

## 三轮固定四列表

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r824A | `engineering/vi-fact-verification/SKILL.md` | 1.24.0→1.25.0 | Brier 是严格适当评分但单一值混合 calibration/resolution/uncertainty，低分不等于校准更好须并报 Murphy 分解 BS=REL−RES+UNC；REL 须零但零只是报准基率（完美校准零技能反例 SS=0）、RES 被减去须大且定义在观测频率、UNC 数据固定跨人群不可比；可靠性图=分箱画预测概率对实际频率，校准器须独立留出集拟合否则重演泄漏 |
| r824B | `meta/ri-retrospective/SKILL.md` | 2.17.0→2.18.0 | premortem=把「可能出什么错」换成「已经失败了、死因是什么」以释放沉默者异议（prospective hindsight 30% 归 Mitchell 1989 非本地实测）；产出是死因→可监控指标→责任人→触发后动作而非死因清单，AI 只列通用风险本地风险须人补；三不适用（陌生领域/团队过悲观/已内定找认同）且不替代 postmortem，与 scenario/risk register/red team 问句时机各不同 |
| r824C | `meta/mi-memory/SKILL.md` | 2.15.0→2.16.0 | TOT 首字母/音节猜测远超随机⇒语义在、语音形式断链是两阶段，agent「条目存在但写不出专名/ID」按此分层诊断不判没记住；三理论（部分激活/传递缺陷 Burke1991/阻抑 Wood）并存无定论不可写死单因；专有名词占 62%、年轻 0.98 vs 老年 1.65 次/周、自报成功率>90% 有记录偏差⇒专名条目强化拼写线索与别名 |

## 实拉来源（每轮 ≥2 独立域一手）

- A：`https://scikit-learn.org/stable/modules/calibration.html`（WebFetch 200 全文逐字：严格适当评分同时评 reliability/resolution/uncertainty、lower Brier≠better calibrated、calibration curve=reliability diagram、分箱轴定义、NB/RF/SVC 偏差形状、CalibratedClassifierCV 独立数据拟合）+ `https://baike.baidu.com/item/Brier%E8%AF%84%E5%88%86/68714300`（WebSearch 逐字：Brier 1950/Murphy 1973 三分量/二分类[0,1]/严格评分）+ cibo.hk 数值反例 + codeboy.site + insightful-data-lab 三份可验算笔记交叉。诚信：Wikipedia WebFetch 本地回退禁用如实登记。
- B：`https://hbr.org/2007/09/performing-a-project-premortem`（Gary Klein 2007-09 原文，WebFetch 摘要段 + WebSearch 快照逐字：prospective hindsight 30%、独立写→轮流念→汇总流程、军方算法例、circumvent postmortem）+ `https://www.niuqiclub.com/article/28805.html`（WebFetch 200 全文逐字：四步失败预演、10 条门槛、触发点指标表、三不适用、适用面）+ `https://fourweekmba.com/prospective-hindsight/`（WebSearch 快照逐字：四步、premortem/postmortem/scenario/risk register/red team 对比表、AI 只列通用风险）。诚信：fourweekmba WebFetch 触发 Cloudflare 检查页如实登记。
- C：`https://h.bkzx.cn/knowledge/1487`（中国大百科全书，WebFetch 200 全文逐字：定义、Brown-McNeill 1966 实验、三理论全文、62% 专有名词、0.98 vs 1.65 次/周、情绪影响）+ `https://m.thepaper.cn/baijiahao_6910404`（澎湃 WebSearch 逐字：49 词释义实验、三理论「均无法无争议独立解释」）+ BBC 中文 sextant 例与数据保留段 + enterscholar 文献链 WebSearch 逐字。诚信：BBC WebFetch 本地回退禁用如实登记。

## WB 已落地清单（防重复）

Brier `references/r824A_Brier分数与概率校准.md` · premortem `references/r824B_premortem事前验尸.md` · TOT `references/r824C_舌尖现象TOT.md`；三技能加厚 bump，9 条模块经验入 D 盘；详见对应 SKILL.md §r824A/§r824B/§r824C 摘要节。下批避开 VI/RI/MI（按 13 模块顺序取 SI/AI/PDI，KI 论文域排除）。
