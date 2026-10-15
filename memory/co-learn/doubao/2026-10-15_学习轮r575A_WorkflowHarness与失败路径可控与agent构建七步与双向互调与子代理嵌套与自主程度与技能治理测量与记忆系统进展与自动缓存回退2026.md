# 学习轮 r575A（2026-10-15 · AI 技能库工程与方法论 + AI 智慧进化）

十站实拉（全量逐站，r575 批第 1 轮，角度与前批错开）：Dify（Workflow Studio/Harness 角度）/ n8n（Agents 一等公民/双向互调角度）/ Langflow（1.10-1.12 组件/工具端口角度）/ Activepieces（Agents 复用/内嵌 MCP 角度）/ Make（AI Agent 新 app/子代理/回退角度）/ Pipedream（Connect 集成层/编辑模式角度）/ Anthropic（Managed Agents 动态工作流/自动缓存角度）/ skills.sh 生态（SkillSpec/注册表评分/威胁扫描角度）/ GitHub 生态（记忆系统项目角度）/ deeplearning.ai（MemGPT/自主程度/连接模式角度）。判重基准：execute 3.92.0（r574C 9 章）+ compressor 3.689.0（r574C 9 章）+ r574A/B 12 章 + r573 批 18 章 + 更早批次 + WB 留痕。

## 落地（execute 3.92.0 → 3.93.0，+3 章）

1. **Workflow 即 Harness 与失败路径可控：模型只是节点 + 节点级停止/默认/恢复分支 + 对话建 agent 自动生成可复用 skills + Human Input 节点**（来源：Dify 2026-08-21/2026-08-27/2026-03-03）
   - Agent=模型节点+Workflow Harness；节点失败三选（停止/默认值/类型化错误转恢复分支）
   - 对话建 agent 自动生成可复用 skills+保留上下文+agent 作工作流节点；Human Input 节点（关键决策人签）
   - **提升层**：工作流 / 可复用 Skill

2. **agent 构建七步框架与 Workflow↔Agent 双向互调：Plan/Build/Configure/Tools/Knowledge/Test + Message an Agent 节点 + Call Workflow Tool + Think-Plan-Act + 工具端口通用**（来源：Make 2026-07-20 + n8n 2026-09-25 + N8N Lab 2026-10-12 + n8n 2026-03-12 + Langflow 2026-09-27）
   - 七步框架（含 knowledge+test）；agent 与工作流互相调用（agent 作节点+工作流作工具）
   - TPA 两段（THINK 结构化推理→ACT 分步执行）；工具端口通用（组件/agent/MCP 都可接）
   - **提升层**：工作流 / 可复用 Skill

3. **子代理嵌套与自主程度：agent 作工具嵌套（无硬编码交接）+ 自主程度光谱/任务分解 + 连接模式三型 + Agent 一等公民一句话构建**（来源：Make 2026-09-01 + DeepLearning.AI 2026-10-12/13 + crewAI 2026-05-09 + Activepieces 2026-09-03）
   - 子代理=agent 作工具嵌套+主代理动态选专业（无硬编码交接）；自主程度光谱+任务分解
   - 连接模式 parallel/sequential/hybrid+crew 测试训练；agent 从步骤设置→命名复用对象
   - **提升层**：工作流

## 落地（compressor 3.689.0 → 3.690.0，+3 章）

1. **技能治理新工具与测量：SkillSpec 可验证技能 + Skilldex frontmatter 评分 + 技能效果三测量 + 技能生态威胁扫描**（来源：SkillSpec 2026-07-31 + arXiv 2604.16911 + CSDN 2026-02-22 + arXiv 2605.28588）
   - SkillSpec 三阶段（Assess/Import/Execute+deny-by-default 工具边界）；Skilldex frontmatter 评分（description≥30 词触发阈值）
   - 技能效果三测量（触发率/工具调用数/失败数）；技能威胁 8 分类+MCP-scan 扫描引擎
   - **提升层**：可复用 Skill

