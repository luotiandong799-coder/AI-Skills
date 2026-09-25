# 学习轮 r207-B：Anthropic hooks后半环境持久化与完成标准前置与pipedream Connect与skillsmp白名单去AI味（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.anthropic.com hooks 页续读（13997-17983/34780） | OK（CLAUDE_ENV_FILE/Setup check-on-miss/UserPromptExpansion 盲区） |
| 2 | skillsmp.com/skills/page/27（#2601-2637） | OK（lieflat 白名单去AI味/video-talkcraft 评估循环/nemo-curator） |
| 3 | docs.pipedream.com/connect/（1281 全） | OK（MCP 聚合 10000+ 工具/不存 payload） |
| 4 | blog.n8n.io long-running-agents（0-3963） | OK（与 r205-B 重复段：harness/durable 已落） |
| 5 | blog.n8n.io long-running-agents 续读（3963-5942 全） | OK（完成标准前置/五类验证门/FSM/非生成式校验） |
| 6 | deepseek-plugin.org/plugins?page=2 | fetch error（死链，累计第 6 次） |
| 7 | dify.ai/blog 列表（3498/176413） | OK（$30M Pre-A/Sonilo/Marketplace 生态事实，增量<40%不落） |
| 8 | docs.openclaw.ai/automation/schedules | 死链 |
| 9 | docs.langflow.org/starter-projects | 死链 |
| 10 | make.com/en/help/general | fetch error（死链） |

