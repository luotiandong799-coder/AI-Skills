# 学习轮 r202-C：ClaudeCode agent-teams机制与fast-jev逐字压缩与名人顾问团与n8n迭代语义（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/tools/ | 死链 |
| 2 | docs.n8n.io/flow-logic/looping/ | OK（2980 字） |
| 3 | docs.langflow.org/starter-projects/ | 死链 |
| 4 | make.com/en/help/functions/data-structures | fetch error |
| 5 | docs.pipedream.com/docs/components/ | 死链 |
| 6 | docs.anthropic.com/en/docs/claude-code/agent-teams | OK（5840 字） |
| 7 | skills.sh/skills | OK（56 字，GitHub 官方 secure-code-game 9 技能，无独点） |
| 8 | skillsmp.com/skills/page/14 | OK（#1301-1336） |
| 9 | deepseek-plugin.org/plugins | OK（96587 字节目录，本次前 3367 token） |
| 10 | trendshift.io/weekly | OK（25 项） |

## 独点（4 个）
### J1：Claude Code agent teams 完整机制：lead/teammate/task-list/mailbox + hooks 质量门（来源：docs.anthropic.com/en/docs/claude-code/agent-teams 全文）
- **与 subagents 的选择判据**：workers 需要互相通信吗？**subagents 只回报主 agent、从不互相说话；agent teams 共享任务清单、claim 工作、直接互相通信**——要讨论协作用 teams，只要结果用 subagents。
- **架构四件**：team lead（主会话协调）/ teammates（独立 Claude 实例，独立上下文）/ task list（共享）/ mailbox（agent 间消息）。**实验性默认关闭**（CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1）。
- **任务协调**：任务三态 pending/in progress/completed + **任务依赖**（有未解决依赖的 pending 任务不可 claim）+ **自 claim**（完成后自动捡下一个未分配未阻塞任务）+ **文件锁防并发竞争**。
- **hooks 质量门（独有）**：TeammateIdle（teammate 将空闲时运行，**退出 code 2 = 发反馈让它继续工作**）/ TaskCreated（退出 code 2 阻止创建并反馈）/ TaskCompleted（退出 code 2 阻止标记完成并反馈）——**质量门是钩子不是人工**。
- **plan approval 门**：复杂/风险任务让 teammate 先只读 plan mode，lead 审批（可拒绝带反馈，teammate 修订重交）后才退出 plan mode 实现；给 lead 审批标准（"只批准含测试覆盖的计划"）。
- **subagent 定义可复用为 teammate**：teammate 用定义 tools/model，body 附加为额外指令（不替换）；**skills/mcpServers 字段在 teammate 模式不生效**（从项目/用户设置加载）；teammate 继承 lead 权限（spawn 时不能设 per-teammate 模式）。
- **存储**：~/.claude/teams/{name}/config.json（运行时状态**勿手编**，下次状态更新覆盖）+ ~/.claude/tasks/{name}/；项目级 teams.json 不算配置。
- 判据：**多会话并行用 teams（可通信），单会话内并行用 subagents（只回报）**；质量门挂 hooks（idle/task 事件）而非靠自觉；审批门只用于复杂/风险任务。
- **提升层**：工具 / 可复用 Skill。

### J2：fast-jev-compaction 逐字保留压缩 + cloudflare 官方安全审计技能（来源：trendshift.io/weekly #23/#24）
- **fast-jev-compaction**（tamaratran/fast-jev-compaction）：Claude Code 插件把 compaction summary 替换为 Jev 决策——**每个工具调用和结果在单次快速请求中打分，陈旧的丢弃或截断，保留的逐字（verbatim）保留**——压缩不是重写摘要而是**保留原件、删陈旧**。
  - 与 wb-context-compressor 的增量：**"保留逐字 vs 摘要重写"**——能保留原文就不摘要（摘要丢细节），旧工具结果打分后丢弃/截断。
