# r256-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | 腾讯 SkillHub（首拉） | ✓ | 2026-03-11 腾讯推出：基于 OpenClaw 官方开源生态（ClawHub）的本土化高速镜像平台，兼容官方全量技能生态不改开源内容；收录 1.3万+→2026-06 8万+ Skills；国内高速镜像秒速安装；三线并行安全审核；首发 TRACE 评测体系识别高质量 Skill；支持 WorkBuddy/QClaw/ima 等腾讯 AI 产品；Skills 广场三类：内置（腾讯文档/IMA/QQ 浏览器/腾讯乐享生态技能，平台安全审核+质量验证，开箱即用）/企业共享（审批后复用）/自定义；云文档技能覆盖写周报/合同发票/网页剪藏/接龙转表格/PDF 拆分/AI PPT；防骗大师.Skill 42.8 万使用；DeepSeek Harness Plugin 广场（9.7千 GitHub MIT 插件，dsh-market 4.0千星） |
| 2 | 阿里虾小宝（首拉） | ✓ | JVS Claw（2026-03-13 阿里云"一键养虾"平台，基于 OpenClaw）：手机三步创建"龙虾"机器人，云端/本地双模式，iOS/Android/网页/Pad 多端；万能 skill 自进化成长型技能体系——"如果没有这个技能，请搜索并创建"，Agent 自主寻找适配技能完成任务，越用越聪明；SkillAtlas 商店（skillhub.wanuai.cn 91,000+ 技能）：复制指令"请根据 https://maas-skill-hub-cli.oss-cn-hangzhou.aliyuncs.com/skillhub.md 安装 SkillAtlas 商店"发给 Agent 安装；自定义审核（技能合规可用由用户把关）；AgentRun 养虾专题技能：agent-browser（网页访问信息提取）/self-improvement（持续优化对话质量）/find-agentrun-skills（发现推荐技能）/fc-vpc-proxy（函数计算 FC 代理访问 VPC 内资源）/searxng（默认搜索引擎）；生意管家"龙虾版"电商 Agent 团队（模组化代理整合淘宝天猫核心能力+本地档案/CRM 连接） |
| 3 | 智谱 AgentMore（首拉） | ✓ | AgentMore=智谱清言 AI 智能体协作平台（2026-05-25 发布）：多 Agent 协作+技能市场扩展+任务执行与工作流编排；Skills 广场整合官方严选/Skill Hub/开源社区三模块，一键零 Token 安装；核心定位给 Agent 一键配置现成专业技能免从零调教；GLM-5-Turbo 从训练阶段针对龙虾任务专项优化：Tool Calling（强化外部工具与各类 Skills 调用不掉链子）/Instruction Following（复杂多层长链路指令拆解，识别目标规划步骤多智能体协同）/定时与持续性任务（时间维度理解长任务不中断）/高吞吐长链路执行；GLM Coding Plan 天猫上架（个人 Lite/Pro/Max+团队标准席位，基于 GLM-5.3，支持 ZCode/Claude Code/Codex 等 20+ Agent） |
| 4 | agentskills.io（首拉） | ✓ | 开放标准时间线：2025-12-18 Anthropic 发布 Agent Skills 规格于 agentskills.io 并由 Agentic AI Foundation 托管；2026-01 MCP 捐赠 Linux Foundation Agentic AI Foundation；2026-03 agentskills.io 成为生态公认开放标准；2026-05 35+ 平台支持+agentskill.sh 技能数突破 110,000；GitHub 技能数量从几百暴增到 2,600+；getsentry 交付 480+ 技能集合；40+ 客户端含 Claude Code/Cursor/GitHub Copilot/VS Code/OpenAI Codex/Gemini CLI/Goose/Databricks/Snowflake；规格刻意最小：文件夹+SKILL.md 两个必填 frontmatter（name/description）+可选 scripts/references/assets；可移植性是关键——一个 Skill 跨兼容平台无需修改；发布 48 小时内微软集成 VS Code、OpenAI 在 ChatGPT/Codex CLI 添加结构相同架构；Atlassian/Figma/Canva/Stripe/Notion/Zapier 推出合作伙伴 Skills |
| 5 | Hugging Face（Skills 面） | ✓ | huggingface/skills 仓库 7,374 stars（单周 +5,938）；HF Skills 框架：agent 与 HF 生态交互的可执行机器可读定义——dataset curation/model training/performance evaluation；从 brittle raw code generation→structured tool execution；声明式 agent 化（declarative, agent-ready）；工具集：查询 HF Hub 模型指标/从 model cards 提取评估分数/跨架构比较选最佳模型；Remote Training Execution：AutoTrain/HF Training Cluster 触发微调作业；技能示例：hugging-face-paper-publisher（发布管理论文）/hugging-face-tool-builder（可复用 API 脚本）/hugging-face-trackio（Trackio 训练实验追踪+实时 dashboard HF Spaces）；hf CLI 技能（下载上传管理 models/datasets/spaces/buckets/repos/papers/jobs）；公开注册表 180,000+ distinct skills（Skills.sh/Claude Registry/HF Skills Hub/GitHub awesome-agent-skills） |
| 6 | n8n（credentials/HTTP 面） | ✓ | HTTP Request node：Predefined Credential Type 优先（内置+社区节点支持平台，token 存储+OAuth 自动刷新免配 endpoint）；Generic credentials 仅平台不支持才用，八种认证：Basic/Custom/Digest/Header/OAuth1/OAuth2/Query auth；表达式选凭据：credential 字段支持表达式运行时动态解析（undefined 属正常）；多租户模式：URL/Header 从 Webhook 输入取（spreadsheetId/googleToken）；环境变量直传 header：{{ $env.MY_API_KEY }}（免 saved credential 权限错误）+retry on fail 处理网络断 |
| 7 | Anthropic（prompt caching 面） | ✓ | 两种启用方式：Automatic caching（顶层加 cache_control，系统自动把缓存断点放最后可缓存块并随对话增长前移，适合多轮对话）；Explicit cache breakpoints（块级显式断点，缓存不同变更频率的区块）；最佳实践：缓存稳定可复用内容（系统指令/背景信息/大上下文/常用工具定义）、缓存内容放 prompt 开头、断点放在保持不变的最后一个块；2026 默认：5 分钟 TTL ephemeral 缓存/1 小时 TTL 高写入成本；缓存写 1.25x 输入价（5 分钟档）/2x（1 小时档）；缓存读约 10% 输入价；最小可缓存块 1,024 tokens（Opus 4.7/Sonnet）；盈亏线：前缀 5 分钟内复用 1-2 次以上才缓存（长 system prompt/skills >2k tokens/RAG 稳定文档/多轮历史） |
| 8 | OpenClaw（sandbox 安全面） | ✓ | 信任边界：docker 容器隔离沙箱子 agent（看不到真实文件/.env/网络外服务）；sandbox mode：off（全 host）/non-main（仅非主会话沙箱，群/频道常见"意外"）/all；bind mount 双重校验（normalized path+最深存在祖先二次解析），symlink 绕过失败关闭；凭据与系统路径 deny-list 不可禁用（dangerouslyAllowExternalBindSources 仅放宽 allowed-roots 检查）；tools.elevated 显式逃生路线：sandbox 外执行 exec（gateway/node），/exec 指令仅授权发件人且按会话持久；per-agent sandbox 配置（v2026.1.6 起每个 agent 独立 sandbox+tool 限制）；Doctor 诊断：sandbox tool policy 隐藏 MCP server 工具告警+workspace repair（stale config/plaintext secrets/invalid provider） |
| 9 | WaytoAGI（教程/知识库面） | ✓ | 社区规模：覆盖 1000万+学习者，知识库访问量超亿次（8000 万+），联动 180 所高校+100+企业，600+ 场活动；10000+ 篇内容可通过飞书知识问答检索；AI 工作流学习路径：基础（图像生成原理+提示词基本结构）→实践（config UI 搭工作流+复刻他人优秀工作流研究吃透替换模型）→提升（参加提示词比赛+学习节点功能）；Code 节点：IDE 底部尝试 AI 输入自然语言自动生成代码；AI 助手搭建四步（百炼大模型应用 API→函数计算搭网站→几行代码引入 AI 助手→加私有知识） |
| 10 | deepseek-plugin（深化面） | ✓ | dsh-secure-audit（0.2.10）：只读安全合规插件，11 项只读检查（config/sessions/plugins/paths/network/env/host）映射 OWASP LLM+Agentic Top 10，带 quick 模式；dsh.so 插件市场：通过 GitHub API 逐条验证+自动化安全扫描+沙盒安装实测"绝无虚报"；dsh-plugin-audit：静态审计插件目录（source/package.json/cordis.patch.yml）返回 permission profile card（Risk: REVIEW 人工评审建议）；dsh-defend：确定性规则库（不调模型），捕获移植词汇+宽容变体，基准 27/28 防回归；DSH 安全护栏（第三方实测）：fail-closed（无沙箱后端 Bash 直接拒绝+精确错误信息）/审批必须写 justification 否则拒绝/三档权限（Read Only/Workspace Write/Full access，切 Full 过风险确认）/防循环（连续重复调用同一工具自动注入提醒） |

