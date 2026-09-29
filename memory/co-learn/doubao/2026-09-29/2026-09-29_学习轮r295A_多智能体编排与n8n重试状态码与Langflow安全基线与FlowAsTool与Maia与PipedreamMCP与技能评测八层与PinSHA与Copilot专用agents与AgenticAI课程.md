# r295A 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r295A 前 + WorkBuddy r294 续作（Cap29/30、变量可见域、提交粒度，ede6bb1 已 push）。查询词与既往全错开（本轮=Agent编排/错误处理重试/部署安全/AI Agent工作流/AI Agent场景/MCP server/评测测试/最佳实践/agent模式/Agent课程）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | 多智能体异构工具链编排（LLM Agent→Router→(Code Interpreter\|API Gateway\|RAG Node)→Aggregator→Response）/ 自动 Fallback 链路+状态持久化+跨 Agent 上下文同步 / AI Guardrails 内容审核集成（moderation 全量留痕） | 合并保留增量（r292B/r293A Dify，本点=编排模式+Fallback+Guardrails） | 工作流 |
| 2 | n8n | 可重试状态码清单（408/409/425/429/500/502/503/504 默认重试；400/401/403/404/422 不重试）+指数退避 jitter 公式（waitSeconds=min(maxDelay, baseDelay×2^attempt)）/ 节点级重试=同执行内只重跑该节点 / 整流程重试=从头开始（无 checkpoint） | 合并保留增量（r292A 重试分类/r294C 节点错误，本点=状态码清单+退避公式+重跑语义） | 工作流 |
| 3 | LangFlow | CVE-2026-33017 未认证 RCE 安全基线（CVSS 9.3，AUTO_LOGIN=false 生产硬约束+public flows 攻击面+/api/v1/build_public_tmp/ 端点；向量 collection 名=访问边界） | 合并保留增量（r293C 生产部署，本点=安全基线与攻击面） | 工具 |
| 4 | Activepieces | Flow-as-Tool（现有工作流变成 agent 可调工具）/ data masking（敏感细节不进日志） | 合并保留增量（r294C Chat-to-automation，本点=Flow-as-Tool+data masking） | 工作流 |
| 5 | Make | AI Agent (New) app 2026-02 发布（open beta）/ Maia 自然语言建/改场景（业务人员原型→IT 审查后上线） | 合并保留增量（r294C 官方插件，本点=Agent New app+Maia 流程） | 工具 |
| 6 | Pipedream | 单 MCP 端点 10K 工具/3K+ API + per-user connected accounts 认证 / sub-agent 配置模式（instruction 传 LLM 子 agent 配置主工具） | 合并保留增量（r294C REST 创建，本点=MCP 端点+sub-agent） | 工具 |
| 7 | Agent Skills 评测 | 八层评测架构（routing/确定性契约/轨迹/终态/语义质量/重复运行可靠性/成本/安全，不塌成模糊分）/ SkillTrustBench 安全基准（62,652 技能→5,520 用例 9 类威胁）/ 真实场景收益衰减证据（Opus 4.6 55.4%→38.4% 自主检索；Kimi/Qwen 被技能拖慢） | 合并保留增量（r293A caliper/r293B Skill Lift，本点=八层架构+安全基准+衰减证据） | 可复用 Skill |
| 8 | skills.sh | Pin to SHA 供应链卫生（owner/repo@<sha> 钉 commit，默认 main 会变）/ 五窄技能>一大而全 / 负面示例写法 / Skill Packs 团队工具定义共享 | 合并保留增量（r293A CLI/r294C API，本点=Pin SHA+负面示例+Skill Packs） | 可复用 Skill |
| 9 | GitHub Copilot | 专用 agents 生态（@debugger 调用栈/变量状态系统排错、@git 审未提交改动、@modernize 感知项目图升级、@profiler、@test）/ agent profile 文件化（.github/agents/*.agent.md=技能即文件） | 合并保留增量（r293B/r294C Copilot，本点=专用 agents+profile 文件化） | 工具 |
| 10 | deeplearning.ai | Agentic AI 课程（反射/工具/规划/多 agent 四大设计模式+degrees of autonomy）/ Agent Memory 新课（长期记忆=模型外持久结构化一等基础设施） | 合并保留增量（r293A 记忆/r293C 生成式UI，本点=Agentic AI 课程+记忆基础设施） | 可复用 Skill |

判重口径：增量判定。本轮 10 合并保留增量，零纯重复。