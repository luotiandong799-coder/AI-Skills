# r252-B WorkBuddy 学习（2026-09-27）

来源：Dify RAG/knowledge pipeline 面 / n8n agent memory 面 / LangFlow testing/export 面 / Activepieces MCP 面 / Make webhooks 面 / Pipedream OAuth 面 / Claude Code memory 面 / SkillsMP 面 / OpenClaw memory 面 / DeepSeek plugin 面（10 站实拉）。

**可内化方法**：
- Dify Agentic RAG 与 Knowledge Pipeline：Agent Node 集中决策引擎（意图+源选择+重试）、动态选 1-2 collection + Google fallback、可视化 RAG ETL（解析/chunk 逐节点）。
- n8n agent memory 分层：Window Buffer 超窗全忘、memory 子节点画布化（contextWindowLength/sessionKey 可配）、Data Table 多 session 持久、Postgres 短期 + pgvector 长期双两层。
- LangFlow 调试与 DevOps：Playground 删测试消息影响行为、Traces 内置可观测（延迟/token/JSON 下载）、lfx validate 本地校验再推送、版本历史恢复。
- Activepieces MCP server：单 URL 暴露 763+ apps、OAuth 浏览器认证、ap_search_actions 按任务搜动作、数据 masking。
- Claude Code 三层记忆：CLAUDE.md 显式 / Auto Memory 隐式（200 行或 25KB）/ Memory Tool API；4 补位模式（hooks/claude-mem/graphify）。

**判重结论**：5 独点相对 r224-r252A 全部新真独，落地 wb-execute-discipline（commit 8da1586）。
