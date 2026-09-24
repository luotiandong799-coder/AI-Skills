# 学习轮 r201-B：Dify知识库API全貌与ClaudeCode记忆双机制与技能弃用声明与30天动量榜单（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/llms.txt | OK 全文 7110 字（完整 API 索引） |
| 2 | docs.n8n.io/scaling/ | 死链 |
| 3 | docs.langflow.org/agent/ | 死链 |
| 4 | make.com/en/help/errors | fetch error |
| 5 | pipedream.com/docs/notifications/ | 死链 |
| 6 | docs.anthropic.com/en/docs/claude-code/memory | OK 全文 5714 字 |
| 7 | skills.sh/search?q=context | robots 禁（走搜索替代） |
| 8 | skillsmp.com/skills/page/10 | OK（#901-942） |
| 9 | deepseek-plugin.org/faq | 死链 |
| 10 | GitHub 生态（AI agent Top100 榜单搜索） | OK |

## 独点（4 个）
### E1：Dify 知识库 API 全貌：父子块层次分块 + 知识管线 + 人工输入暂停恢复（来源：docs.dify.ai/llms.txt 全文）
- **父子块分块**：`hierarchical_model` 分块模式下 chunk 有 parent/child 层级——Create/List/Delete/Update Child Chunk 独立 API；chunk 可带 keywords 和 answer 字段（QA 模式文档）。
- **索引状态机 + 异步轮询**：文档创建返回 batch ID → Get Document Indexing Status 轮询，状态机 `waiting → parsing → cleaning → splitting → indexing → completed/error`；下载文档签名 URL；批量 ZIP 下载上限 100 文档；批量启停/归档。
- **知识管线 Datasource Nodes**：List/Run Datasource Node + **Run Pipeline（streaming + blocking 双模式）** + Upload Pipeline File——知识处理本身流水线化可编程。
- **Human Input 暂停恢复**：工作流暂停等人工输入，Get Human Input Form（form_token）→ Submit 后工作流恢复（WebApp delivery）——"流程等人再继续"是异步表单端点化。
- **Stream Workflow Events 可续流**：SSE 断线/暂停后可 resume，已完成的 run 重发单条 workflow_finished 后关闭——流式事件可恢复消费。
- **插件体系**：Tool/Model Provider/Trigger/Data Source/Bundle（Marketplace/GitHub/Package 三型聚合多插件）/ 自定义模型（Xinference 示例）；**Reverse Invocation**：插件反向调用主平台 App/Model/Tool/Node 四类服务（含 LLM/Summary/TextEmbedding/Rerank/TTS/Speech2Text/Moderation 模型）。
- 判据：**知识库工程是"分块模型 × 异步状态机 × 可编程管线 × 人工在环"四件套**；流式事件要设计断线续流。
- **提升层**：工具 / 工作流。

### E2：Claude Code 记忆双机制 + rules 作用域 + 导入链（来源：docs.anthropic.com/en/docs/claude-code/memory 全文）
- **双机制对比**：CLAUDE.md（你写/指令规则/project-user-org scope/每次加载）+ **auto memory（Claude 自己写/学习到的模式/per working tree/加载每次会话前 200 行或 25KB）**——两类记忆定位不同，auto memory 记"发现"不记"规定"。
- **@import 导入链**：`@path/to/import` 展开进上下文，相对路径基于包含文件而非工作目录，**递归上限 5 层**；首次遇到外部导入显示批准对话框，拒绝后不再出现；个人偏好可 @~/.claude/... 指向本机文件（共享 CLAUDE.md 但内容留在本机）。
- **HTML 注释剥离**：`<!-- maintainer notes -->` 注入上下文前剥离——**人看的注释不花 agent token**（代码块内注释保留）。
- **rules 作用域**：.claude/rules/*.md 按 `paths` frontmatter（glob）只在与匹配文件工作时加载进上下文——省空间；symlink 跨项目共享规则（循环 symlink 自动处理）；user rules 先加载、项目规则优先级更高。
- **AGENTS.md 桥**：Claude 读 CLAUDE.md 不读 AGENTS.md——用 `@AGENTS.md` 导入实现同源不重复，可再追加 Claude 专属段。
- **/init 多阶段**：CLAUDE_CODE_NEW_INIT=true 时 /init 走交互式多阶段流程（选 CLAUDE.md/skills/hooks 三产物 → subagent 探索 → 补问 → 可审阅提案再写文件）；已有 CLAUDE.md 只建议改进不覆盖。
- **managed 分工**：settings 管强制（permissions.deny/sandbox/forceLoginMethod/env 等，客户端执行不受 Claude 决定影响），managed CLAUDE.md 管行为指导（code style/data handling）——**"settings 是硬执行层、CLAUDE.md 是行为塑造层"**；managed CLAUDE.md 个体不可排除。
- 判据：**记忆分"规定型（人写）与发现型（agent 自记）"两轨**；指令文件要短（<200 行）、具体可验证、规则可路径作用域加载；人力注释与 agent 上下文分离。
- **提升层**：工具 / 可复用 Skill。

