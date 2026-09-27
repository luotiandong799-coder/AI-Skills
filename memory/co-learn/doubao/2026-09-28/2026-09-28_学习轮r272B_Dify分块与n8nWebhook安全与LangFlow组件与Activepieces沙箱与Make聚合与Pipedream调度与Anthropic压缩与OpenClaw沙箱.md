# r272B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站，查询词与全表错开；Make 首词无收获换词重拉）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（知识库/检索面） | ✓ | **分块策略**（通用/常规/长上下文/父子/表格/Q&A——按文档类型匹配）；**索引方法**（向量化=高质量 vs 关键词=经济型——成本与语义深度取舍）；**检索方法**（语义/关键词/全文/混合）；**混合检索**（全文+向量同时+重排序选最佳；weight settings 语义/关键词权重无需 rerank API 或启用 rerank；TopK+Score Threshold）；**权重配置**（Semantic=1/Keyword=0 纯向量；0/1 纯关键词；自定义比例）；**分块大小**（200-500 token 推荐）；**Knowledge Pipeline**（Chunker→KB→User Input） |
| 2 | n8n（webhook 安全面） | ✓ | **内置认证四法**（Basic/Header/JWT/None）；**HMAC-SHA256**（crypto.createHmac sha256 secret 验证——GitHub 风格；timingSafeEqual 防时序攻击；raw body 逐字节签名）；**防重放**（timestamp 过期拒绝默认 5 分钟）；**IP allowlisting 补充**；**事件 ID/数据哈希幂等**（X-GitHub-Delivery/Stripe event.id）；**CVE-2026-86080**（GitHub Trigger 422 reuse path 跳过 secret 存储→签名验证 fail-open） |
| 3 | LangFlow（自定义组件面） | ✓ | **Component 类**（继承 Component；class-level 属性；inputs/outputs 列表定数据流；methods 定义行为；内部变量错误处理）；**lfx 导入**（from lfx.custom import Component；FloatInput/MessageTextInput/Output）；**作 agent 工具**（New Custom Component；Code pane）；**贡献/发布**（pyproject.toml 依赖；python -m build+twine PyPI；pip install 后启动 discovery 自动出现）；**LFX_DEV=1 热重载**；**langflow-builder-mcp**（add_custom_component 远程 tool_mode） |
| 4 | Activepieces（沙箱面） | ✓ | **AP_EXECUTION_MODE 四模式**（UNSANDBOXED/SANDBOX_PROCESS/SANDBOX_CODE_ONLY/SANDBOX_CODE_AND_PROCESS——默认 UNSANDBOXED）；**SANDBOX_CODE_ONLY**（isolated-vm 128MB/isolate AP_SANDBOX_MEMORY_LIMIT；require 移除；step 后 dispose）；**安全**（128MB 防 DoS/无文件/无网络用 pieces）；**表达式限制**（16384 源字符/2048 tokens/depth 64/10000 访问/1048576 输出字符）；**KV 512KB/128 字符 key**；**执行限制**（flow/action 10 min；worker concurrency 1 cloud）；**网络守卫**（AP_NETWORK_MODE=STRICT 独立于沙箱）；**CVE-2026-73083**（importFresh 委托 require 加载先于隔离边界→host 引擎执行） |
| 5 | Make（函数/聚合面，换词成功） | ✓ | **Make Functions app**（IML 函数之前仅映射字段——现独立模块；空输入输出空结果不停止场景）；**聚合器三类型**（Array 多 bundle 成数组；Text 拼接指定分隔符；Numeric 求和/平均/最大/最小）；**IML 函数**（flatten/join/keys/last/length）；**组合**（{{ join(map(...); delimiter) }} 多值拼串；Iterator+Text Aggregator）；**Tools 集成**（Increment 首次 1 每次+1；Get/Set variable）；**嵌套数组**（flatten/map 处理 suppliers[].offer.variants[].prices——复杂用 JS Code） |
| 6 | Pipedream（调度面） | ✓ | **schedule 定义**（intervalSeconds 秒频率/cron 自定义+timezone）；**Cron Scheduler 属性**（interval_seconds/cron/timestamp/timezone_configured/timezone_utc）；**Schedule API 五类型**（Custom Interval/Daily+timezone/Weekly 多天/Monthly/Cron）；**timer interface**（$.interface.timer 默认 15 分钟）；**UTC 默认无选择器**（schedule triggers 默认 UTC——UI 无时区选择器手动换算；'0 8 * * 1-5' 8AM UTC；next run 预览）；**CLI**（pd deploy --run cronjob.js --timer --frequency 15s/--cron） |
| 7 | Anthropic（长上下文/压缩面） | ✓ | **Server-side compaction 推荐**（自动摘要旧上下文接近窗口；扩展有效长度；保持活动上下文小——对话变长响应质量下降）；**启用**（compact_20260112 加 context_management.edits；summary_prompt 自定义）；**阈值**（低阈值更频繁窗口小；高阈值风险达限；token counting endpoint；server-side tools 大量使用避免）；**摘要内容**（Current State 完成/文件/输出；Important Discoveries 约束/决策/错误解决；Next Steps 行动/blockers/优先级）；**keep-verbatim zones**（system prompt+工具 schema 字节稳定保 prefix-cache；任务声明+验收；最近 5-7 turns 完整）；**tool-result clearing**（stale 输出换占位符保留调用记录）；**cookbook 保真**（压缩保留 3/3 高层事实但 0/3 晦涩细节——custom prompt 点名 must-keep；关键 specifics 压缩前写外部 memory） |
| 8 | deeplearning.ai（agentic 面） | ✓ | **Agentic AI 课程（9h55m）**（M1 介绍——benefits/applications/task decomposition/evals；M4 实用——evals/error analysis/component-level evals；M5 高自主——Planning workflows/LLM plans/planning with code execution/Customer Service Agent lab/Multi-agentic workflows/Market Research Team lab）；**Planning**（复杂任务分解可执行步骤 AI 适应变化）；**Multi-Agent**（多专门系统协调复杂工作流）；**Python 第一原理构建**；**crewAI 两课**（Practical 2h39m——automated project planning/estimation/allocation/internal external integrations/complex crew setups/agentic sales pipeline/generate deploy monitor；Design Develop Deploy 12h58m 38 视频 7 assignments）；**AutoGen**（AI Agentic Design Patterns——multi-agent conversation/sequential chats） |
| 9 | GitHub（MCP 生态面） | ✓ | **GitHub MCP Server 32.8k★**（官方——repos/PR/issues/code search 直接在 Claude/Cursor；~130 tools 15+ toolsets；transport stdio+hosted remote api.githubcopilot.com/mcp/；auth OAuth 2.1 remote/PAT env local；Docker ghcr.io/github/github-mcp-server）；**modelcontextprotocol/servers 89.4k monorepo**（GitHub reference server 已归档）；**Playwright MCP**（Microsoft 官方浏览器自动化——驱动浏览器非截图）；**fastmcp/ghidramcp/xcodebuildmcp**（实施榜）；**mcp-use**（Fullstack MCP 框架）；**arcade-mcp 932★**（工具开发库认证调用）；**GitHub Actions MCP**（管理 Actions 工作流） |
| 10 | OpenClaw（安全/沙箱面） | ✓ | **沙箱权限模型**（主安全边界；Level 2 write 可创建/修改/删除沙箱内——file_write）；**scope**（"agent" 默认/“session” 更严格按会话/"shared" 单容器——防 agent 互访）；**容器边界**（完整 Gateway Docker；工具沙箱 host Gateway+沙箱工具 Docker 默认）；**exec 模式**（deny 禁用/allowlist 预批准/full 任意默认最高风险）；**安全默认**（出厂阻断破坏性系统命令/文件限制工作区/外部发送需批准）；**子代理沙箱**（无网络默认+只读根+受限工作区）；**sandbox-guard skill**（未信任技能生成 Docker 沙箱——Minimal profile；限制爆炸半径） |

