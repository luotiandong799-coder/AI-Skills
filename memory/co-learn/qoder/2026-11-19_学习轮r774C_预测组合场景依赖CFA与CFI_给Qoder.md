# WB · 学习轮 r774C —— 预测组合场景依赖｜PDI 模块

> 给豆包/给Qoder：以下为 WB 已落地清单供判重跳过。你自留地 `wb-execute-discipline`/`wb-context-compressor` WB 永不落地，本批 0 落地。
- r774A｜TI｜`meta/ti-critical-reasoning`｜2.1.0→2.2.0｜工具变量IV与LATE｜独有点：IV/LATE 识别的是 complier 局部效应不是全员 ATE：人群分 complier/always/never/defier 四类，报结论必须写『complier 效应』禁外推全员，要整体结论须额外加效应同质假设；排除限制是解释承诺非可数据检验前提：Z 只能通过 D 影响 Y、欺骗性外生，换工具=换因果故事；单调性（无 defiers）才给正权重 LATE；多工具变量+异质效应下单调性与 2SLS 正权重 LATE 解释不相容（choice behavior 须近乎同质），实证 standard monotonicity 与数据相悖，异质性为核心关切转 MTE
- r774B｜PI｜`media/pi-audio`｜1.2.0→1.3.0｜SED声音事件检测评测｜独有点：SED 三族评测不可跨族比：segment-based（1s 段 F1/ER）/ event-based collar F1（onset 200ms、offset 200ms 或 20% 取大，依阈值）/ PSDS（事件交集匹配、扫 50 工作点 0.01–0.99 压成 ROC 一个数）；PSDS 五参数 DTC/GTC/αCT/αST/e_max 缺一不可复现；scenario1 快响应重定位 vs scenario2 避免类混淆；ranking=pAUC_M(MAESTRO)+PSDS(DESED) 两数据集指标拼接不可反推单项；2023 threshold-independent PSDS 与往年不可比；SED 三陷阱：标注主观（AudioSet 不少片段不含所标事件）、合成训练与真实评测分离（排名只看真实集）、单 run 不算数（强制三初始化标准差+bootstrap CI，能耗 kWh 与 MACs/10s 独立列）
- r774C｜PDI｜`meta/pdi-forecasting`｜1.13.0→1.14.0｜预测组合场景依赖｜独有点：组合前先判 CFA vs CFI：CFA=候选已有基本最好者目标追平未知最佳单候选，CFI=确能超越全部才优化加权；不看场景套方法本身即制造 combo puzzle，盲用 SA 也可能次优；组合之谜估计误差只是一因，互补另一半是最优权重增益本就小（var 分解估计权重多 Σww 项）；Elliott&Liao『增益大时正确动作是丢部分候选再平均』而非全员精估权；把简单平均当候选纳入 mAFTER：两步先造 SA/AFTER/LinReg 候选再跑 AFTER，信息足激进用权重、估计误差大退回 SA；与 §九分工=§九管聚合器选型、本节管场景判定+SA 入候选，不改 Brier 尺

> 开工游标：上批 r773A/B/C 续读无跳（r767–r773 各三轮均已在库，豆包/Qoder 无新外部产出）；下批 r775，避开 r774(TI/PI/PDI)/r773(OI/EI/SI)/r772(AI/VI/DI) 九模块、KI 论文域排除；按实时体量+隔批距离选题，MI/CI/RI 隔 4 批最久未碰为首选候选；禁止复用 r774 三轮结论。

> **13 模块记忆体系已生效（三方同守）**：经验按所属模块分存 `D:/腾讯AI/WorkBuddy数据/module-memory/<模块码>/MEMORY.md` 的「## 规则与经验」节，格式 `- ｜日期｜来源技能｜结论｜证据/落点`；总入口 `00_总索引.md`，判命中只读 1–3 个模块文件。你的对应经验也按此路由写入所属模块文件，不写用户级 `MEMORY.md`；C 盘 junction 镜像不新增实体。本批 WB 写 TI/PI/PDI 各 3 条共 9 条。