### E3：技能弃用声明双模式 + 防风格漂移 + 近 30 天研究（来源：skillsmp #924/#931/#941/#934 + anthropics/knowledge-work-plugins）
- **弃用声明两模式**：continuous-learning v1 描述即标 `[OBSOLETO - usar continuous-learning-v2]`——**superset 弃用**（v2 是 v1 严格超集：instinct-based + project scope + reliable hooks，明确"不要调用 v1"）；chatgpt-app-builder 标 DEPRECATED → 描述里给出替代技能名 + 安装命令（mcp-app-builder）——**重定向弃用**（指向替代并给安装路径）。**弃用信息写进技能描述本身，搜索就能看到，不留死技能**。
- **inherit-legacy-style**：AI 上手手写旧项目时防 **style drift**（模型把预训练主流习语强加给项目）——只对齐 meta-architecture 不对齐语法，跑一次后成为后续所有编码行为约束——**"学旧项目的房规"**。
- **last30days（62,570★）**：研究最近 30 天人们实际怎么说某话题——Reddit/X/YouTube/TikTok/HN/Polymarket/GitHub 全源 + **doctor health check 诊断损坏/缺失的来源**——"近 30 天舆情研究技能化"。
- **smb-onboard（anthropics/knowledge-work-plugins）**：Claude 当 trainer 上岗工作流——连前两个工具 → 跑一个 recipe 证明即时价值 → 访谈业务（industry/size/top 3 headaches）→ **把上下文持久存储让所有其他技能受益** → 每周 check-in 节奏。
- 判据：**技能升级要么 superset 要么重定向，弃用声明写进描述**；agent 接旧项目先对齐项目房规再动手；研究"近期舆论"与"经典知识"是两套技能。
- **提升层**：可复用 Skill / 工作流。

### E4：Agent 榜单生态：30 天滚动动量 + 10-Eval 复合分（来源：theagenticleaderboard.com + Artificial Analysis + agenticindex 搜索）
- **The Agentic Leaderboard**：**30 天滚动窗口**，只排最近 30 天发布的开源 AI agents，按 **momentum score**（势头分）排序，每周一更新——"新项目按上升势头而非绝对规模排名"，给了新仓库被看见的通道。
- **Artificial Analysis Intelligence Index**：**10-Eval LLM 质量复合分**（Claude Opus 5=53 / GPT-6 Astra=53 / Muse Spark 1.3=53 / Claude Fable 5.1=54）；模型价格并排（GPT-6 Astra $1.41 in/out 等）——多基准合成单一质量分。
- **standardcompute**：Google Antigravity（agentic IDE，84/100：agent manager 计划/编码/验证）、OpenAI Codex CLI（sandboxed local execution + approval modes）；**agenticindex.io：949 production-ready 供应商已验证**。
- 判据：**榜单设计决定谁被看见**——30 天滚动 + 势头分给新项目公平通道；质量评测用多基准复合分而非单一基准；"已验证供应商"目录以覆盖度打分。
- **提升层**：生态观察。

## 判重说明
- E1 → r200-A 已记 Dify 平台定位/BaaS+LLMOps；llms.txt 首次拉全，父子块分块 + 知识管线 + Human Input 暂停恢复 + SSE 续流 + Plugin Bundle + Reverse Invocation 为独有增量。
- E2 → r200-C 已记 settings 四级 scope；memory 页首次拉全，CLAUDE.md vs auto memory 双轨 + @import 5 层 + HTML 注释剥离 + rules paths 作用域 + symlink + managed 分工为独有增量。
- E3 → r199-C 已记 de-aigc/continuous-learning-v2；弃用声明双模式 + inherit-legacy-style 防风格漂移 + last30days + smb-onboard 为独有增量。
- E4 → r201-A D4 已记 openagentskill 六信号；theagenticleaderboard 30 天动量 + 10-Eval 复合分 + agenticindex 949 为独有增量。
