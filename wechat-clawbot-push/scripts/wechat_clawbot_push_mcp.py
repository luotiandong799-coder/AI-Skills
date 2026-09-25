#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自托管版「微信 ClawBot 主动推送」MCP 服务器（stdio）
=================================================================
取代第三方 PyPI 包 wechat-clawbot-push，改为我们自己的实现，目的是：
  1. 零第三方依赖（仅用 Python 标准库）→ 消除供应链投毒风险；
  2. 源码完全自审、可控，不引入未知作者代码；
  3. 缓存文件强制 0600 权限 → 修复明文 token 泄露隐患；
  4. 对 iLink 返回码做健壮判断，失败可诊断。

协议契约（iLink / OpenClaw 官方）：
  - 收消息: POST https://ilinkai.weixin.qq.com/ilink/bot/getupdates
  - 发消息: POST https://ilinkai.weixin.qq.com/ilink/bot/sendmessage
  - 鉴权:  AuthorizationType: ilink_bot_token + Authorization: Bearer {bot_id:secret}
           X-WECHAT-UIN: base64(随机uint32) 防重放
  - 主动发须带回 context_token（随入站消息返回，持久化可复用）

暴露工具（与第三方包同名，便于无缝替换）：
  - push_wechat_message(text[, auto_acquire])
  - acquire_token()
  - bridge_status()

依赖：仅标准库。token 自动从 ~/.workbuddy/settings.json 读取；
      context_token / user_id / 游标缓存在 ~/.workbuddy/wechat-clawbot-push/push_cache.json（0600）。
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE_URL = "https://ilinkai.weixin.qq.com"
CHANNEL_VERSION = "1.0.3"

APP_DIR = os.path.expanduser("~/.workbuddy/wechat-clawbot-push")
os.makedirs(APP_DIR, exist_ok=True)
CACHE_PATH = os.path.join(APP_DIR, "push_cache.json")
SETTINGS_PATH = os.path.expanduser("~/.workbuddy/settings.json")


# ------------------------- 日志/输出（stdio 铁律）-------------------------
def log(msg):
    sys.stderr.write("[mcp] " + msg + "\n")
    sys.stderr.flush()