## 判重基准
双键检索：SkillHub（r246B 本土镜像——本次 TRACE 评测/三类技能/插件广场增量≥40%）；虾小宝/AgentMore/agentskills.io（首拉）；HF Skills（r251C 标准化——具体工具集增量 40% 边缘）；n8n credentials（r233B 凭证分层/r248A webhook 分层——HTTP 认证选型+动态凭据增量≥40%）；Anthropic caching（r243C Caching 成本模型——automatic 模式+cache-busters+前缀纪律增量≥40%）；OpenClaw sandbox（r243B MCP 安全/r254-C 审批/r255-A automation——沙箱信任边界面新）；DSH（r225A 全插件化/r236C 注入/r248A 供应链/r249B 插件生态——安全审计工具链+护栏增量≥40%）；WaytoAGI（r255-A Hermes——知识库问答信息弱）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① OpenClaw 沙箱信任边界 | sandbox mode 三态+双重 bind mount 校验+deny-list 不可禁用 | 工具 | wb-execute-discipline |
| ② Anthropic prompt caching 架构纪律 | automatic vs 显式断点+cache-busters+前缀动态尾+盈亏线 | 工作流 | wb-execute-discipline |
| ③ n8n 认证选型与动态凭据 | Predefined 优先+Generic 八种+表达式凭据+多租户 | 工具 | wb-execute-discipline |
| ④ DSH 插件安全供应链 | 审计工具链+fail-closed 护栏+三档权限 | 工具 | wb-execute-discipline |
| ⑤ Agent Skills 生态治理与规模 | agentskills.io 时间线+Agentic AI Foundation+110,000 技能 | 可复用 Skill | wb-execute-discipline |

## 复核
- 五独点均有当日实拉来源，无编造；①②③④与旧点重叠均≥40% 独有增量（合并保留增量）。
- 备选未落：腾讯 SkillHub TRACE/三类技能（增量明确后续判）、智谱 GLM 龙虾专项选型、虾小宝万能 skill 国内实例、HF 声明式 skills、WaytoAGI 知识库。
- 垃圾：本轮未产生临时文件。
