# 学习轮 r572A（2026-10-15 · AI 技能库工程与方法论 + AI 智慧进化）

十站实拉（全量逐站，独立判重）：Dify / n8n / Langflow / Activepieces / Make / Pipedream / Anthropic Skills / skills.sh / GitHub 生态 / deeplearning.ai。判重基准：r571A/B/C 9 章 + r570 批 + r569 批 + WB 留痕（评估驱动开发）。

## 落地（execute 3.83.0 → 3.84.0，+3 章）

1. **mods：TypeScript 函数级改造——重写 prompt、门控工具调用、非沙箱运行**（来源：Machine Herald《Anthropic Adds Mods to Claude Code》2026-10-03）
   - mods=改变 coding agent 行为与外观的 TS 函数；从 claude 目录或 /plugin 加载
   - 可重写 prompts、门控工具调用、以非沙箱方式运行（per-mod 声明，不是全局开关）
   - **提升层**：工具

2. **外部 agent 经 MCP 参与团队任务：委派 + 写入授权可关 + 运行恢复**（来源：Paperclip 2026-10-13 + CrewAI 评估命令 2026-10-13）
   - 外部智能体经 MCP 参与团队任务：查看/委派任务、授权写入可关闭、改进运行恢复
   - CrewAI 评估命令按每次运行统计成本/耗时 + 记录提前停止原因
   - **提升层**：工作流

3. **执行三层分流：白名单即时 / 沙箱兜底 / 分类器判决**（来源：Cursor《自动审查运行模式》2026-06-05）
   - 允许列表即时执行、可沙箱的在沙箱执行、其余交分类器子智能体判决
   - 减少审批提示持续工作更久 + 可审计判决
   - **提升层**：工具

## 落地（compressor 3.680.0 → 3.681.0，+3 章）

1. **Agentic RAG 六步循环：意图分析→选源→重写→评估证据→重试→回退**（来源：Dify blog 2026-09-17）
   - 与一次性 retrieve-then-generate 不同：迭代分析意图、选择工具与来源、重写查询、评估证据、重试或回退
   - 提升 grounding 与可靠性，但延迟/成本/复杂度都涨——权衡显性
   - **提升层**：工作流 / 工具

2. **skill pack 批量打包分发 + 技能 frontmatter 六 key 白名单（version 非标准）**（来源：Vercel 2026-08-07 + Hivebook 2026-10-14）
   - pack=多技能打包 unlisted 自有 URL，npx skills add https://skills.sh/p/<pack> 一条命令整包安装
   - Agent Skills spec 只允许六个 frontmatter key；version 不在其中（上传 claude.ai 触发 unexpected-key rejection）
   - **提升层**：可复用 Skill

3. **Vercel Connect 短效 scoped token（不存长期密钥）+ 记忆写入双机制（hot path vs background）**（来源：Vercel 2026-06-17 + DeepLearning.AI 2026-09-20）
   - 每 agent 各自 scoped token 与 triggers 到达服务，不存长期 provider secret
   - 三种记忆配两种写入机制：hot path 即时写 / background 后台写
   - **提升层**：工具 / 可复用 Skill

## 十站实拉要点（逐站留痕）

- **Dify**：Build agents by chatting（已落 r571A）；Agentic RAG 六步循环（本轮落）；Workflow=Harness；Creator Center 模板市场；Human Input node（已落 r571C）；plugin-first 多 runtime shapes
- **n8n**：Agents 两层共存（已落 r571A）；v2.40-2.43（guardrails 强化）；AI Agent Tool node 主 agent 监督委派（已落 r571C 同源）；70 MCP 一键连接；Microsoft Agent 365 Trigger（企业级不投）
- **Langflow**：1.11 Human-in-the-Loop/A2A/AG-UI（已落 r571C 观察）；1.9 Assistant/DevOps Toolkit/MCP IDE；Scaling 记忆稳定（已落 r571A）；LangChain 相邻：Engine v2 red teaming、Trajectories 会话视图、Deep Agents 0.6 DeltaChannel 增量 checkpoint
- **Activepieces**：AgentX MCP 单连接 760+ app（本轮观察）；Paperclip 外部 agent MCP 参与（本轮落）；CrewAI 评估成本/耗时统计（本轮落）
- **Make**：AI Agents app 改进；MCP audit log 工具；monday Context ID 对话记忆（已落 r571C 同源）；Claude Opus 4.6
- **Pipedream**：OAuth MCP+ChatGPT（已落 r571C）；MCP Python SDK v2 无握手无会话；pre.dev 本地驱动已开 Chrome 复用登录；Pi 1.0.4 MCP 工具 radius 过滤+输出 home 只读
- **Anthropic**：Claude 5.5 新规则 500 行/引用单层（已落 r569B）；Progressive Disclosure（已落）；mods TS 函数（本轮落）；frontmatter 六 key/version 非标准（本轮落）；script 执行零 token（已落）
- **skills.sh**：skill packs 批量打包（本轮落）；7 个月 100 万技能 2.8 亿安装；skills.sh API OIDC；v1.5.25 fx/Sarvam 支持；Vercel Connect scoped token（本轮落）
- **GitHub 生态**：DeepSeek Harness 万物皆插件 248.7k★；hermes-agent 253.3k★；AIHOT 自找热点自写日报框架（信源+标准可配置）；graphify 124.5k★；OpenClaw 排名 #1
- **deeplearning.ai**：Long-Term Agentic Memory（semantic/episodic/procedural + hot path/background 写入双机制，本轮落）；Agent Memory Oracle 一等基础设施；Agentic AI 9h55m（degrees of autonomy 自主度分级观察）；Reflection 模式（已落 r571A）

## 功能套件核查（⑦）

三核心套件本批无优化项；wb-ponytail/wb-max-token-saver 替代仍未获授权未更新；AIHOT（信源+标准参数化热点框架）与学习流程同构，列为后续借鉴观察对象。

## 垃圾清理（⑨）

删了什么：本批实拉走 general_search 无本地临时文件落盘，未产生新垃圾。保留什么：*.bak 与全部核心产物（两 SKILL 文件 + 本留痕）；历史探针垃圾（probe565/565b/567、probe564/564c、probe、probe566/566b、probe567）待删除通道可用时清理。
