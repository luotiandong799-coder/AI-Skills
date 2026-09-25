# 学习轮 r212-A：Anthropic Agent Skills官方overview与skillsmp p44与国内三平台生态与ModelScope trending（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/44（#4301-4348） | OK（deep-learning-book delta 层/paper-search-pro 7 源） |
| 2 | dify.ai/blog 续读（20987-26578） | OK（POC→Production 五阶段/Shadow AI 治理） |
| 3 | docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview（5000/6399） | OK（官方三级加载+字段约束） |
| 4 | general_search 腾讯 SkillHub | OK（本土镜像/TRACE/Top50/76 万+ skills） |
| 5 | general_search 阿里虾小宝 | OK（3.5 万+ skills/三维认证/JVS Claw） |
| 6 | general_search 智谱 AgentMore | OK（5-Agent 群聊/零 Token 安装） |
| 7 | deeplearning.ai/short-courses（4690/119836 取） | OK（课程目录，低方法） |
| 8 | docs.pipedream.com（813B 全） | OK（Connect SDK 3000+ API，平台事实） |
| 9 | github.com/trending?since=daily | OK（仅首条 ai-engineering-from-scratch ★57,042，与 r211-B 重复记录不重落） |
| 10 | modelscope.cn/models（2817B 全） | OK（258,852 模型总量+新模型发布） |

## 独点（4 个）
### A1：Anthropic Agent Skills 官方 overview：三级加载 token 成本表 + 字段硬约束（来源：docs.anthropic.com agent-skills/overview，2026-09-25 实拉；与 r211-C agentskills.io 官方同源，Claude 官方页独有增量 ≥40% 落）
- **三级加载 + token 成本**：**L1 Metadata 启动常载 ~100 tokens/skill**（YAML frontmatter name+description 进 system prompt）；**L2 Instructions 触发时载 <5k tokens**（SKILL.md 主体 bash 读入）；**L3+ Resources 按需载、effectively unlimited**（bundled 文件 bash 执行**只收输出，脚本代码永不进 context**；reference 文件按需读）——**"可以装很多 skill 而 context 占用小"有了官方数字（~100 tokens/个）**。
- **name/description 字段硬约束**：name ≤64 字符、仅小写字母数字连字符、禁 XML 标签、**禁保留词 "anthropic"/"claude"**；description ≤1024 字符、非空、禁 XML。
- **API 三 beta headers**：`code-execution-2025-08-25` + `skills-2025-10-02` + `files-api-2025-04-14`；Custom Skills 经 `/v1/skills` 上传、**workspace 共享**；claude.ai Custom Skills **仅个人（不可 org 共享、不可中央管理）**。
- **安全**：只从可信来源（自创或 Anthropic）用 skill——**恶意 skill 可指示 Claude 调用工具/执行代码偏离声称目的**（与 r210 工具描述注入同向，官方级确认）。
- **提升层**：可复用 Skill（官方规格，加载成本数字）。

### A2：国内三平台生态：SkillHub / 虾小宝 / AgentMore（来源：general_search 多源，2026-09-25 实拉）
- **腾讯 SkillHub（skillhub.cloud.tencent.com）**：OpenClaw 官方技能生态 ClawHub 的**本土化高速镜像平台**（Lighthouse 团队）——Skills 规模 1.3 万→8 万→**76 万+、3000 万+ 下载量**（数据递增）；发布三种方式（网页可视化/CLI 一键推送/Agent 自动化部署，版本可追溯回滚）；**实名认证+安全内容审核+三线并行安全审核**；首发 **TRACE 评测体系**识别高质量 Skill；**Top50 精选榜单**；支持 WorkBuddy/QClaw/ima。
- **阿里虾小宝（ai.skillatlas.cn）**：专为中国用户优化的 AI Agent Skills 安全社区——**35,000+ 安全审核技能**；**安全性/完整性/可执行性三维认证体系**逐技能审核按等级打标；内置 JVS Claw Agent 助手（挑选一键同步到工具）；市场不收费、调用消耗算力；另有 1688 电商 Skills（1000+ 官方认证）。
- **智谱 AgentMore（agentmore.chatglm.cn）**：多 Agent 云端协作平台——**一句话招募最多 5 个 AI Agent 组成群聊团队**（"职业+性格+背景+场景"定义角色）；"头脑风暴"与"任务分配"双发言模式；7×24 云端待命；**Skills 广场整合官方严选/Skill Hub/开源社区三模块、一键零 Token 安装**；智能体广场模板一键复制到账户。
- **提升层**：可复用 Skill（生态索引/判重参考）。

