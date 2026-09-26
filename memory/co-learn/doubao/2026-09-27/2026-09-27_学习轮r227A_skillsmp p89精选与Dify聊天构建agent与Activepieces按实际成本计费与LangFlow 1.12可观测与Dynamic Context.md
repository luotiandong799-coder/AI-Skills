# 学习轮 r227A：skillsmp p89精选与Dify聊天构建agent与Activepieces按实际成本计费与LangFlow 1.12可观测与Dynamic Context（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/89（#8801-8860 实拉） | OK |
| 2 | Dify 检索（Blog：New Agent 聊天构建/v1.17.1 受限 API key/Sonilo 配乐） | OK |
| 3 | n8n 检索（MCP server 生成 workflow/n8nClaw 自托管助手/Assistant update） | OK |
| 4 | LangFlow 检索（1.12 OpenTelemetry/guardrails 组合检查/custom components） | OK |
| 5 | Activepieces 检索（Breaking Changes：AI 按实际成本计费/Agents 实体化） | OK |
| 6 | Make 检索（2026 release：新模型支持/MCP webhook 队列/ChatGPT 官方插件） | OK |
| 7 | Pipedream 检索（Connect/Component API/dedupe strategies） | OK |
| 8 | Anthropic 检索（Skill authoring best practices/14 模式/三分类决策） | OK |
| 9 | GitHub 生态（OpenAgentSkill official/MagicNetWorld 技能库 Dynamic Context/dsh.so 四问） | OK |
| 10 | agentskills.io/deepseek-plugin（AgenticSkills/sshlg-skills 审计/DSH 注册表） | OK |

## 独点（4 个）
### A1：skillsmp p89 精选：10 阶段推理循环 / 确定性 lint+并行 agent 审查 / MinerU PDF 解析 / 缩略图生成评估闭环（来源：skillsmp.com/skills/page/89，2026-09-27 实拉）
- **think（AgriciDaniel/claude-obsidian ★15,126）**：**Fable 派生的 10 阶段推理循环——OBSERVE/OBSERVE/LISTEN/THINK/CONNECT/CONNECT/FEEL/ACCEPT/CREATE/GROW，用于后果重大或模糊的推理与决策（deep think/架构评审/事后复盘/权衡分析/挑战假设）**（结构化推理面：10 阶段慢思考循环）。
- **qt-cpp-review（mavlink/qgroundcontrol ★4,957）**：**先跑确定性 lint（60+ 规则），再 6 个并行深度分析 agent 覆盖模型契约/所有权/线程/API 正确性/错误处理/性能；只报 >80/100 高置信问题并给结构化缓解方案；只读绝不改码**（代码审查面：确定性 lint+并行 agent+高置信门槛+只读）。
- **mineru-pdf-parser（staruhub/ClaudeSkills ★719，中文）**：**用 MinerU 把复杂 PDF 转成 LLM 友好的 Markdown/JSON——提取文本/表格/公式/图像，为 RAG 应用准备文档数据**（PDF 解析面：复杂版式→Markdown/JSON）。
- **thumbnail-creator（mohitagw15856/pm-claude-skills ★1,320）**：**缩略图候选生成闭环——Claude 读文章→提构图概念→写带品牌规范的图像生成 prompt→调用 Gemini 生成→计算机视觉评估结果→返回排序候选+理由**（图像生成评估闭环面：生成后必评估排序）。
- **提升层**：工作流 / 可复用 Skill。

### A2：Dify 聊天构建 agent / v1.17.1 受限 API key / Activepieces AI 按实际成本计费 / n8n MCP 生成 workflow（来源：dify.ai/blog 2026-08-27 + ai-gallery.jp Dify 更新 + activepieces.com breaking-changes 2026-09-22 + blog.n8n.io 2026-04-29 + n8n.io/workflows，实拉）
- **Dify New Agent（2026-08-27 发布）**：**通过聊天构建 agent——Dify 自动生成可复用 skills 并在对话中保留上下文；准备好后加进 workflow 做更大流程**（聊天构建 agent 增量：对话中自动沉淀可复用 skills，与 r225-C 句子级构建互补）。
- **Dify v1.17.1（2026-09-10）**：**特定数据集限定 API 密钥+workflow 密钥**（受限密钥面：API key 可限定到单个数据集）。
- **Activepieces AI 计费改革（Breaking Changes）**：**AI steps 从"每模型每步固定积分"改为"按 provider 报告的实际美元成本计费"，换算 AP_AI_CREDIT_USD_VALUE（默认 0.0005 即 1 credit=1/20 美分）；用自己的 API key 每次调用 flat 1 credit；文件传 AI step 上限 AP_MAX_FILE_SIZE_MB**（计费面：固定价改实际成本）。
- **n8n MCP 生成 workflow（blog 2026-04-29 + workflow 模板）**：**向 Claude/ChatGPT/IDE 描述需求→n8n MCP server 直接构建、验证、部署好 workflow，无需拖节点；n8nClaw 是完全用 n8n 搭的自托管多通道 AI 助手模板**（MCP 构建 workflow 面，与 r225-A MCP discovery 互补）。
- **提升层**：工作流 / 工具。

