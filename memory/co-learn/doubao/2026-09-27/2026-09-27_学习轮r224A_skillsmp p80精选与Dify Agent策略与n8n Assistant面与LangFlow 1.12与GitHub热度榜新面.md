# 学习轮 r224A：skillsmp p80精选与Dify Agent策略与n8n Assistant面与LangFlow 1.12与Make Maia与GitHub热度榜新面（2026-09-27）

## 实拉记录（10 次调用，9 站实拉 / 1 站判定重复）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/80（#7901-7956，5998/10768 取） | OK |
| 2 | Dify 检索（Agent Strategy Plugin/Allowed tools） | OK |
| 3 | n8n 检索（Assistant 更新/2.40.0/Extra Body） | OK |
| 4 | LangFlow 检索（1.11/1.12/A2A/HITL/Agentics） | OK |
| 5 | Activepieces 检索（AI-Ready Pieces/AgentX MCP） | OK（与 r223-B 重叠，无 ≥40% 增量） |
| 6 | Make 检索（Maia by Make/Agent New） | OK |
| 7 | Pipedream 检索（String/Agent Builder） | OK（与 r223-A 重叠，判定重复不落） |
| 8 | ngjoo.com/trending（Top 20+技术概览 513 项目节选） | OK |
| 9 | WaytoAGI 检索（蓝皮书/VoltAgent 1,500 技能） | OK |
| 10 | （Pipedream 重复判定覆盖，未单独计次） | — |

## 独点（4 个）
### A1：skillsmp p80 精选：PPT 编排纪律 / AEO 主题地图 / 内容审核门控 / 网络改前就绪（来源：skillsmp.com/skills/page/80，2026-09-27 实拉）
- **ppt-orchestra-skill（MiniMax-AI/skills ★13,621）**：**用 subagents 生成整份 deck 前先编排——分类每页 slide 类型、强制视觉多样性、设定排版/间距规则、跑文本 QA 抓内容问题**（"先编排再生成"判据，避免批量 PPT 千篇一律）。
- **kai-topical-map（cgallic ★50）**：**AEO-first 主题地图——实体簇、query fan-out 覆盖、信息增益评分、多平台分发；产出实体图/内容节点架构/schema 蓝图/90 天发布日历**（AI 搜索可见性内容规划面）。
- **creator-content-auditor（aaron-he-zhu ★2,816）**：**typed STAR 预发布门控——Trust/Appeal 双评分、profile 加权 SQS、披露/声明/品牌安全与假互动否决项**（内容发布前质检面）。
- **homelab-network-readiness（affaan-m/ECC）**：**改路由器/防火墙/DHCP/VPN 配置前先跑就绪清单——VLAN 分段、本地 DNS 过滤、WireGuard 式远程访问**（改网络前就绪检查面）。
- **remove-ai-slop（davidamitchell）**：**去 AI 味五个目标清单——可预测短语、结构统一、假主体（false agency）、对齐痕迹、词汇单调**（与 doubao-human-signal 同族，五目标清单为增量）。
- **提升层**：可复用 Skill / 工作流。

### A2：Dify Agent Strategy Plugin 与 n8n Assistant 2.40 面（来源：enterprise-docs.dify.ai/marketplace + n8n 检索，2026-09-27 实拉）
- **Dify Agent Strategy Plugin**：**推理策略插件化——给 LLM 推理与决策逻辑（选工具/调用/处理结果）；Agent node 可选 Allowed tools 白名单（只把列出的工具发给模型运行，留空则全量）**（工具白名单面）。
- **Agent node 两种推理模式**：**原生 function calling（GPT-4/Claude 3.5 类）；ReAct 式 Thought→Action→Observation 显式推理链（无原生 function calling 模型或需显式推理轨迹时）**（按模型能力选推理策略面）。
- **n8n 2.40.0（2026-09-15）**：**OpenAI Chat Model 节点新增 Extra Body 字段——给 Qwen-Max/vLLM 等兼容 API 传 provider 特定参数，非法 JSON 明确报错**；**AI Agent Node 跨工具调用保留 Anthropic thinking blocks（空文本也保留）**。
- **n8n Assistant 更新（2026-09-10）**：**AI Assistant 更名 n8n assistant；支持 agents/MCP servers/one-line self-hosting**。
- **提升层**：工具 / 工作流。

