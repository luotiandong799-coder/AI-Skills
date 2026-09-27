# r233-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify docs（indexing-methods/knowledge-pipeline） | ✓ | 双索引方法（High-Quality 语义 vs Economical 每块 10 关键词倒排零 token 成本）、Summaries 桥接查询-内容差距、Parent-child Chunker 双层结构、Q&A Processor |
| 2 | n8n docs（sharing/projects） | ✓ | Projects 隔离单元（workflow/credentials/data/variables/execution history 一起隔离）、自定义项目角色+SSO 用户供给、external secret store+log streaming |
| 3 | LangFlow（vector-stores dead→search 补） | ✓ | Vector store 配置参数化（search_type similarity/mmr、distance_metric l2/cosine/ip）、RAG 分块实证（简单方案赢） |
| 4 | Activepieces docs（subflows/mcp tools） | ✓ | Child flows（execute_flow 父传数据等子完成取子输出）、Stream CSV to Subflow（分批不整载内存）、Tables 存工作流状态（dedupe keys/approval status 跨 run） |
| 5 | Make（scenario settings/data store） | ✓ | Scenario recovery 自动蓝图备份、Data store 三操作架构（读→AI→写）、时间窗去重清理（processed_at+定时删）、场景 JSON 导出 Git 备份 |
| 6 | Pipedream docs（security/components api） | ✓ | secret props vs env vars 边界（组件不能用环境变量）、Connect dev/prod 双环境隔离、app prop 驼峰引用 |
| 7 | Anthropic（prompt caching 官方+blog） | ✓ | 缓存五则（前缀序 tools→system→messages/断点最后稳定块/messages 不用 system/不中途换工具模型/监控 hit rate 像 uptime）、成本数字（读 0.1x 写 2x、90% hit→$100 变 $19） |
| 8 | skills.sh hot tab | ✓ | Leaderboard 实拉（find-skills 3.6M 居首，mattpocock 4.2M 总量最大），无新内容 |
| 9 | 腾讯 SkillHub（search） | ✓ | TRACE 评测体系五维评估 7万+ Skill（从看描述到看真实效果）、TOP50 三重保障、全量安全扫描识别 Prompt 投毒/恶意代码、ZIP 自定义导入 |
| 10 | GitHub 生态（search：trending AI 标签） | ✓ | TencentDB Agent Memory（agent 专业记忆库 Trending 榜首）、hermes-agent 249k、andrej-karpathy-skills 215k（单 CLAUDE.md 改行为）、mem0 自编辑记忆消重 |

## 判重基准
双键检索（来源标识+概念词）：双索引/Summaries 桥接、分块实证/决策矩阵、Project 隔离、缓存工程/前缀命中——均无同类已有落地。缓存与用户偏好"改配置/换模型破坏前缀缓存应重开会话"部分重叠，但五则+断点位置+成本数字为 ≥40% 独有增量，合并落地。

## 独点落地（4 个，全部真独点）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① 双索引方法+Summaries 桥接 | High-Quality vs Economical（10 关键词倒排零成本）；摘要作浓缩语义层桥接查询-内容差距 | 工具/工作流 | wb-execute-discipline |
| ② 分块实证+决策矩阵 | 512 token 固定大小常赢；structural→hierarchical 决策矩阵；三大错误（>1000/零重叠/切中间） | 工作流 | wb-execute-discipline |
| ③ Project 级隔离单元 | workflow/credentials/data/variables/execution history 同界隔离；自定义角色+SSO 跟项目走 | 工作流 | wb-execute-discipline |
| ④ 缓存工程五则+成本 | 前缀序 tools→system→messages、断点最后稳定块、messages 不用 system、不中途换工具模型、hit rate 监控；读 0.1x 写 2x | 工具/工作流 | wb-execute-discipline |

## 复核
- 无编造凑数：四独点均有当日实拉原文来源。
- 功能套件检查：wb-max-token-saver 与 ④ 缓存成本直接互补（成本层）；wb-context-compressor 与 ①② RAG 内容互补；wb-ponytail 无新增归属。
- 垃圾：未产生临时文件。
