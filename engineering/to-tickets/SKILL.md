---
name: to-tickets
description: 把方案、规格或当前对话拆成一组 tracer-bullet 工单，每张声明其阻塞边（blocking edges），先与用户核对粒度与依赖，再写入本地文件或展示确认。用于把一个大目标切成可独立验证的垂直切片。
version: 1.0.0
display_name: 拆工单
display_name_en: To Tickets
agent_created: true
---

# To Tickets（拆工单）

把一个计划、规格或对话拆成一组 **tickets**：每个都是贯穿各层的「 tracer-bullet 垂直切片」，并声明**阻塞它的其他 ticket**。

## 何时用

用户已有方案/规格/大目标，想切成可逐步执行、可独立验证的小块；或用户说「帮我拆成工单 / 拆成 ticket / 把这一步拆开」。

## 流程

### 1. 收集上下文

从对话上下文直接工作。若用户给出引用（规格路径、issue 编号或 URL），先读取其完整正文与评论。

### 2. 探查代码库（可选）

若尚未理解当前代码状态，先探查，使 ticket 标题/描述使用项目领域术语、尊重相关 ADR。寻找可先做的预重构（"先让改动变容易，再做那件容易的改动"）。

### 3. 起草垂直切片

按 **tracer-bullet** 切分：

- 每个切片都窄但**完整**穿过每一层（schema / API / UI / 测试）：是垂直切片，不是某一层的水平切片
- 完成的切片自身可演示或可验证
- 每个切片大小控制在单个新上下文窗口内可完成
- 任何预重构应先做

给每个 ticket 标 **blocking edges**：必须先于它完成的其它 ticket。无阻塞者的 ticket 可立即开始。

**宽重构是垂直切片的例外**：宽重构是单一机械改动（重命名列、改共享符号类型），爆炸半径横跨整个代码库。不要硬塞进 tracer-bullet，按 **expand–contract** 排序：先 expand（新形式并联旧形式，不破坏任何东西）→ 按爆炸半径分批迁移调用点（每批一个 ticket，批间保持 CI 绿）→ 最后 contract（无调用者后删旧形式）。

### 4. 让用户过一遍

把拆分以编号列表呈现，每个 ticket 显示：

- **标题**
- **Blocked by**：依赖哪些其它 ticket（若有）
- **交付什么**：这个 ticket 让哪段端到端行为可用

问用户：粒度合适吗？阻塞边对吗（每张 ticket 只依赖真正卡住它的）？要不要合并/再拆？迭代到用户认可。

### 5. 发布工单

默认写入**本地文件**（无需外部 tracker）：在用户工作区建 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，按依赖顺序从 `01` 编号（阻塞者在前）。每文件用下方模板，一 ticket 一文件，绝不合并成单文件。

也允许仅**展示给用户确认**而不落盘（当用户要的是拆分本身而非文件）。

<local-ticket-template>

# <NN>: <Ticket 标题>

**要做啥：** 用户视角的端到端行为，不是逐层实现清单。

**Blocked by：** 阻塞它的 ticket 编号/标题，或「None（可立即开始）」。

**Status：** ready

- [ ] 验收标准 1
- [ ] 验收标准 2

</local-ticket-template>

避免写具体文件路径或代码片段（易过时）。例外：原型产出的片段比文字更精确表达某个决策（状态机、reducer、schema、类型形状）时，可内联并简短注明来自原型。

## 与现有体系衔接

- 拆分前若需求还模糊，先走 `grill-me` / `wb-spec-driven` 把方案/规格压实。
- 每个 ticket 落地可交给 `wb-spec-driven` 的计划-实现-验证循环独立推进。
- 宽重构的 expand–contract 排序思路与 `wb-execute-discipline`（失败持续攻坚）互补。

---

> 出处：改编自 [mattpocock/skills](https://github.com/mattpocock/skills)（MIT），已适配 WorkBuddy，去除 Claude 专有字段（disable-model-invocation 等）。
