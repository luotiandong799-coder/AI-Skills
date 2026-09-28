# r283B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站；查询词与 r283A 十词 + r282 三十词 + r281 三十词 + 更早全表错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（知识库索引流水线） | OK | **文档处理四阶段：Extract（格式特定提取器：Notion/上传文件/网页）→ Transform（清洗规则+按处理规则分块）→ Load（生成 embedding+存向量+元数据）→ 索引状态（IndexingStatus 逐文档跟踪）**；分块格式：Paragraph/ParentChild/QA；知识管道编排：Data Source→Extractor+Chunker→Knowledge Base Node→User Input→Test & Publish；**索引方法 High Quality（向量）创建后不可降级 Economical**；引用与归因（Citations and Attributions 显示引用文档名）；Dify Dataset API 上传/实时更新/管理；dify-knowledge-sdk（datasets/documents/segments/metadata）；建议：大集合索引前先预览分块+代表性检索测试；PDF 上传前去页眉页脚页码 |
| 2 | n8n（Merge 节点） | OK | **Merge 五模式：Append（堆叠）/ Combine（按字段=SQL inner join、按位置=zip、全部组合）/ SQL Query / Choose Branch（条件选一支）**；**按位置合并：长度不等时短者决定输出，长出的丢弃**；业务常用模式=按匹配字段用稳定 key（email）连接 lead+enrichment；0.194.0 大改、1.49.0 起支持多输入；等所有输入就绪才合并 |
| 3 | LangFlow（starter projects） | OK | **内置模板库（模式=参考实现可改造复用）：Simple Agent（Agent+Calculator+URL 工具）/ Vector Store RAG（文件→分块→Astra DB 索引→检索）/ Multi-Agent（Travel Planning 多 agent 任务分解）/ Web Scraping（News Aggregator：AgentQL+SaveToFile）/ Code Generation（StructuredOutput+Parser 结构化生成）/ Basic Prompting / Prompt Chaining / Memory Chatbot / Blog Writer（Template Variables）/ Hybrid Search RAG / Document Q&A**；模板 JSON 文件存于 initial_setup/starter_projects/ |
| 4 | Activepieces（暂停/恢复） | OK | **waitpoint=持久化检查点：run 标记 PAUSED、执行状态持久化、resume 时 action 第二次调用（一次创建 waitpoint、一次读 resume payload），每个暂停 action 分支在 ctx.run 上**；**两类暂停：DELAY（到特定时间戳恢复）/ WEBHOOK（外部 HTTP callback 调用恢复，URL 对 run 唯一、携带请求体/头/查询参数到下一步）**；Approval 步骤=暂停等人审、捕获 decision/comments、恢复走选中路径；Resume Paused Run API（Human Input）；**Durable Execution：worker crash/部署→队列重分配→加载 log 重放；paused step→waitpoint fire→resume job 入队→worker 重放 run；重试失败步骤复用同 log** |
| 5 | Make（子文件夹/标签） | OK | **2026-08 新功能：子文件夹（多级层级，如 client→project，不用改名模拟层级）+ 标签（production/billing/experimental）+ 批量编辑（多选移动/批量增删标签）**；**命名规范：[DOMAIN]-[ACTION]-[SOURCE_SYSTEM]→[TARGET_SYSTEM]-[VERSION]**（例 [CRM]-Sync Contacts-HubSpot→Airtable-v2.1）；文件夹结构按部门/域/生命周期阶段；连接命名标注 owner+scope；网格视图按文件夹+过滤+搜索组合 |
| 6 | Pipedream（connected accounts） | OK | **OAuth 托管：Pipedream 自动 refresh、凭据紧密保管；Accounts Page 管理（连接/查看访问/删除）**；REST API Get account（include_credentials=1 返回凭据）；**Rotate client secret（API settings 旋转客户端密钥，复制后不可再见）**；**秘密存储分层：集成支持的用 connected accounts，否则 environment variables，绝不存代码**；Managed Auth：OAuth client ID+secret+short-lived token 启动连接流程；KMS 加密（AWS KMS AES-256 GCM、年度轮换） |
| 7 | Claude Code（output styles） | OK | **output styles 完全替换默认系统提示词（保留全部工具能力）**；内置 Proactive/Concise/Explanatory（区分大小写）；设置三通道：/output-style <style> 命令 / settings.local.json 的 outputStyle 字段 / /output-style:new [description] 创建自定义；项目级保存（不同项目不同风格）；SDK createOutputStyle(name, description, prompt)；**三层分工：CLAUDE.md 加项目上下文 / --append-system-prompt 追加指令 / output styles 替换人格与领域焦点** |
| 8 | GitHub（awesome-claude-code） | OK | **82K+ stars 生态目录**：分类分布=Tooling（40+：Claude Squad/ccflare 用量监控）/ Status Lines（5）/ Hooks（9：TDD Guard/CC Notify 桌面通知）/ Slash-Commands（35+：/commit /tdd /create-pr /prime）/ CLAUDE.md Files（25+：按语言模板 Kotlin/Python/Rust/TS）/ MCP Servers（Notion/Linear/Figma/Playwright）/ Workflows（TDD/重构）；子代理/技能/插件；Lockpaw（隐私锁屏：agent 运行时锁屏、暂停/完成时发光提示，非安全边界诚实披露）；MDXG Redline（人审闭环：浏览器行内评论→JSON→skill 应用到精确行） |
| 9 | OpenClaw（identity 配置） | OK | **set-identity 写入 agents.entries.*.identity：name/theme/emoji/avatar（workspace 相对路径/http(s) URL/data URI）**；**身份三层分离：soul（内部行为）vs IDENTITY.md（外部呈现：自我介绍/人格/命名）vs 配置层（openclaw.json/TOOLS.md：技术能力/工具访问/模型选择）**——身份可换不改灵魂；agent.md 支持多语言直接写中文；NVIDIA 声明式 manifest（id：小写字母数字+_/-、1-32 字符、首字母、不能 main；workspace/agentDir 自动填充） |
| 10 | deeplearning.ai（diffusion 课程） | OK | **How Diffusion Models Work（46m Intermediate）**：课程七步=Intuition 4m→Sampling 7m（代码）→Neural Network 3m→Training 6m→Controlling 5m→Speeding Up 4m→Summary；**学完目标：从零构建并训练自己的扩散模型、实现加速采样算法（10x）**；主题：Deep Learning/Diffusion Models/GenAI Applications/Generative Models |

