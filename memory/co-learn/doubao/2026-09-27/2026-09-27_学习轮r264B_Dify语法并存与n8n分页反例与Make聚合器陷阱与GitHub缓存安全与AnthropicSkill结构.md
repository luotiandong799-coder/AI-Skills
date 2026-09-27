# r264B 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站，查询词与 r263 三轮+r264A 全错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（模板语法面） | ✓ | **LLM 节点支持 Jinja2 模式**（edition_type: "jinja2"）：循环/条件/复杂数据转换；**四套上下文语法并存**：prompt templates `{{#node.field#}}` / Jinja2 `{{ node.field }}` / system variables `sys.*` / environment `env.*` / conversation `{var}`；Template 节点编程式能力（loops/conditionals/filters、dot notation 嵌套、if-else）；**旧记法混用陷阱**（错 `{{#conversation.user_name#}}` → 正 `{{ conversation.user_name }}`）；错误重试最大次数+间隔、异常处理备用分支 |
| 2 | n8n（HTTP 分页面） | ✓ | **内置分页 Add Option > Pagination**；Response Contains Next URL 模式（$response.body.nextLink）；**$pageCount 计数器**（Update a Parameter in Each Request 设 page={{ $pageCount }}，Complete Expression 判停）；**关键反例**：内置分页 Retry on Fail 从第 1 页重跑整节点、已拉数据丢弃→可靠修复=关内置分页手动循环（每页独立请求）；**嵌套 URL-encoded JSON body 的 pageNumber 内置分页够不到**（需动态构建 RequestBody）；Shopify cursor 分页在 response headers（启用 Include Response Headers and Status） |
| 3 | LangFlow（组件端口面） | ✓ | **端口=连接点，承载数据类型**（从字段/端口颜色推断：message=蓝/JSON 对象）；**同类型（同色）输出连输入**；**Tool Mode 把组件变工具**（组件获得 Toolset 端口，连 Agent 的 Tools 端口）；MCP Tools 组件连 Agent Tools 端口；DataFrame/Table 端口只连 DataFrameInput；Astra DB 专用 Vector Store Connection 输出只连 Graph RAG 输入 |
| 4 | Activepieces（数据映射面） | ✓ | **switch() 查找映射**（switch(country_code;"US";"North America";...)）；JSON path `{{step_name['output']['path']}}` + **右键 Copy reference**；公式参考（get_day_of_week/convert_timezone）；**数组操作 JS 语法**（map/filter/reduce/items[0]/length）；**outputSchema 驱动 Smart Output Viewer+Data Selector**（可读标签，不改变表达式路径）；数据同步（AI 映射字段/检测不匹配/校验 schema 兼容/冲突自动处理） |
| 5 | Make（聚合器面） | ✓ | Iterator 拆单 bundle 数组→N bundles；Aggregator 反向合并；**Array Aggregator 批量插入**（迭代 20 行→聚合→批量入库）；**已知陷阱**：Router 多分支时 Aggregator 只含一个 route 的 items（社区 113679）；**对象游标分页**（Dre Dyson）：内置分页对 object cursor 失败→Data Store 存 cursor+filter 判退出循环；flatten(map(map(map(...)))) 嵌套展开 |
| 6 | Pipedream（Python code step 面） | ✓ | **def handler(pd) 结构**（pd.steps 引用前步/pd.inputs 配置）；**标准计划 30 秒执行超时**→500+ 条分两步（fetch 存 raw+aggregate）；**Data Store TTL**（set 第三参数秒）；warm workers 减启动；自定义 components 私有复用；try/catch+自动重试 transient；$.export 跨步传数据 |
| 7 | Anthropic Skills（仓库结构面） | ✓ | **skill 目录解剖**：SKILL.md 必填（YAML frontmatter+instructions）/scripts 可选可执行/references 可选按需加载/assets 可选模板；**frontmatter 仅 name+description 必填**，description 决定何时调用；**级别优先级**（enterprise > personal > project；plugin /skills/）；**ZIP 导入根结构**（my-skill.zip 内 my-skill/ 根，resources/ 同级；错误=文件直接放 ZIP 根）；skills=可复用 agent workflows 不是更多 prompts（团队约定进版本控制/可发现） |
| 8 | GitHub Actions（缓存面） | ✓ | **缓存安全**：缓存可能被修改→恶意代码执行风险；**任何人能开 PR 就能读 base branch 缓存**——不存 secrets/tokens/credentials；**key 设计=整个游戏**（hashFiles lockfile；runner.os+包管理器+语言版本+锁文件哈希）；**restore-keys 前缀回退**（精确 key→前缀→restore-keys→跨分支再试）；setup-* 动作 cache input 自动管理常见包管理器；cache poisoning 防护（least-privilege workflows/cache-mode） |
| 9 | OpenClaw（CLI 参考面） | ✓ | 命令分区：Reset/backup/migration（backup·database·migrate·reset·uninstall·update）/Messaging-agents（message·agent·agents·claws·attach·acp·mcp）/Config（setup·onboard·configure·doctor·dashboard）/Health-sessions（status·health·sessions·audit）/Gateway-logs（gateway·logs·system）/Runtime-sandbox（approvals·exec-policy·sandbox·tui·browser）/worktrees；**exit codes**（0=成功/1=无匹配或 substrate 拒绝/2=参数或解析错误）；**package validate**（ClawHub Plugin Inspector 离线静态校验，hard errors 非零退出）；nodes pairing（pending/approve/reject/remove/rename）；system 命令（--mode now\|next-heartbeat/--session-key） |
| 10 | 阿里云百炼（智能体应用面） | ✓ | **智能体核心能力**（知识库 RAG/插件：代码执行·图像生成·天气查询/引导工具使用）；**三种应用模式选型**（对话/智能体 Agent 2.0 推荐 vs Agent 1.0）；**Managed Agents 4 步**（配置基本信息/模型/工具，预填模板）；**分享发布四方式**（魔笔/钉钉/微信/发布为组件）；**Spring AI Alibaba 集成**（dashscope agent app-id/api-key/workspace-id）；0 代码知识问答（千问-Max）；案例（电商客服/高德 MCP 旅行规划/MineMind 智矿） |

