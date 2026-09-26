# 学习轮 r225A：skillsmp p83精选与Dify变量汇聚与Anthropic工具写作五原则与deepseek-harness全插件化（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/83（#8201-8262 取） | OK |
| 2 | Dify 检索（Variable Aggregator/Human Input/Trigger/动态 prompt） | OK |
| 3 | n8n 检索（Agents 发布/MCP discovery/表达式引擎） | OK |
| 4 | LangFlow 检索（1.11-1.12 面/ALTK bundle） | OK |
| 5 | Activepieces 检索（Tables/队列执行/pieces） | OK |
| 6 | Make 检索（2026 更新面） | OK（与 r224-B 重叠，无新增不落） |
| 7 | Pipedream 检索（Build with AI/String.com/Debug with AI） | OK（r223-A 增量） |
| 8 | Anthropic 检索（工具写作五原则/Agent Skills 原文章/Commerce Agents） | OK |
| 9 | GitHub trending 检索（github.hot 09-26/paperclip/google ax/ECC） | OK |
| 10 | deepseek-plugin.org 生态检索（DSH Plugin Store/graph-memory） | OK |

## 独点（4 个）
### A1：skillsmp p83 精选：范围蔓延检测 / 系统论文段级蓝图 / 保主张去 AI 味 / 多 agent 任务协调（来源：skillsmp.com/skills/page/83，2026-09-27 实拉）
- **scope-creep-detector（Shubhamsaboo/awesome-llm-apps ★139,204）**：**对照声明意图分析 git diff 检测范围蔓延——无关文件/过宽 PR/超出修复的改动/依赖新增/公共 API 改名/配置或 CI 编辑/超大 hunks/仅格式文件；本地离线运行；输出 keep/split/justify 建议**（代码评审面，与既有"AI 收 diff 五连查"互补——那条查代码本身，这条查"改动是否超出该改的范围"）。
- **writing-systems-papers（wanshuiyin ★16,461）**：**OSDI/SOSP/ASPLOS/NSDI/EuroSys 10-12 页系统论文段级结构蓝图——页分配/段落模板/写作模式**（学术写作面专项）。
- **academic-humanizer（dongshuyan/compass-skills ★735）**：**学术去 AI 味但保主张/证据强度/逻辑关系/全篇术语一致性/document-level pattern variation（全篇模式变化防机械重复）/学术语域；明确不做检测规避、不加原文没有的事实**（去 AI 味面增量——r224-C aigc-down 补全篇模式变化维度）。
- **task-coordination-strategies（wshobson/agents ★39,856）**：**拆复杂任务→设计依赖图→协调多 agent（任务描述+负载均衡）**（多 agent 编排面，与 ed §多Agent协作互补——那条管协作纪律，这条管拆解/依赖图/负载均衡）。
- **提升层**：工作流 / 可复用 Skill。

### A2：Dify 变量汇聚与人工介入：Aggregation Group / Human Input node / Trigger（来源：dify.ai/blog + docs，2026-09-27 实拉）
- **Variable Aggregator 的 Aggregation Group（2026-06-06）**：**一个 Variable Aggregator 内分组汇聚多组变量、每组独立输出——多分支各自收敛互不污染**（变量汇聚面，r224-B Context Variables 增量：从"自动引用"到"分组独立汇聚"）。
- **Human Input node（v1.13.0，2026-03-03）**：**workflow 暂停等人工审核，批准/编辑/改道后恢复——边界情况交真人**（人工介入面，与 r224-B n8n 双 Chat tool 澄清互补：一个用于澄清、一个用于批准/编辑）。
- **Trigger（2025-11-21）**：**workflow 后台监听外部事件自动触发，事件载荷转结构化变量注入——workflow 从"等调用"变"后台服务"**（事件驱动面）。
- **提升层**：工具 / 工作流。

### A3：Agent 工具与编排面：Anthropic 工具写作五原则 / n8n MCP discovery / google ax / Commerce Agents（来源：anthropic.com/engineering + datapath.ai + github.hot + marktechpost，2026-09-27 实拉）
- **Anthropic《Writing effective tools for agents》五原则**：**①选对要实现的工具（不实现的明确不写）②工具命名空间化（namespacing 定义功能边界）③返回有意义的上下文给 agent（不只返回状态码）④优化工具响应 token 效率 ⑤prompt 工程化工具描述与规格**（工具编写面，与 r224-B PreToolUse hook 互补：那条管安全 hook，这条管工具本身怎么写）。
- **n8n MCP discovery handshake（spec 2026-07-28）+vm 表达式引擎默认（2026-09）**：**原生支持新版 MCP 发现协议；vm 表达式引擎默认启用（隔离更强+报错更清晰）**（工具/平台面）。
- **google/ax（2026-09-26 上 Trending，Go）**：**Google 开源 agentic orchestration runtime**（编排运行时面）。
- **Claude Commerce Agents（2026-09-03，Apache-2.0）**：**购物/商家 agent 跨 retail/travel/telecom/entertainment 蓝图——避免每团队重建同样脚手架**（领域蓝图面，复用脚手架思路与 §现成可改 一致）。
- **提升层**：工具 / 工作流。

### A4：DeepSeek Harness 全插件化 + graph-memory 知识图谱记忆（来源：deepseek.com/harness + dshplugin.store + skillhub.cloud.tencent.com，2026-09-27 实拉）
- **DSH "Everything is a plugin" 官方声明细化**：**models/tools/skills/sessions/sandboxes/storage/loops/scheduling/UI 九类能力每个都是可替换插件；Cordis services/events 事件总线让插件协作；DSH Plugin Store 已索引 14,073 个插件仓库（2026-09-20 同步）**（r224-C deepseek-harness 面深化：插件目录规模+事件总线机制）。
- **graph-memory（adoresever，清华讨论会 2026-04）**：**从对话提取结构化三元组构建知识图谱，压缩上下文 75%，支持跨会话经验复用——Deepseek Harness/OpenClaw 通用**（记忆面增量：三元组抽取→图谱→跨会话复用，与 r221 claude-mem/记忆四策略互补——那条管分策略提取，这条管图谱化+压缩率）。
- **Activepieces Built-in Tables**：**内建表格存工作流状态——跨 run 状态/联系人/错误日志/队列，查重键+状态字段幂等更新，不配外部数据库**（状态存储面）。
- **提升层**：工具 / 工作流。

## 判重说明
- A1 全为新面（scope-creep 检测/系统论文蓝图/保主张去 AI 味/任务协调），落。
- A2 Dify 面（Aggregation Group/Human Input/Trigger）均为未落机制，落。
- A3 Anthropic 工具写作五原则未落过（原文章）；n8n MCP discovery 新；google ax 新；落。
- A4 DSH 9 类插件化+14k 插件规模为 r224-C 深化；graph-memory 图谱记忆新；Activepieces Tables 新；落。
- 未落：Make（与 r224-B 重叠）；LangFlow（与 r224-A/B 重叠）；Pipedream Build with AI（r223-A 已落 Edit with AI，仅增量不足 40%）。
