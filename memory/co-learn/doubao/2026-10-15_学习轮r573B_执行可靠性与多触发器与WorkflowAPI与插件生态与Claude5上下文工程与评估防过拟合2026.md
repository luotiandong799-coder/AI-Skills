# 学习轮 r573B（2026-10-15 · AI 技能库工程与方法论 + AI 智慧进化）

十站实拉（全量逐站，r573 批第 2 轮，不复用 r573A 结论，逐站重新实拉重新判重）：Dify（插件角度）/ n8n（AI Agent/向量角度）/ Langflow（API/容器化角度）/ Activepieces（piece 管理角度）/ Make（AI Toolkit/认证角度）/ Pipedream（多触发器/组件角度）/ Anthropic（上下文工程角度）/ skills.sh 生态（排名统计角度）/ GitHub 生态 / deeplearning.ai（社区评估角度）。判重基准：execute 3.87.0（r573A 3 章）+ compressor 3.684.0（r573A 3 章）+ r572 批 18 章 + 更早批次 + WB 留痕。

## 落地（execute 3.87.0 → 3.88.0，+3 章）

1. **执行可靠性三件套：持久队列（重启不丢）+ LLM 长任务 polling 声明 + 执行沙箱模式**（来源：n8n 2.42.0 2026-10-09 + dify-plugin PyPI 2026-10-04 + Activepieces Separate Workers 2026-09-08）
   - 持久队列：执行在失败/重启时不丢失
   - LLM polling：模型声明 polling 特性，长任务提交后短请求/响应轮询查结果（push/poll 两范式）
   - AP_EXECUTION_MODE=SANDBOX_CODE_ONLY 代码仅沙箱；worker 分离部署（token/并发/复用可配）
   - **提升层**：工作流 / 工具

2. **多触发器与并行执行：单流多入口 + 步骤级并发 + 认证 webhook 内置安全前门**（来源：Pipedream Triggers 2026-10-01 + Changelog 2026-10-04 + Make Authenticated Webhooks 2025-10-16）
   - 多触发器=单工作流任意数量入口共享逻辑；步骤级并行=独立步骤并发
   - 认证 webhook=内置系统性认证（安全前门），验证数据才进关键流
   - **提升层**：工作流 / 工具

3. **Workflow API 点号寻址组件参数覆盖 + 多智能体=状态机底层原则**（来源：Langflow Workflow API 2026-09-16 + CSDN 2026-09-08）
   - {component_id}.{parameter_name} 点号寻址给流内单组件传值/覆盖，不必重建流
   - 多 agent 系统=状态机（状态流转控全系统），2026 企业级核心工程原则
   - **提升层**：工具 / 工作流

## 落地（compressor 3.684.0 → 3.685.0，+3 章）

1. **插件生态与集成管理：Dify 六类型+发布三通道 + Activepieces piece 两级管理+私有 tgz+凭据无读回**（来源：LobeHub 2026-09-28 + DeepWiki 2026-08-30 + Activepieces Manage Pieces 2026-10-08/10-12 + Security 2026-03-11）
   - 插件六类型（Tool/Trigger/Extension/Model/Datasource/Agent Strategy——推理策略也是可插拔资产）
   - 发布三通道矩阵（官方 PR 自动验证/GitHub Release URL 安装/File Release 私有直发）
   - piece 两级管理（Platform 装卸/Project show-hide）+ registry 小时自动同步+步骤 pin 版本+私有 tgz 上传
   - 凭据无读回 API 设计：256-bit 加密+无 API 读回+agent 拿 OAuth2 limited scopes 不拿 key
   - **提升层**：可复用 Skill / 工具

2. **Claude 5 上下文工程新规则：提示瘦身 80% 无损失 + 服务端压缩自定义 instructions + 缓存布局与缓存读价 5%**（来源：Anthropic 2026-07-24 + Claude Platform 2026-10-12/2026-05-13 + Tabbit 2026-10-05 + wearetandem 2026-10）
   - 强模型提示瘦身实证：系统提示删 80%+ 无编码评测损失，"更强模型要更长提示词"被推翻；实践进 claude doctor
   - 服务端压缩：context_management key+instructions 参数完全替换默认总结提示词
   - 缓存布局：静态长文本前置+ephemeral 标记、动态查询后置（多轮命中前置缓存）；Opus 5.5 缓存读价 5%（vs 10%）
   - **提升层**：可复用 Skill / 工具

3. **评估防过拟合与提示解耦：静态评估集轮换+冻结集双轨 + 系统 prompt 不堆限制 + 小改动静默破坏回归**（来源：华为云 2026-08-31 + XBSTACK 2026-04-28 + Datalaria 2026-10-06）
   - 静态评估集过拟合：评估集每月轮换（新增/淘汰）防应试+冻结集保跨版本可比
   - 系统 prompt 不堆限制：注意力分布有限，工具校验/格式规范/答案生成拆独立 Pipeline 步骤分摊
   - 小改动静默破坏：单短语语气改动可致必填参数省略/无限重试，任何改动过回归
   - **提升层**：可复用 Skill / 工作流

