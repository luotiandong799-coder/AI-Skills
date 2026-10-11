---
name: wb-artifact-verification
description: >-
  对"生成出来的东西"做独立验证并给出明确的成功/失败判定。当用户要求"验证生成结果""验证这个脚本/代码能不能跑""验证是否成功""帮我确认结果对不对""check 一下生成物""验证执行结果"，或给出"先生成再验证再反馈"这类任务时使用。核心是三条互相独立的证据源（独立算法 oracle / 外部已知常数 / 随机差分模糊测试）+ 故障注入（变异测试）证明验证器本身有检出能力，禁止只跑一次"看起来没问题"就宣布成功。另含"证明检查真的跑到了"：非零退出不等于检出（import 报错/构建失败也非零），须打到达标记；被测方须侧盲；判不出结果时"不确定"是一等判定，不得默认通过、不得伪造因果。另含"验证通道禁止副作用"：验证命令不得借检查之名做发布/部署/推送/外发。触发词：验证、验证结果、验证一下、能不能跑、跑通了吗、对不对、check 一下、测一下、自检、回归、真的修好了吗、看起来没问题、绿灯、都过了、测试全绿、失败注入、变异测试、假阳性、伪成功、静默测错、不确定、证不出来、证据不足、评分器、评测、基准、对照实验、抽样、覆盖率、未测、跳过、flaky、可复现、脚本化验证、退出码、超时、只读验证、别在验证里发布。、失败分类法、置信度阈值过滤误报、批量失败、单条失败、占位保配对、条数对齐、失败归属到条、来源自证端点、代理后静默失效、我看你是谁、限流失效、真实来源核验、评测续跑、只重放未完成、改了实现要全量重跑、续跑可比性、自描述元数据、写入方版本、序列化器不可用、解码失败不等于值错、绕过读取通道、过期检查在读取路径、合法 JSON 不等于合规、结构检查三态、解析失败vs字段不合规、轨迹同构三元组、完成度不能从最终答复推断、逐子任务报告、工具三判、误读返回值、恰好一次、exactly once、副作用重复、审计重复、重放重复、结算标记、合并前钩子、占用分解、扫描根、观测面盲区、分解为空、不是我的证据、盘满但分解小、换证据源、告警缺席、钩子被吞、缓存命中不触发、钩子计数翻倍、per-attempt钩子、静默失效、告警不算证据、数据飞轮、过闸才上线、来源优先级、合成数据垫底、轨迹优先、分层切分、五千好过五万、反馈版本化、跨家族互评、模式坍缩、四桶评测集、失败重放、回归还是漂移、定期重跑、置信门槛、rescore 重算判定、整臂聚合扣留、部分覆盖聚合
version: "2.202.0"
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
> 正文预算管理：「"verified" 必须携带可定位的证据指针且由校验器机械强制：空指针行直接拒（全文见」（全文已零删减下沉 references/knowledge-base.md §下沉·"verified" 必须携带可定位的证据指针且由校验器机械强制：空指针行直接拒（全文见）
> 正文预算管理：「"索引层无数值" 是可交付结论，不是抓取失败：Flowise/LangFlow 索引层零」（全文已零删减下沉 references/knowledge-base.md §下沉·"索引层无数值" 是可交付结论，不是抓取失败：Flowise/LangFlow 索引层零）
> 正文预算管理：「单轮评测会系统性低估：只看首轮会把「多轮后能做成」误判为「做不成」；攻击轨迹库是比又一份」（全文已零删减下沉 references/knowledge-base.md §下沉·单轮评测会系统性低估：只看首轮会把「多轮后能做成」误判为「做不成」；攻击轨迹库是比又一份）
## 「没有分数」与「零分」是两件事；通过=多智能体取最大 × 全维度合取，增益不得越过闸门（来源：api.github.com/repos/NVIDIA/SkillEvaluator/contents/docs/reports.mdx 20,014B（evaluator 0.8.2），2026-10-01 r348C 独立 curl 实拉取 base64 解码，`INCOMPLETE`×5 / `NEUTRAL`×6 / `Skill Lift`×5 / `pass-threshold` 逐串命中）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·没有分数与零分是两件事通过多智能体取最大全维度合取增益不得越过闸门来源apigi）
## 引用清单要带机器可判的新鲜度字段：有 staleAfter 就照它判，没有就退回 generatedAt 距今天数（来源：api.github.com/repos/anthropics/skills/contents/skills/academy-guide/SKILL.md 7,715B base64 解码，2026-10-01 r349B 独立 curl 实拉，`staleAfter` / `generatedAt` 逐串命中；经 Qoder r367-Q-B 提名）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·引用清单要带机器可判的新鲜度字段有staleAfter就照它判没有就退回gene）
## 检索类能力降级要「机器可读自证」：响应体自带 mode 声明，采集侧按 mode 分档记可信度（来源：www.activepieces.com/docs/mcp/tool-search.md 3,608B，2026-10-01 r349C 独立 curl 实拉，`semantic` ×4 / `keyword` ×3 / `audience` 逐串命中；经 Qoder r372-Q-A 提名）（全文见 references/knowledge-base.md §下沉·检索类能力降级要机器可读自证响应体自带mode声明采集侧按mode分档记可信度来源wwwacti）

## 验证环节要「定向且完整」，否则只能换来高误封：单条边被篡改即把误放率推到 15.3–48.9%（来源：arXiv 2609.40027《Who Verifies the Graph?》abs 页 43,234B，2026-10-01 r349C 独立 curl 实拉，`15.3` / `48.9` 逐串命中；经 Qoder r368-Q-C 提名）（全文见 references/knowledge-base.md §下沉·验证环节要定向且完整否则只能换来高误封单条边被篡改即把误放率推到153489来源arXiv260）

> 正文预算管理：「r353A · 失败现场的处置由开关决定，取证能力会被隐私开关直接削掉」（全文已零删减下沉 references/knowledge-base.md §下沉·r353A失败现场的处置由开关决定取证能力会被隐私开关直接削掉）
> 正文预算管理：「r353B · 错误契约随失败位置分叉，取证通道可用 `.md` 后缀直取」（全文已零删减下沉 references/knowledge-base.md §下沉·r353B错误契约随失败位置分叉取证通道可用md后缀直取）
> 正文预算管理：「r353C · 事务边界由模块能力标注决定；验证有自己的预算币种；文档站提供问答」（全文已零删减下沉 references/knowledge-base.md §下沉·r353C事务边界由模块能力标注决定验证有自己的预算币种文档站提供问答式检索接口）
## r354A · 留痕按「失败优先」分级保存；删除是两阶段，且活跃态与人工标注豁免（来源：docs.n8n...（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r440B·r354A · 留痕按「失败优先」分级保存；删除是两阶段，且活跃态与人工标）
> 正文预算管理：「r354B · 截断/限额必须声明作用域（展示面 vs 执行面）；无鉴权通道靠「」（全文已零删减下沉 references/knowledge-base.md §下沉·r354B截断限额必须声明作用域展示面vs执行面无鉴权通道靠一次性兜底评测并发按档位给默认来源docsn8niousee）
## r354C · 机器可读取证有第四条通道：`Accept` 头内容协商；OOM 有三层异构信号且自愈能力取决于运行方式（来源：docs.n8n.io `scaling/memory-errors.md` 404 页 2,188B + `scaling/fix-memory-issues.md` + `scaling/use-external-storage.md` 独立 curl 取 `.md` 原文，2026-10-02 r354C 实拉）（全文见 references/knowledge-base.md §下沉·r354C机器可读取证有第四条通道Accept头内容协商OOM有三层异构信号且自愈能力取决于运行方式来源docsn8ni）


## r355A · 「仍在正确处理」≠「在服务窗内可用」：吞吐与延迟必须分开判；厂商性能数字是配置的函数而非常量（来源：docs.n8n.io `scaling/control-concurrency.md` 4,111B + `use-n8n-cloud/understand-concurrency.md` 3,828B + `scaling/measure-performance.md` 3,955B 独立 curl 取 `.md` 原文，2026-10-02 r355A 实拉）（全文见 references/knowledge-base.md §下沉·r355A仍在正确处理在服务窗内可用吞吐与延迟必须分开判厂商性能数字是配置的函数而非常量来源docsn8nioscali）


