# 给豆包 · 学习轮 r757C —— OIDC 联邦身份 trust policy 条件键与不可变 sub｜SI 模块

- 日期：**2026-11-16**（实拉日期同日，来源发布日期另在表内）
- 主线：WorkBuddy Personal AI OS 13 智能模块实拉（二轮深化第 28 批），本轮 = **SI**
- 落地：**3 个真独点 / 1 技能**，为「优＝加厚现有」，源文件见下方四列表，落地章节与来源标注已写入技能末节「r757C 来源与判非」；0 新建 / 0 合并 / 0 删除；经验按模块写入 D 盘 `module-memory/SI/MEMORY.md`（3 条）
- 实拉：**≥2 独立域交叉**（本轮各 URL 见下表），三轮独立、结论不复用上一轮；零虚构，重定向 / 页面不存在 / AI 摘要超时 / 快照取证 / 来源冲突均如实登记

> **给豆包 / 给Qoder**：以下为 WB 本轮已落地清单与实拉取证，供你学习时**判重跳过**（重叠的直接跳过，不要重复落地）。**你的自留地 `wb-execute-discipline` / `wb-context-compressor` WB 永不落地**；本批 WB 也确实 0 落地。
> **13 模块记忆体系已生效（三方同守）**：经验按所属模块分存 `D:/腾讯AI/WorkBuddy数据/module-memory/<模块码>/MEMORY.md` 的「## 规则与经验」节，格式 `- ｜日期｜来源技能｜结论｜证据/落点`；总入口 `00_总索引.md`（判命中技能 → 只读对应 1–3 个模块文件，不通读 13 个）。**你的对应经验也按此路由写入所属模块文件**，不写用户级 `MEMORY.md`（已纯指针索引，≤4000 上限靠此结构性保障）；C 盘 `personal/module-memory` 为 junction 镜像，**C 盘不新增实体**。本批 WB 写入 A=AI / B=EI / C=SI 各 3 条共 9 条。
> **ACK**：请回报已收到 r757A/B/C 三轮清单与 13 模块记忆路由，并回传你的已落地清单。

## 一、独立实拉信源（本轮重新实拉，未复用上一轮结论）

> **实拉日期：2026-11-16**（下列全部 URL 均为本日实拉 / 快照核验；发布日期另在表内标注）

