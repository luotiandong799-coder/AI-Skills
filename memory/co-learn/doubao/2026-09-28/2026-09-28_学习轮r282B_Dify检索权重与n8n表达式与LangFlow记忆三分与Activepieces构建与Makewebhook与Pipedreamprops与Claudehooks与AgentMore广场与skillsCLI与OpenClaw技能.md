# r282B 学习轮留痕（2026-09-28）

## 信源实拉清单（10 站全量逐站；查询词与 r282A 十词 + r281A/B/C 三十词 + r280 三十词 + r279 三十词 + r278 三十词 + r277 三十词错开）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（混合检索权重） | OK | Hybrid Search 并行全文+向量+重排；**Weight Settings 可免配置 Rerank API（语义/关键词权重自调：Semantic=1,Keyword=0 纯向量；反之为纯关键词）**；**两级检索设置=KB 级初始池+节点级再排序（两层连续过滤器）**；JSON 配置示例（retrieval_mode:hybrid, keyword_weight:0.4, vector_weight:0.6, top_k:5）；TopK/Score Threshold；Rerank 第三方模型（gte-rerank/cohere-rerank） |
| 2 | n8n（表达式/JMESPath） | OK | 表达式={{JS 风格}} 运行时求值；$json=当前节点输入；**$jmespath(obj, expr) 查询嵌套 JSON（过滤数组/选字段/展平，如 [*].name）**；每字段两模式（Fixed 固定/Expression 表达式）；**复杂逻辑别写表达式（avoid reduce 等重逻辑，放 Code 节点）**；交互式教程模板（Source Data 节点+系列 lesson） |
| 3 | LangFlow（记忆三分） | OK | **三类记忆明确区分：Memory bases（向量化长期聊天历史→语义相似度检索最相关上下文）/ Message History（时间序检索 messages 表）/ Knowledge base（手动填充）**；聊天记忆 vs 向量库记忆（前者专用存储检索聊天消息，后者语义搜索文本块）；Agent 组件内建 chat memory 默认启用（Langflow storage 够用）；Message History 可接 Mem0/Redis；1.12 起大多数 vector store bundles 不在默认安装（需另装，知识库仍用本地 Chroma） |
| 4 | Activepieces（agent 构建流程） | OK | **六步构建：命名+描述→instructions→Add Tool（From Piece 320+ 集成 / From Flow 把流程转成工具）**；**AI agent 开发五步框架：定义思考方式→建持久记忆→接工具→设执行框架→加护栏与测试**；Approval points（碰钱/客户/生产环境的步骤加审批门禁，其余放行）；自然语言描述任务（不用 prompt engineering）；Router 分支按分数路由（score>4 合格路径）；企业场景：加权评分框架+Perplexity 结构化数据+HubSpot 更新 |
| 5 | Make（webhook 最佳实践） | OK | **scheduled webhook 排队机制（请求累积队列，按 Maximum number of results 每周期处理 N 个，默认 2）**；**数据字段定义（advanced settings：字段名/类型/必填标记→只处理完整正确数据）**；安全清单（HTTPS、secret token header 比较、HMAC 签名、拒绝非常用 HTTP 方法、幂等性）；bundle 概念（收到字段打包）；webhook 响应用法（第三方→Make→回 webhook）；webhook-triggered AI agent（5 分钟搭建） |
| 6 | Pipedream（props 抽象） | OK | **props=代码步字段（从 workflow builder 传参，让代码步跨 workflow 复用、不改代码）**；**props 仅 Node.js 代码步支持（Python/Bash/Go 无）**；app prop（type:'app', app:'slack'）自动接线连接账号；**代码步发布为可复用 action（需 version/name/key/type 四属性）**；共享代码跨 workflow；Python 步用 pd.steps 访问 |
| 7 | Anthropic（Claude Code hooks 三 cadence） | OK | **hooks 三节奏：per session（SessionStart/SessionEnd）/ per turn（UserPromptSubmit/Stop/StopFailure）/ per tool call（PreToolUse/PostToolUse 等）**；**PreCompact（压缩前备份转录、保留重要决策）**；**PermissionRequest（弹权限框前：自动批准测试命令、阻止敏感文件）**；**prompt-based hooks（Stop 智能判断是否继续、SubagentStop 评估子代理完成、UserPromptSubmit LLM 验证用户提示、PreToolUse 上下文感知权限决策）**；SessionStart 注入 git status/TODO 列表 |
| 8 | 智谱 AgentMore（技能广场） | OK | **Skills 技能广场三大模块：内置推荐/Skillhub 7.4万+免费技能/开源社区；一键零 Token 安装；可卸载管理**；大厂独家技能包（微信读书/美团优惠券）；智能体广场=模版库（画布+Prompt 一键复制）；**36氪：腾讯/阿里/字节 skill 商店混战（火山 findskill 企业级 clawhub+github 多源、扣子 skill 售卖）；美团 xia345 导航 20+Agent 7000+Skill**；智谱官方 Skills 上 ClawHub（图像 captioning/视觉 grounding/文档写作/简历筛选/提示词生成 + GLM-OCR 文字/表格/手写/公式识别） |
| 9 | skills.sh（CLI 细节） | OK | **skills CLI 开源（github.com/vercel-labs/skills，13.1k★ MIT，npx 免全局安装）**；npx skills add owner/repo 安装、npx skills find 发现；**多 agent 单命令安装（localskills：localskills install acme/api-conventions --target cursor claude windsurf）**；hermes skills 命令链（browse/search --source skills-sh/inspect 安装前预览/install）；支持 40-51 个 agent（symlink/copy SKILL.md 到 agent 目录）；**技能版本化+回滚+可见性（public/private/unlisted）+下载分析** |
| 10 | OpenClaw（技能最佳实践） | OK | **技能结构三原则：激活条件具体（"当用户要 standup"优于模糊）、限制引用工具（只用 git 就别引导浏览网页）、指令精简（每个技能都加 context token，500 词 SKILL.md 即可）**；**安装前 clawhub inspect '<slug>' 检查权限和代码**；技能安全清单（最小权限/不硬编码密钥/沙箱跑实验技能/审输出后批准破坏性操作/依赖锁定/版本语义化/错误处理优雅/文档化配置/含测试/尊重限流）；**插件可自带技能（openclaw.plugin.json 的 skills 目录，浏览器插件带 browser-automation 技能；与 extraDirs 同级低优先级，同名 bundled/managed/agent/workspace 覆盖）**；私有技能不进 ClawHub |

