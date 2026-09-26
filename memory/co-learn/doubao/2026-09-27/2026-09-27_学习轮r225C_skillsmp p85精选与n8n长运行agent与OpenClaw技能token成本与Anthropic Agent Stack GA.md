# 学习轮 r225C：skillsmp p85精选与n8n长运行agent与OpenClaw技能token成本与Anthropic Agent Stack GA（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/85（#8401-8455 取） | OK |
| 2 | Dify 检索（1.16.1/prompt 优化助手/Code auto-fix/Stateful Orchestrator） | OK |
| 3 | n8n 检索（Agents 用例/long-running agents/multi-channel 记忆管线/AgentCore） | OK |
| 4 | LangFlow 检索（1.13 组件版本化/File Content Retriever） | OK |
| 5 | Activepieces 检索（agent 工具来源/复用/暂停批准） | OK |
| 6 | Make 检索（记忆架构可视化/Functions app/Data Store） | OK |
| 7 | Pipedream 检索（emit 事件链/triggers） | OK |
| 8 | Anthropic 检索（Agent Stack GA/Skills API 渐进式披露/版本钉住） | OK |
| 9 | OpenClaw 检索（技能 token 成本/Memory-Wiki/Skill Workshop/Dreaming） | OK |
| 10 | deeplearning.ai 检索（Agentic AI 课程/LangMem） | OK |

## 独点（4 个）
### C1：skillsmp p85 精选：分镜审核 / 平台无关写书 / OKR 逻辑重组汇报（来源：skillsmp.com/skills/page/85，2026-09-27 实拉）
- **storyboard-review-skill（Supreme-Ultimate/novel-to-script-team ★171）**：**分镜审核——节拍拆解/Beat Board/Sequence Board 逐项比对+脑内预演+评分制确保分镜质量达标**（审核面，与 r225-B 拆解互补：拆解产出后必须过审核门）。
- **best-selling-book-writer（duchangyu ★18）**：**AI 写书+自助出版全流程——选题→大纲→章节→封面→Amazon KDP 元数据→HTML/PDF；平台无关，明示可在 WorkBuddy/Claude Code/Codex/OpenClaw/Hermes 等任何有文件系统的 agent 用**（平台无关长文档工作流面，与用户既有"唯一落地位置+git 留痕"工作流同构）。
- **daily-reporter-skill（freestylefly ★20）**：**日报/周报/月报——碎片信息转成果导向汇报；内置 OKR 逻辑重组引擎自动识别核心产出与日常维护，汇报重点突出**（汇报重组面：核心产出 vs 日常维护分槽）。
- **提升层**：工作流 / 可复用 Skill。

### C2：n8n 长运行 agent 上下文四步 + Anthropic Agent Stack GA 与渐进式披露（来源：blog.n8n.io + claude.com/blog + platform.claude.com，2026-09-27 实拉）
- **n8n《Long-running agents beyond prompt engineering》Context-Memory 四步（2026-08-31）**：**Create（理解并构造上下文）→ Compress（压缩）→ Store（LLM 无状态，上下文易失必须写持久存储）→ Recall（用账本检索）**（长运行 agent 上下文管理面，与 wb-context-compressor 直接同源互补）。
- **多通道自托管助手长期记忆管线**：**Email/Document Manager 各用 Haiku 4.5；独立定时流从 Postgres 拉新 chat 历史→聚合摘要→OpenAI embedding→Supabase 向量库供 RAG**（长期记忆管线具体装配面）。
- **Anthropic Agent Stack GA（2026-08-20）**：**computer use（多动作回合 batch actions 一轮模型回合完成一组动作减少往返+HIPAA）、browser-use tool（读页面结构而非像素）、Skills API、Files API（1TB/组织、5× rate limits）四件套转正**（平台面事实+多动作回合机制）。
- **Skills API 渐进式披露（progressive disclosure）+生产版本钉住**：**启动时 GET /v1/skills 只拉元数据（名字+简短描述，成本极低），任务匹配时才加载完整说明；生产环境 pin 到具体版本 `version:"1759178010641129"`**（技能加载架构面，与 r224-B 规格面互补——元数据/全文分离加载）。
- **提升层**：工具 / 工作流。

