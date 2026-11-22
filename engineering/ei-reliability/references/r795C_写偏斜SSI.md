# r795C｜EI｜二十一、写偏斜 write skew：每条读都一致，整体仍不可串行化

访问日期：2026-11-22。每轮独立实拉，禁止复用上轮结论。

## 一手来源逐字

- https://www.postgresql.org/docs/current/transaction-iso.html（PostgreSQL GDG，v19 文档，WebFetch 200 逐字：SSI 定义 / 330 vs 300 反例 / predicate locks 不阻塞不死锁）

- https://wiki.postgresql.org/wiki/SSI（PostgreSQL 官方项目 Wiki，WebFetch 200 逐字：write skew 定义 / first committer wins / dangerous structure）

- https://arxiv.org/abs/1208.4179（Ports & Grittner，VLDB 2012，2012-08-21，补充：首个生产数据库 SSI 实现）

## 独有点

1. 判据：日志出现 `r1(Y) r2(X) w1(X) w2(Y)` 且写集合不相交 `{X}∩{Y}=∅` → 判 write skew。PG Wiki 逐字：write skew 是「simplest form of serialization anomaly against which SSI protects you」；两个事务都执行到提交，先提交者胜、后者回滚。

2. 业务不变式（「至少一人值守」「余额≥0」）若只在单事务 SELECT 后写，SI 下可被破坏；规避三选一：升 SERIALIZABLE、显式 `SELECT FOR UPDATE` / 物化冲突行使写集合相交、交给数据库 CHECK/排他约束。不能只靠应用层的「我先读一遍」。

3. SSI 检测链 `T_in →rw T_pivot →rw T_out`，pivot 为环中首个提交者才回滚；机检信号 `pg_locks.mode='SIReadLock'`、SQLSTATE `40001`、`could not serialize access due to read/write dependencies` → 必须捕获并重试，否则把正常的并发回滚误报成业务失败。PG 官方逐字：predicate lock 不阻塞、不产生死锁。

## 判重与判非

- 判重：`写偏斜`/`write skew`/`snapshot isolation`/`可串行化` 在本体 0 命中（仅 .research 研究快照与相邻技能 phrasal 命中）；与 §六有界重试、§十五分布式锁、§十七舱壁分工不复用。豆包自留地 WB 0 落地。

- 抓取失败：无。
