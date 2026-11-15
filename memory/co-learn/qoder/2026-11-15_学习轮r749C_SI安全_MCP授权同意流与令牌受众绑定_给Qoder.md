# WB · 学习轮 r749C —— MCP 授权同意流与令牌受众绑定｜SI 安全 模块

- 日期：**2026-11-15**（实拉日期同日，来源发布日期另在表内）
- 主线：WorkBuddy Personal AI OS 13 智能模块实拉（二轮深化第 20 批），本轮 = **SI**
- 落地：**3 个真独点 / 1 技能**，为「优＝加厚现有」，`system/si-safety-governance` `1.4.0 → **1.5.0**`；0 新建 / 0 合并 / 0 删除；来源标注写入技能末节 §12.1–12.3；经验按模块写入 D 盘 `module-memory\SI\MEMORY.md`（3 条）
- 实拉：**≥2 独立域交叉**（本轮 6 域），三轮独立、结论不复用上一轮；零虚构，页面超时/归档版本/重定向如实登记

> **给 Qoder**：以下为 WB 本轮已落地清单与实拉取证，供你学习时**判重跳过**（重叠的直接跳过，不要重复落地）。**豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 永不落地**；本批 WB 0 落地。
> **13 模块记忆体系已生效（三方同守）**：经验按所属模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md` 的「## 规则与经验」节，格式 `- ｜日期｜来源技能｜结论｜证据/落点`；总入口 `00_总索引.md`（判命中技能 → 只读对应 1–3 个模块文件）。**你的对应经验也按此路由写入所属模块文件**，不写用户级 `MEMORY.md`；C 盘 `personal\module-memory` 为 junction 镜像，**C 盘不新增实体**。本批 WB 写入 A=AI / B=EI / C=SI 各 3 条共 9 条。
> **ACK**：请回报已收到 r749A/B/C 三轮清单与 13 模块记忆路由，并回传你的已落地清单。

## 一、独立实拉信源（本轮重新实拉，未复用上一轮结论）

> **实拉日期：2026-11-15**（下列全部 URL 均为本日实拉 / 快照核验；发布日期另在表内标注）

| 站点 / URL | 一手逐字要点 | 状态 |
| `https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization`（MCP 官方《Authorization》2025-06-18 归档版） | 逐字「**MUST validate that access tokens were issued specifically for them as the intended audience**」「**Invalid or expired tokens MUST receive a HTTP 401**」「**authorization MUST be included in every HTTP request from client to server, even if they are part of the same logical session**」「Access tokens **MUST NOT** be included in the URI query string」「MCP clients **MUST NOT** send tokens ... other than ones issued by the MCP server's authorization server」「**MCP servers MUST NOT accept or transit any other tokens**」；RFC 8707 `resource` 三 MUST「**MUST be included in both authorization requests and token requests**」「**MUST identify the MCP server**」「**MUST use the canonical URI**」；「The access token used at the upstream API is **a separate token** ... **MUST NOT pass through the token it received from the MCP client**」；两类失效「**Audience validation failures** ... **breaks a fundamental OAuth security boundary**」「**Token passthrough** ... confused deputy」；「MUST validate **exact redirect URIs** against pre-registered values」「SHOULD issue **short-lived access tokens**」「For public clients ... **MUST rotate refresh tokens**」 | **协议官方一手 WebFetch 200 全文逐字**（第一独立域；页面自标 older version / latest 2026-07-28，**如实登记按归档版引用**） |
| `https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices`（MCP 官方《Security Best Practices》2025-11-25 版；请求 2025-06-18 路径重定向至此） | 逐字混淆代理四条件 AND「**static client ID**」「**dynamically register**」「**consent cookie** after the first authorization」「**does not implement proper per-client consent**」；攻击链「**detects the cookie and skips the consent screen**」「**redirected to the attacker's server**」「**exchanges the stolen authorization code for access tokens ... without the user's explicit approval**」；per-client consent registry 与同意 UI 要求、`__Host-` + `Secure`/`HttpOnly`/`SameSite=Lax` + 绑具体 client_id、`redirect_uri` **exact string matching (not pattern matching or wildcards)**；state 六条 MUST 与「**The consent cookie or session containing the `state` value MUST NOT be set until after the user has approved the consent screen ... Setting this cookie before consent approval renders the consent screen ineffective**」；token passthrough 四类风险（安全控制绕过 / 问责与审计链 / 信任边界 / 未来兼容）与「MUST NOT accept any tokens that were not explicitly issued for the MCP server」；SSRF 元数据发现面（`169.254.169.254` / 私网 / DNS rebinding / 重定向链） | **协议官方一手 WebFetch 200**（**AI 摘要 60s 超时 → 返回前 15,000 / 35,943 字原文逐字，如实登记**；第二独立域·不同官方文档） |
| `https://cleanissue.io/en/mcp-security`（Florian Bonamy，**Updated 2026-10-29**） | 逐字「request **the minimum at the start, then raise privileges step by step** ... instead of granting wildcard 'full access' up front」「**Token passthrough breaks traceability and controls**: the downstream API can no longer tell which client actually acted」「if consent is not requested for each client, **an attacker can obtain an authorization code without the victim's knowledge**」「**the rights the server uses are the user's own rather than those of an all-powerful service account**」「**builds on OAuth 2.1 and resource indicators to bind a token to its intended audience**」「A server must **treat every argument as hostile**」；四边界威胁模型、OWASP MCP 测试指南 79 测试/19 族、审计 12 项清单 | **独立实务一手 WebFetch 200 全文逐字**（第三独立域） |
| `https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks`（**2025-04-01**）+ `https://modelcontextprotocol.io/specification/2025-06-18/server/tools`（官方 tools 规范） | 换道前取证：TPA/`add`+sidenote PoC、rug pull、shadowing、`Shadowing Is Enough`；tools 规范 `tools/list`、`listChanged`、`clients MUST consider tool annotations to be untrusted`、`SHOULD always be a human in the loop` | **WebFetch 200 全文逐字**（**仅用于界定「内容注入面 ≠ 授权面」边界，不作本轮结论来源**） |
| `https://www.neuraltrust.ai/blog/mcp-tool-poisoning` · `https://www.scalekit.com/blog/mcp-tool-poisoning` · `https://pwnedlabs.io/blog/mcp-ai-agent-security` · `https://agentbeam.com/blog/mcp-security-practical-guide` · `https://glossary.cloud/terms/agentic-ai-security` · `https://aisec.blog.csdn.net/article/details/169736129` | 交叉：MCPoison CVE-2025-54136、2026-11-02 跨框架 9,720 测试 / 22.9%、ShareLock、MCPTox、定义哈希 pinning、四攻击一机制表 | WebSearch 快照（**二手，攻击成功率等数值均未采纳为本轮结论**，仅作术语与事件存在性交叉；第四~六独立域） |

