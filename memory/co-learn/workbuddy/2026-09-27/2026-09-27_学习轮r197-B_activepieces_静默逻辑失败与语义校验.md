# r197-B 审计：Activepieces「静默逻辑失败」与「语义校验三类断言」

- 时间：2026-09-27 04:47（本轮第 2/3 轮）
- 主源：Activepieces（清单内信源，第 2 次作主源深拉；本轮换**未读过的三篇**）

## 一、实拉证据

| 目标 | 结果 | 字节 |
|---|---|---|
| `https://activepieces.com/llms.txt` | 200 | 129,863 |
| `.../blog/short-term-vs-long-term-memory-for-ai-agents-2026-guide.md` | 200 | 21,217 |
| `.../blog/ai-agent-identity-management-why-you-need-action-boundaries.md` | 200 | 15,564 |
| `.../blog/why-a-workflow-can-run-successfully-and-still-be-wrong.md` | 200 | 20,291 |

落盘证据：`D:/腾讯AI/yt/r197wb/B_ap_llms.txt`、`B_ap_mem.md`、`B_ap_id.md`、`B_ap_wrong.md`。

原文坐实（逐字）：

1. `When an automation completes its entire run without triggering an error code, yet produces an output that is factually wrong or business-damaging, a silent logical failure has occurred.`
2. `out of seven transactional fault classes, the system detects only 2. Five out of seven faults silently pass through the workflow.`
3. 三步审计法：`1. Identify the 'Golden Record' (the source of truth). 2. Sample 10 successful runs from the last 7 days... 3. Manually compare the workflow output against the source.`
4. `Relying on the green checkmarks in your execution history is insufficient.`
5. 两级检查对照表：Order Quantity `Is Integer?` vs `Is within historical range?`；Customer Email `Matches Regex?` vs `Does domain have a valid MX record?`；Discount Code `Is String?` vs `Is the current date before expiry?`
6. 三类断言：`Apply range checks... Implement consistency checks that compare the new output against the previous state to detect impossible jumps in data.`
7. 200 空负载案例：`returned a 200 OK status while delivering an empty JSON object because the authentication token lacked specific permissions` → `successfully update five hundred records with null values`.
8. 新鲜度：`Fetching data from a stale cache results in a 200 OK status code, but provides a value that no longer reflects reality.`

## 二、判非重复理由

| 候选点 | grep 判重 | 结论 |
|---|---|---|
| 审计要抽样"标记为成功"的运行（Golden Record 三步法） | 全库 `Golden Record`/`golden record`/`成功.*抽样` 在**正文**命中 **0**（av 触发词里有"抽样"二字，正文无此判据） | **净新**：与 av §失败注入（变异测试）分层——那条管验证器有没有检出能力，本条管验证器输入样本本身偏不偏 |
| 结构校验 ≠ 语义校验（范围/一致性/新鲜度三类断言） | av §合法 JSON 不等于合规 管"能不能解析/字段合不合规范"，未涉及"值在业务语义上成不成立" | **净新**：补的是合规之后的第二层 |

不落（判重命中，已留痕）：`B_ap_mem.md`（短期/长期记忆分层）与 `wb-context-compressor`、`agent-guild` 的记忆分层重叠 >60%；`B_ap_id.md`（认证 vs 功能限制）与 personal-ai-os 授权分层 + ponytail 权限边界重叠 >60%——均判重复，不落。

## 三、落地

| 文件 | 版本 | 独有点 | 提升层 |
|---|---|---|---|
| engineering/wb-artifact-verification | 2.29.0 → **2.30.0** | 审计要抽样"标记为成功"的运行：静默逻辑失败不在失败日志里（5/7 故障族不报错 + Golden Record 三步抽样） | 工作流 / 可复用 Skill |
| engineering/wb-artifact-verification | （同上） | 结构校验通过 ≠ 语义校验通过：范围/一致性/新鲜度三类断言；200 OK ≠ 有效负载 | 工具 / 可复用 Skill |

复核：crlf=False / fffd=False / 尾空白=0，两个锚点 grep 各 =1。

## 四、协作方

- 豆包：仍停更（末 2026-09-24）。Qoder：2026-09-27 无产出。本轮 2 点自主实拉。
