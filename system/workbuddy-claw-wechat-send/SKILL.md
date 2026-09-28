---
name: workbuddy-claw-wechat-send
description: Send a text message to the user through the local WorkBuddy assistant's WeChat channel (Claw / weixinClawBot bot). Use this skill when a task requires pushing a notification or result to the user via their connected WeChat bot, e.g. "send me this via WeChat", "push to my WeChat", or an automation that delivers messages through the local assistant's WeChat channel.
version: "1.0.0"
display_name: 微信助理消息推送
display_name_en: WeChat Claw Bot Message Push
description_zh: 通过本地 WorkBuddy 助理已配置的微信通道（Claw / weixinClawBot 机器人）向用户推送文本消息。适用于需要将通知或任务结果经微信送达用户的场景，例如自动化每日资讯推送、定时提醒、任务结果回传等。无需额外申请微信 API 凭证，直接复用本地 settings.json 中已落盘的 botToken 与接收人 userId。发送前会自动以 getupdates 轮询进行会话热身，规避冷 bot 的 session timeout。
description_en: Send a text message to the user through the local WorkBuddy assistant's WeChat channel (Claw / weixinClawBot bot). Use this skill when a task needs to push a notification or result to the user via their connected WeChat bot, e.g. daily news push, reminders, or delivering automation output. No external WeChat API credentials are needed — the bot token and recipient id are already present in the local WorkBuddy settings. A getupdates warm-up is performed automatically before sending to avoid session timeout on a cold bot.
agent_created: true
---

# Send a message via the WorkBuddy Claw WeChat bot

This skill sends a text message to the user's WeChat through the locally configured
`weixinClawBot` (Claw) channel. No external WeChat API credentials are needed — the
bot token and recipient id are already present in the local WorkBuddy settings.

## When to use

- A user request or automation needs to deliver a message through "the local assistant's
  WeChat channel" / "微信通道" / Claw bot.
- Do NOT use this for email (agent-mail), enterprise WeChat (wecom), or other IM platforms.

## How to send (procedural)

1. Read the bot credentials from `~/.workbuddy/settings.json`:
   - Path: `claw.users.<uid>.channels.weixinClawBot`
   - Fields needed: `botToken`, `userId` (recipient), `baseUrl` (usually `https://ilinkai.weixin.qq.com`).
2. POST to `{baseUrl}/ilink/bot/sendmessage` with:
   - Headers:
     - `Content-Type: application/json`
     - `AuthorizationType: ilink_bot_token`
     - `X-WECHAT-UIN: <random base64 of a 32-bit int>`
     - `Authorization: Bearer <botToken>`
     - `Content-Length: <byte length of body>`
   - Body (JSON):
     ```json
     {
       "msg": {
         "from_user_id": "",
         "to_user_id": "<userId from settings>",
         "client_id": "cbc-<ms-timestamp>-<6 hex chars>",
         "message_type": 2,
         "message_state": 2,
         "item_list": [ { "type": 1, "text_item": { "text": "<message>" } } ]
       },
       "base_info": { "channel_version": "cbc-1.0.0" }
     }
     ```
3. A successful response contains a `message_id`. Non-zero `ret` indicates failure
   (check `errmsg`).

## Reference implementation

Use `scripts/send_wx.py`. It reads settings automatically and sends a message passed
as a CLI argument.

```bash
python scripts/send_wx.py "你的消息内容"
```

## Notes / pitfalls

- The token contains `@` and `:` — it is used verbatim as a Bearer token; no extra encoding.
- `item_list[].type` for text is `1`; the outer `message_type`/`message_state` are `2`.
- `context_token` may be omitted (the desktop app omits it for bot-initiated pushes).
- If the channel is disabled or the bot token is stale, the API returns a non-zero `ret`.
- **Session warm-up (critical):** `sendmessage` is only accepted when the bot has an
  active server-side session, which exists only briefly after a `getupdates` poll or
  inbound message. A detached/standalone send without a recent poll returns
  `errcode:-14 "session timeout"` (or `ret:-2 "prepare failed"` with the
  `AuthorizationType` header). Always call `getupdates` immediately before
  `sendmessage`. `send_wx.py`'s `send()` now does this automatically via `warmup()`.
  Practical implication: the push works reliably only while the assistant/Claw app
  is connected and polling (or right after the user sent a message); a cold bot will
  need one inbound trigger or a warm-up poll first.
