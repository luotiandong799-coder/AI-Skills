# r808C · 质量分配 / 自动绑定（Mass Assignment · CWE-915）全文与判非

> SI · 2026-11-26 实拉；≥2 独立域官方一手（OWASP Cheat Sheet + MITRE CWE），OWASP Laravel/DRF Cheat Sheet 交叉。
> 主线：框架「帮你把请求参数写进对象」的便利，正是越权写入字段的通道；白名单管可写面，授权管对象与操作，两道门不可互替。

## 独点1 · 根因、成立条件与命名分裂

- OWASP 逐字：「Software frameworks sometimes allow developers to automatically bind HTTP request parameters into program code variables or objects to make using that framework easier on developers.」；「Attackers can sometimes use this methodology to create new parameters that the developer never intended which in turn creates or overwrites new variable or objects in program code that was not intended. This is called a **Mass Assignment** vulnerability.」
- 别名按语言/框架分裂：Mass Assignment（Ruby on Rails / NodeJS）、Autobinding（Spring MVC / ASP.NET MVC）、Object injection（PHP）。同一机制不同名字，检索判重要三组都查。
- 成立条件（Exploitability 逐字）：「attacker-controlled input can initialize or update fields that the caller is not authorized to change, such as a role or account owner. Field names may be guessed or discovered; source-code access is not required.」
- CWE-915 逐字定义：「The product receives input from an upstream component that specifies multiple attributes, properties, or fields that are to be initialized or updated in an object, but it does not properly control which attributes can be modified.」——弱点定性为**可写属性控制不足**，不是输入格式错误。
- 两个常见误判：① 「空构造器才中招」错——OWASP 逐字「An empty constructor is not a general prerequisite. For example, Spring supports both constructor and setter binding」；② 只看顶层字段错——「Review which inputs the binding mechanism exposes, including nested objects」。
- 实证：2012 GitHub 事件，「A user was able to upload his public key to any organization and thus make any subsequent changes in their repositories」（OWASP GitHub case study）。后果面 CWE：Modify Application Data（Integrity）、Execute Unauthorized Code or Commands、Alter Execution Logic。

## 独点2 · 白名单管可写面，但不替代授权

- OWASP 方案顺序：① 专用输入对象 DTO（只含调用方可编辑字段）；② 对还有额外属性的对象做显式字段 allow-list；③ 「Do not rely on a block-list as the sole protection: a new or overlooked sensitive field remains bindable. CWE-915 recommends allowlists over denylists.」
- CWE 缓解逐字：「If possible, prefer allowlists over denylists.」；「For any externally-influenced input, check the input against an allowlist of internal object attributes or fields that are allowed to be modified.」；另有重构只暴露目标属性 getter/setter、以及签名/封印（HMAC）保证反序列化数据未被篡改。
- 明确的边界句（最容易漏）：「DTOs and field allowlists restrict writable properties; they do not replace authorization for the requested object and operation.」⇒ 与 §21 BOLA/IDOR 分工：BOLA 判「这个登录用户能否对这个对象做这个动作」，本节判「这次绑定能写哪些字段」；前者过了不等于后者过了，反之亦然。
- 框架反模式（OWASP Laravel / Django REST Framework Cheat Sheet 交叉）：Laravel 禁 `$request->all()` 直灌、禁 `unguard()` / `$guarded=[]`、避 `forceFill`/`forceCreate`（除非传已校验数组）；DRF 显式 `ModelSerializer.Meta.fields`、避 `Meta.exclude` 与 `fields="__all__"`、只读字段用 `read_only_fields`/`read_only=True`；Spring `setDisallowedFields` 被官方称 fragile（字段会漏加或后加），用 `setAllowedFields`。
- 判据：新增模型字段即触发一次可写面回归——否则「昨天还安全的 DTO」今天新增 `isAdmin` 后重新可写，正是 denylist 失效路径。

## 独点3 · 检出与验收

- CWE Detection Methods：SAST 通过 source→sink 数据流建模可发现部分实例，Effectiveness: High；但动态字段名、嵌套对象、反射绑定会漏，不能把「SAST 未报」当已治理。
- 回归断言固定为：① 正常字段写入成功；② 额外塞入敏感字段（如 `isAdmin=true`、`ownerId=<他人>`）后，该字段在落库结果与响应中保持原值/被拒；③ 新增模型字段后重跑 ①②；④ 直接对**他人的对象**执行同一写入，验证对象级授权仍拒绝（与 §21 联动）。
- 不防什么：不防已授权字段的业务越用、不防 BOLA 对象越权、不防 SQL 注入（列名由用户输入决定时走注入面）、不防反序列化 gadget 链；签名/HMAC 只保证数据未被篡改，不产生字段级授权。

## 来源与诚信

- `https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html`（OWASP Cheat Sheet Series 官方，WebFetch 200 全文逐字：定义/别名/例子/exploitability/GitHub 案例/解决方案/DTO/各框架 allow-vs-block 示例）——第一独立域·官方一手。
- `https://cwe.mitre.org/data/definitions/915.html`（MITRE CWE-915，WebFetch 200 全文逐字：定义/适用语言/后果/SAST Effectiveness High/allowlist 优先/签名封印/重构）——第二独立域·官方一手。
- OWASP `Laravel_Cheat_Sheet` 与 `Django_REST_Framework_Cheat_Sheet`（WebSearch 逐字交叉，与第一条同域，仅作框架细节补充，不冒充独立域）。
- 判非：全库 SKILL.md + module-memory + co-learn 对 `mass assignment`/`autobinding`/`CWE-915`/`质量分配`/`自动绑定` 0 专节；§21 BOLA 是对象/操作授权异命题，§16 SSRF/§22 CSRF/§24 原型污染均异命题。豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地。按 rules/07 判「增＝加厚现有」，0 新建。
