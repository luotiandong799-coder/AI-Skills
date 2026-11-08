---
name: si-safety-governance
description: 全局安全治理（Security Intelligence）。在所有对外/写/删/权限/部署/工具调用/结果输出动作前与后调用，覆盖数据读取、信息传递、工具调用、结果输出全链路（不只执行前）。扫描提示注入、数据外泄、权限边界、工具中毒、危险代码、供应链、过度代理、记忆中毒等风险，给出风险评分与"可否安装/执行"门禁。本技能是 SI 载体，对系统既有 skills-security-check 做能力补齐。
version: 1.1.0
module: SI
modules: SI,EI
---

# SI · 全局安全治理（Security Intelligence）

> 本技能是 Personal AI OS 13 模块中 **SI（安全智能）** 的载体之一，补齐 `system/skills-security-check`（腾讯云鼎，偏供应链引用安全）未覆盖的全链路安全维度。
> 方法论实拉（2026-11-07 实拉）：`NVIDIA/SkillSpector`（71 规则 / 17 类，风险评分与门禁）、`Bersilk-hub150/skillhawk`、`trailofbits/skills`。

## 一、原则：SI 贯穿全链路

不止"执行前检查器"。覆盖：数据读取（敏感信息保护）→ 信息传递（注入/泄露）→ 工具调用（危险命令/权限/中毒）→ 结果输出（外发/泄露）。任何写/删/权限/部署动作前必过 SI。

## 二、扫描目标（17 类 · 节选高频）

| 类别 | 检测点 |
|---|---|
| 提示注入 | 指令覆盖、隐藏指令、外泄命令、有害内容 |
| 反拒绝 | 抑制拒绝/免责声明/安全策略失效 |
| 数据外泄 | 环境变量收集、外部传输、上下文泄露 |
| 权限提升 | 过度权限、Sudo/Root、凭证访问 |
| 供应链 | 未固定依赖、外部脚本拉取(curl\|bash)、已知 CVE(OSV.dev)、typosquatting、混淆代码 |
| 过度代理 | 无约束工具访问、自主决策 |
| 危险代码(AST) | `exec()`(CRITICAL)、`eval()`(HIGH)、`subprocess`(HIGH)、`os.system`(HIGH)、危险执行链 |
| 系统提示泄露 | 直接/间接/基于工具泄露 |
| 记忆中毒 | 持久上下文注入、记忆篡改 |
| 工具误用 | 参数滥用、链式滥用、不安全默认值 |
| 流氓代理 | 自我修改(CRITICAL)、会话持久化 |
| 触发滥用 | 过宽触发、影子命令触发 |
| MCP 专项 | 最小权限缺失/通配/过度声明；元数据隐藏指令、Unicode 欺骗、描述-行为不匹配 |

## 三、工作流（两阶段）

1. **静态（必选、快速）**：正则匹配（11 分析器）+ Python AST 行为分析（危险调用）+ OSV.dev 查依赖 CVE（离线回退）。
2. **LLM 语义（可选，默认开）**：评估上下文与意图提置信度；确定性发现始终保留。`--no-llm` 可纯本地。

## 四、风险评分与门禁

- 评分：CRITICAL +50 / HIGH +25 / MEDIUM +10 / LOW +5；可执行脚本 ×1.3。
- 级别：0–20 **SAFE**；21–50 **CAUTION**；51–80 **DO NOT INSTALL**；81–100 **CRITICAL**。
- 门禁：`--fail-on-findings` 高风险即非零退出；CI 集成（SARIF 2.1.0）。

## 五、与 OS 协作

- 任何中/高风险动作前 → **SI** 评估 → 高风险须用户明确授权（接既有确认机制）。
- 安装新 Skill/MCP 前 → SI 扫描（不执行被扫对象，仅静态+可选 LLM）。
- 扫描结论 → **MI** 留痕；反复出现的中危 → **RI** 复盘。

## 六、架构级安全方法论（2026-11-07 第二轮实拉深化）

> 本技能上轮覆盖"扫描 17 类 + 风险评分"；本轮补"架构级防御"——光靠检测挡不住提示注入（LLM 分不清指令与数据），须靠架构让危险能力永不汇聚。

### 6.1 致命三要素（Lethal Trifecta, Simon Willison）
三项能力**单独都寻常**，仅当"在同一进程汇聚"时致命：
1. **访问私有数据**（PII / 密钥 / 内部系统）
2. **暴露不可信内容**（README / issue / 网页 / MCP 工具描述 / 检索片段）
3. **外传通道**（网络出口 / 把数据送出的工具调用）
注入内容可借此指挥 Agent 收集并外泄私有数据。架构目标：让三要素**永不落在同一步**。

