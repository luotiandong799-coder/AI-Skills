# 学习轮 r230C：skillsmp p96桌面OCR省token与Dify DSL IaC与Webhook幂等键清单与RAG提示工程模板（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/96（#9501-9538，p96 前 4000 字符） | OK |
| 2 | Dify（DSL 导出导入 IaC/YAML 版本控制/tracing 重放/插件市场/model plugin 结构） | OK |
| 3 | n8n（向量库支持清单 Pinecone/Qdrant/Supabase/Weaviate/Milvus/Zep/MongoDB Atlas/PGVector/增量索引/agent 暴露 MCP） | OK |
| 4 | LangFlow（Flow DevOps Toolkit SDK 版本化部署/lfx serve/OpenAI Responses 兼容端点//build 仅供编辑器） | OK |
| 5 | Activepieces（piece=构建块+MCP server 双角色/TypeScript SDK/bundleDeps external） | OK |
| 6 | Make（Agent 六步构建流程/工具命名与描述/scenario 作工具需定义 inputs/outputs） | OK |
| 7 | Pipedream（webhook 幂等键最佳实践/五大常见错误/constant-time 比较/测试代表性失败） | OK |
| 8 | Anthropic（CLAUDE.md 加性叠加/subagent hooks 双配置/Hook vs Skill 确定性对比/dynamic workflows） | OK |
| 9 | GitHub 生态（Agent 技能化/MCP 工具化趋势/awesome-claude-skills 1000+/mcp-builder 125K 星） | OK |
| 10 | WaytoAGI（RAG 提示工程 18/15 prompts/grounded 模板/OpenClaw 技能格式） | OK |

## 独点（4 个）
### C1：skillsmp p96 精选：桌面 OCR 省 token / git-diff 驱动 UI 测试 / 单工具测试纪律（来源：skillsmp.com/skills/page/96 #9510/9513/9521，2026-09-27 实拉）
- **desktop：桌面操控走原生 OCR 触觉反馈，不截全屏传 AI——极致省 token**（工具层：桌面自动化优先 OCR 定位反馈而非全屏截图喂模型，与 wb-max-token-saver 同源）。
- **ui-test：AI 对抗式 UI 测试**：**分析 git diffs 只测变更内容（或探索全 app 找 bug）；测功能正确性、可访问性、响应式布局、UX 启发式；支持 localhost 与 Browserbase**（工作流层：diff 驱动=只测改了的部分，把回归成本钉在变更范围）。
- **windows-mcp-tool-tester：每次测试恰好一个工具**（工作流层：工具验证单测化，benchmark/validate 分开，不一次测一堆）。
- **提升层**：工具 / 工作流。

### C2：Dify DSL IaC + n8n 增量索引 + LangFlow Flow DevOps SDK（来源：CSDN+dev.to+docs.langflow.org+blog.apify.com，2026-09-27 实拉）
- **Dify DSL 基础设施即代码**：**v0.12 起整个应用（提示词/工作流/工具集成/参数配置）序列化为单文件——导出 YAML 进 Git 版本控制、diff 变更、tracing API 逐步重放历史执行**（工作流层：工作流当代码管——版本化+diff+重放三件套）。
- **n8n RAG 增量索引**：**只有变更的页面重新嵌入，删除页面从索引移除（Apify 管道实测）**（工作流层：增量同步代替全量重建，索引与源同寿命）。
- **LangFlow Flow DevOps Toolkit SDK**：**终端工作流做版本化/环境变量/测试/部署，替代手动导出导入 flow JSON；配套 /build 端点仅供前端编辑器用，跑 flow 用 Flow trigger 端点**（工作流层：flow 生命周期 DevOps 化+API 用途纪律）。
- **提升层**：工作流。

### C3：Webhook 幂等键清单 + Make Agent 六步 + Anthropic Hook vs Skill 确定性（来源：blog.codercops.com + hooklistener.com + help.make.com + code.claude.com，2026-09-27 实拉）
- **幂等键用 provider 的稳定顶层事件 ID**：**Stripe evt_\* / GitHub X-GitHub-Delivery GUID / Shopify X-Shopify-Webhook-Id；不要从 payload body 或时间戳自己造 key（重试可能在 header 与顺序上不同）；接收那一刻存 ID 拒绝二次处理；hash raw body 只在无 ID 时用**（工作流层：幂等键=provider 给的顶层 ID，不是自己拼的签名）。
- **Make Agent 六步构建流程**：**计划 agent 框架→构建承载 scenario→配置 agent 理解工作与做法→添加工具→添加知识→上线前测试**（工作流层：agent 构建=框架先行、工具知识后补、测试在部署前，顺序即质量）。
- **Anthropic Hook vs Skill 对比**：**Hook=shell/HTTP/MCP 调用/prompt/subagent，触发于生命周期事件（PostToolUse/SessionStart），确定性=事件必触发；Skill=Claude 读的指令，触发于你敲 / 或 Claude 匹配描述，Claude 解释执行结果可变**（可复用 Skill 层：要确定性拦截用 Hook，要弹性指导用 Skill——触发机制决定选型）。
- **提升层**：工作流 / 可复用 Skill。

### C4：RAG 提示工程模板 + 对抗查询测试 + 置信度分级（来源：learn.microsoft.com + asibiont.com + sureprompts.com，2026-09-27 实拉）
- **Microsoft grounded 模板五段式**：**用 conversation history 理解意图解决指代 → 只用下方 context 回答 → context 未覆盖就明说 → [Source N] 格式引用来源 → 用户问题放最后**（提示工程层：把 grounded 纪律写进模板结构，比口头要求可靠）。
- **对抗查询测试**：**造 5 条 naive RAG 会答错的 adversarial queries（模糊代词、错误前提），提前暴露检索盲区**（提示工程层：RAG 上线前用对抗集打靶，找的不是"答错"，是"检索不到"）。
- **RAG 置信度分级**：**回答加 confidence 评分（High/Medium/Low 客户影响）；chunk 超窗用"压缩保留关键事实"prompt 适配 context window**（提示工程层：置信度标注让低可靠回答转人工，压缩提示保住关键事实）。
- **提升层**：模型 / 提示工程。

## 判重说明
- C1 桌面 OCR 省 token（新，wb-max-token-saver 面增量）；ui-test diff 驱动（新）；单工具测试纪律（新）；落。
- C2 DSL IaC（新）；增量索引（新）；Flow DevOps SDK（新）；落。
- C3 幂等键 ID 清单（r229-B 幂等面增量——具体 provider ID 源）；Make Agent 六步（新）；Hook vs Skill 确定性对比（新，强相关）；落。
- C4 grounded 模板五段式（r229-A grounded 面互补增量——模板结构落地）；对抗查询测试（新）；RAG 置信度（r229-B 置信度分级路由面互补增量）；落。
- 未落：comsol 自改进调试日志（wb-debug-loop 面已覆盖）；campaign-plan/quality-complaint-8d/ISO27001/渗透测试（企业级/安全不投入）；avbuzz（色情内容不学）；OpenClaw 技能格式示例（r227 已覆盖）；Dify model plugin 结构（面窄）；Agent 技能化趋势新闻（无方法论增量）。
