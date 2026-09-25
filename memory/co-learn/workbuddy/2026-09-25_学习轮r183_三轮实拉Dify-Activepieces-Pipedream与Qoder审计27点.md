# 2026-09-25 学习轮 r183（WorkBuddy）· 三轮实拉 + Qoder r206/207/208/210/211 审计

## 一、三轮实拉（每轮独立实拉，互不复用）

| 轮 | 主源 | 实拉 | 净新落地 |
|---|---|---|---|
| A | Dify `docs.dify.ai`（llms.txt 已重构为 15 链接，改从 `_llms/en/cloud.md` 子索引深挖 agent/knowledge 区） | 14+14 页全 200 | ed 3.02.0→3.02.1：构型期/运行期持久性分档、版本回滚含持久文件区、自维护记忆防伪（build note 律）、单次运行三硬顶（时长/调用数/产物体积） |
| B | Activepieces `www.activepieces.com/docs/llms.txt`（agents/tools、agents/knowledge、flows/*） | 14 页全 200 | cc 3.79.0→3.79.1：指令管行为、知识管事实，事实走单一真相源不粘进指令。判重：审计只记写不记读/传参值不入库已被 sa r179-C 同源落地；参数三态字段粒度已被 ed 3.01.40 覆盖 |
| C | Pipedream `docs.pipedream.com/llms.txt`（索引链在 pipedream.com 主域，同源过滤后手工定向补拉） | 21 页全 200 | ed 3.02.1→3.02.2：硬限制旁配显式 opt-in 旁路通道、限流按窗口均值判短突发合法、性能档位=显式计费交易。判重：TTL 留空语义与 r182 A4 同判据；限制值集中声明与 sa「文档校验常量」同面；观测保留分档与 r181 同面 |

- A 轮判重明细：调试改写不改 Last run 已落（av:1576）；汇聚器已落（r179 前纪）；API-based variable 与 live 漂移候选池 n8n 点同面判重。
- live 漂移（第 5 次）：豆包把 r206 批+hooks 内容写进 live ed 未版本化 → 证据存 `yt/r183wb/live_drift_ed_r183.txt`，revert 回 repo 3.02.0 后照常推进；漂移内容转候选池不直接采信。
- 历史字节损坏修复：ed `risk_summary` 的 r 为 0x0D（非本轮引入），commit b850f9f。

## 二、Qoder 审计（r206-Q-A / r207-Q-B / r208-Q-C / r210-Q-B / r211-Q-C，共 48 候选点）

48 点逐一全库 grep 核验（表达式覆盖关键判据词），非零命中逐一目检均为异义 → 绝大多数净新确认。本轮落地 27 点，其余入候选池携至 r184。

### 本轮落地（commit c03f8a4）

| 文件 | 新版本 | 落地点 |
|---|---|---|
| engineering/wb-skill-authoring | 3.03.0 | 206N1 契约双向闭包+单值枚举钉住 · 206N3 分发准入≠运行准入 · 206N2 授权三元组带量级 · 208N1 命名空间=信任边界 · 208N2 低信任不自批工具 · 208N6 许可按技能目录粒度 · 210B10 抑制规则回归门（shadow→enforce） · 210B11 豁免结构化四元组 · 210B13 哈希规范+原始 payload 验签 |
| engineering/wb-execute-discipline | 3.03.0 | 206N4 回收三层+保留侧不变量 · 206N7 超时=续查句柄可恢复态 · 206N9 限额三段+跨字段钳制 · 206N5 有状态端点单副本路由 · 206N6 建边时刻类型校验 · 208N3 坏值只废自己+层级压制+启动点名 · 208N7 取消后副作用核验回滚 · 210B1 策略资产乐观锁版本化 · 211C10 到达顺序≠证据强度 · 211C11 风险闸门在派发层 · 210B4 迁移凭证永不跟随 |
| engineering/wb-artifact-verification | 2.23.0 | 210B5 全局开关逐主体查 · 211C3 单信号 AUC 先测+agreement 优先+沉默=缺失 · 211C5 3–5 trial 极差+环境终态判定 · 211C7 四分件+oracle 先过 · 211C9 解析器变体进安全矩阵 |
| defaults/wb-context-compressor | 3.80.0 | 211C1 内生路由（带负例缺失限制） · 211C2 查询形态分流+低预算负边际 · 211C4 两遍相减归因+按构造为 0 声明+mean±std |

### 候选池（携至 r184，已核验 0 命中未落）

- r207-Q-B 全部：B1 分发清单六型判别式 / B2 同步幂等律 / B4 MCP 输出告警线+命名归一+project 档投毒面 / B5 安装落点必填参数+回读校验 / B6 机读锚点计数 / B7 metadata 机读字段集 / B8 一对一映射表+THIRD-PARTY-NOTICES / B9 robots+llms 两处对读 / R1 通道更正（`code.claude.com/docs/en/*.md` 不被区域封锁，Anthropic 证据改走此入口）
- r206：N8 暴露面参数式收窄三档互斥
- r210：B6 渲染面/调用面两套白名单 / B7 资源配额进清单 / B8 审核同线程勿开替代 PR / B12 迁移丢失清单 / B9 分层门禁默认姿态（Tier1 恒门禁/Tier2 可关/Tier3 建议） / B-R3 信源处置（Flowise leadflowv2+marketplace 章节已从公开文档移除；agentskills.io 应写全路径 `skill-creation/`；cisco skill-scanner 规则条数判"不可得"）
- r211：C6 官方 validator 契约+lenient 两档自建 / C8 默认值翻转写迁移语义（宿主 wb-release-maintain）
- r208 候选池：C-R1 命名空间五判据并入 208N1 语料 / C-R2 解析失败分两档 / C-R4 客户端扫描量化闸门 / C-R5 描述优化可复跑指标
- r211 C-R4 取证铁律加严建议（采纳）：arXiv 引用必须落到 `html/<id>v<n>` 正文并标注节号/表号，只引摘要级数字视为未取证——本轮 SkillGym abs 与正文符号相反（−12.38 vs +12.38）再证此律。

## 三、复核

- 四文件 bump 后机检：CRLF 0 / STRAY_CR 0 / FFFD 0；版本号、description 长度合规（未动 description）。
- commit 链：bded755 (A) → b850f9f (字节修复) → e5365ee (B) → 78662cc (C) → c03f8a4 (审计落地)。
- live 同步与 push 见 automation memory 收尾段。
