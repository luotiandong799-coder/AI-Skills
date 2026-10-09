---
name: wb-artifact-verification
description: >-
  对"生成出来的东西"做独立验证并给出明确的成功/失败判定。当用户要求"验证生成结果""验证这个脚本/代码能不能跑""验证是否成功""帮我确认结果对不对""check 一下生成物""验证执行结果"，或给出"先生成再验证再反馈"这类任务时使用。核心是三条互相独立的证据源（独立算法 oracle / 外部已知常数 / 随机差分模糊测试）+ 故障注入（变异测试）证明验证器本身有检出能力，禁止只跑一次"看起来没问题"就宣布成功。另含"证明检查真的跑到了"：非零退出不等于检出（import 报错/构建失败也非零），须打到达标记；被测方须侧盲；判不出结果时"不确定"是一等判定，不得默认通过、不得伪造因果。另含"验证通道禁止副作用"：验证命令不得借检查之名做发布/部署/推送/外发。触发词：验证、验证结果、验证一下、能不能跑、跑通了吗、对不对、check 一下、测一下、自检、回归、真的修好了吗、看起来没问题、绿灯、都过了、测试全绿、失败注入、变异测试、假阳性、伪成功、静默测错、不确定、证不出来、证据不足、评分器、评测、基准、对照实验、抽样、覆盖率、未测、跳过、flaky、可复现、脚本化验证、退出码、超时、只读验证、别在验证里发布。、失败分类法、置信度阈值过滤误报、批量失败、单条失败、占位保配对、条数对齐、失败归属到条、来源自证端点、代理后静默失效、我看你是谁、限流失效、真实来源核验、评测续跑、只重放未完成、改了实现要全量重跑、续跑可比性、自描述元数据、写入方版本、序列化器不可用、解码失败不等于值错、绕过读取通道、过期检查在读取路径、合法 JSON 不等于合规、结构检查三态、解析失败vs字段不合规、轨迹同构三元组、完成度不能从最终答复推断、逐子任务报告、工具三判、误读返回值、恰好一次、exactly once、副作用重复、审计重复、重放重复、结算标记、合并前钩子、占用分解、扫描根、观测面盲区、分解为空、不是我的证据、盘满但分解小、换证据源、告警缺席、钩子被吞、缓存命中不触发、钩子计数翻倍、per-attempt钩子、静默失效、告警不算证据、数据飞轮、过闸才上线、来源优先级、合成数据垫底、轨迹优先、分层切分、五千好过五万、反馈版本化、跨家族互评、模式坍缩、四桶评测集、失败重放、回归还是漂移、定期重跑、置信门槛、rescore 重算判定、整臂聚合扣留、部分覆盖聚合
version: "2.172.0"
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
## "verified" 必须携带可定位的证据指针且由校验器机械强制：空指针行直接拒（来源：github.com/dshworks/awesome-dsh-plugins `data/plugins.json` + `scripts/validate.mjs`、skills.sh/、arXiv 2609.14079，2026-10-01 r362-Q-C 实拉）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r439·verified必须携带可定位的证据指针且由校验器机）

## "索引层无数值" 是可交付结论，不是抓取失败：Flowise/LangFlow 索引层零字段须逐页且如实记"不可判"（来源：docs.flowiseai.com/llms.txt、docs.langflow.org/llms.txt、docs.dify.ai/.../knowledge-request-rate-limit、list-workflow-logs，2026-10-01 r362-Q-C 实拉；承接 r326 失效四形态）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r439·索引层无数值是可交付结论不是抓取失败FlowiseL）

## 迁移开关要分「可逆」与「不可逆点」；配置存在 ≠ 配置生效，验收须查该旋钮当前版本是否仍被消费（来源：docs.n8n.io `/deploy/host-n8n/configure-n8n/durable-scheduler.md`，2026-10-01 r348A 独立 curl 实拉；经 Qoder r363-Q-A 提名）（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r439·迁移开关要分可逆与不可逆点配置存在配置生效验收须查该）

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

> 本节原文已零删减下沉 `references/knowledge-base.md §r442C 下沉：任务成功不是安全信号；技能自带的非文本资产是扫描器看不到的指令载体（来源：arXiv 2609.35912 MMSkillRisk 44,757B，2026-10-01 r348C 独立 curl 实拉，`43.1%` / `16.4 percentage points` / `36.5%` / `72.2%` 逐串命中）`（正文预算 ≤500 行）

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

## r353A · 失败现场的处置由开关决定，取证能力会被隐私开关直接削掉

> 原文已下沉 `references/knowledge-base.md §r395-av`（保持原文零删减）。
## r353B · 错误契约随失败位置分叉，取证通道可用 `.md` 后缀直取

> 原文已下沉 `references/knowledge-base.md §r395-av`（保持原文零删减）。
## r353C · 事务边界由模块能力标注决定；验证有自己的预算币种；文档站提供问答式检索接口

> 原文已下沉 `references/knowledge-base.md §r395-av`（保持原文零删减）。
## r354A · 留痕按「失败优先」分级保存；删除是两阶段，且活跃态与人工标注豁免（来源：docs.n8n...（全文见 references/knowledge-base.md §下沉·wb-artifact-verification·r440B·r354A · 留痕按「失败优先」分级保存；删除是两阶段，且活跃态与人工标）
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


## 部分失败的三种降级语义决定的是「输出集合的形状」，下游按位置对齐一定会错位（来源：docs.dify.ai `en/self-host/use-dify/build/predefined-error-handling-logic.md` 3,788B，2026-10-04 r413B 独立 curl 取 `.md` 原文实拉；与 §可选增强缺失应跳过本轮 / §最小可用上下文优先 互补——那两条管"缺件时这一轮还出不出结果"，本条管"缺了几件之后结果长什么样"）
- **原文**：「`terminated` - Stops processing immediately when any item fails (default)／`continue-on-error` - Skips the failed item and continues with the next one／`remove-abnormal-output` - Continues processing but filters out failed items from the final output」「When you set an iteration to `continue-on-error`, **failed items return `null` in the output array**. When you use `remove-abnormal-output`, **the output array only contains successful results, making it shorter than the input array**.」「**The default value must match the node's output type** -- if it outputs a string, your default must be a string.」「**Loop nodes always stop immediately** when any child node fails… **Iteration nodes** let you choose how to handle child node failures」
- **判据**：① **降级策略是一个"形状契约"而不是容错开关**——同样"跑完 10 个里失败 2 个"，三种语义分别产出：中断（0 条）/ 等长含两个 `null`（10 条）/ 变短（8 条）。下游凡是按下标对齐输入输出、或断言"输出条数 == 输入条数"的验证，只有第二种成立。⇒ 验收产物时必须先问"这次收集用的是哪一种语义"，否则"少了两条"既可能是失败也可能是设计。② **占位与剔除必须二选一且要写明**——保留 `null` 占位能对齐但会把空值往下传；剔除能保干净但**破坏位置对应关系**。混合使用（部分剔除部分占位）是最难排查的形态。③ **降级值也是契约的一部分：类型必须与成功产出一致**——默认值必须匹配节点输出类型（string 输出 ⇒ 默认值必须是 string）；类型不符时"降级成功"反而制造了下游类型错误，把一次可恢复失败变成一次难定位的崩溃。④ **控制流节点之间的错误语义并不一致**——Loop 任何子节点失败即整体终止且**不提供继续选项**，Iteration 才可选三种；同为"循环"却有两种不同契约 ⇒ 换控制流节点等于换错误处理语义，重构时这条容易漏。⑤ 对验证的落点：产物/结果集的验收清单里增加一项"**形状假设**"——声明本批次预期是等长还是变短、空位用什么表示；不声明形状，"通过"就只是"没抛异常"。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：部分失败输出形状、continue-on-error、remove-abnormal-output、null 占位、降级值类型必须匹配、Loop 与 Iteration 错误语义不一致。


## 「ok」只说明这一轮跑完了，不说明里面的每一步都成了；诊断必须另有字段承载，且"没发生"要能区分「有意不送」与「想送没送成」（来源：docs.openclaw.ai `automation/cron-jobs/troubleshooting.md` 4,654B，2026-10-04 r413C 独立 curl 取 `.md` 原文实拉；与 §部分失败决定输出形状 / §可选增强缺失应跳过本轮 互补——那两条管"缺件后结果长什么样""缺件时还出不出结果"，本条管"结果状态位到底证明了什么"）
- **原文**：「A run can finish **`ok` after an exec call fails** and the agent replies. Check `diagnostic:` in `openclaw automations show <jobId>` or `diagnostics` in run history; unresolved exec failures produce a **warning without exposing command arguments**.」「When the dispatcher records **intentional suppression**, job state, run history, and finished events include `deliverySuppressionReason` (`empty`, `silent`, `heartbeat`, or `channel_transform`). This is **separate from `lastDeliveryError` / `deliveryError`**; required delivery failures also log an error when they happen.」「`handler-unavailable` means the heartbeat service was not registered or stopped during the wait. The attempt is recorded as **skipped**.」
- **判据**：① **成功终态与内部失败可以合法共存**——exec 失败后 agent 仍然作答，整轮记为 `ok`；把状态位当作"无失败"的证据，会让内部失败永不进入统计。⇒ 验收时必须声明状态位覆盖到哪一层（"跑完了"还是"每一步都成了"），并给出旁路诊断字段的位置。② **诊断信息要单独成字段，不能塞进状态**——`diagnostic:` / `diagnostics` 与状态并存；且**脱敏是硬约束**（"warning without exposing command arguments"），诊断不能因为要可排查就把参数原文吐出来。⇒ 可观测性的两条底线在这里相遇：要么有旁路字段，要么就什么都查不到；同时旁路字段本身也是泄漏面。③ **"没发生"必须二分：被抑制 ≠ 失败**——`deliverySuppressionReason`（empty / silent / heartbeat / channel_transform）与 `lastDeliveryError` / `deliveryError` 两套字段分开；抑制是"我们决定不送"，失败是"想送没送成"。合成一个"未送达"计数会让**有意的静默**被当成故障去修，也会让**真失败**被当成设计放过。④ **跳过要留明确终态而不是不记录**——`handler-unavailable` 记为 skipped 而非缺省；不记录的跳过与"没到这一步"无法区分。⑤ 对验证的落点：产物/交付验收表增加两列——**状态位覆盖范围**（证明到哪一层）与**未发生的原因分类**（抑制枚举 / 真实错误 / 未到该步）；只打一个勾的验收对这三类同等放行。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：ok 掩盖内部失败、diagnostic 旁路字段、deliverySuppressionReason、抑制不等于失败、skipped 终态、状态位覆盖范围。

