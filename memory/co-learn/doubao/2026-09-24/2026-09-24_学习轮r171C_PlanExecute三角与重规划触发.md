# r171-C Plan-and-Execute 三角与重规划触发：省 40-60% 上下文、启发式触发、循环检测

实拉时间：2026-09-24 20:10
信源：aipatternbook plan-and-execute / openlegion 西英双语 agentic patterns / dreaming.press ReAct vs P&E vs Reflexion / callsphere loop patterns / dev.to ljhao / jatinbansal planning vs reactive / bestaiweb / 00011000 / CSDN 动态Replan / zylos.ai adaptive replanning / genai4a11 / aiagents.codeguides.io / codemia replan heuristics / dataaihub replan 上限 / theneuralbase replan loop 循环检测 / xbstack / llmversus（规划组，满 10 站）

## 实拉证据（关键原文）
- aipatternbook：「the planner sees the goal, the executor sees one step plus context」；re-planner 与 planner 同类模型、**稀疏调用**——只在该重规划时用。
- openlegion：「Plan-and-Execute separates a Planner agent from Executor agents, reducing context window consumption by approximately 40–60% on long-horizon tasks compared to ReAct」；「the plan is a discrete text artifact that can be policy-checked before any tool call is made——automated review for prohibited actions」。
- codemia：「after every step adds latency and cost. Production systems use heuristics: Step failure → always replan; New information contradicts a plan assumption → replan; On schedule, nothing surprising → continue without replanning.」
- dataaihub：「if replan_count >= 2: return Unable to complete task after multiple replans」——重规划次数上限。
- theneuralbase：「compute similarity to prior iterations' observations: if similarity > 0.9 (agent is in a loop), force tool pivot or escalate」；「async tool execution: batch all planned tools into one execute call…cuts the loop cycles from 10 to 3」。
- dreaming.press：「ReAct and Plan-and-Execute are the two ends of one axis—how much the agent commits before it observes the world」；P&E「goes stale—so production versions bolt on a re-plan step that drags it back toward ReAct」。

## 独点清单（3 个真独点）

### 独点1：Planner/Executor/Re-planner 三角——executor 只看一步，上下文省 40-60%；计划是可预审工件（工作流层）
- 判据：planner 看目标、executor 只看当前一步+上下文（不背全计划）、re-planner 稀疏调用（与 planner 同类模型，只在计划失效时用）。长任务 vs ReAct 省 40-60% 上下文。计划是**离散文本工件**：工具调用前可自动策略检查（禁止动作/越权操作），人类可在昂贵工作开始前审计划。
- 独有增量（与 wb-execute-discipline「多 Agent 协作纪律·五种编排模式」区别）：那条管多 agent 怎么协作；本条管**单 agent 内部规划-执行分离**的三角结构与上下文节省机制，且计划可预审是独有动作（防违规前置）。
- 提升层：工作流。

### 独点2：重规划三触发启发式 + 次数上限——每步重规划是浪费（工作流层）
- 判据：生产系统用启发式决定何时重规划，不是每步都重规划：①步骤失败（工具错误/意外结果）→必重规划；②新信息与计划假设矛盾（文件结构不同/依赖缺失）→重规划；③按预期完成且无意外→继续，不重规划。同时设重规划上限（如 replan_count ≥2 未完成→放弃并说明），防止重规划死循环烧钱。
- 独有增量：已有条目讲"失败回退"（wb-execute-discipline 失败回退机制=路径错了换路径）；本条给出**重规划的精确触发条件与停止条件**（哪些情况必须重规划、哪些不重规划、重规划几次封顶）。
- 提升层：工作流。

### 独点3：循环检测：观察相似度 >0.9 强制换工具；异步批量工具执行砍循环轮数（工具层）
- 判据：每轮执行后把观察+目标嵌入，与历史迭代算相似度——>0.9 说明 agent 在打转（同一状态重复观察），强制换工具或升级人工；把多步计划中的工具**一次批量发**（Promise.all 式）再统一规划，循环轮数可从 10 砍到 3。
- 独有增量：wb-execute-discipline「工具循环查终止条件」管 stop_reason 防死循环；本条是**基于语义相似度的循环检测**（状态级，不只是 stop_reason）+ 批量并行的优化手段。
- 提升层：工具。

## 判非重复理由
- 与 r170-A RAG / r170-B 成本 / r170-C judge 无重叠；与 wb-execute-discipline 多 Agent 协作/失败回退/循环终止为互补增量（分别管协作形态/路径失败/单工具循环 vs 本条规划分离/重规划触发/状态级循环）。
- ReWOO/LLMCompiler/Reflexion 细节多源重叠 >60% 只留证据。
