---
name: execution-intelligence
description: 执行智能主动调用治理规范（方案 A）。当任务属于多步骤/依赖/批量改动/部署/条件分支/验收类，或需要明确风险边界与执行证明时，按本规范主动调用 _tools/execution_intelligence.py 做 EDG 规划、Guard 判定、GDR 复用与 CCS 验收。不注册 Hook、不接管宿主工具调用、不改模型路由/权限。
module: EI
modules: EI
---

# execution-intelligence · 执行智能主动调用治理规范（方案 A）

> 采用方案 A：**被动架构下 Agent 主动调用**。不注册 Hook、不接管宿主工具调用链、不改模型路由/权限/现有工作流。
> 依托工具：`D:\腾讯AI\skills\_tools\execution_intelligence.py`（EDG / GDR / CCS，纯标准库，已自测 8/8 + 验收对照通过）。
> 本文件是"何时调、怎么调、安全边界"的治理约定，不是工具本身。

## 一、定位

execution_intelligence.py 不是每次对话必跑的工具，而是**复杂 / 确定性 / 多步骤 / 高风险**任务的规划与验证组件。它只做"已确定动作的保存、校验、复用与记账"，不代宿主跳过模型回调——真正的跳过由宿主按 `plan` 输出执行。

### 本质：执行治理层，不是又一个 AI 助手

EI 不负责替代大模型思考，也不负责生成答案；它帮助 Agent 在执行复杂任务时做到：**先规划、再执行、控制风险、减少重复、最后验收**。

四大模块对应职责：

| 模块 | 作用 | 通俗理解 |
|---|---|---|
| EDG | 执行依赖图编译 | 把复杂任务拆成有先后关系的步骤 |
| Guard | 条件与风险判断 | 判断当前步骤能不能执行 |
| GDR | 执行复用判定 | 判断以前做过的工作能不能复用 |
| CCS | 执行证书 | 检查任务是否真正完成，留下验收依据 |

与 Agent / Skill / Hook 的关系（各司其职，不越位）：

| 技术 | 核心职责 |
|---|---|
| 大模型 | 思考、理解、决策 |
| Agent | 调度工具、执行任务 |
| Skill | 提供专业知识和操作能力 |
| Hook | 在特定执行节点自动触发逻辑 |
| EI | 管理执行计划、约束、复用和验收 |

一句话总结：**EI 不负责告诉 AI 应该想什么，而是负责让 AI 把决定要做的事情，有计划、有约束、可追踪、可验收地完成。**

### 三个必须守住的边界

1. EI 不会让模型本身变得更聪明——它只治理"执行过程"，不改造"思考质量"。
2. EI 不会自动提高所有任务的回答质量——仅对多步骤 / 确定性 / 高风险 / 需验收类任务有收益。
3. EI 若规划逻辑不准确，反而可能增加执行成本——故坚持"先审计、后设计、再实施、最后验证"；GDR 仅在条件全满足时复用，不确定一律交回 LLM 重新判断。

## 二、触发条件（应主动评估并优先调用）

满足任一即启用：

1. 多步骤、存在依赖关系的复杂任务。
2. 多个 Skill / 工具需要协同执行的任务。
3. 涉及文件批量修改、代码部署、配置变更的任务。
4. 存在明确条件分支、执行约束或失败回退要求的任务。
5. 自动化工作流及需要结果验收的重要任务。
6. 需要明确风险边界和执行证明（证书）的任务。

**默认不调用**：普通问答 / 翻译润色改写 / 简单资料查询 / 纯创意讨论 / 调用成本明显高于收益的简单操作。

## 三、执行流程

1. 判断任务是否符合触发条件。
2. 检查 EDG 规划输入（spec）与事实数据（facts）是否完整。
3. 调用工具：`compile` → `plan` →（执行后）`certify` → `stats`。
4. 读取并核对 `plan` 的 Guard / GDR 结果（reuse / already_done / needs_llm / confirm_required / blocked）。
5. 按结果制定执行策略：**reuse/already_done 才可跳过模型重判**；needs_llm 必须交回 LLM；confirm_required 须先取得用户确认；blocked 不得执行。
6. 执行任务，**禁止把规划结果等同实际完成**。
7. 完成后验证真实结果（证据），不得伪造成功。
8. 对适用步骤生成 / 校验 CCS 证书（**无真实 evidence 默认拒发**）。
9. 工具不可用时，回退到 WB 原有执行流程并明确说明。

## 四、调用接口（工具路径固定）

```bash
cd "D:/腾讯AI/skills/_tools"
python execution_intelligence.py schema                                       # 查看 spec/facts 结构约定
python execution_intelligence.py compile <spec.json> <edg.json>               # 结构/权限/参数三重校验 -> EDG
python execution_intelligence.py plan   <edg.json> <facts.json>              # GDR 五态判定
python execution_intelligence.py guard  <edg.json> <facts.json> <step_id>    # 单条 Guard 求值
python execution_intelligence.py certify <edg.json> <facts.json> --ledger <certs.jsonl>   # 签发证书（需证据）
python execution_intelligence.py run    <edg.json> <facts.json> [--apply] [--write-facts out.json]  # 保守执行器，默认 dry-run
python execution_intelligence.py stats  <certs.jsonl>                        # 账本聚合
python execution_intelligence.py selftest                                  # 8 组内置用例
```

返回约定：成功返回 JSON + 退出码 0；编译/文件/参数错误返回 `{"ok":false,...}` + 退出码 2。

## 五、安全边界（硬性）

- 不绕过 WB 原有权限与安全机制；不擅自注册 Hook；不擅自改模型路由。
- 规划工具不得自动执行未授权操作；高风险步（risk=high）未确认绝不执行（见 E6 验证：deploy 高风险步 `--apply` 仍不执行）。
- 缺失事实不得当成已验证事实；facts 中 `evidence` 字段必须来自真实执行，否则证书拒发。
- 工具不可用时回退原有流程并说明。

## 六、试运行记录（2~4 周）

每次调用记录：调用次数与原因、EDG 规划有效性、Guard 判断准确性、GDR 复用效果、CCS 验收情况、额外耗时、误/漏调用与失败。试运行结束后形成评估报告，再决定是否进入 Hook 灰度。

## 七、诚实边界（工具侧，不得宣称已解决）

1. 不代宿主跳过模型回调：`plan` 只输出"该步是否需要模型重新判断"。
2. `tokens_saved_estimate` 为估算口径（默认 1200 输入 + 300 输出/次），非实测。
3. 未实现 RSI（自动改提示/Guard/配置）：缺独立验证集与回滚通道，按规范 P2/P3 暂缓。
4. Guard 表达式仅支持比较与布尔组合，不支持函数调用；未知字段返回 unknown 而非 false。
5. **已知限制（待修复，本轮不重构）**：`run --apply` 执行子进程时，若子进程输出含非 UTF-8 字节（如 GBK 路径），后台读线程会抛 `UnicodeDecodeError`，导致 evidence 截断；默认 dry-run 不受影响。修复需改 `run_steps` 的 subprocess 编码处理，留待后续轮次。

## 八、停用 / 回滚

- 停用：不再在触发任务中调用即可，零副作用（工具不被任何 Hook/自动化引用）。
- 卸载：删除本 SKILL.md 及 `D:\腾讯AI\skills\_tools\execution_intelligence.py` + 其 `_acceptance_ei_*` 验收件；未改动任何既有工具、规则、模型配置或插件权限。
