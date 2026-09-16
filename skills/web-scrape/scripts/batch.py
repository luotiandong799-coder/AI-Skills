#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web-scrape 批量抓取：多 URL 顺序抓取，失败不中断，礼貌间隔，产出每页文件 + _report.md 汇总。

用法示例：
    python batch.py "https://a.com/" "https://b.com/" --out-dir ./out
    python batch.py --file urls.txt --out-dir ./out --delay 2
    python batch.py --file urls.txt --out-dir ./out --strategy descending --optimize
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRAPE = os.path.join(BASE_DIR, "scrape.py")

EXT = {"markdown": "md", "text": "txt", "html": "html", "json": "json"}


def _read_urls(args):
    urls = list(args.urls or [])
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)
    return urls


def _safe_name(url, index):
    import re as _re
    host = url.split("//")[-1].split("/")[0]
    name = _re.sub(r"[^\w\-.]+", "_", host)
    return f"{index:03d}_{name}"


def _run_one(url, args, out_dir):
    cmd = [sys.executable, SCRAPE, url,
           "--strategy", args.strategy,
           "--format", args.format]
    if args.tier:
        cmd += ["--tier", args.tier]
    if args.optimize:
        cmd.append("--optimize")
    if args.selector:
        cmd += ["--selector", args.selector]
    if args.fields:
        cmd += ["--fields", args.fields]
    if args.delay:
        cmd += ["--wait", str(args.delay)]
    if args.timeout:
        cmd += ["--timeout", str(args.timeout)]
    if args.no_cache:
        cmd.append("--no-cache")
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=args.timeout + 60)
        elapsed = round(time.time() - t0, 2)
        if proc.returncode == 0:
            body = proc.stdout
            meta = body.splitlines()[0] if body.startswith("# ok") else ""
            content = "\n".join(body.splitlines()[2:]) if meta else body
            ext = EXT.get(args.format, "md")
            fname = _safe_name(url, 0) + "." + ext
            path = os.path.join(out_dir, fname)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"url": url, "ok": True, "file": fname, "chars": len(content),
                    "elapsed": elapsed, "meta": meta, "err": ""}
        return {"url": url, "ok": False, "file": "", "chars": 0, "elapsed": elapsed,
                "meta": "", "err": (proc.stderr or proc.stdout)[-300:]}
    except Exception as e:
        return {"url": url, "ok": False, "file": "", "chars": 0,
                "elapsed": round(time.time() - t0, 2), "meta": "", "err": str(e)[-300:]}


def main():
    ap = argparse.ArgumentParser(prog="batch.py", description="批量网页抓取")
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--file", default=None, help="URL 列表文件（每行一个，# 注释）")
    ap.add_argument("--out-dir", default="./out")
    ap.add_argument("--delay", type=float, default=1.5, help="礼貌间隔秒数/页")
    ap.add_argument("--format", choices=["markdown", "text", "html"], default="markdown")
    ap.add_argument("--tier", choices=["easy", "medium", "hard"], default=None)
    ap.add_argument("--strategy", choices=["adaptive", "ascending", "descending"], default="adaptive")
    ap.add_argument("--optimize", action="store_true")
    ap.add_argument("--selector", default=None)
    ap.add_argument("--fields", default=None)
    ap.add_argument("--timeout", type=int, default=25)
    ap.add_argument("--no-cache", action="store_true")
    args = ap.parse_args()

    urls = _read_urls(args)
    if not urls:
        ap.error("需要 URL 或 --file")
    os.makedirs(args.out_dir, exist_ok=True)

    results = []
    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] {url}")
        res = _run_one(url, args, args.out_dir)
        results.append(res)
        status = "ok" if res["ok"] else "FAIL"
        print(f"  -> {status} | {res.get('meta','')} | {res['elapsed']}s"
              + (f" | {res['err']}" if not res["ok"] else ""))
        if i < len(urls) - 1 and args.delay > 0:
            time.sleep(args.delay)

    ok_n = sum(1 for r in results if r["ok"])
    lines = [
        f"# 批量抓取报告 | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 总数: {len(results)} | 成功: {ok_n} | 失败: {len(results)-ok_n}",
        "",
        "| # | URL | 状态 | 档位 | 字符数 | 耗时 | 文件 | 失败原因 |",
        "|---|-----|------|------|-------|------|------|---------|",
    ]
    for i, r in enumerate(results):
        tier = "?"
        m = r.get("meta", "")
        if "# ok" in m:
            tier = m.split("|")[1].replace("档位=", "").strip()
        lines.append(
            f"| {i+1} | {r['url']} | {'✅' if r['ok'] else '❌'} | {tier} | {r['chars']} | {r['elapsed']}s "
            f"| {r.get('file','')} | {r.get('err','')} |"
        )
    report = os.path.join(args.out_dir, "_report.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\n报告: {report}")
    return 0 if ok_n == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
