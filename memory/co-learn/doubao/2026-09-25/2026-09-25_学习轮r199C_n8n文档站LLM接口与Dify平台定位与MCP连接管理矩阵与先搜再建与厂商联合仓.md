# 学习轮 r199-C：n8n文档站LLM友好接口与Dify平台定位与MCP连接管理矩阵与先搜再建与厂商官方技能联合仓（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/workflow | OK 全文 |
| 2 | docs.n8n.io/flow-logic | 404（暴露文档站 LLM 接口） |
| 3 | docs.langflow.org/guides | 死链 |
| 4 | docs.activepieces.com/docs/authentication | fetch error |
| 5 | make.com/en/help/getting-started/ | fetch error |
| 6 | pipedream.com/docs/api/ | OK 全文 |
| 7 | docs.anthropic.com/en/docs/claude-code/mcp | OK 全文 12739 字 |
| 8 | skills.sh/all-time | 死链 |
| 9 | skillsmp.com/skills/page/5 | OK（#401-435） |
| 10 | GitHub 生态（搜索） | OK |

## 独点（5 个）
### C1：文档站 LLM 友好接口——全文导出 + ask 问答端点（来源：docs.n8n.io 404 页暴露）
- n8n 文档站提供三件套：**`llms-full.txt` 完整文档语料导出**（一次性拉全站自己解析/检索）；**`welcome.md?ask=<question>&goal=<end_goal>` 问答端点**（GitBook 直接返回答案 + 相关摘录 + 来源，goal 参数定制答案方向）；`sitemap.md` 全站索引。
- **偏好 `.md` URL**（结构化内容）或 `Accept: text/markdown` 头内容协商。
- 判据：**大文档站直接 fetch 单页又慢又碎，先看有没有 llms.txt / llms-full.txt 全文导出**；有问答端点就用 ask 参数拿带来源的直接答案——文档检索从"爬页面"升级为"查语料"。
- **提升层**：工具 / 工作流（文档检索方法）。

### C2：Dify 平台定位——BaaS+LLMOps 组合、企业 LLM gateway 集中治理（来源：docs.dify.ai/guides/workflow 介绍页）
- Dify = Backend-as-a-Service + LLMOps 组合：主流 LLM 支持 + Prompt 编排 + RAG 引擎 + Agent 框架 + 低代码 Workflow + API；名字来源"Do It For You"。
- 三种典型用法：Startup 快速原型（加速成功也加速失败）；成熟企业 RESTful API **把 prompt 与业务逻辑分离** + 管理界面跟踪数据/成本/用量；**企业作为内部 LLM gateway 集中治理 GenAI 采用**。
- 社区规模：180,000 开发者、59,000+ 端用户、60,000 开发者在其上做过首个 AI app。
- 判据：**平台类产品看"定位组合"而非单点功能**；REST API 分离 prompt/业务 + 集中治理是它区别于裸框架的核心卖点。
- **提升层**：生态观察。

### C3：MCP 连接管理矩阵——三传输/三 scope/动态更新/自动重连/channels 反客为主（来源：docs.anthropic.com/en/docs/claude-code/mcp 全文）
- **三传输**：HTTP（streamable-http 推荐，远程首选）、**SSE deprecated**、stdio（本地进程，注入 CLAUDE_PROJECT_DIR 供 server 解析项目路径，roots/list 拿启动目录）。
- **三 scope**：local（默认，~/.claude.json 当前项目私有）/ project（.mcp.json 进版本控制共享团队）/ user（所有项目）；企业 managed 配置（managed-mcp.json 独占 + allowlists/denylists allowedMcpServers/deniedMcpServers 命令级/URL 级限制）。
- **动态工具更新**：MCP `list_changed` 通知——server 动态更新工具/资源无需断开重连。
- **自动重连**：HTTP/SSE 断线指数退避最多 5 次（1s 起加倍）；初始连接 3 次重试（5xx/refused/timeout）；**认证/not-found 错误不重试**（需要配置修改）；stdio 本地进程不自动重连。
- **channels 推送**：server 声明 `claude/channel` 能力 + `--channels` opt-in——**MCP server 主动推消息进会话**（CI 结果/监控告警/Telegram），agent 离线也能被事件唤醒。
- **工具输出上限**：>10,000 tokens 警告，MAX_MCP_OUTPUT_TOKENS 提高；**MCP Tool Search** 默认开启（工具多时在 ToolSearch 内等待），关闭走 WaitForMcpServers。
- **plugin 捆绑 MCP**：.mcp.json at plugin root 或 plugin.json inline；`${CLAUDE_PLUGIN_ROOT}`（插件文件）/`${CLAUDE_PLUGIN_DATA}`（跨更新持久状态）/`${CLAUDE_PROJECT_DIR}`；`mcp-server-dev` 官方插件一条命令脚手架 server。
- 安全：连接前 verify trust；fetch 外部内容的 server 有 prompt injection 风险；`workspace` 是保留名。
- 判据：**MCP 连接是"传输+scope+权限+重连"四维配置**；事件驱动型 agent 用 channels 让 server 反向唤醒；选项（--transport/--env/--scope/--header）必须在 server 名前、`--` 分隔命令。
- **提升层**：工具。

