# 学习轮 r203-B：技能注册表API化与子代理fork与持久记忆与大payload上传与插件供应链签名与简历Claim契约（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/llms.txt 后半 | OK（插件开发 specs：签名验证/自动发布 PR/远程调试/key-value 持久存储） |
| 2 | docs.n8n.io/flow-logic/ | OK（144 字导航壳，无独点） |
| 3 | docs.langflow.org/quickstart | 死链（不重试） |
| 4 | make.com/en/help/scenario-builder | 死链（不重试） |
| 5 | pipedream.com/docs/cron/（Triggers 全文） | OK（9855 字：大 payload 上传/x-pd 参数/HTTP 认证两式） |
| 6 | docs.anthropic.com/en/docs/claude-code/sub-agents | OK（13044 字：fork/isolation worktree/持久记忆/--agents JSON） |
| 7 | skillsmp.com/skills/page/16 | OK（#1501-1533） |
| 8 | deepseek-plugin.org/plugins 续拉 | OK（#20-22：CloudBase/Aegis 工作纪律/dsh-vision-router） |
| 9 | openagentskill.com | OK（14640 字：注册表四层架构 + resolve API + 信任评分） |
| 10 | waytoagi.com | OK（80377 字导航壳，无独点） |

## 独点（5 个）
### L1：OpenAgentSkill 技能注册表四层架构：意图→推荐→信任→安装路径，agent 可调用 API（来源：openagentskill.com 全文）
- **注册表不是静态目录，是 agent 可调用的解析循环**：`POST /api/agent/resolve` 输入任务自然语言 → 返回 `{recommended_skill, install_command, why_recommended[], risk_summary{safety, notes[]}}`——**任务意图到技能安装命令的一次 API 调用**。
- **信任档案（trust profile）在安装前展示**：fit（工作流匹配）/quality（质量分）/freshness（新鲜度）/risks（风险提示）/readiness（就绪说明）与安装命令并排——**"装之前把风险和安装命令放一起"**。
- **risk_summary 结构化**：safety=review before install + notes（network access、verify sources）——安装决策的审计信号。
- 规模：33,229 可安装技能 / 25,505 项目 / 222 技能带证据 / 588 agent outcomes。
- 判据：**技能发现要 API 化（agent 自己调 resolve），不能只给人浏览**；每次安装前必须有可读的信任/风险摘要。
- **提升层**：工具 / 工作流。

### L2：子代理三新能力：fork 会话观察引导 / 持久记忆目录 / worktree 隔离（来源：docs.anthropic.com sub-agents 全文）
- **Fork the current conversation**：把当前会话 fork 成可观察/可引导的运行分支——`Observe and steer running forks`；**fork 与命名 subagent 不同**（fork 是会话副本，命名 subagent 是配置化 worker）——临时并行分支无需先定义 subagent。
- **subagent 持久记忆**：配置 `memory: User` → `~/.claude/agent-memory/` 目录，subagent 跨会话累积洞察（codebase patterns、recurring issues）——**worker 也可以有自己的长期记忆**。
- **`isolation: worktree`**：subagent 获得仓库隔离副本，`cd` 不持久也不污染主会话工作目录——高危操作的隔离执行面。
- **CLI `--agents 'JSON'`**：会话级 subagent（不落盘），适合自动化脚本/快速测试；frontmatter 字段与文件版一致（含 maxTurns、effort、background、initialPrompt）。
- 判据：**临时并行用 fork、长期 worker 用命名 subagent、隔离执行用 worktree**；worker 记忆按角色分目录不共用。
- **提升层**：工具 / 可复用 Skill。

