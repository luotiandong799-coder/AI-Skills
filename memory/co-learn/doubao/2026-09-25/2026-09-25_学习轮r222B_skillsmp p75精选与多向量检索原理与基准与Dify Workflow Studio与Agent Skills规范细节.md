# 学习轮 r222B：skillsmp p75精选与多向量检索原理与基准与Dify Workflow Studio与Agent Skills规范细节（2026-09-25）

## 实拉记录（10 次调用，6 成功 / 4 失败计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/75（#7401-7455，5992/10780 取） | OK |
| 2 | langflow.org/blog/blog-nextplaid（4642 全） | OK |
| 3 | docs.n8n.io how-memory-works.md | dead（security 拦） |
| 4 | dify.ai/zh/workflows（4367/22306 取） | OK |
| 5 | OpenClaw 技能生态检索（GOG/ClawHub 下载 Top） | OK |
| 6 | deeplearning.ai 检索（Document AI/新课程确认） | OK |
| 7 | docs.openclaw.ai/concepts/agents | dead（已知） |
| 8 | activepieces.com/docs/agents（1440 全） | OK |
| 9 | skills.sh/docs（434 全） | OK（与 r221A 重复面无新增量） |
| 10 | agentskills.io/specification（1797 全） | OK |

## 独点（4 个）
### B1：skillsmp p75 精选：复合逆境建模 / Time-Per-Hand 留存 / 基金申请六阶段（来源：skillsmp.com/skills/page/75，2026-09-25 实拉）
- **scenario-war-room（alirezarezvani/claude-skills ★26,225）**：**跨职能多变量 what-if 建模——与单假设压力测试不同，同时模拟所有业务职能叠加的复合逆境（compound adversity）；应对"what if X AND Y both happen?"**（复合情景建模面）。
- **kallaway-addictive-storytelling（Farrice）**：**神经化学留存工程——"自动售货机内容"（可预测、零多巴胺、观众离开）→"老虎机内容"（不确定结果、持续多巴胺、观众锁住）；Kallaway 四步成瘾循环（Stakes→Big Question→Head Fake→Rehook）；治理指标 Time-Per-Hand（两次多巴胺峰值间隔）**（内容留存的可测指标）。
- **inno-grant-proposal（OpenLAIR/dr-claw ★1,137）**：**基金申请六阶段工作流：profiling→planning→drafting→quality review→simulated peer review（模拟同行评审）→submission prep；覆盖美国 NSF/NIH/DOE/DARPA/NASA+中国 NSFC**。
- **job-post-builder（anthropics/knowledge-work-plugins ★25,304）**：**端到端招聘包——JD+结构化面试指南（含评分 rubric）+offer letter 模板，从 hiring brief 生成；不筛不排申请人**。
- **university-exam-prep（staruhub ★719）**：**强制先上传课本/PPT/考纲原始材料——没有材料无法辅导；苏格拉底式提问不灌输**（材料门槛纪律）。
- **提升层**：可复用 Skill / 工作流。

### B2：多向量检索原理与实测基准：ColBERT MaxSim / PLAID 量化 / ColPali 无 OCR 视觉检索（来源：langflow.org/blog/blog-nextplaid，2026-09-25 实拉）
- **单向量是有损摘要**：把整段嵌入 768/1536 维=压缩数百 token 概念到单点，强制平均语义细节——长/信息密集文档与视觉复杂文档（PDF 幻灯片/扫描海报，图/表/公式/布局）惩罚最重。
- **ColBERT late interaction**：文档索引为 token 矩阵 (n_tokens,dim)，查询也为矩阵；打分 MaxSim `score=Σ_{i∈q} max_{j∈d}(q_i·d_j)`——**每个查询 token 独立找文档内最佳匹配，不在折叠池化空间比较**。
- **ColPali 扩展图片**：视觉语言模型把页面图编码为 patch 嵌入矩阵，文本查询 token 矩阵与其 MaxSim——**查询可匹配文档中相关图表的 patch，全程无 OCR**。
- **PLAID 两优化**：①残差量化（token 嵌入 2-4bit/codebook，128 维 float32 512B→32-64B，索引可内存化）；②centroid 候选剪枝（扁平 IVF，查询 token 只探少量 cells n_ivf_probe，精确 MaxSim 只用于候选集 n_full_scores）——生产可部署延迟/存储。
- **NextPlaid=Rust PLAID index server**（LightOn 开发）：Axum REST API+MmapIndex+SQLite 元数据，Docker 起 8080+Swagger UI；`uv pip install lfx-nextplaid`+vLLM Multivector Embeddings（`vllm serve answerdotai/answerai-colbert-small-v1 --runner pooling --pooler-config '{"task":"token_embed"}'`）。
- **实测基准**：RealMMRAG-TechReport Recall@10——文本单向量 73.7→PLAID 94.7（+21）；图像单向量 22.6→PLAID 89.7（+67）。ViDoRe v3——图像 17.9→46.5（2.5 倍，无 OCR 流程）。
- **提升层**：工作流（多向量 RAG）/ 模型（检索质量）。

