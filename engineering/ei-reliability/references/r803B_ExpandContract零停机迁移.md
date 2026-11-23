# r803B｜EI｜二十四、Expand-Contract 并行变更：零停机 schema 演进

访问日期：2026-11-23；本轮独立实拉禁止复用上轮。

## 一手来源（逐字 + URL + 日期）

1. Martin Fowler《ParallelChange》（martinfowler.com/bliki/ParallelChange.html，WebFetch 200 全文逐字，2026-11-23）：
   - "Parallel change, also known as expand and contract, is a pattern to implement backward-incompatible changes to an interface in a safe manner, by breaking the change into three distinct phases: expand, migrate, and contract."
   - expand："In the expand phase you augment the interface to support both the old and the new versions."
   - migrate："During the migrate phase you update all clients using the old version to the new version. This can be done incrementally and, in the case of external clients, this will be the longest phase."；"a FeatureFlag can be used to control which version of the interface is used."；"when you have a large number of clients, using branch by abstraction is a better strategy".
   - contract warnings："Once all usages have been migrated to the new version, you perform the contract phase to remove the old version."；"If the contract phase is not executed you might end up in a worse state than you started, therefore you need discipline to finish the transition successfully."
   - 价值："particularly useful when practicing ContinuousDelivery because it allows your code to be released in any of these three phases. It also lowers the risk of change by allowing you to migrate clients and to test the new version incrementally."；"prevents you from spreading breakage across the entire codebase all at once."

2. Java Code Geeks《Zero-Downtime Migrations: The Expand and Contract Pattern with Flyway or Liquibase》（javacodegeeks.com/?p=146230，WebFetch 200 全文逐字，2026-11-23）：
   - 三阶段表（逐字）：Expand = "Add the new column, nullable" / "Deploy code that writes to both columns"；Migrate = "Backfill old rows in small batches" / "Switch reads to the new column"；Contract = "Add constraints, then drop the old column" / "Remove the old code path"。
   - 锁实测："I ran them on PostgreSQL 16.15 against a table with three million rows... the scale is logarithmic, because the differences are enormous."；"changing int to bigint rewrote the table and took about 3.8 seconds. Second, a plain SET NOT NULL scanned every row under a blocking lock for about 340 milliseconds. Meanwhile, adding a nullable column, or one with a constant default, finished in about a millisecond."；"updating all three million rows in a single statement took 14.1 seconds in one run. For that reason, backfill in small batches."
   - NOT VALID 技巧："If a valid CHECK constraint already proves no NULL exists, the scan is skipped. So add the constraint as NOT VALID, validate it, and only then set NOT NULL."（SQL 序列：ADD CONSTRAINT ... CHECK NOT VALID → VALIDATE CONSTRAINT → ALTER COLUMN SET NOT NULL → DROP CONSTRAINT）；"The direct route blocked the table for about 340 ms, while the safe route blocked it for roughly 1.3 ms in total... validation took a median of 188.5 ms but runs under a lock that allows normal reads and writes."；"do not drop the helper constraint in the same command as SET NOT NULL... because the scan then comes back."；"place each of the last four statements in its own migration. Otherwise the tool wraps them in one transaction, and the lock from the first step lasts until the end."
   - contract 时序："keep the contract phase in a later release than the expand phase. Otherwise, the old application version can still be running when the old column disappears."

3. Encore《Zero-Downtime Database Migration: Expand-Contract and Safe Cutover》（encore.dev/articles/zero-downtime-migration，WebSearch 逐字快照，2026-11-23）：
   - 表（逐字）：Expand "Add nullable columns, new tables, new indexes" / 可回滚 Yes；Migrate "Backfill or dual-write into the new shape" / "Yes if both shapes stay valid"；Cut over "New code becomes the single writer/reader" / "Yes until contract"；Contract "Drop old columns, stop dual-write" / "No for the dropped shape"。
   - "Dropping a column in the expand deploy is the classic outage: the previous revision still selects that column during the rolling update."
   - 双写陷阱："Dual-write... often creates silent divergence: Partial failure. The first write commits, the second fails, retries rewrite only one side... Missing dual-read... Ordering and uniqueness... Early contract. You remove the old column while a canary or a stuck task still runs the previous binary."；"A safer sequence is dual-read... then dual-write with an idempotent reconciliation job, then single-write to the new shape, then contract."
   - "PostgreSQL's CREATE INDEX CONCURRENTLY avoids a full write lock for many index builds... On MySQL, online schema change tools such as gh-ost or pt-online-schema-change help when a rewrite would lock a large table for too long."

4. SchemaSmith《Zero-Downtime Database Migrations》（schemasmith.com/guides/zero-downtime-database-migrations.html，WebSearch 逐字快照，2026-11-23）：
   - "Application Code Deploys First... deploy the updated application first, then apply the schema change. This decouples application releases from database releases, and it makes rollbacks much simpler."
   - 大表 rename 反转模式："For large datasets, flip the pattern... rename the column at the database level (which is a fast metadata operation)... Deploy application code that handles both column names... Rename user_name to username at the database level... Deploy application code that only uses username."

## 判非（不采 / 边界）

- 不把 expand-contract 与 §二 Saga / §二十三 TCC 混同：那些是跨服务事务一致性协议；本章是滚动部署期间两个应用版本共享一个库时的 schema 兼容，落点不同。
- 不省略 contract：Fowler 明确警告不执行 contract 比不变更更糟；contract 是计划的一部分。
- 不宣称某工具（Flyway/Liquibase/gh-ost）本身保证零停机：工具只承载每步 migration，锁行为取决于数据库引擎与语句；锁时长须在 prod-sized 表实测（JCG 数字基于 PG16.15/300 万行，换硬件/表大小会变）。
- dual-write 不是保险：Encore 列四类静默分叉；正确序列是 dual-read → 幂等 dual-write+对账 → single-write → contract。
- 增量回填必须小批 + 可断点 + 限流 + 监控复制延迟；JCG 实测 300 万行单条 UPDATE 14.1s。
- 豆包自留地 WB 0 落地；全库 EI SKILL.md `expand-contract/并行变更/expand and contract` 0 命中。
