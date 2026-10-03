---
name: wb-artifact-verification
description: >-
  对"生成出来的东西"做独立验证并给出明确的成功/失败判定。当用户要求"验证生成结果""验证这个脚本/代码能不能跑""验证是否成功""帮我确认结果对不对""check 一下生成物""验证执行结果"，或给出"先生成再验证再反馈"这类任务时使用。核心是三条互相独立的证据源（独立算法 oracle / 外部已知常数 / 随机差分模糊测试）+ 故障注入（变异测试）证明验证器本身有检出能力，禁止只跑一次"看起来没问题"就宣布成功。另含"证明检查真的跑到了"：非零退出不等于检出（import 报错/构建失败也非零），须打到达标记；被测方须侧盲；判不出结果时"不确定"是一等判定，不得默认通过、不得伪造因果。另含"验证通道禁止副作用"：验证命令不得借检查之名做发布/部署/推送/外发。触发词：验证、验证结果、验证一下、能不能跑、跑通了吗、对不对、check 一下、测一下、自检、回归、真的修好了吗、看起来没问题、绿灯、都过了、测试全绿、失败注入、变异测试、假阳性、伪成功、静默测错、不确定、证不出来、证据不足、评分器、评测、基准、对照实验、抽样、覆盖率、未测、跳过、flaky、可复现、脚本化验证、退出码、超时、只读验证、别在验证里发布。、失败分类法、置信度阈值过滤误报、批量失败、单条失败、占位保配对、条数对齐、失败归属到条、来源自证端点、代理后静默失效、我看你是谁、限流失效、真实来源核验、评测续跑、只重放未完成、改了实现要全量重跑、续跑可比性、自描述元数据、写入方版本、序列化器不可用、解码失败不等于值错、绕过读取通道、过期检查在读取路径、合法 JSON 不等于合规、结构检查三态、解析失败vs字段不合规、轨迹同构三元组、完成度不能从最终答复推断、逐子任务报告、工具三判、误读返回值、恰好一次、exactly once、副作用重复、审计重复、重放重复、结算标记、合并前钩子、占用分解、扫描根、观测面盲区、分解为空、不是我的证据、盘满但分解小、换证据源、告警缺席、钩子被吞、缓存命中不触发、钩子计数翻倍、per-attempt钩子、静默失效、告警不算证据、数据飞轮、过闸才上线、来源优先级、合成数据垫底、轨迹优先、分层切分、五千好过五万、反馈版本化、跨家族互评、模式坍缩、四桶评测集、失败重放、回归还是漂移、定期重跑、置信门槛
version: "2.132.0"
agent_created: true
---

# 生成物验证（独立 oracle + 差分 + 变异测试）

三层检查清单
### A. 生成层（结构/契约）
- 存在性 + sha256 + 行数（可溯源）
- `ast.parse` 通过；`python -m py_compile` 真过编译
- 必需函数/接口齐备，**参数名与顺序**符合约定
- 反退化扫描：`TODO`/`FIXME`/`...`/空 `pass` 函数体/占位符
- 自包含性：只 import 标准库（`sys.stdlib_module_names`）
- CLI/接口契约：`--help` exit 0；非法子命令/非法入参 → 非 0 退出
- 以模块方式导入并直接调用 API（不止测 CLI）

### B. 执行层（取值正确性）
每个用例：exit code + 输出可解析 + **schema 键集合完全一致** + **值 == 至少一个 oracle** + **边界值**（0 / 1 / 空 / 负数 / 极值）+ **确定性**（同命令跑两次字节一致）。
- 差分模糊测试：随机输入 × 2 个以上独立 oracle，全量比对（记录 seed 保证可复现）
- 内部一致性：若产物输出"结果 + 过程/证据"（如编辑脚本、对齐、trace），必须**重放过程验证能推出结果**，且过程代价 == 结果值

### C. 检出能力层（变异测试）
- 至少 5 个变异体，覆盖不同失败族：**数值 off-by-one / 过滤条件弱化 / 语义静默归零 / 契约字段改名 / 边界判断翻转**
- **每个检查必须先证明自己跑到了**（到达标记，见「验证完整性三查」1）——变异体"失败"若没打标记，可能是它自己 import/构建挂了，不是被抓住
- **等价变异体必须先识别再排除**：若变异后语义与原实现完全等价（例：删掉 `sorted(key=(-count, first_pos))` 里的 tie-break —— Python dict 插入序本就等于首次出现序），它**必然逃逸**。这不是验证器失明，必须显式标注为"等价变异体，不计入检出率"，否则会误判验证失败、也会掩盖真正的盲点。
- 每个变异体**独立目录 + 原始文件名 + 随机目录名**（见坑 4 与"侧盲"），`caught = 打完到达标记后存在任一 FAIL`
- 报告里记录 `caught_by`，用于确认是"真实的取值检查"抓到它，而不是无关路径错误

<!-- 2026-09-29 r290 下沉：生成侧直连端点/完整性三查/验证通道禁副作用 3 节 → references/knowledge-base.md §早期批 -->
<!-- 2026-10-03 r396A 下沉：失败路径必须被真的跑过 全节（约 206 行）→ references/knowledge-base.md §早期批（失败路径/三界面同一内核/便利入口改值/退出码三分类/结果类别自陈不证明什么） -->
## 失败路径也必须被真的跑过（否则它等于不存在）（原文已下沉 references/knowledge-base.md §失败路径与验证通道，2026-10-03 r396A；触发词：受控失败、失败路径上次执行时间、三种界面同一内核、可脚本化验证、--tool-args-json 保真、退出码三分类、INCONCLUSIVE 单独成类、结果类别自陈「不证明什么」）
## 评测要接回优化器才叫闭环：观测 → AI 评测器 → AI 优化器 → 自动验证，Harness 是与模型、上下文并列的第三可调层（原文已下沉 references/knowledge-base.md §r349A；触发词：评测闭环、AI 评测器、AI 优化器、Harness 第三可调层、自进化引擎）
## 提交粒度是可配的，粒度越细回滚能力越弱：早提交换「部分结果不丢」，代价是出错即不可恢复（原文已下沉 references/knowledge-base.md §r294-C；触发词：逐模块提交、不能回滚、提交粒度、Commit trigger last）

全局覆盖值的存活期与传播面必须显式开启：默认只在内存里、不跨进程、重启即丢全局覆盖值的存活期与传播面必须显式开启：默认只在内存里、不跨进程、重启即丢（来源：docs.n8n.io《Credential overwrites》2026-09-29 r296-A 独立 curl 取 .md 原文 5,099B 核验；与 §2.54.0 SecretRef 禁 OAuth 互补——那条管"可变状态不跨存储分裂"，本条管"一份覆盖值到底活多久、传到哪"）（原文已下沉 references/knowledge-base.md §r325A）
无鉴权的注入端点自带「一次性门」：可被任意人调用一次，所以只允许一次无鉴权的注入端点自带「一次性门」：可被任意人调用一次，所以只允许一次（来源：docs.n8n.io《Credential overwrites》2026-09-29 r296-A 独立 curl 取 .md 原文核验；与 §2.37.0「默认值先可用、收紧从最高风险面起步」同向，本条给的是官方默认设计写法）（原文已下沉 references/knowledge-base.md §r325A）
留痕通道本身不能被多个写者共享：多进程追加同一个事件日志会交错损坏，且平台不会自动清理遗留文件留痕通道本身不能被多个写者共享：多进程追加同一个事件日志会交错损坏，且平台不会自动清理遗留文件（来源：docs.n8n.io《Stream logs to external systems》2026-09-29 r296-A 独立 curl 取 .md 原文 23,919B 核验；与 §Capability 12「留痕通道不能挂在被测对象上」互补——那条管"通道挂谁身上"，本条管"通道被几个写者共用"）（原文已下沉 references/knowledge-base.md §r325B）
## 环境变量的可见性有三个独立面：删掉不报错只返 undefined、分享只带引用不带值、第三方组件默认拿不到（来源：pipedream.com/docs/workflows/environment-variables 2026-09-29 r296-C 独立 curl 取 .md 原文 8,151B 核验；与 §Cap32 凭据只写不可读 互补——那条管"能不能读回值"，本条管"谁看得到引用、删了之后发生什么"）
- 本章已下沉 `references/knowledge-base.md` §r347C-sink（r296/r325/r338/r339 合并腾预算）。

## 审计可能是惰性生成的（「在库里」≠「已审过」），而扫描器自身的遍历顺序即是静默漏报面——两者都不产生任何警告位（来源：www.skills.sh/docs/api 136,145B + api.github.com/repos/NVIDIA/SkillSpector/issues/610 6,455B + docs.n8n.io/deploy/host-n8n/configure-n8n/security/run-security-audits.md 2,425B，2026-09-30 r323A 独立实拉；细则见 references/knowledge-base.md §r323A）

## 审核结论按版本独立成态并可滞留未终：同包内 1.0.1–1.0.4 双引擎 `queued/排队中`+`reportUrl:""` 与 1.0.0/1.0.5–1.0.7 `benign` 并存，每版独立 `versionId`；同源两接口计数须互检（`stats.versions:0` vs `/versions` 实有 8 条），展示计数不可作机检依据；官方文档声明的机器端点必须逐路径实测（skills.sh 搜索面 401、审计端点模板 404），缺陷结论时效随 PR 状态刷新（SkillSpector PR #611 仍 `open`/`merged=false`，2026-09-28 `CHANGES_REQUESTED`）；审计契约要写清「不记什么」（Reads are not recorded / 传入值 never stored / MCP 工具无读写标记⇒整段不可记），事件真源=代码 schema
（来源：api.skillhub.cn/api/v1/skills/cic/versions 4,104B + /skills/cic 2,473B + skills.sh/api/v1/skills?q=pdf 401 + gh api repos/NVIDIA/SkillSpector/pulls/611 + www.activepieces.com/docs/admin-guide/security/audit-logs/overview.md 4,069B，2026-09-30 r324A 独立实拉；细则见 references/knowledge-base.md §r324A）
## 流行度与展示序都不是质量/留存的判据：简单特征（体积、下载量）对「是否持续在架」无稳定预测力，注意力高度集中且权限声明普遍；目录展示序可能是随机洗牌，文档撤除本身是可机检的治理信号（来源：arXiv 2609.17274《After the Party v2》42,842B + agentskills.io/clients.md 25,457B + docs.n8n.io/llms.txt 286,271B，2026-09-30 r324C 独立实拉；与 §目录数字失真四形态 互补——那几条管“数字怎么失真”，本条管“该换用什么指标”；细则见 references/knowledge-base.md §r324C）


