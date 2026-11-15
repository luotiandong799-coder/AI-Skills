---
name: si-safety-governance
description: 全局安全治理（Security Intelligence）。在所有对外/写/删/权限/部署/工具调用/结果输出动作前与后调用，覆盖数据读取、信息传递、工具调用、结果输出全链路（不只执行前）。扫描提示注入、数据外泄、权限边界、工具中毒、危险代码、供应链、过度代理、记忆中毒等风险，给出风险评分与"可否安装/执行"门禁。本技能是 SI 载体，对系统既有 skills-security-check 做能力补齐。
version: 1.6.0
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

## 九、构建产物来源证明：SLSA 是分级递进、不传递、消费者自判（2026-11-11 r735B 实拉，3 独点）

> 定位：本组管「**这个工件是不是按预期方式、由预期的源构建出来的**」（provenance 消费侧验证）；与 §8.3「模型权重加载期即执行」（加载期行为）、§二供应链类别（依赖 CVE / typosquatting）、`skills-security-check` 的技能身份四元组（运行时归属）分工——那几条分别管"加载了会怎样""依赖有没有已知洞""这次回调是谁"，本条管"产物与构建过程的可追溯证明"，且明确声明它**不回答"里面装了什么"**。

### 9.1（r735B-1）SLSA 是分 track 的递进保证，级别不传递、判定权在消费者
- **原文**（`slsa.dev/spec/v1.0/levels` 官方一手 WebFetch 200 全文逐字）：「SLSA levels are split into **tracks**. Each track has its own set of levels **that measure a particular aspect** of supply chain security」；「**SLSA is intended to be a primitive in a broader determination of a software's risk.** SLSA measures specific aspects of supply chain security, particularly those that can be fully automated; **other aspects, such as developer trust and code quality, are out of scope**. Furthermore, **each link in the software supply chain has its own, independent SLSA level — in other words, it is not transitive**」；「**SLSA alone is not sufficient to determine if an artifact is "safe"**」；「Finally, **SLSA is in the eye of the beholder: software consumers ultimately make their own SLSA determinations**, though in practice they may delegate to some authority」。Build 轨 L0（无）/L1（Provenance exists，防 mistakes·documentation）/L2（Hosted build platform，防 tampering **after** the build）/L3（Hardened builds，防 tampering **during** the build）；v1.0 把 Source 面移除，只留 Build track（官方注记「For version 1.0 the Source aspects were removed to focus on the Build track」）。
- **判据**：① **别把"达到 Build L3"当成"这个包安全"**——L3 只保证构建期抗篡改与 provenance 可信，开发者可信度、代码质量、依赖漏洞都在 out of scope；与 §8.3「扫描通过≠安全」同构但对象是构建链而非加载器。② **级别不沿供应链传递**：上游依赖是 L3 不等于我的产物是 L3，本条链路每一环单独定级；验收表要按环节列级，不写一个总级。③ **谁消费谁判定**：生产方「声称 conform to Build L3」不构成结论，消费方须自行验证或显式声明委托给哪个权威（与 `wb-artifact-verification` 的「单一事实源」/「校验两端同源自证恒真」呼应）。④ 门禁输出必须同时写「本条证明了什么 / 不证明什么」清单，避免把框架层级当安全评级。

### 9.2（r735B-2）分级的实质是「谁签名、签名密钥能否被构建步骤碰到」；L1 的证明可未签名、可伪造
- **原文**（同上官方全文）：L1「**Provenance may be incomplete and/or unsigned at L1.** Higher levels require more complete and trustworthy provenance」「Can be used to **prevent mistakes but is trivial to bypass or forge**」；L2「builds run on a **hosted platform** that generates and **signs** the provenance」「Build platform runs on **dedicated infrastructure, not an individual's workstation**」「Downstream verification of provenance includes **validating the authenticity** of the provenance」；L3「prevent **runs from influencing one another, even within the same project**」「prevent **secret material used to sign the provenance from being accessible to the user-defined build steps**」；构建轨三步「**Set project-specific expectations** for how the package should be built / **Generate a provenance attestation automatically during each build** / **Automatically verify** that each package's provenance meets expectations **before allowing its publication and/or consumption**」。ACE Journal（一手 WebFetch 200 全文）：GitHub Actions OIDC → Sigstore Fulcio CA 签名 → 公共 Rekor transparency log；`slsa-verifier` / `cosign verify-attestation --type slsaprovenance`（OCI 1.1 referrers API）；Kyverno / OPA Gatekeeper 在 admission 时拒绝证明缺失或验证失败的镜像；「**requires pinning to image digests, not tags, because a tag can be silently repointed to a different digest with no audit trail**」。
- **判据**：① **"有 provenance"与"provenance 可信"是两件事**：L1 只防误构建（如从不存在的 commit 构建），未签名即等于可伪造；验收时先问"谁签的、签名密钥在不在构建步骤可达范围"，再谈级别。② **验证必须发生在消费点**（registry pull / Helm fetch / dependency resolution / admission controller），不是发布时看一眼签名文件；与 §8.3「加载期 policy」互补：那条在装载瞬间兜底，本条在准入前拒绝。③ **按 digest 固定、不按 tag**——tag 可被静默重定向，与 `wb-execute-discipline`「pinned revision 不用 latest」同族，但本条给的是标准层理由与配套验签工具链。④ 期望值（canonical source repo / build command）要在构建前声明并纳入自动比对，否则证明存在也无法判"是否符合预期"。

### 9.3（r735B-3）provenance 与 SBOM 是互补的两份证据，缺一不能声称供应链已验
- **原文**（ACE Journal 一手全文「Dependency Provenance and the SBOM Gap」）：「**SLSA addresses build provenance but does not itself solve the problem of knowing what is inside an artifact.** That gap is filled by **Software Bills of Materials (SBOMs) in SPDX or CycloneDX format**, generated by tools like Syft or trivy's SBOM mode」；「**the provenance proves the build was not tampered with; the SBOM enumerates the components inside** so vulnerability scanners like Grype can match against the CVE database」；「The **CISA Secure Software Development Attestation Form** ... **now expects both signals**」；「Treating SLSA and SBOM generation as **separate pipeline steps** wired together by a signing and attestation layer is the pattern that scales」。官方首页（`slsa.dev`）交叉：「The first on-ramp to SLSA is **generating provenance**」。
- **判据**：① **门禁两栏分开收证据**：「怎么构建/是否被篡改」→ provenance；「装了哪些组件/有没有已知 CVE」→ SBOM + 扫描。只交一栏不许写"供应链已审"。② 二者各自签名并绑定同一 artifact digest，否则两份证据可能指向不同工件（与 §9.2「pin digest」衔接）。③ 与 §二供应链（OSV.dev/CVE）、§8.3（权重文件）分工明确：§二是清单内容、§8.3 是加载期执行、本条是构建链证明，**三处不在同一功能位并存**，按 rules/07 去重铁律登记为正交补齐。④ 声明适用范围：本条面向「可构建的软件工件/容器镜像/技能包」，对纯文档、运行时生成内容不适用，不硬套。

