---
name: wb-debug-loop
description: >-
  有纪律的排障循环（诊断 bug / 报错 / 性能回归的根因）。当出现报错、崩溃、白屏、500、超时、测试失败、行为与预期不符、构建/部署跑不起来、性能变慢、内存泄漏、复现不了的怪问题时应用：重现 → 最小化 → 假设 → 验证 → 修复 → 回归测试。禁止"先改再猜"、禁止一次改多处、禁止靠重启/清缓存糊过去。另含「修复验证」：补丁是待验证假设，不从 diff 大小/作者/上游一致/原 PoC 失效推成功，须测同根因变体与兄弟路径。触发词：报错、错误、异常、崩溃、闪退、白屏、跑不起来、不生效、没反应、失败、失败原因、找不到原因、查不出、定位、排查、排障、根因、复现、回归、性能变慢、卡顿、内存泄漏、超时、内存溢出、debug、troubleshooting、root cause、stack trace、崩溃日志、模型行为、幻觉、选型、补丁、修复验证、patch、变体、这算 bug 吗、加固算修复吗、兜底不是修复、重试掩盖、静默降级、缓解不是修复、改指令算修了吗、装了不生效、静默失败、幻影字段、声明但未写入。不适用：只是"该不该写这段代码"的取舍（走 wb-ponytail）、多步实现任务的规划与交付（走 wb-spec-driven）、任务级"点名目标全量覆盖 / 失败换路攻坚"纪律（走 wb-execute-discipline）。、一直在重复、转圈、卡死检测、迭代上限定多少、并行单元重名、工具结果用错、喂给判定的字段要人话、验证证据要让外行能下结论、先找仓库既有规程、失败声明、failure cause、只报原因不报对策、分类不出就原样抛、等待提示、错误负载缺省字段、OOM 恢复、中断恢复、取消不等于丢弃、半成品保留、完成标记游标、重试准入、重试不生效、参数冲突、单次超时与总时长、重试留痕、兜底范围、提前终止原因、结束原因可见、主动退出留痕、诊断只读、修复须批准、diagnose不执行repair、读写分离、终态退出码、超时携带诊断、失败不二次变更、幂等护栏、轮询分批、卡住运行恢复
version: "1.182.0"
agent_created: true
---

# wb-debug-loop（排障：按纪律走，不靠猜）

来源：mattpocock/skills 的 `diagnose` 技能（重现 → 最小化 → 假设 → 工具 → 修复 → 回归测试）+ 通用调试纪律。提纯为本地循环。

**核心判断：改不动的 bug，几乎都是"还没复现就先改了"。** 定位是证据工作，不是灵感工作。

> 正文预算管理：「数据钉定（input pinning）与局部执行（partial execution）：」（全文已零删减下沉 references/knowledge-base.md §下沉·数据钉定（input pinning）与局部执行（partial execution）：）
> 正文预算管理：「读侧先行的灰度升级律；原文已下沉 references/knowledge-base.m」（全文已零删减下沉 references/knowledge-base.md §下沉·读侧先行的灰度升级律；原文已下沉 references/knowledge-base.m）
## 「之前照做的规则现在不照做了」先查修剪，再怀疑模型（来源：agentskills.io《How to add skills support to your agent》客户端规范 2026-09-28 r284-A 独立实拉 + arXiv 2606.22528《Governance Decay》独立核验；与 §上下文随循环增长要修剪 互补——那条是主动写减法，本条是被动排障归因）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·r439·之前照做的规则现在不照做了先查修剪再怀疑模型来源ag）

> 正文预算管理：「诊断输出要分「给人看的粗桶」与「给机器读的稳定原因码」两层；先分清「根本没发出调用」还是」（全文已零删减下沉 references/knowledge-base.md §下沉·诊断输出要分「给人看的粗桶」与「给机器读的稳定原因码」两层；先分清「根本没发出调用」还是）
## 超时不是一个数：默认值随触发类型分档、可调上限随套餐分档（来源：pipedream.com/docs/workflows/limits 2026-09-29 r296-C 实拉）；原文已下沉 references/knowledge-base.md §超时分档下沉，2026-10-04 r411A（全文见 references/knowledge-base.md §下沉·超时不是一个数默认值随触发类型分档可调上限随套餐分档来源pipedreamcomdocswork）

## 已处理的失败是「独立可见状态」（Warning 态），不是消失了；重试有固定序列且超限会熔断关停调度（来源：help.make.com《Introduction to errors and warnings》+《Exponential backoff》2026-09-29 r337-Q-A 实拉核验；与 §重试掩盖 互补——那条管"别用重试糊过去"，本条管"重试本身有几条纪律"）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·已处理的失败是独立可见状态Warning态不是消失了重试有固定序列且超限会熔断关）
## 判死前先回查真实执行状态，别把「无信号」直接当「已失败」（来源：n8n 2.41.0 release note「Recheck the execution status before failing a stalled queue job」github.com/n8n-io/n8n/releases 2026-09-29 r334-Q-A 实拉核验；与 §心跳误杀 分工——那条管"心跳为什么发不出去"，本条管"判死这个结论本身要先验证"）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·判死前先回查真实执行状态别把无信号直接当已失败来源n8n2410releasen）
## 超时不是回滚授权：判死与回滚是两个门；只有「已验证回滚」才交回前一代，且与分诊互不自动触发（来源：docs.openclaw.ai cli/update repair-and-recovery，2026-09-30 r320A 实拉）（细则见 KB，2026-09-30 r320C 下沉）（全文见 references/knowledge-base.md §下沉·超时不是回滚授权判死与回滚是两个门只有已验证回滚才交回前一代且与分诊互不自动触发来源docsop）

## 重试钉在单请求而非复合流、已完成步不重放；「已发出无应答」是歧义态须先对账；内层重试独立计数且外层可掐断；鉴权/计费/拒答不进重试预算直接走降级（来源：docs.openclaw.ai/concepts/retry，2026-09-30 r321B 独立实拉 9,854B；细则见 references/knowledge-base.md §r321B）（全文见 references/knowledge-base.md §下沉·重试钉在单请求而非复合流已完成步不重放已发出无应答是歧义态须先对账内层）
## 「恰好一次」的成立前提是在途时间有上界：只靠验证/对账在 late commit 下永远达不到，重尾时等待无效、须给每个写发幂等键；崩溃-恢复要查执行痕迹计数而非看结果（来源：arXiv 2609.29095，2026-09-30 r322C 独立实拉 44,254B，重复率 56%/74%、契约解释 81%；细则见 references/knowledge-base.md §r322C）（全文见 references/knowledge-base.md §下沉·恰好一次的成立前提是在途时间有上界只靠验证对账在latecommit下永远达不到重尾时等待无效须）

## 自述成功不构成幂等证据：重复执行中九成 agent 仍自报成功；引量化结论前先确认分子分母（来源：arxiv.org/abs/2609.29095，2026-09-30 r323B 独立实拉 44,254B）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·自述成功不构成幂等证据重复执行中九成agent仍自报成功引量化结论前先确认分子分）
## 兜底链路可能与故障链路同源：错误工作流默认指向自身、同一兜底可被多条主链路共用，且手动运行不触发——兜底能否工作无法用演练路径验证（来源：docs.n8n.io errortrigger 节点页 822,401B + flow-logic/error-handling 596,446B，2026-09-30 r324C 独立复拉命中「uses itself as the error workflow」×2、「can't test error workflows」×1、「same error workflow for multiple workflows」；与 §超时不是回滚授权 互补——那条管“判死与回滚分两门”，本条管“兜底自己会不会一起死”；细则见 references/knowledge-base.md §r324C）（全文见 references/knowledge-base.md §下沉·兜底链路可能与故障链路同源错误工作流默认指向自身同一兜底可被多条主链路共用且手动运行不触发兜底能）

## 异步入口的丢失窗 =「回执与落库之间」那一段：已应答的请求不会有人重试；有重建路径的子系统，陈旧备份严格劣于空库（来源：www.activepieces.com/docs/install/guarantees/disaster-recovery.md，2026-09-30 r325A 独立 curl 实拉 7,611B 逐串命中；经 Qoder r357-Q-A 提名）（全文见 references/knowledge-base.md §下沉·异步入口的丢失窗回执与落库之间那一段已应答的请求不会有人重试有重建路径的子系统陈旧备份严格劣于空）

## 慢的外部依赖不得阻塞冷启动：连接与刷新各给一个独立上界，超时只降级不阻塞；启动期对未就绪依赖 fail-closed，刷新期旧值继续供给（来源：docs.n8n.io `/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/external-secrets.md` 4,588B，2026-09-30 r325B 独立 curl 实拉逐串命中，**通道更正**：Qoder 给的 `docs.n8n.io/use-environment-variables/external-secrets.md` 实际返回「Page Not Found」壳，真实前缀须经 `docs.n8n.io/llms.txt`(286,271B) 定位；经 Qoder r358-Q-B 提名）（全文见 references/knowledge-base.md §下沉·慢的外部依赖不得阻塞冷启动连接与刷新各给一个独立上界超时只降级不阻塞启动期对未就绪依赖fail-）

## 并发闸门有作用域：「已开限流」≠「全链路受控」，且队列项不可重试（来源：n8n control-concurrency 本机实拉，r326B）（全文见 references/knowledge-base.md §下沉·并发闸门有作用域已开限流全链路受控且队列项不可重试来源n8ncontrol-concurrenc）

## 诊断技能严格只读、修复须经批准：diagnose 与 repair 是分离的两动作（来源：docs.openclaw.ai/tools/custodian-skills.md 5,298B，2026-09-30 r336A 独立实拉）（全文见 references/knowledge-base.md §下沉·诊断技能严格只读修复须经批准diagnose与repair是分离的两动）
## 并发互斥的锁键必须是「执行身份」而不是调用通道或运行时形态；队列满有三档背压语义；旁路维护失败不得替换已完成的回复（来源：docs.openclaw.ai/concepts/queue.md 17,920B + concepts/compaction.md 17,978B，2026-10-01 r340A 独立 curl 实拉逐串命中）（全文见 references/knowledge-base.md §下沉·并发互斥的锁键必须是执行身份而不是调用通道或运行时形态队列满有三档背压语义旁路维护失败不得替换已完成的回复来源docso）

