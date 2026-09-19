---
name: browser-automation
description: 浏览器与网页自动化统一入口（合并原 stealth-browser、smooth-browser 与 wb-browser-reuse 三个同类技能，并保留各自强项）。当需要打开网页、填表、抓取网页数据、测试站点、登录后持久复用会话、绕过反爬/Cloudflare/验证码、跑静默无头自动化、或让 Agent 复用你已登录的真实浏览器（不打断你、爆炸半径收敛到一个借出的标签）时使用。含五条路径：内置 agent-browser（常规默认）→ 持久登录 profile → 本地反检测脚本（CF / 验证码 / 代理 / 会话保存）→ 复用真实登录态的本地浏览器桥接 bsk（借不抢 + 类型化人助）→ 云端自然语言浏览器代理（smooth.sh，需已安装且有余量）。触发词：打开网站、抓取网页、填表、登录、爬取、自动化网页、绕过 Cloudflare、验证码、无头浏览器、browser automation、scrape、fill the form、log into、复用登录态、借浏览器、borrow tab、标签页借用、标签页归还、tab borrow、tab return、human-in-the-loop、request-help、bsk、Agent Window、本地浏览器桥接、不打断用户、验证码交还、复用真实浏览器、已登录浏览器自动化、BrowserSkill。
version: 2.0.0
agent_created: true
sources:
  - 合并自旧 skill `stealth-browser` v1.0.0（本地四层反检测 + 8 个 python 脚本）
  - 合并自旧 skill `smooth-browser` v0.1.0（smooth.sh 云端自然语言浏览器代理：会话纪律 / 结构化输出 / live-view 人工接管）
  - 合并自旧 skill `wb-browser-reuse` v1.0.0（腾讯开源 BrowserSkill「借不抢」范式：标签页借用/归还、确认锚定扩展设置、类型化人助、本地优先数据边界、观测-动作纪律；2026-09-19 实拉 github.com/Tencent/BrowserSkill 的 README / `skill/SKILL.md` / `apps/extension/PRIVACY.md`）
---

# browser-automation（网页自动化：先选路径，再动手）

**核心判断：能静默轻量就用内置通道；被拦住才升级到本地脚本；要复用用户真实登录态走本地桥接；云端付费通道最后考虑。同一任务不要多通道并行试——浪费额度且难定位问题。**

**前置检查（2026-09-13 实测教训，两次根因修正）**：
1. `agent-browser open` 首次调用挂起超时（120s+ 被杀、无输出）的根因是 **ms-playwright Chromium 未安装**——open 会在启动时静默下载 ~500MB。用前先探针：`ls "$LOCALAPPDATA/ms-playwright"`（Windows）或 `ls ~/.cache/ms-playwright`（Linux/mac）；目录不存在/为空 → **先 `agent-browser install`（后台跑，约几分钟）再 open**，不要延长超时硬冲（违反 wb-execute-discipline 原则三）。
2. **open 前台调用容易被工具超时误杀**：冷启动 + 导航可能超过命令超时 → **用后台模式启动**（`(agent-browser open <url> > log 2>&1 &)` + sleep 后 snapshot），不要立刻下"通道不可用"结论——曾因前台超时误判为"沙箱禁浏览器"，被 example.com 探针证伪。
3. **代理兼容坑**：VPN（uniproxy 等）开系统代理时，curl 经代理可通但 Chromium 的 CONNECT 隧道被拒（ERR_TUNNEL_CONNECTION_FAILED）——客户端级不兼容，agent 侧无解，标注归属用户（开 TUN 模式 / 换节点）。

## 一、路径选择

| 任务 | 走哪条 | 成本 |
|---|---|---|
| 打开页面、取内容、截图、点选等常规操作 | **内置 `agent-browser`**（默认） | 最低 |
| 需要登录一次、后续长期复用登录态 | **本技能 Profile 持久登录**（见二） | 低 |
| 被判定为机器人 / 反爬拦截 | **本地反检测脚本**（见三） | 中 |
| Cloudflare Turnstile / JS 挑战 | `scripts/cf_bypass.py` 或 DrissionPage 自动等待 | 中 |
| CAPTCHA（reCAPTCHA / hCaptcha） | `scripts/solve_captcha.py`（需打码平台 key） | 中 |
| 需要人工接管（2FA、复杂授权） | live-view / headed 模式，用户手动完成后继续 | 低 |
| **要复用你已登录的真实浏览器、不打断你、爆炸半径收敛到一个借出的标签** | **本地桥接 bsk**（见五） | 低 |
| 自然语言驱动的复杂网页任务，且本机已装 `smooth` CLI 且有余额 | 云端 smooth 通道（见六） | 高（付费） |

**相邻技能**：
- 要的是「媒体内容本体」（反爬短链里的视频/图片、逐帧取证、无字幕视频）而不是页面文本 → 转 `wb-media-forensics`（Edge 无头取播放地址 + PyAV 抽帧 + 联络表多模态读图）。本技能只负责把页面打开、把 DOM/数据拿到；拿到播放地址之后的抽帧读图不在这里做。
- 走五（bsk 本地桥接）时需要该 CLI 的完整命令参考 → 读 `browser-skill`（bsk 官方技能，由 `bsk` 自行安装维护，不在本仓库版本控制内）。
- 只要页面正文转 Markdown / 批量列表页结构化字段，且不需要交互 → 转 `web-scrape`（本地抓取引擎，三档难度 + `--fields`）。