### 本轮来源（2026-11-11 r735B 实拉）
- `slsa.dev/spec/v1.0/levels` — 官方规范一手 WebFetch 200 全文逐字（tracks / not transitive / in the eye of the beholder / out of scope / L0–L3 要求与收益 / 构建轨三步）。
- `slsa.dev/spec/v1.0-rc1/levels`、`slsa.dev/spec/v1.0-rc1/onepage`、`slsa.dev/` — 搜索快照逐串交叉（L1 unsigned、L3 隔离、Source track 移除、首个 on-ramp 是生成 provenance）。
- `www.acejournal.org/2026/01/27/slsa-supply-chain-levels-in-practice` — 一手 WebFetch 200 全文（Sigstore Fulcio/Rekor、slsa-verifier、cosign verify-attestation、Kyverno/OPA、pin digest、SBOM gap 与 CISA 双信号）；**行业期刊立场（厂商导流倾向）已标注，判定性结论一律以官方规范为准**。
- `marklodato-slsa.netlify.app/spec/v1.0-rc1/levels` — 规范作者镜像，搜索快照交叉佐证，不作唯一依据。

## 十、凭据泄露检出的边界与处置顺序（r739C 实拉 · 2026-11-14）

> 与 §九（SLSA 分 track / 签名者密钥可达性 / provenance 与 SBOM 双栏）分工：§九管**构建产物的来源证明**，本节管**凭据泄露的检出面与检出之后怎么办**；同属供应链安全族，但两者一个证明「东西从哪来」，一个回答「钥匙漏没漏、漏了先做什么」。豆包自留地 r275A 已把 secret scanning / push protection 作为 GHAS 功能清单登记，本节不重复功能介绍，只取官方未覆盖清单与检出失效面。

### 10.1 push protection 是 push 面的模式匹配，不是凭据边界
GitHub Docs 官方逐字：它「blocks pushes that contain secrets **before** they reach your repository」，拦的是四类——partner patterns（「where push protection is supported for that secret」）、**需显式启用**的 generic patterns（私钥 / 数据库连接串）、custom patterns（自定义正则，须逐个选择启用）、AI-detected unstructured secrets（**public preview and subject to change**）。官方另列五种 push surface（命令行 / Web UI commit / 文件上传 / REST API / GitHub MCP server **仅 public repositories**）。

=> 覆盖集 = 模式表 ∩ 启用状态 ∩ push surface，不是「仓库里没有密钥」。dev.to 逐字：「**Push protection is a pattern match at the remote**」「Push protection does not block what it cannot name」「GitHub's scanner is a good delay. **It is not a boundary**」；`DATABASE_URL`、无厂商前缀 bearer、自建 API key、`.env`/`mcp.json` 里的 `env` 块都不在默认集合；密码类「push protection and validity checks are not supported」（checkyourvibe 2026 独立一手）。GitGuardian 口径：generic credentials 占检出泄露 **58%**（该统计仅作规模佐证，不搬为其结论）。

判据：门禁声明必须写出「本次扫描面」（哪些 push surface / 哪些模式已启用），把「已开 push protection」写成「仓库已无凭据泄露风险」是范畴错误。CI 侧须另跑 gitleaks / trufflehog 扫**全历史**与 GitHub 看不见的文件（未被 git 跟踪的 `.env`、CI 日志、构建产物、容器镜像、托管面板、Slack/Jira 工单）——safeguard.sh 独立一手逐字：「Secret Protection only sees what happens inside a GitHub-hosted git push」。

### 10.2 bypass 理由决定告警是否可见，这是治理盲区不是界面细节
官方表逐字：默认「**anyone with write access** to the repository can bypass push protection by specifying a bypass reason」；三种理由的告警行为分别是——`It's used in tests` → **创建已关闭告警**（resolved as used in tests）、`It's a false positive` → **创建已关闭告警**、`I'll fix it later` → 创建开放告警。即三条路里两条不产生待办、不触发跟进通知；「The control then becomes a **dialog, not a gate**」（dev.to）。收紧手段是 delegated bypass，官方给三档：bypass privileges（可自批 + 审批他人请求）/ exemption from push protection（完全不触发）/ 组织级指定哪些模式纳入。

判据：验收不能只查「有没有开 push protection」，还要查「bypass 权限面」与「关闭态告警是否进入审计视图」。把「扫描到了」推成「有人会处理」是错的——理由字段本身就能让告警静默落地。与 §Cap95「拒绝规则的匹配面必须显式声明」同族：这里要问的是「告警的落地状态由谁决定」。

### 10.3 检出后先轮换再清历史；两类动作不可互换
GitHub Docs 官方逐字：「**rotate the affected credential immediately** ... While you can also remove secrets from your Git history, this is **time-intensive and often unnecessary if you've already revoked the credential**」。理由在历史面：secret scanning 扫「your entire Git history on all branches」并告警，但 **push protection 不会 un-commit**——cloudspress/rottenwifi 两篇独立一手逐字：「a later commit that deletes a token leaves the original token in the earlier commit, so it still triggers protection」，必须从**每一个**含该值的 commit 里移除（tip 用 amend、更早用 interactive rebase）。dev.to 交叉：「64 percent were still valid in January 2026」（2022 年首见的密钥）、「**Rotate on alert. Do not wait for a rewrite of git history. The credential is the asset. The commit is the evidence.**」

另有三类常被漏的传播面：① **private-to-public flip**——私有仓期间写入的密钥在可见性翻转那刻全部公开（内部仓含硬编码密钥概率为公开仓 6 倍，GitGuardian 口径）；② **fork 不随父仓轮换**——「Forks copy the blob ... Secret scanning on the parent does not fan out a revoke to every fork」；③ 公开 gist 与 secret gist 同样在扫描范围，但「It does not make the gist private for you」。

还有一组易混：**validity check ≠ partner notification**。官方逐字：validity check 是「checking whether detected secrets are still **active**」（回问发行方，用于排优先级，返回 active/inactive/unknown）；partner notification 是「we **notify the provider** so they can take action, such as revoking the credential」，且「Partner secrets are reported directly to the provider and **aren't displayed in your repository alerts**」。dev.to：「Mix the two and the team waits for a vendor. **The vendor never sees a custom API key.**」

