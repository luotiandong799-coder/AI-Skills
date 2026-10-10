---
name: system/skills-security-check
description: "腾讯云鼎实验室出品，Skill安全审查工具。对用户指定的skill.md文件及其配套的文档、程序、脚本等进行全面安全审计，确保引用安全"
description_zh: "腾讯云鼎出品，Skill 安全审计工具"
description_en: "Scan a third-party skill for security risks before enabling it"
version: "1.40.0"
allowed-tools: Read, Grep, Glob, Bash
display_name: "system/skills-security-check"
display_name_en: "system/skills-security-check"
visibility: "public"
---
> 正文预算管理：「功能描述（全文见 references/knowledge-base.md §下沉·sk」（全文已零删减下沉 references/knowledge-base.md §下沉·功能描述（全文见 references/knowledge-base.md §下沉·sk）
## 约束（全文见 references/knowledge-base.md §下沉·skills-security-check·r439·约束）

> 正文预算管理：「🎯 审计核心原则：关注供应链投毒风险」（全文已零删减下沉 references/knowledge-base.md §下沉·🎯 审计核心原则：关注供应链投毒风险）
## 执行逻辑（全文见 references/knowledge-base.md §下沉·执行逻辑）

## 📊 执行摘要
- **审计对象**: [skill名称和路径]
- **发现问题总数**: X个
  - 🔴 Malicious（恶意）: X个
  - ⚠️ Suspicious（可疑）: X个
  - 📝 信息性提醒: X个（非风险项，不计入风险总数）
- **安全评分**: [0-100]分

---

## 🔴 Malicious（恶意）风险发现
[如果没有，显示：✅ 未发现 Malicious 风险]

1. **[问题类型]**
   - **位置**: 文件名:行号
   - **代码片段**: `具体代码`
   - **风险描述**: 详细说明安全风险
   - **攻击场景**: 攻击者可以如何利用
   - **修复建议**: 具体的修复方案

---

## ⚠️ Suspicious（可疑）风险发现
[如果没有，显示：✅ 未发现 Suspicious 风险]

---

## 📝 信息性提醒（非风险项）
[Step 0 排除的作者自身凭证泄露等不构成投毒风险的发现项归入此处。如果没有，显示：✅ 无信息性提醒]

1. **[问题类型]**（信息性提醒）
   - **位置**: 文件名:行号
   - **代码片段**: `具体代码`
   - **说明**: 该凭证为作者自身凭证，不构成对用户的投毒风险
   - **建议**: 建议作者改用环境变量管理敏感凭证

---

## 📋 详细检查结果

### 命令执行与权限检查
- 发现次数: X次
- 详细列表: [列出所有匹配的行号和内容]

### 文件操作与敏感路径检查
- 发现次数: X次
- 详细列表: [列出所有匹配的行号和内容]

### 网络请求检查
- 发现的URL: [列出所有URL]
- Base64编码检测: [是否发现可疑编码]

### 远程脚本深度分析
[如果存在自动下载+执行的远程URL，对每个URL列出深度分析结果]
- **URL**: [具体URL]
- **脚本可访问性**: [可访问 / 不可访问 / 二进制文件]
- **发现的恶意/可疑行为**: [具体列举，或"未发现明显恶意行为"]
- **脚本主要功能**: [一句话总结]
- **深度分析结论**: [当前内容安全性评估]
- **定级影响**: [基于深度分析结论，该风险项最终定级为 Malicious/Suspicious，并说明理由]

### 依赖安装风险检查
- **全局安装检测**: [是否发现全局安装命令（Suspicious（可疑）环境破坏风险）]
- **虚拟环境检查**: [是否提供虚拟环境隔离说明]
- **依赖来源检查**: [是否从非官方源安装（Suspicious（可疑）潜在风险提示）]

---

## 💡 总体建议

[根据发现的问题给出总体改进建议]

---

## ✅ 审计结论

**风险等级**: [基于 Malicious / Suspicious / Benign 标准判定]

