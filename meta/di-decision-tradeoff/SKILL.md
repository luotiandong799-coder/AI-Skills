---
name: di-decision-tradeoff
description: 决策权衡分析（Decision Intelligence）。当用户面临 ≥2 个可行方案、需要在成本/收益/风险/可行性之间权衡、或要求"帮我选/对比/排优先级"时调用。提供加权决策矩阵、Pros&Cons 加权、Pre-Mortem、机会成本、ICE、RICE、Eisenhower、单向/双向门等框架，输出结构化方案对比与推荐，绝不替用户做需授权的重大决定。
module: DI
modules: DI,TI
---

# DI · 决策权衡分析（Decision Intelligence）

> 本技能是 Personal AI OS 13 模块中 **DI（决策智能）** 的唯一载体。TI 负责"想明白"，DI 负责"在多方案中作合理选择"。
> 方法论实拉自社区技能（2026-11-07 实拉）：`skillmd.ai/skills/decision-matrix-1`、`ruleskill.com/skills/iflytek/decision-matrix`、`hub.decision.ai/skills/nickcrew/decision-maker`、`github.com/alivirgo/Major-AI-Skills`（pros-and-cons-table）。

## 一、何时用

- 存在 ≥2 个可行选项，需要权衡（技术选型 / 架构 / 供应商 / 路线）。
- 需要对一批事项排优先级（功能 / 想法 / 实验）。
- 用户明确说"帮我选 / 对比 / 排优先级 / 该不该做"。
- **不适用**：低风险可逆的日常小事、需要执业资质的结论（医疗/法律/金融重大）、危机即时处置、数据完全不可得。

## 二、框架库（按场景选）

| 框架 | 适用 | 输出 |
|---|---|---|
| **加权决策矩阵（Pugh）** | 多选项 × 多标准 | 加权总分表 + 推荐 |
| **加权 Pros&Cons** | 快速二元抉择 | 两栏带权重评分 |
| **Pre-Mortem** | 高风险、需风险压力测试 | 失败模式清单 + 缓解 |
| **机会成本框架** | 两个都好、二选一 | 得/失/后悔测试 |
| **ICE** | 多事项快速排序 | Impact×Confidence×Ease |
| **RICE** |  backlog/功能优先级 | Reach×Impact×Confidence÷Effort |
| **Eisenhower** | 任务分诊 | 紧迫×重要 2×2 |
| **单向/双向门（贝索斯）** | 判断可逆性 | Type1 不可逆 / Type2 可逆 |

## 三、标准流程

1. **澄清决策**：一句话陈述决策 + 成功标准 + 截止时间。
2. **枚举选项**：列全所有现实选项，含"什么都不做 / 延后"。2–6 个为宜。
3. **选框架**：二元→Pros&Cons；多标准→加权矩阵；排序→ICE/RICE；风险→Pre-Mortem；分诊→Eisenhower。
4. **定标准（加权矩阵）**：列 3–5 条最关键标准（帕累托，>5 条增噪）；**权重由用户定**（防 AI 偏见）；含"切换成本/锁定风险"。
5. **打分**：每选项每标准 1–10 整数；总分 = Σ(分×权重)。
6. **检验假设**：看最强项、不确定性、不可谈判项、可逆性。
7. **输出**：推荐 + 依据 + 可能推翻结论的新信息。

## 四、硬护栏（实拉共识）

- **权重必须由用户确认**后才能打分（防 AI 操纵权重保其偏好）。
- **绝不编造**缺失的成本/概率/约束/偏好；标"估计/未知"。
- 高利害决策：框架只用于"组织问题与权衡"，**不当专业建议或最终结论**；引导用户核实事实并咨询有资质方。
- 分数非客观真理，是"用户已声明偏好的透明表达"——明确标注。
- 决策边界：DI 不替代 TI 分析，不擅自替用户作需授权的重大决定。

## 五、与 OS 协作

- 输出结构化方案对比 → 交给 **EI** 生成执行计划。
- 多 Agent 协作决策 → 委托 `agent-guild` 做收件箱交接。
- 决策记录 → **MI** 沉淀为"已验证经验"。

## 六、来源（2026-11-07 实拉）

- Weighted Decision Matrix / Pugh：skillmd.ai/skills/decision-matrix-1；ruleskill.com/skills/iflytek/decision-matrix
- Pre-Mortem / Opportunity Cost / ICE / RICE / Eisenhower / 10-10-10：hub.decision.ai/skills/nickcrew/decision-maker；skilld.dev/gh/iflytek/skillhub/decision-matrix
- 加权 Pros&Cons + Type1/Type2 门（贝索斯）：github.com/alivirgo/Major-AI-Skills/blob/master/skills/pros-and-cons-table/SKILL.md
