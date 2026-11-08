# knowledge-base


<!-- ≤200 行统一迁移 2026-09-30（用户裁决）：自 SKILL.md 原文下沉，内容零丢失 -->

## 技能库维护的实证基线：是「人类治理 + AI 辅助」，不是自主演化（来源：arXiv 2609.05677《Who Maintains Agent Skills? A Longitudinal Study of Human-Governed, AI-Assisted Skill Maintenance》2026-09-29 r319C arxiv.org 实拉 200）
- 原文：挖取 5 个公共 AI 技能仓的完整提交历史（2025-10 至 2026-06），覆盖 **873 commits、143 个技能文件、254 次实质性创建后修订**；三条结论之一：**every substantive edit is authored or merged through a named human account，而 62% 带 AI co-author trailer**，且仓间差异很大；这些修订是真实的策展（genuine curation）而非机械改动。
- 判据：① 治理设计不要假设"技能库能自己进化"——实证里**每一次实质修订都有具名人类作者或合并者**，AI 是共同署名而非决策者；② 因此自动化治理的正确定位是**把候选变更准备好、把影响面算清楚，把合并权留给人**，而不是自动落盘；③ 用"AI co-author 比例"作健康度指标时先看仓间差异（62% 是均值，个别仓可能近 0 或近 100），别当普适常数；④ 与 §分层判据 互补：分层决定"放哪"，本条决定"谁能改"。
- 提升层：治理/记忆。触发词：谁维护技能、人类治理 AI 辅助、具名合并者、AI co-author trailer、技能库纵向实证。
## r709B · 本地规则只写增量：不得豁免项目级约束，也不得按"目录配额"建文件（来源：GitHub `affaan-m/ECC`·`.agents/skills/module-governance/SKILL.md` 6,643B，2026-11-08 一手实拉；逐串命中 `Local rules cannot waive project-wide constraints` / `Do not create empty files to meet a two-file quota` / `Directory names alone do not establish a bounded context` / `Resolve relative links from each referencing document's directory`）

- **两层规则的权力方向**：项目级指令持有全局约束、模块导航、跨模块协作；**本地规则只能加"额外的"模块约束**（职责、状态归属、公共接口指针、验证入口），**不能豁免项目级约束**——本地是 deny-only 的加严方向，不是讨价还价的入口。
- **项目级已覆盖且本地无缺失 → 链接过去，不建副本**：维护两份必然漂移；沿用仓库已有的 `CLAUDE.md`/`AGENTS.md` 等生效面，不强迫改名。
- **禁止按配额建文件**：不为"每个目录两个文件"补空文件；**缺失的本地文件是复核提示，不是建文件的命令**。空文件会让后来者以为这里有约定。
- **边界不能靠目录名证明**：目录结构不构成 bounded context；业务职责、状态归属、真实消费者要读代码与契约才知道，有歧义就摆出来，不臆造规则。
- **相对链接按"每个引用文档自己的目录"解析**，不是终端 cwd；链接检查通过**不等于**业务实现完成；同名文件仍可能是错的 owner（要核对内容而不是文件名）。
- 判据：**文档检查是复核工具，不是实现证据**——两者混同会把"写好了文档"当成"做完了功能"。
