---
name: ai-input-enhancement
description: >-
  WB 统一 AI 信息入口的总架构原则与输入路由：外部信息如何归一进 AI、如何判断价值、如何路由到正确 Skill、隐私与记忆边界。当用户要梳理「统一输入/信息入口/输入增强/WeChatBridge/输入路由/价值判断/聊天增强/任务提取」或 WB 输入层架构，或要新增输入类能力时应用。本技能是编排/元层原则，不替代各引用 Skill 的执行细节，重叠>60% 一律引用不重复建。触发词：统一输入、信息入口、输入增强、WeChatBridge、输入路由、价值判断、聊天增强、任务提取、记忆管理、开源学习、Fast/Deep 执行。
version: 1.1.0
compatibility: WorkBuddy；引用 media/ engineering/ defaults/ agent/ system/ rules/ 下现有 skill（不重复建）
module: TI
modules: TI,CI
---

# AI 输入入口增强系统（WeChatBridge 融合终版）

> 本技能为**编排/元层原则**，非执行手册，能力由引用 Skill 提供。总入口见 `00_总目录_所有AI入口.md`。

## 边界（先读）
本技能定义「入口如何归一、何时路由」，**能力由引用 Skill 提供**，不是执行手册。它不是 `wb-context-compressor` 的副本，也不是 `wb-spec-driven` 的路由表——价值判断细节看 context-compressor，流程/路由细节看 spec-driven，验证看 artifact-verification。

## STOP / WAIT / PROCEED
| 状态 | 动作 |
|---|---|
| 已有 Skill 覆盖该能力 | **STOP**——直接引用，不重复写 |
| 要落地新输入能力 | **WAIT**——先查现有 skill 重叠；>60% 则引用不建 |
| 确属独特点 | **PROCEED**——落到对应 skill 或本技能独点段 |

## 目标
将 WB 打造成统一 AI 信息入口：
```
信息获取 → 内容理解 → 价值判断 → 任务提取 → 调用 Skill/Agent → 执行验证 → 经验沉淀
```
少重复操作，提 AI 使用效率。

---

# 一、总原则

## 1. 不新增重复 Skill
新输入能力先查已有：消息处理 / Windows 操控 / 文件处理 / 浏览器 / 记忆管理 / 自动化 / 执行验证 类 skill。
- 已有能完成 → 直接复用
- 已有不足 → 合并增强
- **禁止**：为单一功能建重复 skill、为数量增无价值 skill

# 二、统一 AI 输入层（AI Input Layer）
所有外部信息先经统一输入层，归一为 `{ type, source, raw, meta }`。

## 文本输入
来源：微信复制文本 / QQ 消息 / 浏览器文本 / 网页内容 / 剪贴板 / 文档文字。直入处理流。

## 图片输入
来源：微信聊天截图 / 图片资料 / 页面截图 / 图片文件。
```
图片识别 → 文字提取 → 语义理解 → 任务分析
```
实现见 `media/image-processor`、`media/wb-media-forensics`。

## 文件输入
支持 PDF / Word / Excel / 图片 / 压缩文件。
```
读取 → 分析 → 总结 → 提取行动项
```
实现见 `engineering/wb-doc-file-intel`、腾讯文档系（`tencent-docs` / `tencent-docx`）；浏览器来源见 `system/browser-automation`。

# 三、统一信息处理流程
```
输入信息 → 识别来源 → 识别类型 → 提取核心内容 → 补充上下文
→ 判断用户目标 → 选择对应 Skill/Agent → 执行 → 验证结果 → 记录有效经验
```
流程骨架 `engineering/wb-spec-driven`；执行纪律 `engineering/wb-execute-discipline`（点名目标须真实执行）；验证 `engineering/wb-artifact-verification`。

# 四、信息价值判断
收到信息先判价值，筛选机制见 `defaults/wb-context-compressor`。

## 高价值（进任务管理或记忆）
工作任务 / 重要沟通 / 长期偏好 / 决策依据 / 可复用经验 / 已验证方案。

## 中价值（当前任务用，不长期存）
临时资料 / 一次性分析 / 普通咨询。

## 低价值（不保存，避免污染记忆）
普通闲聊 / 重复信息 / 无后续价值通知。

# 五、聊天信息增强能力
针对微信、QQ 等。

## 1. 自动理解上下文
分析：沟通对象 / 当前主题 / 前后关系 / 用户目的 / 历史相关信息 → 输出当前情况、核心问题、建议方案。
通道：`system/wechat-desktop-claw-automatic-control__skillhub`（只发不读）、`system/workbuddy-claw-wechat-send`；对外发消息见 `rules/04_wecom企业微信`（默认先确认，企微直发原样透传）。

## 2. 回复辅助
生成时考虑：联系人关系 / 历史交流方式 / 当前语境 / 用户表达习惯。
```
普通消息：分析 → 生成建议
重要消息：生成 → 检查 → 用户确认 → 发送
```
**禁止**：未经确认自动发高风险消息。

