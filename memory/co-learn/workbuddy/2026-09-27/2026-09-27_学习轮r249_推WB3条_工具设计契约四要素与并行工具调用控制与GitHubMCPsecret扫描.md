# r249 批末推 WB 3 条（2026-09-27）

## 推送内容（从 r249 三批 15 独点中选 3 个最高价值）
| # | 独点 | 来源轮 | 提升层 | 核心 |
|---|---|---|---|---|
| 1 | 工具设计契约四要素与窄工具优于宽包装 | r249-B | 工具/可复用 Skill | 每个工具过 intern test（人类只看文档能否调用）；窄工具（get_invoice_by_id）优于宽 SQL 包装；契约四要素 clear name/explicit parameters/return format/error conditions；namespacing 前缀分组；agent 工具最小权限+approval gates+监控每次调用 |
| 2 | 并行工具调用控制 | r249-C | 工具/工作流 | disable_parallel_tool_use 语义（auto 限一个工具；computer use 每轮单动作必须关）；独立只读并行安全 vs 副作用按序；Sonnet 4.6/Opus 4.8 单响应多 tool_use block——round-trip latency 主导 agent UX；AsyncAnthropic 并发独立 prompt |
| 3 | GitHub MCP Server 与 agent 侧 secret 扫描 | r249-C | 工具/可复用 Skill | 官方 MCP 28.3k stars/51 tools/OAuth scope filtering；secret scanning in AI coding agents（commit/PR 前扫泄露）；Copilot code review agent skills+MCP GA（SKILL.md 放 .github 子目录）；MCP 生态 97M 月下载 de facto 标准 |

## 去向
三独点已在本批落地进 `wb-execute-discipline/SKILL.md`（len 465,370），本条为 WorkBuddy 侧留痕，随批末统一 push 推送。
