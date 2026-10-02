---
name: wb-artifact-verification
description: >-
  对"生成出来的东西"做独立验证并给出明确的成功/失败判定。当用户要求"验证生成结果""验证这个脚本/代码能不能跑""验证是否成功""帮我确认结果对不对""check 一下生成物""验证执行结果"，或给出"先生成再验证再反馈"这类任务时使用。核心是三条互相独立的证据源（独立算法 oracle / 外部已知常数 / 随机差分模糊测试）+ 故障注入（变异测试）证明验证器本身有检出能力，禁止只跑一次"看起来没问题"就宣布成功。另含"证明检查真的跑到了"：非零退出不等于检出（import 报错/构建失败也非零），须打到达标记；被测方须侧盲；判不出结果时"不确定"是一等判定，不得默认通过、不得伪造因果。另含"验证通道禁止副作用"：验证命令不得借检查之名做发布/部署/推送/外发。触发词：验证、验证结果、验证一下、能不能跑、跑通了吗、对不对、check 一下、测一下、自检、回归、真的修好了吗、看起来没问题、绿灯、都过了、测试全绿、失败注入、变异测试、假阳性、伪成功、静默测错、不确定、证不出来、证据不足、评分器、评测、基准、对照实验、抽样、覆盖率、未测、跳过、flaky、可复现、脚本化验证、退出码、超时、只读验证、别在验证里发布。、失败分类法、置信度阈值过滤误报、批量失败、单条失败、占位保配对、条数对齐、失败归属到条、来源自证端点、代理后静默失效、我看你是谁、限流失效、真实来源核验、评测续跑、只重放未完成、改了实现要全量重跑、续跑可比性、自描述元数据、写入方版本、序列化器不可用、解码失败不等于值错、绕过读取通道、过期检查在读取路径、合法 JSON 不等于合规、结构检查三态、解析失败vs字段不合规、轨迹同构三元组、完成度不能从最终答复推断、逐子任务报告、工具三判、误读返回值、恰好一次、exactly once、副作用重复、审计重复、重放重复、结算标记、合并前钩子、占用分解、扫描根、观测面盲区、分解为空、不是我的证据、盘满但分解小、换证据源、告警缺席、钩子被吞、缓存命中不触发、钩子计数翻倍、per-attempt钩子、静默失效、告警不算证据、数据飞轮、过闸才上线、来源优先级、合成数据垫底、轨迹优先、分层切分、五千好过五万、反馈版本化、跨家族互评、模式坍缩、四桶评测集、失败重放、回归还是漂移、定期重跑、置信门槛
version: "2.118.0"
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
## 失败路径也必须被真的跑过（否则它等于不存在）
来源：n8n Docs《Handle errors gracefully》"Stop and Error 节点"（2026-09-14 实访 Markdown 原文）。

**错误处理代码最常见的状态是"写完就再也没执行过"。** 它只在出事时才跑，而出事时你最没空怀疑它有问题——于是最常见的结果是：错误发生了，错误处理自己也崩了。

- **用受控失败去验证失败路径**：主动制造一次失败（专用节点 / 断言 / 断网 / 坏输入），确认错误通道真的被触发、负载字段真的齐全、下游真的收到。
- **判据：这条失败处理上一次被实际执行是什么时候？** 答不上来 = 未验证。
- 与 §C「变异测试」分工：变异测试证明**检查器能抓到问题**，本条证明**出问题后的处置链路能跑通**——前者管检出，后者管兜底，两条都不跑就都不成立。
- 与「不确定（INCONCLUSIVE）是一等判定」联动：**失败路径没跑通过 → 整体判"不确定"**，不能因为它"看起来写对了"就算通过。

验证要能脚本化跑，不能只在界面里点
来源：MCP 官方《MCP Inspector》（2026-09-14 实访）：同一个调试内核提供三种界面——**Web（图形，最丰富）/ CLI（可脚本、机器可读，给 CI、管道和编码 agent）/ TUI（无浏览器时的终端界面）**。

- **关键不是有三种界面，是三种共享同一内核**：同样的传输、同样的配置、同样的认证状态、同样的协议协商。**因此在一处得出的结论在另一处同样成立**——如果每个界面各实现一套，调试结果就无法迁移，还会出现"在 GUI 里是好的、在 CI 里挂了"。
- **必须有一档可脚本化**：验证只有在能被 CI / 管道 / 另一个 agent 调用时，才成为"持续生效的检查"；只能在界面里点的验证，等于只在有人想起来时才存在。
- **机器可读优先**：脚本化形态输出结构化结果（JSON / 一行一项），便于比对与归档；人读的报告由它生成，而不是反过来。
- 与「到达标记落 stdout 单独一行」配套：那是为了证明检查真的跑了，本条是为了让检查能被反复跑。