## 压缩 / 摘要产物本身也要验收：写前校验 + 失败保留原物（来源：docs.openclaw.ai `concepts/compaction` 2026-10-04 r414A 独立 curl 取 `.md` 原文实拉；与 §ok 掩盖内部失败 / §状态位覆盖范围 互补——那条管"交付状态位证明到哪层"，本条管"压缩这个写操作自己有没有校验门"）
- **原文**：「With the built-in safeguard quality guard enabled, OpenClaw applies the final summary budget before validation. **Required headings must remain in the retained generated body, while pending asks and exact identifiers must remain in the exact text** that would be stored. **Invalid output gets only the configured number of corrective attempts. If no finalized summary passes, compaction stops before writing a transcript entry, keeps the original history, and surfaces the existing recovery outcome.**」
- **判据**：① **压缩输出本身是一次写操作，落库前必须过校验门（qualityGuard）**——生成的摘要里必要的标题 / 待办项 / 精确标识符必须还在；凡是没有这道门的压缩，等于"把可能坏掉的上下文直接覆盖上去"。⇒ 压缩产物要像外部交付物一样验收，不是"压完就生效"。② **校验不过的处置是保留原物、不是覆盖**——任何一次尝试都没通过时，停在原历史、返回压缩失败，**绝不写入已知无效的上下文**；这和"覆盖式压缩"是两种相反语义，后者会把坏摘要当成真相。③ 对验证的落点：压缩 / 摘要类产物的验收表增一列——**写前校验是否通过 + 失败时是否保留原物而非覆盖**；只报"已压缩"的验收对"压出来的是不是坏的"同等放行。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：压缩产物写前校验、qualityGuard、校验不过保留原物、摘要不可覆盖式写入、无效上下文拒绝落库。

## 交付 / 通知状态正确性：歧义态标记 Unknown 而非假成功，告警按原因去重（来源：docs.openclaw.ai `automation/cron-jobs/delivery.md` 19,524B，2026-10-04 r414B 独立 curl 取 `.md` 原文实拉；与 §ok 掩盖内部失败 / §状态位覆盖范围 互补——那条管"一轮跑完状态位证明到哪层"，本条管"交付这个异步动作自己的状态机怎么才不被误读"）
- **原文**：「An HTTP rejection records **Not delivered**. If the request may have reached the receiver but its response is lost or times out, delivery stays **Unknown**; the transport does not retry that ambiguous send.」「Repeated failures with the same cause form one incident and do not send repeated alerts, even after the cooldown expires or the Gateway restarts. A changed cause or destination can send a new alert after the cooldown. A successful run clears the incident and its cooldown without sending a notification.」「a run can record `status: "ok"` with `completionStatus: "failed"`. It does not increment the execution-failure streak or backoff.」
- **判据**：① **歧义发送（可能已送达但回执丢失/超时）必须标记 Unknown，绝不重试**——重试要么造成重复投递、要么因"已成功"而误判；把 Unknown 当失败重发或当成功跳过，都会污染下游对账。⇒ 异步交付的终态至少有三态（delivered / not-delivered / unknown），验收必须把 unknown 当成一等公民，不能归并进"成功"或"失败"。② **告警按原因去重，不是按发生次数**：同因连续失败 = 一个事故，冷却过期、Gateway 重启都不重发；原因变化或一次成功才解除并静默清除。⇒ 告警疲劳的根因是"每次发生都发"，正确粒度是"每个新原因发一次"。③ **`status:ok` 与 `completionStatus:failed` 是独立两维**——交付失败不计入执行失败连击、不触发执行侧熔断；把两者混成一个"失败"会让交付问题错误升级为执行熔断。⇒ 验收异步任务时，运行态与交付态分开读，不互相污染计数。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：歧义发送标记 Unknown、不重试歧义、告警按原因去重、同因一事故、status 与 completionStatus 两维、交付失败不连击。

## 监视器信号也须可验证：静默失败≠健康、去重靠持久态而非记忆、检测只读（来源：docs.openclaw.ai `automation/cron-jobs/schedules.md` 16,129B，2026-10-04 r414B 独立 curl 取 `.md` 原文实拉；与 §ok 掩盖内部失败 互补——那条管"一轮结果的状态位"，本条管"无人值守监视器本身怎么设计才不会假健康"）
- **原文**：「Author watchers around **actionable state**, not only success: a watcher that goes quiet when its check fails or times out looks healthy while broken.」「Compare the observation with `trigger.state` and return fresh state to deduplicate; do not rely on model or process memory.」「write scripts as read-only checks and keep actions in the payload. ... If a fired payload run fails, the returned `state` is **not** persisted — the next evaluation sees the previous state and can fire again.」
- **判据**：① **监视器围绕"可行动状态"设计，而非只看成功**——检查在失败/超时时若静默，看起来健康实则已坏；验收无人值守监视器时，先问"它失败时还报不报"，不报的就是假健康。② **去重靠持久态比对，不靠模型/进程记忆**：每次把本次观测与上次持久化的 `trigger.state` 比对，变化才触发；不要让模型"记住"是否已报过——跨重启/跨进程记忆不可信。⇒ 判重原语是"存储里的上一状态"，不是"模型觉得"。③ **检测只读、动作留载荷**：检查失败 → 状态不持久化 → 下次还能再触发，所以检查本身不得做变更（变更放 payload）；把副作用写进检测器，会丢失"失败后自愈重试"的能力。⇒ watcher 的 fire 信号本身是可验证产物：它必须基于持久态比对、且检测与动作分离，信号才可信。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：监视器看可行动状态、静默失败假健康、去重靠持久态不靠记忆、检测只读动作留载荷、fire 信号须可验证。


## 空结果只在「陈旧标记缺席」时才构成结论；功能禁用要返回成功态而非错误；检测器扫不出来的东西要在准入期直接拒（来源：docs.openclaw.ai `cli/memory.md` 35,246B + `clawhub/security-audits.md` 5,974B，2026-10-04 r416B 独立 curl 取 `.md` 原文实拉；与 §状态位覆盖范围 / §输出形状契约 互补——那两条管"状态位覆盖到哪一层""降级后集合是什么形状"，本条管"空结果凭什么算数""扫不出来该表现为通过还是拒绝"）
- **原文**：「…`stale: true`, plus `warning` and `action` fields. Treat an empty `results` array as authoritative **only when `stale` is absent**.」；「Disabled memory returns `{"agentId":"main","status":"disabled"}` with a successful exit.」；「A.I.G 0.2.1 cannot inspect packaged Python bytecode. Until Tencent ships its [CVE-2026-84809] fix, ClawHub **rejects skills containing `.pyc`, `.pyo`, or `.pyd` files before A.I.G runs.** ClawScan also detects packaged Python bytecode independently.」
- **判据**：① **空结果的权威位来自"数据是否新鲜"，不是来自"返回了空数组"**：召回为空只在 `stale` 缺席时才是"确实没有"的结论；陈旧时空数组必须并带 `warning` 与 `action`（下一步动作） ⇒ 把空数组一律当结论，会把"索引还没建好"读成"确认不存在"，且不会有人去修。② **"没启用"与"出错了"必须是两种返回**：mem（功能禁用）返回 `status:"disabled"` 且**退出码成功** ⇒ 禁用是合法状态不是故障；把它当错误会让健康检查永远红，也会淹没真实的取数失败。③ **检测器的盲区要反向写进准入规则**：扫描器读不了打包字节码，正确做法不是"扫不出就放过"，而是注册表**在扫描之前**直接拒该文件类型，并钉 CVE 编号、明说是**过渡规则**（等上游修好可撤） ⇒ 扫不出来的东西如果表现为"通过"，检测覆盖面就成了一个随扫描器版本漂移的隐性变量。④ **独立第二检测面是过渡期的配套**：ClawScan 独立检测同类文件 ⇒ 单一检测器的缺口期必须有旁路，否则"先拒"会连带拒绝所有依赖该形态的正常内容。⑤ 对验收的落点：验收表要能回答三件事——「这个空结果依据的数据是否新鲜」「这个状态是禁用还是失败」「这个'通过'是检测过还是根本没检测」。
- 提升层：可复用 Skill 治理 / 验收。触发词：空结果权威位、stale 标记、禁用返回成功态、禁用≠失败、检测器盲区反向准入、扫不出即拒、过渡规则钉 CVE、独立第二检测面。

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

## 限流/预算的验收必须声明「计数面」：计的是运行还是物理投递，两者不可互换（来源：docs.openclaw.ai/channels/broadcast-groups.md 20,936B，2026-10-05 r418A 独立 curl 取 `.md` 原文实拉逐串命中；与 §扫描预算耗尽只允许降档验证 / §部分失败的三种降级语义决定输出形状 互补——那两条管额度耗尽后怎么判、缺件后结果长什么样，本条管额度本身数的是哪一个对象）

- **原文**："`maxTurns` counts **agent runs started by the coordinator**, including runs that pass or fail."；"Slots are reserved synchronously before parallel launch… If the budget is smaller than the eligible participant count, configured order determines which turns start."；"A turn can produce **multiple platform messages** through chunks, previews, or message-tool sends… **`maxTurns` does not count, buffer, or cap physical messages.**"；"Agents fail independently. One agent's error is logged… and **does not block the others**."
- **判据**：① **验收限流前先问「数的是哪一个」**——把「启动次数」当「投递条数」验收，会在一次运行拆成多条投递时误判超额，反过来会把被 chunk 撑大的真实投递量整段放过；两个数字必须分列，不得互相替代。② **额度对尝试计数，不对成功计数**：失败与弃权同样吃掉额度 ⇒ 「还剩多少次」永远是尝试次数，不是「还能成几次」，把剩余额度当产能估算是错的。③ **并行前的槽位预留使取舍是确定性的**（按配置顺序取前 N），验收要能复现「谁没被启动」，随机丢弃说明预留环节没生效。④ **多执行体的失败相互独立** ⇒ 编排类验收必须有「部分失败」这一独立终态，且它是**完成态的一种**，不是「整体失败」也不是「整体成功」；只报总数会把它抹平。⑤ **与既有「四态」口径一致**：留痕四态（enforced / attribution-only / unknown / unsupported）解决「判出来是什么」，本条解决「判之前先确认在数什么」——这是验收的前后两道关，缺一不可。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：限流验收、计数面、物理投递、chunk 拆分、槽位预留确定性、部分失败独立终态、尝试计数非成功计数。

## 扩展/钩子点只观察不突变：返回值惰性、副作用只能走 producer 拥有的投递通道且有结算窗口（来源：docs.openclaw.ai/automation/hooks/writing-hooks.md 11,109B，2026-10-05 r418B 独立 curl 取 `.md` 原文实拉逐串命中；与 §监视器信号也须可验证 互补——那条管「无人值守监视器」的只读与动作留载荷，本条管「插件/钩子扩展点」的返回惰性、投递归属与结算时序，两者是同一「观察者不改状态」原理在两个不同表面的落地）

