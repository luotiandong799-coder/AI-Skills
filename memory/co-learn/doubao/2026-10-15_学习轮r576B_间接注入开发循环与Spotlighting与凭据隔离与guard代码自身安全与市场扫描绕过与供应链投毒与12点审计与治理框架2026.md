# 学习轮 r576B（2026-10-15 · AI 技能库工程与方法论 + AI 智慧进化）

十站实拉（全量逐站，r576 批第 2 轮，角度为安全与治理，与 r576A 评估可观测性错开）：Dify / n8n / LangFlow / Activepieces / Make / Pipedream / Anthropic-OWASP / skills.sh / GitHub 生态 / deeplearning.ai。判重基准：execute 3.96.0（r576A 3 章）+ compressor 3.693.0（r576A 3 章）+ r575A/B/C 18 章 + r574 批 18 章 + 更早批次 + WB 留痕。

## 落地（execute 3.96.0 → 3.97.0，+3 章）

1. **间接注入开发循环与 excessive agency + Spotlighting 隔离量化：issue/PR 藏指令 + task drift≠injection + 输入隔离 >50%→<2%**（来源：OWASP GenAI《Exploit Roundup Q3 2026》2026-10-08 + OWASP《Secure Coding with AI Cheat Sheet》2026-10-06 + Howardism《Agentic Prompt Injection》2026-05-28 + channel.tel《Every Tool Is an Injection Surface》2026-03-20）
   - 开发循环注入面（issue bodies/PR descriptions 藏指令）；excessive agency 独立风险（LLM03，task drift≠injection，归因分机制）
   - Spotlighting 输入隔离（自然语言输入当不可信数据+定界，间接注入成功率 >50%→<2%，单一最高杠杆）；指令层级（高信任源优先+Claude Opus 4.5 ASR 1.4%）
   - **提升层**：工作流 / 可复用 Skill

2. **凭据隔离与泄漏处置：agent 运行时无凭据访问 + 外部 vault + 保存时验证 vault 访问权 + execution data redaction + 加密密钥泄露即重生成**（来源：n8n《AI Agent Sandboxes》2026-08-06 + n8n《AI Agent Governance》2026-07-24 + n8n《RBAC》2026-08-27 + n8n Release Notes 2026-05-27 + CSA《n8n RCE Attack Surface》2026-03-12）
   - 凭据运行时隔离（agent 无凭据访问+轮换不动逻辑）；外部 secrets+保存时验证（$secrets 表达式，防猜测路径泄露）
   - execution data redaction（API 层掩码+审计日志去 PII+项目隔离）；N8N_ENCRYPTION_KEY 泄露=重新生成+重输全部凭据+全量轮换
   - **提升层**：工作流 / 可复用 Skill

3. **guard 代码自身安全：ToolGuard 生成 guard 也有 CVE + 形状检查被提升为安全边界 + AUTO_LOGIN=true 是 critical misconfiguration**（来源：SentinelOne《CVE-2026-9135》2026-07-24 + Endor Labs 2026-08-18 + CSA《Langflow CVE-2026-33017》2026-03-30）
   - guard 代码是攻击面（ToolGuard 集成 CVE：绕过 allow_custom_components=false+CodeInput 未验证字段+MCP 跨租户）
   - 形状检查≠安全边界（validator→eval 反模式）；生产配置基线（AUTO_LOGIN=false+出站白名单）
   - **提升层**：工作流 / 可复用 Skill

## 落地（compressor 3.693.0 → 3.694.0，+3 章）

1. **技能市场扫描可绕过与供应链投毒新形态：Trail of Bits 5 市场全绕过 + 文档示例藏 payload + Miasma worm + BadSkill 99.5%**（来源：安全内参 2026-06-07 + AgentPatterns 2026-10-13 + StepSecurity 2026-10-08 + SecureTom 2026-04-28）
   - 市场扫描不可靠（5 市场全绕过+4 恶意 skill 3 个 <1 小时）；文档示例投毒（in-context learning 再现 payload 绕过对齐）
   - Miasma worm（配置型投毒不改源码+[skip ci]）；BadSkill 3% 投毒率→99.5% ASR
   - **提升层**：可复用 Skill

