# r291C 学习轮（2026-09-29，十站实拉→十独点）

判重基线同 r291A/B（r284~r291B 全表 + SKILL.md 1,960,958B）。查询词与既往全表错开。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | Human Input 人工审核节点：流程执行到节点暂停→表单发指定人→审阅/填字段/点决策按钮→沿对应分支继续 / 三输出变量（__action_id=yes/no、__action_value=是/否、__rendered_content=表单内容）/ Workflow vs Chatflow 终节点契约（Output 可选 vs Answer 必须，应用类型选后不可改）/ 人机协作判据（置信度低于阈值暂停→人工确认再回复） | 新面 | 工作流 |
| 2 | n8n | LangChain 并入原生 AI 套件：不再有单一 LangChain node，功能拆到 AI 分类（AI Agent 主节点）/ AI Agent 节点=可视化 AgentExecutor（Chat Model/Memory/Tool/Output Parser 子节点+8 种 AI 连接类型=依赖注入端口）/ langchain code 节点可自定义 LLM（callbacks 接 Langfuse 追踪） | 合并保留增量 | 工具 |
| 3 | LangFlow | Prompt 模板组件：结构化输入（自然语言+固定值+动态变量）与聊天消息/文件上传分离 / 模板加变量自动生成字段（可连其他组件自动化 prompting）/ trace_type="prompt" 提示追踪 | 合并保留增量 | 工具 |
| 4 | Activepieces | 版本控制：Project Releases 三来源（Git 拉取/Project 复制/Rollback 恢复）/ Git 连接需 Environments 功能 / Flow versioning（publish/draft 状态+回滚）/ Custom Pieces CI/CD（生产=自建 npm registry：package.json 升版→PR 合主→CLI 或 GitHub/GitLab Action 同步）/ Project Replace CLI（两部署需同 major 版本） | 新面 | 工具 |
| 5 | Make | AI Toolkit 八大文本模块（sentiment/categorize/language/extract/standardize/summarize/translate/chunk）/ AI provider 双通道（Make AI provider 所有计划可用 vs 自定义 provider 连接付费）/ Claude Opus 5（extended thinking 默认开 low/medium/high 三档）/ MCP Client Execute an action with AI（Make credits 或 BYOK） | 合并保留增量 | 工具 |
| 6 | Pipedream | AI 面：OpenAI app 预建 LLM actions（managed connection 计 AI token allowance：免费 100 万/advanced 5000 万，不走个人 key）/ workflow 步骤可任意 Node/Python（add Claude = npm install SDK）/ 并行/非依赖 LLM 调用 / 模型中立（MCP 服务任意模型，客户自带 key） | 新面 | 工具 |
| 7 | Anthropic | 提示工程：示例三要求（Relevant 贴近实际/Diverse 覆盖边界/Structured XML 包裹）/ XML 标签=最强分段信号（Claude 训练视为语义边界）/ "Be concise 是愿望，5 bullets each under 15 words 是规格"——指令被忽略改精确不改长 / 数据与指令分离+防幻觉组合（不知道就说不知道+只依据材料作答） | 合并保留增量 | 可复用 Skill |
| 8 | Copilot | agent mode 2026：cloud agent reasoning level 可调（高=更好但更耗 token/credits）/ auto model selection 按请求复杂度自动选模型（2026-06-17 GA 优化 token）/ cloud agent 脱离 PR 工作流（分支上干活不开 PR）/ canvases 双向工作表面（agent 更新画布+人可编辑/重排/批准/重定向=AX 开端）/ BYOK（Business/Enterprise 链自己的 API key，本地 Ollama） | 新面 | 工具 |
| 9 | OpenClaw | multi-agent：三拓扑选型（Manager+Specialists 复杂多域/Pipeline 顺序交接/Parallel Pool 同质高量）/ agent 完全隔离 persona（独立 workspace 四文件 AGENTS.md/SOUL.md/MEMORY.md/TOOLS.md + per-channel accountId）/ sessions_spawn 工具（父 agent 派生隔离子 agent：任务/模型/权限）/ Triage Agent 拆任务→专家并行→汇总 / openclaw agents add 绑独立渠道 | 合并保留增量 | 可复用 Skill |
| 10 | WaytoAGI | 学习路径：Claude Agent Skills 蓝皮书（五篇二十章：Skill 是给普通人最好的礼物→Agent Team→自动进化）/ AI 编程共学九实操项目（图片字幕生成器/金句卡片/AI 博客/中文名生成器/表情包生成器/Life Coach/浏览器智能插件/个人网页/推荐网站）/ 晚8点共学直播回放库 | 新面 | 可复用 Skill |

判重口径：增量判定。本轮 5 新面 + 5 合并保留增量，零纯重复。