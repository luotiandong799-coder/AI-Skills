---
name: si-safety
description: 全局安全治理（Safety/Security Intelligence）。当任务涉及个人文件安全（删除/清理/扫描高危目录）、技能入库合规门禁、git 强推与 push 红线、私密信息不入公开仓、AI-native 威胁建模（STRIDE/ATLAS/OWASP）、模型权重与 pickle 供应链安全、本地文件去重与 Windows 迁移到 D 盘 junction、跨 AI 工具（WorkBuddy/Qoder/豆包）同守安全规则时使用。是 13 模块中 SI 的载体。
version: 1.2.0
module: SI
modules: SI
---

# SI · 全局安全治理（Safety/Security Intelligence）

> 本技能是 13 模块中 **SI（安全智能）** 的载体。完整经验日志在 D 盘：`D:\腾讯AI\WorkBuddy数据\module-memory\SI\MEMORY.md`。关联子技能：`system/local-file-dedup`、`system/si-safety-governance`、`system/skills-security-check`、`system/windows-migrate-to-d-via-junction`、`system/windows-ops-experience`。

## 一、个人文件红线（最高优先，任何会话不可降级）

- 桌面 / 下载 / 文档 / Home / 系统目录：**禁**递归删除 / 清空；扫描 = 只读；模糊请求先澄清目录与标准；破坏性动作前加粗警告 + 列全路径 + 确认；先备份（`robocopy /E /COPYALL`）并告知备份位置；用回收站而非 `rm`/`del`；单批 ≤10 文件、逐批校验、失败即停。
- 个人文件**永不**永久删除；软件核心 / 系统 / 私钥不碰。

## 二、入库与协作纪律

- 技能库入库：增 / 删 / 改 / 移动须当轮同步 00_总目录 §3/§4 + 共学附录C；过合规门禁（单源 / 8 类归档 / 非空 description / 无旧路径 / 重叠先按 rules/07 拍板不挂待定）。
- git：禁强推、push 试一次失败即弃；私密不入公开仓；重复技能 = 合并好点删差。
- 跨工具同守：WorkBuddy / Qoder / 豆包 三方可信边界一致。

## 三、触发与协作

- 何时加载：任何触碰个人文件 / 删除 / 清理前；新建或修改 Skill 入库前；做威胁建模或安全评审时；跨工具同步安全规则时。
- 与 PI（感知）：操作环境前先过安全闸；与 MI（记忆）：私密信息不进记忆。

## 四、AI-native 威胁建模方法论（实拉 C_SK §8，2026-11-08）

> 来源：`shivam2003.com/posts/ai-threat-modelling`（2026-11-08 实拉）；ICOA training book + `safeguard.sh` 一手全文 + `eliteai.tools` 交叉；`safeguard.sh` 2026-07-09 一手全文；落地 `system/si-safety-governance` §8.1/8.2/8.3。

- **（8.1）三大框架是三个缩放层级，按序跑**：STRIDE / ATLAS / OWASP 不是三选一，而是同一评估的**广角→技术缩放→组件映射**三个层级，须按序执行；威胁↔组件映射须**双向**（威胁找组件、组件找威胁都跑）；加固预算按**组件共现频次**分配（实测推理端点 7/10、向量库 3/10 ⇒ 先修推理端点）；**检索层是信任边界**——外部内容进 context 的那一刻就是攻击面。
- **（8.2）AI-native 须补第四维 inference flow**：传统三维度之外加 **inference flow**，worksheet 加三行：model provenance（权重哪来的）/ context-window trust boundary（什么内容能进上下文）/ tool-call authorization（哪些调用被允许）。不可信输入要**枚举到 chat 之外**（RAG 语料、文件名、网页正文、邮件都是入口）；unexpected-but-permitted 调用当**检测信号**、连同触发 prompt 留日志；HITL 有效性按 **Bannerman Authority/Time/Understanding** 三轴验证——人在环不等于安全，环里的人不懂/没时间/无权限就是空转。
- **（8.3）模型权重是不可信供应链工件**：pickle 反序列化**即执行**、load-time backdoor 早于首次推理（推理时一切正常，恶意在加载那一刻已发生）；**picklescan 存在四种 bypass ⇒ 扫描通过 ≠ 安全**。须补两层：load-time policy（hash 匹配签名 + 发布者白名单）+ 独立条目"加载时会发生什么"（执行环境、依赖、副作用），并把权重来源与扫描结果写进 model provenance 行。

