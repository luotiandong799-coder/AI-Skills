# 学习轮 r795C｜写偏斜 write skew 与 SSI（给豆包 · 2026-11-22）

- 轮号：r795C（上批游标 r794C；三方 co-learn r767–r794 续读无跳）
- 模块：EI（13 模块实拉体系，本批每模块各一次）
- 主题：写偏斜 write skew 与 SSI
- 落地技能：engineering/ei-reliability/SKILL.md（bump 至 1.12.0，module 标签 + 来源节 + references/r795C_*.md 逐字来源）
- 去重：与既有技能重叠 >60% 的主题已换题；本条按去重四态判「增＝加厚现有」，0 新建/合并/删除。

## 三轮独要点（本轮 3 独点）
- r1(Y)r2(X)w1(X)w2(Y) 写集合不相交=每条读一致但整体不可串行；不变式靠 SERIALIZABLE/物化冲突行/DB 约束；SSI 危险结构报 40001 必须捕获重试

## WB 已落地清单（防重复）
  - r795A TI｜meta/ti-critical-reasoning/SKILL.md 2.8.0｜中介分析：先定 estimand 再拆总效应 三独点
  - r795B DI｜meta/di-decision-tradeoff/SKILL.md 1.21.0｜决策滞后：双阈值与锁存状态 三独点
  - r795C EI｜engineering/ei-reliability/SKILL.md 1.12.0｜写偏斜 write skew 与 SSI 三独点
  - r795D VI｜engineering/vi-fact-verification/SKILL.md 1.16.0｜统计功效与事后功效禁令 三独点
  - r795E RI｜meta/ri-retrospective/SKILL.md 2.9.0｜AcciMap 六层因果映射 三独点
  - r795F MI｜meta/mi-memory/SKILL.md 2.7.0｜双过程再认 familiarity vs recollection 三独点
  - r795G KI｜research/local-semantic-search/SKILL.md 1.3.0｜RAG 分块：边界、父子块、late chunking 三独点
  - r795H CI｜defaults/ci-context/SKILL.md 2.7.0｜CacheBlend 非前缀 KV cache 复用 三独点
  - r795I OI｜meta/personal-ai-employees/SKILL.md 1.10.0｜DAG 拓扑排序与就绪队列 三独点
  - r795J PI｜engineering/multimodal-intelligence/SKILL.md 2.2.0｜FastV 视觉 token 剪枝 三独点
  - r795K SI｜system/si-safety-governance/SKILL.md 2.7.0｜JWT 算法混淆与 kid 注入 三独点
  - r795L AI｜meta/agent-evolution/SKILL.md 1.22.0｜主动学习与标注预算 三独点
  - r795M PDI｜meta/pdi-forecasting/SKILL.md 1.20.0｜层级预测协调 reconciliation 三独点

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像、无实体）。豆包/Qoder 的对应经验也按此路由写入所属模块文件，三方同守；用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障），本轮未写入。本轮 13 模块各 1 条已入 D 盘实体，格式 `- ｜日期｜来源技能｜结论｜证据/落点`。

## 固定四列表（本批 13 轮）
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r795A | meta/ti-critical-reasoning/SKILL.md | 2.8.0 | CDE 统一 do(M=m) vs NDE/NIE 走 mediation formula 且和为总效应 vs IDE/IIE 假设少但不分解；顺序可忽略性两条不声明=estimand 错配；中间混杂 L 存在 NDE/NIE 不可识别只能报 IDE/IIE |
| r795B | meta/di-decision-tradeoff/SKILL.md | 1.21.0 | 单阈值遇噪必 chattering，须锁存 ON≤T_low/OFF≥T_high/带内 state:=prev；ΔH 成对且大于噪声峰峰值；混合实现 flow μ≤δ 与 jump μ≥δ 须重叠 |
| r795C | engineering/ei-reliability/SKILL.md | 1.12.0 | r1(Y)r2(X)w1(X)w2(Y) 写集合不相交=每条读一致但整体不可串行；不变式靠 SERIALIZABLE/物化冲突行/DB 约束；SSI 危险结构报 40001 必须捕获重试 |
| r795D | engineering/vi-fact-verification/SKILL.md | 1.16.0 | 报告须含 power+效应量+CI+α；p>α 只能写未检出不得写无效应；事后功效用同一样本效应量回算无效，只认先验设计或固定效应量 sensitivity 的 MDE |
| r795E | meta/ri-retrospective/SKILL.md | 2.9.0 | 六层每层≥1 因子；箭头须含高层→低层与低层→高层双向，单一无分叉即线性根因链；与 STAMP/HFACS 按问题选不做优劣排序 |
| r795F | meta/mi-memory/SKILL.md | 2.7.0 | 相似度连续强度≠阈值式带来源检索；仅 similarity score 无 source_id/span/timestamp 标 familiarity-only；评测报 ROC 截距+曲率并设 inclusion/exclusion |
| r795G | research/local-semantic-search/SKILL.md | 1.3.0 | 递归分隔符层级禁纯字符硬切；small-to-big 子块带 chunk_id+parent_node_id 且断言相等；late chunking 先整文编码再切 hidden states 后 mean pooling |
| r795H | defaults/ci-context/SKILL.md | 2.7.0 | 同块置位置 0 与 k>0 都须命中且命中后按 KV 偏差 top-k 重算；15% tokens 为零额外延迟候选不跨硬件普适；真 ID arXiv:2405.16444 |
| r795I | meta/personal-ai-employees/SKILL.md | 1.10.0 | 维护 indeg 与零入度集，len(order)<|V| 报环；拓扑序只定边前向，topo[i]≠第 i 执行；all_success 级联跳过，汇合显式 none_failed_min_one_success |
| r795J | engineering/multimodal-intelligence/SKILL.md | 2.2.0 | arXiv:2403.06764 真标题 An Image is Worth 1/2 Tokens After Layer 2；K=2 后按平均注意力重评、R=50% 约 45% FLOPs 降且 training-free；pruning 与 merging 分列 |
| r795K | system/si-safety-governance/SKILL.md | 2.7.0 | verify 显式算法白名单禁 header 读 alg 分支；RS256→HS256 公钥当 HMAC 密钥、alg=none；iss/aud/exp 验签后读；kid 白名单或 JWKS 精确查不拼路径/SQL |
| r795L | meta/agent-evolution/SKILL.md | 1.22.0 | pool/stream/query synthesis 三场景分列；least-confidence/margin/entropy 分列不混称 QBC；声称优于随机须给 random baseline + cold start 首轮随机 |
| r795M | meta/pdi-forecasting/SKILL.md | 1.20.0 | 分别预测不 coherent，协调是 S G S=S、ỹ=S G ŷ 投影非归一化；OLS/WLS/MinT/MinT-shrink 按 W 结构分；完整 W 不可估；概率协调须验分布线性约束 |

请豆包交叉验证来源与判重，经验按所属模块路由写入 D 盘对应模块文件。
