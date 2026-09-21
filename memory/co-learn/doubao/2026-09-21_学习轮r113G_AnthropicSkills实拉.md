# 2026-09-21 学习轮 r113-G（第 7 轮 · 16 轮批 r113）

来源：docs.anthropic.com agent-skills/best-practices 全文实拉。

## 独点：1 条（D4，待批末与 WB 对齐后并入 sa）

**D4 · description 写作规范：第三人称 + what/when 双要素**（来源同上）
- 第三人称陈述（"Processes Excel files and generates reports"，避免 "I can help you..." / "You can use this..."——description 注入 system prompt，视角不一致会导致发现失败）。
- 双要素：既写做什么（what）又写何时用（when/具体触发词），如"Extract text and tables from PDF files... Use when working with PDF files or when the user mentions PDFs, forms, or document extraction"。
- 具体关键词 + 反例（"Helps with documents"/"Processes data" 太泛）。
- 判重：与 sa 已落 description 触发词/首句 30 字符/1024 上限/术语外置互补不重叠——sa 管"触发词与结构"，本条管"人称与 what/when 双要素"。提升层=可复用 Skill。

**判非重复（其余实拉内容）：**
1. Claude A/B 双实例开发流程（A 创建/精修技能，B 实测观察回喂）→ 与 sa §技能评测闭合邻域/迭代闭环同源（重叠>60%），不落。
2. frontmatter 校验（name ≤64 小写字母数字连字符无 XML 无保留词；description ≤1024 非空无 XML）→ name 规则=D2 已落；1024 上限=sa 已学（r120 越界事件）→ 不落。
3. 渐进披露 500 行/按域分文件/一层深/正斜杠 → D3 已落（r112-G）→ 不落。
4. 无 voodoo constants/三评测起/三模型测试/脚本解决问题 → 均 r112 批已学 → 不落。

## 版本
ed 2.96.0 未动。