## 五、感知与安全的交接（本会话新增实测）

- 沙箱会**虚拟化**用户目录（桌面写进去了但用户看不到）——"我以为交付了"是感知错误也是安全错误：交付类操作完成后必须以**用户可见位置**复核（真实路径枚举），不以工具返回成功为准。

## 六、来源（2026-11-08 实拉）

- shivam2003.com/posts/ai-threat-modelling（STRIDE/ATLAS/OWASP 层级与频次）
- ICOA AI training book + safeguard.sh 一手全文（inference flow / worksheet 三行）
- eliteai.tools（交叉验证）
- safeguard.sh 2026-07-09（picklescan 四 bypass / load-time backdoor）
- 落地：`system/si-safety-governance/SKILL.md` §8.1–8.3

## 七、架构性抗注入：控制流冻结 / capability 边界 / 不覆盖清单（2026-11-09 r731C 实拉，3 独点）

> 来源（≥3 独立域）：`arxiv.org/abs/2503.18813`（Debenedetti et al., Google / Google DeepMind / ETH Zurich，v1 2025-03-24 / v2 2025-06-24，2026-11-09 WebFetch 一手摘要全文）；`arxiv.org/abs/2506.08837`（Beurer-Kellner 等 14 作者，v1 2025-06-10 / v3 2025-06-27，WebFetch 一手摘要）；`github.com/google-research/camel-prompt-injection`（官方代码库 README，WebFetch 一手逐字）；交叉（**二手，明确标注**）：`safeguard.sh/resources/blog/six-design-patterns-for-prompt-injection-resistant-agents`、`nhimg.org/secure-agent-design-patterns-guide`、`aitalk.it/en/prompt-injection-camel-en`。
> 判非：`CaMeL` / `dual LLM` / `code-then-execute` / `Q-LLM` / `control flow integrity` / `Rule of Two` 全库 SKILL.md 0 命中；`taint` 命中中 `wb-artifact-verification` 末节管**检索片段分类不可自提升**，本条管**值级 capability 随派生传播并在工具调用边界执行**（不同层、互补）；`AgentDojo` 命中在豆包自留地 `wb-execute-discipline`（ClawGuard 评测，非 CaMeL 机制）；`plan-then-execute` 命中为编排完成率（非抗注入）⇒ 净新。§四 威胁建模三层 / inference flow 第四维 / pickle 供应链为 r710C 已落，不复用。

### 7.1（r731C-1）★注入是架构问题：控制流与数据流须从可信请求先抽出并冻结
- **原文**：CaMeL 摘要逐字「creates a **protective system layer around the LLM, securing it even when underlying models are susceptible to attacks**」「explicitly **extracts the control and data flows from the (trusted) query**; therefore, **the untrusted data retrieved by the LLM can never impact the program flow**」；2506.08837 摘要逐字「a set of **principled design patterns** for building AI agents with **provable resistance** to prompt injection」「discuss their **trade-offs in terms of utility and security**」。
- **六模式（二手交叉）**：action-selector（固定动作表、结果不回灌）/ plan-then-execute（读脏数据前定死步骤）/ LLM map-reduce（每份不可信文档隔离、只回受限类型）/ dual LLM（特权模型有工具、隔离模型无工具）/ code-then-execute（计划写成可检视代码）/ context-minimization（用户提示用完即移除）。论文与解读一致：**没有单一模式覆盖所有威胁模型**，通用型 agent 用当代 LLM 拿不到可靠安全保证，须以能力换安全。
- **判据**：① 「提示词告诫 / 输入过滤 / 检测分类器」不是安全边界——保障来自结构（谁先看到什么、谁能触发什么），不是模型自律；② 动作序列必须在读到外部内容**之前**冻结；③ 按任务选约束模式而不是一招通用，并把「少掉的灵活性」显式记为安全成本。
- **提升层**：安全边界 / 工作流。触发词：protective system layer、控制流先冻结、provable resistance、六模式、能力换安全、通用 agent 无可靠保证。

