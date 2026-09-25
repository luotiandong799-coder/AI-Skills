# 2026-09-23 学习轮 r151-A（OpenRouter：评测可比性 / 回退路由韧性 / 评测即规格）

## 实拉证据（全量 165 路 + openrouter 深拉）
- **全量抓取**：`fetchall.py a` → 165 路 / 122 OK200 / 43 未达（与 r150 同集合；未达为 GitHub 403 限流、aliyun/zhipu/hf/gpt_store 经代理 502、部分 404/302，均属已知不可达，非本轮新增）。
- **主源深拉（清单外新信源首读）**：OpenRouter 官方 `openrouter.ai/llms.txt`（40 链接）→ 深拉 **30/37 页全 200**：`docs/guides/ori/eval.md`、`docs/guides/routing/routers/free-router.md`、`docs/guides/routing/model-variants/free.md`、`docs/faq.md`、`agents.md`、`docs/api-reference/overview.md` 等。
- 逐站留痕：fetchall 的 `a/` 目录每站一份 `<name>.txt`（URL/STATUS/BYTES/VIA）；openrouter 深拉 `deep_a/` 30 份原文。

## 独点清单 + 判非重复理由（3 点落地 av/dl/sd）
1. **评测可比性——固定测试台**（→ av 1.89.0→1.90.0）：横向比较多 run 时，harness+被评模型在每次 run 解析一次并全程保持，prompt 不能改它们。判非重复：av 现有 §载荷形状/轨迹三元组 管"评什么、怎么评"，本条管"横向比较多 run 时先冻结测试台否则差异不可信"，增量 ≥50%。
2. **回退路由韧性**（→ dl 1.44.0→1.45.0）：单一外部模型依赖是脆弱点，把"调不通换一个"做成路由层一等能力；不差时让 free-router 决策而非写死。判非重复：dl §熔断窄自救 管"命中上限后怎么退"，本条管"还没命中上限就靠路由拆单点依赖"，相邻不重叠。
3. **评测即规格**（→ sd 1.73.0→1.74.0）：跑 eval 前先冻结四问（测哪部分/成功标准/有真数据吗/成本上限）。判非重复：sd §模糊度闸门 管"请求本身讲清没"，本条管"连评测自己也要先有 spec 且含真实数据+成本两道闸门"。

## 落地汇报（强制四列表格）
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| A | engineering/wb-artifact-verification | 1.90.0 | 评测可比性：每次 run 冻结 harness+模型（测试台），prompt 不可改；否则多 run 差异不可信 |
| A | engineering/wb-debug-loop | 1.45.0 | 回退路由韧性：fallback 是依赖层能力，不差时让 free-router 决策而非写死单模型 |
| A | engineering/wb-spec-driven | 1.74.0 | 评测即规格：跑前冻结四问（测哪部分/成功标准/真数据/成本上限） |

## 三件套评估（A）
- 本轮落 av/dl/sd，**避开豆包主战场 mts/ED**。三件套（pt/ctx/mts）本轮无新料，**维持 3 件套**。

## 审计
- 7 文件 PyYAML 全解析；CRLF=0 / STRAY_CR=0 / U+FFFD=0 / 尾空白=0 / description≤1024（av739/dl696/sd820）。ISSUES=0。
- repo→live 全量 sha256：7/7 SAME。
- 版本化：commit `024ae90`，push `c45a766..024ae90`（SSH over 443，无重试），`merge-base --is-ancestor`=ANCESTOR_OK。