**升级顺序不可跳级**：遇到失败先怀疑选择器 / 等待时机 / 会话态，再考虑上反检测，最后才上云端。

## 二、登录与会话持久化（先 headed 登录，后 headless 复用）

```bash
# 1) 打开可见浏览器，用户手动登录
python scripts/stealth_session.py -u "https://target.com/login" -s sitename --headed
# 2) 登录成功后保存会话
python scripts/stealth_session.py -u "https://target.com" -s sitename --headed --save
# 3) 之后无头复用
python scripts/stealth_session.py -u "https://target.com" -s sitename --load
```
会话存于 `~/.workbuddy/browser-sessions/<sitename>.json`；登录尝试记录在 `attempts.json`。

**会话纪律（来自 smooth 通道的强项，通用适用）**
- **一个网站一个 profile，命名要有含义**（如 `github-account`、`shop-work`），并把「哪个 profile 对应哪个站点」写进记忆，下次直接复用，不重复登录
- **会话是资源，用完必关**；关闭后等 5 秒再复用 profile，确保 cookie 与状态落盘
- **浏览器状态 ≠ 代理记忆**：同一会话连续跑多个任务时，cookie/URL 保留，但**上一步的结论不会自动带过去**，需要显式传入（把上一步结果作为变量写进下一步指令）
- **同一会话一次只跑一个任务**；要并行就开多个会话、每个交给一个子 agent，且**会话由主 agent 创建分配**，不要让子 agent 自己建

**注意与五的区别**：本节的 profile 是**自管浏览器 + 自己保存的登录态**；如果目标站点必须用**用户当前正在用的那个浏览器里已有的登录态**（扫码登录、企业 SSO、内网站点、二次验证），走五，不要在这里重放登录。

## 三、本地反检测四层（脚本）

| 层 | 能力 | 脚本 |
|---|---|---|
| 反检测引擎 | puppeteer-extra-stealth、指纹伪装（WebGL / Canvas / Audio） | `stealth_session.py` |
| 挑战绕过 | Cloudflare Turnstile / JS 挑战、hCaptcha / reCAPTCHA | `cf_bypass.py`、`solve_captcha.py` |
| 会话持久化 | cookie / localStorage 存取、多 profile | `session_manager.py` |
| 代理与身份 | 轮换住宅代理、UA 轮换、时区与语言伪装 | `proxy_rotate.py` |

依赖：`puppeteer-extra` + `puppeteer-extra-plugin-stealth`、`playwright`、`undetected-chromedriver`、`DrissionPage`（`pip install undetected-chromedriver DrissionPage`）。
打码 key 存 `~/.workbuddy/secrets/captcha.json`，代理池存 `~/.workbuddy/secrets/proxies.json`。

执行策略：
1. **先静默后显示**——先 headless 试，失败或需验证码再切 headed，避免打扰用户
2. **断点续传**——长任务（>50 项）用 `task_runner.py` 记进度，跳过已完成项
3. **超时与重试**——单页默认 30 秒，失败自动重试 3 次；每 50 项落一次进度
4. **顽固 Cloudflare** 可上 FlareSolverr 容器（`localhost:8191`）

## 四、任务粒度：给目标，不给步骤

无论走哪条通道，指令粒度决定成功率：

- ✅ 好：「在 LinkedIn 找 5 个 Amazon 的 SDE，返回主页链接」「查 iPhone 17 在 Amazon 的价格」
- ❌ 太细：「点搜索按钮」——过度指挥，把决策权收走了
- ❌ 太粗：「找适合我们公司的软件工程师」——这是目标不是任务，需自己先拆成可执行子任务

**结构化输出**：需要可解析结果时给 schema，而不是让它写一段话。纯取数且已在正确页面时用 `extract`（不走 agent 步数，更省更快）；需要先导航/交互再用 `run`。

## 五、复用真实登录态（本地浏览器桥接，bsk / BrowserSkill）

适用：站点靠**用户真实浏览器里已有的登录态**才能进（公众号后台、企业 SaaS、内网系统、扫码登录、二次验证），造测试账号不可行，或用户明确要求「别打断我」。

**本节的五条是方法论铁律，不是某个 CLI 的操作手册；换实现也要守。** 实现来源：腾讯开源 `Tencent/BrowserSkill`（本地 CLI/daemon + 浏览器扩展，loopback WebSocket 默认端口 52800）。

### 5.1 借不抢：标签页显式借用 + 归还
- 动用户已开标签页必须**先 `tab borrow` 再操作，用完立即 `tab return`**；借用只在该步骤内有效，步骤结束即归还。
- **绝不编造 tab ID**、绝不跨无关任务保留一个用户标签、被拒/超时的借用**不得重复**。
- 「能碰的范围」收敛到用户明确借出的那一个；其余页面一概不碰。这把自动化的爆炸半径从「整个浏览器」压到「一个被借出的标签」。

