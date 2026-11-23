# r797B 视觉对比解码 VCD — 逐字来源与判非

- 轮次：r797B（2026-11-23）· 模块 PI · 载体 `engineering/multimodal-intelligence`
- 主题：training-free 解码期幻觉缓解；与本技能 §16（CHAIR/POPE 测幻觉）分工——那是测，这是缓解。

## 独点1｜两大幻觉根因 + 噪声放大镜：用噪声主动造「差分布」当对比信号
一手（Leng 等, "Mitigating Object Hallucinations in Large Vision-Language Models through Visual Contrastive Decoding", arXiv:2311.16922v1, 2023-11-28, DAMO Academy Alibaba / NTU / Hupan Lab；WebFetch 200 全文逐字）：
> "we introduce Visual Contrastive Decoding (VCD), a simple and training-free method that contrasts output distributions derived from original and distorted visual inputs. The proposed VCD effectively reduces the over-reliance on statistical bias and unimodal priors, two essential causes of object hallucinations."
> "Object Hallucination ... refers to the phenomenon where LVLMs generate textual content that is semantically coherent but inconsistent with ground-truth objects in the given image."
> "up to +7.4 F1 score boost on POPE and +18% improvement on MME across different LVLM families, including LLAVA-1.5, InstructBLIP, and Qwen-VL"
> Figure 1: "The hallucinated object 'Surfboards' is highlighted in red, and it is eliminated during the generative process by contrasting with the output distribution that favors hallucinations."

中文方法详解（CSDN mars_prime，WebFetch 逐字）与 llm-paper-notes 中文镜像（jiabingyang.cn，WebFetch 逐字）：
- 统计偏差：MSCOCO 高频物体（person/dining table/car）与虚假共现（dining table→person/cup/fork）；语言先验：视觉模糊时退化为文本 next-word（banana→yellow/green 而非实际 black）。
- "噪声图像可以作为一面『幻觉放大镜』"——高斯噪声抬高视觉不确定性，同时放大这两类 bias；"MSCOCO 中高频物体……在噪声图像下的幻觉次数显著增加"。

判据：注入噪声不是为了抗噪，而是主动制造一个「偏向幻觉的分布」作负样本；对比原图与噪声图两个分布，把语言先验/统计偏差引入的幻觉概率剥掉。无需训练、无需外部模型，区别于微调（M-HalDetect/LRV-Instruction 需标注+训练）、后处理（Woodpecker 需外部更强模型）、RLHF（LLaVA-RLHF 需人类反馈+奖励模型）。

## 独点2｜对比公式与自适应可信度约束缺一不可
一手（CSDN mars_prime WebFetch 逐字 + DeepWiki DeGF 实现 WebFetch 逐字 + Lacuna 综述 WebFetch 逐字）：
- 两分布：给定文本 x、视觉 v，原图分布 pθ(y|v,x) 与高斯扰动图 v′ 的分布 pθ(y|v′,x)；对比分布由二者对数概率相减得到，DeepWiki 实现式逐字 `diffs = (1 + α_neg) * next_token_logits - α_neg * next_token_logits_neg`。
- "较大的 α 值表示两个分布之间的差异放大更强（α = 0 减少到常规解码）"；结构等价于无分类器扩散引导 `(1 + α)ε(x, c) − αε(x)`（清晰视觉输入=条件 c）。
- 为何要约束（Lacuna 逐字）："A naive subtraction of logit distributions is dangerous. If the amateur model is very confident in a token that the expert model also likes, the subtraction might leave behind a 'winner' that is actually a low-probability, nonsensical token."；"Before the contrastive step, the decoder identifies a 'plausible' set of tokens—usually those that exceed a certain probability threshold in the expert model's original distribution."
- 论文自适应合理性约束（CSDN 逐字）："具有扭曲视觉输入的输出分布仍然可以维护基本的语言标准和常识推理。不加区别的惩罚可能会不准确地惩罚这些有效的输出并促进难以置信的输出的产生"；"V 是 LVLM 的输出词汇表，β 是 [0,1] 中超参控制下一个令牌分布的截断，β 越大表示截断越激进，仅保留高概率的标记"。

判据：只在原图分布的高概率 token 集合内做对比（自适应截断），否则会误伤噪声图仍保留的语法常识。llm-paper-notes 逐字："β=0 时性能最差"（验证约束不可省）、"β=0.5 时幻觉子集 635.00、感知子集 1474.02，均为最优"。报 VCD 必须写 α、β、扰动方式三件。

## 独点3｜收益与边界须写全，且与 POPE 评测分工
一手（arXiv 2311.16922 全文 + llm-paper-notes 中文镜像 WebFetch 逐字）：
- 收益：POPE 最高 +5.8 Accuracy / +7.4 F1、MME 幻觉子集最高 +18%，跨 LLaVA-1.5 / InstructBLIP / Qwen-VL 三家族；"α∈[0.25,1.0] 范围内 MME 三个子集得分变化很小"（对 α 鲁棒）；"VCD 在 Top-P / Top-K / Greedy / Top-K+Temperature 等 5 种策略上一致有效"；7B 与 13B 基线相当说明堆参数不解决幻觉。
- 边界：只缓解存在性幻觉（与 §16 POPE 只测存在性同源）；局限"仅使用全局高斯噪声作为视觉扰动"；VCD 是评测时解码干预，POPE/CHAIR 是评测法，二者不复用。

判据：报 VCD 须写清 α/β/噪声方式/在哪一族模型与哪个 benchmark 上，且不得把它当「消除幻觉」——论文原词是 "mitigate"。"The incurred human effort and computational cost highlight a pressing need for a simpler but efficient approach." 说明 training-free 是核心卖点，落地时若引入外部模型则已偏离本方法。

## 来源与诚信（判非）
- arXiv 2311.16922 为作者一手（WebFetch 200，全文 89887 字符超时仅取前 15000 字，含标题/作者/日期/摘要/引言/贡献，方法公式细节由 CSDN 与 DeepWiki 一手补齐，如实登记不冒充论文正文取到）。
- CSDN/DeepWiki/Lacuna/llm-paper-notes 为方法细节的独立域逐字。
- 判重：全库 SKILL.md 扫描 `contrastive decoding` / `VCD` / `对比解码` 本体 0；本技能 §15 文图对齐（VQAScore/GenEval）、§16 幻觉评测（CHAIR/POPE）、r795J FastV（视觉 token 剪枝）分别管对齐评分、幻觉测量、推理加速，与本章「解码期缓解」异命题。豆包自留地 WB 0 落地。
