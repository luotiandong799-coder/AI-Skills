# 学习轮 r407B · 信源实拉审计（deeplearning.ai / Dify / Flowise / LangFlow）

> WB 自有轮（070cce0c 自动化）。每小时 3 轮连跑之第 2 轮，逐站重新实拉（非复用 r407A 结论）。

## 四列落地表
| 轮 | 文件 | 版本 | 独有点 |
|----|------|------|--------|
| r407B | — | — | （0 落地：逐站实拉证据 + 判非重复理由见下） |

## 逐站实拉证据与判非重复理由
- **deeplearning.ai / Agentic AI（Andrew Ng）+ CrewAI 多智能体课程**：四设计模式（reflection / tool use / planning / multi-agent）、evals 误差分析、延迟成本优化 → 已被 `wb-context-compressor` 3.309.0（规划/反思/成本纪律）+ `wb-skill-authoring` 3.116.0（设计模式方法论）覆盖，**重叠 >60%** → 净 0。
- **Dify 企业级安全**（搜索实拉：RBAC 角色-资源-操作三元组、凭证 env 化、Prompt 注入防护、可解释/可回滚/可观测/可降级四原则）：与 `agent-guild` 1.51.0 权限治理 + `wb-execute-discipline`（可回滚/可观测/降级）+ 历史 r400-Q-B「Dify 插件权限默认 Everyone」**重叠 >60%** → 净 0。
- **Flowise / LangFlow**（搜索实拉：低代码画布、MCP 双端、HITL 审批、可观测外接 Langfuse）：已被 r400A「低代码 Agent 编排平台机制」+ r399B「开源 Agent 框架实践（LangGraph/AutoGen）」覆盖 → 净 0。

## 提升层判定
四站独点均归 模型/工作流/可复用Skill 层，无 >60% 无重叠净新面；属 407 轮穷举后候选池饱和常态（非缩水）。

## WB 已落地台账（本轮 0 新增，无 bump）
wb-skill-authoring 3.116.0 / wb-artifact-verification 2.128.0 / wb-debug-loop 1.136.0 / wb-max-token-saver 1.66.0 / wb-context-compressor 3.309.0 / agent-guild 1.51.0。