判据：处置顺序固定为「轮换/吊销 → 查发行方访问日志 → 再决定是否重写历史 → 按真实原因关闭告警」；被拒的 push **不等于**凭据安全（值已离开本机，须按已暴露处理）。告警优先级 ≠ 修复：validity=inactive 只说明这把钥匙不能用了，不说明没被用过；「清理历史」与「使凭据失效」是两个独立验收点，缺一不得写「已处置」。

**来源（r739C 独立实拉 2026-11-14，≥2 独立域交叉）**：
- `docs.github.com/en/code-security/concepts/secret-security/secret-scanning`（GitHub Docs 官方，WebFetch 200 全文逐字：全历史扫描范围、partner integration、rotate immediately、validity checks 定义）
- `docs.github.com/en/code-security/concepts/secret-security/push-protection`（GitHub Docs 官方，WebFetch 200 全文逐字：四类模式、五种 push surface、bypass 三理由告警行为表、delegated bypass 三档）
- `dev.to/rxkov/github-push-protection-is-a-pattern-match-not-a-secrets-boundary-2bf3`（2026-09-18 独立一手全文逐字：pattern match not boundary、四个洞、validity check ≠ partner notification、rotate on alert、fork/gist 传播面）
- `www.safeguard.sh/resources/blog/github-secret-protection-deep-dive-push-protection-custom-patterns-validity-checks`（独立一手全文：active/inactive/unknown、扫描范围外清单、回溯积压）；`checkyourvibe.dev/blog/how-to/secret-scanning`（2026 独立一手：密码不拦、旧格式 token 不拦、可绕过、处置顺序）；`cloudspress.com` + `rottenwifi.com`（两篇独立一手：删除 commit 无效、须逐 commit 移除）
- 立场登记：safeguard.sh / checkyourvibe.dev 均为安全厂商内容，产品宣传段判非；GitGuardian 统计数字仅作规模佐证，不作为本轮结论依据。


## 十一、软件更新是独立攻击面：TUF 四类攻击、有序检查链与它不证明什么（r743C 实拉 · 2026-11-14，3 独点）

> 与 §九（SLSA/provenance）、§十（push protection）分工：SLSA 证明「这个工件怎么被构建」，push protection 是「提交面的模式匹配」，TUF 防「客户端拿到的**是不是当下该拿的那一份**」。三者覆盖供应链的三个不同面，按 rules/07 登记为补齐而非并存。

### 11.1（r743C-1）包签名 ≠ 更新安全：攻击面在元数据与时间，不在包体
- **原文**：TUF 官方规范 1.0.37（Last modified 8 October 2026）§1.5.2 逐字列出攻击目标：**Rollback attacks**「An attacker cannot trick clients into installing software that is **older than that which the client previously knew** to be available」/ **Indefinite freeze attacks**「without the client being aware of the problem」/ **Mix-and-match attacks**「a **combination of metadata that never existed together** on the repository at the same time」/ Fast-forward / Arbitrary installation / Endless data / Extraneous dependencies / key compromise / wrong software。safeguard.sh 逐字「The SolarWinds attack **didn't exploit a bug. It exploited trust** ... signed with SolarWinds' **legitimate code signing certificate**」「The old version is **legitimately signed, so signature verification passes**」「The client continues running an outdated, vulnerable version while **believing it's up to date**」。
- **判据**：① 验收清单逐问三件事：**旧版本能否被重放 / 陈旧元数据能否一直喂 / 不同时期的元数据能否混搭**；只答「有签名、走了 HTTPS」视为未覆盖。② 规范自陈边界逐字「When saying the framework protects against an attack, it means **the attack will be unsuccessful. It does not mean that a client will always successfully update during an attack** ... the framework **must detect when a client is unable to update**」⇒ 「装不上」与「被攻击但已检出」是两种成功/失败，不得把检测失败写成更新成功。③ 与 §9.1 SLSA「证明了什么/不证明什么」同构：安全声明同级写「不防什么」。

### 11.2（r743C-2）检查链是四道有序门，每道各自 fail-closed
- **原文**：TUF 官方规范 §5.5/5.6 逐字「**Check for a rollback attack.** The version number of the targets metadata file ... **MUST be less than or equal to** its version number in the new snapshot metadata file. Furthermore, any targets metadata filename that was listed in the trusted snapshot metadata file ... **MUST continue to be listed** ... discard the new snapshot metadata, abort the update cycle」；「**Check for a freeze attack.** The expiration timestamp in the new snapshot metadata file **MUST be higher than the fixed update start time** ... If the new snapshot metadata file is expired, discard it, abort the update cycle, and **report the potential freeze attack**」；「Check against snapshot role's targets hash ... This is done, in part, **to prevent a mix-and-match attack** ... **It is safe to check the hashes before the signatures, because the hashes come from the snapshot role, which we have already verified in the previous step**」；THRESHOLD 逐字「each SIGNATURE which is counted towards the THRESHOLD **MUST have a unique KEYID. Even if a KEYID is listed more than once** in the "signatures" list a client **MUST NOT count more than one verified SIGNATURE from that KEYID**」。
- **判据**：① 客户端验收固定顺序 **root → timestamp → snapshot → targets**，每步逐项写「版本号 / 过期时间 / 哈希 / 阈值签名」四项的失败动作（discard + abort + 报告具体攻击名），不许合并成一句「验证通过」。② 新鲜度锚是 **fixed update start time**（本次更新开始时刻），不是检查时的当前时钟——否则长时间更新会被合法喂入过期元数据。③ 同一 KEYID 的重复签名不得凑数达阈值；哈希可先于签名校验的前提是**上一环已验证**，顺序不可任意调换。④ 与 §Cap95「拒绝规则匹配面须显式声明」同族：写出每道门比对的是哪个字段。

