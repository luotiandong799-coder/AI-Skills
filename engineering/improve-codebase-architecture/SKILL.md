---
name: improve-codebase-architecture
description: 扫描代码库找出「深化机会」（把浅模块做深的重构），生成可视化 HTML 报告（Tailwind+Mermaid），再与用户逐个过选定的候选。用于提升可测试性与 AI 可导航性，而非堆接口。
version: 1.0.0
display_name: 架构深化
display_name_en: Improve Codebase Architecture
agent_created: true
---

# Improve Codebase Architecture（架构深化）

把架构摩擦面暴露出来，提出 **deepening opportunities**：把浅模块做深的重构。目标是可测试性与 AI 可导航性。

本技能建立在共享设计词汇之上（**module / interface / depth / seam / adapter / leverage / locality**），及其原则（删除测试、「接口即测试面」、「一个 adapter = 假说缝，两个 = 真实缝」）。每条建议都用这些词，不要漂移到「组件 / 服务 / API / 边界」。

## 流程

### 1. 探查

**先定范围再扫：YAGNI。** 深化模块靠让未来改动更易，所以重点放在最近频繁变动的部分：

- 用户指定了方向（某模块/子系统/痛点）→ 直接采用，跳过下面的推断。
- 否则回看一段提交历史（`git log --oneline`）找热点文件/区域，让这些路径先抓住注意力；若改动分散无热点，再扩大网。

先读项目领域词汇表（如 `CONTEXT.md` 或 README 的领域术语）与所触区域的 ADR。

然后派一个子 agent 走读代码库，有机探索，记录你感到摩擦处：

- 理解一个概念是否要在许多小模块间跳？
- 哪些模块**浅**（接口复杂度接近实现）？
- 哪些纯函数仅为可测性抽出，但真正的 bug 藏在调用方式里（无 **locality**）？
- 紧耦合模块是否跨缝泄漏？
- 哪些部分无测试、或当前接口难测？

对怀疑浅的模块做 **删除测试**：删掉它会集中复杂度，还是仅搬动？「会集中」才是你要的信号。

### 2. 用 HTML 报告呈现候选

写一份**自包含 HTML** 到系统临时目录（`$TMPDIR`→`/tmp`→Windows `%TEMP%`），文件名 `<tmpdir>/architecture-review-<timestamp>.html`，每轮一个新鲜文件，不落仓库。打开给用户（`xdg-open`/`open`/`start`）并给绝对路径。

报告用 **Tailwind CDN** 布局、**Mermaid CDN** 画图（关系呈图状时用：调用图、依赖、序列），手写 CSS/SVG 做更编辑化的视觉（质量图、剖面、折叠动画）。每个候选一张卡：

- **Files**：涉及的文件/模块
- **Problem**：当前架构为何产生摩擦
- **Solution**：会改变什么的 Plain English 描述
- **Benefits**：用 locality 与 leverage 解释，测试如何变好
- **Before / After 图**：并排手绘，示意浅与深
- **Recommendation strength**：`Strong` / `Worth exploring` / `Speculative`，徽章呈现

结尾 **Top recommendation**：先攻哪个、为什么。

用领域词汇表命名模块（词汇表称「Order」就说「Order intake 模块」，不要说「FooBarHandler」或「Order 服务」）。

**ADR 冲突**：仅当摩擦真实到值得重开 ADR 才呈现；在卡上标清（如警示：「与 ADR-0007 冲突，但因…值得重开」）。不要列每个 ADR 禁止的理论重构。

写完后问用户：「想深入哪一个？」

### 3. 过选定候选

用户选定后，调用 `grill-me` 与它走决策树：约束、依赖、深化后模块的形状、缝后面是什么、哪些测试能存活。

决策 crystallize 时的内联副作用：

- 用词汇表没有的概念命名深化模块？→ 加进词汇表（惰性创建文件）。
- 对话中 sharpen 了模糊词？→ 当场更新词汇表。
- 用户以有分量的理由否决候选？→ 提议记一条 ADR：「要我把这记成 ADR，让未来架构评审不再重提吗？」仅当这理由未来探索者确实需要以避免重提时才提；跳过临时理由（「现在不值」）与不证自明的。
- 想探索深化模块的可选接口？→ 调用 `wb-spec-driven` 的设计两次并行子 agent 模式。

## 与现有体系衔接

- 报告前的「探查」阶段与 `wb-debug-loop` 的根因探查、`wb-spec-driven` 的信息收集互补。
- 选定候选后的决策走查可用 `grill-me` 或 `wb-spec-driven`。
- 不在此阶段直接写实现代码；先对齐再交 `wb-spec-driven` 的计划-实现-验证循环落地。

---

> 出处：改编自 [mattpocock/skills](https://github.com/mattpocock/skills)（MIT），已适配 WorkBuddy，去除 Claude 专有字段（disable-model-invocation 等）。
