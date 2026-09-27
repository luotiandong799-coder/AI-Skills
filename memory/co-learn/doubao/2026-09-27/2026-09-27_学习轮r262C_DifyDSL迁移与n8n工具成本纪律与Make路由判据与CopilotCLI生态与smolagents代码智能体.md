# r262C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（DSL/迁移面） | ✓ | 所有 app 可导出 YAML DSL（Dify 自研 Domain-Specific Language），可直接导入创建 app——跨实例移植+分享；导出内容：app 配置+元数据/workflow 编排+节点设置/模型参数+prompt 模板/知识库连接（不含数据本身）；隐藏用法：workflow 导出 YAML→Git 版本控制/diff 部署差异/内置 tracing API 重放历史执行逐步；dify-dsl-builder：YAML Patch System 声明式修改 DSL（18 operations）npx dify-dsl-cli apply patch.yml 自动 validate 非零退出；Dify DSL Visualizer（VS Code）：原生 undo/redo/手改 YAML 或 agent 改立即更新 graph/一键 publish；JSON Schema 校验 schemas.dify.ai/workflow-2026.json+curl PATCH workflows API |
| 2 | n8n（Agent 工具/输出面） | ✓ | AI Agent node "Require Specific Output Format"+Structured Output Parser 选 "Define using JSON Schema" 提供 schema（field types/enums/descriptions）简化 prompt parser 自动注入；Tool parameters 三类型混用：FromAI（agent 决定）/expressions（动态传值）/fixed mode（静态值）——同工具多 agent 用不同 static values；Structured Output Parser 已知不可靠替代=自定义循环手动验证 agent 输出（gpt-4.1 实测）；工具附加 Agent node 每 turn 重计费：精简 tool description（per-turn tax）/不要 just-in-case 附加 5 个少用工具和 5 个常用一样贵/工具返回大 JSON blob 只取 2 字段先 trim 再回 context/短 agent loops 双赢；Anthropic-style Skills 在 n8n：Postgres skills 表 name 主键+description manifest+content 全文 progressive disclosure |
| 3 | LangFlow（自定义组件面） | ✓ | 组件=Component 子类 Python：类级属性（display_name/description/icon）+inputs 列表+outputs 列表（绑定方法）+方法逻辑+错误处理内部变量；输出端口必须绑定方法 Output(name, method="build_message")；Bundles 架构：extension init 脚手架 canonical layout（extension.json v0 manifest/pyproject.toml/src/lfx_my_extension/）；langflow-builder-mcp 0.2.5 用 LLM 生成组件代码；Langflow Assistant 新 import 路径 lfx.custom/lfx.io/lfx.schema |
| 4 | Activepieces（Pieces SDK 面） | ✓ | TypeScript SDK：createPiece({displayName, logoUrl, authors, auth, actions, triggers})；auth 参数在 createPiece/createTrigger/createAction 定义；token caching：无缓存每次 action 前 login 可触发 429；token 自动续期（过期前 15 分钟 clamp 半寿命）；AP_DEV_PIECES 本地开发从 local dist 加载；npm run build-piece 生成 tarball；Platform Admin→Catalogue→Pieces 管理 |
| 5 | Make（Router/Filter 面） | ✓ | Filter 运算符全集：Text（Equal/Contains/Starts with/Matches pattern regex）/Numeric（Greater/Less/Between）/Date（Before/After/Between dates）/Existence（Exists/Does not exist）/Array（Contains item/Does not contain item）+AND/OR 组合；Router vs Filter 判据：单条件过滤=Filter/条件分支不同处理=Router/同数据多路并行=Router 无 filter/spam 阻断=Filter；Router 配置优先级顺序+末尾 fallback——无 fallback 匹配不到的路由 bundle 静默消失无日志；LLM 集成：Router 把 AI 结构化输出转业务结果每 route=目的系统非 code branch |
| 6 | Pipedream（Connect/OAuth 面） | ✓ | Connect 托管认证：OAuth 客户端+安全 token 存储+自动 refresh；用户连接账号秒级开发者不碰凭证；端用户用 OAuth apps（Google Drive/Slack/Notion）必须用自己 custom OAuth clients 注册；凭证加密 at rest 按 project 隔离；Connect tokens 过期且只能使用一次；OAuth 或 User API keys 都 Bearer auth；MCP server 提供 10,000+ 工具 AI agent 接账号 |
| 7 | Claude API（tool streaming 面） | ✓ | stream:true SSE 增量；SDK stream() 方法；Fine-grained tool streaming GA（所有模型所有平台无 beta header）：eager_input_streaming=true 单工具启用；新事件 InputJsonEvent 两个属性流式获取工具调用参数片段；大 max_tokens 请求 SDK 需要 streaming 避免 HTTP 超时；不需要增量处理用 .stream()+.get final message |
| 8 | Copilot CLI（agent/skills 面） | ✓ | Copilot CLI GA（2026-02-25）：autopilot mode 自主执行工具/命令/迭代不需批准；built-in specialized agents：Explore（快速 codebase 分析）/Task（跑 builds/tests）/Code Review（高信号 change review）/Plan（实施规划）多 agent 并行；2026-06-02 agent picker：Agent mode（默认）/Ask mode（快速问答）/Custom agents（个性化）/Plan mode（规划协作）；Custom agents=.agent.md 文件定义（操作方式/工具/标准/输出）；Skills=task-specific instructions auto-trigger based on prompt；SKILL.md YAML frontmatter 同 ARIS 格式 Copilot CLI v0.130+ 原生支持无需 mirror；Rubber Duck：选 Claude 模型作 orchestrator 时 Rubber Duck=GPT-5.4 检查 agent 工作 surfacing 高价值 concerns（missed details/assumptions/edge cases）第二意见模式；Plan mode Shift+Tab 循环进出 ask_user 工具提问澄清先规划后写码 |
| 9 | OpenClaw（Plugins 面） | ✓ | ClawHub=社区插件主发现面：openclaw plugins search "calendar"；install clawhub:<package>@version；源类型五：marketplace（Claude-compatible marketplace 插件 openclaw plugins install --marketplace）/npm pack/npmjs.com（dist-tags/private registry）/git:github.com//@branch|tag|commit/本地 --link ./my-plugin；插件扩展 channels/tools/providers/hooks 等能力；marketplace entries --offline/--feed-profile/list/refresh --expected-sha256 校验；普通 bare package specs 从 npm 装除非匹配 bundled 或官方插件 id |
| 10 | Hugging Face（smolagents 面） | ✓ | smolagents=轻量 code-first agent 库（~1000 行逻辑）；CodeAgent=LLM 写 Python 代码作为 action（非 JSON tool call）单步可调两工具组合/迭代/helper function/条件——HF 基准 ~30% 更少 steps 更高硬任务分；ToolCallingAgent=JSON/text tool calls 行业标准格式；执行 LocalPythonExecutor（AST）或 Sandbox；model-agnostic（transformers/Ollama/HF Inference/OpenAI/Anthropic/Bedrock/Azure/LiteLLM）；三论文背书 Executable... |

