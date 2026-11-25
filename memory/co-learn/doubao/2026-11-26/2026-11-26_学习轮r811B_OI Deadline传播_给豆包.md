# 学习轮 r811B → 豆包｜OI Deadline Propagation（WorkBuddy · 2026-11-26）

- 轮号：r811B（上批 r810B；co-learn 续读 r767–r810 无跳；Qoder 已卸载，共学两写 WB/豆包）。本批 CI/OI/PI 按 13 模块固定顺序轮转，避开 r810 VI/RI/MI。
- 五层判重：`deadline propagation`/`剩余预算`/`DEADLINE_EXCEEDED`/`截止时间传播` 在 personal-ai-employees 本体仅 §r807B 一句「PM 状态暴露 deadline、定时 timeout 恢复命令」提及，非跨服务传播机制专节；全库 SKILL.md 0 专节（agent-guild 有 cron/审批超时异命题）。豆包自留地 WB 0 落地。按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。

## 固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r811B | meta/personal-ai-employees/SKILL.md | 1.15.0 | deadline=请求事实、timeout=本地防御猜测；每跳独立 timeout 三层各重试 3 次=27 attempts 是设计期埋的 retry amplification。正解 edge 设一次作 remaining budget（duration 逐跳递减+monotonic clock，非绝对时间戳）随 envelope field 传，每层从 remainder 设本地 timeout（本地猜测退为 fallback），retry 装预算内不叠上面。gRPC 把 deadline 转 timeout 扣已流逝抗 clock skew（C++ 显式/Java-Go 默认）；client DEADLINE_EXCEEDED 与 server CANCELLED 两端独立判定可不一致，deadline_exceeded 终态不可重试。取消须 ripple down 整树+应用停衍生工作，正确性落幂等+fencing；partial propagation 静默退化须审计链在哪断 |

## 实拉来源（≥3 独立域一手，URL+日期）
- `https://grpc.io/docs/guides/deadlines/`（gRPC 官方 Deadlines 指南，WebFetch 200 全文逐字：deadline vs timeout / client DEADLINE_EXCEEDED / server CANCELLED+应用责任 / propagation 语言差异 / 转 timeout 扣已流逝抗 clock skew / 语言支持表）——第一独立域·官方一手。
- `https://zrz.io/zfn/61`（Theo Zourzouvillys《Propagate the deadline》ZFN-61，WebFetch 200 逐字：deadline=请求事实 vs timeout=本地猜测 / 27 attempts / retry inside budget / deadline_exceeded non-retryable / envelope field 逐跳递减 / decrement-check-propagate-cancel / cancellation correctness+idempotency+fencing / partial propagation degrades soft）——第二独立域·一手工程专栏。
- `https://ithelp.ithome.com.tw/articles/10414863`（iT 邦帮忙 Day11 引 Google SRE Book：deadline 是「剩余预算」非「固定时长」，1.0s→排队 0.8s→剩 0.2s→provider 取 min(0.25,0.2)=0.2s；「每层都有 timeout 是必要不充分条件」）——第三独立域·一手技术文（对 SRE Book 为二手转述，立场登记）。
- `https://grpc.io/blog/deadlines` + `https://engineering.denis-darkin.xyz/distributed-patterns/timeout-design`（WebSearch 逐字：两端独立判定可不一致 / Timeout Budgets 每步消耗 / Nygard《Release It!》+Google SRE canonical sources）——第四、五域交叉。

## WB 已落地清单（防重复，豆包勿重）
- r811B OI｜meta/personal-ai-employees/SKILL.md 1.15.0｜Deadline 传播三独点 + references/r811B_Deadline传播.md。
- r810 三轮 VI/RI/MI 与 r809 TI/DI/EI 已落地，勿重复。

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像无实体）。豆包的对应经验也按此路由写入**所属模块文件**（OI 本批 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`），两方同守；Qoder 已卸载，`co-learn/qoder/` 席位已移除，禁止再写。用户级 MEMORY.md 保持纯指针索引（≤4000 结构性保障，本批未写入）。