## 扫描预算耗尽只允许「降档验证」，不允许判为通过；应用层不隔离要作正面申报，不能让集成方靠缺位反证推断（来源：docs.openclaw.ai/cli/update/how-updates-run.md 84,130B + docs.langflow.org/next/security 34,323B，2026-09-30 r325A 独立 curl 实拉逐串命中；经 Qoder r357-Q-A 提名）
- 本章已下沉 `references/knowledge-base.md` §r347C-sink（r296/r325/r338/r339 合并腾预算）。

## 治理开关默认只向前生效（存量豁免），且必须点名作用域与存量规模：关掉共享/发布后「已存在的仍然有效」，2FA 强制只覆盖邮箱口令不覆盖 SSO（来源：docs.n8n.io `/deploy/host-n8n/configure-n8n/security/manage-security-policies.md` 8,773B，2026-09-30 r325B 独立 curl 实拉逐串命中，**通道更正**：Qoder 给的 `docs.n8n.io/configure-n8n/security/manage-security-policies.md` 返回「Page Not Found」壳；经 Qoder r358-Q-B 提名）
- 本章已下沉 `references/knowledge-base.md` §r347C-sink（r296/r325/r338/r339 合并腾预算）。

## 存在「权限无关的永不可见类」；特权查看须一次性按单次记录，且被拒尝试同留痕（来源：docs.n8n.io/.../redact-execution-data.md 17,934B，2026-09-30 r338C 独立实拉）
- 本章已下沉 `references/knowledge-base.md` §r347C-sink（r296/r325/r338/r339 合并腾预算）。

## 「能自动仲裁」被当成「没有冲突」：冲突检测器的能力边界必须逐类声明，未覆盖的那类会被静默覆盖（来源：docs.n8n.io `/administer/use-source-control-and-environments/push-and-pull-changes.md` 12,333B，2026-10-01 r339B 独立 curl 实拉逐串命中）
- 本章已下沉 `references/knowledge-base.md` §r347C-sink（r296/r325/r338/r339 合并腾预算）。

- **给人看的紧凑视图不构成操作依据**：本章已下沉 `references/knowledge-base.md` §r348A-sink1（r348A）。
- **终态必须由显式信号声明**：本章已下沉 `references/knowledge-base.md` §r348C-sink（r348C）。
## 资格判定三态

> 原文已下沉 `references/knowledge-base.md §r395-av2`（保持原文零删减）。
## 降档/资格判定按成因分档，且只有一类会告警：配置意图 / 角色封顶 / 后端能力矩阵缺项

> 原文已下沉 `references/knowledge-base.md §r395-av2`（保持原文零删减）。
## 投递验收必须双字段分列，且二者可同时矛盾：外发成功 ≠ 回合完成，超时=Unknown 且不重试

> 原文已下沉 `references/knowledge-base.md §r395-av2`（保持原文零删减）。
## "verified" 必须携带可定位的证据指针且由校验器机械强制：空指针行直接拒（来源：github.com/dshworks/awesome-dsh-plugins `data/plugins.json` + `scripts/validate.mjs`、skills.sh/、arXiv 2609.14079，2026-10-01 r362-Q-C 实拉）
- 判据：① `evidence` 格式 `path#key`（例 `skills/reviewer/SKILL.md#frontmatter`），校验器 `scripts/validate.mjs` 直接拒绝没有 `evidence` 的 `verified` 行。量化代价：npm 校验 298/582 包不存在、26 对条目互争同名包、2,357 条因无安装路径被拒（17,323 条 / 10,008 作者）。② 对照：`skills.sh` 榜单条目只有 `name/installs/source repo` 三元组，榜面不含任何质量或权限字段（与 arXiv SkillSecurer "流行技能 >17% 潜伏漏洞" 正交）。⇒ "已核验"最低成本实现不是加一列布尔，而是加一列可 grep 的指针 + 一个拒空指针的校验脚本。
- 提升层：可复用 Skill/工具。触发词：evidence path#key、校验器拒空指针、榜面无质量字段。

## "索引层无数值" 是可交付结论，不是抓取失败：Flowise/LangFlow 索引层零字段须逐页且如实记"不可判"（来源：docs.flowiseai.com/llms.txt、docs.langflow.org/llms.txt、docs.dify.ai/.../knowledge-request-rate-limit、list-workflow-logs，2026-10-01 r362-Q-C 实拉；承接 r326 失效四形态）
- 判据：① Flowise/LangFlow `llms.txt` 仅导航目录（Flowise 只版本号；LangFlow 只 Python 版本+端口），**零字段/零默认值/零超时分页** ⇒ 该站该面在文档层不可判，须记为"索引层无数值"而非"内容缺失"。② Dify 有数字但**无状态码**：限流 10/100/1,000 per min 三档，`limit>100` 语义是"capped at 100"=**静默截断不报错**（无旁路参数）；`page` 硬 `max 99999`。⇒ 这三家的"超限"在文档层是"截断/降档"而非"报错"，不能假设 4xx。③ 通道副产物：n8n 404 页自曝问询端点 `learning-paths.md?ask=&goal=`；但 `hosting/scaling/*` 五路径仍 404 ⇒ 该子树无直觉路径入口。
- 提升层：工具/通道。触发词：索引层无数值可判、Dify 静默截断无状态码、Flowise/LangFlow 零字段。

## 迁移开关要分「可逆」与「不可逆点」；配置存在 ≠ 配置生效，验收须查该旋钮当前版本是否仍被消费（来源：docs.n8n.io `/deploy/host-n8n/configure-n8n/durable-scheduler.md`，2026-10-01 r348A 独立 curl 实拉；经 Qoder r363-Q-A 提名）
- 原文：①`N8N_POLLER_DURABLE_CURSORS_ENABLED`：「Turning it back off doesn't undo it. Cursors stay in their table.」②`QUEUE_WORKER_MAX_STALLED_COUNT`：「Removed in n8n 2.0. Setting this has no effect.」
- 判据：① **开关要标「关回去是否回滚」**：有些迁移开关一旦打开就留下持久产物（游标表），关掉只是停止使用、不删除已产生的东西 —— 这是**不可逆点**，必须在打开前告知。⇒ 把可逆开关与不可逆点混为一类，会让「回退」变成半回退：行为退回来了，数据没退回来。② **旋钮变哑是一类静默失效**：配置项还在文档里、还被接受、甚至还被回显，但当前版本已不消费它。⇒ 验收「这个配置生效了吗」不能只看有没有这个字段，要查当前版本是否仍消费它 ——「配置存在」与「配置生效」必须分列。
- 提升层：工作流。触发词：不可逆点、关掉不回滚、游标留存、旧旋钮变哑、配置存在不等于生效、Removed 无效果。

## 单轮评测会系统性低估：只看首轮会把「多轮后能做成」误判为「做不成」；攻击轨迹库是比又一份 benchmark 更新的证据层（来源：arXiv 2609.13353 SkillAtlas，2026-10-01 r348A 独立 curl 实拉，`42.5%` / `0.770` 逐串命中）
- 原文：「42.5% of successful cases first become successful after a non-success initial round, and trajectory-grounded labels improve pre-execution guard accuracy to 0.770」（3,014 cases / 6,589 traces / 151,131 steps / 233 skills / 8 风险类）。
- 判据：① **「首轮通过率」不是能力的上界**：近半数最终成功的用例第一轮是失败的，只看首轮会把多轮修正后能做成的能力判成做不成。⇒ 评测设计要显式声明**轮次口径**（单轮 / 有界多轮 / 直到收敛），并同时报首轮与最终两个数；只报一个等于隐藏了一半事实。② **轨迹级标注能把前置守卫精度推到 0.770** —— 判「该不该拦」所需的证据在轨迹里、不在单步输出里；这也是「攻击轨迹库（公开、reviewed/redacted/searchable）比新增 benchmark 更有价值」的原因。③ 与 §评测要接回优化器 互补：那条管「评测之后谁把它改回去」，本条管「评测本身是不是测全了」。
- 提升层：可复用 Skill。触发词：单轮评测低估、42.5% 首轮失败后成功、轮次口径、首轮 vs 最终、轨迹级标注、攻击轨迹库。

## 路由器/选择器本身是一等被测对象：指标一经发布即锁定，且报告必须带可复跑的调用预算与双跑差值（来源：github.com/muratcankoylan/Agent-Skills-for-Context-Engineering README 34,923B（18,053★），2026-10-01 r348B 独立 curl 实拉，`600` / `0.920` / `0.913` / `locked metrics` / `results-published/2026-05-15` 逐串命中）
- 判据：① **被评测的不只是最终产物，还有「选谁来做」的那一层**：技能路由/选择器本身要单独端到端跑基准，否则「技能写得很好但从没被选中」不会被任何指标反映。⇒ 评测面清单里要显式列出路由器这一项，并给它自己的用例集。② **指标一经发布即锁定**：原文把 `locked metrics, durable logs, novelty gates, rollback, and human approval boundaries` 并列，且结果落在带日期的 `results-published/2026-05-15` 目录里。⇒ 不锁指标就会变成「追着指标改实现」，历史分数不可比；锁定的最小实现是**结果带日期落目录 + 指标定义随结果一起冻结**。③ **报告必须同时给调用预算与双跑差值**：600 次调用（50 skills × 4 × 3）与 top-1 `0.920` / `0.913` 两次基线同时公布。⇒ 只报一个准确率数字无法复跑、也无法判断波动——**没有预算的分数是不可复现的分数，没有双跑的分数是不知道方差的分数**。
- 提升层：工作流/可复用 Skill。触发词：路由器一等被测、锁定指标、results-published、调用预算、双跑差值、top-1 双基线。

## 「没有分数」与「零分」是两件事；通过=多智能体取最大 × 全维度合取，增益不得越过闸门（来源：api.github.com/repos/NVIDIA/SkillEvaluator/contents/docs/reports.mdx 20,014B（evaluator 0.8.2），2026-10-01 r348C 独立 curl 实拉取 base64 解码，`INCOMPLETE`×5 / `NEUTRAL`×6 / `Skill Lift`×5 / `pass-threshold` 逐串命中）
- 判据：① **报表里「缺一个分数格」与「0.0」必须视觉与语义都可分**：原文区分「failed/incomplete trial publishes none of its scores」与「a genuine model score of `0.0` is still a valid, published score」。⇒ 把基础设施故障产生的缺失读成「能力为零」，是评测面最典型的一次误判；**缺失必须单独成档**。② **证据不足要有独立 verdict**：`INCOMPLETE`（必需扫描器没给出可信证据）与 `NEUTRAL`（证据完整但至少一个必需维度低于通过带）都不是通过。⇒ 验收表如果没有「无证据」这一格，缺省行为就是把失败合并进通过。③ **通过判据是 max-over-agents × all-dimensions**（每个配置维度都过、且至少对某个受支持 agent 成立），不是平均、也不是加权综合分；提升幅度（Skill Lift）只是诊断证据，**本身不能推翻闸门**。⇒ 用「平均提升了多少」叙述通过与否，等于用诊断量替换判据。
- 提升层：可复用 Skill。触发词：缺失不等于零分、INCOMPLETE 独立 verdict、NEUTRAL 不通过、max-over-agents、全维度合取、Skill Lift 不推翻闸门。

