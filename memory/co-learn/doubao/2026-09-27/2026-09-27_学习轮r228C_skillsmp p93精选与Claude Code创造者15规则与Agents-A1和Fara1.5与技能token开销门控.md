# 学习轮 r228C：skillsmp p93精选与Claude Code创造者15规则与Agents-A1/Fara1.5与技能token开销门控（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/93（total_length=11016，读到 #9283 截断约 8800） | OK |
| 2 | Dify（Marketplace 模板/Publish to Marketplace/plugin-first 架构） | OK |
| 3 | n8n（Agents 发布会/Production AI Playbook: Complexity Cliff） | OK |
| 4 | LangFlow（flow 暴露为 MCP server/LFX MCP/Agent 教程） | OK |
| 5 | Activepieces（无代码自动化 4 步/销售自动化三层/11 用例） | OK |
| 6 | Make（webhook 触发 agent/Webhooks 课程：即时 vs 轮询） | OK |
| 7 | Pipedream（Triggers 文档/x-pd-nostore/x-pd-notrigger） | OK |
| 8 | Anthropic（Claude Code Best Practices/Steering 七方法/Boris Cherny 15 规则） | OK |
| 9 | GitHub 生态 + HF/ModelScope（Youtu-LLM-2B/Agents-A1/Fara1.5） | OK |
| 10 | WaytoAGI + OpenClaw（creating-skills 官方文档/agents CLI/技能 token overhead） | OK |

## 独点（4 个）
### C1：skillsmp p93 精选：只读分析纪律/FMEA AP/设计简报协议/市场双向测算（来源：skillsmp.com/skills/page/93，2026-09-27 实拉）
- **analyze 只读仓库分析带置信度与证据边界（Yeachan-Heo/oh-my-codex ★33,297）**：**深度仓库分析返回带显式置信度的排序综合、具体文件引用、清晰的证据-vs-推断边界——"why does"/"what's causing"触发，提任何修改前先做 grounded 跨文件解释**（分析纪律面：改之前先只读取证，边界标注）。
- **FMEA AIAG-VDA 7 步 + Action Priority 替代 RPN（ddunnock/claude-plugins）**：**失效模式与影响分析支持 DFMEA/PFMEA/FMEA-MSR；用 AIAG-VDA 7 步方法论，Action Priority (AP) 风险评估取代传统 RPN**（风险分析面：RPN 乘法指标的替代——AP 按 severity/occurrence/detection 组合直接给行动优先级）。
- **design-brief I-Lang 协议消除模糊（nexu-io/open-design ★97,471）**：**结构化设计简报转具体设计 spec——强制显式维度 palette/typography/layout/mood/density/constraints，消除"make it professional"这类模糊需求**（规格面：模糊审美词翻译成六可测维度）。
- **market-research TAM/SAM/SOM 双向计算（alirezarezvani/claude-skills ★26,225）**：**市场规模同时 top-down 和 bottoms-up 计算，从不单一未署名数字；调查样本量带有限总体校正+每段最小数；用 Kotler 可测量/实质性/可访问/可区分/可行动 5 标准评分候选段**（测算面：双向对账+方法假设必输出）。
- **提升层**：工作流 / 可复用 Skill。

### C2：Claude Code 创造者 15 规则 / flow 暴露为 MCP / Pipedream payload 控制头（来源：rsrini7/claude-code-rules-creator.md 2026-05-02 + langflow.org/blog 2025-10-10 + pipedream.com/docs 2026-09-27，实拉）
- **Boris Cherny（Claude Code 创造者）并行执行与权限流**：**并行工作区——5–15 个 Claude 实例同时在不同目录跑，标签编号 1–5，系统通知 ping 完成/需输入；Auto Mode 用分类器自动批准安全命令；"fewer permission prompts"技能扫描历史白名单常用安全命令减少重复审批；Adaptive Effort——默认 extra high，模型自适应决定思考量，比强制 max 一致性好；Focus Mode 分角色——builder agent 开（隐藏中间步骤只见最终输出）、reviewer agent 关（监控逻辑）**（执行纪律面：与 wb-max-token-saver 的 effort 思想互补——自适应优于硬顶）。
- **Plan Mode 先规划后执行（Shift+Tab）**：**只读探索代码库→迭代方案→再切自动执行；custom slash commands 把 skills 和 plugins 组合成多步工作流，check in .claude/commands/ 全团队可用**（工作流面：读-写分离的探索态）。
- **Langflow 把 flow 暴露为 MCP server**：**不需要从零写 MCP server——flow 直接暴露为 MCP server 供其他 agent 使用，私有数据/API 接入即用**（工具面：已有流程复用为外部 agent 工具）。
- **Pipedream x-pd-nostore / x-pd-notrigger 请求头**：**x-pd-nostore 阻止 Pipedream 存储 payload；x-pd-notrigger 不触发 workflow——敏感数据的存储与触发是显式开关**（安全面：默认存储的退出开关）。
- **提升层**：工具 / 工作流。