便利入口会静默改数据：保真走原样通道（来源 MCP Inspector CLI 2026-09-15 实访）
- Inspector 的 `--tool-arg key=value` 会对值做 **JSON 解析强制转换**：`count=1` 变数字、**`"012"` 静默变成 `12`**（前导零丢失、字符串变数值）。要保真必须换 `--tool-args-json`（整体原样传递、零转换）。
- 迁移：任何"方便手写"的参数入口（shell 拼接、CLI 简写、模板变量替换）都可能**静默改值**；验证/复现类调用一律走**显式原样通道**（整份 JSON、文件、stdin），便利入口只留给探索性调用。
- 判据：**这个值错了会不会改变结论？** 会 → 不许走会改值的通道。
- **探针退出码必须区分失败类别**：Inspector 用 0=有 app / 2=无 app / **5=工具名不存在**——"拼错名字"不能被误读成"没有这个东西"，两类失败的处理动作完全不同。验证脚本的退出码同理：`目标不存在` ≠ `目标存在但检查不通过` ≠ `检查器自身故障`，混用一个非零码会让上层做出错误分支。
- **单项失败不杀死整批**：探针单项出错时把错误放进该项的 `resourceError` 字段继续跑其余项，而不是整体中止——批量验证里一个坏样本不应让其余样本的结果全部丢失。

判定口径
```
inconclusive = 对照 harness 失败 / 缺到达标记 / 基线未建立
ok = (无 FAIL) 且 (全部变异体被捕获) 且 (无 inconclusive)
verdict = "SUCCESS" | "FAILURE" | "INCONCLUSIVE"
exit code: SUCCESS=0 / FAILURE=1 / INCONCLUSIVE=2   # 退出码必须与 verdict 一致
```
不确定**单独成一类**，不许并入 SUCCESS（"没验出来"不等于"没问题"），也不许并入 FAILURE（"验不了"不等于"有问题"）。输出三件套：`REPORT.md`（人读，检查表 + 变异表 + 失败项 + 不确定项）+ `verification_report.json`（机读）+ `console.txt`（一行一项摘要）。

结果类别要写明"它不证明什么"（来源：trailofbits/skills·mutation-testing SKILL.md，2026-09-15 实拉）

每一个结果类别都自带一条"它**不**建立的结论"，写判定报告时必须把这条一并呈现：
- **超时（Timeout）= 不确定，不是覆盖证据**——"跑太久没出结果"既不说明测试能查住它，也不说明查不住它
- **跳过（Skipped）= 被遮蔽，不是通过**——同一处更严重的项已被记为未检出，次严重项被系统跳过；不能把 Skipped 计成任何一方
- **信号的严重级 ≠ 后果的严重级**：严重级排的是**信号本身**，不是风险——计费逻辑里低严重级的漏检，比日志行里高严重级的漏检更要紧；**按被改代码的后果加权排序**，别按信号自带的等级直接出优先级
- **同一个"未检出"有两种解释**：测试真有缺口 vs 变异体与原行为语义等价（等价变异）——不区分就归因 = 一半概率在冤枉测试

生成-发布权限分离 + 密封统计门（来源 Qoder r265-C 审计落地，arXiv 2609.30219，2026-09-26 实拉）
- 产出者（模型/子代理）只当候选生成器，发布权归确定性外部门（schema 校验 + 统计上界阈值，如按样本量单侧置信上界对照密封红线）。
- 必须报告分布外漏检实例：基准内零假发布 ≠ 协议无漏，外推失效要被诚实披露。提升层：验证/可复用 Skill。

隐性矛盾交叉证据题（来源 Qoder r265-C 审计落地，arXiv 2609.30055，2026-09-26 实拉）
- 检索/问答类验收不能只考"文档明说了什么"，须含"答案依赖未被任何文档明说、且显式记录相互矛盾"的题式——最强 agent 84 次仅对 1，正说明本栈"交叉核对/独立证据源"步骤必须覆盖矛盾记录场景。提升层：验证。

验证断言要跨平台可移植（来源：william-london/ownframework-loop `keep retry regression portable`，2026-09-15 实拉）

- 断言命令不许赌平台特有 flag：`stat -f` 是 BSD 专有（GNU 是 `stat -c`），一换平台整条回归就假失败
- **用跨平台运行时 API 替代平台 CLI**：取文件权限用 `python os.stat().st_mode & 0o777`，不调 `stat` 的任何方言
- 与「验证要能脚本化跑」互补：那条管"能脱离界面跑"，这条管"换个平台还能跑出同一结论"