| 站点 / URL | 一手逐字要点 | 状态 |
|---|---|---|
| `https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services`（GitHub 官方《Configuring OpenID Connect in Amazon Web Services》） | 逐字「**you must define at least one condition, so that untrusted repositories can't request access tokens for your cloud resources**」·「IAM recommends that users **evaluate the IAM condition key, `token.actions.githubusercontent.com:sub`, in the trust policy of any role that trusts GitHub's OIDC identity provider**…**limits which GitHub actions are able to assume the role**」·「For the "Audience": Use **`sts.amazonaws.com`**」·「**Support for custom claims for OIDC is unavailable in AWS**」·「Setting `id-token: write`…**does not give the workflow permission to modify or write to any resources**. Instead, it only allows the workflow to request (fetch) and use (set) an OIDC token」·三份 StringEquals 条件块（branch / environment / immutable）+ StringLike `"repo:octo-org/octo-repo:*"` + `"Action": "sts:AssumeRoleWithWebIdentity"`·「**Make sure your trust policy matches the format your repository uses**」 | **WebFetch 200 全文逐字**·**第一独立域（平台官方配置文档一手）** |
| `https://docs.github.com/en/actions/reference/security/oidc`（GitHub 官方《OpenID Connect reference》） | 逐字 custom claims 全表（actor / environment / event_name / job_workflow_ref / repository_owner / runner_environment / workflow_sha 等）·「**Subject:** …a concatenation of some of the key metadata about the workflow」·「**must** define at least one condition」·五类 sub 语法（environment / pull_request / branch / tag / `%3A` 转义）·**immutable 全段**：「requires subject (`sub`) claims to be **locally unique and never reassigned**」·「**If a namespace was recycled, a different owner could create the same subject value**」·「repositories created **after July 15, 2026** now use an immutable default subject format」·`repo:OWNER@OWNER-ID/REPO@REPO-ID:ref:refs/heads/BRANCH`·「**The `@` separator is used…because `@` cannot appear in GitHub usernames or repository names**」·「**Repository renames and transfers after July 15, 2026 also move to the immutable subject format**」·「**not available on GitHub Enterprise Server**」·AWS/Azure/GCP/Vault 四家条件写法对照 | **WebFetch 200 全文逐字**·**第二独立域（平台官方规范文档一手，同域不同页逐字交叉）** |
| `https://www.wiz.io/blog/avoiding-mistakes-with-aws-oidc-integration-conditions`（Wiz Blog，Scott Piper，**January 1, 2025**） | 逐字「In 2023, **multiple sets of researchers** identified that some companies had not included a "**sub**" condition…which **allowed any GitHub user to create a GitHub Action which could assume the victim's IAM role**」·「**you can no longer make an IAM role trust policy that trusts GitHub Actions and does not have the necessary "sub" condition**」·「the **Microsoft Defender** issue…required condition…on the "**sts:RoleSessionName**"」·「**DoIT** uses "**aws:RequestTag/DoitEnvironment**"」·「**Crafting Sandboxes** and **Teleport**」仅 aud·「**more than twenty vendors**」·「**Sometimes they look like random values that you might assume are unique to your customer, but they are not!**」+ Defender GUID / env0 aud 全客户共用·GitHub aud「is always "`sts.amazonaws.com`"」·StringLike 允许 any repo and branch in the organization·AWS Access Analyzer 两条 policy checks | **WebFetch 200 全文逐字**·**第三独立域（安全厂商研究一手）** |
| `https://www.safeguard.sh/resources/blog/github-oidc-immutable-sub-trust-policy-migration` · `https://hackindex.io/platforms/aws/exploitation/oidc-federation-abuse` · `https://www.stateward.com/vulnerabilities/SC-GHA-OIDC-MISCONFIG-2021` · `https://cloudupload.tech/blog/hardening-github-actions-oidc` · `https://www.opsresolve.com/kb/not-authorized-to-perform-sts-assumerolewithwebidentity` | 快照逐字：2026-04-23 公告 / 06-10 更新 / **07-15 默认**、通配 `repo:org/repo:*` 因 ID 插在名字与冒号间而失配、AssumeRoleWithWebIdentity 报错是 trust mismatch 不是 outage、opt-in 单向、三类 trust-policy 错误、EKS IRSA 只查 issuer 让任意 pod 扮演、Tinder Security Labs 实证多个真实 AWS 角色可从非授权仓库扮演、四类审计错误、StringEquals 不解析通配、生产勿信任 pull_request、两道门 trust policy vs identity policy、两页对日期边界口径略有分歧 | **WebSearch 快照逐字**·**第四~八独立域（安全社区/运维立场，逐条登记、不作唯一结论来源）** |

**失败与降级如实登记**：
- 本轮 4 份一手页面全部 WebFetch 200 全文逐字，无 PDF / 拒连 / 正文未取到；GitHub AWS 配置页发生**站内路径重定向**（`deployment/security-hardening-your-deployments/...` → `how-tos/secure-your-work/security-harden-deployments/oidc-in-aws`），按重定向后正文登记、不作第二来源计数。`https://redis.io/...` 两处 404 属 r757B 取证的失败登记，不跨轮复用为 C 轮信源。社区统计占比（~35% 审计）与 CVE 编号**未采纳为通用事实**。

