# r293B 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r293A 全表。查询词与既往全错开（本轮=知识库生产、子工作流、Agent组件、MCP接入、迭代聚合、HTTP响应、Skills官方仓库、发布规范、编码工具评测、Agent课程）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | Summary Index（1.12.0 chunk 摘要自动生成+人工审核，摘要质量直接影响检索）/ Rerank 模型适配坑（OpenAI 无 Rerank、腾讯混元/部分 DeepSeek 有 bug） | 合并保留增量（r291B/r292A 知识库，本点=Summary Index+Rerank 坑） | 工具 |
| 2 | n8n | 子工作流体系（Execute Sub-workflow 4 调用方式/Sub-workflow Trigger 首节点/sub-workflow conversion 自动重构/嵌套循环子工作流绕行/并行+wait-for-all 模式） | 合并保留增量（r291A n8n，本点=子工作流面） | 工作流 |
| 3 | LangFlow | Agentics bundle（aMap 逐行填列/aReduce 行折叠/aGenerate 合成行——LLM 表格数据变换）/ Guardrails 组件（LLM 验证 flows） | 合并保留增量（r292B extension/bundles，本点=Agentics+Guardrails） | 工具 |
| 4 | Activepieces | 单 URL 全 piece MCP server（一个 URL 暴露所有已连接 piece）/ Embeddable MCP（authRequestId→code→token 授权流） | 合并保留增量（r292A Webhook/r292C 嵌入，本点=单URL MCP） | 工具 |
| 5 | Make | Array Aggregator 三陷阱（作用域不闭合→聚合器后模块每迭代跑一次/嵌套迭代 row 上下文丢失/仅部分 Router 分支数据进聚合） | 合并保留增量（r292A 错误语义/r293A 模板，本点=聚合器陷阱） | 工作流 |
| 6 | Pipedream | HTTP 响应自定义驱动重试（配非 200 响应让 QStash 重试）/ 自定义域名端点（endpoint.yourdomain）/ $.respond | 合并保留增量（r292B/C Pipedream，本点=HTTP 响应面） | 工具 |
| 7 | Anthropic | 官方 skills 仓库三区结构（skills 示例/spec 规范/template 模板）/ foundational skills（文档/表格/PPT/PDF）/ .claude/skills 随 repo 版本化+Skills API 自动拾取 | 合并保留增量（r291A 注入/r292A Skills，本点=仓库结构+随版本化） | 可复用 Skill |
| 8 | skills.sh | description=progressive disclosure 触发开关（每轮只读 description 决定加载哪个 body）/ name kebab-case 规范 / find-skills 三标准（1K+ 安装/官方来源/star 检查） | 合并保留增量（r292A 遥测/r293A CLI，本点=发布规范） | 可复用 Skill |
| 9 | GitHub | Copilot agent 模式+agentic code review（2026-03 GA）/ Claude Code vs Copilot 定位（IDE 生态玩家 vs 终端自主专家） | 合并保留增量（r293A 框架选型，本点=编码工具评测） | 工具 |
| 10 | deeplearning.ai | Agent Memory 课（长期记忆=外部持久结构化基础设施）/ Generative UI 课（agent 生成图表/表单/白板）/ Agent Skills with Anthropic（开放标准跨 agent 部署） | 合并保留增量（r292A 四模式/r293A 新课，本点=记忆工程+GenUI） | 可复用 Skill |

判重口径：增量判定。本轮 10 合并保留增量（每点均含≥40% 独有增量），零纯重复。