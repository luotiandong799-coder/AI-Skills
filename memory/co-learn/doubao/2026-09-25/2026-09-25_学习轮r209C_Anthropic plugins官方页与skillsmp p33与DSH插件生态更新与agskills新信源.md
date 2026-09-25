# 学习轮 r209-C：Anthropic plugins官方页与skillsmp p33与DSH插件生态更新与agskills新信源（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/33（#3201-3245） | OK（darwin-skill 2.0/pr-quiz 等） |
| 2 | deepseek-plugin.org 首页复拉 | OK（Top10 更新：desktop/agentscope 等新条目） |
| 3 | docs.pipedream.com/connect/ | OK（MCP server 10k tools，与 r207B 重叠确认） |
| 4 | agentmore.chatglm.cn | 登录墙空页（记录） |
| 5 | docs.anthropic.com/claude-code/plugins（0-3984） | OK（plugin vs standalone/manifest/结构） |
| 6 | skillhub.cloud.tencent.com（3259/44457 取） | OK（Plugin 广场/SkillPay 计费） |
| 7 | docs.langflow.org 根页 | OK（v1.11.x 与 r206-A 重叠确认） |
| 8 | general_search GitHub agent skills 生态 | OK（agskills.dev/archify/cognee 线索） |
| 9 | anthropic plugins 续读（3984-5860 全取完） | OK（marketplace pin/validate/迁移） |
| 10 | agskills.dev（3022/8535 取） | **新信源**（16,561 skills 索引/antigravity 1400+） |

## 独点（3 个）
### C1：Anthropic plugins 官方页完整版：插件体系规范与 marketplace pin 机制（来源：docs.anthropic.com/claude-code/plugins 全 5860B，2026-09-25 实拉；与 r209-B B1 skills 页互补的插件封装层）
- **plugin vs standalone 决策**：standalone（`.claude/` 目录）适合个人工作流/快速实验；plugins（自包含目录+.claude-plugin/plugin.json manifest）适合团队共享/社区分发/版本化发布/跨项目复用——**先 standalone 快速迭代，要分享时再转 plugin**。
- **plugin 结构硬规范**：`.claude-plugin/` 只放 plugin.json；`skills/`（<name>/SKILL.md）/`commands/`/`agents/`/`hooks/`（hooks.json）/`.mcp.json`/`.lsp.json`（LSP server：extensionToLanguage 映射）/`monitors/`（monitors.json）/`bin/`（进 Bash PATH）/`settings.json` 全部在 plugin 根——**常见错误：把 commands/agents/skills/hooks 放进 .claude-plugin/ 目录**。
- **背景监控 monitors（新模式）**：`monitors/monitors.json` 数组——命令每行 stdout 作为通知发给 Claude（`tail -F ./logs/error.log`），**插件激活自动启动，无需指令 Claude 开 watch**——日志/文件/外部状态被动推送型监控。
- **settings.json 默认配置**：`agent` key 激活插件的自定义 agent 作为主线程（system prompt/工具限制/模型一起换）——**插件可改变 Claude Code 默认行为**；settings.json 优先于 plugin.json 的 settings；未知 key 静默忽略。
- **双 marketplace**：`claude-plugins-official`（Anthropic 策展，无申请流程）+ `claude-community`（第三方评审后落地）；**批准后 pinned 到具体 commit SHA**，CI 自动 bump pin，目录每晚同步——供应链可追溯。
- **验证与评测门禁**：`claude plugin validate` 本地验证（✔ passed；--strict 警告当错）；**`claude plugin eval` 用测试 prompt 多次跑 with/without 插件看贡献与回归**（与 caliper 闭合评测同族）；官方建议 gate CI。
- **迁移路径**：.claude/ 下 commands/agents/skills 直接 cp 进 plugin 根，hooks 从 settings.json 移到 hooks/hooks.json（jq 提 file_path 例）；**迁移后删原文件防重复**；同名 agent .claude/ 优先，插件版只在删除原文件后生效；skill 命名空间 `/plugin-name:skill-name` 与原 `/skill-name` 并存不互覆盖。
- 判据：**共享/分发/版本化用插件封装，个人工作流用 standalone**；监控型能力用 monitors 被动推送；分发走 marketplace pin 保证供应链可溯。
- **提升层**：工具 / 可复用 Skill。

