# r263C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（知识库权限面） | ✓ | 三大作用域边界（team_member_role/app_permission/dataset_access_control）；**App Viewer 角色不自动继承团队数据集读取权**需显式 dataset:read；External Knowledge Base 连接（Dify 只有检索权不能修改外部内容）；KB Settings 权限定义可访问成员；**文档自动禁用**（Sandbox 7 天/Pro&Team 30 天不更新不检索自动禁用，可一键重新启用）；KB 设置修改仅 owner/admin/editor |
| 2 | n8n（长期记忆面） | ✓ | memory sub-nodes 保留会话历史；Chat Memory Manager 查大小/清条目；**长期记忆接外部 vector store nodes**（Qdrant/Pinecone/Supabase pgvector/MongoDB Atlas）；生产实例：Postgres 按 sessionId 记忆（chat trigger 每浏览器窗口自动生成唯一 Session ID）+Supabase 向量 top 5 chunks 严格基于文档回答防幻觉；LTM webhook 子工作流提取关键信息存 MongoDB Atlas；self-learning 每日把 memory palace 转向量入 Pinecone；每 agent 节点一个 memory sub-node |
| 3 | LangFlow（agent loop 面） | ✓ | CUGA 企业模式：planner-executor 子任务隔离防上下文过大；smart coder agent 做 tool calling+glue code 管 loops/conditionals/data transform；**大对象用 variables 存不载入 message history 防 context 膨胀，短期记忆只存 variables 摘要**；Policies 组件=自然语言业务规则转可执行守卫工具（guarded tools 工具调用前检查）；Tool 对象 registration+description；interrupt/rollback 运行时语义；工具节点包装（explicit timeout/fallback messages/logging） |
| 4 | Activepieces（流程控制面） | ✓ | Router 条件分支 native（ap_add_branch/ap_update_branch/ap_flow_structure MCP 工具；branch 插到 Otherwise 前）；Loop iterate arrays（type LOOP settings items+loopActions；loop context item/index/total）；BRANCH conditional if/else（conditions 数组 firstValue）；暂停等待人工输入（manual approval 集成进流程）；step-level execution logs（inputs/outputs/timing/errors） |
| 5 | Make（版本历史面） | ✓ | Restore and recover：version history（手动保存版本恢复）+scenario recovery（未保存变更恢复意外中断）；**Scenario Trash**（删除 30 天内一键恢复，2026-07 新功能）；Rollback error handler（停止场景+回滚支持事务模块 mysql/data store 更改，不能 undo gmail send/dropbox delete 非事务）；**Scenario run replay**（用之前 run 的 trigger data 在当前版本重放——测试/解决错误/backfill 数据无需新 trigger data，所有 plan）；Scenario history（run+change log 条目） |
| 6 | Pipedream（HTTP 响应面） | ✓ | pd.respond()（Python）/$ .respond()（Node/components）status/body/headers；**HTTP trigger 需配 "Return a custom response from your workflow"**；immediate: true 立即响应继续跑 workflow；custom_response 字段；x-pd-environment: development 头；出错条件（条件不运行/throw/body 非 string object Buffer）默认 500；source quickstart this.http.respond 回显 body |
| 7 | Claude API（prompt caching 面） | ✓ | 计费三部分：cache write（5min TTL=base×1.25/1h TTL=2×）/cache read（10%；Fable 5.1/Mythos 5.1=2.5%；Opus 5.5=5%）/regular uncached 全价；breakpoints 本身不收费；**前缀匹配**（起始字节流一致命中）；社区实测：缓存命中率 84%，支出降 ~76%（阿里云）；最佳实践：统一模板固定系统提示词+工具定义放前面；长重复系统提示词工作负载减半 |
| 8 | GitHub Actions（OIDC 面） | ✓ | id-token: write 权限；aws-actions/configure-aws-credentials 内部处理 STS；token 单 job 自动过期（~1h）；不存 secret 每次生成；**trust policy subject-claim 条件**（限制 branch/environment，绝不让 PR workflow 承担生产角色）；environment protection rules 审批；**sub 格式 2026-07-15 起 immutable**（owner ID+repo ID 防 namespace recycled——旧格式 repo:owner/repo 命名空间回收后他人可创建相同 subject）；aud=sts.amazonaws.com；Dependabot OIDC 私服认证免长期凭据 |
| 9 | Hugging Face（skills 面） | ✓ | 官方 huggingface/skills 仓库（~1.1w stars）；Agent Skills 格式（SKILL.md+YAML frontmatter 目录，兼容 Claude Code/Codex/Gemini CLI/Cursor）；安装 npx skills add https://github.com/huggingface/skills --skill hugging-face-datasets；.claude-plugin/marketplace.json 列出 skill+CI 校验 name/path 匹配；生态汇总（Skills.sh/Claude Skills Registry/HF Skills Hub/GitHub awesome-agent-skills 等 40+ 注册表 180,000+ skills）；hugging-face-datasets 用 Dataset Viewer REST API 零 Python 依赖 |
| 10 | Anthropic（compaction API 面） | ✓ | server-side compaction beta（compact-2026-01-12 beta 头）；context_management.edits 加 compact_20260112 策略；**token 阈值自动触发（最低 50K）**；返回 typed compaction content block 原生 slot 进对话；**跨 summary 边界处理 tool-use pairing**；自定义 summarization prompt 用 instructions 参数完全替换默认；SDK compaction 备选（client-side，推荐 server-side：集成复杂度低/token 计算准/无客户端限制）；compaction_control 参数 deprecated（TS/Ruby SDK 将移除）；tool_runner 方法；Zero Data Retention 兼容；Bedrock 两种机制独立 beta 头 |

## 判重基准
双键检索：Dify 知识库权限三作用域（§3596 插件安全评级卡/§6322 DSL 迁移——知识库权限面新）；LangFlow CUGA（§2239 Policies 守卫工具已落——planner-executor/大对象 variables 摘要为独有增量合并；§6153 Memory bases 管检索）；Make 版本历史与恢复（§6160 错误处理五模式管错误面——version history/Scenario Trash/run replay 为独有增量合并）；Claude prompt caching 计费（§2188 浏览器交互缓存为另一面——SKILL.md 无 caching 计费章节新面）；GitHub Actions OIDC（无 OIDC 章节新面）。备选并入记录：n8n 长期记忆向量集成（§6183 已落向量记忆——补充实例细节）、Pipedream HTTP 响应（§r260C 错误处理——响应模式增量）、HF skills 生态（§r256A HF——skills 仓库面）、Claude compaction API（§6034 server-side compaction 已落——突出 tool-use pairing/instructions 参数增量）。

## 独点落地（5 个）
| 独点 | 内容 | 提升层 |
|---|---|---|
| ① Dify 知识库权限三作用域 | 角色/应用/数据集边界+显式授权+自动禁用 | 工作流 |
| ② LangFlow CUGA 上下文治理 | planner-executor+variables 摘要+guarded tools | 工作流 |
| ③ Make 版本历史与恢复 | version history/Trash 30 天/run replay | 工作流 |
| ④ Claude prompt caching 计费 | write 1.25×/read 10%/前缀匹配命中率 | 工具 |
| ⑤ GitHub Actions OIDC | id-token write/sub immutable/PR 禁生产角色 | 工具 |

## 复核
五独点均有当日实拉来源；②③按增量判定并入保留增量；①④⑤为新面；备选并入记录。垃圾：本轮未产生临时文件。
