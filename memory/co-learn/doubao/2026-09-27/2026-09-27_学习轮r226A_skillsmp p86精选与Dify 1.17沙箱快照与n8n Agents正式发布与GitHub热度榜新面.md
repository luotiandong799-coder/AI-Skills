# 学习轮 r226A：skillsmp p86精选与Dify 1.17沙箱快照与n8n Agents正式发布与GitHub热度榜新面（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/86（#8501-8584 全文下载实拉） | OK |
| 2 | Dify 检索（v1.17.0 release 2026-08-25） | OK |
| 3 | n8n 检索（Agents 正式发布 2026-09-25/2.40 release） | OK |
| 4 | LangFlow 检索（1.13 Next：Exa bundle/Code Agents/LFX） | OK |
| 5 | Activepieces 检索（changelog 2026-09：Reusable Agents） | OK |
| 6 | Make 检索（AI Agents 透明性/构建六步） | OK |
| 7 | Pipedream 检索（MCP OAuth/toolAnnotations/Connect SDK） | OK |
| 8 | Anthropic 检索（Claude Code best practices/七种 steering 方法） | OK |
| 9 | GitHub Trending（ngjoo.com 镜像 2026-09-25 Top20） | OK |
| 10 | GitHub AI 生态（yuxiaopeng ranking AI_Agents Top） | OK |

## 独点（4 个）
### A1：skillsmp p86 精选：账号级对标拆解 / 脚本转视频提示词 / 行动先行状态摘要（来源：skillsmp.com/skills/page/86 全文，2026-09-27 实拉）
- **yyl-benchmark-breakdown（ttfake92-lab/skills ★253，中文）**：**对标拆解——丢链接自动识别平台（抖音/小红书/B站/YouTube/公众号）和粒度（单条 or 整个账号），抓取后输出三件套：可复用爆款公式、画面+口播逐段拆解、人设与内容定位，自动存档 benchmarks/；短视频自动下载+转写口播+抽视觉帧（contact sheet 多模态读图）不只看 caption；抓不到引导粘贴文案绝不报错**（账号级对标拆解面——与 r225-B 单条视频反推互补：加"平台识别路由+账号粒度+三件套输出+多模态读图"）。
- **ai-video-prompt（ttfake92-lab/skills ★253，中文）**：**把脚本/故事节拍/镜头想法转成图片参考型 AI 视频提示词——含图片参考绑定、秒级动作、声音设计和硬约束；点名适配 Seedance 提示词/多图参考/首尾帧/全能参考**（脚本→视频提示词面，与用户 Seedream/Seedance 直接相关）。
- **summarize-status（paperclipai/paperclip ★81,149）**：**状态摘要格式——开头 1-3 个具体动作（读者现在需要做什么来解除阻塞），再简短状态，流式进度**（行动先行汇报面，与 wb-max-token-saver 进度流互补：状态摘要先给行动项）。
- **handoff（openclaw/agent-skills ★1,089）**：**剪贴板就绪的交接 prompt——给另一个 agent 调查或继续任务**（agent 交接面，与多 agent 协作互补）。
- **提升层**：工作流 / 可复用 Skill。

### A2：Dify v1.17.0：构建态快照 / 技能生命周期 / 分层压缩 / 可复用模型配置（来源：newreleases.io langgenius/dify 1.17.0，2026-08-26 实拉）
- **Build-time Home Snapshots**：**agent build 发布时捕获沙箱 home 目录（已装包/准备文件/工作态），后续运行从快照恢复——agent 从构建时的精确文件系统状态开始**（可复现运行环境面：构建态=运行时态）。
- **Workspace-level Skill 管理**：**workspace 级技能管理器——draft→publish→version 生命周期 + Web UI（技能列表/构建面板/文件编辑器）**（技能生命周期面，与 r224-B SKILL.md 规格互补）。
- **Context-aware history compaction**：**长对话不再撑爆上下文窗口——解析每个模型有效窗口并分层压缩（先清旧工具结果，再摘要更早历史），预算内不失近期上下文**（分层压缩顺序面：清工具结果优先于摘要历史）。
- **Reusable LLM Environment Variables**：**共享 provider/model/mode/parameter 配置一处定义多处引用（如 for_summarize/for_research），模型变更一处生效，跨 DSL import/export/RAG pipelines 存活**（模型配置 DRY 面）。
- **Human Input in Loops and Iterations**：**人工表单在循环/迭代节点内工作，跨页面刷新暂停恢复**（r225-A Human Input 面深化）。
- **提升层**：工具 / 工作流。

### A3：n8n Agents 正式发布 + Claude Code 七种 steering 方法（来源：blog.n8n.io 2026-09-25 + claude.com 2026-06-18，实拉）
- **n8n Agents 正式发布（2026-09-25）**：**新类型 Agent——描述做什么+选模型+选工具和 workflows；你的 workflows 可以就是 agent 的工具（workflows-as-tools）；定义一次到处用：直接聊/作为节点拖进工作流/连 Slack/定时跑；agents 有自己的 tab**（r225-A n8n Agents 面正式版：workflows-as-tools 具体机制）。
- **AI nodes fallback model（n8n 2.40）**：**主模型旁配置备选模型自动降级**（模型容错面）。
- **Claude Code 七种 steering 方法（2026-06-18）**：**CLAUDE.md 文件/rules/skills/subagents/hooks/output styles/appending system prompt——每种方法控制三维：何时加载进上下文、是否跨长会话持久（compaction 行为）、有多大权威**（指令放置决策框架面——"指令放哪"按加载时机+持久性+权威度选）。
- **提升层**：工具 / 工作流。

### A4：GitHub 热度榜与 AI 生态新面：超轻量 agent / prefix-cache 原生 / MCP 工具语义标注（来源：ngjoo.com/trending 2026-09-25 + pipedream.com changelog，实拉）
- **HKUDS/nanobot（★48,561）**：**超轻量、开源、自托管个人 AI agent 框架（Python）**——个人自托管 agent 的轻量路径（个人用户面）。
- **DeepSeek-Reasonix（★35,702）**：**DeepSeek 原生终端 AI coding agent，围绕 prefix-cache 优化**（prefix-cache 原生优化面——低成本 coding agent）。
- **Pipedream MCP toolAnnotations**：**10,000+ 工具带 toolAnnotations 标注帮助 MCP 客户端理解 read vs write/destructive 等语义；MCP server OAuth 认证（static URL）**（工具语义标注面——与 OWASP 工具面安全互补：读/写/破坏性在元数据层可见）。
- **提升层**：工具 / 工作流。

## 判重说明
- A1 全为新面（账号级对标拆解/脚本转视频提示词/行动先行摘要/交接 prompt），落。
- A2 Dify 1.17 四机制均未落过（构建态快照/技能生命周期/分层压缩顺序/模型配置 DRY），落。
- A3 n8n Agents 正式发布（workflows-as-tools）+fallback model 新；Claude Code 七种 steering 决策框架新；落。
- A4 nanobot/DeepSeek-Reasonix/toolAnnotations 均新，落。
- 未落：LangFlow Exa/Code Agents bundle（个人价值弱）；Make Agent 构建六步（基础流程面）；Activepieces 句子级构建（与 r225-C agent 复用面重叠>60%，增量<40%）；yuxiaopeng ranking 头部（ECC/hermes 等与已落面重叠）。