## r355C · 兼容性验证不能只判「崩没崩」：字段移除后的真实表现是「继续运行但降级」；能力按载体版本分档，缺档是「能用但少一档」（来源：docs.n8n.io `changelog/v30-breaking-changes.md` 21,374B 独立 curl 取 `.md` 原文，2026-10-02 r355C 实拉）（全文见 references/knowledge-base.md §下沉·r355C兼容性验证不能只判崩没崩字段移除后的真实表现是继续运行但降级能力按载体版本分档缺档是能用但少一档来源docsn）

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

## 可见性必须分层声明：元数据人人可见、正文按归属可见、管理视图只给 redacted（来源：docs.n8n.io `administer/manage-credentials/end-user-credentials.md` 9,720B，2026-10-03 r390A 独立 curl 取 `.md` 原文实拉；与 §留痕四态 coverage 互补——那条管留痕是否完整，本条管同一份留痕对不同人的可见面）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·可见性必须分层声明：元数据人人可见、正文按归属可见、管理视图）
## 影响边界声明：一个配置项改了什么不重要，重要的是它「不影响什么」；隐私类验收必问「防谁」（来源：docs.openclaw.ai/concepts/session 22,767B，2026-10-03 r390B 独立 curl 取 `.md` 原文实拉；与 §可见性三层 互补——那条管"谁看得到"，本条管"改了 A 会不会连带改了 B"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·影响边界声明：一个配置项改了什么不重要，重要的是它「不影响什）
## 留痕有两种缺口：旁路根本不进账，假名可以复原——覆盖声明必须同时给出「不覆盖清单」与「去标识的密钥在哪」（来源：docs.openclaw.ai `gateway/config-observability.md` 10,454B + `gateway/configuration-reference` 索引，2026-10-03 r391A 独立 curl 取 `.md` 原文实拉；与 §留痕四态 coverage / §审计分层视图 互补——那两条管状态枚举与跨层可见面，本条管账本本身的入口边界与可逆性）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·留痕有两种缺口：旁路根本不进账，假名可以复原——覆盖声明必须）
## 观测数据的裁剪必须选「安全侧」：只裁能重建的那一侧，裁完还超就失败而不是继续跑；取证默认面常常只够定位、不够复现（来源：www.activepieces.com/docs `install/troubleshooting/truncated-logs.md` 2,392B + pipedream.com/docs `workflows/building-workflows/errors.md` 9,150B，2026-10-03 r391B 独立 curl 取 `.md` 原文实拉；与 §截断自证 / §截断只作用展示面 互补——那两条管截断怎么声明与属于哪一面，本条管先裁哪一侧、裁完怎么办）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·观测数据的裁剪必须选「安全侧」：只裁能重建的那一侧，裁完还超）
## 「健康检查通过」要指明是哪个端点：存活不等于就绪，详细指标往往默认关闭；密钥类接口只返回元数据不返回材料（来源：docs.n8n.io `deploy/host-n8n/keep-n8n-running/monitor-n8n.md` 3,069B + `…/security/rotate-encryption-keys.md` 5,972B + `build/manage-workflows/view-change-history.md` 4,190B，2026-10-03 r391C 独立 curl 取 `.md` 原文实拉；与 §影响边界声明 / §声明集合≠生效集合 互补——那两条管改动与权限的声明面，本条管运行状态的探测面）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·「健康检查通过」要指明是哪个端点：存活不等于就绪，详细指标往）
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

## 审计事件名同词不同物会让「按名订阅」选错对象；自报字段不可当聚合键，聚合键必须自证稳定与校验（来源：docs.n8n.io `administer/observe-and-log/stream-logs-to-external-systems.md` 23,919B，2026-10-03 r408A 独立 curl 取 `.md` 原文实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·审计事件名同词不同物会让「按名订阅」选错对象；自报字段不可当）
## 观测数据的入口归因要能区分内部流量与真实用量；数据搬走不等于查不到，但取回是另一条有时效的通道（来源：docs.dify.ai `en/cloud/use-dify/monitor/logs.md` 6,019B（经 `_llms/en/cloud.md` 16,454B 定位真路径），2026-10-03 r408B 独立 curl 取 `.md` 原文实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·观测数据的入口归因要能区分内部流量与真实用量；数据搬走不等于）
## 产物可达性由落点目录决定，且「上传」是一道单向门：持久 ≠ 可取回（来源：docs.bigmodel.cn `cn/managed-agents/files.md` 4,911B + `create-session.md` 6,625B，2026-10-04 r410B 独立 curl 取 `.md` 原文实拉；与 §跨轮持久性分三层 / §归档是搬走不是删除但取回为两步异步产物 互补——那两条管"留多久"与"归档后怎么取"，本条管"同一个文件系统里不同目录的可取回性不同"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·产物可达性由落点目录决定，且「上传」是一道单向门：持久 ≠ ）
## 上下文量与超时预算必须同步放大；可选增强缺失时应「跳过本轮」而不是让主流程失败（来源：docs.openclaw.ai `concepts/active-memory/tuning.md` 4,601B，2026-10-04 r412C 独立 curl 取 `.md` 原文实拉；与 §产物可达性由落点目录决定 互补——那条管"产物放哪才拿得到"，本条管"可选的召回 / 增强环节在什么条件下该被放弃"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·上下文量与超时预算必须同步放大；可选增强缺失时应「跳过本轮」）
## 部分失败的三种降级语义决定的是「输出集合的形状」，下游按位置对齐一定会错位（来源：docs.dify.ai `en/self-host/use-dify/build/predefined-error-handling-logic.md` 3,788B，2026-10-04 r413B 独立 curl 取 `.md` 原文实拉；与 §可选增强缺失应跳过本轮 / §最小可用上下文优先 互补——那两条管"缺件时这一轮还出不出结果"，本条管"缺了几件之后结果长什么样"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·部分失败的三种降级语义决定的是「输出集合的形状」，下游按位置）
## 「ok」只说明这一轮跑完了，不说明里面的每一步都成了；诊断必须另有字段承载，且"没发生"要能区分「有意不送」与「想送没送成」（来源：docs.openclaw.ai `automation/cron-jobs/troubleshooting.md` 4,654B，2026-10-04 r413C 独立 curl 取 `.md` 原文实拉；与 §部分失败决定输出形状 / §可选增强缺失应跳过本轮 互补——那两条管"缺件后结果长什么样""缺件时还出不出结果"，本条管"结果状态位到底证明了什么"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·「ok」只说明这一轮跑完了，不说明里面的每一步都成了；诊断必）
## 压缩 / 摘要产物本身也要验收：写前校验 + 失败保留原物（来源：docs.openclaw.ai `concepts/compaction` 2026-10-04 r414A 独立 curl 取 `.md` 原文实拉；与 §ok 掩盖内部失败 / §状态位覆盖范围 互补——那条管"交付状态位证明到哪层"，本条管"压缩这个写操作自己有没有校验门"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·压缩 / 摘要产物本身也要验收：写前校验 + 失败保留原物）
## 交付 / 通知状态正确性：歧义态标记 Unknown 而非假成功，告警按原因去重（来源：docs.openclaw.ai `automation/cron-jobs/delivery.md` 19,524B，2026-10-04 r414B 独立 curl 取 `.md` 原文实拉；与 §ok 掩盖内部失败 / §状态位覆盖范围 互补——那条管"一轮跑完状态位证明到哪层"，本条管"交付这个异步动作自己的状态机怎么才不被误读"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·交付 / 通知状态正确性：歧义态标记 Unknown 而非假）
## 监视器信号也须可验证：静默失败≠健康、去重靠持久态而非记忆、检测只读（来源：docs.openclaw.ai `automation/cron-jobs/schedules.md` 16,129B，2026-10-04 r414B 独立 curl 取 `.md` 原文实拉；与 §ok 掩盖内部失败 互补——那条管"一轮结果的状态位"，本条管"无人值守监视器本身怎么设计才不会假健康"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·监视器信号也须可验证：静默失败≠健康、去重靠持久态而非记忆、）
## 空结果只在「陈旧标记缺席」时才构成结论；功能禁用要返回成功态而非错误；检测器扫不出来的东西要在准入期直接拒（来源：docs.openclaw.ai `cli/memory.md` 35,246B + `clawhub/security-audits.md` 5,974B，2026-10-04 r416B 独立 curl 取 `.md` 原文实拉；与 §状态位覆盖范围 / §输出形状契约 互补——那两条管"状态位覆盖到哪一层""降级后集合是什么形状"，本条管"空结果凭什么算数""扫不出来该表现为通过还是拒绝"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·空结果只在「陈旧标记缺席」时才构成结论；功能禁用要返回成功态）
## 观测的启用点决定它看不到的那一段；缺失的信号不构成对任何具体故障类别的证据（来源：docs.openclaw.ai diagnostics/flags.md 8,925B，2026-10-04 r417A 独立 curl 取 .md 原文实拉）
- 配置驱动的观测有自举盲区：flag 写在配置里时，「还没读配置」的启动最早段采不到，要看这段必须走进程外通道（环境变量 / 启动参数）。判据：观测的启用时点就是它的最早可见时点，想看更早的段只能换更早的注入点。
- 缺失的信号不反推故障类别：activity 采样含 bookkeeping 块，不证明有可见产出；延迟结算不会刷新已观测到的终态块；unknown reason 或 activity 缺席都不是 provider / timeout / CPU 失败的证据。从「没看到」只能得到「没看到」。
- 「不记什么」比「记了什么」更需要显式声明：明列不记 API key 与响应体之外，还要明写「查询词本身可能敏感」。脱敏清单必须同时给出排除面与残留敏感面，只给排除面会让残留面被当成已脱敏。
- 一次性静音必须能在不改持久配置的前提下完成：环境变量取 0 / false / off / none 时连配置里的 flag 一并关闭，卡在配置里的 profiler 不必编辑文件即可临时关掉。只读的临时覆盖通道是必需项，否则静音只能靠改配置加重启。

