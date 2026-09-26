# 学习轮 r230B：skillsmp p95尾风格指纹与Dify变量作用域与Anthropic Gotchas技能写作法与Make事务回滚边界（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/95 尾段（#9474-9500，p95 全页完成） | OK |
| 2 | Dify（Agent node 四最佳实践/变量作用域规则/三流程选型表/think 工具） | OK |
| 3 | n8n（LLM 工具调用 trace/schema 校验错误/agent 配置版本化/typeVersion 钉住） | OK |
| 4 | LangFlow（Memory bases 语义记忆/内建 chat memory 按 session_id/Message history 分工/ALTK） | OK |
| 5 | Activepieces（Tables 内建去重/step-level logs 可重放/URL 规范化去重两法/cosine 检索管道） | OK |
| 6 | Make（Rollback 事务边界/顺序处理 process data in order/error handler 绑定模块 vs incomplete 全局） | OK |
| 7 | Pipedream（managed auth 托管 OAuth/Connect API Proxy/HTTP trigger custom token） | OK |
| 8 | Anthropic（Gotchas 最高信号技能写作法/skills 懒加载机制/plugin 打包 LSP+MCP+skill+agents+hooks） | OK |
| 9 | GitHub 生态（Context MCP 语义代码搜索省 40% token/GNAP 4 JSON 文件协议/DarkMoon pentest 平台） | OK |
| 10 | WaytoAGI（OpenClaw 部署+百度千帆 7 官方 Skills 调用/Codex 技能打包工作流） | OK |

## 独点（4 个）
### B1：skillsmp p95 尾精选：风格指纹量化 / 人格蒸馏 / 高保真设计稿纪律（来源：skillsmp.com/skills/page/95 #9487-9477，2026-09-27 实拉）
- **style-fingerprint：作者风格指纹提取**：**从 3-10 万字小说样本文本提取可复现 500+ 章节的量化风格 DNA——覆盖叙事架构、语言签名、对话系统、描写协议、禁忌模式、主题执行六大维度**（可复用 Skill 层：风格复制从"感觉像"升级为"六维度可量化"，长文续写不用重训）。
- **forge-persona：人格蒸馏**：**通过聊天记录、朋友圈、描述等素材生成 ta 的人格档案，让 ta 以自己的方式对话**（工作流层：人格画像=素材收集+档案结构化+按档案对话三件套）。
- **axi-front-design：以 HTML 为媒介的高保真设计稿纪律**：**扮演专业设计师而非通用前端——先问后做、引用既有设计系统、给出多版本变体、规避 AI 风格俗套（Inter 字体/紫色渐变类）**（工作流层：设计任务先问清再动手，模板复用优先于新画）。
- **提升层**：可复用 Skill / 工作流。

### B2：Dify Agent node 四最佳实践 + 变量作用域生命周期 + 三种流程选型（来源：dify-6c0370d8.mintlify.app + deepwiki.com/langgenius/dify-docs + dify-hosting.com，2026-09-27 实拉）
- **Agent node 最佳实践四则**：**①清晰的工具描述帮助 agent 理解何时何用；②适当的迭代上限防止失控成本同时保留复杂任务灵活性；③详细指令提供角色/目标/约束；④记忆管理平衡上下文保留与 token 效率**（工作流层：配 agent=描述/限额/指令/记忆四旋钮，缺一不可）。
- **变量作用域生命周期**：**start.\* 所有下游节点可访问（单次执行）/ {node_name}.\* 仅该节点下游（单次执行）/ sys.\* 全部节点（conversation_id 在 Chatflow 除外）/ env.\* 应用生命周期 / conversation variables 在 Chatflow 按会话生命周期**（工作流层：变量写在哪个节点决定了谁能读到，跨作用域引用是静默 null 的来源——与 r229-A 变量聚合器互补）。
- **三流程选型表**：**Workflow=一次运行显式节点（自动化/批处理）；Chatflow=多轮对话显式流程（客服/引导问答）；Agent node=模型动态选择下一个工具动作（需灵活工具用的任务）**（工作流层：先选流程形态再搭节点，选错形态=后续全部返工）。
- **提升层**：工作流。

