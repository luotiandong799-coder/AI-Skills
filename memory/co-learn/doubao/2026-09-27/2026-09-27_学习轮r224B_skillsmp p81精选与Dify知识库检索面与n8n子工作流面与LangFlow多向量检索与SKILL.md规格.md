# 学习轮 r224B：skillsmp p81精选与Dify知识库检索面与n8n子工作流面与LangFlow多向量检索与OpenClaw验证与SKILL.md规格（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/81（#8001-8058 取） | OK |
| 2 | Dify 检索（Summary Index/Context Variables/双层检索） | OK |
| 3 | n8n 检索（2.41.0/Sub-workflows/Dependencies/Chat tool） | OK |
| 4 | LangFlow 检索（Desktop 1.11/NextPlaid 多向量检索/DB Providers） | OK |
| 5 | Activepieces 检索（agents/approval/AI SDK） | OK（approval 流程面增量） |
| 6 | Make 检索（2026-09 app 更新/scenario usage tracking） | OK |
| 7 | Anthropic skills 检索（官方仓库/工程实践/skills API） | OK |
| 8 | docs.openclaw.ai 检索（creating-skills/skills verify/config） | OK |
| 9 | agentskills.io 检索（Specification/SKILL.md 规格） | OK |
| 10 | deeplearning.ai 检索（Agent Skills with Anthropic 课/Agentic AI） | OK |

## 独点（4 个）
### B1：skillsmp p81 精选：SKILL.md 审计 / 写前安全 hook / 论文阅读路由 / EU AI Act 盘点（来源：skillsmp.com/skills/page/81，2026-09-27 实拉）
- **skills-audit（lobehub/lobehub ★82,793）**：**循环审计 .agents/skills SKILL.md——重复/重叠/过时/不一致/损坏的技能与合并删除候选**（技能库审计面，与本批学习判重方法同源但作为可复用 audit skill 新面）。
- **security-guidance（alirezarezvani/claude-skills ★26,225）**：**PreToolUse 安全反模式 hook——捕获 12 类常见安全风险（命令注入/XSS/SQL 注入/不安全反序列化/GitHub Actions workflow 注入/eval/new Function 代码注入）在 Edit/Write/MultiEdit 完成前；会话级状态缓存防止同一文件+规则重复警告；仅 stdlib 无依赖**（写前安全 hook 面，与 OWASP 面同族、hook 机制增量）。
- **paperpilot（eyixinwang ★2）**：**Resolver-first 论文阅读——先分类 survey vs non-survey 再执行正确工作流（非 survey 走 first-principles 精读、survey 走 survey 阅读流）；仅当用户明确要求评估才用 evaluate-rubric**（论文阅读路由面）。
- **ai-inventory（anthropics/claude-for-legal ★9,491）**：**EU AI Act 逐系统盘点——每个 AI 系统的角色（provider/deployer/importer/distributor/授权代表/产品制造商）与风险层级（禁止/高风险/有限/最小/GPAI/GPAI+系统性）；角色与层级按系统评估，不按公司**（合规盘点面）。
- **提升层**：可复用 Skill / 工作流。

### B2：Dify 知识库检索面：Summary Index / Context Variables 自动引用 / 双层检索过滤器（来源：dify.ai blog + mintlify docs，2026-09-27 实拉）
- **Dify 1.12.0 Summary Index**：**把摘要附加到 chunks 上，相关内容一起返回——从碎片化检索到全上下文**（RAG 检索质量面）。
- **Context Variables（LLM 节点）**：**注入外部知识同时保留来源归属；知识检索输出接 LLM context 输入；Dify 自动跟踪 citations 让用户看到信息来源**（上下文变量+自动引用面）。
- **Knowledge Retrieval 双层设置**：**KB 级与节点级两层检索设置——连续两道过滤器：KB 决定初始候选池，节点级再 rerank 或缩小池；rerank 加权分=语义相似度与关键词匹配的相对权重**（双层检索过滤面）。
- **Variable Inspect Panel（Dify 1.5.0）**：**画布底部变量检视面板实时看全 workflow 变量；直接编辑变量值测试下游影响，不用重跑昂贵上游**（调试面）。
- **提升层**：工具 / 工作流。

