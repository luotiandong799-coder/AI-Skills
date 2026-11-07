---
name: si-safety-governance
description: 全局安全治理（Security Intelligence）。在所有对外/写/删/权限/部署/工具调用/结果输出动作前与后调用，覆盖数据读取、信息传递、工具调用、结果输出全链路（不只执行前）。扫描提示注入、数据外泄、权限边界、工具中毒、危险代码、供应链、过度代理、记忆中毒等风险，给出风险评分与"可否安装/执行"门禁。本技能是 SI 载体，对系统既有 skills-security-check 做能力补齐。
module: SI
modules: SI,EI
---

# SI · 全局安全治理（Security Intelligence）

> 本技能是 Personal AI OS 13 模块中 **SI（安全智能）** 的载体之一，补齐 `system/skills-security-check`（腾讯云鼎，偏供应链引用安全）未覆盖的全链路安全维度。
> 方法论实拉（2026-11-07 实拉）：`NVIDIA/SkillSpector`（71 规则 / 17 类，风险评分与门禁）、`Bersilk-hub150/skillhawk`、`trailofbits/skills`。

## 一、原则：SI 贯穿全链路

不止"执行前检查器"。覆盖：数据读取（敏感信息保护）→ 信息传递（注入/泄露）→ 工具调用（危险命令/权限/中毒）→ 结果输出（外发/泄露）。任何写/删/权限/部署动作前必过 SI。

## 二、扫描目标（17 类 · 节选高频）

| 类别 | 检测点 |
|---|---|
| 提示注入 | 指令覆盖、隐藏指令、外泄命令、有害内容 |
| 反拒绝 | 抑制拒绝/免责声明/安全策略失效 |
| 数据外泄 | 环境变量收集、外部传输、上下文泄露 |
| 权限提升 | 过度权限、Sudo/Root、凭证访问 |
| 供应链 | 未固定依赖、外部脚本拉取(curl\|bash)、已知 CVE(OSV.dev)、typosquatting、混淆代码 |
| 过度代理 | 无约束工具访问、自主决策 |
| 危险代码(AST) | `exec()`(CRITICAL)、`eval()`(HIGH)、`subprocess`(HIGH)、`os.system`(HIGH)、危险执行链 |
| 系统提示泄露 | 直接/间接/基于工具泄露 |
| 记忆中毒 | 持久上下文注入、记忆篡改 |
| 工具误用 | 参数滥用、链式滥用、不安全默认值 |
| 流氓代理 | 自我修改(CRITICAL)、会话持久化 |
| 触发滥用 | 过宽触发、影子命令触发 |
| MCP 专项 | 最小权限缺失/通配/过度声明；元数据隐藏指令、Unicode 欺骗、描述-行为不匹配 |

## 三、工作流（两阶段）

1. **静态（必选、快速）**：正则匹配（11 分析器）+ Python AST 行为分析（危险调用）+ OSV.dev 查依赖 CVE（离线回退）。
2. **LLM 语义（可选，默认开）**：评估上下文与意图提置信度；确定性发现始终保留。`--no-llm` 可纯本地。

## 四、风险评分与门禁

- 评分：CRITICAL +50 / HIGH +25 / MEDIUM +10 / LOW +5；可执行脚本 ×1.3。
- 级别：0–20 **SAFE**；21–50 **CAUTION**；51–80 **DO NOT INSTALL**；81–100 **CRITICAL**。
- 门禁：`--fail-on-findings` 高风险即非零退出；CI 集成（SARIF 2.1.0）。

## 五、与 OS 协作

- 任何中/高风险动作前 → **SI** 评估 → 高风险须用户明确授权（接既有确认机制）。
- 安装新 Skill/MCP 前 → SI 扫描（不执行被扫对象，仅静态+可选 LLM）。
- 扫描结论 → **MI** 留痕；反复出现的中危 → **RI** 复盘。

## 六、来源（2026-11-07 实拉）

- NVIDIA/SkillSpector（71 规则 / 17 类 / 风险评分 / SARIF / MCP 工具）：github.com/NVIDIA/SkillSpector
- skillhawk（Skill/MCP 安全扫描器，提示注入/危险命令/权限边界）：github.com/Bersilk-hub150/skillhawk
- trailofbits/skills（安全研究审计技能）：github.com/trailofbits/skills
- 互补：本仓 `system/skills-security-check`（供应链引用审计）
