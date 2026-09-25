# 学习轮 r215-B：Claude Code权限与沙箱续读与skillsmp p54精选与OpenClaw channels官方与DeepSeek Harness插件目录（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/54（#5301-5351，5941/11842 取） | OK（pua/aidetect/assessing-heatmaps/serverless-mcp/visual-qa 等） |
| 2 | dify.ai/blog 续读（76583-81987） | OK（Deep Research 详细版/Palo Alto AI Security 插件/InfraNodus） |
| 3 | docs.anthropic.com claude-code/settings 续读（5000-10993） | OK（权限规则求值顺序/沙箱/技能列表预算/worktree） |
| 4 | docs.langflow.org/glossary | 死链（link dead，计数） |
| 5 | skillsmp.com/skills/page/54 续读（5941-11842，#5352-5400） | OK（reference-verify/cross-documentation/web-design-engineer/novel-video-pipeline 等） |
| 6 | github.com/trending | OK（paperclip ★83,263，同日重复不重落） |
| 7 | deeplearning.ai/short-courses 续读（39004-43417） | OK（Voice for AI Agents 三模式/JAX 20M LLM 课程） |
| 8 | docs.openclaw.ai/channels（2280/2280 取） | OK（30+ 通道/Group join introductions 安全机制） |
| 9 | docs.n8n.io 根页（1227B） | OK（llms.txt/.md 后缀/Claude Code 接 n8n MCP，与 r214-B 重复） |
| 10 | deepseek-plugin.org 根页（596B） | OK（12,733 插件/MemOS 四层记忆/Ouroboros 等） |

## 独点（4 个）
### B1：Claude Code settings 权限与沙箱层：求值顺序 / 沙箱域白名单 / 技能列表预算 / worktree 隔离（来源：docs.anthropic.com claude-code/settings 续读，2026-09-25 实拉；A1 同页增量合并）
- **权限规则求值顺序**：deny 先、ask 次、allow 后，**第一条匹配的规则胜出**——读敏感文件必须 deny 明确路径（`Read(./.env)`、`Read(./secrets/**)`）。
- **沙箱文件系统**：allowWrite/denyWrite/denyRead/allowRead（denyRead 区域内 allowRead 优先）；数组**跨所有作用域合并而非替换**（user/project/managed 叠加）；allowManagedReadPathsOnly=managed-only 读白名单。
- **沙箱网络**：allowedDomains/deniedDomains（denied 优先）；**allowManagedDomainsOnly（managed-only 域白名单，非白名单自动阻断不提示用户）**；httpProxyPort/socksProxyPort 自带代理；failIfUnavailable（沙箱起不来就报错=硬门禁）；allowUnsandboxedCommands=false 彻底禁用 escape hatch。
- **技能列表预算**：**skillListingBudgetFraction（默认 0.01=1% 上下文）**——超出预算时最不常用技能描述折叠成裸名（仍可调用但看不到 why），/doctor 显示截断数与受影响技能；**maxSkillDescriptionChars（默认 1536）**；**skillOverrides（on/name-only/user-invocable-only/off）** 不改 SKILL.md 就隐藏/折叠技能。
- **worktree 隔离**：baseRef（fresh/head 分支策略）、symlinkDirectories、sparsePaths；**bgIsolation=worktree（默认）块主 checkout 的 Edit/Write 直到 EnterWorktree；none 让后台作业直接改工作副本**。
- **defaultMode 安全**：v2.1.142 起 **auto 被 project/local 设置忽略**（仓库不能自授 auto 模式）；disableBypassPermissionsMode 禁 bypassPermissions。
- **提升层**：工具 / 可复用 Skill（agent 权限与沙箱治理）。

