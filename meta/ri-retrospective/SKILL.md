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

## 五、与 OS 协作

- 复盘产出 → **MI** 沉淀为"已验证经验"；可复用规则进长期记忆。
- 改进项（经验证）→ **AI** 调优 EI Guard / 提示词 / 工具顺序。
- 反复失败模式 → 回 **TI/DI** 重审方案。

## 六、来源（2026-11-07 实拉）

- github.com/poloplay0114/hard-won-claude-skills（verification-discipline / handoff-protocol / engineering-economy / spec-citation / cache-discipline / ui-station-delivery，MIT，2026-08）
- 互补：本仓 `engineering/wb-debug-loop`（调试复盘）、`agent/agent-guild`（learnings 台账）
