---
name: vi-fact-verification
description: 事实与结果验证（Verification Intelligence）。当任务涉及事实声称、外部来源引用、数据/计算结果核对、代码或文件改动验收、或"判断任务是否真正完成"时调用。落实独立性原则与来源分级，识别未经证实的结论，给出"真/误导/夸大/缺证据/假"评级。注意：EI 的 CCS 验"执行过"，VI 验"对不对"——二者互补不重复。
module: VI
modules: VI,EI
---

# VI · 事实与结果验证（Verification Intelligence）

> 本技能是 Personal AI OS 13 模块中 **VI（验证智能）** 的载体之一（与 `wb-artifact-verification`/`wb-agent-evaluation`/`wb-ui-visual-qa`/`wb-media-forensics` 同属 VI，各管一块：artifact=产物、eval=评测、ui=界面、media=媒体、本技能=事实/来源/完成度）。
> 方法论实拉（2026-11-07 实拉）：FactCheck.org（Our Process / How to Combat Misinformation）、The Truth in Journalism Project（How to Fact-Check）、Open Government Platform（Fact-Checking Process）。

## 一、核心原则

- **验证 ≠ 执行**：EI 的 CCS 证书只证明"步骤执行过且留痕"；VI 负责证明"结论/事实/交付是对的"。把"执行过"当"完成"是头号误区。
- **独立性原则**：每个事实至少由 **1 个权威源** 或 **多个相互独立的非权威源** 确认；避免用两篇基于同一原始报道的新闻互相印证（它们不独立）。
- **权威是事实相对性的**：某人个人站是其姓名拼写/自我认同的权威源，却不是其 sibling 经历的权威源。

## 二、来源分级（核查时优先序）

1. **一手官方**：政府出版物、法律文本、法院文书、官方数据发布。
2. **权威二手**：同行评审研究、权威机构分析、官方机构报告。
3. **专家源**：经核实专家/组织的直接陈述。
4. **新闻与媒体**：声誉媒体，主要用于时事背景（且须多源交叉）。

> 一手不可得时，明确说明使用二手源并论证其可靠性；匿名源须有名源或强物证佐证。

## 三、核查清单（逐条过）

- [ ] 追溯到一手源
- [ ] 与官方记录核对（可得时）
- [ ] 跨多个可靠源交叉验证
- [ ] 检查时效性与相关性（过时即失效）
- [ ] 检查上下文与完整性（断章取义＝误导）
- [ ] 数据与计算独立复算
- [ ] 技术/代码类：实测可运行、版本与日期依赖注明
- [ ] 多媒体：反向图片/视频/音频检索验真，警惕 AI 生成内容

## 四、评级输出

对每个被核查声称给结论之一：**真 / 误导 / 夸大 / 缺证据 / 假**，并附证据链（来源 + 关键句 + 日期）。

## 五、与 OS 协作

- **EI** 的 `certify` 之后接 VI 做"正确性"双验收（执行+正确）。
- 涉外部事实/引用的交付（论文、报告）→ 先 VI 后交付。
- 验证结论（含未通过项）→ **MI** 沉淀；反复出现的未通过项 → **RI** 复盘。

## 六、来源（2026-11-07 实拉）

- FactCheck.org 流程与反误导：factcheck.org（Our Process / How to Combat Misinformation, 2025-04）
- 独立性原则与来源分级：thetijproject.ca/guide/how-to-fact-check/
- 核查标准与来源层级：opengovtplatform.org/fact-checking
