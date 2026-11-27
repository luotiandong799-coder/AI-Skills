# 学习轮 r813（A/B/C）｜孟德尔随机化 · 成本效果分析 ICER/QALY · singleflight 请求合并（WorkBuddy · 2026-11-27）

- 轮号：r813A/B/C（上批 r812A/B/C；co-learn r767–r812 续读无跳；Qoder 已卸载，共学两写 WB/豆包，qoder 目录 0 写入）。遵用户 2026-11-25 追加指令「13 模块固定顺序轮转」（KI 论文域排除，按 12 模块 4 组），本批取 TI/DI/EI，避开 r812 SI/AI/PDI；除非另行取消不得提前停止或缩减。
- 五层判重：全库 SKILL.md + module-memory + co-learn + references 对 `孟德尔随机化`/`Mendelian`/`MR-Egger`、`成本效果`/`ICER`/`QALY`、`singleflight`/`cache stampede`/`XFetch` 对应模块本体均 0 机制专节（MR 仅 r797A/r809A references 各一句旁及；ICER 仅豆包自留地与论文域子串提及；惊群/thundering herd 属 §16 限流/§26 负载丢弃口号级提及、请求合并 2 命中属豆包自留地）。豆包自留地 `wb-execute-discipline`/`wb-context-compressor` WB 0 落地。按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。

## 三轮固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r813A | meta/ti-critical-reasoning/SKILL.md | 2.11.0 | MR 用遗传变异当工具变量模拟「自然 RCT」，ratio estimate β̂_XY=β_GY/β_GX，是 IV 具体载体非天然 RCT 等价物（随机只支撑独立性）；三假设相关性 F>10 且 p<5e-8(查GWAS)/独立性 G⊥U(群体分层用主成分或家系内)/排他性 α=0 即 G→X→Y 无水平多效(不可直接检验,靠生物学知识+MR-Egger 截距)；参数化 X=πG+γU+εX/Y=βX+δU+αG+εY 对应 π≠0/G⊥U/α=0，禁写「基因随机分配所以因果成立」；水平多效性造双向错误(假阳性+抵消真效应致假阴性,咖啡-吸烟例)，多方法分工非二选一 IVW 效能最高但依赖工具全有效/MR-Egger 诊断方向性多效依赖 InSIDE 且效能低/Weighted median ≥50% 有效稳健，报告须主估计+≥2 敏感性分析+Cochran Q+Egger 截距；两样本须 harmonize 等位基因、样本重叠会偏；边界=群体平均因果效应非个体命运 |
| r813B | meta/di-decision-tradeoff/SKILL.md | 1.26.0 | 成本效果分析 ICER=ΔC/ΔE 与机会成本阈值：CUA 用 QALY(0死亡/1完全健康)跨病种可比、CEA 自然单位不可跨病种、DALY 标度相反；成本与 QALY 须同一贴现率 PV=ΣX_t/(1+r)^t；负 ICER 双义=东南(ΔE>0,ΔC<0)绝对优势直接采纳/西北(ΔE<0,ΔC>0)绝对劣势直接排除,禁只报「ICER 为负」不报符号，只有东北/西南才比阈值；λ 取预算约束下被挤出服务的边际健康产出非主观支付意愿，报值标国家/年份/视角(0.5–1.5×人均GDP/QALY、NICE £20k/QALY)；多方案先剔劣势与扩展劣势、按效果升序排效率前沿只比相邻两级；NMB=λΔE−ΔC 与 ICER≤λ 等价且概率敏感性分析更稳健 |
| r813C | engineering/ei-reliability/SKILL.md | 1.17.0 | stampede=hot key 过期瞬间所有请求同时回源，200ms 重建×10000RPS⇒约2000 并发相同 DB 查询；进程内 singleflight 降到每进程1次(100台⇒100次改善20×但仍100)、分布式锁 SET lock:key token NX PX 3000 才降到全集群1次、XFetch 概率早期刷新；singleflight 只合并「在飞」调用非缓存非限流不设TTL进程内有效、shared=true≠缓存命中(可作告警)、shared=false 那次才写缓存打点、错误也被共享须 Forget(key) 重试、fn 只放幂等纯读；stale set 竞态 singleflight 不挡，机制各有代价(租约 delete 使 lease 失效迟到 set 被拒/版本化 CAS/stale-while-revalidate 有界陈旧/XFetch 不保证驻留)，分布式锁须带 TTL+失败回退否则持锁者死等待者挂起 |