### C3：OpenClaw 面：技能描述 token 成本 / Memory-Wiki / Skill Workshop / Dreaming（来源：docs.openclaw.ai + openclawai.io/changelog，2026-09-27 实拉）
- **技能描述有可量化的 token 成本（docs.openclaw.ai/tools/skills）**：**XML escaping 把 & < > " ' 扩成实体每字符多几字符；~4 chars/token，97 字符 ≈ 24 tokens per skill（字段长度之前）——描述保持简短以最小化 prompt 开销；会话启动时快照合格技能**（技能描述 token 成本量化面——写描述/description 时的成本意识）。
- **Memory-Wiki（v2026.4.7）**：**结构化记忆——Claims+evidence、contradiction detection（矛盾检测）、freshness tracking（新鲜度）、compiled knowledge digests（知识摘要编译）；外接应用可读写**（结构化记忆面，与记忆四策略互补：加"证据+矛盾检测+新鲜度"三维）。
- **Skill Workshop（2026-08-08）**：**治理化技能提案——支持文件处理/审查动作/修订流/可搜索预览/可复用 session handoff**（技能治理面，与 wb-skill-authoring 闭环互补）。
- **Dreaming（v2026.4.9）**：**长期记忆定期整合——分析会话历史周期合并（与 wb-context-compressor"定期整合类似睡眠"同构，OpenClaw 实命名）**。
- **提升层**：工具 / 可复用 Skill。

### C4：Dify 1.16.1 自修复与 Activepieces flow-as-tool 与 Make 记忆可视化（来源：agenticindex.io + dify.ai + activepieces.com + help.make.com，2026-09-27 实拉）
- **Dify v1.16.1（2026-09）+prompt 助手/auto-fix**：**Tool Multi-Select Input（一次配置多个工具参数）；Workflow Node Locator（运行日志错误直连画布节点）；LLM node prompt 优化助手（不达预期自动生成改进版）/Code node auto-fix（失败自动修正代码）——优化与修复都存为新版本可对比回退**（自修复+版本回退面，与 r224-C 双 check 互补：从"检查"到"自动修+可回退"）。
- **Activepieces agent 工具来源与复用（2026-04-03）**：**"From Piece" 用内置集成；"From Flow" 把现有工作流转成 agent 可调用工具；agent 创建后成为可复用组件（像 Gmail piece 一样拖进任意新自动化，一处更新处处生效）；需要先检查的动作等待批准再执行**（flow-as-tool+agent 复用面，与 r225-A Human Input 互补）。
- **Make 记忆架构可视化（2026-05-05）**：**Scenario Builder 直接显示上下文在哪捕获/传递/写入或丢失——记忆架构可见而非从隐藏字段映射推断；场景以 data store read 开始→AI 模块→data store write 更新记录；IML 函数独立成模块（Functions app）链式数据转换**（记忆可见性面——"直接看到上下文在哪丢"）。
- **Pipedream $.send.emit() 工作流事件链**：**工作流发事件触发另一工作流——多个来源事件统一处理（如多工作流统一日志到 S3）**（事件链面）。
- **提升层**：工具 / 工作流。

## 判重说明
- C1 全为新面（分镜审核/平台无关写书/OKR 重组汇报），落。
- C2 n8n 上下文四步与 wb-context-compressor 同源但为平台实现（Create/Compress/Store/Recall 四步+多通道管线装配）；Anthropic Agent Stack GA+渐进式披露+版本钉住未落过；落。
- C3 OpenClaw 技能描述 token 成本量化（具体数字）+Memory-Wiki 三维+Skill Workshop+Dreaming 均未落过，落。
- C4 Dify v1.16.1 自修复存版本回退新；Activepieces From Flow/agent 复用新；Make 记忆可视化+函数模块化新；Pipedream emit 事件链新；落。
- 未落：LangFlow 组件版本化（r225-B Activepieces 版本管理重叠）；deeplearning.ai 课程（基础方法论面，无新增独有机制）。
