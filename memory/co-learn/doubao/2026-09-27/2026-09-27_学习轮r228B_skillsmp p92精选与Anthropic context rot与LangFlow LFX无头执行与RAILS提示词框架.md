# 学习轮 r228B：skillsmp p92精选与Anthropic context rot与LangFlow LFX无头执行与RAILS提示词框架（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/92（total_length=11457，读到 #9178 截断约 8800） | OK |
| 2 | Dify（docs：Agent Strategy Plugin 开发/30-min quick start） | OK |
| 3 | n8n（community/workflows：Data Table 会话记忆/Bedrock AgentCore/Redis 缓冲） | OK |
| 4 | LangFlow（1.13 docs：LFX 无头执行/bundles/custom components） | OK |
| 5 | Activepieces（docs：sandboxing/AI Agent Development 五步） | OK |
| 6 | Make（help：工具命名最佳实践/文件处理三通道） | OK |
| 7 | Pipedream（Connect：custom tools Components API/quickstart） | OK |
| 8 | Anthropic（engineering/cookbook：context rot/三策略/brain-hands 解耦） | OK |
| 9 | GitHub 生态与趋势（github.hot 2026-09-26/Firecrawl 最佳仓库） | OK |
| 10 | WaytoAGI（LangGPT 提示链/RAILS 框架） | OK |

## 独点（4 个）
### B1：skillsmp p92 精选：提问机/NDA 三色分诊/决策就绪审查/上下文文档先建（来源：skillsmp.com/skills/page/92，2026-09-27 实拉）
- **ljg-qa 信息提问机（lijigang/ljg-skills ★7,381）**：**把一篇文章/论文/书的观点抽成尖锐 Q-A 对——Question 切要害不教科书；Answer 简洁清晰、有形式化收口、逻辑链完整；读者顺 Q 链走过复现作者整套推理——是智力脚手架不是摘要**（知识提取面：与摘要明确区分，服务"复现推理链"）。
- **nda-review 三色分诊（anthropics/claude-for-legal ★9,491）**：**进来的 NDA 快速分诊为 GREEN/YELLOW/RED，团队只在真需要时才花律师时间；为销售和 BD 自服务设计，找律师前先过它**（分诊面：把稀缺专家时间留给真正需要的人）。
- **financial-model-review 决策就绪审查（★待查）**：**投资者优先的财务模型审查工作流——"review this model"/"stress test these assumptions"/"what breaks in this forecast"/"is this model decision-ready"**（审查面：先找会破的假设再判决策就绪）。
- **marketing-context 营销上下文文档先建（alirezarezvani/claude-skills ★26,225）**：**创建并维护所有营销技能开始前必读的上下文文档——brand voice/target audience/ICP/style guide/positioning，避免每个营销任务重复基础信息**（上下文面：共享上下文文档消除跨任务重复）。
- **提升层**：工作流 / 可复用 Skill。

### B2：Anthropic context rot 与三策略区分 / LangFlow LFX 无头执行 / Activepieces 执行隔离（来源：platform.claude.com cookbook 2026-03-20 + docs.langflow.org 1.13 + activepieces.com docs，实拉）
- **context rot + 三策略区分（Anthropic cookbook）**：**context rot——窗口 token 越多，模型从上下文准确召回信息的能力越下降，硬限制到达前就退化**；三个上下文策略**各自不同且全部有 first-party API**：**compaction 蒸馏窗口成高保真摘要 / tool-result clearing 丢弃旧的可重新获取的结果但保留"调用发生过"的记录 / memory 结构化笔记写入持久外部存储**（上下文管理面：tool-result clearing 与压缩/记忆明确分工）。
- **Scaling Managed Agents：brain 与 hands 解耦**：**harness 编码的假设会随模型改进而过时；围绕稳定接口构建，harness 变化时接口不变**（架构面：接口稳定优先于 harness 演进）。
- **LangFlow LFX（Langflow Executor）无头执行**：**轻量 CLI/Python 库，flow 在可视化构建器搭好、flow JSON 用 LFX 静态运行——无状态、最小依赖、无数据库、无 UI**（执行面：flow 定义与运行时解耦，可进 CI）。
- **Activepieces AP_EXECUTION_MODE sandbox 隔离 + agent 构建五步**：**flow 代码总在 sandbox 跑、包住 engine 进程，AP_EXECUTION_MODE 决定隔离模式**；**agent 构建五步：定义 agent 怎么想→建持久上下文记忆→连接工具→搭执行框架→加护栏和测试**（执行安全面：隔离是默认不是可选）。
- **提升层**：工具 / 工作流。