## 改向/取消的生效边界是「原子发射检查点」；落盘不等于已被消费；「调用被跳过」不能反推「有用户输入在等」；能力缺失应降级为等待而非失败（来源：docs.openclaw.ai/concepts/queue-steering.md 12,366B + concepts/memory.md 15,623B，2026-10-01 r340B 独立 curl 实拉逐串命中）（全文见 references/knowledge-base.md §下沉·改向取消的生效边界是原子发射检查点落盘不等于已被消费调用被跳过不能反推有用户输入在等能力缺失应降级为等待而非失败来源do）
## 降级是回合局部的；受理后台维护不等于清理完成（来源：docs.openclaw.ai/concepts/context-engine.md 26,167B，2026-10-01 r343A 独立 curl 实拉逐串命中）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·降级是回合局部的；受理后台维护不等于清理完成）
## 配置写入分运行时覆盖与持久两档；异步写失败不回滚已生效的会话选择（来源：docs.openclaw.ai/tools/slash-commands.md 38,378B，2026-10-01 r343B 独立 curl 实拉逐串命中）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·配置写入分运行时覆盖与持久两档；异步写失败不回滚已生效的会话）
## 配置意图要三参数分立：设置值 / 显式置空 / 清除覆盖；吊销不因重新启用而回溯（来源：docs.openclaw.ai/automation/cron-jobs/payloads.md 27,960B，2026-10-01 r343C 独立 curl 实拉逐串命中）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·配置意图要三参数分立：设置值 / 显式置空 / 清除覆盖；吊）
## 失败恢复有两条硬边界：回滚资格按「是否事务模块」封闭枚举，且重试耗尽可级联改变自动化生命周期（来源：help.make.com/rollback-error-handler.md 8,865B + exponential-backoff.md 2,779B + docs.n8n.io/.../executions.md，2026-10-01 r348A 独立 curl 实拉）
- 原文：①「Modules that support transactions are labeled with the 'ACID' label.」②「Auto-commit enabled — Only the module that produced the error can revert its changes.」③「Auto-commit disabled — All changes made during the bundle's execution across every transaction-supported module can be reverted.」④「If the 8th attempt fails, Make disables scheduling of the scenario.」⑤第二证 `N8N_WORKFLOW_AUTODEACTIVATION_MAX_LAST_EXECUTIONS=3`。
- 判据：① **回滚范围不是「尽量回滚」，而是按模块是否事务（ACID 标签）封闭枚举** —— 非事务模块的改动失败后仍然留着。⇒ 任何「出错就回滚」的承诺都必须先回答哪些改动真的可回滚；把不可回滚的算进去，验收时会得到「回滚成功了但状态还是脏的」。② **提交模式反转回滚粒度**：Auto-commit 开=只有出错模块回滚；关=整个 bundle 跨全部事务模块回滚。粒度更粗的那一档不是更好，而是失败时影响面更大，要与业务的原子性需求对表。③ **重试耗尽不止是这次失败**：它可以直接改自动化本身（停用调度）。⇒ 排障「这条自动化怎么不跑了」时，先看是不是先前的重试耗尽把它关掉了，而不是查触发器与权限。
- 提升层：工作流。触发词：ACID 标签回滚资格、Auto-commit 反转回滚粒度、只有出错模块可回滚、重试耗尽停用调度、AUTODEACTIVATION。

## 同一个错误的默认处置会随调度形态分岔；重试资格要按错误类别封闭列举，不靠「看起来可重试」（来源：help.make.com/fix-rate-limit-errors.md 9,275B + docs.dify.ai/en/api-reference/guides/errors.md 3,157B，2026-10-01 r348A 独立 curl 实拉）
- 原文：①同一 `RateLimitError`（429）无 handler 时：定时触发=「pauses the next scenario run for 20 minutes」；即时触发=「reruns the incomplete execution from its start with exponential backoff」。②Dify：「Retry with backoff: `too_many_requests`, `500`, and network failures」vs「Don't retry as-is: validation errors (fix the request first), authorization failures, or quota errors (they won't clear until the quota does)」；`code` 是稳定分支键，`status` 只镜像 HTTP。
- 判据：① **跨调度形态的默认值不可假设一致**：同一个 429 在定时/即时两条路径上的默认动作完全不同（暂停 20 分钟 vs 从头指数退避）。⇒ 写重试/兜底策略时先问这条路径的调度形态是什么，否则同一种错误会得到两种完全不同的用户体验。② **重试资格要写成两张封闭清单**（可重试 vs 不可原样重试），而不是一个「是否重试」布尔：配额类错误在配额刷新前重试纯属浪费，鉴权/校验类不改请求重试必然重复失败。③ **分支键取稳定字段**：用业务 `code` 分支，不要用镜像 HTTP 的 `status` —— 后者会随传输层重映射漂移。
- 提升层：工具/工作流。触发词：429 定时暂停 20 分钟、即时指数退避、同错误分岔、重试白名单黑名单、配额错误不重试、code 稳定分支键、status 只镜像 HTTP。

## 背压要先分「丢弃式 / 阻塞式」两档并显式写出；限流的作用面按触发类型分轨（来源：pipedream.com/docs/concurrency-and-throttling.md + docs.n8n.io `/scaling/control-concurrency.md`，2026-10-01 r348A 独立实拉）
- 原文：①「fixed window throttling」、`limit=0` 即关队列、「exceeds the queue size, events will be lost」。②队列仅对 event-driven 生效，「excluding native HTTP or cron types」。③第二证：n8n 并发上限「applies only to production executions」，显式不含 manual / sub-workflow / error / CLI。
- 判据：① **背压有两档且代价相反**：丢弃式（队列满即丢事件，吞吐让位于内存）与阻塞式（反压上游，延迟换不丢）。⇒ 选型时先声明是哪一档；混着用会出现「既延迟又丢事件」的最坏组合，而日志上两者都只是「慢」。② **`limit=0` 这种取值要显式识别** —— 它不是队列无限，而是队列不存在，溢出直接丢。③ **限流/并发上限必须点名覆盖哪些触发类型**：只覆盖事件驱动、不覆盖 HTTP/cron/子工作流/手动/错误工作流是默认形态。⇒ 排「限流没生效」时先核对触发类型在不在作用域内；恰好漏掉兜底错误工作流与被复用子工作流，是最常见的失效面。
- 提升层：工作流。触发词：丢弃式背压、阻塞式背压、events will be lost、limit=0 关队列、限流按触发类型分轨、生产执行才限流、子工作流不在并发上限内。

## 「我在改的东西会不会被在途同步覆盖」要按锁的覆盖范围判，不按我的操作意图判（来源：docs.openclaw.ai/gateway/openshell.md 25,346B，2026-10-01 r348A 独立 curl 实拉）
- 原文：①「External editors and other Gateway processes do not participate in that lock」—— mirror 模式的锁只覆盖同一 Gateway 进程内的 upload→command→download。②「symlinks, FIFOs, or Unix sockets, into either workspace」永不复制。③清理失败须保留 runtime registry 条目供 recreate/prune 重试，明令勿靠删 registry 或切 workspace 隐藏失败。④`timeoutSeconds:120` 但 sandbox 创建保底 ≥300s。
- 判据：① **锁的作用域不等于「所有会碰这个文件的人」**：进程外的编辑器与宿主进程不参与锁，因此运行中的镜像命令在 download 阶段可以覆盖外部编辑。⇒ 「我刚改的怎么没了」这类问题的判据是谁参与这把锁，不是我改的时候有没有人看着。② **清理失败要留下可重试的把柄**：删沙箱失败时保留 registry 条目，是为了让 recreate/prune 还能找到它；靠删记录或切工作区让错误消失，等于把可重试故障变成不可见孤儿。③ **超时分档要按阶段看**：执行超时与创建保底是两个数值，用执行超时去估创建等待会误判卡死。
- 提升层：工作流。触发词：锁不覆盖外部编辑器、download 覆盖外部编辑、清理失败保留 registry、勿隐藏失败、symlink 不跨同步、创建保底超时。

## 分叉结构的「并行性」与「可合并性」都不对称，不能按图形外观推断（来源：help.make.com/router.md 6,347B + if-else-and-merge.md 19,001B，2026-10-01 r348B 独立 curl 实拉）
- 原文：①「modules connected to a router run **sequentially, not in parallel**」；②同页对照表：`can be merged back together with a Merge module` vs `Routes can't be merged back together`。
- 判据：① **看到扇出就假设并行，是「跑得挺快但结果对不上」类 bug 的误判源头**：同一种图形，在一种节点类型下是顺序执行。⇒ 排障前先确认分叉节点类型，再谈并行；性能预期与正确性预期都要按节点语义而非连线形状来定。② **两种分叉的合并能力不对称是结构事实**：router 分支不可在下游合并，if-else 分支可以。⇒ 不能把一种分叉的收束手法迁移到另一种；「聚合」这个词在同一系统里至少三种语义（顺序聚合 / 按到达顺序收带上限 / 任一分支为空即不产出），引用时必须点名是哪一种。
- 提升层：工作流。触发词：router 顺序非并行、扇出不等于并行、Routes 不可 merge、if-else 可 merge、聚合三种语义。

## 观测面可损、重放面必精：「看不见」不等于「没存」（来源：docs.n8n.io `/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions.md` 13,422B，2026-10-01 r348C 独立 curl 实拉）
- 原文：「For larger executions, n8n omits the data (shown as **too large to display**)」+「**Doesn't affect retrying or resuming executions, which always load the full data**」；`EXECUTION_DATA_MAX_DISPLAY_SIZE` 默认 104857600。
- 判据：① **展示截断与存储完整是两个不同的面**：观测面为了不把低资源实例拖垮而省略大数据，但重试/恢复永远加载全量。⇒ 「界面上看不到数据」不能推出「数据没存」；排障时把「取不到数据」至少分成三支 —— **没存 / 没到（写入未成功）/ 该面故意不可访问**，逐支验证而不是直接判丢。② **阈值是配置项而非固定行为**：`MAX_DISPLAY_SIZE` 可调，同一个现象在不同实例上成因不同。⇒ 报「这里显示 too large」时先读当前配置值，再判是不是容量问题。
- 提升层：工作流/可观测性。触发词：观测可损重放必精、too large to display、看不见不等于没存、取不到数据三分支、MAX_DISPLAY_SIZE。

## 运行期组件健康位与宿主健康态分离：被调组件降级只让「该执行面」失败，宿主整体继续跑（来源：help.make.com/on-premise-agent.md 17,056B，2026-10-01 r349A 独立 curl 实拉，`every four minutes` / `associated scenarios still run` / `500 error` 逐串命中；经 Qoder r366-Q-A 提名）
- 原文：①「Make checks its activity **every four minutes**」；②「When in **Not responding** status, **associated scenarios still run**, but the module using the On-prem agent shows a **500 error**」。
- 判据：① **宿主健康 ≠ 被调组件健康**：组件失联时场景整体照跑，只有用到它的那个模块报错 ⇒ 排障要问「报错落在哪一层」，而不是看整体是否在跑；把「整体在跑」当作依赖健康的证据会漏掉单点降级。② **降级要落到具体执行面**：健康位是每组件独立的，一个组件 Not responding 不应升级为全局停 ⇒ 先定「哪些执行面会因该组件失败」，再定告警粒度。③ 与既有「慢依赖不阻塞冷启动」（启动期）互补：本条是**运行期**。④ 心跳周期（4 分钟）决定失联判定延迟，别把它当实时信号。
- 提升层：工作流。触发词：组件独立健康位、Not responding、降级只失败该执行面、宿主照跑、心跳 4 分钟、运行期降级。

