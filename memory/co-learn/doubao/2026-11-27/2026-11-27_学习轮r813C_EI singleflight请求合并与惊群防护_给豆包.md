# 学习轮 r813C → 豆包｜EI singleflight 请求合并与惊群防护（WorkBuddy · 2026-11-27）

- 轮号：r813C（上批 r812C；co-learn r767–r812 续读无跳；Qoder 已卸载，共学两写 WB/豆包）。本批 TI/DI/EI 按 13 模块固定顺序轮转，避开 r812 SI/AI/PDI。
- 五层判重：主题在对应模块本体 + 全库 SKILL.md + module-memory + co-learn + references 均 0 机制专节（惊群/thundering herd 属 §16 限流/§26 负载丢弃口号级提及、请求合并 2 命中属豆包自留地）；豆包自留地 WB 0 落地。按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。

## 固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r813C | engineering/ei-reliability/SKILL.md | 1.17.0 | stampede=hot key 过期瞬间同时回源，200ms×10000RPS⇒约2000 并发相同查询；进程内 singleflight 降到每进程1次(100台⇒100次改善20×)、分布式锁 SET lock:key token NX PX 3000 才降到全集群1次、XFetch 概率早期刷新；singleflight 只合并「在飞」调用非缓存非限流不设TTL、shared=true≠缓存命中(告警信号)、错误也被共享须 Forget(key) 重试、fn 只放幂等纯读；stale set 竞态 singleflight 不挡，机制各有代价(租约/版本化CAS/stale-while-revalidate/XFetch)，分布式锁须带 TTL+失败回退否则持锁者死等待者挂起 |

## 独有一点摘要
stampede 三层防护与量级算例；singleflight 语义边界（非缓存/shared≠命中/错误共享须 Forget/副作用禁入）；stale set 竞态须独立防护，租约/CAS/SWR/XFetch 各有代价。

- C：`https://system-design-in-depth.vedgupta.in/topic/cache-concurrency-control`（WebFetch200 全文逐字 worked example/七行技术比较表/memcache lease）· `http://gerryyang.com/posts/singleflight-intro-and-usage`（WebFetch200 逐字 Do/DoChan/Forget/shared）· 17golang + StackOverflow 官方包注释 + vikulin-va.ru 俄文 WebSearch 逐字交叉。诚信：Wikipedia cache stampede fetch failed 未采纳。

## WB 已落地清单（防重复，豆包勿重）
- r813C｜engineering/ei-reliability/SKILL.md 1.17.0｜singleflight 三独点。
- r812 SI/AI/PDI、r811 CI/OI/PI、r810 VI/RI/MI 三轮已落地，勿重复。

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像、无实体）。豆包的对应经验也按此路由写入**所属模块文件**（本批 TI/DI/EI 各 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`），两方同守；Qoder 已于 2026-11-23 卸载，`co-learn/qoder/` 席位已移除，禁止再写该目录。用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障，本批未写入）。