**使用建议**:
- ✅ **Benign（可信）- 可以安全使用**（76-100分）：无投毒风险，纯教学内容
- ⚠️ **Suspicious（可疑）- 建议改进后使用**（31-75分）：存在环境风险或供应链风险，建议确认后使用
- 🚫 **Malicious（恶意）- 严禁使用**（0-30分）：存在自动执行危险操作的投毒风险
```

---

## 重要提示

⚠️ **执行此skill时必须**：

1. 完整执行所有步骤（含步骤4远程脚本深度分析）
2. 对存在风险的每个检测项给出明确结果
3. 不跳过任何搜索步骤
4. 提供完整的行号和代码片段
5. 给出明确的安全评分和使用建议
## 学习轮章节（已下沉 references/knowledge-base.md，正文留指针）

- 🏛️ 平台级技能准入参考模型 → 

- Skill 安全风险九类分层（T01–T09）：审查要按"攻击面层级"过，不按文件顺序过 → 

- 审查别拿"符合性代理"当技术证据：记录面要按三类缺陷主动查，不看厂商标签 → 

- 控制门的延迟会诱发绕过：安全开销本身就是合规率的一部分 → 

- 审阅/验证第三方技能这一步本身不得引入运行期副作用：Staging 不跑 install/build/postinstall，按对象类型选扫描器 → 

- 内容可读与代码可执行必须分两档：远端技能包可全文下发、强校验，但包内脚本永不执行；同步排除清单把可信钩子挡在不可信沙箱外 → 

- 风险分层按「是否含可执行资产」，不按文本扫描结论；技能文件本身就是注入载荷 → 

- 本地小模型审计技能包要走"证据引导两段式"，不能让 compact LLM 直接判 → 

- 信任信号要逐维度报覆盖率，不能只给一个总通过率；单维 100% 可能掩盖其他维几乎为零 → 

- 门控资格与分诊资格是两档：一个检测配置有没有「门控资格」由它对良性样本的标记率单独判定，召回提升换不来门控权 → 

- 允许集与校验集是两个集合：字段被接受不等于字段被检查，名字像安全承诺的字段尤其危险 → 

- 审查结论要有一个显式的「不处置」档位，且误报形态可枚举：不是每条读数都要整改，关闭必须带理由 → 

- 出站副作用要在 frontmatter 里声明成契约，审计器不执行也能判：外发字段与失败姿势必须可静态读 → 

- 来源要分两个锚：registry 上的 owner 只是分发渠道标签，不等于发布者密码学证明 →

- 扫描判级三原则（能力≠滥用、云端判定缓冲、Safe 模板禁无证据默认✅）：扫描器判定要区分「能力存在」与「能力被滥用」——敏感原语（bash/子进程/读密钥/env）若属声明功能所需且有文档，只报能力不判恶意；云端 risky 不默认高危，按实际影响二次映射，unknown/请求失败必须降级本地审计并记「云情报不可用」；Safe 输出模板禁止无证据默认✅，须附「静态分析不覆盖后续更新风险」免责（来源：matrix.tencent.com/clawscan/skill.md 46,622B，2026-10-07 独立 curl 实拉逐串命中 `ability vs Abuse`/`can do dangerous`/`base64`/`zero-width`/`ROT13`；与 §审查结论要有「不处置」档位 互补——那条管误报形态枚举，本条管扫描判级的总原则）
- **判据**：① **「能做事」与「在做坏事」是两层判定**：扫描器若一见危险原语就标 Medium+，会把"声明功能需要的敏感能力"误判为恶意 ⇒ 判定逻辑要先问"这个能力是否为该技能声明功能所必需且已文档化"，是则不升恶意、只作能力登记。② **云端分级结论要带缓冲**：risky 类结果默认不映射到高危，必须按本地实际影响二次判定；云端情报不可用（unknown/请求失败）时降级到本地审计并留痕，不许假装云端结论存在。③ **Safe 模板的✅必须基于证据**：无证据不得默认给通过章，且强制附"静态分析不覆盖后续更新"免责，防止"扫过=安全"的错误暗示。④ 与既有「审查结论要有显式不处置档 + 误报形态可枚举」构成"判级原则 + 误报枚举"双层，本条是原则层。
- 提升层：可复用 Skill / 工具。触发词：能力-滥用二分、声明功能所需才报能力、risky 不默认高危、云端降级本地审计、Safe 模板禁无证据默认✅、静态分析不覆盖后续更新。

- 漏洞类别全清单（17 类 / 68 模式）作扫描规则覆盖度对照表，Triage 处置动词表五档（阻断至修或正式接受 / 发布前移除 / 欠声明→改权限或删行为 / 有漏洞依赖→升级-pin-文档化豁免 / 描述-行为失配→改描述或改代码），报告格式含 SARIF 入 CI（来源：docs.nvidia.com/skills/scanning-agent-skills.md 4,822B，2026-10-07 独立 curl 实拉逐串命中 `Memory poisoning`/`Trigger abuse`/`Taint tracking`/`YARA`/`MCP least privilege`/`MCP tool poisoning`；与 §审查九类 T01–T09 互补——九类是自家分层，本条是 NVIDIA 公开 17 类全清单，可作覆盖度对照）
- **判据**：① 自家九类分层要对照公开 17 类找覆盖盲区（如 memory poisoning / trigger abuse / taint tracking / YARA / MCP least privilege / MCP tool poisoning 等是否已在自家判级里）。② **处置动词要可机检**：每条发现对应一个明确动作（修 / 删行为 / 文档化豁免 / 改描述），含糊的"建议注意"不算处置。③ **SARIF 入 CI** 使扫描结果可进流水线条件，不只是给人看的报告。
- 提升层：工具。触发词：17 类漏洞清单、68 模式、Triage 五档处置动词、SARIF 入 CI、覆盖度对照。

- 信任徽标必须自带「负向适用范围」声明：徽标/扫描结论若只报"已覆盖的项"，要同时写明它**不裁定**的那一面（如 AIPM Registry 明示 "metadata checks, not a malware verdict"——元数据校验≠恶意裁决）（来源：aipm-registry.com/research/state-of-agent-skills-2026 43,058B，2026-10-07 独立 curl+UA 实拉逐串命中 `metadata checks`/`not a malware verdict`/`1%`/`Organization`；与 §信任信号要逐维度报覆盖率 互补——那条管"维度覆盖率要分别报"，本条管"结论要明示不裁定面"）
- **判据**：① 任何对外展示的信任信号（徽标/扫描通过章/评分）都要写清它**不证明**什么，否则读者会把"部分覆盖"读成"整体安全"。② 与覆盖率倒挂同族但机制不同：覆盖率倒挂管"各类信号实际占比要公开"（1% 组织审查伪装成 100% 安全感），本条管"每个信号本身要声明否定式适用范围"。
- 提升层：可复用 Skill。触发词：信任徽标负向适用范围、metadata checks not a malware verdict、声明不裁定面。

## r436A-r436A2（全文已下沉 references/knowledge-base.md §r436A-r436A2；2026-10-09 r484 正文预算下沉）
## 技能「形态」应在内容审查之前先定权限档：是否捆绑可执行脚本是可静态判定的事实，直接决定权限下限——实测 bundling executable scripts 使漏洞风险 2.12×（来源：arxiv.org/html/2602.12430v4 169,999B，2026-10-08 独立 curl 实拉逐串命中 `Skills bundling executable scripts are 2.12` / `An unvetted community skill (T1) receives instructions-only access with full tool isolation` / `T1 and T2 skills are never granted script execution` / `Level 3 executable scripts require T3 or T4 trust`；与 §恶意产能按发布者聚合熔断 互补——那条管封禁的作用域单位，本条管单个技能安装前的权限先验档）
- **判据**：① **形态先于内容**：有无 `scripts/`、frontmatter 是否声明可执行资源，是零成本可判的事实；把它作为权限档输入，可在读第一行代码前就把默认权限压到 instructions-only（T1/T2 永不授予脚本执行），审查资源优先投给含脚本者。② **2.12× 是分诊权重不是罪名**：倍数是排队依据（含脚本优先深审、加行为回归），不是「含脚本即恶意」。③ **与行为定档串联而非替换**：既有按沙箱观察后定档是事后校验，本条是事前先验，串成「先验给下限、行为校验再升降档」。④ 数字须连原文位置引：2.12× 出 Sec 6.2 实测、T1–T4 出 Sec 6.4 权限映射，混引会造出不存在的因果。（细则见 references/knowledge-base.md §r437A）
- 提升层：可复用 Skill（准入策略 / 权限先验）。触发词：形态先验权限档、2.12×、T1/T2 不授予脚本执行、Level 3 脚本需 T3/T4、含脚本优先深审、先验档与行为定档串联。


## 风险档位只由「可能性 × 影响」决定，不得按「偏离清单的条目数」打分；判定三态中未确认项被显式剥夺 severity，且检查者不得是发现者（来源：github.com/cloudflare/security-audit-skill 295,484B，2026-10-08 独立 curl 实拉逐串命中 `Severity requires impact.` / `Likelihood x impact, not deviation from a checklist.` / `confirmed, needs_validation, and rejected` / `The agent that checks a finding is never the agent that found it.`；与 §扫描判级三原则 互补——那条管能力≠滥用，本条管定级的算术与判定者分离）
- **判据**：① **符合度不是风险**：偏离清单条目多不等于风险高，只有 likelihood×impact 才是定级输入；把「不符合项计数」当风险分会让清单越长风险越高。② **三态各带约束**：`confirmed` 需 complete source trace + bounded observed result；`needs_validation` 只记未决事实、**禁带 severity**（未证实的候选不得预先打分）；`rejected` **显式记录被证伪的候选**（不静默丢弃）。③ **检查者≠发现者**：验最终源主张要用 fresh agent，不复用原 detector。（细则见 references/knowledge-base.md §r437C-4）
- 提升层：可复用 Skill。触发词：Likelihood x impact、not deviation from a checklist、needs_validation 禁 severity、rejected 记录被证伪候选、检查者不等于发现者。

## 运行期可执行面的允许清单，声明权归「部署运营方」而非技能作者：作者侧管字段可见性，运营方管命令可执行性——两个声明者要分别检查（来源：github.com/FlowiseAI/Flowise/releases/tag/flowise@3.1.4 213,716B，2026-10-08 独立 curl 实拉逐串命中 `Fix Flowise 709 Make Custom MCP stdio command allowlist operator-controlled by @yau-wd in #6578`；与 §出站副作用声明成契约 互补——那条管作者声明外发面，本条管谁有权定义可执行命令面）
- **判据**：① 审计允许清单时先问「这份清单是谁写的」：作者随包提交的允许清单是**自证**，运营方在部署期注入的才是外部约束；二者同名但约束方向相反（作者想放宽以便运行 vs 运营方要收紧以便管控）。② 同一技能可以两面都有，审计报告须分列两个声明者，不许合并成「已配置允许清单」。③ 运行期命令面（stdio 命令、可执行路径）属运营方所有权，作者无权自授。（细则见 references/knowledge-base.md §r437C-5）
- 提升层：可复用 Skill。触发词：允许清单声明权、operator-controlled allowlist、作者自证 vs 运营方约束、运行期命令面所有权、两个声明者分列。