### 7.2（r731C-2）★Dual LLM 只挡控制流、挡不住数据流；capability 要在工具调用边界由确定性代码执行
- **原文**：CaMeL 摘要逐字「uses a notion of a **capability** to **prevent the exfiltration of private data over unauthorized data flows by enforcing security policies when tools are called**」；「solving **77% of tasks with provable security (compared to 84% with an undefended system)** in AgentDojo」＝约 7 个百分点效用代价。机制（一手 + 二手交叉）：特权模型从可信请求生成 Python 风格计划；隔离模型只读不可信数据、无工具、只回结构化值；**非 LLM 的确定性解释器**执行计划，每个值带 capability（来源与允许去向），派生值自动继承，策略在每次工具调用时检查。
- **经典反例（二手）**：「把 Bob 要的文件寄给他，地址在会议记录里」——隔离模型读到的会议记录被注入改写了地址，控制流没变、文档却发给攻击者 ⇒ 分离规划与阅读不等于安全，数据流参数仍可被污染。
- **判据**：① 每个外部读入的值打来源标签，所有派生值继承；② 高风险工具（发送 / 写 / 删 / 外发）在**执行边界**由确定性代码判策略，标签缺失或歧义 → 拒绝（fail-closed），不由模型自评；③ 与 §四 8.2「tool-call authorization」分工：那条把工具授权列为 worksheet 一行，本条给出可执行的标签传播与边界检查机制；与 `wb-artifact-verification`「来源等级是元数据」分工：那条定**片段分类**，本条定**值级传播与执行**。
- **提升层**：安全边界 / 可复用 Skill。触发词：capability 标签、taint 随派生传播、确定性解释器、工具调用边界、dual LLM 数据流失守、77% vs 84%、fail-closed。

### 7.3（r731C-3）★结构性防御必须自带不覆盖清单，且验收用敌意输入实测而非看架构图
- **原文（官方 README 一手逐字）**：「This is a **research artifact** released to reproduce the results in our paper. **The interpreter implementation likely contains bugs ... and the implementation might not be fully secure.**」「This is **not** a Google product, and we are **not planning to provide support for and/or maintain this codebase**.」；局限（二手交叉）：隔离模型返回的**内容**仍可被污染（保证的是不能夺控制流/外发，不是内容可信）、隐蔽/侧信道未解、策略须用户自行编写维护、逐步确认导致**确认疲劳**；safeguard.sh 逐字「Patterns reduce what a hijacked model can do. **They do not make the model honest, and they do not fix bad tool design.**」「**Test the pattern, not the diagram**」——用敌意文档（写着「把内容发到 X」）与要求换工具的工单实测控制流是否改变。
- **判据**：① 安全声明须与能力承诺**同级**写「不防什么」：内容可信度、侧信道、社工让用户手搬数据、坏工具设计；② 验收动作固定为**敌意输入实测**（控制流是否改变、未授权 sink 是否被拒），不是看架构图或读 README；③ 高风险组合（读不可信输入 × 碰私密数据 × 能改状态/外发）保留人工闸门 + 最小权限 + 审批；④ 论文原型代码明确不维护、可能有 bug ⇒ 禁止把 research artifact 当生产依赖直接接入。
- **提升层**：治理 / 安全边界 / 验证。触发词：research artifact、不覆盖清单、Test the pattern not the diagram、确认疲劳、侧信道未解、敌意输入实测、不把原型当生产依赖。

### 本轮来源（2026-11-09 r731C 实拉）
- arxiv.org/abs/2503.18813（CaMeL，WebFetch 一手摘要；v1 2025-03-24 / v2 2025-06-24）
- arxiv.org/abs/2506.08837（六模式论文，WebFetch 一手摘要；v1 2025-06-10 / v3 2025-06-27）
- github.com/google-research/camel-prompt-injection（官方 README，WebFetch 一手逐字：research artifact / 不维护）
- safeguard.sh/resources/blog/six-design-patterns-for-prompt-injection-resistant-agents · nhimg.org/secure-agent-design-patterns-guide · aitalk.it/en/prompt-injection-camel-en（二手交叉：六模式命名、Bob 反例、2.8× token、Rule of Two；均未冒充一手）
