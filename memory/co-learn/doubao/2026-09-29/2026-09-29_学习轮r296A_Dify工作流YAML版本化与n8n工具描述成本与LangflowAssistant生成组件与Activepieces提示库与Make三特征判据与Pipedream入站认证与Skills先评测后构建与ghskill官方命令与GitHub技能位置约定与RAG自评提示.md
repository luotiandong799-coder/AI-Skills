# r296A 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r295 全量（含 r295A/B/C 30 独点 + WorkBuddy r294 续作）。查询词与 r295 三轮全错开（本轮=工作流最佳实践/生产部署/组件开发教程/workflow 教程/场景入门/triggers 步骤/最佳实践集成/CLI 教程/agent skills 仓库/课程评估主题）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | 工作流导出 YAML→Git 版本控制+diff 部署差异+tracing API 逐步回放历史执行 / 节点级失败行为三选项（停止·返回类型化默认值·走失败分支）/ v1.3+ 嵌套 agent 节点（一个 agent 调另一个作工具） | 合并保留增量（r295A 多智能体，本点=YAML 版本化+失败三选项） | 工具 |
| 2 | n8n | 工具描述 token 成本思维（每加一个工具=每次请求加 token，15 工具只用 3 个→拆专注 agent）/ 分类与生成模型分工（Haiku 分类约便宜 10x+Sonnet 生成）/ Boring Reliability 全量日志（存 input/decision/model/cost/approval） | 合并保留增量（r295B 混合管道，本点=工具描述成本+模型分工+全量日志） | 工作流 |
| 3 | LangFlow | Langflow Assistant（1.10.0）提示词直接生成自定义组件代码（模型驱动建组件）/ aMap 组件逐行 LLM 数据变换（自然语言指令+输出 schema，并发批次默认 10，token 随行数线性） | 合并保留增量（r295B 组件管控，本点=组件生成+逐行变换） | 工具 |
| 4 | Activepieces | 提示库（tables 版本化提示模板+流内引用+验证步骤强制输入+日志记 prompt ID 审计）/ 错误捕获中央表（payload/step/correlation ID）+通知+人工分诊+从最后 checkpoint 恢复 / 版本审批提升+失败阈值自动回滚 | 合并保留增量（r295C 错误分诊，本点=correlation ID+checkpoint 恢复+提示库） | 工作流 |
| 5 | Make | AI 自动化候选三特征判据（运行≥10 次/周+现在需人工读自由文本+输出结构化，占二即候选）/ Make 作 MCP client（AI 模块连 CRM MCP server 工具，自动决定调哪个） | 合并保留增量（r295C AI Toolkit/r295A Maia，本点=三特征判据+MCP client） | 工具 |
| 6 | Pipedream | Connect 终用户认证：公开 HTTP webhook 不认证=任何人可触发，强烈推荐创建 Pipedream OAuth client 认证入站请求 | 合并保留增量（r295C 触发面，本点=入站认证安全） | 工具 |
| 7 | Agent Skills | 先评测后构建（代表性任务上跑 agent 观察挣扎点→增量建技能补短板）/ SKILL.md 膨胀拆多文件引用+互斥或极少同用上下文分开路径减 token / metadata 渐进披露（先 ~100 token 判断相关性，全量 body 触发才加载） | 合并保留增量（r295A 评测/r295C 规范，本点=评测驱动建技能+渐进披露） | 可复用 Skill |
| 8 | skills.sh | gh skill（GitHub CLI 2026-04-16 官方命令）发现/安装/管理/发布 / localskills npm 风格版本钉定（my-skill@1.2.3 exact 与 ^ 范围）/ find/add/check/update 完整命令面 | 合并保留增量（r295B/C CLI，本点=gh skill+版本钉定） | 可复用 Skill |
| 9 | GitHub | 官方技能位置约定（项目=.github/skills 或 .claude/skills 或 .agents/skills；个人=~/.copilot/skills 或 ~/.agents/skills）/ GitSkills 数据集（2026-07 抓 3,797,117 个 SKILL.md/282,200 仓库） | 合并保留增量（r295B 生态盘点，本点=位置约定+数据集） | 可复用 Skill |
| 10 | deeplearning | RAG 自评提示三要素（显式逐步推理格式+检索信息必需置信度评分+搜索结果质量结构化分析，混合检索+自评达 72.7% pass）/ 工具描述单条 ≤200 字量纲 / 中文分块通用 512 字符技术 256 字符重叠 10-20% 口径 | 合并保留增量（r295C 分块 800-token，本点=中文字符口径+自评三要素） | 工作流 |

判重口径：增量判定。本轮 10 合并保留增量，零纯重复。