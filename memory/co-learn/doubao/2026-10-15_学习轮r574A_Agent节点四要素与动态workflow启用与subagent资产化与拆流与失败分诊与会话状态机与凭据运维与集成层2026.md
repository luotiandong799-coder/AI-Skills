# 学习轮 r574A（2026-10-15 · AI 技能库工程与方法论 + AI 智慧进化）

十站实拉（全量逐站，r574 批第 1 轮，角度与 r573 批错开）：Dify（agent 编排/会话状态角度）/ n8n（版本/凭证/错误处理角度）/ Langflow（memory/会话角度）/ Activepieces（版本/回滚/发布角度）/ Make（MCP/连接器/API 角度）/ Pipedream（MCP/战略角度）/ Anthropic（hooks/subagents/动态 workflow 启用角度）/ skills.sh 生态（CLI/管理工具角度）/ GitHub 生态（周榜/技能包角度）/ deeplearning.ai（其他课程角度：agentic 模式/数据 agent/事件驱动）。判重基准：execute 3.89.0（r573 批 9 章）+ compressor 3.686.0（r573 批 9 章）+ r572 批 18 章 + 更早批次 + WB 留痕。

## 落地（execute 3.89.0 → 3.90.0，+3 章）

1. **Agent 节点参数四要素与动态工作流启用：工具描述/迭代上限/指令/记忆 + multiagent 字段开启**（来源：Dify Docs 2026-08-27 + AIgent Lab 2026-05-17 + Claude Platform release notes 2026-10-09）
   - New Agent 节点四要素：工具描述清晰/迭代上限防 runaway/指令含角色目标约束/记忆与 token 平衡
   - 动态工作流启用：multiagent 字段设 {"type":"multiagent_20261001","workflows":{"type":"enabled"}} + system prompt 指导何时启动执行
   - **提升层**：工具 / 工作流

2. **Subagent 文件化资产与 hooks 事件自动触发：frontmatter+正文按需加载 + commit 前审查/安全检/质量门**（来源：Claude Blog Steering 2026-06-18 + Subagents 2026-04-07）
   - subagent=markdown 文件（YAML frontmatter+正文作 system prompt；正文大上下文不自动调用）
   - hooks=事件自动触发子代理任务（每次 commit 前自动审查/安全检/CI 式质量门），无需手动调用
   - **提升层**：可复用 Skill / 工作流

3. **Convert to sub-workflow 与失败分诊：一键拆大流 + LLM 分类 transient/logic→retry API 或工单**（来源：n8n Release 2026-06-25 + n8n Workflow 2026-07-08）
   - Convert to sub-workflow：大流一键拆子流（免手拷节点重连）
   - 失败分诊：execution errors→Anthropic 分类 transient/logic→transient 调 retry 端点、logic 转 Jira
   - **提升层**：工具 / 工作流

## 落地（compressor 3.686.0 → 3.687.0，+3 章）

1. **会话记忆与状态管理：session_id 隔离 + 对话状态机三段式 + 记忆库资源化**（来源：Langflow 2026-10-04 + Memory bases 2026-09-21 + 技术栈 2026-08-09）
   - session_id 隔离（多用户跑同一 flow 必须自定义 ID）；对话状态机（LLM 分析→Code 推进/回退/越界钳制→Assigner 持久化）；记忆库资源（preprocessing 指令+ChromaDB 落盘+ingestion 状态）
   - **提升层**：可复用 Skill / 工作流

2. **凭据与密钥运维：凭据备份自动化 + 凭据部分更新 API + 环境迁移前置**（来源：n8n 2026-02-14 + n8n Release 2026-05-20 + Activepieces 2026-10-09）
   - 凭据备份=export+哈希变更检测；凭据部分更新=isPartialData 合并（密钥轮换不删建）；迁移前置=平台级 SERVICE principal key+同 project id 格式+同 major 版本
   - **提升层**：工具 / 可复用 Skill

3. **集成层与激活溯源：托管认证批量接入 + 技能激活状态溯源 + gh skill CLI 入口**（来源：RECATOOLS 2026-10-01 + skill-cli 2026-07-18 + GitHub CLI 2026-04-19）
   - 托管认证集成层（3,000+ 连接器/10,000+ 工具给 agent）；激活状态 source 列（global/global·off/project/被动，派生自 active+isDefault）；gh skill=GitHub CLI 原生技能管理
   - **提升层**：工具 / 可复用 Skill

## 十站实拉要点（逐站留痕，与 r573 批角度不同）

