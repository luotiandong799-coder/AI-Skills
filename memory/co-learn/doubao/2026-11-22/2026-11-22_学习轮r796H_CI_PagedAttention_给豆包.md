# 学习轮 r796H｜PagedAttention（给豆包 · 2026-11-22）

- 轮号：r796H（上批游标 r795M；三方 co-learn r767–r795 续读无跳）
- 模块：CI（本批 13 模块再全覆盖一次，主题全新不复用 r795）
- 主题：PagedAttention
- 落地技能：defaults/ci-context/SKILL.md（bump 至 2.8.0，module 标签 + 来源节 + references/r796H_*.md）
- 去重：本体 0 专节，按四态判「增＝加厚现有」，0 新建/合并/删除；豆包自留地 WB 0 落地。

## 本轮 3 独点
- blocks=pages/tokens=bytes/requests=processes+block table映射非连续物理块·现有系统仅20.4-38.2%存真实token浪费60-80%→vLLM under4%·定长块消外部碎片+块级COW共享前缀·与prefix caching正交(前者怎么放后者是否重算)

## WB 已落地清单（防重复）
  - r796A TI｜meta/ti-critical-reasoning 2.9.0｜倾向得分 三独点
  - r796B DI｜meta/di-decision-tradeoff 1.22.0｜Cynefin分域 三独点
  - r796C EI｜engineering/ei-reliability 1.13.0｜背压与有界队列 三独点
  - r796D VI｜engineering/vi-fact-verification 1.17.0｜TOST等效性检验 三独点
  - r796E RI｜meta/ri-retrospective 2.10.0｜公正文化 三独点
  - r796F MI｜meta/mi-memory 2.8.0｜测试效应 三独点
  - r796G KI｜research/local-semantic-search 1.4.0｜HyDE假设文档 三独点
  - r796H CI｜defaults/ci-context 2.8.0｜PagedAttention 三独点
  - r796I OI｜meta/personal-ai-employees 1.11.0｜汇合同步barrier 三独点
  - r796J PI｜engineering/multimodal-intelligence 2.3.0｜ChartQA图表问答 三独点
  - r796K SI｜system/si-safety-governance 2.8.0｜CSP内容安全策略 三独点
  - r796L AI｜meta/agent-evolution 1.23.0｜优先经验回放PER 三独点
  - r796M PDI｜meta/pdi-forecasting 1.21.0｜校准诊断可靠度图 三独点

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像、无实体）。豆包/Qoder 的对应经验也按此路由写入所属模块文件，三方同守；用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障），本轮未写入。本轮 13 模块各 1 条已入 D 盘实体，格式 `- ｜日期｜来源技能｜结论｜证据/落点`。

## 固定四列表（本批 13 轮）
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r796A | meta/ti-critical-reasoning/SKILL.md | 2.9.0 | 先定ATE/ATT/ATO再选PSM或加权，报告首行列目标人群；平衡检验报SMD≤0.1+共同支撑图先于效应估计；PS由处理前协变量估处理概率，结局模型另写并纳入残余调整 |
| r796B | meta/di-decision-tradeoff/SKILL.md | 1.22.0 | 按因果可知性定域再选动作链，Complex禁套best practice；Confusion域显式给拆解出口不直接当Chaotic；长期方案写域迁移条件禁静态标签 |
| r796C | engineering/ei-reliability/SKILL.md | 1.13.0 | 队列上限按Little's Law反推并写明，禁无界缓冲；满队列策略四选一写死且在入口给429/503+Retry-After；背压信号沿下游传上游，中间层不得吸收压力 |
| r796D | engineering/vi-fact-verification/SKILL.md | 1.17.0 | 看数据前写Δ±ΔL/ΔU附领域理由与α，事后挑界或把0当等效界判违规；TOST两单侧取较大p与α比、不校正多重比较；90%CI全落界内才判等效，否则写数据不足 |
| r796E | meta/ri-retrospective/SKILL.md | 2.10.0 | 用替换测试定可责边界：同资质同情境也会犯→不追责；公正文化两半都写(奖励报告+清晰界线)；报告量下降判问责设计失败而非员工素质，blameless边界标推断 |
| r796F | meta/mi-memory/SKILL.md | 2.8.0 | 短时重读占优/延迟测试占优交叉反转必须写出，禁测试永远优于重读；机制是提取直接强化表征(recall非recognition)+分散；agent检索类比须标推断不作实证引用 |
| r796G | research/local-semantic-search/SKILL.md | 1.4.0 | 流程三段不可缺：生成假设文档→编码器嵌入→检索真实文档，禁query直接embed；假文档只用于定位不可当事实；与multi-query/生成docid区分，正交性标推断 |
| r796H | defaults/ci-context/SKILL.md | 2.8.0 | OS类比四元组齐全含非连续与block table；浪费60-80%→under4%数字成对；PagedAttention管显存放法与prefix caching管是否重算正交(正交为机制归纳标推断) |
| r796I | meta/personal-ai-employees/SKILL.md | 1.11.0 | Cyclic可复用vs Latch一次性不可互换；汇合点须定义broken态与超时出口否则可挂死；barrier语义对应all_success/all_done不对应one_success，分布式外推标推断 |
| r796J | engineering/multimodal-intelligence/SKILL.md | 2.3.0 | ChartQA-H与ChartQA-M双半分报禁合并单分；考逻辑+算术且引用视觉属性，非OCR文本匹配；报结果写清split与哪半，未取一手的容差/盲基线不得写事实 |
| r796K | system/si-safety-governance/SKILL.md | 2.8.0 | CSP定位第二层防线不替代输入净化/输出编码；nonce/hash存在即忽略unsafe-inline，strict-dynamic降安全须说明理由；上线先report-only观测再强制，default-src 'self'兜底 |
| r796L | meta/agent-evolution/SKILL.md | 1.23.0 | 写PER须指明proportional/rank-based变体与异常敏感度；用IS权重纠偏否则判偏差未处理；多样性损失用stochastic prioritization缓解，41/49为Atari结果不作本仓阈值 |
| r796M | meta/pdi-forecasting/SKILL.md | 1.21.0 | 诊断只读图不修正：按acc−conf符号判过/欠自信，全箱≤δ才校准；诊断样本须held-out且ECE+MCE同报，Brier须落Murphy三项；固定M的ECE须做M敏感性，排名翻转判不可采信 |

请豆包交叉验证来源与判重，经验按所属模块路由写入 D 盘对应模块文件。
