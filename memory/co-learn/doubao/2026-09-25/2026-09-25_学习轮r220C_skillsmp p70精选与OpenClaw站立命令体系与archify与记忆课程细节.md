# 学习轮 r220C：skillsmp p70精选与OpenClaw站立命令体系与archify与记忆课程细节（2026-09-25）

## 实拉记录（10 次调用，6 成功 / 4 失败计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/70（#6901-6948，5936/12001 取） | OK |
| 2 | dify.ai/blog 续读（150031-154453） | OK（Annotation Reply v0.3.34/Jina Embeddings v2） |
| 3 | www.langflow.org/blog 续读（4309-8563） | OK（1.10：Memory bases/Assistant flows） |
| 4 | docs.n8n.io/retrieve-relevant-context.md | security strategy 拦截 |
| 5 | GitHub Trending 搜索（archify/ai-engineering-from-scratch/laya） | OK |
| 6 | deeplearning.ai 课程搜索（Agent Memory/LangGraph 记忆） | OK |
| 7 | docs.openclaw.ai/automation/standing-orders | OK（首次完整实拉 2343） |
| 8 | activepieces.com/docs/flows | OK（首次成功：Flow=trigger+actions） |
| 9 | skills.sh/categories | 死链（skills.sh 累积 7 次） |
| 10 | agentskills.io/specification offset 1797 | 越界（total 1797） |

## 独点（4 个）
### C1：skillsmp p70 精选：橡皮鸭评审 / 5 维设计评审 / docx 智能表格填充（来源：skillsmp.com/skills/page/70，2026-09-25 实拉）
- **rubber-duck（microsoft/vscode-team-kit）**：**high-signal 反馈——对 plans/designs/implementations/partial progress 抓 bug/逻辑错误/设计缺陷；最佳时机=规划后实现前；不评风格/格式/琐事**（实现前橡皮鸭评审时机纪律）。
- **critique（nexu-io/open-design ★97,471）**：**5 维专家设计评审——Philosophy/Visual hierarchy/Detail/Functionality/Innovation 各 0-10 分，输出自包含 HTML 报告+雷达图+Keep/Fix/Quick-wins 三清单（证据支撑分数）**。
- **fill-docx-template（LeoYeAI/openclaw-master-skills ★2,128）**：**模板填充 Word——{name} 占位符替换、{name|r:x,c:y} 智能表格填充（标记行向下填充保留上方）、插图、批量生成**。
- **geo-content-optimizer（aaron-he-zhu）**：**AI 引用优化（GEO）——提升 ChatGPT/Perplexity/AI Overviews/Gemini/Claude 的 citation readiness（非结构性 SEO）**。
- **image-to-svg（oaustegard）**：栅格图转 SVG 矢量复刻——构图流水线提取线条为 SVG strokes。
- **提升层**：工作流 / 可复用 Skill。

### C2：OpenClaw Standing orders 体系：永久操作授权四要素 + Execute-Verify-Report（来源：docs.openclaw.ai/automation/standing-orders，2026-09-25 完整实拉）
- **Standing orders = permanent operating authority**：**不用每任务提示，定义 Program（scope 授权范围/triggers 何时执行/approval gates 需人工签字/escalation rules 何时停止求助）**，agent 在边界内自主执行。
- **放置位置**：**AGENTS.md（每会话 auto-injected）最优先；bootstrap 自动注入 AGENTS.md/SOUL.md/IDENTITY.md/USER.md/BOOTSTRAP.md/MEMORY.md——不注入子目录任意文件；CI 一次性入口用 `openclaw agent exec`（跳过 bootstrap）**。
- **Execute-Verify-Report pattern**：**每任务三环：Execute（真干活不是口头确认）→Verify（证明结果正确）→Report（汇报做了什么+验证了什么）；失败重试一次换法，仍失败带诊断上报，绝不静默失败；最多 3 次后升级**（防最常见失败模式 acknowledge-without-completing）。
- **Standing orders 定义 what + Automations 定义 when**：自动化 job 的 prompt 引用 standing order 而非复制它。
- **提升层**：工作流（常驻任务授权模型）。

### C3：GitHub 生态：archify 架构图技能 + ai-engineering-from-scratch 方法论（来源：GitHub Trending 搜索，2026-09-25 实拉）
- **tt-a1i/archify（★71,112，+55,857 stars/月）**：**可验证架构/工作流/时序/数据流/生命周期图 agent skill——自包含 HTML with motion + crisp export**（架构图技能暴涨标杆）。
- **rohitg00/ai-engineering-from-scratch**：**免费开源 AI 工程课程——503 课 20 阶段（线性代数→自治多 agent 群）；每课交付可复用 artifact（prompt/skill/agent/MCP server）遵循 Build It/Use It/Ship It 方法论**。
- **laya（NandhaKishorM）**：**非自回归决策引擎——33ms 单次前向传递读文本返回 typed answer/choice/score/yes-no**（typed decision 基础设施）。
- **提升层**：工具 / 可复用 Skill。

### C4：deeplearning 记忆课程细节 + Langflow 1.10 Memory bases（来源：deeplearning.ai 检索 + langflow.org/blog，2026-09-25 实拉）
- **Agent Memory: Building Memory-Aware Agents（Oracle AI Database）**：**完整记忆系统设计——存储/检索不同记忆类型、语义搜索扩展工具访问、write-back loops 让 agent 自主更新记忆、组装 stateful Memory Aware Agent（启动时加载 prior context 再组装相关 context/state/tools/outputs）**（r219 四类记忆的工程实现面）。
- **Long-Term Agentic Memory With LangGraph**：**Email Assistant 记忆逐步叠加法——Semantic→+Episodic→+Procedural 分阶演进**（可复现的教学路径）。
- **Building and Evaluating Advanced RAG（TruEra/LlamaIndex）**：sentence-window 与 auto-merging 检索 + RAG Triad of metrics。
- **Langflow 1.10**：**Memory bases（长期语义记忆）+ Assistant 构建整个 flows + 可配置向量数据库后端 + 七语言界面**。
- **提升层**：模型（记忆工程）/ 工作流。

## 判重说明
- C1 全新（p70 独有），落。
- C2 openclaw standing-orders 新页完整实拉（授权模型四要素+EVR 模式此前未落），落。
- C3 trending 增量（archify/ai-engineering-from-scratch 新条目），落。
- C4 记忆课程工程细节（Oracle stateful agent 架构+LangGraph 逐步叠加法，r219 记忆工程增量的 ≥40% 独有），落。
- 未落：n8n retrieve-relevant-context（拦截）、skills.sh/categories（死链）。