### C3：Agents-A1 与 Fara1.5 新模型事实 / OpenClaw agents CLI / 技能 token 开销门控（来源：modelscope.ai 2026-09-22 + aitoolsreview.co.uk 2026-08-03 + docs.openclaw.ai 2026-08-18 + tryopenclaw.io 2026-04-20，实拉）
- **Agents-A1（InternScience，ModelScope 2026-09-22）**：**"Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter Performance with a 35B Agent"——35B 参数 agent 通过扩展"地平线"（测试时扩展/多步）达到万亿参数性能，Qwen3.5 MoE**（模型/方法面：参数不再是一切，horizon 扩展是杠杆）。
- **Microsoft Fara1.5（2026-07-22，MIT）**：**27B 浏览器 computer-use agent 家族（4B/9B/27B，Qwen3.5 骨干），Online-Mind2Web 72.3% 高于 OpenAI Operator 58.3%；自曝 long-tail 基准 9B 仅 32.3%**（模型面：本地可自托管浏览器 agent；并自曝短板不藏）。
- **OpenClaw agents CLI 隔离智能体**：**管理相互隔离的智能体——工作区 + 身份验证 + 路由，openclaw agents list --bindings 查看绑定**（编排面：按工作区/认证/路由隔离 agent）。
- **技能 token overhead 和 gating（TryOpenClaw）**：**每个技能都有 token 开销——编写时考虑 gating（何时加载/何时不加载），好技能解剖包括触发条件设计；发布前做安全审查**（Skill 设计面：技能本身也是上下文成本，门控不是白送的）。
- **提升层**：模型 / 工具 / 可复用 Skill。

### C4：Claude Code 验证优先与探索-规划-编码 / n8n Complexity Cliff / 销售自动化三层（来源：code.claude.com best-practices 2026-09-26 + blog.n8n.io 2026-06-09 + activepieces.com/blog 2026-01-22，实拉）
- **Claude Code 验证优先 + 探索→规划→编码 + 对抗性评审**：**"给 Claude 验证自己工作的方式"是单条最重要实践（support.claude.com power user tips 2026-09-23 再次确认）；顺序是探索→规划→编码；加 adversarial review step（专门挑错的评审步骤）；course-correct early and often；manage context aggressively；用 subagents 调查**（执行纪律面：验证优先是 Anthropic 内部反复确认的第一实践）。
- **n8n Complexity Cliff**：**第一个 agent 好用，加到三个后系统不可调试——复杂度悬崖；架构优先于提示词；sub-workflows 作可复用组件优于 AI Agent Tool；会话 ID 是多 agent 记忆的关键**（编排面：可调试性随 agent 数量非线性恶化，先想架构再堆 agent）。
- **Activepieces 销售自动化三层**：**数据层/逻辑层/执行层——先打通数据集成，再写逻辑，最后落执行；敏感动作加 human approvals**（架构面：自动化分层治理）。
- **Dify Typeform 多信号评估路由模板**：**AI agent 评估每个入站申请的 region/product category/ecosystem fit/company signal/Dify plugin status 多信号→路由三条路径之一**（路由面：多信号评分再分流的模板化）。
- **提升层**：工作流 / 可复用 Skill。

## 判重说明
- C1 analyze（证据-推断边界+显式置信度）、FMEA AP（AP 替代 RPN）、design-brief（六维度协议）、market-research（双向测算+方法假设输出）、doc-to-markdown（后处理清单）均新面；落。
- C2 Boris Cherny 规则（并行实例/auto mode/白名单技能/adaptive effort 优于强制 max——wb-max-token-saver effort 思想互补增量）；flow-as-MCP（r225 有 MCP 发布面但"已有 flow 暴露为 MCP server 免写代码"为增量）；x-pd-nostore/x-pd-notrigger（安全退出开关新）；webhook 即时 vs 轮询（r225 webhook 端点化增量）；落。
- C3 Agents-A1/Fara1.5 为新模型事实（区分已核验事实）；OpenClaw agents CLI 隔离（新）；技能 token overhead+gating（新面——skill 本身有 token 成本与门控）；落。
- C4 验证优先（Anthropic 官方 best practices 反复确认第一实践；r226 验证纪律为互补面合并增量）；Complexity Cliff（n8n Playbook 开头概念，r227-B 已落同文 sub-workflows 等面，本批仅 Complexity Cliff 概念为独有增量——合并保留）；销售三层（新）；Typeform 多信号路由（新）；落。
- 未落：Claude Code Steering 七方法（r227-B 已落同一篇，纯重复）；n8n Production AI Playbook 主体（r227-B 已落）；OpenClaw SKILL.md 结构（多轮已落）；HF Youtu-LLM-2B（模型发布事实，个人使用场景外无方法增量）；Claude Code cheatsheet（工具手册面）。
