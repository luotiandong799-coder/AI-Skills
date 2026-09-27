# r243 批末 WorkBuddy 推送（2026-09-27）

## 推 WB 3 条（从 r243 三批 15 独点中选最有吸收价值的）

### 1. LLM 输出当 untrusted input 规范化（来源：n8n 数据转换面，2026-09-27 实拉）
AI 生成的 JSON/结构输出不能直接进下游——agent/LLM 节点后接 tiny Code node 三件事：去 fence+前言（从第一个 `{` 或 `[` 到最后匹配 `}` 或 `]` 取子串再解析）；Webhook payload 在单点归一化到固定 schema（不在 raw 上分支，防御性读 key，schema shift 只碰一个 node）。判据：格式漂移是杀半夜执行的常见元凶，规范化节点是廉价保险。

### 2. Prompt caching 成本模型（来源：Anthropic 上下文工程面，2026-09-27 实拉）
cache reads 0.10× 正常输入价格、writes 1.25×（5m TTL）或 +100%（1h TTL）；cache_control breakpoint 放最后一个跨请求一致的块，绝不放 per-request 变化内容；对话超 20 块用多 breakpoint；低频率批处理（document review/overnight batch/scheduled jobs）用 1h TTL；缓存只存 KV cache+cryptographic hashes 不存 raw text（适合 ZDR 数据保留承诺）。判据：缓存命中率决定真实成本，重复上下文必须缓存，位置纪律决定命中率。

### 3. Agent RBAC 三权分离 + 凭证不暴露（来源：n8n 认证/权限面，2026-09-27 实拉）
agent 权限按三槽分别授：谁能编辑 workflow/谁能执行/每次执行可达哪些凭证——三权独立，Editor 不自动有 execute 权，execute 权不授予凭证访问；Credentials 加密存储不经手明文；OAuth2 Token Exchange（RFC 8693）delegated access 带全审计归因，IdP 为全局角色真相源。判据：agent 比人快、撤销前已造成影响，RBAC 对 agent 比对人类更重要。
