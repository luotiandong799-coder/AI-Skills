# r812A · CORS 错误配置（跨源资源共享）：把响应头权限建在不可信 Origin 之上

> SI · 2026-11-27 独立实拉，≥2 独立域一手交叉（PortSwigger Web Security Academy 全文 + MDN HTTP CORS 全文逐字），3 独点。
> 定位：§二十 JWT 管令牌可信、§十五 SSRF 管服务器被当代理、§二十二 CSRF 管状态变更防线；本章管**浏览器侧「谁能读跨域响应」这一道许可**——CORS 配错等于服务端替攻击者发了一张读取凭据会话数据的授权书。

## 独点1 根因：ACAO 建在客户端可控的 Origin 上，且 CORS 不是 CSRF 防护
- PortSwigger 逐字定义：CORS 是「a browser mechanism which enables controlled access to resources located outside of a given domain. It extends and adds flexibility to the same-origin policy (SOP). However, it also provides potential for cross-domain attacks, if a website's CORS policy is poorly configured」；「**CORS is not a protection against cross-origin attacks such as cross-site request forgery (CSRF)**」。
- SOP 的边界是「generally allows a domain to issue requests to other domains, but not to access the responses」——请求能发出但读不到响应；CORS 用一组 HTTP 头定义「trusted web origins and associated properties such as whether authenticated access is permitted」，把这道读限制打开。
- 成立条件两条同时：① 服务端把请求里的 `Origin` 反射进 `Access-Control-Allow-Origin`（ACAO）；② `Access-Control-Allow-Credentials: true`（ACA-C）使跨源请求带 cookie 并在会话内处理。原文示例请求 `Origin: https://malicious-website.com` → 响应 `ACAO: https://malicious-website.com` + `ACA-C: true`，则任意站点可读受害者敏感数据（API key / CSRF token）。
- 判据：反射任意 Origin 本身就是缺陷，不因「看起来只配了个 header」而成立；ACA-C 缺位时攻击者只能读到无需登录即可直接访问的内容（唯一例外见独点2「内网穿透」）。

## 独点2 五类配置错误形态（按谁被错误信任分）
1. **服务端直接反射 Origin**：为省维护 allowlist 之苦把请求 Origin 写进 ACAO（PortSwigger: server-generated ACAO from client-specified Origin）。
2. **Origin 白名单解析错误**：用 URL 前缀/后缀匹配或正则做「信任所有子域/他组织域」——后缀匹配 `normal-website.com` 被注册 `hackersnormal-website.com` 绕过；前缀匹配 `normal-website.com` 被 `normal-website.com.evil-user.net` 绕过。与 §si §18 Zip Slip 的 sibling-prefix 绕过同族：**子串匹配不是域匹配**。
3. **白名单 `null`**：`Origin: null` 来自跨源重定向、序列化数据、`file:` 协议、沙箱跨源请求；为本地开发放行 null 后，攻击者用 `<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,...withCredentials=true...">` 造出 null Origin 请求即满足白名单。
4. **信任关系的 XSS 放大**：「correctly configured CORS establishes a trust relationship between two origins」——若被信任的 `subdomain.vulnerable-website.com` 有 XSS，攻击者借其注入脚本用 CORS 读信任它的主站 API key；CORS 配得对但信任的是一个可被攻破的源，防御整体失效。
5. **TLS 降级与内网无凭据穿透**：主站严格 HTTPS 却白名单了跑 HTTP 的可信子域，MITM 注入重定向让受害者浏览器带 `Origin: http://trusted-subdomain...` 发 CORS 请求，读到敏感数据——「effective even if the vulnerable website is otherwise robust in its usage of HTTPS, with no HTTP endpoint and all cookies flagged as secure」。另：内网站常配 `ACAO: *`（无凭据），外部站点可借受害浏览器当代理读内网资源——「when it's part of an organization's intranet, and located within private IP address space」，此时**网络位置本身不是访问控制**。
- 真实后果链（CVE-2025-34291 Langflow ≤1.6.9，cvelogic/NVD 披露）：`allow_origins='*'` + `allow_credentials=True` + refresh token cookie `SameSite=None` 三件叠加，恶意页跨源带凭据调 refresh 端点拿 token → 调内置代码执行端点 → RCE。CVE-2025-50579（Nginx Proxy Manager v2.12.3）Origin 校验缺陷使跨域脚本截获 JWT。

