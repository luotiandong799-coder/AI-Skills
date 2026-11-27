# r816A · MLA 多头潜在注意力（Multi-head Latent Attention）逐字与判非

> 落地：defaults/ci-context SKILL.md 2.12.0 → 2.13.0（加厚现有，0 新建）；共学路由 CI。实拉 2026-11-27，≥2 独立域一手交叉。

## 一手来源（URL + 日期 + 抓取方式）

1. **arXiv:2405.04434**《DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model》，DeepSeek-AI，Submitted 7 May 2024 v1 / last revised 19 Jun 2024 v5 — `https://arxiv.org/abs/2405.04434` WebFetch 200 摘要逐字。**第一独立域·原论文官方一手**。
2. **苏剑林《MLA 的本质》** `https://spaces.ac.cn/archives/10091` WebFetch 200 全文逐字推导（行向量记号 c_i=x_i W_c）。**第二独立域·一手推导全文**。
3. CSDN `https://blog.csdn.net/wuud__/article/details/166484251`、messywind `https://blog.messywind.top/posts/mlmla`、DeepSeek 技术社区 `https://deepseek.csdn.net/6aa9416b8f401d3626607566.html`、百度百科词条（WebSearch 逐字）——第三～五域交叉（立场登记，不冒充论文原文）。

## 独点1：低秩 KV 联合压缩，缓存只存 latent 不存展开的头

原文摘要逐字：「DeepSeek-V2 adopts innovative architectures including Multi-head Latent Attention (MLA) and DeepSeekMoE. **MLA guarantees efficient inference through significantly compressing the Key-Value (KV) cache into a latent vector**, while DeepSeekMoE enables training strong models at an economical cost through sparse computation.」；「Compared with DeepSeek 67B, DeepSeek-V2 achieves significantly stronger performance, and meanwhile saves 42.5% of training costs, **reduces the KV cache by 93.3%, and boosts the maximum generation throughput to 5.76 times**」；236B 总参 / 21B 每 token 激活 / 128K 上下文 / 8.1T tokens 预训练。

机制（苏剑林列向量记号，等价 DeepSeek 原记号）：
- `c_t^{KV} = W^{DKV} h_t`（W^{DKV}∈R^{d_c×d}，d_c≪d；DeepSeek-V2 取 d_c=512）
- `k_{t,i}^{C} = W_i^{UK} c_t^{KV}`, `v_{t,i}^{C} = W_i^{UV} c_t^{KV}`（上投影恢复多头表达）
- 推理缓存只存 `c_t^{KV}` 而非展开的 n_h 份 K/V。

维度算例（DeepSeek-V2：d=5120, h=128, d_k=d_v=128）：
- MHA 每 token `h(d_k+d_v)=128×(128+128)=32768`
- MLA 每 token `d_c + d_r = 512 + 64 = 576`（d_r 为解耦 RoPE key，见独点3），约 **57×**
- 苏剑林逐字：「MLA的KV Cache大小跟h无关，增大h只会增加计算量和提升模型能力，但不会增加KV Cache，所以不会带来速度瓶颈。」

判据：MLA 与 GQA 是不同轴——GQA 减「存几份」（每份维度不变），MLA 压「每份体积」（低秩 latent）。苏剑林逐字定位：「MLA被视为GQA的一般化，它用投影矩阵的方式替代了GQA的分割、重复，并引入了一个恒等变换技巧来可以进一步压缩KV Cache，同时采用了一种混合方法来兼容RoPE。」；「MLA的本质改进不是低秩投影，而是低秩投影之后的工作。」

## 独点2：矩阵吸收是推理期关键，RoPE 的位置依赖与之直接冲突

无 RoPE 时 attention logit 恒等变换（苏剑林逐字）：
`q_t^{(s)} k_i^{(s)T} = (x_t W_q^{(s)})(c_i W_k^{(s)})^T = x_t (W_q^{(s)} W_k^{(s)T}) c_i^T`
⇒ K 的上投影吸收进 Q 侧、V 的上投影吸收进输出投影，推理时无需把 c_i 解压成 K/V 就能算 attention，KV cache 只需存 c_i（c_i 与头无关、所有头共享=推理期恒等为一个 MQA）。苏剑林逐字：「此时KV Cache只需要存下所有的c_i就行」「c_i跟^{(s)}无关，也就是说是所有头共享的，即MLA在推理阶段它可以恒等变换为一个MQA。」