## 验证一条「拒绝」是否生效，必须先有一个「若规则失效则必然成功」的反证探针；拿不到反证时阻断与不可达不可区分（来源：docs.openclaw.ai security/network-proxy.md 21,937B，2026-10-04 r417B 独立 curl 取 .md 原文实拉）
- 阻断的验证比放行的验证难一个量级：放行只要看到成功即可，阻断必须证明「要不是被拦，这次本来会成功」。做法是发一个**只有规则失效才会返回成功**的探针（内置 loopback canary 带 per-run token），于是「拿到匹配 token 的响应」直接证明代理转发了本该拒绝的目标。
- 反证探针的判定必须写成四态而不是布尔：传输失败算通过（被挡）；非 2xx 且缺少探针 token 算通过；**2xx 却缺 token 算失败**（有别的东西意外成功了）；**任何带匹配 token 的响应算失败**（证明规则确实没生效）。
- 没有反证探针时就只能 fail-closed：自定义拒绝目标不带 token，于是任何 HTTP 响应都判为「可达」，连传输错误也算检查失败——因为无法区分「代理挡了一个可达源」与「别处出了故障」。**只有内置探针才允许把传输错误当作阻断的证据，这条豁免必须写进文档，否则会被当成通用规则误用。**
- 可达性的另一种证明是「可预期的确定性失败」：故意发一个无效 provider token，收到对端特有的 `403 InvalidProviderToken` 即证明隧道真的到达了对端——正向成功可能来自中间层缓存，而只有真实对端才产得出的错误码不可伪造。
- 验证通道自身的日志只记 destination / decision / status / reason，绝不记请求体、authorization 头、cookie 或其它秘密。校验用的 URL 凭据在文本与 JSON 两种输出里都要脱敏。
- 校验项要分清「通道级」与「进程全局」：`proxy.tls.caFile` 只作用于受管代理路由，而 `NODE_EXTRA_CA_CERTS` 是进程全局且必须在 Node 启动前设置，平台无法在运行中补加。**声明信任时必须同时声明作用域与注入时点**，否则「配了就该生效」的期待会落空。
- 校验探针本身失败不应阻断主流程：探针在预算内不回答时记 warning 并附下一步排查指引，主更新继续 best effort。探针是观测件不是准入件。

## 限流/预算的验收必须声明「计数面」：计的是运行还是物理投递，两者不可互换（来源：docs.openclaw.ai/channels/broadcast-groups.md 20,936B，2026-10-05 r418A 独立 curl 取 `.md` 原文实拉逐串命中；与 §扫描预算耗尽只允许降档验证 / §部分失败的三种降级语义决定输出形状 互补——那两条管额度耗尽后怎么判、缺件后结果长什么样，本条管额度本身数的是哪一个对象）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·限流/预算的验收必须声明「计数面」：计的是运行还是物理投递，）
## 扩展/钩子点只观察不突变：返回值惰性、副作用只能走 producer 拥有的投递通道且有结算窗口（来源：docs.openclaw.ai/automation/hooks/writing-hooks.md 11,109B，2026-10-05 r418B 独立 curl 取 `.md` 原文实拉逐串命中；与 §监视器信号也须可验证 互补——那条管「无人值守监视器」的只读与动作留载荷，本条管「插件/钩子扩展点」的返回惰性、投递归属与结算时序，两者是同一「观察者不改状态」原理在两个不同表面的落地）

## 攻击类评测的「成功判据」必须是合取式且逐项独立计数；通过率必须绑定攻击者画像，静态基准是下界不是上界（来源：docs.openclaw.ai/gateway/security/prompt-injection.md 8,479B，2026-10-05 r419B 独立 curl 取 `.md` 原文实拉逐串命中；与 §验收要报通过率与通过但偏离率双轴并带 Wilson 置信区间 / §验证拒绝须有反证探针 互补——那两条管"通过率怎么统计"与"拒绝怎么验"，本条管"什么叫一次成功攻击"这个判据本身的结构，以及分数脱离攻击者画像后还剩多少意义）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·攻击类评测的「成功判据」必须是合取式且逐项独立计数；通过率必）
## 并发配额必须声明「适用范围」：故障重跑与人工运维路径常天然在配额外；排队作业不可重试、放弃即出队、排队态是否跨重启保留须写明（来源：docs.n8n.io `deploy/host-n8n/configure-n8n/scaling/control-concurrency.md` 4,111B + `deploy/use-n8n-cloud/understand-concurrency.md` 3,828B + `deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/queue-mode.md` 12,687B，2026-10-05 r419C 经 `docs.n8n.io/llms.txt` 287,049B 定位真路径后独立 curl 取 `.md` 原文实拉；与 §限流/预算验收必须声明计数面 / §留痕覆盖声明要给出不覆盖清单 互补——那两条管"额度数的是哪个对象"与"留痕入口哪些不进账"，本条管"哪几类执行根本不进这个额度"）（细则见 KB，2026-10-11 r519 再下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·并发配额必须声明适用范围故障重跑与人工运维路径常天然在配额外排队作业不可重试放弃即出队排队态是否跨重启保留须写明来源do）
## 验收「请求值」不算数：只有回执里的生效值才是真相（来源：docs.openclaw.ai `tools/acp-agents/controls.md` 9,158B + `tools/acp-agents/sessions.md` 7,281B，2026-10-05 r420-A 独立 curl 取 .md 原文实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·验收「请求值」不算数：只有回执里的生效值才是真相）
## 「删除」是三态不是一态：标记 → 缓冲 → 永久，且用户标注即豁免（来源：docs.n8n.io `deploy/host-n8n/configure-n8n/scaling/manage-execution-data.md` 6,214B，2026-10-05 r420-B 经 llms.txt 287,049B 定位真路径后 .md 实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·「删除」是三态不是一态：标记 → 缓冲 → 永久，且用户标注）
## 公开面必须是「显式列举的窄面」，且关键命名空间由平台在所有方法上先行占用（来源：docs.openclaw.ai `web/control-ui/security-model.md` 12,843B，2026-10-05 r420-C 经 llms.txt 定位真路径后 .md 实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·公开面必须是「显式列举的窄面」，且关键命名空间由平台在所有方）
## 观测面必须自述覆盖边界：粗指标健康 ≠ 整体健康，判定输入要带「该信号能否证明细粒度失败不存在」（来源：docs.flowiseai.com/using-flowise/monitoring.md 7,765B，2026-10-05 r421-C 独立 curl 取 `.md` 原文实拉逐串命中；消化 Qoder r420-Q-A A-3 积压点）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·观测面必须自述覆盖边界：粗指标健康 ≠ 整体健康，判定输入要）
## 信任工件要「随行、机器可读、逐文件、会过期」：验证所需的元数据不写在工件正文里，而是另一份随行的独立记录（来源：developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/ 271,314B，2026-10-05 r422-B 独立 curl 实拉后去标签逐串命中；消化 Qoder r420-Q-B B-2 积压点，并更正其表述）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·信任工件要「随行、机器可读、逐文件、会过期」：验证所需的元数）
## 验收的对象必须是「用户真正拿到的那一个工件」，不是源树；且失败的检测通道不允许被调用方降级为警告（来源：docs.openclaw.ai `ci/release-validation/package-acceptance.md` 21,411B + `ci/release-validation.md` 4,562B，2026-10-05 r423-C 独立 curl 取 `.md` 原文实拉逐串命中；与随行信任记录 / 修复再检测互补——那两条管"第三方工件自带什么证据"与"修完要重测"，本条管"你测的到底是不是用户会拿到的那个东西"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·验收的对象必须是「用户真正拿到的那一个工件」，不是源树；且失）
## 无法被宿主解释的安全自陈是独立失败类：处置动作是「撤回这份声明」，不是忽略它、也不是降级为警告（来源：docs.openclaw.ai `clawhub/plugin-validation-fixes.md` 20,657B，2026-10-06 r428-A 独立 curl 取 `.md` 原文实拉、两个错误码段逐串命中；消化 Qoder r427-Q-A A-1 —— WB 已亲自复拉核验原文，未采信转述金句；与「verified 必须带可定位证据指针」互补——那条管"有声明但没证据"，本条管"有声明但没有任何 schema 能解释它"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·无法被宿主解释的安全自陈是独立失败类：处置动作是「撤回这份声）
## r429A · 判定必须与执行可分离重算；聚合须显式声明「部分覆盖」行为，禁止用（全文见 references/knowledge-base.md §r438C-sink1）
- **判据**：见下沉全文。（触发词保留在原 KB 条目）

