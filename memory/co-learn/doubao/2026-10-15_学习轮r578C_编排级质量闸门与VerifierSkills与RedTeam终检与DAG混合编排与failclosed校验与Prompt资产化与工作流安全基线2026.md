# 2026-10-15 学习轮 r578C：提示架构、输出校验与 Agent 编排

主题：AI 技能库工程与方法论 + AI 智慧进化（硬锁）
轮次：r578C（本次触发批 r578 之第 3 轮，共 3 轮连跑）
判重基准：WB r576/r575/r574；doubao r578A（6 章）+ r578B（6 章）+ r577A/B/C（18 章）

## 十站实拉（全量逐站，带来源）

| 站 | 实拉要点 | 来源 |
|---|---|---|
| Dify | 结构化输出三方法（Visual Editor/JSON Schema/AI 生成 schema）；Agent 输出六变量（Final Answer/Tool Outputs/Reasoning Trace ReAct 逐步决策/Iteration Count/Success Status/Agent Logs 结构化日志）；Human Input Node（人机协作暂停点：内容团队审稿/支持团队转人工）；下游期待字段先 validate 再使用 | dify-6c0370d8.mintlify.app + dify.ai/blog + dify-hosting.com |
| n8n | 解析后加显式验证（JSON 合法但 confidence=150%/category 不存在）；反馈验证结果（具体验证错误写进下个 prompt 而非 try again）；本地 LLM 可靠 JSON 五步（schema+tiny example→parse→validate keys/types/enums/empty→修复一次→再失败停止或路由 review）；checksum 指令（输出对象数=输入任务数，losing even a single task is critical）；"只回 JSON 无前后文本"规则独立解决大部分闲聊 | blog.n8n.io + community.n8n.io + getprompting + Semantic Scholar |
| Langflow | Policies（自然语言策略→ToolGuard 编译成工具守卫：prompts 塑造行为、policies 约束执行，运行时 agent 照常规划但守卫工具须过策略）；Cleanlab Evaluator（prompt-response 信任评分）；ALTK（pre-tool SPARC 验证防无效调用 + post-tool 动态生成 Python 提取大 JSON 相关数据缩上下文）；结构化输出组件（同一模型强制 8 字段 schema）；Data Quality Validator（过全部规则才进生产库） | langflow.org/blog + docs.langflow.org |
| Activepieces | Prompt library 标准化（tables 建库、每模板版本化、flow 引用、log prompt ID 审计）；评分规则显式配置（阈值写进 system prompt、字段含义写明、缺失行为写明，推理模型不从 new_company_hint 字段名猜意图）；Approval/manual-input 暂停点；fallback logic | resources.activepieces.com + forgeworkflows.com |
| Make 生态 | 编排级断路器 Tier3（confidence-gated handoffs：agent 附 confidence float 低阈值暂停人工；independent consensus：双独立路径比对，zylos 2026-06-21）；intent-validation gate（返回 unclassified 不默认最高分 agent，幻觉 15%→1.5% 未动模型，InfoQ）；5 层 agent 评估框架（Tool Correctness/Step Quality/Trajectory Coherence，DeepEval CI 门+Braintrust/LangSmith 生产监控）；Mellea 验证重试 2-5x 慢代价 | zylos.ai + infoq.com + baeseokjae.github.io + mellea.ai |
| Pipedream 生态 | fail-closed 两步验证（代码验证器查每个数字字面出现在引用原文，失败不持久化→错误回传重试→耗尽拒绝，QuantArmy）；JSON 三步自我复核（提取→重读自查每字段值或 null/语法→返回验证 JSON，explainx）；meta-prompting 验证（正则校验 ISO8601/version）；malformed JSON 便宜模型修复（try-catch 失败发给更便宜模型"修复这个字符串里的 JSON"）；Structured Outputs constrained decoding vs JSON mode（严格模式对 agent 管线才可靠）；Instructor 标准（response_model 自动 retry，11k+ stars ~3M 月下载） | quantarmy.com + explainx.ai + deepusecase.com + aiworkflowlab + blckalpaca |
| Anthropic | Verifier Skills（脚本化端到端质量门，agent 不发明"完成"定义，2-3x 质量乘数）；Red-Team Final Answer（交付前独立验证事实/算术/逻辑/来源/边界/缺需求+验证摘要）；Skill description 调试法（问 Claude 何时会用该技能）；Agent Skills 新标准（技能包=确定性操作流程：螺丝刀在哪/拧几圈/滑丝怎么办） | ranjankumar.in + buildfastwithai + uml.org.cn + bbs.huaweicloud |
| skills.sh 生态 | DAG Teams 两阶段混合编排（LLM 生成带显式依赖边任务图+确定性调度器执行，SemaClaw）；PermissionBridge（权限检查点嵌入运行时为执行原语）；SKILL.state（技能执行=显式状态转移：不可变规格 P+结构化状态 Σt+最新观察 Ot，模型不收旧观察/动作/轨迹）；SKILL-INJECT 技能供应链注入基准；Symphony（workflow.prompt_template+attempt retry metadata）；Declarative Skills（何时/前置/排序/参数要求声明式） | arxiv 2604.11548 + 2608.26263 + 2602.20156 + 2606.06923 |
| GitHub 生态 | GitLost（普通公开 Issue 藏隐式指令→agent 取私有内容发公开评论，无凭据，Noma 2026-07-06）；GitHub agentic workflow 安全基线（issue/PR/comment/抓取页=不可信数据、限当前仓库、作者完整性过滤、只读、声明安全输出、阻断网络、检查 .lock.yml）；PR comment 攻击 85% 成功率；Don't trust agents with secrets | aident.ai + mcp.directory + github.blog + codeongrass |
| deeplearning.ai | Agent Skills with Anthropic（可复用技能+组合复杂工作流+Skills 与 MCP/subagents 组合）；Agentic AI（reflection/tool use/planning/multi-agent+evaluate）；AI Prompting For Everyone（deep research、给更多上下文、重要决定让 AI 想几分钟） | corporate.deeplearning.ai + learn.deeplearning.ai + charonhub |