## 任务成功不是安全信号；技能自带的非文本资产是扫描器看不到的指令载体（来源：arXiv 2609.35912 MMSkillRisk 44,757B，2026-10-01 r348C 独立 curl 实拉，`43.1%` / `16.4 percentage points` / `36.5%` / `72.2%` 逐串命中）
- 判据：① **验收必须同时断言「任务做对了」与「没越权」，两件事分开计量**：实测攻击成功与合法任务完成在 **36.5%** 的用例中同现（GPT-5.6-sol + Codex 达 **72.2%**），作者明写「task success alone does not establish safe skill use」。⇒ 只看成功率的安全评测会在高同现率下给出绿灯——**成功率是能力指标，不是安全指标**。② **扫描面必须覆盖技能目录里的非文本资产**（图片 / PDF / 示例数据）：把恶意指令做成教学图片的原生成分（标注、界面文字），pooled ASR 43.1%，**比同等文本载体基线高 16.4 个百分点**。⇒ 只扫文本等于留一条免费绕过通道；审一个技能包时，非文本资产要单独列进扫描清单。
- 提升层：可复用 Skill/工具。触发词：任务成功不等于安全、攻击与成功同现 36.5%、非文本资产载体、图片注入、ASR 43.1%、比文本载体高 16.4pp。

## 评测 harness 是「多件」不是「一件」：构建评测 / 成本爬升 / 审计各是独立流程件，且交付包与被引文件集必须核差集（来源：api.github.com/repos/anthropics/skills/commits 58,317B，2026-10-01 r349A 独立 curl 实拉，`build-eval` ×12 / `eval-hillclimb` ×4 / `cost-hillclimb` ×2 / `eval-audit` ×2 / `not shipped` ×2 逐串命中；经 Qoder r366-Q-A 提名）
- 原文：① 2026-09-29 一次性补入 `shared/evals/` 下 `build-eval`、`eval-hillclimb`、`cost-hillclimb`、`eval-audit` 四套流程 + report schema + runner scaffold；② commit 明写「drop references to files **not shipped** with the skill」。
- 判据：① **「跑个评测」不是一个动作而是四件**：构建评测集、按指标爬坡、按成本爬坡、审计评测本身各自独立成流程件 ⇒ 只有一个「评测脚本」的仓库无法回答「指标涨了但成本涨了多少」「评测本身有没有被审」。② **成本爬升与质量爬升必须分开跑**：合并成一个优化目标，成本会被质量掩盖（或反之）。③ **交付包内容集 ⊇ 被引文件集是发布前硬门**：被引但没随包发出的文件等于发布了一个必然断链的产物；与既有「删后查悬空引用」互补——那条是事后补救，本条是**发布前产物一致性门**。④ 状态码承载存在性语义（model access=404、beta gating=400 而非 403）属同一「选择即申报」族，本轮未独立取到原文，登记待复核。
- 提升层：可复用 Skill/工具。触发词：build-eval、eval-hillclimb、cost-hillclimb、eval-audit、评测四件、交付包与被引文件差集、not shipped。

## 外部判定器按「块」返回时，结论的作用域是块不是制品：分段粒度是设计参数，不是实现细节（来源：docs.dify.ai/en/cloud/use-dify/workspace/api-extension/moderation-api-extension.md 7,593B，2026-10-01 r349B 独立 curl 实拉，`segmented into 100-character chunks` / `direct_output` / `overridden` 逐串命中；经 Qoder r367-Q-B 提名）
- 原文：输出内容「will be **segmented into 100-character chunks** for API requests to avoid delayed reviews when output content is lengthy」；审核响应契约 `flagged` / `action`（仅 `direct_output` | `overridden`）/ `preset_response`。
- 判据：① **PASS 只覆盖已检块**：分段送审意味着「这一制品通过了」实际是「这些块通过了」，**拼接处的跨块载荷不在判定面**（把敏感内容拆到两段之间即可绕过）⇒ 采信外部审核结论前先问分段长度与边界。② **分段长度是防延迟的性能参数，却同时决定了安全语义**，两者耦合且默认不可见。③ 与既有扫描三轴（输入格式 × 被读取字段 × 结构深度/来源类型）互补，补**分段边界轴**。
- 提升层：工具。触发词：分段送审、100-character chunks、结论作用域是块、跨块载荷绕过、moderation action 两值。

## 引用清单要带机器可判的新鲜度字段：有 staleAfter 就照它判，没有就退回 generatedAt 距今天数（来源：api.github.com/repos/anthropics/skills/contents/skills/academy-guide/SKILL.md 7,715B base64 解码，2026-10-01 r349B 独立 curl 实拉，`staleAfter` / `generatedAt` 逐串命中；经 Qoder r367-Q-B 提名）
- 原文：URL「taken verbatim from the catalog」（数据源 `catalog.json`）；「`staleAfter` 未到即信任；无该字段时 `generatedAt` 距今 **about 30 天**视为 stale」。
- 判据：① **新鲜度要落成字段而不是靠人判断**：给了 `staleAfter` 就用它，没给就用 `generatedAt` + 默认窗口——**两级兜底**使得「这条推荐还新不新」成为可机检命题，而不是读者凭印象。② **失效时的默认动作是「不推」**：推荐位失效宁可静默不推，也不要把过期清单降级成「仅供参考」继续用。③ 与既有「证据先过期的第三时钟（引用可复核性）」分工：那条判**能不能复核**，本条判**机器怎么判新鲜**。
- 提升层：可复用 Skill。触发词：staleAfter、generatedAt、引用新鲜度字段、30 天窗口、失效即不推、catalog 引用清单。

## 检索类能力降级要「机器可读自证」：响应体自带 mode 声明，采集侧按 mode 分档记可信度（来源：www.activepieces.com/docs/mcp/tool-search.md 3,608B，2026-10-01 r349C 独立 curl 实拉，`semantic` ×4 / `keyword` ×3 / `audience` 逐串命中；经 Qoder r372-Q-A 提名）
- 原文：检索在依赖缺失（无 embedding key / 无 pgvector）时**不报错而静默换档**，故响应体自带 `mode=semantic|keyword`；另有「低相关按阈值丢弃而非凑数返回」与 `audience:'human'` 动作被排除在外两条。
- 判据：① **HTTP 200 + 有结果 ≠ 用的是预期能力**：依赖缺失时降级为关键词检索且不说 ⇒ 结论可信度必须由**响应体自带的 mode 声明**承载，采集侧按 mode 分档，而不是按成功状态码判有效。② **候选集被主动裁剪且裁剪依据随模式变化**：低相关丢弃、`audience:'human'` 排除 —— 「没搜到」可能是被裁掉了，不是不存在。③ 与既有「静态资格报告只覆盖它检查过的项」同族，但作用在**检索返回面**。
- 提升层：工具。触发词：mode 声明降级、semantic/keyword 静默换档、按 mode 分档记可信度、候选集主动裁剪、audience human 排除。

## 验证环节要「定向且完整」，否则只能换来高误封：单条边被篡改即把误放率推到 15.3–48.9%（来源：arXiv 2609.40027《Who Verifies the Graph?》abs 页 43,234B，2026-10-01 r349C 独立 curl 实拉，`15.3` / `48.9` 逐串命中；经 Qoder r368-Q-C 提名）
- 原文：因果动作验证图中**单条边被篡改**即把工具执行误放率推至 **15.3–48.9%**；改随机抽检能拦截篡改但会误封大量合法动作（误封率数值本轮 abs 页未命中，登记待复核）。
- 判据：① **验证的两难是误放率 × 误封率的乘积**：定向且完整的验证能压低误放，随机抽检能拦篡改但把合法动作一起拦掉 ⇒ 「随手核一核」两头不落，比不做更糟（因为它会产生「已验证」的错觉）。② **给验证环节选型前先量化这对指标**：不量化就无法判断该投入多少；「加一道校验」本身不是收益。③ 与既有「静态扫描覆盖三轴」互补：那条讲**覆盖面的坐标系**，本条讲**覆盖率与误报的取舍曲线**。
- 提升层：工具/工作流。触发词：误放率 15.3–48.9%、验证器两种失效端、定向完整 vs 随机抽检、误放误封取舍、因果动作验证图。

## r350C · 验证执行面 ≠ 生产执行面：某些配置只在特定触发/执行方式下生效（来源：help.make.com/scenario-settings.md，2026-10-02 r350C 实拉 5,172B）

- **★同一份配置，手动"Run once"执行会绕过它**：cycles per run 设定在手动点 Run once 时被忽略、**只跑 1 个周期**。判据：**手动复现跑出来的结论不能外推到生产**——你验的是一个被裁剪过的执行面。
- **★失败停用策略按触发类型分叉**："达到最大失败次数后停用场景"对**即时触发（instant trigger）场景被忽略**——第一个错误发生即立即停用。判据：**即时触发场景没有"重试 N 次再停"的缓冲**，验证时的容错假设在即时触发下不成立。
- **★提交时机默认在最外层**：默认只在整场成功结束时 commit，可改为"每个模块运行后 commit"。判据：**默认提交点是全成功，不是逐步**——中途失败即全部未提交，据此设计的"部分完成"假设需要显式改配置并写进验证条件。
- 落地口径：写验证方案时先声明执行方式（手动/定时/即时）与触发类型，再声明该方式下哪些配置会被忽略；否则验证结论不可复现。
- 提升层：工作流 / 可复用 Skill。


## r353A · 失败现场的处置由开关决定，取证能力会被隐私开关直接削掉

> 原文已下沉 `references/knowledge-base.md §r395-av`（保持原文零删减）。
## r353B · 错误契约随失败位置分叉，取证通道可用 `.md` 后缀直取

> 原文已下沉 `references/knowledge-base.md §r395-av`（保持原文零删减）。
## r353C · 事务边界由模块能力标注决定；验证有自己的预算币种；文档站提供问答式检索接口

> 原文已下沉 `references/knowledge-base.md §r395-av`（保持原文零删减）。
## r354A · 留痕按「失败优先」分级保存；删除是两阶段，且活跃态与人工标注豁免（来源：docs.n8n.io `deploy/host-n8n/configure-n8n/scaling/manage-execution-data.md` 独立 curl 取 `.md` 原文，2026-10-02 r354A 实拉）

