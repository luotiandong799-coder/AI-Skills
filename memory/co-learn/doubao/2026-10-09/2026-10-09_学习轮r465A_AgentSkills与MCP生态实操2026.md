# 2026-10-09 学习轮 r465A：Agent Skills 与 MCP 生态实操 2026

轮次：r465A（doubao 侧批 r465 第 1 轮）
判重：双键 grep KB 5275 行 + 留痕基线 → 已落相关面：技能评测与触发质量（wb-skill-authoring）、Agent 工具面安全（wb-context-compressor §Agent 工具面安全）、MCP 选型五标准（用户偏好）、技能治理（CLI/备份/分组）——本主题=**官方规范与生态实操面**（Anthropic 官方 SKILL.md 编写清单（<500 行/Gotchas 节/渐进披露/文件引用一层深/审计日志）、Claude Code 实战经验（不写显而易见/从实际失败积累 gotchas）、skills.sh/SkillsMP/clawhub 生态与 npx skills CLI 安装流程、MCP 2026 安全基线（stdio RCE 漏洞/30+ CVE/iss 校验/Streamable HTTP 默认/permission ask-allow-deny 三级）、MCP 选型实操（小精选集/官方 server/数据库只读角色））——已落管"技能怎么测/工具面怎么防"，本面管"官方怎么规范写 skill+生态怎么装+2026 MCP 安全事件基线"，重叠约 35%，独有增量≥60%，按增量判定落地；净增 5 独点。
实拉：3 query×10 站（claude-platform-overview/claude-skills-guide/r2-agent-skills-pdf/anthropic-blog-bestpractices/claude-api-skill/managed-agents-skills/anthropic-helpcenter/anthropic-resources-guide/claude-code-skills-lessons/claude-agents-skills + skillsmp-ko/skills-sh-docs/iesdouyin-3sites/iesdouyin-platforms/skills-sh-faq/agskills-dev/skillsmp/skillsmp-fr/skillsmp-pt + mcp-rc-2026/maketocreate-mcp/moksh45-mcp/dev-austria-mcp/nerdleveltech-mcp/asoasis-mcp/levelop-mcp/sfeir-cheatsheet/getknit-mcp/clickhelp-mcp，2026-10-09 实拉），逐站带来源标识。

## 落地 5 独点（每点标注提升层）

### 1. Anthropic 官方 Skill 编写清单（可复用 Skill）
来源：anthropic-blog-bestpractices / r2-agent-skills-pdf / anthropic-resources-guide
- **规范核心**：一个 Skill=一个 SKILL.md（YAML frontmatter + Markdown 正文）；frontmatter 的 description 决定何时激活——**description 要具体且含关键触发词+同时写"做什么"和"何时用"**。
- **编写清单**：SKILL.md 正文 **<500 行**（更多细节放独立文件）；附加细节分离文件；**渐进式披露**（先给概述，细节按需下沉）；文件引用一层深（不引深层路径）；示例具体不抽象；一致术语；无时效信息（有就放 old patterns 节）；工作流步骤清晰；API 场景加审计日志（audit logging）。
- 提升层：可复用 Skill（编写规范）。

### 2. Gotchas 节=最高信号内容（可复用 Skill/工作流）
来源：claude-code-skills-lessons / claude-agents-skills
- **别写显而易见的**：Claude 已经会写代码、能读你仓库——skill 里写"如何用 Python"是浪费 token，写的是**领域知识**。
- **Gotchas 节从实际失败点积累**：任何 skill 最高信号内容=Gotchas 节，从 Claude 用你 skill 时反复踩的坑构建，随时间持续更新（例："subscriptions 表是 append-only"）——skill 是活的，要迭代捕获新坑。
- 提升层：可复用 Skill（Gotchas 积累法）。

### 3. Skills 生态与 CLI 安装（工具/可复用 Skill）
来源：skills-sh-docs / skills-sh-faq / skillsmp / iesdouyin
- **三市场定位**：skills.sh=技能目录+排行榜+`npx skills add <owner>/<skill>` CLI；SkillsMP=全球最大多语言市场（中文界面完善，按场景找技能）；clawhub/OpenClaw 官方注册中心（生态兼容性最好、质量审核严格）。
- **安装纪律**：`npx skills add vercel-labs/agent-skills` 安装、`npx skills update` 拉更新；**装前必读 SKILL.md 和任何脚本**再放进环境——市场索引公共仓库不保证安全。
- 提升层：工具（CLI）/ 可复用 Skill（安装纪律）。

### 4. MCP 2026 安全基线（可复用 Skill/工具）
来源：mcp-rc-2026 / moksh45 / clickhelp / nerdleveltech / asoasis / sfeir
- **2026 现实**：2026-04 stdio transport 曝 RCE 漏洞（厂商数天打补丁）；2026 初 30+ CVE 针对流行 MCP server；2026-07-28 RC 规范做授权加固——客户端必须校验授权响应 `iss` 参数（RFC 9207，SEP-2468），防 mix-up 攻击。
- **安全规则**：关键服务只用厂商维护 server（Anthropic/Figma/Sentry/Microsoft）；生产钉版本 `@package/server@1.2.3`；破坏性工具调用前必须人工确认；**所有 server 输出（含 annotations）视为不可信**；本地 server 沙箱化+展示完整启动命令；审工具描述查隐藏指令；**Streamable HTTP=远程默认，stdio 只留本地紧范围进程**；不暴露 shell-exec/文件破坏工具（无确认门）；Claude Code 权限三级=ask（默认，敏感工具）/allow（只读工具）/deny（不想要）。
- 提升层：可复用 Skill（安全清单）/ 工具（权限配置）。

### 5. MCP 选型实操：小精选集+数据库只读（工具/工作流）
来源：dev-austria / getknit / levelop / maketocreate
- **小精选集 > 大目录 dump**：几个精挑 server 胜过一堆目录堆；开发工具类（GitHub/Linear/Jira/Notion/Slack）官方或近官方 server 维护良好——**直接用现成，自己建 GitHub MCP 是白费工**；业务数据（HR/薪酬/ATS）才考虑自建。
- **数据库类纪律**：连 **read replica 或 staging + read-only role**，绝不拿生产写凭证接 agent——**agent 不需要 DELETE**；2026 短名单=GitHub 官方（PR/issue/代码搜索/Actions）、Postgres MCP Pro（含索引顾问，替 Anthropic 归档版）、Firecrawl（网页→结构化数据）。
- 提升层：工具（选型）/ 工作流（数据库接入纪律）。

