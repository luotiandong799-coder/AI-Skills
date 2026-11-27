# r812B · GRPO 组相对策略优化：用组内相对奖励当基线，去掉 critic

> AI · 2026-11-27 独立实拉，≥2 独立域一手交叉（arXiv:2402.03300 HTML 全文逐字公式 + abs 摘要；多域教学页交叉），3 独点。
> 定位：§r797C PPO 管「用 clip 限制每次策略更新步子」，§r801C SAC 管「熵进目标换 off-policy 样本效率」，§r808B DPO 管「偏好对分类损失不经显式奖励模型」；本章管**PPO 的优势基线从哪来**——用一个问题的多个采样输出的组内相对分数替代需单独训练的 value 网络。§r768A 明确把「GRPO 去 critic 路线」标为异命题留给后续，本轮补上。

## 独点1 动机与 removed critic：为什么 value 网络在 LLM 里又贵又难
- arXiv:2402.03300 摘要逐字：「we introduce Group Relative Policy Optimization (GRPO), a variant of Proximal Policy Optimization (PPO), that enhances mathematical reasoning abilities while concurrently optimizing the memory usage of PPO」；§4.1.1「GRPO foregoes the critic model, instead estimating the baseline from group scores, significantly reducing training resources」；Figure 4 caption 同义。
- 原文给出的双重理由：① 「the value function employed in PPO is typically another model of comparable size as the policy model, it brings a substantial memory and computational burden」——critic 常与 policy 同规模，等于多养一个大模型；② 「in the LLM context, usually only the last token is assigned a reward score by the reward model, which may complicate the training of a value function that is accurate at each token」——奖励稀疏在末 token，逐 token 价值函数难训准。第三点：PPO 标准做法为防奖励模型过优化，在 reward 里对每个 token 加来自参考模型的 KL penalty。
- 判据：GRPO 省的是**价值网络这一份显存与训练资源**，不是省掉奖励信号，也不等于「无需任何 critic 类基线」——基线从 learned value 换成 group score 估计。中文教学页（CSDN/cSDN）称省 40–50% 训练内存，数值挂教学页口径，不作普适承诺。

## 独点2 机制对象：组内奖励归一化优势 + 目标函数里的 KL（逐字公式）
- 采样与优势（§4.1.2 Outcome Supervision）：对每个问题 q 从旧策略 π_θ_old 采样一组输出 {o_1,...,o_G}，奖励模型给 G 个奖励 r={r_1,...,r_G}；「these rewards are normalized by subtracting the group average and dividing by the group standard deviation」，把归一化奖励放到每个输出末尾并赋给该输出所有 token：
  `Â_{i,t} = r̃_i = (r_i − mean(r)) / std(r)`
  「The group relative way ... aligns well with the comparative nature of rewards models, as reward models are typically trained on datasets of comparisons between outputs on the same question.」
- 目标函数（式 3，逐字 LaTeX）：
  `J_GRPO(θ)=E_{q~P(Q), {o_i}~π_θ_old(O|q)} [ (1/G)Σ_{i=1}^G (1/|o_i|)Σ_{t=1}^{|o_i|} { min[ (π_θ(o_it|q,o_<t)/π_θ_old(o_it|q,o_<t))·Â_it , clip(ratio,1−ε,1+ε)·Â_it ] − β·D_KL[πθ||π_ref] } ]`
  ε、β 是超参；Â_it 只由组内相对奖励算出。「instead of adding KL penalty in the reward, GRPO regularizes by directly adding the KL divergence between the trained policy and the reference policy to the loss, avoiding complicating the calculation of Â_it」——KL 从 reward 项挪到 loss 项，与 PPO 的位置不同。
- KL 无偏估计（式 4，Schulman 2020）：`D_KL[πθ||π_ref] = (π_ref/π_θ) − log(π_ref/π_θ) − 1`，「which is guaranteed to be positive」。判据：报「用了 GRPO」写 G（组大小）/归一化方式/ε/β/KL 放在 loss 还是 reward 四件。
- 过程监督版（§4.1.3）：过程奖励模型对每步打分，R={每输出各步奖励}，同样按组均值/标准差归一化 `r̃_i^{index(j)}=(r_i^{index(j)}−mean(R))/std(R)`，token 优势取「其后所有步归一化奖励之和」`Â_it=Σ_{index(j)≥t} r̃_i^{index(j)}`。与 outcome 版的分工：outcome 只在输出末给一个奖励，复杂数学任务监督不够密。

## 独点3 边界、误解与退化条件
- 两个常见误解（toolnavs/aigcbaba 教学页交叉）：① 「GRPO 不用奖励模型」——不用的是**单独的 learned critic/value 网络**，奖励本身仍在，改成规则可验证（数学最终答案对错、代码测试通过与否）；② 当成通用训练法——开放式写作/创意任务无可自动判定的裁判，奖励定不下来就不适用。判据：先看「答案能否不靠模型自己自动验证对错」，能才谈 GRPO。
- 组内信号消失：同一题采样的一组输出**全对或全错**时 reward 拉不开差距，std→0 则 Â 退化，学习信号消失；DeepSeek-R1 因此依赖题目难度分布——太简单（全对）/太难（全错）都学不到。判据：报告须写组的正确率分布，不能只报均值奖励。
- 评价偏误：可验证奖励仍取决于判题器与测试覆盖，判题漏洞/弱测试/格式投机可造成 reward hacking → 「模型的输出呈现更长的解题、反思与验算行为；应以正确率和泛化评测证明收益，不能把『更长』本身当作推理更强」。「GRPO 不天然保证更稳定」——组内归一化免去 learned critic，但估计质量受组大小、采样分布和奖励方差影响，不能笼统称为无偏或必然更稳。
- 判重与分工：`GRPO`/`组相对策略优化`/`group relative` 在 agent-evolution 本体仅 §r768A 一句「GRPO 去 critic 路线（异命题，留给后续）」+ GEPA 来源一句「超 GRPO ~10%」，均非机制专节；module-memory AI 0 条、co-learn 标题级 0。与 §r797C PPO（clip 更新步幅）/§r801C SAC（熵目标 off-policy）/§r808B DPO（偏好对分类无 RL 步）/§r768A GAE（优势估计的偏差-方差旋钮）四者分工：本章管基线与资源，不复用。豆包自留地 WB 0 落地。本轮按「增＝加厚现有」0 新建 / 0 合并 / 0 删除。

## 来源与诚信
- arXiv:2402.03300《DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models》HTML v3 `https://arxiv.org/html/2402.03300v3`（WebFetch 200 全文逐字：摘要/§4.1.1 动机+式3+式4/§4.1.2 outcome 归一化/§4.1.3 process 归一化）与 abs 页 `https://arxiv.org/abs/2402.03300`（WebFetch 200 逐字摘要，Submitted 2024-02-05 / v3 2024-04-27）——第一独立域，原论文一手。
- toolnavs.com《GRPO 是什么》+ offer.aigcbaba.com《什么是 GRPO》（WebSearch 逐字：组内均值基线/std 归一化公式/全对全错信号消失/可验证奖励边界/两个误解）、rainbook CSDN《GRPO 详解》WebSearch 逐字（DeepSeekMath 2024-02 首发、40–50% 显存教学页口径）——第二独立域，教学交叉。
- alphaxiv.org/abs/2609.04063《隐藏在 GRPO 中的虚假优势》WebSearch 逐字（SIGNBALANCE/Search-R1 场景虚假优势大）作边界交叉登记，未采纳为机制来源。
- 数值 40–50% 显存、10%/20% 等挂教学页/GEPA 来源口径，不作本技能硬结论。