- **★保存是四个独立开关，不是一档总闸**：`EXECUTIONS_DATA_SAVE_ON_ERROR=all` / `SAVE_ON_SUCCESS=none` / `SAVE_ON_PROGRESS=false` / `SAVE_MANUAL_EXECUTIONS=false` 可分别取值。判据：**取证留痕按"哪类执行值得留"分级**——失败全留、成功不留、过程态可选、手工触发默认不留；把四档合成一个"开/关日志"，要么在故障时什么都没留下，要么在平时把存储吃光。
- **★删除先标记后真删，并保留安全缓冲**：原文 "pruning first **marks targets for deletion**, and then later permanently removes them"，且 "honors a **safety buffer period** of `EXECUTIONS_DATA_HARD_DELETE_BUFFER` hours (default: 1h)"。判据：**清理必须可反悔**——标记与真删之间留一个可撤销窗口，等价于技能侧"先移入待删区、缓冲期后清"。
- **★活跃态不可被清理**："Executions with the `new`, `running`, or `waiting` status **aren't eligible for pruning**"。判据：**任何清理器必须先按状态过滤**——未终态的对象被回收，会把"还在跑"变成"消失了且无日志"。
- **★人工标注即永久豁免**："**Annotated executions (for example, executions with tags or ratings) are never pruned.**" 判据：**人做过标记的证据 = 不可被自动策略删除**；自动化清理规则永远不能覆盖人工显式保留，否则人会失去对"什么值得留下"的最后决定权。
- **★保留策略是双阈值，任一满足即触发**：age（默认 336h/14 天）**OR** count（默认 10,000，从旧到新删）。判据：**只按时间或只按条数设保留策略都会在另一侧失控**——低流量时靠 age 兜住"永远不会自动清"，高流量时靠 count 兜住"存储先爆"。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：留痕分级、save on error、删除两阶段、hard delete buffer、活跃态豁免、标注永不清理、双阈值保留。


## r354B · 截断/限额必须声明作用域（展示面 vs 执行面）；无鉴权通道靠「一次性」兜底；评测并发按档位给默认（来源：docs.n8n.io `use-environment-variables/executions.md`、`use-environment-variables/credentials.md`、`administer/manage-credentials/credential-overwrites.md` 独立 curl 取 `.md` 原文，2026-10-02 r354B 实拉）

- **★截断只作用于展示面，绝不能连带执行面**：`EXECUTIONS_DATA_MAX_DISPLAY_SIZE` 默认 104857600 字节，超出在编辑器/详情/公开 API 显示 "too large to display"（原文目的："to avoid running **low-resource instances** out of memory"），但 "**Doesn't affect retrying or resuming executions, which always load the full data**"。判据：**任何"太大就不给你看"的限额都必须显式声明它不覆盖重试与续跑**——否则用户会把"展示被截"读成"数据没了"，进而放弃本可恢复的执行。
- **★无鉴权通道的安全性靠"只能调用一次"兜底**："**Without an auth token, the endpoint can only be called once for security reasons**"（凭据覆盖端点）。判据：**当一条通道必须存在但无法前置鉴权时，可用"一次性/单发"替代鉴权**——把无限次暴露压成单次窗口；这是"要么鉴权要么裸奔"之外的第三条路。
- **★注入的凭据是"可用不可读"，且平台会主动隐藏**："This data **isn't visible to users**, but n8n uses it automatically in the background"；"In the Editor UI, n8n **hides all overwritten fields** by default"。判据：**平台级注入的凭据面向用户只暴露"连接"动作，不暴露字段**——凡"我配好了你直接用"的能力，界面上必须消字段，否则注入等于没注入。
- **★同一能力有推荐/不推荐两套实现，文档会显式标注**：关于用环境变量写凭据覆盖，原文 "**This approach isn't recommended. Environment variables aren't protected in n8n, so the data can leak to users**"；推荐做法是走自定义 REST endpoint + bearer token。判据：**选型时先找"是否被标注不推荐"，而不是先找"能不能跑通"**——能跑通但不被推荐的实现，通常是在某个维度（此处为泄露面）有已知缺陷。
- **★评测并发与生产并发是两个独立变量，且评测默认被压到最低档**：`N8N_CONCURRENCY_PRODUCTION_LIMIT` 默认 `-1`（禁用、不限）；`N8N_CONCURRENCY_EVALUATION_LIMIT` 默认 **跟随 license 档位**（self-hosted Community 1 / Cloud Pro 1 / Business 3 / Enterprise 5），"Setting this overrides the tier default"。判据：**"未设置"不等于"不限制"，而是"跟随某个你看不见的档位默认值"**；做容量估算时必须先确认该档位是多少，否则按"不限"规划会实际跑在 1 上。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：展示截断、执行面全量、too large to display、无鉴权一次性、凭据覆盖、不推荐实现、评测并发、档位默认。


## r354C · 机器可读取证有第四条通道：`Accept` 头内容协商；OOM 有三层异构信号且自愈能力取决于运行方式（来源：docs.n8n.io `scaling/memory-errors.md` 404 页 2,188B + `scaling/fix-memory-issues.md` + `scaling/use-external-storage.md` 独立 curl 取 `.md` 原文，2026-10-02 r354C 实拉）

- **★第四种机器可读通道：请求头内容协商**：404 页原文 "You may also use **`Accept: text/markdown` header for content negotiation**"。判据：**取证枚举顺序应为：`.md` 后缀 → `Accept: text/markdown` 头 → `?ask=` + `?goal=` 问答接口 → `sitemap.md` 全索引 → `llms-full.txt` 全量导出**；前两条是"同 URL 换形态"（零猜测），后三条是"不知道确切页名时"的检索手段。与 r353C 已落的 `.md` / ask / sitemap 相邻但不同层——那条把「加后缀」当技巧，本条把它编成**有序的通道阶梯**。
- **★OOM 有三个观测入口，且它们不在同一层**：① 应用层提示 "Execution stopped at this node (n8n **may have** run out of memory while executing it)"（注意措辞是 **may**——应用层只能给可疑，不能确认）；② 可用性层症状 "Problem running workflow"、"Connection Lost"、"503 Service Temporarily Unavailable"（"suggest that an n8n instance has become unavailable"）；③ 宿主层日志 "Allocation failed - JavaScript heap out of memory"（**only when self-hosting**）。判据：**资源类故障不能只盯一个入口**——应用层给怀疑、可用性层给影响面、宿主层给确证；把应用层的 "may" 当成确证会误判根因，只看宿主日志又会漏掉没打日志的场景。
- **★自愈能力由运行方式决定，不由产品决定**："On n8n Cloud, or when using n8n's **Docker image**, n8n **restarts automatically** when encountering such an issue. However, when running n8n with **npm you might need to restart it manually**"。判据：**"崩溃后能不能自己起来"是部署形态的属性**；同一份代码在 Cloud/Docker 下有自动重启、在 npm 下没有——写可用性方案时必须绑定运行方式，不能写"系统会自愈"。
- **★"不设限"是显式取舍，代价被转移给用户**："n8n **doesn't restrict** the amount of data each node can fetch and process. While this gives you freedom, **it can lead to errors** when workflow executions require more memory than available"。判据：**评估一个系统时要区分"它没有这个能力"与"它有意不施加这个约束"**——后者把资源风险转嫁给使用者，用户侧的应对是自建预算与分批处理，而不是等平台加限制。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：Accept text/markdown、内容协商、取证通道阶梯、OOM 三层信号、may have run out of memory、heap out of memory、Docker 自动重启、npm 手动、不设限的取舍。


## r355A · 「仍在正确处理」≠「在服务窗内可用」：吞吐与延迟必须分开判；厂商性能数字是配置的函数而非常量（来源：docs.n8n.io `scaling/control-concurrency.md` 4,111B + `use-n8n-cloud/understand-concurrency.md` 3,828B + `scaling/measure-performance.md` 3,955B 独立 curl 取 `.md` 原文，2026-10-02 r355A 实拉）

- **★高负载下的失效形态是"延迟越界"，不是"失败"**：原文 "Under higher loads n8n **usually still processes the data**, but takes **over 100s** to respond"。判据：**验证结论必须同时给"是否正确完成"与"是否在服务延迟窗内完成"两个数**——只判前者会在系统已经不可用时给出全绿结论；**延迟越界是一种独立失败态，不能并进"慢"里当表演化**。⇒ 验收前先声明延迟上界，再判成功。
- **★吞吐数字必须连同它的成立条件一起引用**：原文 "n8n can handle up to **220 workflow executions per second** on a single instance"，紧随其后 "The performance of n8n **depends on** factors including: the workflow type / the resources available to n8n / how you configure n8n's scaling options"，并给出两套基准的完整配置（ECS c5a.large 4GB 单实例 + Postgres；七台 c5a.4xlarge 含 2 webhook + 4 worker + MySQL + Redis），且明确要求 "To get an **accurate estimate for your use case**, run n8n's **benchmarking framework**"。判据：**性能基准是配置的函数**——引用时必须连硬件、拓扑、工作流形态一起记，缺任一项即不可迁移；与 §「没有预算的分数不可复现」分工：那条管评测分数的可比性，本条管性能基准的可迁移性。
- 判非（本轮实拉到但已覆盖，不重复落）：并发闸门只覆盖生产执行 / 排队项不可重试 / 重启按上限恢复（已落 dl §并发闸门有作用域，重叠 >60%）；评测并发是独立额度且默认跟随档位（已落 av §r354B，重叠 100%）；新能力默认关闭 + 行为不变承诺（已落 sa §r354A）。
- 提升层：验证 / 工作流。触发词：吞吐与延迟分离、延迟窗、服务窗内完成、still processes the data、220 执行每秒、性能基准可迁移、自测基准框架。


## r355C · 兼容性验证不能只判「崩没崩」：字段移除后的真实表现是「继续运行但降级」；能力按载体版本分档，缺档是「能用但少一档」（来源：docs.n8n.io `changelog/v30-breaking-changes.md` 21,374B 独立 curl 取 `.md` 原文，2026-10-02 r355C 实拉）

- **★「已移除」不等于「会报错」**：`defaults.color` 被移除后原文是 "Community nodes that still set it **keep working**, but the editor shows a Font Awesome icon in a **neutral color**"，并注明使用文件图标的节点 "aren't affected, because n8n never tints file icons"。判据：**兼容性验证的判据必须包含"效果有没有变"，而不只是"有没有崩"**——只跑「能不能起来」的烟测会系统性漏掉这类静默降级；验收项要按「报错 / 静默降级 / 无影响」三态分别列出。
- **★能力按载体版本分档，缺档时是「能用但少一档」，必须写明哪一档没有**："Hot reload **only works on images that serve `POST /rest/dev/reload`**, so older tags **load your node but need a restart** to pick up changes"。判据：**同一能力在不同载体上是分档的**——把"加载成功"当成"能力完整"会漏掉缺失的那一档；文档/报告里要显写「哪些版本/镜像缺这一档」。与 §检索类能力降级要机器可读自证 分工：那条管**响应体要自带 mode 声明**，本条管**验收清单要按档位逐项核**。
- 判非：具体被删节点名（Function / Function Item）与字段名（`defaults.color`）、Docker Compose 推荐路径、v3.0 的时间点（均属平台登记项，不迁移为判据）。
- 提升层：验证 / 工具。触发词：静默降级三态、移除后仍可用、兼容性验收、能力按镜像分档、缺一档。

