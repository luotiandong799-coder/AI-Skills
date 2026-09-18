---
name: web-scrape
description: 抓取网页并输出干净的 Markdown、纯文本、HTML 或结构化 JSON。当用户要读取、抓取、整理某个网站或 AI Agent 站点的内容，需要批量采集公开网页数据、提取列表页字段，或要求"把某个网页/网站抓下来"时使用。不适用于需要登录、付费墙后的内容。
---

# 网页抓取

把网页变成干净的 Markdown / 文本 / HTML / 结构化字段，供阅读、摘要、入库。

## 一、输出格式（`--format`）

| 格式 | 用途 |
|---|---|
| `markdown` **默认** | 正文 Markdown，喂模型、入库、阅读 |
| `text` | 纯文本，只要文字不要标记 |
| `html` | 原始 HTML，自己解析时用 |

## 二、三档难度（`--tier`）

| 档位 | 典型特征 | 引擎链 | 速度 |
|---|---|---|---|
| `easy` | 静态 HTML、文档站、博客 | scrapling/fast → simple | 秒级 |
| `medium` | JS 渲染、无限滚动、异步加载 | scrapling/dynamic → crawl4ai | 十秒级 |
| `hard` | Cloudflare、403、指纹检测 | scrapling/stealth → crawl4ai | 慢 |

## 三、三种策略（`--strategy`）

| 策略 | 行为 | 适合 |
|---|---|---|
| `adaptive` **默认** | 查难度记忆 → 无记录则**预检一次** → 直接挑档 | 绝大多数 |
| `ascending` | easy → hard，失败才升级 | 站点简单、想最省 |
| `descending` | hard → easy，从重手段开始 | **必须拿到**、不想来回试 |

```
python scripts/scrape.py "URL" # adaptive
python scripts/scrape.py "URL" --strategy descending # 从高到低
python scripts/scrape.py "URL" --strategy descending --optimize
```

### adaptive 的预检

发一个请求（只读前 32KB），看信号直接跳档：

| 信号 | 判定 |
|---|---|
| 403/429/503、`cf-ray` 头、"Just a moment" | → `hard` |
| `<div id="app"></div>`、`__nuxt`、`__next_data__` | → `medium` |
| 源码正文 ≥250 字符 | → `easy` |
| 判不出来 | 退回 ascending 逐级 |

成本约一次 HTTP 请求，远低于「逐级试错三次」。

### `--optimize`：成功后自动往轻档收敛

先用重手段拿到 → 反向试更轻档位 → **可行就改用并更新记忆**。长期自动收敛到最省。
轻档内容不足时自动保留重档结果，不影响正确性。代价是多一次请求。

## 四、结构化提取（`--fields`）

抓列表页、目录页时用，直接出 JSON：

```
python scripts/scrape.py "URL" \
--selector "li.item" \
--fields "name=h2,url=a::attr(href),desc=.desc"
```

```json
[{"name": "Cursor", "url": "https://cursor.com/", "desc": "AI 编程编辑器"}, ...]
```

- `--selector` 指定**列表容器**，每个匹配元素产出一条记录
- 字段语法：`名称=CSS选择器`，属性用 `a::attr(href)`，文本用 `h2` 或 `h2::text`
- 复用难度策略拿 HTML，因此 **JS 渲染页同样有效**
- 零 LLM 成本（纯 CSS 提取）；Crawl4AI 的 LLM 抽取要 $0.01–0.03/页，能用 CSS 就别上

## 五、批量抓取

```
python scripts/batch.py "https://a.com/" "https://b.com/" --out-dir ./out
python scripts/batch.py --file urls.txt --out-dir ./out --delay 2
python scripts/batch.py --file urls.txt --out-dir ./out --strategy descending --optimize
```

产出：每个页面一个文件（扩展名随 `--format` 变）+ `_report.md` 汇总（成功/失败、字符数、引擎、档位、耗时、失败原因）。

特性：失败不中断、礼貌间隔（默认 1.5s/页）、auto 档自动升档、支持 `--format`。

## 六、安装（有坑，按顺序来）

```
Scrapling（默认引擎，必装）
pip install scrapling curl_cffi browserforge msgspec playwright patchright
scrapling install # 浏览器，medium/hard 档需要

Crawl4AI（可选：整站爬取、最高质量 Markdown）
pip install -U crawl4ai && crawl4ai-setup && crawl4ai-doctor
```

⚠️ **四个实测踩过的坑**：

1. **只装 `pip install scrapling` 依赖不全** —— 即使只用静态模式也会连带要一堆包，而且是**层层暴露**：`curl_cffi` → `browserforge` → `msgspec` → `playwright` → `patchright`。报错只提示当前缺的那个，**必须一次补齐**。
2. **不要装 `scrapling[all]`** —— 实测会把 0.4.15 **降级到 0.2.99**。
3. **`stealth` 模式额外需要 camoufox** —— `pip install camoufox && camoufox fetch`。
4. **包可能莫名消失** —— 多轮 pip 装依赖时实测遇到过 scrapling 被卸载。症状：突然报 `No module named 'scrapling'`，且日志显示最终用了 `simple` 引擎。重装即可。

