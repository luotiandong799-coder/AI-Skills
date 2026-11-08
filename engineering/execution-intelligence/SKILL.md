---
name: execution-intelligence
description: 执行智能主动调用治理规范（方案 A）。当任务属于多步骤/依赖/批量改动/部署/条件分支/验收类，或需要明确风险边界与执行证明时，按本规范主动调用 _tools/execution_intelligence.py 做 EDG 规划、Guard 判定、GDR 复用与 CCS 验收。不注册 Hook、不接管宿主工具调用、不改模型路由/权限。
module: EI
modules: EI
version: 1.0.0
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


## 九、契约式执行：Guard 的最小完备集与责任归属（2026-11-08 实拉，r715A）

> 方法论实拉：CMU SEI《API Security through Contract-Driven Programming》（2024-03-18，WebFetch 一手全文逐字）+ llm-coding.github.io/Semantic-Anchors·Design By Contract + 中文维基《契约式设计》+ sagecode.org Eiffel 教程，共 4 独立域交叉。与 §三 Guard 判定分工：§三管「五态结果怎么读」，本节管「断言该写哪三类、失败算谁的」。

- **r715A-1 契约三问＝执行规格的最小完备集**：每步（每次调用）须同时答 ① **expect** 前置条件（运行前必须为真）② **guarantee** 后置条件（运行后必须为真）③ **maintain** 不变式（无论怎么变换都不许变）——SEI 逐字 `What does the contract expect? / What does the contract guarantee? / What does the contract maintain?`（Hoare triple 三问）。且**每条断言只有一个责任方**：前置违反＝调用方（client）的 bug，后置或不变式违反＝实现方（supplier）的 bug；SEI 原文 `A caller or consumer that uses an API function whose preconditions are not met is not entitled to the postconditions`。⇒ 落地到本技能：EDG 每步 Guard 不只写「能不能跑」，要写明三类断言；CCS 拒发证书时按责任方分类（输入不合规 / 输出没达标 / 状态被破坏），而非一律「未完成」。**不双方重复防御性检查**（Semantic Anchors 逐字 `No defensive double-checking on both sides`）：内部可信接缝由调用方保证前置即可，供应商不必再校验被自己前置排除的状态。
- **r715A-2 契约继承三不可违 + 边界张力**：复用/替换既有步骤（子类型、新实现、换工具）时，SEI 逐字 `Preconditions cannot be strengthened` / `Postconditions cannot be weakened` / `Invariants cannot be weakened`——实现不得收窄可接受输入、不得放大输出范围、不得改变不变式（`pop()` 不许新增「栈至少 5 个元素」的前置；`size` 永不为负）。这是 Liskov 替换原则的契约级表述。安全反例：OWASP 2023 API 头号风险 **BOLA** 即「实现未履行前置条件」（请求须携带对**该特定对象**有效的授权 token）⇒ 安全缺陷可归约为契约违约。与 **Postel 定律**按边界分工：DbC 对**可信内部模块缝**严格、违约 fail hard；Postel 对**不可信外部输入**宽松；混用会把无效状态放进内部。⇒ 判据：换实现先验这三条，别只看「接口签名没变」。
- **r715A-3 机检天花板：不是每条契约都能自动生成断言**：OpenAPI 能表达前置（输入域、security scheme）与后置（返回码 + schema），**无法表达不变式**——SEI 逐字 `there is, however, no way to document outside of a text description what an endpoint may or may not change in terms of state`（REST 的 GET 幂等只能写文字）。RESTler / Dredd 从 OpenAPI 自动生成测试用例、JML 编译器把 Javadoc 转成运行时断言，前提都是契约**机器可读**。⇒ 验收设计必须把「能自动生成的断言」与「只能人工复核的文字约定」分开列；文档里写了一句「幂等」不等于已验收，CCS 对后者只能标「需人工」，不得据文字描述签 PASS。

**提升层**：工作流（执行规格与验收判定）+ 可复用 Skill。触发词：契约三问、expect/guarantee/maintain、责任归属、前置不可加强、后置不可削弱、不变式、BOLA、Postel 边界、OpenAPI 不表达不变式、fail hard、断言自动生成。

**判非（本轮独立实拉 5 域，登记不落地）**：progressive delivery 线（`sre.google/workbook/canarying-releases/` / `alerting-on-slos/` 的 canary 受控实验、error budget、multi-window multi-burn-rate、time confounding；Argo Rollouts `AnalysisTemplate` 自动 abort；`DrHazemAli/enterprise-system-design` change class CH0–CH4 + gate invariants I1–I10；techsensedev GKE SRE pipeline；kubo.hexabase 5% 流量×20% 错误率→整体 1%）已逐域取证，但 `engineering/wb-release-maintain` 现存 canary 概念 4 处，且该线属发布运维而非 EI 契约语义 ⇒ 按 rules/07 去重铁律判非换道，留候选池，不冒充本轮独点。

## 十、来源（2026-11-08 r715A 实拉）

- `resources.sei.cmu.edu/blog/api-security-through-contract-driven-programming/`（CMU SEI，2024-03-18，WebFetch 一手全文逐字：Hoare 三问、三不可违、BOLA、OpenAPI 不表达不变式、RESTler/Dredd/JML）
- `llm-coding.github.io/Semantic-Anchors/anchor/design-by-contract`（DbC 语义锚：责任归属、契约继承与 LSP、Postel 边界张力、No defensive double-checking）
- `hackcn.de/zh-cn/契约式设计`（中文维基：契约三问、供应商不校验前置、fail hard、发布版可移除断言）
- `sagecode.org/roadmap/pgp/eiffel/`（Eiffel require/ensure/invariant 语法与继承规则）