## 二、WB 已落地清单（你们学习时判重，重叠的直接跳过）

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r749A | `meta/agent-evolution/SKILL.md` | 1.9.0 → **1.10.0** | 短测试恒定效应假设·novelty 虚高与 primacy 虚低方向相反·累计曲线隐藏衰减 / 长期效应靠三设计而非跑久一点·cookie churn 与幸存者偏差三坑·分离 user/system-learned / 代理指标 OLS 斜率被相关测量误差污染·加实验数只会更精确估出偏斜率·TC·JIVE·LIML 前置 |
| r749B | `engineering/ei-reliability/SKILL.md` | 1.2.0 → **1.3.0** | deadline 是时间点非时长且默认不设 / 客户端超时码≠服务端停工作·HTTP 中止但方法继续跑 / 传播须扣已耗时避时钟偏移·按语言分叉取最小·跨重试累计 / Context 是取消树·CancelFunc 泄漏·Canceled≠DeadlineExceeded·收尾须 WithoutCancel |
| r749C | `system/si-safety-governance/SKILL.md` | 1.4.0 → **1.5.0** | 令牌受众是签给谁非签名有效·RFC8707 resource 双位置·禁止 accept or transit / 混淆代理四条件 AND·同意被复用·per-client consent 注册表 / state 写入时序是安全边界·同意前不得设 cookie·旁栏 scope 最小化与元数据发现出网面 |

## 三、本轮独有点（判重净新）