浏览器实在装不上也能用：脚本自动降级到无浏览器的 `simple` 模式，**静态页照样抓**。

## 七、执行流程

1. **确认能抓**：检查 `robots.txt`，确认公开页面，不抓登录/付费墙内容。
2. **直接跑 adaptive**：`python scripts/scrape.py "<url>"`
3. **检查结果**：
   - 内容空/缺正文 → `--tier medium` 或 `--wait 3`
   - 报 403 → `--tier hard`
   - 混着广告 → `--selector "article"`
   - 要列表数据 → `--selector` + `--fields`
4. **批量时**：`--delay` 至少 1.5 秒，别并发开太猛。

## 八、抓不动了怎么办

按顺序试，别一上来就上最重的手段：

1. `--tier medium` / `--tier hard`
2. `--wait 3` 等 JS 加载完
3. `--proxy http://host:port` 换出口 IP
4. `--cookie "session=xxx"`（**仅限你有权访问的页面**）
5. `--selector ".content"`
6. 仍失败 → 对方防护强，**停止尝试**，换来源或用官方 API

### 403 误拦诊断（来源：GitHub `lobuhi/byp4xx` 方法论合规子集，2026-09-16 实拉）

报 403 先别急着换档/换 IP——先判断是**误拦**还是**真拒绝**：

- **仅限自己有权访问的页面**。先自问：这个页面我本来有权访问吗？没有 → 停止，这是访问控制，不是抓取问题。
- 有权访问 → 用 URL 规范化变体排除 WAF/CDN 误拦（一次只改一个变量，避免混淆成因）：
  1. 尾部斜杠：`/path` ↔ `/path/`
  2. 大小写变体：`/Path` / `/PATH`
  3. 路径编码：`%2e`、`%2f`、`..;`
- 仍 403 → 才走 `--tier hard` / `--proxy`（换出口 IP 验证是否为 IP 级误拦）。
- **禁止**：默认凭据尝试、`X-Custom-IP-Authorization` / `X-Forwarded-For` 伪造来源头等**突破访问控制**手段——与「十一、合规红线」冲突，一律不用。

## 九、站点难度记忆

探测结果按域名记在 `scripts/.tier-cache.json`（已归一化：去 www、去端口、小写）。
下次同站点直接跳档，不做无谓试探。

```
python scripts/scrape.py --show-cache # 看各站用什么档
python scripts/scrape.py --clear-cache # 清空（站点改版后清一次）
python scripts/scrape.py "URL" --no-cache # 本次忽略记忆
```

已知某站难搞时，首次就 `--tier hard`，直接记档跳过探测。

## 十、MCP 接入（让 Agent 自己会爬）

配好后直接说「把这个网站抓下来」。两个引擎都自带 MCP server：

**Scrapling**

```json
{"mcpServers": {"scrapling": {"command": "python", "args": ["-m", "scrapling.mcp_server"]}}}
```

**Crawl4AI**

```json
{"mcpServers": {"crawl4ai": {"command": "python", "args": ["-m", "crawl4ai.mcp"]}}}
```

**MCP 适合交互式探索，脚本适合批量与可复现任务** —— 难度档位控制、难度记忆、批量报告只有脚本有，MCP 没有。两者可同时配。

## 十一、合规红线（不可跳过）

- **先看 `robots.txt`**，被明确禁止的路径不抓。
- **控制频率**：单站点 1–3 秒一页，不要高并发把对方拖垮。
- **不抓付费墙、登录后内容**，不用于绕过学术数据库访问限制。
- **不抓个人隐私数据**。
- 反爬绕过只用于**自己有权访问的公开页面**的技术兼容，不是用来突破访问控制的。

## 十二、常见失败与处理

| 现象 | 原因 | 处理 |
|---|---|---|
| 内容为空/只有导航 | JS 渲染 | `--tier medium` + `--wait 3` |
| 403 / "Just a moment" | 反爬拦截 | 先走「八、403 误拦诊断」（限自己有权访问的页），再 `--tier hard` 或 `--proxy` |
| 超时 | 页面太重 | 加大 `--timeout` |
| Markdown 混着广告 | 正文提取失败 | `--selector "article"` |
| `Executable doesn't exist` | 浏览器未装 | `scrapling install`（不装也能抓静态页） |
| `No module named 'xxx'` | 依赖缺失 | 按第六节安装命令补齐 |
| `--fields` 没匹配到 | 选择器错误 | 先用 `--format html` 看真实结构 |
| 引擎标签带 `(short)` | 内容短于阈值 | 见下 |

### 关于 `(short)` 标记

列表页、卡片页、目录页**内容天然短**。若所有档位都拿到了内容只是短于阈值，脚本会返回最长结果并在引擎标签后加 `(short)`，而不是直接报错。

看到 `(short)` 时：
- 内容本身是对的 → 忽略，或调低 `--min-length`
- 内容确实残缺 → 换 `--selector` 或升档重试

完全拿不到任何内容（各档位都异常）才会真正报错。
