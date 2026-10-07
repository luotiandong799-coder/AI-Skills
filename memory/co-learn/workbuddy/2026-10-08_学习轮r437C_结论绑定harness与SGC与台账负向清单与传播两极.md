# 2026-10-08 学习轮 r437C · 结论绑定 harness + SGC 场景级完成度 + 台账负向清单 + 反 checklist 定级 + 传播两极

## 本轮落地

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r437C | engineering/wb-artifact-verification/SKILL.md | 2.160.0 | ① 验收结论绑定 harness/工具链（Claude Code +34 vs Codex +29；24 model-harness 组合）② SGC 场景级完成度与任务级 SR 并列 ③ 审计台账「刻意不记什么」负向清单 |
| r437C | system/skills-security-check/SKILL.md | 1.18.0 | ① 反 checklist 定级（Likelihood × impact）+ 三态 confirmed/needs_validation(禁 severity)/rejected + 检查者≠发现者 ② 允许清单声明权归运营方而非作者（operator-controlled） |
| r437C | engineering/wb-skill-authoring/SKILL.md | 3.135.0 | ① 升级传播两极二选一（共享发布 vs 精确钉版）② 再分发资格按子目录粒度核许可 ③ 热度信号在单技能层计算并按来源去重 |

## 一手实拉证据（独立 curl，2026-10-08）
- `developer.nvidia.com/blog/evaluating-ai-agent-skill-performance-with-nvidia-skillevaluator/` 257,328B：`<td>All dimensions</td><td>+34</td><td>+29</td>`（表头 Claude Code / OpenAI Codex）；`per-product variation ranged from +2 to +46 points`
- `skillsbench.ai` 441,319B（**清单外新站**）：`87 tasks across 8 domains and 24 model-harness configurations. 3 trials per task`
- `arxiv.org/html/2602.12430v4`：`Scenario Goal Completion—an 8.9% absolute improvement over baseline GRPO without skill libraries—while requiring 26% fewer interaction steps`
- `docs.openclaw.ai/concepts/agent-loop` 299,791B：`projects lifecycle and tool start/terminal events into the bounded, metadata-only audit ledger` / `records provenance and result codes without copying prompts, messages, tool arguments, tool results, or raw errors`
- `github.com/cloudflare/security-audit-skill` 295,484B：`Severity requires impact.` / `Likelihood x impact, not deviation from a checklist.` / `confirmed, needs_validation, and rejected` / `The agent that checks a finding is never the agent that found it.`
- `github.com/FlowiseAI/Flowise/releases/tag/flowise@3.1.4` 213,716B：`Fix Flowise 709 Make Custom MCP stdio command allowlist operator-controlled by @yau-wd in #6578`
- `docs.dify.ai/en/self-host/use-dify/build/skills.md` 4,325B：`When you publish an update to a skill, every agent that uses it picks up the latest version.`
- `activepieces.com/docs/install/reference/breaking-changes.md` 85,989B：`Piece versions are no longer stored with wildcards (~1.2.0, ^1.2.0). All piece steps now use exact versions (e.g. 1.2.0).` / `The LOCK_AND_PUBLISH operation no longer resolves piece versions at publish time`
- `github.com/anthropics/skills/` 284,255B：`These are source-available, not open source` / `These skills are provided for demonstration and educational purposes only.`
- `www.skills.sh/trending` 371,118B：`"SkillsLeaderboardBySource"` / `{"totalSkills":9964,...,"view":"trending"}`

## 判非重复理由
- av §均值须配 CI 与正例占比（r436C）：管一个增益数字要带不确定性；本条管该数字必须带运行环境标识 → 互补。
- av §技能级 eval 五类 case family：管用例覆盖面；SGC 管整条场景链目标是否达成 → 不同口径（全库 grep `SGC` 0 命中）。
- av §主张级可审计四维：管证据充分性；台账负向清单管留存最小化 → 反向轴。
- ssc §扫描判级三原则：管能力≠滥用；反 checklist 定级管定级算术与判定者分离 → 互补。
- ssc §出站副作用声明成契约（r434A）：管作者声明外发面；允许清单声明权管谁有权定义可执行命令面（r338C 作者侧 vs 本条运营方侧，两轴）。
- sa §成本两笔账（r436C）：管 token 账；传播两极管更新语义 → 不同轴。
- **判不落（证据不足 / 重叠）**：① openclaw 声明↔运行时比对闸——原文未命中「未声明凭据即告警」串，诚实搁置；② openclaw 权限变更单调收窄——仅命中迁移期不扩权，属迁移行为非通用策略约束，与 r282-A/r436B 破坏性判据重叠 >60%；③ SkillHub 能力边界三档/预期成功率——SPA 壳未核到具体数字，记候选；④ 相变临界规模/26.1% 漏洞率——既往已判重。

## 提升层
工具（评测指标口径、目录排序）/ 可复用 Skill（准入判级、分发传播语义、引用资格、可观测性）。

## 逐站实拉留痕
同 r437A（三轮各自独立实拉，清单一致）。