### 11.3（r743C-3）freshness 是运维承诺，角色分离是妥协边界，且 TUF 不证明构建完整性
- **原文**：TUF 官方 §1.5 逐字「**online keys ... must not be used for any role that clients ultimately trust for files they may install**」「The root role's private keys **MUST be kept very secure and thus should be kept offline**」，四顶层角色 Root / Targets / Snapshot / Timestamp（另有可选 Mirrors）。hivebook 逐字「**TUF secures delivery, not build integrity** — it ensures clients get authentic, fresh, consistent artifacts; it does not attest how those artifacts were built (that's in-toto)」「**Metadata expiration must be maintained** ... you need automation to re-sign them on schedule or **clients will (correctly) refuse stale metadata and updates stall**」「**Root key management is the whole ballgame**」；分工表逐字 TUF=update/distribution channel / in-toto=build pipeline provenance / Sigstore=artifact signing + transparency log，且「**Sigstore itself uses a TUF root to bootstrap trust in its keys**」。hivebook 一手勘误实证：Docker Notary v1 于 2025-07-31 归档、`notary.docker.io` 2026-12-08 关停、PEP 458 仍 `Accepted` 未实现、PyPI 实际发布的是 PEP 740 attestation、RubyGems PR #719 关闭未合。
- **判据**：① 过期即拒收是**设计**不是故障 ⇒ 严禁为「先让更新跑起来」临时关掉过期检查（与 Cap87「新能力不得绕过宿主既有策略」同向）；须配自动重签作业并监控到期。② 角色/密钥按职责分离，在线密钥不得签客户端最终信任的角色；root 密钥离线 + 阈值 + 轮换仪式。③ 「已采用 TUF」这类现状断言须核**官方 adoptions 列表**，不引二手摘要（hivebook 逐条勘误四类误传即反例）；与 Cap76「误读澄清同表同级」同族。④ 与 §九/§十分工写成一行：构建溯源（SLSA/in-toto）· 交付新鲜度（TUF）· 凭据检出（push protection），缺任一不得写「供应链已验」。

**来源（r743C 独立实拉 2026-11-14，≥2 独立域交叉）**：
- `theupdateframework.org/specification/`（TUF 官方规范 **v1.0.37 / Last modified 8 October 2026**，WebFetch 200 逐字：§1.5.2 九类攻击目标与「does not mean a client will always successfully update」边界、§1.5 online keys 限制、§2.1 四顶层角色、root 离线、§5.5/5.6 rollback/freeze/mix-and-match/THRESHOLD 检查链；**主 spec 页 AI 摘要 60s 超时返回前 15000 字，如实登记**，§5 段由 `.io` 镜像页与搜索快照逐字交叉补足）
- `theupdateframework.io/specification/latest/` + `theupdateframework.com/specification/draft/`（官方规范两独立镜像，搜索快照逐字命中同一检查链，双域交叉）
- `hivebook.wiki/wiki/tuf-the-update-framework-secure-software-updates`（2026-09-22 复核的独立一手条目：四角色表、Gotchas、TUF/in-toto/Sigstore 分工表、Notary/PEP458/PEP740/RubyGems 四条勘误）
- `safeguard.sh/resources/blog/software-update-mechanism-security`（独立一手全文逐字：SolarWinds「exploited trust」、rollback 旧版本仍合法签名、freeze 客户端自以为最新、role separation/threshold/expiration/consistent snapshots 五机制）
- 立场登记：hivebook 为 AI 知识库条目（自带 verified 标注与复核日期），Safeguard.sh 为安全厂商内容，二者均不作唯一结论来源；核心机制以官方规范为准。

## 十二、MCP 授权同意流时序与令牌受众绑定（r749C 独立实拉 2026-11-15）

> **换道说明**：本轮原拟「MCP 工具投毒 / rug pull / 工具影子」，判重扫描发现已由豆包自留地 `engineering/wb-execute-discipline`（r589C 描述即注入面、r650A 连接即加载）与 `defaults/wb-context-compressor`（OWASP MCP 清单、description/schema pin）、以及 `engineering/wb-artifact-verification`（MCP 规范 annotations 不可信实证）、`defaults/wb-ponytail`（listChanged 清单会变）覆盖 ⇒ 按 rules/07 去重铁律四态判「**换道**」，改取官方授权规范与安全最佳实践的**同意流时序 + 令牌受众绑定**，与上述内容注入面正交。
> 与 `system/mcp-builder` §2026-09-24（OAuth 2.1 / 受众绑定 / 签发者 / 细粒度范围，豆包 r159-B 实拉）分工：那条管「**建 MCP server 时按 OAuth 2.1 怎么配**」；本节管「**同意流在哪一步设 `state`、consent cookie 绑谁、代理服何时必须重新征询、令牌不得透传的审计后果**」。与 §九（SLSA 构建溯源）/ §十（push protection 提交面检出）/ §十一（TUF 交付新鲜度）分工：本节是**授权与身份面**，四者缺一不得写「供应链已验」。

### 12.1（r749C-1）令牌受众是「签给谁」不是「签名有效」；RFC 8707 resource 必须双位置出现
- **原文**：MCP 官方《Authorization》（2025-06-18 版）逐字「MCP servers **MUST** validate access tokens ... **MUST validate that access tokens were issued specifically for them as the intended audience**, according to RFC 8707 Section 2. **If validation fails, servers MUST respond according to OAuth 2.1 Section 5.3 ... Invalid or expired tokens MUST receive a HTTP 401 response**」「MCP clients **MUST NOT** send tokens to the MCP server other than ones issued by the MCP server's authorization server」「**MCP servers MUST NOT accept or transit any other tokens**」「MCP clients **MUST** implement Resource Indicators for OAuth 2.0 as defined in **RFC 8707** ... The `resource` parameter: 1. **MUST be included in both authorization requests and token requests** 2. **MUST identify the MCP server** that the client intends to use the token with 3. **MUST use the canonical URI** of the MCP server」「Note that authorization **MUST be included in every HTTP request from client to server, even if they are part of the same logical session**」「Access tokens **MUST NOT** be included in the URI query string」；另逐字「**MUST** only accept tokens specifically intended for themselves and **MUST reject tokens that do not include them in the audience claim**」「The access token used at the upstream API is **a separate token, issued by the upstream authorization server**. The MCP server **MUST NOT pass through the token it received from the MCP client**」。两类失效逐字「**Audience validation failures** ... may accept tokens originally issued for other services. This **breaks a fundamental OAuth security boundary**」「**Token passthrough** ... can potentially cause the 'confused deputy' problem」。
- **判据**：① 门禁固定四问：**令牌受众是否本服务 / `Authorization` 是否每次请求都带 / 令牌是否出现在 URI query / 无效或过期是否 401**；把「验签通过」当「有权访问」是范畴错误（与 §9.1 SLSA「证明了什么/不证明什么」同构）。② **`resource` 参数在授权请求与令牌请求两处都要带**，且值取 MCP server 规范 URI（canonical URI）；只在其中一处带 = 受众绑定链断。③ **调用上游 API 必须用上游授权服务器另发的令牌**，禁止把客户端令牌透传；`MUST NOT accept or transit any other tokens` 是**双向**约束（既不能收也不能转）。④ 与 §Cap63「唯一签发者、出站不转发客户端令牌」的分工：那条是架构原则，本节给出**协议级可机检条文**（audience claim、resource 双位置、401、禁止 query）；二者同向、按「合」登记不并存新层。

