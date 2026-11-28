# 学习轮 r823（A/B/C）· Log4Shell(JNDI) / RND好奇心探索 / MIDAS混频预测（WorkBuddy · 2026-11-28）

- 轮号：r823A/B/C（上批 r822A/B/C；co-learn r767–r822 续读无跳；Qoder 已卸载，共学两写 WB/豆包，qoder 目录 0 写入）。
- 模块：SI 安全 / AI 自适应 / PDI 预测（按 13 模块固定顺序轮转，KI 论文域排除，避开 r822 VI/RI/MI）。
- 五层判重：全库 SKILL.md + module-memory + co-learn + references 对 `Log4Shell`/`CVE-2021-44228`/`JNDI注入`/`RND`/`随机网络蒸馏`/`好奇心探索`/`MIDAS`/`混频`/`nowcast` WB 侧 0 机制专节（SI 的 §8.3 pickle 加载、§15 SSRF、§18 Zip Slip 均异命题；AI 的 §r717A 探索利用门/§r788A PBRS/§r792B 课程学习异命题；PDI 的 §r820C ARIMA/§r795M 层级协调异命题）；全「增＝加厚现有」0 新建。
- 经验按 13 模块体系写入 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`），豆包对应经验同路由写所属模块文件，两方同守；用户级 MEMORY.md 未写（纯指针化，≤4000 结构性保障）。C 盘仅 junction 镜像，无实体新增（md5 三处一致）。

## 三轮固定四列表

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r823A | `system/si-safety-governance/SKILL.md` | 2.15.0→2.16.0 | Log4Shell=CVE-2021-44228 触发点在日志 sink（消息/参数→lookup→JNDI→LDAP 加载代码）；影响仅 log4j-core 的版本区间+CVSS10；默认禁用(2.15.0)≠功能移除(2.16.0)按运行时 Java 选版本；Log4j1 独立 CVE-2021-4104 走 JMSAppender 审计不与 2.x 混 |
| r823B | `meta/agent-evolution/SKILL.md` | 1.29.0→1.30.0 | RND 固定随机 target+可训练 predictor 的 MSE 内在奖励，误差三因只有 epistemic 可用、确定性目标避开 noisy-TV、越访越熟不 stale；双 value 头 V=V_E+V_I+non-episodic 内在/episodic 外在（防自毁重开循环）；两层归一化(奖励 running std + 观测白化 clip)四件验收口径 |
| r823C | `meta/pdi-forecasting/SKILL.md` | 1.28.0→1.29.0 | MIDAS 高低频不等频不先压到低频（简单加总等权失真）、属分布滞后非 ARIMA、Y_t=β0+B(L^{1/m})X_t^(m)+ε；函数化约束 d→q 但转 NLS/QMLE 不免费、U-MIDAS 与 step 是约束谱两端；报五件+适用边界+不给因果识别/conformal 覆盖 |

## 实拉来源（每轮 ≥2 独立域一手）

- A：`https://logging.apache.org/log4j/2.x/security.html`（WebFetch 200 全文逐字：CVE-2021-44228 summary/CVSS10/受影响版本区间/修复版本/log4j1 JMSAppender 缓解）+ `https://nvd.nist.gov/vuln/detail/CVE-2021-44228`（WebFetch 200 逐字：官方描述 2.15.0 默认禁用→2.16.0 完全移除/CVSS 向量）。诚信：OWASP wiki 旧路径 404 弃用；`formatMsgNoLookups`/移除 JndiLookup class 不在本次两官方条目内，不作官方原文引用。
- B：`https://arxiv.org/abs/1810.12894`（WebFetch 200 摘要逐字：bonus=预测误差/Montezuma 超人类平均）+ `https://ar5iv.labs.arxiv.org/html/1810.12894`（WebFetch 200 全文逐字：§2.2 RND 双网络/§2.2.1 误差三因 Factor1/§2.3 双 value 头+non-episodic/§2.4 两层归一化/Algorithm1）+ alphaXiv/Walking Labs/kg.rounds-tech WebSearch 逐字交叉（noisy-TV、γ_E/γ_I）。诚信：OpenAI blog 404、Lilian Weng 与 arxiv/html 直连 WebFetch 本地回退禁用如实登记。
- C：`https://escholarship.org/content/qt9mf223rs/...pdf` + `https://rady.ucsd.edu/_files/faculty-research/valkanov/midas-touch.pdf`（Ghysels/Santa-Clara/Valkanov 原论文 WebSearch 快照逐字：摘要/引言/线性 MIDAS 式/非自回归）+ `https://www.stata.com/meeting/china20-Uone-Tech/slides/China20_Wang_Q1.pdf`（Stata 官方 midasreg 逐字：加总等权缺陷/函数/U-MIDAS/step）+ `https://www.cirano.qc.ca/en/summaries/2004s-20`（CIRANO 官方摘要）+ `https://lianxh.cn/news/8ab193e6f04cc.html`（连享会逐字：d→q/NLS·ML）。诚信：两 PDF 的 WebFetch 受本地回退禁用/CloudFront403，取 WebSearch 原文快照不冒充 200。

## WB 已落地清单（防重复）

Log4Shell `references/r823A_Log4Shell_JNDI注入.md` · RND `references/r823B_RND好奇心探索.md` · MIDAS `references/r823C_MIDAS混频预测.md`；另 AI 旧节 §r801C SAC 全文下沉 `references/r801C_SAC软演员评论家.md` 腾行（内容零丢失）。三技能加厚 bump，9 条模块经验入 D 盘；详见对应 SKILL.md §r823A/§三十八/§三十五 摘要节。下批避开 SI/AI/PDI（按 13 模块顺序取 VI/RI/MI，KI 论文域排除）。
