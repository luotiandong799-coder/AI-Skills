# r178-B Prompt Caching 失败模式：动态内容在尾部、break-even 阈值、cache key 稳定性

实拉时间：2026-09-24 20:40
信源：aiworkflowlab production caching 2026-04 / DigitalOcean hit rate 7%→74% 2026-07 / tokenoptimize design hits 2026-06 / Microsoft Azure prompt caching 2026-08 / genta dev guide 2026-04 / aipromptshub savings 2026-06 / Microsoft classic / openlegion caching 2026-07 / DEV agentic playbook 2026-09 / developersdigest Claude guide 2026-04（caching 组，满 10 站）

## 实拉证据（关键原文）
- aiworkflowlab：「Put variable content at the END. Injecting user query or timestamp at top destroys cache for every request.」
- aipromptshub：timestamp/UUID 在 system prompt 顶部是最常见反模式——hit rate 直接归零。
- developersdigest：break-even = prefix 在 5 分钟内被复用 1-2 次以上就值得 cache；>2k tokens 每次都发的 system prompt 必 cache。
- DigitalOcean：从 7% 到 74% hit rate 的四步法——稳定前缀映射、动态内容移尾、固定 few-shot 顺序、一致 cache key。

## 独点清单（3 个真独点）

### 独点1：稳定前缀在前、动态内容在尾——最反直觉的高杠杆优化（工具层）
- 判据：OpenAI/Claude 都缓存前缀。system prompt 顶部插时间戳/session ID/user_id = 每次请求 cache key 都不同，hit rate 归零。正确顺序：稳定 system/工具 schema/few-shot 在前，user query/timestamp/会话历史在后。和直觉相反（很多人把用户身份写开头）。
- 独有增量（与 r162B prompt cache 区别）：那条讲 cache 省钱原理；本条讲**具体怎么排 prompt 才能命中**——失败模式清单。
- 提升层：工具。

### 独点2：break-even 阈值——5 分钟复用 1-2 次就值得 cache（工作流层）
- 判据：不是所有 prompt 都值得 cache。prefix 在 5 分钟内被复用 >1-2 次才 cache（cache 写入有额外费用）。>2k tokens 每次都发的 system prompt/工具定义必 cache。多轮对话 cache 到最后一个 assistant turn（更早的轮次稳定）。
- 独有增量：给了具体阈值，不是"能 cache 就 cache"。
- 提升层：工作流。

### 独点3：few-shot 顺序固定 + 动态工具列表是隐形 cache 杀手（工具层）
- 判据：为了"多样性"每请求打乱 few-shot 顺序 = 每个顺序都是独立前缀，cache 全失。工具描述里带 live state（当前库存/用户权限）也会 invalidate。工具列表要静态化，运行时数据放尾部。高并发用 prompt_cache_key 做流量分区。
- 独有增量：点出 few-shot 打乱和动态工具列表这两个隐形杀手。
- 提升层：工具。

## 判非重复理由
- r162B 讲 prompt caching 省钱原理；本条讲 hit rate 优化与失败模式，增量 >40%。