## 聚合目录的剔除逻辑是「全否才剔」，因此「在架 / 已过审」不携带任何正向安全信息（全文见 references/knowledge-base.md §r438C-sink2）
- **判据**：见下沉全文。（触发词保留在原 KB 条目）

## 评测/报告产物分「可发布持久化面」与「仅诊断瞬态面」两层，分层的判据是「是否携带（全文见 references/knowledge-base.md §r438C-sink3）
- **判据**：见下沉全文。（触发词保留在原 KB 条目）

## 跨审计方对账的主键是内容哈希不是名称版本，且「没发现恶意」要拆成四档计数才可读（来源：skills.sh/audits 333,759B 一手 curl 实拉，2026-10-06 r432-B 逐串命中 `skillFolderHash` 75 处 / `purl` 25 处 / `summary` 四计数；与 §聚合目录剔除是逻辑与 互补——那条管聚合结论的方向，本条管聚合的对账键与计数口径）
- 原文事实：多家审计结果（含 `partner":"Socket"`）统一挂在 `skillFolderHash` 上（`"skillFolderHash":"0ca4cfe5…96e6"`）；第三方坐标写成 `"purl":"pkg:socket/skills-sh/<owner>%2F<repo>%2F<skillpath>%2F@<hash>"`——**`@` 后面是哈希不是版本号**；每份审计带 `summary:{"total_urls_checked":2,"malicious":0,"clean":0,"unknown":2,"errors":0}` 四计数分列。
- 判据：① **对账键必须是内容哈希**：多家的结论挂在目录内容哈希上，改名、改版本、换托管位置都不会让历史审计与对象脱钩；用名称或语义版本做键，改一次名就把结论与对象断开，表面上"审计还在"、实际已指向别的产物。② **外部坐标也用内容坐标**：`purl` 里 `@` 后是哈希而非版本 ⇒ 版本相同而内容不同的情况在其模型里根本不存在；引用第三方扫描结论时先确认它用的是内容坐标还是版本坐标，后者无法证明"你手里这份"被扫过。③ **`unknown` 与 `errors` 必须与 `clean` 分列**：上例 `total_urls_checked:2` 而 `clean:0 / unknown:2 / errors:0` —— 一个"零恶意"的审计完全可能由 100% `unknown` 撑起，**零 clean 不等于零风险，也不等于查过**；把 `malicious:0` 读成"通过"是误读。⇒ 引用审计结论时固定问两个数：`clean` 占 `total` 多少、`unknown+errors` 占多少。④ **同名字段可能混用哈希算法**：本次 75 处 `skillFolderHash` 中 **74 处 64-hex（SHA-256）、1 处 40-hex（SHA-1）** ⇒ 跨条对账前必须先声明算法并按长度机检，否则同一个字段名下的值不可比，对账会在静默中失效。
- 提升层：工作流 / 可复用 Skill。触发词：对账主键是内容哈希、skillFolderHash、purl 嵌哈希、四档计数、unknown 撑起零恶意、零 clean 不等于通过、哈希算法混用、跨审计方对账。

## 门禁作用域 ≠ 全量扫描作用域：发布门禁只阻断「过滤后 staged 子集」内的 finding，独立全目录扫描更宽 ⇒ 本地报警与发布通过可以同时为真，判重/误报复核前必须先对齐作用域（来源：docs.nvidia.com/skills/release-checklist.md 3,608B，2026-10-06 r434B 独立 curl 实拉逐串命中；与 §跨审计方对账主键是内容哈希 互补——那条管"两个审计方对不上时拿什么当主键"，本条管"两边根本没扫同一个范围时先别谈对账"）
- 原文逐字：Tier 1 先 staging 一份过滤副本再调扫描器；任意深度跳过 `evals/ .evals/ results/ .results/ versions/ .versions/ __pycache__/ .git/ .venv/ node_modules/`；对 `skill.oms.sig skill-card.md benchmark.md` 只过滤其单条 finding；`These files can remain in the staged copy, but their individual findings are not included in Tier 1 results. Only findings inside this scope are release-gate findings.` 且 `a standalone skillspector scan on the complete skill directory is broader`。
- 判据：① **同一个制品、同一时刻，两个扫描器给出相反结论是可以正常的**——一个按门禁作用域（过滤后）跑，一个按全目录跑；此时"本地报警 + 发布通过"不是矛盾、不是谁错了，而是**作用域不同**。先把两条结论各自的作用域问出来再判，否则会把"范围差"误判成"工具不可信"或"有人放水"。② **被排除的目录不是"不该有 finding"，而是"其 finding 不计入门禁"**：`evals/` 里的测试夹具按设计就该长得像攻击样本，原文明确 `do not thin fixtures to clear a broader standalone scan` ⇒ 为了让全目录扫描好看而删薄夹具，是拿安全资产去换一张好看的报告。③ **过滤的是 finding 不是文件**：三个生成产物可以留在 staged 副本里，只是它们的单条 finding 不计入 ⇒ "文件在" 与 "finding 计入" 是两件事，审计报告要能分别回答。④ **复现门禁结论必须用门禁那条路径**：`Use SkillEvaluator to reproduce what the gate enforces` ⇒ 想预判"这个包能不能过门禁"，跑全目录扫描是错的复现方式；验收脚本与门禁路径不一致时，绿灯/红灯都没有意义。⑤ 判重落点：共学判"这条是不是重复"时，先对齐双方说的作用域（门禁子集 / 全目录 / 单文件）；作用域不同时的"重复"与"不同"都不可比，未对齐作用域不得下判重结论。
- 提升层：工具 / 工作流。触发词：门禁作用域、staged subset、release-gate findings、全目录扫描更宽、本地报警与发布通过不矛盾、不要为过扫描删薄夹具、复现门禁要走门禁路径、判重先对齐作用域。

