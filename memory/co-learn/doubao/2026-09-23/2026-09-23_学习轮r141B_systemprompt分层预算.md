# r141-B 全站实拉 · system prompt 分层预算落地 mts

> 日期：2026-09-23｜批次：r141-B（定时触发）｜模式：AI技能库学习批
> 判重基准：WB r138 九点（在途）+ WB r129-133 已落 + 豆包 r135/r139/r140/r141-A 已落

## 一、逐站实拉（10 次，全量信源覆盖）
| # | 信源 | 实拉内容 | 提炼 |
|---|---|---|---|
| 1 | AI 写作（specswriter/risingresearcher/jottler） | 证据检索与起草解耦（架构层）；fact-check 两遍（数值+引用逐个点击）；引用=引用真实+主张匹配成对验证；高利害主张两个独立来源 | 与 wb-doc-writing 引用审计/先取证后落笔重叠>60%，不落 |
| 2 | Agent 规划（arXiv/Microsoft/agentbus） | **重规划三分支：continue（计划有效继续）/ modify（保留完成工作调整剩余）/ replan（丢弃剩余重来）**；失败输入=失败步骤 ID+原因+剩余目标；local adjustment vs global replanning | **ED 1906 已有 PROCEED/RETRY/REPLAN 三选一**，同构判重不落 |
| 3 | AI 编程工具（DEV/frankx/houseofmvps） | Cursor（IDE-first）/Claude Code（terminal-first 长自主）/Codex（并行云任务）定位；SWE-bench 87.6%；按工作形态选工具 | 工具选型事实，个人价值低，不落 |
| 4 | GraphRAG/Agentic RAG（Kanopy/Airbyte/aisavvytech） | GraphRAG 适用=实体关系丰富+多跳问题；向量+图混合；Agentic RAG=多步检索+条件逻辑判据 | 与 r139-B AgenticRAG 检索循环判重不落；基建事实 |
| 5 | Tool 失败恢复（aicassindra/AI-TLDR/agent-works） | 失败分类四类（transient/invalid/permanent/unknown）；**per-tool retry budget（连续 N 次失败返回终态消息）**；**同 args 同 error 两次=循环检测**；effect journal（INTENT/COMMITTED）；fallback chain | **ED 457 失败 2×2 分类 + 538 per-tool 熔断 + 450 循环终止**已覆盖核心，判重不落 |
| 6 | 多模态提取（ai-tldr/mixpeek/stochasticsandbox） | VLM 替代 OCR；render-everything vs hybrid；多页逐页+跨页表格续接检测；结构化 prompt+JSON schema 示例 | 与 ED 视觉提取三纪律重叠，不落 |
| 7 | 压缩（fp8/morphllm/arXiv） | Hermes 5 阶段（先无 LLM 工具结果剪枝→只摘要中区→抗抖动省<10% 停止）；compaction 删除 vs summarization 改写（路径/错误码不可转述）；Telegraph English 结构化重写 | ctx 质量门/压缩反噬已覆盖核心，ctx 在途不碰 |
| 8 | Deep research（DuMate/AgentDisCo/AgentCPM） | outline 级迭代优化（非最终报告级）；critic-explorer 解耦；graph 动态 planner（DAG+回溯）；drafting-deepening 交替 | 与 doc-writing 结构先行/ED 多 agent 同源，不落 |
| 9 | System prompt（Blck Alpaca/Zylos/Microsoft） | **四层结构：identity 50-200 / capability 800-2000（含 schema）/ behavioral 200-600 / context 100-400 动态**；instruction hierarchy；immutable policy block；失败行为/停止条件显式 | **B4：system prompt 分层预算（落 mts）** |
| 10 | 深度搜索（Gemini/max-gherman/union.ai） | Plan→多源搜索→评估→识别缺口→精化查询→合成带溯源；Reviewer 检查充分性不足则回环 | 与 ED 多 agent 质检回退同源，不落 |

## 二、判重与落地
- **B4 system prompt 分层预算（落 · mts）**：mts 有 Relocation Trick（184 行，管"动态/静态放哪"）与技能三级加载（r140-A，管"技能文件分层"），但"system prompt 本体四层容量分配"无 → 落 mts（工具层），与两者分工注明。
- B2 重规划三分支：ED 1906"失败后三选一 PROCEED/RETRY/REPLAN"同构 → 判重不落。
- B3 per-tool 失败预算+重复检测：ED 457 失败 2×2 分类/538 per-tool 熔断/450 循环终止已覆盖核心 → 判重不落。
- 引用成对验证：wb-doc-writing 引用审计已覆盖 → 不落。
- 压缩抗抖动/Telegraph English：ctx 质量门已覆盖且 ctx 在途不可碰 → 不落。

## 三、功能套件检查
- 三件套：mts 新增"system prompt 分层预算"（与 Relocation Trick/技能三级加载互补成提示结构预算链）；pt 无改动；ctx 在途（WB）不碰 → 套件无需增删。
- 垃圾清理：本轮无临时文件（纯搜索+内存追加）；无 __pycache__ 产生。