## 独点3 修复与验收：精确源 + 凭据互斥 + 缓存分域 + 服务端仍鉴权
- MDN 逐字硬规则：带凭据请求「the server **must not** specify the `*` wildcard for the `Access-Control-Allow-Origin` response-header value, but must instead specify an explicit origin」；「If a request includes a credential ... and the response includes an `Access-Control-Allow-Origin: *` ... the browser will block access to the response」。另「any `Set-Cookie` response header ... would not set a cookie if the `Access-Control-Allow-Origin` value ... is the `*` wildcard」。
- 动态白名单（按请求 Origin 返回单一源）必须带 `Vary: Origin`：MDN「the server should also include `Origin` in the `Vary` response header to indicate ... responses will differ based on the value of the `Origin` request header」——否则共享缓存把给 A 源的响应发给 B 源，等于绕过白名单。
- 预检（preflight）：非 GET/HEAD/POST 或非 safelisted 头/Content-Type 的跨源请求先发 OPTIONS 探测；「CORS-preflight requests must never include credentials. The *response* to a preflight request must specify `Access-Control-Allow-Credentials: true` to indicate that the actual request can be made with credentials」。凭据默认不发，须 `fetch({credentials:'include'})` 或 `xhr.withCredentials=true`，且响应缺 ACA-C:true 即被浏览器丢弃。
- PortSwigger 防御五条：敏感资源在 ACAO 精确指定源；只放行可信站点（禁未校验动态反射）；避免 `ACAO: null`；内网避免通配符（「trusting network configuration alone to protect internal resources is not sufficient」）；**CORS 不替代服务端鉴权**——「an attacker can directly forge a request from any trusted origin」，故认证/会话管理必须在服务端继续做。
- 验收四步回归：① 把 Origin 改成恶意域/`null`/前后缀变体，断言 ACAO 不反射、ACA-C 不出现；② 带凭据请求断言 ACAO 是精确源而非 `*`；③ 动态白名单断言响应有 `Vary: Origin`；④ 从被信任但存在 XSS 的子域视角复测能否读到主站敏感数据（信任关系横向验证）。
- 声明不防什么：CORS 不防 CSRF（状态变更）、不防 XSS（信任链内部）、不防服务端鉴权缺失、不防直接伪造请求、不防内网非浏览器客户端。四者各走 §二十二 CSRF / §七 XSS 信任 / 服务端鉴权 / 网络层。

## 来源与诚信
- PortSwigger Web Security Academy《Cross-origin resource sharing (CORS)》`https://portswigger.net/web-security/cors`（WebFetch 200 全文逐字：定义/反射 Origin/解析错误/null/XSS 信任/TLS 降级/内网穿透/防御五条）——第一独立域，权威机构一手。
- MDN Web Docs《CORS》`https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS`（WebFetch 200 全文逐字：ACAO 通配符与凭据互斥/Set-Cookie/preflight 条件/simple request 定义/Vary: Origin/ACA-C 语义）——第二独立域，标准实现文档一手。
- CVE-2025-34291（Langflow）与 CVE-2025-50579（Nginx Proxy Manager）经 cvelogic/NVD 聚合页 WebSearch 逐字，作真实后果佐证，非机制来源。
- 判重：全库 SKILL.md + module-memory + co-learn 标题级 `CORS`/`跨源` 0 专节（SI 正文仅在 SSRF/CSRF/零信任/RAG 向量库宽 CORS 处 4 处子串提及，异命题）；豆包自留地 `wb-execute-discipline`/`wb-context-compressor` WB 0 落地。按 rules/07 去重铁律四态判「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。