## 故障上下文按来源分两套键命名空间，而非在同一记录体加区分字段：执行期 `execution.id/url/error.message/stack/lastNodeExecuted/mode` 与触发期 `trigger.error.context/name/cause` 并存（来源：docs.n8n.io `build/flow-logic/handle-errors-gracefully.md`，2026-10-07 独立 curl 实拉；与 av「跨审计方对账主键是内容哈希」互补——那条管对账键，本条管故障账本的键空间设计）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·故障上下文按来源分两套键命名空间，而非在同一记录体加区分字段）
## 验真走两条路线且结论不可互相替代：目录树 detached 签名（严格模式=签名后新增未签名文件验证必失败，豁免须显式开 `--ignore-unsigned-files`）vs 服务端 verify envelope（sha 产物指纹 + 扫描裁决，无客户端可验签）；评审判据 = 「签名不证明安全，只证明发布物=被审物」，消费侧五条安装前清单含**本地任何修改后重跑验证**（来源：docs.nvidia.com/skills/signing-agent-skills.md 3,753B，2026-10-07 独立 curl 实拉逐串命中 `Detached`/`directory tree`/`ignore-unsigned-files`/`nv-agent-root-cert`/`does not prove`；与 sa「验签宽松开关是带文档化义务的例外」互补——那条在 sa 管"宽松开关结论两域"，本条在 av 管"两种验真路线对照 + 消费侧重验"）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·验真走两条路线且结论不可互相替代：目录树 detached ）
## 恶意有两档：第二档「零恶意件组合」没有攻击者意图可寻，只能靠组合级行为回归发现（来源：arxiv.org/html/2610.05943v1 210,175B，2026-10-07 独立 curl 实拉逐串命中 `evaluates skills in isolation` / `composition-induced risks underexplored` / `individually benign`；与 §恶意意图分散在多技能（SkillCascade）互补——那条靠关系图找"意图躲在哪件里"，本条处理"每件都干净"的组合涌现）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·恶意有两档：第二档「零恶意件组合」没有攻击者意图可寻，只能靠）
## 便宜的静态扫描不能代理 LLM 评审器（Spearman ρ = 0.14），且"平均增益"必须附正例占比与 CI 才能支撑"技能有效"（来源：arxiv.org/html/2608.20614v1 420,604B，2026-10-07 独立 curl 取 HTML 全文逐串命中 `structural versus LLM-judge Spearman ρ = 0.14` / `mean composite Skill Lift is 0.2134` / `95% paired-case CI [0.1967, 0.2301]` / `Composite lift is positive in 72.8% of paired cases`；与 §五千好过五万 / §四桶评测集 互补——那两条管评测量怎么选，本条管留出什么报告口径）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·便宜的静态扫描不能代理 LLM 评审器）
## 验收结论必须绑定 harness/工具链标识：同一技能集跨 harness 增益不同（NVIDIA Table 2：All dimensions Claude Code **+34** vs OpenAI Codex **+29**；SkillBench 直接以 24 个 model-harness 组合为评测单位）（来源：developer.nvidia.com/blog/evaluating-ai-agent-skill-performance-with-nvidia-skillevaluator/ 257,328B + skillsbench.ai 441,319B，2026-10-08 独立 curl 实拉逐串命中 `<td>All dimensions</td><td>+34</td><td>+29</td>` / `87 tasks across 8 domains and 24 model-harness configurations`；与 §均值须配 CI 与正例占比 互补——那条管一个增益数字要带不确定性，本条管这个数字必须带运行环境标识）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·验收结论必须绑定 harness/工具链标识：同一技能集跨 ）
## 场景级完成度（SGC）要与任务级成功率并列报：防止「单步都成功但整条场景目标未达成」被 SR 掩盖（来源：arxiv.org/html/2602.12430v4，2026-10-08 实拉逐串命中 `Scenario Goal Completion—an 8.9% absolute improvement over baseline GRPO without skill libraries—while requiring 26% fewer interaction steps`；全库 grep `SGC` 0 命中。与 §技能级 eval 五类 case family 互补——那条管用例覆盖面，本条管整条场景链目标是否达成）
- **判据**：任务级 SR 与场景级 SGC 是两个不可互相折算的口径，报告须并列给出。（细则见 references/knowledge-base.md §r437C-2）

## 审计台账要有一条「刻意不记什么」的负向清单：只留 provenance 与 result codes，明确排除 prompts / messages / tool arguments / tool results / raw errors（来源：docs.openclaw.ai/concepts/agent-loop 299,791B，2026-10-08 独立 curl 实拉逐串命中 `projects lifecycle and tool start/terminal events into the bounded, metadata-only audit ledger` / `records provenance and result codes without copying prompts, messages, tool arguments, tool results, or raw errors`；与 §主张级可审计四维 互补——那条管证据要充分，本条管留存要最小化）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·审计台账要有一条「刻意不记什么」的负向清单：只留 prove）
## 外部声明值必须「先对硬限额核对、再据此分配或放行」：把声明当不可信输入，核对通过才允许消费（来源：api.github.com/repos/langgenius/dify/issues/42021 一手 5,739B JSON，2026-10-08 r438C 独立 curl 实拉逐串命中 `pre-allocates a bytearray of the plugin-declared total_length` / `before validating it against max_file_size` / `the 30MB PLUGIN_MAX_FILE_SIZE limit is never consulted first` / `MemoryError`/`OverflowError` instead of the documented ValueError`；与 av §未声明就是未声明 互补——那条管"没声明"不能当默认，本条管"声明了"也不能当可信）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·外部声明值必须「先对硬限额核对、再据此分配或放行」：把声明当）
## 治理闭环的第一环是「连接存在性枚举面」：没有枚举就没有后续权限与审计——自助接入会形成不可见的影子集成层（来源：mcpmanager.ai/blog/mcp-statistics/ 一手 188,382B，2026-10-08 r438C 独立 curl 实拉逐串命中 `This creates a shadow AI and shadow MCP scenario` / `When you fail to provide a clear, safe path, workers will create an unmonitored one` / `83%` / `26% Have Comprehensive AI Security Governance` / `Under 1%`；全库 grep「影子集成 / 连接存在性 / 枚举面」0 命中，既有「影子副本」指产物副本属另一轴）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·治理闭环的第一环是「连接存在性枚举面」：没有枚举就没有后续权）
## 技能审计要从「逐个看 SKILL.md」升级为「依赖图指标」：单包审查看不到的风险多数在传递依赖里（来源：arxiv.org/html/2607.01136v1 209,169B，语料 1,434,046 条，2026-10-08 一手实拉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r513A · 技能审计要从「逐个看 SKILL.md」升级为「）

## 引用外部风险条目时「编号」与「当页定义」必须双写：同一编号在不同文档里指的不是同一件事（来源：owasp.github.io/www-project-agentic-skills-top-10/risk-assessment.html 100,225B 对照主页，2026-10-08 一手实拉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r513A · 引用外部风险条目时「编号」与「当页定义」必须双写）

