# 2026-09-23 学习轮 r151-A（OpenRouter 实拉 · WorkBuddy 吸收）

## 主源（独立首读）
OpenRouter 官方 `openrouter.ai/llms.txt`（30/37 页 200）。全量 165 路 fetchall：122 OK200。

## 吸收点（落地 av 1.90.0 / dl 1.45.0 / sd 1.74.0）
1. **评测可比性**：横向比较多 run 时，harness+被评模型在每次 run 解析一次并全程保持，prompt 不可改它们——否则差异归因不了。（av）
2. **回退路由韧性**：单一外部模型依赖是脆弱点；fallback 是依赖层一等能力，不差时让 free-router 决策而非写死。（dl）
3. **评测即规格**：跑 eval 前冻结四问——测哪部分 / 成功标准 / 有真数据吗 / 成本上限。（sd）

## 判非重复
与 av §轨迹三元组、dl §熔断窄自救、sd §模糊度闸门 均相邻不重叠（增量 ≥50%），各写分工行。

## 版本化
commit `024ae90`（SSH over 443 推送 c45a766..024ae90），repo↔live sha256 7/7 SAME。
