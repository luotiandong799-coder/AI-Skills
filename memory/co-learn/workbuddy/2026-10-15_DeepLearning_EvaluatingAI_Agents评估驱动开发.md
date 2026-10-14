# 今日 AI 学习（DeepLearning.AI 每日学习轮 · 2026-10-15）

## 1. 今日最值得学习
- 课程：DeepLearning.AI × Arize AI《Evaluating AI Agents》（John Gilhuly / Aman Khan，2026-07 更新，2h36m，15 课）
- 章节：Evaluation-driven development、Decomposing agents、Tracing（OpenTelemetry/Phoenix）、Router+Skill evals（code-based / LLM-as-a-Judge / human）、Trajectory evals + convergence score、Structuring experiments、Improving your LLM-as-a-Judge、Monitoring in CI/CD
- 学习时间：2026-10-15 00:33–00:50（本轮手动触发，非 11:00 静默批）
- 为什么今天学：共学台账对「LLM-as-a-Judge / 收敛分数 / 评估驱动开发 / 三层分解」近乎零覆盖（grep 全 0 命中），属真实缺口；且直接补益 WB 已有的 `wb-agent-evaluation` 技能（ae 1.22.0）。
- 和以前内容的区别：以前多学「各 Agent 框架怎么评」（工具层），本课给的是**结构化评估方法论**（飞轮 + 三层分解 + 收敛度量 + 评委校准纪律），是上层范式，非具体工具。

## 2. 今天新增知识
- **评估驱动开发（evaluation-driven development）飞轮**：用 agent 自身的评测指标指导改进投入，形成「开发→生产」的度量飞轮；评测不是收尾动作，而是贯穿开发的反馈回路。
- **三层分解评估**：① router 评估（工具/路由选择是否正确，代码类检查如 function-calling 合法性、SQL 正确性）② skill 评估（每个技能输出质量）③ trajectory 评估（步骤序列效率、是否出现无效循环）。
- **收敛分数（convergence score）**：衡量 agent 对给定输入走「最优路径」的频率，0–1 标度；trajectory 效率的客观代理指标。
- **LLM-as-a-Judge 校准纪律**（agentpatterns + 本课 Lesson13 互补）：judge 须 ≥ 被测系统；rubric 冻结不可改（改了旧分不可比）；上线前 vs 人工校准 **Cohen's kappa ≥ 0.6**；低温度；定期重校准防漂移；A/B 配对比较比绝对分更可靠。
- **改进你的评委（improving-your-judge）**：用实验（experiments）提升评委准确率，用语义相似度做横向比较。
- **生产监控 + CI/CD**：评测技术下沉到生产监控、CI 门禁、自改进 agent；eval gate 替代传统单测。

## 3. 核心知识（可复用规则/思维）
- **评测 ≠ 单测**：LLM 系统非确定性，传统 CI 的「同输入同输出」假设失效；要从「测代码正确性」转向「评估行为正确性」（eval gate + 统计显著性，而非精确匹配）。
- **先分解再评测**：不要评「agent 好不好」，拆成 router / skill / trajectory 三层各选合适评估器（代码类 / 评委 / 人工）。
- **评委三件套**：清晰 rubric + 已校准 judge + 已知 judge 偏差；judge 弱于被测系统则分数触顶在盲点。
- **可靠评委 prompt 设计**：二值/低精度标签 > 5 分制（歧义更少）；每个标签明确定义（含边界与不确定时偏向）；复杂维度拆成多个独立评委再确定性聚合；要求 CoT 先理由后判分；低温度；vs 人工校准。
- **golden set + 快照测试 + A/B**：50–100 条已知良轨迹作回归集；对大批输入录轨迹/输出，后续跑对比快照偏差；改 prompt/模型时双版同跑对比指标；全部进版本控制（prompt/工具定义/评测集）。
- **可观测性前置**：用 OpenTelemetry traces/spans（Arize Phoenix）可视化并调试 agent 步骤，是评测的前提。

## 4. 动手实践
### 实践任务
把本课方法论落成一个**真实可跑的 eval harness**，对 WB 三个既有技能（`wb-agent-evaluation` / `wb-artifact-verification` / `wb-debug-loop`）做代码类三层检查 + 收敛分数代理 + 冻结评委 rubric 模板。
脚本：`D:/腾讯AI/yt/tmp/dl-eval/eval_harness.py`，输出 `eval_report.json`。
### 实践目标
验证「评估驱动开发」能直接用于 WB 技能质量门禁；并亲自跑通一次「发现缺陷→诊断→修正→重跑→确认」的评测飞轮。

## 5. 验收
1. **真跑通**：harness 在 3 个技能上实跑，产出代码类检查 + 收敛分数 + 冻结 rubric + 报告 JSON（非假数据）。
2. **发现至少 1 个真问题并闭环**：首跑 3 技能 `version_field` 全 FAIL → 诊断为正则未容错引号（`version: "1.22.0"` 带引号）→ 修正 `^version:\s*"?([\d.]+)"?` → 重跑 3×5/5 全 PASS、收敛分数 1.0 → 确认有效。这是 harness 自身盲区，非技能缺陷。
3. **可量化指标**：代码类检查通过率 12/15→15/15；convergence 代理 0.8→1.0；FFFD 全 0、行数预算全达标、评估口径全覆盖。

## 6. 复盘
1. 今天真正新增掌握：评估驱动开发飞轮、三层分解（router/skill/trajectory）、收敛分数、评委校准纪律（kappa≥0.6 / 冻结 rubric / judge≥系统 / 防漂移）。
2. 可用于 Agent/WB：① 给 `wb-agent-evaluation`(ae) 增补「trajectory/convergence score + 评委校准(kappa)」维度；② 共学自动化收尾可加 eval gate（golden set 回归）防 stealth 退化；③ 技能入库门禁复用本课「代码类检查」清单。
3. 实践发现：评测工具自身也会踩盲点（引号/格式），印证「评估驱动」要先评测评估器本身——与课程 Lesson13 improving-your-judge 呼应。
4. 值得沉淀：把「收敛分数 + 评委校准纪律」作为 ae 技能的候选增量（建议下一轮共学落地，不本轮强改）。
5. 以后可跳过：LLM-as-a-Judge 的入门科普（已懂）；直接进「评委校准实操 / 多评委集成 / drift 监控」等深水区。

## 今日完成标准
新增知识（评估驱动开发+三层分解+收敛分数+评委校准）× 实际实践（可跑 harness 跑通 3 技能）× 可验证验收（发现引号盲区并闭环、收敛 0.8→1.0）× 复盘沉淀（ae 候选增量）。

---
来源：deeplearning.ai/courses/evaluating-ai-agents（recap + landing）；互补 agentpatternscatalog.org/methodologies/ai-as-judge-evaluation；waytoagi 系 LLM 评委实践。去重核验：台账 `LLM-as-a-Judge` 仅 1 泛提、`convergence score/轨迹评估/评估驱动开发/improving-judge/三层分解` 全 0 命中 → 本轮为 genuine gap。
