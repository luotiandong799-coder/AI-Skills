# r297C 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r297B 全量（含 r297A/B 各十独点）+ 并行侧。查询词与 r296 三轮及 r297A/B 全错开（本轮=分块参数值/OTel执行关联/组件发布纪律/agent构建上限/agent类型/RAG源复用/官方评测要求/ghskill供应链验证/Copilot自检/轨迹技能学习主题）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | 分块参数具体值：中文 500 token/技术文档 800+150 重叠/重叠 10-20%；自适应块大小（代码密集→1.5x、简单文本→0.5x）；chunk 级编辑（禁用/改坏 chunk+关键词） | 合并保留增量（r296C Parent-child，本点=具体参数+自适应块） | 工作流 |
| 2 | n8n | OpenTelemetry 原生：workflow 执行自动变 trace（execution ID 作关联键跨系统重建）；AI 审计轨迹默认属性（run ID/节点 IO/时间戳/错误，零插桩）；预算熔断器（Run Budget Status 前置昂贵 AI 步骤，超支回退便宜模型） | 合并保留增量（r297B #3 OTel，本点=execution ID 关联+审计默认+预算熔断） | 工具 |
| 3 | LangFlow | 自定义组件纪律：不重命名 class/name（前端测 type 破坏所有用户）；Update（无破坏）vs Review（快照后再更新）；LANGFLOW_ALLOW_CUSTOM_COMPONENTS=false 可全局关闭；CVE-2026-17633 custom_component API RCE | 合并保留增量（r297A #3 guard RCE，本点=组件发布纪律+关闭开关） | 可复用 Skill |
| 4 | Activepieces | AI agent builder：Max steps 20 单次上限；your model your key（admin 集中设 provider）；agent 可用自有 MCP servers；从指令开始→连工具→立即跑 | 合并保留增量（r295B 审批门，本点=20 步上限+集中 provider） | 工作流 |
| 5 | Make | 四 agent 类型：Synthesizer（多源→结构化摘要）/Routing（输入→动态选工作流，逻辑树不可管理时）/Qualifier（按标准评估决策）/Orchestrator（协调多工具） | 合并保留增量（r295A 多智能体五模式，本点=平台四类型实例+Routing 判据） | 工作流 |
| 6 | Pipedream | Event sources 独立资源：一个 source 触发多个 workflow（一源多流复用）；sources（this.$emit+dedupe 策略）vs actions（return）两类组件；两类部署触发器 | 合并保留增量（r296C 多触发器，本点=source 独立复用+dedupe） | 工作流 |
| 7 | Claude | 官方评测要求：每技能≥3 评测场景+Haiku/Sonnet/Opus 三模型测试+基线对比（无技能 15 往返/3 失败/12k tokens vs 有技能 2 澄清）；Skills 2.0：加权 rubric 自动评分+A/B 并行版本+分数按版本存+批量+生产监控 | 合并保留增量（r296A 先评测后构建，本点=官方要求细节+Skills 2.0 评测功能） | 可复用 Skill |
| 8 | skills.sh | gh skill publish（2026-04-16）：验证 agentskills.io spec+检查 tag protection/secret scanning/code scanning；不可变 release=有人拿 repo 也改不了现有 release | 合并保留增量（r296C skills CLI 命令集，本点=发布供应链验证+不可变 release） | 工具 |
| 9 | GitHub | Copilot coding agent：model picker+self-review+内置安全扫描+custom agents+CLI handoff；workspace context 工具（#githubRepo 语义/#githubTextSearch 文本）；skills 与 custom agents/instructions 三层分工 | 合并保留增量（r296C Copilot 三阶，本点=self-review+安全扫描+context 工具面） | 工作流 |
| 10 | deeplearning | Agent Memory 课程：记忆工程=上下文工程下一层（长期记忆外部化+结构化+写回环自动更新）；**轨迹→技能学习**（Building Adaptive AI Agents：用 agent 留下的 traces 提炼行为技能） | 合并保留增量（r295A 记忆四层，本点=轨迹→技能学习+写回环） | 工作流 |

判重口径：增量判定。本轮 10 合并保留增量，零纯重复。