- **Dify（agent 编排/会话状态角度）**：New Agent 节点（v1.16.0 beta，agent 作工作流一步）四要素；agent 可独立或作节点入工作流；多智能体协同六项（自动 fallback 链路/状态持久化/跨 agent 上下文同步）；对话状态机三段式（LLM 分析→Code 推进回退越界钳制→Assigner 持久化）
- **n8n（版本/凭证/错误处理角度）**：Convert to sub-workflow 一键拆大流；失败分诊（Anthropic 判 transient/logic→retry API 或 Jira+OTel）；GitHub 版本控制部署（双凭据：本地读+生产写）；凭据备份自动化（export+哈希变更检测）；API 更新凭据（PATCH isPartialData 合并，密钥轮换）
- **Langflow（memory/会话角度）**：chat memory 按 session_id 分组（多租户须自定义 ID）；Message History 组件（内置记忆够用优先，专用库 Mem0/Redis 按需）；Memory base（preprocessing instructions 前置+ChromaDB+ingestion 状态）；thread=持久会话容器（跨 run 保持状态）
- **Activepieces（版本/回滚/发布角度）**：flow 回滚三方式（Quick/Review/Gradual）；Git 同步发布（From Git/From Project→三操作：更新/删缺失/新建）；Project Replace CLI 前置（SERVICE principal key+同 major+目标≥源）；AI Agent 上线变更控制（双轨回放+关键任务专项+三分类+灰度门槛）
- **Make（MCP/连接器/API 角度）**：Make MCP server（scenario 包装成 MCP 工具给 Claude）+Make 自身 MCP client（Execute an action with AI）；内置连接器 on Claude（免手配 URL/token）；OAuth 2.0 通用 HTTP 调用（Authorization Code+scope 空格分隔）；四内置函数（arrayDiff/arrayIntersect/set/escapeJSON 省模块）
- **Pipedream（MCP/战略角度）**：MCP 升级（OAuth+ChatGPT 支持；MCP Chat 与所有工具对话）；并行 LLM 查询（互不依赖查询并行+父流引用响应）；战略转向=Connect 集成层（3k 连接器/10k 工具托管认证给 agent）；Workflows 2027-03-31 关停（凭据/OAuth 数据 2027-04-30 删）
- **Anthropic（hooks/subagents/启用角度）**：动态 workflow 启用配置（multiagent 字段+system prompt 指导启动时机）；subagent=markdown 文件（frontmatter+正文作 system prompt，按需加载）；hooks 事件自动触发（commit 前审查/安全检/CI 质量门）；agent harness 三模式（agent 是"长出来的"）
- **skills.sh 生态（CLI/管理工具角度）**：skills CLI 命令集（find/add/check+--skill/-g/-a/--full-depth）；skill-cli source 列（激活溯源：global/global·off/project/被动）；gh skill（GitHub CLI 内置技能管理）；skill-scaffold（openclaw 2026-09-28，多宿主技能骨架生成）
- **GitHub 生态（周榜/技能包角度）**：第 40 周趋势=技能包成核心复用单元（mattpocock/google/anthropics/awesome-claude-skills 霸榜）；claude-mem（会话全捕获→AI 压缩→注入未来会话）；marketingskills（2026-10-03，53,102★，50+ 营销技能）；awesome-claude-skills 77k★
- **deeplearning.ai（其他课程角度）**：Agentic AI 四模式（Reflection/Tool Use/Planning/Multi-Agent）+构建顺序（reflection→tool→evaluation→multi-agent）；Data Agents（planner/executor/专用子代理+goal-plan-action 对齐评估+内联评估调计划）；事件驱动文档工作流（RAG+人在环填表）；多智能体部署（zoom-in/zoom-out 监控+LLM-as-Judge）

## 功能套件核查（⑦）

三核心套件本轮无优化项；新增观察：Convert to sub-workflow（大流拆子流，对照 execute 的流级治理）、失败分诊（LLM 判 transient/logic，对照 §重试分类）、goal-plan-action 对齐评估（对照 compressor 的评估维度）、claude-mem（会话捕获-压缩-注入，对照 compressor 记忆流水线）。

## 垃圾清理（⑨）

删了什么：本批实拉全走 general_search，无本地临时文件落盘，未产生新垃圾。保留什么：*.bak 与全部核心产物（两 SKILL 文件 + r574A 留痕）；历史探针垃圾待删除通道可用时清理。

## 信源健康度

无删源无加源；Flowise 已删除不拉；打不开自动开桌面 VPN（本轮未触发）。commit/push 挂起（git 通道持续不可用，累计 r546→r574A 共 26 批）。