## 攻击类评测的「成功判据」必须是合取式且逐项独立计数；通过率必须绑定攻击者画像，静态基准是下界不是上界（来源：docs.openclaw.ai/gateway/security/prompt-injection.md 8,479B，2026-10-05 r419B 独立 curl 取 `.md` 原文实拉逐串命中；与 §验收要报通过率与通过但偏离率双轴并带 Wilson 置信区间 / §验证拒绝须有反证探针 互补——那两条管"通过率怎么统计"与"拒绝怎么验"，本条管"什么叫一次成功攻击"这个判据本身的结构，以及分数脱离攻击者画像后还剩多少意义）
- **原文**：「a 2026 crowdsourced arena of 272K attacks across 41 agent scenarios — **scored only when the agent both executed the harmful action and hid it from the user** — success rates were 0.5% for Claude Opus 4.5, 1.0% for Sonnet 4.5, 1.3% for Haiku 4.5, and 8.5% for Gemini 2.5 Pro」；「**Adaptive human attackers still break models that score well on static benchmarks**, with published success rates above 80% against state-of-the-art defenses once the attacker adapts」；「Robustness tracked capability within a model family」；「treat model choice as your first and cheapest layer, then keep hard enforcement … for anything whose blast radius you would not accept on a bad day」；「Prompt injection does not require public DMs … **The content itself is a threat surface, not just the sender.**」
- **判据**：① **成功判据要写成合取并逐项计分**：本例「执行了有害动作 ∧ 对用户隐瞒」才算一次成功——只执行（会被发现）与只隐瞒（没真做）都不算 ⇒ 把复合判据简化成任一条件，会把"吵闹但无害"与"无害但撒谎"一起计进失败率，指标立刻失去区分度；凡攻击 / 注入 / 越狱类验收，先问"成功的定义是几个条件的 AND 还是 OR，各条件是否分别留痕"。② **百分比必须绑定攻击者画像，脱离画像的分数不可比较**：静态基准 0.5% 与自适应人类 >80% 描述的是同一批模型 ⇒ 报通过率必须同时报"谁在攻、允许多少轮适配、能否看到反馈"，否则两个分数并列就是把下界当上界。③ **静态基准是下界不是上界**：基准分高只说明"这套固定题没被打中"，可以给能力排序，不能给安全性背书 ⇒ 安全结论必须补自适应红队，或至少显式声明未做。④ **能见度是判据的一级字段，不是事后查日志**：把"是否隐瞒用户"写进成功定义，等于承认"可被观测"本身就是一种防御 ⇒ 设计验收时把"动作是否留痕 / 是否对用户可见"作为一级字段。⑤ **分层防护的层数由爆炸半径决定，不由"哪层更强"决定**：模型选择是最便宜的第一层，工具策略 / 沙箱 / 白名单留给"坏日子里不能接受其爆炸半径"的部分 ⇒ 把硬约束一律上提会把成本付在不值得的地方，把软约束当唯一防线则连下界都没有。⑥ **威胁面是内容不是发件人**：即使只有可信发送者，被读取的网页 / 邮件 / 附件 / 粘贴的日志代码同样携带对抗指令 ⇒ 收窄入站身份 ≠ 收窄注入面，两者必须分别验收。
- 提升层：可复用 Skill / 验证方法论。触发词：攻击判据合取、执行且隐瞒才算成功、静态基准是下界、自适应攻击者、百分比绑定攻击者画像、能见度是一级字段、爆炸半径决定防护层、威胁面是内容不是发件人。

## 并发配额必须声明「适用范围」：故障重跑与人工运维路径常天然在配额外；排队作业不可重试、放弃即出队、排队态是否跨重启保留须写明（来源：docs.n8n.io `deploy/host-n8n/configure-n8n/scaling/control-concurrency.md` 4,111B + `deploy/use-n8n-cloud/understand-concurrency.md` 3,828B + `deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/queue-mode.md` 12,687B，2026-10-05 r419C 经 `docs.n8n.io/llms.txt` 287,049B 定位真路径后独立 curl 取 `.md` 原文实拉；与 §限流/预算验收必须声明计数面 / §留痕覆盖声明要给出不覆盖清单 互补——那两条管"额度数的是哪个对象"与"留痕入口哪些不进账"，本条管"哪几类执行根本不进这个额度"）
- **原文**：「Concurrency control **applies only to production executions**: those started from a webhook or trigger node. It doesn't apply to any other kinds, such as **manual executions, sub-workflow executions, error executions**, or started from CLI.」；「You **can't retry queued executions**. Cancelling or deleting a queued execution also removes it from the queue.」；「On instance startup, n8n **resumes queued executions up to the concurrency limit and re-enqueues the rest**.」；「Evaluation test runs use a **separate concurrency limit** from production executions（Community/Pro 1、Business 3、Enterprise 5）」；「Concurrency control is **disabled by default**.」；「Too many concurrent executions thrash the event loop … queue up any concurrent production executions over the limit … processed in FIFO order.」
- **判据**：① **额度声明必须带「不适用范围」清单**：手动执行、子工作流、错误执行、CLI 启动统统不进生产并发配额 ⇒ 只知道"限 20"而不知道"哪几类不限"，等于不知道系统在什么情况下会被打穿。② **最需要额度的时刻往往在额度之外**：错误执行（失败重跑）与人工运维执行被排除在配额外，而故障期恰恰是重跑与人工干预最密集的时候 ⇒ 设计配额时先问"故障时走的是哪条路径"，那条路径若不受限，限流就只是健康期的装饰。③ **重试资格由"是否已开始"决定，不由"是否失败"决定**：排队中（未开跑）的作业不接受重试，重试等于重复入队/插队；取消或删除即从队列移除、不可恢复 ⇒ 把"重跑"接在排队项上会制造幽灵副本，把"取消"当成暂停会误以为还能回来。④ **排队态是否跨重启保留必须显式声明**：本例重启后恢复到上限、其余重新入队（积压可恢复），而 OpenClaw 的编排预算状态在内存、重启即丢且不续 ⇒ 同一个"排队中"在两种系统里命运相反；验收无人值守流程时必须单问一句"积压在重启后还在不在"。⑤ **评测/测试流量与生产流量必须分额度**：评估用例走独立限额 ⇒ 若共享额度，"跑一次全量评测"就吃掉生产吞吐；若评测完全不受限，它就成了第二条旁路。⑥ **限流默认关闭意味着"有没有限"本身就是待验项**：不能假定并发保护已生效 ⇒ 验收表要留三格——**是否启用 / 限多少 / 覆盖哪些执行类型**，缺任一格都无法判断限流是否真的挡在最坏情况的路上。
- 提升层：工作流 / 验证方法论。触发词：配额适用范围、不适用范围清单、错误执行不受限、故障期旁路、排队作业不可重试、取消即出队、排队态跨重启、评测独立额度、限流默认关闭。

- **原文**："A handler exports a function returning `void` or `Promise<void>`… **Returned values do not block, cancel, or rewrite the operation.**"；"Treat context as an **observation, not a live state-editing API**… patch events carry **cloned snapshots**."；"Pushing to `event.messages` is **not a general send-message API**… **Append messages before the handler's promise settles**; detached work that pushes later can miss the producer's delivery step."
- **判据**：① **扩展点返回值惰性**：钩子/handler 的返回值永远不阻断、不取消、不改写被装饰的操作 ⇒ 扩展点是旁路观察，不是控制流的一部分；把它当「返回 false 就中止」来设计会静默失效。② **上下文是观测快照不是活状态 API**：事件 `context` 是克隆快照（patch 事件带 cloned snapshots），扩展点拿不到也不该拿到可变活状态 ⇒ 想「在钩子里改状态」必须走 producer 自己拥有的通道，不能借观测通道偷改。③ **副作用只能走 producer 拥有的投递通道且有结算窗口**：推到 `event.messages` 不是通用发信 API，只有特定 producer 消费它，且必须在 handler 的 promise settle 之前追加，detached 后推的会错过投递 ⇒ 扩展点副作用有确定归属与时序窗口，乱发即丢。④ **与监视器只读同根不同面**：核心都是「观察者不改状态」，但监视器是无人值守检测（只读 + 动作留载荷），扩展点是装饰器/钩子（返回惰性 + 投递归属 + 结算窗口）；验收扩展机制时分别检查「返回值是否惰性」「副作用是否走对通道且在窗口内」，不能只问「它读不读」。
- 提升层：可复用 Skill / 工作流。触发词：扩展点返回惰性、钩子不阻断、context 是观测快照、副作用走 producer 投递通道、结算窗口、detached 错过投递、观察者不改状态。


## 验收「请求值」不算数：只有回执里的生效值才是真相（来源：docs.openclaw.ai `tools/acp-agents/controls.md` 9,158B + `tools/acp-agents/sessions.md` 7,281B，2026-10-05 r420-A 独立 curl 取 .md 原文实拉）
- **实证**：官方原文「When a backend returns its accepted controls, OpenClaw keeps an already-selected thinking level in sync with that response. A model switch may lower the level or remove thinking support; subsequent turns and reconnects use the accepted selection instead of replaying the old level.」「Backend defaults do not become new session overrides, and unsupported inherited defaults dropped during new session initialization are not saved as overrides.」；`sessions_spawn` 明确「does not accept per-call timeout overrides (`runTimeoutSeconds`/`timeoutSeconds` are rejected with a config-the-default error)」；harness 未 advertise model controls 时「an explicit selection fails; an inherited default may be omitted so the harness can use its own default」。
- **判据**：① **意图与真相必须分成两个字段，验收只认后者**——写下"我请求了 X"不等于"X 生效了"；任何可调旋钮都要回读后端接受的生效值，模型/档位/超时这类被静默降级的参数尤其如此。② **显式与隐式走不同失败语义**——显式指定失败是**错误**，继承默认可省略是**沉默**；验收时不能把两者都写成"没设上"，前者必须报错可见，后者必须明确声明是省略而非失败。③ **被丢弃的默认不得写成 override**——不支持的继承值被丢掉后不保存为显式覆盖，否则"我从未要求过"会变成"我要求过但被拒"。④ **有些旋钮只在配置层存在**——调用层传同一个参数是**被拒绝**而非被忽略；验收须先确认该旋钮在哪个层可调，再判断"没生效"属于哪一类。⑤ 验收表增一列：**生效值来源**（回执 / 继承默认 / 显式覆盖 / 被降级）。
- **与既有能力分工**：§状态位覆盖范围（2.134.0）管"ok 覆盖到哪一层"；§拒绝须有反证探针（2.139.0）管"阻断与不可达如何区分"；本条管**"配了"与"生效了"之间那段被静默改写的过程**。
- 提升层：工作流。触发词：回执才是真相、请求值 vs 生效值、静默降级、显式失败 vs 继承省略、被丢弃的默认、旋钮层级、生效值来源。


## 「删除」是三态不是一态：标记 → 缓冲 → 永久，且用户标注即豁免（来源：docs.n8n.io `deploy/host-n8n/configure-n8n/scaling/manage-execution-data.md` 6,214B，2026-10-05 r420-B 经 llms.txt 287,049B 定位真路径后 .md 实拉）
- **实证**：官方原文「pruning first marks targets for deletion, and then later permanently removes them」；「Pruning honors a safety buffer period of `EXECUTIONS_DATA_HARD_DELETE_BUFFER` hours (default: 1h), to ensure recent data remains available while the user is building or debugging a workflow」；「Executions with the `new`, `running`, or `waiting` status aren't eligible for pruning」；「Annotated executions (for example, executions with tags or ratings) are never pruned」；剪枝触发为 age **或** count 两者任一；「May not strictly prune back down to the exact max count」；「the disk space of any pruned data isn't automatically freed up but rather reused」；二进制剪枝只作用于**当前活跃存储模式**（从 S3 切到 filesystem 后只剪 filesystem）。
- **判据**：① **删除必须拆成"标记 / 缓冲 / 永久"三态并分别可验**——把标记当成已删会在缓冲窗口内丢数据；把已删当成空间已回收则磁盘告警永远解释不通。② **回收资格由生命周期状态决定，不是由年龄决定**——未终态对象（`new`/`running`/`waiting`）一律不可回收，否则清掉的正是还在跑的东西。③ **用户的轻量标注是隐式保留声明**——打 tag / 评分这类低门槛动作能压过全局保留策略；保留策略必须显式列出"豁免面"，否则会出现"我明明标了重要却被清了"。④ **两个独立触发条件要各自可观测**——age 与 count 任一触发即行动，只盯一个条件会漏掉另一条路径上的删除。⑤ **上限是不等式不是等式**——文档自陈"可能不会精确回落到上限"，验收不得断言"条数 == 上限"。⑥ **删除 ≠ 回收空间**，回收是另一个动作（vacuum / 重建），两者必须分别在验收表里占一行。⑦ **剪枝面等于当前配置面**——换了存储介质后，旧介质上的历史数据不在剪枝范围内，表现为"清了但残留还在"。
- **与既有能力分工**：ctx 3.311.0 管上下文层的修剪/压缩双杠杆；ag Cap32 管备份是泄漏面；本条管**产物与记录层的保留/回收生命周期**——"清掉了没有""清的是不是该清的""空间回来没有"三问。
- 提升层：工作流 / 可复用 Skill。触发词：删除三态、缓冲窗口、标注即豁免、未终态不可回收、删除不等于回收、剪枝面等于配置面、保留策略验收。


