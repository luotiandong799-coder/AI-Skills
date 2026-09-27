# r240-B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（错误处理/并发面） | ✓ | v0.14.0 错误处理（单节点失败不再击穿整个工作流；四类节点自定义错误处理）；三隐性风险（工具响应失配 JSON 字段名与 schema 不一致如 user_id vs userId 解析失败未抛错转空值传递；状态异步撕裂多 Agent 并行共享缓存键未加版本前缀旧结果覆盖新上下文）；广播模式（一触发器同时激活多 Agent 并行延迟 O(n)→O(1) 等全部返回统一聚合；大多数团队误用线性串行）；API 幂等（Idempotency-Key header Redis-backed 24h TTL 防重复；per-tenant 并发守卫 SQL COUNT 默认 50 超限 429；zombie reaper Celery Beat 强制失败 stuck 行）；Error Handling 节点定义替代路径；log_level error 减日志 |
| 2 | n8n（AI agent 记忆/上下文面） | ✓ | 上下文工程四件套（IF/Switch 动态上下文选择按意图/用户类型路由不同检索路径；Code node/Basic LLM Chain 压缩数据总结历史/提取结构化事实再进窗口；子工作流隔离每子 agent 自己上下文只要自己工具数据；memory sub-nodes 管历史几轮持久存哪）；Window Buffer Memory（滑窗最近 k 交互；4096 token 上下文留 5-10 轮够；事务型 agent 4-6 条消息够）；Simple Memory（session key 决定会话两用户不同 key 不同历史；context window length 控制成本）；存储选型（Postgres Chat Memory 生产审计 5-20ms/Redis Chat Memory 可扩展 chatbot session store 1-5ms/Buffer 原型）；session key 映射 trigger 用户/会话 ID 不是 execution ID；context window 10-20 turns 起步全文仍存表；Dynamic Context Trimmer Node 裁剪历史适配 token |
| 3 | LangFlow（部署/安全面） | ✓ | JWT 认证两模式（HS256 对称单服务器/开发；RS256 非对称生产私钥公钥对）；安全基座（LANGFLOW_AUTO_LOGIN=False；LANGFLOW_SECRET_KEY 强密钥；Nginx 反代 TLS 绑定 localhost；UFW 只开 22/80/443；fail2ban+AppArmor；CIS Level 1）；secrets 管理（API keys/PostgreSQL 凭据存 K8s secrets/Vault）；CVE 部署纪律（CVE-2026-33017 未认证 RCE+CVE-2025-34291：实例不能直接互联网可达放认证代理/VPN 后；出口过滤限制进程出站只到所需集成端点消除 base64 外泄回调；WAF+反代前置 origin 校验+限流；inventory 所有 AI workflow 工具）；API 网关（认证授权+用户数据隔离+XSS/注入清洗含 ReDoS 正则） |
| 4 | Activepieces（MCP/嵌入面） | ✓ | Embeddable MCP 授权流（start connection→authRequestId→app 内 Authorize popup→用户点→code→换 token→跑用户 flows）；内置 MCP server（自然语言建 flows/管 tables/测自动化；OAuth 首次浏览器认证）；400+ pieces 全部自动变 MCP servers 最大开源 MCP toolkit；HTTP piece 打任意 REST/GraphQL 带 auth+分页；ap_search_actions/ap_search_triggers 按任务不按名字搜工具（描述任务→找 action→查 schema→跑）；MCP 工具调用结构化输入跑 lookup/create tickets 返回给调用模型 |
| 5 | Make（Sub-Agents/多 agent 面） | ✓ | Sub-Agents 编排（orchestrator 读消息→路由 specialist 账号查询/退款/边缘 case 人类交接；财务文档检查/发票匹配/审批准备分离再返回一个结果）；AI Playbook（88 use cases 8 团队按团队与 AI 成熟度组织每 case 有可部署 scenario）；四角色架构（Router 分类路由/Specialist 领域/Validator 质量合规准确度评审/Orchestrator 协调多步）；两 agent 链（Agent1 起草→Agent2 按质量 rubric 评估批准或重写——显著优于单遍）；语音 agent Bland/Vapi 连 Make |
| 6 | Pipedream（MCP/传输面） | ✓ | MCP server 10000+ 工具单端点 remote.mcp.pipedream.net/v3；SSE+streamable HTTP 双传输动态支持无配置；每 app 专属 MCP server；managed auth per-user credentials 按用户注入 token 工具跑在各用户连接 accounts；2600+ 集成 apps 全发 MCP servers；pd_sdk_debug=true 调试看 API calls；proxy raw API calls tokens 按用户注入 |
| 7 | Anthropic（skills 编写面） | ✓ | 五条技能编写建议（聚焦不同工作流分开技能多个聚焦技能组合优于一个大技能；清晰描述 Claude 用描述决定何时调用；先简单 Markdown 基础指令再加复杂脚本；用示例 skill.md 放输入输出示例展示成功长什么样；增量测试）；description 上限（name ≤64 字符小写数字连字符无 XML 无保留字；description ≤1024 字符非空无 XML）；Claude Code 最佳实践（/clear 不相关任务之间；两次纠正失败后 /clear 重写更好的初始 prompt 上下文被失败方法污染）；CLAUDE.md vs Tools vs Hooks vs MCP 分工表（CLAUDE.md 项目上下文防重复指令/Tools 何时用/Hooks 确定性自动化生命周期事件/MCP 外部工具数据库 API） |
| 8 | skills.sh（CLI 面） | ✓ | npx 免安装（npx skills add vercel-labs/agent-skills；npx skills use repo@skill 生成 prompt 管道给 claude 免安装直接用）；命令集（find 交互/关键词/按 owner；add GitHub 或他源；update 全部更新）；skills-cli update 优化（tree SHA 比较跳过未变更技能）；安装器（重跑 install 即更新；list 显示 scope 全局/项目）；reskill（init skills.json/find/install/list/info/update）；@dcentralab slug 去重+同版本跳过 |
| 9 | deeplearning.ai（agentic 评估面） | ✓ | Agentic AI 课程结构（Reflection 设计模式反思改进输出；Tool use；多 agent 协作；评估 evals 错误分析优先下一步/组件级评估）；Evaluating AI Agents（Arize：router+skill 评估；trajectory 轨迹评估；convergence score 收敛分评估 agent 步骤效率；结构化实验改 prompt/LLM/agent 逻辑；生产监控部署）；AutoGen 设计模式（sequential chats/reflection/tool use/planning）——收敛分+分级评估 r239-A 已落，判重跳过 |
| 10 | GitHub（生态面） | ✓ | OpenSpec spec-driven development CLI（AI 编码前加 structured proposal-spec-design-task 层人机对齐要建什么）；CUA Coding agent（开源 computer-use agent 平台跨 OS 桌面自动化+集群管理+专业决策模型+benchmarks）；Tencent browser agent（开源 CLI+browser extension 让 AI agents 用真实登录浏览器不打断工作）；Mastra 28,339★ TS AI 应用/agent 框架；JeecgBoot 47,975★ 企业级 AI 低代码（"Skills 生成→在线配置→代码生成→手工合并-AI 修改"模式解决 90% 重复工作）；OpenMAIC 多 agent 交互课堂；alibaba/open-code-review 40,636★ |

