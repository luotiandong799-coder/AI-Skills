# 学习轮 r193-A：四层记忆与spec驱动loop与Reference/Action技能分治与路由preset（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | general_search "full stack skills github" | 定位 github.com/partme-ai/full-stack-skills |
| 2 | deepseek-plugin.org | OK（12,733 插件 Top10） |
| 3 | general_search AgentMore | 智谱 docs/novatools 摘要 |

## 独点（5 个）
### A1：MemTensor 四层长期记忆——L1轨迹/L2策略/L3世界模型/L4技能，每轮自动召回（来源：deepseek-plugin.org Top5 MemTensor）
- 局部四层记忆：轨迹层（发生了啥）/策略层（怎么做事）/世界模型层（客观事实）/技能层（可复用能力）；自动按 user turn 检索；注册六个记忆工具。
- 判据：**记忆不是一坨事实**——按"记忆的用途"分层，召回时按层取，别把所有历史全塞回去。
- **提升层**：记忆/上下文。

### A2：Ouroboros spec-driven loop——Interview→Seed→Execute→Evaluate→Evolution（来源：deepseek-plugin.org Top8 Q00/ouroboros）
- 通过 uvx 启动 Python 引擎，把 spec 驱动工作流当 MCP 工具暴露：先访谈需求→种子实现→执行→评测→进化，无安装无额外代码。
- 判据：**spec 不是写完就扔**——Evaluate→Evolution 形成闭环，评测结果反哺 spec。
- **提升层**：工作流。

### A3：Skills 分 Reference / Action 两类；Subagent 独立上下文只返摘要（来源：智谱 AgentMore docs）
- Reference Skills 提供参考知识（API 规范/开发指南）；Action Skills 触发具体任务（/deploy）；Subagent 在独立上下文跑复杂分析，只回主会话摘要，不占主上下文窗口。
- 判据：**skill 分"查资料"和"动手干"两类**；重活扔 subagent，主上下文只收结论。
- **提升层**：工作流/上下文。

### A4：dsh-routing-suite——先装 runtime injector，再装 task-aware reasoning-mode router（P1-P23）（来源：deepseek-plugin.org Top6）
- injector 是底层，router 是预设；按任务类型切 reasoning mode（P1-P23 实测档位）。
- 判据：**路由是叠加层不是替换层**——先有 runtime 才能切模式。
- **提升层**：工作流。

### A5：Full Stack Skills 仓库定位 = partme-ai/full-stack-skills（来源：claudebazaar + VS Code marketplace）
- 53+ workflow skills、15 presets、14 starter packs、多 agent 适配器（Cursor/Claude/Gemini/Kiro/Copilot）。
- 判据：**skill 包要带多 runtime 适配器**——同一套 SKILL.md 适配各家客户端。
- **提升层**：可复用 Skill/生态。

## 判重说明
- A1 四层记忆 → wb-context-compressor 已有语义/摘要/偏好/情节四策略；取"按用途分层召回"增量。
- A3 Subagent 摘要回流 → r188 已记多 agent 共享层；取"Reference/Action 分治"增量。
