# 2026-09-23 学习轮 r154-C Agent 编排模式判据与多 Agent 交接契约

轮次：r154-C｜批：每时 3 轮×10 次｜实拉 10 站全量逐站

批前前置：判重基准=WB r154 批三份 + WB r153 批三份 + 自家 r153 批 13 点 + 自家 r150-152 批（含 WB wb-execute-discipline 五编排模式）。

## 一、实拉证据（URL + 原文片段，10 站）

| 站 | URL | 关键原文 |
|---|---|---|
| 多 Agent 编排 | qubittool multi-agent-orchestration + padiso + futureagi + metacto | "Supervisor: best for 3-8 agent deterministic workflows；Swarm: no single point of failure；Hierarchical: scales to 15+"；选择判据=**agent 数 × 任务动态性 × 容错需求**；各模式主风险：Supervisor=manager 瓶颈、Swarm=无限循环/成本、Pipeline=错误级联；**Maker-checker 配对（actor+verifier）削减幻觉**；Supervisor 适合"下一步依赖上一步结果、规划无法预先定死" |
| OpenClaw 记忆 | docs.openclaw.ai + openclawskills.wiki Morrow + mmntm | 三层记忆（短期上下文 RAM / 长期结构化 SQLite-JSON / 语义向量）；**pre-compaction flush：上下文溢出前先把记忆存下来**；**时态知识图谱记忆：每条事实边带 valid_at/invalid_at 时间戳**（Graphiti/Zep 模式）——"回答'当时是什么'正确、过期事实标记无效不删除" |
| agentskills.io | agentman ecosystem report + env.dev + agentskills.me | SKILL.md 标准被 40+ Agent 客户端采纳；**SkillsBench：公共技能平均得分 6.2/12 → 质量参差需 curation**；agentman 走 quality+curation 而非 volume |
| 多 Agent handoff | cognilium + channel.tel + wire + redis + futureagi | "Your agents do not share a brain, they share a mailbox — every message is a lossy compression"；**四类失败：context loss / semantic drift（角色漂移）/ error laundering（错误洗白）/ coordination tax（协调税随链长平方增长）**；"10 hops 后原始意图只剩 ~50%"；"**The fix is not a better prompt. It is a shared, typed store the agents read and write, plus hand-off contracts that make a bad message fail loudly instead of quietly**"；五类可预测退化：因果推理/隐式约束/不确定信号/时序顺序/负空间；LangGraph StateKeyMismatch：worker 返回同名全局字段空值覆盖他人数据 |
| Dify | dev.to dify agentic workflow + theplanettools + mintlify agent | **模型提供者级 fallback 链：主模型→备用→非关键路径便宜模型，不改工作流逻辑**；Agent Node=工作流内嵌 agent 作为确定性图的一步（生产多 agent 推荐方式） |
| Make | make.com blog llm-agents + how-to-guides + blog make-ai-agents | "The agent handles the reasoning step it is uniquely suited for. **Make handles the API connections, retries, formatting**"——agent 与确定性步骤同画布混排：HTTP 拉取→router 处理简单→agent 处理复杂；邮件 agent 模板：**路由按优先级分（P0 记 incident / P1 入 digest / spam 两周稳定运行后才删）** |
| 腾讯 SkillHub | cloud.tencent.com + skillhub.tencent.com + 央广网 | 实名认证发布（人脸核身）+来源认证+内容完整性校验+**SkillPay 支付链路**（分发-调用-支付打通）；7.8 万 Skill、2 个月下载 3000 万+；定位本土化/安全化/场景化 |
| 阿里虾小宝 | skillhub.wanuai.cn + aliyun agentrun FunClaw + 央广网 JVS Claw | 虾小宝=35,000+ 经安全审核技能的社区；FunClaw 养虾；JVS Claw"万能 skill"（"没有这个技能请搜索并创建"）；悟空=企业级 Agent 平台 |
| 智谱 AgentMore | novatools + prompt.cn + docs.bigmodel.cn | **群聊协作：最多 5 个 Agent 拉入群组 + 头脑风暴/任务分配双发言模式 + 共享工作区**；Skills 技能广场一键安装不消耗 Token |
| GitHub agent 生态 | startupcorners 09-23 + github.blog HydraFusion + dailyaiworld | stablyai/orca ADE（并行 agent 舰队）、BuilderIO/agent-native；**GitHub HydraFusion：多模型运行时编排（draft→critique→revise→cascade 更强模型），自动语义路由本地/云/复合模型**；Agent Fleet Manager：1000+ 并发 agent、per-agent token 预算、自适应限流 |