## 公开面必须是「显式列举的窄面」，且关键命名空间由平台在所有方法上先行占用（来源：docs.openclaw.ai `web/control-ui/security-model.md` 12,843B，2026-10-05 r420-C 经 llms.txt 定位真路径后 .md 实拉）
- **实证**：官方原文公开渲染器「reads only user messages and assistant final-answer text. It omits tools, reasoning, files, images, widgets, hidden messages, and internal metadata, and applies credential-pattern redaction」；令牌「is the read capability and does not reveal the agent, session key, session ID, or publication ID」；「Treat the complete URL as public: anyone who receives it can read existing and future published text until the creator or a Gateway admin disables access」；登录代理「bypass authentication only for the Control UI's `/share/*` namespace. Keep the WebSocket, bootstrap, API, dashboard, and all other routes protected」；审批链接「identifies the approval, never authorizes it」，且「The approval namespace is reserved by the Gateway ahead of plugin HTTP routes for **all** HTTP methods, so a plugin route can never shadow or intercept an approval document」；「Signing in on an approval document is ephemeral … it does not overwrite the gateway selection or settings saved by the full Control UI」。
- **判据**：① **公开面用白名单枚举，不用"脱敏后的全集"**——允许哪几类字段要逐条写出来（只含用户消息与最终答案），凡没列举的一律不可见；"我们把敏感字段都脱敏了"是黑名单思路，漏一项就是一次泄漏。② **能力令牌本身不得携带元数据**——token 只证明"能读"，不暴露它指向哪个 agent / 会话 / 发布 ID；把标识编进令牌等于把内部拓扑公开。③ **分享是持续授权不是一次性快照**——拿到链接的人能读到**未来新增**的已发布内容，直到显式关闭；验收必须测"发布后追加的内容是否也可见"，只测当下内容是假通过。④ **旁路认证必须精确到命名空间**——只放行 `/share/*`，WebSocket / bootstrap / API / dashboard 全部保持受保护；按"路径前缀"放行会把同前缀的管理接口一起放开。⑤ **关键命名空间要由平台在所有 HTTP 方法上先行占用**——只占 GET 会让插件用 POST/DELETE 遮蔽或劫持同一路径；预留声明必须写明"全部方法"。⑥ **临时认证不得污染持久配置**——在审批页登录是临时态，不能覆盖完整界面保存的网关选择与设置。⑦ 验收表增三列：**公开面是否白名单枚举** / **令牌是否携带元数据** / **旁路是否精确到命名空间且覆盖全部方法**。
- **与既有能力分工**：Cap32 管「备份是泄漏面」；av 2.138.0 管「脱敏清单须同时给排除面与残留敏感面」；本条管**对外暴露面的形状与边界**——不是"脱敏干不干净"，而是"根本有没有把不该进的面挡在外面"。
- 提升层：安全边界 / 工作流。触发词：公开面白名单、令牌不携带元数据、分享是持续授权、旁路精确到命名空间、命名空间全方法预留、临时认证不污染持久配置。

## 观测面必须自述覆盖边界：粗指标健康 ≠ 整体健康，判定输入要带「该信号能否证明细粒度失败不存在」（来源：docs.flowiseai.com/using-flowise/monitoring.md 7,765B，2026-10-05 r421-C 独立 curl 取 `.md` 原文实拉逐串命中；消化 Qoder r420-Q-A A-3 积压点）
- **实证**：官方原文「Flowise has native support for Prometheus with Grafana and OpenTelemetry. **However, only high-level metrics such as API requests, counts of flows/predictions are tracked.** Refer … for the lists of counter metrics. **For details node by node observability, we recommend using Analytic.**」；同页「`/api/v1/metrics` endpoint requires API key authentication」。
- **判据**：① **"有监控"必须同时声明监控的分辨率**——只有请求数/流程数这类高层计数器，逐节点可观测要换另一套工具 ⇒ 不写覆盖边界时，"指标全绿"会被读成"系统没问题"，而实际它只证明了"入口还活着"。② **验收观测系统要问一个是否题**：这个信号能不能证明"细粒度失败不存在"？能证明才算该层的证据，不能证明的必须注明它缺哪一层 ⇒ 把高层指标当低层证据，是"监控很全但故障发现不了"的头号成因。③ **观测缺口要给出替代通道而不是留白**——官方直接指明逐节点用 Analytic ⇒ 凡"我这层看不到"的能力，应有一条指到能看到的通道；只说"暂不支持"等于让使用者自己猜。④ **观测端点本身就是暴露面**——指标端点需 API key ⇒ 加观测不能顺手加一个未鉴权的入口。⑤ 与既有「监视器信号可验证 / 采集结论三态」分工：那两条管**单次信号靠不靠谱**，本条管**整套观测面覆盖到哪一层**——前者是信号质量，后者是覆盖面声明。
- 提升层：工作流 / 校验纪律。触发词：only high-level metrics、观测分辨率声明、粗指标健康不等于整体健康、该信号能否证明细粒度失败、观测缺口指替代通道、指标端点需鉴权。

## 信任工件要「随行、机器可读、逐文件、会过期」：验证所需的元数据不写在工件正文里，而是另一份随行的独立记录（来源：developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/ 271,314B，2026-10-05 r422-B 独立 curl 实拉后去标签逐串命中；消化 Qoder r420-Q-B B-2 积压点，并更正其表述）
- **实证**：官方原文「Each verified skill is cataloged **daily** from the owning product team, scanned for software and agent-native risks with SkillSpector, **signed with a detached skill.oms.sig**, and documented with a **skill card describing ownership, dependencies, limitations, and verification status**.」；「The skill card provides a **machine-readable trust record** that developers and enterprise teams can review to understand capabilities, risks, and validation status **before deployment**.」；「a publishing flow that can include both human review and automated policy checks, followed by **scanning, evaluation, generation of the skill card, signing, cataloging**, and synchronization into the public catalog」；「Cryptographic signing covers **every file in the skill directory** so developers can verify authenticity and integrity **after download**.」
- **判据**：① **信任记录必须是与工件并行的独立文件（detached），不是写进正文的段落**——正文可被工件自身改写，独立签名记录不可 ⇒ 让被验对象自己声明"我已通过验证"，等于没有验证；验证结论要放在它改不到的地方。② **记录要包含「不能证明什么」**——四要素里 `limitations` 与 `ownership` 并列：谁负责、依赖什么、**已知限制是什么**、验证到什么状态 ⇒ 只写"已通过"不写"限制"的信任卡，是把结论当成属性，不能支撑使用方的判断。③ **签名覆盖目录内每个文件，不是只签清单或摘要**——「every file in the skill directory」⇒ 只签清单会留下"新增文件未入清单也未签名"的注入口；验收完整性时要问"新增一个文件是否会被发现"，而不是"清单对不对得上"。④ **信任状态是每日重算的快照，会过期**——「cataloged daily」⇒ 一次验证结论不是永久属性；复用旧结论前必须核对它的刷新周期与生成时刻，过期结论与未验证同价。⑤ **产物面向"部署前的人"，不是"运行时的机器"**——卡片给开发者/企业团队在部署前审阅 ⇒ 机器可读不等于自动放行；机器可读解决的是"人能不能快速看懂"，不是"能不能跳过人"。⑥ **生产分工**：扫描→评估→生成卡片→签名→编目，卡片是**机器产出、人审阅** ⇒ 把逐次人工审计降级为"人核验机器产出"，人留在核验位而非产出位。
- **与既有能力分工**：上一版（观测面自述覆盖边界）管"监控能证明什么"；本条管"第三方工件自带的可信证据该长什么样、怎么验它没过期"。
- 提升层：可复用 Skill / 校验纪律。触发词：随行信任记录、detached 签名卡、machine-readable trust record、逐文件签名、每日重编目、限制字段、结论会过期、机器产出人核验、部署前审阅。

## 验收的对象必须是「用户真正拿到的那一个工件」，不是源树；且失败的检测通道不允许被调用方降级为警告（来源：docs.openclaw.ai `ci/release-validation/package-acceptance.md` 21,411B + `ci/release-validation.md` 4,562B，2026-10-05 r423-C 独立 curl 取 `.md` 原文实拉逐串命中；与随行信任记录 / 修复再检测互补——那两条管"第三方工件自带什么证据"与"修完要重测"，本条管"你测的到底是不是用户会拿到的那个东西"）
- **实证**：官方原文「normal CI validates **the source tree**, while package acceptance validates **a single tarball** through the same Docker E2E harness **users exercise after install**」；流水线 `resolve_package` 解析出**一个**候选并产出 `package-candidate.json` → `package_integrity` 用 `scripts/check-openclaw-package-tarball.mjs` 强制公开 tarball 契约 → `npm_12_install_sh` **经公开 Linux 安装器**在隔离 home/prefix 安装该工件并校验 CLI 版本、生命周期完成守护与**已安装树体积预算** → `docker_acceptance` 用同一 harness 复跑；收口「`summary` fails the workflow if package resolution, integrity, npm 12 installer acceptance, Docker acceptance, or the optional Telegram lane failed. Selected lanes keep their first failure; **callers cannot downgrade a failing test to a warning**.」
- **判据**：① **源树通过 ≠ 交付物可用**：CI 验的是源码树，用户拿到的是打包后的单一 tarball ⇒ "测试全绿但装上就坏"的根因是**验证对象错位**，不是测试不够；验收链路里必须有一环把"经公开安装路径安装之后的形态"作为被测物，而不是复用构建产物目录里的同名文件。② **验收要走与用户相同的入口**：用公开安装器装到隔离 home/prefix，再跑同一套 E2E harness ⇒ 走内部/特权安装路径会系统性跳过用户实际会踩的打包、权限、路径、体积问题；判断一条验收是否可信，先看它装东西的方式和用户一不一样。③ **打包契约要有独立强制器**：tarball 契约由专门脚本单列一步（`package_integrity`），与安装、E2E 分成不同阶段 ⇒ 契约检查不能被"反正装完会跑测试"顺带覆盖：**装不上与装上不对是两种失败**，合并成一步时前者会被后者掩盖成"测试没跑"。④ **规模预算是验收项而不是优化项**：安装后强制检查已安装树体积（`check-openclaw-installed-package-budget.mts`）⇒ 依赖膨胀在功能测试里永远测不出来（功能全绿而体积翻倍），必须单独设一道。⑤ **失败的车道保留第一次失败，调用方无权把 failing 降级为 warning**：原文明写 callers cannot downgrade ⇒ 允许调用方"降级"的门禁等于没有门禁，谁能把红按成黄，谁就是实际上的放行方；验收结论的可信度取决于**最没有利害关系的那个人能不能推翻它**。⑥ 对 guild 的落点：任何"生成物交付前验收"，先回答三问——被测物是源还是工件？安装路径与用户一致吗？谁能把失败改成警告？三问答不全，验收只是跑了一遍测试。
- 提升层：可复用 Skill / 校验纪律。触发词：验收对象是交付物不是源树、package acceptance、公开安装器、隔离 prefix、独立打包契约、安装树体积预算、失败不可降级为警告、callers cannot downgrade、源树通过不等于装上可用。