## r383A · 升级回归机检与验收探针必须打数据面（来源：docs.langflow.org/deployment-multi-worker + docs.n8n.io + docs.dify.ai Weaviate 迁移页，2026-10-02 r373-Q-A 实拉；经 Qoder 提名）
- 升级后回归面的机检入口 = 为每个观测位写明「非零是否异常」的白名单：`polling_watchdog_kills` 非零正常、`dispatcher_internal_errors` 非零才是 bug、跨 worker 取消证据须显式标记；一次性日志提醒须入机器可读自查清单。
- 验收探针必须打数据面且等就绪窗口：控制面 200（如 `/v1/meta` 2s 即答）与分页计数都不是数据完整证据；`/v1/objects` 404 空、GraphQL 422、totalResults 是分页大小不是集合大小——须用 Aggregate 取真实计数。

## r383B · 评测判分器自证与记忆评测混杂控制（来源：arXiv 2609.38021 + codeload.github.com/cjchanh/longmemeval-evidence、arXiv 2606.29914，2026-10-02 r375-Q-C 实拉；经 Qoder 提名）
- LLM-as-judge 结论必须挂「控制组通过率 + 模板 SHA-256 哈希 + 模型带日期快照」三件，缺一即该分数不可引用；byte-identical 答案重判仍翻 3 个 verdict 证明 judge 非确定性。
- 跨方案对比前先固定嵌入与检索管线、按模型家族分层报数、并把写入成本放在结论之前：只换 embedding 模型即 +6.2pp（p=0.004），同 packet 仅换 reader 使分数从 93 拉到 479，agent 自存记忆 42% 低于基础检索 47%。

## r383C · 翻页终止谓词与截断响应不入均分（来源：skillsmp.com openapi.json、api.github.com anthropics/claude-code CHANGELOG.md #70763，2026-10-02 r380-Q-B / r381-Q-C 实拉；经 Qoder 提名）
- 翻页终止须 `hasNext` × `totalPages` 合取；越界请求被 canonicalize 成重复末页，`totalIsExact=false` 时 total 只是下界不得当完整度分母。
- 评测样本三分类（对/错/不可评）：截断在 `max_tokens` 的响应标记 truncated 并单独计数，否则分差被输出长度分布污染；与既有 Skipped 合成结果须区分（跳过 vs 物理截断）。

## r385A · 导出/迁移产物必须自带机读验收面：清单要含「没导出什么」，截断要自证，跳过的要给原因（来源：pipedream.com/docs/workflows/export-workflows.md 6,591B 独立 curl 取 .md 原文，2026-10-02 实拉；经 Qoder r388-Q-C 提名）
- **★验收清单的价值在「未导出项」而不是「已导出项」**：原文「`manifest.json` lists **every workflow in the project, including workflows that were not exported**, so **nothing is left out without a record**」。判据：**只列成功项的清单无法回答"漏了什么"**——迁移/导出/批量操作的产物必须把失败与跳过项一并登记，且逐项带 `status` 枚举（`exported` / `skipped_never_deployed` / `skipped_export_limit`），让"跳过"本身成为可判状态而不是沉默。
- **★产物要自带截断与限额自证**：manifest 同时给出 `schema: "project-export/2026.01"`、`truncated: false`、`truncated_reason: null`、`limits: {workflows: 500, bytes: 268435456}`。判据：**完整性不是"看起来齐"，而是产物自己声明自己是否被截断、按什么限额截的**——验收方不读这套自证字段，就无法区分"确实只有 3 项"与"到第 4 项被限额掐断"。
- **★需人工重填的部分必须逐条点名到 step 与 prop**：`warnings[]` 给出「step send_message: secret prop api_key was omitted from the export and **must be re-entered after import**」。判据：**"导入后需要重新配置"这种话没有验收价值**——点名到具体步骤与字段才能机检；warnings 为空才是真的无需人工介入。
- **★迁移/导出只搬结构不搬凭证，这条边界要写进验收而不是使用说明**：secret props 一律 `<redacted>`、App props 只保留 `authProvisionId` 且「Tokens and other credentials are removed」、私有组件「includes the component key, **but not its code**」。判据：**导入后"能装上"不等于"能跑"**——凭证与私有代码是结构化缺口，验收必须把它们列为显式待补项，与 §r383A「迁移工具只搬被引用资源」分工：那条管**资源覆盖面**，本条管**产物自带的验收面字段**。
- 提升层：验证 / 工作流。触发词：机读验收面、manifest 含未导出项、status 枚举、truncated_reason、warnings 点名、只搬结构不搬凭证、导入后需重填。

## r385C · 「没报错」是一种会被上游静默翻转的判据：验证要用往返校验，且要能覆盖已入库的坏数据（来源：api.github.com/repos/langflow-ai/langflow/pulls/15241 26,494B JSON，2026-10-02 独立实拉；经 Qoder r389-Q-A 提名）
- **★通过判据要防"上游把失败改成成功"**：同一个检查点在 langchain-core 1.5.1 下 `RAISED PydanticSerializationError`，在 1.6.3 下 `OK {'func': "'<function _run at 0x...>'", 'coroutine': "'<function _arun at 0x...>'"}` 且 `warns: []`。判据：**凡以"未抛异常"为通过条件的验证，都要问一句"如果上游把这种异常改成静默降级，我的判据还成立吗"**——能通过的对象已经坏了，而且**没有任何告警**。⇒ 把"成功"替换为"成功且能还原为同一对象"。
- **★验收要区分「新写入」与「已入库」两条路径**：修复后验证给出双侧对照——`=== lc 1.6.3 WITH fix === built_object stored: None / opaque-dropped: ['chat_input'] / RESUME OK`，而**已入库的毒化 payload 仍要靠读侧降级**才能恢复。判据：**只验证新写入路径的修复，会把存量病灶判成"已解决"**；验收清单必须显式包含"拿老数据跑一遍"。
- **★"文档说覆盖了"不等于"真的覆盖"**：原文自曝「`test_serialize_value_degrades_model_with_unserializable_field` is **documented as covering this case but passes either way**; its docstring now says which failure mode it actually covers」。判据：**测试名与文档声明不构成覆盖证据**——要证明覆盖，必须让该测试在缺陷存在时失败。
- 提升层：验证 / 工具。触发词：往返校验、静默降级、未抛异常不算通过、存量数据验收、测试名不等于覆盖证据。

## 验收权限面：声明集合 ≠ 生效集合，须展开自动授予闭包与单向包含关系（来源：docs.n8n.io `.../create-custom-project-roles.md` 11,109B + `create-custom-instance-roles.md` 8,015B，2026-10-03 r388A 独立实拉）
- **原文**：「Granting `<resource>:read` also grants the matching list scope for that resource」「Granting `workflow:publish` also grants `workflow:unpublish`」「**Manage all roles** ... Automatically includes **Manage project roles**」「**Manage others** ... Automatically includes **Manage own**.」
- **判据**：① **验收权限声明时不能只读字面清单**——系统存在隐式自动授予（read→list、publish→unpublish），「批了这两项」实际生效四项；漏掉闭包会得出「最小权限已满足」的错误结论。② **层级包含是单向的**——实例级 Manage all roles 蕴含项目级，项目级反过来不蕴含实例级；按清单逐条比对会漏掉「被上层顺带带下来的」那部分。③ 落点：验收报告对授权面必须给**展开后的闭包**与**包含方向**，只列「授予了 A、B」不算完成验收。
- 提升层：可复用 Skill / 工作流。触发词：权限闭包、自动授予、read 隐含 list、包含方向、声明≠生效、授权面验收。

## 留痕的四态覆盖等级与「有留痕 ≠ 完整留痕」：验收必须带 coverage 字段（来源：docs.openclaw.ai/gateway/audit.md 37,793B，2026-10-03 r388B 独立实拉）
- **原文**：「It never stores prompts, message bodies, tool arguments, tool results...」「Coverage is `enforced` only when every contributing ingress decision was participant-aware and outcome-affecting. Wildcard/open policy ... remain `attribution-only`; mixed or missing evidence is `unknown`.」「Persistence remains best-effort. Queue saturation, storage failure, shutdown timeout, and process crashes can lose evidence; they log only a bounded operational warning and never abort the run.」
- **判据**：① **留痕必须自带覆盖等级，不能只看有没有**——`enforced`（该判定真实改变结果）/ `attribution-only`（只记录谁观察到，不证明授权）/ `unknown`（证据缺失或混杂，不重建）/ `unsupported`（该通道根本不产生此类证据）四态是互斥的验收结论；把 attribution-only 当 enforced 是验收里最常见的高估。② **留痕通道本身允许丢**：队列饱和、存储故障、关机超时、进程崩溃都会丢证据且只打一条有界警告、**不中止运行**；所以「日志里没有」既可能是「没发生」也可能是「发生了但没记下来」，验收报告必须显式声明丢失面，不能默认留痕完备。③ **只留结构不留内容是设计选择而非缺陷**——元数据账本永不存正文/参数/结果/文件名/URL/命令输出，验收「看到一条记录」不等于拿到可复现内容。
- 提升层：可复用 Skill / 工作流。触发词：coverage 四态、attribution-only、enforced、unknown、unsupported、留痕丢失面、有日志不等于完整、元数据账本。


## 可见性必须分层声明：元数据人人可见、正文按归属可见、管理视图只给 redacted（来源：docs.n8n.io `administer/manage-credentials/end-user-credentials.md` 9,720B，2026-10-03 r390A 独立 curl 取 `.md` 原文实拉；与 §留痕四态 coverage 互补——那条管留痕是否完整，本条管同一份留痕对不同人的可见面）
- **原文**：「When a workflow execution uses an end-user credential, **the execution metadata is visible to anyone with access to that workflow's executions**: the status, when it ran, and that it used an end-user credential. **What changes is who can see the data inside.**」；「Only the user who triggered the workflow with their connected account can see the input and output data for those nodes... **For everyone else, including instance admins, those nodes show redacted output.**」
- **判据**：① 验收"谁能看到什么"要拆成三层分别声明——**元数据层**（状态/时间/用了哪类凭据，全员可见）· **正文层**（输入输出，仅归属者可见）· **管理视图层**（存在性与计数，管理员可见但正文被 redacted）。② **"管理员能看见"不等于"管理员能看见全部"**——管理视图返回脱敏结果是设计就该如此；把管理员可见当成全量可见，会得出"反正 admin 能看到，脱敏没意义"的错误结论。③ 验收动作固定为：**对同一条记录，分别以归属者、同级他人、管理员三种身份各取一次**，比较三次返回差的正是声明里的三层；只验一种身份的可见性等于没验。
- 提升层：可观测性 / 安全边界。触发词：可见性分层、元数据可见正文不可见、admin redacted、三种身份各取一次、脱敏不是摆设。


