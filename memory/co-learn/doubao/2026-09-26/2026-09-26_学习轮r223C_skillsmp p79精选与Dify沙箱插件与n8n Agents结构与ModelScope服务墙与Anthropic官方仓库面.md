# 学习轮 r223C：skillsmp p79精选与Dify沙箱插件与n8n Agents结构与ModelScope服务墙与Anthropic官方仓库面（2026-09-26）

## 实拉记录（10 次调用，8 成功 / 2 失败）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/79（#7801-7855，5974/11547 取） | OK |
| 2 | Dify 检索二批（Better E2B Sandbox plugin/1.16-rc1 Babysit） | OK |
| 3 | docs.openclaw.ai/concepts/skills | FAIL（dead，勿重试） |
| 4 | docs.n8n.io/agents/what-chains-do.md | FAIL（404，勿重试） |
| 5 | deeplearning.ai 检索（Agent Skills with Anthropic/Agent Memory 课程） | OK |
| 6 | ngjoo.com/trending（GitHub 热度榜头部 #1-4） | OK（仅头部） |
| 7 | ModelScope 检索（魔粒体系/技能服务墙/创空间部署 Skill） | OK |
| 8 | Anthropic skills 检索（17 官方技能/skill-creator/managed agents） | OK |
| 9 | Pipedream 检索 | OK（与 r223-A 重叠无增量） |
| 10 | n8n agents 检索（n8n Agents 结构/skills 面） | OK |

## 独点（4 个）
### C1：skillsmp p79 精选：按需安装 / 主协调拆活 / 中文文献核查 / 金丝雀监控 / 图表先定义结论（来源：skillsmp.com/skills/page/79，2026-09-26 实拉）
- **agent-sort（affaan-m/ECC ★264,820）**：**并行仓库审查把 skills/commands/rules/hooks/extras 分类为 DAILY 与 LIBRARY 桶，构建针对特定仓库的基于证据的 ECC 安装计划——项目不需要完整 bundle 时按需修剪**（"只装项目实际需要的，不装整个 bundle"判据）。
- **bom（aklofas/kicad-happy ★1,277）**：**BOM 生命周期主协调技能——统一调度 DigiKey/Mouser/LCSC/element14/JLCPCB/PCBWay/KiCad；ALWAYS 触发（即使点名具体分销商）；分析 schematic 找 sourcing 缺口后推荐该调哪个分销/工厂技能，结果写回 KiCad symbol properties**（"调度技能负责拆活与写回，实际搜索由被调技能执行"面）。
- **literature-verifier（yipng05-max ★292）**：**文献真实性验证+中英文幻觉检测——引用真实/DOI 确认/作者-标题-期刊-年份元数据交叉核对/捏造引用识别/URL 校验/参考文献清单审计；支持知网/万方/维普/百度学术及北大核心/CSSCI/CSCD 核心期刊校验**（中文文献库支持面增量）。
- **canary-watch（affaan-m/ECC）**：**部署/合并/依赖升级后监控已部署 URL 的回归问题**（金丝雀回归监控面）。
- **nature-figure（yniantongtian ★25）**：**投稿级 Nature 图表工作流——画前先定义图的结论、证据逻辑、导出需求与评审风险；未选后端时问"Python or R?"并停止；只用所选后端生成/预览/导出/QA**（"画前定义结论与证据逻辑"面）。
- **提升层**：可复用 Skill / 工作流。

### C2：Dify Better E2B Sandbox 插件与 Babysit once fasten forever（来源：Dify Marketplace/Marketplace 检索，2026-09-26 实拉）
- **Better E2B Sandbox plugin（lysonober 0.0.3）**：**workflow 内创建与管理 E2B 云沙箱——Claude Code 集成、Next.js 项目脚手架（npm/bun）、有状态交互式 shell 会话、常见包安装、文件操作、模板构建、完整沙箱生命周期（pause/resume/kill）**（r223-B 1.17.0 E2B 面的插件实现层增量）。
- **Dify 1.16.0-rc1（2026-07-09）Agent Node**：**Agent Node 代表一个 Agent 在特定 workflow 的一次出现——自带 job instructions/input references/output declarations/failure handling**。
- **Build / Babysit flow**：**引导 Agent 跑一两次测试运行，固定运行中发现的配置/文件/技能/工具——"Babysit once, fasten forever"（保姆一次，永久紧固）**（把真实运行中发现的好配置固化成 agent 配置的面）。
- **提升层**：工具 / 工作流。

