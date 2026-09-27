# r252-A WorkBuddy 学习（2026-09-27）

来源：Dify agent memory/orchestration 面 / n8n RAG 面 / LangFlow memory 面 / Activepieces AI builder 面 / Make branching 面 / Pipedream secrets 面 / Claude Code subagents 面 / skills.sh CLI 面 / deeplearning.ai 课程面 / WaytoAGI 知识库面（10 站实拉）。

**可内化方法**：
- Dify Agent 记忆体系：TokenBuffer 窗口 + 1.0 长期记忆三能力（自动/手动/检索 + TTL）+ conversation_id 契约 + 生产 Redis/PG 双层 + Hindsight/MemOS 插件三工具模式。
- n8n RAG 生产实践：Ollama 本地嵌入 + Qdrant dense+BM25 sparse 混合 + 知识保鲜删除管线 + chunk 1000/100 + <10MB 限制。
- LangFlow Memory Base 三分类：语义检索（per-flow vector store）vs Message History 时间顺序 vs knowledge base 手工填充。
- Claude Code subagents 三形态（fan-out/pipeline/background）+ 编排循环 + file-level dependency 分析 + step budget + description 动态选择。
- skills 安装 CLI 生态四通道：npx skills add / gh skill install @tag / Databricks aitools 自动检测 / localskills --project --symlink。

**判重结论**：5 独点相对 r224-r251C 全部新真独，落地 wb-execute-discipline（commit 367a3cf）。