## 「查不到状态变化」先核默认作用域键是不是资源 ID：同一资源的所有调用共用一个会话/状态桶（来源：docs.langflow.org/memory 56,213B，2026-10-01 r349B 独立 curl 实拉，`default session ID is the flow ID` 逐串命中；经 Qoder r367-Q-B 提名）
- 原文：「The **default session ID is the flow ID**, which means that all chat messages for a flow are stored under the same session ID as one large chat session」。
- 判据：① **默认归属键是资源 ID 而不是使用者 ID**，是一个静默的共享面：不同用户在同一流程上的对话会互相污染记忆、串数据、并把审计归因错到「同一个主体」。② **症状 → 成因要分三档**：串数据（记忆污染）/ 审计归因错（主体不可分）/ 状态莫名被重置（作用域比预期宽）⇒ 排障第一步是问「这个状态的默认键是谁」，而不是先改 prompt。③ 与既有「解析基准 ≠ 隔离边界」互补：那条管路径解析，本条管**状态/会话的默认归属键**。
- 提升层：工作流。触发词：默认 session ID 是 flow ID、作用域键是资源 ID、记忆污染、串数据、审计归因错、共享会话桶。

## 挂起态是双字段：状态位只回答「态」，原因与恢复入口在独立实体；恢复去重的正确原语是存储唯一约束（来源：www.activepieces.com/docs/install/architecture/waitpoints.md 7,102B，2026-10-01 r349B 独立 curl 实拉，`only carries status` / `the *why* lives on the waitpoint` / `never processes a resume twice` / `10 000 is also the ceiling` 逐串命中；经 Qoder r367-Q-B 提名）
- 原文：①「The flow run row **only carries status** (`PAUSED`, `RUNNING`, …); the ***why*** lives on the waitpoint」；②「Duplicate callbacks are absorbed by the **uniqueness constraint**; the engine never processes a resume twice」；③「**10 000 is also the ceiling**: the env var cannot raise it higher」。
- 判据：① **状态位不是原因位**：把「为什么等」压进状态枚举，会在复挂/多因等待时信息不够 ⇒ 等待必须有独立持久实体承载原因与恢复入口。② **去重要落在存储的唯一约束上，不是应用层判重**：应用层判重有并发窗口，唯一约束没有；「重复回调被唯一约束吸收」给出的是**键位实现**，比「记得判重」可靠。③ **要区分可调上限与已封死上限**：10 000 是 env 也抬不上去的硬顶 ⇒ 已封死上限应写进容量规划，别把 env 当逃生口。
- 提升层：工具/工作流。触发词：挂起态双字段、waitpoint 承载原因、唯一约束去重、重复回调吸收、已封死上限、10 000 ceiling。

## 重放默认跑在「最新代码」上：可复现取证必须显式钉住原运行版本（来源：pipedream.com/docs/workflows/building-workflows/inspect.md 2,607B，2026-10-01 r349C 独立 curl 实拉，`replays** the event against the newest version of your workflow` 逐串命中；经 Qoder r368-Q-C 提名）
- 原文：replay「**replays the event against the newest version of your workflow**」（保序）。
- 判据：① **默认把事件与代码版本解耦**：重放通过只能证明「用现在这份代码能跑通这个事件」，**不能证明当时那次执行是正确的** ⇒ 取证/复盘类重放必须显式钉原运行版本，否则「重放通过」会被误当成历史结论。② 与既有「观测可损、重放必精」同族：那条讲**数据完整性**，本条讲**代码版本绑定**。③ 自愈/续跑也有预算（openclaw `concepts/session.md` 22,390B，`budget` 命中，耗尽后换新会话身份而非无限救旧）⇒ 「救回来」不是无成本的默认选项。
- 提升层：工作流。触发词：重放跑最新代码、事件与代码版本解耦、钉原运行版本、取证重放、自愈预算耗尽换新会话。

## 调度面「防惊群」与「漏扫记账」是两件相反极性的事：默认抖峰，漏扫按已完成记账不补跑（来源：docs.openclaw.ai/automation/cron-jobs/schedules.md 15,917B，2026-10-01 r349C 独立 curl 实拉，`stagger` ×5 / `catch-up` / `fire: true` ×3 逐串命中；经 Qoder r371-Q-C 提名）
- 原文：①密集周期默认 **stagger**（随机抖动）防惊群、可显式关闭；②漏扫走 **catch-up** 路径，补录计数为已完成、异常不自滚而交退避队列；③gate 脚本仅当输出 `fire: true` 才触发执行。
- 判据：① **防惊群是默认开启的性能保护**（stagger），但它同时意味着「周期不再精确」——需要精确时刻时必须显式关闭抖动，而不是假设周期严格。② **漏扫不补跑、只记账为已完成**：与既有「misfire 重放」是**相反极性**的两条（一个重放、一个记账），引用时必须点名当前系统的选择，否则「漏了会不会补」两种预期都会错。③ **评估默认静默、触发须显式放行**（`fire: true`）：gate 脚本输出非 true 一律不触发 ⇒ 「脚本跑了但没执行」的正确怀疑方向是 gate 输出，不是调度未触发。
- 提升层：工作流。触发词：stagger 防惊群、漏扫 catch-up 记账、fire:true 才触发、gate 默认静默、周期不精确。

> 正文预算管理：「r350A · 关闭序钩子的超时语义：限时的是调用方等待，不会取消 handle」（全文已零删减下沉 references/knowledge-base.md §下沉·r350A关闭序钩子的超时语义限时的是调用方等待不会取消handler来源docsopenclawaiautomatio）
## r350A · 并发容量要选一个"货币"并按占用时长计量，耗尽按触发类型三路分叉（来源：help.make.com/parallel-capacity.md，2026-10-02 r350A 实拉 9,462B）

- **★并发上限必须用统一货币计量，且按"运行期间持续占用"计**：Make 用 PU（Processing Units），每次运行期间占住、结束即释放；处理大数据的运行全程占多个 PU。判据：**并发配额是"占用时长 × 单份重量"的积分，不是"次数"**——同样跑 N 次的两个场景，占的容量可以差很多。
- **★容量耗尽的处理按触发类型分叉**：即时触发（无 webhook 响应模块）→ 排队，容量可用再处理；定时触发 → 延迟下一次定时运行（**不排队补跑**）。判据：**"延迟"与"丢弃/排队"是三种不同后果**，设计背压前必须明确本次走哪条。
- **★监控要能同时看"余量"和"形状"**：堆叠条按场景上色（每根柱一个时点、每色一个场景），Y 轴有 Full capacity（看剩余余量、触顶线=该时刻被延迟或拒绝）与 Fit to usage 两种刻度；拉长到数天才能看出周期性峰值（夜间同步/周报）。判据：**只看峰值不看按场景堆叠，定位不到是谁打满的；只看短期看不出周期峰**。
- 提升层：工作流 / 工具。

## r350B · 恢复路径由"失败分类"路由，重试不是第一招（来源：docs.openclaw.ai/concepts/model-failover，2026-10-02 r350B 实拉 319,996B）

- **★先判失败类别，再选恢复手段**：临时性限流/供应商故障 → 有界同模型恢复（重试，重试状态带 wait 与 attempt 计数）；供应商在 failover-worthy 错误下耗尽 → 轮换 auth profile / 冷却规则 → 才推进到候选链上的下一个模型。判据：**重试是"同一配置下再试一次"，轮换与降级是另一档动作**，混用会让"换了模型才碰巧成功"被记成"重试有效"。
- **★有些失败必须保留原分类、不得改参数重试**：模型/账户限制、以及"与该请求无关的 unsupported option"，保持原始失败分类并按 fallback 策略走；文档明确 **不会用关闭 thinking 的方式对这类错误重试**。判据：**为了跑通而悄悄降级请求参数 = 把失败伪装成成功**，归因时必须留原分类。
- **★候选链由"选择来源"决定**：配置默认值、cron 主模型、自动选中的 fallback 各自可用不同的 fallback 策略。判据：**同一模型在不同选择来源下，可用降级路径不同**——排查"为什么这个任务没有降级"先看它从哪条路径选中的模型。
- 提升层：工具 / 工作流。

## r350B · 执行序的隐性来源：几何位置与版本分叉（来源：docs.n8n.io/build/flow-logic/understand-execution-order，2026-10-02 r350B 实拉 515,463B）

- **★分支执行序随版本语义分裂**：n8n 1.0 之前 = 逐层推进（所有分支的第 1 个节点 → 再所有分支的第 2 个节点）；1.0 起 = 逐分支跑完（一个分支到底再下一个）。判据：**"多分支谁先跑"不是规范保证的常量**，升级运行时可能静默改写业务时序。
- **★分支顺序取画布几何**：自上到下，同高度则左优先；可在工作流设置里改。判据：**画布布局是执行序的一部分**——拖动节点会改变运行语义，代码评审看不出来。
- 排查顺序：出现"偶发时序错乱" → 先确认运行时版本与执行序模式 → 再看画布几何 → 最后才看业务代码。
- 提升层：工具 / 工作流。

> 早期三节（r350B 保序与并发 / r350C 限流多组预算 / r350C 重试粒度与失败类别预算）已零删减下沉至 references/knowledge-base.md 的 r417-dl 存档节。
## r351B · 扩展点是"观察者"不是"拦截器"：写入成功 ≠ 投递成功（来源：docs.openclaw.ai `automation/hooks/writing-hooks.md` 10,721B，2026-10-02 r351B 独立 curl 实拉逐串命中）

- **★返回值三不：不阻塞、不取消、不改写**：原文 "Returned values **do not block, cancel, or rewrite** the operation."。判据：排障时别把事件钩子当成熔断/拦截点——想在钩子里"返回 false 掐掉这次操作"是无效设计；真要拦截必须走宿主提供的专用否决通道。**这条决定了"为什么我的钩子没生效"的第一类答案：生效了，但它本来就没有阻断权。**
- **★context 是观测快照，唯一可写例外要显式点名**：原文 "Treat context as an **observation, not a live state-editing API**... **patch events carry cloned snapshots**. The **explicit mutable exception** is `agent:bootstrap`'s `context.bootstrapFiles`."。判据：**往 context 里改字段默认不产生任何效果**（且 patch 类事件给的是克隆副本），只有被点名的那一个例外可写。排查"改了没反应"时，先确认写的是不是那个唯一例外。
- **★同一个写入点，投递语义按生产者分档**：`event.messages` 原文 "is **not a general send-message API**"——表列四档：chat 命令会 await 并尝试回复；Gateway 会话 reset/create 的 RPC "messages are **not routed as chat replies**"；压缩事件交给调用方的回调投递；**其余核心事件（含 `/stop`、自动 reset、bootstrap、patch、Gateway 生命周期）"Ignored as replies"**。判据：**推送成功不等于送达**；且"缺失收件人/不支持的路由/发送策略/投递失败"任一都能让回复静默消失。
- **★时序早于 settle 才算数**：原文 "Append messages **before the handler's promise settles**; detached work that pushes later can **miss the producer's delivery step**."。判据：异步尾巴里补写的消息会静默丢失——这类丢失无任何报错，是典型的"偶发不发"根因。
- **★禁用 ≠ 移除，放置 ≠ 生效**：原文 "**Disabling leaves the files in place**"；放 workspace 目录的钩子须显式启用，且 "Workspace placement is **not an agent sandbox or a guarantee that the Gateway will load** that workspace's hooks"。判据：排查残留行为时，被禁用的钩子文件仍在磁盘上（可能被别的机制重新发现）；排查"没加载"时，先查放置位置是否被宿主承认，而不是查代码逻辑。
- 排障顺序：① 该扩展点是否有阻断权 → ② 写的是否为唯一可写例外 → ③ 该生产者是否把这次写入计入投递 → ④ 写入发生在 settle 前还是后 → ⑤ 文件是否被宿主发现（放置位）与被启用（禁用留文件）。
- 提升层：工具 / 工作流。触发词：返回值不阻塞、观察式契约、唯一可写例外、克隆快照、写入不等于投递、settle 前写入、禁用留文件、放置不保证加载。

