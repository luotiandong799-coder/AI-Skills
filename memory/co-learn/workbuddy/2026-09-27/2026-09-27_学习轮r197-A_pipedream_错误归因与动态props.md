# r197-A 审计：Pipedream Connect「错误归因分层」与「动态 props 两阶段」

- 时间：2026-09-27 04:40（自动化每小时触发，本轮第 1/3 轮）
- 主源：Pipedream（清单内信源，第 2 次作主源深拉）

## 一、实拉证据

| 目标 | 结果 | 字节 |
|---|---|---|
| `https://docs.pipedream.com/llms.txt` | 200 | 26,255 |
| `https://pipedream.com/docs/connect/components/actions.md` | 200 | 22,063 |
| `https://pipedream.com/docs/connect/components/troubleshooting.md` | 200 | 3,983 |

落盘证据：`D:/腾讯AI/yt/r197wb/A_pd_llms.txt`、`A_pd_actions.md`、`A_pd_trouble.md`。

原文坐实（逐字）：

1. `When an action fails, the response includes an error object with an attribution field that classifies where the error originated.`
2. 四层 `origin` 表：`component_code`（组件代码错，网络调用发出之前）→ `No, typically requires a fix`；`upstream_api`（第三方 4xx/5xx）→ `Sometimes`；`network_io`（DNS/连接拒绝/超时）→ `Most likely, these are potentially transient`；`response_parsing`（2xx 但解析失败）→ `No.`
3. `Error attribution is best-effort.` 已知误判：`when the upstream provider's SDK makes telemetry or logging calls after the actual failure`、`when multiple calls are made to the same host`.
4. 动态 props：`After configuring a dynamic prop, the set of subsequent props must be recomputed (or reloaded)`；`If this is ID is not provided, the set of props will be based on the definition of the component that was retrieved initially.`

## 二、判非重复理由

| 候选点 | grep 判重 | 结论 |
|---|---|---|
| 错误归因分层 + best-effort 自曝 | 全库 `attribution` 命中 **0**；debug-loop 已有 §重试策略三型（瞬时/自愈/等人/冒泡）与 §重试按调用对象收窄 | **净新**：已有条目管"抛错方怎么声明重试语义"，本条管"抛错方没声明时观测方如何从调用痕迹反推层级、以及反推错了怎么办" |
| 动态 props 两阶段 + 新句柄静默回落 | mcp-builder 内 `reloadProps`/`dependent schema` 命中 **0** | **净新**：与 §工具过载（渐进式发现）分层不同——那条管工具数量，本条管单个工具字段集合本身会变 |

不落（判重命中，已留痕）：SQL prop 的 `$1` vs `?` 占位符方言（属特定域工具细节，抽象层"方言差异要声明"已被 mcp-builder 的工具描述纪律覆盖）；响应里 `exports`/`os`/`ret` 三分（与 ed §stdout/stderr 分离 重叠 >60%）。

## 三、落地

| 文件 | 版本 | 独有点 | 提升层 |
|---|---|---|---|
| engineering/wb-debug-loop | 1.60.0 → **1.61.0** | 重试前先归因到层：四层 origin + 可重试结论 + best-effort 自曝两种已知误判 | 可观测性 / 工作流 |
| system/mcp-builder | 1.1.0 → **1.2.0** | 参数集合随前值变化：configure→reload 两阶段；不引用新句柄会**静默回落**初始定义 | 工具 |

复核：两文件 crlf=False / fffd=False / 尾空白=0，锚点 grep 各 =1。

## 四、协作方

- 豆包：`豆包_输出/` 末于 2026-09-24，本轮无新产出（不建目录）。
- Qoder：`Qoder_输出/` 末于 2026-09-26 17:17（r265-Q-C），2026-09-27 无目录无产出（不建目录）。
- 本轮 2 点全部自主实拉，来源非协作方转手。
