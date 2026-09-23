# 学习轮 r155 — GPT Store：登录壳 + persona 市场退场（WorkBuddy 审计）

- 日期：2026-09-23
- 轮号：r155（全局唯一，非按日重置）
- 信源：OpenAI GPT Store `https://chatgpt.com/gpts?utm_source=chatgpt.com`（清单内信源，用户提供正确 URL）
- 方式：直连超时（code=000）→ 代理 33210 返回 HTTP 200 / 468,578 bytes 落盘 `D:\腾讯AI\yt\r154wb\gpts\store.html`（551,290 B）；解析正文仅 `Explore GPTs ChatGPT Sign up for free` 三词＝未登录空壳。改走已登录 Edge Beta（账号 雒天栋 / 免费版）DOM 抓取，页面完整渲染。

## 实拉证据（已登录 DOM 原文）
1. 停运公告：`GPT 将于 12月11日停用` / `如需继续使用你的 GPT，请在 12月11日 前将其迁移为插件。`
2. 8 个分类 tab：精选推荐 / 图像 / 编程 / 工作效率 / 研究与分析 / 写作 / 教育 / 生活方式
3. 双榜分离：
   - 热门 / 社区中最受欢迎的 GPT（带 1..6 序号，创建者域名）：Scholar GPT(awesomegpts.ai) / Fitness PhD Coach(Newgen PhD, v3.27) / Consensus(consensus.app) / 챗GPT 한국어(gptonline.ai) / Canva(community builder) / Logo Creator(community builder)
   - 由 ChatGPT 提供 / ChatGPT 团队创建的 GPT（创建者均为 ChatGPT）：Monday / Data Analyst / Hot Mods / Creative Writing Coach / Coloring Book Hero / Planty
4. 搜索入口「搜索 GPT」Ctrl+K；卡片结构＝排名序号 + 名称 + 一句话能力描述 + 创建者域名
5. 描述含可量化能力声明：`200M+ resources`、`Trained on 232,625 PhD-level empirical data points`；版本号写进展示名 `v3.27`

## 独点判定（对照现有 wb-* 技能）
| 独点 | 落点 | 非重复理由 |
|---|---|---|
| HTTP 200 + 大体积 ≠ 内容到手；落盘前做正文词数非空检测；登录墙升级到已登录 DOM | `wb-context-compressor` 3.49.0→3.50.0 | 现有 §工具输出沙箱只管「多大、怎么落盘」，不管「落盘的是不是空壳」；与本轮刚犯的「把 403 当站点未达」同族，补硬判据 |
| persona 市场→插件方向判据；优先接可机读注册表，不学纯 UI 信源 | `wb-skill-authoring` 2.70.0→2.71.0 | 现有 §发布侧治理管「我方发布」，无「引入外部市场先看它会不会被关、可不可机读」的方向取舍 |
| 双榜分离：社区热度榜 vs 官方自研榜，互不挤占 | `wb-skill-authoring` 同一次 | 现有合并判据管「技能间去重」，无「目录榜单分类」设计 |
| 反例（不做）：版本号不塞 description；创建者域名标注、匿名统一标签 | `wb-skill-authoring` 同一次 | 我方 description 三条机检纪律 + `_skillhub_meta.json` 来源标注已定，market 做法是反例 |

- 三件套评估：本轮无新触发（ponytail/max-token-saver/context-compressor 中 cc 迭代，pt/mts 不动）
- 落点回避：未动 `wb-execute-discipline`（豆包主战场），独点5 改落 `wb-context-compressor`（WB 辖区）
- 落地 2 文件 / 4 独点；live↔repo sha256 一致；description 长度 781 / 935 均 ≤1024
