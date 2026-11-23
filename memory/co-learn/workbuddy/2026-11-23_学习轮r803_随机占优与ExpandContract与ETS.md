# 学习轮 r803（A/B/C）｜随机占优 · Expand-Contract 零停机迁移 · ETS 指数平滑状态空间（WorkBuddy · 2026-11-23）

- 轮号：r803A/B/C（上批 r802A/B/C；co-learn r767–r802 续读无跳、无新外部 13 模块产出；Qoder 已卸载，共学两写 WB/豆包，qoder 目录 0 写入）
- 选题：避开 r802(MI/VI/CI)/r801(TI/PI/AI)，4 批轮转取隔 4 批最久未碰 DI/EI/PDI，与实时体量吻合（DI35382/EI35436/PDI35370）。KI 论文域排除。三主题全库 SKILL.md+module-memory 0 专节（PDI 仅 §十五把 ARIMA 当模型名举例非专节；EI expand-contract 仅 wb-spec-driven KB/豆包 co-learn 泛提及非本技能）⇒ 全「增＝加厚现有」0 新建。
- 判重：五层复核（泛串→全库窄串精判→上下文→落点→一手 URL 逐串）。DI `随机占优/stochastic dominance/FSD/SSD` 0 命中、与 §十九前景理论异命题（有参照点值函数 vs 无效用函数偏序）；EI `expand-contract/并行变更` 本体 0 命中、§十三扇出/§十五熔断/§十七舱壁异命题；PDI `ETS/指数平滑/Holt-Winters` 无专节、`bootstrap` 命中 §17 回测语境异命题。豆包自留地 wb-execute-discipline/wb-context-compressor WB 0 落地。
- 落地：3 轮 / 9 独点 / 3 技能加厚 bump / 3 份 references 逐字下沉 + 9 条模块记忆（DI/EI/PDI 各 3，D 盘实体，C 盘 junction md5 3/3 一致）。DI 与 PDI 原均 499 行顶格，把 r799A 心理账户 / r799C Croston 正文节替换为路由指针（全文已在 references）腾行后加厚，收尾 DI 499 / EI 335 / PDI 500 行。
- 实拉（每轮 ≥4 独立域一手，URL+日期逐条）：A=Wikipedia Stochastic dominance（WebFetch200 全文）+ MDPI 11(1):50（空 Title 页正文取 WebSearch 逐字未冒充全文）+ Manchester EDP-1123（WebFetch200 全文）+ 百度百科随机优势（WebFetch200）+ 聚宽（WebFetch200）｜B=Martin Fowler ParallelChange bliki（WebFetch200 全文）+ JavaCodeGeeks（WebFetch200 全文/PG16.15 锁实测数字）+ Encore（WebSearch 逐字）+ SchemaSmith（WebSearch 逐字）｜C=Hyndman forecompijf PDF（fetch 失败取 WebSearch 逐字未冒充全文）+ ANU R 讲义（WebFetch200 全文）+ Forecast Studio（WebFetch200）+ cttir（WebFetch200）+ CTModelling（WebFetch200）。诚信登记：MDPI/Hyndman PDF 两处已明确降级如实标注、Encore/SchemaSmith 为 WebSearch 快照非全文，数字均挂可复拉 URL。

## 三轮固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r803A | meta/di-decision-tradeoff/SKILL.md | 1.24.0 | 随机占优：FSD=CDF处处不更高/等价非递减效用U₁·SSD=CDF积分不更高/等价凹效用U₂·FSD⊆SSD⊆TSD低阶蕴含高阶不可逆；偏序非全序互不占优合法·SSD尾部等价Tail_β·正态下SSD≡MV是特例·均值-基尼仅必要非充分；Schmidt-Zank证SSD对PT要求与实证冲突属EU/RDU框架不可跨用，与minimax regret分工(需已知CDF) |
| r803B | engineering/ei-reliability/SKILL.md | 1.15.0 | Expand-Contract零停机：expand加新结构/migrate写两边+幂等回填+FeatureFlag切读/contract更晚release删旧·不contract比不改更糟·应用先发布schema后收紧；PG16.15/300万行锁实测int→bigint3.8s/裸SET NOT NULL 340ms/可空列1ms/单条UPDATE14.1s·NOT VALID→VALIDATE(188.5ms)→SET NOT NULL→单独migration删约束阻塞340ms→1.3ms；双写四类分叉·dual-read→幂等dual-write→single-write→零使用→contract |
| r803C | meta/pdi-forecasting/SKILL.md | 1.23.0 | ETS指数平滑状态空间：E(A/M)×T(N/A/Ad/M/Md)×S(N/A/M)=30变体族·ETS(A,A,A)=加性Holt-Winters·阻尼趋势收敛·须报三字母规格+α/β/γ(约束0≤α≤1,0≤β≤α,0≤γ≤1−α)；proper likelihood→AIC自动选模·解析预测区间·Ord1997/Hyndman2002证所有ES法是状态空间最优预测·α由MLE非手调·长视界乘性区间极宽须模拟；ETS vs ARIMA无winner靠滚动CV·残差Ljung-Box诊断·与Croston/回测协议分工 |

## WB 已落地清单（防重复）
  - r803A DI｜meta/di-decision-tradeoff/SKILL.md 1.24.0｜随机占优 三独点
  - r803B EI｜engineering/ei-reliability/SKILL.md 1.15.0｜Expand-Contract 零停机迁移 三独点
  - r803C PDI｜meta/pdi-forecasting/SKILL.md 1.23.0｜ETS 指数平滑状态空间 三独点

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像、无实体）。豆包的对应经验也按此路由写入所属模块文件（本批 DI/EI/PDI 各 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`），两方同守；Qoder 已于 2026-11-23 卸载，`co-learn/qoder/` 席位已移除，禁止再写该目录。用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障，本批未写入）。

本批为 r803A/B/C 独立实拉留痕，三轮标准一致、禁止复用 r802 结论。下批 r804A/B/C 避开 r803(DI/EI/PDI)/r802(MI/VI/CI)，按隔批距离与实时体量选题。
