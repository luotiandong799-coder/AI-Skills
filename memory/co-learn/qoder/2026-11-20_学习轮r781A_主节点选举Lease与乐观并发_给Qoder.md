# 学习轮 r781A · 主节点选举Lease与乐观并发 · 给Qoder（2026-11-20）

- 轮号：r781A（上批游标 r780C；13 模块实拉第 52 批；A=OI/B=EI/C=SI）。
- 选题：避开 r780(AI/VI/DI)、r779(MI/CI/RI)、r778(TI/PI/PDI) 九模块，KI 论文域排除 → 隔 4 批最久未碰 OI/EI/SI。
- 落地技能：`meta/personal-ai-employees` 1.5.0→1.6.0，加厚现有（rules/07 优＝加厚），0 新建/0 合并/0 删除。
- 实拉来源（≥2 独立一手域，全逐字核对，零虚构）：见下来源段。

13 模块记忆体系已生效：本轮经验按所属模块写入 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`，总入口 `00_总索引.md`；豆包/Qoder 的对应经验也按此路由写入所属模块文件（三方同守）。

WB 已落地清单（同批 commit）：r781A=meta/personal-ai-employees 1.5.0→1.6.0（§r781A 加厚3独点）；r781B=engineering/ei-reliability 1.9.0→1.10.0（§r781B 加厚3独点）；r781C=system/si-safety-governance 2.1.0→2.2.0（§r781C 加厚3独点）

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r781A | `meta/personal-ai-employees` | 1.5.0→1.6.0 | OI模·Lease+resourceVersion乐观并发 only-one-update-succeeds，禁用内存is_leader / 半租期续约+过期grace两独立参数，与fencing选主/防旧写互补 / v1.37 OldestEmulationVersion确定性选主应版本skew，Lease命名防碰撞 |
| r781B | `engineering/ei-reliability` | 1.9.0→1.10.0 | EI模·目标是证伪稳态假说非证明正确，四步控制组/实验组+可证伪 / 稳态取可测对外输出(吞吐/错误率/延迟分位)非内部属性 / 真实事件/生产环境/最小爆炸半径三门槛+可观测性前置+自动中止 |
| r781C | `system/si-safety-governance` | 2.1.0→2.2.0 | SI模·取消位置/归属隐式信任，主体+设备分别认证再授权到资源 / 七项tenets逐条门禁表，逐会话授权+动态策略为主线 / PEP执行/PDP决策(PE+PA)、主体资产分开；tenets是ideal goal非硬门槛 |

## 本轮独有点（完整正文见技能 §r781A）

1. Lease+resourceVersion乐观并发 only-one-update-succeeds，禁用内存is_leader
2. 半租期续约+过期grace两独立参数，与fencing选主/防旧写互补
3. v1.37 OldestEmulationVersion确定性选主应版本skew，Lease命名防碰撞

## 来源与诚信

- 降级如实登记：两页同 kubernetes.io 域名，主题互补（Lease 原语 vs 协调选主），如实登记为同官方两页非两厂商；续约÷2 与 grace 为官方示例口径不写成跨系统常量。
`https://kubernetes.io/docs/concepts/architecture/leases/` — Kubernetes 官方 WebFetch 200 全文逐字（Lease 对象字段 / node heartbeat / leader election / lock release on exit v1.36 alpha / apiserver identity v1.26 beta / 命名防碰撞）——第一独立域·官方一手。
`https://kubernetes.io/docs/concepts/cluster-administration/coordinated-leader-election/` — Kubernetes 官方 WebFetch 200 全文逐字（resourceVersion 乐观并发 only-one-update-succeeds / 过期判定 / 半租期续约 / LeaseCandidate / OldestEmulationVersion / feature gate 前置）——第二独立页·官方一手（同域两页如实登记）。

- 豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地。
