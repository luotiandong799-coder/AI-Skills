---
name: wb-browser-reuse
description: >-
  让 AI Agent 安全复用你已登录的真实浏览器去做网页自动化（「借不抢」范式）。当用户要让 Agent 操作自己已登录的网站（公众号后台、企业 SaaS、内网系统）、复用真实登录态而非造测试账号、在独立窗口跑不打断自己、或遇到验证码/扫码/二次确认需要人助时应用。核心方法论：标签页显式借用+归还、确认开关锚定在 Agent 够不到的扩展设置里、人助带类型化结果且拒绝即停、本地优先数据边界清晰、观测-动作纪律（先 observe 取新鲜 ref 再交互、成功可见即停手、session 成功失败都 stop 归还借出标签）。互补于 browser-automation（后者偏无头/自管浏览器常规爬取）。触发词：复用登录态、借浏览器、borrow tab、标签页借用、标签页归还、tab borrow、tab return、human-in-the-loop、request-help、bsk、Agent Window、本地浏览器桥接、不打断用户、验证码交还、复用真实浏览器、已登录浏览器自动化、BrowserSkill。不适用：纯无头/Playwright 自管浏览器的常规爬取（走 browser-automation）；多步实现任务的规划交付（走 wb-spec-driven）。
version: 1.0.0
agent_created: true
---

# wb-browser-reuse（复用真实登录态的本地浏览器桥接）

来源：腾讯开源 `Tencent/BrowserSkill`（MIT，GitHub 已核实 2026-09-19 实拉；README / 内置 `skill/SKILL.md` / `apps/extension/PRIVACY.md`）。提纯其「借不抢」范式为可复用方法论。互补于 `browser-automation`（后者偏无头/自管浏览器的常规爬取与绕反爬），本技能偏「复用你已登录的真实浏览器 + 边界感」。

## 1. 借不抢：标签页显式借用 + 归还（来源：`skill/SKILL.md`·Borrowing and browser settings, 2026-09-19 实拉）
- 动用户已开标签页必须**先 `tab borrow` 再操作，用完立即 `tab return`**；借用只在该步骤内有效，步骤结束即归还。
- **绝不编造 tab ID**、绝不跨无关任务保留一个用户标签、被拒/超时的借用**不得重复**。
- 「能碰的范围」收敛到用户明确借出的那一个；其余页面一概不碰。这把自动化的爆炸半径从「整个浏览器」压到「一个被借出的标签」。

## 2. 确认开关必须锚定在 Agent 够不到的地方（同来源 `skill/SKILL.md` + `PRIVACY.md` §8, 2026-09-19 实拉）
- 借前确认与人助(human-help)的开关存于**浏览器扩展的本地设置**，默认开，且对**已有会话**同样生效。
- 旧参数 `--unattended` / `--no-confirm` / `BSK_REQUEST_HELP=off` **无法覆盖**这些设置；**绝不改浏览器存储/设置去绕过**。
- 原则：安全确认必须落在 Agent 的控制边界之外——prompt 绕不过、参数盖不住。呼应 findings-ledger「确认不可被 prompt 绕过」。

## 3. 人助(human-in-the-loop)要带类型化结果、拒绝即停（同来源 `skill/SKILL.md`·Human steps and recovery, 2026-09-19 实拉）
- 遇登录 / CAPTCHA / OTP / 付款确认 / 同意等阻塞步，用 `request-help` **主动暂停、交还控制权**，用户处理完再续跑。
- 结果类型化：`continued`/`completed` → 重 observe 续跑；`cancelled`/`timed_out` → **尊重拒绝、不得重复请求**；`disabled` → 不请求也不重开，改用已有登录态/可用替代。
- 铁律：**不得在同种失败上死循环、不得换后端绕过限制、不得伪造「已完成」**（导航本身不算完成）。
- 测了两次仍无进展才求人助；给出精确 prompt 与新鲜 target。

## 4. 本地优先、数据边界清晰（同来源 `skill/SKILL.md` + `PRIVACY.md` §1/§4/§6, 2026-09-19 实拉）
- 架构：CLI/daemon + 浏览器扩展，走 **loopback WebSocket（默认端口 52800）**，全链路本地、数据不出机器；远程模式须**显式配对**，自动化数据只发往用户选定的 daemon/gateway。
- 不枚举浏览器历史 / 书签 / 保存的密码 / 自动填充；不内置分析/广告/追踪。
- 操作审计默认关；开启后记录**不含输入值与截图**，仅时间戳/工具类型/网站源/元素名(基础脱敏)/状态/错误码。
- 结论：复用真实登录态 ≠ 放任数据外泄；本地优先是隐私底线。

## 5. 观测-动作纪律 + 会话生命周期（同来源 `skill/SKILL.md`·Read and interact / Task workflow, 2026-09-19 实拉）
- 先 `observe` 取**新鲜 ref** 再交互；导航 / 大 DOM 变更即令 ref 失效，下次交互前必须**重 observe**。
- 「成功可见即停手，不刷新不复查」——避免无意义轮询与重复动作（与 dbg「别在同种失败死循环」同源）。
- 会话成功**与**失败都要 `session stop`（同时归还借出的标签）；**绝不依赖空闲清理、绝不靠重启 daemon 收尾**。
- 远程/沙箱环境：复用同一 `BSK_HOME` + `BSK_AUTO_START=0`，环境不跨 shell 持久；启动失败重试一次即 `bsk doctor`，不循环启停、不删运行时文件。

## 与现有技能的边界
- 互补 `browser-automation`（无头/自管浏览器常规爬取、填表/抓数/绕反爬）；本技能补「复用你已登录的真实浏览器 + 边界感（借/还/确认/人助/本地优先）」这一条它没覆盖的路线。
- `wb-debug-loop` 的「别在同种失败死循环」在浏览器场景的具象化 → 本技能 §3/§5；不重复展开根因循环。
- `wb-execute-discipline` 的「失败换路攻坚」→ 本技能 §3「不得换后端绕过」同源；不重复。
