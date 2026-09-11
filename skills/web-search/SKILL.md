---
name: web-search
description: 联网搜索（合并原 tavily 与 tencent-yuanbao-standard-search 两个同类技能）。需要检索互联网实时信息时使用：默认走腾讯元宝 WSA（国内直连、中文生态、支持时间范围 / 站点限定 / 天气金价股价汇率等垂类数据）；需要 AI 摘要答案、域名 include/exclude 过滤、news 时效检索、原始网页内容或图片时才用 Tavily 后端。触发词：联网搜索、搜一下、查最新、搜索互联网、最新消息、行情查询、web search、search the web、news lookup、fact-check。轻量单点查询优先用内置 WebSearch / WebFetch，不必启动本技能。
version: 1.0.0
agent_created: true
sources:
  - 合并自旧 skill `tencent-yuanbao-standard-search` v1.0.1（腾讯云 WSA 元宝搜索标准版）
  - 合并自旧 skill `tavily`（Tavily Search API，AI-optimized）
---

# web-search（联网搜索：两条后端）

**核心判断：先选后端，再发查询。** 两条后端能力互补，不要同时都调——同一问题只走一条，避免重复消耗额度与 token。

## 后端选择

| 需求 | 走哪条 |
|---|---|
| 中文内容 / 国内站点 / 时效性新闻 | **元宝 WSA**（默认，国内直连无需代理） |
| 垂类高时效数据：天气、金价、股价、汇率、油价、贵金属 | **元宝 WSA `--mode=2`**（混合模式，独家插件源） |
| 限定某站点内检索 | 元宝 `--site=` |
| 限定时间范围（近一天 / 一周 / 一月 / 一年） | 元宝 `--freshness=` |
| 要 AI 摘要答案（一次拿到综合结论） | **Tavily**（`--depth advanced` 默认带 answer） |
| 要按域名白名单 / 黑名单过滤（如只信 arxiv.org） | **Tavily** `--include-domains` / `--exclude-domains` |
| 要原始网页正文做深读 | **Tavily** `--raw-content` |
| 要图片结果 | **Tavily** `--images` |
| 单点事实、只是取一个页面 | 内置 `WebSearch` / `WebFetch`，不走本技能 |

**默认口径**：中文语境、国内站点、行情类 → 元宝；需要摘要化结论或精确控制来源 → Tavily。

## 后端 A：元宝 WSA（默认）

依赖环境变量 `TENCENTCLOUD_WSA_APIKEY`（腾讯云联网搜索 API 控制台开通并创建）。
**必须在 `scripts/` 同目录下执行。**

```bash
python3 scripts/websearch.py --query="搜索关键词"
python3 scripts/websearch.py --query="搜索关键词" --freshness='week'
python3 scripts/websearch.py --query="腾讯股价" --mode=2
python3 scripts/websearch.py --query="搜索关键词" --site="sogou.com"
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `--query` | 是 | 搜索关键词 |
| `--site` | 否 | 约束到指定站点，需严格域名格式 |
| `--mode` | 否 | 0 自然检索（默认）/ 1 多模态 VR（天气金价股价等）/ 2 混合 |
| `--freshness` | 否 | `day` / `week` / `month` / `year`，不传则不限定时间 |

输出为 markdown：标题、链接、摘要、发布时间、站点、相关图片。

常见报错：服务不可用 → 查腾讯云账户欠费；服务未开通 / 未授权 → 控制台开通并核对 API KEY 是否写入环境变量。

## 后端 B：Tavily

依赖 `pip install tavily-python` 与环境变量 `TAVILY_API_KEY`（`tvly-` 开头）。

```bash
python3 scripts/tavily_search.py "What is quantum computing?"
python3 scripts/tavily_search.py "复杂主题" --depth advanced
python3 scripts/tavily_search.py "最新进展" --topic news
python3 scripts/tavily_search.py "Python 教程" --include-domains python.org docs.python.org
python3 scripts/tavily_search.py "某主题" --raw-content --max-results 5
python3 scripts/tavily_search.py "视觉参考" --images
```

| 参数 | 说明 |
|---|---|
| `--depth` | `basic`（1–2s，默认）/ `advanced`（5–10s，研究级） |
| `--topic` | `general`（全时段）/ `news`（近 7 天） |
| `--include-domains` / `--exclude-domains` | 域名白 / 黑名单 |
| `--max-results` | 结果条数 |
| `--images` / `--raw-content` / `--no-answer` | 图片 / 原文 / 关闭 AI 摘要 |
| `--json` | JSON 输出，便于管道处理 |

完整参数与响应格式见 `references/tavily-api-reference.md`。

## 成本与质量

- **默认先用便宜档**：元宝不带 `mode`/`freshness`；Tavily 用 `basic`。结果不足再升级，不要一上来就 `advanced` 或 `mode=2`
- **只信一手来源**：把检索结果当线索，关键结论要能回到原始 URL 核对；不做二次演绎就当事实用
- **同一问题不双后端重复查**：两条都查＝额度与 token 双倍消耗，收益极低
- **结果先摘要再入上下文**：长结果只留与当前问题相关的要点（呼应 `wb-max-token-saver` 输入侧压缩）

## 反模式
- 明明内置 WebFetch 能取单个页面，却启动搜索后端
- 中文/行情类问题去用 Tavily（时区与语料错配），或需要域名过滤时硬用元宝
- 一次查询把 `mode=2` + `freshness=year` + `advanced` 全开 → 又慢又贵
- 搜到摘要直接当结论交付，不附来源链接

## 合并说明
原 `tavily` 与 `tencent-yuanbao-standard-search` 是同一功能位的两个重复技能（都是"用 API 联网搜索"），已合并为本技能的两条后端：**保留元宝的国内直连 / 垂类 / 时间与站点过滤，保留 Tavily 的 AI 答案 / 域名过滤 / 原文与图片**，两个旧目录已删除（git 历史可回溯）。
