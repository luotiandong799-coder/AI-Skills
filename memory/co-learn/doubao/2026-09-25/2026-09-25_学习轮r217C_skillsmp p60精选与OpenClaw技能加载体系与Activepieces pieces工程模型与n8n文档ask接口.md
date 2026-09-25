# 学习轮 r217C：skillsmp p60精选与OpenClaw技能加载体系与Activepieces pieces工程模型与n8n文档ask接口（2026-09-25）

## 实拉记录（10 次调用，10 成功 / 3 死链计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/60（#5901-5948，5744/11706 取） | OK |
| 2 | dify.ai/blog 续读（109882-114302） | OK（Azure AI Search/Parent-child Retrieval） |
| 3 | docs.langflow.org/manage-memory-bases | 死链（计数，换页） |
| 4 | docs.n8n.io/advanced-ai/ai-assistant.md | 404（返回 ask 查询接口说明，计成功） |
| 5 | GitHub Trending 搜索（github.hot/arran4/ngjoo/agentconn/ghtrends） | OK（security-audit-skill/aichat/reef/Understand-Anything/laya） |
| 6 | deeplearning.ai/community（442B） | OK（社区页，计次） |
| 7 | docs.openclaw.ai/concepts/goals | 死链（计数，换页） |
| 8 | activepieces.com/docs/building-pieces/overview | 死链（计数，换页） |
| 9 | docs.openclaw.ai/skills（4983/8407） | OK（加载优先级/allowlists/$引用/安全） |
| 10 | activepieces.com/docs/pieces/overview（2594B） | OK（pieces=npm TS 包/HITL） |

## 独点（4 个）
### C1：skillsmp p60 精选：代码库→领域流程图 / 长视频多段一致性分镜 / 推理引擎心智模型（来源：skillsmp.com/skills/page/60，2026-09-25 实拉）
- **understand-domain（Egonex-AI/Understand-Anything ★83,219）**：**从代码库提取业务领域知识并生成交互式领域流程图**——轻量扫描独立跑，或从已有 /understand 知识图谱派生。
- **seedance-storyboard（lvzhengbin/AI-Prompts ★2）**：**任何剧本/想法生成多段 Seedance 2.0 分镜提示词——专为 >15 秒长视频设计；支持全能参考+首尾帧两种生成模式，确保多段视频之间角色一致性与叙事连续性**（长视频一致性方法论）。
- **jeff-dean（K-Dense-AI/mimeo ★274）**：Jeff Dean 工程与研究方法——避免过早 100x 扩展、**把 AI 模型当推理引擎而非记忆数据库**、硬件-ML 协同设计、模型蒸馏/稀疏激活/大规模多任务模型。
- **word（ECNU-ICALK/AutoSkill ★553）**：党政机关公文 GB/T 9704-2012 纪律——内容严守事实依据、杜绝虚构政策/机构/案例/数据、**文献引用须 2023-2024 正式发布或现行有效**、输出纯文本零格式标记 Word 可编辑。
- **sn-md-to-html-report（OpenSenseNova/SenseNova-Skills ★5,674）**：Markdown 报告→自包含 HTML 专题页——**必须先写 plan.md 再写 HTML**、保留原文事实断言与结论强度、不套模板不做机械转换。
- **提升层**：工作流 / 可复用 Skill。

### C2：OpenClaw Skills 加载体系：7 层优先级 / allowlists 最终集 / $引用 / 第三方技能不可信（来源：docs.openclaw.ai/skills，2026-09-25 实拉）
- **7 层加载优先级（同名高优先胜）**：workspace skills > 项目 agent skills > 个人 agent skills > managed/local > workshop skills > bundled+custodian > extra dirs；分组发现（SKILL.md 在 root 下最深 6 层都发现，组目录仅组织用）。
- **Per-agent vs shared**：`<workspace>/skills` 仅该 agent；**多 agent 要共享必须发布到 managed library（workshop 学的技能不自动共享）**。
- **Agent allowlists**：位置（precedence）与可见性分开；**非空 `agents.entries.*.skills` 是最终集、不合并 defaults**；`[]` 表示该 agent 无技能。
- **$ 引用**：单消息最多引用 8 个技能（超了显式报错）；**大写 shell 变量（$HOME/$PATH）保持普通文本，小写 $home 引用同名技能，\$name 转义保持字面**；`disable-model-invocation: true` 技能不进 $ picker 与模型 prompt，但 authorized 显式引用仍调用。
- **修订不可变**：保存发布完整快照（revision hash 含路径/内容/大小/可执行标志）；过期编辑冲突失败不覆盖；**会话保留选定技能 ID+修订**；新会话最多 64 个库技能；bundle 限 256 文件/1MiB 每文件/8MiB 总。
- **安全**：**第三方技能当不可信代码——启用前先读、优先沙箱运行**；realpath 路径包含校验；`security.installPolicy` 本地策略命令 fail-closed；**secrets（skills.entries.*.env/apiKey）只注入 host 进程该 agent 轮、不进沙箱**。
- **提升层**：可复用 Skill（技能库工程）。

### C3：Activepieces pieces 工程模型：npm TS 包 / hot reload / Human-in-Loop pieces（来源：activepieces.com/docs/pieces/overview，2026-09-25 实拉）
- **pieces=开源 npm TypeScript 包**：`createPiece({displayName, logoUrl, authors, auth, actions, triggers})`；**60% pieces 由社区贡献**；本地 piece 开发支持 **hot reloading**。
- **Human in Loop**：延迟执行一段时间或要求审批——就是 piece framework 之上的 pieces，可自行构建同类；**内建 human input triggers：Chat Interface / Form Interface**。
- **Secure by Design**：self-hosted+network-gapped；**AI-Ready**：原生 AI pieces+AI SDK 建 agent+Copilot 在 builder 里建 flow。
- **提升层**：工具（集成平台工程模型）。

### C4：n8n 文档 ask 查询接口：GitBook 文档即查（来源：docs.n8n.io/advanced-ai/ai-assistant.md 404 返回，2026-09-25 实拉）
- **docs.n8n.io 支持 `?ask=<question>&goal=<end_goal>` 查询**：GET 任意 `.md` 页带 ask 参数即返回直接回答+相关摘录与来源（GitBook 原生能力）；goal 描述更广的最终目标供定制。
- **sitemap.md 全索引导航**、**llms-full.txt 全量语料导出**（自行解析/检索，更贵）。
- **提升层**：工具（文档查询接口——LLM 直接查文档而非抓站）。

## 判重说明
- C1 全新（p60 独有），落。
- C2 openclaw 增量（skills 页，r217-A/B 只到 slash 命令面），落。
- C3 activepieces 增量（pieces 工程页新入口），落。
- C4 n8n 增量（文档 ask 接口），落。
- 未落：dify Parent-child Retrieval（RAG 面与既有 r214 知识管道点重叠>60%）、trending cloudflare security-audit-skill/laya/reef（描述有限）、deeplearning community（内容有限）。
