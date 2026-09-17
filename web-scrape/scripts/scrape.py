#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web-scrape: 抓取网页并输出干净的 Markdown / 文本 / HTML / 结构化 JSON。
实现 SKILL.md 规格：三档难度引擎链、adaptive 预检、三种策略、站点难度记忆、--optimize 收敛、--fields 结构化提取。

用法示例：
    python scrape.py "https://example.com/"
    python scrape.py "URL" --strategy descending --optimize
    python scrape.py "URL" --selector "li.item" --fields "name=h2,url=a::attr(href),desc=.desc"
    python scrape.py --show-cache | --clear-cache
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
from html import unescape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(BASE_DIR, ".tier-cache.json")

MIN_LENGTH_DEFAULT = 200
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

# ---------- 依赖尽力导入 ----------
try:
    import requests
except ImportError:
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    import html2text
except ImportError:
    html2text = None

try:
    from scrapling import Fetcher, StealthyFetcher
    SCRAPLING_OK = True
except Exception:
    SCRAPLING_OK = False


# ---------- 站点难度记忆 ----------
def _normalize_domain(url):
    try:
        host = urllib.parse.urlparse(url).netloc.lower()
    except Exception:
        host = url.lower()
    host = host.split("@")[-1]
    host = re.sub(r":\d+$", "", host)
    if host.startswith("www."):
        host = host[4:]
    return host


def _load_cache():
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_cache(cache):
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"# 缓存写入失败: {e}", file=sys.stderr)


def _show_cache():
    cache = _load_cache()
    if not cache:
        print("# 站点难度记忆为空")
        return
    for domain, tier in sorted(cache.items()):
        print(f"{domain}\t{tier}")


def _clear_cache():
    if os.path.exists(CACHE_PATH):
        os.remove(CACHE_PATH)
        print("# 站点难度记忆已清空")
    else:
        print("# 缓存本就为空")


# ---------- robots.txt 合规检查 ----------
def _robots_check(url, session, proxies, timeout):
    """按 User-Agent 分组解析 robots.txt；仅匹配当前爬虫的组生效。返回 (allowed, reason)。"""
    try:
        parsed = urllib.parse.urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        r = session.get(robots_url, timeout=timeout, proxies=proxies, headers={"User-Agent": UA})
        if r.status_code >= 400:
            return True, "no robots.txt"
        text = r.text
        # 当前爬虫 UA 关键词（小写）
        my_ua = UA.lower()
        allowed = True
        cur_ua = None          # 当前组匹配的 UA 串（小写）
        cur_applies = False    # 当前组是否适用于本爬虫
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            low = line.lower()
            if low.startswith("user-agent:"):
                cur_ua = line.split(":", 1)[1].strip().lower()
                cur_applies = (cur_ua == "*") or (cur_ua in my_ua) or (
                    cur_ua and cur_ua in my_ua.split("/")[0])
                continue
            if low.startswith("disallow:") and cur_applies:
                path = line.split(":", 1)[1].strip()
                if path and (parsed.path.startswith(path) or path == "/"):
                    allowed = False
        return allowed, "robots.txt"
    except Exception as e:
        return True, f"robots.txt 检查失败({e})，默认放行"


# ---------- 预检 ----------
def _precheck(url, session, proxies, timeout):
    """读前 32KB 判断档位: hard / medium / easy / None(判不出)"""
    try:
        headers = {"User-Agent": UA, "Range": "bytes=0-32767"}
        r = session.get(url, timeout=timeout, proxies=proxies, headers=headers,
                        allow_redirects=True)
        head = (r.headers.get("server") or "").lower()
        body = ""
        try:
            body = r.text[:32768]
        except Exception:
            body = (r.content or b"")[:32768].decode("utf-8", "ignore")
        status = r.status_code
        if status in (403, 429, 503) or "cf-ray" in head or "just a moment" in body.lower()[:2000]:
            return "hard"
        if ('<div id="app"></div>' in body or "__nuxt" in body or "__next_data__" in body
                or '<div id="root"></div>' in body):
            return "medium"
        text_len = len(re.sub(r"<[^>]+>", "", body))
        if text_len >= 250:
            return "easy"
        return None
    except Exception:
        return None


# ---------- 抓取引擎 ----------
def _fetch_simple(url, session, proxies, timeout, wait):
    if requests is None:
        raise RuntimeError("requests 未安装")
    if wait:
        time.sleep(wait)
    r = session.get(url, timeout=timeout, proxies=proxies)
    r.raise_for_status()
    return r.text


def _fetch_dynamic(url, timeout, wait):
    if not SCRAPLING_OK:
        raise RuntimeError("scrapling 未安装，无法 dynamic")
    if wait:
        time.sleep(wait)
    resp = Fetcher.get(url, timeout=timeout)
    return resp.html_content


