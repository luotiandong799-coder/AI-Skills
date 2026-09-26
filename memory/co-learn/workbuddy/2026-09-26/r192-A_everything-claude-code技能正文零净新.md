# r192-A 学习轮审计：everything-claude-code 未读技能正文（0 净新）

日期：2026-09-26 | 角色：WorkBuddy（审计 + 落地）| 主源：`WorldFlowAI/everything-claude-code`（GitHub，r190-B 只读了 README + verification-loop + continuous-learning，本轮补读其余 9 个技能正文里的 4 个高相关）

通道：`gh api` trees + contents（base64 解码），直连可达，未启 VPN。

## 一、实拉证据（逐源 + 成功/未达）

| 技能正文 | 状态 | 方法论要点 |
|---|---|---|
| `skills/eval-harness/SKILL.md` | ✅ 实拉（约 190 行） | EDD（评测驱动开发）；能力 eval vs 回归 eval 二分；pass@k（k 次至少一次成）/ pass^k（k 次全成）；三级 grader（代码确定性 > 模型 > 人工）；先定义 eval 再编码；安全项人工复核 |
| `skills/strategic-compact/SKILL.md` | ✅ 实拉（约 60 行） | 在逻辑边界手动 `/compact`（探索完→执行前 / 里程碑后 / 上下文切换前）而非任意自动压缩；PreToolUse 钩子按阈值（50 次调用）建议、人决定 |
| `skills/tdd-workflow/SKILL.md` | ✅ 实拉（约 410 行） | 测试先于代码；80% 覆盖率；单元/集成/E2E 三型；测用户可见行为不测实现细节；测试隔离；错误路径也测 |
| `skills/coding-standards/SKILL.md` | ✅ 实拉（约 520 行） | KISS/DRY/YAGNI；命名/不可变/错误处理/并行/类型安全/REST/zod 校验/AAA 测试/代码异味 |

未读其余 5 个（backend-patterns/clickhouse-io/frontend-patterns/project-guidelines-example/security-review）属具体语言/框架工程实践，与「可复用于 agent 技能系统的方法论层」无对应——按纪律不拉（省预算，且与 tdd-workflow/coding-standards 同族，结论可外推）。

## 二、判非重复理由（grep 在册 wb-* 正文）

| 候选点 | grep 表达式 | 在册命中 | 判定 |
|---|---|---|---|
| 能力 eval（低通过率起步爬坡）vs 回归 eval（≈100% 下滑即坏） | `能力.*eval`、`回归.*eval`、`capability`、`regression`、`从低通过率起步` | `av:520-521` 已落「两类 eval 的目标通过率相反：能力 eval 从低通过率起步、回归 eval 接近 100%」 | **重叠>60% → 不落** |
| pass@k 粉饰 flaky / 头条用原始单次成功率 | `pass@k`、`原始单次成功率`、`头条` | `av:492-496` 已落「pass@k 会粉饰 flaky 技能，头条指标=raw per-attempt success rate，pass@k 只作 --verbose 次级视图」 | **重叠>60% → 不落** |
| 三级 grader（确定性>概率>人工）| `代码.*grader`、`确定性.*概率.*人工`、`三级` | `av` 三独立证据源（独立算法 oracle/外部事实/交叉验证）同面；`wb-artifact-verification` 绪论已立 | **重叠>60% → 不落** |
| 先定义成功判据再实现 | `验收.*前置`、`定义完成`、`验收标准` | `wb-spec-driven` §三·十 执行前评审 + 验收标准前置；`wb-debug-loop` 先钉不可变基线 | **重叠>60% → 不落** |
| 安全项不自动化、留人工复核 | `安全.*人工`、`人工复核` | `av` 已落「宿主自带能力须剥离/中性化断言」+ 安全人工放行关卡（spec-driven 评审） | **重叠>60% → 不落** |
| 压缩按逻辑/语义边界、半途不压、钩子只建议人决定 | `逻辑边界`、`语义边界`、`子任务完成`、`半途.*压` | `cc:142-151` 已落「压缩时机按任务状态不按 token；一个子任务刚完成=语义边界允许压；半途/卡住禁止压」；`cc:28`「检查点时机在接缝处」 | **重叠>60% → 不落**（「钩子建议人决定」是投递机制细节，非方法论层新增） |
| 测试先于代码 / 测可见行为 / 测错误路径 | `验收标准`、`错误路径`、`先写测试` | `wb-spec-driven`（验收前置）+ `wb-debug-loop`（失败路径必验）同面；其余为通用软件工程实践，答不出「提升 agent 技能系统哪一层」 | **不落**（通用开发实践，非可迁移 agent 方法论） |
| KISS/DRY/YAGNI | `YAGNI`、`DRY`、`KISS` | `ponytail:21` 已落 YAGNI 决策阶梯 + DRY 同源 | **重叠>60% → 不落** |

## 三、结论
本轮 0 净新。everything-claude-code 9 个技能正文的方法论已被现有 wb-* 技能（av/ed/cc/spec-driven/ponytail）全覆盖，无未被覆盖的底层方法论点。证据与判重理由如上，无编造 idle commit。