### L3：Pipedream 大 payload 上传 + x-pd 请求参数（来源：pipedream.com/docs/cron/ Triggers 全文）
- **512KB 默认 body 上限可突破**：加 `pipedream_upload_body=1` query 或 `x-pd-upload-body: 1` header → 任意大小 payload 上传到 Pipedream 托管 S3，返回 **signed URL（30 分钟有效）**，`steps.trigger.event.body.raw_body_url` 引用——**大文件与请求 body 分离，事件只带引用 URL**。
- **`x-pd-nostore: 1`**：本次执行不记录任何日志/事件（Data Retention 控制可关全部）——隐私敏感负载的审计豁免。
- **`x-pd-notrigger: 1`**：发测试事件不触发生产 workflow，只在测试事件列表显示——**测试与生产触发隔离**。
- **event source vs trigger 分工**：source 是独立资源（收集+emit 事件），一个 source 可触发任意多个 workflow——**数据采集与处理逻辑解耦**。
- 判据：**大载荷走"引用 URL"而非 body 直传**；测试/生产触发用请求参数隔离，不靠临时改配置。
- **提升层**：工具 / 工作流。

### L4：Dify 插件供应链：第三方签名验证 / GitHub Actions 自动发布 / 远程调试 / 内置 key-value 持久存储（来源：docs.dify.ai llms.txt 插件开发 specs）
- **插件签名验证**：Community Edition 支持第三方签名验证（key pair 生成→插件签名→环境配置），`FORCE_VERIFYING_SIGNATURE` 处理验证异常——**非官方 Marketplace 插件安装前必须过签名**。
- **自动发布插件 via PR**：GitHub Actions 自动化发布流程（无需人工干预）——插件的 CI/CD 发布通道。
- **Plugin Debugging 远程调试**：环境变量文件+启动远程调试+验证安装状态——插件开发的标准调试回路。
- **Persistent Storage**：内置 key-value 数据库跨交互保持状态——**插件状态不依赖外部 DB**。
- 判据：**插件供应链=签名验证（装前）+ 自动发布（发时）+ 内置状态存储（跑时）**；自建插件平台要三件套齐。
- **提升层**：工具 / 工作流。

### L5：interview 简历 Claim→轮次评分契约（来源：skillsmp #1516，ASu-skills，中文）
- **从简历提取需要验证的经历 Claim** → 按面试轮次建立问题与评分契约 → 一次一问、证据反馈、弱项复练检查真实掌握程度。
- 与 interview-me（r201-C）分工：那条管"95% 置信度一次一问直到意图清楚"；本条增量=**简历 Claim 显式提取 + 每轮评分契约 + 复练回路**。
- mrbeast-perspective（#1504）附带方法：**可运行分析脚本（4 个内容分析脚本）+ 严格触发边界**（仅在"视频优化/标题/缩略图/Hook/留存率"语境触发，一般"内容创作建议"不触发）——触发边界写法可并入。
- 判据：**面试模拟 = 从简历抽可验证主张 → 按轮次设评分契约 → 证据反馈闭环**；触发边界宁可窄不可宽（一般性问题不抢活）。
- **提升层**：可复用 Skill / 工作流。

## 判重说明
- L1 → r202-A G4 已有 VoltAgent 官方聚合仓；本点"resolve API + 信任评分 + risk_summary 结构化 + 四层注册表"为独有增量（API 化推荐），落。
- L2 → r202-A G1 已有 subagent 五级 scope；"fork 会话/持久记忆目录/worktree 隔离/--agents JSON"四项为独有增量，合并保留。
- L3 → r201-C 已有 Pipedream events/context；大 payload/请求参数/测试隔离为全新独点，落。
- L4 → r201-B 已有 Dify 知识库 API；插件供应链（签名/自动发布/远程调试/key-value）为全新层面，落。
- L5 → r201-C 已有 interview-me；简历 Claim→评分契约+复练为独有增量，合并保留。
- theboardroom（#1518 高管董事会 Go/No-Go memo）与 r203-A K4 评审团模式重叠 >60%，增量（CISO 视角/集成 memo）<40%，并入 K4 不单落。
- Aegis（deepseek 工作纪律插件）与 wb-execute-discipline 概念重叠，观察不落。
