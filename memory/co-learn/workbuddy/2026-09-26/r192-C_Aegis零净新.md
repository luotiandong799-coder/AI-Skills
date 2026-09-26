# r192-C 学习轮审计：Aegis Method Pack（GanyuanRan/Aegis，1,282★，0 净新）

日期：2026-09-26 | 角色：WorkBuddy（审计 + 落地）| 主源：`github.com/GanyuanRan/Aegis`（清单外新发现，VoltAgent 精选清单扫出；经 `gh api` 实拉 README）

通道：`gh api` README（base64 解码）+ 比对 `Continuum-AI-Corp/OrcaReplay`（265★）README 选主源。

## 一、实拉证据（逐源 + 成功/未达）

| 源 | 状态 | 方法论要点 |
|---|---|---|
| `GanyuanRan/Aegis` README | ✅ 实拉（README 头部 + What You Get + 冻结 A/B 基准段） | 「Method Pack」让 AI 编码 agent 像守纪律的工程师：① 编辑前对真实基线（owner/契约/边界）对齐规划；② 完成后用**新证据**证伪（covered scope + residual risk）；③ **No ghost code**：退役的 fallback/旧路径须由 retire 触发器跟踪或删除，技术债不得静默累积；④ 简单任务走快速通道、ceremony 只在任务真需要时上；⑤ 冻结 A/B 基准（同 client/prompt/project/tool-policy，只变 Aegis 投射，120 run / 20 case，contract pass 61.67%→93.33%，报 95% 簇区间、不宣称普适质量）；⑥ 一套方法包跨宿主 |
| `Continuum-AI-Corp/OrcaReplay` README | ✅ 实拉（头部 + 三命令 + why） | record 任意 agent 运行、离线 byte-for-byte replay（不调模型）、从任一步 fork 到不同模型比谁对；trace spec CC BY 4.0；「model 是唯一变量」 |

## 二、判非重复理由（grep 在册 wb-* 正文）

| 候选点 | grep 表达式 | 在册命中 | 判定 |
|---|---|---|---|
| 冻结 A/B 基准：同 harness/模型/温度/系统提示/数据集，只变被评方法一个变量，报区间不宣称普适 | `冻结`、`只变.*变量`、`唯一变量`、`其余一律冻结`、`harness` | `av:1359` 已落「横向比较多 run/多模型时，测试台解析一次全程不变；除被测量的变量外其余一律冻结——harness 版本/模型 ID/温度/系统提示/数据集任一漂移差异就归因不了」；`av:48`（同 prompt 只改 effort 的 A/B） | **重叠>60% → 不落** |
| 完成后用新证据证伪（covered scope + residual risk） | `验证.*后`、`证据.*完成`、`残差风险`、`scope` | `wb-artifact-verification` 绪论「独立验证 + 明确成功/失败判定」+ 逐子任务报告 + 完成度不能从最终答复推断 | **重叠>60% → 不落** |
| 简单任务走快速通道、ceremony 随任务需要 | `简单任务`、`快速通道`、`ceremony`、`仪式` | `ponytail:218` 已落「契约不存在时的声明只是仪式」+ YAGNI 决策阶梯（不上的复杂编排） | **重叠>60% → 不落** |
| No ghost code / 退役触发器：替换代码路径/fallback 须显式跟踪或删除，技术债不得静默累积 | `ghost`、`退役`、`retire`、`删除.*登记`、`自动回填`、`技术债` | `ed:2668`「删除要登记，否则自动回填会把删掉的灌回来」；`av:276`「控制的退役条件是根因消失，不是没再出过事」；skill 合并纪律「删差的 ls 复核」 | **重叠>60% → 不落**（Aegis 的「supersede→显式退役」被 ed 删除登记 + av 控制退役 + 合并删差三处覆盖，边际增量不足） |
| OrcaReplay：record→离线 replay（不调模型）→从 checkpoint fork 换模型比谁对，model 是唯一变量 | `replay`、`重放`、`只重放未完成`、`钉版本重放`、`重放不等于复现` | `av` 触发词与 §「重放打最新版/重放不等于复现/钉版本重放/只重跑下游」+ `wb-debug-loop` reproduce→minimize→verify | **重叠>60% → 不落**（replay 作为调试原语已在 av 落版，OrcaReplay 是其工具化实现，非新方法论层） |

## 三、结论
C 轮 0 净新。Aegis / OrcaReplay 的方法论均已被现有 wb-* 技能（av/ed/ponytail/debug-loop）覆盖。无编造 idle commit。
下轮提示：Aegis 的「retire 触发器」概念边际增量极小已判不落；若后续轮次发现规模性「替换路径不留 ghost」实践，可重新评估是否补一条到 ed 的清理纪律。
