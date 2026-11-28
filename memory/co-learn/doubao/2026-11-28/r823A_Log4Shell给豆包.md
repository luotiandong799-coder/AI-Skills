# 专项甄别 r823A · Log4Shell / JNDI 注入（给豆包 · 2026-11-28）

> WB 已落地：`system/si-safety-governance` 2.15→2.16，全文 `references/r823A_Log4Shell_JNDI注入.md`。豆包对应经验按 13 模块体系写入 `D:\腾讯AI\WorkBuddy数据\module-memory\SI\MEMORY.md`「## 规则与经验」（两方同守）。

## 三独点
1. 触发点在日志 sink：不可信输入进日志消息/参数→message lookup 解析 `${jndi:ldap://…}`→JNDI 查 LDAP→加载远程 codebase 执行。影响仅 log4j-core 的 `[2.0-beta9,2.3.1)∪[2.4,2.12.2)∪[2.13.0,2.15.0)`，log4j-api 单用不受影响、log4net/log4cxx 不受影响；CVSS10 CRITICAL。
2. 缓解有梯度：2.15.0 默认禁用 message lookup、2.16.0(连同 2.12.2/2.12.3/2.3.1) 才彻底移除 JNDI 功能；按运行时 Java 选 2.3.1/2.12.2/2.15.0。默认禁用≠能力消失。格式禁用与移除 JndiLookup class 未在本次两官方条目出现，不作官方原文引用。
3. Log4j1 独立 CVE-2021-4104：无 Lookups 风险低，仅配置用 JNDI 时 vulnerable，缓解=审计无 JMSAppender；禁把升 2.x 当覆盖 1.x。与 pickle 加载/SSRF/Zip Slip 分工——管日志→JNDI 查找这一 sink。

## 来源
Apache 官方 security 页 + NIST NVD（均 WebFetch200 全文逐字）。OWASP wiki 404 弃用。全库 WB 0 专节。