### B3：Dify Workflow Studio 生产化定位 + Activepieces Agent 概念面（来源：dify.ai/zh/workflows + activepieces.com/docs/agents，2026-09-25 实拉）
- **Dify Workflow=Harness**：**模型只是其中一个节点，真正让 Agent 可靠的是围绕它的 Workflow 体系**；**关键判断交给人**（敏感数据/访问权限/合规操作前暂停，专人审批/修改/评论/转交后再继续）；**追踪每一次运行**（检查节点输出/变量/执行路径/日志，事务可回溯到检索过程/模型调用/工具/用户/设备）；Workflow 与 Chatflow **共享同一节点库与执行模型**，区别只在触发方式与用户交互；Workflow=端到端一次跑完（自动化/批量/文档/后端流水线）。
- **Activepieces Agent=brief 而非 configure**：**用自然语言写 job、给访问所需 app 的权限，它每次运行自行读情况决定用哪些工具直到完成；同输入两次可不同处理（像同事）**；Flow vs Agent 决策表（逻辑写一次 vs 每次现算；知道流程用 Flow、工作多变用 Agent）；760+ pieces 任何动作变可调工具；答案基于文档/表格；flow 内作一步返回结构化数据；agent 属于一个 project（决定可达 connections/flows/files，移动时对话框告知会破坏什么）。
- **提升层**：工作流（编排平台构件模型）。

### B4：Agent Skills 规范细节 + OpenClaw 技能生态面（来源：agentskills.io/specification + OpenClaw 生态检索，2026-09-25 实拉）
- **frontmatter 字段约束**：`name` ≤64 字符、小写字母数字连字符、不得首尾连字符、**必须匹配父目录名**；`description` ≤1024 非空、描述"做什么+何时用"+关键词（"Helps with PDFs"是差例）；`license` 可选；`compatibility` ≤500 环境要求（intended product/系统包/网络）；`metadata` 任意 KV（key 尽量唯一防冲突）；`allowed-tools` 空格分隔预批工具（experimental，如 `Bash(git:*) Bash(jq:*) Read`）。
- **progressive disclosure 三段加载**：**元数据（~100 tokens）启动时全加载→指令（<5000 tokens 建议）激活时加载→资源按需加载；SKILL.md 保持 <500 行，详细参考拆到引用文件**（agent 激活后整文件加载——长文件=浪费上下文）。
- **文件引用一层深**：相对路径从 skill 根，避免深嵌套引用链；`skills-ref validate ./my-skill` 校验 frontmatter 与命名。
- **OpenClaw 生态面**：**GOG（Google Workspace CLI 单一集成 Gmail/Calendar/Drive/Contacts/Sheets/Docs，ClawHub 下载最多之一）；ClawHub 下载 Top：tavily-search ~23.8K/summarize ~22.4K/github ~21.6K；约三分之一 ClawHub 技能带安全风险（装前自查）**。
- **提升层**：可复用 Skill（规范约束）/ 工具（生态）。

## 判重说明
- B1 scenario-war-room/kallaway/inno-grant/job-post-builder 全新面，落。
- B2 与 r222-A A4（NextPlaid 简介）重叠>60% 含≥40% 增量（PLAID 量化/IVF/MaxSim 原理+实测基准）合并保留增量，落。
- B3 Dify Workflow Studio Harness/人审/追踪为生产化新面；Activepieces agent 概念面为 r221B 三构件互调增量，落。
- B4 specification 字段约束+progressive disclosure+skills-ref 为规范细节增量；GOG/ClawHub 生态面为工具面增量，落。
- 未落：skills.sh/docs（与 r221A 重复）、n8n how-memory（security 拦）、openclaw concepts/agents（死）、deeplearning AI Code Review（r220B 已落）。
