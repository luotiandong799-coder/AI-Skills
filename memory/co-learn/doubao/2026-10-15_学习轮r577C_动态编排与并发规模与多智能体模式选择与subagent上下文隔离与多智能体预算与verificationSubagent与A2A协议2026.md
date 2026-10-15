# 2026-10-15 学习轮 r577C：Agent 编排与多智能体 / 上下文管理

主题：AI 技能库工程与方法论 + AI 智慧进化（硬锁）
轮次：r577C（本次触发批 r577 之第 3 轮，共 3 轮连跑）
判重基准：WB r575/r574/r573/r572/r571；doubao r577A（6 章）+ r577B（6 章）+ r576A/B/C（18 章）+ r575A/B/C

## 十站实拉（全量逐站，带来源）

| 站 | 实拉要点 | 来源 |
|---|---|---|
| Dify | Supervisor mode 多智能体编排（协调 agent 委派给专门子 agent）；嵌套 agent 节点（agent 作为工具调用另一 agent）；ReAct 回退（无 Function Calling 模型） | dify docs + dev.to + ai-solutes |
| n8n | Supervisor-Worker 内建；orchestrator 按 JSON 输出用 Switch 路由到 Worker；Merge wait-for-all 收集并行结果再合成；confidence-based 路由+人工回退；Manager-Worker 轻模型省钱 | n8n workflows + aiagentvn + ai-rockstars |
| Langflow | 多智能体流（Supervisor→Research/Code/Writer）；planner-executor 隔离子任务防上下文过大；LangGraph 原生集成有状态循环 | langflow.org + explainx + CUGA |
| Activepieces | 协调式多智能体（flows 内编排 agents/actions/human steps）；MCP 暴露每个集成让 Claude/Cursor 直接调用；approval steps 人控 | activepieces.com + agenticindex |
| Make | Sub-Agents（agent 作为工具装进另一 agent，无硬编码交接）；编排 agent 选专家返回结果；多模型路由（轻模型分类、重模型起草）；Opus 协调+Sonnet 执行 | make community + blog |
| Pipedream | 拓扑先于代码（顺序确定→chain with gates；需并行单协调点→hierarchical orchestrator-worker；条件分支/并行合并/回路→DAG 先设计）；verifier/critic loop；event-driven reactive | algofuse + build5nines + ai.blocksize |
| Anthropic Skills | 动态编排（lead agent 规划+写编排程序，1000 agents/run 64 并发）；orchestrator-subagent vs agent teams 选择；verification subagent；先单 agent 再协调；每 agent 三预算（turns/cost/time） | claude.com/blog + dev.to + ai-portal |
| skills.sh | superpowers 20+ 技能库把工程跑成 pipeline；parallel executor（依赖图感知、部分失败处理）；compositional skill routing（defer_loading 按需加载工具） | top-agent-skills + agentndx + agentpatterns |
| GitHub 生态 | LangGraph 生产标准（有状态图+checkpointer）；CrewAI 58k★ 角色制；80% 实现时间耗在数据工程与治理；A2A 跨框架协议；Agent teams 跨会话协作 | atlan + dev.to + the-agent-report |
| deeplearning.ai | CrewAI 多智能体课程（memory/tools/guardrails/execution hooks；Flows 编排；LLM-as-Judge 评估）；A2A 课程（每 agent 包 A2A server）；ACP（跨框架通信）；AutoGen 对话模式 | learn.deeplearning.ai |

## 落地（execute 3.100.0→3.101.0 / compressor 3.697.0→3.698.0，各 +3 章）

| 文件 | 新增章节 | 提升层 |
|---|---|---|
| wb-execute-discipline 3.101.0 | 动态编排与并发规模（Claude 决定结构生成编排程序；1000 agents/64 并发；parallel executor 部分失败只重试失败项） | 工具/工作流 |
| wb-execute-discipline 3.101.0 | 多智能体模式选择判据与何时避免并发（orchestrator-subagent vs agent teams；避免并发四条件） | 可复用 Skill/工作流 |
| wb-execute-discipline 3.101.0 | sub-agent 上下文隔离与 hand-off 接口（fresh context/scoped task/tangible result；严格 schema 交接权重） | 可复用 Skill/工作流 |
| wb-context-compressor 3.698.0 | 多智能体预算与模型分级（每 agent 三预算 turns/cost/time；15x 成本判据；Opus 协调+Sonnet 执行） | 工作流/可复用 Skill |
| wb-context-compressor 3.698.0 | verification subagent 模式与更强协调模型（专职验证者；强 orchestrator 可省验证步；critic loop） | 可复用 Skill/工作流 |
| wb-context-compressor 3.698.0 | A2A 协议与跨框架协作（A2A vs MCP 分工；ACP 跨框架互通） | 可复用 Skill/工作流 |

## 判重说明（增量判定）

六点均含独有增量：动态编排（结构生成/1000-64 规模数字）未见于前批；parallel executor 部分失败处理（保留成功只重试失败）未见于前批；模式选择判据（orchestrator-subagent vs agent teams 按任务形态）与避免并发四条件在 §五种编排模式基础上为独有增量；sub-agent 三要素（fresh context/scoped task/tangible result）与 hand-off 接口权重（接口比聪明度重要）在 §接口契约基础上为独有增量；agent 三预算与 15x 成本判据未见于前批（§成本四层是输出侧，本条是多智能体配额）；verification subagent 与 critic loop 在 §质检-回退基础上为独有增量（函数 vs 专职 subagent）；A2A/ACP 跨框架协议未见于前批。

## 功能套件核查（⑦）

wb-ponytail / wb-max-token-saver / wb-context-compressor：本轮 compressor +3 章（多智能体预算/verification subagent/A2A）增强编排与成本覆盖；execute +3 章（动态编排/模式选择/上下文隔离）增强执行纪律；ponytail 与 token-saver 无对应增量，暂不迭代。

## 清理（⑨）

删了什么：无（全程 general_search 实拉，无本地临时文件落盘）。保留什么：*.bak 与全部核心产物（两 SKILL.md + 三份留痕）。

## 批内备注

git commit/push 因通道缺失挂起（累计 r546→r577C 共 36 批，含本批），不重试、不启 VPN、不补推。