## 批准不是权限本身，而是「派生关联」：每次使用都要对活的授权行再验证，且批准绑定的是规范化执行上下文（cwd + 精确 argv + env 绑定 + 固定可执行路径），启动前重解析重检查（来源：docs.openclaw.ai/tools/exec-approvals 一手 363,977B，2026-10-08 r438B 独立 curl 实拉逐串命中 `a grant is derivative correlation, revalidated against the live approval row, automation row, and revocation state on every use` / `bind canonical execution context: cwd, exact argv, env binding when present, and pinned executable path` / `re-check it before launch` / `not a per-user auth boundary or filesystem read-only policy`；全库 grep `revalidated` / `exact argv` 均 0 命中）
- **① 授权状态不能缓存**：批准记录是**对另一行授权状态的派生关联**，不是一份自足的权限；每次使用都要拿活授权行 + 自动化行 + 吊销状态三者重新对一遍。判据：**审计"有没有权限"时，看的是再验证的动作，不是批准记录的存在**；只查"批过没有"等于把可撤销的引用当成了既得权限。
- **② 批准要钉到可执行身份，不能钉到命令名**：批准的粒度是规范执行上下文——cwd、精确 argv、env 绑定、固定可执行文件路径；网关侧在评审前绑定每个解析出的命令段可执行文件，**启动前再检查一次**。原文同时给出边界声明：这只降低误执行风险，**不构成按用户的认证边界，也不构成文件系统只读策略**。判据：审查批准/白名单机制时问三件事——绑的是名字还是 argv+路径？启动时重不重查？文档有没有把"批准过"说成"有权"？三者任一答错即判缺陷。
- 提升层：可复用 Skill（权限模型）/ 工作流（运行期授权复核）。触发词：批准不是授权边界、derivative correlation、revalidated on every use、exact argv、pinned executable path、re-check before launch、授权不能缓存、批准粒度、per-user auth boundary


## 审批校验要验「记录的签发者是否有权为本动作签发」，不能只验记录存在：跨技能链把伪造审批藏在单技能扫描的盲区（来源：arxiv.org/abs/2610.01564 + /html/2610.01564v1 293,934B，2026-10-08 一手实拉）
- **实证**：APEX 全链攻击成功率 **84.3%**，而把同样的两步合并进**单个技能**只有 **17.4%**；512/690 attempts＝**74.2%**；提示层防御把良性 verifier 通过率从 **86.7%** 压到 **56.3%**。原文机制：「an agent-written record of genuine task progress can carry a false claim of user approval across skills」「an upstream skill induces the agent to create the record, and a downstream skill ...」。
- **判据**：① **风险藏在链上，不在件上**——单技能静态扫描对本类攻击天然高漏（84.3% vs 17.4% 的差值就是链带来的增量），审计必须按**调用序列**而非单包取证；② 消费侧见「已批准」记录时，要回溯**该记录的签发者是否被授权签这一类动作**，只验存在性等于把上游诱导当授权；③ **防御代价必须与攻击成功率并列报告**（86.7%→56.3% 的可用性损失不是免费的），只报拦截率的防御方案不可验收。
- **与既有能力分工**：r437C「允许清单声明权归运营方」管**谁有权写清单**；本条管**跨技能传递的审批声明由谁签发**——两处都是「声明者身份」，但一在授权面一在传递面，须分别检查。
- 提升层：工具（取证面）/ 工作流（审计序列）。触发词：链式审批伪造、84.3 vs 17.4、agent-written record、跨技能链、签发者权限、防御代价并列报告。


## 技能根目录是「容纳边界」：装载时对越根软链一律跳过并留原因位，共享靠显式白名单目录而非隐式跟随（来源：docs.openclaw.ai `/gateway/troubleshooting/skills-and-model-providers` 247,412B，2026-10-08 一手实拉）
- **实证**：官方日志形态「Skipping escaped skill path outside its configured root: ... **reason=symlink-escape**」；定性原句「**Every skill root is a containment boundary**」——`~/.agents/skills`、`<workspace>/.agents/skills`、`<workspace>/skills`、`~/.openclaw/skills` 下的越根软链一律 skip；放行须同时具备显式 `extraDirs` + `allowSymlinkTargets`，且 `~`、`/` 这类宽目标被禁。
- **判据**：① **复用技能不许用软链"借道"**——把外部目录链进技能根等价于让该目录绕过一次准入审查；共享只能走显式登记的额外目录白名单；② **跳过必须留原因位**（`reason=symlink-escape`），静默跳过会让"技能没生效"变成无痕失败，排查时看不到被拒的那一次；③ **白名单目标是路径精度问题**：`~`、`/` 这类宽目标一旦开了等于边界失效。
- **与既有能力分工**：r437A「形态先验权限档」管**有没有脚本决定权限下限**；本条管**技能根之外的内容能不能被带进来**——前者是权限档，后者是容纳面。
- 提升层：工具（装载面）/ 工作流（准入）。触发词：容纳边界、symlink-escape、越根软链、extraDirs、allowSymlinkTargets、技能没生效无痕失败。

## 复审的记分对象是「新增」不是全量；LLM 语义阶段只升不降置信，未确认项须显式打 `llm-unconfirmed`（来源：api.github.com/repos/NVIDIA/SkillSpector/contents/README.md 53,632B 全解，2026-10-08 一手实拉）
- **实证**：官方原文「Scan against the baseline — **only NEW findings are reported and scored**」；「Findings the model reviews but does not confirm (disputed, low-confidence, or unaddressed) are tagged **`llm-unconfirmed`** in JSON and SARIF output」。
- **判据**：① **跨轮扫描必须区分三态：新增 / 已被 baseline 抑制 / 未确认**——把全量重贴当"本轮发现"会让同一个 finding 在每轮报告里重复计分，风险趋势图上看到的是基线漂移而非真实新增；② **模型没确认的东西不许当已确认**：语义阶段只升不降置信 ⇒ 未确认项要单独留标签位，混进 confirmed 会让"AI 复核过"变成虚高可信度；③ baseline 是记分口径的一部分，**换基线等于换量纲**，跨基线比较前必须先对齐基线版本。
- **与既有能力分工**：r437C「风险档位 = likelihood×impact，needs_validation 禁 severity」管**单条 finding 怎么定级**；本条管**跨轮之间怎么记分与去重**——定级在前，记分在后。
- 提升层：工作流（扫描口径）/ 工具（报告契约）。触发词：only NEW findings、llm-unconfirmed、基线记分、重复计分、跨轮三态、换基线换量纲。