### A3：skillsmp p44 精选：教材 delta 层 / 7 源中文文献检索 / MCP 强制前置（来源：skillsmp.com/skills/page/44，2026-09-25 实拉）
- **deep-learning-book（alirezarezvani/claude-skills ★26,225）**：Goodfellow 深度学习教材学习伴侣——索引 20 章 + **2016→2026 delta 层**（书里哪些被取代（transformers/AdamW/diffusion/double descent）、哪些仍成立）+ 四个确定性工具（prerequisite-aware 阅读路径规划/training-failure 诊断/capacity 规划/参数-FLOP-内存计算器）——**"经典知识 + 时间 delta 层"是教材类 skill 的范式**。
- **paper-search-pro（O0000-code ★170）**：最多 7 源学术检索（OpenAlex/Semantic Scholar/CrossRef/PubMed/arXiv + **NSSD 国家哲社文献中心 + yiigle 中华医学期刊 中文原生**）；可调深度（Quick scan 5min→Audit prep 3hr）；输出 Shadcn HTML + BibTeX/RIS/CSV + **PRISMA-S log**；按中科院分区/Q1/JCR 筛——**中文原生文献检索独有增量**。
- **mcp-apps-builder（Shubhamsaboo/awesome-llm-apps ★139,204）**：MCP server 开发强制前置——架构决策/安全模式/常见坑；**改 server.tool()/resource()/prompt() 前必读**。
- **bank-flow-reconciliation（nigo81 ★129）**：银行流水合并+序时账双向核对（**9 层递进匹配引擎**）；**claude-hud（★131）**：AI coding agent HUD 仪表盘（context 用量/活跃工具/运行 sub-agents/任务进度实时显示）。
- **提升层**：可复用 Skill / 工作流。

### A4：ModelScope 生态事实：258,852 模型总量 + 2026-09 新模型发布（来源：modelscope.cn/models，2026-09-25 实拉）
- **ModelScope 模型总量 258,852**（vs HF 3,082,055）。
- **新模型发布**：DeepSeek-V4.1-Flash（484.62B Image-Text-to-Text，09-10）、**DeepSeek-V4-Pro-0813（1,650.50B 1.65T，08-14）**、GLM-5.3（ZhipuAI 753.33B，09-04）+ GLM-5.3-Flash（321.32B）、**Kimi-K3（2,779.93B 2.8T MoE，09-02）**、Shanghai_AI_Laboratory/Atria-Dawn-Preview（753.33B，arxiv:2609.15818，09-16）、Intern-S2-397B、Qwen-Image-2.1（16.22B T2I，09-21）、Qwen3.8-27B（27.78B，★522.4k downloads）、MiMo-V2.6 系列（Pro-RL/Distill/Flash-RL）、MiniCPM5-2B、TeleOCR（1.42B 文档解析）、Tencent-Hunyuan AuK（1.69B TTS）。
- **提升层**：工具（模型选型生态事实）。

## 判重说明
- A1 → Claude 官方页（三级加载 token 成本表 L1~100tokens/L2<5k/L3 无限 + name/description 硬约束 + 三 beta headers），与 agentskills.io 同源但官方独有增量 ≥40%，落。
- A2 → 国内三平台（SkillHub 76 万+/虾小宝三维认证/AgentMore 5-Agent 群聊），全新，落。
- A3 → skillsmp p44 精选（deep-learning-book delta 层/paper-search-pro 中文原生/mcp-apps-builder 前置），全新，落。
- A4 → ModelScope trending（258,852 总量 + DeepSeek-V4-Pro 1.65T + Kimi-K3 2.8T + GLM-5.3 753B），全新生态事实，落。
- 未落：dify blog 续读（POC→Production 五阶段/Shadow AI 治理——企业级偏重，背景记录）、GitHub trending 首条（与 r211-B 重复）、deeplearning.ai 课程目录（低方法）、Pipedream 平台事实（记录不落）。
