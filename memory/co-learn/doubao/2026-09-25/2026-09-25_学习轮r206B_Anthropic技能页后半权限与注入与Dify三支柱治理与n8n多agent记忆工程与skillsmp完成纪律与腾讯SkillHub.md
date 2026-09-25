# 学习轮 r206-B：Anthropic技能页后半权限与注入与Dify三支柱治理与n8n多agent记忆工程与skillsmp完成纪律与腾讯SkillHub（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.anthropic.com skills 页续读（3994-7994/8135） | OK（preloaded skills/permission 语法/ultrathink/分发范围） |
| 2 | dify.ai/blog/introducing-new-dify-agent（3995/23043） | OK（Build/Manage/Track 三支柱） |
| 3 | skillsmp.com/skills/page/24（#2301-2338） | OK（unlazy/search-first/CEO review 等） |
| 4 | deepseek-plugin.org/plugins?page=1 | fetch error（死链，第 4 次） |
| 5 | blog.n8n.io production-ai-playbook 续读（7049-10774/19237） | OK（session ID 三模式/安全出口/稳定信封） |
| 6 | docs.pipedream.com/components/api/（3975/11838） | OK（secret prop/propDefinition/async options） |
| 7 | docs.openclaw.ai/capabilities/skills | 死链 |
| 8 | make.com/en/help/functions/data-structures | fetch error（死链） |
| 9 | docs.openclaw.ai/capabilities | 死链 |
| 10 | general_search 腾讯 SkillHub/虾小宝/AgentMore | OK（三线审核/TRACE/8万+ 镜像） |

## 独点（5 个）
### V1：Anthropic skills 页后半：preloaded skills 注入模式与 permission 语法与 ultrathink（来源：docs.anthropic.com skills 页 3994-7994 段 2026-09-25，r206-A U1 的后半增量）
- **subagents with preloaded skills**：常规会话 skill description 进上下文、全量内容仅激活时加载；**带 skills 字段的子代理在启动时全量注入**——两种加载模式分工。
- **permission 语法**：`Skill(name)` 精确 / `Skill(name *)` 前缀匹配（`Skill(review-pr *)`）允许或拒绝；deny `Skill` 工具=禁用全部技能；`Skill(deploy *)` 拒绝。
- **user-invocable 只控菜单可见性，不控 Skill 工具访问**——要阻断程序化调用用 disable-model-invocation。
- **ultrathink**：skill 内容含该词即启用 extended thinking。
- **skill 三分发范围**：project（commit 版本控制）/ plugin（skills/ 目录）/ managed（组织级部署）。
- **troubleshooting 三问**：不触发→description 含自然关键词+确认出现在 What skills are available+改措辞；过触发→description 更具体或 disable；看不到→description 预算（2% 动态）。
- 判据：**子代理预载技能=启动即全量**；权限用规则语法枚举而非对话约束。
- **提升层**：可复用 Skill。

### V2：Dify New Agent Build/Manage/Track 三支柱：变更治理与白盒追踪（来源：dify.ai/blog/introducing-new-dify-agent 2026-09-25，r206-A U3 的管理/追踪增量）
- **Build**：Configure（目标清晰走手动：模型/提示/技能/文件/工具）vs Build mode（目标清晰路径演进：AI 引导 setup，变更分阶段供 review）。
- **Build Draft**：AI 改动先进 draft，面板展示变更，**keep/discard 选择性采纳**；agent 自维护 **build_note.md 运行记录**（已配置什么/还需注意什么）。
- **Manage**：**single source of truth**（model/prompt/skills/files/tools 一处维护）跨多 workflow/多 app 复用——以前每个 agent 绑死在建它的 workflow，复用要重建 prompt/tools。
- **Track**：单次运行追踪 + 长期监控白盒可观测——run 出问题时知道发生了什么。
- **Agent 不止是 prompt**：prompt 塞业务规则/参考材料/工具指令难维护——结构化为 skills/files/tools。
- 判据：**可复用 agent 需要单一事实源+变更可审+运行可溯**三件套，缺一不可。
- **提升层**：工具 / 工作流。

