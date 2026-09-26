# 学习轮 r227C：skillsmp p90续读精选与Dify多模态知识库与n8n fallback模型与DSH间接提示注入量化评估与JIT-Agent即时harness进化（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/90 续读（#8963-9000 完） | OK |
| 2 | LangFlow 检索（1.13 release/Agentics aMap aReduce aGenerate/Logs） | OK |
| 3 | Pipedream 检索（Connect/MCP/connected accounts） | OK |
| 4 | Anthropic 检索（Agent Skills Standard/SKILL.md=package.json/skill-architecture） | OK |
| 5 | Dify 检索（多模态知识库/Agentic RAG/TiDB Vector/PolarDB Agent Memory） | OK |
| 6 | n8n 检索（2.40 release notes/fallback model/3.0 breaking changes） | OK |
| 7 | Activepieces 检索（AI Agent Security 七威胁/开发六步） | OK |
| 8 | Make 检索（2026-09-25 release/plugin for ChatGPT） | OK |
| 9 | GitHub 生态（trending monthly/archify/laya） | OK |
| 10 | DeepSeek Harness 生态（间接提示注入 arXiv 评估/JIT-Agent/桌面版/dsh.do） | OK |

## 独点（4 个）
### C1：skillsmp p90 续读精选：LLM+公式混合评分 / Plan-Research-Synthesize / CLAUDE.md 审计（来源：skillsmp.com/skills/page/90，2026-09-27 实拉）
- **resume-screener（1xiaoyueryuer/boss-hr-agent-toolkit）**：**简历评分实现参考——LLM 评 4 主观维度（exp/skill/proj/major）+脚本查 school_tier 校准 edu +公式重算 total；5 维度 weighted 求和（edu 25%/exp 25%/skill 25%/proj 15%/major 10%），Tier 阈值 ≥70 推荐/60-69 待定/<60 不推荐**（混合评分面：LLM 主观分+确定性公式校准，可复算）。
- **company-research（browserbase/skills ★3,727）**：**Plan→Research→Synthesize 模式做客户公司深研，ICP 匹配评分，输出评分报告+CSV；深度模式 quick/deep/deeper 平衡规模与智能**（销售研究流程面：规划→研究→综合三阶段+深度分级）。
- **claude-md-improver（anthropics/claude-plugins-official ★36,597）**：**审计并改进仓库里所有 CLAUDE.md——扫描全部 CLAUDE.md→对照模板评估质量→输出质量报告→再定向更新**（CLAUDE.md 审计面：先出质量报告再动手改，与 r226-B Karpathy CLAUDE.md drop-in 互补）。
- **提升层**：工作流 / 可复用 Skill。

### C2：Dify 多模态知识库与 Agentic RAG 细节 / n8n fallback 模型与 3.0 / Langflow Agentics（来源：dify.ai 多模态检索 2026-01-07 + Agentic RAG 2026-01-06 + docs.n8n.io release notes 2026-09-15 + langflow docs，实拉）
- **Dify 多模态知识库**：**文本与图像统一到一个语义空间，实现多模态 RAG 和视觉推理**（多模态 RAG 面：统一语义空间）。
- **Agentic RAG 流程细节**：**agent 迭代分析意图→选择工具与来源→重写查询→评估证据→重试或回退；增加 grounding 与可靠性，但加延迟/成本/复杂度**（Agentic RAG 面：r226-B 动作路由的流程细节增量——意图分析/查询重写/证据评估/重试回退）。
- **n8n AI 节点 fallback model**：**主模型旁可配 fallback 模型（2.40）；agents pages 手动创建入口；3.0（2026-10）破坏性变更预告（Docker 部署/安全强化/弃用清理）**（模型容错面：主+备选模型）。
- **Langflow Agentics bundle**：**LLM 转换表格数据——aMap 逐行加/填列、aReduce 多行折叠成一行、aGenerate 生成合成行**（表格处理面：aMap/aReduce/aGenerate 三组件）。
- **提升层**：工作流 / 工具。

