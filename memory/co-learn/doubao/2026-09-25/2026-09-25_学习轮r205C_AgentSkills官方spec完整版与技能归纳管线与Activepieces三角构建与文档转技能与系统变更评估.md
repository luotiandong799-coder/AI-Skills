# 学习轮 r205-C：Agent Skills官方spec完整版与技能归纳管线与Activepieces三角构建与文档转技能与系统变更评估（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | blog.n8n.io/advanced-rag-data-cleaning-retrieval-techniques/ | 死链 |
| 2 | activepieces.com/docs（3375/19123） | OK（三角构建块/BYOK 治理） |
| 3 | skillsmp.com/skills/page/23（#2201-2269 两段） | OK（69 项） |
| 4 | agentskills.io/specification（1797 全） | OK（官方 spec 完整版） |
| 5 | docs.pipedream.com/configuration/ | 死链 |
| 6 | docs.openclaw.ai/concepts/heartbeat | 死链 |
| 7 | （skillsmp p23 后半并入 #3） | — |
| 8 | general_search deeplearning.ai 新课程 | OK（Agent Skills 课程/Adaptive Agents 三层） |
| 9 | （deeplearning.ai 详情并入 #8） | — |
| 10 | （activepieces 根页续段） | — |

## 独点（5 个）
### T1：Agent Skills 官方 spec 完整版：metadata/allowed-tools 新字段 + Progressive Disclosure 三档 token 预算 + skills-ref validate（来源：agentskills.io/specification，r204-C P3/P1 的官方增量，按增量判定合并落地）
- **frontmatter 全字段**：name（1-64 小写字母数字+连字符，不得首尾/连续连字符，匹配父目录）/description（1-1024，做什么+何时用，**含具体关键词帮 agent 识别任务**——好例 "Extracts text and tables from PDF files, fills forms, merges" vs 差例 "Helps with PDFs"）/license（短）/compatibility（1-500，环境要求，多数不需要）/ **metadata（新字段：任意 key-value 映射，存 spec 未定义属性，key 名尽量独特防冲突）** / **allowed-tools（新字段·实验性：空格分隔预批准工具，如 Bash(git:*) Bash(jq:*) Read）**。
- **Progressive Disclosure 三档**：①Metadata（~100 tokens：所有技能 name+description 启动即载）②Instructions（<5000 tokens 建议：SKILL.md 全文激活时载）③Resources（按需：scripts/references/assets 用到才载）——**主 SKILL.md 保持 <500 行，细节外移**。
- **文件引用一层深**：references 用相对路径从 skill root，**避免深层嵌套引用链**。
- **官方校验**：`skills-ref validate ./my-skill` 检查 frontmatter 与命名规范。
- 判据：**技能三档加载预算（100/5000/按需）**；自定义属性进 metadata 不进 description；装前用官方工具校验。
- **提升层**：可复用 Skill（作者规范/官方工具）。

### T2：技能归纳管线 + 三层适应（来源：DeepLearning.AI×Oracle《Building Adaptive AI Agents》2026-08-26）
- **Behavior Adaptation（行为适应）**：**skill induction pipeline——把 agent traces（工具调用序列/对话/错误修复过程）转化为可复用、人批准（human-approved）的程序性技能**——从"这次怎么修的"自动沉淀为"以后都这么修"。
- **Knowledge Adaptation（知识适应）**：**code knowledge graph——用 imports/函数调用/git 历史共编辑映射关系做上下文检索**，比传统向量检索有结构优势（知道"谁依赖谁"而不只是"谁像谁"）。
- **分层分类**：三层适应（行为/知识/第三层按课程全文）——改进分门别类，不一把抓。
- **Agent Skills with Anthropic 课程（2026-01）**：skills=指令文件夹按需加载；**open standard 一次构建跨任何 skills-compatible agent 部署**；预建 skills（Excel/PowerPoint）；**skills+MCP+subagents 组合复杂工作流**。
- 判据：**错误修复要沉淀为技能（人批准后）**；知识检索可走代码结构图不只有向量。
- **提升层**：可复用 Skill / 学习自动化。

### T3：Activepieces 三角构建块 + BYOK 自带治理（来源：activepieces.com/docs）
- **三构建块互调**：**agent 可调 flow、flow 可跑 agent、两者读写同一 tables**——不是孤立三件套，是互通三角。
- **Build with AI**：聊天描述需求→自动建 agent/automation。
- **BYOK + 自托管 + 治理内建**：带自己的 AI keys、跑自己基础设施、保留公司需要的治理——企业 AI 采用的关键约束。
- 判据：**数据层共享（tables）是 agent/flow 互通的支点**；治理随平台内建而非事后补。
- **提升层**：工作流 / Agent 平台。

### T4：文档→结构化技能 book-to-skill + llm-wiki 知识积累架构（来源：skillsmp p23 #2231/#2261，alirezarezvani/claude-skills）
- **book-to-skill**：书/文档夹→结构化 agent skills——提取 named frameworks/principles/techniques/anti-patterns →**master SKILL.md+按需章节文件+glossary+patterns+decision cheatsheet**；可打包 claude-skills 插件。文档→技能的标准化转换链。
- **llm-wiki（第二大脑）**：Obsidian 持久个人知识库，**LLM 增量摄取源→更新实体/概念页→维护交叉引用→保持综合当前**——**知识跨会话积累，而非每查询 RAG 重推导**；触发"second brain/ingest this paper/build a research wiki"。
- 判据：**文档可转为技能资产**（不只摘要）；知识库是增量维护的活页，不是检索缓存。
- **提升层**：可复用 Skill / 知识管理。

### T5：非平凡系统变更评估纪律（来源：skillsmp p23 #2232，bytedance/deer-flow）
- **engineer-system-change**：评估 RFC/issue/设计/重构/迁移/依赖变更/新字段/API/模块——**读真实系统**（不读文档臆测）、**识别具体问题和命名语义消费者**、选**最小充分方案**、**拒绝伪需求和投机抽象**、**证据与风险成比例**（改动风险越大要求证据越硬）。
- **明确不适用**：机械编辑/源码讲解/已完整 diff 的专项评审。
- 判据：**系统变更先读真实系统再下结论**；伪需求与投机抽象是方案膨胀的根源；证据要求随风险缩放。
- **提升层**：工作流 / 工程纪律。

## 判重说明
- T1 → r204-C P3（name/description 约束）与 P1（description 预算 2%）同源；metadata/allowed-tools 新字段+三档 token 预算（100/5000/按需）+文件引用一层深+skills-ref 官方校验为独有增量，合并落地。
- T2 → 无既有"trace→技能"记录；r205-B S4 有 skill 生态管理；"skill induction pipeline+人批准+code knowledge graph"为独有，落。
- T3 → r204-C P2 已有 n8n 多 agent；Activepieces"三角互调+BYOK 治理"为平台增量，落。
- T4 → wb-context-compressor 已有记忆/压缩；"文档→技能转换链+增量知识积累架构"为知识管理增量，落。
- T5 → wb-execute-discipline 已有 AI 代码收 diff 五连查；"读真实系统/最小充分方案/拒伪需求/证据随风险缩放"为评估前置增量，落。
- 未落：n8n advanced-rag/pipedream configuration/openclaw heartbeat 死链；unrestricted-executor（解除限制危险技能，不学）；trump-perspective（政治人物模拟，不落）；business-pulse（渐进连接器裁剪弱）；deslop（human-signal 已有）；deep-research（豆包已有）；talking-head-cut（mediakit 已有）；aig-agent-redteam（安全红队，候选下轮）；dmux-workflows（工具）；recsys-pipeline（专业推荐）。
