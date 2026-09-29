# r298B 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r297 + r298A。查询词与 r298A 及之前全错开（本轮=混合检索重排/版本控制备份/向量库RAG/模板AI采用/webhook数据存储/调度触发/提示缓存/供应链安全/Trending生态/RAG评估主题）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | Weighted Score 加权评分（语义相似度 vs 关键词匹配相对权重=调参旋钮）；Rerank 模型默认禁用显式开（第三方重打分 Cohere/bge-reranker，开启前配 API key）；多模态两段式（Embedding 粗召回+Reranking 精排）；Agentic RAG（Agent 节点=意图+工具编排+来源选择+重试） | 合并保留增量（r296C #10 两阶段检索 ANN+rerank，本点=Dify Weighted Score 权重+默认禁用+多模态） | 工作流 |
| 2 | n8n | n8n package 单文件（workflows+结构+引用，npm 包式跨实例导入导出）；CLI 历史版本导出（export:workflow --version=VERSION_ID）；GitHub 双向同步（只在 n8n→上传/只在 GitHub→创建/两边都有一时间戳比较同步最新）；智能去重提交（GitHub API 取 SHA 对比，没变跳过 commit 防污染历史）；环境路由（沙箱/生产按路径分流） | 独立落地（r296A #1 Dify YAML 版本化，本点=n8n 具体机制 package/双向同步/去重提交） | 工具 |
| 3 | Langflow | Vector Store RAG 双子流（Load Data 子流加载嵌入+Retriever 子流搜索，共享同一 store）；DB Providers 可配置后端（1.10：Chroma/Chroma Cloud/OpenSearch）；Multi-Vector Retrieval（1.11 lfx-nextplaid=ColBERT late interaction+ColPali 视觉检索）；Graph RAG 组件（GraphRetriever 图遍历） | 独立落地（r296C #3 记忆形态，本点=向量库/RAG 检索结构） | 工作流 |
| 4 | Activepieces | AI 两步模式：第一步 AI 理解输入→第二步 AI 生成回复→草稿发 Slack 人审→批准发邮件/打回修改；AI Adoption Stack（按部门策展模板库 HR/Finance/Marketing/Sales/Operations）；agent 共享知识库（文档可被每个 agent 搜索） | 独立落地（r297B #2 n8n Critic 评分循环，本点=Activepieces 模板化两步+人审批准细节） | 工作流 |
| 5 | Make | webhook 队列机制（场景 OFF 请求进队列/默认并行处理超限进队/无 response 模块报错）；Data Store 幂等去重模式（Search by key→Router：0 条处理+Add/有记录跳过）；清理例程（每周删 90 天前记录保持 lean）；webhook 数据结构定义（校验入站数据，无定义=接受一切）；快速响应（Webhook Response 前置防语音延迟） | 合并保留增量（r296C #8 webhook 场景，本点=队列机制+Data Store 查重+清理例程+结构校验） | 工作流 |
| 6 | Pipedream | 触发事件携带调度元数据（interval_seconds/cron/timestamp epoch/timezone_configured 格式化 datetime 随事件进下游）；cron vs interval 判据（要控星期几用 cron 完整表达，简单频率用 intervalSeconds）；组件 timer prop（$.interface.timer）；cron 按 UTC 存储时区显式调 | 合并保留增量（§cron 日周 OR 语义，本点=Pipedream 触发元数据+组件 timer） | 工作流 |
| 7 | Anthropic | 缓存 TTL 权衡（5 分钟默认：写 1.25x 输入价；1 小时可选：写 2x 但久热；缓存按内容寻址改 CLAUDE.md 即失效）；断点前块必须逐字节相同（思考配置+output_config.effort 调用间一致）；stable first variable last（稳定上下文开头：系统指令/背景/大上下文/常用工具定义）；over-retrieval 纯浪费（每查询都付，拼装后数 token 抓膨胀） | 合并保留增量（wb-context-compressor §token/缓存治理 1:5:0.1，本点=TTL 价格细节+断点规则+检索成本项） | 工具 |
| 8 | 供应链安全 | 真实攻击数据：ClawHavoc 2026 年 1-2 月入侵 OpenClaw 市场 1,200+ 恶意技能；Snyk ToxicSkills：36.82%（1,467 技能）至少一个缺陷、13.4% 关键级；静态扫描器四绕过（空白膨胀/预编译字节码/文档归档间接引用，Trail of Bits 4 小时内）；SkillSpector 两阶段（静态正则+AST→动态运行）；SkillDetonate 动态检出 97%（2% 假阳）比最佳静态高 31%；BIV 行为完整性（声明 vs 行为，跨元数据/代码/自然语言三表面）；五类风险（Prompt Injection/Data Exfiltration/Privilege Escalation/Supply Chain/Excessive Agency） | 合并保留增量（r298A #8 多源审计聚合，本点=供应链攻击事实+动态优于静态+BIV） | 工具 |
| 9 | GitHub | Hermes Agent 223K★（Nous Research 自改进 agent：学习循环）；GitHub Agentic Workflows（技术预览：coding agents 在仓库内建自动化）；趋势主线三：Claude Skills 风口（技能模块化周增 1万-12万）+Token 压缩&记忆（headroom/agentmemory/turbovec 周增 1万-14万）+Agent 安全治理（MXC/SkillSpector/agent-governance-toolkit）；安全跑 agent=趋势（smolvm 可嵌入可分支 VM 本地跑） | 独立落地（未落过 Hermes/Agentic Workflows） | 可复用 Skill |
| 10 | deeplearning | RAG Triad 三指标：Context Relevance（检索上下文相关性）+Groundedness（回答是否基于上下文防幻觉）+Answer Relevance（回答与问题相关）；sentence-window 检索+auto-merging 检索（基线之上两种高级检索）；内联评估（agent 运行中自评调整计划） | 合并保留增量（r297A #10 evals→error analysis，本点=RAG Triad 具体三指标） | 工作流 |

判重口径：增量判定。10 独点=4 独立+6 合并保留增量，零纯重复。