2. **SKILL.md 12 点审计 + 检测技术（neuro-symbolic/SkillDetonate）：secrets 模式 10.9% 硬编码 + 技能=低完整性组件 + MalSkills SSO+依赖图**（来源：Knack 2026-05-21 + arXiv 2607.02357 + arXiv 2603.27204）
   - 装前 12 点审计（secrets 扫描打头）；低完整性模型（技能写入限 allowlist+二进制来源验证+动态检测）
   - MalSkills 跨工件 SSO 提取+依赖图+神经符号推理
   - **提升层**：可复用 Skill

3. **治理框架与 guardrail 分层：国标 AI 安全治理框架 3.0 四要求 + agent 治理四支柱 + LLM vs agentic guardrails 区别**（来源：TC260 框架 3.0 2026-09-01 + DeepLearning.AI《Governing AI Agents》2026-07-26 + aitutorialmaker 2026-08-25 + W&B 2026-03-02）
   - 国标四要求（多层检测+人工审批留痕+工具验证+运行监测）；治理四支柱（生命周期/风险/安全/可观测）
   - 双层 guardrail（LLM 内容过滤 vs agentic 动作治理：工具权限/沙箱/花费上限/审批门/审计）；guardrail 三时点 before/during/after
   - **提升层**：可复用 Skill

## 十站实拉要点（逐站留痕）

