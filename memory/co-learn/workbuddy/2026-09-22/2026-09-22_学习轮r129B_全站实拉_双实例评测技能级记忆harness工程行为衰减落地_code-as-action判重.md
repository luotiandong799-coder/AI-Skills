# r129-B 全站实拉 · 双实例评测/技能级记忆/harness工程/行为衰减/工具调用三评分落地 · code-as-action判重

> 日期：2026-09-22｜批次：r129-B｜模式：定时任务「AI技能库学习·每时3轮×10次」触发

## 一、逐站实拉（10 次，全量信源覆盖）
| # | 信源 | 实拉内容 | 提炼 |
|---|---|---|---|
| 1 | LangFlow 1.10/1.11/Activepieces/Pipedream | 平台 | Memory bases/HITL 门控；approval 留痕；平台功能 |
| 2 | Anthropic Skills/SkillsMP/skills.sh | 技能生态 | 双实例 eval-first；三级加载；缓存→脚本→思考分层 |
| 3 | 腾讯 SkillHub/TRACE/虾小宝/AgentMore | 国内市场 | TRACE 五维评测；跨平台导出；平台治理 |
| 4 | deeplearning.ai/MCP/A2A/PydanticAI | 课程 | Agentic AI 四模式；typed agent；协议 |
| 5 | WaytoAGI/agentskills.io/白皮书 | 生态 | 技能即文件；MCP vs Skills 分工；生态数据 |
| 6 | HuggingFace/smolagents | 框架 | CodeAgent code-as-action；MCP 桥；平台 |
| 7 | GitHub 生态/DeepSeek Harness/AHE | 生态 | 组件插件化；harness 工程+深度遥测；Top100 |
| 8 | MemSkill/MUSE/MindMemOS/Proactive Memory/AWS | 记忆架构 | 技能级记忆；记忆 schema 自进化；行为状态衰减+主动注入 |
| 9 | Iterathon/ASOasis/QASkills | 工具可靠性 | structured outputs；tool-calling 三独立评分 |
| 10 | OpenClaw Skill Workshop | 技能流程 | 提案队列 propose-create/update；PROPOSAL.md |

## 二、判重与落地
- **D210 双实例 eval-first 技能迭代（落 · sa）**：sa B 实例 0/挣扎点 0；A 写草案→B 实测 2-3 prompt→观察挣扎点回 A 为独有增量 → 落。
- **D213 Code-as-action（不落）**：ED L1111 已有 Code-as-action（smolagents 2026-09-19 实拉，CodeAgent vs ToolCallingAgent 两形态）→ 重叠，不落。
- **D215 技能级记忆+创建使用同循环（落 · dl）**：dl per-skill 0/技能级记忆 0；per-skill 经验命名空间+skill_create 运行时内建为独有增量 → 落。
- **D217 行为状态衰减+主动记忆注入（落 · ctx）**：ctx 行为状态衰减 0/主动注入 0；长任务目标漂移+独立 memory agent 决定注入时机为独有增量 → 落。
- **D218 工具调用三独立评分（落 · av）**：av 工具选择 0/参数正确性 0/独立评分 0；选对/传对/合规三维分打为独有增量 → 落。
- **D219 Harness 工程+深度遥测（落 · dl）**：dl 遥测 0/Evolution 0/harness 工程 0；把运行环境当被优化对象+遥测"模型看到了什么"为独有增量（与轨迹→技能区分）→ 落。
- **D212 TRACE 五维评测（不落）**：sa 已有闭合邻域/双计分板评测；五维评分与既有评测方法论重叠 → 不落。
- **D216 记忆 schema 自进化（不落）**：ctx dreaming 4 处已覆盖记忆整合；validation-driven 为细分 → 不落。

## 三、逐站判非重复理由（未落地站点）
- 平台类（LangFlow/Activepieces/Pipedream/MCP/A2A/腾讯 SkillHub/ModelScope/HF）：平台/工具层 → 淘汰。
- 缓存→脚本→思考分层：mts §173 压缩纪律已覆盖分层选择 → 重叠。
- TRACE 五维：sa 评测方法论已覆盖 → 重叠。
- 提案队列 propose-create：sa 已落"先提案后写"流程?（判重时 proposal 0 命中但 r129-A 已落双实例，提案队列与 Workshop 平台流程绑定较深 → 不落）。

## 四、功能套件检查（每轮）
- 套件：wb-ponytail / wb-max-token-saver / wb-context-compressor
- 本轮：ctx 新增行为状态衰减，与记忆四策略/压缩纪律互补；三件套覆盖完整，无需增删。