## 影响边界声明：一个配置项改了什么不重要，重要的是它「不影响什么」；隐私类验收必问「防谁」（来源：docs.openclaw.ai/concepts/session 22,767B，2026-10-03 r390B 独立 curl 取 `.md` 原文实拉；与 §可见性三层 互补——那条管"谁看得到"，本条管"改了 A 会不会连带改了 B"）
- **原文**：路由绑定覆盖「**This setting changes session-key selection only**: DM routing, mention gating, delivery context, and replies to the source room remain unchanged.」；incognito「protects them from storage and other gateway-mediated users, **not from the gateway owner or process operator**, who can always observe live sessions」；「Incognito **does not restrict the agent's normal tools**」。
- **判据**：① **配置项/改动说明必须带"不影响面"清单**——原文给出的是标准写法：改了 key 选择，但路由、mention 门控、投递上下文、回复目标一律不变。⇒ 验收时若只验证"改生效了"，会把相邻面被无意改动的情况全部放过。② **隐私/隔离类能力的验收第一问是"防谁"**：防存储与其他用户，不防宿主与运维——写成"已启用隐私保护"而不写防护对象，等于给出一个无法证伪的断言。③ **隔离不得与能力混为一谈**：隐私模式不改工具写盘能力，"没落进会话存储"不等于"没落到磁盘"。⇒ 验证隐私必须到会话存储之外去找（文件、模型提供方、运维侧日志）。
- 提升层：安全边界 / 可观测性。触发词：不影响面、配置影响边界、隐私防谁、隔离不等于不落盘、改动相邻面。


## 留痕有两种缺口：旁路根本不进账，假名可以复原——覆盖声明必须同时给出「不覆盖清单」与「去标识的密钥在哪」（来源：docs.openclaw.ai `gateway/config-observability.md` 10,454B + `gateway/configuration-reference` 索引，2026-10-03 r391A 独立 curl 取 `.md` 原文实拉；与 §留痕四态 coverage / §审计分层视图 互补——那两条管状态枚举与跨层可见面，本条管账本本身的入口边界与可逆性）
- **原文**：消息元数据三档「`messages`: `"off"` | `"direct"` | `"all"` … `"direct"` records known direct conversations only. `"all"` also records group, channel, and unknown conversation kinds. Both modes remain **content-free and replace raw identifiers with installation-local keyed pseudonyms** where correlation is available. These are **correlation aids rather than anonymization**; the state database **stores the derivation key**, but RPC and CLI exports do not.」；覆盖边界「Message coverage includes accepted inbound messages **that reach core dispatch** and one terminal row per original logical outbound reply payload **that reaches shared durable delivery**. **Plugin-local and direct-send paths that bypass those shared boundaries are not covered.**」；「The bounded background writer is **best-effort, not a lossless compliance archive**.」；归因面「`executionIdentity` … This privacy-sensitive metadata is **disabled on fresh installs and upgrades** … for **newly admitted runs**.」；留痕开关「Setting `false` stops new event collection immediately; existing records stay readable until they expire. Turning it back on resumes recording from that point — **the gap is not backfilled**.」
- **判据**：① **"有审计"必须附一份不覆盖清单**：原文的标准是——只记**到达共享边界**的事件（入站要进 core dispatch，出站要到共享持久投递），**插件本地路径与直发路径一律不覆盖**。⇒ 验收留痕完整性时，先问"这条路径走没走共享边界"，没走就是账上本来没有，不是丢了。② **假名化不等于匿名化，判断依据是派生密钥留在哪**：导出面用 installation-local pseudonym 替换原始 id，看起来已去标识，但**派生 key 存在状态库里**，只是 RPC/CLI 导出不带。⇒ 凡"我们导出的日志已匿名"的声明，必须追问密钥存放位置与能否复原；能复原就是假名化，受的是另一套要求。③ **账本写入是 best-effort**：后台写入器允许丢失，官方明说不是无损合规档案。⇒ 需要"一条不落"的场景不能拿它当唯一证据源，必须另配独立通道。④ **敏感归因面默认关、升级也不开、且只对之后新准入的运行生效**：这类开关的语义是"从现在起"，不是"把历史补齐"——与留痕开关**关闭即时停采、重开不回填空档**是同一条规则。⇒ 验收"某次运行有没有归因信息"时，答案是分段的：开之前的一律没有，不能靠事后开启补出来。
- 提升层：可观测性 / 治理。触发词：不覆盖清单、plugin-local 旁路、direct-send 旁路、假名化≠匿名化、派生密钥、best-effort 账本、executionIdentity 默认关、gap 不回填。


## 观测数据的裁剪必须选「安全侧」：只裁能重建的那一侧，裁完还超就失败而不是继续跑；取证默认面常常只够定位、不够复现（来源：www.activepieces.com/docs `install/troubleshooting/truncated-logs.md` 2,392B + pipedream.com/docs `workflows/building-workflows/errors.md` 9,150B，2026-10-03 r391B 独立 curl 取 `.md` 原文实拉；与 §截断自证 / §截断只作用展示面 互补——那两条管截断怎么声明与属于哪一面，本条管先裁哪一侧、裁完怎么办）
- **原文**：「Truncation applies to **step inputs only**. Step **outputs are never truncated**, because downstream steps, subflows, and paused/resumed runs need the original output to continue executing correctly. If outputs were dropped, the next step would receive missing data and fail unpredictably.」；「step input values are replaced with `(truncated)`, **starting from the largest**, until the run fits」；「If the run **still** exceeds the limit after all inputs are truncated — meaning step outputs alone are over the cap — the run **fails with `LOG_SIZE_EXCEEDED`**」；「prefer passing files between steps using the built-in file storage … rather than embedding raw bytes in step outputs」；Pipedream 取证面「list the **most recent 100** workflow errors … By including the `expand=event` query string param, Pipedream will return the full error data, **along with the original event** that triggered your workflow」。
- **判据**：① **裁剪方向由"谁依赖它"决定，不是由"谁更大"决定**：输出被下游步骤、子流、暂停恢复依赖，裁掉会让下一步拿到缺失数据并以不可预测的方式失败 ⇒ 只能裁输入（可从上游重放得到），并且**从最大的开始裁**。设计任何观测裁剪策略时先画依赖方向：会被后续消费的那一侧是不可裁侧。② **"尽力裁"到顶之后必须是失败，不是带病运行**：全部输入裁完仍超限说明是输出把运行撑爆，此时引擎选择 `LOG_SIZE_EXCEEDED` 直接失败。⇒ 观测上限触顶属于**失败态**，要有独立错误码；把它当警告继续跑，等于让后续步骤在缺失数据上静默出错。③ **提高上限通常是下策，换数据通道才是正解**：上限本身可用 `AP_MAX_FLOW_RUN_LOG_SIZE_MB` 调，但官方给的建议是**用文件存储传大对象**而不是把字节塞进 step 输出。⇒ 遇到"数据太大装不进观测面"，第一反应应是把它移出观测面，而不是把观测面撑大。④ **取证接口默认是"够定位"不是"够复现"**：错误列表默认只给最近 100 条，且**不带触发事件的原文**，要靠 `expand=event` 显式展开才拿得到原始事件。⇒ 复盘"能不能重放"时，先确认拿到的是摘要还是原文；默认面缺的那部分通常正是复现所必需的。
- 提升层：可观测性 / 工作流。触发词：只裁输入不裁输出、从最大的开始裁、LOG_SIZE_EXCEEDED、观测上限是失败态、改用文件存储传大对象、最近 100 条、expand=event、够定位不够复现。


## 「健康检查通过」要指明是哪个端点：存活不等于就绪，详细指标往往默认关闭；密钥类接口只返回元数据不返回材料（来源：docs.n8n.io `deploy/host-n8n/keep-n8n-running/monitor-n8n.md` 3,069B + `…/security/rotate-encryption-keys.md` 5,972B + `build/manage-workflows/view-change-history.md` 4,190B，2026-10-03 r391C 独立 curl 取 `.md` 原文实拉；与 §影响边界声明 / §声明集合≠生效集合 互补——那两条管改动与权限的声明面，本条管运行状态的探测面）
- **原文**：「The `/healthz` endpoint returns a standard HTTP status code. **200 indicates the instance is reachable. It doesn't indicate DB status.**」；「`/healthz/readiness` … returns a HTTP status code of 200 **if the DB is connected and migrated** and therefore the instance is ready to accept traffic.」；「The `/metrics` endpoint … **is disabled by default**」；「the health endpoint is always enabled on the main n8n server. For **worker servers in queue mode, the health endpoint is disabled by default**.」；可用面「The `/metrics` endpoint is available on: **Self-hosted:** All editions. **It isn't available on n8n Cloud.**」；密钥接口「n8n **never returns key material in API responses**, only metadata such as the **ID, algorithm, status, and timestamps**.」；两类历史「**Don't confuse workflow history with the … executions list.** Executions are workflow runs … Workflow history is previous versions of the workflow」。
- **判据**：① **存活（reachable）与就绪（ready）是两个端点，混用会让故障从监控下溜走**：`/healthz` 只证明进程在、能应答，**不表示数据库状态**；`/healthz/readiness` 才表示数据库已连接且已迁移、可以接流量。⇒ 探针设计必须区分这两层；拿存活当就绪，会出现"监控全绿但全部请求失败"。② **观测面默认是不完整的，要显式打开**：`/metrics` 默认关闭，队列模式下的 worker 健康检查也默认关闭（主服务才常开）。⇒ "没有指标"不等于"系统没在跑"，先确认采集开关；声明"我们有监控"时应给出开了哪几个端点。③ **能力可用面要按部署形态分档**：`/metrics` 自托管全版本有、**Cloud 没有**。⇒ 同一套验收清单在两种形态下结论不同，写验收标准必须标注形态。④ **密钥类响应的正确性是"没有材料"**：接口只回 ID/算法/状态/时间戳，永不回密钥材料。⇒ 验收这类接口的动作是检查响应体里**不出现**的东西，只测"返回 200 且字段齐全"会漏掉最严重的那一类缺陷。⑤ **"历史"这个词在系统里可能指两套东西**：工作流历史=定义版本，执行列表=运行记录；恢复旧版本会先存当前版本。⇒ 排障时先对齐说的是哪一种历史，否则"看历史"会看错地方。
- 提升层：可观测性 / 治理。触发词：healthz 存活、readiness 就绪、metrics 默认关闭、worker 健康检查默认关、Cloud 无 metrics、密钥接口只回元数据、工作流历史 vs 执行历史。