## 采信任何评测/扫描结论前先做「三查」：判定口径、横向排名可用性、口径切换敏感度（来源：oasb.ai/benchmark 60,443B，2026-10-08 一手实拉；解除 r438A 搁置）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·采信任何评测/扫描结论前先做「三查」：判定口径、横向排名可用）
## 记分表里「没测到」必须记 N/A 不能记 FAIL：跨不同覆盖面比较 pass 数是错误选型依据（来源：oasb.ai/docs 29,646B + /controls 76,804B + /eval 37,230B，2026-10-08 一手实拉逐串命中 `reported N/A, not FAIL, so scorecards stay comparable across tools with different surfaces` / `comparing pass counts across different capability sets`；与 §采信评测前三查 互补——那条管怎么读别人的结论，本条管自己这张记分表怎么打分）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·记分表里「没测到」必须记 N/A 不能记 FAIL：跨不同覆）
## 门禁退出码是稳定契约，且「覆盖缺口」必须并入阻断态；基线抑制只改风险分的口径、不改风险本身（来源：api.github.com/repos/NVIDIA/SkillSpector/readme 74,672B → base64 解码 53,566B 全文，2026-10-08 一手实拉逐串命中 `its exit code and JSON output are a stable contract` / `--fail-on-incomplete` found partial/incomplete analysis / `re-scans surface only *new* findings` / `It never executes the scanned skill`；与 §记分表 N/A 语义 互补——那条管表里怎么记，本条管门禁怎么判与怎么不误放行）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·门禁退出码是稳定契约，且「覆盖缺口」必须并入阻断态；基线抑制）
## 扫描「标记率」不等于风险规模：报告必须固定为「标记数 / 带上下文复核后可疑数」双列，一手漏斗在 238,180 个技能上是 46.8% → 0.52%（来源：arxiv.org/abs/2603.16572 42,685B，2026-10-08 一手 curl 逐串命中 `classify up to 46.8% of skills as malicious` / `only 0.52% remain suspicious after repository-aware analysis` / `238,180 unique skills`；与 §采信评测前三查 互补——那条管别人的结论能不能用，本条管自己这份扫描产出怎么报）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·扫描「标记率」不等于风险规模：报告必须固定为「标记数 / 带）
## 依赖图审计只看「集中度和冲突率」不够：含环率、隐形继承率、放大倍数是三个独立的图结构风险轴（来源：arxiv.org/html/2607.01136v1 209,169B，2026-10-08 一手 curl 逐串命中 `SDA achieves an overall F1 score of 0.95` / `30.41% of root skills with dependencies contain at least one skill in a cycle` / `22.42% gain packages only through reused skills` / `maxima of 347× for skills, 1,754× for packages` / `71.87% and 73.33% of packages, respectively, are inherited through skill reuse`；与 §r439A 依赖图指标（名称冲突率 58.73% / Gini 0.925-0.944 / 传递到达率 98.01%）互补——那条取集中度与冲突面，本条取图结构三件套）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·依赖图审计只看「集中度和冲突率」不够：含环率、隐形继承率、放）
## 「规则库有多大」必须到代码里数：README / docs / 源码三处口径不一致是常态，且第三方转述的缺项结论也可能是错的（来源：api.github.com/repos/NVIDIA/SkillSpector/contents/README.md 53,632B 逐串命中 `71 vulnerability patterns` across 17 categories（同串在 27/488 行各出现一次）；同仓 `src/skillspector/nodes/analyzers/pattern_defaults.py` 44,213B 代码级实测唯一规则 ID = **39**（SC1–SC10、PE1–3、TR1–3、AR1–3、AS1–3、EA1–5、LP1–4、MP1–3、OH1–3、RA1–2）、`PatternCategory` 枚举 = **18** 类、且 **SC7 在代码中存在**（`Code pulls a container image with signature or registry verification disabled`）；与 §门禁退出码是稳定契约 互补——那条管门禁行为，本条管「声称的规则覆盖」本身怎么核）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·「规则库有多大」必须到代码里数：README / docs ）
## 数值断言必须「回原文核语义」而非「只核字符串是否存在」：同一事实两处口径不同（OWASP AST01「100% 恶意同时用两向量」vs Snyk「91%」），且 1,467 是「≥1 缺陷」非「恶意载荷数」（来源：owasp.github.io AST01 + snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/，2026-10-08 一手 curl 逐串命中 `100% of malicious`/`both attack vectors`/`did:web`；r445C 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·数值断言必须「回原文核语义」而非「只核字符串是否存在」：同一）
## r350C · 验证执行面 ≠ 生产执行面（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r350C）

## 验收权限面：声明集合 ≠ 生效集合（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·验收权限面）

## 留痕的四态覆盖等级与「有留痕 ≠ 完整留痕」（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·留痕四态）

## r485B · 评测台账必须带「可复现四元组」；通过阈值是代码常量不是叙述；目录计数要带取数日期（来源：api.github.com/repos/NVIDIA/skills/contents/benchmarks.json 1,083,377B + api.github.com/repos/NVIDIA/SkillEvaluator/contents/src/skillevaluator/constants.py 21,302B + .../reporting/benchmark.py 51,774B，2026-10-10 r485B 一手 curl 实拉逐串命中 `environment` / `evaluator_version` / `dataset_digest` / `attempts_per_task` / `DIMENSION_VERDICT_PASS_THRESHOLD = 0.5` / `DIMENSION_VERDICT_NEUTRAL_THRESHOLD = 0.4` / `TIER3_LIFT_PASS_THRESHOLD = 0.05` / `TIER3_LIFT_FAIL_THRESHOLD = -0.10` / `QUALITY_DEFAULT_MIN_SCORE = 70` / `does not override this gate`）

- **★引用任何增益数字必须同带四元组**：`benchmarks.json` 每行固定含 `environment`（`k8s-sandbox`）、`evaluator_version`（`1.5.6`）、`dataset_digest`（`sha256:307ff8...`）、`attempts_per_task`（`1`）。判据：**没有这四项的 uplift 数字不可复现、不可比对**——`attempts_per_task=1` 意味着「单次尝试、无方差」，把它当稳定结论会系统性高估；换 evaluator 版本或换环境后同一技能的数字不可直接相减。
- **★覆盖率缺口是机读字段，不是报告里的形容词**：同文件 `skills_without_results` 明列 19 个「有卡无结果」的技能（`rag-eval`、`rag-perf`、`rag-blueprint` 等）。判据：**"评测了 405 个"与"405 个都有结果"是两句不同的话**——引用 `skill_count` 时必须同时报 `result_row_count` 与缺口名单长度，否则把未测项算进分母。
- **★通过阈值写成常量而非散文**：`DIMENSION_VERDICT_PASS_THRESHOLD = 0.5` / `NEUTRAL = 0.4` / `TIER3_LIFT_PASS = 0.05` / `TIER3_LIFT_FAIL = -0.10` / `QUALITY_DEFAULT_MIN_SCORE = 70` / `RUBRIC_MIN_SCORE = 60`。判据：**阈值必须能被 grep 到、能被 diff、能被 policy 覆写**（`benchmark.py` 允许覆写 `dimension_pass_threshold`）——只写在叙述里则无法机检，也无法证明两次判定同口径。
- **★目录计数是时变量，必须带取数日期**：本轮实测 `skill_count 405 / result_row_count 3795`，而 Qoder r483-Q-C 于 2026-10-09 记为 `401 / 3755`。判据：**同一上游一天内净增 4 个技能、40 行结果**，用目录规模做基线或做趋势时须写「取数日期 + 上游版本」，跨日引用等于拿两个不同的总体做比较。
- **与既有能力分工**：§「增益不得越过闸门」（r348C，来自 reports.mdx）管**通过判据的形状**（max-over-agents × 全维度合取、lift 只作诊断）；本条管**这些判据的数值从哪来、数字要带哪些上下文才可复现**——两者互补，不重复立点（`does not override this gate` 源码串本轮新增，仅作 r348C 的一手补证）。
- 提升层：工作流 / 可复用 Skill。触发词：可复现四元组、dataset_digest、evaluator_version、attempts_per_task、单次尝试无方差、skills_without_results、覆盖率缺口机读、阈值常量化、目录计数取数日期。