### A3：LangFlow 1.12 OpenTelemetry 与 guardrails / Anthropic skill 三分类决策 / Make 新模型与 webhook 队列（来源：langflow.org/blog 1.12 2026-09-01 + newreleases.io v1.12.2 + agentskillexchange 2026-04-12 + help.make.com 2026 系列，实拉）
- **Langflow 1.12（2026-09-01）**：**OpenTelemetry 支持——服务健康与 flow runs 的可观测性**（平台可观测面：OTel 标准接入）。
- **Langflow 1.12.2 guardrails 升级**：**guardrails 支持可选组合 rule 和 model checks**（guardrails 组合检查面：规则+模型双通道）。
- **Anthropic skill 内容三分类决策**：**skill 最大收益不来自写更多指令，而来自决定什么留在 prompt 上下文、什么变成可执行代码、什么只按需加载——prompt caching 砍重复上下文成本，tool use 把脆弱指令变可靠执行，lazy load 只按需读**（skill 形态决策面：r226-B 简洁三问的深化——不只简洁，还要选形态）。
- **Make 2026 新模型面**：**Claude Opus 5.5/Gemini Omni 1.1 Flash/gpt 6 sol/luna/astra/grok 4.7 支持；MCP tools for webhook queues（webhook 队列管理）；官方 Make plugin for ChatGPT（2026-09-09）**（工具面：模型接入+webhook 队列 MCP）。
- **提升层**：工具 / 工作流。

### A4：Dynamic Context 动态上下文注入 / dsh.so 插件四问信任分层 / OpenAgentSkill 官方来源（来源：magicnetworld.com 2026-09-26 + dsh.so 2026-09-22 + openagentskill.com 2026-09-26，实拉）
- **Dynamic Context（Claude Code 2.1.x）**：**SKILL.md 中用 ! 反引号语法执行命令注入实时上下文——动态上下文注入语法**（上下文注入面：命令输出直接进 skill 上下文）。
- **dsh.so 插件四问信任分层**：**对每个 DSH 插件回答四问：是什么/安全吗/能装吗/还维护吗——安全扫描+sandbox 安装测试，L4=安装测试通过、L5=运行测试通过（15,883 artifacts 索引/15,616 安全扫描/15,009 安装测试/8,610 运行测试/8,685 活跃）**（插件信任分层面：r225-A DSH 全插件化互补，L4/L5 分级是增量）。
- **OpenAgentSkill official**：**官方 AI agent skills 来自技术厂商——13 个厂商 65 个 skills 3.2M stars（Microsoft 21 skills），先查来源/质量/信任/可安装性/维护再进工作流**（官方技能来源面）。
- **提升层**：工具 / 工作流。

## 判重说明
- A1 全为新面（10 阶段推理循环/确定性 lint+并行 agent/高置信门槛/MinerU 复杂 PDF 解析/Gemini+CV 评估闭环），落。
- A2 Dify 聊天构建 agent 含"自动沉淀可复用 skills"≥40% 增量（r225-C 句子级构建互补）；v1.17.1 受限密钥全新；Activepieces 按实际成本计费全新；n8n MCP 生成 workflow 与 r225-A MCP discovery 不同面；落。
- A3 LangFlow 1.12 OTel/guardrails 组合全新；Anthropic 三分类决策为 r226-B 简洁三问的深化增量；Make 新模型支持+webhook 队列工具；落。
- A4 Dynamic Context 注入语法全新；dsh.so L4/L5 信任分层为 r225-A DSH 面增量；OpenAgentSkill 官方来源面新；落。
- 未落：Pipedream Connect（r225-C 已落）；Activepieces Agents 实体化（r226-C 判重后与句子级构建重叠>60%）；agentskills.io 目录本身（r224 已落）；腾讯 SkillHub 数量面（r224 已落）。
