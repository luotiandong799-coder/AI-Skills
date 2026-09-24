# r170-C LLM-as-Judge 的偏差图谱与校正纪律

实拉时间：2026-09-24 19:52
信源：arXiv 2604.23178（Judging the Judges）+ OpenReview QF4lAmG4zc / ai-tldr / aiworkflowlab / futureagi / jatinbansal / prakashkagitha / compelframework / qaskills.sh / dreaming.press（bias 组）；arXiv 2510.16727 Beacon / arXiv 2603.24586 代码评估 / iovstudio judge-bench / arXiv 2604.06996 rubric self-preference / AWS Nova rubric / UNH llmjudge-book / mllm-judge / arXiv 2606.05183 sycophancy 审计（校准组）

## 实拉证据（关键原文）
- 四种生产 bias（aiworkflowlab 2026-08）：position bias（偏向第一选项，15-30% skew）、verbosity bias（偏向长答案，~15% inflation）、self-preference（偏向同家族输出，3-10%）、sycophancy（同意问题里的预设）。修法：order-swapping / length-normalized rubric / cross-family judging / premise-neutral prompt。
- arXiv 2604.23178 关键反直觉发现：**verbosity bias 跨模型异质**——Llama/Gemini Pro/Flash 偏好长（+0.24~+0.44），**Claude Sonnet 4 反而偏好短（-0.12）**，GPT-4o 基本中性（-0.04）。不能假设所有 judge 都偏长。
- Position bias 实测（dreaming.press/compelframework）：GPT-4 两答案互换顺序后，判定一致率仅 ~65%；修法=每次 pairwise 判两次、互换顺序、两次一致才算赢（2x cost 但消除 bias）。
- Judge 与人的 agreement 上限（arXiv 2603.24586）：最强 LLM judge 比多数人类 agreement 低 12-23 个百分点；fine-tuned judge 不必然优于通用模型；个性化任务二选一准确率仅 ~70%、某些场景 <60%。
- arXiv 2604.06996：rubric-based 评估中，输出不满足 rubric 时，模型对自家输出误判"满足"的概率高 50%+；ensemble 多 judge 能减但不能消除。
- UNH llmjudge-book：judge 与被评系统共享信号=**循环论证（circularity）**；sycophancy 奖励从众而非质量；judge 有知识天花板。

## 独点清单（3 个真独点）

### 独点1：四种 judge bias 各有专属修法，不能一刀切（可复用 Skill 层）
- 判据：position bias → pairwise 必跑两次互换顺序，两次一致才算赢；verbosity bias → rubric 显式写"不偏好长答案"并加 conciseness 评分维度；self-preference → judge 必须跨家族（不用被评模型同厂）；sycophancy → premise-neutral prompt，把问题里的预设摘掉再判。
- 关键增量：verbosity bias 方向不固定——Claude Sonnet 4 反而偏好短答案（arXiv 2604.23178），**不能写死"judge 都偏好长"**，要 length-aware 实测自家 judge 的方向再加反向 rubric。
- 与 r168-B golden task 互补：那条管回归集怎么建，本条管**用 LLM 当评委时评委自己偏在哪、怎么校**。
- 提升层：可复用 Skill（评估）。

### 独点2：LLM judge 与人的 agreement 有硬上限——别把它当真值（可复用 Skill 层）
- 判据：最强 judge 比多数人类 agreement 低 12-23 个百分点；个性化/偏好类任务准确率 ~70%。判据：LLM judge 分数只用于**相对排序和回归监控**，不用于断言"这个答案客观正确"；高风险场景保留人审，不把 judge 通过=验收通过。
- 独有增量：fine-tuned judge 不必然优于通用模型（arXiv 2603.24586）——花钱 fine-tune judge 不一定买得到可靠性；judge 与被评系统共享同一家模型时存在 circularity，必须跨家族。
- 提升层：可复用 Skill。

### 独点3：Self-preference 在 rubric 打分里也存在——自家输出被虚高（工具/工作流层）
- 判据：rubric-based 打分不是 pairwise 就安全——输出不满足 rubric 时，模型对自家输出误判"满足"的概率高 50%+（arXiv 2604.06996）；ensemble 多 judge 能减但不能消除。
- 独有增量（与独点1 区别）：独点1 修 pairwise 场景，本条修**pointwise rubric 打分**场景——我们写 skill 自评时如果用同家族模型打 rubric 分，自家 skill 的分会被系统性抬高。
- 提升层：工具/工作流。

## 判非重复理由
- r168-B 覆盖 golden task 回归/评分门禁；本条 3 独点落在 judge bias 谱、judge 与人 agreement 上限、rubric self-preference，与已有条目增量 >40%。
- Beacon/个性化 judge/Gemini sycophancy 审计多源重叠 >60% 不落，只留证据。
