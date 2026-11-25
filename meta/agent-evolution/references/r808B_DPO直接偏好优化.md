# r808B · DPO 直接偏好优化（AI · 2026-11-26 实拉）全文与判非

> AI 模块；≥2 独立域一手（Rafailov et al. 原论文 arXiv:2305.18290 HTML 全文 WebFetch 200 + Hugging Face TRL DPO Trainer 官方文档 WebSearch 逐字），条件等价性反例 arXiv:2605.20834 摘要交叉。
> 主线：把 RLHF 的「奖励模型 + 强化学习」重参数化成对偏好对的一个分类损失；**梯度里的排序误差权重**才是与「等权提升 chosen」的分界线。

## 独点1 · 隐式奖励重参数化：策略即奖励模型

- 原论文 RLHF 目标逐字：`max_{π_θ} E_{x~D,y~π_θ}[r_φ(x,y)] − β D_KL[π_θ(y|x) || π_ref(y|x)]`；「β is a parameter controlling the deviation from the base reference policy π_ref, namely the initial SFT model π_SFT」；约束的作用是「prevents the model from deviating too far from the distribution on which the reward model is accurate, as well as maintaining the generation diversity and preventing mode-collapse to single high-reward answers」。
- DPO 损失（论文式 7，逐字）：`L_DPO(π_θ;π_ref) = −E_{(x,y_w,y_l)~D}[ log σ( β log(π_θ(y_w|x)/π_ref(y_w|x)) − β log(π_θ(y_l|x)/π_ref(y_l|x)) ) ]`。
- 隐式奖励：`r̂_θ(x,y)=β log(π_θ(y|x)/π_ref(y|x))`；论文原话「we fit an implicit reward using an alternative parameterization, whose optimal policy is simply π_θ」。Bradley-Terry + logsigmoid ⇒ 本质是偏好对的二分类，不需要显式 reward model，也不需要 RL/价值网络。
- 与 §r797C PPO 分工：PPO 用 clip 做「软信赖域」、on-policy；DPO 直接优化离线偏好对、无采样策略梯度步骤，二者优化目标/数据来源不同，禁互换措辞；与 §r801C SAC 的最大熵目标更不是一回事。

## 独点2 · 梯度权重是机制核心，不是等权 SFT

- 原论文梯度逐字：`∇_θ L_DPO = −β E[ σ( r̂_θ(x,y_l) − r̂_θ(x,y_w) ) · ( ∇_θ log π(y_w|x) − ∇_θ log π(y_l|x) ) ]`，其中 `σ(r̂(y_l)−r̂(y_w))` 被原文标注为「higher weight when reward estimate is wrong」。
- 逐字解释：「the examples are weighed by how much higher the implicit reward model r̂_θ rates the dispreferred completions, scaled by β, i.e, how incorrectly the implicit reward model orders the completions, accounting for the strength of the KL constraint」；「Our experiments suggest the importance of this weighting, as a naïve version of this method without the weighting coefficient can cause the language model to degenerate」（Appendix Table 3）。
- 判据：报「用了 DPO」必须能说出 β 与参考模型，且检查训练日志中 `rewards/accuracies`（chosen 奖励 > rejected 的比例）与 `rewards/margins`，而不是只看 loss 下降；把 DPO 简化成「chosen 做 SFT、rejected 做负样本」会丢掉这层自适应权重。

## 独点3 · 工程口径、变体与失效边界

- 两阶段流水线（原论文逐字）：①「Sample completions y1,y2∼π_ref(·|x) for every prompt x, label with human preferences to construct the offline dataset」；②「optimize the language model π_θ to minimize L_DPO for the given π_ref and D and desired β」。
- 参考模型初始化：偏好数据来自 `π_SFT` 时「we initialize π_ref=π_SFT whenever available」；没有 SFT 模型时用「π_ref = argmax_π E_{x,y_w~D}[log π(y_w|x)]」（只在 chosen 上最大化似然），以缓「distribution shift between the true reference distribution which is unavailable, and π_ref used by DPO」。
- TRL 官方文档（WebSearch 逐字）：先训 SFT「to ensure the data we train on is in-distribution for the DPO algorithm」；数据三列 `prompt`/`chosen`/`rejected`，同一 prompt 可有多组；`DPOTrainer` 需 `ref_model` 算隐式奖励，model 与 ref_model「need to have the same architecture」；`beta=0.1` 默认、是 DPO loss 的温度参数「typically something in the range of 0.1 to 0.5」，「We ignore the reference model as beta -> 0」；记录 `rewards/chosen`、`rewards/rejected`、`rewards/accuracies`、`rewards/margins`。
- 变体不是同义词：`sigmoid`（默认，BT+logsigmoid）/`hinge`（SLiC-RSO，β 是 margin 倒数）/`ipo`（修 DPO 过拟合，β 是 chosen-rejected log-ratio gap 倒数，loss 在 completion 上取平均而非求和）/`cDPO`（`label_smoothing` 0–0.5 建模噪声标签）/`robust`（偏好噪声无偏估计）。换 loss 必须连 β 的语义一起改口径。
- 边界（原论文 Limitations 逐字）：OOD 泛化相对显式奖励模型「more comprehensive study is needed」；「how does reward over-optimization manifest in the direct preference optimization setting」未解；只评到 6B，「exploration of scaling DPO to state-of-the-art models orders of magnitude larger is an exciting direction」。
- 条件等价反例（arXiv:2605.20834 摘要 WebSearch 逐字）：DPO 与 RLHF 的等价性「conditional rather than universal」，依赖「the RLHF-optimal policy must prefer human-preferred responses」；该假设失败时「DPO optimizes relative advantage over the reference policy rather than absolute alignment with human preferences」，会出现「policies decrease DPO loss while preferring dispreferred responses」；另引 Fisch et al. 2024 隐式奖励过拟合趋向无穷大、Lin et al. 2024 分布漂移下泛化显著差于显式奖励模型。⇒ 只报 loss 下降不足以证明偏好对齐。

## 来源与诚信

- `https://arxiv.org/html/2305.18290v2`（Rafailov et al. 原论文 HTML 全文，WebFetch 200 逐字：式 3/式 7、梯度权重、两步流水线、π_ref 初始化与 fallback、β 含义、Limitations）——第一独立域·原论文一手。
- `https://huggingface.co/docs/trl/v0.8.0/dpo_trainer`（Hugging Face TRL 官方文档 WebSearch 逐字：SFT 前置、prompt/chosen/rejected 格式、ref_model 与同架构要求、β 0.1–0.5 与 β→0、sigmoid/hinge/ipo/cDPO、日志四指标）——第二独立域·框架官方一手；WebFetch 直连失败（fetch failed）已如实登记，未冒充全文。
- `https://arxiv.org/html/2605.20834`（条件等价性/CPO 摘要 WebSearch 逐字）——第三独立域交叉，仅作边界证据不充当主方法来源。
- 判非：全库 SKILL.md + module-memory + co-learn 对 `DPO`/`Direct Preference Optimization`/`直接偏好优化` 0 专节（此前命中均为 adopt 等子串或对话摘要）；与 §r797C PPO、§r801C SAC、§r772A 因果森林、§r788A PBRS 均异命题。豆包自留地 WB 0 落地。按 rules/07 判「增＝加厚现有」，0 新建。
