# 2026-10-08 学习轮 r453A：Function Calling 与工具调用工程 2026

轮次：r453A（doubao 侧批 r453 第 1 轮）
判重：双键 grep KB 5056 行 + WB r444/r445 留痕全文 → 已落相关面：结构化输出（输出 schema 校验侧）、工具上下文（上下文注入侧）、多Agent协议——本主题=**Function Calling 与工具调用执行工程专项面**（工具 schema 设计纪律、并行 vs 顺序调用判据与冲突策略、工具错误处理与重试预算、工具循环终止与防卡死、工具调用评估与输出 schema 校验）——与前各面重叠<60%，独有增量≥40%，按增量判定落地；净增 5 独点。
实拉：3 query×10 站（ai-tldr-toolcalling/loooop-v21/loooop-v23/theneuralbase-function/theneuralbase-parallel/aiworkflowlab-compare/futureagi-functioncall/aiclaude-bestpractices/infini-functioncalling/googlecloud-functioncall/llmversus-functioncall + arxiv-2608.02645-verify-retry/theneuralbase-robustness/langchain-faulttolerance/langchain-toolretry/loooop-v17/theneuralbase-errorhandling/orderstack-reliability/openrouter-agentloop/bswen-malformed/genai-club-toolfail + anthropic-structuredoutputs/futureagi-functioncalling/mcp-spec-tools/claude-definetools/ai-tldr-schema/theneuralbase-grok-schema/explainx-schema/theneuralbase-jsonschema/ai-tldr-flat/claude-define-en，2026-10-08 实拉），逐站带来源标识。

## 落地 5 独点（每点标注提升层）

### 1. 工具 schema 设计纪律：required 取舍与扁平化（工具/工作流/可复用 Skill）
来源：ai-tldr / aiclaude / explainx / claude-docs
- **非必要参数放 required 是调用错误头号原因；over-marking 逼模型编造值或多余澄清→required 只放真正必需**。
- **schema 尽量扁平（一层嵌套足够），少用可选参数（每参数都是模型要推理的 token）；顶层加 strict:true 精确校验；工具名/参数服务端校验、never assume tool name safe**。
- 提升层：工具（schema）/ 工作流（设计纪律）/ 可复用 Skill（schema 模板）。

### 2. 并行 vs 顺序调用判据与冲突策略（工作流/可复用 Skill）
来源：ai-tldr / theneuralbase / aiworkflowlab / llmversus
- **独立+I/O-bound+顺序无关→并行（省 50-70% 延迟）；输出依赖/共享状态/需确定性→顺序**。
- **两并行结果矛盾（如价格源不一致）→先定义 resolution strategy 再让模型综合；disable_parallel 可降低 "No tool output found" 类错误**。
- 提升层：工作流（并行决策）/ 可复用 Skill（判据模板）。

### 3. 工具错误处理：错误当数据 + verify-before-retry + 重试预算（工具/工作流/可复用 Skill）
来源：theneuralbase / genai.club / arxiv-2608.02645 / langchain
- **错误作为工具输出返回（不是异常崩溃），LLM 把错误当数据推理；verify-before-retry=重试前先查后置条件是否已满足（非原子失败）**。
- **重试预算=单调用 3 次/单 agent 任务 10 次，耗尽升级不空转；错误类型分类进工具注册表元数据而非重试逻辑**。
- 提升层：工具（重试）/ 工作流（错误处理）/ 可复用 Skill（预算模板）。

### 4. 工具循环终止与防卡死（工具/工作流/可复用 Skill）
来源：openrouter / llmversus / genai.club
- **max-tool-calls 上限（10/session）；fingerprint 计数=同工具+参数串重复 3 次即停（允 1 次空结果重试仍快速停卡住模型）**。
- **重试预算耗尽升级人工/拒答；工具输出必回给模型（skip 会导致模型幻觉）**。
- 提升层：工具（终止机制）/ 工作流（防卡死）/ 可复用 Skill（循环模板）。

### 5. 工具调用评估与输出 schema 校验（工具/可复用 Skill）
来源：futureagi / mcp-spec / bswen
- **function-call eval=对比实际 vs 期望工具名+参数（跨模型快照回归）；MCP 工具输出 schema=服务端必须符合+客户端应校验**。
- **工具响应先过 model_validate 再入环（HTML 502 页当合法 JSON=模型见到假数据）**。
- 提升层：工具（校验/评估）/ 可复用 Skill（eval 模板）。

