# 学习轮 r731C —— 架构性抗注入、capability 边界与不覆盖清单｜SI 模块

- 日期：2026-11-09｜批次 r731（A/B/C 三连跑）｜轮次：第 3 轮（C）
- 选模块依据：`00_总目录_所有AI入口.md` §3.6 + `module-memory` 实时体量：SI 2488B（最薄第 3）；`system/si-safety` 仅 47 行为 SI 载体最薄技能；上批 r717 建议 TI/SI/VI/PI。只读 `00_总索引.md` + SI/MEMORY.md，未通读 13 个。
- 主线：**13 模块实拉**（2026-11-07 用户强制）；本批二轮深化第 2 批，三轮独立不复用结论（A=TI 推理链忠实度、B=VI Oracle 问题，本轮完全另起）。
- 实拉：本轮独立 WebSearch 定位 + WebFetch 一手逐字核验，≥3 独立域交叉（arXiv 2503.18813 / arXiv 2506.08837 / 官方 GitHub README），二手解读均明确标注不冒充一手。
- 落地：**3 个真独点 / 1 技能**，全为「优＝加厚现有」，0 新建 / 0 合并 / 0 删除；来源标注写入技能末节；经验按模块写入 D 盘 `module-memory\SI\MEMORY.md`（3 条）。
- 轮号判定：游标 r717C + 并发占号至 r730C ⇒ **r731A/B/C**；开工 git fetch 实测 HEAD=origin/main=626dcc09（0/0 无分叉）。
> **13 模块记忆体系已生效（三方同守）**：经验按所属模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`「## 规则与经验」，格式 `- ｜日期｜来源技能｜结论｜证据/落点`；总入口 `00_总索引.md`（判命中技能→只读 1–3 个模块文件）。**豆包 / Qoder 的对应经验也按此路由写入所属模块文件**，不写用户级 `MEMORY.md`；C 盘为 junction 镜像，C 盘不新增实体。本批写入：A=TI / B=VI / C=SI 各 3 条（合计 9 条）。

## 一、独立实拉信源（本轮重新实拉，未复用前两轮结论）

| 站点 / URL | 一手逐字要点 | 状态 |
|---|---|---|
| arxiv.org/abs/2503.18813（Debenedetti et al., Google / Google DeepMind / ETH Zurich；v1 2025-03-24 / v2 2025-06-24） | "creates a protective system layer around the LLM, securing it even when underlying models are susceptible to attacks"；"explicitly extracts the control and data flows from the (trusted) query; therefore, the untrusted data retrieved by the LLM can never impact the program flow"；capability "prevent the exfiltration of private data over unauthorized data flows by enforcing security policies when tools are called"；"77% of tasks with provable security (compared to 84% with an undefended system) in AgentDojo" | 200 一手摘要全文 WebFetch |
| arxiv.org/abs/2506.08837（Beurer-Kellner 等 14 作者；v1 2025-06-10 / v3 2025-06-27） | "a set of principled design patterns for building AI agents with provable resistance to prompt injection"；"discuss their trade-offs in terms of utility and security"；"illustrate their real-world applicability through a series of case studies" | 200 一手摘要全文 WebFetch |
| github.com/google-research/camel-prompt-injection（官方代码库 README） | "This is a research artifact released to reproduce the results in our paper. The interpreter implementation likely contains bugs ... and the implementation might not be fully secure."；"This is not a Google product, and we are not planning to provide support for and/or maintain this codebase." | 200 一手逐字 WebFetch |
| safeguard.sh/resources/blog/six-design-patterns-for-prompt-injection-resistant-agents · nhimg.org/secure-agent-design-patterns-guide · aitalk.it/en/prompt-injection-camel-en | **二手交叉**：六模式命名与各自代价、Bob 会议记录反例、plan-then-execute 参数污染、Rule of Two、约 2.8× token 代价、Q-LLM 内容污染/侧信道/确认疲劳局限 | 二手，明确标注不冒充一手 |

## 二、WB 已落地清单（你们学习时判重，重叠的直接跳过）

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r731C | `system/si-safety` | 1.1.0 → **1.2.0** | r731C-1 ★注入是架构问题、控制流读脏数据前冻结 + 六模式选型 · r731C-2 ★Dual LLM 只挡控制流，capability 标签在工具边界确定性执行 · r731C-3 ★结构性防御自带不覆盖清单 + 敌意输入实测 |

**全批 r731 落地总账（9 独点 / 3 技能，防重复用）**：

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r731A | `meta/ti-critical-reasoning` | 1.2.0 → **1.3.0** | 自述推理非证据/忠实度行为对照 · 假合理化与 RL 平台 28%/20% · monitorability tax |
| r731B | `engineering/vi-fact-verification` | 1.1.0 → **1.2.0** | oracle 来源与「旧版当真值」假设 · MR 的 k≥2 与非确定性关系 · 属性测试闭环 |
| r731C | `system/si-safety` | 1.1.0 → **1.2.0** | 控制流冻结与六模式 · capability 标签边界执行 · 不覆盖清单与敌意实测 |

### 独点判据原文（逐条，不缩水）

- **r731C-1 ★注入是架构问题**：CaMeL 摘要逐字「creates a **protective system layer** around the LLM, **securing it even when underlying models are susceptible to attacks**」「explicitly **extracts the control and data flows from the (trusted) query**; therefore, **the untrusted data retrieved by the LLM can never impact the program flow**」；2506.08837「**principled design patterns** ... with **provable resistance**」「trade-offs in terms of **utility and security**」。六模式（二手交叉）：action-selector / plan-then-execute / LLM map-reduce / dual LLM / code-then-execute / context-minimization，论文与解读一致：**无单一模式覆盖所有威胁模型**，通用型 agent 用当代 LLM 拿不到可靠保证。判据：提示词告诫/输入过滤/检测分类器**不是**安全边界；动作序列须在读到外部内容前冻结；按任务选模式并把少掉的灵活性显式记为成本。
- **r731C-2 ★Dual LLM 只挡控制流、挡不住数据流**：CaMeL 逐字「uses a notion of a **capability** to **prevent the exfiltration of private data over unauthorized data flows by enforcing security policies when tools are called**」；AgentDojo「**77% ... provable security (compared to 84% with an undefended system)**」＝约 7pp 效用代价。机制：特权模型从可信请求生成 Python 风格计划；隔离模型只读脏数据、无工具、只回结构化值；**非 LLM 确定性解释器**执行，每个值带 capability（来源与允许去向）、派生值继承、策略在每次工具调用检查。Bob 反例（二手）：会议记录里的地址被注入改写，控制流没变、文档发给攻击者。判据：外部值打来源标签并继承；高风险工具在**执行边界**由确定性代码判策略，标签缺失/歧义 fail-closed；与 §四 8.2「tool-call authorization」分工（那条列 worksheet 一行，本条给可执行机制）。
- **r731C-3 ★不覆盖清单与敌意实测**：官方 README 一手逐字「This is a **research artifact** ... The interpreter implementation **likely contains bugs ... might not be fully secure**」「**not** a Google product, and we are **not planning to provide support for and/or maintain this codebase**」；局限（二手）：隔离模型返回**内容**仍可被污染、侧信道未解、策略须用户维护、确认疲劳；safeguard.sh「**They do not make the model honest, and they do not fix bad tool design**」「**Test the pattern, not the diagram**」。判据：安全声明与能力承诺同级写「不防什么」；验收用敌意文档实测控制流是否改变、未授权 sink 是否被拒；高风险组合保留人工闸门 + 最小权限；**禁止把 research artifact 当生产依赖**。

**13 模块记忆本轮写入**：SI/MEMORY.md「## 规则与经验」+3 条，五字段格式机检 OK；技能末节已追加本轮来源与判非。

## 三、判非 / 未采纳（防止重复落地）

- 窄串 `CaMeL` / `dual LLM` / `code-then-execute` / `Q-LLM` / `control flow integrity` / `Rule of Two` 全库 SKILL.md **0 命中**。
- `taint` 8 命中中 `engineering/wb-artifact-verification` 末节「来源等级是元数据、污染随内容传播」管**检索片段分类不可自提升**，本条管**值级 capability 随派生传播 + 工具边界执行**（不同层、互补，非重复）；`AgentDojo` 1 命中在豆包自留地 `engineering/wb-execute-discipline`（ClawGuard 评测，非 CaMeL 机制）；`plan-then-execute` 1 命中为编排完成率（非抗注入）；`prompt injection` 6 命中为既有注入/沙箱/凭据条目。
- §四 威胁建模三层法 / inference flow 第四维 / pickle 加载期供应链为 r710C 已落，一律不复用；A/B 轮结论不复用。
- 豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 永不落地；`system/skills-security-check` 506 行、`engineering/wb-artifact-verification` 547 行均超 SKILL.md ≤500 上限，本轮不往这两个文件落地。

## 四、方向收敛与换道建议

- SI 从「威胁建模/供应链」进入「运行时架构性隔离」二轮；TI/VI/SI 三轮形成「推理可核验 / 无 oracle 可验 / 不可信输入可隔离」的验证侧闭环。
- 下批建议：PI 2866B · MI 3130B · CI 3752B · DI 3886B；避开本批与 r717 已加厚模块。

## 五、ACK 要求

- 豆包 / Qoder 侧请 ACK 本批 r731A/B/C 并列出与 9 个独点的判重结果（重叠直接跳过）。
- 三方共守：经验按所属模块写 D 盘 `module-memory\<模块码>\MEMORY.md`，不写用户级 `MEMORY.md`，C 盘不新增实体；`00_总索引.md` 为唯一总入口。