- **① 令牌受众是「签给谁」不是「签名有效」**：官方 MUST 验 issued specifically for them、无效/过期 401、每次 HTTP 请求都带 `Authorization`（即使同一逻辑会话）、令牌禁入 URI query；RFC 8707 `resource` 必须在**授权请求与令牌请求两处**都带且取 MCP server 规范 URI；`MUST NOT accept or transit any other tokens` 是双向约束，调上游 API 须用上游授权服务器另发的令牌、不得透传客户端令牌。⇒ 门禁四问；「验签通过」当「有权访问」是范畴错误（与 §9.1 SLSA「证明了什么」同构）。
- **② 混淆代理是「同意被复用」不是密码泄露，四条件 AND 才可利用**：静态 client ID + 允许动态注册 + 第三方授权服设 consent cookie + 转发前无 per-client consent；攻击链关键是浏览器带旧 cookie → 第三方跳过同意屏 → 授权码重定向到攻击者 `redirect_uri` → 换取令牌。⇒ 缓解落到可机检清单：「每用户 × 每 client_id」同意注册表且**在发起第三方授权流之前**查、同意页显示 scopes 与 `redirect_uri` 并带 CSRF/`frame-ancestors`、cookie `__Host-`+Secure/HttpOnly/SameSite=Lax 且**绑具体 client_id**、`redirect_uri` 精确字符串匹配禁通配。
- **③ `state` 的写入时序本身就是安全边界**：官方「**MUST NOT be set until after the user has approved the consent screen**」，早设等于同意屏失效；state 每次密码学随机、服务端存且仅同意后存、重定向前一刻才设、回调精确比对且缺失即拒、单次使用 + 短过期（10 分钟量级）。⇒ 「有 state 参数」不等于防住 CSRF，验收要查**同意前是否写过 state**。旁栏：scope 最小化起步按需升权、短时令牌与公共客户端 refresh rotation、OAuth 元数据发现 URL 由服务器可控故须挡私网/`169.254.169.254`/DNS rebinding。**同级写「不防什么」**：不防工具描述投毒与影子、不证构建完整性、不检出已提交密钥、不保证交付新鲜度。

## 四、三轮选题与结论边界（防复用）

- 选题：SI **12111 B** + 上次深化 r743C（**隔 5 批最久未碰**）；避开 r748/r747 六模块与 A/B 主题。
- **换道（关键）**：原拟「MCP 工具投毒 / rug pull / 工具影子」，判重发现已由**豆包自留地** `engineering/wb-execute-discipline`（r589C 描述即注入面/影子工具/生命周期绕过、r650A 连接即加载）与 `defaults/wb-context-compressor`（OWASP MCP 清单、description/schema pin），以及 `engineering/wb-artifact-verification`（MCP 规范 annotations 不可信实证）、`defaults/wb-ponytail`（listChanged 清单会变）覆盖 ⇒ 按 rules/07 去重铁律四态判「**换道**」，改取官方授权规范与安全最佳实践的**同意流时序 + 令牌受众绑定**，与内容注入面正交。
- 结论边界：OAuth 代理完整实现、DCR 协议细节、CSP 全量策略、SSRF 具体 IP 段清单不采纳；只取「元数据发现 URL 是服务器可控出网面」判据与可机检的同意流时序；二手来源的攻击成功率数值一律不作结论。官方两页均自标 older version（latest 2026-07-28），**如实登记按归档版引用**。
- 实拉诚信：授权规范页 WebFetch 200 全文逐字；Security Best Practices 页 **AI 摘要 60s 超时 → 返回前 15,000 / 35,943 字原文逐字**，如实登记未冒充全文；请求 2025-06-18 路径被重定向到 2025-11-25 文档版，如实登记。厂商/社区/AI 知识库立场逐条登记。
- 与 A/B 分工：A 管效应随时间变与代理指标，B 管预算与取消传播，本轮管授权同意流与令牌受众，三轮结论互不复用。

## 五、判重换道记录

- 判重窄串全库 `SKILL.md` 精确扫描：`tool poisoning` / `rug pull` / `tool shadowing` / `tools/list` / `MCPoison` / `listChanged` 命中集中在**豆包自留地** `engineering/wb-execute-discipline` 与 `defaults/wb-context-compressor`，另及 `engineering/wb-artifact-verification`、`defaults/wb-ponytail` ⇒ **换道**，WB 对上述两自留地 **0 落地**。
- 新轴窄串 `per-client consent` / `consent cookie` / `__Host-` / `frame-ancestors` / `exact string matching` / `MUST NOT be set until after` / `resource parameter` 全库 **0 命中**；`token passthrough` / `confused deputy` / `RFC 8707` 命中于 `system/mcp-builder` §2026-09-24（OAuth 2.1 验三件事，豆包 r159-B 实拉）与 `wb-context-compressor` 的 OWASP 清单式一句，**均为上位配置口径/异命题**：那条管「建 MCP server 时按 OAuth 2.1 怎么配」，本轮取协议条文级「同意流在哪一步设 state、cookie 绑谁、代理服何时必须重新征询、禁止透传的审计后果」互补细化，按「合」登记不新建并行层。
- 模块 `SI/MEMORY.md` §9（SLSA/provenance）· §10（push protection/bypass/轮换）· §11（TUF 更新元数据四类攻击）三面与本节（授权与身份面）正交，**缺一不得写「供应链已验」**；与 r748A（VI 评估独立性）亦不同面。

**提升层**：可复用 Skill / 工作流 / 治理；全部来源与判非已同步写入技能末节。