### 5.2 确认开关必须锚定在 Agent 够不到的地方
- 借前确认与人助（human-help）的开关存于**浏览器扩展的本地设置**，默认开，且对**已有会话**同样生效。
- 旧参数 `--unattended` / `--no-confirm` / `BSK_REQUEST_HELP=off` **无法覆盖**这些设置；**绝不改浏览器存储/设置去绕过**。
- 原则：安全确认必须落在 Agent 的控制边界之外——prompt 绕不过、参数盖不住。呼应 findings-ledger「确认不可被 prompt 绕过」。

### 5.3 人助（human-in-the-loop）带类型化结果、拒绝即停
- 遇登录 / CAPTCHA / OTP / 付款确认 / 同意等阻塞步，用 `request-help` **主动暂停、交还控制权**，用户处理完再续跑。
- 结果类型化：`continued`/`completed` → 重 observe 续跑；`cancelled`/`timed_out` → **尊重拒绝、不得重复请求**；`disabled` → 不请求也不重开，改用已有登录态/可用替代。
- 铁律：**不得在同种失败上死循环、不得换后端绕过限制、不得伪造「已完成」**（导航本身不算完成）。
- 测了两次仍无进展才求人助；给出精确 prompt 与新鲜 target。

### 5.4 本地优先、数据边界清晰
- 架构：CLI/daemon + 浏览器扩展，走 **loopback WebSocket（默认端口 52800）**，全链路本地、数据不出机器；远程模式须**显式配对**，自动化数据只发往用户选定的 daemon/gateway。
- 不枚举浏览器历史 / 书签 / 保存的密码 / 自动填充；不内置分析/广告/追踪。
- 操作审计默认关；开启后记录**不含输入值与截图**，仅时间戳/工具类型/网站源/元素名（基础脱敏）/状态/错误码。
- 结论：复用真实登录态 ≠ 放任数据外泄；本地优先是隐私底线。

### 5.5 观测-动作纪律 + 会话生命周期
- 先 `observe` 取**新鲜 ref** 再交互；导航 / 大 DOM 变更即令 ref 失效，下次交互前必须**重 observe**。
- 「成功可见即停手，不刷新不复查」——避免无意义轮询与重复动作（与 `wb-debug-loop`「别在同种失败死循环」同源）。
- 会话成功**与**失败都要 `session stop`（同时归还借出的标签）；**绝不依赖空闲清理、绝不靠重启 daemon 收尾**。
- 远程/沙箱环境：复用同一 `BSK_HOME` + `BSK_AUTO_START=0`，环境不跨 shell 持久；启动失败重试一次即 `bsk doctor`，不循环启停、不删运行时文件。

## 六、云端通道（smooth.sh，可选）

仅当 `smooth` CLI 已安装且账号有余量时使用；提供 `create-profile` / `start-session --url` / `run --metadata --response-model` / `extract` / `evaluate-js` / `live-view` / `close-session` 等命令，支持 `--json`。
**若未安装或余额不足 → 直接用上面的本地通道，不要为了用它去装依赖。**

## 七、反模式
- 简单取页面却启动重通道（云端付费 / 反检测脚本），费钱且慢
- 命中反爬先换 IP / 上代理，却没检查是否是选择器或等待时机写错
- 一个会话塞多个不相关任务，状态互相污染
- 任务指令写到"点第几个按钮"这种粒度，或反过来只说一个宏大目标
- 登录态不保存，每次都重新登录（还触发风控）
- 会话不关，留着僵尸会话占额度、状态不落盘
- **碰用户已开的浏览器不先借标签、用完不还，或编造 tab ID**（见 5.1）
- **试图用参数 / 改浏览器设置绕过确认开关，或在用户拒绝后重复请求人助**（见 5.2 / 5.3）
- **导航完就宣布任务完成**，或失败后换后端绕限制、在同种失败上死循环（见 5.3）

## 合并说明
原 `stealth-browser`（本地反检测四层 + 脚本）与 `smooth-browser`（云端自然语言代理 + 会话纪律 / 结构化输出 / live-view）是同一功能位的两个重复技能 → 合并为 v1.2.0：**保留 stealth 的全部脚本与反检测能力，同时把 smooth 的会话纪律、任务粒度原则、结构化输出与人工接管流程吸收进来**。
2026-09-19 再把 `wb-browser-reuse`（腾讯 BrowserSkill 方法论蒸馏）并入本技能 v2.0.0：它覆盖的是同一功能位下的第五条路径「复用你已登录的真实浏览器」，与已有四条路径共享触发词空间（「浏览器自动化 / 抓网页」），独立成 skill 会造成路由二义。并入后**其五条方法论（借不抢 / 确认锚定 / 类型化人助 / 本地优先 / 观测-动作纪律）原样保留**，见五；`browser-automation` 自此是浏览器自动化的**唯一入口**，bsk 的命令细节仍由 `bsk` 自管的 `browser-skill` 承载。
三个旧目录已删除（git 历史可回溯）。常规任务仍优先用内置 `agent-browser`。