### B3：GitHub 新仓库（paperclip/Bumblebee/SkillKit）/ Make 文件处理三通道 / Pipedream custom tools（来源：github.hot 2026-09-26 + firecrawl.dev 2026-08-27 + help.make.com 2026-07-20 + pipedream.com docs，实拉）
- **paperclip（trending 第一，2026-09-26）**：**"the open-source app everyone uses to manage agents at work"——开源 agent 管理工作应用**；**Bumblebee（Perplexity）**：**扫描依赖和 MCP server 的供应链威胁**；**SkillKit**：**46 个 agent × 31 个来源的 skills 包管理器**（生态面：agent 管理/供应链扫描/跨源 skill 包管理是三个新方向）。
- **Make AI Agent 工具命名与描述即选择判据**：**agent 根据工具的名称和描述选工具——添加工具时清楚描述"做什么、何时调用"，例："add customer email to spreadsheet"**；**文件处理三通道：knowledge files 存信息 / 工具检索处理文件 / agent 内直接处理文件（解析和创建无需额外模块）**（工具设计面：名称+描述是 agent 的工具接口）。
- **Pipedream custom tools（Components API）**：**自定义工具是 Node.js 模块，用 Pipedream Components API 开发并发布到 workspace 供 Connect 使用；一个 external_user_id 可同时拥有多个 app 的连接**（工具扩展面：标准组件 API + 用户级多 app 关联）。
- **提升层**：工具 / 可复用 Skill。

### B4：RAILS 提示词框架与 3 次升格规则 / n8n Data Table 会话记忆与单 harness 多 agent（来源：nesyona.com 2026-06-01 + n8n.io/workflows + blog.n8n.io 2026-08-20，实拉）
- **RAILS 框架**：**可复用提示词五要素——Role/Architecture/Instructions/Loop/Safety，每个关闭一个具体失败模式；self-critique Loop 是最高杠杆最低采纳的动作；负面约束（禁用语清单）比纯正面指令更有效控制风格与格式；参数化（{{context}}/{{voice}} 变量槽）区分可复用模板与一次性粘贴**；**3 次升格规则：同一个 prompt 改 3 次以上就不再是 prompt，是系统——给它 schema、测试和版本号**（提示工程面：可复用提示词的成型判据）。
- **n8n Data Table 会话记忆实现**：**多会话 chat agent 把长期对话记忆存 n8n Data Table、按 session ID 组织，可按 name/email 回查过去上下文，同时强制身份验证**（会话记忆面：r227-B 会话 ID 概念的 Data Table 具体实现+身份验证增量）。
- **Amazon Bedrock AgentCore 单 harness 多 agent**：**一个 harness 服务四个 agent——triage agent 路由客户问题给三个专家（沙箱算数/加载 AWS 指导/调查），四者共享每客户记忆，没人被要求重复自己**（编排面：单 harness 多专家+共享客户记忆）。
- **Smart Redis Buffering（Evolution API WhatsApp）**：**等用户打完完整想法（text/audio）再回复，模拟人类交互模式而非即时回复每条消息**（交互面：缓冲防碎片化对话）。
- **提升层**：工作流 / 可复用 Skill。

## 判重说明
- B1 ljg-qa（观点→问题序列，与摘要明确区分）、nda-review 三色分诊、financial-model-review（stress test assumptions + decision-ready）、marketing-context 共享上下文文档均新面；落。
- B2 context rot 现象+tool-result clearing 三策略分工（r225 压缩质量门为互补面，本次为三策略选择+API 支持）；brain/hands 解耦新；LFX 无头执行新；AP sandbox 隔离+构建五步（r227-B 六步流程为 Make 面，本次 Activepieces 五步含护栏测试）增量；落。
- B3 paperclip/Bumblebee/SkillKit 为 Trending 新仓库新面；Make 工具命名+文件三通道增量；Pipedream custom tools 新；落。
- B4 RAILS 五要素+3 次升格+负面约束优于正面（r226 结构化提示词为单 prompt 面，本次为可复用框架+升格判据增量）；n8n Data Table 会话记忆（r227-B 数据库 backed memory 概念，Data Table 具体实现+身份验证+name/email 回查为 ≥40% 增量合并）；Bedrock AgentCore 单 harness 共享记忆新；Redis 缓冲新；落。
- 未落：LangGPT Prompt Chain（r227-B prompt chaining 已落，本批为同概念中文系统文，纯重复）；Anthropic dreaming（r226-C JIT 修复+蒸馏已覆盖 out-of-band 学习面）；vLLM GPU 权重缓存（基础设施面，个人使用场景外）。