### 12.2（r749C-2）混淆代理是「同意被复用」不是「密码泄露」；四条件同时成立才可被利用
- **原文**：MCP 官方《Security Best Practices》（2025-11-25 版）逐字「This attack allows malicious clients to **obtain authorization codes without proper user consent by exploiting the combination of static client IDs, dynamic client registration, and consent cookies**」；四个 Vulnerable Conditions 逐字「MCP proxy server uses a **static client ID** with a third-party authorization server / MCP proxy server allows MCP clients to **dynamically register** (each getting their own client_id) / The third-party authorization server sets a **consent cookie** after the first authorization / MCP proxy server **does not implement proper per-client consent** before forwarding to third-party authorization」；攻击链 8 步关键三步逐字「their browser **still has the consent cookie from the previous legitimate request**」「The third-party authorization server **detects the cookie and skips the consent screen**」「The MCP authorization code is **redirected to the attacker's server** (specified in the malicious `redirect_uri` ...)」「The attacker **exchanges the stolen authorization code for access tokens** ... **without the user's explicit approval**」；《Authorization》官方逐字「MCP proxy servers using static client IDs **MUST obtain user consent for each dynamically registered client before forwarding** to third-party authorization servers」。CleanIssue（2026-10-29 更新）逐字「if consent is not requested for each client, **an attacker can obtain an authorization code without the victim's knowledge**」「In an audit, I also check that the rights the server uses are **the user's own rather than those of an all-powerful service account**」。
- **判据**：① 验收**按四条件 AND 判定**，不是查「有没有同意屏」：静态 client ID + 允许动态注册 + 第三方设 consent cookie + 转发前无 per-client consent，四项齐才构成可利用链；缺一项即降级登记，但仍须说明该项为何不成立。② 缓解落到**可机检清单**：维护「每用户 × 每 client_id」的同意注册表并在**发起第三方授权流之前**查；同意页须显示请求方名称、具体 scopes、注册的 `redirect_uri`，并带 CSRF 防护与 `frame-ancestors` / `X-Frame-Options: DENY`；consent cookie 用 `__Host-` 前缀 + `Secure`/`HttpOnly`/`SameSite=Lax` + 签名或服务端会话 + **绑具体 client_id**（不是「该用户已同意」这种全局标记）；`redirect_uri` **精确字符串匹配**（禁通配/模式匹配），变更须重新注册。③ **与 §8.2「工具调用授权」分工**：那条管模型要不要调工具，本节管**代理服拿用户身份去第三方换令牌时同意是否真的发生过**；与 §Cap42「管理权不含使用权」不同维。

### 12.3（r749C-3）`state` 的写入时序本身就是安全边界；scope 最小化与元数据发现面是旁栏不是补丁
- **原文**：官方《Security Best Practices》逐字「MCP proxy servers implementing OAuth flows **MUST**: Generate a **cryptographically secure random `state` value for each authorization request** / **Store the `state` value server-side ... only after consent has been explicitly approved** / **Set the `state` tracking cookie/session immediately before redirecting to the third-party identity provider (not before consent approval)** / **Validate at the callback endpoint that the `state` query parameter exactly matches** / **Reject any callback requests where the `state` parameter is missing or does not match** / Ensure `state` values are **single-use (delete after validation) and have a short expiration time (e.g., 10 minutes)**」；最强时序约束逐字「**The consent cookie or session containing the `state` value MUST NOT be set until after the user has approved the consent screen at the MCP server's authorization endpoint. Setting this cookie before consent approval renders the consent screen ineffective**, as an attacker could bypass it by crafting a malicious authorization request」；授权规范逐字「Authorization servers **MUST validate exact redirect URIs against pre-registered values**」「MCP clients **SHOULD** use and verify **state parameters** ... **discard any results that do not include or have a mismatch with the original state**」「Authorization servers **SHOULD issue short-lived access tokens** ... For public clients, authorization servers **MUST rotate refresh tokens**」；CleanIssue 逐字「For scopes, the rule is to **request the minimum at the start, then raise privileges step by step** when a specific operation requires it, instead of granting wildcard 'full access' up front」「The MCP authorization specification builds on **OAuth 2.1 and resource indicators to bind a token to its intended audience**」；SSRF 段官方逐字「During OAuth metadata discovery, MCP clients fetch URLs from several sources that could be controlled by a malicious MCP server」「`http://169.254.169.254/` (AWS/GCP/Azure metadata service)」「**DNS rebinding**: Domains that change DNS resolution between validation and use」「MCP clients **SHOULD** block requests to **private and reserved IP address ranges** as recommended by RFC 9728 Section 7.7」。
- **判据**：① **「有 state 参数」不等于防住 CSRF**：必须验 **state 在同意批准之前从未被写入**；验收动作是查写入时序（同意前 → 重定向前 → 回调比对 → 用后即删），不是查字段存在。② 四项配套缺一不可：每次密码学随机 / 服务端存且仅同意后存 / 回调精确比对且缺失即拒 / 单次使用 + 短过期（10 分钟量级，绑官方示例不写成固定标准）。③ **scope 最小化是独立门禁**：起步最小、按需升权、禁通配 full access；短时访问令牌与公共客户端 refresh token 轮换按官方 SHOULD/MUST 分栏登记。④ **元数据发现是出网面**：`resource_metadata` / `authorization_servers` / `token_endpoint` 等 URL 由服务器提供，须挡私网、`169.254.169.254`、localhost 服务、DNS rebinding 与重定向链（与 §Cap87「新能力不得绕过宿主既有 SSRF 策略」同向）。⑤ **本节的「不覆盖」清单**：不防工具描述投毒/影子（内容注入面，已由豆包自留地与 `wb-artifact-verification` 覆盖）、不证构建完整性（§九）、不检出已提交密钥（§十）、不保证交付新鲜度（§十一）；与 §Cap76「误读澄清同表同级」一致，安全声明同级写「不防什么」。

