# 学习轮 r213-B：Anthropic claude-code memory官方增量与skillsmp p48与dify Agentic RAG与deeplearning.ai语音三模式（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/48（#4701-4746，5950/12691 取） | OK（anti-defensive-writing/h3-prompt-writing/liteparse 等） |
| 2 | dify.ai/blog 续读（43212-48746） | OK（Agentic RAG/Multimodal KB/Triggers） |
| 3 | docs.anthropic.com claude-code/memory（5714B 全） | OK（auto memory 存储结构/paths rules/AGENTS.md 导入） |
| 4 | docs.langflow.org/components（720B 全） | OK（组件分组/版本管理） |
| 5 | pipedream.com 续读（4320-8418） | 低方法（纯图片无文字） |
| 6 | github.com/trending（不带 offset，4182/72370 取） | OK（ai-engineering-from-scratch ★57,050 重复） |
| 7 | deeplearning.ai/short-courses 续读（13450-18004） | OK（AI Code Review/Voice for AI Agents/Cerebras） |
| 8 | agentskills.io/docs | 死链（link dead，计数） |
| 9 | github.com/trending 续读（4182-8310） | OK（hindsight ★28,469 与 r212-B 重复） |
| 10 | docs.openclaw.ai/capabilities/skills | 死链（link dead，计数） |

## 独点（4 个）
### B1：Anthropic claude-code/memory 官方页增量：auto memory 存储结构 / paths 条件规则 / AGENTS.md 导入 / compact 存活（来源：docs.anthropic.com/en/docs/claude-code/memory，2026-09-25 实拉；与 r211-B 已落 auto memory 基础合并保留增量，增量 ≥40%）
- **auto memory 存储结构（官方）**：`~/.claude/projects/<project>/memory/`——**MEMORY.md 索引 + 主题文件**（debugging.md/api-conventions.md）；**前 200 行或 25KB 门槛**加载到每会话；主题文件按需读；`/memory` 浏览编辑。
- **同 repo 共享 + 防重定向**：project 路径从 git repo 派生，**同 repo 所有 worktree/子目录共享一个 auto memory 目录**；跨机器不共享；**`autoMemoryDirectory` 不接受 project settings**（防共享项目把 auto memory 重定向到敏感位置）。
- **路径特定规则（.claude/rules paths frontmatter）**：条件规则只在 Claude 读取匹配文件时加载（glob：`src/api/**/*.ts`/`*.md`/brace expansion），非每次工具使用；symlink 共享规则、循环 symlink 优雅处理。
- **AGENTS.md 导入模式**：Claude Code 读 CLAUDE.md 不读 AGENTS.md——**用 `@AGENTS.md` 让两个工具读同一指令不重复**，导入后可追加 Claude 专属指令。
- **CLAUDE.md 加载细节**：向上走目录树全量加载、子目录按需；**HTML 块注释（`<!-- -->`）在注入前剥离**（省 context token，维护者笔记免费）；`@path` 导入最大五跳、相对路径相对导入文件；外部导入首遇显示审批对话框、拒绝后不再出现。
- **/compact 后 CLAUDE.md 完全存活**：compact 后从磁盘重新读入——指令"消失"只可能是会话内说的没写进文件；CLAUDE.md 作为 user message（非 system prompt）传递，无强制保证；`InstructionsLoaded` hook 记录加载文件。
- **提升层**：可复用 Skill / 工作流（记忆与规则组织官方参考）。

