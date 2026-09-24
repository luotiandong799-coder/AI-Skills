# 学习轮 r204-C：Anthropic skills机制细则与n8n三桶架构与SKILL规范硬约束与对抗验收补洞与Dify LastRun增量（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.anthropic.com/en/docs/claude-code/skills（全文 8135 两段） | OK（skills 全字段机制） |
| 2 | skillsmp.com/skills/page/20（全文 12769 三段，#1901-1993） | OK（93 项） |
| 3 | dify.ai/blog/dify-1-5-0-real-time-workflow-debugging（6588/13429） | OK（Last Run/Variable Handoff/Old vs New） |
| 4 | docs.pipedream.com/connect/ | OK（1281 字：managed auth/Connect proxy） |
| 5 | docs.langflow.org/quickstart | 死链 |
| 6 | blog.n8n.io/production-ai-playbook-complex-agent-patterns/（3273/19237 首段） | OK（Complexity Cliff/三桶） |
| 7 | help.make.com/en/help/scenarios/best-practices | 死链 |
| 8 | general_search n8n agent memory | OK（Session ID/immutable ledgers） |
| 9 | general_search SKILL.md 规范 | OK（agentskills.io 规范硬约束） |
| 10 | waytoagi.com/（首页 3149） | OK（工具导航壳） |

## 独点（5 个）
### P1：Anthropic skills 机制细则：bundled skills 并行编排 / invocation 双字段 / 动态上下文注入 / Skill 权限三法 / description 预算 2%（来源：docs.anthropic.com/en/docs/claude-code/skills，r202 技能机制的深度增量）
- **bundled skills 5 个**：`/batch`（调研→拆 5-30 独立单元→每单元一个后台 agent 在隔离 git worktree 实现+跑测试+开 PR）；`/simplify`（**三 review agent 并行**审查最近改动→聚合→修复）；`/loop [interval]`（轮询部署/babysit PR）；`/claude-api`（按语言加载 API 参考，import anthropic 自动激活）；`/debug`（读会话调试日志）。
- **invocation 双字段**：`disable-model-invocation: true`=只有人能调用（副作用操作 /deploy//commit）；`user-invocable: false`=只有 Claude 能调用（背景知识）；default 双方都可。
- **dynamic context injection**：``!`command` `` 语法在 skill 内容发给 Claude **之前**跑 shell 命令，输出替换占位符——Claude 只看到最终数据，预处理不是 Claude 执行。
- **Skill 权限三法**：/permissions deny `Skill` 全禁；permission rules `Skill(name)` 精确/`Skill(name *)` 前缀允许或拒绝；disable-model-invocation 把 skill 从上下文移除。built-in commands（/compact//init）不走 Skill tool。
- **description 上下文预算**：所有 skill 的 description 常驻上下文，**预算动态=上下文窗口的 2%**——技能一多就会超预算，是"技能库膨胀"的量化硬边界。
- **其余**：`$ARGUMENTS`/`$ARGUMENTS[N]`/`$N` 参数替换；`context: fork` 让 skill 在子代理跑（内容成为子代理 prompt）；`agent` 字段选 Explore/Plan/general-purpose 或自定义；`allowed-tools` 免每次确认；`ultrathink` 关键词启用扩展思考；SKILL.md <500 行，细节挪 supporting files；visual output 模式=捆绑脚本干重活+Claude 做编排（codebase visualizer 例）。
- 判据：**技能库是上下文资产**——description 预算 2% 动态上限决定能装多少个技能；有副作用流程用 disable-model-invocation 防 Claude 自作主张。
- **提升层**：可复用 Skill / 工作流。

### P2：n8n 生产多 agent 架构：Complexity Cliff / 分解→两问→三桶 / Session ID 记忆连续性 / immutable ledgers（来源：blog.n8n.io/production-ai-playbook-complex-agent-patterns + n8n blog AI Agent Memory，与 wb-execute-discipline 多 Agent 决策树互补——那条管"何时拆"，本条管"拆后怎么归类与记忆"）
- **Complexity Cliff（复杂性悬崖）**：单 agent 完美→加第二第三→无人想周五调试。根因不是多 agent 本身脆弱，是**按原型方式增量堆积、没有架构兜底**；修复=架构纪律（clear boundaries/explicit interfaces/isolated failure domains/每块独立可测），不是 prompt 纪律。
- **分解→两问→三桶**：先分解目标为子任务，每子任务两问：①需要 LLM 吗（不需要→DETERMINISTIC：DB lookup/Switch/HTTP/regex）②需要自己的 agent 吗（不需要→LLM CHAIN：单 prompt in-out；需要→AGENT：多步推理+工具+动态决策）。**AGENT 是最重工具，只给真正需要的子任务**——示例蓝本：2 deterministic + 3 LLM chains + 1 agent，只有 1 块真需要 agent。
- **Session ID 是多 agent 记忆的关键**：默认每次执行独立 session；**共享 session ID**→orchestrator 与 specialist 共享对话历史（委托连续性）；**隔离 session ID**→各自历史（并行隔离）。
- **immutable ledgers 持久上下文**：LLM 无状态，上下文写持久存储，架构成**不可变账本：agents 可写可读、不可改删**；长跑 agent 可 tear down session，下次从 durable artifacts 重建。
- 判据：**先分解再选工具**——agent 是工具箱里最重的一件；记忆连续性靠 session ID 显式声明，不靠默认。
- **提升层**：工作流 / Agent 编排。