本机（Windows）落地坑 —— 都踩过
1. **bash 不可用**：PortableGit shim 缺 `head/dirname/ls`，管道全废 → 改用 PowerShell 或 Read/Write/Glob/Grep 专用工具。
2. **PowerShell 工具不回传 stdout** → 结论必须由脚本自己写 UTF-8 文件，再用 Read 读回。
3. **重定向编码**：PS 5.1 的 `>` / `*>` 产 UTF-16（Read 会判为二进制拍死）。用 `| Set-Content -Encoding UTF8` 或让 Python 自己 `write_text(..., encoding="utf-8")`。redirect 目标目录**必须先存在**，否则整条 PowerShell 语句失败、子进程根本不执行（现象极具误导性：日志没生成、子进程却"好像跑过"）。
4. **按模块名动态导入的检查会误报**：变异体若写成 `mutants/M1-xxx.py`，`import numkit` 会失败 → 把每个变异体放进 `mutants/<name>/numkit.py`，使导入类检查对原件与变异体行为一致。
5. **`python` 可能是 WindowsApps 桩**：固定用 `C:\Users\26719\.workbuddy\binaries\python\versions\3.13.12\python.exe`。
6. 产物落 `D:\腾讯AI\yt\outputs\<日期>_<主题>\`，不落 C 盘、不落会话工作区。

最小骨架
```python
# 1) 独立 oracle（另一种算法，禁止 import 产物里的实现）
# 2) 检查表：rep.add(id, group, desc, ok, detail) 逐项记 PASS/FAIL + 证据详情
# 3) 变异：src.replace(old, new)，old 必须先断言 in src，否则记 applied=False（证伪无效）
# 4) ok = not rep.failed and all(m["caught"] for m in mutants)
```
参考实现：`D:\腾讯AI\yt\outputs\2026-09-13_dp41flash_medium_verify\verify\verify.py`（34 检查 / 5 变异体 / 全绿通过）。

先验证后嵌入 + 位置真源 + 逐项审计

### 未过验证的产物不得并入父文档（来源：SpillwaveSolutions/design-doc-mermaid "resilient workflow"）
图/表格/代码块等子产物**先落盘 → 渲染 → 验证通过**，才允许写进设计文档/交付物——防"坏产物埋进正文"变成静态污染。配套两条：
- **输出格式匹配消费端渲染能力**：GitHub 原生渲染 mermaid；Confluence/Notion/PDF 不保证渲染，必须附 PNG/SVG 图片——"能写"≠"对方能看"，按阅读入口定格式。
- 验证失败的恢复路径要有底：修不了 → 查外部资料 → 换等效形态，不降级成"直接嵌入没验证的东西"。

### 位置信息的唯一真源（来源：warpdotdev/common-skills review-pr）
评审/校对类产物的行内定位**只认标注源**（带 `[OLD:n]/[NEW:n]` 前缀的标注 diff），禁止从行文叙述、渲染视图、文件长度、上下文片段**反推行号**。推不出精确位置的反馈降级到顶层总述，不进行内评论。产出前跑校验器核对每条 path/side/line 与标注源一一对应，**校验不过不上传**。

### 评审前逐项审计，整体通读不算数（同源 review-pr "pre-verdict audit"）
给结论前逐条枚举 diff 新增/修改的**每一条注释与每一个测试**（file:line 列全），逐个对照仓库自身规范判定——"整体看了一遍觉得还行"是不充分的审计方式。规范性违反独立于技术质量：注释写得再好、问题指得再准，违反规范本身仍构成发现项。

### 断言判别力：验证器自己要先被证明能失败（同源 trailofbits #307 / principal-engineer testing-changes）
一条怎么改都能通过的验证证明不了任何东西。判别力检查：把被验证对象破坏一次（改坏关键值/删关键输出），确认验证**真的变红**，再恢复——"从未失败过的验证"与"从未运行过的验证"一样可疑。写死的期望值要独立推导（手算/规范/真实数据），不从生产逻辑反推，否则是镜像验证。

### 完成度三层：implemented ≠ deployed ≠ externally verified（同源 principal-engineer verifying-before-done）
三层完成度不得跨层宣称：代码进了仓库≠跑在真实环境≠在外部系统里核实过。**用下层的证据宣称上层 = 虚报**。报告格式永远是 "PASS（查了 X 和 Y）"，不是光秃秃的对勾；无法验证时说"无运行面"（纯文档/类型声明适用此类别），**不拿别的关卡跑一遍来凑数**。

### 等价比较先剔除易变字段（同源 ownframework-loop 70f7a6d5）
比对两次产物/状态是否等价时，先剔除 timestamp 等纯易变字段再比整体结构——否则等价判定永远失败，或者被迫放宽比对范围变成假等价。

### findings 与 gaps 双通道独立报告：证据不完整 ≠ 一票作废（来源：trailofbits/skills #304 post-patch-validation 评级改 findings+gaps，2026-09-15 实拉）
验证结果不报单一评级，报**两条独立通道**：`findings`（已证实的失败：检查 ID + 断言 + 日志）与 `gaps`（缺失的证据：哪个检查没跑成、为什么）。关键语义：
- **部分失败 + 部分缺口并存时，两边都报**——一个检查超时/环境坏了，不掩盖另一个检查真抓到的失败；无关的超时不应隐藏 supported findings。
- **"整体不完整"只降低证据等级，不销毁已有发现**：退出码 10（不完整）时产物文件仍可能含已证实的失败——**读产物，别只看退出码**。
- 超时单独记为 gap，不升级成"回归"——超时本身不证明任何方向。

### 控制查询：区分"真无匹配"与"装置没工作"（来源：trailofbits/skills #288 burpsuite-project-parser，2026-09-15 实拉）
查询/搜索/检测类验证返回空时，空结果有两种解释：目标真不存在，或**检测装置本身没生效**（解析器没装、工具被静默吞了参数）。处置：改跑一个**必然有结果的宽对照查询**（同样的装置、足够泛的选择器）——对照有结果 ⇒ 窄查询的空是真匹配为空；对照仍空 ⇒ 装置坏了，按环境失败报，不报"未检出"。配套：分类器逐行分类整个流而非只看首行（日志前导行/许可头会被误判），空白行不算非预期输出。

### 进展证据用语义信号，不用 mtime 这类碰一下就动的信号（同源 planning-with-files 停滞检测）
判断"有没有在推进"时读**语义信号**（台账/日志里有没有新条目、产物有没有实质变化），不读 mtime/文件大小这类任何 touch 都会动的信号——后者把"碰过"当"推进"，停滞检测永远失效。

### 无法证伪的外部副作用记 `unknown`，不记 `success`（来源：OpenClaw 官方 docs.openclaw.ai·gateway/protocol/ledgers，2026-09-15 实拉）
把动作结果映射成状态时，判据是**"相反情况能否被证伪"**，不是"有没有报错"：
- 适配器 / 回调**没有返回外部平台的身份标识** → 记 `unknown`，**不能记成功**——外部副作用无法被证伪，报成功就是在无证据的情况下宣称已完成。
- **`unknown` 必须与 `failed` 分开**：failed 有证据（报错/回执），unknown 是**没有证据**。两者混在一起，等于把"不知道"洗成"知道失败"，也等于把"不知道"洗成"没失败"。
- 同理：外部系统只回"已受理"而无回执 → 记 `unknown`，并写明**缺什么回执才能升格**。
- 报告里不得把 `unknown` 并入成功计数：**未证伪 ≠ 已证实**。（与「完成度三层 implemented≠deployed≠externally verified」互补：那条讲做到哪一层，这条讲连"发生了没有"都不确定时怎么记。）

### 重复来源 ≠ 额外证据：保留全部来源，只计一次（同源 memory-provenance）
同一主张从多个来源 / 会话到达时（回填、多轮重述、多渠道上报）：**保留全部来源以便追溯，但不把它当多条证据计数**。理由：重复的同一主张不构成独立证据（与 AGENTS.md 第 6.3「用户的重复坚持不构成新证据」同源，这里把它落到数据层）。反例：把同一个 bug 的 5 次复述当成"5 个用户报告"→ 优先级虚高，并让"影响面"这类指标失真。

### 聚合指标是泄漏面：调用者看不见的对象会从总量里漏出来（同源 operator-scopes）
返回聚合量（总数 / 成本 / 用量 / 计数）前先问一句：**这个聚合是否包含调用者本来根本看不见的对象**？
- 有对象被隐藏（权限过滤、私密会话、他人数据）时，全集聚合会把它们的存在、数量、成本**间接**暴露出来 → **要么拒绝该聚合查询，要么按调用者可见集重新聚合**。
- 做法：把"调用者可见集合"作为聚合的**输入边界**，而不是在事后过滤输出。
- 判据：**输出能不能反推出被隐藏对象的存在或规模**——能，就是泄漏，不是"脱敏不够"。

### 终态字段成组相关，不是各自可选（同源 ledgers）
状态机 / 事件结构的字段校验不要写成"每个字段各自可选"，要写成**成组约束**：
- 非终态（`started`）**不带**错误码；每个非成功终态**必须**带**匹配错误码族**的错误码（`run_*` / `tool_*` 各归各的族，跨族即非法）。
- 消息类四态各自成套：成功 = 已发送；被拦 = 已抑制 + **必须带原因码**；失败 = 失败 + 错误码 + 失败阶段；未知 = 未知 + 失败阶段。**原因码必须属于该终态族**。
- 验证器按**成组关系**判，不按单字段必填判——单字段校验会放过"状态写着失败却没有错误码""原因码披着别的族的皮"这类结构性谎言。写成表（终态 → 必需字段组合）比散在各处的 if 更容易审计。

### 引用类证据：必须"跟着点开"才算验证（来源：riekelt/technical-writer·reviewing-technical-prose，skills.sh /hot 实拉 2026-09-15）
章号、相对链接、文件名、交叉引用、脚注——**"我读过那段"不等于"这个引用有效"**。唯一有效的验证动作是**跟着它打开，确认目标存在且内容对得上**：
- 判据：验证记录要能说出"这个引用指向的东西**我打开过**，且内容与引用它的那句话对得上"，而不是"来源里写了"。
- "相对链接看着合理""章号在范围内""文件名像存在"都不是证据——**推出来的存在不是存在**（与 §位置信息的唯一真源同源：那条管行号从哪来，本条管引用有没有落地）。
- 反模式：报告里写"引用已核对"，实际只通读了正文。

### 重审只报剩下的（同源）
二次验证 / 回归复审时，**只列仍未解决的问题**：
- 复述"上次提的 X 已修好"是**噪音**，而且会**掩盖真实状态**——读者分不清"还剩 3 条"和"这轮只查了 3 条"。
- 反过来，**判定为已解决的要留下可查的落点**（改在哪、哪条命令验的），但不占发现列表的篇幅。
- 与 §findings 与 gaps 双通道配套：**"本轮无发现"要显式写出来**（空列表是一个结论，不是一个可以省略的字段）。
- 与 `wb-doc-writing` 分工：本技能验**生成物的正确性**（代码 / 脚本 / 报告的事实与可运行性）；**文档本身写得好不好、该怎么改**走 `wb-doc-writing`（那条有不受理清单与去名测试）。

### 验证报告要标明"这条谁能修"，否则不该给作者（来源：OpenClaw 官方 docs.openclaw.ai·plugin-validation-fixes，2026-09-15 实拉）
一份扫描/校验产出里混着两类发现，**职责不同、出口也不同**：
- **作者可修**（author-facing）：能通过改元数据、清单、依赖声明、发布产物解决 → 交给作者，**每条都要带可执行的修复指引**。
- **扫描器维护者才知道的**（内部 coverage / 维护代码）：**只有扫描器维护代码、没有作者修复指引** → 这类**不该丢给作者**（他改不了，只会当成噪音）。
- 判据：**一条发现若写不出"作者下一步该做什么"，就不该出现在给作者的列表里**——否则报告的可信度被稀释，真正的可修项被淹没。
- 配套：修完必须**重跑同一个校验器**确认（不是"看起来改对了"）。

### 评级绑定具体版本，升级即失效；"未检测"是独立一等状态（来源：Dify 官方 blog《Trust Is a Feature》，2026-09-15 实拉）
- **评级只评估"当前版本"，每次升级后必须重评**；**旧评级不得凭惯性跟随新代码**。这直接否定"上次扫过没问题所以这次也没问题"。
- **`未扫描` 是正式等级**（可能是没扫、扫失败、或证据不足），**不得与"无问题"混同**——它和已通过是两回事，必须单独展示。
- **平台级标签（Official / Partner / Verified）可以支持决策，但不能替代构件证据**——标签说明"谁提供的"，不说明"这一版是什么"。
- **确认恶意/严重问题的对象绕过普通分级**，直接进入限制、移除或人工审查——**分级是常规路径，不是唯一出口**。
- 展示层：**颜色只用于加速识别，等级文字 + 警告文本 + 包名 + 版本号才是可审计的载体**（颜色不承重）。

### "没检查过"必须是独立状态，不能读成"通过"也不能读成"失败"；扫描触顶要随结论输出（来源：skills.sh audits + docs.openclaw.ai/gateway/security/audit-checks + concepts/usage-tracking，2026-09-28 r314-Q-B 实拉；作 §未检测是独立一等状态 的升级——把"未扫描"细化成可操作的四值与扫描元数据）
- **结论限定为四值：pass / fail / 未判定 / 不适用**——"未判定"专门容纳"没查过 / 查失败 / 证据不足"（与 §未扫描 同物，本条补成验收报告的**显式第四格**，不是默认的通过或失败）；skills.sh 审计结论枚举里 `Pending` 与 `Safe/Low Risk/Med Risk/Critical` **并列成第六个合法值**，证明"未检查"是独立等级而非缺省。
- **扫描器有硬截断且不报错**：OpenClaw 审计 "Deep code scans check up to 500 source files per plugin or skill"，目录遍历 100,000 条截止，"Some checks only run with `--deep`"——即"干净"可能只是"没扫到"，**报告必须把"是否触顶（文件数/条数上限）"与"本次跑的是浅扫还是深扫"作为元数据随结论输出**。
- **同一 checkId 的严重度依配置浮动**：OpenClaw 明文 "A severity like `warn/critical` means the same checkId can be emitted at either level depending on config"——单看严重度等级不可跨配置比较。
- **缺数据不得折算成 0**：OpenClaw 用量面 "A recorded zero-dollar cost is valid cost data"（0 元是数据不是缺失），同页 MiniMax 字段 `usage_percent`/`usagePercent` 因厂商语义相反需按厂校正后再入表——**字段语义先按来源校正再入表，缺值单独记未判定**。与 §未检测是独立一等状态 互补：那条管"为什么要把未扫描单列"，本条管"怎么把未判定写对 + 怎么暴露扫描本身的盲区"。
- 提升层：工具（验收判据）。触发词：未判定、Pending 状态、扫描截断、浅扫深扫、checkId 严重度浮动、缺数据不折算零。

### 阻塞与警告不得混同；"绿灯"不等于有判断力（同源 Dify）
自动化检查的产出必须分两档，**混淆二者会同时制造两种灾害**：
- **阻塞（blocking）**：证据越线即**停止发布**，不是"提醒一下"。
- **警告（warning）**：提供仍需人工判断的上下文，**默认放行但要求审查**。
- 混同的后果：**要么把危险对象常态化放行，要么把每个不寻常的实现都升级成小危机**——两种都让检查本身失去意义。
- **自动化增强评审者，不会因为流水线全绿就获得判断力**：绿≠正确，只等于"没触发已定义的规则"。凡"规则没覆盖到但看着不对"的情况，仍需人工出口。（与 §断言判别力、§完成度三层互补：那两条管"检查本身是否有效"，本条管"检查结果怎么定级"。）

### 输出/工具调用前的护栏四模式 + 内置检测器（来源：Pydantic AI guardrails 文档，2026-09-27 实拉）
验证不止"放不放行"一档，护栏要按**处置动作**分四类，且应在内容离开 agent 之前就拦：
- **block（阻断）**：命中即不下发（对应 §阻塞与警告 的 blocking 档，但这里是内容层而非发布层）。
- **redact（脱敏）**：把 secret/PII 字段就地替换成占位符，内容其余部分照常走。
- **retry（重试）**：换措辞/降约束再生成一次，仍不达标才升级。
- **require approval（转人工）**：高风险动作（发信/付款/删除）交人确认，不自动过。
- **内置检测器**：secret（密钥）/ PII（个人身份信息）两类应有现成检测器自动识别，不必每次手写正则。
- 判据：**这四种是"同一道关"的四种出口，不是四道关**——一次校验先决定走哪条，别为每类风险各起一条独立流水线（与 §职责分流 同一思路：出口不同但要合并判据）。

### "没出事故"不是"控制冗余"的证据（来源：Dify 同文引 GlassWorm / 假扩展事件）
- 一起事件**影响很小**（很短时间内被下架、只有个位数下载安装），**是控制生效的结果，不是控制不必要的证据**。反推"反正没造成损失，所以这道控制可以砍"是把幸存者偏差当成本分析。
- 正确读法：响应速度是控制链的一环，**"影响小"恰恰说明检测与响应来得早**；评估控制该不该留，看的是**若它不在，最坏情况是什么**，而不是**这次它有没有用上**。
- 与"删除规则前先确认根因已修"配套（`wb-skill-authoring` §规则生命周期）：**控制的退役条件是根因消失，不是没再出过事**。

### 指标必须带口径；没有分母的数字是"看起来很自信的轶事"（同源 Dify）
同一份数据能产出多个**都正确**的数字，但它们描述**不同总体**。发布/引用任何指标前先补齐：
- **快照日期 + 定义 + 局限**，写在数字旁边（缺一不可）。
- **两个精确数字可以回答两个完全不同的问题**：例如"打某标签的条目数"（快照里的标注情况）与"评审者确认在维护的基线数"（实际运行状况）——**把前者当后者的证据，就是干净、方便、且错误**。
- **不同动词不可互推**：**安装 ≠ 调用 ≠ 可靠 ≠ 业务价值 ≠ 维护健康**。安装量说明分发，调用量说明某窗口内的实际使用；任一单独都不足以支撑"可靠"这类结论。
- **计数型指标先自查口径完整性**：若身份信息有缺失、计数器会重置，绝对计数可能**少报数倍** → 此时**只用于相对趋势 / 份额 / 排名，不做绝对量叙述**，并把这个限制写出来。
- 判据：**没有分母的指标只是一个看着很自信的轶事**。

### 失败要区分"根本没到达"与"到达后失败"，且用稳定码不用自由文本（来源：OpenClaw 官方 docs.openclaw.ai·auth-credential-semantics，2026-09-15 实拉）
- 探测/检查结果 = **状态桶**（如 ok / auth / rate_limit / billing / timeout / format / unknown / no_model）**+ 稳定 `reasonCode`**；**"这次检查根本没走到真正执行那一步"必须单列并带码**，不能笼统记为失败。
- 典型"没到达"的码各自区分成因：**被显式顺序排除**、**缺凭据**、**已过期**、**过期字段非法**、**引用解析不出来**、**与配置不兼容**、**凭据有但没有可探测的目标**。**这七类处置完全不同**（该换凭据 / 该改配置 / 该修顺序 / 该重建目标），合成一个"失败"等于把排障信息扔掉。
- **被显式排除的对象不得在后续流程里被静默重试**：要么按排除处理并**在输出里报出来**，要么明确说明这是有意例外（如"某会话级手动指定优先"）——**静默回退重试是最难查的偏差**。
- 稳定码是**可统计、可断言、可跨版本比对**的；自由文本错误信息只能人读。



---

按需阅读（渐进披露，不要常驻加载）

本正文只保留验证决策级核心。方法论来源、判据推导、反模式、特殊场景全部在
[references/knowledge-base.md](references/knowledge-base.md)（完整知识库，下沉于 2026-09-26）。
**先 Grep 定位关键词，再读对应节**。主题速查：发现要有边界 · 优先级与确定性分开 · 预算先给挑错 · 产物回收防调换 · 扫描器看不透先拒收 · 可疑项沙箱实跑 · 多复核者一致度分级 · mutation-testing · 独立 Oracle · 随机差分模糊测试 · 迁移三步验收与不可逆标注。
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
## 资格判定三态（不确定不禁用、禁用带可见且可撤销的理由）；自动修复严守证据自证门槛（来源：docs.openclaw.ai/automation/cron-jobs/payloads.md 27,960B + managing-jobs.md 17,374B，2026-10-01 r343C 独立 curl 实拉逐串命中）

- **原文**：①「In `auto` mode, a review **stays disabled when every statically resolvable model candidate is known to lack** rooted execution support. Its display name includes `no-rooted-runtime` ... **unknown eligibility also keep it enabled, with final checks at execution time**.」「**Convergence clears the reason and restores auto-mode enablement** when the configured chain becomes eligible or unknown.」；②「Doctor **reconciles the account only when the stored creator identity proves it**, and reports the repair.」「**Doctor does not infer ownership from delivery settings or the current caller.**」「Jobs whose stored identity cannot prove an account need **authenticated administrator recovery**.」
- **判据**：① **资格判定是三态而不是二态：确定不合格 → 禁用并带**可见理由**（把理由写进可枚举的载体，如显示名带 `no-rooted-runtime`）；确定合格 → 启用；**未知 → 保持启用，把终判推迟到执行时**。且**收敛过程会清除理由并自动恢复启用**。⇒ 两条硬纪律：一是**"不确定"不等于"不合格"**——把未知当不合格会让环境一变就大面积静默停摆；二是**任何自动禁用都必须带可机读的理由，且理由要能被自动撤销**，否则禁用会变成需要人工考古的持久态。② **自动修复的边界是"证据自证"，不是"看起来说得通"**：修复器只在存储身份本身能证明归属时才动手，绝不从旁证（投递设置、当前调用者）反推归属；证据不足时走显式的管理员恢复通道，而不是猜一个最可能的。⇒ 写自愈/迁移工具时，先定义"什么算充分证据"，达不到就**明确转人工并报出去**；用旁证推断归属是数据污染的高发源——它会把"谁在用"悄悄改成"谁的所有物"。
- **提升层**：工作流/安全边界。触发词：资格三态、不确定不禁用、禁用带可见理由、no-rooted-runtime、收敛自动清除理由、自动修复证据自证、不从旁证推断归属、证据不足转人工。

- **「解析基准」≠「隔离边界」（默认 cwd 非硬沙箱 / 沙箱接管后同名不同体 / 越界别名静默忽略 / 不可读源不可删）**：本章已下沉 references/knowledge-base.md §r346A。

- **涉密分发分「模型可见面/人类可见面」+ 隔离粒度是显式旋钮（默认不隔离会话间）+ 内层沙箱缺失须正面申报**：本章已下沉 references/knowledge-base.md §r346B。

## 降档/资格判定按成因分档，且只有一类会告警：配置意图 / 角色封顶 / 后端能力矩阵缺项（来源：docs.openclaw.ai/gateway/sandboxing/{workspace-access,what-gets-sandboxed,supported-capability-matrix,images-and-setup}，2026-10-01 r362-Q-C 实拉）
- 判据：① 三类成因完全不同：**配置意图**（用户显式设 `workspaceAccess=none`）、**角色封顶**（role 要求沙箱时配置里的 `rw` 被静默降级为 `ro` 并告警）、**后端能力矩阵缺项**（网络限制仅 Docker 有 `docker.network`，SSH/OpenShell 交宿主；沙箱浏览器仅 Docker；插件/MCP 三家都是 "Gateway 侧执行 + sandbox tool policy 再门控"）。② 资格/降级报告须按成因分档，不能统一写"配置未生效"——只有"角色封顶"这一类会告警，其余静默。③ 空转例外：沙箱关闭时 `tools.elevated` 例外通道无意义。
- 提升层：工具/可复用 Skill。触发词：降档三成因、角色封顶告警、能力矩阵缺项、elevated 空转。

## 投递验收必须双字段分列，且二者可同时矛盾：外发成功 ≠ 回合完成，超时=Unknown 且不重试（来源：docs.openclaw.ai/automation/cron-jobs/delivery，2026-10-01 r362-Q-C 实拉；呼应 r340C 投递回执）
- 判据：① `status:"ok"` 可与 `completionStatus:"failed"` 并存——"账面成功"与"回合完成"是两个独立判据。② webhook 只以 2xx 判送达，超时记为 `Unknown` 且不重试 ⇒ 存在第三态"未知"，且只有"疑似从未送达"才自动重试。③ 幂等条款："同一结果不能 append 两次 / 每周期至多一次外发"。⇒ 任何投递验收不得只看单一 status 字段，须同时断言完成字段与"未知"态。
- 提升层：工作流。触发词：status ok 与 completionStatus failed 矛盾、Unknown 第三态、2xx 才送达、双字段验收。

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


## r353A · 失败现场的处置由开关决定，取证能力会被隐私开关直接削掉（来源：help.make.com `scenario-settings.md` 5,172B + `incomplete-executions.md` 1,632B，2026-10-02 r353A 实拉）

- **★"保留现场"默认是关的**：`Store incomplete executions` 默认 disabled；关闭时失败的运行**直接停止并进入 rollback phase**；只有开启后，未完成运行才被存进 *Incomplete executions* 并把场景暂停。判据：**默认假设是"失败即回滚"，不是"失败即留证"**——按"能事后翻现场"设计的验证方案，必须先确认这个开关是开的。
- **★顺序执行与未完成执行互相阻塞**：`Process data in order` 开启后，**只要存在未解决的不完整执行，新运行一律不处理**；webhook 默认并行，开启该选项才改为等上一次跑完。判据：**"保序"的代价是把一次失败升级成整条链路停摆**，验证时要显式声明是否允许这种停摆。
- **★存储满时优先保可用性**：`Discard data if storage is full` —— 失败数据被**丢弃并让场景继续运行**，原文 "Discarded data can't be recovered"。判据：**这是显式的可用性 > 完整性取舍**，且不可恢复；落此配置的场景不能承诺零丢失。
- **★隐私开关会削掉排障能力**：`Keep data confidential` 开启后日志只显示"发生过一次运行"、**不含 payload**，官方同步警告 "there are very limited options to solve errors"；不完整执行的数据**计入订阅存储配额**，超限报错。判据：**可观测性与隐私在这里是同一个旋钮的两端**——开隐私即降取证，排查"为什么失败"要先把这条列为已知盲区。
- 落地口径：写验证/回滚方案时先声明三个开关（保留不完整执行 / 保序 / 保密）与配额余量，再声明失败时走的是回滚还是留存。
- 提升层：工作流 / 可复用 Skill。触发词：不完整执行、incomplete executions、回滚阶段、保序阻塞、丢弃数据、保密日志。


## r353B · 错误契约随失败位置分叉，取证通道可用 `.md` 后缀直取（来源：docs.n8n.io `build/flow-logic/handle-errors-gracefully.md` 5,136B，2026-10-02 r353B 实拉）

- **★错误负载不是单一 schema**：常规节点失败给出 `execution{}`（`id` / `url` / `retryOf` / `error.message` / `error.stack` / `lastNodeExecuted` / `mode`）；**触发器节点失败时形状完全不同**——主体变成 `trigger{}`（`error.context` / `name` / `cause` / `timestamp` / `message` / `node`）、`mode: "trigger"`，且 `execution{}` 里信息更少。判据：**同一套错误处理代码必须按"失败发生在触发器还是后续阶段"分支解析**，用一套 schema 解析所有错误会在触发失败时整片取空。
- **★字段存在性依赖"执行是否入库"**：`execution.id` 与 `execution.url` 都要求该执行已存库——"Not present if the error is in the trigger node of the main workflow, **as the workflow doesn't execute**"；`execution.retryOf` 仅当这是一次重试时才出现。判据：**缺失字段不是解析 bug 而是语义**——先问"这次失败有没有形成一次执行"，再决定能不能按 id 串联日志。
- **★机器可读取证通道：文档站追加 `.md`**：原文 "Markdown versions of documentation pages are available by **appending `.md` to page URLs**"（同 URL 的 HTML 页 596,419B 是 SPA 壳、`.md` 页 5,136B 是真正文）。判据：**对外取证优先找机器可读入口（llms.txt / llms-full.txt / `.md` 后缀），HTML 页常常是空壳**——本轮 dify `llms-full.txt` 2,990,942B、flowise 618,913B、langflow 6,782B 同样一次取全。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：错误工作流、Error Trigger、execution 与 trigger 两种错误体、retryOf、.md 取证通道。


## r353C · 事务边界由模块能力标注决定；验证有自己的预算币种；文档站提供问答式检索接口（来源：help.make.com `scenario-execution-cycles-and-phases.md` 6,351B、pipedream `docs/workflows/limits.md` 9,086B、docs.n8n.io `debug-executions.md` 2,467B 与 404 页，2026-10-02 r353C 实拉）

- **★事务是三阶段，且回滚能力不是普遍的**：执行分 Initialization（建连接并校验、检查每个模块能否执行）→ 至少一个 cycle（operation phase + commit/rollback phase）→ Finalization；"Each cycle represents an **indivisible unit of work**"，默认最大 cycle = 1。关键约束：原文 "**Not all modules allow for rollback.** Modules that support rollback are marked with the `ACID` tag. Modules without this tag **cannot be reverted**"。判据：**"会回滚"这句话的成立范围由链路上每个模块的 ACID 标注决定**——只要含一个无标签模块，该 cycle 的原子性承诺就整体失效；验证前必须逐个核标签，不能拿"它是事务系统"当结论。
- **★commit 阶段失败照样回滚**："If an error occurs during the operation **or commit phase** for any module, the phase is aborted and the rollback phase is started"。判据：**提交不是终点**——"已经提交成功"只有在整个 cycle 结束时才成立，中途提交失败会让本 cycle 全部作废。
- **★验证运行有自己的预算，且币种与生产不同**：pipedream 免费档每天 **750** 次测试执行 / 30 分钟 testing runtime，且 "You **do not** use credits testing workflows"。判据：**测试额度是独立配额，不消耗生产 credits** —— 按"测试跑得多会吃掉生产额度"做的节流假设是错的，反过来"生产额度充足"也不代表测试额度够用。
- **★重放能力按部署形态门控，入口按成败分叉**：n8n 的 "Debugging and re-running past executions" 在 Cloud 全计划可用，自托管**仅 Registered Community / Business / Enterprise**；失败执行入口是 **Debug in editor**，成功执行是 **Copy to editor**，数据被 **pin 在第一个节点**。判据：**"能不能重放"先问部署形态，再问执行成败**；而数据被钉在首节点意味着**重放的输入面是整个工作流的第一节点**，不是出错的那个节点。
- **★文档站有问答式检索接口（取证通道再升一级）**：n8n 404 页明示——对任意 `.md` URL 追加 `?ask=<自然语言问题>&goal=<更宽目标>` 可由 GitBook **直接给答案并附摘录与来源**；另有 `sitemap.md` 全索引、`llms-full.txt` 全量导出；"Prefer `.md` URLs for structured content"。判据：**拿不到精确页名时不要放弃——先用 ask 接口问，再用 sitemap 定位**，比逐个猜 URL 高一个数量级。
- 提升层：工具 / 工作流 / 可复用 Skill。触发词：ACID 标签、cycle 不可分割、commit 失败回滚、测试额度、Debug in editor、pin 在首节点、ask 检索接口、sitemap.md。


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
