# 学习轮 r195-A：Anthropic Agent Skills三层progressive与script零token与跨surface不同步与runtime差异与reserved word（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | make.com/en/help/scenarios/error-handling | 仅导航壳无内容 |
| 2 | pipedream.com/docs/triggers/ | 死链 |
| 3 | docs.anthropic.com Agent Skills overview | OK 全文 |

## 独点（5 个）
### A1：三层 progressive disclosure token 账（来源：Anthropic Agent Skills）
- Level 1 metadata ~100 tokens 常驻 system prompt；Level 2 SKILL.md body <5k tokens 触发时加载；Level 3 resources/scripts 按需 bash 读，不进 context。
- 判据：**装 N 个 skill 只花 N×100 token 常驻**——多 skill 不罚。
- **提升层**：上下文管理。

### A2：script 代码不进 context，只 output 进（来源：Anthropic Agent Skills）
- Claude bash 跑 `validate_form.py`，脚本源码不进 context，只有"Validation passed"进。
- 判据：**确定性操作用脚本，比让 LLM 现写代码省 context 且可靠**。
- **提升层**：上下文/工具。

### A3：跨 surface skill 不同步（来源：Anthropic Agent Skills）
- claude.ai / API / Claude Code 三端各传各的，不自动同步。
- 判据：**同一份 skill 要传三次**——跨端分发是独立工程。
- **提升层**：分发。

### A4：runtime 约束差异——API 无网无装包 / Code 全网络 / claude.ai 视配置（来源：Anthropic Agent Skills）
- API：No network access、No runtime package installation、only pre-installed packages；Code：full network、only local install；claude.ai：varying。
- 判据：**同一份 skill 在不同 surface 行为可能完全不同**——写 skill 时按 surface 降级。
- **提升层**：可移植性。

### A5：skill name 禁 reserved words "anthropic"/"claude"（来源：Anthropic Agent Skills）
- name max 64，小写数字连字符，禁 XML tag，禁 reserved words。
- 判据：**品牌词保留给官方 skill**。
- **提升层**：规范。

## 判重说明
- A1 三层 progressive → r193-B 已记三层 token budget；取"~100/<5k/unlimited 具体 token 数"增量。
- A2 script 零 token → r192 补抓 LangFlow 已记 playground；取"script 源码不进 context"增量。