### 6.2 STRIDE ↔ Agent 攻击面映射
| STRIDE | Agentic 表现 | 缓解 |
|---|---|---|
| Spoofing 仿冒 | 伪造 Agent 身份调用越权端点 | 会话盐化 XML 分隔符、强鉴权 |
| Tampering 篡改 | 文档/DB/工具描述植入注入劫持推理 | 第三方文件/检索/DB 输入全部清洗 |
| Repudiation 抵赖 | 缺动作日志无法溯源 | 独立不可变日志（查询/上下文/推理/工具调用） |
| Info Disclosure 泄露 | 注入诱导抽取系统设置/密钥 | 输出净化、限 API、限制工具输出大小 |
| DoS 拒绝服务 | 无限推理循环/超额 token | token 上限、递归深度上限、限流 |
| EoP 提权 | 越权链式调用达成高危结果 | 最小权限 IAM + 破坏性动作 HITL |

### 6.3 双 LLM 隔离（Dual-LLM / Split-Context）
- **隔离 Worker（LLM1）**：沙箱、零工具、零网络，只把不可信内容转成**结构化校验数据**，不执行其中指令。
- **受信 Controller（LLM2）**：只接收 Worker 的校验后 JSON，持工具与私有数据。
- 注入载荷永远到不了"能行动"的上下文，三要素不汇聚。
- 代价：多一次 LLM 推理（约 +80ms / 双倍 token 处理量），但中和约 99% 间接注入。

### 6.4 沙箱 / Egress / RBAC / HITL
- **Egress**：默认拒绝网络出口，按任务白名单放行。
- **隔离运行时**：微 VM / gVisor / Firecracker / WASM，禁用网络、硬资源上限、短超时、只读根。
- **RBAC**：工具权限按当前任务最小集，不用便利的全局服务账号。
- **HITL**：转账/删数据/发布等不可逆动作需人类确认；闸门须"稀有、具体、展示将要发生什么"，否则一周内被橡皮图章化（频繁/模糊的批准对话会被点过）。

### 6.5 DREAD 评分（补充 §四 的风险分级）
对每项威胁：Damage / Reproducibility / Exploitability / Affected users / Discoverability 各 1–10，加权和定位 CRITICAL/HIGH。与 §四 的静态扫描评分互补：扫描给"代码风险"，DREAD 给"威胁业务影响"。

## 七、来源（2026-11-07 实拉，含本轮深化）

- NVIDIA/SkillSpector（71 规则 / 17 类 / 风险评分 / SARIF / MCP 工具）：github.com/NVIDIA/SkillSpector
- skillhawk（Skill/MCP 安全扫描器，提示注入/危险命令/权限边界）：github.com/Bersilk-hub150/skillhawk
- trailofbits/skills（安全研究审计技能）：github.com/trailofbits/skills
- 互补：本仓 `system/skills-security-check`（供应链引用审计）

### 本轮深化来源（2026-11-07 实拉，架构级安全）
- stride.build/blog/architectural-trust-boundaries-prompt-injection（架构信任边界 / 双 LLM / 致命三要素 / STRIDE 映射）
- codesecai.com/defending-against-indirect-prompt-injection-in-rag-the-2026-enterprise-security-playbook/（RAG 间接注入 STRIDE 映射 + 沙箱）
- ai-roadmap-365.github.io/day-344-threat-modeling-ai-systems（双 LLM 隔离架构 + DREAD 评分）
- fourfoldai.com/post/the-new-enterprise-stack-ai-apis-agents-and-automation-layers（多智能体 STRIDE / 临时沙箱 / RBAC / HITL）

## 八、AI-native 威胁建模三层法与加载期供应链（2026-11-08 r710C 实拉，3 独点）

