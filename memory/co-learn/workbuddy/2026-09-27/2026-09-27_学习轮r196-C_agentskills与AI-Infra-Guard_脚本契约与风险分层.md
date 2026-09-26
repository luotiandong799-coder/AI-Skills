# r196-C 审计：agentskills.io + 腾讯 AI-Infra-Guard 深拉 —— 落 2 点（脚本输出契约 / Skill 风险九类分层）

- 时间：2026-09-27 03:3x（r196-C）
- 主源 1：`agentskills.io/llms.txt`（1,374 B）+ `skill-creation/using-scripts.md`（12,743 B）
- 主源 2：`api.github.com/repos/Tencent/AI-Infra-Guard/readme`（37,515 B，Apache-2.0，6,594★）

## ★ fullstackskills.com 最终结论（连续 3 轮规则触发，本轮 2/3 达成并定性）
- `https://www.fullstackskills.com/` 返回 **200 但正文仅 114 B**：`window.onload=function(){window.location.href="/lander"}`
- `/lander` 返回 709 B：`window.LANDER_SYSTEM="PW" window._trfd.push({ap:"parking"})`
- **结论：该域名是停放页（parking），不是技能站点，不存在未取到的内容** → 移出待补清单，此后只保留探活计数。**无需再等第 3 轮。**

## 落地（2 点）
1. `engineering/wb-skill-authoring` 3.12.0 → **3.13.0**：**技能内脚本输出尺寸要可预测**（harness 会截断 → 默认摘要 + `--offset` 翻页，或强制 `--output` opt-in），并附 agentic 脚本契约五条（禁交互 / `--help` 即接口文档 / 报错带修法 / 结构化输出+stdout-stderr 分离 / 幂等·dry-run·退出码）。
2. `skills-security-check` 1.1.0 → **1.2.0**：**Skill 安全风险九类分层 T01–T09**（A 指令与记忆 / B 代码执行 / C 系统权限 / D 工具链与依赖 / E 代码质量）+ 扫描器自身须给 F1/Precision/Recall/FPR 四元组（SkillTrustBench：Gemini 3.5 Flash 精确 0.9947 但召回 0.9641；Claude Opus 4.6 召回 0.9974 但 FPR 0.0663）。

## 判非重复理由（逐条 grep 证据）
| 候选点 | 命中 | 结论 |
|---|---|---|
| stdout 数据 / stderr 诊断分离 | `ed` §166、`ed` §571 stdio 纪律、`debug-loop` §476、`mcp-builder` §258 | 重叠 >60%，**不落** |
| 退出码区分失败类型 | `debug-loop` §55「退出码相同不代表失败原因相同」（反向判据，已覆盖该面） | 不重复展开 |
| **脚本输出尺寸可预测 + 截断翻页** | grep「10-30K/输出截断/--offset」仅命中 mts §383（检索块超预算）与 debug-loop §191（历史被截断），**均无"生产端设输出上限"** | **0 命中 → 净新，落** |
| **Skill 风险九类分层 T01–T09** | grep「SkillTrustBench/T01/指令劫持/系统驻留/工具劫持」仅命中 `ed` §2022 记忆投毒单条，**无分层分类法** | **0 命中 → 净新，落** |

## 提升层
工具 / 可复用 Skill（脚本契约）；可复用 Skill / 工作流（风险分层）。
