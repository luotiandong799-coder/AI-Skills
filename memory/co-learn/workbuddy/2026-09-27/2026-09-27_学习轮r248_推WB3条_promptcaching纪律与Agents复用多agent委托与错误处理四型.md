# r248 批末 推 WB 3 条（2026-09-27）

## 三条（从 r248-A/B/C 精选）
1. **prompt caching 纪律**（r248-A，Anthropic）：自动缓存（顶层加单个 cache_control 字段，断点自动加到最后一个可缓存块并随对话前移）+ 显式断点（system prompt/tool list/长文档后放 cache_control ephemeral）；TTL 默认 5 分钟命中免费续期，1 小时 TTL 适合 agentic side-agent/长对话存档；读成本 0.1x base、写 1.25x/1h 2x；**响应里必须记录 cache_creation_input_tokens/cache_read_input_tokens 让静默 miss 变响亮日志**；前缀稳定纪律（稳定内容放前变化放后）；70-90% 账单削减。
2. **Agents 一次设随处用 + AI Agent Tool 多 agent 委托**（r248-B，n8n）：agent 设一次随处用（名字/指令/工具/skills 封装成可复用单元）；**workflow 即工具**——每个已建 workflow 都是 agent 可用的工具无需改；AI Agent Tool 委托（orchestrator 的工具之一是另一个 agent 委托子任务）；Max Iterations 设最长工具链+2；Return Intermediate Steps 显示 agent 决策细节=工具调用出问题第一反应。
3. **错误处理四型 + incomplete executions**（r248-C，Make）：Break 只停出错 bundle 存 incomplete execution 其他 bundle 继续（生产最有用）；Ignore 忽略错误继续下一个；Resume 用替代输出替换模块输出；Rollback 撤销先前模块；失败 run 保存 data+blueprint 可重跑防信息丢失；scenario recovery 自动保存 blueprint 恢复未保存更改+version history 60 天。