## r352B · 重放的两副面孔：它跑的是「旧输入 + 当前版本」，且变量取当下值不是当时值（来源：help.make.com `scenario-run-replay.md` 9,556B，2026-10-02 r352B 独立 curl 实拉逐串命中；与 §数据钉定 / §局部执行 互补——那两条管"把输入钉住、把范围收窄"，本条管"拿历史真实输入重跑时到底复现了什么"）

- **★重放 = 旧触发数据 × 当前版本代码，且流经全部模块**：原文 "a **current version** of a scenario runs using the **trigger data of a previous run**… That data **passes through all modules, even those that ran successfully**."。判据：**重放验证的是"修好的新版本能不能吃下旧输入"，不是"复现当时那次失败"**；而全模块重跑意味着**原本成功的副作用（发信、写库、计费）会被再执行一次**——回填型重放必须按副作用清单过一遍，调试型重放则应收窄到待测段（走 §局部执行）。与 §已完成步不重放 不矛盾：那条禁止的是"整流重试"把成功步重跑，本条说的是回填场景**故意**全跑，代价要显式认。
- **★重放不是时光机：可变量取"最新值"而非当时值**：原文存三样 = trigger output data / scenario inputs / "**the most up-to-date** variable value (**values from previous runs are not preserved** if updated during or since these runs)"。判据：**输入被快照了、环境没被快照**——凡依赖全局变量/配置/外部状态的流程，"同样输入跑出不同结果"不要先怀疑代码，先确认这些可变量在这期间变过没有。想要真正可复现，必须把可变量一起钉进快照，光留触发数据不够。
- **★重放能力要附「不可重放清单」与分场景入口**：原文 "**Run cannot be replayed**" 因两类 run 不入库——**Check run**（轮询触发器无新数据的检查运行）与 **Single module run**。入口分两个：Builder 内 *Run with existing data* 用于边建边测，History / Run details 里 *Replay run* 用于错误恢复与数据回填（不需要进 Builder）。判据：**声明"哪些运行没有存"与"从哪进"是重放功能的一部分**；排查"为什么这条不能重放"时，第一件事是核它是不是那两类不入库的运行，而不是查权限。
- 排障顺序（重放相关）：① 这次重放跑的是当前版本还是当时版本 → ② 变量取的是当下值还是当时值 → ③ 全模块重跑的副作用是否已清点 → ④ 该运行是否属于不入库类型。
- 提升层：工具 / 工作流。触发词：重放、replay、旧输入新版本、回填、变量取最新值、不可重放清单、Check run、Run with existing data、Replay run。

## r353A · 确认不是一个动作：ack ≠ transcript commit ≠ 被模型读到（来源：docs.openclaw.ai `plugins/codex-harness-runtime/queue-and-feedback` 4,065B，2026-10-02 r353A 实拉）

- **★三段确认语义互不蕴含**：`turn/steer` 的 acknowledgment **不代表 transcript commitment**；"A message sent to Codex without a confirmed transcript commit is **not replayed automatically**"；而 commit 只证明输入**进入了历史**，"does not prove that a subsequent model request has read it"。判据：**收到 ack 只能说"送达了"，说不了"存下了"，更说不了"生效了"**——排查"我明明发了但没执行"要按这三段分别取证，不能停在 ack。
- **★观测面降级只投运维通道，不回落给用户**：Codex 保存诊断日志失败时，只在 **Gateway logs 记 warning**；每条 native notice **收到即记一次**，不按共享该 app-server 的每个会话重复广播；operator-only，**不回落 chat**；"a logging failure never interrupts the native connection"，且该告警**既不修复原生日志故障，也不代表会话状态丢失**。判据：**日志系统自身的故障是"静默降级"而非"抛错"**——看不到日志 ≠ 没有故障；同时它保证不影响主链路，所以不能靠"业务还在跑"反推日志健康。
- 排障顺序（确认相关）：① 有没有 ack → ② 有没有 transcript commit（无 commit 则不会自动 replay）→ ③ 是否有后续模型请求真的读了它 → ④ 若怀疑日志缺失，先去运维通道查 warning，不要以 chat 无提示为证据。
- 提升层：工具 / 工作流。触发词：确认语义、ack、transcript commit、自动重放、诊断日志失败、operator-only。

## r353B · 日志落点会回退、低级别日志结构性降质、"跳过"不等于有人在等（来源：docs.openclaw.ai `gateway/logging` 23,470B + `concepts/queue-steering` 12,731B，2026-10-02 r353B 实拉）

- **★日志路径不保证稳定**：默认滚动日志在 `/tmp/openclaw/`（每天一个、按网关主机本地时区命名，命名 profile 另加前缀）；**若该目录不安全或不可写（属主错误 / world-writable / 是 symlink）则回退到用户级 `os.tmpdir()` 路径**，且"On Windows it **always** uses that OS-tmpdir fallback"。判据：**取证不能硬编码日志路径**——先解析实际落点；Windows 上默认就在 tmpdir，清理临时目录会直接清掉日志。
- **★低级别日志为省开销主动降质**：`trace` / `debug` / `info` / `warn` 记录**省略调用点元数据 `_meta.path`**（避免每条常规消息都抓取并解析栈），只有 `error` / `fatal` 保留；开启 diagnostics 且有内部消费者订阅时**所有级别都保留**。判据：**warn 级记录天然缺少定位信息，这是设计而非缺陷**——要靠 warn 定位必须临时开 diagnostics，不能指望常规日志自带调用点。
- **★"工具被跳过"不等于"有用户消息在等"**：被跳过的调用仍会收到配对的 start/end 事件与合成结果（`Skipped to process an incoming message.`），但**内部更新（如子 agent 完成报告）走同一个转向边界**，它们"can be hidden from the chat transcript and do not appear in the user message queue"。判据：**看到 Skipped 只能推出"有内部更新进来"，推不出"用户在催"**；把它当作用户行为信号会误判排队原因。
- 排障顺序（日志/信号相关）：① 日志实际落点（是否回退到 tmpdir）→ ② 该条记录的级别是否自带调用点（warn 以下没有）→ ③ Skipped 事件先按内部更新解释，再按用户消息解释。
- 提升层：工具 / 工作流。触发词：日志回退、tmpdir、_meta.path、warn 降质、Skipped 合成结果、内部更新走同一边界。

## r354B · 重试解决瞬时故障、熔断解决持续故障：两者必须成对配置，且熔断默认关（来源：docs.n8n.io `use-environment-variables/executions.md` 独立 curl 取 `.md` 原文，2026-10-02 r354B 实拉）

- **★"反复崩溃自动停用"是一个有默认关闭的熔断开关**：`N8N_WORKFLOW_AUTODEACTIVATION_ENABLED` 默认 `false`，`N8N_WORKFLOW_AUTODEACTIVATION_MAX_LAST_EXECUTIONS` 默认 `3`（"Number of crashed executions before unpublishing a workflow"）。判据：**重试与熔断方向相反且必须成对**——重试把失败再试一次（适合瞬时抖动），熔断在连续失败 N 次后停止投喂（适合持续故障）；只配重试，持续故障会被变成"持续压力 + 持续产生垃圾执行"。
- **★熔断的判据是"最近 N 次"而非"累计 N 次"**：变量名 `MAX_LAST_EXECUTIONS` 指向最近窗口。判据：**连续性与累计性是两种不同的触发语义**——累计计数会让"偶发失败的老工作流"在时间拉长后必然被熔断；连续/最近窗口才对应当下的健康度。
- **★熔断动作是"下线（unpublish）"不是"删除"**：触发后工作流被取消发布而非移除。判据：**自动处置的默认动作应是可逆的停用**；让自动化拥有删除权，等于把误判的代价从"暂停"抬到"数据丢失"。
- **★阈值可配说明熔断强度是策略不是常量**：3 次是默认值而非固定值。判据：**把熔断阈值写死在代码里，等于让运维在"太敏感"和"太迟钝"之间没有调节余地**；阈值、开关、动作三者都应该是配置项。
- 提升层：工作流 / 可复用 Skill。触发词：重试与熔断成对、autodeactivation、最近 N 次、连续 vs 累计、熔断即下线、熔断阈值可配。

## r383A · 额度归属借用四元组与部分可用启动语义（来源：help.make.com worker group + docs.n8n.io external-secrets.md，2026-10-02 r374-Q-B 实拉；经 Qoder 提名）
- 额度模型必须写成「档位 + 借用公式 + 迁移连带 + 互斥组合」四元组：floor（预留）/ ceiling（软上限），未指派默认 `min(plan limit, group slots)` 可借用但被 clamp；换组会把等待中的运行一起搬走，预留与隔离互斥（code-only mode 对 grouped workers 被拒）。
- 依赖源不可用时把「启动是否放行」与「谁因此失败」分开定义：外部密钥源超时标 errored、后台递增延迟重连、startup continues without its secrets，而启动期用到该 secret 的 workflow 在首次拉取完成前失败；更新周期超时旧值继续可用——三者任一未写即为未定义行为。

## r383B · 审批第四终态：`withdrawn` 与 `rejected` 主体相反（来源：activepieces.com 审计事件枚举，2026-10-02 r379-Q-A 实拉；经 Qoder 提名）
- 撤回不得触发驳回分支、不得留授权副作用；合并会污染拒绝率与再触发谓词，须作为独立终态分列。

## r383C · 采样的异常保留例外（来源：activepieces setup-opentelemetry.md + docs.openclaw.ai diagnostics/flags.md，2026-10-02 r381-Q-C 实拉；经 Qoder 提名）
- 按比例丢弃的通道必须显式声明保留谓词：`AP_LOG_SAMPLE_RATE_INFO` + `AP_LOG_KEEP_SLOW_MS`（慢必留、error 免采样）；对偶 = OpenClaw diagnostics flags「单子系统开额外日志而不全局抬 level」。