## 二、独点清单 + 判非重复理由（4 点，均≥40% 独有增量）

### 1. 多 Agent 编排模式选择判据 + 各模式主风险 + Maker-checker 配对（来源：QubitTool + FutureAGI + MetaCTO 2026 实拉）
选编排模式看**三个变量：agent 数 × 任务动态性 × 容错需求**（Supervisor 3-8 个确定性任务 / Swarm 开放对话 / Hierarchical 15+ 分层）；每个模式有**专属主风险**要提前防备：Supervisor=manager 合成瓶颈、Swarm=无限循环与成本失控、Pipeline=错误级联；**Maker-checker 配对**（actor 生成 + verifier 校验）是削减幻觉的结构手段。
- 判非重复：WB execute-discipline 落过"五种编排模式+共享层先建+接口契约"（怎么协作）；本点增量=**选择判据（三变量）+ 各模式主风险清单 + Maker-checker 配对模式**。增量≥40%。
- 提升层：工作流（Agent 编排）。

### 2. 多 Agent 交接四因失败与交接契约修复：交接=有损压缩（来源：Cognilium + Wire + Chanl 2026 实拉）
每次 handoff 都是**有损压缩**：四类失败——context loss（信息丢失，10 hops 后原始意图仅 ~50% 可恢复）/ semantic drift（角色漂移，第 8 hop 在解邻近问题）/ error laundering（小错误下游变真相）/ coordination tax（协调税随链长平方增长）。修复不是更好的 prompt：**共享类型化存储（agents 读写同一处）+ 交接契约让坏消息响亮失败而非安静通过**。
- 判非重复：点 1 管模式选择；本点管**交接边界失败机制与契约设计**（无既有覆盖）。增量≥70%。
- 提升层：工作流（多 Agent 交接）。

### 3. 时态记忆：事实边带 valid_at/invalid_at，过期标记无效不删除（来源：OpenClaw Morrow/Graphiti 模式 2026 实拉）
记忆事实按时间戳建模（每条边 valid_at/invalid_at）：能正确回答"**当时是什么**"；过期事实**标记无效而非删除**（可追溯）；实体去重。适合动态变化的领域（价格/配置/人事）。
- 判非重复：WB cc 记忆分层与保鲜（r152/r154）管存储分层与保鲜规则；本点管**时态维度**（时间戳事实边 + 历史时点查询）。增量≥50%。
- 提升层：工作流（记忆建模）。

### 4. Agent 与确定性逻辑的分工配比：确定性步骤处理简单路径，agent 只做推理步（来源：Make 官方 2026 实拉）
agent 不该编排全流程：**API 连接/重试/格式化/字段映射由确定性层管，agent 只负责它独有的推理步**（"The agent handles the reasoning step it is uniquely suited for"）；同画布混排——HTTP 拉取→router 处理简单分支→agent 处理需要判断的复杂分支→再回到确定性下游；Dify Agent Node 同理=工作流确定性图中的一个节点。
- 判非重复：WB"单 agent 能干的别拆"管**要不要拆**（拆的时机）；本点管**拆了之后 agent 与确定性代码怎么配比**（agent 职责边界）。增量≥40%。
- 提升层：工作流（Agent 与确定性混排）。

## 三、候选未落地点（判非重复理由）
- 模型级 fallback 链（主→备→便宜）：与 wb-execute-discipline 错误重试面相邻但属模型路由，增量<40%，不落。
- 路由按风险分级+破坏性动作延迟批准（spam 两周后删）：与 r153-C 点 3（恢复动作五语义）同域（动作决策面），增量<40%，不落。
- pre-compaction flush（压缩前存记忆）：WB r154A 已落"压缩产物持久化+撤销失效"，重叠>60%，不落。
- SkillsBench 公共技能 6.2/12：与 r153 评测面及"技能质量 curation"已覆盖，增量<40%，不落。
- SkillHub/虾小宝/AgentMore 生态事实（实名/SkillPay/群聊）：平台面事实，非个人可落地方法增量，不落。
- HydraFusion 多模型编排：GitHub 官方产品预告面，无方法增量，不落。

## 四、功能套件检查
wb-ponytail / wb-max-token-saver / wb-context-compressor：点 1/2/4 供 execute-discipline 编排面参考（模式判据/handoff 契约/agent 职责边界），点 3 供记忆建模参考。按 09-23 新规只落留痕不写技能文件。套件覆盖完整，版本不动。

## 五、垃圾清理
本轮仅 general_search，无临时文件。