## 判重（双键检索，增量判定）
- Dify 索引流水线（r268A RAG/r272B 分块/r279A 分块/r278A 混合检索）→ Extract-Transform-Load 四阶段+索引方法不可降级+引用归因为独有增量 → **增量合并**
- n8n Merge（r272C 分支/r282C 响应模式）→ 多流合并五模式为新面 → **新面**
- LangFlow 模板库（r272C/r274C/r281C 模板）→ starter project 模式分类（10 类参考实现）为独有增量 → **增量合并**
- Activepieces waitpoint（r270B 生命周期/r273B Webhook）→ 持久化暂停+durable 重放为新面 → **新面**
- Make 目录治理（r278C 团队/r276B 路由）→ 子文件夹+标签+命名规范为新面 → **新面**
- Pipedream 凭据生命周期（r278A 托管认证/r279B 安全/r272C 秘密）→ Rotate+分层存储+KMS 为独有增量 → **增量合并**
- Claude output styles（r282A 斜杠命令/r281A 记忆）→ 输出风格替换系统提示词为新面 → **新面**
- awesome-claude-code（r282C agentskills/r281B Anthropic Skills）→ Claude 专属生态目录（分类分布）为新面 → **新面**
- OpenClaw identity（r283A 团队编排）→ soul/identity/配置三层为新面 → **新面**
- deeplearning diffusion（r276C RAG/r274B 多模态）→ 从零建扩散模型+采样加速为新面 → **新面**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 文档索引流水线与索引方法约束 | 工具 |
| 2 | n8n Merge 多流合并模式 | 工具 |
| 3 | LangFlow 模板库参考实现分类 | 工具 |
| 4 | Activepieces 持久化等待点 | 工作流 |
| 5 | Make 自动化目录治理 | 工作流 |
| 6 | Pipedream 托管凭据生命周期 | 工具 |
| 7 | Claude 输出风格体系 | 工具 |
| 8 | Claude 生态目录地图 | 工作流 |
| 9 | OpenClaw 身份三层架构 | 工具 |
| 10 | 扩散模型从零构建路径 | 工作流 |

## 复核
十独点均有当日实拉来源；四点增量合并（均含≥40% 独有增量）、六点新面；无纯重复。版本建议 3.66.0。