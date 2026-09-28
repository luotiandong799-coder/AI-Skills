# r289B 学习轮留痕（2026-09-29）

## 信源实拉清单（10 站全量逐站；查询词与 r289A 及 r284-r288 全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（条件分支/循环） | OK | **IF/ELSE 节点=条件分支：字符串比较/数值阈值/regex 匹配/包含检查/内容验证，可加多个 Else If 实现复杂路由；条件表达式类 JavaScript 语法（user.age >= 18）**；**默认路径=所有条件不满足时的执行分支**；**建议用 IF/ELSE 做错误处理——LLM 置信度低时路由到备选响应而非不确定结果**；**循环节点输出契约：{{#node_id.output#}}=循环输出数组、{{#node_id.iteration#}}=当前迭代数**；**Jinja2 模板转换与格式化数据（多变量组合）** |
| 2 | n8n（版本/新特性） | OK | **Canvas Groups（2.28.3+ 云端与自托管）：把相关节点折叠成单个命名块——抽象复杂部分/把大工作流拆成可独立管理的小节；选择节点→拖选框或 Shift 点击→成组**；**一键连接 70 个 MCP servers（2026-08）：Airtable/Grafana/Miro/New Relic/Jotform/PandaDoc 加入 Notion/Stripe/GitLab/Apify/Linear/monday.com**；**Code node 支持 Python（pyodide 模块）——1.0 迁移后可用，1.0 前添加的 Code node 不可用 Python**；**SharePoint 节点默认 v2（Microsoft Graph API，OAuth2/Entra service principal）**；**3.0 breaking：Gmail Trigger 版本 1-1.3 合并为 1.4 行为（Max Emails per Poll 每次轮询生效，默认 10 最多 50）** |
| 3 | LangFlow（知识库） | OK | **knowledge base=向量数据库存 embeddings；默认 Chroma 本地存储，可配外部 provider（Chroma Cloud/OpenSearch/Postgres pgvector）；knowledge bases 与 memory bases 共享 DB Providers**；**knowledge bases 不随每次 flow run 重新摄取数据——一次摄取多次查询，更高效**；**OpenRAG 架构：Docling 解析 chunk → OpenSearch 向量+关键词混合检索 → Langflow RAG flow**；**Langflow 支持发布为 MCP Server——知识库可直接成为 Claude/Cursor 等 AI 工具的外部知识库**；**组件库 60+ 预建集成（Pinecone/Weaviate/Qdrant/Chroma/PGVector/Astra DB）；agent nodes 支持 tool-calling 模型 + 结构化输出校验** |
| 4 | Activepieces（构建 piece） | OK | **type-safe pieces framework 全 TypeScript**；**每个 piece 双重身份：工作流构建块 + MCP server（AI agents 可发现/调用）——贡献一个 piece 立即可供 Claude Desktop/Cursor/Windsurf 等 MCP 兼容接口用**；**piece auth 定义：oauth2 带 authorizationUrl/tokenUrl/scopes，clientIdEnvKey/clientSecretEnvKey 从环境变量取**；**Piece Type=custom（定制方案）或 community（分享社区）**；**CLI：ap create-piece / npm run build / npm run test；构建后上传 tarball .tgz（npm run pieces -- build --name=...）**；**400+ MCP servers** |
| 5 | Make（版本/恢复） | OK | **Version history：访问并恢复此前保存的场景版本，保留 60 天——回滚非预期改动/排查错误/安全试验新配置；实验前先保存 baseline 版本**；**Scenario recovery（2026-03 全计划）：编辑中会话中断（浏览器崩溃/断网/误关 tab）自动保存 blueprint，返回时一键恢复——恢复的版本在 history 明确标记**；**关键：recovery≠autosave，恢复后仍需点 Save 才永久生效**；**Scenario run replay：用之前 run 的 trigger 数据在当前版本重放——测试/解决错误/backfill 无需新 trigger 数据；自定义 run name 区分 history 中 run**；**blueprints=可复用版本（模块+设置+映射值）可导出/分享/备份（失去访问或换账号）** |
| 6 | Pipedream（执行限制） | OK | **默认超时：HTTP/email 触发器 30s、cron 60s；每段 workflow segment 上限 12 分钟（control flow 边界重置 timeout——长跑工作流可跨段执行）**；**默认内存 256MB/工作流，最大 10GB（套餐相关）；内存 ↑ 比例提升 CPU——CPU 密集任务买更多内存可更快完成**；**$.send.http() 请求超时 5 秒（含 DNS/连接/写 body/服务处理/读 body）**；**pd.flow.suspend 默认 24h 自动取消，可自定义 timeout 毫秒**；**async 警告："This step was still trying to run code when the step ended"——忘了 await Promise / 没 promisify 回调**；**timeout 错误定位到具体 step** |
| 7 | Claude Code（CLAUDE.md 记忆） | OK | **加载模式两值：claude-md-or-agents-md（默认）=读 CLAUDE.md，或没有 CLAUDE.md/CLAUDE.local.md 时读 AGENTS.md；claude-md-and-agents-md=两者一起读，每目录 CLAUDE.md 在前 AGENTS.md 在后**；**Claude Code 跳过已加载的 AGENTS.md——CLAUDE.md 导入或 symlink 的不重复读**；**/init 生成 CLAUDE.md 草稿（构建命令/测试命令/结构概览/发现的约定）**；**CLAUDE.md 每次会话加载，每行花上下文预算——保持精简（Anthropic 官方建议）；Claude 主动过滤与当前任务无关的内容——臃肿文件与你的实际规则竞争注意力**；**imports 优先读（@ 导入文件先读，然后读剩余）** |
| 8 | GitHub Actions（安全加固） | OK | **2026 安全路线图 scoped secrets：secrets 绑定显式执行上下文（repo/org、branch/env、workflow identity/paths、可信可复用 workflow 无需调用方显式传 secrets）——secrets 不再隐式继承，访问需匹配显式上下文；修改过/意外的 workflow 不会收到凭证**；**pin 第三方 action 到完整 commit SHA（tag 可变——2025 tj-actions/reviewdog retag 攻击：tag 被重指向偷凭证代码）**；**GITHUB_TOKEN 默认 read-only（工作流级默认，job 级按需写）**；**env: 映射传递不可信输入（环境变量=净化边界，shell 展开把它当数据不当代码）——适用于所有用户可控上下文（PR 标题/issue 正文/commit 消息/分支名/评论）**；**用 JS action 替代内联脚本处理 context 值**；**OIDC 替代长期云凭证（短命凭证 scoped 到特定 role，云侧信任策略 pin repo+branch）**；**删除并轮换暴露 secrets；结构化数据不当 secret（redaction 失败）；公开仓库不用 pull_request_target** |
| 9 | OpenClaw（技能创建规范） | OK | **SKILL.md 最小要求=frontmatter 的 name + description；description 显示给 agent + 斜杠命令发现，保持一行 <160 字符；name 用小写字母/数字/连字符，目录名与 frontmatter name 对齐**；**技能放 skills/ 目录（workspace 下），可子目录组织；OpenClaw 遵循 AgentSkills 规范（与 Anthropic 兼容）**；**最佳实践：简洁明了——指示模型做什么而不是如何成为 AI；安全第一——skill 用 bash 时确保提示词不允许来自不受信任用户输入的任意命令注入；本地测试 openclaw agent --message "use my new skill"**；**Skill Workshop=审查和批准 agent 起草的技能提案** |
| 10 | 腾讯 SkillHub | OK | **基于 OpenClaw 官方开源生态的本土化技能平台（腾讯云 Lighthouse 团队）——ClawHub 国内镜像，标准化 AI 技能包分发**；**支持网页+命令行两种方式上传发布，自带版本管理/安全扫描/质量评分；技能包遵循统一规范，可直接被 OpenClaw/Cursor/Claude Code 加载**；**规模：半年聚合近 8 万 Skill，月下载量 1700 万+，累计 6000 万+，国内最大 Skill 创建与分发平台；全球 AI Agent 工具总量 44 万+，AI Skill 近 30 万，日均新增 1300+**；**SkillPay 支付体系（2026-07）：技能分发+Agent 调用+技能支付三方打通，Agent 付费技能商业化（企业三步接入）**；**三类技能：内置（平台安全审核+质量验证，覆盖办公/医疗/图像/音视频等 7 大领域，SkillHub 社区来源自动检测新版本自动更新）/ 企业共享（审批后企业内复用）/ 自定义（ZIP 导入）** |

