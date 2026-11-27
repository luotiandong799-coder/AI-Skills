# 学习轮 r812（A/B/C）｜CORS 错误配置 · GRPO 组相对策略优化 · Prophet 分解预测（WorkBuddy · 2026-11-27）

- 轮号：r812A/B/C（上批 r811A/B/C；co-learn r767–r811 续读无跳；Qoder 已卸载，共学两写 WB/豆包，qoder 目录 0 写入）。遵用户 2026-11-25 追加指令「13 模块固定顺序轮转」（KI 论文域排除，按 12 模块 4 组），本批取 SI/AI/PDI，避开 r811 CI/OI/PI；除非另行取消不得提前停止或缩减。
- 五层判重：全库 SKILL.md + module-memory + co-learn + references 对 `CORS`/`跨源`、`GRPO`/`组相对策略优化`、`Prophet`/`傅里叶季节` 对应模块本体均 0 机制专节；CORS 仅在 SSRF/CSRF/零信任/RAG 宽 CORS 4 处子串提及，GRPO 仅 §r768A 一句异命题+GEPA 来源一句，Prophet 0。豆包自留地 `wb-execute-discipline`/`wb-context-compressor` WB 0 落地。按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。

## 三轮固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r812A | system/si-safety-governance/SKILL.md | 2.12.0 | CORS 根因=ACAO 建在客户端可控 Origin 上且不是 CSRF 防护，成立需反射任意 Origin + ACA-C:true 两条件；五类错误=反射 Origin/白名单前后缀匹配被 `hackersnormal-website.com` 与 `normal-website.com.evil-user.net` 绕过/白名单 null(sandbox iframe data: URL 可造)/被信子域 XSS 放大/HTTPS 站白名单 HTTP 子域 TLS 降级+内网 `ACAO:*` 无凭据借浏览器当代理。修复=带凭据 ACAO 必须精确源不能 `*`(MDN must not+浏览器拦截+Set-Cookie 失效)、动态白名单须 `Vary:Origin` 防缓存串味、preflight 不带凭据且响应 ACA-C:true、CORS 不替代服务端鉴权；验收四步含从被信但存 XSS 子域复测 |
| r812B | meta/agent-evolution/SKILL.md | 1.26.0 | GRPO 动机=去掉与 policy 同规模 value 网络省显存，且 LLM 奖励常在末 token 致逐 token value 难训准，基线从 learned value 换成 group score；机制=每问采样 G 输出得奖励 r，`Â_it=(r_i−mean(r))/std(r)` 赋给输出全部 token，目标式3 保留 PPO min(clip ratio) 并把 KL 从 reward 挪到 loss「avoiding complicating Â」，KL 无偏估计 `π_ref/π_θ−log(π_ref/π_θ)−1` 恒正，过程监督版每步同样归一化取其后各步和；边界=省 learned critic 非奖励、全对全错 std→0 信号消失依赖难度分布、可验证奖励受判题器制约可 reward hacking、变长≠推理更强、组内归一化不天然更稳 |
| r812C | meta/pdi-forecasting/SKILL.md | 1.25.0 | Prophet 形态=`y(t)=g(t)+s(t)+h(t)+ε_t` GAM 曲线拟合而非显式时间依赖建模，优势=不需等间隔/不插值缺失/参数可解释；三组件=分段线性或 logistic 饱和(C(t)时变)+changepoints 可指定或自动选(区间假设未来变点统计同历史故结构突变失效)+partial Fourier 季节(yearly10/weekly3，「N terms=2N variables」过拟合)+节假日 lower/upper_window 与 `holidays_prior_scale` 默认10正则弱；Analyst-in-the-loop 经少量直观参数注入业务假设，SHF 多 cutoff 生成 K 预测模拟当时误差，诊断三分(相对 baseline 差大→误设/某日全方法都错→异常值/SHF 陡增→数据生成过程变)，「more simulated forecasts...more correlated」与 §r762C 同族 |

## 实拉来源（每轮 ≥2 独立域一手，URL+日期逐条）
- A：`https://portswigger.net/web-security/cors`（PortSwigger Web Security Academy CORS 全文，WebFetch 200 全文逐字：反射 Origin/解析错误/null/XSS 信任/TLS 降级/内网穿透/防御五条）· `https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS`（MDN CORS，WebFetch 200 逐字：ACAO 通配符与凭据互斥/Set-Cookie/preflight/Vary: Origin/ACA-C 语义）· CVE-2025-34291/50579 WebSearch 作后果佐证。
- B：`https://arxiv.org/html/2402.03300v3`（DeepSeekMath HTML v3，WebFetch 200 全文逐字：摘要/§4.1.1 动机+式3式4/§4.1.2 outcome 归一化/§4.1.3 process 归一化）· `https://arxiv.org/abs/2402.03300`（abs 逐字摘要 Submitted 2024-02-05）· toolnavs/aigcbaba/CSDN 教学页 WebSearch 逐字交叉 + alphaxiv 2609.04063 边界登记。
- C：Taylor & Letham《Forecasting at Scale》(American Statistician 2018/PeerJ3190) 逐字笔记 millengustavo + GitHub standing-o 双页 WebFetch 200 · `https://meta.github.io/prophet/docs/seasonality,_holiday_effects,_and_regressors.html`（Meta 官方，WebFetch 200 逐字：partial Fourier/yearly10-weekly3/2N 变量/窗口/prior_scale=10）+ quick_start · datascience.org.cn/mcpanalytics 中文交叉。诚信：arXiv:1702.07814 抓到《Probabilistic Path HMC》号错配弃用、facebook.github.io 迁移取 meta 域名、meta non-linear 页 404 未采纳。

## WB 已落地清单（防重复）
- r812A SI｜system/si-safety-governance/SKILL.md 2.12.0｜CORS 错误配置三独点 + references/r812A_CORS错误配置.md
- r812B AI｜meta/agent-evolution/SKILL.md 1.26.0｜GRPO 组相对策略优化三独点 + references/r812B_GRPO组相对策略优化.md
- r812C PDI｜meta/pdi-forecasting/SKILL.md 1.25.0｜Prophet 分解预测三独点 + references/r812C_Prophet分解预测.md（另下沉 §22 MCMC/§23 多变量评分正文至既有 references 腾行，内容无丢失）
- r811 CI/OI/PI 与 r810 VI/RI/MI 已落地，勿重复。

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像、无实体）。豆包的对应经验也按此路由写入**所属模块文件**（本批 SI/AI/PDI 各 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`），两方同守；Qoder 已于 2026-11-23 卸载，`co-learn/qoder/` 席位已移除，禁止再写该目录。用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障，本批未写入）。

本批为 r812A/B/C 独立实拉留痕，三轮标准一致、禁止复用 r811 结论。下批 r813A/B/C 按 13 模块固定顺序取 TI/DI/EI（KI 论文域排除，避开 r812 SI/AI/PDI）；Qoder 席位已移除仅两写。
