# r796K｜SI｜CSP 内容安全策略：纵深防御第二层，先 report-only 观测再强制

访问日期：2026-11-22；每轮独立实拉禁止复用上轮。

## 一手来源逐字

- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP（MDN 官方，WebFetch 200 逐字：纵深防御 XSS/不替代输入净化/nonce-hash 忽略 unsafe-inline/report-only）

- https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html（OWASP 官方，WebFetch 200 逐字：强 CSP 是第二层/不可作唯一防线/report-only 是强制前奏）

- https://www.w3.org/TR/CSP3/（W3C 官方标准，WebFetch 200 逐字：Report-Only 只观察不强制/strict-dynamic/不替代输入验证与输出编码）

## 独有点

1. 定位判据：CSP 是纵深防御第二层，MDN/OWASP/W3C 三处一致——「not an alternative to sanitizing input」「not a replacement for careful input validation and output encoding」；判据——把 CSP 写成输入转义替代品、或唯一防线，判违规。MDN 逐字：provide a defense in depth against XSS, protecting the website even if sanitization fails。

2. nonce/hash 判据：指令含 nonce 或 hash 时浏览器忽略 `unsafe-inline`；CSP3 的 `strict-dynamic` 允许带 nonce/hash 的脚本加载更多脚本，MDN 明确这会降低安全性，须显式声明为何需要。判据——同时写 `unsafe-inline` 与 nonce 却以为更严格，判理解错误。

3. 上线顺序判据：先发 `Content-Security-Policy-Report-Only` 只上报不拦截（W3C/OWASP 逐字：precursor to blocking mode / fail closed），观测后再切强制 `Content-Security-Policy`；`default-src` 是其余 fetch 指令的 fallback，`default-src 'self'` 为同源兜底。JSONP/AngularJS 具体绕过面本轮未取一手，不得写成已验证。

## 判重与判非

- 判重：`CSP`/`内容安全策略` 在本体仅 §七未采纳句「CSP 全量策略」，无专节；与 §JWT/§SSRF/§CSRF 分工不复用。豆包自留地 WB 0 落地。

- 抓取失败：四官方源全抓取成功；JSONP/AngularJS 绕过面无一手未写。
