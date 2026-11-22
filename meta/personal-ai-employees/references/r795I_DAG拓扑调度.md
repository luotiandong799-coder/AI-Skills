# r795I｜OI｜DAG 调度：拓扑序只定依赖方向，就绪队列才定执行顺序

访问日期：2026-11-22。每轮独立实拉，禁止复用上轮结论。

## 一手来源逐字

- https://www.engineering.upenn.edu/~cit5920/knowledge/objects/graphs-and-trees/dags-and-topological-order（UPenn CIT 5920 讲义，WebFetch 200 逐字：indegree 计数 / 环判定 / n! 个拓扑序 / O(|V|+|E|)）

- https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html（Apache Airflow 3.4.0 官方，WebFetch 200 逐字：all_success 默认 / skip 级联 / none_failed_min_one_success / depends_on_past）

- https://airflow.apache.org/docs/apache-airflow/2.1.0/concepts/overview.html（Apache Airflow 官方，WebFetch 200 逐字：task queue / 发给 worker 不保证同机 / Pools 限并发）

## 独有点

1. 入度/环判据：维护 `indeg[v]` 与 `S={v | indeg[v]==0}`，每消费边 `u→v` 执行 `indeg[v]--`，仅降为 0 才入队；结束断言 `len(order)<|V|` → 报环。复杂度 O(|V|+|E|)。UPenn 讲义逐字：保留「count of the arrows still pointing into it」，剩点无 0 入度则必有环。

2. 顺序≠执行判据：拓扑序只保证每条边前向，同层多源可任选（讲义原文无边时 n! 个拓扑序），因此 `topo_order[i]` 不等于第 i 个被执行的任务；真实执行由就绪队列 + worker / Pool 槽位决定，入队 ≠ 立即执行。

3. 失败传播判据：Airflow 默认 `all_success` 下上游 failed 或 skipped 会级联跳过下游；汇合节点须显式 `none_failed_min_one_success` 才是「任一支成功即继续」。重跑边界须限定在失败节点及其下游依赖闭包，不触碰闭包外已成功节点（此条为工程推断，官方页只直接支持 trigger rule 与 depends_on_past）。

## 判重与判非

- 判重：`拓扑排序`/依赖调度正文在本体 0 专节；`DAG`/`拓扑` 命中是 Airflow 资源配额与 actor model 语境，异命题；与 §r785A 并发四层、§r793A Temporal 确定性分工不复用。豆包自留地 WB 0 落地。

- 抓取失败：无。