### B2：skillsmp p54 精选：执行纠偏 / AI 味量化 / 引用与文档一致性验证 / 视觉设计工程（来源：skillsmp.com/skills/page/54，2026-09-25 实拉）
- **pua（tanweai/pua ★19,666）**：try-harder 生产力教练——受挫/重复失败/质量投诉/被动行为时触发（"try harder/别摆烂/证据呢/没跑测试别说完成/验收/闭环/自嗨/老板体感"）；**calm first-attempt requests 不触发**——"没证据别说完成"执行纠偏。
- **aidetect（tance-mang ★58）**：**中文网文 AI 味量化——AI 味指数 0-10 + 八项指标实测（比喻密度/连续同句式/句长波动/段落分布/高频情绪词重复/极端词堆砌）+ 扣分定位清单（问题具体在第几句）**——AI 味可测量可定位。
- **reference-verify（brycewang-stanford ★3,709）**：**学术参考文献验证——每条 BibTeX 是否真实、文内引用是否匹配被引论文实际内容、产出结构化验证报告**（与 doubao-reference-audit 同族）。
- **cross-documentation-verification（onshoreoutsourcing ★0）**：跨文档一致性验证（epics/features/waves/ADRs/architecture docs）——检测冲突/缺口/重复/错位；**documentation-sync-checker** 验证版本一致性/内部链接/文档漂移。
- **web-design-engineer（mornikar ★2）**：**反 AI 陈词滥调规则（封禁过度使用的 AI 设计模式）+ 设计系统声明（编码前先阐述色彩/排版/间距/动效）+ oklch 色彩理论（感知均匀颜色推导，替代随机 hex）+ 6 套精选字体配色 + 占位符哲学（诚实标记而非拙劣伪造）+ 六步工作流**。
- **project-overview（HHU3637kr ★145）**：整理项目全链路结构与流程，**生成单文件 HTML 总览（tab 分模块/字段级折叠明细/记录 git 版本）**。
- **novel-video-pipeline（woanderingboy ★1）**：小说/网文/漫画改编 AI 漫剧**四站式流水线（S1 改编剧本→S2 视觉资产→S3 分镜提示词→S4 音频）+ 站间门禁校验**；S1 故事结构库/情绪引擎、S2 公共领域负向词 IP 防火墙、S4 CC0 音频清单。
- **提升层**：工作流 / 可复用 Skill。

### B3：OpenClaw channels 官方：30+ 通道矩阵 / Telegram 最快起步 / Group join introductions 安全机制（来源：docs.openclaw.ai/channels，2026-09-25 实拉）
- **通道矩阵**：bundled（Telegram/A2A/Reef/WebChat）+ official plugin（Discord/Feishu/Slack/Signal/Matrix/Teams/WhatsApp/iMessage 等 20+）+ external（WeChat/WeCom/Yuanbao/Zalo ClawBot）；**Telegram 最快起步（bot token 无插件安装）**；WhatsApp 需 QR 配对且存更多状态。
- **Group join introductions 机制（安全防注入）**：机器人加入群组时发布一次房间专属介绍——**读最多 100 条近期消息+房间元数据→整体截断到 12,000 字符（先丢最旧）**；**90 天 durable claim 防重连/重启重复介绍**；Discord 忽略 5 分钟前 server 事件防重启批量介绍。
- **介绍轮安全隔离**：房间标题/主题/置顶/历史均为第三方内容→**包裹为 untrusted external content，介绍轮无任何工具可用**（房间内嵌指令无法触达工具）；**60 秒上限、不在 DM 运行、不绕过通道访问策略**。
- **bot loop protection**：接受 bot 消息的通道可防 bot 互回死循环；ambient room events 让未提及的闲聊成为安静上下文。
- **提升层**：工作流（多通道 agent 接入与安全边界）。

### B4：deepseek-plugin.org 插件目录 Top10：四层记忆 / 项目记忆 / spec-driven 环 / 推理模式路由（来源：deepseek-plugin.org 根页，2026-09-25 实拉）
- **MemOS（MemTensor ★10,843）**：**本地四层长期记忆 L1 trajectory / L2 strategy / L3 world model / skills**，**每用户 turn 自动检索**，注册 6 个记忆工具——与 wb-context-compressor 记忆分层同构增量。
- **Hindsight（vectorize-io ★20,431）**：长期项目记忆——**每 session 自动回忆知识页与上下文，会话自动保存，每仓库共享记忆库**。
- **Ouroboros（Q00 ★5,588）**：**spec-driven AI 工作流作为 MCP 工具（Interview→Seed→Execute→Evaluate→Evolution 五阶段环）**，uvx 启动零安装。
- **dsh-routing-suite（yjh051108 ★6,979）**：injector + router-standard kit——**task-aware 推理模式路由（P1-P23 档）**。
- **dsh-weknora（Tencent ★21,008）**：原始文档→可查询 RAG + 自主推理 agent + **自维护 Wiki**。
- 附：deeplearning.ai Voice for AI Agents 三模式（embedded voice / voice layered on existing agents / voice as callable tool）。
- **提升层**：工具 / 工作流（记忆与路由）。

## 判重说明
- B1 → settings 权限与沙箱层，与 A1 同页增量（A1 落作用域/优先级/drop-in，B1 落权限求值/沙箱/技能预算/worktree），增量独立落地。
- B2 → skillsmp p54 精选，全新，落。
- B3 → OpenClaw channels 官方+入群介绍安全机制，全新，落。
- B4 → deepseek-plugin.org Top10，全新，落。
- 未落：github trending paperclip（同日重复）、n8n docs 根页（与 r214-B 重复）、dify Deep Research 详细版（与 A4 重复）、InfraNodus（与 r213-A 重叠）、死链 1 次计数。
