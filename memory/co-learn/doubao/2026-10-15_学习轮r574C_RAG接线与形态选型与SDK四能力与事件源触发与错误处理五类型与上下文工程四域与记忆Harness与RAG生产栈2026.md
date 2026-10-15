# 学习轮 r574C（2026-10-15 · AI 技能库工程与方法论 + AI 智慧进化）

十站实拉（全量逐站，r574 批第 3 轮，角度与前两轮错开）：Dify（工作流/RAG 角度）/ n8n（模板/用例角度）/ Langflow（组件/向量库角度）/ Activepieces（pieces 开发/管理角度）/ Make（错误处理/迭代器角度）/ Pipedream（工作流开发/事件源角度）/ Anthropic（Agent SDK/MCP 工具角度）/ skills.sh 生态（LobeHub/发现角度）/ GitHub 生态（新仓库/趋势角度）/ deeplearning.ai（LangGraph 记忆/课程角度）。判重基准：execute 3.91.0（r574B 3 章）+ compressor 3.688.0（r574B 3 章）+ r574A 6 章 + r573 批 18 章 + r572 批 18 章 + 更早批次 + WB 留痕。

## 落地（execute 3.91.0 → 3.92.0，+3 章）

1. **RAG 接线与应用形态选型：多库并发/去重叠 + Context 变量引用+自动 citations + 编排四选 + 迭代节点**（来源：Dify 2026-05-18/2026-06-05 + 尧图 2026-10-06 + Dify 2026-06-16）
   - 多知识库并发检索+库间去重叠（重叠=重复结果，选互补主题）；Context 变量引用 {{knowledge_retrieval.result}}+自动 citations
   - 编排四选：聊天助手/Agent（自决）/工作流（固定可控）/文本生成；流程固定用工作流、不确定用 Agent；迭代节点=无条件 array 遍历（多文件）
   - **提升层**：工作流 / 可复用 Skill

2. **Agent SDK 四能力与自定义工具契约：内置工具/Hooks/Subagents/MCP + Handler 规范 + managed agent + 哈希锚定编辑**（来源：Claude Code 2026-09-28/2026-10-10 + Claude 2026-10-10 + oh-my-pi 2026-10-06）
   - SDK 四能力（工具/Hooks/子代理/MCP）；工具 Handler=async+validated arguments+content 数组
   - Managed Agent=markdown 配置（name/model/agent_toolset）+ant apply；哈希锚定编辑（内容哈希定位）
   - **提升层**：工具 / 可复用 Skill

3. **事件源与触发选择：监控新数据发事件（REST/SSE 消费+自建）+ $emit 三字段 + push 优先不 polling**（来源：腾讯云 2026-09-29 + Pipedream 2026-10-14 + Integration Atlas 2026-04-29）
   - 事件源=监视新数据发事件触发工作流（REST/SSE 消费+自建）；$emit 事件带 id/summary/ts
   - 触发优先 push notifications（sub-2 分钟）不选 polling
   - **提升层**：工具 / 工作流

## 落地（compressor 3.688.0 → 3.689.0，+3 章）

1. **错误处理五类型与迭代器扁平化：Break/Ignore/Resume/Commit/Rollback + 默认回滚 + flatten before iterate + 路径隔离**（来源：Make Academy 2026-05-21 + DEV 2026-10-02 + Dre Dyson 2026-05-09 + Make Community 2026-08-21）
   - 错误处理五类型（handler 附加具体模块只在失败时跑）；无 handler 默认取决于不完整执行存储（off→rollback）
   - 迭代器前先扁平化（Set Variable 提取纯数组+映射具体路径+验证单对象）；路由器路径隔离（分流 items 不跨路径）
   - **提升层**：可复用 Skill / 工作流

2. **上下文工程四域与技能包设计：长期记忆/代码库结构/任务状态/工具权限 + 小易改可组合不绑模型（反框架）**（来源：CSDN 40 周 2026-10-11 + AIToolly 2026-10-07 + 抖音 2026-10-11）
   - 上下文工程四域决定 Agent 稳定性（竞争重心从模型原生能力转向上下文工程）
   - 技能包反框架设计（刻意做小/易改/可组合/不绑模型）；技能化趋势（技能包=核心复用单元）
   - **提升层**：可复用 Skill

3. **记忆工程新解法与 RAG 生产栈：Reflex Agent 模型驱动 Harness 无损记忆 + LangMem + RAG 生产五件套 + RAG 边界定位**（来源：智东西 2026-10-14 + DeepLearning.AI 2026-10-14 + Scrimba 2026-05-11 + Agentic Firehose 2026-10-09）
   - Reflex Agent（MIT）=模型驱动 Harness 接管调度（无损记忆/无限上下文，解长任务失忆）；LangMem=LangGraph 记忆管理库
   - RAG 生产五件套（evaluation/logging/monitoring/observability/quantization+多模态）；RAG 边界=查文档+写答案（非 agent）
   - **提升层**：可复用 Skill / 工作流

## 十站实拉要点（逐站留痕，与 r574A/B 角度不同）

