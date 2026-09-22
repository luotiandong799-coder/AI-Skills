# 2026-09-21 学习轮 r112-G（第 7 轮 · 16 轮批 r112）

来源：docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices（实拉全文）。

## 独点：3 条（待批次末与 WB 提交对齐后并入 wb-skill-authoring）

**D1. 指令自由度三档匹配（high/medium/low freedom）**
- 内容：按任务脆弱性与可变性选具体度。高自由度=文本指令（多路径可行、靠上下文判断，如 code review 流程）；中自由度=参数化伪代码/脚本（有偏好模式、可微调）；低自由度=精确命令禁改（脆弱易错、顺序关键，如数据库迁移，加参数都禁止）。比喻：窄桥（只能一条路→低自由度护栏）vs 开阔地（多条路→只给方向）。
- 提升层：可复用 Skill（指令/技能编写原则）。
- 判重：ed 现有 §约束块显式化管"coding prompt 里声明不许改什么"，本条管"按任务脆弱性决定指令给多具体"——互补非重叠；pt §按产物存活期选型管资源，无关。

**D2. 技能命名用动名词形式（gerund form）**
- 内容：processing-pdfs / analyzing-spreadsheets / testing-code，让名字描述活动而非对象；name 字段小写字母数字连字符。
- 提升层：可复用 Skill（命名规范）。
- 判重：sa 已落 name 保留词/长度/字符集（r120），但未规定命名语义形式——补位不重叠。

**D3. 渐进披露结构规范（progressive disclosure）**
- 内容：SKILL.md 体量 ≤500 行；超限按域分子文件（reference/finance.md 等）按需加载；启动只预载全部技能的 name+description 元数据，SKILL.md 仅相关时读取，脚本执行不加载全文（只耗输出 token），大文件零上下文惩罚直到读取；文件引用一层深、路径用正斜杠、命名要描述内容；确定性操作用脚本（validate_form.py）而非让模型现写。
- 提升层：可复用 Skill（技能结构）。
- 判重：WB 已做 description 术语外置附录（同族思想），但"500 行上限+按域分子文件+脚本零上下文惩罚"作为显式结构规范未落——吸收为新条目（可并入 sa，与附录 Z 呼应）。

## 其余判不落
- context window 是公共资源/每 token 竞争 → 与 ctx §上下文预算同源。
- 用所有计划模型测试技能 → 与 sa §引擎是运行时轴重叠>60%。
- 无 voodoo constants → 与既有"参数要可溯源"同源。
- 三评测起 → 与 sa §评测已学同源。

## 版本
ed 2.96.0 未动（WB 工作树 M 状态，待其提交后批次末合并 D1-D3 入 sa/ed）。