## 判重基准
双键检索：Dify（r240-A 已落变量交接契约，广播模式+API 幂等+per-tenant 并发守卫独有增量）；n8n（r239-C/r240-A 已落记忆画布/并发，上下文工程四件套+窗口量化+存储选型独有增量）；LangFlow（r240-A 已落 Tool Mode，JWT 认证模式+CVE 部署纪律独有）；Activepieces（r240-A 已落错误三型，按任务搜工具+嵌入授权流独有）；Make（r239/r240-A 已落，四角色+validator 质量门+两 agent 链独有）；Pipedream（r240-A 已落 Data Store，SSE+streamable 双传输+调试旗独有）；Anthropic（r238/r239 已落，技能编写五建议+两次纠正后 clear 独有）；skills.sh（r238-C/r239-B 已落安装方法论，skills use 免安装+update tree SHA 跳过独有）；deeplearning.ai（r239-A 已落评估五 Lab 收敛分，本轮判重跳过）；GitHub（r240-A 已落，OpenSpec spec-driven+JeecgBoot Skills 生成链独有）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① n8n 上下文工程四件套 | IF/Switch 路由+Code 压缩+子工作流隔离+memory 管历史；窗口 5-10 轮；Postgres 审计/Redis 低延迟选型；session key 映射 trigger ID | 工作流 | wb-execute-discipline |
| ② Dify 广播模式+API 幂等 | 触发器同时激活多 Agent 并行延迟 O(n)→O(1)；Idempotency-Key 24h TTL；per-tenant 并发守卫 50 超限 429 | 工作流 | wb-execute-discipline |
| ③ Make 四角色+两 agent 链质量门 | Router/Specialist/Validator/Orchestrator；Agent2 按 rubric 评估批准或重写 | 工作流 | wb-execute-discipline |
| ④ Anthropic 技能编写五建议 | 聚焦拆分/示例展示成功/先简单；两次纠正失败后 /clear 重写 | 可复用 Skill | wb-execute-discipline |
| ⑤ skills CLI 免安装+智能更新 | npx skills use 生成 prompt 管道给 agent；update tree SHA 跳过未变 | 工具 | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造。
- 功能套件检查：wb-ponytail/wb-max-token-saver/wb-context-compressor 无新可优化项（上下文工程四件套与 context-compressor 同源已覆盖，窗口量化已落 compressor）。
- 垃圾：本轮未产生临时文件。
