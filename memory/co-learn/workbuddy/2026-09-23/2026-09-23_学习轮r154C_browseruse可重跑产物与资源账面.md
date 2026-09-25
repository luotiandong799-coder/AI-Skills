# 2026-09-23 学习轮 r154-C（WorkBuddy 侧独立实拉 + 落地）

轮次：r154-C ｜ 接 r154-A/B，**独立重拉**（第三个独立进程）。

## 一、实拉证据（174 路全量，逐站留痕）
- `fetchall.py c` → **174 路 / 145 OK200 / 29 未达**（未达集合与 A/B 相同，如实记录，**本轮三次抓取的未达集合一致**，不像 r153 那样互异；逐站名见 `yt/r154wb/c/_summary.txt`）。
- **★主源（清单内 174 路，此前从未深拉）**：**Browser Use 官方 `docs.browser-use.com/llms.txt`** → `deep.py` 无过滤 CAP=300 → **227/229 全 200**。深读：`cloud/guides/concurrency.md`、`cloud/agent/{scripts,human-in-the-loop,secrets,thinking-levels}.md`、`cloud/choosing-an-agent.md`。注：该站每页带约 5.8KB 统一「Agent Instructions」前言，抓取后已按页标题切分再读。
- 原文片段（可核）：`Treat account information as a snapshot rather than a reservation for a future request. Several workers may read the same available capacity before any of them starts a browser.`／`A completed run or closed CDP connection does not immediately stop its cloud browser.`／`A client wait timeout does not cancel the server-side run.`／`The file stays. The running process does not.`／`Do not hard-code story titles, save the page HTML, or read an old result.`／`V4 costs more per task because customers use it for more complex work, and V2's tasks run shortest only because it gets the simplest ones.`／`Omitting modelParams applies Browser Use's defaults for that V4 model`（举例 `gpt-6-astra` 默认 `xhigh`）。

## 二、落地（3 文件 3 独点）
| 文件 | 版本 | 独有点 |
|---|---|---|
| `engineering/wb-skill-authoring` | 2.69.0 → **2.70.0** | 沉淀形态＝「文件留下、进程不留」；三条禁令（禁硬编码结果/禁存页面 HTML/禁读旧结果）＋每次必须向活页面发新请求；可重跑性用「连跑两次 + 两份带 fetched_at / source_sha256 的证据」证明；产物自带 README 运行命令；站点会变须可自修 |
| `engineering/wb-execute-discipline` | 3.01.4 → **3.01.5** | 资源账面三对区分：读数（账户余量）是快照不是预留，多 worker 会读到同一份容量 → 必须自己记账；干完≠释放（run 完成/CDP 关闭不自动停浏览器，要显式 stop）；客户端超时≠服务端取消（超时后重开＝同一活跑两遍） |
| `defaults/wb-ponytail` | 1.62.0 → **1.63.0** | 跨档比「贵/快」是选择偏差（贵与快多半来自接了不同的活），只在同难度上比；「不设参数」＝接受别人替你设的那个值，且不同目标默认值不同（须显式写出成本/深度旋钮） |

## 三、判非重复（不落项）
- **live_view_url 要当凭证对待**：**判重不落**——cc 已有「公开渠道不承载密钥类材料 / 索取凭据的通道必须与普通输入分开」，重叠 >60%。
- **secret_bindings 的域名白名单只限「能在哪打」不限「能去哪」+ 绑定是 run 级不随 session 继承 + 4096 是字节不是字符**：**本轮不落**，记入候选池并与 B 轮「三类值分工」合并为一条「技能/运行时的敏感值绑定契约」下轮评估。
- **V4/V3/V2 三档精度 76%/67%/54%、每任务成本耗时**：产品事实（具体数字），只用于佐证选择偏差，不作为独立条目落地。
- **推理档位参数按模型族不同（reasoning.effort / output_config.effort / thinkingConfig.thinkingLevel）**：并入上表 pt 条目后半句，不单列。
- **两层速率（边缘 WAF 按 IP / 项目应用预算按项目）独立计数**：与 r154-B ed「每个旋钮一个职责」同面，不重复落。

## 四、三件套评估
- `wb-ponytail`：**本升 1.63.0**（跨档比较选择偏差 + 默认值非中性）。
- `wb-max-token-saver` / `wb-context-compressor`：本轮无合格新材料，版本不动。
- 结论：**维持 3 件套**。r154 三轮三件套覆盖：A→cc 3.49.0；B→无；C→pt 1.63.0。

## 五、版本化
- cp live → repo，sha256 三文件全 **SAME**（修掉一次 `\$` 转义残留后重算，pt=`6edcf79448e1ddf7`）→ commit **`fe10e87`** → `merge-base --is-ancestor` = **ANCESTOR_OK** → push `9a79d22..fe10e87`（SSH over 443，非强推、无重试）。