### A3：LangFlow 1.11-1.12 与 Make Maia 面（来源：langflow.org blog + help.make.com，2026-09-27 实拉）
- **LangFlow 1.11/1.12**：**A2A（Agent2Agent）协议——发布 flow 让其他 agent 调用、或 flow 内调用远程 A2A agent（默认关，LANGFLOW_A2A_ENABLED=true）**；**Human-in-the-Loop checkpoints（人工检查点）**；**OpenTelemetry 支持（服务健康与 flow runs 可观测）**；**Extension bundles 按需加载（默认最小化安装）**。
- **LangFlow Agentics bundle**：**LLM 处理表格数据的 transduction 代数——aMap（逐行加/填列）/aReduce（多行折叠成一行）/aGenerate（合成行）**（表格 agentic 处理面，arXiv:2603.04241）。
- **Make Maia by Make（2026-08）**：**scenario builder 内的 AI co-worker——描述需求→它 reasoning out loud 实时构建（映射 flow/选工具/配置模块，全部可视化逐步）；No black box**（构建期可视化面，与 r223-A Reasoning Panel 运行期可视化互补）。
- **提升层**：工具 / 工作流。

### A4：GitHub 热度榜新面：OfficeCLI / 到达前压缩 / prefix-cache 工程 / 可视化中间语言 / 决策图漂移检测（来源：ngjoo.com/trending，2026-09-27 实拉）
- **iOfficeAI/OfficeCLI（★15,234）**：**专为 AI 智能体设计的 Office 套件 CLI——单一可执行文件、无需安装 MS Office、零依赖、全平台读取/编辑/自动化 Word(.docx)/Excel(.xlsx)/PPT**（个人用户 Office 自动化面）。
- **headroomlabs-ai/headroom（★73,172）**：**压缩工具输出/日志/文件/RAG chunks 在到达 LLM 之前**（到达前压缩面，与 wb-context-compressor 同族增量：工具输出与 RAG chunk 级）。
- **esengine/DeepSeek-Reasonix（★35,641）**：**DeepSeek 原生终端 AI 编码 agent——围绕 prefix-cache 工程优化**（prefix-cache 缓存工程面）。
- **microsoft/flint-chart（★1,345）**：**可视化中间语言——agent 把简单可编辑图表规范转成精美可视化**（图表规范中间层面）。
- **Brain0-ai/brain0**：**构建决策图把每个 commit 与背后的代理提示关联——漂移检测/数据泄露防护审计/证据驱动风险/MCP 记忆**（提交-提示关联审计面，与 r223-A harness 失败沉淀同族增量）。
- **MemPalace/mempalace（★59,170）+rtk（★81,079）**：**最佳基准开源记忆系统；CLI 代理减 60-90% LLM token 消耗**（记忆/token 代理 benchmark 面）。
- **WaytoAGI Claude Agent Skills 蓝皮书（2026-09-25）**：**五篇二十章学习路径（Skill 是给普通人的礼物→Agent Team→自动进化）+VoltAgent/awesome-agent-skills 1,500+ 官方技能集（Anthropic/Vercel/Stripe/MS/Cloudflare/HF/Trail of Bits）**（技能学习路径面）。
- **提升层**：工具 / 可复用 Skill。

## 判重说明
- A1 五候选全新面，落。
- A2 Dify Agent Strategy Plugin（可插拔推理+Allowed tools 白名单+ReAct 显式链）为 r223-B Agentic RAG 面增量（>60% 平台同源但 ≥40% 策略插件细节增量）；n8n Extra Body+thinking blocks 保留为 2.40 新面，合并落。
- A3 LangFlow A2A/HITL/OpenTelemetry/bundles 为 r223-B Langflow CUGA 面增量（≥40% 新功能）；Make Maia 为 r223-A Reasoning Panel 面增量（构建期可视化），合并落。
- A4 OfficeCLI/headroom/flint-chart/brain0/MemPalace 等新面，落；r222-A CodeGraph 同族面（brain0 决策图）按增量合并保留。
- 未落：Activepieces（与 r223-B AI-ready Pieces/MCP server 重叠无增量）；Pipedream（与 r223-A Edit with AI/MCP server 重叠）。
