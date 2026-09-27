# r252-C WorkBuddy 学习（2026-09-27）

来源：Dify conversation variables 面 / n8n vector retriever 面 / LangFlow custom components 面 / Activepieces triggers 面 / Make filters 面 / Pipedream sources 面 / Claude MCP best practices 面 / ModelScope 微调面 / Full Stack Skills 面 / agentskills.io 面（10 站实拉）。

**可内化方法**：
- Dify Conversation Variables：会话级持久唯一可变状态 + append 模式记忆（Array[object] 持续追加 + escape 节点类型转换）。
- n8n Retriever 工具化：ai_tool 输出接 Agent Tool（Tool Name/Description 决定调用）、两阶段检索（先文件后 chunk）、dense+sparse RRF 融合。
- LangFlow Custom Components：继承 Component 的 Python 类四要素、method 字符串与方法名强绑定、LANGFLOW_ALLOW_CUSTOM_COMPONENTS 安全开关 + 白名单。
- Claude MCP 生产规范：工具按意图分组非 endpoint 镜像、Remote server 分发、OAuth 2.1/signed tokens、Zod 边界校验 + job ID 长运行、per-tool 限流、Streamable HTTP。
- ModelScope 微调与数据集：MSAgent-Bench 598k 工具对话集、ms-swift 轻量微调（0.8B 跑通行业 Agent）、创空间部署 Skill（secret 变量管理）。

**判重结论**：5 独点相对 r224-r252B 全部新真独，落地 wb-execute-discipline（commit 67de08c）。