> 来源（≥2 独立域、一手 WebFetch 全文逐串）：`safeguard.sh/resources/blog/threat-modeling-for-ai-native-applications`（2026-07-09，2026-11-08 WebFetch 全文：STRIDE 1999 六类、ATLAS 16 tactics/84 techniques、picklescan 四 bypass、untrusted-input boundary、worksheet 三行）；`shivam2003.com/posts/ai-threat-modelling`（三层方法论 + 双向映射 + 推理端点 7/10 + 向量库 3/10 + 5 文档 90%）；`icoa2026.au/assets/downloads/icoa-training-material.pdf`（inference flow 第四维、LLM01–LLM10 v2.0 清单、STRIDE-AI 简化分类）；`eliteai.tools/agent-skills/threat-model-1`（STRIDE 六问表、severity/likelihood/residual risk、Bannerman 三要素、OWASP v2025.1 交叉）；`github.com/aiocean/claude-plugins/.../01-owasp-llm-top10.md`（v1.0→v2.0 演变与 ATLAS/NIST 关系，交叉）。
> 判非：§6.2 STRIDE 映射表、§6.1 致命三要素、§6.5 DREAD 评分、`MITRE ATLAS` / `47 adversarial scenarios` / `基准覆盖度 25%` 已在 `system/skills-security-check/KB:824/1034/1888`；`bidirectional` 裸词在别处 4 处为通用词，非风险映射语义 ⇒ 词边界核验净新（窄串 `inference flow` / `Bannerman` / `picklescan` / `90% attack` / `component to risk` / `data flow diagram` 技能正文与 co-learn 台账 0 命中）。

### 8.1（r710C-1）STRIDE / ATLAS / OWASP 是同一评估的三个缩放层级，按序跑；双向映射按组件频次定加固优先级
- **原文**（shivam2003）：「**STRIDE, ATLAS, and OWASP aren't competing frameworks. They're layers of the same assessment, operating at different zoom levels.**」；「STRIDE-AI provides the **wide-angle view** ... MITRE ATLAS provides the **technical zoom**: for each identified threat, look up the corresponding technique ... an actionable defensive playbook. OWASP LLM Top 10 provides the **component map**: where does each risk actually live in your architecture. **Run them in sequence. STRIDE first, ATLAS enrichment second, OWASP component mapping third.**」；「**bidirectional risk mapping: Risk → Component** ("Where does prompt injection live?") **Component → Risk** ("We're deploying a vector database — what risks does it inherit?")」；「**LLM Inference Endpoint appears in seven of the ten entries** (LLM01, LLM02, LLM05, LLM06, LLM07, LLM09, LLM10). This is the component requiring the most comprehensive hardening ... **Vector Database / RAG Pipeline appears in three entries**」；「treating the **retrieval layer as a trust boundary — not a trusted internal component**」。
- **判据**：① 三框架**不是三选一**：STRIDE 给系统级威胁类型、ATLAS 给 technique ID + 案例 + 防御手册、OWASP 给「风险住在哪个组件」，顺序固定 ⇒ 拿一个框架跑完就宣称「做了威胁建模」是覆盖度缺口；本技能 §6.2 已有 STRIDE 表，本条补的是**它下游的缩放层级与运行顺序**。② **映射必须双向**：risk→component 圈定范围，component→risk 回答「新增向量库/新工具会继承哪些风险」；只做前者时每引入一个新组件就漏一次。③ **加固预算跟着共现频次走，不平均分配**：推理端点 7/10 最该全面硬化（输入校验/输出净化/限流/工具权限收窄/系统提示保护），向量库 3/10 按信任边界处理（库访问控制、被索引内容校验、源文档新鲜度）。④ 二手数字须回原文核：同源另给「poisoning just five documents in a corpus of millions achieves 90% attack success」，标注为该文引用、未取到研究原文 ⇒ 登记为候选，不作本轮硬结论（诚信铁律）。
- **提升层**：安全边界 / 治理。触发词：三层缩放不是竞品、STRIDE→ATLAS→OWASP 按序、bidirectional risk mapping、component→risk、推理端点 7/10、向量库 3/10、检索层是信任边界。