### C2：skillsmp p33：darwin-skill 2.0 自主技能优化器与 pr-quiz 提交前自测门（来源：skillsmp.com/skills/page/33 #3201-3245，2026-09-25 实拉）
- **darwin-skill 2.0（★6,048，自主 skill 优化器）**：集成 Microsoft Research **SkillLens（arXiv 2605.23899）9 维评分 rubric**（structure + effectiveness + meta-skill blacklists）+ **SkillOpt（arXiv 2605.23904）验证门控设计** + HITL 检查点；用 9 维 rubric 评估 SKILL.md，**hill-climbing + git version control** 逐步优化，**独立 judge agent 盲评**（避免自评偏差），测试 prompt 验证改进、**收益递减自动停止（auto-break）**，生成可视化结果卡。判据：**技能优化=评分驱动 hill-climbing+盲评+自动收敛，不是手工改**（与 wb-skill-authoring caliper 评测互补：caliper 管"测激活"、darwin 管"自动改"）。
- **pr-quiz（★92,765，AI 代码 PR 提交前自测门）**：PR 作者在请求评审前先被考自己的分支——范围 branch diff、读改动代码，问"改了什么/为什么/怎么工作/可能破坏什么/必须处理哪些边界"，**诚实评分 Correct/Partial/Incorrect 带真实答案 file:line**，给就绪判定点名需重学区域——**尤其针对 AI 写的代码**（作者可能没真正理解）；--free-text/--questions N/--save 计分卡。判据：**AI 生成代码上评审桌之前，先考作者理解度**（与 wb-execute-discipline"AI 代码=junior 写的必须过评审"互补）。
- **cite-verify（引文验证）**：Queries **Crossref 规范元数据**查重——抓 LLM 幻觉（**真实 DOI/NBER 编号配虚构标题**）；**opensource-pipeline**（fork+清理+打包 3 代理串行公开化私有项目）；**news-pulse**（股价异动 4 并行 agent：公司事件/监管/行业对手/市场情绪→事件时间线+异动主因）。
- 附：idea-evaluator（五维 Higher/Faster/Stronger/Cheaper/Broader+致命缺陷审计）、data-access（A股零鉴权取数：**只允许登记的脚本腾讯/新浪/同花顺/baostock/深交所/东财，禁止凭模型记忆给数**——与用户"禁止编造数据"同源）。
- **提升层**：可复用 Skill / 工作流。

### C3：DSH 插件生态更新与 agskills.dev 新信源（来源：deepseek-plugin.org 复拉 + agskills.dev 首拉，2026-09-25 实拉）
- **DSH Top10 更新（新条目）**：anywhere-labs deepseek-harness-desktop（★16,300，**Electron 桌面应用**：原生窗口/系统托盘/profile 切换/独立终端/更新检查）；zhu1090093659 dsh-web（★6,539，web 生态聚合枢纽+创意工坊）；liustack modlens（★3,388，官方插件）；agentscope-ai typescript（★3,374，**记忆管理套件**：跨会话记住/精炼/回忆用户信息做个性化交互）。
- **agskills.dev（Agent Skills Marketplace，新信源）**：**16,561 Skills Indexed** 开放库；Featured：obra/superpowers（★171.7k）、anthropics/skills（★128.1k）、lobehub/lobe-chat（★75.8k）、**sickn33/antigravity-awesome-skills（★36.6k：1400+ agentic skills 覆盖 Claude Code/Cursor/Codex CLI/Gemini CLI/Antigravity，含 installer CLI/bundles/workflows）**、vercel-labs/agent-skills（★25.9k）、pbakaus/impeccable（★21.3k 设计语言）；Trending：**steipete/clawdis（★369.5k，"Your own personal AI assistant. Any OS. Any Platform. The lobster way"）**；Recently updated：breath57/dingtalk-skills（**钉钉 Skill 库，curl only 自动配置**）、jamditis journalism skills；Hot Contributors：affaan-m（184 skills）。
- **腾讯 SkillHub 生态面**：GitHub MIT 开源、可安装（skillhub.cn/install/skillhub.md）；DSH Plugin 广场（routing-suite 7.2k/dsh-market 4.0k/modlens 4.0k）；**SkillPay 企业服务按调用计费**（本月调用 12.8 万次/收益 ¥3.19 万为示例数据）——技能分发商业化。
- 判据：**插件生态多市场交叉监控（DSH/SkillHub/agskills）**；桌面化封装（Electron）与跨工具技能库（antigravity 1400+）是技能分发新形态。
- **提升层**：工具 / 可复用 Skill。

## 判重说明
- C1 → r209-B B1 同域（Claude Code skills）但本页为**插件封装层全规范**（manifest/结构/monitors/settings agent/marketplace pin/validate/迁移），增量 >60%，落。
- C2 → r209-A A2 已落 click-path-audit（p31 与 p33 同 skill 重复出现不重落）；darwin-skill 2.0/pr-quiz/cite-verify 为新增量，落。
- C3 → 新信源 agskills.dev 首拉 + DSH Top10 新条目（desktop/agentscope 等）+ SkillHub SkillPay；与 r208-C C2（SkillHub 技能生态）部分重叠但本次为本轮实拉新增量（SkillPay 计费/agskills 索引规模），合并保留增量落地。
- 未落：Pipedream Connect（r207B 重叠确认）、LangFlow 根页（r206-A 重叠确认）、AgentMore（登录墙）、GitHub 搜索线索（archify/cognee 仅线索）。