- **Dify（工作流/RAG 角度）**：知识检索节点多库并发+节点级设置合并；Vision 标签跨模态检索（返回文本+图）；Context 变量引用 {{knowledge_retrieval.result}}+自动 citations；编排四选（聊天助手/Agent/工作流/文本生成，企业 90% 用工作流因为可控）；最优 chunk 500-1000 token；多库避免重叠（重叠=重复结果）；迭代节点=无条件 array 遍历（多文件）
- **n8n（模板/用例角度）**：9102 AI 模板；GMB 自动回复（30min 监控+品牌语气+Sheets 记录+多业务分离+防重复 provider 事件 ID）；WordPress 博客 HITL（Airtable 界面+人工审阅）；OpenRouter 1.78 专用节点（流中换模型，旧版 BaseURL workaround）；生产实测模板（invoice/PO 对账）；官方库 verified creator
- **Langflow（组件/向量库角度）**：向量库组件能力谱（embedding/相似度/Graph RAG 遍历/OpenSearch）；pgvector 前置三件（vector 扩展+CREATE 权限+可选依赖）；Astra DB 向量化内建（去单独组件）；RAG 接线（Read→Split→Embedding→Ingest）；bundles（Weaviate/FAISS/Milvus/Couchbase/DataStax）
- **Activepieces（pieces 开发/管理角度）**：pieces 两级管理（平台装/项目显隐，项目级只能隐藏平台已装的）+每小时 npm 自动同步+每步钉版本；私有 piece=tarball 上传安装（CLI build→.tgz→平台）；Webhook trigger 两阶段（On Enable 注册+On Handshake challenge）；MCP 工具 ap_read_step_code（全读 vs ap_flow_structure 截断 300 字符）；765 个开源 pieces
- **Make（错误处理/迭代器角度）**：错误处理五类型（Break/Ignore/Resume/Commit/Rollback，handler 附加模块只在失败时跑）；无 handler 默认=不完整执行存储设置（off→rollback，3 次后...）；迭代器前先扁平化（Set Variable/JSON Parse 提取纯数组 response.data.invoices+映射具体路径+验证单对象）；路径隔离（分流 items 不跨路径，if/else+merge 或 magic formula 聚合前取回）；上游数据变形状排查（对比成功/失败 run input bundle）
- **Pipedream（工作流开发/事件源角度）**：事件源监视新数据发事件（REST/SSE 消费+自建）；$emit 三字段（id 去重/summary/ts）；端用户工作流（HTTP trigger+x-pd-environment: development+x-pd-external-user-id）；多触发器（任意数量）；Gmail New Email 用 push 不 polling（sub-2 分钟）
- **Anthropic（Agent SDK/MCP 工具角度）**：Agent SDK 四能力（内置工具/Hooks/Subagents/MCP）；自定义工具 Handler（async+validated arguments+content 数组）；managed agent=markdown（name/model/agent_toolset_20260401）+ant apply；MCP=免写集成（自动认证+API，连 Slack/GitHub/Drive/Asana 不写集成代码）；SRE agent=scoped tools 按安全基础设施限定
- **skills.sh 生态（LobeHub/发现角度）**：LobeHub 市场 334,166 技能（agent-first）；CLI：npx @lobehub/market-cli skills install --agent <client>；发现=给 agent 提示词引市场索引（Read lobehub.com/skills/skill.md）；Browser 合集 Top22=分离轻量检索与完整浏览器控制（fetch/搜网无 GUI vs 驱动浏览器）；proactive-agent（openclaw，WAL Protocol/Working Buffer/Autonomous Crons）；技能包周榜 Top10（superpowers 217k/skills 179.7k）
- **GitHub 生态（新仓库/趋势角度）**：Reflex Agent（APUS-AI-Lab，MIT，模型驱动 Harness 无损记忆/无限上下文）；Matt Pocock skills（28.4 万★，反框架：刻意做小/易改/可组合/不绑模型，30 秒安装）；40 周趋势=Agent 技能化+上下文工程四域；REA（morluto，3 天 12 万★逆向工程）；Agent-Native（Agent+UI+动作+状态同框架，动作双触发）；oh-my-pi（Rust 终端代理，31 工具/60+ 模型，哈希锚定编辑）；Tencent/AI-Infra-Guard
- **deeplearning.ai（LangGraph 记忆/课程角度）**：Long-Term Agentic Memory With LangGraph（LangMem 记忆管理，1h24m）；RAG 课程五模块（概述/文档嵌入/生成/评估/部署）；RAG 生产五件套（evaluation/logging/monitoring/observability/quantization+多模态 RAG）+RAG vs fine-tuning 取舍+agentic RAG；RAG 边界=lookup+write-up（fetch the facts, don't guess，非 agent 本身）；Building Your Own Database Agent / AI Agents in LangGraph

## 功能套件核查（⑦）

三核心套件本轮无优化项；新增观察：编排四选（对照 execute 建流纪律）、错误处理五类型（对照 execute 失败分诊）、上下文工程四域（对照 compressor 上下文预算管理）、RAG 生产五件套（对照 compressor 评测强化）、技能包反框架设计（对照 wb-skill-authoring）。

## 垃圾清理（⑨）

删了什么：本批实拉全走 general_search，无本地临时文件落盘，未产生新垃圾。保留什么：*.bak 与全部核心产物（两 SKILL 文件 + r574C 留痕）；历史探针垃圾待删除通道可用时清理。

## 信源健康度

无删源无加源；Flowise 已删除不拉；打不开自动开桌面 VPN（本轮未触发）。commit/push 挂起（git 通道持续不可用，累计 r546→r574C 共 28 批）。