### V3：n8n 多 agent 记忆工程：key facts 不靠记忆 + Session ID 三模式 + 安全出口（来源：blog.n8n.io production-ai-playbook 7049+ 段 2026-09-25，与 r205-B 记忆拓扑/r205-A R1 互补）
- **Store key facts outside of memory**：客户等级/账户状态/活跃订阅是"绝不能忘"的信息——**不靠记忆保存，每轮开始从系统拉取新鲜数据注入 system prompt**（记忆会出窗，系统状态不会）。
- **Session ID 三模式图**：shared（orchestrator+specialist 同 session ID 共享历史，交接保连续）/ isolated（各自独立历史，orchestrator 通过 tool call 显式传相关上下文，防域间泄漏）/ user-based（user ID 作 session ID 跨 run 持久）。
- **Scope context aggressively**：billing specialist 不需要看三步前的技术排查——只传相关的，别把完整历史给每个 agent。
- **summary memory for long conversations**：窗口超限→摘要+近期消息。
- **revisionCount+maxRevisions 安全出口 + 稳定响应信封**：质量门不过→回写作→达 maxRevisions 退出；pass 与 max-revisions 两种结局**同形状信封**（hitMaxRevisions:true/qualityPassed:false），下游消费者依赖稳定契约。
- 判据：**不可忘的走数据拉取，可遗忘的走记忆**；循环必须配安全出口；结局信封必须同构。
- **提升层**：工作流。

### V4：skillsmp 生态：unlazy 完成纪律 + search-first 前置 + CEO review（来源：skillsmp.com/skills/page/24 2026-09-25，与 r206-A U5 superpowers 闭环互补）
- **unlazy（完成纪律）**：长/多部分任务执行前**写验收门（acceptance gates）**、Depth Tree 拆解、跑批准检查、**报告前重新验证证据**——"不要停在半完成"。
- **search-first**：写自定义代码前先搜现有工具/库/模式——把"先搜再实现"系统化为 workflow。
- **gstack-openclaw-ceo-review**：挑战方案/戳洞/想更大/决定扩或缩——review 视角独立成技能。
- **content-hash-cache-pattern**：SHA-256 内容哈希缓存昂贵文件处理——路径无关/自动失效/服务层分离。
- 判据：**验收门先于执行写**；报告结论前重验证据；写码前先搜。
- **提升层**：可复用 Skill / 工作流。

### V5：腾讯 SkillHub 与国内大厂 Skill 商店模式（来源：general_search skillhub.cloud.tencent.com/腾讯云 techpedia/钛媒体 2026-09-25）
- **腾讯 SkillHub**（2026-03-11 上线，腾讯云 Lighthouse 团队）：专为中国用户优化的 AI Skills 社区，OpenClaw 生态本土化配套，**不改 OpenClaw 官方开源内容**；收录 8万+ Skills；**国内高速镜像秒速安装**；**三线并行安全审核机制**；支持 WorkBuddy/QClaw/ima；**首发 TRACE 评测体系**识别高质量技能；精选 50 最值得装榜单。
- **阿里虾小宝**：JVS Claw Agent 内置 Skill 市场，一键同步到工具；市场免费、**调用消耗算力**（算力=云业务收入）。
- **字节双线**：火山引擎 Find Skill（企业向，整合 ClawHub/GitHub 多源）；扣子技能商店。
- **腾讯 WorkBuddy 开放平台**：统一 AI 智能体底座，首批超百家生态伙伴，支持智能眼镜/录音卡片/智能耳机硬件接入。
- 判据：**Skill 商店三模式=引流/算力/企业多源**；镜像+审核+评测是本土化三件套。
- **提升层**：工具。

## 判重说明
- V1 → r206-A U1 同源页面前后半不同内容（权限语法/预载注入/ultrathink/分发范围为独有增量），落。
- V2 → r206-A U3 互补（构建 vs 治理追踪），落。
- V3 → r205-B S1（记忆存储三选）与 r205-A R1（研究-写作-评审）互补增量（key facts 拉取/三模式图/安全出口信封），落。
- V4 → r206-A U5 互补（闭环 vs 完成纪律+前置搜索），落。
- V5 → 新（SkillHub 详情首次实拉），落。
- 未落：pipedream component API（弱于既有工具知识）、deepseek-plugin（死链）、openclaw capabilities（死链）、make data-structures（死链）。