RoPE 冲突：RoPE 是位置相关的分块对角矩阵 R_m R_n^T=R_{m-n}。若直接给压缩 K 加 RoPE：
`q_t^{(s)} k_i^{(s)T} = x_t (W_q^{(s)} R_{t-i} W_k^{(s)T}) c_i^T`
中间夹着 `R_{t-i}`（依赖相对位置），无法合并成固定投影矩阵。苏剑林逐字：「这里的W_q^{(s)}R_{t-i}W_k^{(s)T}就无法合并为一个固定的投影矩阵了（跟位置差t-i相关），从而MLA的想法无法结合RoPE实现。」；「MLA不是不能加RoPE，而是加了RoPE之后无法用恒等变换技巧来减少KV Cache。」

判据：说「MLA 直接套 RoPE 即可」错；必须走解耦 RoPE。

## 独点3：解耦 RoPE + Q 也低秩但不属于 cache

DeepSeek 解法：Q、K 各拆 content（走低秩压缩与矩阵吸收）与 RoPE part（专属承载位置信息）：
- `k_i^{(s)} = [ c_i W_{kc}^{(s)},  x_i W_{kr}^{cancel(s)} R_i ]`（RoPE key 无 (s) 上标=所有 head 共享，即 k_t^R）
- `q_i^{(s)} = [ c_i' W_{qc}^{(s)},  c_i' W_{qr}^{(s)} R_i ]`，`c_i' = x_i W_c' ∈ R^{d_c'}`，**d_c'=1536**（与 d_c=512 不同，苏剑林逐字强调「其输入还是 x_i 而不是 c_i，这里保持了原论文的设置，不是笔误」）
- 每 token cache = `c_i (512) + k_t^R (64) = 576`，d_r=d_k/2=64（「相比原本的 d_c=512，增加的幅度不大」）
- Q 也压缩但 Q 不缓存，压缩只为省训练参数与激活显存（messywind 逐字）

判据：报 MLA cache 数字须带 d_c/d_r/h/d 与对比基线（MHA 32768），不能只说「压缩 57 倍」；低秩还原有信息损失，d_c 足够大才忽略（CSDN 立场登记）；与 §r802C MQA/GQA（减 KV 头数）、§r775B KIVI（位宽）、§r767B H2O/SnapKV（token 去留）、§r783B placement（块放哪）、§r807A 投机解码（解码调度）正交可叠加——那些改「存几份/几位/哪些/放哪/几次调用」，本节改「每份压成低秩 latent + 用解耦 RoPE 保住矩阵吸收」。

## 判非与去重

- `MLA`/`多头潜在注意力`/`latent`/`低秩` 在 ci-context 本体仅 §r802C 独点3 一句「DeepSeek MLA 是同一问题的另一解（压成共享 latent 而非减头数，memx/ai360xpert 逐字）」，非机制专节；Grep 全库其余命中在 wb-context-compressor（豆包自留地）/co-learn/采购域，WB 0 落地。
- 与同模块 §r802C MQA/GQA、§r775B KIVI、§r767B H2O/SnapKV、§r783B KV placement 均为异命题（分工见独点3）；与 r811A 分词器、r807A 投机解码不复用。
- 按 rules/07「增＝加厚现有」，本轮 0 新建 / 0 合并 / 0 删除。

## 诚信登记

- arXiv:2405.04434 摘要数字（−93.3% KV cache / 5.76× throughput / −42.5% training）为论文官方原文逐字；对比基线是 DeepSeek 67B，不写成「比所有 MHA 模型快 5.76 倍」。
- 苏剑林为博客逐式推导（非 DeepSeek 官方论文正文），行向量记号与论文列向量记号已做符号对照表，立场登记不冒充原文。
- 56.9×/57× 是 d_c=512/d_r=64/h=128 设定下的算例，不是普适倍率。
- 百度百科「1.8–2.3× 推理速度 / KV 降 42–57%」「Kimi K2/GLM-5/Ling 2.5 采纳」为二手口径，立场登记。
