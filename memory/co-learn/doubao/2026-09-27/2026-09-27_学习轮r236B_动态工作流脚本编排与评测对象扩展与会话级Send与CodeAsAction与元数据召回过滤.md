# r236-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | 智谱 ZCode（changelog/docs） | ✓ | 3.14.0 动态工作流（单脚本编排多 sub-agent）；3.14.3 运行中直接调并发不停止+复用逻辑优化；ZCode Agent 统一工作流（tasks/context/permissions/file refs/Review）；飞书/微信 bot @触发远程推进；Goal Mode 完成验证+状态恢复；GLM-5.2+ZCode 通过率高于 Claude Code 组合 2.39%（跨文件跨进程场景）；缓存命中优化配额 +30% |
| 2 | deeplearning.ai（courses/community） | ✓ | Evaluating AI Agents（Arize：Lab 3 加 router 和 skill 评估；系统化评估迭代）；Building and Evaluating Data Agents（GPA 度量/多 agent 工作流/观察性能）；Agent Memory（Oracle：extraction/consolidation/self-updating 三操作）；新课程 Gen UI 交互 agent+vLLM 推理；Agentic AI 四模式 |
| 3 | deepseek-plugin.org/Harness 生态 | ✓ | Everything is a plugin（模型/工具/技能/会话/沙箱/存储/循环/调度/UI 全可换，Cordis services+events 协作）；findharness 7017 插件/dshmarketplace 8978（99% 沙箱实测可装）；Memory Body 记忆单元（命名/跨会话/隔离/可挂载）；swarm_batch 批量并行子 agent 调度插件 |
| 4 | agentskills.io/agentskillslist | ✓ | Top 4061 skills 快照：#01 Self Improving Agent 480.6K downloads（捕获学习/错误/纠正持续改进，触发=命令失败/用户纠正/请求不存在能力/API 失败）；agentskills 规范 40+ 工具跨平台（Anthropic 2025-10 起源）；anthropic-cybersecurity-skills 754 skills 五框架映射（MITRE ATT&CK/ATLAS/NIST CSF 2.0）；OpenAI 关闭自家 catalog 社区目录补位 |
| 5 | WaytoAGI | ✓ | Claude Agent Skills 蓝皮书（五篇二十章：Skill 是给普通人最好的礼物→Agent Team→自动进化）；6 阶段 Agent 学习路线（评测 Ragas/Arize Phoenix 自动化测试集；可观测 LangSmith/LangFuse 每步耗时 token；防 prompt injection 安全）；Skill=工具箱+岗位 SOP 手册（目标/流程/工具/知识/约束/验收封装） |
| 6 | docs.openclaw.ai（agent-loop/session-tool/subagents/tasks） | ✓ | Agent loop=序列化 per-session（intake→context assembly→inference→tool execution→streaming→persistence）；session tools（sessions patch/reset/sessions_send 同 gateway 跑另一 session/conversations_send 发外部会话不跑本地）；sub-agents 独立 session 默认 announce 回审+每个 run 是 background task；会话行存 per-agent SQLite |
| 7 | Make（2026-09 help） | ✓ | 官方 ChatGPT plugin（2026-09-09：ChatGPT 自然语言创建管理 make 自动化，连接/调度/执行历史/结果同步）；Make AI Toolkit（简化 MCP token 创建——API/MCP token 不再区分）；MCP Server/Client（scenario 变 tools 供 Claude/GPT/Cursor；MCP Client 安全调用外部 tools）；Claude Opus 5.5/Gemini Omni 1.1 flash 支持 |
| 8 | Hugging Face（smolagents/ml-intern） | ✓ | smolagents VLM 视觉支持（agent 看网页内容决策点击/导航）；ml-intern 自动化研究 loop（论文→引用→GPU 沙箱→迭代）；1000 行 agent loop 哲学（不需要 planner/router/memory 模块/50 类层级）；code-as-action vs JSON schema（动作即代码提高推理上限）；语义崩塌/间接注入→GraphRAG+code-as-action |
| 9 | ModelScope（魔搭） | ✓ | 创空间部署 Skill（Gradio/Streamlit/Docker/静态站+代码同步+日志监控+明文密钥管理+自动诊断修复）；魔粒体系激励积分；Offering 服务墙技能变现；Agents-A1（35B 达万亿参数性能+开源 agent 评测框架 tool use/多步推理）；阿里云 AgentLoop 观测商业化（Coding Agent 质量守护 Code Review 覆盖推理质量） |
| 10 | 腾讯元器/腾讯云智能体平台 | ✓ | 知识库元数据功能（2026-09：键值对关联文档问答，召回阶段元数据匹配关键实体提召回率，随知识喂模型）；Plugin Marketplace 基于已发布应用创建插件（应用→工具）；多智能体共享知识库（公众号矩阵一个库答所有号）；知识到期时间+文档生成 QA |

## 判重基准
双键检索：智谱（r235-B 已落 Goal 模式，本条独有增量=动态工作流脚本编排+运行中调并发+bot 远程触发）；deeplearning（r235-C 已落评测三支柱，本条独有增量=router+skill 纳入评测对象+GPA 度量）；OpenClaw（r235-A/B 已落 cron watch/Skill Workshop/编排，本条独有增量=sessions_send/conversations_send/sub-agent 默认回审）；HF（r235-C 已落 smolagents 多 agent 纪律，本条独有增量=code-as-action vs JSON schema+VLM 视觉）；腾讯元器（r235-A 已落 RAG 管线，本条独有增量=元数据召回过滤+应用转插件+共享知识库）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① ZCode 动态工作流 | 单脚本编排多 sub-agent；运行中调并发；bot 远程触发；统一任务/上下文/权限/Review | 工作流 | wb-execute-discipline |
| ② 评测对象扩展 router/skill | 不只评输出；Lab3 router+skill 评估；Data Agents GPA 分项归因 | 可复用 Skill | wb-execute-discipline |
| ③ OpenClaw 会话级 send | sessions_send 同 gateway 跑另一 session；conversations_send 外部投递；sub-agents 默认 announce 回审 | 工具 | wb-execute-discipline |
| ④ code-as-action | 动作即代码优于脆弱 JSON schema；1000 行最小 agent loop；VLM 视觉进 loop | 工作流 | wb-execute-discipline |
| ⑤ 元数据召回过滤 | 知识库键值对元数据召回前过滤；应用转插件复用；多智能体共享知识库 | 工作流 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：wb-ponytail/wb-max-token-saver/wb-context-compressor 三件套无新增更优替代；wb-context-compressor 可参照"元数据召回过滤"改进检索注入（下轮评估）。
- 垃圾：本轮未产生临时文件。