## 判重（双键检索，增量判定）
- Dify 条件分支/循环（r284-r289A 未落分支/循环节点契约）→ IF/ELSE 错误处理建议/循环输出契约/JS 语法/默认路径 → **新面**
- n8n 版本演进（r289A 子工作流不覆盖）→ Canvas Groups/一键 70 MCP servers/Code node Python/3.0 breaking → **新面**
- LangFlow 知识库（r285C 已落"LangFlow 记忆"）→ 重叠约 60%，增量=知识库机制（不随 run 重摄取）/发布为 MCP Server/OpenRAG 架构 → **合并保留增量**
- Activepieces piece（r287A 已落"Pieces CI/CD"）→ 重叠约 60%，增量=双重身份（块+MCP server）/auth 定义结构（oauth2 三件套+EnvKey）/Piece Type custom-community → **合并保留增量**
- Make 版本/恢复（r289A 聚合不覆盖）→ version history 60 天/实验前存 baseline/scenario recovery（recovery≠autosave）/run replay/blueprints → **新面**
- Pipedream 执行限制（r289A 凭证不覆盖）→ 默认超时 30s/60s/12 分钟段/内存 256MB→10GB/$.send.http 5s/suspend 24h/async 警告 → **新面**
- Claude Code 记忆（用户偏好已含 CLAUDE.md 写作纪律）→ 重叠约 60%，增量=加载模式两值/AGENTS.md 去重机制//init 生成/上下文预算建议 → **合并保留增量**
- GitHub Actions 安全（r284-r289A 无 Actions 安全主题）→ scoped secrets/pin SHA（retag 攻击）/read-only token/env 净化边界/OIDC → **新面**
- OpenClaw 技能规范（wb-skill-authoring 已落技能编写方法论）→ 重叠约 60%，增量=SKILL.md 最小 frontmatter/description<160 字符/目录名对齐/bash 注入安全/workshop 审批 → **合并保留增量**
- 腾讯 SkillHub（r289A 对比表仅一行提及）→ 本次实拉完整机制/规模/SkillPay 商业化/三类技能 → **新面**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 条件分支与循环节点契约（新面） | 工作流 |
| 2 | n8n Canvas Groups 与 Code node Python（新面） | 工具 |
| 3 | LangFlow 知识库机制与 MCP 发布（合并增量） | 工具 |
| 4 | Activepieces piece 双重身份与 auth 契约（合并增量） | 工具 |
| 5 | Make 版本历史与场景恢复（新面） | 工具 |
| 6 | Pipedream 执行限制与超时治理（新面） | 工具 |
| 7 | Claude Code 记忆加载模式与上下文预算（合并增量） | 工具 |
| 8 | GitHub Actions 安全加固清单（新面） | 工具 |
| 9 | OpenClaw 技能编写规范（合并增量） | 可复用 Skill |
| 10 | 腾讯 SkillHub 平台机制与商业化（新面） | 工作流 |

## 复核
十独点均有当日实拉来源；6 新面 + 4 合并保留增量（增量均≥40%），零纯重复。