def _fetch_stealth(url, timeout, wait):
    if not SCRAPLING_OK:
        raise RuntimeError("scrapling 未安装，无法 stealth")
    if wait:
        time.sleep(wait)
    resp = StealthyFetcher.get(url, timeout=timeout)
    return resp.html_content


def _fetch_by_tier(tier, url, session, proxies, timeout, wait):
    if tier == "easy":
        return _fetch_simple(url, session, proxies, timeout, wait)
    if tier == "medium":
        try:
            return _fetch_dynamic(url, timeout, wait)
        except Exception:
            return _fetch_simple(url, session, proxies, timeout, wait)
    if tier == "hard":
        try:
            return _fetch_stealth(url, timeout, wait)
        except Exception:
            try:
                return _fetch_dynamic(url, timeout, wait)
            except Exception:
                return _fetch_simple(url, session, proxies, timeout, wait)
    raise ValueError(f"未知档位: {tier}")


TIER_ORDER = ["easy", "medium", "hard"]


# ---------- 正文提取与格式化 ----------
def _strip_html(html, selector=None):
    if BeautifulSoup is None:
        raise RuntimeError("beautifulsoup4 未安装")
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "template", "svg", "nav", "footer", "header", "aside", "form", "iframe"]):
        tag.decompose()
    if selector:
        node = soup.select_one(selector)
        if node:
            return node
    return soup


def _to_markdown(html, selector=None):
    node = _strip_html(html, selector)
    if html2text is not None:
        h = html2text.HTML2Text()
        h.body_width = 0
        h.ignore_links = False
        h.ignore_images = True
        return h.handle(str(node)).strip()
    # 内置简易转换
    text = node.get_text("\n")
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.splitlines()]
    return "\n".join([ln for ln in lines if ln])


def _to_text(html, selector=None):
    node = _strip_html(html, selector)
    text = node.get_text("\n")
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.splitlines()]
    return "\n".join([ln for ln in lines if ln])


def _extract_fields(html, selector, fields_spec):
    if BeautifulSoup is None:
        raise RuntimeError("beautifulsoup4 未安装")
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "html.parser")
    containers = soup.select(selector) if selector else [soup]
    specs = []
    for item in fields_spec.split(","):
        item = item.strip()
        if "=" not in item:
            continue
        name, sel = item.split("=", 1)
        specs.append((name.strip(), sel.strip()))
    records = []
    for c in containers:
        rec = {}
        for name, sel in specs:
            node = c.select_one(sel.split("::")[0])
            if "::attr(" in sel:
                attr = sel.split("::attr(")[1].rstrip(")")
                rec[name] = node.get(attr, "").strip() if node else ""
            else:
                rec[name] = unescape(node.get_text(" ", strip=True)) if node else ""
        if any(v for v in rec.values()):
            records.append(rec)
    return records