## 独点（4 个）
### Y1：Anthropic hooks 后半：CLAUDE_ENV_FILE 环境持久化与 Setup check-on-miss 与 UserPromptExpansion 盲区（来源：docs.anthropic.com hooks 13997+ 段 2026-09-25，r207-A X1 的续读增量）
- **CLAUDE_ENV_FILE 环境持久化**：SessionStart/Setup/CwdChanged/FileChanged hooks 把 `export` 语句 append（`>>` 保留其他 hook 设置）写入该文件，会话内后续 Bash 命令全部可用；用 `comm -13 <(export -p before) <(after)` diff 捕获 setup 命令的全部环境变化。
- **Setup 语义**：只由 `--init-only` 或 `-p --init/--maintenance` 触发，**正常启动不触发、不能 block**；插件依赖不能只靠 Setup——**check-on-miss pattern**（首次使用时检测依赖存在与否，缺失才装，如 `${CLAUDE_PLUGIN_DATA}/node_modules` 不存在再 npm install）。
- **InstructionsLoaded**：CLAUDE.md/.claude/rules/*.md 加载时触发；**compaction 后指令文件会重载（load_reason=compact）**；memory_type=User/Project/Local/Managed；无决策控制，纯审计/合规/可观测。
- **UserPromptSubmit 默认超时 30 秒**（其他事件 600 秒）——每次 prompt 前跑且阻塞模型处理，卡住即 stall 会话，需时显式设 timeout。
- **UserPromptExpansion 覆盖 PreToolUse 盲区**：直接输入 `/skillname` 绕过 PreToolUse（Skill 工具只在该工具被 Claude 调用时触发）；UserPromptExpansion 捕获直接 slash 路径，可按 command_name 匹配，给 review 技能追加团队审核清单。
- **WebSearch hook 层域白名单**：PreToolUse input 含 allowed_domains/blocked_domains 字段——可在 hook 层强制搜索域范围。
- 判据：**会话级环境用 CLAUDE_ENV_FILE 而非每次设**；直接 slash 路径必须靠 UserPromptExpansion 拦。
- **提升层**：工具 / 工作流。

### Y2：n8n long-running Part 3：完成标准前置与五类确定性验证门与 FSM 与非生成式校验（来源：blog.n8n.io long-running-agents 全文 2026-09-25，r205-B 该文前半的 Part 3 增量）
- **completion criterion 执行前定义**：任务账本/清单每个 entry 的完成标准必须在 agent 执行前写定——"writing down the done condition before the agent starts is the single highest-leverage move"（**防止 agent 中途重定义 done**）；配套规则一次只做一个 entry（单 pass 单状态转换，验证可判定）。
- **五类确定性验证门**（从便宜可靠到复杂）：status/response codes（200 非 4xx/5xx）→ schema validation（JSON/XML 期望形状）→ cross-field consistency（payload 用户名=请求者身份）→ **state-diff checks（动作后重新查询确认目标系统确实变化）** → test execution。
- **FSM 状态机语义解析**：合法状态=tool-call/step 类型、迁移=允许序列，运行时把观测动作序列过 FSM；**机器外状态=violation、意外迁移=异常**。
- **沙箱行为基线升格**：先在受控环境观察 agent 实际行为（工具调用/数据量/目的地/系统调用）→ 安全动作**升格为确定性 allowlist 条目**（不靠 agent 判断重演）；行为画像作最小权限基线与偏差告警。
- **非生成式校验**：**encoder-only 分类器（BERT 系 DeBERTa/RoBERTa/ModernBERT）fine-tune 对齐/恶意样本**，输出标量对阈值——生成模型不在环。
- **工具调用模式异常检测**：监控递归循环（同工具反复小参数变化）、token 数尖峰、乱序执行，提前 kill。
- **LLM-as-judge 可接受用法**：意图必须**执行前显式定义**（工具白名单/步骤序列/数据源/子代理规则/API 端点）后 eval 才塌缩为对 execution log 的 Yes/No 问题；模型只做窄可检查判断（"trace 是否匹配 taxonomy 类别 X"——fuzzy compiler 映射，不是现场发明"好"）。
- **Restate/DBOS**：事件溯源/journal-based recovery；append-only execution log（每次工具调用/模型响应/状态转换）可确定性重放重建状态。
- 判据：**进度单元=有预定义完成标准的清单项**；验证尽量走非生成式门；LLM 只当 fuzzy compiler。
- **提升层**：工作流。

### Y3：pipedream Connect：MCP server 聚合 10000+ 工具与不存 payload（来源：docs.pipedream.com/connect/ 2026-09-25）
- **Connect=3000+ API 集成开发者工具包**：managed auth（Connect Link/Client SDK 几分钟接 OAuth/API key，代管用户凭据+token refresh）。
- **Pipedream MCP server**：给 AI agent 提供 **10000+ 工具（3000+ API）**——一次接入整注册表预建 tools/triggers。
- **Connect proxy**：发自定义 API 请求而**不碰客户凭据**（凭据由 Pipedream 代管）。
- **数据隐私**：Pipedream **不存储 API 请求 payload 与响应体**；凭据 HTTPS+加密 at rest；external_user_id 标识终端用户（跨集成归因）；SOC 2 Type 2、HIPAA BAA。
- 判据：**接入第三方 API 优先托管认证+代理**，应用代码不碰用户凭据；敏感 payload 选择不落盘的平台。
- **提升层**：工具。

### Y4：skillsmp p27：白名单式去 AI 味与口播视频评估循环与训练数据清洗（来源：skillsmp.com/skills/page/27 2026-09-25，与 r206-C W3 anti-defensive-writing 互补）
- **lieflat-less-ai-tone（白名单去 AI 味）**：只按 SKILL.md 显式列出的规则识别改写 AI 痕迹；**未命中规则的文字必须原样保留，也不能改变文章框架**——成稿清理期使用，与 anti-defensive-writing（删防御不拆承重）互补成"白名单改+承重留"。
- **video-talkcraft（口播视频全流程）**：中文口播稿+成品配音→CPU 字级时间戳→SHOTBOOK 层矩阵分镜→Remotion 电影感成片；统一视觉语言（Apple 范式）、108 张动效配方卡、**自动静止检测 + 独立 subagent 评估循环**（视频动效由独立子代理评估）。
- **nemo-curator（LLM 训练数据清洗）**：GPU 加速，fuzzy deduplication（16× 提速）、quality filtering（30+ 启发式）、semantic dedup、PII redaction、NSFW detection。
- **skill-stocktake**：审计技能质量，快速扫描仅变更技能/全面盘点，**顺序子代理批量评估**（不并行防上下文爆炸）。
- 判据：**去 AI 味用白名单锁定改动范围**；生成类产物配独立评估子代理；数据清洗先模糊去重再质量过滤。
- **提升层**：可复用 Skill / 工作流。

## 判重说明
- Y1 → r207-A X1 同源续读增量（CLAUDE_ENV_FILE/Setup/UserPromptExpansion/WebSearch 域白名单），落。
- Y2 → r205-B 该文前半（harness/durable）的 Part 3 全新段（completion criterion/五类门/FSM/非生成式/LLM-judge 约束），落。
- Y3 → r206-C W5（pipedream 触发隐私）的 Connect 增量（MCP 聚合/托管认证/proxy/不存 payload），落。
- Y4 → r206-C W3（anti-defensive）互补页（白名单式/评估循环/数据清洗），落。
- 未落：dify blog 生态事实（融资/Sonilo/Marketplace 增量<40%）、n8n 前半（与 r205-B 全重复）、openclaw schedules（死链）、langflow/make（死链）。
