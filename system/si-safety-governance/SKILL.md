---
name: si-safety-governance
description: 全局安全治理（Security Intelligence）。在所有对外/写/删/权限/部署/工具调用/结果输出动作前与后调用，覆盖数据读取、信息传递、工具调用、结果输出全链路（不只执行前）。扫描提示注入、数据外泄、权限边界、工具中毒、危险代码、供应链、过度代理、记忆中毒等风险，给出风险评分与"可否安装/执行"门禁。本技能是 SI 载体，对系统既有 skills-security-check 做能力补齐。
version: 1.3.0
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
