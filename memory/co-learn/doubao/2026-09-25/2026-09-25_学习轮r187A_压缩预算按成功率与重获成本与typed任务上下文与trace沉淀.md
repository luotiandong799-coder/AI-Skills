# 学习轮 r187-A：压缩预算按成功率定与重获成本测量与typed任务上下文与trace沉淀skill（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai agent node | 404，留痕 |
| 2 | docs.n8n.io retry-on-fail | 死链 |
| 3 | pipedream suspend | 死链 |
| 搜索 | context engineering 2026 | OK：agentpatterns/openlegion/dev.to |
| 4 | deeplearning.ai/short-courses | OK：新课单 Building Adaptive AI Agents/Spec-Driven/API discovery KG |

## 独点（4 个）
### A1：压缩预算按任务成功率定，不按 token 压缩率定（来源：agentpatterns.ai/context-engineering）
- 常驻指令能压多短，从"环境验证的任务成功率"反推，不是拍一个"压掉 50%"的比率；压缩时保持语义块整体，不把一个完整规则切碎成半句。
- 判据：**压缩目标是成功率不掉，不是 token 好看**——压过头任务崩了再松回来；与 §压缩只付在本次变更范围 互补——那条管"不许偷删无关段"，本条管"压多少才算到位"。
- **提升层**：可复用 Skill（context-compressor）。

### A2：压缩下的"重获成本"测量——工具调用拆 retrieval vs execution（来源：同上）
- 把 agent 的工具调用分成 retrieval（拿信息）和 execution（真动作）两类，单独算压缩后重获信息的交互成本；扁平任务描述会把这两类成本混在一起。
- 判据：**压缩省的 token 和重获花的轮次要一起算**——把检索类工具结果压太狠，后面要多调几次工具补，总成本反而高；只压 execution 无关的冗长回显。
- **提升层**：可复用 Skill。

### A3：Task Context 显式 typed，不埋自由对话（来源：dev.to production context 2026）
- 工作流的当前状态用结构化字段显式传入：goal text / tenant id / user id / product account id / 当前节点 / 要求输出类型——不要只散在对话历史里让模型自己找。
- 判据：**长流程里"当前在哪一步"必须是显式字段**，否则模型每轮都要从对话里重新推断，错一步后面全偏；与 trace_id 互补——那条管一次请求跨重试串联，本条管单次执行内的状态显式化。
- **提升层**：工作流。

### A4：跑完的 agent trace → 人工审批 → 沉淀为 reusable skill（来源：deeplearning.ai 新课 Building Adaptive AI Agents，Oracle）
- agent 每次跑完产出 trace，流水线把 trace 转成可复用的 skill，**人工审批后入库**；另配 code knowledge graph 提升大代码库检索。
- 判据：**经验从"记日志"升级成"沉淀成技能"**——与 wb-debug-loop（按错误签名记修复路径）和学习留痕互补：那条记错误，本条把成功执行路径也沉淀成下次可直接调的 skill；人工审批这步防垃圾经验入库。
- **提升层**：可复用 Skill / 工作流。

## 判重说明
- openlegion"工具结果用便宜小模型先提取再 append"→ 工具结果断言/提取已覆盖，只取 A1/A2 增量。
- 深课单里 Long-Term Memory with LangGraph/LangMem、On-Device Memory 与记忆类已有，不落。
- r186 已记 @不读全文/可视化/NO_INGEST，不重复。
