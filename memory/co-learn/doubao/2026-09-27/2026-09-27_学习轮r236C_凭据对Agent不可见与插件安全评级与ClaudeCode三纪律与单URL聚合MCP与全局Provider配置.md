# r236-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站，全部当日重新实拉）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（Marketplace/Creator Center 面） | ✓ | 内置双向 MCP（v1.6.0+：MCP server 作工具/agent workflow 暴露为 MCP server）；Creator Center & Template Marketplace（发布模板+PartnerStack affiliate 佣金）；插件安全评级卡（Security Rating A/B+outbound calls+访问域名+内存存储上限，安装前可见）；MCP Auth Relay（OAuth relay）；A2A Client 插件（Dify 接入 A2A） |
| 2 | n8n（安全/生产部署面） | ✓ | 凭据加密 at rest+非 admin 赋权 workflow 不可查看提取原始数据+AI Agents 无凭据访问权；AI Agent Sandboxes（capability scoping+least-privilege approved tools）；生产部署 15 实践（HITL/secrets/版本控制/回退/测试/RBAC/TLS/审计日志流 SIEM）；self-hosted Docker/K8s+RBAC/SSO；n8n Agents 上线（Cloud 最新版/self-hosted 额外设置） |
| 3 | Full Stack Skills（2026 路线面） | ✓ | 2026 全栈路线：React 19+TS+Server Components；API 层 thin stateless 函数 Cloudflare Workers；vector DB 新类别（Pinecone/Weaviate/pgvector）；Full AI Stack 三层课程（LLM Engineering & RAG→Agents MCP & Evals：Claude Agent SDK/OpenAI Agents SDK/LangGraph/MCP/guardrails→DevOps Coding Agents：Claude Code/Cursor）；可靠性模式（幂等/outbox/saga/circuit breaker/限流/退避重试） |
| 4 | Pipedream（Connect 面） | ✓ | Private actions（CLI/Node code step 发布私有 action，跨 workflow 可用）；Custom tools（Components API→Connect APIs list/retrieve/run 全可用）；Connect 产品（managed auth+approved client IDs+durable components+serverless；SDK 2400+ APIs；10,000+ 预建 triggers/actions 嵌入 app/agent；MCP remote server 指向 Pipedream） |
| 5 | GitHub 生态（2026-09-26/27 榜面） | ✓ | CopilotKit/OpenBot（AI coworkers 每人一台电脑：浏览器/文件/工具，动作先决定后记录，AG-UI agent 可接入）；affaan-m/ECC（agent harness 性能优化：skills/instincts/memory/security/research-first）；jev-chat-jarvis（手机对话副驾 QQ/X/飞书读上下文）；paperclip（开源管理 agent at work）；vLLM 0.30 GPU weight cache 重启免重载 |
| 6 | skills.sh/ClawHub（安全面） | ✓ | SkillScan（security-first skill vetting：新 skill 必须过 SkillScan 才能用，install/load/add/evaluate 激活）；ClawHub 13000+ skills；capability-evolver（AI self-evolution engine 自主进化）；LobeHub find-skills（bytedance 技能发现安装） |
| 7 | WaytoAGI（AI 编程工作流面） | ✓ | Claude Code 官方 best practices：CLAUDE.md 太长忽略一半→无情修剪/转 hook；trust-then-verify gap→永远给验证（tests/scripts/screenshots）验证不了不交付；infinite exploration 控制；两败后 /clear 重写；@path imports+.claude/rules/ 按文件类型限定；gather→action→verify loop；Cursor+Claude Code 双剑合璧 Edit-Test Loop（写→测→修→通过自主闭环）；Skills/Hooks/MCP 固化发版前检查/CHANGELOG/E2E |
| 8 | Activepieces（MCP 实操面） | ✓ | MCP Server 单 URL 暴露所有连接（largest open source MCP server，400+ app 聚合）；OAuth 首用浏览器认证；授权按项目隔离（Settings→MCP Server 开关+工具类别+URL）；Embeddable MCP（code→token 嵌入）；凭据存 server-side 永不通过 MCP 暴露；HTTP OAuth2/CustomGPT 等 MCP 面 |
| 9 | 智谱（GLM-5 模型面） | ✓ | GLM-5（2026-02：745B/202K context，专为复杂系统工程+长程 agent 任务，代码逻辑密度对标 Claude Opus 4.5，首次集成 DeepSeek Sparse Attention 无损长文本提 token efficiency）；GLM-5.1（MIT 开源 754B MoE 40B active，Gated DeltaNet+standard attention）；GLM-5.3（最强开源 coding 模型）；GLM-5V-Turbo（原生多模态 coding：设计稿/截图→可执行前端代码）；Compute Nest 一键部署 |
| 10 | LangFlow（1.8/1.9 版本面） | ✓ | 1.8：全局模型提供商配置（防凭据 sprawl）+V2 workflow API（/workflow 同步端点）+Component Inspection Panel+traces；1.9：Langflow Assistant+Flow DevOps Toolkit+MCP support for IDEs（Settings 里 MCP Client 连 Claude Code/IBM Bob；MCP Tools 先注册 server 再从 sidebar 添加）+token usage display；Agentics bundle（LLM 填表/折叠/生成表格数据）+Guardrails 组件+LiteLLM bundle |

## 判重基准
双键检索：n8n（r236-A 已落 Agents 一等实体，本条独有增量=凭据对 agent 不可见+agent sandbox 最小权限+15 部署实践）；Dify（r236-A 已落 chat-to-agent，r235-C 已落 SkillPay，本条独有增量=插件安全评级卡+Creator Center affiliate+A2A 插件）；Claude Code（r235-A 已落迭代错误三策略，本条独有增量=CLAUDE.md 修剪原则+trust-then-verify gap+两败后 /clear 官方版）；Activepieces（r236-A 已落 AI-ready 目录，本条独有增量=单 URL 聚合 MCP+项目级授权隔离+凭据不透传）；LangFlow（r236-A 已落 Memory bases，本条独有增量=全局 provider 配置+MCP 先注册后添加+DevOps 工具链）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① n8n 凭据不可见+沙箱 | 凭据给 workflow 不给 agent；agent 工具集最小权限；15 生产实践（HITL+回退+测试） | 工作流 | wb-execute-discipline |
| ② Dify 插件安全评级 | 安装前看安全评级卡+outbound/域名声明；Creator Center 模板 affiliate 分发；A2A 接入 | 工具 | wb-execute-discipline |
| ③ Claude Code 三纪律 | CLAUDE.md 太长即忽略→无情修剪；trust-then-verify gap→验证不了不交付；两败后 /clear 重置 | 工作流 | wb-execute-discipline |
| ④ Activepieces 单 URL 聚合 MCP | 一个 URL 聚合所有连接；授权按项目隔离；凭据 server-side 不透传 | 工具 | wb-execute-discipline |
| ⑤ LangFlow 全局 provider+MCP 注册 | 全局配置防凭据 sprawl；MCP 先注册后添加；Flow DevOps 部署工具链 | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：wb-ponytail/wb-max-token-saver/wb-context-compressor 三件套可参照"CLAUDE.md 修剪"优化自身 SKILL.md 长度控制（下轮评估是否合并）；无更优替代品。
- 垃圾：本轮未产生临时文件。