## r385B · 诊断/修复工具要分清「检查面」与「修复面」，并把「跳过」做成一等结果（来源：docs.openclaw.ai `gateway/doctor/running` 242,314B 独立 curl 实拉，2026-10-02；经 Qoder r388-Q-C 提名并纠错）
- **★检查项出现 ≠ 修复项存在，两个面是不同集合**：原文「Some lint findings are **intentionally diagnostic only**, so **a check appearing in `--lint --all` does not mean `--fix` will mutate that area**. The contract separates `detect()` (reports findings) from `repair()` (reports changes/diffs/side effects), which keeps a path open for a future `doctor --fix --dry-run` **without turning lint checks into mutation planners**」。判据：**把检查器顺手升级成修复器，会让"报出来"隐含"能修好"**——自愈类工具必须分别声明检查面与修复面，且允许只报不修；与 §r336A「诊断只读 / 修复须批准」分工：那条管**读写权限分离**，本条管**两个面的集合关系**。
- **★"跳过"是一等结果，必须与"运行"分列计数，否则 0 结论不可信**：机读信封给出 `checksRun` / `checksSkipped`：「counts (**skipped by profile, `--only`, or `--skip`**)」，且 `ok` 只表示「whether any finding met the selected severity threshold」。判据：**`findings` 为空有两种完全不同的含义——真的干净 / 全被跳过**；不报 `checksSkipped`，"0 问题"就是不可判的。与 §r354C「采集结论三态 命中/缺位/未达」同族：那条管**采集面**，本条管**执行面**。
- **★无人值守档只做 safe 动作，需人确认的动作是"显式跳过"而不是"静默降级为已修"**：`--non-interactive`「applying only **safe migrations** (config normalization + on-disk state moves). **Skips restart/service/sandbox actions that need human confirmation**. Legacy state migrations still run automatically when detected」；`--fix` 才含「workspace setup, session stores, exec approvals, and audit schema migrations」，`--fix --force` 才是激进档。判据：**非交互执行必须列出"这一档不做什么"**，否则运维会以为跑过一遍就修全了——被跳过的动作要留在报告里，不要从结果中消失。
- **★取消不能留下半截修复**：「Once started, Doctor finishes and releases its resources **before a cancelled caller settles**, so **cancellation cannot abandon an in-progress repair**」。判据：**可中断的修复工具必须先声明中断语义**——要么跑完再响应取消，要么整体回滚；把取消当成"尽力而为"会在修复类操作上留下半写状态。
- 判非（纠正 Qoder 转述）：本页**未检索到** `repaired/skipped/failed` 三态枚举与 `HealthFinding[]` 类型名（grep 0 命中），故该表述不作为判据引入；仅落上列可实证的四点。
- 提升层：工具 / 工作流 / 可观测性。触发词：检查面与修复面、检查项不等于可修复项、checksSkipped、0 findings 不可判、non-interactive 只做 safe migrations、显式跳过、取消不半截修复。

## r385C · 断点恢复必须写读双侧对称：存不存的判据是「能不能回校验」，且只修写侧救不了存量病灶（来源：api.github.com/repos/langflow-ai/langflow/pulls/15241 26,494B JSON 独立 curl 实拉，merged=true，标题「fix(checkpoint): drop model state that cannot be validated back on resume」，2026-10-02 实拉；经 Qoder r389-Q-A 提名）
- **★「序列化没报错」不是「能恢复」的证明**：原文根因段「`serialize_value` treats "`model_dump(mode="json")` did not raise" as **proof that a model round-trips**」——上游 langchain-core 1.6.1 让 `BaseTool` 的 dump 从抛异常变成成功，但 pydantic 把 `func` 与 `coroutine` 两个字段**静默降级成 `repr`**，于是「**the dump *succeeds* — and pydantic **silently degrades** the two fields it still cannot represent ... **with no warning**」；落库后 `_restore_model` 在恢复时 `model_validate` 永久抛 `callable_type`，「The pause is durable, so **the run is stuck for good**」。判据：**写盘的通过判据必须是往返校验（dump → re-validate → 同一 model），不是"没抛异常"**；上游一个版本升级就能把"抛"变成"静默降级"，让原本正确的判据失效。
- **★写侧丢弃与读侧恢复要对称，且读侧必须能降级**：修复是双侧——写侧「only encode a model when its dump **validates back into the same model**. This makes the drop **symmetric with `_restore_model`** — anything that would raise on resume is **dropped at write time** instead, and the rebuilt component re-derives it」；读侧「a stored payload that no longer restores **degrades to `None` instead of raising**, and its vertex joins `checkpoint_opaque_dropped_ids` so the existing fixpoint re-runs it」。判据：**只改写侧，库里已经毒化的数据不会自愈**——原文点明「Without this, **runs already paused on an affected install stay stuck after upgrading**, because the poisoned checkpoint is already in the database」。恢复路径的改造必须**新数据（写侧）+ 存量（读侧）**成对出场，否则升级本身成为新的失败源。
- **★丢弃不是丢数据，是让可重建物回到重建路径**：被丢弃的顶点进入 `opaque-dropped: ['chat_input']`、`resume layer: ['chat_output']`，恢复后由重建重新派生。判据：**对"可由重建重新得到"的状态，丢弃严格优于带着坏值继续**——与 §r325A「有重建器的子系统不该备份，陈旧副本严格劣于空库」同族：那条管**备份**，本条管**检查点里的单个状态项**。
- **★回归测试要能对"所有上游版本"都失败，才算覆盖了这一类 bug**：三个回归测试中关键的一条「**Fails on the CI-pinned 1.5.1 without the fix**, so CI now covers this class of bug **regardless of which langchain-core resolves**」；并注明该 bug 之所以没被 CI 抓到，是因为「This repo and CI are **pinned to 1.5.1** ... a clean install today resolves 1.6.3」。判据：**CI 绿可能只是因为锁到了旧版本**——验证一个与上游解析相关的修复时，要证明测试在旧版本与新版本上都能复现失败。
- 提升层：工作流 / 工具。触发词：序列化成功不等于可恢复、往返校验、写侧丢弃与读侧降级对称、checkpoint_opaque_dropped_ids、存量毒化不自愈、CI 绿只是锁了旧版本。

## 相关量不能替代身份：证据缺失时返回 unknown，禁止从元数据反推绑定（来源：docs.openclaw.ai/gateway/audit.md 37,793B，2026-10-03 r388B 独立实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·相关量不能替代身份：证据缺失时返回 unknown，禁止从元）
## 「能解析」不等于「干净」：优先级漂移与残留是两类独立故障；门禁退出码要分「有发现」与「不可用」（来源：docs.openclaw.ai/cli/secrets.md 16,115B，2026-10-03 r388C 独立实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·「能解析」不等于「干净」：优先级漂移与残留是两类独立故障；门）
## 联邦身份撤销不同步 + 全局命名空间先到先得 + 迁移通道的丢失面（来源：docs.n8n.io `verify-user-identity/use-saml/manage-users-with-saml.md` 1,830B + `follow-best-practices.md` 2,455B，2026-10-03 r390A 独立 curl 取 `.md` 原文实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·联邦身份撤销不同步 + 全局命名空间先到先得 + 迁移通道的）
## 会话新鲜度锚定「起点」不是「最近写入」；只差大小写的 ID 会分裂会话与记忆；隐私会话过期即删不归档（来源：docs.openclaw.ai/concepts/session 22,767B，2026-10-03 r390B 独立 curl 取 `.md` 原文实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·会话新鲜度锚定「起点」不是「最近写入」；只差大小写的 ID ）
## 「有错误」不等于「有可重试记录」：四类错误不产生实体；自动重试是白名单不是黑名单，并发上限保护的是下游（来源：help.make.com `errors-that-dont-create-incomplete-executions.md` 1,401B + `automatic-retry-of-incomplete-executions.md` 5,663B，2026-10-03 r390C 独立 curl 取 `.md` 原文实拉；与 §重试与熔断成对 互补——那条管熔断何时介入，本条管哪些错误根本没进重试体系）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·「有错误」不等于「有可重试记录」：四类错误不产生实体；自动重）
## 审计分层视图会收窄可见面：团队视图看不见组织级事件，因此窄视图无法自证「上层没动过我」（来源：help.make.com `audit-logs.md` 8,460B，2026-10-03 r390C 独立 curl 取 `.md` 原文实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·审计分层视图会收窄可见面：团队视图看不见组织级事件，因此窄视）
## 「为什么这条没被脱敏」先要分清是哪一面：用户规则是替换、内置规则始终生效、工具负载是合并——三面语义各不相同（来源：docs.openclaw.ai `gateway/config-observability.md` 10,454B，2026-10-03 r391A 独立 curl 取 `.md` 原文实拉；与 §脱敏保留可观测骨架 互补——那条管脱敏后还能不能排查，本条管脱敏规则之间的覆盖关系）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·「为什么这条没被脱敏」先要分清是哪一面：用户规则是替换、内置）
## 排查要取「生效面」而不是「配置面」：诊断命令是权威来源，拒绝事件有专属审计条目，日志路径会随平台漂移并被轮转清掉（来源：docs.openclaw.ai `gateway/sandbox-vs-tool-policy-vs-elevated.md` 9,792B + `gateway/sandboxing.md` 8,613B + `gateway/config-observability.md` 10,454B，2026-10-03 r391A 独立 curl 取 `.md` 原文实拉；与 §相关量≠身份量 互补——那条管别拿相关量当归属证据，本条管别拿配置值当生效值）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·排查要取「生效面」而不是「配置面」：诊断命令是权威来源，拒绝）
## 限流排查先看作用域再看数值；限额可以随令牌走；同一错误的「去重」是通道属性不是错误属性（来源：pipedream.com/docs `connect/api-reference/rate-limits.md` 2,732B + `workflows/limits.md` 9,083B + `workflows/building-workflows/errors.md` 9,150B，2026-10-03 r391B 独立 curl 取 `.md` 原文实拉；与 §重试与熔断成对 / §自动重试是白名单 互补——那两条管被限之后怎么退，本条管"限的是谁"与"告警为什么没响"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·限流排查先看作用域再看数值；限额可以随令牌走；同一错误的「去）
## 限流要补问「副本语义」与「成功计不计入」；超时时钟只走活跃段；同步调用要分清「答错了」与「没回答」（来源：pipedream.com/docs/conduit/deploy/hardening.md 7,011B + www.activepieces.com/docs/install/reference/limits.md 6,779B，2026-10-03 r393A 独立 curl 取 `.md` 原文实拉；与 §限流排查先看作用域再看数值 互补——那条管"限的是谁"，本条管"多副本会不会放大"与"什么才写进计数器"）

- 限流器要问第四件事：计数器是共享还是 per-replica。认证失败类（登录、OAuth、MCP、SCIM）在 PostgreSQL tier **跨副本共享** ⇒ 跑 N 副本不会让凭据猜测者拿到 N 倍速率；其余限流器**故意 per-replica**（集群总速率≈N×单实例）⇒ 扩容前必须确认目标限流器属于哪一类，否则横向扩容等于放大攻击面。
- 只有失败写计数器，成功登录不写 ⇒ 护栏不该给正常行为制造状态，也不该让攻击者用成功请求探测计数；被限的认证失败会以 `rate_limited` 出现在指标里，是观测信号不是普通错误。
- 超时只计活跃执行时间：被 Wait for Approval / Delay 暂停的时段**不计入** run timeout ⇒ 人类审批挂在流程里不会烧掉执行预算；但"暂停生命周期"另有独立上限，是另一条时钟，两条都要声明。
- 同步 webhook 的状态码语义：流程跑失败**立刻** 500；只有超时窗口内从未产生任何响应才 408（仍在运行，或流程没有 Return Response 步骤）⇒ 500 是"答了但错了"，408 是"根本没答"，排障方向不同。

