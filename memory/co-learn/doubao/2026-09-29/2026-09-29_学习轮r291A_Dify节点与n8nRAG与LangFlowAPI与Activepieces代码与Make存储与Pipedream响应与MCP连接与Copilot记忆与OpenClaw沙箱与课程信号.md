# r291A 学习轮（2026-09-29，十站实拉→十独点）

批前核验：r290 编号已被凌晨另一流程占用并全部 push（03e3083→b868acc→6fe0048→36ce692，豆包线暂停期未写 doubao 文件），本批顺延为 r291。判重基线 = r284~r289C 留痕 + r290 批次 + SKILL.md 1,937,480B（r290 未动 wb-execute-discipline）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | 工作流节点三面：HTTP 请求节点模块化架构（模板变量+SSRF 防护+鉴权/超时管理）/ 代码执行沙箱（安全与资源限制）/ MCP 节点（MCP Server+Tool+输入 Schema 按协议发现调用）；LLM/HTTP/代码/工具四类节点新增异常处理 | 合并保留增量（r287A 错误处理面，本点核心=节点类型面） | 工具 |
| 2 | n8n | RAG 编排管道：Vector Store 节点 Insert/Retrieve 双操作 + Default Data Loader 分块 + Embeddings 选择 + rerank 重排序；metadata enrichment 异步管道（调度抓新 chunk+LLM 元数据+向量库过滤）；cache-first RAG（Redis LangCache，命中跳过嵌入与检索） | 新面 | 工作流 |
| 3 | LangFlow | API 三端点：Workflow API POST /api/v2/workflows 三模式 sync/stream/background（后台模式拿 job 轮询/回调）/ OpenAI Responses API 兼容端点 POST /api/v1/responses（现有 OpenAI 客户端库只改 model 名）/ advanced run 显式 inputs/outputs/tweaks；build flow 返回 job ID 流式事件 | 新面 | 工具 |
| 4 | Activepieces | CODE step 工具面：ap_read_step_code 返回完整源码（ap_flow_structure 截断 300 字符）/ AP_DEV_PIECES 环境变量编辑后重启后端自动重载 piece / createAction 四要素 name+displayName+props+run / Property 类型体系（ShortText/LongText/Dropdown+refreshers） | 合并保留增量（r289B piece 构建，本点=调试工具面） | 工具 |
| 5 | Make | Data Store 结构先行契约：先定义 Data Structure schema（列布局）再建 store，记录按结构校验；跨场景持久化（配置/状态/聚合结果） | 合并保留增量（r284A Make 存储/r289C Pipedream Data Store，本点=结构先行） | 工作流 |
| 6 | Pipedream | HTTP 响应语义：HTTP trigger 事件七属性（body/client_ip/headers/method/path/query/url）/ customResponse+this.http.respond() 自定义响应 / HTTP sources=可 API 管理的 request bins / 返回非 200 触发外部重试（默认 200 会吞掉重试）/ REST API 或私有实时 SSE 流消费事件源事件 | 新面 | 工具 |
| 7 | Anthropic MCP | 连接与工具面治理：远程 MCP 连接先验证 authenticity+审查权限（只连可信源）/ connector 两段式（mcp_servers 定义连接 + mcp_toolset 工具级启用，非全量加载）/ Streamable HTTP 推荐传输 / Server 三暴露面 tools+resources(read-only)+prompts(模板) / ClientSession 管理连接生命周期 | 新面 | 可复用 Skill |
| 8 | GitHub Copilot | Copilot Memory 机制：自动捕获仓库级 memories（编码规范/架构模式/跨文件依赖）/ 严格单仓库限定+应用前对照当前代码验证防 stale / 28 天自动过期 / Pro/Pro+ 默认开启 / 跨 coding agent+code review+CLI 生效；Knowledge Base=Enterprise-only（索引自定义文档）与 Memory 分工 | 合并保留增量（r289C Copilot 治理，本点=记忆机制） | 工具 |
| 9 | OpenClaw | 沙箱三键：mode off/non-main/all（默认 off）+ scope agent/session/shared（默认 agent）+ backend docker/ssh/openshell（默认 docker）；tools.sandbox.tools 工具策略与 subagent tool policy 分层优先级；Docker 危险选项显式命名（dangerouslyAllowReservedContainerTargets 等三个）；openclaw sandbox CLI 检查生效策略 | 新面 | 工具 |
| 10 | deeplearning.ai | 2026 课程方向信号：Agent Memory（记忆工程=一等基础设施：外部于模型/持久/结构化，Oracle AI DB+LangChain+LLM pipelines）/ Document AI（传统 OCR 丢失布局信息——合并单元格表格/图表与标题关系/多列阅读顺序，agentic 提取）/ Generative UI（生成图表/表单/白板等自定义 UI） | 新面 | 可复用 Skill |

判重口径：增量判定（重叠>60% 含≥40% 独有增量合并保留，纯重复不落）。本轮 7 新面 + 3 合并保留增量，零纯重复。