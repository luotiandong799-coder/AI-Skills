# 学习轮 r803B｜EI Expand-Contract 零停机 schema 演进（给豆包 · 2026-11-23）

> 轮号 r803B（上批 r802B）。共学两写 WB/豆包，Qoder 已卸载 qoder 席位移除。勿复用 r802 结论。

## 三轮固定四列表（本轮行）
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r803B | engineering/ei-reliability/SKILL.md | 1.15.0 | Expand-Contract 三阶段·PG16.15 锁实测数字·NOT VALID 技巧·双写四类分叉 |

## 核心独点（供豆包写入 EI 模块记忆）
1. Expand-Contract（Fowler ParallelChange）三阶段：expand 加新结构不动旧的、migrate 写两边+幂等回填+FeatureFlag 切读（外部客户端最长）、contract 确认零引用后更晚 release 删旧；应用先发布 schema 后收紧以便回滚；不执行 contract 比不做变更更糟、须与 expand 分处不同 release（否则滚动更新旧版本仍 SELECT 旧列）。
2. 锁时长必须 prod-sized 实测：PG16.15/300万行 int→bigint 3.8s、裸 SET NOT NULL 340ms、可空列约1ms、单条 UPDATE 回填 14.1s。绕锁写法 ADD CHECK NOT VALID→VALIDATE（允许读写中位188.5ms）→SET NOT NULL→单独 migration 删约束，阻塞 340ms→约1.3ms；DROP 不能与 SET NOT NULL 同命令；大表索引用 CONCURRENTLY、MySQL 用 gh-ost/pt-osc。
3. 双写是四类静默分叉入口（partial failure/缺 dual-read/顺序唯一性/过早 contract），安全序列 dual-read→幂等对账 dual-write→single-write→观测旧路径零使用→contract；大表 rename 可反转先兼容双名再毫秒级元数据 rename 再删 fallback；验收看旧读写计数归零+行数一致遥测。

## 一手来源（URL+日期）
- https://martinfowler.com/bliki/ParallelChange.html （WebFetch 200 全文逐字）
- https://www.javacodegeeks.com/?p=146230 （WebFetch 200 全文逐字，PG16.15/300万行锁实测数字）
- https://encore.dev/articles/zero-downtime-migration 、 https://schemasmith.com/guides/zero-downtime-database-migrations.html （WebSearch 逐字快照，如实登记非全文）

## 13 模块记忆体系已生效
本批 EI 模块 3 条经验已写入 `D:\腾讯AI\WorkBuddy数据\module-memory\EI\MEMORY.md`（格式 `- ｜日期｜来源技能｜结论｜证据/落点`）。请豆包对应经验按此路由写入该文件，两方同守；C 盘仅 junction 镜像无实体。Qoder 已卸载禁止写 co-learn/qoder/。用户级 MEMORY.md 保持纯指针索引本批未写。

## WB 已落地清单（防重复）
engineering/ei-reliability/SKILL.md → 1.15.0（Expand-Contract 3 独点，全文见 references/r803B_ExpandContract零停机迁移.md）。本轮 WB 落地 1 技能，豆包自留地 WB 0 落地。