### C4：先搜再建（skill-scout）+ 代理评测指标（agent-eval）+ 论文发布会视角（anti-defensive-writing）（来源：skillsmp #402/#434、独立仓）
- **skill-scout（ECC）**：创建新 skill 前**搜索现有 local/marketplace/GitHub/web 四源**再决定 fork 或新建——与学习落地判重规则（来源+概念词双键检索）同源的外部正式化；"先搜再建"是技能开发的默认纪律。
- **agent-eval（ECC）**：编码代理（Claude Code/Aider/Codex）在**自定义任务**上的直接比较——通过率/成本/时间/一致性四指标；评测任务集自定义 + 多指标并列，不是只看 pass@k。
- **anti-defensive-writing（1,308★）**：论文写作全流程阻止"防御性写作"——**论文=学术发布会不是实验日志**：识别最值得发表的价值建最强叙事、不平均展示、不主动示弱、不写实验流水账、**不替审稿人攻击自己**；触发词包括"论文AI味"。
- 同页参考：references（共享规范知识库——其他 skills 按需读取、无需单独触发，是共享 reference skill 的落地形态）；grant-proposal 16,461★ 多国基金（KAKENHI/NSF/NSFC 面上青年优青杰青海外优青重点/ERC/DFG）；gtm-operating-cadence 反模式"leadership meetings consume all time without producing decisions"。
- 判据：**先搜再建 / 多指标评测 / 叙事定位**三条是跨域可内化的动作；"不替审稿人攻击自己"是写作侧最反直觉但最值钱的一条。
- **提升层**：可复用 Skill / 输出。

### C5：厂商官方技能联合仓（VoltAgent）+ npx skills 安装语法 + 外部同名 ponytail 观察（来源：GitHub 生态搜索）
- **VoltAgent**：30+ 公司**官方 agent skills 汇集一个 repo（约 1,500 skills）**——厂商官方技能的"联合目录"形态，替代逐个 repo 找。
- **安装语法 `npx skills add https://github.com/anthropics/skills -skill mcp-builder`**（npx skills 指定仓库+单技能粒度安装；vc.ru 提醒：**不要同时装 plugin 和 npx 副本否则技能双写**）。
- 排行榜（ghtrends agent-skills）：anthropics/skills 151,678★、ComposioHQ/awesome-claude-skills 64,863★、addyosmani/agent-skills 61,252★；周增长榜：mattpocock/skills +13,419、**DietrichGebert/ponytail 132.1k★ +12,598/周**（外部存在同名 ponytail 技能且已 13 万星——撞名生态信号，装任何 ponytail 前先核对来源）。
- 判据：**找官方技能先去联合仓/排行榜，单技能安装用 -skill 粒度**；同名技能是高发撞车点，安装前双键核验来源。
- **提升层**：生态观察。

## 判重说明
- C1 → 各站文档抓取记录已多轮累积；n8n 的 llms-full.txt + ask 端点首次见，文档站 LLM 接口为独有增量。
- C2 → Dify 介绍页首次拉全（此前仅导航壳），平台定位为独有增量。
- C3 → r196/r197 已记 MCP 基础（多仓库）；本篇 12739 字全文，传输+scope+channels+重连+plugin 捆绑为独有增量。
- C4 → 判重"先查同类"已在各批使用；skill-scout/agent-eval/anti-defensive-writing 首次见，三条方法论为独有增量。
- C5 → r198-C 已记厂商技能仓入场（vercel-labs 等）；VoltAgent 联合仓 + npx skills 语法 + ponytail 撞名首次见。