## 无法被宿主解释的安全自陈是独立失败类：处置动作是「撤回这份声明」，不是忽略它、也不是降级为警告（来源：docs.openclaw.ai `clawhub/plugin-validation-fixes.md` 20,657B，2026-10-06 r428-A 独立 curl 取 `.md` 原文实拉、两个错误码段逐串命中；消化 Qoder r427-Q-A A-1 —— WB 已亲自复拉核验原文，未采信转述金句；与「verified 必须带可定位证据指针」互补——那条管"有声明但没证据"，本条管"有声明但没有任何 schema 能解释它"）
- **实证**：官方原文 `security-manifest-schema-unavailable` 段「The package ships `openclaw.security.json` with a schema reference that ClawHub **does not recognize as available**.」处置「Remove the schema URL if it is advisory-only. Use a documented versioned schema only after OpenClaw publishes one.」；`unrecognized-security-manifest` 段「The package ships an unsupported security manifest file.」处置「**Remove `openclaw.security.json` until OpenClaw documents a versioned security manifest schema and ClawHub behavior. Keep security-sensitive behavior documented in your public package docs or README until the manifest contract exists.**」；同页另有 `manifest-unknown-fields` / `manifest-unknown-contracts` 两个并列错误码。
- **判据**：① **不可机检的声明比没有声明更糟**——制品自带的"我是安全的"自陈，一旦宿主没有任何版本化 schema 能解释它，读者会默认它已被审过，而它实际上从未被任何校验器读过 ⇒ 留着它等于生产**假安心**；官方给的处置是**删除声明文件**，既不是宽容忽略（→假安心），也不是降级为警告（→噪声里没人再看）。② **"无从判定"是与"违规"并列的独立失败类，两者处置动作不同**——违规要改内容让它合规；无 schema 可依要**撤回声明**，两者各有独立错误码（`schema-unavailable` 与 `unrecognized`）⇒ 把"无从判定"塞进"通过"是假安心，塞进"违规"会让作者去改一个根本没人能读的字段，两种都是把失败分类做错。③ **契约存在之前，把敏感行为放进人能读的面**——官方要求改用 public docs / README 承载安全敏感行为说明 ⇒ 机器不可读时的正确落点是人可读面，不是删掉信息，也不是硬塞进不可校验的结构里等未来有人实现。④ **与邻近能力的分工**：av 已有「`verified` 必须带可定位证据指针、空指针行直接拒」管"有声明没证据"（缺的是证据）；本条管"有声明但没有任何契约能解释它"（缺的是**解释它的 schema**）——证据再全也补不上契约缺席，两者落在不同一层、不可互相替代。⑤ 对 guild 的落点：给技能包 / 插件包写任何安全、权限、合规自陈之前，先确认消费侧存在**版本化的 schema 能解释这个字段**；没有就不要写，把内容放人可读的 README，等契约出现再结构化为声明。
- **配套判非（同步登记）**：A-1 另两点经全库 grep 判非 —— ①「三态门（通过 / 违规 / 无从判定）」⇒ `wb-debug-loop` 已落「门禁退出码必须把『有发现』与『不可用』分开」（`1` 有发现 / `2` 结论不可用 / 目标不存在另给码），重叠 >60%；②「不对称审批（收缩不触发审批、放大才触发）」⇒ `agent-guild` Cap72「deny-only 继承 / 收窄免费且可逆、放大不可逆」已落同一判据，重叠 >60%。⇒ 只落"撤回不可机检声明"这一条，不为配套点重复占版本位。
- 提升层：可复用 Skill / 校验纪律。触发词：不可机检的安全声明、security-manifest-schema-unavailable、unrecognized security manifest、撤回声明、假安心、无从判定不等于通过、advisory-only schema URL、契约缺席。

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

## 故障上下文按来源分两套键命名空间，而非在同一记录体加区分字段：执行期 `execution.id/url/error.message/stack/lastNodeExecuted/mode` 与触发期 `trigger.error.context/name/cause` 并存（来源：docs.n8n.io `build/flow-logic/handle-errors-gracefully.md`，2026-10-07 独立 curl 实拉；与 av「跨审计方对账主键是内容哈希」互补——那条管对账键，本条管故障账本的键空间设计）
- **判据**：① **同一类实体（一次故障）按"它从哪来"分两套键空间**，比"在同一记录体里加 nullable 字段区分"更干净——执行链故障与触发器自身故障的字段集不同，混在一个 schema 里会逼出大量 optional 字段、读时还要先判来源。② **审计/排障账本要按来源命名空间隔离**：拉故障日志时先按 execution/trigger 两个命名空间分别取，避免把触发器错误误归因到执行链。③ `execution.retryOf` 这类重试链字段已在 r353B 覆盖，本条只取"双键空间"这一增量；判重时对齐作用域。
- 提升层：工作流 / 工具。触发词：故障上下文按来源分键命名空间、execution.* 与 trigger.error.* 双键、审计账本命名空间隔离、retryOf 已覆盖只取增量。

## 验真走两条路线且结论不可互相替代：目录树 detached 签名（严格模式=签名后新增未签名文件验证必失败，豁免须显式开 `--ignore-unsigned-files`）vs 服务端 verify envelope（sha 产物指纹 + 扫描裁决，无客户端可验签）；评审判据 = 「签名不证明安全，只证明发布物=被审物」，消费侧五条安装前清单含**本地任何修改后重跑验证**（来源：docs.nvidia.com/skills/signing-agent-skills.md 3,753B，2026-10-07 独立 curl 实拉逐串命中 `Detached`/`directory tree`/`ignore-unsigned-files`/`nv-agent-root-cert`/`does not prove`；与 sa「验签宽松开关是带文档化义务的例外」互补——那条在 sa 管"宽松开关结论两域"，本条在 av 管"两种验真路线对照 + 消费侧重验"）
- **判据**：① **两条路线代表两种信任锚模型**：OMS detached 目录树签名让客户端可独立验（签后加未签文件严格模式必失败）；ClawHub 服务端 envelope 把裁决放在服务器（无客户端密码学签可验）。② **签名只证明"发布物未被改动"，不证明"内容安全"**——扫描是签名前独立环节，把"签名有效"当"可信"等于跳过扫描。③ **消费侧安装前清单含"本地任何修改后重跑验证"**：下载后若本地改过文件，必须重验，否则签名结论失效。④ 与 sa 的 `--ignore-unsigned-files` 两域结论同源：凡可收窄验证范围的参数，结论必带作用域。
- 提升层：工具 / 供应链准入。触发词：目录树签名 vs 服务端 envelope、严格模式签后加文件必失败、签名不证明安全、消费侧本地修改重验、两种信任锚模型。

## 恶意有两档：第二档「零恶意件组合」没有攻击者意图可寻，只能靠组合级行为回归发现（来源：arxiv.org/html/2610.05943v1 210,175B，2026-10-07 独立 curl 实拉逐串命中 `evaluates skills in isolation` / `composition-induced risks underexplored` / `individually benign`；与 §恶意意图分散在多技能（SkillCascade）互补——那条靠关系图找"意图躲在哪件里"，本条处理"每件都干净"的组合涌现）
- **判据**：① 原文：`Existing security vetting, however, largely evaluates skills in isolation, leaving composition-induced risks underexplored. Such risks arise because composing benign skills expands the agent's capability space, enabling behaviors unavailable to any skill alone.` ⇒ **单件扫描全部通过 ≠ 组合后安全**。② 因此除单件静态扫描外必须再有一档**组合级行为回归**：枚举"这个技能与已装技能集合合起来能构成什么能力"，而不是只问"这一件自己做了什么"。③ 两档用例集不同：关系图档的前提是存在恶意意图（分布在多件），本档的前提是**每件都通过审查、恶意由组合涌现**，所以本档不能用"找意图"的判据去扫，只能靠能力空间的行为枚举。
- 提升层：工具 / 工作流。触发词：组合级涌现恶意、individually benign、composition-induced risk、单件通过不等于组合安全、组合行为回归。

## 便宜的静态扫描不能代理 LLM 评审器（Spearman ρ = 0.14），且"平均增益"必须附正例占比与 CI 才能支撑"技能有效"（来源：arxiv.org/html/2608.20614v1 420,604B，2026-10-07 独立 curl 取 HTML 全文逐串命中 `structural versus LLM-judge Spearman ρ = 0.14` / `mean composite Skill Lift is 0.2134` / `95% paired-case CI [0.1967, 0.2301]` / `Composite lift is positive in 72.8% of paired cases`；与 §五千好过五万 / §四桶评测集 互补——那两条管评测量怎么选，本条管留出什么报告口径）
- **判据**：① **两套便宜-昂贵信号不同轴**：145 个真实技能上静态闸与 LLM-judge 的 Spearman 只有 0.14 ⇒ 用"扫描分高"替代"评审通过"等于无信息；两者只能并列报，不能互相折算。② **报均值不足以支撑结论**：947 组配对案例 mean composite lift 0.2134（95% CI [0.1967, 0.2301]），但只有 **72.8% 案例为正** ⇒ 均值 + 正例占比 + CI 是三件一起报；只报均值会把"近三成案例变差"藏掉。③ 结果分与过程分不同向，必须分列：outcome-only lift 0.1799 与 composite 0.2134 的差额就是"轨迹质量"这一维度的增量。
- 提升层：工作流（判定与报告口径）。触发词：静态闸不可代理 judge、ρ=0.14、均值须附正例占比、CI 与对照组、outcome-only 与 composite 分列。


## 验收结论必须绑定 harness/工具链标识：同一技能集跨 harness 增益不同（NVIDIA Table 2：All dimensions Claude Code **+34** vs OpenAI Codex **+29**；SkillBench 直接以 24 个 model-harness 组合为评测单位）（来源：developer.nvidia.com/blog/evaluating-ai-agent-skill-performance-with-nvidia-skillevaluator/ 257,328B + skillsbench.ai 441,319B，2026-10-08 独立 curl 实拉逐串命中 `<td>All dimensions</td><td>+34</td><td>+29</td>` / `87 tasks across 8 domains and 24 model-harness configurations`；与 §均值须配 CI 与正例占比 互补——那条管一个增益数字要带不确定性，本条管这个数字必须带运行环境标识）
- **判据**：脱离 harness 报「技能提升 X 分」不可复现；结论行必须写成「模型×harness×技能集」三元组，跨 harness 结论并列报而不取均值。（细则见 references/knowledge-base.md §r437C-1）