# 六、自动任务提取
聊天/文件/网页分析后自动提取：
```
任务：
负责人：
时间：
优先级：
下一步行动：
```
例：原消息「月底前提交方案」→ 任务：提交方案 / 时间：月底前 / 下一步：整理资料并生成初稿。
结构化落地见 `engineering/to-tickets`。

# 七、AI 输入路由系统
```
所有输入 → AI Input Router → 判断需求 → 调用对应能力
```
调用顺序：① 专用 Skill ② 已有 Workflow ③ 通用能力 ④ 新建能力。
**禁止**：多 Skill 同时抢占任务。未匹配走 `wb-spec-driven` 的显式默认路由（不静默丢弃）；跨 agent 交接见 `agent/agent-guild`。

# 八、隐私安全规则
默认：不读微信数据库 / 不扫无关聊天 / 不取未授权信息 / 只处理用户主动提供内容。
高风险操作（自动发消息 / 删文件 / 改重要数据 / 外部账号操作 / 权限变化）**必须**：执行前确认 → 执行中检查 → 执行后验证。
细则：敏感输入走 `wb-artifact-verification` 护栏四模式（block/redact/retry/require-approval）+ secret/PII 检测器；密钥/token 不提交（`rules/06`）；用户真实文件优先回收站。

# 九、记忆管理规则
只存长期有价值信息：用户长期偏好 / 常用工作方式 / 有效方案 / 已验证流程 / 重要经验。
不存：临时聊天 / 一次性信息 / 无价值内容。目标：提未来效率，避免垃圾记忆。
规范见 `rules/07_记忆管理规则`；共学双写 `memory/co-learn/<工具名>/`，命名 `YYYY-MM-DD_主题.md`。

# 十、开源项目学习机制
学：微信 AI 工具 / Agent / Skill / MCP 项目。流程：
```
发现 → 分析核心能力 → 查已有体系重复 → 删无用部分 → 改造成 WB 能力 → 合并进现有系统
```
**禁止**：直接复制项目 / 引复杂无用功能 / 增重复 skill。调度见自动化 `070cce0c`；信源含腾讯 SkillHub `skillhub.cn/skills?sortBy=score` 分数面。

# 十一、执行标准
**思考策略三档（2026-10-13 AI-1 由用户「元认知」提案落地）**：先判档位再动手；档位由「目标清楚度 × 风险 × 不确定性 × 步骤数」定，不由习惯定。

| 档 | 进入条件（满足即进入） | 必做 | 禁止 |
|---|---|---|---|
| T1 直接答 | 目标清楚 + 对象明确 + 风险低 + 步骤少 + 结果易判（对齐可靠性核心 §一 快速通道） | 识别目标→执行→看结果→交付；先报步数 | 复杂状态管理 / 假设账本 / 预演 / 完整 Self-Audit |
| T2 拆解验证 | 多步 / 跨会话 / 不确定 / 失败≥2 次 / 需自主跑到交付 | `wb-spec-driven` 立规约→计划-实现-检查→独立验证；失败≥2 次必根因 | 边跑边改目标 / 把失败当空结果 |
| T3 多视角复核 | 高风险 / 高价值 / 不可逆 / L2 权限级 / 结果无法自验 | T2 全套 + 引入他者（第二模型 / 子 agent / 用户抽查）+ 外部信号验证 | 用自反思代替外部验证；为形式完整启动大流程 |

**走偏换法触发器**（出现即回 T1 重判档位或换方法）：连续同类失败 / 当前动作不再服务 Goal / 证据与假设冲突 / 预算耗尽仍未降低关键不确定性。换路阶梯见 `wb-execute-discipline` §二。
**档位是动态的**：升级清单复用 `00_WBAgent可靠性核心.md` §一（目标变化 / 状态异常 / 结果不确定 / 失败 / 影响扩大 / 批量 / 不可逆 / 复杂决策 / 无法可靠验证），不另造框架。
执行要求：判断需求 → 制定方案 → 调用能力 → 执行 → 验证 → 总结。
默认三件套常开：`wb-ponytail` / `wb-max-token-saver` / `wb-context-compressor`。

# 十二、最终目标
让 WB 从「回答问题的 AI」升级为「理解信息、整理任务、辅助决策、推动执行的个人 AI 系统」。
核心：少而精 · 优先复用 · 快速执行 · 结果可验证 · 持续优化。

# 十三、输入对齐按关系结构，不按表面特征（2026-11-14 r741A 实拉）

> 落在 §三「统一信息处理流程」与 §七「AI 输入路由系统」之间：本节的判据决定「提取核心内容」之后按什么把输入对齐到已有能力。与 `engineering/wb-instruction-prior`（输入本身缺不缺、矛盾不矛盾）、`meta/ti-critical-reasoning`（论证有效性/健全性）分工，不重做那两层的检查。

