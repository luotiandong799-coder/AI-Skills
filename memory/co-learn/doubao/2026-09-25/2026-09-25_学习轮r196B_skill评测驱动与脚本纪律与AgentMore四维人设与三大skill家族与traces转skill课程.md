# 学习轮 r196-B：skill评测驱动与脚本纪律与AgentMore四维人设与三大skill家族与traces转skill课程（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.n8n.io/flow-logic/error-handling | 无正文 |
| 2 | docs.langflow.org | OK 1.11.x |
| 3 | activepieces.com/docs | OK |
| 4 | pipedream.com/docs/workflows/steps/code | 死链 |
| 5 | docs.anthropic.com agent-skills/best-practices | OK 全文 |
| 6 | make.com/en/help/make-magazine | fetch error |
| 7 | skills.sh/trending | OK 榜 |
| 8 | skillhub.tencent.com | OK 7.6 万 |
| 9 | deeplearning.ai | OK |
| 10 | 智谱 AgentMore（robots 禁走搜索） | OK 经 novatools/maomu |

## 独点（5 个）
### B1：skill 评测驱动开发——先建 eval 再写文档（来源：Anthropic best-practices）
- 五步：无 skill 跑任务找 gap → 建三个场景 eval → 记 baseline → 写最小指令 → 迭代对照；JSON eval 结构含 skills/query/files/expected_behavior；**无内建评测器，自己搭**。
- 判据：**skill 是从真实失败长出来的，不是从想象需求写出来的**。
- **提升层**：可复用 Skill（评测方法）。

### B2：脚本纪律三件套——solve-don't-punt / 禁 voodoo constants / execute vs read 明示（来源：Anthropic best-practices）
- 脚本显式处理错误（FileNotFound→创建默认，PermissionError→给替代），不把问题抛回给 Claude；常量必须注释理由（"三重重试平衡可靠性与速度"），禁 47/5 魔法数（Ousterhout 定律）；指令里写明"Run analyze_form.py"还是"See analyze_form.py"，默认 execute。
- 判据：**脚本是让模型省脑的，不是让模型背锅的**。
- **提升层**：工具/可复用 Skill。

### B3：AgentMore 四维人设 + 5 Agent 群组 + 技能来源三类（来源：智谱 AgentMore 走搜索）
- 人设=职业+性格+背景+场景四维；最多 5 Agent 群组，头脑风暴/任务分配双模式；技能来源三类：推荐/SkillHub/开源社区，7.4 万+ 免费一键装不耗 token。
- 判据：**协作透明可干预 ≠ 系统派单黑盒**——人设驱动 + 用户可打断。
- **提升层**：Agent 编排。

### B4：skills.sh 三大 skill 家族矩阵——antfu / obra/superpowers / wshobson（来源：skills.sh/trending）
- antfu/skills 30+ 项（vite/vue/pinia/vitest/slidev/unocss）；obra/superpowers 30+ 项（brainstorming/systematic-debugging/test-driven-development/writing-plans/executing-plans/dispatching-parallel-agents/verification-before-completion/using-git-worktrees）；wshobson/agents 40 项（前端/后端/测试/数据库/提示词模式）。
- 判据：**个人 skill 库已规模化到家族级**——按作者看生态，别按单 skill 看。
- **提升层**：生态观察。

### B5：deeplearning.ai 新课程信号——traces→skills 管线 + on-device memory（来源：deeplearning.ai）
- "Building Adaptive AI Agents"：把 agent traces 转成 reusable human-approved skills + code knowledge graph 改善大库检索 + 何时适配模型本身；"On-Device Memory"：Qdrant 向量存 text/voice/image 经验按语义检索。
- 判据：**agent 会话结束不是终点，traces 是 skill 的原料**。
- **提升层**：工作流。

## 判重说明
- B1/B2 → r194-A 已记 spec 硬约束 + validate CLI；取 eval-first 流程与脚本纪律增量。
- B3 → r193-A 已记 AgentMore Reference/Action 分治 + 7.4 万技能；取四维人设/5 Agent 群组/来源三类增量。
- B4 → r194-A 已记 find-skills 2.5M 榜；取 antfu/obra/wshobson 家族矩阵增量。
- B5 → 新课程信号，全新。
