# 2026-09-19 学习轮 r82 批（32 轮 · 工程类 · 第二波）

来源（本波 8 页）：LangChain tools/custom-middleware(死链)、AutoGen Swarm、LlamaIndex RAG、CrewAI crews、charonhub（DeepLearning.AI The Batch）、learn.deeplearning.ai、n8n langchain 目录。

## 本批独点（并入 wb-execute-discipline 2.21.0 → 2.22.0）
1. **ToolRuntime 注入面**：工具经 runtime 访问 State/Context/Store/StreamWriter/ExecutionInfo(thread/run/attempt)/ToolCallID，对模型隐藏；工具改 state 走 Command；**LLM 并行工具调用更新同一字段需 reducer**；config/runtime 为保留参数名。
2. **Swarm 交接 + 并行交接陷阱**：HandoffMessage 驱动发言人切换、全 agent 共享上下文、无中央编排；**交接类动作禁止并行**（并行 tool calling 产生多 handoff）；交接给 user 即暂停恢复。
3. **三个 LLM 槽分离**：function_calling_llm（工具调用专用）/ planning_llm（规划）/ 主 LLM（执行）——按职能分槽，工具调用用快模型、规划用强模型。

## 判重说明
- return_direct（LangChain tools）→ r73 已入；swarm 编排模式 → r75 已入（本条补交接机制增量）；并行写守卫 → ed 已有（本条补 LLM 并行调用合并语义增量）；计划器前置注入 → r75 已入（本条补 planning_llm 独立槽增量）。
- 无独点：LlamaIndex RAG 五阶段/检索组件（ctx 系已覆盖）、n8n cluster nodes 目录、learn 平台 UI 指南。
- 死链：LangChain custom-middleware（LangChain 4→5）。

## 观察位
- charonhub：Meta「记忆替身」——独立记忆进程观测步骤流、每 N+1 步更新记忆库并决定是否提醒主 agent（ctx 系记忆架构，按用户指令"工程类"不深落，记观察位）。

## 版本变更
- ed 2.21.0 → **2.22.0**（3 条）