### C3：n8n Agents 结构与 skills 组件面 + deeplearning 课程面（来源：n8n blog/docs + deeplearning.ai 检索，2026-09-26 实拉）
- **n8n Agents（Introducing n8n Agents，2026-09-25）**：**agent 结构——channels（discord/schedule 等）+tools（built-in n8n integrations/MCP servers/任意 workflow）+skills（可复用 instructions 与 reference files，agent 需要时加载，跨 agent 共享）**（n8n skills 组件面）。
- **AI Agent Tool 多 agent 编排**：**主 agent 可调子 agent 作工具（自带模型/记忆/角色）；AI Agent Tool 可多层嵌套**；拓扑层模式：Orchestrator-Executor（sub-workflows）/Pipeline chains/Parallel Fan-Out-Fan-In。
- **ReAct 并入 Tools Agent**：**n8n 弃用独立 ReAct Agent 改 Tools Agent（内嵌迭代推理/工具选择/观察决策）——现代 LLM 直接工具调用趋势**。
- **deeplearning.ai 课程面**：**Agent Memory: Building Memory-Aware Agents（Oracle，2h7m）——跨会话存储/检索/精炼知识的完整记忆系统，把无状态 agent 变会学习改进的**；**Agent Skills with Anthropic（2h19m）——开放标准格式创建可复用 skills，与 MCP 和 subagents 组合**；**Long-Term Agentic Memory With LangGraph（LangMem 记忆管理）**。
- **提升层**：工具 / 工作流。

### C4：ModelScope 技能服务墙与创空间部署 Skill + Anthropic 官方仓库面（来源：ModelScope/Anthropic 检索，2026-09-26 实拉）
- **魔搭「魔粒体系」（2026-09-20 上线）**：**全站通用激励积分；技能服务墙——个人主页开启展示 AI 商业服务，让有需求的个人/团队更容易找到**（AI 技能变现入口面，个人用户相关）。
- **魔搭创空间部署 Skill**：**本地项目部署到 ModelScope Studio——支持 Gradio/Streamlit/Docker/静态网站四类；覆盖创建/代码同步/部署/日志监控/明文与 secret 变量管理/自动诊断**。
- **modelscope v1.40.1（2026-09-16）**：**add agent idp and mcp/studios openapi**（agent 身份与 MCP/工作室 OpenAPI）。
- **anthropics/skills 官方仓库**：**17 个官方技能（algorithmic-art/brand-guidelines/canvas-design/doc-coauthoring/frontend-design/web-artifacts-builder/mcp-builder/webapp-testing/claude-api/pdf 等）；skill-creator 内置 Claude.ai/Claude Code——从自然语言生成 skills**；**Claude managed agents——会话挂载仓库时自动扫描根 .claude/skills 目录，发现的每个 skill 自动可用（无需 upload 或登记）**。
- **提升层**：工具 / 可复用 Skill。

## 判重说明
- C1 agent-sort/bom/literature-verifier/canary-watch/nature-figure 全新面，落。
- C2 Better E2B Sandbox 插件生命周期细节与 r223-B 的 1.17.0 E2B 面重叠>60% 但含≥40% 插件实现增量（有状态 shell/pause-resume-kill/脚手架）+Babysit once fasten forever 新面，合并保留增量，落。
- C3 n8n Agents skills 组件面为 r222-C 的 n8n Agents 面增量（skills 可复用跨 agent 共享具体机制）；deeplearning 课程面（Agent Memory/Agent Skills 课程大纲）新，合并落。
- C4 魔搭魔粒体系/技能服务墙/创空间部署 Skill 全新面；anthropics/skills 官方仓库 17 技能清单+skill-creator+managed agents 自动扫描为工具面增量，落。
- 未落：Pipedream 检索（与 r223-A Edit with AI/MCP server 面重复无增量）；ngjoo trending 仅头部（#1 ponytail/#2 ECC/#3 graphify/#4 caveman，graphify 代码图谱面与 r222-A CodeGraph 同族，无足够增量不单列）。
