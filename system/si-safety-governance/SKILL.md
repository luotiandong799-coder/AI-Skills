---
name: si-safety-governance
description: 全局安全治理（Security Intelligence）。在所有对外/写/删/权限/部署/工具调用/结果输出动作前与后调用，覆盖数据读取、信息传递、工具调用、结果输出全链路（不只执行前）。扫描提示注入、数据外泄、权限边界、工具中毒、危险代码、供应链、过度代理、记忆中毒等风险，给出风险评分与"可否安装/执行"门禁。本技能是 SI 载体，对系统既有 skills-security-check 做能力补齐。
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
