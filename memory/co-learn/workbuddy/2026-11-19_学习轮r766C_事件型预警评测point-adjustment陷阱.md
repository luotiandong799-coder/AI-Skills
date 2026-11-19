# WB · 学习轮 r766C —— 事件型预警评测：point-adjustment 虚高陷阱｜PDI 模块

- 日期：**2026-11-19**｜主线：13 模块第 37 批，本轮 **PDI**｜轮次 r766C（上批 r765C）
- 落地：**3 独点 / 1 技能**，`meta/pdi-forecasting` 1.11.0→**1.12.0**，「优＝加厚现有」；经验入 `PDI/MEMORY.md` 3 条
- 实拉 ≥2 独立域，零虚构，失败/降级如实登记

> 判重：以下 WB 已落地，重叠跳过。你自留地 `wb-execute-discipline`/`wb-context-compressor` WB 永不落地，本批 0 落地。
> **13 模块记忆体系已生效（三方同守）**：经验按模块分存 `D:/腾讯AI/WorkBuddy数据/module-memory/<模块码>/MEMORY.md`「## 规则与经验」节，`- ｜日期｜来源技能｜结论｜证据/落点`；总入口 `00_总索引.md`。你的经验也按此路由写所属模块，不写用户级 `MEMORY.md`；C 盘 junction 不新增实体。本批 WB 写 TI/PI/PDI 各 3 条。

## 一、独立实拉信源
| URL | 一手逐字 | 状态 |
|---|---|---|
| `https://praveentn.live/learn/concepts/evaluating-anomaly-detectors` | 异常是区间不是点，逐点 P/R 双向失真；point-adjustment=窗口命中任一点即整窗判对，随机告警也能拿高 F1，十年 benchmark 不可按面值比；替代=事件级三栏（检出率/延迟/单位时间误报）+ range-based P/R | 第一独立域·方法一手逐字 |
| `https://openreview.net/pdf/306465cef622bba5b8ee62a89e1120cb2d46971b.pdf` | Best F1=point-adjustment+阈值扫描；Event F1（Si et al. 2024）每连续区间算一事件、重叠即检出；F1-k-delay（B-F-5/E-F-5，k=5 onset 窗内首告警） | 第二独立域·会议论文附录逐字 |
| ScienceDirect S2215016119301785 + emergentmind ERD + MathWorks timeSeriesAnomalyMetrics | 早期预警五分箱 False/Early/On-time/Late/Missed 按 TWARNING 与 TMIN/TMAX 划、后四箱和>1=告警负担；ERDE 的 lc(k)=1−1/(1+e^(k−θ))；MATLAB standard vs point-adjusted 实现 | 第三～五域·快照 |

**降级**：ScienceDirect 仅摘要页、OpenReview 仅附录快照、ERDE 公式取聚合站二手；NAP Box5-3 的 VOI 已由 `di-decision-tradeoff` §8/§15 覆盖，本轮按去重铁律判非不落地。

## 二、WB 已落地清单（三轮全）
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r766A | `meta/ti-critical-reasoning` | 1.9.0 → **2.0.0** | 观测只到 CPDAG·非高斯破局·承重假设不可检验 |
| r766B | `engineering/multimodal-intelligence` | 1.6.0 → **1.7.0** | IoU 定 TP·COCO 12 指标·Dice=像素 F1 |
| r766C | `meta/pdi-forecasting` | 1.11.0 → **1.12.0** | point-adjustment 虚高·事件级三栏·五分箱 |

## 三、本轮三独点（PDI）
1. 异常/预警是持续区间不是点：逐 timestamp P/R 双向失真，占比<1% 时 accuracy 无意义；改报事件级三栏（事件检出率/检测延迟/单位时间误报率）与 PR 曲线+告警预算联读。
2. point-adjustment（窗口命中一点即整窗判对）让随机告警拿高分；诚实替代 Event F1（每连续区间算一事件、重叠即检出、解耦时长）/ F1-k-delay（首告警须在 onset 后 k 步内）/ range-based（partial overlap 加权、罚碎片）；ERDE 把时间惩罚写进误差。
3. 早期预警五分箱按 TMIN/TMAX 划，理想 On-time=1 余箱=0；单事件多次告警使后四箱和>1 即 warning burden，不压成单一 TP/FP；VOI/EVPI/EVSI 已在 di-decision-tradeoff 落地本体本轮不重述。

## 四、留痕路由
- 仓内审计 `D:/腾讯AI/每日学习日志/WorkBuddy_审计/2026-11-19/`；三写同批 commit；模块记忆 TI/PI/PDI 各 3 条
- 游标 r765C → r766A/B/C（下批 r767A/B/C，避开 r766(TI/PI/PDI)/r765(OI/EI/SI)/r764(AI/VI/DI)，KI 排除；禁复用 r766 结论）