### P3：SKILL.md 开放标准硬约束：name 64 字符+保留词禁入+目录名匹配+gerund 命名 / description 是路由唯一可见元数据 / 未知 frontmatter 键忽略保可移植（来源：agentskills.io/specification + bcgov spec + addyosmani skill-anatomy）
- **name 硬约束**：1-64 字符、小写字母数字+连字符、不得前后或连续连字符、**不得含保留词 anthropic/claude**、必须匹配父目录名；**prefer gerund 命名**（动词-ing，如 pdf-processing 是名目但建议 doing-形式表达动作）。
- **description 硬约束**：≤1024 字符、非空、描述"做什么+何时用"；**description 是 agent 路由时唯一可见的元数据**（skill 内容只在调用时加载）——路由质量=description 质量。
- **可移植性规则**：spec 兼容运行时**忽略不认识的 frontmatter 键**——加自定义键不破坏跨 agent 可移植；license/compatibility 可选（≤500 字符）。
- 判据：**name 是标识符不是标题**——带保留词/不对齐目录名会让 skill 失效；description 是路由的唯一入口。
- **提升层**：可复用 Skill（作者规范）。

### P4：对抗性验收补洞 find-gaps + NL 生成可导入工作流 DSL + 四声议事 council（来源：skillsmp p20：#1990 find-gaps / #1961 dify-workflow / #1986 council）
- **find-gaps**：对抗性审查**已有文档工件**（故事/计划/验收标准/spec/设计 mock）——找缺状态、未处理边界、未声明假设、不可验证标准、过宽切片；**交互式一次一问，把每个答案写回工件成为新验收标准/计划更新**。requires an artifact（没有工件就用 grill-me/specification 先建）。
- **dify-workflow**：自然语言→**可导入的 Dify workflow DSL**（YAML/JSON，含正确 node schemas/edges/layout）——NL 直接产可导入工作流定义。
- **council（四声议事）**：模糊决定/tradeoff/go-no-go 时召集 4 个声音，选择前做结构化异议——决策对抗机制。
- 判据：**补洞要写回工件**，不是口头列问题；**产出要可导入**才闭环；**决策前必须有结构化异议**。
- **提升层**：工作流 / 工具 / 可复用 Skill。

### P5：Dify 1.5.0 Last Run 飞行记录仪 + Variable Handoff（r204-B O3 的深度增量，重叠>60% 含≥40% 独有增量按判重规则合并落地）
- **Last Run**：每个节点自动保存**最后一次成功执行**的 inputs/outputs/metadata——节点级黑匣子飞行记录仪，调试有可追溯证据。
- **Variable Handoff**：变量面板持有数据即可直接跑该节点，系统自动抓依赖——**像 Jupyter 单元格**：任选节点 run，工作流处理全部数据关系。
- **Old Way vs New Way**：旧=侦探式（翻 run history 逐节点查→改→全重跑或手动敲中间输出→再查循环）；新=run once 全存→变量面板一眼定位（真实案例：template 丢知识库内容而 Exa 正常，面板直接看出 template 输出缺 KB 段）→精确修→单节点重跑下游。多轮调试省时间省 API 成本。
- 判据：**每个节点都有飞行记录**；**修一个节点不重跑昂贵上游**。
- **提升层**：工具 / 工作流。

## 判重说明
- P1 → r202 已有技能触发评测；"bundled 并行编排/invocation 双字段/动态注入/权限三法/description 预算 2%"为独有增量，落。
- P2 → wb-execute-discipline 多 Agent 决策树已录"单 agent 能干的别拆"；"三桶归类+两问决策+session ID 共享/隔离+immutable ledgers"为精确增量，落。
- P3 → 无既有规范记录，全独点，落。
- P4 → find-gaps 与豆包 grill-me 互补（grill-me 管"动手前对齐"，find-gaps 管"已有工件补洞写回"）；dify-workflow/council 无既有记录，落。
- P5 → r204-B O3 同源，按增量判定合并（Last Run/Variable Handoff/New Way 为独有增量），落为合并记录。
- 未落：ponytail-gain（家族重复）、watch（video-extract 重叠）、humanizer（human-signal 已有）、grillme/c-drive-cleaner/dramake（豆包套件已有）、us-stock-prediction（stock 套件已有但五维框架增量不足）、hands-on-deck/sci-ppt/dashiai（PPT 套件重复）、make best-practices 死链。
