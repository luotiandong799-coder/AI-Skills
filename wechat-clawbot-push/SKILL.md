---
name: wechat-clawbot-push
version: 1.0.0
display_name: 微信 ClawBot 推送助手
display_name_en: WeChat ClawBot Push Assistant
description: 微信 ClawBot 个人推送助手——把 WorkBuddy 的任务结果、完成通知、待确认提醒主动推送到用户自己的个人微信。基于腾讯官方 iLink / OpenClaw 协议的自托管 stdio MCP 服务器，零第三方依赖（仅 Python 标准库），凭证仅存本机。当用户希望"任务完成后微信提醒我"、要求把结论/报告/告警推送到手机微信、提到"微信推送""ClawBot 通知""推送到我微信"，或需要安装、配置、排查 wechat-clawbot-push 连接器时，应使用本技能。每位同事安装后绑定各自的微信即可独立使用，互不影响。
description_zh: 微信 ClawBot 个人推送助手——把 WorkBuddy 的任务结果、完成通知、待确认提醒主动推送到用户自己的个人微信。基于腾讯官方 iLink / OpenClaw 协议的自托管 stdio MCP 服务器，零第三方依赖（仅 Python 标准库），凭证仅存本机。当用户希望"任务完成后微信提醒我"、要求把结论/报告/告警推送到手机微信，或需要安装、配置、排查 wechat-clawbot-push 连接器时使用。每位同事安装后绑定各自的微信即可独立使用，互不影响。
description_en: Personal WeChat push assistant via ClawBot. Proactively pushes WorkBuddy task results, completion notices, and confirmation reminders to the user's own personal WeChat. Self-hosted stdio MCP server built on Tencent's official iLink / OpenClaw protocol, zero third-party dependencies (Python standard library only), credentials never leave the local machine. Use this skill when the user wants to be notified on WeChat after a task finishes, asks to push conclusions, reports, or alerts to their phone, or needs to install, configure, or troubleshoot the wechat-clawbot-push connector. Each teammate installs and binds their own WeChat independently.
license: MIT
---

# 微信 ClawBot 推送（自托管 MCP）

把任务结果通过微信 iLink（ClawBot）协议主动推送到**用户自己的个人微信**。本技能自带完整可运行的 stdio MCP 服务器脚本（`scripts/wechat_clawbot_push_mcp.py`），零第三方依赖（仅 Python 标准库），每位同事安装后**绑定各自的微信**即可使用，凭证不出本机。

## 典型使用场景

- 长任务（构建、部署、数据处理、自动化流程）完成后，把结论推送到用户手机微信。
- 定时任务 / 自动化编排中，把执行结果、异常告警发到个人微信。
- 需要用户确认的事项，通过微信提醒用户回到 WorkBuddy 处理。

## 暴露的工具（注册为 MCP 连接器后可用）

| 工具 | 作用 |
|---|---|
| `push_wechat_message(text[, auto_acquire])` | 主动推送一条文本到个人微信 |
| `acquire_token()` | 获取/刷新 context_token（需手机给 bot 发一条消息） |
| `bridge_status()` | 查询是否已缓存 token，供推送前自检 |

## 工作原理（要点）

- 协议：腾讯官方 iLink / OpenClaw，`POST https://ilinkai.weixin.qq.com/ilink/bot/{getupdates,sendmessage}`。
- 鉴权 token 自动从本机 `~/.workbuddy/settings.json` 的 `claw.users.*.channels.weixinClawBot.botToken` 读取。
- 主动发送必须带 `context_token`（回复型协议）。首个 token 只能由"用户主动给 bot 发一条消息"后长轮询获取，之后持久化复用。
- 缓存：`~/.workbuddy/wechat-clawbot-push/push_cache.json`（权限 0600）。

## 安装 / 配置流程

首次使用或用户要求安装时，按以下流程配置（面向同事的手把手图文步骤见 `references/install.md`）：

1. **确认脚本位置**：MCP 服务器脚本位于本技能目录的 `scripts/wechat_clawbot_push_mcp.py`（已自带）。
2. **注册连接器**：在 `~/.workbuddy/mcp.json` 的 `mcpServers` 下新增（路径换成脚本的真实绝对路径）：

```json
"wechat-clawbot-push": {
  "type": "stdio",
  "command": "python3",
  "args": ["<本技能目录绝对路径>/scripts/wechat_clawbot_push_mcp.py", "--mcp"],
  "description": "【自托管】个人微信 ClawBot 主动推送桥（iLink 协议，stdio MCP）。"
}
```

3. **Trust 启用**：引导用户打开 WorkBuddy → 连接器管理 → 找到 `wechat-clawbot-push` → 点 **Trust**。
4. **首次授权**：让用户在手机微信给这个 ClawBot 发任意一条消息；随后调用 `acquire_token()`（或运行 `python3 scripts/wechat_clawbot_push_mcp.py --acquire`）即可缓存 token。

## 推送用法

- 用户在对话/自动化中说："把刚才的结果用微信推送到我手机"→ 调用 `push_wechat_message` 工具，`text` 写具体提醒内容。
- 推送前可先调用 `bridge_status()` 自检 token 是否就绪。
- 自动化 prompt 模板：

```
调用 wechat-clawbot-push 连接器的 push_wechat_message 工具，
把任务结论推送到我的个人微信，text 参数写具体提醒内容。
```

## 排错

| 现象 | 处理 |
|---|---|
| `尚未获取 token / NO_TOKEN` | 首次授权未完成：让用户去微信给 bot 发条消息，再调用 `acquire_token()` |
| `TOKEN_EXPIRED`（errcode -14） | token 失效：重新发消息 + `acquire_token()` |
| 推送静默无反应 | 确认连接器已 Trust、WorkBuddy 在运行、手机微信在线 |
| 想给团队群发通知 | 本通道为个人微信 bot，建议改用企业微信 Webhook |

## 安全说明

- 脚本仅用 Python 标准库，不联网回传，不引入第三方包，消除供应链风险。
- botToken / context_token 只存在本机 `~/.workbuddy/` 下，且缓存文件为 0600 权限。
- 本通道为个人微信 bot，**适合"各自推到自己微信"**；若要给整个团队群发工作通知，建议改用企业微信 Webhook。
