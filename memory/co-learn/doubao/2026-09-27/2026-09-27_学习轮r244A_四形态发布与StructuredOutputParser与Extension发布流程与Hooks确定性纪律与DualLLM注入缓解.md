# r244-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（发布/API 面） | ✓ | Publish 四形态（web app/API endpoint/embeds/MCP-compatible tools，同一逻辑作为 App、API 或 Tool 交付）；API 密钥两级（应用密钥仅作用该应用；知识库密钥权限更大可访问创建账户下所有可见知识库需格外保管）；发布监控（logs/feedback/annotations/latency/usage 理解并改进）；Embed 三样式（全屏/弹窗/固定 widget）；Publish as a Tool（把 workflow 打包成工具给其他 Agent 用）；Cloud 额度（用尽可切自有 API key 无限率） |
| 2 | n8n（Agent 节点/模型面） | ✓ | Structured Output Parser（AI Agent 节点 Require Specific Output Format→接 Output Parser Auto-fixing/Item List/Structured Output；Define using JSON Schema 提供 field types/enums/descriptions；parser 自动注入 JSON 格式指令简化 prompt；agent 响应后校验严格规则 category 永远精确 billing 绝不 Billing）；动态模型路由（Agent Decisioner 按 query 内容/目的路由：coding→Opus 4/reasoning→Gemini Thinking Pro/general→GPT 4.1 mini/search→Perplexity 性能成本最优）；OpenAI-compatible endpoint 切模型（同一 HTTP Request 只改 model 值） |
| 3 | LangFlow（组件/市场面） | ✓ | Extension 发布全流程（build→validate→run→ship：python -m build 建 wheel+sdist→twine upload 发 PyPI→pip install lfx-my-extension→langflow run；discovery 发生在 server startup）；Bundles 贡献（src/lfx/src/lfx/components/<bundle_name>）；HITL 1.11（gated tool calls and reviews）；新 bundle（lfx-arxiv/lfx-docling/lfx-duckduckgo/lfx-ibm；NextPlaid/Paddle/Oracle/Valkey/EmpirioLabs）；Custom Python components（继承 Component 类） |
| 4 | Activepieces（AI 动作面） | ✓ | AI piece 动作（Summarize Text 5 fields；summarize long emails/articles/documents into what matters）；AI steps（summarize activity/extract key details/classify next action；route by skills/language/workload）；678+ prebuilt integrations；npm packages 扩展（解析复杂数据集/格式化 LLM 输出）；manual pause points（人审 AI 生成内容） |
| 5 | Make（AI Toolkit 面） | ✓ | AI Toolkit 模块全家桶（analyze sentiment/categorize text/identify language/extract information/standardize text/summarize text/translate text/chunk text）；Provider 选择（所有 plan 用 Make 内置 provider；付费 plan 可自定义 OpenAI/Anthropic；不存用户数据）；AI Content Extractor（built-in 从 PDF/Word/图片/音频提取结构化文本+元数据无需第三方；多页简历逐页提取+Text Aggregator 合并）；input files（一次性文件 jpg/png/gif/pdf；大文本/常引用文件上传为 knowledge files） |
| 6 | Pipedream（Node.js 运行时面） | ✓ | console.log/error 日志（step 下方黑/红）；异步警告（step 结束时代码仍运行→忘了 await Promise 或回调未 promisify）；AI code generation（自然语言生成 code step 代码，自动刷新 connected accounts/props）；npm 包直接 import（sentiment 例）；降级 pinning（包大版本改 import signature 时 pin 到最后已知可用版本）；早返回守卫（空数组返回占位消息而非空 payload 防 Slack 拒 API 调用）；credentials 存环境变量不 hardcode |
| 7 | Claude Code（agentic coding 面） | ✓ | CLAUDE.md/skills 是 requests 不是 guarantees——必须发生的事放 hook（PreToolUse/PostToolUse/SessionStart 生命周期；可跑 shell 命令/HTTP 请求/prompt/subagent）；hooks 低 context cost（shell/HTTP 不占 token）；hooks 五类型 command/HTTP/mcp_tool/prompt/agent（前三个确定性执行后两个用判断）；on-demand hooks（skill 被调用时激活会话期有效；/careful 阻塞 rm -rf/DROP TABLE/force-push）；skill Gotchas 节（最高信号内容从常见失败点构建随使用持续更新）；任务分解（复杂任务拆顺序 focused commands 每命令单一目标；提供示例与约束 Follow this existing API pattern）；PostCompact hook（压缩后重设关键指令）；/hooks 探索命令 |
| 8 | 安全（prompt injection 缓解面） | ✓ | Dual-LLM 模式（读不可信内容模型与有工具访问模型分离，reader 只传结构化摘要给 acting model 绝不传 raw text，攻击者只能影响结构化 label 不能注入命令）；Safe URL（OpenAI：检测助手试图把对话中获取信息传输给第三方→展示并请求确认或直接阻断指示尝试其他方式）；context separation（停止把不可信内容插进 system prompt，安全改进/实现成本比最高）；allow-listing（验证输入对已知好值而非过滤已知坏模式：检查路径在允许目录内而非查 traversal 序列）；假设 agent 会被攻破（least privilege/sandbox/monitoring/rate limiting/incident response）；LLM 工具参数当 untrusted（同 web API user input） |
| 9 | docs.openclaw.ai（任务/自动化面） | ✓ | Cron jobs 隔离会话（与 heartbeat 轮询不同，每个 cron 有自己的 context/model/thinking level，isolated session）；Task Flow（background tasks 之上 flow orchestration substrate：durable multi-step flows、managed/mirrored sync modes、revision tracking、openclaw tasks flow list\|show\|cancel）；交付通道（output 可到 chat channel/webhook/nowhere）；标准 5-field cron+时区（--tz）；automations CLI（openclaw automations，cron 为别名） |
| 10 | GitHub（生态面） | ✓ | Copilot Agent Teams（multi-agent coding 到达）+OpenHands 1.0（MIT 70k+★ model-agnostic）；Project HydraFusion（multi-model orchestration 前沿质量）；Agent Fleet Manager（171★ 1000+ 并发 coding agents）；plano（AI-native proxy and data plane for agentic applications：orchestration/safety/observability/smart LLM routing）；AgentSys（modular runtime 从 task discovery 到 deployment）；Omnigent Databricks（Apache-2.0 meta-harness 组合/govern/sandbox/share AI agent sessions 跨多 coding tools+custom agents）；LangChain 146.75k★ 171.7M 月下载；ponytail 146,145★（Makes your AI agent think like the laziest senior dev） |

