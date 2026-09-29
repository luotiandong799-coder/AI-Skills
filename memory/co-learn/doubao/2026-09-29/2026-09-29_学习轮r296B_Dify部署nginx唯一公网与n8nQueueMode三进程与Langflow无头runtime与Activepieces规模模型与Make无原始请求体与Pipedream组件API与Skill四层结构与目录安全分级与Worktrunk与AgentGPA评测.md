# r296B 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r295 + r296A + 并行侧 r296 批（WB 自有信源，覆盖凭据/执行顺序/环境变量/超时/审计面，与本轮零重叠）。查询词与 r296A 及 r295 三轮全错开（本轮=部署/生产/部署/自托管/安全/组件开发/编写示例/目录生态/trending/评测课程主题）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | 部署架构：nginx 是唯一需公网暴露的容器（八服务+init_permissions 一次性任务）/ 生产资源文档 2vCPU/4GB 实际给 8GB+headroom / 多阶段构建非 root 用户 dify(UID 1001) | 合并保留增量（r295A LangFlow 生产安全基线，本点=Dify 部署形态） | 工具 |
| 2 | n8n | Queue Mode 三进程职责（n8n start 管 UI/API/webhook + n8n worker --concurrency=10 管执行 + 可选 n8n webhook 专用高吞吐端点）/ N8N_DATA_TABLES_MAX_SIZE_BYTES 默认 50MB 是安全帽非能力上限（Postgres 几 GB 可行，设数据卷 25%）/ SaaS 扩展：拆集群（用户触发 vs 长跑 AI）+缓存模型输出+per-user 限流 | 合并保留增量（r295B 环境隔离，本点=queue 扩容+上限语义） | 工具 |
| 3 | LangFlow | 生产部署：无头 runtime（LANGFLOW_BACKEND_ONLY headless 只跑 API）与 IDE 分离 / 多 worker 参数（LANGFLOW_WORKERS>1+GUNICORN_PRELOAD=true+JOB_QUEUE_TYPE=redis，共享 postgres）/ 生产最低 2Gi RAM+1 CPU×3 副本，外部 PostgreSQL 强推 | 合并保留增量（r295A 安全基线，本点=部署形态+多 worker） | 工具 |
| 4 | Activepieces | 规模模型：workers=峰值并发 flows（每 worker 单 flow，concurrency 1）+apps=ceil(workers/10)（1:10 比例）/ 50 并发=50 workers+5 apps，Redis 溢出队列 / Postgres CPU 跟踪吞吐——加 worker 时共享层要一起涨 | 合并保留增量（r295C 构建三要素，本点=部署规模模型） | 工具 |
| 5 | Make | webhook 默认公开 URL 无认证→两类事故（工作流洪水+数据注入）；缓解=x-make-apikey 自定义头 / **Make 不暴露原始请求体→平台内 HMAC 验证不可行**（toString 重序列化不还原原始字节），验证端点走 Worker 模式 / Meta 验证：返回 hub.challenge 原始字符串（无引号无 JSON）+Content-Type text/plain+3 秒内 | 合并保留增量（r296A Pipedream 入站认证，本点=Make 特有 raw body 判据+Meta challenge） | 工具 |
| 6 | Pipedream | 组件 API 结构：name/key/type/version/description/props/methods/hooks(activate/deactivate/deploy)/dedupe/run / Sources 可本地部署 vs Actions 仅发布 / dedupe 策略 unique（去重所有重复）与 greatest（保最大） | 全新增量（组件开发面此前未拉） | 工具 |
| 7 | SKILL.md | description 好坏对比判据：烂"Helps with PDF files" vs 好"Extract text and tables...Use when...handles page parsing, table detection"——要具体+pushy+触发词 / 渐进披露四层结构（L1 Overview 简要+L2 Quick Start 常见用例+L3 Details 逐步+L4 Reference 外链高级内容） | 合并保留增量（r295C frontmatter 硬约束，本点=四层结构+description 判据） | 可复用 Skill |
| 8 | 技能目录 | 目录安全分级：SkillsMP（~190 万技能，从 GitHub 抓取，**无审查——安装前自行检查**）vs SkillHub（7000+，AI 评估）vs Agensi（人工审查+8 点安全扫描）vs Anthropic（人工策展）/ ClawHub 向量搜索注册表（按语义相似性找技能）/ OpenAI 转变：开放目录→托管 Plugin Directory（开放吸引贡献、托管捕获分发、一厂策展控制发现） | 合并保留增量（r295B 生态盘点，本点=安全分级） | 可复用 Skill |
| 9 | GitHub trending | Worktrunk（max-sixty）：面向并行 AI Agent 的 Git worktree 管理 CLI——多 agent 并行时 worktree 隔离 / Humanizer（blader）52.5K★ 抹 AI 写作痕迹 Agent 技能 / Anthropic 发布 36 个生物学模型 speedup kits | 合并保留增量（r295B 输出形态技能霸榜，本点=Worktrunk+biology kits） | 工具 |
| 10 | deeplearning | Evaluating AI Agents 三步：observability（看步骤/调试）→组件评测（code-based vs LLM-as-a-Judge 评测器选择+指标）→组织成实验迭代 / "Measure Agent's GPA" 给 agent 打 GPA 量纲 / 视频生成评测三方法（SigLIP 图像-文本相似度数值打分+LLM judge 自定义标准+结构化 rubric） | 合并保留增量（r295A 评测八层，本点=评测器选择+实验组织） | 工作流 |

判重口径：增量判定。本轮 10 合并保留增量，零纯重复。