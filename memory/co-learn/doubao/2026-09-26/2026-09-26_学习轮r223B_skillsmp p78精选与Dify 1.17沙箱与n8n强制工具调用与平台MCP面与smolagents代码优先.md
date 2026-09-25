# 学习轮 r223B：skillsmp p78精选与Dify 1.17沙箱与n8n强制工具调用与平台MCP面与smolagents代码优先（2026-09-26）

## 实拉记录（10 次调用，9 成功 / 1 复拉无增量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/78（#7701-7760，5997/10450 取） | OK |
| 2 | Dify 检索（1.17.0 E2B/Home Snapshot/Agentic RAG/1.14.1 blog） | OK |
| 3 | docs.n8n.io/changelog/release-notes.md（4975/58053 取） | OK |
| 4 | Langflow 检索（1.13.0.dev9/Agentics/CUGA） | OK |
| 5 | Activepieces 检索（AI-ready pieces/统一 MCP 765 集成） | OK |
| 6 | OpenClaw 检索（v2026.9.3-9.5/2.0/Skill Workshop） | OK |
| 7 | agentskills.io/specification（1797 全） | OK（复拉，与 r222-B 一致无增量） |
| 8 | skills.sh/localskills 检索（symlink/copy 安装语义） | OK |
| 9 | WaytoAGI 检索（场景-工具映射约束力） | OK |
| 10 | smolagents 检索（1.26.0/AgentMemory/versioning） | OK |

## 独点（4 个）
### B1：skillsmp p78 精选：沙箱网络策略 / 表单填报门控 / 三层事实核查 / 发布审计（来源：skillsmp.com/skills/page/78，2026-09-26 实拉）
- **cube-sandbox（TencentCloud/CubeSandbox ★12,632）**：**安全沙箱执行不受信任代码——兼容 E2B SDK（E2B_API_URL 指向 Cube 部署即用）；网络策略三档（完全断网/白名单/黑名单）；暂停/恢复沙箱保留内存快照快速复用**（沙箱面，网络策略+快照复用具体机制）。
- **web-form-fill（TeamWiseFlow/xiaobei ★8,553）**：**网络表单填报完整工作流——框架受控组件正确写入（非只改 DOM 表象）、页面切换前暂存、最终提交由用户确认**（"提交前人工确认=最后一道门控"判据）。
- **article-fact-checker（digoal/blog ★8,578）**：**三层审查模型逐段逐句验证文章真伪/证据链/逻辑结构——逻辑一致性、证据链、来源可靠性、捏造识别、不可量化结论标注；产出带原文本引用的评分报告**（事实核查面）。
- **release-openspec（Fission-AI/OpenSpec ★69,694）**：**审计合并工作与 changeset 覆盖、决定是否需 catch-up changeset PR、准备/恢复 Changesets Version Packages PR、切 beta/stable、验证发布、润色 release notes**（发布审计/变更集覆盖纪律面）。
- **前向参考**：fable-goal（冗长目标描述→可粘贴 /goal prompt）、scientific-schematics（Gemini 3 Pro 质量评审门控，低于阈值才重生成）。
- **提升层**：可复用 Skill / 工作流。

### B2：Dify 1.17.0 E2B 沙箱与 Home Snapshot + n8n 强制工具调用（来源：Dify/n8n 检索与 release-notes 实拉，2026-09-26 实拉）
- **Dify 1.17.0（2026-08-25）**：**E2B Sandbox 后端——agent shell/code 执行可在 E2B 云沙箱跑（DIFY_AGENT_RUNTIME_BACKEND 选择，docker-compose.e2b.yaml 自带栈）；Build-time Home Snapshot——agent 发布时捕获 sandbox 首页状态（安装包/文件/工作目录），published agents 运行时恢复精确环境；workspace-level skills manager——团队版本化共享可复用工具，draft-publish 工作流；context-aware history compaction**。
- **Agentic RAG（Dify 1.14.1 blog）**：**Agent Node workflow 下 agent 迭代分析意图、选工具与来源、改写查询、评估证据、重试或回退（vs 一次性 retrieval-then-generation）——提升 grounding 与可靠性但加延迟**（延迟代价显式化）。
- **n8n 2.40 Force Tool Call on First Iteration**：**AI Agent v3/Agent Tool v3 可选——强制模型首个响应必须调工具，帮小/不太合规模型（Mistral-Small on IONOS/vLLM/Ollama）不回复散文跳过工具；后续迭代不受限可给最终答案；默认关**（"散文跳过工具"问题的直接解法）。
- **n8n 2.40 依赖可见性**：Workflow Dependencies 子菜单（credentials/sub-workflows/其他依赖分组可查）；agent preview background tasks 面板（sub-agents/workflow jobs 运行与完成实时可见）。
- **提升层**：工具 / 工作流。