## 判重基准
双键检索（相对 r241-r243 已落章节）：Dify（r243-A 落 queue engine/r243-B 落可观测/r243-C 落提示面——"四形态发布+密钥两级"独有增量新面）；n8n（r243-A 落 embedding/r243-B 落 RBAC/r243-C 落输出规范化——"Structured Output Parser+动态模型路由"独有增量深化）；LangFlow（r243-A 落安全/r243-B 落组件/r243-C 落 RAG——"Extension 发布全流程+startup discovery+HITL"独有增量深化）；Activepieces（r243-B 落 worker/r243-C 落 flow 逻辑——"AI piece 动作抽象"增量并入后续）；Make（r243-B 落触发/r243-C 落 IML——"AI Toolkit 全家桶"独有增量新面）；Pipedream（r243-B 落组件开发/r243-C 落调度——"AI code generation+await 警告"独有增量深化）；Claude Code（r242-B 落 hooks 五类型/r243-A 落 skill 创作——"requests not guarantees+on-demand hooks+Gotchas 节"独有增量深化）；安全（r242-C 落 MCP RCE/r243-B 落 MCP 安全/r243-C 落输出规范化——"Dual-LLM 读行动分离+Safe URL 外传阻断"独有增量深化）；openclaw（r243-B 落 Gateway/r243-C 落会话记忆——"cron 隔离会话+Task Flow"独有增量新面）；GitHub（r243 落 MemOS/agentmemory——"多模型编排+meta-harness"独有增量新面）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 四形态发布+密钥两级 | web/API/embed/MCP tool 同一逻辑；应用密钥 vs 知识库密钥 | 工作流 | wb-execute-discipline |
| ② n8n Structured Output Parser+动态模型路由 | schema 一次定义 parser 自动注入格式指令响应后校验；按 query 类型路由模型 | 工作流 | wb-execute-discipline |
| ③ LangFlow Extension 发布全流程+HITL | wheel+sdist→PyPI→pip install→startup discovery；gated tool calls | 工具 | wb-execute-discipline |
| ④ Hooks requests-not-guarantees+Gotchas | 必须发生的事进 hook 零 token；on-demand hooks；Gotchas 节 | 可复用 Skill | wb-execute-discipline |
| ⑤ Dual-LLM 读行动分离+Safe URL | reader 只传结构化摘要；外传阻断确认 | 模型/工作流 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：三件套无新可优化项。
- 垃圾：本轮未产生临时文件。