- **cloudflare/security-audit-skill**（71,526 周涨）：**多阶段安全审计 + 独立验证 + 机器可读发现**——官方厂商安全审计技能化。
- **laya/jev 决策模型小型化生态**：laya（typed decision models）+ laya-mlx（**本地 MLX 运行时 7-14ms 短决策，无文本生成/PyTorch/云 API**）+ kev（Qwen2.5-0.5B 训练可跑 MacBook 的 Jev-like）——**轻量决策模型跑在本地是可行路线**。
- 判据：**压缩优先"删陈旧保留逐字"，摘要只是不得已**；安全审计要机器可读可复核（呼应结果断言层）。
- **提升层**：工具 / 工作流。

### J3：名人顾问团模式 + 论文=新闻发布会（来源：skillsmp #1307 marketing-council + #1315 anti-defensive-writing-en）
- **marketing-council**（coreyhaines31/marketingskills）：**模拟传奇营销人顾问团**（Seth Godin/David Ogilvy/Eugene Schwartz/April Dunford/Rory Sutherland/Alex Hormozi/Byron Sharp）——每个顾问用**自己文档化框架**给意见、**显式展示分歧**、综合出推荐；**执行时交接给对应技能**（positioning/copywriting/ads）——"多专家视角 + 分歧展示 + 交接执行"是顾问团模式三要素。
- **anti-defensive-writing-en**：**论文 = 新闻发布会，不是项目总结/实验日志/自我审计**——识别作品**唯一最可发表的强项**，围绕它构建最有利、完整、有说服力的叙事；**绝不平均呈现一切、绝不主动暴露弱点、绝不写实验日记、绝不替审稿人攻击论文**——与 wb-doc-writing 反防御写作合并保留增量（press conference 比喻 + 唯一最强项叙事）。
- 判据：**多视角咨询的产出必须含"分歧"与"综合"两步**，不能只是并列观点；执行与咨询分离（顾问团只决策，执行交专门技能）。
- **提升层**：可复用 Skill / 工作流。

### J4：低代码迭代语义：默认每 item 执行 + 例外清单 + 批处理防限流 + 分页自建循环（来源：docs.n8n.io/flow-logic/looping/ 全文）
- **默认迭代**：节点自动对每个输入 item 执行一次（"不需要显式建循环"）；**Execute Once 参数**（Settings 里 toggle，只处理第一个 item）。
- **显式循环**：Loop Over Items 节点（Batch Size=1 逐项；**可分组批量处理，用于避免 API rate limit**；Loop Over Items 自动停，无需 IF）。
- **Node exceptions（必须自己设计循环的清单）**：CrateDB/MS SQL/MongoDB/QuestDB（insert/update/delete 类只执行一次）、Code 与 Execute Workflow（Run Once for All Items 模式）、**HTTP Request（分页必须自己循环一页页抓）**、Redis、RSS Read、TimescaleDB。
- 判据：**"默认全量迭代、个别节点只执行一次"的例外必须显式清单化**；分页是最高发的手工循环场景；批量参数是防限流的原生手段。
- **提升层**：工作流 / 工具。

## 判重说明
- J1 → r202-A G1 记 subagents（单会话）；agent teams（多会话可通信 + task list 依赖 + hooks 质量门 + plan approval）为全新独点。
- J2 → wb-context-compressor 已有摘要压缩；"打分删陈旧 + 保留逐字 verbatim"为独有增量；cloudflare 官方安全审计技能为新增生态点。
- J3 → wb-doc-writing 已记反防御写作（r201 系）；press conference 比喻 + 唯一最强项叙事 + 不替审稿人攻击为独有增量，合并保留；marketing-council 顾问团模式全新。
- J4 → 未见 n8n 迭代语义已落地；默认迭代 + 例外清单 + 批处理 + 分页四件全新。
- strategic-compact（skillsmp #1327）与 wb-context-compressor"按任务状态压"重叠>90%，纯重复不落。
