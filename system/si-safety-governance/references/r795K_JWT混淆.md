# r795K｜SI｜JWT 验签通过≠可信：alg 白名单、kid 注入与 claims 校验时序

访问日期：2026-11-22。每轮独立实拉，禁止复用上轮结论。

## 一手来源逐字

- https://www.rfc-editor.org/rfc/rfc8725.txt（IETF RFC 8725，2020-06，WebFetch 200 逐字：alg=none / RS256→HS256 公钥当 HMAC 密钥 / 一密钥一算法 MUST）

- https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/JSON_Web_Token_Cheat_Sheet.md（OWASP 官方 Markdown 源，访问 2026-11-22，WebFetch 200 逐字：拒绝 alg=none / 公钥误作 MAC 密钥 / kid 注入 / 密钥须有信任链）

- https://www.rfc-editor.org/rfc/rfc7519.txt（IETF RFC 7519 §4.1，2015-05，WebFetch 逐字：iss / aud MUST identify / exp MUST NOT be accepted）

## 独有点

1. alg 判据：verify 调用须显式算法白名单（如 `algorithms:['RS256']`），从 token header 读 `alg` 再分支判高危。RFC 8725 逐字：`alg` 可改成 `none` 让某些库「validate」而无签名；`RS256` 可改成 `HS256`，库便拿 RSA 公钥当 HMAC 共享密钥验签。硬约束：「each key MUST be used with exactly one algorithm」。

2. 顺序判据：`iss`/`aud`/`exp` 必须在验签通过**之后**读取；先 decode 未验签 payload 并据此授权即违规。RFC 7519 逐字：`aud` 要求处理方「MUST identify itself with a value in the audience claim」，`exp` 之后「MUST NOT be accepted」。OWASP：验签通过只证明签名者持有密钥，解密成功本身「proves nothing about who issued the claims」。

3. kid 判据：`kid` 不得拼进文件路径/SQL，只允许白名单枚举或预载 JWKS 精确查找；出现 `../`、`http://`、引号即拒绝。OWASP 逐字：`kid`「reaches databases and directories as an injection vector」，且验证密钥不得直接取自 token，除非能经信任链绑到 issuer 的根信任锚。

## 判重与判非

- 判重：`算法混淆`/`algorithm confusion`/`kid 注入`/JWT 专节本体全库 0；与 §十四 OIDC、§十凭据泄露、§十五 SSRF 分工不复用。豆包自留地 WB 0 落地。

- 抓取失败：OWASP Java cheat sheet 两 URL 404；HTML 页 AI 摘要超时，改用官方 Markdown 源取逐字。