### B3：n8n 子工作流编排面 + LangFlow NextPlaid 多向量检索（来源：docs.n8n.io + langflow.org，2026-09-27 实拉）
- **n8n Sub-workflows**：**模块化微服务式 workflow——Execute Workflow + Execute Sub-workflow Trigger 节点；子 workflow 执行不计入月度执行/活跃 workflow 限额；大 workflow 拆分子 workflow 也缓解内存问题**（子工作流模块化+配额豁免面）。
- **n8n Workflow Dependencies 菜单**：**workflow 菜单按类型列出凭据/子 workflow/其他链接资源依赖**（依赖清单面）。
- **n8n Chat tool 节点双实例模式**：**Agent 要在"发消息"或"等输入"间选择时，加两个 Chat tool 节点各管一个动作；Chat Trigger 的 Agent 推荐加 "Send a message and wait for response" 以便请求澄清**（agent 澄清交互面）。
- **n8n 2.41.0（2026-09-22）**：**ai-builder 把父级 ask-user 回答传入 Agent Builder**。
- **Langflow 1.11.0 NextPlaid**：**first-class 多向量检索——ColBERT 式 late interaction（文档存 token embedding 矩阵+MaxSim 评分）+ColPali 式视觉文档检索，零胶水代码；DB Providers 可配置向量后端（Chroma/Chroma Cloud/OpenSearch）**（多向量检索面，r224-A A3 LangFlow 面增量）。
- **提升层**：工具 / 工作流。

### B4：OpenClaw 技能验证 / agentskills.io 规格常量 / deeplearning.ai Skills 边界课（来源：docs.openclaw.ai + agentskills.io + learn.deeplearning.ai，2026-09-27 实拉）
- **OpenClaw skills verify @owner/**：**验证 skill 的 trust envelope；@owner/ 限定 ref 避免 publisher 歧义（不同 owner 可用同名 skill 不互相覆盖）；verify JSON 含 commit-pinned openclaw.verifiedSourceUrl 来源溯源**（owner 限定+提交钉定溯源面）。
- **agentskills.io 开放规格常量**：**name ≤64 字符小写连字符且必须匹配目录名；description 1-1024 字符同时写"做什么+何时用"（agent 加载前唯一可见内容）；SKILL.md <500 行；发现预算约 100 tokens（name+desc）；只允许 scripts/references/assets 三个子目录；第三视角 gerund 式描述**（SKILL.md 规格常量面）。
- **deeplearning.ai《Agent Skills with Anthropic》**：**专门一课 "Skills vs Tools, MCP, and Subagents" 界定三者边界；从预构建技能到创建自定义技能、Claude API/Claude Code/Agent SDK 全链路**（技能边界教学面）。
- **提升层**：可复用 Skill / 工作流。

## 判重说明
- B1 全新面，落。
- B2 Dify Summary Index/Context Variables/双层检索为 RAG 面增量（r223-B Agentic RAG、r224-A Agent Strategy 之外的检索质量面），落。
- B3 n8n Sub-workflow 模块化+配额豁免+Dependencies 为 r223-C n8n Agents 面增量（≥40% 子工作流编排细节）；LangFlow NextPlaid 为 r224-A LangFlow 面增量，合并落。
- B4 OpenClaw verify owner 限定+commit-pinned 溯源为 r223-B OpenClaw 面增量；agentskills.io 规格常量（新事实）；deeplearning Skills 边界课（教学路径面）；落。
- 未落：Make 2026-09 更新（app 更新/API v2，个人用户价值低）；Anthropic skills API 版本格式（r223-C 已落官方 17 技能面）。