2. **记忆系统新进展：Hindsight 四类记忆 + Reflex 三层记忆 + TencentDB CodeGraph 资产 + claude-mem 捕获压缩注入 + 上下文工具三型**（来源：DEV 2026-10-05 + 智东西 2026-10-14 + AIBARS 2026-10-10 + AIToolly 2026-10-06 + AgentIndex 2026-10-15）
   - Hindsight 四类（World facts/Experiences/Observations/Mental models）+Postgres 容器；Reflex 三层（无限累积/无损保存/无损输入）
   - TencentDB 代码库→CodeGraph/技能/Wiki 资产；claude-mem 捕获→AI 压缩→未来注入；上下文工具三型（长记忆/代码库索引/压缩）
   - **提升层**：可复用 Skill

3. **自动缓存与回退：Automatic caching 模式 + OpenAI 自动缓存 + LLM 回退连接 + 本地模型连接 + 内嵌 MCP 用户 token 隔离 + MCP 粒度步骤工具**（来源：Claude 2026-10-14 + Make 2026-10-09/2026-09-29 + Microsoft 2026-10-08 + Activepieces 2026-10-06/2026-10-05）
   - 缓存两方式（自动=顶层 cache_control+断点自动前移 vs 显式断点）；OpenAI 自动缓存；LLM fallback 连接
   - 本地模型调用（端点+提示+文件输入响应作变量）；Embeddable MCP 每用户项目 token 隔离；MCP 粒度步骤工具（add/update step）
   - **提升层**：工具 / 可复用 Skill

## 十站实拉要点（逐站留痕）