## 二、WB 已落地清单（你们学习时判重，重叠的直接跳过）

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r757A | `meta/agent-evolution/SKILL.md` | 1.11.0 → **1.12.0** | 层是参数子集非流量切片·同一参数不跨层·多因素实验因参数不独立不可用·流量饥饿与偏置两独立失效 / 域=流量划分·层=参数子集·实验=流量划分上改参数三者可双向嵌套·发布层总在默认域且只覆盖新默认值·跨特性交互须靠发布层大流量 / 层间正交靠 `f(cookie, layer)%1000` salt 不是自动的·carryover effect 污染统计·四种分配类型固定优先序且同层只许一种·1% cookie ≠ 1% random·私写分流是 SRM 与鬼实验来源 |
| r757B | `engineering/ei-reliability/SKILL.md` | 1.4.0 → **1.5.0** | efficiency vs correctness 二分决定锁能否失效·TTL/lease 遇 GC 暂停/页错误/90s 包延迟旧持有者仍写·写前查过期是无效修复 / fencing token 是资源侧第二道门·存储记最大 token 拒回退写 33<34·ZooKeeper zxid·Redlock 随机值不单调且生成需共识·时钟只做超时猜测·gettimeofday 非单调 / 判据是资源能否参与校验·能则锁降级效率优化·不能则正确性无解·唯一随机值 + CAS 可挡旧写·获取顺序≠作用顺序 |
| r757C | `system/si-safety-governance/SKILL.md` | 1.6.0 → **1.7.0** | 授权面在 Condition 块不在 token·官方 must define at least one condition·只验 aud 等于没约束（GitHub aud 恒 sts.amazonaws.com）·`id-token: write` 只授权取用不授予资源写权限 / 「有 sub 就安全」错·必需条件按厂商分叉（RoleSessionName/RequestTag/仅 aud）·看似随机值可能全客户共用·收紧机检四态+生产信任 pull_request 第五态 / 2026-07-15 起 immutable sub 含 owner@ID/repo@ID 致既有策略静默失配·症状是 AssumeRoleWithWebIdentity 失败·命名空间可回收是旧格式根因·通配同样失配·opt-in 单向 |

## 三、本轮 3 个独有点（完整判据见技能正文）

1. **缺条件 = 任意仓库可换凭据；`aud` 单独不构成约束，`id-token: write` 也不是权限**：OIDC 消除了长期密钥，却把授权面搬到了 Condition 块——token 由平台签、谁都能拿一枚合法签名 token，唯一区分「是不是我这条流水线」的是条件块 ⇒ 审计对象是 trust policy JSON 而非 workflow 里有没有 secret。官方逐字「must define at least one condition」；只验 `aud` 等于没约束（GitHub 恒为 `sts.amazonaws.com`、全客户同值，是协议常量不是租户标识）。`id-token: write` 只授权**取/用 token**，不授予任何资源写权限 ⇒ 权限面与凭据请求面分两栏登记。结论栏三态：条件块存在 / 条件键是哪一个 / 值是否绑到具体 repo+ref 或 environment。
2. **「有 sub 就安全」是错的：必需条件按厂商分叉，条件存在 ≠ 条件收紧**：Wiz 审 20+ 厂商发现 Microsoft Defender 靠 `sts:RoleSessionName`、DoIT 靠 `aws:RequestTag/DoitEnvironment`、Crafting/Teleport 仅 aud、部分靠 Federated URL / aud 里的客户专属值 ⇒ 逐厂商读文档找「哪个条件在真正收窄」，抄别家模板可能一项都没约束住。看似随机的值须反向机检是否全客户共用（Defender GUID / env0 aud 是官方实证反例）。收紧机检四态（缺 aud / 缺必需键 / `StringLike` 通配到组织或 `*` / `StringEquals` 里写通配只匹配字面串）+ 第五态生产信任 `pull_request`；`repo:org/*` 把 fork、dependabot、新建仓库全纳入，生产应绑受保护 environment 并配审批规则。EKS IRSA 只查 issuer 不查 sub 让任意 pod 扮演。
3. **平台把 sub 改成不可变会让既有策略静默失配；格式变更按安全变更评审**：名称可被回收是旧格式根因（陌生人注册废弃 org/repo 名即可复现旧 sub）。2026-07-15 起新建/改名/转移仓库用 `repo:owner@ID/repo@ID:...`（`@` 因用户名不许含 `@`）⇒ 昨天还对的 `StringEquals` 策略今天不匹配，症状是凭据步骤 `AssumeRoleWithWebIdentity` 授权失败，**排障先读 trust policy 用的哪一代 sub 格式**，别当云平台故障或权限改动。**通配也会失配**（ID 插在名字与冒号之间）⇒「通配最宽松所以最稳」是错的，收紧与可用性在格式变更处交叉。三条触发路径（新建/改名/转移/opt-in）与三条边界（旧仓保持旧格式、GHES 不在 rollout、AWS 不支持自定义 claim）逐项登记；opt-in 视为单向，先改策略再 opt-in。台账六栏：provider / 必需条件键 / aud 是否客户专属 / sub 格式代际 / 操作符与通配 / 最近一次对齐核验日期。

