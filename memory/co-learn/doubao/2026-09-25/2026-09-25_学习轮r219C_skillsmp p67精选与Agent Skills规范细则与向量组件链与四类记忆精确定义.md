# 学习轮 r219C：skillsmp p67精选与Agent Skills规范细则与向量组件链与四类记忆精确定义（2026-09-25）

## 实拉记录（10 次调用，8 成功 / 2 失败计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/67（#6601-6653，5955/11142 取） | OK |
| 2 | dify.ai/blog 续读（136630-141115） | OK（Workflow as Tool/Firecrawl 集成） |
| 3 | www.langflow.org/ 续读（16996-20182，读完） | OK（官网全文读完） |
| 4 | docs.n8n.io/store-and-search-data-with-vectors.md | OK（向量数据库组件链） |
| 5 | GitHub Trending 搜索（CLIProxyAPI/Git-Native Agent Protocol） | OK |
| 6 | deeplearning.ai Agent Memory 课程搜索 | OK（Oracle 四类记忆精确定义） |
| 7 | docs.openclaw.ai/automation/cron-jobs（索引页） | OK（automations 全索引结构） |
| 8 | activepieces.com/docs/flows/overview | 死链（activepieces 累积 6 次） |
| 9 | skills.sh/docs | OK（文档页：遥测排行榜/安全审计） |
| 10 | agentskills.io/specification | OK（完整格式规范） |

## 独点（4 个）
### C1：skillsmp p67 精选：证据驱动教练 / 双 agent 对抗验证 / 技能锻造 / 记忆实体化（来源：skillsmp.com/skills/page/67，2026-09-25 实拉）
- **reflection-coach（paperclipai/paperclip ★81,149）**：**反思另一 agent 近期执行记录，提出最小持久指令/技能/工具描述变更——证据支持的教练提议，绝不热替换（never hot-swaps）**。
- **santa-method（affaan-m/ECC ★264,820）**：**带收敛循环的多 agent 对抗验证——两个独立评审 agent 都通过才出货**。
- **browser-act-skill-forge（browser-act/skills ★5,969）**：**从网站探索锻造可复用 Skill 包（SKILL.md+scripts）——理解站内 API、复刻现有 scraper/SaaS 产品、批量提取（几十到几千条、去重）；可复用非一次性**。
- **memory-ingest（basicmachines-co/basic-memory ★4,014）**：**非结构化外部输入→结构化 Basic Memory 实体——提取实体、搜已有匹配、提议新实体需批准、创建含观察与关系的笔记、捕获 action items**。
- **tech-debt-audit（code-yeongyu/oh-my-openagent ★69,266）**：**9 维度技术债审计——AST-grep（tree-sitter）/grep/LSP/语言原生工具、TECH_DEBT_AUDIT.md 含严重度/工作量/优先级修复**。
- **提升层**：工作流 / 可复用 Skill。

### C2：Agent Skills 规范细则：frontmatter 字段约束 + progressive disclosure 预算（来源：agentskills.io/specification + skills.sh/docs，2026-09-25 实拉）
- **SKILL.md frontmatter 字段表**：name（≤64 字符、仅小写字母数字+连字符、不得首/尾/连续连字符、**必须匹配父目录名**）；description（≤1024 字符、写清做什么+何时用+关键词）；license（可选）；compatibility（≤500 字符、环境要求）；metadata（任意键值）；**allowed-tools（可选实验性：空格分隔预批准工具，如 `Bash(git:*) Bash(jq:*) Read`——技能级最小权限）**。
- **progressive disclosure 三档预算**：**metadata ~100 tokens 启动全加载 / instructions <5000 tokens 激活加载（SKILL.md 建议 <500 行）/ resources 按需加载**；references 文件保持聚焦、文件引用一层深。
- **skills-ref validate 校验**：`skills-ref validate ./my-skill` 验证 frontmatter 合法与命名规范。
- **skills.sh/docs**：**排行榜基于匿名遥测（仅统计安装、无个人信息）；README 安装数 badge；例行安全审计（security.vercel.com 报告）；CLI 开源（vercel-labs/skills）**。
- **提升层**：可复用 Skill（规范与预算）。

### C3：n8n 向量数据库组件链 + Dify Workflow as Tool（来源：docs.n8n.io + dify.ai/blog，2026-09-25 实拉）
- **n8n 向量组件链**：**document loaders 拉入文档+text splitters 分块 → embeddings 转向量（n8n 仅支持文本）→ retrievers 从向量库取文档（需配对 embedding 转回数据）**；向量库=高维向量存语义特征、相似性搜索替代常规查询。
- **Dify v0.6.9 Workflow 大更新**：**发布 workflow 作为工具（Publish Workflows as a Tool）——workflow 可被其他节点/应用调用；迭代节点（iteration nodes）+参数提取器（parameter extractors）+增强节点能力**；v0.6.11 集成 Firecrawl 网页数据源知识库。
- **提升层**：工作流（向量管道/工作流工具化）。

### C4：Oracle 四类记忆精确定义 + OpenClaw automations 索引结构（来源：deeplearning.ai 课程 + docs.openclaw.ai，2026-09-25 实拉）
- **Oracle 四类记忆表（r219A A3 的精确化增量）**：**Working=当前思考（scratchpad/notes/TODOs）；Episodic=特定过去事件（对话/错误）；Semantic=稳定事实（领域知识/私有数据/schema）；Procedural=如何做（skills/skill chains/workflows/notes to self）**。
- **Memory Operations**：**Extraction（提取）/ Consolidation（合并）/ Self-Updating（agent 自主写回更新记忆——write-back loops）**；**Semantic Tool Memory——用语义搜索扩展工具访问（工具多了用语义检索而非枚举）**。
- **OpenClaw automations 索引结构**：**Runtime model（how automations work/isolated run hardening/task reconciliation/promoting repeated job into automation）；Payload（agent-turn options --model/--thinking/--light-context/--tools；command/script payloads；main vs current vs isolated vs custom 执行样式；unattended run contract）；Troubleshooting 三形态（automations not firing/job fired but no delivery/rollover & timezone gotchas）**。
- **提升层**：模型（记忆架构）/ 工具（调度器索引）。

## 判重说明
- C1 全新（p67 独有），落。
- C2 agentskills 规范页+skills.sh 文档页增量（frontmatter 约束与预算），落。
- C3 n8n 向量面首成+dify workflow-as-tool 增量，落。
- C4 deeplearning 四类记忆精确化（A3 名目版→精确定义+memory operations+semantic tool memory 增量）+openclaw automations 索引（r218B 调度的故障排查/硬化增量），落。
- 未落：langflow 官网已读完整（无新独点）、activepieces flows（死链）。