## 场景级完成度（SGC）要与任务级成功率并列报：防止「单步都成功但整条场景目标未达成」被 SR 掩盖（来源：arxiv.org/html/2602.12430v4，2026-10-08 实拉逐串命中 `Scenario Goal Completion—an 8.9% absolute improvement over baseline GRPO without skill libraries—while requiring 26% fewer interaction steps`；全库 grep `SGC` 0 命中。与 §技能级 eval 五类 case family 互补——那条管用例覆盖面，本条管整条场景链目标是否达成）
- **判据**：任务级 SR 与场景级 SGC 是两个不可互相折算的口径，报告须并列给出。（细则见 references/knowledge-base.md §r437C-2）

## 审计台账要有一条「刻意不记什么」的负向清单：只留 provenance 与 result codes，明确排除 prompts / messages / tool arguments / tool results / raw errors（来源：docs.openclaw.ai/concepts/agent-loop 299,791B，2026-10-08 独立 curl 实拉逐串命中 `projects lifecycle and tool start/terminal events into the bounded, metadata-only audit ledger` / `records provenance and result codes without copying prompts, messages, tool arguments, tool results, or raw errors`；与 §主张级可审计四维 互补——那条管证据要充分，本条管留存要最小化）
- **判据**：只写「记什么」的台账会因默认全记而失控；须显式列出排除项并可机检。（细则见 references/knowledge-base.md §r437C-3）
- 提升层：工具（指标口径）/ 可复用 Skill（可观测性）。触发词：结论绑定 harness、+34 vs +29、24 model-harness、SGC 场景级完成度、审计台账负向清单、metadata-only ledger。

## 外部声明值必须「先对硬限额核对、再据此分配或放行」：把声明当不可信输入，核对通过才允许消费（来源：api.github.com/repos/langgenius/dify/issues/42021 一手 5,739B JSON，2026-10-08 r438C 独立 curl 实拉逐串命中 `pre-allocates a bytearray of the plugin-declared total_length` / `before validating it against max_file_size` / `the 30MB PLUGIN_MAX_FILE_SIZE limit is never consulted first` / `MemoryError`/`OverflowError` instead of the documented ValueError`；与 av §未声明就是未声明 互补——那条管"没声明"不能当默认，本条管"声明了"也不能当可信）
- **判据**：凡「声明一个数量 → 据此分配资源 / 放行」的代码路径，核对必须在分配之前：声明值由外部可控 ⇒ 据未核对声明分配＝资源型 DoS（原文声明 `2**62` 直接 MemoryError），据未核对声明放行＝审计缺口（本该报超限 ValueError 却被绕过）。自检问一句：**这条路径是先信后查，还是先查后信？**
- 提升层：可复用 Skill（输入校验序）/ 工具（资源分配）。触发词：声明大小、declared total_length、先分配后校验、PLUGIN_MAX_FILE_SIZE、MemoryError 而非 ValueError、声明值不可信

## 治理闭环的第一环是「连接存在性枚举面」：没有枚举就没有后续权限与审计——自助接入会形成不可见的影子集成层（来源：mcpmanager.ai/blog/mcp-statistics/ 一手 188,382B，2026-10-08 r438C 独立 curl 实拉逐串命中 `This creates a shadow AI and shadow MCP scenario` / `When you fail to provide a clear, safe path, workers will create an unmonitored one` / `83%` / `26% Have Comprehensive AI Security Governance` / `Under 1%`；全库 grep「影子集成 / 连接存在性 / 枚举面」0 命中，既有「影子副本」指产物副本属另一轴）
- **判据**：审查接入治理时先看有没有「当前已连客户端 / 来源清单 + 上限展示 + 一键吊销」这一层枚举面；**没有枚举面，后面所有权限、留痕、审计条款都无从落地**——不是做得不够严，是根本不知道要管谁。原文因果也给出治理方向：没有安全的正路，就一定长出不受监控的野路。
- 提升层：工作流（接入治理）/ 可复用 Skill（可观测面）。触发词：影子 MCP、shadow AI、连接存在性、枚举面、一键吊销、未登记接入、83% 24%、26% 治理政策


## 技能审计要从「逐个看 SKILL.md」升级为「依赖图指标」：单包审查看不到的风险多数在传递依赖里（来源：arxiv.org/html/2607.01136v1 209,169B，语料 1,434,046 条，2026-10-08 一手实拉）
- **实证**：① **依赖放大系数 = 传递依赖数 / 直接依赖数**，实测 p99 = **130.5×**（npm/PyPI 侧最大 1,754×）；② 集中度 normalized Gini：skills **0.925**、packages **0.944**；③ **「只能经传递才到达」的危险面占比** 98.01%（axios）、含漏洞 MCP 服务 93.10%；④ name 冲突率 **58.73%**、front-matter 存在率 **99.55%**（⇒ 元数据齐 ≠ 可治理）；⑤ 解析管线五步：front-matter/正文分离 → 证据置信打分（滤模板噪声）→ 类型化通道分类 → 递归 registry 解析 → canonicalize + schema 校验成 **SkillBOM**。
- **判据**：① 审计报告**必须给出「放大系数」与「传递到达率」这两个数**——只报「扫了 N 个技能、发现 M 个问题」会把 130× 的传递面完全漏掉；② **元数据齐备率不能当治理完成度**（99.55% 与 58.73% 冲突率并存），须把「有 front-matter」与「可比对、可溯源」分开计；③ 冲突率 ≥ 半数意味着**按 name 做主键的对账会静默错配**，主键须换内容哈希或 (source, name, revision) 复合键。
- **与既有能力分工**：r438C「治理第一环是连接存在性枚举面」管**有没有清单**；本条管**清单建好之后按什么指标看出来风险**——枚举是输入，图指标是判据。
- 提升层：工作流（审计度量）/ 工具（SBOM 化）。触发词：依赖放大系数、130.5x、Gini 0.925、传递到达率 98.01、name 冲突率 58.73、SkillBOM、元数据齐不等于可治理。


## 引用外部风险条目时「编号」与「当页定义」必须双写：同一编号在不同文档里指的不是同一件事（来源：owasp.github.io/www-project-agentic-skills-top-10/risk-assessment.html 100,225B 对照主页，2026-10-08 一手实拉）
- **实证**：同一 OWASP 项目内，`risk-assessment.html` 把 AST05 定为 **Insufficient Input Validation**、AST06 **Improper Error Handling**、AST07 **Insecure Storage**、AST09 **Lack of Monitoring**，而项目主页的 Top10 把同编号写成 Untrusted External Instructions / Weak Isolation / Update Drift / No Governance。
- **判据**：① **编号不是稳定主键**：跨文档合并时只写编号会静默错配，引用格式必须是「编号 + 该文档当页的定义原文」；② 审计台账里出现编号时，要能指出**它出自哪一份文档的哪一版**——否则两个来源的 AST05 会被当成同一条而合并计分。
- 提升层：工作流（引用规约）。触发词：编号与定义双写、AST05 不同定义、跨文档静默错配、引用要带出处版本。

## 采信任何评测/扫描结论前先做「三查」：判定口径、横向排名可用性、口径切换敏感度（来源：oasb.ai/benchmark 60,443B，2026-10-08 一手实拉；解除 r438A 搁置）
- **实证**：① 判定口径原文「A sample is **flagged malicious on a high/critical attack finding**」——权限类、治理类提示与边缘案例不计入；② 横向排名原文「The comparative accuracy figures on this page **have been withdrawn**」，第三方拦截区间 **3.8%–41.9%** 且**无精确度验证**；③ 同一基准下「计入自标记」与「剔除」两口径的召回率可达 **82.6% vs 47.3%**。
- **判据**：① **先看它把什么算作「命中」**：只计攻击类高/严重告警的恶意判定，与「含风险提示就算」不是同一个量；引用前必须确认分母；② **被作者撤回的横向分禁止用于选型**——撤回声明本身就是不可用证据，拿它做排名等于引用一个已作废的数字；③ **任何召回率/检出率必须绑定口径**：82.6% 与 47.3% 差 35 个点，不写口径的数字无法跨报告比较。
- **与既有能力分工**：r436C「静态闸不可代理 judge（ρ=0.14）+ 均值须配 CI」管**自己怎么做评测**；本条管**怎么采信别人的评测**——一内一外。
- 提升层：可复用 Skill（证据采信）/ 工具（基准报告口径）。触发词：三查口径、flagged malicious、withdrawn 横向分、82.6 vs 47.3、口径切换敏感度、3.8%–41.9%。

## 记分表里「没测到」必须记 N/A 不能记 FAIL：跨不同覆盖面比较 pass 数是错误选型依据（来源：oasb.ai/docs 29,646B + /controls 76,804B + /eval 37,230B，2026-10-08 一手实拉逐串命中 `reported N/A, not FAIL, so scorecards stay comparable across tools with different surfaces` / `comparing pass counts across different capability sets`；与 §采信评测前三查 互补——那条管怎么读别人的结论，本条管自己这张记分表怎么打分）
- **实证**：官方原文「Undeclared capability is **reported N/A, not FAIL**, so scorecards stay comparable across tools with different surfaces」；「use the verdict-based corpus benchmark rather than **comparing pass counts** across different capability sets」；控制项分三层 **L1 Essential（baseline security for development and prototypes）/ L2 Standard / L3 Hardened**，逐项带 rationale + audit procedures + remediation。
- **判据**：① **覆盖缺口与不合格是两栏，禁止合并**：「没测到」记 N/A 而不是 FAIL，否则覆盖面小的工具被系统性压低、覆盖面大的工具靠多测的项刷高；反过来说，把 N/A 当通过也是同样的错——它是一栏独立的"未覆盖"，既不是通过也不是失败。② **横向选型禁止直接比 pass 数**：两套能力集不同时，pass 数多只说明声明得多；可比的只有同一覆盖面下的 verdict 判定，跨集比较必须换成"同一控制项上的通过率"。③ **控制项必须分层且每项自带三件套**（理由/审计步骤/修复动作）：只有名字没有 rationale+audit+remediation 的控制项，评审者无法复现判定，只能凭感觉打勾。④ **分层要写明每层的适用场景**（L1 是开发与原型的基线，不是生产基线）⇒ 报"过了 L1"时不写层号等于把最低档说成合格。
- **与既有能力分工**：r439C「三查」管**采信外部基准**（口径/撤回/敏感度）；本条管**内部记分表的取值与横向可比性**（N/A 语义、禁跨集比 pass、分层三件套）——一外一内。
- 提升层：可复用 Skill（记分规约）/ 工具（评审表设计）。触发词：N/A 不是 FAIL、覆盖缺口单独成栏、禁止跨能力集比 pass 数、verdict-based benchmark、L1/L2/L3 控制分层、rationale+audit+remediation。

