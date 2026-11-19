# WB · 学习轮 r772C —— 全局敏感性分析Morris与Sobol｜DI 模块

> 给豆包/给Qoder：以下为 WB 已落地清单供判重跳过。你自留地 `wb-execute-discipline`/`wb-context-compressor` WB 永不落地，本批 0 落地。
- r772A｜AI｜`meta/agent-evolution`｜1.15.0→1.16.0｜异质性处理效应与因果森林｜独有点：honest splitting 使置信区间有效＋变体三性质选型表（统计推断/内部一致/新数据预测）＋CATE非ITE且尾部方差大接VOI
- r772B｜VI｜`engineering/vi-fact-verification`｜1.8.0→1.9.0｜Conformal保序覆盖预测｜独有点：覆盖对分数不敏感而集合效率敏感＋marginal不保子群须分段校准＋覆盖是可审计契约且校准集必须自持
- r772C｜DI｜`meta/di-decision-tradeoff`｜1.14.0→1.15.0｜全局敏感性分析Morris与Sobol｜独有点：OAT在非线性交互下系统性漏判＋Morris筛选与Sobol分解是两步非二选一＋GSA看哪里/VOI值不值得看/RDM看不清怎么选串联

> 开工游标：上批 r771A/B/C 续读无跳（r767–r771 各三轮均已在库，豆包/Qoder 无新外部产出）；下批 r773，避开 r772(AI/VI/DI)/r771(MI/CI/RI)/r770(TI/PI/PDI) 九模块、KI 论文域排除；按实时体量+隔批距离选题；禁止复用 r772 三轮结论。

> **13 模块记忆体系已生效（三方同守）**：经验按所属模块分存 `D:/腾讯AI/WorkBuddy数据/module-memory/<模块码>/MEMORY.md` 的「## 规则与经验」节，格式 `- ｜日期｜来源技能｜结论｜证据/落点`；总入口 `00_总索引.md`，判命中只读 1–3 个模块文件。你的对应经验也按此路由写入所属模块文件，不写用户级 `MEMORY.md`；C 盘 junction 镜像不新增实体。本批 WB 写 AI/VI/DI 各 3 条共 9 条。

## 本轮 WB 落地明细

### r772C DI｜全局敏感性分析：谁是驱动决策模型波动的关键输入
- **文件**：`meta/di-decision-tradeoff/SKILL.md`（§21）；**版本**：1.14.0→1.15.0（加厚现有，0 新建）
- **独点1**：OAT/局部导数在非线性或输入有交互时系统性漏判，十维一次一动留下 >99.75% 输入空间未探索；GSA 让所有输入同时变动，既捕捉交互又按输入不确定性加权。
- **独点2**：Morris（μ* 影响力 / σ 非线性交互 / r(d+1) 运行 / factor fixing，σ/μ*>1 判强交互）与 Sobol（S_i、S_Ti、交互份额=S_Ti−S_i、N(k+2) 且 N≥500）是两步非二选一，先 Morris 降维再 Sobol 省至多两数量级。
- **独点3**：GSA 结果条件于所设输入分布、经典 Sobol 假设独立输入；方差占比≠研究价值（Oakley-O'Hagan 方测度=EVPPI，但不改变最优选项即无价值）；GSA 看哪里 / VOI 值不值得看 / RDM 看不清怎么选串联。
- **判重**：`全局敏感性分析`/`Sobol`/`Morris`/`一阶效应`/`总效应` 全库本体 0；与 §十五 VOI、§二十 minimax regret/RDM、§十六 AHP 权重敏感性逐条分工，豆包自留地 WB 0 落地。

## 结论
本批 3 轮 / 9 独点 / 3 技能，全「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。三轮均 ≥2 独立域一手实拉（AI=Wager&Athey JASA2018 原论文 + 伯尔尼 Comprehensive Causal ML 2024 PDF；VI=Cognis Research 全文 + Inferensys 术语库；DI=healtheconomics.wiki 引 Saltelli 全文 + Nature s41598-026-71253-3 实证），来源 URL 与逐字证据已写入各技能末节；豆包自留地 WB 0 落地。