- **Dify（Workflow Studio/Harness 角度）**：Workflow 即 Agent 的 Harness（模型只是节点，可靠 agent 靠工作流体系）；节点失败路径三选项（停止/默认值/类型化错误转恢复分支）；版本保留发布历史；对话建 agent（自动生成可复用 skills+保留上下文+可作工作流节点）；Human Input 节点 v1.13.0（关键决策人签）；Agent 推理策略插件 Allowed tools list（名单外工具不给模型）；Creator Center 模板市场（一分钟采用）；医药案例（Copilot 日常+超范围 HTTP 请求升级专家环境）
- **n8n（Agents 一等公民/双向互调角度）**：n8n Agents 一等公民（定义一次到处用：聊天/节点/Slack/schedule）；Message an Agent 节点（工作流里调 agent，agent 带指令/工具/记忆）；Call n8n Workflow Tool（工作流作 agent 工具）；Anthropic writer/critic 双代理模板（house rules+rubric+迭代到阈值/停止条件+Sheets 记录+webhook 通知）；Research/Writer/Reviewer 三代理管线（自纠正+circuit breaker+审计元数据）；Think-Plan-Act 架构（THINK 结构化推理→ACT 分步执行）；LinkedIn MCP 模板（操作暴露为 bearer 认证端点后的 MCP 工具）
- **Langflow（1.10-1.12 组件/工具端口角度）**：Assistant 自然语言建完整 flow（非单组件）+Memory bases 长期语义记忆+DB Providers+7 语言；Extension bundles 组件提供商打包；Agent 组件工具端口（任意组件/其他 Agent/MCP Tools 都可作工具）；Flow DevOps Toolkit（画布外管理流）；预加载+写时复制优化；flow 部署为 MCP server/API/JSON 导出
- **Activepieces（Agents 复用/内嵌 MCP 角度）**：Agents 一等公民（从步骤设置→命名/简述/对话/复用+一句话构建）；Embeddable MCP（token 只对用户项目，用户靠 token 隔离；Cursor/Claude Desktop 自装自连 vs 内嵌给 app 用户）；MCP 粒度工具（ap_build_flow 用 ap_add_step/ap_update_step 加嵌套结构）；Personal AI MCP（memory/messaging/documents 10 工具）；AI Router for flows（0.92.0）
- **Make（AI Agent 新 app/子代理/回退角度）**：Make AI Sub-Agents（agent 作工具嵌套+主代理动态选专业，无硬编码交接）；Fallback connection（LLM 连接不可用保持运行）；OpenAI model caching（自动复用 prompt content）；建 agent 七步（Plan/Build/Configure/Add tools/Add knowledge/Test）；Maia（builder 内建 AI 协作员）；sales outreach agent 流水线；monday.com 平台 agent（Run Platform Agent 带 Context ID 会话记忆+Generate Chat Completion 结构化 JSON）
- **Pipedream（Connect 集成层/编辑模式角度）**：Connect=AI agent 集成层（托管 token/refresh/用户级权限，免 auth plumbing）；Edit with AI（构建器/检查器/code 步骤内按钮编辑既有流）；编辑模式与 live 分离+多语言+granular testing（可测单个步骤）+多触发器；10k+ 预建触发器与操作；本地模型连接（Power Automate Desktop：端点 URL+prompts+文件输入响应作变量）
- **Anthropic（Managed Agents 动态工作流/自动缓存角度）**：Managed Agents 动态工作流 beta（managed-agents-2026-04-01 头；agent 写 workflow=多 agent 分阶段合并结果，如审数百文档）；Automatic caching（顶层单个 cache_control+断点自动应用到最后可缓存块并随对话前移，适合多轮）；Fable 5.1/Mythos 5.1 缓存读 $0.25/M（0.025x）；Sonnet 5.5 缓存读 $0.10（0.05x）
- **skills.sh 生态（SkillSpec/注册表评分/威胁扫描角度）**：SkillSpec 可验证技能（Doctor 测 token load/埋藏指令/名称冲突/缺证据/URL 风险给数字；Import 转 routes/rules/forbids/deny-by-default 边界/回归测试；Execute 运行时问 CLI）；Agent DX CLI Scale（0-21，每轴 0-3）；Skilldex 注册表 frontmatter 评分（YAML 25 致命/name 10/description 10/≥30 词 10）；技能效果三测量（90% 触发/工具调用数/0 失败 API）；技能生态威胁 8 分类+MCP-scan 引擎；SKILL.md 格式演进（版本/依赖/安全元数据）
- **GitHub 生态（记忆系统项目角度）**：Hindsight（周榜 top，7 天 1.1 万星；四类记忆 World facts/Experiences/Observations/Mental models；单 Docker 容器含 Postgres）；Reflex 三层记忆（无限记忆/无损记忆/无损输入）；TencentDB-Agent-Memory 27.6k★（对话/文档/代码→记忆/技能/Wiki/CodeGraph 资产）；claude-mem（捕获全动作→AI 压缩→未来会话注入，支持多客户端）；Memory & Context 工具三型（长记忆/代码库索引/压缩）+更好上下文>更强模型
- **deeplearning.ai（MemGPT/自主程度/连接模式角度）**：LLMs as Operating Systems: Agent Memory（MemGPT agents 自主管理记忆+agentic RAG 外部记忆+多 agent 编排）；Agentic AI 9h55m（Degrees of autonomy 光谱+Task decomposition+Component-level evaluations+高度自主模式含 LLM 计划创建执行）；crewAI（parallel/sequential/hybrid 连接+多 crew flows+crew 测试指标+人类反馈训练+多 LLM 合适模型）

## 功能套件核查（⑦）

三核心套件本轮无优化项；新增观察：Workflow Harness 定位（对照 execute 编排四选）、失败路径可控（对照 execute 错误处理五类型）、子代理嵌套（对照 execute 多 agent 研究流）、自动缓存模式（对照 compressor 缓存成本量化）、记忆系统实现（对照 compressor 记忆流水线）、SkillSpec（对照 compressor 技能评测）。

## 垃圾清理（⑨）

删了什么：本批实拉全走 general_search，无本地临时文件落盘，未产生新垃圾。保留什么：*.bak 与全部核心产物（两 SKILL 文件 + r575A 留痕 + 既往批次留痕）；历史探针垃圾待删除通道可用时清理。

## 信源健康度

无删源无加源；Flowise 已删除不拉；打不开自动开桌面 VPN（本轮未触发）。commit/push 挂起（git 通道持续不可用，累计 r546→r575A 共 29 批）。