# ---------- 主流程 ----------
def run_scrape(url, fmt="markdown", tier=None, strategy="adaptive", optimize=False,
               selector=None, fields=None, wait=0, timeout=25, proxy=None, cookie=None,
               min_length=MIN_LENGTH_DEFAULT, no_cache=False, robots=True, session=None):
    if requests is None:
        raise RuntimeError("requests 未安装：pip install requests beautifulsoup4 lxml html2text")
    s = session or requests.Session()
    headers = {"User-Agent": UA}
    if cookie:
        headers["Cookie"] = cookie
    s.headers.update(headers)
    proxies = {"http": proxy, "https": proxy} if proxy else None

    if robots:
        allowed, reason = _robots_check(url, s, proxies, timeout)
        if not allowed:
            return {
                "ok": False, "error": f"robots.txt 禁止抓取该路径（{reason}）。合规红线：不抓被明确禁止的页面，请换来源或官方 API。",
                "url": url, "tier": None, "engine": "blocked", "chars": 0, "elapsed": 0.0, "short": False,
            }

    domain = _normalize_domain(url)
    cache = {} if no_cache else _load_cache()

    if tier is None:
        if strategy == "adaptive":
            tier = cache.get(domain)
            if tier is None:
                tier = _precheck(url, s, proxies, timeout)
                if tier is None:
                    order = TIER_ORDER
                else:
                    order = [tier] + [t for t in TIER_ORDER if t != tier]
            else:
                order = [tier] + [t for t in TIER_ORDER if t != tier]
        elif strategy == "ascending":
            order = TIER_ORDER
        elif strategy == "descending":
            order = list(reversed(TIER_ORDER))
        else:
            raise ValueError(f"未知策略: {strategy}")
    else:
        order = [tier] + [t for t in TIER_ORDER if t != tier]

    best = None
    t0 = time.time()
    for t in order:
        try:
            html = _fetch_by_tier(t, url, s, proxies, timeout, wait)
        except Exception as e:
            print(f"# [{t}] 失败: {e}", file=sys.stderr)
            continue
        # 内容质量判断
        if fields:
            recs = _extract_fields(html, selector, fields)
            ok = bool(recs)
        else:
            md = _to_markdown(html, selector)
            ok = len(md.strip()) >= min_length
        if ok:
            best = {"tier": t, "html": html, "short": False}
            break
        # 拿到内容但偏短 → 记录候选
        if best is None and not fields:
            md = _to_markdown(html, selector)
            if md.strip():
                best = {"tier": t, "html": html, "short": True}
        if best is None and fields:
            recs = _extract_fields(html, selector, fields)
            if recs:
                best = {"tier": t, "html": html, "short": True}

    if best is None:
        return {
            "ok": False, "error": "各档位均未拿到可用内容（防护过强或页面为空），停止尝试，换来源或官方 API。",
            "url": url, "tier": None, "engine": "failed", "chars": 0,
            "elapsed": round(time.time() - t0, 2), "short": False,
        }

    tier_used = best["tier"]
    html = best["html"]
    short = best["short"]

    # --optimize: 成功后反向试更轻档位，可行则收敛
    if optimize and tier_used != TIER_ORDER[0]:
        lighter = TIER_ORDER[:TIER_ORDER.index(tier_used)]
        for lt in reversed(lighter):
            try:
                html_l = _fetch_by_tier(lt, url, s, proxies, timeout, wait)
                if fields:
                    if _extract_fields(html_l, selector, fields):
                        html, tier_used = html_l, lt
                        short = False
                        break
                else:
                    if len(_to_markdown(html_l, selector).strip()) >= min_length:
                        html, tier_used = html_l, lt
                        short = False
                        break
            except Exception:
                continue

    # 更新站点记忆
    if not no_cache:
        cache[domain] = tier_used
        _save_cache(cache)

    if fields:
        records = _extract_fields(html, selector, fields)
        content = json.dumps(records, ensure_ascii=False, indent=2)
        out_fmt = "json"
    elif fmt == "html":
        content = html
        out_fmt = "html"
    elif fmt == "text":
        content = _to_text(html, selector)
        out_fmt = "text"
    else:
        content = _to_markdown(html, selector)
        out_fmt = "markdown"

    return {
        "ok": True, "url": url, "tier": tier_used, "engine": "scrapling/simple",
        "chars": len(content), "elapsed": round(time.time() - t0, 2),
        "short": short, "format": out_fmt, "content": content,
        "cache_domain": domain,
    }


def main():
    ap = argparse.ArgumentParser(prog="scrape.py", description="网页抓取：Markdown/文本/HTML/结构化 JSON")
    ap.add_argument("url", nargs="?", help="目标 URL")
    ap.add_argument("--format", choices=["markdown", "text", "html"], default="markdown")
    ap.add_argument("--tier", choices=["easy", "medium", "hard"], default=None)
    ap.add_argument("--strategy", choices=["adaptive", "ascending", "descending"], default="adaptive")
    ap.add_argument("--optimize", action="store_true", help="成功后自动往轻档收敛")
    ap.add_argument("--selector", default=None)
    ap.add_argument("--fields", default=None)
    ap.add_argument("--wait", type=float, default=0)
    ap.add_argument("--timeout", type=int, default=25)
    ap.add_argument("--proxy", default=None)
    ap.add_argument("--cookie", default=None)
    ap.add_argument("--min-length", type=int, default=MIN_LENGTH_DEFAULT)
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--no-robots-check", action="store_true", help="跳过 robots.txt 检查（仅用于你有权访问的页面）")
    ap.add_argument("--show-cache", action="store_true")
    ap.add_argument("--clear-cache", action="store_true")
    args = ap.parse_args()

    if args.show_cache:
        _show_cache()
        return 0
    if args.clear_cache:
        _clear_cache()
        return 0
    if not args.url:
        ap.error("需要 URL")

    result = run_scrape(
        args.url, fmt=args.format, tier=args.tier, strategy=args.strategy,
        optimize=args.optimize, selector=args.selector, fields=args.fields,
        wait=args.wait, timeout=args.timeout, proxy=args.proxy, cookie=args.cookie,
        min_length=args.min_length, no_cache=args.no_cache, robots=not args.no_robots_check,
    )

    if not result["ok"]:
        print(f"✗ 抓取失败: {result['error']}")
        return 1

    tag = result["tier"] + ("(short)" if result["short"] else "")
    print(f"# ok | 档位={tag} | 字符数={result['chars']} | 耗时={result['elapsed']}s | 域名记忆={result['cache_domain']}")
    if result["format"] != "json":
        print("---")
    sys.stdout.write(result["content"])
    if not result["content"].endswith("\n"):
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