**来源（r749C 独立实拉 2026-11-15，≥2 独立域交叉）**：
- `https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization`（MCP 官方《Authorization》2025-06-18 归档版；WebFetch 200 **全文逐字**：OAuth 2.1 资源服务器角色、RFC 8707 resource 三 MUST、每次 HTTP 请求带 Authorization、禁止 query、audience 校验与 401、MUST NOT accept or transit any other tokens、上游另发令牌、MUST NOT pass through、confused deputy MUST per-client consent、exact redirect URI、state 验证、短时令牌与 refresh rotation。**第一独立域·协议官方一手**；页面自标「You are viewing an older version (2025-06-18) ... latest 2026-07-28」，**如实登记按归档版引用**）
- `https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices`（实取重定向至 `https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices`；MCP 官方《Security Best Practices》**2025-11-25 版**；WebFetch 200，**AI 摘要 60s 超时 → 返回前 15,000 / 35,943 字原文逐字，如实登记**：confused deputy 四条件与 8 步攻击链、per-client consent registry 与同意 UI 要求、`__Host-`/Secure/HttpOnly/SameSite=Lax、精确字符串匹配 redirect_uri、state 六条 MUST 与「MUST NOT be set until after consent approval」、token passthrough 四类风险（安全控制绕过/问责与审计链/信任边界/未来兼容）与「MUST NOT accept any tokens that were not explicitly issued for the MCP server」、SSRF 元数据发现面与私网阻断。**第二独立域·协议官方一手（不同文档）**）
- `https://cleanissue.io/en/mcp-security`（Florian Bonamy，**Updated 2026-10-29**；WebFetch 200 **全文逐字**：最窄 scope 与按需升权、token passthrough 破坏可追溯性、confused deputy 静态 client ID 与逐客户端同意、OAuth 2.1 + resource indicators 绑定受众、四边界威胁模型、OWASP MCP 测试指南 79 测试/19 族、服务端每参数敌意、审计 12 项清单。**第三独立域·独立实务一手**）
- `https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks`（**2025-04-01**，WebFetch 200 全文逐字：TPA/`add`+sidenote PoC、rug pull 定义、多服务器 shadowing、`Shadowing Is Enough`、三条缓解）——**换道前取证保留，仅用于界定「内容注入面 ≠ 授权面」边界，不作本轮结论来源**；`https://modelcontextprotocol.io/specification/2025-06-18/server/tools`（官方 tools 规范，WebFetch 200：`tools/list`、`listChanged`、`clients MUST consider tool annotations to be untrusted`、`SHOULD always be a human in the loop`）——同属内容/清单面，本轮不取。
- 交叉快照（**二手，逐条登记、不作唯一结论来源**）：`https://www.neuraltrust.ai/blog/mcp-tool-poisoning` · `https://www.scalekit.com/blog/mcp-tool-poisoning` · `https://pwnedlabs.io/blog/mcp-ai-agent-security` · `https://agentbeam.com/blog/mcp-security-practical-guide` · `https://glossary.cloud/terms/agentic-ai-security` · `https://aisec.blog.csdn.net/article/details/169736129`（含 MCPoison CVE-2025-54136、2026-11-02 跨框架 9,720 测试 22.9%、ShareLock、MCPTox 等**均未采纳为本轮结论数值**，仅作术语与事件存在性交叉）。
- **判非 / 换道**：`tool poisoning` / `rug pull` / `tool shadowing` / `tools/list` / `MCPoison` / `listChanged` 全库 `SKILL.md` 命中集中在**豆包自留地** `engineering/wb-execute-discipline`（r589C 描述即注入面/影子工具/生命周期绕过、r650A 连接即加载）与 `defaults/wb-context-compressor`（OWASP MCP 三查清单、description/schema pin），以及 `engineering/wb-artifact-verification`（MCP 规范 annotations 实证）、`defaults/wb-ponytail`（listChanged 清单会变）⇒ **换道**，WB 对上述两自留地 **0 落地**。新轴窄串 `per-client consent` / `consent cookie` / `__Host-` / `frame-ancestors` / `exact string matching` / `MUST NOT be set until after` / `resource parameter` 全库 **0 命中**；`token passthrough` / `confused deputy` / `RFC 8707` 命中于 `system/mcp-builder` §2026-09-24（OAuth 2.1 验三件事，豆包 r159-B 实拉）与 `defaults/wb-context-compressor` 的 OWASP 清单式一句，**均为上位配置口径/异命题**，本轮取协议条文级「同意流时序 + 攻击链 + 令牌不得透传的审计后果」互补细化，按「合」登记不新建并行层。模块 `SI/MEMORY.md` §9/§10/§11（SLSA / push protection / TUF）亦为异命题、不复用。
- **未采纳**：OAuth 代理完整实现、DCR 协议细节、CSP 全量策略、SSRF 具体 IP 段清单（只取「元数据发现 URL 是服务器可控出网面」判据）、上述二手来源的所有攻击成功率数值。


## 十三、CI 触发器是权限面：pwn request、TOCTOU 与缓存投毒的跨工作流横向移动（r753C 独立实拉 2026-11-15，≥2 独立域一手交叉，3 独点）

> 定位：本节管「**谁能触发一段带密钥的代码、以及这段代码的产物会不会流到更高权限的工作流**」。与 §九（SLSA 构建溯源）、§十（push protection 密钥检出）、§十一（TUF 交付新鲜度）、§十二（MCP 授权同意流与令牌受众）分工：那四条管产物、密钥、交付与令牌；本节管 CI/CD 触发器本身的信任边界与跨工作流污染。与 Cap87「新能力不得绕过宿主既有策略」同向但不同层：那条讲并行通道要继承策略，本节讲**同一平台内高低信任工作流共享缓存/工件形成的提权路径**。

### 13.1（r753C-1）触发器决定拿到什么；危险动作不是 checkout 而是「下一步执行了检出的代码」
- **原文**：GitHub Docs《Securely using `pull_request_target`》逐字「Workflows triggered by `pull_request_target` **run with elevated trust: the job receives the base repository's `GITHUB_TOKEN` and access to repository and organization secrets**」「The `pull_request` event ... **runs the workflow file from the merge commit of the pull request** ... GitHub restricts these events to a **read-only `GITHUB_TOKEN`, withholds access to other secrets**, and applies **fork approval policies**」「`pull_request_target` makes one critical and subtle change: the workflow ... is taken from the **base repository's default branch** ... **No code from the fork is executed by default**」「**The checkout step alone does not execute untrusted code** ... The vulnerability is completed by the **next step that runs code checked out into the current working directory**. Here, `make test` executes a `Makefile` taken from the pull request head」「Execution is not limited to your own steps: **build and test commands such as `npm install` and `npm run build`, as well as configuration files and dependencies the code brings with it, can all run attacker-controlled code. Execution does not require an obvious build step**」「**You must ensure the checked-out code is only ever inspected as data and never executed**」；GitHub Security Lab Part 4（Alvaro Munoz，**2025-01-16**）逐字「It is able to **read repository and organization secrets** / It is allowed to **have write permissions** / It **circumvents the usual safeguards of pull request approvals** / It normally runs in the **context of the default branch**, which ... may allow malicious actors to **poison the Action's cache and move laterally to other, more privileged workflows even when removing all permissions to the vulnerable workflow**」。
- **判据**：① **门禁固定三问**：谁能触发（外部 fork 贡献者？）／该触发器给什么（读写 token、全部 secrets、绕过审批？）／检出物**是否被执行**（含 install 生命周期脚本、测试命令、配置文件、依赖）。只看「有没有 checkout fork ref」会漏掉 `git fetch` / `gh pr checkout` / 下载 fork 工件后执行三类等价动作（同 Cap95 按能力等价集枚举，不按命令名点杀）。② **「pwn request」是组合条件**：高信任触发器 + 检出不可信代码 + 后续执行，三者 AND 才成立；缺任一时按实际风险面登记，不把 `pull_request` 一律判危险（官方明写它默认只读无密钥、有 fork 审批）。③ **`workflow_run` 的工件一律当不可信数据**：官方逐字「A `workflow_run` workflow should **treat artifacts uploaded by other workflows as untrusted data**, since their contents can come from a fork」；解包覆盖 workspace 脚本、把工件里的 PR 号/分支/路径拼进 shell 都属执行面。④ 与 §十分工：push protection 挡的是密钥被写进仓库，本节挡的是**合法存在的密钥在运行时被不可信代码读走**；两者不可互相替代。