## 门禁退出码是稳定契约，且「覆盖缺口」必须并入阻断态；基线抑制只改风险分的口径、不改风险本身（来源：api.github.com/repos/NVIDIA/SkillSpector/readme 74,672B → base64 解码 53,566B 全文，2026-10-08 一手实拉逐串命中 `its exit code and JSON output are a stable contract` / `--fail-on-incomplete` found partial/incomplete analysis / `re-scans surface only *new* findings` / `It never executes the scanned skill`；与 §记分表 N/A 语义 互补——那条管表里怎么记，本条管门禁怎么判与怎么不误放行）
- **实证**：官方原文「Its **exit code and JSON output are a stable contract**」；`0` = 扫完且 `risk_score ≤ 50`（SAFE/CAUTION）且无 strict gate 触发；`1` = 扫完且「`risk_score > 50`、**`--fail-on-findings` 命中 active finding**、**`--fail-on-incomplete` 发现 partial/incomplete analysis**、或 **`--min-coverage` 覆盖低于阈值」四者之一；`2` = 错误。「默认退出码把 SAFE 与 CAUTION 折叠进 `0`」，要区分须显式开关。基线「Suppress known/accepted findings so the **risk score reflects only un-triaged issues** and re-scans surface only *new* findings」。信任模型原文「SkillSpector is **defense-in-depth, not a sandbox** … **It never executes the scanned skill.**」
- **判据**：① **「没扫全」必须算阻断，不能算通过**：`1` 同时覆盖"发现高风险"与"分析不完整/覆盖不足" ⇒ 门禁脚本若只看"有没有 finding"，覆盖缺口会静默通过；把覆盖缺口并入阻断态，才不会出现"扫了 30% 报绿灯"。② **默认档位要显式声明它折叠了什么**：默认把 SAFE 与 CAUTION 都折叠成 `0` ⇒ 说"退出码 0"时必须同时说"这一档把 CAUTION 也算通过"，否则使用者会把"有提示但没阻断"读成"没问题"。③ **基线抑制改的是口径不是风险**：基线让风险分只反映未分诊项、重扫只报新增 ⇒ 换基线等于换量纲；把基线当"把误报删掉了"会低估存量风险。④ **静态扫描器的边界必须写进文档**：从不执行被扫对象，且明说"是纵深防御不是沙箱" ⇒ 拿静态扫描结果当"这个技能跑起来安全"的证据是范畴错误。⑤ **不同开关是不同语义的准入面**：`--fail-on-findings` / `--fail-on-incomplete` / `--min-coverage` 分别对应三条独立的准入线，只开一条就说"有门禁"等于只堵了一个口。
- **与既有能力分工**：r439B「复审记分对象是新增 + llm-unconfirmed」管**跨轮怎么记分**；本条管**单次门禁怎么退出、覆盖缺口算不算过、基线会不会让风险假降**。
- 提升层：工具（门禁契约）/ 工作流（准入线）。触发词：exit code stable contract、--fail-on-incomplete、--min-coverage、覆盖缺口并入阻断、CAUTION 折叠进 0、基线只改口径、defense-in-depth not a sandbox、never executes the scanned skill。

## 扫描「标记率」不等于风险规模：报告必须固定为「标记数 / 带上下文复核后可疑数」双列，一手漏斗在 238,180 个技能上是 46.8% → 0.52%（来源：arxiv.org/abs/2603.16572 42,685B，2026-10-08 一手 curl 逐串命中 `classify up to 46.8% of skills as malicious` / `only 0.52% remain suspicious after repository-aware analysis` / `238,180 unique skills`；与 §采信评测前三查 互补——那条管别人的结论能不能用，本条管自己这份扫描产出怎么报）
- **实证**：官方摘要原文「scanner reports from individual marketplaces **classify up to 46.8% of skills as malicious**, raising concerns about false positives」；「we collect **238,180 unique skills** from three major distribution platforms and GitHub」；「Unlike existing scanner-based assessments, which evaluate skills largely in isolation, our **repository-aware** analysis checks whether a flagged skill is consistent with its surrounding GitHub project. This context substantially reduces the number of suspicious skills: **only 0.52% remain suspicious after repository-aware analysis**. Our results show that existing scanners can **substantially overestimate maliciousness when repository context is ignored**.」
- **判据**：① **原始标记率禁止当风险规模上报**：46.8% 与 0.52% 相差约 90 倍——前者是"扫描器打了标"，后者才是"结合仓库上下文后仍可疑"；报前者等于把九成以上的噪声当成风险清单交出去。② **复核必须带上下文，且上下文是仓库级/依赖级的**：单文件静态判恶意在大规模语料下几乎不可用，判据是"该文件在所属仓库里扮演什么角色、与依赖是否自洽"；脱离仓库上下文的扫描结论只能当线索，不能当裁决。③ **报告格式固定为双列**（标记数 / 复核后可疑数）：单列数字无法区分"扫出来的"与"审过的"，双列才能让读者判断还有多少待复核。④ **与既有条目串成完整链**：完整性（哈希/签名）→ 扫描（已知噪声率）→ 上下文复核（裁决）——任何一环单独拿出来的结论都不可作放行证据；本条补的是最后一环的量级校准。
- **与既有能力分工**：r440A「记分表 N/A 不是 FAIL」管**表里怎么记**；r439C「三查」管**外部基准怎么采信**；本条管**自己这份扫描产出怎么报规模、以及为什么不能只报标记率**。
- 提升层：工作流（扫描报告口径）/ 工具（上下文复核）。触发词：46.8% 到 0.52%、标记率不是风险率、repository-aware、238,180、双列报告、上下文复核、扫描噪声九成。


## 依赖图审计只看「集中度和冲突率」不够：含环率、隐形继承率、放大倍数是三个独立的图结构风险轴（来源：arxiv.org/html/2607.01136v1 209,169B，2026-10-08 一手 curl 逐串命中 `SDA achieves an overall F1 score of 0.95` / `30.41% of root skills with dependencies contain at least one skill in a cycle` / `22.42% gain packages only through reused skills` / `maxima of 347× for skills, 1,754× for packages` / `71.87% and 73.33% of packages, respectively, are inherited through skill reuse`；与 §r439A 依赖图指标（名称冲突率 58.73% / Gini 0.925-0.944 / 传递到达率 98.01%）互补——那条取集中度与冲突面，本条取图结构三件套）
- **实证**：官方原文「The skill dependency graph is **not a tree**: **30.41%** of root skills with dependencies contain at least one skill in a cycle, and 30.03% have convergent downstream nodes」；「Among dependency-bearing skills, **22.42%** gain packages only through reused skills, making those packages invisible at the root layer」（实例 `npm/rimraf`：1,495 个 root 直接声明，另有 **5,160** 个 root 通过技能复用继承）；放大表 TABLE V：「Total p50 0.5 / p90 23.0 / p99 130.5 / Max 979.0；Package p99 **350×**、Max **1,754×**」，极端例 `windows-95-web-designer` 只声明 3 个技能依赖却拉入 1,754 个包、1,938 个组件（645×）；「Among npm package exposures, **71.87%** are inherited through skill reuse rather than directly declared; for PyPI, the share reaches **73.33%**」；抽取器 SkillDepAnalyzer（SDA）「overall F1 score of **0.95** on the single-layer benchmark … perfect accuracy (1.00) on metadata fields」。
- **判据**：① **「含环」必须单列成轴**——30.41% 的有依赖 root 落在环里，环意味着**不存在拓扑序**：任何"先更新上游再更新下游""按依赖顺序扫描/退役"的单遍算法在环上不成立，必须先做 SCC 坍缩再排程；把依赖图默认当树，是这类审计最常见的隐藏假设。② **「隐形继承」决定声明面审计的上限**：22.42% 的技能只在被复用时才获得包依赖，根层声明里根本看不见 ⇒ 只在根层做依赖清点会系统性漏掉这批；审计对象必须是**递归展开后的闭包**，不是声明集。③ **放大倍数要看尾部分位不看中位数**：放大 p50 只有 0.5，p99 到 130.5（包维度 350×，最大 1,754×）⇒ 用均值/中位数描述依赖规模会得出"依赖很轻"的结论，而真正的风险与成本全部落在长尾；报数必须给 p99/Max。④ **传递依赖占比说明技能库不是孤立的供应链**：npm/PyPI 侧 71.87%/73.33% 的包是经技能复用继承而来 ⇒ 技能层的治理与包层的治理必须打通审计，只扫技能、不扫它带进来的包，等于只审了入口。⑤ **抽取器自身先要过基准再采信它的统计**：SDA 的 F1=0.95、元数据 1.00 是数字可采信的前提 ⇒ 凡用工具产出的供应链度量，先问该工具在标注集上的分数，否则整套治理结论建立在未校准的抽取上。
- **与既有能力分工**：r439A「依赖图指标（冲突率/Gini/到达率）+ SkillBOM 五步」管**这条链有多集中、名字撞得多严重**；本条管**图长什么样、声明看不看得全、代价落在哪一端**。
- 提升层：可复用 Skill（供应链审计指标集）/ 工具（依赖图分析）。触发词：依赖图不是树、含环率 30.41%、SCC 坍缩、隐形继承 22.42%、递归展开闭包、放大倍数 p99、1,754×、传递依赖占比 71.87% 73.33%、声明面审计上限、抽取器 F1 校准。

## 「规则库有多大」必须到代码里数：README / docs / 源码三处口径不一致是常态，且第三方转述的缺项结论也可能是错的（来源：api.github.com/repos/NVIDIA/SkillSpector/contents/README.md 53,632B 逐串命中 `71 vulnerability patterns` across 17 categories（同串在 27/488 行各出现一次）；同仓 `src/skillspector/nodes/analyzers/pattern_defaults.py` 44,213B 代码级实测唯一规则 ID = **39**（SC1–SC10、PE1–3、TR1–3、AR1–3、AS1–3、EA1–5、LP1–4、MP1–3、OH1–3、RA1–2）、`PatternCategory` 枚举 = **18** 类、且 **SC7 在代码中存在**（`Code pulls a container image with signature or registry verification disabled`）；与 §门禁退出码是稳定契约 互补——那条管门禁行为，本条管「声称的规则覆盖」本身怎么核）
- **实证（三方口径并列）**：① README 自述「**71 vulnerability patterns** across **17 categories**」（同一句在 README 第 27 行与第 488 行各出现一次）；② 代码侧枚举 `PatternCategory` 实测 **18** 个成员（AGENT_SNOOPING / ANTI_REFUSAL / DATA_EXFILTRATION / DESERIALIZATION / EXCESSIVE_AGENCY / MCP_LEAST_PRIVILEGE / MCP_TOOL_POISONING / MEMORY_POISONING / OUTPUT_HANDLING / PRIVILEGE_ESCALATION / PROMPT_INJECTION / ROGUE_AGENT / SERVER_SIDE_REQUEST_FORGERY / SUPPLY_CHAIN / SYSTEM_PROMPT_LEAKAGE / TOOL_MISUSE / TRIGGER_ABUSE / YARA_MATCH）；③ 代码侧 `pattern_defaults.py` 内唯一规则 ID 实测 **39** 个，与 README 的 71 相差近一倍；④ **一手纠错**：Qoder r453-Q-C 转述「README 里 SC7 缺项」，实测 SC7 在 `pattern_defaults.py` 中**完整存在**（第 100 行语义描述、第 202 行类别映射、第 303 行标题「Untrusted Container Image」、第 413 行修复建议），该缺项结论**不成立，不予采纳**。
- **判据**：① **「有多少条规则」是安全声明，不能引 README**：README 71 / 代码 39 是两个不同口径（可能一个是规则条目数、一个是含变体的检测点数），但**使用者无法从 README 分辨** ⇒ 凡把规则库规模写进能力声明的，必须标明"数的是 ID 数还是检测点数、取自哪个文件哪一行、在什么提交上"。② **类别数必须到枚举里数**：18 vs 17 的差 1 不是笔误而是**两个不同的分类维度**（README 的 17 类把 YARA / AST / taint 与语义类并列，代码枚举则按语义域划分）⇒ 类别数不能直接拿来做覆盖率分母，先确认两边是不是同一套分类。③ **转述型缺项结论必须回到源码复核**："README 缺 SC7"这类断言的价值全在"缺"字上，一旦反证存在，整条"覆盖有洞"的推论作废 ⇒ 收到他人判重/判缺结论时，凡涉及"某条规则在不在"，一律回源码 grep 规则 ID，不接受文档面转述。④ **同一句声明在文档里重复出现不等于被多处验证**：README 里 "71 patterns across 17 categories" 出现两次，但两句同源 ⇒ 计数重复出现次数不能当交叉验证，交叉验证必须是**不同文件/不同层（文档 vs 代码）**之间的比对。⑤ **覆盖口径不一致时的落点**：报告里写"覆盖 N 条规则"时必须附三元组（声明值 / 代码实测值 / 差异说明），只写一个数字会把口径差隐藏成确定性。
- **与既有能力分工**：r442A「情报源须带 offline fallback + 71 patterns×17 categories 作覆盖度分母」管**情报源与分母的可用性**；本条管**这个分母本身到代码层实测后与声明不一致时该怎么报**，以及**转述缺项结论的复核义务**。
- 提升层：工具（扫描器覆盖声明）/ 工作流（审计取证口径）。触发词：71 patterns、代码实测 39、17 vs 18 类别、README 与代码口径不一致、SC7 存在、转述缺项须回源码复核、覆盖分母须附三元组、同源重复出现不算交叉验证。