### B2：skillsmp p48 精选：去防御性写作 / 视频多模态提示词结构 / 本地解析 / 子技能总控（来源：skillsmp.com/skills/page/48，2026-09-25 实拉）
- **anti-defensive-writing（Kiterlin/anti-defensive-writing ★599）**：**减少防御性写作**——移除五类：不必要的 caveat、disclaimer、hedge、apology-like framing、负面自我设限/过度解释；**保留**必要范围、准确性、安全、法律、伦理、方法论限制——"去防御 ≠ 丢限制"边界清晰。
- **h3-prompt-writing（MiniMax-AI/MiniMax-H3 ★9,002）**：**MiniMax H3 视频生成提示词结构**——T2VA/I2VA/FL2VA/L2VA/Ref2VA 五模式；`integrated_multimodal_description`/`overall_soundscape`/`non_diegetic_music` 三段结构、关键帧对齐、图像/视频/音频参考标签定义。
- **liteparse（K-Dense-AI/scientific-agent-skills ★45,497）**：本地文档/PDF 解析——**per-token 边界框 + 页面栅格输出 + 全本地无云 API**；布局保留 JSON 供 RAG、批量论文摄取、PNG 渲染供多模态 agent。
- **short-drama-factory（lixiaoxiao9888 ★182）**：短剧工业化编剧引擎——**情绪契约单元链往返法**、三档篇幅（90-120 秒/3 分钟/漫剧 60-90 秒）、60/80/100 集结构、跨集连续性台账、机制级仿写、分档剧本机检。
- **space-video（SpaceZephyr/creator-buddy ★1,495）**：**视频创作总控/导演**——把"参考素材→选题→脚本→剪辑→B-roll→字幕→封面"串成流水线，判断当前该走哪一步、调用哪个 space-video-\* 子技能（总控+子技能路由模式）。
- **nssfc-proposal（LeonChaoX/qinyan-academic-skills ★910）**：国家社科基金 NSSFC 申请书（2025 官方模板，A/B/C/X 四类，分阶段工作流含活页匿名化；工具中性适配五平台）。
- **提升层**：可复用 Skill / 工作流。

### B3：Dify Agentic RAG + 多模态知识库 + Triggers 统一（来源：dify.ai/blog，2026-09-25 实拉）
- **Agentic RAG（Agent Node 工作流）**：不同于一次性 retrieval-then-generation，**agent 迭代分析意图、选择工具与来源、改写查询、评估证据、重试或回退**——提升 grounding 与可靠性，但**明确增加延迟、成本、复杂度**（官方承认的权衡）。
- **Multimodal Knowledge Base**：文本+图像统一到**单一语义空间**（Embedding+Rerank），支持多模态 RAG 与视觉推理。
- **Dify Triggers 统一三形态**：scheduled execution（Schedule）、事件驱动自动化（Plugin）、插件集成（Webhook）——从被动响应到全自动可扩展。
- **提升层**：工作流（RAG 架构）。

### B4：deeplearning.ai 语音三模式 + Langflow 组件分组与版本管理（来源：deeplearning.ai / docs.langflow.org，2026-09-25 实拉）
- **Voice for AI Agents 三种集成模式（Vocal Bridge）**：①嵌入式语音 ②现有 agent 叠加语音层 ③**语音作为可调用工具**——按架构选择。
- **AI Code Review（Qodo）**：AI 代码比团队能手工审查的多——**早期运行 review、给 reviewer 正确上下文**；上下文是 review 可靠的关键。
- **Langflow 组件模型**：组件=输入/输出/参数；**Group Components 把多组件分组为单组件复用**（Shift 拖选→Group→侧栏保存）；**组件版本**：状态存数据库、侧栏是 starter template、拖入后不再 parity、Update Component 图标原地升级代码。
- **提升层**：工具 / 工作流。

## 判重说明
- B1 → claude-code/memory 官方页增量（auto memory 结构/paths rules/AGENTS.md/compact 存活），与 r211-B 已有 auto memory 基础合并保留增量（增量 ≥40%），落。
- B2 → skillsmp p48 精选（去防御性写作/视频提示词结构/本地解析/子技能总控），全新，落。
- B3 → Dify Agentic RAG + Multimodal KB + Triggers，RAG 层增量，落。
- B4 → 语音三模式 + Langflow 组件分组/版本，小增量合并，落。
- 未落：Pipedream 续读（纯图片无文字）、GitHub trending 首条 ai-engineering-from-scratch（与 r211-B 重复）、hindsight（与 r212-B 重复）、adult-nsfw-prose（色情内容安全边界不落）、agentskills.io/docs 与 docs.openclaw.ai/capabilities/skills（死链计数）。