## 实拉来源（每轮 ≥2 独立域一手，URL+日期逐条）
- A：`https://scipedia.bohrium.com/sciencepedia/feynman/preventive_medicine_undergraduate-Mendelian_randomization`（玻尔科学百科预防医学页，WebFetch 200 全文逐字：定义/π≠0·G⊥U·α=0 参数化/群体平均边界）· `https://www.mediecogroup.com/zhuanlan/lessons/1160/`（医咖会梳理 2023-11-03 EHJ IF39.3 MR 综述，WebFetch 200 全文逐字：三假设与各自检验/水平多效双后果/咖啡-吸烟例）· `https://pdrohde.github.io/sites/MR/MR_new.html`（PDRohde Research 英文教程，WebFetch 200 全文逐字：观察三敌/遗传工具四优势/DAG ratio estimate/IVW·MR-Egger·Weighted median 方法比较表/Cochran Q+Egger 截距报告范式）· 玻尔计算生物学分册 + wk8686 中文教程 WebSearch 交叉。诚信：Wikipedia Mendelian_randomization WebFetch fetch failed 未采纳、玻尔两分册按来源族折叠为一条独立证据。
- B：`https://scipedia.bohrium.com/sciencepedia/feynman/translational_medicine_graduate-cost-effectiveness_and_cost-utility_analysis`（玻尔科学百科转化医学页，WebFetch 200 全文逐字：QALY/CBA vs CEA/四象限负 ICER 双义/ICER 公式/λ=机会成本/贴现同率/效率前沿阶梯/扩展优势/NMB）· `https://baike.baidu.com/item/增量成本–效果比/53548531`（百度百科，WebSearch 逐字：0.5–1.5×人均GDP/QALY、罕见病4×、NICE £20k 与英夫利昔单抗 £14,607/QALY、血友病A 55631元/QALY）· 玻尔药学本科与 ICER 词条 + 日本 Astellas 官方术语页 WebSearch 逐字交叉。诚信：PMC5668200 号错配（实为 PKC 癌症综述）整篇弃用未采信一字；药企官方页取术语定义不取产品主张。
- C：`https://system-design-in-depth.vedgupta.in/topic/cache-concurrency-control`（System Design In Depth，WebFetch 200 全文逐字：面包店类比/200ms·10000RPS·100 servers 算例/单进程100次 vs 分布式锁1次/XFetch/memcache lease 10s/七行技术比较表/stale-set race/TTL 回退）· `http://gerryyang.com/posts/singleflight-intro-and-usage`（Gerry's blog，WebFetch 200 全文逐字：Do/DoChan/Forget/shared/错误共享/禁用副作用/进程内局限/shared=false 打点）· 17golang + StackOverflow 官方 Group.Do 注释 + vikulin-va.ru 俄文 WebSearch 逐字交叉。诚信：Wikipedia cache stampede WebFetch fetch failed 未采纳（本批 Wikipedia 第二次失败）。

## WB 已落地清单（防重复）
- r813A TI｜meta/ti-critical-reasoning/SKILL.md 2.11.0｜MR 三独点 + references/r813A_孟德尔随机化.md
- r813B DI｜meta/di-decision-tradeoff/SKILL.md 1.26.0｜成本效果分析三独点 + references/r813B_成本效果分析ICER与QALY.md
- r813C EI｜engineering/ei-reliability/SKILL.md 1.17.0｜singleflight 三独点 + references/r813C_singleflight请求合并与惊群防护.md
- r812 SI/AI/PDI、r811 CI/OI/PI、r810 VI/RI/MI 已落地，勿重复。

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像、无实体）。豆包的对应经验也按此路由写入**所属模块文件**（本批 TI/DI/EI 各 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`），两方同守；Qoder 已于 2026-11-23 卸载，`co-learn/qoder/` 席位已移除，禁止再写该目录。用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障，本批未写入，3709/4000）。

本批为 r813A/B/C 独立实拉留痕，三轮标准一致、禁止复用 r812 结论。下批 r814A/B/C 按 13 模块固定顺序取 VI/RI/MI（KI 论文域排除，避开 r813 TI/DI/EI）；Qoder 席位已移除仅两写。
