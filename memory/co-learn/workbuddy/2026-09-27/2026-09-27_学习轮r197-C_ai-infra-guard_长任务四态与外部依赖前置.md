# r197-C 审计：AI-Infra-Guard「长任务状态四态」与「外部依赖前置检查」

- 时间：2026-09-27 04:54（本轮第 3/3 轮）
- 主源：Tencent/AI-Infra-Guard（r196-C 首次读取 README，本轮**首次深拉 docs/ 目录**）

## 一、实拉证据

| 目标 | 结果 | 字节 |
|---|---|---|
| `api.github.com/repos/Tencent/AI-Infra-Guard/contents/docs` | 200 | 5,661（6 项：`api-checker-integration.md` / `api_data_update.md` / `architecture_evolution.md` / `docs.go` / `swagger.*`） |
| `docs/api_data_update.md`（raw） | 200 | 4,672 |
| `docs/architecture_evolution.md`（raw） | 200 | 9,863 |

落盘证据：`D:/腾讯AI/yt/r197wb/C_aig_docs.json`、`C_aig_data.md`、`C_aig_arch.md`。
注：raw.githubusercontent 在本机 000，改走 `api.github.com contents/<path>` + `Accept: application/vnd.github.raw`（与既有环境事实一致）。

原文坐实（逐字）：

1. 状态字段：`success` —— `Whether the last sync succeeded (null if never run)`；`finished_at` —— `ISO-8601 timestamp when the sync finished (null if still running)`；`running` —— `Whether a sync is currently in progress`。
2. 失败消息透传底层：`"git clone failed: exit status 128\nfatal: unable to access 'https://github.com/...'"`。
3. Notes 三条里两条是硬前置：`The \`git\` binary must be available in the server's PATH.`；`The server must be able to reach \`github.com\` on port 443.`

## 二、判非重复理由

| 候选点 | grep 判重 | 结论 |
|---|---|---|
| 长任务状态要分辨"从未运行/进行中/成功/失败" | av §消息类四态 管"一次发送动作的终态分族"；av §"从未失败过的验证与从未运行过的验证一样可疑" 管验证器本身 | **净新**：本条管**后台任务被查询时状态字段怎么设计**——`null`（没值）与 `false`（失败）是两个不同事实 |
| 致命外部依赖要前置检查而非写进 Notes | debug-loop §外部依赖韧性 管"依赖挂了怎么兜底"；ed §每个外部依赖独立熔断 管"运行中怎么隔离" | **净新**：本条管**部署/启动期就该验掉的缺失**，与运行期兜底分层不同 |

不落（判重命中，已留痕）：`architecture_evolution.md` 的「Rule-first, LLM-augmented（核心检测保持确定性、LLM 只叠在复杂场景）」→ ed §Agent 工程最优解=最简（确定性优先于 agent 决策）+ av §确定性 grader 优先 已覆盖，重叠 >60%；「Data as source of truth（规则不进编译产物）」→ 与 sa §发布即冻结运行环境 相邻且已被技能体系既有"真源"纪律覆盖。

## 三、落地

| 文件 | 版本 | 独有点 | 提升层 |
|---|---|---|---|
| engineering/wb-spec-driven | 1.95.0 → **1.96.0** | 长任务状态对象要能分辨四件事（`success:null` 从未运行 ≠ `false` 失败）+ 失败消息透传底层原始错误 | 工具 / 工作流 |
| engineering/wb-release-maintain | 1.17.0 → **1.18.0** | 会让整体失败的外部依赖必须写成前置检查项，不能写进 Notes 等运行时暴露 | 部署 / 工作流 |

复核：两文件 crlf=False / fffd=False / 尾空白=0，锚点 grep 各 =1。

## 四、协作方

- 豆包 `豆包_输出/2026-09-27`：无产出，不建目录。Qoder `Qoder_输出/2026-09-27`：无产出，不建目录。
- 本轮 2 点自主实拉（GitHub contents API）。

## 五、信源状态

- 本轮新增可达面：AI-Infra-Guard `docs/`（此前只读 README）。
- `fullstackskills.com` 已按 r196-C 结论移出待补清单（停放域名）；`skillhub.tencent.com` API 面无效仅探首页——本轮未重复投入。
