---
name: agent-evolution
version: "1.0.0"
description: 智能体持续进化引擎：将每次高价值任务自动沉淀为可复用 Skill、经验与规则，并统一调度已有 Skill 体系完成智能调用、持续优化、工作流记忆、安全检查与生命周期治理，杜绝重复造轮子。触发：完成复杂任务后需总结方法、发现可复用流程想生成 Skill、任务收尾想自动复盘、希望 Agent 少问多想自主进化时调用。
license: MIT
metadata:
  layer: meta
  role: 协调器/路由器（不重实现，全部委派给已有技能）
  reuse:
    - meta/personal-ai-os
    - engineering/distill-cat
    - engineering/wb-skill-authoring
    - skills/knowledge-governance
    - engineering/wb-spec-driven
    - engineering/wb-execute-discipline
    - engineering/wb-debug-loop
    - system/skills-security-check
    - agent/agent-guild
---

# 智能体能力进化引擎（agent-evolution）

本 Skill 是 **Hermes Agent 式长期进化的常驻协调层**。它不重实现任何能力，而是定义一条「任务后自动进化循环」，并把八大能力逐一路由到已有 Skill。目标：让 WorkBuddy 每完成一次高价值任务，就自动变强一点，同时**保持 Skill 库精简**。

> 最高约束（来自用户原则，优先生效）：**少而精、禁止重复、优先复用、持续进化、结果导向**。本 Skill 自身不存放方法论正文，只做编排与触发。

## 一、八大能力 → 已有技能路由表（优先复用，禁止重造）

| # | 能力 | 实际执行者（已有 Skill） | 本层只做 |
|---|---|---|---|
| 1 | Skill 自动沉淀 | `engineering/distill-cat`（蒸馏成技能包）+ `engineering/wb-skill-authoring`（写法/审计/接线） | 触发判定 + 传料 |
| 2 | Skill 智能调用 | `meta/personal-ai-os` 路由 + 各 Skill 触发词；多 Skill 组合走 `engineering/wb-spec-driven` 编排 | 路由决策 |
| 3 | Skill 持续优化 | `engineering/wb-skill-authoring`（体检/盲测）+ `skills/knowledge-governance`（巡检）+ `engineering/wb-debug-loop` | 排程复盘 |
| 4 | 工作流记忆 | `skills/knowledge-governance`（记忆分层）+ `agent/agent-guild`（跨 agent 共享）+ 工作记忆文件 | 写入规范 |
| 5 | Agent 执行规划 | `engineering/wb-spec-driven`（规约驱动）+ `engineering/wb-execute-discipline`（零省略） | 生命周期串接 |
| 6 | 自动安全检查 | `system/skills-security-check` + `meta/personal-ai-os` §4–§8（三级权限/停止条件） | 前置+后置清单 |
| 7 | Skill 生命周期 | `engineering/wb-skill-authoring`（合并去重/双路由防呆）+ `skills/knowledge-governance`（合并/压缩/归档） | 触发治理 |
| 8 | 多入口适配 | `meta/personal-ai-os` Computer Agent + `system/browser-automation`/`bsk-*` + `system/computer-use-windows` + 各连接器 | 统一收口进本循环 |

## 二、持续进化主循环（统一生命周期）

每次任务严格走：

```
需求分析 → 任务规划 → 调用 Skill → 执行工具 → 结果检查 → 沉淀总结 → 优化迭代
```

- **需求分析**：先判断任务指向，再定入口层（见 `meta/personal-ai-os` 信息获取梯度）。
- **任务规划**：≥3 步的实现任务先立规约（`wb-spec-driven`）。
- **调用 Skill**：命中即加载，不凭记忆复述冒充加载；多步组合用编排。
- **执行工具**：Agent 模式全程自主，仅安全/不可逆/系统强制手势才请用户介入。
- **结果检查**：独立验证（`wb-artifact-verification` 思路）+ 清理垃圾文件（见下「后置安全检查」）。
- **沉淀总结**：跑 §三 复盘清单，决定是否沉淀（§四）。
- **优化迭代**：更新相关 Skill 或记忆，触发 §七 生命周期治理。

## 三、任务后自动复盘清单（每次高价值任务必跑）

逐项回答，结论写进工作记忆，不达标则进入优化：

