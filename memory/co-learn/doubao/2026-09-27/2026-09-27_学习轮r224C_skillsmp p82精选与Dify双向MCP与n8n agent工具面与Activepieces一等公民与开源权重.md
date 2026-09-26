# 学习轮 r224C：skillsmp p82精选与Dify双向MCP与n8n agent工具面与Activepieces一等公民与Make AI Toolkit与Pipedream Connect与开源权重（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/82（#8101-8155 取） | OK |
| 2 | Dify marketplace 检索（双向 MCP/Creator Center/模板市场） | OK |
| 3 | n8n 检索（AI Agent node/HTTP Request as tool/$fromAI） | OK |
| 4 | LangFlow 检索（templates/use-cases/CSV Insights） | OK |
| 5 | Activepieces 检索（changelog/agents/MCP server） | OK |
| 6 | Make 检索（AI Toolkit/2026 更新） | OK |
| 7 | Pipedream 检索（Connect/MCP/Workday 收购） | OK |
| 8 | GitHub AI 标签仓库检索（agent-native/deepseek-harness/firecrawl） | OK |
| 9 | WaytoAGI 检索（蓝皮书/知识库用法） | OK（与 r224-A 重叠，无新增不落） |
| 10 | Hugging Face + ModelScope 检索（Qwen3.8 开源/Agents-A1/生态规模） | OK |

## 独点（4 个）
### C1：skillsmp p82 精选：输出验证三层管线 / 保量降 AIGC / 分镜一致性 / docx 模板转换（来源：skillsmp.com/skills/page/82，2026-09-27 实拉）
- **doublecheck（github/awesome-copilot ★39,255）**：**三层验证管线——①提取可验证主张 ②web 搜索找支持或反驳来源 ③对抗式幻觉审查 → 结构化验证报告带来源链接给人审**（AI 输出验证面，与 r223-B 输出校验面互补：从"校验格式"到"校验事实"）。
- **aigc-down-skill（zczjyq/de-AIGC-skill）**：**降低中文学术写作 AIGC 检测率——基于真实改写实验（AIGC 率从 >50% 降至 11%）归纳规律 + Wikipedia "Signs of AI writing" 模式分类；默认保量润色（避免为降 AIGC 大幅删短）；会话记忆库避免重复释义、滚动段落摘要防前后不一致；LaTeX 源文件保护**（去 AI 味/学术写作面增量：保量润色+滚动摘要防不一致）。
- **storyboard-consistency（lujiaheng-artpivot ★3）**：**AI 视频分镜一致性引擎——3D 空间锁定+180°轴线规则+双提示词体系（首帧/视频），解决角色换脸/场景换景/空间越轴三大一致性崩塌**（AI 视频创作面专项）。
- **docx-template-translator（zouchenzhen ★71）**：**LaTeX/PDF/Markdown→按用户 .docx 模板自适应转换——pandoc --reference-doc 不够时（封面/声明/TOC/标题编号/三线表/公式/引用/视觉验证）**（文档转换面，Word/论文场景可复用）。
- **提升层**：可复用 Skill / 工作流。

### C2：Dify 双向 MCP + n8n agent 工具面：$fromAI 运行时占位 / HTTP as tool / 迭代上限（来源：marketplace.dify.ai + dify.ai/blog + n8nlogic/community，2026-09-27 实拉）
- **Dify 双向 MCP（v1.6.0 内建）**：**任意 MCP server 作工具；或把 Dify agents/workflows 暴露为 MCP server——hjlarry/mcp-server 插件把 workflow app 变 MCP server（endpoint 插件+输入 schema 定义）；langgenius OpenAI Compatible 插件把 Dify app API 转 OpenAI 兼容 API**（Dify 应用外露面，r224-A A2 插件化推理策略面增量）。
- **Dify Creator Center + Template Marketplace（2026-09-17）**：**创作者发布 workflow 模板、用户一键采用，可选 PartnerStack 联盟赚循环佣金**（模板分发面）。
- **n8n $fromAI() 运行时参数占位**：**HTTP Request 参数里写 ={{ $fromAI('city','需要查天气的城市') }} 让 agent 在运行时填参**（agent 动态填参机制面，n8n 独有）。
- **n8n HTTP Request as tool + Max Iterations=最长工具链+2**：**agent 附加 HTTP Request 节点为工具（OAuth/API key/basic auth credential），agent 自行决定何时调用与传参；Max Iterations 设为最长真实工具链+2 防死循环**（agent 工具面）。
- **提升层**：工具 / 工作流。