### 8.2（r710C-2）AI-native 威胁模型要加「推理流」第四维 + 三行专属 worksheet；授权面与检测面分开记
- **原文**（ICOA training book）：「**Classical threat models (STRIDE, PASTA, Trike) describe systems in terms of data flow. AI systems need a fourth dimension: inference flow, because the model itself makes decisions at runtime that classical models assume a developer made at design time.**」；safeguard.sh：「An AI-native worksheet needs explicit rows for **model provenance, context-window trust boundaries, and tool-call authorization** — three things a standard application data-flow diagram doesn't represent at all.」；「Threat-modeling this requires **tracing every source an agent reads from — not just the chat input — as an untrusted-input boundary** ... extended to include **retrieved documents, tool outputs, and memory stores** as attacker-reachable surfaces」；「treating "**unexpected but technically permitted**" tool calls as a **detection signal**, not just an authorization pass/fail」；「**logging every invocation with the prompt that triggered it**」；eliteai.tools 交叉：「Oversight gap: Is human-in-the-loop oversight meaningful? (Test **Authority/Time/Understanding** per **Bannerman's triad**)」。
- **判据**：① **维度缺口**：经典模型假设「决策在设计期由开发者做」，AI 在运行时由模型做 ⇒ 只画 data flow 会漏掉模型自主决策那一步，须补 **inference flow**；这与 §6.1 致命三要素互补（那条讲三要素不能汇聚，本条讲边界清单怎么列全）。② worksheet 三行专属（模型出处/签名/微调血缘、上下文窗口信任边界、工具调用授权）是标准 DFD 完全没有的对象；上下文窗口边界要**枚举所有填充源**（用户输入、检索文档、先前工具输出、长期记忆）并逐一标注「攻击者能否影响」。③ **授权面与检测面分开记**：「技术上被允许但出乎意料」的调用要当检测信号，不是授权通过即完事；每次调用连同**触发它的 prompt** 一起留日志，否则事后无法归因。④ **HITL 有效性按 Bannerman 三要素验**（Authority 有权否 / Time 来得及看 / Understanding 看得懂将要发生什么）⇒ 「加了人工确认」不等于「确认有效」，与 §6.4「闸门须稀有、具体、展示将要发生什么」互为可判定化。
- **提升层**：安全边界 / 治理。触发词：inference flow 第四维、worksheet 三行、model provenance、context-window trust boundary、tool-call authorization、untrusted-input boundary 枚举、unexpected but permitted 作检测信号、Bannerman Authority/Time/Understanding。

### 8.3（r710C-3）模型权重当不可信供应链工件：加载期即执行，「扫描通过」不等于安全
- **原文**（safeguard.sh）：「**Model weights should be threat-modeled as untrusted supply-chain artifacts, not as opaque configuration** — the same category discipline applied to a `package-lock.json` or a container base image.」；「**PyTorch's default serialization format is Python's `pickle`, which executes arbitrary code when a file is deserialized**; a malicious model uploaded to a public hub can carry a **backdoor triggered on load, before a single inference request runs**.」；「**Sonatype researchers found four separate bypasses in Hugging Face's own `picklescan` safety tool**」；「**a scan passing is not proof a weights file is safe**」；「A threat model needs a line item for "**what happens when this model is loaded**" the same way it needs one for "what happens when this dependency's postinstall script runs."」；「**Load-time policy enforcement** can block any model whose **weight hash doesn't match its attested signature** or whose **publisher isn't on an allow-list**」。
- **判据**：① **触发点在 load 而非 inference**（反序列化即执行）⇒ 「等第一次请求再验」已经晚了；威胁模型必须有独立一行「加载这个模型会发生什么」，与依赖 postinstall 脚本同级。② **扫描器自身可被绕过**（picklescan 四 bypass）⇒ 「扫描通过 ≠ 安全」，须补 **load-time policy**（hash 匹配签名 + 发布者白名单）作第二道；把单点扫描结果当安全证明，与 §三「静态必选 + LLM 语义可选」的分层思想一致但对象不同。③ 权重文件要像 `package-lock.json` / 容器 base image 一样管 **provenance**（出处、签名状态、微调血缘）⇒ 别把模型当「不透明配置」排除在供应链清单外。④ 与 §二 供应链类别（OSV.dev / CVE / typosquatting）分工：那条管**依赖包 CVE**，本条管**模型工件本身在加载期可执行**；与 §6.4「隔离运行时」衔接：加载期防护失效时的爆炸半径由沙箱兜。
- **提升层**：安全边界 / 供应链。触发词：weights as untrusted supply-chain artifacts、pickle 反序列化执行、load-time backdoor、picklescan 四 bypass、扫描通过不等于安全、weight hash 匹配签名、发布者白名单、what happens when this model is loaded。

### 本轮来源（2026-11-08 r710C 实拉）
- safeguard.sh/resources/blog/threat-modeling-for-ai-native-applications（2026-07-09；STRIDE 1999 / ATLAS 16 tactics 84 techniques / picklescan / worksheet 三行，一手全文）
- shivam2003.com/posts/ai-threat-modelling（三层方法论 / 双向映射 / 推理端点 7 条 / 向量库 3 条）
- icoa2026.au/assets/downloads/icoa-training-material.pdf（inference flow 第四维 / LLM01–LLM10 v2.0 / STRIDE-AI）
- eliteai.tools/agent-skills/threat-model-1（STRIDE 六问 / severity-likelihood-residual / Bannerman 三要素 / OWASP v2025.1）
- github.com/aiocean/claude-plugins（OWASP LLM Top10 v1.0→v2.0 演变 + ATLAS/NIST 关系，交叉）