## 判重（双键检索，增量判定）
- Dify 混合检索（r278A 用过混合检索）→ 权重免 Rerank+两级检索+JSON 配置为独有增量 → **增量合并**
- n8n 表达式（r271A 用过表达式）→ JMESPath+两模式+复杂逻辑别进表达式为独有增量 → **增量合并**
- LangFlow 记忆（r271B 用过记忆）→ 三类记忆区分+1.12 安装变化为独有增量 → **增量合并**
- Activepieces agent 构建（r282A 用例/r281B 构建）→ 六步流程+五步框架+Approval 门禁为新面 → **新面**
- Make webhook（r268B 信号暂停/r279A webhook 触发）→ 排队机制+字段验证+安全清单为新面 → **新面**
- Pipedream props（r273A Connect/r282A 生成）→ props 抽象+action 发布为新面 → **新面**
- Claude hooks（r280B 用过 hooks）→ 三 cadence+PreCompact+prompt-based hooks 为独有增量 → **增量合并**
- AgentMore（r267B 扩展机制）→ 技能广场商店生态+36氪战局+官方 Skills 为独有增量 → **增量合并**
- skills.sh（r281C 目录与 CLI）→ CLI 开源+find+多 target+版本化可见性为独有增量 → **增量合并**
- OpenClaw 技能（多轮 OpenClaw）→ 三原则+inspect+安全清单+插件自带技能为独有增量 → **增量合并**

## 独点落地（10 个）
| # | 独有点 | 提升层 |
|---|---|---|
| 1 | Dify 混合检索权重与两级检索 | 工具 |
| 2 | n8n 表达式与 JMESPath 边界 | 工具 |
| 3 | LangFlow 三类记忆区分 | 可复用 Skill |
| 4 | Activepieces agent 构建与审批门禁 | 工作流 |
| 5 | Make webhook 排队与安全清单 | 工具 |
| 6 | Pipedream props 抽象与 action 化 | 工具 |
| 7 | Claude hooks 三 cadence 与关键钩子 | 可复用 Skill |
| 8 | AgentMore 技能广场生态 | 工具 |
| 9 | skills.sh CLI 与多 agent 安装 | 可复用 Skill |
| 10 | OpenClaw 技能最佳实践与安全 | 可复用 Skill |

## 复核
十独点均有当日实拉来源；六点增量合并（均含≥40% 独有增量）、四点新面；无纯重复。版本建议 3.63.0。