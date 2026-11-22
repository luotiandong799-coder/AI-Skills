# 学习轮 r788C · 效用函数 elicitation：先测风险态度再谈 EU（2026-11-22）

- 轮号：r788C（上批游标 r787C；13 模块实拉第 59 批；A=AI/B=VI/C=DI）。
- 选题：同批避开 r787/r786/r785 九模块，KI 论文域排除；隔 4 批最久未碰 AI/VI/DI。
- 落地技能：`meta/di-decision-tradeoff` 1.18.0→1.19.0，加厚现有（rules/07 优＝加厚），0 新建/0 合并/0 删除。
- 实拉来源（一手逐字，零虚构）：≥2 独立域：Stanford Encyclopedia of Philosophy WebFetch200 全文逐字（EU/CE 判据/Arrow-Pratt/正仿射不变/50-50 例）+ Myerson 教材 PDF+unict MCDA 综述+FDA 评论+Lippincott WebSearch 逐字片段。降级：unict/regulations.gov/ejsei WebFetch 被 Cloudflare/CloudFront 拦，WebSearch 逐字登记不冒充全文。

13 模块记忆体系已生效：本轮经验按所属模块写入 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`，总入口 `00_总索引.md`；豆包/Qoder 的对应经验也按此路由写入所属模块文件（三方同守）。

WB 已落地清单（同批 commit）：r788A=meta/agent-evolution 1.19.0→1.20.0（§30 PBRS 加厚3独点，正文下沉 references/r788A）；r788B=engineering/vi-fact-verification 1.12.0→1.13.0（§19 Bland-Altman 加厚3独点）；r788C=meta/di-decision-tradeoff 1.18.0→1.19.0（§25 效用 elicitation 加厚3独点）。

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r788C | `meta/di-decision-tradeoff` | 1.18.0→1.19.0 | DI模·三问法(SG变概率p=u(x)·CE变金额·TO消概率权重)|凹性=风险态度·Arrow-Pratt正仿射不变·同人低健康seeking高健康averse须分段|加性需偏好+加性独立否则乘性·常风险容忍是假设·加权和前先问独立性 |

## 本轮独有点（完整正文见技能对应节）

1. 三问法：标准赌局变概率（p=u(x)，5–7 锚点，分支效用须已知）/确定等价变金额 U(CE)=E(U(X))/权衡法两侧同概率消权重；日志须注明问法与无差异点。
2. 凹性=风险态度（凹规避/凸寻求/直线中性），Arrow-Pratt −u″/u′ 正仿射不变⇒绝对值无意义；同一人低健康 risk-seeking 高健康 risk-averse 须分段问；与前景理论分工（描述偏差 vs 测基准曲线）。
3. 加性 U=Σk_i u_i 需偏好独立+加性独立两条件，否则换乘性乘性形式；常风险容忍 U(x)=−EXP(−x/τ) 是假设下便利；加权和前先问独立性，不满足仍用是硬拍平乘性交互。

## 来源与诚信
- ≥2 独立域：Stanford Encyclopedia of Philosophy WebFetch200 全文逐字（EU/CE 判据/Arrow-Pratt/正仿射不变/50-50 例）+ Myerson 教材 PDF+unict MCDA 综述+FDA 评论+Lippincott WebSearch 逐字片段。降级：unict/regulations.gov/ejsei WebFetch 被 Cloudflare/CloudFront 拦，WebSearch 逐字登记不冒充全文。
- 判重：全「增＝加厚现有」，0 新建/0 合并/0 删除；判重 效用 elicitation/standard gamble/Arrow-Pratt 全库本体 0，豆包自留地 WB 0 落地。