## 归因会被反向代理改写；公开写入的报告通道要做信息量过滤；存储有没有卸载通道决定限额是不是同一回事（来源：pipedream.com/docs/conduit/deploy/hardening.md 7,011B + www.activepieces.com/docs/install/reference/limits.md 6,779B，2026-10-03 r393A 独立 curl 取 `.md` 原文实拉；与 §留痕两种缺口 / §影响边界声明 互补——那两条管账本入口与改动连带面，本条管账本里"是谁"这一栏会不会被基础设施改写）

- 反向代理前置会改写身份归因：不设 `CONDUIT_TRUSTED_PROXIES`，审计记录与 per-IP 限额全部算到代理头上，真实客户端消失 ⇒ 验收归因面之前先确认链路里有没有代理，这是**配置前置条件**而不是运行时故障，现象看起来却像"没记录"。
- 未鉴权的报告端点是一块公开写入面，必须做信息量过滤而不是照单全收：Conduit 丢弃两类 CSP 报告——浏览器扩展注入的内容（任何策略都管不了）、页面不在 `CONDUIT_BASE_URL` 内的报告（否则任何人可提交）⇒ **噪声与伪造是同一道门**，不记录比记录错误的东西更安全。
- 安全头作用域要克制：HSTS 是 host-only，不替无关子域 opt-in，也不申请 preload；纯 HTTP 开发地址不发 HSTS ⇒ 作用域越宽，误伤与不可回退性越大（preload 基本不可撤）。
- 同为"存储"，有没有卸载通道是两回事：KV store 的键值直接进 Postgres `jsonb`，**没有对象存储卸载通道、每次访问全量读写、计入数据库大小**；只有文件与运行日志才有卸载 ⇒ 容量验收要按存储面分开算，不能拿"日志 25MB 上限"推出 KV 也有同等余量。


## 验证结论必须声明「证明了什么的上界」，失败要分三类不可合并；同一份托管身份在不同执行面保证不同，验收须按执行面分别写（来源：docs.openclaw.ai `gateway/config-secrets-env.md` 10,309B + `gateway/config-tools.md` 7,517B 索引页 + `gateway/config-tools/github-identity.md` 17,020B，2026-10-03 r395A 独立 curl 取 `.md` 原文实拉）

- **验证证明的是上界不是全体**：官方明确「验证证明的是哪个账号应答了 GitHub API 请求」，而 `/user` 端点**不证明写权限**；仓库级授权要等一次精确仓库操作成功才算已知 ⇒ 验收报告要写「这次验证证明了 A，不证明 B」，只写「校验通过」会让人以为写权限也验过了。
- **失败三分类不可合并**：状态区分区分 missing credentials（缺凭据）/ unverified transport failure（未验证的传输失败）/ rate limiting（限流）三类，且不返回底层 `gh` 诊断 ⇒ 「拿不到结果」至少要分成「没凭据」「网络不可信」「被限流」，三者改的地方完全不同，合成一个「验证失败」就没法处置。
- **同一托管身份在不同执行面保证不同**：本地 gateway-owned exec 每次启动前读取并校验 profile，把 token 只放进私有子进程环境并清掉 `GITHUB_TOKEN`；Codex-native shell 只拿到非密 overlay（`GH_CONFIG_DIR`），**不隔离 OS keyring**，profile 消失时 gh 可回落到原生 keyring；沙箱、node-host exec、remote-exec **根本收不到**托管凭据，只有 `github_publish` 记录一个不含凭据与仓库权限的有界发布请求 ⇒ 验收必须先问「这次跑在哪个执行面」，再说「用了托管身份」保证了什么。
- **要强保证必须换执行面而不是加配置**：官方写明「需要启动绑定的托管身份保证时，用 `gateway_exec`」；native shell 的那套保证明确不覆盖 ⇒ 当能力声明与实际需求差一档时，正确处置是换通道，不是在同一通道里加参数。


## 查询接口收窄后必须自证「生效作用域 + 可能有省略」；被通知不等于可访问；附件的暂存位置、只读投影、脱敏与清理是四条独立约束（来源：docs.openclaw.ai `gateway/config-tools/sessions-and-subagents.md` 9,632B + `gateway/config-tools/custom-providers.md` 13,129B，2026-10-03 r395B 独立 curl 取 `.md` 原文实拉）

- **收窄后的列表要自带省略告警**：可见性不是 `all` 时，`sessions_list` 会在结果里附一个紧凑 `visibility` 字段说明**当前生效模式**，并给出「作用域外的会话可能被省略」的警告 ⇒ 验收方拿到的是**部分结果**，接口必须把它标出来，否则「没返回」会被读成「不存在」。
- **看得见通知不等于拿得到内容**：ambient 群组监听会向主会话排队活动通知并告知「发生了什么」，但官方明确**不授予访问权限** ⇒ 「我收到了通知」与「我能读那份上下文」是两件事，验收要分开问。
- **附件的暂存位置是硬约束**：子 agent 附件一律暂存在网关自有状态里并带 `.manifest.json`，**永不穿过子工作区**；沙箱子进程只在 `/openclaw/attachments/<uuid>/` 拿到**只读投影**；共享作用域沙箱与不支持只读资源投影的后端会在 staging **之前**就拒绝这次 spawn ⇒ 能力前置检查发生在落盘之前，不是先落盘再判。
- **正文脱敏与路径存续是两件事**：附件内容会自动从 transcript 持久化中脱敏，但文件本身仍以 `0700`/`0600` 权限存在；`cleanup=delete` 总是删除附件，`cleanup=keep` **只有在 `retainOnSessionKeep=true` 时**才保留 ⇒ 「已脱敏」不等于「已删除」，验收要分别确认两条路径。
- **退役的遗留路径不删也不遍历**：升级前暂存在子工作区 `.openclaw/attachments/<uuid>/` 的遗留附件，其 registry 记录退役时**既不删除也不遍历**那些文件；回执里的 `relDir` 是**保留下来的标识符，不是可用路径，不得解析** ⇒ 迁移类产物里那些看起来像路径的字段，要显式标注「不可解析」，否则下游会拿着它去读一个已经不存在的位置。


## 一次性链接「重发即吊销旧的」且带递增退避与双重限额；验收必须跑到重定向之后（来源：docs.n8n.io `security/enable-ssrf-protection.md` 3,822B + `security/block-specific-nodes.md` 2,425B + `basic-configuration/use-environment-variables/ssrf-protection.md` 7,039B + pipedream.com/docs `conduit/configure/access-control.md` 13,330B + `conduit/configure/scim.md` 9,789B，2026-10-03 r395C 独立 curl 取 `.md` 原文实拉；n8n 与 Pipedream 均经各自 `llms.txt`（287,049B / 34,240B）定位）

- **重发即吊销**：邀请链接只进受邀者的邮件（持有链接即证明其控制该地址），7 天有效；**重发会生成新链接并使旧链接立即失效**，管理员也可取消 ⇒ 这类链接的生命周期不是「到期」而是「被后继者作废」，验收时不能只看有没有过期。
- **重发退避递增 + 双重限额**：同一邀请的重发间隔依次为 1 分钟 → 5 分钟 → 30 分钟 → 2 小时 → 之后每天一次；工作区最多 200 个邀请，发送按管理员与工作区双重封顶 ⇒ 重发不是免费动作，退避表与限额要写进声明。
- **验收要跑到重定向之后**：SSRF 类防护把重定向目标与 DNS 解析一并纳入校验 ⇒ 「首跳被拦住」不等于「整条链被拦住」，只测第一跳的验收会漏掉 DNS rebinding 这条绕过路径。


## 审计事件目录是「能发出」的全集而非「已发生」的集合；归因空值多义；有 trace id 不等于可回溯也不等于可信身份（来源：pipedream.com/docs `conduit/use/api-reference/audit-log/get-audit-event-catalog.md` 9,011B + `.../list-org-audit-log.md` 11,642B + www.activepieces.com/docs `admin-guide/security/audit-logs/overview.md` 4,198B，2026-10-03 r396A 独立 curl 取 `.md` 原文实拉）

- **目录列的是能力，不是事实**：Pipedream 的审计事件目录返回的是**本构建能发出的事件命名空间树**，官方写明是让过滤 UI 能列出**「甚至尚未被记录过的事件」** ⇒ 「目录里有这个事件」不能证明它发生过，反过来「目录里没有」才是唯一能证明「不会被记录」的证据。覆盖面验收要拿代码里的 event schema 当真源，不能拿目录当台账。
- **归因字段的空值有成因，不是一种状态**：`actorUserId` 为空可能是匿名 actor、SCIM actor、system actor，也可能是**该字段存在之前写入的旧行** ⇒ 空值字段必须枚举它代表的每一种成因，否则「这条没有归属人」会被一律读成「匿名操作」，把系统动作与历史数据都误判成人的缺席。
- **有 trace id 不等于能回溯，也不等于身份可信**：官方注明该 trace **可能已因保留期从遥测后端消失，或从未被导出**；且 trace id 可以是调用方传入的（inbound traceparent 被采纳），**span id 才总是服务端生成的** ⇒ 「日志里有 traceId」既不能推出「能查到那次调用」，也不能推出「这段链路由本系统发起」。
- **审计记「尝试」而不记「输入」**：Activepieces 明确失败的尝试同样入账（errored attempt is still on the record），但 **agent 传给动作的值永不存储** ⇒ 审计能证明「谁在什么时间做了什么、成败如何」，不能用来复现输入；取证前先分清要的是行为证据还是输入证据。
- **覆盖缺口要写「为什么」，且真源在代码**：MCP server tool 完全不入审计，官方给的理由是**没有任何标记能区分它是读还是写** ⇒ 声明「不覆盖 X」时必须同时给出不覆盖的成因，否则下游无法区分「设计如此」与「漏记」；事件目录会随平台增长而加，**其真源是代码里的 event schema，不是文档目录**。

## 审计覆盖面要声明保留期与可见性分级；跨主体凭据使用必须可追溯（来源：help.make.com `audit-logs.md` 8,460B，2026-10-03 r405C 独立 curl 实拉；与 §审计事件目录是能发出全集不是已发生集合 互补——那条管"目录≠已发生"，本条管"覆盖面的两个维度：保留多久、谁能看见"，以及跨主体凭据归属）

- **保留期是覆盖面的隐性边界**：Make 明确审计日志存 12 个月 ⇒ 可追溯窗口=保留期，不是"永远能查"；声明审计覆盖面时必须把保留期写进覆盖面（超过期限=查不到，等同未记录）。
- **审计可见性按层级分级，下级缺事件**：组织级审计含全部事件，团队级审计**看不到组织变量等事件**（"Some events are NOT visible in team audit logs"）⇒ 审计"谁能看"本身分级，下级视图是上级的真子集，不能拿团队级日志当完整审计证据。
- **跨主体凭据使用要记录归属**：Make 记录 `Connection used belongs to someone else` / `Requested connection used` ⇒ 凭据被谁（非 owner）实际使用要入审计，与 §归因空值四义 互补：actor 与凭据 owner 可能不同主体，审计必须区分"操作人"与"凭据归属人"。
- **判不落**：事件类型枚举（who/what/when/which scenario）与 §审计事件目录是能发出全集 同族，仅作 Make 印证；Enterprise 专属特性（登记项）。

