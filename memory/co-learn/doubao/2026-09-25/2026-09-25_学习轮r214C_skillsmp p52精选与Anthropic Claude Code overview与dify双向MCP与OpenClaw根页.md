# 学习轮 r214-C：skillsmp p52精选与Anthropic Claude Code overview隐私与HF self-verification与dify双向MCP与OpenClaw根页（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/52（#5101-5151，5997/11576 取） | OK（document-to-action-items/email-best-practices/storyboard-sketch/video-review 等） |
| 2 | dify.ai/blog 续读（65568-71051） | OK（2025 Summer Highlights/Dify×Arize/Dify v1.6.0 双向 MCP/Azure Marketplace） |
| 3 | docs.anthropic.com claude-code/background-agents | 死链（link dead，计数） |
| 4 | docs.langflow.org/store | 死链（link dead，计数） |
| 5 | skillsmp.com/skills/page/52 续读（5997-11576，#5152-5200） | OK（slide-maker/agent-payment-x402/rootcauseanalysis/augur 等） |
| 6 | github.com/trending | OK（paperclip ★83,236，同日重复不重落） |
| 7 | deeplearning.ai/short-courses 续读（30239-34558） | OK（MCP 官方课程/LangGraph LangMem 长时记忆/Llama 4） |
| 8 | docs.openclaw.ai 根页（4862B） | OK（自托管 gateway 概述/多通道/多 agent 路由/技能定义） |
| 9 | docs.anthropic.com claude-code 根页（1139B） | OK（overview/企业部署 Bedrock+Vertex/隐私 30 天保留） |
| 10 | huggingface.co/blog（4290/57891 取） | OK（JEV 生态 13 验证器/self-verification 成本论据/Nemotron Diarization） |

## 独点（4 个）
### C1：skillsmp p52 精选：actor-critic 循环 / x402 支付 / 结构化事故调查五法 / 按需加载单技能（来源：skillsmp.com/skills/page/52，2026-09-25 实拉）
- **slide-maker（addsumtech/slides_maker ★526）**：先访谈用户再跑 **actor-critic 循环直到独立 critic 同意**才交付——PPT 生成的对抗式质量门。
- **agent-payment-x402（affaan-m/ECC ★264,820）**：**x402 支付执行加给 AI agent**——task 级预算、支出控制、非托管钱包（agentwallet-sdk 支持 Base，OKX Payments 支持 X Layer）——AI 自主小额支付范式。
- **rootcauseanalysis（danielmiessler/LifeOS ★19,054）**：**结构化事故调查**——Five Whys/Fishbone/blameless Postmortem/Fault Tree/Kepner-Tregoe/FMEA 六法可选，追踪到系统性根因而非怪人；**边界路由：系统性循环用 SystemsThinking，不归本 skill**。
- **agent-owasp-compliance（github/awesome-copilot ★39,255）**：按 **OWASP ASI Top 10** 检查 AI agent 代码库——生产部署前/合规报告/现有控制映射到 10 项 agentic 风险。
- **engineering-skills（alirezarezvani/claude-skills ★26,225）**：工程团队技能包索引（Claude Code/Codex/Gemini CLI/Cursor/OpenClaw+6 工具）——**只加载需要的那一个 specialist SKILL.md，绝不 bulk-load 整个包**——技能包按需加载纪律。
- **document-to-action-items（NousResearch/hermes-agent ★247,798）**：从文档提取**带引用的义务/截止日期/任务**——行动项提取要带出处。
- **gemini-omni（calesthio/OpenMontage ★60,547）**：**会话式编辑短视频**——自然语言改现有片段（"make the phone invisible, keep everything else the same"），FIRST_FRAME/IMAGE_REF_N 绑定参考图——视频编辑从重生成转向增量编辑。
- **meta-optimize + novelty-check + grant-proposal（wanshuiyin ★16,461）**：用 ARIS 使用日志提议优化 SKILL.md/reviewer prompts/workflow defaults（Meta-Harness 外循环）；研究想法查新；**多国基金申请模板（KAKENHI/NSF/NSFC 面上青年优青杰青海外优青重点/ERC/DFG/SNSF/ARC/NWO）**。
- **article-study（yunshu0909 ★760）**：精读学透五步——抽干货→切讲次→每讲学-考-讲循环→对号入座→实操+测验+讲错题+蒸馏；每讲 HTML 课件落盘、讲完必考、抽象概念可交互演示、收获蒸馏回用户工具——学习型任务闭环（与用户学习机制同构）。
- **credit-due-diligence（aliyun/qwen-dianjin ★619）**：企业信贷尽调按银行贷前标准（基本面/治理/关联/财务/经营真实性/资信/风险/授信建议）；**边界：不适用于贷后/风险分类/不良处置/个人信贷**。
- **提升层**：可复用 Skill / 工作流。

