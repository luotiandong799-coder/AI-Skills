---
name: ti-critical-reasoning
description: 因果推理与批判性思考（Thinking Intelligence）。当任务需要区分"相关"与"因果"、评估方案真实贡献、做反事实推演（"若当初换方案会怎样"）、识别 LLM 关联机误判因果时调用。基于 Pearl 因果阶梯、do-calculus、结构因果模型（SCM/DAG）、后门/前门调整。本技能是 TI 载体，补齐关联式推理的因果盲区。
module: TI
modules: TI,EI
---

# TI · 因果推理与批判性思考（Critical Reasoning）

> 本技能是 Personal AI OS 13 模块中 **TI（思考智能）** 的载体之一（与 `agent/ai-input-enhancement` / `grill-me` / `prompt-library-40` 同属 TI：输入增强 / 对抗性质询 / 提示词库 / 本技能=因果与反事实）。
> 方法论实拉（2026-11-07 实拉）：youonai.ai（do-operator / do-calculus）、probsee.com（Causal AI / SCM / DAG）、army.mil（Pearl 因果阶梯）、view.inews.qq.com（中文因果阶梯解读）。

## 一、为什么 TI 需要因果层

LLM 本质是关联机：它在海量含人类解释的语料上训练，学到的是 `P(y|x)`（看见 X 推测 Y），而非 `do(x)`（强制 X 后的效应）。部署去决策时，它用"观测装备"回答"干预问题"，常"自信且灾难性地"答错。Pearl 定位：缺 do-operator 的系统身处"两个不同世界"——被展示的世界与被要求行动的世界。

## 二、Pearl 因果阶梯

| 层级 | 名称 | 问题 | AI 现状 |
|---|---|---|---|
| 1 | 关联 Association | "看到 X，Y 如何变？" | LLM 强项（统计相关） |
| 2 | 干预 Intervention | "强制 X=x，会怎样？" | 需 do-calculus；RL/agent 可部分达到 |
| 3 | 反事实 Counterfactual | "若当初 X 不同，Y 会怎样？" | 最弱，需机制假设 |

层级严格递进：仅靠增加低层数据量无法获得高层推理能力。

## 三、do-operator 与 do-calculus

- **do(X=x)**：切断所有指向 X 的箭头，强制 X=x，模拟外部干预。
- **P(y|do(x)) ≠ P(y|x)**：前者是干预分布（去掉混杂），后者是观测条件（含混杂）。
- **do-calculus 三规则**判定：给定因果图与假设，"干预效应能否从观测数据识别"。可识别则无需做实验；不可识别则再多观测数据也无用——这是信息逻辑的边界，非技术局限。

## 四、结构因果模型（SCM / DAG）

- 有向无环图（DAG）表达变量因果结构；函数 `Y = f_Y(父节点, 噪声)`。
- **后门调整（back-door）**：阻断混杂路径估计因果效应。
- **前门调整（front-door）**：当混杂不可观测但存在中介时，经中介估计。
- 局限：依赖"正确因果图"，而图本身是易错的人类判断——但 do-calculus 逼你把假设摆上台面供批评，正是对大模型不可检假设的纠正。

## 五、在 Agent 工作流中的用法

1. **方案评审**：问"这是相关还是因果？"——某改动"伴随"指标改善 ≠ "导致"改善；先找混杂（同期还有别的变化吗）。
2. **反事实推演**：决策前跑"若当初选 B 而非 A，预期差多少"，用 DAG 标注可观测/不可观测。
3. **复盘升级**：RI 的根因分析补因果层——5 Whys 到机制层后，再用 do-calculus 判"该干预是否真能消除故障"。
4. **警惕自己**：Agent 复盘时易把"训练语料里见过解释"当"自主建立因果"，须显式标注证据层级。

## 六、与 OS 协作

- **DI** 方案对比：用反事实给各选项预期效应排序。
- **EI** 执行后：用因果层判"步骤成功是因其做对，还是巧合/混杂"。
- **RI** 复盘：根因从"相关"升到"因果"，行动项更可能对准真因。
- **VI** 验证：因果声称须有一手/独立源，禁把相关当因果声称。

## 七、来源（2026-11-07 实拉）

- youonai.ai/fieldguide/high/the_do_operator（do-operator / do-calculus / 三规则）
- probsee.com/p/Causal_AI（Causal AI / SCM / DAG / 后门前门调整）
- army.mil/article/270910（Pearl 因果阶梯 / AGI 视角）
- view.inews.qq.com/a/20260809A0ACUC00（图灵奖得主 Pearl 因果阶梯中文解读）