### C3：DSH 间接提示注入量化评估 / JIT-Agent 即时 harness 进化 / DSH 桌面版与质量信号（来源：arxiv 2608.16393 Tencent Zhuque Lab + arxiv 2608.25593 LV-NUS + deepseek.com/harness + dsh.do，实拉）
- **DSH 间接提示注入实证评估**：**14,560 次受控执行、16 个间接内容通道、35 个 payload 目标、12 种攻击方法；最强攻击成功率：17.0%（fake-completion 文本）/25.5%（隐藏 Unicode 文件）/16.0%（skills 通道文件）；双判据评估——确定性规则判据 J_R+语义 LLM 判据 J_L**（安全实证面：攻击成功率数字+双判据评估法，未信任内容与敏感动作之间要有控制）。
- **JIT-Agent 即时 harness 进化**：**harness 智能是可训练的——按需合成任务自适应 harness；四模块协议：记忆管理/规划策略/动作协议/工具技能编排；修复 harness+从历史配置归档蒸馏性能信号自进化**（harness 智能面：四模块协议+自进化，Agent 能力不只看模型）。
- **DSH 桌面版+dsh.do 市场**：**DeepSeek 桌面预览版（2026-09-24 V0.1.7-rc.2，Win x64+Apple Silicon）；dsh.do 插件市场 14,047 packages/11,876 bundles/7,651 clients；Star 不再作为默认质量信号**（生态面：桌面端落地+质量信号去 Star 化）。
- **提升层**：工具 / 工作流。

### C4：Agent 安全七威胁六防护 / Make 新模型事实面（来源：activepieces.com AI Agent Security 2026-04-23 + help.make.com 2026-09-25，实拉）
- **agent 七威胁+六防护清单**：**七威胁：间接提示注入/系统间数据暴露/工作流利用与自动化滥用/记忆投毒与上下文操纵/RCE/业务逻辑绕过；六防护：每个 agent 限制权限/验证输入输出/持续监控行为/需要时 HITL/定期审计测试/企业级权限与日志**（agent 安全面：与 r225 OWASP 安全互补——记忆投毒与业务逻辑绕过是增量，防护六项含持续监控+HITL）。
- **Make 2026-09 模型接入面**：**GPT-6 Astra 接入 Make（09-21）、Make plugin for ChatGPT 上线（09-23）、Claude Opus 5.5/Gemini Omni 1.1 Flash（09-25）**（工具面：模型接入节奏事实）。
- **提升层**：工作流 / 工具。

## 判重说明
- C1 resume-screener（LLM 主观分+脚本确定性校准+公式重算）全新面；company-research Plan→Research→Synthesize 三阶段+深度分级新；claude-md-improver（先出质量报告再定向更新）与 r226-B Karpathy CLAUDE.md 互补；落。
- C2 Dify 多模态知识库（文本+图像统一语义空间）新；Agentic RAG 流程细节为 r226-B 动作路由的增量（意图分析/查询重写/证据评估/重试回退，≥40% 增量合并）；n8n fallback model（主+备选）新；3.0 破坏性变更预告新；Langflow aMap/aReduce/aGenerate 新；落。
- C3 DSH 间接提示注入实证（攻击成功率+双判据 J_R/J_L）为 r225 OWASP 安全的实证增量；JIT-Agent 四模块协议+自进化全新面；桌面版/dsh.do 质量信号为生态增量；落。
- C4 Activepieces 七威胁六防护含记忆投毒/业务逻辑绕过/持续监控/HITL 增量（合并保留增量）；Make 模型接入节奏事实（r227-A 已落同批部分，本批 Astra/ChatGPT plugin 为补充）；落。
- 未落：Pipedream Connect（r225-C 已落）；Anthropic SKILL.md=package.json 类比（弱视角，无独立方法）；Anthropic 同名 skill 优先细节（r227-B 统一模型已覆盖）；archify 架构图技能（与既有图技能重叠）；Make 重复 release 面。
