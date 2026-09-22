# r135-C 全站实拉 · 记忆ADD-only+技能供应链签名落地 ctx

> 日期：2026-09-22｜批次：r135-C（手动触发）｜模式：AI技能库学习批

## 一、逐站实拉（10 次，全量信源覆盖）
| # | 信源 | 实拉内容 | 提炼 |
|---|---|---|---|
| 1 | Anthropic（Effective Context Engineering / claude.com blog） | 多窗口任务分工（第一窗口搭框架写测试、后续迭代 todo）；scale effort to query complexity（简单=1 agent+3-10 工具调用、复杂=10+ 子代理）；role-based context layers；stable prefix→prefix caching | 上下文/编排事实（mts 推理成本匹配已覆盖） |
| 2 | GraphRAG 论文与教程（arXiv/kinda） | query decomposition 拆 2-4 子查询独立检索再综合；GraphSearch/StepChain 递进子查询 | 平台模式事实 |
| 3 | Mem0/Letta（blog/vectorize/qiita） | **ADD-only 单遍提取（新事实只加不覆盖）；Memory Decay 0.3×~1.5× recency 软衰减重排不硬删；四层记忆（conversation/session/user/organizational）**；Letta 核心/存档/回忆三层（RAM/disk 隐喻） | **C1：记忆写入只增不覆盖+过期软衰减排序** |
| 4 | OWASP Agentic Skills Top 10（白皮书 2026-08 / registry） | **ed25519 签名强制、未签名拒绝安装；签名绑可撤销发布者身份（key id+domain/did:web+验证密钥）；签名证作者不证安全；Snyk/Tessl 注册级扫描；Registry vetting 扫注入模式** | **C2：技能供应链签名验证+安装扫描** |
| 5 | Langfuse/LangSmith（changelog v4/tuned evaluators） | Pulse 异常尖峰发现；one binary judge per failure mode + 用自己的标签验证 judge；Tuned Evaluators（托管 judge） | 评测工具事实（WB dl 已覆盖 judge 校准） |
| 6 | RouteLLM（PyPI/arXiv HYDRA） | 路由省 85% 成本保 95% GPT-4 质量；MetaRouter 偏好感知路由 | 工具层事实 |
| 7 | Anthropic Skills（docs best-practices/enterprise） | SKILL.md <500 行；互斥上下文分文件减 token；enterprise registry 字段（purpose/owner/version/dependencies/eval status） | sa 已覆盖（渐进披露/版本化） |
| 8 | Context compression（LLMLingua/AGORA/Acon） | LongLLMLingua contrastive perplexity（query 在场/缺席两次打分，加入 query 后更可预测的 token 保留）；Acon 压缩指南迭代优化 | token 级压缩（个人 Agent 不手工 token 级压） |
| 9 | Claude Code subagents（claude.com blog/explainx） | **独立评审子代理（不知晓实现旅程，外部视角抓熟悉度掩盖的问题）**；worktrees 防并行冲突；match scale to task | 编排事实（ED 五连查/质检回退已覆盖主点） |
| 10 | skills 生态（getclaudeskills/articsledge） | 2026 注册表生态数万技能；向"审计+签名注册表"演进（类比软件包注册表） | 生态趋势事实 |

## 二、判重与落地
- **C1 记忆 ADD-only+软衰减（落 · ctx）**：ctx §记忆提取四策略管"提取什么"、§两级沉淀管"组织"，**无"写入冲突策略（覆盖 vs 追加）"与"过期策略（硬删 vs 软重排）"** → 落（工作流/记忆治理）。
- **C2 技能供应链签名（落 · ctx）**：ctx §工具面安全已管"装好后运行时"（审 description/同名拦截/per-tool 权限），**供应链"装之前分发链"（签名+可撤销身份+注册级扫描）是上一环** → 落（可复用 Skill/供应链）。
- Anthropic scale-to-complexity / independent review subagent / Langfuse judge 校准 / RouteLLM / LLMLingua：与已有（mts 成本匹配 / ED 质检回退 / WB dl judge / av）重叠或工具层 → 不落。
- GraphRAG / skills 生态趋势：平台模式/生态罗列 → 不落。

## 三、功能套件检查
- 套件：wb-ponytail / wb-max-token-saver / wb-context-compressor
- 本轮：ctx 新增"记忆写入与过期策略"+"技能供应链签名"两节，与 pt（精简输出）、mts（成本四层）无冲突 → 三件套无需增删。