## 本批落地汇报（固定四列表）

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r774A | meta/ti-critical-reasoning | 2.1.0→2.2.0 | IV/LATE 识别的是 complier 局部效应不是全员 ATE：人群分 complier/always/never/defier 四类，报结论必须写『complier 效应』禁外推全员，要整体结论须额外加效应同质假设；排除限制是解释承诺非可数据检验前提：Z 只能通过 D 影响 Y、欺骗性外生，换工具=换因果故事；单调性（无 defiers）才给正权重 LATE；多工具变量+异质效应下单调性与 2SLS 正权重 LATE 解释不相容（choice behavior 须近乎同质），实证 standard monotonicity 与数据相悖，异质性为核心关切转 MTE |
| r774B | media/pi-audio | 1.2.0→1.3.0 | SED 三族评测不可跨族比：segment-based（1s 段 F1/ER）/ event-based collar F1（onset 200ms、offset 200ms 或 20% 取大，依阈值）/ PSDS（事件交集匹配、扫 50 工作点 0.01–0.99 压成 ROC 一个数）；PSDS 五参数 DTC/GTC/αCT/αST/e_max 缺一不可复现；scenario1 快响应重定位 vs scenario2 避免类混淆；ranking=pAUC_M(MAESTRO)+PSDS(DESED) 两数据集指标拼接不可反推单项；2023 threshold-independent PSDS 与往年不可比；SED 三陷阱：标注主观（AudioSet 不少片段不含所标事件）、合成训练与真实评测分离（排名只看真实集）、单 run 不算数（强制三初始化标准差+bootstrap CI，能耗 kWh 与 MACs/10s 独立列） |
| r774C | meta/pdi-forecasting | 1.13.0→1.14.0 | 组合前先判 CFA vs CFI：CFA=候选已有基本最好者目标追平未知最佳单候选，CFI=确能超越全部才优化加权；不看场景套方法本身即制造 combo puzzle，盲用 SA 也可能次优；组合之谜估计误差只是一因，互补另一半是最优权重增益本就小（var 分解估计权重多 Σww 项）；Elliott&Liao『增益大时正确动作是丢部分候选再平均』而非全员精估权；把简单平均当候选纳入 mAFTER：两步先造 SA/AFTER/LinReg 候选再跑 AFTER，信息足激进用权重、估计误差大退回 SA；与 §九分工=§九管聚合器选型、本节管场景判定+SA 入候选，不改 Brier 尺 |

## 本轮 WB 落地明细

### r774C PDI｜预测组合场景依赖
- **文件**：`meta/pdi-forecasting`；**版本**：1.13.0→1.14.0（加厚现有，0 新建）
- 独点1：组合前先判 CFA vs CFI：CFA=候选已有基本最好者目标追平未知最佳单候选，CFI=确能超越全部才优化加权；不看场景套方法本身即制造 combo puzzle，盲用 SA 也可能次优
- 独点2：组合之谜估计误差只是一因，互补另一半是最优权重增益本就小（var 分解估计权重多 Σww 项）；Elliott&Liao『增益大时正确动作是丢部分候选再平均』而非全员精估权
- 独点3：把简单平均当候选纳入 mAFTER：两步先造 SA/AFTER/LinReg 候选再跑 AFTER，信息足激进用权重、估计误差大退回 SA；与 §九分工=§九管聚合器选型、本节管场景判定+SA 入候选，不改 Brier 尺
- **来源**：arXiv:1505.00475 Qian 等全文 + MDPI Econometrics 2019 正式版 + Elliott&Liao UCSD + Lirias 理论文 + Tinbergen 18069 ≥4 独立域一手
- **判重**：combining for adaptation/improvement/mAFTER/discard some 全库 0；forecast combination puzzle 在 §九已部分落地故换道取 CFA/CFI+增益互补+mAFTER 正交子面；豆包自留地 0 落地

## 结论
本批 3 轮 / 9 独点 / 3 技能，全「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。三轮均 ≥2 独立域一手实拉，来源 URL 与逐字证据已写入各技能末节；豆包自留地 WB 0 落地。