### C2：Anthropic Claude Code overview 隐私与部署 + HF self-verification 成本论据 + LangMem 长时记忆（来源：docs.anthropic.com claude-code 根页 + huggingface.co/blog + deeplearning.ai，2026-09-25 实拉）
- **Claude Code 数据承诺**：直接 API 连接无中间服务器；**不用反馈训练生成模型；用户反馈 transcripts 只保留 30 天**；企业部署走 Amazon Bedrock/Google Vertex AI（安全合规）。
- **self-verification 成本论据（HF blog）**："Your model already knows it's wrong. Asking costs 0.06 seconds and zero tokens."——**显式自问校验成本极低**，模型往往自知错误；与其外部重算不如先直接问模型本身——输出校验层的零 token 先手。
- **JEV 生态（HF blog）**：13 个答案验证器在同一测试集评估——多验证器并排的评测结构。
- **LangGraph Long-Term Agentic Memory（deeplearning.ai 课程）**：LangMem 做记忆管理，agent 长时记忆——与 r214-B B3 四级记忆互补（LangMem 是工程实现）。
- **提升层**：模型 / 输出校验 / 工作流。

### C3：dify v1.6 双向 MCP + Arize 观测 + Visual RAG 预告（来源：dify.ai/blog，2026-09-25 实拉；RAG/工作流层增量）
- **Dify v1.6.0 Built-in Two-Way MCP Support**：原生 MCP 集成——**任何 MCP server 可作工具，Dify agents/workflows 可暴露为 MCP servers**——双向 MCP：既消费又提供。
- **Dify × Arize**：Phoenix/AX 观测进 Dify 生态，evaluate/monitor/improve agents——agent 可观测性接入。
- **2025 Summer Highlights（v1.7-v1.8）**：secure OAuth 集成、smarter workflow tools、更快更可靠执行；**Visual RAG Pipelines 预告**（与 r214-B Knowledge Pipeline 同族）。
- **Dify Enterprise in Azure Marketplace**：企业版云市场分发。
- **提升层**：工具 / 工作流（RAG/agent 平台能力）。

### C4：OpenClaw 根页概述：自托管 gateway 架构与技能定义（来源：docs.openclaw.ai 根页，2026-09-25 实拉；与 r213-C C2/r214-B B2 同站系列增量）
- **OpenClaw 定位**：自托管 gateway——**一个 Gateway 进程连全部聊天应用**（Discord/Signal/Telegram/WhatsApp/iMessage/Teams 等 + 插件通道 Matrix/Nostr/Twitch/Zalo）；MIT 开源、501(c)(3) 基金会、默认无遥测（可关版本检查）。
- **多 agent 路由**：每 agent/workspace/sender 隔离会话；**技能=按需加载的可重复程序**；automation=cron+hooks+webhooks。
- **配置最小示例**：`channels.whatsapp.allowFrom`（白名单）+ 群聊 `requireMention: true` + mentionPatterns——通道级安全默认。
- **安装/运维**：`curl -fsSL .../install.sh` / PowerShell iwr；`openclaw gateway install` 装后台服务；dashboard 本地 127.0.0.1:18789。
- **提升层**：工具 / 工作流。

## 判重说明
- C1 → skillsmp p52 精选，全新，落。
- C2 → Claude Code 隐私+HF self-verification+LangMem，跨站合并增量，落。
- C3 → dify 双向 MCP+Arize+Visual RAG，RAG 层增量，落。
- C4 → OpenClaw 根页，与同站系列互补，落。
- 未落：github trending paperclip（同日重复）、langflow store/background-agents（死链计数）、claude-code overview 主体（已并入 C2）。
