# 2026-10-08 学习轮 r434A：AI Agent 安全与 Guardrails 2026

轮次：r434A（doubao 侧批 r434 第 1 轮）
判重：双键 grep KB 4694 行 → §Agent 工具面安全（工具描述注入/同名拦截/per-tool 最小权限/guardian pattern）、§Agent 安全纵深（dual-LLM 隔离/输入预处理）；本主题=guardrail 架构（结构性 guardrail 在上下文窗口外运行/输入侧语义过滤与 harmlessness 预筛/PromptArmor 检测器模式/输出侧白名单与结构化交接/可信上下文最小化）——与既有工具面条目互补不重叠，增量≥40%，净增；净增 5 独点。
实拉：3 query×10 站（futureagi-rapidclaw-maxim-agent-works/arxiv-2511.18933-2505.09602-microsoft-learn-aip-gov-claude-platform-arxiv-2410.15236-acm-HSF/spinnable-taskade-billdx-openlegion-arnav-dailyaiworld-aideck-nitinksingh-agentswarms-alicelabs），逐站带来源标识。

## 落地 5 独点（每点标注提升层）

### 1. 分层防御框架：输入→工具→输出→审批→评测五层，单层都不够（工作流/可复用 Skill）
来源：rapidclaw-prompt-injection-defense-production-agents-2026 / taskade-ai-guardrails / spinnable-ai-agent-guardrails-design-guide
- **七层协同**：输入处理（可信/不可信文本分离）→ 输出过滤（先验结构再行动）→ 能力沙箱（agent 在 jail 里跑）→ 特权分离（least-authority 工具）→ canary tokens（外泄绊线）→ 策略引擎（高影响动作前确定性检查）→ 持续红队。
- **五层落地版**：①输入守卫（注入/PII/jailbreak 过滤）②工具/动作闸（最小权限/白名单/scoped creds）③输出守卫（grounding/schema/内容安全）④人工审批（高风险动作等人）⑤evals 反馈（离线测量调 1-4 层）。
- 判据：**单层都不够**——至少 3 层协同；评测反馈层调前 4 层，形成闭环。

### 2. 结构性 guardrail：运行在 LLM 上下文窗口外，注入内容无法影响它（工具/可复用 Skill）
来源：openlegion-ai-agent-guardrails / openlegion-fr-ai-agent-guardrails
- **结构性 guardrail=代码在窗口外强制**（LLM 调用前/响应后/推理步与工具派发之间）——**因为执行机制在模型上下文之外，LLM 收到的任何内容都影响不了它**；正则过滤器在 Python 剥离注入模式后再 append 上下文，不问 LLM 查注入。
- **工具响应 JSON 包装 + 长度截断**：`{"tool":"web_search","result":"[sanitized content]","status":"success"}` 比原始字符串难武器化；**工具响应截断=每条 append 前 2,000 token 上限**，防对抗内容靠体量淹没稳定 system prompt。
- 判据：防注入优先选"代码层剥离"，不把过滤交给"让模型自查"。

### 3. PromptArmor 模式：用 off-the-shelf LLM 当注入检测器，FP/FN <1%（模型/工作流）
来源：zylos-defensive-prompt-engineering-multi-tool-ai-agents / brightlume-prompt-injection-production-attack-patterns
- **检测器模式**：单独一个小型快速模型分类输入是否含注入意图，再进主 agent——**语义过滤适配攻击演化、不依赖脆弱的模式匹配**（关键词过滤会被同义词/改写绕过）。
- **PromptArmor（ICLR 2026）实测**：GPT-4o/4.1/o4-mini 当检测器，AgentDojo 上**假阳与假阴均 <1%**；检测器移除注入后，下游攻击成功率显著下降。
- 判据：注入检测=专用独立小模型+语义分类，别指望主模型自查或关键词正则兜底。

### 4. Harmlessness screens 预筛 + 结构化输出约束（模型/工具）
来源：claude-platform-mitigate-jailbreaks / microsoft-learn-prompt-injection / arnav-securing-agentic-ai
- **轻量模型预筛**：Claude Haiku 4.5 之类小模型在用户输入进主对话前 pre-screen，用**结构化输出把响应约束成简单分类**（content moderation 示例）——主对话只收到"通过/拒绝"。
- **输入硬化**：把所有外部内容当不可信（含组织自有数据源——上游可能已被操纵）；web 页面/邮件/附件/API 响应/数据库结果全过内容过滤；**strip/escape HTML-markdown 元素中和 script 标签/隐形文本**；**用 allowlisting 只放行预期数据格式**。
- 判据：预筛模型+结构化分类输出=低延迟低成本的第一道闸；外部内容一律不可信先清洗。

### 5. 可信上下文最小化 + 输出侧白名单 + 结构化交接（工作流/可复用 Skill）
来源：agent-works-prompt-injection-defense / agent-works-layered-controls / futureagi-prompt-injection-2025
- **子代理隔离**：处理不可信内容的子代理运行**降权工具**；可信父代理处理子代理结果后再决策——**越小的可信上下文，越小的攻击面**；Email/文档内容标成明确 "untrusted" 区段进模型。
- **输出侧白名单**：高风险动作输出侧 allowlist；**阶段间用结构化 schema 校验交接**（不把原始文本当指令传）；**canary tokens=外泄绊线**（数据流出时触发器）。
- **屏幕输出过滤**：模型输出到用户/下游工具前先 screen——封堵泄露 system prompt/base64 payload/指向攻击者域名的链接/类外泄工具调用参数。
- 判据：不可信内容给降权子代理、结果过父代理；交接走 schema 校验；输出白名单管高风险动作。

