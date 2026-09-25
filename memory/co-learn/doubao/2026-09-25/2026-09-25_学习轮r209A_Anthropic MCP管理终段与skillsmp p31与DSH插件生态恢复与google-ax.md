# 学习轮 r209-A：Anthropic MCP管理终段与skillsmp p31与DSH插件生态恢复与google-ax/cc-switch（2026-09-25）

## 实拉记录（12 次，超 10 次基线）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.anthropic.com MCP 页终段（9995-12739 全取完） | OK（managed-mcp.json/alwaysLoad/MCP prompts） |
| 2 | skillsmp.com/skills/page/31（#3001-3050） | OK（delivery-gate/click-path-audit 等 50+） |
| 3 | deepseek-plugin.org | **恢复成功（第 9 次）**——DSH Plugin Directory 12,733 插件 |
| 4 | skills.sh 续读（8259-13380） | 图片为主，无新内容 |
| 5 | general_search GitHub Trending（2026-09-25） | OK（google/ax、cc-switch、VoiceStudio 线索） |
| 6 | huggingface.co/blog | 死链（security strategy 拦截） |
| 7 | www.modelscope.cn 首页 | OK（模型趋势产品事实，低方法） |
| 8 | docs.openclaw.ai/concepts/progress | 死链 |
| 9 | blog.n8n.io 根 | 死链（security strategy 拦截） |
| 10 | docs.langflow.org 根页 | OK（v1.11.x 基础介绍，与 r206-A 重叠确认） |
| 11 | general_search google/ax | OK（Agent Executor 四原语/stateful actor） |
| 12 | general_search cc-switch | OK（跨 CLI 工具 MCP/Skills 统一管理） |