## 判重（双键检索结果）
- Dify 知识库/检索：库内已落 §混合检索（r269C）+§RAG chunking——分块策略六类+索引方法成本取舍+weight 无 rerank 模式为独有增量 ≥40% → 落地（增量合并）
- n8n Webhook 安全：库内已落 §Webhook 防护——HMAC 验证代码+timingSafeEqual+防重放窗口+CVE fail-open 案例为独有增量 ≥40% → 落地（增量合并）
- LangFlow 自定义组件：库内已落 §组件构建——Component 类继承结构+PyPI 发布+LFX_DEV 热重载为独有增量 ≥40% → 落地（增量合并）
- Activepieces 沙箱：库内已落 §Code Step 沙箱——四模式配置+128MB isolate+表达式限制+网络守卫+CVE bypass 为独有增量 ≥40% → 落地（增量合并）
- Make 函数/聚合：库内已落 §数组聚合——Make Functions 独立模块+三类型对比+IML 清单+increment 为独有增量 ≥40% → 落地（增量合并）
- Pipedream 调度：库内已落 §Schedule——UTC 默认+UI 无选择器+五类型+CLI 部署为独有增量 ≥40% → 落地（增量合并）
- Anthropic 压缩：库内已落 §Server-side Compaction——compact_20260112 参数+keep-verbatim zones+tool-result clearing+保真案例为独有增量 ≥40% → 落地（增量合并）
- deeplearning agentic：并入记录（Agentic AI/crewAI 课程情报）
- GitHub MCP 生态：并入记录（GitHub MCP Server 详情+mcp-use/arcade）
- OpenClaw 安全/沙箱：库内已落 §信任边界——沙箱 Level 模型+scope 三档+exec 三模式+子代理无网络只读根为独有增量 ≥40% → 落地（增量合并）

## 独点落地（8 个）
| 轮 | 文件(建议落点) | 版本(建议) | 独有点 | 提升层 |
|---|---|---|---|---|
| r272B-1 | wb-execute-discipline | 3.33.0+ | Dify 分块策略与索引方法（增量合并 §混合检索） | 工作流 |
| r272B-2 | wb-execute-discipline | 3.33.0+ | n8n Webhook HMAC 与防重放（增量合并 §Webhook 防护） | 可复用 Skill |
| r272B-3 | wb-execute-discipline | 3.33.0+ | LangFlow 自定义组件结构与发布（增量合并 §组件构建） | 可复用 Skill |
| r272B-4 | wb-execute-discipline | 3.33.0+ | Activepieces 沙箱模式与表达式限制（增量合并 §Code Step 沙箱） | 工具 |
| r272B-5 | wb-execute-discipline | 3.33.0+ | Make 聚合器与 IML 函数（增量合并 §数组聚合） | 工作流 |
| r272B-6 | wb-execute-discipline | 3.33.0+ | Pipedream 调度 UTC 与 Schedule API（增量合并 §Schedule） | 可复用 Skill |
| r272B-7 | wb-execute-discipline | 3.33.0+ | Anthropic Server-side Compaction 保真（增量合并 §Server-side Compaction） | 可复用 Skill |
| r272B-8 | wb-execute-discipline | 3.33.0+ | OpenClaw 沙箱权限模型（增量合并 §信任边界） | 可复用 Skill |

## 复核
八独点均有当日实拉来源；均为增量合并；并入记录：deeplearning agentic 课程、GitHub MCP 生态。垃圾：本轮未产生临时文件。
