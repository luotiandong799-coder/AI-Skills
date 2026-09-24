# 学习轮 r197-C：LangFlow文件高级解析与ClaudeCode云端调度与飞书技能上榜与agent统一监控与模型趋势（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/workflow/node | 死链 |
| 2 | docs.n8n.io/courses/level-two | OK |
| 3 | docs.langflow.org/components-data | OK 全文 |
| 4 | activepieces.com/docs/pieces/overview | 死链 |
| 5 | make.com/en/help/modules | 目录壳 |
| 6 | modelscope.cn/models | OK 258,436 |
| 7 | docs.anthropic.com claude-code/overview | OK 全文 |
| 8 | skillhub.tencent.com | OK 7.6 万复核 |
| 9 | skills.sh | OK all-time 榜 |
| 10 | GitHub AI 生态（robots 禁走搜索） | OK |

## 独点（5 个）
### C1：LangFlow File 高级解析（Docling）+ Web Search 类型转换 + API Request 双模式（来源：docs.langflow.org/components-data）
- File 组件：Docling 高级解析（v1.6+），默认 1024MB 上限（`LANGFLOW_MAX_FILE_SIZE_UPLOAD`），支持 21 种类型（含 py/ts/tsx/js/sql/yaml），单文件输出 Structured/Markdown/File Path 三形态；Web Search 输出 `DataFrame`，接 Prompt Template 必须过 Type Convert，接 Agent Tools 可直接连；API Request 支持 URL 模式与 curl 模式，`include_httpx_metadata` 可带 headers/status_code/redirection_history。
- 判据：**数据组件输出类型不统一（DataFrame/Message/Data），接 LLM 前先查类型，Type Convert 是常备件**。
- **提升层**：工作流。

### C2：Claude Code 文档索引 llms.txt + Routines 云端调度 + auto memory + 跨面接续（来源：docs.anthropic.com claude-code/overview）
- 完整文档索引 `https://code.claude.com/docs/llms.txt`（供 agent 发现全部页面）；Routines 跑在 Anthropic 托管基础设施（电脑关机也跑，可触发于 API/GitHub 事件，CLI `/schedule` 创建）；auto memory 自动记 build 命令/调试洞见跨会话；`/loop` 会话内重复 prompt；`claude --teleport` 把 web/iOS 会话拉回终端；Slack @Claude 报 bug 回 PR。
- 判据：**官方提供 llms.txt 作为 agent 可读文档索引——自己写 skill 也应给"文档地图"文件**。
- **提升层**：工作流/可复用 Skill。

### C3：skills.sh all-time 榜——飞书官方 lark-* 生态上榜 8.8M 总安装（来源：skills.sh）
- All Time 868,875 安装：find-skills 2.5M、frontend-design 660K、grill-me 542K；**open.feishu.cn 的 lark-approval/lark-okr/lark-markdown 等上榜，总安装 8.8M**；microsoft/azure-skills 6.2M total。
- 判据：**skill 生态已出现平台官方（飞书/微软/腾讯）大规模入驻**——选 skill 看厂商官方源。
- **提升层**：生态观察。

### C4：ModelScope 模型趋势——Qwen-Image-2.1 / DeepSeek-V4.1-Flash / AuK（来源：modelscope.cn/models）
- 25.84 万模型：Qwen-Image-2.1 25.9k、DeepSeek-V4.1-Flash 19.9k、MiniCPM5-2B 113.9k、Qwen3.8-27B 509.8k、GLM-5.3-Flash 76.7k、Tencent-Hunyuan/AuK 4.5k、moonshotai/Kimi-K3 27.8k。
- 判据：**国产开源梯队（Qwen/DeepSeek/GLM/MiniCPM/Kimi/Hunyuan）在 ModelScope 全量可见**。
- **提升层**：生态观察。

### C5：agent 统一监控与 harness 优化——agentglass / ECC / BrowserSkill（来源：GitHub 生态走搜索）
- SirAllap/agentglass：把所有 coding agent 放一屏，live 看成本/tokens/tool calls，**危险操作 hold 到用户确认**；affaan-m/ECC：agent harness 性能优化系统（skills/instincts/memory/security/research-first）；Tencent/BrowserSkill 6.6K（让 agent 借用浏览器）；obra/superpowers 29.08 万★（composable skills + initial instructions 引导 agent 应用）。
- 判据：**agent 治理（统一监控+危险操作门禁）已产品化；skill 框架用"初始指令引导应用"替代纯自动触发**。
- **提升层**：生态观察/安全。

## 判重说明
- C1 → r196-C 已记 Tool Mode/MCP Tools；components-data 首次真拉，Docling/类型转换/双模式全新。
- C2 → r197-A 已记三 beta headers + /v1/skills；claude-code overview 首次真拉，llms.txt/Routines/teleport 全新。
- C3 → r196-B 已记 skills.sh trending；all-time 榜 + 飞书 lark-* 首次见，取增量。
- C4 → r194-B 已记模型周榜；ModelScope models 首次真拉（此前仅 studios），取国产梯队增量。
- C5 → r196-A/C 已记 GitHub 生态（google-ax/scientific-agent-skills）；agentglass/ECC/BrowserSkill 增量。