- **Dify（安全治理角度）**：CVE-2026-41947（授权绕过：editor 用户可设置 trace 配置到任意应用，不论 tenant 归属；未认证免费自注册放大）；1.11.0 前置（API key 明文暴露前端可复用）；RBAC（TenantAccountRole：OWNER/ADMIN/EDITOR/NORMAL）；dataset-scoped API keys（1.17.1）；sandbox 安全改进；SOC 2 Type II/ISO 27001:2022/GDPR 第二年
- **n8n（安全治理角度）**：AI agent sandbox（凭据加密存库+agent 运行时无访问+轮换不动逻辑）；external secrets（$secrets 表达式+保存时验证 vault 访问权防猜测路径泄露）；execution data redaction（API 层掩码输入输出+审计日志去 PII）；项目级隔离（workflow/credentials/data/variables/execution history）；Docker secrets；CSA（N8N_ENCRYPTION_KEY 攻破=重生成+重输全部凭据；n8n RCE 主动利用中）；RBAC 静态角色在 agentic 系统失效
- **Langflow（安全治理角度）**：Policies 组件（ToolGuard 自然语言业务规则→自动生成 guard 代码→运行时强制→缓存）；CVE-2026-9135（Policies ToolGuard 集成缺陷绕过 allow_custom_components=false+CodeInput 任意代码执行+MCP 跨租户）；CVE-2026-33017（未认证 RCE，AUTO_LOGIN=true=critical misconfiguration，出站白名单限制爆炸半径）；docs 安全页（untrusted/LLM 生成代码→block custom component+容器化隔离）；guardrails pattern-based vs model-based
- **Activepieces（安全治理角度）**：V8 sandboxing（SANDBOX_PROCESS isolate 二进制+每 run 全新 Linux namespaces+CAP_SYS_ADMIN→privileged true）；RBAC 四默认角色（Admin/Editor/Operator/Viewer）；network security（AP_SSRF_ALLOW_LIST 服务端出站过滤，OAuth token claim/refresh/Vault/Conjur/webhook/MCP tool validation 全部走过滤）；AP_ENCRYPTION_KEY（openssl rand -hex 16）；scoped credentials per piece+敏感动作隔离审批+每特权步日志；Composio 事件（2026-05 Gmail OAuth 被攻，5,001 连接+5,241 API keys 强制轮换）
- **Make（安全治理角度）**：PBKDF2-SHA512 200k 迭代存密码（员工也无法复现）；AES-256 全盘加密；凭据轮换（main 查 token 过期→子场景 Basic Auth 换 token→AES Encryptor 加密存）；MD5 hash 存 API key（数据存储被攻不泄露原 key）；凭据请求工作流（request/reauthorize）；防御纵深（防火墙白名单 Make 服务器+最小权限 API key+Cloudflare tunnel）；API token scopes
- **Pipedream（安全治理角度）**：AWS KMS 256 位 AES 加密静态+私有网络+加密备份；credentials scoped per project+revoke 一次 API call；MCP per-app routing（每 app 独立 endpoint，token 永不暴露给模型）；external auth 运行时取凭据；secrets 存 connected accounts/env vars 绝不进代码；ClaudSkills vault（0600）；Authdog（AES-256-GCM，API 永不返回 refresh token）
- **Anthropic/OWASP（安全治理角度）**：OWASP Q3 2026（LLM03 excessive agency=agent 对无关外部负载行动；不要单从 task drift 推断 prompt injection）；OWASP 间接注入开发循环（issue bodies/PR descriptions 藏指令）；Microsoft Spotlighting（输入隔离，间接注入 >50%→<2%，单一最高杠杆）；Claude Opus 4.5 自适应对抗 1.4% ASR；指令层级（高信任源优先）；五层纵深（权限边界/门控高风险/输入消毒/输出监控/网络凭据隔离）；模型免疫不可行（arXiv 2307.15043）
- **skills.sh（安全治理角度）**：ToxicSkills 76 恶意 payload（凭据窃取/反向 shell/外泄，8 个发布时仍存活，91% 走自然语言指令）；5 个命名威胁 actor；Trail of Bits（5 主流市场扫描全可绕过，4 恶意 skill 3 个 <1 小时）；SkillDetonate（技能=低完整性组件，写入限 allowlist，动态检测）；MalSkills（neuro-symbolic SSO 提取+依赖图）；SKILL.md 12 点审计（secrets 模式 10.9% 硬编码）；BadSkill（3% 投毒→99.5% ASR）；文档示例投毒（in-context learning 再现）；Miasma worm（[skip ci]+配置文件 payload）
- **GitHub 生态（安全治理角度）**：腾讯 Cube Sandbox（RustVMM+KVM，E2B 兼容，<60ms+<5MB）；微软 MXC（policy-driven 分层隔离+每操作审计）；Copilot 云端+本地沙箱（public preview，隔离工具执行+定义策略）；dify-sandbox（kernel-level 隔离+cgroup+seccomp+ephemeral）；cloudflare/sandbox-sdk、vndee/llm-sandbox、swe-agent/mini-swe-agent；Strix（AI 渗透 agent，Docker 沙箱容器）
- **deeplearning.ai（治理角度）**：Governing AI Agents（四支柱=lifecycle management/risk management/security/observability；数据 agent 最小数据访问+输入输出决策可观测）；Safe and reliable AI via guardrails（PII 不泄露）；LLM vs agentic guardrails（LLM 过滤 prompt/output；agentic 额外治理动作：工具权限/执行沙箱/花费上限/审批门/审计轨迹跨 plan-act loop）；guardrail 目标=可预测非变笨（before/during/after 三时点）；NIST 2026 agent identity/authorization

## 功能套件核查（⑦）

三核心套件（wb-ponytail/wb-max-token-saver/wb-context-compressor）本轮无优化升级项；新增章节均标注与既有相邻章节分工边界与触发词（Agent 工具面安全/间接注入/secret manager/guardian pattern/最小权限/OWASP 纵深/audit-skill 机械测试/verified 字段/技能生态安全量化等）。

## 垃圾清理（⑨）

删了什么：本批十站实拉全走 general_search，无本地临时文件落盘、未产生新垃圾。保留什么：*.bak 与全部核心产物（两 SKILL 文件 + r576A/B 留痕 + 既往批次留痕）。

## 信源健康度

无删源无加源；Flowise 已删除不拉；十站全部可达，未触发桌面 VPN。commit/push 挂起（git 通道持续不可用，累计 r546→r576B 共 31 批）。