## 验收要报「通过率」与「通过但偏离率」双轴并带 Wilson 置信区间；检查项数≠根因数；拦截器双指标验收（拒断率 + 授权供给无损）（来源：Qoder r400-Q/r401-Q 审计净新，2026-10-03；对应 pipedream.com/docs `get-audit-event-catalog.md` 9,011B 本轮回拉印证「目录含未发生事件」）

- **通过率单轴会虚高，必须并报「通过但偏离规范」率**：评测/扫描器只报"通过率"会掩盖"形式上过了但偏离规范"的占比，小样本下尤其危险；两率都带 Wilson 置信区间，样本少时间隔宽、不拿点估计当结论。
- **检查项数≠根因数**：报"检查了 N 项"不代表覆盖了 N 个根因维度——检查项计数（如 6.34）和根因数（如 2.65）是两套数，覆盖面验收要标清"查了几项"与"对应几个根因"的区别，避免用项数冒充维度覆盖。
- **拦截器验收看双指标**：拒断率（被拦的里有多少真该拦）+ 授权供给无损（拦截的同时正常授权是否照样下发）；单看拒断率高会误以为严，实则可能把合法授权也掐了。
- 提升层：验收方法论。触发词：通过率双轴、Wilson CI、检查项数≠根因数、拦截器拒断率+授权供给无损。

## 审计事件名同词不同物会让「按名订阅」选错对象；自报字段不可当聚合键，聚合键必须自证稳定与校验（来源：docs.n8n.io `administer/observe-and-log/stream-logs-to-external-systems.md` 23,919B，2026-10-03 r408A 独立 curl 取 `.md` 原文实拉）
- **原文**：① 两组审计事件都提到包："Package installed/updated/deleted" 覆盖装在实例上的 **community nodes**；而 **n8n package** 事件覆盖「在实例间搬工作流的便携归档包」——文档明写 **Two sets of audit events mention packages, and they're unrelated**。② `subscribedEvents` 可写事件名或**组前缀**（`n8n.audit`、`n8n.workflow`、`n8n.audit.mcp` 一次订阅三个）。③ MCP 工具调用事件里，`clientId` 标识**一次客户端注册**，跨 token 刷新保持不变，**同一产品的两次安装会分别注册、拿到不同值**；`clientName` 是客户端自报的，**未经校验且不唯一，不能当 key**；`anonymizeAuditMessages` 只遮 email/name，**不遮 userId / authType / clientId**。
- **判据**：① **事件标识必须自陈作用域**——同名（package）指向两类对象时，按名字订阅会订阅到错误的那一类；验收「订阅是否生效」要先确认订阅到的是哪一个实体，而不是看有没有事件进来。② **组前缀订阅会一次性纳入新增成员**——订阅 `n8n.audit.mcp` 等于承诺未来新加的 MCP 事件也一并接收，这在合规留痕上是优点、在容量与噪声预算上是负债，选用前要明确自己要哪一种。③ **聚合键先问两件事：会不会变、有没有被校验**——`clientId` 跨刷新稳定且由服务端签发，可当键；`clientName` 自报且可重复，只能当展示。度量「某个产品用了多少次」时，`clientId` 数的是**注册数**而不是**产品数**，把两者混用会系统性高估。④ **脱敏声明必须同时给出保留清单**——只说「已脱敏」无法确定脱敏后还能不能归因；保留 `userId`/`clientId` 意味着仍可分组计数，验收要按保留清单逐项确认，而不是笼统认为「脱敏即不可关联」。
- **提升层**：可观测性 / 验证。触发词：审计事件同名不同物、组前缀订阅、clientId 稳定、clientName 不可当键、脱敏保留清单、注册数不等于产品数。

## 观测数据的入口归因要能区分内部流量与真实用量；数据搬走不等于查不到，但取回是另一条有时效的通道（来源：docs.dify.ai `en/cloud/use-dify/monitor/logs.md` 6,019B（经 `_llms/en/cloud.md` 16,454B 定位真路径），2026-10-03 r408B 独立 curl 取 `.md` 原文实拉）
- **原文**：① Chatflow/Workflow 的 **Preview 与 Test Run 测试会话被排除**在日志外；**其他应用类型的测试会话会被列出，且记在团队成员账号名下**。② **Trigger By** 四值：WebApp（「发布后的 web app，或**通过 API 的调用**」）/ Webhook / Schedule / Integration。③ **User Rate** 算终端用户赞踩、**Op. Rate** 算团队评分，两条**都跨整个会话聚合**。④ 工作流运行日志超过约三个月**移出 Logs 页**进**月度归档 ZIP**（`workflow_runs` / `workflow_app_logs` / `workflow_node_executions` / `workflow_node_execution_offload`（**超大节点输入输出单独存放**）/ `workflow_pauses`+`pause_reasons` / `workflow_trigger_logs` 六种 CSV）；归档**仅 owner/admin 可下载**，需先 **Prepare download（后台异步）**、按钮变 Download 后取，**准备好的下载只保留 24 小时**。
- **判据**：① **「是否被记录」对同一动作按应用类型分叉**——同样是试跑，一类被排除、一类被计入且归因到内部账号；按会话数统计用量时，内部流量混在里面且被当成真人 ⇒ 观测口径里「谁在用」必须先声明是否含内部账号，否则活跃度与转化率都被高估。② **标签粒度要问「这个标签吞掉了几种入口」**——`WebApp` 同时表示网页应用与 API 调用，用它统计「API 用量占比」会得到 0；归因维度要按**能否区分**来验收，而不是按有没有这个字段。③ **反馈分来源通道，不可合并计数**：终端用户反馈与运营方反馈是两列、语义不同（用户不满 vs 团队质检），且**聚合粒度是会话而非单条消息**；把一个会话级评分当成某条回复的评分会张冠李戴。④ **「满了就移走」要拆成三件事分别验收**：数据还在不在、在哪、怎么取回——归档不是删除，但**取回是两步异步产物且有效期 24 小时**，把「点了导出」当成「已取得数据」会在过期后才发现没拿到。⑤ **主记录里看不到完整输入输出是设计而非缺失**：超大节点 IO 被 offload 到独立文件，只看主表会以为字段为空；分析执行详情必须连 offload 表一起读。
- **提升层**：可观测性 / 验证。触发词：测试会话是否计入、内部账号污染用量、WebApp 吞掉 API、User Rate 与 Op. Rate、会话级评分、归档 ZIP 六种 CSV、offload 表、Prepare download 24 小时有效。

## 产物可达性由落点目录决定，且「上传」是一道单向门：持久 ≠ 可取回（来源：docs.bigmodel.cn `cn/managed-agents/files.md` 4,911B + `create-session.md` 6,625B，2026-10-04 r410B 独立 curl 取 `.md` 原文实拉；与 §跨轮持久性分三层 / §归档是搬走不是删除但取回为两步异步产物 互补——那两条管"留多久"与"归档后怎么取"，本条管"同一个文件系统里不同目录的可取回性不同"）
- **原文**：`Files API 覆盖两类用法：输入（把材料送进会话给 Agent 读）和产物（把 Agent 写出来的结果拿回来）`；`沙箱路径 /mnt/session/uploads，对 Agent 只读 / /mnt/session/outputs，读写`；`上传文件的 downloadable 为 false，不能再用 Files API 下载；只有写入 /mnt/session/outputs 后编目的会话产物可下载`；`写在 /workspace 的中间文件不会被编目，也无法通过 Files API 取回`；`等到 session.status_idle 再列出 outputs，避免文件还在写入`；`会话范围的 File 在 list/get 响应中带 scope 字段；组织级上传的 File 无 scope`。
- **判据**：① **持久性与可取回性是两个正交维度，别混着用**：`/workspace` 开了 checkpoint 后跨轮持久，但**永远不进 Files API**——"还在"不等于"拿得到"。验收产物时的正确问法不是"它还在不在"，而是"它在不在被编目的那个目录里"。② **上传是单向门**：上传动作产生的对象 `downloadable: false`，不能经同一 API 取回 ⇒ "把材料送进去了"与"还能拿回这份材料"是两件事；凡"送进去"的接口要连"能不能取回、怎么取回"一起设计。③ **编目是有范围的自动动作，不是事后扫描**：只有产物目录被自动编目，且**写入完成前就被列出会读到半写状态** ⇒ 列产物的时机要绑定到结束信号（此处 `session.status_idle`），不是"写完就列"。④ **同一个 File 对象在不同 scope 下权限不同**：组织级上传无 scope、会话产物带 scope ⇒ 判断一个文件能不能下载，看的是它属于哪一个作用域，不是它的类型。
- 提升层：可复用 Skill / 工具。触发词：产物落点决定可达性、uploads 只读、downloadable false、上传单向门、workspace 不编目、持久不等于可取回、等 status_idle 再列、scope 字段。

## 上下文量与超时预算必须同步放大；可选增强缺失时应「跳过本轮」而不是让主流程失败（来源：docs.openclaw.ai `concepts/active-memory/tuning.md` 4,601B，2026-10-04 r412C 独立 curl 取 `.md` 原文实拉；与 §产物可达性由落点目录决定 互补——那条管"产物放哪才拿得到"，本条管"可选的召回 / 增强环节在什么条件下该被放弃"）
- **原文**："Pick the **smallest mode that still answers follow-ups well**; grow `timeoutMs` as context size grows, from `message` to `recent` to `full`"（`message` 约 `3000`–`5000` ms，`recent` / `full` 约 `15000` ms 或更高）；"If nothing in that chain resolves, active memory **skips recall for the turn**."
- **判据**：① **输入量级变了，超时预算必须一起变**：把 3–5 秒的预算套在 `full` 模式上，表面症状是"召回慢 / 召回空"，真实原因是预算没跟上输入规模 ⇒ 这里的超时不是性能问题，是配置与输入不匹配；调超时之前先问输入量级变没变。② **可选环节失败要"跳过本轮"，不要"整轮失败"**：无可用模型 ⇒ 该轮不召回，主答复照常产出 ⇒ 增强件的价值低于主流程可用性；把可选增强做成硬依赖，等于让一个辅助能力的配置缺失升级成整体不可用。③ **最小可用上下文优先**：从 `message` 起步、按需升到 `recent` / `full` ⇒ 上下文不是"越多越保险"，多给的部分同时带来成本与噪声（召回风格随 mode 联动就是它的副作用）。
- 提升层：工作流 / 工具。触发词：上下文与超时同步、timeoutMs 随模式放大、可选增强跳过本轮、最小可用上下文、增强件不做硬依赖。