### C3：Activepieces 一等公民 + Make AI Toolkit + Pipedream Connect（来源：activepieces.com/changelog + apps.make.com + pipedream.com/docs，2026-09-27 实拉）
- **Activepieces Agents 一等公民化（2026-09 changelog）**：**agent 从"flow 一步内的设置包"变成可命名、可 brief、可对话、可复用的一等公民；一句话构建（"summarise my unread emails every morning"）；Agent Builder 三要素=instruction+tools+knowledge；Custom Tools 用 TypeScript createAction 自写**（agent 抽象面）。
- **Activepieces 单 URL MCP（2026-09-24）**：**一个 MCP server 暴露 760+ apps 给 AI 作工具——Claude/Cursor 经单一连接调全部 pieces**（多 app 单点暴露面，与 Dify 双向 MCP 互补）。
- **Make AI Toolkit（apps.make.com/ai-tools）**：**8 个即用 AI 模块——sentiment/categorize/language detect/extract/standardize/summarize/translate/chunk text；AI provider 可选（Make 自带或自定义 OpenAI/Anthropic）**（AI 工具模块化面，r224-A A3 Maia 面增量）。
- **Pipedream Connect 托管 MCP（2026-09-22）**：**Connect 提供 SDK+MCP server 暴露 10,000+ 预构建 tools（3,000+ apps）给 agent——managed auth/tool discovery/跨数千 API 执行；LangChain/CrewAI 直接指 Pipedream MCP server；Workday 2026-02-24 完成收购，定位企业 agent 连接层**（集成即服务面，r223-A Pipedream 面增量）。
- **提升层**：工具 / 工作流。

### C4：agent 框架与开源权重：agent-native / deepseek-harness / Qwen3.8-2.4T-A95B / Agents-A1（来源：aitoolly.com + dev.to + hokai.io + modelscope.ai，2026-09-27 实拉）
- **BuilderIO agent-native（2026-09-22 开源即上 Trending）**：**专用于构建 Agent 智能体应用的框架——顺应从"大模型对话"向"自主智能体"演进**（agent 应用框架面）。
- **deepseek-harness（deepseek-ai ★208,095）**：**模块化 harness，"Everything is a Plugin"——从数据处理到模型执行每个组件可替换/扩展**（插件化 harness 面，r224-A A4 DeepSeek-Reasonix 面延伸）。
- **Qwen3.8-2.4T-A95B（Alibaba，2026-08 开源）**：**首个 Qwen-Max 级开源权重——2.4T 参数 MoE 每 token 激活 95B，面向 agentic coding 与 long-horizon 推理（此前需闭源 API）；Qwen3.8-Max-0902 为后训练升级（2.4T/1M context/$2-6 per M token）**（开源权重面）。
- **Agents-A1（InternScience，ModelScope 2026-09-22）**：**35B agent 达到万亿参数性能——"Scaling the Horizon, Not the Parameters"；4B 版已发布+量化变体**（agent 模型面）。
- **ModelScope 生态规模（2026-09-17）**：**2.9m models / 259.4k datasets / 12.5k MCP / 83.1k skills**（生态事实）。
- **提升层**：模型 / 工具。

## 判重说明
- C1 全新面（doublecheck 事实验证管线/aigc-down 保量润色/分镜一致性/docx 模板转换），落。
- C2 Dify 双向 MCP 为 r224-A A2 增量（应用外露具体插件做法）；n8n $fromAI 为 r224-A A2 增量（运行时填参机制）；合并落。
- C3 Activepieces 一等公民+760 apps MCP 为 r223-A 面增量；Make AI Toolkit 为 r224-A A3 增量；Pipedream Connect 为 r223-A 增量；合并落。
- C4 agent-native/deepseek-harness 为 GitHub 面新点；Qwen3.8/Agents-A1/ModelScope 生态为模型面新事实；落。
- 未落：WaytoAGI（蓝皮书与 r224-A A4 重叠）；LangFlow templates（Agentics/Simple Agent 均已在 A/B 轮落过）。
