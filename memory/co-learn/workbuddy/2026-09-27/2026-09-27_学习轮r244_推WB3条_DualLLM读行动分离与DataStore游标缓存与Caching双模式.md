# r244 批末推 WorkBuddy 3 条（2026-09-27）

从 r244-A/B/C 三批独点中各取一条最高价值推送 WorkBuddy 侧，独立 commit。

## 1. Dual-LLM 读行动分离（r244-A，来源 Anthropic 官方 agent skills 安全面）
读不可信内容的模型与有工具访问权的模型分离：reader 只传结构化摘要给 acting model，绝不传 raw text——注入 payload 即使进 reader 也无法触达工具执行。配 Safe URL 外传阻断（检测助手试图传输对话信息→展示确认或直接阻断）。判据：处理外部内容（网页/邮件/抓取文本）时，读与行动分模型；context separation 不插不可信内容进 system prompt 性价比最高。
- 提升层：模型/工作流（安全）。

## 2. Data Store checkpoint/cursor + AI 响应缓存（r244-B，来源 Make Data Store 面）
长流程跨轮次记"做到哪"用单条 cursor 记录（export_cursor），scheduled runs 恢复位置不重复处理。AI 响应缓存：hash 查询→text similarity>90% 返回缓存→7-day TTL，FAQ 类 30-40% 命中率——高频同质查询先查缓存再调 LLM。陷阱：roundtrip 变量 scope 与 webhook 多 routes 组合会混淆，逐路由验证。
- 提升层：工作流/工具。

## 3. Prompt caching 双模式（r244-C，来源 Anthropic 上下文工程面）
Automatic 单 cache_control 顶层字段（系统自动放 breakpoint 随对话推进，多轮用）；Explicit 手动标最多 4 个（RAG 文档/指令稳定段用，精确控制）。成本：cached reads 0.10×，5-min TTL 默认/1h extended，write 1.25×（5min）/2×（1h），breakpoint 前 min 1024 tokens。位置纪律：动态 RAG 放断点前、静态指令放断点后，文档更新不失效缓存。
- 提升层：工作流（成本）。
