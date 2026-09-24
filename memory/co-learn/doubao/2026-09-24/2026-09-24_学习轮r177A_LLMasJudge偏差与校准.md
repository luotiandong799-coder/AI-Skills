# r177-A LLM-as-Judge 偏差：double-swap 过滤、verbosity 方向因模型而异、fluency 偏差

实拉时间：2026-09-24 20:31
信源：arXiv 2604.23178 judging judges / ai-tldr judge biases / futureagi bias mitigation 2026-05 / aiworkflowlab calibration 2026-08 / zylos fluency 2026-07 / dreaming.press bias 2026-07 / ai-tldr pitfalls / eval.qa biases 2026-02 / eval.qa calibration 2026-02 / chanl 12 biases（judge 组，满 10 站）

## 实拉证据（关键原文）
- ai-tldr：「~25% of comparisons are position-driven rather than quality-driven. Run pairwise twice AB/BA, consistent verdict counts as win; flips discarded as tie.」
- futureagi：「Anything above 5% flip rate is real bias.」
- arXiv 2604.23178：「Pro/Llama/Flash prefer longer (+0.24~0.44); Claude prefers shorter (-0.12); GPT-4o neutral (-0.04).」——verbosity bias 不是统一方向。
- zylos：fluency bias——把"难假"维度设 binary pass/fail gate，不让容易叙述的高分盖过硬伤。

## 独点清单（3 个真独点）

### 独点1：position bias 用 double-swap 一致性过滤（工具层）
- 判据：每对答案比两次（A在前/B在后，再反过来），winner 只在两种顺序下都赢才算赢；翻转的判 tie。~25% 比较是顺序驱动不是质量驱动。flip rate >5% 就是真偏差，要报。成本翻倍但去掉最噪的切片。
- 独有增量（与 r168B eval 区别）：那条讲 eval 流程；本条讲**judge 本身的偏差怎么测怎么消**。
- 提升层：工具。

### 独点2：verbosity bias 方向因 judge family 而异，不能假设都偏好长（工具层）
- 判据：Llama/Pro 偏好长答（+0.24~0.44），Claude 反而偏好短（-0.12），GPT-4o 中立。用哪个 judge 就得测它的长度偏好，不能照搬"长答赢"的经验。rubric 里显式写"正确时偏好简洁"+ 后处理：赢家比输家长 1.5 倍以上要打折。
- 独有增量：打破"所有 judge 都偏好长"的假设——这是实证发现。
- 提升层：工具。

### 独点3：fluency bias——"听着对"≠"真对"，硬维度设 pass/fail gate（工作流层）
- 判据：模型评论文本时，表达流畅的回答分数高，哪怕内容错。解法：把"难假"的维度（实际能力、可验证的事实）设成 binary pass/fail gate，在加权平均之前先过——不让容易叙述的流畅分平均掉硬伤。
- 独有增量：fluency 偏差这个具体类别 + gate 解法。
- 提升层：工作流。

## 判非重复理由
- r168B 讲上线 eval 流程；本条讲 judge 偏差测量与消除，增量 >40%。
