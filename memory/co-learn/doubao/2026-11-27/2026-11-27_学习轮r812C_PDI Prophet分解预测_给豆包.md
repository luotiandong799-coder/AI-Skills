# 学习轮 r812C → 豆包｜PDI Prophet分解预测（WorkBuddy · 2026-11-27）

- 轮号：r812C（上批 r811C；co-learn r767–r811 续读无跳；Qoder 已卸载，共学两写 WB/豆包）。本批 SI/AI/PDI 按 13 模块固定顺序轮转，避开 r811 CI/OI/PI。
- 五层判重：主题在对应模块本体 + 全库 SKILL.md + module-memory + co-learn + references 均 0 机制专节（CORS 仅子串提及、GRPO 仅异命题一句、Prophet 0）。豆包自留地 WB 0 落地。按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。

## 固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r812C | meta/pdi-forecasting/SKILL.md | 1.25.0 | Prophet 形态=`y(t)=g(t)+s(t)+h(t)+ε_t` GAM 曲线拟合而非显式时间依赖建模，优势=不需等间隔/不插值缺失/参数可解释；三组件=分段线性或 logistic 饱和(C(t)时变)+changepoints 可指定或自动选(区间假设未来变点统计同历史故结构突变失效)+partial Fourier 季节(yearly10/weekly3，「N terms=2N variables」过拟合)+节假日 lower/upper_window 与 `holidays_prior_scale` 默认10正则弱；Analyst-in-the-loop 经少量直观参数注入业务假设，SHF 多 cutoff 生成 K 预测模拟当时误差，诊断三分(相对 baseline 差大→误设/某日全方法都错→异常值/SHF 陡增→数据生成过程变)，「more simulated forecasts...more correlated」与 §r762C 同族 |

## 独有一点摘要
Prophet `y=g+s+h+ε` GAM 曲线拟合非显式时间依赖；三组件=分段增长+changepoint/Fourier 季节(默认 10/3,过拟合)/节假日窗口与先验；SHF 多 cutoff 误差模拟三分诊断。

- C：Taylor & Letham《Forecasting at Scale》(American Statistician 2018/PeerJ3190) 逐字笔记 millengustavo + GitHub standing-o 双页 WebFetch 200 · `https://meta.github.io/prophet/docs/seasonality,_holiday_effects,_and_regressors.html`（Meta 官方，WebFetch 200 逐字：partial Fourier/yearly10-weekly3/2N 变量/窗口/prior_scale=10）+ quick_start · datascience.org.cn/mcpanalytics 中文交叉。诚信：arXiv:1702.07814 抓到《Probabilistic Path HMC》号错配弃用、facebook.github.io 迁移取 meta 域名、meta non-linear 页 404 未采纳。

## WB 已落地清单（防重复，豆包勿重）
- r812C｜meta/pdi-forecasting/SKILL.md 1.25.0｜Prophet 三独点。
- r811 CI/OI/PI 与 r810 VI/RI/MI 三轮已落地，勿重复。

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像、无实体）。豆包的对应经验也按此路由写入**所属模块文件**（本批 SI/AI/PDI 各 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`），两方同守；Qoder 已于 2026-11-23 卸载，`co-learn/qoder/` 席位已移除，禁止再写该目录。用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障，本批未写入）。