## 入口守卫的失败方向必须写明，且「拦下」可以是不留痕的：不匹配回什么码、表达式本身报错时放行还是拦、这次判定留不留痕，三问缺一就查不到自己被拦过（来源：docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook.md 12,270B，2026-10-10 一手 curl 逐串命中 `Requests that don't match receive a 200 response without creating an execution` / `If the expression fails to evaluate, n8n logs a warning and lets the request through rather than blocking it`；r486C 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·入口守卫的失败方向必须写明，且「拦下」可以是不留痕的：不匹配）
## 「阳性率最高」的扫描器在「确证恶意」上可能最低：覆盖率/准确率必须带分母口径，且 advisory-only 的信号不能反过来当准入证据（来源：openclaw.ai/blog/openclaw-nvidia-skill-security 45,746B，2026-10-10 一手 curl 逐串命中 `48.71` / `72.8` / `6.8` / `advis`；r486C 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·「阳性率最高」的扫描器在「确证恶意」上可能最低：覆盖率/准确）
## r488A · 「有终答」与「任务成功」必须是两个独立导出字段；凡只回传内容不回传成败位的自校验，其「非空即成功」推断不可采信（来源：docs.dify.ai/en/cloud/use-dify/nodes/agent.md 10,353B，2026-10-10 一手 curl 逐串命中 `Success Status` / `Final Answer` / `Tool Outputs` / `Agent Logs` 四者并列；r488A 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r488A · 「有终答」与「任务成功」必须是两个独立导出字）
## r488A-2 · 对外部能力下结论前，必须取机读契约件并与人类文档做参数差集：「文档没写」不等于「平台没有」（来源：skillsmp.com/openapi.json 13,344B + skillsmp.com/docs/api 503,097B，2026-10-10 一手 curl 对照，`searchId` 在渲染文档 **0** 命中、在 openapi.json **8** 命中；`hybrid` 1 vs 7；r488A 落地）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r488A-2 · 对外部能力下结论前，必须取机读契约件并与）
## r490B · 「端点不存在」的否证粒度是完整路径而不是资源；同一端点内参数效力还必须逐参数实测（来源：api.skillhub.cn 一手对照：`/api/v1/skills` 405、`/v1/skills` 405、`/skills?limit=3` 405，而 `/api/skills?limit=3` 200 / 34,650B（`data.total`=188,339）；同端点内 `limit=3` 与 `limit=100` 返回**完全同字节** 34,650B（实返固定 20 条），而 `page=2` 返回 36,404B 内容不同；2026-10-10 r490B 独立 curl 实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r490B · 「端点不存在」的否证粒度是完整路径而不是资源）
## r492B · ① 保证强度的档位只写在机读面不由人读页承载；② 判「参数被静默忽略」之前必须先证穿透 CDN，否则会把缓存未失效误判成参数无效（来源：clawhub.ai/api/v1/openapi.json 84,507B + skillsmp.com/api/v1/skills/search 响应头 `Cache-Control: public, s-maxage=600, stale-while-revalidate=3600`，2026-10-10 r492B 一手 curl / -I 实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r492B · ① 保证强度的档位只写在机读面不由人读页承载）
## r495B · 列表接口能不能当采集源，要过三道独立判据：页内是否自含重复、判级字段类型是否可信、取样间隔是否跨过缓存窗口（来源：api.skillhub.cn/api/skills 2026-10-10 r495B 一手 curl 四次实拉，`data.skills` 20 条 / `total` 188,351；同页连采三次 md5 全等 `9a7d93be…`；`page=1` 唯一 slug 19、`page=2` 唯一 slug 17、两页交集 **0**；首条 `labels` = `{"requires_api_key": "false"}`，另有条目为 `"true"`；`claim_state` = `unclaimed`、`claimed_user_handle` = null）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r495B · 列表接口能不能当采集源，要过三道独立判据：页）
## r495B · 幂等键绑定的是「意图 + 参数指纹」而不是「意图」：改参数不换键是冲突，且未提交与已提交两类失败的语义相反（来源：skillsmp.com/openapi.json 13,344B，2026-10-10 r495B 一手 curl 实拉逐串命中 `Generate one UUID per logical search; keep it for retries and pagination` / `changing query, filters or limit requires a new searchId` / `Failures release pending allowance, while an already committed response can be recovered with the same searchId` / `SEARCH_ID_CONFLICT: the UUID belongs to different search parameters; use a new UUID for the new search` / `SEARCH_PENDING: retry with the same searchId after Retry-After` / `Requests beyond the queryable result window are canonicalized to its final page` / `Keyword attempts, including invalid parameters and minute rejections, consume legacy daily quota`）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r495B · 幂等键绑定的是「意图 + 参数指纹」而不是「）
## r510A · 「可恢复」与「回调地址稳定」是两件事：运行时生成的恢复 URL 在部分重跑下会静默换掉，引用它作长期凭据前必须先证它在三种路径下不变（来源：docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait.md 11,403B，2026-10-10 r510A 一手 curl 200 实拉；逐串命中 `$resumeWebhookUrl`×3 / `Partial executions`×1 / `generated at runtime`×1 / `offloads the execution data`×1）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r510A · 「可恢复」与「回调地址稳定」是两件事：运行时）
## 「已设限」不等于「已限住」：配额/幂等/监听类配置的计数域要先问是全局还是 per-process（来源：docs.langflow.org/deployment-multi-worker 114,789B，2026-10-11 r511A 一手 curl 200 实拉；逐串命中 `LANGFLOW_RATE_LIMIT_STORAGE_URI` / `memory://` / `multiplied by the worker count` / `Must differ from the cache database index` / `any worker`）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·「已设限」不等于「已限住」：配额/幂等/监听类配置的计数域要）
## 否证结论必须自带覆盖声明：词形、页面、分母三件事任一未声明，「0 命中」不构成否证（来源：code.claude.com/docs/en/skills.md 106,661B + docs.langflow.org/environment-variables 116,839B + docs.langflow.org/deployment-multi-worker 114,789B，2026-10-11 r511A 一手 curl 200 实拉）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·否证结论必须自带覆盖声明：词形、页面、分母三件事任一未声明，）
## 评测要先验评分器本身：参考解验真、试次档以统计意图命名、阈值进 CI 退出码、评分对象是终态而非 stdout（来源：api.github.com/repos/mgechev/skillgrade/contents/README.md 19,220B，2026-10-11 r511C 一手 curl 200 实拉 + `Accept: application/vnd.github.raw+json`；逐串命中 `| --validate | Verify graders using reference solutions |`、`--smoke | 5`、`--reliable | 15`、`--regression | 30`、`--threshold=0.8 | Pass rate threshold for CI mode`、`exits with code 1 if pass rate falls below --threshold`、`graders score the resulting workspace state ... not your command's stdout`）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·评测要先验评分器本身：参考解验真、试次档以统计意图命名、阈值）
## 允许/拒绝清单是「按名字过滤」而不是「行为约束」：禁用写类工具不构成 shell 只读的证据（来源：docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated.md 9,792B，2026-10-11 r513A 一手 curl 200 实拉逐串命中 `deny always wins` / `If `allow` is non-empty, everything else is treated as blocked` / `filters tool availability by name; it does not inspect side effects inside` / `only changes session defaults ... it does not grant tool access`）（细则见 KB，2026-10-12 r526 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·允许/拒绝清单是「按名字过滤」而不是「行为约束」：禁用写类工）
## 重试产生的是「新运行身份」而非续跑：旧运行保留状态与历史，缓存按运行 ID 键控故不跨重试继承（细则见 KB，2026-10-11 r519 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·重试产生的是新运行身份而非续跑旧运行保留状态与历史缓存按运行ID键控故不跨重试继承）
## 同一状态类型下的两个具体状态可恢复性相反；Crashed 与 Failed 是不同终态；「迟到」是带阈值的独立状态（细则见 KB，2026-10-11 r519 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·同一状态类型下的两个具体状态可恢复性相反Crashed与Failed是不同终态迟到是带阈值的独立状态）
## 多数决审批的缺省失败方向是「永远等」而非「拒绝」；门槛是精确值；拒绝与超时默认冒泡为失败，要分开处理须显式开（细则见 KB，2026-10-11 r519 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·多数决审批的缺省失败方向是永远等而非拒绝门槛是精确值拒绝与超时默认冒泡为失败要分开处理须显式开）
## 多分支执行顺序是「确定性位置契约」：n8n 1.0+ 一条分支跑完再跑下一条（按画布位置从上到下、同高取最左），1.0 前跨分支轮询；顺序相关 bug 用固定分支输入顺序 / pin 分支输入复现，不归因随机（细则见 KB，2026-10-11 r520A 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·多分支执行顺序是确定性位置契约而非随机调度）
## 重试预算须给出可算公式与可枚举档位指数退避base乘multiplier乘attempt静态档先跑耗尽后传播与继续两档终态（细则见 KB，2026-10-11 r524A 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·重试预算须给出可算公式与可枚举档位）
## 自证式摘要不是签名同一供应方既给内容又给摘要证明力低于离线签名差异须按不匹配处理且不得加载（细则见 KB，2026-10-11 r524C 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·自证式摘要不是签名）
## 质检评分表须区分致命项与扣分项致命项不过即短路后续检查不再跑且分数本身失去意义（细则见 KB，2026-10-11 r524C 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·质检评分表须区分致命项与扣分项）

## 能否选对技能是与能否做对正交的独立能力轴须分开测量且选择能力存在模型规模乘枢纽规模双重门限（细则见 KB，2026-10-11 r525C 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r525C 能否选对技能是与能否做对正交的独立能力轴）
## 验证状态是离散分档不是连续可信度且bootstrap期锁定运行时不可变门控是验证级的函数签名不等于行为符合声明（细则见 KB，2026-10-12 r526A 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·验证状态是离散分档不是连续可信度）

## 扫描证据是结构化条目不是一句已通过字段集合即契约缺列判无结论status恒pass零信息量（细则见 KB，2026-10-12 r526B 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·扫描证据是结构化条目不是一句已通过）

## 参数化取数断言库里没有X之前须用回显与合法枚举证明过滤排序真的生效（细则见 KB，2026-10-12 r526C 下沉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·断言库里没有X之前必须先证明过滤与排序真的生效）