## 指标与审计是两条通道：会重置的那条不能承载必须精确的数；拒绝不产生耗时样本；认证失败要按 reason 分族（来源：pipedream.com/docs `conduit/deploy/monitoring.md` 9,842B + docs.openclaw.ai `gateway/config-gateway.md` 36,884B，2026-10-03 r393B 独立 curl 取 `.md` 原文实拉；与 §限流要补问副本语义 互补——那条管"限的是谁、会不会被扩容放大"，本条管"看到异常后该改哪里"）（细则见 KB，2026-10-11 r519 再下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·指标与审计是两条通道会重置的那条不能承载必须精确的数拒绝不产生耗时样本认证失败要按reason分族来源pipedream）
## 同一个超时状态码下有两种命运；「提交成功」不等于「会单独跑一次」；404 与 204 指向两处不同配置（来源：docs.openclaw.ai `gateway/config-hooks.md` 36,853B，2026-10-03 r393C 独立 curl 取 `.md` 原文实拉；经 llms.txt/索引页定位；与 §有错误不等于有可重试记录 互补——那条管哪些错误根本没进重试体系，本条管已经拿到回执之后怎么解读）

- 503 不能一概读作"没跑成"：单跑模式下 15 秒内未准入，**那段排队工作被取消**；fan-out 模式下待处理工作**继续在后台执行**；网关暂停/重启也会返回 `503 gateway_unavailable` ⇒ 同一个码、三种后果，先分清提交模式再决定要不要重提。
- wake 回执的 `eventOutcome` 有两个值：`queued`（队列接受了这次唤醒）与 `coalesced`（同样的唤醒已经是队列里最近的待处理事件，被合并了）⇒ **"我提交成功了"不等于"它会单独执行一次"**，重复提交被合并是设计行为，验收时要读这个字段而不是只看 200。
- 404 与 204 是两种"什么都没发生"：404 = 没有任何 mapping 匹配到这个 hook；204 = 匹配到了但没产生任何动作 ⇒ 前者去查匹配条件，后者去查动作定义，方向完全不同。
- 重试前先分类：400 是 JSON/载荷/路由或投递选择不合法，**原文要求先读 `error` 字段再重试**；401 是 hook 鉴权失败；429 必须遵守 `Retry-After`；500 是 mapping/transform 抛异常（查网关日志）；502 是准入前的 agent 准备失败。

## 观测的陈旧窗口要写明秒数，且「负面结果不缓存」是独立设计；凭据状态要报「配置不可用」而非回落到正常态（来源：docs.openclaw.ai `gateway/config-secrets-env.md` 10,309B + `gateway/config-tools.md` 7,517B 索引页 + `gateway/config-tools/github-identity.md` 17,020B，2026-10-03 r395A 独立 curl 取 `.md` 原文实拉）

- **缓存窗口要给出具体秒数，并说明哪些面受影响**：成功的 `gh auth token` 读取会复用最多 **60 秒**（与凭据校验缓存对齐），因此 `gh auth login/logout/switch` 的变更**最多 60 秒后**才在这些读面可见；并发读共享一次原生查找 ⇒ 排查「改了没生效」时先算有没有落在缓存窗口内，别急着判定配置没写进去。
- **失败与「缺席证明」不缓存**：失败的 token 读取、以及「匿名访问不存在」这类否定结论**不进缓存**；环境 token、托管 profile 凭据、调用方权限、会话访问仍实时检查 ⇒ 若把否定结果也缓存，「暂时拿不到」会被固化成「确实没有」，这是两类完全不同的故障。
- **状态错误码不得降级**：托管 profile 缺失/无 token/损坏报 `configured_unavailable` 而不是改报原生账号；不可用的托管身份产生可操作错误而不是偷偷换凭据 ⇒ 排查时看到「还在正常工作」要先确认是不是已经静默切换到了另一套身份。
- **换身份不是即时吊销**：改选身份后，已准入的运行保留原 profile 选择，已启动的本地进程保留启动 token 直到退出、重启或 token 过期，而**新运行立即用新身份**；本地改动也**不撤销 GitHub 侧的授权**，要撤销得去 OAuth 应用设置单独做 ⇒ 撤销动作与生效动作是两个地方，声明里要分开写。

## 文档示例值不是内建默认值；单次超时与含重试的总等待是两个数；「0」可能是关闭也可能是无限制（来源：docs.openclaw.ai `gateway/config-tools/sessions-and-subagents.md` 9,632B + `gateway/config-tools/custom-providers.md` 13,129B，2026-10-03 r395B 独立 curl 取 `.md` 原文实拉）

- **示例值 ≠ 内建默认**：`runTimeoutSeconds` 内建默认 `0`（无超时），文档代码块里写的 `900` 是「常见的 opt-in 取值」而非默认值 ⇒ 排查超时相关问题时，先分清「文档里出现的数」与「不配时的默认值」，把示例抄进生产等于凭空加了一条超时。
- **单次超时 ≠ 含重试的总等待**：`announceTimeoutMs` 默认 120000 是**每次投递尝试**的超时，瞬时重试会让**总等待超过一次配置的超时** ⇒ 看到「超时设了 2 分钟却等了 6 分钟」不是配置没生效，而是重试次数没算进去。
- **同一个 `0` 在不同字段含义相反**：`runTimeoutSeconds: 0` 是**无超时**（放开），`archiveAfterMinutes: 0` 是**关闭自动归档**（收紧）⇒ 数值型开关的零值语义必须逐字段声明，不能靠一类字段的习惯去推另一类。

## 「改不了」先查字段归属方；两侧视图不一致时以记录持有方为准（来源：docs.n8n.io `security/enable-ssrf-protection.md` 3,822B + `security/block-specific-nodes.md` 2,425B + `basic-configuration/use-environment-variables/ssrf-protection.md` 7,039B + pipedream.com/docs `conduit/configure/access-control.md` 13,330B + `conduit/configure/scim.md` 9,789B，2026-10-03 r395C 独立 curl 取 `.md` 原文实拉；n8n 与 Pipedream 均经各自 `llms.txt`（287,049B / 34,240B）定位）

- **改不动某个字段，先查这个字段归谁**：被 SCIM 供给的人，其姓名**归目录所有**，本人改不了；工作区管理员只有在「工作区拥有该账号」时才可改名，条件三条同时成立——通过该工作区自己的 IdP 登录、未被 SCIM 供给、且不高于该管理员；而**后续 SSO 登录永不覆盖本人或管理员设定的姓名** ⇒ 排查「为什么改不了」的正确起点是「这个字段的归属方是谁」，不是「我的权限够不够」。
- **两侧视图不一致时，以持有记录的那一侧为准**：IdP 侧删掉 SCIM 资源后，IdP 读这个地址是 `404`，但平台侧记录仍然占着地址、仍然拒绝新的人 ⇒ 同步类故障要**两边各查一次**，只信其中一侧会得到完全相反的结论。
- **同步错误与审计都写明是人工介入场景**：官方把回收地址标注为「唯一需要人工介入的情形」，同步错误与审计记录都会提示 ⇒ 自动化同步要显式列出「哪些情况转人工」，否则会一直重试一个永远成功不了的动作。

## 诊断输出带执行环境前提；机器可读日志是独立开关；「拒绝执行」要显式声明成没跑（来源：docs.n8n.io `.../use-environment-variables/logs.md` 12,684B + docs.openclaw.ai `tools/exec-approvals.md` 39,387B，2026-10-03 r396B 独立 curl 取 `.md` 原文实拉）

- **诊断输出有环境前提，看不到不等于没执行**：`CODE_ENABLE_STDOUT` 默认 `false`，且置真后**只对 production executions 生效** ⇒ 同一段代码在手动执行与生产执行下可观测性不同；排查「为什么没有输出」的正确起点是**这个开关在哪种执行形态下生效**，而不是代码没跑到。
- **日志能不能被机器消费是独立开关**：`N8N_LOG_FORMAT` 默认 `text`，要一行一 JSON（含 message/level/timestamp/metadata）需显式设 `json` ⇒ 「有日志」不等于「可机读」，把日志接进监控/比对前先确认格式开关，否则下游只能解析人读文本。
- **拒绝类结果必须写成「没有执行」**：`SYSTEM_RUN_DENIED` 的语义是节点**拒绝执行**，官方特别说明它**不是「命令可能已运行」** ⇒ 凡返回拒绝，声明里要明确写出「未执行」，不能让调用方按「结果未知」去猜；配套地，迟到的批准无法重启已取消的那一轮 ⇒ 撤销的生效点在启动边界，批准不复活已终止的执行。

## 日志级别枚举里存在「静音」档；保留窗口是「单份大小 × 份数」的乘积（来源：docs.n8n.io `deploy/host-n8n/keep-n8n-running/set-up-logging.md` 7,738B + `.../use-environment-variables/logs.md` 12,684B，2026-10-03 r396C 独立 curl 取 `.md` 原文实拉）

- **最低档是「什么都不输出」，不是「只报严重错误」**：n8n 的级别枚举含 `silent`（outputs nothing at all），位于 `error` 之下 ⇒ 「一条日志都没有」可能是**合法配置**而未必是进程没起来或日志管道断了；排查零输出时先把级别档位读出来，再怀疑链路。
- **日志能留多久由两个上限相乘决定**：`N8N_LOG_FILE_SIZE_MAX`（单份 MB）与 `N8N_LOG_FILE_COUNT_MAX`（保留份数）共同构成保留窗口，且官方提示**使用 workers 时份数值必须设** ⇒ 「日志还在不在」算的是容量×份数的乘积，只调其中一个算不出保留时长；多进程形态下不设份数会互相覆盖。

## 观测沉降窗与「首读物化」：按物化时点而非开关翻转时点切存量；日志落盘有沉降延迟（来源：Qoder r399-Q/r400-Q 审计净新，2026-10-03；与 §诊断输出带执行环境前提 互补——那条管"看不看到"，本条管"看到的是哪个时点的"）

- **首读物化时点 ≠ 开关翻转时点**：配置/开关从"翻转"到"真正物化进存储/生效"之间有延迟，存量数据要按**物化时点**切，不能按开关翻转时点切——否则会把"已翻转但未生效"的数据算进新状态，或把"已生效但时点在翻转前"的算漏。
- **观测有沉降窗**：日志/指标从产生到可被查询存在延迟窗口，排障时"现在查不到"可能是还没沉降而非没发生；验收覆盖面要标清观测沉降窗，避免把延迟当成缺失。
- 提升层：诊断/观测。触发词：首读物化时点、物化时点切存量、观测沉降窗、开关翻转≠生效。

