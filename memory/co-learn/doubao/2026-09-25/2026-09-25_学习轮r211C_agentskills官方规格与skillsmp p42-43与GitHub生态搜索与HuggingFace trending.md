# 学习轮 r211-C：agentskills官方规格与skillsmp p42-43与GitHub生态搜索与Hugging Face trending（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/42（#4101-4148） | OK（threat-model-analyst/strategic-compact） |
| 2 | dify.ai/blog 续读（15490-20987） | OK（MongoDB RAG 原生/IT Leaders 指南） |
| 3 | docs.anthropic.com/claude-code/batching | **link dead**（记死链） |
| 4 | docs.n8n.io/workflows/（根页 121B） | OK（workflow 定义，低方法） |
| 5 | skillsmp.com/skills/page/43（#4201-4250） | OK（content-strategy/investor-news-impact/skill-creator） |
| 6 | docs.openclaw.ai/guides/automation | **link dead**（记死链，OpenClaw 多子页持续不可达） |
| 7 | agentskills.io 官方（4789/96448 取） | OK（progressive disclosure 三阶段） |
| 8 | general_search GitHub agent 生态 | OK（VoltAgent 1500+ skills/google/skills） |
| 9 | waytoagi.com/ai | **link dead**（记死链） |
| 10 | huggingface.co/models?sort=trending（4199/29397 取） | OK（Qwen-Image-2.1/Ternary-Bonsai gguf） |

## 独点（4 个）
### C1：agentskills.io 官方规格：progressive disclosure 三阶段 + SKILL.md 最小结构（来源：agentskills.io 官方 4789B，2026-09-25 实拉；与 wb-skill-authoring 触发/激活邻域官方增量）
- **Progressive disclosure 三阶段官方定义**：①**Discovery**——启动时只加载每个可用 skill 的 name+description，"just enough to know when it might be relevant"；②**Activation**——任务匹配描述→读完整 SKILL.md 进 context；③**Execution**——按指令执行、按需运行打包脚本/加载引用文件。**全量指令只在任务需要时加载 → agent 可装很多 skills 而 context 占用很小**。
- **SKILL.md 最小结构**：文件夹含 SKILL.md（metadata `name`+`description` 至少）+ 可选 scripts/references/assets/任意附加文件——轻量开放格式，可版本控制、跨产品复用。
- **skills 解决的痛点**：agent 越来越强但常缺"可靠完成真实工作的上下文"——skills 把 procedural knowledge + 公司/团队/用户特定上下文打包成便携、版本控制的文件夹按需加载。
- **提升层**：可复用 Skill（官方规格，触发/激活机制依据）。

### C2：skillsmp p42-43 精选：增量威胁建模 / 逻辑间隔手动压缩 / 战略内容简报（来源：skillsmp.com/skills/page/42-43，2026-09-25 实拉）
- **threat-model-analyst（github/awesome-copilot ★39,255）**：STRIDE-A 威胁模型分析两种模式——①单次分析（架构概览/DFD 图/STRIDE-A 分析/优先级发现/管理层评估）；②**增量分析**：以旧威胁报告为基线、对比最新 commit→产出 change tracking（new/resolved/still-present 威胁）+ STRIDE heatmap + findings diff + 内嵌 HTML 对比——**威胁模型可以像代码一样 diff**。
- **strategic-compact（affaan-m/ECC ★264,820，韩语）**：**任意自动压缩→在逻辑间隔手动上下文压缩**——在任务步骤间主动保存上下文，而非任模型自动压缩随机丢弃。与 wb-context-compressor"预算式管理"同方向。
- **content-strategy（anthropics/knowledge-work-plugins ★25,304）**：分析 PayPal/QuickBooks 销售数据→top performers/slow movers+季节性分层→**30 天内容简报**（推什么/做什么 offer/hold 什么）；**战略输出只出简报，不做日历/资产**——边界克制。
- **investor-news-impact（digoal/blog ★8,578）**：近 3 天新闻抓取+影响分析——8 个默认主题（中美关系/地缘/美联储/民生/高科技/生物医疗/云计算/AI 产业链）并发抓取、按分类总结、推演对行业和上市公司影响、图文并茂输出 markdown。
- **skill-creator（XiaomiMiMo/MiMo-Code ★13,225）**：创建/审查/改进 agent skills 交互指南——包括**修复从不触发或过度触发的 skill、分享前验证 skill 文件夹**（与 wb-skill-authoring 触发质量同域）。
- **patent-application（handsomestWei ★10,034）**：交底→权利要求书/说明书/摘要/附图；**内容争议写入问题清单不阻塞主文件**（与 grill-me 对齐→动手同理念）。
- **提升层**：可复用 Skill / 工作流。

### C3：GitHub agent 生态搜索：VoltAgent 1500+ skills / Google 官方 13 技能（来源：general_search 多源，2026-09-25 实拉）
- **awesome-agent-skills（VoltAgent）**：30+ 公司官方 1500+ Agent Skills 单仓库集合、超 31,800 stars、3,400 forks——生态最全索引（Anthropic 等官方 skills 汇集）。
- **google/skills（Google Cloud Next 2026 发布）**：Google 官方 Agent Skills 仓库，13 项技能覆盖 AlloyDB/BigQuery/Cloud Run/Cloud SQL/Firebase/Gemini API/GKE——云服务 skill 化。
- **addyosmani/agent-skills（Google, Addy Osmani）85K stars**：production-grade 工程 skills 集（API 设计/前后端边界等）。
- **mattpocock/skills 256.9k stars（dev.to 报道）**：工程 skill 集高热度。
- **tt-a1i/archify 54.7k**：AI 代理生成可验证交互式技术图表/系统地图。
- **提升层**：可复用 Skill（生态索引，判重/选型参考库）。

### C4：Hugging Face Trending 生态事实（来源：huggingface.co/models?sort=trending，2026-09-25 实拉）
- **Qwen/Qwen-Image-2.1**：7B Text-to-Image，约 4 小时前更新——图像生成新版本发布。
- **prism-ml/Ternary-Bonsai-2-27B-gguf**：27B Text Generation，**1.91M downloads**、1.6k likes——本地推理 gguf 热门。
- **XingChen-AGI/Xing4.0-29B-A4B**：31B MoE（29B-A4B 激活 4B），12.6k downloads——小激活 MoE 方向。
- **convaiinnovations/laya**：0.4B Text Classification，1 天前更新。
- **HF 模型总量 3,082,055**。
- **提升层**：工具（模型选型生态事实）。

## 判重说明
- C1 → agentskills.io 官方 progressive disclosure 三阶段（Discovery/Activation/Execution）+SKILL.md 最小结构，与 wb-skill-authoring 触发邻域同域、官方机制增量 >60%，落。
- C2 → skillsmp p42-43 精选（STRIDE-A 增量威胁建模 diff/strategic-compact 手动压缩/content-strategy 边界），全新，落。
- C3 → GitHub 生态搜索（VoltAgent 1500+ skills/google/skills 13 技能/addyosmani 85k），生态事实增量，落。
- C4 → HF trending（Qwen-Image-2.1/Ternary-Bonsai gguf/Xing4.0 MoE/总量 308 万），全新生态事实，落。
- 未落：dify blog 续读（difyctl 与 B4 重复；MongoDB RAG 原生记录不落）、n8n workflows 根页（121B 低方法）、死链 3 次（anthropic batching/openclaw automation/waytoagi）按信源健康度持续跟踪。