def send(obj):
    # stdout 只能输出 JSON-RPC（newline-delimited），日志一律走 stderr
    data = (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8")
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()


# ------------------------- 持久化（权限加固）-------------------------
def _harden_cache_perms():
    try:
        if os.path.exists(CACHE_PATH):
            os.chmod(CACHE_PATH, 0o600)
    except Exception:
        pass


def load_cache():
    _harden_cache_perms()
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_cache(data):
    tmp = CACHE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.chmod(tmp, 0o600)
    os.replace(tmp, CACHE_PATH)
    _harden_cache_perms()


# ------------------------- 配置/凭证 -------------------------
def get_token_from_settings():
    if not os.path.exists(SETTINGS_PATH):
        raise RuntimeError("找不到 settings.json: " + SETTINGS_PATH)
    with open(SETTINGS_PATH, encoding="utf-8") as f:
        d = json.load(f)
    for _uid, u in d.get("claw", {}).get("users", {}).items():
        ch = u.get("channels", {}).get("weixinClawBot", {})
        bt = ch.get("botToken")
        if bt and ":" in bt:
            return bt
    raise RuntimeError("settings.json 中未找到 weixinClawBot.botToken")


def make_uin_header():
    u = int.from_bytes(os.urandom(4), "big")
    return base64.b64encode(str(u).encode("ascii")).decode("ascii")


def ilink_post(path, body, secret):
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(BASE_URL + path, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("AuthorizationType", "ilink_bot_token")
    req.add_header("Authorization", "Bearer " + secret)
    req.add_header("X-WECHAT-UIN", make_uin_header())
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8"))
        except Exception:
            return e.code, {"ret": -1, "errmsg": str(e)}
    except Exception as e:
        return -1, {"ret": -1, "errmsg": str(e)}


# ------------------------- 业务函数 -------------------------
def acquire_token_once():
    """长轮询一次获取 context_token + user_id。返回 (ok, detail)。"""
    bearer = get_token_from_settings()
    cache = load_cache()
    cursor = cache.get("get_updates_buf", "")
    status, resp = ilink_post(
        "/ilink/bot/getupdates",
        {"get_updates_buf": cursor, "base_info": {"channel_version": CHANNEL_VERSION}},
        bearer,
    )
    if "errcode" in resp:
        return False, "getupdates 失败: errcode %s %s" % (resp.get("errcode"), resp.get("errmsg", ""))
    if resp.get("get_updates_buf"):
        cache["get_updates_buf"] = resp["get_updates_buf"]
    msgs = resp.get("msgs") or []
    if not msgs:
        return False, "本轮无新消息（35 秒内手机未给 bot 发消息）。token 未变化。"
    m0 = msgs[0]
    cache["user_id"] = m0.get("from_user_id")
    cache["context_token"] = m0.get("context_token")
    save_cache(cache)
    return True, "已获取并缓存 context_token / user_id: %s" % cache.get("user_id")


def do_send(text):
    """用缓存的 context_token 主动发一条文本。返回 (ok, code, detail)。"""
    bearer = get_token_from_settings()
    cache = load_cache()
    user_id = cache.get("user_id")
    ctx = cache.get("context_token")
    if not user_id or not ctx:
        return False, "NO_TOKEN", "尚未获取 token：请先调用 acquire_token 工具，并在手机给 bot 发一条消息完成绑定，再执行推送。"
    msg = {
        "from_user_id": "",
        "to_user_id": user_id,
        "client_id": "push-" + os.urandom(8).hex(),
        "message_type": 2,
        "message_state": 2,
        "context_token": ctx,
        "item_list": [{"type": 1, "text_item": {"text": text}}],
    }
    body = {"msg": msg, "base_info": {"channel_version": CHANNEL_VERSION}}
    status, resp = ilink_post("/ilink/bot/sendmessage", body, bearer)

    # 健壮判断：HTTP 200 且无 errcode、ret 视为成功（iLink 常返回 ret=null 表示成功）
    if status == 200 and "errcode" not in resp and resp.get("ret") in (0, None):
        return True, "OK", "HTTP 200 | 发送成功"

    err = resp.get("errcode")
    if err == -14:
        return False, "TOKEN_EXPIRED", "token 已失效(errcode -14)：请重新调用 acquire_token 获取。"
    # 未知错误码也如实返回，便于排查
    if status == 200 and resp.get("ret") in (0, None):
        # 极少数情况带 errcode 但 ret 正常，仍视为成功
        return True, "OK", "HTTP 200 | 发送成功"
    return False, "SEND_FAIL", "HTTP %s | errcode %s | ret %s | %s" % (
        status, err, resp.get("ret"), resp.get("errmsg", ""))


# ------------------------- MCP 服务器（stdio）-------------------------
TOOLS = [
    {
        "name": "push_wechat_message",
        "description": (
            "向用户【个人微信】(ClawBot)主动推送一条文本消息。发送前自动验证 context_token："
            "已获取则直接推送；未获取或已失效则返回明确指引，提示先调用 acquire_token 并在手机给 bot 发消息。"
            "供自动化在定时/触发任务完成后调用，把结果推送到用户微信。"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "要推送到微信的文本内容"},
                "auto_acquire": {
                    "type": "boolean",
                    "description": "可选。token 缺失时是否自动尝试获取(会阻塞等待手机消息，默认 false)",
                },
            },
            "required": ["text"],
        },
    },
    {
        "name": "acquire_token",
        "description": (
            "获取/刷新 context_token（长轮询，约 35 秒内需用手机给 bot 发一条消息以完成绑定）。"
            "推送前若 bridge_status 显示未获取 token，应先调用本工具。"
        ),
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "bridge_status",
        "description": "返回推送桥当前状态：是否已缓存 context_token、目标用户微信id。供自动化推送前自检。",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def run_mcp():
    log("自托管推送桥 MCP 服务器启动（stdio）。")
    for raw_bytes in sys.stdin.buffer:
        raw = raw_bytes.decode("utf-8").strip()
        if not raw:
            continue
        try:
            msg = json.loads(raw)
        except Exception as e:
            log("JSON 解析失败: " + str(e))
            continue
        method = msg.get("method")
        mid = msg.get("id")
        params = msg.get("params") or {}

        if method == "initialize":
            send({
                "jsonrpc": "2.0",
                "id": mid,
                "result": {
                    "protocolVersion": params.get("protocolVersion", "2024-11-05"),
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "wechat-clawbot-push", "version": "self-hosted-1.0.0"},
                },
            })
        elif method == "notifications/initialized":
            continue
        elif method == "tools/list":
            send({"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}})
        elif method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments") or {}
            if name == "push_wechat_message":
                text = (arguments.get("text") or "").strip()
                auto_acquire = bool(arguments.get("auto_acquire", False))
                if not text:
                    send({"jsonrpc": "2.0", "id": mid, "result": {
                        "content": [{"type": "text", "text": "缺少 text 参数"}], "isError": True}})
                    continue
                cache = load_cache()
                if not (cache.get("context_token") and cache.get("user_id")):
                    if auto_acquire:
                        ok, detail = acquire_token_once()
                        if not ok:
                            send({"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": "token 缺失且自动获取失败：" + detail}], "isError": True}})
                            continue
                        log("auto_acquire 成功，继续推送。")
                    else:
                        send({"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": "尚未获取 token：请先调用 acquire_token 工具，并在手机给 bot 发一条消息完成绑定，再执行推送。"}], "isError": True}})
                        continue
                ok, code, detail = do_send(text)
                if not ok and code == "TOKEN_EXPIRED":
                    send({"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": detail + " 请调用 acquire_token 重新获取后再推送。"}], "isError": True}})
                    continue
                send({"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": detail}], "isError": not ok}})
            elif name == "acquire_token":
                ok, detail = acquire_token_once()
                send({"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": detail}], "isError": not ok}})
            elif name == "bridge_status":
                cache = load_cache()
                send({"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": json.dumps({
                    "has_context_token": bool(cache.get("context_token")),
                    "user_id": cache.get("user_id"),
                    "cache_path": CACHE_PATH,
                }, ensure_ascii=False)}], "isError": False}})
            else:
                send({"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": "未知工具: " + str(name)}], "isError": True}})
        else:
            if mid is not None:
                send({"jsonrpc": "2.0", "id": mid, "result": {}})


# ------------------------- 本地 CLI 调试 -------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mcp", action="store_true", help="以 stdio MCP 服务器模式运行（主用）")
    ap.add_argument("--acquire", action="store_true", help="本地获取 token（需手机给 bot 发消息）")
    ap.add_argument("--test", metavar="TEXT", help="本地手动推送一条（调试）")
    args = ap.parse_args()
    if args.mcp:
        run_mcp()
    elif args.acquire:
        ok, detail = acquire_token_once()
        print(("HTTP 成功 | " if ok else "[FAIL] ") + detail)
    elif args.test:
        ok, code, detail = do_send(args.test)
        print(detail)
        if ok:
            print("[OK] 已主动推送。请检查手机微信是否收到。")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