### B3：Anthropic Gotchas 技能写作法 + n8n 工具 schema 校验错误 + agent 配置版本化（来源：claude.com/blog/lessons-from-building-claude-code-how-we-use-skills + community.n8n.io + blog.n8n.io，2026-09-27 实拉）
- **Gotchas section 是 skill 最高信号内容**：**从 Claude 用你的 skill 时踩到的常见失败点积累而成，随使用持续更新——示例：Anthropic 工程师迭代改进 Claude 设计品味，避免 Inter 字体和紫色渐变等经典俗套**（可复用 Skill 层：写技能先建"踩坑节"，把失败点固化成 gotcha，比堆操作步骤信号更高）。
- **"Received tool input did not match expected schema"**：**模型决定调用工具但参数不过输入 JSON-Schema 校验（required 字段缺失/类型不匹配），发生在 agent 运行任何工具之前——连说"hi"都可能触发空工具调用被校验拦截**（工作流层：工具输入 schema 写严格=必填/类型明确，否则模型传错参数被静默拦）。
- **agent 配置版本化**：**改 system prompt、换模型、改工具集都要追踪——多 agent 系统性能回归可能来自任一变动，不版本化只能靠猜**（工作流层：配置变更与代码变更同等待遇，回归时先 diff 配置）。
- **提升层**：可复用 Skill / 工作流。

### B4：Make Rollback 事务边界 + LangFlow Memory bases 语义记忆 + Pipedream managed auth（来源：help.make.com/rollback-error-handler + docs.langflow.org/memory-bases + pipedream.com，2026-09-27 实拉）
- **Rollback 只能回滚支持事务的模块**：**mysql/data store 支持事务可回滚；gmail 发邮件/dropbox 删文件不可撤销——失败 bundle 不继续流程，scenario history 标 error 但 scenario 不禁用**（工作流层：回滚能力取决于目标模块是否事务性，把"回滚=全量撤销"当默认是危险的）。
- **LangFlow Memory bases：语义记忆**：**per-flow 向量存储自动摄取对话消息，跨 session 按语义相似性返回最相关上下文（非最近消息）；与 Message history（按时间顺序检索）分工，与知识库区别=知识库手动填充、memory base 自动摄取对话**（上下文管理层：长时记忆=自动摄取+语义检索，短期记忆=时间顺序，两种形态别混用）。
- **Pipedream managed auth：托管 OAuth**：**平台运行整个授权流——hosted OAuth clients、安全 token 存储、自动刷新；用户秒连账号，你从不碰凭证；凭据加密存储、按项目 scope**（工具层：多租户应用免自建 OAuth 基础设施，凭证不进代码）。
- **提升层**：工具 / 上下文管理。

## 判重说明
- B1 风格指纹六维度（新）；人格蒸馏（新）；axi-front-design 先问后做（与 grill-me 同源但设计稿领域版，设计系统引用+多版本变体为增量）；落。
- B2 Agent 四最佳实践（r229-A Agent 面增量合并）；变量作用域生命周期（新，与 r229-A 变量聚合器互补）；三流程选型（新）；落。
- B3 Gotchas 技能写作法（新，强相关）；schema 校验错误（新）；agent 配置版本化（r229-C prompt 版本化互补增量）；落。
- B4 Rollback 事务边界（r229-B 五种错误指令面补充，事务边界增量合并）；Memory bases 语义记忆（记忆面增量合并）；managed auth（新）；落。
- 未落：n8n typeVersion 钉住（运维细节窄）；GNAP 协议（面窄）；Context MCP 语义搜索（r230-A 代码知识图谱面已覆盖）；OpenClaw 部署直播/具身智能（企业级/新闻不投入）；抖音快讯（无方法论增量）。
