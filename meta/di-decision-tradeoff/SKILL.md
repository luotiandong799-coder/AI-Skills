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

## 六、MCDA 形式化（加权 / AHP / TOPSIS + 敏感性）

> 加权决策矩阵的严谨版：把"拍分"升级为可审计的多准则决策分析（MCDA）。2026-11-07 实拉。

**① 加权和与归一化**
- 综合值 `V(a)=Σ wᵢ·sᵢ(a)`，权重归一 `Σwᵢ=1, wᵢ≥0`。
- 效益型归一 `s=(x−min)/(max−min)`；成本型反向 `s=(max−x)/(max−min)`——方向反了结论必错。

**② AHP 定权重（防"拍脑袋定权"）**
- 成对比较矩阵 A：`aᵢⱼ=1/aⱼᵢ, aᵢᵢ=1`；取主特征向量为权重。
- **一致性比率 CR** 必须算：常规阈值 CR<0.1；选项多、矩阵大时可放宽（实拉案例用到 0.2）。CR 超标=判断自相矛盾，须重填。

**③ 聚合方式（按需）**
- 加权和（补偿型，最常用）/ TOPSIS（正负理想解距离，`Pᵢ=Sᵢ⁻/(Sᵢ⁺+Sᵢ⁻)`，越近 1 越优）/ 超排序 outranking（PROMETHEE/VIKOR 概念：允许"不可补偿"）。
- 超排序可用一致性指数 `C(a,b)=Σ_{i:sᵢ(a)≥sᵢ(b)} wᵢ` 表达"a 在多大权重上不劣于 b"。

**④ 敏感性分析（必做，否则结论不稳）**
- **OAT（一次一因素）**：目标权重 0%→100%，其余等比缩放保和=1，观察排名反转点 → 画 tornado 图看哪条标准最撼动结论。
- **阈值分析**：找出使 top 选项发生 rank reversal 的权重临界值（安全边界）。
- **全局敏感性**：蒙特卡洛/狄利克雷 bootstrap 抽样上千组权重向量，算**排名稳定性** `RS(a)=P(a 排第一)`；高 RS=稳健，低 RS=靠权重假设撑着。
- **情景分析**：预设若干权重方案（"成本优先" vs "质量优先"），看结论是否随立场翻转。
- **判读铁律**：MCDA 排名是**条件性**的——依赖标准/权重/归一化/聚合规则/不确定性假设。输出须分开"稳健 top"与"边缘候选"，并声明在什么权重变化下结论会变。

## 七、来源（2026-11-07 实拉）

- Weighted Decision Matrix / Pugh：skillmd.ai/skills/decision-matrix-1；ruleskill.com/skills/iflytek/decision-matrix
- Pre-Mortem / Opportunity Cost / ICE / RICE / Eisenhower / 10-10-10：hub.decision.ai/skills/nickcrew/decision-maker；skilld.dev/gh/iflytek/skillhub/decision-matrix
- 加权 Pros&Cons + Type1/Type2 门（贝索斯）：github.com/alivirgo/Major-AI-Skills/blob/master/skills/pros-and-cons-table/SKILL.md
- MCDA 敏感性分析（OAT/阈值/蒙特卡洛/情景）+ AHP 加权求和：ecologysci.com/posts/multicriteria-decision-analysis-for-ecosystem-services-a-comprehensive-framework-for-assessment-optimization-and-validation
- AHP 成对比较/一致性比率 CR/±25% 敏感性：mdpi.com/2071-1050/13/23/13483
- 加权和 V(a)/归一化/超排序一致性指数/排名稳定性 RS：sustainablecatalyst.com/?p=2841
- TOPSIS 正负理想解 + AHP/TOPSIS 敏感性：tandfonline.com/doi/full/10.1080/14786451.2023.2167999
