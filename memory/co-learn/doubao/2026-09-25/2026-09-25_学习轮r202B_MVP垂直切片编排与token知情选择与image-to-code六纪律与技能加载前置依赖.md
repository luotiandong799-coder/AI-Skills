# 学习轮 r202-B：MVP垂直切片编排与token知情选择与image-to-code六纪律与技能加载前置依赖（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/agent/ | 死链 |
| 2 | docs.n8n.io/integrations/creating-nodes/build-node-functions/ | 死链 |
| 3 | docs.langflow.org/help/ | 死链 |
| 4 | make.com/en/help/scenarios/best-practices | fetch error |
| 5 | pipedream.com/docs/api/ | OK（103 字，REST+SSE 概览，无独点） |
| 6 | docs.anthropic.com/en/docs/claude-code/background-agents | 死链 |
| 7 | skills.sh/hot | OK（41830 字节导航壳，无新内容） |
| 8 | skillsmp.com/skills/page/13 | OK（#1201-1238） |
| 9 | deepseek-plugin.org/agent-skills | 死链 |
| 10 | theairankings.com | OK（模型/应用共识榜单） |

## 独点（4 个）
### H1：MVP 垂直切片编排：把 PRD 变成可运行起点（来源：skillsmp #1202 orch-build-mvp，ECC 264,820★）
- **五步切片编排**：ingest 设计/规格文档 → 计划**瘦垂直切片**（thin vertical slices）→ 搭建第一个端到端切片 → **TDD 实现** → 评审 → **gated commit**。
- 与"大爆炸式一次写完"相反：**每个切片可运行、可验证、可交付**，第一个切片贯通端到端（前端→后端→存储）后再加厚。
- 判据：**MVP 不是"最小功能集"而是"最小可运行纵切面"**——先纵切贯通再横向扩展；每切片过门（gated）才合入。
- **提升层**：工作流。

### H2：token 知情选择 + 成本四件套：回答前让用户选深度，且不覆盖已指定级别（来源：skillsmp #1220 token-budget-advisor + #1223 cost-aware-llm-pipeline，ECC）
- **token-budget-advisor**：回答前给用户**知情选择——消耗多少响应深度**（short/detailed/exhaustive）；触发"short version/detailed version/token budget/ahorrar tokens"等变体；**不触发：用户已在当前会话指定级别（保持该级别）**、单字答案、token 指认证/支付令牌。
- **cost-aware-llm-pipeline 四件套**：任务复杂度→模型路由 + 预算跟踪 + 重试逻辑 + **prompt 缓存**。
- 与 wb-max-token-saver 的增量：**"回答前询问深度是默认选项之一，不是每次都要问"**——用户已表态就保持，不反复问；token 指认证令牌时不触发（语义消歧）。
- 判据：**输出深度的知情选择 = 一次问清、之后保持**；成本优化的四件套缺一不可（路由/预算/重试/缓存）。
- **提升层**：工具 / 输出侧。

### H3：image-to-code 六纪律：先自产设计图、再实现匹配（来源：skillsmp #1227 image-to-code，Leonxlnx/taste-skill 89,090★）
- **先自己生成设计图**（视觉重要任务）：先产生设计图本身 → 深度分析 → 实现网站尽量匹配。
- **大尺寸可读分区图 > 小压缩板**；**为分区/细节视图生成全新独立图，而非裁剪旧图**；避免"懒生成"（少图凑数）；避免 card-in-card-in-card 的 UI 嵌套；hero 保持干净、宽敞、在小屏笔记本上可读可见。
- 判据：**"图片转代码"的正确顺序是图先行、分析居中、实现殿后**；裁剪旧图是懒路径，独立新图才保质量；嵌套卡片是 AI 默认审美陷阱。
- **提升层**：可复用 Skill / 工作流。

### H4：技能加载前置依赖：先加载依赖技能再干活（来源：skillsmp #1231 data-table-manager，n8n-io/n8n 203,692★ + #1232 zotero-connector）
- **data-table-manager**：**load before calling data-tables or parse-file**——"what data tables do I have?" 等自然请求先经 data-table-manager；**加载顺序 = 依赖图：data-table-manager → data-tables → parse-file；build-workflow 前先 load workflow-builder**。
- **zotero-connector**：TRIGGER 与 DO NOT TRIGGER **显式枚举**——触发：import papers/add arxiv papers/batch import/check duplicates/by arXiv ID/list collections；不触发：ZoFiles 插件代码/导出/一般 Zotero 问题。
- 判据：**技能之间的加载顺序写进描述（before X call Y）**，比"按需发现"更确定；触发/不触发清单显式化降低误触发率（呼应 wb-skill-authoring 激活两方向）。
- **提升层**：可复用 Skill / 工作流。

## 判重说明
- H1 → wb-execute-discipline 已有"按技能建 agent/质检回退"；"PRD→垂直切片→TDD→gated commit 的 MVP 编排五步"为独有增量。
- H2 → wb-max-token-saver 已有输出侧裁量；"回答前知情选择 + 已指定级别保持 + token 语义消歧 + 成本四件套（含 prompt 缓存）"为独有增量。
- H3 → 未见 image-to-code 纪律已落地（r196~r202 无）；六纪律全为新。
- H4 → 未见"加载顺序写进描述"已落地；与 wb-skill-authoring 激活判重互补（那条管触发质量，本条管依赖顺序）。