## 先落盘后转发的事件缓冲层：多写者会把缓冲变损坏源，恢复解析必须有上界；下游熔断按滑动窗口计数（来源：docs.n8n.io `administer/observe-and-log/stream-logs-to-external-systems.md` 23,919B，2026-10-03 r408A 独立 curl 取 `.md` 原文实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·先落盘后转发的事件缓冲层：多写者会把缓冲变损坏源，恢复解析必）
## 降级值要满足输出类型契约；同叫「循环」，Loop 恒停而 Iteration 可继续，继续方式又分「留位 null」与「剔除」（来源：docs.dify.ai `en/cloud/use-dify/build/predefined-error-handling-logic.md` 3,768B，2026-10-03 r408B 独立 curl 取 `.md` 原文实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·降级值要满足输出类型契约；同叫「循环」，Loop 恒停而 I）
## 需人工确认的工具不能用进无人值守通道；审批是「逐事件回执」协议，回一半不算恢复（来源：docs.bigmodel.cn `cn/managed-agents/permission-policies.md` 6,620B（经 `llms.txt` 49,320B 定位），2026-10-03 r408C 独立 curl 取 `.md` 原文实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·需人工确认的工具不能用进无人值守通道；审批是「逐事件回执」协）
## 依赖失败不阻断会话启动，只降级为带三态重试标的事件；会话外可主动探测且探测结论含「不可判定」一态（来源：docs.bigmodel.cn `cn/managed-agents/{mcp,vaults}.md` 6,511B / 7,423B，2026-10-04 r409A 独立 curl 取 `.md` 原文实拉；与 §长命周期任务故障计数分型 / §判死前先回查真实执行状态 互补——那两条管"怎么判死"与"计数怎么分型"，本条管"依赖不可用时平台选择继续跑"与"探测结论本身可能不可判定"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·依赖失败不阻断会话启动，只降级为带三态重试标的事件；会话外可）
## 跨轮持久性是分层的：产物目录恒久、工作区要开 checkpoint、进程与内存从不保；快照只在成功轮更新，故恢复点会滞后于失败尝试（来源：docs.bigmodel.cn `cn/managed-agents/create-session.md` 9,481B，2026-10-04 r409C 独立 curl 取 `.md` 原文实拉；与 §重放不是时光机（可变量取最新值）/ §观测快照唯一可写例外 互补——那两条管"重放语义"与"快照可写性"，本条管"哪些东西跨轮还在"与"快照什么时候才会推进"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·跨轮持久性是分层的：产物目录恒久、工作区要开 checkpo）
## 循环上限的计数单位被「自我复制」重置就等于没有上限；修完 bug 要把它的状态签名固化成断言；监控缺「增长率 / 同类重复」两个维度就只能等客户上报（来源：www.activepieces.com/docs `handbook/engineering/postmortems/2026-03-19-redis-and-delay-overload.md` 3,797B，2026-10-04 r411A 独立 curl 实拉；与 §长命周期任务故障计数分型 / §熔断按滑动窗口计数 互补——那两条管"达到阈值后怎么停用"，本条管"阈值挂错计量对象时根本达不到"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·循环上限的计数单位被「自我复制」重置就等于没有上限；修完 b）
## 进度标记与产出分两次落库就是失步窗口；超时放弃的语义是「当没发生过」，且放弃阈值必须小于接管租约（来源：docs.n8n.io deploy/host-n8n/configure-n8n/durable-scheduler.md 30,546B，2026-10-04 r417A 独立 curl 取 .md 原文实拉；真页经 llms.txt 287,049B 重新定位，此前 Qoder 引用的 hosting/scaling/durable-scheduler 系 1,930B 404 壳）
- 进度与产出是两个写入就存在失步窗口：轮询光标默认存 workflow static data 并与执行分开保存，崩溃落在两次保存之间时二者错位，症状是「跳过条目」或「重复处理」。修法是把光标与执行放进同一张表的同一事务，使一轮轮询要么完全发生要么完全没发生。判据：写入次数即窗口数。
- 超时放弃必须让标记原地不动：poll 超过阈值被放弃时平台什么都不记、光标不动，下一次覆盖同一段，因此不丢数据。「放弃」的正确语义是「当作没发生过」，若写成「推进到下一处」就会静默丢数据。
- 两个超时必须有偏序：放弃阈值（poll timeout）须严格小于接管租约（lease duration），否则被放弃的工作仍在跑而另一实例已接管同一 run，放弃形同虚设；平台在 timeout 达到 lease 时启动告警。
- 积压补跑是形状选择且没有任何策略逐条重放：丢弃全部 / 坍缩为最新一次 / 每条触发规则各一次，三种策略下时钟一律跨过积压；一次性触发没有「下一次」可恢复，故 catch-up 策略下仍会晚跑，skip 则永久丢弃。与部分失败三形状互补——那条管同批内失败条目的形状，本条管跨批积压的形状。
- 调度实体有所有者：owner reconciliation 周期回收所有者已消失的 schedule，否则留下无人认领的孤儿定时任务。

## 同一根因在四层症状上暴露；调试行为本身会改变资源画像（来源：docs.n8n.io `deploy/host-n8n/configure-n8n/scaling/fix-memory-issues.md` 5,626B，2026-10-05 r420-B 经 llms.txt 定位真路径后 .md 实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·同一根因在四层症状上暴露；调试行为本身会改变资源画像）
## 修复由「再检测」证明，不由返回值证明；耗时与退出码本身不能证明原因（来源：docs.openclaw.ai `cli/doctor/health-contract.md` 3,303B + `ci/checkout.md` 21,314B，2026-10-05 r421-A 独立 curl 取 `.md` 原文实拉逐串命中；消化 Qoder r407-Q-A N3/N12 积压点，并回源钉定 r385B 曾判「转述未证实」的真页）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·修复由「再检测」证明，不由返回值证明；耗时与退出码本身不能证）
## 层级配置「取抬高不取拒绝」；放弃型超时必须严格小于租约；弃跑不留痕以保证重放等价（来源：docs.n8n.io/deploy/host-n8n/configure-n8n/durable-scheduler.md 30,546B，2026-10-05 r421-B 经 llms.txt 287,049B 定位真路径后独立 curl 实拉逐串命中；消化 Qoder r408-Q-B B5/B6 积压点）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·层级配置「取抬高不取拒绝」；放弃型超时必须严格小于租约；弃跑）
## 重放必须钉两维（定义版本 + 输入解析时刻）；进入历史视图须先挂起自动持久化（来源：help.make.com/scenario-settings.md 5,172B + docs.langflow.org/concepts-flows 200 正文，2026-10-05 r421-C 独立 curl 实拉逐串命中；消化 Qoder r420-Q-C C-1 / r420-Q-A A-2 积压点）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·重放必须钉两维）
## 允许自定义代码的节点必须带执行边界：默认沙箱 + 超时保护 + 输入校验，否则是 RCE 与资源失控面（来源：docs.flowiseai.com/llms-full.txt 618,913B + 第 1 片 207,021B「Custom Function / Custom Tool」节点 Features 段，2026-10-05 r424-B 独立 curl 实拉分页全量逐串命中）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·允许自定义代码的节点必须带执行边界：默认沙箱 + 超时保护 ）
## 守卫读不懂载荷时须「阻塞」而非「跳过」：序列化失败属 fail-closed 于工具门，跳过等于默认放行（全文见 references/knowledge-base.md §下沉·守卫读不懂载荷；触发词：守卫读不懂阻塞、序列化失败阻塞、PreToolUse 跳过改阻塞、v2.1.288）

## 为「不丢数据」而加的持久化兜底层，在多进程共享时会自己变成丢数据源；显式配置会取消平台自动保护并把唯一性责任转移给编排方（全文见 references/knowledge-base.md §下沉·多进程共享事件日志；触发词：多进程共享日志、并发追加损坏、兜底层自伤、唯一性归编排方）

