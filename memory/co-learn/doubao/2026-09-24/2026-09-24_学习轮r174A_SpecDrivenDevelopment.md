# r174-A Spec-Driven Development：spec 即真相源、四工件闸门、验收标准升格回归测试

实拉时间：2026-09-24 20:19
信源：augmentcode spec+TDD 2026-06 / shiplight SDD loop 2026-08 / copilot-academy spec kit workshop / Microsoft spec-driven spec-kit / specdriven.ai / ai-tldr SDD 2026-06 / dominicode SDD 2026-06 / arXiv 2602.00180 / thebcms SDD guide 2026-05（SDD 组，满 10 站）

## 实拉证据（关键原文）
- shiplight：「the loop, in four moves: write the spec, let the agent implement it, verify the output against the spec, and promote the acceptance criteria into regression tests.」
- specdriven.ai：「Post-merge, any changes start by revising the spec first. Treat specs as version-controlled code.」
- dominicode：tasks.md「converts the plan into atomic, verifiable commits…each task defines what test to write first and what code makes it green.」
- thebcms：`/clarify` 命令让 spec 工具主动问歧义："magic links 单次还是复用？rate limit 按 email 还是 IP？"
- arXiv 2602.00180：GitHub Spec Kit 四阶段 `/specify → /plan → /tasks → implement`，每阶段有闸门。

## 独点清单（3 个真独点）

### 独点1：spec 是唯一真相源，代码只是 spec 的输出（工作流层）
- 判据：先写结构化 spec（要做什么、业务规则、out-of-scope）再让 agent 写一行代码；**改代码前先改 spec**。spec 当 version-controlled code 对待，不写完 spec 不让 agent 动手——比"vibe coding"多的不是文档负担，是可对照验收的基线。
- 独有增量（与 r162C 编码 agent 区别）：那条讲编码 agent 怎么用；本条讲**spec-first 工作流**——四阶段闸门与"改代码先改 spec"的纪律。
- 提升层：工作流。

### 独点2：验收标准在实现前写成测试，实现后升格为回归测试（工作流层）
- 判据：每个任务先写测试（红），再写实现让测试变绿（TDD）；这个测试不是一次性的——验收标准直接升格为回归测试，下次改动自动跑。tasks.md 把计划拆成原子提交，每个提交=一个测试绿+一块真实功能。
- 独有增量：把"写 spec"和"测试"缝在一起——spec 里的验收条件就是测试用例，不是写完代码再补测试。
- 提升层：工作流。

### 独点3：spec 工具主动问歧义，不等用户提（可复用 Skill 层）
- 判据：写 spec 不是一次性吐文档——工具发现 spec 里有歧义（"链接单次还是复用？""限流按 email 还是 IP？"）主动逐条问用户，答完才进入实现。spec 里要含 user story + EARS 验收条件 + out-of-scope。
- 独有增量：spec 写作本身是个对话式澄清过程，不是长篇 PRD 一次成稿。
- 提升层：可复用 Skill。

## 判非重复理由
- r162C 编码 agent 工具用法；本条讲 spec-first 工作流与验收测试一体化，增量 >40%。
