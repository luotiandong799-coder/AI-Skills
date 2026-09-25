#!/usr/bin/env python3
"""Send a text message to the user via the local WorkBuddy Claw WeChat bot.

Reads bot credentials from ~/.workbuddy/settings.json and POSTs to the
ilinkai weixin bot sendmessage endpoint. Usage: python send_wx.py "message text"
"""
import base64
import json
import os
import random
import sys
import time
import urllib.request

SETTINGS_PATH = os.path.expandvars("%USERPROFILE%/.workbuddy/settings.json")


def load_creds():
    with open(SETTINGS_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    claw = cfg.get("claw", {})
    users = claw.get("users", {})
    for uid, u in users.items():
        ch = u.get("channels", {}).get("weixinClawBot")
        if ch and ch.get("enabled"):
            return {
                "token": ch["botToken"],
                "to_user": ch["userId"],
                "base": ch.get("baseUrl", "https://ilinkai.weixin.qq.com").rstrip("/"),
            }
    raise SystemExit("weixinClawBot channel not found/enabled in settings.json")


def warmup(c=None):
    """Activate the bot's server-side send session.

    The Claw bot's sendmessage endpoint only accepts a push when the bot has an
    *active* server-side session, which exists only for a short window after the
    bot has polled (getupdates) or received an inbound message. A standalone
    sendmessage without a recent warm-up is rejected with errcode:-14
    "session timeout". Calling getupdates first establishes that session.
    Best-effort: failures here are non-fatal; sendmessage will surface the real
    error if the session is still down.
    """
    if c is None:
        c = load_creds()
    url = f'{c["base"]}/ilink/bot/getupdates'
    body = {"base_info": {"channel_version": "cbc-1.0.0"}, "get_updates_buf": ""}
    raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
    uin = base64.b64encode(str(random.getrandbits(32)).encode()).decode()
    req = urllib.request.Request(url, data=raw, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("AuthorizationType", "ilink_bot_token")
    req.add_header("Content-Length", str(len(raw)))
    req.add_header("X-WECHAT-UIN", uin)
    req.add_header("Authorization", "Bearer " + c["token"])
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            r.read()
    except Exception:
        pass


def send(text):
    c = load_creds()
    warmup(c)
    url = f'{c["base"]}/ilink/bot/sendmessage'
    body = {
        "msg": {
            "from_user_id": "",
            "to_user_id": c["to_user"],
            "client_id": "cbc-%d-%s"
            % (int(time.time() * 1000), "".join(random.choice("abcdef0123456789") for _ in range(6))),
            "message_type": 2,
            "message_state": 2,
            "item_list": [{"type": 1, "text_item": {"text": text}}],
        },
        "base_info": {"channel_version": "cbc-1.0.0"},
    }
    raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
    uin = base64.b64encode(str(random.getrandbits(32)).encode()).decode()
    req = urllib.request.Request(url, data=raw, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("AuthorizationType", "ilink_bot_token")
    req.add_header("Content-Length", str(len(raw)))
    req.add_header("X-WECHAT-UIN", uin)
    req.add_header("Authorization", "Bearer " + c["token"])
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return "HTTP_ERR %s %s" % (e.code, e.read().decode("utf-8", "ignore"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: send_wx.py <message>")
        raise SystemExit(1)
    print(send(sys.argv[1]))
