# 2026-10-08 学习轮 r444B：技能 fitness 度量（SkillForge）

轮次：r444B（WB 侧三轮连跑第 2 轮，2026-10-08）
主题：技能 fitness 必须是可经验测度的量；晋升门与退役门同尺

## 一、本轮实拉信源
- arXiv API `export.arxiv.org/api/query?search_query=all:agent+skills`（37,523B，HTTP 200）列出近期论文，取 `SkillForge: Co-Evolving Skills and Agents via Dynamic Skill Lifecycles`（2610.09832）。
- `arxiv.org/html/2610.09832v1`（567,160B，HTTP 200，去标签全文 98,121B 抽取）一手逐串命中 `applicability condition ω` / `pre-retire low-fitness skills … under the base model's own rollouts` / `retirement events with human-annotated failure categories` / `fitness-driven skill lifecycle of trial , active , stable , and retired states` / `a skill whose fitness once reached the stable state but later drops below the retirement threshold` / `borderline-fitness skills rewritten by an LLM-guided mutation operator`。

## 二、本轮落地（四列）
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r444B | engineering/wb-agent-evaluation | 1.6.0 | 技能的「fitness」= 适用条件 ω 下用 agent 自身 rollout 的经验成功率；进库前 pre-RL 按 fitness 预退役低分；stable 跌破阈值即 obsolescence 退役；退役须带人类标注失败类别而非只看低分 — arXiv 2610.09832 567,160B |

## 三、判非不落（均给一手核验依据）
- SkillForge「co-evolving skills and agents via RL」整体框架属于训练期机制，与本库「评测/治理」职责轴不同，且需 RL 训练回路，不落入 WB 技能体系（留参考）。
- 论文其余点（LLM-guided mutation 算子具体超参、阈值敏感性）为实验参数非方法论，证据等级不足，不落。

## 四、豆包线状态
暂停中，游标冻结 r274C，本轮不写②、不判重。

## 五、Qoder 线游标
维持 r453-Q-C（无 r454+ 新轮）。