### 13.2（r753C-2）常见缓解各有失效面：permissions:{} 挡不住缓存投毒，可变引用挡不住 TOCTOU
- **原文**：Security Lab 逐字「**Cache Poisoning**. As a mitigation, developers may **strip out all read and write permissions** ... However, the seemingly innocuous `permissions: {}` configuration can **unexpectedly pave the way for cache poisoning attacks**」「**Even if a workflow doesn't have write access to the repository, it can still poison the cache**, leading to potential code execution or data manipulation in other workflows that utilize the compromised cache」「**Time Of Check Time Of Use (TOCTOU) Attacks** ... submit a seemingly harmless pull request, **patiently wait for approval, and then swiftly update the pull request with malicious code before the workflow execution** ... relying on a **mutable reference like a branch name**」「`head.ref`, pointing to the branch, is **susceptible to manipulation** ... `head.sha` ... provides a **reliable and immutable pointer to the reviewed and approved code**」「**Lurking Threats in Non-Default Branches**. Vulnerabilities often linger in non-default branches ... an attacker can target these vulnerable versions ... by submitting pull requests specifically to those branches」；同文对 `workflow_run` 的「**Non-Effective Mitigations: Repository Checks** ... the workflow always run in the context of the default branch」与 `issue_comment` 的三条无效缓解逐字「**Actor Checks** ... The actor triggering the workflow might not be the same one trying to exploit it」「**Date Checks** ... **An attacker can forge commit dates**」「**Repository Checks** ... redundant」；Label gates 正解逐字「use the **commit SHA rather than the HEAD reference to prevent TOCTOU**」。Docs 硬化段逐字「**Restrict secrets** ... least privileges」「**Ensure the underlying compute is isolated and ephemeral**」、逃逸路径逐字「Fetching the pull request code outside of `actions/checkout` (for example with `git fetch`, `gh pr checkout`, or by **downloading an artifact from a fork's `pull_request` run**) and then running it」「This protection **only covers fork pull request refs**. Checking out other untrusted code ... is **not covered**」。
- **判据**：① **`permissions: {}` 不等于无写面**：缓存作用域挂在默认分支 SHA，不在 `GITHUB_TOKEN` 权限里 ⇒ 低信任工作流写缓存、后续 `push`/`schedule` 恢复，即「even when removing all permissions」也能横向移动；验收必须查缓存作用域，不能只读 permissions 块。② **审批与执行之间的时间窗要按不可变引用封死**：用 commit SHA 不用 HEAD/branch，label gate 取 `pull_request` labeled 事件自带的 SHA，禁止「解析 PR 号→取最新 commit」这种二次查询（同 Cap51「批准绑定那一刻的二进制」）。③ **逐个撞失效面**：repo check 对 `workflow_run` 无效、actor check 与 date check 对 `issue_comment` 无效、非默认分支残留漏洞版本、self-hosted runner 复用与内网可达、显式 `allow-unsafe-pr-checkout` / `cache-mode` 写能力 opt-out——每一项都要在清单里写「失效条件」而非只写「已配置」。④ **正确形态是工作流拆分**：`pull_request`（无密钥只读）做不可信处理 → `workflow_run`（高信任）只消费**经验证的元数据**，且跨边界数据全部视为不可信（Security Lab 逐字「This is a **crucial security boundary**」）；与 §Cap97「一次只放开一项控制」同向。⑤ 与 `system/skills-security-check` 已有「计划期验证≠执行时有效（TOCTOU 面）」按「合」登记不重述：那条管文件改写的计划/执行两段式，本节管审批后 PR 被改写与 CI 触发链。

### 13.3（r753C-3）平台默认值本身是安全边界，且会随生效日期变化；门禁要区分「我配的」与「平台给的」
- **原文**：GitHub Changelog（**2026-06-26**）逐字「GitHub Actions now issues **read-only cache tokens** to the default branch for workflow events that can be triggered without write permissions」「Previously, the Actions service issued **read-write cache tokens for every workflow event**, including triggers like `pull_request_target`, `issue_comment`, and fork-pull-request `workflow_run` cascades」「a trusted workflow such as `push` or `schedule` would later **restore those poisoned entries**. This opened up a path to **run arbitrary code and exfiltrate production secrets**」「a read-only cache token **when both of these are true**: The triggering event is **untrusted** ... **and** The workflow execution context and cache scope come from the **shared default-branch SHA**」「The most common workflow triggers that ... keep full read-write caching ... are `push`, `schedule`, `workflow_dispatch`, `repository_dispatch`, `delete`, `registry_package`, and `page_build`. Additionally, any trigger that uses a **non-default-branch scope, such as `pull_request` and `release`, keeps read-write caching**」「`actions/cache` **logs a warning in the run and the job continues without saving. Restores are unaffected**」「To keep the benefit of caching ... you will need to have a **separate workflow triggered by an event with read-write cache access such as `push`**」；Docs 默认策略段逐字「For public repositories ... GitHub adds a default policy that **blocks workflows triggered by `pull_request_target`**」「**Does not apply to private or internal repositories**」「Currently runs in **evaluate** mode. In this mode, **workflow runs continue**」「On **December 2, 2026**, GitHub will **enforce** the default policy」、显式 opt-out 逐字「Setting `allow-unsafe-pr-checkout: true` ... **The input is intentionally named to be easy to spot in code review and static analysis**」。
- **判据**：① **默认值的方向要逐年核**：从「所有事件读写缓存」到「不可信 ∧ 默认分支作用域 ⇒ 只读」是平台侧收紧，两条件 AND 才生效；把历史默认值写进现行门禁会得到反向结论。② **失败模式是「静默降级 + 告警」**：save 被拒仅 warning、job 继续、restore 不受影响 ⇒ 「CI 全绿」不能证明缓存写入成功了；验收要读日志里的 warning 与另起的 `push` 填缓存工作流是否到位。③ **作用域粒度是分支 SHA 不是仓库**：`pull_request`/`release` 因非默认分支作用域保留读写，与「事件可信/不可信」不是同一维度；门禁按「触发事件 × 作用域」二维表逐格判，禁止一维概括。④ **evaluate 模式 ≠ 已阻断**：2026-12-02 才对受影响的公开仓强制，且私有/内部仓不适用、已有策略不被替换 ⇒ 声明里必须带生效日期、适用仓库类型与当前模式，禁止把「平台会拦」当成现在已生效（同 Cap81「开关为真 ≠ 行为已换」）。⑤ **安全声明同级写「不防什么」**：本节不防工具描述投毒/影子（内容注入面）、不证构建完整性（§九）、不检出已提交密钥（§十）、不保证交付新鲜度（§十一）、不替代 MCP 授权受众校验（§十二）；与 Cap76 一致。