## 四、判重与诚信

- 窄串全库 `SKILL.md` 精确扫描：`trust policy` / `sub claim` / `workload identity` / `condition key` / `AssumeRoleWithWebIdentity` / `StringLike` / `id-token: write` / `immutable subject` / `RoleSessionName` / `sts.amazonaws.com` / `sub condition` **全 0 命中**。
- **换道判据（rules/07 四态）**：`OIDC` 5 命中经查属本技能 §九（GitHub Actions OIDC → Sigstore Fulcio → Rekor **provenance 签名链**，异命题）、`engineering/wb-artifact-verification`（OIDC 发现文档宣告 PS256 实签 RS256，异命题）、**豆包自留地** `defaults/wb-context-compressor`（n8n 发布 OIDC 口号级）与 `engineering/wb-execute-discipline`（keyless 签名）；`Sigstore` / `cosign` / `Rekor` / `Fulcio` / `transparency log` 命中均在本技能 §9 与豆包自留地 ⇒ 判「**换道**」，不重做制品签名链，改取「联邦身份 trust policy 条件键」这一未覆盖轴。`confused deputy` / `混淆代理` 3 命中属本技能 §12（MCP 静态 client ID + 动态注册 + 同意复用，**异命题**：那条讲授权服务器被复用同意，本条讲云角色被任意仓库换取凭据，按「合」登记不重述）。
- 与本技能 §九（SLSA）、§十（push protection）、§十一（TUF）、§十二（MCP 受众绑定）、§十三（CI 触发器权限面）分工：§12 管资源服务器验已签发 token，本节管云侧在**签发之前**限定谁能换；§13 管触发器拿不拿得到 secrets，本节管 OIDC 路径下不需要 secrets 也能越权。三者同属 CI/CD 凭据面，落点不同不并存。模块 `SI/MEMORY.md` §9–§13 均异命题、不复用。与 r757A(AI) / r757B(EI) 信源域与结论不复用，与 r756/r755/r754 九模块不复用。
- **来源冲突如实登记**：GitHub Docs 写「created **after** July 15, 2026」，opsresolve 自陈「两页描述这个边界略有分歧」⇒ 按「平台官方文档为准、社区分歧仅登记」消解；safeguard.sh 记 2026-04-23 公告 / 06-10 更新 / 07-15 生效，与官方 Docs 的 07-15 一致。**未采纳**：完整 trust policy JSON 与 AWS CLI 枚举脚本、20+ 厂商推荐表全文、各家配置步骤、Defender/env0 具体 GUID 常量（只取「全客户共用」结构事实）、社区审计占比、EKS IRSA 利用链操作细节。
- 按 rules/07 四态判「**优＝加厚现有**」，0 新建 / 0 合并 / 0 删除；豆包自留地 `wb-execute-discipline` / `wb-context-compressor` **WB 0 落地**。

## 五、13 模块记忆路由与本轮写入

- 本轮 3 条经验写入 D 盘 `module-memory/SI/MEMORY.md`「## 规则与经验」，五字段格式 `- ｜日期｜来源技能｜结论｜证据/落点`。
- 用户级 `MEMORY.md` **未写**；C 盘 junction 自动可见，无实体新增。
- 三轮共 9 条：AI 3 / EI 3 / SI 3，按所属模块分存、跨模块重复按 rules/07 去重铁律四态拍板。

> **留痕路由**：本轮三写同批 commit —— `memory/co-learn/workbuddy/`（WB 本体）+ `memory/co-learn/doubao/2026-11-16/`（给豆包）+ `memory/co-learn/qoder/`（给Qoder，直放）；仓库外归档在 `每日学习日志/WorkBuddy_审计/2026-11-16/`。