## 数值断言必须「回原文核语义」而非「只核字符串是否存在」：同一事实两处口径不同（OWASP AST01「100% 恶意同时用两向量」vs Snyk「91%」），且 1,467 是「≥1 缺陷」非「恶意载荷数」（来源：owasp.github.io AST01 + snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/，2026-10-08 一手 curl 逐串命中 `100% of malicious`/`both attack vectors`/`did:web`；r445C 落地）
- **实证**：① OWASP AST01：「Hash-pin installed skills… **100% of malicious skills combined both attack vectors**」；② Snyk ToxicSkills 原文：「100% 已确认恶意技能含恶意代码模式，而 **91%** 同时使用提示注入」；ClawHub 全库提示注入政策率仅 **2.6%**；③ Snyk 1,467 = 「至少 1 个任意严重度缺陷」= 36.82%，**不是**恶意载荷数；人审确认恶意仅 **76**（8 个仍在 clawhub.ai）；与 OWASP 口径分歧在于 OWASP 把 Snyk 的 91% 写成了 100%。
- **判据**：① 引用他人数值时，必须回原文核"这句话在原文里到底什么意思"，不能只 grep 字符串存在就当证据；② 同一数字（100%）在两处语义不同（OWASP 的"两向量都用" vs Snyk 的"91% 用提示注入"），引用时必须指出口径差；③ "缺陷数"与"恶意载荷数"是不同分母，混用会夸大风险；④ 与 r439C「采信评测前三查（口径/横向排名可用性/口径切换敏感度）」互补——那条管外部基准，本条管"引用单点数值时的失真防护"。
- **与既有能力分工**：r439C 管外部基准怎么采信；本条管引用单点数值时的语义复核义务（防止口径错位导致结论失真）。
- 提升层：工作流（引用审计）/ 工具（数值断言核验）。触发词：回原文核语义、100% vs 91%、1,467 是缺陷非恶意、引用失真、口径差、字符串存在≠证据、数值断言防护。

> r443 正文预算管理：以下 6 节原文已零删减下沉本技能 `references/knowledge-base.md`，正文只留指针：失败路径也必须被真的跑过（否则它等于不存在）（原文已下沉 references/；评测要接回优化器才叫闭环：观测 → AI 评测器 → AI 优化器 → 自动验证；提交粒度是可配的，粒度越细回滚能力越弱：早提交换「部分结果不丢」，代价是出错即不；环境变量的可见性有三个独立面：删掉不报错只返 undefined、分享只带引用不；审计可能是惰性生成的（「在库里」≠「已审过」），而扫描器自身的遍历顺序即是静默漏；审核结论按版本独立成态并可滞留未终：同包内 1.0.1–1.0.4 双引擎 `q。

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

## 入口守卫的失败方向必须写明，且「拦下」可以是不留痕的：不匹配回什么码、表达式本身报错时放行还是拦、这次判定留不留痕，三问缺一就查不到自己被拦过（来源：docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook.md 12,270B，2026-10-10 一手 curl 逐串命中 `Requests that don't match receive a 200 response without creating an execution` / `If the expression fails to evaluate, n8n logs a warning and lets the request through rather than blocking it`；r486C 落地）
- **实证**：n8n Webhook 的 `Only Run If` 过滤门原文两条——①「Requests that don't match receive a **200 response without creating an execution**」；②「**If the expression fails to evaluate, n8n logs a warning and lets the request through rather than blocking it**」；且该门位于 IP allowlist 与鉴权**之后**。
- **判据**：① **"不匹配返回什么码"必须显式声明**：本例回 200 且不建执行 ⇒ 调用方看到 200 会认为处理成功，实际什么都没发生；守卫的契约里"不匹配时回什么"比"匹配时做什么"更容易被漏写，而前者才是排障入口。② **守卫自身出错时的默认方向要挑明并挑对**：表达式求值失败时**放行**并只写一条 warning ⇒ 这是"安全侧 vs 可用侧"的显式取舍（fail-open）；挑它必须有理由，且必须留 warning，否则守卫失效与守卫通过不可区分。③ **不留痕的拦截比报错更难查**：不建执行意味着排障时表现为"请求根本没来过" ⇒ 任何"没触发"类问题，排查顺序应是 守卫是否拦下 → 是否到达 → 是否被处理，不能从第三段开始。④ **守卫位置决定它保护什么**：该门在鉴权之后 ⇒ 它不防未授权访问，只做条件分流；把一个后置于鉴权的门当成安全边界写进文档，等于声明了一个不存在的防线。⑤ **"只写 warning"要能被检索到**：fail-open 的可观测性全靠那一条日志 ⇒ 启用 fail-open 守卫时必须同时确认日志会被采集，否则失败模式是"既不拦也不记"。
- **与既有能力分工**：r485C「装错目录静默失效」管**产物落错位置被无视**；本条管**请求在入口被静默丢弃**——一个是出口面，一个是入口面。
- 提升层：工具（入口守卫契约）/ 工作流（可观测性）。触发词：200 response without creating an execution、lets the request through rather than blocking it、守卫失败方向、fail-open 守卫、只写 warning、不留痕拦截、守卫在鉴权之后、不匹配回什么码。

## 「阳性率最高」的扫描器在「确证恶意」上可能最低：覆盖率/准确率必须带分母口径，且 advisory-only 的信号不能反过来当准入证据（来源：openclaw.ai/blog/openclaw-nvidia-skill-security 45,746B，2026-10-10 一手 curl 逐串命中 `48.71` / `72.8` / `6.8` / `advis`；r486C 落地）
- **实证**：67,453 个最新公开技能版本上——SkillSpector 阳性 **48.71%**（32,856）、VirusTotal **7.75%**（5,225）、静态 **6.57%**（4,434）；三家两两 Jaccard 仅 0.065–0.104，三家全中只有 468 条（0.69%），**81.9% 的阳性只来自单一扫描器**；关键反转出现在 **206 条真恶意**子集里：VirusTotal 命中 150（**72.8%**）而 SkillSpector 只命中 14（**6.8%**）；治理口径原句「SkillSpector findings are shown as **advisories; they do not automatically block a skill**」。
- **判据**：① **同一个"准确率"在不同分母下结论完全相反**：48.71% 是全量 67,453 上的阳性率，6.8% 是真恶意 206 上的命中率——**高阳性率的通用扫描器在确证恶意上反而最低** ⇒ 任何扫描器评估必须同时给"在谁上面"的三档分母（全量 / 可疑子集 / 确证恶意），只给一个数等于选了一个立场。② **多扫描器结论不一致时默认升人工审，不投票**：81.9% 的阳性只来自单一扫描器、两两 Jaccard 不足 0.11 ⇒ 三家几乎不看同一批东西，多数表决会把"只有一家看到"的真信号投掉；不一致本身就是最强的升级信号。③ **"不阻断只建议"的扫描器不能反过来当准入证据**：advisory 定位意味着它追求召回而非精确 ⇒ 用它做硬阻断会拦掉近一半技能（48.71%）；反过来说，它给出"未报"也不能当作"已通过安全审查"。④ **报告要并列"宽松信号的量"与"严格信号的量"**：把 32,856 与 206 并排写，读者才会问"二者什么关系" ⇒ 只报阳性数会让人误以为风险规模就是这个数。⑤ **跨扫描器引用结论须重新对齐口径**：不同厂商的"阳性"定义不同 ⇒ 引用第二家数字时不能沿用第一家的解释句。
- **与既有能力分工**：r441A「标记率 ≠ 风险规模、报告固定双列（标记数/复核后可疑数）」管**同一扫描器内的两级口径**；r443C「采信评测前三查（判定口径/排名可用性/口径切换敏感度）」管**采信流程**；本条管**多扫描器并列时的分母反转与 advisory 信号的证据等级**。
- 提升层：工具（扫描评估口径）/ 可复用 Skill（证据分级）。触发词：48.71% 阳性、206 条真恶意、72.8% vs 6.8%、Jaccard 0.065、81.9% 单一扫描器、advisories do not automatically block、分母口径反转、advisory-only 不作准入证据。

> 正文预算管理：「流行度与展示序都不是质量/留存的判据：简单特征（体积、下载量）对「是否持续在架」无稳定预测力，注意力高度集中且权限声明普」、「扫描预算耗尽只允许「降档验证」，不允许判为通过；应用层不隔离要作正面申报，不能让集成方靠缺位反证推断（来源：docs.o」、「存在「权限无关的永不可见类」；特权查看须一次性按单次记录，且被拒尝试同留痕（来源：docs.n8n.io/.../red」、「「能自动仲裁」被当成「没有冲突」：冲突检测器的能力边界必须逐类声明，未覆盖的那类会被静默覆盖（来源：docs.n8n.i」、「资格判定三态（全文见 references/knowledge-base.md §下沉·wb-artifact-veri」、「降档/资格判定按成因分档，且只有一类会告警：配置意图 / 角色封顶 / 后端能力矩阵缺项（全文见 references/」、「投递验收必须双字段分列，且二者可同时矛盾：外发成功 ≠ 回合完成，超时=Unknown 且不重试（全文见 referen」 等 7 节原文已零删减下沉本技能 `references/knowledge-base.md`，正文只留指针。
