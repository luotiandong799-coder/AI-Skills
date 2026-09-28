# r281B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与 r281A 十词 + r280 全表 30 词 + r279 全表 30 词 + r278 全表 30 词错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（orchestration loops） | OK | Iteration 节点（数组元素循环、每轮可继续/终止）；Loop 节点（条件重复）；Loop 变量 Previous Iteration Reference（知识累积网络，节点可访问当前与之前迭代输出）；Parallel Mode（并行执行、最大并行度控 API 速率）；Error Response Method（单迭代项异常不影响其他）；graphon 引擎（DAG 拓扑排序执行计划、worker pool 并发、变量池）；agentic RAG（Agent Node 决策引擎：意图分析+工具编排+来源选择+重试逻辑）；深研工作流（子问题分解→检索→总结、visited_urls/knowledge_gaps 状态）；参数提取器节点 |
| 2 | n8n（code node） | OK | Code 节点清单（有意义逻辑/return 存在/返回 {json:{}} 数组/不用 n8n 表达式用模板字面量/守卫子句/All Items 模式/优先 map-filter 不手动循环）；模式选择（Run Once for Each Item=就地转换；Run Once for All Items=跨记录聚合或 100→1/1→100 数量变化）；$input.all() 读全部；**最常坏点=返回裸对象或无 json 包装**；命名描述性（Calculate Order Totals 而非 Code）；每节点一件事、超 50 行拆分或 sub-workflow；秘密用凭证管理不硬编码；环境变量可开外部 npm；AI 辅助生成（明确输入输出、避免歧义） |
| 3 | LangFlow（multi-agent） | OK | agent 可作其他 agent 的工具（tool mode，agent 调 agent 递归编排，1.1 新 agent component）；judge agent 路由（Judge Agent→Router→Specialized Agent，default/think 模型路由）；深研多代理（研究者→子问题→Summarization agent→Reviewer agent 查缺口/反方观点→Professional Research Writer，final writer 用大模型前段 lean 省成本）；flow 可部署为 MCP server 供外部 agent 当工具调用；LLM-agnostic；SSE streaming；LangSmith/LangFuse 可观测 |
| 4 | Activepieces（pieces） | OK | monorepo packages/pieces；CLI 构建自定义 piece（.tgz 归档）；生产环境 Activepieces 当 npm registry（存所有 piece 版本）；CI/CD sync 自定义 pieces；**两级管理：Platform Admin 全局装删 / Project Admin show-hide 特定项目**；OFFICIAL_AUTO 自动加载、AP_DEV_PIECES 本地开发；外部库装进 piece 自己 package.json（bun）；私有 piece 上传 tarball |
| 5 | Make（rollback） | OK | Rollback 错误处理器（回滚 ACID 模块、停止 run、默认行为当无 error handler 或 incomplete executions 禁用）；**不是所有模块支持真回滚（HTTP/API 调用只标记失败、无法撤销已发送请求）**；Commit（部分执行视为完整、保留到失败点写入）；Break（停止但状态 warning）；Ignore（静默继续）；选择逻辑（事务流 Rollback、部分完成有价值 Commit、暂时错误 Break/retry）；Restore/recover（Version history 手动版本恢复 + Scenario recovery 找回未保存改动）；垃圾箱 30 天保留 |
| 6 | Pipedream（webhook signature） | OK | **Pipedream 对每个 trigger webhook 投递用 HMAC-SHA256 签名，x-pd-signature 头（t=timestamp,v1=hmac）**；验证=用 secret 重算比较；app 特定签名（Typeform sha256=hmac 比较、Drip HMAC 验证 action）；**出站 webhook Pipedream 不自动签名（要验证来源自己实现）**；HTTP trigger 属性（body/client_ip/headers/method/path/query/url）；Return custom response 模式配合验证 |
| 7 | Anthropic（Agent Skills） | OK | Skills=可复用文件系统资源（工作流/上下文/最佳实践，把通用 agent 变专家）；四特性 Composable/Portable/Efficient/Powerful（可含可执行代码）；**按需加载：只预载几十 token 元数据进 system prompt，触发时才加载全文**；预构建 Skills（PowerPoint/Excel/Word/PDF）；Skills API（List Skills endpoint；Anthropic 版日期版本 vs 自定义 skver_ 版本）；SKILL.md YAML frontmatter（name kebab-case + description）；finance agent 模板（skills+connectors+guardrails）；arXiv 论文（skill=目录含 SKILL.md+frontmatter，subdirectories scripts/references/assets） |
| 8 | agentskills.io（首次实拉） | OK | 轻量开放格式；SKILL.md（name+description 元数据+指令）；目录 189+ verified skills 16 类（agenticskills.io）；llms.txt 机器可读索引；skills.sh 收录；跨平台（Claude Code/Cursor/Copilot/VS Code，symlinks 共享）；标准（scripts/references/assets 子目录、<5000 tokens 激活）；AgenticSkills=curated directory（不托管本体，链 GitHub/npm） |
| 9 | deeplearning（agentic RAG） | OK | Building Agentic RAG with LlamaIndex（Jerry Liu、44m、6 视频课）；**router 是最简 agentic RAG 形式（query 选 Q&A 或 summarization 两个 query engine 之一）**；多文档 agent 扩展；RAG 课程组件设计（keyword/semantic/hybrid search、chunking、query parsing、prompt design、evaluation、deployment）；query rewriting/grading/web fallback（LangGraph 版） |
| 10 | OpenClaw（file/attachments） | OK | 上传经渠道（web UI/Slack/Discord）存 sandbox uploads/；下载通过链接；模板变量 {{AttachmentPath}}/{{AttachmentUrl}}/{{AttachmentContentType}}/{{AttachmentDir}}（法版 {{MediaPath}}/{{MediaUrl}}/{{Transcript}}）；**attachment outcome markers（handled/handed to native vision/not selected by first-only policy/capability disabled/denied by scope/processing failed——不再静默丢弃）**；attachments 数组（file_name/mime_type/size_bytes/download_url）；2026.4.27 chat.send 扩展非图片附件（文档/音频/视频）；file_fetch/dir_list/dir_fetch/file_write 四工具（default-deny 安全姿态、per-node path policies+operator approval）；PDF 上传限制与浏览器 workflow 替代 |

