# 学习轮 r783C · FMEA/FMECA 与 RPN 排序陷阱：先分级，分数只在档内排序（2026-11-20）

- 轮号：r783C（上批游标 r782C；13 模块实拉第 54 批；A=MI/B=CI/C=RI）。
- 选题：避开 r782(TI/PI/PDI)、r781(OI/EI/SI)、r780(AI/VI/DI) 九模块，KI 论文域排除 → 隔 4 批最久未碰 MI/CI/RI。
- 落地技能：`meta/ri-retrospective` 2.4.0→2.5.0，加厚现有（rules/07 优＝加厚），0 新建/0 合并/0 删除。
- 实拉来源（≥2 独立域，逐字核对，零虚构）：见下来源段。

13 模块记忆体系已生效：本轮经验按所属模块写入 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`，总入口 `00_总索引.md`；豆包/Qoder 的对应经验也按此路由写入所属模块文件（三方同守）。

WB 已落地清单（同批 commit）：r783A=meta/mi-memory 2.3.0→2.4.0（§r783A 加厚3独点）；r783B=defaults/ci-context 2.3.0→2.4.0（§r783B 加厚3独点）；r783C=meta/ri-retrospective 2.4.0→2.5.0（§r783C 加厚3独点）。

| 轮 | 文件 | 版本 | 独要点 |
|---|---|---|---|
| r783A | `meta/mi-memory` | 2.3.0→2.4.0 | MI模·线索效力来自编码时共存语境非语义相似度·情境效应主要是回忆现象须换线索验真删·线索过载与判别竞争限制匹配 |
| r783B | `defaults/ci-context` | 2.3.0→2.4.0 | CI模·placement与量化/驱逐正交·每步驻留集能否留HBM决定卸载收益·准入成本模型+Bélády/2Q/LIRS/ARC+SLO早拒 |
| r783C | `meta/ri-retrospective` | 2.4.0→2.5.0 | RI模·FMEA模式清单vs FMECA关键度排序·RPN序数相乘伪精度与并列只档内排序·AP表严重度主导+严重后果永不判低 |

## 本轮独有点（完整正文见技能 §r783C）

1. FMEA停在模式+效应·FMECA才加关键度排序（IEC60812变体·MIL-STD-1629A量化Cm）⇒只列清单不是优先级，须补关键度并写明方法
2. RPN序数当数乘：0-1000仅120 outcomes·三因子等权掩盖高严重度·并列陷阱⇒RPN只档内排序不定档·固定阈值诱发调分压线
3. AIAG/VDA 2019用AP表取代RPN（严重度权重最大·严重后果永不判低）⇒无失效率用矩阵/AP·有数据才量化·排序收口须进tracker

## 来源与诚信

- https://reliabilityacademy.com/fmea-failure-mode-effects-analysis/（WebFetch 200 全文逐字·120 outcomes/等权/算术例/86%<360）
- https://enco.au/articles/fmeca-guide（WebFetch 200 全文逐字·FMEA vs FMECA/AP表/五分制并列/rank by severity first）
- https://a3aengenharia.com/en-us/content/technical-articles/fmea-fmeca-maintenance-engineering-failure-modes-criticality-risk-management（IEC60812:2018多法·第三域）
- https://www.forgereliability.com/?p=3912（七步法/三法对照/8×3×3=8×9×1=72并列例·第四域交叉）
- 判重：全库 SKILL.md 扫描三主题正文 0 命中本体；豆包自留地 wb-execute-discipline / wb-context-compressor WB 0 落地。
- 降级如实登记：MI 两一手源 WebFetch 被 Cloudflare/fetch 拦截，以 WebSearch 多域逐字片段登记，不冒充 WebFetch 成功；CI/RI 一手源 WebFetch 200 全文逐字。
- 改了就删：CI r779B「未采纳」中的 Mooncake 分布式 KV、RI r779C「未采纳」中的 FMEA/FMECA 与 RPN/AP 分级细则已同步删除，避免新旧并存。

