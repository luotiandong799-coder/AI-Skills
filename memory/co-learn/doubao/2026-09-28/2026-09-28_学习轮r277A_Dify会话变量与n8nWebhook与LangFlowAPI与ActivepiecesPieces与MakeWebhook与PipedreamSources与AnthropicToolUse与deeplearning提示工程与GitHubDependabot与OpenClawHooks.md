# r277A 学习轮留痕（重建，2026-09-28）

> 说明：原 r277A 留痕与 SKILL.md 十独点因 .git 损坏+恢复操作被覆盖丢失（commit 对象随损坏 .git 丢失），本文件为按原主题重新实拉后的重建版，commit 为恢复后的新 hash。

## 信源实拉清单（10 站全量逐站重新实拉，查询词与全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（会话变量与记忆） | OK | Conversation Variables 跨 turn 持久（Chatflow 专用可变变量）；Variable Assigner 节点写/更新；Array[object] 持续追加记忆（default 值灵活）；Input/Output 变量不可变仅单次 run vs conversation 可变持久；上下文工程用途 |
| 2 | n8n（Webhook 响应模式） | OK | 四种响应：Immediately/When Last Node Finishes/Respond to Webhook/Streaming response；异步模式=先 202 立即响应+后台继续+回调 webhook 恢复执行；64 秒 Wait 限制下改异步；Streaming 需 trigger 配 Streaming response+agent 开 streaming |
| 3 | LangFlow（API 全局变量/会话记忆） | OK | X-LANGFLOW-GLOBAL-VAR-{NAME} header 传全局变量；header 优先于环境变量；仅本次请求不持久；FALLBACK_TO_ENV_VARS 兜底；默认 session ID=flow ID 全存一个大会话，自定义 session ID（如 user ID）隔离；Workflow API mode=background+session_id |
| 4 | Activepieces（Pieces 生态/平台治理） | OK | 两级管理：Platform 级安装移除全平台/Project 级 show-hide 特定项目；每步 pin 精确 piece 版本（0.5.3）不自动升级，升级显式；piece-syncing 新 piece 无需升级服务器；企业层 SAML SSO/SCIM/RBAC/audit logs/private pieces/platform API keys（packages/ee 商业许可）；allowlist 从紧开始+生产锁计划+季度审计 |
| 5 | Make（自定义 Webhook） | OK | Custom webhook 模块生成唯一 HTTPS URL；每个 scenario 必须独享 webhook（不能跨 scenario 复用）；Add 配置名称保存生成端点；测试 webhook 发 sample data→执行日志验证字段映射；激活后持续监听；邮件/网络钩子变体 custom mailhooks |
| 6 | Pipedream（Sources 事件触发器） | OK | HTTP source=唯一 endpoint（request bin）可 API 管理；$.interface.http + customResponse；sources 经 Connect API deploy（externalUserId+webhook_url）；emitted events 触发其他 workflow（REST /subscriptions?emitter_id&listener_id）；单 workflow 可听 10 个 RSS 源；事件源与 workflow 解耦 |
| 7 | Anthropic（Tool Use 流式 SDK） | OK | tool_runner beta SDK 简化多轮工具调用（迭代 yields stream）；stream=True + get_final_message() 累积消息；SSE 流式消息事件；Java createStreaming/TS stream/CLI ant messages create --stream --format jsonl；tool use 支持参数级细粒度流式（beta） |
| 8 | deeplearning（提示工程课程体系） | OK | ChatGPT Prompt Engineering for Developers：两原则+系统化工程；四大任务 Summarizing/Inferring/Transforming/Expanding；推断模块非结构化→结构化提取；Prompt Engineering with Llama 2&3（Llama Guard 安全）；系统提示+少样本+参数控制 |
| 9 | GitHub（Dependabot 配置） | OK | dependabot.yml groups+applies-to: security-updates 单 PR 多依赖；Advanced Security 页 Enable alerts/security updates/version updates；versioning strategy 默认；registries 私有源（git/type+token）；multi-ecosystem groups 跨包管理器分组 |
| 10 | OpenClaw（Hooks 会话记忆） | OK | session-memory hook：/new、/reset 触发保存会话上下文到 <workspace>/memory/YYYY-MM-DD-slug.md（须配置 workspace.dir）；bootstrap-extra-files（agent:bootstrap glob 注入）；registerSessionExtension+sessions.pluginPatch 持久插件状态；memory 分层=每日日志+ MEMORY.md 永久参考卡；message_received/session_start 事件钩子；Top-K 相关记忆注入新会话 |

## 判重（双键检索，增量判定）
各主题与库内既有锚点重叠>60% 的按"含≥40% 独有增量合并保留增量"落地；纯重复不落。判定明细：
- Dify 会话变量（r270B 锚点）→ 增量=Variable Assigner 节点/可变性对比表/Array[object] 记忆模式
- n8n Webhook 响应（库内 webhook 锚点）→ 增量=四种响应模式+异步回调+64s Wait 限制
- LangFlow API 全局变量（r269A 锚点）→ 增量=X-LANGFLOW-GLOBAL-VAR header 机制+session ID 隔离
- Activepieces Pieces（r267A/r267B 锚点）→ 增量=两级管理+版本 pin+piece-syncing
- Make Webhook（r270B 锚点）→ 增量=每 scenario 独享+测试/激活流程
- Pipedream Sources（r270A/r273C 锚点）→ 增量=customResponse+deploy API+emitted events 订阅
- Anthropic Tool Use（库内无 tool_runner 锚点）→ 新面
- deeplearning 提示工程（r273C 锚点）→ 增量=Llama 2&3 课程+Llama Guard+四任务体系
- GitHub Dependabot（r275A 安全锚点）→ 增量=groups+applies-to+multi-ecosystem+registries
- OpenClaw Hooks（r268A 锚点）→ 增量=session-memory 详细流程+插件状态持久化+memory 分层

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 会话变量与记忆 | 工作流 |
| 2 | n8n Webhook 响应模式与异步回调 | 工作流 |
| 3 | LangFlow API 全局变量与会话记忆 | 工具 |
| 4 | Activepieces Pieces 生态与平台治理 | 工具 |
| 5 | Make 自定义 Webhook 模块 | 工具 |
| 6 | Pipedream Sources 与事件触发器 | 工具 |
| 7 | Anthropic Tool Use 与流式 SDK | 工具 |
| 8 | deeplearning 提示工程课程体系 | 可复用 Skill |
| 9 | GitHub Dependabot 供应链安全 | 工具 |
| 10 | OpenClaw Hooks 与会话记忆自动化 | 工具 |

## 复核
十独点均有当日重新实拉来源；均按增量判定落地；重建 commit 核验通过。版本建议 3.47.0+。