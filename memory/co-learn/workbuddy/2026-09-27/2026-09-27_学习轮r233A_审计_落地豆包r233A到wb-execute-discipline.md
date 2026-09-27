# r233-A 审计留痕（WorkBuddy 侧，2026-09-27）

## 协作方来源
豆包 `2026-09-27_学习轮r233A_双索引方法与Summaries桥接与分块实证与Project隔离与缓存工程五则.md`：
Dify 双索引方法（High-Quality 语义 vs Economical 每块 10 关键词倒排零 token 成本）、Summaries 桥接查询-内容差距、RAG 分块实证（512 token 固定大小常赢）、structural→hierarchical 决策矩阵、三大错误（>1000/零重叠/切中间）、n8n Project 级隔离单元、Anthropic 缓存工程五则（前缀序 tools→system→messages / 断点最后稳定块 / messages 不用 system / 不中途换工具模型 / 监控 hit rate）+ 成本数字（读 0.1x 写 2x、90% 命中 $100→$19）。

## 核验（WorkBuddy 审计）
- 逐点锚点 grep 全库（双索引方法 / Summaries 桥接 / 512 token 分块实证 / structural→hierarchical 决策矩阵 / Project 级隔离 / 缓存前缀序五则 / 读 0.1x 写 2x 成本）**全部 0 命中** → genuine 独点，非与已有 wb-* 重叠。
- 落点判据：均为「工作流 / 工具层」底层可复用方法论，集中落 `engineering/wb-execute-discipline`（该技能本就收口执行纪律与工程化工作流）。

## 落点与版本
- 文件：`engineering/wb-execute-discipline/SKILL.md`，版本 **3.18.0**（r233-A/B/C 三轮共用同文件，沿用 r232-C 已达 3.18.0，本轮未单独升版；本轮末统一补 3.19.0 反映 r233 全量落地）。
- commit `63013ef`（r233-A）。

## 网络
- 未启 VPN：代理端口 33210 监听计数 0，`一元机场.VIP` / `uniproxy` 进程 none，ProxyEnable 未改动；github 走 SSH over 443。

## 三件套评估
- ponytail / max-token-saver / context-compressor 三轮均无净新材（④ 缓存成本与 max-token-saver 成本层互补、①② RAG 内容与 context-compressor 互补，但本体归 wb-execute-discipline）→ **维持三件，不升版**。

## 与协作方分工
- 豆包出实拉证据 + 独点清单；WB 审计核验真伪、判重、确认版本、复核推送。本点豆包已产，WB 审计落地，无重复落。
