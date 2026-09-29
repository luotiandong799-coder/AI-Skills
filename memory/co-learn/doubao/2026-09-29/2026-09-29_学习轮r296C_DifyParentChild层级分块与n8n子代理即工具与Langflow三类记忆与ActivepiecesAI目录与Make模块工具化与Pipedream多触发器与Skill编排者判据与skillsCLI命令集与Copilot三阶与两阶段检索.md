# r296C 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r295 + r296A + r296B + 并行侧 r296 批（零重叠，其覆盖凭据/执行顺序/环境变量/超时/审计面）。查询词与 r296A（工作流/工具描述/组件生成/提示库/三特征/入站认证/评测/gh skill/位置约定/RAG自评）、r296B（部署/扩容/无头runtime/规模模型/raw body/组件API/四层结构/目录分级/worktree/评测课程）全错开（本轮=RAG分块/子代理/记忆/AI目录/Toolkit模块/触发器/最佳实践/CLI安装/Copilot三阶/两阶段检索主题）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | Parent-child Chunker 层级结构（双层层级：精确匹配+丰富上下文）/ 子块改写为关键词/摘要/用户常见查询（bridging query gap，LED 指示灯例）/ 分块参数按文档类型（技术密集 800 token+150 重叠 vs 中文 500 token 重叠 50-100 / 10-20%） | 合并保留增量（r295C 知识库不重摄取/r296A 中文分块，本点=Parent-child+子块改写） | 工作流 |
| 2 | n8n | 子代理即工具（AI Agent Tool 把第二个 agent 配成工具供第一个调用）/ **模板陷阱：Main Orchestrator+Sub-Agents 同视图不工作，必须拆独立 workflow 再更新 Workflow ID** / Thinking Space 可复用"草稿纸"子 workflow（收文本，多步推理工具化） | 合并保留增量（r295A 多智能体异构工具链，本点=sub-agent 工具化+草稿纸） | 工作流 |
| 3 | LangFlow | 三类记忆形态判据：Message History（按时间倒序取最近）/ Memory Base（1.10+ per-flow 向量存储，自动摄取对话，跨会话语义检索）/ Knowledge Base（手动填充）——用户期望跨会话连续性用 Memory Base，仅会话内用 buffer | 合并保留增量（r296A Assistant/r295C 知识库，本点=语义记忆形态） | 工具 |
| 4 | Activepieces | 763 pieces/5736 actions 全免费（含 free cloud+self-hosted）/ AI-ready 目录：Tool Search（按任务描述找 action，ap_search_actions）+AI metadata+Audience——目录为 AI agent 设计 | 合并保留增量（r296B 规模模型，本点=AI 目录改造） | 工具 |
| 5 | Make | AI Toolkit 9 预置模块（sentiment/categorize/extract/summarize/translate/identify language/standardize/chunk/request anything，无需写 prompt 无需第三方 AI 账户）/ 模块工具化：单模块直接作 agent 工具（vs 以前必须建 scenario 配输入输出）/ sub-agents as tools+工具输出过滤（2026-07） | 合并保留增量（r295C AI Toolkit+Playbook，本点=模块工具化+输出过滤） | 工具 |
| 6 | Pipedream | 一工作流多触发器（distinct events 都跑同一 workflow）/ custom domains（endpoint.yourdomain.com）/ this.http.respond()（快速响应 webhook）与 this.$emit()（发事件）职责分离+db.get/set 状态 | 合并保留增量（r295C $.send.http/r296B 组件 API，本点=多触发器+respond/emit 分离） | 工作流 |
| 7 | Anthropic | SKILL.md 是"编排者"不是"百科全书"（正文 <500 行，深度进 references/ 一级深，>100 行 reference 带目录）/ **确定性操作打包成脚本不给模型重新推导** / 目录结构 SKILL.md+scripts/+references/+assets/ | 合并保留增量（r295C frontmatter/r296B 四层结构，本点=编排者判据+脚本化） | 可复用 Skill |
| 8 | skills CLI | 四命令：npx skills find（搜索）/add（安装）/update（更新全部）/init（创建）/ **--skill 精确安装单个技能**（nvidia cuopt 例）/ packs 未列出集合一条命令装 / .zip 与 .skill 包安装 | 合并保留增量（r296A gh skill+版本钉定，本点=find/update 命令集+pack） | 工具 |
| 9 | Copilot | instructions/skills/agents 三阶区分（被动指令<单任务技能<完整工作风格——agents 定义 Copilot 怎么想/拿什么工具/怎么交流）/ **name 必须匹配父目录名，非法字符导致静默加载失败**（slash/colon/dot/namespace 禁用） | 合并保留增量（r296A 位置约定，本点=三阶区分+静默失败） | 可复用 Skill |
| 10 | deeplearning | 两阶段检索：ANN 粗召回（向量库）+reranking（cross-encoder/ColBERT）精排 / 高级 RAG：sentence-window 与 auto-merging 超 baseline / agentic RAG vs RAG vs fine-tuning 区分 / 生产模块：评测策略+日志监控可观测性 | 合并保留增量（r295C ColBERT/r296A 中文分块，本点=sentence-window/auto-merging+两阶段） | 工作流 |

判重口径：增量判定。本轮 10 合并保留增量，零纯重复。