## 独点（4 个）
### A1：Anthropic MCP 管理终段：managed 配置双模式与 denylist 绝对优先（来源：docs.anthropic.com MCP 页终段 9995-12739，2026-09-25 实拉，r208-C C1 同源延续的新段）
- **Managed MCP 双模式**：Option 1 `managed-mcp.json` **独占控制**（系统级路径 macOS `/Library/Application Support/ClaudeCode/`、Linux `/etc/claude-code/`、Windows `C:\Program Files\ClaudeCode\`，需管理员权限）——用户不能增删改任何其他 server；Option 2 **策略控制** `allowedMcpServers`/`deniedMcpServers`——允许用户自加但限制范围；两者可组合（managed 存在时独占，策略仍过滤 managed 内加载）。
- **三型限制条目**：`serverName`（按名）/`serverCommand`（stdio 命令数组**精确匹配**，`["npx","-y","server"]` 不匹配 `["npx","server"]`）/`serverUrl`（远程 URL 通配 `*`，主机大小写不敏感、忽略尾 FQDN 点，路径大小写敏感）；每条目恰一个维度。
- **行为语义**：allowlist 含任何 serverCommand 条目时 stdio 必须匹配命令（不能只靠名字通过）；含任何 serverUrl 条目时远程必须匹配 URL；**空数组 `[]` = 完全封锁**（用户一个 server 都配不了）；undefined=无限制。
- **denylist 绝对优先**：server 同时在 allowlist 与 denylist → 仍拦截（**deny 胜出**，与 hooks permissionDecision deny>allow 同一语义）；deny 覆盖所有 scope。
- **alwaysLoad 豁免延迟加载**：服务器级 `alwaysLoad: true`（v2.1.121+）或工具级 `_meta["anthropic/alwaysLoad"]: true`——少数每轮都要用的工具豁免 Tool Search；启动时阻塞至多 5s 连接超时。
- **MCP prompts 命令化**：服务器暴露的 prompt 变成 `/mcp__servername__promptname` 命令；参数空格分隔；结果直接注入对话；server/prompt 名空格归一化为下划线。
- 判据：**企业环境用 managed-mcp.json 独占或三型策略**；关键工具用 alwaysLoad 豁免；deny 永远压过 allow。
- **提升层**：工具 / 可复用 Skill（MCP 治理）。

### A2：skillsmp p31：delivery-gate 机械完成门与 click-path-audit 触点状态序列（来源：skillsmp.com/skills/page/31 #3001-3050，2026-09-25 实拉）
- **delivery-gate（Stop hook 机械完成门）**：质量检查+学习捕获通过前**机械阻止** Claude 宣告完成——检测合理化模式（表面文本启发式）、陈旧学习日志（文件系统 mtime）、低磁盘空间；与自我审计互补，把"学习捕获习惯"变成强制。判据：**完成声明由 hook 机械把关而非模型自觉**（与 scipilot Gate 8 评审门同族，但这是执行层 Stop hook 硬拦截）。
- **click-path-audit（触点状态序列审计）**：追踪每个用户可见按钮/触点的完整状态变化序列，发现"功能单独工作但相互抵消、产生错误最终状态、UI 处于不一致状态"的 bug——**适合系统调试无错但用户报按钮失效、或共享状态存储大重构之后**。判据：**UI 正确性看"整条点击路径的最终状态"不看单个功能**。
- **agent-architecture-audit（12 层 agent 栈诊断）**：wrapper regression/内存污染/工具纪律失败/隐藏修复循环/渲染破坏，重要度排序发现项+代码优先修复。
- 附：security-scan（AgentShield 扫 Claude Code 配置：CLAUDE.md/settings.json/MCP/hooks/agent 定义注入风险）、zhuque-detect（腾讯朱雀 AI 检测导出官方报告 PDF）、cut（统一控制剪映+Premiere 的时间轴读写 skill）、mcp-builder DEPRECATED→mcp-app-builder 迁移声明（与 r201B 技能弃用声明模式一致）。
- 判据：**完成门机械执行、UI 审计按点击路径、agent 栈按层诊断**。
- **提升层**：可复用 Skill / 工作流。

### A3：deepseek-plugin.org 信源恢复与 DSH 插件生态 Top10（来源：deepseek-plugin.org 首页 2026-09-25，第 9 次成功）
- **信源健康度更新**：deepseek-plugin.org 累计 8 次失败后本次恢复成功——**结论：非死源，此前为暂时性不可达，健康度计数归零重新累计**（用户规则：10 次进不去才删）。
- **DSH Plugin Directory**：索引 **12,733 个 DeepSeek Harness 插件**，数据每日更新，按 GitHub stars 排行。
- **Top10 高价值插件**：reactive-resume（★41,287，MCP 读写锁在线简历）；腾讯 dsh-weknora（★21,008，**文档→可查询 RAG→自主推理 agent→自维护 Wiki** 知识管理管道）；vectorize-io hindsight（★20,431，项目长时记忆自动召回、会话自动保存、每 repo 共享记忆库）；MemTensor MemOS（★10,843，**四层长期记忆 L1 轨迹/L2 策略/L3 世界模型/skills**+每用户轮自动检索+六记忆工具注册）；**dsh-routing-suite（★6,979，先装运行时注入器再装任务感知推理模式路由预设 P1-P23，measurable）**；Q00 ouroboros（★5,588，uvx 跑规范驱动 AI 工作流 MCP 工具，Interview→Seed→Execute→Evaluate→Evolution 循环，免安装免代码）。
- 判据：**插件目录类信源偶发失败≠死源**，恢复后继续监控；推理模式路由预设（injector+router 两段式安装）是 DSH 生态独特方法。
- **提升层**：可复用 Skill（记忆分层/推理路由）。

### A4：google/ax 与 cc-switch：K8s 风格 agent 编排与跨 CLI 工具配置统一（来源：InfoQ/AI Mastery/腾讯云 2026-09-22 发布 + ccswitch.ai/ccswitch.co 2026-09-25 实拉）
- **google/ax（Agent Executor，2026-09-22 开源，Apache 2.0）**：Kubernetes 风格 agent 编排运行时，Go 声明式 YAML，跑在 **Agent Substrate**（Google+DeepMind 合建执行层）上；**把 agent 当 stateful actor 而非 microservice/batch job**；**亚秒级任务挂起/恢复**（HITL 确认、outage 中断后自动恢复，durable execution）；**四个声明式原语：Task / Workspace / Gateway / Model**；声明一个 agentic 任务→沙箱、工作区、网络围栏、规模化运行。配套：ADK 工作流 agent（SequentialAgent/ParallelAgent/LoopAgent——编排者无自己的工具，"工具"就是委托）+ AgentTool 显式委托 + A2A 协议。
- **cc-switch（farion1231，Tauri Rust+React 桌面应用）**：**一个面板统一管理 Claude Code/Codex/Gemini CLI/OpenCode/OpenClaw/Hermes 六个 CLI 工具的配置**——直接读写各自原生配置文件（~/.claude.json / ~/.codex/config.yaml / ~/.gemini / ~/.config/opencode / ~/.openclaw / ~/.hermes/config.yaml）；**MCP 与 Skills 统一管理：新增一个 MCP server 可同时下发到多个工具**；50+ 内置 provider 预设、一键切换；系统托盘快捷切换；**SQLite 原子写防配置损坏**；proxy 接管/session 搜索/sync。
- 判据：**agent 规模化用声明式编排原语（task/workspace/gateway/model）**；多 CLI 工具并存用统一配置层管理，避免手改六个 JSON/TOML。
- **提升层**：工具 / 工作流。

## 判重说明
- A1 → r208-C C1（MCP 0-9995 段）同源但本段（9995-12739）为全新内容（managed-mcp.json/alwaysLoad/MCP prompts 命令化/denylist 绝对优先），增量 >60%，落。
- A2 → 新（delivery-gate 机械门与 scipilot Gate 8 评审门互补、click-path-audit、12 层诊断），落。
- A3 → 新（deepseek-plugin.org 首拉成功+DSH Top10），与 r200C/r201C DSH 生态补强（routing-suite 注入器/MemOS 四层记忆），落。
- A4 → 新（google/ax 编排原语+cc-switch 配置统一），落。
- 未落：ModelScope 模型趋势（产品事实）、LangFlow 根页（与 r206-A 重叠确认）、n8n blog/HF blog/openclaw progress（死链）、skills.sh 续读（图片）。