## 步预算会被框架"自身环节"消耗，而消耗方从不在文档里披露：LangFlow v1.12.4 修复原文 "compute recursion_limit accounting for middleware graph nodes"（#15362，2026-09-29）——中间件包装出的节点此前不计入 `recursion_limit`，修复后计入（来源：api.github.com/repos/langflow-ai/langflow/releases，2026-10-07 独立 curl 实拉；与 dl「recursion_limit 默认值去哪确认」互补——r309B/r368C 管"默认值多大、按引擎版本确认"，本条管"预算的计量口径是否被框架改动"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·步预算会被框架"自身环节"消耗，而消耗方从不在文档里披露：L）
## 通知抑制键必须含「错误身份」三元组，且去重只作用在通知侧——「没收到告警」不等于「没在坏」（来源：pipedream.com/docs/workflows/building-workflows/errors.md 9,150B，2026-10-07 独立 curl 实拉逐串命中 `at most one email` / `per error` / `per workflow` / `per 24 hour period`；与 §失败留痕纪律 互补——那条管"失败要留痕"，本条管"同一失败的通知会被怎么压掉"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·通知抑制键必须含「错误身份」三元组，且去重只作用在通知侧——）
## 批准绑定具体计划、计划变更即失效；漂移检查只读且不作门——观测面与拦截面必须分离，读不到的 provider 报 unverifiable（既不是 clean 也不是 failure）（来源：api.github.com/repos/mikehasa/golive-skill/readme 44,717B（`Accept: application/vnd.github.raw+json`），2026-10-07 独立 curl 实拉逐串命中 `plan ID` / `not a gate` / `confirm-destroy` / `state.json` / `unverifiable`；与 §诊断只读、修复须批准 互补——那条管 diagnose/repair 分人，本条管"批准绑在哪个对象上"与"漂移该不该拦住"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·批准绑定具体计划、计划变更即失效；漂移检查只读且不作门——观）
## 失败终态要按「责任主体」着色，且子任务重试期间父任务不得进入终态：终态名是派工单，分类错一位就把修的人派错（来源：github.com/activepieces/activepieces/releases 574,402B，2026-10-08 独立 curl 实拉逐串命中 `fix(sandbox): surface missing piece bundles as FAILED runs, not INTERNAL_ERROR` / `fix(subflows): keep the calling flow waiting when a subflow crashes and is retried`；与 §通知抑制键三元组 互补——那条管通知怎么被压掉，本条管失败归到哪一类、父任务何时进终态）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·失败终态要按「责任主体」着色，且子任务重试期间父任务不得进入）
## 自动重放的资格来自「命令动词类型的静态声明」，不来自运行时"看起来安全"：重放白名单按 read/write/destructive 打标签时点判定（来源：docs.dify.ai `/en/cli/integrate-agents/error-handling-and-retries-for-agents.md` 6,093B 全文，2026-10-08 一手实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·自动重放的资格来自「命令动词类型的静态声明」，不来自运行时"）
## 「暂停」必须判为成功而非错误；错误分支要按「恢复动作」分组，不按错误码逐个枚举（来源：同上，docs.dify.ai 6,093B）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·「暂停」必须判为成功而非错误；错误分支要按「恢复动作」分组，）
## 凭据校验的返回值必须是「结构化结果」而不是布尔或异常：失败要带人类可读原因，后台刷新是可选项且未定义者不受影响（来源：www.activepieces.com/docs/build-pieces/piece-reference/authentication.md 7,569B，2026-10-08 一手 curl 逐串命中 `{ valid: false, error: 'Invalid Api Key' }` / `refresh` is opt-in. Pieces that don't define it are unaffected；与 §错误负载缺省字段 / §只报原因不报对策 互补——那两条管错误对象装哪些字段，本条管"校验"这个动作本身的返回契约）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·凭据校验的返回值必须是「结构化结果」而不是布尔或异常：失败要）
## 状态机的边名必须由单一常量源定义：前后端各拼一次字面量，会让超时分支走到用户操作分支上（来源：api.github.com/repos/langgenius/dify/issues/40746 一手 JSON，2026-10-08 实拉，标题 `fix(human-input): align backend timeout handle with frontend DSL`，正文逐串命中 `sourceHandle: "__timeout"` / `_TIMEOUT_HANDLE` was set to `"__timeout__"` / `chose the wrong handle, so the timeout edge could fire on a different (user-action) branch than the one the workflow author drew`；与 §失败终态按责任主体着色 互补——那条管失败归谁，本条管"根本没失败，只是走错了分支"这一类无报错错走）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·状态机的边名必须由单一常量源定义：前后端各拼一次字面量，会让）
## 共享 MCP 连接的「身份默认值」即泄漏面：oauth.identity 默认 shared（跨请求者复用同一身份），改 per-requester 才隔离；且未设 requestTimeout 时「列工具」另用 10s 短预算（来源：docs.openclaw.ai/gateway/config-extensions.md，2026-10-08 一手 curl 逐串命中 `oauth.identity`/`per-requester`/`shared`/`requestTimeoutMs`/`sessionIdleTtlMs`/`256`；r445B 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·共享 MCP 连接的「身份默认值」即泄漏面：oauth.id）
## 观测/重试/保留窗口的长度必须显式大于被观测对象的寿命：问一句「这个窗是按谁的生命周期定的？」，大不过对象就等于没有（来源：docs.dify.ai/llms-full.txt 2,690,424B，2026-10-10 一手 curl 逐串命中 `OPS_TRACE_RETRYABLE_DISPATCH_MAX_RETRIES` `780` / `OPS_TRACE_RETRYABLE_DISPATCH_DELAY_SECONDS`×2 / `OPS_TRACE_PARENT_CONTEXT_TTL_SECONDS` / `DIFY_AGENT_RUN_RETENTION_SECONDS` / `sized to outlast the one-hour workflow limit plus the export grace period`；r486A 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·观测/重试/保留窗口的长度必须显式大于被观测对象的寿命：问一）
## 探活要把「通道失效」与「路径失效」分开记账：403/404/DNS 是三态，且国内站常自带免认证全文变体（`<url>.md` 与 `/.well-known/*`）（来源：www.modelscope.cn/llms.txt 4,267B，2026-10-10 一手 curl 逐串命中 `Source:` / `well-known`×2 / `openapi.json`；辅以 r486-Q-C 浏览器实测 make.com `/en/changelog` 站内 404 而 `/en/whats-new` 正常渲染；r486C 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·探活要把「通道失效」与「路径失效」分开记账：403/404/）
## 「排障窗」与「挂起窗」是两个必须分别声明的时钟：观测数据保留期 ≠ 状态机可恢复寿命，混设会导致「还能续跑但日志没了」或「租约到期后哑火」（来源：api.github.com/repos/langgenius/dify/releases 303,233B（v1.17.1），2026-10-10 一手 curl 逐串命中 `event streams now expire after **2 hours** instead of 3 days` / `3 days) → 7200 (2 hours)` / `Agent runs no longer fill up Redis` / `Lease-based triggers stopped working after about a week` / `unresumable`；r488B 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·「排障窗」与「挂起窗」是两个必须分别声明的时钟：观测数据保留）
## r490A · 取消是「协作式」而非「抢占式」：生效粒度是执行单元间隙，且陈旧取消位是跨轮污染源（来源：api.github.com/repos/langgenius/dify/releases/tags/1.17.0 一手 JSON（body 117,802B），2026-10-10 r490A 独立 curl 实拉逐串命中 `stop` is now honored between non-streaming nodes and paused workflows clear stale cancellation signals correctly (#41090, #40905, #40972) / `fix(api): clear stale cancellation signals when resuming a paused workflow` #40905 / `fix(dify-agent): isolate cancellation intent observer` #40896 / `fix(dify-agent): make run cancellation route-independent` #39942 / `preserve snapshots for failed and cancelled runs` #40876）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·r490A · 取消是「协作式」而非「抢占式」：生效粒度是执）
## r490C · 通道失效记账增第五态「厂商域分离」：同一厂商的可达域 ≠ 被拦域；据此更正 make.com 终结论（来源：www.make.com/en/whats-new → 403 / 5,610B，正文首串 `<title>Just a moment...`、`challenge` 计数 8；同厂商 help.make.com/llms.txt → 200 / 72,873B 且文章 `.md` 全可达；2026-10-10 r490C 一手 curl 对照）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·r490C · 通道失效记账增第五态「厂商域分离」：同一厂商）
## r492A · 陈旧判定有两条互不对偶的路径：一是时间阈值（到点即判旧），二是因果传播（改动沿依赖图向上标脏）；两者回答的问题不同，排障必须分别建账（来源：docs.n8n.io/build/understand-workflows/understand-executions/understand-dirty-nodes.md 5,374B，2026-10-10 r492A 一手 curl 实拉逐串命中 `Modifying node parameters: labels the modified node dirty` / `If any of the above actions occur inside a loop, also labels the first node of the loop dirty` / `also labels any executed parent nodes (up to and including the root)` / `It may also be the point where a partial execution starts from`）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·r492A · 陈旧判定有两条互不对偶的路径：一是时间阈值）
## r495A · 背压不一定以「队列长度」表达：可折算成执行单元数量，且扩容与缩容用的是两种不同量纲的判据（来源：docs.dify.ai/llms-full.txt 2,695,981B，2026-10-10 r495A 一手 curl 实拉；逐串命中 `GRAPH_ENGINE_SCALE_UP_THRESHOLD` \| `0` \| How many tasks may wait for a free worker before the pool adds another，up to `GRAPH_ENGINE_MAX_WORKERS`. At the default `0`，a worker is added as soon as any task waits / `GRAPH_ENGINE_SCALE_DOWN_IDLE_TIME` \| `5.0` \| Seconds of idle time before excess workers are removed / `GRAPH_ENGINE_MIN_WORKERS` `3` / `GRAPH_ENGINE_MAX_WORKERS` `10` / `MAX_SUBMIT_COUNT` `100` / `TENANT_ISOLATED_TASK_CONCURRENCY` `1`）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·r495A · 背压不一定以「队列长度」表达：可折算成执行单）
## r495A · 同一个超时数值被放在多层时，生效值取最严者；改一层不动另一层等于没改，且「配置项存在」不等于「配置项有效」（来源：docs.dify.ai/llms-full.txt 2,695,981B + docs.n8n.io/llms-full.txt 811,527B，2026-10-10 r495A 一手 curl 实拉；逐串命中 `DIFY_AGENT_RUN_TIMEOUT_SECONDS` \| `3600` \| Wall-clock deadline for one agent run's model and tool work. A run that exceeds it fails with `agent_run_limit_exceeded` / The API-side `APP_MAX_EXECUTION_TIME` and `WORKFLOW_MAX_EXECUTION_TIME` (default `3600`) cap runs earlier if set below this / On the `e2b` backend the sandbox's `DIFY_AGENT_E2B_ACTIVE_TIMEOUT_SECONDS` (ceiling 3600) still applies / `QUEUE_WORKER_MAX_STALLED_COUNT` (**deprecated**) \| `1` \| **Deprecated** Removed in n8n 2.0. Setting this has no effect）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·r495A · 同一个超时数值被放在多层时，生效值取最严者；）
## r510A · 「可暂停」不只是多一个终态：恢复侧有四件契约要分别实证——暂停终态事件名、过期是正常出边、重放是显式开关、提交幂等由服务端强制（来源：docs.dify.ai/llms-full.txt 2,695,981B，2026-10-10 r510A 一手 curl 200 实拉；逐串命中 `workflow_paused`×4 / `human_input_required`×10 / `form_token`×40 / `include_state_snapshot`×10 / `continue_on_pause`×6 / `human_input_form_timeout`×4 / `A successful submit is final`×2）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·r510A · 「可暂停」不只是多一个终态：恢复侧有四件契约）
## 架构上不成立的组合要在启动期拒，数值越界才抬高告警；逃生阀必须由命名承载风险且「放行」不等于「变安全」（来源：docs.langflow.org/deployment-multi-worker 114,789B，2026-10-11 r511A 一手 curl 200 实拉；逐串命中 `LANGFLOW_DANGEROUSLY_ALLOW_MULTI_WORKER_WITHOUT_SHARED_QUEUE` / `refuses to start` / `per-process` / `does not make multi-worker safe` / `Unsupported with the Langflow UI`）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·架构上不成立的组合要在启动期拒，数值越界才抬高告警；逃生阀必）
## 补偿的挂靠点与触发点是两个不同对象；回滚只覆盖「已暂存集合」，提交即永久失格，且框架只保证补偿钩子被触发、不保证副作用被消除（细则见 KB，2026-10-11 r519 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·补偿的挂靠点与触发点是两个不同对象回滚只覆盖已暂存集合提交即永久失格且框架只保证补偿钩子被触发不保证副作用被消除）
## 兜底存在按路径作用域的整片豁免，且触发位置在重试预算耗尽之后（细则见 KB，2026-10-11 r519 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·兜底存在按路径作用域的整片豁免且触发位置在重试预算耗尽之后）
## 抽取子工作流是「重构边界」，静默改变 item 排序语义与类型契约：子工作流输入/输出默认 allow-all 类型需手动补；first()/last()/all() 排序在新上下文可能不同（框架加 _firstItem/_lastItem/_allItems 后缀仅尽量保留）；itemMatching 须传固定索引（细则见 KB，2026-10-11 r520B 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·抽取子工作流是重构边界静默改变item排序语义与类型契约）
## 取消是两级超时加一个轮询检测的组合worker宽限30s强杀server300s终态化取消靠worker轮询发现（细则见 KB，2026-10-11 r524A 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·取消是两级超时加一个轮询检测的组合）
## 跨yield分离式子任务结算按归属冻结加代数认领加幂等结算三件套验yield后完成归属不能丢（细则见 KB，2026-10-11 r524B 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·跨yield分离式子任务结算三件套）

## 平台隐式容错可被整版删除重试假设须显式归位且升级后逐项能力探测而非复用旧通过记录（细则见 KB，2026-10-12 r526A 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·平台隐式容错可以被整版删除）

## 多资源加锁须取稳定全序防互锁清理回收类操作显式降级best-effort不阻塞主链不计入成功判据（细则见 KB，2026-10-12 r526A 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·多资源加锁必须取稳定全序）

## 大版本升级翻转默认安全态env与overrideConfig默认不可读不可覆盖须列入升级前自查并逐项探测（细则见 KB，2026-10-12 r526C 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·大版本升级会翻转默认安全态）

## 错误码语义是上游可改契约须把码到类映射表版本化并在上游breaking记录反查（细则见 KB，2026-10-12 r526C 下沉）（全文见 references/knowledge-base.md §下沉·wb-debug-loop·错误码的语义是上游可改的契约）
