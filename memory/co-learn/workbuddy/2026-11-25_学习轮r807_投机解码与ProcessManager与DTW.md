# 学习轮 r807（A/B/C）｜投机解码 · Process Manager 编排 · DTW 动态时间规整（WorkBuddy · 2026-11-25）

- 轮号：r807A/B/C（上批 r806A/B/C；co-learn r767–r806 续读无跳；Qoder 已卸载，共学两写 WB/豆包，qoder 目录 0 写入）。遵用户 2026-11-25 20:56 追加指令「把所有模块学3遍、学完再来3次」：13 模块固定顺序轮转，每模块累计 6 次，但计账台账始终把 KI 论文域排除、按 12 模块 4 组轮转；r807 取 KI 后排的 CI/OI/PI，避开 r806(VI/RI/MI)。用户追加指令 2026-11-25 20:56 起生效，除非另行取消不得提前停止或缩减。
- 选题：CI/OI/PI 三模块，实时体量 CI36619/OI37632/PI35563 B。首判候选全撞车换道：CI attention sink 已有 §r759B 专节 → 换投机解码；OI token bucket/选主/Saga 已有专节（§12/§14/§r738A）→ 换 Process Manager（全库 0 命中）；PI 首判即 DTW 全库 0 命中。三主题 SKILL.md + module-memory + co-learn 台账五层判重 0 专节 ⇒ 全「增＝加厚现有」0 新建。
- 判重：CI 投机解码仅豆包自留地 wb-context-compressor 一句口号（WB 0 落地），与 ci-context §r759B sink/§r802C MQA-GQA 异命题（那些管 KV 存什么怎么存，本轮管解码调度与分布不变）；OI Process Manager 在 personal-ai-employees 本体 0 命中（§r738A 补偿幂等键、§r800B outbox 均 CQRS 语境非机制专节），全库 Saga 命中属 ei-reliability/wb-execute-discipline（豆包自留地）/ki-knowledge-graph 异命题；PI DTW 全库 0 命中（§r801B mel/MFCC 前端异命题）。豆包自留地 wb-execute-discipline/wb-context-compressor WB 0 落地。
- 落地：3 轮 / 9 独点 / 3 技能加厚 bump / 0 新建；CI 383 / OI 352 / PI 228 行（均≤500），desc 1022/541/810（均≤1024），CR/FFFD=0，module 3/3，来源节 3/3。
- 实拉（每轮 ≥2 独立域一手，URL+日期逐条）：A=ecitis.org 一手技术全文 WebFetch 200 逐字（a=min(1,p/q) / p′=max(0,p−q) / 奖励 token / 拒绝丢后缀 / causal mask 并行验证 / cost=(C_D+C_T)/E[A] / 自适应 draft 长度 / 五项采样陷阱 / cache 回滚 / Medusa-EAGLE）+ arXiv:2211.17192 官方摘要 WebFetch 200 逐字（without any changes to the outputs / identical outputs / 2–3× / without retraining）+ wikizero/fullstackaihub WebSearch 交叉｜B=milanjovanovic.tech 一手全文 WebFetch 200 逐字（saga/PM 正交 / compensation is not a rollback / where is order 4712 stuck / 五条 plumbing / 补偿一等业务操作）+ Microsoft Azure Saga 官方页 WebFetch 200 全文逐字（compensable/pivot/retryable 三分类 / pivot=point of no return / choreography vs orchestration 利弊 / 数据异常五缓解）+ ddd-fans/praveentn WebSearch 交叉｜C=tslearn 0.11 官方文档 WebFetch 200 全文逐字（优化式与路径四性质 / O(mn) DP 伪码 / not a valid distance since it does not satisfy the triangular inequality / Sakoe-Chiba 带 / Itakura 斜率 / soft-DTW soft-min+log-sum-exp）+ 百度百科科普中国审核 WebFetch 200 全文逐字（Itakura 60 年代 / 压扩 / warping path 三约束逐条 / 孤立词模板匹配）+ wikiprompt/百度智能云 WebSearch 交叉。诚信降级如实登记：A HuggingFace 官方文档 WebFetch 失败未采纳；C 百度百科公式以图片形式给出未逐字转录、以 tslearn 官方公式为准。

## 三轮固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r807A | defaults/ci-context/SKILL.md | 2.11.0 | 投机解码：无损来自接受规则 a(x)=min(1,p/q)+残差 max(0,p−q) 修正非 draft 猜得准（arXiv 摘要 identical outputs、T5-XXL 2–3×）；四阶段环（draft 提 k→目标一次并行验证 causal mask→首位拒绝采残差并丢弃其后所有 draft→全接受额外采 1 奖励 token），速度量=每目标趟承诺 token 数 E[A] 非 draft 准确率；失效面=高熵/OOD/高温降接受率+高 batch 反降吞吐、两边采样口径须一致（temp/mask/精度/随机数）、词表兼容与分页 cache 回滚、Medusa/EAGLE 去独立 drafter |
| r807B | meta/personal-ai-employees/SKILL.md | 1.14.0 | Process Manager：Saga（本地事务+补偿，补偿非回滚是另一笔可见交易）与 PM（持有显式状态、消费事件产命令的有状态机）是 coordination 与 failure-handling 正交两轴可共存；状态放哪定可运维性（协同 saga 无中心状态「where is order 4712 stuck」须跨服务关联，PM 持久化状态暴露步骤/deadline），选型=线性低风险用 choreography、有分支/超时/人工/钱用 PM；可靠性五硬约束（状态+消息同事务 outbox/参与者幂等/协调 inbox 去重/并发令牌重载重评估/稳定 operation ID 处理不明结果）+ pivot 不可逆点三分类 |
| r807C | media/pi-audio/SKILL.md | 1.7.0 | DTW：解同内容语速不同对齐、非线性映射时间轴使累计距离最小（Itakura 60 年代孤立词模板匹配），tslearn 形式化 min_π √(Σd²)；规整路径三约束（边界左下→右上/连续性相邻点不跨点/单调性不倒退）+ O(mn) DP 递推 C[i,j]=d²+min(三前驱) 是全部机制；两语义坑=不满足三角不等式非合法距离、无约束病态对齐须 Sakoe-Chiba 带/Itakura 斜率收窄，soft-DTW 用 log-sum-exp soft-min 替 min 可微 |

## WB 已落地清单（防重复）
  - r807A CI｜defaults/ci-context/SKILL.md 2.11.0｜投机解码 三独点
  - r807B OI｜meta/personal-ai-employees/SKILL.md 1.14.0｜Process Manager 三独点
  - r807C PI｜media/pi-audio/SKILL.md 1.7.0｜DTW 三独点

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像、无实体）。豆包的对应经验也按此路由写入所属模块文件（本批 CI/OI/PI 各 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`），两方同守；Qoder 已于 2026-11-23 卸载，`co-learn/qoder/` 席位已移除，禁止再写该目录。用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障，本批未写入）。

本批为 r807A/B/C 独立实拉留痕，三轮标准一致、禁止复用 r806 结论。下批 r808A/B/C 按 13 模块固定顺序取 SI/AI/PDI（KI 论文域排除，避开 r807 CI/OI/PI）；每模块累计计数按台账续（CI/OI/PI 本批后各 2–3/6，SI/AI/PDI 待本批后计）；Qoder 席位已移除仅两写。