1. **是否完成目标** —— 是/否；未达成原因与证据。
2. **哪一步效率低** —— 标出耗时/调用最多的环节，给具体优化动作。
3. **是否产生错误** —— 报错/失败/返工；根因与修复（走 `wb-debug-loop`）。
4. **是否需更新 Skill** —— 若某步骤方法可复用且现有 Skill 未覆盖或已过时 → §四 判定。
5. **是否产生新用户习惯/决策规则** —— 是则写入 `skills/knowledge-governance` 记忆层，避免下次再问。

## 四、自动沉淀判定（何时生成/更新 Skill）

满足任一即沉淀，否则不沉淀：

- 同一类任务 **≥2 次**出现，或单次任务步骤 **≥8 步**且方法可迁移。
- 踩过坑且根因具有 **普适性**（不止本次有效）。
- 用户明确说「以后这类都按这个来」。
- 现有 Skill **已过时/描述失准** → 更新而非新建。

沉淀方式：调用 `engineering/distill-cat` 产出技能包草稿 → `engineering/wb-skill-authoring` 审计（PyYAML 全解析、description≤1024、触发词只加末尾、首句<30字、无标点开头）→ 接线（写入相邻技能分工表/触发词）→ 同步仓库+live+push。

**禁止重复硬规则**：新建前必须先 `grep`/全局技能清单确认无同类；存在同类则合并或扩展，绝不平行新建。

## 五、工作流记忆写入规范（避免重复询问）

| 内容 | 落点 | 说明 |
|---|---|---|
| 用户习惯 / 常用操作 / 决策规则 | `~/.workbuddy/MEMORY.md`（跨项目）或项目 `MEMORY.md` | 长期偏好，显式写入 |
| 每日工作留痕 | `项目/.workbuddy/memory/YYYY-MM-DD.md` | 追加式，不覆盖 |
| 工作模板 / 可复用流程 | 独立 Skill（见 §四）或 `memory/` 参考文件 | 不塞进对话 |
| 跨 agent 共享身份/规则/交接 | `agent/agent-guild` | 纯本地 Markdown/JSON |

## 六、前置安全检查（执行前）

逐项过 `meta/personal-ai-os` §4–§8：

- 权限是否足够（L0 自动 / L1 提示 / L2 必须确认）。
- 是否涉及敏感操作（删文件、改注册表、发消息、付费、push）。
- 是否需要用户确认（不可逆/合规/安全风险 → 停手请示）。
- 是否可能造成错误（影响面、回滚点：`personal-ai-os` §5 先建状态与回滚点）。

安装/更新外部 Skill 前必跑 `system/skills-security-check`（纯静态审计，绝不执行被审脚本）。

## 七、后置安全检查（执行后）

- 文件是否正确生成/修改（独立读取核对）。
- 数据是否完整（无截断、无丢失、无部分写入）。
- 是否留下垃圾文件/缓存（`personal-ai-os` §17–§19：临时目录、缓存、垃圾清理规则）。
- 个人目录（Desktop/Downloads/Documents）**绝不**递归删/清空；只生成只读报告。

## 八、Skill 生命周期治理（保持精简）

定期（或每 N 次任务后）触发，复用既有技能：

- **创建**：仅 §四 判定通过，且全局无同类。
- **更新**：方法演进/触发词失效 → `wb-skill-authoring` 改 description/正文。
- **合并**：功能位重叠 → `wb-skill-authoring` 合并判据（同一功能位+触发词互覆盖才合并；市场/第三方只划边界不文件级合并）。
- **删除**：低价值/长期不用/被更好替代 → 经 `knowledge-governance` 归档评估后删除；删除前先确认无依赖引用。
- **核心纪律**：数量随功能位伸缩，不为「变强」无脑堆量（见 `personal-ai-os` §36）。

## 九、多入口适配（统一收口）

所有入口都归一进 §二 主循环，不在入口侧各自实现逻辑：

- 微信/企业聊天消息 → 解析意图 → 进主循环。
- Windows 操作 / 文件处理 / 浏览器任务 / 自动化流程 → 路由到 `personal-ai-os` Computer Agent 与对应执行 Skill。
- 连接器（邮件/会议/网盘等）→ 取数据后归一为任务输入。

## 十、执行原则（常驻，不可被覆盖）

1. **少而精**：宁缺毋滥，一个功能位一个 Skill。
2. **优先复用**：能用现有 Skill 解决的，绝不新建。
3. **持续进化**：每次高价值任务必须考虑沉淀，但只沉淀真有价值的。
4. **结果导向**：Skill 必须提升实际效率，不产出「看起来很强」的无用资产。
