# 学习轮 r231C：Dify循环选型与n8n三阶段节点组与Make错误五指令与技能最佳实践三件套与工具描述即prompt（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/97（#9601-9637） | OK |
| 2 | Dify（变量作用域四类/迭代 30 元素上限/Loop vs Iteration/跨轮引用会话变量） | OK |
| 3 | n8n（Call n8n Workflow Tool/agent-as-tool/hub-and-spoke/三阶段节点组/群组工具进 sub-workflow） | OK |
| 4 | LangFlow（1.11 HITL stateful checkpoint/A2A 协议/Policies 自然语言规则转 guarded tools/Agentics aMap 表格数据） | OK |
| 5 | Activepieces（错误类型 STEP/TIMEOUT/SANDBOX/retry-aware 去重/partial failures 补偿/step-level logs 检测） | OK |
| 6 | Make（error handler 五指令 Commit/Rollback/Resume/Ignore/Break/router filter 放空静默成功/三响应模式） | OK |
| 7 | Pipedream（concurrency=1 串行按序/event sources 共享/无同步 call workflow emit-and-listen） | OK |
| 8 | Anthropic（Gotchas section 最高信号/disable-model-invocation/描述触发短语放最前防截断/触发信号诊断表） | OK |
| 9 | GitHub 生态（HydraFusion 多模型编排/SemaClaw harness DAG 两阶段+PermissionBridge/LightAgent） | OK |
| 10 | WaytoAGI（tool descriptions 是 prompts/4 action 上限 waterfall/稳定流程委托 agent） | OK |

## 独点（4 个）
### C1：Dify 循环选型与迭代边界 + n8n 三阶段节点组（来源：dify.ai/blog/cross-platform-copywriting + jishuzhan.net + dot-ai.myuuu.co.jp + synta.io，2026-09-27 实拉）
- **Loop vs Iteration 选型**：**前次依赖用 Loop（循环变量=要接续的数据，先设计后实现）、数组处理用 Iteration（引用 items/index）；最大循环次数必设防无限循环**（工作流层：选循环型式的判据=本轮是否依赖上轮输出）。
- **迭代边界**：**迭代输入数组 30 元素上限——上游解析节点先截断留余量（data[:20]）；迭代内跨轮引用通过赋值会话变量全局访问**（工作流层：性能边界在设计期就留余量，不是在运行期撞墙）。
- **n8n 三阶段节点组**：**gather context → run inference → validate and act——把不可预测的 LLM 步与确定性路由分开；pins input context、schema 验证输出、解析失败重试、记录每个决策供审计**（工作流层：LLM 步夹在确定性前后文之间，任何一步解析失败都不污染后续路由）。
- **提升层**：工作流。

### C2：Make 错误处理五指令 + 静默成功三方式 + 三响应模式（来源：smartprocessflow.com + community.make.com + thinkbot.agency + make.com/en/how-to-guides，2026-09-27 实拉）
- **五指令各有操作后果**：**Resume（忽略继续）/ Ignore（跳过该记录）/ Break（停场景跑）/ Commit（标记 bundle 已处理即使出错——防重复处理）/ Rollback（撤销本场景先前所有操作——事务原子性）**（工作流层：选哪个不是风格，是"这记录还重不重跑"的语义决策）。
- **场景可以"成功"却啥也没写（三方式）**：**router 路由 filter 全放空/搜索模块返回零 bundle/错误被忽略——修法：错误路径用 if/else 而不是 router，零 bundle 后接 if/else 显式处理**（工作流层：绿色对勾 ≠ 干了活，结果校验要查"目标记录确实写入了"）。
- **三响应模式标准化**：**transient（超时/5xx/临时认证）→退避重试；数据问题→隔离+通知附违规 bundle；升级带上下文（system/module/operation ID+一键重试链接）**（工作流层：错误响应只有三种形状，提前定好每个场景走哪个）。
- **提升层**：工作流。

### C3：Anthropic 技能最佳实践三件套（来源：claude.com/blog/lessons-from-building-claude-code + fatherofai.in + elayachi.dev + resources.anthropic.com PDF，2026-09-27 实拉）
- **Gotchas section 是技能最高信号内容**：**从"Claude 用这个技能时真实撞到的失败点"积累，随使用持续更新（例：subscriptions 表是 append-only）**（可复用 Skill 层：技能的价值一半在别人踩过的坑——把坑写进 Gotchas，不是写进正文）。
- **副作用技能禁止自动调用**：**deploy/commit/notify 类技能设 disable-model-invocation: true——只能手动触发**（可复用 Skill 层：有副作用的技能不该被模型顺手调用；触发权=风险权）。
- **描述截断与触发诊断**：**最重要的触发短语放描述最前（上下文压力下 description 会被截断），/doctor 检查是否被缩短；诊断表：不加载→描述加细节关键词，过度触发→加负面触发，输出不一致→加 examples/**（可复用 Skill 层：描述是技能唯一的广告位，截断掉的就是调用入口；三个症状三个修法）。
- **提升层**：可复用 Skill。

### C4：工具描述即 prompt + 4 action 上限 + Pipedream emit-and-listen + SemaClaw harness（来源：musketeerstech.com + pickaxe.co + qa-sim.cloud.thinkproject.com + arxiv 2604.11548，2026-09-27 实拉）
- **工具描述是 prompt 本身**：**工具型 agent 里模型完全依据 name/description/parameter docs 决定调用什么、传什么参数——模糊描述产生错误调用，没有 system prompt 能修；每个工具描述=迷你操作手册（做什么/何时用/参数契约）**（工具层：写工具描述按写 prompt 的标准来，不是填空）。
- **4 action 上限**：**单 agent 封顶约 4 个 action；更复杂→waterfall 路由到专门 sub-agents，而不是把 10 个工具塞进一个 prompt**（工作流层：工具数超过认知负载就拆层，不是硬塞）。
- **Pipedream 无同步 call workflow**：**连接 workflow 的标准机制是 $.send.emit() 异步 emit——触发 listener workflow 在 emit 方完成后运行；没有"同步调用子流程等返回值"的步骤**（工作流层：平台能力差异决定编排形态——异步事件链 vs 同步子流程调用要按平台选）。
- **SemaClaw harness 工程**：**DAG 两阶段混合 agent 团队编排 + PermissionBridge 行为安全系统 + 三层上下文管理架构**（工作流层：harness 是把"上下文管理+权限桥+编排 DAG"做成基础设施，agent 只在上面跑业务）。
- **提升层**：工具 / 工作流。

## 判重说明
- C1 循环选型（r229-C 循环面增量——Loop/Iteration 区分+30 上限+跨轮引用）；三阶段节点组（新）；落。
- C2 五指令细分（r231-B n8n Continue-on-Fail 面增量——Commit/Rollback 语义）；静默成功三方式（新——结果校验面）；三响应模式（r230-A 重试面互补增量）；落。
- C3 Gotchas（新）；disable-model-invocation（新）；描述截断+诊断表（新——r231-A 描述成本面互补）；落。
- C4 工具描述即 prompt（新角度——r230-A 工具描述注入面互补）；4 action 上限（新）；emit-and-listen（新——平台差异）；SemaClaw harness（r230-C OpenClaw harness 面增量——DAG 两阶段+PermissionBridge）；落。
- 未落：LangFlow Policies（自然语言规则→guard——r229-C guard 面已覆盖）；Agentics aMap（面窄）；Activepieces 错误类型结构（面窄）；HydraFusion 多模型编排（产品面无个人增量）；LightAgent（数量堆积）；李克五观法（领域外）。
