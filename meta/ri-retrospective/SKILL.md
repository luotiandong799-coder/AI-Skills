---
name: ri-retrospective
description: 经验复盘与持续改进（Reflection Intelligence）。当任务完成或失败后需要沉淀经验、比较预期与实际、做根因分析、总结可复用规则时调用。提供 verification-discipline / handoff-protocol / engineering-economy 等方法论，产出复盘报告。RI 可提议修改 Skills/提示词/规则/工作流，但未经授权不得直接改系统核心配置。
module: RI
modules: RI,EI
---

# RI · 经验复盘与持续改进（Reflection Intelligence）

> 本技能是 Personal AI OS 13 模块中 **RI（复盘智能）** 的载体之一（与 `wb-debug-loop` 调试复盘、`agent-guild` learnings 互补）。
> 方法论实拉（2026-11-07 实拉）：`github.com/poloplay0114/hard-won-claude-skills`（8 个从真实生产事故提炼的工程复盘技能，MIT）。

## 一、触发

- 任务完成或失败，需把经验变成下次更好的能力。
- 出现"看起来对其实不对"的偏差、误报绿、交接错位。

## 二、核心方法论（每条规则背后有事故）

1. **verification-discipline（证明对，而非看着对）**
   - 独立 oracle：用与生成者无关的渠道验证（如真实 Excel 打开而非库容忍）。
   - 绝不轻信自报结果：工具说自己成功 ≠ 真的成功。
   - 精确对账：数值/状态逐项比对，不留"差不多"。
   - 比较锚点：用已知正确样本作基准。

2. **handoff-protocol（与实现者协作不失控）**
   - 一句话结论：先给结论再给过程。
   -  phantom stall vs 真实失败：区分"卡住"与"已挂"。
   - 双向对账：双方状态互认，不假设。
   - 自曝假绿：曾报绿但实际未完成的，主动标注。

3. **engineering-economy（最小改动）**
   - 最小改动、最短测试、最佳特性。
   - 动手前先看外部世界（依赖/环境/契约）。
   - 先冻结契约（接口/§条款）再改实现。
   - 性能由基线断言守住。

4. **spec-citation（条款即公共 API）**
   - 编辑前 grep 活引用；语义锚点优于行号。

## 三、复盘报告模板

```
## 复盘：<任务>
- 预期 vs 实际：
- 根因（逐层追问到可改）：
- 应保留（做对的）：
- 应停止（踩的坑）：
- 可复用规则（写入 MI 的条例）：
- 改进建议（含是否需调 EI Guard / 提示词 / 工作流）：
- 证据（日志/产物/截图）：
```

## 四、护栏

- RI **可提议**改 Skills/提示词/规则/工作流，但**不得未经授权直接改系统核心配置**（模型路由、权限、Hook、MCP）。
- 改进项须经验证（在独立集测过）才升级为系统规则；未经验证不得自动生效。

## 五、无责复盘方法论（2026-11-07 第二轮实拉深化）

> 上轮 coverage 偏"工程纪律"（verification-discipline/handoff 等）；本轮补"仪式 + 方法 + 闭环"——复盘开成批斗会百次无用，须让人错也不会出大事的系统视角。

### 5.1 无责复盘（Blameless Postmortem）标准骨架
摘要 → 影响范围（量化：用户数/金额/时长）→ 时间线（从真实开始而非发现）→ 检测与响应 → 根因分析 RCA → 促成因素 → 经验教训 → 行动项。语言中性："什么条件允许了事件发生"而非"谁弄坏"。

### 5.2 根因分析三法
- **5 Whys**：连问五层到机制层（"人不仔细"不是根因，"流程允许 100% 直上"才是）。
- **故障树 FTA**：自顶向下拆解故障为与/或组合，定位关键路径。
- **排障树（LLM 适配）**：节点只问是非题，每步先看视图（span 树 / 三本账 / 版本标签）再动手，叶子全是止损动作；口诀"慢看段占比、错看责任层、坏看版本对齐、贵看三本账"，"当天有变更吗"是最高杠杆问题。

### 5.3 无责五问（Google SRE 落到 LLM 应用）
1. 什么坏了（现象+影响面，数字来自三支柱，非形容词）；
2. 为什么没能更早发现（哪信号该亮没亮）；
3. 为什么会发生（根因链到机制层）；
4. 怎么更快恢复（告警到止损实际用时）；
5. 怎么防止再发（行动项带责任人+验收，下次复盘开场先查上次闭环）。

### 5.4 行动项闭环（反模式预警）
- 必须有 **owner + 到期日 + 验证测试**（证明生产不再复现才算闭环）；无 owner=愿望，无日期=永不排期。
- 反模式：开成追责会（下次没人留真时间线）；行动项写"加强意识"（不可验收=不会发生）。
- 时效：事件后 24–72h 启动；MTTA/MTTR 按严重度分别跟踪趋势，而非混算均值。

### 5.5 与本章关系
上轮纪律 + 本节仪式方法 = 完整复盘；复用 §三 模板时按 5.1 骨架填、5.3 五问挖、5.4 闭环。

## 六、与 OS 协作

- 复盘产出 → **MI** 沉淀为"已验证经验"；可复用规则进长期记忆。
- 改进项（经验证）→ **AI** 调优 EI Guard / 提示词 / 工具顺序。
- 反复失败模式 → 回 **TI/DI** 重审方案。

## 七、来源（2026-11-07 实拉，含本轮深化）

- github.com/poloplay0114/hard-won-claude-skills（verification-discipline / handoff-protocol / engineering-economy / spec-citation / cache-discipline / ui-station-delivery，MIT，2026-08）
- 互补：本仓 `engineering/wb-debug-loop`（调试复盘）、`agent/agent-guild`（learnings 台账）

### 本轮深化来源（2026-11-07 实拉，无责复盘）
- blameless.com/blog/incident-retrospective-postmortem-template（无责复盘标准模板）
- itoc360.com（MTTA/MTTR 指标 + blameless 模板骨架）
- aiknowledge.cn/article/75075（排障树 / 无责五问 / LLM 适配）
- renrendaima.com/wap/article/2354.html（无指责 Postmortem / 5 Whys / FTA）
- yisu.com/zixun/1107281.html（运维事后分析结构）