## 漏洞情报源要带「自动离线回退」，且模式库规模必须给出「类别数 × 模式数」双层粒度作为覆盖基准的分母（来源：api.github.com/repos/NVIDIA/SkillSpector/readme 53,566B 解码全文，2026-10-08 一手 curl 逐串命中 `71 vulnerability patterns` across `17 categories` / `SC4 | Known Vulnerable Dependencies | HIGH | Dependencies with known CVEs (live OSV.dev lookup)` / `real-time CVE data with automatic offline fallback`；与 §r435C 17 类漏洞清单 + Triage 五档处置 + SARIF 入 CI 互补——那条落"检出来怎么处置与怎么进 CI"，本条落"情报从哪来、断网时朝哪个方向失败、覆盖够不够怎么量"）
- **实证**：原文「**71 vulnerability patterns** across **17 categories**: prompt injection, data exfiltration, privilege escalation, supply chain, excessive agency, output handling, system prompt leakage, memory poisoning, tool misuse, rogue agent, anti-refusal, trigger abuse, dangerous code (AST), taint tracking, YARA signatures, MCP least privilege, and MCP tool poisoning」；「**Live vulnerability lookups**: SC4 queries [OSV.dev](https://osv.dev) for real-time CVE data with **automatic offline fallback**」；「**Multiple output formats**: Terminal, JSON, Markdown, and **SARIF** reports」；阶段与基线「Two-stage analysis: Fast static analysis + optional LLM semantic evaluation」「Baseline / false-positive suppression … so re-scans surface only *new* issues」。
- **判据**：① **依赖实时情报的检查必须显式声明离线时的方向**：SC4 命中 CVE 靠在线查询，官方明写"自动离线回退" ⇒ 联网检查的默认失败方向如果是"查不到=没有漏洞"，断网期间的扫描会静默降级成"全部安全"；正确写法是把"情报源不可用"作为可观测状态（与"扫过且无 CVE"区分）。② **模式库规模要分两层报（类别数 × 模式数）**：17 个类别是目录、71 个模式是条目 ⇒ 只报"覆盖 17 类"会让人以为只有 17 项检查；覆盖率的分母是模式数，归类方式由类别数决定，两者缺一都无法判断"这个扫描器是否够用"。③ **类别清单本身就是威胁面清单**：17 类里既有注入/外传/提权这类经典面，也有 memory poisoning、rogue agent、anti-refusal、trigger abuse、MCP tool poisoning 这类 agent 特有的面 ⇒ 审自己的技能库时，先拿这份清单对一遍"哪些面我根本没有检查项"。④ **两阶段（快速静态 + 可选语义）意味着第二阶段可缺席**：LLM 语义评估是 optional ⇒ 报告里必须标注本次是否跑了语义阶段，否则同一份结果可能是两种强度的产出。⑤ **与处置链串成完整闭环**：模式库（覆盖什么）→ 情报源（依赖是否已知有洞，含离线回退）→ 基线（只报新增）→ SARIF（进 CI）⇒ 任何一环缺席，扫描结论都只能当线索不能当裁决。
- **与既有能力分工**：r435C「17 类清单 + Triage 五档 + SARIF 入 CI」管**检出之后的处置与集成**；本条管**情报来源的失败方向与覆盖度的计量基准**。
- 提升层：工具（扫描器接入三要素）/ 治理（覆盖度分母）。触发词：71 模式 17 类别、模式库规模双层粒度、OSV.dev 实时 CVE、automatic offline fallback、离线回退方向、两阶段可选语义、类别清单即威胁面、覆盖度分母。

## 审查对象应是「带证据的发布物 + 可重跑的体检通道」而非源树：发布附带 release-manifest / postpublish-evidence / dependency-evidence（json+sha256）三资产 + Doctor 只读托管配置修复（来源：api.github.com/repos/openclaw/openclaw/releases，2026-10-08 一手 curl 逐串命中 `release-manifest`×12/`postpublish-evidence`×12/`dependency-evidence`×6/`sha256`×26；与 r423C「交付物验收而非源树」同轴，补证据文件命名集；r445A 落地）
- **实证**：openclaw v2026.10.1-beta.1 随发布附带 **release-manifest / postpublish-evidence / dependency-evidence（json+sha256 三件套资产）** + "Updates and Doctor"（serving-verdict 恢复、只读托管配置修复）；v2026.9.8 稳定版 "58 commits · 43 PRs · 21 contributors"。
- **判据**：① 验收一个技能/包，看的应是"它发布时带了哪些可验证证据"而不是"源码长什么样"；② 证据文件要有命名约定（manifest/evidence 分三类：发布清单、发布后证据、依赖证据）且带 sha256 可重算；③ 配套一个只读的"体检"通道（Doctor）能在不破坏托管配置前提下修复/恢复 verdict ⇒ 审查与自愈是两个伴生能力，缺一不可。
- **与既有能力分工**：r423C 管"验收对象是交付物不是源树"这一原则；本条补"交付物该带哪几类证据文件"的具体形态。
- 提升层：工具（发布证据链）/ 治理（验收口径）。触发词：release-manifest、postpublish-evidence、dependency-evidence、json+sha256 三件套、Doctor 只读托管修复、带证据的发布物、交付物验收。

## 软 404 识别法（等大小 200 = SPA 壳，真枚举走 robots→llms→sitemap→*.md）+ 安全审查可落地为「三档判定 + with/without A/B + evals.json 导入」的评测而非人审徽章（来源：skillhub.cn/install/skillhub.md（7,429B 壳对照）+ github.com/alibaba/skill-up README，2026-10-08 一手 curl 逐串命中 `rule_based`/`script`/`agent_judge`/`evals.json`/`Qoder`；r445B 落地）
- **实证**：① 软 404：skillhub.cn `/api/*` `/docs` `/version.json` 全为 ~7,429B 同形 SPA 壳（无 `__NEXT_DATA__`），真内容走 robots→llms.txt→sitemap→`*.md` 链；判定法：**等大小 200 = 壳信号**。② alibaba/skill-up：`eval.yaml` + `cases/*.yaml`、`schema_version: v1alpha1`、判定三档 `rule_based`/`script`/`agent_judge`、with/without-Skill A/B、Docker/OpenSandbox 供给、引擎含 **Qoder CLI**/Claude Code/Codex、可导入 `evals.json`、提供 GitHub Action。
- **判据**：① 抓取技能市场/文档时，必须区分"真 404"与"软 404（同形壳）"——后者会骗过"200 即有内容"的假设，curl 拿到的 7KB 壳不是真内容；② 安全审查不该只是贴"已审"徽章，而应是一套可跑的评测（三档判定 + A/B + 可导入既有 evals）；③ 与 r443C「评测产物落盘契约」互补——那条管 WB 自己怎么评测技能，本条管"上游平台把审查做成评测"的形态。
- **与既有能力分工**：r443C 管 WB 评测产物落盘契约；本条管"上游平台审查即评测"的可复用形态与站点抓取判活法。
- 提升层：工具（站点抓取判活）/ 工作流（审查即评测）。触发词：软404 等大小200、robots→llms→sitemap→md、rule_based script agent_judge、with/without A/B、evals.json 导入、审查可跑评测、skill-up。
## 「已审核 / Vetted」只是形容词：给不出方法学页的市场，其收录量与审核字样一律不计入信任权重，只作候选发现面（来源：skills.rest 688,475B + /llms.txt 2,533B + /sitemap.xml 9,664B + /docs 404（23,304B 软 404 壳），2026-10-09 一手 curl 逐串命中 `113,000+ vetted agent skills` / `Vetted. One-click install. 100% free.` / `contributed by official partners, verified authors, and the community`；r472B 落地）
- **实证**：① 三处自陈「审核」——llms.txt「**113,000+ vetted agent skills**」、首页标语「**Vetted.** One-click install. 100% free.」、贡献者说明「contributed by official partners, **verified authors**, and the community」；但对 `vetting 方法 / scanner / threshold / re-audit 节拍` 的语境逐串抽取，**全部零命中**（"verified" 只作为技能描述里的形容词出现，非平台方法学）。② **方法学页缺失**：`/docs` 返回 404 且附带 23,304B 软 404 壳 ⇒ 无任何方法学页可核对。③ 三通道安装：Claude Code = 详情页给出的安装命令；Claude.ai = 下载 **.zip** → 项目设置上传解压 → `/skill` 激活；API = 引用技能包 URL。④ sitemap 为**索引式**（含 `repos.xml`、`authors-0..3.xml` 等分片，`<loc>` 可枚举）⇒ 按仓轴与作者轴可静态枚举。**诚实边界**：Qoder 转述的 `npx skills add <owner>/<repo> --all -g -y` 在本轮实拉的三个文件内 **0 命中**，不予采信，留候选池待详情页复核。
- **判据**：① **「已审核」是结论不是证据**：凡只给形容词、给不出 **扫描器名单 + 判定阈值 + 复审节拍** 的，其收录量与「审核」字样**不计入信任权重**，只作候选发现面（与 r410C / r442-Q-B「认证是带再验证时钟的状态」「徽标 ≠ 安全」同轴；本条补的是**「方法学页缺失」这一可机检的负证据信号**）。② **机检路径固定**：探 `/docs`、`/methodology`、`/security` 是否 200 且有实质正文；软 404（等大壳页）按**未达**计，不得记为「有页面」——把壳页当正文是最典型的假阳性。③ **规模越大越要先验证方法学**：113,000 级自陈规模配零方法学出处 ⇒ 规模不构成可信度，反而放大误采信面（呼应 ssc 既有「标记率 ≠ 风险规模」）。④ **分发通道本身计入风险面**：zip 下载解压 + `/skill` 激活这类形态把人工复核点从安装流里移除 ⇒ 评信任时要把安装通道的默认参数一并看，凡是「免确认 / 全量」形态都应视为复核点被跳过的显式证据。⑤ **新站登记（建议入必须项，按低信任计数源处理）**：skills.rest = 第三方 Agent Skills 聚合注册表，自述 113,000+ / 10 个专业领域 / 三通道安装，可与 skills.sh、SkillsMP 构成**第三家独立计数源**，用于跨注册表同名技能扩散比对，但不得单独作为可信度依据。
- 提升层：可复用 Skill（市场准入判据）/ 工作流（信源分级）。触发词：自陈已审核、Vetted 无方法学、方法学页缺失、/docs 软 404、113,000 vetted、聚合注册表低信任计数源、skills.rest。

## 扫描覆盖的是「检查面」，执行面可被随包字节码缓存替换：扫描对象须含 __pycache__/.pyc 并与源码做行为一致性比对，且防御代价必须与检出率并列（来源：arxiv.org/abs/2610.10612（PyCache Trap）43,017B，2026-10-09 一手 curl 逐串命中 `Python may execute a bundled bytecode cache with different behavior` / `Across 100 skills and seven scanners, PyCache Trap achieves 94-100% attack success, with no semantic recognition of the cache-resident behavior` / `detects all 100 evaluated source-present cache substitutions and reaches 92.8% Recall at 10.0% FPR across five attack families and 200 benign skills`；r472B 落地）
- **实证**：① 缝隙定义「Existing skill scanners inspect documentation and visible source, but **Python may execute a bundled bytecode cache with different behavior**」；② 攻击构造 = 良性源码 + 被替换且被 loader 接受的缓存 + 任务相关调用，并用 **scanner-guided rewriting** 改调用措辞而保留缓存本体，把「包准入」与「对隐藏行为的识别」脱钩；③ 规模「Across **100 skills and seven scanners**, PyCache Trap achieves **94-100%** attack success, with **no semantic recognition** of the cache-resident behavior」；④ 防御 EAV（execution-aware validation）把被检查的指令 / 脚本 / import / 运行期工件连成 **typed execution graph**，「detects **all 100** evaluated source-present cache substitutions and reaches **92.8% Recall at 10.0% FPR** across five attack families and 200 benign skills」。
- **判据**：① **检查面 ≠ 执行面**：静态扫描默认只覆盖可见源码，运行时却可能加载随包字节码缓存 ⇒ 准入只看源码等于放行执行面（与 r445B / r448-Q-C 已落的「预编译字节码绕过」同机制；本条补的是**一手规模数值**与**防御侧代价**）。② **不是个别扫描器失手，是全行业面失效**：100 技能 × 7 扫描器 94–100% ASR、对缓存内行为零语义识别 ⇒ 单换扫描器不构成缓解。③ **防御的误报率必须与检出率并列报告**：EAV 100/100 检出的代价是 **92.8% Recall @ 10.0% FPR**（200 个良性里约 20 个误报）⇒ 只报 100/100 的防御方案不可采信（沿用 ssc 既有「防御代价须与攻击成功率并列报告」纪律）。④ **可操作增量**：扫描对象清单必须显式包含 `__pycache__/` 与 `*.pyc`，并与源码做**行为一致性比对**（而非仅存在性检查 / 仅源码扫描）。⑤ **措辞层面的相似性比对无效**：攻击靠 scanner-guided rewriting 改措辞保留工件本体 ⇒ 检测必须落到工件级（字节码/代码对象归一化后比对），不能落在文本级。
- 提升层：可复用 Skill（技能扫描与准入）/ 工具（执行面校验）。触发词：PyCache Trap、字节码缓存替换、检查面不等于执行面、__pycache__ 扫描、行为一致性比对、92.8% Recall 10.0% FPR、EAV typed execution graph。

## 技能「选择阶段」存在不需要任何注入痕迹的攻击面：用户提示与技能描述单看都良性，靠语义关系塑形即可把选择率从 15.2% 推到 63.5%，而人工评审只拦住 2.9%、五个 LLM 检查器平均放行 82.9%（来源：arxiv.org/abs/2609.02035（ISM）42,386B，2026-10-09 一手 curl HTTP 200 逐串命中 `increases the average target-selection rate (TSR) from 15.2% to 63.5%` / `73.5% TSR, only 9.8 percentage points below Explicit Steering` / `Human reviewers block ISM in only 2.9% of judgments, versus 91.4% for Explicit Steering` / `five LLM-based inspectors pass ISM at an average rate of 82.9%, versus 37.4%`）
- **实证**：① 攻击定义「even when the user prompt and skill description appear benign **in isolation**, their **semantic relationship** can still be strategically shaped to favor an attacker-chosen skill」；② 三阶段策略「broaden semantic coverage, strengthen target distinctiveness, and preserve natural prompt wording」；③ 跨度「Across four task domains and eight selector models, ISM increases the average TSR from **15.2%** to **63.5%**」；④ 与显式操纵的对照「In a matched comparison, ISM achieves a **73.5%** TSR, **only 9.8 percentage points below** Explicit Steering」；⑤ **人审几乎无效**「Human reviewers block ISM in only **2.9%** of judgments, versus **91.4%** for Explicit Steering」；⑥ **机审同样失效且方向相反**「five LLM-based inspectors **pass ISM at an average rate of 82.9%**, versus **37.4%** for Explicit Steering」。
- **判据**：① **"内容干净"不构成安全证据，因为被操纵的是关系不是内容**：提示与描述各自过审、组合起来仍能定向 ⇒ 检查必须落到"这个技能为什么会被选中"，逐件审查对这类攻击结构性盲。② **显式与隐式的拦截率差 31 倍（91.4% vs 2.9%），说明我们现有的"看一眼内容"式人审只对显式攻击有效**：把人审写进控制项时，必须声明它只对哪一类攻击起效，否则等于在控制矩阵里记了一个 2.9% 的措施却按 91.4% 上报。③ **LLM 检查器不是人审的替代品，是同一种盲的另一种形态**：对显式操纵放行 37.4%、对隐式放行 82.9% ⇒ 隐式攻击对机器评审比对人更宽松；加 LLM 检查器不能补人审的洞，两者在 ISM 上同向失效。④ **隐式攻击的代价只有 9.8pp，防御方却要付出"看起来正常"的全部伪装成本**：有效性损失这么小 ⇒ 不能假设攻击者会为了绕过而留下异常措辞；"读起来自然"不是良性信号。⑤ **选择阶段必须引入与描述无关的第二路判据**：既然描述可被塑形，那么最终选谁就不能只由描述与请求的语义匹配度决定 ⇒ 需要不可由描述单独影响的锚（安装位置 / 显式白名单 / 来源信任档），这与 r472A「安装位置决定谁跑」互补——那条是实测事实，本条给了"为什么必须这样"的攻击面证据。⑥ **报告口径**：任何"已通过人工审核"的声明，只在其针对显式攻击时成立；对隐式选择操纵，现行人工流程的实际拦截率是 2.9%。
- **与既有能力分工**：r439A「审批校验验签发者是否有权为本动作签发」管**授权链**；r437A「形态先验权限档」管**形态决定权限下限**；本条管**选择阶段这一前置入口**（授权与形态都还没生效之前，技能就已经可能被选中了）。
- 提升层：可复用 Skill（准入审查）/ 工具（选择面控制项）。触发词：ISM、Implicit Skill-Selection Manipulation、Semantic Matching、15.2% 到 63.5%、2.9% 人工拦截、82.9% LLM 放行、语义关系塑形、选择阶段攻击面、skill selection poisoning。

## 拦截项要分「可翻墙」与「不可翻墙」两档并显式标注；下架 ≠ 撤权（全文见 references/knowledge-base.md §下沉·skills-security-check·拦截分档）

## r485C · 目录「有无安全标记」要先问「扫不扫」：无标记有两种成因；多家扫描源可并列且允许结论冲突；第三方目录的限流窗口可能是「日」（来源：skillsmp.com/docs/api 503,097B + skillsmp.com 302,679B + www.skills.sh/anthropics/skills/pdf 122,581B，2026-10-10 r485C 一手 curl 实拉逐串命中 `We don't scan for malware (yet)` / `not a live ranking, quality certification, or safety review` / `DAILY_QUOTA_EXCEEDED`×3 / `X-RateLimit-Daily-Limit`×6 / `Gen Agent Trust Hub`×2 / `Socket`×2 / `Snyk`×2）

- **★「没有安全标记」有两种成因，须先分离**：SkillsMP FAQ 原文「**We don't scan for malware (yet).** This is community-driven content」+ 目录页自述「A maintained selection of public examples, **not a live ranking, quality certification, or safety review**」。判据：**在"目录不扫描"的前提下，无标记 = 未测评，不等于"通过了测评"**；采信一个目录的结论前，第一问必须是「该目录究竟扫不扫」，这是二值属性而非程度问题。与 §「已审核是结论不是证据」（r472B）互补：那条给的是**方法学页缺失**这一机检负证据，本条给的是**目录明示不扫描**的一手原文，二者互为佐证但证据形态不同。
- **★同一技能可并列多家扫描源，且允许结论冲突**：skills.sh 明细页同时列出三个独立扫描源（`Gen Agent Trust Hub` / `Socket` / `Snyk`）。判据：**"有徽章"不等于"全绿"**——装机判据应写成**逐源列结论**，而不是"有无 Security Verified"这一个布尔量；把多源结论折叠成单值会直接抹掉源间分歧。本轮**判级值（PASS/WARN）在 HTML 中 0 命中**（JS 渲染），故具体判级不入账，只入"多源并列"这一形态。
- **★第三方目录 API 的限流窗口可能是「日」不是「分」**：SkillsMP 返回 `X-RateLimit-Daily-Limit` / `X-RateLimit-Daily-Remaining`，错误码含 `DAILY_QUOTA_EXCEEDED`（429，与 `INVALID_OCCUPATION` / `INVALID_LANGUAGE` 同族机检枚举）。判据：**日配额耗尽后原地重试零收益**——退避策略须先判窗口类型（日/时/分），日配额须改调度到次日或换用缓存，不能套用分钟级指数退避；批量核验脚本要把剩余配额当输入，而不是把 429 当瞬时抖动。
- 提升层：工作流 / 工具。触发词：目录不扫描、无标记两种成因、not a live ranking、多源并列、逐源列结论、徽章不等于全绿、日配额、DAILY_QUOTA_EXCEEDED、X-RateLimit-Daily、限流窗口类型。

## r488C · 多源审计「可并列但不可归并」：三家词表不同构，折叠成单一 verdict 必然失真；同时更正 r485C 的通道结论——不入账的是「统一判级」而非「判级值」（来源：www.skills.sh/audits 387,367B，2026-10-10 一手 curl 逐串命中 `Combined security audit results from Gen Agent Trust Hub, Socket, and Snyk.` 与 `Safe`×23 / `Low Risk`×17 / `Med Risk`×12 / `alerts`×52 / `Pending`×72 / `Socket`×29 / `Snyk`×29；r488C 落地）
- **实证**：skills.sh `/audits` 页自述聚合三家来源（Gen Agent Trust Hub / Socket / Snyk），但三家的输出**形态互不相同**：Gen 给形容词级（`Safe` / `Low Risk` / `Med Risk`），Socket 给计数级（`N alerts`），Snyk 给分级级；另有独立的 `Pending` 未扫描态（72 次）。**字面串 `PASS` / `WARN` 在该站确实不存在。**
- **判据**：① **不同词表不可比，聚合只能并列不能归并**：形容词级与计数级之间没有映射函数 ⇒ 把三源折成一个"是否通过"会丢掉"Snyk 说中风险但 Socket 说零告警"这类最关键的分歧；报告须**逐源保留原形态**，并允许并列冲突。② **`Pending` 是第三态，既非通过也非失败**：把它填成"通过"（默认）会虚增覆盖率，填成"失败"会污染阳性率 ⇒ 未扫描必须单独成态并在覆盖率分母中显式扣除。③ **更正 r485C**：r485C 因「`PASS/WARN` 0 命中（JS 渲染）」判「判级值不入账」——本轮一手核验表明 raw HTML **机读可得**（387KB 全文含三源异构词表），**真正的结论应是"统一判级不可入账，各源原值可入账"**；把"没有统一词表"误记成"取不到判级"，属于把取证失败与对象性质混为一谈。④ **"多源并列"的实现前提是有源可列**：r485C 只立了"允许冲突"的形态，本条补齐"各源值怎么取、Pending 怎么算" ⇒ 二者合起来才是可用的多源聚合判据。
- **与既有能力分工**：r485C「目录扫不扫是二值属性」管**该不该采信这个目录**；r486C「阳性率最高的扫描器在确证恶意上最低」管**多源之间怎么比强弱**；本条管**多源结论以什么形态同时呈现**。
- 提升层：可复用 Skill（安全校验）/ 工具（多源聚合）。触发词：Combined security audit results、Safe / Low Risk / Med Risk、alerts 计数、Pending 第三态、词表不同构不可归并、逐源列原形态、判级值可入账但统一判级不可。

## r488C-2 · 校验「字段存在」是假信号：有声明字段但值为空、或有值但实现里没有比对，都必须判为未校验；三种失效形态要分态报告（来源：skillhub.cn/install/install.sh 483B（真 bash，非 SPA 壳），2026-10-10 一手 curl 全文核验：`KIT_URL="https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/latest.tar.gz"` 后直接 `curl -fsSL "$KIT_URL"` + `tar -xzf` + `bash "$INSTALLER" "$@"`，全文 `sha256sum|shasum|openssl dgst` **0 命中**；r488C 落地）
- **实证**：SkillHub 安装脚本从对象存储直拉 `latest.tar.gz`，解包后立即 `bash` 执行，**整段脚本不含任何摘要校验**。即"从网络取可执行包并运行"这条链路上没有任何完整性闸门。
- **判据**：① **声明 ≠ 实现，校验判据必须是「有值 且 有比对发生」**：把"响应里有 sha256 字段"当成"已校验"，是把接口契约误当成运行时行为 ⇒ 校验结论只能下在**实际比对动作**上。② **三种失效形态必须分态，不能合并成"未校验"**：`字段缺失`（契约面就没有）/ `字段存在但为空`（契约面有、供给侧没填）/ `有值但实现无比对`（声称校验、代码里没做）⇒ 三者的修复责任方分别是 契约设计者 / 供给方 / 实现方，合并记账会找错人。③ **"文档化了校验"本身就是风险线索**：文档与实现不一致时，文档会给人虚假安全感 ⇒ 审计时要专门做"文档声明 vs 代码行为"的一致性核对，而不是只读文档。④ **安装链路上拉远端包直接执行是最高危形态**：无校验 + 无签名 + 直接 `bash` ⇒ 安装类脚本的审查优先级应高于普通技能包，因为它执行在用户机器上且绕过技能扫描面。⑤ **诚实边界**：本轮另探 `skillhub.cn/install/version.json` 与 `/version.json`、`/api/version.json` 三路径**均返回 7,429B SPA 壳**，未复现上游所述 `{"sha256":""}` 空串原文 ⇒ **空串那一条不入账**，只落本条可由 install.sh 一手证实的"有声明无实现"形态。
- **与既有能力分工**：r487/r485C「缺签名文件时回退保留旧版」管**签名文件缺失时的处置**；本条管**签名/摘要字段存在但没被真正使用**。
- 提升层：可复用 Skill（安全校验）/ 工具（安装链路审查）。触发词：sha256 字段存在但未比对、声明与实现一致性核对、latest.tar.gz 无校验、安装脚本直拉远端包执行、三种校验失效形态、空串不入账。


## r490C · 自报风险分级是「闭域单选」：没选与多选必须落成机检失败态，不能当缺失字段宽容处理（来源：docs.dify.ai/llms-full.txt 2,695,981B，2026-10-10 r490C 一手 curl 实拉逐串命中 `Select exactly one of **Low risk**, **Medium risk**, or **High risk**. The repository applies a matching \`risk:*\` label. Selecting none or multiple levels produces \`risk: missing\` and a bot comment.`）
- **判据**：① **分级是「恰好一个」的闭域约束，不是可选字段** ⇒ 安全分级一旦设成可选项，就等价于允许无分级发布。② **「没选」与「多选」落到同一个失败标签 `risk: missing`** ⇒ 失败态不区分方向，排障时必须回查原始选择而不是只看结果标签。③ **判据由外部机检闭环**：作者自报不能自证，须有独立的机器人/校验器回写结论 ⇒ 自报分级只有配上机检才有意义。④ **与既有「风险档位由可能性 × 影响决定」互补**：那条管**怎么定级**，本条管**定级这个动作本身的合规形态**（必须选、只能选一个、没选即失败）。
- **与既有能力分工**：r405「风险档位算术与判定者分离」管定级方法；本条管分级的存在性与唯一性校验。
- 提升层：可复用 Skill（安全审查清单）/ 工作流（发布门禁）。触发词：风险分级闭域单选、Selecting none or multiple、risk: missing、自报分级机检闭环、分级是必填不是可选。


## r492C · 安装器「假成功」是三层结构的复合故障：计数变量活不到汇总行、落盘结果被硬编码成功吞掉、汇总口径与成功无关审计时必须逐层各验一次（来源：www.modelscope.cn/skills/install.sh 27,039B + github.com/prompt-security/clawsec README 8,314B，2026-10-10 r492C 一手 curl 实拉）
- **判据（安装侧三层）**：① **pipe-into-while 的子 shell 使计数失效**：`echo "$COLLECTION_SKILLS" | while read -r skill` 循环体里的 `success_count=$((success_count + 1))` / `fail_count=$((fail_count + 1))` 全部发生在子 shell，外部的 `local fail_count=0` 永远保持初值 ⇒ **计数点与汇总点不在同一进程 = 计数必然丢失**，审计安装器先看 while 是不是被管道喂的。② **结果位被硬编码覆盖**：复制/提取函数末尾直接 `return 0`，且调用方 `install_single_skill` 末尾亦 `return 0`，中间的 `cp -r` 失败既不检查返回码也不被 set -e 捕获 ⇒ 落盘残缺不影响返回_success_。③ **汇总口径与成功无关**：最终 `print_success "共安装 $total_count 个 Skills"`，而 `total_count` 来自 `echo "$COLLECTION_SKILLS" | wc -l`（清单条目数）⇒ 即使全部失败也报「共安装 N 个」，且用绿框 finish 态呈现。④ **三层可分别单独成立**：只要修好计数而不修 return 0，报告依旧假；只修 return 0 而计数仍丢，报告依旧假 ⇒ 判据要**逐计数点**写，不能整体判定"这个安装器可不可信"。
- **判据（门禁侧两段）**：⑤ **clawsec 把供应链门禁拆成先验/后验两段**：装载前校验签名与 checksum manifest（`Verifies the advisory feed and checksum manifest before matching published risk against installed skills`），装载后做 configuration drift 基线比对（`audit agent environments`、`Gives platform-specific skills baselines for critical files, configuration, attestations, and release artifacts`），破坏性动作另过 approval-gate（`approval-gate risky installs`）⇒ **「装时干净」不豁免「装后漂移」**，二者是时间轴的两半，只做一半等于只堵一头。⑥ **覆盖范围要显式声明**：clawsec 明示覆盖 OpenClaw / NanoClaw / Hermes / Picoclaw 四个 runtime ⇒ 门禁的适用范围必须写明目标面，避免「装了就有保护」的错觉。
- **与既有能力分工**：r490C「自报分级须外部机检闭环」管**元数据真不真**；本条管**安装动作本身的成败信号真不真**。
- 提升层：可复用 Skill（安装器与装载审计）/ 工作流（供应链门禁时间轴）。触发词：假成功、pipe-into-while、fail_count 丢失、return 0 吞失败、wc -l 当成功数、checksum manifest 先验、configuration drift 后验、approval-gate。

## r495C · 引用他方「校验结论」前必须实证三件事：取值域是否含「无法判断」、位点是前置还是终身、失败分支是 fail-open 还是 fail-closed（来源：cloudcache.tencent-cloud.com/qcloud/tea/app/skillhub/assets/skill-hub.oq3neru1.js 3,748,192B，2026-10-10 r495C 一手 curl 实拉逐串命中 `Ew={fail:"Pay Skill 改造检查未通过",partial:"Pay Skill 改造部分通过",unknown:"Pay Skill 改造无法判断",pass:"Pay Skill 改造检查通过"}` / `Ij={fail:"支付宝付费改造检查未通过",…unknown:"支付宝付费改造无法判断",…}` / `if("pass"===s.compliance)return void(await xe());re(s),J(!1)}catch(q4){console.warn("[X402 precheck] 检查失败，跳过并直接提交：",q4),await xe()}` / `"pass"!==s.compliance?ne(s):doSubmit()` / `precheck-alipay` / `此密钥明文仅展示一次,关闭后将无法再次查看完整密钥` / `RSA 2048 私钥（PEM 格式）…**仅展示一次，SkillHub 不存储**`）
- **判据**：① **取值域要数到第四态**：本例 `compliance` 是 `fail/partial/unknown/pass` 四值，`unknown` 的文案是「无法判断」——它既不是待定（Pending）也不是错误（Error），而是**判定能力缺失**；把四值当二值（通过/不通过）用，会把 unknown 吞成 pass 或 fail 中的一边。② **位点是「提交前置」不代表终身保证**：校验挂在 `POST /api/v1/community/skills/precheck-alipay`（multipart 直传 `file` 而非按 slug 引用）⇒ 校验对象是**当时上传的那个包**，包内容此后变更不在其覆盖范围；引用该结论时要写明「对哪一次提交有效」。③ **接口自身失败时是 fail-open**：三个调用点的 catch 分支原文都是「检查失败，跳过并直接提交」并直接执行提交 ⇒ **「有校验」不等于「不通过就拦下」**，只有当次返回非 pass 才弹窗拦截；审计必须单独看失败分支，不能只看有没有校验接口。④ **非 pass 与接口异常是两条完全不同的路径**：`"pass"!==s.compliance` 走提示弹窗，`catch` 走静默放行 ⇒ 同一个"没通过"在两种成因下结果相反。
- **验真责任外迁的识别法（同轮第二证）**：`content_hash` 有可复算的规范化算法，签名态分 `{kind:"signed"}` 与 `{kind:"unsigned",contentHash}`，但 RSA 2048 私钥官方明写「**仅展示一次，SkillHub 不存储**」，验签说明只存在于 `/docs/verify-signature` 文档层 ⇒ **提供方自签 + 平台不托管私钥 = 没有第三方验证器，验真责任 100% 落在消费侧**；判据：**看到签名先问"谁能验"——平台不持私钥即无人代验，消费方须自行实现规范化重算**，不能因为"有签名字段"就当成已验证。
- **与既有能力分工**：r488C「字段存在是假信号（缺失/空值/有值无实现三态）」管**校验声明本身**；r490C「自报分级是闭域单选」管**分级怎么填**；本条管**引用外部校验结论前要验什么**。
- 提升层：工具（第三方结论引用前校验）/ 工作流（上架门禁）。触发词：compliance 四态、unknown 是无法判断、precheck-alipay、跳过并直接提交、fail-open 门禁、前置校验非终身、私钥不存储即无第三方验证器、content_hash 规范化重算。

## 「未列出」不是访问控制；且打包结果与源目录不是同一集合，审计要以包内实际内容为准（来源：skills.sh/docs/packs 45,129B，2026-10-11 r511B 一手 curl 200 实拉；逐串命中 `Packs are unlisted, not access-controlled` / `larger than 2 MB` / `Only skills that changed are re-downloaded`）
- **实证**：官方原文三点——①可见性「**Packs are unlisted, not access-controlled**: anyone with the pack URL can view and install it.」；②构建侧静默跳过「skips invalid skill files and omits binary files or individual files **larger than 2 MB**」；③更新侧增量「**Only skills that changed are re-downloaded**」。
- **判据**：① **把"不进搜索/未列目录"当私密性是错的**——未列出只减少发现路径、不减少可达性，拿到 URL 即可安装 ⇒ 任何「我没公开所以安全」的自证都不成立，含密钥的分发物必须假设已公开。② **打包结果是源目录的真子集且是静默裁剪的**：非法文件与超限文件被略过而不报错 ⇒ 审计对象必须是包内实际内容（解包后清点），不能拿源目录清单当交付清单。③ **增量更新使"本地没变"不等于"远端没变"**：只有变化项被重下 ⇒ 校验覆盖面要包含"本轮未重下的部分"，否则陈旧的本地副本会长期冒充最新。
- 提升层：可复用 Skill（分发与可见性语义）/ 工作流（交付审计）。触发词：unlisted not access-controlled、larger than 2 MB omitted、only skills that changed re-downloaded。

## 扫描器自述的规则数不能当门禁阈值；摄取上限须 fail-closed；基线抑制不能退化成永久豁免（来源：api.github.com/repos/NVIDIA/SkillSpector/contents/README.md 54,171B，2026-10-11 r511C 一手 curl 200 实拉 + `Accept: application/vnd.github.raw+json`；逐串命中 `71 vulnerability patterns across 17 categories` / `fails closed with an IngestLimitExceededError` / `MAX_FILE_BYTES` / `drift-tolerant glob rules` / `evidence-bound` / `--show-suppressed`）
- **实证**：官方原文四点——①自述口径「**71 vulnerability patterns** across **17 categories**: prompt injection, data exfiltration, privilege escalation, supply chain, excessive agency, output handling, system prompt override …」；②摄取上限「A breach of either ingest cap **fails closed** with an `IngestLimitExceededError`」，且「the per-file 1 MB analysis cap (`MAX_FILE_BYTES`) is a **separate, downstream limit**: it bounds what individual analyzers will read out of an **already-ingested** directory」；③基线可漂移「A baseline can also use **drift-tolerant glob rules** (by rule id, file path, or message)」；④基线的失效条件「**Exact fingerprint baselines are evidence-bound**: changing the scanned source or **SkillSpector version** keeps the finding **active until it is reviewed again**」，复核开关 `--show-suppressed`。
- **判据**：① **门禁阈值不能按扫描器自述的规则/类别数设**——自述是文档口径、实现是代码口径，两者会漂移（本例自述同时给「71 patterns」与「17 categories」两套计数）；阈值要按自己实测的命中分布定并周期重算。② **摄取超限必须 fail-closed**：直接抛错而不是截断；且「摄取上限」与「单文件分析上限」是**下游两道不同的闸**（`MAX_FILE_BYTES` 只约束已摄取目录内单个分析器读多少），超限事件必须可见——截断式降级等于静默少检。③ **基线抑制不能变成永久豁免**：抑制项可按 rule id / 路径 / 消息做漂移容忍，但源内容或扫描器版本一变，抑制自动失效并回到待复核；且必须能用 `--show-suppressed` 复核被抑制项，否则「抑制即消失」会形成无人察觉的覆盖盲区。
- 提升层：工具 / 可复用 Skill（扫描治理）。触发词：fails closed、IngestLimitExceededError、MAX_FILE_BYTES 下游限、drift-tolerant baseline、evidence-bound、--show-suppressed。

## 挂载/路径类配置必须过「二次校验」，且「省略访问模式」不等于只读（来源：docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated.md 9,792B，2026-10-11 r513A 一手 curl 200 实拉逐串命中 `pierces` / `validates bind sources twice` / `Symlink-parent escapes do not bypass blocked-path or allowed-root checks` / `Default is read-write if you omit the mode` / `effectively hands host control to the sandbox`）
- **判据**：① 路径类校验只做一次不够——先对**归一化源路径**校验，再解析到**最深存在祖先**后**再校验一次**，符号链接父目录逃逸因此无法绕过；不存在的叶子路径也要安全判定（`alias-out/new-file` 经符号链接父目录解析到阻断路径时整条挂载被拒）。② 挂载模式省略时默认是**读写**，安全审查里「未声明」一律按 rw 判，只有显式 `:ro` 才算只读。③ 任何把宿主控制面挂进沙箱的条目（`/var/run/docker.sock`）要单独点名——它等于把宿主控制权交出去。④ `workspaceAccess` 与 bind 模式是两套独立开关，不能互相代偿。
- 提升层：工具 / 工作流（沙箱与挂载审查）。触发词：binds、:ro、二次校验、最深存在祖先、符号链接逃逸、docker.sock、workspaceAccess。

## 策略一致性检查要分「无效 / 缺项 / 更弱」三态，另加「不可观测」第四态：只报"不一致"会掩盖失败方向（来源：docs.openclaw.ai/cli/policy/findings.md 18,932B，2026-10-11 r513B 一手 curl 200 实拉逐串命中 `policy/policy-conformance-invalid` / `policy/policy-conformance-missing` / `policy/policy-conformance-weaker` / `policy/sandbox-container-posture-unobservable` / `cannot observe it`）
- **判据**：① 比对基线与被检配置至少要三态：**语法无效**（invalid，比不了）、**缺项**（missing，规则不在）、**值更弱**（weaker，在但放宽了）——三者修复动作完全不同，压成"不一致"会造成误修。② 还要有第四态 **unobservable**：规则已启用但当前后端**无法观测**该姿态 ⇒ 「规则生效」不等于「规则可被验证」，验收时要问"这条规则在我这个后端上有没有观测点"。③ 发现项用 `域/条件` 命名空间编码（`policy/mcp-unapproved-server`、`policy/tools-required-deny-missing`…），让"缺 deny"与"有 deny 但被绕过"成为两个可区分的 ID，而不是同一条泛化结论。
- 提升层：工具 / 工作流（合规与配置审计）。触发词：invalid/missing/weaker 三态、unobservable、发现项命名空间、策略一致性。

## 技能装载的校验必须分「警告放行」与「跳过」两档，且诊断要可呈现：description 缺失是硬失败，外观问题是软失败（来源：agentskills.io/client-implementation/adding-skills-support.md 20,357B，2026-10-11 r513C 一手 curl 200 实拉逐串命中 `Lenient validation` / `warn, load anyway`×2 / `skip the skill`×2 / `64 characters` / `don't block skill loading on cosmetic issues` / `Record diagnostics`）
- **判据**：① 四类问题的处置**不是同一档**：name 与父目录名不匹配 → 警告但加载；name 超 64 字符 → 警告但加载；**description 缺失或为空 → 跳过该技能并记错**（description 是渐进式披露的必要条件，没有它等于该技能不可发现）；YAML 完全不可解析 → 跳过并记错。② 安全审查里要把「软失败」与「硬失败」分开报：**外观问题不得阻断加载**，否则一次格式整改会连锁下线一批技能；但**不可发现 = 不存在**，description 缺失不能降级成警告。③ 诊断必须落到可呈现面（debug 命令 / 日志 / UI），「静默跳过」会让技能莫名消失且无人察觉。
- 提升层：工具 / 工作流（技能校验与审查）。触发词：Lenient validation、warn load anyway、skip the skill、description 缺失即跳过、诊断可呈现。
