---
name: browser-automation
description: 浏览器与网页自动化统一入口（合并原 stealth-browser 与 smooth-browser 两个同类技能，并保留两者各自的强项）。当需要打开网页、填表、抓取网页数据、测试站点、登录后持久复用会话、绕过反爬/Cloudflare/验证码、或跑静默无头自动化时使用。含四条路径：内置 agent-browser（常规默认）→ 持久登录 profile → 本地反检测脚本（CF / 验证码 / 代理 / 会话保存）→ 云端自然语言浏览器代理（smooth.sh，需已安装且有余量）。触发词：打开网站、抓取网页、填表、登录、爬取、自动化网页、绕过 Cloudflare、验证码、无头浏览器、browser automation、scrape、fill the form、log into。
version: 1.1.0
agent_created: true
sources:
  - 合并自旧 skill `stealth-browser` v1.0.0（本地四层反检测 + 8 个 python 脚本）
  - 合并自旧 skill `smooth-browser` v0.1.0（smooth.sh 云端自然语言浏览器代理：会话纪律 / 结构化输出 / live-view 人工接管）
---

# browser-automation（网页自动化：先选路径，再动手）

**核心判断：能静默轻量就用内置通道；被拦住才升级到本地脚本；云端付费通道最后考虑。同一任务不要多通道并行试——浪费额度且难定位问题。**

**前置检查（2026-09-13 实测教训，失败≥2次根因诊断结论）**：`agent-browser open` 首次调用挂起超时（120s+ 被杀、无输出）的根因是 **ms-playwright Chromium 未安装**——open 会在启动时静默下载 ~500MB。用前先探针：`ls "$LOCALAPPDATA/ms-playwright"`（Windows）或 `ls ~/.cache/ms-playwright`（Linux/mac）；目录不存在/为空 → **先 `agent-browser install`（后台跑，约几分钟）再 open**，不要延长超时硬冲（违反 wb-execute-discipline 原则三）。

## 一、路径选择

| 任务 | 走哪条 | 成本 |
|---|---|---|
| 打开页面、取内容、截图、点选等常规操作 | **内置 `agent-browser`**（默认） | 最低 |
| 需要登录一次、后续长期复用登录态 | **本技能 Profile 持久登录**（见二） | 低 |
| 被判定为机器人 / 反爬拦截 | **本地反检测脚本**（见三） | 中 |
| Cloudflare Turnstile / JS 挑战 | `scripts/cf_bypass.py` 或 DrissionPage 自动等待 | 中 |
| CAPTCHA（reCAPTCHA / hCaptcha） | `scripts/solve_captcha.py`（需打码平台 key） | 中 |
| 需要人工接管（2FA、复杂授权） | live-view / headed 模式，用户手动完成后继续 | 低 |
| 自然语言驱动的复杂网页任务，且本机已装 `smooth` CLI 且有余额 | 云端 smooth 通道（见五） | 高（付费） |

**相邻技能**：要的是「媒体内容本体」（反爬短链里的视频/图片、逐帧取证、无字幕视频）而不是页面文本 → 转 `wb-media-forensics`（Edge 无头取播放地址 + PyAV 抽帧 + 联络表多模态读图）。本技能只负责把页面打开、把 DOM/数据拿到；拿到播放地址之后的抽帧读图不在这里做。

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

## 五、云端通道（smooth.sh，可选）

仅当 `smooth` CLI 已安装且账号有余量时使用；提供 `create-profile` / `start-session --url` / `run --metadata --response-model` / `extract` / `evaluate-js` / `live-view` / `close-session` 等命令，支持 `--json`。
**若未安装或余额不足 → 直接用上面的本地通道，不要为了用它去装依赖。**

## 六、反模式
- 简单取页面却启动重通道（云端付费 / 反检测脚本），费钱且慢
- 命中反爬先换 IP / 上代理，却没检查是否是选择器或等待时机写错
- 一个会话塞多个不相关任务，状态互相污染
- 任务指令写到"点第几个按钮"这种粒度，或反过来只说一个宏大目标
- 登录态不保存，每次都重新登录（还触发风控）
- 会话不关，留着僵尸会话占额度、状态不落盘

## 合并说明
原 `stealth-browser`（本地反检测四层 + 脚本）与 `smooth-browser`（云端自然语言代理 + 会话纪律 / 结构化输出 / live-view）是同一功能位的两个重复技能。本技能**保留 stealth 的全部脚本与反检测能力，同时把 smooth 的会话纪律、任务粒度原则、结构化输出与人工接管流程吸收进来**；两个旧目录已删除（git 历史可回溯）。常规任务仍优先用内置 `agent-browser`。