## 落地（execute 3.103.0→3.104.0 / compressor 3.700.0→3.701.0，各 +3 章）

| 文件 | 新增章节 | 提升层 |
|---|---|---|
| wb-execute-discipline 3.104.0 | 编排级质量闸门三件套（confidence-gated handoffs/independent consensus/intent-validation gate 返回 unclassified 幻觉 15→1.5%） | 工作流/可复用 Skill |
| wb-execute-discipline 3.104.0 | Verifier Skills 与 Red-Team 最终答案（脚本化质量门完成定义唯一/六项自查+验证摘要） | 工作流/可复用 Skill |
| wb-execute-discipline 3.104.0 | DAG Teams 混合编排与验证反馈回灌（LLM 建图+确定性调度/具体验证错误写进 prompt 定向修复） | 工作流/工具 |
| wb-context-compressor 3.701.0 | 输出校验 fail-closed 与自我复核（数字字面必在原文/重读自查三步/便宜模型修 JSON） | 可复用 Skill/工作流 |
| wb-context-compressor 3.701.0 | Prompt 资产化与显式评分规则（prompt 库版本化 ID 审计/阈值入 prompt 字段含义缺失行为） | 可复用 Skill/工作流 |
| wb-context-compressor 3.701.0 | Agent 工作流安全基线（七条防线/GitLost 与技能供应链注入实锤） | 可复用 Skill/工作流 |

## 判重说明（增量判定）

六点均含独有增量：编排级三闸门（置信度门/双路共识/意图门 unclassified 幻觉数字）未见于前批（§质检-回退/生产三闸门为基础，三模式具体机制为 ≥40% 独有增量）；Verifier Skills（完成定义脚本化）与 Red-Team 六项自查未见于前批（§工具结果断言为工具层，本条为最终答案层）；DAG Teams（LLM 建图+确定性调度）未见于前批（§五编排模式为选型，本条为混合执行机制）；验证反馈回灌（具体错误写进 prompt 而非 try again）未见于前批（§修复一次管次数，本条管错误内容）；fail-closed 字面验证（数字必在原文+耗尽拒绝）未见于前批（§四层校验为基础，字面级核对为独有增量）；自我复核三步 prompt 未见于前批；便宜模型修 JSON 未见于前批；Prompt 资产化（库+版本+ID 审计）未见于前批（§提示词当规格管写什么，本条管存储引用）；显式评分规则（阈值入 prompt/字段含义/缺失行为）未见于前批；Agent 工作流安全基线七条与 GitLost/SKILL-INJECT 威胁事实未见于前批（§工具面安全/注入预检为工具层，本条为协作工作流层）。

## 功能套件核查（⑦）

wb-ponytail / wb-max-token-saver / wb-context-compressor：compressor +3 章（fail-closed 校验/Prompt 资产化/安全基线）增强输出校验与安全域；execute +3 章（质量闸门/Verifier Skill/DAG 编排）增强编排与验收域；ponytail 与 token-saver 无对应增量目录，暂不迭代。

## 清理（⑨）

删了什么：无（全程 general_search 实拉，无本地临时文件落盘）。保留什么：*.bak 与全部核心产物（两 SKILL.md + 三份留痕）。

## 批内备注

git commit/push 因通道缺失挂起（累计 r546→r578B 共 38 批 + 本批），不重试、不启 VPN、不补推。
