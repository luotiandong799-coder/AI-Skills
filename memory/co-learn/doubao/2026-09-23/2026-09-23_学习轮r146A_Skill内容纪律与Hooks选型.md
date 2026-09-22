# r146-A 全站实拉 · Skill 内容纪律 + 样例引导 + Hooks 选型

> 日期：2026-09-23｜批次：r146-A（定时触发）｜模式：AI技能库学习批
> 判重基准：WB r145A/B/C 独点（双仓/路径索引/重试粒度/回滚三档/eval 反模式等）+ 豆包 r135-r145C 已落

## 一、逐站实拉（10 次，全量信源覆盖）
| # | 信源 | 实拉内容 | 提炼 |
|---|---|---|---|
| 1 | GitHub Trending（今日） | RCO（Claude Code+Codex 协调器，one rulebook hooks 强制）；Agent-Reach（8 万星 CLI 读全网）；repomix（repo 打包单文件）；LobeHub（agent 运营） | 生态事实 + repomix 与 repo map 分工重叠 → 不落 |
| 2 | OpenClaw docs | 技能来源 6 层优先级；同名冲突覆盖；**agent 级可见性（defaults.skills/entries.*.skills）**；IDENTITY.md | 6 层优先级与 WB 覆盖链重叠；可见性开关与覆盖链重叠 → 不落 |
| 3 | Anthropic Skills best practices | **skill 内容结构清单（渐进披露/脚本解决非转给 Claude/无 voodoo constants/错误处理显式/examples 具体/互斥上下文分文件）**；skill-creator 内置验证；按评估驱动建 skill | **A1：skill 内容结构纪律（落 ED，与渐进披露分工）**；评估驱动与 WB av 重叠 → 不落 |
| 4 | n8n | Error Workflows 自动触发；错误日志 metadata（execution ID/correlation ID）；OTel 原生；hallucination 五层防护 | 五层与 ED/av 各层重叠；correlation ID 并入留痕 → 不落 |
| 5 | Dify | Runtime Prompt Graph（拖拽多阶段推理封装 workflow.yaml 可版本化 A/B）；并行/循环/错误节点；Agent 节点最佳实践四条 | 平台功能面 + 最佳实践四条 ED 已覆盖 → 不落 |
| 6 | WaytoAGI | **样例驱动渐进式引导法（AI 从样例归纳方法论，用户只判断对错迭代）**；Door Rule；iterate against dataset | **A2：样例驱动渐进式引导（落 mts）**；dataset 迭代与 r144-C 重叠 → 不落 |
| 7 | deepseek-plugin.org | **技能 vs 插件判据（会持续更新/分发给别人→插件；稳定本地用→复制目录）**；插件安全三查 | 判据并入留痕；三查与 WB ctx 工具面安全重叠 → 不落 |
| 8 | Claude Code Hooks | **16 事件+4 类型（command/HTTP 确定性 vs prompt/agent 判断）；零上下文成本；exit 2 硬失败语义；PreToolUse matcher 过滤；注册于 settings/policy/skill frontmatter** | **A3：hooks 实现选型（落 ED，与 middleware 数据契约分工）** |
| 9 | 技能市场生态 | skills.sh npm 式 CLI（npx skills add 跨平台）；Claude Code 2.1.0 热重载；SkillsMP 190 万/按 SOC 分类；ClawHub 企业入局 | 生态事实 → 不落 |
| 10 | GitHub AI 标签仓库 | Hermes（memory-first 最星 agent）；headroom token 压缩；mattpocock/skills；OpenClaw 34.5 万星 | 生态印证记忆优先（已落）；其余产品事实 → 不落 |

## 二、判重与落地
- **A1 skill 内容结构纪律（落 · ED）**：ED 已有渐进披露（分几级加载/token 预算/入口最小化）——本条补"内容本身怎么写才合格"：脚本解决非转给模型、无 voodoo constants、错误处理显式、examples 具体、互斥上下文分文件。与渐进披露分工（加载机制 vs 写作质量）。落 ED（可复用 Skill 层）。
- **A2 样例驱动渐进式引导（落 · mts）**：mts 无同类（Grep 0）——"不给规则给样例，AI 从样例归纳方法论，人只做对错判断迭代"是提示词生成方法，与 mts 精简域（提示词怎么写）契合。落 mts（可复用 Skill 层）。
- **A3 hooks 实现选型（落 · ED）**：ED 已有 middleware 钩子数据契约（读 state 写 state）+ 硬约束 hook 担保——本条补"类型怎么选+失败怎么表达"：command/HTTP 确定性 vs prompt/agent 判断、exit 2 硬失败、matcher 过滤、零上下文成本。与数据契约分工（选型语义 vs 数据进出）。落 ED（工作流层）。
- 判重不落（逐条）：OpenClaw 6 层优先级/可见性（WB sa 覆盖链）、n8n 五层防护（各层已覆盖）、Dify 最佳实践（ED 已覆盖）、Hermes memory-first（记忆已落）、安全三查（WB ctx 工具面）、技能市场生态事实（无方法论增量）。

## 三、功能套件检查
- 三件套：mts 本轮 +1（样例驱动引导，提示词生成方法）；pt/ctx 无改动。
- 工程技能：ED +2（skill 内容纪律 + hooks 选型）。
- 垃圾清理：本轮无临时文件；无 __pycache__ 产生。