## 判重基准
双键检索：Dify 语法（§6288 变量作用域管生命周期/§6175 并行聚合管编排——四套语法并存+Jinja2 混用陷阱为新面）；n8n 分页（无分页章节——新面）；Make 聚合器（§6275 性能优化已落"聚合器+bulk 省钱"——Router 多分支丢数据陷阱+对象游标 Data Store 分页为增量合并）；GitHub Actions 缓存（§6309 Agentic Workflows 为 Markdown 自动化另一面——缓存安全+key 设计新面）；Anthropic skills 结构（§6042 Copilot Agent Skills 规格为 Copilot 侧——Anthropic 仓库解剖+ZIP 导入根结构新面）。备选并入记录：Pipedream Python code step 30s 超时+Data Store TTL（合并 §6129 code step 面）、OpenClaw CLI exit codes（合并 r264A CLI 面）。

## 独点落地（5 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r264B-1 | wb-execute-discipline | 3.20.0+ | Dify 四套上下文语法并存与 Jinja2 混用陷阱 | 提示工程/工作流 |
| r264B-2 | wb-execute-discipline | 3.20.0+ | n8n HTTP 分页反例与手动分页 | 工作流 |
| r264B-3 | wb-execute-discipline | 3.20.0+ | Make 聚合器丢数据陷阱与对象游标分页 | 工作流 |
| r264B-4 | wb-execute-discipline | 3.20.0+ | GitHub Actions 缓存安全与 key 设计 | 工具/工作流 |
| r264B-5 | wb-execute-discipline | 3.20.0+ | Anthropic skills 仓库结构与 ZIP 导入 | 可复用 Skill |

## 复核
五独点均有当日实拉来源（逐站 URL 见各站摘要）；r264B-3 按增量判定合并保留增量；r264B-1/2/4/5 新面；备选并入记录不单独落地。垃圾：本轮未产生临时文件。
