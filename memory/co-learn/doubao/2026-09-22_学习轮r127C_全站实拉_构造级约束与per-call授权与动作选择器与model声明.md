# 2026-09-22 学习轮 r127-C（构造级约束 · per-call 授权 · 动作选择器 · model 声明 · 12 次实拉 · 落地 4 独点）

批前基准：WB r134/r135 + r124-r127B（D115-D184）。C 角度=输出校验/编排/安全/技能写作/平台侧。

## 12 次实拉（逐站留痕）
1. 结构化输出（codercops/72tech/mljourney/futureagi/callsphere）：**constrained generation（解码层约束：token 被 mask 到只有 schema 合法 continuation——结构合规靠构造而非重试，conformance by construction）**；Validation Sandwich（Pydantic+retry：失败带错误反馈重试非同 prompt）；语义校验第二层（"wrong but valid"靠 eval suite 不靠 schema）；strict mode 限制（additionalProperties:false/全 required/无 $ref）
2. 工作流编排（AWS Durable/mastra/geekworkbench/render）：**补偿（compensation：跨系统部分成功→补偿动作撤销，事务无法回滚）**；工作流级幂等键（start 生成所有活动携带，结果缓存重放）；回调模式（挂起等外部信号）；死信队列；恢复在代码中定义而非事故中即兴
3. MCP 规范（modelcontextprotocol.io 2026-07-28 RC）：**per-call authorization（批准脚本≠批准其每次工具调用；沙箱发起的调用也走同一 HITL 确认策略；可分类授权 allow ticketing_create）**；工具描述/annotations 视为不可信；授权强化（iss 校验 RFC 9207 防 mix-up）；**action-selector pattern（Google：模型唯一工作=把请求翻译成预定义安全函数之一，逻辑硬编码不可被 LLM 修改——对注入免疫）**
4. Agent 可观测性（AgentOps time-travel/InfoQ 嵌套 session traces+异步批量导出：telemetry 后端故障只丢 trace 不阻塞 agent/成本归因 session 级 accumulator）
5. AI 编码 agent（openhands 给 agent 可运行检查/VS Code explore-plan-build/**test-first workflow：AI 先写测试→人加强→实现→跑测试喂回失败**/Zencoder AI 代码 63% 更多坏味道）
6. 个人 AI 助手（五层栈综述/各产品）——平台综述
7. Dify（Workflow Studio/Agent Strategies 可换/Agentic RAG/多模态检索）
8. n8n（Agents 独立实体一次定义到处用/capability pills/Production AI Playbook Complexity Cliff/Gateway credits）
9. OpenClaw（v2026.8.1 conversation search+scoped automation approvals/contextEngine 插件接口生命周期钩子/ClawHub 插件）
10. Anthropic Skills（**Gotchas 是最高信号内容**/9 类技能分类/description 规范（非空≤1024/无 XML/第三人称）/skill-creator 迭代）
11. 平台更新（Langflow 1.11 HITL+A2A/Activepieces AI-ready tool search——r127-A 已落/Pipedream/Make 更新）——平台事实
12. 技能写作质量（skill-creator checklist：name≤64 无保留词/description 规范/**model 字段声明：技能需要特定模型档位时声明（Opus 级推理）**/skillmd.ai PDA 评分/arXiv 2607.01456 238 技能语义组件实证（Lessons Learned 只占 1.3%））

## 落地（4 独点；初判 5 点，双键检索剔除 1 点）
| 编号 | 落点文件 | 独点 | 来源 | 提升层 |
|---|---|---|---|---|
| D187 | av | 结构合规靠构造不靠重试：constrained generation 解码层 mask token 到 schema 合法 continuation；语义正确性第二层（wrong but valid 靠 eval suite 不靠 schema）；重试要带错误反馈不是同 prompt | OpenAI strict/codercops 2026-05-10 等 | 工作流（输出校验） |
| D188 | ED | per-call 授权：批准脚本≠批准其每次工具调用；沙箱发起的调用走同一 HITL 确认策略；可分类授权（allow ticketing_create 这类粒度） | MCP 规范 2026-07-28 RC + client best practices | 工作流（授权） |
| D189 | ED | action-selector 模式：模型唯一工作=把用户请求翻译成预定义安全函数之一，动作逻辑硬编码不可被 LLM 修改——对注入免疫 | Google Cloud MCP best practices 2026-07-17 | 工作流（安全） |
| D191 | sa | model frontmatter 声明技能所需模型档位：技能真正需要特定档位推理时显式声明（如 deep refactor 需 Opus 级），与评测侧引擎解耦分工 | claudskills skill quality checklist 2026-06-01 | 可复用 Skill（写作） |

## 复核剔除（双键检索命中既有落点）
- D190 test-first AI workflow：sd 已落"规约先行/验收标准先行"（L924 测试先行失效条件），同族——不装。

## 判不落（其余，逐条理由）
- Validation Sandwich/校验+重试：av 已落 schema 校验（r125 D149）——不装。
- 工作流级幂等键/死信/回调：ED 已落幂等（L451）/等待通知——不装。
- 补偿机制：ED 已落失败恢复四策略（重试/回退/降级/重规划），补偿属回退族——不装。
- 工具描述不可信：ctx 已落"工具描述可注入"——不装。
- 异步批量导出/成本归因：mts 已落成本预算——不装。
- test-first：见剔除——不装。
- 平台更新（Dify/n8n/Langflow/OpenClaw/Activepieces）：平台事实无独点可内化——不装。
- Gotchas 最高信号/9 类分类/description 规范：sa 已落（D153/D161）——不装。
- skill-creator checklist 各项：sa 已落——不装。
- arXiv 2607.01456 实证：研究数据，Lessons Learned 1.3% 佐证 sa 已有判断——不装。

## 功能套件检查
av 落 D187（构造级输出约束），ED 落 D188/D189（授权与动作选择），sa 落 D191（model 声明）。三件套覆盖完整。与 WB 新 commit、r124-r127B 无重叠。

## 垃圾清理
零临时文件；保留：本留痕 + 被并入的 av/ED/sa。