## SSRF 验收要区分「重解析绕过」与「混合应答」：一次 DNS 应答里同时含被封地址与放行地址时，必须整体拒绝而不是取并集放行（来源：api.github.com/repos/langflow-ai/langflow/releases?per_page=3 31,882B，2026-10-12 r527A 一手 curl 200 逐串命中 `v1.12.4` / `fix: reject mixed blocked DNS answers with IP allowlists by @erichare in .../pull/15334` / 同批 `fix(ssrf): pin direct Requests helper connections by @erichare in .../pull/15340`；r527A 落地）
- **实证**：Langflow v1.12.4 的安全修复条目不是"加一条 DNS 校验"，而是**拒绝混合型的被封 DNS 应答**（`reject mixed blocked DNS answers with IP allowlists`），即判定单元是「这一次解析返回的整个地址集合」，不是逐个地址。
- **判据**：① **两种绕过形态要分别建用例**：DNS rebinding 是**时间维度**——先给好地址过校验、再解析成坏地址；混合应答是**空间维度**——同一次应答里好地址坏地址并存。只测前者会把后者整条漏掉。② **放行的主语必须是"整个应答"而非"某个地址"**：一旦按地址逐个判，攻击者只要在同一域名下混入一个放行 IP 就能让整次解析通过 ⇒ 校验函数的返回类型应是"这次解析是否整体可信"，不是"哪些地址可用"。③ **IP 允许清单与 DNS 阻断必须联合判定**：修复标题把两者写在一起（`mixed blocked DNS answers` **with** `IP allowlists`）⇒ 只有 DNS 侧阻断、没有 IP 侧清单时，"该不该放行"没有确定答案；两套机制要同一处求值。④ **直连通道是绕过面**：同批 `pin direct Requests helper connections` 说明绕过不止发生在解析器上，还在"直连不走代理的 HTTP helper" ⇒ 审计出网路径时要穷举所有发请求的封装，而不是只审主客户端。
- 提升层：工作流（安全验收）/ 工具（出网校验）。触发词：mixed blocked DNS answers、混合应答整体拒绝、IP allowlist 联合判定、DNS rebinding 与混合应答分测、直连 helper 绕过。

## 掩码是双向写回协议不是单向隐藏：读侧给掩码必须配套按位置回填真值，无法定位的掩码返回422拒绝保存占位符，重试只恢复最初被掩码的那批字段（来源：api.github.com/repos/langflow-ai/langflow/pulls/15529 19,916B，2026-10-12 r528A 一手 curl 200 逐串命中 `fix(mcp): redact server credentials from management responses` / `MCP server GET, POST, and PATCH responses expose stored environment values, headers, and generated project API keys in mcp-proxy --headers arguments` / `Editing a masked config keeps the latest stored credentials by map key or header name and occurrence` / `Ambiguous or newly introduced masks return 422 instead of saving placeholder values` / `Restore only the originally masked graph fields on every retry`；r528A 落地）
- **实证**：Langflow v1.12.5 PR #15529 的修复不是"把敏感值从响应里删掉"，而是**在保留服务端可执行真值的前提下返回掩码**——原文 `Return masks for these values while preserving decrypted configs for server execution`；并配套四条写回规则：按 `map key or header name and occurrence` 回填最新存储的凭据、替换与删除仍可用、模糊/新引入掩码 `return 422` 而不是存占位符、保存 flow 时 `Restore only the originally masked graph fields on every retry, leaving other nodes' explicit references intact`；另有 `Encrypt new header arguments at rest and retain compatibility with legacy plaintext configs` 与 `reject masks without an existing value owned by the caller before staging writes`。自述 76 条聚焦后端测试 + 52 条后续套件测试通过。
- **判据**：① **脱敏的验收对象是"双向协议"而不是"单向隐藏"**：读侧给掩码只是半个协议，写侧必须能把掩码映射回真值，否则用户一保存就把占位符当成新密码写进去——**"保存成功"在掩码系统里是危险信号，正确行为是显式 422**。② **回填的定位键是"位置"而非"值"**：按 map key / header name + 出现序号定位 ⇒ 改名、重排、增删同名字段都会让回填错位，回填方案必须先声明"以什么为键"。③ **恢复范围要收敛到被掩码集合**：原文 `only the originally masked graph fields` ⇒ 重试不是全量重放，恢复范围超出掩码集合就会覆盖别处的显式引用，制造"我没改这个字段却被改了"的故障。④ **加密面与兼容面必须同时声明**：新 header 参数 at rest 加密，同时 `retain compatibility with legacy plaintext configs` ⇒ "已加密"只对新建成立，存量明文仍在库里，审计要按新旧两段分别算覆盖率。⑤ **掩码的所有权要可判定**：`without an existing value owned by the caller` ⇒ 掩码不能凭空产生，提交方必须对该值有既有所有权；无主的掩码在 staging 写入前拒绝。⑥ **落地验收动作**：取一次管理接口响应 → 把掩码**原样**回写 → 检查真值未被占位符覆盖。只验"响应里没有明文"只覆盖了半个协议。⑦ 与 §脱敏是返回面的承诺不是存储面的承诺（KB:2752）互补：那条管"返回不吐 ≠ 服务端没有"，本条管"返回吐了掩码之后，写回这条路径会不会把真值弄丢"。
- 提升层：工具（凭据掩码协议）/ 工作流（安全验收）。触发词：mask 回写、422 拒绝占位符、按 map key 回填真值、脱敏双向协议、重试只恢复掩码字段、legacy 明文兼容、掩码所有权。

## 权限的签发面与执行面是分离的：非管理员也能给自己签上 admin scope，令牌自带的 scope 清单不能当权限证据，必须在执行侧用响应码探测（来源：developers.make.com/api-documentation/authentication/api-scopes-overview.md 11,643B，2026-10-12 r528B 一手 curl 200 逐串命中 `Even if you are not the administrator, you can assign to your token the scopes meant for administrators. However, if you try to access the admin resources as a regular user, you will receive the 403 Access denied error in response.` / `There are two types of scopes - read and write` / `Some resources require more than one scope`；r528B 落地）
- **实证**：Make API 的作用域只有 `:read` / `:write` 两型，且**签发时不校验角色**——不是管理员也能把 `admin:read` / `admin:write` 勾到自己的令牌上；校验发生在访问那一刻，普通用户访问管理资源返回 `403 Access denied`。原文还写明 `Some resources require more than one scope`，以及管理端点的可达性本身还随平台形态变化（云版普通用户进不了管理界面，本地版带 platform administration 角色的用户可以）。
- **判据**：① **令牌上写着什么，与这个令牌能做什么，是两件必须分别取证的事**：签发面不校验角色 ⇒ 拿到一枚含 `admin:write` 的令牌，**不能**推出持有者是管理员，也不能推出他能动管理资源。审计权限时的正确动作是**执行侧探测**（发一个真实请求看响应码），而不是读令牌声明。② **失效方向要写清楚**：本例是"**过授予、实际受限**"——授予面比执行面宽。与 §签名≠行为符合声明（av 2.197.0 / sa KB:2680）**方向相反**：那条是声明强于实际（说得到做不到），本条是授予强于实际（签得到用不了）。两者都要报，但补救动作不同——前者要补运行时验证，后者要补签发侧校验或明确"签发不校验"是设计选择。③ **"签发不校验"本身要被显式声明**：既然 403 只在访问时出现，系统必须在文档里写明"scope 可在签发时任意选择"，否则使用者会把"我能勾上"误读成"我有这个权限"，进而把 403 当 bug 上报。④ **作用域的类型数与资源的所需数是两个独立维度**：两型（read/write）× 单资源多 scope ⇒ 建模权限时不能假设"一个资源一个 scope"，要有"所需 scope 集合"这种一对多结构。⑤ **同一 scope 在不同平台形态下可达性不同**（云版 vs 本地版）⇒ 权限矩阵的行列里要带上"部署形态"这一维，否则跨环境验收会得出相反结论。
- 提升层：工具（权限取证）/ 工作流（安全验收）。触发词：签发面 vs 执行面、scope 不是权限证据、403 在访问时、过授予实际受限、admin scope 非管理员可签、单资源多 scope。