## 判重（双键检索，增量判定）
- Dify 迭代循环（r281A 插件/r280 变量供应商检索/r279C Agent 节点）→ agentic RAG 已有涉，Iteration/Loop 节点+Parallel+Error Response+loop 变量为独有增量 → **落地**
- n8n code node（r281A 二进制/r280 表达式重试/r279 错误秘密）→ 新面（Code 节点规范与模式选择）
- LangFlow 多代理（r281A 认证/r279C agent 工具）→ 重叠>60% 但多代理编排（agent 调 agent/judge 路由/MCP server 部署）含独有增量 → **增量合并**
- Activepieces pieces（r281A 治理/r278B 自定义 piece）→ 两级管理（平台/项目级）+npm registry 形态为独有增量 → **落地**
- Make rollback（r281A 连接/r279C 错误重试）→ 重叠>60% 但 Rollback/Commit 语义+ACID 回滚限制+Restore/recover 含独有增量 → **增量合并**
- Pipedream webhook 签名（r281A 目录/r279A webhook）→ 重叠>60% 但 HMAC 签名验证机制（x-pd-signature/出站不自动签名）含独有增量 → **增量合并**
- Anthropic Agent Skills（r281A 记忆/r280A subagent/r279 缓存）→ 新面（官方 Skills 格式与按需加载机制）
- agentskills.io → 全新站点首次实拉 → **新面**
- deeplearning agentic RAG（r281A 编排/r278A agentic RAG）→ r278A 已落 agentic RAG 概念，router 最简实现+多文档 agent 为独有增量 → **增量合并**
- OpenClaw 附件（r281A 仪表板/r280 记忆 hooks 渠道）→ 新面（附件处理与 outcome markers）

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 迭代与循环编排 | 工具 |
| 2 | n8n Code 节点规范 | 工具 |
| 3 | LangFlow 多代理编排 | 工作流 |
| 4 | Activepieces piece 构建与两级管理 | 工具 |
| 5 | Make 回滚与错误处理器 | 工具 |
| 6 | Pipedream webhook 签名验证 | 工具 |
| 7 | Anthropic Agent Skills 规范 | 可复用 Skill |
| 8 | agentskills.io 开放格式 | 可复用 Skill |
| 9 | deeplearning agentic RAG 路由器 | 工作流 |
| 10 | OpenClaw 附件处理 | 工具 |

## 复核
十独点均有当日实拉来源；四点为增量合并（均含独有增量）、六点为新面；无纯重复。版本建议 3.60.0+。