**来源（r753C 独立实拉 2026-11-15，≥2 独立域一手交叉）**：
- `https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target`（GitHub 官方《Securely using pull_request_target》；WebFetch 200 **全文逐字**：两类触发器权限对比、merge commit vs 默认分支、pwn request 定义与四类脆弱形态、checkout 不执行而下一步执行、npm install/npm run build/配置文件/依赖均算执行、MUST 只当数据检查、硬化四项（最小权限 / 缓存只读 / runner 隔离且临时 / CodeQL）、**默认策略仅公开仓 + evaluate 模式 + 2026-12-02 强制**、`allow-unsafe-pr-checkout` 显式命名意图与仅覆盖 fork ref 的边界。**第一独立域·平台官方文档一手**；另有 `https://docs.github.com/pt/enterprise-server@3.20/actions/reference/security/securely-using-pull_request_target`（葡语 GHE 3.20 版，WebSearch 快照逐字，用于口径一致性交叉，**按版本归档登记**））
- `https://securitylab.github.com/resources/github-actions-new-patterns-and-mitigations/`（GitHub Security Lab《Keeping your GitHub Actions and workflows secure Part 4》，Alvaro Munoz，**2025-01-16**；WebFetch 200 **全文逐字**：pull_request_target 四条特权（读 secrets / 写权限 / 绕审批 / 默认分支上下文可投毒缓存横向移动）、不可信代码执行、TOCTOU 与 head.ref vs head.sha、非默认分支残留、cache poisoning 与 `permissions: {}` 失效、repo/actor check 加固、workflow splitting 与 crucial security boundary、workflow_run 的 repo check 无效、issue_comment 的 actor/date/repository checks 三条无效与 Label gates + commit SHA 正解、date 可伪造。**第二独立域·官方安全研究一手**）
- `https://github.blog/changelog/2026-06-26-read-only-actions-cache-for-untrusted-triggers`（GitHub 官方 Changelog《Read-only Actions cache for untrusted triggers》，**2026-06-26**；WebFetch 200，**AI 摘要 60s 超时 → 返回全部 8,885 字原文逐字，如实登记**：读改写缓存全事件发放的历史、pwn request/script injection 写默认分支缓存→push/schedule 恢复→任意代码与生产密钥外泄、两条件 AND、保留读写的 7 类触发 + 非默认分支作用域两类、save warning 且 job 继续、restore 不受影响、需另起 push 工作流填缓存、同时上线 github.com 与 Data Residency。**第三独立域·平台官方变更公告一手**）
- `https://github.blog/changelog/2026-11-02-pull_request_target-blocked-by-default-december-2`（官方 Changelog 快照，2026-11-02，与 Docs 的 12-02 强制日期交叉，**仅作存在性与日期一致性校验**）· `https://github.com/paulasilvatech/awesome-harness-primitives/blob/main/harness/claude-code/skills/github-actions-hardening/SKILL.md` + `https://github.com/makifbaysal/tasktrooper/blob/main/catalog/agents/security-agent/skills/ci-cd-and-iac-security/SKILL.md`（WebSearch 快照逐字：`${{ }}` 表达式注入面、env 中间变量正解、`$GITHUB_ENV`/`$GITHUB_OUTPUT` 可设 NODE_OPTIONS/LD_PRELOAD/BASH_ENV、第三方 action 须 40 字符 SHA pin、`persist-credentials: false`、artifact 解包覆盖 workspace 脚本、severity 四级表）。**第四~五独立域·官方公告/社区审查清单立场，逐条登记、不作唯一结论来源**；社区 severity 分级与具体 CVE/事件编号**未采纳为本轮结论事实**。
- **判非 / 换道**：`pull_request_target` / `pwn request` / `cache poisoning` / `head.sha` / `workflow splitting` / `read-only cache` / `allow-unsafe-pr-checkout` / `script injection` / `fork PR` / `GITHUB_ENV` 全库 `SKILL.md` **0 命中**；`TOCTOU` 1 命中属 `system/skills-security-check`（计划期验证 ≠ 执行时有效，异命题，按「合」登记不重述）；`OIDC` / `pinned` / `typosquat` / `dependency confusion` / `workflow_run` / `supply chain` 命中集中在**豆包自留地** `defaults/wb-context-compressor`（包声明式治理、typosquatting 检测、n8n 发布 OIDC、Dify 异步 workflow_run_id 异命题）与 `engineering/wb-execute-discipline`（安装前 vetting、pinned revision、模型供应链），以及 `system/skills-security-check`（技能供应链审查）⇒ **换道**：WB 对上述两自留地 **0 落地**，本轮取「CI 触发器权限面 + 跨工作流缓存污染 + 平台默认值时效」这一正交轴。模块 `SI/MEMORY.md` §9 SLSA / §10 push protection / §11 TUF / §12 MCP 授权均为异命题、不复用。
- **未采纳**：完整 workflow YAML 编写、CodeQL 规则集与查询实现、self-hosted runner 网络隔离拓扑、MMV 类厂商方法、社区清单里的 severity 表与具体攻击事件统计值、GHE 版本号差异细节（只作口径交叉）。
