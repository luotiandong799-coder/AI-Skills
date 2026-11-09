---
name: ci-context
description: 上下文工程与预算（Context Intelligence）。当任务涉及长上下文压缩、token 预算与窗口退化、提示缓存（prompt caching）命中率、多 agent 上下文隔离与缓存税、把必须每次成立的约束放进确定性 hook 而非 advisory context、以及"上下文够不够/会不会静默丢规则"的判断时使用。是 13 模块中 CI 的载体。
version: 1.1.0
module: CI
modules: CI
---

# CI · 上下文工程与预算（Context Intelligence）

> 本技能是 13 模块中 **CI（上下文智能）** 的载体。完整经验日志在 D 盘：`D:\腾讯AI\WorkBuddy数据\module-memory\CI\MEMORY.md`。关联子技能（长期默认运行）：`defaults/wb-context-compressor`、`defaults/wb-max-token-saver`、`defaults/wb-ponytail`。

## 一、核心认知

- 有效上下文窗口是任务复杂度的函数，非标称容量：检索类可扛几千 token，排序 / 摘要类 400–1200 即崩；退化静默无报错（实测 ~40% fill 开始跳过旧规则）⇒ 预算须显式告警、按最重操作测窗口。
- 规则上限按条数不按行数：~200 条 ceiling（system prompt 已占 ~50），超出后遵守率约 70% 且与文件长度无关；**必须每次成立的约束放确定性 hook 而非 advisory context file**；规则增退役成对。

## 二、触发与协作

- 何时加载：长上下文任务开工前估预算；调 prompt caching 命中率异常时；要不要把某规则改成 hook 时；多 agent 并发设计缓存策略时。
- 与 EI（执行）：预算约束影响计划拆解粒度；与 OI（编排）：缓存税是 agent 调度成本项。

## 三、窗口退化与规则上限方法论（实拉 r710A，2026-11-08）

> 来源：`dotex.org/epic/meta-programming/context-engineering` 一手 WebFetch；arXiv 2602.11988 经 dotex 回读原文（p=.87 / +20% cost）。

- **（r710A-1）窗口是任务复杂度的函数**：检索类可扛几千 token，排序 / 摘要类 400–1200 即崩；退化**静默无报错**（实测 40% fill 开始跳过旧规则）。⇒ 预算须显式告警，且按"最重操作"测窗口，不能只看平均。
- **（r710A-2）规则上限按条数不按行数**：~200 条 ceiling（system prompt 已占 ~50），超出后遵守率约 70% 且与文件长度无关。⇒ 必须每次成立的约束放**确定性 hook**而非 advisory context file；规则增 / 退役**成对**进行，避免 orphan。
- **（r710A-3）多 agent 隔离自带 cache tax**：14 子代理 700K cache_create / 0 cache_read，TTL 5 分钟、缓存键含 model id。⇒ 并发须贴近 TTL 窗口、顺序管线共享上下文落成文件、换模型即缓存清零。

## 四、提示缓存方法论（实拉 r715B，2026-11-08）

> 来源：OpenAI 官方 `platform.openai.com/docs/guides/prompt-caching`（Cloudflare 拦，3 独立域交叉补足）+ aiwiki 厂商表；intuitionlabs 2026-09 五家定价表；落地 `defaults/wb-max-token-saver/references/knowledge-base.md` §r715B-1/2/3 → 1.102.0。

- **（r715B-1）缓存键 = 渲染后的完整前缀**：不是用户可见提示词。隐藏 system 指令、tools 定义与顺序、`parallel_tool_calls`、`text.format` schema、`reasoning.effort`、`context_management` 压缩都参与匹配，任一变化自断点后失配。⇒ 排查 miss 先查**不可见渲染层**。
- **（r715B-2）最小可缓存长度按模型档位分裂**：GPT-5.6+ 1024 / 更老 2048，隐藏 system 内容不计入门槛，命中按 128-token 增量。⇒ "请求总长够" ≠ "可缓存前缀够"——整体超阈值但稳定前缀不足仍 `cached_tokens=0`；同一应用跨型号升级会静默改变可缓存性，参数族须标型号与日期。
- **（r715B-3）缓存是三档计费不是开关**：写 1.25x / 读 0.1x / 未读未写原价，一写一读 1.35x vs 2x、一写九读 2.15x vs 10x；每请求最多 4 写断点、读回溯最近 50 断点取最长匹配、TTL 30m 从写入或复用起算且刷新不另收费。`cache_write_tokens` 高而 `cached_tokens` 低 = 断点前混入变化内容的可机检信号。

## 五、来源（2026-11-08 实拉）

- dotex.org/epic/meta-programming/context-engineering（窗口退化 / 规则上限）
- arXiv 2602.11988（规则上限 ~200 条 ceiling，回读原文）
- OpenAI 官方 prompt-caching 文档 + aiwiki 厂商对照表（缓存键 / 档位 / 三档计费）
- intuitionlabs 2026-09 五家定价表
- 落地：`defaults/wb-max-token-saver/references/knowledge-base.md` §r715B-1/2/3