## 判重基准
双键检索：Dify DSL（无前置章节，新面）；n8n Agent 工具成本纪律（r224C/r255A 有 n8n 子工作流但无工具计费纪律——per-turn tax/just-in-case 附加/大返回先 trim 为独有增量）；Make Router/Filter（r261A Make 性能优化有"Router 并行省 50%"——Filter vs Router 判据矩阵+末尾 fallback 必须+无 fallback 静默消失+运算符全集为独有增量合并）；Copilot CLI agent 生态（§6042 GitHub Copilot Agent Skills 规格已有——CLI GA 四模式+Rubber Duck 第二意见+SKILL.md 原生支持 v0.130 为独有增量独立成章与 6042 分工）；smolagents CodeAgent（无前置章节，新面）。备选并入记录：LangFlow 自定义组件骨架（r259C 有 LangFlow 部署、无组件开发）、Pipedream Connect 托管认证（r260C 有错误处理）、OpenClaw 插件源矩阵（r257B 有记忆）、Claude Fine-grained tool streaming（新面）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify DSL 迁移与版本控制 | YAML DSL 导出/导入/Git 版本控制/DSL Visualizer | 工具 | wb-execute-discipline |
| ② n8n Agent 工具成本纪律 | 每 turn 重计费/精简 description/大返回先 trim | 工作流 | wb-execute-discipline |
| ③ Make Router/Filter 判据矩阵 | Filter vs Router/末尾 fallback/静默消失 | 工作流 | wb-execute-discipline |
| ④ Copilot CLI agent 生态 | 四模式/Rubber Duck/SKILL.md 原生 | 工具 | wb-execute-discipline |
| ⑤ smolagents CodeAgent | code-first/30% 少 steps/单步组合 | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源；③④按增量判定与已落章节合并保留增量落地（③并入 Make 性能优化相邻新章、④独立成章与 §Copilot Agent Skills 分工）；①②⑤为新面。
- 备选未落四组并入记录。
- 垃圾：本轮未产生临时文件。