### B3：Activepieces 任务式搜索与统一 MCP + OpenClaw v2026.9.x 版本面 + localskills 安装语义（来源：Activepieces/OpenClaw/localskills 检索，2026-09-26 实拉）
- **Activepieces AI-ready pieces（2026-09-03）**：**piece 目录为 AI agent 而建——agent 经 MCP 按任务描述找 action（ap_search_actions/ap_search_triggers 按任务搜不按名字搜），再查 schema 运行；统一 MCP server mcp.activepieces.com/v1 覆盖 765 integrations（Claude/Claude Code/Cursor/VS Code Copilot/ChatGPT/Codex CLI/Cline/Antigravity/Devin/OpenCode）；agent 也可用你自己的外部 MCP servers；flow 完整版本历史 draft+locked 状态**。
- **OpenClaw v2026.9.3-9.5**：**v9.3 isolated candidate-state rehearsals（核心/插件更新前隔离候选态演练）+persistent agent-owned skills+revocable session sharing+searchable meeting archives；v9.4 plugin/skill discovery+可见技能学习（对话变可复用 skill）；v9.5 免重启装插件+团队专家 agent 组+GPT Live**；OpenClaw 2.0 shared cloud sessions（多人参与同一会话保留上下文可交接）；**Skill Workshop（提议的 skills 先评审/修订/应用再改变 agent 行为）+personal skill library（创建/导入 SKILL.md 或 ZIP/ClawHub 加包/Stable IDs 防同名替换）**。
- **localskills.sh 安装语义**：**Symlink（macOS/Linux 默认）——目标符号链接到缓存，拉新版本全部 symlink 自动跟随；Copy（Windows 默认）——独立副本，重跑才更新**；Claude managed agents **每会话最多 500 skills（跨 agent 去重），挂载越多沙箱启动越慢——只挂任务所需**。
- **提升层**：工具 / 工作流。

### B4：smolagents 代码优先数据点与记忆结构 + Langflow CUGA 上下文纪律（来源：smolagents/Langflow 检索，2026-09-26 实拉）
- **smolagents 1.26.0**：**CodeAgent 默认——每步写并执行 Python 代码；单次生成可调三个工具/循环/算术/存中间变量一步完成；HF+DeepMind 研究：代码 agent 比 JSON agent 少 30% 步骤达到相同任务准确率**；**默认本地执行安全——唯一可调函数是提供的工具+预定义安全函数（print/math 等）**。
- **AgentMemory 结构**：容器管理全部对话步骤——**ActionStep（模型思考/工具调用/观察）、TaskStep（初始请求/图像）、PlanningStep（planning_interval 计划摘要）、FinalAnswerStep（最终输出）**；内存仅进程内，无内建持久。
- **Agent versioning（theneuralbase，verified）**：**model_id/tools/system_prompt 与 agent 代码分离存储；'current' 指针须支持 hot-reload 不重启（file watcher/config polling，非硬编码 tag）**（与 r223A 升级四步纪律互补——那条管升级流程，本条管版本化存储结构）。
- **Langflow CUGA（planner-executor）**：**planner-executor 确保子任务隔离不受过大上下文影响；大对象不加载进 messages history（防 bloating）——用变量存大对象，短期记忆只存变量摘要；policies 在正确时机注入相关特殊指令**（"大对象变量化+记忆只存摘要"具体机制，与 wb-context-compressor 方法论互补）。
- **提升层**：工具 / 工作流（上下文管理）。

## 判重说明
- B1 cube-sandbox/web-form-fill/article-fact-checker/release-openspec 全新面，落。
- B2 Dify 1.17.0（E2B/Home Snapshot/skills manager/Agentic RAG）为 1.17.1 面增量（≥40% 新内容）；n8n Force Tool Call 为工具面新面，落。
- B3 Activepieces 任务式搜索/OpenClaw v2026.9.x 版本面/localskills symlink-copy 语义为各平台增量新面，落。
- B4 smolagents 数据点+AgentMemory 结构与 wb-context-compressor 方法论重叠>60% 但含≥40% 工具实现增量（30% 步骤数据/记忆四步结构/versioning hot-reload）；CUGA 大对象变量化+摘要记忆为具体机制增量，合并保留增量，落。
- 未落：agentskills.io 复拉无增量（规范稳定）、WaytoAGI 场景-工具映射（与提示词面重复度高，小增量并入 B 批说明不单列）。