## 十站实拉要点（逐站留痕，与 r573A 角度不同）

- **Dify（插件角度）**：Marketplace 模板生态（Sonilo 授权配乐/Pangolinfo Amazon Scraper/SearchApi 120,077 安装）；dify-plugin SDK LLM Polling 声明；插件六类型；dify plugin init 脚手架+模型插件权限；发布三通道（Auto-publish PR/GitHub Release/File Release）；dify-plugin-daemon 打包
- **n8n（AI Agent/向量角度）**：n8n Agents 全新一等公民实体（定义一次：对话/节点/Slack/计划）；v2.40–2.43 四连发（2026-09-15→10-06）；durable queue 持久队列；Claude Refine 子节点（block-level prompt caching+extended thinking+effort levels）；Gateway credits 免注册试用；RAG 模板：LLM metadata enrichment（异步补 topics/use_case/risks/audience_level/summary）、pgvector 客服路由（存 Postgres 忽略重复 provider event ID+top 召回+guardrails 强制人工升级）、Postgres→Pinecone（可配置 allow/deny 清单+每表状态存 static data+fail-fast）；n8n GitHub ★破 187,000
- **Langflow（API/容器化角度）**：Workflow API（点号寻址单组件覆盖）；Embed into site 聊天 widget；自定义组件容器化须放 /components 分类文件夹；向量存储组件含 Graph RAG 遍历；LangSmith 集成（LANGSMITH_TRACING）
- **Activepieces（piece 管理角度）**：piece 两级管理（Platform/Project）；官方 pieces=标准 npm 包 registry 每小时自动同步；步骤 pin 版本；私有 piece CLI build+tgz 上传；凭据 256-bit 加密+无读回 API；worker 分离+AP_EXECUTION_MODE=SANDBOX_CODE_ONLY；Pulumi AWS 部署
- **Make（AI Toolkit/认证角度）**：AI Agent fallback connections+审计日志 MCP 工具；Make AI Toolkit 取代 AI Tools（Free/Core 用托管 provider，Pro+ 自带 key）；Authenticated Webhooks 认证内置；Zendesk 新连接 OAuth refresh（旧 2026-04-30 过期）；凭据 API v2 简化
- **Pipedream（多触发器/组件角度）**：多触发器（单流任意数量入口）；并行执行步骤并发；Hooks=组件生命周期自动调用（webhook 订阅自动创建）；Sources=独立资源（props 收输入+URL 声明式部署 action=create&key）；Filter 规则构建器（布尔/分组/嵌套）；Workflows and String 2027-03-31 关停
- **Anthropic（上下文工程角度）**：Claude 5 提示瘦身（80% 删除无损失+claude doctor）；服务端压缩（context_management+instructions 自定义总结提示词）；缓存布局（静态前置 ephemeral+动态后置）；Opus 5.5 缓存读价 5%；研究任务提示（清晰成功标准+多源验证）
- **skills.sh 生态（排名统计角度）**：agentskillslist（4,060 技能下载排序+ClawHub downloads）；Linkly WIS 评分（人气/动量/信誉/维护/信任合成）；agent-browser 105 万安装（浏览器技能=最高需求实证）；SkillMD 下载榜（orchestrator-agent 第一）；Skillselion 84,819 工具目录+MCP 可调用（npx skillselion-mcp）；OpenAgentSkill 信号 0-100
- **GitHub 生态**：TencentDB-Agent-Memory（团队级记忆→对话记忆/技能/Wiki/CodeGraph 四类资产，27,693★）；claude-mem（近 10 万★+662/日，多宿主：Claude Code/Codex/Gemini/Copilot）；Agent 开源全景五层（90% 项目只在五层打转，OpenManus 5.8 万★）；Dragon Brain（MCP 持久记忆+知识图谱）；Octop（腾讯自托管多 agent）；openclaw-supermemory
- **deeplearning.ai（社区评估角度）**：静态评估集过拟合（华为云：每月轮换+冻结集）；多智能体=状态机（LangGraph 底层）；系统 prompt 不堆限制（模块化解耦分摊注意力）；小改动静默破坏（Datalaria：单短语→省略必填参数/无限重试）；评估平台生态成熟（数据集管理/评分器注册/CI gate/生产监控）

## 功能套件核查（⑦）

三核心套件本批无优化项；ponytail（继续观察）与 rtk（替代候选未授权）持续观察；skills.sh 官方 CLI 生态与 anthropics/knowledge-work-plugins 观察；新增观察：agent-browser（浏览器技能 105 万安装实证，对照 wb 浏览器类技能方向）、claude-mem（跨会话记忆多宿主，对照 wb-context-compressor 记忆域）。

## 垃圾清理（⑨）

删了什么：本批实拉全走 general_search，无本地临时文件落盘，未产生新垃圾。保留什么：*.bak 与全部核心产物（两 SKILL 文件 + r573A/r573B 留痕）；历史探针垃圾待删除通道可用时清理。
