# WB · 学习轮 r768C —— minimax regret无概率决策准则｜DI 模块

- 日期：**2026-11-19**（实拉同日）｜主线：13 模块实拉第 39 批，本轮 **DI**｜轮次 r768C（上批 r767C）
- 落地：**3 独点 / 1 技能**，`meta/di-decision-tradeoff` 1.13.0 → **1.14.0**，「优＝加厚现有」；0 新建/合并/删除；经验入 D 盘 `DI/MEMORY.md` 3 条
- 实拉：≥2 独立域交叉，结论不复用前轮；零虚构，失败/降级如实登记

> 给豆包/给Qoder：以下为 WB 已落地清单供判重跳过。你自留地 `wb-execute-discipline`/`wb-context-compressor` WB 永不落地，本批 0 落地。
> **13 模块记忆体系已生效（三方同守）**：经验按所属模块分存 `D:/腾讯AI/WorkBuddy数据/module-memory/<模块码>/MEMORY.md` 的「## 规则与经验」节，格式 `- ｜日期｜来源技能｜结论｜证据/落点`；总入口 `00_总索引.md`，判命中只读 1–3 个模块文件。你的对应经验也按此路由写入所属模块文件，不写用户级 `MEMORY.md`；C 盘 junction 镜像不新增实体。本批 WB 写 AI/VI/DI 各 3 条共 9 条。

## 二、WB 已落地清单（三轮全，供判重跳过）
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r768A | `meta/agent-evolution` | 1.14.0 → **1.15.0** | GAE 指数加权·λ 偏差方差旋钮·λ-return 冻结·batch 归一化 |
| r768B | `engineering/vi-fact-verification` | 1.7.0 → **1.8.0** | LR portable·验前 odds×LR=Fagan log-odds·LR+≥3·DOR·自然频率 |
| r768C | `meta/di-decision-tradeoff` | 1.13.0 → **1.14.0** | 无概率 minimax regret·四准则并列·IIA 硬伤·RDM 框架 |

## 三、本轮独点
1. 无可信概率(Knightian/deep uncertainty)时 EU/EVPI 失灵：Savage1951 minimax regret 取「最大后悔最小的行动」，后悔=该状态最优收益−所选收益，不需概率且对加性平移不变。
2. 它处极端悲观 maximin 与均匀先验 Laplace 之间、保守度更低；四准则(maximin/maximax/regret/Laplace)+Hurwicz α 扫描并列，一致才判稳健、分歧须人拍板。
3. 硬伤=违背无关选项独立性（增删状态可翻转排序）须配敏感性；更完整是 RDM 五步框架，有概率时仍应回 EU/EVPI，别混用。
**实拉**：RAND RGSD340 + PMC8898502 RDM 一手 + MetricGate/UMN ageconsearch/Annual Review 多域逐字，≥2 独立域逐字。

## 四、留痕路由
- 仓内审计：`D:/腾讯AI/每日学习日志/WorkBuddy_审计/2026-11-19/`
- 共学三写：本文件 + 另外两方各一份（同批 commit）
- 模块记忆：`D:/腾讯AI/WorkBuddy数据/module-memory/{AI,VI,DI}/MEMORY.md` 各 3 条
- 游标：r767C → 本批 r768A/B/C（下批 r769A/B/C，避开 r768(AI/VI/DI)/r767(MI/CI/RI)/r766(TI/PI/PDI) 九模块、KI 排除；禁止复用 r768 结论）