### 13.1 路由匹配的单位是关系骨架，不是词面与来源
- **原文**（Gentner 1983 结构映射理论，经 Cognition 2018 原文转述）：「analogical comparison is geared towards finding **a structurally consistent set of one-to-one correspondences that maximizes the common relational structure**」；「people implicitly prefer structurally consistent alignments in which lower-order matches are connected by higher-order relational matches (**the systematicity principle**)」。表面属性不进入对齐：军队的规模、堡垒的石墙在肿瘤问题里没有对应物，也不要求有。
- **判据**：`{ type, source, raw, meta }` 归一后，路由应比对「目标—约束—动作—依赖」的关系骨架。两条输入词面相近、来源相同但关系骨架不同 → 分开路由；表面完全不同但骨架相同 → 共用一条处理链。判定表写「哪些关系必须一一对应」，不写「看起来像哪类历史任务」。
- **反例自查**：拿一条「同名但换了因果结构」的输入去撞现有路由，若被送进同一 Skill，说明路由实际是按表面特征走的。

### 13.2 单一范例不产生迁移，比较才产出可迁移结构
- **原文**（Gick & Holyoak 1980/1983 辐射问题）：冷解约 **10%**；先读堡垒故事约 **30%**；给「用得上那个故事」的提示约 **75%**。两个案例并排比较后自发迁移 **45%**，只读一个案例 **21%**，两案例加图示达 **92%**；「This is why a single worked example transfers poorly while two contrasting examples transfer well: **the comparison is what strips away surface detail and leaves the portable structure**」。
- **判据**：技能/路由表里的示例至少成对给出——表面相异、骨架相同，并显式写出共同关系（schema induction）。只放一个 worked example 的路由规则，遇到长相不同的新输入就会失效；「用户看过一次示例」不等于「已具备该类输入的处理能力」。
- **输入增强的落点**：本节定义的增强不是润色措辞，而是把输入重述成带关系骨架的结构化问题，使它能对齐到已有能力；措辞改写不产生这项能力。

### 13.3 检索门槛与映射门槛要分开记账
- **原文**：「**Spontaneous transfer depends on surface similarity to notice the relevant source, but a correct solution depends on structural similarity to map it.** A hint supplies the noticing step」；Holyoak & Koh 独立操纵表面/结构相似度后，表面相似只影响「想不想得到」，结构相似决定「用不用得上」。结构对齐同时只凸显「在两个系统里扮演对应角色的差异」（**alignable differences**），其余差异是噪声。
- **判据**：① 输入层补一个显式 hint 字段（指出骨架相似的历史案例/技能），不能指望模型自发跨领域召回；② 「没检索到相似先例」不等于「没有适用先例」，检索失败与映射失败分两栏记，不合并成「未匹配」；③ 经验沉淀只写可对齐差异，表面差异不入库（接 §四价值判断、§九记忆管理）。
- **与 §七 分工**：§七 管调用顺序（专用 Skill → Workflow → 通用 → 新建），本节管「凭什么判定某条输入属于某个专用 Skill」；`STOP / WAIT / PROCEED` 里的「已有 Skill 覆盖该能力」判定改用 13.1 的关系骨架口径。

### 13.4 来源（2026-11-14 r741A 逐字核验）
- `sciencedirect.com/science/article/pii/S0010027718303275`（Edwards / Williams / Gentner / Lombrozo，《Explanation recruits comparison in a category-learning task》，*Cognition* 2018）— WebFetch 200 全文逐字：one-to-one correspondences / systematicity principle / abstract relational schema / alignable differences / far transfer。**一手学术期刊**。
- `cognitivepsychology.com/Transfer_of_Learning` — WebFetch 200 全文逐字：Gick & Holyoak 1980/1983、schema induction、surface vs structural similarity、low-road / high-road transfer、10/30/75 数据。**第二独立域**。
- `cognitivepsychology.com/Analogical_Reasoning`、`becisions.com/dictionary/terms/analogical-reasoning` — WebSearch 快照逐串核验：45% / 21% / 92%、Holyoak & Koh 表面与结构相似度分离、alignable differences 定义、属性不进入映射。
- `uknowledge.uky.edu/cgi/viewcontent.cgi?article=1066&context=math_etds`（肯塔基大学学位论文）— 请求返回 Cloudflare「Just a moment...」验证页，**正文 0 命中，如实登记为搜索快照逐串核验，未冒充一手全文**；其 systematicity / working memory 检索瓶颈表述仅作交叉印证。
- **判非**：窄串词边界全库 SKILL.md — `structure-mapping` / `one-to-one correspondence` / `alignable differences` / `schema induction` / `analogical` / `inert knowledge` / `systematicity` **全 0 命中**；`Gick` 1 命中在搜索结果引用链（非技能正文）。全库 co-learn 台账 `analogy` 0 / `structure-mapping` 0 / `schema induction` 0。社区词典与教材站不作唯一结论来源。

**提升层**：TI 输入对齐 / KI 经验沉淀 / OI 路由。触发词：关系骨架、结构映射、表面相似、可对齐差异、schema induction、单范例不迁移、检索门槛、路由判据。
